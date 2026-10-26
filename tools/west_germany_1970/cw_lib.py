# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Small helpers to emit Clausewitz script for the West Germany 1970 content.

Everything is authored as compact script snippets; `fmt` re-indents by braces.
Localisation keys are registered through `L` and written by compile.py.
"""
import re

P = "COLDWAR_GER_1970"          # id prefix for focuses, ideas, decisions, effects
EVG = "COLDWAR_GER"              # event namespace, West Germany
EVD = "COLDWAR_GER_DDR"              # event namespace, East Germany
GATE = "original_tag = GER IMP_is_1970_scenario = yes"

LOC = {}            # key -> text
USED_GFX = set()    # sprite names referenced (checked by validate.py)
USED_EFFECTS = set()
USED_EVENTS = set()


def L(key, text):
    if key in LOC and LOC[key] != text:
        raise ValueError("conflicting localisation for " + key)
    LOC[key] = text
    return key


# --------------------------------------------------------------------- format
def fmt(text, base=0):
    """Re-indent a script snippet by brace depth, one statement block per line."""
    out, depth = [], base
    for raw in text.strip("\n").split("\n"):
        line = raw.strip()
        if not line:
            out.append("")
            continue
        opens, closes = line.count("{"), line.count("}")
        lead = len(line) - len(line.lstrip("}"))
        d = max(0, depth - lead)
        out.append("\t" * d + line)
        depth += opens - closes
    return "\n".join(out)


# --------------------------------------------------------------- effect atoms
def pp(n):
    return f"add_political_power = {n}"


def stab(x):
    return f"add_stability = {x}"


def ws(x):
    return f"add_war_support = {x}"


def money(bn):
    """Treasury change in billions of dollars (negative = cost)."""
    return f"set_temp_variable = {{ treasury_change = {bn} }}\nmodify_treasury_effect = yes"


def money_gdp(frac):
    """Treasury change as a share of GDP (negative = cost); stays in scale over 30 years."""
    return (f"set_temp_variable = {{ treasury_change = gdp_total }}\n"
            f"multiply_temp_variable = {{ treasury_change = {frac} }}\nmodify_treasury_effect = yes")


def debt_gdp(frac):
    return (f"set_temp_variable = {{ debt_change = gdp_total }}\n"
            f"multiply_temp_variable = {{ debt_change = {frac} }}\nmodify_debt_effect = yes")


# GER system variables and their display names / bounds
VARS = {
    "cwger_ostpolitik": ("Inner-German rapprochement", 0, 100),
    "cwger_berlin_access": ("Berlin access", 0, 100),
    "cwger_security": ("Security state", 0, 100),
    "cwger_rechtsstaat": ("Rule-of-law credibility", 0, 100),
    "cwger_terror_left": ("Left-wing terror threat", 0, 100),
    "cwger_terror_right": ("Right-wing terror threat", 0, 100),
    "cwger_terror_foreign": ("Foreign terror threat", 0, 100),
    "cwger_raf_cadre": ("RAF active cadre", 0, 120),
    "cwger_raf_milieu": ("RAF sympathiser milieu", 0, 100),
    "cwger_raf_prisoners": ("Imprisoned RAF leaders", 0, 40),
    "cwger_counterintel": ("Counter-intelligence", 0, 100),
    "cwger_stasi_penetration": ("Stasi penetration", 0, 100),
    "cwger_fdp_course": ("FDP course (social-liberal ↔ market-liberal)", -100, 100),
    "cwger_csu_autonomy": ("CSU autonomy", 0, 100),
    "cwger_bundesrat_union": ("Union share of the Bundesrat", 0, 100),
    "cwger_peace_movement": ("Peace movement", 0, 100),
    "cwger_anti_nuclear": ("Anti-nuclear movement", 0, 100),
    "cwger_westbindung": ("Western integration", 0, 100),
    "cwger_scandal": ("Scandal pressure", 0, 100),
    "cwger_bundesbank": ("Bundesbank friction", 0, 100),
    "cwger_unity": ("Unity momentum", 0, 100),
    "cwger_east_burden": ("Burden of the East", 0, 100),
    "cwger_dark": ("Erosion of the Republic", 0, 100),
    "cwger_resistance": ("Resistance against the Directorate", 0, 100),
}
DDR_VARS = {
    "cwddr_hard_currency": ("GDR hard-currency shortage", 0, 100),
    "cwddr_west_dependency": ("GDR dependence on West German money", 0, 100),
    "cwddr_exit_pressure": ("GDR exit pressure", 0, 100),
    "cwddr_west_media": ("Western media reach in the GDR", 0, 100),
    "cwddr_opposition": ("GDR civic opposition", 0, 100),
    "cwddr_sed_control": ("SED control", 0, 100),
    "cwddr_moscow_backing": ("Moscow's guarantee for the GDR", 0, 100),
    "cwddr_recognition": ("GDR international recognition", 0, 100),
}


def _tt(var, amount, labels):
    sign = "up" if amount > 0 else "down"
    num = str(abs(amount)).replace(".", "_")
    key = f"{P}_tt_{var}_{sign}_{num}"
    name = labels[var][0]
    col = "G" if amount > 0 else "R"
    # colour is neutral for meters where "up" is not obviously good
    L(key, f"{name}: §Y{'+' if amount > 0 else '-'}{abs(amount)}§!")
    return key


def v(var, amount, show=True):
    """Change a GER system variable with clamping and an explicit tooltip."""
    lo, hi = VARS[var][1], VARS[var][2]
    s = f"add_to_variable = {{ {var} = {amount} }}\nclamp_variable = {{ var = {var} min = {lo} max = {hi} }}"
    if var == "cwger_ostpolitik":
        s += f"\nadd_power_balance_value = {{ id = {P}_deutschlandpolitik value = {round(amount / 50.0, 3)} }}"
    if show:
        return f"custom_effect_tooltip = {_tt(var, amount, VARS)}\nhidden_effect = {{\n{s}\n}}"
    return s


def dv(var, amount, show=True):
    """Change a DDR system variable from any scope."""
    lo, hi = DDR_VARS[var][1], DDR_VARS[var][2]
    s = (f"if = {{ limit = {{ country_exists = DDR }} DDR = {{ add_to_variable = {{ {var} = {amount} }} "
         f"clamp_variable = {{ var = {var} min = {lo} max = {hi} }} }} }}")
    if show:
        return f"custom_effect_tooltip = {_tt(var, amount, DDR_VARS)}\nhidden_effect = {{\n{s}\n}}"
    return s


def dv_self(var, amount, show=True):
    """Change a DDR system variable while already in DDR scope."""
    lo, hi = DDR_VARS[var][1], DDR_VARS[var][2]
    s = f"add_to_variable = {{ {var} = {amount} }}\nclamp_variable = {{ var = {var} min = {lo} max = {hi} }}"
    if show:
        return f"custom_effect_tooltip = {_tt(var, amount, DDR_VARS)}\nhidden_effect = {{\n{s}\n}}"
    return s


PARTY = {"cdu": 1, "spd": 3, "dkp": 4, "pds": 5, "fdp": 2, "greens": 17, "rep": 20, "npd": 21, "dvu": 22}


def party(name, pct):
    """Shift a party's share by pct (0.02 = 2 points), moving its outlook with it."""
    from roster import AVAILABLE
    if not AVAILABLE[name]:
        return ''  # No reward for a different organisation occupying that ideology slot.
    i = PARTY[name]
    return ("hidden_effect = {\n"
            f"set_temp_variable = {{ party_index = {i} }}\n"
            f"set_temp_variable = {{ party_popularity_increase = {pct} }}\n"
            f"set_temp_variable = {{ temp_outlook_increase = {pct} }}\n"
            "change_relative_party_popularity = yes\n}\n"
            f"custom_effect_tooltip = {party_tt(name, pct)}")


PARTY_NAMES = {"cdu": "CDU", "spd": "SPD", "dkp": "DKP", "pds": "PDS", "fdp": "FDP",
               "greens": "Greens", "rep": "Republikaner", "npd": "NPD", "dvu": "DVU"}


def party_tt(name, pct):
    sign = "up" if pct > 0 else "down"
    pts = round(abs(pct) * 100, 1)
    key = f"{P}_tt_party_{name}_{sign}_{str(pts).replace('.', '_')}"
    L(key, f"{PARTY_NAMES[name]} popularity: §{'G' if pct > 0 else 'R'}{'+' if pct > 0 else '-'}{pts}%§!")
    return key


FACTIONS = {"dgb": "labour_unions", "bdi": "industrial_conglomerates", "mittelstand": "small_medium_business_owners"}


def faction(name, n):
    f = FACTIONS[name]
    return f"set_temp_variable = {{ temp_opinion_change = {n} }}\nchange_{f}_opinion = yes"


def tension(d):
    """Imperia Cold War world tension (global 0-100)."""
    sign = "up" if d > 0 else "down"
    key = f"{P}_tt_tension_{sign}_{str(abs(d)).replace('.', '_')}"
    L(key, f"Cold War world tension: §{'R' if d > 0 else 'G'}{'+' if d > 0 else '-'}{abs(d)}§!")
    return (f"custom_effect_tooltip = {key}\nhidden_effect = {{ if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} "
            f"set_temp_variable = {{ mdcw_cw_tension_delta = {d} }} mdcw_cw_add_tension = yes }} }}")


def flag(f, days=None):
    if days:
        return f"set_country_flag = {{ flag = {f} days = {days} value = 1 }}"
    return f"set_country_flag = {f}"


def gflag(f):
    return f"set_global_flag = {f}"


def tech(cat, bonus=0.5, uses=1, name=None):
    name = name or f"{P}_bonus"
    return f"add_tech_bonus = {{ name = {name} bonus = {bonus} uses = {uses} category = {cat} }}"


def build(btype, level=1, n=1):
    one = (f"random_owned_controlled_state = {{ limit = {{ free_building_slots = {{ building = {btype} size > {level - 1} include_locked = yes }} }} "
           f"add_building_construction = {{ type = {btype} level = {level} instant_build = yes }} }}")
    return "\n".join([one] * n)


def infra(n=1):
    return "\n".join(["random_owned_controlled_state = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }"] * n)


def event(evid, days=None, hours=None):
    USED_EVENTS.add(evid)
    extra = ""
    if days is not None:
        extra += f" days = {days}"
    if hours is not None:
        extra += f" random_hours = {hours}"
    return f"country_event = {{ id = {evid}{extra} }}"


def call(name):
    USED_EFFECTS.add(name)
    return f"{name} = yes"


def tt(key, text):
    L(key, text)
    return f"custom_effect_tooltip = {key}"


def idea_add(i):
    return f"add_ideas = {i}"


def idea_swap(old, new):
    return f"if = {{ limit = {{ has_idea = {old} }} swap_ideas = {{ remove_idea = {old} add_idea = {new} }} }} else = {{ add_ideas = {new} }}"


def timed_idea(i, days):
    return f"add_timed_idea = {{ idea = {i} days = {days} }}"


def J(*parts):
    return "\n".join(p for p in parts if p)


def check_braces(text, where):
    depth = 0
    for i, ch in enumerate(re.sub(r'"[^"\n]*"', '""', re.sub(r"#[^\n]*", "", text))):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                raise ValueError(f"unbalanced '}}' in {where} at {i}")
    if depth != 0:
        raise ValueError(f"unbalanced braces in {where}: depth {depth}")


# ------------------------------------------------- hooks into existing mod systems
def europe(n):
    """MD/Imperia EU system: change this country's europeanism."""
    key = f"{P}_tt_europe_{'up' if n > 0 else 'down'}_{abs(n)}"
    L(key, f"Europeanism: §{'G' if n > 0 else 'R'}{'+' if n > 0 else '-'}{abs(n)}§!")
    return (f"custom_effect_tooltip = {key}\nhidden_effect = {{ set_temp_variable = {{ modify_europeanism = {n} }} "
            f"set_temp_variable = {{ modify_europeanism_target = ROOT.id }} europeanism_change = yes }}")


def protest(n):
    """MD protest system: raise or lower the national protest strength."""
    key = f"{P}_tt_protest_{'up' if n > 0 else 'down'}_{abs(n)}"
    L(key, f"Protest strength: §{'R' if n > 0 else 'G'}{'+' if n > 0 else '-'}{abs(n)}§!")
    return (f"custom_effect_tooltip = {key}\nhidden_effect = {{ if = {{ limit = {{ NOT = {{ has_variable = protest_strength }} }} set_variable = {{ protest_strength = 0 }} }} "
            f"add_to_variable = {{ protest_strength = {n} }} clamp_variable = {{ var = protest_strength min = 0 max = 100 }} }}")


def corruption(up, chance=100):
    """MD corruption ladder (corruption_level_XX ideas)."""
    eff = "increase_corruption = yes" if up else "decrease_corruption = yes"
    if chance >= 100:
        return eff
    key = f"{P}_tt_corruption_risk_{chance}"
    L(key, f"§R{chance}%§! chance that corruption rises one level.")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ random_list = {{ {chance} = {{ {eff} }} {100 - chance} = {{ }} }} }}"
