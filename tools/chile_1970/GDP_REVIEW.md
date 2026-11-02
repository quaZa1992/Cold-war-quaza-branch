IMPERIA COLD WAR — Chile GDP and cost scale review

Scope: read-only audit of Chile's actual 1970 GDP baseline, native money units, and the approved design's proposed monetary burden. No game or generator files were changed.

## Runtime baseline

The native engine log records Chile at 1 January 1970 with native GDP 28.2553, target historical 1970 GDP 9.261, calibrated internal GDP 31.48733, displayed GDP 9.26097, GDP per capita 0.9402, and population 9.84997 million (`docs/audits/open_findings_20261024/native_attempt_1_game.log:1638`). This is the best available live-country figure; no newer current-run Chile dump was located during this read-only pass.

The same log records weekly income 0.72514, weekly expense 0.84739 and balance -0.12225 (`...native_attempt_1_game.log:1639`). The parent task's fresher 31 October engine log has the same baseline GDP and income, but expense 1.06271 and balance -0.33757. Use the latter for today's deficit comparison; the GDP and income baseline match.

`common/scripted_effects/mdcw_era_reference_effects.txt:3-13, 15-27` establishes that 1970 `gdp_total`, debt, treasury and the MD money system use 2000-dollar internal values. Only GDP display is divided by 3.4 to show historical 1970 dollars. `common/scripted_effects/00_budget_effects.txt:1484-1494` confirms treasury debits apply the supplied amount directly; the treasury amount is not divided by 3.4. Thus a scripted `$1bn` debit is 1 internal billion (about $0.294bn in historical-1970 price terms), while GDP shown to players is about $9.261bn. Keep implementation arithmetic in internal units and explain any player-facing values consistently.

## Burden of the approved amounts

The frozen `tools/chile_1970/approved_design.json` has 184 nodes and $295bn summed focus-node `money` costs across mutually exclusive routes. The largest focus-node charge is $6bn; the largest bilateral setup fee is $4bn. Event options peak at $3bn, and decision contracts peak at $6bn. The $295bn sum is not a reachable route total; still, the larger individual cost sizes are out of scale for the 1970 baseline:

| Cost | Share of internal GDP 31.487bn | Approximate weeks of the fresh weekly deficit 0.33757bn |
| ---: | ---: | ---: |
| $1bn | 3.18% | 3.0 |
| $3bn | 9.53% | 8.9 |
| $6bn | 19.05% | 17.8 |

Even the $1bn floor is a large national commitment for a country whose 1970 weekly budget already runs a deficit. Since native borrowing permits these debits, oversizing does not necessarily block a focus; it can instead create debt and interest that the focus tooltip may obscure.

## Scale recommendation

Use a **1/20 scale for one-time setup costs** as the first rebalance pass. This turns the existing $1–6bn focus/decision range into $0.05–0.30bn, or 0.16–0.95% of the measured GDP baseline. The largest bilateral setup fee becomes $0.20bn and the largest event-option charge becomes $0.15bn. Suggested interpretation: ordinary institutional/policy initiatives $0.05–0.10bn; funded public projects $0.10–0.20bn; exceptional rescue or major national infrastructure $0.20–0.30bn. Reserve values above $0.30bn for a multi-year or externally financed project with a clear historical precedent. This is a proportional design recommendation, not a claim that every focus project had the same historical cost.

For **one-time focus and agreement costs**, keep fixed internal-bn amounts in the approved design, selected as fractions of the 31.487bn 1970 GDP baseline. This keeps the preview stable and lets a 1970 programme remain affordable as later GDP grows. For **recurring operating costs**, use a live GDP share calculated from current `gdp_total`, then convert any annual source budget to a weekly MD amount before integration. Show the resulting weekly amount in the preview. Cap all simultaneously active Chile programme and agreement expenses together around $0.01–0.015bn/week until an engine balance test shows a higher burden is sustainable. The designed bilateral $0.012bn/week aggregate is already about 1.7% of the logged weekly income; the current approved-design node stream total $0.0315bn/week would be about 4.3% if all such costs could overlap.

Treat the suggested recurring cap as a calibration target, not an affordability guard. Chile's deficit should not silently turn approved costs into free rewards; if spending is permitted to borrow, the UI should show the concrete fee and later native debt/interest consequences. Do not scale weekly literals by 3.4 merely because GDP's display is in historical dollars: the treasury and MD weekly budget remain on the same internal scale.

## Limits

This recommendation uses the supplied fresh engine figures plus repository formulas and frozen-design data. It does not launch HOI4, project later growth, or establish long-run debt/interest outcomes. The actual approved spend distribution across simultaneously reachable party and agreement routes still needs a separate route-level budget check after the tree is condensed.
