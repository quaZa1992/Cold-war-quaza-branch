# IMPERIA COLD WAR — Cyprus intervention, Turkish army crisis and Greek escalation concept.
"""Review data only. No events, decisions, ideas, NATO or country history are installed."""
from copy import deepcopy
import re

def clean_prose(text):
 text=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',text)
 text=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',text)
 text=re.sub(r'(?<=%)(?=[A-Za-z])',' ',text)
 text=re.sub(r'(?<=[A-Za-z])(?=[+-]\d)',' ',text)
 text=re.sub(r',(?=[A-Za-z])',', ',text)
 return text.replace('SeeRESEARCH','See RESEARCH').replace('andREVIEW','and REVIEW')

INTERVENTION = dict(name='Cyprus Intervention Forces',days=180,values={
 'navy_org_factor':.15,'naval_invasion_prep_speed':.50,'amphibious_invasion':.15,
 'planning_speed':.30,'max_planning_factor':.20})
ANGRY = dict(name='Angry General Staff',days=180,values={
 'stability_factor':-.10,'army_org_factor':-.10,'political_power_factor':-.15})
CONTROL = dict(name='Command Reorganization',days=90,values={
 'army_org_factor':-.05,'political_power_factor':-.05})
VOLUNTEERS = dict(name='Cyprus Volunteer Mission',days=None,values={
 'send_volunteer_size':2,'send_volunteer_divisions_required':-1.0,
 'send_volunteers_tension':-1.0,'political_power_factor':-.05})
LABELS={'navy_org_factor':'Navy organization','naval_invasion_prep_speed':'Naval invasion preparation speed',
 'amphibious_invasion':'Amphibious invasion attack','planning_speed':'Planning speed',
 'max_planning_factor':'Maximum planning','send_volunteer_size':'Volunteer division limit',
 'send_volunteer_divisions_required':'Minimum army size for volunteers',
 'send_volunteers_tension':'World tension requirement for volunteers'}

def spirit_lines(spirit,labels):
 duration=f" ({spirit['days']} days)"if spirit['days']else ' (while the Cyprus mission remains eligible)'
 lines=[spirit['name']+duration]
 for key,value in spirit['values'].items():
  amount=f'{value:+g}'if key=='send_volunteer_size'else f'{value*100:+g}%'
  lines.append(labels[key]+' '+amount)
 return lines

def extend(data):
 labels=data['modifier_labels'];labels.update(LABELS)
 actors=deepcopy(data['actor_focuses'])
 by={a['key']:a for a in actors}
 by['tur_consult'].update(x=4,cost=2,
  description='The guarantors must consider the overthrow of the constitutional government and the security of both communities. Consultation opens a short period for an agreed settlement or a Turkish decision to act.',
  requirements='A real Cyprus constitutional rupture remains unresolved. Greece, Turkey and Britain are treaty parties.',
  effects=['Greece and the United Kingdom receive Guarantor Consultations','Intervention deadline: 30 days after consultations fail'])
 by['tur_operation'].update(title='Intervene in Cyprus',x=4,y=1,cost=1,
  description='Order a military operation in Cyprus. Concentrated naval readiness and prepared landing plans favour rapid intervention, but the expedition creates real financial and diplomatic commitments.',
  requirements='Consultations failed and the actual Cyprus security crisis remains unresolved. Turkey and Cyprus are independent and not already at war. The 30-day deadline and refusal consequences are shown before selection.',
  effects=['Political power -75','Treasury -0.5% of current Turkish GDP','Expense +0.005% of Turkish GDP per week while the intervention is active',
   'Turkey declares war on Cyprus','Remove Angry General Staff']+spirit_lines(INTERVENTION,labels),
  exclusive=['tur_terms','tur_abstain'],
  transaction={'war_target':'CYP','war_starts_on_completion':True,'one_time_per_crisis':True,
   'setup_gdp_fraction':.005,'weekly_gdp_fraction':.00005,
   'bonus_duration_days':180,'bonus_ends_at_related_peace':True,'repeat_bonus_on_reversal':False})
 by['tur_terms'].update(x=0,y=1,cost=1,exclusive=['tur_operation','tur_abstain'],
  description='Seek an accepted constitutional restoration and credible safeguards for the Turkish Cypriot community. Diplomacy avoids an expedition if it resolves the security crisis before the intervention deadline.',
  requirements='Cyprus and the relevant guarantors must accept the proposed terms. Local communal consent remains separate. An unresolved crisis at the 30-day deadline still produces Angry General Staff and the military-pressure chain.',
  effects=['Cyprus receives Communal Guarantees Proposal','If accepted: Turkey Stability +3%','If accepted: Turkey Army attack -2%',
   'If the security crisis remains unresolved: Angry General Staff (180 days)',
   'Stability -10%','Army organization -10%','Political power gain -15%','Military pressure +70'])
 actors.append(dict(tag='TUR',key='tur_abstain',id='COLDWAR_TUR_CYP_R2_tur_abstain',title='Refuse Intervention',x=8,y=1,pre=['tur_consult'],
  exclusive=['tur_terms','tur_operation'],cost=1,party_trigger=None,
  description='The government refuses an expedition while the Cyprus crisis remains unresolved. It preserves resources and diplomatic restraint, but senior officers challenge its resolve and civilian authority.',
  requirements='The Cyprus security crisis is unresolved. This choice immediately starts the military-pressure chain. A coup is possible after 60 days unless civilian control or intervention resolves the confrontation.',
  effects=['Political power +75']+spirit_lines(ANGRY,labels)+['Military pressure +70','Military memorandum after 30 days','Coup resolution after 60 days'],
  decision_exception='Finite Turkish army crisis only. No Cyprus decision menu.'))

 actors += [
 dict(tag='GRE',key='gre_response',title='The Turkish Landing',x=5,y=4,pre=[],exclusive=[],cost=1,party_trigger=None,
  description='Turkish forces have entered the Cyprus war. Greece must decide whether to sustain Cyprus through a volunteer mission or enter the conflict as a belligerent.',
  requirements='An actual Turkey-Cyprus war from this crisis is active. Greece and Cyprus are independent. Greece is not already fighting Cyprus.',
  effects=['Political power +25','Cyprus receives Greek Assistance Consultations']),
 dict(tag='GRE',key='gre_volunteers',title='Volunteers for Cyprus',x=2,y=5,pre=['gre_response'],exclusive=['gre_escalate'],cost=1,party_trigger=None,
  description='A volunteer mission can assist Cyprus while Greece avoids direct entry into the war. Cyprus must accept the deployment, and the volunteers must come from formations Greece actually possesses.',
  requirements='Turkey is at war with Cyprus. Greece is not at war with either country. Cyprus consents through the real volunteer diplomatic action. Native volunteer and diplomatic-action rules still apply.',
  effects=['Political power -50','Expense +0.002% of Greek GDP per week while the mission remains active',
   'If Cyprus accepts:']+spirit_lines(VOLUNTEERS,labels)+['Cyprus: accepted Greek volunteer deployment','NATO membership unchanged'],
  transaction={'target':'CYP','sponsor':'GRE','recipient_consent':True,'no_free_divisions':True,
   'native_action_required':True,'one_time_per_crisis':True,'weekly_gdp_fraction':.00002,
   'observation':'CYP has_volunteers_amount_from = { tag = GRE count > 0 }','global_rule_override':False}),
 dict(tag='GRE',key='gre_escalate',title='Fight Beside Cyprus',x=8,y=5,pre=['gre_response'],exclusive=['gre_volunteers'],cost=1,party_trigger=None,
  description='Enter the Cyprus war against Turkey. Greece and Turkey leave NATO for the duration of this conflict, and their previous membership is restored once their war and the Cyprus-Turkey war have both ended.',
  requirements='The Turkey-Cyprus war is active. Greece is not already at war with Turkey or Cyprus. Entry must place Greece alongside Cyprus. The temporary NATO exit and return are disclosed to both countries before entry.',
  effects=['Political power -100','Treasury -0.5% of current Greek GDP','Greece: Leave NATO','Turkey: Leave NATO',
   'Greece: remove NATO Membership','Greece: Daily Pro-Western Support -0.02','Greece: Defensive war stability -3%','Greece: War support -2%',
   'Turkey: remove NATO Membership','Turkey: Daily Pro-Western Support -0.02','Turkey: Defensive war stability -3%','Turkey: War support -2%',
   'Greece and Turkey leave NATO technology sharing and mutual military access',
   'Other NATO members: opinion of Greece -20','Other NATO members: opinion of Turkey -20',
   'Greece joins Cyprus in the war against Turkey','After Greece-Turkey and Cyprus-Turkey peace: Greece returns to NATO',
   'After Greece-Turkey and Cyprus-Turkey peace: Turkey returns to NATO',
   'After related peace, Greece: Daily Pro-Western Support +0.02','After related peace, Greece: Defensive war stability +3%',
   'After related peace, Greece: War support +2%','After related peace, Turkey: Daily Pro-Western Support +0.02',
   'After related peace, Turkey: Defensive war stability +3%','After related peace, Turkey: War support +2%',
   'After related peace: both return to NATO technology sharing and mutual military access'],
  transaction={'leave_before_add_to_war':True,'war_side':'CYP','enemy':'TUR','one_time_per_crisis':True,
   'snapshot_prior_members':['GRE','TUR'],'new_faction_not_created':True,'automatic_return':True}),
 ]
 for a in actors:
  a.setdefault('id','COLDWAR_'+a['tag']+'_CYP_R2_'+a['key'])
 data['actor_focuses']=actors
 data['decision_policy']='No Cyprus decision menus. Latest user exception: finite Turkey-only army crisis decisions.'
 data['intervention']={
  'project':'IMPERIA COLD WAR','status':'Concept, not implemented in HOI4',
  'initial_deadline_days':30,'army_crisis_days':180,'military_pressure_initial':70,
  'memorandum_day':30,'memorandum_pressure_delta':15,'coup_day':60,'successful_coup_pressure_min':60,
  'civilian_control_pressure_max':35,'intervention_buff':INTERVENTION,'angry_army':ANGRY,
  'civilian_control_spirit':CONTROL,'volunteer_spirit':VOLUNTEERS,
  'native_keys_reference':'REVIEW_INTERVENTION_MECHANICS.md',
  'eligibility':'Only this campaign crisis, after a real constitutional rupture and failed guarantor consultation. Resolved security terms cancel the countdown and military plot. No pressure merely for an ordinary peaceful disagreement.',
  'activation':'Refuse Intervention starts the army crisis immediately. Inaction or failed negotiations starts it when the 30-day deadline expires. A successful real settlement avoids it.',
  'pressure_is_not_random':'No daily drift or random daily coup roll. Pressure starts at 70, each of two once-only measures removes25, the day30 memorandum adds15, and day60 resolves the disclosed thresholds.',
  'intervention_commitment':'Military bonuses start only with an actual declared Turkish intervention. They end at180days or related peace, whichever occurs first. A reversal from restraint reuses the original crisis receipt and never refreshes a used bonus or setup grant.',
  'crisis_cancellation':'All deadlines are relative to army-crisis activation, not the original consultation date. Explicit refusal activates immediately; no-action or failed diplomacy activates after the30-day intervention window. Any successful intervention, accepted security resolution or completed civilian-control settlement marks the army-crisis instance closed before removing the spirit. All pending30/60/180-day outcomes require the same still-active instance and therefore become no-ops. The original180-day intervention expiry receipt is separate and cannot be restarted.',
  'coup_outcome':'At day60: pressure>=60 installs the dated native military-junta government; pressure36..59 produces a defeated plot and stability-5%; pressure<=35 with the two control measures defeats the plot. A takeover does not automatically declare another war.',
  'scheduler':'One-shot crisis events at30,60and180days. Flags/instance receipts discard stale events. Existing monthly fallback only; no new daily or weekly relationship observer.',
  'historical_status':'The Angry General Staff refusal response and simultaneous full NATO exits/automatic returns are requested RP alternate history. Historical Greece left integrated military command in1974, remained an Alliance member, and returned to the integrated structure in1980.',
  'nato':dict(exit_trigger='Greek direct-war focus, not Turkey initial intervention or the Greek volunteer choice',
   snapshot_before_either_exit=True,leave_effect='NATO_leave',join_effect='NATO_join',
   block_early_readmission=True,
   entry_effect='add_to_war = { targeted_alliance = CYP enemy = TUR }',
   order=['Validate current crisis, participants and war sides','Snapshot actual Greek and Turkish NATO status and current faction',
    'Apply NATO_leave only to actual NATO members','Join Greece to the Cyprus side against Turkey','Create one restoration receipt for each prior member'],
   end_requires_peace_pairs=[['GRE','TUR'],['CYP','TUR']],all_world_peace_required=False,
   restore_only_prior_members=True,restore_once=True,return_delay_maximum='Next monthly fallback if no peace-resolution hook ran',
   safeguards=['Both countries must still exist and be independent','NATO must have a real living faction leader',
    'Block NATO_join, NATO_join_via_event and stale accession acceptance while this separation receipt remains war-active',
    'Do not join a faction while fighting its members','Do not overwrite a different intervening faction',
    'Do not replay exit/join through repeated events','Retain pending restoration if exceptional engine state blocks return'],
   native_bookkeeping='Use the shared helpers for idea, technology sharing, array, opinion, military access and faction changes. No manual member-array edits.',
   article_five='Both leave before Greece joins the war, preventing the ordinary member-versus-nonmember NATO war reaction from treating this entry as an attack on a current ally.'),
 }
 data['crisis_decisions']=[
  dict(key='rotate',title='Reassign Exposed Commanders',country='TUR',once=True,
   requirements='Angry General Staff crisis active. Not already used. Civilian government remains.',
   effects=['Political power -50','Treasury -0.25% of current Turkish GDP','Military pressure -25'],pressure_delta=-25,pp_cost=50,gdp_percent=.25),
  dict(key='mandate',title='Secure a Parliamentary Mandate',country='TUR',once=True,
   requirements='Angry General Staff crisis active. Not already used. Civilian government remains.',
   effects=['Political power -75','Military pressure -25'],pressure_delta=-25,pp_cost=75,gdp_percent=0),
  dict(key='control',title='Reassert Civilian Authority',country='TUR',once=True,
   requirements='Both control measures are completed. Military pressure at most35. The coup has not succeeded.',
   effects=['Political power -75','Treasury -0.25% of current Turkish GDP','Remove Angry General Staff']+spirit_lines(CONTROL,labels),
   pressure_delta=0,pp_cost=75,gdp_percent=.25),
  dict(key='intervene',title='Authorize the Cyprus Operation',country='TUR',once=True,
   requirements='The same Cyprus security crisis remains unresolved. Turkey has not intervened in this crisis and is not already at war with Cyprus.',
   effects=['Political power -75','Treasury -0.5% of current Turkish GDP','Remove Angry General Staff',
    'Turkey declares war on Cyprus','Expense +0.005% of Turkish GDP per week while the intervention is active']+spirit_lines(INTERVENTION,labels),
   pressure_delta=0,pp_cost=75,gdp_percent=.5),
 ]
 for c in data['crisis_decisions']:c['id']='COLDWAR_TUR_CYP_R2_army_'+c['key']
 # Extend the existing road-to-war view with the requested consequences rather than invent a separate story.
 crisis={c['key']:c for c in data['crisis']}
 crisis['intervention'].update(title='Turkish Intervention or Restraint',next=['turkish_operation','army_warning'],
  text='Intervene in Cyprus starts the real war and180days of naval organization+15%, invasion preparation+50%, amphibious attack+15%, planning speed+30%and maximum planning+20%. Refusal or an unresolved30-day deadline starts Angry General Staff.')
 crisis['settlement']['next']=[]
 data['crisis'] += [
  dict(key='army_warning',title='Angry General Staff',actor='Turkey crisis chain',next=['civilian_control','tur_coup','late_intervention'],
   text='180days: stability-10%, army organization-10%, political-power gain-15%. Pressure70. A memorandum at day30 adds15; at day60 a coup succeeds at60or more. Two once-only actions remove25pressure each, allowing a civilian-control settlement.'),
  dict(key='civilian_control',title='Civilian Authority Restored',actor='Turkey',next=[],
   text='Reassign commanders and secure a parliamentary mandate, then reassert civilian authority. This closes the coup chain without declaring war and replaces the angry-army penalty with90days of command reorganization.'),
  dict(key='tur_coup',title='Military Takeover Risk',actor='Turkey',next=[],
   text='Unaddressed pressure60or more at day60 brings a native military-junta government. The danger is stated in advance. No daily random roll and no automatic extra war.'),
  dict(key='late_intervention',title='Authorize the Cyprus Operation',actor='Turkey crisis action',next=['turkish_operation'],
   text='Intervention during the army confrontation removes the refusal penalty and starts the same guarded Cyprus operation. The180-day military bonus cannot be renewed through repeated authorizations.'),
  dict(key='turkish_operation',title='Actual Turkish Intervention',actor='Turkey at war with Cyprus',next=['greek_choice'],
   text='An actual Turkish declaration of war activates the operation. Only this war outcome opens Greece military-support fork; Turkish civilian-control measures or peaceful restraint do not.'),
  dict(key='greek_choice',title='The Greek Exclusive Choice',actor='Greece focus paths',next=['volunteers','greek_war'],
   text='After a real Turkish intervention, Greece chooses Volunteers for Cyprus or Fight Beside Cyprus. The two focuses exclude each other; volunteer aid keeps NATO status, direct war causes both temporary exits.'),
  dict(key='volunteers',title='Volunteers for Cyprus',actor='Greece, Cyprus consent',next=['aftermath'],
   text='Volunteer limit+2, minimum army-size requirement-100%, tension requirement-100%. Cyprus must accept the real deployment; no divisions are created. Greece remains outside the war and both countries keep existing NATO membership.'),
  dict(key='greek_war',title='Greek-Turkish War',actor='Greece fights beside Cyprus',next=['nato_return'],
   text='Snapshot both memberships, remove both through native NATO_leave, then add Greece to the Cyprus side. Neither is a NATO member for this war. Cyprus must be at war with Turkey; no automatic faction annexation or new NATO call.'),
  dict(key='nato_return',title='Peace and NATO Return',actor='Greece and Turkey',next=['aftermath'],
   text='When Greece-Turkey AND Cyprus-Turkey hostilities end, both prior members automatically return through NATO_join. Unrelated foreign wars do not define the end. Exceptional incompatible states retain a pending return; monthly fallback does not poll daily.'),
 ]
 data['crisis_layers']=[['baseline'],['choice'],['autonomy','mission'],['network'],['warning'],['failed','coup'],
  ['consultation'],['settlement','intervention'],['army_warning','turkish_operation'],['civilian_control','tur_coup'],
  ['late_intervention'],['greek_choice'],['volunteers','greek_war'],['nato_return'],['aftermath']]
 # A shared receipt closes the army plot before either focus or crisis authorization starts a war.
 for key in ('tur_operation','gre_escalate','gre_response'):
  a=next(f for f in data['actor_focuses']if f['key']==key)
  a.setdefault('transaction',{})['current_crisis_instance_required']=True
  if key=='tur_operation':
   a['transaction']['close_pending_army_crisis_before_war']=True
  if key in('gre_response','gre_escalate'):
   a['availability_native']=['CYP exists','TUR exists','TUR has_war_with = CYP','current Cyprus intervention receipt active']
 decisions={d['key']:d for d in data['crisis_decisions']}
 for key in('intervene','control'):
  decisions[key]['close_army_instance_before_effects']=True
  decisions[key]['stale_delayed_events_no_op']=True
 decisions['intervene']['shared_receipt_with_focus']='tur_operation'
 for a in data['actor_focuses']:
  for field in('title','description','requirements'):
   if field in a:a[field]=clean_prose(a[field])
  a['effects']=[clean_prose(s)for s in a['effects']]
 for a in data['crisis_decisions']:
  a['requirements']=clean_prose(a['requirements']);a['effects']=[clean_prose(s)for s in a['effects']]
 for node in data['crisis']:
  for field in('title','actor','text'):node[field]=clean_prose(node[field])
 return data

def document(data):
 i=data['intervention']
 lines=['IMPERIA COLD WAR: Turkish intervention, army crisis and Greek escalation','',
  'Concept extension requested27October2026. Not implemented in the loaded mod. The100Cyprus focuses stay intact. Supporting guarantor focuses now include a Turkish intervention/refusal fork and a Greek volunteer/direct-war fork.','',
  '## Player-visible intervention terms','']
 for s in (INTERVENTION,ANGRY,CONTROL,VOLUNTEERS):lines+=['### '+s['name'],'']+['- '+v for v in spirit_lines(s,data['modifier_labels'])]+['']
 lines+=['Turkey pays75political power and0.5%of its own current GDP once on authorizing intervention, with0.005%GDP per week while the expedition is active. The military bonus has an absolute180-day expiry and ends earlier at related peace. Calling the operation through a later army-crisis response cannot renew an already used bonus.','',
  '## Refusal and civilian control','',i['eligibility'],i['activation'],i['pressure_is_not_random'],i['coup_outcome'],'',
  'This is the sole authorized native decision-menu exception. It appears only for the active Turkish army crisis, contains four finite actions, and disappears at resolution. The rest of the Cyprus concept uses focus choices and foreign response events.','']
 for d in data['crisis_decisions']:lines+=['### '+d['title'],'',d['requirements'],'']+['- '+s for s in d['effects']]+['']
 lines+=['At pressure70, the two once-only measures lower pressure to20. If the day30 memorandum has already happened, they lower85to35. Both meet the stated civilian-control threshold. No actions by day60 leave85and cause the coup. The two control measures cost125PP and0.25%GDP; immediate civilian settlement adds75PP and0.25%GDP. Both are alternatives to an expedition and its continuing expense.','',
  'Success or failure is disclosed rather than an unexplained random percentage. A resolved Cyprus security settlement cancels the external-crisis trigger; a genuine peaceful solution is not treated as ordinary inaction. A cabinet change alone cannot erase a pending army confrontation. A successful military takeover uses the actual dated native Turkish party/leader roster, whose exact selection still requires implementation review.','',
  '## Greek intervention and NATO','',
  'Greek volunteers require Cyprus acceptance via the real diplomatic volunteer action. Permission modifiers reduce native thresholds and increase capacity, but do not create units or certify deployment. Global can_send_volunteers rules are not overwritten. The wartime mission pauses when its eligibility fails and expires with the relevant Cyprus war; native volunteer return behavior still needs an engine check.','',
  'Direct Greek entry costs100PP and0.5%Greek GDP. It uses the native add_to_war shape with targeted_alliance=CYP and enemy=TUR after shared NATO_leave effects. It creates co-belligerency with Cyprus rather than forcing Cyprus into a new faction. Full NATO exit is only triggered by this direct-war branch, not initial Turkish intervention or volunteer assistance.','',
  'Before either exit, snapshot GRE and TUR memberships separately, the current NATO faction, and the one-shot conflict instance. Remove through the native NATO_leave helper before war entry; do not just remove the idea or manually alter global.nato_members. This prevents the normal Article5 script from seeing Turkey as a current member attacked by a newly nonmember Greece. NATO_leave already owns array, access, opinion, technology-sharing and leadership cleanup.','',
  'Automatic return requires both GRE-TUR peace and CYP-TUR peace. Unrelated wars need not end. Use NATO_join for prior members only, with an actual living NATO leader, independence, no conflicting faction, and no war against current NATO members. A missing/dead country or incompatible faction retains a pending receipt; retries are monthly rather than daily. Snapshotting both before either removal prevents sequential-state errors. Never restore a country that was outside NATO before the crisis.','',
  'The temporary-separation receipt also blocks early re-admission through NATO_join,NATO_join_via_eventandstale accession responses while the relevant war remains active. A different NATO accession path must not put one participant back inside the Alliance mid-war and create a fresh Article5cascade. The same small guard belongs at the native membership entry transaction, with a targeted direct-idea callback fallback if needed; those shared integration edits are still unimplemented.','',
  'The requested default is automatic return of both1970members. Exceptional later player changes can make native faction entry impossible; those are disclosed pending-state cases rather than silently forced diplomacy. Full immediate automatic restoration after every possible external-state mutation is not proven by source inspection.','',
  'The native left_nato opinion penalty is-20and is not explicitly removed by NATO_join. The concept retains this diplomatic consequence and shows it for both countries at departure; full membership returns, but diplomatic confidence is not silently reset. The pre-existing+30NATO member opinion is removed/reapplied by the native helpers. No custom diplomatic penalty is stacked.','',
  '## Scheduling and evidence','',i['scheduler'],i['crisis_cancellation'],'',
  'Actual entry and peace/settlement effects call the targeted reconciliation immediately. Native peace-conference hooks and a monthly fixed-tag fallback finish restoration when ordinary peace delivery is not observed. One-shot delayed events at30/60/180days are finite deadlines, not recurring daily polling. Recheck the crisis instance before every payment, decision completion and scheduled outcome. Native weekly money bookkeeping reads only cached expedition/mission expense; no relationship scan is added.','',
  'Source checks: common/scripted_effects/01_NATO_effects.txt(NATO_leave,NATO_join); common/ideas/Factions.txt(NATO_memberarray hooks); common/on_actions/MD_NATO_on_actions.txt(Article5andadd_to_war); common/scripted_triggers/00_NATO_scripted_triggers.txt(can_join_NATO). SeeRESEARCH_NATO_RUNTIME.md andREVIEW_INTERVENTION_MECHANICS.md for exact references and remaining native-action limits.','',
  'Historical distinction: Greece left integrated military command in1974but remained an Alliance member; it returned to integrated command in1980. The requested simultaneous full exits and automatic returns, along with a refusal-triggered Turkish coup chain, are RP alternate history and balance proposals. SeeRESEARCH_INTERVENTION.md for FRUS,UNFICYPandNATO sources.','',
  'Static data checks and browser review do not establish in-game faction transitions, actual volunteers, event arrival, coup leaders, naval battle behavior or live multiplayer performance.']
 return '\n'.join(clean_prose(line)for line in lines)+'\n'
