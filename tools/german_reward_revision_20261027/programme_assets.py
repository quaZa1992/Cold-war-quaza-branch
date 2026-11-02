# IMPERIA COLD WAR — Shared German programme construction contracts.
"""Generator-only reader of current MD building caps and research unlocks."""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values

SPECIALISED_TYPES = {'microchip_plant', 'nuclear_reactor', 'renewable_energy_infra',
                     'fuel_silo', 'synthetic_refinery', 'internet_station',
                     'rail_terminal', 'anti_air_building', 'radar_station'}


@lru_cache(maxsize=1)
def building_limits():
    result = {}
    for path in sorted((ROOT / 'common/buildings').glob('*.txt')):
        for name, operator, body in first(parse(path.read_text(encoding='utf-8-sig')), 'buildings', []):
            if not isinstance(body, list):
                continue
            maximum = first(first(body, 'level_cap', []), 'state_max')
            if maximum is not None:
                result[name] = int(maximum)
    return result


@lru_cache(maxsize=1)
def technology_limits():
    result = defaultdict(list)
    for path in sorted((ROOT / 'common/technologies').glob('*.txt')):
        for technology, operator, body in first(parse(path.read_text(encoding='utf-8-sig')), 'technologies', []):
            if not isinstance(body, list):
                continue
            for unlock in values(body, 'enable_building'):
                building = first(unlock, 'building')
                if building in SPECIALISED_TYPES:
                    result[building].append((technology, int(first(unlock, 'level'))))
    assert set(result) == SPECIALISED_TYPES
    return dict(result)


def coalesce(buildings):
    totals = defaultdict(int)
    for state, building, level in buildings:
        assert int(level) > 0
        totals[int(state), building] += int(level)
    return [(state, building, level) for (state, building), level in sorted(totals.items())]


def state_guard(state, building, level, country='ROOT'):
    """Country-scope predicate, with same-state native and researched ceilings."""
    maximum = building_limits()[building]
    conditions = [f'is_owned_by = {country}', f'is_controlled_by = {country}',
                  f'check_variable = {{ building_level@{building} < {maximum-level+1} }}']
    if building == 'dockyard':
        conditions.append('is_coastal = yes')
    if building in SPECIALISED_TYPES:
        alternatives = [f'AND = {{ {country} = {{ has_tech = {tech} }} '
                        f'check_variable = {{ building_level@{building} < {cap-level+1} }} }}'
                        for tech, cap in technology_limits()[building] if cap >= level]
        conditions.append('OR = { ' + ' '.join(alternatives) + ' }' if alternatives else 'always = no')
    return f'{state} = {{ ' + ' '.join(conditions) + ' }'


def bundle_guards(buildings, country='ROOT'):
    return '\n'.join(state_guard(state, building, level, country)
                     for state, building, level in coalesce(buildings))


def bundle_effects(buildings):
    """Same native effects for the non-executing preview and guarded payment."""
    return '\n'.join(f'{state} = {{ add_extra_state_shared_building_slots = {level} '
                     f'add_building_construction = {{ type = {building} level = {level} instant_build = yes }} }}'
                     for state, building, level in coalesce(buildings))
