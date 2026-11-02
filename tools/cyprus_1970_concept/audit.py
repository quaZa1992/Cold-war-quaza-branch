# IMPERIA COLD WAR — Independent compact Cyprus concept consistency audit.
"""Read generated review data, not authoring globals. No loaded-game writes."""
from pathlib import Path
from itertools import product
from collections import defaultdict
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/cyprus_1970_rework_20261027'
D=json.loads((OUT/'concept.json').read_text('utf-8'))
F={f['key']:f for f in D['focuses']}
assert len(F)==100
seen=set()
for f in F.values():
 assert f['anchor'] is None or f['anchor']in seen
 seen.add(f['id'])
 assert not re.search(r'unlock\s*decision|dossier', '\n'.join(f['preview_effects']),re.I)
 for e in f['effects']:
  if e['type']=='building':
   assert e['levels']==e['shared_slots']
   assert all(e['guards'].get(k)for k in('owner','controller','native_capacity','native_building_cap','one_time_receipt','slot_before_building'))
 for other in f['exclusive']:assert f['key']in F[other]['exclusive']
assert D['reconciliation'].startswith('Monthly')
assert next(e for e in F['emergency']['effects']if e['type']=='crisis_value')['amount']==25
assert F['reserve_service']['title']=='Reserve Standards'
for actor in D['actor_focuses']:
 for parent in actor['pre']:assert any(f['key']==parent and f['tag']==actor['tag']for f in D['actor_focuses'])
 for other in actor['exclusive']:assert actor['key']in next(f for f in D['actor_focuses']if f['key']==other)['exclusive']

# Audit the requested exception and its disclosed arithmetic from emitted data.
I=D['intervention'];assert I['intervention_buff']['days']==180 and I['angry_army']['days']==180
assert len(D['crisis_decisions'])==4 and all(d['country']=='TUR'and d['once']for d in D['crisis_decisions'])
decisions={d['key']:d for d in D['crisis_decisions']}
unaddressed=I['military_pressure_initial']+I['memorandum_pressure_delta']
controlled=unaddressed+decisions['rotate']['pressure_delta']+decisions['mandate']['pressure_delta']
assert unaddressed>=I['successful_coup_pressure_min']
assert controlled<=I['civilian_control_pressure_max']
assert I['nato']['end_requires_peace_pairs']==[['GRE','TUR'],['CYP','TUR']]
assert I['nato']['snapshot_before_either_exit']and I['nato']['restore_only_prior_members']
assert not I['nato']['all_world_peace_required']
assert I['nato']['entry_effect']=='add_to_war = { targeted_alliance = CYP enemy = TUR }'
actors={a['key']:a for a in D['actor_focuses']}
assert actors['gre_escalate']['transaction']['leave_before_add_to_war']
assert actors['gre_volunteers']['transaction']['no_free_divisions']
assert actors['tur_operation']['transaction']['weekly_gdp_fraction']==.00005
assert actors['tur_operation']['transaction']['one_time_per_crisis']
nodes={n['key']:n for n in D['crisis']};assert len(nodes)==len(D['crisis'])
assert set(k for layer in D['crisis_layers']for k in layer)==set(nodes)
for n in nodes.values():assert set(n['next'])<=set(nodes)
assert not nodes['civilian_control']['next']

# Enumerate complete compatible political routes. This is an upper envelope, not a native economic simulation.
envelopes={}
for party in('centre','liberal','akel'):
 allowed={k:f for k,f in F.items()if f['group']not in('centre','liberal','akel')or f['group']==party}
 pairs=sorted({tuple(sorted((k,x)))for k,f in allowed.items()for x in f['exclusive']if x in allowed})
 maxima=defaultdict(lambda:-1e9); minima=defaultdict(lambda:1e9); max_weekly=0
 for picks in product((0,1),repeat=len(pairs)):
  excluded={pair[pick]for pair,pick in zip(pairs,picks)}
  reached=set()
  for _ in range(len(allowed)):
   additions={k for k,f in allowed.items()if k not in reached|excluded and all(set(g)&reached for g in f['prerequisites'])}
   if not additions:break
   reached|=additions
  sums=defaultdict(float);weekly=0
  for k in reached:
   f=allowed[k];weekly+=f['weekly_gdp_percent']
   for e in f['effects']:
    if e['type']=='modifier_delta':
     for name,v in e['values'].items():sums[name]+=v
  # Independently consented foreign terms are all potentially compatible.
  for key,o in D['offers'].items():
   offer_focus=next(f for f in F.values()if any(e['type']=='offer'and e['key']==key for e in f['effects']))
   if offer_focus['key']in reached:
    for name,v in o['sides']['CYP']['values'].items():sums[name]+=v
    weekly+=o['weekly'].get('CYP',0)
  for name in sums:maxima[name]=max(maxima[name],sums[name]);minima[name]=min(minima[name],sums[name])
  max_weekly=max(max_weekly,weekly)
 envelopes[party]={'maximum_signed_modifier_deltas':dict(maxima),'minimum_signed_modifier_deltas':dict(minima),
  'max_new_weekly_expense_percent_of_GDP':round(max_weekly,6),
  'annual_equivalent_percent_of_GDP':round(max_weekly*52,4)}

manifest=json.loads((OUT/'source_manifest.json').read_text('utf-8'))
unchanged={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==value for rel,value in manifest['sources'].items()}
assert all(unchanged.values()),unchanged
report={'project':'IMPERIA COLD WAR','checks':'passed','focuses':100,'actor_focuses':len(D['actor_focuses']),
 'monthly_reconciliation':True,'native_decision_unlocks':0,'loaded_baseline_files_unchanged':unchanged,
 'turkey_only_finite_crisis_decisions':4,'pressure_unaddressed_day60':unaddressed,'pressure_after_two_measures_day30':controlled,
 'nato_pairwise_peace_required':I['nato']['end_requires_peace_pairs'],'volunteer_engine_eligibility_tested':False,
 'route_envelopes':envelopes,'limitations':'Independent modifier maxima may belong to different compatible routes. Starting spirits, caps, native faction modifiers and temporary aftermath are not all included. No native performance/tooltip/MP claim.'}
(OUT/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':'passed','max_stability_delta_by_party':{k:round(v['maximum_signed_modifier_deltas'].get('stability_factor',0),4)for k,v in envelopes.items()},'max_weekly_expense_GDP_percent':{k:v['max_new_weekly_expense_percent_of_GDP']for k,v in envelopes.items()},'loaded_baseline_unchanged':all(unchanged.values())}))
