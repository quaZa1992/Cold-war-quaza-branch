# IMPERIA COLD WAR — Local work and external actions

Resolve repository identity from the actual remote before issue or PR operations. Never infer that a number mentioned in upstream instructions belongs to this project. Inspect available connectors or `gh` capability without changing authentication or publishing configuration.

An authorized implementation can proceed with local inspection, edits and relevant tests. It does not by itself authorize assigning, commenting on or closing issues, pushing, publishing or opening PRs. If the user already requested one of those actions, complete it without asking again. A skill should neither expand authority nor invent extra approval requirements.

Prepare a final title/body from the real final diff. Include validation and material limits when useful or required by the repository template. Do not suppress tests because an upstream PR recipe bans a testing section, and do not impose ritual endings. Write multiline bodies to a UTF-8 file and pass `--body-file`; avoid shell interpolation of arbitrary task text.

Preserve existing work, branch choice and explicit direct-main instructions. New branches normally use `codex/`. Fetch and integrate remote changes without destructive reset or force push. Git LFS must remain active for binary staging and upload. Disabling LFS to obtain a readable status is not a safe way to stage binary files.

A stale Git lock can be removed only after establishing that no active owner remains and that the lock is genuinely old. Do not treat a busy or recent lock as disposable. After publication, verify remote and local commit IDs and report any leftover work accurately.
