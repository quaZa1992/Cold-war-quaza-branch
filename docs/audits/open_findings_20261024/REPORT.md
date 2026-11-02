IMPERIA COLD WAR: Follow-up quality and multiplayer audit, 24 October 2026

The current-source follow-up repairs confirmed runtime and generator defects, verifies the UN recognition calculation in the native engine, and separates current functional checks from obsolete preservation expectations. It is a targeted audit of the newly integrated mechanics, with additional repairs where their native diagnostics exposed broken content.

## Confirmed repairs

| Area | Problem and resulting repair |
| --- | --- |
| Nuclear multiplayer registration | `modifier@mdcw_nuclear_safety_target` was not registered as a synchronized dynamic token. The engine explicitly warned that this could cause OOS depending on use. Register the existing identifier in `common/synchronized_dynamic_tokens/ICW_nuclear_power_tokens.txt`. The warning is absent in the final native run. No network desync was reproduced or claimed. |
| Nuclear development budget | The budget file referenced `@math_expressions_max` without defining that file-local constant. The engine tried to resolve a missing dynamic token. Define the same 100000000 cap used by the native money provider. The model previously injected this constant itself; it now loads actual declarations and rejects undeclared constants. The native price function now demonstrably returns 0.2 for a weekly base of 0.2, GDP/c of 36 and inflation multiplier of 1. |
| Startup scope | Eight startup paths used country-only script calls or scenario predicates from the scope-less native `on_startup`. Dispatch each world initialization once through an existing country, with a transient global flag cleared before and after the loop. This covers Covert Action, research thresholds, PMC access, military-industrial setup, Suez, German recognition, missile/satellite history and the immediate zombie scenario guard. The 1970 gate now prevents the modern missile/satellite history from being evaluated through an invalid scope. Canonical research and diplomacy emitters are repaired too. |
| Colonial events | Two files used `namespace` instead of native `add_namespace`, leaving eight event IDs malformed. Fix both emitters and rebuild the canonical scripts and manifest. |
| Syrian events | The streamlining pass inlined retired event definitions as though they were effect calls. Seven nodes then appeared outside any event and could not execute there. Remove retired definitions at the file root and inline only their actual calls. Both regenerated event files preserve every retained event body. Update their generated hashes only after checking the old hashes and canonical output. |
| Cypriot agreements | Yugoslav offers used unregistered `YUG` scopes and country requirements. The actual 1970 Yugoslav country is `SER`, with the Yugoslav cosmetic identity in its history. Route native tags and name lookups to `SER` while retaining existing `_YUG_` decision IDs and pending receipts. Funded acceptance, rejection and replay guards remain intact. |
| German balance of power | Two modifier blocks contained duplicate `drift_defence_factor` entries, which the engine overwrote. Merge the DDR contributions to 0.35 and fix its emitter. Align the GER output with its current canonical generator, retaining the intended 0.10 legal-position modifier. |
| Egyptian doctrines | Two focuses gave a technology research bonus to `land_doctrine`, which is not a research category in the loaded version. Use native `add_doctrine_cost_reduction`, with the specified 0.75 value and one use. Repair the generator's doctrine-category routing without changing the approval data. |
| Chinese 1985 diplomacy | Eleven rewards referenced absent `positive_trade_relations`. Bind them to the existing MD `economic_mission` provider: opinion value 20 and native decay parameter 0.4. This is an explicit compatibility choice using an existing economic-diplomacy reward. All opinion providers referenced by that tree now resolve. |
| Inactive currency example | Its mutation test compared the live economy against an old development snapshot, rejecting legitimate subsequent edits. Keep that provenance snapshot intact and compare the current files before and after the example's test run, including a final class teardown check. All 32 example tests pass. |

## Native evidence

`native_result.json`, `native_game.log`, `native_error.log` and `native_evidence.json` record the final engine attempt. It uses HOI4 1.19.3, a frozen source copy and three hashed overlays for the latest China and nuclear repairs. All 11256 copied source files and all overlays remained unchanged during the test. The content of all 24 repaired production files matches the tested inputs. The three overlays differ from the live files only by CRLF/LF conversion in the earlier harness writer; that writer now preserves LF.

The bounded run completed startup and the first hour, ending at 1 January 1970, 13:00 after 113.9 seconds. The harness deliberately stopped it after the checks; `stopped_by_probe = true` explains return code 1.

- Both UN membership counting methods returned 126. The recognition threshold was 50.4. One recognition did not notify eligibility; 1001 did. The current recognition implementation therefore required no production change.
- The native nuclear price function returned the expected weekly cost of 0.2. Its missing-constant diagnostic and the safety-token OOS warning are absent.
- The final log has zero targeted startup-scope, UN math, obsolete Yugoslav effect, duplicate ideological-defence, Chinese opinion, doctrine category, colonial namespace or Syrian orphan-effect diagnostics.
- The isolated harness now copies `portraits`, which it had incorrectly omitted. The missing-portrait-generation diagnostics from that incomplete profile are absent with the complete portrait rules.

This is not a monthly soak, a human Space Race activation test, a native save/reload test, a UI rehearsal or a multiplayer network test.

## Source and functional checks

`regression_results.json` records 18 passing targeted invocations with their real captured logs. These include 13 new follow-up checks, the 21 uranium/nuclear integration cases, 51 colonial cases, 13 Cypriot transactions, the current 23 Syrian scenarios against both staged and installed output, 30 diplomacy cases, research, PMC access, both Suez suites, the currency integrations and the inactive example. The earlier repaired boundaries still pass their 11 quality regressions.

The German GUI performance check passes 106 checks. Closed or AI views execute zero display operations in its bounded interpreter. Open refreshes execute 131 rivalry and 193 security display operations. These are script operation counts, not FPS, server timings or OOS evidence.

`source_scan.json` parses 5493 current script files with no structural errors, script BOMs, invalid UTF-8 or duplicate event IDs. The one previously identified identical upstream helper remains unchanged. `reference_candidates.json` finds no unresolved literal custom boolean calls in its defined search scope. Modified Python sources parse, their first project markers are present, and scoped Git whitespace checks pass.

## Historical checks and remaining work

The three older currency validators still enforce full-file hashes from an earlier integration stage. They are not included in the 18 passing current invocations. No baseline hash was replaced to make them pass. The new lineage check proves the currency-law bytes match the immutable balance-stage hash after reversing the recorded realignment insertions, later project comments and the documented removal of the Deutsche Mark's calendar expiry. Current numeric drawbacks, interest consumption and the later paid-switch lifecycle are checked separately. Other old protected-file hashes also predate subsequent economy and presentation changes; their historical whole-file preservation claims remain unreconciled.

Older Syrian `test_foreign.py` and `test_lifecycle.py` also contain expectations for the removed WAR.5 popup, officer-bargain menu and retired preparation receipt. Those legacy invocations were not counted as passing. The current streamlining suites exercise their installed replacement paths, including deficit financing and recipient consent.

The two older German differential performance scripts still require a genuine pre-optimization source snapshot. They were not run against a manufactured copy of the current implementation.

The final engine log retains 323 diagnostic lines. They include retained DLC/backend notices, imported native scenario-test references, runtime recruitment notices, diplomatic GUI context diagnostics, retired Antarctica texture references, and underlying unit, map, AI and name-pool notices. They were preserved for review rather than labelled universally harmless. The diplomatic UI and underlying map/AI paths still need their own native reproduction and reachability checks.

A real MP rehearsal remains necessary: identical checksums, two human countries and co-op, simultaneous actions, pending offers, save/rehost, government and controller changes, two weekly pulses and a January/February boundary. This audit does not certify a multiplayer release.

## Evidence and provenance

Primary evidence is the current repository, canonical emitters, captured tests, native logs and installed engine documentation. The doctrine adapter follows the installed `add_doctrine_cost_reduction` interface and existing MD doctrine rewards. The replacement Chinese opinion reward uses the existing provider in `common/opinion_modifiers/generic_modifiers.txt`. The nuclear cap follows `common/scripted_effects/00_money_system.txt`, and token registration follows MD's existing synchronized-token files.

Repairs and audit additions were authored for IMPERIA COLD WAR with Codex assistance. Existing Millennium Dawn, Moveably, quaZa and other credits are retained. Individual authors or permissions not identifiable from those files remain unknown. Project markers establish neither ownership nor a third-party licence; `IMPERIA_COLD_WAR_NOTICE.md` and existing source licences remain authoritative. No graphic, event-frame, map or audio asset pixels were changed.
