# Skills

Project slash commands for Claude Code in the Cold War 1970 RP multiplayer mod. Each
directory holds a `SKILL.md` whose frontmatter (`name`, `description`) is the source of
truth — the session skill list is generated from it, so this table is a human-facing
overview only.

They are adapted from Millennium Dawn's upstream Claude skills. Every skill reads
`.claude/docs/coldwar-1970-context.md` for the facts that differ from upstream: the 1970
bookmark, `IMP_is_1970_scenario` gates, `COLDWAR_<TAG>_` naming, English-only text, the
fork's GitHub repository, and which upstream tools are absent. The Codex skills in
`.agents/skills/` (multiplayer, diplomacy, GUI, recon, validation) cover the same
repository and are referenced where they apply.

| Skill                  | What it does                                                           |
| ---------------------- | ---------------------------------------------------------------------- |
| `/add-leader`          | Scaffold 1970-era generals, field marshals, and admirals for a TAG     |
| `/additional-income`   | Wire a country income/expense stream into the money system             |
| `/adversarial-review`  | Edge-case hunt over a diff or file, including MP and human agency      |
| `/audit`               | Full pre-merge review via parallel reviewer agents                     |
| `/changelog`           | Add branch changes to Changelog.txt                                    |
| `/close-issue`         | Close a fork issue with a fix summary (explicit-only)                  |
| `/content-review`      | Check content against the 1970 content checklist                       |
| `/country-ai-path`     | Build or standardise one AI-run country's 1970 AI path game rule       |
| `/dev-diary`           | Convert a dev-diary .docx to a Markdown post in `docs/dev_diaries/`    |
| `/fix-issue`           | Pick up a fork issue or task, fix it, open a PR                        |
| `/lifecycle-check`     | Audit a 1970 country branch against the lifecycle checklist            |
| `/md-tick-profiler`    | Static call tree of the daily/weekly/monthly tick load (bundled tool)  |
| `/new-focus`           | Scaffold a `COLDWAR_<TAG>_1970_focus.txt` tree with loc stubs          |
| `/new-namelist`        | Scaffold 1970-era division/ship/air namelists for a TAG                |
| `/open-pr`             | Create a draft PR on the fork with summary, issues, changelog          |
| `/party-names`         | Add 1970 party names, descs and gated hooks for a TAG                  |
| `/rework-brief`        | Reframe a rework task issue into a mechanic-by-mechanic design brief   |
| `/search-filter-check` | Validate focus `search_filters` against filters defined in this tree   |
| `/spirit-removal-desc` | Append the removal footer to a TAG's 1970 starting spirit descriptions |
| `/standardize`         | Bring one file up to MD code style by hand (no upstream tool)          |
| `/test-plan`           | Generate a 1970 playthrough and two-client MP test plan (opt-in)       |
| `/update-claude`       | Propose CLAUDE.md/rules/docs/skills improvements from the session      |
| `/validate`            | Run the static checker and country validators (explicit-only)          |
| `/warnings`            | Full untruncated checker findings, filtered (explicit-only)            |

Conventions: every skill has frontmatter with a trigger-quality `description`;
`disable-model-invocation: true` marks skills that only run when the user invokes them.
Reference material belongs in `.claude/docs/`, not in skill bodies — skills cite docs.
