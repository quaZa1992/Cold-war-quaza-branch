# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Ideas, dynamic modifiers, the Inner-German balance of power, opinion modifiers, leader traits, on_actions,
# scripted localisation and the events file of the GDR 1970 tree.
import re
from dg_common import *
import dg_effects as E
from dg_effects import R
import dg_offers as OF
import dg_events as EV
from dg_load import C, PROGS, PARTY, TRIG, TRAITS, OPINION_NAMES, LEADER_NAME, LEADER_KEYS, DYN, PARTY_SECTIONS
from dg_sys import TRUST_TIERS

IDEA_GFX = set(open(os.path.join(EGY, "idea_gfx.txt")).read().split())
PICK = json.load(open(os.path.join(HERE, "gfxsel", "gfx_pick.json"), encoding="utf-8"))["ideas"]
# ideas of the offers and decisions that the gfx pass did not see
PIC_EXTRA = {
    "gdr_advisers_ethiopia": "soviet_advisors", "gdr_engineers_mozambique": "generic_partnership", "mozambican_contract_workers": "blr_north_korea_workers",
    "gdr_ship_orders": "Generic_Ship_Company", "gdr_pipeline_builders": "arm_gasenetgry_idea", "dak_lak_plantations": "agrarian_economy_idea",
    "cultural_exchange": "generic_partnership", "common_security": "vl_treaty", "gdr_engineers": "generic_partnership",
    "open_socialist_borders": "blr_open_border_politics", "gdr_solidarity_shipments": "generic_partnership", "trained_workers_from_the_gdr": "arab_workers_union",
    "gdr_hospital": "generic_partnership", "gdr_trained_security": "blr_nationalsecurity_idea", "gdr_trucks_and_machinery": "State_led_economy",
    "nva_instructors": "german_advisors", "mfs_advisers": "blr_nationalsecurity_idea", "tropical_coffee": "ETH_coffee_exports",
    "gdr_arms_deliveries": "army_strengthened", "grain_contract": "agrarian_economy_idea", "grain_customer": "mercosur_trade",
    "yugoslav_partnership": "generic_partnership", "clean_air_treaty": "vl_treaty", "reconciliation_trade": "generic_partnership",
    "soviet_advisers_gdr": "soviet_advisors", "eastern_social_charter": "economy_housing", "intershop_network": "export_economy",
    "kombinat_contracts_chemistry": "industrial_focus", "kombinat_contracts_machines": "industrial_focus", "kombinat_contracts_electronics": "research_bonus",
    "housing_drive": "economy_housing",
}


def pic_of(iid):
    p = PICK.get(iid) or PIC_EXTRA.get(iid.replace(PFX, ""))
    assert p and p in IDEA_GFX, (iid, p)
    return p


def ideas_file():
    L = [HEADER, "ideas = {", "country = {"]
    for iid, d in R.ideas.items():
        LOC[iid] = d["name"]
        if d.get("desc"):
            LOC[iid + "_desc"] = d["desc"].replace('"', "'")
        L += [f"{iid} = {{", f"picture = {pic_of(iid)}", "allowed_civil_war = { always = yes }", "modifier = {"]
        L += [f"{k} = {fmt(v)}" for k, v in d["mods"]] + ["}", "}"]
        for k, _ in d["mods"]:
            modifier_loc(k)
    L += ["}", "}"]
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- dynamic modifiers
def party_of_prog(key):
    """programme key -> (enable trigger lines, title)"""
    if key in LEADER_KEYS:
        return [f"has_country_flag = {PFX}first_sec_{key}", "emerging_communist_state_are_in_power = yes"], f"{PROGS[key]['name']}"
    i = PARTY_SECTIONS[key]
    return [f"{TRIG[i]}_are_in_power = yes"], PROGS[key]["name"]


def dyn_file():
    L = [HEADER]
    for g, name in DYN.items():
        mod = f"{PFX}{g}_modifier"
        L += [f"{mod} = {{", f'icon = "GFX_idea_{pic_of(mod)}"', ""] + [f"{k} = {PFX}{g}_{k}" for k in R.dyn.get(mod, [])] + ["}", ""]
        for k in R.dyn.get(mod, []):
            modifier_loc(k)
        LOC[mod] = name
    for t, name, cond, mods in TRUST_TIERS:
        iid = f"{PFX}trust_{t}"
        pic = PICK.get(iid) or ("soviet_german_friendship" if t == "garrison_relief" else None)
        assert pic in IDEA_GFX, (iid, pic)
        L += [f"{iid} = {{", f'icon = "GFX_idea_{pic}"', "enable = {", cond, "}", ""] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}", ""]
        for k, _ in mods:
            modifier_loc(k)
        LOC[iid] = name
    for mod, keys in R.dyn.items():
        if not mod.endswith("_programme"):
            continue
        k = mod.replace(PFX, "").replace("_programme", "")
        en, title = party_of_prog(k)
        L += [f"{mod} = {{", f'icon = "GFX_idea_{pic_of(mod)}"', "enable = {", "original_tag = DDR"] + en + ["}", ""] + \
             [f"{x} = {mod}_{x}" for x in keys] + ["}", ""]
        for x in keys:
            modifier_loc(x)
        LOC[mod] = title
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- the Inner-German course (balance of power)
def _mods(text):
    return text


COURSE_RANGES = {
    "left": [("total_demarcation", "Total Demarcation", -1, -0.6, [("drift_defence_factor", 0.25), ("mdcw_cw_ideological_defence", 0.10), ("stability_factor", 0.03),
                                                                   ("trade_opinion_factor", -0.15), ("research_speed_factor", -0.03)]),
             ("demarcation", "Demarcation", -0.6, -0.2, [("drift_defence_factor", 0.10), ("trade_opinion_factor", -0.05)])],
    "right": [("rapprochement", "Rapprochement", 0.2, 0.6, [("trade_opinion_factor", 0.10), ("research_speed_factor", 0.02), ("tax_gain_multiplier_modifier", 0.02),
                                                            ("democratic_drift", 0.01)]),
              ("detente", "German-German Détente", 0.6, 1, [("trade_opinion_factor", 0.20), ("research_speed_factor", 0.04), ("tax_gain_multiplier_modifier", 0.05),
                                                           ("democratic_drift", 0.03), ("drift_defence_factor", -0.15), ("stability_factor", -0.03)])]}


def bop_file():
    b = E.COURSE_BOP
    LOC[b] = "The Inner-German Course"
    LOC[f"{b}_left_side"] = "Demarcation (Abgrenzung)"
    LOC[f"{b}_right_side"] = "Rapprochement (Annäherung)"
    LOC[f"{b}_mid_range"] = "Regulated Coexistence"
    L = [HEADER, f"{b} = {{", f"initial_value = {fmt(C['course']['initial'])}", f"left_side = {b}_left_side", f"right_side = {b}_right_side",
         f"decision_category = {PFX}german_question_category", "",
         "range = {", f"id = {b}_mid_range", "min = -0.2", "max = 0.2", "modifier = {", "political_power_factor = 0.03", "}", "}", ""]
    for side, icon in (("left", "GFX_SOV_bop_eastern"), ("right", "GFX_SOV_bop_westerns")):
        L += ["side = {", f"id = {b}_{side}_side", f"icon = {icon}"]
        for rid, name, lo, hi, mods in COURSE_RANGES[side]:
            LOC[f"{b}_{rid}"] = name
            L += ["range = {", f"id = {b}_{rid}", f"min = {fmt(lo)}", f"max = {fmt(hi)}", "modifier = {"] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}"]
            for k, _ in mods:
                modifier_loc(k)
            if any(k.startswith("mdcw_cw_") for k, _ in mods):
                # a range with Cold War modifiers: the Cold War system caches them (mdcw_coldwar_imperia_hooks.md)
                L += ["on_deactivate = {", "hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }", "}"]
                if rid != "detente":
                    L += ["on_activate = {", "hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }", "}"]
            if rid == "detente":
                L += ["on_activate = {", "if = {", f"limit = {{ has_country_flag = {PFX}initialized NOT = {{ has_country_flag = {PFX}bonns_embrace_cooldown }} }}",
                      f"set_country_flag = {{ flag = {PFX}bonns_embrace_cooldown days = 730 }}",
                      f"country_event = {{ id = {NS}.{EV.EV[PFX + 'bonns_embrace']} days = 1 }}", "}", "}"]
            L.append("}")
        L += ["}", ""]
    L.append("}")
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- opinion modifiers and traits
def opinion_file():
    L = [HEADER, "opinion_modifiers = {"]
    allm = dict(R.opinions)
    names = dict(OPINION_NAMES)
    for k, (v, n) in OF.OPINION_EXTRA.items():
        allm[k] = v
        names[k] = n
    for k, v in sorted(allm.items()):
        L += [f"{k} = {{", f"value = {v}"] + (["decay = 0.25"] if abs(v) >= 20 else []) + ["}"]
        LOC[k] = names[k]
    L.append("}")
    return "\n".join(block(L)) + "\n"


TRAIT_MODS = {
    "ulb_founder_of_the_republic": [("political_power_factor", 0.05), ("research_speed_factor", 0.02)],
    "hon_man_of_the_apparatus": [("political_power_factor", 0.05), ("bureaucracy_cost_multiplier_modifier", -0.05)],
    "sto_the_administrator": [("stability_factor", 0.02), ("production_speed_buildings_factor", 0.03)],
    "mit_economic_czar": [("productivity_growth_modifier", 0.02), ("political_power_factor", 0.02)],
    "hag_keeper_of_the_doctrine": [("drift_defence_factor", 0.10), ("stability_factor", 0.02)],
    "hof_army_general": [("army_org_factor", 0.03), ("war_support_factor", 0.03)],
    "hof_marshal_of_the_gdr": [("army_morale_factor", 0.05), ("planning_speed", 0.05)],
    "lam_the_gdrs_kennedy": [("stability_factor", 0.03), ("political_power_factor", 0.03)],
    "kro_moscows_man": [("political_power_factor", 0.03), ("drift_defence_factor", 0.05)],
    "kre_the_fdj_generation": [("political_power_factor", 0.03), ("production_speed_buildings_factor", 0.02)],
    "mod_the_dresden_reformer": [("research_speed_factor", 0.02), ("bureaucracy_cost_multiplier_modifier", -0.05)],
}


def traits_file():
    L = [HEADER, "leader_traits = {"]
    for t, mods in TRAIT_MODS.items():
        tid = PFX + t
        L += [f"{tid} = {{", "random = no", ""] + [f"{k} = {fmt(v)}" for k, v in mods] + ["}"]
        for k, _ in mods:
            modifier_loc(k)
        LOC[tid] = TRAITS[tid]
    L.append("}")
    assert set(R.traits) <= {PFX + t for t in TRAIT_MODS}, set(R.traits) - {PFX + t for t in TRAIT_MODS}
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- on_actions
ON_ACTIONS = HEADER + """on_actions = {
	on_monthly_DDR = {
		effect = {
			if = {
				limit = { original_tag = DDR has_country_flag = COLDWAR_DDR_initialized }
				COLDWAR_DDR_monthly = yes
				COLDWAR_DDR_monthly_plan = yes
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
    L = [HEADER]
    L += sl(f"{PFX}GetCandidate", [([f"check_variable = {{ global.{PFX}cc_candidate = {i + 1} }}"], f"{PFX}candidate_{k}", LEADER_NAME[k])
                                   for i, k in enumerate(LEADER_KEYS)], (f"{PFX}candidate_unknown", "a new candidate"))
    return "\n".join(block(L)) + "\n"


# ---------------------------------------------------------------- events file
OPT_LETTERS = "abcefghijklmnopqrsuvwxyz"   # option keys skip "d" and "t" (<event>.d / .t are description and title)


def ev_loc(eid, title, desc, opts):
    LOC[f"{eid}.t"] = title
    LOC[f"{eid}.d"] = desc
    for i, t in enumerate(opts):
        LOC[f"{eid}.{OPT_LETTERS[i]}"] = t


def events_file():
    L = [HEADER, f"add_namespace = {NS}", ""]
    for e in sorted(EV.EVENTS, key=lambda x: x["n"]):
        eid = f"{NS}.{e['n']}"
        kind = "news_event" if e.get("kind") == "news" else "country_event"
        L += [f"{kind} = {{", f"id = {eid}", f"title = {eid}.t", f"desc = {eid}.d", f"picture = {e['pic']}", ""]
        if e.get("trigger"):
            L += ["fire_only_once = yes"] if e.get("once") else []
            L += ["trigger = {"] + e["trigger"] + ["}", "mean_time_to_happen = {", f"days = {e['mtth']}", "}"]
        else:
            L.append("is_triggered_only = yes")
            if e.get("ttrigger"):
                L += ["trigger = {"] + e["ttrigger"] + ["}"]
        if e.get("hidden"):
            L.append("hidden = yes")
        L += ["", "immediate = {", f'log = "[GetDateText]: [Root.GetName]: event {eid}"'] + e.get("immediate", []) + ["}", ""]
        for i, (t, code, ai, trig) in enumerate(e["options"]):
            L += ["option = {", f"name = {eid}.{OPT_LETTERS[i]}"]
            if trig:
                L += ["trigger = {"] + trig + ["}"]
            L += ["ai_chance = {", ai if isinstance(ai, str) else f"base = {ai}", "}"] + code + ["}"]
        L += ["}", ""]
        ev_loc(eid, e["title"], e["desc"], [x[0] for x in e["options"]])
    L += OF.offer_events(ev_loc)
    return "\n".join(block(L)) + "\n"
