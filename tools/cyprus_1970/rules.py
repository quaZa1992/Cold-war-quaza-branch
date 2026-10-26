# IMPERIA CW — Cold War: cyprus 1970 — rules.
"""Explicit runtime policy for the reviewed Cyprus design; no text-to-code inference."""
P = 'COLDWAR_CYP_1970_'

FOREIGN = {
    'greek_mission': ['GRE'], 'western_association': ['ENG'], 'soviet_trade': ['SOV'],
    'base_cooperation': ['ENG'], 'base_sovereignty': ['ENG'], 'ankara_channel': ['TUR'],
    'guarantee_review': ['GRE','TUR','ENG'], 'crisis_conference': ['GRE','TUR','ENG'],
    'enosis_agreement': ['GRE','TUR','ENG'], 'ceasefire_lines': ['TUR'],
    'p1_finance_a': ['YUG'], 'p2_finance_a': ['ENG'], 'p3_finance_b': ['YUG'],
    'p4_second_b': ['SOV'], 'p4_finance_a': ['SOV'], 'p20_economic_b': ['GRE'],
    'p22_finance_b': ['GRE'], 'tc_patron_security': ['TUR'],
    'tc_postwar_admin': ['TUR'], 'tc_returns': ['TUR'], 'tc_civilian_access': ['TUR'],
    'tc_beyond_partition': ['TUR','GRE','ENG'],
    'war_civilian_guard': ['GRE'], 'war_junta_links': ['GRE'],
    'war_officer_agreement': ['GRE'], 'war_plot': ['GRE'],
    'war_conference': ['GRE','TUR','ENG'], 'war_geneva': ['GRE','TUR','ENG'],
    'war_july_ceasefire': ['TUR'],
}
LOANS = {'p1_finance_a','p3_finance_b','p4_finance_a','p22_finance_b'}
GUARANTOR_TOPICS = {'war_civilian_guard','war_junta_links','war_officer_agreement','war_plot','war_conference','war_geneva',
                   'war_july_ceasefire','crisis_conference','guarantee_review','ceasefire_lines','enosis_agreement',
                   'tc_postwar_admin','tc_returns','tc_civilian_access','tc_beyond_partition'}
COMMUNITY = {
    'safe_passage','bicomm_constitution','unitary_constitution','federal_compromise','shared_republic',
    'tc_kucuk','tc_denktash','tc_open_trade','tc_routes','tc_utilities','tc_supervised',
    'tc_joint_budgets','tc_local_services','tc_ctp','tc_arms_guarantees','tc_mandate',
    'tc_political_equality','tc_unitary_bargain','tc_federal_framework','tc_shared_republic','tc_enosis_consent',
}
OBSERVED = {
    'war_putsch': 'coup_attempt_resolved', 'war_guarantors': 'guarantor_response_recorded',
    'war_restore': 'constitutional_government_restored', 'war_august': 'renewed_hostilities_decided',
    'war_monitored_settlement': 'final_settlement_implemented',
    'war_military_settlement': 'second_phase_combat',
}
REACTIVE = {
    'war_conference','war_defy','war_prepare_intervention','war_july_ceasefire',
    'war_geneva','war_remobilise',
}
FLEXIBLE_PAIRS = {
    frozenset(x) for x in [('war_conference','war_defy'),('war_geneva','war_remobilise'),
                          ('war_officer_agreement','war_plot'),('war_monitored_settlement','war_military_settlement')]
}

def flag(name): return 'has_country_flag = '+P+name
def ge(var,value): return f'check_variable = {{ var = {P+var} value = {value} compare = greater_than_or_equals }}'
def le(var,value): return f'NOT = {{ check_variable = {{ {P+var} > {value} }} }}'
def no_abuses(): return 'NOT = { '+flag('unresolved_reprisals')+' }'
def access(): return ge('relief_stage',1)
def assent(): return flag('tc_community_assent')
def crisis(): return flag('crisis_active')

EXTRA = {
    'coastal_hotels':'has_war = no\nOR = { controls_state = 145 controls_state = 146 }',
    'famagusta_port':'owns_state = 146\ncontrols_state = 146\nhas_war = no\n146 = { free_building_slots = { building = naval_base size > 0 province = 7193 } }',
    'enosis_debate': 'NOT = { '+flag('independence_settled')+' }',
    'bicomm_constitution': ge('settlement_progress',40)+'\n'+le('communal_tension',45)+'\n'+no_abuses(),
    'federal_compromise': assent()+'\n'+ge('settlement_progress',60)+'\nhas_war = no\n'+no_abuses(),
    'shared_republic': assent()+'\n'+ge('settlement_progress',70)+'\nhas_war = no\n'+no_abuses(),
    'constitutional_settlement': flag('constitutional_package_accepted')+'\n'+assent()+'\n'+no_abuses()+'\ncontrols_state = 145\ncontrols_state = 146\nhas_war = no',
    'guarantee_review': assent()+'\n'+no_abuses(),
    'constitutional_guard': flag('civilian_command_implemented')+'\nNOT = { '+flag('coup_regime_active')+' }',
    'independence_mandate': 'NOT = { '+flag('enosis_implemented')+' }',
    'enosis_agreement': assent()+'\n'+flag('tc_enosis_assent')+'\n'+flag('guarantees_revised')+'\n'+flag('bases_agreement')+'\nhas_war = no\ncontrols_state = 145\ncontrols_state = 146\nNOT = { '+flag('independence_settled')+' }',
    'crisis_response': crisis(), 'crisis_conference': 'OR = { '+crisis()+' '+ge('communal_tension',65)+' }',
    'un_security_council': 'OR = { '+crisis()+' '+ge('coup_pressure',65)+' has_war = yes }',
    'continue_resistance': 'has_war = yes', 'ceasefire_lines': 'has_war_with = TUR',
    'accountability': flag('unresolved_reprisals')+'\n'+flag('housing_implemented'),
    'return_and_restitution': 'has_war = no\n'+no_abuses()+'\nOR = { '+access()+' '+flag('applied_tc_civilian_access')+' }',
    'reconstruction': flag('housing_implemented')+'\nhas_war = no',
    'frozen_partition': flag('actual_partition'),
    'tc_joint_budgets': no_abuses(), 'tc_local_services': no_abuses(),
    'tc_cooperative_credit': access()+'\n'+flag('joint_services_compact'),
    'tc_mixed_workshops': access()+'\n'+flag('joint_services_compact'),
    'tc_business_licences': access()+'\n'+flag('local_services_compact'),
    'tc_property_records': access()+'\n'+flag('local_services_compact'),
    'tc_services_mandate': access(), 'tc_ctp':'date > 1970.12.26\n'+flag('ctp_formed'),
    'tc_constitutional_consent': assent()+'\n'+ge('relief_stage',2)+'\n'+no_abuses(),
    'tc_unilateral_resolution': flag('tc_terms_rejected')+'\nNOT = { '+flag('final_settlement_implemented')+' }',
    'tc_postwar_admin': flag('actual_partition'), 'tc_postwar_dispute': flag('actual_partition'),
    'tc_beyond_partition': 'has_war = no\n'+assent()+'\n'+no_abuses(),
    'war_junta_links': 'GRE = { nationalist_military_junta_are_in_power = yes }',
    'war_plot': 'OR = { check_variable = { ruling_party = 20 } check_variable = { ruling_party = 21 } check_variable = { ruling_party = 22 } }',
    'war_loyal_guard': flag('officer_withdrawal_implemented')+'\n'+flag('militias_disarmed'),
    'war_conference': crisis(), 'war_defy': flag('ultimatum_active'),
    'war_prepare_intervention': 'OR = { has_war = yes '+flag('ultimatum_active')+' '+flag('intervention_threat')+' }',
    'war_july_ceasefire': flag('first_intervention_phase'),
    'war_geneva': flag('first_intervention_phase'),
    'war_remobilise': flag('first_intervention_phase')+'\nNOT = { '+flag('final_settlement_implemented')+' }',
}
HISTORICAL_SKIP = {
    'checkpoint_leverage','civilian_command','police_oversight','emergency_powers','unitary_constitution',
    'federal_compromise','shared_republic','constitutional_settlement','independence_mandate',
    'tolerate_armed_factions','collective_reprisals','tourism_priority','foreign_capital',
    'mobile_reserve','greek_mission','western_association','base_sovereignty','enosis_debate','enosis_agreement',
    'emergency_repression','frozen_partition','tc_pressure','tc_police','tc_security_representation',
    'tc_patron_security','tc_unitary_bargain','tc_shared_republic','tc_enosis_consent','tc_unilateral_resolution',
    'tc_postwar_dispute','war_mainland_command','war_junta_links','war_plot',
}
HISTORICAL_PARTY_CHOICES = {
    'p1_first_b','p1_follow_b','p1_second_a','p1_economic_b','p1_project_b1','p1_project_b2',
    'p1_finance_a','p1_finance_a_follow',
}
TITLE_OVERRIDES = {
    'p1_organisation':'Renew the Presidential Coalition',
    'war_putsch':'A Military Coup Attempt','war_july_ceasefire':'Answer the Ceasefire Appeal',
    'war_geneva':'Negotiate a Political Settlement','war_august':'The Renewed Hostilities Decision',
}
