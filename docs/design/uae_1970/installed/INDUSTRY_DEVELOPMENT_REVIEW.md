# UAE industrial start and population development

> Historical industrial-revision snapshot. The later maritime content, current growth cap and prospective tooltip correction are covered by [MARITIME_REWARD_REVIEW.md](MARITIME_REWARD_REVIEW.md). Current hashes and all 110 positions remain in `LAYOUT_REVIEW.json`; the growth figures and conditional-preview description below describe the earlier reviewed build.

Reviewed 19 October 2026 after the final 110-focus compile. No material layout or starting-industry finding remains. This is the current supplement to the earlier independence/proclamation review; the original approval snapshot remains immutable.

## Starting industry

`economy_start.build(data)` is a pure generator returning exactly three files: the dedicated industrial-start effect and narrowly marked additions to states 179 and 180. The compiler installs them. The industrial module does not edit the oil bootstrap, global money system or GDP calibration.

`COLDWAR_UAE_startup_industry` requires original, non-dynamic UAE in the January 1970 campaign, current date before January 3, both Dubai and Abu Dhabi owned and controlled, no historical GDP-profile receipt and no previous industrial-start receipt. It subtracts Dubai's 19 light-metal units and Abu Dhabi's 22 light-metal and 5 steel units exactly once. The existing oil setup independently supplies its approved 1+3 oil baseline.

The same one-time transaction removes any initial composite plants through native `remove_building`, using a bounded five-attempt loop matching the actual native state cap. Native API precedents include main MD `00_investment_targets_effects.txt:54–57` for temporary-counter loops and `05_afghanistan.txt:2317–2322` for conditional native building removal. A zero-progress operation cannot hang initialization. No recurring clamp removes later development.

The 1970 state snapshots explicitly set composite plants to zero. Separate 2000 history snapshots restore Dubai's native one plant and Abu Dhabi's zero. These are bookmark-load history entries, not scheduled events during an ongoing 1970 campaign. The patch is reversible by removing only its markers; all other state bytes, including existing LF/CRLF, UTF-8 BOM, undated resources, geography, buildings and later history, remain intact. Existing later dated blocks are extended without duplicating their date key.

`python tools/uae_1970/test_start_economy.py --installed` passes **119 checks**, including all 36 valid initial plant-level combinations, bounded termination without removal progress, all identity/date/ownership/control guards, repeated calls after paid resource/plant additions, modern-start exclusion, 1970/1990 versus 2000/2017 plant snapshots, byte reversal and idempotence. All three installed outputs match the pure build. The exact output hashes are in `tools/uae_1970/START_ECONOMY_VALIDATION.json`.

The GDP adjustment remains frozen once at startup. Later paid resources and industrial assets contribute through native recalculation; this module neither resets that offset nor grants money, output or buildings to compensate for the reduced starting industry. This is source/AST evidence, not observed engine GDP accounting.

## Current layout and native presentation

The independent parser in `audit_layout.py` verifies all **110 focuses, 98 relative anchors and 12 groups** against the explicit current revision. It checks actual emitted positions, grouped prerequisites, reciprocal exclusions, durations, titles, descriptions and native artwork. No unrelated card/connector intersection is found. The maximum title advance remains 142 pixels inside the native 147-pixel field.

| New focus | Position | Native title width |
|---|---|---|
| The Jebel Ali Smelter | (33,16) | 127 px |
| Steel Rolling Mills | (37,16) | 107 px |

Both follow Earnings beyond Oil; they are independent investments, without an exclusive link between them. Commerce extends through row 16, leaving row 17 empty before the third-tier roots at row 18. Every previously installed focus retains its position. In particular, the entire society branch and the neighbouring oil, defence and diplomacy sections stay in place.

The reviewer opened the current native-art `OVERVIEW.png`, `BRANCH_commerce.png`, `BRANCH_society.png` and `INDUSTRIAL_NEIGHBOURS.png`. The new native smelter/mill icons and titles fit; the fork reads clearly; there is no clipping or new connector crossing. The industrial-neighbour proof retains the full oil and diplomacy cards instead of isolating the extension. The society view confirms that its updated costs and durations did not alter card geometry. DDS artwork, titlebar and the native bitmap font are inherited; connector routing and unavailable shading remain labelled external approximations.

The final focus source SHA-256 is `e86584281ebf44ff75e9b659ffcdff41c11036fedcba9a9eddc3ceea2daf50b9`. The development overlay SHA-256 is `dd51ed83db1047800c73dc0f9cf1d89d000c719f9f1cd7495ce1a6b82cff0d12`. `LAYOUT_REVIEW.json` records the complete current source hashes and `FOCUS_MANIFEST.json` records actual source lines and all 110 cards.

## Rewards and preserved conditions

The paid industrial-port alternative now commissions one civilian factory and a shared slot in Dubai after its 105-day focus, for $7.5 billion. The paired aviation alternative commissions one airbase level after 105 days for $2.5 billion, without adding a shared slot. Their exclusion remains unchanged. The physical grants and treasury costs are native effects; tooltips no longer advertise receipt flags or a generic economy-refresh call as rewards.

The smelter costs $4.5 billion and adds 12 base light-metal units in Dubai with a +12% energy-use contribution; rolling mills cost $3 billion and add 5 base steel units in Abu Dhabi with +6% energy use. Both require an actual completed Dubai civilian factory plus the recipient state's current ownership/control. Their one-time receipts protect the resource grants from replay; the associated energy contribution follows control of the relevant industrial state. The aviation choice itself does not provide the required civilian factory, so its later metal development needs another completed-factory source.

The five society updates retain native numeric programme presentation. Their population bonuses modify the native growth rate; they are not flat percentage-point additions to population each month. The compatible citizen-housing route supplies +160% growth-modifier contribution from these focuses, while the workforce-housing route supplies +200%, alongside their declared budget/energy burdens. The total tree contribution is additionally clamped at+200% on refresh, and the native reward preview shows its actual marginal amount at the cap. Other national and native growth modifiers still combine normally. The stronger services remain earned national development rather than a repeated one-time population grant.

The independent emitted-preview evaluator passes **1,980 contexts**, including accepted agreements, government eligibility, earned spirit remedies, caps, expired contributions, and loss of control of states 179/180. Every displayed numeric modifier and treasury debit agrees with separate data arithmetic. The existing 36 opening-gate and 60 dated office-preview checks also remain clean. No unrelated gameplay payload was changed by the auditor.

## Remaining engine checks

Actual HOI4 loading, native hover formatting, connector routing, growth over time, startup GDP calculation, multiplayer synchronization and progressed-save behaviour were not observed in this review. The historical-start transaction deliberately refuses to run after GDP calibration or outside the first two days, so it does not silently strip an already developed save.

Subsequent user correction: capped total tree growth at+200%, with40/30/50-or90/40% focus contributions. Source validation82583, development7cases and presentation2339checks pass; the1980-context installed-preview audit was rerun with an independent capped-growth expectation. Live HOI4 remains untested.
