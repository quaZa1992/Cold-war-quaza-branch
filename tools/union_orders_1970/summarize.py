# IMPERIA COLD WAR — Verify final-source parity with the observed native order fixture.
"""Keep native evidence immutable and record any later formatting separately."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def main():
    manifest, static, tests, generator, engine = map(read, (
        'manifest.json', 'VALIDATION.json', 'TEST_REPORT.json',
        'GENERATOR_PARITY.json', 'ENGINE_REPORT.json'))
    comparisons = {}
    for relative, native_hash in engine['private_snapshot_hashes'].items():
        current = (ROOT / relative).read_bytes()
        snapshot = (Path(engine['profile']) / 'fixture' / relative).read_bytes()
        assert hashlib.sha256(snapshot).hexdigest() == native_hash, relative
        if relative.endswith('.txt'):
            observed = parse(snapshot.decode('utf-8'))
            if relative == 'common/scripted_triggers/COLDWAR_UNION_orders.txt':
                body = first(observed, 'COLDWAR_ORD_human_country')
                expected = parse('OR = { is_ai = no has_country_flag = COLDWAR_ORD_ENGINE_human }')
                assert body == expected, 'Unexpected native fixture authority change'
                body[:] = parse('is_ai = no')
            equal = observed == parse(current.decode('utf-8'))
        else:
            equal = snapshot.decode('utf-8-sig') == current.decode('utf-8-sig')
        comparisons[relative] = {
            'matches_tested_semantics': equal,
            'current_sha256': hashlib.sha256(current).hexdigest(),
            'native_snapshot_sha256': native_hash,
        }
    current_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                      for p in manifest['outputs']}
    report = {
        'project': 'IMPERIA COLD WAR',
        'families': static['families'], 'quota_days': manifest['quota_days'],
        'success_days': manifest['success_days'], 'failure_days': manifest['failure_days'],
        'regression_tests': tests['tests_run'], 'native_assertions': len(engine['passed']),
        'static_errors': static['errors'], 'native_order_errors': engine['order_errors'],
        'runtime_parity': comparisons,
        'current_hashes_match_manifest_and_regression': current_hashes == manifest['outputs'] == tests['source_hashes'],
        'native_profile': engine['profile'], 'limitations': engine['limitations'],
        'scope': 'Final source compared with the immutable native snapshot. Clausewitz whitespace is ignored; only the documented fixture authority override is removed. Native test results are not rewritten.',
    }
    report['success'] = (not static['errors'] and tests['success'] and generator['success']
                         and engine['success'] and report['current_hashes_match_manifest_and_regression']
                         and all(row['matches_tested_semantics'] for row in comparisons.values()))
    (HERE / 'IMPLEMENTATION_RESULT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in {'runtime_parity', 'limitations'}}))
    return not report['success']


if __name__ == '__main__':
    raise SystemExit(main())
