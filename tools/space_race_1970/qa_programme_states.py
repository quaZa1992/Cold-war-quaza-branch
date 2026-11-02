# IMPERIA COLD WAR — Historical standings, actual programme states and once-only acceptance.
import json
from pathlib import Path
import validate as V
import render_preview as R
from historical_standings import BASES,established


def run():
    m=V.Machine(('USA','SOV','FRA','SAU'))
    for tag in ['USA','SOV','FRA']:m.countries[tag].ai=True
    m.c=m.countries['SAU'];m.init();m.call('cw_sr_rank')
    V.check([m.targets['cw_sr_rank'+str(i)].tag for i in [1,2,3]]==['USA','SOV','FRA'],'Historical top three absent with one human player')
    for tag,score in BASES.items():
        nation=m.countries[tag];V.check(nation.variables['cw_sr_prestige']==V.D(score) and 'cw_sr_initialized' not in nation.flags and 'cw_sr_leader' not in nation.flags,'AI received an active programme or leadership buff')
    m.call('cw_sr_seed_prestige');V.check(m.countries['USA'].variables['cw_sr_prestige']==100,'Historical baseline awarded twice')
    m.countries['USA'].variables['cw_sr_prestige']=V.D(9999);m.call('cw_sr_rank');V.check(m.g['cw_sr_score1']==100,'AI score advanced beyond its static historical entry')
    m.put('cw_sr_prestige',101);m.call('cw_sr_rank');V.check(m.targets['cw_sr_rank1'].tag=='SAU' and 'cw_sr_leader' in m.c.flags,'Human player cannot overtake historical entries')
    m.put('cw_sr_prestige',100);m.call('cw_sr_rank');V.check('cw_sr_leader' not in m.c.flags,'Tie against historical entry granted a unique-leader bonus')
    m.c=m.countries['FRA'];m.c.ai=False;m.init();V.check(m.get('cw_sr_prestige')==15,'Hotjoin duplicated historical prestige')
    V.check(m.get('cw_sr_p47_successes')==0 and 'cw_sr_p47_awarded' not in m.c.flags,'Historical institution invented a new campaign mission')
    V.check(not m.test(V.TRIGGERS['cw_sr_p47_start_allowed']),'Historically established commission can be developed again')
    for n,p in enumerate(V.DATA['programmes'],1):
        t=V.Machine(('SAU',));t.init();t.c.flags.add('cw_sr_open');t.put('cw_sr_selected',n);t.call('cw_sr_refresh')
        for state,label in [(1,'DEVELOPMENT'),(2,'SUSPENDED'),(4,'MISSION IN FLIGHT'),(6,'INVESTIGATION'),(7,'CANCELLED')]:
            t.put(f'cw_sr_p{n}_state',state);t.call('cw_sr_refresh');V.check(label in R.resolve('[CW_SR_ProgrammeState_'+str(n)+']',t),'Visible programme status differs from runtime')
            V.check(t.get(f'cw_sr_p{n}_ui_frame')=={1:3,2:1,4:3,6:5,7:1}[state],'Colour strip differs from the actual programme status')
        t.put(f'cw_sr_p{n}_state',5);t.c.flags.update([f'cw_sr_p{n}_awarded',f'cw_sr_p{n}_deployed']);t.call('cw_sr_refresh');V.check('COMPLETED' in R.resolve('[CW_SR_ProgrammeState_'+str(n)+']',t),'Accepted programme not marked completed')
        if p.get('commissioningOnly'):
            V.check(not t.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),'Operational one-time institution permits repeated acceptance')
            old=t.get('cw_sr_prestige');t.call(f'cw_sr_p{n}_success');V.check(t.get('cw_sr_prestige')==old,'Restored institution farms repeat prestige')
    for r in range(1,16):V.check(bool(R.LOC.get(f'cw_sr_region_caption_{r}')),'Map marker caption was erased by its transparent button')
    gui=V.first(V.first(V.ASTS['interface/COLDWAR_space_race.gui'],'guiTypes'),'containerWindowType')
    elements={V.first(v,'name').strip('"'):(k,v) for k,op,v in gui if isinstance(v,list) and V.first(v,'name')}
    for n in range(1,85):
        V.check(elements[f'cw_sr_card_state_{n}'][0]=='instantTextBoxType','Status still depends on multiline button rendering')
        V.check(V.first(elements[f'cw_sr_card_state_{n}'][1],'alwaysTransparent')=='yes','Status overlay intercepts card clicks')
    report={'project':'IMPERIA COLD WAR','checks':V.CHECKS,'status':'passed','programmes':84,'historical_prestige':BASES,'ai':'static historical entries only; no programmes or buffs','in_game_tested':False}
    Path(__file__).with_name('programme_states_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
