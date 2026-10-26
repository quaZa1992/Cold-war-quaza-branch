# IMPERIA CW — Cold War: iraq 1970 — engine runtime check.
"""Isolated native-engine probe. The temporary addon is never in the user playset.

Uses engine start_tag/hands_off arguments to attempt an unattended 1970 start.
The result reports actual reached checkpoints, not an assumed engine success.
"""
from pathlib import Path
import subprocess,json,time,hashlib,argparse
from common import ROOT,block,parse

V3_HEAVY_RECEIPT='COLDWAR_IRQ_reward_v3_industry_heavy_0'

HERE=Path(__file__).resolve().parent
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--early-assets',action='store_true',help='Targeted real-engine delivery check before unrelated world startup hooks; synthetic treasury/GDP only in the fixture.')
    args_cli=parser.parse_args()
    profile=HERE/('engine_asset_run' if args_cli.early_assets else 'engine_runtime_run');fixture=profile/'fixture';(profile/'mod').mkdir(parents=True,exist_ok=True)
    (profile/'.gitignore').write_text('*\n',encoding='utf-8')
    for path in ['common/on_actions','events']:(fixture/path).mkdir(parents=True,exist_ok=True)
    desc=(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n'
    (profile/'mod/mdcoldwar.mod').write_text(desc,encoding='utf-8')
    addon_desc='name="COLDWAR IRQ isolated runtime probe"\ndependencies={ "MD Cold War" }\npath="'+fixture.as_posix()+'"\n'
    (profile/'mod/irq_probe.mod').write_text(addon_desc,encoding='utf-8')
    (fixture/'descriptor.mod').write_text(addon_desc,encoding='utf-8')
    (profile/'dlc_load.json').write_text(json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/irq_probe.mod'],'disabled_dlcs':[]}),encoding='utf-8')
    (profile/'settings.txt').write_text('language="l_english"\ngraphics={ size={x=1280 y=720} fullScreen=no borderless=no }\nmaster_volume=0\n',encoding='utf-8')
    # The addon owns only these test hooks, which are absent from the installed
    # game profile. No automatic completion hook is added to the shipped mod.
    hook='''on_actions = { on_startup = { effect = {
 log = "COLDWAR_IRQ_ENGINE_PROBE global_startup reached"
 IRQ = {
 log = "COLDWAR_IRQ_ENGINE_PROBE startup reached"
 if = { limit = { COLDWAR_IRQ_campaign_active = yes } log = "COLDWAR_IRQ_ENGINE_PROBE PASS campaign" }
 else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL campaign" }
 country_event = { id = COLDWAR_IRQ_ENGINE_PROBE.1 hours = 1 }
} } } }'''
    (fixture/'common/on_actions/zzzz_COLDWAR_IRQ_engine_probe.txt').write_text(hook,encoding='utf-8')
    cards=['july_state','unsettled_north','ipc','rural','literacy','patronage','frontier']
    checks=''.join('has_idea = COLDWAR_IRQ_spirit_'+c+'\n' for c in cards)
    effect=block('if',block('limit',checks)+'log = "COLDWAR_IRQ_ENGINE_PROBE PASS seven_starting_cards"')+block('else','log = "COLDWAR_IRQ_ENGINE_PROBE FAIL seven_starting_cards"')
    effect+='''complete_national_focus = COLDWAR_IRQ_regional_command
if = { limit = {
 has_country_flag = COLDWAR_IRQ_regional_command_implemented
 has_country_flag = COLDWAR_IRQ_regional_command_package_earned
 check_variable = { COLDWAR_IRQ_baath_political_power_factor = 0.04 }
 has_dynamic_modifier = { modifier = COLDWAR_IRQ_baath_programme }
 } log = "COLDWAR_IRQ_ENGINE_PROBE PASS actual_focus_modifier" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL actual_focus_modifier" }
set_variable = { treasury = 1000 }
557 = { set_variable = { COLDWAR_IRQ_probe_civilian_before = building_level@industrial_complex } }
complete_national_focus = COLDWAR_IRQ_industry_heavy
if = { limit = {
 has_country_flag = COLDWAR_IRQ_industry_heavy_implemented
 has_country_flag = COLDWAR_IRQ_audit_reward_industry_heavy_building
 check_variable = { COLDWAR_IRQ_industry_production_factory_max_efficiency_factor = 0.10 }
 check_variable = { treasury < 1000 }
 } log = "COLDWAR_IRQ_ENGINE_PROBE PASS audited_heavy_programme" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL audited_heavy_programme" }
set_variable = { COLDWAR_IRQ_probe_paid_treasury = treasury }
COLDWAR_IRQ_apply_industry_heavy = yes
if = { limit = { check_variable = { var = treasury value = COLDWAR_IRQ_probe_paid_treasury compare = equals } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS audited_heavy_no_repayment" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL audited_heavy_no_repayment" }
set_temp_variable = { rul_party_temp = 4 }
set_temp_variable = { change_leader_temp = 1 }
set_temp_variable = { disable_elections = 1 }
change_ruling_party_effect = yes
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_IRQ_baath_programme } } NOT = { has_idea = COLDWAR_IRQ_spirit_july_state } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS party_departure" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL party_departure" }
set_temp_variable = { rul_party_temp = 21 }
set_temp_variable = { change_leader_temp = 1 }
set_temp_variable = { disable_elections = 1 }
change_ruling_party_effect = yes
COLDWAR_IRQ_reconcile_programmes = yes
COLDWAR_IRQ_reconcile_programmes = yes
if = { limit = { has_dynamic_modifier = { modifier = COLDWAR_IRQ_baath_programme } check_variable = { COLDWAR_IRQ_baath_political_power_factor = 0.04 } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS party_return_no_stacking" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL party_return_no_stacking" }
country_event = { id = COLDWAR_IRQ_ENGINE_PROBE.2 hours = 1 }
'''
    event='add_namespace = COLDWAR_IRQ_ENGINE_PROBE\n'+block('country_event','id = COLDWAR_IRQ_ENGINE_PROBE.1\nhidden = yes\nis_triggered_only = yes\n'+block('immediate',effect))
    # Read the actual target-state building level. The country-wide civilian
    # count also includes changing trade/subject contributions during startup.
    asset='''557 = {
set_variable = { COLDWAR_IRQ_probe_expected_civilians = COLDWAR_IRQ_probe_civilian_before }
add_to_variable = { COLDWAR_IRQ_probe_expected_civilians = 1 }
set_variable = { COLDWAR_IRQ_probe_civilian_after = building_level@industrial_complex }
log = "COLDWAR_IRQ_ENGINE_PROBE state_factory_counts before=[?COLDWAR_IRQ_probe_civilian_before] after=[?COLDWAR_IRQ_probe_civilian_after] expected=[?COLDWAR_IRQ_probe_expected_civilians]"
if = { limit = { check_variable = { var = COLDWAR_IRQ_probe_civilian_after value = COLDWAR_IRQ_probe_expected_civilians compare = equals } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS audited_one_actual_factory" }
else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL audited_one_actual_factory" }
}
log = "COLDWAR_IRQ_ENGINE_PROBE COMPLETE"
'''
    event+=block('country_event','id = COLDWAR_IRQ_ENGINE_PROBE.2\nhidden = yes\nis_triggered_only = yes\n'+block('immediate',asset))
    event=event.replace('COLDWAR_IRQ_audit_reward_industry_heavy_building',V3_HEAVY_RECEIPT)
    event=event.replace('COLDWAR_IRQ_baath_political_power_factor = 0.04','COLDWAR_IRQ_baath_political_power_factor = 0.08')
    (fixture/'events/COLDWAR_IRQ_engine_probe.txt').write_text(event,encoding='utf-8')
    if args_cli.early_assets:
        # Exact native state level, deliberately separated from the full-world
        # campaign check. No history/world initializer is suppressed or edited.
        early='''log = "COLDWAR_IRQ_ENGINE_PROBE early_asset_fixture"
IRQ = {
 if = { limit = { has_country_flag = MD_skip_treasury_cost } log = "COLDWAR_IRQ_ENGINE_PROBE startup_cost_skip_present" }
 clr_country_flag = MD_skip_treasury_cost
 set_variable = { gdp_total = 10 }
 set_variable = { treasury = 1000 }
 if = { limit = { COLDWAR_IRQ_campaign_active = yes } log = "COLDWAR_IRQ_ENGINE_PROBE target_campaign_active" }
 557 = {
 if = { limit = { is_owned_and_controlled_by = IRQ } log = "COLDWAR_IRQ_ENGINE_PROBE target_owner_valid" }
 if = { limit = { free_building_slots = { building = industrial_complex size > 0 include_locked = no } } log = "COLDWAR_IRQ_ENGINE_PROBE target_slot_valid" }
 }
 557 = { set_variable = { COLDWAR_IRQ_probe_civilian_before = building_level@industrial_complex } }
 COLDWAR_IRQ_apply_industry_heavy = yes
 log = "COLDWAR_IRQ_ENGINE_PROBE target_payment treasury=[?treasury] invoice=[?COLDWAR_IRQ_industry_heavy_invoice] credit=[?COLDWAR_IRQ_audit_reward_industry_heavy_building_credit]"
 if = { limit = { has_country_flag = COLDWAR_IRQ_industry_heavy_implemented has_country_flag = COLDWAR_IRQ_audit_reward_industry_heavy_building check_variable = { treasury = 999.5 } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS audited_heavy_programme" }
 else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL audited_heavy_programme" }
 COLDWAR_IRQ_apply_industry_heavy = yes
 if = { limit = { check_variable = { treasury = 999.5 } }
 log = "COLDWAR_IRQ_ENGINE_PROBE PASS audited_heavy_no_repayment" }
 else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL audited_heavy_no_repayment" }
}'''+'''IRQ = {
 set_country_flag = COLDWAR_IRQ_industry_maintenance_implemented
 171 = { set_variable = { COLDWAR_IRQ_probe_power_before = building_level@fossil_powerplant } }
 COLDWAR_IRQ_apply_industry_power = yes
 COLDWAR_IRQ_apply_industry_power = yes
 if = { limit = { has_country_flag = COLDWAR_IRQ_reward_v3_industry_power_0 check_variable = { treasury = 999 } }
  log = "COLDWAR_IRQ_ENGINE_PROBE PASS direct_power_payment_once" }
 else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL direct_power_payment_once" }
 171 = {
  set_variable = { COLDWAR_IRQ_probe_power_after = building_level@fossil_powerplant }
  subtract_from_variable = { COLDWAR_IRQ_probe_power_after = COLDWAR_IRQ_probe_power_before }
  if = { limit = { check_variable = { COLDWAR_IRQ_probe_power_after = 1 } }
   log = "COLDWAR_IRQ_ENGINE_PROBE PASS direct_one_actual_powerplant" }
  else = { log = "COLDWAR_IRQ_ENGINE_PROBE FAIL direct_one_actual_powerplant" }
 }
}
'''+block('IRQ',asset)
        early=early.replace('COLDWAR_IRQ_audit_reward_industry_heavy_building',V3_HEAVY_RECEIPT)
        (fixture/'common/on_actions/zzzz_COLDWAR_IRQ_engine_probe.txt').write_text('on_actions = {}\n',encoding='utf-8')
        (fixture/'common/on_actions/000_COLDWAR_IRQ_asset_probe.txt').write_text(block('on_actions',block('on_startup',block('effect',early))),encoding='utf-8')
    for path in [* (fixture/'common/on_actions').glob('*.txt'),* (fixture/'events').glob('*.txt')]:
        parse(path.read_text(encoding='utf-8'))
    dest=HERE/('ENGINE_ASSET_REPORT.json' if args_cli.early_assets else 'ENGINE_RUNTIME_REPORT.json')
    history=dest.with_name(dest.stem+'_ATTEMPTS.json')
    attempts=json.loads(history.read_text(encoding='utf-8')) if history.exists() else []
    if dest.exists():
        previous=json.loads(dest.read_text(encoding='utf-8'))
        if previous not in attempts:attempts.append(previous)
    history.write_text(json.dumps(attempts,indent=2)+'\n',encoding='utf-8')
    # A previous COMPLETE line must never terminate a new process before its
    # logger has opened the files. Only task-owned diagnostic logs are cleared.
    for name in ('game.log','error.log'):
        old_log=profile/'logs'/name
        if old_log.exists():old_log.write_text('',encoding='utf-8')
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    manifest_hash=hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest()
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(profile),'-start_tag=IRQ','-start_speed=1','-hands_off']
    started=time.time();p=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    print(json.dumps({'pid':p.pid,'profile':str(profile)}),flush=True)
    game_log=profile/'logs/game.log';errors_file=profile/'logs/error.log'
    # This full mod needs several minutes to finish loading the world after
    # parsing its databases; stopping at the menu misses on_startup entirely.
    try:
        while p.poll() is None and time.time()-started<600:
            time.sleep(1)
            if game_log.exists() and 'COLDWAR_IRQ_ENGINE_PROBE COMPLETE' in game_log.read_text(encoding='utf-8-sig',errors='replace'):break
    except KeyboardInterrupt:
        p.terminate();p.wait(timeout=10)
        raise
    stopped_by_probe=p.poll() is None
    if stopped_by_probe:p.terminate()
    try:p.wait(timeout=10)
    except subprocess.TimeoutExpired:p.kill();p.wait()
    logs=game_log.read_text(encoding='utf-8-sig',errors='replace') if game_log.exists() else ''
    errors=errors_file.read_text(encoding='utf-8-sig',errors='replace') if errors_file.exists() else ''
    checkpoint=[line for line in logs.splitlines() if 'COLDWAR_IRQ_ENGINE_PROBE' in line]
    scope='Targeted actual HOI4 native asset delivery before unrelated world startup; fixture GDP10/treasury1000; not a completed campaign startup' if args_cli.early_assets else 'Actual isolated HOI4 unattended runtime attempt; UI hover and multiplayer not tested'
    report={'scope':scope,'manifest_sha256':manifest_hash,'manifest_unchanged':hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest()==manifest_hash,'elapsed_seconds':round(time.time()-started,1),'completed':'COLDWAR_IRQ_ENGINE_PROBE COMPLETE' in logs,'checkpoints':checkpoint,'module_error_lines':[l for l in errors.splitlines() if 'COLDWAR_IRQ_' in l or 'COLDWAR_USA_gulf_' in l],'returncode':p.returncode}
    expected=['campaign','seven_starting_cards','actual_focus_modifier','audited_heavy_programme','audited_heavy_no_repayment','audited_one_actual_factory','party_departure','party_return_no_stacking']
    if args_cli.early_assets:expected=['audited_heavy_programme','audited_heavy_no_repayment','audited_one_actual_factory','direct_power_payment_once','direct_one_actual_powerplant']
    report['stopped_by_probe']=stopped_by_probe
    report['all_expected_checkpoints_pass']=all('COLDWAR_IRQ_ENGINE_PROBE PASS '+key in logs for key in expected) and 'COLDWAR_IRQ_ENGINE_PROBE FAIL' not in logs
    report['success']=report['completed'] and report['all_expected_checkpoints_pass'] and report['manifest_unchanged'] and not report['module_error_lines']
    dest.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
