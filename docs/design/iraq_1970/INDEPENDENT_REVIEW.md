# COLDWAR | Independent Iraq 1970 concept review

Reviewed 18 October 2026. This review covers the final approval catalogue and its emitted focus specimen. The reviewer did not edit the authoring generator, catalogue, or loaded mod files.

**Verdict: suitable for concept approval on structure, historical framing and explicit tradeoffs. No confirmed blocking graph defect remains. Runtime integration, historical roster extensions and numerical budget balance remain unimplemented or untested, as the concept states.** This is not an engine compatibility or balance certificate.

## Final snapshot

- Catalogue: `COLDWAR_IRQ_1970_CONCEPT.json`, SHA-256 `9e50677eb90d2a8e827ae19e30b30b0d0037813c079dadce28da7d5780226913`.
- Focus specimen: `COLDWAR_IRQ_FOCUS_SPECIMEN.txt`, SHA-256 `eee89e45c8d71156d445636c7a6fc8ea3d4f1cde223bc5d7f440a4acbe36aafe`.
- **396 focuses, 22 programme areas, 72 decision designs and seven starting-situation cards.** There are 189 proposed paid focus packages, 20 guarded building grants and 24 focuses with additional explicit requirements.
- Resolved focus bounds: x=1–86, y=2–24. Every programme has 18 focuses, with compact, broad, offset or delivery-spur composition. These are catalogue counts, not installed content counts.

## Independent structural checks

A separate brace, quoted-string and comment-aware parser reads exactly 396 focus blocks. Parsed IDs, recursively resolved relative coordinates, prerequisite groups, exclusions and complete availability expressions match the final JSON. This was rerun after the final `industry_steel` position correction to absolute `(50,17)`.

All focus IDs are unique and use `COLDWAR_IRQ_`. Every prerequisite and exclusion resolves. Exclusions are symmetric; the prerequisite graph has no cycle. No two focuses share a resolved coordinate. Decision IDs are unique and do not collide with focus localization keys. The extra-condition ledger has no accidental slug collision between different meanings.

All 396 focuses are structurally reachable in at least one combination of the two internal policy forks; every programme capstone is reachable in all four combinations. That test treats satisfiable external contracts and project payments as possible; it does not claim those conditions automatically occur in a game.

The final graph deliberately mixes AND and OR. Industry, agriculture and society have three delivered domestic components at their capstones. Defence requires `(land OR coastal) AND fuel discipline`. Political/diplomatic capstones retain alternatives. Native grouped prerequisite syntax is preserved rather than flattened.

Negotiated and funded delivery is now on genuine side spurs where refusal or an unfunded early asset would otherwise block all domestic continuation: the first Baath/ICP/KDP/industrial fork, the second PUK/civic/agricultural fork and both oil stages. A completed-but-undelivered focus cannot unlock a dependent focus: each prerequisite group has the matching `_implemented` flag condition, preserving its AND/OR structure. These guards are also repeated in delivery checks.

The war-free route remains reachable with all actual-war, past-war and reconstruction conditions false: contingency plan → armed restraint → crisis channel → civil continuity → civilian budget floor → civilian services → emergency accounts → credit dossier → sanctions-response dossier → peace settlement. The dossiers expose possible responses; they do not require manufacturing a war or obtaining foreign acceptance. Actual emergency production/procurement requires `has_war = yes` both for delivery and ongoing activation.

All final short names begin with a capital and their recorded native glyph advances are at most143px against the147px native text area. This is stronger than counting characters or shrinking global fonts. Browser/engine routing and full visual acceptance remain the separate layout review's scope. During this review I sampled complete Bakr, oil and war branch exports; their full18-node structures, exclusions and joins were visible without card collisions. Earlier browser screenshots were stale, and that mismatch was explicitly reported for regeneration. Final HTML/browser proof must use the rebuilt396-node version, not the superseded468-node exports.

## Historical and political framing

Coverage follows the significant historical parties and leaders. It includes Baath institutions; personal Bakr/Saddam programmes; officer and Arab socialist alternatives; the ICP plus Aziz Muhammad; civilian democratic and constitutional monarchist alternatives; KDP/Barzani and PUK/Talabani programmes; Dawa; later SCIRI/al-Hakim; and the Iraqi Islamic Party. Shared economic, social, military and diplomatic programmes provide continuation under different governments.

The delivered catalogue has no separate Khairi, Amir Abdullah, Baha al-Din Nuri or Central Command national-government trees. The shared ICP congress retains appropriate faction and leadership debate. It does not fabricate a historical sequence of communist Iraqi presidents. Aziz Muhammad's government accession is expressly alternate history. Tariq Aziz retains shared Baath, foreign-policy and continuity content; a distinct18-focus personal Tariq programme is not claimed.

The January start preserves al-Bakr and treats Saddam as the influential deputy rather than an already installed president. The party/leader split, unequal Front participation, coercive administration, oil-backed modernization and Kurdish negotiations fit the documented contemporary setting. A1976 US assessment supports the distinction between Baath control and nominal coalition participation, as well as Soviet cooperation combined with Iraqi external independence. Its information limits and perspective should be retained. [FRUS, Iraq under Baath rule1968–1976](https://history.state.gov/historicaldocuments/frus1969-76v27/d317).

The KDP design separates Mustafa's movement from later Masoud leadership; the latter's official biography dates his election to the KDP presidency to1979. This institutional source establishes chronology, not independent support for territorial claims. [Masoud Barzani official biography](https://www.masoudbarzani.krd/en/biography-masoud-barzani/).

The concept distinguishes living eligible alternatives from dead incumbents, Dawa organization from al-Sadr's spiritual/intellectual role, and founding/later Sunni party figures from Ayad al-Samarrai's youth-organizing role. Named PUK and SCIRI programmes require the later organizations to have formed; they are not initialized as January1970 parties. Iran–Iraq War destruction, Kuwait invasion,1991 sanctions, post2003 institutions and ISIS are not starting facts. Detailed alternative constitutions and numeric policy packages are design proposals, not attributed historical manifestos. Precise unused party slots, executive rosters and office bridges still require integration verification.

The seven starting situations cover regime insecurity, the unresolved north, concessions, agrarian delivery, skills, patronage/parallel commands and the river frontier. Their ownership is appropriate: national problems cannot disappear merely because the governing party changes, while the July regime's active political package is Baath-bound. The .35 literacy input is openly provisional and reuses native education. Its native research, education-cost and productivity consequences must be counted before adding any separate penalty or declaring the starting budget balanced.

## Funding and accumulation

Every paid specimen freezes an invoice from actual `gdp_total`, checks treasury and present delivery conditions, and pays only inside the passing once-only transaction. Invalid delivery creates a pending item with zero reward. The start-accessible retry has an explicit design contract and reuses that invoice and transaction rather than completing the focus again. There is no deposit or artificial refund. Construction, resources, literacy, money and XP are never replayed by programme reconciliation.

The initial raw native-price floor was inappropriate to treat as a1970 affordability guarantee. `common/scripted_effects/IMP_1970_gdp_scripted_effects.txt:1729` sets Iraq's existing target GDP to3.281; lines1829–1830 calibrate its baseline adjustment, consumed by `00_money_system.txt` around6150. A7.5-billion factory reference therefore equals about229% of that starting GDP, and an office reference12 equals about366%. The author corrected the design: those native2000 prices are comparison data only; the actual quoted Iraqi projects use explicit new GDP-share balance proposals. No existing universal historical price factor or native discount is claimed, and no charging native helper is called on top of the authored invoice.

There are meaningful costs, but they are not yet calibrated against a live budget. Completing every compatible industrial focus proposes GDP-share invoices totalling24.5–29% across532 focus-days; these are separately frozen future quotes, not a fixed percentage of starting GDP. Raw full-programme sums for shared sections plus Baath/Bakr include bureaucracy expenditure+.88 to+1.38 before the initial+.18 burden, social expenditure+.30 to+.48 and tax multipliers+.18 to+.30. Those envelopes include conditional packages and are not guaranteed simultaneous active states. They show why an actual1970 budget run is necessary: cumulative administrative costs may be substantially more restrictive than intended.

Policy tradeoffs are substantive: executive discretion versus consent; front versus monopoly; professional versus mass forces; public organization versus overhead; revenue capture versus flexibility; oil specialization versus diversification; service coverage versus recurring expenditure. Positive policy stability uses `min(sum positive active contributions, .15) + sum negative active contributions`. Situation spirits remain separate, so a negative legitimacy cost remains effective even when the positive cap binds.

## Government, contract and implementation boundaries

All active packages read current exact party/office and relevant live conditions. The three currently registered historical families independently checked are Baath/21, ICP/4 and KDP/6; KDP uses the real `emerging_reactionaries_are_in_power` predicate. Other party and office bridges remain explicitly new contracts. Coalition participation is not sovereign governing authority, and a candidature is not actual installation.

Reconciliation derives caches from implemented, selected and currently eligible packages. Earned progress survives departure; active party/leader modifiers suspend and restore on a legitimate return. Durable national construction and literacy persist. Contract-dependent concessions need their agreement flag cleared when terminated; once-delivered settlements need their separately defined persistent ledger. War-only packages become inactive at peace. Same-outlook party switches, actual office changes and save/load must be covered by the refresh integration, not only a generic government-change hook.

Existing effect keys, scopes and consumer proofs are documented in `EFFECTS_REVIEW.md`; this report does not claim every subsystem was independently executed here. The new Iraqi reconcilers, situation arithmetic, political roster/office triggers, policy revision transitions, funded retry and72 usable decision/event providers are still unimplemented. A successful parse does not make those names existing MD APIs.

Before installation, implementation review needs exact situation-component replacements, initialized-law/education overlap, each live condition's setters/clearers, selected-policy revision semantics, truthful native tooltips, full transitive assets/localization and HOI4 government/leader/save/multiplayer checks. The final conceptual structure can be approved while those clearly identified runtime and numerical tests remain the next phase. No game test, exact1:1 engine rendering, or final budget balance is certified by this review.
