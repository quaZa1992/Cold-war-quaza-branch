# COLDWAR | Scripted effects and triggers: initialisation, money, factions, cohesion, Politburo balance,
# General Secretaries (plenum, heirs, deaths), the Politburo of the Republics (seats, votes, proposals, intrigue).
from cw_common import *
import cw_effects as E
import cw_focus as FO
from cw_layout import CONCEPT, REPUBLICS, FOCI

KEYS = ["kos", "pod", "sus", "she", "and", "gre", "ust", "gro", "che", "gor", "bre"]
KIDX = {k: i + 1 for i, k in enumerate(KEYS)}
# Politburo membership windows (alive and in the Politburo); Brezhnev's date moves with the Kremlin doctors
ALIVE = {"kos": ("", "1980.12.18"), "pod": ("", "1983.1.12"), "sus": ("", "1982.1.25"), "she": ("", "1975.4.16"),
         "and": ("1973.4.26", "1984.2.9"), "gre": ("1973.4.26", "1976.4.26"), "ust": ("1976.3.4", "1984.12.20"),
         "gro": ("1976.3.4", ""), "che": ("1978.11.26", "1985.3.10"), "gor": ("1980.10.20", ""), "bre": ("", "1982.11.10")}
FACTIONS_USED = sorted({e["f"] for f in FOCI for e in f["eff"] if e["k"] == "fac"} |
                       {"communist_cadres", "the_military", "intelligence_community", "defense_industry", "industrial_conglomerates",
                        "farmers", "labour_unions"})
DYN_START = {"armed_forces": {"army_personnel_cost_multiplier_modifier": 0.05},
             "commonwealth": {"tax_gain_multiplier_modifier": -0.03, "oil_export_multiplier_modifier": -0.10,
                              "mdcw_cw_support_effectiveness": 0.10, "opinion_gain_monthly_same_ideology_factor": 0.10,
                              "foreign_influence_modifier": 0.05}}
BUILD = [(1, "industrial_complex", "one_random_industrial_complex", 0.005, "a civilian factory"),
         (2, "infrastructure", "one_random_infrastructure", 0.004, "infrastructure"),
         (3, "power_plant", "one_random_fossil_fuel_powerplant", 0.005, "a power station"),
         (4, "agriculture", "one_random_agriculture_district", 0.004, "an agriculture district"),
         (5, "arms_factory", "one_random_arms_factory", 0.008, "a military factory")]
RES_LEAN = {n: lean for n, (fid, lean) in enumerate(REPUBLICS.RESOLUTIONS, start=1)}
UNION_RES = {n for n, (fid, lean) in enumerate(REPUBLICS.RESOLUTIONS, start=1)
             if fid in ("russian_as_lingua_franca", "native_language_schools", "the_renewed_federation", "the_iron_union")}


def T(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"{PFX}{key}_tt"


def ifelse(chain):
    """[(cond, body)] -> if / else_if / else"""
    out = []
    for n, (cond, body) in enumerate(chain):
        kw = "if" if n == 0 else ("else" if cond is None else "else_if")
        if cond is None:
            out += ["else = {"] + body + ["}"]
        else:
            out += [f"{kw} = {{", f"limit = {{ {cond} }}"] + body + ["}"]
    return out


def alive(k):
    a, b = ALIVE[k]
    c = [f"NOT = {{ has_global_flag = {PFX}dead_{k} }}"] if (E.GENSEC[k][2] or k == "bre") else []
    if a:
        c.append(f"date > {a}")
    if b and k != "bre":
        c.append(f"date < {b}")
    if k == "bre":
        c.append(f"OR = {{ date < 1982.11.10 has_country_flag = {PFX}kremlin_doctors }}")
    return c


def build():
    C = CONCEPT
    E_ = [HEADER]
    add = E_.append

    # ------------------------------------------------------------------ init
    laws = [l for l, _ in C.START_LAWS]
    facs = [(f, v) for f, _, v in C.START_FACTIONS]
    spirits = [PFX + k for k, *_ in C.START_SPIRITS]
    L = ["COLDWAR_SOV_initialize_1970 = {", "if = {", f"limit = {{ NOT = {{ has_country_flag = {PFX}initialized }} }}",
         f"set_country_flag = {PFX}initialized", f"set_country_flag = {PFX}gensec_bre",
         "# laws, internal factions and the seven starting spirits", "add_ideas = {"] + laws + [f for f, _ in facs] + spirits + ["}"]
    L += [f"set_variable = {{ {f}_opinion = {v} }}" for f, v in facs]
    L += ["initialize_internal_faction_dynamic_modifiers = yes",
          f"set_variable = {{ {PFX}union_cohesion = {C.COHESION['start']} }}",
          f"set_variable = {{ {PFX}bop = {fmt(C.BOP['initial'])} }}",
          f"set_power_balance = {{ id = {PFX}politburo_bop left_side = {PFX}politburo_bop_left_side right_side = {PFX}politburo_bop_right_side set_value = {fmt(C.BOP['initial'])} }}"]
    for g, mods in DYN_START.items():
        for m, v in mods.items():
            L.append(f"set_variable = {{ {PFX}{g}_{m} = {fmt(v)} }}")
            E.R.dyn.setdefault(f"{PFX}{g}_modifier", [])
            if m not in E.R.dyn[f"{PFX}{g}_modifier"]:
                E.R.dyn[f"{PFX}{g}_modifier"].append(m)
    L += [f"add_dynamic_modifier = {{ modifier = {PFX}cohesion_{t} }}" for t in ("unbreakable", "strained", "crisis", "disintegration")]
    L += ["}", "}"]
    add("\n".join(block(L)))

    add("""
# called once from on_startup (all countries exist by then)
COLDWAR_SOV_setup_politburo = {
	if = {
		limit = { NOT = { has_global_flag = COLDWAR_SOV_politburo_system } }
		set_global_flag = COLDWAR_SOV_politburo_system
		set_variable = { global.COLDWAR_SOV_seat_count = 0 }
		set_variable = { global.COLDWAR_SOV_plan = 8 }			# the VIII Five-Year Plan (1966-1970) is running
		set_variable = { global.COLDWAR_SOV_session_half = 0 }
		set_variable = { global.COLDWAR_SOV_congress = 23 }
		if = { limit = { country_exists = UKR UKR = { COLDWAR_SOV_is_union_republic = yes } } UKR = { COLDWAR_SOV_take_seat = yes } }
		if = { limit = { country_exists = KAZ KAZ = { COLDWAR_SOV_is_union_republic = yes } } KAZ = { COLDWAR_SOV_take_seat = yes } }
		country_event = { id = COLDWAR_SOV.10 days = 181 }
	}
}

# ---- money as a share of GDP (temp COLDWAR_SOV_gdp_share, positive) ----------------------------
COLDWAR_SOV_pay_gdp_share = {
	set_temp_variable = { treasury_change = gdp_total }
	multiply_temp_variable = { treasury_change = COLDWAR_SOV_gdp_share }
	multiply_temp_variable = { treasury_change = -1 }
	modify_treasury_effect = yes
}

COLDWAR_SOV_receive_gdp_share = {
	set_temp_variable = { treasury_change = gdp_total }
	multiply_temp_variable = { treasury_change = COLDWAR_SOV_gdp_share }
	set_variable = { COLDWAR_SOV_last_transfer = treasury_change }
	modify_treasury_effect = yes
}

# the Soviet Union (THIS) pays a share of its GDP to the country in temp COLDWAR_SOV_transfer_target
COLDWAR_SOV_transfer_gdp_share = {
	set_temp_variable = { COLDWAR_SOV_amount = gdp_total }
	multiply_temp_variable = { COLDWAR_SOV_amount = COLDWAR_SOV_gdp_share }
	set_temp_variable = { treasury_change = COLDWAR_SOV_amount }
	multiply_temp_variable = { treasury_change = -1 }
	modify_treasury_effect = yes
	var:COLDWAR_SOV_transfer_target = {
		set_temp_variable = { treasury_change = COLDWAR_SOV_amount }
		modify_treasury_effect = yes
	}
}

# monthly (on_monthly_SOV): the Mongolian garrison (0.2% of GDP a year) and the Afghan Burden (0.3% of GDP a month)
COLDWAR_SOV_monthly_aid = {
	if = {
		limit = { country_exists = MON MON = { has_country_flag = COLDWAR_SOV_garrison_host } }
		set_temp_variable = { COLDWAR_SOV_transfer_target = MON.id }
		set_temp_variable = { COLDWAR_SOV_gdp_share = 0.000167 }
		COLDWAR_SOV_transfer_gdp_share = yes
	}
	if = {
		limit = { has_idea = COLDWAR_SOV_afghan_burden }
		set_temp_variable = { COLDWAR_SOV_gdp_share = 0.003 }
		COLDWAR_SOV_pay_gdp_share = yes
	}
}

COLDWAR_SOV_change_debt_gdp_share = {
	set_temp_variable = { debt_change = gdp_total }
	multiply_temp_variable = { debt_change = COLDWAR_SOV_gdp_share }
	modify_debt_effect = yes
}

# ---- internal factions: exact values (MD doubles positive gains for autocracies) ----------------
COLDWAR_SOV_prepare_exact_opinion = {
	set_temp_variable = { COLDWAR_SOV_requested_opinion = temp_opinion }
	if = {
		limit = {
			check_variable = { temp_opinion > 0 }
			OR = {
				check_variable = { ruling_party = 0 }
				check_variable = { ruling_party = 7 }
				check_variable = { ruling_party = 13 }
				check_variable = { ruling_party = 21 }
				check_variable = { ruling_party = 22 }
			}
		}
		multiply_temp_variable = { temp_opinion = 0.5 }
	}
}

COLDWAR_SOV_restore_exact_opinion = {
	set_temp_variable = { temp_opinion = COLDWAR_SOV_requested_opinion }
}
""")
    for fac in FACTIONS_USED:
        add(f"""COLDWAR_SOV_change_{fac}_opinion_exact = {{
	if = {{
		limit = {{ has_idea = {fac} }}
		COLDWAR_SOV_prepare_exact_opinion = yes
		change_{fac}_opinion = yes
		COLDWAR_SOV_restore_exact_opinion = yes
	}}
}}
""")
    OUTLOOK_PARTY = {0: (0, 3, 2), 1: (4, 9, 4), 2: (10, 11, 10), 3: (12, 19, 13), 4: (20, 23, 20)}
    s = ["# ---- outlook popularity: the ruling party if it belongs to the outlook, otherwise the outlook's main Soviet party",
         "COLDWAR_SOV_change_outlook_popularity = {"]
    for oid, (a, b, d) in OUTLOOK_PARTY.items():
        s += ["if = {", f"limit = {{ check_variable = {{ COLDWAR_SOV_outlook_id = {oid} }} }}", "if = {",
              f"limit = {{ check_variable = {{ ruling_party > {a - 1} }} check_variable = {{ ruling_party < {b + 1} }} }}",
              "set_temp_variable = { party_index = ruling_party }", "}", f"else = {{ set_temp_variable = {{ party_index = {d} }} }}", "}"]
    s += ["set_temp_variable = { party_popularity_increase = COLDWAR_SOV_outlook_amount }",
          "set_temp_variable = { temp_outlook_increase = COLDWAR_SOV_outlook_amount }", "change_relative_party_popularity = yes", "}"]
    add("\n".join(block(s)) + "\n")

    T("union_cohesion", "Union Cohesion: $RIGHT|+=0$")
    add(f"""
# ---- Union cohesion (0-100, SOV scope; temp COLDWAR_SOV_cohesion_delta) ------------------------
COLDWAR_SOV_change_union_cohesion = {{
	if = {{
		limit = {{ NOT = {{ original_tag = SOV }} }}
		SOV = {{ COLDWAR_SOV_change_union_cohesion = yes }}
	}}
	else = {{
		add_to_variable = {{ COLDWAR_SOV_union_cohesion = COLDWAR_SOV_cohesion_delta tooltip = COLDWAR_SOV_union_cohesion_tt }}
		clamp_variable = {{ var = COLDWAR_SOV_union_cohesion min = 0 max = 100 }}
		hidden_effect = {{ force_update_dynamic_modifier = yes }}
	}}
}}

# monthly (on_monthly_SOV): -1 low stability, -1 losing war, -1 deep corruption, +1 high stability
COLDWAR_SOV_monthly_cohesion = {{
	set_temp_variable = {{ COLDWAR_SOV_cohesion_delta = 0 }}
	if = {{ limit = {{ has_stability < 0.4 }} add_to_temp_variable = {{ COLDWAR_SOV_cohesion_delta = -1 }} }}
	if = {{ limit = {{ has_war = yes surrender_progress > 0.1 }} add_to_temp_variable = {{ COLDWAR_SOV_cohesion_delta = -1 }} }}
	if = {{ limit = {{ OR = {{ has_idea = corruption_level_07 has_idea = corruption_level_08 has_idea = corruption_level_09 has_idea = corruption_level_10 }} }} add_to_temp_variable = {{ COLDWAR_SOV_cohesion_delta = -1 }} }}
	if = {{ limit = {{ has_stability > 0.7 }} add_to_temp_variable = {{ COLDWAR_SOV_cohesion_delta = 1 }} }}
	add_to_variable = {{ COLDWAR_SOV_union_cohesion = COLDWAR_SOV_cohesion_delta }}
	clamp_variable = {{ var = COLDWAR_SOV_union_cohesion min = 0 max = 100 }}
	force_update_dynamic_modifier = yes
}}

# ---- Politburo balance: the shadow variable COLDWAR_SOV_bop mirrors the balance of power -------
COLDWAR_SOV_monthly_bop_drift = {{
	if = {{
		limit = {{ check_variable = {{ COLDWAR_SOV_bop > 0.01 }} }}
		add_power_balance_value = {{ id = COLDWAR_SOV_politburo_bop value = -0.01 }}
		add_to_variable = {{ COLDWAR_SOV_bop = -0.01 }}
	}}
	else_if = {{
		limit = {{ check_variable = {{ COLDWAR_SOV_bop < -0.01 }} }}
		add_power_balance_value = {{ id = COLDWAR_SOV_politburo_bop value = 0.01 }}
		add_to_variable = {{ COLDWAR_SOV_bop = 0.01 }}
	}}
}}

COLDWAR_SOV_bop_toward_centre_10 = {{
	custom_effect_tooltip = {T("bop_centre", "The Politburo balance moves §Y0.10§! towards the centre.")}
	hidden_effect = {{
		if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop > 0.1 }} }} {" ".join(E.bop(-0.10))} }}
		else_if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop < -0.1 }} }} {" ".join(E.bop(0.10))} }}
		else_if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop > 0.04 }} }} {" ".join(E.bop(-0.05))} }}
		else_if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop < -0.04 }} }} {" ".join(E.bop(0.05))} }}
	}}
}}

COLDWAR_SOV_bop_toward_centre_05 = {{
	custom_effect_tooltip = {T("bop_centre_05", "The Politburo balance moves §Y0.05§! towards the centre.")}
	hidden_effect = {{
		if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop > 0.04 }} }} {" ".join(E.bop(-0.05))} }}
		else_if = {{ limit = {{ check_variable = {{ COLDWAR_SOV_bop < -0.04 }} }} {" ".join(E.bop(0.05))} }}
	}}
}}

# ---- elections ----------------------------------------------------------------------------------
COLDWAR_SOV_allow_elections = {{
	custom_effect_tooltip = {T("allow_elections", "§GElections are allowed.§!")}
	set_variable = {{ disable_elections = 0 }}
	hidden_effect = {{
		if = {{ limit = {{ has_government = democratic }} set_politics = {{ ruling_party = democratic elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = communism }} set_politics = {{ ruling_party = communism elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = fascism }} set_politics = {{ ruling_party = fascism elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = neutrality }} set_politics = {{ ruling_party = neutrality elections_allowed = yes }} }}
		if = {{ limit = {{ has_government = nationalist }} set_politics = {{ ruling_party = nationalist elections_allowed = yes }} }}
	}}
}}

COLDWAR_SOV_suspend_elections = {{
	custom_effect_tooltip = {T("suspend_elections", "§RElections remain suspended.§!")}
	set_variable = {{ disable_elections = 1 }}
	hidden_effect = {{
		if = {{ limit = {{ has_government = democratic }} set_politics = {{ ruling_party = democratic elections_allowed = no }} }}
		if = {{ limit = {{ has_government = communism }} set_politics = {{ ruling_party = communism elections_allowed = no }} }}
		if = {{ limit = {{ has_government = fascism }} set_politics = {{ ruling_party = fascism elections_allowed = no }} }}
		if = {{ limit = {{ has_government = neutrality }} set_politics = {{ ruling_party = neutrality elections_allowed = no }} }}
		if = {{ limit = {{ has_government = nationalist }} set_politics = {{ ruling_party = nationalist elections_allowed = no }} }}
	}}
}}
""")

    # ------------------------------------------------------------------ General Secretaries
    s = ["# ==== General Secretaries ========================================================================",
         "COLDWAR_SOV_clear_gensec = {"] + [f"clr_country_flag = {PFX}gensec_{k}" for k in KEYS] + ["}", "",
         "COLDWAR_SOV_clear_heirs = {"] + [f"clr_country_flag = {PFX}heir_{k}" for k in KEYS + ["aliyev", "grishin"]] + ["}", ""]
    for k in KEYS:
        name, pic, death = E.GENSEC[k]
        traits = ["emerging_communist_state"] + E.GENSEC_TRAITS[k]
        p = f' picture = "{pic}"' if pic else ""
        LOC[f"{PFX}install_{k}_tt"] = f"§Y{name}§! becomes General Secretary of the CPSU. The tree of his predecessor closes; his own opens."
        s += [f"COLDWAR_SOV_install_gensec_{k} = {{", "COLDWAR_SOV_clear_gensec = yes", "COLDWAR_SOV_clear_heirs = yes",
              f"clr_country_flag = {PFX}bre_retiring", f"set_country_flag = {PFX}gensec_{k}", f"custom_effect_tooltip = {PFX}install_{k}_tt",
              "hidden_effect = {", "retire_country_leader = yes",
              f'create_country_leader = {{ name = "{name}"{p} ideology = communist_state traits = {{ {" ".join(traits)} }} }}',
              "force_update_dynamic_modifier = yes", f"news_event = {{ id = {NS}.33 hours = 6 }}", "}", "}", ""]
        LOC[f"{PFX}heir_{k}_tt"] = f"Designated heir: §Y{name}§!. When the General Secretary dies or retires, the Politburo votes on him first."
        s += [f"COLDWAR_SOV_set_heir_{k} = {{", "COLDWAR_SOV_clear_heirs = yes", f"set_country_flag = {PFX}heir_{k}",
              f"custom_effect_tooltip = {PFX}heir_{k}_tt",
              f"if = {{ limit = {{ has_country_flag = {PFX}bre_retiring }} hidden_effect = {{ country_event = {{ id = {NS}.32 days = 7 }} }} }}", "}", ""]
    for hk, name, pic, trait, of in [("aliyev", "Heydar Aliyev", "gfx/leaders/AZE/AZE_Coldwar_Heydar_Aliyev.dds", "COLDWAR_SOV_chekist_from_baku", "and"),
                                     ("grishin", "Viktor Grishin", None, "COLDWAR_SOV_moscow_boss", "che")]:
        LOC[f"{PFX}heir_{hk}_tt"] = (f"Designated heir: §Y{name}§!. When the General Secretary dies, {name} takes over his office "
                                     f"and continues his course; the tree stays open.")
        p = f' picture = "{pic}"' if pic else ""
        s += [f"COLDWAR_SOV_set_heir_{hk} = {{", "COLDWAR_SOV_clear_heirs = yes", f"set_country_flag = {PFX}heir_{hk}",
              f"custom_effect_tooltip = {PFX}heir_{hk}_tt", "}", "",
              f"COLDWAR_SOV_heir_takes_over_{hk} = {{", f"clr_country_flag = {PFX}heir_{hk}", "hidden_effect = {", "retire_country_leader = yes",
              f'create_country_leader = {{ name = "{name}"{p} ideology = communist_state traits = {{ emerging_communist_state {trait} }} }}',
              f"news_event = {{ id = {NS}.33 hours = 6 }}", "}", "}", ""]
    # succession after death or retirement
    chain = []
    chain.append((f"has_country_flag = {PFX}heir_aliyev has_country_flag = {PFX}gensec_and", [f"{PFX}heir_takes_over_aliyev = yes"]))
    chain.append((f"has_country_flag = {PFX}heir_grishin has_country_flag = {PFX}gensec_che", [f"{PFX}heir_takes_over_grishin = yes"]))
    for k in KEYS:
        if k == "bre":
            continue
        chain.append((f"has_country_flag = {PFX}heir_{k} " + " ".join(alive(k)),
                      [f"set_temp_variable = {{ {PFX}vt = 3 }}", f"set_temp_variable = {{ {PFX}vs = {KIDX[k]} }}",
                       f"set_temp_variable = {{ {PFX}vl = {E.GENSEC_LEAN[k]} }}", f"set_temp_variable = {{ {PFX}vu = 0 }}",
                       "if = {", f"limit = {{ has_global_flag = {PFX}vote_running }}", f"{PFX}install_gensec_{k} = yes", "}",
                       f"else = {{ set_variable = {{ global.{PFX}vote_succession = 1 }} {PFX}start_vote = yes }}"]))
    chain.append((None, [f"country_event = {{ id = {NS}.31 days = 1 }}"]))
    s += ["# the designated heir is put to the Politburo first; otherwise the succession plenum chooses among the living",
          "COLDWAR_SOV_succession = {"] + ifelse(chain) + ["}", ""]
    # back to party rule (from another party's tree)
    chain = [(f"date < 1982.11.10 NOT = {{ has_global_flag = {PFX}dead_bre }}", [f"{PFX}install_gensec_bre = yes"]),
             ("date < 1984.2.9", [f"{PFX}install_gensec_and = yes"]), ("date < 1985.3.10", [f"{PFX}install_gensec_che = yes"]),
             (None, [f"{PFX}install_gensec_gor = yes"])]
    s += ["COLDWAR_SOV_restore_party_rule = {", "set_temp_variable = { rul_party_temp = 4 }", "change_ruling_party_effect = yes"] + ifelse(chain) + ["}", ""]
    # plenum results
    for k in KEYS[:-1]:
        lean = E.GENSEC_LEAN[k]
        against = E.bop(0.05) if lean < 0 else (E.bop(-0.05) if lean > 0 else [])
        s += [f"COLDWAR_SOV_plenum_success_{k} = {{"] + FO.PLENUM_SUCCESS[k] + ["}", "",
              f"COLDWAR_SOV_plenum_failure_{k} = {{", "add_stability = -0.03"] + against + \
             [f"set_country_flag = {{ flag = {PFX}plenum_failed_{k} days = 180 }}", "}", ""]
    add("\n".join(block(s)) + "\n")

    # ------------------------------------------------------------------ Politburo of the Republics
    s = ["# ==== The Politburo and the Republics: three seats, votes, proposals, intrigue ====================",
         "COLDWAR_SOV_take_seat = {", f"set_country_flag = {PFX}seat", f"add_ideas = {PFX}politburo_seat",
         f"add_to_variable = {{ global.{PFX}seat_count = 1 }}", f"set_variable = {{ {PFX}bid = 0 }}", f"clr_country_flag = {PFX}applied", "}", "",
         "# THIS = republic, ROOT/FROM = Moscow",
         "COLDWAR_SOV_grant_seat = {", "COLDWAR_SOV_take_seat = yes", f"set_global_flag = {PFX}seat_changed_this_congress", f"set_temp_variable = {{ {PFX}cohesion_delta = 1 }}",
         "SOV = { COLDWAR_SOV_change_union_cohesion = yes }", f"{PFX}mark_last_seat = yes",
         f"news_event = {{ id = {NS}.26 hours = 6 }}", "}", "",
         "COLDWAR_SOV_leave_seat = {", f"clr_country_flag = {PFX}seat", f"remove_ideas = {PFX}politburo_seat",
         f"add_to_variable = {{ global.{PFX}seat_count = -1 }}", f"clamp_variable = {{ var = global.{PFX}seat_count min = 0 max = 3 }}",
         f"set_global_flag = {PFX}seat_changed_this_congress", "}", "",
         "COLDWAR_SOV_dismiss_seat = {", "COLDWAR_SOV_leave_seat = yes", f"set_temp_variable = {{ {PFX}cohesion_delta = -2 }}",
         "SOV = { COLDWAR_SOV_change_union_cohesion = yes }", f"{PFX}mark_last_seat = yes",
         f"news_event = {{ id = {NS}.27 hours = 6 }}", "}", "",
         "COLDWAR_SOV_mark_last_seat = {", f"every_country = {{ limit = {{ has_country_flag = {PFX}last_seat }} clr_country_flag = {PFX}last_seat }}",
         f"set_country_flag = {PFX}last_seat", "}", ""]
    # votes
    s += ["# temp in: COLDWAR_SOV_vt type (1 resolution, 2 plan, 3 leadership, 4 proposal), _vl lean (-1/0/1), _vs subject, _vu Union question",
          "COLDWAR_SOV_start_vote = {", f"set_global_flag = {PFX}vote_running",
          f"set_variable = {{ global.{PFX}vote_type = {PFX}vt }}", f"set_variable = {{ global.{PFX}vote_lean = {PFX}vl }}",
          f"set_variable = {{ global.{PFX}vote_subject = {PFX}vs }}", f"set_variable = {{ global.{PFX}vote_union = {PFX}vu }}",
          f"set_variable = {{ global.{PFX}vote_rep_yes = 0 }}", f"set_variable = {{ global.{PFX}vote_rep_total = 0 }}",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}in_vote }} clr_country_flag = {PFX}in_vote }}",
          "every_country = {", f"limit = {{ has_country_flag = {PFX}seat {PFX}is_union_republic = yes }}", f"set_country_flag = {PFX}in_vote", f"clr_country_flag = {PFX}voted_yes",
          f"clr_country_flag = {PFX}voted_no", f"clr_country_flag = {PFX}voted_abstain", f"set_country_flag = {PFX}vote_pending",
          f"{PFX}vote_weight = yes", f"add_to_variable = {{ global.{PFX}vote_rep_total = {PFX}w }}", f"country_event = {{ id = {NS}.11 }}", "}",
          f"country_event = {{ id = {NS}.12 days = 10 }}", "}", "",
          "COLDWAR_SOV_vote_weight = {", f"set_temp_variable = {{ {PFX}w = 1 }}", "if = {",
          f"limit = {{ check_variable = {{ global.{PFX}vote_union = 1 }} SOV = {{ has_country_flag = {PFX}federal_union }} }}",
          f"set_temp_variable = {{ {PFX}w = 2 }}", "}", "}", "",
          "COLDWAR_SOV_cast_vote = {   # temp COLDWAR_SOV_ballot: 1 yes, 2 no, 0 abstain",
          "if = {", f"limit = {{ has_global_flag = {PFX}vote_running has_country_flag = {PFX}vote_pending }}",
          f"clr_country_flag = {PFX}vote_pending",
          "if = {", f"limit = {{ check_variable = {{ {PFX}ballot = 1 }} }}", f"set_country_flag = {PFX}voted_yes", f"{PFX}vote_weight = yes",
          f"add_to_variable = {{ global.{PFX}vote_rep_yes = {PFX}w }}", "}",
          f"else_if = {{ limit = {{ check_variable = {{ {PFX}ballot = 2 }} }} set_country_flag = {PFX}voted_no }}",
          f"else = {{ set_country_flag = {PFX}voted_abstain }}", "}", "}", ""]
    # tally
    res = ["if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 1 }} }}",
           "if = {", f"limit = {{ has_global_flag = {PFX}vote_passed }}", "add_political_power = 25", "add_stability = 0.02", "}",
           "else = {", f"add_timed_idea = {{ idea = {PFX}defying_the_politburo days = 180 }}", f"set_temp_variable = {{ {PFX}cohesion_delta = -2 }}",
           f"{PFX}change_union_cohesion = yes", "}", "}",
           "else_if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 2 }} }}",
           "if = {", f"limit = {{ has_global_flag = {PFX}vote_passed }}", "add_political_power = 50", "}",
           f"else = {{ add_timed_idea = {{ idea = {PFX}defying_the_politburo days = 180 }} }}", "}",
           "else_if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 3 }} }}"]
    lead = []
    for k in KEYS[:-1]:
        lead.append((f"check_variable = {{ global.{PFX}vote_subject = {KIDX[k]} }}",
                     ["if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_succession = 1 }} }}",
                      "if = {", f"limit = {{ has_global_flag = {PFX}vote_passed }}", f"{PFX}install_gensec_{k} = yes", "}",
                      f"else = {{ country_event = {{ id = {NS}.31 days = 1 }} }}", "}",
                      "else = {", "if = {", f"limit = {{ has_global_flag = {PFX}vote_passed }}", f"{PFX}plenum_success_{k} = yes", "}",
                      f"else = {{ {PFX}plenum_failure_{k} = yes }}", "}"]))
    res += ifelse(lead) + [f"set_variable = {{ global.{PFX}vote_succession = 0 }}", "}",
                           "else_if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 4 }} }}",
                           f"set_temp_variable = {{ {PFX}tp = global.{PFX}last_proposer }}",
                           f"var:{PFX}tp = {{", f"clr_country_flag = {PFX}proposal_rejected", f"if = {{ limit = {{ NOT = {{ has_global_flag = {PFX}vote_passed }} }} clr_country_flag = {PFX}proposal_locked }}", "}",
                           "if = {", f"limit = {{ has_global_flag = {PFX}vote_passed }}", f"country_event = {{ id = {NS}.22 days = 1 }}", "}", "}"]
    s += ["COLDWAR_SOV_tally_vote = {",
          "# the seven Moscow members follow the Politburo balance; republican proposals always get three of them",
          "if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 4 }} }}", f"set_temp_variable = {{ {PFX}m = 3 }}",
          f"set_temp_variable = {{ {PFX}g = 0 }}", "}", "else = {", f"set_temp_variable = {{ {PFX}m = {PFX}bop }}",
          f"multiply_temp_variable = {{ {PFX}m = global.{PFX}vote_lean }}", f"multiply_temp_variable = {{ {PFX}m = 3.5 }}",
          f"add_to_temp_variable = {{ {PFX}m = 3.5 }}", f"round_temp_variable = {PFX}m",
          f"clamp_temp_variable = {{ var = {PFX}m min = 0 max = 7 }}", f"set_temp_variable = {{ {PFX}g = 1 }}", "}",
          f"set_variable = {{ global.{PFX}vote_moscow = {PFX}m }}",
          f"set_variable = {{ global.{PFX}vote_yes = {PFX}m }}", f"add_to_variable = {{ global.{PFX}vote_yes = {PFX}g }}",
          f"add_to_variable = {{ global.{PFX}vote_yes = global.{PFX}vote_rep_yes }}",
          f"set_variable = {{ global.{PFX}vote_total = 8 }}", f"add_to_variable = {{ global.{PFX}vote_total = global.{PFX}vote_rep_total }}",
          f"set_variable = {{ global.{PFX}vote_no = global.{PFX}vote_total }}", f"subtract_from_variable = {{ global.{PFX}vote_no = global.{PFX}vote_yes }}",
          f"set_temp_variable = {{ {PFX}t = global.{PFX}vote_yes }}", f"multiply_temp_variable = {{ {PFX}t = 2 }}",
          "if = {", f"limit = {{ check_variable = {{ {PFX}t > global.{PFX}vote_total }} }}", f"set_global_flag = {PFX}vote_passed", "}",
          f"else = {{ clr_global_flag = {PFX}vote_passed }}",
          "every_country = {", f"limit = {{ has_country_flag = {PFX}vote_pending }}", f"clr_country_flag = {PFX}vote_pending",
          f"set_country_flag = {PFX}voted_abstain", "}",
          "# the news and the follow-up events read the 'last' copies, so a new vote cannot overwrite what they show",
          f"set_variable = {{ global.{PFX}last_type = global.{PFX}vote_type }}", f"set_variable = {{ global.{PFX}last_subject = global.{PFX}vote_subject }}",
          f"set_variable = {{ global.{PFX}last_succession = global.{PFX}vote_succession }}",
          f"if = {{ limit = {{ has_global_flag = {PFX}vote_passed }} set_global_flag = {PFX}last_passed }} else = {{ clr_global_flag = {PFX}last_passed }}",
          "if = {", f"limit = {{ check_variable = {{ global.{PFX}vote_type = 4 }} }}", f"set_variable = {{ global.{PFX}last_proposer = global.{PFX}vote_proposer }}",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}last_proposer }} clr_country_flag = {PFX}last_proposer }}",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}current_proposer }} set_country_flag = {PFX}last_proposer }}", "}",
          f"every_country = {{ limit = {{ OR = {{ has_country_flag = {PFX}last_yes has_country_flag = {PFX}last_no has_country_flag = {PFX}last_abstain }} }}",
          f"clr_country_flag = {PFX}last_yes clr_country_flag = {PFX}last_no clr_country_flag = {PFX}last_abstain", "}",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}in_vote }}",
          f"if = {{ limit = {{ has_country_flag = {PFX}voted_yes }} set_country_flag = {PFX}last_yes }}",
          f"if = {{ limit = {{ has_country_flag = {PFX}voted_no }} set_country_flag = {PFX}last_no }}",
          f"if = {{ limit = {{ has_country_flag = {PFX}voted_abstain }} set_country_flag = {PFX}last_abstain }}", "}",
          f"news_event = {{ id = {NS}.13 hours = 2 }}"] + res + [f"clr_global_flag = {PFX}vote_running",
                                                                 "# the next resolution in the queue waits three days, so everyone can read the result",
                                                                 f"country_event = {{ id = {NS}.55 days = 3 }}", "}", ""]
    # resolutions queue
    lean_chain = [(f"check_variable = {{ {PFX}q = {n} }}", [f"set_temp_variable = {{ {PFX}vl = {l} }}"]) for n, l in RES_LEAN.items()]
    s += ["# Politburo resolutions on key foci (temp COLDWAR_SOV_queue_subject)",
          "COLDWAR_SOV_queue_resolution = {", f"add_to_array = {{ array = global.{PFX}res_queue value = {PFX}queue_subject }}",
          f"if = {{ limit = {{ NOT = {{ has_global_flag = {PFX}vote_running }} }} {PFX}next_queued_vote = yes }}", "}", "",
          "COLDWAR_SOV_next_queued_vote = {", "if = {", f"limit = {{ check_variable = {{ global.{PFX}res_queue^num > 0 }} }}",
          f"set_temp_variable = {{ {PFX}q = global.{PFX}res_queue^0 }}", f"remove_from_array = {{ array = global.{PFX}res_queue value = {PFX}q }}",
          f"set_temp_variable = {{ {PFX}vt = 1 }}", f"set_temp_variable = {{ {PFX}vs = {PFX}q }}", f"set_temp_variable = {{ {PFX}vu = 0 }}"] + ifelse(lean_chain) + \
         [f"if = {{ limit = {{ OR = {{ " + " ".join(f"check_variable = {{ {PFX}q = {n} }}" for n in sorted(UNION_RES)) + f" }} }} set_temp_variable = {{ {PFX}vu = 1 }} }}",
          f"{PFX}start_vote = yes", "}", "}", ""]
    # proposals
    bchain = []
    for n, key, helper, share, label in BUILD:
        bchain.append((f"check_variable = {{ {PFX}prop_building = {n} }}",
                       ["set_temp_variable = { skip_payment = 1 }", f"{helper} = yes", "set_temp_variable = { skip_payment = 0 }",
                        f"SOV = {{ set_temp_variable = {{ {PFX}gdp_share = {share} }} {PFX}pay_gdp_share = yes }}"]))
    s += ["# THIS = the republic that gets the building; Moscow pays a share of its GDP",
          "COLDWAR_SOV_build_union_project = {"] + ifelse(bchain) + [f"set_temp_variable = {{ {PFX}cohesion_delta = 1 }}",
                                                                      "SOV = { COLDWAR_SOV_change_union_cohesion = yes }", "}", "",
          "# THIS = proposing republic (variables COLDWAR_SOV_prop_type / _prop_building / _prop_benef)",
          "COLDWAR_SOV_execute_proposal = {",
          "if = {", f"limit = {{ check_variable = {{ {PFX}prop_type = 1 }} }}",
          f"set_temp_variable = {{ {PFX}prop_building = {PFX}prop_building }}",
          "if = {", f"limit = {{ has_variable = {PFX}prop_benef NOT = {{ check_variable = {{ {PFX}prop_benef = THIS.id }} }} }}",
          f"var:{PFX}prop_benef = {{ {PFX}build_union_project = yes }}", "}", f"else = {{ {PFX}build_union_project = yes }}", "}",
          "else_if = {", f"limit = {{ check_variable = {{ {PFX}prop_type = 2 }} }}", f"add_timed_idea = {{ idea = {PFX}plan_relief days = 730 }}",
          f"SOV = {{ add_timed_idea = {{ idea = {PFX}plan_shortfall days = 730 }} }}", "}",
          "else_if = {", f"limit = {{ check_variable = {{ {PFX}prop_type = 3 }} }}", f"set_country_flag = {PFX}cadre_protection", "}",
          f"clear_variable = {PFX}prop_benef", "}", ""]
    # intrigue
    s += ["# kompromat against a seat holder (THIS = the accused republic)",
          "COLDWAR_SOV_investigate_republic = {",
          "if = {", f"limit = {{ has_country_flag = {PFX}cadre_protection }}", f"set_temp_variable = {{ {PFX}chance = 0 }}", "}",
          "else = {", f"set_temp_variable = {{ {PFX}chance = 15 }}"] + \
         [f"if = {{ limit = {{ has_idea = corruption_level_{i:02d} }} add_to_temp_variable = {{ {PFX}chance = {5 * i} }} }}" for i in range(1, 11)] + \
         [f"if = {{ limit = {{ has_country_flag = {PFX}pripiski }} add_to_temp_variable = {{ {PFX}chance = 25 }} }}",
          f"if = {{ limit = {{ SOV = {{ has_country_flag = {PFX}discipline_campaign }} }} add_to_temp_variable = {{ {PFX}chance = 20 }} }}",
          f"if = {{ limit = {{ SOV = {{ has_country_flag = {PFX}local_barons }} }} add_to_temp_variable = {{ {PFX}chance = -10 }} }}",
          f"clamp_temp_variable = {{ var = {PFX}chance min = 0 max = 90 }}", "}",
          f"set_temp_variable_to_random = {{ var = {PFX}roll min = 0 max = 100 }}",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}accused }} clr_country_flag = {PFX}accused }}", f"set_country_flag = {PFX}accused",
          "if = {", f"limit = {{ check_variable = {{ {PFX}roll < {PFX}chance }} }}",
          f"set_global_flag = {PFX}kompromat_proven",
          f"if = {{ limit = {{ has_country_flag = {PFX}seat }} {PFX}leave_seat = yes }}",
          f"add_ideas = {PFX}in_disgrace", f"set_variable = {{ {PFX}disgrace_left = 2 }}", f"clr_country_flag = {PFX}pripiski",
          f"set_temp_variable = {{ {PFX}cohesion_delta = -1 }}", "SOV = { COLDWAR_SOV_change_union_cohesion = yes }",
          f"country_event = {{ id = {NS}.35 days = 3 }}", "}",
          f"else = {{ clr_global_flag = {PFX}kompromat_proven }}",
          f"news_event = {{ id = {NS}.18 hours = 6 }}", "}", "",
          "COLDWAR_SOV_federation_council = {",
          f"custom_effect_tooltip = {T('federation_council', 'The §YFederation Council§! replaces the republican seats: every republic now advises the President. The Politburo seats and their bonuses end.')}",
          "hidden_effect = {", f"set_global_flag = {PFX}federation_council",
          "every_country = {", f"limit = {{ has_country_flag = {PFX}seat }}", f"{PFX}leave_seat = yes", "}",
          f"news_event = {{ id = {NS}.28 hours = 6 }}", "}", "}", "",
          "COLDWAR_SOV_withdraw_from_afghanistan = {", f"remove_ideas = {PFX}afghan_burden",
          f"if = {{ limit = {{ country_exists = AFG }} AFG = {{ country_event = {{ id = {NS}.49 days = 1 }} }} }}", "}", ""]
    # five-year plans
    s += ["# a new Five-Year Plan begins (from the session event): the old priority ends, every seat holder chooses a Union project",
          "COLDWAR_SOV_start_plan = {"] + [f"if = {{ limit = {{ has_idea = {PFX}{k} }} remove_ideas = {PFX}{k} }}" for k, *_ in PLAN_PRIOS] + \
         [f"clr_country_flag = {PFX}plan_priority_chosen",
          "every_country = {", f"limit = {{ has_country_flag = {PFX}seat }}", f"country_event = {{ id = {NS}.25 days = 1 }}", "}", "}", "",
          "# a seat holder takes its rejected proposal before the Politburo (THIS = the republic)",
          "COLDWAR_SOV_propose_to_politburo = {",
          f"every_country = {{ limit = {{ has_country_flag = {PFX}current_proposer }} clr_country_flag = {PFX}current_proposer }}",
          f"set_country_flag = {PFX}current_proposer", f"set_variable = {{ global.{PFX}vote_proposer = THIS.id }}",
          f"set_temp_variable = {{ {PFX}vt = 4 }}", f"set_temp_variable = {{ {PFX}vl = 0 }}", f"set_temp_variable = {{ {PFX}vu = 1 }}",
          f"if = {{ limit = {{ check_variable = {{ {PFX}prop_type = 1 }} }} set_temp_variable = {{ {PFX}vs = {PFX}prop_building }} }}",
          f"else_if = {{ limit = {{ check_variable = {{ {PFX}prop_type = 2 }} }} set_temp_variable = {{ {PFX}vs = 6 }} }}",
          f"else = {{ set_temp_variable = {{ {PFX}vs = 7 }} }}",
          f"SOV = {{ {PFX}start_vote = yes }}", "}", ""]
    add("\n".join(block(s)) + "\n")
    return "\n".join(E_) + "\n"


PLAN_PRIOS = [("plan_group_a", "Group A: Heavy Industry", [("production_speed_buildings_factor", 0.10), ("consumer_goods_factor", 0.03)]),
              ("plan_group_b", "Group B: Consumer Goods", [("consumer_goods_factor", -0.04), ("stability_factor", 0.03), ("production_speed_buildings_factor", -0.05)]),
              ("plan_armaments", "The Defence Industry", [("production_speed_arms_factory_factor", 0.15), ("consumer_goods_factor", 0.04)]),
              ("plan_agriculture", "The Food Programme", [("agricolture_productivity_modifier", 0.10), ("industrial_capacity_factory", -0.03)])]
for k, n, m in PLAN_PRIOS:
    E.R.ideas[PFX + k] = dict(name=f"Plan Priority: {n}", mods=m, days=None)
E.R.ideas[PFX + "sovereign_rights"] = dict(name="Sovereign Rights of the Republics", mods=[("political_power_factor", -0.05)], days=365)
E.R.ideas[PFX + "ideological_campaign"] = dict(name="Ideological Campaign", mods=[("research_speed_factor", -0.01)], days=180)


def triggers():
    s = [HEADER, "COLDWAR_SOV_is_union_republic = {", "is_subject_of = SOV", "OR = {"] + [f"original_tag = {t}" for t in SSR] + ["}", "}", ""]
    for k in KEYS:
        s += [f"COLDWAR_SOV_alive_{k} = {{"] + alive(k) + ["}", ""]
    s += ["# a republic may apply for a seat at the next Party Congress",
          "COLDWAR_SOV_can_apply = {", "COLDWAR_SOV_is_union_republic = yes", f"NOT = {{ has_country_flag = {PFX}seat }}",
          f"NOT = {{ has_idea = {PFX}slanderer }}", f"NOT = {{ has_idea = {PFX}in_disgrace }}", f"NOT = {{ has_country_flag = {PFX}applied }}",
          f"has_global_flag = {PFX}applications_open", "}", ""]
    return "\n".join(block(s)) + "\n"
