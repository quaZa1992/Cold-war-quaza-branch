# IMPERIA COLD WAR — France tangible policy trade-offs.
"""Apply the user's later instruction without changing immutable approvals."""
from copy import deepcopy

REVISION = 'France tangible trade-offs, 29 October 2026'
AUTHORISATION = 'Shared Components soll einen realistischeren debuff haben. influence juckt keine sau im spoiel. achte auf ähnliceh fälle und behebe die auch'

# Focus, affected side, old modifier, replacement, value, political description.
CHANGES = [
    ('pooled_armour', 'effects', 'foreign_influence_modifier', 'production_factory_efficiency_gain_factor', -.08,
     'Standardise components and negotiate joint procurement with partners. Common orders lower equipment expenditure, but shared specifications and industrial work-sharing slow the adaptation of production lines.'),
    ('jaguar_doctrine', 'effects', 'foreign_influence_modifier', 'airforce_personnel_cost_multiplier_modifier', .05,
     'Build training around the Anglo-French Jaguar and common operating standards. Joint instruction improves aircrew preparation and fuel discipline, but requires permanent instructor posts and specialist ground crews.'),
    ('escort_navy', 'effects', 'foreign_influence_modifier', 'navy_personnel_cost_multiplier_modifier', .05,
     'Prioritise escorts, maintenance and protection of French approaches. Reliable routine coverage requires continuously staffed patrols, technical crews and a larger naval personnel bill.'),
    ('open_computers', 'effects', 'foreign_influence_modifier', 'corporate_tax_income_multiplier_modifier', -.03,
     'Adopt international standards and concentrate French engineering on competitive niches. Compatibility accelerates renewal, while foreign licensing and support payments reduce the taxable returns retained by French firms.'),
    ('fn_protection', 'effects', 'foreign_influence_modifier', 'research_speed_factor', -.03,
     'Shelter French producers from external competition. Protected markets support local investment, but weaker competition and restricted technical exchange slow research and reduce civilian productivity.'),
    ('atlantic_liberal', 'france', 'foreign_influence_defense_modifier', 'corporate_tax_income_multiplier_modifier', -.03,
     'Negotiate licensing, technical support and export access with American electronics firms. Faster access to expertise and stronger service output come with royalty payments that reduce French taxable returns.'),
    ('soviet_friendship', 'france', 'foreign_influence_defense_modifier', 'production_speed_arms_factory_factor', -.05,
     'Offer industrial equipment, engineering and production cooperation to the Soviet government. Funded orders support civilian investment in both countries, while the French export commitment diverts engineering capacity from arms-factory expansion.'),
    ('pcf_energy_contract', 'france', 'foreign_influence_defense_modifier', 'education_cost_multiplier_modifier', .04,
     'Concentrate the industrial partnership on joint energy studies, equipment and efficient use. France lowers industrial energy demand and Soviet partners improve generation; both countries must fund specialist technical training.'),
    ('fn_export', 'france', 'foreign_influence_defense_modifier', 'airforce_personnel_cost_multiplier_modifier', .04,
     'Offer aviation training, engineering and export support to Argentina. Orders support French firms and Argentine readiness, while France must maintain instructor detachments and technical personnel.'),
    ('atlantic_training', 'france', 'foreign_influence_modifier', 'army_personnel_cost_multiplier_modifier', .04,
     'Negotiate technical training and logistics cooperation with the United States. Better coordination requires permanent French liaison and training cadres, while forces remain outside NATO integrated command.'),
    ('iran_energy', 'france', 'foreign_influence_modifier', 'corporate_tax_income_multiplier_modifier', -.03,
     'Negotiate energy engineering and technical cooperation with Iran. Generation gains come with commercial concessions and long-term service commitments that reduce the French taxable returns retained from the programme.'),
]


def apply_balance_revision(source):
    design = deepcopy(source)
    nodes = {n['key']: n for n in design['nodes']}
    for key, side, old, replacement, value, description in CHANGES:
        node = nodes[key]
        effects = node['effects'] if side == 'effects' else node['offer'][side]['effects']
        matches = [e for e in effects if e.get('kind') == 'modifier' and e.get('key') == old and e['value'] < 0]
        assert len(matches) == 1, (key, side, old)
        assert not any(e.get('key') == replacement for e in effects), (key, replacement)
        matches[0].update(key=replacement, value=value)
        node['description'] = description
    design['balance_revision'] = {'project': 'IMPERIA COLD WAR', 'revision': REVISION,
                                  'authorisation': AUTHORISATION, 'changed_focuses': [c[0] for c in CHANGES]}
    return design
