# IMPERIA COLD WAR — Rebuild and verify the installed approved France V5 tree.
"""Deterministic generation and source-model checks. Does not launch HOI4."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HOOKS = [
    'history/countries/FRA - France.txt',
    'common/scripted_effects/mdcw_1970_focus_tree_effects.txt',
    'common/scripted_effects/99_FRA_scripted_effects.txt',
]
FOLDERS = ['common/national_focus', 'common/scripted_effects', 'common/scripted_triggers',
           'common/dynamic_modifiers', 'common/ideas', 'common/on_actions',
           'common/decisions', 'common/decisions/categories', 'events',
           'interface', 'localisation/english']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def outputs():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in FOLDERS for p in sorted((ROOT / folder).glob('COLDWAR_FRA_1970*'))
            if p.suffix in ('.txt', '.gfx', '.yml')}


def run(name):
    result = subprocess.run([sys.executable, str(HERE / name)], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8')
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    result.check_returncode()
    return {'script': name, 'returncode': result.returncode,
            'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}


def main():
    approval = json.loads((HERE / 'V5_APPROVAL.json').read_text(encoding='utf-8'))
    assert sha(HERE / 'approved_design_v5.json') == approval['sha256']
    assert sha(HERE / 'approved_design.json') == approval['v4_approved_input_preserved']
    archive = HERE / 'archive_v4'
    for name in ('manifest.json', 'README.md'):
        saved = archive / name
        if not saved.exists():
            saved.write_bytes((HERE / name).read_bytes())
    hook_hashes = {p: sha(ROOT / p) for p in HOOKS}
    generation = []
    for name in ('build_offers.py', 'build_offers_v5.py', 'compile.py'):
        generation.append(run(name))
    first = outputs()
    for name in ('build_offers.py', 'build_offers_v5.py', 'compile.py'):
        run(name)
    assert outputs() == first, 'Generated runtime changed on the second identical build.'
    assert hook_hashes == {p: sha(ROOT / p) for p in HOOKS}, 'Generation changed a shared integration hook.'
    assert sha(HERE / 'approved_design_v5.json') == approval['sha256']
    assert sha(HERE / 'approved_design.json') == approval['v4_approved_input_preserved']
    tests = [run(name) for name in ('validate.py', 'test_core_v5.py',
                                   'test_offers_v5.py', 'test_offers.py')]
    assert outputs() == first, 'Verification modified a runtime file.'
    report = {'project': 'IMPERIA COLD WAR', 'revision': 5, 'result': 'pass',
              'approved_sha256': approval['sha256'], 'generation': generation,
              'deterministic_regeneration': True, 'shared_hooks_preserved': True,
              'tests': tests, 'engine_tested': False, 'multiplayer_tested': False}
    (HERE / 'V5_TESTS.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    manifest = {'project': 'IMPERIA COLD WAR', 'approved_revision': 5,
                'approved_sha256': approval['sha256'], 'generated': first,
                'hooks': HOOKS, 'hook_hashes_at_verification': hook_hashes,
                'source_validation': json.loads((HERE / 'VALIDATION.json').read_text(encoding='utf-8')),
                'programme_model_tests': json.loads((HERE / 'PROGRAMME_TESTS.json').read_text(encoding='utf-8')),
                'legacy_offer_model_tests': json.loads((HERE / 'OFFER_TESTS.json').read_text(encoding='utf-8')),
                'verification_report': 'V5_TESTS.json', 'deterministic_regeneration': True,
                'approved_preview': 'proposal_v5/PREVIEW_TESTS.json',
                'independent_reviews': ['V5_INSTALL_REVIEW.md', 'V5_LAYOUT_REVIEW.md', 'ICON_REVIEW.md'],
                'sources': {name: sha(HERE / name) for name in
                            ('compile.py', 'build_offers.py', 'build_offers_v5.py',
                             'approved_design_v5.json', 'icons.json', 'localisation_v5.json')},
                'performance': 'Six bounded family slots plus the preserved legacy pair; no world-country scan. Full domestic reconstruction on first sync, focus completion or government/identity change.',
                'engine_test': 'Not performed; no native hover, save/reload or multiplayer timing claim.'}
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(first)} runtime files reproduced; four verification suites passed.')


if __name__ == '__main__':
    main()
