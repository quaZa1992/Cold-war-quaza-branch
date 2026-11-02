---
name: mdcw-changelog
description: Write concise English changelog or release-note entries for verified IMPERIA COLD WAR changes. Use when changelog updates or player-facing release notes are requested, not automatically after every edit.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Player-facing changelog

Read `AGENTS.md`. Resolve the requested version and change range from the user's task, commits and working tree. On `main`, use the requested commits or current work rather than assuming an empty branch diff means no changes. Preserve an explicit release baseline.

Find the active changelog or release-note destination and read its actual categories and ordering. Keep an existing upstream changelog separate from custom Cold War notes when that is the established project structure. Do not invent a version bump, require a separate commit or impose one bullet per PR when the task has no PR.

Describe observable outcomes in concise English with specific mechanic or country names. Use actual tags for country prefixes where the file uses them. Separate genuinely distinct changes; group related implementation details into the same player outcome. Avoid internal scope names, receipt flags, debug explanations and claims of tests that were not run.

Preserve current categories and formatting, avoid duplicate coverage, and use ordinary punctuation without en or em dashes. Include only verified issue references. Do not label a startup check as a multiplayer stability certification.

Review the final entry against the actual diff and current mechanic names. Editing a changelog does not itself authorize staging, committing, pushing, creating a PR, or posting release notes elsewhere. Follow any existing explicit authorization for those actions.

Source and adaptation: [references/source.md](references/source.md).
