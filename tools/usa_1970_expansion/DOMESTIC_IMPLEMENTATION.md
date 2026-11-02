IMPERIA COLD WAR: USA domestic programme integration

Implemented from the approved `docs/design/usa_1970_expansion_20261024/proposal.json`: 49 non-offer focus rewards, consisting of 13 replacements and 36 new focuses. This module owns only the six `COLDWAR_USA_1970_programmes` runtime files, `domestic.py`, its generated integration specs and its source/model regression checks. The coordinator owns the live focus tree, original focus localisation, history, money integration and on_actions.

Run `python tools/usa_1970_expansion/domestic.py` to regenerate owned files. Imports have no emission side effects. `domestic_focus_specs.json` supplies a `focuses` list keyed by each item's `id`. Each item includes `available`, complete `completion_reward`, native icon, native focus cost, English name/description, programme idea IDs, exact party trigger and completion/preview/apply helper names. Original 13 focus names/descriptions are supplied only in the specs, so the coordinator can update their canonical original localisation without duplicates. The new 36 focus texts are emitted in the owned localisation file.

## Lifecycle hooks

| Hook | Coordinator call site |
| --- | --- |
| `COLDWAR_USA_dom_initialize` | Initial scenario setup and old-save initialization. Its one-time flag prevents migration replay; it then reconciles active spirits. |
| `COLDWAR_USA_dom_reconcile` | Weekly USA update and actual governing-party/law changes. Applies only the highest earned programme tier. Never charges money or grants buildings, research coupons or XP. |
| `COLDWAR_USA_dom_recalculate_weekly_expense` | Recompute the nuclear programme contribution. Resets `COLDWAR_USA_domestic_weekly_expense` to zero, then assigns 0.03 when a Standard Reactor Programme tier is actually active. |
| `COLDWAR_USA_dom_add_expense_rate` | Call exactly once inside the native additional-expense consumer, after its accumulator reset. Recalculates and appends `COLDWAR_USA_domestic_weekly_expense` to `additional_expenses_rate`. |

The reactor idea's concrete numeric expense row describes that same weekly contribution. The display does not charge the Treasury by itself. Fiscal integration must connect the final hook to the real native rate consumer.

## Programme ownership and transactions

There are 27 programme families with 48 static cumulative tiers, plus the temporary Retrofit Adjustment and Export Credit Guarantees ideas. Continuations replace the family tier rather than adding a second programme copy. Party programmes require the actual native Democratic slot-2 or Republican slot-1 trigger in focus availability, execution and reconciliation. Branch visibility is unaffected. Earned factories, infrastructure, offices, research coupons and XP survive a party change; the party's ongoing spirit deactivates and restores without repeating those gains.

Professional Force Establishment operates only with the actual Volunteer Army law. National Service Establishment operates only with the Draft Army law and without the incompatible all-volunteer doctrine. D1/D2 use the existing native law-changing helpers, so the real full law transition is present in the native preview and execution. D2's doctrine incompatibility is an additional visible and executed native constraint. All original 13 availability predicates from the frozen inventory are also rechecked during execution: this preserves Congress thresholds, force-model choices and the dated transition rule.

Domestic focus payments deliberately follow the approved native MD deficit convention: no new Treasury affordability prerequisite. Setup benefits are guarded by the original USA identity, scenario, a pending entitlement, exact party where applicable, prerequisites, exclusions, programme parent, capacity and a one-time completion receipt. If requirements change during focus completion, the whole transaction remains pending without payment or assets. A normal national enactment decision lets the player apply the approved package once its requirements recover. Reconciliation does not silently enact a pending package.

Building transactions select an owned, controlled US core state. Industrial grants use actual Great Lakes states 771/775/777/778; market investment uses actual metropolitan states 769/770/778/800/809/811. Other domestic grants may use eligible US core states. Every grant checks both a building's native level ceiling and currently usable space. It grants one extra shared slot per building level before native construction, inside the same once-only transaction. Infrastructure is included. Direct construction has no hidden building-price helper, so the approved focus payment is the sole setup debit.

Capacity guards compare the documented state dynamic variable `building_level@<type>` with `native maximum - granted quantity`, using `check_variable` and `compare = less_than_or_equals`. Installed native documentation providers are `dynamic_variables_documentation.md:1101-1102` and `triggers_documentation.md:2110-2125`. The native load rejected the earlier superficially plausible `has_building` trigger; that form is removed from both source and model and banned by the integration validator. Boundary tests retain the actual two-level factory and infrastructure ceilings, independent of surplus shared slots.

The native `free_building_slots` predicate receives `include_locked = no` only when the loaded building definition has `level_cap.shares_slots = yes`. Independent infrastructure and energy buildings omit that parameter, as required by `triggers_documentation.md:2901-2913`. User screenshots exposed the former indiscriminate use. The model now rejects this invalid combination; the Industrial Energy Audits regression verifies a two-level infrastructure grant without free shared slots. All matching extra-slot grants remain.

## Native providers and units

All emitted modifier keys were checked against non-owned existing MD idea/dynamic-modifier/custom-definition providers. Important exact mappings include:

- Production growth: `production_factory_efficiency_gain_factor`; retention: `line_change_production_efficiency_factor`; cap: `production_factory_max_efficiency_factor`.
- Research: `research_speed_factor`. Coupons use actual populated technology categories `CAT_industry`, `CAT_electronics`, `CAT_nuclear_reactors`, `CAT_aircraft`, `CAT_destroyers` and `CAT_submarines`. Nuclear coupons apply to reactor development, not nuclear weapons. The mixed two-coupon aircraft/electronics and destroyer/submarine rewards give one coupon to each listed sector. No ahead-of-time reduction or free technology is granted.
- Doctrine coupons use native `add_doctrine_cost_reduction`, `cost_reduction = 0.5`, bounded `uses` and `land_doctrine`/`air_doctrine`/`naval_doctrine`, following the real German and Australian focus providers.
- Army and naval experience percentage bonuses use `experience_gain_army_factor` and `experience_gain_navy_factor`. They are distinct from flat `experience_gain_army` daily XP and one-time `army_experience`/`air_experience` rewards.
- Organisation regain uses native `army_morale_factor`; naval organisation uses `navy_org_factor`; submarine detection uses `navy_submarine_detection_factor`; army training uses `training_time_army_factor`.
- Tax, education, personnel, equipment and bureaucracy modifiers are the registered existing MD money modifiers consumed by `00_money_system.txt`. Naval personnel cost uses `navy_personnel_cost_multiplier_modifier`, read by the real naval payroll calculation at the inspected lines 3209-3219. No invented naval equipment-expense modifier is used.
- Energy demand uses `energy_use_multiplier`; nuclear generation uses `nuclear_energy_generation_modifier`. The actual energy effects read these as multipliers. The reactor programme also uses the existing reactor-construction-speed modifier.
- Native US institutional idea art is reused through registered `USA_interiori`, `USA_energyi`, `USA_armyi`, `USA_navyi`, `USA_capitol_building`, `department_of_defense` and `research_bonus` pictures. The research image resolves to the actual 60 x 68 idea asset `gfx/interface/ideas/research/research_bonus.dds`; a similarly named focus-medallion alias was rejected during independent review. No art was copied, transformed or claimed as newly owned.

The Export Credit Guarantees decision completes the approved node's unlock with the coordinator-approved implementation detail: 75 PP and $5 setup, 180 days of export income +5% and tax collection efficiency -1%, with a 365-day re-enable interval. This decision alone has an exact $5 funding requirement and execution recheck. A stale failed authorization refunds its native 75 PP charge. It produces no buildings, research or XP.

## Old-save migration

The initialize helper recognizes completed old focus IDs before the new transaction receipt exists. It reverses 42 exact unbounded persistent US policy-variable deltas across the 13 replaced reward blocks and assigns the corresponding earned base programme. It then sets `COLDWAR_USA_domestic_v1_initialized`. Newly completed rewards set their own receipt immediately and therefore cannot be misidentified as old rewards.

Historic setup payments, PP, stability/war-support changes, buildings, coupons and XP are not replayed or refunded. Random Congress outcomes and capped faction/regulation history cannot be reconstructed exactly from an aggregate save value, so this module does not attempt an invented reversal. The migration report lists every reversed variable and amount in `domestic_focus_specs.json`. Law state and previously earned institutional receipts are preserved. Subsequent initialization calls only reconcile the ongoing programme tier.

## Verification

`python tools/usa_1970_expansion/test_domestic.py` passed 15 focused source/model tests. Coverage includes all 49 completion transactions and repeat calls, side-effect-free effect previews, wrong-country rejection, lost control during completion and recovery, native capacity despite surplus slots, independent infrastructure capacity with zero free shared slots, retained industry slot checks, party departure/return without repeated assets, actual military-law activation, all-volunteer incompatibility, retained Congress/force-model guards, deliberate focus deficit payments, exact decision funding, migration idempotence and reset/recomputed weekly expense contributions. All generated files parse; script encodings/markers and BOM localisation are checked; native icons, idea pictures, modifier names and populated research categories resolve against existing sources.

These checks execute a bounded model of the emitted script. They do not prove HOI4 tooltip rendering, engine API behavior, weekly Treasury timing or multiplayer/save synchronization. Native playthrough and rehost checks remain distinct validation work for the integrated tree.
