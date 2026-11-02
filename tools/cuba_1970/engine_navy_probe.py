# IMPERIA COLD WAR — Isolated native Cuba naval integration and reward probe.
"""Fresh private 1970 profile. No user playset, saves, or existing game is touched."""
from pathlib import Path
import json
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PROFILE = HERE/'runtime/navy_engine_profile'
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PREFIX = 'COLDWAR_CUB_NAVY_ENGINE'
EXPECTED = []


def write(rel, text):
    path = PROFILE/rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf8', newline='\n')


def check(name, condition):
    EXPECTED.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "{PREFIX} PASS {name}" }} else = {{ log = "{PREFIX} FAIL {name}" }}\n'


def fixture():
    text = '# IMPERIA COLD WAR — Private native naval reward checks in a CUB event ROOT.\n'
    text += 'add_namespace = '+PREFIX+'\ncountry_event = { id = '+PREFIX+'.1 hidden = yes is_triggered_only = yes immediate = {\n'
    text += check('authored_1970_tree', 'IMP_is_1970_scenario = yes has_focus_tree = COLDWAR_CUB_1970_focus')
    text += 'set_variable = { treasury = 30 }\ncomplete_national_focus = COLDWAR_CUB_GEN_naval_reform\n'
    text += check('naval_reform_executes', 'has_completed_focus = COLDWAR_CUB_GEN_naval_reform has_navy_experience > 74')
    text += 'complete_national_focus = COLDWAR_CUB_GEN_naval_bases\n'
    text += check('naval_base_exact_native_cost', 'has_completed_focus = COLDWAR_CUB_GEN_naval_bases check_variable = { treasury = 29.5 }')
    text += 'every_controlled_state = { if = { limit = { dockyard_random_build_loc = yes } log = "'+PREFIX+' ELIGIBLE [This.GetName]" } }\n'
    text += 'complete_national_focus = COLDWAR_CUB_GEN_dockyards\n'
    text += 'every_owned_state = { log = "'+PREFIX+' DOCKYARD [This.GetName] [?building_level@dockyard]" }\n'
    text += check('dockyards_constructed', 'has_completed_focus = COLDWAR_CUB_GEN_dockyards any_owned_state = { check_variable = { building_level@dockyard > 0 } }')
    text += 'complete_national_focus = COLDWAR_CUB_GEN_light_industry_investments\n'
    text += check('industry_feeder_executes', 'has_completed_focus = COLDWAR_CUB_GEN_light_industry_investments')
    text += 'clr_country_flag = COLDWAR_CUB_rural_clinics_applied\nclr_country_flag = COLDWAR_CUB_teaching_hospitals_applied\n'
    text += check('medical_missing_parents_blocks', 'COLDWAR_CUB_can_medical_brigades = no COLDWAR_CUB_can_retain_doctors = no')
    text += 'set_country_flag = COLDWAR_CUB_rural_clinics_applied\n'
    text += check('medical_clinic_parent_unlocks', 'COLDWAR_CUB_can_medical_brigades = yes COLDWAR_CUB_can_retain_doctors = yes')
    text += 'clr_country_flag = COLDWAR_CUB_rural_clinics_applied\nset_country_flag = COLDWAR_CUB_teaching_hospitals_applied\n'
    text += check('medical_hospital_parent_unlocks', 'COLDWAR_CUB_can_medical_brigades = yes COLDWAR_CUB_can_retain_doctors = yes')
    return text + 'log = "'+PREFIX+' COMPLETE"\n} }\n'


def main():
    write('.gitignore', '# IMPERIA COLD WAR — Private test profile.\n*\n')
    write('mod/mdcoldwar.mod', '# IMPERIA COLD WAR — Private reference to the active mod.\n'+(ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n')
    addon = '# IMPERIA COLD WAR — Private naval fixture.\nname="Cuba naval integration probe"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/navy_probe.mod', addon)
    write('fixture/descriptor.mod', addon)
    write('dlc_load.json', json.dumps(dict(enabled_mods=['mod/mdcoldwar.mod', 'mod/navy_probe.mod'], disabled_dlcs=[])))
    write('settings.txt', '# IMPERIA COLD WAR — Private muted window.\nlanguage="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/events/'+PREFIX+'.txt', fixture())
    write('fixture/common/on_actions/zzzzzz_'+PREFIX+'.txt', '# IMPERIA COLD WAR — Day-one event after native country initialization.\non_actions = { on_startup = { effect = { CUB = { country_event = { id = '+PREFIX+'.1 days = 1 } } } } }\n')
    for name in ('game.log', 'error.log'):
        write('logs/'+name, '')
    args = [str(GAME/'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir='+str(PROFILE), '-start_tag=CUB', '-start_speed=2', '-hands_off']
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.monotonic()
    process = subprocess.Popen(args, cwd=GAME, startupinfo=startup)
    print(json.dumps(dict(project='IMPERIA COLD WAR', pid=process.pid, profile=str(PROFILE))), flush=True)
    try:
        while process.poll() is None and time.monotonic()-started < 420:
            time.sleep(1)
            path = PROFILE/'logs/game.log'
            if path.exists() and PREFIX+' COMPLETE' in path.read_text(encoding='utf-8-sig', errors='replace'):
                break
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    game_log = (PROFILE/'logs/game.log').read_text(encoding='utf-8-sig', errors='replace')
    error_log = (PROFILE/'logs/error.log').read_text(encoding='utf-8-sig', errors='replace')
    records = re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)', error_log)
    errors = [row.strip() for row in records if 'COLDWAR_CUB' in row and 'Reloading Events:' not in row]
    passed = [key for key in EXPECTED if PREFIX+' PASS '+key in game_log]
    failed = [key for key in EXPECTED if key not in passed]
    report = dict(project='IMPERIA COLD WAR', passed=passed, failed=failed, cuba_errors=errors,
                  completed=PREFIX+' COMPLETE' in game_log, elapsed_seconds=round(time.monotonic()-started, 1),
                  scope='Fresh native 1970 CUB tree. Forced native focus completion tests rewards, not focus days or advanced availability. No manual UI, save/reload or multiplayer claim.')
    report['success'] = report['completed'] and not failed and not errors
    (HERE/'GENERIC_NAVY_ENGINE_REPORT.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
