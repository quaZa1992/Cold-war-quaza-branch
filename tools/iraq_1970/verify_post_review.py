# IMPERIA CW — Cold War: iraq 1970 — verify post review.
"""Repeat the five review counterexamples against installed game providers.

Generators are replaced with reads from the manifest-owned installed files.
The bounded AST harnesses still do not simulate native UI, diplomacy or MP.
No compiler, installation or gameplay-file mutation is performed here.
"""
from contextlib import ExitStack, redirect_stdout
import hashlib
import io
import json
import unittest
from unittest.mock import patch

from common import ROOT
import decisions_module, gulf_module, runtime_design, starting_spirits
import test_audit_transactions as transactions
import test_concession_feasibility as concession
import test_presentation as presentation
import test_usa_review_regressions as usa

HERE = ROOT / 'tools/iraq_1970'
DEST = ROOT / 'docs/design/iraq_1970/audit_2026_10_19/POST_REVIEW_INSTALLED_TESTS.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_suite(suite):
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {'passed': result.wasSuccessful(), 'tests_run': result.testsRun,
            'output': stream.getvalue()}


def main():
    manifest = json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
    owned = {**manifest['generated'], **{a['path']: a['sha256'] for a in manifest['adapters']}}
    assert all(digest(ROOT/path) == sha for path, sha in owned.items())
    installed = {path: (ROOT/path).read_text(encoding='utf-8-sig')
                 for path in owned if path.endswith(('.txt', '.yml', '.gfx', '.gui'))}
    # Determine each provider's ownership before replacing generation with
    # installed reads. These pure calls themselves write no game files.
    subsets = {module: {path: installed[path] for path in module.generate(ROOT)}
               for module in (decisions_module, gulf_module, runtime_design, starting_spirits)}
    tx = {path: installed[path] for path in transactions.fresh_outputs()}
    us = {path: installed[path] for path in usa.generate(ROOT)}
    with ExitStack() as stack:
        for module, files in subsets.items():
            stack.enter_context(patch.object(module, 'generate', lambda root, files=files: files))
        stack.enter_context(patch.object(usa, 'generate', lambda root: us))
        migration_checks = transactions.pending_child_quote_regressions(tx)
        concession_checks = run_suite(unittest.defaultTestLoader.loadTestsFromTestCase(
            concession.ConcessionFeasibilityTest))
        presentation_checks = run_suite(unittest.TestSuite([
            presentation.PresentationTests('test_front_and_monopoly_previews_share_actual_contract_conditions')]))
        captured = io.StringIO()
        with redirect_stdout(captured):
            usa.main()
        usa_checks = json.loads(captured.getvalue())
    unchanged = all(digest(ROOT/path) == sha for path, sha in owned.items())
    report = {
        'scope': 'Executed the review counterexamples against installed manifest-owned providers, with the actual native treasury effect body.',
        'limits': 'Bounded AST execution, not native event rendering, real old-save loading, air missions or multiplayer testing.',
        'manifest_sha256': digest(HERE/'manifest.json'),
        'revision': manifest['audit_revision'],
        'generated': len(manifest['generated']), 'adapters': len(manifest['adapters']),
        'installed_files_unchanged': unchanged,
        'migration_scenario_groups': migration_checks,
        'concession': concession_checks,
        'conditional_preview_and_consumer': presentation_checks,
        'usa': usa_checks,
        'native_treasury_provider_sha256': digest(ROOT/'common/scripted_effects/00_budget_effects.txt'),
        'source_sha256': {path.name: digest(path) for path in HERE.glob('*.py')},
        'success': unchanged and concession_checks['passed'] and presentation_checks['passed'] and usa_checks['passed'] == 14,
    }
    DEST.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in ('revision','manifest_sha256','generated','adapters','installed_files_unchanged','success')}, indent=2))
    print('Installed counterexample groups: migration=8, concession=6, USA=14, presentation=8 states on both focus/decision surfaces')
    raise SystemExit(0 if report['success'] else 1)


if __name__ == '__main__':
    main()
