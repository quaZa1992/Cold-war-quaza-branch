IMPERIA COLD WAR: Millennium Dawn skill adaptation, 24 October 2026

The reviewed upstream snapshot is [MillenniumDawn/Millennium-Dawn `.claude`](https://github.com/MillenniumDawn/Millennium-Dawn/tree/e1bb482ce492aa54e863d3c420f811f46054ea78/.claude), commit `e1bb482ce492aa54e863d3c420f811f46054ea78`. The complete subtree contains 24 skills, 44 domain documents, 10 agent roles, six path rules, a skill index and Claude settings. Three additional root files were retrieved for context and licensing. `upstream_inventory.json` records all 93 retrieved files, Git blob identities and SHA-256 fingerprints. The initial repository-wide API tree was truncated; it was replaced by the complete, non-truncated `.claude` subtree inventory before adaptation.

The useful upstream structure separates task instructions from conditional domain references. The adaptation follows that approach. Twenty-two new Codex skills are packaged here, and two files narrowly update the existing `mdcw-national-trees` skill. The installed modifier-audit and tree-layout skills retain their existing instructions and resources.

## Source-to-skill coverage

| Upstream skill | Adapted destination |
| --- | --- |
| add-leader | mdcw-leaders |
| additional-income | mdcw-economy-streams |
| adversarial-review | mdcw-edge-case-review |
| audit | mdcw-quality-audit |
| changelog | mdcw-changelog |
| close-issue | mdcw-github-workflow, requested closure mode |
| content-review | mdcw-content-review |
| country-ai-path | mdcw-country-ai |
| dev-diary-mdx | mdcw-dev-diaries |
| fix-issue | mdcw-github-workflow, scoped implementation mode |
| lifecycle-check | mdcw-lifecycle-check |
| md-tick-profiler | mdcw-tick-profiler |
| new-focus | Existing mdcw-national-trees, added scaffolding reference |
| new-namelist | mdcw-namelists |
| open-pr | mdcw-github-workflow, draft PR mode |
| party-names | mdcw-party-names |
| rework-brief | mdcw-rework-brief |
| search-filter-check | mdcw-search-filters |
| spirit-removal-desc | mdcw-localisation, starting-spirit conditions |
| standardize | mdcw-standardize |
| test-plan | mdcw-test-plan |
| update-claude | mdcw-maintain-skills |
| validate | mdcw-validate, scoped check mode |
| warnings | mdcw-validate, complete diagnostic mode |

The extra `mdcw-events-decisions` and `mdcw-scripted-gui` skills expose the useful event-builder role and domain rules as task capabilities for our agreement mechanics and minigames. Agent roles become review perspectives rather than imported agent configurations. All new skills remain discoverable without requiring an explicit-only invocation policy.

## Material adaptations

| Upstream assumption or conflict | Cold War behavior |
| --- | --- |
| 2000/2017 bookmarks and party research covering 2000-2025 | Resolve 1 January 1970 history and actual later gated identities; preserve other scenarios. |
| Modern party templates and a ban on pre-2000 dates | Research actual 1970 parties and institutions; relevant twentieth-century dates are valid. Do not invent country-inappropriate religious paths. |
| Minimum generic-tree focus count, event quotas and regional leader ranges | Use historically motivated programme depth and comparable MD mechanics; respect country-specific approvals rather than universal quotas. |
| Hard-coded upstream repository and task issues | Resolve the project's actual remote and requested issue. No automatic issue selection, claiming or upstream publication. |
| Automatic fix, commit, changelog and PR chain | Preserve the user's actual authorization. Local implementation and external actions are distinct, and already-authorized actions need no repeated permission. |
| Zero comments in AI work | Retain the exact project marker, upstream credit and useful existing comments. |
| Automatic reviewer fan-out and model pins | Use available Codex capabilities and applicable delegation instructions. No copied Claude permissions, model overrides or concurrency settings. |
| Mandatory reporting headings and BLUF endings | Follow the conversation's concise evidence-led communication rules. |
| Skip generated/binary assets during audit | Include runtime output, complete GUI donors and relevant asset closure; inspect the canonical generator too. |
| Modern tool paths assumed available | Discover actual local tools. The modern validation, analysis and standardization directories are absent in this checkout. |
| Generic additional-income example | Trace actual weekly MD consumers, costs, resets, local constants, precision, refresh order and paired transactions. |
| Tooltips satisfied by spirit names or event references | Require full native numeric prospective terms for both parties, including locked or unsigned states, with side-effect-free previews. |
| Generic building helper correctness | Verify internal fees and extra shared slots for every granted level, including infrastructure and forts, in the real state and one-time transaction. |
| Modern UN election/reference implementation | Preserve the current Cold War RP/GC session and consent model. |
| General recurring or expiring agreement patterns | Keep approved standing Cuban paired agreements indefinite, with actual sanction/peace/membership suspension and no repeated setup rewards. |
| Static profiler counts and model validation | Label static estimates, simulations, native startup, calendar/save/UI checks and genuine MP evidence separately. |
| Inconsistent upstream GUI-AI advice | Verify native support and actual configured access locally; do not assume either universal AI capability or universal impossibility. |
| Upstream localisation-file consolidation | Preserve existing country and mechanic file ownership and emitters. |

The current root `AGENTS.md` remains the authority for project standards. Skills include task-specific consequences without replacing the root instructions or altering normal game content. No runtime scripts, campaign balance, historical approvals or graphics are modified by this bundle.

## Reference treatment

Each new skill has a focused source notice with exact upstream paths and hashes, plus conditional domain guides only where needed. Important reviewed material includes scope/array traps, current-provider tracing, GUI invalidation, actual treasury helper fees, native dynamic text, reachable AI cures, OOB variants, complete warning sidecars and preservation-test limits.

The full source snapshot is a local ignored review copy, not an active skill library. Audio, music, loading screens and unrelated 3D or formable implementation recipes are retained as source context; they are not silently installed as new workflows or a modern feature port. Where a related lifecycle review is useful, it points the agent back to actual local providers. No downloaded executable helper is run. The adapted installer uses only the already-bundled skill installer for path validation and copying.

## Packaging and checks

`build_metadata.py` generates native discovery metadata and per-skill attribution without rewriting the authored instructions. `manifest.json` records prepared sources, target paths, expected existing hashes and final hashes. The update to `mdcw-national-trees` changes its entrypoint marker, adds one reading pointer and adds one scoped reference; other resources are untouched.

`validate_bundle.py` runs the official skill validator, parses UI metadata, checks local reading links, markers, encodings, source fingerprints and coverage of all 24 upstream skills. It verifies installed hashes when requested. `install_bundle.py` validates before writing, rejects changed or linked destinations, backs up the existing entrypoint and uses the official skill-installer helper to copy new skill folders. Installation remains within the requested skills and does not change app settings.

Fresh skills are available to Codex on the next turn. The checks establish packaging and discoverability metadata, not that every future task will choose the ideal skill or that game behavior has been tested. A bounded independent read-only task is used to forward-test representative fiscal guidance; its outcome is recorded separately.

Source rights, attribution and modification scope are recorded in [SOURCE_NOTICE.md](SOURCE_NOTICE.md). Prepared and installed verification records are stored alongside this analysis after execution.
