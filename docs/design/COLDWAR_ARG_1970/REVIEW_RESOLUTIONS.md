IMPERIA COLD WAR
# Argentina concept: review disposition

Status: awaiting the owner's design approval. No loaded national-focus, idea, event, decision, history, GUI or localisation files were edited for this task. The spatial fixture is a review file under this directory and is not a playable focus tree.

The final proposal has 299 focuses in 22 clusters, including 16 political programmes, 67 mutual-exclusion pairs, 20 recipient-approved bilateral offers, 16 events, six starting national spirits and seven decision contracts. All new proposed player text is English. The country namespace is `COLDWAR_ARG_`; custom code and generated review output carry the full project marker.

## Owner revision: a native Falklands war goal

`COLDWAR_ARG_rosario_plan`, Plan Operation Rosario, now grants a Take State focus war goal against ENG for state 26 directly on completion. The native form is `create_wargoal = { type = take_state_focus target = ENG generator = { 26 } expire = 730 }`. The 730-day term follows the existing focus-war-goal definition in `common/wargoals/00_invasion.txt:15-29`; the explicit state-generator pattern is used in `common/national_focus/01_EU_USoE_shared.txt:1051-1057`. Britain's ownership/control of the islands and peace with Britain are checked before execution. The focus retains its $2.000 billion cost, position, prerequisites and exclusive choice against Armed Demonstration.

The previous Authorize Operation Rosario war-declaration decision is removed. The player chooses when to declare war through normal diplomacy using the granted war goal. This does not automatically declare war, transfer territory or award victory. `BROWSER_QA.json` explicitly verifies the target, state, type, duration, visible focus effect and absence of an automatic declaration. This revision supersedes earlier review references to the deleted war-declaration decision. It remains an unimplemented approval-stage concept.

## Independent review

- `md_reference_profile.md` measures the installed MD 2.0.4 France, Russia, Generic and Germany sources and the project Soviet architecture. `layout_review.md` independently resolves the spatial fixture and inspects overview and native-scale compositions.
- `history_research.md` records historical sources and separates January 1970, subsequent events and alternate-history programmes. `history_design_review.md` reviews all political families, starting problems, agreements and events.
- `mechanics_reference.md` and `mechanics_design_review.md` trace effects against both the installed donor and the actual Cold War target. The newer donor is not assumed to provide mechanics already integrated in the target.

## Resolved findings

| Finding | Final treatment |
|---|---|
| Donor-only general military-spending modifier | Use the target's `equipment_cost_multiplier_modifier`, labeled Equipment Operating Expenditure. Its reader changes equipment running costs, not all military spending. |
| Mineral export revenue mistaken for grain earnings | The Soviet grain protocol uses a funded weekly bilateral transfer and actual agriculture productivity. Resource-export revenue is not presented as grain income. |
| Already registered Los Gigantes deposit | The first focus funds feasibility and research, without registering the deposit again. Native paid investment remains independently available. Sponsored construction checks zero built/queued mines and remaining native capacity before its funding transaction. |
| Party and leader identity mismatches | Reuse exact native in-power triggers with actual Argentine party labels. Named leader guards record the target's exact spellings and supported aliases. PSD remains an explicit provisional incumbent identity, separate from CGTA. |
| Asset-sale proceeds potentially awarded twice | The privatization event grants a policy mandate and costs money. Only the guarded asset-sale decision awards the single $3.000 billion receipt. |
| Ambiguous inquiry durations | Accountability option modifiers last 730 days. The separately attached Barracks Resistance spirit lasts 365 days and is displayed independently. |
| Later treaties presented as starting facts | Earlier offers are explicit negotiated alternate-history accelerations. Beagle descriptions specifically identify preventive mediation. Madrid restoration requires a recorded real war and subsequent peace. Menem, UCeDe and named leadership transitions retain real identity prerequisites. |
| Historical Soviet contract had a finite term | Record the 1980-1984 historical precedent. The proposed RP offer negotiates a standing successor with no spirit expiry, as requested. |
| Diplomatic buildings assigned to the wrong Uruguay map state | The proposal uses verified state 893, Rio de la Plata, rather than state 300. Every construction level includes one extra shared state slot. |
| Falklands peace path lacked a territorial conclusion | Add a separate Argentine sovereignty-treaty focus. British acceptance transfers state 26 without a core. Argentina pays $6.000 billion including $5.000 billion credited once to Britain; Britain pays $1.000 billion setup. No preview executes this transfer. |
| Crossing diplomatic prerequisites and long titles | Separate regional and overseas diplomatic fans, use a real funded overseas-missions root, shorten native focus names and preserve the final graph in the emitted fixture. |
| Exclusion rails crossed icons | End red exclusion rails at the card boundaries. Camera positioning keeps the selected focus and nearby predecessor visible. |
| Inappropriate art substitutions | Use Argentine service and movement art, a neutral nuclear icon, Catholic art, a neutral election icon and distinct real partner-country icons. The UCR symbol is reserved for its own programme. |

An early review confused party-slot numbers with requested focus counts and reported a duplicate `rural_cabinet` ID. Both findings were independently checked and withdrawn. The current fixture and design each contain 299 unique focus IDs.

## Verification

`MODEL_QA.json` reports unique IDs/positions, valid relative anchors, reciprocal exclusions and satisfiable prerequisite histories. `BROWSER_QA.json` independently parses the emitted Clausewitz graph fixture and compares it with the proposal. It checks all 299 focus inspectors, 16 event views, both sides of all 20 agreements, exact prospective money/modifiers/research/state grants, territorial effects, all 16 government selections and widths 1180, 736 and 360.

Final results: 342 prerequisite links; no missing art, card overlaps, prerequisite lines through cards, exclusion rails through cards, title overflow, browser errors or page-width overflow. All 299 nodes remain visible under every government selection. These are source, model and browser checks, not HOI4 or multiplayer engine tests. The browser typeface, icon composition and connector routing approximate the native view. The full-tree overview is a schematic reduction; its fit-to-width scale is smaller than the game's normal minimum zoom. Chapter views use the actual 96 by 130 GUI grid.

## Implementation dependencies after approval

- Reconcile the current leader pools with Argentina's registry identities and implement lawful succession/elections. The Ongania history expiry differs from his historical June removal date. Approve the distinct PSD incumbent identity and the later PCI/UCeDe reorganization without silently renaming PD Mendoza.
- Implement earned party/leader programme storage and conditional active spirits. Suspend/restore only the current owner's eligible programme; never repeat cash, buildings, research or XP on return. Corporate institutional bonuses require the actual corporate constitutional settlement.
- Implement every Argentine proposal and the recipient's real Accept/Decline decisions. Both active spirits and weekly flows require mutual peace, no embargo and none of the four mirrored Imperia sanction classes, plus an actual active parent where specified. No standing agreement expires. Setup, research, assets and compensation run once.
- Integrate weekly income and expense contributions into the actual MD economy aggregators. Keep every scripted budget literal to at most five fractional digits and preserve borrowing through MD's existing machinery.
- Keep construction, extra slots, ownership/control, mine/building capacity and one-time receipts in one guarded transaction. Inspect the current full native country-event window before composing any event photos.
- The loaded January 1970 reactor baseline is a separate scenario-history issue. This concept adds no free Atucha reactor or premature commercial operation. Correcting the baseline requires a separately scoped change.
- Implement English localisation with BOM; runtime scripts without BOM. Run native load, tooltip, succession, reload, construction and two-player consent/sanction tests after implementation.

## Art and provenance

`PREVIEW_PROVENANCE.json` identifies selected local sprites, original file paths and SHA-256 hashes, preview modifications, credits and unknown permissions. Focus icons are local MD or underlying game art. Individual original artist and separate redistribution permission are unknown unless a source says otherwise. Project markers do not claim third-party ownership. PNG previews are donor-art concept compositions, not live game screenshots. No event picture or invented native event frame is presented as completed.
