# COLDWAR North Vietnam, 1970–1990

The approved national tree is installed as `COLDWAR_VIE_1970_focus`. Start a **new 1970 campaign as North Vietnam (VIE)** with this mod and its Millennium Dawn dependencies enabled. The country history selects this tree; the generic-tree fallback excludes it. The 2000 country-history section is preserved. Existing saves are not a verified migration target.

## Installed content

- 307 focuses in 18 programmes. The whole-tree reward revision reviews all 239 original and 68 campaign focuses, preserves their IDs, and provides 55 reciprocal exclusive pairs. `reward_rework.json` records the later user-authorized replacement values and the few explicit graph corrections.
- Nine political programmes: Le Duan, Truong Chinh, Nguyen Van Linh, alternate Vo Van Kiet, Fatherland Front, Democratic Party, Socialist Party, VNQDD and a provisional military council.
- Common state/outlook, industry, agriculture, armed forces, reunification and diplomatic branches, plus guerrilla warfare, Cambodian campaigns and Chinese frontier policy.
- Six starting spirit families with staged recovery, plus six later crisis spirits. Historical and alternative policies retain their approved benefits and costs.
- 78 substantive decisions, including 22 recipient-approved foreign invitations. Separate deferred-project categories contain 307 conditional retry entries; these are recovery controls rather than additional policy decisions.
- 16 physical construction rewards: one paid Hanoi rehabilitation completes a civilian complex, and fifteen other projects use ordinary construction. The old later Hanoi complex grant is replaced, preventing a duplicate. The northern armament-workshop project now creates a military-factory construction project.
- English localization, native MD focus art and shine registration, four additional historical portraits, and native MD/Imperia political integration. New content identifiers use `COLDWAR_VIE_`.

Political islands occupy rows 0–9; common branches occupy rows 13–22. Chinh's schools and economic-adviser choice now occupies row 1, so the 70-day opening plus one 70-day institution fits his short historical tenure. Aircrew Training branches from the common coastal survey at (32,20), independently of dockyard repairs. Linh's two capital approaches follow either political settlement and are directly exclusive. Campaign islands start at (52,13), (60,13) and (68,13), extending to row 26. The continuous panel and initial camera are unchanged. Outlook alone does not grant an unrelated party's programme.

The expansion includes **Hold the Line** and **Defence in Depth**, corrected at the user's request to entrenchment, core defence and genuine forest/jungle defence instead of higher supply consumption. Depth gives 5 additional entrenchment levels, 25% faster entrenchment, 8% core defence and 10% forest/jungle defence, with lower maximum offensive planning. Timed policies replace their own family; terrain training expires with its owning policy. Cambodia's intervention posture reaches 14% attack and 6% defence, with distinct rewards for an actual secured military outcome. See [CAMPAIGNS.md](CAMPAIGNS.md) for exact stages, objectives, verified assistance, policy replacement, conditional burdens and withdrawal contracts.

`focus_timing.json` now sets 299 focuses to 70 days, seven short reviews/verification tasks to 35 days and the initial military review to 42 days. Hanoi rehabilitation is a substantive 70-day project. Both design loaders preserve the immutable approvals. Focus cost uses seven days per point.

## Whole-tree reward revision

The revision replaces each focus contribution rather than adding the new values on top of the old ones. Every focus has an explicit purpose and a reviewed package in `reward_rework.json`. Pure signed-productivity-growth rewards have been replaced with actual construction, fiscal, production, research, doctrine or administrative outcomes. All 48 original timed decision programmes received the same review; the 30 campaign actions retain their native agreement, verification and renewal roles.

Party Schools now provides 6% lower bureaucracy expenses, 5% construction speed and one 50% industry research bonus, with 1% higher education expenses and its existing contribution. Hear the Economists provides 3% general research, 6% civilian-industry construction, 4% corporate-tax income and one 50% electronics bonus, with 1.5% higher education expenses. These are competing allocations of the next training/advisory budget, not a claim that cadre education excludes economic expertise. Their institutional dynamic modifier survives normal Communist succession, pauses when that party leaves and never replays research on return.

Permanent campaign schools and liaison institutions replace their own family stages without a 180-day expiry. Paid operational terms remain finite. Prepared war plans may be earned before war; their first prepaid term activates immediately in a real war, ends when its genuine conditions disappear and never renews itself on a later daily tick or second war. Subsequent renewals still require funding. Recipient-dependent dividends use actual accepted/current agreement or native-assistance predicates.

Existing completed focuses migrate earned programme values once. Cash, completed or queued buildings, experience and research bonuses are not replayed retroactively. A new campaign remains the cleanest full-tree test; no HOI4 save-migration or multiplayer session has been run by the agent.

## Government, rewards and persistence

Earned political programme values are retained when their government leaves, while their active dynamic modifiers are removed. The matching party and, for personal programmes, exact party chief must return before those earned modifiers operate again. Returning never repeats cash, experience or construction rewards. Common recovery and physical gains persist.

Every focus reward is checked at execution and stamped once. A completed focus whose live funding, authority, territory or building capacity fails can be resumed through a zero-political-power retry decision after the conditions recover. Its implemented prerequisites remain required. Recovery stages cannot regress or stack older stages.

Domestic decision programmes remain limited to one per economy, civic or security family. Foreign programmes use separate partner families, so unrelated aid, trade and negotiations do not share a single global lock. Earned providers and current authority remain required. Paid temporary programmes are not restored free on government return.

Foreign invitations expire after 90 days. Only a valid, funded acceptance by the intended recipient applies and charges the programme. Refusal or silence charges nothing. Offers transfer no territory, equipment or sovereign authority. Flood, actual China-war pressure and loss of an accepted patron programme have explicit observers; none starts a war automatically.

The political provider uses existing native party selection and leader retirement. Historical succession is Le Duan → Truong Chinh (14 July 1986) → Nguyen Van Linh (18 December 1986), with remembered incumbency covering Duan's expiry gap. Explicit alternative player mandates are respected. Kiet's party-chief role and independent governing transformations of Front-allied parties are alternatives, not historical claims. See [POLITICS.md](POLITICS.md) for providers, dates, sources and manual integration maintenance.

## Construction from the difficult starting position

The northern starting states still receive no factory or equipment grant from history. The funded 70-day Hanoi rehabilitation delivers one civilian complex after completion, ownership/control, capacity and money checks. Normal staffing and consumer-goods rules still apply. Other projects need construction capacity. Existing native alternatives remain available:

1. Economy → economic projects → Leasing → Civilian Complexes + leases offsite civilian capacity for recurring native expenses.
2. A foreign player can select a VIE state and propose a native investment project. It requires acceptance, donor funding and VIE's co-payment, and uses the native project timer and influence rules.
3. The existing Imperia Transfer Funds diplomatic action can finance agreed expenses with an actual sender debit and recipient acceptance.

These routes are campaign choices, not automatic aid. Current native economic definitions determine their prices. Starting industry, GDP, OOB and equipment were not increased to bypass the difficulty. Source traces are in [MECHANICS_REVIEW.md](MECHANICS_REVIEW.md).

## Source ownership and rebuild

`approved_design.json` is the **immutable original concept snapshot**, SHA-256:

`a75e577703dbfa708f5e7493539f46e5280628d1a1e940b3204a38d46082d3d2`

Its metadata describes the original concept, not the current implementation. Do not rewrite it. Runtime guards remain in `compile.py`; final narrative comes from `flavour.py` and explicit revision descriptions. `runtime_design.py` first loads the approvals and defensive/timing corrections, then `reward_rework.py` applies the complete explicit `reward_rework.json` revision. The manifest records these hashes separately. The four protected China-defence values remain unchanged. The two legacy Cambodian invitations still use CBD, not Cameroon.

`manifest.json` distinguishes generated files, the three narrow compiler-owned integration patches, hand-authored political sources and three manual political integrations. The compiler deliberately does not regenerate the manual providers or portraits. Preserve unrelated content in shared integration files. Do not run a broad historical-politics generator to rebuild this country.

### Tooltip correction following the first player screenshots

Guarded application helpers alone caused locked future focuses to display no effect. Each focus now has an unconditional native `effect_tooltip` containing the exact approved raw reward and a separate `hidden_effect` calling the guarded implementation. The preview executes no transactions. The validators check both blocks for all 307 focuses, and execution regressions check that previewing pays/grants nothing while actual completion applies once.

Internal scenario/country predicates are retained inside `hidden_trigger`. Implemented-policy requirements use localized `custom_trigger_tooltip` blocks following main MD Russia's pattern. Technical flag labels also resolve in English. `presentation.py` supplies concise programme names and removes visible year annotations and dash punctuation while preserving native value-format controls and actual signed gameplay amounts. Existing political English descriptions received the same presentation cleanup. These changes were explicitly requested after the first in-game screenshots; they do not alter the approved reward values or focus geometry.

The later military screenshot exposed a separate campaign helper that still displayed its scenario label and silent Treasury checks. The campaign eligibility helper now uses only `hidden_trigger`. Positive funding requirements in both generators use native MD `custom_trigger_tooltip` grammar, showing the exact required Treasury and current value. This preserves actual funding and scenario evaluation while removing the misleading single green scenario check. The Long War description now uses narrative flavour rather than implementation disclaimers.

### National-spirit icon sizing correction

National spirits no longer alias the larger focus textures. `spirit_art.py` maps the original 72 starting/recovery, decision and crisis ideas and 15 dynamic programmes to appropriate existing native MD idea textures. `campaigns.py` adds 54 campaign policies and burden stages using the same small native art convention. The selected spirit icons are at most 68 pixels in either dimension, mainly the native 60×68 format. The original replacement art was visually inspected. The validators check every spirit/programme reference and texture dimensions. The earlier layout report records the pre-correction spirit art snapshot.

Run from the mod root with Python and Pillow available:

```powershell
python -X utf8 tools/vietnam_1970/compile.py
python -X utf8 tools/vietnam_1970/validate.py
python -X utf8 tools/vietnam_1970/test_transactions.py
python -B tools/vietnam_1970/test_politics.py
python -X utf8 tools/vietnam_1970/validate_campaigns.py
python -X utf8 tools/vietnam_1970/test_campaigns.py
python -X utf8 tools/vietnam_1970/validate_rewards.py
```

The compiler uses the existing approved art sources inside the mod. It writes the generated manifest and integration list. The main validator and legacy transaction suite write JSON reports; the political and campaign suites are read-only and report to stdout. Compilation is repeatable without replaying in-game rewards.

## Verification and limits

Current results are in `validation.json`, `campaign_validation.json` and `reward_validation.json`. Main, campaign and explicit numeric-revision checks pass. Twenty-one base transaction scenarios, twenty-one campaign scenarios and fourteen political workflow scenarios cover selected execution boundaries. They include institutional succession/party return, once-only value migration, actual completed rehabilitation, immediate wartime activation, finite-term expiry and agreement-owned dividends. Earlier [MECHANICS_REVIEW.md](MECHANICS_REVIEW.md) and [LAYOUT_REVIEW.md](LAYOUT_REVIEW.md) remain historical snapshots. The detailed new source review is under `docs/design/vietnam_rewards_rework_2026_10_19`.

The current byte-for-byte repeatability check covers 63 generated, integration, manual political, approval/manifest, timing and override files. A second compilation changes none of them. Both approved input hashes remain unchanged; see `rebuild_check.json`.

**No agent-run HOI4 engine session or multiplayer balance test has been performed.** The player supplied running-game screenshots that exposed the original tooltip defects; the correction has been checked at source/script level and still needs a new running-game inspection. The script interpreters exercise selected supported statements; they do not emulate engine UI, economics, queue timing or network synchronization. Installed-file previews are reconstructions, not screenshots of the running game.

For the first engine pass: inspect the error log and January 1970 tree/spirits/portraits; hover conditional rewards; exercise native retirement and party departure/return; try a funded and unfunded project with ownership/slot changes; check leasing and investment; accept/refuse/expire invitations; observe crisis boundaries; then save and reload. Confirm that construction is queued once and no money or reward is duplicated.
