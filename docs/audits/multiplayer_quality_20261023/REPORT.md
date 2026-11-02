IMPERIA COLD WAR: Quality, performance and multiplayer audit, 23 October 2026

This audit repairs confirmed source defects and records separate native-engine evidence. It does not certify a multiplayer release. Native network synchronization, a full first month, and real save/reload behavior still require an in-game multiplayer session.

The checkout already contained extensive uncommitted work and continued changing during the audit. Existing changes and approval snapshots were preserved. The final engine attempt uses a copied script snapshot and linked asset directories. Its exact scope and result are recorded in `native_result.json`; earlier attempts remain in `native_attempt_*.json` and their logs.

## Repairs

| Area | Confirmed problem | Change |
| --- | --- | --- |
| Historical leader dispatch | 129 country setters had their final brace swallowed by an END-marker comment. | Restore the newline before that brace; validate generated wrappers and test rebuilding twice. |
| Native requirements | New content used unsupported `political_power` and `stability` trigger names. Spain also used unsupported shorthand inclusive variable comparisons. | Use `has_political_power`, `has_stability`, and documented `check_variable` comparison fields. Preserve valid exported-variable operands inside `check_variable`. Repair emitters as well as installed scripts. |
| Decision eligibility | Dynamic scenario, existence and subject conditions appeared in the static `allowed` field. | Retain static country routing there and preserve the complete original requirement in `visible`. Keep execution guards. |
| UN Security Council | Parameterized seat calls were rejected by the actual engine, although the model tests expanded them. | Emit concrete native effects for the current five seats. Preserve assignment, vacancy, veto, voting and GC authority behavior. |
| Suez Canal | Transit income could continue while physically blocked. The fiscal entry point no longer refreshed the canal burden before reading cached receipts. | Restore the physical-open condition and the nonrecursive local refresh before fiscal calculations. Both Suez suites pass, including 27 lifecycle/calculation tests. |
| Ideological defence | Several providers still emitted a removed custom modifier while political-support calculations already read native `drift_defence_factor`. Some DDR focuses wrote an unmapped variable. | Bind providers, focus receipts and generator input aliases to the actual reader. Migrate saved DDR values once without charging or granting other assets. Preserve approved design JSON. |
| Colonial Affairs | The native run repeatedly attempted to create numeric-prefixed tokens when displaying unset state values. | Read these view fields through explicit state/PREV scopes. Rebuild the canonical output and its generated manifest. The native follow-up no longer emits the observed three-field token errors. |
| Gulf programme | Repeated removal of an absent programme generated runtime errors. | Check presence before removing the dynamic modifier. |
| French legacy agreements | Maintenance and acceptance referenced 24 removed focus IDs after the v5 tree replacement. Family checks also queried absent named targets. | Use the existing `_earned` receipts established by the old compiler. Preserve accepted agreements and original consent/payment guards. Repair 72 installed references and the legacy emitter; guard optional named targets before checking their reservations. |
| Oil calculations | The world trade accumulator wrote country variables instead of the pulse country's temporary totals. Zero generation and an empty relevant-country cohort could produce zero denominators. | Accumulate explicitly in the pulse scope, reset per-call export totals, and guard the documented zero cases. The six-month oil pulse is model-tested, not exercised by the short native run. |
| Space Race performance | Each human country's weekly update repeated the full world ranking, in addition to the daily global pass. | Share the scheduled calendar/ranking pass once per game day. Keep direct mission-outcome ranking updates. Preserve quarantine and saved calendar guards. |

## Verification

- `source_scan.json`: 5,492 current script files parsed, no structural errors, no script BOMs, and no invalid UTF-8. Includes scripted-definition and event-ID checks. The parser supports anonymous native lists and typed colour blocks. This is a structural check, not an engine grammar guarantee.
- `reference_candidates.json`: no unresolved literal custom boolean effect/trigger calls in the scanned current sources. Dynamic references and historical reachability are outside this narrow proof.
- `regression_results.json`: 52 executed scripts, 48 passed. This includes all 15 Space Race scripts, nuclear intelligence, uranium/nuclear integration, colonial transactions, guest workers, RP/GC tools, recipient consent, Suez, French agreements, Spain and the Gulf membership transactions.
- `quality_tests.json`: 11 passing targeted emitted-AST regressions for repaired delimiters, native syntax, scope boundaries, saved DDR migration, zero-energy arithmetic, concrete seat effects and interleaved scheduled rankings. Model persistence is not a native save/reload test.
- `python_syntax.json`: modified Python generators and audit helpers parse without executing their build side effects.
- `test_logs/`: actual captured output, including failures. No frozen reference hash was changed to force a pass.
- `final_source_checks.json`: `git diff --check` passes for 175 scoped tracked paths; the duplicate upstream helper bodies compare equal.

The initial scan found one duplicated upstream helper, `clear_sabotaged_resources_if_necesary`, in two native files. Its two bodies are equivalent; it was left unchanged. No duplicate event IDs or script BOMs were found in the final structural scan.

The ranking test executes several countries in both orders, repeats calls within one day, preserves saved global cache state, advances the day, and checks emergency quarantine. Its reduction is structural: H weekly scheduled world-ranking calls become at most one shared scheduled pass that day. It is not an FPS measurement or a network/OOS test. Players cooperating in the same country still share that country's selections.

The final frozen native attempt reached 9 January 1970, 05:00. It completed startup, the first daily pulse, and a weekly pulse with a nonzero treasury and the Cold War equilibrium initialized. The harness stopped it after 602.6 seconds; `stopped_by_probe = true` explains its termination return code. No spontaneous crash was observed during that bounded attempt. All 11,245 copied source files remained unchanged. This did not cross the first monthly boundary.

The frozen copy predates two final AST-tested refinements: explicit pulse-country oil aggregation scopes and guards for absent optional French reservation targets. Concurrent German diplomacy edits also supplied a recognition helper after the copy was made. The snapshot's missing-helper diagnostic therefore does not describe the current checkout. Do not call this a native test of every byte of the final working tree.

## Checks that remain unresolved

1. Three currency validators stop at an integrity mismatch for `common/ideas/AA_law_expanded_economics.txt`. This mismatch was already present in the initial test run. They cannot establish their downstream claims until their expected transformation chain is reconciled with the current legitimate economy edits.
2. The reserve-currency example has 31 passing tests and one assertion that live economy files must match its earlier snapshot. Its saved hashes do not describe the current integrated economy. This is an example-integrity failure, not evidence that all live currency behavior passed.
3. Two older German differential performance scripts require an explicit pre-optimization source snapshot. They were not counted as passing standalone tests.
4. Earlier native attempts crashed before startup and on 6 January 1970. They included active source edits and database reloads; the crash cause was not established. Do not attribute those crashes to a particular repaired feature solely from adjacent log lines.
5. The final frozen run is a bounded single-process observer smoke test. Human-only Space Race activation, real simultaneous clients, rehosting, native save/reload and the first monthly boundary remain unverified. The frozen run can also lag concurrent edits from other chats; compare its copied sources with the live checkout before treating its diagnostics as current defects.
6. Native logs retain older MD/scenario warnings, including obsolete country references and character/portrait notices. They were not silently removed or classified as harmless without a reachability review.
7. The frozen run also reports a recognition-threshold inline math expression defaulting to zero in `01_international_systems_effects.txt`. The operator and named collection exist in the installed source/documentation, so its underlying loading/evaluation failure remains unresolved. This needs a focused native UN/recognition test; a successful reference lookup alone does not prove the threshold calculation.

## Required multiplayer rehearsal

Use identical checksums and at least two clients. Exercise separate human countries and a same-country co-op pair. Test simultaneous offers, competing crew invitations and world-first awards; reject or suspend agreements; change governments or controller countries; lose control of programme states; exhaust budgets; and save/rehost with pending missions and offers. Verify both parties' money, assets, spirits and selections after rejoining. Cross at least two weekly pulses and the January/February boundary while comparing error logs and simulation speed with the new windows closed and open.

## Evidence and provenance

Primary evidence is the current checkout, emitted native scripts, captured model runs, and the installed HOI4 1.19.3 engine and its generated `documentation/effects_documentation.md`, `triggers_documentation.md` and `dynamic_variables_documentation.md`. Modifier tracing follows `mdcw_cw_apply_pps`, which reads `modifier@drift_defence_factor`. No new historical policy or balance programme was introduced.

These repairs and audit tools were authored for this project with Codex assistance. Existing Millennium Dawn, Moveably, quaZa and other source notices were retained. Original individual authors or permissions not identified in the existing files remain unknown. The project marker does not establish ownership or grant a licence. Applicable terms and credits remain governed by `IMPERIA_COLD_WAR_NOTICE.md` and the existing source licences. Linked graphics, maps, audio and event-frame pixels were not edited by this audit.
