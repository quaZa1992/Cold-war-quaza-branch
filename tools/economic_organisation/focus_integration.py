# IMPERIA COLD WAR — Generic focus economic organisation progression.
"""Bounded patch of the existing economy branches, without rebuilding the tree."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/focus_quality_20261020'))
from source_edit import end_block, focus_span

MARK = '# IMPERIA COLD WAR — Generic focus economic organisation progression.'
TREE = 'common/national_focus/mdcw_1970_generic_focus.txt'
EFFECTS = 'common/scripted_effects/ICW_generic_economic_paths.txt'
LOCALISATION = 'localisation/english/ICW_generic_economic_paths_l_english.yml'
STEPS = {
    'market_liberalisation': 10,
    'attract_foreign_investors': 5,
    'open_the_stock_exchange': 10,
    'simplify_the_tax_code': 5,
    'export_processing_zones': 10,
    'economic_miracle': 10,
    'the_mixed_economy': 'mixed',
    'indicative_planning': 'mixed',
    'national_champions': 'mixed',
    'social_partnership': 'mixed',
    'pension_fund_investments': 'mixed',
    'planned_prosperity': 'mixed',
    'central_planning': -10,
    'nationalise_key_industries': -15,
    'state_planning_committee': -10,
    'collectivise_agriculture': -10,
    'socialist_industrialisation': -15,
}


def effect_name(slug):
    return 'icw_gen_econ_focus_' + slug


def patch_generic_tree(source):
    for slug in STEPS:
        start, end = focus_span(source, 'GEN_1970_' + slug)
        focus = source[start:end]
        name = effect_name(slug)
        if re.search(r'\b' + name + r'\s*=\s*yes', focus):
            continue
        match = re.search(r'\bcompletion_reward\s*=\s*\{', focus)
        assert match, slug
        opening = focus.index('{', match.start())
        closing = end_block(focus, opening) - 1
        insert = '\n\t\t\t' + name + ' = yes\n\t\t'
        focus = focus[:closing].rstrip() + insert + focus[closing:]
        source = source[:start] + focus + source[end:]
    if not source.startswith(MARK + '\n'):
        source = MARK + '\n' + source
    return source


def runtime_files():
    shared = '''icw_gen_econ_apply_shift = {
    hidden_effect = {
        set_temp_variable = { icw_gen_econ_delta = { value = icw_econ_position add = icw_gen_econ_delta clamp = { min = -100 max = 100 } subtract = icw_econ_position } }
        if = {
            limit = { has_country_flag = icw_econ_reform_active }
            set_temp_variable = { icw_gen_econ_old_sale_points = { value = icw_econ_pending_position subtract = icw_econ_market_high_water clamp = { min = 0 max = 10 } } }
        }
    }
    add_to_variable = { icw_econ_position = icw_gen_econ_delta tooltip = icw_gen_econ_position_shift_tt }
    hidden_effect = {
        if = {
            limit = { check_variable = { icw_econ_position > icw_econ_market_high_water } }
            set_variable = { icw_econ_market_high_water = icw_econ_position }
        }
        if = {
            limit = { has_country_flag = icw_econ_reform_active }
            add_to_variable = { icw_econ_pending_position = icw_gen_econ_delta }
            clamp_variable = { var = icw_econ_pending_position min = -100 max = 100 }
            if = {
                limit = { check_variable = { icw_econ_pending_sale > 0 } }
                if = {
                    limit = { check_variable = { icw_gen_econ_old_sale_points > 0 } }
                    set_temp_variable = { icw_gen_econ_sale_ratio = { value = icw_econ_pending_position subtract = icw_econ_market_high_water clamp = { min = 0 max = icw_gen_econ_old_sale_points } } }
                    divide_temp_variable = { icw_gen_econ_sale_ratio = icw_gen_econ_old_sale_points }
                    multiply_temp_variable = { icw_gen_econ_sale_ratio = icw_econ_pending_sale }
                    set_variable = { icw_econ_pending_sale = icw_gen_econ_sale_ratio }
                }
                else = { clear_variable = icw_econ_pending_sale }
            }
        }
        if = {
            limit = { has_country_flag = icw_econ_approval_pending NOT = { icw_econ_request_valid = yes } }
            icw_econ_clear_request = yes
        }
        icw_econ_refresh_tier = yes
        set_variable = { globalism_value_eq = modifier@globalism_equilibrium }
        clamp_variable = { var = globalism_value_eq min = 0 max = 100 }
        if = { limit = { has_dynamic_modifier = { modifier = imp_globalism_modifier } } imp_eco_globalism_modifier = yes }
        if = { limit = { IMP_is_1970_scenario = yes } mdcw_cw_update_world_market = yes }
        ingame_update_setup = yes
    }
}
'''
    effects = [MARK, shared]
    for slug, step in STEPS.items():
        delta = '{ value = icw_econ_position multiply = -1 clamp = { min = -20 max = 20 } }' if step == 'mixed' else str(step)
        effects.append(f'''{effect_name(slug)} = {{
    if = {{
        limit = {{ hidden_trigger = {{ NOT = {{ has_country_flag = icw_gen_econ_done_{slug} }} }} }}
        hidden_effect = {{
            icw_econ_initialize = yes
            set_temp_variable = {{ icw_gen_econ_delta = {delta} }}
        }}
        icw_gen_econ_apply_shift = yes
        hidden_effect = {{ set_country_flag = icw_gen_econ_done_{slug} }}
    }}
}}''')
    loc = 'l_english:\n' + MARK + '\n icw_gen_econ_position_shift_tt: "Economic Organisation: §Y$RIGHT|=0$§!"\n'
    return {EFFECTS: '\n'.join(effects) + '\n', LOCALISATION: loc}


def main():
    path = ROOT / TREE
    source = path.read_bytes().decode('utf-8-sig')
    patched = patch_generic_tree(source)
    assert patch_generic_tree(patched) == patched
    path.write_bytes(patched.encode('utf-8'))
    for rel, text in runtime_files().items():
        (ROOT / rel).write_bytes(text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8'))
    print('IMPERIA COLD WAR: integrated economic organisation steps into 17 existing generic focuses.')


if __name__ == '__main__':
    main()
