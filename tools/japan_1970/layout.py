# IMPERIA CW — Cold War: Japan focus presentation and section anchors.
"""Current presentation of the approved graph; no gameplay data is changed."""
from copy import deepcopy

GRID = (96, 130)
# A section reserves its whole footprint. National institutions occupy the left,
# the economy and diplomacy the right; all five party programmes form one band.
SECTION_ORIGINS = {
    0: (0, 0), 1: (14, 0), 2: (28, 0), 3: (42, 0),
    4: (14, 7), 5: (28, 7), 6: (42, 7),
    7: (14, 14), 8: (28, 14), 9: (42, 14), 10: (14, 21),
    11: (56, 0), 12: (66, 0), 13: (76, 0), 14: (86, 0),
    15: (56, 8), 16: (66, 8), 17: (76, 8), 18: (86, 8),
    19: (56, 16), 20: (66, 16), 21: (76, 16), 22: (86, 16),
    23: (56, 25), 24: (66, 25), 25: (76, 25), 26: (86, 25),
    27: (0, 35), 28: (20, 35), 29: (40, 35),
    30: (60, 35), 31: (80, 35),
}
# This panel fits below the long constitutional spine, outside every card.
CONTINUOUS_POSITION = (0, 2150)


def apply_layout(approved):
    design = deepcopy(approved)
    for index, section in enumerate(design['sections']):
        ox, oy = SECTION_ORIGINS[index]
        if index >= 27:
            # Separate dense policy fans from their join rows. The extra blank
            # connector rows prevent long routes from crossing sibling cards.
            party = section['nodes'][0]['id'].split('_', 1)[0]
            positions = {
                'mandate': (8, 0),
                **{f'policy_{i}': (i * 4, 1) for i in range(5)},
                'institutions': (0, 3), 'industry': (5, 3),
                'society': (11, 3), 'diplomacy': (16, 3),
                'programme': (8, 5), 'deep_policy_charter': (8, 10),
            }
            for fork in range(3):
                for side, dx in (('a', 0), ('b', 4)):
                    positions[f'deep_fork{fork}_{side}'] = (fork * 6 + dx, 7)
                    positions[f'deep_fork{fork}_{side}_follow'] = (fork * 6 + dx, 8)
            for node in section['nodes']:
                node['x'], node['y'] = positions[node['id'][len(party) + 1:]]
        elif index <= 10:
            section['nodes'][0]['x'] = 5
        elif index == 19:
            # Keep the independent logistics arm outside the exclusive pair;
            # neither its card nor its prerequisite crosses the choice line.
            for node in section['nodes']:
                if node['id'] == 'pacific_logistics':
                    node['x'], node['y'] = 6, 5
                elif node['id'] in ('alliance_autonomy', 'alliance_integration'):
                    node['y'] = 6
        for node in section['nodes']:
            node['globalX'] = ox + node['x']
            node['globalY'] = oy + node['y']
    return design
