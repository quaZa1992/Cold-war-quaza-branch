# IMPERIA COLD WAR — Native tests of bilateral consent, suspension and cancellation.
from bilateral import PARTNERS, term_id

EMBARGO_EVENTS = ''


def build(check, payload):
    global EMBARGO_EVENTS
    EMBARGO_EVENTS = ''
    filename = 'COLDWAR_CUB_1970_bilateral.txt'
    code = 'complete_national_focus = COLDWAR_CUB_island_diplomacy\ncomplete_national_focus = COLDWAR_CUB_moscow_guarantee\n'
    for partner, spec in PARTNERS.items():
        tag = spec['tag']
        for term, data in spec['terms'].items():
            tid = term_id(partner, term)
            other = next(t for t in spec['terms'] if t != term)
            actual = payload(f'COLDWAR_CUB_accept_bilat_{partner}_{term}', tag, filename)
            wrong = payload(f'COLDWAR_CUB_accept_bilat_{partner}_{other}', tag, filename)
            cancel = payload(f'COLDWAR_CUB_cancel_bilat_{partner}_{term}_as_partner', tag, filename)
            code += f'set_variable = {{ COLDWAR_CUB_probe_cash = treasury }}\n{tag} = {{ set_variable = {{ COLDWAR_CUB_probe_cash = treasury }} }}\n'
            code += f'COLDWAR_CUB_offer_{partner}_{term} = yes\n{tag} = {{ {wrong} }}\n'
            code += check(f'{partner}_{term}_wrong_terms_blocked',
                          f'NOT = {{ has_country_flag = COLDWAR_CUB_bilat_{partner}_package_signed }} check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} {tag} = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}')
            code += f'subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {data["cost_cub"]} }}\n{tag} = {{ subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {data["cost_partner"]} }} {actual} }}\n'
            paired = f'has_country_flag = {tid}_signed has_idea = {tid}_cub {tag} = {{ has_country_flag = {tid}_signed has_idea = {tid}_{partner} }}'
            balances = f'check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} {tag} = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}'
            code += check(f'{partner}_{term}_signed_and_paid', paired+' '+balances)
            code += f'{tag} = {{ {actual} }}\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
            code += check(f'{partner}_{term}_no_replay', paired+' '+balances)
            code += f'{tag} = {{ {cancel} }}\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
            absent = f'NOT = {{ has_country_flag = {tid}_signed }} NOT = {{ has_idea = {tid}_cub }} {tag} = {{ NOT = {{ has_country_flag = {tid}_signed }} NOT = {{ has_idea = {tid}_{partner} }} }}'
            code += check(f'{partner}_{term}_partner_can_cancel', absent+' '+balances)
            code += f'COLDWAR_CUB_offer_{partner}_{term} = yes\n{tag} = {{ {actual} }}\n'
            code += check(f'{partner}_{term}_reentry_needs_consent_no_second_fee', paired+' '+balances)
            code += f'COLDWAR_CUB_cancel_{partner}_{term} = yes\n'

    # A representative signed agreement must react to each stored direction of
    # every sanction class, including one-sided/mirrored legacy array storage.
    code += 'COLDWAR_CUB_offer_mex_energy = yes\nMEX = { '+payload('COLDWAR_CUB_accept_bilat_mex_energy', 'MEX', filename)+' }\n'
    paired = 'has_country_flag = COLDWAR_CUB_bilat_mex_energy_signed has_idea = COLDWAR_CUB_bilat_mex_energy_cub MEX = { has_country_flag = COLDWAR_CUB_bilat_mex_energy_signed has_idea = COLDWAR_CUB_bilat_mex_energy_mex }'
    absent = 'has_country_flag = COLDWAR_CUB_bilat_mex_energy_signed NOT = { has_idea = COLDWAR_CUB_bilat_mex_energy_cub } MEX = { has_country_flag = COLDWAR_CUB_bilat_mex_energy_signed NOT = { has_idea = COLDWAR_CUB_bilat_mex_energy_mex } }'
    for owner, target in [('CUB', 'MEX'), ('MEX', 'CUB')]:
        for kind in ('dip', 'fin', 'eco', 'mil'):
            for direction in ('on_us', 'by_us'):
                array = f'imp_{kind}_sanc_{direction}'
                code += f'{owner} = {{ add_to_array = {{ array = {array} value = {target} }} }}\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
                code += 'clr_country_flag = COLDWAR_CUB_probe_suspended\nif = { limit = { '+absent+' } set_country_flag = COLDWAR_CUB_probe_suspended }\n'
                code += f'{owner} = {{ remove_from_array = {{ array = {array} value = {target} }} }}\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
                code += check(f'sanction_{owner}_{kind}_{direction}_suspends_and_restores', 'has_country_flag = COLDWAR_CUB_probe_suspended '+paired)
    for index, (owner, target) in enumerate([('CUB', 'MEX'), ('MEX', 'CUB')]):
        # Native break_embargo requires the sender's event ROOT. An inline
        # on_startup wrapper has no such ROOT, unlike an actual country event.
        event_id = f'COLDWAR_CUB_ENGINE.{100+index}'
        probe = f'send_embargo = {target}\nCUB = {{ COLDWAR_CUB_reconcile_bilateral = yes clr_country_flag = COLDWAR_CUB_probe_suspended if = {{ limit = {{ {absent} {owner} = {{ is_embargoing = {target} }} }} set_country_flag = COLDWAR_CUB_probe_suspended }} }}\n'
        probe += f'break_embargo = {target}\nCUB = {{ COLDWAR_CUB_reconcile_bilateral = yes '+check(f'embargo_{owner}_suspends_and_restores', 'has_country_flag = COLDWAR_CUB_probe_suspended '+paired+f' {owner} = {{ NOT = {{ is_embargoing = {target} }} }}')+' }\n'
        name = f'embargo_{owner}_suspends_and_restores'
        EMBARGO_EVENTS += f'country_event = {{ id = {event_id} hidden = yes is_triggered_only = yes immediate = {{ if = {{ limit = {{ has_dlc = "By Blood Alone" }} {probe} }} else = {{ log = "COLDWAR_CUB_ENGINE SKIP {name} requires_By_Blood_Alone" }} }} }}\n'
        code += f'{owner} = {{ country_event = {{ id = {event_id} }} }}\n'
    code += 'declare_war_on = { target = MEX type = annex_everything }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('war_suspends_both_but_keeps_signature', absent+' has_war_with = MEX')
    code += 'white_peace = { tag = MEX }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('peace_restores_both_without_new_signature', paired+' NOT = { has_war_with = MEX }')

    # Generic medical recipients exercise PREV nesting through CUB's reconciler,
    # rather than relying on the outer startup ROOT being the recipient.
    code += 'ALG = { if = { limit = { NOT = { COLDWAR_CUB_valid_health_budget = yes } } add_ideas = health_01 } set_country_flag = COLDWAR_CUB_medical_offer_pending }\nset_country_flag = COLDWAR_CUB_medical_offer_open\n'
    code += 'ALG = { '+payload('COLDWAR_CUB_accept_medical', 'ALG')+' }\n'
    medical_paired = 'has_idea = COLDWAR_CUB_medical_mission_cub ALG = { has_country_flag = COLDWAR_CUB_medical_mission_signed has_idea = COLDWAR_CUB_medical_mission_partner }'
    code += check('medical_is_permanent_and_reciprocal', medical_paired)
    code += 'add_to_array = { array = imp_mil_sanc_by_us value = ALG }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('medical_checks_cuban_sanctions_against_recipient', 'NOT = { has_idea = COLDWAR_CUB_medical_mission_cub } ALG = { NOT = { has_idea = COLDWAR_CUB_medical_mission_partner } has_country_flag = COLDWAR_CUB_medical_mission_signed }')
    code += 'remove_from_array = { array = imp_mil_sanc_by_us value = ALG }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('medical_resumes_after_sanctions', medical_paired)
    code += 'ALG = { '+payload('COLDWAR_CUB_cancel_medical_treaty_as_partner', 'ALG', filename)+' }\nCOLDWAR_CUB_reconcile_bilateral = yes\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('medical_cancellation_does_not_resurrect_legacy', 'NOT = { has_idea = COLDWAR_CUB_medical_mission_cub } ALG = { NOT = { has_country_flag = COLDWAR_CUB_medical_mission_signed } NOT = { has_idea = COLDWAR_CUB_medical_mission_partner } }')

    code += 'set_country_flag = COLDWAR_CUB_history_interests_offer_open\nUSA = { set_country_flag = COLDWAR_CUB_history_interests_offer_pending COLDWAR_CUB_history_accept_interests_sections = yes }\n'
    code += check('interests_sections_signed_but_suspended_by_remaining_sanctions', 'has_country_flag = COLDWAR_CUB_history_interests_sections_active NOT = { has_idea = COLDWAR_CUB_interests_sections_cub } USA = { has_country_flag = COLDWAR_CUB_history_interests_sections_active NOT = { has_idea = COLDWAR_CUB_interests_sections_usa } }')
    # The real trade settlement deliberately leaves diplomatic/military terms
    # unresolved. Explicit fixture lifting tests restoration without re-signing.
    for kind in ('dip', 'mil'):
        for direction in ('on_us', 'by_us'):
            array = f'imp_{kind}_sanc_{direction}'
            code += f'if = {{ limit = {{ is_in_array = {{ array = {array} value = USA }} }} remove_from_array = {{ array = {array} value = USA }} }}\nUSA = {{ if = {{ limit = {{ is_in_array = {{ array = {array} value = CUB }} }} remove_from_array = {{ array = {array} value = CUB }} }} }}\n'
    code += 'COLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('interests_sections_permanent_on_both_sides', 'has_idea = COLDWAR_CUB_interests_sections_cub USA = { has_idea = COLDWAR_CUB_interests_sections_usa }')
    code += 'COLDWAR_CUB_cancel_interests_sections = yes\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('interests_sections_can_be_cancelled', 'NOT = { has_idea = COLDWAR_CUB_interests_sections_cub } USA = { NOT = { has_idea = COLDWAR_CUB_interests_sections_usa } }')

    # Cancellation remains reachable while a signed legacy treaty is suspended.
    code += 'add_to_array = { array = imp_eco_sanc_by_us value = SOV }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('legacy_soviet_treaty_suspends_without_losing_signature', 'has_country_flag = COLDWAR_CUB_soviet_assistance_signed NOT = { has_idea = COLDWAR_CUB_soviet_assistance } SOV = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed NOT = { has_idea = COLDWAR_CUB_soviet_assistance_sov } }')
    code += 'SOV = { '+payload('COLDWAR_CUB_end_soviet_assistance_as_recipient', 'SOV')+' }\nremove_from_array = { array = imp_eco_sanc_by_us value = SOV }\nCOLDWAR_CUB_reconcile_bilateral = yes\n'
    code += check('legacy_soviet_counterparty_can_cancel_suspended_treaty', 'NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } NOT = { has_idea = COLDWAR_CUB_soviet_assistance } SOV = { NOT = { has_country_flag = COLDWAR_CUB_soviet_assistance_signed } NOT = { has_idea = COLDWAR_CUB_soviet_assistance_sov } }')
    return code
