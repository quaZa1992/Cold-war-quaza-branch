IMPERIA COLD WAR: Gulf daily-proration precision repair

24 October 2026. Bounded repair of `tools/iraq_1970/usa_module.py` and its seven owned Gulf runtime outputs. The Iraq compiler, US focus tree, resistance handler, approved catalogue, other Iraqi content and staged focus fragment were not written by this repair.

## Preserved policy

The existing programmes keep their intended weekly budgets of 0.05, 0.025 and 0.02 native MD billions, actual daily charging, 90-day funded-day counters, real recipient consent, route/control requirements, initial fees, equipment receipts and state/settlement policy. This does not add a new money-system income or expense stream. The existing explicit Treasury transactions remain authoritative.

The approved Gulf catalogue SHA256 remains `bdbec679bbe773ec793cba69f68fc5d37f83e2730548c459f055f02a2975fd34`.

## Native arithmetic

Python divisions previously emitted long literals such as `0.007142857142857143`. These violate the project's maximum five fractional digits and are unsafe input for the native fixed-point parser.

The generator now emits short positive weekly literals followed by native `divide_variable = { price = 7 }` to quote persistent daily prices. Affordability checks compare Treasury against those native variables. The installed native trigger documentation at `documentation/triggers_documentation.md:2116` explicitly permits a variable as the comparison value, so no unsupported inline expression is placed inside `check_variable`.

Actual payment uses the same positive weekly literal in `treasury_change`, divides with native `divide_temp_variable`, and only then negates a debit. Matched donor and recipient transfers therefore use the same positive native arithmetic before their opposite signs. No negative-division rounding asymmetry is introduced.

`COLDWAR_USA_gulf_recalculate_prorated_costs` sets three daily prices and their existing 0.5-plus-first-day relief funding floors. It is called before the Gulf daily observer and both settlement commitment effects. The parent USA initialization must also call it before opening controls. A never-initialized daily-price guard rejects the transaction instead of treating a missing variable as a zero price.

The installed native effect documentation declares both `divide_variable` and `divide_temp_variable`; the latter is at `documentation/effects_documentation.md:3587`. The supplied weekly numerators and divisor have valid short literal representations.

## Rounding boundary

Native division, rather than a pre-rounded Python decimal, now determines the engine's charge. The same computed price governs the funding boundary. Actual HOI4 division rounding had not been observed when this report was written.

An additional illustrative five-decimal truncation model yields:

| Intended weekly budget | Model daily amount | Model seven-day sum | Difference |
|---|---:|---:|---:|
| 0.05 | 0.00714 | 0.04998 | -0.00002 |
| 0.025 | 0.00357 | 0.02499 | -0.00001 |
| 0.02 | 0.00285 | 0.01995 | -0.00005 |

These are model values, not a claim about the engine's rounding mode. A native probe should log `COLDWAR_USA_gulf_prorated_005_daily_cost`, `COLDWAR_USA_gulf_prorated_0025_daily_cost` and `COLDWAR_USA_gulf_prorated_002_daily_cost`. No compensating residual ledger or new billing policy was introduced.

## Generator preservation

The original full Iraqi build also applied a separate decision-streamlining pass. Calling only the raw US generator would have reintroduced the retired `respond` and `uprising_aftermath` menus. The owned US generator now retains that exact two-ID retirement, and a comparison against the pre-existing installed decision AST verified the same 48 decision IDs. All other original Gulf runtime ASTs matched the original generator before the numerical repair.

The seven owned output files were rendered with the existing pure native formatter, preserving their established indentation rather than installing raw unformatted output. Modified scripts use UTF-8 without BOM; the English localisation retains its BOM and language header. Every modified code file begins with the required current project marker. Category, on-action and localisation changes are identification comments only.

## Checks

`tools/usa_1970_expansion/test_gulf_precision.py` runs the original 17 Gulf transaction checks and 14 native-treasury review checks in memory, extending their explicit model only for the documented divide operations. Their old artifact writes are intercepted, so earlier reports are preserved. The old whole-tree fixture asserting 214 unchanged US focuses is intentionally not run against the newly expanded 281-focus tree.

All 31 preservation checks pass. Additional checks cover exact daily affordability, rejection just below it, matched donor/recipient transfers, uninitialized-price rejection, 90 charged days and expiry. All generated scripts parse, no generated numeric literal has more than five fractional digits, and the loaded US tree stays unchanged during the test. Results are in `implementation_support_gulf_precision.json`. These are source/model checks; native calendar and multiplayer execution remain separate evidence.
