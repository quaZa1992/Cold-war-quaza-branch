---
name: mdcw-validate
description: Run appropriate available checks for IMPERIA COLD WAR changes and report complete diagnostic artifacts or filtered warnings when requested. Use for validation runs and validator output, not automatic full-repository scans after every edit.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Validation and complete diagnostics

Read `AGENTS.md` and [references/validation.md](references/validation.md). Establish the requested scope, source version, staged versus working-tree inputs and whether the task requests a summary, one diagnostic category or a complete report.

Discover actual tools with `rg --files tools`. Upstream's `tools/validation/run_all_validators.py`, `tools/analysis` and standardizers were absent during adaptation. Do not run nonexistent commands, silently download the modern suite, or promise unsupported flags. Inspect a script before using `--help`: some project scripts interpret unknown arguments as execution requests.

Select relevant parser, reference, encoding, generator and behavioral checks from current project tooling. Inspect output destinations and fixture/restore behavior first. The historical `tools/multiplayer_quality/audit.py` runner writes into a dated report folder; importing its parser is different from executing the whole runner. Use a fresh report destination or isolated adapter where needed, and preserve prior evidence.

Record exact commands, exit codes, source hashes where material and captured output. Classify baseline versus new findings and current versus retired test contracts. A stale preservation assertion is not automatically a runtime defect; do not replace snapshots to turn a test green. A missing tool is unavailable coverage, not a passing check.

For a full warning request, retain every raw finding in a linked text/JSON artifact, preserving order, fields and filters. Use a validator's full sidecar when its console output is capped. Verify the actual sidecar schema and count before claiming completeness. Do not substitute a sample or a terse summary for requested complete output; if the output cannot fit in chat, provide the complete artifact and explain the presentation limit.

Investigate references across scripts, GUI, inherited game assets and dynamic dispatch before deleting alleged orphans. A warning is a candidate, not proof. Stop after appropriate checks pass unless new changes or unresolved concerns justify more testing. Report source/model/native/MP evidence separately and do not claim all tests pass when only selected suites ran.

Source and adaptation: [references/source.md](references/source.md).
