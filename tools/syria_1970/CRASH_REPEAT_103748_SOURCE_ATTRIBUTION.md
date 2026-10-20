# Calibrated source attribution for the repeated crash

Read-only follow-up to `CRASH_REPEAT_103748_DUMP.md`. This analysis uses the two supplied minidumps and the local script inventory. No game was launched, no network download was used, and no loaded game script was edited by this investigation.

## Result

The `CScriptedEffectTemplate` object held in **R12 in both crashes maps to `COLDWAR_SYR_accept_national_pact`, declared at line 74 of `common/scripted_effects/COLDWAR_SYR_politics_effects.txt`**. This is a calibrated metadata attribution, not a claim that the missing heap string was captured.

The dump already identified the null ideology object and the live `Politics will change:` effect-description string. The new metadata attribution ties that native description path to the national-pact template. Before repair, its first native politics effect omitted `ruling_party`; the canonical repair supplies native MD's `ruling_party = ROOT` and leader-change guard. The declaration remains on line 74 after that repair.

## Method and independent calibration

The captured object has the installed executable's `CScriptedEffectTemplate` vtable. Scanning only captured memory finds six objects with that vtable in each dump. At object offsets `+0x2c` and `+0x30` are two 32-bit fields; at `+0x60` is a string with length/capacity at `+0x70`/`+0x78`.

Two short strings are stored inline, so their exact names survive independently of any script inference:

| Dump | Captured inline name | Field +0x2c | Field +0x30 | Source file | Sorted file index |
| --- | --- | ---: | ---: | --- | ---: |
| 100834 | `set_leader_CSB` | 3580 | 1 | `CSB_political_leaders.txt` | 258 |
| 103748 | `set_leader_DAG` | 3586 | 1 | `DAG_political_leaders.txt` | 264 |

Each named source declaration is on line 1. Both independently give the same offset between the file-id field and the **case-sensitive ordinal filename order** of the local scripted-effect-file index: **3322**. The diagnostic uses `sorted(paths, key=lambda path: path.name)` explicitly. This identifies the first field as the source-file identifier within this inventory, and the second as a source-line value. It also confirms that the string metadata belongs to the template name, rather than a filename.

Applying that calibration to other captured objects gives multiple independent, consistent source matches:

| Source id | Sorted index | Source file | Captured line / name length | Matching declaration |
| ---: | ---: | --- | --- | --- |
| 3567 | 245 | `COLDWAR_SYR_focus_rewards.txt` | 9335 / 40 | `COLDWAR_SYR_limited_war_review_implement` |
| 3568 | 246 | `COLDWAR_SYR_foreign_effects.txt` | 36 / 34 | `COLDWAR_SYR_update_operation_costs` |
| **3569** | **247** | **`COLDWAR_SYR_politics_effects.txt`** | **74 / 32** | **`COLDWAR_SYR_accept_national_pact`** |
| 3570 | 248 | `COLDWAR_SYR_programme_effects.txt` | 2 / 42 | `COLDWAR_SYR_initialize_programme_variables` |
| 3570 | 248 | `COLDWAR_SYR_programme_effects.txt` | 3400 / 38 | `COLDWAR_SYR_recompute_starting_spirits` |
| 3570 | 248 | `COLDWAR_SYR_programme_effects.txt` | 3658 / 22 | `COLDWAR_SYR_initialize` |
| 3572 | 250 | `COLDWAR_TUR_1970_regional_effects.txt` | 3 / 31 | `COLDWAR_TUR_1970_refresh_roster` |
| 3572 | 250 | `COLDWAR_TUR_1970_regional_effects.txt` | 715 / 27 | `COLDWAR_TUR_1970_initialize` |

The foreign and Turkish objects are from the earlier dump; the programme and line-9335 reward objects are from the repeated dump. All map through the same offset. The older reward object instead reports line 9263 / length 42, which no longer matches the current generated reward source after the intervening changes; it is retained as an unmatched declaration rather than relabeled.

An independent review caught a reproducibility error in the initially saved diagnostic: it used `sorted(Path objects)`, which applies Windows casefolded ordering, whereas the original inventory calculation used ordinal filename ordering. `COL_political_leaders.txt` then moved ahead of `COLDWAR_*`, shifting the Syria/Turkey group by one while leaving the CSB/DAG anchors unchanged. The saved script and retained JSON have been corrected. The script now rejects any mapped file that contradicts captured line/name-length candidates instead of silently emitting a null declaration. The corrected output validates **5 of 6** declarations in the earlier dump (the changed old reward line is unmatched) and **all 6** in the repeated dump, including both R12 objects.

There is only one top-level declaration on line 74 in the calibrated politics source. If the source-file field is ignored, `reset_democratic_coalition_ideas` in `00_ideology_drifts.txt` also has line 74 and a 32-character name. The independent file-id calibration excludes that otherwise ambiguous candidate.

## The two active objects

| Dump | R12 address | Source-id field | Line field | String length / capacity |
| --- | --- | ---: | ---: | --- |
| 100834 | `0x2237886e230` | 3569 | 74 | 32 / 47 |
| 103748 | `0x2640d210bb0` | 3569 | 74 | 32 / 47 |

The heap pointer holding each long template name is outside captured memory. Neither dump contains a literal `COLDWAR_SYR_` string in its captured memory regions. Exact name bytes therefore must not be presented as recovered. Attribution follows the calibrated file/line metadata plus source declaration and matching name length.

## Tooltip visibility and remaining limits

The installed engine documentation describes `hidden_effect` as an effect not shown in tooltips and `effect_tooltip` as showing only the effect description. Current Syrian event-option callers place pact execution inside `hidden_effect` and preview only the material timed idea. That layout does not explain which UI element caused this particular native template expansion; the UI origin and complete caller context were not preserved as readable identifiers.

Consequently, it would be unjustified to claim that every hidden native effect is always described, or to identify the exact button hovered. It is nevertheless incorrect to exclude this template from the crash investigation solely because its current event callers are hidden: both fault contexts retain its calibrated source metadata and a politics-description string. Repairing its incomplete native effect is warranted independently of hiding it.

This investigation establishes the repeated native fault signature and strongly attributes the expanded template. **It does not establish that the repaired game now runs without crashing.** That requires a new engine run with the regenerated files, preferably including the same tooltips and advancing beyond the supplied saves' failure dates.

## Reproduction

Run `tools/syria_1970/inspect_dump_source_attribution.py --output tools/syria_1970/dump_source_attribution.json` using the project's Python runtime. The script imports the existing read-only minidump parser and writes only its requested diagnostic output. The retained JSON includes every captured template, every same-line/name-length source candidate, literal-name calibrations, calibrated file mappings, and unmatched declarations.

The mapping is specific to the supplied dumps, this executable, and the inspected script inventory. Do not assume the numeric field offsets or the offset 3322 apply to another engine build or a changed file inventory without recalibration.
