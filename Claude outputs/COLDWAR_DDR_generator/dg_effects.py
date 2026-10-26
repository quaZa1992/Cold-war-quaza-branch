# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Compiles the effect dicts of the GDR design into Clausewitz code (MD 2000 style, like the Soviet generator).
import re
from dg_common import *
from dg_load import (BYID, FOCI, IDEAS, PROGS, OFFERS, EVENTS, DECISIONS, OPINIONS, OPINION_NAMES, TRAITS, PARTY, TRIG,
                     LADDERS, LEADER_NAME, SUBIDEO, ideology_trait, FACTION)

# MD tags (the design wrote ANG for Angola; MD's Angola is AGL)
TAG_FIX = {"ANG": "AGL"}


def tag(t):
    return TAG_FIX.get(t, t)


class Reg:
    def __init__(self):
        self.ideas = collections.OrderedDict()   # id -> dict(name, mods [(k, v)], days, desc, pic_key)
        self.dyn = collections.OrderedDict()     # modifier name -> ordered modifier keys
        self.flags_set = set()
        self.events = set()
        self.offers = set()
        self.opinions = {}
        self.traits = set()
        self.decisions = set()
        self.tech_names = set()
        self.ladder_ops = set()                  # (ladder, op)
        self.heirs = set()


R = Reg()
for iid, d in IDEAS.items():
    if iid.startswith(PFX):
        R.ideas[iid] = dict(name=d["name"], mods=list(d["mods"].items()), days=d.get("days"), desc=d.get("desc", ""))
for k, v in OPINIONS.items():
    R.opinions[k] = v


def tt(key, text):
    """custom effect tooltip with an English text"""
    k = f"{PFX}{key}_tt"
    LOC[k] = text
    return f"custom_effect_tooltip = {k}"


def sign(v, pct=False, digits=2):
    if pct:
        s = f"{v * 100:+.{digits}f}".rstrip("0").rstrip(".") + "%"
    else:
        s = f"{v:+g}"
    return s


CW_RECALC = "hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }"


CW_MARKET = "hidden_effect = { if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_update_world_market = yes } }"
# after a dynamic-modifier line with a Cold War key: mdcw_cw_recalculate_country / update_world_market read modifier@<key>, so the
# dynamic modifier must be refreshed first (allowed deviation from MD: force_update only here, mdcw_coldwar_imperia_hooks.md)
CW_RECALC_DYN = "hidden_effect = { force_update_dynamic_modifier = yes if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_recalculate_country = yes } }"
CW_MARKET_DYN = "hidden_effect = { force_update_dynamic_modifier = yes if = { limit = { has_country_flag = mdcw_cw_initialized } mdcw_cw_update_world_market = yes } }"
CW_LINES = (CW_RECALC, CW_MARKET, CW_RECALC_DYN, CW_MARKET_DYN)


def cw_tail(lines):
    """one hidden Cold War update for a whole effect block (force_update first when a dynamic modifier changed)"""
    have = set(l for l in lines if l in CW_LINES)
    if not have:
        return []
    force = bool(have & {CW_RECALC_DYN, CW_MARKET_DYN})
    calls = []
    if have & {CW_RECALC, CW_RECALC_DYN}:
        calls.append("mdcw_cw_recalculate_country = yes")
    if have & {CW_MARKET, CW_MARKET_DYN}:
        calls.append("mdcw_cw_update_world_market = yes")
    return ["hidden_effect = { " + ("force_update_dynamic_modifier = yes " if force else "") +
            "if = { limit = { has_country_flag = mdcw_cw_initialized } " + " ".join(calls) + " } }"]
NEWLINE = "newline = yes"


def dyn_change(modname, varprefix, mods):
    """MD Russia form: one header per dynamic modifier, one add_to_variable per line with MD's <modifier>_tt, newline after the group.
    The modifier itself is added visibly elsewhere (country modifiers at the start, programmes in the entry focus of their tree)."""
    out = [f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {modname} }}"]
    keys = R.dyn.setdefault(modname, [])
    for k, v in mods.items():
        if k not in keys:
            keys.append(k)
        out.append(f"add_to_variable = {{ {varprefix}_{k} = {fmt(v)} tooltip = {mod_tt_key(k)} }}")
    out.append(NEWLINE)
    if any(k.startswith("mdcw_cw_") for k in mods) or "globalism_equilibrium" in mods:
        out.append(CW_RECALC_DYN)  # Cold War capacities are cached by the Cold War system
    if "mdcw_cw_market_exposure" in mods or "globalism_equilibrium" in mods:
        out.append(CW_MARKET_DYN)
    return out


def cw_hooks_for_ideas(lines):
    """an idea with mdcw_cw_* modifiers (or globalism/market exposure) that is added, swapped or removed needs the Cold War recalculation"""
    text = "\n".join(lines)
    out = []
    ladders = set(re.findall(r"COLDWAR_DDR_ladder_(\w+?)_(?:clear|down) = yes", text))
    ids = set(re.findall(r"\b(COLDWAR_DDR_\w+)\b", text))
    for name in ladders:
        if name in LADDERS:
            ids |= set(ladder_ids(name))
    keys = set()
    for i in ids:
        if i in R.ideas:
            keys |= {k for k, _ in R.ideas[i]["mods"]}
    if any(k.startswith("mdcw_cw_") for k in keys) or keys & {"globalism_equilibrium"}:
        out.append(CW_RECALC)
    if keys & {"mdcw_cw_market_exposure", "globalism_equilibrium"}:
        out.append(CW_MARKET)
    return out


def country_dyn(group, mods):
    return dyn_change(f"{PFX}{group}_modifier", f"{PFX}{group}", mods)


def prog_dyn(group, mods):
    return dyn_change(f"{PFX}{group}_programme", f"{PFX}{group}_programme", mods)


def faction(f, n):
    """MD's faction helper directly (MD doubles gains for autocracies - MD behaviour, priced into the design)"""
    return [f"set_temp_variable = {{ temp_opinion = {fmt(n)} }}", f"change_{f}_opinion = yes"]


def party_pop(idx, p, o):
    return [f"set_temp_variable = {{ party_index = {idx} }}",
            f"set_temp_variable = {{ party_popularity_increase = {fmt(p)} }}",
            f"set_temp_variable = {{ temp_outlook_increase = {fmt(o)} }}",
            "change_relative_party_popularity = yes"]


def outlook(o, v):
    return [f"set_temp_variable = {{ {PFX}outlook_id = {o} }}", f"set_temp_variable = {{ {PFX}outlook_amount = {fmt(v)} }}",
            f"{PFX}change_outlook_popularity = yes"]


def _gdp_share(var, share):
    """MD form (00_generic): set_temp_variable = { treasury_change = { value = gdp_total multiply = x } }"""
    return f"set_temp_variable = {{ {var} = {{ value = gdp_total multiply = {fmt(round(share, 5))} }} }}"


def pay(share):
    return [_gdp_share("treasury_change", -share), "modify_treasury_effect = yes"]


def receive(share):
    return [_gdp_share("treasury_change", share), "modify_treasury_effect = yes"]


def credit(share):
    """a Western or Soviet credit: money now, debt of the same size"""
    return receive(share) + [_gdp_share("debt_change", share), "modify_debt_effect = yes"]


def trust(v):
    """Moscow's Trust (0-100): the number in the tooltip is fixed, the change itself is clamped"""
    v = int(v)
    key = f"trust_{'plus' if v >= 0 else 'minus'}_{abs(v)}"
    col = "G" if v > 0 else "R"
    LOC[f"{PFX}{key}_tt"] = f"Moscow's Trust: §{col}{v:+d}§!"
    return [f"custom_effect_tooltip = {PFX}{key}_tt",
            f"hidden_effect = {{ set_temp_variable = {{ {PFX}trust_delta = {v} }} {PFX}change_trust = yes }}"]


COURSE_BOP = f"{PFX}german_course_bop"


def course(v):
    side = f"{COURSE_BOP}_left_side" if v < 0 else f"{COURSE_BOP}_right_side"
    return [f"add_power_balance_value = {{ id = {COURSE_BOP} value = {fmt(v)} tooltip_side = {side} }}",
            f"hidden_effect = {{ add_to_variable = {{ {PFX}course = {fmt(v)} }} clamp_variable = {{ var = {PFX}course min = -1 max = 1 }} }}"]


def tension(v):
    return [f"set_temp_variable = {{ mdcw_cw_tension_delta = {fmt(v)} }}", "mdcw_cw_add_tension = yes"]


def opinion(t, key):
    t = tag(t)
    return [f"if = {{ limit = {{ country_exists = {t} NOT = {{ tag = {t} }} }} add_opinion_modifier = {{ target = {t} modifier = {key} }} }}"]


def influence(tags, v):
    out = []
    for t in tags:
        t = tag(t)
        out += [f"if = {{ limit = {{ country_exists = {t} }}", "set_temp_variable = { tag_index = ROOT.id }",
                f"set_temp_variable = {{ influence_target = {t}.id }}", f"set_temp_variable = {{ percent_change = {fmt(v)} }}",
                "change_influence_percentage = yes", "}"]
    return out


def cw_join(al):
    if al == "west":
        LOC[f"{PFX}cw_join_west_tt"] = "The republic leaves the Soviet bloc and joins the §YWestern bloc§! of the Cold War."
        return ["if = {", "limit = { mdcw_cw_can_join_west = yes }", f"custom_effect_tooltip = {PFX}cw_join_west_tt",
                "set_temp_variable = { mdcw_cw_new_alignment = 1 }", "set_temp_variable = { mdcw_cw_t_free = 1 }", "mdcw_cw_change_alignment = yes",
                "set_temp_variable = { mdcw_cw_t_free = 0 }", "hidden_effect = { mdcw_cw_recalculate_country = yes mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }", "}"]
    LOC[f"{PFX}cw_join_nam_tt"] = "The republic leaves its Cold War bloc and becomes §YNon-Aligned§!."
    return ["if = {", "limit = { has_country_flag = mdcw_cw_initialized NOT = { check_variable = { mdcw_cw_alignment = 0 } } }",
            f"custom_effect_tooltip = {PFX}cw_join_nam_tt", "set_temp_variable = { mdcw_cw_new_alignment = 0 }", "set_temp_variable = { mdcw_cw_t_free = 1 }",
            "mdcw_cw_change_alignment = yes", "set_temp_variable = { mdcw_cw_t_free = 0 }",
            "hidden_effect = { mdcw_cw_recalculate_country = yes mdcw_cw_rebuild_blocs = yes mdcw_cw_refresh_all_bloc_effects = yes }", "}"]


# ---------------------------------------------------------------- leaders
# portraits that exist in the mod (gfx/leaders/DDR); the others show MD's generic portrait
PORTRAIT = {"Walter Ulbricht": "gfx/Leaders/DDR/DDR_Coldwar_WalterUlbricht.dds", "Erich Honecker": "gfx/leaders/DDR/honecker.dds",
            "Egon Krenz": "gfx/leaders/DDR/DDR_Egon_Krenz.dds", "Erich Mielke": "gfx/leaders/DDR/DDR_Erich_Mielke.dds",
            "Hans Modrow": "gfx/leaders/DDR/DDR_Hans_Modrow.dds", "Generaloberst Heinz Keßler": "gfx/leaders/DDR/DDR_Heinz_Kessler.dds",
            "Heinz Keßler": "gfx/leaders/DDR/DDR_Heinz_Kessler.dds", "Manfred Gerlach": "gfx/leaders/DDR/DDR_Manfred_Gerlach.dds"}
# English display names of the party leaders (the design keeps titles in some names)
LEADER_DISPLAY = {"Generaloberst Heinz Keßler": "Heinz Keßler", "Bishop Albrecht Schönherr": "Albrecht Schönherr",
                  "Louis Ferdinand, Prince of Prussia": "Louis Ferdinand"}


def leader_key(name):
    """leader names go through localisation (ASCII-safe script, Umlaute in the yml)"""
    key = f"{PFX}leader_{slug(name.replace('ß', 'ss').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue'))}"
    LOC[key] = name
    return key


def leader_line(idx, name, extra_traits=()):
    en = LEADER_DISPLAY.get(name, name)
    pic = PORTRAIT.get(name) or PORTRAIT.get(en)
    p = f' picture = "{pic}"' if pic else ""
    traits = [ideology_trait(idx)] + list(extra_traits)
    return f'create_country_leader = {{ name = "{leader_key(en)}"{p} ideology = {SUBIDEO[idx]} traits = {{ {" ".join(traits)} }} }}'


def new_leader_tt(name):
    en = LEADER_DISPLAY.get(name, name)
    key = f"new_leader_{slug(en)}"
    LOC[f"{PFX}{key}_tt"] = f"§Y{en}§! becomes the leader of [ROOT.GetNameDef]."
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def ruling_party(f, e):
    i, name = e["i"], e["leader"]
    if i == 4:
        LOC[f"{PFX}restore_party_rule_tt"] = ("The §YSocialist Unity Party§! takes power again under its First Secretary "
                                            "(the living holder of the office, otherwise the Central Committee's choice).")
        return [f"custom_effect_tooltip = {PFX}restore_party_rule_tt", f"{PFX}restore_party_rule = yes"]
    # the party first (MD's set_leader may replace the leader), then our leader
    return [f"set_temp_variable = {{ rul_party_temp = {i} }}", "change_ruling_party_effect = yes", new_leader_tt(name),
            "hidden_effect = {", "retire_country_leader = yes", leader_line(i, name), "}"]


# ---------------------------------------------------------------- ladders
def ladder_ids(name):
    L = LADDERS[name]
    return [PFX + s for s in L["steps"] + L["variants"]]


def ladder(e):
    name, op = e["ladder"], e["op"]
    R.ladder_ops.add((name, op))
    if op == "remove":
        return [f"{PFX}ladder_{name}_clear = yes"]
    if op == "down":
        return [f"{PFX}ladder_{name}_down = yes"]
    target = e["id"]
    # replace / up: whichever form is active goes, the target comes. The economic line always takes effect (a new doctrine);
    # the other ladders only while one of their forms is active - a border that was opened or a lignite economy that was ended stays so.
    if name == "overtaking":
        return [f"{PFX}ladder_{name}_clear = yes", f"add_ideas = {target}"]
    if target in STEP_ONLY:
        # a policy of the old regime only acts on the original form, not on what a new government made of it
        base = PFX + LADDERS[name]["steps"][0]
        return [f"if = {{ limit = {{ has_idea = {base} }}", f"swap_ideas = {{ remove_idea = {base} add_idea = {target} }}", "}"]
    return [f"if = {{ limit = {{ {PFX}ladder_{name}_active = yes }}", f"{PFX}ladder_{name}_clear = yes", f"add_ideas = {target}", "}"]


STEP_ONLY = {f"{PFX}soc_the_antenna_raids", f"{PFX}soc_the_tolerated_window"}


# ---------------------------------------------------------------- events of the tree (focus effects)
EVENT_FIRE = {}   # key -> code lines (filled by dg_events)


def compile_effect(e, f, i=None):
    k = e["k"]
    text = f["etext"][i] if i is not None else ""
    if k == "quality":
        # These rewards execute in the consent/funding callback, but their
        # permanent backing variables still need a generated dynamic reader.
        key = {'open_repayment': 'imp_sanction_resistance',
               'start_licence': 'military_factories_productivity'}.get(e['action'])
        if key:
            keys = R.dyn.setdefault('COLDWAR_DDR_planned_economy_modifier', [])
            if key not in keys:
                keys.append(key)
        return [f"COLDWAR_DDR_Q_{e['action']} = yes"]
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
        return outlook(e["o"], e["v"])
    if k == "dyn":
        return country_dyn(e["g"], e["mods"])
    if k == "prog":
        return prog_dyn(e["g"], e["mods"])
    if k == "idea":
        if e.get("ladder"):
            return ladder(e)
        iid, days = e["id"], e.get("days")
        if e.get("existing"):
            return [f"add_timed_idea = {{ idea = {iid} days = {days} }}"] if days else [f"if = {{ limit = {{ NOT = {{ has_idea = {iid} }} }} add_ideas = {iid} }}"]
        out = []
        if e.get("remove"):
            for r in (e["remove"] if isinstance(e["remove"], list) else [e["remove"]]):
                out.append(f"if = {{ limit = {{ has_idea = {r} }} remove_ideas = {r} }}")
        if e.get("swap"):
            old = e["swap"]
            add = f"add_timed_idea = {{ idea = {iid} days = {days} }}" if days else f"add_ideas = {iid}"
            return out + [f"if = {{ limit = {{ has_idea = {old} }} swap_ideas = {{ remove_idea = {old} add_idea = {iid} }} }}", f"else = {{ {add} }}"]
        if days:
            return out + [f"add_timed_idea = {{ idea = {iid} days = {days} }}"]
        return out + [f"add_ideas = {iid}"]
    if k == "rmidea":
        if e.get("ladder"):
            return ladder(e)
        return [f"if = {{ limit = {{ has_idea = {e['id']} }} remove_ideas = {e['id']} }}"]
    if k == "trust":
        return trust(e["v"])
    if k == "course":
        return course(e["v"])
    if k == "tension":
        return tension(e["v"])
    if k == "tech":
        R.tech_names.add(f["id"])
        cats = " ".join(f"category = {c}" for c in e["cats"])
        return [f"add_tech_bonus = {{ name = {f['id']} bonus = {fmt(e['b'])} uses = {e['n']} {cats} }}"]
    if k == "resource":
        # A named local plant must not develop another country's occupied state.
        return ["if = {", f"limit = {{ {e['state']} = {{ is_owned_and_controlled_by = ROOT }} }}",
                f"{e['state']} = {{ add_resource = {{ type = {e['type']} amount = {e['n']} }} }}", "}"]
    if k == "build":
        out = ["set_temp_variable = { skip_payment = 1 }", f"{e['helper']} = yes", "set_temp_variable = { skip_payment = 0 }"]
        if e.get("cost"):
            out += pay(e["cost"])
        return out
    if k == "offer":
        R.offers.add(e["key"])
        import dg_offers as OF
        return OF.offer_lines(e["key"])
    if k == "op":
        key = e["key"]
        base = R.opinions.get(key, e["v"])
        assert (base > 0) == (e["v"] > 0), (f["id"], key)
        R.opinions.setdefault(key, e["v"])
        return opinion(e["tag"], key)
    if k == "infl":
        return influence(e["tags"], e["v"])
    if k == "rp":
        return ruling_party(f, e)
    if k == "gdp":
        return pay(e["v"])
    if k == "gdp_gain":
        return receive(e["v"])
    if k == "debt":
        return credit(e["v"])
    if k == "corr":
        return [f"{e['helper']} = yes"] * abs(e["v"])
    if k == "heir":
        R.heirs.add(e["key"])
        return [f"{PFX}set_heir_{e['key']} = yes"]
    if k == "decision":
        R.decisions.add(e["key"])
        t = re.sub(r"^Unlocks decisions: ", "Unlocks the decisions ", text) if text else "Unlocks new decisions."
        t = t.replace("<Name>", "...")
        LOC[f"{e['key']}_unlock_tt"] = t
        return [f"set_country_flag = {e['key']}_unlocked", f"custom_effect_tooltip = {e['key']}_unlock_tt"]
    if k == "event":
        R.events.add(e["key"])
        from dg_events import fire
        return fire(e["key"], f)
    if k == "xp":
        return [f"{e['kind']}_experience = {e['v']}"]
    if k == "cp":
        return [f"add_command_power = {e['v']}"]
    if k == "mastery":
        return [f"add_mastery = {{ amount = {e['v']} folder = {e['folder']} }}"]
    if k == "manpower":
        return [f"add_manpower = {e['v']}"]
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
    if k == "flag":
        R.flags_set.add(e["f"])
        out = [f"set_country_flag = {e['f']}"]
        if text and not text.startswith("Candidacy prepared"):
            out.append(tt(f"flag_{short(e['f'])}", re.sub(r" ?\(`[^`]+`\)", "", text)))
        elif text:
            out.append(tt("candidacy_prepared", "The candidacy is prepared: the decision §YConvene the Central Committee§! can put him to the vote."))
        return out
    if k in ("note", "custom"):
        from dg_manual import manual
        return manual(f, e, text)
    raise KeyError(k)
