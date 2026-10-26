# COLDWAR UAE: low-oil concept layout review

Reviewed 19 October 2026. Scope: the revised oil programme, its neighbouring programme footprints, canonical/embedded preview data, native art and the regenerated `BRANCH_oil.png`. This is a bounded concept review; no loaded game files were changed.

**Verdict: no blocking layout defect.** The revised programme clearly separates the ownership/service settlement from compatible capital investment. It adds one focus without shifting the existing neighbouring branches.

## Current snapshot

- `COLDWAR_UAE_1970_CONCEPT.json` final SHA-256: `fa3cd97ca1a914752a7a8f761b4635d671a935820c352d09dd69118255435c2b`.
- Complete concept: 98 focuses, 37 decisions, 35 native icon types.
- Oil group: 11 focuses, origin (20,9), actual x extent 23–29 and y extent 9–15.
- Canonical JSON and embedded `PREVIEW.html` nodes/groups agree exactly.
- Independently recomputed the 14-field hashes for all 87 non-oil focuses against `OIL_PRESERVATION_BASELINE.json`: all match. Their coordinates, labels, art, prerequisites, exclusions and recorded gameplay surfaces remain preserved.
- Final bounded refresh: subsequent startup metadata/guard hardening preserved focus nodes, geometry and art. Rechecked final file hash and canonical/embedded nodes/groups equality; the inspected oil proof remains representative. The root agent reports clean final browser results for98 inspectors,44 branch/width views and8 governments.

## Reviewed positions and connections

| Focus | Absolute position | Prerequisite interpretation | Native art |
|---|---|---|---|
| Review the Concessions | (25,9) | Entry | `oil_companies` |
| Develop the Fields | (25,10) | Concession review | `resource_extraction` |
| Buy a Larger Share | (23,11) | Develop the Fields; exclusive with Service Guarantees | `oil_companies` |
| Service Guarantees | (27,11) | Develop the Fields; exclusive with Buy a Larger Share | `scientific_exchange` |
| Expand Onshore Output | (23,12) | Buy a Larger Share OR Service Guarantees | `oil_production2` |
| Develop Offshore Oil | (27,12) | Buy a Larger Share OR Service Guarantees | `focus_generic_offshore_oil_rig` |
| An Oil Administration | (25,13) | Onshore expansion OR offshore expansion | `government_beu` |
| Offshore Phase Two | (29,13) | Offshore expansion | `oil_red` |
| Save the Windfall | (23,14) | Oil Administration; exclusive with Spend on Development | `gold_standard` |
| Spend on Development | (27,14) | Oil Administration; exclusive with Save the Windfall | `construction_engineering` |
| Prepare for a Downturn | (25,15) | Save the Windfall OR Spend on Development | `money` |

The onshore and offshore investments have no mutual exclusion. Both contain the same single OR prerequisite group, so either ownership/service settlement can fund both physical developments. The parallel prerequisite links form a common horizontal bridge between rows11 and12; the rendered connection is legible and has no unrelated-card intersection. Phase Two branches right from offshore development without becoming an artificial requirement for ordinary oil administration or reserve policy.

The extension at (29,13) remains four grid units from administration at (25,13) and six from the commerce node at (35,13). The nearest lower diplomacy content begins at y18. No new card enters the next tier or requires a changed section root. The additional right-side space is purposeful and does not create a detached investment island.

## Visual and art checks

Opened the final native-scale oil proof sheet after regeneration. Its eleven cards, section heading and bottom capstone are fully visible. No title/icon overlap, clipped label, card collision, title-through-connector crossing or unexpected exclusive mark was observed. The connector from offshore development to Phase Two is present and fits the clear right-hand space.

Independently tested routed prerequisites against actual native icon alpha bounds plus titlebar rectangles across the complete current concept: zero unrelated visible-card intersections. This uses actual icon dimensions rather than treating the entire 165×128 transparent container as painted art. Engine routing remains an eventual HOI4 check.

All revised oil labels fit the native 147-pixel title field. The longest relevant labels, Review the Concessions and Expand Onshore Output, measure 140 pixels with the native glyph metrics. The offshore platform is generic native art; it has no foreign national flag. Resource machinery, derrick/drop, processing infrastructure, offshore platform and barrels distinguish the investment stages. The Iraqi-flagged `increase_oil_prod` candidate was rejected and is not used.

## Numerical reading of the inspector

The four resource investments are presented as paid increases in operating extraction capacity, not percentage export bonuses or free geological discoveries. Recorded setup capacity is4 base oil; all four paid investments add43, giving47 nominal base oil. The capital costs are $0.75bn, $2.50bn, $5bn and $8bn, totalling $16.25bn, with70/70/105/140-day durations. These values are balance proposals reviewed separately for native effect validity and affordability.

Onshore and offshore remain compatible siblings, so their numeric phase numbering represents an illustrative full investment sequence rather than a mandatory completion order. The always-truthful local grants are +8, +10, +15 and +10 base oil. The47-unit endpoint requires all four investments; completion of Phase Two alone does not imply that the onshore investment was purchased.

`OIL_BROWSER_VALIDATION.json` reports zero errors, four checked stages, starting resources Dubai1/Abu Dhabi3 and the $16.25bn aggregate. This review also independently verified current canonical/embedded preview equality. Full browser interaction certification remains with the root agent's browser QA; no new engine claim is made here.

The earlier whole-tree layout review remains applicable to the preserved non-oil content. This document supersedes its oil-branch snapshot and whole-concept hash/counts for the new low-oil design. The user's approval boundary remains in force: the low-oil start and expansion focuses are still a concept, not loaded game changes.
