<!-- IMPERIA CW — Cold War: West Germany runtime performance audit and verification. -->
# West Germany performance audit

Reviewed on 23 October 2026. Scope: the active West German focus tree, the two minigame windows, their monthly systems and the DDR/economy calls they make. This is a source and differential-execution audit, not an engine benchmark.

## Changes

| Recurring work | Before | After |
|---|---|---|
| Border division count | 13 native division queries in each of 12 states: 156 queries per full count | Same stepped result with a sparse-first decision tree: at most 60 queries; 12 when all border states are empty |
| Full window presentation | Rebuilt for AI and humans even while the corresponding window was closed | Only rebuilt for a human with that window open; opening still refreshes immediately |
| GUI invalidation | One global counter invalidated both windows and their bar containers | Country-scoped counters isolate the rivalry and security windows; the compatibility helper can still invalidate both |
| Election cache allocation | Resize to 24 on every parliamentary calculation | Resize only on first use or when repairing an incompatible array; all 24 current source values are still sampled |
| SPD opposition eligibility | Seven repeated checks | One shared gate, preserving the order of the subsequent leadership changes |
| Detailed monthly log | Written every month | Written only in the native debug mode |

The border algorithm keeps all existing thresholds, side scopes and outputs. It introduces no time cache, so counting still observes the current divisions whenever the existing callers request it. The 30-division approximation cap remains per state, as before.

The window optimization separates presentation from gameplay. Border strength and the number of agreed unity chapters continue to update for closed windows and AI countries. The human security top bar retains its hostage-deadline calculation while the larger window is closed. The 99 remaining presentation assignment targets have no gameplay consumers outside the window effects, scripted GUI, scripted localisation and localisation text.

## Work retained deliberately

- There is one guarded `on_monthly_GER` simulation hook. This module adds no daily, weekly or hourly simulation loop.
- All authored events use `is_triggered_only`; the hostage deadline already uses a scheduled event rather than a polling loop.
- The focus and decision availability paths contain no world-wide country/state scans. Country-wide notifications and large state transitions occur on explicit actions or one-off outcomes.
- Immediate GER/DDR dynamic-modifier refresh remains, because it applies the changed gameplay values immediately.
- Real population transfers retain native economic recalculation in both countries. `ingame_update_setup` recalculates state aggregates, weighted productivity, GDP, budgets and display values; later migration charges also read the refreshed GDP. Deferring this work to the weekly economy tick would change the financial behavior.
- Crisis probabilities, random-call order, payments, focus durations, rewards and diplomacy were not redesigned as part of this audit.

## Primary local evidence

- Installed HOI4 `common/scripted_guis/_documentation.md`: its dirty-variable section describes replacing default per-tick GUI updates with updates on dirty-variable changes.
- Main MD `common/scripted_guis/00_MD_alerts_scripted_gui.txt` and `00_MD_politicsview_scripted_guis.txt`: country-scoped dirty variables in player contexts.
- Installed HOI4 `documentation/effects_documentation.md`: `force_update_dynamic_modifier` forces the immediate update instead of waiting for the normal daily update.
- Loaded `common/scripted_effects/00_money_system.txt`: `ingame_update_setup` and `update_state_variables` establish the population/economy dependencies.

The live providers were read from the installed game and MD directories, rather than assuming that these operations are free or substituting incomplete population deltas.

## Verification

The focused tests execute the actual generated Clausewitz AST in the existing strict script harness. Fixture implementations supply only the native engine primitives under examination; these tests do not reproduce the entire game engine.

- `test_performance_border.py <old_windows_effects.txt>`: 1,348 fixtures compare old and new division counts, escalation levels and side scopes, including every count from 0 to 64 in each state, mixed deployments and a missing DDR. The test also counts the actual native query evaluations.
- `test_performance_monthly.py <old_effects.txt>`: 8,784 checks cover leadership transitions, all 24 parties, dates around transition boundaries, source-array changes, sentinel fallback and save-array repair.
- `test_performance_gui.py`: 105 checks of actual emitted window effects and bindings for human/AI, open/closed windows, preserved gameplay bookkeeping, top-bar deadlines, opening saved windows and isolated dirty counters. Its representative open-window refreshes execute 131 rivalry and 193 security presentation arithmetic operations; closed-window and AI refreshes execute none of that presentation arithmetic.
- The normal generator validator reports no errors (its existing average-focus-cost warning reflects the requested 70-day standard). All 1,093 integration checks pass. Output comparison, encoding checks and scoped `git diff --check` pass.

Only changed dedicated runtime outputs are copied from the staging build. The focus file, localisation, interface geometry, events, decisions and gameplay triggers are unchanged by this performance pass. No HOI4 runtime, multiplayer or frame-time measurement was performed; the operation-count reduction is not an FPS estimate.
