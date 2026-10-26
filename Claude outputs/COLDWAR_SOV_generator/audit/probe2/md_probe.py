# IMPERIA CW — Cold War: probe2 — md probe.
"""Positioning probe of MD 2000 Russia (05_russia.txt). Prints numeric rules; writes md_probe.json."""
import sys, json, collections, statistics as st
sys.path.insert(0, '/home/claude/audit')
from md_load import *
from md_analyze import LABEL, G, ORDER_LR
P = {f['id']: (f['ax'], f['ay']) for f in F}
EDGES = [(p, f['id'], len(g)) for f in F for g in f['pre'] for p in g if p in BY]
out = {}
# 1. parent centring
cen = collections.Counter(); cen_n = collections.defaultdict(list)
for p in BY:
    ch = [c for c in CH[p]]
    nxt = [c for c in ch if P[c][1] == P[p][1] + 1]
    if len(nxt) < 2: continue
    xs = sorted(P[c][0] for c in nxt)
    d = P[p][0] - (xs[0] + xs[-1]) / 2
    cen[round(d, 1)] += 1
    cen_n[len(nxt)].append(d)
print("1. parent x - midpoint(children at dy1), n parents with >=2 dy1 children:", sum(cen.values()))
print("   ", sorted(cen.items(), key=lambda t: -t[1])[:12])
for n in sorted(cen_n):
    v = cen_n[n]; print(f"   {n} children: n={len(v)} centred(|d|<=0.5)={sum(abs(x)<=0.5 for x in v)} |d|<=1:{sum(abs(x)<=1 for x in v)}")
# single child directly below?
one = [(p, c) for p in BY for c in CH[p] if len(CH[p]) == 1]
print("   single-child parents:", len(one), "dx=0:", sum(P[c][0] == P[p][0] for p, c in one), "dx<=1:", sum(abs(P[c][0]-P[p][0])<=1 for p, c in one))
# primary tree: parent = prerequisite nearest in x (tie: lowest dy)
PRIM = {}
for f in F:
    c = [p for g in f['pre'] for p in g if p in BY]
    if c:
        PRIM[f['id']] = min(c, key=lambda p: (P[f['id']][1] - P[p][1], abs(P[p][0] - P[f['id']][0])))
KIDS = collections.defaultdict(list)
for c, p in PRIM.items(): KIDS[p].append(c)
def sub(i):
    s = [i]
    for c in KIDS[i]: s += sub(c)
    return s
def box(ids):
    xs = [P[i][0] for i in ids]; ys = [P[i][1] for i in ids]
    return min(xs), max(xs), min(ys), max(ys)
print("\n2. top level: roots and Yeltsin's children")
roots = [f['id'] for f in F if f['id'] not in PRIM]
for r in sorted(roots, key=lambda i: P[i]):
    b = box(sub(r)); print(f"   root {r:40s} at {P[r]}  subtree x{b[0]:.0f}-{b[1]:.0f} y{b[2]:.0f}-{b[3]:.0f} n={len(sub(r))} allow_branch={'Y' if BY[r]['allow_branch'] else '-'} rel={BY[r]['rel']}")
for c in sorted(KIDS['SOV_reign_of_yeltsin'], key=lambda i: P[i]):
    b = box(sub(c)); print(f"   yeltsin-> {c:40s} at {P[c]} dx={P[c][0]-P['SOV_reign_of_yeltsin'][0]:+.0f} subtree x{b[0]:.0f}-{b[1]:.0f} y{b[2]:.0f}-{b[3]:.0f} w={b[1]-b[0]+1:.0f} h={b[3]-b[2]+1:.0f} n={len(sub(c))} centre-offset={P[c][0]-(b[0]+b[1])/2:+.1f}")
# ---- 3. blocks: top-level (party blocks under Yeltsin + domain roots), tops, depths, widths, fill
BLK = {}
for c in KIDS['SOV_reign_of_yeltsin']: BLK[c] = sub(c)
for r in ['SOV_economic_russian', 'SOV_groznyy_offensive', 'SOV_safe_russia', 'SOV_slavic_corps', 'SOV_withdraw_from_the_sco', 'SOV_kob_party_start']:
    BLK[r] = sub(r)
# attach orphans (roots without prereq tucked in) to the block of their rel anchor
for r in roots:
    if r in BLK or r == 'SOV_reign_of_yeltsin': continue
    a = BY[r]['rel']
    for b, ids in BLK.items():
        if a in ids: ids += sub(r)
order = sorted(BLK, key=lambda b: box(BLK[b])[0])
print("\n3. blocks left to right (x0-x1, top row, bottom row, w, h, foci, fill of bbox, rows used)")
rows_info = {}
for b in order:
    x0, x1, y0, y1 = box(BLK[b]); n = len(BLK[b])
    rows = collections.Counter(P[i][1] for i in BLK[b])
    w, h = x1 - x0 + 1, y1 - y0 + 1
    fill = n / ((w / 2 + 0.5) * h)   # cells at 2-column pitch
    rows_info[b] = dict(x0=x0, x1=x1, y0=y0, y1=y1, w=w, h=h, n=n, fill=round(fill, 2), per_row=[rows.get(y, 0) for y in range(int(y0), int(y1) + 1)])
    print(f"   {b:28s} x{x0:5.0f}-{x1:5.0f} y{y0:3.0f}-{y1:3.0f} w{w:4.0f} h{h:3.0f} n{n:4d} fill(2-col pitch) {fill:.2f} per-row {rows_info[b]['per_row']}")
out['blocks'] = rows_info
# gap between neighbouring blocks: per shared row, nearest foci of the two blocks
print("\n   neighbour gaps (per shared row: min distance between nearest foci of block A (left) and block B (right))")
gaps = {}
for a, b in zip(order, order[1:]):
    ra = collections.defaultdict(list); rb = collections.defaultdict(list)
    for i in BLK[a]: ra[P[i][1]].append(P[i][0])
    for i in BLK[b]: rb[P[i][1]].append(P[i][0])
    d = []
    for y in set(ra) & set(rb):
        d.append(min(abs(u - v) for u in ra[y] for v in rb[y]))
    ov = box(BLK[a])[1] - box(BLK[b])[0]
    gaps[f"{a}|{b}"] = dict(min=min(d) if d else None, median=st.median(d) if d else None, bbox_overlap=ov)
    print(f"   {a:26s}| {b:26s} min {min(d) if d else '-'} median {st.median(d) if d else '-'}  bbox overlap {ov:+.0f} cols")
out['neighbour_gaps'] = gaps
# ---- 4. hinges: parents whose children start sub-blocks (>=3 children, or >=2 children each with subtree >=5 foci)
print("\n4. hinges (parent -> sub-blocks): bar span, parent position on bar, sub-block widths/depths, gaps between sub-blocks")
hinges = []
for p in BY:
    ks = sorted(KIDS[p], key=lambda c: P[c][0])
    big = [c for c in ks if len(sub(c)) >= 5]
    if len(ks) >= 4 or len(big) >= 3:
        xs = [P[c][0] for c in ks]
        sb = []
        for c in ks:
            x0, x1, y0, y1 = box(sub(c)); sb.append((c, x0, x1, y0, y1, len(sub(c))))
        gl = []
        for (a, *_), (b, *_) in zip(sb, sb[1:]):
            ra = collections.defaultdict(list); rb = collections.defaultdict(list)
            for i in sub(a): ra[P[i][1]].append(P[i][0])
            for i in sub(b): rb[P[i][1]].append(P[i][0])
            d = [min(abs(u - v) for u in ra[y] for v in rb[y]) for y in set(ra) & set(rb)]
            gl.append(min(d) if d else None)
        h = dict(parent=p, pxy=P[p], n=len(ks), bar=(min(xs), max(xs)), span=max(xs) - min(xs),
                 parent_rel=round((P[p][0] - min(xs)) / max(1, max(xs) - min(xs)), 2), dy=sorted({P[c][1] - P[p][1] for c in ks}),
                 widths=[s[2] - s[1] + 1 for s in sb], depths=[s[4] - s[3] + 1 for s in sb], sizes=[s[5] for s in sb], gaps=gl,
                 child_dx=[P[c][0] - P[p][0] for c in ks])
        hinges.append(h)
for h in sorted(hinges, key=lambda h: -h['span']):
    print(f"   {h['parent']:38s} at {h['pxy']} kids {h['n']:2d} dy{h['dy']} bar {h['bar'][0]:.0f}-{h['bar'][1]:.0f} span {h['span']:3.0f} parent@{h['parent_rel']:.2f}")
    print(f"        sub-block w {h['widths']}\n        depth {h['depths']}\n        size {h['sizes']}\n        gaps {h['gaps']}")
out['hinges'] = hinges
# ---- 5. foci without prerequisite below row 0 (tucked roots)
print("\n5. roots without prerequisite below row 0: gate, anchor, free space around")
occ = {(P[i][0], P[i][1]) for i in P}
tucked = []
for r in roots:
    if P[r][1] == 0: continue
    f = BY[r]
    near = sorted((abs(P[i][0] - P[r][0]) + abs(P[i][1] - P[r][1]), i) for i in P if i != r and i not in sub(r))[:1]
    above = [i for i in P if P[i][1] < P[r][1] and abs(P[i][0] - P[r][0]) <= 1 and i not in sub(r)]
    ab = max(above, key=lambda i: P[i][1]) if above else None
    b = box(sub(r))
    t = dict(id=r, xy=P[r], allow_branch=bool(f['allow_branch']), rel=f['rel'], subtree=b, n=len(sub(r)),
             above=ab, above_xy=P[ab] if ab else None, gap_rows=(P[r][1] - P[ab][1]) if ab else None)
    tucked.append(t)
    print(f"   {r:30s} {P[r]} allow_branch={t['allow_branch']} rel={f['rel']} subtree {b} n={t['n']}; focus straight above: {ab} {t['above_xy']} (dy {t['gap_rows']})")
out['tucked'] = tucked
# ---- 6. mutually exclusive
print("\n6. mutually exclusive groups")
mxs = []
seen = set()
for f in F:
    grp = tuple(sorted([f['id']] + [m for m in f['mx'] if m in BY]))
    if len(grp) < 2 or grp in seen: continue
    seen.add(grp)
    xs = sorted(P[i][0] for i in grp); ys = {P[i][1] for i in grp}
    pars = set.intersection(*[set(p for g in BY[i]['pre'] for p in g) for i in grp])
    par = next(iter(pars)) if pars else None
    mxs.append(dict(g=grp, n=len(grp), same_row=len(ys) == 1, dx=[b - a for a, b in zip(xs, xs[1:])],
                    shared_parent=par, parent_centered=(par is not None and abs(P[par][0] - (xs[0] + xs[-1]) / 2) <= 0.5),
                    parent_dy=(P[grp[0]][1] - P[par][1]) if par else None, adjacent=all(not any(P[k][1] == P[grp[0]][1] and xs[0] < P[k][0] < xs[-1] for k in P if k not in grp) for _ in [0])))
c = collections.Counter(len(m['g']) for m in mxs)
print("   groups by size:", dict(c), " same row:", sum(m['same_row'] for m in mxs), "/", len(mxs))
print("   dx between neighbours:", collections.Counter(d for m in mxs for d in m['dx']).most_common())
print("   with shared parent:", sum(m['shared_parent'] is not None for m in mxs), " parent centred over the group:", sum(m['parent_centered'] for m in mxs), " parent dy:", collections.Counter(m['parent_dy'] for m in mxs if m['parent_dy'] is not None))
print("   no other focus between partners:", sum(m['adjacent'] for m in mxs))
out['mx'] = [dict(m, g=list(m['g'])) for m in mxs]
# ---- 7. lines: lengths
print("\n7. prerequisite lines")
L = [(p, c, abs(P[c][0] - P[p][0]), P[c][1] - P[p][1], k) for p, c, k in EDGES]
print("   n", len(L), " dy:", collections.Counter(int(l[3]) for l in L).most_common(8))
print("   |dx|:", sorted(collections.Counter(int(l[2]) for l in L).items())[:16])
long = sorted(L, key=lambda l: -l[2])[:24]
for p, c, dx, dy, k in long:
    print(f"   dx {dx:4.0f} dy {dy:2.0f} {'OR' if k > 1 else '  '} {p} -> {c}")
out['lines'] = dict(n=len(L), dx_ge6=sum(l[2] >= 6 for l in L), dx_ge10=sum(l[2] >= 10 for l in L), dx_ge20=sum(l[2] >= 20 for l in L), dy1=sum(l[3] == 1 for l in L))
print("   ", out['lines'])
# ---- 8. OR groups
print("\n8. OR prerequisite groups: spread of the OR parents and child position")
ors = []
for f in F:
    for g in f['pre']:
        g = [p for p in g if p in BY]
        if len(g) < 2: continue
        xs = sorted(P[p][0] for p in g); ys = {P[p][1] for p in g}
        ors.append(dict(child=f['id'], n=len(g), spread=xs[-1] - xs[0], same_row=len(ys) == 1, child_between=xs[0] <= P[f['id']][0] <= xs[-1],
                        max_dx=max(abs(P[p][0] - P[f['id']][0]) for p in g), dy=sorted({P[f['id']][1] - P[p][1] for p in g})))
print("   n", len(ors), " parents on one row:", sum(o['same_row'] for o in ors), " child between parents:", sum(o['child_between'] for o in ors))
print("   spread:", sorted(collections.Counter(int(o['spread']) for o in ors).items()))
print("   max dx child-parent:", sorted(collections.Counter(int(o['max_dx']) for o in ors).items()))
out['or_groups'] = dict(n=len(ors), same_row=sum(o['same_row'] for o in ors), child_between=sum(o['child_between'] for o in ors),
                        spread=dict(collections.Counter(int(o['spread']) for o in ors)))
# ---- 9. relative_position_id of block tops
print("\n9. relative_position_id of block tops")
for b in order:
    print(f"   {b:28s} rel={BY[b]['rel']} x={BY[b]['x']} y={BY[b]['y']}")
json.dump(out, open('/home/claude/audit/probe2/md_probe.json', 'w'), indent=1, default=str)
sys.path.insert(0, '/home/claude/audit/probe2')
from colprof import profile
out['columns'] = profile(P)
print("\n10. column profile:", out['columns'])
W = max(x for x, y in P.values()) + 1; Hh = max(y for x, y in P.values()) + 1
out['canvas'] = dict(w=W, h=Hh, aspect_px=round(W * 96 / (Hh * 130), 2), fill=round(len(P) / (W * Hh), 3))
print("    canvas", out['canvas'])
ng = []
rows = collections.defaultdict(list)
BR = {}
for b, ids in BLK.items():
    for i in ids: BR[i] = b
BR['SOV_reign_of_yeltsin'] = 'Y'
for i, (x, y) in P.items(): rows[y].append((x, BR.get(i, '?')))
for y, seq in rows.items():
    seq.sort()
    for (x1, s1), (x2, s2) in zip(seq, seq[1:]):
        if s1 != s2: ng.append(x2 - x1)
out['block_neighbour_gap'] = dict(n=len(ng), min=min(ng), median=st.median(ng), share_2=round(sum(g <= 2 for g in ng) / len(ng), 2), share_ge10=round(sum(g >= 10 for g in ng) / len(ng), 2))
print("    neighbour gap between blocks in a row:", out['block_neighbour_gap'])
json.dump(out, open('/home/claude/audit/probe2/md_probe.json', 'w'), indent=1, default=str)
