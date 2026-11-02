IMPERIA COLD WAR: US-Soviet Competition and Negotiated Agreements
================================================================

Status: researched design proposal, 24 October 2026. No runtime changes.

Current scope is superseded by `USA_SOV_DOSSIER_DESIGN.md`: only existing game actions are permitted in the revised dossier. The custom treaty restrictions and focus integration below remain earlier research/design material, not the current implementation plan.

The purpose is to make actual superpower commitments visible and negotiable. Competition should arise from equipment, troops, access, money, sanctions and strategic forces already present in the campaign. An agreement should exchange concrete commitments rather than award a new abstract national bonus.

## Current US tree

The installed `common/national_focus/USA_1970.txt` declares 229 local focuses: 50 Nixon focuses, 113 election-module focuses, 51 shared focuses including Bahrain, and 15 Gulf focuses. These are source declarations, not a count of simultaneously reachable choices.

The tree has a useful domestic structure: federal administration, inflation and the dollar, drugs policy, Vietnam, foreign policy and military recruitment in Nixon's opening; later Democratic and Republican election programmes; shared industrial, energy, social, foreign-policy and military branches. Its main weakness for this assignment is the limited connection between diplomatic titles and continuing bilateral obligations.

| Source | Observed behaviour | Design implication |
| --- | --- | --- |
| `common/national_focus/USA_1970.txt:1322`, `USA_1970_NIX_F2` | Linkage and SALT deducts 10 treasury units and sends a Soviet offer. The focus is limited to Nixon's first term. | Keep this political entry, but connect it to persistent negotiations usable by later administrations. The current expenditure is not evidence of a calibrated negotiation price. |
| `events/USA_1970_nixon_diplomacy_events.txt:79` | Soviet acceptance gives both countries 25 PP and 1% stability, with additional American political effects. It establishes a channel, not a strategic ceiling. | Separate opening talks from signing and implementing an arms agreement. |
| `common/national_focus/USA_1970.txt:1403`, `events/USA_1970_nixon_diplomacy_events.txt:227` | The Moscow Summit requires the accepted channel and a date after 20 May 1972, deducts 15 treasury units, then offers another agreement. Acceptance changes political and research variables. | A summit should present a concrete pending package rather than independently create another treaty-like reward layer. |
| `common/national_focus/USA_1970.txt:2781` | Arms Control with Readiness changes stability, personnel costs, influence defence and war support without sending an arms-control offer. | Reuse the focus as an administration's route into actual negotiations. |
| `common/national_focus/USA_1970.txt:3537` | Negotiate from Strength changes influence, planning, war support, stability and personnel costs. | Preserve its domestic programme where appropriate, but make the promised negotiation a real action. |
| `common/national_focus/USA_1970.txt:6030`, `events/USA_1970_events.txt:129` | Triangular Diplomacy already offers a native improved trade agreement to a recipient. | Reuse the actual MD trade mechanism where relevant. Do not present it as a guaranteed resource shipment or treasury payment. |

This is a targeted structural and diplomacy review. It is not an exhaustive balance, focus-layout or modifier audit of all 229 focuses.

## Existing Soviet and shared foundations

- The Soviet tree already contains SALT negotiations, SALT I/ABM, the Moscow summit, Vladivostok, Helsinki, SALT II and an INF offer. Soviet SALT I and SALT II are genuine recipient-choice events, but their visible execution supplies ideas and tension changes rather than counting or reducing weapons: `events/COLDWAR_SOV_1970_events.txt:3889`, `:4075`.
- `COLDWAR_SOV_arms_limitation` gives a 10% military-spending cost reduction and a war-support modifier. `COLDWAR_SOV_salt_ii` gives another 5% spending reduction: `common/ideas/COLDWAR_SOV_1970_ideas.txt:837`, `:871`. These are exactly the sort of broad savings that should not substitute for actual force restrictions in the new design.
- A third route already exists: `mdcw_cw_dec_detente`, `common/decisions/mdcw_cold_war_decisions.txt:250`. It costs 75 PP, changes tension and applies a temporary domestic spirit. Two bloc leaders taking the initiative within 90 days receive a year-long Detente idea through `mdcw_cw_detente_initiative`.
- Consequently, US offers, Soviet offers and the shared initiative must converge on one bilateral agreement record. Adding a fourth independent reward route would compound the fragmentation. Existing receipts need a deliberate migration; do not replay payments or destroy existing saves' assets.
- Shared assistance already stores donor/recipient links, programme type, size, state and end date. It is suitable as a source for an activity ledger. A programme's bonuses are not evidence that weapons or divisions were transferred.
- Shared hooks already handle wars, volunteers and coups: `common/on_actions/mdcw_cold_war_on_actions.txt:43`; `common/scripted_effects/mdcw_cold_war_effects.txt:4846`. Existing tension changes must not also be charged by the new observer.
- The existing monthly tension calculation tends toward a baseline derived from 40 and sanctions: `common/scripted_effects/mdcw_cold_war_effects.txt:3832`. It is not presently a pure record of US-Soviet acts. Keep that distinction visible; changing the global model affects other countries and is a separate balance decision.

## Proposed player interface

Add a small Superpower Relations section to the existing Cold War window, with two views: Activities and Agreements. It needs no new competition currency, victory points, trust score or automatic hostility programme.

An activity row contains the actor, recipient, actual action, observation date, evidence category and current state. Examples are an active Soviet lend-lease connection to Egypt, American volunteers in South Vietnam, a suspended military training programme, a new bilateral sanction, or a declared strategic-force expansion covered by a treaty.

Use these evidence categories:

| Activity | Practical first implementation | Display boundary |
| --- | --- | --- |
| Native lend-lease | Read whether the bilateral connection is active. MD already uses `is_lend_leasing`. | Show active arms supplies. Exact equipment, quantities and successful delivery are not established by this trigger. |
| Volunteers and attaches | Existing send/recall hooks and native `has_volunteers_amount_from` / `has_attache_from`. | Show actual presence; publish a numeric count only after the display counter is verified. |
| Existing assistance | Read the actual programme links and lifecycle. | Identify the programme accurately. Training assistance must not be labelled a troop deployment. |
| Specifically instrumented shipment | Record the actual transaction, origin, equipment and quantity when supported by a verified transfer/receipt path. | Distinguish an offer, dispatch and delivery. Never invent a receipt from the proposed amount. |
| Sanctions, war and access | Observe actual existing diplomatic state or instrument its transaction. | Do not infer a war plan from a country's focus title. |
| Covert action or nuclear intelligence | Use established discovery/attribution records, where those records actually support the claim. | Do not reveal an undiscovered operation or the opponent's full arsenal. The current nuclear-intelligence system detects programme activity, not every transfer or precise deployed total. |

Public acts and voluntarily declared support can populate the first version. Some native indicators can expose information beyond the player's normal knowledge; their disclosure policy must be explicit. Do not promise a full intelligence-gated global delivery tracker as part of this small system.

The activities list should register both escalation and withdrawal. A completed withdrawal is as useful to a negotiator as a new deployment. Old reports must not masquerade as current presence.

## Counteractions with actual costs

Selecting an activity opens relevant existing actions or a tightly scoped offer. It does not award a free response package.

- Supply the opposing participant using real equipment from stock, subject to native diplomacy and recipient acceptance.
- Provide a real loan, payment or existing funded programme, with its normal treasury and weekly budget effects.
- Send volunteers or an attache through normal game permissions.
- Seek military access or a base from the actual host government.
- Impose or lift an existing sanction.
- Offer reciprocal restraint in the named conflict, or continue the current commitment.

Every response must remain legal if the same action were attempted outside the ledger. An entry is not a new justification to bypass war, access, recipient or sanction rules. Do not mint free weapons, money, volunteer capacity, construction or influence just because the other superpower acted.

## One negotiation procedure

Both countries use the same procedure: propose terms, accept/refuse/counter, sign, implement, monitor, expire or withdraw. A counteroffer replaces the pending version and requires the original proposer to accept the changed terms. Neither side can approve its own revised package on the other's behalf.

Keep one pending bilateral offer at a time in the first version. Proposed balance defaults are 30 days to answer and 180 days for a regional restraint agreement. These are design defaults, not historical treaty terms. An unanswered offer expires without becoming consent or silently charging an asset transfer.

Terms specify named countries/conflict participants, covered actions or assets, each side's ceiling or obligation, implementation deadline and treaty duration. Store a fixed offer version and a signed baseline. A changed arsenal while talks are open must not quietly change the offered ceiling.

On acceptance, recheck both countries, the current offer version, authority, real asset/funding availability and recipient permissions. Charge and transfer only once. Where a native action cannot safely be executed by the agreement, show Implementation Pending and monitor the player's actual action. Do not mark a promised withdrawal as already completed.

Display both parties' complete prospective native effects in the originating focus and response. Narrative context belongs in descriptions. Obligations belong in the agreement's terms and requirements, not invented modifier bonuses or misleading effect summaries.

## Treaty templates

| Template | Actual exchange and opportunity cost | Scope and limitation |
| --- | --- | --- |
| Regional Restraint Agreement | Both superpowers stop the specified military-support connections and recall the agreed volunteers/attaches for a named conflict. Each sacrifices leverage while reducing the opponent's support. | First use a 180-day template with exact donor-recipient pairs. It does not end the local war or bind another human government. Native `recall_volunteers_from` and `recall_attache` exist; automatic cancellation of every native support channel still needs separate verification. |
| Trade Normalization | Mutually agreed relief from specified bilateral sanctions/embargoes and, when selected, the existing improved trade agreement. | Benefits come through existing diplomacy and actual trade. No guaranteed cash income or fictitious grain commodity. Any loan is a separate real transaction. |
| SALT I and ABM | Freeze the agreed strategic launch capacity and separately limit the strategic defensive systems that are actually represented. Each accepts constraints on future expansion. | SALT I is a launcher limitation, not general warhead disarmament. An initial national-capacity freeze can be a clearly labelled game adaptation. `rocket_site` levels represent regional capacity, not individual historical silos. ABM must not be implemented by restricting every ordinary SAM site. |
| SALT II | Agree a ceiling on an explicitly documented set of strategic delivery systems and relevant sublimits. | Distinguish signature, ratification and voluntary observance. Historically SALT II was signed in 1979 and never ratified by the US. A generic PP reward does not establish observance. |
| INF | Eliminate the covered ground-launched ballistic and cruise-missile systems and monitor the prohibition on rebuilding them. | Historically signed in 1987; the relevant range is 500 to 5,500 km. Equipment must be classified by model and launch role. The loaded ballistic archetypes include models above 5,500 km, so deleting the entire archetype would be incorrect. |
| START I | Reduce agreed strategic forces to explicit ceilings, using actual retirement actions and an implementation period. | Historically signed on 31 July 1991. The original ceilings included 1,600 deployed strategic delivery vehicles and 6,000 accountable warheads, with detailed counting rules. These are historical values, not automatically appropriate mod balance numbers. |

SALT/INF/START need a single authoritative mapping of the loaded stockpile, deployed missiles, nuclear payloads, bombers and naval systems. Native equipment and legacy MD arrays both exist in this checkout; their presence does not establish that both represent independent live arsenals. Retiring inventory must not leave the same weapon active in a deployed unit or remove an unrelated asset. Actual missile consumption during war is not verified disarmament. Moving arms to an ally must not count as treaty destruction.

The first playable treaty can monitor declared national launch capacity and bilateral regional restraint. Exact historical INF/START implementation is the more demanding extension. Do not advertise full triad accounting until stock, deployment and retirement have been tested in the native game.

## Conflict and detente can coexist

An incident should identify the concrete dispute: increased support for a named opponent, a new sanction, a direct intervention, or a violated force ceiling. A high global tension number alone should not forbid opening talks. Conversely, signing SALT must not automatically prohibit all Third World involvement.

Treaties have their own termination rules. Regional fighting or a trade embargo does not automatically terminate an unrelated arms-control treaty. A verified breach creates a visible case and allows a demand for compliance, a counteroffer, the player's own sanctions, suspension of an applicable economic concession, or withdrawal under the agreed rule. No arbitrary national debuff is needed. A political accusation must remain distinguishable from a verified technical breach.

The system cannot guarantee perpetual crises if both players choose restraint. Its continuing interaction comes from new real commitments, changed support, arms expansion and opportunities to trade concessions.

An example sequence is Soviet equipment support for a participant in an active Middle Eastern war, an American response with real supplies to its opponent, and then a proposed reciprocal halt to further supplies. Israel, Egypt, Cuba and any other participant retain authority over their own forces and agreements. The superpowers negotiate only what each actually controls.

## Focus integration and minimum release

Use existing US Linkage and SALT, The Moscow Summit, Arms Control with Readiness, A Verifiable Nuclear Freeze and Negotiate from Strength as routes to the common procedure. Use the existing Soviet SALT, summit and INF focuses on the other side. Keep strategic talks usable after Nixon and across government changes. A new president should not erase an existing state treaty.

The minimum useful release contains the two-view ledger, actual native support/presence observations, proposal/response/counteroffer handling, regional restraint and one carefully defined strategic freeze. Native trade normalization is a compatible existing mechanism. More elaborate INF/START accounting follows the same negotiation procedure once its force mapping is verified. A major new focus branch or separate crisis simulation is unnecessary.

Use transaction hooks where available. Reconcile unhooked native support periodically for USA and SOV, with one shared bounded country pass rather than daily state/province sweeps. Treaty checks should use relevant participants and existing caches. Record transitions once; repeated viewing, save loading or the same continuing shipment connection must not generate repeated tension or payments. Global tension changes must have one owner. UI display state must never grant assets or constitute consent.

## Historical grounding and sources

Historical facts, paraphrased; no source text or images reproduced:

1. [US Department of State, Office of the Historian: SALT I and II](https://history.state.gov/milestones/1969-1976/salt). Talks began in November 1969; SALT I and ABM were signed in May 1972. SALT II was signed in June 1979 and not ratified by the US. Basis for separate negotiations, signatures and compliance.
2. [US Department of State: Soviet-American Relations, The Detente Years](https://2001-2009.state.gov/r/pa/prs/ps/2007/oct/93778.htm). The Kissinger-Dobrynin channel discussed arms, Berlin, Vietnam and other disputes. Basis for a continuing negotiating channel with concrete issue linkage.
3. [US Department of State, Office of the Historian: The Angola Crisis](https://history.state.gov/milestones/1969-1976/angola). Rival aid and intervention strained detente. Basis for simultaneous regional competition and bilateral talks; not a claim that Cuba lacked independent agency.
4. [Ronald Reagan Presidential Library: Themes on the INF Treaty, 27 November 1987](https://www.reaganlibrary.gov/public/2021-01/40-158-7255719-002-001-2017.pdf). Records elimination of ground-launched systems in the 500 to 5,500 km range and verification. Basis for asset-specific elimination and declarations.
5. [George H. W. Bush Presidential Library: White House START Fact Sheet, 31 July 1991](https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/white-house-fact-sheet-strategic-arms-reduction). Contemporary ceilings and detailed accounting. Basis for reductions rather than a spending-discount spirit.
6. [National Park Service: Strategic Arms Reduction Treaty of 1991](https://www.nps.gov/articles/start-treaty-1991.htm). Signing date and physical retirement of launch facilities. Used for retirement examples, not to replace the contemporary treaty's warhead-counting rules.

Publishers/authors: the named US government institutions; individual authors are unknown where the source does not identify them. Reproduction permissions for individual third-party illustrations and embedded materials are unknown. No such assets are bundled by this proposal.

Technical sources: installed IMPERIA COLD WAR scripts cited above; installed main Millennium Dawn diplomacy trigger reference at `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/scripted_triggers/00_diplo_action_valid_triggers.txt:91`; installed HOI4 `documentation/triggers_documentation.md` and `effects_documentation.md` for lend-lease, volunteers, attaches and recall effects. Original MD contributors' attribution remains with upstream files; exact individual authorship is unknown.

Skills applied: `mdcw-national-trees`, `mdcw-rework-brief`, `mdcw-content-review`, `mdcw-events-decisions` and `mdcw-quality-audit`, including the newly installed MD-derived review and transaction guidance.

Verification boundary: source inspection and historical research only. No compiler, game launch, multiplayer test or runtime file modification was performed. The USA and shared Cold War files name historical generators that are absent from this checkout; establish a maintained bounded emitter before implementing generated-file changes. Existing unrelated working-tree changes were preserved.
