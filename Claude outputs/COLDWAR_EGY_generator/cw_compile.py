# IMPERIA CW — Cold War: Egypt 1970 content generator.
# COLDWAR | Generator for the Egypt 1970 focus tree.
# Source of truth: egy_tree.json (approved design v2, 805 foci) + desc/out_*.json (English descriptions)
# + desc/icons_*.json (icon picks). Writes the mod files into ./out/<mod-relative path>.
import json, re, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from cw_common import *
import cw_effects as E
from cw_effects import R, MAN, EVLINES
import cw_avail as A
import cw_events as EV

OUT = "out"
D = json.load(open("egy_tree.json"))
FOCI = D["foci"]
SECT = {s["key"]: s for s in D["sections"]}
BYID = {f["id"]: f for f in FOCI}
DESC = {}
ICONS = {}
for g in range(1, 6):
    DESC.update(json.load(open(f"desc/out_{g}.json")))
    ICONS.update(json.load(open(f"desc/icons_{g}.json")))

# ---- design fixes agreed in implementation (documented in the project doc)
import cw_october as OCT
D["sections"].insert([s["key"] for s in D["sections"]].index("arab"), OCT.SECTION)
SECT = {s["key"]: s for s in D["sections"]}
for f in OCT.FOCI:
    f = dict(f)
    DESC[f["id"]] = f.pop("desc")
    ICONS[f["id"]] = {"icon": f.pop("icon"), "alt": []}
    f.setdefault("av", "")
    f.setdefault("note", "")
    f.setdefault("bypass", "")
    FOCI.append(f)
BYID = {f["id"]: f for f in FOCI}

# ---- independent trees: no prerequisite lines between sections (request 14 Oct 2026)
# outlook blocks: remember which foci form the "strengthen the outlook" part before cutting the links
STRONG = set()
for f in FOCI:
    if f["sec"] in ("na", "em", "we", "sa", "nt"):
        pre = [p for g in f["pre"] for p in g]
        if any(p.startswith("EGY_1970_dir_") for p in pre) or any(p in STRONG for p in pre):
            STRONG.add(f["id"])
PARTY_SECS = {k for k, s in SECT.items() if re.search(r"\((\d+)\)$", s["title"])}
OUTLOOK_PARTIES = {"na": ["asu", "tp", "mb", "tag", "fc", "nb", "fe", "fn"], "em": ["cop", "ecp", "wc", "misr", "irf", "grd"],
                   "we": ["ndp", "wafd", "lib", "slp"], "sa": ["azh", "ij"], "nt": ["arm", "ye", "rcc", "mon"]}
OUTLOOK_OF_PARTY = {p: ok for ok, ps in OUTLOOK_PARTIES.items() for p in ps}
for f in FOCI:
    keep, xav = [], []
    for g in f["pre"]:
        same = [p for p in g if BYID[p]["sec"] == f["sec"]]
        other = [p for p in g if BYID[p]["sec"] != f["sec"]]
        linked = [p for p in other if p.startswith("EGY_1970_dir_")
                  or (f["sec"] in PARTY_SECS and BYID[p]["sec"] == OUTLOOK_OF_PARTY.get(f["sec"]))]
        if same or linked:
            keep.append(same + linked)  # links of the approved design: direction -> outlook, outlook in power -> party paths
        elif f["sec"] in PARTY_SECS or other == ["EGY_1970_shadow_of_the_naksa"]:
            pass  # party trees open with their party in power; shared branches start freely
        else:
            xav.append(other)
    f["pre"] = keep
    f["_xav"] = xav

ORDER_ALL = [f["id"] for f in FOCI]
PARTY_OF_SEC = {}
for k, s in SECT.items():
    m = re.search(r"\((\d+)\)$", s["title"])
    if m:
        PARTY_OF_SEC[k] = int(m.group(1))
for f in FOCI:
    if f["sec"] in PARTY_OF_SEC:
        f["_party"] = PARTY_OF_SEC[f["sec"]]
    rp = [e for e in f["eff"] if e.startswith("Regierungspartei → ")]
    if rp:
        f["_rp"] = E.PARTY_BY_NAME[re.match(r"^Regierungspartei → (.+?) `", rp[0]).group(1)]
        if "_party" not in f:
            f["_party"] = f["_rp"]

# every "Power to X" focus leads down to the path of its party (request 14 Oct 2026, evening):
# party root prerequisite = Power to X OR the outlook-in-power root (party reached power by elections or at start)
TRANSFER_OF = {}
for ok, ps in OUTLOOK_PARTIES.items():
    by_rp = {BYID[i]["_rp"]: i for i in [f["id"] for f in FOCI if f["sec"] == ok and f["id"] in STRONG]
             if BYID[i].get("_rp") is not None}
    for p in ps:
        TRANSFER_OF[p] = by_rp[PARTY_OF_SEC[p]]
for p, t in TRANSFER_OF.items():
    root = [f for f in FOCI if f["sec"] == p and f["pre"] and all(BYID[q]["sec"] != p for g in f["pre"] for q in g)]
    assert len(root) == 1, p
    root[0]["pre"] = [root[0]["pre"][0] + [t]]

TOOLTIPS = set()
for fn in os.listdir("/mnt/user-data/uploads/mdcoldwar/localisation/english"):
    p = "/mnt/user-data/uploads/mdcoldwar/localisation/english/" + fn
    if fn.endswith(".yml"):
        for line in open(p, encoding="utf-8-sig", errors="replace"):
            m = re.match(r"^\s+([\w.]+_tt):", line)
            if m:
                TOOLTIPS.add(m.group(1))
E.TOOLTIP_KEYS.update(TOOLTIPS)


# ------------------------------------------------------------ formatting
def block(lines, base=0):
    """indent a list of code lines by brace depth"""
    out, d = [], base
    for raw in "\n".join(lines).split("\n"):
        line = raw.strip()
        if not line:
            if out and out[-1] != "" and not out[-1].endswith("{"):
                out.append("")
            continue
        opens, closes = line.count("{"), line.count("}")
        if line.startswith("}"):
            d -= 1
            out.append("\t" * d + line)
            d += opens - (closes - 1)
        else:
            out.append("\t" * d + line)
            d += opens - closes
    assert d == base, ("unbalanced", lines[:3], d)
    return out


HEADER = ("# IMPERIA CW — Cold War: Egypt 1970 content generator.\n## COLDWAR | Cold War mod (MD Imperia) - Egypt 1970\n## Generated by the COLDWAR Egypt generator (cw_compile.py) from the approved design (project doc claude/mdcw_egy_1970_focus_tree_design.md). Edit the generator, not this file.\n## Search for 'COLDWAR' to find every Cold War addition.\n")


def write(path, text, bom=False):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    data = text.replace("\r\n", "\n")
    with open(full, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as fh:
        fh.write(data)


# ------------------------------------------------------------ effects per focus
def focus_effects(f):
    short = f["id"].replace("EGY_1970_", "")
    lines = [f'log = "[GetDateText]: [Root.GetName]: Focus {cid(f["id"])}"']
    for e in f["eff"]:
        if e.startswith("Event:"):
            if short in EVLINES:
                lines += EVLINES[short]
            else:
                R.unhandled.append((f["id"], e))
            continue
        if e.startswith("Bei ") and (short, e) not in MAN:
            R.unhandled.append((f["id"], e))
            continue
        lines += E.compile_line(e, f)
    if short == "the_heir_apparent" or short == "the_succession_question":
        pass
    if short == "reopen_the_suez_canal":
        # Revalidate the focus's control/war gate at delivery. Its own Authority
        # reward and 1% GDP cost remain separate from the decision's contract.
        lines = lines[:1] + [
            "if = {",
            "limit = { 214 = { is_controlled_by = ROOT } OR = { NOT = { has_war_with = ISR } 213 = { is_controlled_by = ROOT } } }",
            *lines[1:],
            "hidden_effect = { mdcw_suez_refund_reopening_project = yes mdcw_suez_reopen_historical_canal = yes }",
            "}",
        ]
    return lines


SEARCH = [
    (r"Partei|Regierungspartei|Outlook|Popularität|Wahlen|Staatschef|PP ", "FOCUS_FILTER_POLITICAL"),
    (r"Forschungsbonus|Forschung", "FOCUS_FILTER_RESEARCH"),
    (r"Gebäude|Fabrik|Industrie|Baugeschw|Stahl|Öl|Aluminium", "FOCUS_FILTER_INDUSTRY"),
    (r"Stabilität", "FOCUS_FILTER_STABILITY"),
    (r"Kriegsunterstützung", "FOCUS_FILTER_WAR_SUPPORT"),
    (r"_exact|Fraktion", "FOCUS_FILTER_INTERNAL_FACTION"),
    (r"Einfluss|Angebot|Meinung [A-Z]{3}", "FOCUS_FILTER_INFLUENCE"),
    (r"Korruption", "FOCUS_FILTER_CORRUPTION"),
    (r"budget|Steuersatz|Kosten [\d.]+ % BIP|Treasury|Schulden", "FOCUS_FILTER_EXPENDITURE"),
    (r"Rekrut|Streitkräfte|Organisation|Angriff|Erfahrung", "FOCUS_FILTER_MILITARY_LAWS"),
    (r"Ansprüche|annex|integriert", "FOCUS_FILTER_ANNEXATION"),
]


def search_filters(f):
    txt = " ".join(f["eff"])
    out = []
    for pat, fl in SEARCH:
        if re.search(pat, txt) and fl not in out:
            out.append(fl)
    return out[:4] or ["FOCUS_FILTER_POLITICAL"]


# ------------------------------------------------------------ icons / sprites
GOAL_SPRITES = {}
for n, p in json.load(open("goal_sprites.json")):
    GOAL_SPRITES.setdefault(p.lower(), n)
NEW_SPRITES = {}  # sprite name -> texture path


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


ICON_USE = collections.Counter()
BAN = re.compile(r"coldwar/Egyptian_army\.dds|/idea_[^/]*$|/GFX_idea", re.I)


def icon_of(f):
    pick = ICONS.get(f["id"])
    if not pick:
        return sprite_for("gfx/interface/goals/coldwar/focus_islam_egypt.dds") if "azh" in f["id"] else "egypt_flag"
    cands = [c for c in [pick["icon"]] + pick.get("alt", []) if not BAN.search(c)] or ["gfx/interface/goals/egypt/egyptian_republic.dds"]
    pick = dict(icon=cands[0])
    for cand in cands:
        if ICON_USE[cand] < 3:
            ICON_USE[cand] += 1
            return sprite_for(cand)
    ICON_USE[pick["icon"]] += 1
    return sprite_for(pick["icon"])


# ------------------------------------------------------------ layout
def tidy(ids):
    S = set(ids)
    par = {i: [p for g in BYID[i]["pre"] for p in g if p in S] for i in ids}
    y = {}

    def gy(i, stack=()):
        if i in y:
            return y[i]
        y[i] = 0 if not par[i] else max(gy(p) for p in par[i]) + 1
        return y[i]
    for i in ids:
        gy(i)
    prim = {i: (max(par[i], key=lambda p: y[p]) if par[i] else None) for i in ids}
    ch = {i: [] for i in ids}
    roots = []
    for i in ids:
        (ch[prim[i]] if prim[i] else roots).append(i)
    cnt = [0]
    X = {}

    def place(i):
        if not ch[i]:
            X[i] = cnt[0]
            cnt[0] += 1
        else:
            for c in ch[i]:
                place(c)
            X[i] = (X[ch[i][0]] + X[ch[i][-1]]) / 2
    for r in roots:
        place(r)
    pos = {i: (X[i], y[i]) for i in ids}
    return pos, cnt[0], (max(y.values()) + 1 if y else 0)


ORDER = [f["id"] for f in FOCI]


def secids(s):
    return [i for i in ORDER if BYID[i]["sec"] == s]


OUTLOOKS = [("na", ["asu", "tp", "mb", "tag", "fc", "nb", "fe", "fn"]), ("em", ["cop", "ecp", "wc", "misr", "irf", "grd"]),
            ("we", ["ndp", "wafd", "lib", "slp"]), ("sa", ["azh", "ij"]), ("nt", ["arm", "ye", "rcc", "mon"])]
SHARED = ["war", "arab", "pw", "eco", "nile", "ind", "mil"]
POS = {}


XS = 2  # one tidy column = 2 focus units, so names and icons never overlap


def refine(ids):
    """tidy tree, then row by row: put every focus at the mean x of its parents (merges sit
    centred under the foci they need), keeping at least XS units between neighbours."""
    if not ids:
        return {}, 0, 0
    p, w, h = tidy(ids)
    S = set(ids)
    X = {i: p[i][0] * XS for i in ids}
    Y = {i: p[i][1] for i in ids}
    par = {i: [q for g in BYID[i]["pre"] for q in g if q in S] for i in ids}
    for row in range(h):
        items = [i for i in ids if Y[i] == row]
        want = {i: (sum(X[q] for q in par[i]) / len(par[i]) if par[i] else X[i]) for i in items}
        items.sort(key=lambda i: (want[i], X[i]))
        pos, last = {}, None
        for i in items:
            x = round(want[i])
            if last is not None and x < last + XS:
                x = last + XS
            pos[i] = x
            last = x
        # shift the row back so that it is centred on what it wanted
        if items:
            shift = round(sum(want[i] - pos[i] for i in items) / len(items))
            for i in items:
                X[i] = pos[i] + shift
    # roots (row 0) sit centred above the foci that need them
    kids = {i: [k for k in ids if i in par[k]] for i in ids}
    items = [i for i in ids if Y[i] == 0]
    want = {i: (sum(X[k] for k in kids[i]) / len(kids[i]) if kids[i] else X[i]) for i in items}
    items.sort(key=lambda i: (want[i], X[i]))
    last = None
    for i in items:
        x = round(want[i])
        if last is not None and x < last + XS:
            x = last + XS
        X[i] = x
        last = x
    mn = min(X.values())
    for i in ids:
        X[i] -= mn
    return {i: (X[i], Y[i]) for i in ids}, max(X.values()) + XS, h


def place_block(ids, x0, y0):
    p, w, h = refine(ids)
    for i, (x, y) in p.items():
        POS[i] = (x0 + x, y + y0)
    return w, h


def block_size(ids):
    p, w, h = refine(ids)
    return w, h


GAPX, GAPY = 4, 3          # between trees
GAP_HEAD = 8               # between "strengthen the outlook" and "outlook in power" heads
GAP_GROUP = 12             # between two outlook groups in the same band


def outlook_group(ok, x0=None, y0=None):
    """Order of the approved visualisation, fully linked:
    direction focus -> strengthen roots -> head -> row of "Power to X" foci, each standing directly
    above the path of its party; between that row and the party paths the "outlook in power" root,
    which also opens every party path (elections, game start). Its own branch sits in the middle."""
    ids = secids(ok)
    parties = OUTLOOK_PARTIES[ok]
    trs = [TRANSFER_OF[p] for p in parties]
    top = [i for i in ids if i in STRONG and i not in trs]
    gv = [i for i in ids if i not in STRONG]
    root = [i for i in gv if not [p for g in BYID[i]["pre"] for p in g if p in gv]][0]
    rest = [i for i in gv if i != root]
    half = (len(parties) + 1) // 2
    order = parties[:half] + [None] + parties[half:]
    sub = [refine(rest if p is None else secids(p)) for p in order]
    hp, hw, hh = refine(top)
    bw = sum(w for _, w, _ in sub) + GAPX * (len(sub) - 1)
    W = max(hw, bw)
    ty = hh                       # row of the "Power to X" foci
    gy = ty + 2                   # row of the "outlook in power" root
    H = gy + 1 + max(h for _, _, h in sub)
    if x0 is None:
        return W, H
    px = x0 + (W - bw) // 2
    mid = None
    for p, (pp, w, h) in zip(order, sub):
        for i, (x, y) in pp.items():
            POS[i] = (px + x, y0 + gy + 1 + y)
        tops = [px + x for i, (x, y) in pp.items() if y == 0]
        if p is None:
            mid = round((min(tops) + max(tops)) / 2)
        else:
            r = [i for i, (x, y) in pp.items() if y == 0][0]
            POS[TRANSFER_OF[p]] = (POS[r][0], y0 + ty)
        px += w + GAPX
    POS[root] = (mid, y0 + gy)
    # roots and head centred over the "Power to X" row
    txs = [POS[t][0] for t in trs]
    c = round((min(txs) + max(txs)) / 2)
    hb = [i for i in top if hp[i][1] == hh - 1]
    shift = c - round(sum(hp[i][0] for i in hb) / len(hb))
    for i, (x, y) in hp.items():
        POS[i] = (x + shift, y0 + y)
    return W, H


OUTLOOK_ROW = ["na", "em", "we", "sa", "nt"]          # same order as the trunk's direction foci
LEFT_OF_TRUNK = ["war", "oct", "arab", "pw"]
RIGHT_OF_TRUNK = ["eco", "nile", "ind", "mil"]


def layout():
    starts = {}
    # top: trunk in the middle, shared branches left and right of it
    sizes = {s: block_size(secids(s)) for s in ["trunk"] + LEFT_OF_TRUNK + RIGHT_OF_TRUNK}
    grp = {ok: outlook_group(ok) for ok in OUTLOOK_ROW}
    row_w = sum(w for w, _ in grp.values()) + GAP_GROUP * (len(OUTLOOK_ROW) - 1)
    lw = sum(sizes[s][0] for s in LEFT_OF_TRUNK) + GAPX * len(LEFT_OF_TRUNK)
    rw = sum(sizes[s][0] for s in RIGHT_OF_TRUNK) + GAPX * len(RIGHT_OF_TRUNK)
    tx = max(lw, (row_w - sizes["trunk"][0]) // 2)
    x0 = max(0, lw - tx)                  # shift everything right if the left side would leave the canvas
    tx += x0
    place_block(secids("trunk"), tx, 0)
    starts["trunk"] = (tx, 0)
    x = tx
    for s in reversed(LEFT_OF_TRUNK):
        x -= sizes[s][0] + GAPX
        place_block(secids(s), x, 0)
        starts[s] = (x, 0)
    x = tx + sizes["trunk"][0] + GAPX
    for s in RIGHT_OF_TRUNK:
        place_block(secids(s), x, 0)
        starts[s] = (x, 0)
        x += sizes[s][0] + GAPX
    # below: the five outlook groups in a row, in direction order
    # Start the three gateway foci directly below the direction choices.
    y = max(POS[i][1] for i in secids("trunk") if i.startswith("EGY_1970_dir_")) + 1
    x = x0
    for ok in OUTLOOK_ROW:
        outlook_group(ok, x, y)
        starts[ok] = (x, y)
        x += grp[ok][0] + GAP_GROUP
    placed = set(POS)
    assert placed == {f["id"] for f in FOCI}, len({f["id"] for f in FOCI} - placed)
    return starts


STARTS = layout()
# anchors: first focus of each section
ANCHOR = {}
for s in SECT:
    ids = secids(s)
    if ids:
        ANCHOR[s] = min(ids, key=lambda i: (POS[i][1], POS[i][0]))

# overlap check
seen = {}
for i, p in POS.items():
    assert p not in seen, ("overlap", i, seen.get(p), p)
    seen[p] = i


# ------------------------------------------------------------ focus file
def ai_block(f):
    short = f["id"].replace("EGY_1970_", "")
    if short == "doctors_from_moscow":
        return ["ai_will_do = {", "base = 0", "}"]
    if f.get("hist"):
        return ["ai_will_do = {", "base = 10", "}"]
    return ["ai_will_do = {", "base = 3", "modifier = {", "factor = 0.1", "is_historical_focus_on = yes", "}", "}"]


def focus_text(f):
    fid = cid(f["id"])
    short = f["id"].replace("EGY_1970_", "")
    x, y = POS[f["id"]]
    anc = ANCHOR[f["sec"]]
    L = ["focus = {", f"id = {fid}", f"icon = {icon_of(f)}", ""]
    if anc == f["id"]:
        L += [f"x = {x}", f"y = {y}", ""]
    else:
        ax, ay = POS[anc]
        L += [f"x = {x - ax}", f"y = {y - ay}", f"relative_position_id = {cid(anc)}", ""]
    L += [f"cost = {fmt(f['cost'])}", ""]
    for g in f["pre"]:
        L.append("prerequisite = { " + " ".join(f"focus = {cid(p)}" for p in g) + " }")
    if f["mx"]:
        L.append("mutually_exclusive = { " + " ".join(f"focus = {cid(m)}" for m in f["mx"]) + " }")
    av = A.convert(f["av"], f.get("_rp"))
    if f.get("av_raw"):
        av = (av + "\n" + f["av_raw"]).strip()
    for g in f.get("_xav", []):
        cond = " ".join(f"has_completed_focus = {cid(p)}" for p in g)
        av = (av + "\n" + (cond if len(g) == 1 else f"OR = {{ {cond} }}")).strip()
    extra = A.EXTRA_AV.get(short, "")
    if av or extra:
        L += ["", "available = {"] + [l for l in (av + "\n" + extra).split("\n") if l.strip()] + ["}"]
    if f.get("_bypass"):
        L += ["", "bypass = {", f["_bypass"], "}"]
    L += ["", "search_filters = { " + " ".join(search_filters(f)) + " }", "", "completion_reward = {"]
    L += focus_effects(f)
    L += ["}", ""] + ai_block(f) + ["}"]
    return block(L, 1)


def focus_file():
    parts = [HEADER, "focus_tree = {", f"\tid = {TREE_ID}", "\tcountry = {", "\t\tfactor = 0", "\t\tmodifier = {",
             "\t\t\tadd = 30", "\t\t\toriginal_tag = EGY", "\t\t\tIMP_is_1970_scenario = yes", "\t\t}", "\t}",
             "\tdefault = no", "\treset_on_civilwar = no",
             f"\tcontinuous_focus_position = {{ x = {(max(POS[i][0] for s in RIGHT_OF_TRUNK for i in secids(s)) + 6) * 96} y = 150 }}",  # free space right of the top band
             f"\tinitial_show_position = {{ focus = {cid(ANCHOR['trunk'])} }}", ""]
    SHORTCUTS = [("trunk", "Revolution and Succession"), ("na", "Non-Aligned Outlook"), ("em", "Emerging Outlook"),
                 ("we", "Western Outlook"), ("sa", "Salafist Outlook"), ("nt", "Nationalist Outlook"),
                 ("war", "War and the Sinai"), ("oct", "The Road to October"), ("arab", "The Arab World"), ("pw", "The Superpowers"),
                 ("eco", "Economic Model"), ("nile", "The Nile and Agriculture"), ("ind", "Industry and Oil"), ("mil", "Armed Forces")]
    for ok, parties in OUTLOOK_PARTIES.items():
        for s in parties:
            SHORTCUTS.append((s, re.sub(r"^Partei: |\s*\(\d+\)$", "", SECT[s]["title"])))
    for k, t in SHORTCUTS:
        parts += ["\tshortcut = {", f"\t\tname = {PFX}shortcut_{k}", f"\t\ttarget = {cid(ANCHOR[k])}", "\t\tscroll_wheel_factor = 0.80", "\t}"]
        LOC[f"{PFX}shortcut_{k}"] = t
    parts.append("")
    for s in SECT:
        parts.append(f"\t### COLDWAR | {SECT[s]['title']} ###")
        for f in FOCI:
            if f["sec"] == s:
                parts += focus_text(f)
                parts.append("")
    parts.append("}")
    return "\n".join(parts) + "\n"


LOC = collections.OrderedDict()
