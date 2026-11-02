# Cuba 1970 concept mechanics review

Scope: independent review of the pure-data proposal in `tools/cuba_1970_concept/content.py`. This is a concept audit; it adds no game code. The listed values are proposed balance values, not historical quantities. Runtime loading, focus tooltips, and live-game scope behavior remain untested.

## Confirmed corrections

- `rail_lorries` originally requested `CAT_railway`, which has no technology category consumer in the repository. Its rail technology `mdcw_mechanized_track_renewal_1967` is valid in 1970 and tagged `CAT_industry` and `CAT_infrastructure` in `common/technologies/mdcw_early_railway.txt`; use `CAT_infrastructure` for the project. The available rail technologies are dated 1940, 1953, 1960, and 1967, so the suggested bonus has relevant pre-1970 research.
- `coastal_patrols` originally requested singular `CAT_corvette`. The exact category is `CAT_corvettes`, used by naval technologies in `common/technologies/naval.txt`; the concept data now uses the plural spelling.
- `CAT_small_arms` is valid, including the 1969 `mdcw_underbarrel_grenade_launcher_1969` in `common/technologies/mdcw_infantry_1965_1990.txt`. `CAT_electronics` is valid in `common/technologies/engineering.txt`, and `CAT_industry` is valid in the early railway, early industry, and 1968–85 industry files. These categories have eligible 1970-era technologies; generic category bonuses can also affect later eligible technologies when they are researched.
- `STARTING_SPIRITS.social_achievements.picture = "cubabattleofidea"` points at a focus graphic in `interface/goals.gfx`, not an idea graphic. `interface/MD_ideas.gfx` has no `GFX_idea_cubabattleofidea`. The renderer must substitute a confirmed idea image such as `castroismcubaidea` and validate every spirit picture against `GFX_idea_<picture>`; focus art is not interchangeable with idea art.

## Supported API and scope

The following are supported by current main MD consumers. Values in these modifier blocks are additive fractions unless the named system's calculation says otherwise; most `0.05` values mean 5%, while `stability_factor = 0.05` is a 5 percentage-point stability change. The API proves that the value is read, not that the proposed balance is ideal.

| Concept keys | Consumer / interpretation | Audit note |
|---|---|---|
| `production_speed_buildings_factor` | Construction-speed calculation and construction-related effects | Construction speed, not a direct building grant. |
| `civilian_factories_productivity`, `industrial_capacity_factory`, `production_factory_efficiency_gain_factor`, `production_factory_max_efficiency_factor` | Main-MD productivity / factory-output modifier readers | Supported output and efficiency effects. Keep named factory-output claims distinct from construction speed. |
| `agricolture_productivity_modifier`, `agriculture_district_income_tax_modifier` | Weekly money aggregation reads both in the agriculture productivity / district-tax calculations (`common/scripted_effects/00_money_system.txt`, approx. lines 412–553) | `agricolture_` spelling is the actual API key. These affect modeled output/income, not state food stock or direct food security. |
| `bureaucracy_cost_multiplier_modifier`, `health_cost_multiplier_modifier`, `education_cost_multiplier_modifier`, `social_cost_multiplier_modifier`, `army_personnel_cost_multiplier_modifier` | Main-MD weekly spending calculations and expense modifier definitions | Positive values increase the associated ongoing expenditure; negative values reduce it. Do not describe as one-time Treasury. |
| `healthcare_workforce_requirement_modifier`, `healthcare_income_multiplier_modifier` | Healthcare budget/system calculations and money modifier definitions (`common/modifier_definitions/money_modifier_definitions.txt`) | These change modeled sector staffing requirement/income. They do not create doctors or hospitals. |
| `total_workforce_modifier`, `monthly_population` | Workforce and population-growth readers | They are rate/factor effects, not historical head-count changes or migration events. |
| `migration_rate_value_factor`, `imp_refugee_integration_rate` | Native migration model and Imperia refugee integration (`common/modifier_definitions/migration_modifier_definitions.txt`; `common/scripted_effects/imp_refugees_effects.txt`) | Does not count Cuban emigrants or trigger return migration by itself. Integration rate is subject to the refugee-system clamp. |
| `foreign_influence_modifier`, `foreign_influence_defense_modifier` | Main-MD influence calculation / influence modifier definitions | These affect influence and resistance calculations; do not use them to claim direct relations or treaty acceptance. |
| `imp_sanction_resistance` | Imperia sanction effectiveness/resistance calculation (`common/scripted_effects/imp_sanctions_effects.txt`) | Affects sanction calculations, not legal embargo state. Do not stack the same embargo fiction as a duplicated malus. |
| `research_speed_factor`, `political_power_factor`, `stability_factor`, `drift_defence_factor`, `intelligence_agency_defense` | Native HOI4/MD country modifier readers | Standard modifier key; `intelligence_agency_defense` is a counterintelligence effect, not generalized repression. |
| `army_core_defence_factor`, `army_attack_factor`, `army_defence_factor`, `army_org_factor`, `training_time_army_factor`, `supply_consumption_factor`, `army_fuel_consumption_factor` | Native military modifiers used in MD ideas/doctrines and the Cold War files | They affect division statistics/costs. Training-time key is specifically `training_time_army_factor` (not `training_time_factor`). |
| `send_volunteer_size`, `special_forces_cap` | Native volunteer and special-forces modifiers used in ideas/traits | Keys are valid. Before emitting player-facing units, render/hover the modifiers: do not assume `send_volunteer_size = 2` literally means two extra divisions or that `.03` special-forces capacity means 3 percentage points without confirming the UI's native description. |

The concept's recurring cost modifiers are correctly proposed as weekly-system modifiers rather than repeated Treasury debits. Their displayed effect should say, for example, “Weekly education expenditure +5%,” not a flat “cost +5%.” `healthcare_income_multiplier_modifier` is healthcare-sector income; `health_cost_multiplier_modifier` is a separate spending multiplier.

## Budget helper contract

Native helpers in `common/scripted_effects/00_budget_effects.txt` are not safe unguarded concept effects at cap: `increase_education_budget` upgrades `edu_01` through `edu_04` to `edu_05` and falls through to `add_political_power = 150`; `increase_healthcare_budget` upgrades `health_01` through `health_05` to `health_06` and also falls through to `add_political_power = 150`. The files' `_2`/`_3`/`_4` variants likewise have PP compensation branches.

For `social_promise` and `health_workforce`, proposed contract:

```hoi4
# Concept contract only; emitter must provide separate named fallback idea/effect.
if = {
    limit = { OR = { has_idea = edu_01 has_idea = edu_02 has_idea = edu_03 has_idea = edu_04 } }
    increase_education_budget = yes
}
else_if = {
    limit = { has_idea = edu_05 }
    add_idea = COLDWAR_CUB_education_efficiency
}
else = {
    set_country_flag = COLDWAR_CUB_education_budget_initialization_pending
}
```

Healthcare uses the corresponding `health_01`–`health_05`, max `health_06`, and named `COLDWAR_CUB_health_efficiency` fallback. There is **no confirmed 1970 idea baseline** in the current Cuban setup. The `1970.1.1` history block in `history/countries/CUB - Cuba.txt` (lines 5–58) has no education or healthcare budget idea; `edu_02`, `health_02`, and `corruption_level_06` appear only in its later `2000.1.1` idea set (lines 504, 510–511) and do not load in the 1970 scenario. The native startup `every_country` path calls `set_law_vars = yes` (`common/on_actions/00_on_actions.txt`, line 1830); `common/scripted_effects/00_law_attitudes.txt` (lines 55–76 and 79–104) then gives a missing education or health idea a fallback *law variable* of 1. It does not add `edu_01` or `health_01`. The subsequent `ingame_update_setup` (`common/scripted_effects/00_money_system.txt`, line 222), expected-spending calculation (`common/scripted_effects/00_expected_spending_effects.txt`), and literacy setup (`common/scripted_effects/00_education_effects.txt`) calculate spending/tables or literacy modifiers but do not create those idea tiers. Cuba therefore has floor-level law-variable spending, but the idea-based budget helpers see no tier and would grant their `+150` PP fallback. Do not invoke either helper until exporter/startup setup establishes a real tier idea.

Required export/startup contract: add explicit tier ideas to the 1970 CUB initialization, then recheck the idea on both focus availability and completion. If this initialization is absent, keep each budget node unavailable with a visible initialization requirement/pending receipt; do not invent a tier. Once initialized, education below-cap is `edu_01..edu_04`, cap is `edu_05`; healthcare below-cap is `health_01..health_05`, cap is `health_06`. The concept's cap alternative is a named -3% ongoing relevant expenditure/service-efficiency programme; its actual idea, scope, stacking, removal, and display still need definition.

`decrease_corruption = yes` also has a PP floor fallback: at `corruption_level_01`, `common/scripted_effects/00_budget_effects.txt` grants `+150` PP instead of reducing corruption. Guard the helper to existing `corruption_level_02..corruption_level_10` tiers. At the minimum-corruption cap (`corruption_level_01`), use a named oversight programme with bureaucracy expenditure -3%; if no corruption tier idea exists, leave the focus pending or make initialization explicit rather than invoking the helper. This keeps the declared alternative within supported weekly-spending modifiers and avoids unrelated PP.

The same initialization issue applies to corruption: CUB's 1970 history block has no `corruption_level_XX` idea. Its later 2000 idea set contains `corruption_level_06`, but the generic startup path does not establish a corruption tier. `decrease_corruption` (`common/scripted_effects/00_budget_effects.txt`, lines 783–850) silently does nothing with no tier (there is no final `else`), so guard `courts_factions` and `national_settlement` on an actual tier and provide an explicit pending/initialization path. Once initialized, the exact branch contract is:

```hoi4
if = {
    limit = {
        OR = {
            has_idea = corruption_level_02
            has_idea = corruption_level_03
            has_idea = corruption_level_04
            has_idea = corruption_level_05
            has_idea = corruption_level_06
            has_idea = corruption_level_07
            has_idea = corruption_level_08
            has_idea = corruption_level_09
            has_idea = corruption_level_10
        }
    }
    decrease_corruption = yes
}
else_if = {
    limit = { has_idea = corruption_level_01 }
    add_idea = COLDWAR_CUB_oversight_efficiency # named -3% bureaucracy expenditure programme
}
else = {
    set_country_flag = COLDWAR_CUB_corruption_initialization_pending
}
```

## Effect syntax and transaction boundaries

These concept kinds require a renderer to turn them into proven effect sequences or clearly marked new custom glue; the Python records themselves are not native HOI4 commands.

```hoi4
# One-time Treasury debit/credit in the acting country's country scope.
set_temp_variable = { treasury_change = -0.60 }
modify_treasury_effect = yes

# Debt principal adjustment; debt is separate from cash transfer.
set_temp_variable = { debt_change = 0.50 }
modify_debt_effect = yes

# Research uses need to be one-time grants; do not put them in a repeating refresh.
add_tech_bonus = { name = COLDWAR_CUB_example uses = 1 bonus = 0.25 category = CAT_electronics }
```

Treasury literal examples in the concept are at most two decimal places, below the project's five-fractional-digit parser limit. Event offers must be recipient-owned and revalidate both parties, the pending receipt, the agreed native finance/debt policy, target state ownership/control, and any target building cap before charging. Each payment, research use, building or transfer should have an exactly-once receipt. The transaction claims in `CONTRACTS` are appropriate as requirements, but cannot be delivered by a focus `offer` record without bilateral events/receipts.

Existing `mdcw_diaspora_*`, `mdcw_guest_workers_*` and `IMP_refugees` systems do provide migration-related hooks. They cover registered bilateral guest-worker, voluntary-return, refugee-pull, and integration processes. They do not make `migration_rate_value_factor` a mass-emigration simulator or establish that historical departures are a second population subtraction. The exile spirit's workforce disruption plus explicit voluntary-return agreement is consequently the safer scope.

## Graph, party gates, and lifetime checks

- Current registry slot mapping confirms these concept slots: PCC/Fidel `4`; Microfraction `6`; Guevarist `19`; FAR `22`; Auténtico `3`; Ortodoxo `18`; Christian Democrat `1`; Liberal `2`; RECE `0`; Alpha 66 `20`. The final concept has thirteen governing programmes including the compact institutional programmes in the addendum; it introduces no invented live slot. Keep the party gate exact in both focus availability and completion reward. Shared economy/society/defence/foreign programmes have no party slot and remain persistent country projects.
- `cmea_application` is reachable from `moscow_guarantee` before the only currently explicit member-only node, `division_labour`. Its requirement must resolve to the actual `COLDWAR_CUB_cmea_member` spirit in availability and again in completion reward. The admission event must add that idea only on Soviet acceptance. If emitter adds more member-only nodes later, each needs the same paired gate. Do not claim the generic MD CMEA/commonwealth membership framework exists: current Soviet Cold War files provide a Soviet commonwealth framework, while Cuba-specific admission/receipt and membership semantics still require custom integration.
- Party programmes must be active modifiers keyed to the exact governing subparty, not permanent ideas applied when a branch is completed. Their active modifiers must deactivate on change away and reactivate on return; one-time funds, buildings, research grants, and agreement receipts must persist and never replay. Shared social achievements, literacy, health, and built assets must not be removed with a party programme.
- `extra_gate` currently stores prose, not machine-verifiable triggers. Emitter must translate each into actual script: country existence/peace, ownership/control, date, actual spirit/receipt, or duplicate-payment guard. Route/date/SOV existence are hidden presentation checks; the actual CMEA membership requirement should be visible as a meaningful player requirement.

## Custom glue required; not existing native effects

The following `fx(kind=...)` values are concept opcodes, not stock effects: `harvest_course`, `stability`, `enterprise_reform`, `relations`, `transition_charter`, `rename_island`, `contract_followup`, `offer`, `debt`, and `law` as a data wrapper. Implement them through marked scripted effects/events or map them to exact native commands. `law` helper names that do exist include budget helpers and corruption helpers; the max/missing budget behavior above still needs guarding. Treaty terms for Soviet support, CMEA admission, requested medical/overseas assistance, US normalization, DDR commission/cooperation, and island cession all require custom bilateral acceptance, expiration, refusal, duplicate-receipt, and acceptance-time revalidation glue. There is no generic Cuban Colonial Affairs effect to deliver an African mandate; the current colonial/contact machinery is tied to defined imperial, occupation, or country-specific contacts. Use an accepted recipient-owned advisory/volunteer route and do not bypass troop stocks or recipient consent.

The US normalization offer must query live bilateral embargo/sanction state. Cuban history may contain opinion modifiers, but opinions are not legal embargo state. Remove the Cuban embargo spirit only after the settlement, and avoid charging both that idea and a live native/Imperia sanction for the same restriction. A `break_embargo` command may need correct source/target scope; confirm the exact live direction before emitting.

## Verification limits and next build gate

The two category typos were fixed in the pure data. Before converting this proposal to runtime files, the emitter should validate every category against technology category tags and eligible 1970 techs, each modifier against its provider and consumer, every idea picture against `interface/MD_ideas.gfx`, each budget completion branch against its tier, each governing slot against `CUB.json`, and each custom contract against an exactly-once receipt. Run the project parser/generator checks and then open the tree in game to inspect loaded effects and visible requirement/effect rows. Static source evidence cannot establish engine tooltip wording, actual spendable Treasury changes on multiplayer clients, or event transaction behavior under simultaneous acceptance.


## Addendum: governing-current coverage

The pure data now includes nine focuses in three compact institutional programmes. Total content is 115 focuses across 17 groups, below the 120-focus cap. All three roots sit at their requested coordinates; each choice branch is gated by its root and the two alternatives are mutually exclusive.

| Registered current slot | Programme / focus IDs | Scope and trade-off |
|---|---|---|
| `5` | `tricontinental_secretariat`, `diplomatic_solidarity`, `foreign_cadres` | OSPAAAL-led alternate governing alignment: conference and diplomatic solidarity versus a larger overseas cadre network that reduces domestic workforce, increases bureaucracy spending, and weakens foreign-influence defence. Registry current is represented as an alternate government; OSPAAAL was an international solidarity organization, not a Cuban political party. |
| `7` | `interior_ministry`, `professional_intelligence`, `mass_surveillance` | MININT-led alternate government: professional counterintelligence with research and staffing costs versus mass surveillance with stronger counterintelligence but penalties to political-power gain, research, workforce, and foreign-influence defence. No separate historical party is claimed. |
| `13` | `plan_balances`, `balanced_targets`, `enterprise_incentives` | JUCEPLAN-led technocratic alternative: balance agricultural/civilian output while accepting weaker construction and market income, or improve enterprise productivity/efficiency at the cost of some agricultural priority and tax income. No separate historical party is claimed. |

All nine nodes use already audited MD modifier keys and confirmed focus-art aliases. Their modifiers remain conditional on the exact subparty in office; no extra starting spirit, leader, migration event, treaty, or one-time reward is introduced. The MININT alternatives model diplomatic insulation through the existing foreign-influence modifier rather than claiming a direct bilateral opinion penalty. The repository has no source-backed generic raw-opinion modifier key for this concept; any literal bilateral relations penalty needs a separately defined opinion modifier/effect contract and should not be inferred from counterintelligence or influence defence.


## Final design reconciliation

`lifecycle.py` now specifies the proposed missing-category initialization (`edu_02`, `health_02`, `corruption_level_04`), guarded native helpers and non-stacking cap alternatives. These tiers are explicit balance proposals, not values present in Cuba's January 1970 history. The final exporter creates review excerpts only, hides internal routing/date conditions, retains real availability and completion guards, and distinguishes new custom agreement contracts from existing MD effects. Government eligibility follows the actual native governing slot immediately; political-transition context is not an extra redundant unlock focus. No runtime files were installed.


## Final economic-scope correction

The equipment-market reader at `00_money_system.txt:2425` multiplies `market_sold_cost` from equipment sales. It is not sugar or general commerce revenue. The final design therefore removes this key from all Cuban focus and starting-spirit effects: sugar specialization/CMEA use the already verified agricultural district tax income reader (~550); food-first reduces those receipts. General resource-export exposure uses `resource_export_multiplier_modifier`, with the exact export-revenue reader verified in the final audit. Joint Ventures improves production efficiency growth; exile investment settlements improve construction. No equipment-market modifier is mislabeled as sugar income. Caribbean cooperation, African missions and Washington talks remain reachable from either Soviet cooperation or independent diplomacy.


## Accepted concept revision: overseas and medical costs

User feedback removes `total_workforce_modifier = -0.01` from both Expeditionary Forces (native preview title Overseas Forces) and Medical Brigades. Expeditionary readiness instead applies `supply_consumption_factor = 0.05`; its existing +12% weekly army personnel expenditure remains. Medical Brigades now applies `health_cost_multiplier_modifier = 0.10` in total, replacing the earlier +5% healthcare expense and -1% workforce combination. The medical-mission contract carries no extra workforce penalty. These are already audited native modifier readers; focus descriptions, agreement terms, generated matrix, preview and compatible balance ranges have been regenerated. No live game files were changed.
