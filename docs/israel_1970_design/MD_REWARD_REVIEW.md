# Israel 1970 reward and modifier review

Read-only review of the live Israel 1970 reward source against the installed Millennium Dawn references. No reward values were changed.

## Sources and method

- Live Israel reward authoring: `tools/israel_1970/revised_rewards.py` (`SPECS`, `P`, `Q`, and `apply`). The comment now refers to legacy focus gates; the design input has 347 nodes and the current build removes 32 obsolete political-unlock nodes, leaving 315 live focuses as stated in `tools/israel_1970/README.md`.
- Live Israel modifier wiring: `common/scripted_effects/ISR70_effects.txt` (`ISR70_refresh_programmes`, `ISR70_sync_reward_revision`) and `common/dynamic_modifiers/ISR70_dynamic_modifiers.txt` (`ISR70_p0_programme` through `ISR70_p23_programme`). Only the governing party's matching programme is enabled; the daily refresh removes a former governing programme and enables the new one.
- Starting spirits and their defined values: `tools/israel_1970/design_source.json` (`starting_spirits`), materialized in `common/ideas/ISR70_ideas.txt`.
- Installed MD reference files: `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649\common\national_focus\00_generic.txt`, `05_russia.txt`, and `common\scripted_effects\99_SOV_scripted_effects.txt` / `common\dynamic_modifiers\99_SOV_dynamic_modifiers.txt`.
- For a conservative envelope, I sum negative and positive common-focus modifier contributions separately; this avoids allowing an optional positive cost modifier to cancel a negative one in the lower bound. I then add each attainable programme package: institution + finish + one of ea/eb (including its deepen focus) + one of ca/cb (including its deepen focus). The p1 package includes `gahal_coalition`; p3 includes `alignment_balance`, `golda_labour`, `golda_manager`, `golda_housing`, and one of `rabin_cabinet` / `peres_cabinet`, as these completed focuses feed those active programme variables in `ISR70_effects.txt`. The common envelope intentionally counts mutually exclusive common rewards simultaneously and is not an attainable build. Programme ranges use the 20 active party paths and their branch combinations.

## Reference patterns

The installed generic tree's ordinary political rewards include 100–200 political power, about +0.05 stability or war support, one-use technology bonuses usually around +0.25, and 365- or 730-day ideas. It also uses concrete building and state effects, costs, and eligibility gates. The Russia tree's domestic economy path instead uses named dynamic modifiers and explicit `add_to_variable` increments, commonly about +0.01 to +0.05 for research speed, corporate tax, and cycle costs, with several -0.05/-0.10 administrative adjustments. Russia's larger geography and resource base support state-specific resource and industrial packages that do not transfer directly to Israel.

Israel's current pattern fits the smaller 1970 campaign: ordinary focuses grant 50–100 political power, 5–15 interest-group opinion, +0.02 to +0.05 stability, 15–40 experience, and contemporary one- or two-use research bonuses. Construction is state-targeted and funded, usually for one or two levels and with a GDP-based treasury debit of roughly 0.4–1.5%. Programme changes use MD's visible `add_to_variable` tooltip conventions and aggregate through dynamic modifiers rather than issuing repeated generic idea packages.

## Modifier envelope

The following are the largest absolute or strategically relevant sums from all common focus `SPECS` modifiers plus the largest matching active-programme branch. Because the common-focus side includes mutually exclusive alternatives simultaneously, treat these as conservative ceilings. Values use the modifier's native decimal convention (for example, 0.10 is a 10% modifier where the modifier definition is percentage-valued).

| Modifier | Common-focus lower / upper envelope | Active-programme lower / upper | Combined lower / upper envelope |
| --- | ---: | ---: | ---: |
| Bureaucracy cost | -0.40 / +0.05 | -0.20 / 0 | -0.60 / +0.05 |
| Incoming investment cost | -0.55 / 0 | -0.15 / 0 | -0.70 / 0 |
| Social cost | -0.15 / 0 | -0.20 / 0 | -0.35 / 0 |
| Health cost | -0.10 / 0 | -0.05 / 0 | -0.15 / 0 |
| Supply consumption | -0.18 / 0 | -0.15 / 0 | -0.33 / 0 |
| Army training time | -0.05 / 0 | -0.05 / 0 | -0.10 / 0 |
| Industrial capacity (factories) | 0 / +0.05 | 0 / +0.08 (includes p3 Golda manager) | 0 / +0.13 |
| Army defence | 0 / +0.26 | 0 / +0.05 | 0 / +0.31 |
| Army organization | 0 / +0.18 | 0 / +0.05 | 0 / +0.23 |
| Mobilization speed | 0 / +0.40 | 0 / +0.25 | 0 / +0.65 |
| Political power factor | 0 / +0.20 | 0 / +0.15 (p1 Gahal brings p1 to +0.10) | 0 / +0.35 |
| Research speed | 0 / +0.08 | 0 / +0.04 | 0 / +0.12 |
| Productivity growth | 0 / +0.20 | 0 / +0.15 (includes p3 Golda labour) | 0 / +0.35 |
| Infrastructure construction speed | 0 / +0.25 | 0 / +0.15 | 0 / +0.40 |
| Office construction speed | 0 / +0.35 | 0 / +0.15 | 0 / +0.50 |
| Foreign influence defence | 0 / +0.45 | 0 / +0.10 | 0 / +0.55 |

The widest negative cost stack in this deliberately overinclusive envelope is -0.70 for incoming investment; bureaucracy's lower envelope is -0.60 because it includes both negative reductions and the positive +0.05 cost in `territory_administration`. The corresponding upper envelope is +0.05, preserving that optional penalty instead of netting it away. The largest combat/readiness number is +0.65 mobilization speed. These figures are static plausibility bounds, not a gameplay balance verdict or a claim that the common choices can all be reached together. The live focus graph's exclusions reduce actual combinations.

`steady_budget` in `revised_rewards.py` assigns `interest_rate_multiplier_modifier = -0.50`. This is not a multiplicative -50% interest reduction. `common/modifier_definitions/money_modifier_definitions.txt` defines the field as `value_type = number`; `common/scripted_effects/00_money_system.txt`, `calculate_interest_rate`, adds it directly to `pre_clamp_interest_rate`, whose result is clamped to 0.8–50. It therefore subtracts 0.50 percentage points from the calculated interest rate. Other MD focuses use changes such as -0.25, so -0.50 is a meaningful but bounded credit improvement, not an invalid value. No interest-rate nerf is supported by this check.

## Starting spirits and replacements

The starting package is not a freely stackable set of permanent additions. The revised focus effects explicitly swap or remove several spirits:

- `ISR70_unity` starts at stability +0.04 and political power factor -0.05. `unity_cabinet` or `narrow_cabinet` removes it; those cabinet rewards then provide +0.05 or +0.10 political-power factor, with unity also adding +0.05 stability.
- `ISR70_citizen_army` starts at mobilization +0.15 and army organization +0.03. `reserve_system` removes it and grants the revised reserve spirit, whose modifiers are provided by the focus programme.
- `ISR70_histadrut` starts at industrial-complex construction speed +0.05 and social cost -0.03. Its treatment in the revised campaign is a distinct starting idea; no generic focus effect swaps it out.
- `ISR70_attrition` starts at war support +0.03, mobilization +0.05, personnel cost +0.08. `ceasefire` and `egypt_peace` remove it; `armed_stalemate` explicitly retains the burden.
- `ISR70_embargo` starts at arms-factory construction speed -0.05. The local aircraft programme sets a flag, and `air_maintenance` removes the spirit when that programme exists.
- `ISR70_absorption` starts at population growth +0.05 and social cost +0.05. `absorption_reform` swaps it for `ISR70_integrated_immigration`, removing the surcharge while retaining population growth.
- `ISR70_ambiguity` starts at foreign-influence defence +0.05. `keep_ambiguity` or `nuclear_transparency` removes it before granting its separate policy reward.

The one-time revision synchronizer restores programme modifier totals for completed focuses in existing 1970 saves, then removes the legacy intelligence idea and superseded spirits where applicable. It deliberately does not replay one-time factory, cash, or research grants.

## Findings and recommendations

The static envelope contains no cost modifier at or below -1.00, but that threshold alone says nothing about overall balance. The most unusual positive cost is p15's patronage route: `p15_eb` and `p15_cb` each add +0.05 `corruption_cost_factor`, a combined +0.10 for that programme choice. Both focus descriptions explicitly identify the corruption cost as the price of privileged concessions and patronage networks, so this is an intentional trade-off rather than a silent error.

The p3 Alignment extension adds more programme value than the base p3 package alone: `alignment_balance` adds +0.05 political power factor, `golda_labour` adds +0.05 factory max efficiency and +0.10 productivity growth, `golda_manager` adds +0.05 factory industrial capacity, and `golda_housing` adds -0.05 social cost. The cabinet alternatives add either `rabin_cabinet`'s -0.05 bureaucracy cost or `peres_cabinet`'s +0.10 arms-factory construction speed. These are included in the active p3 range. p1's `gahal_coalition` adds +0.05 political power factor; included in p1's range. Their effects are also re-derived by the reward synchronizer from completed-focus IDs.

`territory_administration` grants `resistance_damage_to_garrison = -0.15` while adding +0.05 bureaucracy cost, an explicitly paid administrative trade-off. `import_substitution` and `export_specialization` are mutually exclusive because their exposure/resilience effects point in opposite directions. `steady_budget` and `development_budget` are mutually exclusive; the former trades the development package for the 0.50 percentage-point interest reduction.

I did not find a broken modifier ID in the reviewed authored reward table. The Israel programme variables are registered in `ISR70_dynamic_modifiers.txt` and reset/rebuilt by the scripted-effect synchronizer; named persistent shared rewards become idea definitions in `ISR70_ideas.txt`. Static inspection cannot establish engine loading or tooltip execution.
