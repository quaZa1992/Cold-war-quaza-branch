# IMPERIA COLD WAR: MD 2.0.3 update review

Status: the recommended proposal was subsequently approved and implemented. See IMPLEMENTED.md and implementation.json for the actual changes and verification. The original comparison and file choices below are retained as review evidence.

## Scope and evidence

The supplied Workshop source contains 79,711 regular files; the current Cold War tree contains 98,740. All were read and hashed. The archived original MD inventory contains 79,721 files. Their union is 98,818 paths. There were no read errors, case collisions or final-scan source changes.

The archive is the actual source inventory from the earlier migration, not an assumed ancestor. Its SHA256 and current Git HEAD are in inventory_summary.json. Every one of the 71 changed/deleted historical MD files has a recovered, hash-verified original. The research GUI ancestor was verified against the official v2.0.2 tag. The Workshop descriptor was recovered by reversing only its version literal and matching its exact archived raw hash.

Git metadata, private caches and the audit output/tool directories are explicitly excluded. Four asset-provider junctions are recorded without traversal. They are aliases rather than independent game assets. No regular runtime directory was excluded.

## What this installed MD update actually changes

There are 73 changed/additional/deleted source paths: 59 changed existing files, 12 deletions and two development PNG additions. Of these, 69 are runtime-directory paths. The installed source changes native UI controls and keyboard shortcuts for HOI4 1.19.4, research-tab tooltips, the native agency upgrade queue and obsolete offer filters. It also changes version labels. This delta contains no changed MD country focus tree, state history, map binary, economy formula or unit-technology definition. The technology-tag file differs in formatting only.

The two additional files are Cold War Egyptian preview PNGs under Claude outputs. They are documented source-folder development artifacts, not interpreted as a new upstream gameplay feature. The supplied folder is the user-selected source; it is not falsely certified as a byte-identical pristine GitHub release.

The public release is [v2.0.3](https://github.com/MillenniumDawn/Millennium-Dawn/releases/tag/v2.0.3). The release link confirms the release identity, while the local full-file hashes establish this comparison. The public Git tag descriptor still contains a developer 2.0.2 label; the supplied Workshop descriptor contains 2.0.3. Version strings alone are therefore not the merge baseline.

## Results and preservation

Twenty-three script/text files have exactly the same executable tokens as the new MD source after excluding comments and whitespace. Two localisation files already have all the same MD key values, including both research-tab tooltip strings. The full three-way probes returned 34 files with no additional executable changes, 22 clean metadata/text updates and three textual conflicts.

The three textual conflicts are: descriptor version plus the custom mod name; an already-removed satellite filter handler next to locally reformatted closing blocks; and research tooltip lines that are already identical except for a local comment. These do not justify replacing the shared Cold War files.

14,534 runtime files are additional or modified Cold War content outside the MD delta and are preserved. The remaining shared-file custom changes also stay: early research and equipment, nine-resource uranium trade/UI, Space Race, recognition presentation, nuclear-intelligence passive-defence receipts, dossier observers, guest workers, reserve-currency tracking and 1970 event guards. The separate SSR agency-creation blocker and its native parent window remain in place.

Existing MD auto-agency files are already comment-only stubs or an empty localisation header in the current Git commit. Removing these twelve empty files follows upstream cleanup without removing an active Cold War programme. Keeping them is an equally feature-preserving compatibility option. Reinstating the obsolete modded queue is not part of either proposal.

## Decisions for the user

| Area | Proposed source choice |
| --- | --- |
| Native UI, shortcuts, queue and filters | Retain the MD 2.0.3 fixes already merged into our files. |
| Research, uranium, Space Race, SSR, diplomacy and 1970 content | Retain Cold War implementations and additions. |
| Descriptor and version labels | Update to 2.0.3, retain Cold War name and custom paths. |
| Twelve obsolete empty agency files | Recommended: remove. Alternative: retain empty compatibility stubs. |
| Two Egyptian preview PNGs in the supplied MD folder | Exclude from the update. |

The requested decision is whether to apply the recommended version-and-cleanup proposal, retain the twelve empty compatibility files, or select individual file exceptions. Nothing in the active mod has been replaced while this choice is pending.

## Complete changed-source file catalogue

| File | Classification and proposed action |
| --- | --- |
| `Changelog.txt` | ASK_UPDATE_UPSTREAM_NOTE: Retain the earlier MD notes as historical reference in the audit, and adopt the supplied current upstream note with project provenance. |
| `Claude outputs/COLDWAR_EGY_1970_layout_preview.png` | EXCLUDE_SOURCE_DEVELOPMENT_ARTIFACT: Exclude these two Cold War development previews found in the supplied MD folder; they are not a runtime update. |
| `Claude outputs/COLDWAR_EGY_1970_nationalist_preview.png` | EXCLUDE_SOURCE_DEVELOPMENT_ARTIFACT: Exclude these two Cold War development previews found in the supplied MD folder; they are not a runtime update. |
| `common/decisions/categories/MD_auto_agency_category.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/decisions/MD_auto_agency_decisions.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/ideas/MD_auto_agency_ideas.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep completed passive-defence tracking for nuclear intelligence and the Cold War covert-action artwork; the MD native upgrade changes are already present. |
| `common/intelligence_agency_upgrades/README.md` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `common/modifier_definitions/MD_auto_agency_modifier_definitions.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/on_actions/MD_auto_agency_on_actions.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/on_actions/MD_on_actions.txt` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep guest-worker updates, 1970 date guards and reserve-currency accounting observers; the MD queue callback removal is already present. |
| `common/scripted_diplomatic_actions/00_scripted_diplomatic_actions.txt` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep dossier correspondence receipts; obsolete MD offer filtering has already been removed. |
| `common/scripted_diplomatic_actions/MD_missile_scripted_diplomatic_actions.txt` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `common/scripted_effects/00_MD_auto_agency_scripted_effects.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/scripted_guis/00_MD_auto_agency_scripted_gui.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/scripted_guis/00_missiles_scripted_guis.txt` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep Space Race, Cold War satellites and international-system changes. The obsolete satellite-reject handler is already absent; retain current balanced closing blocks. |
| `common/scripted_guis/01_automation_settings_scripted_gui.txt` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `common/scripted_localisation/00_automation_settings_scripted_localisation.txt` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `common/scripted_localisation/00_MD_auto_agency_scripted_localisation.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/scripted_localisation/01_missiles_scripted_localisation.txt` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `common/scripted_triggers/00_MD_auto_agency_scripted_triggers.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `common/synchronized_dynamic_tokens/MD_tokens.txt` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep uranium, uranium-mine, energy and resource-toolbar tokens; MD removed queue/filter tokens are already absent. |
| `common/technology_tags/00_technology.txt` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `descriptions/descriptions_BR.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_DE.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_EN.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_ES.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_FR.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_JP.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_KR.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_PL.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_RU.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_SC.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptions/descriptions_TC.txt` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `descriptor.mod` | ASK_UPDATE_METADATA_KEEP_IDENTITY: Set version to 2.0.3; retain MD Cold War name, portable launcher identity and all custom replace paths. |
| `events/MD_auto_agency_events.txt` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `interface/airselectionview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/alerts.gfx` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/alerts.gui` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep COMECON toolbar clearance; new MD native alert buttons are already present. |
| `interface/command_character_view.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/countryconstructionsview.gfx` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/countryconstructionsview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/countrydiplomacyview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/countryintelligenceagencyview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/countrytechtreeview.gui` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep 1970 research branches, early equipment and custom positions. Native MD research-tab controls are already present. |
| `interface/countrytradeview.gui` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep nine-resource uranium geometry. New MD trade controls are already present. |
| `interface/frontendgamesetupview.gfx` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/general_stuff.gfx` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep nine-frame resource strips including uranium. New MD sprites are already present. |
| `interface/mapicons.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/mapmodes_interface.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/MD_auto_agency_queue.gui` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `interface/MD_automation_settings.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/MD_countrymissilesview.gui` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep Space Race ledger and compact recognition list; obsolete MD satellite filter controls are already removed. |
| `interface/MD_energy_scripted.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/nationalfocusview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/naviesview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/operativeleader.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/topbar.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `interface/unitview.gui` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `localisation/braz_por/MD_frontend_l_braz_por.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/english/MD_auto_agency_l_english.yml` | ASK_REMOVE_EMPTY_LEGACY_FILE: Optional cleanup: delete this comment-only/empty-language-header file. Its earlier functionality is already disabled. |
| `localisation/english/MD_automation_settings_l_english.yml` | ALREADY_PRESENT_KEEP: Already contains the new MD content; keep current file. |
| `localisation/english/MD_frontend_l_english.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/english/MD_missiles_l_english.yml` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep Cold War GNSS benefit wording and legacy cleanup labels. The MD obsolete-filter text changes are already present. |
| `localisation/english/research_l_english.yml` | KEEP_COLD_WAR_WITH_MD_FIXES_ALREADY_PRESENT: Keep current file: both new MD research-keyboard tooltip values already match exactly, including all local extra keys. |
| `localisation/french/MD_frontend_l_french.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/german/MD_frontend_l_german.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/japanese/MD_frontend_l_japanese.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/korean/MD_frontend_l_korean.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/polish/MD_frontend_l_polish.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/russian/MD_frontend_l_russian.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/simp_chinese/MD_frontend_l_simp_chinese.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |
| `localisation/spanish/MD_frontend_l_spanish.yml` | ASK_SYNC_EXISTING_VERSION_LABELS: Update existing upstream version literals from 2.0.2 to 2.0.3 without generating new translations or replacing Cold War identity. |

## Artifacts and limits

- all_files.jsonl.gz: one record for every union path, with original/new/local hashes and classification.
- inventory_summary.json: source coverage, exclusions, stable-scan evidence and area counts.
- upstream_changes.json and upstream_delta.diff: all source changes and verified original-to-new textual hunks.
- semantic_review.json and local_preservation.diff: full token/key comparison, dry-run merges and local feature differences.
- decisions.csv and adoption_plan.json: per-file action catalogue and pending user choices.

This is source and merge-probe evidence. No HOI4 launch, save conversion, tooltip rendering, economy tick or multiplayer rehearsal has run for this update. A full engine feature audit is not claimed merely from hashing every file.

## Provenance

The audit tools and review narrative were authored for IMPERIA COLD WAR with Codex. Original source credit: Millennium Dawn contributors and existing Cold War/Imperia contributors. Source code excerpts in the two diff reports retain their original source identity; no artwork pixels are modified or copied into the active mod. Individual upstream authors and separate redistribution permissions are unknown where the inherited source does not identify them. Existing repository licence and notices remain authoritative; a project marker does not establish third-party ownership.
