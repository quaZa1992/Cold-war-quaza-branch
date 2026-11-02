# IMPERIA COLD WAR — Israel V2 legacy occupation scope integration.
# IMPERIA COLD WAR — Israel 1970 territorial occupation profiles.
"""Distinct native state burdens and live national budget commitments.

The values are authored balance choices, not measured historical percentages.
The January 1970 ownership/core map is retained, including both Jerusalem cores.
Country budget modifiers are applied only to Israel, never in state scope.
"""
from policy_common import ident, scope


PROFILES = (
    dict(state=208, label='West Bank', occupied='PAL', resistance=18, compliance=25,
         state_modifiers={'resistance_target': .15, 'required_garrison_factor': .40,
                          'resistance_damage_to_garrison': .20, 'local_factories': -.15},
         country_modifiers={'police_cost_multiplier_modifier': .05,
                            'bureaucracy_cost_multiplier_modifier': .03,
                            'personnel_cost_multiplier_modifier': .02},
         rationale='A populated Palestinian territory requires military administration, policing and the protection of routes between communities.'),
    dict(state=209, label='Gaza', occupied='PAL', resistance=25, compliance=15,
         state_modifiers={'resistance_target': .25, 'required_garrison_factor': .60,
                          'resistance_damage_to_garrison': .35, 'local_factories': -.20},
         country_modifiers={'police_cost_multiplier_modifier': .08,
                            'bureaucracy_cost_multiplier_modifier': .04,
                            'personnel_cost_multiplier_modifier': .03},
         rationale='Dense civilian communities and contested military control place a substantial burden on the security establishment and civil administration.'),
    dict(state=213, label='Sinai', occupied='EGY', resistance=8, compliance=30,
         state_modifiers={'resistance_target': .05, 'required_garrison_factor': .20,
                          'local_supplies_for_controller': -.12, 'local_factories': -.10},
         country_modifiers={'police_cost_multiplier_modifier': .02,
                            'bureaucracy_cost_multiplier_modifier': .03,
                            'personnel_cost_multiplier_modifier': .08},
         rationale='Long desert supply routes and dispersed military positions make the Sinai commitment expensive in personnel and administration.'),
    dict(state=587, label='Golan Heights', occupied='SYR', resistance=10, compliance=20,
         state_modifiers={'resistance_target': .08, 'required_garrison_factor': .25,
                          'local_supplies_for_controller': -.05, 'local_factories': -.10},
         country_modifiers={'police_cost_multiplier_modifier': .02,
                            'bureaucracy_cost_multiplier_modifier': .02,
                            'personnel_cost_multiplier_modifier': .05},
         rationale='A contested upland frontier requires defended positions, dependable supply and a continuing regional administration.'),
)


def build(api):
    """Register once. The existing Israel policy tick invokes reconciliation."""
    records = []
    init = []
    reconcile = ['set_temp_variable = { ISR70_policy_occupation_budget_changed = 0 }']
    for profile in PROFILES:
        state, label = profile['state'], profile['label']
        # Ownership is intentionally not restricted: annexing a non-core state
        # does not by itself end its administrative and security requirements.
        eligible = (f'controls_state = {state}\n'
                    f'{state} = {{ NOT = {{ is_core_of = ISR }} }}')
        state_gate = (f'{state} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}\n'
                      'ISR = { tag = ISR ISR70_is_scenario = yes }')
        country_gate = 'tag = ISR\nISR70_is_scenario = yes\n' + eligible
        local = api.state_modifier(f'occupation_{state}_local',
            label + ': Military Administration', profile['rationale'],
            dict(profile['state_modifiers']), enable=state_gate)
        # The compiler method registers a dynamic modifier definition without
        # imposing its application scope. This definition is used only by the
        # country-scoped add/remove calls below, and has a country-only enable.
        national = api.state_modifier(f'occupation_{state}_budget',
            label + ': Administration and Security Budget',
            'Israel funds the personnel, policing and civil administration required to maintain its control of ' + label + '.',
            dict(profile['country_modifiers']), enable=country_gate)
        present = ident(f'occupation_{state}_budget_active')
        seeded = ident(f'occupation_{state}_seeded')
        # Native resistance systems can initially have zero strength. Start one
        # only if absent, using the actual 1970 occupied country's identity.
        # No forced core override is introduced, and no recurring value reset.
        init.append(f'''if = {{
limit = {{ {eligible} }}
{state} = {{
if = {{ limit = {{ NOT = {{ has_resistance = yes }} }} start_resistance = {profile['occupied']} }}
set_resistance = {profile['resistance']}
set_compliance = {profile['compliance']}
}}
set_country_flag = {seeded}
}}''')
        reconcile.append(f'''if = {{
limit = {{ {eligible} }}
{state} = {{
if = {{
limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {local} }} }} }}
add_dynamic_modifier = {{ modifier = {local} scope = ISR }}
}}
}}
if = {{
limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {national} }} }} }}
add_dynamic_modifier = {{ modifier = {national} }}
set_temp_variable = {{ ISR70_policy_occupation_budget_changed = 1 }}
}}
if = {{
limit = {{ NOT = {{ has_country_flag = {present} }} }}
set_country_flag = {present}
set_temp_variable = {{ ISR70_policy_occupation_budget_changed = 1 }}
}}
}}
else = {{
if = {{
limit = {{ has_dynamic_modifier = {{ modifier = {national} }} }}
remove_dynamic_modifier = {{ modifier = {national} }}
set_temp_variable = {{ ISR70_policy_occupation_budget_changed = 1 }}
}}
if = {{
limit = {{ has_country_flag = {present} }}
clr_country_flag = {present}
set_temp_variable = {{ ISR70_policy_occupation_budget_changed = 1 }}
}}
}}''')
        records.append(dict(state=state, label=label, occupied_country=profile['occupied'],
            state_modifier=local, country_modifier=national,
            state_modifiers=dict(profile['state_modifiers']),
            country_modifiers=dict(profile['country_modifiers']),
            initial_resistance=profile['resistance'], initial_compliance=profile['compliance'],
            seed_receipt=seeded, composition_receipt=present,
            rationale=profile['rationale'], eligibility=eligible,
            history_source='history/states/' + {
                208:'208-West Bank.txt',209:'209-Gaza.txt',213:'213-Sinai.txt',587:'587-Golan.txt'}[state]))

    receipt = ident('occupation_initial_seed_processed')
    body = f'''if = {{
limit = {{ tag = ISR ISR70_is_scenario = yes }}
if = {{
limit = {{ NOT = {{ has_country_flag = {receipt} }} }}
if = {{
limit = {{ date < 1970.2.1 }}
{chr(10).join(init)}
}}
set_country_flag = {receipt}
}}
{chr(10).join(reconcile)}
if = {{
limit = {{ check_variable = {{ ISR70_policy_occupation_budget_changed > 0 }} }}
update_money_dirty_variable = yes
}}
}}'''
    helper = api.effect('occupation_reconcile_profiles', body)
    api.tick.append(helper + ' = yes')
    api.data['occupation_profiles'] = {
        'project': 'IMPERIA COLD WAR',
        'profiles': records,
        'reconcile_effect': helper,
        'initial_seed_receipt': receipt,
        'seed_cutoff_exclusive': '1970.2.1',
        'seed_policy': 'Only the first reconciliation can seed a controlled non-core state, and only before February 1970. Existing later saves retain resistance and compliance.',
        'activation': 'Israeli control, no Israeli core, and the 1970 scenario. Ownership changes alone do not end a non-core occupation burden.',
        'restoration': 'Only modifiers and composition receipts are reconciled. No fees, assets, population or seeds are replayed.',
        'jerusalem': 'States 207 and 1253 retain their existing Israeli cores and are excluded.',
        'workforce_changes': False,
        'tax_penalties': False,
        'historical_numbers': False,
        'source_rationale': [
            'Current January 1970 state histories establish Palestinian ownership of 208/209, Egyptian ownership of 213, Syrian ownership of 587, and Israeli control without Israeli cores.',
            'Native effects_documentation.md: state-scoped set_resistance, set_compliance, start_resistance and add_dynamic_modifier; dynamic modifier scope can be restricted to ISR.',
            'Native modifiers_documentation.md and MD occupation_laws.txt: resistance target, garrison requirement and damage, local factory access and local supply are supported state effects.',
            'common/scripted_effects/00_money_system.txt: update_bureaucracy_rate, update_police_rate and update_military_rate consume the country budget multipliers.',
            'The differentiated profiles reflect civilian administration, security commitments and supply geography. All numeric penalties and initial values are explicit game-balance choices.',
        ],
        'runtime_verified': False,
    }
    return helper
