# IMPERIA COLD WAR — Cold War: independent emitted South Korean runtime checks.
"""Validate loaded/staged scripts; source tests are not an HOI4 engine run."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse,hashlib,json,re,sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
STAGE=Path(r'E:\HOI4_Mod_Tools\mdcoldwar\runtime\quaza_eastasia_20261027\kor_stage')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
from COLDWAR_KOR_alliance_revision import load_design
from COLDWAR_KOR_reward_revision import OVERLAY
from COLDWAR_KOR_reward_revision import BUILDING_METADATA
P='COLDWAR_KOR_'

def localization_map(text):
    result={}
    for line in text.splitlines():
        match=re.match(r'\s+([^\s:#]+):\d+\s+"(.*)"\s*$',line)
        if match:result[match[1]]=match[2]
    return result

def normalized_localization(key,value):
    # These four pre-install display normalizations are documented semantic
    # parity: remove dash glyphs from newly emitted player-facing text.
    if key=='COLDWAR_KOR_buma_1979.t':
        return value.replace('\u2013','-')
    if key in ('COLDWAR_KOR_start_energy_intermediate','COLDWAR_KOR_start_rural_intermediate',
               'COLDWAR_KOR_usfk_exercise_launch_terms_tt'):
        return re.sub(r'\s*:\s*',' : ',value.replace('\u2014',':')).strip()
    return value

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');args=ap.parse_args()
    base=ROOT if args.installed else STAGE
    d=load_design()
    pre_reward=load_design(apply_rewards=False)
    pre_reward_by_key={node['key']:node for node in pre_reward['nodes']}
    reward_revision=json.loads(OVERLAY.read_text(encoding='utf-8'))
    manifest=json.loads((DOC/'COLDWAR_KOR_runtime_manifest.json').read_text(encoding='utf-8'))
    errors=[];notes=[]
    def ck(ok,msg):
        if not ok:errors.append(msg)
    parsed={};blobs={}
    for rel,digest in manifest['files'].items():
        path=base/rel;ck(path.exists(),'missing output '+rel)
        if not path.exists():continue
        blob=path.read_bytes();blobs[rel]=blob
        actual_hash=hashlib.sha256(blob).hexdigest()
        if args.installed and rel in manifest.get('shared',[]):
            if actual_hash!=digest:
                notes.append('Installed shared integration differs from staged bytes; KOR contributions checked semantically: '+rel)
        elif args.installed and rel.endswith('.yml'):
            staged=STAGE/rel
            ck(staged.exists(),'missing staged localization for installed semantic comparison '+rel)
            if staged.exists():
                staged_map=localization_map(staged.read_text(encoding='utf-8-sig'))
                installed_map=localization_map(blob.decode('utf-8-sig'))
                ck(set(installed_map)==set(staged_map),'installed localization key set differs from staged output '+rel)
                ck(all(normalized_localization(k,v)==normalized_localization(k,installed_map.get(k,'')) for k,v in staged_map.items()),
                    'installed localization differs beyond approved punctuation normalization '+rel)
                if actual_hash!=digest:
                    notes.append('Installed localization matched staged keys/values after approved dash normalization: '+rel)
        else:
            ck(actual_hash==digest,'changed after emission '+rel)
        if rel.endswith('.yml'):
            ck(blob.startswith(b'\xef\xbb\xbf'),'localisation BOM missing '+rel);continue
        ck(not blob.startswith(b'\xef\xbb\xbf'),'script BOM '+rel)
        try:parsed[rel]=parse(blob.decode('utf-8'))
        except Exception as e:errors.append('parse '+rel+': '+str(e))
        ck(not re.search(rb'(?m)^\s*_(bare|list)\s*=',blob),'parser sentinel leaked '+rel)
        if '/COLDWAR_KOR_' in '/'+rel:
            ck(not re.search(rb'\b\d+\.\d{6,}\b',blob),'fixed-point literal precision '+rel)
        elif re.search(rb'\b\d+\.\d{6,}\b',blob):
            notes.append('Existing native long literals outside Korean additions preserved: '+rel)
    treepath='common/national_focus/COLDWAR_KOR_1970_focus.txt'
    tree=first(parsed.get(treepath,[]),'focus_tree',[])
    foci=values(tree,'focus');by={first(n,'id'):n for n in foci};expected={n['id']:n for n in d['nodes']}
    ck(len(by)==len(foci)==len(d['nodes'])<=300,'focus definition count/uniqueness/cap')
    ck(set(by)==set(expected),'approved focus IDs changed')
    emitted_order={first(n,'id'):i for i,n in enumerate(foci)}
    for id,focus in by.items():
        anchor=first(focus,'relative_position_id')
        if anchor:
            ck(anchor in emitted_order,'missing emitted relative anchor '+anchor+' for '+id)
            if anchor in emitted_order:
                ck(emitted_order[anchor]<emitted_order[id],'relative anchor must be serialized before child '+id+' -> '+anchor)
    ck(len(values(tree,'shortcut'))==8,'shortcut capacity/count')
    ck(first(first(tree,'initial_show_position',[]),'focus')==d['layout']['initial_focus'],'initial camera')
    E={};T={};DM={};IDEA={};sprites={};events={};paths={};decisions={};categories=set();used_categories=set()
    for rel,rows in parsed.items():
        if '/COLDWAR_KOR_' not in '/'+rel:continue
        target=E if '/scripted_effects/' in '/'+rel else T if '/scripted_triggers/' in '/'+rel else DM if '/dynamic_modifiers/' in '/'+rel else None
        if target is not None:
            for k,op,v in rows:
                ck(k not in target,'duplicate definition '+k)
                ck(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',k) is not None,'invalid top-level identifier '+k)
                target[k]=v;paths[k]=rel
        if '/ideas/' in '/'+rel:
            for k,op,v in first(first(rows,'ideas',[]),'country',[]):
                ck(k not in IDEA,'duplicate idea '+k);IDEA[k]=v;paths[k]=rel
        if rel.startswith('common/decisions/') and '/categories/' not in rel:
            for category,o,body in rows:
                used_categories.add(category)
                for key,o,decision in body:
                    if not isinstance(decision,list):continue
                    ck(key not in decisions,'duplicate decision '+key);decisions[key]=decision
        if rel.startswith('common/decisions/categories/'):
            categories.update(k for k,o,v in rows)
        if rel.endswith('.gfx'):
            for b in values(first(rows,'spriteTypes',[]),'spriteType'):
                name=first(b,'name','').strip('"');sprites[name]=first(b,'texturefile','').strip('"')
        if rel.startswith('events/'):
            declared=set(values(rows,'add_namespace'))
            for b in values(rows,'country_event')+values(rows,'news_event'):
                id=first(b,'id');ck(id not in events,'duplicate event '+str(id));events[id]=b;paths[id]=rel
                ck(bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*\.\d+',id or '')),'invalid event ID '+str(id))
                ck(id.split('.')[0] in declared,'undeclared event namespace '+str(id))
                ck(first(b,'is_triggered_only')=='yes' or bool(first(b,'trigger',[])),'unscoped automatic event '+str(id))
    for id,body in DM.items():
        ck(not any(k in ('modifier','allowed','removal_cost') for k,op,v in body),'idea shape in dynamic modifier '+id)
        ck(first(body,'enable') is not None,'dynamic modifier has no live enable '+id)
    ck(not (used_categories-categories),'unregistered decision categories: '+', '.join(sorted(used_categories-categories)))
    loc={}
    for rel,blob in blobs.items():
        if not rel.endswith('.yml'):continue
        lines=blob.decode('utf-8-sig').splitlines();ck(lines[0]=='l_english:','wrong language '+rel)
        for line in lines:
            m=re.match(r'\s+([^\s:#]+):\d+\s+"(.*)"\s*$',line)
            if m:
                ck(m[1] not in loc,'duplicate localisation '+m[1]);loc[m[1]]=m[2]
    def treasury_gdp_multipliers(rows):
        result=[]
        for row,_,body in walk(rows):
            if row!='set_temp_variable' or not isinstance(body,list):continue
            change=first(body,'treasury_change')
            if not isinstance(change,list) or first(change,'value')!='gdp_total':continue
            multiplier=first(change,'multiply')
            if multiplier is not None:result.append(float(multiplier))
        return result
    cost_scale=reward_revision['domestic_gdp_cost_scale']
    converted_domestic_cost_focuses=0
    ck(d.get('contracts')==pre_reward.get('contracts'),
       'Domestic GDP cost conversion changed bilateral agreement or recipient terms')
    for node in d['nodes']:
        key=node['key'];effective=node.get('effects',{})
        legacy_cost=float(pre_reward_by_key[key].get('effects',{}).get('cost',0))
        expected_base=min(legacy_cost*cost_scale['basis_per_legacy_billion'],
                          cost_scale['maximum_base_fraction']) if legacy_cost>0 else 0.0
        expected_project=float(reward_revision.get('projects',{}).get(key,{}).get('gdp_cost_fraction',0))
        expected_total=expected_base+expected_project
        if legacy_cost>0:
            converted_domestic_cost_focuses+=1
            ck(effective.get('cost',0)==0,
               'Converted domestic focus retained a fixed Treasury charge: '+key)
            ck(abs(float(effective.get('legacy_fixed_cost_bn',0))-legacy_cost)<1e-9 and
               abs(float(effective.get('gdp_base_cost_fraction',0))-expected_base)<1e-9,
               'Converted domestic focus base fraction differs from its authorized scale: '+key)
        ck(abs(float(effective.get('gdp_project_cost_fraction',0))-expected_project)<1e-9,
           'Project funding increment differs from its authorized overlay: '+key)
        if not expected_total:continue
        ck(abs(float(effective.get('gdp_share_cost_fraction',0))-expected_total)<1e-9,
           'Effective focus GDP share is not the sum of base and project costs: '+key)
        focus=by.get(P+key,[]);gate=T.get(P+'can_'+key,[])
        ck(any(name=='gdp_total' and op=='>' and value=='0'
               for row,_,body in gate if row=='check_variable'
               for name,op,value in body),
           'GDP-based domestic focus must require positive GDP before its guarded completion: '+key)
        available=first(focus,'available',[])
        visible=[row for row in available if row[0]!='hidden_trigger']
        ck(not any(name=='gdp_total' for row,_,body in walk(visible)
                   if row=='check_variable' for name,_,_ in body),
           'Internal GDP validity check leaked into visible focus requirements: '+key)
        reward=first(focus,'completion_reward',[]);preview=first(reward,'effect_tooltip',[])
        expected_tt=P+key+'_gdp_cost_tt'
        ck(any(row=='custom_effect_tooltip' and value==expected_tt
               for row,_,value in walk(preview)),
           'Locked focus preview omits its numeric total GDP cost explanation: '+key)
        expected_multiplier=-expected_total
        ck(len(treasury_gdp_multipliers(preview))==1 and
           abs(treasury_gdp_multipliers(preview)[0]-expected_multiplier)<1e-8,
           'Focus preview does not show the single total GDP-based native Treasury amount: '+key)
        helper=E.get(P+'complete_'+key,[])
        ck(len(treasury_gdp_multipliers(helper))==1 and
           abs(treasury_gdp_multipliers(helper)[0]-expected_multiplier)<1e-8 and
           sum(1 for row,_,_ in walk(helper) if row=='modify_treasury_effect')==1,
           'Guarded focus helper does not charge the same total GDP-based Treasury amount once: '+key)
    # Compare every finite-bonus payload in the native focus preview against
    # both the effective design and the executed one-time helper. Name-only
    # checks miss changed signs, categories, amounts, uses, and equipment types.
    def finite_bonus_payloads(rows):
        payloads={'equipment_bonuses':[],'tech_bonuses':[],'doctrine_bonuses':[]}
        def scalar(value):
            try:return float(value)
            except (TypeError,ValueError):return value
        for row,_,body in walk(rows):
            if not isinstance(body,list):continue
            if row=='add_equipment_bonus':
                typed=[]
                for equipment_type,_,modifiers in first(body,'bonus',[]):
                    if not isinstance(modifiers,list):continue
                    typed.append((equipment_type,tuple(sorted(
                        (key,scalar(value)) for key,_,value in modifiers))))
                payloads['equipment_bonuses'].append((first(body,'name'),tuple(sorted(typed))))
            elif row=='add_tech_bonus':
                payloads['tech_bonuses'].append((first(body,'name'),float(first(body,'bonus')),
                    int(first(body,'uses')),first(body,'category')))
            elif row=='add_doctrine_cost_reduction':
                payloads['doctrine_bonuses'].append((first(body,'name'),
                    float(first(body,'cost_reduction')),int(first(body,'uses')),
                    first(body,'category')))
        return {key:Counter(value) for key,value in payloads.items()}
    finite_bonus_counts=Counter()
    finite_bonus_focuses=0
    for node in d['nodes']:
        focus=by.get(node['id'],[])
        preview=first(first(focus,'completion_reward',[]),'effect_tooltip',[])
        execution=E.get(P+'complete_'+node['key'],[])
        expected={'equipment_bonuses':Counter(), 'tech_bonuses':Counter(),
                  'doctrine_bonuses':Counter()}
        structured=node.get('effects',{})
        for bonus in structured.get('equipment_bonuses',[]):
            expected['equipment_bonuses'][(bonus['name'],tuple(sorted(
                (kind,tuple(sorted([(key,float(value)) for key,value in modifiers.items()]+
                                   [('instant','yes')])))
                for kind,modifiers in bonus['types'].items())))]+=1
        for bonus in structured.get('tech_bonuses',[]):
            expected['tech_bonuses'][(bonus['name'],float(bonus['bonus']),
                int(bonus['uses']),bonus['category'])]+=1
        for bonus in structured.get('doctrine_bonuses',[]):
            expected['doctrine_bonuses'][(bonus['name'],float(bonus['cost_reduction']),
                int(bonus['uses']),bonus['category'])]+=1
        shown=finite_bonus_payloads(preview)
        granted=finite_bonus_payloads(execution)
        for field in expected:
            ck(shown[field]==expected[field],
               'Native focus preview finite-bonus payload differs from effective reward data: '+node['key']+' / '+field)
            ck(granted[field]==expected[field],
               'Native completion helper finite-bonus payload differs from effective reward data: '+node['key']+' / '+field)
            ck(shown[field]==granted[field],
               'Native focus preview finite-bonus payload differs from completion helper: '+node['key']+' / '+field)
            finite_bonus_counts[field]+=sum(expected[field].values())
        if any(expected[field] for field in expected):finite_bonus_focuses+=1
    for node in d['nodes']:
        buildings=node.get('effects',{}).get('buildings',[])
        if not buildings:continue
        totals={}
        group_totals={}
        for building in buildings:
            kind=building['type'];state=str(building['state'])
            spec=BUILDING_METADATA.get(kind,{})
            ck(spec.get('state_max') is not None,
               'Construction has no current MD state cap: '+node['key']+' / '+kind)
            key=(state,kind);totals[key]=totals.get(key,0)+int(building['level'])
            if spec.get('group_by'):
                group_key=(state,spec['group_by'])
                group_totals[group_key]=group_totals.get(group_key,0)+int(building['level'])
        gate=T.get(P+'can_'+node['key'],[])
        for (state,kind),amount in totals.items():
            state_rows=first(gate,state,[])
            threshold=BUILDING_METADATA[kind]['state_max']-amount+1
            ck(any(k==kind and op=='<' and value==str(threshold) for k,op,value in state_rows),
               'Aggregate native-cap headroom missing for '+node['key']+' / '+state+' / '+kind)
            ck(any(k=='is_owned_by' and value=='ROOT' for k,_,value in state_rows) and
               any(k=='is_controlled_by' and value=='ROOT' for k,_,value in state_rows),
               'State ownership/control guards missing for '+node['key']+' / '+state)
        for (state,group),amount in group_totals.items():
            members=[kind for kind,spec in BUILDING_METADATA.items() if spec.get('group_by')==group]
            cap=min(BUILDING_METADATA[kind]['state_max'] for kind in members)
            threshold=str(cap-amount+1);state_rows=first(gate,state,[])
            ck(all(any(k==kind and op=='<' and value==threshold for k,op,value in state_rows)
                   for kind in members),
               'Cross-type native cap group guard missing for '+node['key']+' / '+state+' / '+group)
    def resolve(id,trail=()):
        ck(id not in trail,'cyclic anchor '+id)
        n=by[id];xy=[int(first(n,'x','0')),int(first(n,'y','0'))];anchor=first(n,'relative_position_id')
        if anchor:
            ck(anchor in by,'missing anchor '+anchor)
            if anchor in by:a=resolve(anchor,trail+(id,));xy=[xy[0]+a[0],xy[1]+a[1]]
        return xy
    for id in sorted(decisions):
        ck(id in loc,'missing decision name '+id)
        ck(id+'_desc' in loc,'missing decision description '+id)
    for id in sorted(categories):
        ck(id in loc,'missing decision category name '+id)
        ck(id+'_desc' in loc,'missing decision category description '+id)
    # Native routing checks remain executable, but none may leak through a
    # scripted-trigger expansion into a focus/decision/option tooltip.
    def check_routing_hidden(rows,where,hidden=False):
        for k,o,v in rows:
            technical=k in ('tag','original_tag','IMP_is_1970_scenario') or (k=='has_country_flag' and v==P+'initialized')
            if technical:ck(hidden,'visible initialization/routing check in '+where)
            if isinstance(v,list):check_routing_hidden(v,where,hidden or k=='hidden_trigger')
    for id,body in T.items():check_routing_hidden(body,id)
    for id,body in DM.items():check_routing_hidden(first(body,'enable',[]),id)
    for id,n in expected.items():
        if id not in by:continue
        b=by[id]
        ck(resolve(id)==n['xy'],'geometry changed '+id)
        ck([values(x,'focus') for x in values(b,'prerequisite')]==n['prerequisites'],'prerequisite groups changed '+id)
        ck(set(values(first(b,'mutually_exclusive',[]),'focus'))==set(n['mutually_exclusive']),'exclusions changed '+id)
        ck(abs(float(first(b,'cost'))-n['days']/7)<1e-5,'duration changed '+id)
        ck(first(b,'icon') in sprites,'unregistered focus icon '+id)
        ck(id in loc and id+'_desc' in loc,'focus localisation missing '+id)
        reward=first(b,'completion_reward',[])
        ck(first(reward,'effect_tooltip') is not None and first(reward,'hidden_effect') is not None,'preview/execution not separated '+id)
        helper=P+'complete_'+n['key'];body=E.get(helper,[])
        ck(bool(body),'missing completion '+id)
        guard=first(first(body,'if',[]),'limit',[])
        ck(any(k=='NOT' and ('has_country_flag','=',id+'_paid') in v for k,o,v in guard),'missing once-only guard '+id)
        ck((P+'can_'+n['key'],'=','yes') in guard,'runtime gate missing '+id)
        for p in n['effects']['policies']:
            idea=IDEA.get(id+'_preview',[])
            preview={k:float(v) for k,o,v in first(idea,'modifier',[]) if not isinstance(v,list)}
            ck(preview==p['modifiers'],'visible policy coefficients changed '+id)
            dynamic=DM.get(id+'_programme',[])
            native_vars={k:v for k,o,v in dynamic if k not in ('icon','enable')}
            wanted={k:id+'_'+p['slot']+'_'+k for k in p['modifiers']}
            ck(native_vars==wanted,'modifier variables lack consumer '+id)
            assignments={k:v for k,o,v in walk(body) if o=='=' and not isinstance(v,list)}
            for k,v in p['modifiers'].items():ck(str(v)==assignments.get(wanted[k]) or float(assignments.get(wanted[k],'nan'))==v,'wrong policy assignment '+id+' '+k)
    # Resolve new transitive symbols, options and texture references.
    used_effects=set();used_triggers=set();reference_count=0
    for rel,rows in parsed.items():
        if '/COLDWAR_KOR_' not in '/'+rel:continue
        for k,op,v in walk(rows):
            if k.startswith(P) and v in ('yes','no') if isinstance(v,str) else False:
                reference_count+=1;ck(k in E or k in T,'undefined Korean helper '+k+' in '+rel)
            if k in ('country_event','news_event','state_event') and isinstance(v,list):
                id=first(v,'id')
                if id and id.startswith(P):ck(id in events,'undefined event '+id+' in '+rel)
            if k in ('add_dynamic_modifier','remove_dynamic_modifier','has_dynamic_modifier') and isinstance(v,list):
                id=first(v,'modifier')
                if id and id.startswith(P):ck(id in DM,'undefined dynamic modifier '+id)
            if k=='add_dynamic_modifier' and isinstance(v,str):ck(False,'scalar dynamic modifier addition '+rel)
            if k=='remove_dynamic_modifier' and isinstance(v,str):ck(False,'scalar dynamic modifier removal '+rel)
            if k=='add_timed_idea' and isinstance(v,list):
                id=first(v,'idea')
                if id and id.startswith(P):ck(id in IDEA,'undefined timed idea '+id)
            if k=='add_ideas' and isinstance(v,str) and v.startswith(P):ck(v in IDEA,'undefined idea '+v)
            if k in ('title','desc','name','tooltip','not_tooltip','custom_effect_tooltip') and isinstance(v,str) and v.startswith(P):
                ck(v in loc,'missing English text '+v+' in '+rel)
            if k=='set_politics' and isinstance(v,list):
                ruling=first(v,'ruling_party');ck(ruling is not None and not str(ruling).isdigit(),'invalid engine ideology '+rel)
            if k=='picture' and isinstance(v,str) and v.strip('"').startswith('gfx/'):
                ck((ROOT/v.strip('"')).exists(),'missing portrait '+v)
    for sprite,texture in sprites.items():ck((ROOT/texture).exists(),'missing texture '+texture)
    writes=set();reads=set()
    for rows in parsed.values():
        for k,o,v in walk(rows):
            if k=='set_country_flag':writes.add(v if isinstance(v,str) else first(v,'flag'))
            if k=='has_country_flag' and isinstance(v,str) and v.startswith(P):reads.add(v)
    ck(not (reads-writes),'Korean flags have no provider: '+', '.join(sorted(reads-writes)))
    # Policy traits and weekly accounting must connect to real native readers.
    money=blobs.get('common/scripted_effects/00_money_system.txt',b'').decode('utf-8')
    ck('COLDWAR_KOR_add_weekly_programme_cost = yes' in money and 'COLDWAR_KOR_contract_expenses = yes' in money,'weekly expenses unhooked')
    ck('COLDWAR_KOR_contract_income = yes' in money,'weekly contract income unhooked')
    history=blobs.get('history/countries/KOR - Korea.txt',b'').decode('utf-8')
    ck('load_focus_tree = COLDWAR_KOR_1970_focus' in history,'1970 history tree not installed')
    ck('name = "Park Chung Hee"' in history,'historical starting leader changed')
    ck('COLDWAR_KOR_1970_set_leader = yes' in blobs.get('common/scripted_effects/00_leader_setup_scripted_effects.txt',b'').decode('utf-8'),'native leader routing missing')
    ck('COLDWAR_KOR_sync_politics = yes' in blobs.get('common/scripted_effects/00_MD_politicsview_scripted_effects.txt',b'').decode('utf-8'),'exact-party hook missing')
    # Borrowing must not be blocked by new own-spending cash gates.
    for id,body in T.items():
        ck(not any(k in ('treasury','cash') for k,o,v in walk(body)),'new own-spending treasury gate '+id)
    # Pending referendum/court provider and normal continuation checks.
    ck(P+'calculate_charter_vote' in E,'ballot arithmetic not defined')
    ck(P+'on_native_election_resolved' in E,'election-result provider not defined')
    ck(any(k=='set_country_flag' and v==P+'election_resolution_pending' for b in E.values() for k,o,v in walk(b)),'no pending election setter')
    for n in d['nodes']:
        for a in n['effects']['actions']:
            if a['type']=='action':ck(P+'action_'+a['value'] in E,'missing action implementation '+a['value'])
            if a['type']=='offer':ck(P+'send_'+a['value'] in E,'missing bilateral sender '+a['value'])
    # Every building contract must be visible together in its focus preview,
    # and repeated in the guarded one-time executor before native construction.
    def state_effects(rows):
        found={}
        for key,_,body in rows:
            if key.isdigit() and isinstance(body,list):
                found.setdefault(key,[]).extend((kind,value) for kind,_,value in body)
            elif key in ('if','hidden_effect','effect_tooltip','custom_effect_tooltip') and isinstance(body,list):
                nested=[entry for entry in body if entry[0]!='limit'] if key=='if' else body
                child=state_effects(nested)
                for state,items in child.items():found.setdefault(state,[]).extend(items)
        return found
    def effect_amount(items,kind):
        return [int(value) if kind=='add_extra_state_shared_building_slots' else
                (first(value,'type'),int(first(value,'level','1'))) for effect,value in items if effect==kind]
    for node in d['nodes']:
        contracts=node['effects'].get('buildings',[])
        if not contracts:continue
        key=node['key'];focus=by.get(node['id'],[])
        reward=first(focus,'completion_reward',[])
        preview=state_effects(first(reward,'effect_tooltip',[]))
        executor=state_effects(E.get(P+'complete_'+key,[]))
        expected_by_state={}
        for building in contracts:
            state=str(building['state'])
            row=expected_by_state.setdefault(state,{'slots':0,'buildings':Counter()})
            level=int(building['level'])
            row['slots']+=level
            row['buildings'][building['type']]+=level

        def check_state_transaction(rows,state,contract,label):
            slots=sum(effect_amount(rows,'add_extra_state_shared_building_slots'))
            actual=Counter()
            for kind,level in effect_amount(rows,'add_building_construction'):
                actual[kind]+=level
            ck(slots==contract['slots'],
               f'{label}: state {state} must grant {contract["slots"]} shared slot(s), found {slots}')
            ck(actual==contract['buildings'],
               f'{label}: state {state} construction levels/types differ from aggregate contract')
            available=0;valid_order=True
            for effect,value in rows:
                if effect=='add_extra_state_shared_building_slots':available+=int(value)
                elif effect=='add_building_construction':
                    level=int(first(value,'level','1'))
                    if available<level:valid_order=False
                    available-=level
            ck(valid_order,
               f'{label}: state {state} must grant each building level shared capacity before construction')

        for state,contract in expected_by_state.items():
            check_state_transaction(preview.get(state,[]),state,contract,node['id']+' preview')
            check_state_transaction(executor.get(state,[]),state,contract,
                                    P+'complete_'+key+' guarded executor')
        guard=first(E.get(P+'complete_'+key,[]),'if',[])
        guard_rows=first(guard,'limit',[])
        ck(any(k==P+'can_'+key and v=='yes' for k,_,v in guard_rows),
           f'{P}complete_{key}: building transaction lost native availability guard')
        ck(any(k=='has_country_flag' and v==P+key+'_paid' for k,_,v in walk(guard_rows)),
           f'{P}complete_{key}: building transaction lost paid/replay guard')

    # Independent core execution model tests emitted guards/leaves/consumers.
    model=CoreModel(E,T)
    model.v['gdp_total']=100
    model.execute(E[P+'complete_chaebol_compact'])
    model.execute(E[P+'complete_export_targets'])
    model.execute(E[P+'calculate_weekly_cost'])
    ck(abs(model.v.get(P+'weekly_cost',0)-.004)<1e-8,'terminal policy expense does not replace prior level')
    paid_snapshot=(model.cash,deepcopy(model.buildings),deepcopy(model.slot_grants),deepcopy(model.pending_slots),model.grants)
    model.execute(E[P+'complete_export_targets']);ck(paid_snapshot==(model.cash,model.buildings,model.slot_grants,model.pending_slots,model.grants),'completion replay pays again')
    model.party=1;model.execute(E[P+'refresh_programmes']);model.execute(E[P+'calculate_weekly_cost'])
    ck(model.v.get(P+'weekly_cost',0)==0,'departed owner still billed')
    ck(not any('chaebol_compact_programme' in x or 'export_targets_programme' in x for x in model.dm),'departed owner modifier retained')
    model.party=0;model.execute(E[P+'refresh_programmes']);model.execute(E[P+'calculate_weekly_cost'])
    ck(abs(model.v.get(P+'weekly_cost',0)-.004)<1e-8,'returning owner does not resume cost')
    ck(paid_snapshot==(model.cash,model.buildings,model.slot_grants,model.pending_slots,model.grants),'returning owner repeats one-time payout')
    model.cash=0;model.execute(E[P+'complete_pohang_foundry'])
    ck(abs(model.cash+1.75)<1e-8,'Pohang total GDP-based setup charge is not 1.75B at GDP 100')
    shot=(model.cash,deepcopy(model.buildings),deepcopy(model.slot_grants),deepcopy(model.pending_slots));model.execute(E[P+'complete_pohang_foundry']);ck(shot==(model.cash,model.buildings,model.slot_grants,model.pending_slots),'paid construction/slot replay')
    report={'project':'IMPERIA COLD WAR','status':'PASS' if not errors else 'FAIL','target':'installed' if args.installed else 'staged','focuses':len(foci),'scripted_effects':len(E),'scripted_triggers':len(T),'dynamic_modifiers':len(DM),'ideas':len(IDEA),'events':len(events),'sprites':len(sprites),'english_keys':len(loc),'new_helper_references':reference_count,'domestic_gdp_cost_conversion':{'focuses_checked':len(d['nodes']),'converted_focuses':converted_domestic_cost_focuses,'rate_per_legacy_billion':cost_scale['basis_per_legacy_billion'],'base_fraction_cap':cost_scale['maximum_base_fraction'],'reference_gdp_total_bn':cost_scale['reference_gdp_total_bn'],'bilateral_terms_unchanged':d.get('contracts')==pre_reward.get('contracts')},'finite_bonus_preview_parity':{'focuses_checked':len(d['nodes']),'focuses_with_finite_bonuses':finite_bonus_focuses,**dict(finite_bonus_counts)},'errors':errors,'notes':notes,'scope':'Source AST/graph/reference/API shape and bounded emitted-effect model; not an HOI4 engine, tooltip, multiplayer or save test','approved_design_sha256':manifest['approved_design_sha256']}
    (DOC/'COLDWAR_KOR_runtime_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
    if errors:raise SystemExit(1)

class CoreModel:
    """Small fail-closed interpreter for core policy scenarios used above."""
    def __init__(self,e,t):
        self.e=e;self.t=t;self.v={};self.flags={P+'initialized'};self.dm=set();self.party=0;self.leader='Park Chung Hee';self.cash=100.;self.tmp={};self.buildings={};self.state_buildings={};self.slot_grants={};self.pending_slots={};self.grants=0
    def value(self,v):
        if isinstance(v,list):
            result=self.value(first(v,'value','0'))
            for operation,_,operand in v:
                if operation=='add':result+=self.value(operand)
                elif operation=='subtract':result-=self.value(operand)
                elif operation=='multiply':result*=self.value(operand)
                elif operation=='divide':result/=self.value(operand)
            return result
        try:return float(v)
        except (TypeError,ValueError):return self.tmp.get(v,self.v.get(v,0))
    def trigger(self,rows,state=None):
        result=[]
        for k,op,v in rows:
            if k in self.t:r=self.trigger(self.t[k],state)==(v=='yes')
            elif k in ('AND','hidden_trigger'):r=self.trigger(v,state)
            elif k=='custom_trigger_tooltip':r=self.trigger([x for x in v if x[0] not in ('tooltip','not_tooltip')],state)
            elif k=='OR':r=any(self.trigger([x],state) for x in v)
            elif k=='NOT':r=not self.trigger(v,state)
            elif k in ('original_tag','tag'):r=v=='KOR'
            elif k=='IMP_is_1970_scenario':r=v=='yes'
            elif k=='is_subject':r=v=='no'
            elif k=='has_country_flag':r=v in self.flags
            elif k=='has_country_leader':r=first(v,'name').strip('"')==self.leader
            elif k=='has_dynamic_modifier':r=first(v,'modifier') in self.dm
            elif k=='check_variable':
                a,cmp,b=v[0];lhs=self.party if a=='ruling_party' else self.value(a);rhs=self.value(b)
                r={'=':lhs==rhs,'>':lhs>rhs,'<':lhs<rhs,'>=':lhs>=rhs,'<=':lhs<=rhs}[cmp]
            elif k.isdigit():r=self.trigger(v,k)
            elif k in BUILDING_METADATA and state is not None:
                group=BUILDING_METADATA[k]['group_by']
                current=sum(amount for (building_state,building),amount in self.state_buildings.items()
                            if building_state==state and (building==k or (group and BUILDING_METADATA.get(building,{}).get('group_by')==group)))
                current+=sum(amount for (building_state,building),amount in self.buildings.items()
                             if building_state==state and (building==k or (group and BUILDING_METADATA.get(building,{}).get('group_by')==group)))
                r=current>float(v) if op=='>' else current<float(v)
            elif k in ('is_owned_by','is_controlled_by'):r=v=='ROOT'
            elif k=='free_building_slots':r=True
            elif k=='has_elections':r=True
            else:raise ValueError('Unmodelled core trigger '+k)
            result.append(r)
            if not r:return False
        return all(result)
    def execute(self,rows):
        previous=False
        for k,op,v in rows:
            if k=='if':
                previous=self.trigger(first(v,'limit',[]))
                if previous:self.execute([r for r in v if r[0]!='limit'])
            elif k=='else':
                if not previous:self.execute(v)
                previous=False
            elif k=='else_if':
                if not previous:
                    previous=self.trigger(first(v,'limit',[]))
                    if previous:self.execute([r for r in v if r[0]!='limit'])
            elif k in self.e:self.execute(self.e[k])
            elif k=='set_variable':
                a,_,b=v[0];self.v[a]=self.value(b)
            elif k=='add_to_variable':
                a,_,b=v[0];self.v[a]=self.v.get(a,0)+self.value(b)
            elif k=='set_temp_variable':
                a,_,b=v[0];self.tmp[a]=self.value(b)
            elif k=='subtract_from_temp_variable':
                a,_,b=v[0];self.tmp[a]=self.tmp.get(a,0)-self.value(b)
            elif k=='modify_treasury_effect':self.cash+=self.tmp['treasury_change']
            elif k=='set_country_flag':self.flags.add(v if isinstance(v,str) else first(v,'flag'))
            elif k=='clr_country_flag':self.flags.discard(v)
            elif k=='add_dynamic_modifier':self.dm.add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':self.dm.discard(first(v,'modifier'))
            elif k.isdigit():
                for kind,o,b in v:
                    if kind=='add_extra_state_shared_building_slots':
                        level=int(b);assert level>0,('invalid shared slot grant',k,level)
                        self.slot_grants[k]=self.slot_grants.get(k,0)+level
                        self.pending_slots[k]=self.pending_slots.get(k,0)+level
                    elif kind=='add_building_construction':
                        level=int(first(b,'level','1'))
                        assert self.pending_slots.get(k,0)>=level,('construction lacks same-state slots',k,level,self.pending_slots)
                        target=(k,first(b,'type'));self.buildings[target]=self.buildings.get(target,0)+int(first(b,'level'))
                        self.pending_slots[k]-=level
                    else:raise ValueError('Unmodelled state effect '+kind)
            elif k in ('hidden_effect',):self.execute(v)
            elif k=='effect_tooltip':continue
            elif k in ('add_political_power','add_stability','add_war_support','army_experience'):self.grants+=1
            elif k in ('force_update_dynamic_modifier','custom_effect_tooltip'):continue
            else:raise ValueError('Unmodelled core effect '+k)

if __name__=='__main__':main()
