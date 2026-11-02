IMPERIA COLD WAR

# France: African networks and foreign-policy contracts

Implemented on 30 October 2026 following the user's instruction to research, visualize and implement a substantial French foreign-policy tree, followed by a correction to make its placement condensed and aesthetic. The installed total is 213 focuses and 67 recipient-approved agreements, including 37 additional focuses, 32 additional agreements and 16 new exclusive pairs.

## Political and economic choices

Four compact chapters extend the existing diplomacy branch:

- **African Economic Networks:** Senegalese and Cameroonian financial services versus stronger locally governed institutions; Gabonese petroleum services versus local processing; French uranium investment rights versus a Nigerien processing charter.
- **African Security and Development:** Ivorian transit versus commercial port investment; Libreville stationing versus Gabonese officer schools; a Chadian airlift mission versus national military cadres; Sahel field services versus rural development.
- **Arab Contracts and the Mediterranean:** Libyan versus Egyptian aviation-support priorities; Iraqi energy services versus industrial localisation; Saudi naval support versus civilian engineering; a Lebanese field mission versus civilian recovery works.
- **Global Technical Partnerships:** Indian aviation versus power engineering; Vietnamese engineering versus medical services; Mauritian agricultural versus marine services; Djiboutian defence access versus a civilian compact after sovereignty.

The content separates actual institutions and documented precedents from counterfactual selectable packages. `HISTORY_AFRICA.md` and `HISTORY_GLOBAL.md` link the research. Exact GDP shares and modifier values are proposed game balance, not historical contract values. Future-dated precedents inform possible alternative policies without giving future aircraft or technologies in January 1970.

## Compact native placement

The rejected wide comb is superseded. The new shared focus is at (94,9), attached to An Independent Voice. Economic Africa and Arab contracts occupy compact upper blocks centred at (68,14) and (88,14); African security and global partnerships occupy the lower blocks at (68,19) and (88,19). Each chapter has two rows of four offer cards, with two clear exclusive pairs in each row. All 176 earlier focus coordinates and prerequisite groups remain unchanged.

`LAYOUT_PLAN.json` is the design's coordinate source, addressed by stable group IDs. `build_design.py` emits the full design and additions. The default preview opens a readable chapter; a separate Foreign Policy Area view fits the new branches, while the complete France tree remains inspectable. Existing native icons, titlebars and shine providers are reused.

## Real benefits, costs and consent

New reward families include actual military access, uranium investment rights, factories, offices, agricultural districts, dockyards, airfields, infrastructure, finite research and doctrine bonuses, experience and paid commercial services. The complete catalogue includes 82 new building levels with 82 prior slot grants. That figure includes both countries and incompatible alternatives; it is not a single French campaign's reward total.

Every setup cost uses the paying country's own current GDP. Operating costs use annual GDP shares divided by 52. Every agreement has a real recipient acceptance/refusal decision, and both countries' complete prospective costs, named spirit modifiers, assets and rights remain visible before acceptance.

Service fees and aid are matched transfers: one nominal payer expense and one equal recipient income. A shared France-scoped seven-day quote is calculated from the named payer's GDP and read by both ledgers, preventing separate country refreshes from quoting different sums. Repeated budget recalculation does not charge or credit treasury directly. Existing native Additional Income and Additional Expenses breakdowns show the actual active programme totals.

Signed agreements have no fixed expiry. Both countries must exist, remain at peace with each other and impose neither native embargo nor any of the four mirrored Imperia sanction classes. Suspension removes both programme spirits and their cash streams; restoration repeats neither setup payments nor finite rewards. Access and resource rights have separate ownership receipts, so external pre-existing permissions are preserved.

The Niger concession grants native uranium rights in the surveyed state 329 and funded infrastructure. It grants no uranium mine, raw output, fixed shipment or guaranteed reactor fuel. Paid mine development remains in the existing Imperia resource-investment system. Since native rights revocation operates by state, the concession excludes an existing French resource right there. That exclusion is a proposal/acceptance preflight, not a standing activation condition that would disable its own granted right.

The Djiboutian deals require an independent Djibouti owning and fully controlling state 230. The January 1970 state belongs to France; existing sovereignty/release mechanics must establish the partner first. These focuses do not silently create a country or award recipient assets in French territory.

## Canonical implementation

`tools/france_1970_runtime/approved_foreign_policy.json` is an exact frozen copy of the researched compact design. SHA-256: `7bd27bfa457cda2c8443a4252150ed806396a5cc7adb4353a3e5ddaad0f3785f`. `FOREIGN_POLICY_APPROVAL.json` records both the implementation instruction and subsequent layout correction. Prior approval snapshots remain unchanged.

The canonical compiler applies `foreign_policy_revision.py` after the prior 176-focus overlays. It merges only the four new groups and 37 new focuses, asserting that every earlier focus, domestic decision and group is preserved. `diplomacy.py` supplies guarded transactions, finite rewards, paired lifecycle, permissions, shared transfer quotes and budget totals. `integration.py` appends one native additional-income hook and the budget display entries, preserving current shared-file content and required encodings. Shared YAML retains UTF-8 BOM; script files remain UTF-8 without BOM.

## Verification and limits

- `DESIGN_CHECKS.json`, `REVIEW.md` and `MECHANICS.md`: historical fit, native effect support, actual 1970 state ownership and physical caps. Egypt's airfield project uses Alexandria, whose initial level leaves real capacity. Djibouti is an explicitly guarded later-sovereignty case.
- `tools/france_1970_runtime/VALIDATION.json`: current emitted source, graph, frozen approvals, IDs, native references, localisation, encoding and generation contracts.
- `tools/france_1970_runtime/COST_DISPLAY_CHECKS.json`: all 134 country-side cost previews and 201 non-executing call sites; original agreement transactions remain unchanged while their aggregators are intentionally extended.
- `check_foreign_runtime.py`, `RUNTIME_REVIEW.md` and `RUNTIME_REVIEW.json`: independent emitted agreement, payment, permission, suspension and replay checks.
- `PREVIEW_QA.json`: latest browser inspection of native positions, labels, full agreement effects and responsive branch views. `screenshots/` contains browser compositions, not game screenshots.
- Earlier party and starting-spirit migration checks are retained and run against the expanded tree. The obsolete whole-tree count assertions were updated to include this explicitly authorized extension without replacing old approval snapshots.

The compiler's `--check` verifies repeatable output. No new HOI4 engine launch, native hover, real save/reload, calendar observation, performance benchmark or live multiplayer session was run for this extension. Source and browser checks do not establish those behaviors.

See `NOTICE.md` for provenance and third-party permissions.
