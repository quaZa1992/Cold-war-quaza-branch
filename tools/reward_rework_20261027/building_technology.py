# IMPERIA COLD WAR — Technology requirements for Korea/Japan construction rewards.
"""Use the actual installed MD unlocks, including the resulting building tier.

Ordinary starting buildings keep their existing rules. These specialised types
must have a researched enable_building entry that covers the entire new level.
The same emitted country/state predicate is used by availability and execution.
"""
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values

TECH_LOCKED_BUILDINGS = {
    'microchip_plant', 'nuclear_reactor', 'renewable_energy_infra', 'fuel_silo',
    'synthetic_refinery', 'internet_station', 'rail_terminal',
    'anti_air_building', 'radar_station',
}


@lru_cache(maxsize=1)
def unlocks():
    result = defaultdict(list)
    for path in sorted((ROOT / 'common/technologies').glob('*.txt')):
        technologies = first(parse(path.read_text(encoding='utf-8-sig')), 'technologies', [])
        for technology, operator, body in technologies:
            if not isinstance(body, list):
                continue
            for entry in values(body, 'enable_building'):
                building = first(entry, 'building')
                if building in TECH_LOCKED_BUILDINGS:
                    result[building].append((technology, int(first(entry, 'level'))))
    assert set(result) == TECH_LOCKED_BUILDINGS, 'Missing installed building unlock provider'
    return dict(result)


def state_technology_guard(building, awarded_levels, country='ROOT'):
    """Return a STATE-scope condition; country is the actual asset recipient."""
    if building not in TECH_LOCKED_BUILDINGS:
        return ''
    alternatives = []
    for technology, maximum in unlocks()[building]:
        if maximum >= awarded_levels:
            alternatives.append(
                f'AND = {{ {country} = {{ has_tech = {technology} }} '
                f'check_variable = {{ building_level@{building} < {maximum - awarded_levels + 1} }} }}'
            )
    return 'OR = { ' + ' '.join(alternatives) + ' }' if alternatives else 'always = no'


def country_technology_guard(building, awarded_levels):
    """Visible minimum technical capability; final state tier is checked too."""
    if building not in TECH_LOCKED_BUILDINGS:
        return ''
    options = [f'has_tech = {technology}' for technology, maximum in unlocks()[building]
               if maximum >= awarded_levels]
    return 'OR = { ' + ' '.join(options) + ' }' if options else 'always = no'
