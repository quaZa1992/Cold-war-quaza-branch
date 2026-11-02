IMPERIA COLD WAR

Retained design-stage source review. This is historical/design evidence, not an engine execution report.

# France armaments concept — final mechanics review

**Target:** `COLDWAR_FRA_POLITICS_CONCEPT.json`, revision 4, concept-only.  
**SHA-256:** `F90E6193464FFCE880D3A6BA049568F779CCB0AB8111ACB252C34118CDBDC780`  
**Scope:** 48 new armaments focuses across 12 party programmes; static source audit of effects and consumers. No game-engine or live-tooltip testing was performed.

## Findings

1. **Rename and explain `equipment_cost_multiplier_modifier` as land-equipment upkeep.** In the local consumer, `00_money_system.txt:2802–3029` accumulates deployed and stockpiled *land* equipment upkeep (including land equipment classes), then applies the equipment multiplier at line 3217 before the separate Navy accounting section begins. Naval and air personnel use their own multipliers. This is not factory input/procurement price, and does not lower naval or aircraft upkeep. Several proposed `+/-` effects can read as generic equipment cost; localize the modifier label and focus explanation as “land-equipment upkeep” (or equivalent). Positive values raise that recurring expense; negative values lower it. The concept’s “Equipment Life Extension,” “Maintenance Cost Audits,” “Lifetime Equipment Support,” etc. are mechanically plausible as upkeep reductions but should make that scope explicit in the visible reward.

2. **No armaments effect appears to be an army-personnel wage modifier.** New armament-node modifiers do not include `army_personnel_cost_multiplier_modifier`. `equipment_cost_multiplier_modifier` changes the land equipment upkeep accumulator above; do not describe it as factory-worker wages or military payroll.

3. **Production and capacity mechanics have real local readers.** `00_productivity_effects.txt:171,201` reads `modifier@industrial_capacity_factory` and `modifier@industrial_capacity_dockyard` in separate military-factory and dockyard output calculations. These change output per existing factory/dockyard; they do not add buildings or slots. `00_ledger_scripted_effects.txt:99,109` separately includes those capacity terms in effective factory counts for ledger/output accounting. The project builder `99_investment_scripted_effects.txt:266–269` maps project types 1/2/3 to industrial-complex/arms-factory/dockyard construction speed, so the respective `production_speed_*_factor` effects concern construction projects, not production-line throughput. The production-efficiency maximum and gain fields are distinct production-line effects; negative gain values trade away the rate of gaining efficiency, while a positive maximum raises its ceiling.

4. **Integration needs two France modifier mappings.** The shared modifier definitions declare `equipment_cost_multiplier_modifier` as a country percentage (`money_modifier_definitions.txt:44–49`); the cost consumer is above. But the existing France wrapper file `common/dynamic_modifiers/99_FRA_dynamic_modifiers.txt` currently has no `equipment_cost_multiplier_modifier` mapping and no `production_speed_dockyard_factor` mapping (searched the complete file). Before these proposed effects can work through party-owned dynamic modifiers, add and verify those fields in the relevant French dynamic-modifier blocks. France already maps factory/dockyard output, arms-factory construction speed, factory efficiency maximum/gain and the concept’s education/corporate/social cost fields there (for example lines 33–72, 378–392, 485–497, 587–592, 675–677). Shared country cost definitions exist for education, social and corporate-tax fields at `money_modifier_definitions.txt:65–107,212+`; confirm the intended country wrapper points at the correct variables when implementation is prepared. This is an integration prerequisite, not a claim that this concept-only file is already executable.

## Compatible programme envelope

The revision-4 group `variants` data reports complete compatible focus-route sums, not a raw sum of incompatible exclusive alternatives. It yields 96 Gaullist, 64 Orthodox Gaullist, 64 liberal, 128 centre, 128 radical, 96 socialist, 128 communist, 32 Old Guard, 64 PSU, 64 ecology, 64 CID and 64 National variants. Across those compatible routes, the armaments-sensitive modifier envelope (all applicable programme nodes, including the existing compatible route effects represented by the concept) is:

| Party | Factory capacity | Dockyard capacity | Arms-factory project speed | Dockyard project speed | Efficiency gain | Efficiency cap | Land-equipment upkeep |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gaullist | −2.5%…+7.5% | 0…+5% | 0…+10% | 0…+5% | −2.5%…+20% | +5%…+12.5% | 0…+7.5% |
| Orthodox Gaullist | 0…+7.5% | 0…+10% | −5%…+7.5% | 0…+7.5% | −7.5%…+4% | 0…+10% | 0…+5% |
| Liberal | +2.5%…+7.5% | 0 | 0…+7.5% | 0 | +5%…+7.5% | −2.5%…+5% | −7.5%…+5% |
| Centre | −2.5%…+5% | 0…+7.5% | 0…+7.5% | 0…+7.5% | +5%…+10% | 0 | 0 |
| Radical | 0…+7.5% | 0 | −5%…+7.5% | 0 | −2.5%…+10% | 0…+5% | −5%…+2.5% |
| Socialist | −2.5%…+7.5% | 0 | 0…+7.5% | 0 | +7.5%…+17.5% | +2.5%…+5% | −7.5%…0 |
| Communist | +2.5%…+7.5% | 0 | −5%…+7.5% | 0 | −5%…+15% | +2.5%…+15% | −2.5%…0 |
| Old Guard | −5%…+10% | 0 | 0…+12.5% | 0 | −11.5%…+17.5% | +5%…+20% | −10%…+7.5% |
| PSU | −5%…0 | 0 | −5%…0 | 0 | +2.5%…+27.5% | −5%…+5% | −5%…0 |
| Ecology | −7.5%…+5% | 0 | −2.5%…0 | 0 | 0…+5% | 0…+2.5% | −2.5% |
| CID | −5%…+5% | 0 | 0…+5% | 0 | +2.5%…+7.5% | 0…+5% | −7.5%…−2.5% |
| National | −2.5%…+7.5% | 0 | −2.5%…+10% | 0 | −2.5%…0 | +2.5%…+5% | −7.5%…+7.5% |

The route table indicates distinct industrial choices rather than one duplicated bonus stack. The strongest efficiency-gain envelope is PSU at +27.5%, and the largest maximum-efficiency envelope is Old Guard at +20%; these arise from compatible route stacking with prior programme effects and should remain visible in balance review. The armaments pairs themselves generally trade one production emphasis for another. Some follow-ups impose an explicit opportunity cost, e.g. dockyard capacity paired with lower factory capacity, factory investment paired with reduced growth, or repair/upkeep savings paired with lower factory capacity. These are credible trade-offs, not new worker-wage penalties.

The variant totals do not add the 1970 history/startup active party modifiers or a simultaneously active bilateral offer. France history calls `FRA_update_party_programmes = yes` at `history/countries/FRA - France.txt:2729`; its startup modifier must be added for a true start-to-finish numeric route total once the final party programme-to-modifier mapping is fixed. Do not treat the table as including that baseline. Offers are temporary and consent-gated. The offer catalogue allows at most one timed compact at a time; where a chosen offer adds `production_factory_efficiency_gain_factor` or `production_factory_max_efficiency_factor`, it adds at most +2.5 percentage points for its stated 365-day term. Include that overlay when reviewing a particular route’s transient peak. The concept states the one-off research bonuses use one 50% award on one target; those are outside this production-modifier audit.

## Verification limits

This confirms source-level consumers and design-data arithmetic only. It does not prove the later generated focus code applies, removes, previews or displays these values correctly; party dynamic-modifier ownership, save/load behavior and native hovers still require integration review and an in-game test. No game files were changed for this audit.


## Bounded refresh — 23 October 2026

Rechecked the current revision-4 concept after the final wording pass. Its SHA-256 is now `F90E6193464FFCE880D3A6BA049568F779CCB0AB8111ACB252C34118CDBDC780`. The modifier label is `Weekly Land Equipment Upkeep`; each armament description that applies this modifier now identifies the cost as land-equipment upkeep/support, and the effect list contains no army personnel wage modifier. Civilian conversion rows explicitly describe industrial-complex construction, while the sampled Gaullist, Orthodox Gaullist and Radical descriptions distinguish factory output from facility construction. The 48 armament focus IDs still resolve as four per party across twelve parties. This refresh was limited to wording, scope labels and hash confirmation; modifier values, focus IDs/targets, DLC/project guards and coordinates were left as supplied. The report’s earlier wrapper-mapping requirements and startup-baseline caveat remain applicable.

