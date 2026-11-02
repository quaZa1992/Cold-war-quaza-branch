IMPERIA COLD WAR: USA Triangular Diplomacy and Treaty Integration
=============================================================

Status: implemented integration, 29 October 2026. The twelve-focus expansion and programme clauses are installed in the mod. This document records their mapping to the existing superpower treaty system. Source/model checks and native-asset compositions were used; no game engine or live multiplayer execution was performed.

The player controls Washington's strategy. Beijing and Moscow decide their own responses to American proposals. The two basic channels remain open; Play the China Card and Consolidate Détente are mutually exclusive preferential American programmes.

## Focus and treaty mapping

| American initiative | Existing negotiating instrument | Installed connection |
| --- | --- | --- |
| Détente with Moscow | Nuclear Risk Reduction, slot 7 | Prepares or locates the actual consultation paper and recognises an existing jointly observed agreement. Replaces the duplicate standalone consultation offer. |
| Bilateral Cooperation | Investment Cooperation, slot 9 | Offer the existing bilateral investment protocol alongside an explicitly signed scientific programme. Opening investment terms: cost -5%, duration -5%. |
| Consolidate Détente | Treaty register | The preferential US spirit requires actual joint investment participation and the signed scientific clause. A completed focus alone is insufficient. |
| Grain and Credit | Commercial Accord, slot 8 | Opening trade protocol: bilateral trade opinion +100, relations +25. Attach a funded civilian supply programme. Negotiate loans through native loan diplomacy; no invented grain resource or automatic export cash. |
| Arms-Control Talks | SALT I, slot 1; ABM, slot 2 | Opening SALT terms: nuclear and thermonuclear bomb production -10%, no stored-missile retirement, until withdrawal. Both governments may revise these terms before submission. ABM is a separate strategic-defence consultation paper. |
| Link Benefits to Restraint | Regional Stand-down, slot 10; optional Sanctions and Restraint, slot 11 | Select each core government's own mission recipient. Negotiate actual attache and volunteer recalls. Include the additional economic programme in the reviewed paper. |
| Maintain the American Balance | Treaty register and Soviet activity dossier | Consult, review outstanding commitments, prepare revised packages, and use disclosed Soviet activity to inform the next American offer. |

Research, supply and strategic-consultation spirits are explicit programme clauses in the treaty system. Their complete bilateral numeric effects and GDP-based setup and weekly costs appear in the actual review paper before signature. Opening terms remain negotiable. Signed programme addenda let existing treaties adopt or remove the additional programme without replaying material concessions.

## Authoritative lifecycle

Use the source owner `tools/superpower_dossier/build.py` and its treaty modules. Do not patch generated runtime alone. Existing functions include `icwt_select_<slot>`, guarded `icwt_edit_<slot>`, `icwt_send_<slot>`, `icwt_review_<slot>`, `icwt_sign_<slot>`, `icwt_join_<slot>`, `icwt_leave_<slot>`, `icwt_refresh` and `icwt_weekly`. `icsd_open` opens the dossier. Selecting a focus is never authority to call `icwt_sign_<slot>` for another country.

1. A focus unlocks or prepares Washington's initiative. Locate an existing instrument or pending paper before preparing anything new. Do not overwrite the pending paper, reset an active slot, or automatically send a different revision.
2. Extend the canonical terms, frozen revision, preflight and prospective effects to carry the new programme clause and its actual participant scope. A counteroffer invalidates prior review. Optional third-party membership does not implicitly enrol that country in a USA-SOV bilateral programme.
3. Signature checks the complete current costs and assets for both core parties before committing anything. Apply setup charges, one-time assets and programme receipts exactly once for that instrument and revision. Recipient consent covers the whole package.
4. Programme spirits and weekly funding require the qualifying selected protocols, peace between the two core parties, actual shared membership and their signed programme clause. Apply the same activity test to both countries and all associated funding.
5. Where an existing instrument is only temporarily inactive, restoration must not replay setup charges, old equipment retirement or military recalls. Expiry or termination ends the old programme. A fresh instrument requires fresh review and cannot inherit a historical programme receipt silently.
6. Departure removes the departing country's ongoing treaty effects. Remaining signatories keep their own obligations. End a bilateral programme on both sides if shared core participation ends. Do not refund completed concessions. A departure is not an automatic breach verdict or an automatic sanction.
7. Migrate existing consultation receipts deliberately. Preserve paid assets and standing obligations; do not replay rewards or treat an old, narrower consultation acceptance as consent to new material obligations.

Existing strongest-protocol handling remains authoritative for trade, investments and production restraint. Investment discounts are bilateral native project adjustments, not a global construction-speed reward. Only named stored missile models are eligible for negotiated retirement. The system does not count deployed strategic launchers, remove ordinary SAMs as strategic ABM systems, terminate another country's war, or automatically stop lend-lease.

## Consequences visible to players

The existing Cold War tension value receives reversible relief of one point per jointly observed USA-SOV instrument, capped at five. Do not add another focus-completion reduction. Show a prospective additional point only while fewer than five qualifying instruments are observed. Ending shared participation removes that instrument's existing relief through the same refresh calculation.

Selected sanctions relief costs the imposing government 35 Political Power per existing class actually lifted. Native volunteer recall, if deployed and permitted, costs 50 Political Power and 15 Command Power. Neither is a new money charge. New monetary programme costs use GDP shares and weekly MD budget units.

Existing treaty signature, accession and withdrawal news remain the international announcements. An extra political joint statement needs its own approval. The existing dossier observes actual actions at its native intelligence thresholds; it must not expose secret Soviet choices merely because a US focus was completed.

The approved China exchange remains separate: China receives Productivity Growth +10% and the USA Consumer Goods Factor -3%, both for four years from acceptance. It also applies Bureaucracy Cost +1% and the approved GDP-based programme costs. The exact magnitudes are gameplay balance choices.

## Evidence and validation boundary

Implementation references: `tools/superpower_dossier/README.md`, `treaties.py`, `transactions.py`, `treaty_text.py`, `treaty_integrations.py`, `common/ideas/ICW_superpower_treaties.txt` and the emitted treaty effects. Earlier historical research is recorded in the triangular preview's provenance notice and `USA_SOV_DETENTE_CONCEPT.md`; older proposal documents do not supersede the current generator.

The installed output has independent layout evidence and emitted-AST transaction/lifecycle tests. New focus previews keep complete prospective bilateral terms while locked. The China exchange has both native 1460-day previews and a persistent acceptance deadline. Legacy Moscow migration does not grant consent to new obligations. See `usa_triangular_20261029/IMPLEMENTATION.md`, the layout report, and the owning test reports for precise evidence boundaries. Save migration and multiplayer synchronization have not been tested in the engine.
