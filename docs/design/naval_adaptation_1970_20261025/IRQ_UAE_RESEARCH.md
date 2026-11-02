IMPERIA COLD WAR

# Iraqi and Trucial States coastal-navy adaptation: research and integration review

Read-only source review, 25 October 2026. No gameplay file, approval snapshot, generator or runtime output was changed or executed for this review. The UAE providers contain active work belonging to another chat; all of it remains intact. Line references describe the inspected working files and can move with that work.

## Recommendation

Both countries fit a small coastal variant. Reuse their existing naval/coastal institutions, focus receipts and maritime economy. A copied carrier, SSBN or oceanic fleet branch would misrepresent their January 1970 capabilities. These are design recommendations, not approved numeric rewards or a complete January 1970 ship inventory.

| Country | Appropriate starting identity | Credible emphasis | Recommended attachment |
| --- | --- | --- | --- |
| IRQ | Iraqi Navy with restricted Gulf frontage and limited repair infrastructure | Crew training, repair workshops, approaches to Basrah/Umm Qasr, patrol and mine-countermeasure capability | Extend the existing Coastal Defence and The Coastal Fleet sequence |
| UAE | Sea Wing of the Abu Dhabi Defence Force within the British-protected Trucial States | Seamanship, coastal watches, patrol support, counter-smuggling, island communications and reimbursable technical assistance | A small shared coastal core from the defence staff; later federal coordination follows actual political integration |

The common structure can share technical concepts and verified native research categories, but national names, diplomatic providers, timing and rewards need separate adapters. No ship formation, modern OOB, faction membership, territorial transfer or foreign base should be granted by copying the generic branch.

## Historical evidence and its limits

### Iraq

The near-period American record describes Soviet naval visits to Umm Qasr at the turn of 1970/71. This establishes regional access and diplomatic sensitivity, not an Iraqi submarine force or an exclusive Soviet naval base. See the [6 January 1971 Tehran telegram, FRUS E-4 document 279](https://history.state.gov/historicaldocuments/frus1969-76ve04/d279).

A CIA assessment of 12 May 1972 found insufficient Iraqi maintenance/repair capacity to support Soviet naval ships. Basrah was busy, while Umm Qasr needed expansion despite its deep anchorage. This supports a paid repair and support-infrastructure route. It is evidence from 1972, not a measurement of the exact January 1970 port level. The same assessment discusses the April 1972 treaty, which must not become an automatic 1970 alliance. See [FRUS E-4 document 307](https://history.state.gov/historicaldocuments/frus1969-76ve04/d307).

The April 1973 diplomatic record explicitly distinguishes Soviet assistance and probable access from Soviet control or exclusive use of Iraqi facilities. A Soviet advisory/technical route is credible; an automatically established Soviet base is not. See [FRUS volume XXVII document 212 and its State Department footnote](https://history.state.gov/historicaldocuments/frus1969-76v27/d212).

Basrah's exposed river approach and Umm Qasr's geographic constraints make harbour access a meaningful national concern. They do not justify free Kuwaiti territory, access rights or annexation. Any cooperation affecting another RP country needs its real consent. See the [17 April 1973 INR note, FRUS volume XXVII document 213](https://history.state.gov/historicaldocuments/frus1969-76v27/d213).

No sufficiently firm primary January 1970 hull count was established in this bounded review. Later Iraqi Osa acquisitions, 1980s fleet lists and Soviet visiting warships must not be treated as a 1970 Iraqi starting fleet.

### Abu Dhabi and the Trucial States

The official WAM report on Athol Yates and Cliff Lord's naval history identifies the Sea Wing's foundation in 1967, its renaming as the Abu Dhabi Navy in 1971, and the UAE Navy identity following armed-forces unification in 1976. It records British and Pakistani seconded officers, a first Emirati naval officer commissioned in 1970, early patrol craft and an initial Abu Dhabi island base. These support training and small coastal institutions before federation. They do not establish an exact January 1970 ship OOB. See [WAM, Book on early history of UAE Navy released, 21 February 2019](https://www.wam.ae/en/article/hszr85ss-book-early-history-uae-navy-released).

Six emirates proclaimed the federation on 2 December 1971; Ras Al Khaimah joined on 10 February 1972. Federation and naval unification were separate developments. A focus can represent earlier voluntary coordination, but it should name that policy accurately rather than present a unified federal navy as a January 1970 fact. See the [UAE National Library and Archives: The Formation of the Federation](https://www.nla.ae/en/our-history/historical-periods/the-formation-of-the-federation/).

## Confirmed current IRQ providers

| Provider and anchor | Inspected content |
| --- | --- |
| `common/national_focus/COLDWAR_IRQ_1970_focus.txt:16366` | `COLDWAR_IRQ_defence_coastal`: cost 7, normally 49 days; relative to `COLDWAR_IRQ_defence_professional`, local x=3/y=6; requires implemented logistics. Costs 5% of GDP, using the frozen invoice once quoted; grants one dockyard in state 171. |
| `common/national_focus/COLDWAR_IRQ_1970_focus.txt:16489` | `COLDWAR_IRQ_defence_ship_maintenance`: cost 5, normally 35 days; same anchor x=3/y=7; requires implemented coastal defence. Costs 2% GDP; grants +10% dockyard output and 20 navy experience. No ships. |
| `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt:15684` | `COLDWAR_IRQ_apply_defence_coastal` owns quotation, treasury guard, capacity/ownership/control checks and one-time component credit. Actual dockyard construction is at line 15741. |
| `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt:15871` | `COLDWAR_IRQ_apply_defence_ship_maintenance` preserves the coastal receipt and once-only XP transaction. |
| `tools/iraq_1970/reward_overhaul_economy.json:1566` and `:1609` | Canonical structured economic content for the two nodes. Change these definitions or a narrowly coordinated overlay, not only emitted rewards. |
| `tools/iraq_1970/audit_design.py:189` and `:210` | `load_design()` assembles the immutable baseline and reward overhaul; decision streamlining follows at line 214. |
| `tools/iraq_1970/reward_overhaul.py:95` and `:142` | `apply()` reads the structured revisions. The building-component emitter currently emits construction without an additional slot. |
| `tools/iraq_1970/compile.py:13`, `:20`, `:281` | Loads the assembled design and generates reward packages/expansions. This is a broad country compiler; it was not run. |
| `history/countries/IRQ - Iraq.txt:62` | The 1970 branch deliberately loads `mdcw_1970_empty_naval`. Preserve the existing deferred force-formation policy. |
| `history/states/171-Basrah.txt:25` | Umm Qasr province 9045 has naval base level 2. The relevant Iraqi coastal state is 171. |

Confirmed integration defect to avoid copying: the dockyard preview at tree line 16399 and the guarded actual grant at rewards line 15741 lack the required extra shared building slot. This review records the defect without modifying it. A later fix must preserve the existing credits and receipts and must not rebuy an already delivered dockyard.

The existing IDs, implemented receipts, quotation invoices, credit migration and dynamic defence programme should survive expansion. The minimal integration is to continue these two nodes rather than grant another baseline dockyard under a new generic root.

## Confirmed current UAE providers

| Provider and anchor | Inspected content |
| --- | --- |
| `common/national_focus/COLDWAR_UAE_1970_focus.txt:5766` | `COLDWAR_UAE_security_handover` is the defence branch anchor. |
| `common/national_focus/COLDWAR_UAE_1970_focus.txt:6135` | `COLDWAR_UAE_defence_staff` provides a suitable common institutional attachment. |
| `common/national_focus/COLDWAR_UAE_1970_focus.txt:6168` | `COLDWAR_UAE_air_coastal_shield`, x=-2/y=5 relative to security handover. Cost 10, 70 days; mutually exclusive with land deterrence. Costs 0.02 MD money units, gives +5% army organisation, +10% equipment spending, 10 air and 10 navy experience and calls the existing procurement offer. |
| `common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt:965` | Air-coastal activation requires the campaign, completed defence staff, no land-deterrence receipt and an available procurement partner. It does not currently require federation. |
| `common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt:2246` | The once-only programme receipt and actual procurement routing. |
| `common/scripted_effects/COLDWAR_UAE_1970_diplomacy.txt:2147` | Existing British procurement preview: UAE pays 0.25, ENG receives it and sends 1,000 `infantry_weapons_1`. It is not a ship purchase. |
| `common/national_focus/COLDWAR_UAE_1970_focus.txt:4279` and `:4803` | Fishing Harbours (`port_planning`) and industrial port are existing civil-development content. Do not overwrite the maritime-livelihoods economy. |
| `common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt:1572` | Harbour work checks actual ownership/control of state 179, control of Dubai province 3725 and province naval-base capacity before queued construction. |
| `common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt:338` | `COLDWAR_UAE_form_federation` requires actual independence, both institutional focus receipts and founders' consent. It sets the real federation flags. Reuse this state rather than a calendar-only check. |
| `tools/uae_1970/revision.py:19` | `current_design()` layers changes over immutable `approved_design.json`, then calls development, streamlining, focus-only and specialist overlays. Its final loop explicitly makes every UAE focus 70 days. Preserve this user choice. |
| `tools/uae_1970/development.py:21` | Owns maritime-livelihoods, fishing and harbour development overlays. |
| `tools/uae_1970/focus_delivery.py:15` and `tools/uae_1970/focus_only.py:23` | Existing focus-to-offer routing; air-coastal procurement and harbour project already have owners. |
| `tools/uae_1970/compile.py:23`, `:126`, `:374` | Assembles the current design, explicitly targets Dubai harbour capacity, and builds broad country outputs. Do not import/run the compiler as a harmless data reader. |
| `history/countries/UAE - United Arab Emirates.txt:19` | 1970 deliberately uses `mdcw_1970_empty_naval`. The modern OOB at line 204 belongs to a later block. |
| `history/states/180-Abu Dhabi.txt:26` | Inherited Abu Dhabi province 3689 already has naval base level 10. This is a current provider/capacity fact, not historical proof of a huge 1970 naval installation. |

Confirmed slot gap: the existing Dubai harbour construction at focus-effects line 1580 has no adjacent extra shared slot. The corresponding canonical preview in `tools/uae_1970/diplomacy.py:633` also emits construction without a slot. Record and coordinate a narrow fix with the active UAE owner instead of regenerating their country files independently.

## Suitable expansion choices

These concepts need source-resolved native modifiers, costs and full numeric previews before implementation. They are not approved effect values.

For Iraq, retain the paid dockyard and repair sequence, then offer a choice between imported tactical expertise and domestic repair depth. Both can improve a small fleet: one favours training/limited naval research and carries continuing foreign-service expense; the other favours repair readiness and modest local production at a larger initial facility cost. Patrol/approach security and mine-countermeasure training can be common continuations. Do not invent a free submarine flotilla to make one side competitive.

For the Trucial States, a pre-union coastal core can cover the Abu Dhabi Sea Wing, training, radio watches and patrol logistics. A later choice can favour externally supported professional training or a shared emirate support organisation, with real spending and institutional trade-offs. Federal coordination must require actual federation/integration; naming full unification before 1976 should clearly represent an alternative policy. A basic coastal service should remain reachable alongside land deterrence, unless excluding it is an explicitly chosen strategic trade-off.

A British, Pakistani or Soviet technical partnership must reuse or extend real recipient-approved routing. Existing partner procurement must not be silently reclassified as a naval transfer. Full prospective effects must remain visible before agreement, with setup and weekly expenses, signed modifiers, facilities and slots for both countries.

## Later implementation and verification boundaries

1. Coordinate UAE ownership first. Add a pure country-specific overlay in its canonical assembly; preserve immutable approval, specialists revision, 70-day rule, maritime economy, focus delivery and political integration. Do not run a broad country generator over concurrent unreviewed work.
2. Reuse current roots and receipts. All new assets/costs need the same one-time execution guard. Existing completed nodes must not duplicate money, XP, dockyards or port construction during migration.
3. A new facility must grant one additional state shared slot per building level before construction, inside the guarded transaction. Check ownership, control and the native building cap separately, including province-level naval bases.
4. Preserve empty 1970 OOBs and existing force-formation policy. No `create_unit`, `load_oob` or modern `set_naval_oob` reward is justified by this research.
5. Resolve actual technologies and modifier units in the installed MD providers before numbers are proposed. Hull production, repair, navy experience and naval research are different rewards; a dockyard-output modifier is not a free working fleet.
6. Render against the current full branch, not an isolated generic diagram. Confirm names, focus widths, connectors, all prospective effects and visible prerequisites independently. This read-only report does not claim a native hover test or a layout render.

## Provenance

Historical text above is a short original paraphrase of the linked official sources. FRUS publishes identified US government diplomatic/intelligence documents; WAM credits Athol Yates and Cliff Lord's book and Collaborative Publications, whose text/images are not reproduced here. UAE National Library and Archives is the cited institutional history provider. Separate redistribution permissions for WAM/book material were not established. No image, texture, font, ship model or other third-party asset was copied. Existing runtime/generator authorship and licences remain as recorded in their providers and `IMPERIA_COLD_WAR_NOTICE.md`; this project marker does not assert ownership of them.
