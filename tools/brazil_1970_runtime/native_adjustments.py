# IMPERIA COLD WAR — Brazil native modifier corrections after engine verification.
from copy import deepcopy

REPLACEMENTS = {
    'military_spending_cost_multiplier_modifier': 'personnel_cost_multiplier_modifier',
    'inflation_gain_multiplier_modifier': 'inflation_cost_multiplier_modifier',
}

def runtime_design(approved):
    """Keep the approval immutable and record the narrower supported translations."""
    d = deepcopy(approved)
    changes = []
    def visit(v, path):
        if isinstance(v, dict):
            if v.get('kind') == 'modifier' and v.get('key') in REPLACEMENTS:
                old = v['key']; v['key'] = REPLACEMENTS[old]
                changes.append(dict(path=path, approved_key=old, runtime_key=v['key'], value=v['value']))
            for k, child in v.items():
                if isinstance(child, (dict, list)): visit(child, path+'/'+str(k))
        elif isinstance(v, list):
            for i, child in enumerate(v): visit(child, path+'/'+str(i))
    visit(d, '')
    descriptions = {
        'monetary': 'Restrain public commitments and reduce the fiscal cost of inflation. Tighter demand slows investment.',
        'investment': 'Protect productive investment while accepting more expensive public commitments during inflation.',
        'price_restraint': 'Tighten indexation and credit commitments to reduce the public cost of inflation. Investment slows. This does not recreate the 1990 deposit freeze.',
    }
    # Select by the immutable approved title rather than assume internal key names.
    by_title = {
        'Monetary Restraint': descriptions['monetary'],
        'Investment Compact': descriptions['investment'],
        'Price Restraint': descriptions['price_restraint'],
    }
    for n in d['nodes']:
        if n['title'] in by_title: n['description'] = by_title[n['title']]
    for key in ('labels', 'modifier_labels', 'modifier_names'):
        if key in d:
            for old, new in REPLACEMENTS.items():
                if old in d[key]: del d[key][old]
            d[key]['personnel_cost_multiplier_modifier'] = 'Personnel Cost'
            d[key]['inflation_cost_multiplier_modifier'] = 'Inflation Cost'
    d['native_modifier_corrections'] = dict(
        project='IMPERIA COLD WAR', source='First isolated native engine run, 2 November 2026',
        reason='The engine rejected two unregistered modifier names in the approved concept.',
        scope='Personnel cost replaces total military spending cost. Inflation-related fiscal costs replace inflation-rate growth; these policies do not directly change the inflation rate.',
        entries=changes,
    )
    return d
