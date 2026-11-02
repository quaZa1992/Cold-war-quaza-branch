# IMPERIA COLD WAR - MD France and Russia reference profile

## Scope and source snapshot

This is a code and coordinate profile for a Chile January 1970 to 1990 concept. It does not change loaded mod content. The donor is the installed Millennium Dawn workshop tree at `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\3374271790`, especially `common/national_focus/05_france.txt` and `common/national_focus/05_russia.txt`. The donor descriptor reports MD `2.0.4` (`descriptor.mod:1` in the workshop directory). The project descriptor independently reports `2.0.3`. The focus files contain legacy `IMPERIA CW` comments and are treated as upstream examples, not project-authored files.

## Geometry and structure

Coordinates below resolve each focus's `relative_position_id` recursively by adding local `x/y` to its anchor. The count covers focus blocks with a resolvable position. Coordinates are focus-grid units, not pixels.

| Tree | Focuses | Resolved span | Typical structure |
|---|---:|---|---|
| France | 381 | x 2 to 194, y 0 to 9 | Broad political entry row, then party-specific programmes with repeated short policy chains and several joins |
| Russia | 806 | x 0 to 235, y 0 to 26 | Many party or leader programme clusters with short spines, adjacent alternatives and local joins |

France puts `FRA_state_of_french_politics` at (68,0), then fans eight party focuses out along one row at relative x values -45, -32, -21, -10, 0, 10, 21 and 32, all y=1 (`05_france.txt:33-40,58-400`). The opening political card costs 2; the party cards cost 1. The broad row deliberately keeps the party alternatives visible and inspectable. France also declares four topic shortcuts for politics, diplomacy, economy and military near the top (`05_france.txt:10-29`).

Russia starts `SOV_reign_of_yeltsin` at (62,0), gives it six topic or leader shortcuts, and opens several distinct branches immediately (`05_russia.txt:16-46,48-64`). Its Putin programme anchors repeated offsets to `SOV_putin`: near neighbors at x=-2, 0 and +2, followed by branches extending downward in rows (`05_russia.txt:155-220,278-431`). Its overall footprint is larger and deeper than France's; the extra area is the consequence of more parallel programmes, not a standard size to copy for Chile.

Both trees reuse stable focus anchors instead of repeating absolute coordinates. Same-row siblings are often 2 grid units apart in these examples; 2-unit x steps are the observed tight pattern, not a universal spacing rule. The France fan uses wider intervals because all eight political choices share the opening row. Put a Chile fork around a coherent section root, then reserve each full downstream branch footprint before placing a neighboring section.

## Native focus UI measurements

The installed `interface/nationalfocusview.gui` sets `focus_spacing` to 96 by 130 and the focus item container to 165 by 128, with the title field at x=15, y=58 and 147 by 20 max bounds, using `hoi_16mbs` (`nationalfocusview.gui:536-588,664-690`). The 1x1 grid slots are declared at lines 137-142. Focus cards therefore extend beyond a single grid interval; do not judge collision risk from focus centers alone. The generic focus background is positioned at x=5, y=40 within the item, while the focus icon button sits at x=5, y=-44 (`nationalfocusview.gui:553-565`). These are this installation's actual UI values.

The same GUI keeps the grid clipped to the scrolling tree viewport (`nationalfocusview.gui:73-86,133-142`) and defines visible focus title states in the native GFX (`interface/nationalfocusview.gfx:75-91`). Keep a Chile initial view on the opening political decision point, and add a small number of useful shortcuts only if the final tree's extents merit them. Russia's initial view is a legacy coordinate (`initial_show_position = { x = 2 y = 0 }`, `05_russia.txt:10`); the project's Soviet 1970 implementation instead points directly to its first focus and defines named shortcut groups (`COLDWAR_SOV_1970_focus.txt:15-65`).

## Rewards, costs and code patterns

France's 381 focus costs range from 1 to 30, with most at 5 or 10; Russia's 806 costs range from 1 to 10, with most at 3, 5 or 7. These native focus `cost` values appear as whole focus durations in code, not monetary values. Keep economic monetary costs separate and describe them through the project's native MD economy interface if a Chile concept uses them.

The French opening focus uses direct, concrete effects (`add_political_power = 100`) and then an event (`05_france.txt:44-53`). A socialist-policy branch combines political conditions with a clear chain and party-popularity effects (`05_france.txt:440-527`). Russia's examples include a mixed reward on its entry focus (`add_stability = -0.02`, `add_political_power = 50`, and an event, `05_russia.txt:48-64`), as well as programme effects such as a debt change and external influence adjustments (`05_russia.txt:220-275`). Other Russian nodes apply named dynamic modifiers or rely on an actual mission/event rather than hand-written custom tooltip text (`05_russia.txt:186-217`).

For Chile, borrow the organization and focus grammar: concise economic, institutional and political chains; concrete native rewards; named modifiers or ideas where an ongoing effect is warranted; and joins that do not force mutually exclusive parties into an impossible AND gate. Do not copy the donor's implementation-era comments or verbose hidden mechanics into player-facing localization.

## Chile baseline in this checkout

There is no Chile-specific focus file in `common/national_focus`; the current Chile baseline uses the generic content until a separate concept is implemented. The generic tree's political and diplomacy roots use anchored child positions and its shortcuts point to those roots (`common/national_focus/00_generic.txt:28-54,57-92,1208-1225`).

The 1970 country history sets democratic support to 72%, communism 5%, fascism 2%, neutrality 15%, and nationalist 6%, with democratic government and a 48-month election frequency. The mod's 24-slot party array sets party 1 to 48%, party 2 to 14%, party 3 to 8%, party 14 to 10%, and other smaller shares, with party 1 ruling and party 2 in the government coalition (`history/countries/CHL - Chile.txt:278-301`). Eduardo Frei Montalva is set as the opening leader (`:302-305`). This makes an Allende path a real political alternative, not the starting party. The current native leader-pool routing associates Chilean slot 1 with Eduardo Frei Ruiz-Tagle and slot 3 with Salvador Allende (`common/scripted_effects/mdcw_historical_native_pools.txt:14803-14828`); that mapping conflicts with the 1970 party/leader registry. The concept's proposed correction is PDC/Tomic-Aylwin in slot 1, PS/Allende in slot 18, PR/Baltra in slot 3, and Pinochet in slot 22. Do not preserve the current slot 3 Allende mapping when representing the Chilean 1970 party programmes. Slot 22 should still be guarded by the actual ruling-party checks and leader identity where appropriate (`common/scripted_effects/CHL_political_leaders.txt:2-18`).

## Candidate reusable art

The base MD focus icon aliases already appear in installed focus content and can be reused without adding new textures. For a Chile programme, inspect these at actual focus-icon size before selection:

- `focus_CHL_strengthen_the_central_bank` for monetary institutions (`05_china.txt:18700`, `05_greece.txt:5472`).
- `focus_CHL_high_quality_nitrate` for mining, nitrate or resource policy (`03_china_russia_joint.txt:469`, `05_japan.txt:5850`).
- `focus_CHL_enlarge_the_textile_industries` for manufacturing and labor (`05_iran.txt:1997`, `05_netherlands.txt:24620`).
- `focus_CHL_expand_the_forestry` for regional development or land use (`05_artsakh.txt:385`, `05_Australia.txt:9440`).
- `focus_CHL_focus_on_cattle_and_wool` for agricultural production (`05_chechnya.txt:6223`, `05_greece.txt:3214`).
- `focus_CHL_silverworking` for mining or skilled industry (`05_Australia.txt:9713`, `05_china.txt:20577`).
- `focus_CHL_protect_the_easter_island` for Pacific defense or strategic geography (`05_china.txt:18089`).

These are existing references, not a visual inspection of the textures. Inspect the donor textures in the live focus viewer before approving icons; the name alone does not establish that the motif reads well at the intended size.

## Evidence limits

The tree counts and coordinate spans are parsed from the full installed France and Russia focus files, but they are not a live-game render or an exhaustive connector-collision audit. The repository currently contains no Chile-specific focus geometry to compare. No textures were visually opened in this reference pass. Treat native card and spacing measurements as evidence for layout planning, then check the proposed Chile tree in the actual focus viewer at normal zoom.
