# COLDWAR IRQ 1970 â€” independent layout review

18 October 2026. Final approval concept: **396 focuses, 22 sections, 72 decisions**. Read-only review of the catalogue, independently parsed specimen, English localisation, embedded browser data and raster previews. No loaded mod files or authoring sources were changed by this reviewer. Final title/coordinate/art changes are included below.

## Verdict and final snapshot

**PASS for static geometry, graph consistency and reviewed visual presentation.** All 396 specimen focuses match the JSON IDs, raw offsets, relative anchors, resolved positions, grouped prerequisites, reciprocal exclusions, icons and costs. Every focus has a satisfiable prerequisite history. All 396 English localisation names match the short card names and fit the native147px text width. Full-tree card/connector geometry has no unresolved overlap.

| Artifact | Final SHA-256 |
|---|---|
| `COLDWAR_IRQ_1970_CONCEPT.json` | `9e50677eb90d2a8e827ae19e30b30b0d0037813c079dadce28da7d5780226913` |
| `COLDWAR_IRQ_FOCUS_SPECIMEN.txt` | `eee89e45c8d71156d445636c7a6fc8ea3d4f1cde223bc5d7f440a4acbe36aafe` |
| `COLDWAR_IRQ_CONCEPT_l_english.yml` | `5557fa97a0906ddbbc16c6d882d5ef92663c0b00aa108c162b8a626d96943d17` |
| `PREVIEW.html` | `7a908579fb69890a991cca0f5ec7d5eb4ae0e0462654f5a10f81b8c01d8e97e7` |
| `BROWSER_VALIDATION.json` | `a045bf3e6fa230499436cdc28c59dd84ef9fde6ea5395c15be61e469b29585c2` |

The latest rebuilt HTML has 396 nodes and 72 decisions. Its groups,decisions and starting spirits match the JSON exactly. Every shared node field matches after removing comment-only lines from effect bodies; no executable body differs. Ownership and active-condition fields are intentionally reconstructed from each node's group/availability at runtime; that reconstruction was inspected. This is a semantic data comparison, not a claim that proposed helpers have already been implemented.

## Independent checks

Used the brace/quote/comment-aware parser documented in `MD_STRUCTURE_AUDIT.md`; no generator was imported or executed by this reviewer. Preserved the prerequisite list of lists instead of flattening OR/AND logic. Checked IDs, missing/cyclic relative anchors, offsets, resolved positions, costs,7-day point durations, icon references, exclusions, prerequisite target validity and satisfiable histories. Histories containing any mutual-exclusion pair were rejected.

| Test | Result |
|---|---|
| JSON/specimen focuses | 396/396 |
| Missing/duplicate IDs or missing/cyclic relative anchors | 0 |
| Position/anchor/offset/grouped prerequisite/exclusion/icon/cost mismatches | 0 |
| Missing/asymmetric exclusion references | 0 |
| Unsatisfiable focus prerequisite histories | 0 |
| English focus-name localisation mismatches | 0/396 |
| Drawn prerequisite edges | 462 |
| All edge vertical deltas | dy1, all 462 |
| Absolute horizontal deltas | dx0=191;dx1=117;dx2=154 |
| OR prerequisite groups | 63 |
| Focuses using multiple AND prerequisite groups | 4 |
| Full visible-card overlaps with original DDS dimensions | 0 |
| Minimum same-row native titlebar gap | 28px |
| Non-endpoint connector/card intersections | 0 |
| Proper nonincident connector crossings | 0 |
| Native-font focus names over147px | 0/396 |
| Largest measured native focus-name width | 143px |

A complete-neighbour check caught an oil/industry collision introduced by the final delivery spur: `oil_concession_delivery=(48,17)` and `industry_steel=(49,17)` had 68px of titlebar overlap. The author moved only `COLDWAR_IRQ_industry_steel` to **(50,17)**, emitted offset(âˆ’2,2) from the industry root(52,15). It now falls directly below Heavy Industry(50,16), remains 2 units from the power-grid card(52,17), and preserves its prerequisites/effects. The final complete-tree recheck above includes that correction. An isolated branch image would have missed the neighbour collision.

Four explicit AND joins are legal and intentional:

- Industry delivery review(52,23): grid management AND quality AND tax service.
- Agricultural delivery(61,23): distribution AND water inspection AND rural clinics.
- Society compact(68,24): rural schooling AND municipal finance AND science maintenance.
- Defence readiness(75,24): (armaments OR coastal-fleet maintenance) AND fuel discipline.

Their required lane endpoints are not mutually exclusive. Political cooperation and foreign acceptance requirements remain on authored side deliveries rather than silently forcing every domestic core through a foreign player's signature. Paid delivery,actual office-holding,consent and eligibility remain additional runtime conditions; they are not presumed fulfilled by static graph satisfiability.

## Complete positioning and native reference

Resolved whole-tree bounds: **x1â€¦86,y2â€¦24**, using the current native **96Ã—130px** focus grid. Two horizontal tiers have 11 root columns each, normal root interval 8 grid units. First-tier roots are y2; second-tier roots y15. The branches use ordinary leaf pitch2,dy1, deliberate broad forks and offset spines. All simultaneously visible political alternatives occupy separate reserved locations.

| Root x | First tier | Second tier |
|---:|---|---|
| 4 | Iraqi State | KDP |
| 12 | Baath Party | PUK |
| 20 | al-Bakr | Dawa |
| 28 | Saddam | Supreme Council alternative |
| 36 | Officer Republic | Iraqi Islamic Party |
| 44 | Arab nationalist alternative | Oil |
| 52 | Iraqi Communist Party | Industry |
| 60 | Aziz Muhammad | Agriculture |
| 68 | Civilian Republic | Society/Education |
| 76 | Constitutional Monarchy | Defence |
| 84 | Foreign Policy | War/Peace |

Six layout families are present:6 compact, 4 institutional-delivery-spur, 4 left-offset, 4 broad-fork, 3 conditional-delivery-spur and 1 two-stage conditional delivery programme. Branches vary in width,depth and side spurs instead of repeating one graph 26 times. Native Russia has even more varied footprint shapes; the concept adapts its measured spacing/relative-anchor grammar without claiming to reproduce every Russian topology.

The focus specimen uses `country={factor=0}` to remain inactive outside loaded content. Its camera targets actual historical starting-leader focus `COLDWAR_IRQ_bakr_presidency`. Eight shortcuts target valid roots,all with native `scroll_wheel_factor=0.80`; all 396 focuses have native search filters. `initial_show_position={focus=ID}` has direct current MD precedents in `05_greenland.txt:24` and `05_netherlands.txt:18`.

The continuous panel is specified at pixel(0,3600). The last y24node container ends at3248px,leaving 352px before the native770Ã—380px panel. Imported/shared focuses and any conditional offsets must still be checked at implementation; they are not present in the inactive local specimen.

## Actual card, font and connector checks

`MD` means `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`; `GAME` means `E:/SteamLibrary/steamapps/common/Hearts of Iron IV`. Source measurements and file hashes are recorded in `MD_STRUCTURE_AUDIT.md`.

`MD/interface/nationalfocusview.gui:446â€“607` defines a 165Ã—128node region,a 164Ã—50titlebar at(5,40),a 147Ã—20title box at(15,58),and 96Ã—130focus spacing. The CW GUI is byte-identical. Native titlebar DDS files are inherited from `GAME/gfx/interface/focusview/titlebar/`; default sprite registration is in `MD/interface/nationalfocusview.gfx:132,136,153,188`,and default states in `common/national_focus/00_titlebar_styles.txt:1`.

The preview now displays real DDS icons at their source dimensions. Visible bounds were the union of original icon,titlebar and title,including protrusion above the containerâ€”not just node-center distances or a 165px rectangle. The preview's centered symbol origin at(87.5,20) is an engine approximation. All DDS-sized cards clear each other in the complete geometry model.

Native font proof: `MD/interface/core.gfx:1447` registers `hoi_16mbs` from inherited `GAME/gfx/fonts/hoi_16mbs.fnt` and `.dds`. Metadata identifies Ubuntu Bold 16,lineHeight 16. The preview embeds this atlas and draws glyphs/kerning onto 147Ã—20canvases. Independent source-font advances confirm all 396 shortened English focus names fit, max 143px. Longer narrative naming remains in the catalogue. This fixes the earlier Georgia-font mismatch and ellipsis; surrounding browser controls are still approximations.

Connector checks reproduce the browser's actual orthogonal polyline: parent(x+80,y+90)â†’child(x+80,yâˆ’26),horizontal bar at their y-midpoint. Shared stems and intentional OR/AND joins are not counted as unrelated crossings. All462 edges descend exactly one row. This proves this preview model,not HOI4's compiled connector routing or animated glows.

## Visual inspection and art

Viewed complete native-size `FULL_BRANCH_baath.png`,`FULL_BRANCH_industry.png`,`FULL_BRANCH_agriculture.png`,`FULL_BRANCH_defence.png` and the final rebuilt oil/industry images. They show all 18 cards per programme,the side deliveries and bottom joins without clipping. English titles are readable; forks,exclusions and joins are visually clear. The rebuilt oil/industry source positions also pass the complete-neighbour calculation. The final defence image confirms the period-neutral army and naval art replacements. Re-inspected the final 22-section overview: all sections and lateral extremes remain visible at 12% zoom. Reviewed start/opposition treatment and all seven starting spirits in raster previews. The overview establishes composition,not label readability.

The art varies by policy: party/leader symbols,administration,judiciary,education,treaties,budget,oil,water,railway,procurement and naval maintenance. The final embedded asset inventory has no `soldier2`; abstract `army_reform` replaced its modern-looking soldier fallback,and `naval_upgrade` now represents coastal fleet work. Both were visually inspected. Earlier native Iraq assets carrying later flag variants remain excluded. Avoid `war_and_logistics` for generic Iraq: it is an Iranian military emblem; `focus_generic_university_3` contains an unrelated human portrait.

Additional source-verified thematic sprites in `MD/interface/goals.gfx` (paths relative to `gfx/interface/goals/`):

| Bare sprite | Line | DDS path | Size |
|---|---:|---|---|
| `focus_generic_education` | 10605 | `00_science/focus_generic_education.dds` | 100Ã—88 |
| `generic_university` | 5905 | `00_economy/generic_university.dds` | 100Ã—88 |
| `focus_generic_court` | 8801 | `00_politics/focus_generic_court.dds` | 100Ã—88 |
| `judiciary` | 9157 | `00_politics/judiciary.dds` | 100Ã—100 |
| `treaty` | 4445 | `00_diplomacy/treaty.dds` | 100Ã—88 |
| `diplomatic_treaty` | 4321 | `00_diplomacy/diplomatic_treaty.dds` | 82Ã—83 |
| `focus_generic_supply_line` | 1877 | `00_army/focus_generic_supply_line.dds` | 100Ã—88 |
| `focus_generic_reinforcing_the_supply_network` | 1869 | `00_army/focus_generic_reinforcing_the_supply_network.dds` | 100Ã—88 |
| `economic_railroads` | 5525 | `00_economy/economic_railroads.dds` | 100Ã—88 |
| `army_reform` | 1673 | `00_army/army_reform.dds` | 97Ã—86 |
| `naval_upgrade` | 8385 | `00_navy/naval_upgrade.dds` | 100Ã—88 |

The policy-art contact sheet was independently viewed at `C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/COLDWAR_IRQ_policy_art_audit.png`; the naval candidate was separately viewed. No art was generated or live GFX changed by this review.

## Remaining verification boundary

This review verifies concept/specimen spatial agreement,focus-name localisation and native-width fit,static history satisfiability,complete browser-model geometry and the named raster views. It does not certify proposed scripted-helper implementation,effect balance,engine hover rendering,literal dynamic branch hiding,saveload transitions,AI or multiplayer contracts. These require implementation and HOI4 testing after approval. Independent mechanics/history reports cover their own evidence boundaries.

The final `BROWSER_VALIDATION.json` was read after the final view-only fixes. It records **zero errors**, 66 branch views across 320/736/1024px widths, 396 focus-inspector checks and 13 government views. Its 396-node/462-edge views agree with the independent static counts. The author additionally reported successful native-font/image loading, Baathâ†”ICP availability treatment and a targeted spirit-detail camera regression test. The final embedded catalogue was independently compared again after those view-only fixes: no shared data/effect-body differences,396 nodes and 72 decisions. JSON/specimen hashes remained unchanged. No unresolved concept-layout issue remains in this review.


## Author addendum: user-selected Saddam artwork, 18 October 2026

The independent review above describes the preceding revision. This later artwork-only update replaces the Saddam root and five portrait fallbacks with the user-supplied transparent portrait, preserved unchanged in the concept assets. Its 100 x 91 preview retains the full wreath; the complete Saddam branch was visually inspected. The normalized concept hash with only icon fields removed is unchanged (`0f5fff2fc27534c9df93e32e933f1260d807f0a57a228e3a17e49a0d1275c979`), proving identical gameplay, labels and coordinates. English localisation is byte-for-byte unchanged. Existing browser QA was rerun: zero errors, 66 branch views, 396 inspectors, 13 government views, no broken images, and the supplied root icon decodes at 100 x 91. Updated catalogue SHA256: `d3bef2b2cbb30cd74f4f65e6fe0d62a2b0448f896a3e3841ab920ed6b5ef94d4`. The local artwork is explicitly unregistered until implementation approval; all other art retains its native source provenance. The initial browser view now selects Saddam for artwork inspection, without changing the proposed scenario start. This addendum is by the implementing author, not a new independent review.
