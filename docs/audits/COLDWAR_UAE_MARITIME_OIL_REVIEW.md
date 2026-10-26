# UAE focus costs and maritime transition — independent review

Reviewed 19 October 2026. **No blocking finding in the inspected scope.** This supersedes the earlier maritime reward review. The reviewer changed this report only, not generators, tests or game files.

## Treasury costs

All **110** emitted focus availability/application triggers have no Treasury comparison. All **52** priced focuses retain exactly one negative `treasury_change` and one native `modify_treasury_effect` call in their actual application. Costs also remain visible through the native non-executing preview. Political, treaty, prerequisite, exclusion, ownership/control, building-capacity and one-time delivery guards remain.

The native provider at `common/scripted_effects/00_budget_effects.txt:1487` adds `treasury_change` directly; it has no affordability check or lower clamp. Its existing `MD_skip_treasury_cost` flag serves history setup and is unchanged. Negative Treasury is therefore possible immediately after completion. Existing MD weekly processing calls `automated_debt_taker` (`00_economic_system_utilities.txt:29`, `common/on_actions/MD_on_actions.txt:169`): its borrowing amount is 1.25 times the shortfall plus 1% of GDP, with a 1% debt fee. This revision introduces no separate loan system. Decision and recipient-agreement affordability remains separate from focus eligibility.

## Maritime reconciliation

`tools/uae_1970/maritime.py` counts the four successfully delivered oil-focus flags, independent of their completion order. Retained share is `max(0.20, 1 - 0.20 × delivered phases)`.

Only the explicitly named sources scale:

- Starting **Pearls, Fishing and Dhows**: agriculture productivity +10%, office productivity +3%, social-cost multiplier −5%.
- **Pearls and Fishing**: agriculture +10%, offices +6%, social costs −2%.
- **Fishing Harbours**: agriculture +10%, social costs −3%.

With both maritime focuses earned, their combined contributions are:

| Delivered oil phases | Retained share | Agriculture productivity | Office productivity | Social-cost multiplier |
|---:|---:|---:|---:|---:|
| 0 | 100% | +30% | +9% | −10% |
| 1 | 80% | +24% | +7.2% | −8% |
| 2 | 60% | +18% | +5.4% | −6% |
| 3 | 40% | +12% | +3.6% | −4% |
| 4 | 20% | +6% | +1.8% | −2% |

Unrelated commerce contributions retain their full values. Harbour naval-base construction +15%, bureaucracy +3%, energy use +2%, and the starting productivity-growth penalty/remedy remain unscaled. Reconciliation recomputes from original contributions; repeat calls neither compound the reduction nor replay money, buildings, resources or experience.

The registered percentage modifier `social_cost_multiplier_modifier` is read by `00_money_system.txt:3493`: it multiplies the population-based social-law cost before the spending ladder. The separate `gw_welfare_weekly` charge is added afterward. A weakening negative social-cost modifier correctly appears as a **positive cost delta**, not an income payment.

## Native presentation and independent checks

`presentation.py:272` supplies named native numeric oil-loss previews for starting and already-earned maritime sources. Future, unearned coastal grants are excluded. Both maritime focus previews use the current retained share. The reviewed emitted fragments exactly equal the current provider output. Advertised main rewards remain outside current-eligibility wrappers; actual application and programme guards remain authoritative.

**3,383 independent assertions/equality checks passed**, covering all 16 oil-flag subsets × four maritime-earned states; 256 marginal oil-preview contexts; 128 coastal-preview contexts; all focus gates and costs; and eleven representative negative-Treasury completions. These included repeat application, unchanged unrelated commerce, harbour costs, the unscaled growth remedy, and no asset/cash replay. The focused interpreter deliberately excludes native economic recalculation and game UI behavior.

This establishes source/AST consistency. **HOI4 loading, rendered native hovers, actual weekly economic outcomes, save/reload and multiplayer were not tested.**

## Reviewed artifact hashes

SHA-256:

- `tools/uae_1970/maritime.py`: `5da1e13c035676eba92a4d25923734302e58ca5857074ca4ad1fd8d9c798ccfe`
- `tools/uae_1970/presentation.py`: `4eb10c5cfec7aec29032e16f29bfdab2d30918ac1a4598e61ddf06f8b318b9b6`
- `common/national_focus/COLDWAR_UAE_1970_focus.txt`: `5e7473cfc34c866649e2f53f600d73cf1fcadc72f5067d5fc084ba0cf0ed8e96`
- `common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt`: `68a982c07e33bc61f97881a0a1ad8e18794d521625cf3e2993daab77280167d3`
- `common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt`: `45cf9f4a597f9ebd1315bf407356d517f9d1344d07bebaf4a3f87997660c1b10`
- `common/scripted_effects/COLDWAR_UAE_1970_programmes.txt`: `c2af5329c5ecb9f54429fcf20f33117e53e9f57a474fbabc537bb1427e413e4e`
