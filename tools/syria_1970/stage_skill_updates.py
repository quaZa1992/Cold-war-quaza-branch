"""Stage bounded skill amendments; installing outside the workspace is separate."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = Path('C:/Users/sonyz/.codex/skills')
DEST = HERE / 'skill_updates'

updates = {
    'mdcw-national-trees/SKILL.md': (
        '## Implement and prove the integration',
        'Read [runtime-presentation.md](references/runtime-presentation.md) when implementing guarded rewards, repairing missing effects, or responding to in-game screenshots/logs. It covers independent display/execution checks, script encoding and player-facing English.\n\n## Implement and prove the integration'),
    'mdcw-modifier-audit/SKILL.md': (
        'Static parsers, source searches, and local validators',
        'For unavailable or unaffordable focuses, audit the displayed reward independently of the guarded payout. In-game screenshots and parser errors take precedence over an earlier static PASS. See the presentation and parser checks in [references/modifier-effect-audit.md](references/modifier-effect-audit.md).\n\nStatic parsers, source searches, and local validators'),
    'mdcw-tree-layout/references/layout-method.md': (
        '## Geometry and visual review',
        '## Investigate reportedly missing focuses\n\nCompare the affected screenshot section with the approved design and emitted IDs, resolved coordinates, prerequisite groups, visibility and actual rewards. A total focus count cannot establish that a particular branch is complete. Small organizing sections may intentionally unlock decisions rather than grant passive modifiers; expose those real unlocks instead of adding filler focuses or invented buffs. Preserve approved gaps and grouping unless a layout change is authorized.\n\nMeasure the active `interface/nationalfocusview.gui` as well as the art. In the Syrian repair reference, native MD used a 96 by 130 grid, a 165 by 128 item container and a 147 by 20 name field with `hoi_16mbs`; the preview used 165 by 112 visible-art bounds. Those measurements describe that installation, not a universal engine constant. Label connector and visible-bounds approximations; a browser preview does not prove millimetre-identical engine rendering.\n\n## Geometry and visual review'),
    'mdcw-modifier-audit/references/modifier-effect-audit.md': (
        '## Establish units and stacking',
        '## Check parser acceptance and locked-focus previews\n\nAudit both the unconditional display and the actual guarded payout. For a guarded implementation, native `effect_tooltip = { ... }` can display material effects while `hidden_effect = { ... }` executes the eligibility/once-only logic. The display-only block must not be counted as a real grant by validators or scenario models. Conversely, a correct preview does not prove execution. Compare modifier amounts, cash, buildings, event outcomes and decision unlocks on both sides, including conditions that can change before completion.\n\nRecheck actual argument shapes, not just effect names. The Syrian repair exposed invalid scalar removal: native `remove_dynamic_modifier` uses `remove_dynamic_modifier = { modifier = ID }`. Locate the installed engine effects documentation and current MD examples before adapting the pattern.\n\nInspect raw bytes when logs reject an unexpected token at the beginning of otherwise normal scripts. In the Syrian case, leading UTF-8 BOMs in changed non-localization helper files caused native political helpers to fail to register; downstream unknown-effect errors were symptoms. Repair only affected files and fix their writers. Preserve the required localization encoding separately. Do not infer parser acceptance because a Python reader using `utf-8-sig` succeeded.\n\nUse a fresh game process/log after parser repairs. Record the log timestamp and whether it predates the changed files. A source PASS is not a post-repair engine test.\n\n## Establish units and stacking'),
}

manifest = []
for relative, (old, new) in updates.items():
    path = SOURCE / relative
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    assert text.count(old) == 1, relative
    output = DEST / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text.replace(old, new), encoding='utf-8', newline='\n')
    manifest.append({'relative': relative, 'previous_sha256': hashlib.sha256(raw).hexdigest()})

reference = '''# Runtime presentation and parser acceptance

Use this reference when focus rewards disappear from unavailable paths or a player's screenshot/log contradicts a static report. The Syria 1970 repair is evidence for these checks, not a requirement to copy its whole architecture.

## Display rewards independently from their guarded execution

A focus tooltip evaluates conditional reward branches in the current country state. Wrapping every material reward inside an `if` for party, funds or completion can leave an unavailable focus showing only a fallback paragraph. Test the hover before prerequisites, under a different government, without funds, when available and after completion.

Where current MD and engine documentation support it, use an unconditional native `effect_tooltip` containing the truthful material preview and a separate `hidden_effect` containing the guarded, once-only payout. Native Germany focus examples use `effect_tooltip` with real building/temp-variable/helper bodies. Recheck that example in the active MD version. Preserve conditional wording for genuinely conditional outcomes; do not promise every mutually exclusive event option.

Validate display and execution as separate paths. A display-only block is not a second factory, treasury charge or modifier grant. Trace its helpers and compare amounts, scopes, costs, buildings, decision unlocks and events with the actual payout. Keep lifecycle flags, cache refreshes, logging and deferred-programme bookkeeping out of the material preview. A deferred implementation message must not replace the focus's real rewards. Structural entries should truthfully describe their downstream choices or decision unlocks rather than inventing bonuses.

## Show political requirements, hide technical plumbing

Keep scenario identity, original-tag and initialization predicates executable but hidden through the native trigger presentation mechanism supported by that context, such as `hidden_trigger`. Localize meaningful party, leader, coalition, funding, formation and reform requirements. Do not expose raw flags or generic 'game initially started' lines to explain a national policy. Hidden technical checks must remain in the execution gate; removing their display does not authorize removing the condition.

## Accept the engine's evidence

Check actual argument syntax and encoding in addition to vocabulary. In the Syrian log, scalar dynamic-modifier removal was rejected; the supported form was `remove_dynamic_modifier = { modifier = ID }`. Changed non-localization scripts also contained leading UTF-8 BOM bytes that the game rejected, preventing shared native party helpers from registering. Inspect raw bytes; a BOM-stripping text reader can conceal the defect. Keep localization's encoding convention separate and repair only files within the authorized change. Fix the generator so rebuilding cannot reintroduce the error.

An actual screenshot or engine parser error overrides earlier claims based on static checks. Retain that evidence, identify the primary error before following downstream unknown-helper messages, and rerun the relevant validator after the repair. Restart the game fully and inspect a fresh log when possible; explicitly report when fresh engine verification has not occurred.

## Write descriptions for players

Use specific historical institutions, policy choices and practical burdens in English descriptions. Keep the native numerical reward tooltip separate from narrative. Avoid repeated 'benefits and costs apply' boilerplate, raw script names, array indexes and generator explanations. Cross-check each narrative against the implemented outcome and the actual historical actor; do not improve prose by inventing a new mechanic.

## Local repair anchors to reconfirm

- `tools/syria_1970/validate_tooltips.py`: independently compares 420 emitted reward previews and guarded helpers, checks raw encoding and modifier-removal syntax, and verifies the eight outlook entries against approved source. Its country-specific counts are not universal requirements.
- `tools/syria_1970/presentation.py`: separates meaningful eligibility labels from hidden scenario identity.
- `tools/syria_1970/script_encoding.py`: bounded repair of changed files, not a repository-wide recoding recipe.
- Current MD `common/national_focus/05_germany.txt` and installed `effects_documentation.md`: native presentation and effect argument forms. Source paths/line numbers vary with version.
'''
path = DEST / 'mdcw-national-trees/references/runtime-presentation.md'
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(reference, encoding='utf-8', newline='\n')
manifest.append({'relative': 'mdcw-national-trees/references/runtime-presentation.md', 'previous_sha256': None})
(DEST / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(f'Staged {len(manifest)} exact skill files in {DEST}')
