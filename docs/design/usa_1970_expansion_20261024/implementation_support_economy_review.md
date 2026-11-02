IMPERIA COLD WAR: Independent USA tax-calibration review

24 October 2026. Reviewed `economy.py`, `test_economy.py`, the emitted economy provider and `USA_ECONOMY_PLAYABILITY_20261024.md/.json` before parent integration. This reviewer changed no runtime file, compiler, test or economy source and launched no game process.

## Finding corrected during review

The original forecast used a sum of consumer-goods percentages, giving 1.545. That was inconsistent with the supplied screenshot's native "Factors multiplied together" heading. The six displayed factors produce:

`0.99 * 1.05 * 1.04 * 1.10 * 1.355 * 1.01 = 1.6274632374`.

The author corrected the forecast API to take the final multiplier directly, added an independent compound-factor function and regression, and updated the evidence. The emitted rate changes themselves remain 48 to 20 and 42 to 17.5. This finding is resolved in the reviewed versions.

The native engine's English production tooltip at `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/localisation/english/production_l_english.yml:71` explicitly uses the civilian plus military industrial total, fulfilled by civilian factories. Its line 76 labels the factor product. The installed MD tax effect at `common/scripted_effects/00_money_system.txt:327` sets the base to `corporate_tax_rate * 0.015`; `common/dynamic_modifiers/00_money_dynamic_modifiers.txt:20` passes that to native `consumer_goods_expected_value`. The separate scripted display estimate at `00_money_system.txt:4766` is not proof that native construction adds factor rows.

With 162 total industries and 100 civilian factories, the six-factor product gives these conditional forecasts:

| Corporate slider | Required civilian factories | Conservative usable factories, rounding demand upward |
| --- | ---: | ---: |
| 48 | 189.82731 | 0 |
| 42 | 166.09890 | 0 |
| 20 | 79.09471 | 20 |
| 17.5 | 69.20787 | 30 |
| 25 | 98.86839 | 1 |

The screenshot's rounded total 1.62 instead gives 78.732 and 68.8905 for 20 and 17.5, with conservative counts 21 and 31. The author's revised report distinguishes the observed rounded total from the product reconstructed from displayed rows. Neither reconstructed product nor ceiling assumption establishes the exact post-change integer count in the engine. The source-product bounds are the safer statements when promising minimum capacity.

## Provider and migration review

No remaining implementation defect was found in the bounded provider before the coordinator's call-site integration.

- Fresh-start initialization requires actual USA, the 1970 scenario, the existing systems-initialized receipt and no calibration receipt. Its integration contract puts it inside the original once-only initializer after the old fiscal assignments. It changes the corporate slider and marks the calibration once.
- Migration uses the same country/scenario/system/receipt guards. Exactly 48 becomes 20 and exactly 42 becomes 17.5. The latter preserves the 42/48 relative reduction. Other values, including 20, 25, 42.5 and 47, remain unchanged and receive the receipt.
- Because even unchanged custom rates receive the receipt, a player later choosing 42 or 48 is not recalibrated on the next reconciliation. A country outside the scope or a save without the systems initialization is not marked prematurely.
- A changed migration calls native tax recalculation, dynamic-modifier refresh and the ordinary fiscal recalculation. It does not directly change treasury, debt, tax-gain multipliers, spending, sanctions arrays or recurring streams, and it does not apply an extra weekly payment.
- The native slider also changes its existing investment-cost and productivity-growth outputs in `00_money_system.txt:334` and `:342`. These are normal consequences of the same native tax input, rather than an added compensation mechanism.

The source's current history calls `USA_1970_initialize_systems` at `history/countries/USA - USA.txt:58`, before ordinary startup fiscal calculation. `ingame_update_setup` calls `calculate_tax_gain`, which calls `calculate_tax_rate` at `00_money_system.txt:415`. The proposed fresh-start hook must stay after the old 48 assignment and inside that once-only initializer. The parent still owns installation of the two call sites; this review does not claim they are already integrated.

The older source cannot distinguish a manually chosen exact 48 from its default, or a manually chosen exact 42 from the supplied save. The authorized migration explicitly names those two values. It preserves every other value and all choices made after its receipt; it does not claim to infer prior player intent from a bare number.

## Native benchmark and historical interpretation

The actual MD 2.0.2 donor USA 2000 history at `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/history/countries/USA - USA.txt:881` uses corporate slider 30 and population slider 25. Comparable main-MD histories use UK 19, Japan 23, France 28 and Germany 35 at lines 1610, 133, 2391 and 1541 respectively. The local native missing-value fallback is 20 in `00_money_system.txt:6431`. These are native economy settings with different factories and modifiers; none independently proves that 20 is the unique correct USA 1970 rate.

Historical statutory rates are a different quantity. The primary [IRS Table 24](https://www.irs.gov/pub/irs-soi/09sprbul.pdf), printed page 245, lists a 49.2% top bracket for 1970 including the 2.5% surcharge, and 48% for 1971-74. Thus the original 48 is recognizable as a basic statutory rate, while the new 20 is an explicit MD gameplay calibration. It is not a claim about the historical top rate, actual effective business rate, federal share of GDP or share of factories employed in government production.

## Fiscal playability remains a material qualification

The earlier native startup observation at `tools/usa_1970_expansion/native_probe/runs/usa_final_20261024/bounded_loading_attempt_3/profile_logs/game.log:1607` records income 69.25320, corporate receipts 49.76320 and expense 54.85895, with 120 treasury and 371 debt. The preceding line records native GDP 3941.76292. This is a real earlier observation at corporate slider 48, not a post-calibration observation.

Holding its other readers fixed, rate 20 projects income 40.22467 and a weekly deficit of 14.63428 MD billions. That is approximately 761 MD billions over 52 weeks, or 19.3% of the recorded annual GDP scale. The unchanged initial 120 treasury lasts about 8.2 weeks at that fixed flow, before policy setup fees or other spending. Rate 17.5 would project a 17.22612 weekly deficit against the same frozen baseline; the supplied save may have different income, expenses, reserves and debt, so that is not its observed balance.

Native deficit financing prevents an immediate cash lock. `common/on_actions/MD_on_actions.txt:164` applies the signed weekly balance and then calls `automated_debt_taker`. At `common/scripted_effects/00_economic_system_utilities.txt:29`, negative treasury triggers an advance equal to 1.25 times the shortfall plus 1% of GDP. Treasury receives the advance; debt receives 101% of it. This is borrowing with a fee, not free revenue. The interest provider at `00_money_system.txt:2572` includes debt/GDP, the central-bank rate, tension and modifiers. Debt service at line 2603 is debt times 0.00019 times the annual-rate number and the currency debt factor. It rises as debt grows.

The bankruptcy mission at `common/decisions/bankruptcy_decisions.txt:901` activates when debt service exceeds potential income, subject to its peace/recent-collapse conditions. An ordinary weekly deficit is not itself an immediate bankruptcy trigger. Nevertheless, freeing 20 to 31 construction factories does not establish a sustainable or enjoyable budget: the new baseline requires substantial fiscal management, and native AI deficit rules may raise taxes again. The calibration should be presented as restoring construction capacity with an explicit revenue trade-off. A longer-run playability claim still needs a normal post-fix fiscal observation and policy response, rather than hidden cash, a debt wipe or an undocumented spending discount.

## Independent checks and reviewed hashes

All 15 focused tests passed under a reviewer harness that blocked both `Path.write_bytes` and `Path.write_text`. Thus the suite's deterministic-emission check also completed without writing runtime outputs. The report's eight recorded source hashes all matched the inspected files.

| Reviewed file | SHA256 |
| --- | --- |
| `tools/usa_1970_expansion/economy.py` | `ff42dcbca9942637a3869f552ac9c258c40bbd735ee932712fc8f88b210b512a` |
| `tools/usa_1970_expansion/test_economy.py` | `17578a853a78a8144d12a3ada18b2b51597dd1811bb41dde2dc339cd56c6ef41` |
| `common/scripted_effects/COLDWAR_USA_1970_economy.txt` | `6d65c355009baf21facd2d6360181e9105fc3391a9f51ac23bc3e3f122aba3e4` |

No native process, live save, post-fix hover, new factory count, updated budget, long-run AI behaviour or multiplayer session was tested by this reviewer. Parent integration, emitted validation and any current-save refresh remain separate evidence.
