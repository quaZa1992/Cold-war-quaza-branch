# IMPERIA CW — Cold War: probe2 — cw probe.
"""Measures OUR tree with the same positioning metrics as md_probe.py. Usage: SB=<sandbox> python3 cw_probe.py <label> -> cw_probe_<label>.json"""
import sys, os, json, collections, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cw_load_sb as C
L = C.L
P = {f['id']: (f['ax'], f['ay']) for f in C.F}          # positions as written in the focus file (relative ids resolved)
assert all(P[i] == tuple(map(float, L.POS[i])) for i in P), "file and cw_layout.POS disagree"
SEC = C.SEC
out = {}
W = max(x for x, y in P.values()) + 1; Hh = max(y for x, y in P.values()) + 1
out['canvas'] = dict(w=W, h=Hh, aspect_px=round(W * 96 / (Hh * 130), 2), fill=round(len(P) / (W * Hh), 3))
print(f"canvas {W:.0f} x {Hh:.0f}  aspect {out['canvas']['aspect_px']}:1  fill {out['canvas']['fill']}")
# lines
E = [(p, f['id'], len(g)) for f in C.F for g in f['pre'] for p in g]
dxs = [abs(P[c][0] - P[p][0]) for p, c, k in E]; dys = [P[c][1] - P[p][1] for p, c, k in E]
out['lines'] = dict(n=len(E), dy1=sum(d == 1 for d in dys), dx_le2=sum(d <= 2 for d in dxs), dx_ge6=sum(d >= 6 for d in dxs),
                    dx_ge20=sum(d >= 20 for d in dxs), max_dx=max(dxs), cross_section=sum(SEC[p] != SEC[c] for p, c, k in E),
                    or_groups=sum(1 for f in C.F for g in f['pre'] if len(g) > 1))
print("lines", out['lines'])
# roots (no prerequisite) and their placement
roots = [f['id'] for f in C.F if not f['pre']]
row0 = [r for r in roots if P[r][1] == 0]
fl = []
for r in roots:
    if P[r][1] == 0: continue
    f = L.BYID[r]
    par = [p for g in f['_xav'] for p in g]
    sk = C.short(r) if hasattr(C, 'short') else r
    if not par and SEC[r] in L.LEADER_SECS and SEC[r] != 'bre':
        par = [C.PFX + 'ple_' + SEC[r]]
    d = [(P[r][0] - P[p][0], P[r][1] - P[p][1]) for p in par]
    near = min(d, key=lambda t: (abs(t[1]), abs(t[0]))) if d else None
    fl.append(dict(id=r.replace(C.PFX, ''), sec=SEC[r], xy=P[r], logical_parents=[p.replace(C.PFX, '') for p in par], nearest_dxdy=near))
out['roots'] = dict(n=len(roots), row0=len(row0), below_row0=len(fl), floating=fl)
print(f"roots without prerequisite: {len(roots)} (row 0: {len(row0)}, below row 0: {len(fl)})")
for x in fl:
    print(f"   {x['sec']:6s} {x['id']:40s} at {x['xy']} logical parent dx/dy {x['nearest_dxdy']}")
# logical links that are not lines (available only): _xav + dropped plenum links
links = []
for f in L.FOCI:
    for g in f['_xav']:
        for p in g:
            links.append((p, f['id']))
for k in L.LEADER_SECS:
    if k != 'bre':
        links.append((C.PFX + 'ple_' + k, L.ANCHOR[k]))
ld = [(abs(P[c][0] - P[p][0]), P[c][1] - P[p][1]) for p, c in links]
out['dotted_links'] = dict(n=len(links), median_dx=st.median(d[0] for d in ld) if ld else 0, max_dx=max((d[0] for d in ld), default=0),
                           median_dy=st.median(d[1] for d in ld) if ld else 0, max_dy=max((d[1] for d in ld), default=0),
                           over10=sum(1 for d in ld if d[0] + abs(d[1]) > 10))
print("dotted links", out['dotted_links'])
# section boxes, tops, stacking
box = {}
for k in L.ORDER:
    pts = [P[i] for i in P if SEC[i] == k]
    box[k] = (min(x for x, y in pts), max(x for x, y in pts), min(y for x, y in pts), max(y for x, y in pts))
out['sections'] = {k: dict(x0=b[0], x1=b[1], y0=b[2], y1=b[3]) for k, b in box.items()}
UP = collections.defaultdict(set)      # section -> sections it hangs from (prerequisite line, `available` link, candidacy)
for f in L.FOCI:
    for g in f['pre'] + f['_xav']:
        for p in g:
            if SEC[p] != f['sec']:
                UP[f['sec']].add(SEC[p])
for k in L.LEADER_SECS:
    UP[k].add('ple')


def related(a, b, seen=()):
    """a hangs (directly or through other sections) from b"""
    return b in UP[a] or any(related(c, b, seen + (a,)) for c in UP[a] if c not in seen)
stacked = []
for a in L.ORDER:
    for b in L.ORDER:
        if a == b: continue
        A, B = box[a], box[b]
        ov = min(A[1], B[1]) - max(A[0], B[0])
        if ov >= 2 and B[2] > A[3]:     # b entirely below a with >=2 columns of x overlap
            stacked.append((b, a, ov, related(b, a)))
out['stacked'] = [dict(lower=b, upper=a, x_overlap=ov, logical_child=r) for b, a, ov, r in stacked]
print("stacked below another section:", len(stacked), " unrelated:", sum(1 for s in stacked if not s[3]))
for b, a, ov, r in stacked:
    print(f"   {b:6s} below {a:6s} (x overlap {ov:.0f}) {'logical child' if r else 'UNRELATED'}")
# empty space: column profile (top margin above the first focus, interior vertical holes >= 3 rows)
from colprof import profile
out['columns'] = profile(P)
print("column profile:", out['columns'])
# neighbour gaps between sections in shared rows
rows = collections.defaultdict(lambda: collections.defaultdict(list))
for i, (x, y) in P.items():
    rows[y][SEC[i]].append(x)
ng = []
for y, d in rows.items():
    seq = sorted((x, s) for s, xs in d.items() for x in xs)
    for (x1, s1), (x2, s2) in zip(seq, seq[1:]):
        if s1 != s2:
            ng.append(x2 - x1)
out['section_neighbour_gap'] = dict(n=len(ng), min=min(ng), median=st.median(ng), share_2=round(sum(g <= 2 for g in ng) / len(ng), 2),
                                    share_ge10=round(sum(g >= 10 for g in ng) / len(ng), 2))
print("neighbour gap between sections in a row:", out['section_neighbour_gap'])
# tops of side-by-side blocks
tops = collections.Counter(box[k][2] for k in L.ORDER)
out['section_top_rows'] = dict(sorted(tops.items()))
print("section top rows:", dict(sorted(tops.items())))
# mutually exclusive
mx = []; seen = set()
for f in L.FOCI:
    g = tuple(sorted([f['id']] + f['mx']))
    if len(g) < 2 or g in seen: continue
    seen.add(g)
    ys = {P[i][1] for i in g}; xs = sorted(P[i][0] for i in g)
    between = [i for i in P if P[i][1] == P[g[0]][1] and xs[0] < P[i][0] < xs[-1] and i not in g]
    mx.append(dict(g=[i.replace(C.PFX, '') for i in g], same_row=len(ys) == 1, adjacent=not between, dx=[b - a for a, b in zip(xs, xs[1:])]))
out['mx'] = dict(n=len(mx), same_row=sum(m['same_row'] for m in mx), adjacent=sum(m['adjacent'] for m in mx),
                 dx=dict(collections.Counter(d for m in mx for d in m['dx'])), bad=[m for m in mx if not (m['same_row'] and m['adjacent'])])
print("mutually exclusive groups:", {k: v for k, v in out['mx'].items() if k != 'bad'}, "bad:", out['mx']['bad'])
# parent centring
cen = []
for p in P:
    nxt = [c for c in C.CH[p] if P[c][1] == P[p][1] + 1]
    if len(nxt) >= 2:
        xs = sorted(P[c][0] for c in nxt); cen.append(P[p][0] - (xs[0] + xs[-1]) / 2)
out['centring'] = dict(n=len(cen), exact=sum(abs(d) <= 0.5 for d in cen), within1=sum(abs(d) <= 1 for d in cen))
print("parent centring (>=2 children at dy 1):", out['centring'])
lc = L.line_conflicts()
out['line_conflicts'] = len(lc)
print("line conflicts:", len(lc))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'cw_probe_{sys.argv[1]}.json'), 'w'), indent=1, default=str)
