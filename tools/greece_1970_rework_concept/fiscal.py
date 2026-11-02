# IMPERIA COLD WAR — Greece concept GDP repricing and spirit-bound fiscal streams.
from decimal import Decimal

PERMANENT_RATES={'army_school':.004,'aegean_command':.006,'professional_cadres':.01,'sea_control':.015,'close_support':.01,'external_room':.003,'aegean_deterrence':.01,'security_budget':.01}
LARGE_PROJECTS={'industrial_credit','shipyards','public_credit','national_health','orthodox_plan'}
ACTOR_PRICES={'gre_network':.75,'gre_coup':1.5,'gre_escalate':1.5}

def native_fraction(percent):
 value=Decimal(str(percent))/100
 text=format(value,'f').rstrip('0').rstrip('.')
 if text in ('','0'):return '0'
 assert len(text.split('.')[1])<=5,(percent,text)
 return text

def binding(spirit,rate,receipt,days=None,additional_flags=()):
 ids={'Staff College Funding':'COLDWAR_GRE_R2_idea_staff_college_funding','Aegean Staff Funding':'COLDWAR_GRE_R2_idea_aegean_staff_funding','Forward Operational Planning':'COLDWAR_GRE_R2_idea_forward_operational_planning','Operational Initiative in Cyprus':'COLDWAR_GRE_R2_idea_operational_initiative','Aegean Expeditionary Command':'COLDWAR_GRE_R2_idea_aegean_expeditionary_command'}
 return {'spirit':spirit,'required_idea_id':ids.get(spirit,spirit),'idea_definition_status':'New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.','weekly_gdp_percent':rate,'native_weekly_fraction':native_fraction(rate),'active_instance_receipt':receipt,'original_issue_receipt':receipt+'_issued_once','original_expiry_receipt':receipt+'_expired'if days else None,'required_flags':list(additional_flags),'maximum_days':days,
  'gate':'Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.',
  'cleanup':'On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.',
  'refresh_on_removal':'Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.',
  'removal_order':['Clear only the active budget episode, preserving the original issue/expiry clock','Set this stream contribution to zero','Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time'],
  'expiry_clock':'Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.',
  'calculation':'Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans.'}

def apply_prices(d):
 if d.get('fiscal_revision'):return
 records=[]
 def record(key,old,new,kind):
  if old!=new:records.append({'key':key,'kind':kind,'old_gdp_percent':old,'new_gdp_percent':new})
 for f in d['focuses']:
  old=f['setup_gdp_percent'];new=round(old*(3 if f['key']in LARGE_PROJECTS else 2),5)
  f['setup_gdp_percent']=new;record(f['key'],old,new,'one-time setup')
  old=f['weekly_gdp_percent'];new=PERMANENT_RATES.get(f['key'],round(old*4,5))
  if f['key']=='operational_initiative':new=.03
  if f['key']=='staff_network':new=.01
  f['weekly_gdp_percent']=new;record(f['key'],old,new,'weekly expense')
  if new:f['native_weekly_fraction']=native_fraction(new)
  if f['key']in ('army_school','aegean_command'):
   name='Staff College Funding'if f['key']=='army_school'else'Aegean Staff Funding'
   f['effects'].append({'type':'temporary','spirit':name,'days':180,'values':{}})
   f['description']=('A cohort of officers receives training in combined operations. A 180-day appropriation pays instructors and facilities; the completed staff education endures after the appropriation ends.'if f['key']=='army_school'else'Naval and air staffs prepare a common defence plan for the islands and sea lanes. A 180-day appropriation funds the initial coordination. The technical preparation and staff experience endure after that funding period.')
  temp=next((e for e in f['effects']if e['type']=='temporary'),None)
  if temp and new:
   receipt='COLDWAR_GRE_R2_'+f['key']+'_budget_episode'
   f['budget_binding']=binding(temp['spirit'],new,receipt,temp['days'])
   f['weekly_lifetime']=f"Only while {temp['spirit']} is active, for at most {temp['days']} days from its original issue. Removal or cancellation stops the expense immediately."
   if f['key']=='staff_network':f['budget_binding']['separate_from_penetration_receipt']=True
  elif new:
   f['budget_binding']={'weekly_gdp_percent':new,'native_weekly_fraction':native_fraction(new),'gate':'Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.','source_receipt':f['id']}
  for e in f['effects']:
   if e['type']=='conditional_transaction'and f['key']=='gre_escalate':
    old=e['weekly_gdp_percent'];e['weekly_gdp_percent']=.05;record(f['key']+'_expedition',old,.05,'weekly expense')
    spirit=next(x for x in e['effects']if x['type']=='temporary')
    e['budget_binding']=binding(spirit['spirit'],.05,e['active_receipt'],spirit['days'])
   if e['type']=='existing_actor':
    if f['key']in ACTOR_PRICES:
     new=ACTOR_PRICES[f['key']]
     e['effects']=[f'Treasury -{new:g}% of current Greek GDP'if text.startswith('Treasury -')else text for text in e['effects']]
     f['native_price_override']={'payer':'GRE','gdp_basis':'GRE','setup_gdp_percent':new,'native_fraction':native_fraction(new),'charge_count':1,'policy':'Replace the old helper debit, cached price, affordability guard and native preview. Do not add a new fee on top. Preserve the shared focus/apply IDs.','replaces':'.25% CYP GDP'if f['key']=='gre_network'else'.5% CYP GDP'if f['key']=='gre_coup'else'.5% GRE GDP'}
    if f['key']=='gre_volunteers':
     e['effects']=[text.replace('0.002%','0.02%')for text in e['effects']]
     f['budget_binding']=binding('COLDWAR_CYP_R2_cyprus_volunteer_mission',.02,'COLDWAR_CYP_R2_volunteer_mission_authorized',additional_flags=['COLDWAR_CYP_R2_volunteer_expense_active'])
     f['budget_binding']['replaces_native_stream']='Replace the existing Greek volunteer contribution in COLDWAR_CYP_R2_crisis_weekly_streams with 0.0002 and its has_idea gate. Do not also add it as a second Greek programme.'
     f['weekly_lifetime']='Only while the actual volunteer mission exists and real deployment remains active. Removing the mission stops this expense.'
   if e['type']=='union_integration':
    e['setup_per_state_gdp_percent']=1
    e['weekly_after_gdp_percent']=.004
    for name,v in e['variants'].items():
     v['setup_gdp_percent']=2 if name=='full'else 1
     v['stop_weekly_gdp_percent']=.03 if name=='full'else .015
    e['lifecycle']='Remove the matching unsettled administration and its weekly charge, then add the regional-representation spirit and 0.004% Greek-GDP weekly civil-service programme. The programme lasts while Greece retains the integrated territory. Never repeat assets or setup payments.'
    e['budget_binding']={'spirit':e['settlement_spirit'],'weekly_gdp_percent':.004,'native_weekly_fraction':native_fraction(.004),'gate':'Actual regional-representation spirit and retained integrated territory. State institutions persist across party changes.'}
 for key,o in d['offers'].items():
  for country,s in o['sides'].items():
   old=s['setup_gdp_percent'];s['setup_gdp_percent']=round(old*2,5);record(key+'_'+country,old,s['setup_gdp_percent'],'one-time setup')
   for field in ('weekly_gdp_percent','income_gdp_percent'):
    old=s.get(field)
    if old:s[field]=round(old*4,5);record(key+'_'+country,old,s[field],field)
   if s.get('weekly_formula'):
    formula=s['weekly_formula'];formula['per_recipient_gdp_percent']=.004;formula['preview_gdp_percent']=round(.004*formula['recipient_count'],5)
    formula['runtime']='0.00004 * Greek GDP * exact approved recipient count in native MD weekly units.'
   if key in ('enosis_full','enosis_south')and country=='GRE':
    previous_setup=s['setup_gdp_percent'];previous_weekly=s['weekly_gdp_percent']
    s['setup_gdp_percent']=5 if key=='enosis_full'else 2.5
    s['weekly_gdp_percent']=.03 if key=='enosis_full'else .015
    record(key+'_'+country,previous_setup,s['setup_gdp_percent'],'territorial setup override')
    record(key+'_'+country,previous_weekly,s['weekly_gdp_percent'],'territorial weekly override')
   for field in ('weekly_gdp_percent','income_gdp_percent'):
    if s.get(field):s['native_'+field+'_fraction']=native_fraction(s[field])
   if s.get('weekly_gdp_percent')or s.get('income_gdp_percent'):
    s['budget_binding']={'spirit':s['spirit'],'gate':'Actual owning spirit plus the signed active programme/relationship receipt. Clear to zero on suspension or removal. Both payer and receiver use the same current Greek-GDP basis for transferred money.','once_per_accumulator':True}
    if o.get('kind')=='territorial_union':s['budget_binding']['gate']='Actual interim administration spirit and retained transferred territory, until integration or removal. Cyprus is expected to no longer exist; do not apply bilateral-country-existence gates to this Greek domestic administration.'
  if key in ('association','accession'):
   o['requirements']=o['requirements'].replace('0.001%','0.004%').replace('0.006%','0.024%')
  if key in ('enosis_full','enosis_south'):
   o['transaction']['budget_lifecycle']='Charge the new setup once on actual incorporation. Weekly unsettled-administration expense requires the actual interim spirit and ownership, and stops on integration/removal. After integration replace it with the0.004% weekly regional programme, never stack both charges.'
 d['fiscal_revision']={'project':'IMPERIA COLD WAR','date':'2026-10-30','policy':'General one-time commitments x2, selected major capital programmes x3; larger differentiated recurring budgets and explicit crisis-helper replacement prices. Modifier percentages, focus times, material requirements and PP prices are unchanged.','changes':records,'one_time_overrides':ACTOR_PRICES,'temporary_streams':[f['budget_binding']for f in d['focuses']if f.get('budget_binding',{}).get('maximum_days')],
  'expeditionary_stream':next(e['budget_binding']for f in d['focuses']if f['key']=='gre_escalate'for e in f['effects']if e['type']=='conditional_transaction'),
  'volunteer_stream':next(f['budget_binding']for f in d['focuses']if f['key']=='gre_volunteers'),
  'native_turkish_stream':'Preserve its separately approved rate, but require COLDWAR_CYP_R2_cyprus_intervention_forces plus the active intervention receipt in the existing local accumulator. A stale intervention_expense_cached flag must not charge after the 180-day spirit expires. No new Turkish fee or duplicated stream.',
  'precision':'Each numeric runtime coefficient is GDP-percent /100, at most five fractional digits. Community aggregate uses exact member count, not another custom membership list.','integration_boundary':'Concept repricing only. Update each owning Greek/CYP generator, actual native helper fee, native preview and weekly money consumer together after approval. These data are not installed runtime changes.'}
 d['implementation_contract']['fiscal_revision']=d['fiscal_revision']['policy']+' Temporary charges require actual spirit presence and the original live instance in the existing money calculation; resetting contributions to zero prevents stale cached expenses. No weekly relationship observer is added.'
 d['implementation_contract']['community']=d['implementation_contract']['community'].replace('0.001%','0.004%')
 d['implementation_contract']['nato']=d['implementation_contract']['nato'].replace('0.005%','0.05%')
 d['implementation_contract']['entry_transaction']=d['implementation_contract']['entry_transaction'].replace('0.5% Greek-GDP','1.5% Greek-GDP')

def report(d):
 from math import ceil
 bindings=d['fiscal_revision']['temporary_streams']+[d['fiscal_revision']['expeditionary_stream']]
 scenarios=[]
 for b in bindings:
  assert b['required_idea_id'].startswith('COLDWAR_')and b['maximum_days']==180
  for case,idea,episode,live in [('active',True,True,True),('spirit_removed_stale_cache',False,True,True),('original_deadline_expired',True,True,False),('episode_cancelled',True,False,True)]:
   amount=b['weekly_gdp_percent']if idea and episode and live else 0
   scenarios.append({'spirit':b['spirit'],'case':case,'expected_weekly_gdp_percent':amount})
 def compatible_max(group):
  fs=[f for f in d['focuses']if f['group']==group];names={f['key']for f in fs};best=(0,[])
  for mask in range(1<<len(fs)):
   chosen={fs[i]['key']for i in range(len(fs))if mask&(1<<i)}
   if any(any(e in chosen for e in f['exclusive'])or any(not(set(g)&chosen)for g in f['prerequisites']if set(g)<=names)for f in fs if f['key']in chosen):continue
   price=sum(f['setup_gdp_percent']for f in fs if f['key']in chosen)
   if price>best[0]:best=(price,sorted(chosen))
  return {'setup_sum_gdp_percent':round(best[0],5),'focuses':best[1],'basis':'Maximum structurally compatible one-time price sum within this section, constant-GDP reference. Not a treasury forecast or a combination of incompatible focuses.'}
 return {'project':'IMPERIA COLD WAR','status':'Static design-price and lifecycle audit. Not observed native cash flow.','revision':d['fiscal_revision']['date'],'rates':d['fiscal_revision']['changes'],'native_actor_replacement_prices':d['fiscal_revision']['one_time_overrides'],'temporary_stream_count':len(bindings),'temporary_streams':[dict(b,max_week_equivalents=ceil(b['maximum_days']/7),reference_period_gdp_percent=round(b['weekly_gdp_percent']*ceil(b['maximum_days']/7),5))for b in bindings],'desired_lifecycle_scenarios':scenarios,'compatible_setup_maxima':{g:compatible_max(g)for g in ('economy','defence')},'limits':'Country GDP changes, native spending laws, active party/leader, debts, bilateral funding and native payment boundaries affect the real result. Spirit presence, money refresh, weekly boundaries and shortfalls must be tested in the actual engine after implementation.'}
