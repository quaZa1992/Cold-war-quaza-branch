# IMPERIA CW — Cold War: isolated native-engine uranium integration probe.
from pathlib import Path
import argparse,json,subprocess,time
from port import ROOT,AUDIT,read,write
from adapt import block

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE=ROOT/'tools/quaza_nuclear_integration/runtime'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--hold-ui',action='store_true',help='Keep this isolated profile open until ui_release.txt contains done (up to 10 minutes).')
    options=parser.parse_args()
    # This profile is task-owned; the normal launcher playset is untouched.
    for folder in ['mod','fixture/common/on_actions','fixture/events']:(PROFILE/folder).mkdir(parents=True,exist_ok=True)
    write(PROFILE/'.gitignore','*\n')
    write(PROFILE/'mod/mdcoldwar.mod',read(ROOT/'descriptor.mod')+'\npath="'+ROOT.as_posix()+'"\n')
    addon='name="COLDWAR Uranium integration probe"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write(PROFILE/'mod/probe.mod',addon)
    write(PROFILE/'fixture/descriptor.mod',addon)
    write(PROFILE/'dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    height=900 if options.hold_ui else 720
    write(PROFILE/'settings.txt',f'language="l_english"\ngraphics={{size={{x=1280 y={height}}} fullScreen=no borderless=no}}\nmaster_volume=0\n')
    if options.hold_ui:write(PROFILE/'ui_release.txt','pending\n')
    # Resource exports include extraction bonuses and are refreshed by the
    # engine's simulation. Compare actual deltas after startup, rather than
    # asserting an unmodified raw deposit value during initialisation.
    hook='''# IMPERIA CW — Cold War: isolated probe after normal scenario initialisation.
on_actions = { on_startup = { effect = {
 log = "COLDWAR_URANIUM_ENGINE STARTUP"
 USA = { country_event = { id = COLDWAR_URANIUM_ENGINE.1 hours = 1 } }
} } }
'''
    events='''# IMPERIA CW — Cold War: isolated uranium regression events.
add_namespace = COLDWAR_URANIUM_ENGINE
country_event = { id = COLDWAR_URANIUM_ENGINE.1 hidden = yes is_triggered_only = yes immediate = {
 set_country_flag = { flag = imp_ai_uranium_mine_cooldown days = 90 }
 if = { limit = { NOT = { any_state = { has_resources_amount = { resource = uranium amount > 0 } } } }
  log = "COLDWAR_URANIUM_ENGINE PASS zero_initial_world_production" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL zero_initial_world_production" }
 789 = {
  set_variable = { COLDWAR_engine_before = resource@uranium }
  log = "COLDWAR_URANIUM_ENGINE baseline=[?resource@uranium]"
  set_building_level = { type = uranium_mine level = 1 instant_build = yes }
  PREV = { imp_uranium_update_mines = yes }
  log = "COLDWAR_URANIUM_ENGINE first_sync output=[?imp_uranium_mine_output] applied=[?imp_uranium_levels_applied] levels=[?imp_uranium_mine_levels] slots=[?imp_uranium_mine_slots] per=[?imp_uranium_per_level]"
 }
 country_event = { id = COLDWAR_URANIUM_ENGINE.2 hours = 1 }
} }
country_event = { id = COLDWAR_URANIUM_ENGINE.2 hidden = yes is_triggered_only = yes immediate = {
 789 = {
  set_variable = { COLDWAR_engine_after = resource@uranium }
  log = "COLDWAR_URANIUM_ENGINE after=[?resource@uranium] before=[?COLDWAR_engine_before]"
  if = { limit = { check_variable = { COLDWAR_engine_after > COLDWAR_engine_before } check_variable = { imp_uranium_mine_output = 6 } }
   log = "COLDWAR_URANIUM_ENGINE PASS mine_production" }
  else = { log = "COLDWAR_URANIUM_ENGINE FAIL mine_production" }
  PREV = { imp_uranium_update_mines = yes }
 }
 country_event = { id = COLDWAR_URANIUM_ENGINE.3 hours = 1 }
} }
country_event = { id = COLDWAR_URANIUM_ENGINE.3 hidden = yes is_triggered_only = yes immediate = {
 789 = {
  if = { limit = { check_variable = { resource@uranium = COLDWAR_engine_after } }
   log = "COLDWAR_URANIUM_ENGINE PASS no_duplicate_resources" }
  else = { log = "COLDWAR_URANIUM_ENGINE FAIL no_duplicate_resources" }
  damage_building = { type = uranium_mine damage = 1 }
  PREV = { imp_uranium_update_mines = yes }
 }
 country_event = { id = COLDWAR_URANIUM_ENGINE.4 hours = 1 }
} }
country_event = { id = COLDWAR_URANIUM_ENGINE.4 hidden = yes is_triggered_only = yes immediate = {
 789 = {
  log = "COLDWAR_URANIUM_ENGINE damaged=[?resource@uranium] output=[?imp_uranium_mine_output] applied=[?imp_uranium_levels_applied]"
  if = { limit = { check_variable = { resource@uranium < COLDWAR_engine_after } check_variable = { imp_uranium_mine_output = 0 } }
   log = "COLDWAR_URANIUM_ENGINE PASS damaged_mine" }
  else = { log = "COLDWAR_URANIUM_ENGINE FAIL damaged_mine" }
 }
 COLDWAR_refresh_enrichment_count = yes
 log = "COLDWAR_URANIUM_ENGINE enrichment=[?undamaged_enrichment_facilities]"
 COLDWAR_ENGINE_BUDGET_CHECKS
 log = "COLDWAR_URANIUM_ENGINE COMPLETE"
} }
'''
    # The rate helper receives explicit research-budget inputs; actual project
    # eligibility/lifecycle is exercised by test_integration.py. Reuse the live
    # defence-total statement and native update_display for accounting checks.
    money=read(ROOT/'common/scripted_effects/00_money_system.txt')
    n=block(money,'update_military_rate');military=money[n['start']:n['end']]
    n=block(military,'defence_gain')
    defence_total='set_variable = { '+military[n['start']:n['end']]+' }'
    checks='''
 update_military_rate = yes
 update_display = yes
 set_variable = { COLDWAR_engine_expense_before = display_expense }
 set_variable = { COLDWAR_engine_rate_before = treasury_rate }
 set_variable = { COLDWAR_engine_treasury_before = treasury }
 set_variable = { gdp_per_capita = 36 }
 set_temp_variable = { inflation_multiplier = 1 }
 set_temp_variable = { COLDWAR_nuclear_development_weekly_base = 0.15384 }
 COLDWAR_price_nuclear_development_budget = yes
 log = "COLDWAR_URANIUM_ENGINE bomb_weekly=[?COLDWAR_nuclear_development_weekly_cost]"
 if = { limit = { check_variable = { COLDWAR_nuclear_development_weekly_cost > 0.153 } check_variable = { COLDWAR_nuclear_development_weekly_cost < 0.155 } }
  log = "COLDWAR_URANIUM_ENGINE PASS bomb_budget" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL bomb_budget" }
 COLDWAR_ENGINE_DEFENCE_TOTAL
 update_display = yes
 set_variable = { COLDWAR_engine_expense_delta = { value = display_expense subtract = COLDWAR_engine_expense_before } }
 set_variable = { COLDWAR_engine_rate_delta = { value = COLDWAR_engine_rate_before subtract = treasury_rate } }
 if = { limit = { check_variable = { COLDWAR_engine_expense_delta > 0.153 } check_variable = { COLDWAR_engine_expense_delta < 0.155 } check_variable = { COLDWAR_engine_rate_delta > 0.153 } check_variable = { COLDWAR_engine_rate_delta < 0.155 } }
  log = "COLDWAR_URANIUM_ENGINE PASS budget_enters_treasury_rate" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL budget_enters_treasury_rate expense=[?COLDWAR_engine_expense_delta] rate=[?COLDWAR_engine_rate_delta]" }
 set_variable = { COLDWAR_engine_expense_after = display_expense }
 COLDWAR_price_nuclear_development_budget = yes
 COLDWAR_ENGINE_DEFENCE_TOTAL
 update_display = yes
 if = { limit = { check_variable = { display_expense = COLDWAR_engine_expense_after } check_variable = { treasury = COLDWAR_engine_treasury_before } }
  log = "COLDWAR_URANIUM_ENGINE PASS budget_refresh_no_double_charge" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL budget_refresh_no_double_charge" }
 set_temp_variable = { COLDWAR_nuclear_development_weekly_base = 0.09615 }
 COLDWAR_price_nuclear_development_budget = yes
 log = "COLDWAR_URANIUM_ENGINE warhead_weekly=[?COLDWAR_nuclear_development_weekly_cost]"
 if = { limit = { check_variable = { COLDWAR_nuclear_development_weekly_cost > 0.095 } check_variable = { COLDWAR_nuclear_development_weekly_cost < 0.097 } }
  log = "COLDWAR_URANIUM_ENGINE PASS warhead_budget" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL warhead_budget" }
 COLDWAR_calculate_nuclear_development_budget = yes
 COLDWAR_ENGINE_DEFENCE_TOTAL
 update_display = yes
 if = { limit = { check_variable = { COLDWAR_nuclear_development_weekly_cost = 0 } check_variable = { display_expense = COLDWAR_engine_expense_before } check_variable = { treasury_rate = COLDWAR_engine_rate_before } }
  log = "COLDWAR_URANIUM_ENGINE PASS inactive_budget_reset" }
 else = { log = "COLDWAR_URANIUM_ENGINE FAIL inactive_budget_reset" }
'''.replace('COLDWAR_ENGINE_DEFENCE_TOTAL',defence_total)
    events=events.replace('COLDWAR_ENGINE_BUDGET_CHECKS',checks)
    write(PROFILE/'fixture/events/COLDWAR_uranium_probe.txt',events)
    write(PROFILE/'fixture/common/on_actions/000_COLDWAR_uranium_probe.txt',hook)
    # Retain previous logs so a fresh run cannot be mistaken for an earlier one.
    previous_report=AUDIT/'engine_report.json'
    if previous_report.exists():write(AUDIT/'engine_report_before_performance.json',read(previous_report))
    for name in ['game.log','error.log']:
        p=PROFILE/'logs'/name
        if p.exists():write(p,'')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    # An interactive verification window must be visible; background probes remain hidden.
    startup.wShowWindow=1 if options.hold_ui else 0
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=USA','-start_speed=1','-hands_off']
    process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    print(json.dumps({'pid':process.pid,'profile':str(PROFILE)}),flush=True)
    start=time.time();game_log=PROFILE/'logs/game.log'
    while process.poll() is None and time.time()-start<(900 if options.hold_ui else 420):
        time.sleep(1)
        if game_log.exists() and 'COLDWAR_URANIUM_ENGINE COMPLETE' in read(game_log):break
    if options.hold_ui and process.poll() is None and game_log.exists() and 'COLDWAR_URANIUM_ENGINE COMPLETE' in read(game_log):
        print(json.dumps({'ui_ready_pid':process.pid,'release_file':str(PROFILE/'ui_release.txt')}),flush=True)
        until=time.monotonic()+600
        while process.poll() is None and time.monotonic()<until:
            if read(PROFILE/'ui_release.txt').strip()=='done':break
            time.sleep(1)
    stopped=process.poll() is None
    if stopped:process.terminate()
    try:process.wait(timeout=10)
    except subprocess.TimeoutExpired:process.kill();process.wait()
    logs=read(game_log) if game_log.exists() else ''
    errors=read(PROFILE/'logs/error.log') if (PROFILE/'logs/error.log').exists() else ''
    pertinent=[l for l in errors.splitlines() if any(t in l.lower() for t in ['uranium','coldwar_quaza','coldwar_nuclear','imp_raid','imp_ai_raid','launchable','country_resource_cost_uranium']) and 'Missing icon shine' not in l]
    report={'elapsed_seconds':round(time.time()-start,1),'returncode':process.returncode,'stopped_by_probe':stopped,
    'startup_reached':'COLDWAR_URANIUM_ENGINE STARTUP' in logs,
    'checkpoints':[l for l in logs.splitlines() if 'COLDWAR_URANIUM_ENGINE' in l],
    'relevant_errors':pertinent,'scope':'Native isolated-profile load, weekly mine reconciliation and explicit budget-input accounting checks; actual project start/cancel conditions are tested separately in the script model. No multiplayer or visual UI test.'}
    report['completed']='COLDWAR_URANIUM_ENGINE COMPLETE' in logs
    report['all_expected_checkpoints_pass']=all('COLDWAR_URANIUM_ENGINE PASS '+key in logs for key in ['zero_initial_world_production','mine_production','no_duplicate_resources','damaged_mine','bomb_budget','warhead_budget','budget_enters_treasury_rate','budget_refresh_no_double_charge','inactive_budget_reset'])
    report['success']=report['completed'] and report['all_expected_checkpoints_pass'] and 'COLDWAR_URANIUM_ENGINE FAIL' not in logs and not pertinent
    write(AUDIT/'engine_report.json',json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
