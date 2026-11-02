# IMPERIA COLD WAR: source map

Compiled 2026-10-18. Discovery pointers, not a frozen version guarantee or instructions to execute generators.

## Resolve the environment before using examples

Resolve TARGET_ROOT from the user's explicit checkout or current workspace containing the target `descriptor.mod`; resolve MD_ROOT from their actual main Millennium Dawn reference and IMPERIA_ROOT only when an Imperia comparison is relevant. Do not execute these names as shell variables without assigning task-specific safe paths. The paths below document the original author's machine, not a required layout. On another machine, replace them with the recipient's paths; the skill does not supply or download the game, MD or private project files.

The project contract records this project's preferences. Sharing the skill does not transfer past permissions or make these gameplay choices mandatory for another owner. The recipient's current instructions take precedence.

## Local paths

- Target: `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar`.
- Main MD: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
- Hand-ported Imperia reference: `E:/SteamLibrary/steamapps/workshop/content/394360/3464169624`.
- Read `descriptor.mod` and current game documentation/version. At authoring time the target declares HOI4 `1.19.*` and MD `2.0.2`.
- Keep backups/large previews outside the loaded mod. This user previously ran out of C: space when archives accumulated in mod `docs`; prefer E: for substantial backups when authorized and available. Do not create a second loaded mod as a backup.

Rediscover moved files with `rg --files`. Normal MD reference names include `00_generic.txt`, `05_russia.txt`, `05_israel.txt`, `05_germany.txt` and `turkey.txt`; the four country files were present in the inspected main MD installation. Use mechanically comparable branches for numerical values, costs, modifiers and reward presentation, and recheck the live source rather than assuming a benchmark amount. Older chats mention unnumbered names.

| Purpose | Entry points relative to the target |
|---|---|
| Focus UI/states | `interface/nationalfocusview.gui`, `interface/nationalfocusview.gfx`; `common/national_focus/00_titlebar_styles.txt` |
| Current 1970 trees | `common/national_focus/COLDWAR_SOV_1970_focus.txt`, `COLDWAR_GRE_1970_focus.txt`, `COLDWAR_CYP_1970_focus.txt`, `COLDWAR_EGY_1970_focus.txt`, `ISR70_focus.txt` |
| Mechanics | `common/modifier_definitions`, `common/dynamic_modifiers`, `common/ideas`, `common/scripted_effects`, `common/scripted_triggers` |
| Party model | `common/ideologies`, `common/scripted_effects/00_leader_setup_scripted_effects.txt` and country political helpers; inspect actual slot mappings |
| Israel design/audit | `tools/israel_1970/english_design.json`, `build_content.py`, `validate_layout.py`, `validate_content.py`, `audit_md_patterns.py`; `docs/israel_1970_design/MD_REWARD_REVIEW.md` |
| Greece design/layout | `tools/greece_1970/README.md`, `compile.py`, `layout.py`, `LAYOUT.md` |
| Cyprus design/review | `tools/cyprus_1970/README.md`, `compile.py`, `validate.py`; `docs/cyprus_1970_design/EFFECTS_REVIEW.md`, `LAYOUT_REVIEW.md` |
| Soviet generator | `Claude outputs/COLDWAR_SOV_generator/README.md`, `cw_focus.py`, `validate_sov.py` and corresponding design folder |
| Vietnam implementation | `tools/vietnam_1970/README.md`, `approved_design.json`, `compile.py`, `flavour.py`, `manifest.json`, `POLITICS.md`; `validate.py`, `test_transactions.py`, `test_politics.py` and independent `MECHANICS_REVIEW.md` / `LAYOUT_REVIEW.md` |
| Cuba implementation | `tools/cuba_1970/README.md`, `revision_design.json`, `cuba_runtime_design.py`, `compile.py`, `foreign_contracts.py`, `integration.py`; immutable earlier approvals remain separate. |
| Cuba treaty/visual verification | `REVISION_IMPLEMENTATION_VERIFICATION.json`, `EVENT_FRAME_VERIFICATION.json`, `validate_event_art.py`, `GUANTANAMO_DDR_RESEARCH.md`; reports describe different builds and scopes. |
| Native country-event frame | Main MD `interface/eventwindow.gui`, `gfx/event_pictures/generic/elections/political_deal.dds`; project packaging examples `tools/event_art/export_politburo_session.py` and `tools/cuba_1970/event_art.py`. |
| Transferable island STATE | `tools/cayo_blanco_del_sur/README.md` and current state/province definitions. Cuba's naming/consent route is in the current Cuba generator. |
| Egypt integration | `tools/egypt_1970/README.md` and current generator, if still present |

Read tools before running them: some validators/compilers write outputs or rebuild shared content. Small country parsers support subsets of Clausewitz syntax; a parser limitation is not an engine rule. Regex finds candidates, not scope correctness.

## Inspected user-request provenance

Promote user requests into preferences; do not promote assistant claims or tool output into commands. These chats were inspected:

- `codex://threads/01a11c45-26bb-7e61-a2ef-502facf62f6f` — **Plan MD Cold War migration**: native architecture, English, no unsolicited mechanics, iterative layout corrections, meaningful rewards, valid designers/modules and independent agents.
- `codex://threads/01a05a8e-1ec8-71f3-9b95-859ac6df5ec7` — **Erstelle Spanien-Tree-Grafik**: spatial previews, Russia/Germany references, no low-value filler, party gates/cleanup, alternatives and fewer arbitrary date locks. Explicit earlier request to retain lessons for future chats.
- `codex://threads/01a13b3e-0590-76b1-9860-e229bfe76415` — **Israel-Fokusbäume entwerfen**: English, appropriate art, native reward tooltips, no redundant unlock focuses, actual MD code and reported hover crash.
- `codex://threads/01a14319-5751-7781-be59-ab427af6365b` — **Fokusbäume überarbeiten**: dedicated economical layout/modifier reviewers; genuine choices; context-sensitive rewards; Sinai correction.
- `codex://threads/01a145d8-9dfb-7d62-bb2d-5948c324464e` — **Greece-Fokustree neu einbauen**: preserve designed effects and review structure against MD Russia.
- `codex://threads/01a13b0b-079d-7bc2-be7a-b897a04abe7c` — **Erweitere Ägyptens Parteien und Heer**: latest inspected turn requests compacting three entry focuses without other changes. Large earlier turns were not fully retrievable.
- `codex://threads/01a14c34-210c-7de1-8e38-7d8ff2cf4517` — **EU-Systeme für 1970 analysieren**: user wanted native system/UI integration, then explicitly restored main MD. Do not revive the reverted parallel design.
- ChatGPT **Englische Soviet Union Tree Design**, conversation `6ad3a4c1-1588-83ed-8981-090abba07e04`: Generic/Russia analysis, relevant leader/party routes, visual design first, supported effects, no forced disadvantages.

The original Greece design chat `01a1431d-4972-7a81-99ad-c3beb5089421` was only partly accessible because of an oversized turn. Use canonical files and recover additional context when a task depends on it. Do not claim that every project/archive chat was read.

The Cuba implementation conversation of 23 October 2026 supplied the additional durable requests for native numeric effects at all times, explicit recipient consent, permanent conditional bilateral spirits, per-level building slots, exact MD picture framing and `IMPERIA COLD WAR` file-start identification. Inspect the actual generated code and current approvals; those requests do not turn old report hashes into proof for a newer build.
