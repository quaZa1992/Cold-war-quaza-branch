# IMPERIA COLD WAR — Independent emitted-source checks for France 1970.
"""Source contract checks, not an HOI4 engine or save/load test."""
from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk

D = json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
I = json.loads((HERE/'icons.json').read_text(encoding='utf-8'))
issues, checks = [], 0
def check(ok, msg):
    global checks
    checks += 1
    if not ok:
        issues.append(msg)
def ast(rel):
    return parse((ROOT/rel).read_text(encoding='utf-8-sig'))
def rows_at(row, key):
    return [(k,v) for k,o,v in walk(row) if k == key]
def as_num(v):
    return Decimal(str(v))

paths = [p for folder in ['common/national_focus','common/scripted_effects','common/scripted_triggers','common/dynamic_modifiers','common/ideas','common/on_actions','common/decisions','common/decisions/categories','events','interface','localisation/english'] for p in (ROOT/folder).glob('COLDWAR_FRA_1970*')]
for p in paths:
    raw=p.read_bytes(); txt=raw.decode('utf-8-sig')
    check(raw.startswith(b'\xef\xbb\xbf') == (p.suffix == '.yml'), 'BOM mismatch: '+str(p))
    check('IMPERIA COLD WAR' in txt.splitlines()[0:3].__str__(), 'Project marker missing: '+str(p))
    if p.suffix != '.yml':
        try:
            parsed=parse(txt)
            check(not any(o in ('>=','<=','!=') for k,o,v in walk(parsed)), 'Unsupported script operator: '+str(p))
            check(not any(re.search(r'\d\.\d{6,}',v) for k,o,v in walk(parsed) if isinstance(v,str) and not v.startswith('"')), 'Overprecision literal: '+str(p))
        except ValueError as e:
            check(False, 'Parse failure '+str(p)+': '+str(e))
check(hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest() == 'f90e6193464ffce880d3a6ba049568f779ccb0ab8111acb252c34118cdbdc780', 'Approved data mutated')
tree=first(ast('common/national_focus/COLDWAR_FRA_1970_focus.txt'),'focus_tree')
fmap={first(n,'id'):n for n in values(tree,'focus')}
effects={k:v for k,o,v in ast('common/scripted_effects/COLDWAR_FRA_1970_effects.txt')}
triggers={k:v for k,o,v in ast('common/scripted_triggers/COLDWAR_FRA_1970_triggers.txt')}
md_party_triggers={k:v for k,o,v in ast('common/scripted_triggers/01_political_triggers.txt')}
md_party_loc=(ROOT/'localisation/english/MD_tooltips_l_english.yml').read_text(encoding='utf-8-sig')
dyn={k:v for k,o,v in ast('common/dynamic_modifiers/COLDWAR_FRA_1970_dynamic_modifiers.txt')}
ideas={k:v for k,o,v in first(first(ast('common/ideas/COLDWAR_FRA_1970_ideas.txt'),'ideas'),'country')}
loc={}
for p in (ROOT/'localisation/english').glob('COLDWAR_FRA_1970*.yml'):
    for k,v in re.findall(r'^ (\S+):0 (".*")$',p.read_text(encoding='utf-8-sig'),re.M):
        check(k not in loc,'Duplicate localisation: '+k)
        try:
            loc[k]=json.loads(v)
        except ValueError:
            check(False,'Invalid localisation escaping: '+k)
check(len(fmap)==234,'Incorrect focus count')
check(len(dyn)==13,'Incorrect programme count')
check(len(ideas)==5,'Incorrect starting/residual idea count')
check(set(fmap)=={n['id'] for n in D['nodes']},'Focus IDs differ')
resolved={}
def position(nid, seen=frozenset()):
    check(nid not in seen, 'Cyclic anchor: '+nid)
    n=fmap[nid]; xy=(int(first(n,'x')),int(first(n,'y')))
    anchor=first(n,'relative_position_id')
    if anchor:
        check(anchor in fmap,'Missing anchor: '+str(anchor))
        ax,ay=position(anchor,seen|{nid}); xy=(xy[0]+ax,xy[1]+ay)
    return xy

contributions={}
for group in D['groups']:
    gid=group['id']; programme='COLDWAR_FRA_'+gid+'_programme'
    check(first(first(dyn[programme],'enable'),'COLDWAR_FRA_'+gid+'_government')=='yes','Missing dynamic enable gate: '+gid)
    for n in [n for n in D['nodes'] if n['group']==gid]:
        nid=n['id']; f=fmap[nid]; apply=first(effects['COLDWAR_FRA_apply_'+n['key']],'if')
        guard=first(apply,'limit')
        check(first(guard,'COLDWAR_FRA_'+gid+'_government')=='yes','Missing completion government guard: '+nid)
        check(nid+'_earned' in [v for k,v in rows_at(guard,'has_country_flag')],'Missing once-only guard: '+nid)
        check(first(apply,'set_country_flag')==nid+'_earned','Missing earned receipt: '+nid)
        check(float(first(apply,'add_political_power'))==n['pp'],'Wrong PP charge: '+nid)
        check(position(nid)==tuple(n['absolute']),'Position differs: '+nid)
        check(first(f,'cancel_if_invalid')=='yes' and first(f,'continue_if_invalid')=='no','Invalid focus continuation: '+nid)
        check([values(p,'focus') for p in values(f,'prerequisite')]==n['prerequisites'],'AND/OR predecessor mismatch: '+nid)
        check(set(values(first(f,'mutually_exclusive',[]),'focus'))=={'COLDWAR_FRA_'+p for p in n['exclusive']},'Exclusion mismatch: '+nid)
        check(first(f,'icon')==I['focus_icons'][nid],'Icon map not installed: '+nid)
        check(nid in loc and nid+'_desc' in loc,'Missing focus localisation: '+nid)
        check(float(first(f,'cost'))*7==n['days'],'Focus duration mismatch: '+nid)
        expected_bonus=[]
        for e in n['one_time_effects']:
            if e['kind']=='tech_bonus':
                variants=e.get('target_variants') or [{'technologies':[]}]
                for v in variants:
                    expected_bonus.append((e['name'],as_num(e['bonus']),int(e['uses']),tuple(v['technologies']),e.get('category')))
            else:
                check(first(apply,e['kind'])==str(e['amount']),'XP grant mismatch: '+nid)
        emitted_bonus=[(first(b,'name'),as_num(first(b,'bonus')),int(first(b,'uses')),tuple(values(b,'technology')),first(b,'category')) for k,b in rows_at(apply,'add_tech_bonus')]
        check(emitted_bonus==expected_bonus,'Research reward differs: '+nid)
        for kind,amount in n['once']:
            check(as_num(first(apply,'add_'+kind))==as_num(amount),'One-time effect mismatch: '+nid)
        preview=first(first(f,'completion_reward'),'effect_tooltip')
        deltas={}
        for a in values(preview,'add_to_variable'):
            [(var,v)] = [(k,v) for k,o,v in a if k!='tooltip']
            deltas[var.removeprefix('COLDWAR_FRA_'+gid+'_')]=as_num(v)
        check(deltas=={k:as_num(v) for k,v in n['mods'].items() if v!=0},'Visible modifier deltas differ: '+nid)
        check(all(v!=0 for v in deltas.values()),'Meaningless zero modifier displayed: '+nid)
        contributions[n['key']]=deltas
        if n.get('offer_id'):
            check(first(preview,'unlock_decision_tooltip')==n['offer_id'],'Native offer decision unlock missing: '+nid)
        check(not any(k=='custom_effect_tooltip' and isinstance(v,str) and v.startswith('COLDWAR_FRA_') for k,o,v in walk(preview)),'Custom explanatory prose in focus effects: '+nid)
        check(first(f,'allow_branch') is None,'Party content hidden by a branch visibility gate: '+nid)
        if gid!='institutions':
            available=first(f,'available')
            check(any(k=='COLDWAR_FRA_'+gid+'_government' and v=='yes' for k,o,v in walk(available)),'Visible party focus missing execution gate: '+nid)
            native=[k for k,o,v in available if k.endswith('_are_in_power') and v=='yes']
            check(len(native)==1,'Missing direct native MD party requirement: '+nid)
            if native:
                check(native[0] in md_party_triggers,'Undefined MD party trigger: '+native[0])
                body=first(md_party_triggers[native[0]],'custom_trigger_tooltip')
                required_slot=first(first(body,'check_variable'),'ruling_party')
                check(required_slot==str(n['party_gate']['ruling_party_equals']),'Native MD requirement checks wrong party: '+nid)
                tooltip=first(body,'tooltip')
                match=re.search(r'^\s*'+re.escape(tooltip)+r':(?:\d+)?\s*"([^"]*)"',md_party_loc,re.M)
                check(match is not None,'Native party tooltip missing: '+native[0])
                if match:
                    party_label=re.search(r'\[([^\]]+_L)\]',match[1]).group(1)
                    check(loc['COLDWAR_FRA_'+gid+'_programme']==f'[{party_label}] Programme','Programme uses invented party name: '+gid)
                    check(loc['COLDWAR_FRA_shortcut_'+gid]==f'[{party_label}]','Shortcut uses invented party name: '+gid)
            check(not any(k=='custom_trigger_tooltip' and first(v,'tooltip','').endswith('_government_tt') for k,o,v in available),'Invented party tooltip retained: '+nid)

# Compare real refresh clauses and dynamic bindings, independently of preview rows.
refresh=first(effects['COLDWAR_FRA_refresh_programmes'],'if')
for group in D['groups']:
    gid=group['id']; prefix='COLDWAR_FRA_'+gid+'_'
    body=next(b for b in values(refresh,'if') if first(first(b,'limit',[]),prefix+'government')=='yes')
    actual={}
    for clause in values(body,'if'):
        receipt=first(first(clause,'limit',[]),'has_country_flag')
        if receipt:
            key=receipt.removeprefix('COLDWAR_FRA_').removesuffix('_earned')
            actual[key]={k.removeprefix(prefix):as_num(v) for a in values(clause,'add_to_variable') for k,o,v in a}
    expected={n['key']:{k:as_num(v) for k,v in n['mods'].items()} for n in D['nodes'] if n['group']==gid and n['mods']}
    check(actual==expected,'Runtime modifier contributions differ: '+gid)
    bindings={k:v for k,o,v in dyn[prefix+'programme'] if k not in ('icon','enable')}
    check(bindings=={m:prefix+m for m in {m for n in D['nodes'] if n['group']==gid for m in n['mods']}},'Missing/incorrect dynamic binding: '+gid)
    # Source-level programme ownership model for every approved compatible route.
    for route in group['variants']:
        sums=defaultdict(Decimal)
        for key in route['focuses']:
            for m,v in actual.get(key,{}).items(): sums[m]+=v
        want={k:as_num(v) for k,v in route['mods'].items() if v}
        got={k:v for k,v in sums.items() if v}
        check(set(got)==set(want) and all(abs(got[k]-want[k])<Decimal('0.000001') for k in got),'Compatible route sum differs: '+gid)
    check(not any(k in ('add_political_power','army_experience','navy_experience','air_experience','add_tech_bonus','swap_ideas','add_stability') for k,o,v in walk(body)),'Refresh replays a one-time grant: '+gid)

for s in D['spirits']+D['residual_spirits']:
    body=ideas[s['id']]
    check({k:as_num(v) for k,o,v in first(body,'modifier')}=={k:as_num(v) for k,v in s['mods'].items()},'Starting idea effect differs: '+s['id'])
    check(first(body,'picture')==I['spirit_idea_pictures'][s['id']].removeprefix('GFX_idea_'),'Wrong small spirit art: '+s['id'])

# Technology definitions and custom modifier providers must resolve in the actual checkout.
tech_sources='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/technologies').glob('*.txt'))
for n in D['nodes']:
    for e in n['one_time_effects']:
        for v in e.get('target_variants',[]):
            for tech in v['technologies']:
                check(bool(re.search(r'^\s*'+re.escape(tech)+r'\s*=\s*\{',tech_sources,re.M)), 'Undefined technology: '+tech)
            for project in v.get('required_projects',[]):
                apply=effects['COLDWAR_FRA_apply_'+n['key']]
                check('sp:'+project in [v for k,v in rows_at(first(first(apply,'if'),'limit'),'is_special_project_completed')],'Missing project completion guard: '+n['key'])
definitions='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/modifier_definitions').glob('*.txt'))
for m in {m for n in D['nodes'] for m in n['mods']}:
    if m.endswith('_modifier'):
        check(bool(re.search(r'^'+re.escape(m)+r'\s*=\s*\{',definitions,re.M)),'Custom modifier unregistered: '+m)

sprites={}
for p in (ROOT/'interface').glob('*.gfx'):
    if p.name not in ('MD_ideas.gfx','COLDWAR_FRA_1970_icons.gfx'):continue
    for b in values(first(parse(p.read_text(encoding='utf-8-sig')),'spriteTypes',[]),'spriteType'):
        name=first(b,'name','').strip('"'); sprites[name]=b
for nid,icon in I['focus_icons'].items():
    check(icon in sprites and icon+'_shine' in sprites,'Missing focus sprite/shine: '+nid)
    if icon in sprites:
        texture=first(sprites[icon],'texturefile','').strip('"')
        check((ROOT/texture).is_file(),'Missing Cold War focus art: '+texture)
for icon in set(I['programme_idea_pictures'].values())|set(I['spirit_idea_pictures'].values()):
    check(icon in sprites,'Missing idea alias: '+icon)
    if icon in sprites:
        tex=first(sprites[icon],'texturefile','').strip('"')
        check((ROOT/tex).is_file() or (MD/tex).is_file(),'Missing idea art: '+tex)
for key,text in loc.items():
    check(not any(s in text for s in ('â€','Ã','Â·')), 'Mojibake in localisation: '+key)

# Resolve transitive custom effect/trigger and player-facing name references, including offers.
definitions_all={}
for folder in ('common/scripted_effects','common/scripted_triggers'):
    for p in (ROOT/folder).glob('COLDWAR_FRA_1970*.txt'):
        definitions_all.update({k:v for k,o,v in parse(p.read_text(encoding='utf-8'))})
for p in paths:
    if p.suffix=='.yml':continue
    source=parse(p.read_text(encoding='utf-8'))
    for k,o,v in walk(source):
        if k.startswith('COLDWAR_FRA_') and v=='yes':
            check(k in definitions_all,'Unresolved custom effect/trigger '+k+' in '+str(p))
        if k=='add_tech_bonus':
            check(first(v,'name') in loc,'Research reward name unlocalized: '+str(first(v,'name')))
        if k in ('title','desc','name') and isinstance(v,str) and v.startswith('COLDWAR_FRA_'):
            check(v in loc,'Unlocalized title/description/name: '+v)
        if k=='custom_effect_tooltip' and isinstance(v,str) and v.startswith('COLDWAR_FRA_'):
            check(v in loc,'Unlocalized effect tooltip: '+v)
        if k=='tooltip' and isinstance(v,str) and v.startswith('COLDWAR_FRA_'):
            check(v in loc,'Unlocalized condition/variable tooltip: '+v)
for programme in dyn:
    check(programme in loc and programme+'_desc' in loc,'Unlocalized programme idea: '+programme)
for idea in ideas:
    check(idea in loc and idea+'_desc' in loc,'Unlocalized starting idea: '+idea)

offers=ast('common/scripted_effects/COLDWAR_FRA_1970_offers.txt')
offer_by={k:v for k,o,v in offers}
offer_ideas={k:v for k,o,v in first(first(ast('common/ideas/COLDWAR_FRA_1970_treaties.txt'),'ideas'),'country')}
events=values(ast('events/COLDWAR_FRA_1970_offers.txt'),'country_event')
check(len(events)==24,'Offer event coverage differs')
for offer in D['offers']:
    oid=offer['id']; effect=first(offer_by[oid+'_accept'],'if')
    check(first(effect,'limit') is not None,'Unguarded agreement acceptance: '+oid)
    preview=first(offer_by[oid+'_preview'],'effect_tooltip')
    check(preview is not None,'Missing native agreement preview: '+oid)
    check(not rows_at(offer_by[oid+'_preview'],'custom_effect_tooltip'),'Prose replaced native agreement effects: '+oid)
    recipients=effect
    france=first(effect,'FRA')
    check(france is not None,'Missing French agreement scope: '+oid)
    for side,body in [('partner',recipients),('france',france)]:
        wanted=offer[side]['completion_effects']
        pp=sum(e['amount'] for e in wanted if e['kind']=='political_power')
        check(sum(as_num(v) for v in values(body,'add_political_power'))==pp,'Agreement PP charge mismatch: '+oid+' '+side)
        treasury=sum(e['amount'] for e in wanted if e['kind']=='treasury')
        emitted_treasury=sum(as_num(first(b,'treasury_change')) for b in values(body,'set_temp_variable') if first(b,'treasury_change') is not None)
        check(emitted_treasury==as_num(treasury),'Agreement treasury charge mismatch: '+oid+' '+side)
        bonuses=values(body,'add_tech_bonus')
        expected=[e for e in wanted if e['kind']=='tech_bonus']
        check(len(bonuses)==len(expected),'Agreement research count mismatch: '+oid+' '+side)
        for b,e in zip(bonuses,expected):
            check(first(b,'name')==e['name'] and as_num(first(b,'bonus'))==as_num(e['bonus']) and int(first(b,'uses'))==e['uses'] and first(b,'category')==e['category'],'Agreement research mismatch: '+oid+' '+side)
    expected_france_preview=[r for r in preview if r[0]!='FROM']
    partner_preview=first(preview,'FROM')
    for label,rendered,executed in [('France',expected_france_preview,france),('recipient',partner_preview,recipients)]:
        native={'set_temp_variable','modify_treasury_effect','add_political_power','add_tech_bonus','add_ideas'}
        actual_native=[r for r in executed if r[0] in native]
        check(rendered==actual_native,'Native prospective rewards differ from execution: '+oid+' '+label)
    event=next(e for e in events if first(e,'title')==oid+'_title')
    accept_option=values(event,'option')[0]
    event_preview=first(accept_option,'effect_tooltip')
    check(first(first(accept_option,'hidden_effect'),oid+'_accept')=='yes','Event hidden transaction missing: '+oid)
    check([r for r in event_preview if r[0]!='FRA']==partner_preview and first(event_preview,'FRA')==expected_france_preview,'Event native rewards differ from execution: '+oid)
    check(not any(k=='custom_effect_tooltip' for k,o,v in walk(accept_option)),'Custom prose in acceptance effects: '+oid)
    if offer['duration_days']:
        idea=offer_ideas[oid+'_treaty']
        check({k:as_num(v) for k,o,v in first(idea,'modifier')}=={k:as_num(v) for k,v in offer['france']['mods'].items()},'Agreement modifiers differ: '+oid)
        check(offer['france']['mods']==offer['partner']['mods'],'Asymmetric treaty requires separate ideas: '+oid)
        check(first(effect,'add_ideas')==oid+'_treaty' and first(france,'add_ideas')==oid+'_treaty','Permanent paired agreement ideas missing: '+oid)
        check(not rows_at(effect,'add_timed_idea'),'Permanent agreement has a timed expiry: '+oid)
        check(first(idea,'cancel') is not None,'Missing orphaned spirit safeguard: '+oid)
    else:
        check(first(france,'set_country_flag')==oid+'_consumed','Missing French finite-research receipt: '+oid)
        check(first(effect,'set_country_flag')=='COLDWAR_FRA_research_pair_consumed','Missing bilateral finite-research receipt: '+oid)

policy=json.loads((HERE/'offer_policy.json').read_text(encoding='utf-8'))
check(policy['compact_duration_days'] is None,'Permanent lifecycle override missing')
maint=offer_by['COLDWAR_FRA_offer_maintenance']
check(not any(k in ('every_country','every_other_country','for_each_scope_loop') for k,o,v in walk(maint)),'Maintenance scans countries instead of the saved pair')
check(not any(k in ('every_country','every_other_country') for k,o,v in walk(offer_by['COLDWAR_FRA_end_compact'])),'Withdrawal scans countries')
rel=first(ast('common/scripted_triggers/COLDWAR_FRA_1970_offer_triggers.txt'),'COLDWAR_FRA_offer_partner_relations_valid')
array_rows=[dict((k,v) for k,o,v in b) for k,b in rows_at(rel,'is_in_array')]
check({(b['array'],b['value']) for b in array_rows}=={('imp_'+kind+'_sanc_'+direction,'FRA') for kind in ('dip','fin','eco','mil') for direction in ('on_us','by_us')},'Bilateral sanctions coverage differs')

pairs={tuple(sorted((n['key'],peer))) for n in D['nodes'] for peer in n['exclusive']}
by={n['key']:n for n in D['nodes']}
check(len(pairs)==79,'Exclusion pair count changed')
for a,b in pairs:
    check(a in by[b]['exclusive'] and b in by[a]['exclusive'],'Nonreciprocal exclusion: '+a)
report={'project':'IMPERIA COLD WAR','kind':'Emitted-source validation; no engine claims','checks':checks,'focuses':len(fmap),'programmes':len(dyn),'exclusive_pairs':len(pairs),'compatible_routes':sum(len(g['variants']) for g in D['groups']),'issues':issues}
(HERE/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(bool(issues))
