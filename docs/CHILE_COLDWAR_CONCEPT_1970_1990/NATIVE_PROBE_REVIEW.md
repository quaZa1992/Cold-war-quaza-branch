# IMPERIA COLD WAR — Chile 1970 native probe and mechanics review

## Scope and disposition

This review covers `tools/chile_1970/native_probe.py` and a static trace of the Chile focus transaction, programme modifier refresh, building guards, and weekly expense integration. The 184-focus staged static QA reports 21 files, no errors, and `engine_tested: false` in `RUNTIME_STATIC_QA.json`. The tree preview, native donor layout review, and event-art mapping are design/rendering evidence, not a loaded-game result.

The user explicitly chose to keep private profiles on `E:` and skip the game test. The host also has no accessible `E:` runtime root. No profile was prepared, no game process was launched, and no native result is claimed. The current report remains a source review only.

## Harness changes

- The transaction probe now spends from a treasury balance of zero, expects the $3 billion native debit to leave `treasury = -3`, and requires the guarded focus receipt, building level, and extra shared slot to appear. It no longer expects a negative-treasury rejection.
- The slot counter now iterates to 82, covering the installed MD definition of 80 shared slots and the known adjacent 82-slot profile. Its checks use the actual `free_building_slots` trigger.
- The PDC party-change check requires the dynamic modifier to be absent while its earned modifier variables and receipt remain, and the domestic weekly ledger returns to its pre-programme value. Returning to the governing party must restore the programme and weekly fee; replaying its apply helper must not add the reward or fee again.
- Foreign-agreement preview checks now discover both spirit IDs from the current emitted decision helper and idea definitions, rather than embedding fixed spirit IDs in the probe.
- If the runner stops its own HOI4 process after the `COMPLETE` checkpoint, the report records that as expected termination. A completed checkpoint is still required for success.

## Static mechanics trace

- `compile.py` emits each building grant with the additional shared slot before construction. The building trigger separately checks country ownership and control, state ownership and control, native building-level capacity, and shared-slot availability for building types that consume slots. The infrastructure focus still receives its one extra shared slot even though infrastructure does not use shared slots.
- The focus payout checks its real eligibility and one-time receipt before charging treasury, setting the receipt, applying the building, and refreshing programmes. The transaction probe targets the Central Corridor helper, whose staged output shows the $3 billion charge and one-time receipt adjacent to the slot and infrastructure grants.
- Programme refresh rebuilds retained modifier variables from completed-focus receipts. Party-specific dynamic modifiers use the real party trigger, are removed while inactive, and are re-added on return. Weekly charges are first reconstructed from receipts, then subtracted for inactive programmes, so earned modifier variables and receipts persist while the inactive programme contributes neither its modifier nor recurring cost.
- The generated integration adds Chile's weekly ledger into Millennium Dawn's native `additional_expenses_rate`; amounts are expressed in the weekly units used by the MD money system. This establishes the intended source path, while actual tick behavior and debt handling still require an engine run.
- The 36 modifier keys found across approved spirits, focuses, and agreements all have a source match in MD modifier definitions, ideas, dynamic modifiers, or focus rewards. Two project-relevant custom economy keys were followed to readers: `social_cost_multiplier_modifier` is registered in `common/modifier_definitions/money_modifier_definitions.txt` and read by the social expense calculation in `common/scripted_effects/00_money_system.txt`; `imp_sanction_resistance` is registered in `common/modifier_definitions/mdcw_imperia_globalism_modifiers.txt` and read by `common/scripted_effects/imp_sanctions_effects.txt` when scaling the four sanction effects.
- Root reported a correction to the Andean membership guard: it now references the emitted `COLDWAR_CHL_dip_andean_protocol_chl` spirit. The resulting staged triggers contain that membership requirement. Root's latest static validation reports all 21 staged files passing.
- All 17 approved focus-art sprite keys resolve in the current `interface/**/*.gfx` registry, and all approved art source paths exist. The research categories used by the concept (`CAT_industry`, `CAT_computing`, `CAT_surface_ships`, `CAT_aircraft`) each appear in live technology definitions.

## Unverified

The focus tree, costs, negative treasury behavior, building slot increment, programme party-change cycle, diplomacy decision execution, native tooltips, and engine diagnostics have not been tested in HOI4. The foreign probe is prepared to follow the current emitted diplomacy IDs, but was not generated or run. No native screenshot exists. The available preview and donor reviews are not presented as live game captures.

Offline checks passed without touching `E:`: the compiler built all 21 payload files in memory; the transaction and foreign-consent fixture events both passed the project script parser; all 19 transaction checks and 9 foreign checks are unique; and Python parsed the runner source. No compiled fixture or native profile was written. The native game test remains explicitly skipped by the user.
