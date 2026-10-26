# COLDWAR IRQ — independent Iran branch layout review

18 October 2026. Read-only review of the appended Iran campaign concept. This reviewer changed only this report; no live game file or authoring source was edited. Scope: all 422 focus records, 23 sections, the emitted inactive focus specimen, native art bounds, and the new 26-focus branch. Approval for live implementation remains reserved.

## Static verdict

**PASS for emitted coordinates, grouped prerequisite logic, complete-neighbour geometry and the inspected native-size branch.** The new section is a distinct 26-card campaign spine rooted at **(94,15)**, occupying **x90–98, y15–27**. Its closest existing section is War/Restraint at x82–86,y15–24; Foreign Policy occupies x82–86,y2–11. The new branch reserves its entire expansion rather than only separating its root.

The reviewer independently tokenized the emitted specimen with quote/comment/brace handling, recursively resolved `relative_position_id`, and compared every focus against the JSON. The authoring generator was not imported or executed. The parser preserves repeated prerequisite blocks and multiple `focus` entries within one block.

| Check | Result |
|---|---:|
| Specimen and JSON focus counts | 422 / 422 |
| Missing/duplicate IDs or missing/cyclic anchors | 0 |
| Position, raw offset, anchor, grouped prerequisite, exclusion, icon or cost mismatches | 0 |
| Unsatisfiable prerequisite histories, including exclusivity conflicts | 0 |
| New branch drawn prerequisite edges | 30 |
| Complete tree drawn prerequisite edges | 492 |
| Complete tree full-art/titlebar overlaps | 0 |
| Complete tree unrelated connector/card intersections | 0 |
| Complete tree proper nonincident connector crossings | 0 |
| Native title widths over 147px | 0 / 422 |
| Longest new card title | 140px |

Every node has at least one legal prerequisite history. This is graph satisfiability; current wartime, territorial, treasury and implementation-flag eligibility is additional and was not assumed satisfied.

## Choice and continuation structure

`COLDWAR_IRQ_iran_operational_plan=(94,18)` correctly requires both Southern Command `(92,17)` and the Iranian army assessment `(96,17)` using two AND blocks. Neither parent is mutually exclusive.

Short War `(92,19)` and Sustained War `(96,19)` are reciprocal alternatives. `COLDWAR_IRQ_iran_final_ultimatum=(94,22)` uses **one OR block** containing Forward Supply Depots `(92,21)` and War Contracts `(96,21)`. It therefore accepts either doctrine instead of requiring both exclusive histories. Gulf Backing `(90,21)` and Foreign Spares `(98,21)` are optional end spurs; their recipients cannot veto the drawn route to the ultimatum.

`COLDWAR_IRQ_iran_campaign_accounts=(94,24)` is another OR join of Execute the War Plan and Mobilise the Nation at y23. The two late outcomes reserve distinct lanes: territorial consolidation on the left, extended war on the right. Arabistan Secured `(92,27)` correctly AND-joins its two territorial administration programmes at `(90,26)` and `(92,26)`; Victory at Any Cost `(96,27)` correctly AND-joins Reserves `(96,26)` and Another Blow `(98,26)`. Those programme pairs are compatible.

## Native geometry and art

The reviewer re-read current main-MD Generic and Russia openings and confirmed their original audit hashes. Generic's relative spines, two-unit choice pitch and centered AND join remain applicable; Russia's independently anchored programme sections remain the reference for the reserved campaign footprint. `interface/nationalfocusview.gui:448,492,575` directly confirms the 165×128 node region, 147px title field and 96×130 grid. No global GUI or font adjustment is proposed.

Complete-neighbour calculations used the actual dimensions recorded in `ART_PROVENANCE.json`, including the supplied Saddam portrait elsewhere in the full tree. Bounds conservatively include the entire source-art rectangle plus the native 164×50 titlebar at `(5,40)`. Connector routes use the actual preview's orthogonal parent-bottom/child-top routing. Tests include all 422 simultaneously displayed cards, not only Iran or only center positions. Ordinary two-unit titlebar pitch leaves 28px; the new branch's nearest previous-sector column is four units away, leaving at least 220px between titlebars on coincident rows.

`FULL_BRANCH_iran_war.png` was viewed at native resolution. The opening demand fork, centered operational join, explicit doctrine exclusion, optional supply/credit spurs, ultimatum, campaign ledger and two deep endings are readable and uncropped. Icons retain native MD proportions, titlebars and Ubuntu Bold bitmap rendering. The bottom endings retain normal row spacing rather than stretching to fill an arbitrary canvas. `FULL_BRANCH_war.png` was also inspected as the immediate neighbour's native-size reference.

Whole-tree resolved centers now span x1–98,y2–27. The specimen continuous-focus panel is at `(0,3800)`; the longest y27 node container ends at3638px and is far to the right. Neither the new cards nor its connections approach the panel.

## Freshness and boundary

The final rebuilt `PREVIEW_overview.png` was independently viewed: all 23 sections and both horizontal tiers are visible at10% fit, including the full Iran expansion on the lower right. It clears the existing War/Restraint section and the right/bottom edges. This overview proves composition, not small-label readability. The current normal-scale `PREVIEW_iran_war.png` was also inspected: native icons, titlebars, initial demand fork and the corrected **Assess Tehran's Army** title are clear; the long branch intentionally continues below the pannable viewport. The complete rebuilt `FULL_BRANCH_iran_war.png` was re-inspected through both bottom capstones and has no clipping.

The final `PREVIEW.html` embedded data has422 nodes and23 groups. Its IDs, titles, art references, coordinates, grouped prerequisites, exclusions, durations, descriptions and reward summaries exactly match the current JSON. All422 specimen comparisons and full-neighbour geometry checks passed on the structural revision. The bounded final art/prose refresh below preserves those completed checks rather than presenting a new engine audit.

The refreshed `BROWSER_VALIDATION.json` was read independently: zero errors, zero broken images,69 branch views across three viewport widths,422 focus inspectors and13 government views. This reviewer did not rerun or overwrite that shared browser suite. Its fresh evidence replaces the preceding396-node browser result; it remains browser QA, not an engine test.

| Reviewed artifact | Final SHA-256 |
|---|---|
| `COLDWAR_IRQ_1970_CONCEPT.json` | `e1db5aa9c9a1595fb73f4db8808ecf9c28e0c0a44b046a5dd752efc2f46b5495` |
| `COLDWAR_IRQ_FOCUS_SPECIMEN.txt` | `e05d3944c8f53cbb3e9db0ab9e4fbc2f51352fab39a0f6fbbf1151b585223ac2` |
| `COLDWAR_IRQ_CONCEPT_l_english.yml` | `2185c542047ccc724b79d58fb5d875e1004aca09a2c1ac493b4005fd832d629c` |
| `PREVIEW.html` | `87f73352215a5252f98c7c1f1546a42eec5df0b56531f2f5cb158bdbbff536fa` |
| `FULL_BRANCH_iran_war.png` | `6973a51cdf0cb0c3b674bbd03689f3bb647c08331d3f23c66be7dc26ca957f65` |
| `PREVIEW_overview.png` | `2d9a465719f32bc1270a1360fc81b94b04d7cca60beb2d2462e61e0081cb5610` |
| `PREVIEW_iran_war.png` | `22d654f81cb182fd0e2ff8ca221a7e54fdd46c19a4519927a06ad789e9dda180` |
| `BROWSER_VALIDATION.json` | `889e530ebf9866e03ff7a2be6fc1356d1cf9cc7570e1d21b2773b135e38b4c1f` |

No unresolved layout issue was found in this revision.

### Bounded final art and prose refresh

Following the completed structural audit, the author replaced four new-branch art references and inserted spaces around numbers in new English prose. The reviewer independently re-inspected the resulting complete native-size Iran image, its normal-scale browser view, and the whole-tree overview. The crown and red-heart symbols have been removed from the campaign's affected cards; the resulting military, administration and oil artwork fits their policy topics.

| Focus | Position | Final native icon | Actual dimensions |
|---|---|---|---|
| `COLDWAR_IRQ_iran_frontier` | (94,15) | `army_reform` | 97×86 |
| `COLDWAR_IRQ_iran_secure_khuzestan` | (92,25) | `government_beu` | 85×85 |
| `COLDWAR_IRQ_iran_home_front` | (96,23) | `government_beu` | 85×85 |
| `COLDWAR_IRQ_iran_regional_power` | (92,27) | `oil_production2` | 94×77 |

Their emitted sprite names and offsets were compared with the current JSON. All four cards were rechecked against every tree card and every unrelated routed connector using the new actual art dimensions: zero overlaps and zero line/card intersections. No geometry or title changed. The final embedded preview matches the JSON for all displayed structural, art and prose fields checked above. The root inspector now displays readable number spacing, including “1969” and “1970” in its prose. Fresh browser evidence again records zero errors/failed images,69 branch views,422 inspectors and13 governments. The final fingerprints in the table above include this bounded refresh; the earlier structural findings remain valid.

## Superseding extension: Khuzestan core continuation and navigation

18 October 2026, later revision. **PASS for the four appended focus cards.** The concept now contains426 focuses,23 sections and30 Iran focuses. This bounded review preserves the completed422-focus audit above and checks the new continuation against all current neighbours. The fingerprints below supersede the earlier snapshot for current-artifact freshness. Only this report was edited by the reviewer.

| Added focus | Resolved position | Offset from Iranian Frontier(94,15) | Native title width |
|---|---|---|---:|
| `COLDWAR_IRQ_iran_provincial_settlement` | (92,28) | (−2,13) | 142px |
| `COLDWAR_IRQ_iran_equal_citizenship` | (90,29) | (−4,14) | 101px |
| `COLDWAR_IRQ_iran_central_administration` | (94,29) | (0,14) | 109px |
| `COLDWAR_IRQ_iran_core_khuzestan` | (92,30) | (−2,15) | 100px |

The reviewer independently parsed all426 emitted focus definitions to locate and resolve the four additions. For each addition, the raw offset, anchor, absolute position, grouped prerequisites, reciprocal exclusions, `available` block, cost and icon exactly match the JSON. Native font advances were independently measured; all four titles fit the147px field without reducing the font. Their displayed IDs, labels, coordinates, prerequisite groups, exclusions, icons, availability, descriptions and reward summaries also match the final embedded preview.

Provincial Settlement correctly descends from Arabistan Secured(92,27). Equal Citizenship and Central State Rule are reciprocal alternatives, both descending from Settlement. An Iraqi Province uses **one OR prerequisite block** containing those two policies, together with an OR of their implemented flags in availability. It never requires both mutually exclusive paths. Both histories remain structurally reachable.

The emitted settlement gate requires actual Iraqi ownership/control and peace with Iran. The two policy gates require Iraqi ownership/control of the still non-core state and delivered Settlement. The final core gate retains Iraqi ownership/control, non-core status, infrastructure≥3, compliance≥60%, resistance<15%, peace with Iran, the730-day ownership/control flag and one implemented policy. These gates agree with the catalogue. This confirms their representation and grouping; the new ownership/control clock still requires its proposed runtime integration and engine testing.

The five new prerequisite edges all descend one native row; total drawn edges are now497. New card/art rectangles were checked against every current tree card, all new routes against unrelated cards, all existing routes against the additions, and all new routes against other routes: **zero overlaps, zero unrelated line/card intersections and zero proper nonincident crossings**. Bounds use the actual court and administration artwork plus native titlebars. The exclusion line and final OR join have separate clear rows. The continuous-focus panel now emits(0,4300); the last y30 container ends at4028px and lies far to its right, leaving no collision.

The rebuilt complete `FULL_BRANCH_iran_war.png` was visually inspected through the new bottom core focus. It shows the short continuation beneath the territorial-success lane, a clear two-policy fork/exclusion, and a centered reconvergence. The final capstone and title are uncropped. The renderer's long image was scaled by the image viewer to2048px height for display; native font measurements and art-bound calculations above remain authoritative for pixel fit. `PREVIEW_navigation_core.png` was also inspected: the core inspector explicitly says **Equal Citizenship OR Central State Rule** and displays its eligibility and invoice text. Its map is a pannable viewport rather than a full-height branch image.

Navigation was tested by the author in a separate real-Chromium suite. The reviewer read `NAVIGATION_VALIDATION.json`: zero errors across12 checks covering focus/background drags, left/middle/right buttons, wheel, Shift-wheel, Ctrl-wheel, travel from Iran to Iraqi State, host-state echo, resize preservation and physical clicking of the new core focus. These gesture checks were not rerun by this layout reviewer and are not HOI4 engine QA. The refreshed general browser report independently read by this reviewer records zero errors/failed images,69 branch views,426 inspectors and13 government views.

| Current reviewed artifact | SHA-256 |
|---|---|
| `COLDWAR_IRQ_1970_CONCEPT.json` | `82deef2b498d5e67d2b5dc157eda3ba534c2a8d35de215e7f7de679ffcc24eff` |
| `COLDWAR_IRQ_FOCUS_SPECIMEN.txt` | `c083ca5e658c60b0f692a5881f437d1b1c6fc1b2d799985da273cb355953b3c9` |
| `COLDWAR_IRQ_CONCEPT_l_english.yml` | `7d2c9336f93c1a442bf373519da06f110648ca64a1503ce5dcc40a674971e0aa` |
| `FULL_BRANCH_iran_war.png` | `e64d7795e9d2bd49711045f23e138e0fc74131a332eff9c62e77b5deb1e7d804` |
| `PREVIEW.html` | `f93c8c8a9b0cb9150874e9ba200056b2db0ae6efad5859fa445c8204582fde4e` |
| `BROWSER_VALIDATION.json` | `f08cb6bac5ee9cabbaf95133a511e6afcbf80789b5304ae2a822b2d2d9182625` |

No unresolved layout issue was found in this bounded extension. Live implementation remains outside this concept review.

This is concept/specimen QA, not an HOI4 engine screenshot or runtime certification. Native connector routing, eligibility reconciliation, timed campaign integration, saved games and multiplayer behavior require implementation and an engine test after approval. The static route does not force peace, cede a province, or presume an Iranian collapse. Mechanics and historical validity are covered by their separate reviews.


## Author metadata refresh after independent review

Only the global policy-selection explanation was clarified: the Iran sector has one explicit Short/Sustained doctrine slot, and its river/Khuzestan demands remain compatible. Restoring the preceding rule string with the original Windows newline encoding reproduces the independently reviewed full catalogue hash `e1db5aa9c9a1595fb73f4db8808ecf9c28e0c0a44b046a5dd752efc2f46b5495` exactly. Thus every focus, group, decision, idea, coordinate, icon, reward, live gate and native payload is unchanged. Existing raster views and complete geometry remain representative; no rerender is necessary. The matching embedded rule was refreshed, and targeted browser QA verified it with422rendered focuses and no runtime errors. Current JSON SHA256 `d0ca1325e3abe3532ffa5967766f08f795cb76b23318091d999ea2f01eb41a7b`; PREVIEW.html `e3f7c59440a3904fe228f51ae8636ab0f593fd138cf44ecaa839ca4455fd38fa`; inline fragment `2f4a00b674e81b255a96336bbba6812c5bd08013dff7ecf8b0c97007f15a4c1e`. This paragraph is an author preservation refresh, not a new independent review.
