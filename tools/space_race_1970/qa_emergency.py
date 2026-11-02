# IMPERIA COLD WAR — GC quarantine authority, complete shutdown and save persistence.
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from qa_crew import setup,invite as crew_invite
from qa_cooperation import invite as work_invite
from emergency import FLAG,EXEMPT


def snapshot(m):
    return deepcopy((m.countries,m.g,m.gf,m.targets,m.events,m.rolls))


def run():
    decision=V.first(V.first(V.ASTS['common/decisions/COLDWAR_space_race_emergency.txt'],'imp_gc_tools_decisions'),'cw_sr_gc_emergency_shutdown_decision')
    V.check(V.first(decision,'days_remove') is None and V.first(decision,'cost')=='0','Emergency shutdown is delayed or costs political power')
    for ai,gc in [(False,False),(True,True),(True,False)]:
        m=V.Machine(('SAU',));m.c.ai=ai
        if gc:m.c.ideas.add('imp_gc_nation')
        before=snapshot(m);m.run(V.first(decision,'complete_effect'));V.check(snapshot(m)==before,'Unauthorized country or AI activated the shutdown')
    m,p=setup();crew_invite(m,27,1,'DDR');work_invite(m,27,1,'USA')
    m.rolls.append(0);m.call('cw_sr_p27_launch');V.check(m.get('cw_sr_p27_state')==4,'Test joint flight did not depart')
    m.c.ideas.add('imp_gc_nation');m.c.flags.add('imp_gc_tools_show_perf_decisions');m.call('cw_sr_rank')
    for country in m.countries.values():
        country.dynamic_modifiers.update(['satellite_system','unrelated_nuclear_modifier'])
        country.flags.update(['cw_sr_open','space_auto_active','cw_sr_p1_deployed','cw_sr_crew_invitation_open','cw_sr_op_invitation_open'])
        country.variables.update({'space_prod_expense':V.D(4),'cw_sr_weekly_upkeep_m':V.D(10),'var_open_MD_space_gui':V.D(2)})
        country.missions.update([f'missile_construction_{i}' for i in range(10,15)]+['unrelated_military_mission'])
        country.arrays.update({'orbit_array':[V.D(141)],'missile_inventory_array':[V.D(7),V.D(8)],'payload_array':[V.D(161)]})
    m.put('cw_sr_p84_state',1);m.put('cw_sr_p84_work',33);m.put('cw_sr_p84_months',12);m.put('cw_sr_crew_pending_prestige',5);m.put('cw_sr_op_pending_prestige',7)
    historical={tag:deepcopy((c.variables['treasury'],c.pp,c.manpower,c.technologies,c.tech_bonuses,c.arrays)) for tag,c in m.countries.items()}
    V.check(m.test(V.first(decision,'visible')) and m.test(V.first(decision,'available')),'Human GC cannot access the emergency decision')
    m.run(V.first(decision,'complete_effect'))
    V.check(FLAG in m.gf,'Persistent campaign-wide kill flag absent')
    V.check(not m.test(V.first(decision,'available')),'Disabled system can be repeatedly shut down or re-enabled through its decision')
    for tag,c in m.countries.items():
        V.check(deepcopy((c.variables['treasury'],c.pp,c.manpower,c.technologies,c.tech_bonuses,c.arrays))==historical[tag],'Shutdown charged, refunded, killed personnel, removed research or corrupted military/orbital inventories: '+tag)
        V.check('satellite_system' not in c.dynamic_modifiers and 'unrelated_nuclear_modifier' in c.dynamic_modifiers,'Wrong passive modifiers removed')
        V.check(c.missions=={'unrelated_military_mission'},'Native orbital production not cancelled or ordinary military mission removed')
        V.check(not c.flags&{'cw_sr_open','space_auto_active','cw_sr_leader','cw_sr_p1_deployed','cw_sr_crew_invitation_open','cw_sr_op_invitation_open'},'An active space window, service or invitation survived')
        V.check(c.variables['space_prod_expense']==0 and c.variables['cw_sr_weekly_upkeep_m']==0,'Live space costs survived shutdown')
        V.check(c.variables['cw_sr_crew_status']==0 and c.variables['cw_sr_op_w1_status']==0 and c.variables['cw_sr_op_w2_status']==0,'Foreign assignments still reserve capacity')
    V.check(m.get('cw_sr_p84_work')==33 and m.get('cw_sr_p84_months')==12,'Historical engineering records were wiped')
    V.check(m.get('cw_sr_crew_pending_prestige')==0 and m.get('cw_sr_op_pending_prestige')==0,'Deferred award cache can still pay out')
    # Every generated entry point, including direct outcome/death/award effects,
    # must be inert. This is stronger than hiding normal command-room buttons.
    before=snapshot(m);guarded=V.MANIFEST['emergency_quarantine']['guarded_effects']
    for name in guarded:
        m.call(name);V.check(snapshot(m)==before,'Disabled generated effect still mutates state: '+name)
    for name in ['cw_sr_gc_emergency_shutdown','cw_sr_gc_quarantine_country']:
        m.call(name);V.check(snapshot(m)==before,'Emergency cleanup is not idempotent: '+name)
    for name in ['cw_sr_p27_start_allowed','cw_sr_p27_launch_allowed','cw_sr_p27_technology','cw_sr_p27_crew_ready','cw_sr_p27_operations_ready','cw_sr_p27_crew_invite1_allowed','cw_sr_p27_op_invite_allowed']:
        V.check(not m.test(V.TRIGGERS[name]),'A disabled programme still reports an allowed action: '+name)
    gui=V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'],'scripted_gui'),'cw_sr_main')
    V.check(not m.test(V.first(gui,'visible')),'Command room can still be opened')
    for name,_,body in V.first(gui,'effects'):
        m.run(body);V.check(snapshot(m)==before,'Stale command-room callback still acts: '+name)
    hooks=V.first(V.ASTS['common/on_actions/COLDWAR_space_race_on_actions.txt'],'on_actions')
    for name in ['on_startup','on_daily','on_weekly']:
        m.run(V.first(V.first(hooks,name),'effect'));V.check(snapshot(m)==before,'Disabled hook scans/initializes/advances the system: '+name)
    # A deep-copied save and a new human country must retain the same lockdown.
    loaded=deepcopy(m);loaded.c=loaded.countries['FRA'];loaded.c.ai=False
    loaded.c.flags.discard('cw_sr_initialized');loaded.call('cw_sr_initialize');loaded.call('cw_sr_daily')
    V.check(FLAG in loaded.gf and 'cw_sr_initialized' not in loaded.c.flags,'Load/hotjoin bypasses the emergency switch')
    # Inspect complete shared native GUIs, callbacks, production timeouts and
    # network services. Do not replace their military siblings with test stubs.
    native_gui=V.first(V.parse((V.ROOT/'common/scripted_guis/00_missiles_scripted_guis.txt').read_text(encoding='utf-8')),'scripted_gui')
    by_gui={name:body for name,_,body in native_gui};main=by_gui['MD_missiles_gui']
    for name in V.MANIFEST['emergency_quarantine']['native_guis']:
        V.check(not m.test(V.first(by_gui[name],'visible')),'Native space window remains visible: '+name)
        for callback,_,body in V.first(by_gui[name],'effects',[]):m.run(body);V.check(snapshot(m)==before,'Stale native orbital callback still acts: '+callback)
    triggers={k:v for k,_,v in V.first(main,'triggers')}
    for name in ['space_gui_ledger_button','icon_ledger_btn_1','antarctica_gui_ledger_button','icon_antarctica_gui_ledger']:
        V.check(not m.test(triggers[name+'_visible']),'Orbital ledger button/icon still visible: '+name)
    for callback in ['space_gui_ledger_button_click','antarctica_gui_ledger_button_click']:
        m.run(V.first(V.first(main,'effects'),callback));V.check(snapshot(m)==before,'Legacy ledger callback bypasses lockdown')
    production=V.first(V.parse((V.ROOT/'common/decisions/00_missile_decisions.txt').read_text(encoding='utf-8')),'missile_decisions')
    for i in range(10,15):
        mission=V.first(production,f'missile_construction_{i}');V.check(m.test(V.first(mission,'cancel_trigger')),'Native orbital mission does not cancel under lockdown')
        m.run(V.first(mission,'timeout_effect'));V.check(snapshot(m)==before,'Delayed production completion delivers hardware or settles a bill')
    for path in ['common/scripted_effects/00_missiles_scripted_effects.txt','common/scripted_effects/00_space_automation_effects.txt','common/scripted_effects/01_international_systems_effects.txt']:
        for name,_,body in V.parse((V.ROOT/path).read_text(encoding='utf-8')):
            if name in V.MANIFEST['emergency_quarantine']['native_effects']:V.EFFECTS[name]=body
    for name in V.MANIFEST['emergency_quarantine']['native_effects']:
        m.call(name);V.check(snapshot(m)==before,'Native orbital effect is not quarantined: '+name)
    m.put('space_prod_expense',99);m.call('space_prod_weekly_expense');V.check(m.get('space_prod_expense')==0,'Cached production expense still enters the money system')
    native_triggers=V.parse((V.ROOT/'common/scripted_triggers/00_special_projects_triggers.txt').read_text(encoding='utf-8'))
    for name in ['has_completed_space_program','has_completed_space_weapons']:
        V.check(not m.test(V.first(native_triggers,name)),'Native project access bypasses lockdown')
    native_fx=V.parse((V.ROOT/'common/scripted_effects/00_missiles_scripted_effects.txt').read_text(encoding='utf-8'))
    for name in ['nuclear_reactor_fuel_consumption','add_missile_building_level','update_missile_satellite_inventory']:
        V.check(FLAG not in str(V.first(native_fx,name)),'Ordinary nuclear/missile/inheritance function was disabled')
    for ident,body in V.EVENTS.items():V.check(not m.test(V.first(body,'trigger')),'Queued event still passes its delivery guard: '+ident)
    info=V.MANIFEST['emergency_quarantine']
    report={'project':'IMPERIA COLD WAR','feature':'GC emergency space quarantine','status':'passed','checks':V.CHECKS,'generated_effects_blocked':len(guarded),'native_effects_blocked':len(info['native_effects']),'native_windows_blocked':len(info['native_guis']),'event_delivery_guards':info['guarded_events'],'orbital_production_missions_cancelled':5,'campaign_persistent':True,'reversible':False,'historical_research_and_inventories_retained':True,'refunds_or_new_casualties':False,'live_game_tested':False,'multiplayer_tested':False}
    Path(__file__).with_name('emergency_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
