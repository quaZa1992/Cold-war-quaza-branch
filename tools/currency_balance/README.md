# Currency drawbacks

All existing currency law IDs now have a fixed drawback. Values are deliberate
game-balance abstractions, not historically measured monetary-policy effects.
The user authorized all currencies for this balance pass, including the Deutsche
Mark; its previous exclusion concerned the presentation/icon pass.

| Currency | Fixed drawback | Status |
|---|---|---|
| US Dollar | -5% foreign-influence defense | Added; exposure through an international financial network |
| Deutsche Mark | +0.25 percentage points interest | Added; restrictive-credit abstraction |
| Euro | +50% economic-cycle and cycle-upgrade costs | Retained |
| Chinese Yuan, all three tiers | +5% outgoing investment-project costs | Retained |
| Japanese Yen | -2 percentage points investment returns | Retained; already included in projected total return |
| Soviet/Russian Rouble | +7.5% incoming investment-project costs | Added; constrained external capital access |
| British Pound | -2.5% foreign-influence defense | Added; exposure through international finance |
| Swiss Franc | +5% incoming investment-project costs | Added; expensive domestic investment location |
| Dutch Guilder | -2 percentage points investment returns, -5% base migration | Retained |
| Brazilian Real | +0.5 percentage points interest | Added; credit-risk abstraction |
| Bitcoin | +15% inflation-cost multiplier | Retained; affects spending costs, not a direct inflation-rate increase |
| Generic Domestic Reserve | +5% incoming investment-project costs | Added; limited external credit access |
| Mark der DDR (Ostmark) | +10% incoming investment-project costs | Added; currency and capital controls |

New drawbacks use direct visible native modifier entries rather than hidden
modifiers or duplicated manual numeric tooltips. The Ostmark retains +0.05
political power/day, +2 stability points, and -0.5 interest-rate points. Its former
second interest line was explanatory text, not another interest effect; that
line and its reference have been removed. The remaining native entry is labeled
in percentage points in English. The name retains German wording in English UI.

`receiving_investment_cost_modifier` adds to the target-country component of the
investment project cost. It does not directly confiscate investment income.
`foreign_influence_defense_modifier` is read by the influence/manipulation system.
`interest_rate_multiplier_modifier` adds percentage points before the existing
interest clamp. The current debt system still has a single national-debt balance.
Removing a currency removes its static modifiers through normal law replacement.

Existing reserve calculations, issuer/adopter counts, currency-strength/inflation
formulas, migration flags, date gates, AI conditions, icons and country history
are preserved. New games and existing currency holders use the updated law
definitions after restarting HOI4 and loading. No new campaign is necessary.

## Validation

```powershell
python tools/currency_balance/validate.py
python tools/historical_currencies/validate.py
python tools/ddr_currency/validate.py
```

The new balance audit validates current source and exact before/after edits.
Older audit baselines are not rewritten: the balance manifest reverses this
authorized pass before those earlier preservation checks. The historical audit
therefore checks its original presentation-stage law modifiers, while this
balance audit checks the actual current modifiers. Static checks are not an
in-game test.

Sources motivating the broad trade-offs, rather than their numerical values:
[contemporary study of Comecon currency controls](https://www.bpb.de/shop/zeitschriften/apuz/archiv/533656/das-waehrungssystem-der-rgw-laender/),
[IMF study of dominant-currency finance](https://www.imf.org/en/publications/staff-discussion-notes/issues/2020/07/16/dominant-currencies-and-external-adjustment-48618),
[Swiss National Bank discussion of the franc](https://www.snb.ch/en/snb-explained/swiss-franc).
