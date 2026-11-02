IMPERIA COLD WAR

# France: additional party programmes

Design and interactive comparison requested on 29 October 2026. The user approved implementation on 30 October 2026. The 176-focus expansion is now installed through the canonical runtime compiler. See `IMPLEMENTATION.md` for the current installation and checks.

The original comparison, `BASELINE.json`, `proposal.json`, `ADDITIONS.json` and `RUNTIME_BASELINE.json` remain historical design records. Their design-only status and 156-focus preservation checks describe the pre-approval phase; they are not current runtime assertions. The approved proposal is copied unchanged to `tools/france_1970_runtime/approved_expansion.json`.

## Proposed content

The proposal adds 20 focuses across the eight non-UDR programme groups, including nine new mutually exclusive pairs. The result has 176 focuses, 56 exclusive pairs and the same 35 recipient-approved agreements. It adds no domestic decision: Conversion Boards supplies an alternative prerequisite for the existing Regional Conversion Fund, preserving its exact fee, rewards and one-time receipt.

| Programme | New exclusive choice | Additional outcome |
|---|---|---|
| Independent Republicans | SME Risk Capital or Export Finance | Industrial suppliers and research versus service/export capacity; different tax and education costs |
| Democratic Centre | Family Services or Mutual Districts | Public family-service expansion versus mutual provision; social expenditure or reduced corporate-tax yield |
| Radical Republicans | Civil Service Trials or Open Public Orders | Civic-service administration and infrastructure versus competitive procurement and a civilian factory; military-training or incumbent-industry costs |
| Socialist Party | Basin Conversion or Workplace Charters | Industrial conversion versus workplace services; both can lead to Conversion Boards and the existing regional project |
| French Communist Party | Municipal Health or Supply Contracts | Municipal prevention and health services versus civilian production and agricultural provision; social expenditure or reduced corporate-tax yield |
| Unified Socialist Party | Cooperative Markets or Tenants' Councils | Cooperative market access versus local services; both can lead to Cooperative Land, with a credit office and serviced sites |
| Political Ecology | River Basin Works or Municipal Heat | Water-quality administration versus district-heating investment; construction or training/education costs |
| Shopkeepers and national right | Mutual Purchasing or Rural Shop Grants; Arsenal Renewal or Export Inspection | Separate dated CID and FN choices: local commerce versus rural access, and domestic orders versus export capability |

Every new focus has a setup cost measured as a percentage of the payer's current native GDP. The 32 new building levels each include a shared building slot in the same state before construction. Five further standalone slots represent prepared sites, not completed buildings. Research bonuses are finite. No new positive productivity, production-efficiency, workforce or influence modifier is introduced.

All party branches remain visible. Execution and programme activation use the existing native party checks. The CID's four proposed programme nodes are dated before 5 October 1972, distinct from the later FN identity in the same native party slot. Two existing CID nodes change only lifecycle metadata. Implementing this proposal would require migrating their old programme contribution without replaying finite assets, costs or focus receipts.

## Placement and inspection

The full tree retains its x=4..103 and y=0..13 footprint. New nodes occupy free rows inside existing branch widths. Original focus coordinates, prerequisites and numerical rewards remain unchanged. The new prerequisite routes were adjusted to clear existing mutual-exclusion bars. `LAYOUT_REVIEW.md` records every new coordinate.

The interactive `france-party-expansion.html` comparison in the thread's visualization directory has Current and Proposed views, party navigation, zoom, branch fitting and clickable effects. New focuses are highlighted. All 35 existing agreements retain complete prospective effects for both participants. The existing Fund's changed prerequisite and unchanged transaction are shown separately.

## Evidence and limits

- `HISTORY.md`: historical precedents, dated identities, sources and counterfactual boundaries. The numerical balance is a proposal, not an estimate of historical economic effects.
- `MECHANICS.md`, `REVIEW.md` and `REVIEW.json`: independent native MD effect evidence and route/stacking review.
- `DESIGN_CHECKS.json`: unique IDs, prerequisite DAG, reciprocal exclusions, route reachability, party/GDP/ownership/control/capacity guards, slots, native references and preservation of the loaded runtime.
- `LAYOUT_REVIEW.json` and `PREVIEW_QA.json`: no detected card, prerequisite, exclusion-bar or heading intersections; 42 browser section-fit checks at 320, 736 and 1024 px; no clipped nodes or title-width failures.
- `PREVIEW_BUILD.json`: native artwork references, converted texture dimensions, fragment size and hash. `screenshots/` contains browser compositions, not live game screenshots.

The original records above are design, source and browser checks. Current emitted-source migration and runtime checks are recorded in `IMPLEMENTATION.md`. No live HOI4 save loading, native tooltip, performance or multiplayer validation is claimed. Existing native caps can still be filled by later player construction; execution rechecks them at payment and reward time.

## Reproduction

The retained design tools `build_proposal.py` and `verify_proposal.py` require the pre-approval installed design SHA-256 `00d5e2721934ad527360ce0265f1213e345a1df8b0f1999c22599f23199dbbe9`. Their preservation assertions are intentionally obsolete against the newly approved installation; do not replace their baseline or snapshots to make them pass. Use `tools/france_1970_runtime/compile.py --check`, `validate.py`, the cost-display check and `check_implementation.py` for current verification. The runtime renderer supplies the installed preview. The retained proposal renderer remains a historical comparison.

See `NOTICE.md` for authorship, asset sources and permission limits.
