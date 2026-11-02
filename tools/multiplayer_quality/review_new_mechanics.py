# IMPERIA COLD WAR — Scoped regression capture for the October 25 mechanics review.
"""Run inspected checks; capture evidence and detect unintended runtime writes."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/audits/new_mechanics_20261025'


def runtime_hashes():
    result = {}
    for folder in ['common', 'events', 'history', 'interface', 'localisation/english']:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and path.suffix in {'.txt', '.gui', '.gfx', '.yml', '.lua'}:
                result[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def tasks(related=False):
    if related:
        scripts = ['tools/space_race_1970/validate.py']
        scripts += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'tools/space_race_1970').glob('qa_*.py'))]
        scripts += [
            'tools/colonial_affairs/validate.py', 'tools/colonial_affairs/test_runtime.py',
            'tools/nuclear_intelligence/test_runtime.py', 'tools/cold_war_gc/test_controls.py',
            'tools/gc_unsc/test_session_seats.py', 'tools/economic_organisation/validate.py',
            'tools/multiplayer_quality/test_quality.py', 'tools/multiplayer_quality/test_open_findings.py',
        ]
        return [(path, [path]) for path in scripts]
    scripts = [
        'tools/comecon/validate.py',
        'tools/superpower_dossier/validate.py',
        'tools/superpower_dossier/behavior_tests.py',
        'tools/superpower_dossier/test_treaties.py',
        'tools/ssr_1970/validate.py',
        'tools/naval_adaptation_1970/validate.py',
        'tools/usa_1970_expansion/validate.py',
        'tools/usa_1970_expansion/test_gulf_precision.py',
        'tools/usa_1970_quality/test_presentation.py',
        'tools/quaza_nuclear_integration/test_integration.py',
        'tools/cuba_1970/validate.py',
        'tools/iraq_1970/test_gulf_access_20261025.py',
        'tools/iraq_1970/test_gulf_counterplay.py',
        'tools/iraq_1970/test_gulf_previews.py',
        'tools/uae_1970/test_specialists.py',
        'tools/uae_1970/test_focus_runtime.py',
        'tools/uae_1970/test_presentation.py',
        'tools/uae_1970/test_revision.py',
    ]
    commands = [(path, [path]) for path in scripts]
    for folder in ['ssr_1970/tests', 'naval_adaptation_1970', 'usa_1970_expansion']:
        commands.append((folder, ['-m', 'unittest', 'discover', '-s', 'tools/' + folder, '-p', 'test_*.py', '-v']))
    return commands


def run_task(task):
    name, args = task
    started = time.monotonic()
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    try:
        process = subprocess.run([sys.executable, '-X', 'utf8', *args], cwd=ROOT, env=env,
                                 capture_output=True, encoding='utf-8', errors='replace', timeout=240)
        output, code = process.stdout + process.stderr, process.returncode
    except subprocess.TimeoutExpired as error:
        output, code = 'Check timed out: ' + str(error), -1
    log = OUT / 'test_logs' / (name.replace('/', '__') + '.log')
    log.write_text('IMPERIA COLD WAR: current-source mechanics check\n' + output, encoding='utf-8')
    match = re.search(r'Ran (\d+) tests? in ', output)
    return {'name': name, 'arguments': args, 'exit_code': code, 'seconds': round(time.monotonic()-started, 2),
            'unittest_cases': int(match[1]) if match else None,
            'log': log.relative_to(ROOT).as_posix(), 'failure_tail': output[-4000:] if code else None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'test_logs').mkdir(exist_ok=True)
    before = runtime_hashes()
    results = []
    related = '--related' in sys.argv
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(run_task, task) for task in tasks(related)]):
            result = future.result()
            results.append(result)
            print(('PASS ' if result['exit_code'] == 0 else 'FAIL ') + result['name'], flush=True)
    after = runtime_hashes()
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    report = {'project': 'IMPERIA COLD WAR', 'results': sorted(results, key=lambda x:x['name']),
              'runtime_files_checked': len(before), 'runtime_changed_by_checks': changed,
              'live_multiplayer_tested': False, 'native_engine_tested': False}
    (OUT / ('related_regressions.json' if related else 'regressions.json')).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'executed': len(results), 'passed': sum(x['exit_code']==0 for x in results),
                      'failed': [x['name'] for x in results if x['exit_code']], 'runtime_changed': changed}), flush=True)


if __name__ == '__main__':
    main()
