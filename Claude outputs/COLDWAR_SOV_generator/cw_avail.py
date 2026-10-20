# COLDWAR | Converts the `available` conditions of the design (German text with `code` marks) into triggers.
import re
from cw_common import *
from cw_layout import BYID, FOCI, PARTY, TRIG

NAME2ID = {}
for f in FOCI:
    NAME2ID.setdefault(f["name"], f["id"])
PARTY_BY_NAME = {v[0]: k for k, v in PARTY.items()}
FACTION_VAR = {"Nomenklatura": "communist_cadres", "Gewerkschaften": "labour_unions", "KGB": "intelligence_community",
               "Armee": "the_military", "Rüstungskomplex": "defense_industry", "Branchenministerien": "industrial_conglomerates"}
GOVS = {"communism", "democratic", "neutrality", "nationalist", "fascism"}
CMP = {"≥": ">", ">": ">", "<": "<", "≤": "<"}


def num(s):
    return float(s.replace("−", "-").replace(",", ".").replace("+", ""))


def cmp_val(op, v, scale=1.0, step=0.001):
    """HOI4 check_variable / > < are strict; >= v is written as > v - step"""
    v = v * scale
    if op == "≥":
        return ">", v - step
    if op == "≤":
        return "<", v + step
    return CMP[op], v


def bop(op, v):
    o, x = cmp_val(op, v, step=0.001)
    return f"check_variable = {{ {PFX}bop {o} {fmt(round(x, 3))} }}"


def atom(a):
    a = a.strip().rstrip(".")
    a = re.sub(r"\s*\((?:Reformer|Orthodoxe|Tod Kossygins|danach nicht mehr im Politbüro)\)", "", a)
    m = re.match(r"^`(\w+_are_in_power)`$", a)
    if m:
        return f"{m.group(1)} = yes"
    m = re.match(r"^`has_government = (\w+)`$", a)
    if m:
        return f"has_government = {m.group(1)}"
    m = re.match(r"^`(COLDWAR_SOV_\w+)` erledigt$", a)
    if m:
        return f"has_completed_focus = {m.group(1)}"
    m = re.match(r"^„(.+?)“ erledigt$", a)
    if m:
        names = m.group(1).split("“/„")
        ids = [NAME2ID[n] for n in names]
        return " ".join(f"has_completed_focus = {i}" for i in ids) if len(ids) == 1 else "OR = { " + " ".join(f"has_completed_focus = {i}" for i in ids) + " }"
    m = re.match(r"^`(COLDWAR_SOV_\w+)` gesetzt$", a)
    if m:
        return f"has_country_flag = {m.group(1)}"
    m = re.match(r"^Datum ≥ (\d\d\.\d\d\.\d{4}) und < (\d\d\.\d\d\.\d{4})$", a)
    if m:
        return f"date > {date_minus_one(m.group(1))} date < {date_hoi(m.group(2))}"
    m = re.match(r"^Datum ≥ (\d\d\.\d\d\.\d{4})$", a)
    if m:
        return f"date > {date_minus_one(m.group(1))}"
    m = re.match(r"^Datum < (\d\d\.\d\d\.\d{4})$", a)
    if m:
        return f"date < {date_hoi(m.group(1))}"
    m = re.match(r"^(.+?) ist Generalsekretär \(`(COLDWAR_SOV_gensec_\w+)`\)$", a)
    if m:
        return f"has_country_flag = {m.group(2)}"
    m = re.match(r"^(.+?) ist nicht Generalsekretär$", a)
    if m:
        return None  # handled by the caller (needs the key)
    m = re.match(r"^Politbüro-Balance ([≤≥<>]) ([−+-]?[\d,]+)$", a)
    if m:
        return bop(m.group(1), num(m.group(2)))
    m = re.match(r"^Politbüro-Balance zwischen ([−+-]?[\d,]+) und ([−+-]?[\d,]+)$", a)
    if m:
        return bop("≥", num(m.group(1))) + " " + bop("≤", num(m.group(2)))
    m = re.match(r"^Stabilität ([≤≥<>]) (\d+) %$", a)
    if m:
        o, x = cmp_val(m.group(1), int(m.group(2)) / 100)
        return f"has_stability {o} {fmt(round(x, 3))}"
    m = re.match(r"^(Nomenklatura|Gewerkschaften|KGB|Armee|Rüstungskomplex|Branchenministerien)(?:-Meinung)? ([≤≥<>]) (\d+)$", a)
    if m:
        o, x = cmp_val(m.group(2), int(m.group(3)), step=1)
        return f"check_variable = {{ {FACTION_VAR[m.group(1)]}_opinion {o} {fmt(x)} }}"
    m = re.match(r"^Zusammenhalt der Union ([≤≥<>]) (\d+)$", a)
    if m:
        o, x = cmp_val(m.group(1), int(m.group(2)), step=1)
        return f"check_variable = {{ {PFX}union_cohesion {o} {fmt(x)} }}"
    m = re.match(r"^Cold-War-Spannung ([≤≥<>]) (\d+)$", a)
    if m:
        o, x = cmp_val(m.group(1), int(m.group(2)), step=1)
        return f"check_variable = {{ global.mdcw_cw_tension {o} {fmt(x)} }}"
    m = re.match(r"^Ölpreis-Level \(Cold War\) ([≤≥<>]) (\d+)$", a)
    if m:
        o, x = cmp_val(m.group(1), int(m.group(2)), step=1)
        return f"check_variable = {{ global.mdcw_cw_oil_level {o} {fmt(x)} }}"
    m = re.match(r"^Korruptionsstufe ≥ (\d+)$", a)
    if m:
        return "OR = { " + " ".join(f"has_idea = corruption_level_{i:02d}" for i in range(int(m.group(1)), 11)) + " }"
    m = re.match(r"^Popularität (.+?) ≥ (\d+) %$", a)
    if m:
        i = PARTY_BY_NAME[m.group(1)]
        return f"check_variable = {{ party_pop_array^{i} > {fmt(int(m.group(2)) / 100 - 0.001)} }}"
    if a == "Partei regiert noch nicht":
        return None  # handled by the caller
    if a == "nicht im Bürgerkrieg":
        return "has_civil_war = no"
    if a == "nur Spieler":
        return "is_ai = no"
    if a == "im Krieg" or a == "Im Krieg":
        return "has_war = yes"
    m = re.match(r"^Im Krieg mit (\w{3})$", a)
    if m:
        return f"has_war_with = {m.group(1)}"
    m = re.match(r"^(\w{3}) existiert$", a)
    if m:
        return f"country_exists = {m.group(1)}"
    m = re.match(r"^hat „(.+?)“$", a)
    if m:
        from cw_layout import IDEAS
        iid = [k for k, v in IDEAS.items() if v["name"] == m.group(1)][0]
        return f"has_idea = {iid}"
    if a == "`emerging_communist_state_are_in_power`":
        return "emerging_communist_state_are_in_power = yes"
    raise KeyError(a)


def convert(f):
    av = f["av"].strip()
    if not av:
        return ""
    sid = f["id"]
    m = re.match(r"^Keine andere Richtung erledigt – ODER `has_government = (\w+)` und noch keine Richtung unter dieser Regierung$", av)
    if m:
        gov = m.group(1)
        others = [d for d in ("dir_the_leading_role", "dir_convergence", "dir_third_way", "dir_the_russian_idea") if PFX + d != sid]
        return ("OR = {\nNOT = { " + " ".join(f"has_completed_focus = {PFX}{d}" for d in others) + " }\n"
                f"AND = {{ has_government = {gov} NOT = {{ has_country_flag = {PFX}direction_under_{gov} }} }}\n}}")
    out = []
    party_line = None
    for part in [p for p in av.split("; ") if p.strip()]:
        if re.search(r" (?:ODER|oder) ", part):
            alts = [atom(x) for x in re.split(r" (?:ODER|oder) ", part)]
            out.append("OR = { " + " ".join(alts) + " }")
            continue
        m = re.match(r"^(.+?) ist nicht Generalsekretär$", part)
        if m:
            key = short(sid).replace("ple_", "")
            out.append(f"NOT = {{ has_country_flag = {PFX}gensec_{key} }}")
            continue
        if part == "Partei regiert noch nicht":
            rp = [e for e in f["eff"] if e["k"] == "rp"]
            out.append(f"NOT = {{ {TRIG[rp[0]['i']]}_are_in_power = yes }}")
            continue
        r = atom(part)
        if r:
            out.append(r)
    return "\n".join(out)
