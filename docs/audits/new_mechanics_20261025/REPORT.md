IMPERIA COLD WAR: Recent mechanics quality and multiplayer review, 25 October 2026

The user clarified that this review covers all recently added mechanics and minigames, not only the last UAE workforce change. The inspected base is commit `87e971e559e2db6946f507c0d49215b8385cb803`; the current reviewed head is `a604deca72691677133dcb29dc82d30bd90a62bc`. There are 159 changed runtime files across the new systems and their shared integrations. `scope.json` records the exact paths and pre-review hashes.

## Result and repairs

The latest execution of all 47 distinct validation commands passes. These commands include suites and script-style scenario checks, not 47 individual assertions. There were 52 actual invocations; the initial dossier failure and an intermediate UAE test failure are retained in the logs rather than overwritten. No tested command changed a loaded runtime file. Runtime repairs were applied separately and are hashed in `repairs.json`.

| Finding | Correction and verification |
| --- | --- |
| UAE airport omitted the required shared slot | Aviation Hub now grants one extra shared slot in Dubai before its one airbase level. Native focus preview and real execution agree. The slot is inside the same once-only focus transaction. The development model confirms that repeated application cannot grant a second slot, and that full, foreign-owned or occupied sites receive no slot, construction or charge. Canonical compiler, development data and current documentation are aligned. |
| Nuclear expense label omitted civilian research and enrichment | The existing cost provider already charges seven civilian projects as well as two weapons projects and enrichment upkeep. The Defence Budget label now says Nuclear Research and Enrichment. Its explanation includes all current bases, and the seven civilian project descriptions now show their weekly research budgets. Existing prices, treasury logic and budget formulas are unchanged. |
| Nuclear tests did not cover the civilian/facility extension | The bounded interpreter now supports the actual `multiply_temp_variable` operation. New cases exercise each civilian project, concurrent projects, zero/one/three facilities, GDP/c scaling, inflation, repeated refresh, deactivation and combined expense aggregation. All 25 integration tests pass. The current reporting helper and documentation no longer claim that enrichment has no separate cash upkeep. |
| Dossier validator failed after the feature was committed | It stripped feature insertions only from the working copy, then compared that result with an unstripped HEAD that already contained the feature. Both sides now use the same native-source projection, retaining the check on code outside the marked integrations. The full validator completes 1,522 checks. |
| UAE development test assumed one preview grammar for every tree extension | It attempted to iterate a missing wrapper on the new naval focuses. It now explicitly checks all authored UAE focuses and identifies the 15 naval additions, whose native grammar is covered by their separate validators and model suites. The complete development run passes, including the repaired airport transaction. |

The original country approvals remain intact. No project price, recurring charge, focus duration, political gate, treaty term, workforce balance or calendar cadence is retuned by this review. The only new gameplay asset is the airport's required shared building slot on future successful completion. There is no automatic replay of previously completed projects.

## Coverage

The primary checks cover COMECON, the superpower dossier and configurable treaties, SSR lifecycle/market/diplomacy, generic naval adaptations, USA expansion and early/bilateral cooperation, Gulf counterplay and access, Cuban integration, nuclear integration and UAE programme execution/presentation. They include actual emitted-code parsing, guarded transaction models, ownership/capacity cases, one-time receipts, authority/consent boundaries, programme cleanup, price aggregation, graph/reference checks and generator ownership preservation.

The related-system phase runs the current Space Race validator and all 15 `qa_` scripts, colonial structure and runtime checks, nuclear-intelligence tests, Cold War GC controls, session-based UN Council seats, economic-organisation validation and the previous quality/open-findings regressions. All 24 related commands pass. A filename containing multiplayer means a source/model check unless its report explicitly records real clients.

The full source scan parses 5,576 current script files without structural errors, script BOMs, invalid UTF-8 or duplicate event IDs. Literal custom boolean calls resolve in the scanner's defined provider universe. One identical inherited helper duplication remains recorded as unchanged upstream content. Modified runtime scripts were reparsed after repairs; all five modified runtime files have the required encoding and project markers, and the changed Python sources parse.

`regressions.json`, `related_regressions.json`, `final_regressions.json` and `development_recheck.json` preserve exact arguments, exit codes, timing and logs. `summary.json` derives the latest result per distinct command. `nuclear_costs_current.json` evaluates the current production expressions in the bounded model and records the unchanged provider hash.

## Performance and multiplayer boundaries

The reviewed scheduling has bounded country/system entry points: COMECON uses its saved organisation clock; dossier observation uses a single weekly anchor/day guard; SSR lifecycle work is attached to fourteen country-specific hooks; naval maintenance and USA reconciliation use their country hooks. The new repairs add no recurring loop, background worker or new financial payment path. Static structure and operation estimates do not establish frame rate, host timing or OOS behavior.

Slot-candidate scanning is deliberately heuristic. The large COMECON supply-hub dispatcher contains thousands of province branches whose shared-slot grant belongs to the checked caller transaction. They are not thousands of confirmed errors or recurring world scans. Other candidates include inherited Iraqi deliveries, native investment helpers and legacy USA revenue-sharing decisions that were already present before the reviewed feature change. They are preserved in `building_slot_candidates.json` as follow-up candidates; this review does not certify those unchanged legacy delivery paths or silently redesign their funding/refund contracts.

No new native game process was launched because the user's HOI4 was already running. It was neither stopped nor manipulated. The current default game log contained no matching new-feature diagnostic at inspection, but that is not evidence that every feature was activated or exercised.

Existing native evidence was checked against current source hashes. All 42 SSR runtime files match its recorded successful isolated engine test. Its report covers forced completions, real releases/re-entry and natural daily callbacks, not normal prerequisite playthroughs, manual hovers or MP. The COMECON Council reports match most current inputs but predate the current authority-restoration line, several interface/text changes and the SSR weekly-expense insertion. These differences were inspected; those old reports are not represented as new native verification of the current whole build. `native_source_lineage.json` records exact matches and differences.

A genuine two-client rehearsal remains open: identical builds/checksums, simultaneous inputs, co-op, recipient consent, loss/return of controller authority, save/load, rehost, weekly settlement and a month/year boundary where relevant. The source/model checks do not establish that the previously reported crash is fixed or that the mod is multiplayer-release certified.

## Provenance

Primary evidence is the current project source, canonical generators, emitted scripts, preserved source hashes, captured check outputs and the explicitly bounded existing native reports. Corrections and review tooling were authored for IMPERIA COLD WAR with Codex assistance. Existing Millennium Dawn, quaZa and project notices are retained; separate individual authors or permissions not established in those sources remain unknown. No image, frame, map, font or audio asset is modified. The project identifier does not relicense inherited content; see `IMPERIA_COLD_WAR_NOTICE.md`.
