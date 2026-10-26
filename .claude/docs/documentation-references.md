# Documentation References

Start with `coldwar-1970-context.md`. Every other doc below was written for current
upstream Millennium Dawn (2000 start); verify what it names against this 2.0.2-based
1970 tree before relying on it.

## Engine Documentation (HOI4 install `documentation/`)

This repository does not carry a copy. The authoritative lists for the installed game
version (1.19.x) are in the HOI4 install folder, for example
`<Steam>/steamapps/common/Hearts of Iron IV/documentation/`. Ask the user for the path
or for the file when you need to confirm an effect, trigger or modifier exists. An
upstream MD claim that something is valid is not proof for this game version.

| File                                 | Contents                                                |
| ------------------------------------ | ------------------------------------------------------- |
| `effects_documentation.md`           | All effects by scope (COUNTRY, STATE, CHARACTER, …)     |
| `triggers_documentation.md`          | All triggers by scope                                   |
| `modifiers_documentation.md`         | All modifiers by category (army, navy, country, …)      |
| `dynamic_variables_documentation.md` | Read-only dynamic variables by scope                    |
| `loc_formatter_documentation.md`     | Localization formatters (`idea_desc`, `tech_effect`, …) |
| `loc_objects_documentation.md`       | Localization scope objects and their properties         |
| `script_collection_input.md`         | Collection inputs (`game:all_countries`, …)             |
| `script_collection_operator.md`      | Collection operators (`faction_members`, `limit`, …)    |
| `script_concept_documentation.md`    | Bindable/formatted loc, collections, script constants   |
| `script_math_functions.md`           | Math functions for `value = { ... }` expressions        |
| `console_commands_documentation.md`  | Console commands and tweakable variables                |

## External Wiki References

Use for broader modding context not covered in local docs:

- [Focus Tree Modding](https://hoi4.paradoxwikis.com/National_focus_modding)
- [Decision Modding](https://hoi4.paradoxwikis.com/Decision_modding)
- [Event Modding](https://hoi4.paradoxwikis.com/Event_modding)
- [Idea Modding](https://hoi4.paradoxwikis.com/Idea_modding)
- [Scopes](https://hoi4.paradoxwikis.com/Scopes)
- [On Actions](https://hoi4.paradoxwikis.com/On_actions)
- [AI Modding](https://hoi4.paradoxwikis.com/AI_modding)
- [Scripted GUI](https://hoi4.paradoxwikis.com/Scripted_GUI_modding)
- [Technology Modding](https://hoi4.paradoxwikis.com/Technology_modding)
- [Equipment Modding](https://hoi4.paradoxwikis.com/Equipment_modding)
- [MIO Modding](https://hoi4.paradoxwikis.com/Military_industrial_organization_modding)
- [Unit Modding](https://hoi4.paradoxwikis.com/Unit_modding)
- [Faction Modding](https://hoi4.paradoxwikis.com/Faction_modding)

## Conventions in this repository

Keep `AGENTS.md` and agent prompts to guardrails and task-based reading pointers.
Implementation details belong in the existing reference for that domain. Country design
records, integration contracts and acceptance matrices belong in
`docs/<country>_1970_design/` or `docs/<country>_1970/`, next to the work they describe.
Upstream MD's player and contributor site (`docs/src/content/`) does not exist here.

Docs hold rules, shapes, and traps. Open backlogs, finding counts, and change history
go in GitHub issues and commit messages, not in a doc. Do not copy inventories the
script files already hold, and do not cite line numbers.

Write the answer or action first where useful. Keep prose terse and tables readable
in plaintext: pad columns and keep each whole padded row within about 100 characters.
Shorten cells or use a list instead of a wide table.

### Naming Scheme

Most filenames end in one of four suffixes: `-reference` (structure or valid-key lookup), `-rules` (must-follow conventions), `-patterns` (recipe/refactor catalogs), or `-system` (subsystem architecture). A few docs use a plain descriptive name when none of those fit.

All files below live in `.claude/docs/`.

| File                             | Contents                                                     |
| -------------------------------- | ------------------------------------------------------------ |
| `coldwar-1970-context.md`        | This fork: 1970 start, gates, naming, absent upstream tools  |
| `agent-conventions.md`           | Agent roles: task reading, boundaries, BLUF handoffs         |
| `ai-equipment-reference.md`      | AI equipment variants: role templates, coverage errors       |
| `ai-strategy-reference.md`       | Unit production: 5 layers, on_action entries, plan files     |
| `bug-patterns.md`                | Known bug patterns: scan signatures, diff-review questions   |
| `content-guidelines.md`          | Content checklist: economic, political, military, visual, AI |
| `counter-terrorism-reference.md` | CT slots, lifecycle, country coverage, cadence, recipients   |
| `debug-commands.md`              | Console recipes for testing MD systems (EU/USoE focus)       |
| `decision-reference.md`          | Decision structure, targeted-decision perf, examples         |
| `diplomatic-action-reference.md` | Scripted diplomatic actions: files, ROOT/THIS/PREV scopes    |
| `dynamic-modifier-tooltips.md`   | `adds_` vs `modifies_dynamic_modifier_tt` tooltips           |
| `energy-power-balance.md`        | Power-per-cost + tech S-curves; read before energy edits     |
| `entity-system.md`               | Mesh→entity→animation chain, pdxmesh naming, landmarks       |
| `event-reference.md`             | Event types, TT*IF*\* tooltips, `random_events` dispatch     |
| `faction-rules.md`               | `common/factions/rules/`: rule types and trigger scopes      |
| `focus-tree-reference.md`        | Focus structure, property order, bankruptcy-guard examples   |
| `formable-reference.md`          | Formable paths, AI ratchet, sentinel, cross-guards, traps    |
| `hoi4-data-structures.md`        | Variables, arrays, loops, collections, formatted loc         |
| `idea-reference.md`              | Idea structure: pictures, tiered naming, `name =` gotchas    |
| `known-false-positives.md`       | Intentional bug-lookalikes; review agents must skip them     |
| `loading-screen-system.md`       | Loading rotation vs menu picker, `GFX_<x>_small`, generator  |
| `loc-smoke-checklist.md`         | In-game checks for dynamic loc that tests cannot prove       |
| `localisation-rules.md`          | English `.yml` rules: BOM, file naming, key formatting       |
| `md-custom-modifiers.md`         | Where custom modifier keys live; faction opinion keys        |
| `meta-effect-patterns.md`        | `meta_effect`/`meta_trigger` dispatch; `[!]` tooltips        |
| `mio-reference.md`               | MIO structure, per-block modifier keys, trait-grid rules     |
| `music-system.md`                | Stations, playlists, chance weights, radio GUI wiring        |
| `namelist-reference.md`          | Division/ship name-list files and mandatory groups           |
| `oob-variants-reference.md`      | OOB files, variants, type systems, slot and tech rules       |
| `party-loc-reference.md`         | Politics-view party keys, subideology slots, loc hooks       |
| `performance-patterns.md`        | Hoisting, dirty counters, clamp-before-divide, early-outs    |
| `refactor-checklist.md`          | Rename/migration sweeps: namespaces, GUI/GFX refs, tags      |
| `scripted-gui-patterns.md`       | `dynamic_lists`, loc dispatchers, dirty-var standard         |
| `scripted-gui-rules.md`          | scripted_gui mechanics: structure, dirty-var perf, AI        |
| `scripting-edge-cases.md`        | Niche pitfalls: temp-var defaults, `^index`, vacant office   |
| `search-filters.md`              | Every `FOCUS_FILTER_*`, Israel subcats, common mistakes      |
| `simplification-patterns.md`     | Lookups→arrays, parameterized loc, shared helpers            |
| `sound-system.md`                | Sound defs, combat sounds, voicelines, compressors           |
| `typo-watchlist.md`              | Recurring localisation typos to check in review              |
| `un-system-reference.md`         | UN votes/elections: invariants, new-resolution recipe        |
| `validation-pipeline.md`         | Static checker, reference trace, country tools, engine/MP    |
