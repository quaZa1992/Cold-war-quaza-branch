IMPERIA COLD WAR: random oversupply oil-price review

The reported popup is `imp_oil.21`, "Oversupply of oil hits markets". It belongs to Imperia's original random oil-event pool, not to the new OPEC voting or quota-enforcement system. Its only regular call is the existing global random-oil dispatcher on the Liechtenstein monthly pulse. The global draw has a 232-day shared cooldown, so the monthly check normally yields a draw about once per eight monthly pulses. The popup is broadcast, but its option has no second price effect.

The old pool gave oversupply a weight of 30 out of 200, or 15% of unmodified draws. It did not inspect actual OPEC quota breaches, and it had no event-specific repeat cooldown. A random sequence could therefore choose it again at the next eligible global draw. This source tracing found no second normal call per human country.

The misleading strength came from `imp_spike_oil_price`: it multiplies a fixed reference of 75 by the supplied -0.05. Each oversupply event therefore subtracted 3.75 model points, not five percent of the current spot price. At a current price of 30 this was a 12.5% drop. The old random pool is slightly positive in nominal expected raw price change; this one event is not evidence that the entire pool has a downward expected-value bias.

Changes installed:

| Rule | Previous | Current |
| --- | --- | --- |
| Oversupply price movement | Fixed -3.75 model points | -1% of current spot price, retaining the native 15-200 bounds |
| Example at 75 | 71.25 | 74.25 |
| Example at 30 | 26.25 | 29.70 |
| Unlocked event weight | 30 of 200, 15% | 15 of 185, about 8.11% |
| Specific repeat protection | None | Global 730-day cooldown |
| Regular global draw | Existing 232-day cooldown and monthly check | Unchanged |

The cooldown is checked in both selection and execution. A locked entry has zero weight rather than consuming a draw silently. The guard is set before the one-time global price change and notification. Display prices refresh immediately. The news description no longer claims that producers violated quotas when no quota check happened. Native war, sanctions, trade-policy, GC and OPEC spike calculations remain unchanged.

A separate cause of persistently low prices remains in the equilibrium formula: the reference price plus exporter adjustments is multiplied by average global oil dependence. With no other adjustments, dependence of 0.7 gives 52.5 instead of 75. The existing weekly market then moves the spot price 7.5% of the remaining gap towards equilibrium, accelerated by a factor of 1.5 in the existing extreme-price cases. The new oversupply helper changes the spot price only. It does not lower that equilibrium, producer asking-price policy, OPEC posted-price level, CPI or embargo multipliers. A low equilibrium can therefore keep prices low even after random shocks are made smaller. The screenshot does not contain the saved global variables, so their actual values in the user's running campaign were not measured.

Performance and saves: no new on_action, daily/weekly pulse, world scan or per-player loop is introduced. The new timed global flag persists through normal saved state. Old saves begin without this new cooldown until their first post-update oversupply event. Previously applied historical shocks are not reversed, and the current price is not reset. The existing weekly convergence remains active.

Ownership: the live native oil scripted-effects file is the canonical source. No owning generator for `imp_random_global_oil_event` was found in the current tools or OPEC generator bundle. Original Moveably attribution and unrelated custom integration comments are retained. No image, font or other binary artwork is modified.

Verification: `python -X utf8 tools/oil_market_1970/test_oversupply.py` passed 10 focused tests and two existing GC oil-price/control regressions. They execute the installed ASTs for relative price changes at several price levels, display scaling, repeat and cross-country guards, flag expiry and restored global state, disabled weights, the original global dispatcher, empty broadcast options, unchanged other oil mechanics, weekly recovery, and encoding/workload boundaries. `OVERSUPPLY_BASELINE.json` pins the pre-change source commit and hashes of untouched effects, random branches, scheduler and news event. `VALIDATION.json` records current source hashes and evidence limits. Expiring flags and branch selection are simulated; no native game, save/rehost, RNG-frequency or live multiplayer test was run.
