IMPERIA COLD WAR: Superpower briefings and treaty negotiations
============================================================

This implements the approved CIA/KGB folder and subsequent configurable-agreement request. The reference is superpower-briefings.html; earlier approval snapshots remain unchanged. The native folder is 790 x 794 with separate CIA/KGB artwork, private regular fonts, narrow index tabs, paperclip, stamps and watermark. No visible date or predetermined historical outcome is shown. All player text is English.

Private native profiles now use `E:/HOI4_Mod_Tools/mdcoldwar/runtime/superpower_dossier`. Retained profiles were relocated to `E:/MDColdWar_Backups/Codex_Test_Archives/2026-10-25/mdcoldwar/tools/superpower_dossier/runtime`; historical reports retain their original recorded paths and hashes. Compact reports and the source generator stay here.

Use the toolbar agency emblem, Shift+I, or Superpower Diplomacy > Open Intelligence Dossier. The dossier is limited to human USA/SOV players in the 1970 scenario. Invited governments use ordinary recipient events and decisions.

## Briefings and responses

USA sees Soviet activities; SOV sees American activities. The addressee is the President or General Secretary. Reports identify the actual provider, recipient, activity and disclosed quantities. Where cached own commitments support a country fighting the reported recipient, the assessment names that connection. Own commitments and correspondence remain separately accessible.

The observer reads existing lend-lease connections, volunteers, attaches, Imperia sanctions, improved trade agreements, foreign construction, assistance, public party campaigns, money/aid correspondence, discovered interference and recurring subsidies. Connections do not establish delivered quantities. Financial detail requires existing native intelligence: 60% civilian intelligence on the provider or 50% network strength in the recipient. No separate agency-strength statistic is added. Undiscovered old payments are not reconstructed later. Correspondence is capped at 24 records per observer.

Response buttons close the file and locate the chosen capital. The player right-clicks that country to use normal diplomacy. Costs, ownership and replies remain in the native action. There is no instruction modal, automatic right-click, replacement money-transfer path or fabricated shipment information.

## Configurable agreements

Eleven named templates plus an independent Custom Agreement: SALT I, ABM Treaty, SALT II, INF Treaty, START I, Reykjavik Framework, Nuclear Risk Reduction, Commercial Accord, Investment Cooperation, Regional Stand-down, Sanctions and Restraint, and Custom Agreement. The title supplies the political subject; selected visible protocols determine the actual effects.

| Protocol | Selectable terms and actual effect |
| --- | --- |
| Covered reserves | None; six nuclear ICBM models; all eleven ballistic models; six cruise models; all 23 loaded models; nuclear-capable models only; or the eleven actual INF-range models. Original 15 plan indices remain fixed for old instruments. |
| Retirement | 0/10/25/50/100% of each covered stored model, rounded to whole equipment. Exact core quantities freeze on sending; invitee quantities freeze on review. Actual equipment is removed once on conclusion/accession. |
| Reserve ceiling | Optional aggregate ceiling at the agreed post-reduction quantity. Weekly inspections compare real covered missile reserves. A breach suspends affected continuing benefits and protection. Excess equipment is dismantled only through the owner's explicit Restore the missile ceiling decision. |
| Core sanctions | None, a diplomatic/financial/economic/military class, or all four. Exact native lift bodies remove both mirrors. 35 PP per class actually lifted, paid by its imposing government. Reimposition of selected classes between USA/SOV is guarded during shared participation. Ordinary embargoes remain separate. |
| Trade | None, +50 trade opinion/+10 relations, or +100/+25, between participants at peace. Overlapping custom accords use their maximum. An existing native improved trade accord suppresses the custom copy. |
| Investment | None, -5% or -10% native investment cost and construction duration between participants at peace. No free buildings or global construction bonus. Existing applicable native investment discounts are considered. |
| Term | Until withdrawal, or 180/365/730/1825/5475 days from conclusion. A guarded scheduled native event ends fixed terms; weekly lifecycle processing provides recovery. |
| Core missions | Recall own attaches, own volunteers, both or neither, from separately chosen American/Soviet recipients. Volunteer recall retains its game rule and 50 PP/15 CP cost if a deployment exists. It does not end the recipient's war. |
| Joint programme | Optional American-Soviet scientific cooperation, civilian supply, strategic consultations or regional economic cooperation. Each requires its associated investment, trade, missile-ceiling or mission-withdrawal protocol, the unlocked American initiative, and the two core governments' reviewed consent. Optional signatories are not enrolled. |

Historical proposal opens a researched starting draft; Custom agreement opens an independent blank instrument. These percentages and reserve ceilings are explicit gameplay adaptations, not historical deployed-force quantities. All editor fields, recipients, invitations and the footer help control explain their scope and operation. Historical precedents and implementation differences are recorded in docs/design/USA_SOV_MISSILE_PROTOCOLS_20261030.md.

Reduction covers explicitly labelled stored reserves. It does not account for deployed launchers, submarines, MIRV attribution or every historical 500-5,500 km class. No separate strategic ABM category was established; the default ABM template is consultation with optional real protocols. Ordinary SAM sites are not relabelled as strategic ABM installations. Lend-lease termination and broader peace terms remain in native diplomacy and RP negotiation.

## Consent, spirits and departure

One immutable pending core paper stores terms, exact quantities, author and new revision. A counteroffer requires a fresh review. The author cannot supply the other government's signature. Both countries' assets, current costs, recall conditions and peace are rechecked before either side's concessions execute. Failure leaves the paper unsigned and resources intact.

At most eight participants per instrument: USA, SOV and six optional invitees. Invitations can accompany the paper or follow conclusion. Invitees review and decide independently, without blocking the core accord. Early acceptance waits for core conclusion; later acceptance is accession. Unrelated native agreements are not silently adopted, cancelled or answered.

Each participant receives the named treaty spirit. The obsolete production spirits have no modifiers and are removed during refresh. New missile ceilings require explicit agreement; old material commitments are not silently expanded. Commercial and investment effects apply between actual participating partners. All twelve slots are reachable through the paged treaty register. Third countries use normal withdrawal decisions.

Individual departure removes only the acting country's membership spirit and continuing effects. Retired equipment, PP and recalled deployments are not refunded. Other governments remain signatories. Treaty-specific international news announces signature, accession and withdrawal. Receipts block replay. Departure from a revision is final for that revision; a new instrument can be negotiated after remaining participation ends.

The existing Cold War tension value receives reversible relief of one point per jointly observed USA/SOV instrument, capped at five. It is removed as shared participation ends or the core countries fight each other. Refreshes and clicks do not award it again. Native sanction-lift tension effects remain in the original lift body. Focus and complete-paper previews show the prospective point for a new joint instrument only, when the system is initialised, fewer than five points are already applied and tension is above zero. The displayed decrease is capped by current tension. Addenda and existing joint instruments do not preview an additional point. This is a non-executing numeric preview of the existing relief, not another focus reward.

### Focus-linked programmes and standing-treaty addenda

The scientific, supply, strategic-consultation and regional cooperation clauses are explicit fields in the immutable negotiating paper. Both countries' complete spirit modifiers, setup costs and weekly balances appear in the prospective effect inspector and the recipient's notification. The American focus opens or locates the negotiating paper; it never supplies the Soviet signature. Current-GDP percentages are fixed by the clause; the exact setup amount is calculated for both governments at conclusion and preflighted atomically before any concession executes.

| Programme | USA setup / weekly | Soviet setup / weekly |
| --- | --- | --- |
| Scientific cooperation | 0.0003% / 0.00002% of own GDP | 0.0003% / 0.00002% of own GDP |
| Civilian supply | 0.001% / 0.00002% of own GDP | 0.001% / 0.00002% of own GDP |
| Strategic consultations | 0.0005% / 0.00002% of own GDP | 0.0005% / 0.00002% of own GDP |
| Regional cooperation | 0.0005% of own GDP / 0.00005% of US GDP | No setup charge / receives the same 0.00005% of US GDP |

These are shares of annual GDP charged at the stated weekly cadence, not annual budgets divided by 52. `icwt_programme_fiscal` resets and supplies `icwt_weekly_expense` and `icwt_weekly_income` in native MD billions/week. The integrated economy provider adds each exactly once. The funding predicate is the same as spirit activation: actual shared membership, the signed programme revision, required protocol, unexpired term, peace, no bilateral embargo and no mirrored Imperia sanctions. Suspension clears both countries' programme effects and their funding; restoration repeats no setup cost. The shared American regional spirit is also retained while the separately consented Chinese regional agreement is active, without stacking its identical influence modifier.

Regional programme funding additionally requires continuing absence of the mission types covered by the signed withdrawal protocol in each government's own named recipient. Mode 1 checks attaches, mode 2 volunteers, and mode 3 both. A missing or disappeared recipient suspends cooperation. Renewed deployment pauses both programme spirits and the matched funding; withdrawing it restores cooperation without repeating setup costs or recalls. The original bare Regional Stand-down remains a one-time recall concession. These programme conditions do not impose sanctions or end local wars. New programme spirits are excluded from native civil-war inheritance.

Standing accords can receive an explicitly reviewed **programme addendum** through the same paper, counteroffer, review and signature path. Their original material protocols, term, membership roster, invitations and material receipts remain intact. A separate accepted programme revision controls new setup receipts. An addendum cannot retire missiles, recall a new deployment, repeat sanction-lift fees or charge an already signed unchanged programme. Refusal/cancellation leaves the standing accord intact. A mutually signed removal ends only the attached programme. Withdrawal or expiry invalidates an outstanding addendum. This gives existing saves access to the new clauses without treating old, narrower consent as authority for new costs.

## Runtime and multiplayer limits

Canonical entry: tools/superpower_dossier/build.py. Observer modules: runtime.py, ui.py, presentation.py, typography.py, integrations.py. Treaty modules: treaties.py, transactions.py, treaty_text.py, treaty_ui.py, treaty_integrations.py, programmes.py, programme_addenda.py, missile_protocols.py and treaty_help.py. Do not patch only emitted files. generated.json records 20 emitted files and six narrow native integrations with hashes. Referenced equipment tokens have a dedicated synchronized token catalogue.

One weekly observer pass for the pair, 15 native investment slots per superpower, and existing assistance/campaign partner lists. The period guard reads the native global day counter. GUI visibility/paging uses disclosed saved caches. No new per-frame world, state, province, division or stockpile sweeps.

Treaties have twelve fixed slots and eight members each. Pair refresh visits actual and previous partners for cleanup, not a world cross product. Each instrument has at most 56 directed participant links. Missile compliance adds at most 2,208 fixed reserve queries across twelve slots, eight participants and 23 equipment models per weekly inspection. These are static operation bounds, not native timings. Signature, accession, departure and scheduled expiry are event-driven. Weekly processing recovers expiry and removes disappeared members.

Terms, revisions, receipts, membership and caches are synchronized saved script state. Display selection cannot sign for another country. Co-op players share their country's page and selection. All observer and treaty integrations have exact provider-preservation checks. No country focus trees are changed by this generator.

This is not a desync guarantee. Source tests and isolated native execution do not establish network synchronization, save/rehost behaviour or measured tick performance. A real USA/SOV multiplayer rehearsal with an optional recipient and simultaneous co-op input remains required before an MP stability claim. The existing money provider's mutable native offer amount is retained; this feature does not certify that provider's concurrency handling.

## Verification and provenance

Run build.py, validate.py, behavior_tests.py, test_treaties.py, test_programmes.py, test_missile_protocols.py, render_preview.py and engine_probe.py --treaties from this directory using Python. Their JSON reports state the precise test scope. previews/ composes emitted native geometry, textures and font glyphs for both country perspectives and treaty screens, including the programme editor/review. These are not live game screenshots.

The engine probe freezes source in an ignored disposable profile, starts and terminates only its own process, and leaves normal saves/profiles unchanged. A STOP file in the reported profile ends the run. Its asset-provider directories are read-only junctions and must never be recursively modified.

art_notice.json records source hashes, unknown individual authorship/licence, the unchanged treaty icon, native event/news donors and local font provenance. Country events retain the native 217 x 163 frame with 180 x 150 inset. News uses the separate 397 x 153 viewport. The generator creates the folder/paper/stamp/control composition and private font aliases, retaining upstream ownership and global fonts.
