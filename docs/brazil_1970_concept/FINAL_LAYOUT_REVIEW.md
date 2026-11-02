IMPERIA COLD WAR — Brazil 1970 final layout review

Date: 2026-11-02  
Scope: Independent structural and visual review of the final `concept.json` and its static native-art reconstructions. This remains an unapproved concept. I changed only this review document.

## Verdict

The revised 224-focus model resolves the previous layout blockers. The final rendered overview and all 13 branch panels are visually legible at their supplied 165x128 focus-card reconstruction scale. The compacted political row reads as separate programmes, the shared national branches are legible, and I found no visible card collision or connector passing through a third focus card. The checker reports zero title overflow, unreachable focuses, or third-card connector intersections. The old 210-focus review findings about repeated political topology, large repeated gaps, ten connector crossings, title overflow, and 17 shortcuts are superseded and are not current findings.

This is static concept and image review, not a live-browser or HOI4 screenshot. The images reproduce the declared card/grid layout and MD art, but cannot establish native engine placement, zoom, connector behavior, or UI state treatment.

## Final model snapshot

- SHA-256: `7637b0cbffe3fdffcb8cb9e288000f35bc225eb05c9b17c4d18518d3b92683cd` (`RENDER_CHECKS.json`, line 3).
- 224 focuses in 18 groups; resolved extent is x=0..92 and y=0..17. The group declarations start at `concept.json` line 9; the initial Armed Forces focus is at line 175.
- There are 45 mutual-exclusion pairs and 14 recipient-approved offers. The static checker finds no missing references, unreachable focuses, title overflow, or connector-through-third-card paths. I independently checked that each AND prerequisite block has at least one selectable alternative after accounting for direct exclusions; no impossible block was found.
- Main MD shows eight visible focus-tree shortcuts (`common\national_focus\nationalfocusview.gui`, lines 385-397, as sampled in the initial audit). The model declares eight shortcuts at `concept.json` line 14784, so the earlier shortcut overflow is resolved.
- Political topologies are no longer a repeated 12-group template. The only duplicate normalized topology reported by the current checker is the ARENA and PCB pair. This is a single remaining similarity to review during content approval, not a tree-wide layout defect.
- The political formations retain distinct concept identities and explicit historical context (`concept.json` lines 11-126). Party-slot collisions remain an integration dependency: Historic PTB, PDT, PT, and later PTB share slot 3; ARENA/PFL share slot 1; MDB/PSDB share slot 2; Lacerdists/PRN share slot 20. The existing Brazil registry already distinguishes ARENA 1, MDB 2, old PTB 3, PCB 4, PCdoB 19, Lacerdists 20, and the armed forces 22. These concept labels do not create new runtime identities. Resolve succession/formation identity and party triggers before implementation; do not conflate the military government with ARENA or silently reassign occupied slots.

## Visual pass

Inspected `PREVIEW_OVERVIEW.png`, `PREVIEW_POLITICAL_NEIGHBOURS.png`, and all 13 branch renders: `PREVIEW_military.png`, `PREVIEW_mdb.png`, `PREVIEW_ptb_late.png`, `PREVIEW_pdt.png`, `PREVIEW_pt.png`, `PREVIEW_pcb.png`, `PREVIEW_psdb.png`, `PREVIEW_prn.png`, `PREVIEW_society.png`, `PREVIEW_economy.png`, `PREVIEW_energy.png`, `PREVIEW_defence.png`, and `PREVIEW_diplomacy.png`. There is no separate ARENA-only render; that branch is visible in the political-neighbours panel.

- The overview (`PREVIEW_OVERVIEW.png`, 2261x614) has clear political headers and a legible division between the political band and shared branches. Its fitted scale necessarily suppresses card labels; use the branch renders for label review.
- The neighbour panel (`PREVIEW_POLITICAL_NEIGHBOURS.png`, 1941x1158) shows Armed Forces, ARENA/PDS, and MDB/PMDB with readable names, clear inter-branch separation, and no apparent overlap. Armed Forces remains a separate military programme from ARENA's civilian party programme.
- The political branch renders are individually legible. In the PDT render, the “PDT” section label is at the upper left and “Labourist Democracy” is the centered root focus; they do not overlap.
- The society, economy, energy, and defence branches use their available width coherently. Their longer connector runs are readable, and convergences terminate at visible focus cards rather than crossing a third card.
- Diplomacy is the widest panel (2325x1028) because it separates Atlantic, pragmatic, and regional partner agreements. It has substantial open space between some partner strands, but those are visually distinct sub-branches rather than unexplained gaps between repeated party templates. Keep its overview zoom/shortcut behavior in the eventual native pass.
- Supplied branch images show title text fitting within their bars at the reconstructed scale. The independent static check reports zero overflow against the declared 147px title field. This does not prove the game uses the same font rasterization or title rendering.

## Layout and reward-graph interpretation

The current 96x130 grid and 165x128 card rectangles are a useful engineering approximation, not a claim of exact game geometry. The static check supports anchor/offset resolution, non-overlapping focus rectangles, satisfiable prerequisite blocks, and non-intersecting connector paths under the preview's routing formula. Native HOI4 focus connectors and group-label placement still require engine confirmation.

All focuses have either concrete modeled effects or an offer record; the 14 offers are separate from the focus choice and visibly assigned to recipient-approved agreement flows in the concept. This review checked that branch connections and group geometry present those choices clearly, but did not audit the historical balance or runtime execution of each effect, offer, or event.

## Remaining review items

1. Resolve later-party identity and slot/trigger mappings before generating executable focus branches. The JSON records these as distinct identities but current slot numbers are shared, as detailed above.
2. During native integration, confirm the full-tree starting camera and all eight shortcut targets at game resolution. The compiled model fits the native eight-shortcut capacity, but the external preview is not the game GUI.
3. Review the only duplicate political topology pair (ARENA/PCB) as a content decision. No other group pair shares a full normalized topology in the current checker.
4. Use the historical/reward review to approve numeric effects, recurring costs, building-slot transactions, offer previews, and recipient-side consent behavior. Static geometry does not prove those runtime rules.

## Evidence and limits

`RENDER_CHECKS.json` records the concept hash and reports `title_overflow: []`, `unreachable: []`, `connector_through_third_party_card: []`, the sole ARENA/PCB duplicate topology, and eight native shortcuts. I visually inspected its listed overview and branch PNGs with the local image viewer. I did not open `PREVIEW.html` in a browser because the local-file URL attempt was denied by policy; I did not use a browser workaround. No HOI4 game was launched.
