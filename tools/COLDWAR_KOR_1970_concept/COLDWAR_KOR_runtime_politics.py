# IMPERIA CW — Cold War: Korea 1970 domestic politics runtime.
"""Generate native political handlers, transition decisions/events and ideas."""

P = "COLDWAR_KOR_"
HEADER = "# IMPERIA CW — Cold War: South Korea 1970 political institutions."


def block(name, body):
    return name + " = {\n" + "\n".join("\t" + x if x else "" for x in body.strip().splitlines()) + "\n}\n"


def action_bodies():
    # Root applies approved leaf effects (costs, policies, buildings and state
    # changes) before calling these once-only transition/institution receipts.
    return {
        "yushin_institutions": "set_country_flag = COLDWAR_KOR_constitution_yushin",
        "constitutional_reform_commitment": "set_country_flag = COLDWAR_KOR_electoral_opening\nset_country_flag = COLDWAR_KOR_negotiating_commitment",
        "managed_succession": "set_country_flag = COLDWAR_KOR_managed_succession",
        "open_succession": "set_country_flag = COLDWAR_KOR_civilian_succession_open",
        "restore_civil_liberties": "set_country_flag = COLDWAR_KOR_civil_liberties_restored",
        "parliamentary_republic": "set_country_flag = COLDWAR_KOR_parliamentary_republic",
        "presidential_term_limits": "set_country_flag = COLDWAR_KOR_term_limits",
        "intelligence_oversight": "set_country_flag = COLDWAR_KOR_intelligence_oversight",
        "political_prisoner_review": "set_country_flag = COLDWAR_KOR_prisoner_review",
        "confirm_constitutional_settlement": "if = { limit = { has_country_flag = COLDWAR_KOR_constitutional_ratification_passed } COLDWAR_KOR_refresh_programmes = yes }",
        "nordpolitik_negotiations": "set_country_flag = COLDWAR_KOR_nordpolitik_authorized",
        "controlled_constitution": "set_country_flag = COLDWAR_KOR_constitution_controlled_fifth",
        "open_constitutional_negotiations": "set_country_flag = COLDWAR_KOR_military_opening_authorized",
        "accept_direct_election_principle": "set_country_flag = COLDWAR_KOR_military_opening_authorized\nset_country_flag = COLDWAR_KOR_direct_election_principle",
        "independent_union_law": "set_country_flag = COLDWAR_KOR_lawful_labour_bargaining",
        "socialist_international_contacts": "set_country_flag = COLDWAR_KOR_socialist_contacts_authorized",
        "legal_civic_associations": "set_variable = { party_banned_array^5 = 0 }\nset_variable = { party_banned_array^19 = 0 }\nset_country_flag = COLDWAR_KOR_civic_legal_5\nset_country_flag = COLDWAR_KOR_civic_legal_19",
        "civic_pluralism": "set_country_flag = COLDWAR_KOR_civic_pluralism",
        "left_pluralism": "set_country_flag = COLDWAR_KOR_left_pluralism",
        "southern_ratification": "set_country_flag = COLDWAR_KOR_southern_settlement_ratified",
        "civilian_transition_agreement": "set_country_flag = COLDWAR_KOR_civilian_transition_terms",
        "political_case_review": "set_country_flag = COLDWAR_KOR_case_review_authorized",
        "security_transition_terms": "set_country_flag = COLDWAR_KOR_security_transition_terms",
        "bind_electoral_succession": "set_country_flag = COLDWAR_KOR_electoral_succession_bound",
        "independent_repression_inquiry": "set_country_flag = COLDWAR_KOR_independent_inquiry_authorized",
        "warranted_security_operations": "COLDWAR_KOR_refresh_programmes = yes",
        "open_constitutional_dossier": "set_country_flag = COLDWAR_KOR_constitutional_dossier_open",
        "resolve_command_challenge": "COLDWAR_KOR_refresh_programmes = yes",
        "authorize_constitutional_talks": "COLDWAR_KOR_refresh_programmes = yes",
        "register_charter_participants": "set_country_flag = COLDWAR_KOR_charter_participants_registered",
        "preserve_case_records": "set_country_flag = COLDWAR_KOR_case_records_preserved",
        "negotiate_unity_ticket": "COLDWAR_KOR_refresh_programmes = yes",
        "retain_separate_tickets": "COLDWAR_KOR_refresh_programmes = yes",
        "conditional_disclosure_compact": "set_country_flag = COLDWAR_KOR_conditional_disclosure_compact",
        "ratify_negotiating_mandate": "COLDWAR_KOR_refresh_programmes = yes",
        "submit_constitutional_ballot": "set_country_flag = COLDWAR_KOR_ballot_submission_recorded",
        "configure_lawful_election": "if = { limit = { has_country_flag = COLDWAR_KOR_constitutional_ratification_passed has_country_flag = COLDWAR_KOR_constitutional_order } set_elections_60_months = yes if = { limit = { check_variable = { COLDWAR_KOR_charter_model = 1 } } set_variable = { term_limit = 1 } set_variable = { current_term = 0 } } COLDWAR_KOR_on_native_election_campaign = yes country_event = { id = MD4_election_campaign.0 } }\nCOLDWAR_KOR_refresh_programmes = yes",
        "protect_civil_press": "COLDWAR_KOR_refresh_programmes = yes",
        "constitutional_review_rules": "COLDWAR_KOR_refresh_programmes = yes",
        "bind_civilian_appointments": "COLDWAR_KOR_refresh_programmes = yes",
        "accelerated_officer_retirement": "COLDWAR_KOR_refresh_programmes = yes",
        "staged_officer_retirement": "COLDWAR_KOR_refresh_programmes = yes",
        "restore_assembly_audits": "COLDWAR_KOR_refresh_programmes = yes",
        "register_native_labor_faction": "COLDWAR_KOR_refresh_programmes = yes",
        "prepare_local_autonomy_law": "COLDWAR_KOR_refresh_programmes = yes",
        "confirm_native_handover": "COLDWAR_KOR_refresh_programmes = yes",
        "enforce_democratic_safeguards": "COLDWAR_KOR_refresh_programmes = yes",
        "conservative_merger": "if = { limit = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } set_country_flag = COLDWAR_KOR_conservative_identity_active }",
        "constitutional_party_guarantees": "set_country_flag = COLDWAR_KOR_civilian_party_settlement",
        "conditional_peninsula_review": "if = { limit = { OR = { has_country_flag = COLDWAR_KOR_confederal_secretariat_signed has_country_flag = COLDWAR_KOR_limited_trade_signed } } set_country_flag = COLDWAR_KOR_joint_ratification_open }\nelse_if = { limit = { OR = { has_country_flag = COLDWAR_KOR_confederal_secretariat_refused has_country_flag = COLDWAR_KOR_confederal_secretariat_expired has_country_flag = COLDWAR_KOR_limited_trade_refused has_country_flag = COLDWAR_KOR_limited_trade_expired } } add_political_power = 25 }",
        "inter_korean_channels": "set_country_flag = COLDWAR_KOR_inter_korean_channels_authorized",
        "extend_social_insurance": "set_country_flag = COLDWAR_KOR_social_insurance_framework",
        "native_construction_contract_bids": "set_country_flag = COLDWAR_KOR_construction_bids_authorized",
        "publish_treaty_obligations": "set_country_flag = COLDWAR_KOR_treaty_publication_authorized",
        "sector_investment_priority": "set_country_flag = COLDWAR_KOR_sector_investment_authorized",
        "verify_korean_signatures": "set_country_flag = COLDWAR_KOR_korean_signatures_verified",
    }


def script_effects():
    out = [HEADER]
    for name, body in action_bodies().items():
        out.append(block("COLDWAR_KOR_action_" + name, body))
    # This dispatcher preserves the historical Park leader on startup. New
    # leaders are installed only after a genuine native party/office transition.
    leader = '''update_set_politics = yes
if = {
 limit = { has_country_flag = COLDWAR_KOR_select_interim_choi }
 hidden_effect = { kill_country_leader = yes }
 create_country_leader = { name = "Choi Kyu-hah" ideology = Western_Autocracy traits = { western_Western_Autocracy } }
 clr_country_flag = COLDWAR_KOR_select_interim_choi
 set_country_flag = COLDWAR_KOR_caretaker_installed
}
else_if = { limit = { check_variable = { ruling_party = 0 } has_country_leader = { name = "Choi Kyu-hah" ruling_only = yes } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_kjp_nominated } } NOT = { has_country_flag = COLDWAR_KOR_kjp_successor } } }
else_if = { limit = { check_variable = { ruling_party = 0 } has_country_leader = { name = "Park Chung Hee" ruling_only = yes } NOT = { has_country_flag = COLDWAR_KOR_kjp_successor } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_kjp_nominated } } } }
else_if = { limit = { check_variable = { ruling_party = 0 } has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_kjp_nominated } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Kim Jong-pil" picture = "gfx/Leaders/KOR/Kim_Jong-pil.dds" ideology = Western_Autocracy traits = { western_Western_Autocracy } } set_country_flag = COLDWAR_KOR_kjp_successor }
else_if = { limit = { check_variable = { ruling_party = 0 } has_country_leader = { name = "Kim Jong-pil" ruling_only = yes } } }
else_if = { limit = { check_variable = { ruling_party = 0 } has_country_flag = COLDWAR_KOR_kjp_successor } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Kim Jong-pil" picture = "gfx/Leaders/KOR/Kim_Jong-pil.dds" ideology = Western_Autocracy traits = { western_Western_Autocracy } } }
else_if = { limit = { check_variable = { ruling_party = 0 } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "DRP Cabinet" ideology = Western_Autocracy traits = { western_Western_Autocracy } } }
else_if = { limit = { check_variable = { ruling_party = 1 } has_country_leader = { name = "Yun Po-sun" ruling_only = yes } } }
else_if = { limit = { check_variable = { ruling_party = 1 } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Yun Po-sun" ideology = conservatism traits = { } } }
else_if = { limit = { check_variable = { ruling_party = 2 } has_country_leader = { name = "Kim Dae-jung" ruling_only = yes } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_ys_nominated } } } }
else_if = { limit = { check_variable = { ruling_party = 2 } has_country_leader = { name = "Kim Young-sam" ruling_only = yes } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_dj_nominated } } } }
else_if = { limit = { check_variable = { ruling_party = 2 } has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_dj_nominated } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Kim Dae-jung" picture = "gfx/Leaders/KOR/Kim_Dae-jung.dds" ideology = liberalism traits = { western_liberalism } } }
else_if = { limit = { check_variable = { ruling_party = 2 } has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_ys_nominated } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Kim Young-sam" picture = "gfx/leaders/mdcw_historical_pool/KOR_kim_young_sam.dds" ideology = liberalism traits = { western_liberalism } } }
else_if = { limit = { check_variable = { ruling_party = 2 } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Forties Reform Cabinet" ideology = liberalism traits = { western_liberalism } } }
else_if = { limit = { check_variable = { ruling_party = 3 } has_country_leader = { name = "Kim Chul" ruling_only = yes } } }
else_if = { limit = { check_variable = { ruling_party = 3 } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Kim Chul" ideology = socialism traits = { western_socialism } } }
else_if = { limit = { check_variable = { ruling_party = 4 } has_country_flag = COLDWAR_KOR_revolutionary_settlement } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Revolutionary Cabinet" ideology = communist_state traits = { } } }
else_if = { limit = { check_variable = { ruling_party = 5 } has_country_flag = COLDWAR_KOR_civic_legal_5 } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Student Civic Cabinet" ideology = anarchist_communism traits = { } } }
else_if = { limit = { check_variable = { ruling_party = 7 } has_country_flag = COLDWAR_KOR_security_directorate_ratified } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Security Directorate" ideology = Autocracy traits = { } } }
else_if = { limit = { check_variable = { ruling_party = 19 } has_country_flag = COLDWAR_KOR_civic_legal_19 } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Independent Left Cabinet" ideology = Neutral_green traits = { neutrality_Neutral_green } } }
else_if = { limit = { check_variable = { ruling_party = 22 } has_country_leader = { name = "Roh Tae-woo" ruling_only = yes } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_roh_nominated } } } }
else_if = { limit = { check_variable = { ruling_party = 22 } has_country_leader = { name = "Chun Doo-hwan" ruling_only = yes } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_roh_nominated } } } }
else_if = { limit = { check_variable = { ruling_party = 22 } has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_roh_nominated } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Roh Tae-woo" ideology = Nat_Autocracy traits = { nationalist_Nat_Autocracy } } }
else_if = { limit = { check_variable = { ruling_party = 22 } has_country_flag = COLDWAR_KOR_historical_chun_transition NOT = { has_country_flag = COLDWAR_KOR_election_resolution_pending } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Chun Doo-hwan" picture = "gfx/leaders/mdcw_historical_pool/KOR_chun_doo_hwan.dds" ideology = Nat_Autocracy traits = { nationalist_Nat_Autocracy } } }
else_if = { limit = { check_variable = { ruling_party = 22 } } hidden_effect = { kill_country_leader = yes } create_country_leader = { name = "Army Command Cabinet" ideology = Nat_Autocracy traits = { nationalist_Nat_Autocracy } } }'''
    # A retired president is replaced only at an actual resolved election.
    # Keep that native successor on subsequent refreshes until a different
    # party wins or an eligible, explicitly nominated candidate wins office.
    nominations = " OR = { AND = { check_variable = { ruling_party = 0 } has_country_flag = COLDWAR_KOR_kjp_nominated } AND = { check_variable = { ruling_party = 2 } OR = { has_country_flag = COLDWAR_KOR_ys_nominated has_country_flag = COLDWAR_KOR_dj_nominated } } AND = { check_variable = { ruling_party = 22 } has_country_flag = COLDWAR_KOR_roh_nominated } }"
    hold = "if = { limit = { has_country_flag = COLDWAR_KOR_term_successor_active check_variable = { ruling_party = COLDWAR_KOR_term_successor_party } NOT = { AND = { has_country_flag = COLDWAR_KOR_install_elected_incumbent " + nominations + " } } } }\nelse_"
    leader = leader.replace("update_set_politics = yes\nif =", "update_set_politics = yes\n" + hold + "if =", 1)
    for name, party in (("Revolutionary Cabinet", 4), ("Student Civic Cabinet", 5), ("Security Directorate", 7), ("Independent Left Cabinet", 19)):
        marker = f'else_if = {{ limit = {{ check_variable = {{ ruling_party = {party} }}'
        guard = f'else_if = {{ limit = {{ check_variable = {{ ruling_party = {party} }} has_country_leader = {{ name = "{name}" ruling_only = yes }} }} }}\n'
        leader = leader.replace(marker, guard + marker, 1)
    out.append(block("COLDWAR_KOR_1970_set_leader", leader))
    out.append(block("COLDWAR_KOR_record_presidential_term", presidential_term()))
    out.append(block("COLDWAR_KOR_on_native_election_campaign", "if = { limit = { has_country_flag = COLDWAR_KOR_constitutional_order has_elections = yes NOT = { has_country_flag = COLDWAR_KOR_election_resolution_pending } NOT = { has_country_flag = coalition_forming } } set_country_flag = COLDWAR_KOR_election_resolution_pending }"))
    out.append(block("COLDWAR_KOR_on_native_election_resolved", "if = { limit = { has_country_flag = COLDWAR_KOR_constitutional_order has_elections = yes has_country_flag = COLDWAR_KOR_election_resolution_pending has_country_flag = COLDWAR_KOR_install_elected_incumbent NOT = { has_country_flag = elections_in_progress } NOT = { has_country_flag = coalition_forming } } COLDWAR_KOR_1970_set_leader = yes set_country_flag = COLDWAR_KOR_lawful_election_completed clr_country_flag = COLDWAR_KOR_election_resolution_pending if = { limit = { check_variable = { ruling_party = 22 } } set_country_flag = COLDWAR_KOR_djp_formed set_country_flag = COLDWAR_KOR_electoral_party_22_legal } if = { limit = { has_country_leader = { name = \"Kim Young-sam\" ruling_only = yes } } set_country_flag = COLDWAR_KOR_ys_incumbent clr_country_flag = COLDWAR_KOR_dj_incumbent clr_country_flag = COLDWAR_KOR_ys_nominated clr_country_flag = COLDWAR_KOR_dj_nominated } if = { limit = { has_country_leader = { name = \"Kim Dae-jung\" ruling_only = yes } } set_country_flag = COLDWAR_KOR_dj_incumbent clr_country_flag = COLDWAR_KOR_ys_incumbent clr_country_flag = COLDWAR_KOR_ys_nominated clr_country_flag = COLDWAR_KOR_dj_nominated } clr_country_flag = COLDWAR_KOR_ys_nominated clr_country_flag = COLDWAR_KOR_dj_nominated clr_country_flag = COLDWAR_KOR_roh_nominated clr_country_flag = COLDWAR_KOR_kjp_nominated COLDWAR_KOR_politics_sync = yes }"))
    out[-1] = out[-1].replace("set_country_flag = COLDWAR_KOR_lawful_election_completed", "COLDWAR_KOR_record_presidential_term = yes set_country_flag = COLDWAR_KOR_lawful_election_completed", 1)
    out.append(block("COLDWAR_KOR_calculate_charter_vote", charter_calc()))
    maintenance = "COLDWAR_KOR_refresh_programmes = yes\nif = { limit = { has_country_flag = COLDWAR_KOR_judicial_review has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_court_appointments_implemented has_country_flag = COLDWAR_KOR_court_implementation_pending NOT = { has_country_flag = COLDWAR_KOR_court_commissioning_delay } NOT = { has_country_flag = COLDWAR_KOR_court_event_queued } } set_country_flag = COLDWAR_KOR_court_event_queued country_event = { id = COLDWAR_KOR_transition.88 days = 1 } }"
    out.append(block("COLDWAR_KOR_politics_sync", maintenance))
    daily = "COLDWAR_KOR_politics_sync = yes\n"
    pulses = [
        ("date > 1970.11.12 date < 1970.11.16 has_dynamic_modifier = { modifier = COLDWAR_KOR_start_labour }", "labour_crisis_open"),
        ("date > 1971.4.26 date < 1971.4.30 has_country_leader = { name = \"Park Chung Hee\" ruling_only = yes }", "1971_contest_pending"),
        ("date > 1979.8.10 date < 1979.8.15 has_country_flag = COLDWAR_KOR_constitution_yushin", "yh_case_open"),
        ("date > 1979.10.15 date < 1979.10.20 has_country_flag = COLDWAR_KOR_constitution_yushin", "buma_crisis_open"),
        ("date > 1980.5.16 date < 1980.5.20 check_variable = { ruling_party = 22 } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order }", "officer_control_crisis"),
        ("date > 1985.2.11 date < 1985.2.16 check_variable = { ruling_party = 22 } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } OR = { check_variable = { party_pop_array^1 > 0 } check_variable = { party_pop_array^2 > 0 } }", "opposition_reorganization_pending"),
        ("date > 1987.1.13 date < 1987.1.18 check_variable = { ruling_party = 22 } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order }", "torture_disclosure_crisis"),
        ("date > 1987.6.9 date < 1987.6.15 check_variable = { ruling_party = 22 } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } has_country_flag = COLDWAR_KOR_opposition_constitutional_demand", "constitutional_mobilization"),
        ("date > 1987.6.30 date < 1987.7.5 has_country_flag = COLDWAR_KOR_june_movement_1987_recorded", "post_june_labor_wave"),
    ]
    for conditions, receipt in pulses:
        daily += f"if = {{ limit = {{ original_tag = KOR IMP_is_1970_scenario = yes {conditions} NOT = {{ has_country_flag = COLDWAR_KOR_{receipt} }} }} set_country_flag = COLDWAR_KOR_{receipt} }}\n"
    daily += "if = { limit = { original_tag = KOR IMP_is_1970_scenario = yes date > 1990.1.21 check_variable = { party_pop_array^0 > 0 } NOT = { has_country_flag = COLDWAR_KOR_ndrp_formed } } set_country_flag = COLDWAR_KOR_ndrp_formed }\n"
    out.append(block("COLDWAR_KOR_politics_daily", daily))
    out.append(block("COLDWAR_KOR_politics_maintenance", "COLDWAR_KOR_politics_sync = yes"))
    out.append(block("COLDWAR_KOR_politics_initialize", "if = { limit = { original_tag = KOR IMP_is_1970_scenario = yes has_country_leader = { name = \"Park Chung Hee\" ruling_only = yes } NOT = { has_country_flag = COLDWAR_KOR_park_succession_unresolved } } set_country_flag = COLDWAR_KOR_park_succession_unresolved }\nCOLDWAR_KOR_politics_sync = yes"))
    return "\n".join(out)


def presidential_term():
    people = (("park", "Park Chung Hee"), ("yun", "Yun Po-sun"), ("kjp", "Kim Jong-pil"), ("ys", "Kim Young-sam"), ("dj", "Kim Dae-jung"), ("chun", "Chun Doo-hwan"), ("roh", "Roh Tae-woo"))
    repeat = [f'AND = {{ has_country_leader = {{ name = "{name}" ruling_only = yes }} has_country_flag = COLDWAR_KOR_presidential_term_served_{key} }}' for key, name in people]
    unknown = " ".join(f'NOT = {{ has_country_leader = {{ name = "{name}" ruling_only = yes }} }}' for key, name in people)
    repeat.append("AND = { " + unknown + " check_variable = { current_term > 1 } check_variable = { ruling_party = COLDWAR_KOR_last_presidential_party } }")
    body = "if = { limit = { has_country_flag = COLDWAR_KOR_install_elected_incumbent has_country_flag = COLDWAR_KOR_constitutional_order check_variable = { COLDWAR_KOR_charter_model = 1 } }\n"
    body += "if = { limit = { OR = { " + " ".join(repeat) + " } } hidden_effect = { kill_country_leader = yes update_set_politics = yes set_correct_ideology_trait = yes } set_country_flag = COLDWAR_KOR_term_successor_active set_variable = { COLDWAR_KOR_term_successor_party = ruling_party } }\nelse = { clr_country_flag = COLDWAR_KOR_term_successor_active }\n"
    for key, name in people:
        body += f'if = {{ limit = {{ has_country_leader = {{ name = "{name}" ruling_only = yes }} }} set_country_flag = COLDWAR_KOR_presidential_term_served_{key} }}\n'
    return body + "set_variable = { current_term = 1 } set_variable = { COLDWAR_KOR_last_presidential_party = ruling_party }\n}"


def charter_calc():
    # Sum native party_pop_array shares for each eligible party exactly once;
    # support flags are a unique subset. No generated party popularity.
    s = ["set_temp_variable = { COLDWAR_KOR_charter_support = 0 }", "set_temp_variable = { COLDWAR_KOR_charter_electorate = 0 }"]
    slots = [(0, ""), (1, ""), (2, ""), (3, ""), (4, "has_country_flag = COLDWAR_KOR_electoral_party_4_legal"), (5, "has_country_flag = COLDWAR_KOR_civic_legal_5"), (19, "has_country_flag = COLDWAR_KOR_civic_legal_19"), (22, "has_country_flag = COLDWAR_KOR_electoral_party_22_legal")]
    for n, extra in slots:
        cond = ((extra + " ") if extra else "") + f"check_variable = {{ party_banned_array^{n} = 0 }}"
        s.append(f"if = {{ limit = {{ {cond} }} add_to_temp_variable = {{ COLDWAR_KOR_charter_electorate = party_pop_array^{n} }} if = {{ limit = {{ has_country_flag = COLDWAR_KOR_charter_supporter_{n} }} add_to_temp_variable = {{ COLDWAR_KOR_charter_support = party_pop_array^{n} }} }} }}")
    s += ["set_variable = { COLDWAR_KOR_charter_support_share = 0 }", "if = { limit = { check_variable = { COLDWAR_KOR_charter_electorate > 0 } } set_variable = { COLDWAR_KOR_charter_support_share = { value = COLDWAR_KOR_charter_support divide = COLDWAR_KOR_charter_electorate clamp = { min = 0 max = 1 } } } }"]
    return "\n".join(s)


def trigger_file():
    return HEADER + "\n" + block("COLDWAR_KOR_political_scenario", "original_tag = KOR\nIMP_is_1970_scenario = yes\nis_subject = no") + block("COLDWAR_KOR_pending_court_commission", "COLDWAR_KOR_political_scenario = yes\nhas_country_flag = COLDWAR_KOR_judicial_review\nhas_country_flag = COLDWAR_KOR_constitutional_order\nhas_country_flag = COLDWAR_KOR_court_appointments_implemented\nhas_country_flag = COLDWAR_KOR_court_implementation_pending\nNOT = { has_country_flag = COLDWAR_KOR_court_commissioning_delay }")


def decisions_file():
    base = HEADER + '''
COLDWAR_KOR_constitutional_decisions = {
 COLDWAR_KOR_legalize_civic_parties = {
  cost = 50
  fire_only_once = yes
  available = { COLDWAR_KOR_political_scenario = yes OR = { has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_negotiating_commitment } NOT = { has_country_flag = COLDWAR_KOR_nationwide_martial_law } NOT = { AND = { has_country_flag = COLDWAR_KOR_civic_legal_5 has_country_flag = COLDWAR_KOR_civic_legal_19 } } }
  complete_effect = { COLDWAR_KOR_action_legal_civic_associations = yes add_timed_idea = { idea = COLDWAR_KOR_civic_legalization_adjustment days = 90 } }
 }
 COLDWAR_KOR_reopen_constitutional_talks = {
  cost = 75
  available = { COLDWAR_KOR_political_scenario = yes check_variable = { ruling_party = 22 } has_country_flag = COLDWAR_KOR_military_reconsolidation has_country_flag = COLDWAR_KOR_opposition_constitutional_demand NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } NOT = { has_country_flag = COLDWAR_KOR_military_opening_authorized } NOT = { has_country_flag = COLDWAR_KOR_transition_open } NOT = { has_country_flag = COLDWAR_KOR_talks_authorized } NOT = { has_country_flag = COLDWAR_KOR_talks_retry_cooldown } }
  complete_effect = { set_country_flag = COLDWAR_KOR_military_opening_authorized clr_country_flag = COLDWAR_KOR_military_reconsolidation set_country_flag = { flag = COLDWAR_KOR_talks_retry_cooldown days = 90 } }
 }
 COLDWAR_KOR_reopen_charter_ballot = {
  cost = 50
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_charter_rejected has_country_flag = COLDWAR_KOR_talks_authorized has_country_flag = COLDWAR_KOR_charter_mandate NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } NOT = { has_country_flag = COLDWAR_KOR_ballot_pending } NOT = { has_country_flag = COLDWAR_KOR_charter_retry_cooldown } check_variable = { COLDWAR_KOR_charter_model > 0 } }
  complete_effect = { clr_country_flag = COLDWAR_KOR_charter_rejected set_country_flag = COLDWAR_KOR_ballot_pending country_event = { id = COLDWAR_KOR_transition.30 days = 30 } }
 }
 COLDWAR_KOR_implement_constitutional_court = {
  cost = 50
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_judicial_review NOT = { has_country_flag = COLDWAR_KOR_court_appointments_implemented } NOT = { has_country_flag = COLDWAR_KOR_court_implementation_pending } NOT = { has_country_flag = COLDWAR_KOR_judicial_review_operational } }
  complete_effect = { set_temp_variable = { treasury_change = -1 } modify_treasury_effect = yes set_country_flag = COLDWAR_KOR_court_implementation_pending set_country_flag = COLDWAR_KOR_court_appointments_implemented set_country_flag = { flag = COLDWAR_KOR_court_commissioning_delay days = 90 } }
 }
 COLDWAR_KOR_review_repression_cases = {
  cost = 75
  available = { COLDWAR_KOR_political_scenario = yes OR = { has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_judicial_review has_country_flag = COLDWAR_KOR_intelligence_oversight } NOT = { has_country_flag = COLDWAR_KOR_nationwide_martial_law } NOT = { has_country_flag = COLDWAR_KOR_repression_cases_reviewed } }
  complete_effect = { set_temp_variable = { treasury_change = -1 } modify_treasury_effect = yes set_country_flag = COLDWAR_KOR_repression_cases_reviewed remove_ideas = { idea = COLDWAR_KOR_martial_law_legitimacy_scar } add_ideas = COLDWAR_KOR_accountability_settlement }
 }
 COLDWAR_KOR_authorize_djp_merger = {
  available = { COLDWAR_KOR_political_scenario = yes date > 1990.1.21 has_country_flag = COLDWAR_KOR_djp_formed check_variable = { party_banned_array^22 = 0 } check_variable = { party_pop_array^22 > 0 } NOT = { has_country_flag = COLDWAR_KOR_djp_merger_authorized } NOT = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } }
  complete_effect = { set_country_flag = COLDWAR_KOR_djp_merger_authorized }
 }
 COLDWAR_KOR_authorize_ys_merger = {
  available = { COLDWAR_KOR_political_scenario = yes date > 1990.1.21 check_variable = { party_banned_array^2 = 0 } check_variable = { party_pop_array^2 > 0 } NOT = { has_country_flag = COLDWAR_KOR_ys_merger_authorized } NOT = { has_country_flag = COLDWAR_KOR_ys_merger_pending } NOT = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } }
  complete_effect = { set_country_flag = COLDWAR_KOR_ys_merger_pending country_event = { id = COLDWAR_KOR_transition.230 } }
 }
 COLDWAR_KOR_authorize_ndrp_merger = {
  available = { COLDWAR_KOR_political_scenario = yes date > 1990.1.21 has_country_flag = COLDWAR_KOR_ndrp_formed check_variable = { party_banned_array^0 = 0 } check_variable = { party_pop_array^0 > 0 } NOT = { has_country_flag = COLDWAR_KOR_ndrp_merger_authorized } NOT = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } }
  complete_effect = { set_country_flag = COLDWAR_KOR_ndrp_merger_authorized }
 }
 COLDWAR_KOR_open_conservative_merger = {
  available = { COLDWAR_KOR_political_scenario = yes date > 1990.1.21 has_country_flag = COLDWAR_KOR_djp_merger_authorized has_country_flag = COLDWAR_KOR_ys_merger_authorized has_country_flag = COLDWAR_KOR_ndrp_merger_authorized NOT = { has_country_flag = COLDWAR_KOR_transition_1990_recorded } NOT = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } }
  complete_effect = { set_country_flag = COLDWAR_KOR_merger_talks_pending country_event = { id = COLDWAR_KOR_transition.114 } }
 }
 COLDWAR_KOR_nominate_ys = {
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_constitutional_order OR = { has_country_flag = COLDWAR_KOR_constitution_presidential has_country_flag = COLDWAR_KOR_constitution_consensus } has_elections = yes check_variable = { party_banned_array^2 = 0 } check_variable = { party_pop_array^2 > 0 } NOT = { has_country_flag = COLDWAR_KOR_ys_nominated } NOT = { has_country_flag = COLDWAR_KOR_dj_nominated } }
  complete_effect = { set_country_flag = COLDWAR_KOR_ys_nominated }
 }
 COLDWAR_KOR_nominate_dj = {
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_constitutional_order OR = { has_country_flag = COLDWAR_KOR_constitution_presidential has_country_flag = COLDWAR_KOR_constitution_consensus } has_elections = yes check_variable = { party_banned_array^2 = 0 } check_variable = { party_pop_array^2 > 0 } NOT = { has_country_flag = COLDWAR_KOR_ys_nominated } NOT = { has_country_flag = COLDWAR_KOR_dj_nominated } }
  complete_effect = { set_country_flag = COLDWAR_KOR_dj_nominated }
 }
 COLDWAR_KOR_nominate_roh = {
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_direct_election_principle has_country_flag = COLDWAR_KOR_djp_formed has_country_flag = COLDWAR_KOR_electoral_party_22_legal OR = { has_country_flag = COLDWAR_KOR_constitution_presidential has_country_flag = COLDWAR_KOR_constitution_consensus } has_elections = yes check_variable = { party_banned_array^22 = 0 } check_variable = { party_pop_array^22 > 0 } NOT = { has_country_flag = COLDWAR_KOR_roh_nominated } }
  complete_effect = { set_country_flag = COLDWAR_KOR_roh_nominated }
 }
 COLDWAR_KOR_authorize_military_succession = {
  cost = 75
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_officer_council_contest NOT = { has_country_flag = COLDWAR_KOR_historical_chun_transition } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } }
  complete_effect = { set_country_flag = COLDWAR_KOR_historical_chun_transition set_temp_variable = { rul_party_temp = 22 } set_temp_variable = { disable_elections = 1 } change_ruling_party_effect = yes clr_country_flag = COLDWAR_KOR_officer_council_contest add_timed_idea = { idea = COLDWAR_KOR_contested_command days = 90 } }
 }
 COLDWAR_KOR_ratify_revolutionary_settlement = {
  fire_only_once = yes
  available = { COLDWAR_KOR_political_scenario = yes check_variable = { ruling_party = 4 } NOT = { has_country_flag = COLDWAR_KOR_revolutionary_settlement } }
  complete_effect = { set_variable = { party_banned_array^4 = 0 } set_country_flag = COLDWAR_KOR_electoral_party_4_legal set_country_flag = COLDWAR_KOR_revolutionary_settlement COLDWAR_KOR_1970_set_leader = yes add_timed_idea = { idea = COLDWAR_KOR_revolutionary_settlement_burden days = 90 } }
 }
 COLDWAR_KOR_form_democratic_justice_party = {
  fire_only_once = yes
  available = { COLDWAR_KOR_political_scenario = yes check_variable = { ruling_party = 22 } check_variable = { party_banned_array^22 = 0 } check_variable = { party_pop_array^22 > 0 } OR = { has_country_flag = COLDWAR_KOR_constitution_controlled_fifth has_country_flag = COLDWAR_KOR_military_opening_authorized } NOT = { has_country_flag = COLDWAR_KOR_djp_formed } }
  complete_effect = { set_country_flag = COLDWAR_KOR_djp_formed set_country_flag = COLDWAR_KOR_electoral_party_22_legal }
 }
 COLDWAR_KOR_authorize_security_directorate = {
  cost = 100
  fire_only_once = yes
  available = { COLDWAR_KOR_political_scenario = yes OR = { has_country_flag = COLDWAR_KOR_officer_council_contest has_country_flag = COLDWAR_KOR_military_reconsolidation } has_stability < 0.30 NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } NOT = { has_country_flag = COLDWAR_KOR_security_directorate_ratified } }
  complete_effect = { add_stability = -0.05 set_country_flag = COLDWAR_KOR_security_directorate_ratified set_variable = { party_banned_array^7 = 0 } clr_country_flag = COLDWAR_KOR_officer_council_contest clr_country_flag = COLDWAR_KOR_military_reconsolidation set_temp_variable = { rul_party_temp = 7 } set_temp_variable = { disable_elections = 1 } change_ruling_party_effect = yes COLDWAR_KOR_1970_set_leader = yes add_timed_idea = { idea = COLDWAR_KOR_security_directorate_burden days = 180 } }
 }
 COLDWAR_KOR_nominate_kjp = {
  fire_only_once = no
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_constitutional_order has_elections = yes check_variable = { party_banned_array^0 = 0 } check_variable = { party_pop_array^0 > 0 } NOT = { has_country_flag = COLDWAR_KOR_kjp_nominated } }
  complete_effect = { set_country_flag = COLDWAR_KOR_kjp_nominated }
 }
 COLDWAR_KOR_authorize_kjp_handover = {
  fire_only_once = yes
  available = { COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_civilian_succession_open check_variable = { party_banned_array^0 = 0 } check_variable = { party_pop_array^0 > 0 } NOT = { has_country_flag = COLDWAR_KOR_nationwide_martial_law } NOT = { has_country_flag = COLDWAR_KOR_constitutional_order } NOT = { has_country_flag = COLDWAR_KOR_kjp_successor } }
  complete_effect = { set_country_flag = COLDWAR_KOR_kjp_successor set_temp_variable = { rul_party_temp = 0 } set_temp_variable = { disable_elections = 1 } change_ruling_party_effect = yes clr_country_flag = COLDWAR_KOR_civilian_succession_open COLDWAR_KOR_1970_set_leader = yes }
 }
}
'''
    decisions = []
    party_names = {
        0: ("drp", "Democratic Republican Party"),
        1: ("ndp", "New Democratic Party"),
        2: ("two_kim_reform", "Two Kim Reform Movement"),
        3: ("usp", "Unification Socialist Party"),
        4: ("rpr", "Revolutionary Party for Reunification"),
        5: ("student_civic", "Student Civic Coalition"),
        19: ("independent_left", "Independent Southern Left"),
        22: ("army_djp", "Army and Democratic Justice Party"),
    }
    for slot, legal in [(0, ""), (1, ""), (2, ""), (3, ""), (4, "has_country_flag = COLDWAR_KOR_electoral_party_4_legal"), (5, "has_country_flag = COLDWAR_KOR_civic_legal_5"), (19, "has_country_flag = COLDWAR_KOR_civic_legal_19"), (22, "has_country_flag = COLDWAR_KOR_electoral_party_22_legal")]:
        legal_gate = (legal + " ") if legal else ""
        slug, party_name = party_names[slot]
        key = f"COLDWAR_KOR_{slug}"
        common = f"COLDWAR_KOR_political_scenario = yes has_country_flag = COLDWAR_KOR_talks_authorized NOT = {{ has_country_flag = COLDWAR_KOR_ballot_pending }} check_variable = {{ party_banned_array^{slot} = 0 }} check_variable = {{ party_pop_array^{slot} > 0 }} {legal_gate}"
        decisions.append(f''' COLDWAR_KOR_register_charter_endorsement_{slot} = {{
  fire_only_once = no
  days_re_enable = 1
  available = {{ {common} NOT = {{ has_country_flag = COLDWAR_KOR_charter_supporter_{slot} }} NOT = {{ has_country_flag = COLDWAR_KOR_charter_endorsement_pending_{slot} }} }}
  complete_effect = {{ set_country_flag = COLDWAR_KOR_charter_endorsement_pending_{slot} country_event = {{ id = COLDWAR_KOR_transition.{200 + slot} }} }}
 }}
 COLDWAR_KOR_withdraw_charter_endorsement_{slot} = {{
  fire_only_once = no
  days_re_enable = 1
  available = {{ {common} has_country_flag = COLDWAR_KOR_charter_supporter_{slot} }}
  complete_effect = {{ clr_country_flag = COLDWAR_KOR_charter_supporter_{slot} }}
 }}''')
        decisions[-1] = decisions[-1].replace(f"COLDWAR_KOR_register_charter_endorsement_{slot}", f"COLDWAR_KOR_request_charter_endorsement_{slug}").replace(f"COLDWAR_KOR_withdraw_charter_endorsement_{slot}", f"COLDWAR_KOR_withdraw_charter_endorsement_{slug}")
    base = base.rsplit("\n}\n", 1)[0] + "\n" + "\n".join(decisions) + "\n}\n"
    # The five-year presidential settlement is non-renewable for a person;
    # alternative parliamentary/consensus charters retain their own rules.
    base = base.replace("has_country_flag = COLDWAR_KOR_constitution_presidential has_country_flag = COLDWAR_KOR_constitution_consensus", "has_country_flag = COLDWAR_KOR_constitution_presidential has_country_flag = COLDWAR_KOR_constitution_parliamentary has_country_flag = COLDWAR_KOR_constitution_consensus")
    lines = base.splitlines()
    candidate = None
    for i, line in enumerate(lines):
        if line.strip().startswith("COLDWAR_KOR_nominate_"):
            candidate = line.strip().split(" =", 1)[0].removeprefix("COLDWAR_KOR_nominate_")
        elif line.strip().startswith("available =") and candidate in ("ys", "dj", "roh", "kjp"):
            gate = f"NOT = {{ AND = {{ check_variable = {{ COLDWAR_KOR_charter_model = 1 }} has_country_flag = COLDWAR_KOR_presidential_term_served_{candidate} }} }}"
            lines[i] = line.rstrip()[:-1] + gate + " }"
            candidate = None
    base = "\n".join(lines) + "\n"
    return base


def category_file():
    return HEADER + "\n" + block("COLDWAR_KOR_constitutional_decisions", "visible = { COLDWAR_KOR_political_scenario = yes }\nvisible_when_empty = yes\npriority = 40")


def events_file():
    out = [HEADER, "add_namespace = COLDWAR_KOR_transition"]
    out.append('''country_event = {
 id = COLDWAR_KOR_transition.230
 title = COLDWAR_KOR_transition.230.t
 desc = COLDWAR_KOR_transition.230.d
 is_triggered_only = yes
 option = { name = COLDWAR_KOR_transition.230.option_a trigger = { has_country_flag = COLDWAR_KOR_ys_merger_pending check_variable = { party_banned_array^2 = 0 } check_variable = { party_pop_array^2 > 0 } NOT = { has_country_flag = COLDWAR_KOR_conservative_merger_ratified } } set_country_flag = COLDWAR_KOR_ys_merger_authorized clr_country_flag = COLDWAR_KOR_ys_merger_pending }
 option = { name = COLDWAR_KOR_transition.230.option_b clr_country_flag = COLDWAR_KOR_ys_merger_pending }
}''')
    out.append('''country_event = {
 id = COLDWAR_KOR_transition.12
 title = COLDWAR_KOR_transition.12.t
 desc = COLDWAR_KOR_transition.12.d
 is_triggered_only = yes
 option = { name = COLDWAR_KOR_transition.12.option_a trigger = { has_country_flag = COLDWAR_KOR_caretaker_installed NOT = { has_country_flag = COLDWAR_KOR_nationwide_martial_law } } add_political_power = -75 set_temp_variable = { treasury_change = -1 } modify_treasury_effect = yes add_timed_idea = { idea = COLDWAR_KOR_command_reorganization days = 90 } set_country_flag = COLDWAR_KOR_negotiating_commitment clr_country_flag = COLDWAR_KOR_command_settlement_pending }
 option = { name = COLDWAR_KOR_transition.12.option_b add_political_power = -25 set_country_flag = COLDWAR_KOR_military_reconsolidation set_country_flag = { flag = COLDWAR_KOR_talks_retry_cooldown days = 90 } clr_country_flag = COLDWAR_KOR_command_settlement_pending clr_country_flag = COLDWAR_KOR_negotiating_commitment clr_country_flag = COLDWAR_KOR_caretaker_installed clr_country_flag = COLDWAR_KOR_transition_open clr_country_flag = COLDWAR_KOR_military_opening_authorized }
}
country_event = {
 id = COLDWAR_KOR_transition.30
 title = COLDWAR_KOR_transition.30.t
 desc = COLDWAR_KOR_transition.30.d
 is_triggered_only = yes
 immediate = { if = { limit = { has_country_flag = COLDWAR_KOR_ballot_pending has_country_flag = COLDWAR_KOR_charter_mandate check_variable = { COLDWAR_KOR_charter_model > 0 } check_variable = { COLDWAR_KOR_charter_model < 4 } } COLDWAR_KOR_calculate_charter_vote = yes if = { limit = { check_variable = { COLDWAR_KOR_charter_support_share > 0.5 } } set_country_flag = COLDWAR_KOR_constitutional_ratification_passed clr_country_flag = COLDWAR_KOR_ballot_pending clr_country_flag = COLDWAR_KOR_charter_rejected if = { limit = { check_variable = { COLDWAR_KOR_charter_model = 1 } } set_country_flag = COLDWAR_KOR_constitution_presidential } if = { limit = { check_variable = { COLDWAR_KOR_charter_model = 2 } } set_country_flag = COLDWAR_KOR_constitution_parliamentary } if = { limit = { check_variable = { COLDWAR_KOR_charter_model = 3 } } set_country_flag = COLDWAR_KOR_constitution_consensus } } else = { clr_country_flag = COLDWAR_KOR_ballot_pending set_country_flag = COLDWAR_KOR_charter_rejected set_country_flag = { flag = COLDWAR_KOR_charter_retry_cooldown days = 90 } } } }
 option = { name = COLDWAR_KOR_transition.30.option_a }
}
country_event = { id = COLDWAR_KOR_transition.88 title = COLDWAR_KOR_transition.88.t desc = COLDWAR_KOR_transition.88.d is_triggered_only = yes option = { name = COLDWAR_KOR_transition.88.option_a trigger = { COLDWAR_KOR_pending_court_commission = yes } set_country_flag = COLDWAR_KOR_judicial_review_operational clr_country_flag = COLDWAR_KOR_court_implementation_pending clr_country_flag = COLDWAR_KOR_court_event_queued } option = { name = COLDWAR_KOR_transition.88.option_b trigger = { NOT = { COLDWAR_KOR_pending_court_commission = yes } } clr_country_flag = COLDWAR_KOR_court_event_queued } }
country_event = {
 id = COLDWAR_KOR_transition.100
 title = COLDWAR_KOR_historical.1979.t
 desc = COLDWAR_KOR_historical.1979.d
 trigger = { tag = KOR IMP_is_1970_scenario = yes date > 1979.10.25 date < 1979.10.28 has_country_leader = { name = "Park Chung Hee" ruling_only = yes } has_country_flag = COLDWAR_KOR_park_succession_unresolved }
 mean_time_to_happen = { days = 1 }
 fire_only_once = yes
 option = { name = COLDWAR_KOR_historical.1979.option_a clr_country_flag = COLDWAR_KOR_park_succession_unresolved set_country_flag = COLDWAR_KOR_select_interim_choi set_temp_variable = { rul_party_temp = 0 } set_temp_variable = { disable_elections = 1 } change_ruling_party_effect = yes set_country_flag = COLDWAR_KOR_transition_open set_country_flag = COLDWAR_KOR_civilian_succession_open add_timed_idea = { idea = COLDWAR_KOR_interim_government days = 180 } }
 option = { name = COLDWAR_KOR_historical.1979.option_b clr_country_flag = COLDWAR_KOR_park_succession_unresolved set_country_flag = COLDWAR_KOR_select_interim_choi set_temp_variable = { rul_party_temp = 0 } set_temp_variable = { disable_elections = 1 } change_ruling_party_effect = yes set_country_flag = COLDWAR_KOR_officer_council_contest add_timed_idea = { idea = COLDWAR_KOR_contested_command days = 90 } }
}
''')
    # Each organization receives an explicit RP response before its unique
    # native-support share can enter the constitutional ballot.
    party_names = {
        0: ("drp", "Democratic Republican Party"),
        1: ("ndp", "New Democratic Party"),
        2: ("two_kim_reform", "Two Kim Reform Movement"),
        3: ("usp", "Unification Socialist Party"),
        4: ("rpr", "Revolutionary Party for Reunification"),
        5: ("student_civic", "Student Civic Coalition"),
        19: ("independent_left", "Independent Southern Left"),
        22: ("army_djp", "Army and Democratic Justice Party"),
    }
    party_legality = {
        4: "has_country_flag = COLDWAR_KOR_electoral_party_4_legal",
        5: "has_country_flag = COLDWAR_KOR_civic_legal_5",
        19: "has_country_flag = COLDWAR_KOR_civic_legal_19",
        22: "has_country_flag = COLDWAR_KOR_electoral_party_22_legal",
    }
    for slot in (0, 1, 2, 3, 4, 5, 19, 22):
        slug, _ = party_names[slot]
        legal = party_legality.get(slot, "")
        legal = (legal + " ") if legal else ""
        out.append(f'''country_event = {{
 id = COLDWAR_KOR_transition.{200 + slot}
 title = COLDWAR_KOR_transition.{200 + slot}.t
 desc = COLDWAR_KOR_transition.{200 + slot}.d
 is_triggered_only = yes
 trigger = {{ original_tag = KOR IMP_is_1970_scenario = yes has_country_flag = COLDWAR_KOR_charter_endorsement_pending_{slot} }}
 option = {{ name = COLDWAR_KOR_transition.{200 + slot}.option_a trigger = {{ {legal}check_variable = {{ party_banned_array^{slot} = 0 }} check_variable = {{ party_pop_array^{slot} > 0 }} }} set_country_flag = COLDWAR_KOR_charter_supporter_{slot} clr_country_flag = COLDWAR_KOR_charter_endorsement_pending_{slot} }}
 option = {{ name = COLDWAR_KOR_transition.{200 + slot}.option_b clr_country_flag = COLDWAR_KOR_charter_endorsement_pending_{slot} }}
}}
''')
    # Dated histories only appear when their named crisis has actually been
    # established by the native government or player, once per receipt.
    events = [("labour_1970","1970.11.13","labour_crisis_open"),("transition_1971","1971.4.27","1971_contest_pending"),("yh_1979","1979.8.11","yh_case_open"),("buma_1979","1979.10.16","buma_crisis_open"),("martial_law_may17","1980.5.17","officer_control_crisis"),("transition_gwangju","1980.5.18","nationwide_martial_law"),("transition_1985","1985.2.12","opposition_reorganization_pending"),("park_jongcheol_1987","1987.1.14","torture_disclosure_crisis"),("april13_1987","1987.4.13","opposition_constitutional_demand"),("june_movement_1987","1987.6.10","constitutional_mobilization"),("workers_1987","1987.7.1","post_june_labor_wave"),("eight_member_talks","1987.8.31","charter_mandate"),("court_1988","1988.9.1","court_commissioning_delay"),("transition_1990","1990.1.22","merger_talks_pending")]
    outcomes = {
        "labour_1970": ("set_country_flag = COLDWAR_KOR_labour_1970_recorded\nset_country_flag = COLDWAR_KOR_labour_inspection_authorized", "set_country_flag = COLDWAR_KOR_labour_1970_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_wage_discipline days = 180 }"),
        "transition_1971": ("add_political_power = -50\nadd_stability = 0.03\nset_country_flag = COLDWAR_KOR_constitutional_crisis\nset_country_flag = COLDWAR_KOR_electoral_opening", "add_political_power = 50\nadd_stability = -0.05\nset_country_flag = COLDWAR_KOR_constitutional_crisis\nset_country_flag = COLDWAR_KOR_executive_emergency_proposed"),
        "yh_1979": ("set_country_flag = COLDWAR_KOR_yh_case_recorded\nset_country_flag = COLDWAR_KOR_workplace_mediation_authorized", "set_country_flag = COLDWAR_KOR_yh_case_recorded\nset_country_flag = COLDWAR_KOR_repression_costs_recorded"),
        "buma_1979": ("set_country_flag = COLDWAR_KOR_buma_crisis_recorded\nset_country_flag = COLDWAR_KOR_military_opening_authorized", "set_country_flag = COLDWAR_KOR_buma_crisis_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_emergency_controls days = 180 }"),
        "martial_law_may17": ("set_country_flag = COLDWAR_KOR_may17_decision_recorded\nset_country_flag = COLDWAR_KOR_transition_open", "set_country_flag = COLDWAR_KOR_may17_decision_recorded\nset_country_flag = COLDWAR_KOR_nationwide_martial_law\nadd_ideas = COLDWAR_KOR_martial_law_legitimacy_scar"),
        "transition_gwangju": ("add_political_power = -75\nset_country_flag = COLDWAR_KOR_gwangju_case_recorded\nset_country_flag = COLDWAR_KOR_military_opening_authorized", "set_country_flag = COLDWAR_KOR_gwangju_case_recorded\nset_country_flag = COLDWAR_KOR_controlled_fifth_republic"),
        "transition_1985": ("add_political_power = -50\nset_country_flag = COLDWAR_KOR_opposition_reorganized\nset_country_flag = COLDWAR_KOR_opposition_constitutional_demand", "set_country_flag = COLDWAR_KOR_opposition_reorganized\nset_country_flag = COLDWAR_KOR_separate_democratic_organizations"),
        "park_jongcheol_1987": ("set_country_flag = COLDWAR_KOR_torture_disclosure_recorded\nset_country_flag = COLDWAR_KOR_case_records_preserved\nset_country_flag = COLDWAR_KOR_independent_inquiry_authorized", "set_country_flag = COLDWAR_KOR_torture_disclosure_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_disclosure_suppression days = 180 }"),
        "april13_1987": ("set_country_flag = COLDWAR_KOR_april13_position_recorded\nset_country_flag = COLDWAR_KOR_military_opening_authorized", "set_country_flag = COLDWAR_KOR_april13_position_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_indirect_selection_crisis days = 180 }"),
        "june_movement_1987": ("set_country_flag = COLDWAR_KOR_june_mobilization_recorded\nset_country_flag = COLDWAR_KOR_charter_mandate", "set_country_flag = COLDWAR_KOR_june_mobilization_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_unresolved_constitutional_crisis days = 180 }"),
        "workers_1987": ("set_country_flag = COLDWAR_KOR_workers_1987_recorded\nset_country_flag = COLDWAR_KOR_lawful_labour_bargaining", "set_country_flag = COLDWAR_KOR_workers_1987_recorded\nadd_timed_idea = { idea = COLDWAR_KOR_labour_conflict days = 180 }"),
        "eight_member_talks": ("set_country_flag = COLDWAR_KOR_charter_negotiations_recorded\nset_country_flag = COLDWAR_KOR_ballot_pending\ncountry_event = { id = COLDWAR_KOR_transition.30 days = 30 }", "set_country_flag = COLDWAR_KOR_charter_negotiations_recorded"),
        "court_1988": ("if = { limit = { COLDWAR_KOR_pending_court_commission = yes } set_country_flag = COLDWAR_KOR_judicial_review_operational clr_country_flag = COLDWAR_KOR_court_implementation_pending }", "set_country_flag = COLDWAR_KOR_court_appointments_delayed"),
        "transition_1990": ("set_country_flag = COLDWAR_KOR_1990_merger_recorded\nset_country_flag = COLDWAR_KOR_conservative_merger_ratified\nadd_political_power = 75\nadd_stability = -0.03", "set_country_flag = COLDWAR_KOR_1990_merger_recorded\nadd_political_power = 25"),
    }
    for index, (ident, date, receipt) in enumerate(events, start=101):
        year = date.split('.')[0]
        eid = "COLDWAR_KOR_transition." + str(index)
        locid = "COLDWAR_KOR_" + ident
        recorded = "COLDWAR_KOR_" + ident + "_recorded"
        out.append(f'''country_event = {{
 id = {eid}
 title = {locid}.t
 desc = {locid}.d
 trigger = {{ original_tag = KOR IMP_is_1970_scenario = yes date > {date} date < {year}.12.31 has_country_flag = COLDWAR_KOR_{receipt} NOT = {{ has_country_flag = {recorded} }} }}
 mean_time_to_happen = {{ days = 1 }}
 option = {{ name = {locid}.option_a {outcomes[ident][0]} set_country_flag = {recorded} }}
 option = {{ name = {locid}.option_b {outcomes[ident][1]} set_country_flag = {recorded} }}
}}
''')
    return "\n".join(out)


def ideas_file():
    ideas = {
        "COLDWAR_KOR_interim_government": "political_power_factor = -0.1\nstability_factor = -0.03",
        "COLDWAR_KOR_contested_command": "army_org_factor = -0.05\nstability_factor = -0.05",
        "COLDWAR_KOR_martial_law_legitimacy_scar": "stability_factor = -0.08\ntrade_opinion_factor = -0.05\npolice_cost_multiplier_modifier = 0.08",
        "COLDWAR_KOR_accountability_settlement": "stability_factor = -0.03\nbureaucracy_cost_multiplier_modifier = 0.04",
        "COLDWAR_KOR_wage_discipline": "stability_factor = -0.03\ncivilian_factories_productivity = 0.02",
        "COLDWAR_KOR_emergency_controls": "stability_factor = -0.05\npolitical_power_factor = -0.04",
        "COLDWAR_KOR_disclosure_suppression": "stability_factor = -0.04\ntrade_opinion_factor = -0.03\npolice_cost_multiplier_modifier = 0.04",
        "COLDWAR_KOR_indirect_selection_crisis": "stability_factor = -0.04\npolitical_power_factor = -0.03",
        "COLDWAR_KOR_unresolved_constitutional_crisis": "stability_factor = -0.04\npolice_cost_multiplier_modifier = 0.04",
        "COLDWAR_KOR_labour_conflict": "stability_factor = -0.03\ncivilian_factories_productivity = -0.02",
        "COLDWAR_KOR_revolutionary_settlement_burden": "stability_factor = -0.08\ncivilian_factories_productivity = -0.05",
        "COLDWAR_KOR_security_directorate_burden": "trade_opinion_factor = -0.05\npolice_cost_multiplier_modifier = 0.05",
        "COLDWAR_KOR_civic_legalization_adjustment": "political_power_factor = -0.05",
    }
    families = {
        "COLDWAR_KOR_interim_government": "political",
        "COLDWAR_KOR_contested_command": "army",
        "COLDWAR_KOR_martial_law_legitimacy_scar": "political",
        "COLDWAR_KOR_accountability_settlement": "political",
        "COLDWAR_KOR_wage_discipline": "industry",
        "COLDWAR_KOR_emergency_controls": "political",
        "COLDWAR_KOR_disclosure_suppression": "political",
        "COLDWAR_KOR_indirect_selection_crisis": "political",
        "COLDWAR_KOR_unresolved_constitutional_crisis": "political",
        "COLDWAR_KOR_labour_conflict": "industry",
        "COLDWAR_KOR_revolutionary_settlement_burden": "political",
        "COLDWAR_KOR_security_directorate_burden": "political",
        "COLDWAR_KOR_civic_legalization_adjustment": "political",
    }
    out = [HEADER, "ideas = {\n\tcountry = {"]
    for ident, mods in ideas.items():
        out.append(f"\t\t{ident} = {{\n\t\t\tallowed = {{ original_tag = KOR IMP_is_1970_scenario = yes }}\n\t\t\tpicture = GFX_idea_COLDWAR_KOR_spirit_{families[ident]}\n\t\t\tmodifier = {{\n" + "\n".join("\t\t\t\t" + x for x in mods.splitlines()) + "\n\t\t\t}\n\t\t}")
    out.append("\t}\n}\n")
    return "\n".join(out)


def loc_file():
    entries = {
        "COLDWAR_KOR_transition.12.t": "The Command Challenge",
        "COLDWAR_KOR_transition.12.d": "The interim government must secure civilian authority within the armed forces. The cabinet may fund a reorganization or yield the command dispute.",
        "COLDWAR_KOR_transition.12.option_a": "Reorganize and Uphold Civilian Command",
        "COLDWAR_KOR_transition.12.option_b": "Yield the Command",
        "COLDWAR_KOR_transition.30.t": "The Constitutional Ballot",
        "COLDWAR_KOR_transition.30.d": "The charter passes only if recorded endorsements exceed half of current legal electoral parties’ combined native support. No candidate or election result is selected by this ballot.",
        "COLDWAR_KOR_transition.30.option_a": "Close the Ballot Record",
        "COLDWAR_KOR_transition.88.t": "Constitutional Review Becomes Operational",
        "COLDWAR_KOR_transition.88.d": "The funded appointments and commissioning period are complete. The constitutional court can now exercise judicial review.",
        "COLDWAR_KOR_transition.88.option_a": "Commence Judicial Review",
        "COLDWAR_KOR_transition.88.option_b": "Return the Funded Commission to Its Pending State",
        "COLDWAR_KOR_historical.1979.t": "A Presidential Succession Crisis",
        "COLDWAR_KOR_historical.1979.d": "Park Chung Hee’s death leaves the constitutional succession unresolved. The historical civilian route installs Choi Kyu-hah as caretaker; military command remains a separate contest.",
        "COLDWAR_KOR_historical.1979.option_a": "Support the Interim Civilian Government",
        "COLDWAR_KOR_historical.1979.option_b": "Submit to an Officer Council",
        "COLDWAR_KOR_constitutional_decisions": "Constitutional Settlement",
        "COLDWAR_KOR_constitutional_decisions_desc": "Party and public decisions concerning the transition to constitutional government.",
        "COLDWAR_KOR_reopen_constitutional_talks": "Reopen Constitutional Negotiations",
        "COLDWAR_KOR_reopen_constitutional_talks_desc": "Answer the opposition’s demand for constitutional revision and authorize renewed negotiations after military reconsolidation.",
        "COLDWAR_KOR_reopen_charter_ballot": "Resubmit the Constitutional Charter",
        "COLDWAR_KOR_reopen_charter_ballot_desc": "Return the selected constitutional draft to ratification after the previous ballot failed. The negotiating mandate and the required interval must remain valid.",
        "COLDWAR_KOR_implement_constitutional_court": "Commission the Constitutional Court",
        "COLDWAR_KOR_implement_constitutional_court_desc": "Fund judicial appointments and the court’s ninety-day commissioning period under the ratified constitution.",
        "COLDWAR_KOR_review_repression_cases": "Review Political Repression Cases",
        "COLDWAR_KOR_review_repression_cases_desc": "Authorize an independent review of political repression and begin an accountability settlement once nationwide martial law has ended.",
        "COLDWAR_KOR_authorize_djp_merger": "Authorize the DJP Merger Mandate",
        "COLDWAR_KOR_authorize_djp_merger_desc": "The established Democratic Justice Party accepts negotiations with the RDP and NDRP.",
        "COLDWAR_KOR_authorize_ys_merger": "Authorize the RDP Merger Mandate",
        "COLDWAR_KOR_authorize_ys_merger_desc": "Kim Young-sam’s Reunification Democratic Party accepts negotiations with the DJP and NDRP.",
        "COLDWAR_KOR_authorize_ndrp_merger": "Authorize the NDRP Merger Mandate",
        "COLDWAR_KOR_authorize_ndrp_merger_desc": "The New Democratic Republican Party accepts negotiations with the DJP and RDP.",
        "COLDWAR_KOR_open_conservative_merger": "Convene the Conservative Merger Talks",
        "COLDWAR_KOR_open_conservative_merger_desc": "Each participating organization has separately authorized talks. Kim Dae-jung’s party remains outside this agreement.",
        **{f"COLDWAR_KOR_request_charter_endorsement_{slug}": f"Request Charter Endorsement from the {name}" for slug, name in (("drp", "Democratic Republican Party"), ("ndp", "New Democratic Party"), ("two_kim_reform", "Two Kim Reform Movement"), ("usp", "Unification Socialist Party"), ("rpr", "Revolutionary Party for Reunification"), ("student_civic", "Student Civic Coalition"), ("independent_left", "Independent Southern Left"), ("army_djp", "Army and Democratic Justice Party"))},
        **{f"COLDWAR_KOR_request_charter_endorsement_{slug}_desc": f"Request a separate response from the {name}. No popularity or electoral result is changed." for slug, name in (("drp", "Democratic Republican Party"), ("ndp", "New Democratic Party"), ("two_kim_reform", "Two Kim Reform Movement"), ("usp", "Unification Socialist Party"), ("rpr", "Revolutionary Party for Reunification"), ("student_civic", "Student Civic Coalition"), ("independent_left", "Independent Southern Left"), ("army_djp", "Army and Democratic Justice Party"))},
        **{f"COLDWAR_KOR_withdraw_charter_endorsement_{slug}": f"Withdraw the {name} Charter Endorsement" for slug, name in (("drp", "Democratic Republican Party"), ("ndp", "New Democratic Party"), ("two_kim_reform", "Two Kim Reform Movement"), ("usp", "Unification Socialist Party"), ("rpr", "Revolutionary Party for Reunification"), ("student_civic", "Student Civic Coalition"), ("independent_left", "Independent Southern Left"), ("army_djp", "Army and Democratic Justice Party"))},
        **{f"COLDWAR_KOR_withdraw_charter_endorsement_{slug}_desc": f"Withdraw the {name} endorsement while the organization remains legally represented and before the ballot is submitted." for slug, name in (("drp", "Democratic Republican Party"), ("ndp", "New Democratic Party"), ("two_kim_reform", "Two Kim Reform Movement"), ("usp", "Unification Socialist Party"), ("rpr", "Revolutionary Party for Reunification"), ("student_civic", "Student Civic Coalition"), ("independent_left", "Independent Southern Left"), ("army_djp", "Army and Democratic Justice Party"))},
        **{f"COLDWAR_KOR_transition.{200 + slot}.t": f"Charter Endorsement: {name}" for slot, (slug, name) in {0: ("drp", "Democratic Republican Party"), 1: ("ndp", "New Democratic Party"), 2: ("two_kim_reform", "Two Kim Reform Movement"), 3: ("usp", "Unification Socialist Party"), 4: ("rpr", "Revolutionary Party for Reunification"), 5: ("student_civic", "Student Civic Coalition"), 19: ("independent_left", "Independent Southern Left"), 22: ("army_djp", "Army and Democratic Justice Party")}.items()},
        **{f"COLDWAR_KOR_transition.{200 + slot}.d": f"The {name} is asked to accept or decline the proposed constitutional terms. Its recorded native support counts once only if it endorses." for slot, (slug, name) in {0: ("drp", "Democratic Republican Party"), 1: ("ndp", "New Democratic Party"), 2: ("two_kim_reform", "Two Kim Reform Movement"), 3: ("usp", "Unification Socialist Party"), 4: ("rpr", "Revolutionary Party for Reunification"), 5: ("student_civic", "Student Civic Coalition"), 19: ("independent_left", "Independent Southern Left"), 22: ("army_djp", "Army and Democratic Justice Party")}.items()},
        **{f"COLDWAR_KOR_transition.{200 + slot}.option_a": "Accept the Constitutional Terms" for slot in (0, 1, 2, 3, 4, 5, 19, 22)},
        **{f"COLDWAR_KOR_transition.{200 + slot}.option_b": "Decline the Constitutional Terms" for slot in (0, 1, 2, 3, 4, 5, 19, 22)},
        "COLDWAR_KOR_nominate_ys": "Register Kim Young-sam’s Electoral Candidacy",
        "COLDWAR_KOR_nominate_ys_desc": "The Forties reform party places Kim Young-sam on its lawful electoral ticket. This nomination does not guarantee a party victory.",
        "COLDWAR_KOR_nominate_dj": "Register Kim Dae-jung’s Electoral Candidacy",
        "COLDWAR_KOR_nominate_dj_desc": "The Forties reform party places Kim Dae-jung on its lawful electoral ticket. This nomination does not guarantee a party victory.",
        "COLDWAR_KOR_nominate_roh": "Register Roh Tae-woo’s Presidential Candidacy",
        "COLDWAR_KOR_nominate_roh_desc": "The legally formed Democratic Justice Party nominates Roh Tae-woo under the direct-election settlement. The native election remains decisive.",
        "COLDWAR_KOR_authorize_military_succession": "Authorize a Military Cabinet",
        "COLDWAR_KOR_authorize_military_succession_desc": "The officer council claims the succession and installs Chun Doo-hwan through the native ruling-party transition. This is an alternate political outcome, not the automatic result of Park’s death.",
        "COLDWAR_KOR_ratify_revolutionary_settlement": "Ratify the Revolutionary Settlement",
        "COLDWAR_KOR_ratify_revolutionary_settlement_desc": "After an actual revolutionary or electoral accession, ratify the Southern revolutionary cabinet. Reorganizing the state imposes a ninety-day stability and industrial burden.",
        "COLDWAR_KOR_transition.230.t": "The Reunification Democratic Party’s Merger Mandate",
        "COLDWAR_KOR_transition.230.d": "Kim Young-sam’s organization must decide whether to join the conservative merger negotiations. Kim Dae-jung’s organization remains outside these terms.",
        "COLDWAR_KOR_transition.230.option_a": "Authorize the RDP Negotiators",
        "COLDWAR_KOR_transition.230.option_b": "Retain an Independent Organization",
        "COLDWAR_KOR_form_democratic_justice_party": "Constitute the Democratic Justice Party",
        "COLDWAR_KOR_form_democratic_justice_party_desc": "The Army-led government formalizes the Democratic Justice Party as an electoral organization. This creates neither support nor a presidential result.",
        "COLDWAR_KOR_authorize_security_directorate": "Authorize an Exceptional Security Directorate",
        "COLDWAR_KOR_authorize_security_directorate_desc": "During a documented command crisis and severe instability, the cabinet may install a security caretaker at a high political and administrative cost.",
        "COLDWAR_KOR_nominate_kjp": "Register Kim Jong-pil for a Native Election",
        "COLDWAR_KOR_nominate_kjp_desc": "Record Kim Jong-pil as the Democratic Republican Party candidate. This nomination does not change the incumbent or predetermine the native result.",
        "COLDWAR_KOR_authorize_kjp_handover": "Authorize the Civilian Succession to Kim Jong-pil",
        "COLDWAR_KOR_authorize_kjp_handover_desc": "With a civilian succession explicitly open and the Democratic Republican Party represented, authorize a noncompetitive party handover through the native ruling-party system.",
        "COLDWAR_KOR_revolutionary_settlement_burden": "Revolutionary Settlement Burden",
        "COLDWAR_KOR_revolutionary_settlement_burden_desc": "The revolutionary party’s entry carries a temporary stability and industrial productivity cost.",
        "COLDWAR_KOR_security_directorate_burden": "Security Directorate Burden",
        "COLDWAR_KOR_security_directorate_burden_desc": "Exceptional security government incurs diplomatic and policing costs during its first six months.",
        "COLDWAR_KOR_legalize_civic_parties": "Legalize Civic Political Organizations",
        "COLDWAR_KOR_legalize_civic_parties_desc": "Authorize student civic and independent left organizations to contest elections. Legal recognition grants neither an electoral mandate nor a place in government.",
        "COLDWAR_KOR_civic_legalization_adjustment": "Civic Legalization Adjustment",
        "COLDWAR_KOR_civic_legalization_adjustment_desc": "Political institutions adjust to newly recognized civic organizations.",
        "COLDWAR_KOR_labour_1970.t": "Labour Law and Enforcement",
        "COLDWAR_KOR_transition_1971.t": "The Presidential Contest",
        "COLDWAR_KOR_yh_1979.t": "YH and the Parliamentary Opposition",
        "COLDWAR_KOR_buma_1979.t": "The Busan–Masan Crisis",
        "COLDWAR_KOR_martial_law_may17.t": "The Nationwide Martial-Law Decision",
        "COLDWAR_KOR_transition_gwangju.t": "The Martial-Law Crisis",
        "COLDWAR_KOR_transition_1985.t": "The Opposition Reorganizes",
        "COLDWAR_KOR_park_jongcheol_1987.t": "Torture, Disclosure and Accountability",
        "COLDWAR_KOR_april13_1987.t": "Constitutional Defense or Revision",
        "COLDWAR_KOR_june_movement_1987.t": "The June Democracy Movement",
        "COLDWAR_KOR_workers_1987.t": "The Great Workers’ Struggle",
        "COLDWAR_KOR_eight_member_talks.t": "The Constitutional Bargain",
        "COLDWAR_KOR_court_1988.t": "Constitutional Review Becomes Operational",
        "COLDWAR_KOR_transition_1990.t": "The Conservative Coalition Talks",
        "COLDWAR_KOR_interim_government": "Interim Civilian Government",
        "COLDWAR_KOR_interim_government_desc": "A temporary caretaker administration must govern without a settled electoral mandate.",
        "COLDWAR_KOR_contested_command": "Contested Command",
        "COLDWAR_KOR_contested_command_desc": "Military command remains disputed during the succession crisis.",
        "COLDWAR_KOR_martial_law_legitimacy_scar": "Martial-Law Legitimacy Scar",
        "COLDWAR_KOR_martial_law_legitimacy_scar_desc": "Emergency rule and its violent enforcement impose enduring legitimacy and administrative costs.",
        "COLDWAR_KOR_accountability_settlement": "Accountability Settlement",
        "COLDWAR_KOR_accountability_settlement_desc": "Independent review and compensation begin without erasing the historical record.",
        "COLDWAR_KOR_wage_discipline": "Wage Discipline",
        "COLDWAR_KOR_wage_discipline_desc": "Export production remains prioritized amid unresolved workplace protections.",
        "COLDWAR_KOR_emergency_controls": "Emergency Controls",
        "COLDWAR_KOR_emergency_controls_desc": "Emergency powers impose political and economic costs on ordinary administration.",
        "COLDWAR_KOR_disclosure_suppression": "Disclosure Suppression",
        "COLDWAR_KOR_disclosure_suppression_desc": "Attempts to suppress evidence deepen the credibility and enforcement burden.",
        "COLDWAR_KOR_indirect_selection_crisis": "Indirect Selection Crisis",
        "COLDWAR_KOR_indirect_selection_crisis_desc": "The defense of indirect presidential selection leaves the constitutional crisis unresolved.",
        "COLDWAR_KOR_unresolved_constitutional_crisis": "Unresolved Constitutional Crisis",
        "COLDWAR_KOR_unresolved_constitutional_crisis_desc": "The government has declined the negotiating mandate while civic mobilization continues.",
        "COLDWAR_KOR_labour_conflict": "Industrial Labour Conflict",
        "COLDWAR_KOR_labour_conflict_desc": "Restrictions on new unions prolong disruption across industrial workplaces.",
    }
    names = {
        "labour_1970": ("Labour Law and Enforcement", "Jeon Tae-il’s protest exposes unsafe conditions and failed enforcement. The government must choose inspection or wage discipline.", "Enforce Existing Protections", "Retain Wage Discipline"),
        "transition_1971": ("The Presidential Contest", "The 1971 contest tests the amended presidential order. The government chooses a competitive mandate or an executive emergency.", "Respect the Competitive Mandate", "Prepare an Executive Emergency"),
        "yh_1979": ("YH and the Parliamentary Opposition", "The YH workers’ sit-in and police raid connect workplace grievances to the opposition crisis.", "Accept Workplace Mediation", "Clear the Political Occupation"),
        "buma_1979": ("The Busan–Masan Crisis", "Regional protest follows Kim Young-sam’s exclusion during the late-Yushin crisis.", "Open a Political Channel", "Maintain Emergency Rule"),
        "martial_law_may17": ("The Nationwide Martial-Law Decision", "The officer-led government decides whether emergency rule will extend nationwide. This is separate from the later Gwangju crisis.", "Continue Civilian Talks", "Extend Nationwide Martial Law"),
        "transition_gwangju": ("The Martial-Law Crisis", "The May uprising and violent suppression leave a lasting accountability claim, distinct from the December 1979 officer challenge.", "Negotiate Civilian Guarantees", "Extend Nationwide Martial Law"),
        "transition_1985": ("The Opposition Reorganizes", "The opposition’s parliamentary breakthrough reconnects the constitutional campaign and the Two Kims’ organizations.", "A Joint Reform Ticket", "Separate Democratic Organizations"),
        "park_jongcheol_1987": ("Torture, Disclosure and Accountability", "Park Jong-cheol’s death in police custody and the attempted cover-up intensify the constitutional crisis.", "Protect the Investigation", "Suppress Disclosure"),
        "april13_1987": ("Constitutional Defense or Revision", "The government must answer the demand to replace indirect presidential selection.", "Accept Revision Talks", "Defend Indirect Selection"),
        "june_movement_1987": ("The June Democracy Movement", "The June mobilization brings the constitutional question to the streets. Only an actual government response can open negotiations.", "Authorize a Negotiating Mandate", "Refuse the Demand"),
        "workers_1987": ("The Great Workers’ Struggle", "The post-June industrial organizing wave raises labour demands beyond constitutional settlement.", "Recognize Lawful Bargaining", "Restrict the New Unions"),
        "eight_member_talks": ("The Constitutional Bargain", "Ruling and opposition representatives must submit an agreed text or return to negotiation.", "Submit the Agreed Text", "Return to Negotiation"),
        "court_1988": ("Constitutional Review Becomes Operational", "The court’s constitutional establishment and its operational start are distinct stages.", "Commence Judicial Review", "Delay Appointments"),
        "transition_1990": ("The Conservative Coalition Talks", "The Democratic Justice Party, Reunification Democratic Party and New Democratic Republican Party consider a merger. Kim Dae-jung’s organization remains outside unless it separately agrees.", "Ratify the Conservative Merger", "Keep the Parties Independent"),
    }
    for key, (title, desc, a, b) in names.items():
        entries[f"COLDWAR_KOR_{key}.t"] = title
        entries[f"COLDWAR_KOR_{key}.d"] = desc
        entries[f"COLDWAR_KOR_{key}.option_a"] = a
        entries[f"COLDWAR_KOR_{key}.option_b"] = b
    action_hints = {
        "resolve_command_challenge": "Opens the command settlement event; it does not appoint a military president.",
        "submit_constitutional_ballot": "Begins a 30-day ballot resolved from recorded endorsements and current native party support.",
        "configure_lawful_election": "Enacts lawful election administration after charter ratification; the native election system selects the incumbent.",
        "open_constitutional_dossier": "Opens the constitutional negotiation route. It does not pass a charter or name an office-holder.",
        "legal_civic_associations": "Legalizes civic participation for slots 5 and 19 without changing party popularity or government.",
        "confirm_native_handover": "Records a handover only after a lawful native election has resolved.",
        "constitutional_review_rules": "Enacts the court mandate; appointments and funded commissioning remain necessary before review begins.",
        "conservative_merger": "Records a conservative coalition identity only after the participating parties ratify the merger.",
    }
    for action, hint in action_hints.items():
        entries[f"COLDWAR_KOR_action_{action}_tt"] = hint
    return entries


def build(data):
    assert data.get("country") == "South Korea"
    files = {
        "common/scripted_effects/COLDWAR_KOR_1970_politics.txt": script_effects(),
        "common/scripted_triggers/COLDWAR_KOR_1970_politics.txt": trigger_file(),
        "common/decisions/COLDWAR_KOR_1970_politics.txt": decisions_file(),
        "common/decisions/categories/COLDWAR_KOR_1970_politics.txt": category_file(),
        "events/COLDWAR_KOR_1970_politics.txt": events_file(),
        "common/ideas/COLDWAR_KOR_1970_politics.txt": ideas_file(),
    }
    return files, loc_file()
