---
name: new-focus
description: 'Scaffold a new 1970 Cold War country focus tree file (COLDWAR_<TAG>_1970_focus.txt) with tree selection gated to the 1970 start, a correctly structured root focus, history wiring, and English localisation stubs. Use when asked to create, start, or scaffold a focus tree for a country, e.g. "/new-focus TUR". Takes the 3-letter TAG.'
---

Scaffold a new focus tree file for a country in the Cold War 1970 fork.

Country TAG (3-letter code): $ARGUMENTS

Read `.claude/docs/coldwar-1970-context.md` and `.claude/docs/focus-tree-reference.md`
first.

Steps:

1. Confirm the TAG is valid (3 uppercase letters, defined in `common/country_tags/`).
   If $ARGUMENTS is empty, ask the user for the TAG.

2. Check what the country loads at 1970 today: the `load_focus_tree` line in the
   `1970.1.1` block of `history/countries/TAG - *.txt`, any existing
   `common/national_focus/COLDWAR_TAG_1970_focus.txt`, and the design notes in
   `docs/<country>_1970*/`. If a 1970 tree or a generator under `tools/<country>_1970/`
   already exists, stop and ask; a generated tree is changed in its generator. Remind
   the user that an approved design comes before coding.

3. Create `common/national_focus/COLDWAR_TAG_1970_focus.txt` (UTF-8 without BOM, tabs)
   with:
   - A `focus_tree` block: `id = COLDWAR_TAG_1970_focus`, `default = no`,
     `reset_on_civilwar = no`, and the 1970-only selection:
     `country = { factor = 0 modifier = { add = 100 original_tag = TAG IMP_is_1970_scenario = yes } }`,
     plus `initial_show_position = { focus = COLDWAR_TAG_1970_start }` and a placeholder
     `continuous_focus_position`.
   - One root focus `COLDWAR_TAG_1970_start` following the property order in
     `focus-tree-reference.md`, with `icon`, `x`/`y`, `cost`, `search_filters` (required),
     `available = { hidden_trigger = { original_tag = TAG IMP_is_1970_scenario = yes } }`,
     `completion_reward` that starts with
     `log = "[GetDateText]: [Root.GetName]: focus COLDWAR_TAG_1970_start"`, and
     `ai_will_do` (required).
   - Script ids capitalised and namespaced: `COLDWAR_TAG_1970_<name>`.
   - `relative_position_id` on every focus after the root.
   - Commented-out optional blocks (allow_branch, prerequisite, mutually_exclusive,
     bypass, cancel, select_effect, bypass_effect) as scaffolding hints; remind the user
     to remove any that stay empty.
   - Omit default values: `cancel_if_invalid = yes`, `continue_if_invalid = no`,
     `available_if_capitulated = no`.

4. Wire selection in history: inside the `1970.1.1` block's `date < 1985.1.1` guard in
   `history/countries/TAG - *.txt`, add `load_focus_tree = COLDWAR_TAG_1970_focus`
   (replace an existing 1970 `load_focus_tree`, never the dormant `2000.1.1` block).

5. Create `localisation/english/COLDWAR_TAG_focus_l_english.yml` (UTF-8 **with** BOM,
   `l_english:` header, one-space indent) with `COLDWAR_TAG_1970_start`,
   `COLDWAR_TAG_1970_start_desc`, and the tree's shortcut names if any. English only;
   no other language file.

6. Run the static checker on the three files (`.claude/docs/validation-pipeline.md`).

7. Remind the user of next steps:
   - Real icon instead of the placeholder (`GFX_COLDWAR_TAG_1970_*` sprites in a
     namespaced `.gfx`).
   - `continuous_focus_position` after the layout settles.
   - Any branch that affects another country needs a proposal/response path and a
     two-client acceptance matrix (`AGENTS.md`).
   - Then `/lifecycle-check TAG` for ideas, decisions, history, characters, namelists,
     AI and localisation.
