# IMPERIA CW — Cold War: israel 1970 — validate policy map.
"""Check the existing Sinai target and removal of the superseded map split."""
from pathlib import Path
import json,re
from script_format import read

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
errors=[];checks=0

def check(ok,message):
    global checks
    checks+=1
    if not ok:errors.append(message)

def value(ast,key,default=None):return next((v for k,o,v in ast if k==key),default)

def provinces(state):return {int(k) for k,o,v in value(state,'provinces',[]) if o is None and k.isdigit()}

spec=json.loads((HERE/'policy_map_source.json').read_text(encoding='utf-8'))
original=read(spec['original_state_214'])
main=read((ROOT/'history/states/214-Suez.txt').read_text(encoding='utf-8-sig'))
check(main==original,'State 214 was not restored with all original population, history, buildings and provinces')
check(not (ROOT/'history/states/1252-Suez Canal.txt').exists(),'Superseded canal state still exists')
check(not (ROOT/'common/state_category/ISR70_delta_remainder.txt').exists(),'Superseded split category still exists')
sinai=value(read((ROOT/'history/states/213-Sinai.txt').read_text(encoding='utf-8-sig')),'state')
check(provinces(sinai)=={1155,10099,1112,12073,11922,10002,4161,11979,9947},'Sinai province boundaries changed')
expected={p:213 for p in provinces(sinai)}
expected.update({1178:214,4073:214,12049:214})
assigned={}
for path in (ROOT/'history/states').glob('*.txt'):
    state=value(read(path.read_text(encoding='utf-8-sig')),'state',[])
    for province in provinces(state):
        if province in expected:
            check(province not in assigned,'Province appears in multiple states: '+str(province))
            assigned[province]=int(value(state,'id'))
check(assigned==expected,'Sinai or canal provinces have an incorrect state assignment')
placements=(ROOT/'map/buildings.txt').read_text(encoding='utf-8-sig').splitlines()
check(not any(line.startswith('1252;') for line in placements),'Obsolete canal building-model state references remain')
for province in (4073,12049):
    check(any(line.startswith('214;floating_harbor;') and line.endswith(';'+str(province)) for line in placements),'Canal port model not restored: '+str(province))
hooks=(ROOT/'common/on_actions/02_dod_on_actions.txt').read_text(encoding='utf-8-sig')
check('# ISR70 canal closure adapter' in hooks and 'controls_state = 214' in hooks,'Original canal shore-control hooks missing')
check('1252' not in hooks,'Native on_actions still refer to the obsolete canal state')
money=(ROOT/'common/scripted_effects/00_money_system.txt').read_text(encoding='utf-8-sig')
check(money.count('has_global_flag = ISR70_policy_canal_open')>=2,'Closed canal can still earn native income')
metadata=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
check(metadata['policy_expansion']['target_state']==213,'Expansion target is not Sinai')
check(metadata['policy_expansion']['map']['borders_changed'] is False,'Expansion still splits the map')
check(metadata['policy_status_rules']['state']==213,'Occupation status is not scoped to Sinai')
check(metadata['policy_factory_access']['state']==213,'Factory access is not scoped to Sinai')
for migration in metadata['policy_migrations']:
    check(migration['source']==204 and migration['target']==213,'Migration routes outside the Sinai programme')
for project in metadata['policy_expansion']['projects']:
    if project['key'].startswith(('gi_','occ_')):
        check(project['states']==[213],'Territorial project targets a non-Sinai state: '+project['key'])
    for building in project['buildings']:
        if 'province' in building and project['states']==[213]:
            check(building['province'] in provinces(sinai),'Project port lies outside Sinai: '+project['key'])
effects=(ROOT/'common/scripted_effects/ISR70_policy_effects.txt').read_text(encoding='utf-8-sig')
cores=[k for k,o,v in read(effects) if k=='ISR70_policy_complete_gi_canal_core']
check(len(cores)==1,'Sinai core completion missing or duplicated')
core=next(v for k,o,v in read(effects) if k=='ISR70_policy_complete_gi_canal_core')
check(any(k=='213' and ('add_core_of','=','ISR') in v for k,o,v in core if isinstance(v,list)),'Core completion does not core Sinai')
for rel in ('common/national_focus/ISR70_focus.txt','common/scripted_effects/ISR70_policy_effects.txt','common/scripted_triggers/ISR70_policy_triggers.txt','common/decisions/ISR70_policy_decisions.txt','events/ISR70_policy_events.txt'):
    text=(ROOT/rel).read_text(encoding='utf-8-sig')
    check(not re.search(r'(?<![\w])1252(?![\w])',text),'Obsolete state reference in '+rel)
check('set_global_flag = ISR70_policy_canal_open' not in next(project['delivery_summary'] for project in metadata['policy_expansion']['projects'] if project['key']=='gi_canal_navigation'),'Sinai logistics still advertises canal opening')
result={'status':'FAIL' if errors else 'PASS','checks':checks,'errors':errors,'target_state':213,'canal_state':214,'borders_changed':False,'runtime_test':False}
(ROOT/'docs/israel_1970_design/policy_map_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
