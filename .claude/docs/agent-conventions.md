# Agent Conventions

Read `AGENTS.md` and `coldwar-1970-context.md` at the start of every task. `AGENTS.md`
sets the design priorities (human RP agency, multiplayer reliability, transparent
interactions, English-only text); `coldwar-1970-context.md` sets the repository facts
(1970 start, naming, gates, which tools exist). Role files add only role-specific
requirements.

## Scope and Reading

- Work on the caller's assigned files, issue, or diff. No idle scans or unrelated fixes
  unless requested. Trace shared consumers when needed without widening edit scope.
- Read the relevant definitions and callers, including nested effects and AI blocks.
  Use the task links in `AGENTS.md`; do not load every reference for every role.
- The other docs in this folder describe current upstream Millennium Dawn. Verify a
  mechanic, file or key exists in this tree before relying on it, and never call an
  upstream tool the context file lists as absent.
- Reviewers read `known-false-positives.md` and the relevant domain reference before
  reporting a suspected bug. Scripting reviews also use `bug-patterns.md`.
- Read `performance-patterns.md` when execution frequency or scope expansion matters.
- English-localisation work uses `localisation-rules.md` and `typo-watchlist.md`.
- Tooling work uses the tool's own README under `tools/<area>/` and
  `validation-pipeline.md`, not game-script recipes.
- Anything a human player can trigger against another country also follows the
  `hoi4-rp-multiplayer` and `hoi4-rp-diplomacy` skills in `.agents/skills/`.

Paths without a directory above are under `.claude/docs/`.

## Hand Back in BLUF Style

Lead with the result or blocker, then only the evidence the caller needs.

- Writers: changed behavior and `path:line`, checks actually run and their result,
  remaining work, and any in-game or two-client verification still needed. Do not
  paste whole files already edited; provide code blocks only when the caller requested
  a draft.
- Reviewers: findings ordered by severity, each with `path:line`, impact, and the
  smallest safe fix. Say no findings when clean. Do not invent issues to fill categories.
  When the branch has an open PR, verify the PR body (title and description) describes what
  the diff actually changes; a mismatch is a blocker that rejects the PR until the body is
  corrected. Name what the body claims that the diff lacks or what the diff contains that
  the body omits. A missing or empty body counts as not matching.
- Separate confirmed defects from uncertain observations. Never claim a check passed
  without running it, and never report a static check as an in-game or multiplayer
  result. Omit empty headings and redundant counts.
- End the handoff with `BLUF`. Follow a requested machine-readable schema instead
  when a prose marker would invalidate it.

Severity: Critical means game-breaking, save-corrupting, desync-prone, or severe
repeated runtime cost; High is a correctness bug, a broken human-to-human interaction,
or significant cost; Medium is a smaller maintainability/performance issue; Low is
cosmetic. Judge frequency and reach, not syntax alone.

## Maintaining Agent Instructions

Keep each role to its purpose, task-specific reading, boundaries, and useful handoff
requirements. Do not copy scripting examples, toolchain versions, helper inventories,
or shared output templates into it. Update the owning reference instead.

Where player and contributor guidance goes: `documentation-references.md`.
