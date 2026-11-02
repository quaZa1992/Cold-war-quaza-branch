# IMPERIA COLD WAR — isolated native checks for nuclear intelligence integration.
from pathlib import Path
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE = Path(__file__).resolve().parent / 'runtime'


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')


def main():
    write(PROFILE / '.gitignore', '*\n')
    write(PROFILE / 'mod/mdcoldwar.mod', (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + f'\npath="{ROOT.as_posix()}"\n')
    addon = f'name="Nuclear intelligence probe"\ndependencies={{ "MD Cold War" }}\npath="{(PROFILE / "fixture").as_posix()}"\n'
    write(PROFILE / 'mod/probe.mod', addon)
    write(PROFILE / 'fixture/descriptor.mod', addon)
    write(PROFILE / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/mdcoldwar.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write(PROFILE / 'settings.txt', 'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write(PROFILE / 'fixture/common/ideas/COLDWAR_NI_probe.txt', '''# IMPERIA COLD WAR — isolated test idea.
ideas = { country = { COLDWAR_NI_probe_defense = { allowed = { always = yes } modifier = { intelligence_agency_defense = 2.5 } } } }
''')
    write(PROFILE / 'fixture/common/on_actions/000_COLDWAR_NI_probe.txt', '''# IMPERIA COLD WAR — isolated native test.
on_actions = { on_startup = { effect = { USA = { country_event = { id = COLDWAR_NI_PROBE.1 hours = 1 } } } } }
''')
    write(PROFILE / 'fixture/events/COLDWAR_NI_probe.txt', '''# IMPERIA COLD WAR — native construction and defence queries.
add_namespace = COLDWAR_NI_PROBE
country_event = { id = COLDWAR_NI_PROBE.1 hidden = yes is_triggered_only = yes immediate = {
 log = "COLDWAR_NI_PROBE START"
 set_technology = { nuclear_technology = 1 popup = no }
 set_variable = { ni_before = modifier@intelligence_agency_defense }
 if = { limit = { has_dlc = "La Resistance" }
  create_intelligence_agency = yes
  upgrade_intelligence_agency = upgrade_passive_defense
 }
 set_variable = { ni_upgrade = modifier@intelligence_agency_defense }
 log = "COLDWAR_NI_PROBE defense_upgrade=[?ni_upgrade]"
 add_ideas = COLDWAR_NI_probe_defense
 set_variable = { ni_after = modifier@intelligence_agency_defense }
 log = "COLDWAR_NI_PROBE defense_before=[?ni_before] defense_after=[?ni_after]"
 COLDWAR_NI_calculate_defense = yes
 log = "COLDWAR_NI_PROBE factors=[?COLDWAR_NI_enrichment_defense_factor]/[?COLDWAR_NI_weapons_defense_factor]"
 if = { limit = { check_variable = { COLDWAR_NI_enrichment_defense_factor = 0.85 } check_variable = { COLDWAR_NI_weapons_defense_factor = 0.8 } }
  log = "COLDWAR_NI_PROBE PASS national_defense" }
 COLDWAR_NI_initialize_country = yes
 random_owned_controlled_state = { limit = { enrichment_facility < 1 free_building_slots = { building = enrichment_facility size > 0 } }
  save_event_target_as = ni_probe_site
  log = "COLDWAR_NI_PROBE state=[This.GetName]"
  if = { limit = { can_construct_building = enrichment_facility } log = "COLDWAR_NI_PROBE PASS empty_state_buildable" }
  add_building_construction = { type = enrichment_facility level = 1 instant_build = no }
  if = { limit = { free_building_slots = { building = enrichment_facility size > 0 } } log = "COLDWAR_NI_PROBE queue_free_slots=1" }
  else = { log = "COLDWAR_NI_PROBE queue_free_slots=0" }
  if = { limit = { can_construct_building = enrichment_facility } log = "COLDWAR_NI_PROBE queue_can_construct=1" }
  else = { log = "COLDWAR_NI_PROBE queue_can_construct=0" }
 }
 COLDWAR_NI_update_enrichment = yes
 if = { limit = { has_country_flag = COLDWAR_NI_expansion_active } log = "COLDWAR_NI_PROBE PASS live_construction_detected" }
 else = { log = "COLDWAR_NI_PROBE FAIL live_construction_detected" }
 ENG = {
  COLDWAR_NI_observer_rates = yes
  log = "COLDWAR_NI_PROBE ENG_rates=[?COLDWAR_NI_enrichment_chance]/[?COLDWAR_NI_weapons_chance]"
  COLDWAR_NI_enrichment_success = yes
  COLDWAR_NI_enrichment_success = yes
  COLDWAR_NI_weapons_success = yes
  COLDWAR_NI_weapons_success = yes
  log = "COLDWAR_NI_PROBE ENG_knowledge=[?COLDWAR_NI_enrichment_knowledge@ROOT]/[?COLDWAR_NI_weapons_knowledge@ROOT]"
 }
 SOV = { log = "COLDWAR_NI_PROBE SOV_private=[?COLDWAR_NI_enrichment_knowledge@ROOT]/[?COLDWAR_NI_weapons_knowledge@ROOT]" }
 set_variable = { COLDWAR_NI_passive_defense_level = 4 }
 COLDWAR_NI_calculate_defense = yes
 if = { limit = { check_variable = { COLDWAR_NI_enrichment_defense_factor = 0.75 } check_variable = { COLDWAR_NI_weapons_defense_factor = 0.6 } }
  log = "COLDWAR_NI_PROBE PASS passive_defense" }
 COLDWAR_NI_refresh_observer_cache = yes
 set_variable = { ni_cache_count = global.COLDWAR_NI_observers^num }
 COLDWAR_NI_refresh_observer_cache = yes
 if = { limit = { check_variable = { ni_cache_count = global.COLDWAR_NI_observers^num } check_variable = { ni_cache_count > 4 } }
  log = "COLDWAR_NI_PROBE PASS observer_cache" }
 ENG = {
  COLDWAR_NI_roll = yes
  log = "COLDWAR_NI_PROBE random=[?COLDWAR_NI_roll_value]"
  if = { limit = { check_variable = { COLDWAR_NI_roll_value > -0.001 } check_variable = { COLDWAR_NI_roll_value < 100 } }
   log = "COLDWAR_NI_PROBE PASS bounded_roll" }
 }
 COLDWAR_NI_monthly_country = yes
 log = "COLDWAR_NI_PROBE PASS monthly_sweep_executed"
 log = "COLDWAR_NI_PROBE COMPLETE"
} }
''')
    # Log source scoping in the actual report definitions, without changing production events.
    source = (ROOT / 'events/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')
    source = source.replace('is_triggered_only = yes', 'is_triggered_only = yes\n\timmediate = { log = "COLDWAR_NI_PROBE report_scope=[Root.GetTag] source=[From.GetTag]" }')
    write(PROFILE / 'fixture/events/COLDWAR_nuclear_intelligence.txt', source)
    for name in ['game.log', 'error.log']:
        write(PROFILE / 'logs' / name, '')
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    process = subprocess.Popen([str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', f'-userdir={PROFILE}', '-start_tag=USA', '-start_speed=1', '-hands_off'], cwd=GAME, startupinfo=startup)
    print(json.dumps({'pid': process.pid, 'profile': str(PROFILE)}), flush=True)
    start = time.monotonic()
    while process.poll() is None and time.monotonic() - start < 600:
        time.sleep(1)
        log_path = PROFILE / 'logs/game.log'
        if log_path.exists() and 'COLDWAR_NI_PROBE COMPLETE' in log_path.read_text(encoding='utf-8-sig', errors='replace'):
            break
    if process.poll() is None:
        process.terminate()
    process.wait(timeout=30)
    log_output = {}
    for name in ['game.log', 'error.log']:
        path = PROFILE / 'logs' / name
        content = path.read_text(encoding='utf-8-sig', errors='replace') if path.exists() else ''
        log_output[name] = [line for line in content.splitlines() if 'COLDWAR_NI' in line or 'COLDWAR_nuclear_intelligence' in line]
    report = {'project': 'IMPERIA COLD WAR', 'exit_code': process.returncode, 'elapsed_seconds': round(time.monotonic() - start), 'checkpoints': log_output['game.log'], 'relevant_errors': log_output['error.log']}
    report['complete'] = any('COLDWAR_NI_PROBE COMPLETE' in line for line in report['checkpoints'])
    required = ['national_defense', 'empty_state_buildable', 'live_construction_detected', 'passive_defense', 'observer_cache', 'bounded_roll', 'monthly_sweep_executed']
    report['required_checkpoints'] = {k: any('PASS ' + k in line for line in report['checkpoints']) for k in required}
    report['private_knowledge_verified'] = any('ENG_knowledge=2/2' in x for x in report['checkpoints']) and any('SOV_private=0/0' in x for x in report['checkpoints'])
    report['four_report_sources_verified'] = sum('report_scope=ENG source=USA' in x for x in report['checkpoints']) == 4
    report['terminated_after_complete'] = report['complete']
    report['passed'] = report['complete'] and all(report['required_checkpoints'].values()) and report['private_knowledge_verified'] and report['four_report_sources_verified'] and not report['relevant_errors'] and not any(' FAIL ' in line for line in report['checkpoints'])
    write(ROOT / 'docs/nuclear_intelligence/native_probe.json', json.dumps(report, indent=2))
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
