# IMPERIA COLD WAR — Israel 2.2 focus-only spatial arrangement.
"""Arrange the review design without changing policy or reward semantics.

Only node ``xy`` and group ``origin`` are modified. Mafdal sits beside the
territorial programmes so its explicit freeze/reopening prerequisite can remain
a forward, visible connection. There is no generator execution or file I/O.
"""
from copy import deepcopy


ORIGINS = {
    'institutions': (7, 0),
    'capital': (21, 0),
    'absorption': (35, 0),
    'water': (49, 0),
    'reserves': (7, 8),
    'arsenal': (21, 8),
    'diplomacy': (35, 8),
    'territories': (49, 8),
    'mafdal': (63, 8),
    'alignment': (7, 22),
    'gahal': (22, 22),
    'orthodox': (35, 22),
    'liberals': (7, 40),
    'haolam': (21, 40),
    'rakah': (35, 40),
    'state_list': (49, 40),
    'mapam': (7, 50),
    'maki': (21, 50),
    'free_center': (35, 50),
}

# Coordinates here are relative to the owning group's origin. Unlisted cards
# retain their existing local position, translated with the group as a whole.
POSITIONS = {
    # The two named tenders are separate focus actions, not a hidden menu.
    'sapir_negev': (5, 3),
    # Competing appropriations occupy one actual exclusive-choice row.
    'supplier_competition': (-3, 3),
    'national_bargain': (1, 3),
    'gahal_settlement_match': (3, 3),
    # The three land choices remain adjacent and inspectable at normal scale.
    'mafdal_budget': (0, 0),
    'hesder': (-3, 1),
    'mizrahi_coops': (1, 1),
    'religious_towns': (-4, 2),
    'mafdal_survey': (-1, 2),
    'mafdal_land_westbank': (1, 2),
    'mafdal_land_gaza': (3, 2),
    'service_bargain': (0, 3),
    # A readable reserve training, mobilisation and release action pocket.
    'reserve_exercise': (-2, 6),
    'reserve_callup': (2, 6),
    'reserve_release': (2, 7),
    # Shared administration, followed by region-aligned action rows.
    'occupation_accounts': (0, 0),
    'civil_admin': (-2, 1),
    'cap_projects': (2, 1),
    'negotiated_terms': (-2, 2),
    'controlled_sites': (-3, 3),
    'gaza_projects': (-1, 3),
    'sinai_projects': (1, 3),
    'golan_projects': (3, 3),
    'west_bank_projects': (-3, 4),
    'foreign_footholds': (-3, 5),
    'gaza_foothold': (-1, 5),
    'sinai_foothold': (1, 5),
    'golan_foothold': (3, 5),
    'funded_network': (0, 6),
    'close_west_bank': (-3, 8),
    'close_gaza': (-1, 8),
    'close_sinai': (1, 8),
    'close_golan': (3, 8),
    # Keeps both real OR inputs, including Mafdal's later restraint focus.
    'lift_freeze': (0, 11),
}


def _semantic_snapshot(nodes, groups):
    return deepcopy({
        'nodes': [{key: value for key, value in node.items() if key != 'xy'}
                  for node in nodes],
        'groups': [{key: value for key, value in group.items() if key != 'origin'}
                   for group in groups],
    })


def _overlap(a, b):
    return (min(a[2], b[2]) > max(a[0], b[0]) and
            min(a[3], b[3]) > max(a[1], b[1]))


def _verify_geometry(nodes, groups):
    # These are the actual external inspector's card and label bounds, not a
    # claim about native engine pixels. Check whole subgroup footprints too.
    boxes = {node['id']: (node['xy'][0] * 82,
                          node['xy'][1] * 178,
                          node['xy'][0] * 82 + 147,
                          node['xy'][1] * 178 + 142)
             for node in nodes}
    for index, left in enumerate(nodes):
        for right in nodes[index + 1:]:
            assert not _overlap(boxes[left['id']], boxes[right['id']]), (
                'Focus-card collision', left['id'], right['id'])
    footprints = {}
    for group in groups:
        children = [boxes[node['id']] for node in nodes
                    if node['group'] == group['id']]
        assert children, ('Group has no cards', group['id'])
        footprints[group['id']] = (
            min(box[0] for box in children) - 28,
            min(box[1] for box in children) - 70,
            max(box[2] for box in children) + 28,
            max(box[3] for box in children) + 19,
        )
    for index, left in enumerate(groups):
        for right in groups[index + 1:]:
            assert not _overlap(footprints[left['id']], footprints[right['id']]), (
                'Programme-footprint collision', left['id'], right['id'])
    by_id = {node['id']: node for node in nodes}
    assert len(by_id) == len(nodes), 'Duplicate focus IDs'
    for node in nodes:
        for row in node.get('pre', []):
            for predecessor in row:
                assert predecessor in by_id, ('Missing prerequisite', node['id'], predecessor)
                assert by_id[predecessor]['xy'][1] < node['xy'][1], (
                    'Prerequisite does not run downwards', predecessor, node['id'])
        for alternative in node.get('exclusive', []):
            assert alternative in by_id, ('Missing exclusive alternative', alternative)
            assert node['xy'][1] == by_id[alternative]['xy'][1], (
                'Exclusive choices must share a row', node['id'], alternative)


def arrange(nodes, groups):
    """Mutate only coordinates/origins in place and prove semantic preservation."""
    before = _semantic_snapshot(nodes, groups)
    previous_origins = {group['id']: tuple(group['origin']) for group in groups}
    assert set(previous_origins) == set(ORIGINS), 'Review new group footprints first'
    for node in nodes:
        group_id = node['group']
        old_x, old_y = previous_origins[group_id]
        local = POSITIONS.get(node['id'].removeprefix('ISR2_'))
        if local is None:
            local = (node['xy'][0] - old_x, node['xy'][1] - old_y)
        new_x, new_y = ORIGINS[group_id]
        node['xy'] = [new_x + local[0], new_y + local[1]]
    for group in groups:
        group['origin'] = list(ORIGINS[group['id']])
    assert before == _semantic_snapshot(nodes, groups), 'Layout changed focus semantics'
    _verify_geometry(nodes, groups)
