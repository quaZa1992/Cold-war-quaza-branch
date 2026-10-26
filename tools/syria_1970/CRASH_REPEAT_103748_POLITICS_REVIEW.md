# Independent politics-effect review

Reviewed 20 October 2026 against the repeated `hoi4_20261019_103748` crash. The review used the installed `mdcw-modifier-audit` skill and read the dump, script and global-chain reports. No loaded game files were changed by this reviewer. This report was added after the parent agent repaired and regenerated the Syrian helper.

## Evidence and bounded repair

Both dumps identify the same near-null read; the retained `Politics will change:` string, null `CIdeologyGroup` RTTI and `CScriptedEffectTemplate` RTTI narrow the failure to native politics-effect presentation. They do not recover a script-helper name. Therefore the Syrian omission is a concrete matching defect and strong repair candidate, rather than an independently proven unique source of the crash.

Before repair, `COLDWAR_SYR_accept_national_pact` omitted `ruling_party` from an election-only `set_politics` effect. The installed engine's `documentation/effects_documentation.md:7526` describes `set_politics` as country-scoped and lists `ruling_party` as the new ruling ideology key. Native MD supplies `ruling_party = ROOT` when preserving a country's governing outlook: see `common/scripted_effects/00_MD_politicsview_scripted_effects.txt:2168` (`set_elections_with_frequency`) and `:2332` (`enable_elections_with_no_leader_change`). Both surround the effect with `no_leader_change`.

The regenerated Syrian helper at `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:74` now follows that native form:

```
set_country_flag = no_leader_change
set_politics = { ruling_party = ROOT elections_allowed = yes election_frequency = 48 }
clr_country_flag = no_leader_change
```

Canonical source is `tools/syria_1970/politics.py:408`. The repair supplies a resolvable country reference and retains the intended 48-month elections. It must not substitute MD's numeric party-array index, such as `7`, for the engine ideology/country argument. Existing legalization, party-name refresh and earned-programme refresh remain after this effect.

## Scope and presentation callers

The helper has two emitted invocations, both in country events for Syria:

- `events/COLDWAR_SYR_politics_events.txt:242`: `COLDWAR_SYR_POL.4.option_a`. Event trigger and the execution condition both require `original_tag = SYR` and the 1970 scenario. The helper runs inside `hidden_effect` without another country/state scope. `ROOT` consequently remains the Syrian recipient.
- `events/COLDWAR_SYR_politics_events.txt:1572`: `COLDWAR_SYR_POL.34.option_a`. The same Syrian/scenario conditions apply, with MD governing-party slot `22` additionally required. The call likewise retains the recipient's root country.

Both options have authored outcome localization; their explicit `effect_tooltip` blocks preview their respective temporary transition/disruption idea and do not invoke the pact helper. Hiding the original broken effect was not a sufficient repair: the native effect itself is now complete. There is no new leader-retirement or leader-creation effect in the pact.

## Global alternative-candidate scan

A comment/string-aware token scan of all `.txt` files below loaded `common`, `events` and `history` found **838 `set_politics` blocks**. Before the Syrian repair, exactly three omitted `ruling_party`: the Syrian pact and two Spanish transition helpers. All explicit values except one matched the five declared engine ideology groups (`democratic`, `communism`, `fascism`, `neutrality`, `nationalist`) or native country scopes (`ROOT`, `THIS`). No numeric party-slot or unresolved event-target argument was found in those blocks.

Remaining separate candidates are:

| Source | Observation | Context and limitation |
| --- | --- | --- |
| `common/scripted_effects/SPR_1970_scripted_effects.txt:775` | `SPR_1970_hold_first_free_elections` lacks `ruling_party`. | Called through hidden event `SPR_1970.109` by the deep Spanish transition focus at y=20. Historical AI preference delays it until 1977; this is an AI preference, not a hard date prerequisite. No supplied evidence connects it to the June 1970 Syrian interaction. |
| Same file, `:870` | `SPR_1970_install_felipe_gonzalez_government` lacks `ruling_party`. | Called through hidden event `SPR_1970.120` by the subsequent Spanish democracy focus at y=26, with a historical AI preference for 1982. No supplied evidence connects it to the crash. |
| `events/Iran.txt:3463` | Hidden `axis_of_resistance_events.39` uses `Communism`, whereas the declared key is lowercase `communism`; the following party effect repeats the uppercase value. | Triggered by the modern Iranian Iraqi-replacement focus (`common/national_focus/05_iran.txt:11264`) after the NTR/IRS context has formed. Identifier case handling was not engine-tested; treat this as a source spelling inconsistency, not a proven invalid lookup or current Syrian crash cause. The supplied error log reports no ideology error. |

After regeneration the same scan still finds 838 blocks, with Syria moved from the omitted group into the native `ROOT` group. The remaining two Spanish omissions and the Iranian case discrepancy were not modified by this bounded Syrian repair.

## Independent verification

A read-only parse/assertion check of the emitted scripts passed: the pact contains `ROOT`, enables elections, retains frequency `48`, and has the native flag immediately before and after `set_politics`; both event calls remain under the correct hidden execution guards; neither explicit preview calls the pact; no nested country/state scope changes `ROOT` at the call sites. These are source checks only. They do not reproduce the crash or establish its absence in HOI4.

The required live verification remains: restart HOI4 to load the changed scripts, inspect the relevant Syrian political decisions and event options, and advance beyond both June 1 and June 13. A continued crash should be compared to the exact native instruction and RTTI signature rather than attributed to the last logged UN/Algerian/debt action.

## Addendum: calibrated template metadata supports the exact Syrian helper

A subsequent read-only source-attribution examination materially strengthens the helper identification above. `inspect_dump_source_attribution.py` decodes captured `CScriptedEffectTemplate` objects and infers source metadata fields by comparison with captured short names and neighboring declarations. These field meanings are calibrated inferences, not public debugger symbols.

The first dump captures the inline name `set_leader_CSB`, associated with a source-ID field of `3580`; the second captures `set_leader_DAG`, associated with `3586`. Ordinal, case-sensitive sorting by each filename (`key=lambda path: path.name`) puts their current files at indices `258` and `264`. Both independently produce the same source-ID offset, **3322**. A first saved version of the diagnostic incorrectly sorted Windows `Path` objects, whose default comparison folds case; this moved `COL_political_leaders.txt` relative to the `COLDWAR` files and made several local mappings inconsistent. Explicit filename sorting resolves the discrepancy, including the independent neighboring source matches. This correction is necessary when reproducing the result.

The fault-context `R12` template in **both** dumps then has the same metadata:

| Inferred field | Captured value / calibrated match |
| --- | --- |
| Source ID (`+0x2c`) | `3569` |
| Source declaration line (`+0x30`) | `74` |
| Name length (`+0x70`) | `32` |
| Calibrated file index | `3569 - 3322 = 247` |
| Current file at ordinal index 247 | `COLDWAR_SYR_politics_effects.txt` |
| Declaration at line 74 with length 32 | `COLDWAR_SYR_accept_national_pact` |

This combination resolves the other line/length candidate (`reset_democratic_coalition_ideas` in `00_ideology_drifts.txt`) to a different file. It also consistently identifies neighboring foreign-operation, Syrian programme-initialization and Turkish roster helpers. Across the two dumps, **11 of 12 captured templates** match complete current source declarations under this calibration; the remaining older focus-reward template maps to the expected file but its old declaration line no longer matches the changed generated content. That mismatch is retained rather than forced into a name.

An independent invocation rebuilt the declaration inventory with explicit ordinal filename sorting and asserted the calibrated pact identity for both dumps; it passed. The Syrian name bytes themselves remain outside captured heap memory and must not be reported as a literal string recovered from the dump. File enumeration and current source content may have changed between crashes and analysis, and the metadata layout is inferred. Nevertheless, two independent inline anchors, identical fault-template metadata in both runs and multiple neighboring declaration matches make attribution to the Syrian pact **strongly supported**. This supersedes the earlier statement that the template could not be associated with a helper; it still does not establish that the repaired build has passed a live engine run.
