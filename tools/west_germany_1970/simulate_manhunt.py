import random, statistics as st
def run(new, bka=2, inpol=True, milieu=22, gen=1, ct=0.1, gsg=1, months=120):
    ort=[10]*6; ort[4]=20; stt=[0]*6; arrests=0; cd=0; months_to=None; shoot=0
    for m in range(months):
        if new:
            gain=0.5+bka*1.0+(2 if inpol else 0)-milieu/15-(1 if gen==2 else 0)-(2.5 if gen==3 else 0)+min(2,ct*6)
        else:
            gain=1+bka*1.5+(2 if inpol else 0)-milieu/25-(1.5 if gen==3 else 0)+ct*10
        for i in range(6):
            if stt[i]>=2: continue
            ort[i]+=gain+random.choice([1.5,-1.5])
            if new and stt[i]==1 and random.random()<(0.3 if gen>1 else 0.2): ort[i]-=15
            ort[i]=max(0,min(100,ort[i]))
            if ort[i]>59 and stt[i]==0: stt[i]=1
            if ort[i]<50 and stt[i]==1: stt[i]=0
        # auto arrests
        p=(0.06+0.04+(0.04 if bka>1 else 0)+(0.03 if bka>2 else 0)+0.03) if new else (0.10+0.06+0.06+(0.08 if bka>2 else 0)+0.04)
        if random.random()<p and any(s<2 for s in stt):
            n=(2 if random.random()<0.5 else 1) if (bka>2 if new else bka>1) else 1
            for _ in range(n):
                c=[i for i in range(6) if stt[i]<2]
                if c: b=max(c,key=lambda i:ort[i]); stt[b]=2; arrests+=1
        # player access
        cd-=1
        if cd<=0:
            t=[i for i in range(6) if stt[i]==1]
            if t:
                i=max(t,key=lambda i:ort[i]); cd=2 if new else 1
                if new:
                    w=30+(8 if ort[i]>74 else 0)+(10 if ort[i]>89 else 0)+(6 if gsg>0 else 0)+(6 if gsg>1 else 0)+(5 if bka>1 else 0)
                    tot=w+45+15*(0.5 if gsg>1 else 1)
                else:
                    w=40+(10 if ort[i]>74 else 0)+(10 if ort[i]>89 else 0)+(8 if gsg>0 else 0)+(8 if gsg>1 else 0)+(6 if bka>1 else 0); tot=w+30
                r=random.random()*tot
                if r<w: stt[i]=2; arrests+=1
                elif new and r>w+45: shoot+=1; stt[i]=random.choice([3,0]); ort[i]-=40 if stt[i]==0 else 0
                else: ort[i]-=35 if new else 30; stt[i]=0
        if months_to is None and sum(1 for s in stt if s>=2)>=4: months_to=m+1
    return months_to or months, shoot
for new in (False,True):
    for bka in (1,2,3):
        r=[run(new,bka=bka) for _ in range(2000)]
        print('neu' if new else 'alt','BKA',bka,'Monate bis 4 Festnahmen (Median):',st.median(x[0] for x in r),' Schusswechsel/Spiel:',round(st.mean(x[1] for x in r),2))
