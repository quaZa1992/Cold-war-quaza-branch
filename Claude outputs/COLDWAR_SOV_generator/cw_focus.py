# COLDWAR | Writes the focus tree file (layout of the design visualisation, MD 2000 focus style).
import re
from cw_common import *
import cw_layout as L
from cw_layout import FOCI, BYID, SECT, POS, ANCHOR, ORDER, DESC, ICONS
import cw_avail as A
import cw_effects as E
import cw_manual as M
from cw_layout import REPUBLICS

for n, (fid, lean) in enumerate(REPUBLICS.RESOLUTIONS, start=1):
    M.RES_INDEX[fid] = n

GENSEC_KEYS = ["kos", "pod", "sus", "she", "and", "gre", "ust", "gro", "che", "gor", "bre"]
PLENUM_SUCCESS = {}   # key -> code lines run when the plenum votes for the candidate


def tt(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def plenum_focus(f):
    k = short(f["id"]).replace("ple_", "")
    name = E.GENSEC[k][0]
    effs = f["eff"]
    i0 = next(i for i, e in enumerate(effs) if e["k"] == "note" and e["t"].startswith("Bei Mehrheit"))
    i1 = next(i for i, e in enumerate(effs) if e["k"] == "note" and e["t"].startswith("Ohne Mehrheit"))
    succ = []
    for e in effs[i0 + 1:i1]:
        succ += E.compile_effect(e, f) if e["k"] != "gensec" else [f"{PFX}install_gensec_{k} = yes"]
    PLENUM_SUCCESS[k] = succ
    lean = E.GENSEC_LEAN[k]
    LOC[f"{PFX}candidacy_{k}_tt"] = (
        f"§Y{name}§! becomes a candidate for General Secretary. The decision §YConvene the Plenum: {name}§! asks the Politburo to elect him "
        f"(the Moscow members vote {['as reformers', 'by the balance', 'as the orthodox'][lean + 1]}, the three republican seats vote freely). "
        f"With a majority he takes over; without one nothing changes, stability falls by §R3%§! and the balance shifts against him.")
    return [f"set_country_flag = {PFX}candidate_{k}", f"custom_effect_tooltip = {PFX}candidacy_{k}_tt"]


EXTRA = {   # extra code for single foci (implementation notes of the design)
    "the_treaty_with_egypt": [f"if = {{ limit = {{ has_country_flag = {PFX}treaty_signer }} add_political_power = 25 }}"],
    "treaty_with_india": [f"if = {{ limit = {{ has_country_flag = {PFX}treaty_signer }} add_political_power = 25 }}"],
    "syria_and_iraq": [f"if = {{ limit = {{ has_country_flag = {PFX}treaty_signer }} add_political_power = 25 }}"],
    "bre_the_kremlin_doctors": [f"set_country_flag = {PFX}kremlin_doctors", tt("kremlin_doctors", "The Kremlin doctors keep §YBrezhnev§! alive: his death comes up to §Ytwo years§! later than history recorded.")],
}
BYPASS = {
    "operation_kavkaz": "country_exists = EGY\nEGY = { has_idea = COLDWAR_EGY_operation_kavkaz }",
}


def focus_effects(f):
    sid = short(f["id"])
    lines = [f'log = "[GetDateText]: [Root.GetName]: Focus {f["id"]}"']
    if f["sec"] == "ple" and sid != "ple_the_politburo":
        return lines + plenum_focus(f)
    for e in f["eff"]:
        lines += E.compile_effect(e, f)
    if sid.startswith("dir_"):
        gov = {"dir_the_leading_role": "communism", "dir_convergence": "democratic", "dir_third_way": "neutrality",
               "dir_the_russian_idea": "nationalist"}[sid]
        lines.append(f"hidden_effect = {{ if = {{ limit = {{ has_government = {gov} }} set_country_flag = {PFX}direction_under_{gov} }} }}")
    if sid.startswith("power_"):
        lines.append(f"hidden_effect = {{ set_country_flag = {PFX}power_transferred }}")
    lines += EXTRA.get(sid, [])
    return lines


SEARCH = [
    ({"party", "rp", "outlook", "heir", "elections", "bop", "gensec", "leader", "trait"}, "FOCUS_FILTER_POLITICAL"),
    ({"tech", "space", "sp"}, "FOCUS_FILTER_RESEARCH"),
    ({"build"}, "FOCUS_FILTER_INDUSTRY"),
    ({"stab"}, "FOCUS_FILTER_STABILITY"),
    ({"ws"}, "FOCUS_FILTER_WAR_SUPPORT"),
    ({"fac"}, "FOCUS_FILTER_INTERNAL_FACTION"),
    ({"offer", "op", "infl", "tension", "cwjoin"}, "FOCUS_FILTER_INFLUENCE"),
    ({"corr"}, "FOCUS_FILTER_CORRUPTION"),
    ({"gdp", "gdp_gain", "debt", "law"}, "FOCUS_FILTER_EXPENDITURE"),
    ({"xp", "cp", "mastery", "manpower"}, "FOCUS_FILTER_MILITARY_LAWS"),
]


def search_filters(f):
    kinds = {e["k"] for e in f["eff"]}
    if f["sec"] in ("army", "str", "navy"):
        kinds.add("xp")
    if any(e["k"] == "dyn" and e["g"] == "armed_forces" for e in f["eff"]):
        kinds.add("xp")
    out = [fl for ks, fl in SEARCH if kinds & ks]
    return out[:4] or ["FOCUS_FILTER_POLITICAL"]


# ------------------------------------------------------------ icons / sprites
GOAL_SPRITES = {}
for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json"))):
    GOAL_SPRITES.setdefault(p.lower(), n)
NEW_SPRITES = {}
ICON_USE = collections.Counter()


def sprite_for(path):
    if path.lower() in GOAL_SPRITES:
        return GOAL_SPRITES[path.lower()]
    stem = re.sub(r"[^A-Za-z0-9_]", "_", os.path.splitext(path.split("/")[-1])[0])
    name = f"GFX_COLDWAR_goal_{stem}"
    if name in NEW_SPRITES and NEW_SPRITES[name] != path:
        sub = re.sub(r"[^A-Za-z0-9_]", "_", path.split("/")[-2])
        name = f"GFX_COLDWAR_goal_{sub}_{stem}"
    NEW_SPRITES[name] = path
    return name


def icon_of(f):
    pick = ICONS[f["id"]]
    cands = [pick["icon"]] + pick.get("alt", [])
    for c in cands:
        if ICON_USE[c] < 3:
            ICON_USE[c] += 1
            return sprite_for(c)
    ICON_USE[cands[0]] += 1
    return sprite_for(cands[0])


# ------------------------------------------------------------ AI
def ai_block(f):
    sid = short(f["id"])
    if f.get("ai") == "0":
        return ["ai_will_do = {", "base = 0", "}"]
    if sid.startswith("power_"):
        return ["ai_will_do = {", "base = 1", "modifier = {", "factor = 0", f"has_country_flag = {PFX}power_transferred", "}",
                "modifier = {", "factor = 0", "is_historical_focus_on = yes", "}", "}"]
    if f["sec"] == "ple" and sid != "ple_the_politburo":
        return ["ai_will_do = {", "base = 0", "}"]   # the AI changes leaders only through the historical deaths
    if f.get("hist"):
        return ["ai_will_do = {", "base = 10", "}"]
    return ["ai_will_do = {", "base = 3", "modifier = {", "factor = 0.1", "is_historical_focus_on = yes", "}", "}"]


def focus_text(f):
    fid = f["id"]
    sid = short(fid)
    x, y = POS[fid]
    anc = ANCHOR[f["sec"]]
    Lf = ["focus = {", f"id = {fid}", f"icon = {icon_of(f)}", ""]
    if anc == fid:
        Lf += [f"x = {x}", f"y = {y}", ""]
    else:
        ax, ay = POS[anc]
        Lf += [f"x = {x - ax}", f"y = {y - ay}", f"relative_position_id = {anc}", ""]
    Lf += [f"cost = {fmt(f['cost'])}", ""]
    for g in f["pre"]:
        Lf.append("prerequisite = { " + " ".join(f"focus = {p}" for p in g) + " }")
    if f["mx"]:
        Lf.append("mutually_exclusive = { " + " ".join(f"focus = {m}" for m in f["mx"]) + " }")
    av = A.convert(f)
    for g in f.get("_xav", []):
        cond = " ".join(f"has_completed_focus = {p}" for p in g)
        av = (av + "\n" + (cond if len(g) == 1 else f"OR = {{ {cond} }}")).strip()
    if av:
        Lf += ["", "available = {"] + [l for l in av.split("\n") if l.strip()] + ["}"]
    if sid in BYPASS:
        Lf += ["", "bypass = {"] + BYPASS[sid].split("\n") + ["}"]
    Lf += ["", "search_filters = { " + " ".join(search_filters(f)) + " }", "", "completion_reward = {"]
    Lf += focus_effects(f)
    Lf += ["}", ""] + ai_block(f) + ["}"]
    return block(Lf, 1)


SHORT_EN = {
    "pol": "The Collective Leadership", "em": "Emerging Outlook", "we": "Western Outlook", "na": "Non-Aligned Outlook",
    "nt": "Nationalist Outlook", "cpsu": "CPSU: The Party of Lenin", "ple": "The Politburo", "bre": "Brezhnev", "kos": "Kosygin",
    "pod": "Podgorny", "sus": "Suslov", "she": "Shelepin", "and": "Andropov", "gre": "Marshal Grechko", "ust": "Marshal Ustinov",
    "gro": "Romanov", "che": "Chernenko", "gor": "Gorbachev", "eco": "Gosplan and the Five-Year Plans", "agr": "Agriculture and Grain",
    "en": "Energy, Siberia and the BAM", "sci": "Science and Space", "army": "The Soviet Army", "str": "Strategic Forces and Air Defence",
    "navy": "The Ocean-Going Fleet", "kgb": "The KGB", "union": "The Union of Republics", "soc": "Soviet Society",
    "det": "Detente and the West", "chi": "The Chinese Question", "bloc": "Warsaw Pact and Comecon", "tw": "The Third World",
}


def section_title_en(k):
    if k in SHORT_EN:
        return SHORT_EN[k]
    m = re.match(r"^Partei: (.+?) \((\d+)\)$", SECT[k]["title"])
    return m.group(1)


def focus_file():
    pol = L.SEC_ORIGIN["pol"]
    parts = [HEADER, "focus_tree = {", f"\tid = {TREE_ID}", "\tcountry = {", "\t\tfactor = 0", "\t\tmodifier = {",
             "\t\t\tadd = 30", "\t\t\toriginal_tag = SOV", "\t\t\tIMP_is_1970_scenario = yes", "\t\t}", "\t}",
             "\tdefault = no", "\treset_on_civilwar = no",
             f"\tcontinuous_focus_position = {{ x = {(pol[0] + pol[2] + 6) * 96} y = 100 }}",
             f"\tinitial_show_position = {{ focus = {ANCHOR['pol']} }}", ""]
    for k in ORDER:
        parts += ["\tshortcut = {", f"\t\tname = {PFX}shortcut_{k}", f"\t\ttarget = {ANCHOR[k]}", "\t\tscroll_wheel_factor = 0.80", "\t}"]
        LOC[f"{PFX}shortcut_{k}"] = section_title_en(k)
    parts.append("")
    for k in ORDER:
        parts.append(f"\t### COLDWAR | {SECT[k]['title']} ###")
        for f in FOCI:
            if f["sec"] == k:
                parts += focus_text(f)
                parts.append("")
                LOC[f["id"]] = f["name"]
                LOC[f["id"] + "_desc"] = DESC[f["id"]].replace('"', "'")
    parts.append("}")
    return "\n".join(parts) + "\n"
