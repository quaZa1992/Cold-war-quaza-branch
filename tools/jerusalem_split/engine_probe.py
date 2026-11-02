# IMPERIA COLD WAR — Isolated native map, capital and transfer probe on E:.
"""Freeze scripts and map once. Never alter the user's profile or active game."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import time

from integrate import ROOT, OUT, MARK, sha

GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUNTIME = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/jerusalem_split')

FIXTURE = '''add_namespace = ICW_JERUSALEM_PROBE
country_event = { id = ICW_JERUSALEM_PROBE.1 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { owns_state = 207 controls_state = 207 owns_state = 1253 controls_state = 1253
  207 = { is_core_of = ISR is_core_of = PAL } 1253 = { is_core_of = ISR is_core_of = PAL } }
  log = "ICW_JERUSALEM_PROBE PASS initial_owner_core" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL initial_owner_core" }
 if = { limit = { 1253 = { is_capital = yes } 207 = { is_capital = no } }
  log = "ICW_JERUSALEM_PROBE PASS western_capital" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL western_capital" }
 if = { limit = { 207 = { landmark_domeofrock > 0 landmark_jerusalem_western_wall > 0 }
  1253 = { NOT = { landmark_domeofrock > 0 } NOT = { landmark_jerusalem_western_wall > 0 } } }
  log = "ICW_JERUSALEM_PROBE PASS landmarks_east_only" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL landmarks_east_only" }
 if = { limit = { 1253 = { check_variable = { productivity_state_var = 655.667 } } check_variable = { gdp_total > 0 } }
  log = "ICW_JERUSALEM_PROBE PASS startup_productivity_and_gdp" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL startup_productivity_and_gdp" }
 207 = { log = "ICW_JERUSALEM_PROBE EAST name=[This.GetName] population_k=[?state_population_k] productivity=[?productivity_state_var]" }
 1253 = { log = "ICW_JERUSALEM_PROBE WEST name=[This.GetName] population_k=[?state_population_k] productivity=[?productivity_state_var]" }
 PAL = { transfer_state = 207 }
 DDR = { transfer_state = 1252 }
 country_event = { id = ICW_JERUSALEM_PROBE.2 hours = 1 }
} }
country_event = { id = ICW_JERUSALEM_PROBE.2 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { 207 = { is_owned_and_controlled_by = PAL } 1253 = { is_owned_and_controlled_by = ISR is_capital = yes } }
  log = "ICW_JERUSALEM_PROBE PASS isolated_eastern_transfer" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL isolated_eastern_transfer" }
 if = { limit = { 1252 = { is_owned_and_controlled_by = DDR is_core_of = CUB NOT = { is_core_of = DDR } }
  1251 = { is_owned_and_controlled_by = GER } 45 = { is_owned_and_controlled_by = DDR } 1241 = { is_owned_and_controlled_by = PER } }
  log = "ICW_JERUSALEM_PROBE PASS cayo_berlin_kharg_independent" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL cayo_berlin_kharg_independent" }
 transfer_state = 207
 CUB = { transfer_state = 1252 }
 country_event = { id = ICW_JERUSALEM_PROBE.3 hours = 1 }
} }
country_event = { id = ICW_JERUSALEM_PROBE.3 hidden = yes is_triggered_only = yes immediate = {
 if = { limit = { 207 = { is_owned_and_controlled_by = ISR } 1253 = { is_owned_and_controlled_by = ISR is_capital = yes }
  1252 = { is_owned_and_controlled_by = CUB has_state_flag = COLDWAR_CUB_cayo_blanco_del_sur } }
  log = "ICW_JERUSALEM_PROBE PASS restored_owners_and_capital" }
 else = { log = "ICW_JERUSALEM_PROBE FAIL restored_owners_and_capital" }
 log = "ICW_JERUSALEM_PROBE COMPLETE"
} }
'''


def copy_tree(source, target):
    """Walk only real directories; never follow asset junctions into another tree."""
    target.mkdir(parents=True)
    count = 0
    for current, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(current) / d).is_junction() and not (Path(current) / d).is_symlink()]
        destination = target / Path(current).relative_to(source)
        destination.mkdir(parents=True, exist_ok=True)
        for name in files:
            path = Path(current) / name
            if path.is_symlink():
                continue
            shutil.copy2(path, destination / name)
            count += 1
    return count


def main():
    active = subprocess.run(['powershell', '-NoProfile', '-Command', "Get-Process hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"], capture_output=True, text=True)
    assert not active.stdout.strip(), 'An existing HOI4 process is running; no second game was launched'
    prior = OUT / 'native_report.json'
    if prior.exists():
        index = 1
        while (OUT / f'native_attempt_{index}.json').exists():
            index += 1
        target = OUT / f'native_attempt_{index}.json'
        assert prior.resolve().parent == target.resolve().parent == OUT.resolve()
        prior.rename(target)
    run = RUNTIME / ('native_' + str(time.time_ns()))
    snapshot, profile = run / 'snapshot', run / 'profile'
    snapshot.mkdir(parents=True)
    copied = {}
    for name in ['common', 'events', 'history', 'interface', 'localisation', 'portraits', 'map']:
        copied[name] = copy_tree(ROOT / name, snapshot / name)
    for entry in ROOT.iterdir():
        if entry.is_file() and entry.suffix in ('.txt', '.mod', '.lua'):
            shutil.copy2(entry, snapshot / entry.name)
    for name in ['gfx', 'music', 'sound']:
        subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(snapshot / name), str(ROOT / name)], check=True, capture_output=True)
    installed = json.loads((OUT / 'installation.json').read_text())
    hashes = {}
    for relative, digest in installed['outputs'].items():
        hashes[relative] = sha((snapshot / relative).read_bytes())
        assert hashes[relative] == digest, 'Snapshot input changed: ' + relative

    def write(relative, content):
        path = profile / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8', newline='\n')

    write('mod/mdcoldwar.mod', MARK + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + f'\npath="{snapshot.as_posix()}"\n')
    addon = MARK + f'name="IMPERIA Jerusalem probe"\ndependencies={{ "MD Cold War" }}\npath="{(profile / "fixture").as_posix()}"\n'
    write('mod/probe.mod', addon)
    write('fixture/descriptor.mod', addon)
    write('dlc_load.json', json.dumps({'enabled_mods': ['mod/mdcoldwar.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write('settings.txt', MARK + 'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/events/ICW_jerusalem_probe.txt', MARK + FIXTURE)
    write('fixture/common/on_actions/zzzzzzzz_ICW_jerusalem_probe.txt', MARK + '''on_actions = { on_startup = { effect = {
 log = "ICW_JERUSALEM_PROBE STARTUP"
 ISR = { country_event = { id = ICW_JERUSALEM_PROBE.1 hours = 1 } }
} } }
''')
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.monotonic()
    process = subprocess.Popen([str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no',
                               '-userdir=' + str(profile), '-start_tag=ISR', '-start_speed=2', '-hands_off'],
                               cwd=GAME, startupinfo=startup)
    print(json.dumps({'pid': process.pid, 'profile': str(profile), 'copied_files': copied}), flush=True)
    game_log, error_log = profile / 'logs/game.log', profile / 'logs/error.log'
    log = ''
    try:
        while process.poll() is None and time.monotonic() - started < 720:
            time.sleep(1)
            log = game_log.read_text(encoding='utf-8-sig', errors='replace') if game_log.exists() else ''
            if 'ICW_JERUSALEM_PROBE COMPLETE' in log:
                break
    finally:
        stopped = process.poll() is None
        if stopped:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    errors = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    relevant = [line for line in errors.splitlines() if re.search(r'ICW_JERUSALEM|ICW_jerusalem|ICW_COMECON_hubs|1253-West|16538|West Jerusalem|East Jerusalem|Jerusalem split|landmark_domeofrock|landmark_jerusalem_western_wall', line)]
    checkpoints = [line for line in log.splitlines() if 'ICW_JERUSALEM_PROBE' in line]
    expected = ['initial_owner_core', 'western_capital', 'landmarks_east_only', 'startup_productivity_and_gdp',
                'isolated_eastern_transfer', 'cayo_berlin_kharg_independent', 'restored_owners_and_capital']
    report = {'project': 'IMPERIA COLD WAR', 'scope': 'Frozen current scripts and full map, one native client; no MP or save/reload claim',
              'profile': str(profile), 'copied_files': copied, 'feature_hashes': hashes, 'elapsed_seconds': round(time.monotonic() - started, 1),
              'checkpoints': checkpoints, 'relevant_error_lines': relevant, 'all_error_lines': len(errors.splitlines()),
              'completed': 'ICW_JERUSALEM_PROBE COMPLETE' in log, 'stopped_by_probe': stopped, 'returncode': process.returncode}
    report['success'] = report['completed'] and all('ICW_JERUSALEM_PROBE PASS ' + name in log for name in expected) and 'ICW_JERUSALEM_PROBE FAIL' not in log and not relevant
    (OUT / 'native_report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)
    raise SystemExit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
