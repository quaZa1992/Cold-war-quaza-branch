# Reading the tick audit

Output of `scripts/tick_audit.py`. Read this before explaining why a number looks the
way it does.

## Engine facts

Only six `on_action` hooks run on a clock:

- `on_daily`, `on_weekly`, `on_monthly` are global. They run once per country per
  period, and the engine staggers them across the period.
- `on_daily_<TAG>`, `on_weekly_<TAG>`, `on_monthly_<TAG>` run for that country only.

The script finds hooks by parsing every `common/on_actions/*.txt` and labels each as
GLOBAL or its TAG from the hook name, not the file name. A global `on_weekly` inside
`99_LBA_on_actions.txt` is still GLOBAL. Several files may add to the same hook; each
block is listed separately.

**Once-per-period guards.** MD wraps much of its global weekly and monthly work in
`if = { limit = { NOT = { has_global_flag = on_weekly_global_done } } ... set_global_flag = ... }`
(see `MD_on_actions.txt`). Such a body runs once per period, not once per country. The
script does not evaluate guards, so it ranks those blocks as if every country ran them;
open the `file:line` and check for the guard before calling a hook expensive.

## Ops

`ops` counts `key = ...` statements: effects and the `limit` and trigger checks the
engine evaluates each tick.

- A node's `own` is the statements directly in its body (calls excluded).
- A node's `total` is its own ops plus everything it calls. Bar size uses `total`.
- A loop node's total is **one pass**. The real cost is that times the number of
  countries or states it iterates, which the script cannot know.
- It is a proxy, never time. Native `profile` measures time for a bounded workload.

## Accuracy contract

Only work reachable from a real clock hook is counted.

- Calls are resolved when a statement is `name = yes` (or `no`) and `name` is a defined
  scripted effect or trigger. Recursion is cut and labelled.
- An event is counted when a hook or anything it calls fires it through
  `country_event`, `news_event`, `state_event`, leader events, or a `random_events`
  pool. Its `trigger`, `immediate` and heaviest `option` are counted.
- `country_event = { id = X days = N }` is a one-shot delay, labelled `fired after N`.
  It recurs only when the event reschedules itself; that is labelled
  `self-rescheduling loop`.
- An event fired inside a loop is labelled with the loop; the fire itself still
  happens once per iteration that passes its `limit`.
- `meta_effect` calls are reported with the number of scripted effects their pattern
  could match and are not counted. `trigger_year_[year]_events` is the main one; in this
  fork only the 2001 to 2030 targets exist.
- Fired event ids not found in `events/` are listed at the end; they are usually
  inherited references to removed content and worth a grep.

## Common questions

- "Every country's daily column is the same." Correct. Only a few countries have their
  own `on_daily_<TAG>`. Everyone else's daily cost is the shared global hooks.
- "Does event X really fire daily?" Wired into that tick means it is reached, still
  subject to its own `if`, `limit` and `trigger`. Open the `file:line` and read the
  guard.
- "Is this why multiplayer lags?" Static ops cannot say. Use the report to pick a
  suspect, then measure with `profile` on the same save before and after.
