IMPERIA COLD WAR — Greece 1970 Final Concept Layout Review

# Scope and evidence

Read-only visual review of `docs/greece_1970_rework_20261029/full-tree-preview.png`, `cyprus-section-preview.png`, the final `concept.json`, and `tools/greece_1970_rework_concept/preview.html`. No concept, renderer, runtime or game file was changed.

The renderer uses the native 96 × 130 pixel focus pitch and 165 × 128 pixel focus window. Its cards use the matching 165 × 128 bounds, 96 × 70 icon area and a 147-pixel title box. The final coordinate set resolves to x=0..48 and y=0..18. The 100 focus windows have no pairwise overlaps at those bounds.

# Findings

1. **The full-tree overview is balanced and all six political routes remain visible.** At the 15% fit-width overview, all eleven groups and 100 focus icons fit inside the canvas. The five common domains are above the six party/regime routes. The branch headings are separated and readable. Focus titles are intentionally hidden at this zoom, so this view is useful for the whole-tree footprint, not title QA.

2. **The visible Cyprus cards and text fit cleanly.** The 80% section view shows the root and visible branches through row 3. The visible titles, including “Prepare the Cypriot Officer Network” and “Civilian Cooperation with Cyprus,” wrap to two lines inside their boxes; no visible card, title or icon overlaps another. The dashed exclusivity links sit behind the focus art and show no collision with unrelated cards. The `gre_network` → `gre_coup` line is now vertically aligned at x=46 and clears `staff_network` at x=48 by two grid columns.

3. **The Cyprus section image is vertically clipped.** The file `cyprus-section-preview.png` stops at the map viewport after showing only the first four rows. Five of its 13 focus cards are below the crop: `guarantee_settlement` (40,4), `operational_initiative` (48,5), `gre_response` (44,7), `gre_volunteers` (42,8), and `gre_escalate` (46,8). The `fit()` code in `preview.html:115` chooses the section scale from width and enforces a minimum 80%; the map is 490px tall (`:20`). This setting cannot show rows 0–8 together. The interactive focus selector and pan controls can expose each card, but this PNG does not visually verify the lower branch. For a complete section overview, use a height-aware fit or provide a second lower-branch view.

4. **One approximate connector bus creates two cross-junctions.** In `preview.html:119`, the special `external_room` routes to `yugoslav_corridor` and `bulgarian_trade` put their horizontal bus at `sy + 12` (screen y=204 after compaction). That track crosses the short vertical links from `external_room` to `american_standard` at (32,1) and `french_option` at (36,1). It does not cross their icon or title art: it runs below the source title box, but the intersections can look like extra junctions in the diplomacy cluster. A preview-only route at `sy + 4` (screen y=196) would sit below the source title and above those first-child connector tracks, removing the crossings. Native engine routing remains unverified.

5. **The Aegean OR bus is legible but runs close to source-card bounds.** `american_standard` (32,1) and `french_option` (36,1) each appear in one OR prerequisite block for `aegean_talks` (32,2) and `aegean_deterrence` (36,2). The renderer consolidates the links on one shared track, preserving the OR meaning; it does not draw four crossing diagonals. That horizontal segment passes through the bottom 9px of the other source card’s transparent 165 × 128 button region, about 6px below the visible 43px title box. No icon or text is obscured in the screenshot. The source/renderer keep the AND/OR groups intact.

# Text and native-engine caveat

The preview’s 43px title area can show two lines. Native `nationalfocusview.gui:577-585` defines `maxWidth = 147` and `maxHeight = 20`, and its focus-name font differs from this preview’s Georgia font (`preview.html:4, 28`). Titles over 30 characters, such as “A Constitutional Return for Constantine” (39), “Technical Schools and Returning Skills” (38), and “Prepare the Cypriot Officer Network” (35), therefore need a live native-title check; the preview’s line wrapping does not prove the engine will display them fully.

The screenshot labels the external font and connector approximation. The full-tree picture shows no visible false joins at its overview scale, but it is too small to establish engine connector routing. The 80% Cyprus picture confirms its visible top portion only. Native HOI4 layout and title rendering remain the final visual check.

# Conclusion

No card or visible text overlap is apparent in the supplied images. The repaired Cyprus branch spacing is clean. The remaining concrete preview improvements are the diplomacy bus crossing two incoming links and a height-aware/full lower-branch Cyprus view; title wrapping also needs native validation.

## Addendum: refreshed renderer output

I opened `cyprus-entire-section.png` (800 × 1641) directly. It shows all 13 Cyprus-section focuses at 80%, including the lower `gre_response`, `gre_volunteers`, and `gre_escalate` path. The full section has clear card and title separation; the long visible titles fit in the preview boxes. This supersedes the earlier clipping finding for `cyprus-section-preview.png`. The refreshed renderer adds the Whole section control (`preview.html:137`) to expose the full vertical footprint.

The diplomacy preview route now places its outer bus at `sy + 4` (`preview.html:119`), above the incoming first-child tracks, and the prior false connector junction is resolved in the renderer. Exclusive-link endpoints are sorted by x before drawing (`:126`); the refreshed Cyprus screenshot shows the dashed links between the alternatives without crossing their titles or unrelated cards.

The design has shortened the long focus titles, including `Prepare the Officer Network`. The preview now exposes those labels more cleanly. It still uses an external font and approximate connectors; native focus-name rendering remains a post-approval check. No runtime test or native-engine validation was performed.
