"""Independently audit visible focus rewards versus once-only execution.

Checks the emitted scripts, not the compiler's reward catalogue alone. A native
effect_tooltip displays effects without executing them; hidden_effect executes
effects without displaying them (installed engine documentation3644/4659).
This is source QA, not evidence that a currently running process reloaded files.
"""
from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import re

from validate_content import parse, first, vals, walk

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LOG = Path.home() / 'Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log'


def audit(root=ROOT):
    root = Path(root)
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    manifest = json.loads((root / 'tools/syria_1970/manifest.json').read_text(encoding='utf-8-sig'))
    nodes = {n['id']: n for n in manifest['nodes']}
    focus_path = root / 'common/national_focus/COLDWAR_SYR_1970_focus.txt'
    tree = first(parse(focus_path.read_text(encoding='utf-8-sig')), 'focus_tree', [])
    focuses = {first(f, 'id'): f for f in vals(tree, 'focus')}
    helper_bodies = {}
    hashes = {str(focus_path.relative_to(root)): hashlib.sha256(focus_path.read_bytes()).hexdigest()}
    for path in (root / 'common/scripted_effects').glob('COLDWAR_SYR*.txt'):
        raw = path.read_bytes()
        hashes[str(path.relative_to(root))] = hashlib.sha256(raw).hexdigest()
        for key, _, body in parse(raw.decode('utf-8-sig')):
            if isinstance(body, list):
                helper_bodies[key] = body

    def expand_focus_helpers(body, hidden, chain=frozenset()):
        """Only inline focus-local wrappers; national lifecycle calls remain calls."""
        out = []
        for key, op, value in body:
            if key == 'effect_tooltip' and hidden:
                continue
            if key == 'hidden_effect' and not hidden:
                continue
            if (value == 'yes' and key in helper_bodies and key not in chain and
                    key.startswith('COLDWAR_SYR_') and
                    any(key.startswith(focus + '_') for focus in focuses)):
                out.extend(expand_focus_helpers(helper_bodies[key], hidden, chain | {key}))
            else:
                out.append((key, op, expand_focus_helpers(value, hidden, chain) if isinstance(value, list) else value))
        return out

    def signatures(body, node):
        result = Counter()
        for key, _, value in walk(body):
            if key == 'add_to_variable' and isinstance(value, list):
                for var, _, amount in value:
                    if var.startswith(node['owner'] + '_'):
                        result[('programme', var, str(float(amount)))] += 1
            elif key == 'set_temp_variable' and isinstance(value, list):
                amount = first(value, 'treasury_change')
                if isinstance(amount, str) and re.fullmatch(r'-?\d+(?:\.\d+)?', amount):
                    result[('cash', str(float(amount)))] += 1
                for var in ('corp_change', 'pop_change'):
                    if first(value, var) is not None:
                        result[('tax', var, first(value, var))] += 1
            elif key == 'add_building_construction' and isinstance(value, list):
                result[('building', first(value, 'type'), first(value, 'level'), first(value, 'province', 'state'))] += 1
            elif key == 'country_event':
                result[('event', first(value, 'id') if isinstance(value, list) else value)] += 1
            elif key == 'unlock_decision_tooltip':
                result[('decision', value)] += 1
            elif key == 'custom_effect_tooltip' and isinstance(value, str) and value.endswith('_reform_tt'):
                result[('reform', value)] += 1
        return result

    unavailable_checks = 0
    preview_grants = 0
    structural_root_checks = 0
    localization = {}
    for path in (root / 'localisation/english').glob('COLDWAR_SYR*.yml'):
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for key, encoded in re.findall(r'^\s+(\S+):\d+\s+(".*")\s*$', path.read_text(encoding='utf-8-sig'), re.M):
            try:
                localization[key] = json.loads(encoded)
            except json.JSONDecodeError:
                errors.append('Invalid English localization: ' + key)

    def check_requirement_presentation(body, ident, visible=True):
        for key, _, value in body:
            if visible and key in ('IMP_is_1970_scenario', 'has_start_date', 'original_tag'):
                errors.append('Technical scenario requirement still visible: ' + ident + '/' + key)
            if isinstance(value, list):
                child_visible = visible and key not in ('hidden_trigger', 'custom_trigger_tooltip', 'custom_override_tooltip')
                check_requirement_presentation(value, ident, child_visible)

    for ident, body in focuses.items():
        node = nodes.get(ident)
        if not node:
            errors.append('Focus absent from implementation manifest: ' + ident)
            continue
        completion = first(body, 'completion_reward', [])
        check_requirement_presentation(first(body, 'available', []), ident)
        display_blocks = vals(completion, 'effect_tooltip')
        execution_blocks = vals(completion, 'hidden_effect')
        check(len(display_blocks) == 1, 'Expected one unconditional native effect_tooltip: ' + ident)
        check(len(execution_blocks) == 1, 'Expected one hidden execution block: ' + ident)
        # No real payout is permitted beside the display-only and hidden blocks.
        check(all(k in ('effect_tooltip', 'hidden_effect') for k, _, _ in completion),
              'Execution or conditional display leaked outside the presentation boundary: ' + ident)
        if not display_blocks or not execution_blocks:
            continue
        display = expand_focus_helpers(display_blocks[0], hidden=False)
        execution = expand_focus_helpers(execution_blocks[0], hidden=True)
        direct = [k for k, _, _ in display]
        check(bool(display), 'Empty focus reward preview: ' + ident)
        check(direct != ['if'], 'Preview remains gated by a single conditional branch: ' + ident)
        for key, _, value in walk(display):
            check(not (key == 'custom_effect_tooltip' and value == 'COLDWAR_SYR_deferred_tt'),
                  'Deferred fallback still visible as the reward: ' + ident)
            check(not (key in ('IMP_is_1970_scenario', 'has_start_date', 'original_tag')),
                  'Technical scenario condition appears inside reward presentation: ' + ident)
            check(not (key == 'COLDWAR_SYR_refresh_programmes' and value == 'yes'),
                  'Lifecycle refresh appears in reward preview: ' + ident)
            bookkeeping_flag = (key in ('set_country_flag', 'clr_country_flag') and isinstance(value, str)
                                and value.endswith(('_implemented', '_pending', '_earned')))
            check(not (bookkeeping_flag or key == 'log'),
                  'Internal lifecycle bookkeeping appears in reward preview: ' + ident)
        preview_signature = signatures(display, node)
        execution_signature = signatures(execution, node)
        check(preview_signature == execution_signature,
              'Displayed/executed reward mismatch: ' + ident +
              ' preview_only=' + str(list((preview_signature - execution_signature).elements())) +
              ' execution_only=' + str(list((execution_signature - preview_signature).elements())))
        for modifier, amount in node['modifiers'].items():
            signature = ('programme', node['owner'] + '_' + modifier, str(float(amount)))
            check(preview_signature[signature] == 1, 'Unavailable focus loses/duplicates modifier preview: ' + ident + '/' + modifier)
            check(execution_signature[signature] == 1, 'Modifier payout missing/duplicated: ' + ident + '/' + modifier)
            preview_grants += 1
        if node['treasury_cost_bn']:
            signature = ('cash', str(-float(node['treasury_cost_bn'])))
            check(preview_signature[signature] == 1, 'Unavailable focus loses treasury cost preview: ' + ident)
            check(execution_signature[signature] == 1, 'Cash payout duplicated/missing: ' + ident)
        choices_tip = ident + '_policy_choices_tt'
        check(('custom_effect_tooltip', '=', choices_tip) not in display,
              'Branch-opening placeholder still substitutes for a material reward: '+ident)
        if ident in manifest['contract'].get('entry_reward_amendments', {}):
            check(bool(node['modifiers']), 'Entry focus still lacks its approved material bonus: '+ident)
            structural_root_checks += 1
        # Payout must remain protected independently from the unconditional UI.
        implementation = helper_bodies.get(ident + '_implement', [])
        guard = first(first(implementation, 'if', []), 'limit', [])
        for key, _, value in walk(first(body, 'available', [])+guard):
            check(not (key == 'check_variable' and isinstance(value, list) and first(value, 'treasury') is not None),
                  'Focus still requires cash instead of allowing native borrowing: '+ident)
        expected_guard = ('NOT', '=', [('has_country_flag', '=', ident + '_implemented')])
        check(expected_guard in guard, 'Once-only implementation guard missing: ' + ident)
        check(any(k == 'if' for k, _, _ in execution_blocks[0]), 'Runtime affordability/authority branch missing: ' + ident)
        unavailable_checks += 1

    script_paths = list((root / 'common').rglob('COLDWAR_SYR*.txt')) + list((root / 'events').glob('COLDWAR_SYR*.txt'))
    shared = [
        'common/scripted_effects/00_MD_politicsview_scripted_effects.txt',
        'common/scripted_effects/00_leader_setup_scripted_effects.txt',
        'common/scripted_effects/00_yearly_effects.txt',
        'common/scripted_triggers/99_CHI_scripted_triggers.txt',
        'common/game_rules/00_game_rules.txt',
    ]
    for path in script_paths + [root / rel for rel in shared]:
        if not path.exists():
            continue
        raw = path.read_bytes()
        check(b'\xef\xbb\xbf' not in raw, 'Non-localization script contains UTF-8 BOM rejected by actual engine: ' + str(path.relative_to(root)))
        check(not re.search(rb'\b_(?:bare|list)\s*=', raw), 'AST sentinel leaked into loaded game script: '+str(path.relative_to(root)))
        try:
            ast = parse(raw.decode('utf-8-sig'))
        except ValueError as exc:
            errors.append(str(path.relative_to(root)) + ': ' + str(exc))
            continue
        for key, _, value in walk(ast):
            if key == 'remove_dynamic_modifier':
                check(isinstance(value, list) and isinstance(first(value, 'modifier'), str),
                      'Engine rejects scalar remove_dynamic_modifier: ' + str(path.relative_to(root)))

    # Compare the small optional organising branch by actual IDs, geometry,
    # prerequisites and material decision rewards; a total count is insufficient.
    outlook_nodes = [n for n in manifest['nodes'] if n['group'] == 'outlooks']
    approved = json.loads((root / 'tools/syria_1970/design_source.json').read_text(encoding='utf-8-sig'))
    outlook_approved = {n['id']: n for n in approved['nodes'] if n['group'] == 'outlooks'}
    outlook_summary = []

    def emitted_xy(ident, seen=frozenset()):
        if ident not in focuses or ident in seen:
            errors.append('Missing/cyclic outlook positioning anchor: ' + ident)
            return [float('nan'), float('nan')]
        body = focuses[ident]
        xy = [float(first(body, 'x')), float(first(body, 'y'))]
        anchor = first(body, 'relative_position_id')
        if anchor:
            parent = emitted_xy(anchor, seen | {ident})
            xy = [a + b for a, b in zip(xy, parent)]
        return xy

    for node in outlook_nodes:
        ident = node['id']
        old = outlook_approved[ident]
        body = focuses.get(ident, [])
        xy = emitted_xy(ident)
        prerequisites = [vals(row, 'focus') for row in vals(body, 'prerequisite')]
        display = expand_focus_helpers(first(first(body, 'completion_reward', []), 'effect_tooltip', []), hidden=False)
        unlocks = [v for k, _, v in walk(display) if k == 'unlock_decision_tooltip']
        check(xy == old['xy'] and prerequisites == old['prerequisites'],
              'Optional outlook geometry/connector changed: ' + ident)
        check(bool(node.get('decision_unlocks')), 'Optional outlook focus has no decision reward: ' + ident)
        check(unlocks == node.get('decision_unlocks', []), 'Optional outlook decision reward is not shown: ' + ident)
        outlook_summary.append({'id': ident, 'emitted_xy': xy, 'emitted_prerequisites': prerequisites,
                                'emitted_visible_decision_unlocks': unlocks})
    observed_log_issues = []
    if LOG.exists():
        for line in LOG.read_text(encoding='utf-8-sig', errors='replace').splitlines():
            if ('COLDWAR_SYR' in line or '00_MD_politicsview_scripted_effects' in line or
                    '00_leader_setup_scripted_effects' in line) and ('Error' in line or 'Invalid' in line):
                observed_log_issues.append(line)
    return {
        'status': 'FAIL' if errors else 'PASS', 'errors': list(dict.fromkeys(errors)),
        'focuses_checked': len(focuses), 'unavailable_focus_display_boundaries_checked': unavailable_checks,
        'display_and_payout_modifier_pairs_checked': preview_grants,
        'entry_focus_bonus_packages_checked': structural_root_checks,
        'outlooks': outlook_summary,
        'native_documentation': {'effect_tooltip': 'effects_documentation.md:3644–3651: Shows just tooltip of effects',
                                 'hidden_effect': 'effects_documentation.md:4659–4666: Effect not shown in tooltips',
                                 'remove_dynamic_modifier': 'effects_documentation.md:5978–5989: block form with modifier field'},
        'source_hashes': hashes,
        'observed_previous_engine_log_errors': observed_log_issues,
        'engine_tested_after_changes': False,
        'limitations': 'Source presentation boundaries and payout parity only. The log belongs to the last game process and may predate current files. Restart/reload and unavailable/affordable/completed focus hovers must be verified in HOI4.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('outlooks', 'source_hashes', 'observed_previous_engine_log_errors')}, ensure_ascii=True, indent=2))
    raise SystemExit(bool(result['errors']))


if __name__ == '__main__':
    main()
