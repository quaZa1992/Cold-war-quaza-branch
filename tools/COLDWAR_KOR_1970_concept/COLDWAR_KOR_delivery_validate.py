# IMPERIA COLD WAR — Cold War: diplomatic delivery, USFK consent and preservation checks.
from pathlib import Path
import argparse,json,sys,hashlib
HERE=Path(__file__).parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
from COLDWAR_KOR_alliance_revision import load_design
from COLDWAR_KOR_reward_revision import OVERLAY
from COLDWAR_KOR_runtime_scenarios import World,P
from COLDWAR_KOR_presentation_validate import executable,predicate,digest

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');a=ap.parse_args();base=ROOT if a.installed else HERE/'runtime_staged'
 d=load_design();pre_reward=load_design(apply_rewards=False);w=World(base);errors=[];checks=[]
 def ck(ok,text):
  if not ok:errors.append(text)
 by={n['id']:n for n in d['nodes']};old=json.loads((DOC/'COLDWAR_KOR_design.json').read_text(encoding='utf-8'))
 pre_reward_by_key={n['key']:n for n in pre_reward['nodes']}
 reward_revision=json.loads(OVERLAY.read_text(encoding='utf-8'))
 authorized_reward_ids={P+key for key in reward_revision['entries']} | {P+key for key in reward_revision.get('projects',{})}
 ck(len(by)==300 and all(n['id'] in by for n in old['nodes']),'300 cap and all original IDs preserved')
 ck(sum(n['group']=='usfk' for n in d['nodes'])==12,'USFK branch depth')
 for i,n in enumerate(d['nodes']):
  for m in d['nodes'][i+1:]:
   ck(not(abs(n['xy'][0]-m['xy'][0])*96<165 and abs(n['xy'][1]-m['xy'][1])*130<128),'Card overlap: '+n['id']+' / '+m['id'])
 ck(len(d['layout']['shortcuts'])==8,'Native shortcut cap')
 # Preserve the untouched political programmes and shared native integration.
 baseline=DOC/'COLDWAR_KOR_delivery_baseline.json'
 def protected(base):
  result={}
  e={k:v for k,o,v in parse((base/'common/scripted_effects/COLDWAR_KOR_1970_focus.txt').read_text(encoding='utf-8'))}
  t={k:v for k,o,v in parse((base/'common/scripted_triggers/COLDWAR_KOR_1970_focus.txt').read_text(encoding='utf-8'))}
  for n in old['nodes']:
   if n['group'] in ('defence','foreign','korea') or n['id'] in authorized_reward_ids:continue
   for key,body in ((P+'complete_'+n['key'],e[P+'complete_'+n['key']]),):result[key]=digest(executable(body,t))
  return result
 if not baseline.exists():
  assert not a.installed,'Capture pre-install baseline first'
  baseline.write_text(json.dumps({'protected_political_effects':protected(ROOT)},indent=2)+'\n',encoding='utf-8')
 ck(protected(base)==json.loads(baseline.read_text())['protected_political_effects'],'Unrelated political focus effects changed')
 ck(d.get('reward_revision',{}).get('entries')==len(reward_revision['entries']),
    'Effective design records the complete reward overlay')
 ck(d.get('reward_revision',{}).get('projects')==len(reward_revision.get('projects',{})),
    'Effective design records the complete tangible-project overlay')
 # Every authorized overlay leaf must carry the concrete final slot values used by
 # both catalogue previews and later emission. All other gate/graph checks remain
 # against the immutable baseline above.
 for key,entry in reward_revision['entries'].items():
  node=next((n for n in d['nodes'] if n['key']==key),None)
  policy=next((p for p in node.get('effects',{}).get('policies',[]) if p['slot']==entry['slot']),None) if node else None
  ck(bool(policy),'Missing effective reward policy '+key)
  if policy:
   ck(all(policy['modifiers'].get(k)==v for k,v in entry['modifiers'].items()),
      'Overlay reward values missing from preview data '+key)
   leaf=node.get('native_leaf_effects','')
   ck(all(f"{node['id']}_{entry['slot']}_{k} = {v:g}" in leaf for k,v in entry['modifiers'].items()),
      'Overlay reward values missing from native leaf data '+key)
  for bonus in entry.get('equipment_bonuses',[]):
   ck(bonus in node.get('effects',{}).get('equipment_bonuses',[]),
      'Equipment bonus missing from effect preview '+key)
   ck('name = '+bonus['name'] in node.get('native_leaf_effects','') and
      all(f'{equipment_type} = {{' in node['native_leaf_effects'] and
          all(f'{modifier} = {value:g}' in node['native_leaf_effects'] for modifier,value in values.items())
          for equipment_type,values in bonus['types'].items()),
      'Equipment bonus missing from native reward '+key)
  for bonus in entry.get('tech_bonuses',[]):
   ck(bonus in node.get('effects',{}).get('tech_bonuses',[]),
      'Research bonus missing from effect preview '+key)
   text=f"name = {bonus['name']}"
   ck(text in node.get('native_leaf_effects','') and
      f"bonus = {bonus['bonus']:g}" in node['native_leaf_effects'] and
      f"uses = {bonus['uses']}" in node['native_leaf_effects'] and
      f"category = {bonus['category']}" in node['native_leaf_effects'],
      'Research bonus missing from native reward '+key)
  for bonus in entry.get('doctrine_bonuses',[]):
   ck(bonus in node.get('effects',{}).get('doctrine_bonuses',[]),
      'Doctrine bonus missing from effect preview '+key)
   ck(f"name = {bonus['name']}" in node.get('native_leaf_effects','') and
      f"cost_reduction = {bonus['cost_reduction']:g}" in node['native_leaf_effects'] and
      f"uses = {bonus['uses']}" in node['native_leaf_effects'] and
      f"category = {bonus['category']}" in node['native_leaf_effects'],
      'Doctrine bonus missing from native reward '+key)
 for key,project in reward_revision.get('projects',{}).items():
  node=next((n for n in d['nodes'] if n['key']==key),None)
  ck(bool(node),'Missing tangible project focus '+key)
  if not node:continue
  effects=node.get('effects',{});leaf=node.get('native_leaf_effects','')
  fixed_cost=pre_reward_by_key[key]['effects'].get('cost',0)
  base_fraction=min(fixed_cost*reward_revision['domestic_gdp_cost_scale']['basis_per_legacy_billion'],
                    reward_revision['domestic_gdp_cost_scale']['maximum_base_fraction']) if fixed_cost>0 else 0
  ck(effects.get('cost',0)==0,
     'Domestic project focus retained a flat Treasury charge '+key)
  ck(effects.get('legacy_fixed_cost_bn',0)==fixed_cost and
     abs(effects.get('gdp_base_cost_fraction',0)-base_fraction)<1e-9,
     'Domestic project focus has the wrong converted base GDP charge '+key)
  fraction=project.get('gdp_cost_fraction',0)
  total_fraction=base_fraction+fraction
  ck(effects.get('gdp_project_cost_fraction',0)==fraction and
     abs(effects.get('gdp_share_cost_fraction',0)-total_fraction)<1e-9,
     'Project and converted base GDP fractions do not match total cost '+key)
  for building in project.get('buildings',[]):
   ck(building in effects.get('buildings',[]),'Project building missing from preview data '+key)
   expected=(f"{building['state']} = {{ add_building_construction = {{ type = {building['type']} "
             f"level = {building['level']} instant_build = yes }} }}")
   ck(expected in leaf,'Project building missing from native reward '+key)
  for field in ('equipment_bonuses','tech_bonuses','doctrine_bonuses'):
   for bonus in project.get(field,[]):
    ck(bonus in effects.get(field,[]),'Project '+field+' missing from effect preview '+key)
    ck('name = '+bonus['name'] in leaf,'Project '+field+' missing from native reward '+key)
 # Every positive domestic base focus cost uses one combined GDP formula in its
 # effective leaf. Bilateral terms live in contracts and are untouched.
 ck(d['contracts']==pre_reward['contracts'],
    'Domestic cost conversion changed bilateral agreement or recipient terms')
 def gdp_multipliers(rows):
  result=[]
  for row,_,body in walk(rows):
   if row!='set_temp_variable' or not isinstance(body,list):continue
   change=first(body,'treasury_change')
   if isinstance(change,list) and first(change,'value')=='gdp_total' and first(change,'multiply') is not None:
    result.append(float(first(change,'multiply')))
  return result
 scale=reward_revision['domestic_gdp_cost_scale']
 for node in d['nodes']:
  old=pre_reward_by_key[node['key']]['effects'].get('cost',0)
  base=min(old*scale['basis_per_legacy_billion'],scale['maximum_base_fraction']) if old>0 else 0
  project=reward_revision.get('projects',{}).get(node['key'],{}).get('gdp_cost_fraction',0)
  total=base+project
  effects=node.get('effects',{})
  if old>0:
   ck(effects.get('cost',0)==0 and effects.get('legacy_fixed_cost_bn')==old,
      'Legacy domestic flat cost not converted '+node['key'])
  if total:
   ck(abs(effects.get('gdp_share_cost_fraction',0)-total)<1e-9,
      'Effective total GDP fraction mismatch '+node['key'])
   multipliers=gdp_multipliers(parse(node.get('native_leaf_effects','')))
   ck(len(multipliers)==1 and abs(multipliers[0]+total)<1e-8,
      'Native cost leaf is not one total GDP-based charge '+node['key'])
 ideas={}
 for path in (base/'common/ideas').glob('COLDWAR_KOR_1970*.txt'):
  for key,o,body in first(first(parse(path.read_text(encoding='utf-8')),'ideas',[]),'country',[]):ideas[key]=body
 for c in d['contracts']:
  key=c['key'];helper=w.e.get(P+'preview_agreement_'+key,[])
  ck(bool(helper),'Missing numerical agreement preview '+key)
  for side in ('kor','partner'):
   mods={}
   if side=='kor':
    for policy in c['KOR_policy']:mods.update(policy['modifiers'])
   else:mods.update(c['recipient_effects'].get('policy',{}))
   if not mods:continue
   preview=ideas.get(P+'agreement_'+key+'_'+side+'_preview',[])
   actual={k:float(v) for k,o,v in first(preview,'modifier',[])}
   ck(actual==mods,'Inaccurate visible agreement coefficients '+key+' / '+side)
   prefix=P+'1970_foreign_'+key+'_'+side
   for id,body in w.dm.items():
    if id==prefix or id.startswith(prefix+'_'):
     coefficients={k:float(v) for k,o,v in body if k not in ('icon','enable')}
     ck(coefficients==mods,'Executed agreement coefficients differ '+id)
 # Every offer focus must actually include its numerical proposal helper.
 focus=first(parse((base/'common/national_focus/COLDWAR_KOR_1970_focus.txt').read_text(encoding='utf-8')),'focus_tree',[])
 foci={first(n,'id'):n for n in values(focus,'focus')}
 for n in d['nodes']:
  for action in n['effects']['actions']:
   if action.get('type')!='offer':continue
   preview=first(first(foci[n['id']],'completion_reward',[]),'effect_tooltip',[])
   ck((P+'preview_agreement_'+action['value'],'=','yes') in preview,'Focus omits material offer preview '+n['id'])
 def test(name,fn):
  try:fn();checks.append(name)
  except Exception as exc:errors.append(name+': '+repr(exc))
 def setup():
  x=World(base);x.c['KOR']['v'][P+'office_epoch']=1
  x.call('send_us_garrison');x.call('accept_us_garrison','USA')
  assert P+'usfk_member' in x.c['KOR']['ideas'] and P+'usfk_member' in x.c['USA']['ideas']
  assert 'KOR' in x.c['USA']['access']
  x.addflag('KOR',P+'combined_exercises_paid')
  x.c['KOR']['v']['num_divisions']=5;x.c['USA']['v']['num_divisions']=5
  return x
 def contacts():
  x=World(base);cash=x.snapshot_cash();x.call('send_working_contacts');assert x.snapshot_cash()==cash
  x.call('accept_working_contacts','NKO');assert x.c['KOR']['v']['treasury']==-1 and x.c['NKO']['v']['treasury']==-1
  assert x.weekly('KOR')[0]==.001 and x.weekly('NKO')[0]==.001
  assert P+'1970_foreign_working_contacts_kor' in x.c['KOR']['dm'] and P+'1970_foreign_working_contacts_partner' in x.c['NKO']['dm']
  before=x.snapshot_cash();x.call('accept_working_contacts','NKO');assert x.snapshot_cash()==before
 test('Working Contacts has reciprocal paid benefits only after acceptance and cannot replay',contacts)
 def replies():
  x=World(base);x.call('send_working_contacts');x.call('refuse_working_contacts','NKO')
  assert any(id==P+'foreign.406' for tag,id,day in x.queue) and x.snapshot_cash()['KOR']==0
  x.day=181;x.call('send_working_contacts');assert not x.flag('KOR',P+'working_contacts_refused')
  x.day=241;x.call('contract_maintenance');assert any(id==P+'foreign.506' for tag,id,day in x.queue)
 test('Decline and expiry have distinct visible feedback; new offers clear obsolete refusal state',replies)
 def old_terms():
  x=World(base)
  for tag in ('KOR','NKO'):x.addflag(tag,P+'working_contacts_signed')
  assert x.weekly('KOR')==(0,0) and x.weekly('NKO')==(0,0)
  before=x.snapshot_cash();x.call('foreign_initialize');assert x.snapshot_cash()==before
  assert not x.flag('KOR',P+'working_contacts_signed') and x.flag('KOR',P+'legacy_working_contacts')
  assert any(id==P+'foreign.700' for tag,id,day in x.queue)
  x.call('send_working_contacts');x.call('accept_working_contacts','NKO');assert x.c['KOR']['v']['treasury']==-1
 test('Older free frameworks require fresh consent before revised fees or material benefits',old_terms)
 def field():
  x=setup();cash=x.snapshot_cash();x.call('usfk_exercise_invite_field');x.call('usfk_exercise_accept','USA');assert x.snapshot_cash()==cash
  x.call('usfk_exercise_conduct');assert x.c['KOR']['v']['treasury']==cash['KOR']-2 and x.c['USA']['v']['treasury']==cash['USA']-1
  assert abs(x.weekly('KOR')[0]-.006)<1e-9 and abs(x.weekly('USA')[0]-.008)<1e-9
  paid=x.snapshot_cash();x.call('usfk_exercise_conduct');assert x.snapshot_cash()==paid
  x.day=29;x.call('usfk_exercise_daily');assert x.c['KOR']['v'].get('army_experience',0)==0
  x.day=30;x.call('usfk_exercise_daily');assert x.c['KOR']['v']['army_experience']==40 and x.c['USA']['v']['army_experience']==15
  assert x.weekly('KOR')[0]==.002 and x.weekly('USA')[0]==.004
  x.call('usfk_exercise_daily');x.call('usfk_exercise_complete');assert x.c['KOR']['v']['army_experience']==40
  assert 'KOR' in x.c['USA']['access']
 test('Field exercise requires both approvals, charges once, runs for30days and rewards each army once',field)
 def cancel():
  for refusal in (True,False):
   x=setup();cash=x.snapshot_cash();x.call('usfk_exercise_invite_staff')
   if refusal:x.call('usfk_exercise_decline','USA')
   else:x.call('usfk_exercise_accept','USA');x.call('usfk_exercise_cancel')
   assert x.snapshot_cash()==cash and not x.flag('KOR',P+'usfk_exercise_running')
 test('US refusal and Korean cancellation commit no exercise resources',cancel)
 def stale():
  x=setup();cash=x.snapshot_cash();x.call('usfk_exercise_invite_staff');x.c['KOR']['v'][P+'office_epoch']=2
  x.call('usfk_exercise_accept','USA');x.call('usfk_exercise_conduct');assert x.snapshot_cash()==cash
  x.call('usfk_exercise_daily');assert not x.flag('KOR',P+'usfk_exercise_pending')
 test('A changed Korean negotiating mandate invalidates a pending exercise without charge',stale)
 def war():
  x=setup();x.call('usfk_exercise_invite_field');x.call('usfk_exercise_accept','USA');x.call('usfk_exercise_conduct')
  x.wars.add(frozenset(('KOR','NKO')));x.day=5;x.call('usfk_exercise_daily');assert not x.flag('KOR',P+'usfk_exercise_running')
  x.day=35;x.call('usfk_exercise_complete');assert x.c['KOR']['v'].get('army_experience',0)==0
 test('War interrupts field training and denies an uncompleted training reward',war)
 def no_army():
  x=setup();x.c['USA']['v']['num_divisions']=0;before=x.snapshot_cash()
  x.call('usfk_exercise_invite_field');x.call('usfk_exercise_accept','USA');x.call('usfk_exercise_conduct');assert x.snapshot_cash()==before
  assert not x.flag('KOR',P+'usfk_exercise_running')
 test('Field training cannot award experience from an absent participating army',no_army)
 def drawdown():
  x=setup();x.addflag('KOR',P+'strategic_autonomy_paid');x.call('send_us_drawdown');x.call('accept_us_drawdown','USA')
  assert not x.flag('KOR',P+'us_garrison_signed') and 'KOR' not in x.c['USA']['access']
  assert P+'usfk_member' in x.c['KOR']['ideas'] and P+'usfk_member' in x.c['USA']['ideas']
  x.call('usfk_exercise_invite_staff');x.call('usfk_exercise_accept','USA');x.call('usfk_exercise_conduct')
  assert 'KOR' in x.c['USA']['access'];x.day=30;x.call('usfk_exercise_daily')
  assert 'KOR' not in x.c['USA']['access'] and x.c['KOR']['v']['army_experience']==20 and x.c['USA']['v']['army_experience']==10
 test('Agreed drawdown removes stationing benefits yet permits consensual visiting-force exercises',drawdown)
 def previous_access():
  x=World(base);x.c['USA']['access'].add('KOR');x.call('send_us_garrison');x.call('accept_us_garrison','USA')
  assert not x.flag('KOR',P+'usfk_access_granted')
  x.addflag('KOR',P+'strategic_autonomy_paid');x.call('send_us_drawdown');x.call('accept_us_drawdown','USA');assert 'KOR' in x.c['USA']['access']
 test('Pre-existing military access is never revoked by the new agreement cleanup',previous_access)
 def expiry():
  x=setup();x.day=1825;x.call('contract_maintenance')
  assert P+'usfk_member' not in x.c['KOR']['ideas'] and P+'usfk_member' not in x.c['USA']['ideas'] and 'KOR' not in x.c['USA']['access']
  assert x.weekly('KOR')==(0,0) and x.weekly('USA')==(0,0)
 test('Stationing expiry removes owned access, membership and recurring support costs',expiry)
 report={'status':'FAIL' if errors else 'PASS','target':'installed' if a.installed else 'staged','focuses':len(by),'usfk_focuses':12,'contracts':len(d['contracts']),'protected_political_effects':len(protected(base)),'tests':checks,'errors':errors,'scope':'Static native-source checks plus bounded emitted-script execution; not an HOI4 engine, multiplayer or saved-game test'}
 (DOC/'COLDWAR_KOR_delivery_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
 if errors:raise SystemExit(1)

if __name__=='__main__':main()
