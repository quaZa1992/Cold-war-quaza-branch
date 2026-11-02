# IMPERIA COLD WAR — Record actual MD 2.0.3 follow-up compatibility evidence.
"""Preserve failed native evidence without replacing it with source-test results."""
from pathlib import Path
import hashlib
import json
import re

from audit import ROOT, OUT, PROJECT, emit


def main():
    native_path = OUT/'native_report.json'
    native = json.loads(native_path.read_text(encoding='utf-8'))
    profile = Path(native['profile'])
    crashes = sorted((profile/'crashes').glob('*/exception.txt'))
    native['native_test_executed'] = True
    native['native_test'] = native['success']
    native['status'] = 'PASS' if native['success'] else ('FAIL_ENGINE_CRASH' if crashes else 'FAIL_INCOMPLETE')
    native['crash_exceptions'] = [str(path) for path in crashes]
    emit(native_path, native)
    errors_path = Path(native['full_error_log'])
    raw = errors_path.read_bytes()
    errors = raw.decode('utf-8-sig', errors='replace').splitlines()
    observed = [line for line in errors if 'ISR70_' in line]
    automation_errors = [line for line in errors if re.search(r'automation|auto_agency|MD203', line, re.I)]
    automation = json.loads((OUT/'automation_verification.json').read_text(encoding='utf-8'))
    report = dict(project=PROJECT, source_update_status='PASS',
        overall_runtime_certification='NOT_READY_NATIVE_TEST_FAILED',
        automation_source_status=automation['status'],
        callbacks_checked=automation['callback_count'], dynamic_images_checked=automation['dynamic_image_count'],
        supplied_md_files=automation['source_files_seen'],
        supplied_md_metadata_changes=automation['source_metadata_changes'],
        native_status=native['status'], native_returncode=native['returncode'],
        native_checks_passed=native['passed'], native_checks_unrun=native['unrun'],
        frozen_source_files=native['frozen_files'],
        snapshot_drift=native['snapshot_drift'], source_drift=native['source_drift'],
        full_error_log=dict(path=str(errors_path), sha256=hashlib.sha256(raw).hexdigest(), lines=len(errors)),
        crash_exceptions=[dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in crashes],
        israel_diagnostics=observed, automation_named_diagnostics=automation_errors,
        additional_commands=[
            dict(command='python tools/quaza_nuclear_integration/test_integration.py', exit_code=0,
                result='25 tests passed', evidence='Current installed source and bounded behavioral models; captured terminal result.'),
            dict(command='python tools/space_race_1970/qa_system_audit.py', exit_code=0,
                result='1318 checks passed', evidence='Current installed source and behavioral models; tools/space_race_1970/system_audit_validation.json.'),
            dict(command='python tools/md_update_203/verify_automation.py', exit_code=0,
                result='75 callbacks, 34 dynamic images, six recurring effect providers checked',
                evidence='automation_verification.json; source checks only.'),
            dict(command='python tools/md_update_203/native_probe.py', exit_code=1,
                result='Engine startup observed; process exited with crash before all eight checkpoints.',
                evidence='native_report.json and preserved private engine logs.')],
        conclusions=[
            'The supplied MD folder still has 79711 files and unchanged metadata relative to the complete hash review.',
            'The source delta remains the 73 previously verified paths; the approved metadata transaction is complete.',
            'Automation controls match the supplied MD implementation and retain their callbacks and periodic providers.',
            'No active Cold War feature was removed by this follow-up; the native snapshot also reports no installed-source drift.',
            'The engine reached startup on 1 January 1970 and then produced an access-violation crash at the first-hour transition.',
            'The eight scheduled feature checkpoints did not execute. None may be reported as passed.',
            'State-only is_controlled_by conditions in four Israel occupation dynamic modifiers were evaluated in country scope.',
            'Existing Israel array-removal, variable-bound and modifier-cleanup diagnostics also require review.',
            'The crash cause remains unisolated. Its last log line is not proof of causation.',
            'A complete clean-runtime, automation-interaction, save/reload or multiplayer claim is unsupported.'])
    emit(OUT/'follow_up_verification.json', report)
    note = '''# IMPERIA COLD WAR: MD 2.0.3 follow-up compatibility verification

The source update is complete. Full runtime compatibility is **not certified**: an isolated native test on HOI4 1.19.4 reached January 1970 startup and crashed at the first-hour transition before its eight scheduled assertions. The crash report records an access violation. The cause has not been isolated.

## What passed

- The supplied MD folder still has 79,711 files and no path, size or modification-time change since its complete hash pass. The verified source delta remains 73 paths.
- The complete automation interface, callbacks, dynamic checkbox localisation and native agency window match the supplied MD executable tokens.
- 75 automation callbacks resolve to their own native widgets. All 34 dynamic checkbox image providers resolve, including the energy provider in shared money localisation.
- Influence, internal investments, economic budgets and space automation retain their actual daily, weekly and monthly hook calls and unique effect providers.
- Cold War internal investment terms, all four completed nuclear passive-defence receipts, and the SSR agency blocker remain present.
- The current uranium/nuclear integration suite passed 25 tests. The Space Race system audit passed 1,318 source/model checks. These are not native gameplay tests.
- The isolated snapshot contained 11,778 copied files. Neither the snapshot's recorded files nor installed sources drifted during the test.

## What prevents a clean-runtime claim

The engine process crashed before the day-three assertions. Consequently there is no passing native result for the scenario, focus tree, GDP, occupation budget, Jerusalem split or SSR permission checkpoints. Loading startup alone is insufficient.

The engine also reported state-only `is_controlled_by` triggers evaluated in country scope for the four Israel occupation dynamic modifiers, plus Israel array-removal, missing debt-bound and modifier-cleanup messages. These files were not changed by the metadata update. Their retained bytes do not establish correct behavior. The messages are actionable audit evidence, not a proven cause of the crash.

Other inherited diagnostics exist in the full error log. Some may concern inactive content or native parser behavior; they have not all been classified. No blanket harmless-warning exemption is asserted. No named automation diagnostic appeared in this run, but the run did not exercise automation buttons or complete its calendar checks.

## Evidence and remaining work

See `follow_up_verification.json`, `automation_verification.json` and `native_report.json`. Full engine logs, the frozen snapshot and crash files are retained on E: at the exact private paths recorded there. The earlier implementation evidence remains a record of the approved source transaction, not an all-feature gameplay certificate.

Resolve the confirmed scope/initialization diagnostics, isolate the first-hour crash, then repeat native calendar and automation interaction checks. Save/reload, rehost and actual multi-client checks remain outstanding. No user save or Launcher playset was modified; only the probe's own process was launched.

Provenance: verification and this report were authored for IMPERIA COLD WAR with Codex. Existing MD, Imperia and Cold War source credits and licences remain applicable. No third-party artwork or runtime content was changed by this follow-up.
'''
    (OUT/'FOLLOW_UP_VERIFICATION.md').write_text(note, encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('source_update_status','overall_runtime_certification','automation_source_status','native_status')},indent=2))


if __name__ == '__main__':
    main()
