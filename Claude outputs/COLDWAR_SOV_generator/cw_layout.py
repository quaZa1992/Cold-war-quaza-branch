# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Loads the approved design and lays the focus tree out on one canvas.
# Inside every section the layout is the same tidy tree as the design visualisation
# (soviet_union_1970_focus_tree.html); the sections keep the order of the visualisation's tabs.
import sys, json, collections
from cw_common import *

sys.path.insert(0, DESIGN)
import build_all  # noqa: F401  (registers every focus of the design)
import d_concept as CONCEPT
import d_republics as REPUBLICS
import sov_dsl as DSL
from sov_dsl import FOCI, SECTIONS, IDEAS, PROGS, OFFERS, EVENTS, DECISIONS, OPINIONS, TRAITS, PARTY, TRIG

BYID = {f["id"]: f for f in FOCI}
SECT = {s["key"]: s for s in SECTIONS}
ORDER = [s["key"] for s in SECTIONS]
GROUPS = []
for s in SECTIONS:
    if s["group"] not in GROUPS:
        GROUPS.append(s["group"])

DESC, ICONS = {}, {}
for g in range(1, 9):
    DESC.update(json.load(open(os.path.join(HERE, f"desc/out_{g}.json"))))
    ICONS.update(json.load(open(os.path.join(HERE, f"desc/icons_{g}.json"))))
assert set(DESC) == set(BYID) == set(ICONS), (len(DESC), len(BYID), len(ICONS))

# ---------------------------------------------------------------- effect audit (MD 2000 Russia norms, Imperia / Cold War hooks)
# overrides/<group>.json: per focus `set` (replace effect idx), `del`, `add`, `cost`, `available_add`;
# plus new ideas, tooltips and opinion modifiers. Applied before anything else reads the design.
NEW_LOC, OP_NAMES_NEW, AUDIT = {}, {}, {}
CANON_IDEA_NAMES = {f"{PFX}ni_window_society": "Policy Window: Our Society", f"{PFX}ni_window_economy": "Policy Window: Our Economy",
                    f"{PFX}ni_window_military": "Policy Window: Our Military"}
IDEA_HINT = {}
for _p in sorted(__import__("glob").glob(os.path.join(HERE, "overrides", "*.json"))):
    _o = json.load(open(_p, encoding="utf-8"))
    for fid, ov in _o["foci"].items():
        f = BYID[fid]
        AUDIT[fid] = ov
        if ov.get("verdict") != "fix":
            continue
        effs = list(f["eff"])
        for s in ov.get("set", []):
            effs[s["idx"]] = s["e"]
        dels = set(ov.get("del", []))
        f["eff"] = [e for n, e in enumerate(effs) if n not in dels] + list(ov.get("add", []))
        if "cost" in ov:
            f["cost"] = ov["cost"]
        f["_av_add"] = list(ov.get("available_add", []))
    for iid, d in _o.get("new_ideas", {}).items():
        new = dict(name=CANON_IDEA_NAMES.get(iid, d["name"]), mods=dict(d["mods"]), days=d.get("days"))
        if iid in IDEAS:
            assert IDEAS[iid]["mods"] == new["mods"], (iid, _p)
            continue
        IDEAS[iid] = new
        IDEA_HINT[iid] = d.get("picture_hint", "")
    for k, v in _o.get("new_loc", {}).items():
        NEW_LOC.setdefault(k, v)
    for k, v in _o.get("new_opinions", {}).items():
        if k not in OPINIONS:
            OPINIONS[k] = (v["value"], False)
            OP_NAMES_NEW[k] = v["name"]

# policy windows: one wording for every tooltip. The idea halves the cost of its whole pool (imp_national_ideas_N_cost_factor),
# not only of the national idea the focus names (pools checked against mdcw_imperia_national_ideas_* / mdcw_cold_war_national_ideas).
NI_WINDOW_TT = {"natality": ("Natality Campaigns", "Our Society"), "censorship": ("Censorship Bureaus", "Our Society"),
                "broadcasting": ("International Broadcasting Service", "Our Society"), "patriotic_education": ("Patriotic Education", "Our Society"),
                "mass_surveillance": ("Mass Surveillance", "Our Society"), "youth_service": ("Mandatory Youth Service", "Our Society"),
                "border_regime": ("Border Regime and Exit Controls", "Our Society"),
                "labour_mobilization": ("National Labour Mobilization", "Our Economy"), "worker_cooperatives": ("Worker Co-operatives", "Our Economy"),
                "import_substitution": ("Import Substitution Industrialisation", "Our Economy"),
                "development_agency": ("International Development Agency", "Our Economy"),
                "military_parades": ("Military Parades", "Our Military"), "civil_militia": ("Civil Militia", "Our Military"),
                "maritime_hub": ("Maritime Industry Hub", "Our Military"), "military_advisers": ("Military Advisers Abroad", "Our Military")}
for _k, (_idea, _pool) in NI_WINDOW_TT.items():
    if f"{PFX}ni_window_{_k}_tt" in NEW_LOC:
        NEW_LOC[f"{PFX}ni_window_{_k}_tt"] = (f"For one year, national ideas of the §Y{_pool}§! pool (Government screen), such as §Y{_idea}§!, "
                                              f"cost §G50%§! less political power.")

# MD 2000 Russia gives political power in only 9 % of its foci: where a focus already has two or more other rewards,
# its political power is halved (rounded to 5, at least 25), so PP stays a seasoning and not the main reward.
PP_SCALED = 0
for _f in FOCI:
    _other = [e for e in _f["eff"] if e["k"] not in ("pp", "note", "custom", "flag", "decision", "event", "heir")]
    if len(_other) >= 2:
        for _e in _f["eff"]:
            if _e["k"] == "pp" and _e["v"] > 25:
                _e["v"] = max(25, int(round(_e["v"] * 0.5 / 5.0)) * 5)
                PP_SCALED += 1

# ---------------------------------------------------------------- fixes from the independent review of the audited tree
def _f(sid):
    return BYID[PFX + sid]


def _drop(sid, pred):
    _f(sid)["eff"] = [e for e in _f(sid)["eff"] if not pred(e)]


# one step of space-programme progress per focus, 0.10 each, so the Moon path stays below 1.0 before Energia-Buran
for _x in FOCI:
    _sp = [e for e in _x["eff"] if e["k"] == "space" or (e["k"] == "sp" and e["project"] == "sp_space_program")]
    if _sp:
        _x["eff"] = [e for e in _x["eff"] if e not in _sp]
        _x["eff"].append(dict(k="sp", project="sp_space_program", v=0.25 if any(e.get("v") == 0.25 for e in _sp) else 0.10))
# Semichastny never takes over (Shelepin does not die): the designation stays flavour, the dead flag goes
_drop("kv_heir_semichastny", lambda e: e["k"] == "flag")
_f("kv_heir_semichastny")["eff"].insert(0, dict(k="raw", code=[f"custom_effect_tooltip = {PFX}semichastny_heir_tt"]))
NEW_LOC[f"{PFX}semichastny_heir_tt"] = "§YVladimir Semichastny§!, former KGB chairman, is named the second man of the Komsomol line."
# the outlook helper already strengthens the CPSU when it rules
_drop("dir_the_leading_role", lambda e: e["k"] == "party" and e["i"] == 4)
# austerity is not income
_drop("tighten_the_belts", lambda e: e["k"] in ("gdp_gain", "ws"))
_f("tighten_the_belts")["eff"].append(dict(k="dyn", g="gosplan", mods={"consumer_goods_factor": -0.02}))
# the drought focus is a hub, not an agricultural bonus
_drop("the_harvest_of_1972", lambda e: e["k"] in ("dyn", "fac"))
for _e in _f("the_harvest_of_1972")["eff"]:
    if _e["k"] == "pp":
        _e["v"] = 25
# refusing to intervene does not raise war support
_drop("no_soviet_soldier", lambda e: e["k"] == "ws")
# offers give no advance reward: the money comes with each republic that accepts (event COLDWAR_SOV.60)
for _s in ("nts_a_russian_federation", "chr_the_right_of_secession", "lnl_release_the_republics"):
    _drop(_s, lambda e: e["k"] == "gdp_gain")
# payment only where something is built
_drop("the_amur_fortified_districts", lambda e: e["k"] == "gdp")
_drop("civil_defence_of_the_ussr", lambda e: e["k"] == "gdp" or (e["k"] == "raw" and "civilian_shelter" in " ".join(e["code"])))
_f("civil_defence_of_the_ussr")["eff"].append(dict(k="raw", code=[
    "if = {", "limit = { capital_scope = { free_building_slots = { building = civilian_shelter size > 1 } } }",
    "capital_scope = { add_building_construction = { type = civilian_shelter level = 2 instant_build = yes } }",
    f"set_temp_variable = {{ {PFX}gdp_share = 0.003 }}", f"{PFX}pay_gdp_share = yes", "}",
    f"custom_effect_tooltip = {PFX}shelters_tt"]))
# a candidacy only opens a decision: cheap gate like MD's entry foci
for _k in ("kos", "pod", "sus", "she", "and", "gre", "ust", "gro", "che", "gor"):
    _f(f"ple_{_k}")["cost"] = 2
# the human-subject guard of the bloc change lives in the generator (cw_effects.cw_join)
for _s in ("nts_into_the_west", "chr_join_the_free_world"):
    for _n, _e in enumerate(_f(_s)["eff"]):
        if _e["k"] == "raw" and "mdcw_cw_change_alignment" in " ".join(_e["code"]):
            _f(_s)["eff"][_n] = dict(k="cwjoin", al="west")

OUTLOOK_SECS = {"em", "we", "na", "nt"}
LEADER_SECS = {"bre", "kos", "pod", "sus", "she", "and", "gre", "ust", "gro", "che", "gor"}
PARTY_SECS = {s["key"] for s in SECTIONS if s["group"] == "Parteien"} | {"cpsu"}

# ---------------------------------------------------------------- links: lines only inside a section and
# trunk direction -> outlook block (as in the visualisation). Everything else becomes `available`.
for f in FOCI:
    keep, xav = [], []
    for g in f["pre"]:
        same = [p for p in g if BYID[p]["sec"] == f["sec"]]
        other = [p for p in g if BYID[p]["sec"] != f["sec"]]
        if not other:
            keep.append(g)
            continue
        if f["sec"] in OUTLOOK_SECS and all(BYID[p]["sec"] == "pol" for p in other):
            keep.append(g)  # direction focus -> outlook block: the line of the design
            continue
        assert not same, f["id"]
        if f["sec"] in LEADER_SECS and all(p.startswith(PFX + "ple_") and p != PFX + "ple_the_politburo" for p in other):
            continue  # a General Secretary's tree opens with his flag, however he came to power
        xav.append(other)
    f["pre"] = keep
    f["_xav"] = xav


# ---------------------------------------------------------------- section layout (MD 2000 Russia positioning rules)
# Probe of 05_russia.txt (audit/probe2/md_layout_probe.md): a parent stands over the middle of its first and last child,
# a single child straight below its parent, and sub-trees are packed by their row contour: the nearest foci of two
# neighbouring sub-trees are 2 columns apart and a deep sub-tree may run on under a shallow neighbour.
VIRT = collections.defaultdict(int)   # parent id -> reserved empty column under the parent (its line runs down several rows)
GAP = 2           # free columns between foci of neighbouring sub-trees, sections and sub-blocks (MD: 2)
BLOCK_GAP = 4     # between the main blocks: politics | Politburo | economy | military | state | foreign (MD: 2-5)
OUTLOOK_GAP = 4   # between two outlook groups (each one hangs from its own direction focus)
MIRROR = {"pol"}  # the trunk keeps the design order and is mirrored, so whither_the_union (and its bar) faces the outlooks


# row contours: row -> [focus_lo, focus_hi, line_lo, line_hi] (None = nothing of that kind in the row)
def _c_add(C, row, lo, hi, kind=0):
    e = C.setdefault(row, [None, None, None, None])
    k = 2 * kind
    e[k] = lo if e[k] is None else min(e[k], lo)
    e[k + 1] = hi if e[k + 1] is None else max(e[k + 1], hi)


def _c_merge(A, B, dx=0):
    for r, e in B.items():
        for kind in (0, 1):
            if e[2 * kind] is not None:
                _c_add(A, r, e[2 * kind] + dx, e[2 * kind + 1] + dx, kind)


def _c_offset(A, B, gap):
    """smallest shift of B so that, in every shared row, its foci stay `gap` columns right of A's foci (lines: 1 column)"""
    off = None
    for r, eb in B.items():
        ea = A.get(r)
        if not ea:
            continue
        for ka in (0, 1):
            for kb in (0, 1):
                if ea[2 * ka] is None or eb[2 * kb] is None:
                    continue
                need = ea[2 * ka + 1] + (gap if ka == kb == 0 else 1) - eb[2 * kb]
                off = need if off is None else max(off, need)
    return off


def _tree(key, skip=()):
    order = [f["id"] for f in FOCI if f["sec"] == key and f["id"] not in skip]
    ids = set(order)
    layer = {}

    def L(fid):
        if fid in layer:
            return layer[fid]
        ps = [p for g in BYID[fid]["pre"] for p in g if p in ids]
        layer[fid] = 0 if not ps else 1 + max(L(p) for p in ps)
        return layer[fid]
    for i in order:
        L(i)
    children = {i: [] for i in order}
    roots = []
    for i in order:
        ps = [p for g in BYID[i]["pre"] for p in g if p in ids]
        if ps:
            prim = max(ps, key=lambda p: (layer[p], -order.index(p)))
            children[prim].append(i)
        else:
            roots.append(i)
    return order, layer, children, roots


def layout_section(key, skip=()):
    """contour tidy tree of one section; returns local positions (x >= 0, y = layer), width (+2 margin) and height"""
    order, layer, children, roots = _tree(key, skip)
    ids = set(order)
    low = collections.defaultdict(int)          # deepest row a line of this parent ends in
    for i in order:
        for g in BYID[i]["pre"]:
            for p in g:
                if p in ids:
                    low[p] = max(low[p], layer[i])

    def place(i):
        items = list(children[i])
        if VIRT[i]:      # reserved column: the parent's line runs down several rows, nothing may stand under it
            items.insert(len(items) // 2, None)
        if not items:
            C = {}
            _c_add(C, layer[i], 0, 0)
            return {i: 0}, C
        sub = {}
        for c in items:
            if c is None:
                Cv = {}
                for r in range(layer[i] + 1, max(low[i], layer[i] + 1)):
                    _c_add(Cv, r, 0, 0, 1)
                sub[None] = ({}, Cv)
            else:
                sub[c] = place(c)
        # MD keeps a story column upright: the sibling order (or its mirror, which keeps mutually exclusive partners
        # side by side) is chosen so the sub-tree stays narrow and its deepest foci stay under the parent
        best = None
        for seq in ((items,) if key in MIRROR else (items, items[::-1])):
            res = combine(i, seq, sub)
            pos, C = res
            fx = [C[r] for r in C if C[r][0] is not None]
            wdt = max(e[1] for e in fx) - min(e[0] for e in fx)
            deep = max(layer[f_] for f_ in pos)
            drift = abs(sum(x for f_, x in pos.items() if layer[f_] == deep))
            key_ = (wdt, drift)
            if best is None or key_ < best[0]:
                best = (key_, res)
        return best[1]

    def combine(i, items, sub):
        pos, C, xs, vx = {}, {}, [], None
        for n, c in enumerate(items):
            pc, Cc = sub[c]
            if not xs:
                off = 0
            else:
                off = _c_offset(C, Cc, GAP)
                step = 1 if (c is None or items[n - 1] is None) else GAP
                off = max(off if off is not None else xs[-1] + step, xs[-1] + step)
                if n == len(items) - 1 and c is not None and (xs[0] + off) % 2 and None not in items:
                    off += 1      # first and last child an even distance apart: the parent stands exactly in the middle
            for f_, x in pc.items():
                pos[f_] = x + off
            _c_merge(C, Cc, off)
            xs.append(off)
            if c is None:
                vx = off
        px = vx if vx is not None else (xs[0] + xs[-1]) // 2
        pos = {f_: x - px for f_, x in pos.items()}
        C2 = {}
        _c_merge(C2, C, -px)
        pos[i] = 0
        _c_add(C2, layer[i], 0, 0)
        return pos, C2
    allpos, C = {}, {}
    for r in roots:
        p, Cr = place(r)
        off = 0 if not C else _c_offset(C, Cr, GAP)
        if off is None:
            off = max(e[1] for e in C.values() if e[1] is not None) + GAP - min(p.values())
        for f_, x in p.items():
            allpos[f_] = x + off
        _c_merge(C, Cr, off)
    pos = {i: (allpos[i], layer[i]) for i in order}
    _settle(pos)
    mn = min(x for x, _ in pos.values())
    pos = {i: (x - mn, y) for i, (x, y) in pos.items()}
    return pos, max(x for x, _ in pos.values()) + 2, max(layer.values()) + 1


def _line_hits(pos, pairs):
    occ = set(pos.values())
    n = 0
    for p, c in pairs:
        (px, py), (cx, cy) = pos[p], pos[c]
        for y in range(py + 1, cy):
            n += ((px, y) in occ) + ((cx, y) in occ)
    return n


def _settle(pos):
    """inside a section: a child several rows below one of its parents stands 1-3 columns aside, so the line drops down a
    free column (MD practice); it keeps 2 columns to the other foci of its row and never jumps over one"""
    kids = collections.defaultdict(list)
    for i in pos:
        for g in BYID[i]["pre"]:
            for p in g:
                if p in pos:
                    kids[p].append(i)

    def into(c):
        return [(p, c) for g in BYID[c]["pre"] for p in g if p in pos]
    for _ in range(4):
        bad = sorted((c for c in pos if _line_hits(pos, into(c))), key=lambda i: pos[i][1])
        moved = False
        for c in bad:
            pairs = into(c) + [(c, k) for k in kids[c]]
            before = _line_hits(pos, pairs)
            if not before:
                continue
            x0, y0 = pos[c]
            taken = set(pos.values())
            best = None
            for dx in (1, -1, 2, -2, 3, -3):
                if any((x0 + dx + d, y0) in taken and d + dx != 0 for d in (-1, 0, 1)):
                    continue
                pos[c] = (x0 + dx, y0)
                n = _line_hits(pos, pairs)
                pos[c] = (x0, y0)
                if n < before and (best is None or n < best[0]):
                    best = (n, dx)
            if best:
                pos[c] = (x0 + best[1], y0)
                moved = True
        if not moved:
            return


POS = {}
SEC_ORIGIN = {}
LAY = {k: layout_section(k) for k in ORDER}


# ---------------------------------------------------------------- MD 2000 style canvas: wide and shallow, blocks side by side
#   politics: the trunk `pol` (whither_the_union) hangs the four direction foci on one long bar, each direction heads its
#             outlook group; the outlook's power foci form the hinge row and every party tree hangs straight below its
#             power focus, side by side (MD: Yeltsin -> party leaders, Westernism's convention -> party columns)
#   Politburo: ple_the_politburo hangs the candidacies on one long bar; every General Secretary tree stands straight below
#             his candidacy, side by side (Brezhnev straight below the Politburo, his line of the design)
#   economy | military | state | foreign: every section root at row 0, side by side (MD: military reform | security | PMC)
OPP = [("nt", ["rp", "cnr", "com", "rom"]), ("na", ["gt", "lnl", "rd", "fel", "fob", "smc", "usr"]),
       ("we", ["sd", "nts", "chr", "uds"]), ("em", ["cpsu", "wc", "ns", "kv"])]
GS_T1 = ["kos", "pod", "sus", "she", "bre"]              # the 1970 Politburo, Brezhnev in the middle of the row ...
GS_T2 = ["and", "gre", "ust", "gro", "che", "gor"]       # ... the men who enter it 1973-1980 to his right (same row)
# ple_the_politburo stands straight above Brezhnev, so its bar to the candidacies runs about half each way (MD: Yeltsin 0.46)
DOMAINS = [("economy", ["eco", "agr", "en", "sci"]), ("military", ["army", "str", "navy"]),
           ("state_union", ["union", "kgb", "soc"]), ("foreign", ["bloc", "det", "chi", "tw"])]
BLOCK_X, BLOCK_BOTTOM = {}, {}
TRUNK_SKIP = {f["id"] for f in FOCI if f["sec"] == "pol" and short(f["id"]).startswith("dir_")}
DIR_ROW = max(LAY["pol"][0][PFX + "whither_the_union"][1] + 1, 1)   # one row below whither_the_union
HINGE = DIR_ROW + 3          # direction -> outlook tops -> merge focus -> power foci (hinge row) -> party roots


def _w(k):
    return LAY[k][1]


def _h(k):
    return LAY[k][2]


def _local(k, lay=None):
    pos, w, h = lay or LAY[k]
    return {i: ((w - 2 - x) if k in MIRROR else x, y) for i, (x, y) in pos.items()}


def _root(k):
    r = [i for i, (x, y) in LAY[k][0].items() if not any(p in LAY[k][0] for g in BYID[i]["pre"] for p in g)]
    assert len(r) == 1, (k, r)
    return r[0]


def _hang(k, x, y):
    """positions of section k with its root at (x, y)"""
    pos = _local(k)
    rx, ry = pos[_root(k)]
    return {i: (x + px - rx, y + py - ry) for i, (px, py) in pos.items()}


def _contour(pts):
    """row contour of placed foci plus their prerequisite lines (incl. the _xav groups that get a line below)"""
    C = {}
    for i, (x, y) in pts.items():
        _c_add(C, y, x, x)
    for i in pts:
        for g in BYID[i]["pre"] + BYID[i]["_xav"]:
            if not all(p in pts for p in g):
                continue
            for p in g:
                (px, py), (cx, cy) = pts[p], pts[i]
                _c_add(C, py + 1, min(px, cx), max(px, cx), 1)        # the bar under the parent ...
                _c_add(C, cy, min(px, cx), max(px, cx), 1)            # ... or above the child
                for y in range(py + 1, cy):
                    _c_add(C, y, px, px, 1)
                    _c_add(C, y, cx, cx, 1)
    return C


def _pack(parts, gap, x0=0):
    """places the parts (dicts id -> (x, y)) left to right, each as far left as its row contour allows"""
    C, out, prev = {}, {}, None
    for pts in parts:
        Cp = _contour(pts)
        lo = min(x for x, _ in pts.values())
        if not C:
            off = x0 - lo
        else:
            off = _c_offset(C, Cp, gap)
            if off is None:
                off = max(e[1] for e in C.values() if e[1] is not None) + gap - lo
            off = max(off, prev + 1 - lo)      # never left of the previous part: no part slides under another one
        for i, (x, y) in pts.items():
            out[i] = (x + off, y)
        _c_merge(C, Cp, off)
        prev = lo + off
    return out


def _outlook_group(ok, parties):
    """direction focus -> outlook tops -> merge focus -> power foci (hinge row); party trees straight below their power
    focus; the outlook's second root (government already in power) closes the hinge row on the right"""
    ids = [f["id"] for f in FOCI if f["sec"] == ok]
    power = [i for i in ids if short(i).startswith("power_")]
    merge = {p for i in power for g in BYID[i]["pre"] for p in g}
    assert len(merge) == 1, ok
    merge = merge.pop()
    tops = sorted({p for g in BYID[merge]["pre"] for p in g}, key=lambda i: LAY[ok][0][i][0])
    dirf = {p for t in tops for g in BYID[t]["pre"] for p in g}
    assert len(dirf) == 1 and BYID[next(iter(dirf))]["sec"] == "pol", ok
    dirf = dirf.pop()
    second = [i for i in ids if not BYID[i]["pre"]]
    assert len(second) == 1, ok
    second = second[0]
    sub = {second}
    for i in ids:                                  # ids are in design order: parents first
        if any(p in sub for g in BYID[i]["pre"] for p in g):
            sub.add(i)
    assert set(ids) == set(tops) | {merge} | set(power) | sub, ok
    owner = {}
    for k in parties:
        g = BYID[_root(k)]["_xav"] + BYID[_root(k)]["pre"]     # (pre: layout() run again after the links were drawn)
        hit = [p for gg in g for p in gg if p in power]
        assert len(hit) == 1, (k, hit)
        owner[hit[0]] = k
    parts = []
    for p in sorted(power, key=lambda i: LAY[ok][0][i][0]):
        part = _hang(owner[p], 0, HINGE + 1)
        part[p] = (0, HINGE)
        parts.append(part)
    sp = LAY[ok][0]
    parts.append({i: (sp[i][0] - sp[second][0], HINGE + sp[i][1] - sp[second][1]) for i in sub})
    pts = _pack(parts, GAP)
    xs = sorted(pts[p][0] for p in power)
    mx = (xs[0] + xs[-1]) // 2
    pts[merge] = (mx, HINGE - 1)
    for n, t in enumerate(tops):
        pts[t] = (mx + 2 * n - (len(tops) - 1), HINGE - 2)
    pts[dirf] = (mx, DIR_ROW)
    return pts


def _trunk():
    """the trunk without its direction foci, mirrored so whither_the_union faces the outlook groups; whither stands at
    least 2 columns left of every trunk focus below it, so its long bar to the directions never runs into the bar of
    the doctrine branch (both hang at the same height)"""
    lay = layout_section("pol", TRUNK_SKIP)
    pos = _local("pol", lay)
    wt = PFX + "whither_the_union"
    wx, wy = pos[wt]
    if any(x < wx for i, (x, y) in pos.items() if y >= wy and i != wt):
        pos = {i: (lay[1] - 2 - x, y) for i, (x, y) in pos.items()}      # undo the mirror: whither already faces left
        wx, wy = pos[wt]
    lim = min(x for i, (x, y) in pos.items() if y >= wy and i != wt) - 2
    pos[wt] = (min(wx, lim), wy)
    return pos


BLOCK_IDS = {}


def _boxes():
    """block extents (x0, x1 incl. the 2-column margin), block bottoms and section boxes (x, y, w, h) from POS"""
    for name, b in BLOCK_IDS.items():
        xs = [POS[i][0] for i in b]
        BLOCK_X[name] = (min(xs), max(xs) + 2)
        BLOCK_BOTTOM[name] = max(POS[i][1] for i in b)
    for k in ORDER:
        pts = [POS[i] for i in POS if BYID[i]["sec"] == k]
        x0, y0 = min(x for x, _ in pts), min(y for _, y in pts)
        SEC_ORIGIN[k] = (x0, y0, max(x for x, _ in pts) - x0 + 2, max(y for _, y in pts) - y0 + 1)


def layout():
    blocks = []
    # politics: outlook groups left to right, the trunk right of them (next to the Politburo, MD: trunk | ruling party)
    groups = [_outlook_group(ok, ks) for ok, ks in OPP]
    pol = _pack(groups, OUTLOOK_GAP)
    pol = _pack([pol, _trunk()], OUTLOOK_GAP)
    blocks.append(("outlooks_parties", pol))
    # Politburo: candidacies on one bar, each General Secretary tree straight below his candidacy
    parts = []
    for k in GS_T1 + GS_T2:
        part = _hang(k, 0, 2)
        if k != "bre":
            part[PFX + "ple_" + k] = (0, 1)
        parts.append(part)
    gs = _pack(parts, GAP)
    gs[PFX + "ple_the_politburo"] = (gs[_root("bre")][0], 0)
    blocks.append(("cpsu_politburo_gs", gs))
    for name, keys in DOMAINS:
        blocks.append((name, _pack([_hang(k, 0, 0) for k in keys], GAP)))
    allpts = _pack([b for _, b in blocks], BLOCK_GAP)
    POS.clear()
    POS.update(allpts)
    for name, b in blocks:
        BLOCK_IDS[name] = set(b)
    _boxes()
    assert set(POS) == set(BYID), set(BYID) ^ set(POS)
    seen = {}
    for i, p in POS.items():
        assert p not in seen, ("overlap", i, seen[p])
        seen[p] = i
    return max(x for x, _ in POS.values()) + 1, max(y for _, y in POS.values()) + 1


def section_conflicts(key):
    pos = LAY[key][0]
    occ = {p: i for i, p in pos.items()}
    bad = []
    for i, (cx, cy) in pos.items():
        for g in BYID[i]["pre"]:
            for p in g:
                if p not in pos:
                    continue
                px, py = pos[p]
                for y in range(py + 1, cy):
                    if (px, y) in occ:
                        bad.append(p)
    return bad


for _ in range(12):
    changed = False
    for k in ORDER:
        for p in set(section_conflicts(k)):
            if VIRT[p] < 2:
                VIRT[p] += 1
                changed = True
    if not changed:
        break
    LAY = {k: layout_section(k) for k in ORDER}

WIDTH, HEIGHT = layout()
MOVED = None   # set below, after line_conflicts() is defined
ANCHOR = {k: min((i for i in BYID if BYID[i]["sec"] == k), key=lambda i: (POS[i][1], POS[i][0])) for k in ORDER}


def link_cross_prerequisites():
    """MD hangs every block from its hinge with a real line. A section root whose cross-section prerequisite group (`_xav`,
    written as `available = { has_completed_focus }`) now stands in the row straight above it - or straight above it in the
    same column - gets that group back as a prerequisite line: the same condition, now drawn. Only where the new lines
    cross no focus."""
    occ = set(POS.values())
    n = 0
    for f in FOCI:
        if f["pre"] or not f["_xav"]:
            continue
        cx, cy = POS[f["id"]]
        keep = []
        for g in f["_xav"]:
            above = [p for p in g if POS[p][0] == cx and POS[p][1] < cy]
            ok = above and all(POS[p][1] == cy - 1 or (POS[p][0] == cx and POS[p][1] < cy) for p in g)
            for p in g if ok else ():
                px, py = POS[p]
                if any((px, y) in occ or (cx, y) in occ for y in range(py + 1, cy)):
                    ok = False
            if ok:
                f["pre"].append(g)
                n += 1
            else:
                keep.append(g)
        f["_xav"] = keep
    return n


XAV_LINKED = link_cross_prerequisites()


def _conflicts_of(fid):
    """conflicts of the lines that end in fid or start in fid (both HOI4 drawing sides)"""
    occ = {p: i for i, p in POS.items()}
    bad = 0
    f = BYID[fid]
    pairs = [(p, fid) for g in f["pre"] for p in g] + [(fid, c["id"]) for c in CHILDREN.get(fid, [])]
    for p, c in pairs:
        px, py = POS[p]
        cx, cy = POS[c]
        for y in range(py + 1, cy):
            bad += ((px, y) in occ) + ((cx, y) in occ)
    return bad


def fix_child_columns():
    """a child several rows below one of its parents gets a free column: the line bends under the parent and drops
    down the child's column (MD practice), so the child moves one column aside instead of sitting under a chain"""
    moved = 0
    for _ in range(4):
        bad = {c for p, c, o, side in line_conflicts()}
        if not bad:
            break
        for c in sorted(bad, key=lambda i: POS[i][1]):
            before = _conflicts_of(c)
            if not before:
                continue
            x0, y0 = POS[c]
            taken = set(POS.values())
            best = None
            for dx in (1, -1, 2, -2, 3, -3):
                # never closer than 2 columns to another focus of the row (MD: no two foci of a row are 1 column apart)
                if any((x0 + dx + d, y0) in taken and (x0 + dx + d, y0) != (x0, y0) for d in (-1, 0, 1)):
                    continue
                POS[c] = (x0 + dx, y0)
                n = _conflicts_of(c)
                POS[c] = (x0, y0)
                if n < before and (best is None or n < best[0]):
                    best = (n, dx)
            if best:
                POS[c] = (x0 + best[1], y0)
                moved += 1
    return moved


CHILDREN = collections.defaultdict(list)
for _f in FOCI:
    for _g in _f["pre"]:
        for _p in _g:
            CHILDREN[_p].append(_f)


def line_conflicts():
    """foci standing in the column of a multi-row line (HOI4 draws it below the parent or above the child)"""
    occ = {p: i for i, p in POS.items()}
    bad = []
    for f in FOCI:
        cx, cy = POS[f["id"]]
        for g in f["pre"]:
            for p in g:
                px, py = POS[p]
                for y in range(py + 1, cy):
                    for x, side in ((px, "below parent"), (cx, "above child")):
                        if (x, y) in occ:
                            bad.append((p, f["id"], occ[(x, y)], side))
    return bad


MOVED = fix_child_columns()
_boxes()
ANCHOR = {k: min((i for i in BYID if BYID[i]["sec"] == k), key=lambda i: (POS[i][1], POS[i][0])) for k in ORDER}
WIDTH, HEIGHT = max(x for x, _ in POS.values()) + 1, max(y for _, y in POS.values()) + 1

if __name__ == "__main__":
    print("canvas", WIDTH, "x", HEIGHT, " cross-section links drawn as lines:", XAV_LINKED, " children moved aside:", MOVED)
    for name, (a, b) in BLOCK_X.items():
        print(f"  block {name:18s} x {a}-{b} bottom {BLOCK_BOTTOM[name]}")
    for k in ORDER:
        print(" ", k, SEC_ORIGIN[k])
    b = line_conflicts()
    print("line conflicts", len(b))
    print("  below parent:", sum(1 for x in b if x[3] == "below parent"), " above child:", sum(1 for x in b if x[3] == "above child"))
    for x in b[:30]:
        print(" ", [short(i) for i in x[:3]], x[3])
