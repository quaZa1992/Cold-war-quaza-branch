---
name: adversarial-review
description: "Adversarial edge-case hunt over the branch diff or a single file in the Cold War 1970 RP multiplayer mod: challenges every change for unhandled scenarios, silent failures, scope/timing/variable traps, multiplayer and human-agency gaps, and 1970 anachronisms that rule-based review misses. Use when asked to adversarially review, stress-test, or find edge cases in a change."
---

**Syntax:** `/adversarial-review [file_path]`. Without a path, review every file the
branch changes against `origin/main` (see `.claude/docs/coldwar-1970-context.md`).

Do not check compliance against known rules. Imagine every way the change could break
in practice, in a long multiplayer session with several humans.

## 1. Gather context

`git log origin/main..HEAD --oneline` and `git diff origin/main...HEAD`. Identify the
changed files and their types, and whether any are generated (header comment naming a
`tools/` builder).

If the diff touches `tools/**`, dispatch `tools-reviewer` in parallel with the list of
changed tooling files, and fold its findings into the report.

## 2. Challenge every changed block

Apply both sections of `.claude/docs/bug-patterns.md`, plus the relevant parts of
`.claude/docs/scripting-edge-cases.md` and `.claude/docs/hoi4-data-structures.md`. Then
ask, for each block:

- Two humans act at once, or one clicks twice, or co-op players both click. Is the
  effect applied once? Is eligibility re-checked at execution, not only at display?
- The game is paused, saved, reloaded, or a player disconnects and rejoins mid-chain.
  Does any state, timer or pending proposal duplicate, vanish or stall?
- The target is human. Can they refuse, see the cost and deadline, and is the default
  on expiry visible? Does anything force war, annexation, government change or an
  irreversible loss on them without consent?
- The target is AI, or does not exist at 1970, or is in a civil war.
- The content runs at a 1970 start: is it gated on `IMP_is_1970_scenario` where needed,
  and does it leak into or depend on dormant 2000-era MD content? Any anachronistic
  people, parties, equipment or dates?
- Generated file edited by hand? The next build reverts it.

Flag every question whose answer is "no, it is not handled".

## 3. Output

Lead with the findings, or "No findings in the reviewed scope." Per file:

1. The path and type.
2. A numbered issue list with category labels (`[Scope]`, `[Timing]`, `[Variable]`,
   `[Silent]`, `[Cross-Country]`, `[MP]`, `[Agency]`, `[1970]`, `[GUI]`, `[Content]`)
   and line numbers.
3. For each issue: the exact scenario that breaks, what happens to the player or game
   state, and a suggested defense, or a note that the omission looks intentional.

Mark anything that could corrupt a save, desync clients, soft-lock a player, or crash
the GUI `[critical]`. State what was not verified, and that no multiplayer test was run.

When the branch has an open PR, a title or body that does not match the diff is a
`[blocker]`. Name what the body claims that the diff lacks and what the diff contains
that the body omits. A missing body counts.

End with `BLUF`.
