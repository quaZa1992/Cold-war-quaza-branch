# Cyprus 1970 effects and rewards review

Design audit only. No runtime files changed. References use repository-relative paths unless prefixed `MD:`. `MD:` means `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/`.

**Current candidate: 295 focuses, six deep political routes, 39 Turkish Cypriot focuses and22 road-to-war focuses; nine starting spirits plus two crisis-only definitions. The final273-focus six-route numerical rerun passed all requested permanent ceilings; the added crisis branch grants no permanent positive organization, research or construction bonus. Earlier328/330 counts and pre-trim numerical findings are historical records. See final295-focus addendum below and WAR_MECHANICS.md for the crisis audit.**

## Findings that constrain the design

- Cyprus owns and controls states **145 and 146** in the authored January 1970 blocks. State 146's undated `owner = NCY` is overridden. State **812 remains British**. Do not start an independent Northern Cyprus, a 1974 invasion, or postwar property settlement in January 1970. See `history/states/145-Cyprus.txt`, `146-Northern Cyprus.txt`, `812-Cyprus British Territory.txt`.
- `history/countries/CYP - Cyprus.txt:5` starts Makarios III, `ideology = conservatism`, via `IMP_1970_profile_democratic_conservative`; the MD ruling subparty index is **1**. Generic later-century CYP advisors and leaders are not automatically appropriate for 1970.
- `treasury`, `debt`, `gdp_total` are **billions**; GDP per capita is **thousands**. See `localisation/english/MD_money_l_english.yml:11`, `:16`, `:25`. `treasury_change = -1` therefore costs one billion, not one million.
- The visible authored starting population is about 635,446 in the two CYP states before engine growth/recalculation, and authored GDP/capita is 1.010. This suggests roughly 0.642 billion as a scale illustration, **not a verified in-game budget/GDP result**. GDP, workforce, revenue, employment and currency calculation must be inspected after scenario initialization before any building grants are approved for runtime.
- Latest MD generic and Russia are useful syntax/style references, not absolute reward budgets for Cyprus. Russia spends single/double digit billions. A copied major-power factory helper can bankrupt Cyprus.

## MD reward and cost idioms

`MD:common/national_focus/00_generic.txt:61` uses `cost = 8.6`, with +200 political power at line 67. Its service-announcement focus grants +0.05 stability and +0.05 war support at lines 180–181. Political spirits in local `common/ideas/generic_ideas.txt:87` give +0.10 / +0.20 political power factor. Several economic generic foci cost `7.86`; others cost `5` or `10`. Follow the regional pattern, not a uniform 70-day template.

The generic uses a GDP fraction for fiscal policies: `treasury_change = { value = gdp_total multiply = -0.015 }` at line 245, `-0.005` at line 623, `-0.03` at line 2153. The local Cold War generic already uses comparable fractions (`common/national_focus/mdcw_1970_generic_focus.txt:335`, `:1364`).

```text
set_temp_variable = { treasury_change = { value = gdp_total multiply = -0.005 } }
modify_treasury_effect = yes
```

`modify_treasury_effect` exists at `common/scripted_effects/00_budget_effects.txt:1487`: it updates treasury and dirty money state and displays the standard tooltip. It does **not** perform an affordability check. Define a focus's affordability trigger and its behavior if GDP/cash changes while it is running. Do not silently mint a free project or fall through to a different building when unavailable.

Recommended Cyprus design ranges: minor administration project **0.25–0.5% GDP**; education/policing reform **0.5–1% GDP**; exceptional reconstruction **1–2% GDP**; grants **0.5–1.5% GDP** only when a partner accepts and pays. A state-project construction cost is distinct from a GDP-relative administrative subsidy. A tiny GDP fraction does not plausibly pay for an instant modern factory.

`modify_debt_effect` at `00_budget_effects.txt:1501` requires `debt_change`. Borrowing must create both money and debt via the appropriate helpers; setting treasury alone does not constitute a loan. Tax helpers require `corp_change` or `pop_change` (percentage **points**, e.g. `-1`) and live at `:1553`, `:1590`.

### Building helper traps

| Existing helper | Hidden cost / extra output | Source |
|---|---|---|
| `one_random_arms_factory = yes` | Adds a slot and instant military factory; charges **7.5 billion**, unless `skip_payment = 1` | `common/scripted_effects/00_scripted_effects.txt:4` |
| `one_random_industrial_complex = yes` | Adds a slot and instant civilian factory; charges **7.5 billion**, unless skipped | same file `:223` |
| `one_office_construction = yes` | Adds a slot, an office **and fossil plant**; charges **12 billion**, unless skipped | same file `:706` |

Do not double-charge those helpers. Do not casually use a global skip-payment switch to make factories free. For Cyprus prefer production, tax, workforce and infrastructure improvements; at most one rare, expressly funded/staffed civilian or military workshop project per chosen route. Any direct `add_building_construction` needs ownership, control, workforce, slot and cap guards; province buildings also need correct province IDs. Use `can_staff_an_industrial_complex`, `can_staff_an_arms_industry`, `can_staff_an_offices`, defined at `common/scripted_triggers/00_economic_triggers.txt:449–459`. These compare available unemployment and building workers, both in thousands.

## Verified modifier whitelist and units

Suggested values below are balance proposals, **not inherited game constants**. They describe a single relevant spirit or programme, not a reward every focus should add permanently.

| Country modifier | Typical Cyprus magnitude | Verified source |
|---|---:|---|
| `stability_factor` | ±0.02–0.08 | `common/ideas/05_cyprus.txt:7` |
| `political_power_factor` | ±0.03–0.10 | `common/ideas/generic_ideas.txt:91` |
| `production_speed_buildings_factor` | ±0.03–0.08 | generic ideas `:202`, `05_cyprus.txt:27` |
| `army_org_factor` | ±0.03–0.05 | generic ideas `:647` |
| `max_planning` | ±0.03–0.05 | `common/ideas/05_china.txt:292`, `:770` |
| `army_defence_factor` | +0.03–0.05 | generic ideas `:670` |
| `army_attack_factor` | +0.03–0.05 | generic ideas `:509` |
| `research_speed_factor` | ±0.01–0.03 | `common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt:17` |
| `tax_gain_multiplier_modifier` | ±0.02–0.05 | `common/modifier_definitions/money_modifier_definitions.txt:2` |
| `corporate_tax_income_multiplier_modifier` | ±0.03–0.05 | `common/ideas/05_cyprus.txt:36` |
| `office_park_income_tax_modifier` | +0.03–0.08 | `common/ideas/05_cyprus.txt:46` |
| `bureaucracy_cost_multiplier_modifier` | ±0.05–0.10 | money modifier definitions `:50` |
| `police_cost_multiplier_modifier` | ±0.05–0.10 | money modifier definitions `:57` |
| `education_cost_multiplier_modifier` | +0.05–0.10 | money modifier definitions `:64` |
| `social_cost_multiplier_modifier` | ±0.05–0.10 | money modifier definitions `:106` |
| `interest_rate_multiplier_modifier` | ±0.25–0.50 **interest points** | money modifier definitions `:9` (`value_type = number`) |
| `productivity_growth_modifier` | +0.02–0.04 **base-growth units** | money modifier definitions `:410`, `00_productivity_effects.txt:75` |
| `country_productivity_growth_modifier` | ±0.03–0.08 growth multiplier | money modifier definitions `:515` |
| `foreign_influence_defense_modifier` | ±0.03–0.08 | `common/modifier_definitions/influence_modifier_definitions.txt:1` |
| `imp_refugee_integration_rate` | +0.10–0.25 | `common/modifier_definitions/mdcw_imperia_idea_dependency_modifiers.txt:14` |

Never label `productivity_growth_modifier = 0.03` as “GDP +3%” or immediately raise `overall_productivity`. The local growth algorithm takes that additive base, multiplies by 0.5 and by a clamped `country_productivity_growth_modifier`, then applies state catch-up and growth modifiers. See `common/scripted_effects/00_productivity_effects.txt:31–86`. `country_productivity_growth_modifier` only scales positive growth and cannot make it negative by itself.

Verified state keys:

- `state_production_speed_buildings_factor`: use **-0.05** in 145 and **-0.08** in 146 for restricted movement/security disruption, if that geographic approximation is explicitly explained. Verified `common/dynamic_modifiers/00_raid_dynamic_modifiers.txt:106`.
- `state_productivity_growth_modifier`: optional **-0.05 / -0.08** multiplier of positive growth; definition `money_modifier_definitions.txt:508`, consumption `00_productivity_effects.txt:50`. This is not a direct GDP/output loss.
- `local_building_slots_factor` exists (`common/dynamic_modifiers/00_global_reaction_modifiers.txt:14`) but is **not recommended** for Cyprus; tiny slot counts can round awkwardly and the political conflict should not erase physical geographic space.

Country and state modifiers are not interchangeable. New Cyprus dynamic-modifier IDs and their variables will still need definitions. “Exists in MD” validates modifier keys, not a newly invented spirit ID or scripted helper.

## Research and education

Use `add_tech_bonus`, not an invented research helper:

```text
add_tech_bonus = {
    name = coldwar_CYP_infantry_school
    uses = 1
    bonus = 0.25
    category = CAT_small_arms
}
```

`MD:common/national_focus/00_generic.txt:6045` uses this category with two 50% uses; one 25% use is a more appropriate Cyprus baseline. Verified 1970-appropriate category IDs in `common/technology_tags/00_technology.txt`: `CAT_small_arms` (12), `CAT_utility_vehicles` (14), `CAT_night_vision` (15), `CAT_command_and_control_equipment` (18), `CAT_towed_artillery` (43), `CAT_anti_air` (50), `CAT_industry` (183), `CAT_construction` (194). Categories are technologically broad; a category bonus alone does not prevent a player applying it to far-future research. Avoid ahead-of-time reductions and research slots in the initial design.

Literacy has a real API: `set_temp_variable = { LR_change = 0.01 }` followed by `update_literacy_rate = yes`; definition `common/scripted_effects/00_education_effects.txt:166`, example `common/national_focus/COLDWAR_EGY_1970_focus.txt:3960`. Guard remaining headroom, and use modest 1 percentage-point increments rather than directly changing research slots. Check Cyprus's initialized literacy before promising the reward.

## Party gates and programme lifecycle

Use exact native subparty triggers from `common/scripted_triggers/01_political_triggers.txt`: `western_conservatism_are_in_power` (176), `western_liberals_are_in_power` (183), `western_social_democrats_are_in_power` (190), `emerging_communist_state_are_in_power` (197), and their 20 other equivalents. `has_government = democratic` alone does not distinguish the four Western parties.

The existing generic already implements persistent-unlock, current-government-only programmes in `common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt:23`:

```text
GEN_1970_con_programme = {
    icon = GFX_idea_democracy
    enable = {
        IMP_is_1970_scenario = yes
        western_conservatism_are_in_power = yes
    }
    stability_factor = GEN_1970_con_stability_factor
    political_power_factor = GEN_1970_con_political_power_factor
    # further defined variables
}
```

Replicate this lifecycle under `coldwar_CYP_` IDs. Policy modifiers earned under one government become dormant when that party leaves office and return when it returns; built infrastructure and diplomatic commitments persist. Mutually exclusive choices should be irreversible on the first design, with any later repeal carrying an explicit cost/event. Prevent permanent stacking by touring all 24 parties. Same outlook-specific trigger on every party focus; branch root does not suffice.

Native popularity: `party_index`, `party_popularity_increase` (fraction, 0.02 = 2 percentage points), optional `temp_outlook_increase`, then `change_relative_party_popularity = yes`. Definition `common/scripted_effects/00_MD_politicsview_scripted_effects.txt:267`. Never use 2 as a 2% party boost. A government-specific boost can remain around 0.01–0.025, similar to `MD:common/national_focus/05_russia.txt:1491–1500`.

## Proposed start and meaningful choices

| New coldwar_CYP spirit | Proposed starting values | Narrative cause and relief |
|---|---|---|
| `constitutional_breakdown` | stability -0.08; PP factor -0.10 | Disputed operation of the 1960 power-sharing constitution, absent shared institutions and armed communal separation; restore institutions or impose costly central authority. No ethnicity is inherently detrimental. |
| `fragmented_security` | army organization -0.05; max planning -0.05 | Rival armed networks, foreign command influence and civilian/military disagreement; professionalize, negotiate disarmament, or empower factions at coup/escalation risk. |
| `narrow_island_economy` | construction speed -0.05 | Small capital base, trade sensitivity and uneven development; phased infrastructure and skills reforms. Avoid claiming a prosperous 1970 economy was already a postwar ruin. |
| state `restricted_movement` | state145 construction -0.05; state146 -0.08 | Enclave restrictions and insecurity, geographically approximated in the two-state map; both communities have costs. Does not rename the northern state a separate polity. |

National negative stability modifiers are flat points, not the same presentation as one-time `add_stability`. Budget starting and final totals together with existing laws and Imperia development spirits. No extra generic `CYP_division_of_the_island` in 1970; its later-date setup has a different historical context.

Useful in-tree mutually exclusive choices (each chosen pair may later reconnect):

| Choice | Route A | Route B |
|---|---|---|
| Territorial administration | Shared municipal commissions: stability +0.03, bureaucracy cost +0.05, gradual state restriction relief | Central commissioners: PP factor +0.05, tax yield +0.02, police cost +0.10, restrictions remain until a later settlement |
| Development | Tourism/service upgrade: office tax +0.05, foreign influence defense -0.03, vulnerability expressed through crisis events | Productive cooperatives: base productivity growth +0.02, construction +0.03, initial 1% GDP reform cost |
| Education | Technical institutes: one 25% construction bonus and base growth +0.02; education cost +0.05 | Scholarships abroad: one 25% relevant bonus, research +0.01; explicit partner acceptance and no free slot |
| Defence | Professional guard: organization +0.05, personnel or police expense premium using verified key | Reserve territorial force: defence +0.05 and planning +0.03, slower training/less expeditionary utility only when an actual verified modifier is selected |
| Sovereignty | Nonalignment and mediation: influence defense +0.05, modest stability, no automatic guarantee | Foreign training mission: one 25% military research bonus, dependency/influence concession and partner consent |
| Emergency policing | Accountable intelligence: stability +0.02, police cost +0.05 | Emergency powers: PP factor +0.05 and temporary security gains, stability -0.03, escalation/abuse event exposure |

Do not force a permanent debuff onto every ordinary school, port or road. A fiscal cost, construction time, diplomatic obligation, route exclusion or foregone alternative can be sufficient tradeoff. Keep individual permanent rewards modest: ~25–75 PP, 2–3 stability points, one 25% bonus, 3–5% relevant spirit improvement. Cap a chosen party programme's contribution around 3–8 stability points, 5–10% construction/organization, 1–3% research and +0.02–0.06 base productivity growth, then separately assess shared-sector totals. These are review targets, not guaranteed balance.

## Imperia integration and historical violence

The local Imperia systems already calculate development status, interest and workforce pressure (`common/scripted_effects/mdcw_imperia_development_effects.txt`, `common/dynamic_modifiers/mdcw_imperia_development_dynamic_modifiers.txt`). Let focus modifiers feed those calculations rather than overwriting derived variables. Small-country safeguards already exist in development effects.

`imp_refugee_integration_rate` is genuinely consumed in `common/scripted_effects/imp_refugees_effects.txt:283`. Its +0.25 modifies integration speed, **not “25% of the population integrated”**. The refugee system otherwise models war-contested states: `imp_refugees_calc_refs` at line 6 moves fractions of population into casualty/refugee pools. It is not a safe all-purpose focus effect. Do not call its whole-country automatic calculator to simulate a single targeted historical incident or double-count generated refugees.

A later crisis can depict coups, attacks on civilians, displacement, intervention and property loss in plain historical language. Violent routes can bring short-term coercive control and diplomatic/security opportunities, but must retain concrete civilian losses, legitimacy damage, reduced workforce, refugee/housing costs, external reaction and renewed conflict. Do not make removing a minority a permanent tax/research/production optimization. Province/state-scale casualty numbers require separately researched historical bounds and population-conservation checks; do not invent mass casualty values from the modifier design.

Civilian shelters exist in `common/buildings/mdcw_imperia_shelters.txt`: base construction cost **15000**, extra per-level cost **15000**, cap 10, `local_supplies_for_controller = 0.02`. They interact with nuclear damage through `common/scripted_effects/mdcw_imperia_nuclear_effects.txt:15`. However, the current infrastructure upkeep at `common/scripted_effects/mdcw_imperia_infrastructure_effects.txt:55–62` is **0.008 billion/week intact**, **0.02 billion/week damaged**, per level before the multiplier. An intact shelter alone is roughly **0.416 billion/year**, enormous for 1970 Cyprus. Do not insert a free shelter focus just to mention Imperia features. Prefer a modest civil-defence training programme or reserve an actual shelter for a late, funded and affordability-tested project. Stronghold upkeep there is even higher at **0.05 billion/week**.

## Runtime acceptance checks for the later implementation

1. Load the actual January 1970 scenario and capture population, GDP, cash, debt, workforce, literacy, law modifiers and existing startup spirits.
2. Audit each chosen-route cumulative modifier total, not just single focuses. Check party-switch removal/reactivation and exclusivity.
3. Test costs only once, test unavailable/occupied/lost target states, fully occupied construction slots, and insufficient cash or workers. Province buildings must be placed in their correct state province.
4. Foreign grants/missions/union/guarantees need recipient and sponsor agency; a focus cannot force another multiplayer participant's money, land or diplomatic assent.
5. Keep 1970 enclave disruption separate from the later territorial partition and refugee consequences. Existing later-date Cyprus events must be gated away from incompatible new crisis state machines.
6. All IDs/localisation start `coldwar_CYP_`; English names/descriptions explain exact units. New modifier/tooltips and scripted effects are explicitly authored and validated rather than merely assumed to exist.

## Ongoing design review

Additional keys in the initial `build_design.py` draft were verified locally: `naval_detection` (`common/dynamic_modifiers/05_antarctica_modifiers.txt:12`), `mobilization_speed` (`05_internal_factions_modifiers.txt:148`), `dig_in_speed_factor` (`05_POTEF_dynamic_modifiers.txt:20`), `production_speed_offices_factor` (`02_commonwealth_dynamic_modifiers.txt:11`), `production_speed_naval_base_factor` (`05_internal_factions_modifiers.txt:82`), `industrial_capacity_factory` (`common/ideas/generic_ideas.txt:368`), `personnel_cost_multiplier_modifier` (same `:897`) and `planning_speed` (`common/ideas/COLDWAR_EGY_1970_ideas.txt:799`). `CAT_agriculture` exists at `common/technology_tags/00_technology.txt:201`.

The current infrastructure upkeep code also charges each road/infrastructure or air-base level **0.005 billion/week**, and radar/anti-air **0.007 billion/week** before its multiplier (`mdcw_imperia_infrastructure_effects.txt:29–46`). Queueing a building avoids a free instant grant but does not remove eventual upkeep; mark such projects as dependent on engine budget validation.

Narrative/access checks requested during drafting: civilian protection must not block military resistance to invasion, and military resistance must not require repression. Emergency housing and property restitution may compete for immediate funding but housing must not permanently erase restitution/return claims. Implement each as a real resource/pacing choice instead of treating military defence or temporary shelter as a moral veto.

Concrete later-date decision leak, to fix only when runtime work is authorised: `common/decisions/categories/99_GRE_decision_categories.txt:47` exposes `CYP_NCY_diplomatic_category` for CYP/NCY whenever GRE exists, without a scenario/date gate. Its `common/decisions/CYP_decisions.txt:2` offshore-gas decision and `:25` EU-accession push can therefore appear in 1970. The foreign-investment decision at `:86` also spends 0.3 billion (a major 1970 sum) for a timed idea. Exclude incompatible modern decisions in the Cold War scenario rather than leave parallel bonuses and anachronistic gas/EU content active. `common/on_actions/CYP_on_actions.txt` already requires the later partition idea and NCY existence for its ambient Green Line incident; this is distinct from the new 1970 enclave system.

## Initial 328-focus JSON audit (superseded by the final 330-focus review below)

Reviewed the generated `coldwar_cyprus_1970_design.json` with 328 focus proposals, 240 party focuses, 36 distinct modifier keys, 5 distinct research categories and 26 named event contracts (29 focus references). The following is a static design audit, not an engine validation or a claim that comment-only requirements work in game.

### Verified in the full data

- **All 36 modifier keys** occur as definitions or active uses in the local MD/Cold War scripts; zero unsupported modifier names were found. This covers both starting/contingent spirit definitions and all focus rewards.
- **All five actual research categories** are present in `common/technology_tags/00_technology.txt`: `CAT_agriculture`, `CAT_anti_air`, `CAT_small_arms`, `CAT_towed_artillery`, `CAT_utility_vehicles`. The six generated `add_tech_bonus` blocks use a unique bonus name, `bonus = 0.25`, `uses = 1` and a valid category. No research slots or ahead-of-time reductions are granted.
- Every generated money-cost snippet sets `treasury_change = gdp_total`, multiplies by negative design percentage divided by 100, then calls the existing `modify_treasury_effect`. Thus a design `cost = 0.5` means **0.5% GDP**, not 50% or 0.5 billion. Syntax and helper signature match local implementations. Affordability/atomicity remain future implementation work.
- **All 24 index/ideology pairs** match native MD's subparty categories; all **240 political focuses** contain an exact `ruling_party = index` check. Indices 0–3 Western, 4–9 Emerging, 10–11 Salafist, 12–19 Non-Aligned and 20–23 Nationalist match the native party system. These are engine categories, not historical evidence that all 24 movements existed in Cyprus.
- `force_update_dynamic_modifier = yes` is used by native MD (`common/scripted_effects/99_Commonwealth_scripted_effects.txt:74` and following). Programme-update snippets use real engine/script syntax, but their **new programme definitions and variable initialization do not yet exist**. Current-party `enable` conditions still must be authored, not inferred from `scope = party programme` metadata.
- Every referenced event-contract label has a design contract entry. These labels are **new unimplemented event contracts**, not pre-existing scripted-effect names, and the snippets correctly show them only as comments. None may be pasted as `label = yes` and assumed functional.

### Prioritized corrections and implementation prerequisites

1. **Combined civilian-construction reward exceeds the stated 15% target.** The graph-compatible route `productive_diversification` (+5% civilian construction), `industrial_estate` (+5%), accepted `soviet_trade` (+3%), and active-party `p4_second_b` (+5%) totals **+18%** before base-game effects. Count building-specific bonuses together with generic construction bonuses. Reduce one or more rewards by 3 percentage points, or explicitly revise the cap and justify the higher specialized bonus. This is independent of the initial narrow-economy penalty once that penalty has been removed.
2. **Clarify net versus gross organization cap and encode retained penalties.** Static compatible-focus optimization reaches **+14% gross organization** under parties 21/22 via retained mainland officers, mobile reserve, accepted Greek mission, air observation/evacuation and the relevant party military policy. The note that mainland officers retain half the divided-command penalty means a final **-2.5%** organization penalty remains, making this approximately **+11.5% net**. The cap must say whether it means gross rewards or net authored final effects. A constitutional-guard path must require civilian command and bar coup regimes in real code; otherwise +13–14% can remain possible without the intended malus. Do not remove the remaining divided-command malus inadvertently via a shared capstone or party switch.
3. **Avoid duplicate reprisal tension.** `collective_reprisals.reward_code` already adds 20 communal tension. Its `reprisal_consequences` contract separately says “raise tension20”. Specify one owner for this increment; implementing both literally produces +40. The event should apply displacement/damage/settlement blocking once, while the focus owns the +20 increment, or vice versa. The contract's consequences are harms, so wording about deferring “benefits” should not obscure that they are mandatory outcomes.
4. **Formation, date, affordability and outcome gates remain prose/comments.** All generated `available_code` blocks contain only the base scenario/tag gate and, for party focuses, the exact subparty gate. They do not implement EOKA B's formation date, the post-1979 extreme-history gate, a Greek monarchy, shared settlement consent, funds, active war, no-coup status or ownership requirements. This is acceptable for a design dossier but these snippets are **partial examples, not paste-ready implementation**. `famagusta_port` has no executable building queue yet; spirit removals are comments; bilateral event dispatch and acceptance logic are also pending.
5. **Distinguish real starting spirits from contingent definitions structurally.** The `starting_spirits` collection includes `displacement_emergency` and `shattered_communities`, which their notes explicitly exclude from January 1970. Add an explicit activation/trigger field or rename the collection `spirit_definitions` before an importer uses it. A note is insufficient protection against granting all nine as startup spirits. Makarios's authority additionally needs a real leader-lifecycle removal hook.
6. **Current-party enable prevents modifier stacking but not permanent progress shopping.** The 12 party focuses granting settlement progress sum to **75 permanent points** across party changes; most are in mutually compatible separate party islands. These are one-time, so this is not infinite farming, but repeated political switching can bypass the intended shared negotiation work if progress alone unlocks settlements. Require shared, named reform milestones and actual community acceptance, award each institutional milestone once globally, and distinguish durable institutional achievements from rhetorical party policies. The optional extreme-history gates must be implemented. A one-time agriculture bonus from party17 can persist after departure; account for this openly rather than imply all political rewards go dormant.

### Cumulative static checks and limits

Binary optimization was run over every encoded prerequisite group (groups AND; alternatives inside each group OR) and reciprocal exclusion, independently for each of 24 active party programmes. Timed modifiers were excluded from permanent totals; conditional agreements were assumed accepted for upper-bound calculations. A constitutional-guard/civilian-command requirement and its exclusion for party22 were also represented for the organization assessment. Prose-only historical, settlement, war and lifecycle conditions are not fully machine-readable, so these are conservative graph bounds, not a playthrough proof.

| Authored permanent modifier objective | Maximum compatible gross reward | Interpretation |
|---|---:|---|
| Research speed | +5% | Under the stated +8% ceiling, before other game sources |
| Generic construction speed | +4% | Does not include building-specific bonuses |
| Civilian-factory construction, generic + specific | +18% | Exceeds the broadly worded +15% construction ceiling |
| Office construction, generic + specific | +4% | No free office sector |
| Infrastructure construction, generic + specific | +12% | Excludes construction upkeep and initial national penalties |
| Naval-base construction, generic + specific | +14% | Includes alternative-port construction support |
| Army organization | +14% gross | Net can be +11.5% when half the starting command penalty correctly remains |
| Stability spirit contributions | +25 points | High graph bound across shared settlement/recovery and one party; not a claim all historical conditions can coincide |

The existing starting penalties, their partial/full replacement, leader spirits, dynamic programme dormancy, event refusals, actual war damage and base-game/Imperia laws are not silently mixed into those gross maxima. Final net totals need explicit outcome-state accounting. Re-check this table after numerical revisions.

The earlier defence/access issue is resolved in the revised design: both civilian protection and emergency repression can lead to either a ceasefire proposal or military resistance. Housing is now expressly described as postponing rather than extinguishing restitution, with later accountability/reconstruction conditions. The later event implementation must preserve that distinction.

## Historical 330-focus JSON review (superseded by the six-route revision)

**Current result: the identified numerical and data-model issues are resolved in the 330-focus design.** This section supersedes the earlier 328-focus corrective findings and maxima. No runtime files were edited or game execution performed by this audit agent.

The final file retains 24 party routes / 240 party focuses, 36 verified real modifier keys, five verified technology categories, six correctly shaped one-use 25% `add_tech_bonus` examples and 26 explicitly unimplemented event contracts. All actual modifier keys and party index/ideology mappings remain valid. New crisis/liaison merge nodes do not add economic or military buffs.

Re-ran **192 binary optimization objectives** (24 active parties × eight modifier objectives), including each encoded prerequisite group/exclusion, executable `has_completed_focus` gate sketches and the no-coup constraint for the constitutional guard under parties21/22. Conditional diplomatic rewards are assumed accepted, timed effects excluded, and starting penalties not subtracted from these gross maxima:

| Authored permanent reward objective | Final compatible gross maximum | Target check |
|---|---:|---|
| Army organization | +12% | Meets +12% ceiling; residual starting penalties may lower the net result |
| Research speed | +5% | Below +8% ceiling |
| Generic construction speed | +4% | Below +15% ceiling |
| Civilian-factory construction, generic + specific | +15% | Meets +15% ceiling |
| Office construction, generic + specific | +4% | Below +15% ceiling |
| Infrastructure construction, generic + specific | +12% | Below +15% ceiling |
| Naval-base construction, generic + specific | +14% | Below +15% ceiling |
| Stability spirit contribution | +25 points | Broad compatible-graph bound; not an engine balance certification |

Confirmed changes:

- `mobile_reserve` and accepted `greek_mission` now give organization **+0.02 each**. The gross organization ceiling is met without relying on leaving part of a starting malus behind.
- `industrial_estate` now gives civilian construction **+0.02**. The specialized maximum is now +5% diversification +2% estate +3% accepted Soviet trade +5% active AKEL compact = **+15%**.
- Every spirit definition now has an `activation` field: **seven `start`**, **two `crisis_only`**. Displacement and shattered communities cannot be confused with normal January1970 starts by a field-aware importer.
- `COLDWAR_CYP_1970_party_reform_credit` is initialized to **0**. Each of the 12 party settlement contributions uses `settlement_credit_target` of 5 or10 and adds only `target - previous_credit` when the target is higher; all party focuses now have direct `settlement = 0`. Across arbitrary party switches the ledger is monotonic and its total contribution is bounded at **10**, replacing the old possible75. This proof assumes the ledger is never reset by elections, tree reloads or regime events.
- `reprisal_consequences` now states the focus applies **+20 tension once**, and the event adds displacement, damage and settlement blocking without a second tension increment.
- Outcome-dependent reward sketches are explicitly marked **outcome payload**, below any upfront project-administration payment. They belong in a one-time accepted/result event, not in a focus reward merely sending an offer. These remain design instructions and do not themselves create an event dispatcher.
- Constitutional-settlement gate sketches now block `COLDWAR_CYP_1970_unresolved_reprisals`; the constitutional guard requires completed police oversight and absence of `COLDWAR_CYP_1970_coup_regime_active`. These new flags and their setting/clearing lifecycle must still be implemented coherently.

**Remaining limits are implementation work, not unresolved design numeric blockers:** new programme/idea definitions and initialization; party-enable lifecycles; historical formation/date and extreme-history setting gates; affordability and atomic payments; state/province construction/upkeep; diplomatic dispatch/acceptance/refusal/timeout; once-only outcome markers; leader removal; partial/full starting-spirit replacement; consistent crisis flag lifecycle; modern-decision scenario guards; English localisation and engine validation. Party settlement credit is now bounded, but a numerical credit still cannot substitute for actual shared-reform and community-assent outcome flags. Do not reset its ledger on political transitions.

The static ceilings cover only authored Cyprus reward contributions. Base laws, technologies, Imperia development/employment modifiers, existing national spirits and future foreign effects can change final net game values; these need an initialized January1970 save and selected-path playtests before any multiplayer-balance claim.

## Requested revision: six deeper political routes and Turkish Cypriot agency

The user subsequently requested fewer, more important political parties with deeper and stronger economic choices, an explicit Turkish Cypriot branch and more visible starting burdens. The earlier all24 layout and its numerical ceilings are therefore **superseded as the target design**. The revised proposal retains native indices **1,2,3,4,20,22** and folds the EOKA B/Grivas material into the Enosis/coup crisis network rather than presenting 24 equally developed Cypriot parties. This does not remove the other native MD ideologies from the game.

Pending new JSON audit, proposed **total authored permanent** ceilings are: generic plus specific construction **25%**, army organization **18%**, research **10%**, office tax income **20%**. These are balance targets chosen for a smaller country with deeper paths, not MD constants. Shared rewards and the currently active government programme must both count. Rewards can be stronger without free factories, research slots, modern technologies, unconditional donor cash or bypassing native workforce and recurring upkeep.

### Initial penalty recommendation and correct interpretation

| Proposed starting component | Modifier values | Interpretation / intended relief |
|---|---|---|
| Constitutional breakdown | `stability_factor = -0.10`, `political_power_factor = -0.12` | Institutional legitimacy and policymaking paralysis, relieved by constitutional negotiation or an explicitly different authoritarian settlement with continuing costs |
| Enclave administration and insecurity | `police_cost_multiplier_modifier = 0.10`, `bureaucracy_cost_multiplier_modifier = 0.08` | Police expenses +10%, bureaucracy expenses +8%; the cost is fragmented services/checkpoints/security, not ethnicity |
| State145 movement disruption | `state_production_speed_buildings_factor = -0.05` | Modest geographic approximation, repairable through civilian access and services |
| State146 movement disruption | `state_production_speed_buildings_factor = -0.12`, `state_productivity_growth_modifier = -0.15` | Construction -12%; **positive productivity growth** -15%, not GDP/output -15% |
| Narrow economy, retained | `production_speed_buildings_factor = -0.05` | Import/capital constraints; together with state construction penalties approximately -10% south and -17% north before other sources |

All these keys already exist and use the units specified earlier. If Makarios's authority remains stability +0.03 and PP factor +0.08, the constitutional/leader combination is net stability **-7 points** and PP factor **-4%** before other ideas and laws. Showing both bonuses and burdens makes the difficult start comprehensible without hiding a huge penalty behind a similarly large compensation. The map-state difference must explicitly acknowledge mixed settlements and enclaves across Cyprus, not imply a homogeneous, pre-existing northern polity.

Provide early attainable relief through supervised movement, shared water/health services and police oversight; reserve final constitutional removal for the harder negotiated outcome. Do not demand that a player complete several full political trees before ordinary roads, schools and services become viable. Cost/time and competing priorities can supply the tradeoff for ordinary development focuses without another artificial debuff attached to every benefit.

### Stronger, distinguishable active-government economic profiles

These are profile directions and ranges, not simultaneous grants on every focus:

- **Makarios / independence coalition:** cooperative credit, rural processing, local suppliers and balanced tourism; modest stability plus meaningful sector-specific construction and office income. Municipal partnership versus executive coordination should change where administrative costs fall.
- **Clerides / liberal alternative:** commercial services, shipping administration and investment access; office tax income around +10–15% in the political programme is substantial if offices exist, with foreign dependence/market exposure for the capital-open route. The regulated domestic alternative should offer a positive workforce or tax-administration benefit rather than merely fewer penalties.
- **EDEK / social republic:** skills, public services and a labour compact; research/training or worker-efficiency gains plus service/construction rewards, paid for through education/social spending. Genuine choice between public investment and negotiated cooperatives; neither is a free research slot.
- **AKEL / workers' republic:** food processing, light industry, coordinated construction and workplace representation; strong civilian-industry construction or factory-output profile with appropriate administration costs. Democratic coalition and party-monopoly choices must remain distinct; historical AKEL is not automatically a one-party dictatorship.
- **Progressive Front / Enosis nationalism:** local business, infrastructure and patronage versus transparent island-wide development; useful economic benefits and a real fiscal/diplomatic constraint. Do not turn coercion or removing a community into a productivity upgrade.
- **Coup presidency:** more immediate military organization/readiness and procurement administration, with visible personnel/police expense and a civilian-investment opportunity cost. A junta should still have a playable reconstruction choice instead of existing only as a punitive event chain.

`office_park_income_tax_modifier = 0.20` means **office tax income +20%**, not GDP +20%, all treasury income +20% or 20 tax-rate points. Its definition is at `money_modifier_definitions.txt:268`, and its revenue use at `common/scripted_effects/00_money_system.txt:520`. Benefits only matter if the relevant sector exists; output modifiers alone do not create a factory. `corporate_tax_income_multiplier_modifier` is separately defined at `:212` and used at `00_money_system.txt:431`. Inspect joint tax/office stacking when optimizing the new income ceiling, and do not describe a larger office-revenue modifier as a cash transfer.

### Turkish Cypriot political agency and historical naming

**Rauf Raif Denktaş is Denktaş's full name, not a third politician.** Küçük and Denktaş should have distinct institutional roles and a dated succession; Makarios remains the authored leader of CYP at the January1970 start. A Turkish Cypriot administration, leadership preference, negotiating position and consent should therefore be represented separately from the whole-country `ruling_party` index. Do not set a Turkish Cypriot community leader as sovereign CYP president simply to unlock negotiations, and do not release NCY in1970 to create the missing community mechanics. The official [Denktaş biography](https://cb.gov.ct.tr/tr/cumhurba%C5%9Fkanli%C4%9Fi/cumhurba%C5%9Fkanlar%C4%B1m%C4%B1z/kurucu_cumhurba%C5%9Fkan%C4%B1_rauf_raif_denkta%C5%9F) establishes the name and role in the intercommunal negotiations; the official [Küçük biography](https://www.guvkk.gov.ct.tr/Liderlerimiz/DrFazilKucuk) records his vice-presidential role ending in1973. These are partisan institutional sources, used here for names and institutional chronology, not to adopt their wider conflict narrative.

The CTP branch should unlock no earlier than **27 December1970**, with **Ahmet Mithat Berberoğlu** as founding leader, not a later party leader. The party's own [Berberoğlu biography](https://cumhuriyetciturkpartisi.org/4-nisan-2020-ctpnin-kurucu-genel-baskani-ahmet-mithat-berberoglu-aniliyor/) records his founding leadership for1970–76. A pre-foundation civic/labour organising focus is possible, but it must not pretend the formal party already exists at the January start. If UBP appears later, use its actual **11 October1975** foundation, recorded in [UBP's party history](https://ubp.org.tr/tarihce/), rather than putting the later party label on every1970 Denktaş supporter.

Design recommendation: a clearly visible Turkish Cypriot negotiation/community branch with distinct **Küçük-led institutional protection**, **Denktaş-led autonomy/security negotiation**, and, from its foundation, **Berberoğlu/CTP pluralist-left alternative**. These are design interpretations of political choices, not fixed historical effect measurements. Each can contain civilian-service and economic development options, representation/municipal questions, external support/dependence and negotiations over shared institutions. Community leadership choice must be made by the community/counterpart outcome, or an explicitly playable later administration, not unilaterally awarded to the CYP player's preferred negotiator. The CYP player can choose offers and commitments, and face refusal or a competing counterproposal. TUR approval is not a substitute for Turkish Cypriot political assent.

No new JSON numerical certification is made in this preliminary revision section. The next review must recalculate shared-plus-active-party totals, the different Turkish Cypriot agreement outcomes and mutually exclusive economic packages against the stronger ceilings.

## Six-route 273-focus candidate audit (pre-trim findings; final closeout below)

Reviewed the regenerated design with **273 focuses**, **six political routes of24 focuses each**, **39 Turkish Cypriot focuses**, **eight starting spirit definitions**, **two crisis-only spirit definitions**, **37 distinct real modifier keys**, **eight one-use25% research-bonus examples in five valid categories**, and **49 declared event contracts**. Every referenced contract has a declaration; none of those new labels is misrepresented as an existing MD scripted-effect API. The current target is construction25%, organization18%, research10%, and **office tax income35%** across shared rewards plus one active government programme. The office ceiling was deliberately raised from the preliminary20% proposal; it is a sectoral tax-income ceiling, not a GDP promise.

### Modifiers, gates and persistence

All37 keys, including values inside `spirit_changes.modifiers_after`, were checked against local modifier definitions or active MD uses; no unsupported name was found. The added `production_factory_max_efficiency_factor` exists in `common/ideas/generic_ideas.txt:390`. The five research categories remain `CAT_agriculture`, `CAT_anti_air`, `CAT_small_arms`, `CAT_towed_artillery`, `CAT_utility_vehicles`; all eight snippets use25%, one use, no ahead-of-time reduction or research slot.

All144 political and political-economic focuses use their exact governing indices. The combined Enosis/security route correctly emits `OR = { check_variable = { ruling_party =21 } check_variable = { ruling_party =22 } }` and uses the same **p22** programme namespace for both phases. Its eventual dynamic modifier `enable` must use that same OR. A transition21→22 must neither zero variables nor re-grant completed focuses. Other routes use1/2/3/4/20 respectively; no broad outlook gate replaces the subparty check.

Both `scope = party programme` and `scope = party economic programme` examples update the same `COLDWAR_CYP_1970_pN_programme` variables and modifier. This is correct: economic rewards cannot remain independently active after an election while their political programme goes dormant. Programme definitions/lifecycle hooks are still future runtime work, so prose about current-government-only effects is a contract, not already functioning code. Foreign accepted effects must update that same programme namespace if they are intended as government policy; durable national agreements need a separately explicit persistence decision.

The global party-reform highest-milestone ledger remains bounded at10 and is initialized at0. The prior all24 switching exploit is therefore not restored. Real buildings, existing agreements and shared funded institutions can persist across governments; former party research/construction policies must not.

### Turkish Cypriot relief is explicit and staged

The proposed access stage is dimensionally correct: state145 construction **-2.5%**; state146 construction **-6%** and **positive-growth multiplier -7.5%**; national bureaucracy **+4%** and police **+5%**. These replace the corresponding starting values; they are not additional modifiers. The shared `tc_access_protocol` contract explicitly requires a highest-relief stage ledger, preventing repeated halving, duplicate rewards or a delayed offer reapplying a worse stage.

Accepted joint/local service compacts each remove the two initial state-access modifiers and the national parallel-administration spirit. Exactly **one** accepted service programme replaces them: joint services stability+4/bureaucracy+3%; local services stability+3/bureaucracy+6%. The two focuses reciprocally exclude each other and their contracts require atomic replacement, civilian access and actual community acceptance. These outcomes do not remove constitutional deadlock or war damage automatically. An eventual outcome dispatcher must read `spirit_changes` and preserve state145/146 scopes; metadata alone does not execute removal.

**One remaining synchronization detail:** the older `joint_services` focus still describes removing the southern penalty and setting northern construction to-3% in note text without an explicit `spirit_changes` payload. Route that older relief through the same global relief ledger as the Turkish Cypriot branch. Otherwise a later access event could revive an already removed penalty, or two service programmes could coexist. Similarly, constitutional settlement and the service compact must share coherent final-stage rules. This is a state-machine implementation requirement, not a demand for another permanent debuff.

CTP's actual gate sketch uses **`date >1970.12.26` plus `COLDWAR_CYP_1970_ctp_formed`**, matching the sourced27December1970 foundation. Berberoğlu is correctly identified as founding leader. Küçük/Denktaş channels retain counterpart agency; `tc_community_mandate` explicitly prevents CYP setting assent by unilateral focus completion or substituting Ankara's approval. NoNCY release at the1970 start is implied.

### Exact compatible-combination optimization

Ran **54 binary optimization objectives** (six active programmes ×nine reward objectives) over encoded prerequisites/exclusions and explicit completed-focus gates; the constitutional guard is barred under the combined coup route. Timed effects are excluded, conditional offers assumed accepted for a conservative upper bound, and starting maluses are not used to conceal excessive rewards.

| Permanent authored reward objective | Candidate gross maximum | Assessment |
|---|---:|---|
| Army organization | +18% | Meets18% target; combined coup route |
| Research | +8% | Below10%; Clerides route |
| Generic construction | +15% | Below25%; EDEK route |
| Civilian construction, generic+specific | **+27%** | **Exceeds25%; Progressive Front route** |
| Office construction, generic+specific | +15% | Below25% |
| Infrastructure construction, generic+specific | **+29%** | **Exceeds25%; EDEK route** |
| Naval-base construction, generic+specific | +25% | Meets25% |
| Office tax income | +34% | Below35%; Clerides with tourism/service and accepted local-services context |
| Stability spirit contributions | +43points | Conservative shared+party+community graph bound; no formal stability ceiling was requested |

**Prioritized numeric fixes:**

1. Progressive Front's maximum civilian construction is shared diversification5 +estate2 +accepted Soviet trade3 +party generic construction12 +party workshop construction5 = **27%**. Trim two points from that compatible political/economic package (for example workshop-specific5→3), preserving route identity.
2. EDEK's maximum infrastructure construction is shared roads8 +party generic construction15 +party infrastructure6 = **29%**. Trim four points from that combination (for example the infrastructure-specific6→2) or explicitly adopt a higher specialized ceiling. Its civilian construction already meets25% and its naval construction meets25%, so trimming only the infrastructure-specific reward is a clean adjustment.
3. AKEL currently reaches **25%**, not27%, in the audited file: shared civilian10 plus its selected economic/political contributions15. No further AKEL construction reduction is necessary for the stated ceiling.

The strongest office profile is34% office tax income: shared tourism/services11 +Turkish Cypriot business licences3 +Clerides's compatible programme20. The original office sector's size, staffing, general tax multipliers and tax rate still determine actual revenue. Higher stability can result from multiple lasting civilian institutions; the43-point gross bound warrants an initialized-save playtest but is not a declared cap breach or a43% GDP claim.

Loans have explicit new contracts requiring a consenting lender debit, CYP treasury credit, equal debt through `modify_debt_effect`, and repayment/amount checks. These are not implemented loan APIs or free money. GDP-relative administrative costs continue to use the real treasury helper correctly. Partial reward snippets, formation/date flags, state-stage dispatcher, programme definitions, counterpart AI decisions, affordability and engine/multiplayer testing remain implementation work.

## Final six-route closeout: 273 focuses

**All requested permanent numerical ceilings now pass the static compatible-route audit.** The final revision sets EDEK's `p3_project_a2` infrastructure bonus to **+2%**, and Progressive Front's `p20_national_programme` generic construction to **+1%**. Re-ran all54 objectives over the updated JSON, with the same explicit prerequisite/exclusion and coup-regime constraints described above:

| Permanent authored objective | Final maximum | Ceiling |
|---|---:|---:|
| Organization | +18% | 18% |
| Research speed | +8% | 10% |
| Generic construction | +15% | 25% |
| Civilian construction, generic+specific | +25% | 25% |
| Office construction, generic+specific | +15% | 25% |
| Infrastructure construction, generic+specific | +25% | 25% |
| Naval-base construction, generic+specific | +25% | 25% |
| Office tax income | +34% | 35% |

The conservative stability contribution bound remains **+43points**, a shared/community/one-government graph bound rather than a promised actual start-to-finish stability gain. It has no requested numeric ceiling; initialized-save playtesting remains appropriate because baseline stability, leadership changes, war effects, timing and mutually inconsistent event outcomes are not fully represented by graph constraints.

The previous AKEL/Progressive Front/EDEK cap findings are closed for this JSON. All37 modifier keys, eight research examples, six24-focus political routes and their exact gates remain as audited. Combined21/22 shares a single programme namespace; Turkish Cypriot staged relief, independent assent and datedCTP formation remain explicit design requirements.

No remaining numerical blocker was identified. The legacy `joint_services` note-only stage must be routed through the same relief ledger during implementation, and all contracts/programme/flag/affordability/state-dispatch lifecycles need actual code and engine checks. This document certifies source-key and static design consistency to the stated extent; it does not claim completed runtime implementation or multiplayer-tested balance.

## Final 295-focus crisis addendum

The research-led22-focus road-to-war branch increases the design to295 nodes while retaining six political routes and39 Turkish Cypriot nodes. It adds one starting **Armed Enosis Underground** spirit (stability-3points, PPfactor-5%) and no new modifier key: nine starting spirits and two contingent crisis spirits are explicitly distinguished. Historical names/starting explanations now acknowledge1969normalisation rather than an unchanged1964blockade. NationalFront1970 andEOKA-B1971 are distinct.

New crisis-focus modifiers are foreign-influence defence-4% for retained mainland dependence, and defence+3% for180days on a valid preparedness outcome. No permanent positive organization/research/construction contribution was added, so the273-focus final permanent maxima remain applicable without a redundant full optimization run. Coup pressure is a separate initialized45/clamped0–100 design variable, not a historical probability. Every war event-contract reference resolves to a design declaration; events/adapters themselves are unimplemented.

The older `joint_services` path and Turkish Cypriot access/service contracts now explicitly share the monotonic highest-relief ledger, closing the prior note-level synchronization ambiguity as a design requirement. Runtime stage replacement is still to author and test. The new stage/actor gates, fast July/August pacing requirement, empty-OOB/naval readiness, two-province map, NCYcore/release and generic conditional-peace pitfalls are documented in [WAR_MECHANICS.md](WAR_MECHANICS.md). There is no claim that a flag stops combat, that an event creates a valid landing plan or that a new ceasefire adapter already exists.
