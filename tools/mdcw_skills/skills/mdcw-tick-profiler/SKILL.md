---
name: mdcw-tick-profiler
description: Trace and assess recurring script workload in IMPERIA COLD WAR daily, weekly, monthly, decision and GUI paths. Use for tick lag, expensive minigames, on_action scheduling or static workload profiling; distinguish script-operation estimates from native timings.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Recurring script workload

Read `AGENTS.md` and [references/profiling.md](references/profiling.md). Identify the named mechanic, current source and real execution context. Include both canonical emitters and loaded hooks; a file named after one country can still contain a global hook.

Check for `tools/analysis/tick_audit.py` or `tools/run.py` before using upstream commands. They were absent from this checkout during adaptation. If present, inspect their help and limitations before running them. Otherwise construct a bounded call inventory using current source and existing parsers; do not claim to have generated a flamegraph or measured timings.

Start at genuine recurring on_actions, event rescheduling, decision timers and UI evaluation paths. Follow reachable scripted effects and event dispatch, preserving country gates, call multiplicity, loop population and cadence. A delayed one-shot event is not inherently periodic. Separate startup and focus completion from recurring work.

Inspect expensive loops, repeated country/state lookups, accumulator reset, near-zero division, decision visibility scans, AI weight arithmetic and scripted-GUI invalidation. Cache only where its maintenance and freshness are better than direct cheap predicates. Do not remove correctness gates or introduce a daily stale cache for a small native trigger.

For global campaign calendars, rankings and archives, establish how many countries and human clients reach the pass. Check a once-per-period campaign guard where appropriate. Keep user display refreshes bounded, and ensure legitimate data changes from any source still invalidate affected views. UI dirty counters are not gameplay transaction guards.

Prioritize by cadence, reach, data size and actual work, not file length. Operation counts and static fan-out are estimates; branch reachability, random choices and engine implementations limit them. Confirm an optimization's material effect with comparable native samples when available.

Report heavy paths with source lines, assumptions and before/after evidence. If native timings, frame rate, monthly rollover or network behavior were not measured, say so. Do not call a single-client hidden probe a multiplayer soak.

Source and adaptation: [references/source.md](references/source.md).
