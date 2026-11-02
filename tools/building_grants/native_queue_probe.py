# IMPERIA COLD WAR — Isolated native construction-queue and collection probe.
"""Read the current mod as a base, add a private E: fixture and own one PID.

No assets are copied or traversed. Private positive controls use radar1945;
the combined fixture isolates a second phase with construction-only programme
entitlements. No later MD research is granted. Existing games are untouched.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
OWN = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/building_grants_20261027/queue')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PREFIX = 'ICW_BUILDING_QUEUE'
MARK = '# IMPERIA COLD WAR — Private native building-queue probe.\n'
CONTROLLED = False
ALIASES = False
COMBINED = False
TECHS = ('railway_system_01', 'railway_system_02', 'railway_system_04',
         'railway_system_05', 'railway_system_06', 'air_defense', 'SAM', 'SAM0',
         'SAM1', 'SAM2', 'air_defense_non_got', 'SAM_non_got', 'SAM0_non_got',
         'SAM1_non_got', 'SAM2_non_got')

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, text):
    path = Path(path)
    assert path.absolute().is_relative_to(OWN.absolute()), path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def assertion(label, condition):
    return ('if = { limit = { ' + condition + ' } log = "' + PREFIX + ' PASS ' + label + '" }\n'
            'else = { log = "' + PREFIX + ' FAIL ' + label + '" }\n')

def collection(flag, comparison):
    return ('collection_size = { input = { input = game:scope operators = { '
            'owned_states limit = { has_state_flag = ' + flag + ' } } } '
            'value ' + comparison + ' }')

def slot_counter(variable):
    # There is no documented shared-slot dynamic accessor. Count the true
    # native headroom thresholds below the independent factory ceiling.
    code = 'set_variable = { ' + variable + ' = 0 }\n'
    for threshold in range(50):
        code += ('if = { limit = { free_building_slots = { building = industrial_complex size > '
                 + str(threshold) + ' include_locked = yes } } add_to_variable = { ' + variable + ' = 1 } }\n')
    return code

def alias_checks():
    call = 'COLDWAR_GRANT_native_one_state_renewable_energy_infra = yes\n'
    code = 'set_temp_variable = { skip_payment = 1 }\nset_variable = { ICW_ALIAS_cash_before = treasury }\n'
    code += ('806 = { set_state_flag = ICW_ALIAS_target add_extra_state_shared_building_slots = 18 '
             'set_building_level = { type = renewable_energy_infra level = 18 }\n')
    code += slot_counter('ICW_ALIAS_slots_before')
    code += assertion('ALIAS_SLOT_OBSERVATION_UNSATURATED', 'check_variable = { ICW_ALIAS_slots_before < 49 }')
    code += call
    code += assertion('ALIAS_18_TO_19', 'check_variable = { building_level@renewable_energy_infra = 19 }')
    code += slot_counter('ICW_ALIAS_slots_after')
    code += 'subtract_from_variable = { ICW_ALIAS_slots_after = ICW_ALIAS_slots_before }\n'
    code += assertion('ALIAS_SHARED_SLOT_PLUS_ONE', 'check_variable = { ICW_ALIAS_slots_after = 1 }')
    code += 'log = "' + PREFIX + ' DIAG ALIAS shared_headroom_before=[?ICW_ALIAS_slots_before] slot_increase=[?ICW_ALIAS_slots_after]"\n}\n'
    code += assertion('ALIAS_SKIP_PAYMENT_NO_CHARGE', 'check_variable = { var = treasury value = ICW_ALIAS_cash_before compare = equals }')
    # A state helper deliberately falls back to another owned eligible state.
    # Saturate every other owned state to test the real no-capacity branch.
    code += ('every_owned_state = { limit = { NOT = { has_state_flag = ICW_ALIAS_target } } '
             'add_extra_state_shared_building_slots = 20 set_building_level = { type = renewable_energy_infra level = 20 } }\n'
             '806 = { add_extra_state_shared_building_slots = 1 set_building_level = { type = renewable_energy_infra level = 20 }\n')
    code += slot_counter('ICW_ALIAS_full_slots_before') + '}\n'
    code += 'set_temp_variable = { skip_payment = 0 }\n806 = {\n' + call
    code += assertion('ALIAS_AT_CAP_UNCHANGED', 'check_variable = { building_level@renewable_energy_infra = 20 }')
    code += slot_counter('ICW_ALIAS_full_slots_after')
    code += 'subtract_from_variable = { ICW_ALIAS_full_slots_after = ICW_ALIAS_full_slots_before }\n'
    code += assertion('ALIAS_AT_CAP_NO_SLOT_REPLAY', 'check_variable = { ICW_ALIAS_full_slots_after = 0 }') + '}\n'
    code += assertion('ALIAS_AT_CAP_NO_CHARGE', 'check_variable = { var = treasury value = ICW_ALIAS_cash_before compare = equals }')
    return code

def fixtures():
    if COMBINED:
        return combined_fixtures()
    first = assertion('USA_1970', 'tag = USA IMP_is_1970_scenario = yes')
    first += assertion('NO_MANUAL_TECH_BEFORE', ' '.join('NOT = { has_tech = ' + t + ' }' for t in TECHS))
    first += ('add_ideas = ICW_BUILDING_QUEUE_booster\n'
              'add_offsite_building = { type = industrial_complex level = 100 }\n'
              'set_variable = { corporate_tax_rate = 0 }\n'
              'set_variable = { treasury = 10000 }\n')
    if ALIASES:
        first += alias_checks()
    if CONTROLLED:
        first += 'set_technology = { radar = 1 }\n'
        first += assertion('BOOSTER_ACTIVE', 'has_idea = ICW_BUILDING_QUEUE_booster')
        first += assertion('CIVILIANS_AVAILABLE', 'check_variable = { var = num_of_civilian_factories_available_for_projects value = 15 compare = greater_than_or_equals }')
        first += ('log = "' + PREFIX + ' DIAG ECONOMY civs=[?num_of_civilian_factories] '
                  'available=[?num_of_civilian_factories_available_for_projects] speed=[?modifier@production_speed_buildings_factor] '
                  'infra_speed=[?modifier@production_speed_infrastructure_factor] tax=[?corporate_tax_rate]"\n')
    first += '800 = { set_state_flag = ICW_QUEUE_count1 set_state_flag = ICW_QUEUE_count2 }\n'
    first += '804 = { set_state_flag = ICW_QUEUE_count2 }\n'
    for count in (0, 1, 2):
        flag = 'ICW_QUEUE_count' + str(count)
        first += assertion('COLLECTION_EXACT_' + str(count), collection(flag, '= ' + str(count)))
        for threshold in (0, 1, 2, 3):
            condition = collection(flag, '> ' + str(threshold))
            # Native 1.19.4 retry02 established strict comparisons at all
            # three equality boundaries, despite the installed docs' note.
            if count <= threshold:
                condition = 'NOT = { ' + condition + ' }'
            first += assertion('COLLECTION_' + str(count) + '_GT_' + str(threshold), condition)
    plans = [(800, 'infrastructure', 3), (804, 'anti_air_building', 0)]
    if CONTROLLED:
        plans += [(811, 'industrial_complex', None), (805, 'radar_station', None)]
    for sid, kind, expected in plans:
        first += str(sid) + ' = {\n'
        first += 'set_variable = { ICW_QUEUE_before = building_level@' + kind + ' }\n'
        first += 'log = "' + PREFIX + ' DIAG BEFORE state=' + str(sid) + ' kind=' + kind + ' built=[?ICW_QUEUE_before]"\n'
        if expected is not None:
            first += assertion('INITIAL_' + kind, 'check_variable = { var = building_level@' + kind + ' value = ' + str(expected) + ' compare = equals }')
            first += assertion('MANUAL_ZERO_' + kind, 'NOT = { free_building_slots = { building = ' + kind + ' size > 0 } }')
        first += 'add_extra_state_shared_building_slots = 1\n'
        if expected is None:
            first += assertion('MANUAL_ALLOWED_' + kind, 'free_building_slots = { building = ' + kind + ' size > 0' + (' include_locked = no' if kind == 'industrial_complex' else '') + ' }')
        first += 'add_building_construction = { type = ' + kind + ' level = 1 instant_build = no }\n'
        first += assertion('QUEUE_NOT_INSTANT_' + kind, 'check_variable = { var = building_level@' + kind + ' value = ICW_QUEUE_before compare = equals }')
        first += '}\n'
    first += 'log = "' + PREFIX + ' QUEUED"\ncountry_event = { id = ICW_BUILDING_QUEUE.2 days = ' + ('3' if CONTROLLED else '7') + ' }\n'
    later = assertion('NO_MANUAL_TECH_AFTER', ' '.join('NOT = { has_tech = ' + t + ' }' for t in TECHS))
    for sid, kind, _ in plans:
        later += str(sid) + ' = {\nset_variable = { ICW_QUEUE_after = building_level@' + kind + ' }\n'
        later += 'set_variable = { ICW_QUEUE_delta = ICW_QUEUE_after }\nsubtract_from_variable = { ICW_QUEUE_delta = ICW_QUEUE_before }\n'
        later += 'log = "' + PREFIX + ' DIAG AFTER state=' + str(sid) + ' kind=' + kind + ' before=[?ICW_QUEUE_before] after=[?ICW_QUEUE_after] delta=[?ICW_QUEUE_delta]"\n'
        later += assertion('BUILT_PLUS_ONE_' + kind, 'check_variable = { ICW_QUEUE_delta = 1 }') + '}\n'
    later += 'log = "' + PREFIX + ' COMPLETE"\n'
    events = MARK + 'add_namespace = ICW_BUILDING_QUEUE\n'
    for index, body in ((1, first), (2, later)):
        events += 'country_event = { id = ICW_BUILDING_QUEUE.' + str(index) + ' hidden = yes is_triggered_only = yes immediate = {\n' + body + '} }\n'
    speed = '1000' if CONTROLLED else '100000'
    ideas = MARK + ('ideas = { country = { ICW_BUILDING_QUEUE_booster = { picture = generic_industry_1 removal_cost = -1 modifier = { '
                    'production_speed_buildings_factor = ' + speed + ' production_speed_infrastructure_factor = ' + speed + ' '
                    'production_speed_anti_air_building_factor = ' + speed + ' consumer_goods_factor = -1 } } } }\n')
    actions = MARK + 'on_actions = { on_startup = { effect = { USA = { country_event = { id = ICW_BUILDING_QUEUE.1 hours = 1 } } } } }\n'
    return {'events/zzz_ICW_BUILDING_QUEUE.txt': events,
            'common/ideas/zzz_ICW_BUILDING_QUEUE.txt': ideas,
            'common/on_actions/zzz_ICW_BUILDING_QUEUE.txt': actions}, first.count(' PASS ') + later.count(' PASS ')


def combined_fixtures():
    """Isolate API without permission for three days, then permission queues.

    Full queue reservation is tested after permission, before the queue can
    progress. All setup levels are private instant fixtures, never a reward.
    """
    from queue_permissions import permission_outputs, technology_id
    no_md = ' '.join('NOT = { has_tech = ' + t + ' }' for t in TECHS)
    def check(label, body):
        return assertion(label, body)
    def diag_free(label, sid, kind):
        native = f'free_building_slots = {{ building = {kind} size > 0'
        return (f'{sid} = {{\n' + check(label + '_DEFAULT_BLOCKED', 'NOT = { ' + native + ' } }')
                + 'if = { limit = { ' + native + ' include_locked = yes } } log = "' + PREFIX + ' DIAG ' + label + '_INCLUDE_LOCKED YES" }\n'
                + 'else = { log = "' + PREFIX + ' DIAG ' + label + '_INCLUDE_LOCKED NO" }\n}\n')
    first = check('USA_1970', 'tag = USA IMP_is_1970_scenario = yes')
    first += check('NO_MD_TECH_PHASE1', no_md)
    first += ('add_ideas = ICW_BUILDING_QUEUE_booster\n'
              'add_offsite_building = { type = industrial_complex level = 100 }\n'
              'set_variable = { corporate_tax_rate = 0 } set_variable = { treasury = 10000 }\n'
              'set_technology = { radar = 1 }\n')
    first += check('CIVILIANS_AVAILABLE', 'check_variable = { var = num_of_civilian_factories_available_for_projects value = 15 compare = greater_than_or_equals }')
    first += diag_free('INFRA_NO_TECH', 800, 'infrastructure') + diag_free('AA_NO_TECH', 804, 'anti_air_building')
    for sid, kind, initial, final in ((800, 'infrastructure', 3, 4), (804, 'anti_air_building', 0, 1)):
        first += (f'{sid} = {{ add_extra_state_shared_building_slots = 1\n'
                  f'set_building_level = {{ type = {kind} level = {final} instant_build = no }}\n')
        first += check('API_NOT_INSTANT_' + kind, f'check_variable = {{ building_level@{kind} = {initial} }}') + '}\n'
    # Ordinary construction positive controls and original API negative controls.
    for sid, kind, initial, label in ((811, 'industrial_complex', 10, 'CIV'), (805, 'radar_station', 0, 'RADAR'),
                                      (807, 'infrastructure', 1, 'BASE_INFRA'), (808, 'anti_air_building', 0, 'BASE_AA')):
        first += (f'{sid} = {{ add_extra_state_shared_building_slots = 1\n'
                  f'add_building_construction = {{ type = {kind} level = 1 instant_build = no }}\n')
        first += check(label + '_NOT_INSTANT', f'check_variable = {{ building_level@{kind} = {initial} }}') + '}\n'
    first += 'log = "' + PREFIX + ' PHASE1_QUEUED"\ncountry_event = { id = ICW_BUILDING_QUEUE.2 days = 3 }\n'
    second = check('NO_MD_TECH_API_RESULT', no_md)
    for sid, kind, expected, label in ((800, 'infrastructure', 4, 'API_INFRA'), (804, 'anti_air_building', 1, 'API_AA'),
                                       (811, 'industrial_complex', 11, 'CONTROL_CIV'), (805, 'radar_station', 1, 'CONTROL_RADAR'),
                                       (807, 'infrastructure', 1, 'BASE_INFRA_BLOCKED'), (808, 'anti_air_building', 0, 'BASE_AA_BLOCKED')):
        second += f'{sid} = {{ log = "' + PREFIX + f' DIAG PHASE1 {label} actual=[?building_level@{kind}]"\n'
        second += check(label, f'check_variable = {{ building_level@{kind} = {expected} }}') + '}\n'
    second += 'log = "' + PREFIX + ' PHASE1_COMPLETE_BEFORE_PERMISSION"\n'
    # Private setup: normalize independent candidate states before granting tech.
    for sid, kind, level in ((803, 'infrastructure', 3), (809, 'anti_air_building', 0),
                             (806, 'infrastructure', 3), (810, 'infrastructure', 5)):
        second += f'{sid} = {{ set_building_level = {{ type = {kind} level = {level} instant_build = yes }} }}\n'
    second += ('set_technology = { popup = no ' + technology_id('infrastructure', 4) + ' = 1 '
               + technology_id('anti_air_building', 1) + ' = 1 }\n')
    for sid, kind, level in ((803, 'infrastructure', 3), (809, 'anti_air_building', 0)):
        second += f'{sid} = {{\n' + check('PERMISSION_AVAILABLE_' + kind, f'free_building_slots = {{ building = {kind} size > 0 }}')
        second += f'add_extra_state_shared_building_slots = 1 add_building_construction = {{ type = {kind} level = 1 instant_build = no }}\n'
        second += check('PERMISSION_NOT_INSTANT_' + kind, f'check_variable = {{ building_level@{kind} = {level} }}') + '}\n'
    second += ('806 = { add_extra_state_shared_building_slots = 1 '
               'add_building_construction = { type = infrastructure level = 1 instant_build = no }\n')
    second += check('RESERVED_MINIMUM_BLOCKS_NEXT', 'NOT = { free_building_slots = { building = infrastructure size > 0 } }')
    second += ('}\nset_technology = { popup = no ' + technology_id('infrastructure', 5) + ' = 1 }\n806 = {\n')
    second += check('RESERVED_ESCALATE_ONE_OPENS_NEXT', 'free_building_slots = { building = infrastructure size > 0 }')
    second += 'add_extra_state_shared_building_slots = 1 add_building_construction = { type = infrastructure level = 1 instant_build = no }\n'
    second += check('RESERVED_TWO_NOT_INSTANT', 'check_variable = { building_level@infrastructure = 3 }') + '}\n'
    # Full physical reservation must reject a second fee/slot, even though built<cap.
    second += 'set_technology = { popup = no ' + technology_id('infrastructure', 6) + ' = 1 }\n810 = {\n'
    second += 'add_extra_state_shared_building_slots = 1 add_building_construction = { type = infrastructure level = 1 instant_build = no }\n'
    second += check('FULL_PHYSICAL_RESERVATION_BLOCKS', 'NOT = { free_building_slots = { building = infrastructure size > 0 } }')
    second += 'ROOT = { set_variable = { ICW_QUEUE_paid_before = treasury } }\n'
    second += 'if = { limit = { free_building_slots = { building = infrastructure size > 0 } } ROOT = { subtract_from_variable = { treasury = 1 } } add_extra_state_shared_building_slots = 1 add_building_construction = { type = infrastructure level = 1 instant_build = no } }\n}\n'
    second += check('FULL_RESERVATION_NO_FEE', 'check_variable = { var = treasury value = ICW_QUEUE_paid_before compare = equals }')
    second += check('NO_MD_TECH_PERMISSION_START', no_md)
    second += 'log = "' + PREFIX + ' PHASE2_QUEUED"\ncountry_event = { id = ICW_BUILDING_QUEUE.3 days = 3 }\n'
    third = check('NO_MD_TECH_PERMISSION_RESULT', no_md)
    for sid, kind, expected, label in ((803, 'infrastructure', 4, 'PERMISSION_INFRA_BUILT'), (809, 'anti_air_building', 1, 'PERMISSION_AA_BUILT'),
                                       (806, 'infrastructure', 5, 'RESERVED_PLUS_GIFT_BUILT'), (810, 'infrastructure', 6, 'FULL_RESERVED_ONLY_ONE')):
        third += f'{sid} = {{ log = "' + PREFIX + f' DIAG PHASE2 {label} actual=[?building_level@{kind}]"\n'
        third += check(label, f'check_variable = {{ building_level@{kind} = {expected} }}') + '}\n'
    third += 'log = "' + PREFIX + ' COMPLETE"\n'
    sources = permission_outputs()
    sources['events/zzz_ICW_BUILDING_QUEUE.txt'] = MARK + 'add_namespace = ICW_BUILDING_QUEUE\n' + ''.join(
        f'country_event = {{ id = ICW_BUILDING_QUEUE.{i} hidden = yes is_triggered_only = yes immediate = {{\n{body}}} }}\n'
        for i, body in ((1, first), (2, second), (3, third)))
    sources['common/ideas/zzz_ICW_BUILDING_QUEUE.txt'] = MARK + ('ideas = { country = { ICW_BUILDING_QUEUE_booster = { picture = generic_industry_1 removal_cost = -1 modifier = { '
        'production_speed_buildings_factor = 1000 production_speed_infrastructure_factor = 1000 '
        'production_speed_anti_air_building_factor = 1000 consumer_goods_factor = -1 } } } }\n')
    sources['common/on_actions/zzz_ICW_BUILDING_QUEUE.txt'] = MARK + 'on_actions = { on_startup = { effect = { USA = { country_event = { id = ICW_BUILDING_QUEUE.1 hours = 1 } } } } }\n'
    return sources, sum(body.count(' PASS ') for body in (first, second, third))

def prepare():
    assert not (OWN / 'manifest.json').exists(), 'Existing private run must remain untouched'
    addon = OWN / 'fixture'
    profile = OWN / 'profile'
    sources, expected = fixtures()
    for rel, source in sources.items():
        write(addon / rel, source)
        if rel.endswith('.yml'):
            (addon / rel).write_bytes(b'\xef\xbb\xbf' + source.encode('utf-8'))
    # Small, exact provider snapshots only. No asset folder traversal or copy.
    frozen = ['common/buildings/00_buildings.txt', 'common/technologies/industry.txt',
              'common/technologies/missile_defense.txt', 'common/technologies/non_got_missiles.txt']
    if CONTROLLED or COMBINED:
        frozen.append('common/technologies/engineering.txt')
    if ALIASES:
        frozen += ['common/scripted_effects/COLDWAR_GRANT_native.txt',
                   'common/scripted_effects/COLDWAR_GRANT_programmes.txt',
                   'common/scripted_triggers/COLDWAR_GRANT_programmes.txt',
                   'common/on_actions/COLDWAR_GRANT_programmes.txt',
                   'localisation/english/COLDWAR_GRANT_capacity_l_english.yml']
    for rel in frozen:
        target = addon / rel
        assert target.absolute().is_relative_to(OWN.absolute())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / rel).read_bytes())
    base = MARK + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + ROOT.as_posix() + '"\n'
    overlay = MARK + 'name="ICW native queue probe"\ndependencies={"MD Cold War"}\npath="' + addon.as_posix() + '"\n'
    write(profile / 'mod/base.mod', base)
    write(profile / 'mod/probe.mod', overlay)
    write(addon / 'descriptor.mod', overlay)
    write(profile / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/base.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write(profile / 'settings.txt', 'language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\nautosave="DAILY"\nautosave_tocloud=no\n')
    manifest = dict(project='IMPERIA COLD WAR', created_utc=datetime.now(timezone.utc).isoformat(),
                    profile=str(profile), expected_passes=expected,
                    controls=CONTROLLED, aliases=ALIASES, combined=COMBINED, probe_generator_sha256=digest(__file__),
                    fixture_hashes={p.relative_to(addon).as_posix(): digest(p) for p in addon.rglob('*') if p.is_file()},
                    source_hashes={rel: digest(ROOT / rel) for rel in frozen},
                    asset_mode='Read-only existing base. No asset traversal, copy, link or archive.',
                    scope='Private single-player native queue/collection observation. No UI, save or multiplayer claim.')
    write(OWN / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'prepared': str(profile), 'expected_passes': expected}), flush=True)
    return profile

def existing_pids():
    command = '@(Get-Process | Where-Object { $_.ProcessName -eq "hoi4" } | Select-Object -ExpandProperty Id) | ConvertTo-Json -Compress'
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', command], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    value = json.loads(result.stdout.strip() or '[]')
    return [] if value is None else value if isinstance(value, list) else [value]

def run(profile, duration):
    assert 60 <= duration <= 900
    assert not existing_pids(), 'Existing HOI4 process remains untouched; probe not launched'
    manifest = json.loads((OWN / 'manifest.json').read_text())
    addon = OWN / 'fixture'
    assert all(digest(addon / rel) == sha for rel, sha in manifest['fixture_hashes'].items())
    log = profile / 'logs/game.log'
    error_log = profile / 'logs/error.log'
    assert not log.exists(), 'Do not overwrite a prior native run'
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    # A live read-only provider must not hot-reload other chats' edits. Existing
    # native USA probes likewise omit -debug after demonstrated reload failures.
    args = [str(GAME / 'hoi4.exe'), '-noasserts', '-assertsdialog=no', '-userdir=' + str(profile), '-start_tag=USA', '-start_speed=5', '-hands_off']
    started = time.monotonic()
    process = subprocess.Popen(args, cwd=GAME, startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps({'pid': process.pid, 'hidden': True, 'profile': str(profile), 'duration_bound': duration}), flush=True)
    reason = 'process exited'
    try:
        while process.poll() is None and time.monotonic() - started < duration:
            time.sleep(1)
            text = log.read_text(encoding='utf-8-sig', errors='replace') if log.exists() else ''
            if PREFIX + ' COMPLETE' in text:
                reason = 'fixture complete'
                break
        else:
            if process.poll() is None:
                reason = 'bounded timeout'
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)
    text = log.read_text(encoding='utf-8-sig', errors='replace') if log.exists() else ''
    errors = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    checkpoints = [line for line in text.splitlines() if PREFIX in line]
    scoped_errors = [line for line in errors.splitlines() if PREFIX in line or 'zzz_ICW_BUILDING_QUEUE' in line]
    result = dict(project='IMPERIA COLD WAR', pid=process.pid, own_pid_only=True,
                  elapsed_seconds=round(time.monotonic() - started, 2), stop_reason=reason,
                  return_code=process.returncode,
                  crashes=[p.name for p in (profile / 'crashes').glob('*') if p.is_dir()],
                  expected_passes=manifest['expected_passes'], passes=sum(PREFIX + ' PASS ' in line for line in checkpoints),
                  failures=[line for line in checkpoints if PREFIX + ' FAIL ' in line],
                  checkpoints=checkpoints, task_errors=scoped_errors,
                  external_error_lines=len(errors.splitlines()) - len(scoped_errors),
                  fixture_immutable=all(digest(addon / rel) == sha for rel, sha in manifest['fixture_hashes'].items()),
                  source_changed_during_run=[rel for rel, sha in manifest['source_hashes'].items() if digest(ROOT / rel) != sha],
                  logs={'game': str(log), 'error': str(error_log)}, scope=manifest['scope'])
    result['native_pass'] = bool(PREFIX + ' COMPLETE' in text and result['passes'] == result['expected_passes'] and not result['failures'] and not scoped_errors and result['fixture_immutable'])
    write(OWN / 'native_result.json', json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checkpoints'}, indent=2), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--duration', type=int, default=600)
    parser.add_argument('--attempt', default='')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--aliases', action='store_true')
    parser.add_argument('--combined', action='store_true')
    args = parser.parse_args()
    CONTROLLED = args.controls
    ALIASES = args.aliases
    COMBINED = args.combined
    if args.attempt:
        assert re.fullmatch(r'[a-zA-Z0-9_-]{1,40}', args.attempt)
        OWN = OWN / args.attempt
    profile = prepare() if args.prepare else OWN / 'profile'
    if args.run:
        run(profile, args.duration)
