IMPERIA COLD WAR

# France party revision: independent mechanics review

## Scope

Read-only review of `proposal.json` and `CHANGES.json` at proposal SHA-256 `5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419` and changes SHA-256 `5d03972c102c622231d77917b83d93dada885781aece1258dd46f91d6d132ae7`. The proposal has 156 focuses, 35 bilateral offers, 16 party-specific offers, and five domestic decisions. No builder, generated game script, or loaded-mod file was edited.

## Native effect and research verification

All 45 modifier keys used by the current proposal appear in active local MD idea or dynamic-modifier blocks. The companion [REVIEW.json](REVIEW.json) records one exact provider example and line for each key. The implementation distinction matters for several families:

- `civilian_factories_productivity`, `offices_productivity`, `military_factories_productivity`, `corporate_tax_income_multiplier_modifier`, `tax_gain_multiplier_modifier`, and `agricolture_productivity_modifier` feed MD economic calculations. For example, the current money system multiplies corporate-tax yield by its modifier and separately applies office and civilian productivity factors in [00_money_system.txt](../../common/scripted_effects/00_money_system.txt:442).
- Personnel, equipment, administration, education, health, police, and social cost modifiers change their corresponding expense multipliers. Positive values raise costs; they are not bonuses. The native consumers include [00_money_system.txt](../../common/scripted_effects/00_money_system.txt:3240) and the percentage definitions in [money_modifier_definitions.txt](../../common/modifier_definitions/money_modifier_definitions.txt:23).
- `production_factory_efficiency_gain_factor` changes line-efficiency growth; `production_factory_max_efficiency_factor` changes the maximum. `production_speed_*_factor` changes construction speed for that building family. These are distinct effects.
- `foreign_influence_defense_modifier` raises defensive resistance when positive and weakens it when negative. The calculation compares the target's defense against the influencer's influence in [00_influence_scripted_effects.txt](../../common/scripted_effects/00_influence_scripted_effects.txt:250). `foreign_influence_modifier` changes the country's influence output.
- `energy_use_modifier_civs` changes civilian-factory energy demand only. The current formula is in [!_energy_effects.txt](../../common/scripted_effects/!_energy_effects.txt:254). It does not grant power generation. `energy_gain_multiplier` and `nuclear_energy_generation_modifier` are separate generation effects; nuclear generation applies to reactors that exist, as shown at [!_energy_effects.txt](../../common/scripted_effects/!_energy_effects.txt:483).
- Army organization, core defence, reinforcement, supply, training time, planning, air training XP, and accident modifiers are present in current MD idea blocks. Their displayed values affect those specific systems; they do not imply a generic combat bonus.

All seven proposed research categories are real technology tags: `CAT_armor`, `CAT_naval`, `CAT_aircraft`, `CAT_industry`, `CAT_energy`, `CAT_nuclear_reactors`, and `CAT_electronics` appear in [00_technology.txt](../../common/technology_tags/00_technology.txt:26). `CAT_energy` is a valid category; it was omitted from the older France palette but exists in this live source. Finite `research` rewards remain distinct from `research_speed_factor`.

## Payment, consent, and assets

The 35 bilateral offers use each payer's own `gdp_total` basis for setup and weekly costs. Weekly contracts are annual GDP shares divided by 52; no flat Treasury cost, fixed-price fallback, or Treasury-balance gate appears in the proposal. Offer effects describe both France and the recipient, while the acceptance terms require named-recipient consent, peace, no bilateral embargo or mirrored sanctions, valid parent/membership requirements, and a one-time atomic transaction.

All building rewards specify one slot per level before the building and one-time application. The seven external state candidates and their static headroom are recorded in [ASSET_REFERENCE.md](ASSET_REFERENCE.md). Local French assets have matching 1970 owner/controller records and room under their category/building limits. These history-derived figures are not live-game guarantees: acceptance still needs current ownership, control, full control, native building cap, and slot-capacity rechecks before either payer is charged.

Party-focus modifiers use the exact current ruling-party triggers in [core.py](../france_1970_runtime/core.py:11). Its programme synchronizer activates only the matching party pool, and deactivates it when that party leaves office ([core.py](../france_1970_runtime/core.py:503)). NATO party programmes additionally require UDR and `NATO_member`. Treaty ideas are separate from domestic party modifiers and persist across elections under the proposal lifecycle rules.

## Reachable stacking bounds

These are long-horizon campaign ceilings, not one-government or January 1970 opening totals. They assume relevant party governments occur in succession, all recipients accept, every partner continues to exist, and agreements remain valid at peace without embargoes or sanctions. Date-gated FN content is unavailable before its later identity transition. Mutually exclusive focuses were not summed together.

- The 16 party-specific offers permit at most 10 concurrently signed party agreements along compatible focus branches: one each in UDR, RI, Centre, Radical, PS, PSU, Ecology, and the right branch, plus the PCF Soviet parent and one of its two mutually exclusive specialisations. The PCF Italian cooperation path excludes the Soviet parent path. `pcf_energy_contract` and `pcf_shipping_contract` exclude each other; `communist_settlement` accepts the selected continuation through one OR prerequisite group.
- The compatible long-horizon ceiling is 19 signed offers total: up to 10 party-specific, up to eight compatible diplomatic offers from the general diplomacy branches, and one NATO offer from one NATO strategy branch. This requires government changes over time; the domestic modifiers from different party governments do not add together.
- Selecting a compatible set that maximises French recurring programme commitments gives **1.05% of France's annual GDP per year**, recalculated weekly as that share divided by 52. This is the aggregate of 19 standing treaties in that selected route; each recipient separately pays its own GDP share. A different compatible selection maximises French setup fees at **4.99% of France's GDP**. These two ceilings come from different branch selections and are not presented as one combined route. They exclude focus and domestic-decision setup costs.
- Shared defence can reach `army_org_factor = +0.09` by completing Balanced Forces and Professional Core; both are compatible. This is +9% division organization, not an army damage modifier. In a separate compatible treaty selection, Atlantic Training and NATO Rhine can add `army_org_regain = +0.06` (+6% organization regain). These are different modifiers and should remain separately labelled.
- Per-modifier ceilings include significant continuing cost penalties. For example, compatible long-horizon routes can produce roughly `social_cost_multiplier_modifier = +0.39`, `bureaucracy_cost_multiplier_modifier = +0.35`, and `equipment_cost_multiplier_modifier = +0.20` while party-government bonuses and all valid treaty streams are active. Positive values raise those bills. Each per-modifier ceiling uses its own best compatible branch selection; do not add ceiling rows together as though every row came from one route.

The Soviet Energy Engineering specialization now awards both signatories two `CAT_energy` research bonuses of 50%. The Soviet side receives `energy_gain_multiplier = +0.06` and `education_cost_multiplier_modifier = +0.03`; this adds a 3% education-cost increase on routes that include that accepted treaty. Its weekly share remains 0.05% of Soviet GDP, so the French recurring and setup ceilings above are unchanged. The removed Soviet civilian-productivity penalty is not counted. These totals are source-model route bounds only, not a native engine or multiplayer balance test. The primary balance watch is accumulated signed agreements across multiple governments: the native lifecycle intentionally keeps signed treaty benefits and recurring shares after elections, so many modest agreements can remain active together.

## Decision review and notes

The two new domestic decisions are fully specified at design level with once-only GDP shares, local asset and cap requirements, shared slots, and finite industry research. Their `runtime_guards` now contain explicit native predicates. The existing runtime generator still needs a future mapping for the two decision records and those guard fields before implementation; this is an implementation TODO, not a proposal defect.

The inherited starting-spirit balance, including `COLDWAR_FRA2_franc_stabilisation`, is outside this party-deal revision and is preserved as approved.

## Conclusion

No unsupported modifier key, category alias, GDP payment model, building-slot omission, invalid partner tag, or party-activation defect was found in this review. Keep the implementation TODO visible for the two new decisions. Static source evidence does not establish live-game UI or multiplayer behavior.
