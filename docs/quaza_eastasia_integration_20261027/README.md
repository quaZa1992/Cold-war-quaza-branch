IMPERIA COLD WAR

The later user-authorized reward and GDP-price revision is documented in [`../reward_rework_20261027/IMPLEMENTATION.md`](../reward_rework_20261027/IMPLEMENTATION.md). This import dossier and its native hashes describe the earlier integration; consult the new dossier for current reward values and validation.

Reviewed quaZa East Asia integration, 27 October 2026.

Source: [quaZa1992/Cold-war-quaza-branch](https://github.com/quaZa1992/Cold-war-quaza-branch), pinned commit `7bef99f058f5796788feb839c617407171141c1d`. The donor and the current repository have no common ancestor. This is a selective content integration, preserving the current SSR, Cuba, COMECON, nuclear economy, uranium, human-only raid policy and other existing work. It is not an unrelated-history whole-repository merge.

The integration installs the authored 1970 trees for North Korea (360 focuses), South Korea (300) and Japan (425), together with nuclear readiness, bilateral crisis diplomacy and the first-use procedure. Only the relevant new files and narrow native integration hooks were taken. Donor snapshots, original shared-file backups and native test profiles remain on E:. `SOURCE_INVENTORY.json`, `ASSETS.json` and `INTEGRATION.json` record source paths, pinned hashes and installed scope. Original donor reports describe their historical source state; current integration evidence is recorded here separately.

Corrections include guaranteed per-building shared slots before construction, exact native party requirements while keeping branches visible, complete prospective numeric foreign-agreement previews, corrected 1970 reachability and native focus serialization/icon support. Small spirit artwork uses actual native idea textures. Nuclear reconnaissance no longer attributes a confirmed nuclear posture to a country with no weapons. Standing agreement execution retains genuine acceptance, peace and mutual-sanction guards; preview helpers have no transaction authority.

Kim Il Sung dies on 8 July 1994, including catch-up in loaded campaigns. Both starting and native-pool spellings are recognized. If he remains in office, his death leads to a Funeral Committee using the colourised memorial portrait. A free, clearly named succession decision confirms Kim Jong-il, then opens his leader-bound focus branch. The shared native leader router preserves the mourning government and the confirmed incumbent rather than resurrecting Kim Il Sung. A different incumbent is not killed by the historical death news. Source tests cover replay, the precise date boundary, party eligibility, unavailable successor and old-save catch-up. The user-supplied photo is also the new ordinary leader portrait.

Implementation and regeneration

The canonical generators are retained. `python -B tools/quaza_eastasia_integration/regenerate.py` runs the ordered pipeline and compares outputs. Its final run produced no changed runtime files. Run it without a game process reading the mod. The underlying order is:

1. `python -B tools/north_korea_1970/compile.py`
2. `python -B tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py`
3. `python -B tools/japan_1970/build_diplomatic_runtime.py`
4. `python -B tools/japan_1970/stage_focus_graph.py`
5. `python -B tools/quaza_eastasia_integration/apply_reviewed.py`

KOR staging is on `E:/HOI4_Mod_Tools/mdcoldwar/runtime/quaza_eastasia_20261027/kor_stage`. KOR's last integration step owns the reciprocal NK-SK bridge additions in the NKO foreign files. A standalone NKO rebuild therefore needs the KOR stage/apply steps afterward. Do not copy an old staged shared file over a newer working tree. Stage from the current files immediately before applying. Immutable approved designs and the donor's before-polish archive remain unchanged.

Current validation

`VALIDATION.json` covers emitted syntax, encoding, references, all 99 native/custom modifier keys and custom consumers, visible text, absolute graph positions, reciprocal exclusions, native declaration order, decision categories and portrait DDS headers/payloads. Country validators execute the current effects in bounded models, including one-time receipts and agreement suspension/restoration. Readiness tests cover the 72-hour warning, launch authority, targets, cancellation, human-only raids, no automatic war, budget integration and duplicate-hit protection. Source/model checks are distinct from native engine evidence.

`ENGINE_ATTEMPT_1.json` preserves the first failed native run: six startup checks passed, but the run crashed after loading Pillow DX10 typeless/mip-zero portrait and funeral textures. It also exposed forward KOR anchors and missing shines. These findings were corrected at their generators. Raw native profiles and crash dumps remain on E:, outside the mod. The final native run in `ENGINE_REPORT.json` passed all 26 assertions, with zero feature-specific diagnostics, zero changed inputs during execution and no crash. The targeted shared integration paths also have zero native diagnostics. Unrelated whole-mod baseline diagnostics remain in the E: log; this is not a clean whole-mod certification. `POST_NATIVE_FORMAT_NORMALIZATION.json` proves that subsequent formatting changed no script AST or localisation text. A single-client fixture does not establish multi-client OOS stability, save/rehost behavior or live combat balance.

Attribution

Source contribution: quaZa1992's repository at the pinned commit. Individual original authors and separate redistribution permissions are unknown unless identified in retained source notices. Existing MD textures, event frames and bitmap fonts retain upstream rights. `docs/nuclear_readiness/event_art/CREDITS.md` and source metadata retain the nuclear artwork records. `gfx/leaders/NKO/COLDWAR_NKO_PORTRAIT_NOTICE.md` and `PORTRAITS.json` record the user-provided photograph, unknown original image author/licence, inherited mourning frame, image-generation edits and native exports. A project marker establishes no third-party ownership.

Verified final results

- `VALIDATION.json`: 1,085 unique focuses, 99 supported native/custom modifier keys, no reference/graph/encoding findings.
- NKO `implementation_validation.json`: 1,150 modeled transactions/lifecycle cases, source structure and English localisation passed.
- KOR installed validator: 300 focuses, 601 effects, 706 triggers, 347 dynamic modifiers, 357 ideas, 233 events, 104 sprites, 4,475 English keys; 24 named scenario cases passed.
- Japan installed checker: 425 focus rewards, 39 scripts and 10 English localisation files, zero findings; source-derived overview and 32 branch previews pass their preserved-payout and geometry checks.
- `READINESS_TESTS.json`: 41 source tests passed. Read-only parity comparison matches all 15 runtime generator outputs. The artwork-writing test was deliberately not executed.
- `test_succession.py`: seven source tests passed.
- `ENGINE_REPORT.json`: 26 native assertions passed, zero targeted diagnostics. Tests call actual death, caretaker, native leader router, successor and readiness transaction helpers. The fixture substitutes a private death-date authority at the 1970 start; it does not simulate a 24-year campaign. The first-use helper is invoked directly, without live raid combat.
- `REBUILD.json`: complete ordered regeneration is byte-identical. `SHARED_RECEIPTS.json` explains the two legitimate shared SSR-manifest hash updates.

`KOREA_QUALITY.md`, `JAPAN_QUALITY.md` and `READINESS_QUALITY.md` contain quantified representative choices, sources and remaining evidence limits. The donor's timed Japanese agreements retain their approved durations; they do not use Cuba's permanent standing-agreement lifecycle. No general numerical rebalance, historical policy redesign, multi-client session or save/rehost claim is implied by this import. There is a small remaining source workload for non-nuclear countries that open the readiness interface, because initialization keeps their daily cleanup path eligible. This also services civil defence; closing that path requires a separate lifecycle-aware optimisation.

The two PNG previews here are lossless format previews of the final 156 x 210 native DDS exports. The image-generation prompt specifications and original-photo provenance remain in `PORTRAITS.json`.
