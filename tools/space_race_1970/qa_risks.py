# IMPERIA COLD WAR — qa risks validation.
# COLDWAR 2025-cut: test fixtures use tier 6, the highest remaining OLV/GNSS/COMSAT/SPYSAT research.
import json
from copy import deepcopy
from pathlib import Path
import validate as V
from mission_rules import REQUIREMENTS
from risk_rules import profile


def ready(n):
    m=V.Machine(('SAU','USA') if n==50 else ('SAU',));m.init();p=V.DATA['programmes'][n-1]
    m.date='1984.12.1' if 'fixedWindowStartMonth' in p else f'{max(1995,p["minYear"])}.12.1'
    m.g.update(cw_sr_window_mars=V.D(0),cw_sr_window_venus=V.D(0))
    m.c.flags.update('cw_sr_cap_'+x.replace('-','_') for x in p['capabilityRequirements'])
    ids={p['id']:i for i,p in enumerate(V.DATA['programmes'],1)}
    m.c.flags.update('cw_sr_p'+str(ids[group[0]])+'_awarded' for group in REQUIREMENTS.get(p['id'],[]))
    m.c.technologies.update(['OLV6','GNSS6','COMSAT6','SPYSAT6']);m.put(f'cw_sr_p{n}_state',3);m.put('cw_sr_selected',n);m.call('cw_sr_refresh')
    # IMPERIA COLD WAR — A purchased foreign launch has an actual consenting provider.
    if n==50:
        from qa_cooperation import qualify
        m.c=m.countries['USA'];m.init();qualify(m,'USA');m.c=m.countries['SAU'];m.put('cw_sr_p50_op_role',4);m.put('cw_sr_crew_candidate',m.country_ids['USA']);m.call('cw_sr_p50_op_invite')
        m.c=m.countries['USA'];m.call('cw_sr_op_accept_50')
        for _ in range(26):m.call('cw_sr_op_weekly')
        m.c=m.countries['SAU'];m.call('cw_sr_refresh');m.events.clear()
    return m


def run():
    flights=0
    for n,p in enumerate(V.DATA['programmes'],1):
        m=ready(n);r=profile(p);lp=m.get(f'cw_sr_p{n}_lp');op=m.get(f'cw_sr_p{n}_op')
        expected=(100-lp)*V.D(r['cat_l'])/100+lp*(100-op)*V.D(r['cat_o'])/10000
        V.check(abs(expected-m.get('cw_sr_view_risk_loss'))<V.D('.003'),'Displayed catastrophic exposure is inconsistent: '+p['id'])
        V.check(m.get('cw_sr_view_risk_crew')<=m.get('cw_sr_view_risk_loss'),'Crew risk exceeds hardware-loss risk')
        V.check(abs(lp*op/100-m.get('cw_sr_view_full'))<V.D('.002'),'Hidden third failure chance introduced')
        before=deepcopy(m.c.variables);m.call('cw_sr_refresh');V.check(m.c.variables==before and not m.events,'UI refresh changed a mission outcome')
        if p.get('commissioningOnly'):
            V.check(m.get('cw_sr_view_risk_anomaly')==0 and m.get('cw_sr_view_risk_crew')==0,'Ground facility acquired flight incidents or crew deaths');continue
        flights+=1
        # Successful departure, forced recoverable fault, single invoice/delay.
        m.rolls.append(0);m.call(f'cw_sr_p{n}_launch');V.check(m.get(f'cw_sr_p{n}_state')==4,'Prepared flight did not depart')
        frozen={k:v for k,v in m.c.variables.items() if k.startswith(f'cw_sr_p{n}_risk_')}
        m.put(f'cw_sr_p{n}_days',m.get(f'cw_sr_p{n}_incident_at'));days=m.get(f'cw_sr_p{n}_days');cash=m.get('treasury')
        m.rolls.append(0);m.call(f'cw_sr_p{n}_flight')
        V.check(m.get(f'cw_sr_p{n}_days')==days+r['delay']-1,'Anomaly did not extend the campaign')
        V.check(abs(cash-m.get('treasury')-V.D(r['cost']))<V.D('.002'),'Anomaly services were free or overcharged')
        V.check(m.get(f'cw_sr_p{n}_incident_checked')==1 and m.get(f'cw_sr_p{n}_incident')==1,'Safety checkpoint not recorded')
        V.check(m.get('cw_sr_fatalities')==0 and f'cw_sr_p{n}_awarded' not in m.c.flags,'Contained anomaly killed crew or qualified the flight')
        V.check(('country_event',f'cw_sr_report.{n*20+14}','SAU') in m.events,'Incident report missing')
        before=m.get('treasury');m.call(f'cw_sr_p{n}_flight');m.call('cw_sr_refresh');V.check(m.get('treasury')==before and not m.rolls,'Incident rerolled or charged twice')
        m.put('cw_sr_science',10000);m.put(f'cw_sr_p{n}_oa',4);m.call('cw_sr_refresh');V.check(all(m.get(k)==v for k,v in frozen.items()),'In-flight safety snapshot changed')
        m.put(f'cw_sr_p{n}_days',1);m.rolls.append(0);m.call(f'cw_sr_p{n}_flight');V.check(f'cw_sr_p{n}_awarded' in m.c.flags,'Contained fault made full success impossible')
        # Safe abort: no casualties, completion or awards, funded short review.
        a=ready(n);a.rolls.extend([9999,20]);a.call(f'cw_sr_p{n}_launch')
        V.check(a.get(f'cw_sr_p{n}_im')==1 and a.get('cw_sr_fatalities')==0,'Safe abort did not preserve the crew')
        V.check(f'cw_sr_p{n}_awarded' not in a.c.flags and not a.c.tech_bonuses,'Aborted mission earned success rewards')
        a.put('cw_sr_allocation',1000,True)
        for _ in range(8):a.call(f'cw_sr_p{n}_week')
        V.check(a.get(f'cw_sr_p{n}_state')==3 and a.get(f'cw_sr_p{n}_ic')==0,'Abort inspection did not finish with paid work')
    # Debt is retained, charged once on replenishment and prevents another launch.
    m=ready(84);m.rolls.append(0);m.call('cw_sr_p84_launch');m.put('treasury',0)
    m.put('cw_sr_p84_days',m.get('cw_sr_p84_incident_at'));m.rolls.append(0);m.call('cw_sr_p84_flight')
    V.check(m.get('cw_sr_p84_arrears')==V.D(profile(V.DATA['programmes'][83])['cost']) and m.get('treasury')==0,'Contingency invoice disappeared or created money')
    m.put('cw_sr_p84_days',1);m.rolls.append(0);m.call('cw_sr_p84_flight');m.put('treasury',1000)
    V.check(not m.test(V.TRIGGERS['cw_sr_p84_launch_allowed']),'Outstanding contingency bill did not block repeat flight')
    owed=m.get('cw_sr_p84_arrears');cash=m.get('treasury');m.c.flags.discard('cw_sr_p84_deployed');m.call('cw_sr_p84_upkeep')
    V.check(m.get('cw_sr_p84_arrears')==0 and cash-m.get('treasury')==owed,'Deferred invoice not paid exactly once')
    # More paid assurance/support experience lowers absolute exposure, never removes it.
    m=ready(84);old=m.get('cw_sr_view_risk_loss');incident=m.get('cw_sr_view_risk_anomaly');m.put('cw_sr_p84_la',2.5);m.put('cw_sr_p84_oa',4);m.put('cw_sr_p84_successes',3);m.call('cw_sr_refresh')
    V.check(0<m.get('cw_sr_view_risk_loss')<old and m.get('cw_sr_view_risk_anomaly')<incident,'Qualified experience does not improve safety')
    for n in [15,27,78,84]:
        m=ready(n);crew=V.DATA['programmes'][n-1]['crewSize'];national=V.DATA['programmes'][n-1].get('nationalCrewSize',crew)
        m.rolls.append(0);m.call(f'cw_sr_p{n}_launch');m.put(f'cw_sr_p{n}_days',1);m.rolls.extend([9999,0]);m.call(f'cw_sr_p{n}_flight')
        # IMPERIA COLD WAR — National casualty totals and total mission losses are distinct.
        V.check(m.get('cw_sr_fatalities')==national and m.get(f'cw_sr_p{n}_fatalities')==crew and m.c.manpower==100000-national,'Fatal accident attributed foreign crew to the national casualty total')
    m=ready(15);m.rolls.extend([9999,0]);m.call('cw_sr_p15_launch');V.check(m.get('cw_sr_fatalities')==0,'Uncrewed station launch killed a crew not aboard')
    for roll,months in [(30,3),(80,6)]:
        m=ready(84);m.rolls.append(0);m.call('cw_sr_p84_launch');m.put('cw_sr_p84_days',1);m.rolls.extend([9999,roll]);m.call('cw_sr_p84_flight')
        V.check(m.get('cw_sr_fatalities')==0 and m.get('cw_sr_p84_im')==months and 'cw_sr_p84_awarded' not in m.c.flags,'Survivable failure killed crew or qualified the Mars expedition')
    # A marginally severe failure can be fatal on Mars while remaining survivable
    # in a less exposed orbital architecture, matching each displayed risk profile.
    for n,expected in [(53,0),(84,6)]:
        m=ready(n);m.rolls.append(0);m.call(f'cw_sr_p{n}_launch');m.put(f'cw_sr_p{n}_days',1);m.rolls.extend([9999,10]);m.call(f'cw_sr_p{n}_flight')
        V.check(m.get('cw_sr_fatalities')==expected,'Mission-specific catastrophe share is not used at resolution')
    # Old flights do not acquire a new mid-flight roll after loading an existing save.
    m=V.Machine(('USA',));m.init();m.put('cw_sr_p84_state',4);m.put('cw_sr_p84_op',80);m.put('cw_sr_p84_days',1);m.rolls.extend([9999,6]);m.call('cw_sr_p84_flight')
    V.check(m.get('cw_sr_fatalities')==0 and m.get('cw_sr_p84_im')==3,'Legacy flight was silently upgraded to more lethal safety rules')
    for stage in [13,14]:
        m=ready(27);m.put('cw_sr_p27_last_report',stage);before=deepcopy(m.c.variables);money=m.get('treasury');m.call('cw_sr_replay_bulletin')
        V.check(m.get('treasury')==money and not m.rolls and not m.c.tech_bonuses,'Report replay applied incident costs or RNG')
    report={'project':'IMPERIA COLD WAR','checks':V.CHECKS,'status':'passed','programmes':84,'flight_checkpoints':flights,'risk_draws':'one checkpoint per flight; no UI RNG','in_game_tested':False}
    Path(__file__).with_name('risk_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
