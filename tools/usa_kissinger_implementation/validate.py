# IMPERIA COLD WAR — Independent bounded installed-source validator.
"""Check current Kissinger output without regenerating gameplay content."""
from __future__ import annotations
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

P='COLDWAR_USA_KS_';STEM='COLDWAR_USA_kissinger'
REGIONAL_BASELINE={'mdcw_infantry_weapons_1940','mdcw_util_vehicle_1940','mdcw_cnc_equipment_1940','mdcw_support_weapons_1940','mdcw_special_forces_1940','mdcw_camouflage_1940','mdcw_body_armor_1945','mdcw_anti_tank_1940','mdcw_nsb_anti_air_1940','mdcw_anti_air_1940'}
OUT=ROOT/'docs/design/usa_kissinger_20261028/IMPLEMENTATION_VALIDATION_STATIC.json'


def walk(items):
    for node in items:
        yield node
        yield from walk(node.children())


def direct(body,key):return next((n for n in body if n.key==key),None)


def validate():
    findings=[];checks=[];hashes={}
    def require(value,message,path='',severity='error'):
        if not value:findings.append(dict(severity=severity,message=message,path=str(path)))
        return bool(value)
    def read(relative):
        path=ROOT/relative
        if not require(path.exists(),'Required generated file is missing',relative):return ''
        raw=path.read_bytes();hashes[str(relative)]=hashlib.sha256(raw).hexdigest()
        require(raw.startswith(b'\xef\xbb\xbf')==str(relative).endswith('.yml'),'Incorrect UTF-8 BOM contract',relative)
        text=raw.decode('utf-8-sig')
        expected=1 if str(relative).endswith('.yml') else 0
        lines=text.splitlines()
        require(len(lines)>expected and lines[expected].startswith('# IMPERIA COLD WAR — '),'Missing exact file-start project marker',relative)
        return text
    def parse(relative):
        text=read(relative)
        try:return nodes(text)
        except Exception as e:require(False,'Script parser failed: '+str(e),relative);return []
    paths={kind:f'common/{kind}/{STEM}.txt' for kind in ('scripted_effects','scripted_triggers','ideas','decisions','on_actions','scripted_guis','opinion_modifiers','scripted_localisation')}
    ast={kind:parse(path) for kind,path in paths.items()}
    events=parse(f'events/{STEM}.txt')+parse('events/COLDWAR_USA_triangular.txt')+parse('events/COLDWAR_USA_triangular_statecraft.txt')
    categories=parse(f'common/decisions/categories/{STEM}.txt')
    gui=parse(f'interface/{STEM}.gui');gfx=parse(f'interface/{STEM}.gfx')+parse('interface/COLDWAR_USA_triangular.gfx')
    localisation=read(f'localisation/english/{STEM}_l_english.yml')
    loc_rows=re.findall(r'^\s*([^#\s:]+):\d*\s+"(.*)"\s*$',localisation,re.M)
    loc=dict(loc_rows)
    require(len(loc_rows)==len(loc),'Duplicate English localisation keys',f'localisation/english/{STEM}_l_english.yml')
    for key,value in loc_rows:
        require(not re.search('[\u2013\u2014]',value),'New player text contains a prohibited dash: '+key)
    checks.append('Target files parse and encoding/marker/localisation contracts checked')
    fx={n.key:n for n in ast['scripted_effects']};tr={n.key:n for n in ast['scripted_triggers']}
    def expanded_effect(node,seen=None):
        seen=set() if seen is None else seen
        for current in walk([node]):
            yield current
            if current.key in fx and current is not fx[current.key] and current.key not in seen:
                seen.add(current.key)
                yield from expanded_effect(fx[current.key],seen)
    for kind in ('scripted_effects','scripted_triggers'):
        require(len({n.key for n in ast[kind]})==len(ast[kind]),'Duplicate top-level provider in '+kind,paths[kind])
    ideas={n.key:n for root in ast['ideas'] for country in root.children() if country.key=='country' for n in country.children()}
    opinions={n.key:n for root in ast['opinion_modifiers'] for n in root.children()}
    decisions={n.key:n for category in ast['decisions'] for n in category.children() if direct(n.children(),'complete_effect')}
    for key,decision in decisions.items():
        if key.endswith(('_cancel','_terminate','_end_programme','_end_rights','_pause')) or re.search(r'_(?:end_liaison|stand_down|withdraw_rights)_',key):
            ai=direct(decision.children(),'ai_will_do')
            require(ai and field(ai.children(),'factor')=='0','Standing arrangement can be ended by an unconditional AI weight: '+key)
    event_ids={field(n.children(),'id') for n in events if n.key in ('country_event','news_event')}
    tree_path='common/national_focus/USA_1970.txt';tree_raw=(ROOT/tree_path).read_bytes();tree_text=tree_raw.decode('utf-8-sig')
    hashes[tree_path]=hashlib.sha256(tree_raw).hexdigest()
    tree=next(n for n in nodes(tree_text) if n.key=='focus_tree')
    focus_rows=[n for n in tree.children() if n.key in ('focus','joint_focus')]
    all_focuses={field(n.children(),'id'):n for n in focus_rows}
    require(len(focus_rows)==len(all_focuses),'Duplicate USA focus ID',tree_path)
    new={key:value for key,value in all_focuses.items() if str(key).startswith(P)}
    design=json.loads((ROOT/'docs/design/usa_kissinger_20261028/DESIGN.json').read_text(encoding='utf-8'))
    approved={n['id']:n for n in design['nodes'] if not n['existing']}
    triangle=json.loads((ROOT/'tools/usa_kissinger_implementation/triangular_approved.json').read_text(encoding='utf-8'))
    for n in triangle['nodes']:
        if n.get('existing'):continue
        groups=[n['parents']] if n.get('parent_mode')=='OR' else [[p] for p in n.get('parents',[])]
        approved[P+n['id']]=dict(n,prerequisite_groups=groups,exclusive=[n['exclusive']] if n.get('exclusive') else [])
    require(new.keys()==approved.keys(),'Installed statecraft IDs differ from the approved original and triangular designs',tree_path)
    require(len(all_focuses)==301+len(approved),'Installed USA focus count differs from the base and approved additions',tree_path)
    graph={}
    for fid,n in all_focuses.items():
        parents=[str(c.value) for p in n.children() if p.key=='prerequisite' for c in p.children() if c.key=='focus']
        graph[fid]=parents
        for parent in parents:require(parent in all_focuses,'Missing parent '+parent+' for '+fid,tree_path)
    active=set();done=set()
    def visit(fid):
        if fid in active:require(False,'Cyclic focus graph at '+fid,tree_path);return
        if fid in done:return
        active.add(fid)
        for parent in graph.get(fid,[]):visit(parent)
        active.remove(fid);done.add(fid)
    for fid in graph:visit(fid)
    for fid,n in new.items():
        require(fid in loc and fid+'_desc' in loc,'Missing new focus name/description '+fid)
        require(direct(n.children(),'allow_branch') is None,'New focus unexpectedly hides a branch '+fid)
        actual_groups=[[str(c.value) for c in p.children() if c.key=='focus'] for p in n.children() if p.key=='prerequisite']
        expected_groups=[[P+x for x in group] for group in approved[fid].get('prerequisite_groups',[])]
        require(actual_groups==expected_groups,'Prerequisite grouping differs from approved design: '+fid)
        exclusive=[str(c.value) for p in n.children() if p.key=='mutually_exclusive' for c in p.children() if c.key=='focus']
        require(set(exclusive)=={P+x for x in approved[fid]['exclusive']},'Exclusions differ from approved design: '+fid)
        for other in exclusive:
            other_node=all_focuses.get(other)
            if other_node:
                reverse={str(c.value) for p in other_node.children() if p.key=='mutually_exclusive' for c in p.children() if c.key=='focus'}
                require(fid in reverse,'Non-reciprocal exclusion '+fid+' / '+other)
        require(direct(n.children(),'ai_will_do') is not None,'Missing native focus AI weight '+fid)
    checks.append('Installed full USA graph, both approved design snapshots, groups and reciprocal choices checked')
    # New-namespace references are a closed set. Native helpers/assets are
    # checked at their actual owner where material rather than blanket allowed.
    all_nodes=[x for rows in ast.values() for x in walk(rows)]+list(walk(events))+list(walk(categories))+list(walk(new.values()))
    known=set(fx)|set(tr)
    for n in all_nodes:
        if isinstance(n.value,str):
            require(not re.fullmatch(r'[+-]?\.\d+',n.value),'Native numeric literal requires an explicit leading zero: '+n.value)
        if n.key=='check_variable':
            require(not any(child.op in ('>=','<=','!=') for child in n.children()),'Native check_variable requires an expanded compare for inclusive or unequal operators')
        if n.key=='add_equipment_to_stockpile' and field(n.children(),'type')=='infantry_weapons_1':
            amount=str(field(n.children(),'amount',''))
            if amount and not amount.startswith('-'):
                require(field(n.children(),'producer')=='USA','Positive American aid must use the actual USA equipment producer in runtime and previews')
        if n.key.startswith(P) and n.value in ('yes','no'):
            require(n.key in known,'Undefined namespace helper '+n.key)
        if n.key in ('add_ideas','remove_ideas') and isinstance(n.value,str) and n.value.startswith(P):
            require(n.value in ideas,'Undefined national spirit '+n.value)
        if n.key=='unlock_decision_tooltip' and isinstance(n.value,str) and n.value.startswith(P):
            require(n.value in decisions,'Undefined decision unlock '+n.value)
        if n.key=='country_event':
            eid=field(n.children(),'id')
            if str(eid).startswith(('COLDWAR_USA_KS.','COLDWAR_USA_TD.','COLDWAR_USA_TDSP.')):require(eid in event_ids,'Undefined country event '+str(eid))
        if n.key=='add_opinion_modifier':
            modifier=field(n.children(),'modifier')
            if str(modifier).startswith(P):require(modifier in opinions,'Undefined native opinion modifier '+str(modifier))
        if n.key in ('custom_effect_tooltip','tooltip','title','desc','name','localization_key') and isinstance(n.value,str) and n.value.startswith(P) and not n.value.startswith(P+'Get'):
            require(n.value in loc,'Missing referenced English localisation '+n.value)
        if n.key in ('title','desc','name') and isinstance(n.value,str) and n.value.startswith(('COLDWAR_USA_TD.','COLDWAR_USA_TDSP.')):
            require(n.value in loc,'Missing triangular event localisation '+n.value)
    checks.append('Namespace effects, triggers, ideas, decisions, events and visible localisation references checked')
    for n in walk(ast['scripted_effects']):
        if isinstance(n.value,str) and re.fullmatch(r'[+-]?(?:\d*\.)?\d+',n.value):
            require('.' not in n.value or len(n.value.split('.')[1])<=5,'Native numeric literal has more than five fractional digits: '+n.value)
    # Native treasury application must still be the inspected native provider,
    # not an invented monetary modifier or a tooltip-only promise.
    budget=(ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8-sig')
    treasury=next(n for n in nodes(budget) if n.key=='modify_treasury_effect')
    require(any(n.key=='has_country_flag' and n.value=='MD_skip_treasury_cost' for n in walk([treasury])),'Native treasury skip guard changed')
    require(any(n.key=='add_to_variable' and field(n.children(),'treasury')=='treasury_change' for n in walk([treasury])),'Native treasury consumer changed')
    money=(ROOT/'common/scripted_effects/00_money_system.txt').read_bytes()
    hashes['common/scripted_effects/00_money_system.txt']=hashlib.sha256(money).hexdigest()
    require(not money.startswith(b'\xef\xbb\xbf'),'Shared money system has a BOM')
    money_nodes=nodes(money.decode('utf-8'))
    for name,total,contribution in [('calculate_additional_income_rate','additional_income_rate',P+'weekly_income'),('calculate_additional_expense_rate','additional_expenses_rate',P+'weekly_expense')]:
        provider=next(n for n in money_nodes if n.key==name)
        calls=[n for n in walk([provider]) if n.key==P+'calculate_streams']
        additions=[n for n in walk([provider]) if n.key=='add_to_variable' and field(n.children(),total)==contribution]
        require(len(calls)==1 and len(additions)==1,'New weekly contribution must enter native '+name+' exactly once')
        if name=='calculate_additional_expense_rate':
            inflation=[n for n in walk([provider]) if n.key=='multiply_variable' and field(n.children(),total)=='additional_expenses_inflation']
            require(inflation and additions and additions[0].start>max(n.start for n in inflation),'Nominal KS expenses must enter after native inflation compensation')
    checks.append('Weekly literals, real native treasury provider and single native income/expense integration checked')
    # All prospective modifier numbers must be present directly alongside the
    # spirit names, outside real acceptance and suspension guards.
    for key,node in fx.items():
        if not (key.startswith(P+'deal_') and key.endswith('_preview')):continue
        if key==P+'deal_moscow_preview':
            require(any(n.key=='icwt_focus_preview_7' and n.value=='yes' for n in walk([node])),'Legacy Moscow preview must delegate to the real consultation paper')
            treaty=nodes((ROOT/'common/scripted_effects/ICW_superpower_treaties.txt').read_text(encoding='utf-8'))
            native=next((n for n in treaty if n.key=='icwt_focus_preview_7'),None)
            grants=[n for n in walk([native]) if n.key=='add_ideas' and n.value=='icwt_spirit_7'] if native else []
            require(len(grants)==2,'Delegated Moscow preview lacks both treaty membership spirits')
            continue
        offered=[n for n in walk([node]) if n.key=='add_ideas' and str(n.value).startswith(P+'deal_')]
        require(len(offered)>=2,'Prospective agreement lacks both named spirits: '+key)
        require(not any(n.key in ('if','else_if') for n in walk([node])),'Prospective agreement numbers are guarded by live conditions: '+key)
        for grant in offered:
            idea=ideas.get(grant.value)
            if not idea:continue
            native=direct(idea.children(),'modifier')
            for modifier in native.children() if native else []:
                if modifier.key=='custom_modifier_tooltip':continue
                matching=[n for n in walk([node]) if n.key=='add_to_variable' and field(n.children(),P+'preview_'+modifier.key)==modifier.value]
                require(matching,'Missing prospective signed '+modifier.key+' for '+grant.value)
    checks.append('Agreement previews expose both names and every actual signed spirit modifier without eligibility guards')
    for preview in [n for n in walk(ast['scripted_effects']) if n.key=='effect_tooltip']:
        aid=[n for scope in preview.children() for n in scope.children() if n.key=='add_ideas' and str(n.value).startswith(P+'aid_')]
        if not aid:continue
        require(len(aid)==2 and {str(n.value).rsplit('_',1)[1] for n in aid}=={'usa','partner'},'Material assistance preview omits a prospective budget spirit')
        for scope in preview.children():
            for grant in [n for n in scope.children() if n.key=='add_ideas' and str(n.value).startswith(P+'aid_')]:
                tier,role=str(grant.value).rsplit('_',2)[1:]
                rate=Decimal('.005') if tier=='legacy' else Decimal('.00005') if tier=='3' else Decimal('.00002')
                if role=='usa':rate=-rate
                percentage=P+'preview_weekly_gdp' if role=='usa' else P+'preview_weekly_usa_gdp'
                rows=[field(n.children(),percentage) for n in walk(scope.children()) if n.key=='add_to_variable' and field(n.children(),percentage) is not None]
                require(any(Decimal(value)==rate for value in rows),'Material assistance preview lacks its signed GDP percentage for '+str(grant.value))
                maths=list(walk(scope.children()))
                basis='gdp_total' if role=='usa' else 'USA.gdp_total'
                require(any(n.key=='set_temp_variable' and field(n.children(),P+'preview_weekly_amount')==basis for n in maths),'Material preview does not use the donor GDP: '+str(grant.value))
                require(any(n.key=='multiply_temp_variable' and field(n.children(),P+'preview_weekly_amount') is not None and Decimal(field(n.children(),P+'preview_weekly_amount'))==rate for n in maths),'Material preview GDP multiplication has the wrong sign or percentage: '+str(grant.value))
                require(any(n.key=='divide_temp_variable' and field(n.children(),P+'preview_weekly_amount')=='100' for n in maths),'Material preview does not convert percent to native monetary units: '+str(grant.value))
                require(any(n.key=='add_to_variable' and field(n.children(),P+'preview_weekly')==P+'preview_weekly_amount' for n in maths),'Material preview omits the calculated native monetary amount: '+str(grant.value))
                if role=='partner':
                    require(any(n.key=='add_equipment_to_stockpile' and field(n.children(),'type')=='infantry_weapons_1' and field(n.children(),'amount') is not None for n in walk(scope.children())),'Recipient material preview omits real equipment amount for '+str(grant.value))
    checks.append('Material assistance previews expose both budget spirits, signed weekly transfers and recipient equipment')
    for key in ('tur_networks','syr_voice'):
        focus_effect=fx[P+'execute_'+key]
        for node in expanded_effect(focus_effect):
            require(not (node.key=='add_equipment_to_stockpile' and field(node.children(),'type')=='infantry_weapons_1' and field(node.children(),'amount')=='1000'),'Political-only network promises an uncommitted weapon delivery: '+key)
            require(not (node.key=='add_to_variable' and field(node.children(),P+'preview_material')=='1000'),'Political-only network promises an uncommitted material cache: '+key)
    checks.append('Political-only Turkish and Syrian networks do not promise uncommitted weapon shipments')
    baseline=fx.get(P+'regional_research')
    require(baseline is not None,'Missing undated regional research baseline')
    baseline_nodes=list(walk([baseline])) if baseline else []
    technologies={child.key for node in baseline_nodes if node.key=='set_technology' for child in node.children() if child.key!='popup'}
    require(technologies==REGIONAL_BASELINE,'Regional baseline differs from the bounded1940-45 plus DLC-AA contract')
    require(not any(n.key in ('date','original_tag','inherit_technology','load_oob','add_equipment_to_stockpile') for n in baseline_nodes),'Regional research baseline depends on date/tag or grants unrelated technology/assets')
    init=fx.get(P+'initialize_new_actor')
    require(init and any(n.key==P+'regional_research' for n in walk([init])),'New actor does not apply its own undated research baseline')
    require(init and not any(n.key=='mdcw_apply_1970_infantry_research' for n in walk([init])),'New actor still routes research through the dated known-tag dispatcher')
    checks.append('American material has a real producer and new regional actors receive only the undated bounded early research baseline')
    # Own newborn tags cannot copy a player treasury, equipment, technologies
    # or the MD broad fresh-start asset grants.
    birth_fx=[n for key,n in fx.items() if key.startswith(P+'uprising_')]
    def cleanup_scopes(node,ancestors,owner):
        if node.key=='set_equipment_fraction':
            target=ancestors[-1].key if ancestors else None
            require(owner.startswith(P+'uprising_') and target in ('KUR','PUK','KPI','KPT','KPS') and node.value=='0','Equipment cleanup escapes a named newborn scope: '+owner)
            guards=[direct(a.children(),'limit') for a in ancestors if a.key=='if']
            guards=[x for x in guards if x is not None]
            if target in ('KUR','PUK'):
                require(any(x.key=='has_country_flag' and x.value==P+'new_'+target.lower() for guard in guards for x in walk([guard])),'Existing Iraqi RP actor is not excluded from equipment cleanup: '+str(target))
            else:
                require(any(x.key=='NOT' and any(c.key=='country_exists' and c.value==target for c in x.children()) for guard in guards for x in walk([guard])),'Existing regional RP actor is not excluded from equipment cleanup: '+str(target))
            require(any(x.key=='create_unit' and field(x.children(),'owner')==target and x.start<node.start for a in ancestors for x in walk(a.children())),'Equipment cleanup does not follow its own new column creation: '+str(target))
        for child in node.children():cleanup_scopes(child,[*ancestors,node],owner)
    for key,node in fx.items():cleanup_scopes(node,[],key)
    for node in birth_fx:
        for n in expanded_effect(node):require(n.key not in ('create_dynamic_country','civil_war_replication_effect','ingame_startup_nations_effect','inherit_technology'),'Unsafe broad newborn/copy helper in '+node.key)
        top=next((n for n in node.children() if n.key=='if'),None)
        limit=direct(top.children(),'limit') if top else None
        guards=list(walk([limit])) if limit else []
        host=node.key.removeprefix(P+'uprising_')
        require(any(n.key==P+'mobilisation_'+host and n.value=='yes' for n in guards),'Uprising execution omits current mobilisation guard '+node.key)
        require(any(n.key=='check_variable' and field(n.children(),P+'warning_days')=='44' for n in guards),'Uprising execution omits completed warning '+node.key)
        require(any(n.key=='check_variable' and field(n.children(),P+'qualifying_days')=='29' for n in guards),'Uprising execution omits completed organisation '+node.key)
        if host!='irq':
            flat=list(expanded_effect(node))
            for variable in ('treasury','debt','int_investments','nation_to_copy_from'):
                require(any(n.key=='set_variable' and field(n.children(),variable)=='0' for n in flat),'Newborn does not explicitly zero '+variable+' in '+node.key)
            require(any(n.key=='set_variable' and field(n.children(),'last_quarter_gdp_total') is not None for n in flat),'Newborn lacks receipt preventing native fresh-start assets '+node.key)
            require(not any(n.key in ('add_manpower','add_to_stockpile','load_oob','oob') for n in flat),'Newborn receives unapproved free assets '+node.key)
    gui_objects={field(n.children(),'name') for n in walk(gui) if n.key in ('containerWindowType','iconType','instantTextBoxType','buttonType','progressbarType')}
    for node in walk(ast['scripted_guis']):
        if node.key=='window_name':require(node.value in gui_objects,'Scripted GUI window does not resolve: '+str(node.value))
    sprites={str(field(n.children(),'name')).strip('"'):n for n in walk(gfx) if n.key.lower() in ('spritetype','progressbartype')}
    for fid,focus in new.items():
        icon=str(field(focus.children(),'icon','')).strip('"')
        require(icon in sprites,'New focus icon does not resolve in owned GFX: '+fid+' / '+icon)
        require(icon+'_shine' in sprites,'New focus native shine alias does not resolve in owned GFX: '+fid+' / '+icon+'_shine')
    for sprite,node in sprites.items():
        for child in node.children():
            if child.key.lower() in ('texturefile','texturefile1','texturefile2'):
                texture=str(child.value).strip('"')
                require((ROOT/texture).exists(),'Missing registered texture '+texture)
    tag_nodes=parse('common/country_tags/'+STEM+'.txt')
    require({n.key for n in tag_nodes}=={'KPI','KPT','KPS'},'Unexpected or missing distinct regional country identities')
    for n in tag_nodes:
        read('common/'+str(n.value).strip('"'))
        histories=list((ROOT/'history/countries').glob(n.key+' - *.txt'))
        require(len(histories)==1,'Missing or ambiguous own-country history for '+n.key)
        if len(histories)==1:
            history=parse(str(histories[0].relative_to(ROOT)))
            require(any(x.key==P+'regional_research' for x in history),'New country history omits its own minimum research: '+n.key)
            require(not any(x.key=='mdcw_apply_1970_infantry_research' for x in history),'New country history still uses the dated dispatcher: '+n.key)
            for variable in ('treasury','debt','int_investments'):
                require(any(x.key=='set_variable' and field(x.children(),variable)=='0' for x in history),'New country history does not start '+variable+' at zero: '+n.key)
            for x in history:
                if x.key in ('set_oob','set_naval_oob','set_air_oob'):
                    require((ROOT/'history/units'/str(x.value).strip('"')).with_suffix('.txt').exists(),'Empty OOB provider missing: '+str(x.value))
    checks.append('Newborn broad-copy hazards, distinct country histories, native UI windows and owned texture references checked')
    report=dict(project='IMPERIA COLD WAR',scope='Targeted installed source/reference checks',status='PASS' if not any(f['severity']=='error' for f in findings) else 'FAIL',checks=checks,findings=findings,hashes=hashes,
        evidence='Source and parser evidence only. Separate emitted-AST models and native/MP tests are not implied.',counts=dict(new_focuses=len(new),all_usa_focuses=len(all_focuses),new_effects=len(fx),new_triggers=len(tr),ideas=len(ideas),decisions=len(decisions)))
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    report=validate();print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['status']=='PASS' else 1)
