---
name: lifecycle-check
description: 'Audit a 1970 Cold War country branch against the content lifecycle checklist (design notes, focus tree, ideas, decisions, history, characters, English loc, namelists, AI, game rules, graphics, multiplayer acceptance, changelog), reporting done/missing/partial per item. Use when asked if a country''s content is complete or review-ready, e.g. "/lifecycle-check ICE".'
---

**Syntax:** `/lifecycle-check [TAG]`. Without a TAG, infer it from the most frequent
`COLDWAR_<TAG>_` prefix in `git diff origin/main...HEAD --name-only`.

Read `.claude/docs/coldwar-1970-context.md` first. Upstream MD's lifecycle checklist is
online only and assumes `05_<country>.txt` / `MD_focus_TAG` files; the table below is
the 1970 version.

## Checks

Mark each item Done, Missing, or Partial (the file exists but looks like a stub).

### Design

| Item               | How to check                                                                 |
| ------------------ | ---------------------------------------------------------------------------- |
| Design notes       | `docs/<country>_1970_design/` or `docs/<country>_1970/` exists with a README  |
| Draft approval     | Cannot be checked from files. Remind the user approval comes before coding   |
| Generator (if any) | `tools/<country>_1970/` exists; loaded files' headers name it                |

### Coding

| Item                     | How to check                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| Focus tree file          | `common/national_focus/COLDWAR_TAG_1970_focus.txt` exists and is non-empty                    |
| Tree selection           | Its `country` block weights TAG under `IMP_is_1970_scenario = yes`, and/or `load_focus_tree` in the history `1970.1.1` block |
| Focus tree rewards       | Count `completion_reward` blocks vs focus count to spot stubs                                 |
| National ideas           | `common/ideas/COLDWAR_TAG_*.txt` exists; grep for idea blocks                                 |
| National decisions       | `common/decisions/COLDWAR_TAG_*.txt` and a category in `categories/COLDWAR_TAG_*`             |
| History 1970 block       | `history/countries/TAG - *.txt` has a `1970.1.1` block with leader, politics and focus tree   |
| OOB                      | Planned 1970 OOB, or the `mdcw_1970_empty_*` placeholder noted as deferred                     |
| Characters               | 1970 generals/advisors in `common/characters/` (`COLDWAR_TAG_*` or the TAG file)              |
| Party localisation       | 1970 party keys and `IMP_is_1970_scenario` clauses before the inherited ones                  |
| Focus localisation       | `localisation/english/COLDWAR_TAG_*_l_english.yml` covers every focus `id` and `_desc`        |
| Ideas localisation       | Every idea key and `_desc` resolves                                                           |
| Decisions localisation   | Every decision and category key resolves (AI-only ones have none)                             |
| English only             | No new non-English localisation file in the diff                                              |
| Unit namelists           | TAG entries in `common/units/names_divisions/`, `names_ships/`, `names/`                      |
| AI                       | Focus `ai_will_do` everywhere; AI path rule in `common/game_rules/COLDWAR_TAG_1970_rules.txt` if the tree forks |
| Scripted localisation    | `common/scripted_localisation/` entries for TAG (if used)                                     |
| Static checker           | Run it on every file above; record errors and warnings                                        |
| Country validators       | `tools/<country>_1970/validate*.py` run, if present                                           |

### Multiplayer and roleplay

| Item                   | How to check                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Cross-country actions  | Every effect on another country has accept/refuse, a deadline and a visible default           |
| Repeat and concurrency | One-shot effects guarded by flags set before payout; eligibility re-checked at execution      |
| Acceptance matrix      | A two-client matrix exists in the design notes or PR (`AGENTS.md`); unrun cases marked unrun |

### Graphics

| Item             | How to check                                                         |
| ---------------- | -------------------------------------------------------------------- |
| Focus icons      | Every focus has `icon =`; flag placeholders like `goal_unknown`      |
| Idea icons       | Grep the ideas file for `picture =`                                  |
| Leader portraits | 1970 leaders' portrait paths exist under `gfx/leaders/TAG/`          |
| Period fit       | Spot-check that icons and portraits show 1970-era people and kit     |

### Polish and completion

| Item            | How to check                                                |
| --------------- | ----------------------------------------------------------- |
| Spell-check     | Manual review needed                                        |
| error.log clear | Requires an in-game 1970 start                              |
| Playtest        | Requires manual confirmation, single player and two clients |
| Code compliance | Recommend `/content-review` and `/audit`                    |
| Changelog entry | Grep `Changelog.txt` for the TAG or country name            |

## Output

One line per item, grouped by phase, with `[✓]`, `[✗]`, `[~]`, or `[?]`, the item name,
and the path or reason. End with a count of done, missing, partial, and manual-only.
Flag any missing item required before review: focus tree, tree selection, history 1970
block, English localisation, acceptance matrix for cross-country content, changelog.
