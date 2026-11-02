# IMPERIA COLD WAR — private native SSR independence and programme probe.
"""Uses a separate user directory and addon; never changes user saves/playsets."""
from pathlib import Path
import hashlib,json,re,subprocess,time
import shared,lifecycle

ROOT=shared.ROOT
HERE=shared.HERE
PROFILE=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/ssr_1970/engine_profile')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PREFIX='COLDWAR_SSR_ENGINE'
EXPECTED=[]
EMBARGO_CHECKS={'native_embargo_exists','native_embargo_ended'}

def classify_capabilities(passed,failed,unrun,game,system):
    # This native action is a By Blood Alone feature. A process with no active
    # DLCs cannot exercise it; preserve raw verdicts and report explicit skips.
    unavailable=(PREFIX+' FEATURE native_embargo unavailable' in game or
                 re.search(r'Active DLC Count:\s*0\b',system) is not None)
    skipped=[]
    if unavailable:
        skipped=[{'check':name,'reason':'Native embargo requires By Blood Alone; that DLC is not active in the private engine process.'} for name in sorted(EMBARGO_CHECKS) if name in passed+failed+unrun]
    omitted={row['check'] for row in skipped}
    return ([n for n in passed if n not in omitted],[n for n in failed if n not in omitted],[n for n in unrun if n not in omitted],skipped)

def check(name,condition):
    EXPECTED.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}\n'

def event(index,body):
    return f'country_event = {{ id = {PREFIX}.{index} hidden = yes is_triggered_only = yes immediate = {{\n{body}\n}} }}\n'

def fixture():
    catalog=lifecycle.specialisation_catalog()
    selected={}
    for role in ('aircraft','agriculture'):
        selected[role]=next(v for v in catalog[role] if len(v['receipts'])==8 and any('_left' in r for r in v['receipts']) and any('_efficiency' in r for r in v['receipts']))
    air=selected['aircraft'];agri=selected['agriculture']
    models=shared.models()
    by={n['id']:n for n in models['UKR']['nodes']}
    first=check('ukraine_historical_ssr','COLDWAR_SSR_is_ssr = yes has_focus_tree = COLDWAR_SSR_1970_focus')
    first+='if = { limit = { has_dlc = "By Blood Alone" } log = "'+PREFIX+' FEATURE native_embargo available" } else = { log = "'+PREFIX+' FEATURE native_embargo unavailable" }\n'
    first+=check('foreign_country_not_ssr_participant','GER = { COLDWAR_SSR_is_participant = no }')
    first+='set_variable = { treasury = 10000 }\n'
    for identifier in sorted(air['receipts'],key=lambda i:by[i]['y']):
        first+='complete_national_focus = '+identifier+'\n'
    first+=check('aircraft_full_active','has_idea = '+air['full_idea']+' NOT = { has_idea = '+air['legacy_idea']+' }')
    first+=check('actual_aircraft_factory_receipt','has_country_flag = COLDWAR_SSR_special_aircraft_works_rewarded')
    first+='mdcw_load_1970_fallback_tree = yes\n'
    first+=check('fallback_preserves_authored_tree_and_progress','has_focus_tree = COLDWAR_SSR_1970_focus has_completed_focus = COLDWAR_SSR_special_aircraft_works')
    first+='set_variable = { SSR_ENGINE_saved_treasury = treasury }\nCOLDWAR_SSR_reward_special_aircraft_works = yes\n'
    first+=check('focus_reward_not_recharged','check_variable = { var = treasury value = SSR_ENGINE_saved_treasury compare = equals }')
    first+='set_variable = { ruling_party = 2 }\nCOLDWAR_SSR_reconcile = yes\n'
    first+=check('noncommunist_ssr_keeps_content','COLDWAR_SSR_is_ssr = yes has_idea = '+air['full_idea'])
    first+='set_variable = { ruling_party = 4 }\n'
    first+='UZB = {\nset_variable = { SSR_ENGINE_agri_baseline = modifier@agriculture_workers_modifier }\nset_variable = { SSR_ENGINE_district_baseline = modifier@agriculture_district_worker_requirement_modifier }\n'
    # This fixture simulates already-earned national development. Reconciliation
    # must never issue construction or research when those receipts are restored.
    first+='\n'.join('set_country_flag = '+identifier+'_rewarded' for identifier in agri['receipts'])+'\nCOLDWAR_SSR_reconcile = yes\n'
    first+=check('agriculture_full_active','has_idea = '+agri['full_idea'])
    first+='set_variable = { SSR_ENGINE_agri_expected = SSR_ENGINE_agri_baseline }\nadd_to_variable = { SSR_ENGINE_agri_expected = -0.2 }\nset_variable = { SSR_ENGINE_agri_actual = modifier@agriculture_workers_modifier }\n'
    first+=check('subsistence_workforce_reduced','check_variable = { var = SSR_ENGINE_agri_actual value = SSR_ENGINE_agri_expected compare = equals }')
    first+='set_variable = { SSR_ENGINE_district_expected = SSR_ENGINE_district_baseline }\nadd_to_variable = { SSR_ENGINE_district_expected = -0.25 }\nset_variable = { SSR_ENGINE_district_actual = modifier@agriculture_district_worker_requirement_modifier }\n'
    first+=check('district_workforce_reduced','check_variable = { var = SSR_ENGINE_district_actual value = SSR_ENGINE_district_expected compare = equals }')
    first+='}\nSOV = { set_autonomy = { target = UKR autonomy_state = autonomy_free } set_autonomy = { target = UZB autonomy_state = autonomy_free } set_autonomy = { target = BLR autonomy_state = autonomy_free } }\ncountry_event = { id = '+PREFIX+'.2 days = 1 }'

    def finish():
        return 'if = { limit = { UKR = { has_country_flag = SSR_ENGINE_lifecycle_done } BLR = { has_country_flag = SSR_ENGINE_diplomacy_done } UZB = { has_country_flag = SSR_ENGINE_market_done } } log = "'+PREFIX+' COMPLETE" }\n'

    second=check('ukraine_independent_recorded','COLDWAR_SSR_is_independent = yes')
    second+=check('automatic_aircraft_legacy','has_idea = '+air['legacy_idea']+' NOT = { has_idea = '+air['full_idea']+' }')
    second+=check('automatic_agriculture_legacy','UZB = { COLDWAR_SSR_is_independent = yes has_idea = '+agri['legacy_idea']+' NOT = { has_idea = '+agri['full_idea']+' } }')
    second+=check('transition_problems_created','has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_transition_broken_supply } has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_transition_state_accounts }')
    second+='BLR = { country_event = { id = '+PREFIX+'.20 } }\nUZB = { country_event = { id = '+PREFIX+'.30 } }\n'
    second+='set_country_flag = COLDWAR_SSR_UKR_p1_root_rewarded\nset_country_flag = COLDWAR_SSR_UKR_p2_root_rewarded\nset_variable = { ruling_party = 1 }\nCOLDWAR_SSR_reconcile = yes\n'
    second+=check('party_one_active','has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_1 } NOT = { has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_2 } }')
    second+='set_variable = { ruling_party = 2 }\nCOLDWAR_SSR_reconcile = yes\n'
    second+=check('same_outlook_party_programme_swapped','has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_2 } NOT = { has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_1 } }')
    second+='set_variable = { ruling_party = 4 }\ncomplete_national_focus = COLDWAR_SSR_payment_register\n'
    second+=check('independent_repair_receipt','has_country_flag = COLDWAR_SSR_payment_register_rewarded')
    second+='SOV = { puppet = UKR }\ncountry_event = { id = '+PREFIX+'.3 days = 1 }'
    third=check('rejoined_ssr_restores_full','COLDWAR_SSR_is_ssr = yes has_idea = '+air['full_idea']+' NOT = { has_idea = '+air['legacy_idea']+' }')
    third+=check('repair_receipt_survives_reentry','has_country_flag = COLDWAR_SSR_payment_register_rewarded has_country_flag = COLDWAR_SSR_lifecycle_transition_recorded')
    third+=check('independent_party_programmes_suspended','NOT = { has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_1 } } NOT = { has_dynamic_modifier = { modifier = COLDWAR_SSR_lifecycle_group_party_ukr_2 } }')
    third+='SOV = { set_autonomy = { target = UKR autonomy_state = autonomy_free } }\ncountry_event = { id = '+PREFIX+'.4 days = 1 }'
    fourth=check('second_exit_keeps_repairs_and_legacy','COLDWAR_SSR_is_independent = yes has_idea = '+air['legacy_idea']+' has_country_flag = COLDWAR_SSR_payment_register_rewarded')
    fourth+='set_country_flag = SSR_ENGINE_lifecycle_done\n'+finish()

    offer=check('belarus_independent_for_agreement','COLDWAR_SSR_is_independent = yes')
    offer+='GER = { set_variable = { treasury = 10000 } save_global_event_target_as = COLDWAR_SSR_dip_selected_partner }\nset_variable = { treasury = 10000 }\nCOLDWAR_SSR_dip_dispatch_technical = yes\n'
    offer+=check('actual_recipient_offer_pending','has_country_flag = COLDWAR_SSR_dip_technical_pending GER = { has_country_flag = COLDWAR_SSR_dip_in_technical_from_BLR_pending NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient } }')
    offer+='GER = { COLDWAR_SSR_dip_accept_technical_BLR = yes }\n'
    offer+=check('accepted_agreement_both_sides','has_idea = COLDWAR_SSR_diplomacy_technical_origin GER = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient }')
    offer+='if = { limit = { has_dlc = "By Blood Alone" } send_embargo = GER } else = { add_to_array = { imp_fin_sanc_by_us = GER } }\ncountry_event = { id = '+PREFIX+'.21 days = 1 }\n'
    embargo=check('native_embargo_exists','is_embargoing = GER')
    embargo+=check('daily_bilateral_restriction_suspends_both','NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_origin } GER = { NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient } }')
    embargo+='COLDWAR_SSR_diplomacy_refresh_budget = yes\nGER = { COLDWAR_SSR_diplomacy_refresh_budget = yes }\n'
    embargo+=check('suspended_agreement_costs_zero','check_variable = { COLDWAR_SSR_diplomacy_weekly_expense = 0 } GER = { check_variable = { COLDWAR_SSR_diplomacy_weekly_expense = 0 } }')
    embargo+='if = { limit = { has_dlc = "By Blood Alone" } break_embargo = GER } else = { remove_from_array = { imp_fin_sanc_by_us = GER } }\ncountry_event = { id = '+PREFIX+'.22 days = 1 }\n'
    restored=check('native_embargo_ended','NOT = { is_embargoing = GER }')
    restored+=check('daily_bilateral_restriction_restores_both','has_idea = COLDWAR_SSR_diplomacy_technical_origin GER = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient }')
    restored+='set_variable = { SSR_ENGINE_agreement_treasury = treasury }\nGER = { set_variable = { SSR_ENGINE_agreement_treasury = treasury } }\nCOLDWAR_SSR_diplomacy_reconcile = yes\nGER = { COLDWAR_SSR_diplomacy_reconcile = yes }\n'
    restored+=check('restoration_reconcile_no_setup_charge','check_variable = { var = treasury value = SSR_ENGINE_agreement_treasury compare = equals } GER = { check_variable = { var = treasury value = SSR_ENGINE_agreement_treasury compare = equals } }')
    restored+='GER = { add_to_array = { imp_eco_sanc_by_us = BLR } }\nCOLDWAR_SSR_diplomacy_refresh_budget = yes\nGER = { COLDWAR_SSR_diplomacy_refresh_budget = yes }\n'
    restored+=check('recipient_sanctions_suspend_both','NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_origin } GER = { NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient } }')
    restored+='GER = { remove_from_array = { imp_eco_sanc_by_us = BLR } }\nCOLDWAR_SSR_diplomacy_refresh_budget = yes\nGER = { COLDWAR_SSR_diplomacy_refresh_budget = yes }\n'
    restored+=check('sanction_end_restores_both','has_idea = COLDWAR_SSR_diplomacy_technical_origin GER = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient }')
    restored+='GER = { COLDWAR_SSR_dip_terminate_technical_BLR = yes }\n'
    restored+=check('recipient_termination_clears_both','NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_origin } NOT = { has_country_flag = COLDWAR_SSR_dip_technical_active } GER = { NOT = { has_idea = COLDWAR_SSR_diplomacy_technical_recipient } NOT = { has_country_flag = COLDWAR_SSR_dip_in_technical_from_BLR_active } }')
    restored+='set_country_flag = SSR_ENGINE_diplomacy_done\n'+finish()

    market='set_variable = { treasury = 10000 }\nCOLDWAR_SSR_start_market_shock = yes\nCOLDWAR_SSR_start_market_gradual = yes\n'
    market+=check('market_course_flags_set','has_country_flag = COLDWAR_SSR_market_course_started has_country_flag = COLDWAR_SSR_market_shock_started has_country_flag = COLDWAR_SSR_market_shock_deadline NOT = { has_country_flag = COLDWAR_SSR_market_gradual_started }')
    market+=check('market_course_once_only','has_dynamic_modifier = { modifier = COLDWAR_SSR_market_window_dynamic_modifier }')
    # Give this private fixture a guaranteed state-specific transaction asset.
    # Production decisions keep their real duration; only this timer is shortened.
    market+='capital_scope = { add_extra_state_shared_building_slots = 2 add_building_construction = { type = industrial_complex level = 2 instant_build = yes } save_global_event_target_as = SSR_ENGINE_liquidation_state set_state_flag = COLDWAR_SSR_market_selected_UZB set_variable = { SSR_ENGINE_expected_civs = building_level@industrial_complex } subtract_from_variable = { SSR_ENGINE_expected_civs = 1 } }\nset_country_flag = COLDWAR_SSR_market_pending_light_industry_liquidate\nset_country_flag = COLDWAR_SSR_market_pending_transaction\nset_country_flag = { flag = COLDWAR_SSR_market_pending_timer value = 1 days = 1 }\ncountry_event = { id = '+PREFIX+'.31 days = 2 }\n'
    settled=check('daily_settlement_completes_once','has_country_flag = COLDWAR_SSR_market_lot_light_industry_settled check_variable = { COLDWAR_SSR_market_lot_count = 1 } NOT = { has_country_flag = COLDWAR_SSR_market_pending_transaction }')
    settled+=check('liquidation_removes_one_actual_civ','event_target:SSR_ENGINE_liquidation_state = { check_variable = { var = building_level@industrial_complex value = SSR_ENGINE_expected_civs compare = equals } }')
    settled+='set_variable = { SSR_ENGINE_market_treasury = treasury }\nCOLDWAR_SSR_market_complete_light_industry_liquidate = yes\n'
    settled+=check('liquidation_cannot_pay_or_remove_twice','check_variable = { var = treasury value = SSR_ENGINE_market_treasury compare = equals } check_variable = { COLDWAR_SSR_market_lot_count = 1 } event_target:SSR_ENGINE_liquidation_state = { check_variable = { var = building_level@industrial_complex value = SSR_ENGINE_expected_civs compare = equals } }')
    settled+='set_country_flag = SSR_ENGINE_market_done\n'+finish()
    phases={1:first,2:second,3:third,4:fourth,20:offer,21:embargo,22:restored,30:market,31:settled}
    return shared.MARKER+'\nadd_namespace = '+PREFIX+'\n'+''.join(event(i,body) for i,body in phases.items())

def write(rel,text):
    path=PROFILE/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')

def main():
    output_paths=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))['outputs']
    input_hashes={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in output_paths}
    # The private addon overrides an immutable copy of every emitted game file.
    # A delayed external generator cannot hot-reload different tested inputs.
    native_paths=[path for path in output_paths if Path(path).suffix in {'.txt','.yml'}]
    for path in native_paths:
        target=PROFILE/'fixture'/path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes((ROOT/path).read_bytes())
    write('.gitignore',shared.MARKER+'\n*\n')
    write('mod/mdcoldwar.mod',shared.MARKER+'\n'+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon=shared.MARKER+'\nname="SSR native lifecycle probe"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/ssr_probe.mod',addon);write('fixture/descriptor.mod',addon)
    write('dlc_load.json',json.dumps(dict(enabled_mods=['mod/mdcoldwar.mod','mod/ssr_probe.mod'],disabled_dlcs=[])))
    write('settings.txt',shared.MARKER+'\nlanguage="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/events/'+PREFIX+'.txt',fixture())
    write('fixture/common/on_actions/zzzzzz_'+PREFIX+'.txt',shared.MARKER+'\non_actions = { on_startup = { effect = { UKR = { country_event = { id = '+PREFIX+'.1 } } } } }')
    for name in ('game.log','error.log'):write('logs/'+name,'')
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','-userdir='+str(PROFILE),'-start_tag=UKR','-start_speed=5','-hands_off']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
    started=time.monotonic();process=subprocess.Popen(args,cwd=GAME,startupinfo=startup)
    print(json.dumps(dict(project='IMPERIA COLD WAR',pid=process.pid,profile=str(PROFILE))),flush=True)
    try:
        while process.poll() is None and time.monotonic()-started<900:
            time.sleep(1)
            path=PROFILE/'logs/game.log'
            if path.exists() and PREFIX+' COMPLETE' in path.read_text(encoding='utf-8-sig',errors='replace'):break
    finally:
        if process.poll() is None:process.terminate()
        try:process.wait(timeout=10)
        except subprocess.TimeoutExpired:process.kill();process.wait()
    game=(PROFILE/'logs/game.log').read_text(encoding='utf-8-sig',errors='replace')
    errors=(PROFILE/'logs/error.log').read_text(encoding='utf-8-sig',errors='replace')
    records=re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)',errors)
    own=[row.strip() for row in records if 'COLDWAR_SSR' in row and 'Reloading Events:' not in row]
    passed=[name for name in EXPECTED if PREFIX+' PASS '+name in game]
    failed=[name for name in EXPECTED if PREFIX+' FAIL '+name in game]
    unrun=[name for name in EXPECTED if name not in passed+failed]
    raw_verdicts=dict(passed=passed.copy(),failed=failed.copy(),unrun=unrun.copy())
    system=(PROFILE/'logs/system.log').read_text(encoding='utf-8-sig',errors='replace')
    passed,failed,unrun,skipped=classify_capabilities(passed,failed,unrun,game,system)
    report=shared.baseline();report.update(passed=passed,failed=failed,unrun=unrun,ssr_errors=own,completed=PREFIX+' COMPLETE' in game,
       elapsed_seconds=round(time.monotonic()-started,1),scope='Private native 1970 scenario. Forced focus completion and real subject releases/re-entry across natural daily callbacks. No manual tooltip, save/reload or multiplayer claim.')
    report.update(raw_verdicts=raw_verdicts,skipped=skipped,all_optional_features_exercised=not skipped)
    report['tested_runtime_hashes']=input_hashes
    report['runtime_files_changed_during_test']=[path for path,digest in input_hashes.items() if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest]
    report['private_snapshot_changed_during_test']=[path for path in native_paths if hashlib.sha256((PROFILE/'fixture'/path).read_bytes()).hexdigest()!=input_hashes[path]]
    report['fixture_sha256']=hashlib.sha256((PROFILE/'fixture/events'/f'{PREFIX}.txt').read_bytes()).hexdigest()
    report['success']=report['completed'] and not failed and not unrun and not own and not report['runtime_files_changed_during_test'] and not report['private_snapshot_changed_during_test']
    (HERE/'ENGINE_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(dict(success=report['success'],passed=len(passed),failed=failed,unrun=unrun,skipped=len(skipped),ssr_error_count=len(own),ssr_error_sample=own[:4],completed=report['completed'],elapsed_seconds=report['elapsed_seconds'],report=str(HERE/'ENGINE_REPORT.json'))),flush=True)

if __name__=='__main__':main()
