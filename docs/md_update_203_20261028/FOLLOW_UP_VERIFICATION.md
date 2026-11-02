# IMPERIA COLD WAR: MD 2.0.3 follow-up compatibility verification

The source update is complete. Full runtime compatibility is **not certified**: an isolated native test on HOI4 1.19.4 reached January 1970 startup and crashed at the first-hour transition before its eight scheduled assertions. The crash report records an access violation. The cause has not been isolated.

## What passed

- The supplied MD folder still has 79,711 files and no path, size or modification-time change since its complete hash pass. The verified source delta remains 73 paths.
- The complete automation interface, callbacks, dynamic checkbox localisation and native agency window match the supplied MD executable tokens.
- 75 automation callbacks resolve to their own native widgets. All 34 dynamic checkbox image providers resolve, including the energy provider in shared money localisation.
- Influence, internal investments, economic budgets and space automation retain their actual daily, weekly and monthly hook calls and unique effect providers.
- Cold War internal investment terms, all four completed nuclear passive-defence receipts, and the SSR agency blocker remain present.
- The current uranium/nuclear integration suite passed 25 tests. The Space Race system audit passed 1,318 source/model checks. These are not native gameplay tests.
- The isolated snapshot contained 11,778 copied files. Neither the snapshot's recorded files nor installed sources drifted during the test.

## What prevents a clean-runtime claim

The engine process crashed before the day-three assertions. Consequently there is no passing native result for the scenario, focus tree, GDP, occupation budget, Jerusalem split or SSR permission checkpoints. Loading startup alone is insufficient.

The engine also reported state-only `is_controlled_by` triggers evaluated in country scope for the four Israel occupation dynamic modifiers, plus Israel array-removal, missing debt-bound and modifier-cleanup messages. These files were not changed by the metadata update. Their retained bytes do not establish correct behavior. The messages are actionable audit evidence, not a proven cause of the crash.

Other inherited diagnostics exist in the full error log. Some may concern inactive content or native parser behavior; they have not all been classified. No blanket harmless-warning exemption is asserted. No named automation diagnostic appeared in this run, but the run did not exercise automation buttons or complete its calendar checks.

## Evidence and remaining work

See `follow_up_verification.json`, `automation_verification.json` and `native_report.json`. Full engine logs, the frozen snapshot and crash files are retained on E: at the exact private paths recorded there. The earlier implementation evidence remains a record of the approved source transaction, not an all-feature gameplay certificate.

Resolve the confirmed scope/initialization diagnostics, isolate the first-hour crash, then repeat native calendar and automation interaction checks. Save/reload, rehost and actual multi-client checks remain outstanding. No user save or Launcher playset was modified; only the probe's own process was launched.

Provenance: verification and this report were authored for IMPERIA COLD WAR with Codex. Existing MD, Imperia and Cold War source credits and licences remain applicable. No third-party artwork or runtime content was changed by this follow-up.
