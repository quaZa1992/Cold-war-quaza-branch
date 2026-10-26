# IMPERIA CW — Cold War: real launch gates, reachable progression and modifier snapshots.
import json
from pathlib import Path
import validate as V
from mission_rules import REQUIREMENTS, HERITAGE


def run():
    ps=V.DATA['programmes'];ids={p['id']:i for i,p in enumerate(ps,1)}
    for ident,groups in REQUIREMENTS.items():
        n=ids[ident];p=ps[n-1];m=V.Machine(('SAU',));m.init();year=1984 if ident=='vega' else max(1995,p['minYear']);m.date=f'{year}.12.1';m.g.update(year=V.D(year),month=V.D(12),cw_sr_window_mars=V.D(0),cw_sr_window_venus=V.D(0))
        m.c.flags.update('cw_sr_cap_'+k.replace('-','_') for k in p['capabilityRequirements'])
        V.check(m.test(V.TRIGGERS[f'cw_sr_p{n}_start_allowed']),ident+' prevents parallel development before flight qualifications')
        m.put(f'cw_sr_p{n}_state',3);m.put(f'cw_sr_p{n}_work',100)
        V.check(not m.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),ident+' permits launch with no precursor successes')
        before=(m.get('treasury'),len(m.rolls),len(m.events));m.call(f'cw_sr_p{n}_launch')
        V.check(before==(m.get('treasury'),len(m.rolls),len(m.events)),ident+' direct launch bypasses precursor guards')
        receipts={'cw_sr_p'+str(ids[item])+'_awarded' for group in groups for item in group}
        m.c.flags.update(receipts)
        V.check(m.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),ident+' remains locked after all qualifications')
        for group in groups:
            missing={'cw_sr_p'+str(ids[item])+'_awarded' for item in group};m.c.flags.difference_update(missing)
            V.check(not m.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),ident+' ignores a required qualification')
            m.c.flags.update(missing)
        for group in groups:
            for item in group[1:]:m.c.flags.discard('cw_sr_p'+str(ids[item])+'_awarded')
        V.check(m.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),ident+' requires every alternative rather than one')
    # Failed, partial and catastrophic predecessor outcomes are never qualifications.
    for outcome in ['partial','failure','catastrophic']:
        m=V.Machine(('SAU',));m.init();m.call('cw_sr_p26_'+outcome)
        V.check('cw_sr_p26_awarded' not in m.c.flags,outcome+' predecessor qualified a major flight')
    # No free prestige, science, programme completion or deployed hardware from history.
    for tag,entries in HERITAGE.items():
        m=V.Machine((tag,));m.init();before=(m.get('cw_sr_prestige'),m.get('cw_sr_science'),m.c.pp,len(m.c.tech_bonuses));m.call('cw_sr_refresh');m.call('cw_sr_refresh')
        V.check(before==(m.get('cw_sr_prestige'),m.get('cw_sr_science'),m.c.pp,len(m.c.tech_bonuses)),'Historical qualification awards campaign rewards')
        for item in entries:
            V.check('cw_sr_heritage_'+str(ids[item]) in m.c.flags and 'cw_sr_p'+str(ids[item])+'_awarded' not in m.c.flags,'History was omitted or granted a new programme completion')
    # Reachability from a completely new national programme, including OR branches.
    for profile in V.DATA['profiles']:
        caps=set(profile.get('capabilities',[]));done=set(HERITAGE.get(profile['id'],()))
        for _ in range(85):
            old=(len(caps),len(done))
            for p in ps:
                if set(p['capabilityRequirements'])<=caps and all(set(group)&done for group in REQUIREMENTS.get(p['id'],[])):
                    done.add(p['id']);caps.update(p['grants'])
            if old==(len(caps),len(done)):break
        V.check(len(done)==84,'Unreachable programmes for '+profile['id']+': '+','.join(p['id'] for p in ps if p['id'] not in done))
    # Displayed components are the actual inputs and freeze with the departed flight.
    m=V.Machine(('SAU',));m.init();m.put('cw_sr_selected',35);m.put('cw_sr_science',50);m.c.flags.add('cw_sr_leader')
    m.put('cw_sr_p35_la',1.25);m.put('cw_sr_p35_oa',2.5);m.put('cw_sr_p35_successes',2);m.put('cw_sr_p35_corrective',1);m.put('cw_sr_p35_disruption',4)
    m.c.flags.add('cw_sr_p1_deployed');m.call('cw_sr_refresh')
    lp=m.get('cw_sr_view_base_l')+sum(m.get('cw_sr_view_mod_'+k+'_l') for k in ['paid','support','experience','disruption','corrective'])
    op=m.get('cw_sr_view_base_o')+sum(m.get('cw_sr_view_mod_'+k+'_o') for k in ['paid','support','experience','disruption','corrective'])+m.get('cw_sr_view_mod_analysis')+m.get('cw_sr_view_mod_leader')
    V.check(abs(m.get('cw_sr_view_launch')-lp)<V.D('.003') and abs(m.get('cw_sr_view_objective')-op)<V.D('.003'),'Visible probability components differ from actual inputs')
    frozen={k:v for k,v in m.c.variables.items() if k.startswith('cw_sr_p35_mod_')};m.put('cw_sr_p35_state',4);m.put('cw_sr_science',500);m.c.flags.discard('cw_sr_leader');m.call('cw_sr_refresh')
    V.check(all(m.get(k)==v for k,v in frozen.items()),'Departed mission modifier breakdown changed')
    legacy=V.Machine(('USA',));legacy.init();legacy.put('cw_sr_selected',35);legacy.put('cw_sr_p35_state',4);legacy.put('cw_sr_p35_lp',82.5);legacy.put('cw_sr_p35_op',80);legacy.put('cw_sr_p35_fp',66);legacy.call('cw_sr_refresh')
    V.check(legacy.get('cw_sr_view_mod_recorded')==0 and legacy.get('cw_sr_view_full')==66,'Legacy flight probabilities were reconstructed or presented as a recorded breakdown')
    # Removed header clutter must not return through regeneration.
    source=(V.ROOT/'interface/COLDWAR_space_race.gui').read_text(encoding='utf-8')
    for name in ['cw_sr_campaign','cw_sr_country_label','name = "cw_sr_country"','cw_sr_standings_note']:
        V.check(name not in source,'Removed header widget regenerated: '+name)
    result={'checks':V.CHECKS,'status':'passed','gated_programmes':len(REQUIREMENTS),'profiles_reachable':17,'historical_qualifications':'no campaign rewards','modifier_components':'actual calculation; frozen in flight','in_game_tested':False}
    Path(__file__).with_name('readiness_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':run()
