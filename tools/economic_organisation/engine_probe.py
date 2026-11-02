# IMPERIA COLD WAR — Economic organisation isolated native-engine verification
import json
import argparse
import hashlib
import os
import shutil
import subprocess
import time
from pathlib import Path
from catalogue import ROOT, HERE, MARKER

GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUN = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/economic_organisation')/('native_'+str(time.time_ns()))
PROFILE = RUN/'profile'
SNAPSHOT = RUN/'snapshot'
OUT = ROOT/'docs/audits/economic_reforms_ui_20261027'

def freeze():
    SNAPSHOT.mkdir(parents=True)
    for name in ['common','events','history','interface','localisation','portraits','map']:
        source=ROOT/name
        for current,dirs,files in os.walk(source,followlinks=False):
            dirs[:]=[d for d in dirs if not (Path(current)/d).is_junction() and not (Path(current)/d).is_symlink()]
            destination=SNAPSHOT/name/Path(current).relative_to(source);destination.mkdir(parents=True,exist_ok=True)
            for filename in files:
                path=Path(current)/filename
                if not path.is_symlink():shutil.copy2(path,destination/filename)
    for entry in ROOT.iterdir():
        if entry.is_file() and entry.suffix in ('.txt','.mod','.lua'):shutil.copy2(entry,SNAPSHOT/entry.name)
    for name in ['gfx','music','sound']:
        subprocess.run(['cmd.exe','/c','mklink','/J',str(SNAPSHOT/name),str(ROOT/name)],check=True,capture_output=True)

def write(rel, source):
    path=PROFILE/rel;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(source,encoding='utf-8')

def assertion(condition,name):
    return f'if = {{ limit = {{ {condition} }} log = "ICW_ECON_ENGINE PASS {name}" }} else = {{ log = "ICW_ECON_ENGINE FAIL {name}" }}\n'

def main(core_only=False):
    until=time.monotonic()+60
    active=subprocess.run(['powershell','-NoProfile','-Command','Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    if active.stdout.strip():print(json.dumps({'waiting_for_user_to_close_hoi4':True,'maximum_seconds':60}),flush=True)
    while active.stdout.strip() and time.monotonic()<until:
        time.sleep(2)
        active=subprocess.run(['powershell','-NoProfile','-Command','Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not active.stdout.strip(),'HOI4 is already running. No second game was launched.'
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'engine_report.json').exists():
        index=1
        while (OUT/f'engine_attempt_{index}.json').exists():index+=1
        source=OUT/'engine_report.json';target=OUT/f'engine_attempt_{index}.json'
        assert source.resolve().parent==target.resolve().parent==OUT.resolve()
        source.rename(target)
    freeze()
    manifest=json.loads((ROOT/'docs/design/economic_organisation/implementation_manifest.json').read_text())
    hashes={rel:hashlib.sha256((SNAPSHOT/rel).read_bytes()).hexdigest() for rel in manifest['generated']}
    write('mod/mdcoldwar.mod',MARKER+' isolated frozen mod\n'+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+SNAPSHOT.as_posix()+'"\n')
    addon='name="IMPERIA COLD WAR economic organisation probe"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/economic_probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/economic_probe.mod'],'disabled_dlcs':[]}))
    write('settings.txt','language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/common/on_actions/zzzzzzzzz_ICW_probe.txt',MARKER+' isolated test hook\non_actions = { on_startup = { effect = { CUB = { icw_econ_probe_checks = yes } } } }\n')
    script=[MARKER+' diagnostic effects, isolated profile only','add_namespace = ICW_ECON_ENGINE','country_event = { id = ICW_ECON_ENGINE.1 hidden = yes is_triggered_only = yes immediate = {','log = "ICW_ECON_ENGINE START"']
    script.append(assertion('has_country_flag = icw_econ_initialized has_idea = icw_econ_command check_variable = { icw_econ_position = -80 }','cuban_initial_profile'))
    for tag,bop in [('SOV','COLDWAR_SOV_politburo_bop'),('GER','COLDWAR_GER_1970_deutschlandpolitik'),('DDR','COLDWAR_DDR_german_course_bop')]:
        script.append(tag+' = {')
        script.append(assertion('has_power_balance = { id = '+bop+' }','native_bop_'+tag+'_before'))
        script.append('set_variable = { icw_probe_original_bop = power_balance_value } set_variable = { icw_econ_position = 25 } icw_econ_refresh_tier = yes set_variable = { icw_probe_current_bop = power_balance_value }')
        script.append(assertion('has_power_balance = { id = '+bop+' } check_variable = { icw_probe_current_bop = icw_probe_original_bop }','native_bop_'+tag+'_unchanged'))
        script.append('}')
    script.append('set_variable = { icw_econ_position = 65 } set_variable = { globalism_value = 79.9 } icw_econ_refresh_tier = yes')
    script.append(assertion('NOT = { icw_econ_can_autonomy = yes } NOT = { icw_econ_can_privatisation = yes } NOT = { icw_econ_can_capital = yes }','globalisation_gate_below_80'))
    script.append('add_political_power = 2000 set_variable = { globalism_value = 80 }')
    script.append(assertion('icw_econ_can_autonomy = yes icw_econ_can_privatisation = yes icw_econ_can_capital = yes','globalisation_gate_at_80'))
    script.append('set_variable = { icw_econ_position = 10 } set_variable = { globalism_value = 62 } icw_econ_refresh_tier = yes set_variable = { icw_probe_expected_pp = political_power } subtract_from_variable = { icw_probe_expected_pp = 50 } icw_econ_start_privatisation = yes icw_econ_start_privatisation = yes icw_econ_start_ownership = yes')
    script.append(assertion('check_variable = { political_power = icw_probe_expected_pp } check_variable = { icw_econ_position = 10 } check_variable = { icw_econ_pending_position = 20 } check_variable = { icw_econ_days_remaining = 90 } check_variable = { icw_econ_cooldown_days = 180 }','single_payment_delayed_change'))
    script.append('for_loop_effect = { start = 0 end = 89 icw_econ_daily = yes }')
    script.append(assertion('has_country_flag = icw_econ_reform_active check_variable = { icw_econ_position = 10 } check_variable = { icw_econ_days_remaining = 1 }','day_89_not_applied'))
    script.append('icw_econ_daily = yes icw_econ_complete_reform = yes')
    script.append(assertion('NOT = { has_country_flag = icw_econ_reform_active } has_idea = icw_econ_regulated check_variable = { icw_econ_position = 20 } check_variable = { icw_econ_cooldown_days = 90 } check_variable = { political_power = icw_probe_expected_pp } check_variable = { globalism_value = 62 } check_variable = { gdp_total > 0 }','day_90_applied_once_preserves_globalisation'))
    script.append('for_loop_effect = { start = 0 end = 90 icw_econ_daily = yes } icw_econ_initialize = yes')
    script.append(assertion('icw_econ_can_ownership = yes check_variable = { icw_econ_position = 20 } check_variable = { icw_econ_cooldown_days = 0 }','day_180_and_initialize_idempotent'))
    for position,tier in [(-100,'command'),(-70,'planning'),(-40,'development'),(-15,'mixed'),(15,'regulated'),(40,'liberal'),(70,'laissez'),(100,'laissez')]:
        script.append(f'set_variable = {{ icw_econ_position = {position} }} icw_econ_refresh_tier = yes')
        script.append(assertion('has_idea = icw_econ_'+tier,'boundary_'+str(position).replace('-','minus')))
    script.append('set_variable = { icw_econ_position = 0 } icw_econ_refresh_tier = yes set_variable = { project_type = 1 } set_variable = { project = -1 } set_temp_variable = { local_state_modifier = 1 } set_temp_variable = { receiving_investment_duration_temp = 0 } calculate_project_duration = yes set_variable = { icw_probe_baseline_days = project_construction_duration^-2 } set_temp_variable = { receiving_investment_duration_temp = 0.2 } calculate_project_duration = yes')
    script.append('log = "ICW_ECON_ENGINE duration_positive baseline=[?icw_probe_baseline_days] days=[?project_construction_duration^-2] cost=[?building_cost] speed=[?construction_speed] factor=[?icw_investment_duration_factor] base_cost=[?global.build_const_cost_array^1]"')
    script.append(assertion('check_variable = { project_construction_duration^-2 > icw_probe_baseline_days }','positive_duration_slower'))
    script.append('set_temp_variable = { receiving_investment_duration_temp = -0.2 } calculate_project_duration = yes')
    script.append('log = "ICW_ECON_ENGINE duration_negative days=[?project_construction_duration^-2] cost=[?building_cost] factor=[?icw_investment_duration_factor]"')
    script.append(assertion('check_variable = { project_construction_duration^-2 < icw_probe_baseline_days } check_variable = { project_construction_duration^-2 > 0 }','negative_duration_faster'))
    # Original compact-concept values are independent expectations, not read back from the compiler catalogue.
    original={
        'command':(-80,{'total_workforce_modifier':.05,'production_factory_max_efficiency_factor':.10,'country_productivity_growth_modifier':-.20}),
        'planning':(-55,{'total_workforce_modifier':.03,'production_factory_max_efficiency_factor':.05,'country_productivity_growth_modifier':-.12}),
        'development':(-25,{'internal_investments_money_cost_modifier':-.05,'production_speed_industrial_complex_factor':.08,'bureaucracy_cost_multiplier_modifier':.05}),
        'mixed':(0,{'internal_investments_money_cost_modifier':-.02,'production_factory_efficiency_gain_factor':.03}),
        'regulated':(25,{'country_productivity_growth_modifier':.05,'production_speed_offices_factor':.05,'bureaucracy_cost_multiplier_modifier':.05}),
        'liberal':(55,{'country_productivity_growth_modifier':.10,'receiving_investment_duration_modifier':-.10,'internal_investments_money_cost_modifier':.10}),
        'laissez':(85,{'country_productivity_growth_modifier':.15,'return_on_investment_modifier':.01,'internal_investments_money_cost_modifier':.20}),
    }
    script.append('remove_ideas = { '+' '.join('icw_econ_'+slug for slug in original)+' }')
    for key in sorted({k for pos,mods in original.values() for k in mods}):
        script.append('set_variable = { icw_probe_base_'+key+' = modifier@'+key+' }')
    script.append('calculate_gdp = yes set_variable = { icw_probe_unplanned_workforce = workforce_total_display }')
    for slug,(position,mods) in original.items():
        script.append(f'set_variable = {{ icw_econ_position = {position} }} icw_econ_refresh_tier = yes')
        condition=[]
        for key,value in mods.items():
            script.append('set_variable = { icw_probe_actual_'+key+' = modifier@'+key+' } subtract_from_variable = { icw_probe_actual_'+key+' = icw_probe_base_'+key+' }')
            condition.append(f'check_variable = {{ icw_probe_actual_{key} > {value-.0001:.5f} }} check_variable = {{ icw_probe_actual_{key} < {value+.0001:.5f} }}')
        script.append(assertion(' '.join(condition),'original_package_'+slug))
        if slug in ('command','planning'):
            script.append('calculate_gdp = yes')
            script.append(assertion('check_variable = { workforce_total_display > icw_probe_unplanned_workforce }','available_workforce_increases_'+slug))
        if slug in ('command','regulated','laissez'):
            script.append('productivity_growth_country_display_effect = yes set_variable = { icw_probe_growth_expected = { value = modifier@productivity_growth_modifier multiply = 0.5 multiply = { value = 1 add = modifier@country_productivity_growth_modifier clamp = { min = 0 max = 100 } } } }')
            script.append(assertion('check_variable = { productivity_growth_scaled = icw_probe_growth_expected }','relative_productivity_reader_'+slug))
        if slug=='laissez':
            script.append('calculate_int_investments_rate = yes set_variable = { icw_probe_roi_expected = { value = 0.04 add = modifier@return_on_investment_modifier clamp = { min = 0 max = global.roi_rate_cap } } }')
            script.append(assertion('check_variable = { roi_rate = icw_probe_roi_expected }','annual_roi_reader'))
    script.append('set_variable = { icw_econ_position = 0 } icw_econ_refresh_tier = yes calculate_gdp = yes')
    script.append(assertion('check_variable = { workforce_total_display = icw_probe_unplanned_workforce }','workforce_removed_on_return_to_mixed'))
    script.append('set_variable = { icw_probe_base_western = modifier@democratic_drift } set_variable = { icw_probe_base_emerging = modifier@communism_drift }')
    for position,key,value in [(45,'western',.01),(85,'western',.02),(-55,'emerging',.01),(-80,'emerging',.02)]:
        modifier='democratic_drift' if key=='western' else 'communism_drift'
        script.append(f'set_variable = {{ icw_econ_position = {position} }} icw_econ_refresh_tier = yes set_variable = {{ icw_probe_support_delta = modifier@{modifier} }} subtract_from_variable = {{ icw_probe_support_delta = icw_probe_base_{key} }}')
        script.append(assertion(f'check_variable = {{ icw_probe_support_delta > {value-.0001:.5f} }} check_variable = {{ icw_probe_support_delta < {value+.0001:.5f} }}','support_'+key+'_'+str(position).replace('-','minus')))
    script.append('set_variable = { icw_econ_position = 20 } icw_econ_refresh_tier = yes set_variable = { icw_econ_market_high_water = 20 } set_variable = { icw_econ_cooldown_days = 0 } set_variable = { treasury = 10 } set_variable = { gdp_total = 100 } icw_econ_start_privatisation = yes icw_econ_start_privatisation = yes')
    script.append(assertion('check_variable = { treasury = 10 } check_variable = { icw_econ_pending_sale = 0.5 } has_country_flag = icw_econ_reform_active','sale_quote_no_early_payment'))
    script.append('set_variable = { gdp_total = 200 } icw_econ_complete_reform = yes icw_econ_complete_reform = yes')
    script.append(assertion('check_variable = { treasury = 10.5 } check_variable = { icw_econ_market_high_water = 30 } check_variable = { icw_econ_pending_sale = 0 }','sale_starting_quote_paid_once'))
    script.append('set_variable = { icw_econ_cooldown_days = 0 } icw_econ_start_ownership = yes icw_econ_complete_reform = yes set_variable = { icw_econ_cooldown_days = 0 } icw_econ_start_privatisation = yes')
    script.append(assertion('check_variable = { icw_econ_pending_sale = 0 }','sale_repeat_range_no_proceeds'))
    script.append('icw_econ_complete_reform = yes')
    script.append(assertion('check_variable = { treasury = 10.5 }','sale_reversal_cannot_mint_money'))
    script.append('set_variable = { icw_econ_position = 35 } set_variable = { icw_econ_selected_reform = 4 } icw_econ_refresh_tier = yes log = "ICW_ECON_ENGINE UI_TARGET=[icw_econ_selected_target_name]"')
    script.append('set_variable = { icw_econ_position = 0 } icw_econ_refresh_tier = yes')
    script.append('SOV = { puppet = CUB } set_variable = { icw_econ_cooldown_days = 0 } icw_econ_clear_request = yes set_variable = { icw_probe_pp_before_request = political_power } icw_econ_start_ownership = yes icw_econ_start_ownership = yes')
    script.append(assertion('is_subject_of = SOV has_country_flag = icw_econ_approval_pending NOT = { has_country_flag = icw_econ_reform_active } check_variable = { political_power = icw_probe_pp_before_request } check_variable = { icw_econ_position = 0 } check_variable = { icw_econ_cooldown_days = 0 }','subject_request_waits_without_payment'))
    script.append('country_event = { id = ICW_ECON_ENGINE.2 days = 2 } log = "ICW_ECON_ENGINE WAIT_FOR_APPROVAL_TIMER"')
    if core_only:
        index=next(i for i,line in enumerate(script) if line.startswith('SOV = { puppet = CUB }'))
        script=script[:index]+['log = "ICW_ECON_ENGINE COMPLETE"']
    write('fixture/common/scripted_effects/ICW_economic_probe.txt',MARKER+' isolated engine assertions\nicw_econ_probe_checks = {\n'+'\n'.join(script[3:])+'\n}\n')
    # Add observations to an otherwise identical fixture copy of the shipped approval events.
    approval=(ROOT/'events/ICW_economic_organisation.txt').read_text(encoding='utf-8')
    observer=assertion('original_tag = SOV date > 1970.1.2 date < 1970.1.3 event_target:icw_econ_applicant = { original_tag = CUB has_country_flag = icw_econ_approval_pending NOT = { has_country_flag = icw_econ_reform_active } }','approval_delivered_to_overlord_next_day')
    observer+='event_target:icw_econ_applicant = { set_variable = { icw_probe_expected_approval_pp = political_power } subtract_from_variable = { icw_probe_expected_approval_pp = 50 } }'
    approval=approval.replace('id = ICW_ECON_APPROVAL.1 title','id = ICW_ECON_APPROVAL.1 immediate = { '+observer+' } title',1)
    payment=assertion('check_variable = { political_power = icw_probe_expected_approval_pp } has_country_flag = icw_econ_reform_active','overlord_approval_charges_subject_once')
    approval=approval.replace('icw_econ_approve_ownership = yes','icw_econ_approve_ownership = yes add_to_variable = { icw_probe_approval_count = 1 } '+payment,1)
    write('fixture/events/ICW_economic_organisation.txt',approval)
    second=assertion('has_country_flag = icw_econ_reform_active NOT = { has_country_flag = icw_econ_approval_pending } check_variable = { icw_probe_approval_count = 1 } check_variable = { icw_econ_position = 0 } check_variable = { icw_econ_pending_position = -10 } check_variable = { icw_econ_days_remaining > 0 } check_variable = { icw_econ_days_remaining < 91 }','approved_reform_runs_after_wait')
    second+='clr_country_flag = icw_econ_reform_active set_variable = { icw_econ_cooldown_days = 0 } icw_econ_start_autonomy = yes set_variable = { icw_probe_decline_pp = political_power } SOV = { country_event = { id = ICW_ECON_ENGINE.3 } }'
    third='CUB = { icw_econ_decline_autonomy = yes icw_econ_approve_autonomy = yes '+assertion('NOT = { has_country_flag = icw_econ_approval_pending } NOT = { has_country_flag = icw_econ_reform_active } check_variable = { political_power = icw_probe_decline_pp } check_variable = { icw_econ_position = 0 } check_variable = { icw_econ_cooldown_days = 0 }','decline_and_replayed_acceptance_do_nothing')+' } log = "ICW_ECON_ENGINE COMPLETE"'
    write('fixture/events/ICW_economic_probe.txt',MARKER+' delayed engine assertions\nadd_namespace = ICW_ECON_ENGINE\ncountry_event = { id = ICW_ECON_ENGINE.2 hidden = yes is_triggered_only = yes immediate = { '+second+' } }\ncountry_event = { id = ICW_ECON_ENGINE.3 hidden = yes is_triggered_only = yes immediate = { '+third+' } }\n')
    for name in ['game.log','error.log']:
        path=PROFILE/'logs'/name
        if path.exists():path.write_text('',encoding='utf-8')
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=CUB','-start_speed='+('0' if core_only else '5'),'-hands_off']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    started=time.time();process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    write('process.json',json.dumps({'project':'IMPERIA COLD WAR','pid':process.pid,'args':args,'started':started},indent=2))
    print(json.dumps({'pid':process.pid,'profile':str(PROFILE)}),flush=True)
    logs='';errors=''
    try:
        while process.poll() is None and time.time()-started<900:
            time.sleep(1)
            path=PROFILE/'logs/game.log'
            logs=path.read_text(encoding='utf-8-sig',errors='replace') if path.exists() else ''
            if 'ICW_ECON_ENGINE COMPLETE' in logs:break
    finally:
        stopped=process.poll() is None
        if stopped:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    path=PROFILE/'logs/error.log'
    errors=path.read_text(encoding='utf-8-sig',errors='replace') if path.exists() else ''
    relevant=[l for l in errors.splitlines() if re_filter(l)]
    report={'project':'IMPERIA COLD WAR','profile':str(PROFILE),'feature_hashes':hashes,'core_only':core_only,'completed':'ICW_ECON_ENGINE COMPLETE' in logs,'checks':[l for l in logs.splitlines() if 'ICW_ECON_ENGINE' in l],'feature_errors':relevant,'all_error_lines':len(errors.splitlines()),'elapsed_seconds':round(time.time()-started,1),'returncode':process.returncode,'stopped_owned_process':stopped,'scope':'Frozen scripts and map on E:. Core mode verifies startup and forced native transactions while paused, excluding the forced new subject/calendar fixture. Not pointer interaction, natural 90-day progression or an actual save/reload.'}
    report['success']=report['completed'] and 'ICW_ECON_ENGINE FAIL' not in logs and not relevant
    (OUT/'engine_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['success'] else 1)

def re_filter(line):
    return any(k in line.lower() for k in ['icw_econ','icw_investment_duration_factor','economic organisation'])

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--core-only',action='store_true')
    main(core_only=parser.parse_args().core_only)
