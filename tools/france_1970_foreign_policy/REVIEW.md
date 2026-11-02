IMPERIA COLD WAR — France foreign-policy proposal review

# Review result

**Freeze clearance: no design blocker found** for proposal SHA-256 `0f282ae598957dd25f8f75a40e422c0327d3015b501ba0c5f0cba16c57c67577`.

This is a source-backed proposal review, not a compiled-runtime or in-game test. The checker found 213 total focus nodes, 37 additions, 32 new recipient-approved offers across 16 mutually exclusive families, and zero issues. It verified the prior frozen baseline hash `57b479c47dafef3d83917931994617bf08c1467d8a00175aa28da957a7518628`.

# Mechanics and implementation boundaries

- All new modifier keys, eight research-category tags, and three doctrine categories resolve in the loaded mod's native definitions/consumers. Notable examples are `oil_export_multiplier_modifier`, `training_time_army_factor`, `army_org_factor`, finite `add_tech_bonus`, and finite doctrine cost reductions.
- The oil-export modifier changes the exporting country's proceeds from actual exported oil. It does not create a France-specific buyer, shipment, quantity, or price. The Gabon and Iraq offers describe export earnings and do not claim French oil offtake.
- Niger's uranium agreement grants resource rights only. Zinder has the source-defined deposit and mine capacity; production still depends on the existing investment and mine-building path. The proposal does not grant raw uranium output or an automatic mine.
- All 32 new offers have matched weekly transfer records. The same payer, recipient, GDP share, and amount are used for both countries' expense/income entries. Setup payments use the paying country's GDP at acceptance; recurring streams use the payer's GDP divided by 52. All checked literals stay within five decimal places.
- Every proposed building level has a same-state shared-slot grant in the proposal before construction, with ownership/control/full-control and physical capacity checks. The checker also verified dockyard coast requirements. Egypt's Alexandria target is below its physical airbase cap. Both Djibouti offers require DJI to own and control state 230 after independence; the state is French-owned at the January 1970 start, so the new checker records that expected transitional condition.
- The Niger focus has a visible condition for the state-wide existing French resource-rights case. The agreement's standing activation logic is separate and does not self-disable on acceptance.

# Route ceilings

These are conservative theoretical ceilings if every family is signed simultaneously, selecting the most expensive eligible option in each family. They are not expected playthrough totals.

| Scope | Setup cost | Recurring annual burden as share of own GDP |
| --- | ---: | ---: |
| New 16 families, France | 6.85% | 0.302% gross outflow, including transfers and programmes |
| New 16 families, highest partner | 0.75% (Saudi Arabia) | 0.34% (Saudi Arabia) |
| All 35 design families, France | 13.17% | 1.582% gross outflow |

Across the new France packages, the simultaneous maximum includes education-cost +31%, army-personnel cost +18%, air-force-personnel cost +13%, navy-personnel cost +10%, equipment cost +7%, army training time +8%, corporate-tax income -8%, and supply consumption -11%. Several are substantial costs. They represent a deliberately extreme all-family stack; ordinary play selects among family alternatives. The new setup maximum is a one-time GDP share, while the recurring figure is annualized from weekly expense streams.

# Remaining implementation limits

The proposal uses military access where specified; it does not promise docking rights or a guarantee unless the corresponding native effect is explicitly present. Bilateral partner-tag and custom effect support must still be checked in the runtime generator/compiler, and game-engine behavior remains untested in this review. Neither is a proposal-level blocker.

Checker: `check_design.py`, run against the exact hash above. Its only notes concern the expected French ownership of Djibouti in the 1970 history and the explicit post-independence recipient ownership/control guards.
