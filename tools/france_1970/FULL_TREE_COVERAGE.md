IMPERIA COLD WAR — France 1970 full-tree coverage audit

## Result

No missing node, group, modifier contribution, one-time reward, research transition, prerequisite, or exclusion was found between the approved revision 4 concept, its visual preview, and the installed France 1970 focus tree/effect helpers. Static checks pass. No HOI4 engine load was performed.

## Coverage counts

The visual source `coldwar_france_politics/COLDWAR_FRA_POLITICS_CONCEPT.json` is structurally identical to `tools/france_1970/approved_design.json`. The `ef-data` payload embedded in `coldwar-france-politics.html` has the same 234 focus IDs and matches the concept on all player-visible focus fields checked: title, coordinates, group/domain, modifier deltas, one-time grants, transitions, duration, cost, prerequisites and exclusions. Its labels, starting spirits, revision notes, offers, offer rules, technology targets, and all 13 group IDs also match. The visible group/domain split is 9 institutions plus 225 political focuses across 12 governments; domains are 34 politics, 80 economy, 96 military, and 24 foreign-policy focuses.

Every one of the 234 concept IDs exists in the installed tree and has an `COLDWAR_FRA_apply_<key>` helper. Across the tree, the approved effects comprise 492 modifier entries over 37 distinct modifier keys, 35 technology bonuses, 17 experience grants, one other one-time grant, and 25 spirit transitions. The 35 research bonuses use 35 target variants; required project gates cover five armoured-vehicle, three aircraft, and two naval-vessel design cases. The tree has 288 prerequisite references in 221 focus nodes, including 65 two-way OR rows and one three-way OR row; 79 reciprocal mutual-exclusion pairs; and 24 focus-linked offers.

## Installed-source checks

`tools/france_1970/validate.py` reports 10,347 checks, all 234 focus IDs, 13 programme modifiers, 79 exclusion pairs, 996 compatible routes, and no issues. It verifies modifier preview and runtime sums against the concept, every focus helper’s PP and ordinary one-time costs, research rewards and project gates, position, duration, prerequisites, exclusions, and registered dynamic-modifier bindings. `tools/france_1970/test_programmes.py` passes 22,449 emitted-source model checks over both DLC configurations and all 996 compatible routes, including once-only behavior, research gates, and spirit transitions. The offers source model passes 720 checks across 16 compacts and eight sanction directions per compact.

## France tree routing

The France 1970 country history block loads `COLDWAR_FRA_1970_focus` directly and initializes it under `IMP_is_1970_scenario` (`history/countries/FRA - France.txt:47-50`). The tree’s France/1970 country weight adds 30, above the installed MD France tree’s France weight of 20 (`common/national_focus/COLDWAR_FRA_1970_focus.txt:6`; installed MD `common/national_focus/05_france.txt`). The shared fallback dispatcher routes an original-tag FRA country to this tree and initializes it if it lacks it, then exempts 1970 FRA from the generic-tree branch (`common/scripted_effects/mdcw_1970_focus_tree_effects.txt:16-24, 34-51`). Searches found no other France-specific `load_focus_tree` assignment. The France daily initializer only refreshes programme state; it does not load the generic tree. Existing event calls to the fallback dispatcher therefore preserve the authored France tree once loaded.

This audit compares sources and source-model checks. It does not certify runtime event ordering, focus cancellation semantics, DLC behavior in the engine, or rendered GUI legibility.
