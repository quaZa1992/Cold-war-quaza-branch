# IMPERIA CW — Cold War: greece 1970 — rewards.
"""Complete the missing effects in the original Greek design snapshot.

Values use the existing MD modifier catalogue in EFFECTS_REVIEW.json. This is
an explicit content revision: the snapshot is retained, rather than silently
pretending the old flag-only implementation already contained these benefits.
"""
from copy import deepcopy


def apply_rewards(data):
    p = data['prefix']
    by = {n['key']: n for n in data['focuses']}
    changes = {}

    def programme(key, mods, slot=None, research=None, states=None, note=''):
        n = by[key]
        before = deepcopy(n['modifiers'])
        n['modifiers'].update(mods)
        if slot: n['modifier_slot'] = slot
        if research: n['research_bonuses'] = [{'category': category, 'bonus': bonus, 'uses': 1} for category, bonus in research]
        if states: n['state_programme'] = deepcopy(states)
        n['implementation_note'] = note
        changes[key] = {'before': before, 'after': deepcopy(n['modifiers']), 'slot': n['modifier_slot'],
                        'research_bonuses': n.get('research_bonuses', []), 'state_programme': n.get('state_programme'), 'note': note}

    # These were paid, empty programme stages in the runtime. Government
    # programmes occupy common replacement slots, never seven cumulative sets.
    models = {
        'pap': {'production_speed_industrial_complex_factor': .08, 'industrial_capacity_factory': .05, 'bureaucracy_cost_multiplier_modifier': .04},
        'ioa': {'industrial_capacity_factory': .06, 'production_speed_industrial_complex_factor': -.03, 'bureaucracy_cost_multiplier_modifier': .05},
        'nd': {'production_speed_industrial_complex_factor': .08, 'production_factory_efficiency_gain_factor': .05, 'corporate_tax_income_multiplier_modifier': .04},
        'centre': {'research_speed_factor': .04, 'productivity_growth_modifier': .02, 'education_cost_multiplier_modifier': .06},
        'pasok': {'industrial_capacity_factory': .06, 'productivity_growth_modifier': .03, 'social_cost_multiplier_modifier': .08},
        'kke': {'industrial_capacity_factory': .08, 'production_speed_industrial_complex_factor': .06, 'bureaucracy_cost_multiplier_modifier': .05, 'social_cost_multiplier_modifier': .06},
        'royal': {'tax_gain_multiplier_modifier': .04, 'production_speed_industrial_complex_factor': .06, 'bureaucracy_cost_multiplier_modifier': -.03},
    }
    civil = {
        'pap': ({'productivity_growth_modifier': .02, 'education_cost_multiplier_modifier': .02}, {'political_power_gain': .05, 'bureaucracy_cost_multiplier_modifier': .03}),
        'ioa': ({'political_power_gain': .05, 'police_cost_multiplier_modifier': .04}, {'supply_consumption_factor': -.02, 'bureaucracy_cost_multiplier_modifier': .02}),
        'nd': ({'tax_gain_multiplier_modifier': .02, 'bureaucracy_cost_multiplier_modifier': .02}, {'supply_consumption_factor': -.02, 'social_cost_multiplier_modifier': .02}),
        'centre': ({'police_cost_multiplier_modifier': -.03, 'bureaucracy_cost_multiplier_modifier': .02}, {'political_power_gain': .04, 'social_cost_multiplier_modifier': .02}),
        'pasok': ({'productivity_growth_modifier': .02, 'social_cost_multiplier_modifier': .03}, {'production_factory_efficiency_gain_factor': .025, 'bureaucracy_cost_multiplier_modifier': .03}),
        'kke': ({'productivity_growth_modifier': .025, 'social_cost_multiplier_modifier': .02}, {'production_factory_efficiency_gain_factor': .03, 'bureaucracy_cost_multiplier_modifier': .04}),
        'royal': ({'bureaucracy_cost_multiplier_modifier': -.02, 'political_power_gain': .025}, {'supply_consumption_factor': -.02, 'bureaucracy_cost_multiplier_modifier': .03}),
    }
    fiscal = {
        'pap': {'tax_gain_multiplier_modifier': .025, 'projects_cost_modifier': -.03},
        'ioa': {'projects_cost_modifier': -.04, 'tax_gain_multiplier_modifier': .02},
        'nd': {'tax_gain_multiplier_modifier': .03, 'interest_rate_multiplier_modifier': -.03},
        'centre': {'tax_gain_multiplier_modifier': .04, 'bureaucracy_cost_multiplier_modifier': -.02},
        'pasok': {'tax_gain_multiplier_modifier': .035, 'corporate_tax_income_multiplier_modifier': .025},
        'kke': {'tax_gain_multiplier_modifier': .03, 'projects_cost_modifier': -.03},
        'royal': {'tax_gain_multiplier_modifier': .03, 'bureaucracy_cost_multiplier_modifier': -.02},
    }
    for route in models:
        programme(route + '_7', models[route], 'government_economic_model',
                  note='A funded economic model for the current government; replaced when executive authority changes.')
        for index, mods in zip((4, 5), civil[route]):
            programme(route + '_' + str(index), mods, 'government_civil_administration',
                      note='Implements the selected institutional bargain. Its recurring costs remain active with its benefits.')
        programme(route + '_12', fiscal[route], 'government_fiscal_programme',
                  note='A funded fiscal audit changes tax collection and administration; it does not delete public debt.')

    # Give the existing 365-day construction programmes their actual subject:
    # hotels differ from export credit, hospitals from cooperative services.
    temporary = {
        'pap_10': {'office_park_income_tax_modifier': .04},
        'pap_11': {'industrial_capacity_factory': .04},
        'ioa_10': {'industrial_capacity_factory': .04},
        'ioa_11': {'production_factory_efficiency_gain_factor': .04},
        'nd_10': {'production_factory_efficiency_gain_factor': .04},
        'nd_11': {'productivity_growth_modifier': .04},
        'centre_10': {'corporate_tax_income_multiplier_modifier': .04},
        'centre_11': {'productivity_growth_modifier': .04},
        'pasok_10': {'social_cost_multiplier_modifier': -.03},
        'pasok_11': {'productivity_growth_modifier': .04},
        'kke_10': {'production_factory_efficiency_gain_factor': .04},
        'kke_11': {'industrial_capacity_factory': .04},
        'royal_10': {'productivity_growth_modifier': .04},
        'royal_11': {'corporate_tax_income_multiplier_modifier': .04},
    }
    for key, mods in temporary.items():
        programme(key, mods, note='A 365-day implementation programme. Expiry does not recreate the programme or repeat its payment.')

    programme('economy_4', {'productivity_growth_modifier': .025}, 'industrial_standards', [('CAT_construction', .25)],
              note='Industrial standards improve productivity growth and grant one targeted construction research bonus.')
    programme('economy_5', {'production_factory_efficiency_gain_factor': .025, 'corporate_tax_income_multiplier_modifier': .02}, 'sme_finance',
              note='Funded SME guarantees improve efficiency gain and the corporate tax base; they do not add free cash.')
    programme('economy_10', {}, states={'states': [139, 142, 974], 'modifiers': {'state_productivity_growth_modifier': .04}},
              research=[('CAT_agriculture', .25)], note='Irrigation and veterinary services improve only the specified owned and controlled rural states.')
    programme('economy_11', {}, states={'states': [139, 142, 974], 'modifiers': {'state_production_speed_buildings_factor': .04}},
              note='Rural logistics improve construction locally; no national bonus is claimed for an unimplemented state project.')
    programme('economy_18', {'tax_gain_multiplier_modifier': .04}, 'professional_tax_collection',
              note='Professional tax collection removes the clientelism spirit and improves revenue; the audit reduces corruption by one level only above its floor.')
    by['economy_18']['corruption_reduction'] = True
    programme('economy_19', {'industrial_capacity_factory': .025, 'productivity_growth_modifier': .015}, 'resilient_expansion',
              note='A funded capstone improves output and gradual productivity rather than setting GDP directly.')

    programme('army_4', {}, research=[('CAT_command_and_control_equipment', .20)], note='Promotion rules provide their existing army XP and a targeted command-equipment research bonus.')
    programme('army_5', {'experience_gain_army_factor': .05}, 'officer_training', note='Merit boards improve training experience; existing one-time XP is retained.')
    programme('army_6', {'army_defence_factor': .03}, 'professional_command', note='Professional command replaces the politicised-officer penalty with an implemented defensive organisation benefit.')
    programme('army_10', {'supply_consumption_factor': -.025}, 'army_transport', [('CAT_command_and_control_equipment', .25)], note='Funded transport and signals improve supply use and command research.')
    programme('army_11', {'supply_consumption_factor': -.02}, 'army_stores', note='Dispersed stores reduce the operational supply burden; no equipment is spawned.')
    programme('army_15', {'production_factory_efficiency_gain_factor': .02}, 'army_workshops', [('CAT_small_arms', .25)])
    programme('army_16', {}, research=[('CAT_artillery', .25)], note='A supplier-approved procurement dossier grants research capacity, not free imported weapons.')
    programme('army_18', {'experience_gain_army_factor': .05}, 'field_exercises')
    programme('army_19', {'army_defence_factor': .02}, 'defence_doctrine', [('CAT_small_arms', .25)])

    programme('navy_4', {}, research=[('CAT_submarines', .25)], note='The existing navy XP is retained; one submarine research bonus supports the selected mission.')
    programme('navy_5', {}, research=[('CAT_frigates', .25)], note='The existing navy XP is retained; one frigate research bonus supports convoy escort.')
    programme('navy_11', {'navy_max_range_factor': .05}, 'island_fleet_support')
    programme('navy_15', {'office_park_income_tax_modifier': .03}, 'shipping_registry')
    programme('navy_16', {'industrial_capacity_dockyard': .04}, 'domestic_yard_orders', [('CAT_naval_engines', .25)])
    programme('navy_18', {'naval_morale_factor': .03}, 'damage_control')
    programme('navy_19', {'industrial_capacity_dockyard': .04}, 'sustainable_fleet', [('CAT_frigates', .25)])

    programme('air_4', {}, research=[('CAT_electronics', .25)])
    programme('air_5', {}, research=[('CAT_air_to_ground_weapons', .25)])
    programme('air_10', {'air_accidents_factor': -.03}, 'airframe_workshops', [('CAT_air_engines', .25)])
    programme('air_11', {'air_accidents_factor': -.02}, 'instructor_access', note='Instructor access requires supplier acceptance; training reduces accidents without creating aircraft.')
    programme('air_15', {'air_accidents_factor': -.02}, 'protected_ground_services')
    programme('air_16', {}, research=[('CAT_electronics', .25)])
    programme('air_18', {'projects_cost_modifier': -.02}, 'air_procurement_budget', [('CAT_aircraft', .25)])
    programme('air_19', {'air_accidents_factor': -.03}, 'air_maintenance', [('CAT_air_engines', .25)])

    programme('foreign_4', {'bureaucracy_cost_multiplier_modifier': .02}, 'independent_monitoring', note='Independent monitoring has a real administrative cost and enables an accepted rehabilitation dossier.')
    programme('foreign_5', {'foreign_influence_defense_modifier': -.02, 'political_power_gain': .025}, 'censure_response', note='The government retains autonomy of action while continued censure has a diplomatic cost.')
    programme('foreign_10', {'supply_consumption_factor': -.015}, 'reciprocal_access', note='The operational benefit activates only after the named counterpart accepts.')
    programme('foreign_11', {'army_defence_factor': .015}, 'national_command')
    programme('foreign_15', {'corporate_tax_income_multiplier_modifier': .02}, 'balkan_trade', note='Only an accepted Yugoslav commercial agreement enables the domestic revenue benefit.')
    programme('foreign_16', {'office_park_income_tax_modifier': .02}, 'shipping_diplomacy')
    programme('foreign_18', {'foreign_influence_defense_modifier': .03}, 'diplomatic_service')
    programme('foreign_19', {'projects_cost_modifier': -.02}, 'negotiated_commitments')

    programme('cyprus_18', {'social_cost_multiplier_modifier': .02, 'stability_factor': .01}, 'crisis_relief', note='Domestic relief administration improves stability but retains its ongoing social cost. It neither erases Cypriot losses nor transfers foreign territory.')
    programme('cyprus_19', {'bureaucracy_cost_multiplier_modifier': .02, 'stability_factor': .02}, 'crisis_reconstruction', note='Reconstruction and missing-person casework require recorded harm and an accepted settlement; victim claims survive.')
    programme('pasok_return_narrow', {'social_cost_multiplier_modifier': .02}, 'return_restitution', note='A limited return programme retains excluded refugees’ claims and has a smaller processing budget.')
    programme('pasok_return_equal', {'social_cost_multiplier_modifier': .04, 'productivity_growth_modifier': .02}, 'return_restitution', note='Equal return and property processing cost more and support broader productive reintegration.')
    programme('energy_diversify', {'projects_cost_modifier': -.02}, 'energy_diversification', note='Supplier-approved diversification funds domestic resilience; it never generates imported fuel for free.')
    programme('aegean_1', {}, research=[('CAT_electronics', .20)], note='Funded hydrographic and legal surveys develop research capacity; they do not establish title to the shelf.')
    programme('aegean_3', {}, research=[('CAT_infrastructure', .20)], note='Licensed exploration develops domestic engineering; it does not create a commercial oil deposit.')
    programme('aegean_6', {'bureaucracy_cost_multiplier_modifier': .01}, 'aegean_legal_dossier', note='A legal dossier has a recurring administrative cost; jurisdiction still requires the counterpart’s valid consent.')

    # State reconstruction is an implemented local measure, not a way to erase
    # recorded human losses merely by completing a national focus.
    by['cyprus_19']['required_settlement'] = True
    for key in changes:
        n = by[key]
        n['idea_definition'] = 'modifier = { ' + ' '.join(k + ' = ' + str(v) for k, v in n['modifiers'].items()) + ' }' if n['modifiers'] else ''
    return {'source': 'docs/greece_1970_design/EFFECTS_REVIEW.json', 'revised_focuses': len(changes), 'changes': changes}


LABELS = {
    'industrial_capacity_factory': 'Factory output', 'industrial_capacity_dockyard': 'Dockyard output',
    'productivity_growth_modifier': 'Productivity growth', 'state_productivity_growth_modifier': 'Local productivity growth',
    'state_production_speed_buildings_factor': 'Local construction speed',
    'production_speed_buildings_factor': 'Construction speed', 'production_speed_industrial_complex_factor': 'Civilian factory construction speed',
    'production_factory_efficiency_gain_factor': 'Production efficiency growth', 'production_factory_max_efficiency_factor': 'Production efficiency cap',
    'tax_gain_multiplier_modifier': 'Tax revenue', 'corporate_tax_income_multiplier_modifier': 'Corporate tax revenue',
    'office_park_income_tax_modifier': 'Office income tax revenue', 'bureaucracy_cost_multiplier_modifier': 'Bureaucracy cost',
    'education_cost_multiplier_modifier': 'Education cost', 'social_cost_multiplier_modifier': 'Social spending cost',
    'police_cost_multiplier_modifier': 'Police cost', 'projects_cost_modifier': 'Economic project cost',
    'interest_rate_multiplier_modifier': 'Interest rate', 'supply_consumption_factor': 'Supply consumption',
    'army_defence_factor': 'Army defence', 'army_org_factor': 'Army organisation', 'max_planning': 'Maximum planning',
    'experience_gain_army_factor': 'Army experience gain', 'naval_morale_factor': 'Naval organisation recovery',
    'navy_max_range_factor': 'Naval range', 'naval_coordination': 'Naval coordination',
    'air_accidents_factor': 'Air accident chance', 'air_mission_efficiency': 'Air mission efficiency',
    'research_speed_factor': 'Research speed', 'political_power_factor': 'Political power gain',
    'political_power_gain': 'Daily political power', 'stability_factor': 'Stability',
    'foreign_influence_defense_modifier': 'Foreign influence resistance',
}


def reward_summary(n):
    lines = []
    for k, v in n['modifiers'].items():
        value = f'{v:+.3g}/day' if k == 'political_power_gain' else f'{100*v:+.3g}%'
        lines.append(LABELS.get(k, k) + ': ' + value)
    for k, v in n.get('state_programme', {}).get('modifiers', {}).items():
        lines.append(LABELS.get(k, k) + f': {100*v:+.3g}% in eligible rural states')
    for b in n.get('research_bonuses', []):
        lines.append(f"One {b['bonus']:.0%} research bonus: " + b['category'].removeprefix('CAT_').replace('_', ' '))
    if n.get('corruption_reduction'): lines.append('Reduce corruption by one level, if above the minimum')
    if n.get('duration_days') and n['modifiers']: lines.append(f"Programme duration: {n['duration_days']} days")
    return '\n'.join(lines)
