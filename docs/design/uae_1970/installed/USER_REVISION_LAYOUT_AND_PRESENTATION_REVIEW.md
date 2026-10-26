# UAE independence, proclamation and native reward presentation

> Historical review of the 108-focus independence revision. The current 110-focus maritime/presentation build is reviewed in [MARITIME_REWARD_REVIEW.md](MARITIME_REWARD_REVIEW.md); the intervening industrial revision is preserved in [INDUSTRY_DEVELOPMENT_REVIEW.md](INDUSTRY_DEVELOPMENT_REVIEW.md). Current hashes and all 110 positions are in `LAYOUT_REVIEW.json`.

Independently reviewed on 19 October 2026 after the final compile. **No material open finding.** The installed tree contains 108 focuses in 12 groups. This supersedes the earlier 107-focus layout review for current output.

## Exact scope and evidence

`python tools/uae_1970/audit_layout.py` reads the installed Clausewitz, English localisation and GFX directly. It does not import the compiler or take its emitted coordinates on trust. It writes only the evidence directory. The immutable original approval retains SHA-256 `23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272`; the explicit subsequent user correction is layered in `revision.py`, SHA-256 `3b649019fefcc6e44297381a72a4377bb54c70b90622a9d54495229257dbc39c`.

The final focus file has SHA-256 `8c886139e7028bc0cd644f03a6ef076a141f51312af602f1599806a7f16e5a7d`. The reviewed presentation module has SHA-256 `56e3a5b68c97faa85f0c7ad1acc61edcdb31c6312badc2e38bd37ca62f80f28d`. `LAYOUT_REVIEW.json` records all contributing source and inherited native-asset hashes; `FOCUS_MANIFEST.json` records every actual focus line, anchor, offset, resolved coordinate, duration, title, description, prerequisites, exclusions and texture.

## Requested gameplay correction

The actual campaign predicate requires original tag UAE, a non-dynamic country and the January 1, 1970 start-date window. It does not depend on a later startup flag. Thirty-six checks combine valid and invalid campaign identities with British, American and no overlord, and negative, zero and funded treasury.

| Actual status in the 1970 UAE campaign | The Protected Coast | A Coast in Transition |
|---|---|---|
| Subject of Britain | Available without a treasury fee | Unavailable |
| Fully independent | Unavailable / bypass condition satisfied | Available |
| Subject of another country | Unavailable | Unavailable |

The original source had a silent $0.01 billion requirement on The Protected Coast. It is removed from both its real guarded transaction and preview. This is a source-level defect and correction; the user's exact saved-game runtime blocker was not independently reproduced in HOI4. Other funded focuses retain their approved charges and now expose the required and current treasury alongside the real affordability check.

Only `COLDWAR_UAE_apply_proclaim_federation` calls the actual formation helper. That provider rechecks full independence, the earned withdrawal and proclamation focuses, founding consent and the one-time formation guard before dropping the Trucial cosmetic and creating federal offices. The existing government-change callback preserves the Trucial cosmetic before formation. British release alone therefore does not create the UAE identity.

British Withdrawal retains its 21-day constitutional join and opens the new proclamation node. A single short unlock line names its actual successor; there is no invented modifier or unsupported focus-unlock API. Its independence condition is not made an automatic bypass that could permit the live proclamation helper to skip the preceding settlement.

## Layout and visual inspection

All 108 resolved positions, grouped prerequisites, exclusions, nominal durations, English titles, narrative descriptions, focus icons and shine masks match the current revision. The revision changes only six existing nodes plus the new proclamation. There are 96 relative anchors, no missing or cyclic anchors, zero unrelated card/connector intersections and a maximum native title advance of 142 pixels within the 147-pixel field.

| Focus | Resolved position |
|---|---|
| British Withdrawal | (5,5), unchanged |
| Proclaim the Union | (5,6), new |
| The Seventh Emirate | (3,7) |
| A National Council | (7,7) |
| A Common Currency | (5,8) |
| A Social Compact, neighbouring left programme | (5,9), unchanged |

The reviewer opened `OVERVIEW.png`, `UNION_LEFT_NEIGHBOURS.png` and `BRANCH_british.png`. The new proclamation and following join remain legible; the row-eight currency card and row-nine left-programme root have visible separation. British cards at negative x coordinates remain fully inside the preview. No title/header clipping or connector crossing through an unrelated card was observed. Other groups retain their previous footprint. The opening camera still targets The Protected Coast, with twelve programme shortcuts.

The proof sheets use the actual installed DDS artwork, inherited titlebar and native `hoi_16mbs` bitmap atlas at 96 by 130 pixels per grid unit. `OVERVIEW_NATIVE.png` retains the full-resolution composition; `OVERVIEW.png` is its reduced overview. Connections and unavailable-state treatment remain external approximations, explicitly marked on the sheets.

## Native reward and office presentation

Main MD Russia's named `modifies_dynamic_modifier_tt` heading and native numeric `add_to_variable` formatters, for example `05_russia.txt:410–413`, remain the reference grammar. The installed previews use those native formatter keys, signed units and colours. Only two genuinely missing Imperia formatter keys are supplied locally, retaining the registered modifier names. The native lower-is-better interest-rate formatter is used.

The old per-focus reward essays, repeated programme eligibility text and repeated stability-cap paragraph are absent. Programme conditions appear as native `if`/`limit` clauses. Numeric starting-spirit relief now shows the actual marginal change after strongest-family credits, already earned remedies, decision relief and zero clamps. A spirit removal is shown only if the spirit currently exists and all resulting components are cleared. Positive political stability displays the actual capped marginal amount.

The independent emitted-preview evaluator checks 1,296 contexts across all focuses. Its expected results come from separate design-data arithmetic, rather than importing `presentation.py`: normal and accepted agreements, earned and unearned remedies, settled decisions, expired temporary contributions, active and inactive government conditions, and British, foreign and no overlord. Every numeric modifier and treasury preview agrees. The real one-time application remains hidden behind its original atomic grant guard; tooltip arithmetic itself does not charge the player.

Proclaim the Union shows the native cosmetic-name result and the actual dated presidential and prime-minister appointments. Sixty additional emitted-preview contexts cover both dynastic party slots, a non-dynastic government, cabinet settlement, the historical date and later succession boundaries. Zayed, Khalifa and Mohammed bin Zayed use their existing portraits and corresponding native ideologies; prime-minister status follows the existing Rashid/Maktoum office provider. A non-dynastic government is not advertised a royal appointment. The dirham displays the real currency idea; bilateral offers display the relevant native British event titles.

## Limits

These are current source, arithmetic and native-asset checks. They do not establish live HOI4 hover rendering, initial scroll behaviour, native connector routing, shader states, multiplayer synchronisation or compatibility with an already progressed save. The wider diplomacy and startup-history systems retain their separate audits; they were not reimplemented by this layout review. No loaded game file was written by the independent auditor.
