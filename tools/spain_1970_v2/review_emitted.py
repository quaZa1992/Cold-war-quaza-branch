# IMPERIA CW — Cold War: independent Spain v2 emitted-tree review helper.
"""Compare approved Spain v2 graph/localisation/reward signatures to emitted code.

Read-only. Uses the existing Vietnam 1970 Clausewitz subset parser and writes
only a review report under tools/spain_1970_v2.
"""
from __future__ import annotations

import json
import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools' / 'vietnam_1970'))
from script_ast import emit, first, parse  # noqa: E402

DESIGN = HERE / 'approved_design.json'
FOCUS_REL = Path('common/national_focus/COLDWAR_SPR_1970_focus.txt')
LOC_REL = Path('localisation/english/COLDWAR_SPR_v2_focus_l_english.yml')


def flat(rows):
    return [r for r in rows if not (r[0] == '_bare' and isinstance(r[2], list))]


def blocks(rows, key):
    return [v for k, _, v in rows if k == key and isinstance(v, list)]


def one(rows, key):
    return first(rows, key)


def focus_nodes(tree):
    result = {}
    for node in blocks(tree, 'focus'):
        ident = one(node, 'id')
        if ident:
            result[ident] = node
    return result


def resolve_positions(nodes):
    resolved, errors = {}, []

    def resolve(ident, stack=()):
        if ident in resolved:
            return resolved[ident]
        if ident in stack:
            errors.append({'id': ident, 'error': 'relative-position cycle'})
            return (None, None)
        node = nodes[ident]
        x, y = one(node, 'x'), one(node, 'y')
        anchor = one(node, 'relative_position_id')
        try:
            x, y = int(x), int(y)
        except (TypeError, ValueError):
            errors.append({'id': ident, 'error': 'missing/non-integer x or y'})
            return (None, None)
        if anchor:
            if anchor not in nodes:
                errors.append({'id': ident, 'error': f'missing anchor {anchor}'})
                return (None, None)
            ax, ay = resolve(anchor, stack + (ident,))
            if ax is None:
                return (None, None)
            x, y = x + ax, y + ay
        resolved[ident] = (x, y)
        return (x, y)

    for ident in nodes:
        resolve(ident)
    return resolved, errors


def prereq_groups(node):
    groups = []
    for block in blocks(node, 'prerequisite'):
        groups.append([v for k, _, v in block if k == 'focus'])
    return groups


def read_loc(text):
    # HOI4 English localisation is YAML-like and keys may be quoted.
    entries = {}
    for line in text.splitlines():
        m = re.match(r'^\s*"?([^"\s:]+)"?\s*:\d*\s*"(.*)"\s*$', line)
        if m:
            entries[m.group(1)] = m.group(2).replace('\\"', '"')
    return entries


def number(value):
    try:
        return f'{float(value):g}'
    except (TypeError, ValueError):
        return str(value)


def expected_signatures(effect):
    """Return source-level signatures for the approved reward type."""
    kind = effect.get('type')
    if kind == 'native_effect':
        name = effect.get('effect')
        args = effect.get('args')
        if isinstance(args, (int, float, str)):
            return [rf'\b{re.escape(name)}\s*=\s*{re.escape(number(args))}\b']
        return [rf'\b{re.escape(name)}\b']
    if kind == 'treasury':
        amount = effect.get('amount')
        return [r'\btreasury_change\s*=\s*-?\s*' + re.escape(number(amount)),
                r'\bmodify_treasury_effect\s*=\s*yes\b']
    if kind == 'modifier':
        key, amount = effect.get('key'), effect.get('amount')
        # Compiler previews represent modifier changes as a grouped backing variable
        # named COLDWAR_SPR_v2_<group>_<key> = amount.
        group = effect.get('_group')
        if group:
            return [rf'\bCOLDWAR_SPR_v2_{re.escape(group)}_{re.escape(key)}\s*=\s*{re.escape(number(amount))}\b']
        return [rf'\b{re.escape(key)}\b', rf'(?<![\w.]){re.escape(number(amount))}(?![\w.])']
    if kind == 'building':
        name = effect.get('building') or effect.get('type')
        level = effect.get('amount', effect.get('level'))
        sig = [rf'\btype\s*=\s*{re.escape(str(name))}\b'] if name else []
        if level is not None:
            sig.append(rf'\blevel\s*=\s*{re.escape(number(level))}\b')
        return sig
    if kind == 'research':
        sig = []
        for key in ('category', 'bonus', 'uses'):
            if effect.get(key) is not None:
                sig.append(rf'\b{key}\s*=\s*{re.escape(number(effect[key]))}\b')
        return sig
    if kind == 'experience':
        field = effect.get('field', effect.get('service', 'army') + '_experience')
        amount = effect.get('amount', effect.get('value'))
        return [rf'\b{re.escape(field)}\s*=\s*{re.escape(number(amount))}\b']
    if kind == 'decision':
        return []
    if kind == 'spirit_swap':
        return [re.escape(str(effect[k])) for k in ('remove', 'add', 'idea') if effect.get(k)]
    if kind == 'scripted_effect':
        return []
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=Path, help='review a compiler --stage directory instead of the loaded mod')
    parser.add_argument('--report', type=Path, default=HERE / 'review_emitted_report.json')
    args = parser.parse_args()
    source = args.stage if args.stage else ROOT
    focus_path = source / FOCUS_REL
    loc_path = source / LOC_REL
    design = json.loads(DESIGN.read_text(encoding='utf-8'))
    ast = parse(focus_path.read_text(encoding='utf-8-sig'))
    trees = blocks(ast, 'focus_tree')
    tree = trees[0] if trees else []
    emitted = focus_nodes(tree)
    approved = {n['id']: n for n in design['nodes']}
    positions, position_errors = resolve_positions(emitted)
    loc = read_loc(loc_path.read_text(encoding='utf-8-sig')) if loc_path.exists() else {}
    # Inspect only currently loaded v2 providers. Broad recursive scans are slow
    # and can pick up duplicate staging copies or retired implementations.
    runtime_paths = []
    for folder, pattern in (
        ('common/scripted_effects', 'COLDWAR_SPR_v2_*.txt'),
        ('common/decisions', 'COLDWAR_SPR_v2_*.txt'),
        ('common/ideas', 'COLDWAR_SPR_v2_*.txt'),
        ('common/dynamic_modifiers', 'COLDWAR_SPR_v2_*.txt'),
        ('events', 'COLDWAR_SPR_v2_*.txt'),
    ):
        directory = source / folder
        if directory.exists():
            runtime_paths.extend(directory.glob(pattern))
    runtime_text = '\n'.join(p.read_text(encoding='utf-8-sig') for p in sorted(set(runtime_paths)))
    runtime_symbols = set(re.findall(r'(?m)^\s*([A-Za-z][\w.]*)\s*=\s*\{', runtime_text))
    groups = {g['id']: g for g in design['groups']}
    report = {
        'approved_focus_count': len(approved),
        'emitted_focus_count': len(emitted),
        'missing_ids': sorted(set(approved) - set(emitted)),
        'unexpected_ids': sorted(set(emitted) - set(approved)),
        'position_errors': position_errors,
        'focuses': [],
    }
    for ident, spec in approved.items():
        node = emitted.get(ident)
        row = {'id': ident, 'issues': []}
        if node is None:
            report['focuses'].append(row)
            continue
        group = groups[spec['group']]
        xy = spec['xy']
        expected_xy = (group['offset'][0] + xy[0], group['offset'][1] + xy[1])
        actual_xy = positions.get(ident)
        row.update({'expected_xy': expected_xy, 'emitted_xy': actual_xy,
                    'expected_prerequisite_groups': spec.get('prerequisites', []),
                    'emitted_prerequisite_groups': prereq_groups(node),
                    'expected_icon': spec.get('icon'), 'emitted_icon': one(node, 'icon')})
        if actual_xy != expected_xy:
            row['issues'].append('position mismatch')
        if prereq_groups(node) != spec.get('prerequisites', []):
            row['issues'].append('prerequisite grouping mismatch')
        if one(node, 'icon') != spec.get('icon'):
            row['issues'].append('icon mismatch')
        title = loc.get(ident)
        desc = loc.get(ident + '_desc')
        row.update({'expected_title': spec.get('title'), 'emitted_title': title,
                    'expected_description': spec.get('description'), 'emitted_description': desc})
        if title != spec.get('title'):
            row['issues'].append('title localisation mismatch')
        if desc != spec.get('description'):
            row['issues'].append('description localisation mismatch')
        reward_blocks = blocks(node, 'completion_reward')
        # The visible preview and guarded runtime helper are separate blocks.
        rewards = ''
        if reward_blocks:
            preview_blocks = blocks(reward_blocks[0], 'effect_tooltip')
            rewards = emit(preview_blocks[0]) if preview_blocks else ''
        runtime_helper = 'COLDWAR_SPR_complete_' + ident.removeprefix('COLDWAR_SPR_')
        helper_present = bool(re.search(rf'\b{re.escape(runtime_helper)}\s*=\s*\{{', runtime_text))
        row['reward_signatures'] = []
        for i, effect in enumerate(spec.get('effects', [])):
            effect = dict(effect)
            effect['_group'] = spec['group']
            signatures = expected_signatures(effect)
            # Legal settlements express their distinct permanent package through
            # named ideas rather than the ordinary programme variables.
            if ident in {'COLDWAR_SPR_fundamental_settlement', 'COLDWAR_SPR_royal_executive',
                         'COLDWAR_SPR_parliamentary_settlement'} and effect.get('type') == 'modifier':
                signatures = []
            missing = [s for s in signatures if not re.search(s, rewards)]
            if effect.get('type') in {'decision', 'scripted_effect'} and not helper_present:
                missing.append('runtime helper ' + runtime_helper)
            decision_present = None
            if effect.get('type') == 'decision':
                effect_name = effect.get('id', '') + '_effect'
                decision_present = effect_name in runtime_symbols
                if not decision_present:
                    missing.append('unlock effect ' + effect_name)
            if effect.get('type') == 'scripted_effect':
                if f'{effect.get("effect", "")} = yes' not in runtime_text:
                    missing.append('runtime scripted effect ' + effect.get('effect', ''))
                if effect.get('effect') == 'increase_education_budget' and 'increase_education_budget = yes' not in rewards:
                    missing.append('guarded education-law effect preview')
            row['reward_signatures'].append({'index': i, 'type': effect.get('type'),
                                             'description': effect.get('description'),
                                             'preview_text': rewards,
                                             'runtime_helper_present': helper_present,
                                             'decision_provider_present': decision_present,
                                             'missing_signatures': missing})
            if missing:
                row['issues'].append(f'approved reward {i} source signature missing')
        report['focuses'].append(row)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Reviewed {len(approved)} approved focuses against {len(emitted)} emitted; report: {args.report}")
    print(f"Missing IDs: {len(report['missing_ids'])}; unexpected IDs: {len(report['unexpected_ids'])}; position errors: {len(position_errors)}; focuses with issues: {sum(bool(x['issues']) for x in report['focuses'])}")


if __name__ == '__main__':
    main()
