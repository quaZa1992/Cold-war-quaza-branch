# IMPERIA COLD WAR — France investment assets instead of repeated productivity rewards.
"""Apply the user's preference for funded civilian factories and offices."""
from copy import deepcopy
from decimal import Decimal

PRODUCTIVITY_KEYS = {'country_productivity_growth_modifier', 'civilian_factories_productivity',
                     'offices_productivity', 'production_factory_efficiency_gain_factor'}

# Focus: (own-GDP setup percent, concrete investment sites, revised narrative).
REWARDS = {
    'radical_enterprise': (.50, [(60, 'industrial_complex'), (56, 'offices')],
        'Support private industrial investment in Aquitaine and technical services in the Paris region. Enterprise gains room to expand, while public credit and tax concessions put part of the risk on the state.'),
    'national_champions': (.40, [(55, 'offices')],
        'Support a productive site in Rhone-Alpes and engineering offices in Normandie. Large industrial groups can undertake national projects, but expect public support and favourable tax treatment.'),
    'participation': (.35, [(58, 'industrial_complex')],
        'Give workers a stake in industrial expansion through participation agreements and a funded production site. Employers must share returns, while technical workshops require their own investment.'),
    'management': (.25, [(56, 'offices')],
        'Give professional managers greater freedom and support a Paris-region business and technical office. Firms retain more of the gains, while organised labour loses influence over investment decisions.'),
    'social_contract_ps': (.30, [(58, 'offices')],
        'Back collective bargaining with a regional labour-services office and stronger guarantees for organised workers. Employers face new obligations and the social budget carries continuing commitments.'),
    'competitiveness_ps': (.55, [(54, 'industrial_complex'), (57, 'offices')],
        'Combine industrial renewal in Hauts-de-France with technical and commercial services in Alsace-Lorraine. Investment provides practical capacity, while maintaining the necessary skills requires higher education spending.'),
    'public_banks': (.50, [(54, 'offices')],
        'Use public banks to expand credit offices in Paris and Hauts-de-France. Regional investment gains an institutional base, while public administration must supervise the lending commitments.'),
    'left_radicals': (.25, [(60, 'offices')],
        'Bring cooperative credit and local public services into the republican programme through an Aquitaine office. Labour gains a stronger voice, alongside continuing social commitments.'),
    'civilian_republic': (.45, [(58, 'offices'), (64, 'offices')],
        'Expand civilian services in Bourgogne and Bretagne. Public investment supports a social republic, while the military sector receives a smaller share of economic and political attention.'),
    'cid_cooperatives': (.35, [(64, 'offices')],
        'Extend shopkeepers and small firms a local credit network in Aquitaine and Bretagne. More offices improve access to finance, while supervision and guarantees enlarge the administrative bill.'),
    'champion_model': (.60, [(54, 'industrial_complex')],
        'Concentrate industrial investment in major productive groups, with factories in Normandie and Hauts-de-France. Coordinated projects can achieve scale, but require continuing public administration.'),
    'regional_industry': (.60, [(63, 'offices')],
        'Pair industrial renewal in Hauts-de-France with port and commercial facilities in Provence. Regional development spreads investment, while local services add continuing social costs.'),
    'conversion': (.45, [(54, 'industrial_complex')],
        'Renew an industrial basin in Hauts-de-France with a funded civilian plant and technical retraining. The transition protects employment at the cost of continued social support.'),
    'progress': (.25, [(56, 'offices')],
        'Give the New Society programme a practical administrative and service base in the Paris region. Social consultation needs institutions and staff, and enlarges the cost of government.'),
    'self_management': (.50, [(58, 'offices')],
        'Build a worker-managed production site and an associated service office in Bourgogne. Enterprise autonomy requires institutions capable of coordinating investment and public oversight.'),
    'workers_control': (.25, [(62, 'offices')],
        'Support worker representation with a technical and bargaining office in Rhone-Alpes. Workplace participation strengthens organised labour, while employers and central government lose some freedom of action.'),
    'party_discipline': (.10, [],
        'Concentrate political authority and industrial study within the party apparatus. The leadership can act more decisively, but political discipline deepens opposition outside its own organisations.'),
    'contract': (.30, [(57, 'offices')],
        'Anchor the social settlement in collective bargaining and an Alsace-Lorraine labour-services office. Cooperation improves industrial relations, while stronger guarantees enlarge continuing social expenditure.'),
    'statute': (.35, [(55, 'industrial_complex')],
        'Combine statutory labour rules with industrial investment in Normandie. Employers gain firmer operating conditions, while enforcement costs and union opposition remain real.'),
    'open_computers': (.30, [(56, 'offices')],
        'Adopt compatible computer systems and expand a Paris-region technical office. Licensing accelerates access to electronics expertise, while royalties and support payments reduce the returns retained by French firms.'),
}


def _fee(percent):
    fraction = -Decimal(str(percent)) / 100
    return {'kind':'treasury_gdp', 'percent':-percent, 'gdp_fraction':float(fraction),
            'runtime_share_literal':format(fraction,'.5f'), 'base':'gdp_total',
            'payer':'own_country', 'valuation':'at_payment', 'once':True}


def apply_asset_reward_revision(source):
    design = deepcopy(source)
    nodes = {n['key']: n for n in design['nodes']}
    records = []
    for key, (fee, sites, description) in REWARDS.items():
        node = nodes[key]
        assert not node.get('offer'), key
        removed = [e for e in node['effects'] if e.get('kind')=='modifier'
                   and e['key'] in PRODUCTIVITY_KEYS and e['value']>0]
        assert removed, key
        node['effects'] = [e for e in node['effects'] if e not in removed and e['kind']!='treasury_gdp']
        node['effects'].insert(0, _fee(fee))
        for state, kind in sites:
            match = next((e for e in node['effects'] if e['kind']=='building'
                          and e['state']==state and e['building']==kind and not e.get('province')),None)
            if match:
                match['amount'] += 1
                match['slots'] += 1
            else:
                node['effects'].append({'kind':'building','state':state,'building':kind,'amount':1,
                    'slots':1,'slots_before_construction':True,'once':True})
        node['description'] = description
        records.append({'focus':node['id'],'removed_modifiers':removed,
                        'setup_gdp_percent':fee,'added_assets':[{'state':s,'building':b,'levels':1,'slots':1} for s,b in sites]})
    design['asset_reward_revision'] = {'project':'IMPERIA COLD WAR',
        'id':'france_1970_investment_assets_20261029',
        'authorisation':'Productivity growth buffs sollen nicht so oft gegeben werden. Stattdessen Foki fuer mehr Civs oder Offices.',
        'scope':'Twenty domestic focuses. Signed bilateral packages, focus graph and IDs remain unchanged.',
        'completed_focus_policy':'Rebuild current programme modifiers. Never replay completed focus fees or finite awards.',
        'changes':records}
    return design
