import sys, json, re
sys.path.insert(0, '/home/claude/sov')
import build_all
from sov_dsl import *
import d_concept as C
import d_republics as R

CW, CH, SX, SY = 150, 76, 174, 116
PADX, PADTOP, PADBOT, SECGAP, BANDGAP, MAXW = 22, 46, 22, 40, 56, 5600

byid = {f['id']: f for f in FOCI}
secs = {s['key']: s for s in SECTIONS}
order = [s['key'] for s in SECTIONS]

def layout_section(key):
    nodes = [f for f in FOCI if f['sec'] == key]
    ids = {f['id'] for f in nodes}
    layer = {}
    def L(fid):
        if fid in layer: return layer[fid]
        f = byid[fid]
        ps = [p for g in f['pre'] for p in g if p in ids]
        layer[fid] = 0 if not ps else 1 + max(L(p) for p in ps)
        return layer[fid]
    for f in nodes: L(f['id'])
    children = {f['id']: [] for f in nodes}
    roots = []
    for f in nodes:
        ps = [p for g in f['pre'] for p in g if p in ids]
        if ps:
            prim = max(ps, key=lambda p: (layer[p], -[n['id'] for n in nodes].index(p)))
            children[prim].append(f['id'])
        else:
            roots.append(f['id'])
    xs = {}
    slot = [0]
    def place(fid):
        ch = children[fid]
        if not ch:
            xs[fid] = slot[0]; slot[0] += 1
        else:
            for c in ch: place(c)
            xs[fid] = (xs[ch[0]] + xs[ch[-1]]) / 2
    for r in roots:
        place(r)
    # overlap check
    seen = {}
    for fid in xs:
        k = (layer[fid], round(xs[fid] * 2))
        assert k not in seen, (key, fid, seen.get(k))
        seen[k] = fid
    w = slot[0]; h = max(layer.values()) + 1
    return xs, layer, w, h

groups = []
for s in SECTIONS:
    if s['group'] not in groups: groups.append(s['group'])

out_foci, out_secs = [], []
HEADED = {"Politbüro & Outlooks": 1, "KPdSU & Generalsekretäre": 2}
for g in groups:
    gx, gy, bandh = 0, 0, 0
    keys = [k for k in order if secs[k]['group'] == g]
    lays = {k: layout_section(k) for k in keys}
    dims = {k: (PADX * 2 + (lays[k][2] - 1) * SX + CW, PADTOP + (lays[k][3] - 1) * SY + CH + PADBOT) for k in keys}
    if g in HEADED:
        hn = HEADED[g]
        rest = keys[hn:]
        band2 = min(MAXW, sum(dims[k][0] for k in rest) + SECGAP * (len(rest) - 1))
        band1 = sum(dims[k][0] for k in keys[:hn]) + SECGAP * (hn - 1)
        gx = max(0, (band2 - band1) // 2)
    for n, key in enumerate(keys):
        xs, lay, w, h = lays[key]
        bw, bh = dims[key]
        if g in HEADED and n == HEADED[g]:
            gx = 0; gy += bandh + BANDGAP * 2; bandh = 0
        elif gx > 0 and gx + bw > MAXW:
            gx = 0; gy += bandh + BANDGAP; bandh = 0
        out_secs.append(dict(key=key, group=g, title=secs[key]['title'], color=secs[key]['color'], desc=secs[key]['desc'],
                             party=secs[key]['party'], x=gx, y=gy, w=bw, h=bh,
                             n=sum(1 for f in FOCI if f['sec'] == key)))
        for f in FOCI:
            if f['sec'] != key: continue
            out_foci.append(dict(id=f['id'], name=f['name'], sec=key, g=g,
                                 x=round(gx + PADX + xs[f['id']] * SX), y=gy + PADTOP + lay[f['id']] * SY,
                                 c=f['cost'], pre=f['pre'], mx=f['mx'], av=f['av'], eff=[e['t'] for e in f['eff']],
                                 note=f['note'], h=f['hist'], ai=f['ai']))
        gx += bw + SECGAP
        bandh = max(bandh, bh)

COSTK = {'bureaucracy_cost_multiplier_modifier','corruption_cost_factor','consumer_goods_factor','agriculture_workers_modifier','military_spending_cost_factor','army_personnel_cost_multiplier_modifier','democratic_drift','nationalist_drift'}
concept = dict(
    spirits=[dict(id=PFX + k, name=n, mods=[[fmt_mod(a, b), (b > 0) != (a in COSTK)] for a, b in m.items()], why=w, how=hw) for k, n, m, w, hw in C.START_SPIRITS],
    already=C.ALREADY_THERE, laws=C.START_LAWS, factions=C.START_FACTIONS, dynmods=C.DYNMODS, bop=C.BOP, coh=C.COHESION,
    decisions=C.DECISIONS_C, events=C.EVENTS_C, leaders=C.LEADERS_C, notree=C.NO_TREE, politburo=R.POLITBURO, portraits=C.PORTRAITS, files=C.FILES,
    parties=[dict(i=i, name=PARTY[i][0], ideo=PARTY[i][1], leader=PARTY[i][2], outlook=OUTLOOK[OUTLOOK_OF[i]][0],
                  trig=TRIG[i] + "_are_in_power") for i in range(24)],
    offers=[dict(key=k, tags=v['tags'], text=v['text']) for k, v in OFFERS.items()],
    ideas=len(IDEAS), progs=len(PROGS), traits=sorted(TRAITS.values()), opinions=len(OPINIONS),
)
data = dict(foci=out_foci, sections=out_secs, groups=groups, concept=concept, card=[CW, CH])
s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
open('/home/claude/sov/sov_data.json', 'w').write(s)
print(len(out_foci), len(s))
for sct in out_secs: pass
import collections
print(collections.Counter((o['group']) for o in out_secs))
print(max(o['x']+o['w'] for o in out_secs), max(o['y']+o['h'] for o in out_secs))
