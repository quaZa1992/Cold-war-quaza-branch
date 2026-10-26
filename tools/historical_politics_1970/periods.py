# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Period labels reviewed separately from the research draft catalogues."""
from __future__ import annotations

import copy


EGYPT_CURRENTS = [
    'ASU Centrist Current', 'Conservative Current', 'Civic Liberal Current',
    'Social Democratic Current', 'Independent Communist Current',
    'Revolutionary Socialist Current', 'Nasserist Opposition', 'Nasserist Current',
    'Reformist Shiite Current (Alternate Path)', 'Shiite Clerical Current (Alternate Path)',
    'Salafi Current', 'Radical Islamist Current (Alternate Path)',
    'Muslim Brotherhood', 'Coptic Orthodox Institution',
    'Liberal Constitutional Current', 'Civic Republican Current',
    'Administrative Reform Current', 'Environmental Reform Current',
    'Arab Socialist Union (ASU)', 'ASU Independent Left',
    'State Nationalist Current', "Ba'athist Current", 'Military Command',
    'House of Muhammad Ali - Restorationists',
]


def apply_period_labels(world, research):
    """Apply the user's reviewed historical-current policy without new effects.

    Where an establishment year is uncertain, a formal name is exposed only
    after that year. This conservative boundary is documented, not asserted to
    be the foundation day. The underlying political families never change.
    """
    world = copy.deepcopy(world)
    by_tag = {c['tag']: c for c in world['countries']}
    egypt = research['countries'][0]['parties']
    rows = []
    for index, name in enumerate(EGYPT_CURRENTS):
        record = egypt[index]
        assert record['index'] == index
        rows.append({'index': index, 'name': name, 'from': '1970.1.1',
            'until': None, 'source_urls': record['sources'] or ['local:localisation/english/COLDWAR_EGY_1970_parties_l_english.yml#' + record['current_key']],
            'description': ('A political current or institution represented in this alternate path; not a claim that a later party already existed in 1970.' if index != 18 else 'The Arab Socialist Union was Egypt\'s sole legal political organization at the 1970 bookmark.')})
    transitions = [
        (0, '1977.1.1', 'Egyptian Arab Socialist Party', 0),
        (0, '1979.1.1', 'National Democratic Party (NDP)', 0),
        (4, '1976.1.1', 'Egyptian Communist Party', 4),
        (5, '1996.1.1', 'Revolutionary Socialists', 5),
        (6, '1997.1.1', 'Al-Karama Movement', 6),
        (7, '1993.1.1', 'Arab Democratic Nasserist Party', 7),
        (14, '1978.3.1', 'New Wafd Party', 14),
        (17, '1990.5.1', 'Egyptian Green Party', 17),
        (19, '1976.5.1', 'National Progressive Unionist Party (Tagammu)', 19),
    ]
    for index, start, name, source_index in transitions:
        prior = [p for p in rows if p['index'] == index][-1]
        prior['until'] = start
        rows.append({'index': index, 'name': name, 'from': start, 'until': None,
            'source_urls': egypt[source_index]['sources'],
            'description': 'Historical political organization. The display boundary follows the documented foundation month or year; it neither grants power nor schedules a government change.',
            'date_policy': 'Conservative boundary after documented foundation month/year.'})
    for index, flag, name in [
        (0, 'COLDWAR_EGY_1970_future_party', 'State Modernization Movement'),
        (18, 'COLDWAR_EGY_1970_socialist_alliance', 'Independent Socialist Alliance'),
    ]:
        rows.append({'index': index, 'name': name, 'from': '1970.1.1', 'until': '2001.1.1',
            'extra_trigger': f'has_country_flag = {flag}',
            'source_urls': egypt[index]['sources'],
            'description': 'An alternate political coalition formed by the chosen political path. It does not bear the name of a party founded after 2000.'})
    by_tag['EGY']['parties'] = rows
    return world
