# IMPERIA COLD WAR - Chile concept layout review

## Scope and current evidence

Reviewed the complete 184-node model in `COLDWAR_CHL_design.json`, its 15 groups, all prerequisite groups and exclusions, `build_concept.py`, `preview-review.html`, and the current MD focus GUI/GFX. The model reports 11 party programmes. This is a concept review; no loaded tree or mod files were changed.

Reviewed `preview-overview.png`, `preview-pdc.png`, `preview-pinochet.png`, and `preview-agreement.png` as well as the wrapper. No live HOI4 screenshot or engine-rendered tree was present. `preview-review.html` explicitly labels its connector routing as approximate (`:21`) and creates elbow paths from the parent's bottom center, through the vertical midpoint, to the child's top center (`:109`). I assessed every path using that exact route and the displayed 165 by 128 focus card bounds (`:41`). This is a deterministic concept-preview check, not proof of the engine's final link routing.

## Geometry and card bounds

The JSON stores resolved focus coordinates in `x/y` and local emitted offsets in `dx/dy`; anchors are the focus IDs used to emit those offsets (`build_concept.py:52-61`). The 184 positions span x=4..160 and y=0..33, matching `meta.span`. The top chapters occupy y=0..12; lower party and diplomatic chapters occupy y=17..33. Main row roots run x=8, 26, 48, 74, 90, 106, 122, 138, 154; the lower party roots begin at y=17 and the diplomacy root sits at (48,17). All 184 remain visible across government states; the preview dims other-party programmes instead of removing them (`preview-review.html:97-98,112`).

MD's current focus GUI uses a 96 by 130 grid spacing and a 165 by 128 item container (`interface/nationalfocusview.gui:536-588,664-690`). The full-position comparison found **zero overlapping focus-card rectangles** at these bounds. The closest regular same-row horizontal pitch is 2 grid units, or 192 pixels, leaving 27 pixels between 165-pixel items. The current 2-row vertical pitch is 260 pixels, leaving 132 pixels between 128-pixel items. All 178 prerequisite groups have known parents, all 223 prerequisite link instances point from an earlier row to a later row, and all 52 mutual-exclusion pairs are reciprocal. These checks agree with the model QA's no-collision and no-unreachable result, while also considering the visible item bounds.

### Donor parent-to-child row spacing

I resolved the full installed MD 2.0.4 France and Russia focus trees and measured every prerequisite edge from the parent's resolved y coordinate to the child's. France has 518 edges: 18 same-row links, then 461 at dy=1, 30 at dy=2, 8 at dy=3 and 1 at dy=4. Russia has 1,292 edges: 95 same-row links, then 1,100 at dy=1, 95 at dy=2 and 2 at dy=3. Among edges that descend, dy=1 accounts for 92.2% in France and 91.9% in Russia. A one-row vertical step is the clear native MD norm for a parent and child.

For this 184-focus concept, compress sequential branch steps from dy=2 to dy=1, and move the lower bank root from y=17 to about y=9 while retaining deliberate room around section changes and large joins. This would bring the proposed total depth from 34 coordinate rows to about 18, approximately halving the vertical scroll and making more than the current two to three levels visible in the normal viewport. The focus card leaves only a 2-pixel nominal gap at dy=1, but that spacing is what the donor uses. At 104-pixel focus art, the 130-pixel row pitch still leaves 26 pixels between icons; validate titlebars and links in the native-scale capture after compaction. Avoid keeping dy=2 as a default solely to create blank space.

## Prerequisite connector collisions in the review route

The exact preview elbow route intersects a third focus card on five of the 223 prerequisite links. The links are rendered behind focus cards, so the intersecting segment is occluded and can appear to enter from the wrong side or vanish before reaching its child. The review captures show these banks are hard to follow at their present depth. Clear the intersecting paths while compacting, then validate the native elbow join around each row.

| Link | Coordinates | Intervening card | Layout adjustment to consider |
|---|---|---|---|
| `COLDWAR_CHL_corfo_plan` to `COLDWAR_CHL_rural_extension` | (26,0) to (20,4) | `COLDWAR_CHL_negotiated_copper` (22,2) and `COLDWAR_CHL_national_copper` (26,2) | Give the long CORFO-to-rural link a clear elbow lane, or reposition the copper choices and/or rural branch so the selected route does not pass through either card. Preserve the single CORFO prerequisite. |
| `COLDWAR_CHL_corfo_plan` to `COLDWAR_CHL_price_compact` | (26,0) to (30,4) | `COLDWAR_CHL_national_copper` (26,2) and `COLDWAR_CHL_concession_copper` (30,2) | Route around both the source and destination columns, or move the price focus/choice row to leave a continuous clear elbow. |
| `COLDWAR_CHL_corfo_plan` to `COLDWAR_CHL_monetary_restraint` | (26,0) to (34,4) | `COLDWAR_CHL_national_copper` (26,2) and `COLDWAR_CHL_concession_copper` (30,2) | Move the monetary focus to a clear route or lay out a deliberate outer elbow. Keep its CORFO-only gate. |
| `COLDWAR_CHL_andean_admission` to `COLDWAR_CHL_andean_industry` | (48,21) to (46,25) | `COLDWAR_CHL_peru_maritime` (46,23) | Shift the Andean industry destination or use a clear side lane around the Peru agreement focus. Preserve its admission prerequisite and spirit requirements. |
| `COLDWAR_CHL_andean_admission` to `COLDWAR_CHL_andean_autonomy` | (48,21) to (50,25) | `COLDWAR_CHL_bolivia_transit` (50,23) | Shift the autonomy destination or use a clear side lane around the Bolivia agreement focus. Preserve its admission prerequisite and spirit requirements. |

These are specific collisions in the current HTML review elbow. They are not speculative center-distance complaints. Recheck after any position change against all neighboring rows and rebuild the native-scale view before settling the fix.

## Mutually exclusive connector collisions

The current preview draws same-row exclusions as a horizontal red line between focus centers at y+45 (`preview-review.html:110`). Five rows contain a full three-focus exclusion clique with the middle card directly between the outer cards. Keep all three pair exclusions in the design and runtime logical matrix, but draw only the two adjacent visual links, left-to-middle and middle-to-right. This leaves the middle focus in place and preserves the clique.

| Clique row | Focuses left to right | Draw these two visual links while retaining all three logical pairs |
|---|---|---|
| Copper alternatives, y=2 | `COLDWAR_CHL_negotiated_copper` (22), `COLDWAR_CHL_national_copper` (26), `COLDWAR_CHL_concession_copper` (30) | negotiated to national; national to concession |
| Gremialist programme, y=23 | `COLDWAR_CHL_gremial_tutelage` (102), `COLDWAR_CHL_gremial_electoral` (106), `COLDWAR_CHL_gremial_guildrule` (110) | tutelage to electoral; electoral to guild rule |
| MIR programme, y=23 | `COLDWAR_CHL_mir_agreement` (118), `COLDWAR_CHL_mir_command` (122), `COLDWAR_CHL_mir_nonalign` (126) | agreement to command; command to non-alignment |
| Pinochet programme, y=27 | `COLDWAR_CHL_pinochet_rescue` (142), `COLDWAR_CHL_pinochet_losses` (146), `COLDWAR_CHL_pinochet_supervision` (150) | rescue to losses; losses to supervision |
| Pinochet programme, y=31 | `COLDWAR_CHL_pinochet_technocrat` (140), `COLDWAR_CHL_pinochet_security` (144), `COLDWAR_CHL_pinochet_plebiscite` (148) | technocrat to security; security to plebiscite |

## Art, UI states and navigation

The MD item and titlebar state assets are present in `interface/nationalfocusview.gui` and `interface/nationalfocusview.gfx`: unavailable, can-start and completed bars, plus native elbow link sprites (`nationalfocusview.gfx:42-107,132-188`; GUI item and text fields at `nationalfocusview.gui:537-588`). The preview's semantic icon map names existing donor candidates such as `GFX_focus_CHL_high_quality_nitrate`, `GFX_focus_CHL_strengthen_the_central_bank`, `GFX_goal_generic_army_doctrines`, `GFX_goal_generic_diplomacy`, and the native `GFX_focus_unavailable` bar (`build_concept.py:451-466`). The concept captures show these motifs at the intended review scale. The shared briefcase motif across diplomacy offers is visually repetitive; consider other existing MD diplomacy or trade icons where the subject fits. The captures are local HTML compositions and do not establish exact in-game texture sizing or titlebar rendering.

The PDC, Pinochet and agreement captures show only about two to three vertical levels in the normal viewport at the current dy=2 pitch, with the next row clipped below the view. The full overview has a broad empty band between upper chapters and the lower programme bank. This supports compressing sequential levels and moving the lower bank upward. At normal scale, several names are cut off by the preview's single-line 147-pixel title field: examples include "Community Social Devel...", "Tomic's Popular Converg...", "The Service Chiefs' Admi...", and "Soviet Machinery and Te...". Shorten long focus titles to fit, especially repeated agreement cards. Focus art is legible in the group captures; the compressed overview works for section relationships but not for reading focus titles.

The opening focus is `COLDWAR_CHL_constitutional_mandate` at (8,0), so the initial view is anchored at the Republic's entry. The continuous panel proposal is (768,2080) in the design metadata. A tree-window capture is needed to confirm that initial viewport and continuous panel placement together. Party groups remain visible in every government layout; review the starting PDC view, Popular Unity choices, and the later military government view at normal zoom. The preview UI's government filter is an inspection aid, not engine conditional loading.

## Independent party-slot correction

The existing MD native leader pool is inconsistent with Chile's January 1970 registry. Do not carry its slot 3 Allende mapping into this concept. The proposed Chile mapping is PDC/Tomic-Aylwin in slot 1, PS/Allende in slot 18, PR/Baltra in slot 3, and Pinochet in slot 22, subject to the design's actual ruler and identity guards. This correction is recorded in the concept integration notes and updated `MD_REFERENCE.md`; it is separate from the geometry audit.

## Review disposition

The first-pass card positions passed the full-tree 165 by 128 bounds check. The original recommendation to compress sequential levels and move the lower bank has been implemented in the current concept; see the superseding review below. No runtime code was changed.

## Superseding review: compact layout preview

This section supersedes the first-pass layout recommendations above for the updated concept positions and captures inspected on 2026-10-31. The current model has 184 focuses, 15 groups, 223 prerequisite links, and 52 logical exclusion pairs. Its span is x=4..160, y=0..17; lower-bank roots now start at y=9. All focus anchors resolve, all prerequisite references exist, and every exclusion pair remains reciprocal. The full 165 by 128 card comparison again finds zero focus-to-focus overlap.

Ordinary sequential focus levels now use dy=1. The donor measurement supports this: France uses dy=1 for 461 of 500 descending prerequisite edges (92.2%); Russia uses dy=1 for 1,100 of 1,197 (91.9%). The updated overview uses the vertical area evenly, and the PDC, Pinochet, and diplomacy captures show more branch depth in the same normal viewport. The art and titlebars remain distinct, with foreign-agreement art varied by subject. There is no live HOI4 screenshot, so these findings describe the labelled browser composition, which states that native font and connector routing are approximated.

An independent title overflow check ran against the actual headless Brave rendering of `preview-review.html`: all 184 rendered title spans have `scrollWidth <= clientWidth` at the 147-pixel maximum. The inspected PDC, Pinochet, agreement, and overview images also show the shortened names fitting. This supersedes the first-pass note about truncation.

### Updated connector and exclusion check

I reran the exact preview elbow model against all 223 prerequisite links using the updated 165 by 128 item rectangles. No edge crosses focus art or a title bar. A strict full-button rectangle test flags 27 geometric contacts, each only 1.5 pixels into the otherwise blank bottom edge of a peer item. This follows from the preview elbow midpoint at y+126.5 inside a 128-pixel button; the title bar ends at y+115 and the focus art at y+88. The updated screenshots show the links below the art and title content. If zero intersection with the complete button rectangle is required, place link ports at the item bottom and child top, then rerun the whole tree geometry. Do not move focus nodes for these blank-edge contacts alone.

For same-row exclusions, the preview draws 47 visual links from the 52 logical pairs. It omits only the outer-to-outer edge in each of five complete three-focus cliques; adjacent links still show each clique, while all three exclusion pairs remain intact in the design data. This resolves the former line-through-middle-card issue without relocating the middle focus.

The diplomatic and Andean branches show clean visible routes in `preview-agreement.png`: Andean industry and autonomy now sit at x=46/50, y=15, below the y=12 agreement row. On the tested route, those children no longer intersect the agreement cards. The remaining long diplomatic service links only touch the blank bottom edge of the first agreement row, as described above.

## Final current disposition

The compact 17-row concept passes the full focus-card overlap check; all 184 title labels fit in the current HTML rendering; and all logical references and exclusions remain complete. The former visible-content prerequisite crossings are resolved. The only strict geometry finding is the 1.5-pixel contact with blank item-box bottoms on 27 dy=1 links. The generated captures are not engine screenshots. They do not prove live HOI4 connector routing, native title font, camera, or shortcut behavior. No design JSON, generator, preview, or loaded mod asset was changed by this review update.

## Final supersession: preview connector ports

The current preview now starts prerequisite links at the parent card bottom (`py(parent)+128`) and ends at the child card top (`py(child)`). This changes rendered connector ports only; focus positions are unchanged. I independently rechecked all 223 prerequisite paths against all 184 focus rectangles at 165 by 128 pixels: zero unrelated-card intersections and zero focus-card overlaps. The current `BROWSER_QA.json` independently records 223 checked links, zero collisions, zero title overflow, and zero missing art. This supersedes the 27 blank-edge contacts recorded immediately above. The preview remains a browser composition, not a live HOI4 engine test.

## Staged native-tree compiler audit

I also checked the implementation-stage files in `tools/chile_1970/stage`, without editing or installing them. The emitted `COLDWAR_CHL_1970_focus` contains 184 unique focuses. Reconstructing absolute coordinates from every emitted anchor and local x/y offset yields zero mismatches against the approved design; the compact bounds are x=4..160, y=0..17. All 223 prerequisite edges, 178 prerequisite groups, and 52 mutually-exclusive pairs exactly match the approved JSON. All 184 focus rewards route the displayed effects through the matching preview helper and their real effects through the matching guarded apply helper. The staged reward inventory includes 21 building grants; each preview and payout includes a state shared-slot grant and construction. The tree adds no party-dependent `allow_branch`, and its icon keys resolve to existing MD `goals.gfx` assets. This is a static staging audit, not a live event popup or game-rendered tree check.

The PDC and Pinochet browser captures show legible focus labels and the expected named party/leader requirements with numeric consequences. The design preview does not validate MD's live tooltip renderer. In particular, verify in the engine that scripted `COLDWAR_CHL_can_complete_*` wrappers do not expose the internal scenario/date or receipt checks as raw tooltip text; those remain runtime guards in the staged source. No HOI4 process was launched during this audit.
