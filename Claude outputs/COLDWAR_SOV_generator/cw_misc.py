# COLDWAR | Ideas, dynamic modifiers, the Politburo balance of power, opinion modifiers, leader traits,
# on_actions, scripted localisation and the events file of the Soviet Union 1970 tree.
import re
from cw_common import *
import cw_effects as E
from cw_effects import R
import cw_offers as OF
import cw_events as EV
from cw_layout import SECT, PARTY, TRIG, TRAITS, OPINIONS, REPUBLICS
from cw_sys_effects import KEYS, KIDX, PLAN_PRIOS, RES_LEAN

IDEA_GFX = set(open(os.path.join(EGY, "idea_gfx.txt")).read().split())

# ---------------------------------------------------------------- national spirits
PIC = {
    "stability_of_cadres": "sov_politburo", "burden_of_parity": "sov_rebuild_vpk_idea", "agrarian_problem": "risk_of_famine",
    "ussuri_frontier": "sov_transkbaikal_ideas", "shadow_of_prague": "anti_soviet_pact", "second_economy": "nko_black_market_idea",
    "dissent": "sov_ipso_idea", "shadow_of_prague_eased": "anti_soviet_pact", "burden_of_parity_eased": "sov_rebuild_vpk_idea",
    "ussuri_frontier_eased": "sov_transkbaikal_ideas",
    "cadre_renewal": "political_reform", "era_of_stagnation": "stagnation", "party_mobilisation": "communism",
    "thaw_atmosphere": "sov_russian_democratic", "third_way_debate": "neutrality", "russian_revival": "sov_russia_great_idea",
    "cooperative_sector": "sov_nep_idea", "scientific_technical_revolution": "sov_computing_economy", "oil_dependency": "oil_profits",
    "bam_construction": "SOV_soviet_railways", "red_moon": "sov_roskosmos_idea", "scientific_superpower": "research_bonus",
    "army_of_a_superpower": "sov_all_army_idea", "nuclear_parity": "SOV_atomic_bomb_project", "correlation_of_forces": "SOV_soviet_hegemony",
    "blue_water_navy": "sov_good_fleet", "silenced_dissent": "secret_police", "dissent_abroad": "sov_information_war_idea",
    "socialist_pluralism": "sov_socialist_humanism_idea", "shield_and_sword": "SOV_kgb_idea", "renewed_federation": "sub_federalism_idea",
    "soviet_people": "sov_new_ussr_idea", "socialist_way_of_life": "sov_socialism_idea", "arms_race": "sov_oboronprom_idea",
    "basket_three": "international_treaty", "eastern_fortress": "sov_transkbaikal_ideas", "strike_at_dawn": "sov_vks_idea",
    "brezhnev_doctrine": "SOV_soviet_hegemony", "socialist_commonwealth": "communism3", "vanguard_of_revolution": "sov_export_revoult_idea",
    "transition_of_power": "sov_government_idea", "socialist_state": "communism2", "free_union": "sov_russian_democratic",
    "non_aligned_union": "neutrality2", "russia_first": "sov_go_russia_idea", "plenum_shakeup": "generic_purge", "little_deal": "sov_kulaks_idea",
    "developed_socialism": "sov_socialism_idea", "reformed_economy": "sov_perestroika_idea", "soviet_state": "sov_government_idea",
    "orthodox_union": "sov_restalinisation", "iron_order": "sov_special_servises_idea", "disciplined_union": "sov_agency_anti_corrupt_idea",
    "garrison_party": "sov_military_departments", "arsenal_of_socialism": "sov_uvz", "ordered_union": "sov_loyal_communists",
    "old_guard": "sov_politburo", "common_european_home": "european_union_member", "self_management_transition": "worker_reforms",
    "commune_state": "communism4", "second_industrialisation": "sov_five_year_idea", "vanguard_state": "sov_young_guard_idea",
    "managed_union": "sov_planned_economy_idea", "new_russia": "sov_new_russia_economic_idea", "open_society": "democracy",
    "human_face": "sov_socialist_humanism_idea", "planned_society": "sov_planned_economy_idea", "self_limitation": "orthodox_christian_idea",
    "shadow_capitalism": "sov_oligarch", "corporate_union": "SOV_Politisation_of_oligarchs", "market_union": "market_liberalism",
    "green_union": "khm_bad_ecology", "market_commonwealth": "market_dynamics", "commonwealth_of_soviet_states": "sov_eaes_idea",
    "great_russia": "sov_russia_great_idea", "rebirth_state": "sov_nazbols_idea", "garrison_state": "sov_cult_of_war",
    "restored_empire": "SOV_romanov_tsars",
    "politburo_seat": "sov_politburo", "defying_the_politburo": "generic_civil_unrest", "patron_in_moscow": "sov_government_idea",
    "in_disgrace": "generic_purge", "slanderer": "spy_political", "plan_relief": "sov_five_year_idea", "plan_shortfall": "stagnation",
    "declaration_of_sovereignty": "sov_republic_rf",
    "arms_limitation": "international_treaty2", "basic_principles": "international_treaty", "space_cooperation": "sov_baikonur_idea",
    "scientific_cooperation": "research_bonus", "salt_ii": "international_treaty2", "inf_treaty": "nuclear_power_def",
    "soviet_advisers": "soviet_advisors", "soviet_arms_package": "army_strengthened", "soviet_combat_support": "revolutionary_army",
    "interkosmos_flight": "sov_russian_cosmodes_idea", "soviet_gas": "sov_gas_streams_idea", "soviet_garrison": "national_defenders",
    "oil_for_sugar": "oil_profits", "limited_contingent": "soviet_advisors", "afghan_burden": "afghan_disorganized_army",
    "slavic_union_member": "blr_union_state_integration", "union_treaty_member": "sub_federalism_idea",
    "plan_group_a": "sov_five_year_idea", "plan_group_b": "Stabilized_Food_Supply", "plan_armaments": "sov_rebuild_vpk_idea",
    "plan_agriculture": "agricultural_reforms", "sovereign_rights": "sub_federalism_idea", "ideological_campaign": "propaganda",
}


def ideas_file():
    L = [HEADER, "ideas = {", "country = {"]
    for iid, d in R.ideas.items():
        s = iid.replace(PFX, "")
        pic = PIC[s]
        assert pic in IDEA_GFX, (iid, pic)
        LOC[iid] = d["name"]
        L += [f"{iid} = {{", f"picture = {pic}", "allowed = { always = no }", "allowed_civil_war = { always = yes }", "modifier = {"]
        L += [f"{k} = {fmt(v)}" for k, v in d["mods"]] + ["}", "}"]
    L += ["}", "}"]
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- dynamic modifiers
COUNTRY_MODS = {"party_state": ("The Party State", "sov_politburo"), "gosplan": ("Gosplan: The Planned Economy", "sov_planned_economy_idea"),
                "armed_forces": ("The Armed Forces of the USSR", "sov_all_army_idea"), "union": ("The Union of Republics", "sov_new_ussr_idea"),
                "commonwealth": ("The Socialist Community", "SOV_soviet_hegemony")}
PROG_ICON = {"cpsu": "communism", "bre": "sov_government_idea", "kos": "sov_planned_economy_idea", "pod": "sov_republic_rf", "sus": "sov_restalinisation",
             "she": "sov_young_guard_idea", "and": "SOV_kgb_idea", "gre": "sov_all_army_idea", "ust": "sov_rebuild_vpk_idea", "gro": "sov_loyal_communists",
             "che": "sov_socialism_idea", "gor": "sov_perestroika_idea", "wc": "worker_reforms", "ns": "sov_restalinisation", "kv": "sov_young_guard_idea",
             "sd": "sov_computing_economy", "nts": "sov_legacy_of_rus_idea", "chr": "sov_russian_democratic", "uds": "sov_socialist_humanism_idea",
             "gt": "sov_planned_economy_idea", "lnl": "orthodox_christian_idea", "rd": "sov_oligarch", "fel": "market_liberalism", "fob": "khm_bad_ecology",
             "smc": "market_dynamics", "usr": "sov_republic_rf", "rp": "sov_russia_great_idea", "cnr": "sov_revoult_spirit_idea",
             "com": "sov_military_departments", "rom": "SOV_romanov_tsars"}
COHESION = [("unbreakable", "Unbreakable Union", "national_unity", "check_variable = { COLDWAR_SOV_union_cohesion > 74 }",
             [("stability_factor", 0.03), ("political_power_factor", 0.03), ("nationalist_drift", -0.02)]),
            ("strained", "Strained Union", "generic_civil_unrest", "check_variable = { COLDWAR_SOV_union_cohesion > 34 } check_variable = { COLDWAR_SOV_union_cohesion < 55 }",
             [("stability_factor", -0.03), ("drift_defence_factor", -0.10), ("tax_gain_multiplier_modifier", -0.05)]),
            ("crisis", "Union in Crisis", "sov_nat_angry", "check_variable = { COLDWAR_SOV_union_cohesion > 14 } check_variable = { COLDWAR_SOV_union_cohesion < 35 }",
             [("stability_factor", -0.08), ("nationalist_drift", 0.05), ("tax_gain_multiplier_modifier", -0.10)]),
            ("disintegration", "Disintegration", "sov_revoult_spirit_idea", "check_variable = { COLDWAR_SOV_union_cohesion < 15 }",
             [("stability_factor", -0.15)])]


def party_of(sec):
    m = re.search(r"\((\d+)\)$", SECT[sec]["title"])
    return int(m.group(1)) if m else None


def dyn_file():
    L = [HEADER]
    for g, (name, icon) in COUNTRY_MODS.items():
        mod = f"{PFX}{g}_modifier"
        assert icon in IDEA_GFX, icon
        L += [f"{mod} = {{", f"icon = GFX_idea_{icon}", ""] + [f"{k} = {PFX}{g}_{k}" for k in R.dyn.get(mod, [])] + ["}", ""]
        LOC[mod] = name
    for g, name, icon, cond, mods in COHESION:
        assert icon in IDEA_GFX, icon
        L += [f"{PFX}cohesion_{g} = {{", f"icon = GFX_idea_{icon}", "enable = {", cond, "}", ""] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}", ""]
        LOC[f"{PFX}cohesion_{g}"] = name
    for mod, keys in R.dyn.items():
        if not mod.endswith("_programme"):
            continue
        k = mod.replace(PFX, "").replace("_programme", "")
        if k == "cpsu":
            en = ["emerging_communist_state_are_in_power = yes"]
            title = "The Programme of the CPSU"
        elif k in KEYS:
            en = [f"has_country_flag = {PFX}gensec_{k}", "emerging_communist_state_are_in_power = yes"]
            title = f"The Course of {E.GENSEC[k][0]}"
        else:
            i = party_of(k)
            en = [f"{TRIG[i]}_are_in_power = yes"]
            title = f"Programme: {PARTY[i][0]}"
        icon = PROG_ICON[k]
        assert icon in IDEA_GFX, icon
        L += [f"{mod} = {{", f"icon = GFX_idea_{icon}", "enable = {", "original_tag = SOV"] + en + ["}", ""] + [f"{x} = {mod}_{x}" for x in keys] + ["}", ""]
        LOC[mod] = title
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- the Politburo balance
BOP_RANGES = {
    "left": [("revisionist_crisis", "Revisionist Crisis", -1, -0.7, [("research_speed_factor", 0.06), ("productivity_growth_modifier", 0.08),
                                                                  ("stability_factor", -0.10), ("democratic_drift", 0.05)], 47),
             ("reform_ascendancy", "Reform Ascendancy", -0.7, -0.4, [("research_speed_factor", 0.05), ("productivity_growth_modifier", 0.06),
                                                                     ("trade_opinion_factor", 0.10), ("stability_factor", -0.03), ("drift_defence_factor", -0.15)], None),
             ("reform_current", "Reform Current", -0.4, -0.15, [("research_speed_factor", 0.03), ("productivity_growth_modifier", 0.03),
                                                               ("drift_defence_factor", -0.05)], None)],
    "right": [("orthodox_course", "Orthodox Course", 0.15, 0.4, [("stability_factor", 0.03), ("drift_defence_factor", 0.10), ("research_speed_factor", -0.02)], None),
              ("neo_stalinist_tide", "Neo-Stalinist Tide", 0.4, 0.7, [("stability_factor", 0.05), ("political_power_factor", 0.05), ("drift_defence_factor", 0.20),
                                                                      ("police_cost_multiplier_modifier", 0.10), ("research_speed_factor", -0.05),
                                                                      ("productivity_growth_modifier", -0.05)], None),
              ("reaction", "Reaction", 0.7, 1, [("drift_defence_factor", 0.25), ("war_support_factor", 0.05), ("research_speed_factor", -0.08),
                                                 ("productivity_growth_modifier", -0.08), ("stability_factor", -0.05)], 48)]}


def bop_file():
    b = f"{PFX}politburo_bop"
    LOC[b] = "The Politburo"
    LOC[f"{b}_left_side"] = "Reformers and Technocrats"
    LOC[f"{b}_right_side"] = "The Orthodox and the Siloviki"
    LOC[f"{b}_mid_range"] = "Collective Leadership"
    L = [HEADER, f"{b} = {{", "initial_value = 0.15", f"left_side = {b}_left_side", f"right_side = {b}_right_side",
         f"decision_category = {PFX}politburo_category", "",
         "range = {", f"id = {b}_mid_range", "min = -0.15", "max = 0.15", "modifier = {", "stability_factor = 0.02", "political_power_factor = 0.03", "}", "}", ""]
    for side, icon in (("left", "GFX_SOV_bop_westerns"), ("right", "GFX_SOV_bop_eastern")):
        L += ["side = {", f"id = {b}_{side}_side", f"icon = {icon}"]
        for rid, name, lo, hi, mods, evn in BOP_RANGES[side]:
            LOC[f"{b}_{rid}"] = name
            L += ["range = {", f"id = {b}_{rid}", f"min = {fmt(lo)}", f"max = {fmt(hi)}", "modifier = {"] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}"]
            if evn:
                L += ["on_activate = {", f"if = {{ limit = {{ has_country_flag = {PFX}initialized }} country_event = {{ id = {NS}.{evn} days = 1 }} }}", "}"]
            L.append("}")
        L += ["}", ""]
    L.append("}")
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- opinion modifiers and traits
OP_NAMES = {"economic_partners": "Economic Partnership", "grain_customer": "Grain Customer", "energy_partner": "Energy Partner",
            "euromissiles": "The Euromissiles", "human_rights": "Human Rights Dialogue", "detente": "Detente", "asian_security": "Asian Collective Security",
            "bloc_relations": "Strained Bloc Relations", "horn_of_africa": "The Horn of Africa", "afghan_question": "The Afghan Question",
            "third_way": "The Third Way", "third_world": "Third World Solidarity", "eurocommunism": "Eurocommunism", "sino_split": "The Sino-Soviet Split",
            "olympic_boycott": "Olympic Boycott", "stalin_question": "The Stalin Question", "republics": "Respect for the Republics"}


def opinion_file():
    L = [HEADER, "opinion_modifiers = {"]
    allm = dict(R.opinions)
    for k, (v, n) in OF.OPINION_EXTRA.items():
        allm[k] = v
        LOC[k] = n
    for k, v in sorted(allm.items()):
        trade = OPINIONS.get(k, (0, False))[1]
        L += [f"{k} = {{", f"value = {v}"] + (["trade = yes"] if trade else []) + (["decay = 0.25"] if abs(v) >= 20 else []) + ["}"]
        if k not in LOC:
            LOC[k] = OP_NAMES[k.replace(PFX, "")]
    L.append("}")
    return "\n".join(block(L)) + "\n"


TRAIT_MODS = {
    "economist_premier": [("productivity_growth_modifier", 0.02), ("political_power_factor", 0.03)],
    "head_of_state": [("stability_factor", 0.03), ("political_power_factor", 0.03)],
    "chief_ideologue": [("drift_defence_factor", 0.10), ("stability_factor", 0.02)],
    "iron_shurik": [("political_power_factor", 0.05), ("police_cost_multiplier_modifier", -0.05)],
    "chekist": [("corruption_cost_factor", -0.05), ("drift_defence_factor", 0.05)],
    "marshal_of_the_soviet_union": [("army_org_factor", 0.03), ("war_support_factor", 0.03)],
    "the_armourer": [("production_speed_arms_factory_factor", 0.05), ("equipment_cost_multiplier_modifier", -0.03)],
    "leningrad_boss": [("production_speed_buildings_factor", 0.03), ("stability_factor", 0.02)],
    "apparatchik": [("political_power_factor", 0.05), ("bureaucracy_cost_multiplier_modifier", -0.05)],
    "new_generation": [("research_speed_factor", 0.03), ("productivity_growth_modifier", 0.02)],
    "four_times_hero": [("political_power_factor", 0.05), ("stability_factor", 0.02)],
    "ailing_leader": [("political_power_factor", -0.05), ("stability_factor", 0.03)],
    "president_of_the_ussr": [("political_power_factor", 0.05), ("stability_factor", 0.03)],
    "vozhd": [("political_power_factor", 0.10), ("stability_factor", 0.03), ("drift_defence_factor", 0.10)],
    "chekist_from_baku": [("political_power_factor", 0.03), ("corruption_cost_factor", -0.05)],
    "strong_hand": [("stability_factor", 0.03), ("police_cost_multiplier_modifier", -0.05)],
    "moscow_boss": [("political_power_factor", 0.03), ("production_speed_buildings_factor", 0.02)],
    "new_vozhd": [("political_power_factor", 0.08), ("war_support_factor", 0.03)],
    "head_of_the_house": [("stability_factor", 0.05), ("political_power_factor", 0.03)],
}


def traits_file():
    L = [HEADER, "leader_traits = {"]
    for t, mods in TRAIT_MODS.items():
        tid = PFX + t
        L += [f"{tid} = {{", "random = no", ""] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}"]
        LOC[tid] = TRAITS[tid]
    L.append("}")
    used = set(R.traits) | {t for ts in E.GENSEC_TRAITS.values() for t in ts}
    assert used <= {PFX + t for t in TRAIT_MODS}, used - {PFX + t for t in TRAIT_MODS}
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- on_actions
ON_ACTIONS = HEADER + """on_actions = {
	on_startup = {
		effect = {
			# on_startup has no country scope: enter SOV explicitly (only the 1970 history block initialises it)
			if = {
				limit = { country_exists = SOV SOV = { has_country_flag = COLDWAR_SOV_initialized } }
				SOV = { COLDWAR_SOV_setup_politburo = yes }
			}
		}
	}

	on_monthly_SOV = {
		effect = {
			if = {
				limit = { original_tag = SOV has_country_flag = COLDWAR_SOV_initialized }
				COLDWAR_SOV_monthly_cohesion = yes
				COLDWAR_SOV_monthly_bop_drift = yes
				COLDWAR_SOV_monthly_aid = yes
			}
		}
	}
}
"""


# ---------------------------------------------------------------- scripted localisation
def sl(name, entries, fallback=None):
    L = ["defined_text = {", f"name = {name}"]
    for trig, key, text in entries:
        LOC[key] = text
        L += ["text = {", "trigger = {"] + trig + ["}", f"localization_key = {key}", "}"]
    if fallback:
        key, text = fallback
        LOC[key] = text
        L += ["text = {", f"localization_key = {key}", "}"]
    L.append("}")
    return L


def scripted_loc_file():
    from cw_layout import BYID
    L = [HEADER]
    g = lambda v: f"check_variable = {{ global.{PFX}{v} }}"
    props = ["a §Ycivilian factory§!", "§Yinfrastructure§!", "a §Ypower station§!", "an §Yagriculture district§!", "a §Ymilitary factory§!"]
    # the running vote (vote_*) and the last counted vote (last_*, read by the result news)
    for fn, ty, su, sc, pr, kp in ((f"{PFX}GetVoteSubject", "vote_type", "vote_subject", "vote_succession", "GetProposer", "vs"),
                                   (f"{PFX}GetLastVoteSubject", "last_type", "last_subject", "last_succession", "GetLastProposer", "ls")):
        ent = []
        for n, (fid, lean) in enumerate(REPUBLICS.RESOLUTIONS, start=1):
            ent.append(([g(f"{ty} = 1"), g(f"{su} = {n}")], f"{PFX}{kp}_res_{n}", f"the resolution §Y{BYID[PFX + fid]['name']}§!"))
        for i, (k, n, m) in enumerate(PLAN_PRIOS, start=1):
            ent.append(([g(f"{ty} = 2"), g(f"{su} = {i}")], f"{PFX}{kp}_plan_{i}", f"the priority of the [COLDWAR_SOV_GetPlanName]: §Y{n}§!"))
        for k in KEYS[:-1]:
            name = E.GENSEC[k][0]
            ent.append(([g(f"{ty} = 3"), g(f"{su} = {KIDX[k]}"), g(f"{sc} = 1")], f"{PFX}{kp}_succ_{k}", f"the succession: §Y{name}§! as General Secretary"))
            ent.append(([g(f"{ty} = 3"), g(f"{su} = {KIDX[k]}")], f"{PFX}{kp}_plenum_{k}", f"a change of leadership: §Y{name}§! as the new General Secretary"))
        for i, p in enumerate(props, start=1):
            ent.append(([g(f"{ty} = 4"), g(f"{su} = {i}")], f"{PFX}{kp}_prop_{i}",
                        f"a proposal of the [COLDWAR_SOV_{pr}]: {p} built in the republic at Moscow's expense"))
        ent.append(([g(f"{ty} = 4"), g(f"{su} = 6")], f"{PFX}{kp}_prop_6", f"a proposal of the [COLDWAR_SOV_{pr}]: §Yrelief from the plan§! for two years"))
        ent.append(([g(f"{ty} = 4"), g(f"{su} = 7")], f"{PFX}{kp}_prop_7", f"a proposal of the [COLDWAR_SOV_{pr}]: §Yprotection of its cadres§!"))
        L += sl(fn, ent, (f"{PFX}vs_unknown", "a question of the day"))
    L += sl(f"{PFX}GetVoteLean", [
        ([g("vote_type = 4")], f"{PFX}lean_prop", "are sceptical of the republics: three of them will vote in favour, four against. The General Secretary votes against."),
        ([g("vote_lean = -1")], f"{PFX}lean_ref", "vote with the reformers: the further the Politburo balance leans to reform, the more of them vote in favour. The General Secretary votes in favour."),
        ([g("vote_lean = 1")], f"{PFX}lean_orth", "vote with the orthodox: the further the Politburo balance leans to orthodoxy, the more of them vote in favour. The General Secretary votes in favour.")],
        (f"{PFX}lean_neutral", "are split: four of them will vote in favour. The General Secretary votes in favour."))
    L += sl(f"{PFX}GetGSVote", [([g("last_type = 4")], f"{PFX}gs_vote_no", "the General Secretary voted against.")],
            (f"{PFX}gs_vote_yes", "the General Secretary voted in favour."))
    L += sl(f"{PFX}GetVoteResult", [([f"has_global_flag = {PFX}last_passed"], f"{PFX}vote_passed_txt", "§GADOPTED§!")],
            (f"{PFX}vote_failed_txt", "§RREJECTED§!"))
    line = []
    seat = []
    for t in SSR:
        for v, txt in (("yes", "§Gin favour§!"), ("no", "§Ragainst§!"), ("abstain", "§Yabstained§!")):
            line.append(([f"original_tag = {t}", f"has_country_flag = {PFX}last_{v}"],
                         f"{PFX}vote_line_{t}_{v}", f"\\n  {SSR_NAME[t]}: {txt}"))
        seat.append(([f"original_tag = {t}", f"has_country_flag = {PFX}seat"], f"{PFX}seat_line_{t}", f"\\n  §Y{SSR_NAME[t]}§!"))
    L += sl(f"{PFX}GetVoteLine", line, (f"{PFX}empty", ""))
    L += sl(f"{PFX}GetSeatLine", seat, (f"{PFX}empty", ""))
    for fn, flag in (("GetProposer", "current_proposer"), ("GetLastProposer", "last_proposer"), ("GetAccused", "accused"), ("GetLastSeat", "last_seat")):
        L += sl(f"{PFX}{fn}", [([f"{t} = {{ has_country_flag = {PFX}{flag} }}"], f"{PFX}name_{t}", SSR_NAME[t]) for t in SSR],
                (f"{PFX}name_unknown", "republic"))
    L += sl(f"{PFX}GetCongress", [([g(f"congress = {c}")], f"{PFX}congress_{c}", f"{['XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII'][c - 24]} Congress")
                                  for c in range(24, 29)], (f"{PFX}congress_next", "next Congress"))
    L += sl(f"{PFX}GetPlanName", [([g(f"plan = {n}")], f"{PFX}plan_{n}", f"{r} Five-Year Plan ({y}-{y + 4})")
                                  for n, r, y in ((9, "Ninth", 1971), (10, "Tenth", 1976), (11, "Eleventh", 1981), (12, "Twelfth", 1986))],
            (f"{PFX}plan_8", "Eighth Five-Year Plan (1966-1970)"))
    L += sl(f"{PFX}GetBid", [([f"has_country_flag = {PFX}bid_{b}"], f"{PFX}bid_{b}_txt", f"\\n\\nApplication with a gift of §G{b}§! political power.") for b in (100, 50, 25)],
            (f"{PFX}bid_none_txt", "\\n\\nNo application."))
    L += sl(f"{PFX}GetKompromatResult", [([f"has_global_flag = {PFX}kompromat_proven"], f"{PFX}kompromat_proven_txt",
                                          "The accusations have been §Rconfirmed§!. The First Secretary has lost his seat in the Politburo, and his republic is in disgrace.")],
            (f"{PFX}kompromat_failed_txt", "The accusations could §Gnot be proven§!. The accuser is branded a slanderer until the next Party Congress."))
    L += sl(f"{PFX}GetProposal", [([f"check_variable = {{ {PFX}prop_type = 1 }}", f"check_variable = {{ {PFX}prop_building = {i} }}"],
                                   f"{PFX}proposal_{i}", f"{p} built in the republic at the Union's expense ({'0.8' if i == 5 else '0.5'}% of our GDP).")
                                  for i, p in enumerate(props, start=1)] +
            [([f"check_variable = {{ {PFX}prop_type = 2 }}"], f"{PFX}proposal_6", "§Yrelief from the plan§! for two years (the republic gains Plan Relief, we carry Plan Shortfall)."),
             ([f"check_variable = {{ {PFX}prop_type = 3 }}"], f"{PFX}proposal_7", "§Yprotection of its cadres§! from any investigation until the next Party Congress.")],
            (f"{PFX}proposal_unknown", "a request."))
    L += sl(f"{PFX}GetSessionState", [
        ([f"has_global_flag = {PFX}vote_running"], f"{PFX}state_vote", "§YThe Politburo is voting§! on [COLDWAR_SOV_GetVoteSubject]."),
        ([f"has_global_flag = {PFX}congress_open"], f"{PFX}state_congress", "§YThe [COLDWAR_SOV_GetCongress] is in session.§! Seats can change hands freely."),
        ([f"has_global_flag = {PFX}applications_open"], f"{PFX}state_applications", "§YApplications are open§! for the [COLDWAR_SOV_GetCongress].")],
        (f"{PFX}state_quiet", "The Politburo meets on 1 January and 1 July."))
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- events file
def ev_loc(eid, title, desc, opts):
    LOC[f"{eid}.t"] = title
    LOC[f"{eid}.d"] = desc
    for i, t in enumerate(opts):
        LOC[f"{eid}.{'abcdefghijklmnopqrstuvwxyz'[i]}"] = t


def events_file():
    L = [HEADER, f"add_namespace = {NS}", ""]
    for e in sorted(EV.EVENTS, key=lambda x: x["n"]):
        eid = f"{NS}.{e['n']}"
        kind = "news_event" if e.get("kind") == "news" else "country_event"
        L += [f"{kind} = {{", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d", f"picture = {e['pic']}", ""]
        if e.get("major"):
            L.append("major = yes")
        if e.get("trigger"):
            L += ["fire_only_once = yes"] if e.get("once") else []
            L += ["trigger = {"] + e["trigger"] + ["}", "mean_time_to_happen = {", f"days = {e['mtth']}"] + e.get("mtth_mods", []) + ["}"]
        else:
            L.append("is_triggered_only = yes")
            if e.get("ttrigger"):
                L += ["trigger = {"] + e["ttrigger"] + ["}"]
        if e.get("timeout"):
            L.append(f"timeout_days = {e['timeout']}")
        if e.get("hidden"):
            L.append("hidden = yes")
        if e.get("immediate"):
            L += ["", "immediate = {", f'log = "[GetDateText]: [Root.GetName]: event {eid}"'] + e["immediate"] + ["}"]
        L.append("")
        letters = "abcdefghijklmnopqrstuvwxyz"
        for i, (t, code, ai, trig) in enumerate(e["options"]):
            L += ["option = {", f"name = {eid}.{letters[i]}"]
            if trig:
                L += ["trigger = {"] + trig + ["}"]
            L += ["ai_chance = {", ai if isinstance(ai, str) else f"base = {ai}", "}"] + code + ["}"]
        L += ["}", ""]
        ev_loc(eid, e["title"], e["desc"], [x[0] for x in e["options"]])
    L += OF.offer_events(ev_loc)
    return "\n".join(block(L)) + "\n"
