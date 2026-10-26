# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Writes the focus tree file of the GDR in the code style of MD's Russia tree (05_russia.txt):
# field order id, icon | x, y, relative_position_id | cost | prerequisite, mutually_exclusive | search_filters | available | bypass |
# completion_reward (log first, newline between modifier groups) | ai_will_do (base + one-line modifiers with scripted triggers).
import re
from dg_common import *
from dg_load import FOCI, BYID, SECT, POS, ANCHOR, ORDER, P
import dg_avail as A
import dg_effects as E

PICK = json.load(open(os.path.join(HERE, "gfxsel", "gfx_pick.json"), encoding="utf-8"))["foci"]
GOAL_SPRITES = {}
for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json"))):
    # MD registers goal sprites with bare names (goals.gfx: name = "sov_gru"); prefer the bare name of a texture
    cur = GOAL_SPRITES.get(p.lower())
    if cur is None or (cur.startswith("GFX_") and not n.startswith("GFX_")):
        GOAL_SPRITES[p.lower()] = n
NEW_SPRITES = {}
ICON_USE = collections.Counter()
BANNED_ICONS = {"gfx/interface/goals/coldwar/stalin_plan.dds", "gfx/interface/goals/coldwar/abmt_1.tga"}

# one search filter per block, like FOCUS_FILTER_RUSSIA_* (loc + filter sprite written by dg_build)
BLOCK_FILTER = {"Politics & Outlooks": ("POLITICS", "GDR: Parties and Outlooks", "gfx/interface/focusview/filter/ukr_between_east_and_west.dds"),
                "SED & First Secretaries": ("SED", "GDR: SED and First Secretaries", "gfx/interface/focusview/filter/internal_factions.dds"),
                "Economy": ("ECONOMY", "GDR: Planned Economy", "gfx/interface/focusview/filter/industry.dds"),
                "Military": ("MILITARY", "GDR: National People's Army", "gfx/interface/focusview/filter/military_equipment.dds"),
                "State Security & Society": ("SECURITY", "GDR: State Security and Society", "gfx/interface/focusview/filter/insurgency.dds"),
                "Foreign Policy": ("FOREIGN", "GDR: Foreign Policy", "gfx/interface/focusview/filter/foreign_policy.dds")}
FILTERS = collections.OrderedDict()     # FOCUS_FILTER_COLDWAR_DDR_<X> -> (English name, texture)
GENERIC_BLOCK_FILTERS = {"FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_ECONOMY", "FOCUS_FILTER_ARMY", "FOCUS_FILTER_FOREIGN_POLICY"}

# the AI follows the historical path (MD Russia: SOV_ai_historical_path); triggers in COLDWAR_DDR_1970_scripted_triggers.txt
AI_TRIGGERS = collections.OrderedDict()
AI_TRIGGERS[f"{PFX}ai_historical_path"] = ["is_historical_focus_on = yes"]
AI_TRIGGERS[f"{PFX}ai_no_power_transfer"] = ["OR = {", f"has_country_flag = {PFX}power_transferred", "is_historical_focus_on = yes", "}"]


def sprite_for(path):
    if path.lower() in GOAL_SPRITES and not GOAL_SPRITES[path.lower()].startswith("GFX_"):
        return GOAL_SPRITES[path.lower()]
    stem = re.sub(r"[^A-Za-z0-9_]", "_", os.path.splitext(path.split("/")[-1])[0])
    name = f"COLDWAR_DDR_goal_{stem}"
    if name in NEW_SPRITES and NEW_SPRITES[name] != path:
        sub = re.sub(r"[^A-Za-z0-9_]", "_", path.split("/")[-2])
        name = f"COLDWAR_DDR_goal_{sub}_{stem}"
    NEW_SPRITES[name] = path
    return name


GOAL_PATHS = sorted({p for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json")))})
USED_TEX = set()      # lower-case texture paths already on a focus (each icon only once in the tree)


def _tokens(s):
    return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if len(t) > 2}


def icon_of(f):
    """the design's icon or one of its alternatives; if all are taken, the most similar unused icon from the same folders
    (house rule: every icon only once in the tree)"""
    pick = PICK[f["id"]]
    cands = [c for c in [pick["icon"]] + pick.get("alt", []) if c.lower() not in BANNED_ICONS]
    for c in cands:
        if c.lower() not in USED_TEX:
            USED_TEX.add(c.lower())
            return sprite_for(c)
    want = _tokens(f["id"].replace(PFX, "") + " " + f["name"])
    folders = {c.rsplit("/", 1)[0].lower() for c in cands} | {"gfx/interface/goals/coldwar", "gfx/interface/goals/ddr", "gfx/interface/goals/germany"}
    best = None
    for p in GOAL_PATHS:
        if p.lower() in USED_TEX or p.lower() in BANNED_ICONS or p.rsplit("/", 1)[0].lower() not in folders:
            continue
        score = len(want & _tokens(p.rsplit("/", 1)[-1])) * 10 + (p.rsplit("/", 1)[0].lower() == cands[0].rsplit("/", 1)[0].lower())
        if best is None or score > best[0]:
            best = (score, p)
    assert best, f["id"]
    USED_TEX.add(best[1].lower())
    ICON_SWAPS[f["id"]] = (cands[0], best[1])
    return sprite_for(best[1])


ICON_SWAPS = {}


def bypass(f):
    """the design's bypass: an equivalent focus elsewhere was done (no double reward)"""
    return re.findall(r"`([^`]+)`", f["bypass_text"] or "")


def section_roots():
    """the entry focus of every section (no prerequisite inside the section)"""
    out = {}
    for f in FOCI:
        k = f["sec"]
        if not any(BYID[p]["sec"] == k for g in f["pre"] for p in g if p in BYID):
            out.setdefault(k, f["id"])
    return out


SEC_ROOT = section_roots()
PROG_SECTIONS = {e["g"] for f in FOCI for e in f["eff"] if e["k"] == "prog"}


def focus_effects(f):
    sid = short(f["id"])
    lines = [f'log = "[GetDateText]: [Root.GetName]: Focus {f["id"]}"']
    for i, e in enumerate(f["eff"]):
        lines += E.compile_effect(e, f, i)
    # entry focus of a party/leader tree: its programme modifier comes visibly, MD SOV_putin order -
    # the programme's add_to_variable lines first (no "modifies" header), then add_dynamic_modifier
    if SEC_ROOT.get(f["sec"]) == f["id"] and f["sec"] in PROG_SECTIONS:
        mod = f"{PFX}{f['sec']}_programme"
        add = f"add_dynamic_modifier = {{ modifier = {mod} }}"
        head = f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {mod} }}"
        if head in lines:
            i = lines.index(head)
            j = i + 1
            while j < len(lines) and lines[j].startswith(f"add_to_variable = {{ {mod}_"):
                j += 1
            lines = lines[:i] + lines[i + 1:j] + [add] + lines[j:]
        else:
            lines.insert(1, add)
    if sid.startswith("power_"):
        lines.append(f"hidden_effect = {{ set_country_flag = {PFX}power_transferred }}")
    # ideas with Cold War modifiers need the recalculation too (mdcw_coldwar_imperia_hooks.md)
    lines += E.cw_hooks_for_ideas(lines)
    # one Cold War recalculation per focus, at the end (after all mdcw_cw_* lines); no trailing newline
    recalc = E.cw_tail(lines)
    out = [l for l in lines if l not in E.CW_LINES]
    while out and out[-1] == E.NEWLINE:
        out.pop()
    out = [l for n, l in enumerate(out) if not (l == E.NEWLINE and n + 1 < len(out) and out[n + 1] == E.NEWLINE)]
    return out + recalc


def ai_block(f):
    sid = short(f["id"])
    if f["id"] == P["header"]["initial_show"]:
        return [f"ai_will_do = {{ base = 1000 }}"]
    if sid.startswith("power_"):
        return ["ai_will_do = {", "base = 1", f"modifier = {{ factor = 0 {PFX}ai_no_power_transfer = yes }}", "}"]
    if sid == "cc_the_letter_of_the_thirteen":
        return ["ai_will_do = { base = 10 }"]
    if f.get("hist"):
        return ["ai_will_do = {", "base = 1", f"modifier = {{ factor = 5 {PFX}ai_historical_path = yes }}", "}"]
    return ["ai_will_do = {", "base = 1", f"modifier = {{ factor = 0.2 {PFX}ai_historical_path = yes }}", "}"]


def filters_of(f):
    key, name, tex = BLOCK_FILTER[SECT[f["sec"]]["b"]]
    own = f"FOCUS_FILTER_COLDWAR_DDR_{key}"
    FILTERS[own] = (name, tex)
    extra = [x for x in (f["filters"] or []) if x not in GENERIC_BLOCK_FILTERS and x != own]
    return [own] + extra[:2]


def one_line(name, lines):
    """MD writes short blocks on one line (available = { emerging_reactionaries_are_in_power = yes })"""
    if len(lines) == 1 and len(lines[0]) < 90 and lines[0].count("{") == lines[0].count("}"):
        return [f"{name} = {{ {lines[0]} }}"]
    return [f"{name} = {{"] + lines + ["}"]


def focus_text(f):
    fid = f["id"]
    x, y = POS[fid]
    anc = ANCHOR[fid]
    Lf = ["focus = {", f"id = {fid}", f"icon = {icon_of(f)}", ""]
    if not anc or anc == fid:
        Lf += [f"x = {x}", f"y = {y}", ""]
    else:
        ax, ay = POS[anc]
        Lf += [f"x = {x - ax}", f"y = {y - ay}", f"relative_position_id = {anc}", ""]
    Lf += [f"cost = {fmt(f['cost'])}", ""]
    pre = ["prerequisite = { " + " ".join(f"focus = {p}" for p in g) + " }" for g in f["pre"]]
    pre += [f"mutually_exclusive = {{ focus = {m} }}" for m in f["mx"]]
    if pre:
        Lf += pre + [""]
    Lf += ["search_filters = { " + " ".join(filters_of(f)) + " }", ""]
    av = A.convert(f)
    if av:
        Lf += one_line("available", [l for l in av.split("\n") if l.strip()]) + [""]
    bp = bypass(f)
    if bp:
        Lf += one_line("bypass", bp if len(bp) == 1 else ["OR = {"] + bp + ["}"]) + [""]
    Lf += ["completion_reward = {"] + focus_effects(f) + ["}", ""]
    Lf += ai_block(f) + ["}"]
    return block(Lf, 1)


def focus_file():
    H = P["header"]
    cfp = H["continuous_focus_position"]
    LOC[TREE_ID] = "East German Focus Tree"
    parts = [HEADER, "focus_tree = {", f"\tid = {TREE_ID}", "\tcountry = {", "\t\tfactor = 0", "\t\tmodifier = {",
             "\t\t\tadd = 100", "\t\t\toriginal_tag = DDR", "\t\t\tIMP_is_1970_scenario = yes", "\t\t}", "\t}",
             "\tdefault = no", "\treset_on_civilwar = no",
             f"\tcontinuous_focus_position = {{ x = {cfp['x']} y = {cfp['y']} }}", "",
             f"\tinitial_show_position = {{ focus = {H['initial_show']} }}", "", "\t# Focus Shortcut"]
    for target, label in H["shortcuts"]:
        key = f"{PFX}{slug(label)}_tree_shortcut"
        parts += ["\tshortcut = {", f"\t\tname = {key}", f"\t\ttarget = {target}", "\t\tscroll_wheel_factor = 0.80", "\t}"]
        LOC[key] = label if label.endswith("Tree") else f"{label} Tree"
    parts.append("")
    for k in ORDER:
        parts.append(f"\t#Start of {SECT[k]['t']} Branch")
        for f in FOCI:
            if f["sec"] == k:
                parts += focus_text(f)
                parts.append("")
                LOC[f["id"]] = f["name"]
                LOC[f["id"] + "_desc"] = (f["desc"] or "").replace('"', "'")
    while parts[-1] == "":
        parts.pop()
    parts.append("}")
    return "\n".join(parts) + "\n"
