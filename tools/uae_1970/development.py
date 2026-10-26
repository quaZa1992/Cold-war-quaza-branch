# IMPERIA CW — Cold War: uae 1970 — development.
"""User-authorized costly industrialisation and strong population development.

Values are roleplay balance in native MD billions/resource units, not historical
construction invoices or a claim that the coast contained domestic metal ores.
"""
from copy import deepcopy
import re
from maritime import OIL_PHASES

P = 'COLDWAR_UAE_'
POPULATION_GROWTH_CAP = 2.0


def apply_revision(data):
    by = {n['id'].removeprefix(P): n for n in data['nodes']}
    data['modifier_labels']['monthly_population'] = ['Monthly Population Growth', 'percent']
    data['modifier_labels']['agricolture_productivity_modifier'] = ['Agriculture Productivity', 'percent']
    data['modifier_labels']['social_cost_multiplier_modifier'] = ['Social Spending Multiplier', 'percent']
    data['starting_spirits'].append({
        'id': P+'maritime_livelihoods', 'label': 'Pearls, Fishing and Dhows',
        'description': "Fishing, dhow crews and maritime merchants still support coastal households, easing their reliance on public assistance. Pearling helped build these settlements and their trading connections, but its long decline has left debts and uncertain livelihoods. Better harbours can improve these trades, while the expansion of oil draws workers and commerce away from the traditional coastal economy.",
        'modifiers': {'agricolture_productivity_modifier': .10, 'offices_productivity': .03, 'social_cost_multiplier_modifier': -.05, 'country_productivity_growth_modifier': -.05},
        'treatment': 'Fishing harbours remove the inherited growth penalty. Each completed oil-capacity phase reduces the original maritime productivity and social-cost relief by20%, retaining at least20%.',
    })
    maritime = by['trading_coast']
    maritime.update(title='Pearls and Fishing', narrative_title='Pearls and Fishing', treasury_cost_billion=.10,
        available='always = yes',
        description="Long before oil exports, pearl divers, fishermen, boatbuilders and merchants earned their living along the coast. The great pearling seasons have faded, but fishing boats and dhow trading networks still sustain families. Better boats, handling and local markets can provide steadier livelihoods and reduce reliance on public assistance, even as the oil industry competes for crews and capital.")
    maritime['modifiers']['agricolture_productivity_modifier'] = .10
    maritime['modifiers']['social_cost_multiplier_modifier'] = -.02
    maritime['reward_summary'] = ['Treasury: -$0.10 billion.', 'Before oil expansion: primary-sector productivity +10%, office-sector productivity +6%, social spending multiplier -2%; maritime contributions retain20% after all four oil phases.']
    harbour = by['port_planning']
    harbour.update(title='Fishing Harbours', narrative_title='Fishing Harbours', treasury_cost_billion=.15,
        available='always = yes',
        description="Reliable landing grounds, ice stores and fish markets can reduce spoilage and give crews a steadier return for their catch. A more secure household income eases demand for assistance. The works will also serve coastal traders, although administration and refrigeration bring continuing costs and oil development draws activity towards new industries.")
    harbour['modifiers'].update(agricolture_productivity_modifier=.10, energy_use_multiplier=.02, social_cost_multiplier_modifier=-.03)
    harbour['spirit_changes'].append({
        'spirit': P+'maritime_livelihoods', 'component': 'country_productivity_growth_modifier',
        'operation': 'set', 'value': 0, 'floor': 0, 'owner_focus': harbour['id'],
        'family': 'maritime_modernisation',
        'evaluation': 'strongest_in_family_then_sum_credits_from_original_component_clamp_at_zero',
    })
    harbour['reward_summary'] = ['Treasury: -$0.15 billion.', 'Before oil expansion: primary-sector productivity +10%, social spending multiplier -3%; energy use +2%.', 'Remove the inherited maritime productivity-growth penalty; retained coastal contributions fall with oil expansion.']
    # Focus completion and full funding commission the first factory. This
    # avoids making a zero-CIC country queue a factory it cannot construct.
    port = by['industrial_port']
    port['treasury_cost_billion'] = 7.5
    port['days'], port['cost'] = 105, 15.0
    port['available'] = 'always = yes'
    port['description'] = (
        "Dubai's ports can support more than the movement of imported goods. Serviced industrial land, workshops and reliable utilities "
        "will give manufacturers a foothold beside the harbour, at the cost of a major capital commitment and greater demand for power and labour."
    )
    port['reward_summary'] = ['Treasury: -$7.50 billion.', 'Complete one civilian factory and add one shared building slot in Dubai.']
    port['effect_body'] = '179 = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }'
    aviation = by['aviation_hub']
    aviation.update(treasury_cost_billion=2.5, days=105, cost=15.0, available='always = yes',
        description="Dubai's commercial air links need a larger airport, reliable ground services and connections to the port economy. A new runway and supporting facilities can bring passengers and high-value cargo to the coast, but their construction and operation require substantial funding and electricity.",
        reward_summary=['Treasury: -$2.50 billion.', 'Complete one airport/airbase level in Dubai.'],
        effect_body='179 = { add_building_construction = { type = air_base level = 1 instant_build = yes } }')

    # A completed industrial base is a genuine extra condition, not a hidden
    # duplicate of a graph predecessor. The compiler supplies its numeric label.
    industrial_base = ('179 = { is_owned_by = ROOT is_controlled_by = ROOT '
        'custom_trigger_tooltip = { tooltip = COLDWAR_UAE_completed_industry_tt '
        'check_variable = { building_level@industrial_complex > 0 } } }')
    specs = [
        ('jebel_ali_smelter', 'The Jebel Ali Smelter', [33, 16], 4.5, 179, 'aluminium', 12, .12, 'focus_generic_aluminum',
         "Oil and gas revenues can finance an aluminium industry at Jebel Ali, turning imported alumina into metal for export. "
         "The smelter needs dependable electricity, cooling water, specialised equipment and trained crews. "
         "Its success would create a new industrial export, while tying a substantial part of the coast's power supply to continuous operation."),
        ('steel_rolling_mills', 'Steel Rolling Mills', [37, 16], 3.0, 180, 'steel', 5, .06, 'focus_generic_steel_mill',
         "Construction across the emirates consumes steel brought through their ports. A state-backed rolling industry in Abu Dhabi "
         "can process imported billets and scrap into a domestic supply of finished steel. This accelerated industrial programme "
         "requires machinery, power and long-term working capital before it can compete with established foreign suppliers."),
    ]
    for key, title, xy, price, state, resource, amount, energy, icon, description in specs:
        node = deepcopy(port)
        node.update(id=P+key, title=title, narrative_title=title, xy=xy,
                    days=105, cost=15.0, treasury_cost_billion=price,
                    prerequisites=[[P+'beyond_oil']], mutually_exclusive=[],
                    icon=icon, description=description,
                    available=industrial_base+f'\n{state} = {{ is_owned_by = ROOT is_controlled_by = ROOT }}',
                    modifiers={'energy_use_multiplier': energy},
                    active_condition=f'{state} = {{ is_owned_by = ROOT is_controlled_by = ROOT }}',
                    resource_changes=[{'state': state, 'resource': resource, 'base_amount': amount}],
                    one_time_delivery_flag=P+key+'_paid',
                    reward_summary=[f'Treasury: -${price:.2f} billion.', f'+{amount} base {resource} in state {state}.', f'Energy use: +{energy*100:g}%.'],
                    historical_status=('DUBAL production began in1979; player-controlled construction timing and values are proposed balance.'
                                       if resource == 'aluminium' else 'Accelerated alternative industrialisation; not a claim of a historical1970 steel industry.'),
                    effect_body=f'{state} = {{ add_resource = {{ type = {resource} amount = {amount} }} }}\ningame_update_setup = yes',
                    requirement_contracts=[{'meaning': 'Completed industrial base and recipient ownership/control rechecked before one-time payment and commissioning; no Treasury prerequisite.',
                                            'proposed_code': industrial_base}])
        data['nodes'].append(node)

    changes = {
        'schools_clinics': (.15, 35, {'monthly_population': .40, 'health_cost_multiplier_modifier': .15}),
        'water_network': (.50, 70, {'monthly_population': .30, 'energy_use_multiplier': .10}),
        'citizen_housing': (.75, 70, {'monthly_population': .50, 'social_cost_multiplier_modifier': .12}),
        'worker_towns': (.60, 70, {'monthly_population': .90, 'health_cost_multiplier_modifier': .15, 'social_cost_multiplier_modifier': .08}),
        'efficient_services': (.25, 49, {'monthly_population': .40, 'health_cost_multiplier_modifier': .05}),
    }
    descriptions = {
        'schools_clinics': "Many settlements still rely on a small number of teachers, medical staff and visiting services. District clinics, maternity care and new classrooms can help children survive and families remain in the towns. Keeping those services staffed will require a lasting commitment to health and education budgets.",
        'water_network': "Growing settlements cannot depend indefinitely on wells and irregular deliveries. Desalination, distribution pipes and sanitation can make larger towns viable and reduce disease, but the pumps and treatment works will consume power even when oil revenues fall.",
        'citizen_housing': "Serviced neighbourhoods give citizen families room to grow without abandoning their ties to the emirates. Housing, schools and local facilities can strengthen the founding social bargain, while creating permanent obligations for the public budget.",
        'worker_towns': "The ports, building sites and industries depend on workers arriving from abroad. Permanent housing, clean water and clinics can turn crowded work camps into viable communities and sustain a much larger resident population. The emirates must fund the resulting health services and social infrastructure.",
        'efficient_services': "A growing population needs reliable district health services, trained staff and an administration able to maintain them. Professional management can keep those institutions effective as the towns expand, although continuing care will remain a permanent public expense.",
    }
    for key, (price, days, modifiers) in changes.items():
        node = by[key]
        node.update(treasury_cost_billion=price, days=days, cost=days/7,
                    available='always = yes', description=descriptions[key])
        node['modifiers'].update(modifiers)
        node['reward_summary'] = [f'Treasury: -${price:.2f} billion.', f'Monthly population growth modifier: +{modifiers["monthly_population"]*100:g}%.']
    for key in OIL_PHASES:
        by[key]['description'] += (
            ' Expanding oil operations draws labour and commerce towards the new industry, '
            'reducing the traditional coastal trades\' contribution to household income.'
        )
        by[key]['reward_summary'].append('Reduce original maritime productivity and social-cost relief by20%; retain at least20%.')
    # Focus costs may take the treasury below zero through native MD. Do not
    # leave either an advertised requirement or an obsolete catalogue veto.
    treasury_check = re.compile(r'check_variable\s*=\s*\{[^{}]*\btreasury\b[^{}]*\}')
    for node in data['nodes']:
        for field in ('available', 'effect_body'):
            node[field] = treasury_check.sub('', node[field]).strip()
        for contract in node.get('requirement_contracts', []):
            contract['proposed_code'] = treasury_check.sub('', contract['proposed_code']).strip()
    return data
