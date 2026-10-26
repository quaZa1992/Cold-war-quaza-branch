# IMPERIA CW — Cold War: cyprus 1970 — runtime.
"""Native runtime: funded outcomes, independently evaluated offers and passive MP hooks."""

def generate_runtime(c):
    for key in ('P','ROOT','HERE','D','NODES','BY','EFFECTS','TRIGGERS','LOC','EVENTS','DECISIONS','FOREIGN_DECISIONS','FOREIGN','LOANS','GUARANTOR_TOPICS','COMMUNITY','OBSERVED','REACTIVE','EXTRA',
                'block','cond','indent','write','loc','fid','flag','setflag','clrflag','effect','ge','le','party','allowed_controller','conditions','cost','amount_key','effective_cost','recalc_cost','afford_current','pay_cost','base_payload'):
        globals()[key]=getattr(c,key)
    make_core();make_relief();make_leaders();make_nodes();make_decisions();make_hooks()

def addvar(key,value):return f'add_to_variable = {{ {fid(key)} = {value:g} }}\nclamp_variable = {{ var = {fid(key)} min = 0 max = 100 }}'
def remove_ideas(*keys):return '\n'.join('remove_ideas = '+fid(k) for k in keys)
def dm_remove(state,*keys):return block(str(state),'\n'.join('remove_dynamic_modifier = { modifier = '+fid(k)+' }' for k in keys))
def dm_add(state,key):return block(str(state),'add_dynamic_modifier = { modifier = '+fid(key)+' }')
def event(number,title,desc,options,trigger='original_tag = CYP\nIMP_is_1970_scenario = yes'):
    key=f'COLDWAR_CYP_1970.{number}'
    titlekey=loc(fid('event_'+str(number)+'_title'),title);desckey=loc(fid('event_'+str(number)+'_desc'),desc)
    body=f'id = {key}\ntitle = {titlekey}\ndesc = {desckey}\nis_triggered_only = yes\n'+block('trigger',trigger)
    for label,payload,test,weight in options:
        optkey=loc(fid('event_'+str(number)+'_option_'+str(len(LOC))),label)
        b='name = '+optkey
        if test:b+='\n'+block('trigger',test)
        b+='\n'+block('ai_chance',f'base = {weight}')
        b+='\n'+payload
        body+='\n'+block('option',b)
    EVENTS.append(block('country_event',body))
    return key

def make_core():
    cache=[]
    for v in sorted(set(effective_cost(n) for n in NODES if effective_cost(n))):
        key=fid('cost_'+str(round(v*100)).zfill(3))
        cache += [f'set_variable = {{ {key} = gdp_total }}',f'multiply_variable = {{ {key} = {v/100:g} }}']
    effect('refresh_budget','\n'.join(cache))
    init=[
        'load_focus_tree = '+fid('focus'),setflag('initialized'),
        f'set_variable = {{ {fid("communal_tension")} = 55 }}',
        f'set_variable = {{ {fid("settlement_progress")} = 10 }}',
        f'set_variable = {{ {fid("coup_pressure")} = 45 }}',
        f'set_variable = {{ {fid("party_reform_credit")} = 0 }}',
        f'set_variable = {{ {fid("relief_stage")} = 0 }}',
        f'set_variable = {{ {fid("crisis_instance")} = 0 }}',
        cond('is_ai = no',setflag('human_seat_reserved'),
            cond('has_game_rule = { rule = '+fid('seat_policy')+' option = HISTORICAL_AI }',
                setflag('dedicated_historical_ai'),setflag('human_seat_reserved'))),
    ]
    for s in D['starting_spirits']:
        if s['activation']!='start':continue
        if s['scope'].startswith('state '):init.append(dm_add(int(s['scope'].split()[-1]),s['id'][len(P):]))
        else:init.append('add_ideas = '+s['id'])
    for p in D['parties']:
        for k in sorted({k for n in NODES if n['party']==p['index'] for k in n['modifiers']}):
            init.append(f'set_variable = {{ {fid("p"+str(p["index"])+"_"+k)} = 0 }}')
    init += [fid('refresh_budget')+' = yes']
    for target in sorted({t for ts in FOREIGN.values() for t in ts}):
        init.append(block(target,setflag('human_seat_reserved')))
    effect('initialize',cond('original_tag = CYP\nIMP_is_1970_scenario = yes\nNOT = { '+flag('initialized')+' }','\n'.join(init)))
    loc(fid('seat_policy'),'Cyprus 1970: Player Seat')
    loc(fid('seat_ai'),'Dedicated Historical AI')
    loc(fid('seat_ai_desc'),'An unselected Cyprus follows its historical government policy. Selecting Cyprus as a human country reserves the human seat instead.')
    loc(fid('seat_human'),'Reserve for a Human Player')
    loc(fid('seat_human_desc'),'Reserve Cyprus even before its player joins. Temporary AI control cannot select the scenario\'s political choices. Pause before changing player seats.')
    write('common/game_rules/COLDWAR_CYP_1970_rules.txt',block(fid('seat_policy'),
        'name = '+fid('seat_policy')+'\ngroup = MD_AI_RULES\n'+
        block('default','name = HISTORICAL_AI\ntext = '+fid('seat_ai')+'\ndesc = '+fid('seat_ai_desc'))+'\n'+
        block('option','name = RESERVED_HUMAN\ntext = '+fid('seat_human')+'\ndesc = '+fid('seat_human_desc')))+'\n')
    begin=[setflag('crisis_active'),clrflag('final_settlement_implemented'),clrflag('geneva_failed'),
           f'add_to_variable = {{ {fid("crisis_instance")} = 1 }}',f'set_variable = {{ {fid("current_substantive_replies")} = 0 }}']
    for f in ('first_intervention_phase','ultimatum_active','intervention_threat','ultimatum_rejected','settlement_talks_open','cypriot_remobilisation',
              'guarantor_response_recorded','coup_attempt_resolved','constitutional_government_restored','renewed_hostilities_decided','second_phase_combat'):
        begin.append(clrflag(f))
    for k in sorted(REACTIVE):
        begin += [clrflag('registered_'+k),clrflag('applied_'+k),clrflag('pending_completion_'+k)]
    for t in ('GRE','TUR','ENG'):begin.append(clrflag('current_reply_'+t))
    for t in ('GRE','TUR','ENG'):begin.append(clrflag('talks_withdrawn_'+t))
    effect('begin_crisis',cond('NOT = { '+flag('crisis_active')+' }','\n'.join(begin)))
    for target in ('GRE','TUR','ENG'):
        effect('record_'+target+'_response',cond(flag('crisis_active')+'\nNOT = { '+flag('current_reply_'+target)+' }',
            setflag('current_reply_'+target)+'\n'+addvar('current_substantive_replies',1)+'\n'+setflag('guarantor_response_recorded')))
        # Actor-owned entry point. Never calls a foreign action on behalf of CYP.
        effect(target+'_publish_response',cond('original_tag = '+target+'\nis_ai = no\nCYP = { exists = yes IMP_is_1970_scenario = yes '+flag('crisis_active')+' }',
            block('CYP',fid('record_'+target+'_response')+' = yes')))
    harms=[setflag('unresolved_reprisals'),setflag('grave_renewed_communal_violence'),setflag('displacement_active'),fid('begin_crisis')+' = yes',
           clrflag('tc_community_assent'),clrflag('tc_enosis_assent'),clrflag('constitutional_package_accepted'),clrflag('federal_terms_accepted'),clrflag('unitary_terms_accepted'),
           'add_ideas = '+fid('displacement_emergency'),
           'set_temp_variable = { mdcw_cw_tension_delta = 2 }','mdcw_cw_add_tension = yes']
    for state in (145,146):
        harms.append(block(str(state),cond('is_owned_by = CYP\nis_controlled_by = CYP','add_dynamic_modifier = { modifier = '+fid('shattered_communities')+' }')))
    effect('civilian_harm','\n'.join(harms))
    # Framework callbacks are factual records, not a political/war simulator.
    effect('record_coup_attempt',fid('begin_crisis')+' = yes\n'+setflag('coup_attempt_resolved'))
    effect('record_restoration',setflag('constitutional_government_restored')+'\n'+clrflag('coup_regime_active'))
    effect('restore_civilian_authority',
        'set_temp_variable = { rul_party_temp = 2 }\nset_temp_variable = { disable_elections = 0 }\nchange_ruling_party_effect = yes\n'+
        setflag('acting_clerides')+'\n'+cond('date > 1973.12.31\ndate < 1974.12.7\nNOT = { '+flag('makarios_deceased')+' }',setflag('makarios_return_context'))+'\n'+fid('record_restoration')+' = yes')
    effect('update_displacement_recovery',cond(flag('applied_reconstruction')+'\n'+flag('restitution_implemented')+'\n'+flag('final_settlement_implemented')+'\nNOT = { '+flag('unresolved_reprisals')+' }',
        remove_ideas('displacement_emergency')+'\n'+clrflag('displacement_active')))
    effect('record_settlement',cond('original_tag = CYP\nIMP_is_1970_scenario = yes\nhas_war = no\n'+flag('tc_community_assent')+'\nNOT = { '+flag('unresolved_reprisals')+' }',
        setflag('final_settlement_implemented')+'\n'+clrflag('grave_renewed_communal_violence')+'\n'+clrflag('crisis_active')+'\n'+fid('update_displacement_recovery')+' = yes'))
    effect('TUR_record_ultimatum',cond('original_tag = TUR\nis_ai = no\nCYP = { exists = yes IMP_is_1970_scenario = yes '+flag('crisis_active')+' }',
        block('CYP',setflag('ultimatum_active')+'\n'+setflag('intervention_threat')+'\n'+fid('record_TUR_response')+' = yes')))
    effect('TUR_record_renewed_hostilities_decision',cond('original_tag = TUR\nis_ai = no\nCYP = { exists = yes IMP_is_1970_scenario = yes '+flag('crisis_active')+' '+flag('first_intervention_phase')+' '+flag('geneva_failed')+' NOT = { '+flag('final_settlement_implemented')+' } }',
        block('CYP',setflag('renewed_hostilities_decided')+'\n'+fid('record_TUR_response')+' = yes\n'+fid('sync_milestones')+' = yes')))
    for actor in ('GRE','TUR','ENG'):
        withdrawal=setflag('talks_withdrawn_'+actor)+'\n'+clrflag('reply_'+actor+'_war_geneva')+'\n'+fid('record_'+actor+'_response')+' = yes'
        if actor=='TUR':withdrawal+='\n'+setflag('geneva_failed')+'\n'+clrflag('settlement_talks_open')
        effect(actor+'_withdraw_current_talks',cond('original_tag = '+actor+'\nis_ai = no\nCYP = { exists = yes IMP_is_1970_scenario = yes '+flag('crisis_active')+' '+flag('settlement_talks_open')+' '+flag('reply_'+actor+'_war_geneva')+' check_variable = { '+fid('offer_instance_war_geneva')+' = '+fid('crisis_instance')+' } NOT = { '+flag('final_settlement_implemented')+' } }',
            block('CYP',withdrawal)))
    effect('observe_turkish_war',fid('begin_crisis')+' = yes\n'+setflag('first_intervention_phase')+'\n'+fid('record_TUR_response')+' = yes')
    loc(fid('external_milestone_tt'),'This focus records a real event or a response chosen in the crisis dossier.')
    loc(fid('dossier'),'Cyprus: Communities and the Guarantors')
    loc(fid('foreign_dossier'),'Cyprus: Current Diplomatic Proposals')
    loc(fid('foreign_dossier_desc'),'Review and answer the current Cypriot proposals here. Event notices do not sign agreements. Each decision rechecks the current conditions before applying any outcome. Silence leaves a proposal unanswered until it expires.')
    loc(fid('dossier_desc'),'Communal tension: [?'+fid('communal_tension')+'|0]/100\\nSettlement progress: [?'+fid('settlement_progress')+'|0]/100\\nCoup pressure: [?'+fid('coup_pressure')+'|0]/100\\nCurrent crisis: [?'+fid('crisis_instance')+'|0] — substantive guarantor responses: [?'+fid('current_substantive_replies')+'|0]/3.\\nHistorical focus markers remain complete; current offers and responses are recorded separately.')
    event(1,'A Programme Awaits Funding','The programme has reached its completion date, but its current treasury requirement or implementation conditions are not met. Its benefits have been withheld. The crisis dossier allows the administration to fund eligible outstanding programmes once conditions permit.',
          [('Review the outstanding programme.', '', '',100)])
    enosis=BY['enosis_agreement']
    union_guard=conditions(enosis)+'\nis_ai = no\n'+flag('applied_enosis_agreement')+'\nNOT = { '+flag('enosis_implemented')+' '+flag('unresolved_reprisals')+' '+flag('declined_enosis_agreement')+' }\n'+\
        '\n'.join(flag('reply_'+t+'_enosis_agreement') for t in ('GRE','TUR','ENG'))+'\ncheck_variable = { '+fid('offer_instance_enosis_agreement')+' = '+fid('crisis_instance')+' }'
    event(4000,'Final Ratification of Union','Greece, Turkey, Britain and the communal representatives have accepted the negotiated framework. Ratifying now transfers every territory currently owned by Cyprus to Greece and ends independent Cypriot play. British-owned bases are not transferred by this act. This cannot be reversed by cancelling a focus.',
          [('Ratify the union and end independent Cypriot government.',cond(union_guard,setflag('enosis_implemented')+'\nGRE = { annex_country = { target = CYP transfer_troops = yes } }'),union_guard,0),
           ('Withhold final ratification.','', '',100)])
    decision('restore_authority','Restore Constitutional Authority','End the coup presidency and appoint Glafkos Clerides as acting constitutional president. This is a Cypriot decision; it neither commands foreign withdrawal nor ends an engine war.',
        flag('coup_regime_active')+'\n'+allowed_controller(),fid('restore_civilian_authority')+' = yes',flag('coup_regime_active'))
    decision('review_ratification','Review Final Ratification of Union','Reopen the final ratification. The agreed framework and all current conditions are checked again. Confirming ends independent Cypriot play.',
        union_guard,'country_event = { id = COLDWAR_CYP_1970.4000 days = 1 }',flag('applied_enosis_agreement')+'\nNOT = { '+flag('enosis_implemented')+' }')

def make_relief():
    all_south=['restricted_movement_south','access_south_1']
    all_north=['restricted_movement_north','access_north_1','access_north_2']
    for stage in (1,2,3):
        body=[remove_ideas('tc_parallel_administration','admin_stage_1','admin_stage_2')]
        for state,keys in ((145,all_south),(146,all_north)):
            body.append(block(str(state),cond('is_owned_by = CYP\nis_controlled_by = CYP','\n'.join('remove_dynamic_modifier = { modifier = '+fid(k)+' }' for k in keys))))
        if stage==1:body += [dm_add(145,'access_south_1'),dm_add(146,'access_north_1'),'add_ideas = '+fid('admin_stage_1')]
        if stage==2:body += [dm_add(146,'access_north_2'),'add_ideas = '+fid('admin_stage_2')]
        if stage==3:
            body += [remove_ideas('joint_services_idea','checkpoint_leverage_idea','tc_pressure_idea','tc_police_idea','tc_unilateral_resolution_idea'),clrflag('tc_terms_rejected')]
        body += [f'set_variable = {{ {fid("relief_stage")} = {stage} }}',setflag('civilian_access_implemented')]
        effect('relief_'+str(stage),cond(f'check_variable = {{ {fid("relief_stage")} < {stage} }}\nowns_state = 145\ncontrols_state = 145\nowns_state = 146\ncontrols_state = 146','\n'.join(body)))

def make_leaders():
    # Unnamed alternate administrations use an institutional emblem, never an
    # unrelated person's face. Named leaders always require verified assets.
    generic='gfx/leaders/NCY/1970/COLDWAR_NCY_1970_generic.dds'
    assert (ROOT/generic).is_file(),'Missing institutional Cyprus emblem'
    import json
    portrait_assets=json.loads((HERE/'portraits/assets.json').read_text(encoding='utf-8'))['portraits']
    regional_assets=json.loads((ROOT/'tools/eastern_mediterranean_1970/CYP/assets.json').read_text(encoding='utf-8'))['assets']
    for key in ('makarios','clerides'):
        portrait_assets[key]=regional_assets['CYP_'+key]
    def portrait(key):
        path=portrait_assets[key]['portrait']
        assert (ROOT/path).is_file(),'Missing Cyprus portrait '+path
        return path
    roster={1:('Makarios III','conservatism',portrait('makarios')),
            2:('Glafkos Clerides','liberalism',portrait('clerides')),
            3:('Vassos Lyssarides','socialism',portrait('lyssarides')),4:('Ezekias Papaioannou','communist_state',portrait('papaioannou')),
            20:('Nikos Sampson','Nat_Populism',portrait('sampson')),21:('Georgios Grivas','Nat_Fascism',portrait('grivas')),
            22:('Nikos Sampson','Nat_Autocracy',portrait('sampson'))}
    # Use the actual index mapping from the existing political trigger registry.
    ideos=['Western_Autocracy','conservatism','liberalism','socialism','communist_state','anarchist_communism','Conservative','Autocracy',
           'Mod_Vilayat_e_Faqih','Vilayat_e_Faqih','Kingdom','Caliphate','Neutral_Muslim_Brotherhood','Neutral_Autocracy','Neutral_conservatism',
           'oligarchism','Neutral_Libertarian','Neutral_green','neutral_Social','Neutral_Communism','Nat_Populism','Nat_Fascism','Nat_Autocracy','Monarchist']
    parts=['update_set_politics = yes']
    for idx in range(24):
        name,ideology,pic=roster.get(idx,('Cypriot National Administration',ideos[idx],generic))
        create=f'create_country_leader = {{ name = "{name}" picture = "{pic}" expire = "2000.1.1" ideology = {ideology} }}'
        if idx==21:
            create=cond('date > 1974.1.26',f'create_country_leader = {{ name = "Nikos Sampson" picture = "{portrait("sampson")}" expire = "2000.1.1" ideology = Nat_Fascism }}',create)
        if idx==1:
            successor=f'create_country_leader = {{ name = "Spyros Kyprianou" picture = "{portrait("kyprianou")}" expire = "2000.1.1" ideology = conservatism }}'
            create=cond(flag('makarios_deceased'),successor,create)
        parts.append(('if' if idx==0 else 'else_if')+' = {\n'+indent('limit = { check_variable = { ruling_party = '+str(idx)+' } }\n'+create)+'\n}')
    parts += [f'set_variable = {{ {fid("leader_party")} = ruling_party }}',setflag('portraits_v1'),setflag('portraits_v2'),fid('sync_makarios_spirit')+' = yes']
    effect('set_leader','\n'.join(parts))
    effect('sync_makarios_spirit',cond('check_variable = { ruling_party = 1 }\nNOT = { '+flag('makarios_deceased')+' }\nNOT = { '+flag('coup_regime_active')+' }',
        cond('NOT = { has_idea = '+fid('makarios_authority')+' }','add_ideas = '+fid('makarios_authority')),
        'remove_ideas = '+fid('makarios_authority')))
    # Named historical leaders have real photo-based assets; generic art remains
    # only for unnamed minor alternate administrations outside the main routes.
    named={name:pic for name,ideology,pic in roster.values()}
    named['Spyros Kyprianou']=portrait('kyprianou')
    write('tools/cyprus_1970/leader_assets.json',json.dumps({'generic_portrait':generic,
        'historical_portraits_available':list(named),'generic_portraits_required':[],
        'portraits':named,'photo_based_ai_restorations':list(portrait_assets),
        'sources':['tools/cyprus_1970/portraits/SOURCES.md','tools/eastern_mediterranean_1970/CYP/roster_research.json']},indent=2)+'\n')

def extras(n):
    k=n['key'];lines=[]
    if k in ('safe_passage','tc_open_trade','tc_routes'):lines.append(fid('relief_1')+' = yes')
    if k in ('joint_services','tc_utilities'):lines.append(fid('relief_2')+' = yes')
    if k in ('tc_joint_budgets','tc_local_services'):
        lines += [fid('relief_3')+' = yes',setflag('joint_services_compact' if k=='tc_joint_budgets' else 'local_services_compact')]
    if k=='foreign_officers':lines += [remove_ideas('divided_command'),'add_ideas = '+fid('command_half')]
    if k=='police_oversight':lines += [remove_ideas('divided_command','command_half'),setflag('civilian_command_implemented')]
    if k in ('ban_armed_factions','war_domestic_security'):
        lines += [setflag('militias_disarmed'),addvar('coup_pressure',-10)]
    if k=='war_loyal_guard':lines += [remove_ideas('armed_enosis_opposition','divided_command','command_half'),setflag('civilian_command_implemented')]
    if k=='famagusta_port':lines.append('146 = { add_building_construction = { type = naval_base level = 1 province = 7193 instant_build = no } }')
    if k=='balanced_development':lines.append(remove_ideas('narrow_economy'))
    if k=='constitutional_settlement':
        lines += [remove_ideas('constitutional_breakdown'),fid('relief_3')+' = yes',setflag('constitution_implemented'),fid('record_settlement')+' = yes']
    if k=='independence_mandate':lines.append(setflag('independence_settled'))
    if k in ('collective_reprisals','emergency_repression'):lines.append(fid('civilian_harm')+' = yes')
    if k in ('return_and_restitution','temporary_housing'):
        lines.append(setflag('housing_implemented'))
        if k=='return_and_restitution':lines.append(setflag('restitution_implemented'))
    if k=='accountability':
        lines += [setflag('restitution_implemented'),setflag('accountability_implemented'),clrflag('unresolved_reprisals'),
                  remove_ideas('collective_reprisals_idea','emergency_repression_idea'),fid('update_displacement_recovery')+' = yes']
    if k=='reconstruction':
        for state in (145,146):
            lines.append(block(str(state),cond('is_owned_by = CYP\nis_controlled_by = CYP\nhas_dynamic_modifier = { modifier = '+fid('shattered_communities')+' }',
                'remove_dynamic_modifier = { modifier = '+fid('shattered_communities')+' }\nadd_dynamic_modifier = { modifier = '+fid('reconstruction_damage')+' }')))
        lines.append(fid('update_displacement_recovery')+' = yes')
    if k=='tc_mandate':lines.append(setflag('tc_negotiating_mandate'))
    if k in ('bicomm_constitution','tc_political_equality'):lines.append(setflag('federal_terms_accepted'))
    if k in ('unitary_constitution','tc_unitary_bargain'):lines.append(setflag('unitary_terms_accepted'))
    if k in ('tc_federal_framework','tc_shared_republic'):
        lines += [setflag('tc_community_assent'),clrflag('tc_terms_rejected'),f'set_variable = {{ {fid("constitutional_model")} = {1 if k=="tc_federal_framework" else 2} }}']
    if k=='tc_enosis_consent':lines.append(setflag('tc_enosis_assent'))
    if k in ('federal_compromise','shared_republic'):lines.append(setflag('constitutional_package_accepted'))
    if k=='base_cooperation':lines.append(setflag('bases_agreement'))
    if k=='base_sovereignty':
        lines += ['transfer_state = 812',setflag('bases_agreement')]
    if k=='guarantee_review':lines += [setflag('guarantees_revised'),remove_ideas('guarantor_pressure')]
    if k=='war_officer_agreement':lines.append(setflag('officer_withdrawal_implemented'))
    if k=='war_junta_links':lines.append(setflag('gre_sponsorship_accepted'))
    if k=='war_plot':lines.append(setflag('gre_authorized_coup'))
    if k=='war_defy':lines += [setflag('ultimatum_rejected'),clrflag('ultimatum_active')]
    if k=='war_remobilise':lines.append(setflag('cypriot_remobilisation'))
    if k=='war_geneva':lines.append(setflag('settlement_talks_open'))
    if k=='p22_second_a':lines.append(fid('restore_civilian_authority')+' = yes')
    if k=='tc_beyond_partition':lines.append(fid('record_settlement')+' = yes')
    if k in ('ceasefire_lines','war_july_ceasefire'):lines.append(setflag('ceasefire_proposal_accepted'))
    if k=='enosis_agreement':lines.append('country_event = { id = COLDWAR_CYP_1970.4000 days = 1 }')
    return '\n'.join(lines)

def community_test(n):
    k=n['key'];safe='NOT = { '+flag('unresolved_reprisals')+' }'
    normal=ge(fid('relief_stage'),1)+'\n'+safe+'\n'+le(fid('communal_tension'),60)
    if k in ('safe_passage','tc_open_trade','tc_routes','tc_utilities','tc_supervised','tc_kucuk','tc_denktash','tc_ctp'):
        return 'always = yes'
    if k in ('tc_joint_budgets','tc_local_services'):return safe+'\n'+le(fid('communal_tension'),70)
    if k in ('tc_arms_guarantees','tc_mandate'):return normal
    if k=='bicomm_constitution':return safe+'\n'+le(fid('communal_tension'),45)
    if k in ('unitary_constitution','tc_unitary_bargain'):
        return ge(fid('relief_stage'),2)+'\n'+safe+'\n'+le(fid('communal_tension'),25)
    if k=='tc_political_equality':return flag('tc_negotiating_mandate')+'\n'+normal+'\n'+le(fid('communal_tension'),45)
    if k=='tc_federal_framework':return flag('federal_terms_accepted')+'\n'+normal
    if k=='tc_shared_republic':return flag('unitary_terms_accepted')+'\n'+normal
    if k=='federal_compromise':return flag('tc_community_assent')+'\ncheck_variable = { '+fid('constitutional_model')+' = 1 }\n'+safe
    if k=='shared_republic':return flag('tc_community_assent')+'\ncheck_variable = { '+fid('constitutional_model')+' = 2 }\n'+safe
    if k=='tc_enosis_consent':return normal+'\n'+ge(fid('relief_stage'),3)+'\n'+ge(fid('settlement_progress'),90)+'\n'+le(fid('communal_tension'),15)+'\n'+flag('guarantees_revised')
    return normal

def make_nodes():
    for i,n in enumerate(NODES):
        k=n['key']
        if k in OBSERVED:continue
        # Grant is separate from registration/submission. Benefits are idempotent.
        payload=base_payload(n)+'\n'+extras(n)
        effect('grant_'+k,cond('NOT = { '+flag('applied_'+k)+' }',setflag('applied_'+k)+'\n'+payload))
        if k in FOREIGN:make_foreign(n,i)
        elif k in COMMUNITY:
            yesid=event(5000+i,n['title']+': Communal Response','The communal representatives have accepted the specified terms under the current access and security conditions. The agreed programme is now being implemented.', [('Record the agreed outcome.','','',100)])
            noid=event(6000+i,n['title']+': Terms Not Accepted','The communal representatives have not accepted these terms. Civilian access, protection from reprisals, negotiating authority and constitutional safeguards are evaluated independently of the governing party. The crisis dossier allows a renewed proposal after conditions improve.', [('Keep the negotiating channel open.','','',100)])
            # Reaffirming revoked consent can restore the actual agreement, but
            # the guarded grant never repeats money, reform credit or modifiers.
            decision=clrflag('community_pending_'+k)+'\n'+cond(conditions(n,False)+'\n'+community_test(n),fid('grant_'+k)+' = yes\n'+extras(n)+'\ncountry_event = { id = '+yesid+' days = 1 }',
                setflag('tc_terms_rejected')+'\n'+setflag('declined_'+k)+'\ncountry_event = { id = '+noid+' days = 1 }')
            # Delayed hidden resolver lets the counterpart evaluate implemented facts,
            # with deterministic criteria instead of a CYP-selected yes button.
            EVENTS.append(block('country_event',f'id = COLDWAR_CYP_1970.{3000+i}\nhidden = yes\nis_triggered_only = yes\n'+block('trigger',
                'original_tag = CYP\nIMP_is_1970_scenario = yes\n'+flag('registered_'+k)+'\n'+flag('community_pending_'+k))+'\n'+block('immediate',decision)))
            effect('send_'+k,setflag('community_pending_'+k)+f'\ncountry_event = {{ id = COLDWAR_CYP_1970.{3000+i} days = 1 }}')
        else:effect('send_'+k,fid('grant_'+k)+' = yes')
        entry=setflag('registered_'+k)+'\n'+clrflag('pending_completion_'+k)+'\n'+pay_cost(n)+'\n'+fid('send_'+k)+' = yes'
        test=conditions(n)
        if effective_cost(n):test+='\n'+afford_current(n)
        defer=setflag('pending_completion_'+k)+'\n'+setflag('programmes_pending')
        body=cond('NOT = { '+flag('registered_'+k)+' }',recalc_cost(n)+'\n'+cond(test,entry,defer))
        effect('complete_'+k,body)

def make_foreign(n,i):
    k=n['key'];targets=FOREIGN[k]
    send=[]
    for target in targets:
        send += [clrflag('reply_'+target+'_'+k),clrflag('declined_'+k),setflag('pending_'+target+'_'+k),
                 'set_country_flag = { flag = '+fid('live_'+target+'_'+k)+' days = 90 value = 1 }',
                 block(target,f'country_event = {{ id = COLDWAR_CYP_1970.{1000+i*3+targets.index(target)} days = 1 }}')]
    send += [f'set_variable = {{ {fid("offer_instance_"+k)} = {fid("crisis_instance")} }}']
    if k in LOANS:send.append(cond('NOT = { has_variable = '+fid('principal_'+k)+' }',f'set_variable = {{ {fid("principal_"+k)} = gdp_total }}\nmultiply_variable = {{ {fid("principal_"+k)} = 0.02 }}'))
    effect('send_'+k,'\n'.join(send))
    if k in ('war_conference','war_july_ceasefire'):
        EFFECTS[fid('send_'+k)]+='\n'+setflag('applied_'+k)
    for target in targets:
        num=1000+i*3+targets.index(target)
        valid=block('CYP','exists = yes\n'+flag('pending_'+target+'_'+k)+'\n'+flag('live_'+target+'_'+k)+'\n'+
                    'check_variable = { '+fid('offer_instance_'+k)+' = '+fid('crisis_instance')+' }\n'+conditions(n,False))
        choose='original_tag = '+target+'\nis_ai = no\n'+valid
        accepted=clrflag('pending_'+target+'_'+k)+'\n'+clrflag('live_'+target+'_'+k)+'\n'+setflag('reply_'+target+'_'+k)
        if target in ('GRE','TUR','ENG') and k in GUARANTOR_TOPICS:
            accepted+='\n'+cond('check_variable = { '+fid('offer_instance_'+k)+' = '+fid('crisis_instance')+' }',fid('record_'+target+'_response')+' = yes')
        all_replies='\n'.join(flag('reply_'+t+'_'+k) for t in (['TUR'] if k=='war_geneva' else targets))
        accepted+='\n'+cond(all_replies+'\nNOT = { '+flag('declined_'+k)+' }',fid('grant_'+k)+' = yes')
        transfer=''
        if k in LOANS:
            choose+='\n'+ge('treasury','CYP.'+fid('principal_'+k))
            transfer=f'set_temp_variable = {{ treasury_change = CYP.{fid("principal_"+k)} }}\nmultiply_temp_variable = {{ treasury_change = -1 }}\nmodify_treasury_effect = yes\n'
            accepted=f'set_temp_variable = {{ treasury_change = {fid("principal_"+k)} }}\nmodify_treasury_effect = yes\nset_temp_variable = {{ debt_change = {fid("principal_"+k)} }}\nmodify_debt_effect = yes\n'+accepted
        if k=='base_sovereignty':choose+='\nowns_state = 812\ncontrols_state = 812\nhas_war = no'
        if k=='war_junta_links':choose+='\nnationalist_military_junta_are_in_power = yes'
        no=clrflag('pending_'+target+'_'+k)+'\n'+clrflag('live_'+target+'_'+k)+'\n'+setflag('declined_'+k)
        if target in ('GRE','TUR','ENG') and k in GUARANTOR_TOPICS:
            no+='\n'+cond('check_variable = { '+fid('offer_instance_'+k)+' = '+fid('crisis_instance')+' }',fid('record_'+target+'_response')+' = yes')
        desc='Cyprus proposes: '+n['title']+'. An explicit response applies only to this proposal. Other guarantor channels remain open. Acknowledgement and silence provide no agreement.'
        if k in LOANS:desc+=' Acceptance transfers a loan equal to 2% of Cyprus\'s GDP at submission: your treasury pays the principal, and Cyprus receives matching treasury and debt. Funds are checked at acceptance. Repayments to your treasury require a separate agreement.'
        if k=='base_sovereignty':desc+=' Acceptance transfers sovereignty of the British Sovereign Base Areas to Cyprus. This is a territorial transfer, not merely an access agreement.'
        # Notices can remain open across renewals. They never authorize a transfer;
        # only a fresh decision in the current country-owned dossier may do so.
        decline='original_tag = '+target+'\nis_ai = no\n'+valid
        current='\nCurrent crisis: [?CYP.'+fid('crisis_instance')+'|0]. Review the live proposal before responding.'
        if k in LOANS:current+='\nFrozen principal: [?CYP.'+fid('principal_'+k)+'|Y3] billion. Renewal preserves this original principal.'
        decision('accept_'+target+'_'+k,'Accept: '+n['title'],desc+current,choose,cond(choose,transfer+block('CYP',accepted)),decline,foreign=True)
        decision('decline_'+target+'_'+k,'Decline: '+n['title'],'Decline this current proposal. Other channels remain open.'+current,decline,cond(decline,block('CYP',no)),decline,foreign=True)
        event(num,n['title'],desc+' Review and answer the current proposal in the Cyprus diplomatic decisions dossier. This notice records no consent.',[('Review the current diplomatic dossier.','', '',100)],
            'original_tag = '+target+'\n'+valid)

def decision(key,title,desc,available,payload,visible='',ai=0,foreign=False):
    loc(fid(key),title);loc(fid(key)+'_desc',desc)
    text='icon = GFX_decision_generic_political_discourse\ncost = 0\n'+block('visible',visible or 'always = yes')+'\n'+block('available',available)+'\n'+block('complete_effect',payload)+'\n'+block('ai_will_do',f'base = {ai}')
    (FOREIGN_DECISIONS if foreign else DECISIONS).append(block(fid(key),text))

def make_decisions():
    decision('fund_outstanding','Fund Outstanding Programmes','Apply eligible outstanding programme costs and benefits once. Unaffordable programmes remain pending.',
        allowed_controller(),fid('retry_pending')+' = yes',flag('programmes_pending'),10)
    retry=[clrflag('programmes_pending')]
    for n in NODES:
        if n['key'] not in OBSERVED:retry.append(cond(flag('pending_completion_'+n['key']),fid('complete_'+n['key'])+' = yes'))
    effect('retry_pending','\n'.join(retry))
    for k in sorted(REACTIVE):
        n=BY[k];test=conditions(n)+'\nNOT = { '+flag('registered_'+k)+' }'
        if cost(n):test+='\n'+cost(n)
        # Self-owned immediate actions; no foreign declaration/settlement effect.
        decision('respond_'+k,n['title'],'Choose this Cypriot response now. Other countries choose their own replies; the completed focus is a permanent historical marker.',test,
                 fid('complete_'+k)+' = yes',EXTRA.get(k,'always = yes'),2 if k in ('war_conference','war_july_ceasefire','war_geneva') else 0)
        # Explicit current-government policy table: no random human action.
        if k in ('war_conference','war_july_ceasefire','war_geneva'):
            regime='NOT = { '+flag('coup_regime_active')+' }'
        elif k in ('war_defy','war_prepare_intervention'):
            regime=flag('coup_regime_active')
        else:
            regime=flag('second_phase_combat')+'\n'+flag('geneva_failed')
        old=DECISIONS[-1]
        import re
        DECISIONS[-1]=re.sub(r'ai_will_do = \{\s*base = \d+\s*\}',
            block('ai_will_do','base = 100\n'+block('modifier','factor = 0\nNOT = { '+regime+' }')),old)
    for n in NODES:
        k=n['key']
        if k not in FOREIGN and k not in COMMUNITY:continue
        if k in OBSERVED:continue
        visible=flag('registered_'+k)
        unapplied='NOT = { '+flag('applied_'+k)+' }'
        revalidate={'bicomm_constitution':'federal_terms_accepted','tc_political_equality':'federal_terms_accepted',
                    'unitary_constitution':'unitary_terms_accepted','tc_unitary_bargain':'unitary_terms_accepted',
                    'tc_federal_framework':'tc_community_assent','tc_shared_republic':'tc_community_assent',
                    'tc_enosis_consent':'tc_enosis_assent','federal_compromise':'constitutional_package_accepted','shared_republic':'constitutional_package_accepted'}
        if k in revalidate:unapplied=block('OR',unapplied+'\nNOT = { '+flag(revalidate[k])+' }')
        if k=='enosis_agreement':unapplied=block('OR',unapplied+'\nNOT = { check_variable = { '+fid('offer_instance_'+k)+' = '+fid('crisis_instance')+' } }')
        visible+='\n'+unapplied
        test=conditions(n)+'\nNOT = { '+flag('retry_cooldown_'+k)+' }'
        if k in FOREIGN:
            test+='\n'+'\n'.join('NOT = { '+flag('live_'+t+'_'+k)+' }' for t in FOREIGN[k])
        decision('renew_'+k,'Renew: '+n['title'],'Renew the existing terms under the current conditions. This does not replay project costs or benefits. Loan principal remains fixed at its first submission; the counterpart decides again in its current diplomatic dossier.',test,
            'set_country_flag = { flag = '+fid('retry_cooldown_'+k)+' days = 60 value = 1 }\n'+fid('send_'+k)+' = yes',visible)
    loc(fid('claim_human_seat'),'Reserve Cyprus for a Human Player')
    decision('claim_human_seat','Reserve Cyprus for a Human Player','Keep political choices with the human seat during temporary AI control. Existing results remain recorded. Pause the session before changing seats.',
             'is_ai = no',setflag('human_seat_reserved')+'\n'+clrflag('dedicated_historical_ai'),'NOT = { '+flag('human_seat_reserved')+' }')

def make_hooks():
    sync=[]
    for k,observed in OBSERVED.items():
        sync.append(cond(flag(observed)+'\nNOT = { has_completed_focus = '+fid(k)+' }','complete_national_focus = '+fid(k)))
    for k in sorted(REACTIVE):
        sync.append(cond(flag('applied_'+k)+'\nNOT = { has_completed_focus = '+fid(k)+' }','complete_national_focus = '+fid(k)))
    effect('sync_milestones','\n'.join(sync))
    daily=[fid('initialize')+' = yes',fid('refresh_budget')+' = yes',
           cond('is_ai = no',setflag('human_seat_reserved')+'\n'+clrflag('dedicated_historical_ai')),
           cond('date > 1970.12.26',setflag('ctp_formed')),
           cond('date > 1977.8.2\nNOT = { '+flag('makarios_deceased')+' }',setflag('makarios_deceased')+'\nclear_variable = '+fid('leader_party')),
           cond('date > 1974.1.26\nNOT = { '+flag('grivas_deceased')+' }',setflag('grivas_deceased')+'\nclear_variable = '+fid('leader_party')),
           cond('OR = { NOT = { '+flag('portraits_v2')+' } NOT = { has_variable = '+fid('leader_party')+' } NOT = { check_variable = { '+fid('leader_party')+' = ruling_party } } }',fid('set_leader')+' = yes'),
           fid('sync_makarios_spirit')+' = yes',
           cond(flag('acting_clerides')+'\n'+flag('makarios_return_context')+'\nNOT = { '+flag('makarios_deceased')+' }\ndate > 1974.12.6\ndate < 1975.1.1\n'+flag('dedicated_historical_ai')+'\nNOT = { '+flag('human_seat_reserved')+' }\nis_ai = yes\ncheck_variable = { ruling_party = 2 }',
                'set_temp_variable = { rul_party_temp = 1 }\nset_temp_variable = { disable_elections = 0 }\nchange_ruling_party_effect = yes\n'+clrflag('acting_clerides')+'\n'+clrflag('makarios_return_context')),
           cond(flag('coup_regime_active')+'\nOR = { check_variable = { ruling_party = 20 } check_variable = { ruling_party = 21 } check_variable = { ruling_party = 22 } }\nhas_war = yes\nNOT = { '+flag('coup_recent')+' }\n'+flag('dedicated_historical_ai')+'\nNOT = { '+flag('human_seat_reserved')+' }\nis_ai = yes',fid('restore_civilian_authority')+' = yes'),
           cond('OR = { has_war = yes '+ge(fid('communal_tension'),65)+' '+flag('coup_regime_active')+' '+flag('grave_renewed_communal_violence')+' }',fid('begin_crisis')+' = yes'),
           cond(flag('coup_regime_active')+'\nhas_elections = yes\nOR = { check_variable = { ruling_party = 1 } check_variable = { ruling_party = 2 } check_variable = { ruling_party = 3 } }',fid('record_restoration')+' = yes'),
           cond('OR = { TUR = { controls_state = 146 } NCY = { exists = yes owns_state = 146 } }',setflag('actual_partition')),
           cond(flag('programmes_pending')+'\n'+allowed_controller(),fid('retry_pending')+' = yes'),
           fid('sync_milestones')+' = yes']
    # Foreign humans can recover deferred popups; temporary AI only receives standby.
    for i,n in enumerate(NODES):
        k=n['key']
        if k not in FOREIGN:continue
        for j,t in enumerate(FOREIGN[k]):
            daily.append(cond(flag('pending_'+t+'_'+k)+'\nOR = { NOT = { '+flag('live_'+t+'_'+k)+' } NOT = { check_variable = { '+fid('offer_instance_'+k)+' = '+fid('crisis_instance')+' } } }',
                clrflag('pending_'+t+'_'+k)+'\n'+clrflag('live_'+t+'_'+k)+'\n'+setflag('expired_'+k)))
            daily.append(cond(flag('pending_'+t+'_'+k)+'\n'+flag('live_'+t+'_'+k),block(t,cond(
                'is_ai = no\nNOT = { '+flag('notice_'+k)+' }',
                'set_country_flag = { flag = '+fid('notice_'+k)+' days = 7 value = 1 }\ncountry_event = { id = COLDWAR_CYP_1970.'+str(1000+i*3+j)+' days = 1 }'))))
    effect('daily_tick','\n'.join(daily))
    onstart=block('CYP',cond('exists = yes\nIMP_is_1970_scenario = yes',fid('initialize')+' = yes'))
    tick=cond('original_tag = CYP\nexists = yes\nIMP_is_1970_scenario = yes',fid('daily_tick')+' = yes')
    war=cond('ROOT = { original_tag = TUR }\nFROM = { original_tag = CYP IMP_is_1970_scenario = yes }',
             block('FROM',fid('observe_turkish_war')+' = yes\n'+fid('sync_milestones')+' = yes'))
    coup=cond('original_tag = CYP\nIMP_is_1970_scenario = yes',fid('record_coup_attempt')+' = yes\n'+cond('OR = { check_variable = { ruling_party = 20 } check_variable = { ruling_party = 21 } check_variable = { ruling_party = 22 } }',setflag('coup_regime_active')+'\nset_country_flag = { flag = '+fid('coup_recent')+' days = 8 value = 1 }')+'\n'+fid('sync_milestones')+' = yes')
    body=block('on_startup',block('effect',onstart))+'\n'+block('on_daily',block('effect',tick))+'\n'+block('on_war_relation_added',block('effect',war))+'\n'+block('on_coup_succeeded',block('effect',coup))
    write('common/on_actions/COLDWAR_CYP_1970_on_actions.txt','# IMPERIA CW — Cold War: cyprus 1970 generated content.\n## COLDWAR | Cyprus scenario observers; no forced foreign actions.\n'+block('on_actions',body)+'\n')
