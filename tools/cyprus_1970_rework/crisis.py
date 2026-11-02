# IMPERIA COLD WAR — Cyprus 1970 crisis and guarantor runtime generator.
"""Emit the crisis, foreign-response, temporary NATO, and fiscal-stream script module."""

from __future__ import annotations

from copy import deepcopy
from textwrap import dedent, indent


PREFIX = "COLDWAR_CYP_R2_"
NS = "COLDWAR_CYP_R2_CRISIS"
ACTORS = {
    "gre_officers": "GRE", "gre_treaty": "GRE", "gre_network": "GRE",
    "gre_consult": "GRE", "gre_withdraw": "GRE", "gre_coup": "GRE",
    "tur_consult": "TUR", "tur_terms": "TUR", "tur_operation": "TUR",
    "eng_consult": "ENG", "eng_mediation": "ENG", "eng_restraint": "ENG",
    "tur_abstain": "TUR", "gre_response": "GRE", "gre_volunteers": "GRE",
    "gre_escalate": "GRE",
}

IDEAS = {
    "greek_officers": ("GRE", {"army_org_factor": .02, "training_time_factor": -.05}),
    "greek_treaty": ("GRE", {"foreign_influence_defense_modifier": .05, "stability_factor": .02}),
    "greek_network": ("CYP", {"stability_factor": -.02}),
    "greek_withdrawal": ("CYP", {"stability_factor": .03}),
    "turkish_terms": ("TUR", {"stability_factor": .03, "army_attack_factor": -.02}),
    "angry_general_staff": ("TUR", {"stability_factor": -.10, "army_org_factor": -.10, "political_power_factor": -.15}),
    "command_reorganization": ("TUR", {"army_org_factor": -.05, "political_power_factor": -.05}),
    "cyprus_intervention_forces": ("TUR", {"navy_org_factor": .15, "naval_invasion_prep_speed": .50,
        "amphibious_invasion": .15, "planning_speed": .30, "max_planning_factor": .20}),
    "cyprus_volunteer_mission": ("GRE", {"send_volunteer_size": 2, "send_volunteer_divisions_required": -1.0,
        "send_volunteers_tension": -1.0, "political_power_factor": -.05}),
    "english_mediation": ("CYP", {"bureaucracy_cost_multiplier_modifier": .01}),
    "english_restraint": ("ENG", {"bureaucracy_cost_multiplier_modifier": -.01,
        "foreign_influence_defense_modifier": -.03}),
}

def _script(name: str, body: str) -> str:
    body = dedent(body).strip("\n")
    return f"{name} = {{\n{indent(body, chr(9))}\n}}\n"


def _fenced(script: str) -> str:
    return "\n" + script.replace("\n", "\n")


def _modifier_block(values: dict[str, float | int]) -> str:
    return "\n".join(f"{key} = {value:g}" for key, value in values.items())


def _actor_preview_body(key: str) -> str:
    """Native non-executing tooltip effects. No availability tests or live transaction helpers."""
    bodies = {
        "gre_officers": """
            add_ideas = COLDWAR_CYP_R2_greek_officers
        """,
        "gre_treaty": """
            add_ideas = COLDWAR_CYP_R2_greek_treaty
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = -10 tooltip = COLDWAR_CYP_R2_penetration_tt }
            }
        """,
        "gre_network": """
            add_political_power = -50
            set_temp_variable = { treasury_change = CYP.gdp_total }
            multiply_temp_variable = { treasury_change = -0.0025 }
            modify_treasury_effect = yes
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = 20 tooltip = COLDWAR_CYP_R2_penetration_tt }
                add_ideas = COLDWAR_CYP_R2_greek_network
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
            }
        """,
        "gre_consult": """
            add_political_power = 50
            CYP = {
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
            }
        """,
        "gre_withdraw": """
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = -20 tooltip = COLDWAR_CYP_R2_penetration_tt }
                remove_ideas = COLDWAR_CYP_R2_greek_network
                add_ideas = COLDWAR_CYP_R2_greek_withdrawal
            }
        """,
        "gre_coup": """
            add_political_power = -100
            set_temp_variable = { treasury_change = CYP.gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            CYP = {
                country_event = { id = COLDWAR_CYP_R2_CRISIS.1 hours = 1 }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.2 days = 14 }
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
            }
        """,
        "tur_consult": """
            CYP = {
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
            }
        """,
        "tur_terms": """
            custom_effect_tooltip = COLDWAR_CYP_R2_offer_if_accepted_tt
            add_ideas = COLDWAR_CYP_R2_turkish_terms
            CYP = {
                country_event = { id = COLDWAR_CYP_R2_CRISIS.20 hours = 1 }
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.21 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.22 hours = 1 } }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.23 days = 14 }
            }
        """,
        "tur_operation": """
            add_political_power = -75
            set_temp_variable = { treasury_change = gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            add_timed_idea = { idea = COLDWAR_CYP_R2_cyprus_intervention_forces days = 180 }
            declare_war_on = { target = CYP type = annex_everything }
            custom_effect_tooltip = COLDWAR_CYP_R2_weekly_intervention_expense_tt
        """,
        "eng_consult": """
            add_political_power = 35
            CYP = {
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
            }
        """,
        "eng_mediation": """
            custom_effect_tooltip = COLDWAR_CYP_R2_offer_if_accepted_tt
            add_political_power = 50
            CYP = {
                add_ideas = COLDWAR_CYP_R2_english_mediation
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.30 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.31 hours = 1 } }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.32 hours = 1 }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.33 days = 14 }
            }
        """,
        "eng_restraint": """
            add_political_power = 50
            add_ideas = COLDWAR_CYP_R2_english_restraint
        """,
        "tur_abstain": """
            add_political_power = 75
            add_timed_idea = { idea = COLDWAR_CYP_R2_angry_general_staff days = 180 }
            set_variable = { COLDWAR_CYP_R2_military_pressure = 70 }
            custom_effect_tooltip = COLDWAR_CYP_R2_army_pressure_preview_tt
            country_event = { id = COLDWAR_CYP_R2_CRISIS.40 days = 30 }
            country_event = { id = COLDWAR_CYP_R2_CRISIS.41 days = 60 }
            country_event = { id = COLDWAR_CYP_R2_CRISIS.42 days = 180 }
        """,
        "gre_response": """
            add_political_power = 25
            CYP = { country_event = { id = COLDWAR_CYP_R2_CRISIS.3 hours = 1 } }
        """,
        "gre_volunteers": """
            add_political_power = -50
            add_ideas = COLDWAR_CYP_R2_cyprus_volunteer_mission
            custom_effect_tooltip = COLDWAR_CYP_R2_weekly_volunteer_expense_tt
        """,
        "gre_escalate": """
            add_political_power = -100
            set_temp_variable = { treasury_change = gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            if = { limit = { has_idea = NATO_member } NATO_leave = yes }
            TUR = { if = { limit = { has_idea = NATO_member } NATO_leave = yes } }
            add_to_war = {
                targeted_alliance = CYP
                enemy = TUR
                hostility_reason = asked_to_join
            }
        """,
    }
    try:
        return bodies[key]
    except KeyError as exc:
        raise ValueError(f"No native effect preview for actor focus {key}") from exc


def _effect_file() -> str:
    effects: list[str] = []
    effects.append(_script("COLDWAR_CYP_R2_crisis_close_army", """
        if = {
            limit = { has_country_flag = COLDWAR_CYP_R2_army_crisis_active }
            set_country_flag = COLDWAR_CYP_R2_army_crisis_closed
            clr_country_flag = COLDWAR_CYP_R2_army_crisis_active
        }
        if = {
            limit = { country_exists = TUR }
            TUR = {
                if = {
                    limit = { has_country_flag = COLDWAR_CYP_R2_army_crisis_active }
                    set_country_flag = COLDWAR_CYP_R2_army_crisis_closed
                    clr_country_flag = COLDWAR_CYP_R2_army_crisis_active
                    remove_ideas = COLDWAR_CYP_R2_angry_general_staff
                }
            }
        }
    """))
    effects.append(_script("COLDWAR_CYP_R2_resolve_cyprus_crisis", """
        COLDWAR_CYP_R2_crisis_close_army = yes
        clr_country_flag = COLDWAR_CYP_R2_crisis_active
        set_country_flag = COLDWAR_CYP_R2_crisis_resolved
    """))
    effects.append(_script("COLDWAR_CYP_R2_apply_army_pressure_delta", """
        if = {
            limit = {
                original_tag = TUR
                has_country_flag = COLDWAR_CYP_R2_army_crisis_active
                NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed }
            }
            add_to_variable = { COLDWAR_CYP_R2_military_pressure = COLDWAR_CYP_R2_military_pressure_delta }
            clamp_variable = { var = COLDWAR_CYP_R2_military_pressure min = 0 max = 100 }
            clear_variable = COLDWAR_CYP_R2_military_pressure_delta
        }
    """))
    effects.append(_script("COLDWAR_CYP_R2_start_army_crisis", """
        if = {
            limit = {
                original_tag = TUR
                IMP_is_1970_scenario = yes
                NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_started }
                NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed }
                country_exists = CYP
                CYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active }
            }
            set_country_flag = COLDWAR_CYP_R2_army_crisis_started
            set_country_flag = COLDWAR_CYP_R2_army_crisis_active
            set_variable = { COLDWAR_CYP_R2_military_pressure = 70 }
            add_timed_idea = { idea = COLDWAR_CYP_R2_angry_general_staff days = 180 }
            CYP = { set_country_flag = COLDWAR_CYP_R2_army_crisis_active }
            country_event = { id = COLDWAR_CYP_R2_CRISIS.40 days = 30 }
            country_event = { id = COLDWAR_CYP_R2_CRISIS.41 days = 60 }
            country_event = { id = COLDWAR_CYP_R2_CRISIS.42 days = 180 }
        }
    """))

    actor_bodies = {
        "gre_officers": """
            add_ideas = COLDWAR_CYP_R2_greek_officers
            set_country_flag = COLDWAR_CYP_R2_greek_officer_focus_completed
            CYP = { set_country_flag = COLDWAR_CYP_R2_greek_officer_footprint }
        """,
        "gre_treaty": """
            add_ideas = COLDWAR_CYP_R2_greek_treaty
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = -10 }
                clamp_variable = { var = COLDWAR_CYP_R2_officer_penetration min = 0 max = 100 }
                set_country_flag = COLDWAR_CYP_R2_greek_treaty_observed
            }
        """,
        "gre_network": """
            add_political_power = -50
            set_temp_variable = { treasury_change = CYP.gdp_total }
            multiply_temp_variable = { treasury_change = -0.0025 }
            modify_treasury_effect = yes
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = 20 }
                clamp_variable = { var = COLDWAR_CYP_R2_officer_penetration min = 0 max = 100 }
                add_ideas = COLDWAR_CYP_R2_greek_network
                set_country_flag = COLDWAR_CYP_R2_greek_network_active
                set_country_flag = COLDWAR_CYP_R2_crisis_active
                COLDWAR_CYP_R2_convene_guarantors = yes
            }
            set_country_flag = COLDWAR_CYP_R2_greek_network_authorized
        """,
        "gre_consult": """
            add_political_power = 50
            CYP = { COLDWAR_CYP_R2_convene_guarantors = yes }
            set_country_flag = COLDWAR_CYP_R2_gre_consult_used
        """,
        "gre_withdraw": """
            CYP = {
                add_to_variable = { COLDWAR_CYP_R2_officer_penetration = -20 }
                clamp_variable = { var = COLDWAR_CYP_R2_officer_penetration min = 0 max = 100 }
                remove_ideas = COLDWAR_CYP_R2_greek_network
                add_ideas = COLDWAR_CYP_R2_greek_withdrawal
                clr_country_flag = COLDWAR_CYP_R2_greek_network_active
                set_country_flag = COLDWAR_CYP_R2_greek_network_withdrawn
            }
            set_country_flag = COLDWAR_CYP_R2_greek_network_withdrawn
        """,
        "gre_coup": """
            add_political_power = -100
            set_temp_variable = { treasury_change = CYP.gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            set_country_flag = COLDWAR_CYP_R2_greek_coup_attempted
            CYP = {
                set_country_flag = COLDWAR_CYP_R2_crisis_active
                set_country_flag = COLDWAR_CYP_R2_coup_warning
                set_country_flag = COLDWAR_CYP_R2_greek_coup_attempted
                set_variable = { COLDWAR_CYP_R2_coup_defense = 40 }
                add_to_variable = { COLDWAR_CYP_R2_coup_defense = COLDWAR_CYP_R2_presidential_preparedness }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.1 hours = 1 }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.2 days = 14 }
                COLDWAR_CYP_R2_convene_guarantors = yes
            }
        """,
        "tur_consult": """
            CYP = { COLDWAR_CYP_R2_convene_guarantors = yes }
            set_country_flag = COLDWAR_CYP_R2_tur_consult_used
        """,
        "tur_terms": """
            CYP = { COLDWAR_CYP_R2_tur_terms_open = yes }
            set_country_flag = COLDWAR_CYP_R2_tur_terms_proposed
        """,
        "tur_operation": """
            add_political_power = -75
            set_temp_variable = { treasury_change = gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            CYP = {
                COLDWAR_CYP_R2_crisis_close_army = yes
                set_country_flag = COLDWAR_CYP_R2_turkish_operation_authorized
            }
            COLDWAR_CYP_R2_begin_turkish_operation = yes
            set_country_flag = COLDWAR_CYP_R2_turkish_operation_used
            set_country_flag = COLDWAR_CYP_R2_army_intervention_used
        """,
        "eng_consult": """
            add_political_power = 35
            CYP = { COLDWAR_CYP_R2_convene_guarantors = yes }
            set_country_flag = COLDWAR_CYP_R2_eng_consult_used
        """,
        "eng_mediation": """
            CYP = { COLDWAR_CYP_R2_english_mediation_open = yes }
            set_country_flag = COLDWAR_CYP_R2_english_mediation_proposed
        """,
        "eng_restraint": """
            add_political_power = 50
            add_ideas = COLDWAR_CYP_R2_english_restraint
            set_country_flag = COLDWAR_CYP_R2_english_restraint_selected
        """,
        "tur_abstain": """
            add_political_power = 75
            set_country_flag = COLDWAR_CYP_R2_tur_refused_intervention
            COLDWAR_CYP_R2_start_army_crisis = yes
        """,
        "gre_response": """
            add_political_power = 25
            CYP = {
                set_country_flag = COLDWAR_CYP_R2_greek_assistance_consultation
                country_event = { id = COLDWAR_CYP_R2_CRISIS.3 hours = 1 }
            }
            set_country_flag = COLDWAR_CYP_R2_gre_response_taken
        """,
        "gre_volunteers": """
            add_political_power = -50
            add_ideas = COLDWAR_CYP_R2_cyprus_volunteer_mission
            set_country_flag = COLDWAR_CYP_R2_volunteer_mission_authorized
        """,
        "gre_escalate": """
            add_political_power = -100
            set_temp_variable = { treasury_change = gdp_total }
            multiply_temp_variable = { treasury_change = -0.005 }
            modify_treasury_effect = yes
            CYP = {
                COLDWAR_CYP_R2_crisis_close_army = yes
                set_country_flag = COLDWAR_CYP_R2_greek_direct_entry_active
                set_country_flag = COLDWAR_CYP_R2_nato_intervention_instance
            }
            if = {
                limit = { has_idea = NATO_member }
                set_country_flag = COLDWAR_CYP_R2_nato_was_member
                set_country_flag = COLDWAR_CYP_R2_nato_separated
            }
            if = {
                limit = { TUR = { has_idea = NATO_member } }
                TUR = {
                    set_country_flag = COLDWAR_CYP_R2_nato_was_member
                    set_country_flag = COLDWAR_CYP_R2_nato_separated
                }
            }
            if = { limit = { has_idea = NATO_member } NATO_leave = yes }
            TUR = { if = { limit = { has_idea = NATO_member } NATO_leave = yes } }
            add_to_war = {
                targeted_alliance = CYP
                enemy = TUR
                hostility_reason = asked_to_join
            }
            set_country_flag = COLDWAR_CYP_R2_greek_direct_entry_used
            CYP = { COLDWAR_CYP_R2_crisis_reconcile = yes }
        """,
    }

    price_refresh = {
        "gre_network": "set_variable = { COLDWAR_CYP_R2_budget_cyp_025 = CYP.gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_cyp_025 = 0.0025 }",
        "gre_coup": "set_variable = { COLDWAR_CYP_R2_budget_cyp_050 = CYP.gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_cyp_050 = 0.005 }",
        "tur_operation": "set_variable = { COLDWAR_CYP_R2_budget_intervention_050 = gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_intervention_050 = 0.005 }",
        "gre_escalate": "set_variable = { COLDWAR_CYP_R2_budget_greek_050 = gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_greek_050 = 0.005 }",
    }

    for key, tag in ACTORS.items():
        body = actor_bodies[key]
        refresh = price_refresh.get(key, "")
        lines = [
            "if = {",
            "\tlimit = {",
            f"\t\toriginal_tag = {tag}",
            "\t\tIMP_is_1970_scenario = yes",
            f"\t\tNOT = {{ has_country_flag = COLDWAR_CYP_R2_applied_{key} }}",
            "\t}",
        ]
        if refresh:
            lines.append("\t" + refresh)
        lines.extend([
            "\tif = {",
            f"\t\tlimit = {{ COLDWAR_CYP_R2_ACT_{key}_available = yes }}",
        ])
        lines.extend("\t\t" + line for line in dedent(body).strip().splitlines())
        lines.extend([
            f"\t\tset_country_flag = COLDWAR_CYP_R2_applied_{key}",
            "\t}",
            "}",
        ])
        effects.append(f"COLDWAR_CYP_R2_ACT_{key}_apply = {{\n{indent(chr(10).join(lines), chr(9))}\n}}\n")

    effects.extend([
        _script("COLDWAR_CYP_R2_begin_turkish_operation", """
            if = {
                limit = {
                    original_tag = TUR
                    IMP_is_1970_scenario = yes
                    NOT = { has_country_flag = COLDWAR_CYP_R2_intervention_receipt_used }
                    CYP = { exists = yes is_subject = no NOT = { has_war_with = TUR } }
                }
                set_country_flag = COLDWAR_CYP_R2_intervention_receipt_used
                set_country_flag = COLDWAR_CYP_R2_intervention_expense_cached
                add_timed_idea = { idea = COLDWAR_CYP_R2_cyprus_intervention_forces days = 180 }
                declare_war_on = { target = CYP type = annex_everything }
                CYP = {
                    set_country_flag = COLDWAR_CYP_R2_turkish_intervention_active
                    set_country_flag = COLDWAR_CYP_R2_crisis_active
                }
            }
        """),
        _script("COLDWAR_CYP_R2_tur_terms_open", """
            if = {
                limit = {
                    original_tag = CYP
                    IMP_is_1970_scenario = yes
                    has_country_flag = COLDWAR_CYP_R2_crisis_active
                    NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_pending }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_resolved }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_attempted }
                    has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent
                    has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent
                    country_exists = GRE
                    country_exists = TUR
                    country_exists = ENG
                }
                set_country_flag = COLDWAR_CYP_R2_tur_terms_pending
                set_country_flag = COLDWAR_CYP_R2_tur_terms_attempted
                set_country_flag = COLDWAR_CYP_R2_tur_terms_CYP_pending
                set_country_flag = COLDWAR_CYP_R2_tur_terms_GRE_pending
                set_country_flag = COLDWAR_CYP_R2_tur_terms_ENG_pending
                country_event = { id = COLDWAR_CYP_R2_CRISIS.20 hours = 1 }
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.21 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.22 hours = 1 } }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.23 days = 14 }
            }
        """),
        _script("COLDWAR_CYP_R2_tur_terms_try_resolve", """
            if = {
                limit = {
                    original_tag = CYP
                    has_country_flag = COLDWAR_CYP_R2_tur_terms_pending
                    has_country_flag = COLDWAR_CYP_R2_tur_terms_CYP_accepted
                    has_country_flag = COLDWAR_CYP_R2_tur_terms_GRE_accepted
                    has_country_flag = COLDWAR_CYP_R2_tur_terms_ENG_accepted
                    has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent
                    has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent
                    NOT = { has_war = yes }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_resolved }
                }
                set_country_flag = COLDWAR_CYP_R2_tur_terms_resolved
                clr_country_flag = COLDWAR_CYP_R2_tur_terms_pending
                TUR = {
                    add_ideas = COLDWAR_CYP_R2_turkish_terms
                    set_country_flag = COLDWAR_CYP_R2_tur_terms_signed
                }
                COLDWAR_CYP_R2_resolve_cyprus_crisis = yes
                set_country_flag = COLDWAR_CYP_R2_security_terms_accepted
                set_country_flag = COLDWAR_CYP_R2_coup_resolved
            }
        """),
        _script("COLDWAR_CYP_R2_english_mediation_open", """
            if = {
                limit = {
                    original_tag = CYP
                    has_country_flag = COLDWAR_CYP_R2_crisis_active
                    NOT = { has_country_flag = COLDWAR_CYP_R2_english_mediation_pending }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_english_mediation_attempted }
                    country_exists = GRE
                    country_exists = TUR
                }
                set_country_flag = COLDWAR_CYP_R2_english_mediation_pending
                set_country_flag = COLDWAR_CYP_R2_english_mediation_attempted
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.30 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.31 hours = 1 } }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.32 hours = 1 }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.33 days = 14 }
            }
        """),
        _script("COLDWAR_CYP_R2_english_mediation_try_resolve", """
            if = {
                limit = {
                    original_tag = CYP
                    has_country_flag = COLDWAR_CYP_R2_english_mediation_pending
                    has_country_flag = COLDWAR_CYP_R2_english_mediation_GRE_yes
                    has_country_flag = COLDWAR_CYP_R2_english_mediation_TUR_yes
                    has_country_flag = COLDWAR_CYP_R2_english_mediation_CYP_yes
                    has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent
                    has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent
                    NOT = { has_country_flag = COLDWAR_CYP_R2_english_mediation_resolved }
                }
                set_country_flag = COLDWAR_CYP_R2_english_mediation_resolved
                clr_country_flag = COLDWAR_CYP_R2_english_mediation_pending
                add_ideas = COLDWAR_CYP_R2_english_mediation
                ENG = { add_political_power = 50 }
            }
        """),
        _script("COLDWAR_CYP_R2_convene_guarantors", """
            if = {
                limit = {
                    original_tag = CYP
                    IMP_is_1970_scenario = yes
                    NOT = { has_country_flag = COLDWAR_CYP_R2_consultation_open }
                    country_exists = GRE
                    country_exists = TUR
                    country_exists = ENG
                }
                clr_country_flag = COLDWAR_CYP_R2_consultation_failed
                set_country_flag = COLDWAR_CYP_R2_consultation_open
                set_country_flag = COLDWAR_CYP_R2_consultation_unresolved
                GRE = { country_event = { id = COLDWAR_CYP_R2_CRISIS.11 hours = 1 } }
                TUR = { country_event = { id = COLDWAR_CYP_R2_CRISIS.12 hours = 1 } }
                ENG = { country_event = { id = COLDWAR_CYP_R2_CRISIS.13 hours = 1 } }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.10 days = 30 }
            }
        """),
        _script("COLDWAR_CYP_R2_geneva_conference", """
            if = {
                limit = {
                    original_tag = CYP
                    IMP_is_1970_scenario = yes
                    has_country_flag = COLDWAR_CYP_R2_crisis_active
                    NOT = { has_country_flag = COLDWAR_CYP_R2_geneva_pending }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_geneva_attempted }
                    has_war = yes
                }
                set_country_flag = COLDWAR_CYP_R2_geneva_pending
                set_country_flag = COLDWAR_CYP_R2_geneva_attempted
                every_country = {
                    limit = { has_war_with = CYP }
                    clr_country_flag = COLDWAR_CYP_R2_geneva_acceptance
                    set_country_flag = COLDWAR_CYP_R2_geneva_response_pending
                    country_event = { id = COLDWAR_CYP_R2_CRISIS.80 hours = 1 }
                }
                country_event = { id = COLDWAR_CYP_R2_CRISIS.81 days = 14 }
            }
        """),
        _script("COLDWAR_CYP_R2_geneva_try_resolve", """
            if = {
                limit = {
                    original_tag = CYP
                    has_country_flag = COLDWAR_CYP_R2_geneva_pending
                    NOT = { has_country_flag = COLDWAR_CYP_R2_geneva_resolved }
                    NOT = {
                        any_country = {
                            has_war_with = CYP
                            NOT = { has_country_flag = COLDWAR_CYP_R2_geneva_acceptance }
                        }
                    }
                }
                set_country_flag = COLDWAR_CYP_R2_geneva_resolved
                clr_country_flag = COLDWAR_CYP_R2_geneva_pending
                every_country = {
                    limit = {
                        has_war_with = CYP
                        has_country_flag = COLDWAR_CYP_R2_geneva_acceptance
                    }
                    white_peace = { tag = CYP }
                }
                COLDWAR_CYP_R2_resolve_cyprus_crisis = yes
                set_country_flag = COLDWAR_CYP_R2_coup_resolved
            }
        """),
        _script("COLDWAR_CYP_R2_crisis_reconcile", """
            if = {
                limit = {
                    country_exists = TUR
                    TUR = {
                        has_country_flag = COLDWAR_CYP_R2_intervention_receipt_used
                        OR = {
                            NOT = { country_exists = CYP }
                            CYP = { NOT = { has_war_with = TUR } }
                        }
                    }
                }
                TUR = {
                    remove_ideas = COLDWAR_CYP_R2_cyprus_intervention_forces
                    clr_country_flag = COLDWAR_CYP_R2_intervention_expense_cached
                    set_country_flag = COLDWAR_CYP_R2_intervention_ended
                }
                if = { limit = { country_exists = CYP } CYP = { clr_country_flag = COLDWAR_CYP_R2_turkish_intervention_active } }
            }
            if = {
                limit = { country_exists = GRE }
                GRE = {
                    if = { limit = { has_country_flag = COLDWAR_CYP_R2_volunteer_mission_authorized }
                        if = {
                            limit = { has_idea = COLDWAR_CYP_R2_cyprus_volunteer_mission }
                            if = {
                                limit = {
                                    country_exists = CYP
                                    CYP = { has_war_with = TUR has_volunteers_amount_from = { tag = GRE count > 0 } }
                                    NOT = { has_war_with = CYP }
                                    NOT = { has_war_with = TUR }
                                }
                                set_country_flag = COLDWAR_CYP_R2_volunteer_expense_active
                            }
                            else = { clr_country_flag = COLDWAR_CYP_R2_volunteer_expense_active }
                            if = {
                                limit = {
                                    OR = {
                                        NOT = { country_exists = CYP }
                                        CYP = { NOT = { has_war_with = TUR } }
                                        has_war_with = CYP
                                        has_war_with = TUR
                                    }
                                }
                                if = { limit = { country_exists = CYP } recall_volunteers_from = CYP }
                                remove_ideas = COLDWAR_CYP_R2_cyprus_volunteer_mission
                                clr_country_flag = COLDWAR_CYP_R2_volunteer_mission_authorized
                                clr_country_flag = COLDWAR_CYP_R2_volunteer_expense_active
                            }
                        }
                        else = {
                            clr_country_flag = COLDWAR_CYP_R2_volunteer_mission_authorized
                            clr_country_flag = COLDWAR_CYP_R2_volunteer_expense_active
                        }
                    }
                }
            }
            if = {
                limit = {
                    country_exists = GRE
                    country_exists = TUR
                }
                if = { limit = { GRE = { has_country_flag = COLDWAR_CYP_R2_nato_was_member has_country_flag = COLDWAR_CYP_R2_nato_separated NOT = { has_war_with = TUR } }
                            OR = { NOT = { country_exists = CYP } CYP = { NOT = { has_war_with = TUR } } } }
                    GRE = { COLDWAR_CYP_R2_try_nato_return = yes }
                }
                if = { limit = { TUR = { has_country_flag = COLDWAR_CYP_R2_nato_was_member has_country_flag = COLDWAR_CYP_R2_nato_separated NOT = { has_war_with = GRE } }
                            OR = { NOT = { country_exists = CYP } CYP = { NOT = { has_war_with = TUR } } } }
                    TUR = { COLDWAR_CYP_R2_try_nato_return = yes }
                }
                if = {
                    limit = {
                        country_exists = CYP
                        CYP = { has_country_flag = COLDWAR_CYP_R2_nato_intervention_instance }
                        NOT = {
                            OR = {
                                GRE = { has_country_flag = COLDWAR_CYP_R2_nato_separated }
                                TUR = { has_country_flag = COLDWAR_CYP_R2_nato_separated }
                            }
                        }
                    }
                    CYP = { clr_country_flag = COLDWAR_CYP_R2_nato_intervention_instance }
                }
            }
        """),
        _script("COLDWAR_CYP_R2_crisis_monthly", """
            if = { limit = { original_tag = CYP IMP_is_1970_scenario = yes } COLDWAR_CYP_R2_crisis_reconcile = yes }
            if = {
                limit = { original_tag = CYP country_exists = TUR country_exists = GRE }
                TUR = {
                    set_variable = { COLDWAR_CYP_R2_budget_intervention_050 = gdp_total }
                    multiply_variable = { COLDWAR_CYP_R2_budget_intervention_050 = 0.005 }
                    set_variable = { COLDWAR_CYP_R2_budget_turkish_025 = gdp_total }
                    multiply_variable = { COLDWAR_CYP_R2_budget_turkish_025 = 0.0025 }
                }
                GRE = {
                    set_variable = { COLDWAR_CYP_R2_budget_cyp_025 = CYP.gdp_total }
                    multiply_variable = { COLDWAR_CYP_R2_budget_cyp_025 = 0.0025 }
                    set_variable = { COLDWAR_CYP_R2_budget_cyp_050 = CYP.gdp_total }
                    multiply_variable = { COLDWAR_CYP_R2_budget_cyp_050 = 0.005 }
                    set_variable = { COLDWAR_CYP_R2_budget_greek_050 = gdp_total }
                    multiply_variable = { COLDWAR_CYP_R2_budget_greek_050 = 0.005 }
                }
            }
        """),
        _script("COLDWAR_CYP_R2_crisis_weekly_streams", """
            set_variable = { COLDWAR_CYP_R2_crisis_weekly_expenses = 0 }
            if = {
                limit = { has_country_flag = COLDWAR_CYP_R2_intervention_expense_cached }
                set_variable = { COLDWAR_CYP_R2_crisis_weekly_expenses = gdp_total }
                multiply_variable = { COLDWAR_CYP_R2_crisis_weekly_expenses = 0.00005 }
            }
            if = {
                limit = { has_country_flag = COLDWAR_CYP_R2_volunteer_expense_active }
                set_temp_variable = { COLDWAR_CYP_R2_weekly_volunteer_cost = gdp_total }
                multiply_temp_variable = { COLDWAR_CYP_R2_weekly_volunteer_cost = 0.00002 }
                add_to_variable = { COLDWAR_CYP_R2_crisis_weekly_expenses = COLDWAR_CYP_R2_weekly_volunteer_cost }
            }
        """),
        _script("COLDWAR_CYP_R2_try_nato_return", """
            if = {
                limit = {
                    COLDWAR_CYP_R2_nato_join_allowed = yes
                    COLDWAR_CYP_R2_nato_return_allowed = yes
                    has_country_flag = COLDWAR_CYP_R2_nato_was_member
                    has_country_flag = COLDWAR_CYP_R2_nato_separated
                    has_idea = NATO_member
                }
                clr_country_flag = COLDWAR_CYP_R2_nato_separated
                clr_country_flag = COLDWAR_CYP_R2_nato_was_member
            }
            else_if = {
                limit = {
                    COLDWAR_CYP_R2_nato_join_allowed = yes
                    COLDWAR_CYP_R2_nato_return_allowed = yes
                    has_country_flag = COLDWAR_CYP_R2_nato_was_member
                    has_country_flag = COLDWAR_CYP_R2_nato_separated
                    NOT = { has_idea = NATO_member }
                    NATO_currently_exists = yes
                }
                NATO_join = yes
                if = { limit = { has_idea = NATO_member } clr_country_flag = COLDWAR_CYP_R2_nato_separated clr_country_flag = COLDWAR_CYP_R2_nato_was_member }
            }
        """),
    ])

    for key in ACTORS:
        effects.append(_script(f"COLDWAR_CYP_R2_ACT_{key}_preview", f"effect_tooltip = {{\n{indent(dedent(_actor_preview_body(key)).strip(), chr(9))}\n}}"))
    return "# IMPERIA COLD WAR — Cyprus 1970 generated crisis and guarantor effects.\n" + "\n".join(effects)


def _trigger_file() -> str:
    conditions = {
        "gre_officers": """original_tag = GRE\ncountry_exists = CYP\nCYP = { IMP_is_1970_scenario = yes }""",
        "gre_treaty": """original_tag = GRE\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_greek_officer_footprint }\nNOT = { has_war_with = CYP }""",
        "gre_network": """original_tag = GRE\ncountry_exists = CYP\nnationalist_military_junta_are_in_power = yes\nCYP = { has_country_flag = COLDWAR_CYP_R2_greek_officer_footprint NOT = { has_country_flag = COLDWAR_CYP_R2_greek_network_withdrawn } check_variable = { gdp_total > 0 } }\ncheck_variable = { political_power >= 50 }\ncheck_variable = { treasury >= COLDWAR_CYP_R2_budget_cyp_025 }""",
        "gre_consult": """original_tag = GRE\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active }""",
        "gre_withdraw": """original_tag = GRE\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_greek_network_active NOT = { has_country_flag = COLDWAR_CYP_R2_coup_warning } }""",
        "gre_coup": """original_tag = GRE\nIMP_is_1970_scenario = yes\nnationalist_military_junta_are_in_power = yes\ncountry_exists = CYP\nCYP = { IMP_is_1970_scenario = yes is_subject = no has_country_flag = COLDWAR_CYP_R2_greek_network_active has_country_flag = COLDWAR_CYP_R2_greek_officer_footprint NOT = { has_war_with = GRE } check_variable = { COLDWAR_CYP_R2_officer_penetration >= 60 } check_variable = { gdp_total > 0 } }\nNOT = { has_country_flag = COLDWAR_CYP_R2_greek_coup_attempted }\ncheck_variable = { political_power >= 100 }\ncheck_variable = { treasury >= COLDWAR_CYP_R2_budget_cyp_050 }""",
        "tur_consult": """original_tag = TUR\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active }""",
        "tur_terms": """original_tag = TUR\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active has_country_flag = COLDWAR_CYP_R2_consultation_open has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_resolved } }\nNOT = { has_war_with = CYP }""",
        "tur_operation": """original_tag = TUR\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\nCYP = { is_subject = no has_country_flag = COLDWAR_CYP_R2_crisis_active has_country_flag = COLDWAR_CYP_R2_consultation_failed NOT = { has_war_with = TUR } }\nNOT = { has_country_flag = COLDWAR_CYP_R2_intervention_receipt_used }\nNOT = { has_country_flag = COLDWAR_CYP_R2_turkish_operation_used }\ncheck_variable = { gdp_total > 0 }\ncheck_variable = { political_power >= 75 }\ncheck_variable = { treasury >= COLDWAR_CYP_R2_budget_intervention_050 }""",
        "eng_consult": """original_tag = ENG\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active }""",
        "eng_mediation": """original_tag = ENG\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active has_country_flag = COLDWAR_CYP_R2_consultation_open NOT = { has_country_flag = COLDWAR_CYP_R2_english_mediation_resolved } }""",
        "eng_restraint": """original_tag = ENG\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active has_country_flag = COLDWAR_CYP_R2_consultation_open }\nNOT = { has_country_flag = COLDWAR_CYP_R2_english_mediation_proposed }\ncheck_variable = { political_power >= 50 }""",
        "tur_abstain": """original_tag = TUR\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\nCYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active }\nNOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_started }\ncheck_variable = { political_power >= 25 }""",
        "gre_response": """original_tag = GRE\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\ncountry_exists = TUR\nTUR = { has_war_with = CYP }\nCYP = { has_country_flag = COLDWAR_CYP_R2_turkish_intervention_active }\nNOT = { has_war_with = CYP }""",
        "gre_volunteers": """original_tag = GRE\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\ncountry_exists = TUR\nTUR = { has_war_with = CYP }\nCYP = { has_country_flag = COLDWAR_CYP_R2_turkish_intervention_active }\nNOT = { has_war_with = CYP }\nNOT = { has_war_with = TUR }""",
        "gre_escalate": """original_tag = GRE\nIMP_is_1970_scenario = yes\ncountry_exists = CYP\ncountry_exists = TUR\nTUR = { has_war_with = CYP }\nCYP = { has_country_flag = COLDWAR_CYP_R2_turkish_intervention_active }\nNOT = { has_war_with = CYP }\nNOT = { has_war_with = TUR }\ncheck_variable = { gdp_total > 0 }\ncheck_variable = { political_power >= 100 }\ncheck_variable = { treasury >= COLDWAR_CYP_R2_budget_greek_050 }""",
    }
    output = []
    for key, tag in ACTORS.items():
        body = conditions[key] + f"\nNOT = {{ has_country_flag = COLDWAR_CYP_R2_applied_{key} }}"
        output.append(_script(f"COLDWAR_CYP_R2_ACT_{key}_available", body))
    output.extend([
        _script("COLDWAR_CYP_R2_nato_join_allowed", """
            OR = {
                NOT = { has_country_flag = COLDWAR_CYP_R2_nato_separated }
                AND = {
                    has_country_flag = COLDWAR_CYP_R2_nato_separated
                    NOT = { GRE = { has_war_with = TUR } }
                    OR = {
                        NOT = { country_exists = CYP }
                        CYP = { NOT = { has_war_with = TUR } }
                    }
                }
            }
        """),
        _script("COLDWAR_CYP_R2_nato_return_allowed", """
            exists = yes
            is_subject = no
            NATO_currently_exists = yes
            can_join_NATO = yes
            NOT = { is_in_faction = yes }
            any_country = {
                has_idea = NATO_member
                is_faction_leader = yes
            }
            NOT = {
                any_country = {
                    has_idea = NATO_member
                    ROOT = { has_war_with = PREV }
                }
            }
        """),
    ])
    return "# IMPERIA COLD WAR — Cyprus 1970 generated crisis triggers.\n" + "\n".join(output)


def _ideas_file() -> str:
    pieces = ["# IMPERIA COLD WAR — Cyprus 1970 generated crisis spirits.", "ideas = {", "\tcountry = {"]
    for key, (tag, values) in IDEAS.items():
        idea = PREFIX + key
        modifier = _modifier_block(values)
        lifecycle = ""
        if key == "cyprus_volunteer_mission":
            lifecycle = (
                "\n\t\t\trule = { can_send_volunteers = yes }"
                "\n\t\t\ton_add = { add_relation_rule_override = { target = CYP can_send_volunteers = yes } }"
                "\n\t\t\ton_remove = { remove_relation_rule_override = { target = CYP can_send_volunteers = yes } }"
            )
        pieces.append(f"\t\t{idea} = {{\n\t\t\tpicture = generic_political_support\n\t\t\tallowed = {{ always = no }}\n\t\t\tallowed_civil_war = {{ always = yes }}{lifecycle}\n\t\t\tmodifier = {{\n{indent(modifier, chr(9) * 4)}\n\t\t\t}}\n\t\t}}")
    pieces.extend(["\t}", "}"])
    return "\n".join(pieces)


def _decision_files() -> dict[str, str]:
    category = _script("COLDWAR_CYP_R2_turkish_army_crisis", """
        icon = GFX_decision_category_generic_political_reform
        visible = { original_tag = TUR has_country_flag = COLDWAR_CYP_R2_army_crisis_active }
        allowed = { original_tag = TUR }
    """)
    records = [
        ("rotate", "Reassign Exposed Commanders", -50, .0025, "COLDWAR_CYP_R2_army_commanders_used", """
            has_country_flag = COLDWAR_CYP_R2_army_crisis_active
            NOT = { has_country_flag = COLDWAR_CYP_R2_army_commanders_used }
            NOT = { nationalist_military_junta_are_in_power = yes }
            check_variable = { gdp_total > 0 }
            check_variable = { political_power >= 50 }
            check_variable = { treasury >= COLDWAR_CYP_R2_budget_turkish_025 }
        """),
        ("mandate", "Secure a Parliamentary Mandate", -75, 0, "COLDWAR_CYP_R2_army_mandate_used", """
            has_country_flag = COLDWAR_CYP_R2_army_crisis_active
            NOT = { has_country_flag = COLDWAR_CYP_R2_army_mandate_used }
            NOT = { nationalist_military_junta_are_in_power = yes }
            check_variable = { political_power >= 75 }
        """),
        ("control", "Reassert Civilian Authority", -75, .0025, "COLDWAR_CYP_R2_army_control_used", """
            has_country_flag = COLDWAR_CYP_R2_army_crisis_active
            has_country_flag = COLDWAR_CYP_R2_army_commanders_used
            has_country_flag = COLDWAR_CYP_R2_army_mandate_used
            NOT = { nationalist_military_junta_are_in_power = yes }
            NOT = { has_country_flag = COLDWAR_CYP_R2_army_takeover_succeeded }
            check_variable = { COLDWAR_CYP_R2_military_pressure <= 35 }
            check_variable = { gdp_total > 0 }
            check_variable = { political_power >= 75 }
            check_variable = { treasury >= COLDWAR_CYP_R2_budget_turkish_025 }
        """),
        ("intervene", "Authorize the Cyprus Operation", -75, .005, "COLDWAR_CYP_R2_army_intervention_used", """
            has_country_flag = COLDWAR_CYP_R2_army_crisis_active
            NOT = { has_country_flag = COLDWAR_CYP_R2_army_intervention_used }
            NOT = { has_country_flag = COLDWAR_CYP_R2_intervention_receipt_used }
            NOT = { has_country_flag = COLDWAR_CYP_R2_army_takeover_succeeded }
            country_exists = CYP
            CYP = { has_country_flag = COLDWAR_CYP_R2_crisis_active NOT = { has_war_with = TUR } is_subject = no }
            check_variable = { gdp_total > 0 }
            check_variable = { political_power >= 75 }
            check_variable = { treasury >= COLDWAR_CYP_R2_budget_intervention_050 }
        """),
    ]
    decisions = ["# IMPERIA COLD WAR — Cyprus 1970 generated Turkish army crisis decisions.", "COLDWAR_CYP_R2_turkish_army_crisis = {"]
    for key, title, pp, gdpfrac, receipt, available in records:
        decision = f"COLDWAR_CYP_R2_army_{key}"
        native_effects = [f"add_political_power = {pp}"]
        if gdpfrac:
            native_effects += ["set_temp_variable = { treasury_change = gdp_total }", f"multiply_temp_variable = {{ treasury_change = -{gdpfrac:g} }}", "modify_treasury_effect = yes"]
        native_effects += [f"set_country_flag = {receipt}"]
        if key == "rotate":
            native_effects += ["add_to_variable = { COLDWAR_CYP_R2_military_pressure = -25 tooltip = COLDWAR_CYP_R2_military_pressure_tt }",
                "clamp_variable = { var = COLDWAR_CYP_R2_military_pressure min = 0 max = 100 }"]
        elif key == "mandate":
            native_effects += ["add_to_variable = { COLDWAR_CYP_R2_military_pressure = -25 tooltip = COLDWAR_CYP_R2_military_pressure_tt }",
                "clamp_variable = { var = COLDWAR_CYP_R2_military_pressure min = 0 max = 100 }"]
        elif key == "control":
            native_effects = ["CYP = { COLDWAR_CYP_R2_crisis_close_army = yes }", f"add_political_power = {pp}",
                "set_temp_variable = { treasury_change = gdp_total }", "multiply_temp_variable = { treasury_change = -0.0025 }", "modify_treasury_effect = yes",
                "remove_ideas = COLDWAR_CYP_R2_angry_general_staff", "add_timed_idea = { idea = COLDWAR_CYP_R2_command_reorganization days = 90 }",
                f"set_country_flag = {receipt}"]
        else:
            native_effects = [
                "set_country_flag = COLDWAR_CYP_R2_intervention_receipt_used",
                "set_country_flag = COLDWAR_CYP_R2_intervention_expense_cached",
                f"set_country_flag = {receipt}",
                f"add_political_power = {pp}",
                "set_temp_variable = { treasury_change = gdp_total }",
                "multiply_temp_variable = { treasury_change = -0.005 }",
                "modify_treasury_effect = yes",
                "CYP = { COLDWAR_CYP_R2_crisis_close_army = yes set_country_flag = COLDWAR_CYP_R2_turkish_intervention_active set_country_flag = COLDWAR_CYP_R2_crisis_active }",
                "add_timed_idea = { idea = COLDWAR_CYP_R2_cyprus_intervention_forces days = 180 }",
                "declare_war_on = { target = CYP type = annex_everything }",
                "custom_effect_tooltip = COLDWAR_CYP_R2_weekly_intervention_expense_tt"]
        price_refresh = {
            "rotate": "set_variable = { COLDWAR_CYP_R2_budget_turkish_025 = gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_turkish_025 = 0.0025 }",
            "control": "set_variable = { COLDWAR_CYP_R2_budget_turkish_025 = gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_turkish_025 = 0.0025 }",
            "intervene": "set_variable = { COLDWAR_CYP_R2_budget_intervention_050 = gdp_total }\nmultiply_variable = { COLDWAR_CYP_R2_budget_intervention_050 = 0.005 }",
        }.get(key)
        complete = []
        if price_refresh:
            complete.append(price_refresh)
        actual_guard = "original_tag = TUR\nIMP_is_1970_scenario = yes\n" + dedent(available).strip()
        complete.append("if = {\nlimit = {\n" + actual_guard + "\n}\n" + "\n".join(native_effects) + "\n}")
        decisions.append(f"\t{decision} = {{\n\t\ticon = GFX_decision_generic_political_discourse\n\t\tcost = 0\n\t\tvisible = {{ has_country_flag = COLDWAR_CYP_R2_army_crisis_active }}\n\t\tavailable = {{\n{indent(dedent(available).strip(), chr(9) * 3)}\n\t\t}}\n\t\tcomplete_effect = {{\n{indent(chr(10).join(complete), chr(9) * 3)}\n\t\t}}\n\t\tai_will_do = {{ base = 0 }}\n\t}}")
    decisions.append("}")
    return {
        "common/decisions/categories/COLDWAR_CYP_R2_crisis.txt": "# IMPERIA COLD WAR — Cyprus 1970 generated crisis decision category.\n" + category,
        "common/decisions/COLDWAR_CYP_R2_crisis.txt": "\n\n".join(decisions),
    }


def _events_file() -> str:
    events: list[str] = ["# IMPERIA COLD WAR — Cyprus 1970 generated crisis events.", f"add_namespace = {NS}"]

    def event(event_id: int, title: str, desc: str, tag: str | None, opts: list[str]) -> str:
        trigger = (f"original_tag = {tag}\nIMP_is_1970_scenario = yes" if tag else
                   "has_country_flag = COLDWAR_CYP_R2_geneva_response_pending")
        timing = "is_triggered_only = yes"
        option_text = "\n".join(opts)
        return _script("country_event", f"""
            id = {NS}.{event_id}
            title = {title}
            desc = {desc}
            picture = GFX_COLDWAR_CYP_R2_agreement
            {timing}
            trigger = {{ {trigger} }}
            {option_text}
        """)

    def option(name: str, effect: str, trigger: str = "", ai_weight: int | None = None) -> str:
        trig = f"trigger = {{ {trigger} }}" if trigger else ""
        ai = f"ai_chance = {{ factor = {ai_weight} }}" if ai_weight is not None else ""
        return _script("option", f"""
            name = {name}
            {trig}
            {ai}
            {effect}
        """)

    # The 14-day coup warning is informational. The delayed resolution is deterministic, and ties defend the civilian government.
    events.append(event(1, "COLDWAR_CYP_R2_coup_warning_title", "COLDWAR_CYP_R2_coup_warning_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            custom_effect_tooltip = COLDWAR_CYP_R2_coup_warning_effect_tt
        """),
    ]))
    events.append(event(2, "COLDWAR_CYP_R2_coup_resolution_title", "COLDWAR_CYP_R2_coup_resolution_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            if = {
                limit = {
                    has_country_flag = COLDWAR_CYP_R2_coup_warning
                    NOT = { has_country_flag = COLDWAR_CYP_R2_coup_resolved }
                    check_variable = { COLDWAR_CYP_R2_officer_penetration > COLDWAR_CYP_R2_coup_defense }
                }
                COLDWAR_CYP_R2_install_coup_government = yes
                set_country_flag = COLDWAR_CYP_R2_coup_government
                set_country_flag = COLDWAR_CYP_R2_coup_resolved
                clr_country_flag = COLDWAR_CYP_R2_coup_warning
            }
            else = {
                if = { limit = { has_country_flag = COLDWAR_CYP_R2_coup_warning NOT = { has_country_flag = COLDWAR_CYP_R2_coup_resolved } }
                    set_country_flag = COLDWAR_CYP_R2_coup_resolved
                    clr_country_flag = COLDWAR_CYP_R2_coup_warning
                }
            }
        """),
    ]))
    events.append(event(3, "COLDWAR_CYP_R2_greek_assistance_title", "COLDWAR_CYP_R2_greek_assistance_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """set_country_flag = COLDWAR_CYP_R2_greek_assistance_notice_seen"""),
    ]))

    # Informed consultation is a notification with affirmative/refusal replies; silence is recorded as abstention at day 30.
    for number, tag, title in ((11, "GRE", "COLDWAR_CYP_R2_consult_GRE_title"),
                               (12, "TUR", "COLDWAR_CYP_R2_consult_TUR_title"),
                               (13, "ENG", "COLDWAR_CYP_R2_consult_ENG_title")):
        events.append(event(number, title, "COLDWAR_CYP_R2_consultation_desc", tag, [
            option("COLDWAR_CYP_R2_consult_participate", f"""
                if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_consultation_open }} }}
                    CYP = {{ set_country_flag = COLDWAR_CYP_R2_consult_{tag}_participating }}
                }}
            """),
            option("COLDWAR_CYP_R2_consult_abstain", f"""
                if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_consultation_open }} }}
                    CYP = {{ set_country_flag = COLDWAR_CYP_R2_consult_{tag}_abstained }}
                }}
            """),
        ]))
    events.append(event(10, "COLDWAR_CYP_R2_consultation_deadline_title", "COLDWAR_CYP_R2_consultation_deadline_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            if = {
                limit = {
                    has_country_flag = COLDWAR_CYP_R2_consultation_open
                    has_country_flag = COLDWAR_CYP_R2_consultation_unresolved
                }
                clr_country_flag = COLDWAR_CYP_R2_consultation_open
                clr_country_flag = COLDWAR_CYP_R2_consultation_unresolved
                if = {
                    limit = {
                        has_country_flag = COLDWAR_CYP_R2_crisis_active
                        NOT = { has_country_flag = COLDWAR_CYP_R2_tur_terms_resolved }
                        NOT = { has_country_flag = COLDWAR_CYP_R2_turkish_intervention_active }
                    }
                    set_country_flag = COLDWAR_CYP_R2_consultation_failed
                    TUR = { COLDWAR_CYP_R2_start_army_crisis = yes }
                }
            }
        """),
    ]))

    # Guarantor consent events record named approvals. Options are real country responses; no focus reward is granted by previews.
    for number, tag in ((21, "GRE"), (22, "ENG")):
        events.append(event(number, f"COLDWAR_CYP_R2_tur_terms_{tag}_title", "COLDWAR_CYP_R2_tur_terms_desc", tag, [
            option("COLDWAR_CYP_R2_offer_accept", f"""
                if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_tur_terms_pending }} }}
                    CYP = {{ set_country_flag = COLDWAR_CYP_R2_tur_terms_{tag}_accepted COLDWAR_CYP_R2_tur_terms_try_resolve = yes }}
                }}
            """, ai_weight=0),
            option("COLDWAR_CYP_R2_offer_refuse", f"""
                CYP = {{
                    if = {{ limit = {{ has_country_flag = COLDWAR_CYP_R2_tur_terms_pending }}
                        set_country_flag = COLDWAR_CYP_R2_tur_terms_{tag}_refused
                        clr_country_flag = COLDWAR_CYP_R2_tur_terms_pending
                    }}
                }}
            """, ai_weight=100),
        ]))
    events.append(event(20, "COLDWAR_CYP_R2_tur_terms_CYP_title", "COLDWAR_CYP_R2_tur_terms_desc", "CYP", [
        option("COLDWAR_CYP_R2_offer_accept", """
            trigger = {
                has_country_flag = COLDWAR_CYP_R2_tur_terms_pending
                has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent
                has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent
            }
            set_country_flag = COLDWAR_CYP_R2_tur_terms_CYP_accepted
            COLDWAR_CYP_R2_tur_terms_try_resolve = yes
        """, ai_weight=0),
        option("COLDWAR_CYP_R2_offer_refuse", """
            if = { limit = { has_country_flag = COLDWAR_CYP_R2_tur_terms_pending }
                set_country_flag = COLDWAR_CYP_R2_tur_terms_CYP_refused
                clr_country_flag = COLDWAR_CYP_R2_tur_terms_pending
            }
        """, ai_weight=100),
    ]))
    events.append(event(23, "COLDWAR_CYP_R2_tur_terms_deadline_title", "COLDWAR_CYP_R2_tur_terms_deadline_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """clr_country_flag = COLDWAR_CYP_R2_tur_terms_pending"""),
    ]))

    for number, tag in ((30, "GRE"), (31, "TUR")):
        events.append(event(number, f"COLDWAR_CYP_R2_english_mediation_{tag}_title", "COLDWAR_CYP_R2_english_mediation_desc", tag, [
            option("COLDWAR_CYP_R2_offer_accept", f"""
                if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_english_mediation_pending }} }}
                    CYP = {{ set_country_flag = COLDWAR_CYP_R2_english_mediation_{tag}_yes COLDWAR_CYP_R2_english_mediation_try_resolve = yes }}
                }}
            """, ai_weight=0),
            option("COLDWAR_CYP_R2_offer_refuse", f"""
                if = {{ limit = {{ CYP = {{ has_country_flag = COLDWAR_CYP_R2_english_mediation_pending }} }}
                    CYP = {{ set_country_flag = COLDWAR_CYP_R2_english_mediation_{tag}_no clr_country_flag = COLDWAR_CYP_R2_english_mediation_pending }}
                }}
            """, ai_weight=100),
        ]))
    events.append(event(32, "COLDWAR_CYP_R2_english_mediation_CYP_title", "COLDWAR_CYP_R2_english_mediation_desc", "CYP", [
        option("COLDWAR_CYP_R2_offer_accept", """
            trigger = { has_country_flag = COLDWAR_CYP_R2_english_mediation_pending has_country_flag = COLDWAR_CYP_R2_greek_delegation_assent has_country_flag = COLDWAR_CYP_R2_turkish_delegation_assent }
            set_country_flag = COLDWAR_CYP_R2_english_mediation_CYP_yes
            COLDWAR_CYP_R2_english_mediation_try_resolve = yes
        """, ai_weight=0),
        option("COLDWAR_CYP_R2_offer_refuse", """clr_country_flag = COLDWAR_CYP_R2_english_mediation_pending""", ai_weight=100),
    ]))
    events.append(event(33, "COLDWAR_CYP_R2_english_mediation_deadline_title", "COLDWAR_CYP_R2_english_mediation_deadline_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """clr_country_flag = COLDWAR_CYP_R2_english_mediation_pending"""),
    ]))

    # Turkish army chain: finite delayed events at 30, 60 and 180 days, each protected by an active-instance receipt.
    events.append(event(40, "COLDWAR_CYP_R2_army_memorandum_title", "COLDWAR_CYP_R2_army_memorandum_desc", "TUR", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            if = {
                limit = { has_country_flag = COLDWAR_CYP_R2_army_crisis_active NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed } NOT = { has_country_flag = COLDWAR_CYP_R2_army_memorandum_recorded } }
                add_to_variable = { COLDWAR_CYP_R2_military_pressure = 15 }
                clamp_variable = { var = COLDWAR_CYP_R2_military_pressure min = 0 max = 100 }
                set_country_flag = COLDWAR_CYP_R2_army_memorandum_recorded
            }
        """),
    ]))
    events.append(event(41, "COLDWAR_CYP_R2_army_coup_title", "COLDWAR_CYP_R2_army_coup_desc", "TUR", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            if = {
                limit = {
                    has_country_flag = COLDWAR_CYP_R2_army_crisis_active
                    NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_army_coup_resolved }
                    check_variable = { COLDWAR_CYP_R2_military_pressure >= 60 }
                }
                set_country_flag = COLDWAR_CYP_R2_army_takeover_succeeded
                set_country_flag = COLDWAR_CYP_R2_army_coup_resolved
                set_variable = { ruling_party = 22 }
                set_politics = { ruling_party = nationalist elections_allowed = no }
                COLDWAR_TUR_1970_set_leader = yes
            }
            else_if = {
                limit = {
                    has_country_flag = COLDWAR_CYP_R2_army_crisis_active
                    NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed }
                    NOT = { has_country_flag = COLDWAR_CYP_R2_army_coup_resolved }
                    check_variable = { COLDWAR_CYP_R2_military_pressure > 35 }
                    check_variable = { COLDWAR_CYP_R2_military_pressure < 60 }
                }
                add_stability = -0.05
                set_country_flag = COLDWAR_CYP_R2_army_plot_defeated
                set_country_flag = COLDWAR_CYP_R2_army_coup_resolved
            }
            else = {
                if = {
                    limit = { has_country_flag = COLDWAR_CYP_R2_army_crisis_active NOT = { has_country_flag = COLDWAR_CYP_R2_army_crisis_closed } NOT = { has_country_flag = COLDWAR_CYP_R2_army_coup_resolved } check_variable = { COLDWAR_CYP_R2_military_pressure <= 35 } }
                    set_country_flag = COLDWAR_CYP_R2_army_plot_defeated
                    set_country_flag = COLDWAR_CYP_R2_army_coup_resolved
                }
            }
            if = {
                limit = { has_country_flag = COLDWAR_CYP_R2_army_coup_resolved has_country_flag = COLDWAR_CYP_R2_army_crisis_active }
                set_country_flag = COLDWAR_CYP_R2_army_crisis_closed
                clr_country_flag = COLDWAR_CYP_R2_army_crisis_active
                CYP = { clr_country_flag = COLDWAR_CYP_R2_army_crisis_active }
            }
        """),
    ]))
    events.append(event(42, "COLDWAR_CYP_R2_army_crisis_end_title", "COLDWAR_CYP_R2_army_crisis_end_desc", "TUR", [
        option("COLDWAR_CYP_R2_event_acknowledge", """
            if = { limit = { has_country_flag = COLDWAR_CYP_R2_army_crisis_active }
                set_country_flag = COLDWAR_CYP_R2_army_crisis_closed
                clr_country_flag = COLDWAR_CYP_R2_army_crisis_active
                remove_ideas = COLDWAR_CYP_R2_angry_general_staff
                CYP = { clr_country_flag = COLDWAR_CYP_R2_army_crisis_active }
            }
        """),
    ]))

    # Geneva asks every actual Cyprus belligerent. White peace is bilateral with CYP only after every current belligerent signs.
    events.append(event(80, "COLDWAR_CYP_R2_geneva_offer_title", "COLDWAR_CYP_R2_geneva_offer_desc", None, [
        option("COLDWAR_CYP_R2_offer_accept", """
            if = { limit = { has_country_flag = COLDWAR_CYP_R2_geneva_response_pending CYP = { has_country_flag = COLDWAR_CYP_R2_geneva_pending } }
                set_country_flag = COLDWAR_CYP_R2_geneva_acceptance
                CYP = { COLDWAR_CYP_R2_geneva_try_resolve = yes }
            }
        """, ai_weight=0),
        option("COLDWAR_CYP_R2_offer_refuse", """
            if = { limit = { has_country_flag = COLDWAR_CYP_R2_geneva_response_pending CYP = { has_country_flag = COLDWAR_CYP_R2_geneva_pending } }
                clr_country_flag = COLDWAR_CYP_R2_geneva_response_pending
                CYP = { clr_country_flag = COLDWAR_CYP_R2_geneva_pending set_country_flag = COLDWAR_CYP_R2_geneva_refused }
            }
        """, ai_weight=100),
    ]))
    events.append(event(81, "COLDWAR_CYP_R2_geneva_deadline_title", "COLDWAR_CYP_R2_geneva_deadline_desc", "CYP", [
        option("COLDWAR_CYP_R2_event_acknowledge", """clr_country_flag = COLDWAR_CYP_R2_geneva_pending"""),
    ]))

    return "\n".join(events)


def _loc(design: dict) -> dict[str, str]:
    loc = {}
    loc.update({
        "COLDWAR_CYP_R2_event_acknowledge": "Acknowledge",
        "COLDWAR_CYP_R2_offer_accept": "Accept the proposal",
        "COLDWAR_CYP_R2_offer_refuse": "Refuse the proposal",
        "COLDWAR_CYP_R2_consult_participate": "Participate in consultation",
        "COLDWAR_CYP_R2_consult_abstain": "Abstain from consultation",
        "COLDWAR_CYP_R2_coup_warning_title": "Warning of a Coup Attempt",
        "COLDWAR_CYP_R2_coup_warning_desc": "The Greek officer network is preparing to overthrow the government. Its strength will be compared with the Republic's prepared defence after 14 days.",
        "COLDWAR_CYP_R2_coup_resolution_title": "The Coup Attempt",
        "COLDWAR_CYP_R2_coup_resolution_desc": "The armed network moves against the constitutional government. The prepared defence succeeds in a tie.",
        "COLDWAR_CYP_R2_coup_warning_effect_tt": "Resolution in 14 days. Defence: 40 + presidential preparedness. Strength: current officer penetration. Ties favour the defender.",
        "COLDWAR_CYP_R2_greek_assistance_title": "Greek Assistance for Cyprus",
        "COLDWAR_CYP_R2_greek_assistance_desc": "Greece has opened an assistance channel during the war. Cyprus may accept or refuse the offer.",
        "COLDWAR_CYP_R2_consult_GRE_title": "Guarantor Consultation: Greece",
        "COLDWAR_CYP_R2_consult_TUR_title": "Guarantor Consultation: Turkey",
        "COLDWAR_CYP_R2_consult_ENG_title": "Guarantor Consultation: United Kingdom",
        "COLDWAR_CYP_R2_consultation_desc": "The guarantors have been asked to consult on the constitutional crisis in Cyprus. Silence at the deadline is treated as abstention.",
        "COLDWAR_CYP_R2_consultation_deadline_title": "Consultation Deadline",
        "COLDWAR_CYP_R2_consultation_deadline_desc": "The 30-day consultation period has ended without a settlement. If the Cyprus crisis remains active, Turkey's army crisis begins.",
        "COLDWAR_CYP_R2_tur_terms_CYP_title": "Communal Guarantees Proposal",
        "COLDWAR_CYP_R2_tur_terms_GRE_title": "Communal Guarantees Proposal",
        "COLDWAR_CYP_R2_tur_terms_ENG_title": "Communal Guarantees Proposal",
        "COLDWAR_CYP_R2_tur_terms_desc": "Turkey proposes constitutional safeguards. Cyprus can accept only after both communal delegations have separately assented. Greece and the United Kingdom decide their own response.",
        "COLDWAR_CYP_R2_tur_terms_deadline_title": "Communal Guarantees Lapse",
        "COLDWAR_CYP_R2_tur_terms_deadline_desc": "The proposal lapses after 14 days without every required signature.",
        "COLDWAR_CYP_R2_english_mediation_GRE_title": "Joint Restoration Proposal",
        "COLDWAR_CYP_R2_english_mediation_TUR_title": "Joint Restoration Proposal",
        "COLDWAR_CYP_R2_english_mediation_CYP_title": "Joint Restoration Proposal",
        "COLDWAR_CYP_R2_english_mediation_deadline_title": "Joint Restoration Proposal Lapses",
        "COLDWAR_CYP_R2_english_mediation_deadline_desc": "The joint restoration proposal lapses after 14 days without every required signature.",
        "COLDWAR_CYP_R2_english_mediation_desc": "The United Kingdom proposes coordinated mediation. Greece and Turkey must agree, and Cyprus must ratify after both communal delegations assent.",
        "COLDWAR_CYP_R2_army_memorandum_title": "The General Staff Memorandum",
        "COLDWAR_CYP_R2_army_memorandum_desc": "Senior officers challenge civilian authority. If the army crisis is still active, military pressure rises by 15.",
        "COLDWAR_CYP_R2_army_coup_title": "The Turkish Army Crisis",
        "COLDWAR_CYP_R2_army_coup_desc": "At day 60, pressure of 60 or more installs the dated military-junta government. Pressure of 36 to 59 defeats the plot with stability -5%. Pressure of 35 or less defeats it without a further penalty.",
        "COLDWAR_CYP_R2_army_crisis_end_title": "The Army Crisis Ends",
        "COLDWAR_CYP_R2_army_crisis_end_desc": "The finite 180-day army crisis has ended. Its pending outcomes can no longer fire.",
        "COLDWAR_CYP_R2_geneva_offer_title": "Ceasefire and Constitutional Restoration",
        "COLDWAR_CYP_R2_geneva_offer_desc": "Every country currently at war with Cyprus receives this proposal. A white peace with Cyprus is applied only if every current Cyprus belligerent accepts.",
        "COLDWAR_CYP_R2_geneva_deadline_title": "Geneva Proposal Expires",
        "COLDWAR_CYP_R2_geneva_deadline_desc": "The 14-day Geneva response period has elapsed. No ceasefire is imposed without every belligerent's consent.",
        "COLDWAR_CYP_R2_military_pressure_tt": "Military pressure: $RIGHT|+=0$",
        "COLDWAR_CYP_R2_army_pressure_preview_tt": "Military pressure starts at 70. The day 30 memorandum adds 15. The day 60 coup succeeds at 60 or more.",
        "COLDWAR_CYP_R2_offer_if_accepted_tt": "If all required participants accept:",
        "COLDWAR_CYP_R2_weekly_intervention_expense_tt": "Weekly expedition expense: 0.005% of current Turkish GDP while the intervention remains active.",
        "COLDWAR_CYP_R2_weekly_volunteer_expense_tt": "Weekly volunteer expense: 0.002% of current Greek GDP while Greek divisions serve in Cyprus.",
    })
    for key, (tag, values) in IDEAS.items():
        name = "COLDWAR_CYP_R2_" + key
        loc[name] = {
            "greek_officers": "Greek Officers on Cyprus",
            "greek_treaty": "Greek Guarantor Commitment",
            "greek_network": "Greek Officer Network",
            "greek_withdrawal": "Greek Network Withdrawn",
            "turkish_terms": "Accepted Communal Guarantees",
            "angry_general_staff": "Angry General Staff",
            "command_reorganization": "Command Reorganization",
            "cyprus_intervention_forces": "Cyprus Intervention Forces",
            "cyprus_volunteer_mission": "Cyprus Volunteer Mission",
            "english_mediation": "Joint British Mediation",
            "english_restraint": "British Restraint",
        }[key]
        loc[name + "_desc"] = {
            "greek_officers": "Army organization +2%. Unit training time -5%.",
            "greek_treaty": "Foreign influence defence +5%. Stability +2%.",
            "greek_network": "Stability -2%.",
            "greek_withdrawal": "Stability +3%.",
            "turkish_terms": "Stability +3%. Army attack -2%.",
            "angry_general_staff": "Stability -10%. Army organization -10%. Political power gain -15%.",
            "command_reorganization": "Army organization -5%. Political power gain -5%.",
            "cyprus_intervention_forces": "Navy organization +15%. Naval invasion preparation speed +50%. Amphibious invasion attack +15%. Planning speed +30%. Maximum planning +20%.",
            "cyprus_volunteer_mission": "Volunteer limit +2. Minimum army-size requirement -100%. World-tension requirement -100%. Political power gain -5%.",
            "english_mediation": "Bureaucracy cost +1%.",
            "english_restraint": "Bureaucracy cost -1%. Foreign influence defence -3%.",
        }[key]
    # The event text and modifier preview labels are exact English game loc; parent merges this mapping into l_english.
    for d in design.get("crisis_decisions", []):
        loc["COLDWAR_CYP_R2_army_" + d["key"]] = d["title"]
    loc["COLDWAR_CYP_R2_turkish_army_crisis"] = "Army Crisis"
    return loc


def build(design: dict) -> dict:
    """Return generated runtime content and loc/meta for the Cyprus R2 compiler."""
    data = deepcopy(design)
    keys = {a["key"] for a in data.get("actor_focuses", [])}
    if keys != set(ACTORS):
        raise ValueError(f"actor_focuses mismatch: missing={sorted(set(ACTORS)-keys)}, extra={sorted(keys-set(ACTORS))}")
    files = {
        "common/scripted_effects/COLDWAR_CYP_R2_crisis.txt": _effect_file(),
        "common/scripted_triggers/COLDWAR_CYP_R2_crisis.txt": _trigger_file(),
        "common/ideas/COLDWAR_CYP_R2_crisis_ideas.txt": _ideas_file(),
        "events/COLDWAR_CYP_R2_crisis.txt": _events_file(),
    }
    files.update(_decision_files())
    return {
        "files": files,
        "loc": _loc(data),
        "meta": {
            "project": "IMPERIA COLD WAR",
            "namespace": NS,
            "event_picture_sprite": "GFX_COLDWAR_CYP_R2_agreement",
            "actor_focus_keys": sorted(ACTORS),
            "actor_helpers": {
                key: {"apply": f"COLDWAR_CYP_R2_ACT_{key}_apply", "preview": f"COLDWAR_CYP_R2_ACT_{key}_preview",
                      "available": f"COLDWAR_CYP_R2_ACT_{key}_available"}
                for key in ACTORS
            },
            "additional_effects": ["COLDWAR_CYP_R2_convene_guarantors", "COLDWAR_CYP_R2_geneva_conference",
                "COLDWAR_CYP_R2_crisis_monthly", "COLDWAR_CYP_R2_crisis_reconcile", "COLDWAR_CYP_R2_crisis_weekly_streams",
                "COLDWAR_CYP_R2_nato_join_allowed"],
            "weekly_money_hook": "Add COLDWAR_CYP_R2_crisis_weekly_streams = yes to each country's weekly expense calculation, then add COLDWAR_CYP_R2_crisis_weekly_expenses exactly once to additional_expenses_rate.",
            "budget_cache_initialization": "Call COLDWAR_CYP_R2_crisis_monthly = yes once after CYP initialization so GRE/TUR percent-of-GDP affordability checks are initialized before their first focus access.",
            "monthly_hook": "Call COLDWAR_CYP_R2_crisis_monthly = yes once in CYP scope from an existing monthly fixed-tag fallback.",
            "transition_hook": "Call COLDWAR_CYP_R2_crisis_reconcile = yes in CYP scope from existing war-start/peace/settlement transition hooks.",
            "annex_fallback_hook": "When CYP no longer exists, call COLDWAR_CYP_R2_crisis_reconcile = yes from USA monthly fallback scope so foreign intervention expense and prior NATO membership receipts can be reconciled.",
            "unverified_native_volunteers": "The module grants MD volunteer modifier spirit only. The player must use native diplomacy; engine-side enemy-of-ally constraints remain unverified.",
        },
    }
