# IMPERIA COLD WAR — Israel 2.2 compact native focus-tree arrangement.
"""Convert the immutable approved catalogue into native MD grid coordinates.

``arrange(data)`` returns a deep copy. Only coordinates, group origins and the
preview's pixel conversion change. This module has no file I/O or mod emission.
Native artwork must fit the 112 x 72 symbol canvas described by NATIVE below.
"""
from copy import deepcopy
from itertools import combinations


NATIVE = {
    'x_unit': 96,
    'y_unit': 130,
    'node_width': 165,
    'node_height': 128,
    'symbol_width': 112,
    'symbol_height': 72,
    'symbol_center': [87.5, 20],
    'title_bounds': [15, 58, 162, 78],
    'title_background_bounds': [5, 40, 169, 90],
    'link_begin': [80, 64],
    'link_end': [80, 0],
}

# Leftmost local card column and top row. A one-column gutter separates the
# nearest full programme footprints. Smaller parties fill actual free pockets.
PLACEMENT = {
    'institutions': (0, 0),
    'capital': (9, 0),
    'absorption': (18, 0),
    'water': (27, 0),
    'reserves': (0, 7),
    'arsenal': (13, 7),
    'diplomacy': (26, 7),
    'territories': (0, 14),
    'mafdal': (11, 14),
    'orthodox': (21, 14),
    'rakah': (30, 14),
    'maki': (30, 19),
    'mapam': (21, 22),
    'free_center': (30, 23),
    'alignment': (0, 27),
    'gahal': (11, 27),
    'liberals': (24, 27),
    'haolam': (31, 27),
    'state_list': (31, 35),
}

# Values are relative to the approved programme origin. Unlisted focuses retain
# their approved local offset. These changes clear real native-style links;
# none replaces a prerequisite with an invisible availability condition.
LOCAL = {
    'religious_concord': (-3, 3),
    'civil_charter': (3, 3),
    'diamond_desk': (-1, 1),
    'bonds_plant': (1, 2),
    'credit_guarantees': (-2, 2),
    'financing_usa': (-3, 6),
    'financing_ger': (0, 6),
    'financing_rom': (3, 6),
    # Early, separate exercise and call-up actions occupy the reserve fan's
    # outside columns; releasing the call-up remains beneath its own focus.
    'reserve_exercise': (-5, 1),
    'reserve_callup': (5, 1),
    'reserve_release': (5, 2),
    'security_emergency': (-5, 3),
    'tal_tank': (-5, 2),
    'gabriel': (-1, 2),
    'civil_spillover': (1, 3),
    'arms_exports': (3, 4),
    'arms_congo': (1, 5),
    'washington': (1, 1),
    'jarring_channel': (-5, 1),
    # Interleaved columns keep the root's long regional action connections
    # between, rather than through, the earlier development medallions.
    'cap_projects': (4, 1),
    'west_bank_projects': (-5, 4),
    'foreign_footholds': (-4, 5),
    'gaza_foothold': (-2, 5),
    'sinai_foothold': (0, 5),
    'golan_foothold': (2, 5),
    'funded_network': (-2, 6),
    'close_west_bank': (-3, 7),
    'close_gaza': (-1, 7),
    'close_sinai': (1, 7),
    'close_golan': (3, 7),
    'labor_indexed_savings': (-1, 9),
    'gahal_arbitration': (-5, 4),
    'gahal_health_bill': (5, 2),
    'gahal_big_bang': (-5, 6),
    'gahal_daily_workers': (5, 6),
    'gahal_pensions': (5, 8),
    'mafdal_bar_ilan': (-1, 6),
    'mafdal_cooperative_bank': (1, 6),
    'religious_agriculture': (4, 2),
    'orthodox_cooperative_plant': (2, 6),
}


def semantic(data):
    """Return the complete catalogue semantics, excluding spatial metadata."""
    result = deepcopy(data)
    result.pop('layout', None)
    for node in result['nodes']:
        node.pop('xy', None)
    for group in result['groups']:
        group.pop('origin', None)
    return result


def _overlap(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


def _segment_hits(a, b, box):
    left, top, right, bottom = box
    if a[0] == b[0]:
        return left < a[0] < right and max(min(a[1], b[1]), top) < min(max(a[1], b[1]), bottom)
    assert a[1] == b[1], 'Connector must be orthogonal'
    return top < a[1] < bottom and max(min(a[0], b[0]), left) < min(max(a[0], b[0]), right)


def connector(source, target):
    """Approximate native link anchors with a middle-row orthogonal join.

    This is a collision model, not control of the game's internal link router.
    """
    x1, y1 = source['xy'][0] * 96 + 80, source['xy'][1] * 130 + 64
    x2, y2 = target['xy'][0] * 96 + 80, target['xy'][1] * 130
    mid = (y1 + y2) / 2
    return [(x1, y1), (x1, mid), (x2, mid), (x2, y2)]


def audit(data):
    """Check full containers, programme footprints and actual visible artwork.

    Full native containers include empty connector space below the title.
    Route checks therefore use the union of normalized symbol and title bounds,
    while sibling-card checks conservatively reserve all 165 x 128 pixels.
    """
    nodes = data['nodes']
    by_id = {node['id']: node for node in nodes}
    assert len(by_id) == len(nodes), 'Duplicate focus ID'
    cards = {key: (n['xy'][0] * 96, n['xy'][1] * 130,
                   n['xy'][0] * 96 + 165, n['xy'][1] * 130 + 128)
             for key, n in by_id.items()}
    visible = {key: (box[0] + 5, box[1] - 16, box[0] + 169, box[1] + 90)
               for key, box in cards.items()}
    for a, b in combinations(by_id, 2):
        assert not _overlap(cards[a], cards[b]), ('Native container collision', a, b)
        assert not _overlap(visible[a], visible[b]), ('Native art/title collision', a, b)
    footprints = {}
    for group in data['groups']:
        members = [cards[node['id']] for node in nodes if node['group'] == group['id']]
        assert members, ('Empty programme', group['id'])
        # The native title background extends four pixels beyond its nominal
        # 165px container. Ten-pixel side clearance includes that overhang while
        # preserving three clear pixels in the narrowest 23px inter-group gap.
        footprints[group['id']] = (min(box[0] for box in members) - 10,
                                   min(box[1] for box in members) - 16,
                                   max(box[2] for box in members) + 4 + 10,
                                   max(box[3] for box in members) + 12)
    for a, b in combinations(footprints, 2):
        assert not _overlap(footprints[a], footprints[b]), ('Programme collision', a, b)
    edges = 0
    for node in nodes:
        for alternative in node.get('exclusive', []):
            assert node['xy'][1] == by_id[alternative]['xy'][1], ('Exclusive alternatives off row', node['id'], alternative)
        for row in node.get('pre', []):
            for predecessor in row:
                source = by_id[predecessor]
                assert source['xy'][1] < node['xy'][1], ('Non-descending prerequisite', predecessor, node['id'])
                points = connector(source, node)
                for key, bounds in visible.items():
                    if key not in (predecessor, node['id']):
                        assert not any(_segment_hits(a, b, bounds) for a, b in zip(points, points[1:])), ('Native-style link crosses visible focus', predecessor, node['id'], key)
                edges += 1
    all_boxes = list(cards.values())
    return {
        'project': 'IMPERIA COLD WAR', 'nodes': len(nodes), 'groups': len(footprints),
        'edges': edges, 'card_collisions': 0, 'visible_link_collisions': 0,
        'footprints': {key: list(box) for key, box in footprints.items()},
        'bounds': [min(b[0] for b in all_boxes), min(b[1] for b in all_boxes),
                   max(b[2] for b in all_boxes), max(b[3] for b in all_boxes)],
        'visible_image_bounds_relative': [5, -16, 169, 90],
        'title_background_bounds_relative': [5, 40, 169, 90],
        'native_engine_routing_tested': False,
    }


def arrange(data):
    """Deep-copy the catalogue into a compact native grid without gameplay edits."""
    result = deepcopy(data)
    before = semantic(data)
    groups = {group['id']: group for group in result['groups']}
    assert set(groups) == set(PLACEMENT), 'New programme needs native footprint review'
    extra_capital_row = int(any(n['id'] == 'ISR2_financing_usa' for n in result['nodes']))
    for key, group in groups.items():
        origin = group['origin']
        children = [n for n in result['nodes'] if n['group'] == key]
        local = {n['id']: LOCAL.get(n['id'].removeprefix('ISR2_'),
                                   (n['xy'][0] - origin[0], n['xy'][1] - origin[1]))
                 for n in children}
        left, top = PLACEMENT[key]
        if top:
            top += extra_capital_row
        base_x = left - min(x for x, y in local.values())
        group['origin'] = [base_x, top]
        for node in children:
            x, y = local[node['id']]
            node['xy'] = [base_x + x, top + y]
    result['layout'].update(deepcopy(NATIVE))
    assert semantic(result) == before, 'Native layout changed catalogue semantics'
    audit(result)
    return result
