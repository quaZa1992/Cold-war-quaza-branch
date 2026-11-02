---
name: mdcw-quality-audit
description: Audit quality, performance, and multiplayer stability of IMPERIA COLD WAR mechanics, minigames, or a specified change, and fix confirmed defects when requested. Use for broad mechanics audits rather than focus-only modifier or layout reviews.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Mechanics quality and multiplayer audit

Read `AGENTS.md`, then [references/audit-method.md](references/audit-method.md). Establish the requested mechanics and review baseline, including current unstaged and untracked source where relevant. Preserve unrelated work. Resolve owning generators before changing emitted files.

Trace actual entry points through decisions, events, scripted effects, triggers, ideas, dynamic modifiers, on_actions, scripted GUI and English localisation. Review correctness, player presentation, scenario reachability, recurring work, transaction safety, save migration and AI/RP boundaries. Generated scripts and referenced graphics are part of the feature; do not blanket-exclude them as upstream's diff audit does.

For minigames, inspect state transitions and terminal paths: initialization, start, pause, resolution, failure, cancellation, reset and restoration. Check simultaneous users, co-op, repeated inputs, target changes and recovery after reload. A global calendar or ranking pass must not run once per human country when it should run once per campaign period. UI refresh state must not become gameplay authority.

Verify native effect/trigger support and scopes against the installed version, actual provider and consumer, and relevant native evidence. Check synchronized dynamic token registration when tokens are used dynamically. Keep startup's scope-less dispatch distinct from recurring country hooks. Validate exact modifiers and file-local math constants rather than trusting source spelling or a model's injected defaults.

Use the available targeted project tests. Inspect their scope and write behavior first. Legacy snapshot assertions, historical logs and identical upstream duplicates require classification, not fabricated passing baselines. Measure work at its real cadence; operation counts are not timing or OOS evidence.

When authorized, repair confirmed causes in generators and loaded files, then run the checks appropriate to those repairs. Report findings, fixes, evidence and remaining engine/MP gaps. Never certify network stability from parsing, a single-client startup or a Python simulation. Do not impose upstream agent fan-out, repository workflow or cosmetic reporting markers.

Source and adaptation: [references/source.md](references/source.md).
