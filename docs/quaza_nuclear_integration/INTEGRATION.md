# Uranium and nuclear infrastructure integration

Integrated from **Feature Test quaZa**, Workshop **3818306694**, into **MD Cold War**, using installed main Millennium Dawn **2.0.2** as the comparison ancestor. Existing Cold War changes were retained through reviewed merges. Donor files were not copied wholesale over the economy, buildings, equipment or national trees.

## Implemented mechanics

| Area | Result in Cold War |
| --- | --- |
| Resource | Uranium is resource 9. Existing resource IDs remain in their original order. |
| Mining | Constructible state mines on surveyed deposits. Deposit capacity permits 1–3 levels; reserved capacity blocks construction elsewhere. |
| Mine cost | 32,000 construction cost, increasing by 4,000 per existing level. International investment costs $6 billion per level. |
| Running costs | Base mine power demand 0.25 GW and base infrastructure maintenance $0.022 billion weekly, subject to existing MD cost modifiers. |
| Production | Zero starting production. Surveyed deposits produce nothing until paid mine development is completed. Each working mine level supplies 3–12 units; damage, removal and repeated recalculation do not generate duplicate resources. |
| Labour | Uranium contributes to resource-sector labour demand and its workforce fulfillment modifiers. |
| Enrichment | Each facility consumes 25 natural Uranium. Shortages proportionally reduce new nuclear-fuel production. No uranium means no new fuel production. Existing fuel and strategic-resource stocks still work normally. |
| Nuclear projects | Atomic weapons and warhead programmes require three working enrichment facilities to start. Existing projects remain registered if facilities are lost; the weekly disruption check imposes a 90% special-project speed penalty until capacity returns. |
| Weapons development budgets | Atomic bomb research: approximately $0.154 billion/week base; warhead programme: approximately $0.096 billion/week base. Both enter the native weekly Defence Budget, adjusted by GDP per capita and inflation. |
| Project resources | Nuclear energy: 2 Uranium; thorium project: 1; atomic bomb: 4; warhead programme: 4; naval nuclear engineering: 2; nuclear torpedoes: 1. Existing other project costs are preserved. |
| Equipment | Nuclear missile archetypes and relevant naval reactor/torpedo modules consume Uranium. Existing Cold War equipment costs, ranges and classifications are retained. |
| Trade | Uranium imports/exports, export revenue, labour effects and a supply/demand price between 0.04 and 1.00. Initial price 0.20. These are MD monetary units, not quoted historical commodity prices. |
| Reserves | Uranium can be stored and withdrawn through the existing strategic-resource reserve interface and game rule. |
| Investments | Mine construction through the investment system, checked when selecting, accepting and delivering an investment. Existing Imperia recipient bonuses and all previous investment prices remain. |
| Interface | Nine-resource trade/production presentation, economy price display, configurable topbar values, reserve controls, investment controls and a Uranium Deposits map mode. |
| Artwork | Donor resource, deposit, map-mode, topbar and enrichment-raid assets are included. The existing shelter icon remains frame 39; Uranium uses a new frame 40. |
| AI economy | Mining responds to economic demand and deposit limits. Nuclear construction considers threats and nuclear umbrellas. Civilian reactor fuel production is not blocked by the weapons-programme policy. |

## Raids: mandatory human-only policy

**All 50 loaded raid definitions, across all eight non-empty raid files, have `is_ai = no` as their first preparation and launch condition.** The actual native fields are `available` and `launchable`. This applies to air, carrier, cruise missile, drone, infiltration, naval, nuclear and special-forces raids. No scripted force-launch effects were found in the installed country events or effects.

Donor raid improvements are retained for human players: peacetime strike eligibility and the enrichment-facility strike target fix. Enrichment facilities are targeted through their state because the building has no map position. Alliance, subject, non-aggression and political-power conditions remain where applicable. Donor raid AI scoring does not override the human-only guards.

## 1970 adaptation

- All states start with **zero raw Uranium and no uranium mines**, as requested. The former automatic production entries in 34 state histories are zeroed in history, not removed by a startup override.
- The 1970 profile contains 57 sourced development districts known before 1 January 1970. Nebraska is removed, later discoveries do not inflate starting capacity, and the northern Kazakh district is mapped to state 714. Country ownership and all other state resources remain unchanged. A surveyed deposit grants construction capacity rather than free production. See [the geological audit](URANIUM_1970.md) and [dated source register](uranium_1970_research.json).
- The zero-production start is the requested development rule, not a claim that historical uranium mining did not exist. The historical sources below inform district selection; deposit capacities remain explicit gameplay estimates.
- Wismut production is represented in Saxony and Thuringia. The exhausted German reserves of a modern scenario are not used as the Cold War starting industry.
- Namibia, Niger and later Australian developments, like every other district, require paid development before producing Uranium.
- The modern Red Book reserve table is not used to populate the 1970 surveyed-district profile.
- The donor's permanent 45% output without uranium, justified by post-Cold-War secondary supplies, is removed. Strategic stocks must actually exist.
- The zero-production start and initial deposit/investment setup require a **new campaign**. Existing campaigns retain their saved state resources; the startup initializer is not a general save-load migration.

## Corrections and intentionally excluded donor changes

- Uranium for nuclear torpedo research is attached to `sp_nuclear_torpedoes`. In the donor, it was attached to the conventional anti-torpedo project.
- The nuclear-state predicate is supplied locally rather than depending on an unrelated donor shelter-AI file.
- Removed the invalid `include_locked` parameter from the state-building enrichment construction check after native-engine validation.
- Working mine output uses `non_damaged_building_level@uranium_mine`, so bombing has an actual economic effect.
- Added current controlled enrichment-capacity recounting before the weekly programme-disruption check.
- Preserved existing investment prices, Imperia segment rewards, shelter mechanics, power-plant balance, equipment balance, focus trees and technological cutoffs.
- Did not import unrelated donor agriculture/disaster systems, modern country content, the modern Burevestnik variant or the separate generation-weighted arsenal-upkeep model. The specifically approved weapons-research budgets are included separately.

## Cost and performance audit

The cost chain is connected to actual weekly finances, rather than a tooltip-only amount:

- Mine maintenance enters `infra_gain`, then total expenditure and the weekly treasury balance. Its $0.022 billion/level base is adjusted by the infrastructure modifier, the existing GDP/c and inflation multiplier, and native population-size scaling.
- Mine investments retain the $6 billion/level base, existing investment adjustments and an additional 4,000 IC per existing level when calculating construction duration.
- Enrichment costs 45,000 IC per facility and requires 25 natural Uranium per facility. There is no new standalone cash operating fee for enrichment; the existing reactor maintenance charge remains in infrastructure spending.
- Weapons research uses `weekly_base × clamp(GDP/c in thousands / 36, 0.4, 1.2) × inflation_multiplier`. Weekly base rates are $0.15384 billion for the bomb and $0.09615 billion for warheads; player-facing base amounts use the native budget display precision. These match the previous native baseline within the engine's five-place fixed-point precision. Before inflation, weekly costs range from approximately $61.54–184.61 million and $38.46–115.38 million respectively. Scripted budget literals use at most five fractional digits: a native probe confirmed that longer literals are misread by the engine.
- Research costs apply while the actual project is active, including during disruption. Completion or cancellation clears the expense on the next normal economic refresh. Existing warheads do not exempt further research from its budget.
- Refreshing the economy recalculates a rate; it never directly debits the treasury. The normal weekly MD accounting performs payment once. The Defence Budget breakdown and both project descriptions show the expense.

The additional integration no longer scans the world's states daily. Its two weekly mine passes were combined, the unused country output cache was removed, and the extra enrichment recount is restricted to active or disrupted weapons programmes. AI mine searches require a country with deposits and retain the economic eligibility checks and 90-day build cooldown. Nuclear AI policy/construction runs monthly; the uranium market price uses the existing once-per-month global price update. Research-budget calculation adds no state or country loops.

The saved scripts contain **11 equivalent unconditional state passes per week before optimization and 1 afterward**, plus the necessary conditional recounts. This is a structural count of the additional integration, excluding native MD accounting and conditional AI searches. The report's 13,761 versus 1,251 map-size visit figures are upper bounds using the 1,251 state files; they are not measured simulation work, a total game-load reduction, or an FPS benchmark. A long multiplayer performance test remains outside this check.

## Verification

`python tools/quaza_nuclear_integration/test_integration.py`

**21 tests passed**, including actual imported script arithmetic, zero/partial/full uranium supply, mine damage/repair, resource conservation, deposit loss, output rebalancing, all 50 raid guards, existing investment prices, project costs, icon-frame preservation, interface spacing, duplicate definitions, UTF-8 encoding and brace structure. The checks cover development-budget scaling, repeated refreshes, completion/cancellation reset, native financial aggregation, mine upkeep and bounded weekly work. Additional coverage compares the complete affected Uranium GUI geometry with the current donor, verifies core donor effect/trigger definitions and artwork, and checks all state histories for free starting uranium or mines. The latest checks also verify the dated geological register, its generated capacities, the capacity-based map legend and non-overlapping project-card rows with a locally registered native bomb icon.

The latest native verification is **incomplete** and predates the new geological profile and project-card correction. The first zero-production run reached scenario startup, then the engine failed with an access violation and `Invalid rehash requested for CPdxRobinHoodTable`. No Uranium-specific parser error was reported. A global Space Race ranking call without a country context was identified and guarded in both its runtime hook and generator; that correction has not yet been confirmed by a completed native run.

The follow-up interactive test was stopped after the user cancelled Computer Use with the physical Escape key. The task-owned game process was closed. The corrected trade screen has therefore **not been visually verified**, and a successful full startup after these coverage changes remains unconfirmed. `engine_report.json` records the interrupted run; `engine_report_coverage_first_startup.json` records the first failure. Earlier successful mine/accounting results predate the zero-production change and must not be presented as verification of the current build.

The 21 passing script tests cover the current source and donor geometry, not a completed native campaign or multiplayer test. A fresh campaign is required to exercise the zero-production state histories. Existing unrelated errors elsewhere in the mod were not treated as fixes delivered by this integration.

## Full UI coverage correction

The initial keyword-filtered import omitted adjacent layout hunks that contained no Uranium identifier. A wider parent container alone did not remove the trade grid's eight-slot limit. The current review compares complete functional blocks against the installed donor:

- Trade resource totals: exact donor 691×200 background, nine slots, 67-pixel columns, 603-pixel grid width; the Uranium balance, extraction, imports, exports, projects, production, surplus and cancellation control can occupy the ninth column.
- Trade filters: scaled button artwork and centered icons match the nine-tab layout.
- Production resource strip: 57-pixel entries fit the 58-pixel slots; icon/text placement and the obsolete overlapping click overlay are corrected.
- Market prices: all nine items use 74-pixel spacing; the former eight-resource positions overlapped the new Uranium item.
- State buildings: the complete extra row and associated lower-panel positions are adopted, exposing the additional state building.
- Resource concessions: uranium-only states and Uranium concessions are recognized by the existing Imperia request/cancel/reclaim controls.

Construction costs, upkeep, power use, employment, enrichment demand, project/equipment inputs, reserve handling, investments, export revenue, price updates, topbar choices, deposit map mode and human-only raid guards remain part of the verified integration. The comment-only donor `imp_uranium_ai.txt` contains no missing AI definitions; mine AI is implemented in the imported scripted effects. Modern national-tree stories and the pre-existing approved Cold War nuclear strike balance are not replaced by a wholesale donor copy. `raid_current_donor_coverage.json` records those raid differences explicitly rather than treating the presence of a file as proof of equivalence.

See `cost_audit.json`, `performance_report.json`, `engine_report.json`, `engine_modified_files_errors.json`, `coldwar_balance.json`, `raid_policy.json` and `manifest.json` for the exact results and touched-file hashes. `report_costs_and_performance.py` refreshes audit reports without modifying runtime code. The port scripts retain the comparison/merge record; the installed runtime files and tests are authoritative. Do not rerun the initial one-time import or performance-migration scripts over later edits.

## Historical references

- [British Geological Survey: Statistical Summary 1966–1970](https://nora.nerc.ac.uk/id/eprint/535264/), p.375; source table checked visually and against extracted text. The year columns distinguish long tons and metric tonnes.
- [Wismut: company history](https://www.wismut.de/geschichte), including its 1967 peak and later production restrictions.
- [Rössing: operating history](https://www.rossing.com/our-operations/), production beginning in 1976.
- [IAEA: Nuclear Technology Review 2006](https://www.iaea.org/sites/default/files/gc/gc50inf-3_en.pdf), historical distinction between primary production and later secondary supplies.

Donor implementation credit: quaZa, Workshop 3818306694. Imported function IDs retain their IMP names for dependency compatibility; added files use `COLDWAR_quaza_` names and custom-code markers.
