# IMPERIA COLD WAR — Multiplayer mechanics quality audit.
"""Source inventory and existing regression runner, not a live network test."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / 'docs/audits/multiplayer_quality_20261023'
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import TOKEN, walk, first


def parse(source):
    """Read native anonymous lists and typed colour blocks as well as scripts."""
    tokens = [m[0] for m in TOKEN.finditer(source) if not m[0].startswith('#')]
    position = 0

    def block(nested=False):
        nonlocal position
        rows = []
        while position < len(tokens):
            key = tokens[position]
            position += 1
            if key == '}':
                if not nested:
                    raise ValueError('Unexpected closing brace')
                return rows
            if key == '{':
                rows.append(('_anonymous', '=', block(True)))
                continue
            if position < len(tokens) and tokens[position] in {'=', '<', '>', '<=', '>=', '!='}:
                operator = tokens[position]
                position += 1
                if position == len(tokens):
                    raise ValueError('Missing value')
                value = tokens[position]
                position += 1
                if value == '{':
                    value = block(True)
                elif value == '}':
                    raise ValueError('Missing value before closing brace')
                elif value in {'rgb', 'hsv', 'hsv360'} and position < len(tokens) and tokens[position] == '{':
                    position += 1
                    value = [('_type', '=', value), *block(True)]
                rows.append((key, operator, value))
            else:
                rows.append(('_bare', '=', key))
        if nested:
            raise ValueError('Unclosed block')
        return rows

    return block()


def save(name, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps({'project': 'IMPERIA COLD WAR', **value}, indent=2) + '\n', encoding='utf-8')


def inventory():
    files = {}
    for directory in ['common', 'events', 'interface', 'localisation/english', 'tools']:
        for path in (ROOT / directory).rglob('*'):
            if not path.is_file() or any(part in {'.vendor', '__pycache__'} or part.startswith('runtime') for part in path.relative_to(ROOT).parts):
                continue
            if path.suffix not in {'.txt', '.gui', '.gfx', '.yml', '.py'}:
                continue
            files[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    save('source_baseline.json', {'created_utc': datetime.now(timezone.utc).isoformat(), 'sha256': files})
    print('Baseline:', len(files), 'source files', flush=True)


def scan():
    errors, boms, invalid_utf8, duplicates = [], [], [], []
    definitions = {}
    asts = {}
    for directory in ['common', 'events', 'interface']:
        for path in sorted((ROOT / directory).rglob('*')):
            if not path.is_file() or path.suffix not in {'.txt', '.gui', '.gfx'}:
                continue
            rel = path.relative_to(ROOT).as_posix()
            raw = path.read_bytes()
            if raw.startswith(b'\xef\xbb\xbf'):
                boms.append(rel)
            try:
                source = raw.decode('utf-8-sig')
            except UnicodeDecodeError as error:
                invalid_utf8.append({'file': rel, 'error': str(error)})
                source = raw.decode('cp1252', errors='replace')
            try:
                rows = parse(source)
                asts[rel] = rows
            except ValueError as error:
                errors.append({'file': rel, 'error': str(error)})
                continue
            if path.parent.name in {'scripted_effects', 'scripted_triggers', 'scripted_guis', 'dynamic_modifiers'}:
                group = path.parent.name
                for key, _, value in rows:
                    if not isinstance(value, list):
                        continue
                    if group == 'scripted_guis' and key == 'scripted_gui':
                        entries = value
                    else:
                        entries = [(key, '=', value)]
                    for name, _, body in entries:
                        if isinstance(body, list):
                            definitions.setdefault((group, name), []).append(rel)
    for (kind, name), paths in definitions.items():
        if len(paths) > 1:
            duplicates.append({'kind': kind, 'name': name, 'files': paths})
    events = {}
    for rel, rows in asts.items():
        if rel.startswith('events/'):
            for key, _, body in rows:
                if key in {'country_event', 'news_event'} and isinstance(body, list):
                    ident = first(body, 'id')
                    if ident:
                        events.setdefault(ident, []).append(rel)
    duplicate_events = [{'id': key, 'files': paths} for key, paths in events.items() if len(paths) > 1]
    save('source_scan.json', {'parsed_files': len(asts), 'parse_errors': errors, 'script_boms': boms,
                            'invalid_utf8': invalid_utf8, 'duplicate_definitions': duplicates,
                            'duplicate_event_ids': duplicate_events})
    print(json.dumps({'parsed': len(asts), 'parse_errors': errors, 'boms': boms,
                      'invalid_utf8': invalid_utf8, 'duplicate_definitions': len(duplicates),
                      'duplicate_event_ids': len(duplicate_events)}), flush=True)


def regressions():
    if (OUT / 'regression_results.json').exists() and not (OUT / 'regression_baseline.json').exists():
        (OUT / 'regression_baseline.json').write_bytes((OUT / 'regression_results.json').read_bytes())
    paths = [ROOT / 'tools/space_race_1970/validate.py']
    paths += sorted((ROOT / 'tools/space_race_1970').glob('qa_*.py'))
    for directory in ['nuclear_intelligence', 'quaza_nuclear_integration', 'cold_war_gc', 'gc_unsc',
                      'guest_workers', 'resource_discoveries', 'rural_transition', 'colonial_affairs',
                      'pmc_access', 'ssr_intelligence', 'research_slots', 'cartels_1970',
                      'suez_1970', 'suez_canal', 'diplomacy_1970', 'economic_organisation',
                      'currency_balance', 'ddr_currency', 'currency_switches', 'historical_currencies',
                      'west_germany_1970', 'reserve_currency_example']:
        folder = ROOT / 'tools' / directory
        paths += sorted(folder.glob('test_*.py'))
        if directory in {'colonial_affairs', 'guest_workers', 'economic_organisation', 'currency_balance',
                         'ddr_currency', 'currency_switches', 'historical_currencies'}:
            paths.append(folder / 'validate.py')
    results = []
    requires_baseline = {'test_performance_border.py', 'test_performance_monthly.py'}
    skipped = [{'script': p.relative_to(ROOT).as_posix(), 'reason': 'Requires an explicit pre-optimization source snapshot argument.'}
               for p in paths if p.name in requires_baseline]
    paths = [p for p in paths if p.name not in requires_baseline]
    logdir = OUT / 'test_logs'
    logdir.mkdir(parents=True, exist_ok=True)

    def run(path):
        started = time.monotonic()
        rel = path.relative_to(ROOT).as_posix()
        try:
            completed = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True,
                                       encoding='utf-8', errors='replace', timeout=180)
            output = completed.stdout + completed.stderr
            code = completed.returncode
        except subprocess.TimeoutExpired as error:
            output, code = str(error), -1
        logfile = logdir / (rel.replace('/', '__') + '.log')
        logfile.write_text('IMPERIA COLD WAR: regression output\n' + output, encoding='utf-8')
        return {'script': rel, 'exit_code': code, 'seconds': round(time.monotonic() - started, 2),
                'log': logfile.relative_to(ROOT).as_posix(), 'tail': output[-1800:] if code else output[-350:]}

    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(run, path) for path in paths]):
            result = future.result()
            results.append(result)
            print(('PASS ' if result['exit_code'] == 0 else 'FAIL ') + result['script'], flush=True)
    save('regression_results.json', {'live_multiplayer_tested': False, 'skipped': skipped, 'results': sorted(results, key=lambda r: r['script'])})
    failures = [r for r in results if r['exit_code']]
    print(json.dumps({'suites': len(results), 'passed': len(results) - len(failures), 'failures': failures}), flush=True)


def refresh():
    """Recheck changed components and retain the earlier independent results."""
    report = json.loads((OUT / 'regression_results.json').read_text(encoding='utf-8'))
    results = {row['script']: row for row in report['results']}
    scripts = ['tools/colonial_affairs/validate.py', 'tools/colonial_affairs/test_runtime.py',
               'tools/france_1970/test_offers.py', 'tools/france_1970/test_offers_v5.py',
               'tools/france_1970/test_core_v5.py', 'tools/spain_1970_v2/politics_test.py',
               'tools/gcc_1970/test_integration.py', 'tools/multiplayer_quality/test_quality.py']
    for relative in scripts:
        started = time.monotonic()
        completed = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT, capture_output=True,
                                   encoding='utf-8', errors='replace', timeout=180)
        output = completed.stdout + completed.stderr
        logfile = OUT / 'test_logs' / (relative.replace('/', '__') + '.log')
        logfile.write_text('IMPERIA COLD WAR: regression output\n' + output, encoding='utf-8')
        results[relative] = {'script': relative, 'exit_code': completed.returncode,
                             'seconds': round(time.monotonic() - started, 2),
                             'log': logfile.relative_to(ROOT).as_posix(), 'tail': output[-1800:] if completed.returncode else output[-350:]}
        print(('PASS ' if not completed.returncode else 'FAIL ') + relative, flush=True)
    report['results'] = sorted(results.values(), key=lambda r: r['script'])
    save('regression_results.json', report)
    print(json.dumps({'suites': len(results), 'passed': sum(r['exit_code'] == 0 for r in results.values()),
                      'failed': [r['script'] for r in results.values() if r['exit_code']]}), flush=True)


def references():
    definitions = set()
    asts = {}
    for directory in ['scripted_effects', 'scripted_triggers']:
        for path in (ROOT / 'common' / directory).glob('*.txt'):
            rows = parse(path.read_text(encoding='utf-8-sig'))
            asts[path.relative_to(ROOT).as_posix()] = rows
            definitions.update(k for k, _, v in rows if isinstance(v, list))
    for directory in ['common/on_actions', 'common/scripted_guis', 'common/decisions', 'events']:
        for path in (ROOT / directory).rglob('*.txt'):
            asts[path.relative_to(ROOT).as_posix()] = parse(path.read_text(encoding='utf-8-sig'))
    missing = {}
    for relative, rows in asts.items():
        for key, _, value in walk(rows):
            if value == 'yes' and key.startswith(('COLDWAR_', 'mdcw_', 'ICW_', 'IMP_', 'imp_')) and key not in definitions:
                missing.setdefault(key, set()).add(relative)
    save('reference_candidates.json', {'scope': 'Literal custom boolean calls in effects, triggers, hooks, GUIs, decisions and events. Candidates require reachability review.',
                                       'missing_custom_calls': {k: sorted(v) for k, v in sorted(missing.items())}})
    print(json.dumps({'unresolved_custom_call_candidates': {k: sorted(v) for k, v in sorted(missing.items())}}), flush=True)


if __name__ == '__main__':
    actions = {'--baseline': inventory, '--scan': scan, '--regressions': regressions,
               '--refresh': refresh, '--references': references}
    for argument in sys.argv[1:]:
        actions[argument]()
