# IMPERIA COLD WAR — Native execution cases for the approved foreign-policy revision.
"""Fixture-only political changes and independence never enter shipped gameplay."""
from cuba_runtime_design import MODEL

BY = {n['key']: n for n in MODEL['nodes']}
EMBARGO_EVENTS = ''
DELIVERY_EXPECTED = []
NAME_EXPECTED = []


def seed(key):
    return '\n'.join('set_country_flag = '+p[0]+'_applied' for p in BY[key]['prerequisites'])+'\n'


def fort_level(province, building, level):
    base=f'province = {{ id = {province} }} building = {building}'
    return (f'any_province_building_level = {{ {base} level > {level-1} }} '
            f'NOT = {{ any_province_building_level = {{ {base} level > {level} }} }}')


def build(check, payload, event_payload):
    global EMBARGO_EVENTS, DELIVERY_EXPECTED, NAME_EXPECTED
    EMBARGO_EVENTS = ''
    DELIVERY_EXPECTED = []
    NAME_EXPECTED = []
    code = 'log = "COLDWAR_CUB_ENGINE START"\nCOLDWAR_CUB_initialize = yes\n'
    code += check('authored_1970_tree', 'has_focus_tree = COLDWAR_CUB_1970_focus COLDWAR_CUB_is_1970 = yes emerging_communist_state_are_in_power = yes')
    code += check('starting_circumstances', 'has_idea = COLDWAR_CUB_american_embargo has_idea = COLDWAR_CUB_zafra_campaign has_country_flag = COLDWAR_CUB_initialized')
    code += '1252 = { set_state_category = state_inhospitable }\nCOLDWAR_CUB_repair_island_investment = yes\n'
    code += check('island_existing_save_investment_repair', 'owns_state = 1252 1252 = { has_state_category = state_00 is_core_of = CUB }')
    code += 'COLDWAR_CUB_apply_popular_power = yes\nset_variable = { COLDWAR_CUB_probe_cash = treasury }\nsubtract_from_variable = { COLDWAR_CUB_probe_cash = 0.20 }\nCOLDWAR_CUB_apply_family_code = yes\nCOLDWAR_CUB_apply_family_code = yes\n'
    code += check('family_code_paid_once', 'has_country_flag = COLDWAR_CUB_family_code_applied check_variable = { treasury = COLDWAR_CUB_probe_cash } check_variable = { COLDWAR_CUB_pcc_total_workforce_modifier = 0.02 }')
    code += 'set_variable = { ruling_party = 6 }\nCOLDWAR_CUB_sync_programmes = yes\n'
    code += check('party_departure_deactivates_programme', 'NOT = { has_dynamic_modifier = { modifier = COLDWAR_CUB_pcc_programme } } check_variable = { COLDWAR_CUB_pcc_total_workforce_modifier = 0 }')
    code += 'set_variable = { ruling_party = 4 }\nCOLDWAR_CUB_sync_programmes = yes\n'
    code += check('party_return_restores_without_payment', 'has_dynamic_modifier = { modifier = COLDWAR_CUB_pcc_programme } check_variable = { COLDWAR_CUB_pcc_total_workforce_modifier = 0.02 } check_variable = { treasury = COLDWAR_CUB_probe_cash }')
    code += 'set_variable = { COLDWAR_CUB_probe_cash = treasury }\nsubtract_from_variable = { COLDWAR_CUB_probe_cash = 0.75 }\n854 = { set_variable = { COLDWAR_CUB_probe_infra = building_level@infrastructure } add_to_variable = { COLDWAR_CUB_probe_infra = 1 } }\nCOLDWAR_CUB_apply_restore_sectors = yes\nCOLDWAR_CUB_apply_restore_sectors = yes\n'
    code += check('merged_rail_paid_once_and_built_once', 'has_country_flag = COLDWAR_CUB_restore_sectors_applied has_country_flag = COLDWAR_CUB_rail_lorries_applied check_variable = { treasury = COLDWAR_CUB_probe_cash } 854 = { check_variable = { building_level@infrastructure = COLDWAR_CUB_probe_infra } }')
    code += check('merged_rail_focus_and_component_receipts', 'has_country_flag = COLDWAR_CUB_restore_sectors_applied has_country_flag = COLDWAR_CUB_rail_lorries_applied')
    code += check('merged_rail_exact_treasury', 'check_variable = { treasury = COLDWAR_CUB_probe_cash }')
    code += check('merged_rail_exact_infrastructure', '854 = { check_variable = { building_level@infrastructure = COLDWAR_CUB_probe_infra } }')
    code += 'clr_country_flag = COLDWAR_CUB_restore_sectors_applied\nCOLDWAR_CUB_apply_restore_sectors = yes\n'
    code += check('old_rail_receipt_prevents_merged_replay', 'has_country_flag = COLDWAR_CUB_restore_sectors_applied check_variable = { treasury = COLDWAR_CUB_probe_cash } 854 = { check_variable = { building_level@infrastructure = COLDWAR_CUB_probe_infra } }')
    code += 'set_country_flag = COLDWAR_CUB_tricontinental_secretariat_applied\nCOLDWAR_CUB_sync_programmes = yes\nset_variable = { ruling_party = 5 }\nCOLDWAR_CUB_apply_diplomatic_solidarity = yes\n'
    expected = BY['diplomatic_solidarity']['modifiers']['foreign_influence_modifier']
    code += check('merged_old_political_modifiers_counted_once', f'check_variable = {{ COLDWAR_CUB_ospaaal_foreign_influence_modifier = {expected} }}')
    code += 'set_variable = { ruling_party = 4 }\nCOLDWAR_CUB_sync_programmes = yes\n'
    code += 'set_country_flag = COLDWAR_CUB_far_reorganisation_applied\nset_variable = { COLDWAR_CUB_probe_cash = treasury }\nsubtract_from_variable = { COLDWAR_CUB_probe_cash = 0.45 }\nCOLDWAR_CUB_apply_coastal_patrols = yes\nCOLDWAR_CUB_apply_coastal_patrols = yes\n'
    code += check('guantanamo_forts_native_levels_paid_once', 'has_country_flag = COLDWAR_CUB_coastal_patrols_applied check_variable = { treasury = COLDWAR_CUB_probe_cash } 855 = { '+fort_level(7590,'bunker',2)+fort_level(7590,'coastal_bunker',1)+' }')
    code += 'subtract_from_variable = { COLDWAR_CUB_probe_cash = 0.45 }\nCOLDWAR_CUB_apply_civil_military_pact = yes\nCOLDWAR_CUB_apply_civil_military_pact = yes\n'
    code += check('coastal_strongpoints_native_levels_paid_once', 'has_country_flag = COLDWAR_CUB_civil_military_pact_applied check_variable = { treasury = COLDWAR_CUB_probe_cash } 855 = { '+fort_level(7590,'coastal_bunker',2)+fort_level(9603,'bunker',1)+fort_level(9603,'coastal_bunker',1)+' }')
    code += check('forts_do_not_touch_us_base', 'USA = { owns_state = 424 controls_state = 424 } 424 = { NOT = { any_province_building_level = { province = { id = 13247 } building = bunker level > 0 } } NOT = { any_province_building_level = { province = { id = 13247 } building = coastal_bunker level > 0 } } }')
    code += 'COLDWAR_CUB_apply_foreign_diplomacy = yes\nset_variable = { COLDWAR_CUB_probe_cash = treasury }\nsubtract_from_variable = { COLDWAR_CUB_probe_cash = 0.20 }\n'
    code += 'set_variable = { COLDWAR_CUB_probe_requirement = modifier@send_volunteer_divisions_required }\nsubtract_from_variable = { COLDWAR_CUB_probe_requirement = 0.25 }\nset_variable = { COLDWAR_CUB_probe_tension = modifier@send_volunteers_tension }\nsubtract_from_variable = { COLDWAR_CUB_probe_tension = 0.05 }\n'
    code += 'COLDWAR_CUB_apply_foreign_overseas = yes\nCOLDWAR_CUB_apply_foreign_overseas = yes\n'
    code += check('overseas_native_thresholds_paid_once', 'check_variable = { treasury = COLDWAR_CUB_probe_cash } check_variable = { COLDWAR_CUB_foreign_send_volunteer_divisions_required = -0.25 } check_variable = { COLDWAR_CUB_foreign_send_volunteers_tension = -0.05 } has_dynamic_modifier = { modifier = COLDWAR_CUB_foreign_programme }')
    code += check('overseas_threshold_reader_reaches_native_modifier', 'check_variable = { modifier@send_volunteer_divisions_required = COLDWAR_CUB_probe_requirement } check_variable = { modifier@send_volunteers_tension = COLDWAR_CUB_probe_tension }')
    code += 'COLDWAR_CUB_apply_foreign_advisers = yes\n'
    code += check('adviser_posture_native_capacity_and_cost', 'has_country_flag = COLDWAR_CUB_foreign_advisers_applied check_variable = { COLDWAR_CUB_foreign_send_volunteer_size = 1 } check_variable = { COLDWAR_CUB_foreign_army_personnel_cost_multiplier_modifier = 0.09 }')
    code += 'COLDWAR_CUB_apply_foreign_expeditionary = yes\n'
    code += check('posture_exclusion_enforced_in_reward', 'NOT = { has_country_flag = COLDWAR_CUB_foreign_expeditionary_applied } check_variable = { COLDWAR_CUB_foreign_send_volunteer_size = 1 }')
    # A hypothetical sovereign, compatible partner is fixture-owned test setup.
    code += 'POR = { release = AGL }\nAGL = { set_variable = { ruling_party = 4 } }\nETH = { set_variable = { ruling_party = 4 } }\n'
    code += 'complete_national_focus = COLDWAR_CUB_medical_brigades\nset_country_flag = COLDWAR_CUB_medical_brigades_applied\n'
    filename = 'COLDWAR_CUB_1970_foreign_contracts.txt'
    proposals = [n for n in MODEL['nodes'] if n.get('partner')]
    for n in proposals:
        key = n['key'].removeprefix('foreign_'); tag = n['partner']; base = 'COLDWAR_CUB_foreign_'+key
        for excluded in n['mutually_exclusive']:
            code += f'clr_country_flag = {excluded}_applied\n'
        if key == 'specialisation':
            code += 'add_ideas = COLDWAR_CUB_cmea_member\n'
        if key in ('symbolic', 'cession'):
            code += seed(n['key'])+f'COLDWAR_CUB_apply_{n["key"]} = yes\n'
            code += check(key+'_blocked_before_1972', f'owns_state = 1252 NOT = {{ has_country_flag = {n["id"]}_applied }} NOT = {{ has_country_flag = {base}_offer_open }}')
            continue
        if key in ('ddr','ddr_industry','ddr_science'):
            code += seed(n['key'])+f'COLDWAR_CUB_apply_{n["key"]} = yes\n'
            code += check(key+'_blocked_without_ratified_parent', f'NOT = {{ has_country_flag = {n["id"]}_applied }} NOT = {{ has_country_flag = {base}_offer_open }}')
            # Do not let fixture-only parent receipts contaminate later date tests.
            code += '\n'.join('clr_country_flag = '+p[0]+'_applied' for p in n['prerequisites'])+'\n'
            continue
        DELIVERY_EXPECTED.append(n['key']+' '+tag)
        for owner,target in (('CUB',tag),(tag,'CUB')):
            for cls in ('dip','fin','eco','mil'):
                for direction in ('on_us','by_us'):
                    arr=f'imp_{cls}_sanc_{direction}'
                    code += f'{owner} = {{ if = {{ limit = {{ is_in_array = {{ array = {arr} value = {target} }} }} remove_from_array = {{ array = {arr} value = {target} }} }} }}\n'
        accept=payload(base.replace('_'+key,'_accept_'+key),tag,filename)
        refuse=payload('COLDWAR_CUB_foreign_refuse_'+key,tag,filename)
        reopen=payload('COLDWAR_CUB_foreign_reopen_'+key,tag,filename)
        cancel=payload('COLDWAR_CUB_foreign_cancel_'+key,tag,filename)
        code += f'set_variable = {{ COLDWAR_CUB_probe_cash = treasury }}\n{tag} = {{ set_variable = {{ COLDWAR_CUB_probe_cash = treasury }} }}\n'
        code += seed(n['key'])+f'COLDWAR_CUB_apply_{n["key"]} = yes\n'
        code += check(key+'_focus_opens_recipient_proposal', f'has_country_flag = {n["id"]}_applied has_country_flag = {base}_offer_open {tag} = {{ has_country_flag = {base}_offer_pending }}')
        alternatives=[other for other in proposals if other['id'] in n['mutually_exclusive']]
        if alternatives:
            wrong=alternatives[0]['key'].removeprefix('foreign_')
            code += f'{tag} = {{ '+payload('COLDWAR_CUB_foreign_accept_'+wrong,tag,filename)+' }\n'
            code += check(key+'_cannot_accept_different_terms',f'NOT = {{ has_country_flag = {base}_signed }} NOT = {{ has_country_flag = COLDWAR_CUB_foreign_{wrong}_signed }} check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} {tag} = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}')
        code += f'{tag} = {{ {refuse} }}\n'
        code += check(key+'_refusal_has_no_cost', f'NOT = {{ has_country_flag = {base}_signed }} check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} {tag} = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}')
        code += f'{tag} = {{ {reopen} }}\n'
        cub_cost,partner_cost=n['setup_costs']
        code += f'subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {cub_cost} }}\n{tag} = {{ subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {partner_cost} }} }}\n'
        for e in n.get('accepted_effects',[]):
            if e['kind']=='treasury':
                code+=f'{e["country"]} = {{ add_to_variable = {{ COLDWAR_CUB_probe_cash = {e["amount"]} }} }}\n'
        if key=='sov_industry':
            code+='855 = { set_variable = { COLDWAR_CUB_probe_factory = building_level@industrial_complex } add_to_variable = { COLDWAR_CUB_probe_factory = 1 } }\n'
        if key in ('interests', 'limited', 'settlement'):
            for cls in ('dip','fin','eco','mil'):
                code += f'add_to_array = {{ array = imp_{cls}_sanc_by_us value = USA }}\n'
        accepted_option = event_payload(key,tag) if key in ('soviet','settlement') else accept
        code += f'{tag} = {{ {accepted_option} }}\n'
        paired=f'has_country_flag = {base}_signed {tag} = {{ has_country_flag = {base}_signed }}'
        balances=f'check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} {tag} = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}'
        code += check(key+'_both_signed_exact_cost',paired+' '+balances)
        if key in ('interests','limited'):
            code += check(key+'_can_sign_with_remaining_sanctions',f'NOT = {{ has_idea = {base}_cub }} USA = {{ NOT = {{ has_idea = {base}_partner }} }} '+paired)
        elif key=='settlement':
            code += check('full_settlement_removes_all_four_mutual_restrictions', 'has_idea = COLDWAR_CUB_foreign_settlement_cub USA = { has_idea = COLDWAR_CUB_foreign_settlement_partner } NOT = { has_idea = COLDWAR_CUB_american_embargo } NOT = { has_idea = COLDWAR_CUB_american_embargo_limited }')
        else:
            cubidea = 'COLDWAR_CUB_cmea_member' if key=='cmea' else base+'_cub'
            code += check(key+'_paired_spirits_are_active',f'has_idea = {cubidea} {tag} = {{ has_idea = {base}_partner }}')
        if key=='sov_industry':
            code+=check('sov_industry_camaguey_factory_once','855 = { check_variable = { building_level@industrial_complex = COLDWAR_CUB_probe_factory } }')
        code+=f'{tag} = {{ {accept} }}\nCOLDWAR_CUB_daily_update = yes\n'
        code+=check(key+'_accept_replay_blocked',paired+' '+balances)
        # Keep the interests signature for its two child negotiations.
        if key!='interests':
            code+=f'{tag} = {{ {cancel} }}\nCOLDWAR_CUB_daily_update = yes\n'
            code+=check(key+'_recipient_can_cancel',f'NOT = {{ has_country_flag = {base}_signed }} {tag} = {{ NOT = {{ has_country_flag = {base}_signed }} }} '+balances)
            code+=f'{tag} = {{ {reopen} {accept} }}\n'
            code+=check(key+'_reentry_no_second_fee',paired+' '+balances)
            if key != 'cmea':
                code+=f'{tag} = {{ {cancel} }}\n'
    # All one-sided and mirrored sanctions must suspend both actual spirits.
    code+='set_country_flag = COLDWAR_CUB_foreign_mex_fuel_applied\nclr_country_flag = COLDWAR_CUB_foreign_mex_agro_applied\nMEX = { '+payload('COLDWAR_CUB_foreign_reopen_mex_fuel','MEX',filename)+payload('COLDWAR_CUB_foreign_accept_mex_fuel','MEX',filename)+' }\n'
    paired='has_idea = COLDWAR_CUB_foreign_mex_fuel_cub MEX = { has_idea = COLDWAR_CUB_foreign_mex_fuel_partner }'
    absent='NOT = { has_idea = COLDWAR_CUB_foreign_mex_fuel_cub } MEX = { NOT = { has_idea = COLDWAR_CUB_foreign_mex_fuel_partner } }'
    for owner,target in (('CUB','MEX'),('MEX','CUB')):
        for cls in ('dip','fin','eco','mil'):
            for direction in ('on_us','by_us'):
                arr=f'imp_{cls}_sanc_{direction}'
                code+=f'{owner} = {{ add_to_array = {{ array = {arr} value = {target} }} }}\nCOLDWAR_CUB_daily_update = yes\n'
                code+=check(f'sanction_{owner}_{cls}_{direction}_suspends',absent+' has_country_flag = COLDWAR_CUB_foreign_mex_fuel_signed')
                code+=f'{owner} = {{ remove_from_array = {{ array = {arr} value = {target} }} }}\nCOLDWAR_CUB_daily_update = yes\n'
                code+=check(f'sanction_{owner}_{cls}_{direction}_restores',paired)
    for index,(owner,target) in enumerate((('CUB','MEX'),('MEX','CUB'))):
        name=f'embargo_{owner}_suspends_restores'; event=f'COLDWAR_CUB_ENGINE.{100+index}'
        probe=f'send_embargo = {target}\nCUB = {{ COLDWAR_CUB_daily_update = yes '+check(name+'_suspends',absent)+f' }}\nbreak_embargo = {target}\nCUB = {{ COLDWAR_CUB_daily_update = yes '+check(name+'_restores',paired)+' }'
        EMBARGO_EVENTS+=f'country_event = {{ id = {event} hidden = yes is_triggered_only = yes immediate = {{ if = {{ limit = {{ has_dlc = "By Blood Alone" }} {probe} }} else = {{ log = "COLDWAR_CUB_ENGINE SKIP {name}_suspends requires_By_Blood_Alone" log = "COLDWAR_CUB_ENGINE SKIP {name}_restores requires_By_Blood_Alone" }} }} }}\n'
        code+=f'{owner} = {{ country_event = {{ id = {event} }} }}\n'
    code+='declare_war_on = { target = MEX type = annex_everything }\nCOLDWAR_CUB_daily_update = yes\n'
    code+=check('war_suspends_both_keeps_signature',absent+' has_country_flag = COLDWAR_CUB_foreign_mex_fuel_signed has_war_with = MEX')
    code+='white_peace = { tag = MEX }\nCOLDWAR_CUB_daily_update = yes\n'
    code+=check('peace_restores_both',paired+' NOT = { has_war_with = MEX }')
    code+='MEX = { clr_country_flag = COLDWAR_CUB_foreign_mex_fuel_signed } COLDWAR_CUB_foreign_cancel_mex_fuel = yes\n'
    code+=check('termination_cleans_orphaned_partner_receipt',absent+' NOT = { has_country_flag = COLDWAR_CUB_foreign_mex_fuel_signed }')
    code+='log = "COLDWAR_CUB_ENGINE COMPLETE"\n'
    return '# IMPERIA COLD WAR — Isolated native execution fixture.\nCOLDWAR_CUB_ENGINE_run = { '+code+' }\n'


def build_islands(check, payload, event_payload):
    global EMBARGO_EVENTS, DELIVERY_EXPECTED, NAME_EXPECTED
    EMBARGO_EVENTS = ''
    DELIVERY_EXPECTED = []
    NAME_EXPECTED = ['symbolic Ernst Thälmann Island','cession_pending Cayo Blanco del Sur','cession Ernst Thälmann Island']
    filename = 'COLDWAR_CUB_1970_foreign_contracts.txt'
    code = 'log = "COLDWAR_CUB_ENGINE START"\nCOLDWAR_CUB_initialize = yes\n'
    code += check('future_fixture_date_and_scenario', 'date > 1972.6.18 COLDWAR_CUB_is_1970 = yes country_exists = DDR owns_state = 1252')
    for owner, target in (('CUB','DDR'),('DDR','CUB')):
        for cls in ('dip','fin','eco','mil'):
            for direction in ('on_us','by_us'):
                arr=f'imp_{cls}_sanc_{direction}'
                code += f'{owner} = {{ if = {{ limit = {{ is_in_array = {{ array = {arr} value = {target} }} }} remove_from_array = {{ array = {arr} value = {target} }} }} }}\n'
    for key in ('symbolic','cession'):
        DELIVERY_EXPECTED.append('foreign_'+key+' DDR')
        base='COLDWAR_CUB_foreign_'+key
        if key=='cession':
            code += '1252 = { set_state_name = "Cayo Blanco del Sur" }\n'
        code += seed('foreign_'+key)
        code += f'set_variable = {{ COLDWAR_CUB_probe_cash = treasury }}\nDDR = {{ set_variable = {{ COLDWAR_CUB_probe_cash = treasury }} }}\n'
        code += f'COLDWAR_CUB_apply_foreign_{key} = yes\n'
        code += check(key+'_offers_do_not_transfer_or_charge', f'has_country_flag = {base}_offer_open DDR = {{ has_country_flag = {base}_offer_pending check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }} owns_state = 1252 check_variable = {{ treasury = COLDWAR_CUB_probe_cash }}')
        if key=='symbolic':
            code += check('symbolic_completes_without_transfer', 'has_country_flag = COLDWAR_CUB_foreign_symbolic_applied owns_state = 1252')
            code += '1252 = { log = "COLDWAR_CUB_STATE_NAME symbolic [THIS.GetName]" }\n'
        else:
            code += '1252 = { log = "COLDWAR_CUB_STATE_NAME cession_pending [THIS.GetName]" }\n'
        code += 'DDR = { '+payload('COLDWAR_CUB_foreign_refuse_'+key,'DDR',filename)+' }\n'
        code += check(key+'_refusal_keeps_sovereignty_and_money', f'owns_state = 1252 NOT = {{ has_country_flag = {base}_signed }} check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} DDR = {{ check_variable = {{ treasury = COLDWAR_CUB_probe_cash }} }}')
        code += 'DDR = { '+payload('COLDWAR_CUB_foreign_reopen_'+key,'DDR',filename)+' }\n'
        if key=='symbolic':
            code += 'subtract_from_variable = { COLDWAR_CUB_probe_cash = 0.05 }\nDDR = { subtract_from_variable = { COLDWAR_CUB_probe_cash = 0.05 } }\n'
        else:
            code += 'add_to_variable = { COLDWAR_CUB_probe_cash = 0.40 }\nDDR = { subtract_from_variable = { COLDWAR_CUB_probe_cash = 0.40 } }\n'
        code += 'DDR = { '+payload('COLDWAR_CUB_foreign_accept_'+key,'DDR',filename)+' }\n'
        paired=f'has_country_flag = {base}_signed has_idea = {base}_cub DDR = {{ has_country_flag = {base}_signed has_idea = {base}_partner }}'
        balances='check_variable = { treasury = COLDWAR_CUB_probe_cash } DDR = { check_variable = { treasury = COLDWAR_CUB_probe_cash } }'
        code += check(key+'_ratification_exact_cost_and_paired_spirits',paired+' '+balances)
        if key=='symbolic':
            code += check('symbolic_never_transfers_state', 'owns_state = 1252 1252 = { is_core_of = CUB NOT = { is_core_of = DDR } }')
        else:
            code += check('cession_transfers_only_island_preserves_cuban_core', 'owns_state = 854 owns_state = 855 owns_state = 1121 1252 = { is_owned_and_controlled_by = DDR is_core_of = CUB NOT = { is_core_of = DDR } }')
            code += '1252 = { log = "COLDWAR_CUB_STATE_NAME cession [THIS.GetName]" }\n'
        code += 'DDR = { '+payload('COLDWAR_CUB_foreign_accept_'+key,'DDR',filename)+' }\n'
        code += check(key+'_ratification_cannot_replay_money',paired+' '+balances)
        if key=='cession':
            for child in ('ddr','ddr_industry','ddr_science'):
                n=BY['foreign_'+child]; childbase='COLDWAR_CUB_foreign_'+child
                DELIVERY_EXPECTED.append(n['key']+' DDR')
                cc,pc=n['setup_costs']
                code += seed(n['key'])+f'COLDWAR_CUB_apply_{n["key"]} = yes\n'
                code += check(child+'_real_focus_opens_offer',f'has_country_flag = {n["id"]}_applied has_country_flag = {childbase}_offer_open DDR = {{ has_country_flag = {childbase}_offer_pending }}')
                code += f'subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {cc} }} DDR = {{ subtract_from_variable = {{ COLDWAR_CUB_probe_cash = {pc} }} }}\n'
                if child=='ddr_industry':
                    code += '855 = { set_variable = { COLDWAR_CUB_probe_agriculture = building_level@agriculture_district } add_to_variable = { COLDWAR_CUB_probe_agriculture = 1 } }\n'
                code += 'DDR = { '+event_payload(child,'DDR')+' }\n'
                childpaired=f'has_idea = {childbase}_cub DDR = {{ has_idea = {childbase}_partner }}'
                code += check(child+'_event_accepts_pair_and_exact_cost',childpaired+' '+balances)
                if child=='ddr_industry':
                    code += check('ddr_citrus_builds_actual_agriculture','855 = { check_variable = { building_level@agriculture_district = COLDWAR_CUB_probe_agriculture } }')
                code += 'DDR = { '+event_payload(child,'DDR')+' }\n'
                code += check(child+'_popup_cannot_replay',childpaired+' '+balances)
            children='NOT = { has_idea = COLDWAR_CUB_foreign_ddr_industry_cub } NOT = { has_idea = COLDWAR_CUB_foreign_ddr_science_cub } DDR = { NOT = { has_idea = COLDWAR_CUB_foreign_ddr_industry_partner } NOT = { has_idea = COLDWAR_CUB_foreign_ddr_science_partner } }'
            code += 'DDR = { '+payload('COLDWAR_CUB_foreign_cancel_ddr','DDR',filename)+' } COLDWAR_CUB_daily_update = yes\n'
            code += check('ddr_parent_cancellation_suspends_children',children+' has_country_flag = COLDWAR_CUB_foreign_ddr_industry_signed has_country_flag = COLDWAR_CUB_foreign_ddr_science_signed '+balances)
            code += 'DDR = { '+payload('COLDWAR_CUB_foreign_reopen_ddr','DDR',filename)+event_payload('ddr','DDR')+' } COLDWAR_CUB_daily_update = yes\n'
            code += check('ddr_parent_restoration_resumes_without_fees','has_idea = COLDWAR_CUB_foreign_ddr_industry_cub has_idea = COLDWAR_CUB_foreign_ddr_science_cub DDR = { has_idea = COLDWAR_CUB_foreign_ddr_industry_partner has_idea = COLDWAR_CUB_foreign_ddr_science_partner } '+balances+' 855 = { check_variable = { building_level@agriculture_district = COLDWAR_CUB_probe_agriculture } }')
        code += 'DDR = { '+payload('COLDWAR_CUB_foreign_cancel_'+key,'DDR',filename)+' }\nCOLDWAR_CUB_foreign_reconcile_all = yes\n'
        code += check(key+'_cancellation_removes_both_spirits', f'NOT = {{ has_idea = {base}_cub }} DDR = {{ NOT = {{ has_idea = {base}_partner }} }} '+balances)
        if key=='symbolic':
            # Fixture-only branch reset allows two independent policy tests in one boot.
            code += 'clr_country_flag = COLDWAR_CUB_foreign_symbolic_applied\n'
        else:
            code += 'DDR = { '+payload('COLDWAR_CUB_foreign_reopen_'+key,'DDR',filename)+' }\n'
            code += check('cession_cannot_be_reoffered_after_ownership_changes', 'DDR = { owns_state = 1252 NOT = { has_country_flag = COLDWAR_CUB_foreign_cession_offer_pending } } NOT = { has_country_flag = COLDWAR_CUB_foreign_cession_offer_open } '+balances)
    code += 'log = "COLDWAR_CUB_ENGINE COMPLETE"\n'
    return '# IMPERIA COLD WAR — Isolated future-date island fixture.\nCOLDWAR_CUB_ENGINE_run = { '+code+' }\n'
