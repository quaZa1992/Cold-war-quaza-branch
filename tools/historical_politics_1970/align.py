# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Apply narrowly keyed historical party-family corrections to research data."""
from __future__ import annotations

from copy import deepcopy


def apply_alignment(world, patches):
    world = deepcopy(world)
    countries = {country['tag']: country for country in world['countries']}
    for patch in patches['corrections']:
        country = countries[patch['tag']]
        kind = patch['target_type']
        rows = country['leaders' if kind == 'leader' else 'parties']
        field = 'id' if kind == 'leader' else 'name'
        matches = [row for row in rows if row.get(field) == patch['target']]
        if len(matches) != 1:
            raise ValueError(('Alignment target is not unique', patch['tag'], patch['target']))
        row = matches[0]
        for name, expected in patch['before'].items():
            if row.get(name) not in (expected, patch['after'].get(name)):
                raise ValueError(('Alignment input changed', patch['tag'], patch['target'], name))
        row.update(patch['after'])
        row['source_urls'] = sorted(set(row.get('source_urls', []) + patch['source_urls']))
        row['alignment_note'] = patch['reason']
    world['party_family_alignment_count'] = len(patches['corrections'])
    return world
