# IMPERIA COLD WAR — Isolated native loading and calendar smoke test.
"""Launch an isolated hidden HOI4 profile and report only observed checkpoints."""
import json
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
RUNTIME = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/multiplayer_quality')
PROFILE = RUNTIME / 'profile'
OUT = ROOT / 'docs/audits/multiplayer_quality_20261023'
MARKER = '# IMPERIA COLD WAR — Isolated mechanics smoke test.\n'


def write(relative, source):
    path = PROFILE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding='utf-8', newline='\n')


def main():
    global OUT
    if '--out-dir' in sys.argv:
        OUT = ROOT / sys.argv[sys.argv.index('--out-dir') + 1]
        assert OUT.resolve().is_relative_to((ROOT / 'docs/audits').resolve())
    duration = int(sys.argv[sys.argv.index('--duration') + 1]) if '--duration' in sys.argv else 600
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'native_result.json').exists():
        index = 1
        while (OUT / f'native_attempt_{index}.json').exists():
            index += 1
        for name, suffix in [('native_result.json', '.json'), ('native_error.log', '_error.log'), ('native_game.log', '_game.log')]:
            path = OUT / name
            if path.exists():
                (OUT / f'native_attempt_{index}{suffix}').write_bytes(path.read_bytes())
    # Freeze runtime scripts before launching. Live editing with -debug caused
    # database reloads in earlier attempts and is not a controlled soak test.
    use_snapshot = '--snapshot' in sys.argv
    snapshot = (Path(sys.argv[sys.argv.index('--snapshot') + 1]) if use_snapshot else
                RUNTIME / ('engine_snapshot_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')))
    copied = {'common', 'events', 'history', 'interface', 'localisation', 'portraits'}
    ignored = {'tools', 'docs', 'Claude outputs', '.git', '.codex', '.agents', '__pycache__', 'rollback_backups'}
    assets = {'gfx', 'map', 'sound', 'music'}
    if not use_snapshot:
        snapshot.mkdir(parents=True)
        for entry in ROOT.iterdir():
            target = snapshot / entry.name
            if entry.is_dir():
                if entry.name not in ignored | assets and not entry.name.startswith('.'):
                    shutil.copytree(entry, target)
            elif entry.suffix in {'.mod', '.txt', '.lua'}:
                shutil.copy2(entry, target)
        print(json.dumps({'prepared_snapshot': str(snapshot), 'asset_junctions_required': sorted(assets)}), flush=True)
        return
    assert snapshot.resolve().is_relative_to(RUNTIME.resolve())
    assert all((snapshot / name).is_dir() for name in copied | assets), 'Incomplete runtime snapshot'
    source_hashes = {p.relative_to(snapshot).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                     for name in copied for p in (snapshot / name).rglob('*') if p.is_file()}
    write('.gitignore', MARKER + '*\n')
    write('mod/mdcoldwar.mod', MARKER + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + f'\npath="{snapshot.as_posix()}"\n')
    addon = MARKER + f'name="IMPERIA quality probe"\ndependencies={{ "MD Cold War" }}\npath="{(PROFILE / "fixture").as_posix()}"\n'
    write('mod/probe.mod', addon)
    write('fixture/descriptor.mod', addon)
    write('dlc_load.json', json.dumps({'enabled_mods': ['mod/mdcoldwar.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write('settings.txt', MARKER + 'language="l_english"\ngraphics={size={x=1024 y=720} fullScreen=no borderless=no}\nmaster_volume=0\n')
    write('fixture/common/on_actions/zzzzzzzzzz_IMPERIA_quality_probe.txt', MARKER + '''on_actions = {
 on_startup = { effect = {
  log = "ICW_QUALITY STARTUP"
  USA = { country_event = { id = ICW_QUALITY.1 hours = 1 } }
 } }
 on_daily_USA = { effect = {
  if = { limit = { NOT = { has_country_flag = ICW_QUALITY_first_day } }
   set_country_flag = ICW_QUALITY_first_day
   log = "ICW_QUALITY FIRST_DAY"
  }
 } }
 on_weekly_USA = { effect = { log = "ICW_QUALITY WEEK treasury=[?treasury] tension=[?global.mdcw_cw_tension]" } }
 on_monthly_USA = { effect = {
  add_to_variable = { ICW_QUALITY_months = 1 }
  log = "ICW_QUALITY MONTH count=[?ICW_QUALITY_months] treasury=[?treasury]"
  if = { limit = { check_variable = { ICW_QUALITY_months > 2 } } log = "ICW_QUALITY COMPLETE" }
 } }
}
''')
    write('fixture/common/on_actions/000_IMPERIA_quality_probe.txt', MARKER + '''on_actions = {
 on_startup = { effect = { log = "ICW_QUALITY EARLY_STARTUP" } }
}
''')
    write('fixture/events/ICW_quality_probe.txt', MARKER + '''add_namespace = ICW_QUALITY
country_event = { id = ICW_QUALITY.1 hidden = yes is_triggered_only = yes immediate = {
 log = "ICW_QUALITY FIRST_HOUR"
 if = { limit = { has_global_flag = mdcw_cw_initialized } log = "ICW_QUALITY EQUILIBRIUM_INITIALIZED" }
 if = { limit = { has_country_flag = cw_sr_initialized } log = "ICW_QUALITY SPACE_INITIALIZED" }
} }
''')
    if '--recognition-test' in sys.argv:
        write('fixture/events/ICW_quality_probe.txt', MARKER + '''add_namespace = ICW_QUALITY
country_event = { id = ICW_QUALITY.1 hidden = yes is_triggered_only = yes immediate = {
 log = "ICW_QUALITY FIRST_HOUR"
 set_temp_variable = { ICW_QUALITY_inline = { value = 0 every_collection = { named_collection = un_general_assembly_members_collection add = 1 } } }
 set_temp_variable = { ICW_QUALITY_explicit = 0 }
 every_collection_element = {
  input = { input = collection:un_general_assembly_members_collection }
  PREV = { add_to_temp_variable = { ICW_QUALITY_explicit = 1 } }
 }
 log = "ICW_QUALITY UN inline=[?ICW_QUALITY_inline] explicit=[?ICW_QUALITY_explicit]"
 BUL = {
  clr_country_flag = un_ascension_eligible_notified
  set_variable = { Granted_Recognition = 0 }
  recognition_grant_increment = yes
  log = "ICW_QUALITY UN_LOW threshold=[?recog_threshold] recognitions=[?Granted_Recognition]"
  if = { limit = { has_country_flag = un_ascension_eligible_notified } log = "ICW_QUALITY FAIL_LOW" }
  else = { log = "ICW_QUALITY PASS_LOW" }
  set_variable = { Granted_Recognition = 1000 }
  recognition_grant_increment = yes
  if = { limit = { has_country_flag = un_ascension_eligible_notified } log = "ICW_QUALITY PASS_HIGH" }
  else = { log = "ICW_QUALITY FAIL_HIGH" }
 }
 log = "ICW_QUALITY COMPLETE"
} }
''')
    if '--nuclear-test' in sys.argv:
        assert '--recognition-test' in sys.argv
        event_path = PROFILE / 'fixture/events/ICW_quality_probe.txt'
        event_source = event_path.read_text(encoding='utf-8')
        nuclear = '''set_temp_variable = { ICW_QUALITY_old_gdpc = gdp_per_capita }
 set_temp_variable = { ICW_QUALITY_old_inflation = inflation_multiplier }
 set_temp_variable = { ICW_QUALITY_old_nuclear_cost = COLDWAR_nuclear_development_weekly_cost }
 set_variable = { gdp_per_capita = 36 }
 set_variable = { inflation_multiplier = 1 }
 set_temp_variable = { COLDWAR_nuclear_development_weekly_base = 0.2 }
 COLDWAR_price_nuclear_development_budget = yes
 log = "ICW_QUALITY NUCLEAR_WEEKLY_COST=[?COLDWAR_nuclear_development_weekly_cost]"
 if = { limit = { check_variable = { COLDWAR_nuclear_development_weekly_cost = 0.2 } } log = "ICW_QUALITY PASS_NUCLEAR" }
 else = { log = "ICW_QUALITY FAIL_NUCLEAR" }
 set_variable = { gdp_per_capita = ICW_QUALITY_old_gdpc }
 set_variable = { inflation_multiplier = ICW_QUALITY_old_inflation }
 set_variable = { COLDWAR_nuclear_development_weekly_cost = ICW_QUALITY_old_nuclear_cost }
 '''
        event_source = event_source.replace('log = "ICW_QUALITY COMPLETE"', nuclear + 'log = "ICW_QUALITY COMPLETE"')
        write('fixture/events/ICW_quality_probe.txt', event_source)
    overlay_hashes = {}
    for flag, relative in [('--chi-opinion-test', 'common/national_focus/CHI_1985.txt'),
                           ('--nuclear-test', 'common/scripted_effects/COLDWAR_nuclear_development_budget.txt'),
                           ('--nuclear-test', 'common/synchronized_dynamic_tokens/ICW_nuclear_power_tokens.txt')]:
        overlay = PROFILE / 'fixture' / relative
        if flag in sys.argv:
            write('fixture/' + relative, (ROOT / relative).read_text(encoding='utf-8'))
            overlay_hashes[relative] = hashlib.sha256(overlay.read_bytes()).hexdigest()
        elif overlay.exists():
            overlay.unlink()
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    arguments = [str(GAME / 'hoi4.exe'), '-noasserts', '-assertsdialog=no',
                 '-userdir=' + str(PROFILE), '-start_tag=USA', '-start_speed=5', '-hands_off']
    run_id = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    # Never let a previous run's COMPLETE line satisfy this run's stop condition.
    for name in ('game.log', 'error.log'):
        path = PROFILE / 'logs' / name
        if path.exists():
            archived = path.with_name(run_id + '_previous_' + name)
            assert archived.resolve().is_relative_to(PROFILE.resolve())
            path.rename(archived)
    started = time.monotonic()
    process = subprocess.Popen(arguments, cwd=GAME, startupinfo=startup)
    print(json.dumps({'pid': process.pid, 'profile': str(PROFILE)}), flush=True)
    game_log = PROFILE / 'logs/game.log'
    observed = ''
    try:
        while process.poll() is None and time.monotonic() - started < duration:
            time.sleep(1)
            observed = game_log.read_text(encoding='utf-8-sig', errors='replace') if game_log.exists() else ''
            if 'ICW_QUALITY COMPLETE' in observed:
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
    error_log = PROFILE / 'logs/error.log'
    errors = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'native_error.log').write_text('IMPERIA COLD WAR: native engine diagnostics\n' + errors, encoding='utf-8')
    (OUT / 'native_game.log').write_text('IMPERIA COLD WAR: native engine checkpoints\n' + observed, encoding='utf-8')
    report = {'project': 'IMPERIA COLD WAR', 'run_id': run_id, 'elapsed_seconds': round(time.monotonic() - started, 1),
              'return_code': process.returncode, 'stopped_by_probe': stopped,
              'checkpoints': [line for line in observed.splitlines() if 'ICW_QUALITY' in line],
              'probe_mode': 'recognition' if '--recognition-test' in sys.argv else 'calendar',
              'calendar_complete': '--recognition-test' not in sys.argv and 'ICW_QUALITY COMPLETE' in observed,
              'recognition_passed': '--recognition-test' in sys.argv and all(
                  marker in observed for marker in ('ICW_QUALITY PASS_LOW', 'ICW_QUALITY PASS_HIGH'))
                  and 'ICW_QUALITY FAIL_' not in observed,
              'nuclear_budget_passed': '--nuclear-test' in sys.argv and 'ICW_QUALITY PASS_NUCLEAR' in observed
                  and 'ICW_QUALITY FAIL_NUCLEAR' not in observed,
              'error_lines': len(errors.splitlines()), 'live_multiplayer_tested': False,
              'save_reload_tested': False, 'snapshot': str(snapshot),
              'frozen_source_files': len(source_hashes), 'source_snapshot_unchanged': all(
                  hashlib.sha256((snapshot / relative).read_bytes()).hexdigest() == digest
                  for relative, digest in source_hashes.items()),
              'source_overlays': overlay_hashes,
              'source_overlays_unchanged': all(hashlib.sha256((PROFILE / 'fixture' / relative).read_bytes()).hexdigest() == digest
                                             for relative, digest in overlay_hashes.items()),
              'last_observed_game_date': next(iter(__import__('re').findall(r'\[(1970\.[0-9.]+)\]', observed)[-1:]), None)}
    (OUT / 'native_result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
