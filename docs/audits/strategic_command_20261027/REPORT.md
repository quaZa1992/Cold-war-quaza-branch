IMPERIA COLD WAR

# Strategic Command localisation and mechanics review

Review date: 27 October 2026. Scope: the current nuclear readiness, civil defence and bilateral crisis subsystem, including its first-use procedure and existing money-system and nuclear-raid consumers.

## Confirmed defects repaired

1. The East Asia integration writer used `json.dumps()` directly on localisation containing authored `\n` sequences. This escaped 155 line breaks a second time. The game consequently printed literal `\n` in tooltips and event text. Both writers now use `build.localisation_source()`, which normalises the input before serialisation. The installed English localisation was rewritten with one native escape per break and retains its integration marker and UTF-8 BOM.
2. Readiness and civil-defence orders accepted 24.5 PP for a 25 PP order, and allied consultation accepted 19.5 PP for a 20 PP order. The previous checks only required more than 24 or 19. Execution and GUI gates now require the complete price, including fractional PP boundaries. Prices are unchanged.
3. The open command panel cached button eligibility behind a readiness-specific dirty counter. Other PP spending could therefore leave buttons visually enabled or disabled until the next readiness refresh. The open window now reevaluates its small set of eligibility triggers; the topbar launcher retains its dirty counter. Existing click-time guards remain authoritative.
4. Civil-defence release unconditionally removed its dynamic modifier, including when it had never been added or was already removed. Cleanup now checks for the modifier first. Repeated release and capitulation cleanup neither refund PP nor retain weekly civil-defence costs.
5. An empty arsenal displayed only a generic posture notice. It now explicitly shows `NO MISSILES IN STORAGE`. Zero missiles continue to mean zero operational allocation, zero dispersed reserve and zero strategic-force funding. Civil defence remains separately available.

The four changed runtime scripts are the readiness triggers, readiness effects, command scripted GUI and scripted localisation. The English localisation is the fifth runtime file. Generator changes are limited to `build.py`, `command_ui.py`, the integration writer, the source/model tests and the offline preview renderer. Runtime textures, policy balance, raid damage, employment doctrines and starting arsenals were not changed.

## Checks and findings

- All 49 source/model tests passed in `final_tests.log`, including seven new regressions for the defects above. The interpreter now respects PP comparison operators and rejects removal of an absent dynamic modifier instead of silently concealing that engine error.
- The existing tests exercise order delays, cancellation, fatigue recovery, preparation and release costs, weapon loss, simultaneous and independent crises, pair identity, stale or expired consent, capped tension relief, target-bound first-use authority, its 72-hour preparation and seven-day release window, doctrine changes, alliances, collapse and native raid eligibility.
- The money-system consumer aggregates the weekly readiness cost once. GUI budget refreshes calculate rates without transferring treasury funds. Civilian protection remains connected to both damage callbacks. All raid preparation/launch consumers retain their actual-equipment and doctrine checks.
- All 15 authored script outputs match the current generator. Script parsing, reference closure within the module, duplicate English keys, UTF-8 encodings and budget precision checks pass. The source snapshot is `baseline.json`; final hashes and validation results are in `verification.json`.
- Seven offline layouts pass widget bounds and native bitmap-font measurements. The empty-arsenal render was visually inspected. These proofs now read the installed localisation rather than the authoring dictionary, so a broken integration writer is no longer concealed by the renderer. They are composed previews, not screenshots from HOI4. They do not render native hover tooltips.
- Warning, assessment, direct communications, negotiated stand-down, withdrawal, counter-alert, ultimatum and revocation are connected through the existing eight diplomatic actions. Actual attacks still use native raids. No missing panel-only launch action was added, and no automatic attack is introduced.

## Remaining validation boundary

This revision was not loaded in a fresh HOI4 process. Native hover rendering, button refresh timing and real engine cleanup after reloading these changes still require a live check. The older `interface/native_review.json` and `tools/nuclear_readiness/engine_report.json` are historical evidence only. The script interpreter does not measure native performance, multiplayer synchronisation, rehost behaviour or network/OOS stability. A two-client rehearsal is still required for those claims. Previous crashes were outside this review.

## Provenance

The reviewed subsystem was selectively imported from `quaZa1992/Cold-war-quaza-branch`, commit `7bef99f058f5796788feb839c617407171141c1d`. Existing donor design and script credits remain applicable; individual authors and separate redistribution permissions are unknown where not recorded in the donor notices. This repair adds project-authored fixes, regression checks and one English status message. Native MD integrations retain their upstream attribution. Existing emblem, event-photo, frame and bitmap-font rights remain separate; no binary game asset is modified. Preview composition and existing image sources are recorded in `docs/nuclear_readiness/interface/ART_DIRECTION.md` and `docs/nuclear_readiness/event_art/CREDITS.md`; individual font authors and separate font redistribution permission are unknown in this audit.
