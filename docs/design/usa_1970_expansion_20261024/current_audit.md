IMPERIA COLD WAR: Current USA 1970 tree audit, 24 October 2026

Scope: source review of the loaded USA 1970 tree, its USA systems, Nixon offers, policy decisions and selected native providers. This is a design audit, not an engine or multiplayer test. Runtime files were not changed. `current_inventory.json` records all current focus definitions; `current_defense_route_sums.json` records two compatible military routes.

## Measured structure and reward shapes

The loaded tree is `common/national_focus/USA_1970.txt`, selected by `history/countries/USA - USA.txt:47`.

- 229 focus definitions: 50 opening Nixon focuses, 113 election-module focuses, 50 general economic/energy/society/diplomatic/defence focuses, 15 Gulf focuses and one Bahrain focus. The inventory's provisional GULF bucket includes Bahrain and therefore totals 16.
- Election modules: 17 definitions each for 1972, 1976, 1980, 1984, 1988 and 1992; 11 for 1996. These include 14 zero-cost election markers across all seven elections.
- Costs: 132 at 8.6; 26 at 5; 18 at 4; 17 at 4.3; 14 at 0; 10 at 2; 9 at 3; 2 at 6; 1 at 1. Do not translate focus cost into a claimed observed in-game duration without checking the engine.
- 41 definitions declare an exclusion. A count of exclusive nodes is not a count of distinct forks.
- Direct focus reward blocks contain 104 bureaucracy-cost helper calls, 82 stability rewards, 52 PP rewards and 18 generic research-speed helper calls.
- No direct `add_tech_bonus` or `add_doctrine_cost_reduction` appears in the tree. The USA 1970 core effects/events, Nixon effects/events, Gulf effects/events and Bahrain effects/events also contain no such specialised bonus grants. This supports adding limited-use sector/doctrine rewards. It does not mean the country has no research, doctrines or external systems.
- Only one direct timed-spirit grant appears in the tree, for Gulf air readiness. Transitive grants also exist: the Nixon price freeze is a 90-day spirit in `common/scripted_effects/USA_1970_nixon_scripted_effects.txt:9`; Israel assistance can trigger native 180-day AIPAC ideas in `common/scripted_effects/mdcw_1970_aipac_consumed_helpers.txt:2` and `:17`. Native army-law swaps are meaningful spirit changes too. Counting direct keys alone would miss them.

## What already works as a design foundation

`common/scripted_effects/USA_1970_scripted_effects.txt:8` initializes the native MD US policy modifiers, law system, Congress and internal factions. Nixon, the Republican presidency facing Democratic chambers, native institutional departments and the draft are already represented. The initial economy has treasury 120 and debt 371 (`:94`), factory-output variable -0.16 (`:104`), general construction -0.15 and civilian construction -0.35 (`:115`). These are actual systems a programme can improve rather than decorative national-spirit names.

Vietnam is substantial existing gameplay. `USA_1970_policy_decision_effects.txt:7` initializes domestic war burden and drug crisis. The overextension profile at `:53` adds personnel +60%, army personnel +150%, equipment +60%, supply +50%, consumer goods +10% and army training time +15% through the corresponding dynamic modifier. The staged settlement, drawdown and emergency-account decisions at `USA_1970_policy_decisions.txt:364`, `:436` and `:508` require real hostilities to end, time and substantial PP/money. A proposed diplomacy branch must preserve those systems and not promise automatic peace or instant removal of the costs.

The opening Nixon programme already offers credible choices: executive investigations versus lawful counterintelligence; clean campaign versus clandestine advantage; inflation restraint versus employment; market adjustment versus a temporary freeze versus tripartite guidelines; gold-window closure versus defending Bretton Woods; public health versus interdiction versus a national drug war; Vietnam operational ceiling versus Vietnamization versus escalation; congressional limits versus presidential operational discretion; Israeli deterrence versus Rogers diplomacy; volunteer transition versus Selective Service reform. Expansion should deepen their consequences, not invent a second copy of every choice.

## Confirmed presentation and integration gaps

### Building slots and transaction feasibility

51 direct focus blocks grant buildings. Only 3 of these contain any extra shared building-slot grant: the hydrocarbon, nuclear and grid focuses. The remaining 48 contain no slot grant. Their other calls are the reviewed numerical US adjustment, Congress, faction, regulation, treasury and party-popularity helpers, which do not grant shared slots.

Examples: `USA_1970_E1` at tree line 5039 grants three civilian factories; `USA_1970_E5` at 5240 grants seven infrastructure levels; `USA_1970_S3` at 6273 grants two offices. Each currently uses direct state construction without the project's required matching shared slots. Direct fixed-state grants also lack local owner/controller/native-capacity checks. A larger reward should not be promised until this transaction contract is corrected. Do not assume all three slot-bearing focuses already satisfy ownership/capacity rules simply because they contain a slot command.

### Party programmes and lifecycle

Election entry markers use the actual ruling-party variable in bypass predicates, for example `USA_1970_1972_democratic_victory` at 1659 and the Republican equivalent at 1686. The later programme focuses do not repeat exact native party-in-power checks in availability or completion. For example `USA_1970_1972_dem_1_end_the_imperial_presidency` at 1713 depends on the election receipt and directly applies permanent numerical changes. Therefore an earned election receipt can continue to authorize its programme after a later government change. There is no programme-specific suspension layer for these ordinary additive changes.

This is not a finding that party-dependent `allow_branch` hides the two parties. The entry markers instead have date-dependent `allow_branch` windows, such as `date < 1977.1.1` at 1664/1691. Older election branches become date-hidden. A redesign should explicitly separate durable national legislation from currently active party programmes, keep party branches inspectable, and use the existing exact-party triggers for visible live requirements.

### Bilateral agreements already exist, but lack the requested paired-spirit form

Do not describe the existing tree as having no foreign policy or no recipient consent.

- `USA_1970_F4` at 6011 offers Atlantic terms to Britain, France, West Germany and Canada via `USA_1970_send_atlantic_bargain_offers` at scripted-effects line 429.
- `USA_1970_F5` at 6030 approaches the USSR and China.
- `USA_1970_F7/F8/F9` at 6073/6102/6131 offer Israeli security assistance, mediation or Arab trade.
- `USA_1970_D6` at 6632 offers maritime basing to Britain, Japan and the Philippines.
- `USA_1970_E9` at 5473 offers North American trade to Canada and Mexico.
- The Nixon channel dispatchers at `USA_1970_nixon_diplomacy_effects.txt:11` onward set pending flags and deliver recipient-owned acceptance/refusal events. Summits require accepted earlier channels.

The ordinary recipient events in `events/USA_1970_events.txt` at 67, 129, 195, 261, 324 and 389 grant opinion, native trade/access, partner flags and US registration rewards. They do not create a pair of named treaty spirits with a shared active lifecycle. For example the Atlantic recipient gets opinion and a partner flag while the US package is applied after two registrations (`USA_1970_scripted_effects.txt:357`). Maritime acceptance at event line 324 grants access, but no recipient development/training spirit.

The generic dispatchers at effect lines 429-483 usually check only country existence. They do not share the Nixon pending protocol or a consistent war, embargo and mirrored-sanction guard. The ordinary offer events lack a common acceptance-time eligibility/funding transaction. Generic registrations often permanently mutate US variables, so a later war or revoked access cannot simply remove one identifiable partner's contribution.

The Bahrain agreement and Gulf module are separate existing content and require their own preservation/integration check. They must not be silently replaced by a new blanket Middle East branch. The available source proves these components exist, not that every effect is multiplayer-tested.

## Choice quality and useful expansion seams

| Existing choice | Current consequence | Stronger design seam |
| --- | --- | --- |
| Federal Industrial Grants / Market Investment Zones, tree 5039/5084 | Three factories versus two offices and one factory; regulation/faction/output differences. Follow-through also locks Great Plains and highways behind grants, while procurement corridors and zoning follow markets. | Make the choice public industrial renewal versus private capital formation. Give each its own sector outcomes, but move ordinary interstate maintenance and agriculture out of this arbitrary exclusivity. |
| Information Economy / Post-Industrial Bargain, 5493/5539 | Offices, research and workforce efficiency versus productivity/investment returns and PP. | Automation and technical education versus productivity-sharing and worker adjustment. Distinct follow-ups, finite research bonuses, costs already expressed in the native systems. |
| Federal Enforcement / State-Negotiated Compliance, 6223/6251 | Stability and federal enforcement costs versus lower bureaucracy and PP gain. Fair housing is locked to the former and tribal self-determination to the latter. | Retain equal-rights execution through two administrative approaches; give negotiated enforcement real investment and compliance benefits. Shared civil-rights measures need not disappear with the administrative choice. |
| Intelligence under Law / Keep the Covert Hand Free, 6541/6574 | Oversight versus intelligence reach; additionally locks AirLand Battle versus Second Offset. | Keep intelligence authority as its own choice. Let both governments modernize conventional doctrine and precision technology; put military procurement choices on an independent funded branch. |
| Volunteer Force / Renew National Service, 6462/6499 | Important native law change, small specialist modifiers and different political requirements. | Add training, retention and reserves follow-through. Preserve the very large native quality/manpower/payroll trade-off described below. |
| The Atlantic Bargain / regional offers | Consent already occurs; partner benefits are comparatively thin and US rewards are often aggregate. | Distinct country focuses with visible complete terms, a named spirit for each country, temporary exercises and standing agreements, plus negotiated follow-ups. |

Three specific low-satisfaction endpoints: `USA_1970_F10` at 6179 awards 100 PP, influence modifiers and Congress support for another +5 percentage points of bureaucracy cost; `USA_1970_S7` at 6383 awards 35 PP, +1% drift defence and a decision flag but also costs money/stability/administration; `USA_1970_N8` at 5892 supplies small energy/influence changes and upkeep flag. These are opportunities for identifiable institutions, finite projects or concrete continuation rather than a general numerical buff. Their flags really do unlock downstream decisions, so they are not empty focuses.

## Two compatible defence routes and the native-law caveat

The route JSON intentionally sums direct focus-variable deltas, not all national effects.

Route A: D0, D1, D3, D5, D6, D8. Route B: D0, D2, D4, D7, D6, D8. The OR prerequisites in D5/D7 and D6 make these compatible routes; D8 requires one of D5/D7 and D6.

Both routes directly add personnel-cost factor +16 percentage points and bureaucracy-cost factor +5 points. Route A pays 40 treasury, grants +1 point army attack, +3 points max planning, -2 points supply use, +2 points leader XP, +0.02 daily army XP, +0.01 air/navy XP, -3 points army training time, +2 points unit XP, -1 point recruitable-population factor and the small shared naval package. Route B pays 50 treasury, grants +0.2 points base conscription, +2 points recruitable-population factor, +3 points research speed, +1 point production-efficiency cap and the shared naval package. It also adds education cost +3 points, office-workforce requirement +2 points, consumer goods +1 point and loses 5 points PP gain and 4 points stability.

However, D1 and D2 call native army-law effects. `common/scripted_effects/00_military_effects.txt:131` swaps to volunteer army; `:159` keeps or swaps to the draft and grants 20 army XP if the draft already exists. Native law modifiers at `common/ideas/AA_law_military_ideas.txt:932` and `:1194` are much larger than the individual focus deltas:

| Native law | Volunteer army | Draft army |
| --- | --- | --- |
| Base conscription | 2.5% | 5% |
| Army organisation and morale | +10% each | -10% each |
| Attack and defence | No direct penalty | -20% each, offset by +20% each on cores |
| Personnel cost | +80% | No law modifier |
| Daily army/navy/air XP | 0.06 / 0.03 / 0.03 | 0.02 / 0.01 / 0.01 |
| Total workforce | -2.5% | -4% |
| Additional trade-off | Quality and payroll | General training time -20%, migration -10% |

The country starts with the draft. Moving to volunteers therefore already trades manpower/payroll for considerable quality and XP improvements. Do not label one route strictly dominated by comparing only its small US dynamic-variable helpers. Do not add another equivalent quality bonus without accounting for the law. Law-specific modifiers, subtype training-time modifiers and recruitable-population factor must not be added as though they were the same quantity.

## Stacking and cap risks before raising rewards

1. The US bridge (`mdcw_1970_USA_native_api_bridge.txt`) adds each `temp_change` to persistent policy variables and forces the native modifier update. These are cumulative deltas, not replacements. Multiple decades of compatible legislation, decisions and treaties can coexist.
2. Starting penalties are already large. For example army attack begins at -5% in the US army department, and an unresolved Vietnam burden has a separate -4% army-attack modifier. The direct +1-point AirLand Battle improvement does not resolve these. The volunteer law removes the separate draft penalty, which must be evaluated distinctly.
3. Stability and faction opinion can reach native caps. The reviewed faction helpers explicitly clamp opinion to 0-100 (`00_internal_faction_effects.txt:1102`, `:1410`, `:1549`). Economic regulation is clamped to 0-100 (`99_USA_main_scripted_effects.txt:382`) and Wall Street strength to 0-50 (`:371`). Another nominal improvement may then have no marginal effect.
4. Building capacity can swallow grants or place them in states no longer controlled by the US. Matching shared slots alone does not override a building's native level ceiling.
5. Generic research speed has 18 direct focus sources plus accepted Moscow summit at `USA_1970_nixon_diplomacy_events.txt:267`. Limited-use sector bonuses should replace overlapping existing speed bonuses where appropriate.
6. Native member spirits, laws, decision profiles, internal factions, election modules and future treaty spirits need whole-route evaluation. There is no support for a universal new +attack percentage or arbitrary global treaty cap from this audit.

Recommended priority: fix transaction and preview foundations; improve the most arbitrary forks; replace repetitive signature rewards with distinct institutions and limited-use sector rewards; expand partner-owned agreements and their concrete follow-ups. Preserve the existing difficult start and consent already implemented.

## Evidence limits

This audit inspected source and a parsed inventory. It did not launch HOI4, observe focus hovers, execute saves, measure engine timings or conduct multiplayer replay tests. Historical justification and upstream mechanical comparisons are supplied by the main design review. Inventory coordinates resolve declared relative anchors; the record does not evaluate every conditional camera/branch state or prove native connector routing. No runtime implementation or unrequested repository-wide cleanup was performed.
