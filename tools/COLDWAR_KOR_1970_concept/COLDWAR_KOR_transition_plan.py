# IMPERIA CW — Cold War: exact proposed state providers for the researched transition.
"""Approval-stage event, decision and ballot recipes; never installs content."""
P='COLDWAR_KOR_'

def complete_plan(d):
    ns={n['key']:n for n in d['nodes']}
    # Resolve the authored generic party category into an exact MD registry
    # owner before storing or comparing programme/expense records.
    group_party={g['id']:g['party'] for g in d['groups']}
    for n in d['nodes']:
        if n['ownership']=='party':
            slot=group_party[n['group']];assert slot is not None,n['id']
            n['ownership']='party:'+str(slot)
            commitment=n['effects'].get('expense_commitment')
            if commitment:commitment['slot']=n['ownership']+'|'+commitment['slot'].split('|',1)[1]
    aliases={'kjp_independent_party':'An Independent Party','korean_implementation_review':'Reciprocal Obligations',
      'constitutional_question':'Constitutional Review','defend_civil_command':'Uphold Civil Command',
      'independent_inquiry':'Independent Inquiry','consensus_presidency':'Consensus Presidency',
      'constitution_referendum':'Submit the Charter','accountable_intelligence':'Security Accountability',
      'independent_constitutional_court':'Constitutional Court',
      'staged_officer_retirement':'Phased Retirement','restore_labour_bargaining':'Labour Bargaining'}
    for key,label in aliases.items():ns[key]['full_title']=ns[key]['label'];ns[key]['label']=label
    # Remove an accidental duplicated informational guard before code emission.
    for n in d['nodes']:n['condition_code']=list(dict.fromkeys(n.get('condition_code',[])))
    # Distinct institutions may coexist. Explicit names also prevent a later
    # implementation from confusing government and leader-qualified records.
    for key,slot in (('roh_nordpolitik','nordpolitik'),('conservative_merger','coalition')):
        n=ns[key];n['effects']['policies'][0]['slot']=slot
        n['effects']['policies'][0]['qualified_slot']='army:'+slot
        n['effects']['expense_commitment']['slot']=n['ownership']+'|army:'+slot
    merger=ns['conservative_merger']
    merger['effects']['policies'][0]['active_condition']='Actual conservative coalition agreement ratified by the participating party organizations'
    merger['effects']['policies'][0]['active_trigger']='has_country_flag = '+P+'conservative_merger_ratified'
    merger['effects']['expense_commitment']['active_condition']=merger['effects']['policies'][0]['active_trigger']
    for index,key in enumerate(('presidential_democracy','parliamentary_democracy','consensus_presidency'),1):
        ns[key]['state_effects'].append('set_variable = { '+P+'charter_model = '+str(index)+' }')
    # Enacted legal basis and operational judicial review are separate.
    court=ns['independent_constitutional_court']
    court['requirements'].append('Enacts the court mandate; appointments and funded implementation must then be completed by decision before judicial review operates')
    court['effects']['policies'][0]['active_trigger']='has_country_flag = '+P+'constitutional_order\nhas_country_flag = '+P+'judicial_review_operational'
    court['effects']['policies'][0]['active_condition']='Constitutional order and actually operational judicial review'
    court['effects']['expense_commitment']['active_condition']=court['effects']['policies'][0]['active_trigger']
    for key in ('urban_insurance_network','rural_insurance_network'):
        ns[key]['historicity']='Rural insurance extension in1988 and urban self-employed coverage in1989 are historical references. An earlier funded extension is explicitly alternate history.'
    # All authority receipts have a named provider and a real political outcome.
    providers={
      P+'electoral_opening':{'provider':P+'transition_1971 / Respect the Competitive Mandate',
        'guard':'A genuine1971 electoral contest or a separately authorized earlier constitutional contest, not mere party popularity',
        'effect':'set_country_flag = '+P+'electoral_opening'},
      P+'caretaker_installed':{'provider':P+'install_interim_choi',
        'guard':'Park has actually left office; civilian succession chosen; native office transition has installed Choi Kyu-hah',
        'native_effect':'set_temp_variable = { rul_party_temp = 0 }\nset_temp_variable = { disable_elections = 1 }\nset_country_flag = '+P+'select_interim_choi\nchange_ruling_party_effect = yes\nif = { limit = { has_country_leader = { name = "Choi Kyu-hah" ruling_only = yes } } set_country_flag = '+P+'caretaker_installed }',
        'router_note':'NEW1970 dispatcher consumes select_interim_choi before modern pools;0 is the existing governing parliamentary vehicle, not a claim Choi personally joined the DRP. Preserve party votes.'},
      P+'military_opening_authorized':{'provider':P+'reopen_constitutional_talks / accepted1987 concession',
        'guard':'Actual military-led government accepts a negotiated opening after organized opposition pressure or a resolved command crisis',
        'effect':'set_country_flag = '+P+'military_opening_authorized'},
      P+'negotiating_commitment':{'provider':'Bind the Incumbent OR Retirement Guarantees OR a successful command-challenge resolution',
        'effect':'set_country_flag = '+P+'negotiating_commitment'},
      P+'lawful_election_completed':{'provider':P+'on_native_election_resolved',
        'guard':'Native election/coalition result actually resolved under the ratified constitution and installed the resulting incumbent',
        'effect':'set_country_flag = '+P+'lawful_election_completed',
        'prohibition':'No focus, declaration, party popularity or coalition membership may set this receipt on its own.'},
      P+'conservative_merger_ratified':{'provider':P+'transition_1990 / Ratify the Conservative Merger',
        'guard':'Actual participating DJP/RDP/NDRP organizations have authorized the bargain; earlier equivalents are alternate history. Kim Dae-jung’s organization is not included automatically.',
        'effect':'set_country_flag = '+P+'conservative_merger_ratified',
        'cleanup':'Clear on actual coalition dissolution. The earned programme can resume only with an actual re-ratified agreement; party change alone never manufactures one.'},
    }
    d['transition_receipt_providers']=providers
    decisions=[
      {'id':P+'reopen_constitutional_talks','repeatable':True,
       'available':'original_tag = KOR\nIMP_is_1970_scenario = yes\ncheck_variable = { ruling_party = 22 }\nhas_country_flag = '+P+'military_reconsolidation\nhas_country_flag = '+P+'opposition_constitutional_demand\nNOT = { has_country_flag = '+P+'constitutional_order }\nNOT = { has_country_flag = '+P+'military_opening_authorized }\nNOT = { has_country_flag = '+P+'transition_open }\nNOT = { has_country_flag = '+P+'talks_authorized }\nNOT = { has_country_flag = '+P+'talks_retry_cooldown }',
       'additional_guard':'The actual military-led government chooses this authorization. A legal opposition demand must be registered by the1985 constitutional campaign or equivalent verified opposition response.',
       'cost':'75PP; no automatic appointment or popularity',
       'effect':'add_political_power = -75\nset_country_flag = '+P+'military_opening_authorized\nclr_country_flag = '+P+'military_reconsolidation\nset_country_flag = { flag = '+P+'talks_retry_cooldown days = 90 }',
       'reader':'Enables Negotiated Withdrawal after a failed caretaker/command window without resetting any completed focus.'},
      {'id':P+'reopen_charter_ballot','repeatable':True,
       'available':'original_tag = KOR\nIMP_is_1970_scenario = yes\nhas_country_flag = '+P+'charter_rejected\nhas_country_flag = '+P+'talks_authorized\nhas_country_flag = '+P+'charter_mandate\nNOT = { has_country_flag = '+P+'constitutional_order }\nNOT = { has_country_flag = '+P+'ballot_pending }\nNOT = { has_country_flag = '+P+'charter_retry_cooldown }\ncheck_variable = { '+P+'charter_model > 0 }',
       'cost':'50PP;90d after rejection; same chosen constitutional model',
       'effect':'add_political_power = -50\nclr_country_flag = '+P+'charter_rejected\nset_country_flag = '+P+'ballot_pending\ncountry_event = { id = COLDWAR_KOR_transition.30 days = 30 }',
       'reader':'The decision itself reopens the ballot; the one-shot Submit the Charter focus remains completed. No new model, focus reward or building is granted.'},
      {'id':P+'register_charter_endorsement','repeatable':True,
       'available':'has_country_flag = '+P+'talks_authorized\nNOT = { has_country_flag = '+P+'ballot_pending }',
       'cost':'No new monetary fee; the party representative must accept the recorded negotiated terms',
       'effect':'For one actual eligible party slot s, set '+P+'charter_supporter_s only after that party’s endorsement response. No free support; a withdrawal clears the same receipt.',
       'reader':'The ballot helper checks this unique per-slot endorsement against current eligible native support. Power blocs are not automatically electoral parties.'},
    ]
    decisions.append({'id':P+'implement_constitutional_court','repeatable':False,
      'available':'original_tag = KOR\nIMP_is_1970_scenario = yes\nhas_country_flag = '+P+'constitutional_order\nhas_country_flag = '+P+'judicial_review\nNOT = { has_country_flag = '+P+'court_appointments_implemented }\nNOT = { has_country_flag = '+P+'court_implementation_pending }\nNOT = { has_country_flag = '+P+'judicial_review_operational }',
      'cost':'50PP and $1bn once;90d funded implementation',
      'effect':'add_political_power = -50\nset_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nset_country_flag = '+P+'court_implementation_pending\nset_country_flag = '+P+'court_appointments_implemented\nset_country_flag = { flag = '+P+'court_commissioning_delay days = 90 }\ncountry_event = { id = COLDWAR_KOR_transition.88 days = 90 }',
      'reader':'Appointments follow the enacted constitution and its nomination/confirmation rules. The event rechecks constitutional order. Interruption suspends operation without refund or repeat payment; restoration resumes the already funded process.'})
    d['transition_decisions']=decisions
    providers[P+'opposition_constitutional_demand']={'provider':'Actual1985 constitutional campaign or verified legal-opposition demand response',
      'guard':'Legal opposition party exists and has explicitly accepted the constitutional-demand campaign; no date-only automatic demand',
      'effect':'set_country_flag = '+P+'opposition_constitutional_demand'}
    providers[P+'court_appointments_implemented']={'provider':P+'implement_constitutional_court',
      'guard':'Enacted court mandate, actual nomination/confirmation settlement and paid implementation',
      'effect':'See the once-only decision; focus completion alone never grants this receipt'}
    ballot=d['transition_system']['ratification']
    ballot['resubmit_decision']=P+'reopen_charter_ballot'
    ballot['model_rejection_rule']='Keep the previously chosen model1/2/3. Negotiations may change safeguards/endorsements within that model; resubmit by decision after90d. Changing the model requires a separate constitutional-reversal process, not free focus reset.'
    ballot['eligible_slots']={
      'ordinary':[0,1,2,3],
      'conditional':{'4':'Only after a legal revolutionary-party participation settlement','5':'civic_legal_5','19':'civic_legal_19','22':'Only an actually formed legal DJP electoral vehicle; an Army institution alone is not a ballot party'},
      'excluded':'KCIA7, EPB13 and non-party association slots are not independently counted as ballot parties. Native banned parties are excluded.'}
    ballot['denominator']='Sum party_pop_array^s for every currently eligible, non-banned electoral party, whether endorsing or opposing. Endorsement membership is a subset, never the whole denominator by definition.'
    ballot['supporter_membership']='Unique charter_supporter_s flags are set only by accepted, recorded party endorsement. Iterate each eligible slot once; sum its current native popularity only when that receipt is present.'
    ballot['zero_denominator']='Support share remains0 and the vote is rejected/postponed with a data/eligibility diagnostic in the review log. Never divide by zero, fabricate an electorate or grant automatic passage.'
    lines=['set_temp_variable = { '+P+'charter_support = 0 }','set_temp_variable = { '+P+'charter_electorate = 0 }']
    for s in (0,1,2,3,4,5,19,22):
        eligibility=[]
        if s in (4,22):eligibility=['has_country_flag = '+P+'electoral_party_'+str(s)+'_legal']
        if s in (5,19):eligibility=['has_country_flag = '+P+'civic_legal_'+str(s)]
        eligibility+=['check_variable = { party_banned_array^'+str(s)+' = 0 }']
        lines += ['if = {','  limit = { '+' '.join(eligibility)+' }',
          '  add_to_temp_variable = { '+P+'charter_electorate = party_pop_array^'+str(s)+' }',
          '  if = { limit = { has_country_flag = '+P+'charter_supporter_'+str(s)+' } add_to_temp_variable = { '+P+'charter_support = party_pop_array^'+str(s)+' } }','}']
    lines += ['set_variable = { '+P+'charter_support_share = 0 }',
      'if = { limit = { check_variable = { '+P+'charter_electorate > 0 } } set_variable = { '+P+'charter_support_share = { value = '+P+'charter_support divide = '+P+'charter_electorate clamp = { min = 0 max = 1 } } } }']
    ballot['native_calculation']='\n'.join(lines)
    d['proposed_transition_events']={
      'COLDWAR_KOR_transition.12':{
        'trigger':'has_country_flag = '+P+'command_settlement_pending',
        'success':'Set negotiating_commitment; clear command_settlement_pending; legitimate civilian command continues.',
        'failure':'Set military_reconsolidation and90d talks_retry_cooldown; clear command_settlement_pending, negotiating_commitment and caretaker_installed; record command burden. A separate actual office event installs a military president; reopening requires the actual military-led government and registered opposition demand.'},
      'COLDWAR_KOR_transition.30':{
        'trigger':'has_country_flag = '+P+'ballot_pending\nhas_country_flag = '+P+'charter_mandate',
        'immediate':'Run NEW '+P+'calculate_charter_vote using the exact native calculation in ratification.native_calculation.',
        'pass_guard':'check_variable = { '+P+'charter_support_share > 0.5 }',
        'pass':'Set constitutional_ratification_passed and the selected model’s constitution receipt; clear pending/rejected. No incumbent appointment. Election-board implementation remains required.',
        'reject':'Clear ballot_pending; set charter_rejected and a90d charter_retry_cooldown; retain chosen model. No constitutional modifiers or election grant. Resubmit only through reopen_charter_ballot.'},
      'COLDWAR_KOR_transition.88':{
        'trigger':'has_country_flag = '+P+'judicial_review\nhas_country_flag = '+P+'constitutional_order\nhas_country_flag = '+P+'court_appointments_implemented\nhas_country_flag = '+P+'court_implementation_pending\nNOT = { has_country_flag = '+P+'court_commissioning_delay }',
        'effect':'set_country_flag = '+P+'judicial_review_operational\nclr_country_flag = '+P+'court_implementation_pending',
        'historicity':'The constitutional creation in1987 and operational court in1988 are distinct. An earlier alternative still needs appointments/implementation; no automatic court operational at draft approval.'},
    }
    d['transition_maintenance_recipe']='if = { limit = { has_country_flag = '+P+'constitutional_order has_country_flag = '+P+'judicial_review has_country_flag = '+P+'court_appointments_implemented has_country_flag = '+P+'court_implementation_pending NOT = { has_country_flag = '+P+'court_commissioning_delay } } country_event = { id = COLDWAR_KOR_transition.88 days = 1 } }'
    d['transition_maintenance_note']='Run from the monthly KOR synchronization and constitutional restoration hook. This resumes an already funded, matured court commissioning after emergency interruption; the cleared pending receipt prevents repeated operation or payment.'
    d['refusal_routes']['graph']='298 focus cards; native bypass is separate from guarded completion rewards.'
    command=d['proposed_transition_events']['COLDWAR_KOR_transition.12']
    command['success_option_guard']='has_country_flag = '+P+'caretaker_installed\nNOT = { has_country_flag = '+P+'nationwide_martial_law }'
    command['success_native']='add_political_power = -75\nset_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nadd_timed_idea = { idea = '+P+'command_reorganization days = 90 }\nset_country_flag = '+P+'negotiating_commitment\nclr_country_flag = '+P+'command_settlement_pending'
    command['failure_native']='add_political_power = -25\nset_country_flag = '+P+'military_reconsolidation\nset_country_flag = { flag = '+P+'talks_retry_cooldown days = 90 }\nclr_country_flag = '+P+'command_settlement_pending\nclr_country_flag = '+P+'negotiating_commitment\nclr_country_flag = '+P+'caretaker_installed\nclr_country_flag = '+P+'transition_open\nclr_country_flag = '+P+'military_opening_authorized'
    command['success_cost']='75PP and $1bn once;90d command reorganization: army organization -5%, political power gain -5%. No new president is installed.'
    command['resolution_mode']='Player-facing internal command-resolution event. Reorganize and Uphold Civil Command purchases a costly alternate outcome under the actual caretaker; Yield the Command records failure. These options resolve the challenge itself. No hidden dice, external success receipt or invented command meter is assumed.'
    d['proposed_temporary_ideas']={P+'command_reorganization':{'army_org_factor':-0.05,'political_power_factor':-0.05}}
    vote=d['proposed_transition_events']['COLDWAR_KOR_transition.30']
    vote['trigger']+='\ncheck_variable = { '+P+'charter_model > 0 }\ncheck_variable = { '+P+'charter_model < 4 }'
    vote['pass_native']='set_country_flag = '+P+'constitutional_ratification_passed\nclr_country_flag = '+P+'ballot_pending\nclr_country_flag = '+P+'charter_rejected'
    for i,model in enumerate(('presidential','parliamentary','consensus'),1):
        vote['pass_native']+='\nif = { limit = { check_variable = { '+P+'charter_model = '+str(i)+' } } set_country_flag = '+P+'constitution_'+model+' }'
    vote['reject_native']='clr_country_flag = '+P+'ballot_pending\nset_country_flag = '+P+'charter_rejected\nset_country_flag = { flag = '+P+'charter_retry_cooldown days = 90 }'
    vote['implementation']='After the immediate calculation, execute one guarded pass/reject branch once. This is an adjudicated support model, not a player option that can choose passage against the result.'
    # The command focus sends a resolution event and cannot itself claim victory.
    ns['defend_civil_command']['state_effects'].append('country_event = { id = COLDWAR_KOR_transition.12 days = 1 }')
    ns['constitution_referendum']['state_effects'] += ['set_country_flag = '+P+'ballot_pending','country_event = { id = COLDWAR_KOR_transition.30 days = 30 }']
    for key in ('one_term_presidency','cabinet_responsibility','coalition_veto_rules'):
        ns[key]['requirements'].append('The chosen model remains a draft until the actual ratification event passes')
    # A referendum cannot queue twice while its pending receipt is active.
    ns['constitution_referendum']['condition_code'].append('NOT = { has_country_flag = '+P+'ballot_pending }')
    # National legal rules remove emergency-policy receipts at implementation.
    ns['impartial_election_board']['state_effects'] += [
      'clr_country_flag = '+P+'constitution_yushin','clr_country_flag = '+P+'constitution_controlled_fifth',
      'clr_country_flag = '+P+'nationwide_martial_law']
    d['actions']['ballot_and_reopening']={'ids':['reopen_constitutional_talks','reopen_charter_ballot','register_charter_endorsement'],
      'design':'Use transition_decisions and proposed_transition_events. No reset of completed focuses or free model/leader change.'}
    d['actions']['institution_providers']={'ids':['configure_lawful_election','register_charter_participants','submit_constitutional_ballot','resolve_command_challenge','open_constitutional_dossier'],
      'design':'Read the exact provider/decision/event table. Dossier opens legal negotiation routes; endorsement uses actual eligible parties; command and ballot events resolve before their receipts are granted.'}

    # Event outcomes are explicitly connected to the three focus-entry flags.
    for e in d['transition_events']:
        if e['id']==P+'transition_1990':e['choices'][0]['state_effects']=['set_country_flag = '+P+'conservative_merger_ratified']
        if e['id']==P+'transition_1985':e['choices'][0]['state_effects']=['set_country_flag = '+P+'opposition_constitutional_demand']
        if e['id']==P+'transition_1971':e['choices'][0]['state_effects']=['set_country_flag = '+P+'electoral_opening']
        if e['id']==P+'transition_1979':e['choices'][0]['provider']=P+'install_interim_choi'
        if e['id']==P+'transition_1987':
            e['historical_context']='Park Jong-cheol’s torture death and exposure, the13April constitutional-defense measure, Lee Han-yeol’s9June injury and the June10–26 mobilization preceded Roh’s29June concession. The concession opened negotiations; it did not itself ratify the constitution or predetermine the winner.'
            e['choices'][0]['state_effects']=['set_country_flag = '+P+'military_opening_authorized']
            e['choices'][0]['effects']='Authorize constitutional negotiations and the direct-election principle; PP -75. Actual ratification/election follows the shared transition. No automatic democracy or Roh appointment.'
        if e['id']==P+'transition_gwangju':
            e['trigger']='After a separately resolved17May nationwide martial-law expansion and actual violent suppression, historical18–27May1980; never the12December1979 coup itself'
            e['historical_context']='The18–27May Gwangju uprising and suppression are separate from the17May emergency measures and the earlier officer coup. Preserve case evidence and the lasting accountability claim.'
    # Separate labor and mobilization receipts preserve chronology across reform.
    d['transition_events']=[e for e in d['transition_events'] if e['id']!=P+'transition_labour']
    def history_event(suffix,label,date,context,trigger,choices,receipt):
        return {'id':P+suffix,'label':label,'historical_date':date,'historical_context':context,'trigger':trigger,
          'choices':[{'label':name,'effects':effect} for name,effect in choices],'history_receipt':receipt,
          'replay_rule':'Once for this actual historical/equivalent crisis. Never erase another stage or replay material rewards on cabinet change.'}
    d['transition_events'] += [
      history_event('labour_1970','Labour Law and Enforcement','1970-11-13',
        'Jeon Tae-il’s protest exposed dangerous working conditions and the failure to enforce existing protections. A tragedy is not a beneficial policy action.',
        'Historical date and an actual unresolved workplace-rights crisis, or a separately named earlier equivalent',
        [('Enforce Existing Protections','Create lawful inspection/mediation process; bureaucracy expenses +3%; no automatic universal insurance.'),('Retain Wage Discipline','Retain the actual export/labor policy and its legitimacy costs; no reward from a death.')],P+'labour_1970_recorded'),
      history_event('yh_1979','YH and the Parliamentary Opposition','1979-08-11',
        'The YH workers’ sit-in and police raid connected workplace grievances to NDP politics; they are not the same event as the later mass labor surge.',
        'An actual export-firm labor dispute and opposition crisis; historical1979 reference',
        [('Accept Workplace Mediation','Authorize mediation and preserve records; do not install an opposition government.'),('Clear the Political Occupation','Record repression/rights consequences and unresolved grievances; no positive stability gift.')],P+'yh_case_recorded'),
      history_event('buma_1979','The Busan–Masan Crisis','1979-10-16',
        'Regional mass protest followed the exclusion of Kim Young-sam and the escalating late-Yushin crisis.',
        'Actual Yushin/political exclusion crisis, or a separately framed alternate crisis',
        [('Open a Political Channel','Authorize an early negotiated opening; no automatic successor.'),('Maintain Emergency Rule','Retain emergency controls and their actual costs; preserve the crisis record.')],P+'buma_crisis_recorded'),
      history_event('martial_law_may17','The Nationwide Martial-Law Decision','1980-05-17',
        'The17May extension, political arrests and Assembly closure preceded the18–27May Gwangju events.',
        'A resolved officer-control crisis with an actual decision on renewed emergency rule',
        [('Continue Civilian Talks','Keep the civilian negotiating window open.'),('Extend Nationwide Martial Law','Set nationwide_martial_law; political activity is restricted and the legitimacy burden remains; no free civil-democratic rights.')],P+'may17_decision_recorded'),
      history_event('park_jongcheol_1987','Torture, Disclosure and Accountability','1987-01-14',
        'Park Jong-cheol died under police torture; disclosure and the attempted cover-up became central to the1987 crisis.',
        'A recorded state-abuse/disclosure crisis; use generic naming for alternate earlier cases',
        [('Protect the Investigation','Preserve evidence and support an independent inquiry.'),('Suppress Disclosure','Record continuing rights and credibility costs; do not delete the case on a later government change.')],P+'torture_disclosure_recorded'),
      history_event('april13_1987','Constitutional Defense or Revision','1987-04-13',
        'Chun’s13April measure deferred constitutional revision and fueled the demand to end indirect selection.',
        'Actual military-led government facing a constitutional demand',
        [('Accept Revision Talks','Authorize military_opening_authorized after a real government agreement.'),('Defend Indirect Selection','Keep the existing rule, opposition campaign and costs; reopening talks later remains possible.')],P+'april13_position_recorded'),
      history_event('june_movement_1987','The June Democracy Movement','1987-06-10',
        'Lee Han-yeol was injured on9June and died on5July. The June10 rally, June18 protest and June26 march preceded the29June declaration.',
        'Actual constitutional mobilization; earlier negotiated alternatives do not fabricate these dated casualties',
        [('Authorize a Negotiating Mandate','Open the shared constitutional process under an accepted public mandate.'),('Refuse the Demand','Keep the political crisis and its costs. No date automatically resolves it.')],P+'june_mobilization_recorded'),
      history_event('eight_member_talks','The Constitutional Bargain','1987-08-31',
        'The eight-member ruling/opposition talks and Assembly process produced the agreed text submitted to voters in October.',
        'Real charter mandate, chosen model and actual party endorsements',
        [('Submit the Agreed Text','Use the30-day ratification event; no guaranteed approval.'),('Return to Negotiation','Preserve the chosen model; renegotiate endorsements and safeguards without focus reset.')],P+'charter_negotiations_recorded'),
      history_event('workers_1987','The Great Workers’ Struggle','1987-07-01',
        'The post-June labor upsurge was a distinct organizing wave, especially in heavy industry; constitutional reform did not settle every workplace demand.',
        'An actual post-opening workplace-organizing wave; not erased by the1970 or1979 labor response',
        [('Recognize Lawful Bargaining','Register the actual native labor faction if needed; preserve existing opinion and negotiate enforceable terms.'),('Restrict the New Unions','Record the separate industrial and rights dispute; previous labor milestones remain historical receipts.')],P+'workers_1987_recorded'),
      history_event('court_1988','Constitutional Review Becomes Operational','1988-09-01',
        'The court’s creation in the1987 constitution and its1988 operational beginning are separate institutional stages.',
        'Court legal basis enacted, appointments/implementation completed and constitutional order active; earlier operation is alternate history',
        [('Commence Judicial Review','Run the already funded implementation event only with court_appointments_implemented and court_implementation_pending; activate the actual court reader once.'),('Delay Appointments','Retain the legal mandate but do not grant an operational court or its modifier.')],P+'court_operational_recorded'),
    ]
    for e in d['transition_events']:
        e.setdefault('historical_date',{'transition_1971':'1971-04-27','transition_1979':'1979-10-26','transition_officers':'1979-12-12','transition_gwangju':'1980-05-18','transition_1985':'1985-02-12','transition_1987':'1987-06-29','transition_1990':'1990-01-22'}.get(e['id'].removeprefix(P),'1990-12-31'))
    d['transition_events'].sort(key=lambda e:e['historical_date'])
    d['transition_system']['event_history']='Separate1970 labor,1979 YH/Bu-Ma,1979 succession,12.12 command coup,17May emergency rule,18–27May Gwangju,1985 NKDP,1987 torture/4.13/June/6.29/eight-member negotiation,1987 labor surge and1988 court operation receipts. A reform never erases later chronology.'
    d['transition_system']['court_reader']+=' Operational review additionally requires judicial_review_operational, not merely a completed founding focus.'
    # Readable narrative spacing; identifiers and native bodies stay literal.
    import re
    narrative={'description','history','historicity','historical_context','resolution','effects'}
    def prose(obj):
        if isinstance(obj,dict):
            for key,value in obj.items():
                if key in narrative and isinstance(value,str):obj[key]=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', value)
                elif key=='requirements' and isinstance(value,list):obj[key]=[re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', v) for v in value]
                elif isinstance(value,(dict,list)):prose(value)
        elif isinstance(obj,list):
            for value in obj:prose(value)
    prose(d['nodes']);prose(d['starting_spirits']);prose(d['transition_events'])
    d['rules']['balance']='Persistent policies replace owner-qualified slots. Mature cross-sector examples are documented in balance_expansion_review.md; they are not guaranteed national output or solvency. Interest adjustments add percentage points before native clamps. Bureaucracy cost modifiers multiply only the bureaucracy spending category; civilian productivity affects its civilian-industrial tax/GDP component. Weekly commitments add to department costs and one-time capital costs. No hidden aggregate cap is assumed.'
    return d
