# IMPERIA COLD WAR

## France party expansion layout review

This is an independent review of the proposal preview, not an installed tree or a live HOI4 screenshot. The proposal adds 20 focuses to the 156-focus baseline, revises the dated programme identity on two existing CID focuses, and leaves the total offer count at 35. The expansion adds one decision route to the existing Regional Conversion Fund; its current and proposed requirements and unchanged effects are shown separately in the preview.

### Geometry and presentation

The full native tree remains within x=4..103 and y=0..13. Focus cards render at 165 x 128 px with 96 x 130 px grid steps. New cards use the existing France artwork aliases and native titlebar textures. The 147 px title-width audit found no overflows across the current or proposed tree. Group headings are positioned at the declared section entry coordinates, including Diplomacy at (78,8); this avoids placing that heading over the new PCF cards on row 7.

New focus coordinates and parent routes:

| Programme | Added focus coordinates | Parent route |
|---|---|---|
| Independent Republicans | (27,5), (31,5) | `atlantic_liberal` OR `europe_liberal` at row 4 |
| Radical Republicans | (47,4), (51,4) | `municipal_france` OR `europe_technology` at row 3 |
| Socialist Party | (57,6), (61,6), then (59,7) | `public_banks` OR `social_contract_ps`; the final focus joins both new row-6 choices |
| French Communist Party | (67,7), (71,7) | `communist_settlement` |
| Unified Socialist Party | (75,4), (83,4), then (79,5) | existing cooperative-exchange OR union-institutes choices; final focus joins both new row-4 choices |
| Political Ecology | (87,4), (91,4) | `ecological_industry` OR `local_sufficiency` at row 3 |
| CID | (95,3), (97,3) | `cid_cooperatives` |
| FNRI | (99,3), (103,3) | `fn_defence` |
| Centrist institutions | (37,5), (41,5) | `centrist_covenant` |

The revised RI, Radical, Ecology and Socialist Party parent routes avoid the earlier skipped-row paths through existing mutual-exclusion bars. PSU side branches also route clear of the old defence-choice bar. A connector audit found no new card intersections, connector crossings, crossings of old exclusion bars, or overlaps with exclusion bars. The check also found no card collisions, heading/card collisions, or heading overlaps.

### Verification

The current preview verifier inspected all 176 proposed focuses and all 35 bilateral offers. It checked complete offer effect rows and both countries' ownership/capacity requirements; it checked title width and visible effects for every added focus. The decision comparison confirmed the existing Fund has the same effects in both views while its prerequisite changes from Public Bank Credit to Public Bank Credit OR Conversion Boards. It passed 42 section-fit views across 320, 736 and 1024 px widths, with zero clipped nodes and zero reported failures. The inline artifact is 966,940 bytes, below the strict 1,000,000-byte ceiling.

Artifact SHA-256 values and full machine-readable geometry findings are in [LAYOUT_REVIEW.json](LAYOUT_REVIEW.json) and [PREVIEW_QA.json](PREVIEW_QA.json). Native engine rendering and game execution were not tested.
