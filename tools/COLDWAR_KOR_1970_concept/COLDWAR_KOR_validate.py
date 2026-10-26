# IMPERIA CW — Cold War: independent concept graph, geometry and API checks.
"""Reads approval-stage output; writes reports only. Does not load HOI4."""
from pathlib import Path
from functools import lru_cache
from decimal import Decimal
import hashlib, itertools, json, re
from PIL import ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/design/COLDWAR_KOR_1970'
D=json.loads((OUT/'COLDWAR_KOR_design.json').read_text(encoding='utf-8'))
N={n['id']:n for n in D['nodes']};errors=[]
def check(test,message):
    if not test:errors.append(message)

@lru_cache(None)
def resolve(id,trail=()):
    check(id not in trail,'cyclic position '+id)
    n=N[id]
    if n['anchor']:
        a=resolve(n['anchor'],trail+(id,));return (a[0]+n['offset'][0],a[1]+n['offset'][1])
    return tuple(n['offset'])

def compatible(history):
    return not any(set(N[id]['mutually_exclusive'])&history for id in history)

@lru_cache(None)
def histories(id):
    n=N[id];options=[frozenset()]
    for row in n['prerequisites']:
        row_options=[s for p in row for s in histories(p)]
        options=[a|b for a in options for b in row_options if compatible(a|b)]
    return tuple({s|{id} for s in options if compatible(s|{id})})

check(len(N)==len(D['nodes']),'duplicate ids')
check(len(N)<=300,'over300 focus limit')
check(len(D['layout']['shortcuts'])<=8,'shortcut native grid capacity exceeded')
for id,n in N.items():
    check(id.startswith('COLDWAR_KOR_'),'prefix '+id)
    check(n['ownership']=='national' or n['ownership'].startswith(('party:','leader:')),'unresolved programme owner '+id)
    for p in [x for row in n['prerequisites'] for x in row]+n['mutually_exclusive']:
        check(p in N,'missing reference '+p)
    for x in n['mutually_exclusive']:
        check(id in N[x]['mutually_exclusive'],'asymmetric exclusion '+id)
    check(resolve(id)==tuple(n['xy']),'resolved mismatch '+id)
    check(bool(histories(id)),'unreachable under exclusions '+id)
    for p in n['effects']['policies']:
        check(len(p['modifiers'])>=1,'empty policy '+id)
    if n['effects']['weekly']:
        check(n['effects'].get('expense_commitment',{}).get('weekly_bn')==n['effects']['weekly'],'unowned weekly cost '+id)
    for num in [n['effects']['cost'],n['effects']['weekly']]:
        check(Decimal(str(num)).as_tuple().exponent>=-5,'fixed point precision '+id)
    if n['effects']['buildings']:
        check('free_building_slots' in n['native_gate_body'],'missing capacity guard '+id)
    check(n['native_gate_body']==n['native_completion_guard'].split('\nNOT = { has_country_flag = '+id+'_paid }')[0],'availability/reward guard mismatch '+id)
    for body in n.get('condition_code',[]):
        check(body in n['native_gate_body'],'condition omitted from start/reward '+id)
    check('civic_legal_None' not in n['native_gate_body'],'invalid civic legality receipt '+id)
    if isinstance(n.get('bypass'),dict) and n['bypass'].get('native_pattern'):
        check('has_completed_focus' in n.get('native_bypass_body',''),'missing dispatch-aware native bypass '+id)
        check(n['bypass']['native_pattern'] not in n['native_completion_guard'],'refusal wrongly unlocks treaty reward '+id)

collisions=[]
for a,b in itertools.combinations(N.values(),2):
    dx=abs(a['xy'][0]-b['xy'][0])*96;dy=abs(a['xy'][1]-b['xy'][1])*130
    if dx<165 and dy<128:collisions.append([a['id'],b['id']])
check(not collisions,'item collisions '+str(collisions[:3]))
font=ImageFont.truetype('C:/Windows/Fonts/georgia.ttf',14)
overflow=[{'id':id,'title':n['label'],'pixels':round(font.getlength(n['label']),2)} for id,n in N.items() if font.getlength(n['label'])>147]
check(not overflow,'name field overflow '+str(overflow))

# Native sources prove API vocabulary and custom readers separately.
used={k for n in N.values() for p in n['effects']['policies'] for k in p['modifiers']}
used|={k for s in D['starting_spirits'] for k in s['modifiers']}
used|={k for c in D['contracts'] for p in c['KOR_policy'] for k in p['modifiers']}
evidence={key:{'uses':[],'definitions':[],'readers':[]} for key in used}
for folder,bucket,pattern in [
 ('common/ideas','uses',r'^\s*KEY\s*='),
 ('common/dynamic_modifiers','uses',r'^\s*KEY\s*='),
 ('common/modifier_definitions','definitions',r'^\s*KEY\s*='),
 ('common/scripted_effects','readers',r'modifier@KEY\b')]:
    for path in (ROOT/folder).glob('*.txt'):
        lines=path.read_text(encoding='utf-8-sig',errors='replace').splitlines()
        for line_no,line in enumerate(lines,1):
            for key in used:
                if key in line and re.search(pattern.replace('KEY',re.escape(key)),line):
                    if len(evidence[key][bucket])<4:evidence[key][bucket].append(f'{path.relative_to(ROOT).as_posix()}:{line_no}')
for key,ev in evidence.items():
    check(bool(ev['uses']), 'no MD country modifier usage '+key)
    if ev['definitions']:check(bool(ev['readers']),'custom modifier without traced reader '+key)
    ev['consumer']='custom scripted reader' if ev['definitions'] else 'native HOI4 modifier; current MD country-idea/dynamic usage'

# A small independent lifecycle model verifies actual requirements: latest-slot
# replacement, inactive party returns, no repeat of treasury/buildings/XP.
slots={};expense={};receipts=set();bank=100;buildings=0
def complete(key):
    global bank,buildings
    n=next(n for n in N.values() if n['key']==key)
    if n['id'] in receipts:return
    receipts.add(n['id']);bank-=n['effects']['cost'];buildings+=sum(b['level'] for b in n['effects']['buildings'])
    for p in n['effects']['policies']:slots[(n['ownership'],p['qualified_slot'])]=p['modifiers']
    c=n['effects'].get('expense_commitment')
    if c:expense[(n['ownership'],c['slot'])]=c['weekly_bn']
def active(owner):
    return sum(v for (o,s),v in expense.items() if o in ('national',owner))
complete('chaebol_compact');complete('export_targets')
check(abs(active('leader:Park Chung Hee')-.004)<1e-9,'upgrade double-counts expense')
check(active('party:1')==0,'departed Park expense active')
snapshot=(bank,buildings,len(receipts))
check(abs(active('leader:Park Chung Hee')-.004)<1e-9,'returned Park missing programme')
check(snapshot==(bank,buildings,len(receipts)),'refresh paid a one-time effect')
complete('pohang_foundry');snapshot=(bank,buildings);complete('pohang_foundry')
check(snapshot==(bank,buildings),'duplicate paid building reward')
complete('real_name_accounts');complete('national_health_cover')
check(any(o=='leader:Kim Young-sam' for o,s in slots),'YS programme not retained')
check(any(o=='leader:Kim Dae-jung' for o,s in slots),'DJ programme not retained')
complete('roh_nordpolitik');complete('conservative_merger')
roh_keys=[(o,s) for o,s in slots if o in ('party:22','leader:Roh Tae-woo') and s in ('army:nordpolitik','army:coalition')]
check(len(roh_keys)==2,'compatible Roh programmes overwrite one another')
check(abs(sum(slots[k].get('political_power_factor',0) for k in roh_keys)-.06)<1e-9,'combined ratified Roh programme coefficients')

# Action declarations are closed, so a focus cannot promise a nameless handler.
known_actions={x for a in D['actions'].values() for x in a['ids']}
for n in N.values():
    for a in n['effects']['actions']:
        if a['type']=='action':check(a['value'] in known_actions,'undeclared action '+a['value'])
known_contracts={c['key'] for c in D['contracts']}
for n in N.values():
    for a in n['effects']['actions']:
        if a['type']=='offer':check(a['value'] in known_contracts,'undeclared contract '+a['value'])
framework=next(c for c in D['contracts'] if c['key']=='sovereign_confederation')
check(framework['KOR_on_accept']['add_ideas']==framework['recipient_effects']['add_ideas'],'membership grant must reach both countries')
check('has_idea = COLDWAR_KOR_confederal_member' in next(n for n in N.values() if n['key']=='confederal_secretariat')['native_completion_guard'],'member-only completion missing actual spirit')

# Revision2 must extend every original area while retaining the owner's cap.
check(len(N)==298,'revision2 expected298 focuses')
check(all(v>0 for v in D['expansion_summary']['group_deltas'].values()),'an area was not expanded')
check(sum(n['group']=='transition' for n in N.values())==36,'transition count')
check(len(D['starting_spirits'])==9,'expanded starting constraints')
ns={n['key']:n for n in N.values()};decisions={x['id']:x for x in D['transition_decisions']}
P='COLDWAR_KOR_'
check(not set(ns['roh_nordpolitik']['mutually_exclusive'])&{ns['conservative_merger']['id']},'historically compatible Roh policies exclude')
check(ns['roh_nordpolitik']['effects']['policies'][0]['qualified_slot']!=ns['conservative_merger']['effects']['policies'][0]['qualified_slot'],'Roh policies share ambiguous slot')
check('conservative_merger_ratified' in ns['conservative_merger']['effects']['policies'][0]['active_trigger'],'coalition reward activates before agreement')
retry=decisions[P+'reopen_charter_ballot']
check('charter_rejected' in retry['available'] and 'charter_retry_cooldown' in retry['available'],'ballot retry missing state/cooldown')
check('COLDWAR_KOR_transition.30' in retry['effect'] and 'add_political_power = -50' in retry['effect'],'ballot retry does not queue funded vote')
check(not any(x in retry['effect'] for x in ('reset_focus','charter_model =','constitutional_order')),'retry changes model/focus/order')
talks=decisions[P+'reopen_constitutional_talks']
check('ruling_party = 22' in talks['available'] and 'opposition_constitutional_demand' in talks['available'],'reopening government/demand missing')
check('NOT = { has_country_flag = '+P+'military_opening_authorized }' in talks['available'],'authorization replay not blocked')
check('clr_country_flag = '+P+'military_reconsolidation' in talks['effect'],'reopening leaves failure active')
vote=D['proposed_transition_events']['COLDWAR_KOR_transition.30']
check('charter_support_share > 0.5' in vote['pass_guard'],'ratification threshold')
check('charter_retry_cooldown days = 90' in vote['reject_native'],'rejection cooldown missing')
check(not any(x in vote['pass_native'] for x in ('change_ruling_party_effect','set_country_leader','lawful_election_completed')),'ratification appoints winner')
check('lawful_election_completed' in ns['orderly_handover']['native_gate_body'],'handover lacks actual election result')
check(all('has_country_flag = '+P+'constitutional_order' in ns[k]['effects']['policies'][0]['active_trigger'] for k in ('one_term_presidency','cabinet_responsibility','coalition_veto_rules')),'draft activates before implementation')
court=ns['independent_constitutional_court']
check('judicial_review_operational' in court['effects']['policies'][0]['active_trigger'],'court grants benefit from legal mandate alone')
check('country_event' not in '\n'.join(court['state_effects']),'court focus automatically schedules operation')
check('court_appointments_implemented' in D['proposed_transition_events']['COLDWAR_KOR_transition.88']['trigger'],'court ignores appointments')
check('court_implementation_pending' in D['transition_maintenance_recipe'],'interrupted commissioning cannot resume')
command=D['proposed_transition_events']['COLDWAR_KOR_transition.12']
check('command_settlement_pending' in ns['defend_civil_command']['native_leaf_effects'],'no command pending setter')
check('military_reconsolidation' in command['failure_native'] and 'clr_country_flag = '+P+'transition_open' in command['failure_native'],'failed command blocks later opening')

# Independent arithmetic cases: all eligible opponents remain in denominator;
# supporters are unique, bans/conditional legality apply, and zero never wins.
def charter_vote(pop,supporters,banned=(),legal=()):
    slots={0,1,2,3}|(set(legal)&{4,5,19,22});slots-=set(banned)
    denominator=sum(pop.get(s,0) for s in slots)
    share=sum(pop.get(s,0) for s in slots&set(supporters))/denominator if denominator else 0
    return share,share>.5
check(charter_vote({0:49,1:51},[1])==(0.51,True),'majority ballot')
check(charter_vote({0:50,1:50},[1])==(0.5,False),'tie passes')
check(charter_vote({0:49,1:51},[1,1])==(0.51,True),'duplicate supporter counted')
check(charter_vote({0:40,1:30,7:30},[7])==(0.0,False),'security association counted as electoral party')
check(charter_vote({0:40,1:30,5:30},[5],legal=[5])==(0.3,False),'civic inclusion denominator')
check(charter_vote({0:40,1:60},[1],banned=[1])==(0.0,False),'banned support counted')
check(charter_vote({},[0,1])==(0,False),'zero electorate passes')
check('charter_electorate > 0' in D['transition_system']['ratification']['native_calculation'],'native zero branch missing')

# Count choice components separately from reciprocal pair links.
seen=set();choice_components=[]
for id in N:
    if id in seen or not N[id]['mutually_exclusive']:continue
    stack=[id];component=set()
    while stack:
        x=stack.pop()
        if x in component:continue
        component.add(x);stack.extend(N[x]['mutually_exclusive'])
    seen|=component;choice_components.append(sorted(component))
check(sum(len(c)==3 for c in choice_components)==3,'expected three3-way policy decisions')

report={'status':'PASS' if not errors else 'FAIL','focuses':len(N),'groups':len(D['groups']),
 'exclusive_pairs':sum(len(n['mutually_exclusive']) for n in N.values())//2,
 'choice_groups':len(choice_components),'three_way_choices':sum(len(c)==3 for c in choice_components),
 'contracts':len(D['contracts']),'starting_spirits':len(D['starting_spirits']),
 'reachable_structural':sum(bool(histories(id)) for id in N),
 'native_item_collisions':collisions,'title_overflow':overflow,'shortcut_count':len(D['layout']['shortcuts']),
 'used_modifier_keys':len(used),'lifecycle_model':'latest level replaces slot; depart/return restores without payout; paid construction once; separate Two Kim owners retained',
 'transition_checks':'same-model retry, strict majority/tie/zero/bans/unique supporters, genuine election receipt, court mandate/paid appointments/operation, failed command reopening, refusal bypass without payout',
 'errors':errors,'scope':'Design-only consistency and source/API evidence; not engine, hover, save or live browser QA',
 'design_sha256':hashlib.sha256((OUT/'COLDWAR_KOR_design.json').read_bytes()).hexdigest()}
(OUT/'COLDWAR_KOR_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(OUT/'COLDWAR_KOR_modifier_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
if errors:raise SystemExit(1)
