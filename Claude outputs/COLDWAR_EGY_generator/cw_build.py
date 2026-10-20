# COLDWAR | Writes every mod file of the Egypt 1970 tree. Run: python3 cw_build.py
import os, re, json, shutil, collections
import cw_compile as C
from cw_compile import write, block, HEADER, LOC
from cw_common import *
import cw_effects as E
from cw_effects import R
import cw_events as EV
import cw_october as OCT

shutil.rmtree(C.OUT, ignore_errors=True)

# ---------------------------------------------------------------- focus tree (collect first)
FOCUS_TXT = C.focus_file()
for f in C.FOCI:
    fid = cid(f["id"])
    LOC[fid] = f["name"]
    LOC[fid + "_desc"] = C.DESC[f["id"]].replace('"', "'")

# ---------------------------------------------------------------- start spirits and offer ideas
START = {
    "Shadow of the Naksa": [("stability_factor", -0.05), ("army_morale_factor", -0.10), ("war_support_factor", 0.05)],
    "The Closed Canal": [("tax_gain_multiplier_modifier", -0.04), ("office_park_income_tax_modifier", -0.05)],
    "Soviet Military Mission": [("enemy_army_bonus_air_superiority_factor", -0.15), ("training_time_factor", -0.10), ("foreign_influence_defense_modifier", -0.15)],
    "The Mugamma": [("bureaucracy_cost_multiplier_modifier", 0.15), ("political_power_factor", 0.05), ("productivity_growth_modifier", -0.05)],
    "War of Attrition Economy": [("production_speed_buildings_factor", -0.05), ("conscription", 0.005)],
}
for n, m in START.items():
    E.reg_idea(n, m, start=True)
OFFER_IDEAS = {
    "American Aid": ([("tax_gain_multiplier_modifier", 0.03)], 1095),
    "US Strategic Partner": ([("training_time_factor", -0.05), ("international_market_purchase_modifier", -0.10)], None),
    "Gulf Capital": ([("receiving_investment_cost_modifier", -0.10)], 1095),
    "Nile Water Agreement": ([("agricolture_productivity_modifier", 0.03)], 1825),
    "Comecon Member": ([("production_factory_efficiency_gain_factor", 0.05), ("globalism_equilibrium", -10)], None),
    "American Wheat": ([("stability_factor", 0.05)], 1095),
    "Joint Nile Authority": ([("agricolture_productivity_modifier", 0.03)], 1825),
    "FAR Member": ([("trade_opinion_factor", 0.15), ("research_speed_factor", 0.02)], None),
    "Nile Valley Union": ([("agriculture_tax_modifier", 0.05)], 1825),
    "Operation Kavkaz": ([("enemy_army_bonus_air_superiority_factor", -0.20)], None),
    "Gulf Investment": ([("receiving_investment_duration_modifier", -0.10)], 1825),
    "Joint Arab Command": ([("army_org_factor", 0.03), ("planning_speed", 0.05)], None),
    "Bread Riots": ([("stability_factor", -0.10)], 180),
    "Year of Mourning": ([("stability_factor", -0.03), ("war_support_factor", 0.05)], 180),
    "October Coalition": ([("war_support_factor", 0.05)], None),
}
for n, (m, d) in OFFER_IDEAS.items():
    E.reg_idea(n, m, d)
assert E.idea_id("US Strategic Partner") == "COLDWAR_EGY_us_strategic_partner"

PIC = {  # idea -> picture (GFX_idea_ is added)
    "shadow_of_the_naksa": "egy_otdate_army_idea", "the_closed_canal": "suez_canal_blocked", "soviet_military_mission": "soviet_advisors",
    "the_mugamma": "ETH_corrupt_bureaucracy", "war_of_attrition_economy": "egy_broken_economy_idea",
    "upheaval_from_below": "generic_civil_unrest", "the_raiss_fragile_health": "health_care", "palace_purges": "generic_purge",
    "neither_east_nor_west": "neutrality", "eastward_course": "communism", "westward_turn": "democracy", "the_islamic_awakening": "islam",
    "misr_awwalan": "pharaonism_idea", "transition_of_power": "Presidential_republic", "non_aligned_republic": "neutrality2",
    "competing_patrons": "generic_partnership", "third_world_champion": "egypt_flag_spir", "progressive_front": "communism2",
    "peoples_militias": "pmr_people_militia", "socialist_egypt": "democratic_socialism", "open_door_republic": "foreign_capital",
    "partner_of_the_west": "pro-american", "islamic_government": "islamic_world", "dar_al_islam": "true_caliphate",
    "officers_republic": "egy_corrupt_army_idea", "war_economy": "national_mobilization", "egypt_above_all": "nationalism",
    "a_nation_in_arms": "national_defenders", "redistribution_disruption": "agricultural_reforms", "second_five_year_plan": "sov_five_year_idea",
    "population_council": "population_stagnation", "shock_therapy": "market_liberalism", "purged_command": "generic_purge",
    "five_year_plan_soviet_template": "sov_five_year_idea", "mass_mobilisation": "national_mobilization", "revolutionary_upheaval": "revolutionary_army",
    "zili_gengsheng": "ser_autarky_idea", "collectivisation": "gre_agricultural_communes", "factory_occupations": "factory_strikes",
    "red_militias": "generic_militia", "islamic_militia": "generic_militia_bonus", "revolutionary_guard": "guarde_javid",
    "resistance_economy": "axis_of_resistance", "american_military_aid": "american_militarism", "liberalisation_shock": "market_dynamics",
    "purged_army": "army_bad_officer", "siege_economy": "GER_autarky", "emirate_war_economy": "an_algerian_emirate", "mujahidin": "foreign_jihadis",
    "total_mobilisation": "war_support_boost", "green_shirts": "nationalist_outlook", "youth_battalions": "nko_red_youth_guard_idea",
    "command_economy": "State_led_economy", "national_guard": "egy_special_force", "revolutionary_autarky": "ser_autarky_idea",
    "raiding_parties": "egy_special_force", "operation_badr": "army_dominant", "spirit_of_the_crossing": "egypt_flag_spir",
    "suez_canal_authority": "full_control_of_suez", "armed_forces_day": "army_good_officer", "gulf_remittances": "saudi_expat",
    "pivot_of_the_cold_war": "generic_partnership", "front_austerity": "egy_imf_idea", "egyptian_model_socialism": "democratic_socialism",
    "egyptian_model_infitah": "market_liberalism", "egyptian_model_islamic_economy": "islamic_world", "the_high_dam": "hydroelectric",
    "family_planning_council": "population_stagnation", "strength_of_numbers": "population_growth", "gift_of_the_nile": "agriculture",
    "industrial_heartland": "egy_vpk_idea", "graduates_in_uniform": "officer_military_academy", "air_defence_forces": "ukr_antiair_missile_troops_idea",
    "bilbeis_air_academy": "air_bonus", "army_of_the_crossing": "army_dominant", "american_aid": "pro-american", "us_strategic_partner": "pro-american",
    "gulf_capital": "saudi_aid", "nile_water_agreement": "water_conservation", "comecon_member": "communism3", "american_wheat": "Stabilized_Food_Supply",
    "joint_nile_authority": "water_conservation", "far_member": "arab_workers_union", "nile_valley_union": "agriculture", "operation_kavkaz": "soviet_advisors",
    "gulf_investment": "foreign_capital", "joint_arab_command": "army_planning", "bread_riots": "generic_civil_unrest", "year_of_mourning": "egypt_flag_spir",
    "air_force_rearmament": "air_industry", "the_badr_plan": "war_support_boost", "october_coalition": "army_planning",
}
IDEA_GFX = set(open("idea_gfx.txt").read().split())


def ideas_file():
    L = [HEADER, "ideas = {", "country = {"]
    for iid, d in R.ideas.items():
        s = iid.replace(PFX, "")
        pic = PIC.get(s, "egypt_flag_spir")
        assert pic in IDEA_GFX, (iid, pic)
        LOC[iid] = d["name"].replace("Egyptian Model: ", "Egyptian Model: ")
        L += [f"{iid} = {{", f"picture = {pic}", "allowed = { always = no }", "allowed_civil_war = { always = yes }", "modifier = {"]
        for k, v in d["mods"]:
            L.append(f"{k} = {fmt(v)}")
        L.append("}")
        tg = collections.defaultdict(list)
        for tag, k, v in OCT.TARGETED.get(iid, []):
            tg[tag].append(f"{k} = {fmt(v)}")
        for tag, lines in tg.items():
            L += ["targeted_modifier = {", f"tag = {tag}"] + lines + ["}"]
        L.append("}")
    L += ["}", "}"]
    return "\n".join(block(L)) + "\n"


IDEAS_TXT = ideas_file()

# ---------------------------------------------------------------- dynamic modifiers
DYN_ICON = {"state": "GFX_idea_egypt_flag_spir", "economy": "GFX_idea_egy_broken_economy_idea", "armed_forces": "GFX_idea_egy_otdate_army_idea"}
PROG_ICON = {"asu": "egypt_flag_spir", "tp": "Presidential_republic", "mb": "islamic_world", "tag": "communism4", "fc": "market_dynamics",
             "nb": "family_supports", "fe": "market_liberalism", "fn": "water_conservation", "cp": "communism", "ecp": "communism2",
             "wc": "factory_strikes", "misr": "egy_police_idea", "irf": "revolutionary_iran", "grd": "guarde_javid", "ndp": "democracy",
             "wafd": "democratic_party", "lib": "social_liberalism", "slp": "democratic_socialism", "azh": "the_ulema", "ij": "true_caliphate",
             "arm": "army_dominant", "ye": "nationalism", "rcc": "fascism", "mon": "monarchy"}
PARTY_TRIGGER = {}
for f in C.FOCI:
    if f["sec"] in C.PARTY_OF_SEC and f["av"].startswith("`") and f["av"].endswith("_are_in_power`"):
        PARTY_TRIGGER.setdefault(f["sec"], f["av"].strip("`"))
SEC_KEY = {"cop": "cp"}  # design programme key differs from section key for the Vanguard


def dyn_file():
    L = [HEADER.rstrip("\n")]
    names = {"state": "The Egyptian State", "economy": "The Egyptian Economic Model", "armed_forces": "The Egyptian Armed Forces"}
    for g in ("state", "economy", "armed_forces"):
        L += ["", f"{PFX}{g}_modifier = {{", f"icon = {DYN_ICON[g]}", ""]
        for k in R.dyn.get(g, []):
            L.append(f"{k} = {PFX}{g}_{k}")
        L.append("}")
        LOC[f"{PFX}{g}_modifier"] = names[g]
    for sec, idx in C.PARTY_OF_SEC.items():
        key = SEC_KEY.get(sec, sec)
        g = f"{key}_programme"
        if g not in R.dyn:
            continue
        L += ["", f"{PFX}{key}_programme = {{", f"icon = GFX_idea_{PROG_ICON[key]}", "",
              "enable = {", "IMP_is_1970_scenario = yes", f"{PARTY_TRIGGER[sec]} = yes", "}", ""]
        for k in R.dyn[g]:
            L.append(f"{k} = {PFX}{g}_{k}")
        L.append("}")
        LOC[f"{PFX}{key}_programme"] = "Programme: " + re.sub(r"^Partei: |\s*\(\d+\)$", "", C.SECT[sec]["title"])
    for k in R.dyn:
        if k.endswith("_programme"):
            assert any(SEC_KEY.get(s, s) + "_programme" == k for s in C.PARTY_OF_SEC), k
    return "\n".join(block(L)) + "\n"


DYN_TXT = dyn_file()

# ---------------------------------------------------------------- opinion modifiers
def opinion_file():
    L = [HEADER, "opinion_modifiers = {"]
    for mid, v in sorted(R.opinions.items()):
        L += [f"{mid} = {{", f"value = {v}", "decay = 0.5" if abs(v) >= 20 else "decay = 0.25", "}"]
        LOC[mid] = ("Egyptian Diplomacy" if v > 0 else "Egyptian Snub")
    extra = {"COLDWAR_EGY_partnership": (25, "Egyptian Partnership"), "COLDWAR_EGY_peace_treaty": (30, "Peace Treaty with Egypt"),
             "COLDWAR_EGY_alliance_of_scholars": (30, "Alliance of the Scholars"), "COLDWAR_EGY_alliance_of_crowns": (30, "Alliance of Crowns"),
             "COLDWAR_EGY_arab_solidarity": (15, "Arab Solidarity"), "COLDWAR_EGY_peace_effort": (10, "Peace Effort"),
             "COLDWAR_EGY_separate_peace": (-30, "Separate Peace with Israel"), "COLDWAR_EGY_us_peace_ally": (25, "Peace with Israel")}
    for mid, (v, n) in extra.items():
        L += [f"{mid} = {{", f"value = {v}", "}"]
        LOC[mid] = n
    L.append("}")
    return "\n".join(block(L)) + "\n"


OPINION_TXT = opinion_file()

# ---------------------------------------------------------------- traits
TRAITS = {
    "COLDWAR_EGY_field_marshal": ("Field Marshal", ["army_org_factor = 0.05", "political_power_factor = 0.05"]),
    "COLDWAR_EGY_air_force_hero": ("Hero of the Air Force", ["air_superiority_efficiency = 0.05", "stability_factor = 0.03"]),
    "COLDWAR_EGY_technocrat_in_chief": ("Technocrat-in-Chief", ["bureaucracy_cost_multiplier_modifier = -0.05", "productivity_growth_modifier = 0.02"]),
    "COLDWAR_EGY_ailing_rais": ("Ailing Rais", ["political_power_factor = 0.10", "stability_factor = 0.03"]),
    "COLDWAR_EGY_consolidated_rule": ("Consolidated Rule", ["political_power_factor = 0.05", "stability_factor = 0.02"]),
    "COLDWAR_EGY_rais_for_life": ("Rais for Life", ["political_power_factor = 0.10"]),
}


def traits_file():
    L = [HEADER, "leader_traits = {"]
    for t, (n, mods) in TRAITS.items():
        L += [f"{t} = {{", "random = no", ""] + mods + ["}"]
        LOC[t] = n
    L.append("}")
    return "\n".join(block(L)) + "\n"


TRAITS_TXT = traits_file()

# ---------------------------------------------------------------- scripted triggers
TRIGGERS_TXT = HEADER + """
COLDWAR_EGY_is_arab_league_state = {
	is_in_array = { global.arabic_countries = THIS.id }
}

# Emerging outlook (vanilla ideology communism) at 12% or more
COLDWAR_EGY_outlook_at_least_emerging_12 = {
	communism > 0.119
}
"""
LOC["COLDWAR_EGY_outlook_emerging_12_tt"] = "The §YEmerging§! outlook has at least §Y12%§! popularity."

# ---------------------------------------------------------------- scripted effects
def offers_effects():
    L = []
    for short in sorted(R.offers):
        o = EV.OFFERS[short]
        n = o["n"]
        LOC[f"{PFX}offer_{short}_tt"] = f"We send a proposal to {', '.join('[' + t + '.GetNameDef]' for t in o['targets'] if t != 'FACTION') or 'our faction partners'}. §YThey decide§! whether to accept; its terms take effect only then."
        L += [f"{PFX}offer_{short} = {{", f"custom_effect_tooltip = {PFX}offer_{short}_tt", "hidden_effect = {"]
        if o["targets"] == ["FACTION"]:
            L += ["every_country = {", "limit = { is_in_faction_with = ROOT NOT = { tag = ROOT } }", f"country_event = {{ id = {NS}.{n} days = 1 }}", "}"]
        else:
            for t in o["targets"]:
                L += [f"if = {{ limit = {{ country_exists = {t} }}", f"{t} = {{ country_event = {{ id = {NS}.{n} days = 1 }} }}", "}"]
        L += ["}", "}", ""]
    return L


EFFECTS = f"""{HEADER}
# ---- initialisation (called from the 1970 history block) --------------------------------------
COLDWAR_EGY_initialize_1970 = {{
	if = {{
		limit = {{ NOT = {{ has_country_flag = COLDWAR_EGY_initialized }} }}
		set_country_flag = COLDWAR_EGY_initialized
		# MD helpers only work on existing law and faction ideas
		add_ideas = {{
			bureau_03
			defence_05
			police_04
			edu_03
			health_02
			social_03
			the_military
			intelligence_community
			labour_unions
			farmers
			the_ulema
			COLDWAR_EGY_shadow_of_the_naksa
			COLDWAR_EGY_the_closed_canal
			COLDWAR_EGY_soviet_military_mission
			COLDWAR_EGY_the_mugamma
			COLDWAR_EGY_war_of_attrition_economy
		}}
		set_variable = {{ the_military_opinion = 70 }}
		set_variable = {{ intelligence_community_opinion = 65 }}
		set_variable = {{ labour_unions_opinion = 55 }}
		set_variable = {{ farmers_opinion = 60 }}
		set_variable = {{ the_ulema_opinion = 45 }}
		initialize_internal_faction_dynamic_modifiers = yes
	}}
}}

# ---- money as a share of GDP (temp COLDWAR_EGY_gdp_share, positive) ----------------------------
COLDWAR_EGY_pay_gdp_share = {{
	set_temp_variable = {{ treasury_change = gdp_total }}
	multiply_temp_variable = {{ treasury_change = COLDWAR_EGY_gdp_share }}
	multiply_temp_variable = {{ treasury_change = -1 }}
	modify_treasury_effect = yes
}}

COLDWAR_EGY_receive_gdp_share = {{
	set_temp_variable = {{ treasury_change = gdp_total }}
	multiply_temp_variable = {{ treasury_change = COLDWAR_EGY_gdp_share }}
	set_variable = {{ COLDWAR_EGY_last_transfer = treasury_change }}
	modify_treasury_effect = yes
}}

# signed share
COLDWAR_EGY_change_debt_gdp_share = {{
	set_temp_variable = {{ debt_change = gdp_total }}
	multiply_temp_variable = {{ debt_change = COLDWAR_EGY_gdp_share }}
	modify_debt_effect = yes
}}

COLDWAR_EGY_change_intinv_gdp_share = {{
	set_temp_variable = {{ int_investment_change = gdp_total }}
	multiply_temp_variable = {{ int_investment_change = COLDWAR_EGY_gdp_share }}
	modify_international_investment_effect = yes
}}

# ---- internal factions: exact values (MD doubles positive gains for autocracies) ----------------
COLDWAR_EGY_prepare_exact_opinion = {{
	set_temp_variable = {{ COLDWAR_EGY_requested_opinion = temp_opinion }}
	if = {{
		limit = {{
			check_variable = {{ temp_opinion > 0 }}
			OR = {{
				check_variable = {{ ruling_party = 0 }}
				check_variable = {{ ruling_party = 7 }}
				check_variable = {{ ruling_party = 13 }}
				check_variable = {{ ruling_party = 21 }}
				check_variable = {{ ruling_party = 22 }}
			}}
		}}
		multiply_temp_variable = {{ temp_opinion = 0.5 }}
	}}
}}

COLDWAR_EGY_restore_exact_opinion = {{
	set_temp_variable = {{ temp_opinion = COLDWAR_EGY_requested_opinion }}
}}
"""
for fac in ["the_military", "intelligence_community", "labour_unions", "farmers", "the_ulema", "communist_cadres",
            "small_medium_business_owners", "landowners", "oligarchs", "industrial_conglomerates"]:
    EFFECTS += f"""
COLDWAR_EGY_change_{fac}_opinion_exact = {{
	COLDWAR_EGY_prepare_exact_opinion = yes
	change_{fac}_opinion = yes
	COLDWAR_EGY_restore_exact_opinion = yes
}}
"""
OUTLOOK_PARTY = {0: (0, 3), 1: (4, 9), 2: (10, 11), 3: (12, 19), 4: (20, 23)}
DEFAULT_PARTY = {0: 0, 1: 7, 2: 10, 3: 18, 4: 22}
EFFECTS += """
# ---- outlook popularity: boosts the ruling party when it belongs to the outlook,
# ---- otherwise the outlook's main Egyptian party (temp COLDWAR_EGY_outlook_id / _amount)
COLDWAR_EGY_change_outlook_popularity = {
"""
for oid, (a, b) in OUTLOOK_PARTY.items():
    EFFECTS += f"""	if = {{
		limit = {{ check_variable = {{ COLDWAR_EGY_outlook_id = {oid} }} }}
		if = {{
			limit = {{ check_variable = {{ ruling_party > {a - 1} }} check_variable = {{ ruling_party < {b + 1} }} }}
			set_temp_variable = {{ party_index = ruling_party }}
		}}
		else = {{ set_temp_variable = {{ party_index = {DEFAULT_PARTY[oid]} }} }}
	}}
"""
EFFECTS += """	set_temp_variable = { party_popularity_increase = COLDWAR_EGY_outlook_amount }
	set_temp_variable = { temp_outlook_increase = COLDWAR_EGY_outlook_amount }
	change_relative_party_popularity = yes
}

COLDWAR_EGY_influence_arab_league = {
	custom_effect_tooltip = COLDWAR_EGY_influence_arab_league_tt
	every_country = {
		limit = { COLDWAR_EGY_is_arab_league_state = yes NOT = { tag = ROOT } }
		set_temp_variable = { tag_index = ROOT.id }
		set_temp_variable = { influence_target = THIS.id }
		set_temp_variable = { percent_change = COLDWAR_EGY_influence_amount }
		change_influence_percentage = yes
	}
}

COLDWAR_EGY_set_regulation_law_minimal = { add_ideas = minimal_regulations }
COLDWAR_EGY_set_regulation_law_light = { add_ideas = light_regulations }
COLDWAR_EGY_set_environment_law_partial = { add_ideas = partial_environmental_protections }

# ---- Nasser ------------------------------------------------------------------------------------
COLDWAR_EGY_nasser_dies = {
	set_country_flag = COLDWAR_EGY_nasser_deceased
	clr_country_flag = COLDWAR_EGY_nasser_ailing
	if = { limit = { has_idea = COLDWAR_EGY_the_raiss_fragile_health } remove_ideas = COLDWAR_EGY_the_raiss_fragile_health }
	add_timed_idea = { idea = COLDWAR_EGY_year_of_mourning days = 180 }
	custom_effect_tooltip = COLDWAR_EGY_nasser_dies_tt
	hidden_effect = {
		retire_country_leader = yes
		if = {
			limit = { NOT = { has_country_flag = COLDWAR_EGY_succession_decided } }
			create_country_leader = { name = "Anwar as-Sadat" picture = "gfx/leaders/EGY/1970/sadat.dds" ideology = neutral_Social traits = { neutrality_neutral_Social } }
		}
	}
}

# ---- war and peace with Israel (THIS = Israel, FROM = Egypt) ------------------------------------
# Ceasefire on the current line, as MD's conditional peace does it: occupied states change owner, then white peace.
COLDWAR_EGY_ceasefire_status_quo = {
	FROM = {
		every_owned_state = {
			limit = { is_controlled_by = ROOT }
			ROOT = { transfer_state = PREV }
		}
	}
	every_owned_state = {
		limit = { is_controlled_by = FROM }
		FROM = { transfer_state = PREV }
	}
	if = { limit = { has_war_with = FROM } white_peace = FROM }
}

COLDWAR_EGY_ceasefire_accepted = {
	set_country_flag = COLDWAR_EGY_ceasefire
	add_stability = 0.05
	add_war_support = -0.05
	if = { limit = { country_exists = USA } USA = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_EGY_peace_effort } } }
}

COLDWAR_EGY_return_sinai = {
	if = {
		limit = { 213 = { OR = { is_owned_by = ROOT is_controlled_by = ROOT } } }
		FROM = { transfer_state = 213 }
	}
}

COLDWAR_EGY_peace_with_israel_consequences = {
	if = { limit = { country_exists = USA } USA = { add_opinion_modifier = { target = ROOT modifier = COLDWAR_EGY_us_peace_ally } } }
	every_country = {
		limit = { COLDWAR_EGY_is_arab_league_state = yes NOT = { tag = ROOT } }
		add_opinion_modifier = { target = ROOT modifier = COLDWAR_EGY_separate_peace }
	}
	country_event = { id = COLDWAR_EGY.8 days = 14 }
}

# Cairo Agreement (THIS = Jordan or the Palestinians, FROM = Egypt)
COLDWAR_EGY_cairo_agreement_signed = {
	if = { limit = { tag = JOR } FROM = { set_country_flag = COLDWAR_EGY_cairo_jor } }
	if = { limit = { tag = PAL } FROM = { set_country_flag = COLDWAR_EGY_cairo_pal } }
	add_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_partnership }
	if = {
		limit = { FROM = { has_country_flag = COLDWAR_EGY_cairo_jor has_country_flag = COLDWAR_EGY_cairo_pal } }
		if = {
			limit = { country_exists = JOR country_exists = PAL JOR = { has_war_with = PAL } }
			JOR = { white_peace = PAL }
		}
	}
	custom_effect_tooltip = COLDWAR_EGY_cairo_agreement_tt
}

# Arab Organisation for Industrialisation: each partner halves Egypt's remaining share (THIS = Egypt)
COLDWAR_EGY_aoi_cofinance = {
	if = { limit = { NOT = { has_variable = COLDWAR_EGY_aoi_share } } set_variable = { COLDWAR_EGY_aoi_share = 0.015 } }
	set_temp_variable = { COLDWAR_EGY_gdp_share = COLDWAR_EGY_aoi_share }
	multiply_temp_variable = { COLDWAR_EGY_gdp_share = 0.5 }
	subtract_from_variable = { COLDWAR_EGY_aoi_share = COLDWAR_EGY_gdp_share }
	COLDWAR_EGY_receive_gdp_share = yes
}

# yearly rent of the Soviet squadron (THIS = Egypt)
COLDWAR_EGY_eskadra_rent = {
	set_temp_variable = { COLDWAR_EGY_gdp_share = 0.005 }
	COLDWAR_EGY_receive_gdp_share = yes
	if = {
		limit = { country_exists = SOV }
		SOV = {
			set_temp_variable = { treasury_change = ROOT.COLDWAR_EGY_last_transfer }
			multiply_temp_variable = { treasury_change = -1 }
			modify_treasury_effect = yes
		}
	}
}

"""

EFFECTS += """
# ---- elections (MD keeps the ideology in set_politics and the variable disable_elections) -------
COLDWAR_EGY_allow_elections = {
	custom_effect_tooltip = COLDWAR_EGY_allow_elections_tt
	set_variable = { disable_elections = 0 }
	hidden_effect = {
		if = { limit = { has_government = democratic } set_politics = { ruling_party = democratic elections_allowed = yes } }
		if = { limit = { has_government = communism } set_politics = { ruling_party = communism elections_allowed = yes } }
		if = { limit = { has_government = fascism } set_politics = { ruling_party = fascism elections_allowed = yes } }
		if = { limit = { has_government = neutrality } set_politics = { ruling_party = neutrality elections_allowed = yes } }
		if = { limit = { has_government = nationalist } set_politics = { ruling_party = nationalist elections_allowed = yes } }
	}
}

COLDWAR_EGY_suspend_elections = {
	custom_effect_tooltip = COLDWAR_EGY_suspend_elections_tt
	set_variable = { disable_elections = 1 }
	hidden_effect = {
		if = { limit = { has_government = democratic } set_politics = { ruling_party = democratic elections_allowed = no } }
		if = { limit = { has_government = communism } set_politics = { ruling_party = communism elections_allowed = no } }
		if = { limit = { has_government = fascism } set_politics = { ruling_party = fascism elections_allowed = no } }
		if = { limit = { has_government = neutrality } set_politics = { ruling_party = neutrality elections_allowed = no } }
		if = { limit = { has_government = nationalist } set_politics = { ruling_party = nationalist elections_allowed = no } }
	}
}
"""
LOC["COLDWAR_EGY_allow_elections_tt"] = "§GElections are allowed.§!"
LOC["COLDWAR_EGY_suspend_elections_tt"] = "§RElections remain suspended.§!"
LOC["COLDWAR_EGY_influence_arab_league_tt"] = "Our influence grows in every member state of the §YArab League§!."
LOC["COLDWAR_EGY_nasser_dies_tt"] = "§RGamal Abdel Nasser dies.§!"
LOC["COLDWAR_EGY_cairo_agreement_tt"] = "Once both §YJordan§! and the §YPalestinians§! have signed, the fighting between them ends."

# fix the Cairo agreement accept code and offer dispatchers
EV.OFFERS["mediate_black_september"]["accept_code"] = "COLDWAR_EGY_cairo_agreement_signed = yes"
EFFECTS += "\n".join(block(offers_effects())) + "\n"


# ---------------------------------------------------------------- events
def ev_loc(eid, title, desc, opts):
    LOC[f"{eid}.t"] = title
    LOC[f"{eid}.d"] = desc
    for i, t in enumerate(opts):
        LOC[f"{eid}.{'abcdefgh'[i]}"] = t


def events_file():
    L = [HEADER, f"add_namespace = {NS}", ""]
    for key, e in sorted(EV.EVENTS.items(), key=lambda kv: kv[1]["n"]):
        eid = f"{NS}.{e['n']}"
        kind = "news_event" if e.get("news") else "country_event"
        L += [f"# COLDWAR | {key}", f"{kind} = {{", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d", f"picture = {e['pic']}", ""]
        if e.get("news"):
            L += ["major = yes"]
        trig = e.get("triggered")
        if trig:
            L += ["fire_only_once = yes", "trigger = {", "original_tag = EGY"] + trig["trigger"].split("\n") + ["}",
                  f"mean_time_to_happen = {{ days = {trig['mtth']} }}"]
            if key == "nasser_health":
                k = len(L) - 1 - L[::-1].index("fire_only_once = yes")
                L[k] = "# repeats every year or so while the ailing Nasser lives"
        else:
            L.append("is_triggered_only = yes")
        if e.get("hidden"):
            L.append("hidden = yes")
        if e.get("immediate"):
            L += ["", "immediate = {"] + e["immediate"].split("\n") + ["}"]
        if key == "lease":
            L += ["", "immediate = {", "if = {", "limit = { has_country_flag = COLDWAR_EGY_eskadra_lease }", "COLDWAR_EGY_eskadra_rent = yes",
                  f"country_event = {{ id = {eid} days = 365 }}", "}", "}"]
        L.append("")
        for i, (t, code, ai) in enumerate(e["options"]):
            L += ["option = {", f"name = {eid}.{'abcdefgh'[i]}", f"ai_chance = {{ base = {ai} }}"] + [c for c in code.split("\n") if c] + ["}"]
        L += ["}", ""]
        ev_loc(eid, e["title"], e["desc"], [o[0] for o in e["options"]])
    # Nasser's death (historical date) and the yearly health event
    L += [f"# COLDWAR | Nasser's death on 28 September 1970", "country_event = {", f"id = {NS}.13", f"title = {NS}.13.t", f"desc = {NS}.13.d",
          "picture = GFX_egy_flagg", "", "fire_only_once = yes", "trigger = {", "original_tag = EGY", "date > 1970.9.27",
          'has_country_leader = { name = "Gamal Abdel Nasser" ruling_only = yes }', "NOT = { has_country_flag = COLDWAR_EGY_nasser_ailing }",
          "}", "mean_time_to_happen = { days = 1 }", "", "option = {", f"name = {NS}.13.a", "COLDWAR_EGY_nasser_dies = yes", "}", "}", ""]
    ev_loc(f"{NS}.13", "The Rais Is Dead",
           "Hours after seeing off the last guests of the Arab summit that ended the fighting in Jordan, Gamal Abdel Nasser has died of a heart attack. "
           "Millions pour into the streets of Cairo in grief such as the Arab world has never seen. Vice President Anwar as-Sadat assumes the presidency for now, "
           "but the struggle for the succession has only begun.", ["Egypt mourns its Rais."])
    # offers
    for short in sorted(R.offers):
        o = EV.OFFERS[short]
        eid = f"{NS}.{o['n']}"
        L += [f"# COLDWAR | offer from focus {PFX}{short}", "country_event = {", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d",
              f"picture = {o['pic']}", "", "is_triggered_only = yes", ""]
        opts = [(o["accept"], o["accept_code"], o["ai_base"], o["ai_mods"]), (o["decline"], o["decline_code"], 100 - o["ai_base"], "")]
        for t, code, ai in o.get("extra_options", []):
            opts.append((t, code, ai, ""))
        for i, (t, code, ai, mods) in enumerate(opts):
            L += ["option = {", f"name = {eid}.{'abcdefgh'[i]}", "ai_chance = {", f"base = {ai}"] + [m for m in mods.split("\n") if m] + ["}"]
            L += [c for c in code.split("\n") if c]
            L.append(f"FROM = {{ country_event = {{ id = {NS}.{900 if i == 0 else 901} days = 1 }} }}")
            L.append("}")
        L += ["}", ""]
        ev_loc(eid, o["title"], o["desc"], [x[0] for x in opts])
    for n, t, d, a in [(900, "[From.GetNameDefCap] Accepts", "Our envoys report that [From.GetNameDef] has accepted our proposal. The agreed terms now take effect.", "Excellent."),
                       (901, "[From.GetNameDefCap] Declines", "[From.GetNameDefCap] has turned down our proposal. We will have to find another way.", "Unfortunate.")]:
        L += ["country_event = {", f"id = {NS}.{n}", f"title = {NS}.{n}.t", f"desc = {NS}.{n}.d", "picture = GFX_news_arab_conference", "",
              "is_triggered_only = yes", "", "option = {", f"name = {NS}.{n}.a", "}", "}", ""]
        ev_loc(f"{NS}.{n}", t, d, [a])
    return "\n".join(block(L)) + "\n"


EVENTS_TXT = events_file()
LOC[f"{PFX}oil_weapon_request_tt"] = "This is only a request. Whether the §YOil Weapon§! is used remains our own decision."

# ---------------------------------------------------------------- party names 1970 (cosmetic tags)
PARTY_ICON = {0: "£EGY_Autocracy_small", 1: "£EGY_conservatism", 2: "£generic_liberalism_small", 3: "£EGY_neutral_Social",
              4: "£EGY_Communist_State", 5: "£EGY_Neutral_Communism", 6: "£generic_Conservative_small", 7: "£generic_Autocracy_small",
              10: "£EGY_kingdom", 11: "£generic_Caliphate_small", 12: "£EGY_Neutral_Muslim_Brotherhood", 13: "£EGY_Neutral_Autocracy",
              15: "£EGY_oligarchism", 16: "£generic_Neutral_Libertarian_small", 17: "£EGY_Neutral_Green", 18: "£EGY_neutral_Social",
              19: "£EGY_em_Autocracy", 20: "£EGY_Conservative", 21: "£EGY_Nat_Fascism", 22: "£EGY_Nat_Autocracy", 23: "£EGY_Monarchist"}
import egy_dsl as DSL
for tag in ["EGY_UAR_1970"] + list(R.cosmetic):
    for i, sub in E.SUBIDEO.items():
        name = re.sub(r"\s*\([^)]*\)$", "", DSL.PARTY[i]).replace(" - ", " – ")
        icon = PARTY_ICON.get(i)
        LOC[f"{tag}.{sub}"] = f"{icon} {name}" if icon else name
for tag, (name, adj) in R.cosmetic.items():
    for ide in ["", "_democratic", "_communism", "_fascism", "_neutrality", "_nationalist"]:
        LOC[f"{tag}{ide}"] = name
        LOC[f"{tag}{ide}_DEF"] = "the " + name
        LOC[f"{tag}{ide}_ADJ"] = adj
FLAG_SRC = {"COLDWAR_EGY_KINGDOM": "EGY_AUTH_S_nationalist", "COLDWAR_EGY_PEOPLES_REPUBLIC": "EGY_AUTH_S_communism",
            "COLDWAR_EGY_ISLAMIC_STATE": "UAR_islamist", "COLDWAR_EGY_ISLAMIC_REPUBLIC": "EGY_AUTH_S_fascism"}
FLAGS = {}
for tag, src in FLAG_SRC.items():
    for sub in ["", "medium/", "small/"]:
        FLAGS[f"gfx/flags/{sub}{tag}.tga"] = f"/mnt/user-data/uploads/mdcoldwar/gfx/flags/{sub}{src}.tga"

# ---------------------------------------------------------------- tooltips
LOC.update(R.tt)
LOC.update(OCT.LOC)
VAN_MOD_LOC = set()
for line in open("/mnt/user-data/uploads/mdcoldwar/localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml", encoding="utf-8-sig"):
    m = re.match(r"^\s+(MODIFIER_[A-Z0-9_]+):", line)
    if m:
        VAN_MOD_LOC.add(m.group(1))


def resolve_tt(text):
    def rep(m):
        return E.tooltip_for(m.group(1))
    return re.sub(r"@TT:(\w+)@", rep, text)


FOCUS_TXT = resolve_tt(FOCUS_TXT)
EVENTS_TXT = resolve_tt(EVENTS_TXT)
EFFECTS = resolve_tt(EFFECTS)
for key, mod in E.NEW_MOD_TT.items():
    up = "MODIFIER_" + mod.upper()
    label = f"${up}$" if up in VAN_MOD_LOC else f"${mod}$"
    flat = mod in FLAT_KEYS
    LOC[key] = f"{label}: $RIGHT|+={'0' if mod.startswith('if_') else ('2' if flat else '%1')}$"

# ---------------------------------------------------------------- gfx
def gfx_files():
    a = ["spriteTypes = {"]
    b = ["spriteTypes = {"]
    for name, path in sorted(C.NEW_SPRITES.items()):
        a += ["\tspriteType = {", f'\t\tname = "{name}"', f'\t\ttexturefile = "{path}"', "\t}"]
        b += ["\tspriteType = {", f'\t\tname = "{name}_shine"', f'\t\ttexturefile = "{path}"', '\t\teffectFile = "gfx/FX/buttonstate.lua"']
        for rot in ("-90.0", "90.0"):
            b += ["\t\tanimation = {", f'\t\t\tanimationmaskfile = "{path}"', '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                  f"\t\t\tanimationrotation = {rot}", "\t\t\tanimationlooping = no", "\t\t\tanimationtime = 0.75", "\t\t\tanimationdelay = 0",
                  '\t\t\tanimationblendmode = "add"', '\t\t\tanimationtype = "scrolling"', "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
                  "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }", "\t\t}"]
        b += ["\t\tlegacy_lazy_load = no", "\t}"]
    a.append("}")
    b.append("}")
    hdr = "## COLDWAR | Egypt 1970 focus icons from gfx/interface/goals (mostly the coldwar folder), registered for the COLDWAR Egypt tree.\n"
    return hdr + "\n".join(a) + "\n", hdr + "\n".join(b) + "\n"


GFX, GFX_SHINE = gfx_files()

# ---------------------------------------------------------------- localisation
MD_LOC_KEYS = set()
for _f in __import__("glob").glob("/mnt/user-data/uploads/mdcoldwar/localisation/english/**/*.yml", recursive=True):
    for _l in open(_f, encoding="utf-8-sig", errors="replace"):
        _m = re.match(r"^\s+([^\s:#]+):\d*\s", _l)
        if _m:
            MD_LOC_KEYS.add(_m.group(1))


def loc_file():
    dup = [k for k in LOC if k in MD_LOC_KEYS]
    print("skipped existing loc keys:", dup)
    for k in dup:
        del LOC[k]
    out = ["l_english:", " # COLDWAR | Egypt 1970 (focus tree, ideas, events, tooltips). Generated - edit cw_compile.py / cw_build.py."]
    for k, v in LOC.items():
        v = str(v).replace("\n", "\\n").replace('"', "'")
        out.append(f' {k}:0 "{v}"')
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- history / fallback patches
HIST_SRC = "/mnt/user-data/uploads/mdcoldwar/history/countries/EGY - Egypt.txt"
hist = open(HIST_SRC, encoding="utf-8-sig").read()
assert "load_focus_tree = mdcw_1970_generic_focus" in hist or "COLDWAR_EGY_initialize_1970" in hist
hist = hist.replace("\t\tload_focus_tree = mdcw_1970_generic_focus\n",
                    "\t\tload_focus_tree = COLDWAR_EGY_1970_focus # COLDWAR | Egypt 1970 tree\n", 1)
if "COLDWAR_EGY_initialize_1970" not in hist:
  hist = hist.replace("\t\tset_cosmetic_tag = EGY_UAR_1970\n",
                    "\t\tset_cosmetic_tag = EGY_UAR_1970\n\t\tCOLDWAR_EGY_initialize_1970 = yes # COLDWAR | laws, factions, start spirits\n", 1)
assert "COLDWAR_EGY_initialize_1970" in hist
FB_SRC = "/mnt/user-data/uploads/mdcoldwar/common/scripted_effects/mdcw_1970_focus_tree_effects.txt"
fb = open(FB_SRC, encoding="utf-8-sig").read()
assert "\t\t\t\t\toriginal_tag = LBA\n" in fb
if "original_tag = EGY" not in fb:
  fb = fb.replace("\t\t\t\t\toriginal_tag = LBA\n", "\t\t\t\t\toriginal_tag = LBA\n\t\t\t\t\toriginal_tag = EGY # COLDWAR | own 1970 tree\n", 1)

# ---------------------------------------------------------------- write
FILES = {
    "common/national_focus/COLDWAR_EGY_1970_focus.txt": FOCUS_TXT,
    "common/ideas/COLDWAR_EGY_1970_ideas.txt": IDEAS_TXT,
    "common/dynamic_modifiers/COLDWAR_EGY_1970_dynamic_modifiers.txt": DYN_TXT,
    "common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt": EFFECTS,
    "common/scripted_triggers/COLDWAR_EGY_1970_scripted_triggers.txt": TRIGGERS_TXT,
    "common/opinion_modifiers/COLDWAR_EGY_1970_opinion_modifiers.txt": OPINION_TXT,
    "common/country_leader/COLDWAR_EGY_1970_traits.txt": TRAITS_TXT,
    "events/COLDWAR_EGY_1970_events.txt": EVENTS_TXT,
    "interface/COLDWAR_EGY_1970_goals.gfx": GFX,
    "interface/COLDWAR_EGY_1970_goals_shine.gfx": GFX_SHINE,
    "history/countries/EGY - Egypt.txt": hist,
    "common/scripted_effects/mdcw_1970_focus_tree_effects.txt": fb,
}
for p, t in FILES.items():
    write(p, t)
write("localisation/english/COLDWAR_EGY_1970_l_english.yml", loc_file(), bom=True)
for dst, src in FLAGS.items():
    os.makedirs(os.path.dirname(os.path.join(C.OUT, dst)), exist_ok=True)
    shutil.copyfile(src, os.path.join(C.OUT, dst))
print("written", len(FILES) + 1 + len(FLAGS), "files;", len(C.FOCI), "foci;", len(R.ideas), "ideas;", len(C.NEW_SPRITES), "new sprites;",
      len(LOC), "loc keys; unhandled", len(R.unhandled))
