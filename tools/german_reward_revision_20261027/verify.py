# IMPERIA COLD WAR — Independent BRD and DDR reward-revision source checks.
"""Compare loaded output with the private pre-revision copy, not catalogue claims."""
from pathlib import Path
import hashlib
import json
import re
import sys
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/german_reward_revision_20261027'
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk


def shortcut_values(tree):
    # The native parser rejects .8; writing the same numeric value as 0.8
    # repairs that literal without changing camera navigation.
    def normalise(rows):
        return [(key, operator, normalise(body) if isinstance(body, list) else
                 Decimal(body) if key == 'scroll_wheel_factor' else body)
                for key, operator, body in rows]
    return [normalise(rows) for rows in values(tree, 'shortcut')]


def paths():
    result = []
    for directory in ('common', 'events', 'interface', 'localisation/english'):
        for path in (ROOT / directory).rglob('*'):
            if path.is_file() and path.suffix in {'.txt', '.gfx', '.gui', '.yml'} and path.name.startswith(('COLDWAR_GER', 'COLDWAR_DDR', 'COLDWAR_Germany', 'COLDWAR_GRANT')):
                result.append(path.relative_to(ROOT).as_posix())
    return sorted(result)


def main():
    before = json.loads((REPORT / 'BEFORE.json').read_text(encoding='utf-8'))
    backup = Path(before['runtime_backup'])
    errors = []
    graphs = {}
    changed_rewards = {}
    for tag in ('GER', 'DDR'):
        relative = f'common/national_focus/COLDWAR_{tag}_1970_focus.txt'

        def load(base):
            tree = first(parse((base / relative).read_text(encoding='utf-8')), 'focus_tree')
            return tree, {first(node, 'id'): node for node in values(tree, 'focus')}

        old_tree, old = load(backup)
        new_tree, new = load(ROOT)
        if old.keys() != new.keys():
            errors.append(f'{tag}: changed focus ID set')
        emitted = set()
        for identifier, node in new.items():
            anchor = first(node, 'relative_position_id')
            if anchor and anchor not in emitted:
                errors.append(f'{identifier}: relative anchor must be emitted first: {anchor}')
            emitted.add(identifier)
        for field in ('initial_show_position', 'continuous_focus_position', 'shortcut', 'country', 'reset_on_civilwar'):
            old_value, new_value = (shortcut_values(old_tree), shortcut_values(new_tree)) if field == 'shortcut' else (values(old_tree, field), values(new_tree, field))
            if old_value != new_value:
                errors.append(f'{tag}: changed tree presentation or routing: {field}')
        for identifier in new.keys() & old.keys():
            for field in ('x', 'y', 'relative_position_id', 'cost', 'prerequisite', 'mutually_exclusive', 'allow_branch', 'bypass'):
                if values(old[identifier], field) != values(new[identifier], field):
                    errors.append(f'{identifier}: changed graph/duration/branch field {field}')
        changed_rewards[tag] = sorted(identifier for identifier in new.keys() & old.keys()
                                      if values(old[identifier], 'completion_reward') != values(new[identifier], 'completion_reward'))
        graphs[tag] = {'focuses': len(new), 'graph_and_duration_unchanged': not any(tag in error for error in errors)}

    inventory = paths()
    hashes = {relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() for relative in inventory}
    modified = sorted(relative for relative in inventory if hashes[relative] != before['runtime_sha256'].get(relative))
    modified_localisation = []
    for relative in modified:
        path = ROOT / relative
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        if path.suffix == '.yml':
            if not raw.startswith(b'\xef\xbb\xbf') or not text.startswith('l_english:\n# IMPERIA COLD WAR'):
                errors.append('Invalid localization header/encoding: ' + relative)
            names = re.findall(r'(?m)^\s+([^\s:#]+):', text)
            if len(names) != len(set(names)):
                errors.append('Duplicate localization keys: ' + relative)
            modified_localisation.append(relative)
        else:
            if raw.startswith(b'\xef\xbb\xbf') or not text.startswith('# IMPERIA COLD WAR'):
                errors.append('Invalid script marker/encoding: ' + relative)
            parse(text)
            if path.suffix == '.txt' and 'scripted_effects' in relative and relative not in before['runtime_sha256']:
                for key, operator, body in walk(parse(text)):
                    if key == 'add_building_construction' and isinstance(body, list):
                        if not first(body, 'type') or int(first(body, 'level', '0')) <= 0:
                            errors.append('Invalid building effect: ' + relative)
            if re.search(r'(?<![\w.])-?\d+\.\d{6,}(?![\w.])', text):
                errors.append('Unsafe fixed-point literal precision: ' + relative)
    history_changed = []
    for relative, digest in before['runtime_sha256'].items():
        if relative.startswith('history/') and hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != digest:
            history_changed.append(relative)
    if history_changed:
        errors.append('Changed historical setup: ' + ', '.join(history_changed))
    # Resolve the actual loaded custom calls, rather than nested pseudo-definitions.
    effect_names = set()
    trigger_definitions = {}
    for path in (ROOT / 'common/scripted_effects').glob('*.txt'):
        effect_names.update(key for key, operator, body in parse(path.read_text(encoding='utf-8-sig')))
    for path in (ROOT / 'common/scripted_triggers').glob('*.txt'):
        trigger_definitions.update((key, body) for key, operator, body in parse(path.read_text(encoding='utf-8-sig'))
                                   if isinstance(body, list))
    technology_names = set()
    research_categories = set()
    for path in (ROOT / 'common/technologies').glob('*.txt'):
        entries = first(parse(path.read_text(encoding='utf-8-sig')), 'technologies', [])
        technology_names.update(key for key, operator, body in entries)
        for key, operator, body in walk(entries):
            if key == 'categories' and isinstance(body, list):
                research_categories.update(value for key, operator, value in body if key == '_bare')
    equipment_types = set()
    for path in (ROOT / 'common/units/equipment').glob('*.txt'):
        entries = parse(path.read_text(encoding='utf-8-sig'))
        for wrapper in ('equipments', 'duplicate_archetypes'):
            equipment_types.update(key for key, operator, body in first(entries, wrapper, []))
        for key, operator, body in walk(entries):
            if key in ('type', 'allowed_types', 'categories'):
                if isinstance(body, str):
                    equipment_types.add(body)
                elif isinstance(body, list):
                    equipment_types.update(value for key, operator, value in body if key == '_bare')
    reward_api_counts = {'research': 0, 'equipment': 0, 'doctrine': 0}
    for relative in modified:
        if not relative.endswith('.txt'):
            continue
        entries = parse((ROOT / relative).read_text(encoding='utf-8'))
        for key, operator, body in walk(entries):
            if isinstance(body, str) and re.fullmatch(r'[+-]?\.\d+', body):
                errors.append(f'Native numeric literal requires a leading zero: {key} = {body} in {relative}')
            if key.startswith('COLDWAR_') and body == 'yes':
                if key not in effect_names and key not in trigger_definitions:
                    errors.append(f'Unregistered German effect/trigger: {key} in {relative}')
            if key == 'has_tech' and body not in technology_names:
                errors.append(f'Unknown technology {body} in {relative}')
            if key == 'add_tech_bonus' and isinstance(body, list):
                reward_api_counts['research'] += 1
                for category in values(body, 'category'):
                    if category not in research_categories:
                        errors.append(f'No actual technology consumes category {category} in {relative}')
            if key == 'add_equipment_bonus' and isinstance(body, list):
                reward_api_counts['equipment'] += 1
                for target, operator, modifiers in first(body, 'bonus', []):
                    if target not in equipment_types:
                        errors.append(f'Unknown equipment bonus target {target} in {relative}')
            if key == 'add_doctrine_cost_reduction':
                reward_api_counts['doctrine'] += 1
    new_trigger_names = {key for relative in modified if '/scripted_triggers/' in relative
                         for key, operator, body in parse((ROOT / relative).read_text(encoding='utf-8'))}

    def trigger_cycle(name, stack=()):
        if name in stack:
            return list(stack[stack.index(name):]) + [name]
        for key, operator, body in walk(trigger_definitions.get(name, [])):
            if body == 'yes' and key in trigger_definitions:
                cycle = trigger_cycle(key, stack + (name,))
                if cycle:
                    return cycle
        return None

    for name in sorted(new_trigger_names):
        cycle = trigger_cycle(name)
        if cycle:
            errors.append('Recursive trigger cycle: ' + ' -> '.join(cycle))
    result = {'project': 'IMPERIA COLD WAR', 'success': not errors, 'graphs': graphs,
              'changed_focus_rewards': changed_rewards, 'modified_runtime_files': modified,
              'localisation_files_checked': modified_localisation, 'history_changed': history_changed,
              'runtime_files': len(inventory), 'runtime_sha256': hashes, 'errors': errors,
              'reward_api_occurrences_checked': reward_api_counts,
              'scope': 'Actual loaded graph/duration/routing preservation, changed-file syntax, encoding, precision and localization uniqueness. API, transaction, native and route-balance evidence recorded separately.'}
    (REPORT / 'SOURCE_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'success': result['success'], 'graphs': graphs,
                      'changed_rewards': {tag: len(ids) for tag, ids in changed_rewards.items()},
                      'modified_files': len(modified), 'errors': errors}))
    return not result['success']


if __name__ == '__main__':
    raise SystemExit(main())
