# IMPERIA COLD WAR — isolated Cuba implementation engine checks.
"""Task-owned profile and fixture. Never changes the user's playset or saves."""
from pathlib import Path
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
ISLANDS = '--islands' in sys.argv
PROFILE = HERE/('runtime/engine_profile_1972' if ISLANDS else 'runtime/engine_profile')
EXPECTED = []
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, emit


def write(rel, text):
    p = PROFILE/rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def check(name, condition):
    EXPECTED.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "COLDWAR_CUB_ENGINE PASS {name}" }} else = {{ log = "COLDWAR_CUB_ENGINE FAIL {name}" }}\n'




def decision_payload(key, actor=None, filename='COLDWAR_CUB_1970_diplomacy.txt'):
    """Execute the installed transaction with its decision actor bound explicitly.

    An on_startup country scope has no country decision ROOT. Bind the literal
    ROOT operands in the extracted decision to its fixed recipient, preserving
    the exact live guard (Cuba must not be at war with that recipient). Called
    external helpers retain their own native scope requirements; this fixture
    does not certify those helpers' event/decision ROOT behaviour.
    """
    actor = actor or ('SOV' if key.endswith('soviet_assistance') else
                     'USA' if '_us_' in key else 'DDR')
    def bind_root(rows):
        return [(k, op, bind_root(v) if isinstance(v, list) else actor if v == 'ROOT' else v)
                for k, op, v in rows]
    ast = parse((ROOT/'common/decisions'/filename).read_text(encoding='utf-8'))
    for _, _, category in ast:
        for ident, _, decision in category:
            if ident == key:
                return emit(bind_root(first(decision, 'complete_effect')))
    raise KeyError(key)






def fixture():
    from engine_foreign_fixture import build, build_islands
    return (build_islands if ISLANDS else build)(check, decision_payload, event_option_payload)


def event_option_payload(key, actor):
    """Execute the emitted accept option, including its real guarded helper."""
    from foreign_contracts import PARTNER_NODES, _offer_event_id
    ident = 'COLDWAR_CUB_foreign_contracts.'+str(_offer_event_id(PARTNER_NODES['foreign_'+key]))
    ast = parse((ROOT/'events/COLDWAR_CUB_1970_foreign_contracts.txt').read_text(encoding='utf8'))
    for kind, _, event in ast:
        if kind != 'country_event' or first(event, 'id') != ident:
            continue
        for name, _, option in event:
            if name == 'option' and first(option, 'name') == 'COLDWAR_CUB_foreign_contracts.'+key+'.accept':
                return emit([(k, op, v) for k, op, v in option if k not in ('name','trigger','ai_chance')])
    raise KeyError(ident)


def main():
    write('.gitignore', '*\n')
    descriptor = (ROOT/'descriptor.mod').read_text(encoding='utf-8-sig')+'\npath="'+ROOT.as_posix()+'"\n'
    write('mod/mdcoldwar.mod', descriptor)
    addon = 'name="COLDWAR Cuba isolated engine fixture"\ndependencies={ "MD Cold War" }\npath="'+(PROFILE/'fixture').as_posix()+'"\n'
    write('mod/cuba_probe.mod', addon)
    write('fixture/descriptor.mod', addon)
    if ISLANDS:
        # IMPERIA COLD WAR — Isolated future-date guard test, not a campaign override.
        bookmarks = (ROOT/'common/bookmarks/blitzkrieg.txt').read_text(encoding='utf-8-sig')
        write('fixture/common/bookmarks/blitzkrieg.txt', bookmarks.replace('date = 1970.1.1.12', 'date = 1972.6.20.12', 1))
        write('fixture/common/scripted_triggers/IMP_cold_war_scenario_triggers.txt',
              '# IMPERIA COLD WAR — Fixture-only 1970 routing at a future test date.\n'
              'IMP_is_1970_scenario = { has_start_date > 1972.6.19 has_start_date < 1972.6.22 }\n'
              'IMP_is_1985_scenario = { has_start_date > 1984.12.31 has_start_date < 1985.1.2 }\n')
    write('dlc_load.json', json.dumps({'enabled_mods': ['mod/mdcoldwar.mod', 'mod/cuba_probe.mod'], 'disabled_dlcs': []}))
    write('settings.txt', 'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    write('fixture/common/scripted_effects/COLDWAR_CUB_ENGINE.txt', fixture())
    from engine_foreign_fixture import EMBARGO_EVENTS, DELIVERY_EXPECTED, NAME_EXPECTED
    write('fixture/events/COLDWAR_CUB_ENGINE.txt', '# IMPERIA COLD WAR — native embargo tests with the sender as event ROOT.\nadd_namespace = COLDWAR_CUB_ENGINE\n'+EMBARGO_EVENTS)
    write('fixture/common/on_actions/zzzzzz_COLDWAR_CUB_ENGINE.txt', '# IMPERIA COLD WAR — isolated probe hook, after the native startup setup.\non_actions = { on_startup = { effect = { log = "COLDWAR_CUB_ENGINE STARTUP" CUB = { COLDWAR_CUB_ENGINE_run = yes } } } }\n')
    for filename in ['game.log', 'error.log']:
        write('logs/'+filename, '')
    args = [str(GAME/'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir='+str(PROFILE), '-start_tag=CUB', '-start_speed=2', '-hands_off']
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.monotonic()
    process = subprocess.Popen(args, cwd=GAME, startupinfo=startup)
    write('process.json', json.dumps({'pid': process.pid, 'args': args}, indent=2))
    print(json.dumps({'pid': process.pid, 'profile': str(PROFILE)}), flush=True)
    game_log, error_log = PROFILE/'logs/game.log', PROFILE/'logs/error.log'
    complete_seen = None
    try:
        while process.poll() is None and time.monotonic()-started < 540:
            time.sleep(1)
            logs = game_log.read_text(encoding='utf-8-sig', errors='replace') if game_log.exists() else ''
            if 'COLDWAR_CUB_ENGINE COMPLETE' in logs:
                if complete_seen is None:
                    complete_seen = time.monotonic()
                # Triggered offers may arrive after the startup effect stack unwinds.
                arrived = all('COLDWAR_CUB_EVENT_DELIVERED '+entry in logs for entry in DELIVERY_EXPECTED)
                if arrived:
                    break
                if time.monotonic()-complete_seen > 35:
                    break
    finally:
        stopped_by_probe = process.poll() is None
        if stopped_by_probe:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    logs = game_log.read_text(encoding='utf-8-sig', errors='replace') if game_log.exists() else ''
    error_text = error_log.read_text(encoding='utf-8-sig', errors='replace') if error_log.exists() else ''
    lines = error_text.splitlines()
    relevant = []
    for i, line in enumerate(lines):
        if 'COLDWAR_CUB' in line and 'Reloading Events:' not in line:
            relevant += lines[max(0, i-1):i+3]
    passed = [name for name in EXPECTED if 'COLDWAR_CUB_ENGINE PASS '+name in logs]
    skipped = [name for name in EXPECTED if 'COLDWAR_CUB_ENGINE SKIP '+name+' ' in logs]
    failed = [name for name in EXPECTED if name not in passed and name not in skipped]
    delivered = [entry for entry in DELIVERY_EXPECTED if 'COLDWAR_CUB_EVENT_DELIVERED '+entry in logs]
    delivery_missing = [entry for entry in DELIVERY_EXPECTED if entry not in delivered]
    native_names = [entry for entry in NAME_EXPECTED if 'COLDWAR_CUB_STATE_NAME '+entry in logs]
    names_missing = [entry for entry in NAME_EXPECTED if entry not in native_names]
    report = dict(scope=('Native 1972 island transactions with fixture-only future bookmark and 1970 scenario routing override.' if ISLANDS else 'Native 1970 start and fixture execution of loaded Cuba code; no multiplayer, manual hover or save/reload claim.'),
                  elapsed_seconds=round(time.monotonic()-started, 1), completed='COLDWAR_CUB_ENGINE COMPLETE' in logs,
                  expected=len(EXPECTED), executed=len(EXPECTED)-len(skipped), passed=passed, skipped=skipped, failed=failed, relevant_errors=list(dict.fromkeys(relevant)),
                  checkpoints=[line for line in logs.splitlines() if 'COLDWAR_CUB_ENGINE' in line], returncode=process.returncode,
                  event_delivery_expected=DELIVERY_EXPECTED, event_delivered=delivered, event_delivery_missing=delivery_missing,
                  native_state_names=native_names, native_state_names_missing=names_missing,
                  stopped_by_probe=stopped_by_probe,
                  agreement_scope='Installed response ASTs execute with literal decision ROOT operands bound to the fixed recipient. Real installed focus apply helpers issue offers; fixtures seed prerequisite receipts and use hypothetical partner independence/government setup. The future island fixture overrides only its private bookmark and 1970 scenario routing. Manual tooltips, a real save/load cycle and multiplayer are not covered.')
    report['success'] = report['completed'] and not failed and not relevant and not delivery_missing and not names_missing
    report_path = HERE/('ENGINE_REPORT_1972.json' if ISLANDS else 'ENGINE_REPORT.json')
    report_path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('success', 'completed', 'expected', 'executed', 'passed', 'skipped', 'failed', 'elapsed_seconds', 'returncode')}
                     | {'relevant_error_count': len(report['relevant_errors']), 'events_delivered':len(delivered), 'event_delivery_missing':delivery_missing, 'report': str(report_path)}, indent=2), flush=True)


if __name__ == '__main__':
    main()
