# Iraq 1970 authoring and validation

The approved audit revision is implemented. Current scope and exact outcomes:
`docs/design/iraq_1970/audit_2026_10_19/IMPLEMENTATION.md`.

`approved_iraq.json` is the immutable original catalogue. `audit_design.load_design()`
copies it, applies `audit_rewards.py`, rewrites the approved structure and attaches
current decision providers. `compile.py` consumes this result and records
`current_design.json`, 103 generated outputs and nine narrow integrations in
`manifest.json`. Do not edit generated focus/effect files as the source.

Regenerate from the mod root with `python tools/iraq_1970/compile.py`; validate
with `python tools/iraq_1970/validate.py`. Never import another country's broad
compiler to obtain an AST helper. Test harness paths append the shared AST-helper
directory, keeping the Iraqi compiler first during discovery.

Run the data/graph suites with `python -m unittest discover -s tools/iraq_1970 -p
"test_audit_*.py"`. Script-style scenario suites must be run directly:
`test_audit_transactions.py`, `test_audit_politics.py`, `test_audit_usa.py`,
`test_core.py`, `test_decisions_module.py`, `test_starting_spirits.py`,
`test_presentation.py`, `test_usa_module.py`, `gulf_module.py` and `startup_patch.py`.
All are under this directory. Direct scripts exercise their `main`/`self_test`
scenario families; merely importing them through unittest does not run those
families. Tests record native API boundaries rather than simulate HOI4.

`audit_migration.py` credits actual old successful receipts and historical paid
invoices. Keep component receipts, partial XP/literacy credits, current policy
gates, frozen supplementary quotes and all 115 old event numbers stable. The
14 new decision-event IDs are explicitly reserved in `decision_event_ids.json`.
Party names/icons are owned by the shared historical-politics curation; the
pure presentation adapter in `politics.py` preserves them on regeneration.

`render_installed.py` renders installed native assets/positions. `installed_viewer.py`
updates the existing whole-tree inspector from actual installed definitions;
`node tools/iraq_1970/test_installed_viewer.cjs` checks real browser navigation
and all 638 active inspectors. Neither renderer certifies native HOI4 hover.

`engine_runtime_check.py` attempts an actual unattended full 1970 start in a
task-owned isolated profile. `--early-assets` instead checks actual state
building delivery and once-only payment with fixture GDP10/treasury1000 before
unrelated world initialization; it does not certify a completed campaign start.
No fixture hook belongs in shipped game files or the user's normal playset.
Read the separate JSON reports and their manifest hashes; keep failed startup
attempts visible rather than presenting the targeted test as a full playthrough.

The requested durable skill edits were installed with the exact bounded
`skill_updates/install.py --impact` transaction. `verify_impact_update.py` checks
their content and existing metadata. Do not rerun the installer against an
already updated skill: its before-hash check deliberately rejects stale writes.
