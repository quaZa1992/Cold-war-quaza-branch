---
name: mdcw-github-workflow
description: Fix a specified repository issue, prepare an accurate draft PR, or close an issue for IMPERIA COLD WAR when requested. Resolve the actual Git remote and preserve the user's chosen branch and publication scope.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Repository issues and pull requests

Read `AGENTS.md` and [references/repository-actions.md](references/repository-actions.md). Resolve the current repository and remote. This project's origin was `Imperia-MD/mdcoldwar` during adaptation; reconfirm it. Never send project work to `MillenniumDawn/Millennium-Dawn` merely because an upstream recipe hard-codes that repository.

Choose the mode from the user's request:

- Fix an issue: read the specified issue and relevant comments, reproduce or establish its cause, implement the scoped fix, and run relevant checks. A pasted task needs no tracker search. Do not select an unrelated issue or claim an assignee automatically.
- Prepare a PR: compare the actual branch with the intended base, inspect the final diff, draft an outcome-led title and body with relevant validation and limits, and preserve the repository's template. Include linked closures only for verified issues the change actually resolves. Use a UTF-8 body file with `--body-file` for multiline text.
- Close an issue: verify the named repository, issue, fix and publication state. Draft the concrete fix summary before applying the requested closure. A local fix alone is insufficient evidence that a published release contains it.

Keep local implementation independent of external publication. A bugfix request does not automatically ask for comments, assignment, push, PR creation or closure. Conversely, carry out already-authorized actions without redundant confirmation. Prepare the concrete reviewable result before requesting genuinely missing approval.

Inspect the worktree before Git mutations. Use `codex/` for a new branch unless the user chooses otherwise. Preserve direct-main instructions and existing work; do not forcibly reset, stash indiscriminately or overwrite a remote. Respect Git LFS for binary assets and verify the remote commit after a requested push.

Report the fix, actual checks and resulting commit/PR/issue links where applicable. Do not use upstream's mandatory BLUF ending, forced changelog commit, automatic issue selection or validation omission rules.

Source and adaptation: [references/source.md](references/source.md).
