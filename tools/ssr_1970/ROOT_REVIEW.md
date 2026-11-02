IMPERIA COLD WAR

# Root implementation review

Read-only review of `compile.py`, `integration.py`, and the current emitted focus and reward files. No generators were run and no implementation files were changed. This was a static review, not an in-game parse or runtime test.

## Findings

1. **Public ownership focus advertises the market-auction decision.** `compile.py` maps every non-offer `decision` node to `COLDWAR_SSR_market_light_industry_auction` (line 159). The emitted `COLDWAR_SSR_UKR_p4_public` focus repeats that unlock tooltip (focus file line 3213), while the actual public transaction is `COLDWAR_SSR_market_light_industry_public` (market decisions file line 78). The auction decision requires `COLDWAR_SSR_market_has_market_authority`; the public decision requires `COLDWAR_SSR_market_has_public_authority`. The public-charter branch therefore previews the wrong decision and does not identify the public method available to that route.

2. **Removing the Union exposure previews no numeric relief.** In `modifier_preview()`, `remove_exposure` emits only the “Remove Unconverted Union Orders” tooltip (`compile.py` line 140). The removed national spirit carries `tax_gain_multiplier_modifier = -0.04` and `civilian_factories_productivity = -0.05` in the approved model, and lifecycle reconciliation removes it after either `COLDWAR_SSR_export_conversion` or `COLDWAR_SSR_domestic_chains` is rewarded (`lifecycle.py` line 303). Both focus previews show the spirit removal label but omit the corresponding `+4%` tax income and `+5%` civilian factory productivity changes.

## Checks with no issue found

- The shared tree contains 201 unscoped common nodes, including all 99 specialization focuses. All 14 country views include the shared menu, and every focus is guarded by the appropriate SSR or independence status.
- Country-specific party branches use MD party-in-power triggers in availability while `allow_branch` remains country-only, so party content stays visible when another party governs.
- Relative anchors and transitive prerequisite/exclusion references resolve; anchors precede their children in the emitted tree.
- Focus execution rechecks requirements and the one-time receipt before charging GDP and granting rewards. Building rewards add the matching shared slots before construction, and resource focuses check for existing state resources.
- Repair, market-course, and bilateral-offer previews have matching scripted-effect callbacks. The generated integration hooks call finance refresh and lifecycle reconciliation.

