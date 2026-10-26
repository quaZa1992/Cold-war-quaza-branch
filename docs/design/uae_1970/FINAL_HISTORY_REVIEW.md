# Independent final history and country-design review

Final catalogue rechecked: `build_concept.py` and `COLDWAR_UAE_1970_CONCEPT.json`, Concept 1, **97 focuses and 37 decisions**. Scope: country history, political plausibility, historical order, starting conditions and narrative. No loaded game files changed. Numerical balance and executable mechanics remain the mechanics reviewer's responsibility.

**Final verdict: suitable for the user's concept approval from a historical and country-design perspective. All seven major findings from the first review have been addressed in the current catalogue.** The starting situation and explicit alternative-history boundaries remain credible. This is approval-stage design, not a certification of implementation or engine behaviour.

| Original finding | Verified closure in the final catalogue |
|---|---|
| Veto versus ministries was a false binary | `Emirate Guarantees` and `A Stronger Mandate` both recognise common ministries; the difference is the extent of delegated federal authority. The historical constitutional combination is available. |
| State equity versus foreign partners was a false binary | `Buy a Larger Share` explicitly retains foreign technical partners; `Service Guarantees` explicitly permits state participation. The choice concerns ownership risk and contractual priority. |
| 1971 islands response depended on GCC | Both islands focuses now descend from `Open the Channels`, independently of GCC formation. The Kuwait invasion response decision unlocks from early `Gulf Diplomacy`. |
| 1973 currency was missing | `A Common Currency` now introduces the Currency Board and dirham, correctly identifying the Bahraini dinar and Qatar–Dubai riyal as predecessors. It does not claim a 1973 full central bank. |
| Sharjah crisis was only a disclaimer | `The Sharjah Crisis` is a defined restoration/coup response decision with January 1972 context, surrender/intervention choices and an explicit local ruler settlement. It does not install a fictional Baath government. |
| 1979 crisis was reduced to transfers | `The Federal Cabinet Bargain` now covers a Dubai-nominee cabinet, historically Rashid in 1979, emirate authority and separate presidential/prime-ministerial offices. Mediation transfers remain a separate instrument. |
| National voting and municipal advice were falsely opposed | `Citizen Preference` versus `A Resident Compact` now concerns jobs, residency and administrative obligations. Both permit citizen elections. The labour penalty has an explicit migrant-access restriction. |

The terminal programme's unrelated military-equipment cost has also been replaced with a bureaucracy/administration cost. No further major historical change is required for this concept review. Minor wording and context details below can be handled during final localisation and implementation; they do not reopen the settled design.

## Original review record

The following sections retain the first review's reasoning and evidence. Their seven principal findings are **closed by the final catalogue**, as recorded above; they are not a list of outstanding blockers.

### Original changes requested

### 1. The Dual Veto and Common Ministries are not historical opposites

`COLDWAR_UAE_dual_veto` and `COLDWAR_UAE_federal_ministries` are mutually exclusive. The historical federation had both federal ministries and the Abu Dhabi/Dubai veto. Their current titles make a real constitutional combination unavailable and imply that federal administration requires abandoning the historical bargain.

Keep the meaningful choice as **greater emirate guarantees versus a stronger delegated federal mandate**. Both can establish common ministries; the historical veto should remain unless a clearly labelled alternative constitutional settlement changes it. The common institutions must not be presented as the unreal historical option. [UAE Constitution, Articles 45–49](https://uaecabinet.ae/en/the-constitution)

### 2. Public oil participation did not require removing technical partners

`COLDWAR_UAE_state_participation` and `COLDWAR_UAE_partner_expertise` form a second misleading institutional binary. Abu Dhabi purchased participation while foreign oil companies remained involved. A real trade-off is the **size and cost of the public equity purchase versus contractual guarantees and longer-term technical dependence**, not public participation versus the continued existence of partners.

Also review the downstream split: associated-gas development did not depend on rejecting foreign expertise, and better terminals did not depend on rejecting public participation. These can be alternative investment priorities while keeping their historical compatibility explicit. [World Bank UAE mission brief, January–March 1973, initial 25% participation](https://thedocs.worldbank.org/en/doc/984811391204517823-0560011973/original/WorldBankGroupArchivesFolder1772673.pdf)

### 3. Early islands diplomacy must not require the later GCC programme

Both `COLDWAR_UAE_islands_arbitration` and `COLDWAR_UAE_islands_claim` require `COLDWAR_UAE_gulf_cooperation`. The islands crisis occurred in November 1971; the GCC Charter followed in May 1981. On a historical progression, the current dependency either delays the island response by a decade or requires an accelerated alternative GCC first.

Unlock the islands response through early Gulf diplomacy/contact institutions, independently of GCC formation. The GCC can later support an existing policy. Likewise, an Iraqi invasion of Kuwait should activate a national response even if the player never completed the islands-policy choice. [US State Department, 1 December 1971](https://history.state.gov/historicaldocuments/frus1969-76v24/d110), [GCC founding Charter](https://www.gcc-sg.org/en/AboutUs/Pages/default.aspx)

### 4. The 1973 Currency Board and dirham are absent

No focus or decision currently represents the federation's new currency. This is a conspicuous omission from an otherwise detailed institutional tree and from the user's supplied timeline. A single shared institutional focus or decision is sufficient; it can replace a more generic accounts/civil-administration step.

The historical sequence must say: **Currency Board and dirham in May 1973; full central bank in 1980**. The dirham replaced the Bahraini dinar in Abu Dhabi and the Qatar–Dubai riyal elsewhere. It did not directly replace an everywhere-current Gulf rupee. [CBUAE institutional history](https://centralbank.ae/en/about/about-cbuae/our-history/), [IMF monetary history](https://www.elibrary.imf.org/view/journals/024/1975/002/article-A009-en.xml)

### 5. The 1972 Sharjah coup is mentioned but not represented

The event appears only in a reward disclaimer under `COLDWAR_UAE_arab_awakening`. There is no actual historical crisis, response decision or succession outcome in the concept. Add a compact crisis contract outside the focus count, or explicitly reserve it as an identified implementation requirement.

The historical default is the **failed restoration attempt by former ruler Saqr bin Sultan**, the death of Khalid, federal intervention, and Sultan bin Mohammed's accession. Do not automatically create an Arab-nationalist republic or assert a historical Baath government. Date the crisis to January 1972; avoid unsupported exact force sizes. [Contemporary State Department assessment](https://history.state.gov/historicaldocuments/frus1969-76v24/d36)

### 6. The 1979 constitutional crisis needs an actual constitutional settlement

`COLDWAR_UAE_rulers_compact` and `COLDWAR_UAE_decision_mediate` provide a useful place for the crisis, but the only defined outcome is a GDP transfer removing a general stability penalty. That is too thin for the actual dispute over federal power, military integration and a permanent constitution.

Retain the transfer as one bargaining instrument. Explicitly include the cabinet settlement and distribution of authority: the historical 1979 compromise placed **Rashid of Dubai in the premiership**, while Zayed remained president. Do not settle the entire crisis merely by paying money. This can remain one decision chain rather than several extra focuses. [Study citing official UAE gazettes, chapter four](https://wrap.warwick.ac.uk/36095/1/WRAP_THESIS_Jakka_1993.pdf), [Heard-Bey, constitutional-crisis discussion](https://www.cooperative-individualism.org/heard-bey-frauke_the-united-arab-emirates-2005-summer.pdf)

### 7. The citizenship branch uses an unsupported conflict and penalty

`COLDWAR_UAE_citizen_ballot` is exclusive with `COLDWAR_UAE_municipal_compact`. A citizen national electorate can coexist with advisory municipal participation by noncitizen residents. The current opposition is between different levels of representation, not inherently conflicting policies.

Either express a clear first-priority choice or use genuinely competing residency/participation settlements. The ballot's **−3% workforce** needs an actual labour/residency restriction to justify it; a citizen franchise alone does not reduce the supply of workers. Citizen-first benefits versus residence-based entitlements in the social branch is a clearer conflict because both compete for the same public-service budget.

## Smaller corrections and precision

- Rename `The Seventh Emirate` to a Ras Al Khaimah-specific title or adapt it to the settlement. Its present title is awkward if Bahrain/Qatar have joined or Ras Al Khaimah was already included in the initial agreement. The historical six-plus-one outcome is accurate; a nine-state alternative needs its own member count.
- `The Security Handover` describes British protection as already ended but is available in January 1970. Use anticipatory wording or require the relevant handover context. Planning before withdrawal is historical; claiming that it has already happened is not.
- Federal offices and constitutional mediation in the monarchy branch need an established federation or explicit preparatory wording. This is a context check, not a blanket date lock.
- The **+3% military equipment cost** in `Improve the Terminals` has no clear relationship to commercial loading/maintenance. Use a relevant operating/administrative cost, unless a separate coastal-security purchase is actually part of the programme.
- `Save the Windfall` correctly distinguishes Abu Dhabi assets from federal assets. Retain the earlier Financial Investments Board of 1967 as background; ADIA should not imply that investment management began only in 1976. [ADIA institutional history](https://www.adia.ae/media/azure/adia/media/annual_review_website2009.pdf)
- The consent conditions on Bahrain, Qatar, Iran and Saudi Arabia are appropriate. A diplomatic offer alone should not claim that an accord exists. The islands focus currently grants +7% offices immediately; explain whether that reflects unilateral confidence-building or make it conditional on an accepted commercial accord.
- Keep the proposed figures labelled as game balance. None of the spirit percentages is a historical statistical measurement.

## What already works

The January 1970 framing correctly distinguishes the Trucial States from the later UAE. Nine-state negotiations remain possible without compulsory annexation. Zayed and Rashid are presented as partners with different priorities rather than fabricated real electoral parties. The FNC is correctly consultative, natural resources remain emirate-owned, and stronger presidential authority does not automatically abolish other dynasties.

The alternative-history boundaries are clear: national liberal, republican and socialist governments are explicitly alternatives; Saqr's restoration is not treated as proof of a republican majority. Islah requires organisation and is correctly contextualised from 1974. There is no invented mass Shia or Salafi governing branch.

The starting-spirit themes are credible: fragmented authority, uneven development, skilled-worker shortages, water/power constraints, narrow revenue sources, dependence on the British security framework, and the difference between imported labour and citizen military reserves. Avoid turning these into a portrait of universal destitution: Abu Dhabi already had substantial oil income, Dubai had an active trading economy, and development work existed before independence.

The port, aviation, savings and oil-slump themes are well selected. The distinction between Abu Musa's negotiated arrangement and the Tunbs dispute is preserved. Modern F-16 Block 60 deliveries are correctly excluded. The English descriptions are short and mostly country-specific; the recommended corrections should replace vague steps rather than inflate the number of nodes.

## Turning-point coverage at the first review

This table records the first 96-focus draft. For the final 97-focus / 37-decision catalogue, the islands dependency, currency omission, Sharjah crisis and cabinet-bargain findings are closed by the changes at the top of this review.

| Turning point | Current status | Required resolution |
|---|---|---|
| January 1970 institutions | Present and broadly accurate | Preserve separation between preparation and an established federation. |
| 1971 federation and withdrawal | Present | Keep consent and historical expiry distinct. |
| November 1971 islands | Present but behind GCC | Remove the chronological dependency. |
| January 1972 Sharjah coup | Disclaimer only | Define compact crisis/response/succession content. |
| February 1972 RAK / FNC | Present | Adapt accession title to alternative membership. |
| 1973 currency | Missing | Add/replace one institutional step. |
| 1973 oil politics | Present as export-restraint decision | Retain distinction between Arab embargo policy and OPEC pricing. |
| 1976 military union | Present, labelled as legal milestone | Retain gradual integration and context. |
| 1976–79 federal crises | Mentioned, outcome underdeveloped | Include cabinet and authority bargain. |
| 1981 GCC | Present | Keep it independent of the ability to respond to earlier disputes. |
| 1985 free zone / airline | Present | Earlier achievements remain explicit accelerated alternatives. |
| 1986 oil downturn | Present | Preserve exposure to native oil prices. |
| 1990–91 Kuwait crisis | Conditional continuation | Trigger response from the invasion, not an unrelated islands prerequisite. |

This review does not certify implementation, party-slot correctness, modifiers, affordability or engine behaviour. The final catalogue has addressed its major historical corrections and is ready for user review as a concept.
