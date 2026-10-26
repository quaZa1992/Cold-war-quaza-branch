# Saddam concept: independent mechanics review

Reviewed 21 October 2026. Design-only review of `CONCEPT.json` and `build_concept.py`; no loaded game files changed by this review.

**Result: no remaining must-fix mechanics or reward-design issue in the final concept.** The weak initial household option and infrastructure-category timing issue have both been corrected. This conclusion covers source-supported mechanics and the concept's arithmetic. It does not establish engine execution, save migration, actual in-game tooltip rendering, or multiplayer behaviour.

## Five exclusive programmes

Every row compares the complete two-focus programme. Both alternatives consume the same time and percentage-of-GDP allocation within that pair.

| Pair | A | B | Assessment |
|---|---|---|---|
| Government | +15% political power gain, +15% command power gain, +12% influence defence, +8% army intelligence, +10% planning speed; +8% police spending | +12% efficiency growth, +5 points efficiency cap, +5% office productivity, -4% education spending, one 50% industry research bonus; -5% political power gain | Distinct executive/military coordination and industrial-professional rewards. The alternative remains authoritarian ministerial delegation. |
| Industry | Baghdad: one civilian industry; +6% military output, +10% efficiency growth, -10% resource-shortage penalty; +2% consumer-goods factor | Baghdad: one office; +10% civilian productivity, +10% office productivity, -15% incoming investment cost, +10% office tax income; -3% population tax income | Both deliver a tangible building. Do not describe the productivity modifiers as national GDP percentages or the investment modifier as free foreign finance. |
| Education | +4 percentage points literacy; +3% direct research speed; Nineveh: one infrastructure level. Native literacy additionally changes research, office productivity, education spending, productivity growth and agricultural productivity | +5 points starting production efficiency, +4 points efficiency cap; 35% construction, 35% electronics and 50% industry bonuses; +5% education spending | Strong permanent broad education against specialist production and substantial finite research grants. The literacy cap and native agricultural downside are disclosed. |
| Army | +3% organisation, +4% defence, -5% supply consumption, -8% equipment design XP cost, 25 army XP; +6% army personnel spending | +8% recovery, -10% army training time, 60 army XP, one 35% land-doctrine cost reduction; +4% army personnel spending | The military values remain modest beside the compatible shared army tree. Both affect the national army; the concept does not falsely claim template-specific Guard bonuses. |
| Households | -8% consumer-goods factor, -10% health spending, Maysan: one infrastructure level; +6% social spending | +8% civilian productivity, +8% efficiency growth, +6% corporate tax income, +8% office tax income; -3% population tax income, -2 points stability | Final revised A is a credible service-and-budget alternative to B. Keep the infrastructure and medical efficiencies instead of adding another generic factory. |

The five pairs produce 32 combinations; each full Saddam route takes 15 focuses and 679 focus days. The summed one-time allocation is 34.5% of annual GDP quoted at different completion dates, **not** a fixed treasury forecast or annual recurring tax. Replacing the old Saddam programme is essential: these values are not additions on top of its old 18-focus reward carrier.

## Units and actual consumers

- `consumer_goods_factor` is a relative factor. Current MD computes displayed consumer goods as `consumer_goods_expected_value * (1 + consumer_goods_factor)`: `common/scripted_effects/00_money_system.txt:4605-4613`. The preview correctly says factor; -8% does not promise eight percentage points of civilian allocation.
- Health, education, social, police and personnel fields multiply the corresponding budget costs. They do not directly raise spending-law levels or public-service quality. The descriptions connect medical efficiencies and purchasing to lower costs rather than claiming a new law.
- `civilian_factories_productivity` and `offices_productivity` have real sector income and GDP readers: `00_money_system.txt:463`, `:523`, `:5934`, `:5955`. A +10% sector modifier is not +10% national GDP. `industrial_capacity_factory` is military production output; it is deliberately different from MD military-sector economic productivity.
- `receiving_investment_cost_modifier` has an actual reader in `common/scripted_effects/99_investment_scripted_effects.txt:171`. It needs a real investment transaction and does not compel a partner to invest.
- Office/corporate/population tax-income modifiers change their collection/income channels. They are not changes to nominal household or corporate tax rates.
- Literacy uses `LR_change` with `update_literacy_rate`; the native calculation is in `common/scripted_effects/00_education_effects.txt:121-130,166`. Before the 100% literacy cap, +4 points yields +2 points research, +2 points office productivity, -4 points education-cost contribution, +0.08 native productivity-growth contribution and -2 points agricultural-productivity contribution. Do not duplicate these derived changes in the Saddam carrier.
- `army_morale_factor` is recovery; negative `training_time_army_factor` shortens army training. `equipment_upgrade_xp_cost`, efficiency growth/cap/base/retention, army intelligence, influence defence, organisation, defence and supply are native supported modifiers. Equipment-design savings need an actual eligible equipment design to spend XP on.
- The doctrine reward must compile as `add_doctrine_cost_reduction` with `category = land_doctrine`, `uses = 1`, `cost_reduction = 0.35`; it must not become an ordinary technology research bonus. Native Iraq `05_iraq.txt:5899` uses this reward form.

## Compatible stacking

These are explicit source sums, not newly implemented hard caps. They exclude technology, laws, advisors, temporary offensive ideas and the starting national burdens.

| Route/source scope | Sum | Implication |
|---|---:|---|
| Shared command + professional defence + new Guard | +16% organisation | 2% command review +3% professional command +8% defence professional +3% Guard. Baath screening instead of the National Front subtracts one point. |
| Previous row + Southern Command + War of Reserves | +24% organisation | Existing Iran-war focuses add 4% each. Do not describe 16% as the whole-war maximum. |
| Shared mass reserve + reserve training + land schools + new regular-army route | +22% recovery | 8% +3% +3% +8%; the mass reserve's -3% organisation is retained. Professional defence plus the regular route instead gives +11% recovery before other sources. |
| Baath + heavy industry + maintenance + new public corporations | +14% military output | 4% +5% -1% +6%. |
| Previous row + war economy + sustained Iran war + No Easy Exit | +40% military output | Existing 8%, 8% and 10% wartime rewards carry substantial existing personnel, consumer-goods and research penalties. |
| Baath + heavy industry + credit follow-up + maintenance + machine tools + new ministerial/specialist route | +33 points efficiency cap | Existing 24 plus new 9. No new universal output multiplier or extra national organisation is hidden in these bonuses. |
| New Saddam programmes alone | +0% to +30% efficiency growth | The 30% route is ministerial authority + public corporations' follow-up + production incentives. |
| Previous growth route + National Front/enterprise audit + oil training/Baiji + public-finance/maintenance + defence procurement + wartime procurement + sustained Iran war/contracts | +98% efficiency growth | This is the main cumulative hotspot. It accelerates filling production efficiency; it does not add 98 points to the efficiency cap. Previously earned reconstruction contracts can add more if their live condition remains true. Avoid further growth rewards in this redesign. |

Old Bakr leader programmes and other-party programmes cannot be counted as simultaneous Saddam benefits. The current programme gate is actual Baath slot21 and actual Saddam office-holder. One-time buildings, research, XP and literacy survive government changes but must never replay.

## State and technology verification

- **557** includes Baghdad/province11266 and is Iraq's capital; **171** is Basrah. Civilian industry, offices and arms factories are actual MD building types. Capacity, ownership/control, funding and once-only receipt guards remain implementation requirements.
- **166** is Nineveh; **167** is Salahuddin, containing Baiji; **1124** is Maysan, containing Amarah/province14401. Current `history/states/1124-Maysan.txt:18` starts at infrastructure1, so the proposed service programme raises it to2.
- Current early `CAT_construction`, `CAT_industry` and `CAT_electronics` technologies have usable 1960s/1970s entries in `common/technologies/mdcw_historical_industry.txt`. Research bonuses are finite uses, not permanent research-speed modifiers.
- The initial `CAT_infrastructure` bonus was changed to `CAT_construction`: infrastructure's added rail targets are1940/1953/1960/1967 (`mdcw_early_railway.txt:27,42,58,73`); the next native railway target is1985 (`common/technologies/industry.txt:3797`). The final construction bonus avoids an unnecessarily stale research reward.

## Native presentation and implementation boundary

Descriptions explain institutions, policies and consequences in English. Costs and effects are numeric in the inspector; implementation explanations are confined to concept notes. Mutual exclusion represents competing allocations or authority over the same offices, not the ahistorical claim that Iraq could have either education or technical institutes, either private firms or state companies, or either regular soldiers or a Guard.

Before any later implementation, preserve or explicitly migrate the removed Saddam dossier/credit/debt access receipts, keep meaningful office-holder requirements visible, hide redundant predecessor/scenario receipts, maintain transactional cost/delivery guards, add the real programme icon/localisation, and verify the resulting effects in the game. These are implementation obligations, not claims that this concept has already installed them.
