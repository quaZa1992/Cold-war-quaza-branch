IMPERIA COLD WAR: COMECON human finance and passive AI safety revision
===================================================================

The user approved passive AI recipients only. AI governments can host or receive an agreed programme but cannot offer capital, sign, choose sites, initiate agreements or join through autonomous decisions. Human funding remains voluntary and belongs to the offering government. This is a multiplayer RP authority rule, not a claim about historical Council voting.

The four saved contract files now have separate Draft, Council Review, Funded Implementation, Partner Programmes and Completed phases. The human chair edits the draft programme and host; each human member changes its own contribution. Submission requires exactly 100% human coverage and eligible sites. It captures the payers, signatories and actual recipients, fixes the quote, and advances the revision. Review Terms records an explicit receipt. Approval and local implementation confirmation require that same revision. Reopening invalidates old receipts and signatures. No price or national contribution can change during review or execution.

Soviet human control presides when available. Otherwise the first actual human Council member in the saved register presides. The automatic clock remains Soviet while that country exists, with a deterministic existing-member fallback. Clock maintenance is separate from project authority. Union republics retain their existing native status check and have no independent Council vote; a human republican recipient confirms its own implementation. No human Union republic is treated as an AI substitute for Soviet finance.

AI passive recipients pay neither capital nor COMECON national service charges. The native weekly expense consumer independently returns zero for AI, including stale saved service rates. Existing ordinary native building/economy costs are unaffected. Train deliveries require a human supplier with real stock. Civil nuclear requirements remain those of the installed nuclear system; the player-only operator-safety offer is not extended to AI through this change.

Confirmed defects and corrections
--------------------------------

| Severity | Trigger and impact | Smallest correction | Evidence |
| --- | --- | --- | --- |
| High | Native AI decisions could finance and approve, committing player projects to autonomous actions. | Human actor checks at decisions, funding and vote effects; zero AI weights; passive recipient consent waiver. | Generated-source regressions and actual native AI negative commands. |
| High | A draft could reach ratification without a sealed review period; mutable terms could invalidate what a delegation believed it approved. | Explicit phase 1 review, captured parties and quote, matching explicit review/signature revision, draft-only mutations. | Native sealed-edit, preview, reopen and stale-signature cases; source guards. |
| High | Generic footer and programme actions read the currently selected file on execution. A later selection could redirect a command. | Literal per-file action bindings and selected-file guards. | Widget-binding validation and native wrong-file contribution rejection. Co-op scheduling still needs real clients. |
| High | A disconnected human financier could become an AI payer of an existing contract. | Daily actual-controller guard, all-payer validation before invoices, pause without moving liability. | Native actual AI financier fixture and legacy migration fixture. This does not simulate a real client disconnect. |
| High | Repeated invoice or completion actions could repeat economic changes if guards were bypassed by an overlapping command. | Phase/period guards before debits, affordability for every payer before any debit, one-time per-recipient delivery receipt. | Native duplicate ratify/prepay, exact liability and completion replay checks. |
| Medium | With an AI Soviet government, a Soviet-only editor would prevent human members from using the system. | Deterministic human chair fallback, separate organisation clock. | Genuine human Hungary scenario with native AI Soviet control. |
| Medium | Legacy AI offers or service rates could survive an AI-only participation restriction. | One-time safety migration, human-only coverage and independent fiscal consumer guard. | Native legacy quote and stale service-rate checks; source regressions. |

Exact source entry points for the corrected paths: `tools/comecon/actions.py:5` (human decision category), `governance.py:7` (human membership), `governance.py:12` (draft-only authority), `governance.py:71` (sealed review), `controls.py:8` and `compact_ui.py:81` (literal file actions), `governance.py:90` (controller guard), `mechanics.py:85` (invoice validation and replay guard), `governance.py:45` (human chair election), `governance.py:51` (legacy migration), and `build.py:248` (human-only weekly fiscal consumer).

Source locations are `tools/comecon/governance.py` for actor, review and migration guards; `mechanics.py` for quotes, captured arrays, invoices and delivery; `controls.py` and `compact_ui.py` for literal file actions; `actions.py` for decisions; `build.py` for the native fiscal consumer. The generated runtime files mirror these sources. The machine-readable source report records current hashes.

Old saves
---------

`cc_safety_v2` migrates older drafts by discarding AI offers and invalidating old signatures. Running agreements retain their price, paid sums, liabilities, recipients and funded-day progress. An old AI-financed agreement pauses during its funded stage instead of silently reallocating the bill. A returning human financier must explicitly review and approve continuation. Completely paid service periods can continue for passive recipients. The revision performs no automatic refunds or cancellations.

Workload and evidence limits
----------------------------

The recurring daily path advances four saved contract counters from one clock. Controller guards inspect the captured payers and recipients of active files. Political checks occur weekly and inspect captured contract parties in both directions, including actual Union recipients. They do not scan all states each day. Council admission is capped at 32 members. These are source-level bounds, not native timing measurements. Normal political suspension can take up to a weekly check; controller and payment failures are also checked on the daily or invoice paths.

`source-validation.json` checks generated native structure, references, encoding, exact widget bindings, file isolation, passive AI authority, fiscal integration and transaction guards. The native safety reports exercise synchronous engine effects under actual human Soviet or Hungarian control and actual AI partner control. Their profile source snapshots record the tested file hashes. Minimal startup replaces unrelated on_actions in the fixture only. The large historical script baseline is frozen, while current COMECON files and the current money/toolbar integrations are overlaid. Feature errors are filtered separately from the inherited full-mod diagnostics.

The native checks cover funded-day arithmetic through bounded explicit calls. They do not cover real calendar order, actual pointer interaction, save/reload, rehost, multiple human countries or co-op clients. A genuine multiplayer rehearsal still needs two human member countries changing their own shares at once, a chair sealing during incoming edits, reopen with delayed acceptance, a financier disconnect and reconnect, and save/rehost in both review and prepaid execution. Verify identical contract revisions, shares, paid sums and remaining days on both clients and check the game's OOS logs. No source or single-client result is a guarantee that multiplayer cannot desynchronise.

Provenance
----------

Authority and safety policy: the user's instructions in this conversation. Implementation: custom IMPERIA COLD WAR code built on the existing HOI4/Millennium Dawn scripted effects, decisions, GUI and economy. Original upstream rights and notices remain in force; separate upstream script permissions are unknown in this record. This revision adds no new third-party artwork, fonts or historical policy claims. Existing asset provenance remains in `tools/comecon/ART_NOTICE.md` and its font/source records.

The retired first Hungarian fixture expected two recipients even when the human financier was also the default host. The correct saved recipient union has one country in that case. All its economic and authority checks passed; the fixture expectation was corrected without changing production membership or recipient logic. The retired reports remain alongside the final reports for traceability.

The first pair of final profiles ended during database loading without reaching assertions. They were retained as `native-retired-safety-*-load-abort.json`. The definitive runs are sequential. The cause of the early process exits was not established; they are not counted as passing tests. A successful fixture deliberately terminates its own game process after the COMPLETE marker, so its recorded process exit code alone is not a crash diagnosis.

Final verification
------------------

The final source suite passed 1,916 structure, reference, widget and safety checks. The definitive native Soviet and Hungarian fixtures each passed all 26 assertions with no COMECON diagnostics. The Hungarian fixture's complete recorded source hash set matches the installed files, including the compact footer containers. The Soviet fixture differs only in the earlier footer container geometry; its authority, financial and lifecycle scripts match the installed version. `safety-evidence.json` records this closure without treating the retired load aborts or corrected fixture failure as passes.

The two definitive profiles terminated only after their COMPLETE marker. They leave existing user profiles and other game processes untouched. Restart the game to load the new scripted interface and effects; older saves migrate through the native initialisation/opening path. This verification is separate from an actual multi-client multiplayer, calendar, save/reload or rehost test.
