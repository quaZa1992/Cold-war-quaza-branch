"""Monte Carlo model of the inner-German rivalry (1970-1990) for balancing.

    python3 simulate_rivalry.py [ai|hawk]

A simplified copy of the monthly tick, crisis rounds (every six months) and AI weights in rivalry.py.
Both sides are played by their AI here; the multiplayer paths (human answers) are not modelled.
"""
import random, statistics, sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rivalry as rv
M=rv.MATRIX; CR=rv.CRISIS_BY_ID
def run(seed, policy='ai'):
    r=random.Random(seed)
    k=-5; d=10; stufe=2; ib=2; idd=2; mob_b=mob_d=0; nato=True
    treaties=set(); verh=0; prog=0; chan={'vogel':1}; crisis=None; cd=0
    log=dict(crises=0, peaks=0, wars=0, won=0, lost=0, stale=0, comp=0, treaty_years={}, kl={}, stages=[])
    leader=0
    for m in range(12*20):
        year=1970+m//12
        if m==16: leader=1
        hard=30+m*0.2; moscow=90 - max(0,(year-1986))*12
        ib=min(6,ib+1+(1 if chan.get('sv') else 0)+(1 if stufe>2 else 0)); idd=min(6,idd+1+(1 if stufe>2 else 0))
        b=4*len(treaties)+2*sum(1 for v in chan.values() if v==1)
        b+= -5 if leader==0 else (-5 if 1980<=year<1983 else (5 if year>=1983 else 0))
        if year>=1983: b-=5  # CDU
        # focus effects of the historical AI path
        if policy=='hawk' and m>=4: b-=15
        elif m>=4: b+=3          # change through rapprochement
        if m>=8: b+=1          # erfurt and kassel
        if year>=1973: b+=2    # ratification
        if year>=1976: b+=2    # helsinki
        if year>=1978: b+=3    # community of responsibility
        if year>=1984: b+=4    # coalition of reason
        k += (b-k)*0.05 - d*0.03; k=max(-100,min(100,k)); d*=0.9
        # negotiations
        if verh:
            if stufe>3: verh=0; prog=0
            elif stufe<3:
                t=12+4*bool(chan.get('bahr'))+4*bool(chan.get('sv'))+k/10+2
                if leader==0 and verh>2: t*=0.5
                prog+=max(2,min(30,t))
                if prog>=100:
                    treaties.add(verh); log['treaty_years'][verh]=year
                    if verh==1: chan['bahr']=1; k+=10
                    if verh==2: k+=8; chan.setdefault('draht',0)
                    if verh==3: k+=10
                    if verh==5: chan['sv']=1; k+=6
                    if verh in (4,6,7,8,9): k+=6
                    verh=0; prog=0
        else:
            reqs={1:(-10,[],True),2:(-5,[1],True),3:(0,[1,2],year>=1971),4:(0,[3],True),5:(5,[3],True),6:(20,[3],True),7:(30,[5],year>=1980),8:(40,[5,6],year>=1983),9:(70,[3,5],False)}
            if crisis is None and r.random()<0.5 and policy!='hawk':
                for n,(mk,pre,ex) in reqs.items():
                    if n not in treaties and k>=mk and all(p in treaties for p in pre) and ex and stufe<3 and ib>=2:
                        verh=n; prog=0; ib-=2; break
        for c in ('bahr','draht'):
            if c in chan and chan[c]==0: chan[c]=1
        # DDR ai
        if crisis is None and idd>=2 and r.random()<0.4:
            idd-=2; x=r.random()
            if x<0.2: k-=6
            elif x<0.35: k-=5 if 2 not in treaties else 1; d+=12 if 2 not in treaties else 3
            elif x<0.55: pass
            elif x<0.7: k-=3
            elif x<0.85: d+=8
            else: k+=6
        # crisis roll
        cd=max(0,cd-1)
        if crisis is None and cd==0:
            w=18+15*(k<-10)+15*(k<-25)+15*(k<-40)+15*(k<-60)+15*(d>20)+25*(d>45)
            if k>30: w*=0.5
            if r.random()< w/(1000+w):
                typ=r.choice([1,2,3,5,8,9]) if year<1990 else r.choice([2,3])
                if typ==1 and 2 in treaties and r.random()<0.85: typ=2
                crisis=dict(typ=typ,int=CR[typ][3],rd=0,mon=0,mx=CR[typ][5]); log['crises']+=1; d+=10
        if crisis:
            crisis['mon']+=1
            if crisis['mon']>=6:
                crisis['mon']=0
                # bonn stance (AI)
                h=r.choice([4,4,3,7]) if policy=='hawk' else r.choices([1,2,3,4,5,6],[10,25*(2 if year<1983 else 1),25*(2 if year>=1983 else 1),10,15*nato,25*any(v==1 for v in chan.values())])[0]
                cost={1:0,2:1,3:1,4:2,5:1,6:2,7:3}[h]
                if ib<cost: h=1
                else: ib-=cost
                ww=[10*(3 if leader>2 else 1)*(0.5 if leader==0 else 1),30*(1.5 if leader in(1,2) else 1),20*(1.5 if leader==0 else 1)*(1.5 if moscow>69 else 1)*(0.6 if mob_b>1 else 1)*(idd>=1),10*(1.5 if moscow>69 else 1)*(idd>=1),10*(2 if hard>60 else 1)*(2 if leader==1 and year>1980 else 1)*(idd>=1)]
                a=r.choices([1,2,3,4,5],ww)[0]
                if a>2: idd-=1
                di=M[h][a]
                if CR[crisis['typ']][4]==h: di-=10
                if a in (3,4): di+=(moscow-50)/7
                crisis['int']=max(0,min(100,crisis['int']+di)); crisis['rd']+=1
                if di>0: d+=di/2; k-=di/5
                else: k+=-di/10
                settle=lambda: 1 if (a==1 and h!=2) else (2 if (h==2 and a not in (1,2)) else 7)
                out=None
                if crisis['int']<=0:
                    out=settle()
                elif crisis['int']>=100:
                    log['peaks']+=1
                    # AI: 60 give way, 25 resolve, 15 mediate (needs NATO or the hotline)
                    x=r.random() if policy!='hawk' else 0.99
                    if x<0.6: out=4
                    elif x<0.75 and (nato or chan.get('draht')): crisis['int']=50
                    else:
                        for step in range(3):   # monthly countdown
                            p=0.3*(1.5 if moscow<50 else 1)*(1.5 if leader>0 and year>1980 else 1)
                            p=p/(p+0.7*(1.3 if moscow>69 else 1))
                            if r.random()<p: out=5; break
                            if policy!='hawk' and r.random()<0.5: out=4; break   # AI gives way half the time
                        if out is None:
                            pw=0.15*(2 if moscow<70 else 1)*0.7
                            out=6   # an AI East Berlin is always reined in by Moscow; only humans order war
                elif crisis['rd']>crisis['mx']:
                    out=settle() if crisis['int']<50 else 3
                if out:
                    if out in (1,5,6): log['won']+=1
                    elif out in (2,4): log['lost']+=1
                    elif out==7: log['comp']+=1; k+=5
                    else: log['stale']+=1; k-=5; d+=10
                    if out==5: k-=10
                    if out==4: k+=10
                    crisis=None; cd=12
                    if out==8: return log
        # stage
        ci=crisis['int'] if crisis else 0
        t=3
        if k>39: t=0
        elif k>9: t=1
        elif k>-21: t=2
        if ci>49: t=max(t,3)
        if k<-45 or ci>74: t=max(t,4)
        if ci>89 and k<-60: t=5
        stufe=t
        d=max(0,min(100,d)); k=max(-100,min(100,k))
        log['kl'][year]=k; log['stages'].append(stufe)
    return log
N=2000
logs=[run(i, sys.argv[1] if len(sys.argv)>1 else 'ai') for i in range(N)]
print('crises/run', statistics.mean(l['crises'] for l in logs), 'peaks', statistics.mean(l['peaks'] for l in logs), 'war%', 100*sum(l['wars'] for l in logs)/N)
print('won',statistics.mean(l['won'] for l in logs),'lost',statistics.mean(l['lost'] for l in logs),'compromise',statistics.mean(l['comp'] for l in logs),'stale',statistics.mean(l['stale'] for l in logs))
for y in (1970,1972,1975,1980,1985,1989):
    v=[l['kl'].get(y) for l in logs if y in l['kl']]
    print(y, 'klima', round(statistics.mean(v),1), round(min(v)),round(max(v)))
for n in range(1,10):
    ys=[l['treaty_years'][n] for l in logs if n in l['treaty_years']]
    print('treaty',n, len(ys)/N, round(statistics.mean(ys),1) if ys else None)
import collections
c=collections.Counter(s for l in logs for s in l['stages']); tot=sum(c.values()); print({k:round(v/tot*100,1) for k,v in sorted(c.items())})
