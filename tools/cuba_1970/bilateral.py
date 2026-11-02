# IMPERIA COLD WAR — persistent Cuban bilateral treaties.
"""Emit accepted bilateral agreements and recipient-owned contract decisions."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
FLAVOUR = json.loads((Path(__file__).parent / "bilateral_flavour.json").read_text(encoding="utf-8"))["descriptions"]

PARTNERS = {
    "sov": {"tag": "SOV", "focus": "COLDWAR_CUB_moscow_guarantee", "label": "Soviet Union", "terms": {
        "commodity": {"label": "Commodity Protocol", "cost_cub": .15, "cost_partner": .35,
            "cub": "agriculture_district_income_tax_modifier = 0.12 resource_export_multiplier_modifier = 0.08 foreign_influence_defense_modifier = -0.08",
            "partner": "civilian_factories_productivity = 0.03 foreign_influence_modifier = 0.04 bureaucracy_cost_multiplier_modifier = 0.02"},
        "industry": {"label": "Industrial Modernisation Protocol", "cost_cub": .40, "cost_partner": .20,
            "cub": "civilian_factories_productivity = 0.08 production_speed_buildings_factor = 0.06 bureaucracy_cost_multiplier_modifier = 0.04",
            "partner": "research_speed_factor = 0.02 resource_export_multiplier_modifier = 0.05 education_cost_multiplier_modifier = 0.03"},
    }},
    "mex": {"tag": "MEX", "focus": "COLDWAR_CUB_island_diplomacy", "label": "Mexico", "terms": {
        "energy": {"label": "Regional Energy Coordination", "cost_cub": .15, "cost_partner": .20,
            "cub": "imp_sanction_resistance = 0.10 civilian_factories_productivity = 0.05 foreign_influence_defense_modifier = -0.04",
            "partner": "resource_export_multiplier_modifier = 0.06 foreign_influence_modifier = 0.04 bureaucracy_cost_multiplier_modifier = 0.03"},
        "agro": {"label": "Agro-Industrial Commission", "cost_cub": .25, "cost_partner": .15,
            "cub": "agricolture_productivity_modifier = 0.10 research_speed_factor = 0.02 education_cost_multiplier_modifier = 0.04",
            "partner": "agricolture_productivity_modifier = 0.04 research_speed_factor = 0.02 education_cost_multiplier_modifier = 0.03"},
    }},
    "spr": {"tag": "SPR", "focus": "COLDWAR_CUB_island_diplomacy", "label": "Spain", "terms": {
        "nickel": {"label": "Nickel and Machinery Trade Protocol", "cost_cub": .20, "cost_partner": .20,
            "cub": "resource_export_multiplier_modifier = 0.10 civilian_factories_productivity = 0.05 foreign_influence_defense_modifier = -0.04",
            "partner": "production_speed_buildings_factor = 0.04 resource_export_multiplier_modifier = 0.05 bureaucracy_cost_multiplier_modifier = 0.03"},
        "training": {"label": "Industrial Training Agreement", "cost_cub": .30, "cost_partner": .15,
            "cub": "production_speed_buildings_factor = 0.05 research_speed_factor = 0.03 education_cost_multiplier_modifier = 0.03",
            "partner": "research_speed_factor = 0.03 civilian_factories_productivity = 0.03 foreign_influence_defense_modifier = -0.02"},
    }},
    "can": {"tag": "CAN", "focus": "COLDWAR_CUB_island_diplomacy", "label": "Canada", "terms": {
        "rail": {"label": "Rail Service Contract", "cost_cub": .40, "cost_partner": .10,
            "cub": "production_speed_buildings_factor = 0.08 supply_consumption_factor = -0.04 foreign_influence_defense_modifier = -0.04",
            "partner": "resource_export_multiplier_modifier = 0.06 civilian_factories_productivity = 0.03 bureaucracy_cost_multiplier_modifier = 0.02"},
        "industry": {"label": "Industrial Purchasing Agreement", "cost_cub": .25, "cost_partner": .20,
            "cub": "civilian_factories_productivity = 0.08 research_speed_factor = 0.02 resource_export_multiplier_modifier = -0.04",
            "partner": "research_speed_factor = 0.03 resource_export_multiplier_modifier = 0.03 education_cost_multiplier_modifier = 0.02"},
    }},
}

def term_id(partner, term):
    return f"COLDWAR_CUB_bilat_{partner}_{term}"

def all_terms(partner):
    return list(PARTNERS[partner]["terms"])

def clear_trigger(partner, tag=None):
    tag = tag or PARTNERS[partner]["tag"]
    arrays = []
    for typ in ("dip", "fin", "eco", "mil"):
        for direction in ("on_us", "by_us"):
            arrays.append(f"is_in_array = {{ array = imp_{typ}_sanc_{direction} value = {tag} }}")
    p_arrays = []
    for typ in ("dip", "fin", "eco", "mil"):
        for direction in ("on_us", "by_us"):
            p_arrays.append(f"is_in_array = {{ array = imp_{typ}_sanc_{direction} value = CUB }}")
    return f"""COLDWAR_CUB_pair_{partner}_clear = {{
	country_exists = {tag}
	NOT = {{ has_war_with = {tag} }}
	NOT = {{ is_embargoing = {tag} }}
	NOT = {{ OR = {{ {' '.join(arrays)} }} }}
	{tag} = {{
		NOT = {{ has_war_with = CUB }}
		NOT = {{ is_embargoing = CUB }}
		NOT = {{ OR = {{ {' '.join(p_arrays)} }} }}
	}}
}}"""

TRIGGERS = "# IMPERIA COLD WAR — bilateral treaty eligibility.\n" + "\n\n".join(clear_trigger(p) for p in PARTNERS)
TRIGGERS += "\n\n" + clear_trigger("usa", "USA") + "\n\n" + clear_trigger("ddr", "DDR")
TRIGGERS += r'''
COLDWAR_CUB_medical_pair_clear = {
	NOT = { has_war_with = CUB }
	NOT = { is_embargoing = CUB }
	NOT = { OR = {
		is_in_array = { array = imp_dip_sanc_on_us value = CUB }
		is_in_array = { array = imp_dip_sanc_by_us value = CUB }
		is_in_array = { array = imp_fin_sanc_on_us value = CUB }
		is_in_array = { array = imp_fin_sanc_by_us value = CUB }
		is_in_array = { array = imp_eco_sanc_on_us value = CUB }
		is_in_array = { array = imp_eco_sanc_by_us value = CUB }
		is_in_array = { array = imp_mil_sanc_on_us value = CUB }
		is_in_array = { array = imp_mil_sanc_by_us value = CUB }
	} }
	CUB = {
		NOT = { has_war_with = PREV }
		NOT = { is_embargoing = PREV }
		NOT = { OR = {
			is_in_array = { array = imp_dip_sanc_on_us value = PREV }
			is_in_array = { array = imp_dip_sanc_by_us value = PREV }
			is_in_array = { array = imp_fin_sanc_on_us value = PREV }
			is_in_array = { array = imp_fin_sanc_by_us value = PREV }
			is_in_array = { array = imp_eco_sanc_on_us value = PREV }
			is_in_array = { array = imp_eco_sanc_by_us value = PREV }
			is_in_array = { array = imp_mil_sanc_on_us value = PREV }
			is_in_array = { array = imp_mil_sanc_by_us value = PREV }
		} }
	}
}
'''

EFFECTS = r'''# IMPERIA COLD WAR — persistent bilateral agreement lifecycle.
COLDWAR_CUB_reconcile_bilateral = {
'''
for p, spec in PARTNERS.items():
    tag = spec["tag"]
    for term, data in spec["terms"].items():
        tid = term_id(p, term)
        signed = f"{tid}_signed"
        idea_cub = f"{tid}_cub"
        idea_partner = f"{tid}_{p}"
        EFFECTS += f'''
	if = {{
		limit = {{ has_country_flag = {signed} {tag} = {{ has_country_flag = {signed} }} COLDWAR_CUB_pair_{p}_clear = yes }}
		if = {{ limit = {{ NOT = {{ has_idea = {idea_cub} }} }} add_ideas = {idea_cub} }}
		{tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = {idea_partner} }} }} add_ideas = {idea_partner} }} }}
	}}
	else = {{
		if = {{ limit = {{ has_idea = {idea_cub} }} remove_ideas = {idea_cub} }}
		if = {{ limit = {{ country_exists = {tag} {tag} = {{ has_idea = {idea_partner} }} }} {tag} = {{ remove_ideas = {idea_partner} }} }}
	}}
'''
EFFECTS += r'''
	# Legacy SOV and DDR agreements keep their original Cuba-side terms; counterpart spirits
	# are suspended and restored by the same mutual-peace/mutual-sanctions checks.
	if = { limit = { NOT = { has_country_flag = COLDWAR_CUB_bilateral_legacy_migrated } }
		if = { limit = { has_country_flag = COLDWAR_CUB_soviet_assistance_active SOV = { has_country_flag = COLDWAR_CUB_soviet_assistance_active } NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } }
			set_country_flag = COLDWAR_CUB_soviet_assistance_signed
			SOV = { set_country_flag = COLDWAR_CUB_soviet_assistance_signed }
		}
		if = { limit = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_active DDR = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_active } NOT = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } }
			set_country_flag = COLDWAR_CUB_symbolic_cooperation_signed
			DDR = { set_country_flag = COLDWAR_CUB_symbolic_cooperation_signed }
		}
		if = { limit = { has_country_flag = COLDWAR_CUB_history_interests_sections_active USA = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } }
			set_country_flag = COLDWAR_CUB_history_interests_receipt
			USA = { set_country_flag = COLDWAR_CUB_history_interests_receipt }
		}
		set_country_flag = COLDWAR_CUB_bilateral_legacy_migrated
	}
	if = { limit = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed SOV = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } COLDWAR_CUB_pair_sov_clear = yes }
		if = { limit = { NOT = { has_idea = COLDWAR_CUB_soviet_assistance } } add_ideas = COLDWAR_CUB_soviet_assistance }
		SOV = { if = { limit = { NOT = { has_idea = COLDWAR_CUB_soviet_assistance_sov } } add_ideas = COLDWAR_CUB_soviet_assistance_sov } }
		set_country_flag = COLDWAR_CUB_soviet_assistance_active
		SOV = { set_country_flag = COLDWAR_CUB_soviet_assistance_active }
	}
	else = {
		if = { limit = { has_idea = COLDWAR_CUB_soviet_assistance } remove_ideas = COLDWAR_CUB_soviet_assistance }
		if = { limit = { country_exists = SOV SOV = { has_idea = COLDWAR_CUB_soviet_assistance_sov } } SOV = { remove_ideas = COLDWAR_CUB_soviet_assistance_sov clr_country_flag = COLDWAR_CUB_soviet_assistance_active } }
		clr_country_flag = COLDWAR_CUB_soviet_assistance_active
	}
	if = { limit = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed DDR = { has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } COLDWAR_CUB_pair_ddr_clear = yes owns_state = 1252 controls_state = 1252 }
		if = { limit = { NOT = { has_idea = COLDWAR_CUB_symbolic_cooperation } } add_ideas = COLDWAR_CUB_symbolic_cooperation }
		DDR = { if = { limit = { NOT = { has_idea = COLDWAR_CUB_symbolic_cooperation_ddr } } add_ideas = COLDWAR_CUB_symbolic_cooperation_ddr } }
		set_country_flag = COLDWAR_CUB_symbolic_cooperation_active
		DDR = { set_country_flag = COLDWAR_CUB_symbolic_cooperation_active }
	}
	else = {
		if = { limit = { has_idea = COLDWAR_CUB_symbolic_cooperation } remove_ideas = COLDWAR_CUB_symbolic_cooperation }
		if = { limit = { country_exists = DDR DDR = { has_idea = COLDWAR_CUB_symbolic_cooperation_ddr } } DDR = { remove_ideas = COLDWAR_CUB_symbolic_cooperation_ddr clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active } }
		clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active
	}
	# Accepted medical treaties remain signed indefinitely. One Cuban programme spirit
	# represents all currently eligible recipients, avoiding stacking with multiple missions.
	if = { limit = { has_idea = COLDWAR_CUB_medical_mission_cub } remove_ideas = COLDWAR_CUB_medical_mission_cub }
	clr_country_flag = COLDWAR_CUB_medical_mission_active
	clr_country_flag = COLDWAR_CUB_medical_mission_signed
	every_country = {
		limit = { has_idea = COLDWAR_CUB_medical_mission_365 NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } NOT = { tag = CUB } }
		set_country_flag = COLDWAR_CUB_medical_mission_signed
		CUB = { set_country_flag = COLDWAR_CUB_medical_mission_signed }
	}
	every_country = {
		limit = { has_country_flag = COLDWAR_CUB_medical_mission_signed NOT = { tag = CUB } }
		CUB = { set_country_flag = COLDWAR_CUB_medical_mission_signed }
		if = { limit = { COLDWAR_CUB_medical_pair_clear = yes }
			if = { limit = { NOT = { has_idea = COLDWAR_CUB_medical_mission_partner } } add_ideas = COLDWAR_CUB_medical_mission_partner }
			CUB = { add_ideas = COLDWAR_CUB_medical_mission_cub set_country_flag = COLDWAR_CUB_medical_mission_active }
		}
		else = { if = { limit = { has_idea = COLDWAR_CUB_medical_mission_partner } remove_ideas = COLDWAR_CUB_medical_mission_partner } }
		if = { limit = { has_idea = COLDWAR_CUB_medical_mission_365 } remove_ideas = COLDWAR_CUB_medical_mission_365 }
	}
	if = { limit = { has_country_flag = COLDWAR_CUB_history_interests_sections_active USA = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } COLDWAR_CUB_pair_usa_clear = yes }
		if = { limit = { NOT = { has_idea = COLDWAR_CUB_interests_sections_cub } } add_ideas = COLDWAR_CUB_interests_sections_cub }
		USA = { if = { limit = { NOT = { has_idea = COLDWAR_CUB_interests_sections_usa } } add_ideas = COLDWAR_CUB_interests_sections_usa } }
	}
	else = {
		if = { limit = { has_idea = COLDWAR_CUB_interests_sections_cub } remove_ideas = COLDWAR_CUB_interests_sections_cub }
		if = { limit = { country_exists = USA USA = { has_idea = COLDWAR_CUB_interests_sections_usa } } USA = { remove_ideas = COLDWAR_CUB_interests_sections_usa } }
	}
	if = { limit = { has_idea = COLDWAR_CUB_hist_interests_sections_365 } remove_ideas = COLDWAR_CUB_hist_interests_sections_365 }
}

COLDWAR_CUB_reconcile_interests_sections = {
	COLDWAR_CUB_reconcile_bilateral = yes
}

COLDWAR_CUB_cancel_interests_sections = {
	if = { limit = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } clr_country_flag = COLDWAR_CUB_history_interests_sections_active USA = { clr_country_flag = COLDWAR_CUB_history_interests_sections_active } }
	COLDWAR_CUB_reconcile_bilateral = yes
}

COLDWAR_CUB_cancel_medical_mission = {
	if = { limit = { has_country_flag = COLDWAR_CUB_medical_mission_signed } clr_country_flag = COLDWAR_CUB_medical_mission_signed if = { limit = { has_idea = COLDWAR_CUB_medical_mission_partner } remove_ideas = COLDWAR_CUB_medical_mission_partner } if = { limit = { has_idea = COLDWAR_CUB_medical_mission_365 } remove_ideas = COLDWAR_CUB_medical_mission_365 } }
	CUB = { COLDWAR_CUB_reconcile_bilateral = yes }
}
'''

for p, spec in PARTNERS.items():
    for term in spec["terms"]:
        tid = term_id(p, term); tag = spec["tag"]
        EFFECTS += f"\nCOLDWAR_CUB_cancel_{p}_{term} = {{ clr_country_flag = {tid}_signed clr_country_flag = COLDWAR_CUB_bilat_{p}_package_signed {tag} = {{ clr_country_flag = {tid}_signed clr_country_flag = COLDWAR_CUB_bilat_{p}_package_signed }} COLDWAR_CUB_reconcile_bilateral = yes }}\n"
EFFECTS += "\nCOLDWAR_CUB_cancel_soviet_assistance = { clr_country_flag = COLDWAR_CUB_soviet_assistance_signed clr_country_flag = COLDWAR_CUB_soviet_assistance_active SOV = { clr_country_flag = COLDWAR_CUB_soviet_assistance_signed clr_country_flag = COLDWAR_CUB_soviet_assistance_active } COLDWAR_CUB_reconcile_bilateral = yes }\n"
EFFECTS += "COLDWAR_CUB_cancel_symbolic_cooperation = { clr_country_flag = COLDWAR_CUB_symbolic_cooperation_signed clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active DDR = { clr_country_flag = COLDWAR_CUB_symbolic_cooperation_signed clr_country_flag = COLDWAR_CUB_symbolic_cooperation_active } COLDWAR_CUB_reconcile_bilateral = yes }\n"

IDEAS = "# IMPERIA COLD WAR — paired bilateral agreement spirits.\nideas = {\n\tcountry = {\n"
for p, spec in PARTNERS.items():
    for term, data in spec["terms"].items():
        tid = term_id(p, term)
        for side, label, modifier in (("cub", "Cuban " + data["label"], data["cub"]), (p, spec["label"] + " " + data["label"], data["partner"])):
            IDEA = tid + "_" + side
            IDEAS += f"\t\t{IDEA} = {{ picture = communism3 allowed = {{ always = no }} allowed_civil_war = {{ always = yes }} modifier = {{ {modifier} }} }}\n"
IDEAS += r'''
		COLDWAR_CUB_soviet_assistance_sov = { picture = communism3 allowed = { always = no } allowed_civil_war = { always = yes } modifier = { foreign_influence_modifier = 0.05 bureaucracy_cost_multiplier_modifier = 0.02 } }
		COLDWAR_CUB_symbolic_cooperation_ddr = { picture = communism3 allowed = { always = no } allowed_civil_war = { always = yes } modifier = { research_speed_factor = 0.02 education_cost_multiplier_modifier = 0.03 } }
		COLDWAR_CUB_medical_mission_cub = { picture = generic_healthcare allowed = { always = no } allowed_civil_war = { always = yes } modifier = { foreign_influence_modifier = 0.03 education_cost_multiplier_modifier = 0.02 } }
		COLDWAR_CUB_medical_mission_partner = { picture = generic_healthcare allowed = { always = no } allowed_civil_war = { always = yes } modifier = { health_cost_multiplier_modifier = -0.05 } }
		COLDWAR_CUB_interests_sections_cub = { picture = communism3 allowed = { always = no } allowed_civil_war = { always = yes } modifier = { foreign_influence_modifier = 0.03 foreign_influence_defense_modifier = -0.02 } }
		COLDWAR_CUB_interests_sections_usa = { picture = communism3 allowed = { always = no } allowed_civil_war = { always = yes } modifier = { foreign_influence_modifier = 0.03 bureaucracy_cost_multiplier_modifier = 0.01 } }
	}
}
'''

def offer_effect(partner, term):
    spec = PARTNERS[partner]; tag = spec["tag"]; tid = term_id(partner, term)
    return f"""COLDWAR_CUB_offer_{partner}_{term} = {{
	if = {{ limit = {{ has_completed_focus = {spec['focus']} country_exists = {tag} COLDWAR_CUB_pair_{partner}_clear = yes NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_package_signed }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_offer_open }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_refused }} {tag} = {{ NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_offer_pending }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_refused }} }} }}
		set_country_flag = {{ flag = COLDWAR_CUB_bilat_{partner}_offer_open value = 1 days = 90 }}
		set_country_flag = {{ flag = COLDWAR_CUB_bilat_{partner}_{term}_offer_open value = 1 days = 90 }}
		{tag} = {{ set_country_flag = {{ flag = COLDWAR_CUB_bilat_{partner}_offer_pending value = 1 days = 90 }} set_country_flag = {{ flag = COLDWAR_CUB_bilat_{partner}_{term}_offer_pending value = 1 days = 90 }} country_event = {{ id = COLDWAR_CUB_bilateral.{offer_number(partner, term)} }} }}
	}}
}}"""

def offer_number(partner, term):
    n = 1
    for p, spec in PARTNERS.items():
        for t in spec["terms"]:
            if (p, t) == (partner, term): return n
            n += 1
    raise KeyError((partner, term))

EFFECTS = EFFECTS.replace("# Caller is Cuba; ROOT is one of the four fixed partners.", "# Called from Cuba. Each partner package is exclusive; paid flags survive cancellation.")
EFFECTS += "\n".join(offer_effect(p,t) for p,s in PARTNERS.items() for t in s["terms"])
EFFECTS += r'''
COLDWAR_CUB_start_soviet_assistance = {
	set_country_flag = COLDWAR_CUB_soviet_assistance_signed
	SOV = { set_country_flag = COLDWAR_CUB_soviet_assistance_signed }
	COLDWAR_CUB_reconcile_bilateral = yes
}
COLDWAR_CUB_start_symbolic_cooperation = {
	set_country_flag = COLDWAR_CUB_symbolic_cooperation_signed
	DDR = { set_country_flag = COLDWAR_CUB_symbolic_cooperation_signed }
	COLDWAR_CUB_reconcile_bilateral = yes
}
COLDWAR_CUB_reconcile_medical_mission = { COLDWAR_CUB_reconcile_bilateral = yes }
'''

EVENTS = "# IMPERIA COLD WAR — consent notices for bilateral treaty proposals.\nadd_namespace = COLDWAR_CUB_bilateral\n"
for p,spec in PARTNERS.items():
    for term,data in spec["terms"].items():
        n=offer_number(p,term)
        EVENTS += f'''\ncountry_event = {{
	id = COLDWAR_CUB_bilateral.{n}
	title = COLDWAR_CUB_bilateral.{n}.t
	desc = COLDWAR_CUB_bilateral.{n}.d
	is_triggered_only = yes
	trigger = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_{term}_offer_pending CUB = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_{term}_offer_open COLDWAR_CUB_pair_{p}_clear = yes }} }}
	option = {{ name = COLDWAR_CUB_bilateral.review }}
}}
'''
EVENTS += r'''
country_event = {
	id = COLDWAR_CUB_bilateral.900
	title = COLDWAR_CUB_bilateral.900.t
	desc = COLDWAR_CUB_bilateral.900.d
	is_triggered_only = yes
	option = { name = COLDWAR_CUB_bilateral.review }
}
'''

DECISIONS = "# IMPERIA COLD WAR — bilateral offers, consent, cancellation and reactivation.\n"
DECISIONS += "COLDWAR_CUB_bilateral_offers = {\n"
for p,spec in PARTNERS.items():
    for term,data in spec["terms"].items():
        tid=term_id(p,term); flag=f"{tid}_signed"; tag=spec["tag"]
        offer=f"COLDWAR_CUB_offer_{p}_{term}"
        DECISIONS += f'''	{offer} = {{
		icon = generic_diplomacy
		visible = {{ has_completed_focus = {spec['focus']} }}
		available = {{ has_completed_focus = {spec['focus']} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_package_signed }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_refused }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_offer_open }} COLDWAR_CUB_pair_{p}_clear = yes country_exists = {tag} {tag} = {{ NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_offer_pending }} NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_refused }} }} }}
		cost = 0 days_re_enable = 1 complete_effect = {{ {offer} = yes }} ai_will_do = {{ base = 0 }}
	}}
'''
        cancel=f"COLDWAR_CUB_cancel_bilat_{p}_{term}"
        DECISIONS += f'''	{cancel} = {{
		icon = generic_diplomacy
		visible = {{ has_country_flag = {flag} }} available = {{ has_country_flag = {flag} }}
		cost = 0 days_re_enable = 1 complete_effect = {{ COLDWAR_CUB_cancel_{p}_{term} = yes }} ai_will_do = {{ base = 0 }}
	}}
'''
DECISIONS += r'''	COLDWAR_CUB_end_medical_treaty_target = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_medical_targeting_enabled }
		target_array = global.countries
		target_root_trigger = { COLDWAR_CUB_is_1970 = yes }
		target_trigger = { FROM = { has_country_flag = COLDWAR_CUB_medical_mission_signed } }
		available = { FROM = { has_country_flag = COLDWAR_CUB_medical_mission_signed } }
		cost = 0 days_re_enable = 1
		complete_effect = { FROM = { COLDWAR_CUB_cancel_medical_mission = yes } }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_end_interests_sections = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_history_interests_sections_active }
		available = { has_country_flag = COLDWAR_CUB_history_interests_sections_active }
		cost = 0 days_re_enable = 1
		complete_effect = { COLDWAR_CUB_cancel_interests_sections = yes }
		ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_reopen_interests_sections = {
		icon = generic_diplomacy
		visible = { has_country_flag = COLDWAR_CUB_history_interests_sections_seen }
		available = { has_country_flag = COLDWAR_CUB_history_interests_sections_seen NOT = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } NOT = { has_country_flag = COLDWAR_CUB_history_interests_offer_open } country_exists = USA NOT = { has_war_with = USA } USA = { NOT = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } NOT = { has_country_flag = COLDWAR_CUB_history_interests_offer_pending } } }
		cost = 0 days_re_enable = 1
		complete_effect = { if = { limit = { has_country_flag = COLDWAR_CUB_history_interests_sections_seen NOT = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } NOT = { has_country_flag = COLDWAR_CUB_history_interests_offer_open } country_exists = USA NOT = { has_war_with = USA } USA = { NOT = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } NOT = { has_country_flag = COLDWAR_CUB_history_interests_offer_pending } } } set_country_flag = { flag = COLDWAR_CUB_history_interests_offer_open value = 1 days = 90 } USA = { set_country_flag = { flag = COLDWAR_CUB_history_interests_offer_pending value = 1 days = 90 } country_event = { id = COLDWAR_CUB_history.12 } } } }
		ai_will_do = { base = 0 }
	}
}

COLDWAR_CUB_bilateral_responses = {
'''
for p,spec in PARTNERS.items():
    tag=spec["tag"]
    for term,data in spec["terms"].items():
        tid=term_id(p,term); signed=f"{tid}_signed"; paid=f"{tid}_paid"; pending=f"COLDWAR_CUB_bilat_{p}_{term}_offer_pending"; opened=f"COLDWAR_CUB_bilat_{p}_{term}_offer_open"; shared_pending=f"COLDWAR_CUB_bilat_{p}_offer_pending"; shared_open=f"COLDWAR_CUB_bilat_{p}_offer_open"
        unpaid_guard=f"NOT = {{ has_country_flag = {paid} }}"
        guard=f"has_country_flag = {pending} has_country_flag = {shared_pending} CUB = {{ has_country_flag = {opened} has_country_flag = {shared_open} COLDWAR_CUB_pair_{p}_clear = yes NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{p}_package_signed }} }} CUB = {{ COLDWAR_CUB_pair_{p}_clear = yes }}"
        effect_preview=f"if = {{ limit = {{ {unpaid_guard} }} set_temp_variable = {{ treasury_change = -{data['cost_partner']} }} modify_treasury_effect = yes CUB = {{ set_temp_variable = {{ treasury_change = -{data['cost_cub']} }} modify_treasury_effect = yes }} }} add_ideas = {tid}_{p} CUB = {{ add_ideas = {tid}_cub }}"
        DECISIONS += f'''	COLDWAR_CUB_accept_bilat_{p}_{term} = {{
		icon = generic_diplomacy visible = {{ has_country_flag = {pending} }} available = {{ {guard} }}
		cost = 0 days_remove = 90
		complete_effect = {{
			effect_tooltip = {{ {effect_preview} }}
			hidden_effect = {{ if = {{ limit = {{ {guard} }}
			if = {{ limit = {{ {unpaid_guard} }}
				set_temp_variable = {{ treasury_change = -{data['cost_partner']} }} modify_treasury_effect = yes
				CUB = {{ set_temp_variable = {{ treasury_change = -{data['cost_cub']} }} modify_treasury_effect = yes set_country_flag = {paid} }}
				set_country_flag = {paid}
			}}
			set_country_flag = {signed} CUB = {{ set_country_flag = {signed} set_country_flag = COLDWAR_CUB_bilat_{p}_package_signed }}
			set_country_flag = COLDWAR_CUB_bilat_{p}_package_signed
			clr_country_flag = {pending} clr_country_flag = {shared_pending} CUB = {{ clr_country_flag = {opened} clr_country_flag = {shared_open} COLDWAR_CUB_reconcile_bilateral = yes country_event = {{ id = COLDWAR_CUB_bilateral.900 days = 1 }} }}
			}} }} }}
		ai_will_do = {{ base = 4 }}
	}}
	COLDWAR_CUB_refuse_bilat_{p}_{term} = {{
		icon = generic_diplomacy visible = {{ has_country_flag = {pending} has_country_flag = {shared_pending} }} available = {{ has_country_flag = {pending} has_country_flag = {shared_pending} CUB = {{ has_country_flag = {opened} has_country_flag = {shared_open} }} }}
		cost = 0 days_remove = 90
		complete_effect = {{ if = {{ limit = {{ has_country_flag = {pending} has_country_flag = {shared_pending} CUB = {{ has_country_flag = {opened} has_country_flag = {shared_open} }} }} clr_country_flag = {pending} clr_country_flag = {shared_pending} set_country_flag = {{ flag = COLDWAR_CUB_bilat_{p}_refused value = 1 days = 90 }} CUB = {{ clr_country_flag = {opened} clr_country_flag = {shared_open} set_country_flag = {{ flag = COLDWAR_CUB_bilat_{p}_refused value = 1 days = 90 }} }} }} }}
		ai_will_do = {{ base = 1 }}
	}}
	COLDWAR_CUB_cancel_bilat_{p}_{term}_as_partner = {{
		icon = generic_diplomacy visible = {{ tag = {tag} has_country_flag = {signed} CUB = {{ has_country_flag = {signed} }} }}
		available = {{ tag = {tag} has_country_flag = {signed} CUB = {{ has_country_flag = {signed} }} }}
		cost = 0 days_re_enable = 1 complete_effect = {{ if = {{ limit = {{ has_country_flag = {signed} CUB = {{ has_country_flag = {signed} }} }} CUB = {{ COLDWAR_CUB_cancel_{p}_{term} = yes }} }} }} ai_will_do = {{ base = 0 }}
	}}
'''
DECISIONS += r'''	COLDWAR_CUB_cancel_medical_treaty_as_partner = {
		icon = generic_diplomacy visible = { has_country_flag = COLDWAR_CUB_medical_mission_signed CUB = { has_country_flag = COLDWAR_CUB_medical_mission_signed } }
		available = { has_country_flag = COLDWAR_CUB_medical_mission_signed CUB = { has_country_flag = COLDWAR_CUB_medical_mission_signed } }
		cost = 0 days_re_enable = 1 complete_effect = { COLDWAR_CUB_cancel_medical_mission = yes } ai_will_do = { base = 0 }
	}
	COLDWAR_CUB_cancel_interests_sections_as_partner = {
		icon = generic_diplomacy visible = { tag = USA has_country_flag = COLDWAR_CUB_history_interests_sections_active CUB = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } }
		available = { tag = USA has_country_flag = COLDWAR_CUB_history_interests_sections_active CUB = { has_country_flag = COLDWAR_CUB_history_interests_sections_active } }
		cost = 0 days_re_enable = 1 complete_effect = { CUB = { COLDWAR_CUB_cancel_interests_sections = yes } } ai_will_do = { base = 0 }
	}
}
'''

CATEGORIES = r'''# IMPERIA COLD WAR — bilateral treaty decision categories.
COLDWAR_CUB_bilateral_offers = {
	allowed = { tag = CUB IMP_is_1970_scenario = yes }
	icon = generic_diplomacy
	priority = 206
	visible = { OR = { has_completed_focus = COLDWAR_CUB_island_diplomacy has_completed_focus = COLDWAR_CUB_moscow_guarantee has_country_flag = COLDWAR_CUB_medical_targeting_enabled has_country_flag = COLDWAR_CUB_history_interests_sections_active has_country_flag = COLDWAR_CUB_history_interests_sections_seen } }
}
COLDWAR_CUB_bilateral_responses = {
	allowed = { NOT = { tag = CUB } }
	icon = generic_diplomacy
	priority = 211
	visible = { OR = { has_country_flag = COLDWAR_CUB_bilat_sov_offer_pending has_country_flag = COLDWAR_CUB_bilat_sov_commodity_offer_pending has_country_flag = COLDWAR_CUB_bilat_sov_industry_offer_pending has_country_flag = COLDWAR_CUB_bilat_mex_offer_pending has_country_flag = COLDWAR_CUB_bilat_mex_energy_offer_pending has_country_flag = COLDWAR_CUB_bilat_mex_agro_offer_pending has_country_flag = COLDWAR_CUB_bilat_spr_offer_pending has_country_flag = COLDWAR_CUB_bilat_spr_nickel_offer_pending has_country_flag = COLDWAR_CUB_bilat_spr_training_offer_pending has_country_flag = COLDWAR_CUB_bilat_can_offer_pending has_country_flag = COLDWAR_CUB_bilat_can_rail_offer_pending has_country_flag = COLDWAR_CUB_bilat_can_industry_offer_pending has_country_flag = COLDWAR_CUB_bilat_sov_commodity_signed has_country_flag = COLDWAR_CUB_bilat_sov_industry_signed has_country_flag = COLDWAR_CUB_bilat_mex_energy_signed has_country_flag = COLDWAR_CUB_bilat_mex_agro_signed has_country_flag = COLDWAR_CUB_bilat_spr_nickel_signed has_country_flag = COLDWAR_CUB_bilat_spr_training_signed has_country_flag = COLDWAR_CUB_bilat_can_rail_signed has_country_flag = COLDWAR_CUB_bilat_can_industry_signed has_country_flag = COLDWAR_CUB_medical_mission_signed has_country_flag = COLDWAR_CUB_history_interests_sections_active has_country_flag = COLDWAR_CUB_soviet_assistance_signed has_country_flag = COLDWAR_CUB_symbolic_cooperation_signed } }
}
'''

LOC = "l_english:\n"
for p,spec in PARTNERS.items():
    for term,data in spec["terms"].items():
        n=offer_number(p,term); tid=term_id(p,term); label=data["label"]
        flavour = FLAVOUR[f"{p}_{term}"]
        condition = "The standing terms operate only while both governments remain at peace and free of mutual sanctions; either government may terminate the agreement."
        early = " If concluded before the documented precedent, this is an alternate-history early agreement."
        LOC += f' COLDWAR_CUB_bilateral.{n}.t:0 "Cuba–{spec["label"]}: {label}"\n COLDWAR_CUB_bilateral.{n}.d:0 "{flavour["proposal"]}{early} {condition}"\n'
        LOC += f' {tid}_cub:0 "Cuban {label}"\n {tid}_cub_desc:0 "{flavour["cub"]} {condition}"\n {tid}_{p}:0 "{spec["label"]} {label}"\n {tid}_{p}_desc:0 "{flavour["partner"]} {condition}"\n'
        LOC += f' COLDWAR_CUB_offer_{p}_{term}:0 "Propose {label}"\n COLDWAR_CUB_cancel_bilat_{p}_{term}:0 "Terminate {label}"\n COLDWAR_CUB_accept_bilat_{p}_{term}:0 "Accept {label}"\n COLDWAR_CUB_refuse_bilat_{p}_{term}:0 "Decline {label}"\n COLDWAR_CUB_cancel_bilat_{p}_{term}_as_partner:0 "Terminate {label}"\n'
LOC += r''' COLDWAR_CUB_bilateral.review:0 "Review the proposal in the diplomatic decisions."
 COLDWAR_CUB_bilateral.900.t:0 "Bilateral Agreement Ratified"
 COLDWAR_CUB_bilateral.900.d:0 "Both governments have entered the negotiated agreement. Its provisions will operate while the bilateral conditions remain in force."
 COLDWAR_CUB_medical_mission_cub:0 "International Medical Cooperation Programme"
 COLDWAR_CUB_medical_mission_cub_desc:0 "A standing medical cooperation programme with one or more consenting partners, active only while each bilateral relationship remains eligible."
 COLDWAR_CUB_medical_mission_partner:0 "Cuban Medical Mission Agreement"
 COLDWAR_CUB_medical_mission_partner_desc:0 "A standing, recipient-approved medical mission agreement with Cuba."
 COLDWAR_CUB_soviet_assistance_sov:0 "Soviet–Cuban Technical Assistance"
 COLDWAR_CUB_soviet_assistance_sov_desc:0 "A continuing programme of technical assistance with Cuba, subject to bilateral peace and sanctions conditions."
 COLDWAR_CUB_symbolic_cooperation_ddr:0 "Playa RDA Scientific Cooperation"
 COLDWAR_CUB_symbolic_cooperation_ddr_desc:0 "A continuing cultural and scientific exchange with Cuba."
 COLDWAR_CUB_interests_sections_cub:0 "Cuban–American Interests Sections"
 COLDWAR_CUB_interests_sections_cub_desc:0 "Reciprocal diplomatic representation, active while bilateral peace and sanctions conditions permit."
 COLDWAR_CUB_interests_sections_usa:0 "American–Cuban Interests Sections"
 COLDWAR_CUB_interests_sections_usa_desc:0 "Reciprocal diplomatic representation, active while bilateral peace and sanctions conditions permit."
 COLDWAR_CUB_end_medical_treaty_target:0 "Terminate the Medical Mission Agreement"
 COLDWAR_CUB_cancel_medical_treaty_as_partner:0 "Terminate the Medical Mission Agreement"
 COLDWAR_CUB_end_interests_sections:0 "Close the Interests Sections Agreement"
 COLDWAR_CUB_reopen_interests_sections:0 "Renew the Interests Sections Proposal"
 COLDWAR_CUB_cancel_interests_sections_as_partner:0 "Close the Interests Sections Agreement"
'''

def write(rel, data, bom=False):
    from file_headers import stamp
    data=stamp(data,'Cuba 1970 bilateral agreements.',localisation=bom)
    path=ROOT/rel; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8-sig" if bom else "utf-8"))

def main():
    write("common/scripted_effects/COLDWAR_CUB_1970_bilateral.txt", EFFECTS)
    write("common/scripted_triggers/COLDWAR_CUB_1970_bilateral.txt", TRIGGERS)
    write("common/ideas/COLDWAR_CUB_1970_bilateral_ideas.txt", IDEAS)
    write("common/decisions/COLDWAR_CUB_1970_bilateral.txt", DECISIONS)
    write("common/decisions/categories/COLDWAR_CUB_1970_bilateral.txt", CATEGORIES)
    write("events/COLDWAR_CUB_1970_bilateral.txt", EVENTS)
    write("localisation/english/COLDWAR_CUB_1970_bilateral_l_english.yml", LOC, bom=True)

if __name__ == "__main__": main()
