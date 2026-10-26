# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Keyed native-MD family corrections; leaves unrelated monarchies untouched."""
from copy import deepcopy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def corrections():
    return json.loads((HERE / 'native_monarchy_alignment.json').read_text(encoding='utf-8'))['countries']


def apply_country(original):
    if original['tag'] == 'QAT':
        from qatar_identity import align_country
        return align_country(original)
    country = deepcopy(original)
    patch = corrections().get(country['tag'])
    if not patch:
        return country
    for kind, name_key, index_key, targets in [('parties', 'name', 'index', patch['parties']),
                                               ('leaders', 'id', 'party_index', patch['leaders'])]:
        for target in targets:
            matches = [row for row in country[kind] if row[name_key] == target]
            assert len(matches) == 1, (country['tag'], kind, target, len(matches))
            row = matches[0]
            assert row[index_key] in (patch['from_index'], patch['to_index']), (country['tag'], target, row[index_key])
            row[index_key] = patch['to_index']
            row['native_md_alignment'] = patch['native_reference']
            if patch.get('historical_sources'):
                row['source_urls'] = sorted(set(row.get('source_urls', []) + patch['historical_sources']))
                row['alignment_evidence_kind'] = patch['evidence_kind']
            if kind == 'leaders' and target in patch['sovereigns']:
                row['traits'] = list(dict.fromkeys(row.get('traits', []) + ['king']))
    return country


def apply_world(original):
    world = deepcopy(original)
    world['countries'] = [apply_country(country) for country in world['countries']]
    return world
