IMPERIA COLD WAR — Brazil 1970 native MD reference profile

## Scope and sources

Read-only source profile for spacing, coding and presentation. Reference build: latest installed MD workshop tree at `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3374271790`, inspected 2026-11-01. Main focus sources: `common/national_focus/05_brazil.txt`, `05_russia.txt`, `00_generic.txt`, and `05_germany.txt`; card interface: `interface/nationalfocusview.gui`, `interface/goals.gfx`, and `interface/countrytechtreeview.gfx`. Project start context: `history/countries/BRA - Brazil.txt`, `tools/party_registry_1970/data/BRA.json`, and `localisation/english/mdcw_1970_party_registry_l_english.yml`. No mod files or runtime content were changed.

## Full-tree geometry and logical structure

A brace-aware parser collected every focus block and recursively resolved `relative_position_id` as anchor absolute coordinate plus child `x/y`. It found no missing or cyclic focus anchors. No focus block in these three reference trees contains conditional `offset` code.

| Source tree | Focuses | Anchored | Resolved extent (x, y) | Prerequisite blocks | Blocks with multiple focus parents (OR) |
| --- | ---: | ---: | --- | ---: | ---: |
| Brazil | 338 | 329 | -24..97, -1..18 | 421 | 20 |
| Russia | 806 | 800 | 0..235, 0..26 | 995 | 100 |
| Generic | 158 | 150 | -13..51, 0..10 | 175 | 14 |

These are intentionally large, multi-programme MD trees; their whole-tree dimensions are not Brazil 1970 canvas targets. Brazil's nine coordinate roots establish separate section starts rather than a single screen-wide spine. Named examples from `05_brazil.txt`: `BRA_2002_elections` (9,-1, line 50), `BRA_nossa_economia` (-12,0, line 68), `BRA_lula` (5,0, line 246), `BRA_serra` (28,0, line 1465), `BRA_global_diplomacy` (5,6, line 2518), `BRA_nosso_exercito` (39,0, line 4837), `BRA_marinha_do_brasil` (49,0, line 4866), `BRA_cardosos_last_years` (-3,0, line 6665), `BRA_op_car_wash` (70,0, line 7163). Brazil child offsets are mainly `y=1` (263 of 338); immediate `dx=0,+1,-1` are most common. This supports compact one-step policy chains and modest fans around anchored roots, with whole-card title collision checks before reusing sibling deltas.

Russia's early Putin block is a useful large-tree fan reference: root `SOV_reign_of_yeltsin` at (62,0), `SOV_subjects` at (62,1), and `SOV_putin` at (75,1), file lines 51-114. From Putin, `SOV_the_grand_bargain` is (75,2); `SOV_npp` is (73,3); `SOV_kasyanov_govern` is (77,3); and `SOV_stabilisation_fund` is (75,3). This reads as small symmetric offsets around an institutional root, while its later separately rooted sections explain the broad tree bbox. Do not borrow its 806-focus canvas.

Coordinate style in `00_generic.txt` is similarly anchor-first. `GENERIC_political_reform` at (-7,0) is a section root; `GENERIC_cabinet_reform` and `GENERIC_strengthen_government` are parallel descendants at (-4,1) and (-2,1) from that root (lines 54-119). `GENERIC_political_games` is (-3,2), and subsequent institutional paths merge with distinct prerequisite blocks: focus entries in one block are OR; separate `prerequisite = { ... }` blocks are AND. Keep that grouping in the layout and generated code. In each resolved tree, every y row between its min and max contains at least one focus. For Brazil, Russia and Generic, the most common nearest same-row center gap is 2 grid units; this is a coordinate statistic, not a visual clearance guarantee.

The Germany party example in `05_germany.txt` lines 18272-18439 provides a native style precedent for visible alternatives: `GER_the_alternative` is a branch root; two children `GER_volk` and `GER_vaterland` use relative offsets -1/+1 at y=1; a later focus has separate prerequisite blocks for those parents, which produces a real AND join. Ruling-party gating is expressed through actual availability triggers such as `nationalist_right_wing_populists_are_in_power = yes`, rather than hiding focus cards through coordinates. Its branch costs are 4.3 at entry and 6.5 in these policy cards.

## Cost, reward and navigation conventions

| Tree | Most common costs | Other cost tiers |
| --- | --- | --- |
| Brazil | 5 (186 focuses) | 10 (58), 6.8 (21), 6.4 (11), 7.2 (9) |
| Russia | 3 (314) | 5 (216), 7 (168), 2 (76) |
| Generic | 10 (103) | 7.86 (29), 8.6 (10), 5 (9) |

Native focus cost uses the standard seven days per cost unit. Thus Brazil cost 5 is 35 days, Russia cost 3 is 21 days, Generic cost 10 is 70 days; decimal costs produce corresponding fractional-day nominal values and should be checked against the game's display. For an economical country tree, Brazil's common 5/35-day entry is a closer source profile than Soviet/Superpower reward budgets. Sample source code: Generic `GENERIC_political_reform` (line 54, cost 8.6) trades one 200 PP reward; `GENERIC_cabinet_reform` (line 80, same cost) gives 150 PP; `GENERIC_strengthen_government` (line 109) awards a named political-power idea. The sources show reward specificity and branch economy, not a requirement to copy PP payouts.

Brazil defines five topical focus shortcuts in `05_brazil.txt` lines 18-40 and a continuous-focus panel at `{x=0 y=1500}`; it has no explicit `initial_show_position`. Russia sets `initial_show_position = { x = 2 y = 0 }` at line 13 and six shortcuts at lines 20-46. These establish that opening camera and shortcut count are design choices; use only the number of shortcuts needed to reach actual programme clusters. None of the reviewed Brazil/Russia/Generic focus files uses a `title` field for sections. Section hierarchy is encoded by root anchors, names, connectors and ordinary focus localization, not custom titlebar rows. The native titlebar is the card-state background: `00_titlebar_styles.txt` defines the default mapping unavailable/completed/available/current to `GFX_focus_unavailable`, `GFX_focus_completed`, `GFX_focus_can_start` and `GFX_focus_current`; `nationalfocusview.gfx` provides the state textures and animated current/completed treatment. Keep the default style for ordinary domestic focuses unless a genuinely shared/joint focus needs an existing specialized style.

## Card and interface measurements

In `interface/nationalfocusview.gui`, the native `national_focus_item` container starts at line 536 and is 165x128, with clipping disabled. The background uses `GFX_technology_unavailable_item_bg` at x=5,y=40; the centered symbol control is at x=5,y=-44 and defaults to `GFX_goal_unknown`. A checked Brazil source focus art (`BRA_the_2018_elections`) is 100x88 from its registered DDS source. The title is `hoi_16mbs`, centered in a 147x20 field at x=15,y=58, vertical-centered. The adjacent continuous focus item is 80x124, icon center x=40,y=-18, title field 145x20. Use the native card/name/icon treatment and verify title fit at standard scale; don't replace cards with broad rectangles or resize shared GUI. The grid view uses a `gridboxtype` with 1x1 slots, but that alone does not expose the focus-coordinate pixel conversion; the layout skill's 96x130 native grid figure is a separate measured installation reference. Treat connector routes, scaled title fit and apparent card gap as requiring native-game/faithful-preview review.

## Brazil 1970 party and leader baseline

Project history sets Médici as the January 1970 country leader and `ruling_party = 22` (military command), with party popularity 60% at history lines 394-419. The 1970 party registry note explicitly distinguishes military rulers from civilian ARENA: slot 22 is the Brazilian Armed Forces; slot 1 is ARENA; coalition slot 13 is Delfim Netto's technocrats. Other directly relevant current slots include MDB 2, historical/exile PTB 3, PCB 4, ALN 5, PCdoB 19, Lacerdists 20, CNBB 14 and FIESP 15. Do not equate the armed forces with ARENA, or treat the military slot as a free alternative for a later elected party.

Later party labels should remain provisional and timeline-aware: ARENA became PDS in 1979; MDB took the PMDB name in 1980; PDT and PT are separate later formations, not synonyms for the exiled 1970 PTB; PFL split from PDS in 1985. The existing registry slots are already allocated to historically described institutions/parties. Any separate live representation of later formations needs an explicit registry/design decision; this reference audit did not revise or repurpose slots.

## Use as layout grammar

For a compact 1970 programme, borrow the anchor hierarchy and economy of `00_generic.txt`, the policy-root/parallel-subbranch grammar of Brazil, and the explicit party-gate/AND-join grammar of the German party example. A practical starting pattern is: a stable political entry/root; named party routes beneath it; local alternatives on modest symmetric offsets; one- or two-row vertical spacing for forks and merges; thematic economy, defence and diplomacy roots placed as separate clusters; one AND join only when both inputs are substantively required. Check child subtree bounds and the native title field, not just center-point distances. Avoid adopting Russia's 806-focus width, Brazil's modern branch spread, superpower rewards, or a new global GUI style.

## Limits

This audit measured code coordinates and GUI declarations and sampled relevant party history. It did not render all trees or icons, evaluate every conditional trigger in a running game, measure actual camera pixel conversion, inspect title fit image-by-image, or verify native connector routing. The output is a quantified source reference, not visual QA for a proposed Brazil 1970 design.
