# South Korea 1970–1990 — installed implementation

Installed into `mdcoldwar-main` on 25 October 2026. The approved 298-focus design is now loaded by the 1970 South Korean country history and protected from the generic-tree fallback. The modern MD tree remains available to its original scenario.

The authoritative inventory and installed SHA-256 hashes are in `COLDWAR_KOR_runtime_manifest.json`. The approved design hash is `4e12530a291d08822eb2d1fa3690a9c0ad8154bab766baa5accbce3353f61d2f`. All 298 IDs, positions, relative anchors, durations, prerequisite groups and exclusions match that design. Eight navigation shortcuts and the approved initial camera are registered. Existing MD artwork supplies all 78 sprite registrations.

## Content

The 14 sections cover the 36-focus democratic transition; Park’s DRP; Kim Jong-pil; the NDP; the Two Kims; Chun and Roh’s Army/DJP; the Unification Socialist Party; student and independent left organizations; the Southern revolutionary party; an exceptional security cabinet; national development; defense; foreign policy; and inter-Korean relations. Starting challenges use eight new national spirits alongside the existing overseas-employment spirit.

Domestic policies write real native modifier values. Each policy has an explicit owner and latest-policy selector. Government changes remove inactive programmes and their recurring commitments; returning owners recover earned policies. Construction, treasury payments, research/experience grants and other one-time effects do not repeat during synchronization. Costs use native treasury changes and weekly budget readers, including spending from zero or negative cash. Reward tooltips are separate from guarded execution so unavailable branches can still show their numerical consequences.

The constitutional route separates an opening, command settlement, negotiations, organizational endorsements, charter choice, majority ratification, electoral administration, an actual election, civilian command and court commissioning. A tied charter ballot fails safely. Legal opposition parties can endorse without first entering government. The one-term presidential model records completed personal terms and retires an incumbent at the following resolved election. Parliamentary and consensus models retain their alternative political rules. Nominations do not install a leader or manufacture votes.

Political entry decisions cover civic legalization, actual revolutionary accession, a crisis-bound security caretaker, a civilian Kim Jong-pil succession and DJP organization before its first election. Revolutionary accession preserves an already established lawful election system. A coalition containing the security service alone cannot authorize the exceptional caretaker. The 1990 RDP merger mandate has a separate organizational response and does not require Kim Young-sam to replace Roh in government.

There are 29 agreement definitions with recipient-controlled acceptance. Sending and refusing do not charge either country. Live offers close after 60 days, with daily expiry recovery and cooldowns. Old office offers, duplicate acceptance, expired multilateral assents and war/subject conditions cannot supply valid agreement rewards. Soviet and Chinese openings have separate signatures and benefits. Cultural contacts, separated families, military notifications, trade and a sovereign consultative framework interact with North Korea. Membership requires actual agreement; it never implies annexation or automatically creates old North Korean paid-contract receipts.

Energy focuses use existing energy/project services and their real prerequisites and budgets. They do not grant reactors, uranium production, fuel or unearned research. Deferred starting armed forces remain deferred.

## Source and integration

The bounded compiler is `tools/COLDWAR_KOR_1970_concept/COLDWAR_KOR_runtime.py`; its politics and foreign modules own their respective outputs. It installs 24 new country-owned files and eight marked integration changes. The manifest lists every path. Shared integrations cover country history, tree fallback, leader and exact-party routing, internal-faction reconciliation, weekly budget readers, four final election-result options plus campaign setup, and the existing North Korean diplomatic bridge. Original shared files were saved once in the compiler’s `shared_baseline` directory (approximately 720 KiB total).

Scripts are UTF-8 without BOM; the single new English localization file is UTF-8 with BOM. Custom blocks carry the searchable Cold War comment. All new runtime identifiers use `COLDWAR_KOR_`.

## Verification and limits

- `COLDWAR_KOR_runtime_validate.py --installed`: PASS. It checks installed hashes and encoding, exact approved geometry and graph, preview/modifier coefficient agreement, definitions and transitive references, decision categories, event scoping, flag providers, portraits/textures, budget hooks and bounded policy lifecycle behavior.
- `COLDWAR_KOR_runtime_scenarios.py --installed`: PASS, 22 scenarios. These execute emitted scripts through a bounded source interpreter, with explicit stand-ins for native helpers. They cover borrowing, recipient payments and weekly income, refusal/expiry, office changes, separate partners, multilateral signatures, charter voting, court commissioning, personal term retirement, nominations, political entry and labor opinion preservation.
- Existing approved overview and normal-scale branch renders remain spatially applicable because the installed graph matches their design coordinates. See the earlier independent layout/reference reviews and `runtime_reference_review.md` for their scope and the implementation closure below.
- No live HOI4 session was run. Source checks do not establish engine loading, exact hover rendering, save/reload behavior or multiplayer event delivery. Choi Kyu-hah and Roh Tae-woo lack dedicated portraits in the available asset pool and use the game’s generic portrait fallback; all explicitly referenced portraits exist.

Fully restart HOI4 and start a new January 1970 South Korean campaign for the first engine check. Verify initial spirits and Park, focus hover/shortcuts, representative construction and borrowing, party departure/return, a charter/election sequence, and a two-player Korean agreement including refusal and timeout. Existing-save migration has not been tested.

## Rebuilding

Run the compiler without arguments to stage, then the two validators without arguments. After they pass, run the compiler with `--install`, followed by both validators with `--installed`. The compiler does not run another country’s generator. Changing the approved design requires rebuilding its corresponding preview separately; runtime-only fixes do not authorize a new layout or rebalance.

## Localization repair — 25 October 2026

Added the missing English names and descriptions for reopening constitutional talks, resubmitting the charter, commissioning the court and reviewing repression cases. Scenario, country-routing and initialization checks in Korean trigger providers are hidden from native tooltips while remaining executable. The compiler preserves these fixes and avoids rewriting identical installed files. Validation now checks every decision/category name and description and rejects exposed routing checks. The installed validation and all 22 existing scenarios pass; comparison with the previous installed scripts confirms identical gameplay conditions after removing display wrappers. Live tooltip rendering has not been rechecked in HOI4.

## English release polish — 25 October 2026

The next screenshot showed that decision prerequisites still exposed country flags even though their titles were localized. `COLDWAR_KOR_presentation.py` now gives all 64 Korean decisions readable requirements, including semantic inverses for negative conditions. The presentation layer inlines existing provider predicates at decision/category call sites, hides technical routing, and retains government, party legality, support, signature and cooldown requirements. Native numeric reward previews are separate from hidden execution so bookkeeping does not appear as a reward.

All 298 focus descriptions received a policy-specific English editorial pass. The canonical narrative sources are `COLDWAR_KOR_prose_politics.json` and `COLDWAR_KOR_prose_national.json`; the approved design JSON remains authoritative for geometry and numerical mechanics. Decisions have edited descriptions and concise institutional consequence tooltips. Requests for party endorsements identify their political interests, while diplomatic retry decisions use the corresponding policy narrative.

Policy upkeep is distinct from conditional agreement upkeep. Small flows display in millions per week; runtime amounts remain in native billions. Agreement text identifies the proposal, consent, contributions, upkeep and duration. The incident-hotline focus now shows policy upkeep of $2 million/week and, separately, agreement upkeep of $0.5 million/week for each government after ratification. Initial acceptance charges remain in native numeric previews and are not duplicated in the supplementary summary. Empty country-only reward previews have been removed.

Installed structural validation and all 22 existing scenarios pass. `COLDWAR_KOR_presentation_validate.py` checks 64 decisions, 418 positive/inverse requirement labels and 298 unique focus descriptions. Canonical executable predicates and effects match the saved pre-polish installed baseline: no gameplay semantics changed. The independent review is recorded in `presentation_polish_review.md`. Live HOI4 tooltip rendering has not been rechecked; restart the game to load the revised scripts and localization.

When rebuilding, also run the presentation validator before installation and with `--installed` afterward. Preserve `COLDWAR_KOR_presentation_baseline.json`, which records earlier executable semantics without storing large file backups.
