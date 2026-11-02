# IMPERIA COLD WAR — South Korea 1970 reward revision overlay.
"""Apply the authorized KOR reward revision to the effective, derived design."""
from copy import deepcopy
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OVERLAY = ROOT / 'docs/reward_rework_20261027/KOR_reward_revision.json'
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first


def _number(value):
    return f'{value:.5f}'.rstrip('0').rstrip('.')


def _building_metadata():
    """Read current native MD state caps and shared cap groups."""
    source = ROOT / 'common/buildings/00_buildings.txt'
    rows = parse(source.read_text(encoding='utf-8'))
    metadata = {}
    for key, _, body in first(rows, 'buildings', []):
        cap = first(body, 'level_cap', [])
        if not cap:
            continue
        state_max = first(cap, 'state_max')
        group_by = first(cap, 'group_by')
        metadata[key] = {
            'state_max': int(state_max) if state_max is not None else None,
            'group_by': group_by,
        }
    return metadata


BUILDING_METADATA = _building_metadata()


def _aggregate_building_gates(node, metadata):
    """Require ownership/control plus full state-cap headroom for the bundle.

    Every awarded level has its own preceding shared-slot grant. The gate
    therefore checks native type caps directly instead of requiring those
    shared slots to exist before completion.
    """
    gate = node.get('native_gate_body', '')
    kept = [line for line in gate.splitlines()
            if not re.match(r'^\s*\d+\s*=\s*\{\s*is_owned_by\s*=\s*ROOT\s+is_controlled_by\s*=\s*ROOT\s+free_building_slots\s*=', line)]
    buildings = node.get('effects', {}).get('buildings', [])
    if not buildings:
        node['native_gate_body'] = '\n'.join(kept)
        return

    levels = {}
    for building in buildings:
        key = building['type']
        if key not in metadata or metadata[key]['state_max'] is None:
            raise ValueError('KOR construction lacks a native state cap for ' + key)
        pair = (int(building['state']), key)
        levels[pair] = levels.get(pair, 0) + int(building['level'])

    groups = {}
    for key, spec in metadata.items():
        if spec['group_by']:
            groups.setdefault(spec['group_by'], []).append(key)
    states = sorted({state for state, _ in levels})
    for state in states:
        checks = ['is_owned_by = ROOT', 'is_controlled_by = ROOT']
        by_group = {}
        for (asset_state, building_type), amount in levels.items():
            if asset_state != state:
                continue
            spec = metadata[building_type]
            group = spec['group_by']
            if group:
                by_group[group] = by_group.get(group, 0) + amount
            else:
                threshold = spec['state_max'] - amount + 1
                checks.append(f'{building_type} < {threshold}')
        for group, total in by_group.items():
            members = groups[group]
            cap = min(metadata[member]['state_max'] for member in members)
            threshold = cap - total + 1
            checks.extend(f'{member} < {threshold}' for member in members)
        kept.append(f"{state} = {{ {' '.join(checks)} }}")
    node['native_gate_body'] = '\n'.join(kept)


def apply_reward_revision(data):
    """Return a revised copy; the approval-stage design and its hash remain untouched."""
    result = deepcopy(data)
    revision = json.loads(OVERLAY.read_text(encoding='utf-8'))
    by_key = {node['key']: node for node in result['nodes']}
    missing = set(revision['entries']) - set(by_key)
    if missing:
        raise ValueError('Reward overlay refers to missing KOR focus keys: ' + ', '.join(sorted(missing)))

    for key, entry in revision['entries'].items():
        node = by_key[key]
        slot = entry['slot']
        policies = node.setdefault('effects', {}).setdefault('policies', [])
        policy = next((p for p in policies if p['slot'] == slot), None)
        if policy is None:
            policy = {'slot': slot, 'qualified_slot': f"{node['group']}:{slot}", 'modifiers': {}}
            policies.append(policy)
        policy['modifiers'].update(entry['modifiers'])

        # Regenerate the native variable leaves for this exact policy slot so preview
        # data and the code emitter observe the same completed values.
        prefix = node['id'] + '_' + slot + '_'
        lines = [line for line in node.get('native_leaf_effects', '').splitlines()
                 if not (line.startswith('set_variable = { ' + prefix))]
        lines.extend(f'set_variable = {{ {prefix}{modifier} = {_number(value)} }}'
                     for modifier, value in policy['modifiers'].items())
        for bonus in entry.get('equipment_bonuses', []):
            node.setdefault('effects', {}).setdefault('equipment_bonuses', []).append(deepcopy(bonus))
            lines.append('add_equipment_bonus = {')
            lines.append('    name = ' + bonus['name'])
            lines.append('    bonus = {')
            for equipment_type, values in bonus['types'].items():
                lines.append('        ' + equipment_type + ' = {')
                lines.extend(f'            {modifier} = {_number(value)}'
                             for modifier, value in values.items())
                lines.append('            instant = yes')
                lines.append('        }')
            lines.extend(('    }', '}'))
        for bonus in entry.get('tech_bonuses', []):
            node.setdefault('effects', {}).setdefault('tech_bonuses', []).append(deepcopy(bonus))
            lines.extend((
                'add_tech_bonus = {',
                '    name = ' + bonus['name'],
                '    bonus = ' + _number(bonus['bonus']),
                '    uses = ' + str(bonus['uses']),
                '    category = ' + bonus['category'],
                '}',
            ))
        for bonus in entry.get('doctrine_bonuses', []):
            node.setdefault('effects', {}).setdefault('doctrine_bonuses', []).append(deepcopy(bonus))
            lines.extend((
                'add_doctrine_cost_reduction = {',
                '    name = ' + bonus['name'],
                '    cost_reduction = ' + _number(bonus['cost_reduction']),
                '    uses = ' + str(bonus['uses']),
                '    category = ' + bonus['category'],
                '}',
            ))
        node['native_leaf_effects'] = '\n'.join(lines)
        node.setdefault('reward_revision', {})['rationale'] = entry['reason']

    # Tangible regional projects are a separate, explicit overlay layer.  The
    # compiler already grants one shared slot per level and performs its
    # ownership/control/native-capacity checks from effects.buildings.  Keeping
    # the project list here means previews and one-time completion transactions
    # consume the same derived data.
    for key, project in revision.get('projects', {}).items():
        if key not in by_key:
            raise ValueError('Project overlay refers to missing KOR focus key: ' + key)
        node = by_key[key]
        effects = node.setdefault('effects', {})
        buildings = project.get('buildings', [])
        effects.setdefault('buildings', []).extend(deepcopy(buildings))
        lines = node.get('native_leaf_effects', '').splitlines()
        for building in buildings:
            lines.append(
                f"{building['state']} = {{ add_building_construction = {{ "
                f"type = {building['type']} level = {building['level']} instant_build = yes }} }}"
            )

        gdp_cost_fraction = project.get('gdp_cost_fraction', 0)
        if gdp_cost_fraction:
            if not 0.005 <= gdp_cost_fraction <= 0.02:
                raise ValueError('Project GDP fraction is outside the authorised 0.5 to 2.0 percent range: ' + key)
            fraction_text = f'{gdp_cost_fraction:g}'
            if '.' in fraction_text and len(fraction_text.split('.', 1)[1]) > 5:
                raise ValueError('Project GDP fraction exceeds fixed-point precision: ' + key)
            effects['gdp_project_cost_fraction'] = gdp_cost_fraction

        for bonus in project.get('equipment_bonuses', []):
            effects.setdefault('equipment_bonuses', []).append(deepcopy(bonus))
            lines.append('add_equipment_bonus = {')
            lines.append('    name = ' + bonus['name'])
            lines.append('    bonus = {')
            for equipment_type, values in bonus['types'].items():
                lines.append('        ' + equipment_type + ' = {')
                lines.extend(f'            {modifier} = {_number(value)}'
                             for modifier, value in values.items())
                lines.append('            instant = yes')
                lines.append('        }')
            lines.extend(('    }', '}'))
        for bonus in project.get('tech_bonuses', []):
            effects.setdefault('tech_bonuses', []).append(deepcopy(bonus))
            lines.extend(('add_tech_bonus = {', '    name = ' + bonus['name'],
                          '    bonus = ' + _number(bonus['bonus']),
                          '    uses = ' + str(bonus['uses']),
                          '    category = ' + bonus['category'], '}'))
        for bonus in project.get('doctrine_bonuses', []):
            effects.setdefault('doctrine_bonuses', []).append(deepcopy(bonus))
            lines.extend(('add_doctrine_cost_reduction = {', '    name = ' + bonus['name'],
                          '    cost_reduction = ' + _number(bonus['cost_reduction']),
                          '    uses = ' + str(bonus['uses']),
                          '    category = ' + bonus['category'], '}'))
        node['native_leaf_effects'] = '\n'.join(lines)
        node.setdefault('reward_revision', {})['project_rationale'] = project['reason']

    # Existing domestic setup prices were authored as fixed billions, which
    # overwhelms South Korea's 1970 GDP base. Convert each positive focus price
    # to a capped GDP fraction, then combine it with any explicit project
    # increment. Bilateral agreement terms remain in their separate contract
    # records and are not touched here.
    cost_scale = revision['domestic_gdp_cost_scale']
    rate = float(cost_scale['basis_per_legacy_billion'])
    cap = float(cost_scale['maximum_base_fraction'])
    for node in result['nodes']:
        effects = node.setdefault('effects', {})
        legacy_cost = float(effects.get('cost', 0))
        base_fraction = min(legacy_cost * rate, cap) if legacy_cost > 0 else 0.0
        project_fraction = float(effects.get('gdp_project_cost_fraction', 0))
        if not (base_fraction or project_fraction):
            continue
        total_fraction = base_fraction + project_fraction
        total_text = f'{total_fraction:.5f}'.rstrip('0').rstrip('.')
        if '.' in total_text and len(total_text.split('.', 1)[1]) > 5:
            raise ValueError('Domestic GDP charge exceeds fixed-point precision: ' + node['key'])
        effects['legacy_fixed_cost_bn'] = legacy_cost
        effects['gdp_base_cost_fraction'] = base_fraction
        effects['gdp_share_cost_fraction'] = total_fraction
        effects['cost'] = 0

        # Replace the single old fixed debit with one canonical amount based on
        # the combined structured fraction. Keep all other native reward leaves.
        lines = [line for line in node.get('native_leaf_effects', '').splitlines()
                 if not line.lstrip().startswith('set_temp_variable = { treasury_change = ')
                 and not line.lstrip().startswith('set_variable = { treasury_change = ')
                 and line.strip() != 'modify_treasury_effect = yes']
        formula = f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{total_text} }} }}"
        node['native_leaf_effects'] = '\n'.join([formula, 'modify_treasury_effect = yes'] + lines)
        node.setdefault('reward_revision', {})['domestic_gdp_cost'] = {
            'legacy_fixed_cost_bn': legacy_cost,
            'base_fraction': base_fraction,
            'project_increment_fraction': project_fraction,
            'total_fraction': total_fraction,
        }

    result['reward_revision'] = {
        'id': revision['revision'],
        'source': 'docs/reward_rework_20261027/KOR_reward_revision.json',
        'entries': len(revision['entries']),
        'projects': len(revision.get('projects', {})),
        'domestic_cost_scale': cost_scale,
        'converted_domestic_focus_costs': sum(
            1 for node in result['nodes']
            if node.get('effects', {}).get('legacy_fixed_cost_bn', 0) > 0),
        'design_baseline_unchanged': True,
    }
    for node in result['nodes']:
        _aggregate_building_gates(node, BUILDING_METADATA)
        node['native_completion_guard'] = (
            node.get('native_gate_body', '') + '\nNOT = { has_country_flag = '
            + node['id'] + '_paid }'
        )
        gate = result.get('gate_definitions', {}).get(node.get('proposed_trigger'))
        if gate is not None:
            gate['body'] = node.get('native_gate_body', '')
    return result
