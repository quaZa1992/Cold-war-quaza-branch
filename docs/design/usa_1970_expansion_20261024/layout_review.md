IMPERIA COLD WAR: Independent USA concept layout and graph review

Reviewed 24 October 2026 and refreshed after the author's geometry corrections. Scope: final `proposal.json`, `build_visual.py`, `review_fragment.html`, the full current and original inventories, and `usa-review-tree-final.png`. This review is separate from the primary author's browser interaction and responsive checks. No runtime files were edited.

Final inspected proposal SHA256: `f524a00e9ab934872d748994b5de1ac89608a791de6cf6b28b0d7c55b142cfa8`. Inspected inline-fragment SHA256: `dd4f289425436f7db708d9157146b4af6b18ae28b27e15058ffd8b67ece91656`. Later regeneration can change the fragment hash without changing the concept graph.

## Structural checks

The merged concept consists of the 229 existing focuses, 13 replacement reward proposals and 52 added focuses: 281 distinct nodes. The proposal has 65 authored nodes, 16 offer nodes and 34 unique mutually exclusive pairs after its rewiring. These counts agree with the manifest and presentation labels.

The full merged graph was checked after applying every declared prerequisite replacement, exclusion removal and added exclusion, rather than checking the 65-node proposal in isolation.

- Missing prerequisite targets: zero.
- Missing exclusion targets: zero.
- Asymmetric exclusions: zero.
- Directed prerequisite cycles: zero.
- Exact duplicate node coordinates: zero.
- Structurally impossible descendants under grouped AND/OR prerequisites and mutual exclusions: zero.
- New nodes with a prerequisite on the same or a later row: zero after correction.
- New nodes with a same-row neighbour less than two x-units away: zero after correction.
- Reworked-focus timing mismatches against native source cost multiplied by seven: zero across all 13 reworks.

For the last check, the reviewer recursively combined the completion sets permitted by each OR group, combined separate prerequisite groups as AND, removed combinations containing an exclusive pair, and discarded redundant supersets. All 281 nodes retained at least one feasible structural route. The largest retained family contained 15 minimal completion sets; no route enumeration was capped. This establishes graph feasibility, not dated-government availability or treaty execution feasibility.

Original MD inventory fidelity was independently established during extraction: all 776 nodes have English names/descriptions, resolved relative anchors, no missing or forward relative anchors and no conditional offset blocks in the inspected donor. The current and original overview data use their source coordinates, while the expansion overlays use the proposal coordinates. The visual labels this as a source-derived approximation rather than a HOI4 screenshot.

## Layout findings and final resolution

### L1: Foreign additions occupied the new defence footprint. Corrected.

The original prepared concept has no exact coordinate duplicates, but these unrelated nodes occupy the same row with only one x-unit separation:

| Pair | Coordinates |
|---|---|
| `USA_X_britain` and `USA_X_nco_corps` | (22, 7) and (21, 7) |
| `USA_X_israel` and `USA_X_logistics_schools` | (22, 10) and (21, 10) |
| `USA_X_saudi` and `USA_X_test_ranges` | (26, 10) and (25, 10) |

The renderer uses 96 pixels per x-unit at normal scale, with labels wrapping at approximately 23 characters. That was insufficient for these neighbouring multiword labels. Their modules are different, so a filtered Atlantic or Middle East screenshot could conceal the collision. The final foreign additions are reserved within x = 10 to 19, while the military additions remain at x = 21 and 25. The Bahrain, Israeli and Saudi offers now sit on row 14 at x = 10, 14 and 18. The closest reviewed same-row new military/foreign pair is Britain at (19, 7) and the NCO programme at (21, 7), separated by two x-units. The final merged-data check finds no new same-row pair closer than two x-units.

### L2: Four 1980 election additions had sideways or upward prerequisite edges. Corrected.

| New focus | Child row | Required parent row |
|---|---:|---:|
| `USA_X_dem80_retool` | 29 | 29 |
| `USA_X_dem80_newfirms` | 29 | 29 |
| `USA_X_rep80_invest` | 29 | 29 |
| `USA_X_rep80_fiscal` | 29 | 30 |

The initial graph was acyclic, but those edges ran horizontally or upward. In the final concept, all four new 1980 entries are on row 33 and their follow-ups are on row 34. The latest existing required parent is on row 30. The original parents remain intact, including the distinct 1981 budget parent of the fiscal alternative. The final merged-data check finds no new focus with a same-row or upward prerequisite edge.

### L3: Intermediate zoom requires visual confirmation

The SVG keeps labels and detailed circles at a fixed screen size while the coordinate spacing changes with zoom. It enables labels at a scale greater than 0.48. At the lower end of that range, adjacent rows are approximately 63 pixels apart, while a three-line title extends to about 65 pixels below its node centre. Multi-line titles can therefore meet the next row's circle. The primary author should either confirm readable branch fitting or raise the label threshold, adapt detail density or keep sufficiently large row gaps. This is a renderer risk identified statically; it is not a claim that every branch currently exhibits a collision.

## Available screenshot inspection

`usa-review-tree-final.png` shows the corrected Atlantic module with seven visible focuses, including the Atlantic Bargain, both Bonn alternatives, the Auto Pact, British escort exercises and both follow-ups. At the shown width, these visible icons and titles do not overlap. The exclusive connector between the Bonn offers is visually distinct from ordinary prerequisites. The selected Bonn offer inspector visibly labels `If they accept` and both countries. The earlier `usa-review-tree.png` additionally shows the separate forward-defence spirit names, setup costs and weekly terms; the final screenshot does not display the full terms area, so it is not evidence of every numeric line.

The screenshot is a filtered view. It does not itself establish that the British node clears the NCO programme, because that programme is absent from the filtered module. Their final separation and the revised 1980 rows were checked against the full merged coordinate model. Browser interaction, narrow-width behaviour, intermediate zoom and other branch screenshots remain covered by the primary author's checks rather than this bounded screenshot review.

## Positive concept-layout observations

- The first election forks have different follow-ups and use a specific meaningful parent rather than a new ceremonial entry focus.
- The general military programme is no longer gated by an intelligence choice.
- Atlantic and Middle East cooperation remain reachable under all three general doctrines.
- Japan, South Vietnam, China and Soviet channels include later general-diplomacy access instead of depending solely on a missed Nixon administration window.
- The Bahrain facilities offer and the existing sovereignty-transfer offer are symmetrically exclusive.
- Removed region-wide Israeli/Arab/mediation exclusions are represented in the merged graph rather than merely described in prose.
- Every authored offer's inspector can expose its full paired prospective terms independently of the selected agreement-state illustration.

## Evidence boundary

The graph tests do not evaluate real ruling-party triggers, date windows, membership spirits, treasury affordability, sanctions, temporary-deadline behaviour or state ownership/capacity. The concept does not implement any of its 52 new focuses. Text and connectors in the HTML approximate MD; small preview icons are reduced derivatives of existing local art, with their provenance in `preview_provenance.json`. L1 and L2 are resolved in the final metadata. The independent review clears the final graph's references, basic coordinate separation and downward progression, while L3 remains a presentation consideration for the author's browser QA. It does not constitute native-engine or exhaustive rendered whole-tree validation.
