# IMPERIA CW — Cold War: Preserve the existing West German political roster.
"""Compile-time party identity checks; never create or rename political parties."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'party_registry_1970/data/GER.json'
EXPECTED = {
    'cdu': (1, 'Christlich Demokratische Union Deutschlands'),
    'spd': (3, 'Sozialdemokratische Partei Deutschlands'),
    'dkp': (4, 'Deutsche Kommunistische Partei'),
    'fdp': (2, 'Freie Demokratische Partei'),
    'npd': (21, 'Nationaldemokratische Partei Deutschlands'),
    'pds': (5, 'Partei des Demokratischen Sozialismus'),
    'greens': (17, 'Die Grünen'),
    'rep': (20, 'Die Republikaner'),
    'dvu': (22, 'Deutsche Volksunion'),
}
NAMES = {'pds': 'The PDS', 'greens': 'The Greens', 'rep': 'Die Republikaner', 'dvu': 'The DVU'}
_data = json.loads(DATA.read_text(encoding='utf-8'))
AVAILABLE = {name: any(p['name'] == expected for p in _data['slots'].get(str(slot), []))
             for name, (slot, expected) in EXPECTED.items()}


def requirement(name):
    from cw_lib import L, P
    key = L(f'{P}_tt_roster_{name}', f'{NAMES.get(name, name.upper())} must be an established political party.')
    return f'custom_trigger_tooltip = {{ tooltip = {key} always = {"yes" if AVAILABLE[name] else "no"} }}'


def slot_available(slot):
    matches = [name for name, (index, expected) in EXPECTED.items() if index == slot]
    return all(AVAILABLE[name] for name in matches)
