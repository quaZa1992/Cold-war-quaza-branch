IMPERIA COLD WAR

# France 1970 V5 installed layout and art review

## Scope and result

I compared the installed generated focus tree with the frozen `approved_design_v5.json`, inspected the 1024-pixel branch renders and the 360/736-pixel responsive previews, and checked the focus and idea artwork contact sheet. The installed source matches the approved 260-focus design. The supplied images show readable cards, distinct branch grouping, and no visible card collisions in the reviewed branches. This is source and browser-preview evidence; it does not establish how the HOI4 engine renders the tree.

## Structure and navigation

The emitted file contains all 260 approved focus IDs and preserves their absolute coordinates after recursively resolving every `relative_position_id` anchor. The independent project validator passed 17,760 emitted-source checks with no issues: 260 focuses, 13 programmes, 67 mutually exclusive pairs, and 252 compatible routes. Those checks compare the installed source to the frozen design, including positions, AND/OR predecessor groups, exclusion pairs, icon assignments, focus durations, and programme routing.

All 13 shortcuts target their group's actual entry focus, and the opening camera targets `COLDWAR_FRA_progress_contracts`. Party columns keep the approved 30-grid stride, with the shared institutions branch at the left and twelve party programmes arranged across the panoramic tree. Each party's military choices occupy a compact two-column, four-row block; its foreign offers occupy the specified five-column rows. The military branch render shows the personnel alternatives converging on the shared arms allocation route, with exclusion markers visible. The Gaullist and National previews show their political/military/foreign groupings and named-country offer cards without card overlap.

Some prerequisite runs remain long by design. In the Gaullist preview, the Soviet civil-space focus sits at `[38,1]` and connects back to the Gaullist entry at `[16,0]`; that line crosses empty space and does not cover cards. The National preview likewise has long drops from its lower offer bus. These are visible and legible in the browser renderer, but native line routing should be checked in game.

## Visual checks

I viewed `v5-centre-military.png`, `v5-gaullist-foreign.png`, `v5-national-all.png`, `v5-responsive-736.png`, `v5-responsive-360.png`, and `art-contact.png` in the approved V5 preview directory. Centre military choices form a tidy forked block with clear vertical links and a visible exclusion mark. Gaullist foreign offers are spaced apart; the Soviet route is long but unobstructed, and country-specific art helps distinguish Germany and Greece. National offers remain separated despite their long connector drops. At 736 pixels the controls and focus detail remain readable, though the panoramic canvas requires navigation. At 360 pixels the preview provides arrows and fit/readable controls and keeps the selected offer detail legible; the branch itself is necessarily narrow and vertically scrollable.

The 260 focus assignments use 37 existing Cold War aliases, with country- and subject-relevant art for military industry, civilian industry, science, civil resilience, commerce, training, and Germany. The 13 shared programme pictures and five starting/residual spirit pictures use the small existing idea artwork and registered `GFX_idea_*` aliases, not focus medallions. The idea art is visually coherent at its smaller scale: political identity, labour, industry, and ecological programmes are represented by the corresponding class of icons. No artwork was edited in this review.

## Validation boundaries and provenance

The browser renders use a project preview, not the HOI4 focus-tree UI. The validator establishes that the emitted source matches the approved data and that its references resolve under project checks. It cannot establish engine parsing, actual connector placement, focus-camera behavior, shortcut behavior, sprite loading, shine animation, or in-game overlap. Those require a game launch and a native focus-screen inspection. In particular, the configured shine overlay is a stock path not present in this checkout, so its availability in the active game installation remains unverified.

Artwork paths, dimensions, focus aliases, shine pairs, and idea-picture mappings are recorded in [ICON_REVIEW.md](ICON_REVIEW.md). The reused assets' original author and licence are not identified in the project checkout and remain unknown.

## Source hashes

SHA-256 values recorded for this review:

- `approved_design_v5.json` and `proposal_v5/proposal.json`: `fc3c856880a9d48a668f454168730f08b3e64f8652caea55a34e128b42240464` (the proposal is an exact copy of the frozen approved data).
- Installed `common/national_focus/COLDWAR_FRA_1970_focus.txt`: `86a5f0602b02cca71ce50b9f9ba768c3bec94f5bfe79903ac49aa2b36caeb484`.
- `icons.json`: `4d7bcaaf6a1bf2ef51a25dde8d903e50c6dd70d60e0e3a84414ea5f313be5137`.
- `interface/COLDWAR_FRA_1970_icons.gfx`: `4e514c85731b18c06a360dd06b8af15f9b08d3f4113f5a7b07d67baf44c4d991`.

The installed focus source begins with the required `# IMPERIA COLD WAR` marker and is UTF-8 without BOM. The preview images are review artifacts, not game assets.
