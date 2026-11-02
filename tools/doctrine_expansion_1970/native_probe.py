# IMPERIA COLD WAR — Isolated native doctrine loading and mastery probe.
"""Freeze scripts on E:, run a private hidden game, and collect bounded evidence."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from coverage_revision import ARTILLERY, GRAND_FILES, SUB_FILES, UNIT_MODIFIERS, COLOUR_PATH, SYNC_PATH

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/doctrine_expansion_1970')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MARKER = '# IMPERIA COLD WAR — Private native doctrine expansion test.\n'
CONFIGS = {
 'USA': ('mdcw_deliberate_firepower', ['battalion_combat_teams', 'mdcw_maskirovka', 'mdcw_assault_breaching', 'mdcw_cadre_reserve_system', 'mdcw_institutional_combat_learning', 'mdcw_radio_electronic_combat']),
 'EGY': ('mdcw_deliberate_firepower', ['mdcw_integrated_support_commands', 'mdcw_heliborne_reaction_forces', 'mdcw_coastal_denial', 'mdcw_opposing_force_exercises', 'mdcw_institutional_combat_learning', 'mdcw_counterfire_coordination']),
 'AUS': ('mdcw_total_defence', ['mdcw_cohesive_unit_rotation', 'mdcw_forest_envelopment', 'mdcw_key_zone_defence', 'mdcw_mission_rehearsal', 'mdcw_opposing_force_exercises', 'mdcw_guided_anti_armour_integration']),
 'SAF': ('mdcw_mobile_raiding_warfare', ['decentralized_command', 'mdcw_forest_envelopment', 'mdcw_heliborne_reaction_forces', 'mdcw_opposing_force_exercises', 'mdcw_institutional_combat_learning', 'common_technology_army']),
}


def write(path, text, encoding='utf-8'):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding, newline='\n')


def copy_scripts(source, target):
    """Only traverse real script directories; never follow an asset junction."""
    target.mkdir(parents=True, exist_ok=True)
    for current, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = [name for name in dirs if not (Path(current) / name).is_junction() and not (Path(current) / name).is_symlink()]
        relative = Path(current).relative_to(source)
        (target / relative).mkdir(exist_ok=True)
        for name in files:
            path = Path(current) / name
            if not path.is_symlink():
                shutil.copy2(path, target / relative / name)


def fixture_events():
    configure = ['log = "ICW_DOCTRINE CONFIGURE"']
    verify = ['log = "ICW_DOCTRINE VERIFY"']
    for tag, (grand, subs) in CONFIGS.items():
        configure += [tag + ' = {', 'set_grand_doctrine = ' + grand]
        for index, sub in enumerate(subs):
            configure += ['set_sub_doctrine = { sub_doctrine = ' + sub + ' folder = land track = ' + str(index) + ' }']
        configure += ['add_mastery = { amount = 500 folder = land }', '}']
        verify += [tag + ' = {', 'if = { limit = { has_doctrine = ' + grand + ' } log = "ICW_DOCTRINE GRAND_PASS ' + tag + ' ' + grand + '" }',
                   'else = { log = "ICW_DOCTRINE FAIL GRAND ' + tag + '" }']
        for sub in subs:
            verify += ['if = { limit = { has_completed_subdoctrine = ' + sub + ' } log = "ICW_DOCTRINE MASTERY_PASS ' + tag + ' ' + sub + '" }',
                       'else = { log = "ICW_DOCTRINE FAIL MASTERY ' + tag + ' ' + sub + '" }']
        verify.append('}')
    configure += ['country_event = { id = ICW_DOCTRINE.2 hours = 26 }']
    # Observe the native country modifier, then swap only the grand doctrine.
    # This isolates the new supply-gap penalty from national modifiers/subdoctrines.
    verify += [
        'SAF = {',
        'set_temp_variable = { ICW_DOCTRINE_supply_before = modifier@out_of_supply_factor }',
        'set_grand_doctrine = combined_arms',
        'set_temp_variable = { ICW_DOCTRINE_supply_removed = ICW_DOCTRINE_supply_before }',
        'subtract_from_temp_variable = { ICW_DOCTRINE_supply_removed = modifier@out_of_supply_factor }',
        'log = "ICW_DOCTRINE SUPPLY_GAP_SWITCH removed=[?ICW_DOCTRINE_supply_removed]"',
        'if = { limit = { check_variable = { ICW_DOCTRINE_supply_removed = 0.15 } } log = "ICW_DOCTRINE SUPPLY_PENALTY_PASS" }',
        'else = { log = "ICW_DOCTRINE FAIL SUPPLY_PENALTY" }',
        '}',
    ]
    verify += [
        'AUS = {',
        'if = { limit = { does_not_have_mdcw_territorial_defence_doctrine = yes } log = "ICW_DOCTRINE FAIL TERRITORIAL_CONFLICT" }',
        'else = { log = "ICW_DOCTRINE TERRITORIAL_CONFLICT_BLOCKED" }', '}',
        'set_temp_variable = { ICW_DOCTRINE_before = modifier@' + ARTILLERY + ' }',
        'set_grand_doctrine = mdcw_mobile_raiding_warfare',
        'set_temp_variable = { ICW_DOCTRINE_after = modifier@' + ARTILLERY + ' }',
        'set_temp_variable = { ICW_DOCTRINE_removed = ICW_DOCTRINE_before }',
        'subtract_from_temp_variable = { ICW_DOCTRINE_removed = ICW_DOCTRINE_after }',
        'log = "ICW_DOCTRINE GRAND_SWITCH before=[?ICW_DOCTRINE_before] after=[?ICW_DOCTRINE_after] removed=[?ICW_DOCTRINE_removed]"',
        # This fixture now includes +0.20 from the grand and +0.10 from EW.
        # Native grand replacement clears the old subdoctrine tracks as well.
        'if = { limit = { check_variable = { ICW_DOCTRINE_removed = 0.3 } } log = "ICW_DOCTRINE SWITCH_CLEANUP_PASS" }',
        'else = { log = "ICW_DOCTRINE FAIL SWITCH_CLEANUP" }',
    ]
    # Every grand's own immediate drawback is observed against a reference without
    # that field. Setting a grand clears its previous track modifiers natively.
    for ident, field, value in [
        ('combined_arms', 'supply_consumption_factor', .08),
        ('shock_and_awe', 'army_fuel_consumption_factor', .15),
        ('defence_in_depth', 'org_loss_when_moving', .10),
        ('mission_command', 'army_personnel_cost_multiplier_modifier', .08),
        ('battlefield_support', 'supply_consumption_factor', .05),
        ('guerrilla_warfare', 'max_planning_factor', -.15),
        ('mdcw_deep_operation', 'initiative_factor', -.05),
        ('mdcw_active_defense', 'breakthrough_factor', -.10),
        ('mdcw_airland_battle', 'army_fuel_consumption_factor', .05),
        ('mdcw_peoples_war', 'army_armor_attack_factor', -.10),
        ('mdcw_total_defence', 'army_non_core_attack_factor', -.05),
        ('mdcw_fanatical_struggle', 'experience_loss_factor', .10),
        ('mdcw_deliberate_firepower', 'supply_consumption_factor', .12),
        ('mdcw_mobile_raiding_warfare', 'out_of_supply_factor', .15),
    ]:
        reference = 'combined_arms' if ident == 'mdcw_total_defence' else 'mdcw_total_defence'
        verify += ['SAF = {', 'set_grand_doctrine = ' + reference,
                   'set_temp_variable = { ICW_DOCTRINE_base = modifier@' + field + ' }',
                   'set_grand_doctrine = ' + ident,
                   'set_temp_variable = { ICW_DOCTRINE_delta = modifier@' + field + ' }',
                   'subtract_from_temp_variable = { ICW_DOCTRINE_delta = ICW_DOCTRINE_base }',
                   'if = { limit = { check_variable = { ICW_DOCTRINE_delta = ' + str(value) + ' } } log = "ICW_DOCTRINE GRAND_PENALTY_PASS ' + ident + '" }',
                   'else = { log = "ICW_DOCTRINE FAIL GRAND_PENALTY ' + ident + ' value=[?ICW_DOCTRINE_delta]" }', '}']
    verify += ['USA = {', 'set_grand_doctrine = mission_command',
               'set_temp_variable = { ICW_DOCTRINE_training_base = modifier@training_time_army_factor }',
               'set_sub_doctrine = { sub_doctrine = skill_school_focus folder = land track = 2 }',
               'set_sub_doctrine = { sub_doctrine = officer_training_focus folder = land track = 3 }',
               'set_sub_doctrine = { sub_doctrine = nco_training_focus folder = land track = 4 }',
               'set_temp_variable = { ICW_DOCTRINE_training_delta = modifier@training_time_army_factor }',
               'subtract_from_temp_variable = { ICW_DOCTRINE_training_delta = ICW_DOCTRINE_training_base }',
               'if = { limit = { check_variable = { ICW_DOCTRINE_training_delta = 0.3 } } log = "ICW_DOCTRINE SCHOOLS_IMMEDIATE_PASS" }',
               'else = { log = "ICW_DOCTRINE FAIL SCHOOLS_IMMEDIATE value=[?ICW_DOCTRINE_training_delta]" }',
               'add_mastery = { amount = 500 folder = land }', '}']
    # Mastery is applied on the next hourly update, so observe it in another event.
    verify += ['country_event = { id = ICW_DOCTRINE.3 hours = 2 }']
    final = ['USA = {']
    for sub in ('skill_school_focus', 'officer_training_focus', 'nco_training_focus'):
        final += ['if = { limit = { has_completed_subdoctrine = ' + sub + ' } log = "ICW_DOCTRINE SCHOOLS_MASTERY_PASS ' + sub + '" }',
                  'else = { log = "ICW_DOCTRINE FAIL SCHOOLS_MASTERY ' + sub + '" }']
    final += ['}', 'log = "ICW_DOCTRINE RUN_COMPLETE"']
    return MARKER + 'add_namespace = ICW_DOCTRINE\n' + '\n'.join(
        'country_event = { id = ICW_DOCTRINE.' + str(index) + ' hidden = yes is_triggered_only = yes immediate = {\n' + '\n'.join(body) + '\n} }\n'
        for index, body in ((1, configure), (2, verify), (3, final)))


def prepare(reuse_snapshot=None):
    run_id = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    run = BASE / run_id
    snapshot, profile, fixture = run / 'snapshot', run / 'profile', run / 'fixture'
    assert run.resolve().is_relative_to(BASE.resolve())
    assert not run.exists()
    run.mkdir(parents=True)
    script_dirs = ['common', 'events', 'history', 'interface', 'localisation', 'portraits', 'tutorial', 'descriptions']
    if reuse_snapshot:
        snapshot = Path(reuse_snapshot).resolve()
        assert snapshot.is_relative_to(BASE.resolve()) and snapshot.is_dir()
        prior_manifest = json.loads((snapshot.parent / 'snapshot_manifest.json').read_text(encoding='utf-8'))
        # Reuse frozen scripts only when every installed runtime input is identical.
        for relative in [*GRAND_FILES, *SUB_FILES, UNIT_MODIFIERS, COLOUR_PATH,
                         'common/doctrines/grand_doctrines/mdcw_land_doctrine_expansion.txt',
                         'common/doctrines/subdoctrines/land/mdcw_land_doctrine_expansion.txt',
                         'common/doctrines/subdoctrines/land/land_doctrines_combat.txt',
                         'common/doctrines/subdoctrines/land/land_doctrines_supporting.txt',
                         'common/doctrines/subdoctrines/land/mdcw_cold_war_free_subdoctrines.txt',
                         'common/scripted_triggers/00_doctrines_scripted_triggers.txt',
                         'interface/mdcw_land_doctrine_expansion.gfx',
                         'localisation/english/mdcw_land_doctrine_expansion_l_english.yml',
                         'localisation/english/MD_doctrines_ncns_l_english.yml',
                         'localisation/english/mdcw_cold_war_doctrines_l_english.yml']:
            assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == prior_manifest['script_sha256'][relative], relative
        print('Reusing verified immutable scripts: ' + str(snapshot), flush=True)
    else:
        for name in script_dirs:
            if (ROOT / name).is_dir():
                copy_scripts(ROOT / name, snapshot / name)
                print('Frozen ' + name, flush=True)
        for path in ROOT.iterdir():
            if path.is_file() and path.suffix in {'.txt', '.mod', '.lua'}:
                shutil.copy2(path, snapshot / path.name)
        for name in ['gfx', 'map', 'sound', 'music']:
            target = snapshot / name
            # Directory junction creation only. No recursive move/delete or shell enumeration.
            result = subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(target), str(ROOT / name)], capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr or result.stdout)
    descriptor = (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig')
    write(profile / 'mod/mdcoldwar.mod', MARKER + descriptor + '\npath="' + snapshot.as_posix() + '"\n')
    addon = MARKER + 'name="IMPERIA doctrine probe"\ndependencies={ "MD Cold War" }\npath="' + fixture.as_posix() + '"\n'
    write(profile / 'mod/probe.mod', addon)
    write(fixture / 'descriptor.mod', addon)
    write(profile / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/mdcoldwar.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write(profile / 'settings.txt', MARKER + 'language="l_english"\ngraphics={size={x=1280 y=800} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write(fixture / 'common/on_actions/zzzzzzzz_IMPERIA_doctrine_probe.txt', MARKER + '''on_actions = {
 on_startup = { effect = {
  log = "ICW_DOCTRINE STARTUP"
  USA = { country_event = { id = ICW_DOCTRINE.1 hours = 2 } }
 } }
}
''')
    write(fixture / 'events/IMPERIA_doctrine_probe.txt', fixture_events())
    # A new synchronised token may be supplied through the last-loaded fixture
    # when reusing immutable scripts. All existing affected inputs must still match.
    overlay_hashes = {}
    sync_raw = (ROOT / SYNC_PATH).read_bytes()
    frozen_sync = snapshot / SYNC_PATH
    if not frozen_sync.is_file() or frozen_sync.read_bytes() != sync_raw:
        write(fixture / SYNC_PATH, sync_raw.decode('utf-8'))
        overlay_hashes[SYNC_PATH] = hashlib.sha256(sync_raw).hexdigest()
    hashes = prior_manifest['script_sha256'] if reuse_snapshot else {}
    for directory in ([] if reuse_snapshot else script_dirs):
        if not (snapshot / directory).exists():
            continue
        for current, dirs, files in os.walk(snapshot / directory, followlinks=False):
            dirs[:] = [name for name in dirs if not (Path(current) / name).is_junction()]
            for name in files:
                path = Path(current) / name
                hashes[path.relative_to(snapshot).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    record = {'project': 'IMPERIA COLD WAR', 'run_id': run_id, 'run': str(run), 'snapshot': str(snapshot),
              'profile': str(profile), 'script_sha256': hashes, 'fixture_runtime_sha256': overlay_hashes,
              'asset_junctions_not_traversed': ['gfx', 'map', 'sound', 'music']}
    write(run / 'snapshot_manifest.json', json.dumps(record, indent=2) + '\n')
    write(HERE / 'native_run_location.json', json.dumps({key: value for key, value in record.items() if key != 'script_sha256'}, indent=2) + '\n')
    print(json.dumps({'prepared': str(run)}), flush=True)


def run_probe(duration):
    record = json.loads((HERE / 'native_run_location.json').read_text(encoding='utf-8'))
    run, profile = Path(record['run']), Path(record['profile'])
    assert run.resolve().is_relative_to(BASE.resolve())
    assert not (run / 'native_result.json').exists(), 'Use a fresh prepared run; never replace previous engine evidence'
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    arguments = [str(GAME / 'hoi4.exe'), '-noasserts', '-assertsdialog=no', '-userdir=' + str(profile),
                 '-start_tag=USA', '-start_speed=5', '-hands_off']
    started = time.monotonic()
    process = subprocess.Popen(arguments, cwd=GAME, startupinfo=startup)
    print(json.dumps({'pid': process.pid, 'profile': str(profile)}), flush=True)
    game_log = profile / 'logs/game.log'
    source, observed = '', []
    try:
        while process.poll() is None and time.monotonic() - started < duration:
            time.sleep(2)
            source = game_log.read_text(encoding='utf-8-sig', errors='replace') if game_log.exists() else ''
            markers = [line for line in source.splitlines() if 'ICW_DOCTRINE ' in line]
            if markers != observed:
                for line in markers[len(observed):]:
                    print(line, flush=True)
                observed = markers
            if 'ICW_DOCTRINE RUN_COMPLETE' in source:
                break
    finally:
        running = process.poll() is None
        exit_code = process.poll()
        if running:
            process.terminate()
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
    error_log = profile / 'logs/error.log'
    errors = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    ids = set(sub for _, subs in CONFIGS.values() for sub in subs) | {'mdcw_deliberate_firepower', 'mdcw_mobile_raiding_warfare'}
    changed_names = ['mdcw_land_doctrine_expansion', 'land_doctrines_combat.txt',
                     'land_doctrines_supporting.txt', 'mdcw_cold_war_free_subdoctrines.txt', 'ICW_DOCTRINE',
                     *[Path(p).name for p in (*GRAND_FILES, *SUB_FILES, UNIT_MODIFIERS, COLOUR_PATH, SYNC_PATH)], ARTILLERY]
    relevant = [line for line in errors.splitlines() if any(name in line for name in changed_names) or any(key in line for key in ids)]
    result = {'project': 'IMPERIA COLD WAR', 'pid': process.pid, 'elapsed_seconds': round(time.monotonic() - started, 1),
              'profile': str(profile), 'engine_exit_before_termination': exit_code, 'stopped_own_test_process': running,
              'completed': 'ICW_DOCTRINE RUN_COMPLETE' in source, 'markers': observed,
              'failed_markers': [line for line in observed if 'ICW_DOCTRINE FAIL' in line],
              'doctrine_related_errors': relevant, 'full_error_log': str(error_log),
              'tested_subdoctrines': sorted(set(sub for _, subs in CONFIGS.values() for sub in subs)),
              'multiplayer_test': False, 'live_ui_inspected': False}
    write(run / 'native_result.json', json.dumps(result, indent=2) + '\n')
    write(HERE / 'native_result.json', json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)
    if not result['completed'] or result['failed_markers'] or result['doctrine_related_errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--duration', type=int, default=300)
    parser.add_argument('--snapshot', help='reuse a verified immutable snapshot with a new fixture and private profile')
    args = parser.parse_args()
    if args.prepare:
        prepare(args.snapshot)
    if args.run:
        run_probe(args.duration)
