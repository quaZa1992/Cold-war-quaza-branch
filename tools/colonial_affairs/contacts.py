# IMPERIA CW — Cold War: regional intelligence contacts, domestic organisations and disclosure.
"""Shared foreign contacts; domestic threats never create a military occupation."""
from runtime import HEADER, block, iff

GROUPS = {
    'ira': dict(name='Irish Republican Army', states=[17], power='ENG', start='1969.12.1', threat=35, floor=25),
    'raf': dict(name='Red Army Faction', states=[41, 42, 1080, 1251], power='GER', start='1970.5.13', external=True),
}
MOVEMENTS = {
    'eng_belize': ('People\'s United Party', 'pup'),
    'eng_pacific_south': ('Territorial self-government movement', 'solomon'),
    'fra_comoros': ('Comorian independence organisations', 'comoros'),
    'fra_french_somaliland': ('African independence organisations', 'djibouti'),
    'por_angola': ('MPLA / FNLA / UNITA', 'angola'),
    'por_mozambique': ('FRELIMO', 'frelimo'),
    'por_guinea_bissau': ('PAIGC', 'paigc'),
    'saf_namibia': ('SWAPO', 'swapo'),
    'spr_western_sahara': ('Saharan independence movement', 'sahara'),
}


def append_file(files, path, text):
    files[path] = files.get(path, HEADER) + '\n' + text


def build(files, rows):
    triggers, effects, local = [], [], {}
    trig = lambda name, body: triggers.append(block(name, body))
    effect = lambda name, body: effects.append(block(name, body))
    trig('COLDWAR_COL_contacts_scenario', 'OR = { IMP_is_1970_scenario = yes IMP_is_1985_scenario = yes }')
    trig('COLDWAR_COL_has_regional_network', '''has_intelligence_agency = yes
network_strength = { state = var:COLDWAR_COL_support_target value > 50 }''')
    registered = []
    for row in rows:
        if row.get('support_allowed') and row.get('native_tag') and row['profile'] in ('contested', 'war'):
            registered.append('AND = { OR = { '+' '.join(f'state = {s}' for s in row['states'])+f' }} COLDWAR_COL_active_state = yes {row["states"][0]} = {{ has_state_flag = COLDWAR_COL_organised_movement }} }}')
    for rid, (name, icon) in MOVEMENTS.items():
        local['COLDWAR_COL_movement_' + icon] = name
    trig('COLDWAR_COL_registered_contact', block('OR', '\n'.join(registered)))
    for group, data in GROUPS.items():
        power = data['power']
        native_gate='\nGER = { has_country_flag = COLDWAR_GER_1970_initialized NOT = { has_country_flag = COLDWAR_GER_1970_raf_dissolved } check_variable = { cwger_raf_gen < 4 } }' if data.get('external') else ''
        trig(f'COLDWAR_COL_group_{group}', f'''COLDWAR_COL_contacts_scenario = yes
date > {data['start']}
{power} = {{ exists = yes NOT = {{ has_country_flag = COLDWAR_COL_{group}_settlement }} }}
OR = {{ {' '.join('state = '+str(s) for s in data['states'])} }}
is_owned_by = {power}
is_controlled_by = {power}{native_gate}''')
        local[f'COLDWAR_COL_movement_{group}'] = data['name']
    trig('COLDWAR_COL_domestic_contact', 'OR = { COLDWAR_COL_group_ira = yes COLDWAR_COL_group_raf = yes }')
    trig('COLDWAR_COL_ira_active', '17 = { COLDWAR_COL_group_ira = yes }')
    trig('COLDWAR_COL_occupation_contact', '''has_resistance = yes
NOT = { is_core_of = controller }
NOT = { COLDWAR_COL_registered_contact = yes }
NOT = { COLDWAR_COL_domestic_contact = yes }''')
    trig('COLDWAR_COL_contact_state', '''COLDWAR_COL_contacts_scenario = yes
OR = { COLDWAR_COL_registered_contact = yes COLDWAR_COL_domestic_contact = yes COLDWAR_COL_occupation_contact = yes }''')
    # State context, ROOT is always the viewing/paying country.
    trig('COLDWAR_COL_foreign_contact_visible', '''COLDWAR_COL_contact_state = yes
controller = { NOT = { tag = ROOT } NOT = { is_subject_of = ROOT } }
controller = { ROOT = { NOT = { is_subject_of = PREV } } }
ROOT = {
    is_ai = no
    has_intelligence_agency = yes
    network_strength = { state = PREV value > 50 }
}''')
    trig('COLDWAR_COL_contact_target_available', '''COLDWAR_COL_contacts_scenario = yes
has_variable = COLDWAR_COL_support_target
var:COLDWAR_COL_support_target = { COLDWAR_COL_foreign_contact_visible = yes }
COLDWAR_COL_has_regional_network = yes''')
    trig('COLDWAR_COL_local_target_available', '''COLDWAR_COL_contact_target_available = yes
var:COLDWAR_COL_support_target = { NOT = { COLDWAR_COL_registered_contact = yes } }''')
    trig('COLDWAR_COL_case_target_available', '''has_variable = COLDWAR_COL_case_target
var:COLDWAR_COL_case_target = { COLDWAR_COL_group_ira = yes is_controlled_by = PREV }''')
    trig('COLDWAR_COL_can_change_case', '''COLDWAR_COL_case_target_available = yes
NOT = { political_power < 25 }
var:COLDWAR_COL_case_target = { check_variable = { COLDWAR_COL_case_lock < 1 } }''')
    for policy in range(3):
        trig(f'COLDWAR_COL_can_change_case_{policy}',f'COLDWAR_COL_can_change_case = yes\nvar:COLDWAR_COL_case_target = {{ NOT = {{ check_variable = {{ COLDWAR_COL_case_policy = {policy} }} }} }}')
        effect(f'COLDWAR_COL_adopt_case_{policy}', iff(f'COLDWAR_COL_can_change_case_{policy} = yes', f'add_political_power = -25\nvar:COLDWAR_COL_case_target = {{ set_variable = {{ COLDWAR_COL_case_policy = {policy} }} set_variable = {{ COLDWAR_COL_case_lock = 180 }} COLDWAR_COL_apply_domestic = yes }}\nCOLDWAR_COL_refresh_case = yes'))
    case_view=''
    for group, data in GROUPS.items():
        if data.get('external'):continue
        for state in data['states']:
            case_view+=iff(f'COLDWAR_COL_case_target_available = no\n{state} = {{ COLDWAR_COL_group_{group} = yes is_controlled_by = PREV }}',f'set_variable = {{ COLDWAR_COL_case_target = {state} }}')
    case_view+=iff('COLDWAR_COL_case_target_available = yes', '''var:COLDWAR_COL_case_target = {
 set_variable = { PREV.COLDWAR_COL_case_strength = COLDWAR_COL_cells }
 set_variable = { PREV.COLDWAR_COL_case_aid = COLDWAR_COL_local_aid }
 set_variable = { PREV.COLDWAR_COL_case_days = COLDWAR_COL_case_lock }
 set_variable = { PREV.COLDWAR_COL_case_policy = COLDWAR_COL_case_policy }
 if = { limit = { check_variable = { COLDWAR_COL_case_policy = 0 } } set_variable = { PREV.COLDWAR_COL_case_cost = 0.005 } }
 if = { limit = { check_variable = { COLDWAR_COL_case_policy = 1 } } set_variable = { PREV.COLDWAR_COL_case_cost = 0.012 } }
 if = { limit = { check_variable = { COLDWAR_COL_case_policy = 2 } } set_variable = { PREV.COLDWAR_COL_case_cost = 0.02 } }
}''')
    effect('COLDWAR_COL_refresh_case',case_view)
    effect('COLDWAR_COL_refresh_local_aid', '''set_variable = { COLDWAR_COL_local_aid = 0 }
set_temp_variable = { COLDWAR_COL_counted_state = THIS.id }
every_country = {
    limit = { OR = { has_country_flag = COLDWAR_COL_local_funding_live has_country_flag = COLDWAR_COL_local_arms_live } }
    if = {
        limit = { has_country_flag = COLDWAR_COL_local_funding_live check_variable = { COLDWAR_COL_local_funding_state = PREV.id } }
        if = { limit = { PREV = { is_controlled_by = var:PREV.COLDWAR_COL_local_funding_power COLDWAR_COL_contact_state = yes NOT = { COLDWAR_COL_registered_contact = yes } } } PREV = { add_to_variable = { COLDWAR_COL_local_aid = 5 } } }
        else = { clr_country_flag = COLDWAR_COL_local_funding_live }
    }
    if = {
        limit = { has_country_flag = COLDWAR_COL_local_arms_live check_variable = { COLDWAR_COL_local_arms_state = PREV.id } }
        if = { limit = { PREV = { is_controlled_by = var:PREV.COLDWAR_COL_local_arms_power COLDWAR_COL_contact_state = yes NOT = { COLDWAR_COL_registered_contact = yes } } } PREV = { add_to_variable = { COLDWAR_COL_local_aid = 5 } } }
        else = { clr_country_flag = COLDWAR_COL_local_arms_live }
    }
}
clamp_variable = { var = COLDWAR_COL_local_aid min = 0 max = 15 }
remove_resistance_target = 19709990
if = {
    limit = { COLDWAR_COL_occupation_contact = yes check_variable = { COLDWAR_COL_local_aid > 0 } }
    add_resistance_target = { id = 19709990 amount = COLDWAR_COL_local_aid days = 2 tooltip = COLDWAR_COL_foreign_target_tt }
}''')
    # The existing German security module is the sole RAF simulation. This
    # bridge sums regional contacts into one bounded native organisation supply.
    raf_sum='set_variable = { COLDWAR_COL_raf_aid = 0 }\n'
    for state in GROUPS['raf']['states']:
        raf_sum+=block(str(state),'COLDWAR_COL_refresh_local_aid = yes')
        raf_sum+=f'add_to_variable = {{ COLDWAR_COL_raf_aid = {state}.COLDWAR_COL_local_aid }}\n'
    effect('COLDWAR_COL_refresh_raf_aid',raf_sum+'clamp_variable = { var = COLDWAR_COL_raf_aid min = 0 max = 15 }')
    # Disclosure uses event-local targets. Parallel donor/region stories do not
    # share a mutable global news identity, nor is every shipment automatically public.
    for package, risk in [('political', 10), ('funding', 25), ('arms', 40)]:
        effect(f'COLDWAR_COL_disclose_{package}', f'''random_list = {{
    {100-risk} = {{ }}
    {risk} = {{
        save_event_target_as = COLDWAR_COL_exposed_sponsor
        var:COLDWAR_COL_support_target = {{
            save_event_target_as = COLDWAR_COL_exposed_region
            controller = {{ country_event = {{ id = COLDWAR_colonial_contacts.1 }} }}
        }}
    }}
}}''')
        gate = f'''COLDWAR_COL_local_target_available = yes
NOT = {{ has_country_flag = COLDWAR_COL_local_{package}_cooldown }}'''
        if package in ('political', 'arms'):
            gate += '\nNOT = { political_power < 15 }'
        if package == 'funding':
            gate += '\nNOT = { has_country_flag = MD_skip_treasury_cost }\ncheck_variable = { var = treasury value = 0.05 compare = greater_than_or_equals }'
        if package in ('funding', 'arms'):
            gate += '\nOR = { AND = { var:COLDWAR_COL_support_target = { COLDWAR_COL_group_raf = yes } GER = { check_variable = { COLDWAR_COL_raf_aid < 15 } } } AND = { var:COLDWAR_COL_support_target = { NOT = { COLDWAR_COL_group_raf = yes } check_variable = { COLDWAR_COL_local_aid < 15 } } } }'
        if package == 'arms':
            gate += '\nhas_equipment = { infantry_weapons_type > 249 }\nhas_equipment = { cnc_equipment_type > 24 }'
        if package == 'political':
            # Do not charge for political backing that would hit a ceiling.
            gate += '\nvar:COLDWAR_COL_support_target = { OR = { AND = { COLDWAR_COL_group_raf = yes GER = { check_variable = { cwger_raf_milieu < 99 } } } AND = { COLDWAR_COL_group_ira = yes check_variable = { COLDWAR_COL_cells < 86 } } AND = { COLDWAR_COL_occupation_contact = yes compliance > 2 } } }'
        trig(f'COLDWAR_COL_can_local_{package}', gate)
        pay = 'add_political_power = -15\n' if package in ('political', 'arms') else 'set_temp_variable = { treasury_change = -0.05 }\nmodify_treasury_effect = yes\n'
        if package == 'arms':
            pay += 'add_equipment_to_stockpile = { type = infantry_weapons_type amount = -250 }\nadd_equipment_to_stockpile = { type = cnc_equipment_type amount = -25 }\n'
        pay += f'set_country_flag = {{ flag = COLDWAR_COL_local_{package}_cooldown days = 180 }}\n'
        if package in ('funding', 'arms'):
            pay += f'set_country_flag = {{ flag = COLDWAR_COL_local_{package}_live days = 180 }}\nset_variable = {{ COLDWAR_COL_local_{package}_state = COLDWAR_COL_support_target }}\n'
            pay += f'var:COLDWAR_COL_support_target = {{ controller = {{ set_variable = {{ ROOT.COLDWAR_COL_local_{package}_power = THIS }} }} }}\n'
        result = ''
        if package == 'political':
            result = iff('COLDWAR_COL_group_raf = yes','GER = { add_to_variable = { cwger_raf_milieu = 2 } clamp_variable = { var = cwger_raf_milieu min = 0 max = 100 } }',iff('COLDWAR_COL_group_ira = yes', 'add_to_variable = { COLDWAR_COL_cells = 5 }', 'add_compliance = -3'))
        if package == 'arms':
            result = iff('COLDWAR_COL_group_raf = yes','GER = { add_to_variable = { cwger_raf_cadre = 1 } clamp_variable = { var = cwger_raf_cadre min = 0 max = 120 } }',iff('COLDWAR_COL_group_ira = yes', 'add_to_variable = { COLDWAR_COL_cells = 3 }', 'add_resistance = 5'))
        pay += block('var:COLDWAR_COL_support_target', result + '\nCOLDWAR_COL_refresh_local_aid = yes')
        pay += iff('var:COLDWAR_COL_support_target = { COLDWAR_COL_group_raf = yes }','GER = { COLDWAR_COL_refresh_raf_aid = yes }')
        pay += f'COLDWAR_COL_disclose_{package} = yes\nCOLDWAR_COL_refresh_support_target = yes\n'
        effect(f'COLDWAR_COL_send_local_{package}', iff('has_variable = COLDWAR_COL_support_target', 'var:COLDWAR_COL_support_target = { COLDWAR_COL_refresh_local_aid = yes }\n'+iff('var:COLDWAR_COL_support_target = { COLDWAR_COL_group_raf = yes }','GER = { COLDWAR_COL_refresh_raf_aid = yes }')) + iff(f'COLDWAR_COL_can_local_{package} = yes', pay))

    # Every domestic organisation gets its own regional record and icon, while
    # using the same donor transaction and disclosure system as an occupation.
    initialise, initialise_only, monthly, budget = '', '', '', ''
    for group, data in GROUPS.items():
        if data.get('external'):continue
        power, anchor = data['power'], data['states'][0]
        for state in data['states']:
            init = f'''set_state_flag = COLDWAR_COL_{group}_initialized
set_variable = {{ COLDWAR_COL_cells = {data['threat']} }}
set_variable = {{ COLDWAR_COL_case_policy = 0 }}'''
            step = f'''COLDWAR_COL_refresh_local_aid = yes
set_temp_variable = {{ COLDWAR_COL_case_drift = 1 }}
if = {{ limit = {{ check_variable = {{ COLDWAR_COL_case_policy = 1 }} }} set_temp_variable = {{ COLDWAR_COL_case_drift = -0.5 }} }}
if = {{ limit = {{ check_variable = {{ COLDWAR_COL_case_policy = 2 }} }} set_temp_variable = {{ COLDWAR_COL_case_drift = -1 }} }}
add_to_variable = {{ COLDWAR_COL_cells = COLDWAR_COL_case_drift }}
set_temp_variable = {{ COLDWAR_COL_aid_drift = COLDWAR_COL_local_aid }}
multiply_temp_variable = {{ COLDWAR_COL_aid_drift = 0.1 }}
add_to_variable = {{ COLDWAR_COL_cells = COLDWAR_COL_aid_drift }}
clamp_variable = {{ var = COLDWAR_COL_cells min = {data['floor']} max = 90 }}
COLDWAR_COL_apply_domestic = yes
if = {{ limit = {{ check_variable = {{ COLDWAR_COL_cells > 44 }} controller = {{ NOT = {{ has_country_flag = COLDWAR_COL_incident_recent }} }} }} random_list = {{ 85 = {{ }} 15 = {{ controller = {{ set_country_flag = {{ flag = COLDWAR_COL_incident_recent days = 90 }} country_event = {{ id = COLDWAR_colonial_contacts.3 }} }} }} }} }}'''
            initialise += block(str(state), iff(f'is_controlled_by = PREV', iff(f'COLDWAR_COL_group_{group} = yes', iff(f'NOT = {{ has_state_flag = COLDWAR_COL_{group}_initialized }}', init) + iff('check_variable = { COLDWAR_COL_case_lock > 0 }', 'subtract_from_variable = { COLDWAR_COL_case_lock = 1 }') + 'COLDWAR_COL_apply_domestic = yes', 'remove_dynamic_modifier = { modifier = COLDWAR_COL_domestic_security }')))
            initialise_only += block(str(state), iff(f'is_controlled_by = PREV\nCOLDWAR_COL_group_{group} = yes', iff(f'NOT = {{ has_state_flag = COLDWAR_COL_{group}_initialized }}', init) + 'COLDWAR_COL_apply_domestic = yes'))
            monthly += block(str(state), iff(f'COLDWAR_COL_group_{group} = yes\nis_controlled_by = PREV', step))
            for policy, cost in [(0, .005), (1, .012), (2, .02)]:
                budget += iff(f'{state} = {{ COLDWAR_COL_group_{group} = yes is_controlled_by = PREV check_variable = {{ COLDWAR_COL_case_policy = {policy} }} }}', f'add_to_variable = {{ COLDWAR_COL_domestic_weekly_cost = {cost} }}')
    effect('COLDWAR_COL_apply_domestic', '''set_variable = { COLDWAR_COL_domestic_construction = COLDWAR_COL_cells }
multiply_variable = { COLDWAR_COL_domestic_construction = -0.001 }
set_variable = { COLDWAR_COL_domestic_resources = COLDWAR_COL_cells }
multiply_variable = { COLDWAR_COL_domestic_resources = -0.0005 }
set_variable = { COLDWAR_COL_domestic_workforce = COLDWAR_COL_cells }
multiply_variable = { COLDWAR_COL_domestic_workforce = -0.0005 }
if = { limit = { check_variable = { COLDWAR_COL_case_policy = 2 } } add_to_variable = { COLDWAR_COL_domestic_construction = -0.05 } add_to_variable = { COLDWAR_COL_domestic_workforce = -0.02 } }
if = { limit = { NOT = { has_dynamic_modifier = { modifier = COLDWAR_COL_domestic_security } } } add_dynamic_modifier = { modifier = COLDWAR_COL_domestic_security } }''')
    migration = iff('tag = ENG', 'remove_ideas = ENG_ulster_flashpoint\n' + iff('has_country_flag = ENG_1985_ira_state_initialised', '17 = { force_disable_resistance = { clear = yes occupier = ENG } remove_dynamic_modifier = { modifier = ENG_ira_troubles_state_modifier } remove_dynamic_modifier = { modifier = ENG_ira_static_modifier } }\nclr_country_flag = ENG_1985_ira_state_initialised'))
    effect('COLDWAR_COL_contacts_initialize',iff('COLDWAR_COL_contacts_scenario = yes',migration + initialise_only + '\nCOLDWAR_COL_refresh_case = yes'))
    effect('COLDWAR_COL_contacts_daily', iff('COLDWAR_COL_contacts_scenario = yes', migration + initialise + '\n' + '\n'.join(iff(f'has_variable = COLDWAR_COL_local_{p}_state', f'var:COLDWAR_COL_local_{p}_state = {{ COLDWAR_COL_refresh_local_aid = yes }}\n' + iff(f'NOT = {{ has_country_flag = COLDWAR_COL_local_{p}_live }}', f'clear_variable = COLDWAR_COL_local_{p}_state')) for p in ('funding', 'arms')) + '\n' + iff('has_variable = COLDWAR_COL_support_target\nCOLDWAR_COL_contact_target_available = no', 'clr_country_flag = COLDWAR_COL_support_panel_open') + '\nCOLDWAR_COL_refresh_support_target = yes\nCOLDWAR_COL_refresh_case = yes'))
    monthly+=iff('tag = GER\nhas_country_flag = COLDWAR_GER_1970_initialized\nOR = { '+' '.join(f'{s} = {{ COLDWAR_COL_group_raf = yes }}' for s in GROUPS['raf']['states'])+' }', '''COLDWAR_COL_refresh_raf_aid = yes
set_temp_variable = { COLDWAR_COL_raf_reinforcement = COLDWAR_COL_raf_aid }
multiply_temp_variable = { COLDWAR_COL_raf_reinforcement = 0.05 }
add_to_variable = { cwger_raf_cadre = COLDWAR_COL_raf_reinforcement }
clamp_variable = { var = cwger_raf_cadre min = 0 max = 120 }''')
    effect('COLDWAR_COL_contacts_monthly', iff('COLDWAR_COL_contacts_scenario = yes', monthly))
    effect('COLDWAR_COL_domestic_budget', 'set_variable = { COLDWAR_COL_domestic_weekly_cost = 0 }\n' + iff('COLDWAR_COL_contacts_scenario = yes', budget))
    # Selected state data is copied only while that viewer still has access.
    refresh = '''set_variable = { COLDWAR_COL_support_group = 0 }
if = {
    limit = { COLDWAR_COL_contact_target_available = yes }
    var:COLDWAR_COL_support_target = {
        set_variable = { ROOT.COLDWAR_COL_support_resistance = THIS.resistance }
        if = { limit = { COLDWAR_COL_occupation_contact = yes } set_variable = { ROOT.COLDWAR_COL_support_bonus = COLDWAR_COL_local_aid } }
        if = { limit = { COLDWAR_COL_domestic_contact = yes } set_variable = { ROOT.COLDWAR_COL_support_resistance = COLDWAR_COL_cells } set_variable = { ROOT.COLDWAR_COL_support_bonus = COLDWAR_COL_local_aid } }
    }
}'''
    for index, (group, data) in enumerate(GROUPS.items(), 101):
        refresh += iff(f'var:COLDWAR_COL_support_target = {{ COLDWAR_COL_group_{group} = yes }}\nCOLDWAR_COL_contact_target_available = yes', f'set_variable = {{ COLDWAR_COL_support_group = {index} }}')
    refresh+=iff('var:COLDWAR_COL_support_target = { COLDWAR_COL_group_raf = yes }\nCOLDWAR_COL_contact_target_available = yes','GER = { COLDWAR_COL_refresh_raf_aid = yes }\nset_variable = { COLDWAR_COL_support_resistance = GER.cwger_raf_cadre }\nset_variable = { COLDWAR_COL_support_bonus = GER.COLDWAR_COL_raf_aid }\nset_variable = { COLDWAR_COL_raf_milieu_view = GER.cwger_raf_milieu }')
    effect('COLDWAR_COL_refresh_contacts_view', iff('has_variable = COLDWAR_COL_support_target', refresh))

    decisions = block('COLDWAR_COL_select_contact', '''icon = generic_political_discourse
state_target = yes
cost = 0
visible = { COLDWAR_COL_contacts_scenario = yes }
target_trigger = { FROM = { COLDWAR_COL_foreign_contact_visible = yes } }
available = { FROM = { COLDWAR_COL_foreign_contact_visible = yes } }
complete_effect = { if = { limit = { FROM = { COLDWAR_COL_foreign_contact_visible = yes } } set_variable = { COLDWAR_COL_support_target = FROM.id } COLDWAR_COL_refresh_support_target = yes set_country_flag = COLDWAR_COL_support_panel_open } }
ai_will_do = { factor = 0 }''')
    decisions += block('COLDWAR_COL_select_case', '''icon = generic_political_discourse
state_target = yes
cost = 0
visible = { COLDWAR_COL_contacts_scenario = yes }
target_trigger = { FROM = { COLDWAR_COL_group_ira = yes is_controlled_by = ROOT } }
complete_effect = { if = { limit = { FROM = { COLDWAR_COL_group_ira = yes is_controlled_by = ROOT } } set_variable = { COLDWAR_COL_case_target = FROM.id } COLDWAR_COL_refresh_case = yes } }
ai_will_do = { factor = 0 }''')
    # Domestic countermeasures are new, share the regional file, and have real
    # recurring appropriations. They do not invoke any retired IRA slider.
    for policy, name in [(0, 'Routine policing'), (1, 'Community liaison'), (2, 'Intensive investigation')]:
        decisions += block(f'COLDWAR_COL_case_policy_{policy}', f'''icon = generic_political_discourse
state_target = yes
cost = 0
visible = {{ COLDWAR_COL_contacts_scenario = yes }}
target_trigger = {{ FROM = {{ COLDWAR_COL_domestic_contact = yes is_controlled_by = ROOT }} }}
available = {{ NOT = {{ political_power < 25 }} FROM = {{ check_variable = {{ COLDWAR_COL_case_lock < 1 }} }} }}
complete_effect = {{ if = {{ limit = {{ NOT = {{ political_power < 25 }} FROM = {{ COLDWAR_COL_domestic_contact = yes is_controlled_by = ROOT check_variable = {{ COLDWAR_COL_case_lock < 1 }} }} }} add_political_power = -25 FROM = {{ set_variable = {{ COLDWAR_COL_case_policy = {policy} }} set_variable = {{ COLDWAR_COL_case_lock = 180 }} }} }} }}
ai_will_do = {{ factor = 0 }}''')
        local[f'COLDWAR_COL_case_policy_{policy}'] = name + ': [FROM.GetName]'
        local[f'COLDWAR_COL_case_policy_{policy}_desc'] = ['Standing policing: $0.005bn/week; organisation strength +1/month. Costs 25 Political Power; 180-day commitment.', 'Community liaison: $0.012bn/week; organisation strength −0.5/month. Costs 25 Political Power; 180-day commitment.', 'Intensive investigation: $0.020bn/week; organisation strength −1/month. Additional local construction −5% and workforce −2% from security restrictions. Costs 25 Political Power; 180-day commitment.'][policy] + ' Foreign support can offset progress. These are regional security cases, not military occupations.'
    foreign_decision = decisions[:decisions.index('COLDWAR_COL_select_case')]
    domestic_decisions = decisions[decisions.index('COLDWAR_COL_select_case'):decisions.index('COLDWAR_COL_case_policy_0')]
    append_file(files, 'common/decisions/COLDWAR_colonial_contacts.txt', block('COLDWAR_COL_contacts_category', foreign_decision) + block('COLDWAR_COL_domestic_category', domestic_decisions))
    append_file(files, 'common/decisions/categories/COLDWAR_colonial_contacts.txt', block('COLDWAR_COL_contacts_category', '''icon = generic_political_discourse
scripted_gui = COLDWAR_COL_contacts_gui
visible_when_empty = yes
visible = { is_ai = no COLDWAR_COL_contacts_scenario = yes any_state = { COLDWAR_COL_foreign_contact_visible = yes } }''') + block('COLDWAR_COL_domestic_category', '''icon = generic_political_discourse
scripted_gui = COLDWAR_COL_domestic_gui
visible_when_empty = yes
visible = { is_ai = no COLDWAR_COL_contacts_scenario = yes any_controlled_state = { COLDWAR_COL_group_ira = yes } }'''))
    append_file(files, 'common/dynamic_modifiers/COLDWAR_colonial_contacts.txt', block('COLDWAR_COL_domestic_security', '''enable = { COLDWAR_COL_group_ira = yes }
state_production_speed_buildings_factor = COLDWAR_COL_domestic_construction
state_resources_factor = COLDWAR_COL_domestic_resources
local_manpower = COLDWAR_COL_domestic_workforce'''))
    # Disabled legacy definitions exist solely so old-save modifier removal has
    # valid native identifiers. They carry no old effects or active interface.
    for name in ('ENG_ira_troubles_state_modifier','ENG_ira_static_modifier'):
        append_file(files,'common/dynamic_modifiers/COLDWAR_colonial_contacts.txt',block(name,'enable = { always = no }'))
    append_file(files, 'common/on_actions/COLDWAR_colonial_contacts.txt', block('on_actions', block('on_startup', block('effect','every_country = { limit = { COLDWAR_COL_contacts_scenario = yes } COLDWAR_COL_contacts_initialize = yes }')) + block('on_daily', block('effect', 'COLDWAR_COL_contacts_daily = yes')) + block('on_monthly', block('effect', 'COLDWAR_COL_contacts_monthly = yes'))))
    append_file(files, 'events/COLDWAR_colonial_contacts.txt', '''namespace = COLDWAR_colonial_contacts
country_event = {
 id = COLDWAR_colonial_contacts.1
 title = COLDWAR_COL_leak_title
 desc = COLDWAR_COL_leak_desc
 is_triggered_only = yes
 immediate = {
  event_target:COLDWAR_COL_exposed_sponsor = { add_stability = -0.01 }
  add_opinion_modifier = { target = event_target:COLDWAR_COL_exposed_sponsor modifier = COLDWAR_COL_foreign_assistance }
  news_event = { id = COLDWAR_colonial_contacts.2 }
 }
 option = { name = COLDWAR_COL_leak_response add_political_power = 15 }
}
news_event = {
 id = COLDWAR_colonial_contacts.2
 title = COLDWAR_COL_leak_news_title
 desc = COLDWAR_COL_leak_news_desc
 major = yes
 is_triggered_only = yes
 option = { name = COLDWAR_COL_leak_news_response }
}
country_event = {
 id = COLDWAR_colonial_contacts.3
 title = COLDWAR_COL_incident_title
 desc = COLDWAR_COL_incident_desc
 is_triggered_only = yes
 option = { name = COLDWAR_COL_incident_response add_stability = -0.005 add_political_power = -10 }
}
''')
    local.update({
        'COLDWAR_COL_contacts_category': 'Resistance Contacts',
        'COLDWAR_COL_contacts_category_desc': 'Regional files require an intelligence agency and an intelligence network above 50% in the selected state. Losing access closes the file and blocks further assistance. Existing deliveries run for their remaining term.',
        'COLDWAR_COL_domestic_category': 'Internal Security Cases',
        'COLDWAR_COL_domestic_category_desc': 'Review regional investigations, community liaison and standing police appropriations. Underground organisations do not create a military occupation.',
        'COLDWAR_COL_select_contact': 'Regional file: [FROM.GetName]',
        'COLDWAR_COL_select_contact_desc': 'Open the regional organisation file. Requires an intelligence network above 50% in this state.',
        'COLDWAR_COL_domestic_security': 'Underground Organisation',
        'COLDWAR_COL_select_case': 'Security file: [FROM.GetName]',
        'COLDWAR_COL_select_case_desc': 'Review this region’s organisation strength, foreign assistance and police appropriation.',
        'COLDWAR_COL_legacy_ira_channel_tt': 'Review the Northern Ireland regional contact file. Deliveries require a regional intelligence network above 50% and are commissioned through Resistance Contacts.',
        'COLDWAR_COL_british_domestic_setup_tt': 'Establish the British domestic political institutions and regional development programmes. Northern Ireland is administered through Internal Security Cases.',
        'COLDWAR_COL_local_effects_tt': 'Current local construction: §Y[?COLDWAR_COL_view_construction_penalty|0]%§!; resources: §Y[?COLDWAR_COL_view_resources_penalty|0]%§!. Resistance stages are cumulative: §Y20%§!, construction §R−10%§!; §Y40%§!, resources §R−10%§! and garrisons §R+15%§!; §Y60%§!, supplies §R−10%§!. Active colonial wars retain at least §Y35%§! resistance; contested administrations retain §Y25%§!, where occupation resistance exists. A settled petition has a §Y15%§! chance of a §Y90-day§! détente with a lower §Y15%§! floor. At §Y40%§! resistance weekly costs rise §R25%§!; at §Y60%§!, §R50%§!. An unanswered petition adds §R−5%§! construction and resources for §Y90 days§!.',
        'COLDWAR_COL_issue_grant_tt': 'Pay §Y$[?COLDWAR_COL_issue_grant_cost|3]bn§!. Local construction §G+5%§! for §Y90 days§! and §G+5 compliance§! where occupation applies. Resolve the petition. In contested or armed administrations: §Y15%§! chance of a §Y90-day§! détente with a §Y15%§! resistance floor.',
        'COLDWAR_COL_issue_consult_tt': 'Spend §Y[?COLDWAR_COL_issue_pp_cost|0] Political Power§!. Local resources §G+3%§! for §Y90 days§!; resistance §G−3§! where occupation applies. Resolve the petition. In contested or armed administrations: §Y15%§! chance of a §Y90-day§! détente with a §Y15%§! resistance floor.',
        'COLDWAR_COL_movement_generic': 'Local resistance organisations',
        'COLDWAR_COL_contact_unknown': 'Select a regional file',
        'COLDWAR_COL_leak_title': 'Foreign support exposed',
        'COLDWAR_COL_leak_desc': 'Evidence links [event_target:COLDWAR_COL_exposed_sponsor.GetAdjective] assistance to clandestine contacts in [event_target:COLDWAR_COL_exposed_region.GetName]. The documents have reached the international press.',
        'COLDWAR_COL_leak_response': 'Lodge a formal protest.',
        'COLDWAR_COL_leak_news_title': '[event_target:COLDWAR_COL_exposed_sponsor.GetAdjectiveCap] SUPPORT FOR [COLDWAR_COL_GetExposedMovement] EXPOSED',
        'COLDWAR_COL_leak_news_desc': 'Documents linking [event_target:COLDWAR_COL_exposed_sponsor.GetAdjective] officials to support for [COLDWAR_COL_GetExposedMovement] in [event_target:COLDWAR_COL_exposed_region.GetName] have become public. The responsible authorities have lodged a diplomatic protest.',
        'COLDWAR_COL_leak_news_response': 'A serious diplomatic disclosure.',
        'COLDWAR_COL_incident_title': 'Underground violence',
        'COLDWAR_COL_incident_desc': 'A clandestine organisation has carried out an attack. Investigators face renewed pressure to disrupt its local support and supply networks.',
        'COLDWAR_COL_incident_response': 'Support the investigation.',
        'COLDWAR_COL_support_political_tt': '[COLDWAR_COL_GetPoliticalTerms]\\nRequires a regional intelligence network §Yabove 50%§!. §Y10%§! chance of public disclosure: sponsor stability §R−1%§!, relations §R−25§! for §Y180 days§!, international news and notification of the responsible government.',
        'COLDWAR_COL_support_funding_tt': '§Y$0.05bn§!: +§R5§! resistance target or organisation support for §Y180 days§!. Shared regional aid cap: §Y15§!. RAF aid is shared across its regional contacts and adds §R0.05 cadres per aid point each month§! to the German security case. Requires a regional intelligence network §Yabove 50%§!. §Y25%§! chance of public disclosure: sponsor stability §R−1%§!, relations §R−25§! for §Y180 days§!, international news and notification of the responsible government.',
        'COLDWAR_COL_support_arms_tt': '§Y15 Political Power, 250 Infantry Weapons, 25 Command and Control Equipment§!: +§R5§! resistance and +§R5§! resistance target for §Y180 days§!. IRA cells instead gain §R3§! organisation strength and §R5§! support. RAF instead gains §R1 cadre§! and §R5§! aid for §Y180 days§!; each aid point adds §R0.05 cadres per month§!. Shared aid cap: §Y15§!; RAF contacts share one organisation cap. Requires a regional intelligence network §Yabove 50%§!. §Y40%§! chance of public disclosure: sponsor stability §R−1%§!, relations §R−25§! for §Y180 days§!, international news and notification of the responsible government.',
        'COLDWAR_COL_political_colonial_terms': '§Y15 Political Power§!: strengthen the next colonial petition within §Y180 days§!. Settlement costs rise by §Y$0.025bn§! or §Y10 Political Power§!.',
        'COLDWAR_COL_political_domestic_terms': '§Y15 Political Power§!: organisation strength §R+5§!. One political package per sponsor every §Y180 days§!.',
        'COLDWAR_COL_political_raf_terms': '§Y15 Political Power§!: RAF sympathiser milieu §R+2§! in the German security case. One political package per sponsor every §Y180 days§!.',
        'COLDWAR_COL_political_occupation_terms': '§Y15 Political Power§!: local compliance §R−3§!. One political package per sponsor every §Y180 days§!.',
    })
    for package, risk in [('funding',25),('arms',40)]:
        local[f'COLDWAR_COL_support_{package}_tt']=f'[COLDWAR_COL_Get{package.title()}Terms]\\nRequires a regional intelligence network §Yabove 50%§!. Package cooldown: §Y180 days§!. §Y{risk}%§! public disclosure chance: sponsor stability §R−1%§!, relations §R−25§! for §Y180 days§!, international news and notification of the responsible government.'
    local.update({
        'COLDWAR_COL_funding_standard_terms':'§Y$0.05bn§!: resistance target §R+5§! for §Y180 days§!. Combined regional target bonus capped at §Y15§!.',
        'COLDWAR_COL_funding_ira_terms':'§Y$0.05bn§!: IRA aid §R+5§! for §Y180 days§!, adding §R0.5 organisation strength per month§!. Combined aid capped at §Y15§!.',
        'COLDWAR_COL_funding_raf_terms':'§Y$0.05bn§!: RAF aid §R+5§! for §Y180 days§!, adding §R0.25 cadres per month§!. All RAF regional contacts share one §Y15§!-point aid cap.',
        'COLDWAR_COL_arms_standard_terms':'§Y15 Political Power, 250 Infantry Weapons, 25 Command and Control Equipment§!: resistance §R+5§! and resistance target §R+5§! for §Y180 days§!. Shared target bonus capped at §Y15§!.',
        'COLDWAR_COL_arms_ira_terms':'§Y15 Political Power, 250 Infantry Weapons, 25 Command and Control Equipment§!: IRA organisation strength §R+3§!; aid §R+5§! for §Y180 days§!, adding §R0.5 strength per month§!. Shared aid cap: §Y15§!.',
        'COLDWAR_COL_arms_raf_terms':'§Y15 Political Power, 250 Infantry Weapons, 25 Command and Control Equipment§!: RAF cadres §R+1§!; aid §R+5§! for §Y180 days§!, adding §R0.25 cadres per month§!. All RAF contacts share one §Y15§!-point aid cap.',
    })
    append_file(files, 'common/scripted_triggers/COLDWAR_colonial_contacts.txt', '\n'.join(triggers))
    append_file(files, 'common/scripted_effects/COLDWAR_colonial_contacts.txt', '\n'.join(effects))
    return local
