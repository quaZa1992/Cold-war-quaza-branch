# IMPERIA COLD WAR — Authorized French agreement and doctrine rebalance.
"""Apply later player requests without rewriting immutable approved snapshots."""
from copy import deepcopy

REMOVED_FRENCH_DOCTRINE = {
    'fp_gabon_officers', 'fp_chad_cadres',
    'fp_niger_field_services', 'fp_lebanon_field',
}
DESCRIPTION_REVISIONS = {
    'atlantic_liberal': 'Negotiate licensing, technical support and export access with American electronics firms. Faster access to expertise and stronger service output require continuing licensing and technical support expenditure.',
    'iran_energy': 'Negotiate energy engineering and technical cooperation with Iran. Generation gains come with commercial commitments and continuing French expenditure on technical services.',
    'fp_senegal_clearing': 'Offer Dakar French-backed clearing and banking services on privileged commercial terms. Senegal receives practical financial capacity, while contracted service fees favour the French providers.',
}


def apply_deal_balance_revision(design):
    out = deepcopy(design)
    removed, doctrine_changes = [], []
    for node in out['nodes']:
        key = node['key']
        if key in DESCRIPTION_REVISIONS:
            node['description'] = DESCRIPTION_REVISIONS[key]
        for side in ('france', 'recipient'):
            effects = node.get('offer', {}).get(side, {}).get('effects', [])
            for effect in list(effects):
                if (effect.get('kind') == 'modifier'
                        and effect.get('key') == 'corporate_tax_income_multiplier_modifier'
                        and effect['value'] < 0):
                    effects.remove(effect)
                    removed.append({'focus': key, 'side': side, 'effect': effect})
        for location, effects in (
                ('national', node.get('effects', [])),
                ('agreement_france', node.get('offer', {}).get('france', {}).get('effects', []))):
            for effect in list(effects):
                if effect.get('kind') != 'doctrine' or effect.get('category') != 'land_doctrine':
                    continue
                old = deepcopy(effect)
                if key in REMOVED_FRENCH_DOCTRINE and location == 'agreement_france':
                    effects.remove(effect)
                    new = None
                else:
                    cap = .10 if key.startswith('fp_') else .15 if key.startswith('nato_') else .25
                    effect['reduction'] = min(effect['reduction'], cap)
                    effect['uses'] = 1
                    new = deepcopy(effect)
                if old != new:
                    doctrine_changes.append({'focus': key, 'location': location, 'before': old, 'after': new})
    out['deal_balance_revision'] = {
        'project': 'IMPERIA COLD WAR', 'date': '2026-10-30',
        'authorization': [
            '- Corporate Tax Income Multiplier: -3% das kann weg vom niger dings, und vergleichbaren deals',
            '- Land Doctrine: -50% cost, 1 use viel zu viel, frankreich darf nicht so viel erhalten.',
        ],
        'removed_negative_agreement_tax_modifiers': removed,
        'french_land_doctrine_changes': doctrine_changes,
    }
    return out
