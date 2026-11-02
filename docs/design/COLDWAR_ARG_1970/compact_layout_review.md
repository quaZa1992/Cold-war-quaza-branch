IMPERIA COLD WAR

# Argentina 1970 compact layout review

## Scope and sources

Independent review of the compact Argentina focus layout requested by the user. I inspected `tools/argentina_1970/layout.py`, the runtime design and baseline manifest, the emitted `common/national_focus/COLDWAR_ARG_1970_focus.txt`, the measured MD profile in `md_reference_profile.md`, and the regenerated `runtime-preview.html`. The preview uses the native focus art and titlebars. It is a browser composition, not an HOI4 screenshot.

The measured UI reference is the installed MD `interface/nationalfocusview.gui`: a 96 by 130 focus grid, 165 by 128 item container and 147 by 20 title field. Exact game rendering and connector routing remain engine-only checks.

## Structural review

The baseline records the pre-layout positions and a normalized semantic SHA-256. Recomputing that digest from the compact runtime design after removing only node positions/offsets, group positions and the layout revision matches the baseline: `8457ed7d5367f146a97d595fb395c3f5c7720355f54c5193af443fa9dcfae7a9`. This confirms the recorded non-geometric design data is unchanged.

I independently parsed the emitted focus blocks and recursively resolved their relative anchors. All 299 focus IDs resolve, with no missing or cyclic anchors, and their absolute coordinates match the runtime design. The emitted file contains 342 prerequisite targets, matching the approved groups. The new bounds are x=2..100 and y=0..23; baseline bounds were x=2..222 and y=0..36. Eight party-programme column pairs and three adjacent national-policy pairs are kept as distinct visible sections. No party branch is hidden by governing party.

Using the measured grid and item size, an independent axis-aligned card-box sweep found zero overlaps among the 299 positions. The project validator additionally reports zero orthogonal prerequisite-route card cuts, zero title overflow, zero title/card overlap and a clear continuous-focus pocket. These checks cover the complete tree rather than only the sampled crops.

## Visual review

I rendered the updated runtime preview in Brave at the full-tree overview and inspected native-scale chapter views for the FFAA, constitutional institutions, diplomatic partners, science, defence and Malvinas branches. The overview keeps the 16 party programmes in eight adjacent column pairs, with the shared programmes grouped to their right. Native-scale views show legible cards and titles, clear separation between alternatives, and short joins that remain readable at the measured grid. In the sampled military and Malvinas alternatives, the dashed exclusion rails pass through open space between the cards. No concrete focus-ID collision, card collision, clipping or unclear join was found.

The new arrangement preserves the 8 existing shortcuts and their section targets. The opening focus remains the FFAA entry, now near the left edge of the compact tree. No shortcut or initial-camera regression was apparent in the browser preview.

## Verdict and limits

The compact layout is geometrically and visually sound in the inspected browser preview. The comparison and anchor checks support that gameplay requirements, prerequisite groups, exclusions, rewards, costs and visibility remain frozen. This review did not change project code or design data. Native HOI4 card rendering, exact connector routes, scrolling and shortcut behavior were not tested in game.
