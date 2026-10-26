# Cyprus 1970 runtime

Implemented in the mod on 2026-10-16. Prefix: `COLDWAR_CYP_1970_`; event namespace: `COLDWAR_CYP_1970`. All new game-facing localisation is English. The earlier JSON, diagrams and research in `docs/cyprus_1970_design` remain the design/research snapshot; generated runtime files are now the executable implementation.

## Content

- 295 focuses at the reviewed design coordinates; six substantial governing-party programmes, 39 Turkish Cypriot focuses and 22 road-to-war focuses. Ordinary mutually exclusive choices remain in the tree; time-sensitive crisis choices run through the dossier and update record-only focus markers.
- 25 existing Cold War focus images selected by the Luna icon agent, reused through registered sprites. All 295 focus mappings and 11 original spirit mappings are in `docs/cyprus_1970_design/runtime_icon_map.json`; additional idea aliases reuse these textures.
- Nine initial country/state spirits: constitutional breakdown, divided command, narrow economy, guarantor pressure, Makarios's authority, fragmented southern markets, northern enclave economies, parallel communal administration and the armed Enosis underground. The first five, parallel administration and armed opposition are country ideas; the two geographical access penalties are state modifiers. Northern Cyprus is not independent in 1970. The two wartime harm definitions are not initial modifiers.
- Six programme modifiers require the exact current ruling subparty. Completed programme variables persist through elections, but inactive parties' programmes do not apply. The nationalist programme supports indices21/22; the coup route also requires actual coup context.
- Budget costs use current annual GDP in MD's billion-unit treasury. Pending unfunded projects provide no benefit, and children require actual implementation. Research bonuses use existing technology categories. Famagusta queues one naval-base level with the original province, owner/control and free-slot guards; construction is not instant.
- Three bounded ledgers track communal tension, settlement progress and coup pressure. Civilian access improves through one shared monotonic relief ledger. Reprisals cause displacement and state damage and revoke earlier communal constitutional/union consent. Reaffirmation restores eligible agreements without replaying rewards. Reconstruction changes only states that actually have shattered-community damage.

## Multiplayer and current limits

An unselected Cyprus defaults to its dedicated historical-AI policy. The lobby rule can reserve an initially vacant human CYP seat. Human control also sets the reservation; temporary AI then cannot select its custom political actions. Native `is_ai` is not treated as a disconnect detector. Pause before seat changes.

All foreign partners are treated as human seats. Proposal events are informational. Accept/decline decisions appear in the recipient's **Cyprus: Current Diplomatic Proposals** dossier and revalidate current actor, human control, Cyprus existence, active offer, crisis instance and applicable conditions at execution. Silence expires unanswered after90days; ordinary refusal does not fabricate war. A substantive relevant GRE/TUR/ENG response records the guarantor milestone; routine trade does not.

Loans freeze principal at2% of first-submission CYP GDP. Acceptance debits donor treasury, credits CYP treasury and adds equal CYP debt once. Renewals retain the principal. Debt uses the normal budget system; this implementation does not create automatic bilateral repayments to the donor. Current accepted consents are required again for final union ratification, which explicitly ends independent Cypriot play. A withheld ratification can be reviewed later; a new crisis requires reconfirming the framework. British-owned bases do not transfer through union; the separate sovereignty offer requires British acceptance.

Full Greek/Turkish trees and their sponsored-coup/intervention event networks remain the explicitly deferred next stage. This tree supplies proposals, immediate Cypriot responses, actual-war/coup observers and actor-owned integration entry points. It does not schedule a coup, declare a foreign war, create modern troops or automatically release NCY. July/August's amphibious campaign, a temporary ceasefire preserving control, military readiness and a whole-state northern administration require the separately researched military/map adapter. In particular, `war_military_settlement` honestly waits for actual `second_phase_combat` evidence; a Turkish declaration of intent is insufficient.

Modern CYP decisions and weekly events are era-gated. The second modern CYP/NCY diplomatic category is also gated. Native 2000+ history remains intact. The generic1970 fallback and central leader dispatcher preserve the new Cyprus tree and contemporary leaders.

Makarios and Clerides retain their existing portraits. Lyssarides, Papaioannou, Grivas, Sampson and Spyros Kyprianou now have individual photo-based portraits restored with built-in image_gen using the requested colourised phone-photo treatment. They are installed as156×210RGBA DDSs in `gfx/leaders/CYP/1970`; source links, complete prompts and PNG masters are retained in `tools/cyprus_1970/portraits`. `build_portraits.py` performs only native-format export. The unrelated Andros Kyprianou portrait is not used. Initial party popularity retains the existing 1970 world profile; it is not a newly researched vote-share model.

All24 political name/description/emblem slots for both CYP and NCY now have era-specific display hooks, with dated Eniaion/DISY, Democratic Alignment/DIKO, EDEK, CTP, UBP and TKP names. Unattested minor slots are alternate political currents using neutral native outlook emblems. The new dormant NCY roster contains11 political figures and12 TMT/GKK commanders. All23 named northern characters now have individually restored, real-photo-based portraits with a consistent photographic background. The six placeholder faces, two native portraits and eight untreated GKK source cards were replaced in revision2; none remains in the named roster. Anonymous collective administrations use a neutral institutional image without a human face. See [the northern roster and source report](north/README.md), [the exported portrait preview](north/portrait_preview.png) and [the party catalog](party_catalog.json).

NCY is initialized only when it actually exists in the 1970 scenario. This does not create the country, move borders or force foreign decisions. A human's date-based succession is an optional, guarded Leadership Review. Military and advisor dates are separate from country formation and actual cabinet appointments. Later GKK officers are not available in1970, and Turkish invasion-corps commanders are not assigned to NCY. The existing142 Cyprus decisions are supplemented by one northern leadership decision; the manifest reports its separate counts.

## Source and regeneration

Run from the repository or any working directory:

```powershell
python tools/cyprus_1970/compile.py
python tools/cyprus_1970/validate.py
python tools/cyprus_1970/test_transactions.py
python tools/cyprus_1970/test_north.py
```

`compile.py` consumes the approved design JSON/icon map. `rules.py` specifies counterpart, condition and AI policies explicitly; `runtime.py` emits guarded outcomes and dossier interactions; `integrate.py` applies small idempotent edits to existing era dispatchers. Edit those sources, then regenerate. Running the earlier design builder is not required to rebuild runtime.

`manifest.json` lists generated outputs and counts. `integration.json` lists the seven modified legacy files. `validation.json` records structural/reference checks and generated hashes. `transaction_tests.json` records nine focused checks over the actual emitted script AST: insufficient/later funding, duplicate loans, funds/AI/stale/wrong-actor rejection, frozen loan principal, monotonic relief, untouched-state reconstruction, unaccepted-finance follow-up lock, current-party programme enable conditions, and later settlement recovery. These tests model the documented command subset; they are not an engine emulator.

`north/validation.json` records eight additional emitted-script checks for party name boundaries, absent/late NCY, roster availability, leadership review, advisor conditions, portraits and dispatcher protection. `politics.py` owns the48 political display slots, `north.py` owns the dormant character/leader runtime, and `build_north_assets.py` performs only portrait copying, framing and DDS encoding. The seven restored PNG masters already reside inside the project, so asset rebuilds do not require access to the original tool output directory.

## Entry points for later foreign content

Call actor-owned functions from a freshly validated current actor action, not from an archived unguarded popup. All below are new scripted effects, not base-game commands.

| Scope | Entry point | Contract |
|---|---|---|
| GRE/TUR/ENG | `COLDWAR_CYP_1970_<TAG>_publish_response` | Records a substantive current crisis response; human actor only. Caller must own the actual declared policy. |
| TUR | `COLDWAR_CYP_1970_TUR_record_ultimatum` | Records the actor's current ultimatum; does not send forces or declare war. |
| GRE/TUR/ENG | `COLDWAR_CYP_1970_<TAG>_withdraw_current_talks` | Requires its own accepted participation in the current opened talks. TUR withdrawal closes the required Cyprus–Turkey channel; optional GRE/ENG withdrawal records only that withdrawal. |
| TUR | `COLDWAR_CYP_1970_TUR_record_renewed_hostilities_decision` | Requires a current first phase and failed talks. Records the decision and relevant response only; does not create `second_phase_combat`. |
| CYP | `COLDWAR_CYP_1970_record_coup_attempt` | Record an actual externally resolved coup attempt, independently of focus prerequisites. The native successful-coup observer also does this. |
| CYP | `COLDWAR_CYP_1970_record_restoration` | Record actual constitutional restoration; does not appoint a government. The self-owned restoration decision uses the separate appointment helper. |
| CYP | `COLDWAR_CYP_1970_record_settlement` | Called only after actual agreed terms are implemented; checks peace, communal assent and no unresolved reprisals. |

The future military adapter alone owns `second_phase_combat`; it must first verify a real prior phase, an implemented ceasefire/truce and renewed combat. Never infer these from old completed focus badges. A queued future foreign action must carry its own immutable proposal/case context and revalidate it before invoking these current-action functions.

## Validation status

Static checks and nine targeted transaction tests pass. **No HOI4 engine or live multiplayer test has been performed.** A fresh1970 campaign is needed for the new history/initial modifiers. Verify the focus UI, idea refresh after elections, event/decision scopes, hotjoin reservation, save/reload, donor payment deduplication and terminal union ownership in game before a campaign release. The manifest deliberately keeps `engine_tested: false`.

Historical return timing is sourced to [ERT's Makarios return archive](https://www.ertnews.gr/arxeio-afierwmata/epistrofi-tou-makariou-7-dekemvriou-1974/) and [FRUS, document162](https://history.state.gov/historicaldocuments/frus1969-76v30/d162). The bounded1974 acting-Clerides return context applies only to dedicated AI while Makarios is alive. Further causal research and Turkish parliamentary archival references remain in `WAR_HISTORY.md`.
