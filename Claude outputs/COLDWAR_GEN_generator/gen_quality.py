# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""Transactional two-office projects for the approved focus quality pass.

Each phase delivers one office and its power station in the same eligible state.
The two phases may use the same state. No periodic on_action is installed.
"""
import re

# Net original project invoice as GDP share, including its design's subsidy or
# privatisation proceeds. None preserves the base generic project's $24bn fee.
OFFICE_PROJECTS = {
    'GEN_1970_wa_free_export_zones': (0.027, 'western_autocrats_are_in_power'),
    'GEN_1970_lib_deregulate_the_banks': (0.032, 'western_liberals_are_in_power'),
    'GEN_1970_ce_joint_ventures': (0.027, 'emerging_communist_state_are_in_power'),
    'GEN_1970_ea_the_open_door': (0.032, 'emerging_autocracy_are_in_power'),
    'GEN_1970_mvf_the_merchants_guilds': (0.032, 'emerging_moderate_shiite_are_in_power'),
    'GEN_1970_ncon_a_neutral_banking_centre': (0.032, 'neutrality_neutral_conservatism_are_in_power'),
    'GEN_1970_nlib_free_enterprise_zones': (0.032, 'neutrality_neutral_libertarians_are_in_power'),
    'GEN_1970_nlib_the_free_society': (0.032, 'neutrality_neutral_libertarians_are_in_power'),
    'GEN_1970_jun_privatise_the_state_firms': (0.022, 'nationalist_military_junta_are_in_power'),
    'GEN_1970_mon_indigenise_the_economy': (0.022, 'nationalist_monarchists_are_in_power'),
    'GEN_1970_export_processing_zones': (None, None),
}


def prefix(fid):
    return 'COLDWAR_GEN_Q_' + fid.removeprefix('GEN_1970_')


def runtime_files():
    effects, triggers = ['# Paid office projects: focus/decision callbacks only.'], []
    loc = ['l_english:\n# IMPERIA CW — Cold War: COLDWAR GEN generator English localisation.',
           ' COLDWAR_GEN_Q_office_projects:0 "Commercial Development Projects"',
           ' COLDWAR_GEN_Q_finish_offices:0 "Continue Outstanding Office Projects"',
           ' COLDWAR_GEN_Q_finish_offices_desc:0 "Complete funded phases of approved commercial projects. Each phase delivers one office and one fossil-fuel power plant. Both phases may be built in the same state. Once priced, the project keeps its agreed invoice; only successful phases are paid."',
           ' COLDWAR_GEN_Q_office_ready_tt:0 "An authorised project is ready for pricing or has the required government, funds and construction capacity for a paid phase."',
           ' COLDWAR_GEN_Q_quote_pending_tt:0 "The project is awaiting its initial price. No payment or buildings have been granted."']
    site = '''is_owned_and_controlled_by = ROOT
            free_building_slots = { building = offices size > 0 include_locked = no }
            free_building_slots = { building = fossil_powerplant size > 0 }'''
    for fid, (share, party) in OFFICE_PROJECTS.items():
        p = prefix(fid)
        price = '12' if share is None else '{ value = gdp_total multiply = ' + str(share / 2) + ' max = 0 }'
        condition = f'{party} = yes' if party else 'always = yes'
        triggers.append(f'''
{p}_ready = {{
    has_country_flag = {p}_pending
    check_variable = {{ {p}_delivered < 2 }}
    {condition}
    NOT = {{ has_country_flag = MD_skip_treasury_cost }}
    check_variable = {{ {p}_price > 0 }}
    check_variable = {{ var = treasury value = {p}_price compare = greater_than_or_equals }}
    any_owned_state = {{ {site} }}
}}
''')
        if share is not None:
            triggers.append(f'''
{p}_can_quote = {{
    has_country_flag = {p}_pending
    check_variable = {{ {p}_price = 0 }}
    check_variable = {{ gdp_total > 0 }}
    {condition}
    NOT = {{ has_country_flag = MD_skip_treasury_cost }}
}}
''')
        effects.append(f'''
{p}_open = {{
    custom_effect_tooltip = {p}_terms_tt
    hidden_effect = {{
        if = {{
            limit = {{ NOT = {{ has_country_flag = {p}_started }} }}
            set_country_flag = {p}_started
            set_country_flag = {p}_pending
            set_variable = {{ {p}_delivered = 0 }}
            set_variable = {{ {p}_price = {price} }}
            {p}_finish = yes
        }}
    }}
}}
{p}_phase = {{
    if = {{
        limit = {{ {p}_ready = yes }}
        random_owned_controlled_state = {{
            limit = {{ {site} }}
            add_extra_state_shared_building_slots = 1
            add_building_construction = {{ type = offices level = 1 instant_build = yes }}
            add_building_construction = {{ type = fossil_powerplant level = 1 instant_build = yes }}
            PREV = {{
                set_temp_variable = {{ treasury_change = {{ value = {p}_price multiply = -1 }} }}
                modify_treasury_effect = yes
                add_to_variable = {{ {p}_delivered = 1 }}
            }}
        }}
    }}
}}
{p}_finish = {{
    @PREPARE_QUOTE@
    {p}_phase = yes
    {p}_phase = yes
    if = {{
        limit = {{ check_variable = {{ {p}_delivered > 1 }} }}
        clr_country_flag = {p}_pending
    }}
}}
''')
        effects[-1] = effects[-1].replace('@PREPARE_QUOTE@', '' if share is None else
            f'if = {{ limit = {{ {p}_can_quote = yes }} set_variable = {{ {p}_price = {price} }} }}')
        label = '$12.00 billion' if share is None else f'{share * 50:g}% of GDP'
        loc.append(f' {p}_terms_tt:0 "Authorise §Y2 offices§! and §Y2 fossil-fuel power plants§! in two phases. Each delivered phase costs §Y{label}§!, fixed at authorisation. Both phases may use the same state. Undelivered phases remain under §YCommercial Development Projects§! and cause no charge."')
        loc.append(f' {p}_status_tt:0 "§Y${fid}$§! — completed phases: §Y[?{p}_delivered|0]/2§!; price per remaining phase: §Y$[?{p}_price|2] billion§!."')
    pending = '\n'.join('has_country_flag = ' + prefix(fid) + '_pending' for fid in OFFICE_PROJECTS)
    ready = '\n'.join(prefix(fid) + '_ready = yes' + (f'\n{prefix(fid)}_can_quote = yes' if share is not None else '') for fid,(share,_) in OFFICE_PROJECTS.items())
    finish = '\n'.join(f'if = {{ limit = {{ has_country_flag = {prefix(fid)}_pending }} if = {{ limit = {{ check_variable = {{ {prefix(fid)}_price > 0 }} }} custom_effect_tooltip = {prefix(fid)}_status_tt }} else = {{ custom_effect_tooltip = COLDWAR_GEN_Q_quote_pending_tt }} {prefix(fid)}_finish = yes }}' for fid in OFFICE_PROJECTS)
    categories = f'''
COLDWAR_GEN_Q_office_projects = {{
    icon = GFX_decision_category_generic_economy
    priority = 140
    allowed = {{ always = yes }}
    visible = {{ OR = {{ {pending} }} }}
}}
'''
    decisions = f'''
COLDWAR_GEN_Q_office_projects = {{
    COLDWAR_GEN_Q_finish_offices = {{
        icon = GFX_decision_generic_construction
        cost = 0
        days_re_enable = 7
        visible = {{ OR = {{ {pending} }} }}
        available = {{ custom_trigger_tooltip = {{ tooltip = COLDWAR_GEN_Q_office_ready_tt OR = {{ {ready} }} }} }}
        complete_effect = {{ {finish} }}
        ai_will_do = {{ base = 1 }}
    }}
}}
'''
    return {
        'common/scripted_effects/COLDWAR_GEN_1970_quality.txt': '\n'.join(effects),
        'common/scripted_triggers/COLDWAR_GEN_1970_quality.txt': '\n'.join(triggers),
        'common/decisions/categories/COLDWAR_GEN_1970_quality.txt': categories,
        'common/decisions/COLDWAR_GEN_1970_quality.txt': decisions,
        'localisation/english/COLDWAR_GEN_1970_quality_l_english.yml': '\n'.join(loc) + '\n',
    }


def patch_base_office_focus(text):
    """The legacy base generator is absent; preserve its maintained live block."""
    from gen_common import block_end
    fid = 'GEN_1970_export_processing_zones'
    match = re.search(r'(?m)^\s*id\s*=\s*' + fid + r'\s*$', text)
    assert match, fid
    start = text.rfind('\n\tfocus = {', 0, match.start()) + 1
    end = block_end(text, start) + 1
    body = text[start:end]
    call = prefix(fid) + '_open = yes'
    if 'two_office_construction = yes' in body:
        body = body.replace('two_office_construction = yes', call, 1)
    else:
        assert call in body, fid
    return text[:start] + body + text[end:]
