---
name: test-plan
description: Generate an approximate 1970 playthrough and two-client multiplayer test plan for the current branch of the Cold War RP mod. Run after /open-pr to attach a test plan, or standalone to draft test steps for a diff.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

Generate an approximate playthrough test plan for the current branch. The model cannot
run the game, so the output is a draft the human verifies and trims.

Arguments (optional, space-separated):

- Issue numbers the plan should cover, e.g. `12 15`

Requested arguments: $ARGUMENTS

## Steps

### 1. Gather context

```
git rev-parse --abbrev-ref HEAD
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
git diff origin/main...HEAD
```

If the branch has no commits ahead of the base, stop: "No commits ahead of main, nothing
to test."

For each issue number in `$ARGUMENTS`, run
`gh issue view <N> --repo quaZa1992/Cold-war-quaza-branch --json number,title,body` to
label which checks cover which issue. If `gh` errors, skip that number.

### 2. Derive the tests

From the diff, identify the affected country tags and systems (focus tree, events,
decisions, ideas, GUI, AI, diplomacy between countries). For each, infer the concrete
in-game action a tester would take and the outcome they should confirm. Every
playthrough starts from the **Cold War 1970** bookmark; that is the only start.

Group checks into **playthroughs** keyed by country tag (a tester loads one save and
runs all its checks together). Keep every check grounded in what actually changed in the
diff. Do not invent coverage for untouched systems.

When the diff touches anything one country does to another, a shared GUI, a timer, a
proposal, or shared state, add a **Multiplayer** block for two real clients using the
`AGENTS.md` matrix: concurrent actions, refusal, repeated click, pause/resume,
save/reload, disconnect/rejoin, and co-op on the same country where relevant. Add an
AI-counterpart check (the other side run by the AI).

### 3. Emit the test plan block

Use this exact structure:

```
### Test plan

**Playthrough A: <TAG> 1970 (covers #N, #M)**

<phase header, e.g. "Game start, before unpausing:">

- [ ] `tag <TAG>`, <action>, confirm <expected outcome> (#N).
- [ ] <next checkbox> (#M).

<next phase header, e.g. "Mid-game checks (advance several in-game weeks first):">

- [ ] <action>, confirm <expected outcome> (#N).

**Multiplayer: <TAG> host + <TAG> client, 1970 (covers #N)**

- [ ] Both players open <GUI/decision> at the same moment and click <action>, confirm it applies once and both clients show the same result (#N).
- [ ] Recipient refuses, confirm the sender sees the refusal and no cost is kept (#N).
- [ ] Pause before the deadline, save, reload, resume, confirm the deadline and pending state survive unchanged on both clients (#N).
- [ ] Client disconnects and rejoins while the proposal is pending, confirm matching state and no duplicate event (#N).
- [ ] Same action against an AI-run counterpart, confirm the AI answers within the deadline (#N).
```

Rules:

- Each playthrough block starts with a bold header naming the country tag, `1970`, and
  the issues it covers. Group checks under phase sub-headers when a check needs setup
  beyond game start.
- Every check is a markdown task list item: start with `- [ ]`, never bare `- `. One
  checkbox per distinct in-game action. End each with the issue ref it covers, `(#N)`.
- Checkbox structure: console command (if any) in backticks, then the action, then
  `confirm <expected outcome>`. Separate clauses with commas or periods, not `→` or `—`.
- Console-fired events have no real FROM/PREV; use the real trigger for sender and
  recipient checks.
- Add `Check error.log for new lines naming the changed ids` as the last item of each
  single-player playthrough.
- Skip the Multiplayer block only when the diff has no cross-country or shared-state
  effect, and say so.
- **Never use em dashes (`—`, U+2014) anywhere.** Use a colon, period, or comma.

### 4. Output

1. Print the test plan block for the user to paste.
2. If a PR already exists for the branch
   (`gh pr view --repo quaZa1992/Cold-war-quaza-branch --json number,body`), offer to add
   the `### Test plan` section to the PR body via `gh pr edit`, above the closing `BLUF`
   line. Do not overwrite an existing test plan without confirmation.
3. State plainly that the plan is approximate, that no in-game or two-client test was
   run, and that it needs human review before it is trusted.
