# IMPERIA COLD WAR — Profiling interpretation and tool availability

Upstream's profiler reconstructs a static call tree from recurring hooks. Its operation count is a proxy: a node includes its own statements and calls, shared effects may appear under several paths, and static conditions do not prove actual dispatch. Do not present estimated operations as milliseconds, FPS or multiplayer desync probability.

At adaptation time `tools/analysis/tick_audit.py` and `tools/run.py` were absent. Check their availability before running the upstream example `python tools/run.py tick_audit --flamegraph ... --tree ...`. If later present, inspect actual help and source, output paths, tag gates and treatment of event/decision timers. Do not invent its options or transplant a newer toolchain as part of a profiling request.

Without that tool, use the project's parser or direct source tracing to record hook, cadence, scope, called effects/events, guard, loop population, approximate statement count and unresolved dynamic calls. Keep the result labelled a static inventory. Preserve repeated execution paths rather than deduplicating all shared calls into a misleading total.

Discover native hook semantics from the installed documentation and current callers. A generic recurring hook may run per country; a tag-suffixed hook is country-specific. `on_startup` must be reviewed separately because its dispatch can lack a country scope. A global campaign action behind a country loop needs a correct campaign-period guard, with save/rehost behavior considered.

For minigames examine display-only refresh, dynamic lists, open-view guards, AI paths, nested every-country/state loops and archive retention. Do not reduce work by dropping consent checks, capacity checks, necessary invalidation or calendar recovery. A cheap direct trigger can outperform a periodically maintained cached flag.

Native before/after samples should use comparable frozen source, save, speed, date window, observer country, open windows and machine state. Repeat enough to judge noise when measuring a small effect. A changed calendar window or different source snapshot invalidates a precise comparison. Keep UI FPS, script timing and network consistency as separate measurements.
