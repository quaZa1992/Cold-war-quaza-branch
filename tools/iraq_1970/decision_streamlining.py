# IMPERIA CW — Cold War: focus-owned reforms and essential multiplayer decisions.
"""Pure design/output transforms. Installation is explicitly scoped by apply_streamlining.py."""
from pathlib import Path
from copy import deepcopy
import json,re
from common import P,block,parse,emit,first,values,walk,flag,check,invoice,pay_var,group_gate,locline

HERE=Path(__file__).resolve().parent
VERSION=P+'focus_owned_reforms_v1'
KEYS={
 'arab_leadership','icp_leadership_vote','dawa_leadership','iip_congress','baath_succession','kdp_succession_vote',
 'icp_preaccession','aziz_exit_front','civic_election','industry_repay','oil_contract_review','iran_supplier',
 'iran_opening','iran_followup','iran_disarray','iran_revoke_settlement','iran_policy_review',
 'war_authorization','war_mediation','war_sanctions_diplomacy',
 'organize_western','organize_emerging','organize_nonaligned','organize_nationalist',
}
AUTO={
 'march_offer','north_fiscal_settlement','icp_federal_talks','puk_federal_convention','kdp_kirkuk_talks',
 'bakr_syria_offer','arab_development_offer','arab_support_offer','arab_union_offer','icp_soviet_exchange',
 'civic_credit_offer','foreign_shatt_offer','dawa_iran_offer','sciri_border_offer','sciri_aid_offer',
 'oil_concession_offer','industry_credit','defence_soviet_advisers','defence_diversified_offer',
}
ALIASES={'baath_succession':['baath_succession','baath_continuity_cabinet','bakr_power_settlement','bakr_retire'],
         'icp_leadership_vote':['icp_leadership_vote','aziz_renewal'],
         'industry_repay':['industry_repay','saddam_repay','foreign_credit_review']}
LOCAL={
 'review_detentions':'amnesty', 'officer_amnesty':'legalization','aziz_united_opposition':'legalization',
 'national_front':'front','icp_front_strategy':'front','officer_civic_timetable':'transition',
 'baath_monopoly':'mobilization','defence_readiness':'readiness','war_peace_dividend':'civilian_budget',
}
EXTRA_PRICES={'review_detentions':.015,'officer_amnesty':.01,'aziz_united_opposition':.01,
              'national_front':.01,'icp_front_strategy':.01,'officer_civic_timetable':.02}
PATH='common/scripted_effects/COLDWAR_IRQ_focus_owned_reforms.txt'
RETRY_ID=P+'decision_reopen_negotiations'
RETRY_EVENT='COLDWAR_IRQ_decision_events.99000'
HEADER='# IMPERIA CW — Cold War: focus-owned reforms; minimal RP actions.\n'
# IMPERIA CW — Cold War: concise cabinet language for essential RP actions.
DECISION_TEXT={
 'baath_succession':('Regional Leadership Contest','Convene the Regional Command to settle the presidency among eligible party leaders. The incumbent retains office until a successor is selected.'),
 'arab_leadership':('Convene an Arab Socialist Leadership Council','Bring the party leadership together to nominate a living, eligible executive and settle the direction of the Arab socialist programme.'),
 'icp_leadership_vote':('Elect the Party Secretariat','Convene the Communist Party congress to choose an eligible secretary and settle the leadership of its political programme.'),
 'aziz_exit_front':('Review Continued Front Participation','Review the Communist Party’s participation in the governing Front. Withdrawal ends the coalition agreement without transferring the presidency.'),
 'civic_election':('Hold a Contested Parliamentary Election','Hold a parliamentary election among the legal parties. The result determines which party forms the next government.'),
 'kdp_succession_vote':('Convene the KDP Leadership Council','Convene the Kurdish leadership to choose a living, eligible executive and agree the party’s negotiating position.'),
 'dawa_leadership':('Select a Political Executive','Select an eligible political executive to direct Dawa’s organisation and government programme.'),
 'iip_congress':('Reconstitute the IIP Leadership','Convene eligible party organisers to elect a political executive and reconstitute the Islamic Party leadership.'),
 'oil_contract_review':('Renegotiate an Export Contract','Review the terms of an existing oil contract and seek a replacement agreement. The current contract remains subject to its own terms until replaced.'),
 'industry_repay':('Repay a Foreign Credit Tranche','Repay an outstanding foreign credit from the treasury. Payment cannot exceed the recorded obligation or the funds available.'),
 'war_mediation':('Request Crisis Mediation','Ask an eligible government to mediate the current dispute. A settlement requires the parties’ agreement.'),
 'war_authorization':('Authorize a Specific War Proposal','Present the current territorial dispute to the cabinet and authorize a specific war proposal. An authorization does not itself declare war.'),
 'war_sanctions_diplomacy':('Request a Sanctions Review','Seek a review of the sanctions currently imposed on Iraq. Relief depends on the governments responsible for those measures.'),
 'iran_revoke_settlement':('Repudiate the Border Settlement','Repudiate the existing border agreement with Iran. Its reciprocal benefits end and the unresolved river dispute returns.'),
 'iran_disarray':('Exploit Iranian Disarray','Commit 1% of annual GDP to exploiting a current Iranian civil war or stability below 40%. Planning Speed: +10% for 120 days. Available once.'),
 'iran_supplier':('Negotiate a Wartime Supply Contract','Approach an eligible arms supplier for a wartime delivery. Equipment, funding and delivery depend on the supplier’s agreement and available stocks.'),
 'iran_opening':('Launch the Khuzestan Offensive','Commit 2% of annual GDP within the first 30 days of war with Iran. Choose a short offensive or a sustained campaign; both increase operational costs and impose an army personnel bill that continues after an early peace.'),
 'iran_followup':('Fund a Renewed Offensive','After at least 90 days of war and the end of the opening campaign, commit 3% of annual GDP. Attack against Iran: +5% for 60 days; Supply Consumption and Army Fuel Consumption: +12%. Army personnel costs rise for 90 days. Cooldown: 180 days.'),
 'icp_preaccession':('The Communist Question','Determine whether the Communist Party seeks legal participation in the Front or organises an independent opposition. The incumbent government retains office.'),
}
for _outlook in ['western','emerging','nonaligned','nationalist']:
 _name={'western':'Western','emerging':'Emerging','nonaligned':'Non-Aligned','nationalist':'Nationalist'}[_outlook]
 DECISION_TEXT['organize_'+_outlook]=('Organize the '+_name+' Outlook','Support an existing party of the '+_name+' outlook through a political campaign. Cost: 55 Political Power. Party Support and Outlook Support: +3 points before normalization. Cooldown: 180 days. The campaign does not change the government.')

def key(dec):return dec['id'].removeprefix(P+'decision_')
def retained(dec):return key(dec) in KEYS
def advertised(dec):
 k=key(dec)
 for canonical,aliases in ALIASES.items():
  if k in aliases:return P+'decision_'+canonical
 return dec['id'] if k in KEYS else None
def is_charter(n):
 from decisions_module import CONSTITUTION_CHOICES
 return any(n['key'] in pair for pair in CONSTITUTION_CHOICES.values())
def charter_kind(n):
 from decisions_module import CONSTITUTION_CHOICES
 for pair in CONSTITUTION_CHOICES.values():
  if n['key'] in pair:return 'executive' if n['key']==pair[0] else 'representative'

def augment_overrides(overrides):
 """One reviewed overlay; preserve v3 component ordering of unchanged rewards."""
 additions=json.loads((HERE/'reward_overhaul_streamlining.json').read_text(encoding='utf-8'))
 for k,patch in additions.items():overrides[k]={**overrides.get(k,{}),**deepcopy(patch)}
 for k,extra in EXTRA_PRICES.items():
  assert k in overrides,('Missing current focus override',k)
  overrides[k]['budget_gdp_share']=overrides[k].get('budget_gdp_share',0)+extra
 descriptions={
  'review_detentions':('A Political Amnesty','Political detention has deprived public life of experienced organisers and deepened the divide between the government and its opponents. An amnesty will release living detainees whose cases can still be resolved, restore their legal standing and establish safeguards for lawful political activity.'),
  'officer_amnesty':('Civilian Political Guarantees','The officers cannot promise an orderly republic while every organised opponent risks detention. Legal activity and enforceable safeguards will give civilian parties room to prepare for public responsibility without handing them command of the state.'),
  'officer_civic_timetable':('Ratify the Civilian Transition','A published timetable must give way to binding electoral rules. Ratification will permit contested elections and protect lawful political activity, leaving the choice of the next government to the existing electoral institutions.'),
  'puk_regional_cooperation':('A Kurdish Liaison Council','Local representatives need a common Iraqi forum for public services and regional administration. A liaison council can coordinate their work within the republic without merging parties or claiming authority over a separate Kurdish government.'),
  'puk_joint_services':('Regional Services Board','Shared procurement and professional administration can make provincial services more dependable. The board will coordinate Iraqi institutions and spending in the regions under our own authority.'),
 }
 for k,(title,description) in descriptions.items():
  assert k in overrides,k
  overrides[k].update(title=title,description=description)

def apply_design(data):
 if data.get('decision_streamlining_revision')==VERSION:return data
 by={n['id']:n for n in data['nodes']}
 for n in data['nodes']:
  if n['key']=='puk_joint_services':
   for field in ['requires','active_requires']:
    if field in n:n[field]=[r for r in n[field] if r!='Accepted KDP-PUK cooperation pact']
 # Preserve exact original provider authority for consolidated native leaders/accounts.
 decs={key(d):d for d in data['decisions']}
 authority={}
 for canonical,oldkeys in ALIASES.items():
  clauses=[]
  for old in oldkeys:
   d=decs[old];gate=group_gate(d['group'])
   providers=d.get('audit_providers',[d['unlock']])
   if d['unlock']!='START':gate+='\nhas_country_flag = '+d['id']+'_unlocked\n'+block('OR','\n'.join(flag(p+'_implemented') for p in providers))
   clauses.append(gate)
  authority[canonical]=block('OR','\n'.join(block('AND',c) for c in clauses))
 for d in data['decisions']:
  d['focus_owned_mode']='retained' if retained(d) else ('automatic_offer' if key(d) in AUTO else 'removed')
  if key(d) in DECISION_TEXT:d['label'],d['summary']=DECISION_TEXT[key(d)]
 for n in data['nodes']:
  n['focus_owned_actions']=[key(d) for d in n['decisions'] if key(d) in AUTO]
  baseline=json.loads((HERE/'decision_streamlining_baseline.json').read_text(encoding='utf-8'))
  n['streamline_previous_modifiers']=deepcopy(baseline['modifiers'][n['key']])
  # Keep the pre-existing v2 -> v3 bill separate from this revision's bill.
  if n.get('overhaul_changed'):
   n['overhaul_price_increment']=max(0,baseline['shares'][n['key']]-n['overhaul_previous_share'])
 # A joint-service board is Iraqi administration, not a fictional foreign acceptance.
 n=by[P+'puk_regional_cooperation'];n['modifiers']={'offices_productivity':.06,'social_cost_multiplier_modifier':.02}
 data['focus_owned_authority']=authority
 data['decision_streamlining_revision']=VERSION
 return data

def authority(data,k):return data.get('focus_owned_authority',{}).get(k)
def hook_name(n):return P+'focus_owned_'+n['key']
def receipt(n):return P+'focus_owned_'+n['key']+'_delivered'
def has_hook(n):return bool(n.get('focus_owned_actions') or n['key'] in LOCAL or is_charter(n))
def revised(n):return has_hook(n) or n['key'] in json.loads((HERE/'reward_overhaul_streamlining.json').read_text(encoding='utf-8')) or n['key']=='puk_regional_cooperation'
def hook_call(n):return hook_name(n)+' = yes' if revised(n) else ''
def offer_text(k):return P+'focus_owned_offer_'+k+'_tt'

def preview(n):
 rows=[]
 for k in n.get('focus_owned_actions',[]):rows.append('custom_effect_tooltip = '+offer_text(k))
 kind=charter_kind(n)
 if kind:rows.append('custom_effect_tooltip = '+P+'focus_owned_'+kind+'_tt')
 mode=LOCAL.get(n['key'])
 if mode in ['amnesty','legalization','front','transition']:rows.append('custom_effect_tooltip = '+P+'focus_owned_'+mode+'_tt')
 if mode in ['amnesty','legalization','front','transition']:rows.append('effect_tooltip = { add_ideas = COLDWAR_IRQ_civil_rights_cost }')
 if mode=='mobilization':rows.append('effect_tooltip = { add_command_power = 25 }')
 if mode=='readiness':rows.append('effect_tooltip = { add_timed_idea = { idea = COLDWAR_IRQ_readiness_cycle days = 90 } }')
 if mode=='civilian_budget':rows.append('custom_effect_tooltip = '+P+'focus_owned_civilian_budget_tt')
 return '\n'.join(rows)+'\n' if rows else ''

def local_payload(mode):
 legal='''set_country_flag = COLDWAR_IRQ_legalization_accepted
set_temp_variable = { party_index = 4 }
unban_party_scripted_call = yes
add_ideas = COLDWAR_IRQ_civil_rights_cost
if = { limit = { date < 1971.11.28 NOT = { has_country_flag = COLDWAR_IRQ_rikabi_dead } } set_country_flag = COLDWAR_IRQ_rikabi_rehabilitated }
if = { limit = { date < 1971.1.1 NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } } set_country_flag = COLDWAR_IRQ_dawa_cadres_protected }'''
 if mode=='amnesty':
  from prison_review import CASES,case_gate
  cases='\n'.join(block('if',block('limit',case_gate(*case))+'set_country_flag = '+P+case[2]+ ('\nclr_country_flag = COLDWAR_IRQ_dukhayl_unavailable' if case[2]=='dukhayl_released' else '')) for case in CASES)
  return legal+'\n'+cases
 if mode=='legalization':return legal
 if mode=='front':return legal+'''\nset_country_flag = COLDWAR_IRQ_front_accepted
set_country_flag = COLDWAR_IRQ_icp_strategy_front
clr_country_flag = COLDWAR_IRQ_icp_strategy_independent
remove_ideas = COLDWAR_IRQ_party_mobilization
if = { limit = { check_variable = { ruling_party = 21 } NOT = { is_in_array = { array = gov_coalition_array value = 4 } } } add_to_array = { gov_coalition_array = 4 } }
if = { limit = { check_variable = { ruling_party = 4 } NOT = { is_in_array = { array = gov_coalition_array value = 21 } } } add_to_array = { gov_coalition_array = 21 } }
update_government_coalition_strength = yes'''
 if mode=='transition':return legal+'\nset_country_flag = COLDWAR_IRQ_transition_accepted\nset_politics = { elections_allowed = yes }'
 if mode=='mobilization':return 'COLDWAR_IRQ_leave_front = yes\nadd_command_power = 25'
 if mode=='readiness':return 'add_timed_idea = { idea = COLDWAR_IRQ_readiness_cycle days = 90 }'
 if mode=='civilian_budget':return 'set_country_flag = COLDWAR_IRQ_emergency_ended'
 return ''

def _all_events(text):return {first(b,'id'):b for b in values(parse(text),'country_event')}
def _first_event(rows):return next((first(v,'id') for k,o,v in walk(rows) if k=='country_event' and isinstance(v,list)),None)
def _runtime_refs(rows,effects,event_ids):
 ef={k for k,o,v in walk(rows) if k in effects and v=='yes'}
 ev={first(v,'id') for k,o,v in walk(rows) if k=='country_event' and isinstance(v,list) and first(v,'id') in event_ids}
 return ef,ev

def transform(outputs,data,eligible,capacity,original_shares,conditions):
 """Transform in-memory generated content; retain only reachable general menus."""
 import reward_overhaul
 result=dict(outputs);loc={}
 def L(k,v):loc[k]=v
 def out(path,rows):result[path]=HEADER+emit(rows)+'\n'
 decision_path='common/decisions/COLDWAR_IRQ_1970_decisions.txt'
 effects_path='common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt'
 events_path='events/COLDWAR_IRQ_1970_decisions.txt'
 ast=parse(result[decision_path]);category=first(ast,P+'1970_decisions')
 definitions={k:b for k,o,b in category}
 effects_ast=parse(result[effects_path]);effects={k:b for k,o,b in effects_ast if isinstance(b,list)}
 events=_all_events(result[events_path]);generated=[];nby={n['id']:n for n in data['nodes']}
 # The sender's quote executes even when its one-target selection menu is omitted.
 for k in sorted(AUTO):
  helper=P+'do_'+k;body=effects[helper];eid=_first_event(body)
  if not eid or eid not in events:continue
  ev=events[eid];opts=[o for o in values(ev,'option') if any(j=='country_event' for j,_,_ in walk(o))]
  # Domestic autonomy and fiscal conventions retain their actual local choices.
  if len(opts)==1 and k not in ['march_offer','north_fiscal_settlement','icp_federal_talks','puk_federal_convention','kdp_kirkuk_talks']:
   actions=[r for r in opts[0] if r[0] not in ['name','trigger','ai_chance']]
   replacement=first(ev,'immediate',[])+[('if','=',[('limit','=',first(opts[0],'trigger',[]))]+actions)]
   def inline(rows):
    return [r for k2,o2,v2 in rows for r in (replacement if k2=='country_event' and isinstance(v2,list) and first(v2,'id')==eid else [(k2,o2,inline(v2) if isinstance(v2,list) else v2)])]
   effects[helper]=inline(body)
 # A manual RP dossier is still needed BEFORE its guarded assessment focus.
 dossier=definitions[P+'decision_iran_policy_review']
 dossier_gate='COLDWAR_IRQ_campaign_active = yes\n'+group_gate('saddam')+'\nhas_country_flag = COLDWAR_IRQ_saddam_regional_role_implemented\nNOT = { has_country_flag = COLDWAR_IRQ_iran_rp_dossier }'
 for i,(k,o,v) in enumerate(dossier):
  if k in ['visible','available']:dossier[i]=(k,o,parse(dossier_gate))
  elif k=='complete_effect':dossier[i]=(k,o,parse('set_country_flag = COLDWAR_IRQ_iran_rp_dossier\nadd_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 60 }'))
 L(P+'decision_iran_policy_review','Publish the Iranian Policy Dossier')
 L(P+'decision_iran_policy_review_desc','Publish the presidency’s assessment of Iran as the basis for a deliberate frontier policy. Publication does not grant a claim, a war goal or an automatic declaration of war.')
 # Focus delivery commits the local reform; foreign callbacks retain their own consent.
 for n in data['nodes']:
  if n.get('audit_retired') or not revised(n):continue
  payload=[]
  kind=charter_kind(n)
  if kind:payload.append(P+'adopt_constitution_'+kind+' = yes')
  if n['key'] in LOCAL:payload.append(local_payload(LOCAL[n['key']]))
  for k in n.get('focus_owned_actions',[]):payload.append(P+'do_'+k+' = yes')
  guard='COLDWAR_IRQ_campaign_active = yes\n'+group_gate(n['group'])+'\nhas_country_flag = '+n['id']+'_implemented\nNOT = { '+flag(receipt(n))+' }'
  generated.append(parse(block(hook_name(n),block('if',block('limit',guard)+'set_country_flag = '+receipt(n)+'\n'+'\n'.join(payload))))[0])
 # Failed/expired one-time negotiations remain repeatable through one shared channel.
 retry_options=[];retry_gates=[]
 for k in sorted(AUTO):
  d=definitions[P+'decision_'+k];gate=first(d,'available',[])
  retry_gates.append(('AND','=',gate))
  retry_options.append(('option','=',[('name','=',P+'focus_owned_retry_'+k)]+[('trigger','=',gate)]+parse(P+'do_'+k+' = yes')))
  label=next(d['label'] for d in data['decisions'] if key(d)==k);L(P+'focus_owned_retry_'+k,label)
  L(offer_text(k),'Opens negotiations: '+label+'. The other government retains its decision where applicable.')
 gate=[('COLDWAR_IRQ_campaign_active','=','yes'),('OR','=',retry_gates)]
 retry=[('icon','=','generic_political_discourse'),('cost','=','0'),('visible','=',gate),('available','=',gate),('complete_effect','=',[('country_event','=',[('id','=',RETRY_EVENT)])]),('ai_will_do','=',[('factor','=','0')])]
 category[:]=[(k,o,v) for k,o,v in category if k.removeprefix(P+'decision_') in KEYS]
 category.append((RETRY_ID,'=',retry))
 events[RETRY_EVENT]=[('id','=',RETRY_EVENT),('title','=',RETRY_EVENT+'.t'),('desc','=',RETRY_EVENT+'.d'),('is_triggered_only','=','yes'),('trigger','=',[('COLDWAR_IRQ_campaign_active','=','yes')])]+retry_options+[('option','=',[('name','=',P+'focus_owned_close')])]
 L(RETRY_ID,'Reopen Diplomatic Negotiations');L(RETRY_ID+'_desc','Return to an unresolved negotiation after refusal, delay or a change of circumstances. Agreements still require their own funding and the recipient’s consent. No political fee is charged for opening this channel.')
 L(RETRY_EVENT+'.t','Outstanding Negotiations');L(RETRY_EVENT+'.d','The cabinet may return to a proposal whose terms remain relevant. Foreign governments retain control of their response and no agreement takes effect merely by reopening talks.')
 L(P+'focus_owned_close','Close the consultations.')
 out(decision_path,ast)
 # Scope first: remove only two redundant US sender menus; actual actions stay.
 us='common/decisions/COLDWAR_USA_gulf_decisions.txt'
 ua=parse(result.get(us,''))
 for k,o,b in ua:
  if isinstance(b,list):b[:]=[r for r in b if r[0] not in ['COLDWAR_USA_gulf_respond','COLDWAR_USA_gulf_uprising_aftermath']]
 if ua:out(us,ua)
 # Free status popup is redundant beside the actual pending-delivery list.
 pp='common/decisions/COLDWAR_IRQ_1970_pending.txt';pa=parse(result[pp])
 for k,o,b in pa:
  if isinstance(b,list):b[:]=[r for r in b if r[0]!=P+'decision_retry_pending']
 out(pp,pa)
 result['events/COLDWAR_IRQ_1970_projects.txt']=HEADER+'# Project rewards are inspected on their individual pending deliveries.\n'
 # Legacy saves receive guarded upgrades rather than replaying focus awards on refresh.
 upgrades=[];migration=['remove_ideas = COLDWAR_IRQ_front_labour_charter','remove_ideas = COLDWAR_IRQ_party_mobilization','COLDWAR_IRQ_cancel_prison_review = yes']
 modified=json.loads((HERE/'reward_overhaul_streamlining.json').read_text(encoding='utf-8'))
 candidates=[n for n in data['nodes'] if not n.get('audit_retired') and revised(n)]
 for n in candidates:
  pending=P+'focus_owned_'+n['key']+'_pending';action=P+'upgrade_focus_owned_'+n['key'];q=P+'focus_owned_'+n['key']+'_upgrade'
  delta=max(0,n['budget_gdp_share']-original_shares[n['key']])
  # Existing v3 projects awaiting payment keep their original GDP basis while
  # adopting the full revised price. Older revisions reprice in their own path.
  oldshare=original_shares[n['key']]
  if delta and oldshare:
   reprice=flag(reward_overhaul.VERSION)+'\nNOT = { '+flag(n['id']+'_implemented')+' }\n'+flag(n['id']+'_quoted')+'\n'+check(n['id']+'_invoice',0,'greater_than')
   migration.append(block('if',block('limit',reprice)+f'multiply_variable = {{ {n["id"]}_invoice = {(n["budget_gdp_share"]/oldshare):g} }}'))
  gate=eligible(n,False)+'\n'+capacity(n)+'\nhas_country_flag = '+n['id']+'_implemented\nhas_country_flag = '+n['id']+'_reward_v3_current'
  quote=invoice(q,delta) if delta else ''
  cash=(flag(q+'_quoted')+'\n'+check('treasury',q+'_invoice')+'\nNOT = { has_country_flag = MD_skip_treasury_cost }') if delta else ''
  payload=(pay_var(q+'_invoice')+'\n' if delta else '')
  if n.get('overhaul_changed'):payload+=reward_overhaul.delivery(n)+'\n'
  payload+=hook_call(n)+'\nclr_country_flag = '+pending
  generated.append(parse(block(action,block('if',block('limit',flag(pending)) +quote+block('if',block('limit',gate+'\n'+cash)+payload))))[0])
  dec=P+'focus_owned_'+n['key']+'_upgrade_delivery'
  import presentation
  shown=presentation.available_ui(n,gate+'\n'+cash,conditions,hide_prerequisites=True)
  shown_reward=preview(n)+block('effect_tooltip',(pay_var(q+'_invoice') if delta else '')+'\n'+(reward_overhaul.delivery(n) if n.get('overhaul_changed') else ''))
  upgrades.append((dec,'=',parse('icon = generic_construction\ncost = 0\n'+block('visible','COLDWAR_IRQ_campaign_active = yes\n'+flag(pending))+block('available',shown)+block('complete_effect',shown_reward+block('hidden_effect',action+' = yes')))))
  # Credit domestic settlements already enacted by the old paid events.
  credit='';mode=LOCAL.get(n['key'])
  prior={'legalization':P+'legalization_accepted','front':P+'front_accepted','transition':P+'transition_accepted'}
  if delta and mode in prior:
   credit=block('if',block('limit',flag(prior[mode]))+f'set_variable = {{ {q}_invoice = 0 }}')
  if delta and mode=='amnesty':
   credit=block('if',block('limit',flag(P+'legalization_accepted'))+f'multiply_variable = {{ {q}_invoice = {(.005/delta):g} }}')
   settled=block('OR','\n'.join(flag(P+k) for k in ['dukhayl_released','rikabi_rehabilitated','dawa_cadres_protected']))
   credit+=block('if',block('limit',settled)+block('if',block('limit',flag(P+'legalization_accepted'))+f'set_variable = {{ {q}_invoice = 0 }}')+block('else',f'multiply_variable = {{ {q}_invoice = {(.01/delta):g} }}'))
  migration.append(block('if',block('limit',flag(n['id']+'_implemented')+'\nNOT = { '+flag(receipt(n))+' }')+quote+credit+'set_country_flag = '+pending))
  L(dec,'Implement '+n['title']);L(dec+'_desc','Complete the revised programme once. Outstanding appropriation: $[?'+q+'_invoice|2] billion. Previously funded commitments and delivered investments are credited.')
 for n in data['nodes']:
  if not n['mutually_exclusive'] or n.get('audit_retired'):continue
  migration.append(block('if',block('limit','has_completed_focus = '+n['id']+'\n'+flag(n['id']+'_implemented'))+'set_country_flag = '+P+'policy_'+n['group']+'_'+n['key']+'\n'+'\n'.join('clr_country_flag = '+P+'policy_'+n['group']+'_'+nby[j]['key'] for j in n['mutually_exclusive'])))
 generated.append(parse(block(P+'migrate_focus_owned_reforms',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes\nNOT = { '+flag(VERSION)+' }')+'set_country_flag = '+VERSION+'\n'+'\n'.join(migration))))[0])
 for k,o,b in pa:
  if isinstance(b,list):b.extend(upgrades)
 out(pp,pa)
 pending_category='common/decisions/categories/COLDWAR_IRQ_1970_pending.txt'
 pc=parse(result[pending_category]);v=first(pc,P+'pending_projects');pflags=first(first(v,'visible',[]),'OR',[])
 for n in candidates:pflags.append(('has_country_flag','=',P+'focus_owned_'+n['key']+'_pending'))
 out(pending_category,pc)
 # Synchronisation initializes compatibility receipts, never replays a new delivery.
 prog='common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt';pr=parse(result[prog]);reconcile=first(pr,P+'reconcile_programmes')
 first(reconcile,'if').insert(1,(P+'migrate_focus_owned_reforms','=','yes'))
 out(prog,pr)
 v3path='common/scripted_effects/COLDWAR_IRQ_1970_direct_rewards_v3.txt'
 v3=parse(result[v3path]);first(v3,P+'migrate_direct_rewards_v3').insert(0,(P+'migrate_focus_owned_reforms','=','yes'));out(v3path,v3)
 out(PATH,generated)
 # Follow actual external roots before pruning unused generic dispatchers/events.
 effects.update({k:b for k,o,b in generated})
 roots=[]
 for path,text in result.items():
  if path in [effects_path,events_path,PATH] or not path.endswith(('.txt','.gui')):continue
  roots+=parse(text)
 # Narrow native adapters can call general political/leader effects.
 root=HERE.parents[1]
 for folder in ['common/scripted_effects','common/scripted_triggers','common/on_actions','events']:
  for p in (root/folder).glob('*.txt'):
   rel=str(p.relative_to(root)).replace('\\','/')
   if rel in result or not ('COLDWAR_IRQ' in p.name or 'COLDWAR_USA_gulf' in p.name or p.name=='IRQ_political_leaders.txt'):continue
   roots+=parse(p.read_text(encoding='utf-8-sig'))
 keep_e,keep_v=_runtime_refs(roots,effects,set(events));todo_e=list(keep_e);todo_v=list(keep_v)
 while todo_e or todo_v:
  rows=effects[todo_e.pop()] if todo_e else events[todo_v.pop()]
  ef,ev=_runtime_refs(rows,effects,set(events))
  todo_e+=list(ef-keep_e);todo_v+=list(ev-keep_v);keep_e|=ef;keep_v|=ev
 out(effects_path,[(k,o,effects[k]) for k,o,v in effects_ast if k in keep_e])
 out(events_path,[('add_namespace','=','COLDWAR_IRQ_decision_events')]+[('country_event','=',v) for k,v in events.items() if k in keep_v])
 L(P+'focus_owned_executive_tt','Establishes executive constitutional authority for the government programme.')
 L(P+'focus_owned_representative_tt','Establishes representative constitutional authority for the government programme.')
 L(P+'focus_owned_amnesty_tt','Releases eligible living detainees and restores their political standing before the applicable case deadlines. Legal political guarantees take effect.')
 L(P+'focus_owned_legalization_tt','Legalises Communist political activity and enacts political guarantees.')
 L(P+'focus_owned_front_tt','Enacts the Baath–Communist Front charter, legalises Communist activity and forms the domestic coalition. The leading party retains government.')
 L(P+'focus_owned_transition_tt','Ratifies the civilian transition and permits contested elections.')
 L(P+'focus_owned_civilian_budget_tt','Ends the active emergency budget. Previously committed personnel bills remain payable until expiry.')
 # Existing removed menu/option localisation is harmless, but do not advertise deleted actions.
 result['localisation/english/COLDWAR_IRQ_focus_owned_reforms_l_english.yml']='l_english:\n'+HEADER+'\n'.join(locline(k,v) for k,v in loc.items())+'\n'
 return result,{'general_decisions_before':len(definitions),'general_decisions_after':len(category),'events_before':len(_all_events(outputs[events_path])),'events_after':len(keep_v),'retained_events':sorted(keep_v),'retained_effects':sorted(keep_e),'automatic_offers':sorted(AUTO),'legacy_upgrade_actions':len(upgrades)}
