---
name: content-review
description: "Check a file or the branch diff against the content checklist for the Cold War 1970 RP multiplayer mod (economic, political, visual, military, AI, code, multiplayer agency, 1970 fit) with blocker tags. Use when asked to content-review country content or verify content-guideline compliance before merge."
---

**Syntax:** `/content-review [file_path]`. With a path, review that file. Without one,
review every file the branch changes against `origin/main`.

## 1. Gather context

- File mode: read the file and identify its type.
- Branch mode: `git diff origin/main...HEAD` and `git log origin/main..HEAD --oneline`.

Read `.claude/docs/content-guidelines.md` (the checklist) and
`.claude/docs/coldwar-1970-context.md` (1970 rules). Read the country's design notes in
`docs/<country>_1970*/` when they exist: the review checks the content against its
approved design, not only against general rules. Upstream MD's full content review guide
is online only and assumes a 2000 start; use it as background.

## 2. Apply the checklist

Check each file against the categories in `content-guidelines.md`. Skip categories that
do not apply to the file type.

For a focus tree, run the Variety check as a comparison against the finished 1970 trees
(`COLDWAR_GER_1970_focus.txt`, `COLDWAR_ICE_1970_focus.txt`), not in isolation.

Sweep the whole file for these. Sampling undercounts them:

- Treasury double-charge. The scripted building effects (`one_random_arms_factory`,
  `two_random_*`, `one_office_construction`, and the rest in
  `common/scripted_effects/`) charge treasury themselves unless
  `set_temp_variable = { skip_payment = 1 }` is set first. A focus that calls one and
  also adds an explicit `treasury_change` with `modify_treasury_effect` pays twice. A
  raw `add_building_construction` with one explicit charge is correct.
- Referenced loc keys. Check that every `tooltip = <key>`, idea key, and modifier `_tt`
  key the tree references resolves in `localisation/english/`, not only the keys the
  diff adds.
- Dynamic-modifier first add. An `add_dynamic_modifier` without a
  `NOT = { has_dynamic_modifier = { modifier = X } }` guard double-applies when another
  focus reachable in the same branch adds the same modifier.
- 1970 fit. People, parties, organisations, equipment, technology and place names that
  did not exist on 1 January 1970 appear only behind the gate that creates them. No text
  written from a 2000 viewpoint.
- Human agency. Any effect on another country that a human may run: is there a
  proposal or event with refuse, a deadline, a visible default, and a cost shown before
  the click? Forced war, annexation, government change or irreversible loss without
  consent is a `[blocker]` unless a documented house rule allows it.
- Gates. New content reachable at 1970 (`IMP_is_1970_scenario` where the selection
  needs it) and not reachable through dormant 2000-era MD content.

## 3. Output

Per file: the path and type, then a numbered issue list with category labels
(`[Economic]`, `[Political]`, `[Visual]`, `[Military]`, `[AI]`, `[Code]`, `[Variety]`,
`[Agency]`, `[1970]`, `[Misc]`) and line numbers. Mark anything that must be fixed before
merge `[blocker]`. End with a count per category, or "No content issues found."

When the branch has an open PR, a title or body that does not match the diff is a
`[blocker]`. Name what the body claims that the diff lacks and what the diff contains
that the body omits. A missing body counts.
