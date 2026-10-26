# North Korea 1970 expansion layout review

**Scope:** Full emitted `COLDWAR_NKO_1970_focus` tree, all 360 focuses.

**Preview reference:** `preview_manifest.json` source SHA-256 matches the emitted focus file (`2f2c1d7510668fce021d0ae1bcb34081e5eff177f91cedc913f5af9d23c8a9e1`). The manifest uses the installed 96 × 130 focus grid, 165 × 128 item bounds, a 147 × 20 title field, the installed `hoi_16mbs` glyph atlas and the actual registered focus icons. Connector routing is approximate; the preview is not an in-engine render.

## Geometry and graph checks

- All 360 design IDs occur in the emitted focus tree. Resolved positions match `current_design.json`; root absolute coordinates, child anchors and relative offsets, grouped prerequisite blocks and mutual-exclusion links also match.
- No native-card bounds overlap within or across branches. The staggered lower roots fit their preceding footprints: KPA/Yan'an begin at y=17 after the defence subtree ends at y=13; Union begins at y=13 after diplomacy ends at y=9; KDP begins at y=25 after WPK ends at y=21; Chondo/cabinet begin at y=29 after economy ends at y=26; Christian/Jong Il begin at y=25 after China/Soviet end at y=21. Approximate emitted connector routes produced no cross-branch card intersections.
- No focus has a mutual-exclusion link to itself, and the graph-only prerequisite/MEX satisfiability check found no focus without a conflict-free prerequisite history. The four independently investable defence programmes occupy separate columns and each begins from the existing `military_research OR readiness_inspections` gate. Their internal alternatives and joins remain legible in the defence branch view.
- Patron nodes now occupy rows 12–21. China places Domestic Procurement at (58,19) and Balance of Relations at (54,21); the Soviet branch places Command Exercises and National Standards at y=19 and the Security Compact at y=21. Both final joins remain legible in their normal-scale previews.
- No new eligibility helper adds its own date gate. The added Investment Accounts industrial continuation follows Joint Ventures and inherits its existing `date > 1984.9.7 OR early_venture_law` requirement; the approved timing is retained, so that continuation is not immediately reachable in 1970. Existing dated helpers also remain attached to The Ten Principles (1974) and The NPT Bargain (1985).
- Sixteen shortcut targets are present, including one for every lower political root. The initial view remains anchored on The Fifth Congress.

## English title and visual checks

- All 360 focus titles and descriptions have English localization entries (720 keys). Every localized title exactly matches the title used by the preview design data.
- Measuring titles with the installed `hoi_16mbs` glyph advances found no title wider than the native 147 px field. The widest is **Community Associations** at exactly 147 px; it renders inside the field.
- Inspected the full overview and normal-scale branch previews for WPK, economy, defence, diplomacy, atomic policy, foreign diplomacy, successor, KDP, Chondo, cabinet, KPA, Yan'an, union, Christian, China and Soviet branches. Actual registered icons and native title glyphs are visible. No title clipping, card collision or material connector-through-card issue was observed.

## Review note and limits

The staggered lower roots make the full overview more compact while preserving three to four grid-row intervals (two to three empty focus rows) between adjacent subtree footprints. Sixteen shortcut targets remain present, including the lower political and patron roots, and the initial view remains anchored on The Fifth Congress. The preview renderer does not establish exact engine connector routing, live camera behavior, hover states or conditional focus visibility in HOI4.
