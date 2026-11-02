# IMPERIA COLD WAR — Isolated native nonshared building-capacity A/B probe.
"""Use an E: private profile and frozen target providers, without asset copies.

The baseline directory is captured before the production fix. The addon keeps
those providers byte-identical and adds probe-namespaced clones of the real
energy focus's ready/capacity/completion helpers. Only the candidate capacity
predicate changes. No user's save, playset, profile or existing process is used.
"""
from __future__ import annotations

import argparse
import ctypes
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
OWN = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/usa_capacity_20261027')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
DOC = ROOT / 'docs/design/usa_capacity_20261027'
MARK = '# IMPERIA COLD WAR — Isolated USA physical-capacity engine fixture.\n'
PREFIX = 'ICW_USA_CAPACITY'
FID = 'USA_1970_1976_dem_2_a_national_energy_effort'
SHORT = '1976_dem_2_a_national_energy_effort'
STATES = (800, 804, 811)
TRIGGER = 'common/scripted_triggers/COLDWAR_USA_1970_expansion.txt'
EFFECT = 'common/scripted_effects/COLDWAR_USA_1970_expansion.txt'
FROZEN = ('common/buildings/00_buildings.txt', TRIGGER, EFFECT,
          'common/scripted_effects/COLDWAR_USA_1970_legacy_previews.txt',
          'common/national_focus/USA_1970.txt')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, text):
    path = Path(path)
    assert path.absolute().is_relative_to(OWN.absolute()), path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')


def extract(text, key):
    found = re.search(r'(?m)^' + re.escape(key) + r'\s*=\s*\{', text)
    assert found, key
    i = text.index('{', found.start()) + 1
    depth = 1
    while depth:
        depth += (text[i] == '{') - (text[i] == '}')
        i += 1
    return text[found.start():i]


def assertion(name, condition):
    return ('if = { limit = { ' + condition + ' } log = "' + PREFIX + ' PASS ' + name + '" }\n'
            'else = { log = "' + PREFIX + ' FAIL ' + name + '" }\n')


def diagnostic(name, condition):
    return ('if = { limit = { ' + condition + ' } log = "' + PREFIX + ' DIAG ' + name + '=yes" }\n'
            'else = { log = "' + PREFIX + ' DIAG ' + name + '=no" }\n')


def clones():
    trig = (OWN / 'baseline' / TRIGGER).read_text(encoding='utf-8')
    effects = (OWN / 'baseline' / EFFECT).read_text(encoding='utf-8')
    original = {
        'capacity': extract(trig, 'COLDWAR_USA_legacy_capacity_' + FID),
        'ready': extract(trig, 'COLDWAR_USA_legacy_ready_' + FID),
        'complete': extract(effects, 'COLDWAR_USA_legacy_complete_' + FID),
    }
    old = 'free_building_slots = { building = renewable_energy_infra size > 0 }'
    candidate = 'check_variable = { var = building_level@renewable_energy_infra value = 19 compare = less_than_or_equals }'
    assert sum(s.count(old) for s in original.values()) == 6, 'Baseline was not captured before correction'
    assert original['complete'].count('add_extra_state_shared_building_slots = 1') == 3
    assert original['complete'].count('add_building_construction = { type = renewable_energy_infra level = 1 instant_build = yes }') == 3
    result = {}
    for mode in ('baseline', 'candidate'):
        pieces = {}
        for kind, raw in original.items():
            changes = {'COLDWAR_USA_legacy_' + k + '_' + FID: PREFIX + '_' + mode + '_' + k
                       for k in original}
            changes.update({'COLDWAR_USA_legacy_' + receipt + '_' + SHORT: PREFIX + '_' + mode + '_' + receipt
                            for receipt in ('done', 'pending')})
            changes['COLDWAR_USA_legacy_active_' + FID] = PREFIX + '_' + mode + '_active'
            text = raw
            for source, target in sorted(changes.items(), key=lambda p: -len(p[0])):
                text = text.replace(source, target)
            if mode == 'candidate':
                text = text.replace(old, candidate)
            reverse = text.replace(candidate, old) if mode == 'candidate' else text
            for source, target in sorted(changes.items(), key=lambda p: -len(p[1])):
                reverse = reverse.replace(target, source)
            assert reverse == raw, (mode, kind, 'Unintended helper change')
            pieces[kind] = text
        result[mode] = pieces
    return result


def fixture():
    out = [assertion('country_and_scenario', 'tag = USA IMP_is_1970_scenario = yes'),
           diagnostic('fuel_silos_before', 'has_tech = fuel_silos'),
           'set_variable = { ruling_party = 2 }\nset_variable = { treasury = 1000 }\nclr_country_flag = MD_skip_treasury_cost\n',
           assertion('native_democratic_party_guard', 'western_liberals_are_in_power = yes')]
    for sid in STATES:
        out.append(str(sid) + ' = {\nset_variable = { ' + PREFIX + '_before = building_level@renewable_energy_infra }\n'
                   'log = "' + PREFIX + ' DIAG state=' + str(sid) + ' initial_level=[?' + PREFIX + '_before]"\n' +
                   diagnostic('state_' + str(sid) + '_baseline_free_before',
                              'free_building_slots = { building = renewable_energy_infra size > 0 }') +
                   assertion('state_' + str(sid) + '_physical_room_before',
                             'check_variable = { var = building_level@renewable_energy_infra value = 19 compare = less_than_or_equals }') + '}\n')
    out += [diagnostic('baseline_ready_before', PREFIX + '_baseline_ready = yes'),
            assertion('candidate_ready_before', PREFIX + '_candidate_ready = yes'),
            PREFIX + '_baseline_complete = yes\n',
            assertion('baseline_no_charge', 'check_variable = { treasury = 1000 }'),
            assertion('baseline_not_delivered', 'NOT = { has_country_flag = ' + PREFIX + '_baseline_done }')]
    for sid in STATES:
        out.append(assertion('baseline_no_build_' + str(sid), str(sid) + ' = { check_variable = { var = building_level@renewable_energy_infra value = ' + PREFIX + '_before compare = equals } }'))
    out += [PREFIX + '_candidate_complete = yes\n',
            assertion('candidate_fee_25_5_once', 'check_variable = { treasury = 974.5 }'),
            assertion('candidate_receipt', 'has_country_flag = ' + PREFIX + '_candidate_done')]
    for sid in STATES:
        out.append(str(sid) + ' = {\nset_variable = { ' + PREFIX + '_after = building_level@renewable_energy_infra }\n'
                   'set_variable = { ' + PREFIX + '_increase = ' + PREFIX + '_after }\n'
                   'subtract_from_variable = { ' + PREFIX + '_increase = ' + PREFIX + '_before }\n'
                   'log = "' + PREFIX + ' DIAG state=' + str(sid) + ' after_grant=[?' + PREFIX + '_after] increase=[?' + PREFIX + '_increase]"\n' +
                   assertion('candidate_plus_one_' + str(sid), 'check_variable = { ' + PREFIX + '_increase = 1 }') + '}\n')
    out += [PREFIX + '_candidate_complete = yes\n', assertion('repeat_no_charge', 'check_variable = { treasury = 974.5 }')]
    for sid in STATES:
        out.append(assertion('repeat_no_build_' + str(sid), str(sid) + ' = { check_variable = { var = building_level@renewable_energy_infra value = ' + PREFIX + '_after compare = equals } }'))
    out += ['set_technology = { fuel_silos = 1 }\n', assertion('technology_added_for_AB_only', 'has_tech = fuel_silos')]
    for sid in STATES:
        out.append(diagnostic('state_' + str(sid) + '_baseline_free_after_tech', str(sid) + ' = { free_building_slots = { building = renewable_energy_infra size > 0 } }'))
        out.append(assertion('tech_does_not_add_building_' + str(sid), str(sid) + ' = { check_variable = { var = building_level@renewable_energy_infra value = ' + PREFIX + '_after compare = equals } }'))
    out += ['set_variable = { treasury = 1000 }\nclr_country_flag = ' + PREFIX + '_candidate_done\n']
    for sid in STATES:
        out.append(str(sid) + ' = { add_building_construction = { type = renewable_energy_infra level = 20 instant_build = yes } }\n')
        out.append(assertion('state_' + str(sid) + '_cap20_fixture', str(sid) + ' = { check_variable = { var = building_level@renewable_energy_infra value = 20 compare = equals } }'))
    out += [assertion('at_cap_candidate_not_ready', 'NOT = { ' + PREFIX + '_candidate_ready = yes }'),
            PREFIX + '_candidate_complete = yes\n',
            assertion('at_cap_no_charge', 'check_variable = { treasury = 1000 }'),
            assertion('at_cap_no_receipt', 'NOT = { has_country_flag = ' + PREFIX + '_candidate_done }')]
    for sid in STATES:
        out.append(assertion('at_cap_unchanged_' + str(sid), str(sid) + ' = { check_variable = { var = building_level@renewable_energy_infra value = 20 compare = equals } }'))
    out.append('log = "' + PREFIX + ' COMPLETE"\n')
    return ''.join(out)


def prepare():
    assert OWN.is_dir() and (OWN / 'baseline').is_dir(), 'Capture pre-fix baseline first'
    profile = OWN / 'profile'; addon = OWN / 'fixture'
    for rel in FROZEN:
        target = addon / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = (OWN / 'baseline' / rel).read_bytes()
        target.write_bytes(raw)
    # Freeze these direct dependencies too. No asset tree is traversed.
    for rel in ('common/technologies/industry.txt', 'common/scripted_triggers/01_political_triggers.txt',
                'common/scripted_effects/USA_1970_scripted_effects.txt'):
        target = addon / rel; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / rel).read_bytes())
    generated = clones()
    write(addon / 'common/scripted_triggers/zzz_ICW_USA_capacity_probe.txt', MARK + '\n\n'.join(generated[m][k] for m in generated for k in ('capacity', 'ready')) + '\n')
    write(addon / 'common/scripted_effects/zzz_ICW_USA_capacity_probe.txt', MARK + '\n\n'.join(generated[m]['complete'] for m in generated) + '\n')
    write(addon / 'common/on_actions/zzz_ICW_USA_capacity_probe.txt', MARK + 'on_actions = { on_startup = { effect = { USA = { country_event = { id = ICW_USA_CAPACITY.1 hours = 1 } } } } }\n')
    write(addon / 'events/zzz_ICW_USA_capacity_probe.txt', MARK + 'add_namespace = ICW_USA_CAPACITY\ncountry_event = { id = ICW_USA_CAPACITY.1 hidden = yes is_triggered_only = yes immediate = {\n' + fixture() + '} }\n')
    base = '# IMPERIA COLD WAR — Read-only current mod provider for capacity probe.\n' + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + ROOT.as_posix() + '"\n'
    overlay = MARK + 'name="ICW USA capacity probe"\ndependencies={"MD Cold War"}\npath="' + addon.as_posix() + '"\n'
    write(profile / 'mod/base.mod', base); write(profile / 'mod/probe.mod', overlay); write(addon / 'descriptor.mod', overlay)
    write(profile / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/base.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write(profile / 'settings.txt', 'language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    manifest = {'project': 'IMPERIA COLD WAR', 'created_utc': datetime.now(timezone.utc).isoformat(),
                'profile': str(profile), 'asset_mode': 'Existing mod base read by the engine. No asset copy, traversal, counting, archive or junction creation.',
                'frozen_baseline': {rel: digest(OWN / 'baseline' / rel) for rel in FROZEN},
                'fixture_hashes': {str(p.relative_to(addon)).replace('\\', '/'): digest(p) for p in addon.rglob('*') if p.is_file()},
                'source_proof': 'Candidate helpers reverse exactly to original baseline after undoing only probe identifiers and six renewable free-slot predicates. Completion helper unchanged except identifiers. Each actual grant has one shared slot immediately before construction.',
                'slot_observation': 'Three +1 slot commands are source-verified in the exact cloned completion. No unverified native slot-count variable is instrumented.',
                'boundaries': 'Isolated single-process script test; not a UI, save/reload or live multiplayer test.'}
    write(OWN / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    DOC.mkdir(parents=True, exist_ok=True)
    (DOC / 'PREPARE.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'prepared': str(profile), 'manifest_sha256': digest(OWN / 'manifest.json')}), flush=True)
    return profile


def running_game_pids():
    command = "@(Get-Process | Where-Object { $_.ProcessName -eq 'hoi4' } | Select-Object -ExpandProperty Id) | ConvertTo-Json -Compress"
    p = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-Command', command], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
    text = p.stdout.strip()
    value = json.loads(text) if text else []
    return [] if value is None else value if isinstance(value, list) else [value]


def run(profile, duration):
    assert 60 <= duration <= 900
    assert not running_game_pids(), 'Existing hoi4 process found: no launch or termination authorised'
    manifest = json.loads((OWN / 'manifest.json').read_text(encoding='utf-8'))
    addon = OWN / 'fixture'
    assert all(digest(addon / rel) == sha for rel, sha in manifest['fixture_hashes'].items()), 'Frozen fixture changed'
    assert ' ' not in str(profile), 'Private profile path must not contain spaces'
    log = profile / 'logs/game.log'; errors = profile / 'logs/error.log'
    assert not log.exists(), 'Refusing to overwrite an earlier native run'
    startup = subprocess.STARTUPINFO(); startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW; startup.wShowWindow = 0
    args = [str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir=' + str(profile), '-start_tag=USA', '-start_speed=5', '-hands_off']
    started = time.monotonic(); process = subprocess.Popen(args, cwd=GAME, startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps({'pid': process.pid, 'profile': str(profile), 'duration_bound': duration, 'hidden': True}), flush=True)
    reason = 'process exited'
    try:
        while process.poll() is None and time.monotonic() - started < duration:
            time.sleep(1)
            if time.monotonic() - started > 35 and not log.exists():
                reason = 'private profile log not created'; break
            text = log.read_text(encoding='utf-8-sig', errors='replace') if log.exists() else ''
            if PREFIX + ' COMPLETE' in text:
                reason = 'fixture complete'; break
        else:
            if process.poll() is None: reason = 'bounded timeout'
    finally:
        if process.poll() is None:
            process.terminate()
        try: process.wait(timeout=15)
        except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=10)
    text = log.read_text(encoding='utf-8-sig', errors='replace') if log.exists() else ''
    err = errors.read_text(encoding='utf-8-sig', errors='replace') if errors.exists() else ''
    checkpoints = [line for line in text.splitlines() if PREFIX in line]
    task_errors = [line for line in err.splitlines() if any(key in line for key in (PREFIX, 'COLDWAR_USA_1970_expansion.txt', '00_buildings.txt', 'zzz_ICW_USA_capacity_probe'))]
    report = {'project': 'IMPERIA COLD WAR', 'pid': process.pid, 'elapsed_seconds': round(time.monotonic() - started, 2),
              'stop_reason': reason, 'own_pid_only': True, 'checkpoints': checkpoints,
              'expected_passes': 33, 'passes': sum(PREFIX + ' PASS ' in line for line in checkpoints),
              'failures': [line for line in checkpoints if PREFIX + ' FAIL ' in line],
              'task_diagnostics': task_errors, 'external_error_lines': len(err.splitlines()) - len(task_errors),
              'fixture_immutable': all(digest(addon / rel) == sha for rel, sha in manifest['fixture_hashes'].items()),
              'profile': str(profile), 'logs': {'game': str(log), 'error': str(errors)},
              'manifest_sha256': digest(OWN / 'manifest.json'), 'scope': manifest['boundaries'],
              'shared_slots': manifest['slot_observation']}
    report['native_pass'] = (PREFIX + ' COMPLETE' in text and report['passes'] == report['expected_passes'] and not report['failures'] and not task_errors and report['fixture_immutable'])
    write(OWN / 'native_result.json', json.dumps(report, indent=2) + '\n')
    (DOC / 'NATIVE_RESULT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (DOC / 'CHECKPOINTS.txt').write_text('IMPERIA COLD WAR\n\n' + '\n'.join(checkpoints) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'checkpoints'}, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--prepare', action='store_true'); parser.add_argument('--run', action='store_true'); parser.add_argument('--duration', type=int, default=600)
    args = parser.parse_args()
    profile = prepare() if args.prepare else OWN / 'profile'
    if args.run: run(profile, args.duration)
