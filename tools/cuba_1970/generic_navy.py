# IMPERIA COLD WAR — Faithful MD generic naval branch and required feeder focuses.
"""Frozen donor, namespaced IDs, unchanged naval geometry and native mechanics.

The only reward adaptations implement the standing one-slot-per-building rule.
Source, authorship and permissions are recorded in GENERIC_NAVY_SOURCE.json.
"""
from copy import deepcopy
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, emit

SOURCE = json.loads((HERE/'GENERIC_NAVY_SOURCE.json').read_text(encoding='utf8'))
ID_MAP = {record['id']: record['id'].replace('GENERIC_', 'COLDWAR_CUB_GEN_', 1) for record in SOURCE['focuses']}
IDS = set(ID_MAP.values())
COMPOSITE = 'COLDWAR_CUB_GEN_one_random_composite_plant'
ROOT_POSITIONS = {
    'GENERIC_naval_reform': (24, 6),
    'GENERIC_light_industry_investments': (5, 6),
    'GENERIC_air_force_reform': (32, 6),
}


def rewrite(rows):
    result = []
    for key, operator, value in rows:
        if isinstance(value, list):
            value = rewrite(value)
        elif value in ID_MAP:
            value = ID_MAP[value]
        elif key == 'log':
            for old, new in sorted(ID_MAP.items(), key=lambda row: -len(row[0])):
                value = value.replace(old, new)
        if key == 'one_random_composite_plant':
            key = COMPOSITE
        result.append((key, operator, value))
    return result


def focuses():
    nodes = []
    for record in SOURCE['focuses']:
        rows = rewrite(parse(record['script']))
        if record['id'] in ROOT_POSITIONS:
            x, y = ROOT_POSITIONS[record['id']]
            rows = [(k, op, str(x) if k == 'x' else str(y) if k == 'y' else v) for k, op, v in rows]
        if record['id'] == 'GENERIC_naval_bases':
            reward = first(rows, 'completion_reward')
            state = first(reward, 'random_owned_controlled_state')
            index = next(i for i, row in enumerate(state) if row[0] == 'construct_building_in_random_province')
            state.insert(index, ('add_extra_state_shared_building_slots', '=', '1'))
        if record['id'] == 'GENERIC_light_industry_investments':
            state = first(first(rows, 'completion_reward'), 'capital_scope')
            # One completed industry and one queued power-plant level: two slots.
            state[:] = [(k, op, '2' if k == 'add_extra_state_shared_building_slots' else v) for k, op, v in state]
        nodes.append(rows)
    return nodes


def helpers():
    rows = parse(SOURCE['composite_helper'])
    state = first(rows, 'every_controlled_state')
    slot = next(row for row in state if row[0] == 'add_extra_state_shared_building_slots')
    state.remove(slot)
    state.insert(next(i for i, row in enumerate(state) if row[0] == 'add_building_construction'), slot)
    return [(COMPOSITE, '=', rows)]


def localisation():
    return {new + suffix: SOURCE['localisation'][old + suffix]
            for old, new in ID_MAP.items() for suffix in ('', '_desc')}


def scripts():
    return ['focus = {\n' + emit(node) + '\n}' for node in focuses()]


def resolved():
    by = {first(n, 'id'): n for n in focuses()}
    coordinates = {}
    def position(key):
        if key not in coordinates:
            node = by[key]
            x, y = int(first(node, 'x')), int(first(node, 'y'))
            anchor = first(node, 'relative_position_id')
            if anchor:
                ax, ay = position(anchor)
                x, y = x + ax, y + ay
            coordinates[key] = (x, y)
        return coordinates[key]
    for key in by:
        position(key)
    return coordinates
