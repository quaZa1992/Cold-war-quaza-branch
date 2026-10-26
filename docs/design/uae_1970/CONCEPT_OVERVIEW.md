# COLDWAR_UAE — approved design archive

Status: approved for implementation with “okay reincoden” and now installed. Current code and verification notes are in `tools/uae_1970/README.md`. The concept-phase details below remain as design history; statements about proposed integration or unloaded files describe that earlier phase. The immutable approval is kept separately from executable providers.

The revised concept contains **107 focuses**, **24 mutually exclusive focus pairs**, **40 decisions**, **12 compact programme areas** and **7 starting UAE spirits**. The latest revision starts both countries with the British withdrawal announced in 1968 and corrects the handover programme; the earlier low-oil start and costly extraction remain. These totals describe alternatives, not a single compulsory campaign. Other governing programmes remain visible but locked.

The authoritative design is `COLDWAR_UAE_1970_CONCEPT.json`. `build_concept.py` produces that manifest and the preview from one coordinate model. `PREVIEW.html` is the standalone inspector. The chat preview uses the same data, images and connections. `BRANCH_*.png` are full branches at native scale; `PREVIEW_*.png` show the interactive inspector. These are source reconstructions of a proposal, not game screenshots.

## Starting country

January 1970 uses the existing UAE tag, Trucial States identity, Council leader and Monarchist ruling slot 23. The seven sheikhdoms are represented by the existing Dubai and Abu Dhabi states. Zayed is ruler of Abu Dhabi, Rashid ruler of Dubai; the historical federal presidency follows formation. Their cooperation and different institutional priorities are not presented as rival historical parties.

British treaty dependence, uncertain security after withdrawal, unequal emirate resources, scarce specialists, incomplete services and oil-price exposure shape the opening. The model deliberately does not start with an independent modern federation or its 2000-era national spirits. The existing deferral of starting forces and equipment is preserved.

| Proposed starting spirit | Exact initial contributions | Structural response |
|---|---|---|
| British Withdrawal Announced | Political power gain −10%; existing British subject relationship | Deactivates on actual release from British subject status, separately from federal formation |
| Fragmented Authority | Bureaucracy spending +20%; army organisation −10% | Agreed charter and force integration |
| Unequal Development | Construction −12%; stability −6 percentage points | Charter, development transfers, accession and federal mediation |
| Scarce Specialists | Research −10%; workforce −8% | National training or foreign recruitment, followed by technical institutes |
| Water and Power Constraints | Energy use +15%; civilian sector productivity −5% | Water network, with a continuing energy burden |
| A Narrow Revenue Base | Civilian and office productivity each −10%; only4 base oil units | Expensive physical extraction plus diversification; native oil export prices still apply |
| An Expatriate Workforce | Workforce +10%; division recovery rate −20% | A small military cadre takes longer to restore unit cohesion and readiness |

All values are proposed game balance. They are not historical statistical estimates. Starting-spirit remedies are recorded as owned credits against original components, recomputed independently of completion order and clamped at zero. They do not become extra positive modifiers after the penalty disappears.

## Oil revision: a small start and costly capacity

The proposed new1970 start has **Abu Dhabi3 + Dubai1 =4 base oil**, compared with the inherited **40 +7 =47**: a **91.49% reduction** in raw mapped operating capacity. This distinguishes valuable underground reserves from wells and offshore systems that can actually produce. It is roleplay balance, not a historical barrels-per-day estimate.

| Paid focus | One-time base oil addition | Full capital expenditure | Focus time | Nominal total in the illustrated sequence |
|---|---|---|---|---|
| Develop the Fields | Abu Dhabi +8 | $0.75bn |70 days |12 |
| Expand Onshore Output | Abu Dhabi +10 | $2.50bn |70 days |22 |
| Develop Offshore Oil | Abu Dhabi +12, Dubai +3 | $5.00bn |105 days |37 |
| Offshore Phase Two | Abu Dhabi +7, Dubai +3 | $8.00bn |140 days |47 |

All four cost **$16.25bn** and add43 base units. The first investment precedes the ownership/services choice. The main onshore and offshore expansions are compatible and can be funded after either settlement. Their order is optional; the cumulative column illustrates all investments completed in table order. Offshore Phase Two requires the first offshore programme, and nominal47 requires all four investments.

These are actual native `add_resource` rewards, not export multipliers or cash grants. Each focus requires the whole treasury amount and ownership/control of every recipient state. It rechecks those conditions and its unpaid flag immediately before a once-only payment/resource transaction. Native borrowing or agreed multiplayer finance can supply the money; the focus does not create a loan or give free capital. A government change, independence or reload must not repeat a paid grant.

For a new1970 campaign, apply the low-oil start **before** existing GDP calibration freezes its accounting offset. Keep the authored $0.686bn initial GDP snapshot; it does not restore oil units or oil export cash. Future physical investments increase endogenous GDP without rerunning that calibration. Placing the reduction after calibration would create an unrelated artificial GDP-floor/debt trap, so that approach is excluded.

World prices, actual exported quantities, extraction research, infrastructure and native depletion still apply. The nominal47 is the sum of paid base-capacity grants before subsequent depletion, not a permanent output cap or a periodic refill. Source-backed cost and cash-flow limits are in `OIL_REVISION_AUDIT.md`; this is still untested proposed balance. No loaded resource/history files have been edited.

## Structure and geography

The upper tier covers British protection at the left, federation, ruling houses, constitutional government and Arab nationalism. The middle tier contains the social republic, Sunni social reform, oil policy and the trading coast. The lower tier contains public services, defence and Gulf diplomacy. This reserves inactive political space and keeps the geometry stable after a government change. The nine-focus British programme uses x−6…−1/y0…4; every previous focus keeps its coordinates.

## British protection, the existing withdrawal schedule and paired spirits

**The historical withdrawal is already part of the 1 January 1970 starting situation.** Both UK and UAE start with **British Withdrawal Announced**, recording the British policy announced on 16 January 1968: withdrawal from the Gulf by the end of 1971. This is an existing policy alongside continuing special treaty responsibilities, not a new bilateral independence treaty awaiting an Emirati petition. [Wilson's announcement](https://api.parliament.uk/historic-hansard/commons/1968/jan/16/public-expenditure)

The starting tooltip separates **Announced deadline: by the end of 1971** from **Historical scenario execution: 1 December 1971**. The precise day uses the later historical termination as an explicit scenario convention; it was not already a jointly signed date in January 1970. Special relations ended on 1 December; the sovereign federation was established on 2 December. [Completed transition](https://api.parliament.uk/historic-hansard/commons/1971/dec/06/the-gulf)

- **Prepare the Handover** replaces the former Petition for Freedom title and purpose, preserving its ID and position. It opens talks about earlier release and practical handover terms. Neither completing it nor obtaining a new UK approval is required for the normal historical release.
- If the player takes no British focus before automatic release, only the non-exclusive starting liaison is bypassed without a fee or reward. Prepare the Handover remains available as domestic preparation after independence and sends no release offer then. Neither exclusive choice is automatically completed; the handover/friendship follow-up remains reachable.
- **Renew the Protection** seeks a different policy: continued British protection. Only an agreement accepted by both countries before the current deadline replaces the starting schedule. Sending, ignoring or refusing that proposal never pauses the historical withdrawal.
- **Shared Administration**, the training/commercial choice and **An Enduring Compact** require an actually accepted renewed compact and British subject status. **An Orderly Handover** and **A Friendship Treaty** require actual independence; friendship cooperation needs its own agreement.

The protected training and commercial programmes retain their proposed numeric trade-offs. Training Teams gives −15% training time, −5% equipment costs, +8% personnel costs and 15 one-time Army experience. Commercial Partnership gives +12% office productivity, +1 inward investment capacity and +5% bureaucracy spending. Native subject rules already transfer 50% of civilian and military factory capacity and restrict war declarations; no duplicate transfer penalty is added.

| Paired spirit state | What both countries see | Sovereignty |
|---|---|---|
| Starting withdrawal announced | Existing 1968 policy, end-1971 horizon, labelled historical execution date and each side's continuing duties | British subject until normal release; no new petition or approval |
| Later agreed handover terms | Accepted terms and the same date; handover-only cooperation preserves the baseline date | Subject until the current schedule executes |
| Renewed protection | Accepted alternative compact, review date and **No fixed independence date** | British subject; a review is not automatic release |
| Withdrawal completed | Actual completion date, then a 30-day notice | Independent; no second release or continuing protection benefit |
| Independent friendship | Agreed consultation/cooperation and already-independent status | No subject relation, automatic faction, base rights or unconditional guarantee |

The new-1970 scenario bootstrap creates the starting schedule and both spirits once. Save/load and government changes resynchronise that current record, never recreate the baseline over a valid renewal. A daily/load observer and scheduled callback execute the current due schedule once through the verified UK-scoped `end_puppet = UAE`. The consumer accepts the initial-policy origin as well as a mutually accepted replacement; there is no focus or fresh-approval gate. Another overlord or annexation invalidates stale British delivery. A late renewal popup must recheck the nonce and due date and cannot retroactively postpone a release already due.

Relative amendments retain the verified native `global.date` / `GetDateStringNoHourLong` convention; a 360-day term uses +8.64. Rejection, timeout and handover-only talks preserve the existing schedule. Date/cost changes require mutual consent. Retried talks have a 180-day cooldown but never control the default release. After a valid retained-protection settlement, later independence is a newly negotiated change to that compact.

The main **British Withdrawal** focus still requires actual `is_subject = no` plus founder consent. An announcement or future date is not independence. This focus forms the already-independent federation; it does not release the subject itself. The Council/interim administration remains until actual formation or a real government change.

The optional UK development grant remains $0.25bn: guarded UK debit and UAE credit only after acceptance, sufficient treasury, valid current compact and unpaid flag. The low-oil start, all four expensive extraction phases and 97 unrelated focuses remain unchanged.

In the inspector, **Treaty status → 1970 · Withdrawal announced** and **UK–UAE Treaty Spirits** show the starting paired records. The revised starting UAE spirit reuses `COLDWAR_UAE_treaty_dependence` and its −10% political power contribution rather than adding another subject penalty. The same contribution must persist in its accepted-compact replacement until actual release. The historical correction and mechanics review are in `STARTING_WITHDRAWAL_CORRECTION_HISTORY.md` and `STARTING_WITHDRAWAL_CORRECTION_MECHANICS.md`; these supersede any earlier request-first wording. All helpers and native event delivery remain concept work pending implementation approval.

The native grid is **96 × 130**, with actual MD/HOI4 icons, titlebars and the inherited Ubuntu Bold 16 atlas. Simple political choices use two-grid spacing; wider delivery branches reserve their full footprint. Relative anchors are the intended emitted-code convention. All preview coordinates are absolute resolutions of those intended anchors. There are no loaded national-focus declarations yet.

The seven-emirate route and a negotiated nine-state charter are alternatives. Bahrain and Qatar retain individual acceptance, refusal and associated-partner options. Nothing silently annexes another human player. The smaller emirates use a consent ledger within the existing two-state map; the concept does not claim seven map states already exist.

## Political choices

| Governing programme | Native party condition | Two internal dilemmas |
|---|---|---|
| Ruling-house bargain | Monarchist, slot 23 | Zayed-style development solidarity versus Rashid-style commercial autonomy; negotiated union versus stronger executive authority |
| Constitutional cabinet | Western liberal slot 2 or conservative slot 1 | Constitutional crown versus citizen republic; citizen employment/residency preference versus a broader resident compact |
| Arab nationalist republic | Emerging autocracy slot 7 or nationalist junta slot 22 | Civilian Arabism versus officer government, each requiring its own actual party; regional solidarity versus independent national policy |
| Social republic | Communist slot 4 or non-aligned social slot 18 | Public ownership versus social-market administration, each requiring its own party; universal resident services versus citizen entitlements |
| Sunni social reform | Muslim Brotherhood slot 12, with association organised | Charitable provision versus federal welfare; consultative civic reform versus clerical supervision |

Constitutional and republican governments are explicitly alternative history. The social republic is particularly speculative; it does not assert a real mass UAE communist party. Islah’s association history begins in 1974, and an alternate governing party requires a separately organised political transition. No generic Shia or Salafist state path is inserted merely because the MD slots exist.

The first focus in each political area already makes a substantive policy change. It becomes available when the relevant party governs. There is no redundant focus to unlock the party already in office. Political organisation and government changes use the existing outlook/subparty system, with proposed historical roster bridges identified as new integration work.

Government-bound contributions deactivate when the qualifying party leaves and return with its earned programme when it returns. Completed physical projects, starting-spirit reforms and one-time productivity grants remain national. Refreshing, succession and save/load must never repeat treasury payments, construction, resources or experience grants. Shared political clusters retain exact-party checks on their internally party-specific alternatives.

## Economic and military impact

The design uses substantial sector, institutional and force changes rather than long chains of small political-power gifts. Examples:

| Choice | Gain | Cost or limitation |
|---|---|---|
| Zayed’s Solidarity | Infrastructure construction +15%; additional six-point relief of the national construction penalty | Bureaucracy spending +6%; setup $0.02bn |
| Rashid’s Enterprise | Office productivity +12% | Political power gain −5%; setup $0.02bn |
| Buy a Larger Share | Accepted oil contract: export revenue multiplier +15% | Bureaucracy +6% while contract operates; $0.04bn setup plus negotiated participation price; partner consent |
| Service Guarantees | Productivity growth multiplier +8%; Abu Dhabi +15 productivity points | Export revenue multiplier −4%; setup $0.02bn |
| Save the Windfall | Annual interest rate −0.50 percentage points; native investment return +0.50 percentage points; reserve decisions | Construction −4%; setup $0.04bn; only separately funded native assets earn native returns, subject to the cap; the cash reserve ledger earns zero |
| Spend on Development | Construction +12%; development project decisions | Energy use +8%; setup $0.04bn; fewer reserves |
| A Free Zone | +1 concurrent inward investment; office productivity +10% | Bureaucracy +5%; setup $0.03bn |
| Back Local Merchants | Office productivity +15% | Productivity growth multiplier −3%; setup $0.03bn |
| A Union Command | Army organisation +10%; strongest remedy removes fragmented command penalty | Military personnel spending +10%; agreed federation required |
| Coordinated Commands | Training time −10%; command penalty reduced to −3% | Bureaucracy +8%; emirate command autonomy remains |

The 1970 authored GDP target is $0.686bn in native MD units. Initial 1% GDP is $0.00686bn; actual new-game values still require an engine check. Ordinary small focus fees fund preparation and institutions; the four oil fees are full field-development capital expenditure. The two possible civilian factories and office project are **queued**, not instant grants: normal native construction output, staffing and energy are still needed. A +1 slot is not a free workforce. No impossible extra level is added to Abu Dhabi’s inherited level-10 port.

The native oil-export multiplier affects export receipts. `imp_oil_price_resistance` affects consumer oil-cost exposure, so it is not used as fake protection against falling export revenue. Native OPEC restraint already supplies its export multiplier penalty. ADIA is modelled as an Abu Dhabi institution, with any federal asset-sharing agreement separate. The Dirham needs a proposed domestic-currency identity bridge; it does not create a reserve-currency issuer or set an arbitrary currency-strength bonus.

## Roleplay decisions and historical crises

The concrete decision catalogue includes founding ruler settlements; separate Bahrain/Qatar charter offers; constitutional organisation; Sharjah’s restoration/coup crisis; the 1976–79 authority dispute and a Dubai-led cabinet bargain; residency and labour measures; scholarships; negotiated oil participation; reserve principal deposits and releases; OPEC policy; downturn responses; port and airline finance; paid training; procurement offers; the Saudi border; distinct island arrangements; GCC participation; and a response to an invasion of Kuwait.

An agreement offer freezes its GDP-based amount, displays the concrete numeric costs and effects in native event options, and requires the recipient’s choice. Rejection grants nothing and charges no contractual payment. Paid repeated courses have stated cooldowns and replace identical timed contributions. The reserve principal ledger cannot generate income merely by existing, and withdrawal deducts the same principal it returns.

Island diplomacy unlocks early from bilateral contacts; it does not require a GCC charter. Abu Musa’s arrangement is distinguished from the Tunbs dispute. Kuwaiti invasion responses unlock from early Gulf Diplomacy when the world-state condition exists; the later Gulf Crisis focus is not the sole way to respond. No historical war is forced. F-16 Block 60 deliveries belong to 2005 and are excluded.

## Evidence and limits

Three independent agents researched history, measured Generic/Russia layout and traced mechanics. Historical evidence, native effect providers, exact party slots and numerical MD comparisons are recorded in `HISTORY_RESEARCH.md`, `MD_REFERENCE_LAYOUT.md` and `MECHANICS_AUDIT.md`. The final review files record corrections and closure against the current manifest.

Structural checks cover dependencies, reciprocal exclusions, title metrics, row collisions, six combinations/orders of national remedies, oil totals/invoices/flags, actual independence gates and complete paired treaty records. The British revision preserves 97 prior focuses exactly; its one authorised existing-focus change is the sovereign formation gate/title/reward. Browser checks inspect all 107 focuses, eight government cases, twelve branches at four viewport widths, six treaty-status cases, paired dates/cards, images, pan, zoom and locked-node inspection. The oil and British revisions have dedicated mechanics/layout reviews. Connector routing, shader shine and actual in-game behavior remain untested until implementation is approved.

The modifier keys and leaf APIs have source support. The historical programme values, contracts, dynamic modifiers, currency bridge, spirit remedies and `COLDWAR_UAE_*` helpers are **proposed integration**, not claims of existing executable country content. The approval decision is about this reviewable design; implementation and HOI4 testing follow only after approval.

Historical anchors: [National Library and Archives — federation](https://www.nla.ae/en/our-history/historical-periods/the-formation-of-the-federation/), [UAE Constitution](https://uaecabinet.ae/en/the-constitution), [US contemporary islands memorandum](https://history.state.gov/historicaldocuments/frus1969-76v24/d110). The research report supplies the full source list and factual qualifications.
