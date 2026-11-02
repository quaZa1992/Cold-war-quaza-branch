# IMPERIA COLD WAR — Physical capacity for scripted national building grants.
"""Pure, bounded country-generator integration. Manual construction is separate."""
from __future__ import annotations
from collections import Counter,defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys
from textwrap import indent

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/usa_1970_expansion'))
from focus_prerequisite_ui import nodes,field
from usa_building_capacity import building_definitions

MARK='# IMPERIA COLD WAR — Scripted national building-grant integration.\n'
PREFIX='COLDWAR_GRANT_'
TECH_TYPES={'infrastructure','renewable_energy_infra','fuel_silo','nuclear_reactor','radar_station','anti_air_building','internet_station','enrichment_facility','synthetic_refinery','microchip_plant','composite_plant','rail_terminal','rocket_site'}

def block(key,body):return key+' = {\n'+indent(body.strip(),'\t')+'\n}'

def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())

def normal(text):
    def emit(n,depth=0):
        pad='\t'*depth
        if n.key=='_bare':return pad+str(n.value)
        if not isinstance(n.value,list):return pad+n.key+' '+n.op+' '+str(n.value)
        return pad+n.key+' '+n.op+' {\n'+'\n'.join(emit(c,depth+1) for c in n.children())+'\n'+pad+'}'
    return '\n'.join(emit(n) for n in nodes(text))

def cap_key(building,quantity):return PREFIX+'capacity_'+building+'_'+str(quantity)+'_tt'

def physical(building,quantity=1,tooltip=True):
    d=building_definitions()[building]
    assert not d['shares_slots'] and d['state_max'] is not None,(building,quantity)
    assert isinstance(quantity,int) and quantity>0
    raw='check_variable = { var = building_level@'+building+' value = '+str(int(d['state_max'])-quantity)+' compare = less_than_or_equals }'
    return block('custom_trigger_tooltip','tooltip = '+cap_key(building,quantity)+'\n'+raw) if tooltip else raw

def rewrite_queries(text,buildings=None):
    allowed=TECH_TYPES if buildings is None else set(buildings)
    edits=[]
    for n in walk(nodes(text)):
        if n.key!='free_building_slots':continue
        b=field(n.children(),'building')
        if b not in allowed or field(n.children(),'province') is not None:continue
        d=building_definitions()[b]
        if d['shares_slots'] or d['state_max'] is None:continue
        size=next(c for c in n.children() if c.key=='size')
        if size.op not in ('>','>='):raise AssertionError(('Unreviewed grant comparison',b,size.op))
        quantity=int(size.value)+(1 if size.op=='>' else 0)
        assert quantity>0
        edits.append((n.start,n.end,physical(b,quantity)))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    return text

def capacity_localisation():
    loc={}
    for building,d in sorted(building_definitions().items()):
        if d['shares_slots'] or d['state_max'] is None:continue
        for q in range(1,int(d['state_max'])+1):
            loc[cap_key(building,q)]='Room for §Y'+str(q)+'§! additional $'+building+'$ '+('level' if q==1 else 'levels')+'. State limit: §Y'+str(d['state_max'])+'§!.'
    return loc

@lru_cache(maxsize=1)
def scope():
    return json.loads((HERE/'scope.json').read_text(encoding='utf-8'))['countries']

@lru_cache(maxsize=1)
def helpers():
    source=(ROOT/'common/scripted_effects/00_scripted_effects.txt').read_text(encoding='utf-8-sig')
    inventory=json.loads((ROOT/'docs/design/building_capacity_audit_20261027/INVENTORY.json').read_text(encoding='utf-8'))
    wanted={r['helper'] for r in inventory['native_helper_callers']}
    result={}
    for n in nodes(source):
        if n.key not in wanted:continue
        grants=[c for c in walk(n.children()) if c.key=='add_building_construction']
        kind=field(grants[0].children(),'type')
        count=max([int(c.value) for c in walk(n.children()) if c.key=='random_select_amount'] or [1])
        prices=[float(c.value) for row in walk(n.children()) if row.key=='set_temp_variable' for c in row.children() if c.key=='treasury_change' and isinstance(c.value,str) and re.fullmatch(r'-?\d+(?:\.\d+)?',c.value)]
        assert prices and len(set(prices))==1,(n.key,prices)
        assert all(field(g.children(),'level')=='1' for g in grants),(n.key,'Review multi-level helper')
        result[n.key]=dict(building=kind,count=count,state='_state_' in n.key,fee=prices[0])
    assert set(result)==wanted,(set(result)^wanted)
    return result

def alias(name):return PREFIX+'native_'+name

def _body(text,n):return text[text.index('{',n.start)+1:n.end-1].strip()

def _fields(text,updates):
    root=nodes(text)[0];seen=set();edits=[]
    for n in root.children():
        if n.key not in updates:continue
        edits.append((n.start,n.end,updates[n.key] if n.key not in seen else ''));seen.add(n.key)
    missing='\n'.join(v for k,v in updates.items() if k not in seen)
    if missing:edits.append((root.end-1,root.end-1,'\n'+indent(missing,'\t')+'\n'))
    for a,b,value in sorted(edits,reverse=True):text=text[:a]+value+text[b:]
    return text

def rewrite_native_calls(text):
    names=set(helpers());edits=[]
    for n in walk(nodes(text)):
        if n.key in names and n.value=='yes':edits.append((n.start,n.start+len(n.key),alias(n.key)))
    for a,b,value in sorted(edits,reverse=True):text=text[:a]+value+text[b:]
    return text

def _state_limit(building,quantity=1):
    return 'is_owned_and_controlled_by = ROOT\n'+physical(building,quantity,False)

def _count_states(building,count):
    # Native 1.19.4 A/B checks prove strict comparisons. The installed
    # documentation's inclusive-comparison note is inaccurate here.
    collection=block('input','input = game:scope\n'+block('operators','owned_states\n'+block('limit',_state_limit(building))))
    return block('collection_size',collection+'\nvalue > '+str(count-1))

def _room(building,count,max_distinct=1):
    if count==1:return block('any_owned_state',_state_limit(building))
    if max_distinct>1:return _count_states(building,count)
    alternatives=[block('any_owned_state',_state_limit(building,count)),_count_states(building,count)]
    if count==3:alternatives.append(block('AND',block('any_owned_state',_state_limit(building,2))+'\n'+_count_states(building,2)))
    assert count<=3,('Review combined grant planning',building,count)
    return block('OR','\n'.join(alternatives))

def _grant(building,quantity=1):
    return 'add_extra_state_shared_building_slots = '+str(quantity)+'\nadd_building_construction = { type = '+building+' level = '+str(quantity)+' instant_build = yes }'

def _fee(value):
    return block('ROOT',block('if','limit = { NOT = { check_variable = { skip_payment = 1 } } }\nset_temp_variable = { treasury_change = '+format(value,'g')+' }\nmodify_treasury_effect = yes'))

def _random_grant(name,meta):
    building=meta['building'];count=meta['count'];remaining=PREFIX+'remaining_'+name;reserved=PREFIX+'selected_'+name
    grant=_grant(building)+'\nset_state_flag = '+reserved+'\n'+block('ROOT','subtract_from_temp_variable = { '+remaining+' = 1 }')
    first=block('every_owned_state',block('limit',_state_limit(building)+'\nis_in_home_area = yes')+'\nrandom_select_amount = '+str(count)+'\n'+grant)
    rest=[]
    for q in range(1,count+1):
        selection=block('every_owned_state',block('limit',_state_limit(building)+'\nNOT = { has_state_flag = '+reserved+' }')+'\nrandom_select_amount = '+str(q)+'\n'+grant)
        rest.append(block('if','limit = { check_variable = { '+remaining+' = '+str(q)+' } }\n'+selection))
    cleanup=block('every_owned_state','limit = { has_state_flag = '+reserved+' }\nclr_state_flag = '+reserved)
    return 'set_temp_variable = { '+remaining+' = '+str(count)+' }\n'+first+'\n'+'\n'.join(rest)+'\n'+cleanup

def _native_outputs():
    effects=[]
    for name,meta in sorted(helpers().items()):
        b=meta['building'];n=meta['count'];random=_random_grant(name,meta)
        preview_random=block('every_owned_state','random_select_amount = '+str(n)+'\n'+_grant(b))
        if meta['state']:
            own=_state_limit(b)
            preview=block('if',block('limit',own)+'\n'+_grant(b))+'\n'+block('else',block('ROOT',preview_random))
            action=block('if',block('limit',own)+'\n'+_grant(b))+'\n'+block('else',block('ROOT',random))
            ready=block('OR',block('AND',own)+'\n'+block('ROOT',_room(b,n,n)))
        else:
            preview=preview_random;action=random;ready=_room(b,n,n)
        body=block('effect_tooltip',preview+'\n'+_fee(meta['fee']))+'\n'+block('hidden_effect',block('if',block('limit',ready)+'\n'+action+'\n'+_fee(meta['fee'])))
        effects.append(block(alias(name),body))
    return effects

def add_missing_slots(text):
    edits=[]
    def visit(rows):
        for i,n in enumerate(rows):
            if n.key=='add_building_construction':
                amount=field(n.children(),'level','1')
                if i and rows[i-1].key=='add_extra_state_shared_building_slots' and rows[i-1].value==amount:continue
                prefix=text[text.rfind('\n',0,n.start)+1:n.start]
                prefix=prefix if not prefix.strip() else ''
                edits.append((n.start,'add_extra_state_shared_building_slots = '+amount+'\n'+prefix))
            visit(n.children())
    visit(nodes(text))
    for pos,new in sorted(edits,reverse=True):text=text[:pos]+new+text[pos:]
    return text

def require_physical_owner(text,owner='ROOT'):
    edits=[]
    for n in walk(nodes(text)):
        if not(n.key.isdecimal() or n.key=='capital_scope'):continue
        if any(c.key=='is_owned_and_controlled_by' for c in n.children()):continue
        if any(c.key=='custom_trigger_tooltip' and str(field(c.children(),'tooltip','')).startswith(PREFIX+'capacity_') for c in n.children()):
            pos=text.index('{',n.start)+1
            edits.append((pos,'\nis_owned_and_controlled_by = '+owner+'\n'))
    for pos,value in sorted(edits,reverse=True):text=text[:pos]+value+text[pos:]
    return text

_TREES={}
_RECORDS={}

def _original_available(raw,fid):
    n=next((n for n in nodes(raw)[0].children() if n.key=='available'),None)
    if n is None:return ''
    kept=[]
    for c in n.children():
        if c.key=='custom_trigger_tooltip' and field(c.children(),'tooltip')==PREFIX+'focus_capacity_'+fid+'_tt':continue
        if c.key=='hidden_trigger' and any(z.key=='has_country_flag' and z.value==PREFIX+'done_'+fid for z in walk(c.children())):continue
        kept.append(raw[c.start:c.end])
    return '\n'.join(kept)

def _external_available(payload,external_triggers=None):
    """Retain the requirements of the newer DDR paid transactions verbatim."""
    calls=[n.key for n in walk(nodes(payload)) if n.key.startswith('COLDWAR_DDR_20261027_run_') and n.value=='yes']
    if not calls:return None
    assert len(calls)==1,('Review combined external transactions',calls)
    source=external_triggers
    if source is None:
        source=(ROOT/'common/scripted_triggers/COLDWAR_DDR_20261027_programmes.txt').read_text(encoding='utf-8-sig')
    key=calls[0].replace('_run_','_can_',1)
    matching=[n for n in nodes(source) if n.key==key]
    assert len(matching)==1,('Missing external transaction requirement',key)
    return _body(source,matching[0])

def _fixed_capacity(payload,fid):
    """Read complete fixed-state quantities from the transaction's native preview."""
    quantities=Counter()
    def visit(rows,state=None):
        for n in rows:
            target=n.key if n.key.isdecimal() else state
            if n.key=='add_building_construction':
                assert target is not None,(fid,'Unreviewed nonfixed direct grant')
                assert field(n.children(),'instant_build')=='yes',(fid,'Queued grant needs a separate contract')
                quantities[target,field(n.children(),'type')]+=int(field(n.children(),'level','1'))
            visit(n.children(),target)
    visit(nodes(payload))
    assert quantities,(fid,'No adapted grant payload')
    by_state=defaultdict(list)
    for (state,building),quantity in sorted(quantities.items()):
        maximum=building_definitions()[building]['state_max']
        assert maximum is not None,(fid,building,'Review province or uncapped grant')
        by_state[state].append('check_variable = { var = building_level@'+building+' value = '+str(int(maximum)-quantity)+' compare = less_than_or_equals }')
    return '\n'.join(block(state,'is_owned_and_controlled_by = ROOT\n'+'\n'.join(checks)) for state,checks in by_state.items())

def _programme_capacity(payload,fid):
    if fid=='LBA_1970_a_revolutionary_administration':
        office=int(building_definitions()['offices']['state_max'])-1
        return block('391','is_owned_and_controlled_by = LBA\ncheck_variable = { var = building_level@offices value = '+str(office)+' compare = less_than_or_equals }\n'+physical('internet_station',1,False))
    grouped=defaultdict(list);helper_names={alias(k):k for k in helpers()}
    for n in walk(nodes(payload)):
        if n.key in helper_names and n.value=='yes':grouped[helpers()[helper_names[n.key]]['building']].append(helpers()[helper_names[n.key]])
    if not grouped:return _fixed_capacity(payload,fid)
    conditions=[]
    for building,items in grouped.items():
        amount=sum(m['count'] for m in items);maximum=max(m['count'] for m in items)
        assert not(maximum>1 and len(items)>1),(fid,'Review multiple distinct-state batches')
        condition=_room(building,amount,maximum)
        # The original focus awards air defence only after its named technology.
        # Retain its research-only route when that condition is false.
        if fid=='GEN_1970_countermeasures_against_aircraft':
            guard='OR = { AND = { has_dlc = "Gotterdammerung" has_tech = air_defense } has_tech = air_defense_non_got }'
            condition=block('OR',block('NOT',guard)+'\n'+condition)
        conditions.append(condition)
    assert conditions,(fid,'No adapted grant payload')
    return '\n'.join(conditions)

def repair_focus_tree(tag,text,external_triggers=None):
    spec=scope()[tag];tree=next(n for n in nodes(text) if n.key=='focus_tree');records=[];edits=[]
    for focus in tree.children():
        if focus.key!='focus':continue
        fid=field(focus.children(),'id')
        if fid not in spec['focuses']:continue
        raw=text[focus.start:focus.end];f=nodes(raw)[0]
        completion=next(n for n in f.children() if n.key=='completion_reward')
        wrapped=any(n.key==PREFIX+'complete_'+fid for n in walk(completion.children()))
        payload=_body(raw,next(n for n in completion.children() if n.key=='effect_tooltip')) if wrapped else _body(raw,completion)
        payload=normal(add_missing_slots(rewrite_queries(rewrite_native_calls(payload))))
        assert not any(n.key==PREFIX+'complete_'+fid for n in walk(nodes(payload))),(fid,'Recursive focus reward')
        if fid=='GEN_1970_capital_defence_scheme':payload=normal(require_physical_owner(payload))
        # A wrapped tree carries its complete reviewed availability. During an
        # atomic overlay build, the freshly supplied triggers can be newer than
        # the files on disk; a later runtime-pack pass must not read old guards.
        external=_external_available(payload,external_triggers) if tag=='DDR' and (not wrapped or external_triggers is not None) else None
        available=normal(rewrite_queries(_original_available(raw,fid) if external is None else external))
        capacity=_programme_capacity(payload,fid)
        new_available=available+'\n'+block('hidden_trigger','NOT = { has_country_flag = '+PREFIX+'done_'+fid+' }')+'\n'+block('custom_trigger_tooltip','tooltip = '+PREFIX+'focus_capacity_'+fid+'_tt\n'+PREFIX+'capacity_'+fid+' = yes')
        new_reward=block('completion_reward',block('effect_tooltip',payload)+'\n'+block('hidden_effect',PREFIX+'complete_'+fid+' = yes'))
        replacement=normal(_fields(raw,{'available':block('available',new_available),'completion_reward':new_reward,'cancel_if_invalid':'cancel_if_invalid = yes','continue_if_invalid':'continue_if_invalid = no'}))
        prefix=text[text.rfind('\n',0,focus.start)+1:focus.start]
        prefix=prefix if not prefix.strip() else ''
        replacement=replacement.replace('\n','\n'+prefix)
        edits.append((focus.start,focus.end,replacement))
        groups=[[c.value for c in p.children() if c.key=='focus'] for p in f.children() if p.key=='prerequisite']
        excluded=[c.value for p in f.children() if p.key=='mutually_exclusive' for c in p.children() if c.key=='focus']
        records.append(dict(id=fid,tag=tag,tree=field(tree.children(),'id'),payload=payload,available=available,capacity=capacity,prerequisites=groups,excluded=excluded))
    assert len(records)==len(spec['focuses']),(tag,'Missing reviewed focus',len(records),len(spec['focuses']))
    for a,b,new in sorted(edits,reverse=True):text=text[:a]+new+text[b:]
    if not text.startswith('# IMPERIA COLD WAR —'):text=MARK+text
    _TREES[tag]=text;_RECORDS[tag]=records
    return text

def _programme_outputs():
    effects=[];triggers=[];actions=[];loc={}
    for tag,spec in scope().items():
        repair_focus_tree(tag,_TREES.get(tag) or (ROOT/spec['tree']).read_text(encoding='utf-8-sig'))
        tick=[];pending=[]
        for r in _RECORDS[tag]:
            fid=r['id'];done=PREFIX+'done_'+fid;wait=PREFIX+'pending_'+fid
            triggers.append(block(PREFIX+'capacity_'+fid,r['capacity']))
            ready='IMP_is_1970_scenario = yes\nhas_focus_tree = '+r['tree']+'\nNOT = { has_country_flag = '+done+' }\n'+r['available']+'\n'+r['capacity']
            if tag!='GENERIC1970':ready+='\ntag = '+tag
            for group in r['prerequisites']:ready+='\n'+block('OR','\n'.join('has_completed_focus = '+p for p in group))
            for other in r['excluded']:ready+='\nNOT = { has_completed_focus = '+other+' }'
            triggers.append(block(PREFIX+'ready_'+fid,ready))
            country_guard='IMP_is_1970_scenario = yes\nhas_focus_tree = '+r['tree']+'\nNOT = { has_country_flag = '+done+' }'+('' if tag=='GENERIC1970' else '\ntag = '+tag)
            delivered=r['payload']+'\nset_country_flag = '+done+'\nclr_country_flag = '+wait
            effects.append(block(PREFIX+'complete_'+fid,block('if',block('limit',country_guard)+'\nset_country_flag = '+wait+'\nset_country_flag = '+PREFIX+'any_pending\n'+block('if',block('limit',PREFIX+'ready_'+fid+' = yes')+'\n'+delivered))))
            tick.append(block('if','limit = { has_country_flag = '+wait+' }\n'+PREFIX+'complete_'+fid+' = yes'))
            # Stamp completed content in existing saves without replaying rewards.
            tick.append(block('if','limit = { has_completed_focus = '+fid+' NOT = { has_country_flag = '+wait+' } NOT = { has_country_flag = '+done+' } }\nset_country_flag = '+done))
            pending.append('has_country_flag = '+wait)
            loc[PREFIX+'focus_capacity_'+fid+'_tt']='Owned and controlled states have room for the complete building programme.'
        tick.append(block('if',block('limit',block('NOT',block('OR','\n'.join(pending))))+'\nclr_country_flag = '+PREFIX+'any_pending'))
        effects.append(block(PREFIX+'tick_'+tag,'\n'.join(tick)))
        hook='on_daily' if tag=='GENERIC1970' else 'on_daily_'+tag
        guard='IMP_is_1970_scenario = yes\nhas_focus_tree = '+_RECORDS[tag][0]['tree']+'\nOR = { has_country_flag = '+PREFIX+'any_pending NOT = { has_country_flag = '+PREFIX+'migrated_'+tag+' } }'
        call=PREFIX+'tick_'+tag+' = yes\nset_country_flag = '+PREFIX+'migrated_'+tag
        actions.append(block(hook,block('effect',block('if',block('limit',guard)+'\n'+call))))
    return effects,triggers,actions,loc

def runtime_outputs():
    loc=capacity_localisation()
    effects,triggers,actions,extra_loc=_programme_outputs();loc.update(extra_loc)
    return {'localisation/english/COLDWAR_GRANT_capacity_l_english.yml':'l_english:\n'+MARK+'\n'.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False) for k,v in sorted(loc.items()))+'\n',
            'common/scripted_effects/COLDWAR_GRANT_native.txt':MARK+'\n\n'.join(_native_outputs())+'\n',
            'common/scripted_effects/COLDWAR_GRANT_programmes.txt':MARK+'\n\n'.join(effects)+'\n',
            'common/scripted_triggers/COLDWAR_GRANT_programmes.txt':MARK+'\n\n'.join(triggers)+'\n',
            'common/on_actions/COLDWAR_GRANT_programmes.txt':MARK+block('on_actions','\n\n'.join(actions))+'\n'}

def write_outputs(outputs=None):
    changed=[]
    for path,text in (runtime_outputs() if outputs is None else outputs).items():
        p=ROOT/path;data=text.encode('utf-8-sig' if path.endswith('.yml') else 'utf-8')
        if p.exists() and p.read_bytes()==data:continue
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);changed.append(path)
    return changed

if __name__=='__main__':print(json.dumps(dict(project='IMPERIA COLD WAR',changed=write_outputs()),indent=2))
