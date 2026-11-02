IMPERIA COLD WAR — France 1970 core review

## Findings

- **Unverified in-engine:** Static layout checks pass, but no HOI4 load or GUI render was performed. The generated tree spans x=2–368 and y=0–7; this is wider than MD France’s current tree (x=2–194), though within the scale of other large MD Cold War trees. Review shortcut navigation and legibility in the running game.

## Review evidence

- The generated tree contains 234 focus IDs matching the approved revision 4 design, with no unresolved prerequisites or exclusions, no duplicate centers, reciprocal exclusivity pairs, and all relative positions resolving to the design coordinates. Bounds and route counts were checked against the emitted graph; `tools/france_1970/VALIDATION.json` reports 7,122 emitted-source checks, 79 exclusive pairs, 996 compatible routes, and no issues.
- The new tree’s country rule gives France in the persistent 1970 scenario priority 30 (`common/national_focus/COLDWAR_FRA_1970_focus.txt:6`). The installed MD France tree gives France priority 20, so the new tree wins under the intended scenario predicate.
- Native forms checked against the installed MD source include `add_tech_bonus`, `is_special_project_completed`, and `force_update_dynamic_modifier`. Each referenced technology exists in the project source. The 1970 research entries gate on at least one unresearched target technology, and design-dependent entries also test the corresponding completed MD special project. Tooltips distinguish the project-gated and project-free cases; the engineer-specific targets are not granted in France’s initial 1970 infantry profile.
- Dynamic-modifier keys and effect forms were compared with MD definitions and usage. The programme refresh clears only the legacy party-programme modifiers, recomputes the active government’s values from earned flags, attaches that government’s programme, removes inactive programme modifiers, and forces an update (`common/scripted_effects/COLDWAR_FRA_1970_effects.txt:4479`). Initialization grants the three starting spirits once and then refreshes (`...effects.txt:6182`). Earned flags and one-time focus costs are not reset by refresh.
- The exact ruling-party checks are visible through player-facing custom trigger tooltips while scenario and country routing remain hidden. Research condition tooltips name relevant technology groups and, where required, the specific completed design programme. Player-facing localisation is English.
- Political-government tooltips use the regenerated neutral label “Governing political current: <name>.” The earlier plural agreement issue is resolved. `tools/france_1970/test_programmes.py` passes 22,389 emitted-source model checks across both DLC configurations, including all 996 compatible government routes; it is an AST source-model check, not a HOI4 engine test.
- The per-country government epoch increment in global government-change callbacks is intentional: pending offers snapshot both the recipient country’s local epoch and France’s epoch. Daily programme refresh provides a fallback for changes made outside the exact-subparty callback.

This is a static source review. It is not a game-load, save migration, offer-flow, or rendered-layout certificate.
