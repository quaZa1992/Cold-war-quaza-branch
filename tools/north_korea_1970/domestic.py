# IMPERIA CW — Cold War: North Korea 1970 domestic adapters.
"""Emit the approved NKO 1970 domestic decision and account support."""

from __future__ import annotations

import json


P = "COLDWAR_NKO_"
HEADER = "# IMPERIA CW — Cold War: North Korea 1970 domestic adapters.\n"


def build(ROOT, D, put):
    """Generate country-scoped adapters; formatting/encoding is owned by put()."""
    LOC: dict[str, str] = {}
    loan_share=next(e['principal_gdp_share'] for n in D['nodes'] for e in n['extra'] if e['kind']=='debt')
    finance=next(i for i in D['incidents'] if i['id']=='COLDWAR_NKO_machinery_account')
    reschedule_share=next(c['cost_gdp_share'] for c in finance['choices'] if c['name']=='Reschedule the Account')
    mitigation_share=next(i['mitigation_cost_gdp_share'] for i in D['incidents'] if i['id']=='COLDWAR_NKO_patron_disruption')
    from script_ast import parse,first,emit
    focus_rows=first(parse((ROOT/'common/national_focus/COLDWAR_NKO_1970_focus.txt').read_text(encoding='utf-8')),'focus_tree')
    previews={first(v,'id'):emit(first(first(v,'completion_reward'),'effect_tooltip')) for k,_,v in focus_rows if k=='focus'}

    def L(key: str, value: str) -> str:
        if key in LOC and LOC[key] != value:
            raise ValueError("Conflicting domestic localization: " + key)
        LOC[key] = value
        return key

    effects: list[str] = []
    triggers: list[str] = []
    decisions: list[str] = []
    events: list[str] = []

    # Daily adapter centralizes the independent country generators and repairs
    # the outstanding-credit receipt before the core modifier reconciliation.
    effects.append(f"""COLDWAR_NKO_daily = {{
	if = {{
		limit = {{ original_tag = NKO IMP_is_1970_scenario = yes }}
		if = {{ limit = {{ NOT = {{ has_country_flag = COLDWAR_NKO_initialized }} }} COLDWAR_NKO_initialize = yes }}
		COLDWAR_NKO_succession_daily = yes
		COLDWAR_NKO_foreign_refresh = yes
		if = {{
			limit = {{ has_country_flag = COLDWAR_NKO_machinery_account_open check_variable = {{ debt = 0 }} }}
			set_variable = {{ COLDWAR_NKO_machinery_principal = 0 }}
			clr_country_flag = COLDWAR_NKO_machinery_account_open
			clr_country_flag = COLDWAR_NKO_machinery_review_available
			clr_country_flag = COLDWAR_NKO_machinery_review_pending
			clr_country_flag = COLDWAR_NKO_machinery_due_clock
			if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_credit_rescheduled }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_credit_rescheduled }} }}
			if = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_NKO_credit_default }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_NKO_credit_default }} }}
		}}
		if = {{
			limit = {{ has_country_flag = COLDWAR_NKO_machinery_account_open NOT = {{ has_country_flag = COLDWAR_NKO_machinery_due_clock }} NOT = {{ has_country_flag = COLDWAR_NKO_machinery_review_available }} }}
			set_country_flag = COLDWAR_NKO_machinery_review_available
			COLDWAR_NKO_review_machinery_account = yes
		}}
		COLDWAR_NKO_refresh_programmes = yes
	}}
}}""")

    effects.append("""COLDWAR_NKO_open_machinery_credit = {
	if = {
		limit = {
			original_tag = NKO
			IMP_is_1970_scenario = yes
			NOT = { has_country_flag = COLDWAR_NKO_machinery_credit_opened }
			check_variable = { gdp_total > 0 }
	}
	set_temp_variable = { COLDWAR_NKO_credit_amount = gdp_total }
	multiply_temp_variable = { COLDWAR_NKO_credit_amount = 0.015 }
	set_variable = { COLDWAR_NKO_machinery_principal = COLDWAR_NKO_credit_amount }
	set_temp_variable = { debt_change = COLDWAR_NKO_credit_amount }
	modify_debt_effect = yes
	set_temp_variable = { treasury_change = COLDWAR_NKO_credit_amount }
	modify_treasury_effect = yes
	set_temp_variable = { treasury_change = COLDWAR_NKO_credit_amount }
	multiply_temp_variable = { treasury_change = -1 }
	modify_treasury_effect = yes
	set_country_flag = COLDWAR_NKO_machinery_credit_opened
	set_country_flag = COLDWAR_NKO_machinery_account_open
	set_country_flag = { flag = COLDWAR_NKO_machinery_due_clock value = 1 days = 730 }
}
}""")

    effects.append("""COLDWAR_NKO_review_machinery_account = {
	if = {
		limit = {
			original_tag = NKO
			IMP_is_1970_scenario = yes
			has_country_flag = COLDWAR_NKO_machinery_account_open
			NOT = { has_country_flag = COLDWAR_NKO_machinery_review_pending }
			check_variable = { COLDWAR_NKO_machinery_principal > 0 }
		}
		set_country_flag = COLDWAR_NKO_machinery_review_pending
		country_event = { id = COLDWAR_NKO_domestic.1 }
	}
}""")

    # This is the existing Imperia permanent investment-target API. It only
    # grants access for already-active accepted industrial agreements; regular
    # investment proposals and their acceptance/financing remain native.
    partners = [
        ("SOV", "soviet_industry", "Soviet Union"),
        ("DDR", "gdr_machinery", "East Germany"),
        ("ROM", "romanian_exchange", "Romania"),
        ("BUL", "bulgarian_engineering", "Bulgaria"),
    ]
    for tag, agreement, display in partners:
        receipt = f"COLDWAR_NKO_joint_venture_access_{tag}"
        effect_id = f"COLDWAR_NKO_authorize_investment_access_{tag}"
        trigger_id = f"COLDWAR_NKO_can_authorize_investment_access_{tag}"
        triggers.append(f"""{trigger_id} = {{
	original_tag = NKO
	IMP_is_1970_scenario = yes
	has_country_flag = COLDWAR_NKO_joint_ventures_open
	{P}{agreement}_active = yes
	{tag} = {{ exists = yes }}
	NOT = {{ has_country_flag = {receipt} }}
}}""")
        effects.append(f"""{effect_id} = {{
	if = {{
		limit = {{ {trigger_id} = yes }}
		set_temp_variable = {{ target_nation = {tag}.id }}
		set_temp_variable = {{ adding_nation = NKO.id }}
		change_permanent_investment_target = yes
		set_country_flag = {receipt}
		COLDWAR_NKO_foreign_refresh = yes
	}}
}}""")
        decision_id = f"COLDWAR_NKO_domestic_authorize_investment_access_{tag}"
        title = L(decision_id, f"Authorize Joint-Venture Access with {display}")
        desc = L(decision_id + "_desc", "Open the DPRK to investment proposals under the active industrial cooperation agreement. Foreign governments may submit financed projects for our approval.")
        decisions.append(f"""{decision_id} = {{
	icon = GFX_decision_obtain_foreign_investment
	cost = 0
	visible = {{ has_country_flag = COLDWAR_NKO_joint_ventures_open NOT = {{ has_country_flag = {receipt} }} }}
	available = {{ {trigger_id} = yes }}
	complete_effect = {{ {effect_id} = yes }}
	ai_will_do = {{ factor = 0 }}
}}""")

    # Advance funding executes the same guarded completion effect as the focus.
    # The focus itself must still be completed later to open its descendants.
    nodes = {n["key"]: n for n in D["nodes"]}
    project_rows = []
    for node in D["nodes"]:
        buildings = [e for e in node.get("extra", []) if e.get("kind") == "building"]
        if not buildings:
            continue
        key = node["key"]
        focus = node["id"]
        receipt = focus + "_earned"
        prereq = []
        for group in node.get("prerequisites", []):
            prereq.append("OR = { " + " ".join("has_completed_focus = " + x for x in group) + " }")
        guards = [f"COLDWAR_NKO_can_{key} = yes", f"NOT = {{ has_completed_focus = {focus} }}", f"NOT = {{ has_country_flag = {receipt} }}"]
        guards.extend(prereq)
        triggers.append(f"COLDWAR_NKO_can_advance_{key} = {{ {' '.join(guards)} }}")
        building = buildings[0]
        building_label = {
            "industrial_complex": "civilian factory",
            "arms_factory": "military factory",
            "dockyard": "naval dockyard",
            "infrastructure": "infrastructure level",
            "radar_station": "radar station",
            "fossil_powerplant": "coal-fired power plant",
            "renewable_energy_infra": "hydropower installation",
            "agriculture_district": "agricultural district",
        }.get(building["type"], building["type"].replace("_", " "))
        project_rows.append((key, node, building, building_label, " ".join(guards)))
    for key, node, building, building_label, guards in project_rows:
        decision_id = f"COLDWAR_NKO_domestic_advance_{key}"
        L(decision_id, "Advance " + node["title"])
        share = float(node.get("cost_gdp_share", 0))
        lines = [
            f"Authorize advance funding for the {building_label} project under the national investment programme.",
        ]
        L(decision_id + "_desc", "\n".join(lines))
        decisions.append(f"""{decision_id} = {{
	icon = GFX_decision_industry
	cost = 0
	visible = {{ has_country_flag = COLDWAR_NKO_planning_decisions_open NOT = {{ has_country_flag = {node['id']}_earned }} }}
	available = {{ custom_trigger_tooltip = {{ tooltip = COLDWAR_NKO_domestic_project_ready_tt COLDWAR_NKO_can_advance_{key} = yes }} }}
	complete_effect = {{ effect_tooltip = {{ {previews[node['id']]} }} hidden_effect = {{ COLDWAR_NKO_complete_{key} = yes }} }}
	ai_will_do = {{ factor = 0 }}
}}""")

    account_decision = "COLDWAR_NKO_domestic_review_machinery_account"
    triggers.append("""COLDWAR_NKO_machinery_review_due = {
	has_country_flag = COLDWAR_NKO_machinery_account_open
	has_country_flag = COLDWAR_NKO_machinery_review_available
	NOT = { has_country_flag = COLDWAR_NKO_machinery_review_pending }
	check_variable = { COLDWAR_NKO_machinery_principal > 0 }
}""")
    L(account_decision, "Review the Machinery Account")
    L(account_decision + "_desc", "The account is due for review. Settle recorded principal, reschedule the account for two years, or suspend payments for two years.")
    decisions.append(f"""{account_decision} = {{
	icon = GFX_decision_economy
	cost = 0
	visible = {{ COLDWAR_NKO_machinery_review_due = yes }}
	available = {{ COLDWAR_NKO_machinery_review_due = yes }}
	complete_effect = {{ COLDWAR_NKO_review_machinery_account = yes }}
	ai_will_do = {{ factor = 0 }}
}}""")

    handover_decision = "COLDWAR_NKO_domestic_deliberate_civilian_handover"
    L(handover_decision, "Convene the Civilian Handover Deliberation")
    L(handover_decision + "_desc", "Convene negotiations on the transfer of authority to a civilian government.")
    decisions.append(f"""{handover_decision} = {{
	icon = GFX_decision_politics
	cost = 0
	visible = {{ has_country_flag = COLDWAR_NKO_civilian_negotiations_open }}
	available = {{ check_variable = {{ ruling_party = 22 }} NOT = {{ has_country_flag = COLDWAR_NKO_civilian_negotiation_resolved }} }}
	complete_effect = {{ country_event = {{ id = COLDWAR_NKO_domestic.2 }} }}
	ai_will_do = {{ factor = 0 }}
}}""")

    events.extend(["""add_namespace = COLDWAR_NKO_domestic

# The prompt is opened once by an NKO decision after the account reaches its due date.
country_event = {
	id = COLDWAR_NKO_domestic.1
	title = COLDWAR_NKO_domestic.1.t
	desc = COLDWAR_NKO_domestic.1.d
	trigger = { original_tag = NKO IMP_is_1970_scenario = yes has_country_flag = COLDWAR_NKO_machinery_review_pending }
	is_triggered_only = yes

	option = {
		name = COLDWAR_NKO_domestic.1.a
		trigger = { original_tag = NKO has_country_flag = COLDWAR_NKO_machinery_account_open }
		custom_effect_tooltip = COLDWAR_NKO_domestic.1.a_tt
		hidden_effect = { COLDWAR_NKO_settle_machinery_account = yes }
	}
	option = {
		name = COLDWAR_NKO_domestic.1.b
		trigger = { original_tag = NKO has_country_flag = COLDWAR_NKO_machinery_account_open check_variable = { gdp_total > 0 } }
		effect_tooltip = {
			set_temp_variable = { treasury_change = gdp_total }
			multiply_temp_variable = { treasury_change = -0.002 }
			modify_treasury_effect = yes
			add_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled days = 730 }
		}
		hidden_effect = { COLDWAR_NKO_reschedule_machinery_account = yes }
	}
	option = {
		name = COLDWAR_NKO_domestic.1.c
		trigger = { original_tag = NKO has_country_flag = COLDWAR_NKO_machinery_account_open }
		effect_tooltip = { add_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default days = 730 } }
		hidden_effect = { COLDWAR_NKO_suspend_machinery_repayments = yes }
	}
	option = {
		name = COLDWAR_NKO_domestic.1.option_d
		trigger = { NOT = { has_country_flag = COLDWAR_NKO_machinery_account_open } }
		hidden_effect = { clr_country_flag = COLDWAR_NKO_machinery_review_pending }
	}
}""",
"""country_event = {
	id = COLDWAR_NKO_domestic.2
	title = COLDWAR_NKO_domestic.2.t
	desc = COLDWAR_NKO_domestic.2.d
	trigger = { original_tag = NKO IMP_is_1970_scenario = yes has_country_flag = COLDWAR_NKO_civilian_negotiations_open check_variable = { ruling_party = 22 } }
	is_triggered_only = yes

	option = {
		name = COLDWAR_NKO_domestic.2.a
		trigger = { check_variable = { ruling_party = 22 } }
		set_temp_variable = { rul_party_temp = 5 }
		set_temp_variable = { change_leader_temp = 1 }
		set_temp_variable = { disable_elections = 1 }
		change_ruling_party_effect = yes
		set_country_flag = COLDWAR_NKO_civilian_negotiation_resolved
		COLDWAR_NKO_refresh_programmes = yes
	}
	option = {
		name = COLDWAR_NKO_domestic.2.b
		trigger = { check_variable = { ruling_party = 22 } }
		set_temp_variable = { rul_party_temp = 13 }
		set_temp_variable = { change_leader_temp = 1 }
		set_temp_variable = { disable_elections = 1 }
		change_ruling_party_effect = yes
		set_country_flag = COLDWAR_NKO_civilian_negotiation_resolved
		COLDWAR_NKO_refresh_programmes = yes
	}
	option = {
		name = COLDWAR_NKO_domestic.2.c
		trigger = { check_variable = { ruling_party = 22 } }
		set_country_flag = COLDWAR_NKO_civilian_negotiation_resolved
	}
}"""])

    effects.append("""COLDWAR_NKO_settle_machinery_account = {
	if = {
		limit = { has_country_flag = COLDWAR_NKO_machinery_review_pending has_country_flag = COLDWAR_NKO_machinery_account_open }
		set_temp_variable = { debt_change = COLDWAR_NKO_machinery_principal }
		if = { limit = { check_variable = { debt < debt_change } } set_temp_variable = { debt_change = debt } }
		set_temp_variable = { treasury_change = debt_change }
		multiply_temp_variable = { treasury_change = -1 }
		multiply_temp_variable = { debt_change = -1 }
		modify_treasury_effect = yes
		modify_debt_effect = yes
		if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled } } remove_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled } }
		if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default } } remove_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default } }
		set_variable = { COLDWAR_NKO_machinery_principal = 0 }
		clr_country_flag = COLDWAR_NKO_machinery_account_open
		clr_country_flag = COLDWAR_NKO_machinery_review_available
		clr_country_flag = COLDWAR_NKO_machinery_review_pending
		clr_country_flag = COLDWAR_NKO_machinery_due_clock
		COLDWAR_NKO_refresh_programmes = yes
	}
}""")

    effects.append("""COLDWAR_NKO_reschedule_machinery_account = {
	if = {
		limit = { has_country_flag = COLDWAR_NKO_machinery_review_pending has_country_flag = COLDWAR_NKO_machinery_account_open check_variable = { gdp_total > 0 } }
		set_temp_variable = { treasury_change = gdp_total }
		multiply_temp_variable = { treasury_change = -0.002 }
		modify_treasury_effect = yes
		if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default } } remove_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default } }
		add_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled days = 730 }
		set_country_flag = { flag = COLDWAR_NKO_machinery_due_clock value = 1 days = 730 }
		clr_country_flag = COLDWAR_NKO_machinery_review_available
		clr_country_flag = COLDWAR_NKO_machinery_review_pending
	}
}""")

    effects.append("""COLDWAR_NKO_suspend_machinery_repayments = {
	if = {
		limit = { has_country_flag = COLDWAR_NKO_machinery_review_pending has_country_flag = COLDWAR_NKO_machinery_account_open }
		if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled } } remove_dynamic_modifier = { modifier = COLDWAR_NKO_credit_rescheduled } }
		add_dynamic_modifier = { modifier = COLDWAR_NKO_credit_default days = 730 }
		set_country_flag = { flag = COLDWAR_NKO_machinery_due_clock value = 1 days = 730 }
		clr_country_flag = COLDWAR_NKO_machinery_review_available
		clr_country_flag = COLDWAR_NKO_machinery_review_pending
	}
}""")

    # Explicit withdrawal ends the reciprocal safeguarded upgrade at both ends.
    effects.append('''COLDWAR_NKO_withdraw_safeguards = {
      if = { limit = { tag = NKO IMP_is_1970_scenario = yes has_country_flag = COLDWAR_NKO_safeguards_valid }
        clr_country_flag = COLDWAR_NKO_safeguards_valid
        COLDWAR_NKO_foreign_refresh = yes
        COLDWAR_NKO_refresh_programmes = yes
      }
    }''')
    decisions.append('''COLDWAR_NKO_domestic_withdraw_safeguards = {
      icon = GFX_decision_relation cost = 0
      visible = { has_country_flag = COLDWAR_NKO_safeguards_valid }
      complete_effect = {
        custom_effect_tooltip = COLDWAR_NKO_withdraw_safeguards_tt
        effect_tooltip = { remove_dynamic_modifier = { modifier = COLDWAR_NKO_safeguards_programme } }
        hidden_effect = { COLDWAR_NKO_withdraw_safeguards = yes }
      }
      ai_will_do = { factor = 0 }
    }''')
    L('COLDWAR_NKO_domestic_withdraw_safeguards','Withdraw the Safeguards Commitment')
    L('COLDWAR_NKO_domestic_withdraw_safeguards_desc','Withdraw the inspection commitment and relinquish cooperation tied to international safeguards.')
    L('COLDWAR_NKO_withdraw_safeguards_tt','End safeguarded cooperation for both signatories. The original civilian nuclear agreement remains subject to peaceful relations and the absence of bilateral sanctions.')

    effects.append('''COLDWAR_NKO_mitigate_patron_disruption = {
      if = { limit = { tag = NKO IMP_is_1970_scenario = yes check_variable = { gdp_total > 0 } has_dynamic_modifier = { modifier = COLDWAR_NKO_patron_disruption } }
        set_temp_variable = { treasury_change = gdp_total }
        multiply_temp_variable = { treasury_change = -0.004 }
        modify_treasury_effect = yes
        remove_dynamic_modifier = { modifier = COLDWAR_NKO_patron_disruption }
      }
    }''')
    decisions.append('''COLDWAR_NKO_domestic_mitigate_patron_disruption = {
      icon = GFX_decision_industry cost = 0
      visible = { has_dynamic_modifier = { modifier = COLDWAR_NKO_patron_disruption } }
      available = { hidden_trigger = { check_variable = { gdp_total > 0 } } }
      complete_effect = {
        effect_tooltip = {
          set_temp_variable = { treasury_change = gdp_total }
          multiply_temp_variable = { treasury_change = -0.004 }
          modify_treasury_effect = yes
          remove_dynamic_modifier = { modifier = COLDWAR_NKO_patron_disruption }
        }
        hidden_effect = { COLDWAR_NKO_mitigate_patron_disruption = yes }
      }
      ai_will_do = { factor = 0 }
    }''')
    L('COLDWAR_NKO_domestic_mitigate_patron_disruption','Secure Replacement Industrial Supplies')
    L('COLDWAR_NKO_domestic_mitigate_patron_disruption_desc','Emergency purchases and industrial adjustments can relieve the disruption of external support.')

    # Category and loc names are deliberately English-only. Numeric terms match
    # the existing approved finance ratios and recurring costs are absent.
    category_visible = "OR = { has_country_flag = COLDWAR_NKO_safeguards_valid has_dynamic_modifier = { modifier = COLDWAR_NKO_patron_disruption } has_country_flag = COLDWAR_NKO_planning_decisions_open has_country_flag = COLDWAR_NKO_joint_ventures_open has_country_flag = COLDWAR_NKO_machinery_review_available AND = { has_country_flag = COLDWAR_NKO_civilian_negotiations_open check_variable = { ruling_party = 22 } } }"
    category = f"""COLDWAR_NKO_1970_domestic = {{
	icon = investment
	allowed = {{ tag = NKO original_tag = NKO IMP_is_1970_scenario = yes }}
	visible = {{ {category_visible} }}
	priority = 130
}}"""

    L("COLDWAR_NKO_domestic.1.t", "Review the Machinery Account")
    L("COLDWAR_NKO_domestic.1.d", "The machinery account has reached its review date. The recorded principal can be settled against outstanding debt, rescheduled on a two-year basis, or left unpaid for two years.")
    L("COLDWAR_NKO_domestic.1.a", "Settle the recorded principal")
    L("COLDWAR_NKO_domestic.1.b", "Reschedule repayments")
    L("COLDWAR_NKO_domestic.1.c", "Suspend repayments")
    L("COLDWAR_NKO_domestic.1.option_d", "The account is settled.")
    L('COLDWAR_NKO_domestic_project_ready_tt','The project is authorized, remains unfunded and has a suitable state.')
    L('COLDWAR_NKO_domestic_project_ready_tt_NOT','The project requires authorization, an unfunded account and suitable construction capacity.')
    L('COLDWAR_NKO_1970_domestic','National Investment Programme')
    L('COLDWAR_NKO_1970_domestic_desc','Fund national projects, review external accounts and manage institutional commitments.')
    L("COLDWAR_NKO_domestic.1.a_tt", "Repay up to §R$[?THIS.COLDWAR_NKO_machinery_principal|2] billion§! and remove the same amount of debt, capped at outstanding debt.")
    L("COLDWAR_NKO_domestic.2.t", "A Civilian Handover Deliberation")
    L("COLDWAR_NKO_domestic.2.d", "The emergency council has opened negotiations on a civilian transition. The current military government remains in office unless a civilian arrangement is selected.")
    L("COLDWAR_NKO_domestic.2.a", "Transfer authority to the Democratic Front")
    L("COLDWAR_NKO_domestic.2.b", "Establish a cabinet-led transition")
    L("COLDWAR_NKO_domestic.2.c", "Keep the emergency council in office")

    loc_text = "l_english:\n" + HEADER
    for key, value in LOC.items():
        loc_text += f" {key}:0 {json.dumps(value, ensure_ascii=False)}\n"

    def prices(text):
        return text.replace('COLDWAR_NKO_credit_amount = 0.015',f'COLDWAR_NKO_credit_amount = {loan_share:.5f}').replace('treasury_change = -0.002',f'treasury_change = -{reschedule_share:.5f}').replace('treasury_change = -0.004',f'treasury_change = -{mitigation_share:.5f}')
    put("common/scripted_effects/COLDWAR_NKO_1970_domestic_effects.txt", prices("\n".join(effects)))
    put("common/scripted_triggers/COLDWAR_NKO_1970_domestic_triggers.txt", "\n".join(triggers))
    put("common/decisions/COLDWAR_NKO_1970_domestic_decisions.txt", prices("COLDWAR_NKO_1970_domestic = {\n" + "\n".join(decisions) + "\n}"))
    put("common/decisions/categories/COLDWAR_NKO_1970_domestic_categories.txt", category)
    put("events/COLDWAR_NKO_1970_domestic_events.txt", prices("\n".join(events)))
    put("localisation/english/COLDWAR_NKO_1970_domestic_l_english.yml", loc_text, True)
