IMPERIA COLD WAR

**RETIRED on 28 October 2026 at the user's request.** See `RETIRED.md`. The installation statements below are historical records. Do not regenerate this package. The replacement concept lives in `../france_1970_design/` and awaits approval.

# France 1970: installed political and party programmes, revision 5

The user-approved V5 is installed as `COLDWAR_FRA_1970_focus`: **260 focuses**, twelve exact-party programmes and shared republican institutions. It contains 34 political, 80 economic, 96 military and 50 fixed-country foreign-policy focuses, with 67 mutually exclusive pairs and 252 complete compatible routes. All twelve party programmes include their own economic, military and foreign-policy choices.

Approval is recorded in `V5_APPROVAL.json`, with the user's actual instruction and SHA-256 `fc3c856880a9d48a668f454168730f08b3e64f8652caea55a34e128b42240464`. `approved_design_v5.json` is an immutable copy of the approved preview data. Its original proposal-status field is historical metadata; the separate approval record authorizes this installation. The V4 frozen input, runtime snapshot and original manifest are preserved under their original names or `archive_v4/`. Old V4 reports with 234 focuses, 24 offers or 996 routes describe the preceding version.

## Political and domestic behavior

Pompidou, the January 1970 government and the existing MD party, election and leader systems are retained. Shared/history integration routes the persistent 1970 campaign to this tree; other scenario starts retain their existing routing. The scenario predicate does not expire in the 1980s.

All party branches remain visible. Focus availability and real completion require the exact registered MD subparty, using its existing `*_are_in_power` requirement and party-name localisation. Internal scenario checks, dated CID/FN separation and predecessor receipts remain real hidden guards. There is no party-dependent `allow_branch` hiding.

Government-bound dynamic programmes and removable equipment-production ideas are reconstructed from permanent earned receipts. Leaving government removes their active benefits and drawbacks; returning restores them without repeating PP, experience, doctrine, research or stability awards. Shared republican institutions endure. CID and FN keep separate receipts despite sharing native slot 20, divided at 5 October 1972.

The three historical starting spirits are granted once: Presidential Republic, Unsettled Social Compromise and Uneven Modernisation. Approved reforms conditionally remove or replace the latter difficulties. Initialization never restores an already resolved starting penalty.

The 96 revised domestic packages cover sector productivity, taxation and investment, electricity use, procurement, armed-forces training, doctrine, fuel, personnel costs, reinforcement, maintenance, territorial readiness and other supported MD/Imperia systems. There are 53 distinct modifier keys across the full revision. Thirty-two domestic focus packages use removable, archetype-specific production-cost ideas. BBA and legacy aircraft configurations use their actual different archetypes. The 24 dedicated research priorities follow the corresponding funded armaments programme; ten additional retained economic focuses also grant research bonuses. Project-completion and unresearched-target guards apply to the narrow technology rewards. No focus completes a technology or special project outright.

Effects display concrete native costs, signed modifier changes, XP, research/doctrine bonuses, named spirits and decision unlocks. No explanatory custom paragraphs or zero modifier rows are appended to reward fields. The 62 finished English description overrides in `localisation_v5.json` preserve approved gameplay and replace concept shorthand with country-specific institutional narrative.

## Fifty recipient-owned agreements

The French player selects a named country through a distinct foreign-policy focus. That country receives ordinary Accept and Decline decisions. There is no initial French country-picker decision. A completed focus later permits a fixed-partner reissue after a 180-day cooldown. Invitations expire after 90 days; reissuing requires fresh consent.

The initial 56-day proposal focus costs 25 PP. Completing or declining an invitation grants no bilateral benefit. On acceptance, both governments must still afford their displayed setup costs. These are normally 20 PP and $50 million each; the approved Algerian social-development proposal costs France $75 million and Algeria $50 million. Costs and the two spirits are applied in one guarded transaction. The native prospective preview lists both countries' actual numeric costs and named ideas even before the offer can execute.

Accepted spirits have no fixed expiry and survive government changes. Both halves end on bilateral war, any diplomatic/financial/economic/military Imperia sanctions in either direction, withdrawal, loss of sovereignty, a missing signatory or an absent matching spirit. Third-country wars and sanctions do not terminate the pair. Lifting sanctions or ending a war does not automatically restore it.

Six independent families permit at most one active France-linked agreement per family: military industry, civil industry, science and energy, civil resilience, commerce, and training. Different families may coexist across French governments; the six-family cap prevents stacking rival agreements. Every approved offer has continuing benefits and costs. There are no repeatable finite XP or research awards in these offers. The exact French party must remain in office while its invitation is pending; the recipient's new government can still decide whether to accept it. Acceptance is never forced.

Maintenance checks the registered family slots and their fixed counterpart tags, with eight bilateral sanction-array lookups per live pair. It has no daily world-country scan. Full domestic reconstruction runs at initialization/upgrade, focus completion and actual party or dated-identity changes; ordinary daily work performs agreement maintenance. This is bounded source work, not a measured FPS result.

The legacy 24 French country-picker decisions are hidden. Previously accepted V4 compacts and already pending invitations retain their original providers and cleanup; accepted legacy compacts reserve their matching V5 family. The 210 retained domestic focus IDs and their receipts are preserved. The removed 24 generic foreign-focus completions are not mapped into 50 free new completions: the named-country offers are new initiatives. New V5 finite awards are not retroactively replayed for retained focuses already earned in an old save. Live save/reload migration remains an engine check.

## Reproduction and evidence

Run from the mod root with Python:

```text
python tools/france_1970/verify_v5.py
```

The verifier builds the preserved legacy subsystem, the V5 agreement subsystem and the V5 core, then builds them again and compares every France output byte. It checks that the frozen designs and shared integration hooks remain unchanged, then runs `validate.py`, `test_core_v5.py`, `test_offers_v5.py` and `test_offers.py`. The existing `test_programmes.py` entry point delegates to the same independent V5 domestic suite.

`VALIDATION.json` records emitted IDs, resolved coordinates, AND/OR prerequisites, reciprocal exclusions, durations, native party requirements, research targets, artwork/localisation references, dynamic bindings and all 252 reachable compatible routes. `PROGRAMME_TESTS.json` records the emitted-AST domestic execution model. `V5_TESTS.json` retains the results of the four verification suites, including the V5 agreement world model and legacy lifecycle tests. `manifest.json` records generated runtime hashes and canonical source hashes. All are source checks rather than an HOI4 simulation.

Independent source, native MD presentation and layout reviews are in `V5_INSTALL_REVIEW.md`, `V5_LAYOUT_REVIEW.md` and `ICON_REVIEW.md`. Historical evidence and 56 source records are in the approved V5 data and `proposal_v5/`; the mechanics catalogue traces current MD/native/custom providers and consumers. Earlier history, research and modifier evidence files remain available for retained content.

The approved V5 browser preview and `proposal_v5/PREVIEW_TESTS.json` cover 260 selectable focuses, 100 agreement sides, 290 prerequisite links, native artwork and normal/responsive views. Installed focus positions and grouped prerequisites are independently compared with that frozen preview model. It is a source reconstruction, not a native HOI4 screenshot. Long offer connectors and engine-specific line routing remain native UI checks.

## Verification limits and provenance

No HOI4 load, native hover, save/reload, AI campaign or multiplayer timing test was performed. Source parsers and models cannot establish Clausewitz execution order or native UI rendering. The guarded completion-order tests specifically exercise sending before the engine marks a focus complete, but still do not substitute for a live game test.

Script files are UTF-8 without BOM; English localisation uses UTF-8 with BOM. All custom identifiers retain the searchable `COLDWAR_FRA_` namespace and project markers. No game artwork was generated or modified. Focus textures are reused from this checkout's Cold War folders, with existing small MD idea artwork for spirits. The stock shine overlay is an external base-game dependency. Original individual art authors and redistribution licences are unknown in the available checkout; the project marker grants no ownership or licence. See `IMPERIA_COLD_WAR_NOTICE.md` and the icon review.
