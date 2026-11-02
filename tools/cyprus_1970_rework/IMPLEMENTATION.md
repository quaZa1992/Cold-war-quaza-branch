IMPERIA COLD WAR: Cyprus 1970 compact replacement

The approved design is installed. Start a new 1970 campaign to use the replacement country history and focus tree. The immutable design is `approved_design.json`, SHA-256 `90e64f0a4e2e609e41159096094ddad2f6f20b02da60c31b8ad1895cf4bf994a`. Research and the original visual preview remain in `docs/cyprus_1970_rework_20261027/`.

The 28 October spacing revision is installed through the geometry-only `layout.py` overlay. It reduces horizontal span by 42.2% while preserving every gameplay field. Current coordinates, rendered review and verification limits are recorded in `LAYOUT_REVIEW.md` and `LAYOUT_REPORT.json`.

The focus artwork revision is also installed: 44 distinct icons across the 100 focuses, including three generated Cyprus emblems. `ART_REVIEW.md` records native sprite/shine wiring, source prompts, preserved compact positions, unchanged effects and verification boundaries.

## Installed content

- Exactly 100 Cyprus focuses, 15 mutually exclusive pairs, and three 12-focus programmes: Makarios/centrist tradition, Eniaion/later DISY, and AKEL. Branches remain visible. Native MD party-in-power requirements govern completion and programme activation. Party spirits suspend and restore; one-time assets do not replay.
- Shared constitutional, communal, security, economic, defence and diplomatic chapters. Eight starting spirits represent the constitutional breakdown, separate communal administrations, divided Guard command, Enosis networks, technical shortages, Makarios, UNFICYP and the 1960 Treaty of Guarantee. There are no workforce-size penalties.
- Sixteen supporting focuses in the actual Greek tree and the Turkish/British 1970 generic tree. The old Greek Cyprus branch and duplicate offers are retired. Other Greek event numbers are preserved; Ioannidis's retained policy receipts require the corresponding R2 policy.
- Seven recipient-approved agreements. Native prospective effects show both countries' numbers. EEC association requires all six founding members' actual membership and consent; Cyprus receives association, not membership.
- Signed agreement spirits have no expiry. War, native embargo or any mirrored Imperia sanction class suspend both countries' spirits. Eligibility restores both without repeating setup fees or assets. Existing sanction callbacks reconcile immediately; a monthly check covers missed transitions.
- A Greek coup attempt, guarantor consultations, Turkish intervention, Greek volunteer authorization or direct entry, and negotiated settlements. These are player-directed campaign alternatives. The Treaty of Guarantee is separate from NATO and does not automatically establish a legal right to the alternative war.
- Turkish intervention grants the approved 180-day operational spirit. An unresolved crisis can start the finite army-pressure chain. Its four Turkish crisis decisions are the user's explicit exception to the focus-only policy. Cyprus has no replacement decision catalogue.
- Direct Greek entry records both prior NATO memberships and invokes native NATO departure before joining Cyprus's war. Return is blocked while either Greece-Turkey or Cyprus-Turkey remains at war. Prior members return through native admission when normal independence, faction and alliance conditions permit; pending returns retry monthly. Native departure opinion consequences remain.
- English localisation only. Existing MD icons, portraits and framed event imagery are reused unchanged.

## Runtime

Run `python tools/cyprus_1970_rework/compile.py --install` to regenerate and install. `--check` writes a separate generation report without clearing the installed manifest. The retired large Cyprus compiler forwards here. Greek/generic owning generators retain the imports. Files are written atomically.

New runtime IDs use `COLDWAR_CYP_R2_`; foreign focus IDs also identify their hosts. The native tree ID `COLDWAR_CYP_1970_focus` remains stable. Existing portrait asset filenames retain `COLDWAR_CYP_1970_`.

One fixed-country monthly reconciliation owner handles continuing eligibility. There is no daily or weekly Cyprus reconciliation observer. War/peace, annexation and sanctions callbacks handle targeted transitions. Native weekly money calculations read cached activation flags and GDP; they do not rescan diplomatic eligibility. Agreement maintenance does not scan the world.

Domestic setup charges use native treasury effects and may take treasury below zero. They represent policy commitments rather than cash-only purchases. Bilateral ratification and paid crisis actions have explicit affordability guards. Recurring costs use weekly MD units and literals with at most five fractional digits.

Every building level grants one shared slot before construction in the same one-time transaction, including infrastructure and forts. Ownership, control and native building caps are checked.

Two reachability corrections: refusal of Greek training bypasses its dependent training-only focus without its reward; rejected or expired federal amendments uncomplete the unratified focus so another proposal or the exclusive 1960 settlement remains selectable.

## Verification

`VALIDATION_REPORT.json` records installed-file static checks and hashes. `test_crisis.py` covers crisis guards, timers, native syntax regressions, NATO conditions and volunteer permission lifecycle. `ENGINE_REPORT.json` records the latest private native-game run and every checkpoint. Earlier reports and raw logs remain retained.

Final installed-state evidence: 26 static checks passed, 13 crisis regression tests passed, and all 64 native engine checkpoints passed with zero Cyprus-related errors in that run. Native checks covered the eight starting spirits, treaty holders, three party programme lifecycles, representative infrastructure/factory/province-fort grants and slot/replay protection, bilateral agreement ratification and sanctions, Turkish war entry, Greek war entry, departure of both NATO members, blocked premature re-entry, and return after both relevant wars ended. The private probe intentionally terminates its game process after its completed checkpoint sequence; its process return code is not a campaign stability score.

`greek_preservation_audit.json` compares the old and new shared Greek functions against the archived originals. All 24 unrelated pending-offer pairs, 174 non-Cyprus reconciliation grant references and surviving proposal event numbers were preserved.

The native fixture starts the installed 1970 campaign in a private E: user directory and executes real runtime helpers. It seeds test budgets, prerequisite receipts and crisis conditions. It is not a complete human playthrough and does not certify multiplayer synchronization, manual tooltips, calendar-driven event delivery, save/reload or actual volunteer deployment through diplomacy.

Greek volunteer authorization uses a native permission rule, a targeted Cyprus relation override, reduced thresholds and the approved spirit. It does not spawn substitute divisions. Deployment against an existing NATO ally remains a manual native-diplomacy check.

## Sources and assets

The approved source catalogue distinguishes January 1970 conditions, later precedents and alternative-history terms. Primary evidence includes the [IPU election report](https://data.ipu.org/election-summary/PDF/CYPRUS_1970_E.PDF), [World Bank memorandum](https://documents1.worldbank.org/curated/en/714871468027642843/pdf/multi0page.pdf), [1960 treaty texts](https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf), [UNFICYP chronology](https://unficyp.unmissions.org/en/1967-crisis), [1974 account](https://unficyp.unmissions.org/en/events-summer-1974), and [1977 agreement](https://digitallibrary.un.org/record/564485/files/S_12323-EN.pdf). Numerical effects are balance choices, not historical estimates.

The MD donor is `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`, alongside existing IMPERIA systems and installed native game documentation. MD/base-game contributors retain their credits and rights. Individual authors and separate redistribution permissions for reused portraits, icons and photographs are unknown in the available snapshot. No asset pixels, frames or alpha were changed. The event picture is the existing 217 x 163 MD composite with a 180 x 150 photo inset.

The 87-file original archive is recorded in `backup.json`; the shared sanctions-hook original is in `supplemental_backup.json`. Archives are on E: and do not traverse asset junctions. Native profiles and raw logs use `E:/HOI4_Mod_Tools/mdcoldwar/runtime/cyprus_r2_20261027`.
