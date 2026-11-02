# IMPERIA COLD WAR — Cuba branch layout and restored medical continuation.
"""User-requested repair layered over immutable approved design snapshots.

Keep every focus identity, reward, duration, exclusion and consent contract.
Only the medical fork regains the OR predecessor lost in consolidation.
"""
from copy import deepcopy

P = 'COLDWAR_CUB_'

# Parallel diplomatic offers share one row. Their continuation lanes stay clear
# of unrelated cards. Soviet and DDR roots remain independent beside each other.
POSITIONS = {
    'foreign_diplomacy': (56, 0),
    'foreign_overseas': (36, 2),
    'foreign_advisers': (34, 4),
    'foreign_expeditionary': (38, 4),
    'foreign_angola': (34, 6),
    'foreign_ethiopia': (38, 6),
    'foreign_interests': (44, 2),
    'foreign_limited': (42, 4),
    'foreign_settlement': (46, 4),
    'foreign_mex_fuel': (50, 2),
    'foreign_mex_agro': (54, 2),
    'foreign_spr_nickel': (58, 2),
    'foreign_spr_training': (62, 2),
    'foreign_can_rail': (66, 2),
    'foreign_can_fisheries': (70, 2),
    'foreign_caribbean': (74, 2),
    'foreign_algeria': (78, 2),
    'foreign_soviet': (44, 7),
    'foreign_cmea': (42, 9),
    'foreign_specialisation': (42, 10),
    'foreign_sov_commodity': (46, 9),
    'foreign_sov_industry': (50, 9),
    'foreign_symbolic': (58, 7),
    'foreign_cession': (62, 7),
    'foreign_ddr': (60, 9),
    'foreign_ddr_industry': (58, 11),
    'foreign_ddr_science': (62, 11),
}
MILITARY_KEYS = ('far_reorganisation', 'territorial_defence', 'air_defence',
                 'coastal_patrols', 'civil_military_pact', 'foreign_overseas',
                 'foreign_advisers', 'foreign_expeditionary', 'foreign_angola',
                 'foreign_ethiopia')
MEDICAL_PARENTS = [[P + 'rural_clinics', P + 'teaching_hospitals']]


def apply_layout_repair(model):
    result = deepcopy(model)
    by = {node['key']: node for node in result['nodes']}
    for key, xy in POSITIONS.items():
        by[key]['xy'] = list(xy)
    for key in POSITIONS:
        node = by[key]
        if key in ('foreign_diplomacy', 'foreign_soviet', 'foreign_symbolic', 'foreign_cession'):
            anchor = None
        elif key in MILITARY_KEYS:
            anchor = P + 'far_reorganisation'
        elif key in ('foreign_cmea', 'foreign_specialisation', 'foreign_sov_commodity', 'foreign_sov_industry'):
            anchor = P + 'foreign_soviet'
        elif key in ('foreign_ddr', 'foreign_ddr_industry', 'foreign_ddr_science'):
            anchor = P + 'foreign_symbolic'
        else:
            anchor = P + 'foreign_diplomacy'
        node['anchor'] = anchor
        origin = by[anchor.removeprefix(P)]['xy'] if anchor else node['xy']
        node['local_xy'] = [node['xy'][i] - origin[i] for i in (0, 1)]
    for key in ('medical_brigades', 'retain_doctors'):
        assert by[key]['prerequisites'] in ([], MEDICAL_PARENTS)
        by[key]['prerequisites'] = deepcopy(MEDICAL_PARENTS)
    for group in result['groups']:
        if group['id'] == 'foreign':
            group['root'] = list(POSITIONS['foreign_diplomacy'])
    result['project'] = 'IMPERIA COLD WAR'
    result['layout_repair'] = 'Cuba branch layout and restored medical OR continuation, 25 October 2026'
    return result
