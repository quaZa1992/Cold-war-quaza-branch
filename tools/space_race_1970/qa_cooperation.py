# IMPERIA COLD WAR — Execute native operational-contract transactions.
# COLDWAR 2025-cut: test fixtures use tier 6, the highest remaining OLV/GNSS/COMSAT/SPYSAT research.
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from qa_crew import setup, invite as crew_invite, economic
from cooperation import eligible, roles, field, order, ROLES, money, adjustment


def qualify(m,tag):
    g=m.countries[tag]
    g.flags.update('cw_sr_cap_'+s for s in ['space_administration','scientific_instruments','satellite_engineering','ground_tracking','deep_space_communications','orbital_flight','crewed_flight','launch_basic','heavy_lift'])
    g.technologies.update(['OLV6','GNSS6','COMSAT6','SPYSAT6'])


def invite(m,n,r,tag='DDR',train=True):
    m.c=m.countries['SOV'];m.put(field(n,'role'),r);m.put('cw_sr_crew_candidate',m.country_ids[tag]);qualify(m,tag)
    m.call(f'cw_sr_p{n}_op_invite')
    w=int(m.get(field(n,'order')));V.check(w in [1,2],f'No outbound order assigned: {n}/{r}')
    m.c=m.countries[tag];V.check(m.get(order(w,'status'))==1,'No actual invitation delivered')
    m.call(f'cw_sr_op_accept_{n}');V.check(m.get(order(w,'status'))==2,'Valid government consent rejected')
    if train:
        start=m.get('treasury')
        for _ in range(ROLES[r][1]):m.call('cw_sr_op_weekly')
        V.check(start-m.get('treasury')==V.D(ROLES[r][1])*V.D(ROLES[r][2]),'Qualification charges are not weekly funded work')
    m.c=m.countries['SOV'];return w


def launch(m,n):
    if 'fixedWindowStartMonth' in V.DATA['programmes'][n-1]:m.date='1984.12.1'
    m.rolls.append(0);m.call(f'cw_sr_p{n}_launch')
    V.check(m.get(f'cw_sr_p{n}_state')==4,'Cleared work package cannot depart '+str(n))


def run():
    count=0
    # Every eligible architecture/role must work with real native scopes. Clearing
    # each order after an attempt must not release other national commitments.
    for n,p in enumerate(V.DATA['programmes'],1):
        if not eligible(p):continue
        for r in roles(p):
            m,_=setup(n);w=invite(m,n,r)
            V.check(m.test(V.TRIGGERS[f'cw_sr_p{n}_operations_ready']),f'Qualified contract not ready {n}/{r}')
            start={tag:m.countries[tag].variables['treasury'] for tag in ['SOV','DDR']}
            net=V.D(f'{p["missionCostB"]+adjustment(p,r):.3f}');m.put('treasury',net)
            V.check(m.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']) if 'fixedWindowStartMonth' not in p else True,f'Net bill guard exceeds actual launch bill: {n}/{r}')
            launch(m,n);V.check(m.get('treasury')==0,'National net departure bill is incorrect')
            V.check(m.countries['DDR'].variables['treasury']-start['DDR']==V.D(f'{money(p,.35)-money(p,.30) if r==4 else -money(p,.10):.3f}'),'Partner contribution or procurement invoice incorrect')
            m.call(f'cw_sr_p{n}_failure');V.check(m.countries['DDR'].variables[order(w,'status')]==0,'Completed attempt retained foreign capacity')
            V.check(m.countries['DDR'].manpower==100000 and m.countries['DDR'].variables.get('cw_sr_fatalities',0)==0,'Ground partner suffered astronaut casualties')
            count+=1
    # Consent, real capabilities, peace and a free order are independent guards.
    m,p=setup(35);m.put(field(35,'role'),1);m.put('cw_sr_crew_candidate',m.country_ids['DDR'])
    m.countries['DDR'].flags.discard('cw_sr_cap_satellite_engineering');m.call('cw_sr_p35_op_invite')
    V.check(m.get(field(35,'country'))==0,'Unqualified instrument contractor accepted')
    qualify(m,'DDR');m.countries['DDR'].ai=True;m.call('cw_sr_p35_op_invite');V.check(m.get(field(35,'country'))==0,'AI operational participation accepted');m.countries['DDR'].ai=False
    m.wars.add(frozenset(('SOV','DDR')));m.call('cw_sr_p35_op_invite');V.check(m.get(field(35,'country'))==0,'Enemy operational participation accepted');m.wars.clear()
    w=invite(m,35,1,train=False);V.check(not m.test(V.TRIGGERS['cw_sr_p35_launch_allowed']),'Approval bypassed interface qualification')
    m.c=m.countries['DDR'];m.put('treasury',0);m.call('cw_sr_op_weekly');V.check(m.get(order(w,'weeks'))==0,'Unfunded qualification advanced')
    m.put('treasury',100)
    for _ in range(25):m.call('cw_sr_op_weekly')
    m.c=m.countries['SOV'];V.check(not m.test(V.TRIGGERS['cw_sr_p35_launch_allowed']),'Incomplete course cleared')
    m.c=m.countries['DDR'];m.call('cw_sr_op_weekly');m.put('treasury',0);m.c=m.countries['SOV'];V.check(not m.test(V.TRIGGERS['cw_sr_p35_launch_allowed']),'Unfunded departure contribution cleared')
    m.c=m.countries['DDR'];m.put('treasury',100);m.c.flags.discard('cw_sr_cap_scientific_instruments');m.c=m.countries['SOV'];V.check(not m.test(V.TRIGGERS['cw_sr_p35_operations_ready']),'Lost partner capability ignored');qualify(m,'DDR')
    # Country may support two different missions while training an astronaut.
    t,p=setup(35);w1=invite(t,35,1)
    t.put('cw_sr_p36_state',3);w2=invite(t,36,2,train=False);V.check(w1==1 and w2==2,'Second concurrent work order overwrote the first')
    t.put('cw_sr_p37_state',3);t.put('cw_sr_p37_op_role',3);t.call('cw_sr_p37_op_invite');V.check(t.get(field(37,'country'))==0,'Third foreign work order bypasses national coordination capacity')
    t.put('cw_sr_p27_state',3);t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p27_crew_invite1');V.check(t.get('cw_sr_p27_guest1_country')==t.country_ids['DDR'],'Work packages blocked independent astronaut assignment')
    t.c=t.countries['DDR'];t.call('cw_sr_op_withdraw2');V.check(t.get(order(1,'status'))==2 and t.get(order(2,'status'))==0,'Withdrawing one order cleared another');t.c=t.countries['SOV']
    # Stale windows retain their own serial and cannot accept a newer agreement.
    t,p=setup(35);qualify(t,'DDR');t.put(field(35,'role'),1);t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p35_op_invite');t.call('cw_sr_p35_op_remove');t.call('cw_sr_p35_op_invite')
    V.check(t.get(field(35,'country'))==0,'Unresolved old popup was overwritten')
    t.c=t.countries['DDR'];t.call('cw_sr_op_accept_35');V.check(t.get(order(1,'status'))==0,'Withdrawn old invitation accepted');t.call('cw_sr_op_decline_35');t.c=t.countries['SOV'];t.call('cw_sr_p35_op_invite');V.check(t.get(field(35,'country'))==t.country_ids['DDR'],'Old popup dismissal did not reopen invitation channel')
    t.c=t.countries['DDR']
    for _ in range(90):t.call('cw_sr_op_daily')
    t.call('cw_sr_op_accept_35');V.check(t.get(order(1,'status'))==0,'Expired agreement accepted')
    t.call('cw_sr_op_decline_35');V.check('cw_sr_op_invitation_open' not in t.c.flags,'Expired popup could not be dismissed')
    # A country cannot obtain both the astronaut and operational share of one flight.
    t,p=setup();crew_invite(t,27,1,'DDR');t.put(field(27,'role'),1);qualify(t,'DDR');t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p27_op_invite');V.check(t.get(field(27,'country'))==0,'One country took two reward roles in one mission')
    t,p=setup();invite(t,27,1);t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p27_crew_invite1');V.check(t.get('cw_sr_p27_guest1_country')==0,'Reverse order bypassed exclusive national participation')
    # All three partner shares come out of the same first-success/world-first pool.
    t,p=setup(15);crew_invite(t,15,1,'DDR');crew_invite(t,15,2,'POL');invite(t,15,1,'USA')
    start={tag:t.countries[tag].variables.get('cw_sr_prestige',0) for tag in t.countries};launch(t,15)
    frozen=economic(t);t.put('cw_sr_selected',36);t.call('cw_sr_op_remove');V.check(t.get(field(15,'country'))==t.country_ids['USA'],'UI removed a different inflight agreement')
    t.call('cw_sr_p15_op_remove');t.c=t.countries['USA'];t.call('cw_sr_op_withdraw1');V.check(t.get(order(1,'status'))==3,'Partner withdrew after departure');t.c=t.countries['SOV'];t.call('cw_sr_p15_success')
    ms=next(x for x in V.DATA['milestones'] if x['capability'] in p['grants']);pool=V.D(p['prestige']+ms['prestige'])
    for tag,share in [('SOV','.5'),('DDR','.2'),('POL','.2'),('USA','.1')]:V.check(t.countries[tag].variables.get('cw_sr_prestige',0)-start[tag]==pool*V.D(share),'Combined award pool multiplied or misallocated '+tag)
    V.check([x[2] for x in t.countries['SOV'].tech_bonuses]==['0.10'],'Host did not surrender operational world-first research share')
    V.check([x[2] for x in t.countries['USA'].tech_bonuses]==['0.02'],'Operational partner world-first research share incorrect')
    V.check('cw_sr_cap_orbital_station' not in t.countries['USA'].flags,'Contractor received operator flight qualification')
    # State changes after departure cannot modify the roster or frozen success odds.
    t,p=setup(35);invite(t,35,1);launch(t,35);op=t.get('cw_sr_p35_op');t.countries['DDR'].ai=True;t.call('cw_sr_refresh');V.check(t.get('cw_sr_p35_op')==op,'Contract view rerolled frozen objective chance')
    start=t.countries['DDR'].variables.get('cw_sr_prestige',0);t.call('cw_sr_p35_success');V.check(t.countries['DDR'].variables.get('cw_sr_prestige',0)==start and t.countries['DDR'].variables['cw_sr_op_pending_prestige']>0,'AI takeover received active awards or lost signed entitlement')
    t.c=t.countries['DDR'];t.c.ai=False;t.call('cw_sr_op_daily');paid=t.get('cw_sr_prestige');t.call('cw_sr_op_daily');V.check(t.get('cw_sr_prestige')==paid and t.get('cw_sr_op_pending_prestige')==0,'Escrow paid twice')
    # Operational partners never lose manpower when the host crew is killed.
    t,p=setup();invite(t,27,2);launch(t,27);t.put('cw_sr_p27_phase',1);t.call('cw_sr_p27_catastrophic');V.check(t.countries['DDR'].manpower==100000 and t.countries['SOV'].manpower==99997,'Ground personnel treated as flight crew')
    # Preview navigation is mechanically inert, and combined UI shares are exact.
    t,p=setup();crew_invite(t,27,1,'DDR');invite(t,27,1,'USA');t.call('cw_sr_refresh');V.check(t.get('cw_sr_crew_host_percent')==70 and t.get('cw_sr_crew_share_frame')==4,'Combined UI national share/bar is inaccurate')
    before=economic(t);t.call('cw_sr_refresh');t.call('cw_sr_refresh');V.check(economic(t)==before,'Read-only view changed financial or persistent gameplay state')
    t.put('cw_sr_selected',35);t.call('cw_sr_refresh');V.check(t.get('cw_sr_crew_host_percent')==100,'Uncrewed view inherited previous crew reward share')
    # IMPERIA COLD WAR — Concurrent reports carry static role text and native event country scopes.
    for n,p in enumerate(V.DATA['programmes'],1):
        if not eligible(p):continue
        for r in roles(p):
            for stage in [2,3,4,5,6]:
                ident=f'cw_sr_ops.{n*100+r*10+stage}';ev=V.EVENTS[ident]
                V.check(V.first(ev,'desc')==ident+'.d','Outcome event did not bind its own role-specific description')
    # A researched supplier is mandatory; neither cash nor a signed placeholder is technical qualification.
    t,p=setup(84);qualify(t,'DDR');t.countries['DDR'].technologies={'OLV1'};t.put(field(84,'role'),4);t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p84_op_invite')
    V.check(t.get(field(84,'country'))==0,'Obsolete foreign launcher accepted for a Mars expedition')
    t,p=setup(6);qualify(t,'DDR');t.countries['DDR'].technologies.discard('COMSAT6');t.put(field(6,'role'),1);t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p6_op_invite');V.check(t.get(field(6,'country'))==0,'Instrument supplier bypassed actual payload-family research')
    # Withdrawal and loss of diplomatic access release one signed order without refunds or progress awards.
    t,p=setup(35);w=invite(t,35,2);before=t.countries['DDR'].variables['treasury'];t.wars.add(frozenset(('SOV','DDR')));t.c=t.countries['DDR'];t.call('cw_sr_op_daily');V.check(t.get(order(w,'status'))==0 and t.get('treasury')==before,'Diplomatic rupture stranded capacity or refunded spent qualification');t.c=t.countries['SOV'];t.call('cw_sr_op_daily');V.check(t.get(field(35,'country'))==0,'Host retained a withdrawn foreign work package')
    report={'project':'IMPERIA COLD WAR','status':'passed','checks':V.CHECKS,'programme_role_transactions':count,'eligible_programmes':sum(eligible(p) for p in V.DATA['programmes']),'roles':len(ROLES),'concurrent_work_orders_per_country':2,'share_per_operational_partner':.10,'additional_random_draws':0,'in_game_tested':False}
    Path(__file__).with_name('cooperation_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
