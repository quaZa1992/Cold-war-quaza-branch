"""Independent source, graph and geometry audit for the approved Syrian 1970 tree.

This module is deliberately separate from the compiler. It parses emitted Clausewitz
files and compares them to the approved catalogue; importing it never writes files.
No result from this script establishes HOI4 runtime or save compatibility.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
GAME_ROOT = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')
DEFAULT_DESIGN = Path(r"C:\Users\sonyz\.codex\visualizations\2026\10\18\01a14f68-6ecc-7ec1-bc09-11cc54d8ee44\syria-1970-concept\design.json")
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+')


def parse(source):
    """Preserve repeated keys, prerequisite groups, scopes and comparison operators."""
    ts = [m[0] for m in TOKEN.finditer(source) if not m[0].startswith('#')]
    cursor = 0
    if any(x in ('>=', '<=', '!=') for x in ts):
        raise ValueError('unsupported compound comparison; use native compare/NOT syntax')

    def block(nested=False):
        nonlocal cursor
        result = []
        while cursor < len(ts):
            key = ts[cursor]
            cursor += 1
            if key == '}':
                if not nested:
                    raise ValueError('unexpected closing brace')
                return result
            if key == '{':
                result.append(('_list', '=', block(True)))
            elif cursor < len(ts) and ts[cursor] in ('=', '>', '<'):
                op = ts[cursor]
                cursor += 1
                if cursor == len(ts):
                    raise ValueError('missing value after ' + key)
                value = ts[cursor]
                cursor += 1
                if value == '{':
                    value = block(True)
                elif value == '}':
                    raise ValueError('missing value before closing brace')
                result.append((key, op, value))
            else:
                result.append(('_bare', '=', key))
        if nested:
            raise ValueError('unclosed block')
        return result

    return block()


def vals(block, key):
    return [v for k, _, v in block if k == key]


def first(block, key, default=None):
    return next(iter(vals(block, key)), default)


def walk(block):
    for key, op, value in block:
        yield key, op, value
        if isinstance(value, list):
            yield from walk(value)


def plain(value):
    return value[1:-1] if isinstance(value, str) and value.startswith('"') and value.endswith('"') else value


def audit(root=ROOT, design_path=DEFAULT_DESIGN):
    root = Path(root)
    design_path = Path(design_path)
    design = json.loads(design_path.read_text(encoding='utf-8-sig'))
    expected = {n['id']: n for n in design['nodes']}
    policy = json.loads((root/'tools/syria_1970/runtime_policy.json').read_text(encoding='utf-8'))
    amendments = dict(policy['entry_rewards'])
    additional = root/'tools/syria_1970/additional_entry_rewards.json'
    if additional.exists():
        amendments.update(json.loads(additional.read_text(encoding='utf-8')))
    for ident, amendment in amendments.items():
        expected[ident]['modifiers'] = amendment['modifiers'].copy()
    runtime_path = root / 'tools/syria_1970/manifest.json'
    runtime = json.loads(runtime_path.read_text(encoding='utf-8-sig')) if runtime_path.exists() else {}
    # The user subsequently approved a2–7bn focus cost schedule. Geometry and
    # rewards still compare to the approved design; cash debits compare to the
    # compiler's runtime manifest so the earlier design cannot override the user.
    runtime_costs = runtime.get('focus_costs_bn', {})
    if isinstance(runtime_costs, list):
        runtime_costs = {row['id']: row.get('treasury_cost_bn', row.get('cost_bn')) for row in runtime_costs}
    if runtime.get('nodes'):
        runtime_costs.update({node['id']: node['treasury_cost_bn'] for node in runtime['nodes']})
    errors, warnings = [], []

    def check(condition, message):
        if not condition:
            errors.append(message)

    # Only country-owned outputs are required to be parseable here. Native helpers
    # are indexed separately; unrelated pre-existing syntax is not in audit scope.
    sources, asts, hashes = {}, {}, {}
    for directory in ('common/national_focus', 'common/scripted_effects',
                      'common/scripted_triggers', 'common/dynamic_modifiers',
                      'common/ideas', 'common/decisions', 'common/decisions/categories',
                      'common/on_actions', 'common/opinion_modifiers', 'events', 'interface'):
        folder = root / directory
        if not folder.exists():
            continue
        for path in folder.glob('*'):
            if not path.is_file() or 'COLDWAR_SYR' not in path.name or path.suffix not in ('.txt', '.gfx'):
                continue
            rel = path.relative_to(root).as_posix()
            raw = path.read_bytes()
            source = raw.decode('utf-8-sig')
            sources[rel] = source
            hashes[rel] = hashlib.sha256(raw).hexdigest()
            try:
                asts[rel] = parse(source)
            except ValueError as exc:
                errors.append(f'{rel}: {exc}')
            check(not re.search(r'#\s*(?:NEW|TODO|FIXME|DESIGN ONLY|PROPOSED)\b', source),
                  f'Unfinished design placeholder in {rel}')

    trees = [(rel, tree) for rel, ast in asts.items()
             if rel.startswith('common/national_focus/') for tree in vals(ast, 'focus_tree')]
    check(len(trees) == 1, f'Expected one Syrian tree; found {len(trees)}')
    tree = trees[0][1] if trees else []
    focus_list = vals(tree, 'focus')
    focusmap = {first(f, 'id'): f for f in focus_list}
    check(len(focus_list) == len(focusmap), 'Duplicate emitted focus IDs')
    check(set(focusmap) == set(expected), 'Focus ID set mismatch: missing=' + str(sorted(set(expected) - set(focusmap))) +
          ' extra=' + str(sorted(set(focusmap) - set(expected))))
    check(first(tree, 'reset_on_civilwar') == 'no', 'Focus progress resets in civil war')

    resolved = {}

    def resolve(ident, active=frozenset()):
        if ident in resolved:
            return resolved[ident]
        if ident in active:
            errors.append('Cyclic focus position: ' + ident)
            return (float('nan'), float('nan'))
        if ident not in focusmap:
            errors.append('Missing focus position anchor: ' + str(ident))
            return (float('nan'), float('nan'))
        item = focusmap[ident]
        try:
            x, y = float(first(item, 'x')), float(first(item, 'y'))
        except (ValueError, TypeError):
            errors.append('Non-numeric position: ' + ident)
            return (float('nan'), float('nan'))
        anchor = first(item, 'relative_position_id')
        if anchor:
            ax, ay = resolve(anchor, active | {ident})
            x, y = x + ax, y + ay
        resolved[ident] = (x, y)
        return resolved[ident]

    native_helpers = set()
    helper_bodies = {}
    for directory in ('common/scripted_effects', 'common/scripted_triggers'):
        for path in (root / directory).glob('*.txt'):
            source = path.read_text(encoding='utf-8-sig')
            native_helpers.update(re.findall(r'(?m)^(\w+)\s*=\s*\{', source))
    for rel, ast in asts.items():
        if rel.startswith(('common/scripted_effects/', 'common/scripted_triggers/')):
            helper_bodies.update({k: v for k, _, v in ast if isinstance(v, list)})

    def expand(body, chain=frozenset()):
        """Follow emitted country helpers, retaining scopes and branches for audit."""
        result = []
        for key, op, value in body:
            if key == 'effect_tooltip':
                # Display-only effects are checked separately against execution;
                # they must not be counted as a second real programme grant.
                continue
            if value == 'yes' and key in helper_bodies and key not in chain:
                result.extend(expand(helper_bodies[key], chain | {key}))
            else:
                result.append((key, op, expand(value, chain) if isinstance(value, list) else value))
        return result

    loc, loc_paths = {}, []
    for path in (root / 'localisation/english').glob('*COLDWAR_SYR*.yml'):
        loc_paths.append(path)
        raw = path.read_bytes()
        check(raw.startswith(b'\xef\xbb\xbf'), 'Localization needs UTF-8 BOM: ' + path.name)
        source = raw.decode('utf-8-sig')
        check(source.startswith('l_english:'), 'English localization header absent: ' + path.name)
        for key, value in re.findall(r'^\s+(\S+):\d+\s+(".*")\s*$', source, re.M):
            check(key not in loc, 'Duplicate localization key: ' + key)
            try:
                loc[key] = json.loads(value)
            except json.JSONDecodeError:
                errors.append('Invalid localization quoting: ' + key)
        check(not re.search(r'â[€™€œ“”–—]|Ã[¤¶¼Ÿ]|\ufffd', source), 'Mojibake in localization: ' + path.name)
    check(bool(loc_paths), 'No Syrian English localization generated')
    for language in ('german', 'french', 'russian'):
        check(not list((root / 'localisation' / language).glob('*COLDWAR_SYR*.yml')),
              'Unrequested localization generated: ' + language)

    sprites = set()
    sprite_paths = {}
    # Interface is not replace_path: base sprites remain available unless a mod
    # file replaces the same relative file. Mod registrations take precedence.
    sprite_files = [p for p in (GAME_ROOT / 'interface').glob('*.gfx') if not (root / 'interface' / p.name).exists()]
    sprite_files += list((root / 'interface').glob('*.gfx'))
    for path in sprite_files:
        source = path.read_text(encoding='utf-8-sig')
        sprites.update(re.findall(r'name\s*=\s*"([^"]+)"', source))
        for name, texture in re.findall(r'name\s*=\s*"([^"]+)"[^}]*?texturefile\s*=\s*"([^"]+)"', source, re.I):
            sprite_paths[name] = texture

    dynamic = {k: body for rel, ast in asts.items() if rel.startswith('common/dynamic_modifiers/')
               for k, _, body in ast if isinstance(body, list)}
    opinions = {k: body for rel, ast in asts.items() if rel.startswith('common/opinion_modifiers/')
                for container in vals(ast, 'opinion_modifiers') for k, _, body in container if isinstance(body, list)}
    ideas = {}
    for rel, ast in asts.items():
        if rel.startswith('common/ideas/'):
            for container in vals(ast, 'ideas'):
                for country in vals(container, 'country'):
                    ideas.update({k: v for k, _, v in country if isinstance(v, list)})
    event_list = [body for rel, ast in asts.items() if rel.startswith('events/') for body in vals(ast, 'country_event')]
    events = {first(body, 'id'): body for body in event_list}
    check(len(events) == len(event_list), 'Duplicate country-event IDs')
    decision_list = [(k, v) for rel, ast in asts.items() if rel.startswith('common/decisions/')
                 and '/categories/' not in rel for _, _, category in ast if isinstance(category, list)
                 for k, _, v in category if isinstance(v, list) and k.startswith('COLDWAR_SYR_decision_')]
    decisions = dict(decision_list)
    check(len(decisions) == len(decision_list), 'Duplicate decision IDs')
    wanted_decisions = {d['id'] for d in design['decisions']}
    check(wanted_decisions <= set(decisions), 'Missing approved decisions: ' + str(sorted(wanted_decisions - set(decisions))))
    wanted_events = {e['id'] for e in design.get('events', [])}
    check(wanted_events <= set(events), 'Missing approved events: ' + str(sorted(wanted_events - set(events))))
    for rel, ast in asts.items():
        if rel.startswith('common/decisions/categories/'):
            bodies = [(key, body, 'GFX_decision_category_') for key, _, body in ast if isinstance(body, list)]
        elif rel.startswith('common/decisions/'):
            bodies = [(key, body, 'GFX_decision_') for _, _, category in ast if isinstance(category, list)
                      for key, _, body in category if isinstance(body, list) and key.startswith('COLDWAR_SYR_')]
        elif rel.startswith('common/ideas/'):
            bodies = [(key, body, 'GFX_idea_') for key, body in ideas.items()]
        else:
            bodies = []
        for ident, body, prefix in bodies:
            key = 'picture' if prefix == 'GFX_idea_' else 'icon'
            ref = plain(first(body, key, ''))
            if ref:
                sprite = ref if ref.startswith('GFX_') else prefix + ref
                check(sprite in sprites, 'Missing ' + key + ' sprite: ' + ident + '/' + sprite)
    for rel, ast in asts.items():
        for key, _, value in walk(ast):
            if key == 'picture' and isinstance(value, str):
                ref = plain(value)
                if ref.startswith('gfx/'):
                    check((root / ref).exists() or (GAME_ROOT / ref).exists(), 'Missing portrait/texture: ' + ref)
                elif ref.startswith('GFX_'):
                    check(ref in sprites, 'Missing event sprite: ' + ref)

    modifiers_checked = 0
    expected_gates = {}
    for group in design['groups']:
        expected_gates[group['id']] = parse(group['gate'])
    for ident, body in focusmap.items():
        if ident not in expected:
            continue
        node = expected[ident]
        check(tuple(node['xy']) == resolve(ident), 'Changed approved coordinates: ' + ident)
        actual_rows = [vals(row, 'focus') for row in vals(body, 'prerequisite')]
        check(actual_rows == node['prerequisites'], 'Changed grouped prerequisites: ' + ident)
        excluded = sorted(v for row in vals(body, 'mutually_exclusive') for v in vals(row, 'focus'))
        check(excluded == sorted(node['mutually_exclusive']), 'Changed focus exclusions: ' + ident)
        for other in excluded:
            reciprocal = [v for row in vals(focusmap.get(other, []), 'mutually_exclusive') for v in vals(row, 'focus')]
            check(ident in reciprocal, 'Asymmetric exclusion: ' + ident + '/' + other)
        check(str(first(body, 'cost')) == str(node['cost']), 'Changed focus duration: ' + ident)
        icon = plain(first(body, 'icon', ''))
        approved_icon = node['icon'] if node['icon'].startswith('GFX_') else 'GFX_goal_' + node['icon']
        check(icon == approved_icon or icon == node['icon'], 'Changed approved icon: ' + ident + ': ' + icon)
        check(icon in sprites, 'Missing native focus sprite: ' + icon)
        if icon in sprite_paths:
            check((root / sprite_paths[icon]).exists(), 'Missing focus texture: ' + sprite_paths[icon])
        check(ident in loc and ident + '_desc' in loc, 'Missing focus title/description: ' + ident)
        check(first(body, 'cancel_if_invalid') == 'yes', 'Missing cancellation guard: ' + ident)
        reward = expand(first(body, 'completion_reward', []))
        avail = expand(first(body, 'available', []))
        avail_walk = list(walk(avail))
        for key, op, value in walk(expected_gates[node['group']]):
            if key not in ('OR', 'AND', 'NOT'):
                check((key, op, value) in avail_walk, 'Missing governing gate ' + key + ' in ' + ident)
        for key, expected_value in node['modifiers'].items():
            var = node['owner'] + '_' + key
            grants = [first(v, var) for k, _, v in walk(reward)
                      if k == 'add_to_variable' and isinstance(v, list) and first(v, var) is not None]
            check(len(grants) == 1 and math.isclose(float(grants[0]), float(expected_value), abs_tol=1e-8),
                  'Missing/changed/duplicate programme grant: ' + ident + '/' + key)
            mapping = first(dynamic.get(node['owner'], []), key)
            check(mapping == var, 'Missing dynamic consumer: ' + node['owner'] + '/' + key)
            modifiers_checked += 1
        approved_cost = runtime_costs.get(ident, node['treasury_cost_bn'])
        if approved_cost:
            charges = [first(v, 'treasury_change') for k, _, v in walk(reward)
                       if k == 'set_temp_variable' and isinstance(v, list) and first(v, 'treasury_change') is not None]
            check(any(isinstance(x, str) and re.fullmatch(r'-?\d+(?:\.\d+)?', x) and
                      math.isclose(float(x), -approved_cost, abs_tol=1e-8) for x in charges),
                  'Missing/changed approved treasury expense: ' + ident)
            treasury_guards = [v for k, _, v in walk(avail) if k == 'check_variable' and isinstance(v, list)
                               and any(a == 'treasury' and b == '>' for a, b, _ in v)]
            check(not treasury_guards, 'Focus still prevents native debt financing: ' + ident)
        for group in actual_rows:
            check(all(parent in focusmap for parent in group), 'Unresolved prerequisite: ' + ident)

    # Graph fixed point separately preserves AND between blocks and OR inside each.
    completed = set()
    while True:
        additions = {ident for ident, body in focusmap.items() if ident not in completed and
                     all(any(p in completed for p in vals(row, 'focus')) for row in vals(body, 'prerequisite'))}
        if not additions:
            break
        completed |= additions
    check(completed == set(focusmap), 'Cyclic/unreachable prerequisite graph: ' + str(sorted(set(focusmap) - completed)))

    # Complete card bounds and orthogonal connector approximation are based on the
    # approved preview's measured model; engine routing remains explicitly untested.
    rects = {ident: (xy[0] * 96 + 120, xy[1] * 130 + 110,
                     xy[0] * 96 + 285, xy[1] * 130 + 222) for ident, xy in resolved.items()}
    collisions, connector_hits = [], []
    items = list(rects.items())
    for i, (a, aa) in enumerate(items):
        for b, bb in items[i + 1:]:
            if max(aa[0], bb[0]) < min(aa[2], bb[2]) and max(aa[1], bb[1]) < min(aa[3], bb[3]):
                collisions.append((a, b))

    def hits(segment, rect):
        x1, y1, x2, y2 = segment
        if x1 == x2:
            return rect[0] < x1 < rect[2] and max(min(y1, y2), rect[1]) < min(max(y1, y2), rect[3])
        return rect[1] < y1 < rect[3] and max(min(x1, x2), rect[0]) < min(max(x1, x2), rect[2])

    for ident, body in focusmap.items():
        if ident not in rects:
            continue
        bb = rects[ident]
        for row in vals(body, 'prerequisite'):
            for parent in vals(row, 'focus'):
                if parent not in rects:
                    continue
                aa = rects[parent]
                x1, y1, x2, y2 = aa[0] + 82.5, aa[3], bb[0] + 82.5, bb[1]
                mid = (y1 + y2) / 2
                segments = ((x1, y1, x1, mid), (x1, mid, x2, mid), (x2, mid, x2, y2))
                for other, rect in rects.items():
                    if other not in (parent, ident) and any(hits(s, rect) for s in segments):
                        connector_hits.append((parent, ident, other))
    check(not collisions, 'Card collisions: ' + str(collisions[:10]))
    check(not connector_hits, 'Connector/card collisions: ' + str(connector_hits[:10]))

    # Transitive source references and provider completeness.
    flags_read, flags_set = set(), set()
    for rel, ast in asts.items():
        for key, _, value in walk(ast):
            if key.startswith('COLDWAR_SYR_') and value == 'yes':
                check(key in native_helpers, 'Undefined Syria helper/trigger: ' + key + ' in ' + rel)
            if key == 'has_country_flag' and isinstance(value, str) and value.startswith('COLDWAR_SYR_'):
                flags_read.add(value)
            if key == 'set_country_flag':
                flag = first(value, 'flag', '') if isinstance(value, list) else value
                if flag.startswith('COLDWAR_SYR_'):
                    flags_set.add(flag)
            if key in ('has_completed_focus', 'relative_position_id') and isinstance(value, str) and value.startswith('COLDWAR_SYR_'):
                check(value in focusmap, 'Unknown Syrian focus: ' + value)
            if key in ('add_ideas', 'remove_ideas', 'has_idea', 'idea') and isinstance(value, str) and value.startswith('COLDWAR_SYR_'):
                check(value in ideas, 'Unknown Syrian idea: ' + value + ' in ' + rel)
            if key == 'modifier' and isinstance(value, str) and value.startswith('COLDWAR_SYR_'):
                check(value in dynamic or value in opinions, 'Unknown Syrian dynamic/opinion modifier: ' + value)
            if key == 'country_event' and isinstance(value, list):
                event = first(value, 'id', '')
                if event.startswith('COLDWAR_SYR'):
                    check(event in events, 'Unknown Syrian event: ' + event)
            if key in ('custom_effect_tooltip', 'custom_trigger_tooltip', 'tooltip', 'name', 'title', 'desc', 'localization_key') and isinstance(value, str):
                ref = plain(value)
                if ref.startswith('COLDWAR_SYR'):
                    check(ref in loc, 'Missing English localization: ' + ref + ' in ' + rel)
    check(flags_read <= flags_set, 'Read flags with no provider: ' + str(sorted(flags_read - flags_set)))
    for ident in decisions:
        check(ident in loc and ident + '_desc' in loc, 'Missing decision localization: ' + ident)
    for ident, body in events.items():
        check(first(body, 'is_triggered_only') == 'yes', 'Event may fire spontaneously: ' + ident)
    for spirit in design['starting_spirits']:
        check(spirit['id'] in dynamic or spirit['id'] in ideas, 'Missing starting spirit: ' + spirit['id'])

    # Explicit native mechanics invariants catch known implementation pitfalls.
    joined = '\n'.join(sources.values())
    check('mdcw_cw_on_war_relation = yes' not in joined, 'Duplicate native Cold War war shock')
    check(not re.search(r'type\s*=\s*(?:renewable_powerplant|annex)\b', joined), 'Invented building/wargoal type')
    check(not re.search(r'\b(?:white_peace|declare_war_on)\s*=', joined), 'Automatic declaration/peace in Syrian content')
    goals = [(first(v, 'type'), first(v, 'expire')) for ast in asts.values() for k, _, v in walk(ast)
             if k == 'create_wargoal' and isinstance(v, list)]
    check(('take_state_focus', '365') in goals and ('annex_everything', '365') in goals,
          'Missing owner-aware365-day Israel wargoal types')
    check('COLDWAR_SYR_refresh_programmes' in helper_bodies, 'Programme refresh provider missing')
    check('COLDWAR_SYR_update_operation_costs' in helper_bodies, 'GDP operation cost provider missing')
    # A negotiated agreement and its command-implementation focus are distinct.
    # Evaluate the emitted spirit-clearing conditions rather than the compiler.
    recompute = helper_bodies.get('COLDWAR_SYR_recompute_starting_spirits', [])
    command_clear_conditions = []
    for key, _, body in walk(recompute):
        if key == 'if' and isinstance(body, list) and any(
                k == 'set_variable' and isinstance(v, list) and
                first(v, 'COLDWAR_SYR_divided_command_political_power_factor') == '0'
                for k, _, v in body):
            command_clear_conditions.append(first(body, 'limit', []))

    def flag_condition(body, flags):
        outcomes = []
        for key, _, value in body:
            if key == 'has_country_flag':
                outcomes.append(value in flags)
            elif key == 'AND':
                outcomes.append(flag_condition(value, flags))
            elif key == 'OR':
                outcomes.append(any(flag_condition([item], flags) for item in value))
            elif key == 'NOT':
                outcomes.append(not any(flag_condition([item], flags) for item in value))
            else:
                raise ValueError('Unsupported command-spirit condition: ' + key)
        return all(outcomes)

    if command_clear_conditions:
        prefix = 'COLDWAR_SYR_'
        command_cases = [
            (set(), False, 'unreformed start'),
            ({prefix + 'dual_command_resolved'}, False, 'agreement without implementation'),
            ({prefix + 'opening_settlement_implemented'}, False, 'implementation without agreement'),
            ({prefix + 'dual_command_resolved', prefix + 'opening_settlement_implemented'}, True, 'completed settlement'),
            ({prefix + 'parliament_05_implemented'}, True, 'civilian constitution'),
            ({prefix + 'military_transfer_agreed'}, True, 'negotiated civilian transfer'),
        ]
        try:
            for flags, expected_clear, title in command_cases:
                check(any(flag_condition(c, flags) for c in command_clear_conditions) == expected_clear,
                      'Divided-command spirit regression: ' + title)
        except ValueError as exc:
            errors.append(str(exc))
    else:
        errors.append('No executable divided-command reform found')
    for rel, source in sources.items():
        if 'clear_campaign' in source:
            for key, body in helper_bodies.items():
                if 'clear_campaign' in key:
                    check(not any(k == 'remove_ideas' and v == 'COLDWAR_SYR_war_bridge_credit' for k, _, v in walk(body)),
                          'Demobilization erases bridge-credit interest liability')
    for group in design['groups']:
        owner = group['owner']
        if not any(n['modifiers'] for n in design['nodes'] if n['group'] == group['id']):
            continue
        check(owner in dynamic, 'Missing programme definition: ' + owner)
        if group['kind'] != 'national' and owner in dynamic:
            enabled = list(walk(expand(first(dynamic[owner], 'enable', []))))
            for key, op, value in walk(parse(group['gate'])):
                if key not in ('OR', 'AND', 'NOT'):
                    check((key, op, value) in enabled, 'Programme ownership gate missing: ' + owner + '/' + key)

    errors = list(dict.fromkeys(errors))
    return {
        'status': 'FAIL' if errors else 'PASS', 'errors': errors, 'warnings': warnings,
        'counts': {'focuses': len(focusmap), 'decisions': len(decisions), 'events': len(events),
                   'programmes': len(dynamic), 'modifier_grants_checked': modifiers_checked,
                   'flags_read': len(flags_read), 'flags_provided': len(flags_set)},
        'geometry': {'card_collisions': collisions, 'connector_card_collisions': connector_hits,
                     'model': 'Approved96x130grid,165x112cards; approximate orthogonal routing'},
        'files_sha256': hashes, 'approved_design_sha256': hashlib.sha256(design_path.read_bytes()).hexdigest(),
        'engine_tested': False,
        'limitations': 'Independent static source/graph/geometry checks. HOI4 loading, scope evaluation, exact tooltips, native connector rendering and save behavior require engine tests.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--design', type=Path, default=DEFAULT_DESIGN)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.root, args.design)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(bool(result['errors']))


if __name__ == '__main__':
    main()
