# Modifier and effect audit

Resolve TARGET_ROOT to the user's actual project checkout and MD_ROOT to their main MD reference. Relative source anchors refer to TARGET_ROOT unless marked as main MD. Absolute original-machine examples below are optional pointers; replace them on another machine. Skills do not include or download these external files, and missing external inputs must not be treated as confirmed live defects.

## Prove the modifier, scope, and reader

Start from the focus completion effect, then search the installed MD source for the exact key. A useful local pattern is `tools/israel_1970/audit_md_patterns.py`: it checks keys against country-idea modifier blocks, dynamic modifier definitions, and registered custom modifier definitions, and checks custom scopes. Adapt its searches to the target key and current MD checkout; do not copy its accepted keys or treat its report as current without rerunning it.

Use evidence in this order:

- Find an actual MD use in a relevant country idea, dynamic modifier, focus, or scripted system.
- If the key is custom, inspect its registration and scope under the current mod's `common/modifier_definitions/` and then find the effect or formula that reads it.
- Follow the reader to its calculation, clamps, conditional branches, and unit conversion. A definition proves that a key is registered; it does not establish what a user-facing reward does.
- If no actual reader or supported native application path is found, mark the key unresolved or unsupported. Do not infer meaning from its name.

The local reward audit provides a concrete example of the reader check: its `interest_rate_multiplier_modifier` review follows the key from `common/modifier_definitions/money_modifier_definitions.txt` to `common/scripted_effects/00_money_system.txt` and the `calculate_interest_rate` logic. That code adds the value to `pre_clamp_interest_rate` and clamps the result. This example demonstrates why a suffix such as `_multiplier` cannot establish percentage semantics. Recheck those files and formula in the current MD version before citing the example in another review.

## Distinguish execution from presentation

Inspect the actual `completion_reward` and every called helper. `custom_effect_tooltip`, `effect_tooltip`, tooltip labels on variable effects, and localization strings describe or format behavior; they do not by themselves prove that a modifier is granted. Conversely, hidden effects may execute without appearing in the main reward summary. Confirm both sides:

- Does the player see a truthful label and amount for each material effect?
- Does the effect run once, on each completion, in the intended country/state/character scope?
- Is there a hidden effect or event choice that changes the amount or recipient?
- Are the visible costs, duration, conditions, and failure/refund paths consistent with the code?

Use `tools/israel_1970/validate_rewards.py` as a local example of checking visible variable-change tooltips, localization keys, sprite registration, repeat limits, and cost/refund assumptions. Its checks are project-specific; adapt them rather than treating their rules as universal.

## Check parser acceptance and locked-focus previews

Audit both the unconditional display and the actual guarded payout. For a guarded implementation, native `effect_tooltip = { ... }` can display material effects while `hidden_effect = { ... }` executes the eligibility/once-only logic. The display-only block must not be counted as a real grant by validators or scenario models. Conversely, a correct preview does not prove execution. Compare modifier amounts, cash, buildings, event outcomes and decision unlocks on both sides, including conditions that can change before completion.

Recheck actual argument shapes, not just effect names. The Syrian repair exposed invalid scalar removal: native `remove_dynamic_modifier` uses `remove_dynamic_modifier = { modifier = ID }`. Locate the installed engine effects documentation and current MD examples before adapting the pattern.

Inspect raw bytes when logs reject an unexpected token at the beginning of otherwise normal scripts. In the Syrian case, leading UTF-8 BOMs in changed non-localization helper files caused native political helpers to fail to register; downstream unknown-effect errors were symptoms. Repair only affected files and fix their writers. Preserve the required localization encoding separately. Do not infer parser acceptance because a Python reader using `utf-8-sig` succeeded.

Use a fresh game process/log after parser repairs. Record the log timestamp and whether it predates the changed files. A source PASS is not a post-repair engine test.

## Establish units and stacking

Do not label a value “percent,” “percentage points,” “flat,” or “per month” until the native definition or consumer establishes that unit. Track the value from assignment to read site and display. Record whether the host applies it additively, multiplicatively, as a cap, as a daily/monthly tick, or through another formula.

Check how many live sources can contribute at once. For national ideas, dynamic modifiers, timed ideas, and variable-backed programmes, inspect all grant, replacement, refresh, and removal paths. A second idea may stack, overwrite, or be gated out depending on MD's implementation. Verify the actual branch and effect that refreshes the active modifier set; do not assume that a party change clears prior effects.

Where a formula reads a modifier variable, write down the source and transformed value, including clamps and frequency. A static arithmetic check can validate the written calculation, but do not present a bounded scenario estimate as a guaranteed campaign result unless all triggering conditions and concurrent sources have been established.

## Check specialized reward APIs directly

For equipment design bonuses, inspect the actual `add_equipment_bonus` usage, its `name`, nested bonus target, and whether that equipment type or designer category exists in the current MD source. MD focus examples are searchable in `common/national_focus/05_Australia.txt` (for example near its `add_equipment_bonus` usages); verify current lines and surrounding scopes.

For research, confirm that each `add_tech_bonus` category is used by real technologies in the current technology tree. A category declaration with no technologies is not meaningful coverage. The Israel local design validator follows this pattern in `tools/israel_1970/validate_design.py` by checking used categories against technology definitions.

Treat doctrine research as its own API. Search actual MD examples of `add_doctrine_cost_reduction` and confirm its `category`, `uses`, and cost fields against the intended doctrine tree. Do not replace a removed/nonexistent technology research target with a doctrine category, or describe a doctrine-cost reduction as a technology research bonus.

## Local anchors to recheck

The current workspace includes useful starting points:

- `tools/israel_1970/audit_md_patterns.py` and `docs/israel_1970_design/effect_api_audit.json` for modifier-key evidence and reader searches.
- `docs/israel_1970_design/MD_REWARD_REVIEW.md` for a worked, source-traced formula discussion; confirm each cited line against the live files.
- `<MD_ROOT>/common/ideas/`, `common/dynamic_modifiers/`, and `common/modifier_definitions/` for installed MD modifier uses and registration.
- `<MD_ROOT>/common/national_focus/00_generic.txt`, `05_russia.txt`, and `05_israel.txt` for native focus API patterns.
- `<MD_ROOT>/common/scripted_effects/00_money_system.txt` for an example of a formula reader; follow the current call path, not just the field definition.

These are version-sensitive references. Check that the installed MD path is active and that the source has not moved before using any anchor in findings.

## Soviet example: distinct effect owners

The implemented Soviet 1970 tree is a preferred project reference, not an unquestioned whitelist. Permanent sector modifiers map accumulated variables; `*_programme` modifiers have current-party/office-holder `enable` conditions. Timed burdens and one-time outcomes are separate categories. Classify ownership before prescribing cleanup: false `enable` can intentionally deactivate a retained programme without deleting earned variables. Trace authoritative office/party changes and refresh; verify runtime when possible.

Read `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt` (sectors from line 6, programmes from 183) and `COLDWAR_SOV_clear_gensec`/`COLDWAR_SOV_install_gensec_*` in emitted effects. Leadership change does not inherently reset permanent sector gains.

`cw_effects.py`'s `dyn_change` emits ensure-present -> native heading -> mapped variable change with stat tooltip -> refresh. Check all four in output and the actual custom consumer. Guard system-specific refresh on initialization; do not recalculate the world after every effect by default.

Compare design record, applicable `overrides/*.json`, compiler transformation, staged result and loaded script. An override is not final-value evidence. Top-level imports can rebuild output or mutate design data; inspect before execution.
