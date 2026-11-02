# IMPERIA COLD WAR — Actual native Atlas and Mission Control navigation contracts.
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from mission_rules import REQUIREMENTS
import render_preview as R


def economic(m):
    fields=['treasury','cw_sr_prestige','cw_sr_science','cw_sr_fatalities','cw_sr_spent','cw_sr_budget']
    fields += [f'cw_sr_p{n}_{suffix}' for n in range(1,85) for suffix in ['state','work','months','spent','arrears','days','successes','launches','la','oa','im','ic','incident','fatalities']]
    return ([m.get(k) for k in fields],m.c.pp,m.c.manpower,deepcopy(m.c.tech_bonuses),len(m.events),len(m.rolls),deepcopy(m.c.flags))


def run():
    gui=V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'],'scripted_gui'),'cw_sr_main')
    callbacks={k:v for k,op,v in V.first(gui,'effects')};enabled={k:v for k,op,v in V.first(gui,'triggers') if k.endswith('_click_enabled')}
    def click(m,name):
        if name+'_click_enabled' in enabled:V.check(m.test(enabled[name+'_click_enabled']),'Disabled control '+name)
        m.run(callbacks[name+'_click'])
    for n,p in enumerate(V.DATA['programmes'],1):
        m=V.Machine(('SAU',));m.init();m.c.flags.add('cw_sr_open');m.put('cw_sr_selected',n);m.call('cw_sr_refresh')
        before=economic(m);click(m,'cw_sr_control_open')
        # Opening a view can dismiss menu flags but may not change campaign data.
        V.check(economic(m)==before,'Mission Control opening changed campaign state: '+p['id'])
        V.check(m.get('cw_sr_tab')==8 and m.get('cw_sr_selected')==n,'Control room lost the selected programme')
        V.check(m.get('cw_sr_control_missing')==len(REQUIREMENTS.get(p['id'],[])),'Incorrect outstanding precursor count')
        click(m,'cw_sr_control_stage_0');V.check(m.get('cw_sr_details_mode')==2 and 'cw_sr_requirements_open' in m.c.flags,'Research stage does not open real hardware requirements')
        click(m,'cw_sr_requirements_close');click(m,'cw_sr_control_risks');V.check(m.get('cw_sr_details_mode')==3,'Safety plan not routed')
        click(m,'cw_sr_requirements_close');click(m,'cw_sr_control_atlas');V.check(m.get('cw_sr_tab')==1,'Return to atlas failed')
        if p['id'] in REQUIREMENTS:
            before=economic(m);m.call('cw_sr_control_focus_requirement');m.call('cw_sr_refresh')
            V.check(m.get('cw_sr_control_parent')==n,'Expedition breadcrumb missing')
            target=int(m.get('cw_sr_selected'));first=REQUIREMENTS[p['id']][0];V.check(V.DATA['programmes'][target-1]['id'] in first,'Wrong missing precursor selected')
            V.check(economic(m)==before,'Reviewing a prerequisite paid for or completed a programme')
            click(m,'cw_sr_control_return');V.check(m.get('cw_sr_selected')==n and m.get('cw_sr_control_parent')==0,'Expedition breadcrumb did not return')
    # Prefer an in-progress alternative, preserve the top-level mission and clear
    # stale breadcrumbs when the player explicitly chooses a different programme.
    m=V.Machine(('SAU',));m.init();m.put('cw_sr_selected',84)
    ids={p['id']:i for i,p in enumerate(V.DATA['programmes'],1)}
    for group in REQUIREMENTS['mars-crewed-landing'][:-1]:m.c.flags.add('cw_sr_p'+str(ids[group[0]])+'_awarded')
    m.put('cw_sr_p43_state',2);m.call('cw_sr_refresh');m.call('cw_sr_control_focus_requirement');m.call('cw_sr_refresh')
    V.check(m.get('cw_sr_selected')==43 and m.get('cw_sr_control_parent')==84,'Started lunar alternative was ignored')
    m.put('cw_sr_selected',47);m.call('cw_sr_refresh');V.check(m.get('cw_sr_control_parent')==0,'Unrelated programme retained a stale expedition breadcrumb')
    # Readiness is derived from the same real technology gate used by launch.
    m=V.Machine(('SAU',));m.init();m.put('cw_sr_selected',6);m.put('cw_sr_p6_state',3);m.c.technologies.add('OLV1');m.call('cw_sr_refresh')
    V.check('Research required' in R.resolve('[CW_SR_Control_Research]',m),'Missing payload research shown as available')
    before=m.get('treasury');click(m,'cw_sr_primary_wait');V.check(m.get('cw_sr_tab')==8 and m.get('treasury')==before and not m.events,'Blocked mission button launched or failed to guide the player')
    m.c.technologies.add('COMSAT1');m.call('cw_sr_refresh');V.check('Available' in R.resolve('[CW_SR_Control_Research]',m),'Researched payload not reflected in Mission Control')
    # A loaded in-flight mission can be reviewed without rerolls or new rewards.
    m.put('cw_sr_p6_state',4);m.put('cw_sr_p6_days',4);before=economic(m)
    for _ in range(3):click(m,'cw_sr_control_open');click(m,'cw_sr_control_atlas')
    V.check(economic(m)==before,'Flight review changed frozen state or rolled a new incident')
    m.c.ai=True;before=deepcopy(m.c.variables);m.call('cw_sr_open_control');m.call('cw_sr_control_focus_requirement');m.call('cw_sr_control_return');V.check(m.c.variables==before,'AI entered player-only command room')
    report={'project':'IMPERIA COLD WAR','status':'passed','checks':V.CHECKS,'programmes':84,'navigation':'actual generated effects; no mission spending, progression, rewards or RNG','in_game_tested':False}
    Path(__file__).with_name('atlas_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
