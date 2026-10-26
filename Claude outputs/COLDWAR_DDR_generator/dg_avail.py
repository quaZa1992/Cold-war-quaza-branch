# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Converts the `available` conditions of the design (English text, code in backticks) into triggers.
# House rule (Enes, 17.10.2026, SOV): no focus is locked to a calendar date. Date clauses are dropped, also inside an OR;
# historical events and AI weights still use dates.
import re
from dg_common import *
from dg_load import BYID, FOCI, PARTY, TRIG, NAME2ID, LEADER_NAME, LADDERS, FACTION_BY_NAME

KEY_OF_LEADER = {v: k for k, v in LEADER_NAME.items()}
FACTION_ALIAS = {"MfS": "intelligence_community", "Stasi": "intelligence_community", "NVA": "the_military",
                 "SED cadres": "communist_cadres", "FDGB": "labour_unions", "the Church": "the_clergy"}
PARTY_BY_NAME = {v["name"]: k for k, v in PARTY.items()}
DROPPED = []          # (focus, clause) - reported by the build
UNKNOWN = []


def num(s):
    return float(s.replace("−", "-").replace(",", "").replace("+", ""))


def ge(var, v, step):
    """var >= v (HOI4 compares strictly)"""
    return f"check_variable = {{ {var} > {fmt(round(v - step, 4))} }}"


def le(var, v, step):
    return f"check_variable = {{ {var} < {fmt(round(v + step, 4))} }}"


TRUST = f"{PFX}moscow_trust"
COURSE = f"{PFX}course"           # shadow variable of the balance of power (the BOP value cannot be read)


def ladder_ideas(name):
    L = LADDERS[name]
    return [PFX + s for s in L["steps"] + L["variants"]]


def any_idea(ids):
    return "OR = { " + " ".join(f"has_idea = {i}" for i in ids) + " }" if len(ids) > 1 else f"has_idea = {ids[0]}"


def focus_done(names):
    ids = [NAME2ID[n] for n in names]
    return " ".join(f"has_completed_focus = {i}" for i in ids) if len(ids) == 1 else "OR = { " + " ".join(f"has_completed_focus = {i}" for i in ids) + " }"


def atom(a, f):
    a = a.strip().rstrip(".").strip()
    if not a:
        return ""
    # ---- code in backticks only
    m = re.match(r"^`([^`]+)`$", a)
    if m:
        c = m.group(1).strip()
        if re.match(r"^\w+_are_in_power$", c) or c in ("mdcw_cw_can_join_west",):
            return f"{c} = yes"
        if re.match(r"^COLDWAR_DDR_\w+$", c):
            return f"has_country_flag = {c}"
        return c
    m = re.match(r"^`([^`]+)` \((.+)\)$", a)       # `code` (explanation)
    if m:
        return atom(f"`{m.group(1)}`", f)
    # ---- dates: dropped
    if re.match(r"^(?:[Dd]ate) (?:from|between|before)\b", a):
        DROPPED.append((f["id"], a))
        return ""
    # ---- First Secretaries
    m = re.match(r"^(.+?) is First Secretary(?: \(`(COLDWAR_DDR_first_sec_\w+)`\))?$", a)
    if m and m.group(1) in KEY_OF_LEADER:
        return f"has_country_flag = {PFX}first_sec_{KEY_OF_LEADER[m.group(1)]}"
    m = re.match(r"^(.+?) is not First Secretary$", a)
    if m and m.group(1) in KEY_OF_LEADER:
        return f"NOT = {{ has_country_flag = {PFX}first_sec_{KEY_OF_LEADER[m.group(1)]} }}"
    m = re.match(r"^(.+?) is alive(?: \(.*?\))?( and not First Secretary)?$", a)
    if m and m.group(1) in KEY_OF_LEADER:
        k = KEY_OF_LEADER[m.group(1)]
        out = f"{PFX}alive_{k} = yes"
        if m.group(2):
            out += f" NOT = {{ has_country_flag = {PFX}first_sec_{k} }}"
        return out
    # ---- meters
    m = re.match(r"^Moscow's Trust (at least|below|at most) (\d+)$", a)
    if m:
        v = int(m.group(2))
        return {"at least": ge(TRUST, v, 1), "below": f"check_variable = {{ {TRUST} < {v} }}", "at most": le(TRUST, v, 1)}[m.group(1)]
    m = re.match(r"^Moscow's Trust between (\d+) and (\d+)$", a)
    if m:
        return ge(TRUST, int(m.group(1)), 1) + " " + le(TRUST, int(m.group(2)), 1)
    m = re.match(r"^Inner-German course (at least|at most|below) ([−+-]?[\d.]+)(?: \(.*\))?$", a)
    if m:
        v = num(m.group(2))
        return {"at least": ge(COURSE, v, 0.001), "at most": le(COURSE, v, 0.001), "below": f"check_variable = {{ {COURSE} < {fmt(v)} }}"}[m.group(1)]
    m = re.match(r"^Inner-German course between ([−+-]?[\d.]+) and ([−+-]?[\d.]+)$", a)
    if m:
        return ge(COURSE, num(m.group(1)), 0.001) + " " + le(COURSE, num(m.group(2)), 0.001)
    m = re.match(r"^[Ss]tability (at least|below) (\d+) %$", a)
    if m:
        v = int(m.group(2)) / 100
        return f"has_stability > {fmt(round(v - 0.001, 3))}" if m.group(1) == "at least" else f"has_stability < {fmt(v)}"
    m = re.match(r"^Cold War tension at least (\d+)$", a)
    if m:
        return ge("global.mdcw_cw_tension", int(m.group(1)), 1)
    m = re.match(r"^Corruption level at least (\d+)$", a)
    if m:
        return any_idea([f"corruption_level_{i:02d}" for i in range(int(m.group(1)), 11)])
    # ---- factions and parties
    m = re.match(r"^(.+?) opinion at least (\d+)$", a)
    if m and (m.group(1) in FACTION_BY_NAME or m.group(1) in FACTION_ALIAS):
        fv = FACTION_BY_NAME.get(m.group(1)) or FACTION_ALIAS[m.group(1)]
        return f"has_idea = {fv} " + ge(f"{fv}_opinion", int(m.group(2)), 1)
    m = re.match(r"^(.+?) popularity at least (\d+) %$", a)
    if m and m.group(1) in PARTY_BY_NAME:
        i = PARTY_BY_NAME[m.group(1)]
        return f"check_variable = {{ party_pop_array^{i} > {fmt(int(m.group(2)) / 100 - 0.001)} }}"
    if a == "the party does not govern yet":
        rp = [e for e in f["eff"] if e["k"] == "rp"]
        return f"NOT = {{ {TRIG[rp[0]['i']]}_are_in_power = yes }}"
    if a == "the SED does not govern":
        return "NOT = { emerging_communist_state_are_in_power = yes }"
    # ---- foci and ideas
    m = re.match(r'^"([^"]+)" or "([^"]+)" completed$', a)
    if m:
        return focus_done([m.group(1), m.group(2)])
    m = re.match(r'^"([^"]+)" completed(?: \(`has_completed_focus`.*\))?$', a)
    if m:
        return focus_done([m.group(1)])
    m = re.match(r'^The .+? focus "(.+?)" completed$', a)
    if m:
        return focus_done([m.group(1)])
    m = re.match(r'^the .+? focus "(.+?)" has not been completed \(`(.+)`\)$', a)
    if m:
        return m.group(2)
    m = re.match(r"^`(COLDWAR_DDR_\w+)` not completed", a)
    if m:
        return f"NOT = {{ has_completed_focus = {m.group(1)} }}"
    if a.startswith("a border regime spirit is active"):
        return any_idea(ladder_ideas("border"))
    m = re.match(r'^"King Lignite" or "Coal Instead of Oil" active$', a)
    if m:
        return any_idea(ladder_ideas("lignite"))
    m = re.match(r"^No other direction chosen \(`COLDWAR_DDR_direction_\*` flag\)$", a)
    if m:
        me = [e["f"] for e in f["eff"] if e["k"] == "flag" and "direction_" in e["f"]][0]
        others = [f"{PFX}direction_{d}" for d in ("em", "we", "na", "nt") if f"{PFX}direction_{d}" != me]
        return "NOT = { " + " ".join(f"has_country_flag = {o}" for o in others) + " }"
    m = re.match(r"^Planned economy: trade law is not .+ \(`(.+)`\)$", a)
    if m:
        return m.group(1)
    if a == "trade law is not Closed Economy":
        return "NOT = { has_idea = md_closed_economy }"
    m = re.match(r"^In the Warsaw Pact \(`(.+)`\)$", a)
    if m:
        return m.group(1)
    # ---- flags with explanations
    m = re.match(r"^(?:Bonn accepted .+?|a Western capital accepted recognition|the event .+? has fired|Hoffmann's succession named Keßler) \(`(?:has_country_flag = )?(COLDWAR_DDR_\w+)`(?: flag)?\)$", a)
    if m:
        return f"has_country_flag = {m.group(1)}"
    m = re.match(r"^Hoffmann's succession named Keßler \(`(COLDWAR_DDR_\w+)`\) and the Central Committee failed to elect a successor$", a)
    if m:
        return f"AND = {{ has_country_flag = {m.group(1)} has_country_flag = {PFX}kessler_refused }}"
    m = re.match(r"^`(COLDWAR_DDR_\w+)` flag(?: \(.*\))?$", a)
    if m:
        return f"has_country_flag = {m.group(1)}"
    m = re.match(r"^the LDPD has not returned the firms \(`(COLDWAR_DDR_\w+)` not set\)$", a)
    if m:
        return f"NOT = {{ has_country_flag = {m.group(1)} }}"
    # ---- world
    if a == "not in a civil war":
        return "has_civil_war = no"
    if a == "not at war with a major power":
        return "NOT = { any_enemy_country = { is_major = yes } }"
    if a in ("at war", "At war"):
        return "has_war = yes"
    if a == "player only":
        return "is_ai = no"
    if a == "the Soviet Union is led by Gorbachev":
        return "country_exists = SOV SOV = { has_country_flag = COLDWAR_SOV_gensec_gor }"
    m = re.match(r"^(Ethiopia|Mozambique|Nicaragua|Angola) exists( and is governed by an Emerging party)?(?: \(.*\))?$", a)
    if m:
        tag = {"Ethiopia": "ETH", "Mozambique": "MOZ", "Nicaragua": "NIC", "Angola": "AGL"}[m.group(1)]
        return f"country_exists = {tag}" + (f" {tag} = {{ has_government = communism }}" if m.group(2) else "")
    m = re.match(r"^Commercial Coordination focus completed OR KoKo hard-currency decisions taken (\d+) times$", a)
    if m:
        return ("OR = { has_completed_focus = COLDWAR_DDR_plan_commercial_coordination "
                + ge(f"{PFX}hard_currency_deals", int(m.group(1)), 1) + " }")
    raise KeyError(a)


SPECIAL = {
    # parenthesised extra condition: the cadre threshold is 80 if Ulbricht kept the cadre department (Verner)
    "Moscow's Trust at least 40 OR SED Nomenklatura opinion at least 70 (80 if Ulbricht kept the cadre department, `COLDWAR_DDR_ulb_team_verner`)":
        f"OR = {{ {ge(TRUST, 40, 1)} AND = {{ NOT = {{ has_country_flag = COLDWAR_DDR_ulb_team_verner }} has_idea = communist_cadres "
        f"{ge('communist_cadres_opinion', 70, 1)} }} AND = {{ has_country_flag = COLDWAR_DDR_ulb_team_verner has_idea = communist_cadres "
        f"{ge('communist_cadres_opinion', 80, 1)} }} }}",
    "Moscow's Trust at least 65 OR (Moscow's Trust at most 30 AND the Soviet Union endorses a change)":
        f"OR = {{ {ge(TRUST, 65, 1)} AND = {{ {le(TRUST, 30, 1)} has_country_flag = {PFX}soviet_endorses_change }} }}",
}


def split_top(s, sep=" OR "):
    """split at `sep` outside parentheses and backticks"""
    parts, depth, tick, cur, i = [], 0, False, "", 0
    while i < len(s):
        c = s[i]
        if c == "`":
            tick = not tick
        elif not tick and c == "(":
            depth += 1
        elif not tick and c == ")":
            depth -= 1
        if depth == 0 and not tick and s.startswith(sep, i):
            parts.append(cur)
            cur, i = "", i + len(sep)
            continue
        cur += c
        i += 1
    parts.append(cur)
    return [p.strip() for p in parts]


def wrap(a):
    """an alternative of an OR that holds several statements needs an AND"""
    if a.startswith(("OR = {", "NOT = {", "AND = {")) and a.count("{") == 1 or re.match(r"^\w+ = \{.*\}$", a) and a.count("{") == 1:
        return a
    return f"AND = {{ {a} }}" if len(re.findall(r"(?:^|\s)[\w.^@:]+ [=<>] ", a)) > 1 else a


def convert(f):
    av = (f.get("available") or "").strip()
    if not av:
        return ""
    out = []
    for part in [p.strip() for p in av.split("; ") if p.strip()]:
        if part in SPECIAL:
            out.append(SPECIAL[part])
            continue
        alts_raw = split_top(part)
        if len(alts_raw) > 1 and re.match(r"^Commercial Coordination focus completed OR ", part):
            alts_raw = [part]          # one clause of its own (atom knows it)
        if len(alts_raw) > 1:
            try:
                alts = [x for x in (atom(x, f) for x in alts_raw) if x]
            except KeyError as e:
                UNKNOWN.append((f["id"], str(e)))
                continue
            if len(alts) > 1:
                out.append("OR = { " + " ".join(wrap(a) for a in alts) + " }")
            elif alts:
                out.append(alts[0])
            continue
        try:
            r = atom(part, f)
        except KeyError:
            UNKNOWN.append((f["id"], part))
            continue
        if r:
            out.append(r)
    return "\n".join(o for o in out if o)
