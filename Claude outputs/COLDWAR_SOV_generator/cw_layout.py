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


# ---------------------------------------------------------------- section layout (same algorithm as the design export)
VIRT = collections.defaultdict(int)   # parent id -> number of reserved empty columns among its children


def layout_section(key):
    nodes = [f for f in FOCI if f["sec"] == key]
    order = [n["id"] for n in nodes]
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
    # reserved empty columns: a parent with a line that runs down several rows gets an empty slot
    # in the middle of its children, so the line never crosses a focus (as in the design export)
    for p, n in VIRT.items():
        if p in children:
            for k in range(n):
                children[p].insert(len(children[p]) // 2, f"__virt__{p}_{k}")
    xs, slot = {}, [0]

    def place(i):
        ch = children.get(i, [])
        if not ch:
            xs[i] = slot[0]
            slot[0] += 1
        else:
            for c in ch:
                place(c)
            xs[i] = (xs[ch[0]] + xs[ch[-1]]) / 2
    for r in roots:
        place(r)
    pos = {i: (int(round(xs[i] * 2)), layer[i]) for i in order}   # 2 focus units per column
    w = (slot[0] - 1) * 2 + 2
    h = max(layer.values()) + 1
    return pos, w, h


SECGAP = 4      # x units between sections in a row
ROWGAP = 2      # free rows between rows of sections
GROUPGAP = 4    # free rows between groups
MAXW = 150      # wrap width of a group band
POS = {}
SEC_ORIGIN = {}
LAY = {k: layout_section(k) for k in ORDER}


def place_section(key, x0, y0):
    pos, w, h = LAY[key]
    for i, (x, y) in pos.items():
        POS[i] = (x0 + x, y0 + y)
    SEC_ORIGIN[key] = (x0, y0, w, h)


def place_row(keys, x0, y0, width=None):
    """keys in one row, centred in `width` if given; returns height"""
    rw = sum(LAY[k][1] for k in keys) + SECGAP * (len(keys) - 1)
    x = x0 + ((width - rw) // 2 if width and width > rw else 0)
    for k in keys:
        place_section(k, x, y0)
        x += LAY[k][1] + SECGAP
    return max(LAY[k][2] for k in keys)


def wrap(keys, maxw):
    rows, cur, w = [], [], 0
    for k in keys:
        kw = LAY[k][1]
        if cur and w + SECGAP + kw > maxw:
            rows.append(cur)
            cur, w = [], 0
        w = kw if not cur else w + SECGAP + kw
        cur.append(k)
    if cur:
        rows.append(cur)
    return rows


def row_width(keys):
    return sum(LAY[k][1] for k in keys) + SECGAP * (len(keys) - 1)


def group_rows(g):
    keys = [k for k in ORDER if SECT[k]["group"] == g]
    if g == "Politbüro & Outlooks":
        return [["pol"], [k for k in keys if k != "pol"]]
    if g == "KPdSU & Generalsekretäre":
        return [["cpsu", "ple"]] + wrap([k for k in keys if k not in ("cpsu", "ple")], MAXW)
    return wrap(keys, MAXW)


def layout():
    bands = [(g, group_rows(g)) for g in GROUPS]
    W = max(row_width(r) for _, rows in bands for r in rows)
    y = 0
    for g, rows in bands:
        for r in rows:
            h = place_row(r, 0, y, W)
            y += h + ROWGAP
        y += GROUPGAP - ROWGAP
    assert set(POS) == set(BYID)
    seen = {}
    for i, p in POS.items():
        assert p not in seen, ("overlap", i, seen[p])
        seen[p] = i
    return W, y


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
ANCHOR = {k: min((i for i in BYID if BYID[i]["sec"] == k), key=lambda i: (POS[i][1], POS[i][0])) for k in ORDER}


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


if __name__ == "__main__":
    print("canvas", WIDTH, "x", HEIGHT)
    for k in ORDER:
        print(k, SEC_ORIGIN[k])
    b = line_conflicts()
    print("line conflicts", len(b))
    print("  below parent:", sum(1 for x in b if x[3] == "below parent"), " above child:", sum(1 for x in b if x[3] == "above child"))
    for x in b[:30]:
        print(" ", [short(i) for i in x[:3]], x[3])
