# MD layout and style reference for a DPRK 1970 concept

Scope: reference profile for the proposed DPRK 1970 tree. This file records geometry and syntax only; it does not authorize or implement loaded game content.

## Sources and measurement method

- Donor: Millennium Dawn workshop install `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2777392649`, `descriptor.mod` version `2.0.2`, supported HOI4 `1.19.*`.
- Donor files read: `common/national_focus/05_north_korea.txt` (9,849 lines), `05_russia.txt` (37,174 lines; full focus blocks extracted), `00_generic.txt` (6,456 lines), `interface/nationalfocusview.gui`, `interface/nationalfocusview.gfx`, and `interface/goals.gfx`.
- Target comparison: `C:\Users\sonyz\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar-main\common\national_focus\05_north_korea.txt` and `common/national_focus/COLDWAR_SOV_1970_focus.txt`.
- A read-only parser extracted top-level focus blocks, recursively summed `relative_position_id` offsets, and counted costs. All focus anchors resolved in these four files. The measurements below describe source coordinates; the game renderer was not run.

## Geometry profile

| Tree | Focus count | Resolved x/y bounds | Cost in focus points | Typical local offsets |
|---|---:|---|---|---|
| Donor DPRK | 233 | x -27..99, y 0..13 | min 1, median 5, max 10 | Frequent child offsets: (0,1), (±1,1), (0,2), then ±2 columns for wider forks |
| Donor Russia | 806 | x 0..235, y 0..26 | min 1, median 3, max 10 | Frequent child offsets: (0,1..4), (±1,1..3), (±2,1..4) |
| Donor Generic | 158 | x -13..51, y 0..10 | min 2, median/max 10 | More deliberate open branching; long offsets occur at domain boundaries |
| Target Soviet 1970 | 836 | x 0..426, y 0..18 | min 1, median 5, max 10 | Cluster anchors with local fans; intentional 2-column subtree spacing, 4-column major-block spacing |

The standard focus duration is 7 days per focus point: 5 points is 35 days, 7.2 is about 50 days, and 10 is 70 days. DPRK's observed median is 5; Russia's post-2000 tree uses shorter median focuses at 3. Use DPRK/Soviet timing as the closer setting analogue for a 1970 programme.

### DPRK sample positions and patterns

Values below are resolved absolute grid coordinates. Local values in code remain offsets from the named anchor.

| Donor focus | Source lines | Local placement | Resolved | Cost / sprite | Style observation |
|---|---:|---|---:|---|---|
| `NKO_solve_the_arduous_march` | `05_north_korea.txt:41-65` | root `(-5,0)` | (-5,0) | 5 / `NKO_korea_rebuild` | Stable section root; several parallel economy and social-policy limbs anchor to it. |
| `NKO_promote_songun` | `:69-106` | +2,0 from root | (-3,0) | 5 / `dprk_army` | Same-row parallel choice, feasible because roots and whole subtree are far apart. |
| `NKO_humanitarian_aid` | `:109-156` | -1,+1 from root | (-6,1) | 5 / `economic_un_money` | First row fans one column left of the root. |
| `NKO_food_production_boost` | `:160-192` | +1,+1 from root | (-4,1) | 5 / `NKO_food` | Paired first-row fork at one-column offsets; do not copy this spacing where long titles or adjacent subtrees need more room. |
| `NKO_admit_the_donju` | `:572-593` | -3,+5 from root | (-8,5) | 5 / `donju` | A later institutional branch remains tied to the same stable economy anchor. |
| `NKO_huichon` | `:597-629` | +2,+4 from root | (-3,4) | 7.2 / `NKO_huichon` | Project sub-tree gets its own anchor. |
| `NKO_huichon_hydroelectric_power` | `:633-663` | -3,+1 from Huichon | (-6,5) | 7.2 / `Hydro_sheep` | Left branch. |
| `NKO_huichon_silk_mill` | `:667-723` | -1,+1 from Huichon | (-4,5) | 7.2 / `economic_silk_factory` | Paired project branch. |
| `NKO_struggle_for_power` | `:4898-4949` | root `(86,0)` | (86,0) | 5 / `kim_il_sung` | Separate political cluster, with a conditional offset for a completed junta path. |
| `NKO_orthodox_successor` | `:4951-5011` | +11,+1 from political root, with a conditional -7 x offset | (97,1) normally; (90,1) in its HIDE state | 5 / `NKO_kim_boom` | Visible branch choice, `allow_branch` visibility, prerequisites, MEX choice, and government/leader availability are separate fields. |
| `NKO_focus_on_the_f_35` | `:4224-4295` | -2,+2 from `NKO_defend_our_skies`, conditional +2 x offset | conditional | 5 / `f35` | Uses `allow_branch` and MEX to manage visible aircraft alternatives, plus a real `available` gate for ROK completion. |

The donor's sections are spaced widely: economy starts at x=-5, armed forces at x=39 (`NKO_national_defence_force`, line 2639), parallel/reunification at x=55 (`NKO_the_38th_parallel`, line 8800), and domestic succession at x=86. This yields 126 grid columns across despite only 233 focuses. It demonstrates deliberate section reservations, not a compactness target. DPRK 1970 should use a few legible section anchors and reserve each branch's full descendants; a target around the donor's 126-column span would be excessive for the proposed 170-180 foci.

### Russia and Soviet 1970 comparison

- The donor Russia tree's opening anchors are `SOV_reign_of_yeltsin` at (62,0), line 51, and `SOV_putin` at (75,1), line 108, using a 13-column jump for separate regime-era material. Its 806-focus size and median cost 3 belong to post-Soviet content; use its join and branch syntax, not that scale or timeline.
- A concrete Russia join is `SOV_a_just_system`, line 27628: three separate `prerequisite` groups require `SOV_empower_legislature`, `SOV_defend_people`, and `SOV_social_gurantees`. Three groups mean all three; multiple `focus =` entries inside one prerequisite block mean any listed focus.
- The target 1970 tree opens at `COLDWAR_SOV_the_collective_leadership` (93,0), line 81; its second institutional cluster starts at `COLDWAR_SOV_em_the_party_of_a_new_type` (89,5), line 617. The first fan has 2- and 3-column local offsets; four outlook paths spread broadly to x=8..94. The full tree resolves to x=0..426/y=0..18, driven by its 836-focus programme and shared/joint content. Its `initial_show_position` and shortcut setup are at lines 20-41.
- The project layout method in `Claude outputs/COLDWAR_SOV_generator/cw_layout.py` states `GAP = 2`, `BLOCK_GAP = 4`, `OUTLOOK_GAP = 4` (near lines 190-193). Treat these as tested project construction choices for a wide multi-domain tree, not engine constants. For the DPRK concept, pairs with 2-column separation and major domains around 4 columns apart are a sound starting measure; use 1-row descents for simple progressions and 2-row steps around forks, joins or text-heavy areas. NKO donor examples prove that 1-column sibling spacing exists, while the GUI's 165px item width warns that this can look crowded.

## Native syntax, visibility and connectors

- Focus declaration convention is `focus = { id = ... x = ... y = ... [relative_position_id = ...] }`. An anchored child emits a local delta, e.g. `NKO_promote_songun` is `x = 2, y = 0` relative to `NKO_solve_the_arduous_march`, not absolute (-3,0).
- Separate `prerequisite = { ... }` blocks combine with AND. Multiple `focus` entries within one block form OR. The donor uses repeated one-focus blocks for joins (see `NKO_food_production_boost` and the agricultural follow-ups around lines 160-380; Russia join above).
- `mutually_exclusive = { focus = X }` is the native MEX form. Repeat it for each alternative, or group several `focus` entries where the alternatives are a set. Example: F-35 at `05_north_korea.txt:4258-4259` excludes the F-16 and future KAI/KF-21 branches. MEX blocks encode completion exclusion; they do not hide losing cards or replace availability checks.
- `allow_branch = { ... }` is a conditional branch-visibility rule in donor NKO. The file contains 20 such blocks, including the aircraft choice (line 4244) and successor route (around line 4968); these use the `obsolete_focus_branches_visibility = HIDE` game rule with completed-focus tests. Treat this as card visibility behavior; keep actual party, leader, membership and date/runtime requirements in `available` and reward guards. NKO `NKO_struggle_for_power` around lines 4899-4949 shows explicit communist-government and Kim Jong-il availability. Its conditional `offset` around lines 4904-4912 relocates the political root after a junta path; offsets are layout state, so review both states.
- `offset = { x = ... y = ... trigger = { ... } }` is additional condition-dependent placement. Resolve each state separately and inspect the full subtree in each state. NKO's F-35 offset is lines 4229-4241; its political root offset is lines 4904-4912.
- A visible connector comes from `prerequisite`; `available` adds a gameplay gate without a line. `mutually_exclusive` prevents selecting an alternative after completion but does not hide it. Keep those semantics distinct in a generated concept.
- Standard durations are not explicit on every focus. Donor cost declarations sit near each focus header; no extra `days` field is required for ordinary focus time.

## Focus card UI and style

In donor `interface/nationalfocusview.gui`, `national_focus_item` is a 165x128 container (lines 446-449); the title textbox is at (15,58), uses `hoi_16mbs`, and has maxWidth 147/maxHeight 20 (lines 488-496). The icon button/symbol is centered in the item around its top art area (lines 467-478). This explains why one-column sibling separation can crowd and why the concept should reserve room for title length, icon bounds, and adjacent rows. The active layout grid uses a `slotsize` of 1x1 at lines 133-140; focus-grid screen pitch is not defined by that UI snippet itself, so do not infer a pixel-per-focus conversion from it. Focus link sprites use dedicated directional textures in `nationalfocusview.gfx` around lines 39-100. No game render or precise engine connector-route check was performed.

Native style keeps the actual subject or institution in the title and icon, allows major policy sections to fan into several policy instruments, and brings related inputs back together through prerequisite joins. `search_filters` aid navigation but do not form in-tree labels. The NKO focus tree declares economy, military, parallel, and political shortcuts at file lines 20-39. The Soviet 1970 tree declares 11 navigation shortcuts and an initial start position; this is useful for a wide tree, not a target count.

## Reusable icon sprite / texture candidates

Sprite registrations were checked in donor `interface/goals.gfx`; textures are relative to the donor root. Names identify candidate subjects, but textures were not visually previewed here. Keep icons consistent in visual weight and avoid repeating the leader portrait for every institutional focus.

| Use | Sprite | Texture |
|---|---|---|
| Kim Il-sung / leadership | `kim_il_sung` | `gfx/interface/goals/north_korea/kim_il_sung.dds` |
| Juche / self-reliance | `juche` | `gfx/interface/goals/north_korea/juche.dds` |
| Juche / national doctrine | `juche3` | `gfx/interface/goals/north_korea/juche3.dds` |
| Juche / state programme | `juche4` | `gfx/interface/goals/north_korea/juche4.dds` |
| WPK / party organization | `WPRG` | `gfx/interface/goals/north_korea/WPRG.dds` |
| Party reform | `NKO_party_reform` | `gfx/interface/goals/north_korea/NKO_party_reform.dds` |
| Inter-Korean front / 38th parallel | `NKO_38_parallel` | `gfx/interface/goals/north_korea/NKO_38_parallel.dds` |
| Anti-corruption | `NKO_anti_corruption` | `gfx/interface/goals/north_korea/NKO_anti_corruption.dds` |
| Agriculture / food | `NKO_food` | `gfx/interface/goals/north_korea/NKO_food.dds` |
| General agriculture | `agriculture` | `gfx/interface/goals/00_economy/agriculture/agriculture.dds` |
| Huichon / power and industry | `NKO_huichon` | `gfx/interface/goals/north_korea/NKO_huichon.dds` |
| Civil industry | `economic_civil_industry` | `gfx/interface/goals/00_economy/economic_civil_industry.dds` |
| Armed forces | `dprk_army` | `gfx/interface/goals/north_korea/dprk_army.dds` |
| Defence | `NKO_defence` | `gfx/interface/goals/north_korea/NKO_defence.dds` |
| China relations | `align_to_china` | `gfx/interface/goals/00_align/align_to_china.dds` |
| Soviet/Russian relations | `align_to_russia` | `gfx/interface/goals/00_align/align_to_russia.dds` |
| Nuclear programme | `NKO_nuclear` | `gfx/interface/goals/north_korea/NKO_nuclear.dds` |
| Missile testing | `NKO_rocket_test` | `gfx/interface/goals/north_korea/NKO_rocket_test.dds` |
| State atheism (generic candidate) | `focus_ARG_state_atheism` | `gfx/interface/goals/00_religion/focus_ARG_state_atheism.dds` |

The religion illustration is Argentina-named and may be country-coded art; only reuse it if visual inspection confirms it reads as a generic state-atheism symbol. The native NKO focus set contains no dedicated religious-policy symbol. If none fits, use an appropriate general icon or create a DPRK-specific asset after visual review.

## Actionable profile for the DPRK concept

1. Organize the proposed 170-180 focuses into compact stable roots for political authority, the planned economy, social policy, armed forces, foreign policy and nuclear policy. Conditional subprogrammes should branch from their real party/institution gates, not a cosmetic unlock chain.
2. Use relative anchors for local branches. Start with 2 columns between paired subtree footprints, 4 between major domains, and 1-2 rows for ordinary progress; increase where fan-out, title length or joins require it. Reserve complete descendant widths before placing neighbors.
3. Preserve the semantic distinction between connector requirements, hidden eligibility, branch visibility, MEX and conditional offsets. With eight party/institution variants, report the full simultaneous visibility states and re-evaluate shifted subtrees.
4. Set initial view and shortcuts to expose the governing programme and the main alternatives. The native tree's initial viewport and scroll behavior cannot be proven from coordinates alone.
5. The economic, military and diplomatic subject may follow NKO icon conventions, but the whole 2000s NKO tree is not a political or historical template for January 1970. The Soviet 1970 tree is the project precedent for depth and multi-domain policy clusters; adapt organization, not its vast breadth or Soviet institutions.

## Unverified

No in-game render, title/localization review, icon pixel preview, engine connector routing, or full conditional-state screenshot was produced. The coordinates are statically resolved from source. The target's `05_north_korea.txt` was inspected as the current baseline, and the donor `05_north_korea.txt` supplied comparable native patterns; no files in the loaded focus tree were edited.
