# IMPERIA CW — Cold War: native readiness verification in an owned, unsaved test campaign.
from pathlib import Path
import argparse
import json
import subprocess
import time
import hashlib
from build import expand

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PROFILE=Path('C:/Users/sonyz/.codex/visualizations/2026/10/25/01a17278-9784-74c0-b852-08f09d128edf/readiness-runtime')
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')

def launch(hold=False,live_fixture=False,presentation=False):
    if (PROFILE/'process.json').exists():
        old=json.loads((PROFILE/'process.json').read_text())
        # A new probe must not silently replace a previously recorded process.
        tasks=subprocess.run(['tasklist','/FI',f'PID eq {old["pid"]}','/NH'],capture_output=True,text=True).stdout
        if str(old['pid']) in tasks:raise RuntimeError('Recorded probe is still running')
    write(PROFILE/'mod/mdcoldwar.mod',(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon='name="Cold War Readiness Verification"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write(PROFILE/'mod/probe.mod',addon)
    write(PROFILE/'fixture/descriptor.mod',addon)
    write(PROFILE/'dlc_load.json',json.dumps({'enabled_mods':['mod/mdcoldwar.mod','mod/probe.mod'],'disabled_dlcs':[]}))
    write(PROFILE/'settings.txt','language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\n')
    hook='# IMPERIA CW — Cold War: temporary native readiness verification.\non_actions = { on_startup = { effect = { USA = { country_event = { id = nr_probe.1 hours = 1 } } } } }\n'
    write(PROFILE/'fixture/common/on_actions/readiness_probe.txt',hook)
    fixture='''
add_namespace = nr_probe
country_event = { id = nr_probe.1 hidden = yes is_triggered_only = yes immediate = {
    log = "READINESS_PROBE START"
    add_ideas = { nuclear_power_off full_first_use }
    add_political_power = 500
    set_technology = { ICBM = 1 ICBM1 = 1 popup = no }
    add_equipment_to_stockpile = { type = nuclear_missile_equipment_1 amount = 1000 }
    set_variable = { gdp_per_capita = 36 }
    set_variable = { inflation_multiplier = 1 }
    COLDWAR_nr_init = yes
    log = "READINESS_PROBE stock=[?COLDWAR_nr_arsenal] cost=[?COLDWAR_nr_forces_weekly]"
    if = { limit = { check_variable = { COLDWAR_nr_arsenal > 999 } } log = "READINESS_PROBE PASS stock" }
    else = { log = "READINESS_PROBE FAIL stock" }
    COLDWAR_nr_order_level = { LEVEL = 3 }
    if = { limit = { check_variable = { COLDWAR_nr_build_days = 4 } check_variable = { COLDWAR_nr_level = 5 } }
        log = "READINESS_PROBE PASS order_lead_time"
    } else = { log = "READINESS_PROBE FAIL order_lead_time" }
    for_loop_effect = { end = 4 COLDWAR_nr_daily = yes }
    if = { limit = { check_variable = { COLDWAR_nr_level = 3 } COLDWAR_nr_tactical_ready = yes }
        log = "READINESS_PROBE PASS tactical_readiness"
    } else = { log = "READINESS_PROBE FAIL tactical_readiness" }
    SOV = {
        add_ideas = { nuclear_power_off full_first_use }
        set_technology = { ICBM = 1 ICBM1 = 1 popup = no }
        add_equipment_to_stockpile = { type = nuclear_missile_equipment_1 amount = 500 }
        COLDWAR_nr_init = yes
        USA = { COLDWAR_nr_begin_crisis = yes }
    }
    if = { limit = { COLDWAR_nr_pair_valid = yes }
        log = "READINESS_PROBE PASS bilateral_pair"
    } else = { log = "READINESS_PROBE FAIL bilateral_pair" }
    SOV = { USA = {
        COLDWAR_nr_send_offer = { KIND = 1 }
        set_variable = { COLDWAR_nr_accept_kind = 1 }
        COLDWAR_nr_finish_offer = { KIND = 1 }
    } }
    if = { limit = { has_country_flag = COLDWAR_nr_hotline SOV = { has_country_flag = COLDWAR_nr_hotline } }
        log = "READINESS_PROBE PASS bilateral_hotline"
    } else = { log = "READINESS_PROBE FAIL bilateral_hotline" }
    SOV = { USA = {
        set_variable = { COLDWAR_nr_offer_cd@PREV = global.num_days }
        log = "READINESS_PROBE standdown_before day=[?global.num_days] pair=[?COLDWAR_nr_opponent] serial=[?COLDWAR_nr_serial] cd=[?COLDWAR_nr_offer_cd@SOV] until=[?COLDWAR_nr_offer_until@SOV]"
        COLDWAR_nr_send_offer = { KIND = 2 }
        log = "READINESS_PROBE standdown_offer kind=[?COLDWAR_nr_offer_kind@SOV] until=[?COLDWAR_nr_offer_until@SOV] serial=[?COLDWAR_nr_offer_serial@SOV] own=[?COLDWAR_nr_offer_own_use@SOV] peer=[?COLDWAR_nr_offer_peer_use@SOV]"
        set_variable = { COLDWAR_nr_accept_kind = 2 }
        COLDWAR_nr_finish_offer = { KIND = 2 }
        log = "READINESS_PROBE standdown_after pair=[?COLDWAR_nr_opponent] level=[?COLDWAR_nr_level]"
        if = { limit = { has_country_flag = COLDWAR_nr_standdown } log = "READINESS_PROBE standdown_USA_flag_yes" } else = { log = "READINESS_PROBE standdown_USA_flag_no" }
        if = { limit = { has_variable = COLDWAR_nr_opponent } log = "READINESS_PROBE standdown_USA_variable_yes" } else = { log = "READINESS_PROBE standdown_USA_variable_no" }
    } }
    SOV = {
        log = "READINESS_PROBE standdown_SOV pair=[?COLDWAR_nr_opponent] level=[?COLDWAR_nr_level]"
        if = { limit = { has_country_flag = COLDWAR_nr_standdown } log = "READINESS_PROBE standdown_SOV_flag_yes" } else = { log = "READINESS_PROBE standdown_SOV_flag_no" }
        if = { limit = { has_variable = COLDWAR_nr_opponent } log = "READINESS_PROBE standdown_SOV_variable_yes" } else = { log = "READINESS_PROBE standdown_SOV_variable_no" }
    }
    if = { limit = { NOT = { has_variable = COLDWAR_nr_opponent } has_country_flag = COLDWAR_nr_standdown
        SOV = { NOT = { has_variable = COLDWAR_nr_opponent } has_country_flag = COLDWAR_nr_standdown }
    } log = "READINESS_PROBE PASS mutual_standdown" }
    else = { log = "READINESS_PROBE FAIL mutual_standdown" }
    COLDWAR_nr_start_civil = yes
    for_loop_effect = { end = 3 COLDWAR_nr_daily = yes }
    if = { limit = { has_country_flag = COLDWAR_nr_civil_active }
        log = "READINESS_PROBE PASS civil_preparation"
    } else = { log = "READINESS_PROBE FAIL civil_preparation" }
    set_variable = { COLDWAR_nr_level = 1 }
    COLDWAR_nr_refresh = yes
    set_temp_variable = { COLDWAR_nr_counterforce_fraction = 0.4 }
    set_temp_variable = { nr_probe_stock_before = num_equipment@nuclear_missile_equipment }
    COLDWAR_nr_counterforce_loss = yes
    log = "READINESS_PROBE counterforce before=[?nr_probe_stock_before] after=[?num_equipment@nuclear_missile_equipment] reserve=[?COLDWAR_nr_reserve_share]"
    set_temp_variable = { nr_probe_expected_stock = nr_probe_stock_before }
    multiply_temp_variable = { nr_probe_expected_stock = 0.8 }
    if = { limit = { check_variable = { num_equipment@nuclear_missile_equipment = nr_probe_expected_stock } }
        log = "READINESS_PROBE PASS counterforce_reserve"
    } else = { log = "READINESS_PROBE FAIL counterforce_reserve" }
    set_country_flag = COLDWAR_nr_open
    COLDWAR_nr_refresh = yes
    # IMPERIA CW — Cold War: reset only the owned fixture's earlier stand-down.
    clr_country_flag = COLDWAR_nr_standdown
    clear_variable = COLDWAR_nr_cooldown@SOV
    set_variable = { COLDWAR_nr_level = 1 }
    set_variable = { COLDWAR_nr_build_days = 0 }
    COLDWAR_nr_refresh = yes
    SOV = {
        clr_country_flag = COLDWAR_nr_standdown
        clear_variable = COLDWAR_nr_cooldown@USA
        USA = {
            COLDWAR_nr_begin_crisis = yes
            COLDWAR_nr_issue_ultimatum = yes
        }
    }
    if = { limit = { COLDWAR_nr_first_use_context = yes check_variable = { COLDWAR_nr_fu_partner = SOV.id } }
        log = "READINESS_PROBE PASS ultimatum_context"
    } else = { log = "READINESS_PROBE FAIL ultimatum_context" }
    if = { limit = { has_country_flag = COLDWAR_nr_fu_waiting check_variable = { COLDWAR_nr_fu_hours = 72 }
        NOT = { has_country_flag = COLDWAR_nr_fu_authorised } NOT = { has_war_with = SOV }
    } log = "READINESS_PROBE PASS initial_release_blocked" }
    else = { log = "READINESS_PROBE FAIL initial_release_blocked" }
    country_event = { id = nr_probe.2 hours = 4 }
} }
country_event = { id = nr_probe.2 hidden = yes is_triggered_only = yes immediate = {
    log = "READINESS_PROBE timer_native hours=[?COLDWAR_nr_fu_hours] partner=[?COLDWAR_nr_fu_partner] serial=[?COLDWAR_nr_serial] level=[?COLDWAR_nr_level]"
    if = { limit = { check_variable = { COLDWAR_nr_fu_hours < 72 } check_variable = { COLDWAR_nr_fu_hours > 67 } COLDWAR_nr_first_use_context = yes }
        log = "READINESS_PROBE PASS scheduled_hourly_tick"
    } else = { log = "READINESS_PROBE FAIL scheduled_hourly_tick" }
    # Restore the counter only in this unsaved fixture for a literal loop-bound check.
    set_variable = { COLDWAR_nr_fu_hours = 72 }
    for_loop_effect = { end = 71 COLDWAR_nr_advance_first_use = yes }
    log = "READINESS_PROBE timer_boundary hours=[?COLDWAR_nr_fu_hours] partner=[?COLDWAR_nr_fu_partner]"
    if = { limit = { has_country_flag = COLDWAR_nr_fu_waiting check_variable = { COLDWAR_nr_fu_hours = 1 }
        NOT = { has_country_flag = COLDWAR_nr_fu_authorised } NOT = { has_war_with = SOV }
    } log = "READINESS_PROBE PASS full_ultimatum_delay" }
    else = { log = "READINESS_PROBE FAIL full_ultimatum_delay" }
    COLDWAR_nr_advance_first_use = yes
    if = { limit = { has_country_flag = COLDWAR_nr_fu_authorised check_variable = { COLDWAR_nr_fu_hours = 168 }
        COLDWAR_nr_first_use_context = yes NOT = { has_war_with = SOV }
    } log = "READINESS_PROBE PASS release_window" }
    else = { log = "READINESS_PROBE FAIL release_window" }
    set_variable = { actor_country = USA.id }
    set_variable = { victim_country = SOV.id }
    COLDWAR_nr_resolve_peacetime_operation = yes
    if = { limit = { has_war_with = SOV has_country_flag = COLDWAR_nr_nuclear_aggressor }
        log = "READINESS_PROBE PASS first_use_opens_war"
    } else = { log = "READINESS_PROBE FAIL first_use_opens_war" }
    if = { limit = { SOV = { is_in_array = { array = COLDWAR_nr_aggressors value = USA.id } } }
        log = "READINESS_PROBE PASS attributed_first_use"
    } else = { log = "READINESS_PROBE FAIL attributed_first_use" }
    set_temp_variable = { nr_probe_tension_after = global.mdcw_cw_tension }
    COLDWAR_nr_resolve_peacetime_operation = yes
    if = { limit = { check_variable = { global.mdcw_cw_tension = nr_probe_tension_after } }
        log = "READINESS_PROBE PASS single_war_consequences"
    } else = { log = "READINESS_PROBE FAIL single_war_consequences" }
    COLDWAR_nr_refresh = yes
    log = "READINESS_PROBE COMPLETE"
} }
'''
    # IMPERIA CW — Cold War: optional visual scene, after all mechanical checks finish.
    if presentation:
        fixture=fixture.replace('log = "READINESS_PROBE COMPLETE"', '''log = "READINESS_PROBE COMPLETE"
    set_variable = { COLDWAR_nr_level = 5 }
    set_variable = { COLDWAR_nr_order = 1 }
    set_variable = { COLDWAR_nr_build_days = 8 }
    set_variable = { COLDWAR_nr_fatigue = 80 }
    COLDWAR_nr_refresh = yes
    log = "READINESS_PRESENTATION preparing: current=5 order=1 days=8"
''')
    fixture=expand(fixture.replace('COLDWAR_nr_','nr_')).replace('nr_','COLDWAR_nr_').replace('COLDWAR_nr_probe','nr_probe')
    fixture='# IMPERIA CW — Cold War: temporary native readiness verification.\n'+fixture
    write(PROFILE/'fixture/events/readiness_probe.txt',fixture)
    temporary=[]
    if live_fixture:
        if not hold:raise RuntimeError('The in-place fixture requires process ownership until cleanup')
        for rel,content in [('common/on_actions/zz_COLDWAR_readiness_verification.txt',hook),('events/zz_COLDWAR_readiness_verification.txt',fixture)]:
            path=ROOT/rel
            if path.exists():raise RuntimeError('Refusing to replace '+str(path))
            write(path,content);temporary.append((path,content))
    for name in ['game.log','error.log']:
        path=PROFILE/'logs'/name
        if path.exists():write(path,'')
    args=[str(GAME/'hoi4.exe'),'-debug','-noasserts','-assertsdialog=no','userdir='+PROFILE.as_posix()+'/', '-start_tag=USA','-start_speed=1']
    startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=1
    output=(PROFILE/'process_output.txt').open('w',encoding='utf-8')
    try:
        process=subprocess.Popen(args,cwd=GAME,startupinfo=startup,stdout=output,stderr=subprocess.STDOUT)
    except BaseException:
        for path,content in temporary:
            if path.read_text(encoding='utf-8')==content:path.unlink()
        raise
    info={'pid':process.pid,'launched_at':time.time(),'profile':str(PROFILE),'presentation_scene':presentation}
    write(PROFILE/'process.json',json.dumps(info))
    print(json.dumps(info),flush=True)
    try:
        if hold:
            (PROFILE/'release.txt').unlink(missing_ok=True)
            until=time.monotonic()+900
            while process.poll() is None and time.monotonic()<until:
                if (PROFILE/'release.txt').exists():break
                time.sleep(1)
            if process.poll() is None:process.terminate()
            print(json.dumps({'returncode':process.wait(timeout=20)}),flush=True)
    finally:
        for path,content in temporary:
            if path.exists() and path.read_text(encoding='utf-8')==content:path.unlink()

def report():
    logs=PROFILE/'logs'
    if not (logs/'game.log').exists():logs=Path.home()/'Documents/Paradox Interactive/Hearts of Iron IV/logs'
    game=(logs/'game.log').read_text(encoding='utf-8-sig',errors='replace') if (logs/'game.log').exists() else ''
    errors=(logs/'error.log').read_text(encoding='utf-8-sig',errors='replace') if (logs/'error.log').exists() else ''
    lines=errors.splitlines();relevant=[]
    for i,line in enumerate(lines):
        if any(x in line for x in ['COLDWAR_nr','COLDWAR_nuclear_readiness','COLDWAR_nuclear_escalation','cw_nuclear.','nr_probe']) and any(x in line.lower() for x in ['error','invalid','failed','archetype','does not exist','dynamic token','unknown promotion','unknown variable','unexpected token']):
            relevant.append(line)
    result={'completed':'READINESS_PROBE COMPLETE' in game,
        'checkpoints':[line for line in game.splitlines() if 'READINESS_PROBE' in line],
        'relevant_errors':list(dict.fromkeys(relevant))}
    expected=['stock','order_lead_time','tactical_readiness','bilateral_pair','bilateral_hotline','mutual_standdown','civil_preparation','counterforce_reserve',
              'ultimatum_context','initial_release_blocked','scheduled_hourly_tick','full_ultimatum_delay','release_window','first_use_opens_war','attributed_first_use','single_war_consequences']
    result['passed']=[name for name in expected if 'READINESS_PROBE PASS '+name in game]
    result['failed']=[line for line in result['checkpoints'] if 'READINESS_PROBE FAIL ' in line]
    info=json.loads((PROFILE/'process.json').read_text()) if (PROFILE/'process.json').exists() else {}
    result['fresh_log']=bool((logs/'game.log').exists() and (logs/'game.log').stat().st_mtime>=info.get('launched_at',float('inf')))
    result['success']=result['completed'] and result['fresh_log'] and len(result['passed'])==len(expected) and not result['failed'] and not result['relevant_errors']
    result['scope']='Native 1970 single-player fixture; no two-client multiplayer or network/OOS test.'
    result['timer_scope']='First hourly callback runs on the native clock; remaining countdown is advanced through the native timer helper. Raid outcome helper is invoked directly, without a live combat launch.'
    from build import FILES
    sources=set(FILES)|{'interface/COLDWAR_nuclear_readiness.gfx','localisation/english/COLDWAR_nuclear_readiness_l_english.yml',
        'common/raids/nuclear_raids.txt','common/scripted_effects/00_money_system.txt',
        'common/scripted_effects/mdcw_imperia_nuclear_effects.txt','common/scripted_triggers/01_raids_triggers.txt',
        'common/decisions/categories/99_SOV_decision_categories.txt','localisation/english/MD_money_l_english.yml'}
    result['source_sha256']={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in sorted(sources)}
    result['source_snapshot_scope']='Hashes captured at report generation; debug hot-reloads may postdate fixture execution.'
    write(HERE/'engine_report.json',json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--launch',action='store_true');parser.add_argument('--hold',action='store_true');parser.add_argument('--live-fixture',action='store_true');parser.add_argument('--presentation',action='store_true');args=parser.parse_args()
    launch(args.hold,args.live_fixture,args.presentation) if args.launch else report()
