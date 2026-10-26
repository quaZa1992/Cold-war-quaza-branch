---
name: md-tick-profiler
description: Profile the Cold War 1970 mod's recurring per-tick scripted workload (the daily/weekly/monthly on_action hooks and everything they run) as a call tree sized by script ops, plus spot checks and a collapsible HTML view. Use for any question about performance, lag, tick cost, on_actions, or why a multiplayer session is slow, even without the word "profiler".
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# Tick Profiler

`.claude/skills/md-tick-profiler/scripts/tick_audit.py` (bundled with this skill,
standard library only) reconstructs, statically, what each recurring tick runs. Upstream
MD's `tools/run.py tick_audit` is not in this repository; do not call it. The game's own
`profile` console command measures real time for a bounded workload. They answer
different questions: use the static report to find what to measure, and native timing to
confirm a change matters.

The fork already has measured repair history: read `docs/RUNTIME_PERFORMANCE_1970.md`
and `docs/RUNTIME_PERFORMANCE_MD202.md` first, and use `tools/runtime_performance/` for
the country harnesses they describe.

## What an op is

Say this to the user. An op is one scripted statement: set a variable, check a
condition, fire an event, call an effect. A node's count is its own statements plus
everything it calls. More ops means more work per tick. It is a proxy for cost, not
measured milliseconds, and it cannot see how many times a loop iterates.

The output is a call tree, not a call graph. An effect called from three hooks is
counted under all three, so tree totals exceed what one tick really runs. That is
expected.

## Run

From the mod root:

```bash
python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py
python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --cadence daily --depth 3 --top 15
python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --tag ICE
python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --spot-check
python -X utf8 .claude/skills/md-tick-profiler/scripts/tick_audit.py --json "$TMPDIR/ticks.json" --html "$TMPDIR/ticks.html"
```

`--tag` keeps the global hooks plus that country's own `on_*_TAG` hooks. Open the HTML
with `start ""` (Windows), `open` or `xdg-open`. It is a collapsible tree with bars sized
by total ops and a filter box (tag, file, effect name).

Tell the user the heaviest one or two hooks per cadence with `file:line`. Children are
sorted heaviest first.

## Spot checks

`--spot-check` ranks static hotspots by severity, then cadence and scope:

- loops over all countries or all states inside a recurring hook (daily global is worst);
- `create_country_leader` or `force_update_dynamic_modifier` on a recurring path (the
  Greek leader bug in `RUNTIME_PERFORMANCE_1970.md` is this pattern);
- events wired straight into a global daily hook;
- self-rescheduling event loops and `meta_effect` dynamic calls (not expanded).

## Accuracy

Read [references/reading-the-tick-audit.md](references/reading-the-tick-audit.md) before
explaining why a number looks the way it does. In short: only work reachable from a real
clock hook is counted; event options count only the heaviest option; delayed events are
labelled with their delay; dynamic `meta_effect` targets (such as
`trigger_year_[year]_events`) are reported, not counted; global-flag guards that make a
per-country hook run once per period are not evaluated.

## Native spot tests

For a before and after measurement, use `profile` with the same 1970 save, game speed,
map position, open UI, human player count and observation window. Repeat the sample
before concluding. In multiplayer, also note whether the slowdown is on the host or
every client.
