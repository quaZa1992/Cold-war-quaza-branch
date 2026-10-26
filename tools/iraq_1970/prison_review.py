# IMPERIA CW — Cold War: iraq 1970 — prison review.
"""Finite prisoner cases and a recipient-owned review invoice.

The native decision charges30PP. Its pending receipt is the only authority for
a refund, so reopening/closing an old event cannot generate political power.
"""
from common import P, block, parse, emit, first, invoice, pay_var, check, locline

PENDING = P + 'prison_review_pending'
ELIGIBLE = P + 'prison_review_has_case'
AUTHORITY = ('COLDWAR_IRQ_campaign_active = yes\n'
             'has_country_flag = COLDWAR_IRQ_decision_prison_review_unlocked\n'
             'has_country_flag = COLDWAR_IRQ_review_detentions_implemented')
CASES = [
    ('1971.1.1', 'dukhayl_dead', 'dawa_cadres_protected'),
    ('1973.1.1', 'dukhayl_dead', 'dukhayl_released'),
    ('1971.11.28', 'rikabi_dead', 'rikabi_rehabilitated'),
]


def case_gate(deadline, dead, settled):
    return (f'date < {deadline}\nNOT = {{ has_country_flag = {P+dead} }}\n'
            f'NOT = {{ has_country_flag = {P+settled} }}')


def apply(outputs):
    """Replace this one provider's generated blocks, preserving stable IDs."""
    result = dict(outputs)
    trigger = block(ELIGIBLE, block('OR', '\n'.join(
        block('AND', case_gate(*case)) for case in CASES)))
    result['common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt'] += '\n' + trigger
    clear = ('clr_country_flag = ' + PENDING + '\n'
             'clr_country_flag = COLDWAR_IRQ_D_prison_review_quoted\n'
             'clear_variable = COLDWAR_IRQ_D_prison_review_invoice')
    refund = block(P+'cancel_prison_review', block('if',
        block('limit', 'has_country_flag = '+PENDING) +
        'add_political_power = 30\n' + clear))
    valid = AUTHORITY + '\n' + ELIGIBLE + ' = yes'
    session = 'has_country_flag = '+PENDING+'\n'+valid
    cancel = P+'cancel_prison_review = yes'
    do = block(P+'do_prison_review', block('if',
        block('limit','has_country_flag = '+PENDING) +
        block('if', block('limit',valid) + 'country_event = { id = COLDWAR_IRQ_decision_events.139 }') +
        block('else', cancel)))

    effects_path='common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt'
    effects=parse(result[effects_path])
    effects=[parse(do)[0] if k==P+'do_prison_review' else (k,o,v) for k,o,v in effects]
    result[effects_path]=emit(effects)+'\n'+refund

    decision_path='common/decisions/COLDWAR_IRQ_1970_decisions.txt'
    ast=parse(result[decision_path]);category=first(ast,P+'1970_decisions')
    decision=first(category,P+'decision_prison_review')
    for i,(k,o,v) in enumerate(decision):
        if k=='visible':decision[i]=(k,o,v+parse(ELIGIBLE+' = yes'))
        elif k=='available':decision[i]=(k,o,v+parse(
            block('custom_trigger_tooltip','tooltip = COLDWAR_IRQ_prison_review_case_tt\n'+ELIGIBLE+' = yes')+
            block('custom_trigger_tooltip','tooltip = COLDWAR_IRQ_prison_review_pending_tt\nNOT = { has_country_flag = '+PENDING+' }')))
        elif k=='complete_effect':decision[i]=(k,o,parse(
            'clr_country_flag = COLDWAR_IRQ_D_prison_review_quoted\n'
            'clear_variable = COLDWAR_IRQ_D_prison_review_invoice\n'
            'set_country_flag = '+PENDING+'\n'+P+'do_prison_review = yes'))
    result[decision_path]=emit(ast)+'\n'

    quoted = invoice(P+'D_prison_review',.005)
    immediate=block('if',block('limit',session)+quoted)+block('else',cancel)
    cashgate=('has_country_flag = COLDWAR_IRQ_D_prison_review_quoted\n'
              'check_variable = { COLDWAR_IRQ_D_prison_review_invoice > 0 }\n'+
              check('treasury',P+'D_prison_review_invoice')+'\n'
              'check_variable = { gdp_total > 0 }\n'
              'NOT = { has_country_flag = MD_skip_treasury_cost }')
    releases='\n'.join(block('if',block('limit',case_gate(*case))+
        'set_country_flag = '+P+case[2]+
        ('\nclr_country_flag = COLDWAR_IRQ_dukhayl_unavailable' if case[2]=='dukhayl_released' else '')) for case in CASES)
    acceptance=block('if',block('limit',session+'\n'+cashgate)+
        pay_var(P+'D_prison_review_invoice')+'\n'+releases+
        '\nadd_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 90 }\n'+clear)+block('else',cancel)
    retention=block('if',block('limit',session)+
        'add_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 60 }\n'+clear)+block('else',cancel)
    close=block('if',block('limit',block('NOT',valid))+cancel)+block('else',clear)
    event=block('country_event',
        'id = COLDWAR_IRQ_decision_events.139\ntitle = COLDWAR_IRQ_decision_events.139.t\n'
        'desc = COLDWAR_IRQ_decision_events.139.d\nis_triggered_only = yes\n'
        'trigger = { always = yes }\n'+block('immediate',immediate)+
        block('option','name = COLDWAR_IRQ_option_152\nai_chance = { factor = 50 }\n'+block('trigger',session)+acceptance)+
        block('option','name = COLDWAR_IRQ_option_153\nai_chance = { factor = 50 }\n'+block('trigger',session)+retention)+
        block('option','name = COLDWAR_IRQ_option_154\nai_chance = { factor = 50 }\n'+close))
    path='events/COLDWAR_IRQ_1970_decisions.txt';ast=parse(result[path])
    ast=[parse(event)[0] if k=='country_event' and first(v,'id')=='COLDWAR_IRQ_decision_events.139' else (k,o,v) for k,o,v in ast]
    result[path]=emit(ast)+'\n'
    path='localisation/english/COLDWAR_IRQ_1970_decisions_l_english.yml'
    import re
    loc = {
        'COLDWAR_IRQ_decision_prison_review_desc': 'Review living, unresolved detainees. Protect Dawa organisers before January 1971, rehabilitate Rikabi before 28 November 1971, or release Dukhayl before January 1973. If no eligible case remains, the 30 Political Power review fee is refunded.',
        'COLDWAR_IRQ_decision_events.139.d': 'The review concerns living detainees whose cases remain unresolved. Release requires the stated funding. If no eligible case remains, the review fee is refunded and no implementation costs are charged.',
        'COLDWAR_IRQ_prison_review_case_tt': 'At least one living detainee can still benefit from review before their case deadline.',
        'COLDWAR_IRQ_prison_review_pending_tt': 'No prisoner review is awaiting our response.',
    }
    text=result[path]
    for key,value in loc.items():
        pattern=r'(?m)^ '+re.escape(key)+r':0 ".*"$'
        line=locline(key,value)
        if re.search(pattern,text):text=re.sub(pattern,lambda _:line,text)
        else:text+='\n'+line+'\n'
    result[path]=text
    return result
