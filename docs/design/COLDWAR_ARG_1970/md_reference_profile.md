IMPERIA COLD WAR

# Argentina 1970 concept: MD layout reference profile

## Scope and sources

This is a measured layout and presentation reference for an Argentina tree concept of roughly 170 to 220 focuses. It records native MD examples and project architecture, not Argentina branch content or runtime recommendations. No runtime files were changed.

Reference installation: Millennium Dawn workshop content `394360/3374271790`, inspected 2026-11-01. Main source files: `common/national_focus/00_generic.txt`, `05_france.txt`, `05_russia.txt`, `05_germany.txt`; UI: `interface/nationalfocusview.gui`, `nationalfocusview.gfx`. Argentina has no country focus source or Argentina-specific design doc in the current project checkout. Existing country systems include `common/countries/Argentina.txt`, `common/characters/ARG.txt`, Argentine decisions, and `common/scripted_effects/ARG_political_leaders.txt`.

Counts and resolved coordinates below come from brace-matched full focus block scans, recursively resolving each `relative_position_id` as anchor absolute coordinate plus local x/y. France, Russia, Germany, and Generic include legacy content and are density references, not recommended country-size targets. No game launch or GUI render was performed.

## Measured tree profiles

| Tree | Focuses | Resolved bounds | Focus cost distribution | Navigation / notes |
|---|---:|---|---|---|
| MD France | 381 | x 2..194, y 0..9 | Most frequent 5 (128), 10 (110), 6 (28), 7 (22), 8 (37); also fractional costs | 4 shortcuts: politics, diplomacy, economy, military; continuous focus pocket at (100,1000) |
| MD Russia | 806 | x 0..235, y 0..26 | Most frequent 3 (314), 5 (216), 7 (168), 2 (76) | 6 shortcuts; shared focuses; continuous focus pocket at (17000,1000); initial view x=2,y=0 |
| MD Germany | 588 | x 23..209, y 0..19 | Frequent 4.3, 6.5, 7.15, 7.9, 10; legacy fractional costs | Large energy and industry trunks with repeated forks and joins |
| MD Generic | 158 | x -13..51, y 0..10 | 10 most frequent (103), then 7.86 (29) | Compact one-screen-scale reference for standard sectors |

In native focus data, `cost = 10` is the usual 70-day focus; smaller costs scale proportionally in the standard focus system (for example 5 is 35 days and 1 is 7 days). MD uses fractional cost values in many older trees. For a new concept, use a deliberate small set of readable costs unless the chosen local focus-duration modifiers require otherwise.

### France political fan and sector layout

`05_france.txt:35` begins with `FRA_state_of_french_politics`, absolute `(68,0)`, cost 2, icon `french_republic`. The next nine visible party cards sit at y=1 relative to this focus. Their x offsets are `-45, -32, -21, -10, 0, 10, 21, 32`; the available cards span a wide fan. They cost 1 each. The source blocks begin at lines 60, 105, 157, 205, 254, 306, 352, and 393 for the listed party branches, with the zero-offset UDF/LREM block at line 105. `FRA_friend_eu` at line 440 is at `(56,2)`, one row below `FRA_PS` at `(58,1)`, demonstrating a branch that begins close to the party node then develops independently.

France uses named absolute sector roots, with children positioned relative to roots or local predecessor anchors. Top-level sections include the party fan, diplomacy, economy, armed forces and France-specific institutions. The full tree's compact y range reflects short parallel branches, not one very tall sequence. Its broad x range is appropriate for simultaneous alternatives remaining visible.

The party fan is a helpful precedent for Argentina's visible party programmes: put the fan after a small shared political context root, reserve space across all alternatives at once, and keep the currently non-governing party cards inspectable. Do not copy France's x positions directly. Its 9-way fan is already wide; Argentina should allocate a measured row or staggered fan according to actual concurrent visible cards and title bounds.

### Russia sector roots, forks and joins

`05_russia.txt:51` starts `SOV_reign_of_yeltsin` at `(62,0)`, cost 1. `SOV_subjects` at line 81 is `(62,1)` relative to that root, and `SOV_putin` at line 108 is `(75,1)` relative to it. This separates the federal/subject trunk from the Putin political programme at 13 columns of horizontal spacing.

`SOV_putin` then anchors several branches: `SOV_the_grand_bargain` at line 155 is `(75,2)`, with costs mostly 5 to 7 in its first tier; NPP, cabinet and stabilization branches begin at relative offsets around -2, +2 and 0, y=2 from Putin. Long-term political outcomes visibly split and merge: `SOV_oligarchic_republic` and `SOV_combined_economic_system` at y=7 both require `SOV_gen_3_nuclear_plants` and `SOV_revision_6`, while other branches continue separately. Keep such real AND joins visually centered between their incoming branch endpoints, and preserve their AND versus OR grouping.

Russia's many top-level sector roots share a very wide canvas; an audit of this source found most foci use relative anchors and most offsets stay within a few columns of their parent. The design lesson is to organize around stable thematic roots, then keep local branch offsets compact. Do not make every focus absolute, and do not connect every visual section with long diagonal lines.

### German precedent for gated programme content

Germany is 588 focuses over 20 rows and includes long economic/energy chains. It shows a useful difference between independent eligibility and branch visibility. Its source uses `available` for land/state/technology requirements, and actual government requirements appear as checks inside gameplay logic. France has some legacy `allow_branch` uses for special/extremist subbranches (`05_france.txt:6250`, `9882`). These older patterns should not override the project rule: keep all party programme branches visible and inspectable, while gating availability, focus activation, and reward execution with the actual ruling-party trigger. Reuse the installed MD party-in-power trigger and name localisation for requirement text.

## Native geometry and title bounds

The active MD GUI declares `national_focus_item` as 165 by 128 at `interface/nationalfocusview.gui:536-538`. Its title textbox starts at `(15,58)`, uses `hoi_16mbs`, has max width 147 and max height 20 (`:575-586`). The focus symbol is centered at `(5,-44)` relative to the item container, and clipping is disabled. The container dimensions are not the same as the clickable title/art footprint; adjacent x positions can use native grid spacing while long titles and prominent art still need review at rendered scale. Keep Argentina names concise enough for the native single-line title field where possible, and inspect title collisions in neighbouring rows, not just center-to-center distances.

The target GUI also explicitly defines `focus_spacing` as `(96,130)` at `interface/nationalfocusview.gui:664-667`; the installed donor has the same values. This is the preview coordinate conversion. The base game's `common/defines/00_graphics.lua:1341-1344` sets focus-tree zoom to 0.2 through 1.0. The concept's fit-entire-tree overview is therefore a schematic reduction beyond the normal minimum game zoom. Chapter views preserve the native coordinate spacing; the overview does not claim to reproduce a possible single in-game camera view.

`nationalfocusview.gfx` provides native unavailable and can-start titlebar states (`GFX_focus_unavailable`, `GFX_focus_can_start`) and focus link sprites. Leave global GUI sizing, fonts, titlebars, and icon scale unchanged. Use actual native/MD goal sprites at their normal size. France's party portrait/symbol icons (`FRA_ps_party`, `FRA_udf_party`, `FRA_larem_party`, `FRA_cdg`, `FRA_la_france_party`, `FRA_eelv_party`, `french_communist_party`) demonstrate faction-specific icons; Russia uses institution and subject symbols (`RUS_flag`, `SOV_federation_council`, `sov_npp_more`) plus general MD industry/government goals. These are asset identifiers and style references only; check definitions and texture appearance before reuse in Argentina.

The installed GUI layout places the tree beneath the title, with native minimap, search and zoom controls, and a shortcut grid sized for up to eight rows in this view. Shortcuts are valuable when a large tree spans sectors, but every shortcut must land on a recognizable section root. Use an opening focus near the shared political setup and add a small set of shortcuts for Argentina's major political programmes and broad policy domains. A two hundred-focus tree should not require opening at an arbitrary far corner.

## Project Soviet 1970 architecture reference

The loaded project tree is `common/national_focus/COLDWAR_SOV_1970_focus.txt`; its header at lines 9 to 80 uses a dedicated tree id, scenario-gated country selector, an initial view on the collective-leadership entry, a shared Union tree, and 11 section/programme shortcuts. It starts at `(93,0)`. The file documents that its generator is canonical, so it was inspected but not run.

Project layout source `Claude outputs/COLDWAR_SOV_generator/cw_layout.py` uses section anchors and reserved subtree footprints. `cw_focus.py` converts resolved design positions to offsets from their section anchors. The project audit records six principal roots and relative child anchoring. This is the best local architecture reference for a deep programme tree: define themed sections with stable roots, reserve space for their full branch footprints, place party/leader programmes as visible clusters, and use navigation to reduce travel. It is not a requirement to copy the Soviet canvas width, number of shortcuts, or any Soviet-specific institutions.

## Reusable arrangement proposal for Argentina

For about 170 to 220 focuses, use around 6 to 8 stable section roots across a broad canvas, with about 8 to 12 vertical rows per active cluster. Keep sector spines mostly vertical. Use x offsets of 1 to 3 columns for a local fork, a compact 1 to 3 column offset back toward a spine for nearby merges, and larger deliberate gaps between full domains. Use about 10 to 14 columns between unrelated major roots, then enlarge separation where multiple party choices run in parallel. The France fan's 10 to 11 column party spacing is evidence that several simultaneously visible branches need real width. These are planning ranges, not engine limits.

A plausible spatial allocation, without prescribing policy content, is:

- One shared political and 1970 starting context spine near the opening camera.
- A wide, short fan of all relevant party programmes, with each programme's full subtree footprint reserved before adding shared content beneath or beside it.
- Internal movement and alternative programme choices in a dedicated adjacent cluster, with mutually exclusive cards co-visible and non-overlapping.
- Economy and production as one deep sector, with major subsectors as short parallel chains and genuine shared-outcome joins centered under them.
- Armed forces and security as a separate sector with parallel service/institution chains and a readable join only where the parent requirements are truly common.
- Bilateral diplomacy in a dedicated wide band with named counterpart/groupings and visible focus branches, linked back through appropriate short prerequisites or eligibility checks.

Prefer section-root-relative positions over long chains of fragile anchors. Use predecessor anchors for short straight spines and branches, stable section anchors for unrelated sibling rows, and absolute coordinates only for section roots. Use `available` only when a real eligibility check should not draw a connector. Keep political branch visibility unconditional; actual ruling-party guards belong in focus availability and reward effects, not `allow_branch`. Use distinct native icons by institution or policy domain and reuse shared icon families sparingly so neighbouring alternatives remain distinguishable.

Before approval or implementation, resolve every anchor recursively, check the complete simultaneous-visible layout, capture overview and normal-scale branch previews with native icons and English titles, and inspect the opening camera, shortcut targets, and lower/outer extents. Graph-only diagrams cannot establish title, icon or rendered connector clearance.

## Unverified

No native game screenshot was taken. No icons were visually inspected at target in-game scale. The profile uses parsed source coordinates and static GUI dimensions, not engine-rendered collision results. Cost-to-days descriptions assume default focus duration modifiers. The local project has no Argentina focus layout to compare.
