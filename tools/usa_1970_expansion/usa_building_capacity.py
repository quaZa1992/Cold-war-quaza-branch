# IMPERIA COLD WAR — Native USA construction-capacity predicates.
"""Check physical room for scripted building grants, not manual tech unlocks.

Native free_building_slots includes technology-unlocked construction levels.
An instant focus grant of an independent state building checks its actual
building_level against the loaded state_max instead. Ports remain province
specific, and shared-slot buildings keep their native free-slot predicate.
"""
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field

CAPACITY_LOC_PREFIX = 'COLDWAR_USA_building_capacity_'


@lru_cache(maxsize=1)
def building_definitions():
    result = {}
    for path in sorted((ROOT / 'common/buildings').glob('*.txt')):
        for root in nodes(path.read_text(encoding='utf-8-sig')):
            if root.key != 'buildings':
                continue
            for building in root.children():
                cap = next((n for n in building.children() if n.key == 'level_cap'), None)
                if cap is None:
                    continue
                result[building.key] = {
                    'shares_slots': field(cap.children(), 'shares_slots', 'no') == 'yes',
                    'state_max': field(cap.children(), 'state_max'),
                    'province_max': field(cap.children(), 'province_max'),
                    'source': path.relative_to(ROOT).as_posix(),
                }
    return result


def capacity_trigger(building, quantity=1, province=None):
    assert isinstance(quantity, int) and quantity > 0, (building, quantity)
    definition = building_definitions()[building]
    if not definition['shares_slots'] and province is None:
        assert definition['state_max'] is not None, (building, 'Explicit province required')
        ceiling = int(definition['state_max']) - quantity
        key = CAPACITY_LOC_PREFIX + building + '_' + str(quantity) + '_tt'
        return ('custom_trigger_tooltip = { tooltip = ' + key
                + ' check_variable = { var = building_level@' + building
                + ' value = ' + str(ceiling) + ' compare = less_than_or_equals } }')
    fields = [f'building = {building}', f'size > {quantity - 1}']
    if definition['shares_slots']:
        fields.append('include_locked = no')
    if province is not None:
        assert definition['province_max'] is not None, (building, province)
        fields.append(f'province = {int(province)}')
    return 'free_building_slots = { ' + ' '.join(fields) + ' }'


def capacity_localisation(sources):
    """Emit only requirement keys referenced by the actual owned USA outputs."""
    keys = {key for text in sources for key in re.findall(
        r'\btooltip\s*=\s*(' + CAPACITY_LOC_PREFIX + r'\w+_tt)\b', text)}
    entries = []
    for key in sorted(keys):
        building, quantity = key.removeprefix(CAPACITY_LOC_PREFIX).removesuffix('_tt').rsplit('_', 1)
        cap = building_definitions()[building]['state_max']
        level = 'level' if quantity == '1' else 'levels'
        text = ('Room for §Y' + quantity + '§! additional $' + building
                + '$ ' + level + '. State limit: §Y' + str(cap) + '§!.')
        entries.append(' ' + key + ':0 ' + json.dumps(text, ensure_ascii=False))
    return ('l_english:\n# IMPERIA COLD WAR — USA physical building capacity requirements.\n'
            + '\n'.join(entries) + '\n')
