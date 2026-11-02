IMPERIA COLD WAR: Superpower Diplomacy Menu
=========================================

Design revision: 24 October 2026. Scope: an independent menu for the USA and Soviet Union. Existing national focuses are outside this design. The supplied interactive concept uses illustrative campaign data, not a live save.

Superseded by `USA_SOV_DOSSIER_DESIGN.md` on 24 October 2026. The current user instruction permits only existing game mechanics. Custom strategic limits, custom counterproposal rules and the separate agreement-state model below are historical proposal material, not the current action catalogue.

## Player experience

A single movable native MD window opens directly for the American or Soviet delegation. It contains three tabs and one selected-item detail area. There is no focus prerequisite, new tension currency, trust score, diplomatic XP, random crisis generator or passive reward spirit.

The header identifies both delegations. The active delegation comes from the actual country being played. Switching countries in the concept's design controls is a preview feature, not a power provided by the in-game menu. The launch control and all authoritative commands are restricted to the actual USA and SOV country identities. Testing only `original_tag` would be insufficient where civil-war countries share that original identity.

The first version supports human negotiations between both countries. If one country ceases to exist or is AI controlled, pending execution is suspended and the surviving human can inspect the record. No AI acceptance, timeout acceptance or disconnected-player proxy signature is introduced. A government or leader change does not erase a state agreement.

## Three tabs

### Activities

The left side lists known commitments and changes; selecting a row shows its actor, recipient, action, evidence, current state and observation date. The right side offers the relevant existing support/diplomacy route or a proposal for reciprocal restraint.

Both American and Soviet activities appear in the same list. Country and action labels make the sides distinguishable without depending on colour. New deployments and actual withdrawal are both recorded. A report of a past shipment remains a dated report, not proof of a continuing shipment.

The initial observer covers native lend-lease presence, volunteer presence, attaches and instrumented assistance transactions. A detected connection does not reveal equipment quantities, a successfully delivered shipment or an undiscovered covert operation. The disclosure policy must be specified per source. V1 can use declared acts and established known connections without pretending that every internally queryable flag is public intelligence.

The UI renders at most six rows per native page. Pagination does not discard active commitments or limit the countries a superpower can support. A short recent-event journal is separate from current facts and treaty evidence.

Counteractions use actual stockpiles, funding, diplomatic permissions and recipient approval. The menu links to the existing game actions. It does not create free weapons, automatically command a third country or simulate a shipment by adding another modifier. The concept deliberately presents these as routes to existing interfaces rather than pretending that a browser button performed a native action.

### Negotiations

The left side lists outstanding proposals. Each proposal detail presents both parties' obligations side by side, duration and reply deadline. Its actions are Review and Sign, Counterproposal, Decline, or Withdraw Proposal, according to who currently owes a response.

The first release has two outstanding-offer slots: one originating from the USA and one originating from SOV. The proposer cannot submit another new offer into its occupied origin slot. A counterproposal remains in the same negotiation and transfers the right to respond. This permits simultaneous diplomatic initiatives without requiring a global winner for creating the first offer.

Use structured clauses, not free-form legal text interpreted by scripts. Initial templates:

- Regional restraint: exact American donor-recipient and Soviet donor-recipient pairs; end named military-support channels, recall relevant volunteers, optionally include attaches.
- Trade normalization: named existing sanctions to lift and/or the existing improved trade agreement. No fictional resource deliveries or guaranteed income.
- Strategic launch-capacity freeze: a clearly defined capacity measure and signed ceilings. Classification and native accounting must be proven before this template becomes executable.
- INF and START remain inspectable treaty templates until their stockpile/deployment accounting and retirement paths exist. Their names alone do not justify an enabled signing button.

The opening concept illustrates Middle Eastern restraint for 180 days and a 30-day reply period. These are design defaults, not asserted historical treaty terms. Date values use campaign time. The real implementation stores deadlines, then derives remaining days for display.

Submitted terms are a fixed version. Countering creates a new version; it cannot silently overwrite an offer that an old signing command would still accept. A changed proposal shows the ordinary player message: "The terms have changed. Review the latest proposal."

Signing is preceded by a compact final review with the exact same bilateral terms. Opening the review grants nothing, reserves nothing and does not count as consent. An amendment names the exact agreement being replaced. The old agreement remains in force until a valid replacement is accepted.

### Agreements

The left side lists signed agreements; the detail shows the obligations of each side and their actual implementation. Separate signing, implementation and compliance.

For example, signing an end to military supplies does not mean that native lend-lease has already stopped. A safely supported recall can execute with the signature if it is explicitly part of the accepted terms. An unsupported native cancellation remains an implementation task until the underlying action actually changes.

The first release has eight active agreement slots. At capacity, require a deliberate replacement or withdrawal. Never discard the ninth agreement, an unpaid obligation or a compliance case. This is an explicit initial scope limit, not a hidden cap on observed activity. Revisit it if a real campaign reaches the limit.

Amendment and withdrawal operate on the selected agreement's immutable identity and version. The historical journal can be bounded; current commitments and replay receipts cannot be evicted while still relevant. A dispute in one region does not automatically cancel unrelated strategic treaties.

## Native layout target

Use a 780 by 700 native window as the initial target, following the existing local MD dossier and Cold War dimensions. Reuse native font roles and real MD controls during implementation. The concept approximates that presentation using original CSS; it does not port a donor frame or establish native pixel parity.

Proposed native geometry: a compact header and bilateral line, three tabs, approximately 270 pixels for the list and the remaining width for a detail area, and a small footer. No full-screen dashboard, world map, continuously animated meter or nested pop-up chain is needed. A final signing review is the only necessary modal.

The concept reflows on narrow screens to remain inspectable in chat. Native UI scale/resolution behaviour requires separate work. Before implementation, inspect the complete chosen donor window and its adjoining buttons, text bounds, list entry templates, first/last slots and conditional states. Do not infer native geometry from the browser preview.

## Multiplayer state contract

HOI4 uses synchronized game simulation. This design does not assume a custom host server, host-only filesystem, remote procedure call service or host-only random decision. Every authoritative state transition must run through the supported synchronized native command/effect path and use the same campaign state on all peers.

### Persistent state

- One schema version and monotonic negotiation/transaction identifiers.
- Two fixed origin slots with current proposal identity, terms version, proposer, respondent, clause enums, named targets, committed terms and campaign deadlines.
- Up to eight active agreements, each with identity, version, accepted terms, parent replacement identity, implementation state and required one-time receipts.
- A 32-entry recent-event ring, using explicit event type and participant fields. No unbounded string or country history growth.
- Deterministic observation facts and a last-completed reconciliation stamp where a periodic observer is necessary.

Offer slot reuse increments a generation identifier; it must not reuse the old identity just because an array position is free. The accepted record contains the actual signed terms. A journal entry or spirit is not the agreement itself.

### Final execution

A gameplay command identifies its actor, action, exact proposal/agreement identity and expected terms version. A model-level command object illustrates the contract; it is not a claim that native scripted GUI supports arbitrary JavaScript-style payloads.

The executing effect validates actor authority, entity identity/generation, version, response ownership, status, campaign deadline, country existence/control, conflicting live commitments, actual price/assets and previous receipt. Only then can it mark the transaction and perform its deterministic, non-yielding effects. Invalid commands leave gameplay state unchanged. Never schedule a delayed event between spending money and recording the corresponding transaction.

This is an all-or-nothing design contract, not a native database rollback feature. Every possible failure must be preflighted. If a native effect can still fail after partial execution, use a staged implementation process that records actual completion rather than inventing atomicity or issuing a refund that creates a second exploit.

An old command cannot become consent to a newer offer. Two co-op clicks can produce one valid acceptance and one no-op rejection. Two incompatible agreements cannot both activate; the second synchronized command sees the already active commitment. The outcome follows the game's synchronized command order, not a client clock or arbitrary actor priority. No same-tick mutex simulation is needed.

### Important native implementation gate

The exact native mechanism for carrying the proposal identity/version from the displayed review to the synchronized effect must be verified. Reading the latest proposal variables inside an Accept callback is insufficient: it could accept terms different from the ones reviewed. A single mutable country-level "reviewed version" shared by co-op clients is also insufficient if one client can overwrite the other's acknowledgement.

Use a supported immutable response context or another demonstrated native mechanism that binds the command to the reviewed terms. If that cannot be proven, freeze the proposal through the native response workflow and prevent replacement until the old response context is resolved. The fallback also needs a stale-context test; a GUI-only disabled button is not proof. Do not advertise version safety from the browser model alone.

### Co-op and display state

Selecting a tab or row, hovering a tooltip, closing a menu and generating a preview do not constitute gameplay commands. No balance, agreement, receipt or payment may depend on which screen is open.

Country-scoped GUI variables may be shared by co-op players. Do not describe them as guaranteed client-local state. Use current native UI scope behaviour, and ensure that gameplay actions name an unambiguous entity rather than whichever array index a co-op partner most recently selected. A co-op draft is a shared national draft unless a genuinely local draft mechanism is demonstrated. Submission validates its exact revision.

AI or third-country actions can alter the observed facts even when both menus are closed. Gameplay facts update independently; only display formatting is suppressed for hidden views. Reopening a menu reads the existing record without rerunning signatures or replaying assets.

## Performance design

| Work | Trigger and bound |
| --- | --- |
| Change a proposal or agreement | A valid explicit action; fixed small records only. |
| Observe instrumented support | The actual start, end, acceptance, recall or sanction transaction. |
| Discover unhooked native connections | One weekly country-level reconciliation for the two superpowers. Read lend-lease, volunteer and attache presence for existing recipients. No state/province or division-location sweep. |
| Check deadlines and implementation | The two offer slots and at most eight active agreements, once per shared scheduled pass and immediately before a command executes. |
| Strategic force accounting | Only when a relevant agreement exists; reuse verified caches and necessary USA/SOV scopes. No claim that all strategic assets are already correctly counted. |
| Rebuild visible text | Data-driven invalidation of the relevant visible view. Repeated hovering or rendering reads cached values. |
| Recent history | Append one real transition, cap at 32 entries, suppress duplicate reports of continuing unchanged state. |

The periodic dispatcher runs once for the pair. Choose a deterministic native anchor, normally USA and SOV only when USA is absent, plus a saved reconciliation stamp. Do not run the world pass for every country or every connected human. Save/load does not clear the stamp or force a second same-period settlement.

For C existing recipient countries, the basic weekly discovery budget is approximately 2 x C x 3 presence queries, before native trigger internals. This is a script-operation estimate, not timing or evidence of negligible lag. Native profiling must measure a realistic campaign with both menus open and closed.

No `dirty` value tied to date/time, per-frame country loops, per-client polling authority, `random_country`, unsaved scratch transaction identity, wall-clock expiry or UI-driven treaty settlement. A data revision changes when substantive data changes. It does not increment merely because a player opened the panel.

The menu creates no additional global tension simulation. Any integration with the existing Cold War tension uses one owner per incident, after a real state transition. The observer must not charge a second change for a volunteer deployment already processed by an existing hook.

## Cases the implementation must survive

1. Both superpowers submit different proposals on the same date.
2. Both attempt to activate incompatible commitments in the same command batch.
3. Two co-op players accept the same offer.
4. Counterproposal, refusal or withdrawal arrives while an old review remains open.
5. An agreement is amended or withdrawn while another client reviews it.
6. The current day reaches the expiry boundary before the command executes.
7. The actual available money or stock changes after review, if a future paid clause is added.
8. A recipient is annexed, changes controller, enters a civil war or stops existing.
9. A delegation becomes AI controlled or the two countries enter direct war.
10. A save is loaded after signing, after dispatch and during pending implementation.
11. A game is saved and rehosted by the other player.
12. A menu stays closed for a long period, then opens with changed observations.
13. A list is empty/full, a selection disappears and an origin slot is reused.
14. A persistent native support connection is seen repeatedly without another real action.

These are acceptance cases, not assertions that native synchronization has passed. Actual multiplayer release testing needs two clients, then a three-client co-op session, concurrent input, the relevant save/rehost paths and a sustained run. Compare the actual authoritative records on peers and investigate any native OOS report. A UI screenshot, source parser or single-client run cannot certify the result.

## Prototype evidence and boundaries

The concept supports activity selection, all three tabs, proposal creation, counterproposal editing, perspective changes through preview controls, final signature review, a deliberate stale-offer scenario, agreement amendment/withdrawal, empty states and close/reopen. Existing native support routes are represented honestly as routes, not executed browser transactions.

An embedded pure state model exercises identity/version checks, response ownership, replay prevention, deadline boundaries, funding preflight, missing countries, AI takeover, conflicting agreements and parent-bound amendments. Its browser and model checks are recorded in the visualization directory's `verification.json`. Those checks validate the design example only. They do not execute Clausewitz scripts, simulate network lockstep or establish desync immunity.

Current verification: 39 design-model and browser checks passed. All three primary views were visually inspected; the browser checks include widths from 320 to 860 pixels, the complete selected regional clauses, a revised offer rejected by an old signing action, and restoration of a signed record after preview reload. Native multiplayer performance and synchronization remain untested.

No runtime mod file is changed by this concept. Implementation should begin with the state/command mechanism and two-client proof, then map the presentation onto native MD controls. Exact INF/START force accounting is a separate provider needed by the same menu, not another minigame.

Sources inspected: local `interface/mdcw_cold_war.gui`, `interface/COLDWAR_DDR_1970_relations.gui`, `common/scripted_guis/COLDWAR_GER_1970_windows.txt`; previously traced native support triggers and HOI4 documentation; project skills `mdcw-scripted-gui`, `mdcw-quality-audit`, `mdcw-edge-case-review` and `visualize`. Existing files are reference patterns, not a certification that every donor line is safe.

Provenance: original HTML/CSS concept and original illustrative campaign data prepared with Codex for this project. No third-party image, texture or native frame was reproduced. Third-party asset licence/permission is therefore not applicable to the illustration. Native MD contributors retain credit for the referenced implementation patterns; exact individual authorship is unknown. Historical treaty sources remain recorded in `USA_SOV_DETENTE_CONCEPT.md` and do not establish native feature support.
