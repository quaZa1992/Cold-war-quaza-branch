IMPERIA COLD WAR

# France 1970: tangible trade-off review

## Scope

Bounded review of the 11 authorised replacements applied by `tools/france_1970_runtime/balance_revision.py` after the immutable party-revision snapshot. All replacement keys below are present as native/current MD idea modifiers or are consumed by the MD money system. Party/focus effects and signed treaty sides were checked in the compiled design and emitted definitions. This review does not estimate total in-game cash deltas or claim engine balance.

## Replacement effects and fit

| Focus | New signed effect | Mechanical interpretation and fit |
|---|---|---|
| Shared Components (`pooled_armour`) | `production_factory_efficiency_gain_factor = -0.08`; existing `equipment_cost_multiplier_modifier = -0.05` remains | Eight percent lower production-line efficiency growth represents slower adaptation. The existing five percent equipment-cost reduction remains the gain. This is a real production trade-off instead of an influence number. |
| Jaguar Coordination (`jaguar_doctrine`) | `airforce_personnel_cost_multiplier_modifier = +0.05` | Adds five percent to the national air personnel cost multiplier. Existing air-training experience and fuel-consumption improvements remain. |
| Escort Fleet (`escort_navy`) | `navy_personnel_cost_multiplier_modifier = +0.05` | Adds five percent to national naval personnel expenses. The focus retains its naval base, finite naval research and lower accident chance. |
| Open Computing (`open_computers`) | `corporate_tax_income_multiplier_modifier = -0.03` | Lowers the corporate-tax multiplier by three percent while retaining electronics research and factory-efficiency growth. The effect changes the corporate-tax stream, not all national income by three percent. |
| Market Protection (`fn_protection`) | `research_speed_factor = -0.03` | Slows all research by three percent while the right-party programme is active. Existing civilian-factory productivity loss remains, so the narrative names both costs. |
| Atlantic Electronics (`atlantic_liberal`, French signatory) | `corporate_tax_income_multiplier_modifier = -0.03` | Reduces French corporate-tax proceeds by three percent under the multiplier. French office productivity and electronics research remain. The US side retains its separate approved modifier. |
| Soviet Industrial Partnership (`soviet_friendship`, French signatory) | `production_speed_arms_factory_factor = -0.05` | Reduces the construction speed of arms factories by five percent, not equipment-line output. The French industrial-complex construction bonus remains, as do both countries' approved assets. |
| Energy Engineering (`pcf_energy_contract`, French signatory) | `education_cost_multiplier_modifier = +0.04` | Raises French education expenses by four percent; the Soviet side already has its distinct three percent education-cost modifier. Both sides keep two 50% energy research bonuses. |
| Aviation Export (`fn_export`, French signatory) | `airforce_personnel_cost_multiplier_modifier = +0.04` | Raises the French national air personnel cost multiplier by four percent alongside the French corporate-tax gain. Argentina's existing signatory idea separately retains its four percent air personnel cost. |
| Atlantic Training (`atlantic_training`, French signatory) | `army_personnel_cost_multiplier_modifier = +0.04` | Raises French national army personnel expenses by four percent alongside the organisation-regain and air-training benefits. The US side is unchanged. |
| Iran Energy (`iran_energy`, French signatory) | `corporate_tax_income_multiplier_modifier = -0.03` | Reduces French corporate-tax proceeds by three percent alongside energy-generation gain. Iran's separate productivity, bureaucracy cost and fiscal terms are unchanged. |

The new modifiers are supported by the current source. `production_factory_efficiency_gain_factor` appears in MD country ideas, including `common/ideas/05_Australia.txt:287` and `05_china.txt:246`. `production_speed_arms_factory_factor` appears in `common/ideas/!_generic_faction_goals.txt:6`, Australia and France. The three personnel-cost keys are registered as country percentage modifiers in `common/modifier_definitions/money_modifier_definitions.txt:23-37`; `00_money_system.txt:3240-3242` forms `1 + modifier` and multiplies the matching service cost. Education cost uses the same cost-multiplier pattern at `00_money_system.txt:3440`. Corporate-tax income uses `1 + corporate_tax_income_multiplier_modifier` in `00_money_system.txt:442` and `:755`. `research_speed_factor` is used by current MD ideas, including China and Armenia.

## Trade-off scale and stacking

Positive personnel and education cost values increase the respective whole-country expense line. They do not bill only the named programme's staff. Actual currency impact depends on each country's present force, education bill, other modifiers and GDP-calculation state. Negative corporate-tax values reduce that income stream, not GDP directly. The new values are modest per source, but the permanent/signed lifetimes mean they can coexist after successive governments: Shared Components' efficiency-growth penalty can sit beside Open Computing's growth bonus; Jaguar's five percent air personnel cost can coexist with the signed four percent French Aviation Export cost; and the three French corporate-tax penalties from Open Computing, Atlantic Electronics and Iran Energy can coexist. Aviation Export's existing French five percent corporate-tax gain offsets part of that tax subset. These are compatible source sums, not a whole-economy net estimate.

The five non-offer changes are stored in their group modifier pools. `fn_protection` belongs to the right-party pool and deactivates when that party leaves office; its earned receipt keeps the value for a later return. Shared defence and economy pool values are not party-gated. Bilateral France-side idea modifiers remain while the agreement's pair, peace, sanction and actual parent/membership conditions are valid, even after the original proposing party leaves office. The accepted agreement values therefore persist by design.

## Historical anchor and wording check

The French National Assembly's retrospective 2014 defence budget report describes the Jaguar as a successful Franco-British programme despite initial cooperation difficulties, including coordination across national industries, cost distortions from equal industrial work shares, and shifting aircraft requirements. It dates first flight to 1968 and service entry to 1973. This is a historical analogue supporting a modest shared-specifications/production-adaptation trade-off, not evidence that the project failed or a precise measure of 1970 production efficiency: [Assemblée nationale, Rapport sur le projet de loi de finances pour 2014, Annexe 10, sections on Jaguar cooperation](https://www.assemblee-nationale.fr/14/budget/plf2014/b1428-tIII-a10.asp#3301).

The descriptions generally identify the new practical cost. Four personnel-cost descriptions name instructor, patrol, liaison or technical staffing while the modifier affects the whole national service-cost multiplier; the numeric native effect must remain visible so the country-wide scale is not obscured. The compiled FN Export recipient idea also increases Argentina's air personnel cost by four percent, separate from the new French-side increase. The native offer preview should expose both signatory ideas.

## Migration note

The core party-revision migration rebuilds non-offer modifier pools from existing `COLDWAR_FRA2_earned_*` flags, replacing old influence values with the new modifiers without repeating GDP costs, assets, finite research or experience. Two existing signed agreements reuse their idea IDs: Atlantic Training gains the French army-personnel-cost modifier, and Iran Energy gains the French corporate-tax modifier. Existing accepted treaties therefore inherit those continuing terms when the revised ideas refresh; no setup payments or one-time rewards replay. This behavior is consistent with the authorized balance change and permanent agreement contract, but it should remain explicit in release notes and save-transition QA.

## Conclusion

All 11 replacements have supported mechanics and concrete economic, industrial or research consequences. No unsupported key was found. The primary watch is whole-country modifier accumulation across agreements that persist through elections. Actual rendered hovers, engine application and multiplayer impact remain for root-owned native testing.