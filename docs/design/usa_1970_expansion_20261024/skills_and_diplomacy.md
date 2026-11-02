IMPERIA COLD WAR

# USA expansion: skill review and diplomatic architecture

Review date: 24 October 2026. This is a source-led concept review, not a gameplay implementation or a live multiplayer certification. All 25 installed `mdcw-*` skill entrypoints were reviewed for relevance. Historical precedents, proposed policy choices and numerical balance still to be calibrated are distinguished below.

## What the project skills imply

| Skill | Application to this request |
| --- | --- |
| mdcw-national-trees | Deep programmes with meaningful continuation. Preserve existing elections, leaders, institutions and exact party gates. Strengthen current forks before multiplying them. |
| mdcw-content-review | Compare complete reachable alternatives, their timing, costs, follow-ups and stacking. Both choices should be desirable. A drawback on every individual focus is not required. |
| mdcw-rework-brief | Separate real January 1970 institutions, plausible alternatives and game balance. The requested concept does not authorize automatic runtime changes. |
| mdcw-modifier-audit | Trace actual reward providers and consumers. Names, sprites and variables alone do not establish working effects. Inspect prospective terms while their execution conditions are false. |
| mdcw-tree-layout | Every focus, including locked and opposing-party branches, remains inspectable. Preserve AND/OR prerequisites and use a common coordinate model for the eventual code and preview. |
| mdcw-events-decisions | Real recipient acceptance controls the transaction. Revalidate target, cost, requirements and replay state when executing. Focus offers and recipient responses are separate stages. |
| mdcw-economy-streams | Separate setup payment from weekly running expenditure and any actual recipient income. Follow the native money consumer. Maximum five fractional digits in budget literals. |
| mdcw-party-names | Use real US parties and registered native exact-party requirements. Do not populate irrelevant MD outlook slots with invented parties. |
| mdcw-localisation | English political and institutional names and descriptions. Effects expose concrete numeric terms, signed modifiers, spirits, assets and unlocks. Keep bookkeeping out of ordinary player prose. |
| mdcw-country-ai | Historical AI and alternative AI need coherent, reachable routes. A human recipient's agreement cannot be accepted by an AI fallback. Human authority and existing game rules persist. |
| mdcw-lifecycle-check | Check the actual 1970 start and every integration surface. Existence of a file or an earlier report does not prove current readiness. |
| mdcw-quality-audit | Review transitive execution, UI, recurring workload, state restoration and RP authority. Parsing is not network-stability evidence. |
| mdcw-edge-case-review | Challenge duplicate clicks, co-op, simultaneous offers, refusal, expired pending offers, sanctions, war, government changes, country disappearance and rehost. |
| mdcw-tick-profiler | Keep recurring checks bounded to relevant countries and signed programmes. Source operation estimates are not native timing measurements. |
| mdcw-test-plan | A future native test needs two independent humans, actual event arrival, treasury/weekly changes, paired spirits, suspension/restoration and no repeated one-time grants. |
| mdcw-validate | Use applicable existing checks after inspecting their write behavior. Separate current checks from old snapshots and engine tests. |
| mdcw-search-filters | Eventual economic, political, research and foreign-policy additions need useful registered filters; spending AI checks do not replace transaction guards. |
| mdcw-leaders | Conditional: use only if the military continuation includes actual commanders/advisers. Avoid importing post-1970 celebrities into the starting roster. |
| mdcw-namelists | Conditional: preserve real US service traditions if named formations become part of the design. Do not change the OOB merely to satisfy a template. |
| mdcw-scripted-gui | Conditional: existing events and decisions may suffice. A new diplomacy window is not required; any later GUI needs complete donor geometry and authoritative execution guards. |
| mdcw-standardize | No broad formatting change requested. Preserve IDs, graph semantics, markers, encoding and generator ownership during any later implementation. |
| mdcw-changelog | No changelog edit is required for an unimplemented concept. Later entries must describe verified behavior. |
| mdcw-dev-diaries | No diary or publication requested. Concept previews must not be described as live game screenshots. |
| mdcw-github-workflow | No commit, push, issue edit or PR is implied by this analysis request. |
| mdcw-maintain-skills | Reviewing skills does not ask to install or rewrite them. No global instruction changes are needed here. |

The national-tree skill's Soviet reference contributes programme ownership, leader variation, thematic reward bundles and follow-up decisions. Soviet institutions, focus counts and numbers are not a USA template. Cuba contributes a reusable consent/lifecycle pattern. Its 120-focus ceiling and Cuba-specific workforce restrictions do not apply to the USA.

## Existing US diplomacy is a foundation

The US tree already has recipient-controlled diplomatic channels. An expansion should consolidate and deepen these rather than create parallel copies.

1. `common/scripted_effects/USA_1970_nixon_diplomacy_effects.txt` dispatches China backchannel, SALT, Beijing summit, Moscow summit, Okinawa consultation, ARVN assistance and Vietnam-talk invitations. The dispatchers generally mark an offer and route an event without granting the material benefit themselves.
2. `events/USA_1970_nixon_diplomacy_events.txt` contains the real acceptance/refusal options. Events `.1` through `.6` begin at lines 9, 80, 153, 228, 304 and 381 respectively. China/Soviet/Japan acceptance mostly gives the recipient 25 or 50 PP, 1 or 2 percentage points of stability and opinion. The USA receives persistent domestic/federal modifier changes. These six acceptance options do not grant paired named agreement spirits.
3. `common/scripted_effects/USA_1970_scripted_effects.txt:342` onward registers theater, Atlantic, Israeli, Arab and commercial acceptances. From line 429, generic dispatchers offer Atlantic burden sharing, triangular trade, Arab trade, Israeli assistance, mediation, maritime basing and North American trade. `events/USA_1970_events.txt` offers acceptance, counteroffer and refusal. These already offer RP interaction, but partner flags, counters and opinion changes often carry more of the relationship than visible paired institutions do.
4. The Israeli package already calls native AIPAC and money-package effects. Reuse that relationship and audit the called costs instead of adding another independent payment or prestige loop.
5. Vietnam-talk invitations are invitations. The existing `.7` and `.8` responses convene talks without automatically imposing a peace settlement. Preserve this distinction.

The opportunity is substantial: countries should receive a useful, named institution with specific benefits and obligations. The USA should gain a distinct benefit only from an accepted programme, not simply from sending an offer. Follow-up implementation can replace or migrate overlapping permanent modifier rewards, so the same historical deal does not pay twice.

## Concrete cautions in the current donors

- `common/scripted_effects/COLDWAR_USA_gulf_effects.txt:998`, `:1055`, `:1180`, `:1184` and `:1215` contain daily treasury literals with more than five fractional digits. Examples include `-0.0035714285714285718` and `-0.0071428571428571435`. These conflict with the current weekly-unit and precision contract. This is source evidence of the mismatch, not an observed native-parser failure. Do not copy this billing pattern into new standing treaties.
- `common/scripted_effects/00_money_system.txt:812` owns `calculate_additional_income_rate`; line 3670 owns `calculate_additional_expense_rate`, whose accumulator is named `additional_expenses_rate`. They reset the respective totals and already include bilateral subsidy totals. Direct searches did not find USA_1970/COLDWAR_CUB treaty streams in this file. This does not prove that no indirect native subsidy flow exists. A new flat weekly charge or transfer still needs a provider-to-consumer trace and exact one-time aggregation.
- Okinawa in this map is split. `history/states/618-Okinawa.txt` starts the populated island under JAP, including its 1970 dated block. `history/states/827-Okinawa Base.txt` starts the separate base state under USA. Existing Nixon event `.5` grants modifiers but does not transfer either state. A proposal must not promise to return the whole island as if it were currently US-owned. Consultative basing arrangements are a better initial fit; any actual territory change needs explicit map-specific design and consent.
- `events/COLDWAR_USA_bahrain_base_events.txt:41` transfers state 624 after Bahrain accepts. This is a territorial agreement, not an existing example of paired beneficial treaty spirits. Its presence does not justify automatic transfers in the proposed diplomacy expansion.

These are review findings only. This document makes no changes to runtime files.

## Reusable consent and lifecycle architecture

The current Cuba contract implementation is the strongest local structural reference:

- Generator: `tools/cuba_1970/foreign_contracts.py` separates previews, offer dispatch, acceptance, refusal, cancellation and reconciliation.
- Loaded offer: `common/scripted_effects/COLDWAR_CUB_1970_foreign_contracts.txt:3` creates a 90-day pending offer. It does not make the standing treaty expire after 90 days.
- Loaded transaction: the same file at line 210 applies the accepted Soviet agreement through its validation trigger, charges its setup terms and records signatures. Refusal begins at line 549 and cancellation at line 710.
- Paired lifecycle: the same file at line 959 adds or removes the two named spirits together, preserving signatures and one-time receipts.
- Bilateral checks: `common/scripted_triggers/COLDWAR_CUB_1970_foreign_contracts.txt:3` checks both native embargo directions and both countries' mirrored diplomatic, financial, economic and military sanction arrays. Line 187 begins the recipient-time acceptance checks.
- Recipient controls: `events/COLDWAR_CUB_1970_foreign_contracts.txt` and `common/decisions/COLDWAR_CUB_1970_foreign_contracts.txt` expose real accept/refuse decisions. Both signatories can terminate a signed agreement.

For the USA, propose a common contract with separate country offers, not a generic US menu that silently selects and signs partners. A signed standing treaty lasts until termination and can suspend during bilateral war, embargo or sanctions. Restore its spirits without replaying money, buildings or research grants. Temporary programmes keep their explicit agreed duration. Their deadline must not reset through suspension, reload or reconciliation. Duration semantics should be shown in descriptions and exact terms before acceptance.

Dependent projects require an actual active parent/membership spirit. Talks and admission remain reachable before member-only content. Exact prospective benefits for both countries stay visible while locked, unsigned, refused or suspended. The acceptance option and focus inspector must show identical setup cost, weekly cost, spirit modifiers, assets and research uses. Every construction level comes with one extra shared slot in the same checked state before construction.

## Ten partnership directions

These are programme directions, not a final numerical balance manifest. Proposed benefits must use verified MD providers and be calibrated against whole compatible US routes.

| Proposed programme | Partner and duration | Distinct benefits | Plausible cost or tension |
| --- | --- | --- | --- |
| NATO Standardisation Agreement | GER, standing | Limited doctrine/research and equipment-standardisation gains for both | US support appropriation; German equipment or personnel expense. Genuine NATO membership needed. |
| North Atlantic ASW Programme | ENG, 365 days | Both gain naval experience and limited naval doctrine/training rewards | Naval operating expenditure for each partner. Renewal requires a new agreement rather than replaying initial rewards. |
| Expand the Auto Pact | CAN, standing | Civilian productivity and sector trade gains for both | Industrial integration and administration costs; existing 1965 treaty is deepened rather than newly invented. |
| Border Industrial Development | MEX, standing | Mexican factory/slot and industrial training; US commercial/productivity benefit | Paid US investment and recipient education/integration expense. No automatic workforce transfer. |
| Pacific Alliance Consultation | JAP, standing | US logistics/influence defence; Japanese civilian/defence research continuation | US basing flexibility and operating burden; Japanese defence costs. No automatic ownership change. |
| Strategic Stability Framework | SOV, 730 days | Tangible savings or civil-science cooperation for both | Real agreed strategic restraint only if the existing nuclear mechanics support it. A global war-support penalty alone does not implement SALT. |
| Commercial Opening to China | CHI, standing after accepted backchannel | Both gain limited commercial and civilian production outcomes | Conversion/integration cost and domestic political tension. No automatic Taiwan status or recognition change. |
| ARVN Advisory Mission | SVN, 365 days | Recipient receives training, organisation/logistics or paid equipment; USA gets experience and limited doctrine benefit | US funding/personnel burden and recipient operating costs. No automatic US war entry. |
| Defensive Supply Agreement | ISR, 365 days | Real recipient delivery/training; US export or doctrine benefit | Appropriation, delivery and recipient support costs integrated with the current package/AIPAC system. |
| Rogers Mediation Initiative | EGY and ISR, staged 90/180-day phase | Accepted talks can lead to separately consented reconstruction and stability | Both relevant humans must accept operative settlement terms. US acceptance of a focus cannot impose borders, peace or Suez reopening. |

Do not make China opening and Soviet detente mutually exclusive: their simultaneous pursuit is central to the historical strategy. Likewise, do not exclude every Israeli relationship from all Egyptian or Arab commerce. Strong exclusions belong between competing commitments or programme terms, such as competing appropriations, constrained force postures or an exclusive arms pledge versus neutral mediation. Ordinary complementary development remains shared.

## Primary historical records

The following links are historical evidence, not numerical balance sources. Modifiers, costs and durations in the proposed design remain game-balance choices.

- [NATO Defence Planning Committee, 16 January 1969](https://www.nato.int/en/about-us/official-texts-and-resources/official-texts/1969/01/16/final-communique): conventional improvements, budget resources, balance-of-payments burdens, the 1969-1973 force plan, an on-call Allied Naval Force and common infrastructure. This supports defence cooperation with real funding choices instead of free global combat buffs.
- [Canada-US Automotive Products Agreement, official treaty record](https://www.treaty-accord.gc.ca/details.aspx?id=100604) and [full treaty text](https://www.treaty-accord.gc.ca/text-texte.aspx?id=100604): signed 16 January 1965, provisional application the same day and entry into force in September 1966. The 1970 concept should expand existing sector integration. Modern NAFTA is not its historical identity.
- [Kissinger memorandum to Nixon on Okinawa, 12 March 1969](https://history.state.gov/historicaldocuments/frus1969-76v19p2/d4): explicitly weighs the political cost of continued administration against the military flexibility lost through reversion, and discusses costs and defence responsibilities. This is a credible basis for two attractive negotiated arrangements with different costs.
- [Rogers memorandum on the Sato visit, 14 November 1969](https://history.state.gov/historicaldocuments/frus1969-76v19p2/d23): links Okinawa, bases, nuclear storage and textiles. It supports consultation and commercial follow-through rather than a PP-only reward.
- [Rogers Plan editorial record, December 1969](https://history.state.gov/historicaldocuments/frus1969-76v12/d104) and [FRUS Arab-Israeli Dispute, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v23): identifies real negotiation tracks and local disagreement. A successful settlement remains an RP alternative requiring the affected parties.
- [US-Saudi economic commission telegram, 6 March 1974](https://history.state.gov/historicaldocuments/frus1969-76ve09p2/d104): describes economic, strategic and technical cooperation and the policy tension over guaranteed oil supplies. A named 1974 joint commission belongs to later continuation, or must be marked as an early negotiated alternative if made available in 1970.

## Remaining evidence boundary

No game was launched for this skill/diplomacy review. No live event delivery, weekly budget execution, tooltip rendering, save migration or multiplayer rehost was tested. The concept should be independently reviewed for cumulative compatible rewards and preview completeness before implementation. Existing old markers, old pictures and unrelated runtime issues have been left unchanged.
