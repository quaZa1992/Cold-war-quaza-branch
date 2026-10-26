# IMPERIA CW — Cold War: coldwar 1970 economy — alloc.
from data import *
ISO={'ADO':['AND'],'AFG':['AFG'],'ALB':['ALB'],'ALG':['DZA'],'ARG':['ARG'],'ARM':['ARM'],'AST':['AUS'],'AUS':['AUT'],'AZE':['AZE'],'BAR':['BRB'],'BEL':['BEL'],'BEN':['BEN'],'BFA':['BFA'],'BHR':['BHR'],'BHU':['BTN'],'BLR':['BLR'],'BOL':['BOL'],'BOT':['BWA'],'BRA':['BRA'],'BRM':['MMR'],'BRU':['BRN'],'BUL':['BGR'],'BUR':['BDI'],'CAM':['CMR'],'CAN':['CAN'],'CAR':['CAF'],'CBD':['KHM'],'CDI':['CIV'],'CHA':['TCD'],'CHI':['CHN'],'CHL':['CHL'],'CNG':['COG'],'COL':['COL'],'COS':['CRI'],'CUB':['CUB'],'CYP':['CYP'],'CZE':['CZE','SVK'],'DEN':['DNK'],'DOM':['DOM'],'DRC':['COD'],'ECU':['ECU'],'EGU':['GNQ'],'EGY':['EGY'],'ELS':['SLV'],'ENG':['GBR'],'EST':['EST'],'ETH':['ETH'],'FIN':['FIN'],'FRA':['FRA'],'GAB':['GAB'],'GAH':['GHA'],'GAM':['GMB'],'GEO':['GEO'],'GRE':['GRC'],'GUA':['GTM'],'GUI':['GIN'],'GUY':['GUY'],'HAI':['HTI'],'HOL':['NLD'],'HON':['HND'],'HUN':['HUN'],'ICE':['ISL'],'IND':['IDN'],'IRE':['IRL'],'IRQ':['IRQ'],'ISR':['ISR'],'ITA':['ITA'],'JAM':['JAM'],'JAP':['JPN'],'JOR':['JOR'],'KAZ':['KAZ'],'KEN':['KEN'],'KOR':['KOR'],'KUW':['KWT'],'KYR':['KGZ'],'LAO':['LAO'],'LAT':['LVA'],'LBA':['LBY'],'LEB':['LBN'],'LES':['LSO'],'LIB':['LBR'],'LIT':['LTU'],'LUX':['LUX'],'MAD':['MDG'],'MAL':['MLI'],'MAY':['MYS'],'MEX':['MEX'],'MLD':['MDV'],'MLT':['MLT'],'MLV':['MDA'],'MLW':['MWI'],'MNC':['MCO'],'MON':['MNG'],'MOR':['MAR'],'NAU':['NRU'],'NEP':['NPL'],'NGR':['NER'],'NIC':['NIC'],'NIG':['NGA'],'NRY':['NOR'],'NZL':['NZL'],'OMA':['OMN'],'PAK':['PAK','BGD'],'PAN':['PAN'],'PAR':['PRY'],'PER':['IRN'],'PHI':['PHL'],'POL':['POL'],'POR':['PRT'],'PRU':['PER'],'QAT':['QAT'],'RAJ':['IND'],'ROM':['ROU'],'RWA':['RWA'],'SAF':['ZAF'],'SAM':['WSM'],'SAU':['SAU'],'SEN':['SEN'],'SER':['SRB','HRV','SVN','BIH','MNE','MKD'],'SIA':['THA'],'SIE':['SLE'],'SIN':['SGP'],'SMA':['SMR'],'SOM':['SOM'],'SOV':['RUS'],'SPR':['ESP'],'SRI':['LKA'],'SUD':['SDN'],'SWA':['SWZ'],'SWE':['SWE'],'SWI':['CHE'],'SYR':['SYR'],'TAJ':['TJK'],'TNZ':['TZA'],'TOG':['TGO'],'TON':['TON'],'TRI':['TTO'],'TRK':['TKM'],'TUN':['TUN'],'TUR':['TUR'],'UAE':['ARE'],'UGA':['UGA'],'UKR':['UKR'],'URG':['URY'],'USA':['USA'],'UZB':['UZB'],'VEN':['VEN'],'ZAM':['ZMB'],'ZIM':['ZWE']}
# Real output growth 1970->2000 (approx., Maddison/WDI constant prices). Used only to cap 1970 building counts against the MD 2000 map.
GROW={'USA':2.75,'CAN':2.6,'MEX':3.1,'BRA':3.4,'ARG':1.8,'CHL':2.6,'COL':3.2,'VEN':2.0,'PRU':2.0,'ENG':1.95,'FRA':2.15,'GER':1.95,'DDR':1.3,'ITA':2.0,'SPR':2.6,'POR':2.6,'HOL':2.2,'BEL':2.1,'SWE':1.8,'NRY':2.7,'DEN':1.9,'FIN':2.3,'SWI':1.6,'AUS':2.3,'IRE':4.0,'GRE':2.2,'TUR':3.5,'JAP':2.8,'KOR':9.0,'TAI':7.5,'CHI':8.0,'RAJ':4.0,'PAK':4.2,'IND':4.5,'SIA':5.5,'MAY':5.8,'SIN':8.0,'PHI':2.7,'SOV':1.3,'UKR':0.75,'BLR':1.3,'KAZ':1.0,'UZB':1.4,'EST':1.1,'LAT':1.0,'LIT':1.0,'GEO':0.6,'ARM':0.8,'AZE':0.8,'MLV':0.6,'KYR':0.9,'TAJ':0.7,'TRK':1.0,'POL':1.7,'CZE':1.5,'HUN':1.5,'ROM':1.3,'BUL':1.3,'SER':1.2,'ALB':1.6,'EGY':4.5,'ISR':3.8,'SAU':3.2,'PER':2.0,'IRQ':1.0,'SYR':4.0,'JOR':4.5,'ALG':2.5,'MOR':3.0,'TUN':4.0,'LBA':1.0,'NIG':2.2,'BIA':2.2,'SAF':2.1,'KEN':3.0,'ETH':2.0,'DRC':0.6,'GAH':2.0,'AST':2.6,'NZL':1.9,'CUB':1.5,'VIE':3.5,'SVN':3.5,'NKO':1.0,'YEM':3.0,'SYE':3.0,'UAE':6.0,'KUW':1.5,'QAT':3.0,'OMA':6.0,'BHR':3.0,'LEB':1.6,'CYP':4.0,'MLT':4.0,'ICE':2.8,'LUX':3.2}
def grow(t):
    if t in GROW: return GROW[t]
    return 2.4
SOCIALIST={'SOV','UKR','BLR','KAZ','UZB','EST','LAT','LIT','GEO','ARM','AZE','MLV','KYR','TAJ','TRK','DDR','POL','CZE','HUN','ROM','BUL','SER','ALB','CHI','NKO','VIE','CUB','MON','SYE'}
# 1970 military expenditure, bn current US$ (SIPRI/ACDA order of magnitude). Arms factories = 0.8 per bn for the superpowers, 1.0 otherwise.
USSR_SPLIT={'SOV':.62,'UKR':.18,'BLR':.05,'KAZ':.04,'UZB':.03,'GEO':.015,'AZE':.015,'ARM':.01,'LIT':.01,'LAT':.01,'EST':.01,'MLV':.005,'KYR':.005,'TAJ':.005,'TRK':.005}
MILX={'USA':77.8,'CHI':20,'ENG':5.9,'FRA':6.0,'GER':6.1,'ITA':2.6,'JAP':1.6,'CAN':1.9,'AST':1.0,'RAJ':1.6,'PAK':0.7,'ISR':1.3,'EGY':1.3,'SYR':0.3,'IRQ':0.3,'PER':0.8,'SAU':0.4,'TUR':0.5,'GRE':0.4,'POL':2.0,'CZE':1.7,'DDR':1.9,'HUN':0.5,'ROM':0.6,'BUL':0.4,'SER':0.6,'SWE':1.1,'HOL':1.3,'BEL':0.7,'SPR':0.6,'NRY':0.4,'DEN':0.4,'SWI':0.5,'BRA':1.0,'ARG':0.5,'MEX':0.2,'KOR':0.4,'TAI':0.6,'NKO':0.8,'VIE':0.8,'SVN':0.8,'SAF':0.4,'CUB':0.3,'POR':0.6,'FIN':0.2,'AUS':0.2,'JOR':0.15,'LBA':0.1,'ALG':0.1,'MOR':0.1,'IND':0.3,'SIA':0.25,'PHI':0.15,'NIG':0.3,'ETH':0.05,'VEN':0.2,'CHL':0.15,'PRU':0.15,'COL':0.1}
for t,f in USSR_SPLIT.items(): MILX[t]=70*f
DOCKS={'USA':18,'SOV':10,'UKR':4,'JAP':15,'ENG':8,'GER':7,'SWE':5,'FRA':5,'ITA':4,'HOL':3,'SPR':3,'POL':3,'NRY':2,'DEN':2,'DDR':2,'CHI':3,'KOR':1,'BRA':1,'CAN':1,'SER':2,'FIN':1,'AST':1,'RAJ':1,'ARG':1,'TUR':1,'GRE':1,'POR':1,'BUL':1,'ROM':1,'TAI':1,'BEL':1,'LAT':1,'EST':0,'LIT':0}
def sectors(gpc,t):
    if gpc<0.15: a,i,s=.45,.15,.40
    elif gpc<0.4: a,i,s=.30,.25,.45
    elif gpc<1.0: a,i,s=.15,.33,.52
    elif gpc<2.5: a,i,s=.08,.40,.52
    else: a,i,s=.04,.38,.58
    if t in SOCIALIST: i+=.15; s-=.15
    return a,i,s
VAL=dict(industrial_complex=10,arms_factory=1.5,dockyard=1.5,offices=35,agriculture_district=15)
WRK=dict(industrial_complex=0.206,arms_factory=0.0188,dockyard=0.0188,offices=0.473,agriculture_district=0.188)
def r_tag(t): return 1.3 if t=='USA' else (1.0 if t=='CHI' else 0.8)
def mult(prod,t):
    pm=prod/1000
    if prod<1000: pm*=prod/1000
    return pm*r_tag(t)
def inv_comp(T):
    if T>=1000: return T
    return (-0.75+math.sqrt(0.5625+0.001*T))/0.0005
def comp(x): return x if x>=1000 else x*(0.75+0.25*x/1000)
EXCLUDE={'UAE'}
U_TARGET=0.12   # unemployed share of the workforce aimed for at start (MD threshold is 6 %)
M_MAX_DEV=2.0
M_MAX_DEVING=3.0
def plan(t):
    c=C[t]; P=c['pop']; prod=c['prod_pw']; T=tgt[t]*3.4; gpc=tgt[t]/P if P>0 else 1
    W=0.6*P
    dev=prod>699
    rp=0.1 if dev else min(1,max(0.1,0.9*(1-prod/650)))
    rw=min(c['res']*0.01*rp,0.75*W)
    ap=0.05 if dev else min(0.9,max(0.05,0.9*(1-prod/650)))
    aw=(W-rw)*ap
    misc=0.012*P  # healthcare + bureaucracy staff
    Wn=max(W-rw-aw-misc,0)
    fixed=aw*0.3677+c['res']*0.5+P*0.02*(T/P if P else 0)*1.0
    base=defaultdict(float)
    for sid in c['states']:
        for k,v in bs[sid]['base'].items(): base[k]+=v
    fixed+=base['nuclear_reactor']*4+base['renewable_energy_infra']*2
    S=inv_comp(T)/mult(prod,t)
    need_val=max(S-fixed,0)
    mil=round(MILX.get(t,0)*(0.8 if t in ('USA','CHI') or t in USSR_SPLIT else 1.0))
    if MILX.get(t,0)>=0.25: mil=max(mil,1)
    dock=DOCKS.get(t,0)
    if not any(bs[s]['base'].get('dockyard',0)>0 for s in c['states']): dock=0
    rest=max(need_val-1.5*(mil+dock),0)
    v2000=sum(base[k]*VAL[k] for k in ('industrial_complex','offices','agriculture_district'))
    cap=v2000/grow(t)*1.25
    # composition: MD 2000 building mix of these states, shifted to 1970 (more farms, fewer offices)
    adj=dict(agriculture_district=1.6,industrial_complex=1.3,offices=0.55)
    if t in SOCIALIST: adj=dict(agriculture_district=1.6,industrial_complex=1.4,offices=0.35)
    wts={k:base[k]*adj[k] for k in adj}
    if sum(wts.values())<3:
        a,i,s_=sectors(gpc,t); wts=dict(agriculture_district=a/15,industrial_complex=i/10,offices=s_/35)
    vs=sum(wts[k]*VAL[k] for k in wts)
    comp_=dict((k,wts[k]/vs) for k in wts)   # buildings per value unit
    wpv=sum(comp_[k]*WRK[k] for k in comp_)  # workers per value unit (base requirement)
    mmax=M_MAX_DEV if prod>=600 else M_MAX_DEVING
    avail=max(Wn-U_TARGET*W-(mil+dock)*0.0188,0)
    val0=min(rest,cap)
    if val0*wpv>avail: val=avail/wpv; mode='SCALED'
    elif val0*wpv*(1+mmax)<avail: val=min(avail/(1+mmax)/wpv, max(rest, 2*cap)); mode='FILLED' if val>val0 else 'CAP'
    else: val=val0; mode='CAP' if rest>cap else 'GDP'
    n={k:int(round(val*comp_[k])) for k in comp_}
    if (val>=5 or (tgt[t]>=1.0 and P>1)) and n['industrial_complex']<1: n['industrial_complex']=1
    n['arms_factory']=mil; n['dockyard']=dock
    need0=sum(n[k]*WRK[k] for k in ('agriculture_district','industrial_complex','offices'))
    if sum(n[k] for k in comp_)==0 and Wn>0.03: n['industrial_complex']=1; need0=WRK['industrial_complex']
    m=0.0
    if need0>0: m=max(-0.85,min(avail/need0-1,mmax))
    it=0
    while need0>0 and (Wn-need0*(1+m))/W>U_TARGET+0.06 and it<60 and Wn>0.03:
        n['industrial_complex']+=1; need0+=WRK['industrial_complex']; it+=1
        m=max(-0.85,min(avail/need0-1,mmax))
    m=round(m,2)
    need0+= (mil+dock)*0.0188
    capped=mode; scaled=False
    employed=(need0-(mil+dock)*0.0188)*(1+m)+(mil+dock)*0.0188
    unemp=max(Wn-employed,0)/W if W else 0
    bval=sum(n[k]*VAL[k] for k in n)
    native=comp((bval+fixed)*mult(prod,t))
    return dict(tag=t,pop=P,prod=prod,T=T,gpc=gpc,n=n,m=m,unemp=unemp,native=native,cap=capped,scaled=scaled,v2000=v2000,base={k:base[k] for k in VAL},sub=aw/W if W else 0)
PLANS={t:plan(t) for t in C if t not in EXCLUDE}
if __name__=='__main__':
    for t in sorted(PLANS,key=lambda t:-PLANS[t]['T'])[:60]:
        p=PLANS[t];n=p['n'];b=p['base']
        print(f"{t} T{p['T']:7.0f} nat{p['native']:7.0f} prod{p['prod']:4.0f} civ{n['industrial_complex']:3d}/{b['industrial_complex']:.0f} mil{n['arms_factory']:3d}/{b['arms_factory']:.0f} dock{n['dockyard']:2d}/{b['dockyard']:.0f} off{n['offices']:3d}/{b['offices']:.0f} agr{n['agriculture_district']:3d}/{b['agriculture_district']:.0f} m{p['m']:.2f} u{p['unemp']*100:4.1f}% sub{p['sub']*100:3.0f}% {p['cap']}")
