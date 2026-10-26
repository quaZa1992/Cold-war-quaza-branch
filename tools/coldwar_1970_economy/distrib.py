# IMPERIA CW — Cold War: coldwar 1970 economy — distrib.
from alloc import *
CAPS=dict(industrial_complex=50,arms_factory=35,dockyard=20,offices=50,agriculture_district=10)
SHARED=('industrial_complex','arms_factory','dockyard','offices','agriculture_district')
def slots(sid): return catslots.get(cat.get(sid,'state_00'),1)+extra.get(sid,0)
def weights(t,k):
    ss=PLANS[t] and C[t]['states']
    out={}
    tot_base=sum(bs[s]['base'].get(k,0) for s in ss)
    for s in ss:
        if catslots.get(cat.get(s),1)==0 and k!='dockyard': out[s]=0; continue
        p=st[s]['mp']/1e6; pr=sprod[int(s)]/1000
        if k=='dockyard':
            out[s]=bs[s]['base'].get(k,0); continue
        if k=='offices': w=p*pr*pr
        elif k=='agriculture_district': w=p
        else: w=p*pr
        out[s]=w
    tw=sum(out.values())
    if k!='dockyard':
        bw={0.5:0.0}
        mix=0.7 if k=='arms_factory' else 0.5
        for s in ss:
            a=out[s]/tw if tw>0 else 0
            b=bs[s]['base'].get(k,0)/tot_base if tot_base>0 else a
            out[s]=(1-mix)*a+mix*b if tot_base>0 else a
    return out
def distribute(t):
    p=PLANS[t]; ss=C[t]['states']
    res={s:defaultdict(int) for s in ss}
    used={s:0 for s in ss}
    for k in ('arms_factory','dockyard','industrial_complex','offices','agriculture_district'):
        N=p['n'][k]
        if N<=0: continue
        w=weights(t,k)
        if sum(w.values())<=0:
            if k=='dockyard': continue
            w={s:st[s]['mp'] for s in ss}
        tw=sum(w.values())
        # D'Hondt-like: give one unit at a time to the state with the highest w/(alloc+1), respecting caps
        for _ in range(N):
            best=None;bv=-1
            for s in ss:
                if w[s]<=0: continue
                if res[s][k]>=CAPS[k]: continue
                soft=slots(s)+6   # runtime adds missing slots, but do not stuff tiny states
                if used[s]>=soft: continue
                v=w[s]/(res[s][k]+0.5)
                if v>bv: bv=v;best=s
            if best is None:
                for s in sorted(ss,key=lambda s:-w[s]):
                    if res[s][k]<CAPS[k] and w[s]>0: best=s;break
            if best is None: break
            res[best][k]+=1; used[best]+=1
    return res
ALLOC={t:distribute(t) for t in PLANS}
if __name__=='__main__':
    import collections
    over=0
    for t,r in ALLOC.items():
        for s,d in r.items():
            u=sum(d.values())
            if u>slots(s): over+=1
    print('states needing extra slots',over)
    for t in ['USA','GER','DDR','SOV','EGY']:
        print(t,{st[s]['file'][:-4]:dict(d) for s,d in ALLOC[t].items() if sum(d.values())>0})
