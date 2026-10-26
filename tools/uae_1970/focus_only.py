# IMPERIA CW — Cold War: uae 1970 — focus only.
"""COLDWAR focus-led UAE policy; retain only repeatable oil/reserve decisions.

Domestic programme purposes are absorbed by the corresponding existing focus.
Their former temporary modifiers and invoices are not added a second time.
Foreign-consent actions are metadata for the compiler's recipient-owned hooks.
"""
from copy import deepcopy

P = 'COLDWAR_UAE_'
RETAINED_DECISIONS = frozenset({'oil_restraint', 'reserve_deposit', 'reserve_withdraw'})
FOCUS_ACTIONS = {
    'nine_states': ['bahrain', 'qatar'],
    'federal_council': ['association_law'],
    'constitutional_competition': ['convention'],
    'municipal_compact': ['residency'],
    'arab_solidarity': ['arab_exchange'],
    'public_industry': ['industry_project'],
    'labour_code': ['labour_inspection'],
    'technical_cadres': ['scholarships'],
    'charitable_network': ['charity_oversight'],
    'state_participation': ['participation'],
    'port_planning': ['port_project'],
    'aviation_hub': ['airline'],
    'industrial_port': ['industrial_power'],
    'citizen_housing': ['housing'],
    'worker_towns': ['housing_workers'],
    'technical_institutes': ['vocational'],
    'sustainable_force': ['training'],
    'air_coastal_shield': ['procurement'],
    'land_deterrent': ['maintenance'],
    'security_contracts': ['training_offer'],
    'technical_exchange': ['exchange_offer'],
    'enduring_protection': ['british_cofinance'],
    'kuwait_support': ['kuwait_support'],
    'kuwait_transit': ['kuwait_transit'],
    'kuwait_deployment': ['kuwait_deployment'],
}
KUWAIT_KEYS = ('kuwait_support', 'kuwait_transit', 'kuwait_deployment')
NEW_FOCUS_KEYS = (*KUWAIT_KEYS, 'constitutional_competition')


def apply_revision(data):
    """Overlay authored policy delivery without altering the approved snapshot."""
    by = {n['id'].removeprefix(P): n for n in data['nodes']}
    removed = {d['id'] for d in data['decisions']
               if d['id'].removeprefix(P+'decision_') not in RETAINED_DECISIONS}
    data['decisions'] = [d for d in data['decisions'] if d['id'] not in removed]
    for n in data['nodes']:
        for field in ('unlocks_decisions', 'decision_unlocks'):
            if field in n:
                n[field] = [x for x in n[field] if x not in removed]
        # The compiler derives actual unlock rows from the surviving catalogue.
        n['reward_summary'] = [line for line in n.get('reward_summary', [])
                               if not any(word in line.lower() for word in
                                   ('unlock', 'decision', 'respond to an invasion', 'crisis popup'))]
        key = n['id'].removeprefix(P)
        if key in FOCUS_ACTIONS:
            n['focus_actions'] = list(FOCUS_ACTIONS[key])

    council = by['federal_council']
    council['streamlined'] = True
    council['description'] = "A consultative federal council can give the emirates a forum for public affairs while the rulers retain their constitutional authority. Recognising educational and civic associations under federal law gives their activities an accountable framework. Consultations and supervision require trained officials and a continuing federal administration."
    council['focus_only_effect_body'] = P+'organise_association = yes'
    council['reward_summary'] += ['Recognise educational associations under federal law.']
    if P+'constitutional_competition' not in by:
        convention = deepcopy(council)
        convention.update(id=P+'constitutional_competition', title='Political Competition',
            narrative_title='Political Competition', xy=[9, 9], days=70, cost=10.0,
            prerequisites=[[P+'federal_council']], mutually_exclusive=[],
            treasury_cost_billion=0, modifiers={}, spirit_changes=[], conditional_contributions=[],
            requirement_contracts=[], effect_body='',
            focus_only_effect_body=P+'convene_constitution = yes',
            focus_actions=['convention'], streamlined=True,
            available='is_subject = no\nhas_country_flag = '+P+'federation_established\n'
                      'hidden_trigger = { has_country_flag = '+P+'federation_formed }',
            active_condition='always = yes',
            description="The consultative council has given public affairs a federal forum. A further constitutional reform can open legal political competition and regular elections. The electorate will determine the governing coalition, while the ruling houses must accept a more uncertain political settlement.",
            reward_summary=['Allow elections every four years and legal political competition through the native party system.'],
            historical_status='Optional alternative constitutional reform; the historical consultative council does not itself introduce elected party government.')
        data['nodes'].append(convention)
    for key, wording in {
        'majlis': ' Maintaining the rulers\' confidence and clear lines of responsibility can help the union withstand a local succession crisis.',
        'oil_shock_plan': ' Budget reserves and clear spending priorities can protect essential administration when oil prices fall.',
        'gulf_diplomacy': ' An invasion of Kuwait may require financial support, transit arrangements and preparations for a military contribution.',
    }.items():
        by[key]['streamlined'] = True
        if wording.strip() not in by[key]['description']:
            by[key]['description'] += wording

    base = by['gulf_diplomacy']
    texts = [
        ('Aid for Kuwait', 'An invasion of Kuwait threatens the security of the Gulf and places its government under exceptional financial pressure. We can offer a contribution to support Kuwait, subject to its government\'s agreement. This financial commitment is separate from decisions on military access and participation in the war.'),
        ('Offer Transit to Kuwait', 'Kuwait may need access to the federation\'s ports and transport links during an invasion. Our government can offer transit arrangements to support its defence, subject to Kuwaiti agreement and the responsibilities of hosting foreign forces.'),
        ('A Contingent for Kuwait', 'A military contribution to Kuwait\'s defence requires an explicit agreement over access, command and support. We can seek that agreement while retaining responsibility for our own troops and our decision to enter the war.'),
    ]
    existing = {n['id'] for n in data['nodes']}
    for index, (key, (title, description)) in enumerate(zip(KUWAIT_KEYS, texts)):
        if P+key in existing:
            continue
        n = deepcopy(base)
        n.update(id=P+key, title=title, narrative_title=title,
                 xy=[37+4*index, 19], days=70, cost=10.0,
                 prerequisites=[[P+'gulf_diplomacy']],
                 mutually_exclusive=[],
                 treasury_cost_billion=0, modifiers={}, spirit_changes=[],
                 conditional_contributions=[], requirement_contracts=[],
                 effect_body='', focus_only_effect_body='',
                 description=description, streamlined=True,
                 reward_summary=['Send the agreed national policy to the relevant government; access and cooperation require valid consent.'],
                 available='is_subject = no\nhas_country_flag = '+P+'federation_established\n'
                           'hidden_trigger = { has_country_flag = '+P+'federation_formed }\n'
                           'country_exists = KUW\nKUW = { has_war = yes }\nNOT = { has_war_with = KUW }',
                 active_condition='always = yes',
                 focus_actions=[key],
                 historical_status='Reactive Cold War policy; actual invasion required. No automatic war entry or military deployment.')
        data['nodes'].append(n)
    return data


def focus_leaves(key, preview=False):
    """Direct domestic law changes; foreign agreements have separate providers."""
    key = key.removeprefix(P)
    if key == 'constitutional_competition':
        return ('set_politics = { elections_allowed = yes election_frequency = 48 }'
                if preview else P+'convene_constitution = yes')
    if preview:
        return ''
    if key == 'federal_council':
        return P+'organise_association = yes'
    return ''
