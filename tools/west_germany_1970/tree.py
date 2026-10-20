"""The West Germany 1970 focus tree, built after MD's Russia and Israel trees.

* one root and a hub focus per pillar; every other focus is placed with relative_position_id
* short costs (1 hub, 2 quick, 3 standard, 5 reform, 7 major project)
* eight core spirits (dynamic modifiers) that focuses grow step by step, shown as
  "Modifies <core>" blocks in the reward tooltip
* concrete effects: buildings and modifiers in named states, railways, MD influence,
  internal factions, treasury, BoP, decisions and window functions unlocked
* path flags drive the AI (historical: rapprochement, the 1982 change of government, unity)
"""
import json
import os
from cw_lib import P, L, J, fmt, tt as _tt

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = json.load(open(os.path.join(HERE, "old_focus_text.json"), encoding="utf-8"))

FOCUSES = []          # dicts, in definition order
BY_KEY = {}

# ------------------------------------------------------------------ core spirits
# core -> (title, icon, description, {short: (modifier, kind, good_if_positive, label)})
CORES = {
    "bonn": ("The Chancellor's Office", "GFX_idea_political_power_bonus",
             "The machinery of government in Bonn: the chancellery, the coalition committee and the art of the majority.",
             {"stab": ("stability_factor", "pct", True, "Stability"),
              "pp": ("political_power_factor", "pct", True, "Political power gain"),
              "drift": ("drift_defence_factor", "pct", True, "Ideology drift defence"),
              "bureau": ("bureaucracy_cost_multiplier_modifier", "pct", False, "Bureaucracy costs")}),
    "modell": ("Modell Deutschland", "GFX_idea_stable_growth",
               "Social partnership, a hard currency and the export machine.",
               {"prod": ("productivity_growth_modifier", "pct", True, "Productivity growth"),
                "cg": ("consumer_goods_factor", "pct", False, "Consumer goods"),
                "fac": ("industrial_capacity_factory", "pct", True, "Factory output"),
                "tax": ("tax_gain_multiplier_modifier", "pct", True, "Tax revenue"),
                "social": ("social_cost_multiplier_modifier", "pct", False, "Social spending costs"),
                "build": ("production_speed_buildings_factor", "pct", True, "Construction speed")}),
    "energie": ("The Energy Mix", "GFX_idea_coal",
                "Coal from the Ruhr, oil from the Gulf, gas from Siberia, power from the reactors - and the bill for each.",
                {"gain": ("energy_gain_multiplier", "pct", True, "Energy production"),
                 "fossil": ("fossil_fuel_consumption", "pct", False, "Fossil fuel consumption"),
                 "nuclear": ("nuclear_energy_gain", "pct", True, "Nuclear energy"),
                 "renew": ("renewable_energy_gain_multiplier", "pct", True, "Renewable energy"),
                 "use": ("energy_use_multiplier", "pct", False, "Energy consumption")}),
    "wehrhaft": ("Militant Democracy", "GFX_idea_spy_intel",
                 "A democracy that defends itself - against its enemies and, sometimes, against its own excesses.",
                 {"detect": ("terror_threat_detection_modifier", "pct", True, "Terror detection"),
                  "defend": ("terror_threat_base_defense_modifier", "pct", True, "Terror defence"),
                  "police": ("police_cost_multiplier_modifier", "pct", False, "Police costs"),
                  "influence": ("foreign_influence_defense_modifier", "pct", True, "Foreign influence defence")}),
    "armee": ("An Army in the Alliance", "GFX_idea_NATO_member",
              "Twelve divisions on the inner-German border, assigned to NATO from the first day of war.",
              {"org": ("army_org_factor", "pct", True, "Division organisation"),
               "core": ("army_core_defence_factor", "pct", True, "Defence on core territory"),
               "xp": ("experience_gain_army", "flat", True, "Daily army experience"),
               "consc": ("conscription_factor", "pct", True, "Recruitable population"),
               "equip": ("equipment_cost_multiplier_modifier", "pct", False, "Equipment costs"),
               "plan": ("max_planning", "pct", True, "Maximum planning")}),
    "west": ("Anchored in the West", "GFX_idea_european_union_member",
             "NATO, the Community, Paris and Washington: Bonn's foreign policy has one fixed point.",
             {"trade": ("trade_opinion_factor", "pct", True, "Trade opinion"),
              "research": ("research_speed_factor", "pct", True, "Research speed"),
              "europe": ("europeanism_drift", "flat", True, "Europeanism drift"),
              "ideo": ("mdcw_cw_ideological_defence", "pct", True, "Ideological defence (Cold War)"),
              "opinion": ("opinion_gain_monthly_factor", "pct", True, "Monthly opinion gain")}),
    "ost": ("Deutschlandpolitik", "GFX_idea_anti_soviet_pact",
            "Bonn's policy towards the other German state - and the price it pays for it at home.",
            {"stab": ("stability_factor", "pct", True, "Stability"),
             "ws": ("war_support_factor", "pct", True, "War support"),
             "cg": ("consumer_goods_factor", "pct", False, "Consumer goods"),
             "sanc": ("imp_sanction_resistance", "pct", True, "Sanction resistance")}),
    "welt": ("A Civilian Power", "GFX_idea_trade",
             "An economic giant that wants to be more than a political dwarf - without guns.",
             {"cap": ("mdcw_cw_assistance_capacity", "flat", True, "Assistance capacity"),
              "eff": ("mdcw_cw_assistance_effectiveness", "pct", True, "Assistance effectiveness"),
              "support": ("mdcw_cw_support_effectiveness", "pct", True, "Political support effectiveness"),
              "market": ("international_market_income_modifier", "pct", True, "International market income")}),
}
# the Deutschlandpolitik core has two faces, swapped by the policy choice
OST_NAMES = {"neutral": "Deutschlandpolitik", "rapprochement": "Change through Rapprochement", "strength": "Policy of Strength"}


def ost_face(face):
    """Swap the face of the Deutschlandpolitik core (same variables, different name)."""
    out = [f"if = {{ limit = {{ has_dynamic_modifier = {{ modifier = {P}_core_ost_{k} }} }} remove_dynamic_modifier = {{ modifier = {P}_core_ost_{k} }} }}"
           for k in OST_NAMES if k != face]
    out.append(f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {P}_core_ost_{face} }} }} }} add_dynamic_modifier = {{ modifier = {P}_core_ost_{face} }} }}")
    key = f"cwfo_tt_ostface_{face}"
    L(key, f"The core spirit §Y{CORES['ost'][0]}§! becomes §Y{OST_NAMES[face]}§!.")
    return f"custom_effect_tooltip = {key}\nhidden_effect = {{ " + " ".join(out) + " }"


# state dynamic modifiers used by focuses: key -> (name, {modifier: value})
STATE_MODS = {
    "bavarian_model": ("The Bavarian Model", {"state_production_speed_buildings_factor": 0.15, "local_building_slots": 1}),
    "red_green_land": ("Red-Green Land Government", {"state_renewable_energy_generation_modifier": 0.2}),
    "capital_berlin": ("Capital of Germany", {"state_production_speed_buildings_factor": 0.25, "local_building_slots": 2}),
    "steel_rescue": ("Steel Rescue", {"state_productivity_growth_modifier": 0.05}),
    "high_tech": ("High-Tech Region", {"state_productivity_growth_modifier": 0.08, "local_building_slots": 1}),
    "ruhr_change": ("Structural Change in the Ruhr", {"state_productivity_growth_modifier": 0.05, "state_production_speed_buildings_factor": 0.1}),
    "showcase": ("Showcase of the West", {"state_production_speed_buildings_factor": 0.2, "local_building_slots": 1}),
    "garrison": ("Franco-German Brigade", {"local_building_slots": 1}),
    "olympic_city": ("Olympic City", {"state_production_speed_buildings_factor": 0.15}),
    "expo": ("Expo Site", {"state_productivity_growth_modifier": 0.03}),
}


def core_var(core, short):
    return f"cwfo_{core}_{short}"


def fmt_val(kind, x):
    if kind == "pct":
        return f"{x * 100:+.0f}%" if abs(x * 100 - round(x * 100)) < 1e-9 else f"{x * 100:+.1f}%"
    return f"{x:+g}"


def core(name, **mods):
    """Grow a core spirit: a 'Modifies ...' header plus one line per modifier, MD style."""
    title, _icon, _d, defs = CORES[name]
    head = f"cwfo_tt_head_{name}"
    L(head, f"Modifies §Y{title}§! by:")
    out = [f"custom_effect_tooltip = {head}"]
    hidden = []
    for short, val in mods.items():
        mod, kind, good, label = defs[short]
        sval = fmt_val(kind, val)
        col = "G" if (val > 0) == good else "R"
        key = f"cwfo_tt_{name}_{short}_{str(val).replace('-', 'm').replace('.', '_')}"
        L(key, f"  {label}: §{col}{sval}§!")
        out.append(f"custom_effect_tooltip = {key}")
        hidden.append(f"add_to_variable = {{ {core_var(name, short)} = {val} }}")
    out.append("hidden_effect = { " + " ".join(hidden) + " }")
    return "\n".join(out)


def core_modifiers_file():
    out = []
    for name, (title, icon, desc, defs) in CORES.items():
        faces = [(f"{P}_core_{name}", title)] if name != "ost" else [(f"{P}_core_ost_{k}", t) for k, t in OST_NAMES.items()]
        for n, t in faces:
            L(n, t)
            L(n + "_desc", desc)
            lines = [f"{n} = {{", f"\ticon = {icon}", "\tenable = { always = yes }"]
            for short, (mod, kind, good, label) in defs.items():
                lines.append(f"\t{mod} = {core_var(name, short)}")
            lines.append("}")
            out.append("\n".join(lines))
    return "\n\n".join(out) + "\n"


def core_setup():
    lines = []
    for name, (_t, _i, _d, defs) in CORES.items():
        for short in defs:
            lines.append(f"set_variable = {{ {core_var(name, short)} = 0 }}")
        if name != "ost":
            lines.append(f"add_dynamic_modifier = {{ modifier = {P}_core_{name} }}")
    # starting values: the Bonn Republic of 1969
    lines += [f"set_variable = {{ {core_var('west', 'trade')} = 0.1 }}", f"set_variable = {{ {core_var('armee', 'core')} = 0.05 }}",
              f"set_variable = {{ {core_var('energie', 'fossil')} = 0.1 }}", f"set_variable = {{ {core_var('modell', 'prod')} = 0.02 }}"]
    return "\n".join(lines)


# ------------------------------------------------------------------ effect helpers
def unlock(flag, text, key=None):
    """Unlock something with an explanatory line (like MD's unlock_decision_tooltip)."""
    k = key or f"cwfo_tt_unlock_{flag}"
    L(k, f"§GUnlocks:§! {text}")
    return f"custom_effect_tooltip = {k}\nhidden_effect = {{ set_country_flag = {flag} }}"


def unlock_dec(dec_key):
    return f"unlock_decision_tooltip = {P}_dec_{dec_key}"


SHARED = {"industrial_complex", "arms_factory", "dockyard", "offices", "fossil_powerplant", "nuclear_reactor", "renewable_energy_infra"}


def state_build(state, btype, level=1, slot=True):
    s = f"if = {{ limit = {{ {state} = {{ is_owned_by = ROOT }} }} {state} = {{ "
    if slot and btype in SHARED:
        s += f"add_extra_state_shared_building_slots = {level} "
    s += f"add_building_construction = {{ type = {btype} level = {level} instant_build = yes }} }} }}"
    return s


def state_mod(state, modifier):
    if modifier not in STATE_MODS:
        raise KeyError("state modifier " + modifier)
    return (f"if = {{ limit = {{ {state} = {{ is_owned_by = ROOT NOT = {{ has_dynamic_modifier = {{ modifier = {P}_sdm_{modifier} }} }} }} }} "
            f"{state} = {{ add_dynamic_modifier = {{ modifier = {P}_sdm_{modifier} }} }} }}")


def state_modifiers_file():
    out = []
    for k, (name, mods) in STATE_MODS.items():
        n = f"{P}_sdm_{k}"
        L(n, name)
        out.append(f"{n} = {{\n\ticon = GFX_idea_economic_boom\n\tenable = {{ always = yes }}\n" + "".join(f"\t{m} = {v}\n" for m, v in mods.items()) + "}")
    return "\n\n".join(out) + "\n"


def rail(a, b, level=1):
    return f"build_railway = {{ level = {level} start_province = {a} target_province = {b} }}"


def infl(target, pct):
    key = f"cwfo_tt_infl_{target}_{pct}"
    L(key, f"Our influence in §Y[{target}.GetName]§!: §G+{pct}%§!")
    return (f"if = {{ limit = {{ country_exists = {target} }} custom_effect_tooltip = {key} hidden_effect = {{ set_temp_variable = {{ percent_change = {pct} }} "
            f"set_temp_variable = {{ tag_index = GER }} set_temp_variable = {{ influence_target = {target} }} change_influence_percentage = yes }} }}")


def opinion(tag, mod="medium_increase", mutual=False):
    s = f"if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ add_opinion_modifier = {{ target = ROOT modifier = {mod} }} }}"
    if mutual:
        s += f" add_opinion_modifier = {{ target = {tag} modifier = {mod} }}"
    return s + " }"


def swap(old, new):
    return f"if = {{ limit = {{ has_idea = {P}_idea_{old} }} swap_ideas = {{ remove_idea = {P}_idea_{old} add_idea = {P}_idea_{new} }} }} else = {{ add_ideas = {P}_idea_{new} }}"


def remove_idea(i):
    return f"if = {{ limit = {{ has_idea = {P}_idea_{i} }} remove_ideas = {P}_idea_{i} }}"


def gamevar(var, n, text_key, text):
    """Change a mini-game variable with an explicit tooltip line."""
    L(text_key, text)
    return f"custom_effect_tooltip = {text_key}\nhidden_effect = {{ add_to_variable = {{ {var} = {n} }} }}"


def climate_base(n):
    return gamevar("cwgg_basis_bonus", n, f"cwfo_tt_basis_{'up' if n > 0 else 'down'}_{abs(n)}",
                   f"Inner-German climate base: §{'G' if n > 0 else 'R'}{'+' if n > 0 else '-'}{abs(n)}§! (permanent)")


def sec_slots(n=1):
    return gamevar("cwsec_slots", n, f"cwfo_tt_slots_{n}", f"Protection details for the RAF's targets: §G+{n}§!")


def bka(n=1):
    return gamevar("cwger_bka_level", n, f"cwfo_tt_bka_{n}", f"BKA level: §G+{n}§! (manhunt, foiled attacks, intelligence on the RAF's plans)")


def gsg9(n=1):
    return gamevar("cwger_gsg9_tier", n, f"cwfo_tt_gsg9_{n}", f"GSG 9 tier: §G+{n}§! (raids and rescues)")


# ------------------------------------------------------------------ focus DSL
ROOT_KEY = "government_statement"


def F(key, rel, dx, dy, cost=3, name=None, desc=None, icon=None, pre=None, mutex=None, avail="", bypass="",
      reward="", ai=10, ai_mod="", filt="FOCUS_FILTER_POLITICAL", pillar=None, cancel=False, wargoal=None):
    """rel: key of the focus this one is positioned against (None for the root)."""
    o = OLD.get(key, {})
    name = name or o.get("name")
    desc = desc or o.get("desc")
    icon = icon or o.get("icon", "parliament")
    if name is None or desc is None:
        raise ValueError("focus text missing for " + key)
    if rel is not None and rel not in BY_KEY:
        raise ValueError(f"{key}: relative position {rel} not defined yet")
    if pillar is None:
        pillar = "root" if rel is None else (key if rel == ROOT_KEY else BY_KEY[rel]["pillar"])
    ax = (BY_KEY[rel]["ax"] if rel else 0) + dx
    ay = (BY_KEY[rel]["ay"] if rel else 0) + dy
    if pre is None:
        pre = [[rel]] if rel else []
    fc = dict(key=key, id=f"{P}_{key}", rel=rel, dx=dx, dy=dy, ax=ax, ay=ay, cost=cost, name=name, desc=desc, icon=icon,
              pre=pre, mutex=mutex or [], avail=avail, bypass=bypass, reward=reward, ai=ai, ai_mod=ai_mod, filt=filt,
              pillar=pillar, wargoal=wargoal)
    FOCUSES.append(fc)
    BY_KEY[key] = fc
    return key


# All focuses take longer: the costs in the modules are relative weights, the game sees cost x factor
# (one cost unit = 7 days). Factor 2 puts the typical focus at 42 days.
FOCUS_TIME_FACTOR = 2


def focus_cost(c):
    return max(1, int(round(c * FOCUS_TIME_FACTOR)))


def check_layout():
    pos, problems = {}, []
    for fc in FOCUSES:
        p = (fc["ax"], fc["ay"])
        if p in pos:
            problems.append(f"overlap {fc['key']} / {pos[p]} at {p}")
        pos[p] = fc["key"]
        for g in fc["pre"]:
            for k in g:
                if k not in BY_KEY:
                    problems.append(f"{fc['key']}: unknown prerequisite {k}")
                elif BY_KEY[k]["ay"] >= fc["ay"]:
                    problems.append(f"{fc['key']}: prerequisite {k} not above")
        for m in fc["mutex"]:
            if m not in BY_KEY:
                problems.append(f"{fc['key']}: unknown mutex {m}")
    return problems


def mutex_symmetric():
    for fc in FOCUSES:
        for m in fc["mutex"]:
            other = BY_KEY[m]
            if fc["key"] not in other["mutex"]:
                other["mutex"].append(fc["key"])


# ------------------------------------------------------------------ automatic layout
COMPACT_ROWS = True   # rows from the prerequisites only (no empty rows inside a branch)
SIB_GAP = 2      # x distance between neighbouring focuses (MD convention)
PILLAR_GAP = 3   # x distance between the outermost focuses of two pillars


def auto_layout():
    """Recompute every focus position as a compact tidy tree, MD style.

    Rows: a focus sits one row below its lowest prerequisite (event-gated focuses without
    prerequisites sit one row below the focus they are anchored to). Columns: each pillar is laid
    out as a tree over its first in-pillar prerequisite, children packed left to right by their
    row contours with SIB_GAP, the parent centred over its children; pillars are packed side by side
    with PILLAR_GAP and the root centred over the hubs. relative_position_id stays as written;
    x/y are recomputed against it.
    """
    order = {fc["key"]: i for i, fc in enumerate(FOCUSES)}
    root = BY_KEY[ROOT_KEY]
    # ---- rows: one below the lowest prerequisite (or the designer's row, see COMPACT_ROWS)
    y = {}

    def row(k):
        if k in y:
            return y[k]
        fc = BY_KEY[k]
        preds = [p for g in fc["pre"] for p in g]
        if k == ROOT_KEY:
            v = 0
        elif COMPACT_ROWS and preds:
            v = max(row(p) + 1 for p in preds)
        elif COMPACT_ROWS and fc["rel"] and fc["rel"] != ROOT_KEY:
            v = row(fc["rel"]) + 1
        else:
            v = max([fc["ay"]] + [row(p) + 1 for p in preds])
        y[k] = v
        return v

    for fc in FOCUSES:
        row(fc["key"])
    # ---- layout parent: first prerequisite in the same pillar, else the anchor
    kids = {fc["key"]: [] for fc in FOCUSES}
    for fc in FOCUSES:
        if fc["key"] == ROOT_KEY:
            continue
        cand = [p for g in fc["pre"] for p in g if BY_KEY[p]["pillar"] == fc["pillar"] and p != ROOT_KEY]
        if fc["rel"] == ROOT_KEY:
            parent = ROOT_KEY
        elif cand:
            parent = max(cand, key=lambda p: (y[p], -order[p]))   # the lowest prerequisite, so lines stay short
        else:
            parent = fc["rel"]
        kids[parent].append(fc["key"])
    for k in kids:
        # keep the designer's left-to-right intent (old x), event-gated branches to the right
        kids[k].sort(key=lambda c: (not BY_KEY[c]["pre"], BY_KEY[c]["ax"], order[c]))

    def place(k):
        """Return (x offsets relative to k, contour {row: (min, max)})."""
        xs = {k: 0}
        cont = {y[k]: (0, 0)}
        if not kids[k]:
            return xs, cont
        packed_x, packed_c = {}, {}
        firsts = []
        for c in kids[k]:
            cx, cc = place(c)
            shift = 0
            if packed_c:
                common = [r for r in cc if r in packed_c]
                if common:
                    shift = max(packed_c[r][1] + SIB_GAP - cc[r][0] for r in common)
                else:
                    # nothing in the way on these rows: tuck the branch under its left neighbours
                    shift = min(v[0] for v in packed_c.values()) - min(v[0] for v in cc.values())
            for n, v in cx.items():
                packed_x[n] = v + shift
            for r, (a, b) in cc.items():
                a, b = a + shift, b + shift
                if r in packed_c:
                    packed_c[r] = (min(packed_c[r][0], a), max(packed_c[r][1], b))
                else:
                    packed_c[r] = (a, b)
            if BY_KEY[c]["pre"]:
                firsts.append(packed_x[c])
        if not firsts:
            firsts = [packed_x[kids[k][0]]]
        mid = (firsts[0] + firsts[-1]) // 2
        for n, v in packed_x.items():
            xs[n] = v - mid
        for r, (a, b) in packed_c.items():
            a, b = a - mid, b - mid
            cont[r] = (min(cont.get(r, (a, b))[0], a), max(cont.get(r, (a, b))[1], b))
        return xs, cont

    def subtree(k):
        out = [k]
        for c in kids[k]:
            out += subtree(c)
        return out

    # event-gated branches (no prerequisite) of a pillar go into a block beside the pillar
    orphan_roots = {}
    for fc in FOCUSES:
        k = fc["key"]
        if k == ROOT_KEY or fc["rel"] == ROOT_KEY or fc["pre"]:
            continue
        nodes = set(subtree(k))
        # only if nothing in the branch depends on a focus outside it
        if all(p in nodes for n in nodes for g in BY_KEY[n]["pre"] for p in g):
            orphan_roots.setdefault(fc["pillar"], []).append(k)
    for roots in orphan_roots.values():
        for r in roots:
            for k in kids:
                if r in kids[k]:
                    kids[k].remove(r)

    hubs = kids[ROOT_KEY]
    hubs.sort(key=lambda h: BY_KEY[h]["ax"])
    absx, packed = {}, {}
    for h in hubs:
        hx, hc = place(h)
        roots = sorted(orphan_roots.get(h, []), key=lambda r: (BY_KEY[r]["ax"], order[r]))
        if roots:
            start = y[h] + 1
            bottom = max(hc)
            blocks = []
            for r in roots:
                rx, _rc = place(r)
                off = {n: y[n] - y[r] for n in rx}
                blocks.append((r, rx, off, max(off.values()) + 1, min(rx.values()), max(rx.values())))
            limit = max(bottom - start + 1, max(b[3] for b in blocks))
            cols, cur, used = [], [], 0
            for b in blocks:
                if cur and used + b[3] > limit:
                    cols.append(cur)
                    cur, used = [], 0
                cur.append((b, used))
                used += b[3] + 1
            cols.append(cur)
            x0 = max(v[1] for v in hc.values()) + SIB_GAP
            for col in cols:
                left = min(b[4] for b, _ in col)
                right = max(b[5] for b, _ in col)
                for (r, rx, off, _hgt, _l, _rr), r0 in col:
                    for n, v in rx.items():
                        hx[n] = x0 - left + v
                        y[n] = start + r0 + off[n]
                        a = hx[n]
                        hc[y[n]] = (min(hc.get(y[n], (a, a))[0], a), max(hc.get(y[n], (a, a))[1], a))
                x0 += right - left + SIB_GAP
        shift = 0
        if packed:
            # pillars stay separate blocks: no branch of one pillar slides under its neighbour
            shift = max(v[1] for v in packed.values()) + PILLAR_GAP - min(v[0] for v in hc.values())
        for n, v in hx.items():
            absx[n] = v + shift
        for r, (a, b) in hc.items():
            a, b = a + shift, b + shift
            packed[r] = (min(packed[r][0], a), max(packed[r][1], b)) if r in packed else (a, b)
    absx[ROOT_KEY] = (absx[hubs[0]] + absx[hubs[-1]]) // 2
    lo = min(absx.values())
    for fc in FOCUSES:
        fc["ax"], fc["ay"] = absx[fc["key"]] - lo, y[fc["key"]]
    for fc in FOCUSES:
        if fc["rel"]:
            fc["dx"] = fc["ax"] - BY_KEY[fc["rel"]]["ax"]
            fc["dy"] = fc["ay"] - BY_KEY[fc["rel"]]["ay"]
        else:
            fc["dx"], fc["dy"] = fc["ax"], fc["ay"]
