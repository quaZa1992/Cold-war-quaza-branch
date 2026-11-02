# IMPERIA COLD WAR — Chile 1970 political institutions and domestic events.
"""Build the Chilean election, crisis, and accountability runtime files.

The function is deliberately side-effect free. Callers may inspect or install
the returned file mapping; importing this module never writes to the mod.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tools/chile_1970/approved_design.json"
sys.path.insert(0,str(SOURCE.parent))
from current_design import load_design
from political_revision import INTERVENTION_DAYS, INTERVENTION_PP
P = "COLDWAR_CHL_"


def n(v):
    return f"{v:.5f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def idea(k):
    return f"{P}choice_{k}"


def _effect_cost(money):
    if not money:
        return ""
    return f"set_temp_variable = {{ treasury_change = -{n(money)} }} modify_treasury_effect = yes"


def _option_mods(k, mods, duration):
    if not mods:
        return ""
    args = " ".join(f"{key} = {n(value)}" for key, value in mods.items())
    return f"{idea(k)} = {{ modifier = {{ {args} }} }}"


def _event_option_effect(e, oi, opt):
    key = f"{e['key']}_{oi+1}"
    lines = [_effect_cost(opt.get("money", 0))]
    mods = _option_mods(key, opt.get("modifiers", {}), opt.get("duration"))
    if mods:
        if opt.get("duration"):
            lines.append(f"add_timed_idea = {{ idea = {idea(key)} days = {opt['duration']} }}")
        else:
            lines.append(f"add_ideas = {idea(key)}")
    if e["key"] == "election":
        slot = opt["party_support"]["party"]
        amount = opt["party_support"]["amount"]
        lines += [f"set_temp_variable = {{ party_index = {slot} }}", f"set_temp_variable = {{ party_popularity_increase = {n(amount)} }}", "change_relative_party_popularity = yes", f"set_country_flag = {P}campaign_{slot}"]
    elif e["key"] == "congress":
        if oi == 0:
            lines += [f"set_variable = {{ {P}election_confirmed_slot = {P}election_winner_slot }}", f"set_country_flag = {P}election_ratified"]
        else:
            lines += [f"if = {{ limit = {{ {P}congress_alternative_majority = yes }} set_variable = {{ {P}election_confirmed_slot = {P}election_runner_up_slot }} set_country_flag = {P}negotiated_alternative_majority set_country_flag = {P}election_ratified }}", f"else = {{ set_country_flag = {P}constitutional_crisis set_country_flag = {{ flag = {P}congress_retry value = 1 days = 7 }} clr_country_flag = {P}congress_event_seen }}"]
    elif e["key"] == "copper":
        lines.append(f"set_country_flag = {P}copper_settlement_{oi+1}")
    elif e["key"] == "transport":
        lines.append(f"set_country_flag = {P}transport_response_{oi+1}")
        if oi == 2:
            lines += [f"set_country_flag = {P}constitutional_crisis", f"set_country_flag = {P}military_intervention_condition"]
    elif e["key"] == "rupture":
        if oi == 0:
            lines += [f"set_country_flag = {P}constitutional_accord", f"set_country_flag = {P}rupture_resolved"]
        else:
            lines += [f"set_country_flag = {P}1970_calendar_superseded", f"set_country_flag = {P}military_government", f"set_country_flag = {P}pinochet_available", f"set_country_flag = {P}repression_occurred", f"set_country_flag = {P}rupture_resolved", "add_ideas = COLDWAR_CHL_repression", f"{P}clear_coalition_parameters = yes", "set_variable = { rul_party_temp = 22 }", "set_variable = { disable_elections = 1 }", "set_variable = { change_leader_temp = 0 }", "COLDWAR_CHL_apply_government_change = yes", "COLDWAR_CHL_sync_native_outlook = yes", f"set_variable = {{ {P}leader_slot = 22 }}", "COLDWAR_CHL_route_leader = yes", "COLDWAR_CHL_refresh_programmes = yes"]
    elif e["key"] == "junta":
        if oi == 0:
            lines += [f"set_country_flag = {P}constitutional_military_council", f"clr_country_flag = {P}pinochet_available", f"set_country_flag = {P}junta_decided"]
        else:
            lines += [f"set_country_flag = {P}pinochet_presidency", f"clr_country_flag = {P}constitutional_military_council", f"set_country_flag = {P}junta_decided", f"{P}clear_coalition_parameters = yes", "set_variable = { rul_party_temp = 22 }", "set_variable = { disable_elections = 1 }", "set_variable = { change_leader_temp = 0 }", "COLDWAR_CHL_apply_government_change = yes", "COLDWAR_CHL_sync_native_outlook = yes", f"set_variable = {{ {P}leader_slot = 22 }}", "COLDWAR_CHL_route_leader = yes", "COLDWAR_CHL_refresh_programmes = yes"]
    elif e["key"] == "repression":
        if oi == 0:
            lines += ["add_ideas = COLDWAR_CHL_repression", f"set_country_flag = {P}repression_occurred", f"set_country_flag = {P}repression_decided"]
        else:
            lines += [f"set_country_flag = {P}civilian_safeguards", f"set_country_flag = {P}repression_decided"]
    elif e["key"] == "banking":
        if oi == 0:
            lines += ["add_ideas = COLDWAR_CHL_bank_crisis", f"set_country_flag = {P}banking_crisis"]
        else:
            lines.append(f"set_country_flag = {P}bank_prevention_receipt")
    elif e["key"] == "early_exit":
        if oi == 0:
            lines += [f"set_country_flag = {P}early_exit_resolved", f"set_country_flag = {P}early_exit_election", f"{P}clear_coalition_parameters = yes", "set_variable = { rul_party_temp = ruling_party }", "set_variable = { disable_elections = 0 }", "set_variable = { change_leader_temp = 0 }", "COLDWAR_CHL_apply_government_change = yes", "COLDWAR_CHL_sync_native_outlook = yes", "set_temp_variable = { election_year_param = global.year }", "set_temp_variable = { election_month_param = global.month }", "set_temp_variable = { election_freq = 12 }", "set_country_flag = no_leader_change", "set_elections_with_frequency = yes", "clr_country_flag = no_leader_change"]
        else:
            lines += [f"set_country_flag = {{ flag = {P}early_exit_cooldown value = 1 days = 180 }}", f"clr_country_flag = {P}early_exit_event_seen"]
    elif e["key"] == "plebiscite":
        lines += [f"set_country_flag = {P}plebiscite_no_won" if oi == 0 else f"set_country_flag = {P}plebiscite_yes_won", f"set_country_flag = {P}plebiscite_decided"]
    elif e["key"] == "handover":
        lines += [f"set_country_flag = {P}civilian_handover", "COLDWAR_CHL_install_1990_candidate = yes", "COLDWAR_CHL_sync_native_outlook = yes", "COLDWAR_CHL_route_leader = yes", f"{P}record_1990_presidential_term = yes", "COLDWAR_CHL_refresh_programmes = yes"]
    elif e["key"] == "truth":
        if oi == 0:
            lines += ["remove_ideas = COLDWAR_CHL_repression", f"remove_ideas = COLDWAR_CHL_limited_accountability", "add_ideas = COLDWAR_CHL_lasting_legacy", f"set_country_flag = {P}reparations_full", f"set_country_flag = {P}truth_full"]
        else:
            lines += ["remove_ideas = COLDWAR_CHL_repression", "add_ideas = COLDWAR_CHL_limited_accountability", "add_ideas = COLDWAR_CHL_lasting_legacy", f"set_country_flag = {P}reparations_limited", f"set_country_flag = {P}truth_limited"]
    elif e["key"] == "andean":
        lines.append(f"set_country_flag = {P}andean_reviewed")
        if oi == 0:
            lines.append(f"set_country_flag = {P}andean_retained")
        else:
            lines += ["remove_ideas = COLDWAR_CHL_cartagena_member", f"set_country_flag = {P}andean_withdrawn", "COLDWAR_CHL_refresh_programmes = yes"]
    if opt.get("weekly", 0):
        lines.append(f"custom_effect_tooltip = {P}weekly_cost_{key}")
    repeatable = (e["key"] == "early_exit" and oi == 1) or (e["key"] == "congress" and oi == 1)
    if not repeatable:
        lines.append(f"set_country_flag = {P}{e['key']}_choice_resolved")
    return " ".join(x for x in lines if x)


def _event_trigger(e):
    key = e["key"]
    base = f"COLDWAR_CHL_is_scenario = yes"
    if key == "election": return f"{base} {P}civilian_calendar_active = yes date > 1969.12.31 date < 1970.9.4 NOT = {{ has_country_flag = {P}campaign_opened }}"
    if key == "congress": return f"{base} {P}civilian_calendar_active = yes date > 1970.10.23 has_country_flag = {P}election_ballot_counted NOT = {{ has_country_flag = {P}election_ratified }} NOT = {{ has_country_flag = {P}congress_retry }}"
    if key == "transport": return f"{base} date > 1972.9.30 date < 1972.11.1 has_country_flag = {P}high_confrontation check_variable = {{ ruling_party = 18 }} NOT = {{ has_country_flag = {P}transport_event_seen }}"
    if key == "rupture": return f"{P}can_resolve_rupture = yes"
    if key == "junta": return f"{base} has_country_flag = {P}military_government NOT = {{ has_country_flag = {P}junta_decided }}"
    if key == "banking": return f"{base} date > 1981.12.31 has_country_flag = {P}fragile_banks NOT = {{ has_idea = COLDWAR_CHL_banking_stress_test }} NOT = {{ has_country_flag = {P}bank_prevention_receipt }} NOT = {{ has_country_flag = {P}banking_crisis }}"
    if key == "andean": return f"{base} date > 1975.12.31 has_idea = COLDWAR_CHL_cartagena_member NOT = {{ has_country_flag = {P}andean_reviewed }}"
    return base


def _event_execution_guard(e, oi):
    """Recheck the live political context when the player selects an option."""
    key = e["key"]
    c = [f"{P}is_scenario = yes"]
    if key == "election":
        c += [f"{P}civilian_calendar_active = yes", f"NOT = {{ has_country_flag = {P}election_ballot_counted }}", "date > 1969.12.31", "date < 1970.9.4"]
    elif key == "congress":
        c += [f"{P}civilian_calendar_active = yes", f"has_country_flag = {P}election_ballot_counted", f"NOT = {{ has_country_flag = {P}election_ratified }}", "date > 1970.10.23"]
    elif key == "copper":
        c += ["has_completed_focus = COLDWAR_CHL_national_copper", f"NOT = {{ has_country_flag = {P}copper_choice_resolved }}"]
    elif key == "transport":
        c += [f"has_country_flag = {P}high_confrontation", "check_variable = { ruling_party = 18 }", f"NOT = {{ has_country_flag = {P}transport_choice_resolved }}"]
    elif key == "rupture":
        c += [f"{P}can_resolve_rupture = yes"]
    elif key == "junta":
        c += [f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"NOT = {{ has_country_flag = {P}junta_decided }}"]
        if oi == 1: c.append(f"has_country_flag = {P}pinochet_available")
    elif key == "repression":
        c += [f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"NOT = {{ has_country_flag = {P}repression_decided }}"]
    elif key == "adjustment":
        c += ["has_completed_focus = COLDWAR_CHL_pinochet_chicago", f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"NOT = {{ has_country_flag = {P}adjustment_choice_resolved }}"]
    elif key == "banking":
        c += [f"has_country_flag = {P}fragile_banks", f"NOT = {{ has_country_flag = {P}banking_crisis }}", f"NOT = {{ has_country_flag = {P}bank_prevention_receipt }}", f"NOT = {{ has_idea = COLDWAR_CHL_banking_stress_test }}"]
        if oi == 1: c.append("has_completed_focus = COLDWAR_CHL_prudential_banks")
    elif key == "early_exit":
        c += ["has_completed_focus = COLDWAR_CHL_military_ballot", f"has_country_flag = {P}constitutional_military_council", f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"NOT = {{ has_country_flag = {P}pinochet_presidency }}", f"NOT = {{ has_country_flag = {P}early_exit_resolved }}"]
    elif key == "plebiscite":
        c += ["has_completed_focus = COLDWAR_CHL_pinochet_plebiscite", f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"has_country_flag = {P}plebiscite_vote_counted", f"NOT = {{ has_country_flag = {P}plebiscite_decided }}"]
        c.append(f"has_country_flag = {P}plebiscite_no_won" if oi == 0 else f"has_country_flag = {P}plebiscite_yes_won")
    elif key == "handover":
        c += ["has_completed_focus = COLDWAR_CHL_pinochet_handover", f"has_country_flag = {P}plebiscite_no_won", f"has_country_flag = {P}military_government", "check_variable = { ruling_party = 22 }", f"has_country_flag = {P}civilian_1990_winner_confirmed", f"NOT = {{ has_country_flag = {P}civilian_handover }}"]
    elif key == "truth":
        c += ["has_completed_focus = COLDWAR_CHL_commission_truth", "has_idea = COLDWAR_CHL_repression", f"{P}civilian_government = yes", f"NOT = {{ has_country_flag = {P}truth_choice_resolved }}"]
    elif key == "andean":
        c += ["has_idea = COLDWAR_CHL_cartagena_member", f"NOT = {{ has_country_flag = {P}andean_reviewed }}"]
    else:
        c.append(f"NOT = {{ has_country_flag = {P}{key}_choice_resolved }}")
    repeatable = (key == "early_exit" and oi == 1) or (key == "congress" and oi == 1)
    if not repeatable:
        c.append(f"NOT = {{ has_country_flag = {P}{key}_choice_resolved }}")
    return " ".join(c)


def build():
    data = load_design(SOURCE)
    events = data["events"]
    effects = ["# IMPERIA COLD WAR — Chile 1970 political calendar, leader routing, and domestic effects."]
    # The shared core generator owns COLDWAR_CHL_civilian_government. Keep this
    # file limited to event conditions to avoid duplicate scripted triggers.
    triggers = ["# IMPERIA COLD WAR — Chile 1970 domestic event conditions."]
    decisions = ["# IMPERIA COLD WAR — Chile 1970 banking and judicial remedy decisions."]
    categories = ["# IMPERIA COLD WAR — Chile 1970 civic decisions.", f"{P}civic_remedies = {{ allowed = {{ tag = CHL {P}is_scenario = yes }} icon = generic_political_actions priority = 210 visible = {{ {P}is_scenario = yes }} }}"]
    event_text = ["# IMPERIA COLD WAR — Chile 1970 domestic events.", "add_namespace = COLDWAR_CHL"]
    ideas = ["# IMPERIA COLD WAR — Chile 1970 event choices and civic obligations.", "ideas = {", " country = {"]
    loc = ["l_english:", "# IMPERIA COLD WAR — Chile 1970 political events and civic remedies."]

    # A deliberate alternate-history route, independent of presidential ballots.
    # Preparation creates no coup rewards. The existing event retains the real
    # civilian/military choice and applies its one-time consequences on selection.
    triggers += [f"""{P}civilian_calendar_active = {{
{P}civilian_government = yes
NOT = {{ has_country_flag = {P}1970_calendar_superseded }}
}}""", f"""{P}intervention_context = {{
{P}is_scenario = yes
custom_trigger_tooltip = {{ tooltip = {P}civilian_tt {P}civilian_government = yes }}
is_subject = no
has_civil_war = no
has_capitulated = no
owns_state = 468
controls_state = 468
NOT = {{ has_country_flag = {P}rupture_resolved }}
}}""", f"""{P}can_prepare_intervention = {{
{P}intervention_context = yes
NOT = {{ has_country_flag = {P}intervention_in_progress }}
NOT = {{ has_country_flag = {P}intervention_prepared }}
NOT = {{ has_country_flag = {P}rupture_event_seen }}
}}""", f"""{P}can_resolve_rupture = {{
{P}intervention_context = yes
OR = {{
has_country_flag = {P}intervention_prepared
AND = {{
NOT = {{ has_country_flag = {P}intervention_in_progress }}
date > 1973.9.10 date < 1974.1.1
has_country_flag = {P}constitutional_crisis
has_country_flag = {P}high_confrontation
has_country_flag = {P}military_intervention_condition
check_variable = {{ ruling_party = 18 }}
}}
}}
}}"""]
    categories.append(f"{P}political_transition = {{ allowed = {{ tag = CHL {P}is_scenario = yes }} icon = generic_political_actions priority = 220 visible = {{ {P}is_scenario = yes }} }}")
    decisions.append(f"""{P}political_transition = {{
{P}prepare_military_intervention = {{
icon = generic_political_discourse
visible = {{ {P}is_scenario = yes NOT = {{ has_country_flag = {P}rupture_resolved }} NOT = {{ has_country_flag = {P}intervention_prepared }} }}
available = {{ {P}can_prepare_intervention = yes }}
cost = {INTERVENTION_PP}
days_remove = {INTERVENTION_DAYS}
days_re_enable = 1
complete_effect = {{ hidden_effect = {{ if = {{ limit = {{ {P}can_prepare_intervention = yes }} set_country_flag = {P}intervention_in_progress }} }} }}
cancel_trigger = {{ NOT = {{ {P}intervention_context = yes }} }}
cancel_effect = {{ hidden_effect = {{ clr_country_flag = {P}intervention_in_progress }} }}
remove_effect = {{
effect_tooltip = {{ country_event = {{ id = COLDWAR_CHL.5 }} }}
hidden_effect = {{
if = {{ limit = {{ {P}intervention_context = yes has_country_flag = {P}intervention_in_progress NOT = {{ has_country_flag = {P}rupture_event_seen }} }}
set_country_flag = {P}intervention_prepared
{P}trigger_event_rupture = yes
}}
clr_country_flag = {P}intervention_in_progress
}}
}}
ai_will_do = {{ base = 0 }}
}}
}}""")
    loc += [f' {P}political_transition:0 "Chile: Political Transition"',
            f' {P}political_transition_desc:0 "The armed forces remain divided over intervention in politics. A civilian government can seek an agreement with the officer corps or prepare a break with constitutional rule."',
            f' {P}prepare_military_intervention:0 "Secure the Officer Corps"',
            f' {P}prepare_military_intervention_desc:0 "Build officer backing over {INTERVENTION_DAYS} days at a cost of {INTERVENTION_PP} political power. The service chiefs will then demand a settlement: retain civilian government through constitutional guarantees, or allow a military takeover. Once in government, the junta can retain collective authority or place Augusto Pinochet at its head. Preparations can proceed under any civilian administration. They end if civilian authority falls, Chile becomes a subject, capitulates or enters civil war, or Santiago is lost; political power is not recovered."',
            f' {P}event_political_context_changed:0 "Acknowledge the changed political situation"']

    effects.append(f"""{P}clear_coalition_parameters = {{
clear_variable = col_one
clear_variable = col_two
clear_variable = col_three
clear_variable = col_four
clear_variable = col_five
}}""")
    effects.append(f"""{P}apply_government_change = {{
set_country_flag = no_leader_change
change_ruling_party_effect = yes
clr_country_flag = no_leader_change
}}""")
    effects.append(f"""COLDWAR_CHL_sync_native_outlook = {{
set_country_flag = no_leader_change
update_set_politics = yes
clr_country_flag = no_leader_change
}}""")
    effects.append(f"""{P}record_1970_presidential_term = {{
set_country_flag = no_leader_change
set_politics = {{ ruling_party = ROOT elections_allowed = yes last_election = \"1970.9.4\" election_frequency = 72 }}
clr_country_flag = no_leader_change
}}""")
    effects.append(f"""{P}record_1990_presidential_term = {{
set_country_flag = no_leader_change
set_politics = {{ ruling_party = ROOT elections_allowed = yes last_election = \"1989.12.14\" election_frequency = 48 }}
clr_country_flag = no_leader_change
}}""")

    # 1970's real vote is counted from the three registered presidential tickets,
    # adding each coalition partner once and normalizing the resulting shares.
    effects.append(f"""{P}election_count = {{
if = {{ limit = {{ {P}civilian_calendar_active = yes NOT = {{ has_country_flag = {P}election_ballot_counted }} }}
hold_elections = yes
set_temp_variable = {{ {P}ticket_1 = party_pop_array^1 }}
add_to_temp_variable = {{ {P}ticket_1 = party_pop_array^20 }}
set_temp_variable = {{ {P}ticket_2 = party_pop_array^2 }}
add_to_temp_variable = {{ {P}ticket_2 = party_pop_array^14 }}
set_temp_variable = {{ {P}ticket_18 = party_pop_array^18 }}
add_to_temp_variable = {{ {P}ticket_18 = party_pop_array^4 }}
add_to_temp_variable = {{ {P}ticket_18 = party_pop_array^3 }}
add_to_temp_variable = {{ {P}ticket_18 = party_pop_array^19 }}
set_temp_variable = {{ {P}ticket_total = {P}ticket_1 }}
add_to_temp_variable = {{ {P}ticket_total = {P}ticket_2 }}
add_to_temp_variable = {{ {P}ticket_total = {P}ticket_18 }}
if = {{ limit = {{ check_variable = {{ {P}ticket_total > 0 }} }}
divide_temp_variable = {{ {P}ticket_1 = {P}ticket_total }}
divide_temp_variable = {{ {P}ticket_2 = {P}ticket_total }}
divide_temp_variable = {{ {P}ticket_18 = {P}ticket_total }}
set_variable = {{ {P}election_winner_slot = 1 }}
set_variable = {{ {P}election_runner_up_slot = 2 }}
set_variable = {{ {P}election_winner_share = {P}ticket_1 }}
set_variable = {{ {P}election_runner_up_share = {P}ticket_2 }}
if = {{ limit = {{ check_variable = {{ {P}ticket_2 > {P}ticket_1 }} }} set_variable = {{ {P}election_winner_slot = 2 }} set_variable = {{ {P}election_runner_up_slot = 1 }} set_variable = {{ {P}election_winner_share = {P}ticket_2 }} set_variable = {{ {P}election_runner_up_share = {P}ticket_1 }} }}
if = {{ limit = {{ check_variable = {{ {P}ticket_18 > {P}election_winner_share }} }}
set_variable = {{ {P}election_runner_up_slot = {P}election_winner_slot }} set_variable = {{ {P}election_runner_up_share = {P}election_winner_share }} set_variable = {{ {P}election_winner_slot = 18 }} set_variable = {{ {P}election_winner_share = {P}ticket_18 }}
}} else_if = {{ limit = {{ check_variable = {{ {P}ticket_18 > {P}election_runner_up_share }} }} set_variable = {{ {P}election_runner_up_slot = 18 }} set_variable = {{ {P}election_runner_up_share = {P}ticket_18 }} }}
set_variable = {{ {P}election_confirmed_slot = -1 }}
if = {{ limit = {{ check_variable = {{ {P}election_winner_share > 0.5 }} }} set_variable = {{ {P}election_confirmed_slot = {P}election_winner_slot }} set_country_flag = {P}election_ratified }}
set_country_flag = {P}election_ballot_counted
}}
}}
}}""")

    effects.append(f"""{P}update_congress_support = {{
update_majority_threshold = yes
set_variable = {{ {P}congress_runner_up_in_coalition = 0 }}
set_variable = {{ {P}congress_coalition_support = party_pop_elect_array^ruling_party }}
if = {{ limit = {{ check_variable = {{ ruling_party = {P}election_runner_up_slot }} }} set_variable = {{ {P}congress_runner_up_in_coalition = 1 }} }}
for_each_loop = {{
array = gov_coalition_array
value = {P}coalition_member
if = {{ limit = {{ check_variable = {{ {P}coalition_member = {P}election_runner_up_slot }} }} set_variable = {{ {P}congress_runner_up_in_coalition = 1 }} }}
if = {{ limit = {{ NOT = {{ check_variable = {{ {P}coalition_member = ruling_party }} }} }} add_to_variable = {{ {P}congress_coalition_support = party_pop_elect_array^{P}coalition_member }} }}
}}
}}""")
    triggers.append(f"{P}congress_alternative_majority = {{ has_country_flag = {P}election_ballot_counted NOT = {{ has_country_flag = {P}election_ratified }} check_variable = {{ {P}congress_runner_up_in_coalition = 1 }} check_variable = {{ {P}congress_coalition_support > majority_threshold }} }}")

    candidate_slots_1990 = [0, 1, 2, 3, 4, 5, 14, 18, 19, 20]
    count_1990 = [f"{P}count_1990_election = {{", "hold_elections = yes", f"set_temp_variable = {{ {P}1990_winner_slot_temp = -1 }}", f"set_temp_variable = {{ {P}1990_winner_share_temp = -1 }}", f"set_temp_variable = {{ {P}1990_runner_up_share_temp = -1 }}"]
    for slot in candidate_slots_1990:
        count_1990.append(f"if = {{ limit = {{ check_variable = {{ party_pop_elect_array^{slot} > {P}1990_winner_share_temp }} }} set_temp_variable = {{ {P}1990_runner_up_share_temp = {P}1990_winner_share_temp }} set_temp_variable = {{ {P}1990_winner_share_temp = party_pop_elect_array^{slot} }} set_temp_variable = {{ {P}1990_winner_slot_temp = {slot} }} }}")
        count_1990.append(f"else_if = {{ limit = {{ check_variable = {{ party_pop_elect_array^{slot} > {P}1990_runner_up_share_temp }} }} set_temp_variable = {{ {P}1990_runner_up_share_temp = party_pop_elect_array^{slot} }} }}")
    count_1990 += [f"if = {{ limit = {{ check_variable = {{ {P}1990_winner_share_temp > {P}1990_runner_up_share_temp }} check_variable = {{ {P}1990_winner_share_temp > 0 }} }} set_variable = {{ {P}1990_election_confirmed_slot = {P}1990_winner_slot_temp }} set_country_flag = {P}civilian_1990_winner_confirmed set_country_flag = {P}1990_election_counted }}", "}"]
    effects.append("\n".join(count_1990))

    install_1990 = [f"{P}install_1990_candidate = {{"]
    for i, slot in enumerate(candidate_slots_1990):
        branch = "if" if i == 0 else "else_if"
        coalition = " set_variable = { col_one = 3 } set_variable = { col_two = 18 }" if slot == 1 else " set_variable = { col_one = 14 } set_variable = { col_two = 0 }" if slot == 2 else ""
        install_1990.append(f"{branch} = {{ limit = {{ check_variable = {{ {P}1990_election_confirmed_slot = {slot} }} }} {P}clear_coalition_parameters = yes set_variable = {{ rul_party_temp = {slot} }}{coalition} set_variable = {{ {P}leader_slot = {slot} }} set_variable = {{ disable_elections = 0 }} set_variable = {{ change_leader_temp = 0 }} {P}apply_government_change = yes }}")
    install_1990 += [f"set_country_flag = {P}election_installed", "}"]
    effects.append("\n".join(install_1990))

    # Use native subparty setter only when an actual transfer is confirmed. The
    # daily route never kills and recreates an unchanged incumbent.
    effects.append(f"""{P}install_confirmed_candidate = {{
if = {{ limit = {{ {P}civilian_calendar_active = yes has_country_flag = {P}election_ratified NOT = {{ has_country_flag = {P}election_installed }} }}
set_country_flag = {P}election_installed
if = {{ limit = {{ check_variable = {{ {P}election_confirmed_slot = 1 }} }} {P}clear_coalition_parameters = yes set_variable = {{ rul_party_temp = 1 }} set_variable = {{ col_one = 20 }} set_variable = {{ change_leader_temp = 0 }} set_variable = {{ disable_elections = 0 }} COLDWAR_CHL_apply_government_change = yes set_variable = {{ COLDWAR_CHL_leader_slot = 1 }} }}
else_if = {{ limit = {{ check_variable = {{ {P}election_confirmed_slot = 2 }} }} {P}clear_coalition_parameters = yes set_variable = {{ rul_party_temp = 2 }} set_variable = {{ col_one = 14 }} set_variable = {{ change_leader_temp = 0 }} set_variable = {{ disable_elections = 0 }} COLDWAR_CHL_apply_government_change = yes set_variable = {{ COLDWAR_CHL_leader_slot = 2 }} }}
else_if = {{ limit = {{ check_variable = {{ {P}election_confirmed_slot = 18 }} }} {P}clear_coalition_parameters = yes set_variable = {{ rul_party_temp = 18 }} set_variable = {{ col_one = 4 }} set_variable = {{ col_two = 3 }} set_variable = {{ col_three = 19 }} set_variable = {{ change_leader_temp = 0 }} set_variable = {{ disable_elections = 0 }} COLDWAR_CHL_apply_government_change = yes set_variable = {{ COLDWAR_CHL_leader_slot = 18 }} }}
COLDWAR_CHL_sync_native_outlook = yes
COLDWAR_CHL_route_leader = yes
COLDWAR_CHL_record_1970_presidential_term = yes
COLDWAR_CHL_refresh_programmes = yes
}}
}}""")

    route = ["COLDWAR_CHL_route_leader = {", f"if = {{ limit = {{ {P}is_scenario = yes }}"]
    candidates = [
        ("pinochet", "Augusto Pinochet", 22, "Nat_Autocracy", "gfx/leaders/mdcw_historical_pool/CHL_augusto_pinochet.dds", f"has_country_flag = {P}pinochet_presidency check_variable = {{ ruling_party = 22 }}"),
        ("military_council", "Chilean Military Council", 221, "Nat_Autocracy", "", f"has_country_flag = {P}military_government check_variable = {{ ruling_party = 22 }} NOT = {{ has_country_flag = {P}pinochet_presidency }}"),
        ("aylwin", "Patricio Aylwin", 101, "conservatism", "gfx/leaders/mdcw_historical_pool/CHL_patricio_aylwin.dds", f"has_country_flag = {P}civilian_1990_winner_confirmed has_country_flag = {P}civilian_handover check_variable = {{ ruling_party = 1 }}"),
        ("frei", "Eduardo Frei Montalva", 100, "conservatism", "gfx/leaders/CHL/CHL_Coldwar_Eduardo_Frei_Montalva.dds", f"check_variable = {{ ruling_party = 1 }} NOT = {{ has_country_flag = {P}election_installed }}"),
        ("tomic", "Radomiro Tomic", 1, "conservatism", "", f"has_country_flag = {P}election_installed check_variable = {{ ruling_party = 1 }} NOT = {{ has_country_flag = {P}civilian_handover }}"),
        ("buchi", "Hernán Büchi", 201, "liberalism", "", f"has_country_flag = {P}civilian_1990_winner_confirmed has_country_flag = {P}civilian_handover check_variable = {{ ruling_party = 2 }}"),
        ("alessandri", "Jorge Alessandri", 2, "liberalism", "", f"check_variable = {{ ruling_party = 2 }} NOT = {{ has_country_flag = {P}civilian_handover }}"),
        ("allende", "Salvador Allende", 18, "neutral_Social", "gfx/leaders/mdcw_historical_pool/CHL_salvador_allende.dds", "check_variable = { ruling_party = 18 }"),
        ("baltra", "Alberto Baltra", 3, "socialism", "", "check_variable = { ruling_party = 3 }"),
        ("corvalan", "Luis Corvalán", 4, "communist_state", "", "check_variable = { ruling_party = 4 }"),
        ("enriquez", "Miguel Enríquez", 5, "anarchist_communism", "", "check_variable = { ruling_party = 5 }"),
        ("duran", "Julio Durán", 14, "Neutral_conservatism", "", "check_variable = { ruling_party = 14 }"),
        ("chonchol", "Jacques Chonchol", 19, "Neutral_Communism", "", "check_variable = { ruling_party = 19 }"),
        ("correa", "Raúl Correa Labra", 20, "Nat_Populism", "", "check_variable = { ruling_party = 20 }"),
        ("guzman", "Jaime Guzmán", 0, "Western_Autocracy", "", "check_variable = { ruling_party = 0 }"),
    ]
    for i, (key, name, leader_id, ideology, picture, condition) in enumerate(candidates):
        pic = f' picture = "{picture}"' if picture else ""
        current = f'has_country_leader = {{ name = "{name}" ruling_only = yes }}'
        branch = "if" if i == 0 else "else_if"
        route.append(f'{branch} = {{ limit = {{ {condition} }} if = {{ limit = {{ NOT = {{ {current} }} }} hidden_effect = {{ kill_country_leader = yes }} create_country_leader = {{ name = "{name}"{pic} ideology = {ideology} }} }} }}')
    route += ["}", "}"]
    effects.append("\n".join(route))

    effects.append(f"""{P}politics_initialize = {{
if = {{ limit = {{ {P}is_scenario = yes NOT = {{ has_country_flag = {P}politics_initialized }} }}
set_country_flag = {P}politics_initialized
set_variable = {{ {P}leader_slot = 1 }}
}}
}}""")

    for i, e in enumerate(events, 1):
        eid = f"COLDWAR_CHL.{i}"
        triggers.append(f"{P}can_event_{e['key']} = {{ {_event_trigger(e)} }}")
        opts = []
        for oi, opt in enumerate(e["options"]):
            key = f"{e['key']}_{oi+1}"
            avail = ""
            if e["key"] == "congress":
                avail = f"trigger = {{ has_country_flag = {P}election_ballot_counted NOT = {{ has_country_flag = {P}election_ratified }} }} "
            if e["key"] == "banking" and oi == 1:
                avail = f"trigger = {{ has_completed_focus = COLDWAR_CHL_prudential_banks NOT = {{ has_country_flag = {P}banking_crisis }} }} "
            if e["key"] == "plebiscite":
                avail = f"trigger = {{ has_country_flag = {P}plebiscite_no_won }} " if oi == 0 else f"trigger = {{ has_country_flag = {P}plebiscite_yes_won }} "
            if e["key"] == "junta" and oi == 1:
                avail = f"trigger = {{ has_country_flag = {P}pinochet_available }} "
            if e["key"] == "handover":
                avail = f"trigger = {{ has_country_flag = {P}civilian_1990_winner_confirmed }} "
            effect = _event_option_effect(e, oi, opt)
            option_preview = f"effect_tooltip = {{ custom_effect_tooltip = {P}congress_alternative_requirement_tt }} " if e["key"] == "congress" and oi == 1 else ""
            guard = _event_execution_guard(e, oi)
            if e['key'] in ('election', 'congress', 'rupture', 'junta'):
                avail = f"trigger = {{ {guard} }} "
            opts.append(f"option = {{ name = {P}event_{e['key']}_option_{oi+1} {avail}{option_preview}effect_tooltip = {{ {effect} }} hidden_effect = {{ if = {{ limit = {{ {guard} }} {effect} }} }} }}")
        if e['key'] in ('election', 'congress', 'rupture', 'junta'):
            live_options = ' '.join(f"AND = {{ {_event_execution_guard(e, oi)} }}" for oi in range(len(e['options'])))
            cleanup = ''
            if e['key'] == 'rupture':
                # A dismissed stale crisis must not permanently strand a save
                # after temporary loss of Santiago or a change in government.
                cleanup = f"hidden_effect = {{ if = {{ limit = {{ NOT = {{ has_country_flag = {P}rupture_resolved }} }} clr_country_flag = {P}intervention_prepared clr_country_flag = {P}rupture_event_seen }} }}"
            elif e['key'] == 'junta':
                cleanup = f"hidden_effect = {{ if = {{ limit = {{ NOT = {{ has_country_flag = {P}junta_decided }} }} clr_country_flag = {P}junta_event_seen }} }}"
            opts.append(f"option = {{ name = {P}event_political_context_changed trigger = {{ NOT = {{ OR = {{ {live_options} }} }} }} {cleanup} }}")
        immediate_effect = f"set_country_flag = {P}{e['key']}_event_seen"
        if e["key"] == "election": immediate_effect += f" set_country_flag = {P}campaign_opened"
        event_text.append(f"""country_event = {{
id = {eid}
title = {P}event_{e['key']}_title
desc = {P}event_{e['key']}_desc
is_triggered_only = yes
trigger = {{ {P}is_scenario = yes }}
immediate = {{ {immediate_effect} }}
{chr(10).join(opts)}
}}""")
        description = e["description"]
        if e["key"] == "congress":
            description += " If no alternative coalition majority exists, no president is confirmed and Congress reconvenes after seven days."
        loc += [f" {P}event_{e['key']}_title:0 \"{e['title']}\"", f" {P}event_{e['key']}_desc:0 \"{description}\""]
        for oi, opt in enumerate(e["options"], 1):
            loc.append(f" {P}event_{e['key']}_option_{oi}:0 \"{opt['name']}\"")
            if e["key"] == "congress" and oi == 2:
                loc.append(f" {P}congress_alternative_requirement_tt:0 \"The stored runner-up must be in the government coalition, and its electoral coalition must exceed the majority threshold. Current support: [?{P}congress_coalition_support|%1]. Required: more than [?majority_threshold|%1].\"")
            k = f"{e['key']}_{oi}"
            if opt.get("weekly", 0):
                loc.append(f" {P}weekly_cost_{k}:0 \"Weekly budget: -${n(round(opt['weekly']*1000,5))} million per week\"")
            mods = opt.get("modifiers", {})
            if mods:
                idea_mod = " ".join(f"{m} = {n(v)}" for m,v in mods.items())
                ideas.append(f"  {idea(k)} = {{ picture = generic_political_reform allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {idea_mod} }} }}")
                loc += [f" {idea(k)}:0 \"{e['title']}: {opt['name']}\"", f" {idea(k)}_desc:0 \"{e['description']}\""]

    # Firing sequence: campaign, ballot, conditional congressional count,
    # inauguration, then only crises gated by actual player/state conditions.
    daily = [f"{P}politics_daily = {{", f"set_variable = {{ {P}politics_weekly = 0 }}", f"if = {{ limit = {{ {P}is_scenario = yes }}", f"{P}politics_initialize = yes"]
    # Keep the civic/military state synchronized to the actual ruling subparty.
    # Party-bound modifiers are refreshed on both transitions; durable earned
    # programme variables remain owned by the core refresh effect.
    daily.append(f"if = {{ limit = {{ check_variable = {{ ruling_party = 22 }} }} set_country_flag = {P}1970_calendar_superseded if = {{ limit = {{ NOT = {{ has_country_flag = {P}military_government }} }} set_country_flag = {P}military_government {P}route_leader = yes {P}refresh_programmes = yes }} }}")
    daily.append(f"if = {{ limit = {{ NOT = {{ check_variable = {{ ruling_party = 22 }} }} has_country_flag = {P}military_government }} clr_country_flag = {P}military_government clr_country_flag = {P}pinochet_presidency {P}route_leader = yes {P}refresh_programmes = yes }}")
    # The twelve-month schedule arranges the exceptional civilian ballot.
    # After that transfer, ordinary presidential terms return to six years.
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}early_exit_election NOT = {{ check_variable = {{ ruling_party = 22 }} }} NOT = {{ has_country_flag = {P}early_exit_term_recorded }} }} set_country_flag = {P}early_exit_term_recorded set_country_flag = no_leader_change set_politics = {{ ruling_party = ROOT election_frequency = 72 elections_allowed = yes }} clr_country_flag = no_leader_change }}")
    daily += [f"if = {{ limit = {{ date > 1970.11.2 has_stability < 0.4 }}", f"set_temp_variable = {{ {P}left_bloc = party_pop_array^18 }}", f"add_to_temp_variable = {{ {P}left_bloc = party_pop_array^4 }}", f"add_to_temp_variable = {{ {P}left_bloc = party_pop_array^3 }}", f"add_to_temp_variable = {{ {P}left_bloc = party_pop_array^19 }}", f"set_temp_variable = {{ {P}right_bloc = party_pop_array^2 }}", f"add_to_temp_variable = {{ {P}right_bloc = party_pop_array^14 }}", f"if = {{ limit = {{ check_variable = {{ {P}left_bloc > 0.25 }} check_variable = {{ {P}right_bloc > 0.25 }} }} add_to_variable = {{ {P}confrontation_days = 1 }} }}", f"else = {{ set_variable = {{ {P}confrontation_days = 0 }} clr_country_flag = {P}high_confrontation }}", f"}} else = {{ set_variable = {{ {P}confrontation_days = 0 }} clr_country_flag = {P}high_confrontation }}", f"if = {{ limit = {{ check_variable = {{ {P}confrontation_days > 30 }} }} set_country_flag = {P}high_confrontation }}"]
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}stress_test_active NOT = {{ has_idea = COLDWAR_CHL_banking_stress_test }} }} clr_country_flag = {P}stress_test_active }}")
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}pinochet_chicago_applied date > 1981.12.31 }} set_country_flag = {P}fragile_banks }}")
    daily.append(f"if = {{ limit = {{ has_completed_focus = COLDWAR_CHL_pinochet_handover has_country_flag = {P}plebiscite_no_won date > 1989.12.13 NOT = {{ has_country_flag = {P}civilian_1990_winner_confirmed }} }} {P}count_1990_election = yes }}")
    daily += [f"if = {{ limit = {{ {P}can_event_election = yes }} {P}trigger_event_election = yes }}"]
    daily += [f"if = {{ limit = {{ {P}civilian_calendar_active = yes }}"]
    daily += [f"if = {{ limit = {{ has_country_flag = {P}campaign_opened date > 1970.9.3 NOT = {{ has_country_flag = {P}election_ballot_counted }} }} {P}election_count = yes }}"]
    daily += [f"if = {{ limit = {{ has_country_flag = {P}election_ballot_counted NOT = {{ has_country_flag = {P}election_ratified }} }} {P}update_congress_support = yes }}"]
    daily += [f"if = {{ limit = {{ {P}can_event_congress = yes NOT = {{ has_country_flag = {P}congress_event_seen }} }} {P}trigger_event_congress = yes }}"]
    daily += [f"if = {{ limit = {{ has_country_flag = {P}election_ratified date > 1970.11.2 NOT = {{ has_country_flag = {P}election_installed }} }} {P}install_confirmed_candidate = yes }}"]
    daily.append('}')
    for idx, key in [(4,"transport"),(5,"rupture"),(6,"junta"),(9,"banking"),(14,"andean")]:
        daily.append(f"if = {{ limit = {{ {P}can_event_{key} = yes }} {P}trigger_event_{key} = yes }}")
    daily += [f"if = {{ limit = {{ has_country_flag = {P}military_government NOT = {{ has_country_flag = {P}repression_event_seen }} }} {P}trigger_event_repression = yes }}"]
    # Event hooks driven by completed native policy focuses; each is one-shot and
    # parent focus effects can also call the exported event IDs directly.
    for focus,key,i in [("COLDWAR_CHL_national_copper","copper",3),("COLDWAR_CHL_pinochet_chicago","adjustment",8),("COLDWAR_CHL_commission_truth","truth",13),("COLDWAR_CHL_military_ballot","early_exit",10),("COLDWAR_CHL_pinochet_plebiscite","plebiscite",11),("COLDWAR_CHL_pinochet_handover","handover",12)]:
        flag = f"{P}{key}_event_seen"
        retry_guard = f" NOT = {{ has_country_flag = {P}early_exit_cooldown }}" if key == "early_exit" else ""
        daily.append(f"if = {{ limit = {{ has_completed_focus = {focus} NOT = {{ has_country_flag = {flag} }}{retry_guard} }} {P}trigger_event_{key} = yes }}")
    truth=next(e for e in events if e['key']=='truth')
    bank=next(c for c in data['decision_contracts'] if c['id']==P+'civilian_bank_restructuring')
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}truth_full }} add_to_variable = {{ {P}politics_weekly = {n(truth['options'][0]['weekly'])} }} }}")
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}truth_limited }} add_to_variable = {{ {P}politics_weekly = {n(truth['options'][1]['weekly'])} }} }}")
    daily.append(f"if = {{ limit = {{ has_country_flag = {P}financial_resolution_funded has_idea = COLDWAR_CHL_restructuring }} add_to_variable = {{ {P}politics_weekly = {n(bank['weekly'])} }} }}")
    weekly_by_key = {e["key"]: opt.get("weekly", 0) for e in events for opt in e["options"] if opt.get("weekly", 0) and opt.get("duration")}
    for key, amount in weekly_by_key.items():
        for oi, opt in enumerate(next(e for e in events if e["key"] == key)["options"], 1):
            if opt.get("weekly", 0):
                daily.append(f"if = {{ limit = {{ has_idea = {idea(key+'_'+str(oi))} }} add_to_variable = {{ {P}politics_weekly = {n(amount)} }} }}")
    daily += ["}", "}"]
    effects.append("\n".join(daily))

    # Decision-contract-driven remedies; requirements and funded alternatives
    # remain reachable after party changes, while preventing duplicate payment.
    decisions.append(f"{P}civic_remedies = {{")
    decision_specs = [
        ("banking_stress_test", f"OR = {{ has_country_flag = {P}pinochet_crisis_applied has_country_flag = {P}prudential_banks_applied }} NOT = {{ has_idea = COLDWAR_CHL_bank_crisis }} NOT = {{ has_idea = COLDWAR_CHL_banking_stress_test }} NOT = {{ has_country_flag = {P}stress_test_active }}", 1, 365, {"bureaucracy_cost_multiplier_modifier":.02,"interest_rate_multiplier_modifier":-.25}, "stress_test_active"),
        ("civilian_bank_restructuring", f"has_idea = COLDWAR_CHL_bank_crisis {P}civilian_government = yes NOT = {{ has_country_flag = {P}financial_resolution_receipt }} NOT = {{ has_country_flag = {P}bank_remedy_used }}", 6, None, {"production_speed_buildings_factor":.08,"interest_rate_multiplier_modifier":.5,"tax_gain_multiplier_modifier":-.03}, "bank_remedy_used"),
        ("civilian_creditor_losses", f"has_idea = COLDWAR_CHL_bank_crisis {P}civilian_government = yes NOT = {{ has_country_flag = {P}financial_resolution_receipt }} NOT = {{ has_country_flag = {P}bank_remedy_used }}", 2, None, {"interest_rate_multiplier_modifier":-.5,"production_speed_buildings_factor":-.06,"stability_factor":-.05}, "bank_remedy_used"),
        ("full_judicial_settlement", f"has_idea = COLDWAR_CHL_limited_accountability {P}civilian_government = yes NOT = {{ has_country_flag = {P}judicial_settlement_used }}", 2, None, {}, "judicial_settlement_used")]
    specs = {x[0]:x for x in decision_specs}
    for contract in data["decision_contracts"]:
        key = contract["id"].removeprefix(P)
        _, requirement, _original_price, duration, mods, receipt = specs[key]
        money=contract['money']
        modtext = " ".join(f"{a} = {n(b)}" for a,b in mods.items())
        apply = [_effect_cost(money)]
        if key != "banking_stress_test":
            apply.append(f"set_country_flag = {P}{receipt}")
        if key == "banking_stress_test":
            apply += [f"add_timed_idea = {{ idea = COLDWAR_CHL_banking_stress_test days = {duration} }}", f"set_country_flag = {{ flag = {P}stress_test_active value = 1 days = {duration} }}"]
        elif key in ("civilian_bank_restructuring","civilian_creditor_losses"):
            package_idea = f"{P}financial_restructuring_funded" if key == "civilian_bank_restructuring" else f"{P}financial_restructuring_losses"
            apply += ["remove_ideas = COLDWAR_CHL_bank_crisis", f"add_timed_idea = {{ idea = COLDWAR_CHL_restructuring days = 365 }}", f"add_timed_idea = {{ idea = {package_idea} days = 365 }}", f"set_country_flag = {P}financial_resolution_receipt"]
            if key == "civilian_bank_restructuring":
                apply.append(f"set_country_flag = {P}financial_resolution_funded")
        elif key == "full_judicial_settlement": apply.append("remove_ideas = COLDWAR_CHL_limited_accountability")
        preview = [_effect_cost(money)]
        if key == "banking_stress_test":
            preview.append(f"add_timed_idea = {{ idea = COLDWAR_CHL_banking_stress_test days = {duration} }}")
        elif key in ("civilian_bank_restructuring", "civilian_creditor_losses"):
            package_idea = f"{P}financial_restructuring_funded" if key == "civilian_bank_restructuring" else f"{P}financial_restructuring_losses"
            preview += ["remove_ideas = COLDWAR_CHL_bank_crisis", f"add_timed_idea = {{ idea = COLDWAR_CHL_restructuring days = 365 }}", f"add_timed_idea = {{ idea = {package_idea} days = 365 }}"]
        elif key == "full_judicial_settlement":
            preview.append("remove_ideas = COLDWAR_CHL_limited_accountability")
        if key == "civilian_bank_restructuring" and contract.get("weekly", 0):
            preview.append(f"custom_effect_tooltip = {P}weekly_cost_civilian_bank_restructuring")
        guard = f"{P}is_scenario = yes {requirement}"
        decisions.append(f"{contract['id']} = {{ icon = generic_political_discourse visible = {{ {P}is_scenario = yes }} available = {{ {guard} }} cost = 0 days_re_enable = 1 complete_effect = {{ effect_tooltip = {{ {' '.join(preview)} }} hidden_effect = {{ if = {{ limit = {{ {guard} }} {' '.join(apply)} }} }} }} ai_will_do = {{ base = 0 }} }}")
        loc.append(f" {contract['id']}:0 \"{contract['title']}\"")
        if key == "banking_stress_test":
            loc.append(f" {contract['id']}_desc:0 \"Funded bank reviews remain active for 365 days and deter only the first fragile-bank event.\"")
        if key == "civilian_bank_restructuring":
            ideas.append(f"  {P}financial_restructuring_funded = {{ picture = generic_political_reform allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {modtext} }} }}")
            loc.append(f" {P}financial_restructuring_funded:0 \"Financial Restructuring: Public Intervention\"")
            loc.append(f" {P}financial_restructuring_funded_desc:0 \"Public funds stabilize credit while public revenue remains constrained and the 365-day restructuring burden continues.\"")
            loc.append(f" {P}weekly_cost_civilian_bank_restructuring:0 \"Weekly budget: -${n(round(contract['weekly']*1000,5))} million per week for 365 days\"")
        elif key == "civilian_creditor_losses":
            ideas.append(f"  {P}financial_restructuring_losses = {{ picture = generic_political_reform allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {modtext} }} }}")
        elif modtext and key not in ("banking_stress_test",):
            ideas.append(f"  {P}decision_{key} = {{ picture = generic_political_reform allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {modtext} }} }}")
    decisions.append("}")

    ideas.append(f"  COLDWAR_CHL_banking_stress_test = {{ picture = generic_political_reform allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ bureaucracy_cost_multiplier_modifier = 0.02 interest_rate_multiplier_modifier = -0.25 }} }}")
    loc += [f" {P}financial_restructuring_losses:0 \"Financial Restructuring through Creditor Losses\"", f" {P}financial_restructuring_losses_desc:0 \"Creditors bear part of the losses while industrial output and public confidence suffer.\""]
    ideas += [" }", "}"]
    loc += [f" {P}civic_remedies:0 \"Chile: Civic Remedies\""]

    effects.append(f"""{P}count_plebiscite_vote = {{
if = {{ limit = {{ NOT = {{ has_country_flag = {P}plebiscite_vote_counted }} }}
set_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^1 }}
add_to_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^3 }}
add_to_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^4 }}
add_to_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^18 }}
add_to_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^19 }}
add_to_temp_variable = {{ {P}plebiscite_no_total_temp = party_pop_array^20 }}
set_temp_variable = {{ {P}plebiscite_yes_total_temp = party_pop_array^0 }}
add_to_temp_variable = {{ {P}plebiscite_yes_total_temp = party_pop_array^2 }}
add_to_temp_variable = {{ {P}plebiscite_yes_total_temp = party_pop_array^14 }}
add_to_temp_variable = {{ {P}plebiscite_yes_total_temp = party_pop_array^22 }}
set_variable = {{ {P}plebiscite_no_total = {P}plebiscite_no_total_temp }}
set_variable = {{ {P}plebiscite_yes_total = {P}plebiscite_yes_total_temp }}
if = {{ limit = {{ check_variable = {{ {P}plebiscite_no_total > {P}plebiscite_yes_total }} }} set_country_flag = {P}plebiscite_no_won }}
else = {{ set_country_flag = {P}plebiscite_yes_won }}
set_country_flag = {P}plebiscite_vote_counted
}}
}}""")

    # Root-owned focus and event call sites use these guarded entry points. They
    # never replay a dated ballot or an already-consumed event receipt.
    for i, e in enumerate(events, 1):
        key = e["key"]
        seen = f"{P}{key}_event_seen"
        extra = []
        if key == "congress": extra += [f"{P}civilian_calendar_active = yes", f"has_country_flag = {P}election_ballot_counted", "date > 1970.10.23", f"NOT = {{ has_country_flag = {P}election_ratified }}", f"NOT = {{ has_country_flag = {P}congress_retry }}"]
        if key == "truth": extra += ["has_idea = COLDWAR_CHL_repression", "has_completed_focus = COLDWAR_CHL_commission_truth"]
        if key == "early_exit": extra += ["has_completed_focus = COLDWAR_CHL_military_ballot", f"has_country_flag = {P}constitutional_military_council"]
        if key == "plebiscite": extra += ["has_completed_focus = COLDWAR_CHL_pinochet_plebiscite", f"has_country_flag = {P}military_government"]
        if key == "handover": extra += ["has_completed_focus = COLDWAR_CHL_pinochet_handover", f"has_country_flag = {P}plebiscite_no_won", f"has_country_flag = {P}civilian_1990_winner_confirmed"]
        if key == "copper": extra.append("has_completed_focus = COLDWAR_CHL_national_copper")
        if key == "adjustment": extra.append("has_completed_focus = COLDWAR_CHL_pinochet_chicago")
        if key == "repression": extra.append(f"has_country_flag = {P}military_government")
        if key == "junta": extra.append(f"has_country_flag = {P}military_government")
        if key == "banking": extra.append(f"{P}can_event_banking = yes")
        if key == "andean": extra.append(f"{P}can_event_andean = yes")
        if key == "transport": extra.append(f"{P}can_event_transport = yes")
        if key == "rupture": extra.append(f"{P}can_event_rupture = yes")
        # _event_trigger already enforces the complete campaign window.
        if key == "election": extra += [f"NOT = {{ has_country_flag = {P}campaign_opened }}"]
        if key == "election": extra.append(f"{P}can_event_election = yes")
        if key == "early_exit": extra.append(f"NOT = {{ has_country_flag = {P}early_exit_cooldown }}")
        cond = " ".join([f"{P}is_scenario = yes", f"NOT = {{ has_country_flag = {seen} }}"] + extra)
        count_vote = f"{P}count_plebiscite_vote = yes " if key == "plebiscite" else ""
        effects.append(f"{P}trigger_event_{key} = {{ if = {{ limit = {{ {cond} }} {count_vote}country_event = {{ id = COLDWAR_CHL.{i} }} }} }}")

    return {
        "common/scripted_effects/COLDWAR_CHL_1970_politics.txt": "\n\n".join(effects)+"\n",
        "common/scripted_triggers/COLDWAR_CHL_1970_politics.txt": "\n\n".join(triggers)+"\n",
        "events/COLDWAR_CHL_1970_politics.txt": "\n\n".join(event_text)+"\n",
        "common/decisions/COLDWAR_CHL_1970_politics.txt": "\n\n".join(decisions)+"\n",
        "common/decisions/categories/COLDWAR_CHL_1970_politics.txt": "\n\n".join(categories)+"\n",
        "common/ideas/COLDWAR_CHL_1970_politics.txt": "\n".join(ideas)+"\n",
        "localisation/english/COLDWAR_CHL_1970_politics_l_english.yml": "\n".join(loc)+"\n",
    }


if __name__ == "__main__":
    for rel, text in build().items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8-sig" if rel.endswith(".yml") else "utf-8")
        print(rel)
