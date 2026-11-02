# IMPERIA COLD WAR — Approved Cuba 1970 diplomatic agreements compiler.
"""Emit diplomacy-owned runtime files from the frozen approved design.

This is deliberately separate from the focus/idea compiler: the agreements
have recipient-owned decisions and atomic transaction guards.
"""
from pathlib import Path
import json
import sys
from file_headers import stamp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from building_capacity_audit.irq_cub import cub_radar_queries
DESIGN = json.loads((Path(__file__).parent / "approved_design.json").read_text(encoding="utf-8"))
EXPECTED = {
    "soviet_assistance", "cmea_admission", "air_defence", "medical_mission",
    "overseas_mission", "us_normalisation", "ddr_commission",
    "symbolic_island_cooperation", "island_cession",
}
assert set(DESIGN["contracts"]) == EXPECTED

EFFECTS = r'''# IMPERIA COLD WAR — Cuba 1970 diplomatic contracts.
# Recipient-owned offers, acceptance-time validation, and once-only rewards.

# Fixed-recipient offers are opened from a CUB-scoped national-focus reward.
# Matching flags on sender and recipient expire after 90 days; no payment is made at proposal.
COLDWAR_CUB_offer_soviet_assistance = {
	if = {
		limit = { country_exists = SOV NOT = { has_country_flag = COLDWAR_CUB_soviet_offer_open } NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } SOV = { NOT = { has_country_flag = COLDWAR_CUB_soviet_offer_pending } NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } NOT = { has_war_with = CUB } } NOT = { has_war_with = SOV } }
		set_country_flag = { flag = COLDWAR_CUB_soviet_offer_open value = 1 days = 90 }
		SOV = { set_country_flag = { flag = COLDWAR_CUB_soviet_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.1 } }
	}
}

# Metadata-only bilateral fuel undertaking. The recorded baseline observes current native imports;
# this agreement does not create imports, alter trade routes, or pay either treasury.
COLDWAR_CUB_offer_soviet_fuel_commitment = {
	if = {
		limit = { country_exists = SOV check_variable = { resource_imported@oil > 0 } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_offer_open } SOV = { NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = SOV } }
		set_country_flag = { flag = COLDWAR_CUB_soviet_fuel_offer_open value = 1 days = 90 }
		SOV = { set_country_flag = { flag = COLDWAR_CUB_soviet_fuel_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.10 } }
	}
}

COLDWAR_CUB_offer_cmea_admission = {
	if = {
		limit = { country_exists = SOV NOT = { has_idea = COLDWAR_CUB_cmea_member } NOT = { has_country_flag = COLDWAR_CUB_cmea_offer_open } SOV = { NOT = { has_country_flag = COLDWAR_CUB_cmea_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = SOV } }
		set_country_flag = { flag = COLDWAR_CUB_cmea_offer_open value = 1 days = 90 }
		SOV = { set_country_flag = { flag = COLDWAR_CUB_cmea_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.2 } }
	}
}

COLDWAR_CUB_offer_air_defence = {
	if = {
		limit = { country_exists = SOV NOT = { has_country_flag = COLDWAR_CUB_air_defence_receipt } NOT = { has_country_flag = COLDWAR_CUB_air_offer_open } SOV = { NOT = { has_country_flag = COLDWAR_CUB_air_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = SOV } owns_state = 854 controls_state = 854 854 = { free_building_slots = { building = radar_station size > 0 include_locked = no } } }
		set_country_flag = { flag = COLDWAR_CUB_air_offer_open value = 1 days = 90 }
		SOV = { set_country_flag = { flag = COLDWAR_CUB_air_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.3 } }
	}
}

# Focus enables recipient selection; the actual recipient-specific offer is opened by a targeted decision.
COLDWAR_CUB_offer_medical_mission = {
	if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_medical_offer_open } NOT = { has_country_flag = COLDWAR_CUB_medical_refused } }
		set_country_flag = COLDWAR_CUB_medical_targeting_enabled
	}
}

COLDWAR_CUB_offer_overseas_mission = {
	if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_overseas_offer_open } NOT = { has_country_flag = COLDWAR_CUB_overseas_refused } }
		set_country_flag = COLDWAR_CUB_overseas_targeting_enabled
	}
}

# History events can open a recipient-owned offer to the named wartime partner only.
COLDWAR_CUB_offer_overseas_mission_to_angola = {
	if = {
		limit = { country_exists = AGL NOT = { has_country_flag = COLDWAR_CUB_overseas_offer_open } AGL = { COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } }
		set_country_flag = { flag = COLDWAR_CUB_overseas_offer_open value = 1 days = 90 }
		AGL = { set_country_flag = { flag = COLDWAR_CUB_overseas_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.5 } }
	}
}
COLDWAR_CUB_offer_overseas_mission_to_ethiopia = {
	if = {
		limit = { country_exists = ETH NOT = { has_country_flag = COLDWAR_CUB_overseas_offer_open } ETH = { COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } }
		set_country_flag = { flag = COLDWAR_CUB_overseas_offer_open value = 1 days = 90 }
		ETH = { set_country_flag = { flag = COLDWAR_CUB_overseas_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.5 } }
	}
}

COLDWAR_CUB_offer_us_normalisation = {
	if = {
		limit = { country_exists = USA NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } NOT = { has_country_flag = COLDWAR_CUB_us_offer_open } USA = { NOT = { has_country_flag = COLDWAR_CUB_us_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = USA } }
		set_country_flag = { flag = COLDWAR_CUB_us_offer_open value = 1 days = 90 }
		USA = { set_country_flag = { flag = COLDWAR_CUB_us_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.6 } }
	}
}

COLDWAR_CUB_offer_ddr_commission = {
	if = {
		limit = { country_exists = DDR NOT = { has_country_flag = COLDWAR_CUB_ddr_commission_receipt } NOT = { has_country_flag = COLDWAR_CUB_ddr_offer_open } DDR = { NOT = { has_country_flag = COLDWAR_CUB_ddr_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = DDR } }
		set_country_flag = { flag = COLDWAR_CUB_ddr_offer_open value = 1 days = 90 }
		DDR = { set_country_flag = { flag = COLDWAR_CUB_ddr_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.7 } }
	}
}

COLDWAR_CUB_offer_symbolic_island_cooperation = {
	if = {
		limit = { country_exists = DDR has_completed_focus = COLDWAR_CUB_thaelmann_name owns_state = 1252 controls_state = 1252 COLDWAR_CUB_pair_ddr_clear = yes NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } NOT = { has_country_flag = COLDWAR_CUB_symbolic_offer_open } DDR = { NOT = { has_country_flag = COLDWAR_CUB_symbolic_offer_pending } NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } NOT = { has_war_with = CUB } } NOT = { has_war_with = DDR } }
		set_country_flag = { flag = COLDWAR_CUB_symbolic_offer_open value = 1 days = 90 }
		DDR = { set_country_flag = { flag = COLDWAR_CUB_symbolic_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.8 } }
	}
}

COLDWAR_CUB_offer_island_cession = {
	if = {
		limit = { date > 1972.6.18 country_exists = DDR owns_state = 1252 controls_state = 1252 NOT = { has_completed_focus = COLDWAR_CUB_thaelmann_name } NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } NOT = { has_country_flag = COLDWAR_CUB_cession_offer_open } DDR = { NOT = { has_country_flag = COLDWAR_CUB_cession_offer_pending } NOT = { has_war_with = CUB } } NOT = { has_war_with = DDR } }
		set_country_flag = { flag = COLDWAR_CUB_cession_offer_open value = 1 days = 90 }
		DDR = { set_country_flag = { flag = COLDWAR_CUB_cession_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.9 } }
	}
}

# Called by CUB's diplomacy daily reconciliation. COLDWAR_CUB_american_embargo is a fallback;
# the native and Imperia trade restrictions take precedence at start and after partial easing.
COLDWAR_CUB_sync_embargo = {
	if = {
		limit = { COLDWAR_CUB_us_trade_restriction_active = yes }
		if = { limit = { has_idea = COLDWAR_CUB_american_embargo } remove_ideas = COLDWAR_CUB_american_embargo }
		if = { limit = { has_idea = COLDWAR_CUB_american_embargo_limited } remove_ideas = COLDWAR_CUB_american_embargo_limited }
	}
	else_if = {
		limit = { has_country_flag = COLDWAR_CUB_us_easing_limited NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } }
		if = { limit = { has_idea = COLDWAR_CUB_american_embargo } remove_ideas = COLDWAR_CUB_american_embargo }
		if = { limit = { NOT = { has_idea = COLDWAR_CUB_american_embargo_limited } } add_ideas = COLDWAR_CUB_american_embargo_limited }
	}
	else = {
		if = { limit = { has_idea = COLDWAR_CUB_american_embargo_limited } remove_ideas = COLDWAR_CUB_american_embargo_limited }
		if = { limit = { has_idea = COLDWAR_CUB_american_embargo } remove_ideas = COLDWAR_CUB_american_embargo }
		if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } NOT = { has_idea = COLDWAR_CUB_american_embargo } } add_ideas = COLDWAR_CUB_american_embargo }
	}
}

# IMPERIA COLD WAR — reconcile accepted bilateral agreements each day.
COLDWAR_CUB_diplomacy_daily = {
	COLDWAR_CUB_sync_embargo = yes
	COLDWAR_CUB_sync_soviet_fuel_commitment = yes
	COLDWAR_CUB_refresh_overseas_aggregate = yes
	COLDWAR_CUB_reconcile_bilateral = yes
}

# A shortage is verified only after a signed Soviet undertaking is withdrawn (or SOV ceases
# to exist) and Cuban aggregate oil imports fall below 80% of the recorded nonzero baseline.
COLDWAR_CUB_sync_soviet_fuel_commitment = {
	if = {
		limit = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active OR = { NOT = { country_exists = SOV } SOV = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn } } check_variable = { COLDWAR_CUB_soviet_oil_import_baseline > 0 } }
		set_temp_variable = { COLDWAR_CUB_oil_import_recovery_threshold = COLDWAR_CUB_soviet_oil_import_baseline }
		multiply_temp_variable = { COLDWAR_CUB_oil_import_recovery_threshold = 0.8 }
		if = {
			limit = { has_country_flag = COLDWAR_CUB_verified_supply_shortage NOT = { check_variable = { resource_imported@oil < COLDWAR_CUB_oil_import_recovery_threshold } } }
			clr_country_flag = COLDWAR_CUB_verified_supply_shortage
			COLDWAR_CUB_refresh_dependency = yes
		}
		else_if = {
			limit = { NOT = { has_country_flag = COLDWAR_CUB_verified_supply_shortage } check_variable = { resource_imported@oil < COLDWAR_CUB_oil_import_recovery_threshold } }
			set_country_flag = COLDWAR_CUB_verified_supply_shortage
			COLDWAR_CUB_refresh_dependency = yes
		}
	}
}

# Per-recipient mission flags persist while the partner remains an independent wartime partner.
COLDWAR_CUB_refresh_overseas_aggregate = {
	every_country = {
		limit = { has_country_flag = COLDWAR_CUB_overseas_mission_active NOT = { COLDWAR_CUB_independent_wartime_partner = yes } }
		clr_country_flag = COLDWAR_CUB_overseas_mission_active
	}
	clr_country_flag = COLDWAR_CUB_overseas_mission_active
	every_country = {
		limit = { has_country_flag = COLDWAR_CUB_overseas_mission_active NOT = { tag = CUB } is_subject = no has_war = yes NOT = { has_war_with = CUB } }
		CUB = { set_country_flag = COLDWAR_CUB_overseas_mission_active }
	}
}

# Limited settlement removes the native US embargo and only the Imperia economic link.
# Finance, diplomacy and military restrictions require their own terms.
COLDWAR_CUB_lift_usa_economic_restriction = {
	if = {
		limit = { country_exists = USA }
		USA = { if = { limit = { is_embargoing = CUB } break_embargo = CUB } }
		if = {
			limit = { is_in_array = { array = imp_eco_sanc_on_us value = USA } }
			remove_from_array = { array = imp_eco_sanc_on_us value = USA }
			remove_opinion_modifier = { target = USA modifier = opinion_eco_sanctioned_us }
			USA = { remove_from_array = { array = imp_eco_sanc_by_us value = CUB } }
			set_temp_variable = { mdcw_cw_t_sanc_type = 3 }
			if = { limit = { has_global_flag = mdcw_cw_initialized } mdcw_cw_on_sanction_lifted = yes }
			imp_sanctions_calculate = yes
			USA = { imp_sanctions_calculate = yes }
		}
	}
}

# Full executive settlement additionally removes the bilateral financial restriction.
COLDWAR_CUB_lift_usa_trade_restrictions = {
	COLDWAR_CUB_lift_usa_economic_restriction = yes
	if = {
		limit = { country_exists = USA }
		if = {
			limit = { is_in_array = { array = imp_fin_sanc_on_us value = USA } }
			remove_from_array = { array = imp_fin_sanc_on_us value = USA }
			remove_opinion_modifier = { target = USA modifier = opinion_fin_sanctioned_us }
			USA = { remove_from_array = { array = imp_fin_sanc_by_us value = CUB } }
			set_temp_variable = { mdcw_cw_t_sanc_type = 2 }
			if = { limit = { has_global_flag = mdcw_cw_initialized } mdcw_cw_on_sanction_lifted = yes }
			imp_sanctions_calculate = yes
			USA = { imp_sanctions_calculate = yes }
		}
	}
}

# IMPERIA COLD WAR — make bilateral termination available during suspension too.
COLDWAR_CUB_end_soviet_assistance = {
	if = {
		limit = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed }
		if = { limit = { has_idea = COLDWAR_CUB_soviet_assistance } remove_ideas = COLDWAR_CUB_soviet_assistance }
		clr_country_flag = COLDWAR_CUB_soviet_assistance_active
		COLDWAR_CUB_refresh_dependency = yes
		if = { limit = { country_exists = SOV } SOV = { clr_country_flag = COLDWAR_CUB_soviet_assistance_active } }
		COLDWAR_CUB_cancel_soviet_assistance = yes
	}
}

# IMPERIA COLD WAR — make symbolic bilateral termination available during suspension.
COLDWAR_CUB_end_symbolic_cooperation = {
	if = { limit = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } COLDWAR_CUB_cancel_symbolic_cooperation = yes }
	clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active
	if = { limit = { country_exists = DDR } DDR = { clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active } }
	COLDWAR_CUB_cancel_symbolic_cooperation = yes
}

# No second compensation or transfer can occur at the follow-up focus.
COLDWAR_CUB_island_cession_followup = {
	if = { limit = { has_country_flag = COLDWAR_CUB_island_cession_ratified DDR = { owns_state = 1252 } } set_country_flag = COLDWAR_CUB_development_protocol_completed }
}

'''

TRIGGERS = r'''# IMPERIA COLD WAR — Cuba 1970 diplomatic eligibility triggers.

COLDWAR_CUB_valid_health_budget = {
	OR = { has_idea = health_01 has_idea = health_02 has_idea = health_03 has_idea = health_04 has_idea = health_05 has_idea = health_06 }
}

COLDWAR_CUB_us_trade_restriction_active = {
	OR = {
		USA = { is_embargoing = CUB }
		is_in_array = { array = imp_eco_sanc_on_us value = USA }
	}
}

COLDWAR_CUB_independent_mission_target = {
	NOT = { tag = CUB }
	is_subject = no
	COLDWAR_CUB_valid_health_budget = yes
	NOT = { has_war_with = CUB }
}

COLDWAR_CUB_independent_wartime_partner = {
	NOT = { tag = CUB }
	is_subject = no
	has_war = yes
	NOT = { has_war_with = CUB }
}
'''

EVENTS = r'''# IMPERIA COLD WAR — Cuba 1970 recipient-owned diplomatic notices.
add_namespace = COLDWAR_CUB_diplomacy

country_event = {
	id = COLDWAR_CUB_diplomacy.1
	title = COLDWAR_CUB_diplomacy.1.t
	desc = COLDWAR_CUB_diplomacy.1.d
	picture = GFX_cuba_wants_protec_rus
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.2
	title = COLDWAR_CUB_diplomacy.2.t
	desc = COLDWAR_CUB_diplomacy.2.d
	picture = GFX_soviet_union_flag
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.3
	title = COLDWAR_CUB_diplomacy.3.t
	desc = COLDWAR_CUB_diplomacy.3.d
	picture = GFX_soviet_union_flag
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.4
	title = COLDWAR_CUB_diplomacy.4.t
	desc = COLDWAR_CUB_diplomacy.4.d
	picture = GFX_cuba_constitution
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.5
	title = COLDWAR_CUB_diplomacy.5.t
	desc = COLDWAR_CUB_diplomacy.5.d
	picture = GFX_cuba_constitution
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.6
	title = COLDWAR_CUB_diplomacy.6.t
	desc = COLDWAR_CUB_diplomacy.6.d
	picture = GFX_news_us_cuba
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.7
	title = COLDWAR_CUB_diplomacy.7.t
	desc = COLDWAR_CUB_diplomacy.7.d
	picture = GFX_pol_socialism_event
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.8
	title = COLDWAR_CUB_diplomacy.8.t
	desc = COLDWAR_CUB_diplomacy.8.d
	picture = GFX_pol_socialism_event
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.9
	title = COLDWAR_CUB_diplomacy.9.t
	desc = COLDWAR_CUB_diplomacy.9.d
	picture = GFX_pol_socialism_event
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.10
	title = COLDWAR_CUB_diplomacy.10.t
	desc = COLDWAR_CUB_diplomacy.10.d
	picture = GFX_soviet_union_flag
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.review }
}

country_event = {
	id = COLDWAR_CUB_diplomacy.900
	title = COLDWAR_CUB_diplomacy.900.t
	desc = COLDWAR_CUB_diplomacy.900.d
	picture = GFX_cuba_constitution
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.close }
}
country_event = {
	id = COLDWAR_CUB_diplomacy.901
	title = COLDWAR_CUB_diplomacy.901.t
	desc = COLDWAR_CUB_diplomacy.901.d
	picture = GFX_cuba_constitution
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_diplomacy.close }
}
'''

IDEAS = r'''# IMPERIA COLD WAR — Cuba 1970 diplomatic programme ideas.
ideas = {
	country = {
		COLDWAR_CUB_cmea_member = {
			picture = communism3
			allowed = { always = no }
			allowed_civil_war = { always = yes }
		}
		COLDWAR_CUB_soviet_assistance = {
			picture = communism3
			allowed = { always = no }
			allowed_civil_war = { always = yes }
			modifier = { imp_sanction_resistance = 0.15 foreign_influence_defense_modifier = -0.15 }
		}
		COLDWAR_CUB_medical_mission_365 = {
			picture = generic_healthcare
			allowed = { always = no }
			allowed_civil_war = { always = yes }
			modifier = { health_cost_multiplier_modifier = -0.05 }
		}
		COLDWAR_CUB_symbolic_cooperation = {
			picture = communism3
			allowed = { always = no }
			allowed_civil_war = { always = yes }
			modifier = { research_speed_factor = 0.02 education_cost_multiplier_modifier = 0.03 }
		}
	}
}
'''

def response_offer(kind, accepted_effects, accept_guard="", title=""):
    """Recipient owns the accept/refuse decision; all runtime guards are repeated at execution."""
    stem = {"soviet_assistance": "soviet"}.get(kind, kind)
    flag = f"COLDWAR_CUB_{stem}_offer_pending"
    rootflag = f"COLDWAR_CUB_{stem}_offer_open"
    guard = f"has_country_flag = {flag} CUB = {{ has_country_flag = {rootflag} country_exists = CUB NOT = {{ has_war_with = ROOT }} }} {accept_guard}".strip()
    return f'''
	COLDWAR_CUB_accept_{kind} = {{
		icon = generic_diplomacy
		visible = {{ has_country_flag = {flag} }}
		available = {{ {guard} }}
		cost = 0
		days_remove = 90
		complete_effect = {{
			if = {{
				limit = {{ {guard} }}
{accepted_effects}
				clr_country_flag = {flag}
				CUB = {{ clr_country_flag = {rootflag} country_event = {{ id = COLDWAR_CUB_diplomacy.900 days = 1 }} }}
			}}
		}}
		ai_will_do = {{ base = 4 }}
	}}
	COLDWAR_CUB_refuse_{kind} = {{
		icon = generic_diplomacy
		visible = {{ has_country_flag = {flag} }}
		available = {{ has_country_flag = {flag} CUB = {{ has_country_flag = {rootflag} country_exists = CUB }} }}
		cost = 0
		days_remove = 90
		complete_effect = {{
			if = {{
				limit = {{ has_country_flag = {flag} CUB = {{ has_country_flag = {rootflag} country_exists = CUB }} }}
				clr_country_flag = {flag}
				set_country_flag = {{ flag = COLDWAR_CUB_{kind}_refused value = 1 days = 90 }}
				CUB = {{ clr_country_flag = {rootflag} set_country_flag = {{ flag = COLDWAR_CUB_{kind}_refused value = 1 days = 90 }} country_event = {{ id = COLDWAR_CUB_diplomacy.901 days = 1 }} }}
			}}
		}}
		ai_will_do = {{ base = 1 }}
	}}
'''

SOV_ACCEPT = r'''
				if = { limit = { NOT = { CUB = { has_country_flag = COLDWAR_CUB_soviet_assistance_receipt } } }
					set_temp_variable = { treasury_change = -0.30 }
					modify_treasury_effect = yes
					CUB = { set_temp_variable = { treasury_change = -0.10 } modify_treasury_effect = yes add_tech_bonus = { name = COLDWAR_CUB_soviet_industry_bonus bonus = 0.25 uses = 1 category = CAT_industry } set_country_flag = COLDWAR_CUB_soviet_assistance_receipt }
					set_country_flag = COLDWAR_CUB_soviet_assistance_receipt
				}
				add_opinion_modifier = { target = CUB modifier = COLDWAR_CUB_opinion_15 }
				# IMPERIA COLD WAR — record and reconcile the signed Soviet agreement.
				CUB = { COLDWAR_CUB_start_soviet_assistance = yes }
'''

RESPONSES = r'''# IMPERIA COLD WAR — Cuba 1970 recipient decisions and CUB contract desk.
COLDWAR_CUB_diplomacy_responses = {
'''

RESPONSES += response_offer(
    "soviet_assistance", SOV_ACCEPT,
    "NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed }",
)
RESPONSES += response_offer(
    "soviet_fuel", r'''
				CUB = {
					set_variable = { COLDWAR_CUB_soviet_oil_import_baseline = resource_imported@oil }
					set_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active
					clr_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn
					clr_country_flag = COLDWAR_CUB_verified_supply_shortage
					COLDWAR_CUB_refresh_dependency = yes
				}
				set_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active
				clr_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn
''',
    "NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active } CUB = { check_variable = { resource_imported@oil > 0 } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active } }",
)
RESPONSES += response_offer(
    "cmea", r'''
				CUB = {
					set_temp_variable = { treasury_change = -0.10 }
					modify_treasury_effect = yes
					add_ideas = COLDWAR_CUB_cmea_member
					clr_country_flag = COLDWAR_CUB_cmea_left
				}
''', "NOT = { has_idea = COLDWAR_CUB_cmea_member }",
)
RESPONSES += response_offer(
    "air", r'''
				set_temp_variable = { treasury_change = -0.15 }
				modify_treasury_effect = yes
				CUB = {
					if = { limit = { owns_state = 854 controls_state = 854 854 = { free_building_slots = { building = radar_station size > 0 include_locked = no } } } }
					set_temp_variable = { treasury_change = -0.45 }
					modify_treasury_effect = yes
					854 = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = radar_station level = 1 instant_build = yes } }
					add_tech_bonus = { name = COLDWAR_CUB_air_defence_radar_bonus bonus = 0.25 uses = 1 technology = radar }
					set_country_flag = COLDWAR_CUB_air_defence_receipt
				}
''', "NOT = { has_country_flag = COLDWAR_CUB_air_defence_receipt } CUB = { owns_state = 854 controls_state = 854 854 = { free_building_slots = { building = radar_station size > 0 include_locked = no } } }",
)
RESPONSES += response_offer(
    "medical", r'''
				# IMPERIA COLD WAR — one-time setup cost and indefinite accepted treaty.
				if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_medical_mission_receipt } }
					set_temp_variable = { treasury_change = -0.10 }
					modify_treasury_effect = yes
					set_country_flag = COLDWAR_CUB_medical_mission_receipt
					CUB = {
						set_temp_variable = { treasury_change = -0.15 }
						modify_treasury_effect = yes
						add_opinion_modifier = { target = ROOT modifier = COLDWAR_CUB_opinion_15 }
					}
				}
			set_country_flag = COLDWAR_CUB_medical_mission_signed
			CUB = { set_country_flag = COLDWAR_CUB_medical_mission_signed COLDWAR_CUB_reconcile_medical_mission = yes }
''', "NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } COLDWAR_CUB_valid_health_budget = yes COLDWAR_CUB_medical_pair_clear = yes",
)
RESPONSES += response_offer(
    "overseas", r'''
				set_country_flag = COLDWAR_CUB_overseas_mission_receipt
				set_country_flag = COLDWAR_CUB_overseas_mission_active
				CUB = {
					set_country_flag = COLDWAR_CUB_overseas_mission_active
				}
''', "NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } COLDWAR_CUB_independent_wartime_partner = yes",
)

RESPONSES += r'''
	COLDWAR_CUB_accept_us_limited = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_us_offer_pending }
		available = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB NOT = { has_war_with = ROOT } NOT = { has_country_flag = COLDWAR_CUB_us_easing_limited } NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } } }
		cost = 0
		days_remove = 90
		complete_effect = {
			if = { limit = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB NOT = { has_war_with = ROOT } NOT = { has_country_flag = COLDWAR_CUB_us_easing_limited } NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } } }
				CUB = {
					if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_us_commission_paid } } set_temp_variable = { treasury_change = -0.10 } modify_treasury_effect = yes set_country_flag = COLDWAR_CUB_us_commission_paid }
					COLDWAR_CUB_lift_usa_economic_restriction = yes
					set_country_flag = COLDWAR_CUB_us_easing_limited
					add_opinion_modifier = { target = USA modifier = COLDWAR_CUB_opinion_10 }
					COLDWAR_CUB_sync_embargo = yes
				}
				add_opinion_modifier = { target = CUB modifier = COLDWAR_CUB_opinion_10 }
				clr_country_flag = COLDWAR_CUB_us_offer_pending
				CUB = { clr_country_flag = COLDWAR_CUB_us_offer_open country_event = { id = COLDWAR_CUB_diplomacy.900 days = 1 } }
			}
		}
		ai_will_do = { base = 4 }
	}
	COLDWAR_CUB_accept_us_full = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_us_offer_pending }
		available = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB NOT = { has_war_with = ROOT } NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } } }
		cost = 0
		days_remove = 90
		complete_effect = {
			if = { limit = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB NOT = { has_war_with = ROOT } NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } } }
				CUB = {
					if = { limit = { has_country_flag = COLDWAR_CUB_us_commission_paid } set_temp_variable = { treasury_change = -0.15 } modify_treasury_effect = yes }
					else = { set_temp_variable = { treasury_change = -0.25 } modify_treasury_effect = yes set_country_flag = COLDWAR_CUB_us_commission_paid }
					set_country_flag = COLDWAR_CUB_us_full_settlement
					clr_country_flag = COLDWAR_CUB_us_easing_limited
					COLDWAR_CUB_lift_usa_trade_restrictions = yes
					COLDWAR_CUB_sync_embargo = yes
					add_opinion_modifier = { target = USA modifier = COLDWAR_CUB_opinion_20 }
				}
			add_opinion_modifier = { target = CUB modifier = COLDWAR_CUB_opinion_20 }
			clr_country_flag = COLDWAR_CUB_us_offer_pending
			CUB = { clr_country_flag = COLDWAR_CUB_us_offer_open country_event = { id = COLDWAR_CUB_diplomacy.900 days = 1 } }
			}
		}
		ai_will_do = { base = 3 }
	}
	COLDWAR_CUB_refuse_us_normalisation = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_us_offer_pending }
		available = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB } }
		cost = 0
		days_remove = 90
		complete_effect = { if = { limit = { has_country_flag = COLDWAR_CUB_us_offer_pending CUB = { has_country_flag = COLDWAR_CUB_us_offer_open country_exists = CUB } } clr_country_flag = COLDWAR_CUB_us_offer_pending set_country_flag = { flag = COLDWAR_CUB_us_normalisation_refused value = 1 days = 90 } CUB = { clr_country_flag = COLDWAR_CUB_us_offer_open set_country_flag = { flag = COLDWAR_CUB_us_normalisation_refused value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.901 days = 1 } } } }
		ai_will_do = { base = 1 }
	}
	COLDWAR_CUB_withdraw_soviet_fuel_commitment = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active }
		available = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn } } set_country_flag = COLDWAR_CUB_soviet_fuel_commitment_withdrawn CUB = { COLDWAR_CUB_sync_soviet_fuel_commitment = yes } } }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_end_soviet_assistance_as_recipient = {
		icon = generic_diplomacy
		visible = { tag = SOV has_country_flag = COLDWAR_CUB_soviet_assistance_signed CUB = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } }
		available = { tag = SOV has_country_flag = COLDWAR_CUB_soviet_assistance_signed CUB = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { tag = SOV has_country_flag = COLDWAR_CUB_soviet_assistance_signed CUB = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } } CUB = { COLDWAR_CUB_end_soviet_assistance = yes } } }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_end_symbolic_cooperation_as_recipient = {
		icon = generic_diplomacy
		visible = { tag = DDR has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed CUB = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } }
		available = { tag = DDR has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed CUB = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { tag = DDR has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed CUB = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } } CUB = { COLDWAR_CUB_end_symbolic_cooperation = yes } } }
		ai_will_do = { base = 0 }
	}
'''

RESPONSES += response_offer(
    "ddr", r'''
				set_temp_variable = { treasury_change = -0.10 }
				modify_treasury_effect = yes
				CUB = {
					if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_ddr_commission_receipt } }
						set_temp_variable = { treasury_change = -0.10 }
						modify_treasury_effect = yes
						add_tech_bonus = { name = COLDWAR_CUB_ddr_electronics_bonus bonus = 0.25 uses = 1 category = CAT_electronics }
						set_country_flag = COLDWAR_CUB_ddr_commission_receipt
					}
					add_opinion_modifier = { target = DDR modifier = COLDWAR_CUB_opinion_15 }
				}
				add_tech_bonus = { name = COLDWAR_CUB_ddr_electronics_bonus bonus = 0.25 uses = 1 category = CAT_electronics }
				add_opinion_modifier = { target = CUB modifier = COLDWAR_CUB_opinion_15 }
				set_country_flag = COLDWAR_CUB_ddr_commission_receipt
''', "NOT = { has_country_flag = COLDWAR_CUB_ddr_commission_receipt }",
)
RESPONSES += response_offer(
    "symbolic", r'''
				# IMPERIA COLD WAR — one-time package reward and re-acceptable treaty signature.
				if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_receipt } }
					set_temp_variable = { treasury_change = -0.20 }
					modify_treasury_effect = yes
					add_tech_bonus = { name = COLDWAR_CUB_symbolic_electronics_bonus bonus = 0.25 uses = 1 category = CAT_electronics }
					set_country_flag = COLDWAR_CUB_symbolic_cooperation_receipt
					CUB = { set_temp_variable = { treasury_change = -0.05 } modify_treasury_effect = yes add_tech_bonus = { name = COLDWAR_CUB_symbolic_electronics_bonus bonus = 0.25 uses = 1 category = CAT_electronics } set_country_flag = COLDWAR_CUB_symbolic_cooperation_receipt }
				}
			CUB = { COLDWAR_CUB_start_symbolic_cooperation = yes }
''', "NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } CUB = { COLDWAR_CUB_pair_ddr_clear = yes owns_state = 1252 controls_state = 1252 NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } }",
)
RESPONSES += response_offer(
    "cession", r'''
				set_temp_variable = { treasury_change = -0.40 }
				modify_treasury_effect = yes
				CUB = {
					if = { limit = { owns_state = 1252 controls_state = 1252 NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } }
						set_temp_variable = { treasury_change = 0.40 }
						modify_treasury_effect = yes
						add_stability = -0.03
						add_tech_bonus = { name = COLDWAR_CUB_island_industry_bonus bonus = 0.50 uses = 1 category = CAT_industry }
						set_country_flag = COLDWAR_CUB_island_cession_ratified
					}
				}
			transfer_state = 1252
			1252 = { set_state_name = COLDWAR_CUB_thaelmann_island_name }
			set_country_flag = COLDWAR_CUB_island_cession_ratified
''', "NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } CUB = { owns_state = 1252 controls_state = 1252 NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } } NOT = { has_war_with = CUB }",
)

RESPONSES += r'''
}

# CUB's diplomacy desk: offers, targeted programmes, and explicit termination.
COLDWAR_CUB_diplomacy = {
 COLDWAR_CUB_retry_soviet_assistance = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_moscow_guarantee } available = { country_exists = SOV NOT = { has_country_flag = COLDWAR_CUB_soviet_offer_open } NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_refused } NOT = { has_war_with = SOV } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_soviet_assistance = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_propose_soviet_fuel_commitment = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_moscow_guarantee } available = { country_exists = SOV check_variable = { resource_imported@oil > 0 } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_offer_open } NOT = { has_country_flag = COLDWAR_CUB_soviet_fuel_refused } NOT = { has_war_with = SOV } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_soviet_fuel_commitment = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_cmea_admission = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_cmea_application } available = { country_exists = SOV NOT = { has_idea = COLDWAR_CUB_cmea_member } NOT = { has_country_flag = COLDWAR_CUB_cmea_offer_open } NOT = { has_country_flag = COLDWAR_CUB_cmea_refused } NOT = { has_war_with = SOV } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_cmea_admission = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_air_defence = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_air_defence } available = { country_exists = SOV NOT = { has_country_flag = COLDWAR_CUB_air_offer_open } NOT = { has_country_flag = COLDWAR_CUB_air_defence_receipt } NOT = { has_country_flag = COLDWAR_CUB_air_refused } owns_state = 854 controls_state = 854 854 = { free_building_slots = { building = radar_station size > 0 include_locked = no } } NOT = { has_war_with = SOV } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_air_defence = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_us_normalisation = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_washington_talks } available = { country_exists = USA NOT = { has_country_flag = COLDWAR_CUB_us_offer_open } NOT = { has_country_flag = COLDWAR_CUB_us_full_settlement } NOT = { has_country_flag = COLDWAR_CUB_us_normalisation_refused } NOT = { has_war_with = USA } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_us_normalisation = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_ddr_commission = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_berlin_havana } available = { country_exists = DDR NOT = { has_country_flag = COLDWAR_CUB_ddr_offer_open } NOT = { has_country_flag = COLDWAR_CUB_ddr_commission_receipt } NOT = { has_country_flag = COLDWAR_CUB_ddr_refused } NOT = { has_war_with = DDR } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_ddr_commission = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_symbolic_cooperation = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_playa_rda } available = { country_exists = DDR has_completed_focus = COLDWAR_CUB_thaelmann_name owns_state = 1252 controls_state = 1252 COLDWAR_CUB_pair_ddr_clear = yes NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } NOT = { has_country_flag = COLDWAR_CUB_symbolic_offer_open } NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } NOT = { has_country_flag = COLDWAR_CUB_symbolic_refused } NOT = { has_war_with = DDR } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_symbolic_island_cooperation = yes } ai_will_do = { base = 1 } }
 COLDWAR_CUB_retry_island_cession = { icon = generic_diplomacy visible = { has_completed_focus = COLDWAR_CUB_caribbean_treaty } available = { country_exists = DDR owns_state = 1252 controls_state = 1252 date > 1972.6.18 NOT = { has_completed_focus = COLDWAR_CUB_thaelmann_name } NOT = { has_country_flag = COLDWAR_CUB_island_cession_ratified } NOT = { has_country_flag = COLDWAR_CUB_cession_offer_open } NOT = { has_country_flag = COLDWAR_CUB_cession_refused } NOT = { has_war_with = DDR } } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_offer_island_cession = yes } ai_will_do = { base = 1 } }

	COLDWAR_CUB_medical_offer_target = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_medical_targeting_enabled }
		target_array = global.countries
		target_root_trigger = { COLDWAR_CUB_is_1970 = yes }
		target_trigger = { FROM = { COLDWAR_CUB_independent_mission_target = yes NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } } }
		available = { NOT = { has_country_flag = COLDWAR_CUB_medical_offer_open } NOT = { has_country_flag = COLDWAR_CUB_medical_refused } FROM = { COLDWAR_CUB_independent_mission_target = yes NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_medical_offer_open } NOT = { has_country_flag = COLDWAR_CUB_medical_refused } FROM = { COLDWAR_CUB_independent_mission_target = yes NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } } } set_country_flag = { flag = COLDWAR_CUB_medical_offer_open value = 1 days = 90 } FROM = { set_country_flag = { flag = COLDWAR_CUB_medical_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.4 } } } }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_overseas_offer_target = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_overseas_targeting_enabled }
		target_array = global.countries
		target_root_trigger = { COLDWAR_CUB_is_1970 = yes }
		target_trigger = { FROM = { COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } }
		available = { NOT = { has_country_flag = COLDWAR_CUB_overseas_offer_open } NOT = { has_country_flag = COLDWAR_CUB_overseas_refused } FROM = { COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_overseas_offer_open } NOT = { has_country_flag = COLDWAR_CUB_overseas_refused } FROM = { COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } } set_country_flag = { flag = COLDWAR_CUB_overseas_offer_open value = 1 days = 90 } FROM = { set_country_flag = { flag = COLDWAR_CUB_overseas_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_diplomacy.5 } } } }
		ai_will_do = { base = 0 }
	}
 COLDWAR_CUB_conduct_overseas_advisory = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_overseas_mission_active }
		target_array = global.countries
		target_root_trigger = { COLDWAR_CUB_is_1970 = yes }
		target_trigger = { FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_advisory_receipt } } }
		available = { has_army_size = { size > 0 } FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_advisory_receipt } } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { has_army_size = { size > 0 } FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active COLDWAR_CUB_independent_wartime_partner = yes NOT = { has_country_flag = COLDWAR_CUB_overseas_advisory_receipt } } } set_temp_variable = { treasury_change = -0.20 } modify_treasury_effect = yes FROM = { army_experience = 15 set_country_flag = COLDWAR_CUB_overseas_advisory_receipt } } }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_end_overseas_mission_for_partner = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_overseas_mission_active }
		target_array = global.countries
		target_root_trigger = { COLDWAR_CUB_is_1970 = yes }
		target_trigger = { FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active } }
		available = { FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active } }
		cost = 0
		days_re_enable = 1
		complete_effect = { if = { limit = { FROM = { has_country_flag = COLDWAR_CUB_overseas_mission_active } } FROM = { clr_country_flag = COLDWAR_CUB_overseas_mission_active } COLDWAR_CUB_refresh_overseas_aggregate = yes } }
		ai_will_do = { base = 0 }
	}
 COLDWAR_CUB_end_soviet_assistance_decision = { icon = generic_diplomacy visible = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } available = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_end_soviet_assistance = yes } ai_will_do = { base = 0 } }
 COLDWAR_CUB_end_symbolic_cooperation_decision = { icon = generic_diplomacy visible = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } available = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_end_symbolic_cooperation = yes } ai_will_do = { base = 0 } }
	COLDWAR_CUB_leave_cmea_decision = { icon = generic_diplomacy visible = { has_idea = COLDWAR_CUB_cmea_member } available = { has_idea = COLDWAR_CUB_cmea_member } cost = 0 days_re_enable = 1 complete_effect = { remove_ideas = COLDWAR_CUB_cmea_member set_country_flag = COLDWAR_CUB_cmea_left } ai_will_do = { base = 0 } }
	COLDWAR_CUB_end_own_overseas_mission = { icon = generic_diplomacy visible = { has_country_flag = COLDWAR_CUB_overseas_mission_active } available = { has_country_flag = COLDWAR_CUB_overseas_mission_active } cost = 0 days_re_enable = 1 complete_effect = { clr_country_flag = COLDWAR_CUB_overseas_mission_active CUB = { COLDWAR_CUB_refresh_overseas_aggregate = yes } } ai_will_do = { base = 0 } }
}
'''

DECISION_CATEGORIES = r'''# IMPERIA COLD WAR — Cuba 1970 diplomatic decision categories.
COLDWAR_CUB_diplomacy = {
	allowed = { tag = CUB IMP_is_1970_scenario = yes }
	icon = generic_diplomacy
	priority = 205
	visible = { COLDWAR_CUB_is_1970 = yes OR = { has_completed_focus = COLDWAR_CUB_moscow_guarantee has_completed_focus = COLDWAR_CUB_cmea_application has_completed_focus = COLDWAR_CUB_air_defence has_completed_focus = COLDWAR_CUB_medical_brigades has_completed_focus = COLDWAR_CUB_african_mandate has_completed_focus = COLDWAR_CUB_washington_talks has_completed_focus = COLDWAR_CUB_berlin_havana has_completed_focus = COLDWAR_CUB_playa_rda has_completed_focus = COLDWAR_CUB_caribbean_treaty } }
}
COLDWAR_CUB_diplomacy_responses = {
	allowed = { NOT = { tag = CUB } }
	icon = generic_diplomacy
	priority = 210
	visible = { OR = { has_country_flag = COLDWAR_CUB_soviet_offer_pending has_country_flag = COLDWAR_CUB_soviet_fuel_offer_pending has_country_flag = COLDWAR_CUB_cmea_offer_pending has_country_flag = COLDWAR_CUB_air_offer_pending has_country_flag = COLDWAR_CUB_medical_offer_pending has_country_flag = COLDWAR_CUB_overseas_offer_pending has_country_flag = COLDWAR_CUB_us_offer_pending has_country_flag = COLDWAR_CUB_ddr_offer_pending has_country_flag = COLDWAR_CUB_symbolic_offer_pending has_country_flag = COLDWAR_CUB_cession_offer_pending has_country_flag = COLDWAR_CUB_overseas_mission_active has_country_flag = COLDWAR_CUB_soviet_assistance_active has_country_flag = COLDWAR_CUB_soviet_assistance_signed has_country_flag = COLDWAR_CUB_soviet_fuel_commitment_active has_country_flag = COLDWAR_CUB_symbolic_cooperation_active has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } }
}
'''

LOC = r'''l_english:
 COLDWAR_CUB_diplomacy.1.t:0 "Soviet Technical Assistance"
 COLDWAR_CUB_diplomacy.1.d:0 "Moscow has placed a technical-assistance proposal before the Cuban government. The Soviet Union has 90 days to consider the agreement in its national diplomatic decisions."
 COLDWAR_CUB_diplomacy.2.t:0 "CMEA Admission Application"
 COLDWAR_CUB_diplomacy.2.d:0 "The Soviet government has received Cuba's application for admission to the Council for Mutual Economic Assistance. A decision is available in the Soviet diplomatic decisions for 90 days."
 COLDWAR_CUB_diplomacy.3.t:0 "Air-Defence Training Proposal"
 COLDWAR_CUB_diplomacy.3.d:0 "Havana proposes a limited air-defence training arrangement. The Soviet government may review or refuse the Cuban proposal in its diplomatic decisions within 90 days."
 COLDWAR_CUB_diplomacy.4.t:0 "Cuban Medical Mission Offer"
 COLDWAR_CUB_diplomacy.4.d:0 "Cuba offers a requested medical mission. This recipient-owned proposal remains available for 90 days and charges neither government unless accepted."
 COLDWAR_CUB_diplomacy.5.t:0 "Cuban Overseas Assistance Proposal"
 COLDWAR_CUB_diplomacy.5.d:0 "Cuba offers an advisory arrangement in support of an agreed wartime partner. This recipient-owned proposal remains available for 90 days; refusal or expiry costs nothing."
 COLDWAR_CUB_diplomacy.6.t:0 "A Cuban–American Settlement"
 COLDWAR_CUB_diplomacy.6.d:0 "Havana proposes a negotiated settlement on bilateral trade restrictions. The United States may refuse, accept limited easing, or accept a full executive settlement within 90 days."
 COLDWAR_CUB_diplomacy.7.t:0 "Berlin–Havana Commission"
 COLDWAR_CUB_diplomacy.7.d:0 "Cuba proposes a joint commission with the German Democratic Republic. Acceptance requires both governments to meet the stated costs; the proposal expires after 90 days."
 COLDWAR_CUB_diplomacy.8.t:0 "Playa RDA Cultural Programme"
 COLDWAR_CUB_diplomacy.8.d:0 "Havana proposes cultural and scientific cooperation at the renamed Playa RDA. The island remains Cuban territory; the offer expires in 90 days."
 COLDWAR_CUB_diplomacy.9.t:0 "Ernst Thälmann Island — Territorial Proposal"
 COLDWAR_CUB_diplomacy.9.d:0 "Cuba has proposed the cession of Cayo Blanco del Sur. The GDR must explicitly accept; refusal leaves ownership and Cuban Treasury unchanged."
 COLDWAR_CUB_diplomacy.10.t:0 "Bilateral Oil-Import Undertaking"
 COLDWAR_CUB_diplomacy.10.d:0 "Havana proposes to record the current level of Cuban oil imports as a baseline for a bilateral Soviet supply undertaking. Acceptance creates no fuel, trade route, payment or automatic delivery; it records only a signed commitment against which later aggregate imports can be assessed."
 COLDWAR_CUB_diplomacy.review:0 "Review the proposal in the national diplomatic decisions."
 COLDWAR_CUB_diplomacy.900.t:0 "Agreement Accepted"
 COLDWAR_CUB_diplomacy.900.d:0 "The recipient has accepted Cuba's proposal. The agreed payment and one-time provisions have been applied."
 COLDWAR_CUB_diplomacy.901.t:0 "Proposal Refused"
 COLDWAR_CUB_diplomacy.901.d:0 "The recipient has refused the proposal. No Treasury payment or one-time reward was applied. A fresh offer may be made after the 90-day refusal period."
 COLDWAR_CUB_diplomacy.close:0 "Close"

 COLDWAR_CUB_diplomacy_response_title:0 "Diplomatic Proposals"
 COLDWAR_CUB_diplomacy_desk_title:0 "Cuban Diplomatic Desk"
 COLDWAR_CUB_diplomacy_category_desc:0 "Recipient governments review pending Cuban proposals here. Offers expire after 90 days and charge neither side if refused or unanswered."
 COLDWAR_CUB_accept_soviet_assistance:0 "Accept Soviet Technical Assistance"
 COLDWAR_CUB_accept_soviet_assistance_desc:0 "Soviet Treasury −0.30; Cuban Treasury −0.10. Cuba receives 1 × 25% CAT_industry research bonus and assistance programme (sanction resistance +15%, foreign-influence defence −15%). Soviet opinion of Cuba +15."
 COLDWAR_CUB_refuse_soviet_assistance:0 "Refuse Soviet Technical Assistance"
 COLDWAR_CUB_accept_soviet_fuel:0 "Accept the Oil-Supply Undertaking"
 COLDWAR_CUB_accept_soviet_fuel_desc:0 "No payment or delivery is created. Records current Cuban oil imports only when they are above zero. After Soviet withdrawal, imports falling below 80% of this baseline verify a supply shortage; recovery to 80% clears it."
 COLDWAR_CUB_refuse_soviet_fuel:0 "Decline the Oil-Supply Undertaking"
 COLDWAR_CUB_accept_cmea:0 "Admit Cuba to the CMEA"
 COLDWAR_CUB_accept_cmea_desc:0 "Cuban Treasury −0.10 on accepted admission. Grants the CMEA membership spirit; no automatic money or factories."
 COLDWAR_CUB_refuse_cmea:0 "Refuse CMEA Admission"
 COLDWAR_CUB_accept_air:0 "Accept Air-Defence Training"
 COLDWAR_CUB_accept_air_desc:0 "Cuban Treasury −0.45; Soviet Treasury −0.15. Cuba receives +1 radar level in Havana and one 25% radar research use."
 COLDWAR_CUB_refuse_air:0 "Refuse Air-Defence Training"
 COLDWAR_CUB_accept_medical:0 "Accept the Requested Medical Mission"
 COLDWAR_CUB_accept_medical_desc:0 "Recipient Treasury −0.10; Cuban Treasury −0.15. Recipient healthcare expenditure −5% for 365 days; Cuban opinion of recipient +15. The Cuban medical brigades' weekly funding is listed on its governing programme and is not charged again here."
 COLDWAR_CUB_refuse_medical:0 "Decline the Medical Mission"
 COLDWAR_CUB_accept_overseas:0 "Accept Overseas Assistance"
 COLDWAR_CUB_accept_overseas_desc:0 "Opens an advisory decision. If conducted while the eligibility remains valid, Cuba pays Treasury −0.20 and the recipient receives 15 army experience once. Ordinary volunteer and equipment diplomacy remains subject to the usual diplomatic rules and available troops and equipment."
 COLDWAR_CUB_refuse_overseas:0 "Decline Overseas Assistance"
 COLDWAR_CUB_accept_us_limited:0 "Accept Limited Trade Easing"
 COLDWAR_CUB_accept_us_limited_desc:0 "Cuban Treasury −0.10 once; reciprocal opinion +10. Removes the US embargo and US economic sanctions, while financial, diplomatic and military restrictions remain. Residual burden: resource-export revenue −10%, civilian productivity −3%, suspended if an comprehensive trade embargo is active."
 COLDWAR_CUB_accept_us_full:0 "Accept the Full Executive Settlement"
 COLDWAR_CUB_accept_us_full_desc:0 "Cuban Treasury −0.25 total (−0.15 if the commission was already paid); reciprocal opinion +20. Removes the US trade embargo and US economic and financial sanctions. Diplomatic and military restrictions, MFN, credit, claims and Guantánamo require separate terms."
 COLDWAR_CUB_refuse_us_normalisation:0 "Refuse the Settlement"
 COLDWAR_CUB_accept_ddr:0 "Establish the Berlin–Havana Commission"
 COLDWAR_CUB_accept_ddr_desc:0 "Cuban and DDR Treasury −0.10 each; each receives 1 × 25% electronics research bonus and +15 bilateral opinion."
 COLDWAR_CUB_refuse_ddr:0 "Decline the Commission"
 COLDWAR_CUB_accept_symbolic:0 "Accept Playa RDA Cooperation"
 COLDWAR_CUB_accept_symbolic_desc:0 "DDR Treasury −0.20; Cuban Treasury −0.05. Each receives 1 × 25% electronics research bonus. Cuba gains research speed +2% and weekly education expenditure +3%. Cayo Blanco del Sur remains Cuban."
 COLDWAR_CUB_refuse_symbolic:0 "Decline Cultural Cooperation"
 COLDWAR_CUB_accept_cession:0 "Ratify the Island Cession"
 COLDWAR_CUB_accept_cession_desc:0 "DDR Treasury −0.40; Cuban Treasury +0.40; Cuba stability −3 percentage points. Cayo Blanco del Sur transfers to DDR without a DDR core; Cuba receives 1 × 50% industrial research bonus."
 COLDWAR_CUB_refuse_cession:0 "Reject the Territorial Proposal"

 COLDWAR_CUB_retry_soviet_assistance:0 "Renew the Soviet Assistance Proposal"
 COLDWAR_CUB_propose_soviet_fuel_commitment:0 "Propose a Soviet Oil-Supply Undertaking"
 COLDWAR_CUB_withdraw_soviet_fuel_commitment:0 "Withdraw the Oil-Supply Undertaking"
 COLDWAR_CUB_retry_cmea_admission:0 "Renew the CMEA Application"
 COLDWAR_CUB_retry_air_defence:0 "Renew Air-Defence Proposal"
 COLDWAR_CUB_retry_us_normalisation:0 "Renew Trade-Settlement Talks"
 COLDWAR_CUB_retry_ddr_commission:0 "Renew the Berlin–Havana Proposal"
 COLDWAR_CUB_retry_symbolic_cooperation:0 "Renew Playa RDA Cooperation"
 COLDWAR_CUB_retry_island_cession:0 "Renew the Territorial Proposal"
 COLDWAR_CUB_medical_offer_target:0 "Offer a Medical Mission"
 COLDWAR_CUB_overseas_offer_target:0 "Offer Overseas Assistance"
 COLDWAR_CUB_conduct_overseas_advisory:0 "Conduct the Advisory Mission"
 COLDWAR_CUB_end_soviet_assistance_decision:0 "Terminate Soviet Technical Assistance"
 COLDWAR_CUB_end_soviet_assistance_as_recipient:0 "Withdraw Soviet Technical Assistance"
 COLDWAR_CUB_end_symbolic_cooperation_decision:0 "End Playa RDA Cooperation"
 COLDWAR_CUB_end_symbolic_cooperation_as_recipient:0 "End Playa RDA Cooperation"
 COLDWAR_CUB_leave_cmea_decision:0 "Withdraw from the CMEA"
 COLDWAR_CUB_thaelmann_island_name:0 "Ernst Thälmann Island"
 COLDWAR_CUB_soviet_industry_bonus:0 "Soviet Technical Assistance Programme"
 COLDWAR_CUB_air_defence_radar_bonus:0 "Soviet Air-Defence Training"
 COLDWAR_CUB_ddr_electronics_bonus:0 "Berlin–Havana Technical Commission"
 COLDWAR_CUB_symbolic_electronics_bonus:0 "Playa RDA Scientific Cooperation"
 COLDWAR_CUB_island_industry_bonus:0 "Ernst Thälmann Island Development Programme"
'''

def write(rel, data, bom=False):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if not bom:
        data = cub_radar_queries(data)
    data = stamp(data, 'Cuba 1970 diplomatic support.', localisation=bom)
    path.write_bytes(data.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8-sig" if bom else "utf-8"))

def main():
    write("common/scripted_effects/COLDWAR_CUB_1970_diplomacy.txt", EFFECTS)
    write("common/scripted_triggers/COLDWAR_CUB_1970_diplomacy.txt", TRIGGERS)
    write("events/COLDWAR_CUB_1970_diplomacy.txt", EVENTS)
    write("common/ideas/COLDWAR_CUB_1970_diplomacy_ideas.txt", IDEAS)
    write("common/decisions/COLDWAR_CUB_1970_diplomacy.txt", RESPONSES)
    write("common/decisions/categories/COLDWAR_CUB_1970_diplomacy.txt", DECISION_CATEGORIES)
    write("localisation/english/COLDWAR_CUB_1970_diplomacy_l_english.yml", LOC, bom=True)
    from bilateral import main as build_bilateral
    build_bilateral()
    print("Emitted diplomacy support files for 9 approved Cuba contracts and the metadata-only Soviet fuel undertaking.")

if __name__ == "__main__":
    main()
