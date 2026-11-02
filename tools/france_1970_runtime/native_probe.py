# IMPERIA COLD WAR — Isolated France 1970 native transaction fixture.
"""Freeze target providers in a new E: profile and inspect one hidden HOI4 process.

The fixture has artificial balances and research for assertions. It does not
modify a player profile, save, playset, existing game process or live mod file.
It is not a human recipient/UI, save/reload or multiplayer rehearsal.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNTIME = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/france_1970')
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MARK = '# IMPERIA COLD WAR — Isolated France 1970 native fixture.\n'
PREFIX = 'ICW_FRA2_NATIVE'
CHECKS = []
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assertion(name, condition):
    CHECKS.append(name)
    return (f'if = {{ limit = {{ {condition} }} log = "{PREFIX} PASS {name}" }}\n'
            f'else = {{ log = "{PREFIX} FAIL {name}" }}\n')


def number(value):
    return format(Decimal(str(value)), 'f')


def equal(var, value):
    return f'check_variable = {{ var = {var} value = {number(value)} compare = equals }}'


def fixture(design):
    from core import PARTY_REVISION_MIGRATION_FLAG
    CHECKS.clear()
    bykey = {n['key']: n for n in design['nodes']}
    out = [assertion('scenario_and_tree', 'tag = FRA IMP_is_1970_scenario = yes has_focus_tree = COLDWAR_FRA2_1970_focus'),
           assertion('initial_receipt', 'has_country_flag = COLDWAR_FRA2_initialized'),
           assertion('historical_governing_party', 'western_conservatism_are_in_power = yes')]
    for spirit in design['starting_spirits']:
        out.append(assertion('initial_' + spirit['id'], 'has_idea = ' + spirit['id']))
    out += ['set_variable = { ruling_party = 1 }\nset_variable = { gdp_total = 1000 }\nset_variable = { treasury = 1000 }\nclr_country_flag = MD_skip_treasury_cost\n',
            'COLDWAR_FRA2_complete_public_service = yes\n',
            assertion('domestic_own_gdp_fee', equal('treasury', '999.2')),
            assertion('domestic_receipt', 'has_country_flag = COLDWAR_FRA2_earned_public_service'),
            'COLDWAR_FRA2_complete_public_service = yes\n',
            assertion('domestic_no_replay', equal('treasury', '999.2')),
            'COLDWAR_FRA2_complete_progress = yes\n',
            assertion('gaullist_programme_active', 'has_dynamic_modifier = { modifier = COLDWAR_FRA2_udr_programme }'),
            'set_variable = { ICW_FRA2_saved_treasury = treasury }\nset_variable = { ruling_party = 2 }\nFRA_update_party_programmes = yes\n',
            assertion('party_departure', 'NOT = { has_dynamic_modifier = { modifier = COLDWAR_FRA2_udr_programme } }'),
            assertion('shared_programme_retained', 'has_dynamic_modifier = { modifier = COLDWAR_FRA2_institutions_programme }'),
            'set_variable = { ruling_party = 1 }\nFRA_update_party_programmes = yes\n',
            assertion('party_return', 'has_dynamic_modifier = { modifier = COLDWAR_FRA2_udr_programme }'),
            assertion('party_return_no_charge', 'check_variable = { var = treasury value = ICW_FRA2_saved_treasury compare = equals }')]
    # Exercise the actual instantaneous infrastructure helper, including the
    # native physical-level getter and its one-time country receipt.
    helpers = nodes((ROOT / 'common/scripted_effects/COLDWAR_FRA2_1970_effects.txt').read_text(encoding='utf-8'))
    housing_helper = next(n.key for n in helpers if n.key.startswith('COLDWAR_FRA2_build_housing_'))
    housing_receipt = housing_helper.replace('_build_', '_asset_', 1)
    out += ['56 = { set_variable = { ICW_FRA2_infra_before = building_level@infrastructure } }\n',
            housing_helper + ' = yes\n',
            '56 = { set_variable = { ICW_FRA2_infra_delta = building_level@infrastructure } subtract_from_variable = { ICW_FRA2_infra_delta = ICW_FRA2_infra_before }\n',
            assertion('infrastructure_added', equal('ICW_FRA2_infra_delta', 1)),
            'set_variable = { ICW_FRA2_infra_after = building_level@infrastructure } }\n',
            assertion('asset_country_receipt', 'has_country_flag = ' + housing_receipt),
            housing_helper + ' = yes\n',
            assertion('asset_no_replay', '56 = { check_variable = { var = building_level@infrastructure value = ICW_FRA2_infra_after compare = equals } }')]
    offers = [(n['key'], n['offer']) for n in design['nodes'] if n.get('offer')]
    groups = {g['id']: g for g in design['groups']}
    # Keep the historical CoCom relationship in the real mod. Lift it only in
    # this private fixture, after proving that it blocks the first Soviet offer.
    out += [assertion('soviet_seeded_cocom_link', 'is_in_array = { array = imp_mil_sanc_by_us value = SOV } SOV = { is_in_array = { array = imp_mil_sanc_on_us value = FRA } }'),
            assertion('soviet_restricted_send_blocked', 'NOT = { COLDWAR_FRA2_offer_can_send_soviet_science = yes }'),
            'remove_from_array = { array = imp_mil_sanc_by_us value = SOV }\nSOV = { remove_from_array = { array = imp_mil_sanc_on_us value = FRA } }\n',
            assertion('soviet_cocom_lift_opens_pair', 'COLDWAR_FRA2_pair_SOV_clear = yes')]
    for key, offer in offers:
        partner = offer['partner']
        family = offer['family']
        fraidea, otheridea = offer['france']['spirit'], offer['recipient']['spirit']
        node = bykey[key]
        slot = groups[node['group']].get('slot') or 1
        wrong_slot = 2 if slot == 1 else 1
        out.append(f'set_variable = {{ ruling_party = {slot} }}\n')
        for tag, gdp in [('FRA', 1000), (partner, 500)]:
            out.append(f'{tag} = {{ set_variable = {{ gdp_total = {gdp} }} set_variable = {{ treasury = 1000 }} clr_country_flag = MD_skip_treasury_cost }}\n')
        # Positive technology gates are fixture inputs, never start-game grants.
        if key == 'symphonie':
            out.append('set_technology = { internet_1 = 1 }\nGER = { set_technology = { internet_1 = 1 } }\n')
        if key.startswith('nato_'):
            out.append(f'add_ideas = NATO_member\n{partner} = {{ add_ideas = NATO_member }}\n')
        if key == 'fn_export':
            out.append(assertion('fn_export_future_identity_blocked_1970', 'NOT = { COLDWAR_FRA2_offer_can_send_fn_export = yes }'))
            continue
        seeded_parents = []
        # Memberships and actual active parent agreements are explicit fixture
        # inputs. They are never granted by the installed focus implementation.
        import re
        for condition in offer.get('activation_conditions', []):
            match = re.fullmatch(r'(\w+) = \{ has_idea = (\w+) \}', condition)
            if not match:
                continue
            tag, idea = match.groups()
            out.append(f'{tag} = {{ add_ideas = {idea} }}\n')
            for parentkey, parent in offers:
                if idea in (parent['france']['spirit'], parent['recipient']['spirit']) and parentkey not in seeded_parents:
                    seeded_parents.append(parentkey)
                    out.append(f'set_country_flag = COLDWAR_FRA2_signed_{parentkey}\n{parent["partner"]} = {{ set_country_flag = COLDWAR_FRA2_signed_{parentkey} }}\n')
        if offer.get('proposal_party'):
            out.append(f'set_variable = {{ ruling_party = {wrong_slot} }}\n')
            out.append(assertion(key + '_wrong_party_send_blocked', f'NOT = {{ COLDWAR_FRA2_offer_can_send_{key} = yes }}'))
            out.append(f'set_variable = {{ ruling_party = {slot} }}\n')
        if key == 'algeria_training':
            parent = bykey['algeria_energy']['offer']
            out.append('set_country_flag = COLDWAR_FRA2_signed_algeria_energy\nALG = { set_country_flag = COLDWAR_FRA2_signed_algeria_energy }\nCOLDWAR_FRA2_sync_treaties = yes\n')
            out.append(assertion('dependent_parent_active', f'has_idea = {parent["france"]["spirit"]} ALG = {{ has_idea = {parent["recipient"]["spirit"]} }}'))
        if key == 'airbus':
            out.append(assertion('offer_france_gdp_input', equal('gdp_total', 1000)))
            out.append(assertion('offer_partner_gdp_input', f'{partner} = {{ {equal("gdp_total", 500)} }}'))
            out.append(assertion('offer_pair_exists', f'country_exists = {partner}'))
            out.append(assertion('offer_bilateral_peace', f'NOT = {{ has_war_with = {partner} }} {partner} = {{ NOT = {{ has_war_with = FRA }} }}'))
            out.append(assertion('offer_no_bilateral_embargo', f'NOT = {{ is_embargoing = {partner} }} {partner} = {{ NOT = {{ is_embargoing = FRA }} }}'))
            out.append(assertion('offer_positive_gdp_operator', f'check_variable = {{ gdp_total > 0 }} {partner} = {{ check_variable = {{ gdp_total > 0 }} }}'))
            out.append(f'if = {{ limit = {{ check_variable = {{ var = gdp_total value = 0 compare = greater_than }} {partner} = {{ check_variable = {{ var = gdp_total value = 0 compare = greater_than }} }} }} log = "{PREFIX} DIAG positive_gdp_enum=yes" }} else = {{ log = "{PREFIX} DIAG positive_gdp_enum=no" }}\n')
            for family_code in ('dip', 'fin', 'eco', 'mil'):
                for direction in ('on', 'by'):
                    array = f'imp_{family_code}_sanc_{direction}_us'
                    out.append(assertion(f'offer_no_{family_code}_{direction}', f'NOT = {{ is_in_array = {{ array = {array} value = {partner} }} }} {partner} = {{ NOT = {{ is_in_array = {{ array = {array} value = FRA }} }} }}'))
            out.append(assertion('offer_pair_clear', f'COLDWAR_FRA2_pair_{partner}_clear = yes'))
            out.append(assertion('offer_can_send', 'COLDWAR_FRA2_offer_can_send_airbus = yes'))
        out.append(f'COLDWAR_FRA2_offer_{key} = yes\n')
        out.append(assertion(key + '_recipient_pending', f'has_country_flag = COLDWAR_FRA2_pending_{key} {partner} = {{ has_country_flag = COLDWAR_FRA2_pending_{key} }}'))
        out.append(assertion(key + '_no_award_before_consent', f'NOT = {{ has_idea = {fraidea} }} {partner} = {{ NOT = {{ has_idea = {otheridea} }} }}'))
        if offer.get('proposal_party'):
            out.append(f'set_variable = {{ ruling_party = {wrong_slot} }}\n{partner} = {{ COLDWAR_FRA2_accept_{key} = yes }}\n')
            out.append(assertion(key + '_party_change_blocks_acceptance', f'NOT = {{ has_country_flag = COLDWAR_FRA2_signed_{key} }} '+equal('treasury',1000)+f' {partner} = {{ '+equal('treasury',1000)+' }'))
            out.append(f'set_variable = {{ ruling_party = {slot} }}\n')
        assets = [(side, index, effect) for side in ('france', 'recipient') for index, effect in enumerate(offer[side]['effects']) if effect['kind'] == 'building']
        for side, index, effect in assets:
            var = f'ICW_FRA2_{key}_{side}_{index}'
            out.append(f'{effect["state"]} = {{ set_variable = {{ {var}_before = building_level@{effect["building"]} }} }}\n')
        out.append(f'{partner} = {{ COLDWAR_FRA2_accept_{key} = yes }}\n')
        out.append(assertion(key + '_paired_active', f'has_idea = {fraidea} {partner} = {{ has_idea = {otheridea} }}'))
        if offer.get('proposal_party'):
            out.append(f'set_variable = {{ ruling_party = {wrong_slot} }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
            out.append(assertion(key + '_signed_treaty_survives_election', f'has_idea = {fraidea} {partner} = {{ has_idea = {otheridea} }}'))
            out.append(f'set_variable = {{ ruling_party = {slot} }}\n')
        for side, index, effect in assets:
            var = f'ICW_FRA2_{key}_{side}_{index}'
            out.append(f'{effect["state"]} = {{ set_variable = {{ {var}_after = building_level@{effect["building"]} }} set_variable = {{ {var}_delta = {var}_after }} subtract_from_variable = {{ {var}_delta = {var}_before }}\n')
            out.append(assertion(key + '_' + side + '_building_added', equal(var + '_delta', effect['amount'])))
            out.append('}\n')
        for side, tag, gdp in [('france', 'FRA', 1000), ('recipient', partner, 500)]:
            share = next(e['runtime_share_literal'] for e in offer[side]['effects'] if e['kind'] == 'treasury_gdp')
            expected = Decimal(1000) + Decimal(gdp) * Decimal(share)
            out.append(assertion(key + '_' + side + '_own_gdp_fee', f'{tag} = {{ {equal("treasury", expected)} }}'))
        out.append(f'{partner} = {{ COLDWAR_FRA2_accept_{key} = yes }}\n')
        for side, index, effect in assets:
            var = f'ICW_FRA2_{key}_{side}_{index}'
            out.append(assertion(key + '_' + side + '_building_no_replay', f'{effect["state"]} = {{ check_variable = {{ var = building_level@{effect["building"]} value = {var}_after compare = equals }} }}'))
        for side, tag, gdp in [('france', 'FRA', 1000), ('recipient', partner, 500)]:
            share = next(e['runtime_share_literal'] for e in offer[side]['effects'] if e['kind'] == 'treasury_gdp')
            expected = Decimal(1000) + Decimal(gdp) * Decimal(share)
            out.append(assertion(key + '_' + side + '_no_duplicate_fee', f'{tag} = {{ {equal("treasury", expected)} }}'))
        if key == 'airbus':
            # Exercise each mirrored sanction class in both signatory scopes.
            for family_code in ('dip', 'fin', 'eco', 'mil'):
                for direction in ('on', 'by'):
                    for tag, target in [('FRA', partner), (partner, 'FRA')]:
                        array = f'imp_{family_code}_sanc_{direction}_us'
                        label = f'airbus_{family_code}_{direction}_{tag}'
                        out.append(f'{tag} = {{ add_to_array = {{ array = {array} value = {target} }} }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
                        out.append(assertion(label + '_suspended', f'NOT = {{ has_idea = {fraidea} }} {partner} = {{ NOT = {{ has_idea = {otheridea} }} }}'))
                        out.append(f'{tag} = {{ remove_from_array = {{ array = {array} value = {target} }} }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
                        out.append(assertion(label + '_restored', f'has_idea = {fraidea} {partner} = {{ has_idea = {otheridea} }}'))
            for tag, side, gdp in [('FRA', 'france', 1000), (partner, 'recipient', 500)]:
                annual = next(e['runtime_share_literal'] for e in offer[side]['effects'] if e['kind'] == 'weekly_gdp_expense')
                out.append(f'{tag} = {{ set_variable = {{ additional_expenses_rate = 0 }} COLDWAR_FRA2_add_weekly_expenses = yes\n')
                # Compare to the exact same fixed-point arithmetic, rather than
                # asserting a higher-precision Python decimal as a game literal.
                out.append(f'set_temp_variable = {{ ICW_FRA2_expected_weekly = {{ value = gdp_total multiply = {annual} divide = 52 }} }}\n')
                out.append(assertion('weekly_' + side + '_own_gdp', 'check_variable = { var = additional_expenses_rate value = ICW_FRA2_expected_weekly compare = equals }'))
                out.append(assertion('weekly_' + side + '_nonzero', 'check_variable = { var = additional_expenses_rate value = 0 compare = greater_than }'))
                out.append('}\n')
        if key.startswith('nato_'):
            out.append(f'{partner} = {{ remove_ideas = NATO_member }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
            out.append(assertion(key + '_membership_suspended', f'NOT = {{ has_idea = {fraidea} }} {partner} = {{ NOT = {{ has_idea = {otheridea} }} NOT = {{ has_idea = NATO_member }} }}'))
            out.append(f'{partner} = {{ add_ideas = NATO_member }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
            out.append(assertion(key + '_membership_restored', f'has_idea = {fraidea} {partner} = {{ has_idea = {otheridea} }}'))
        out.append(f'clr_country_flag = COLDWAR_FRA2_signed_{key}\nclr_country_flag = COLDWAR_FRA2_family_signed_{family}\n{partner} = {{ clr_country_flag = COLDWAR_FRA2_signed_{key} }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
        for parentkey in seeded_parents:
            parent = bykey[parentkey]['offer']
            out.append(f'clr_country_flag = COLDWAR_FRA2_signed_{parentkey}\n{parent["partner"]} = {{ clr_country_flag = COLDWAR_FRA2_signed_{parentkey} }}\nCOLDWAR_FRA2_sync_treaties = yes\n')
        if key == 'algeria_training':
            out.append('clr_country_flag = COLDWAR_FRA2_signed_algeria_energy\nALG = { clr_country_flag = COLDWAR_FRA2_signed_algeria_energy }\nCOLDWAR_FRA2_sync_treaties = yes\n')
    # Exercise actual emitted decision bodies, including their execution guards,
    # instead of manufacturing a simplified model of the payment transaction.
    decision_text = (ROOT / 'common/decisions/COLDWAR_FRA2_1970_decisions.txt').read_text(encoding='utf-8')
    decision_rows = [d for category in nodes(decision_text) for d in category.children()]
    for decision in design['decisions']:
        if not decision['id'].startswith('COLDWAR_FRA2P_'):
            continue
        did = decision['id']
        key = did.removeprefix('COLDWAR_FRA2P_')
        parent = 'participation' if key == 'participation_workshops' else 'public_banks'
        slot = 1 if key == 'participation_workshops' else 3
        wrong_slot = 2 if slot == 1 else 1
        row = next(d for d in decision_rows if d.key == did)
        complete = next(c for c in row.children() if c.key == 'complete_effect')
        block = decision_text[complete.start:complete.end]
        body = block[block.index('{') + 1:block.rindex('}')] + '\n'
        asset = next(e for e in decision['effects'] if e['kind'] == 'building')
        state, building = asset['state'], asset['building']
        out.append(f'set_variable = {{ ruling_party = {slot} }}\ncomplete_national_focus = COLDWAR_FRA2_{parent}\n')
        out.append(f'set_variable = {{ gdp_total = 1000 }}\nset_variable = {{ treasury = 1000 }}\n{state} = {{ set_variable = {{ ICW_FRA2_decision_before = building_level@{building} }} }}\n')
        out.append(f'set_variable = {{ ruling_party = {wrong_slot} }}\n' + body)
        out.append(assertion(key + '_wrong_party_no_transaction', equal('treasury',1000)+f' NOT = {{ has_country_flag = {did}_completed }}'))
        out.append(f'set_variable = {{ ruling_party = {slot} }}\n' + body)
        fee = next(e for e in decision['effects'] if e['kind'] == 'treasury_gdp')
        expected = Decimal(1000) + Decimal(1000) * Decimal(fee['runtime_share_literal'])
        out.append(assertion(key + '_own_gdp_fee', equal('treasury',expected)))
        out.append(assertion(key + '_receipt', f'has_country_flag = {did}_completed'))
        out.append(f'{state} = {{ set_variable = {{ ICW_FRA2_decision_after = building_level@{building} }} set_variable = {{ ICW_FRA2_decision_delta = ICW_FRA2_decision_after }} subtract_from_variable = {{ ICW_FRA2_decision_delta = ICW_FRA2_decision_before }}\n')
        out.append(assertion(key + '_asset_added',equal('ICW_FRA2_decision_delta',1))+'}\n')
        out.append(body)
        out.append(assertion(key + '_no_replay_fee', equal('treasury',expected)))
        out.append(assertion(key + '_no_replay_asset',f'{state} = {{ check_variable = {{ var = building_level@{building} value = ICW_FRA2_decision_after compare = equals }} }}'))
    out += ['set_country_flag = COLDWAR_FRA2_earned_soviet_friendship\nset_country_flag = COLDWAR_FRA2_earned_pooled_armour\n',
            'add_dynamic_modifier = { modifier = COLDWAR_FRA2_pcf_parent_soviet_science_programme }\n',
            'set_variable = { COLDWAR_FRA2_pcf_parent_soviet_science_land_doctrine_cost_factor = -0.06 }\nset_variable = { COLDWAR_FRA2_pcf_parent_soviet_science_foreign_influence_modifier = -0.05 }\nset_variable = { COLDWAR_FRA2_defence_production_factory_efficiency_gain_factor = 0.99 }\n',
            f'set_variable = {{ ICW_FRA2_before_migration = treasury }}\nclr_country_flag = {PARTY_REVISION_MIGRATION_FLAG}\nCOLDWAR_FRA2_migrate_party_revision = yes\n',
            assertion('migration_removes_legacy_unilateral_soviet_modifiers',equal('COLDWAR_FRA2_pcf_parent_soviet_science_land_doctrine_cost_factor',0)+' '+equal('COLDWAR_FRA2_pcf_parent_soviet_science_foreign_influence_modifier',0)),
            assertion('migration_detaches_retired_dynamic_pool','NOT = { has_dynamic_modifier = { modifier = COLDWAR_FRA2_pcf_parent_soviet_science_programme } }'),
            assertion('shared_components_tangible_production_penalty',equal('COLDWAR_FRA2_defence_production_factory_efficiency_gain_factor','-0.08')),
            assertion('migration_no_treasury_replay','check_variable = { var = treasury value = ICW_FRA2_before_migration compare = equals }'),
            'COLDWAR_FRA2_migrate_party_revision = yes\n',
            assertion('migration_no_modifier_stacking',equal('COLDWAR_FRA2_defence_production_factory_efficiency_gain_factor','-0.08'))]
    # Complete coherent native focus paths for the revised national recoveries.
    # No elapsed-time claim is made: instant completion is a private fixture input.
    completed = set()
    def complete_path(key):
        if key in completed:
            return
        node = bykey[key]
        for alternatives in node.get('prerequisites', []):
            parent = next((p for p in alternatives if p in completed), alternatives[0])
            complete_path(parent)
        completed.add(key)
        out.append(f'complete_national_focus = {node["id"]}\n')
    out.append('set_variable = { ruling_party = 1 }\nset_variable = { gdp_total = 1000 }\nset_variable = { treasury = 1000 }\n')
    complete_path('parliament')
    out.append(assertion('constitutional_first_choice_keeps_residual',
        'NOT = { has_idea = COLDWAR_FRA2_presidency } has_idea = COLDWAR_FRA2_institutional_balance_residual'))
    out.append('COLDWAR_FRA2_complete_parliament = yes\n')
    out.append(assertion('constitutional_replay_keeps_one_residual','has_idea = COLDWAR_FRA2_institutional_balance_residual'))
    complete_path('civic_settlement')
    out.append(assertion('funded_civic_chain_resolves_institutional_residual',
        'has_country_flag = COLDWAR_FRA2_earned_civic_settlement NOT = { has_idea = COLDWAR_FRA2_institutional_balance_residual }'))
    complete_path('technical_colleges')
    out.append(assertion('education_reform_keeps_adjustment_costs',
        'NOT = { has_idea = COLDWAR_FRA2_education } has_idea = COLDWAR_FRA2_higher_education_pressures'))
    complete_path('diverse_energy')
    out.append(assertion('funded_energy_choice_partial_relief',
        'NOT = { has_idea = COLDWAR_FRA2_oil } has_idea = COLDWAR_FRA2_oil_dependence_intermediate NOT = { has_idea = COLDWAR_FRA2_oil_dependence_residual }'))
    complete_path('oil_resilience')
    out.append(assertion('oil_resilience_keeps_import_exposure',
        'NOT = { has_idea = COLDWAR_FRA2_oil_dependence_intermediate } has_idea = COLDWAR_FRA2_oil_dependence_residual'))
    # Test a changed two-asset focus from its actual native badge and handler.
    complete_path('progress')
    champion_assets = [e for e in bykey['national_champions']['effects'] if e['kind']=='building']
    for index, asset in enumerate(champion_assets):
        out.append(f'{asset["state"]} = {{ set_variable = {{ ICW_FRA2_invest_{index} = building_level@{asset["building"]} }} }}\n')
    out.append('set_variable = { gdp_total = 1000 }\nset_variable = { treasury = 1000 }\n')
    complete_path('national_champions')
    out.append(assertion('investment_focus_own_gdp_fee',equal('treasury',996)))
    for index, asset in enumerate(champion_assets):
        out.append(f'{asset["state"]} = {{ set_variable = {{ ICW_FRA2_invest_delta_{index} = building_level@{asset["building"]} }} subtract_from_variable = {{ ICW_FRA2_invest_delta_{index} = ICW_FRA2_invest_{index} }}\n')
        out.append(assertion('investment_asset_'+str(index),equal('ICW_FRA2_invest_delta_'+str(index),asset['amount']))+'}\n')
    out.append('COLDWAR_FRA2_complete_national_champions = yes\n')
    out.append(assertion('investment_no_repeat_fee',equal('treasury',996)))
    # Model a saved, already-completed relief route with its former ideas absent.
    out += ['remove_ideas = COLDWAR_FRA2_higher_education_pressures\nremove_ideas = COLDWAR_FRA2_oil_dependence_residual\n',
            'set_variable = { ICW_FRA2_recovery_treasury = treasury }\nclr_country_flag = COLDWAR_FRA2_starting_spirit_revision_20261029_migrated\nCOLDWAR_FRA2_migrate_starting_spirit_revision = yes\n',
            assertion('old_education_completion_gets_residual_once','has_idea = COLDWAR_FRA2_higher_education_pressures'),
            assertion('old_oil_completion_gets_residual_once','has_idea = COLDWAR_FRA2_oil_dependence_residual'),
            assertion('old_final_civic_settlement_stays_resolved','NOT = { has_idea = COLDWAR_FRA2_institutional_balance_residual }'),
            'COLDWAR_FRA2_migrate_starting_spirit_revision = yes\n',
            assertion('recovery_migration_no_fees','check_variable = { var = treasury value = ICW_FRA2_recovery_treasury compare = equals }')]
    out.append(f'log = "{PREFIX} COMPLETE"\n')
    return ''.join(out)


def prepare():
    validation = json.loads((HERE / 'VALIDATION.json').read_text(encoding='utf-8'))
    assert validation['passed'], 'Source validation must pass before native preparation.'
    run = RUNTIME / datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    assert run.resolve().is_relative_to(RUNTIME.resolve())
    run.mkdir(parents=True)
    profile, overlay = run / 'profile', run / 'fixture'
    def write(path, text):
        assert path.absolute().is_relative_to(run.absolute())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    frozen = {}
    for rel in manifest['files']:
        if rel.startswith(('common/', 'events/', 'history/', 'interface/', 'localisation/')):
            source = ROOT / rel
            target = overlay / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
            frozen[rel] = digest(source)
    for rel in ['common/scripted_triggers/01_political_triggers.txt',
                'common/scripted_effects/00_budget_effects.txt',
                'common/scripted_effects/00_internal_faction_effects.txt',
                'common/buildings/00_buildings.txt']:
        target = overlay / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / rel).read_bytes())
        frozen[rel] = digest(ROOT / rel)
    body = fixture(json.loads((HERE / 'runtime_design.json').read_text(encoding='utf-8')))
    write(overlay / 'common/on_actions/zzzz_ICW_FRA2_native.txt', MARK + 'on_actions = { on_startup = { effect = { FRA = { country_event = { id = ICW_FRA2_NATIVE.1 hours = 1 } } } } }\n')
    write(overlay / 'events/zzzz_ICW_FRA2_native.txt', MARK + 'add_namespace = ICW_FRA2_NATIVE\ncountry_event = { id = ICW_FRA2_NATIVE.1 hidden = yes is_triggered_only = yes immediate = {\n' + body + '} }\n')
    base = MARK + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + ROOT.as_posix() + '"\n'
    addon = MARK + 'name="IMPERIA France native fixture"\ndependencies={"MD Cold War"}\npath="' + overlay.as_posix() + '"\n'
    write(profile / 'mod/base.mod', base)
    write(profile / 'mod/fixture.mod', addon)
    write(overlay / 'descriptor.mod', addon)
    write(profile / 'dlc_load.json', json.dumps({'enabled_mods': ['mod/base.mod', 'mod/fixture.mod'], 'disabled_dlcs': []}))
    write(profile / 'settings.txt', 'language="l_english"\ngraphics={size={x=1280 y=720} fullScreen=no borderless=no}\nmaster_volume=0\nsave_as_binary=no\n')
    record = {'project': 'IMPERIA COLD WAR', 'profile': str(profile), 'overlay': str(overlay),
              'frozen_sources': frozen, 'checks': CHECKS,
              'boundary': 'One isolated native process. Target providers frozen; other current mod providers/assets read only, with no asset traversal, copying or junction creation. No human UI, save/reload or multiplayer evidence.',
              'fixture_inputs': 'Artificial GDP and Treasury balances, controlled offer-family reset between cases, internet research for Symphonie and NATO membership for membership cases. The Soviet case first checks the seeded CoCom military restriction blocks the offer, then clears only that bilateral array link inside the test profile for the consent/payment case.'}
    write(run / 'manifest.json', json.dumps(record, indent=2) + '\n')
    (HERE / 'NATIVE_PREPARE.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'run': str(run), 'expected_checks': len(CHECKS)}, indent=2) + '\n', encoding='utf-8')
    return run


def run_probe(run, duration):
    record = json.loads((run / 'manifest.json').read_text(encoding='utf-8'))
    profile = Path(record['profile'])
    existing = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                               'Get-Process -Name hoi4 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'], capture_output=True, text=True)
    assert not existing.stdout.strip(), 'Existing HOI4 process found; leave it untouched.'
    assert all(digest(Path(record['overlay']) / rel) == value for rel, value in record['frozen_sources'].items())
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    args = [str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir=' + str(profile), '-start_tag=FRA', '-start_speed=5', '-hands_off']
    started = time.monotonic()
    process = subprocess.Popen(args, cwd=GAME, startupinfo=startup, creationflags=subprocess.CREATE_NO_WINDOW)
    print(json.dumps({'project': 'IMPERIA COLD WAR', 'pid': process.pid, 'profile': str(profile), 'expected_checks': len(record['checks'])}), flush=True)
    logpath, errorpath = profile / 'logs/game.log', profile / 'logs/error.log'
    status = 'bounded_timeout'
    last = 0
    try:
        while process.poll() is None and time.monotonic() - started < duration:
            time.sleep(1)
            log = logpath.read_text(encoding='utf-8-sig', errors='replace') if logpath.exists() else ''
            if PREFIX + ' COMPLETE' in log:
                status = 'fixture_complete'
                break
            elapsed = int(time.monotonic() - started)
            if elapsed - last >= 30:
                last = elapsed
                print(json.dumps({'phase': 'native', 'elapsed_seconds': elapsed, 'log_exists': logpath.exists()}), flush=True)
        if process.poll() is not None:
            status = 'process_exited'
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    log = logpath.read_text(encoding='utf-8-sig', errors='replace') if logpath.exists() else ''
    error = errorpath.read_text(encoding='utf-8-sig', errors='replace') if errorpath.exists() else ''
    passed = [name for name in record['checks'] if PREFIX + ' PASS ' + name in log]
    failed = [name for name in record['checks'] if PREFIX + ' FAIL ' + name in log]
    missing = [name for name in record['checks'] if name not in passed + failed]
    relevant = [line for line in error.splitlines() if any(key in line for key in ('COLDWAR_FRA2', 'ICW_FRA2_NATIVE', 'zzzz_ICW_FRA2'))]
    result = {'project': 'IMPERIA COLD WAR', 'run': str(run), 'pid': process.pid, 'status': status,
              'elapsed_seconds': round(time.monotonic() - started, 2), 'expected': len(record['checks']),
              'passed': len(passed), 'failed': failed, 'missing': missing,
              'feature_diagnostics': relevant, 'total_error_lines': len(error.splitlines()),
              'frozen_source_drift': [rel for rel, value in record['frozen_sources'].items() if digest(ROOT / rel) != value],
              'boundary': record['boundary']}
    result['native_pass'] = status == 'fixture_complete' and not failed and not missing and not relevant and not result['frozen_source_drift']
    (run / 'NATIVE_RESULT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (HERE / 'NATIVE_RESULT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (HERE / 'NATIVE_CHECKPOINTS.txt').write_text('IMPERIA COLD WAR\n\n' + '\n'.join(line for line in log.splitlines() if PREFIX in line) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('feature_diagnostics', 'failed', 'missing')} |
                     {'failed_count': len(failed), 'first_failures': failed[:15], 'missing_count': len(missing),
                      'feature_diagnostic_lines': len(relevant)}, indent=2), flush=True)
    return not result['native_pass']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--duration', type=int, default=600)
    args = parser.parse_args()
    raise SystemExit(run_probe(prepare(), args.duration))
