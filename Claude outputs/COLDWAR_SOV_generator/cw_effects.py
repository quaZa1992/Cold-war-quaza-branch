# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Compiles the effect dicts of the design (sov_dsl.py) into Clausewitz code (MD 2000 style).
import re
from cw_common import *
from cw_layout import BYID, FOCI, IDEAS, PROGS, OFFERS, EVENTS, DECISIONS, OPINIONS, TRAITS, PARTY, TRIG, DSL

SUBIDEO = {0: "Western_Autocracy", 1: "conservatism", 2: "liberalism", 3: "socialism", 4: "communist_state",
           5: "anarchist_communism", 6: "Conservative", 7: "Autocracy", 8: "Mod_Vilayat_e_Faqih", 9: "Vilayat_e_Faqih",
           10: "Kingdom", 11: "Caliphate", 12: "Neutral_Muslim_Brotherhood", 13: "Neutral_Autocracy",
           14: "Neutral_conservatism", 15: "oligarchism", 16: "Neutral_Libertarian", 17: "Neutral_green",
           18: "neutral_Social", 19: "Neutral_Communism", 20: "Nat_Populism", 21: "Nat_Fascism", 22: "Nat_Autocracy",
           23: "Monarchist"}
GROUP_TRAIT = {range(0, 4): "western", range(4, 10): "emerging", range(10, 12): "salafist",
               range(12, 20): "neutrality", range(20, 24): "nationalist"}


def ideology_trait(i):
    for r, g in GROUP_TRAIT.items():
        if i in r:
            return f"{g}_{SUBIDEO[i]}"


# English leader names and existing 1970 portraits
LEADER_EN = {
    "Leonid Brezhnev": ("Leonid Brezhnev", "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds"),
    "Pyotr Siuda": ("Pyotr Siuda", None), "Sergei Trapeznikov": ("Sergei Trapeznikov", None),
    "Alexander Shelepin": ("Alexander Shelepin", "gfx/leaders/mdcw_historical_pool/SOV_alexander_shelepin.dds"), "Dzhermen Gvishiani": ("Dzhermen Gvishiani", None),
    "Vladimir Poremsky": ("Vladimir Poremsky", None), "Andrei Sakharov": ("Andrei Sakharov", None),
    "Roy Medvedev": ("Roy Medvedev", None), "Nikolai Baibakov": ("Nikolai Baibakov", None),
    "Aleksandr Solzhenitsyn": ("Aleksandr Solzhenitsyn", None), "Nikolai Shchelokov": ("Nikolai Shchelokov", None),
    "Nikolai Shmelyov": ("Nikolai Shmelyov", None), "Grigory Galazy": ("Grigory Galazy", None),
    "Alexander Yakovlev": ("Alexander Yakovlev", None), "Pyotr Shelest": ("Pyotr Shelest", "gfx/leaders/UKR/UKR_Coldwar_Petro_Shelest.dds"),
    "Dmitry Polyansky": ("Dmitry Polyansky", None), "Committee of National Rebirth": ("Committee of National Rebirth", None),
    "Andrei Grechko": ("Andrei Grechko", "gfx/leaders/mdcw_historical_pool/SOV_andrei_grechko.dds"), "Grand Duke Vladimir Kirillovich": ("Grand Duke Vladimir Kirillovich", None),
    "Vladimir Kirillovich": ("Emperor Vladimir III", None), "Mikhail Gorbachev": ("Mikhail Gorbachev", "gfx/leaders/SOV/mikhail_gorbachev.dds"),
    "Heydar Aliyev": ("Heydar Aliyev", "gfx/leaders/AZE/AZE_Coldwar_Heydar_Aliyev.dds"), "Viktor Grishin": ("Viktor Grishin", "gfx/leaders/mdcw_historical_pool/SOV_viktor_grishin.dds"),
}
# General Secretaries (key -> English name, portrait, death date or None); portraits from gfx/leaders/mdcw_historical_pool (19.10.2026)
GENSEC = {
    "bre": ("Leonid Brezhnev", "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds", "1982.11.10"),
    "kos": ("Alexei Kosygin", "gfx/leaders/mdcw_historical_pool/SOV_alexei_kosygin.dds", "1980.12.18"), "pod": ("Nikolai Podgorny", "gfx/leaders/mdcw_historical_pool/SOV_nikolai_podgorny.dds", "1983.1.12"),
    "sus": ("Mikhail Suslov", "gfx/leaders/mdcw_historical_pool/SOV_mikhail_suslov.dds", "1982.1.25"), "she": ("Alexander Shelepin", "gfx/leaders/mdcw_historical_pool/SOV_alexander_shelepin.dds", None),
    "and": ("Yuri Andropov", "gfx/leaders/mdcw_historical_pool/SOV_yuri_andropov.dds", "1984.2.9"), "gre": ("Andrei Grechko", "gfx/leaders/mdcw_historical_pool/SOV_andrei_grechko.dds", "1976.4.26"),
    "ust": ("Dmitry Ustinov", "gfx/leaders/mdcw_historical_pool/SOV_dmitry_ustinov.dds", "1984.12.20"), "gro": ("Grigory Romanov", "gfx/leaders/mdcw_historical_pool/SOV_grigory_romanov.dds", None),
    "che": ("Konstantin Chernenko", "gfx/leaders/coldwar/chernenko.dds", "1985.3.10"),
    "gor": ("Mikhail Gorbachev", "gfx/leaders/SOV/mikhail_gorbachev.dds", None),
}
GENSEC_LEAN = {"bre": 0, "kos": -1, "pod": 0, "sus": 1, "she": 1, "and": 0, "gre": 1, "ust": 1, "gro": 1, "che": 1, "gor": -1}
GENSEC_TRAITS = {"bre": [], "kos": ["COLDWAR_SOV_economist_premier"], "pod": ["COLDWAR_SOV_head_of_state"],
                 "sus": ["COLDWAR_SOV_chief_ideologue"], "she": ["COLDWAR_SOV_iron_shurik"], "and": ["COLDWAR_SOV_chekist"],
                 "gre": ["COLDWAR_SOV_marshal_of_the_soviet_union"], "ust": ["COLDWAR_SOV_the_armourer"],
                 "gro": ["COLDWAR_SOV_leningrad_boss"], "che": ["COLDWAR_SOV_apparatchik"], "gor": ["COLDWAR_SOV_new_generation"]}
# stand-ins (Enes, 17.10.2026): when a candidate has died, a man of the same camp carries his plenum focus and his tree
# key -> (English name, portrait or None, leader trait)
STANDIN = {"kos": ("Nikolai Ryzhkov", "gfx/leaders/mdcw_historical_pool/SOV_nikolai_ryzhkov.dds", "COLDWAR_SOV_economist_premier"),
           "pod": ("Vasily Kuznetsov", "gfx/leaders/mdcw_historical_pool/SOV_vasily_kuznetsov.dds", "COLDWAR_SOV_head_of_state"),
           "sus": ("Mikhail Zimyanin", None, "COLDWAR_SOV_chief_ideologue"),
           "and": ("Heydar Aliyev", "gfx/leaders/AZE/AZE_Coldwar_Heydar_Aliyev.dds", "COLDWAR_SOV_chekist_from_baku"),
           "gre": ("Nikolai Ogarkov", "gfx/leaders/mdcw_historical_pool/SOV_nikolai_ogarkov.dds", "COLDWAR_SOV_marshal_of_the_soviet_union"),
           "ust": ("Leonid Smirnov", None, "COLDWAR_SOV_the_armourer"),
           "che": ("Viktor Grishin", "gfx/leaders/mdcw_historical_pool/SOV_viktor_grishin.dds", "COLDWAR_SOV_moscow_boss")}
# party leaders who may have died by the time a party takes power: (death date, replacement)
LEADER_FALLBACK = {"Andrei Grechko": ("1976.4.26", "Nikolai Ogarkov")}


class Reg:
    def __init__(self):
        self.ideas = {}        # id -> dict(name, mods, days)
        self.dyn = collections.OrderedDict()   # modifier name -> ordered keys
        self.flags = set()
        self.events = set()
        self.offers = set()
        self.opinions = {}
        self.traits = set()
        self.decisions = set()
        self.unhandled = []
        self.resolutions = {}  # focus short -> lean
        self.tech_names = set()


R = Reg()
for iid, d in IDEAS.items():
    R.ideas[iid] = dict(name=d["name"], mods=list(d["mods"].items()), days=d.get("days"))
for k, (v, trade) in OPINIONS.items():
    R.opinions[k] = v


def tt(key, text):
    k = f"{PFX}{key}_tt"
    LOC[k] = text
    return f"custom_effect_tooltip = {k}"


CW_RECALC = "hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }"
# opinion keys whose sign the design reuses the other way round: the negative use gets its own modifier
OPINION_FLIP = {f"{PFX}human_rights": (f"{PFX}human_rights_criticism", -10, "Human Rights Criticism"),
                f"{PFX}eurocommunism": (f"{PFX}eurocommunist_rift", -10, "The Eurocommunist Rift"),
                f"{PFX}detente": (f"{PFX}detente_setback", -10, "Detente Setback")}
OPINION_FLIP_NAMES = {}


def dyn_change(modname, varprefix, mods):
    out = [f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {modname} }} }} }} hidden_effect = {{ add_dynamic_modifier = {{ modifier = {modname} }} }} }}",
           f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {modname} }}"]
    keys = R.dyn.setdefault(modname, [])
    for k, v in mods.items():
        if k not in keys:
            keys.append(k)
        out.append(f"add_to_variable = {{ {varprefix}_{k} = {fmt(v)} tooltip = {mod_tt_key(k)} }}")
    out.append(f"hidden_effect = {{ force_update_dynamic_modifier = yes }}")
    if any(k.startswith("mdcw_cw_") for k in mods):
        # Cold War capacities and modifiers are cached by the Cold War system: recalculate at once (audit P1)
        out.append(CW_RECALC)
    if "mdcw_cw_market_exposure" in mods or "globalism_equilibrium" in mods:
        out.append("hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_update_world_market = yes } }")
    return out


DYN_GROUP = {"party_state": "party_state", "gosplan": "gosplan", "armed_forces": "armed_forces", "union": "union", "commonwealth": "commonwealth"}


def faction(f, n):
    return [f"set_temp_variable = {{ temp_opinion = {fmt(n)} }}", f"{PFX}change_{f}_opinion_exact = yes"]


def party_pop(idx, p, o):
    return [f"set_temp_variable = {{ party_index = {idx} }}",
            f"set_temp_variable = {{ party_popularity_increase = {fmt(p)} }}",
            f"set_temp_variable = {{ temp_outlook_increase = {fmt(o)} }}",
            "change_relative_party_popularity = yes"]


def gdp(effect, share):
    return [f"set_temp_variable = {{ {PFX}gdp_share = {fmt(round(share, 4))} }}", f"{PFX}{effect} = yes"]


def opinion(tag, key):
    return [f"if = {{ limit = {{ country_exists = {tag} }} add_opinion_modifier = {{ target = {tag} modifier = {key} }} }}"]


def bop(v):
    side = f"{PFX}politburo_bop_left_side" if v < 0 else f"{PFX}politburo_bop_right_side"
    return [f"add_power_balance_value = {{ id = {PFX}politburo_bop value = {fmt(v)} tooltip_side = {side} }}",
            f"hidden_effect = {{ add_to_variable = {{ {PFX}bop = {fmt(v)} }} clamp_variable = {{ var = {PFX}bop min = -1 max = 1 }} }}"]


def cohesion(v):
    return [f"set_temp_variable = {{ {PFX}cohesion_delta = {fmt(v)} }}", f"{PFX}change_union_cohesion = yes"]


def leader_lines(idx, name, trait=None):
    en, pic = LEADER_EN.get(name, (name, None))
    traits = [ideology_trait(idx)] + ([trait] if trait else [])
    p = f' picture = "{pic}"' if pic else ""
    return [f'create_country_leader = {{ name = "{en}"{p} ideology = {SUBIDEO[idx]} traits = {{ {" ".join(traits)} }} }}']


def new_leader_tt(name):
    key = f"new_leader_{slug(name)}"
    LOC[f"{PFX}{key}_tt"] = f"§Y{name}§! becomes the leader of [ROOT.GetNameDef]."
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def ruling_party(f, e):
    i, name = e["i"], e["leader"]
    if i == 4:
        # back to the CPSU: the living leader of the historical line takes over the Party again
        LOC[f"{PFX}restore_party_rule_tt"] = "The §YCommunist Party of the Soviet Union§! returns to power under the General Secretary of the historical line."
        return [f"custom_effect_tooltip = {PFX}restore_party_rule_tt", f"{PFX}restore_party_rule = yes"]
    en = LEADER_EN.get(name, (name, None))[0]
    out = [new_leader_tt(en), "hidden_effect = {", "retire_country_leader = yes"]
    if name in LEADER_FALLBACK:
        d, alt = LEADER_FALLBACK[name]
        out += [f"if = {{ limit = {{ date < {d} }}"] + leader_lines(i, name) + ["}", "else = {"] + leader_lines(i, alt) + ["}"]
    else:
        out += leader_lines(i, name)
    out += ["}", f"set_temp_variable = {{ rul_party_temp = {i} }}", "change_ruling_party_effect = yes"]
    return out


INFL_TAGS_OK = {"RAJ", "VIE", "MON", "AFG", "PAK", "EGY", "SYR", "SOM", "ETH", "AGL", "MOZ", "CUB", "YEM", "SYE"}


def influence(tags, v):
    out = []
    for t in tags:
        out += [f"if = {{ limit = {{ country_exists = {t} }}", "set_temp_variable = { tag_index = ROOT.id }",
                f"set_temp_variable = {{ influence_target = {t}.id }}", f"set_temp_variable = {{ percent_change = {fmt(v)} }}",
                "change_influence_percentage = yes", "}"]
    return out


def cw_join(al):
    code = {"west": (1, "mdcw_cw_can_join_west"), "na": (0, None), "soviet": (2, "mdcw_cw_can_join_soviet")}[al]
    LOC[f"{PFX}cw_partners_keep_bloc_tt"] = "Countries under our protection that are led by players keep their own Cold War bloc; computer-led ones follow us."
    # multiplayer: mdcw_cw_change_alignment moves every subject with its overlord - human partners keep their bloc (audit P1)
    body = ["hidden_effect = { every_subject_country = { limit = { is_ai = no has_country_flag = mdcw_cw_initialized } "
            "set_variable = { COLDWAR_SOV_keep_alignment = mdcw_cw_alignment } } }",
            f"set_temp_variable = {{ mdcw_cw_new_alignment = {code[0]} }}", "set_temp_variable = { mdcw_cw_t_free = 1 }", "mdcw_cw_change_alignment = yes",
            "set_temp_variable = { mdcw_cw_t_free = 0 }", f"custom_effect_tooltip = {PFX}cw_partners_keep_bloc_tt",
            "hidden_effect = {", "every_subject_country = {", "limit = { has_variable = COLDWAR_SOV_keep_alignment }",
            "set_variable = { mdcw_cw_alignment = COLDWAR_SOV_keep_alignment }", "clear_variable = COLDWAR_SOV_keep_alignment",
            "mdcw_cw_recalculate_country = yes", "}", "mdcw_cw_rebuild_blocs = yes", "mdcw_cw_refresh_all_bloc_effects = yes", "}"]
    if code[1]:
        return [f"if = {{ limit = {{ {code[1]} = yes }}"] + body + ["}"]
    return [f"if = {{ limit = {{ NOT = {{ check_variable = {{ mdcw_cw_alignment = 0 }} }} }}"] + body + ["}"]


def compile_effect(e, f):
    k = e["k"]
    sid = short(f["id"])
    if k == "pp":
        return [f"add_political_power = {e['v']}"]
    if k == "stab":
        return [f"add_stability = {fmt(e['v'])}"]
    if k == "ws":
        return [f"add_war_support = {fmt(e['v'])}"]
    if k == "fac":
        return faction(e["f"], e["v"])
    if k == "party":
        return party_pop(e["i"], e["v"], e["o"])
    if k == "outlook":
        return [f"set_temp_variable = {{ {PFX}outlook_id = {e['o']} }}", f"set_temp_variable = {{ {PFX}outlook_amount = {fmt(e['v'])} }}",
                f"{PFX}change_outlook_popularity = yes"]
    if k == "dyn":
        g = e["g"]
        return dyn_change(f"{PFX}{g}_modifier", f"{PFX}{g}", e["mods"])
    if k == "prog":
        g = e["g"]
        return dyn_change(f"{PFX}{g}_programme", f"{PFX}{g}_programme", e["mods"])
    if k == "idea":
        iid, days = e["id"], e.get("days")
        if e.get("swap") or e.get("swap_id"):
            old = e.get("swap_id") or [x for x, d in IDEAS.items() if d["name"] == e["swap"]][0]
            return [f"if = {{ limit = {{ has_idea = {old} }} swap_ideas = {{ remove_idea = {old} add_idea = {iid} }} }}",
                    f"else = {{ add_ideas = {iid} }}"]
        if days:
            return [f"add_timed_idea = {{ idea = {iid} days = {days} }}"]
        return [f"add_ideas = {iid}"]
    if k == "rmidea":
        return [f"if = {{ limit = {{ has_idea = {e['id']} }} remove_ideas = {e['id']} }}"]
    if k == "coh":
        return cohesion(e["v"])
    if k == "tech":
        R.tech_names.add(f["id"])
        cats = " ".join(f"category = {c}" for c in e["cats"])
        return [f"add_tech_bonus = {{ name = {f['id']} bonus = {fmt(e['b'])} uses = {e['n']} {cats} }}"]
    if k == "bop":
        return bop(e["v"])
    if k == "build":
        out = ["set_temp_variable = { skip_payment = 1 }", f"{e['helper']} = yes", "set_temp_variable = { skip_payment = 0 }"]
        if e.get("cost"):
            out += gdp("pay_gdp_share", e["cost"])
        return out
    if k == "tension":
        return [f"set_temp_variable = {{ mdcw_cw_tension_delta = {fmt(e['v'])} }}", "mdcw_cw_add_tension = yes"]
    if k == "offer":
        R.offers.add(e["key"])
        return [f"{e['key']} = yes"]
    if k == "op":
        key = e["key"]
        base = R.opinions.get(key, e["v"])
        if (base > 0) != (e["v"] > 0):
            fk, fv, fname = OPINION_FLIP.get(key, (f"{key}_{'strained' if e['v'] < 0 else 'improved'}", e["v"], None))
            R.opinions.setdefault(fk, fv)
            OPINION_FLIP_NAMES[fk] = fname
            key = fk
        R.opinions.setdefault(key, e["v"])
        return opinion(e["tag"], key)
    if k == "rp":
        return ruling_party(f, e)
    if k == "gdp":
        return gdp("pay_gdp_share", e["v"])
    if k == "gdp_gain":
        return gdp("receive_gdp_share", e["v"])
    if k == "debt":
        return gdp("receive_gdp_share", e["v"]) + gdp("change_debt_gdp_share", e["v"])
    if k == "corr":
        n = abs(e["v"])
        return [f"{e['helper']} = yes"] * n
    if k == "heir":
        return [f"{PFX}set_heir_{e['key']} = yes"]
    if k == "decision":
        R.decisions.add(e["key"])
        return [f"set_country_flag = {e['key']}_unlocked", f"custom_effect_tooltip = {e['key']}_unlock_tt"]
    if k == "event":
        R.events.add(e["key"])
        n = EVENT_ID[e["key"]]
        if e["key"] == f"{PFX}warsaw_discipline":
            return [f"if = {{ limit = {{ country_exists = POL }} POL = {{ country_event = {{ id = {NS}.{n} days = 1 }} }} }}"]
        if e["key"] == f"{PFX}lop_nur_world":
            return [f"news_event = {{ id = {NS}.{n} hours = 12 }}"]
        return [f"country_event = {{ id = {NS}.{n} days = 1 }}"]
    if k == "space":
        return ["add_space_program_progress = yes"]
    if k == "sp":
        p = e["project"]
        return [f"if = {{ limit = {{ NOT = {{ is_special_project_completed = sp:{p} }} }} sp:{p} = {{ add_project_progress_ratio = {fmt(e['v'])} }} }}"]
    if k == "xp":
        return [f"{e['kind']}_experience = {e['v']}"]
    if k == "cp":
        return [f"add_command_power = {e['v']}"]
    if k == "mastery":
        return [f"add_mastery = {{ amount = {e['v']} folder = {e['folder']} }}"]
    if k == "manpower":
        return [f"add_manpower = {e['v']}"]
    if k == "infl":
        return influence(e["tags"], e["v"])
    if k == "elections":
        return [f"{PFX}allow_elections = yes"] if e["on"] else [f"{PFX}suspend_elections = yes"]
    if k == "setlaw":
        return [f"add_ideas = {e['idea']}"]
    if k == "law":
        return [f"{e['helper']} = yes"]
    if k == "cwjoin":
        return cw_join(e["al"])
    if k == "trait":
        R.traits.add(e["trait"])
        return [f"add_country_leader_trait = {e['trait']}"]
    if k == "leader":
        R.traits.add(e["trait"])
        if e["i"] == 4:   # heir without a tree of his own (Aliyev after Andropov, Grishin after Chernenko)
            return [f"{PFX}set_heir_{slug(e['name']).split('_')[-1]} = yes"]
        return [new_leader_tt(LEADER_EN[e['name']][0]), "hidden_effect = {", "retire_country_leader = yes"] + leader_lines(e["i"], e["name"], e["trait"]) + ["}"]
    if k == "flag":
        R.flags.add(e["f"])
        return [f"set_country_flag = {e['f']}"]
    if k == "raw":
        return list(e["code"])
    if k in ("note", "custom", "gensec"):
        from cw_manual import manual
        return manual(f, e)
    raise KeyError(k)


EVENT_ID = {f"{PFX}intro": 1, f"{PFX}lenin_centenary": 2, f"{PFX}constitution_1977": 3, f"{PFX}moonshot": 4,
            f"{PFX}solzhenitsyn_expelled": 5, f"{PFX}olympics": 6, f"{PFX}helsinki_groups": 7, f"{PFX}lop_nur_world": 8,
            f"{PFX}warsaw_discipline": 9}
