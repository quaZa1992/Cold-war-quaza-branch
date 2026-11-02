# IMPERIA COLD WAR — Israel V2 domestic project funds and reserve actions.
"""Pure runtime emitter; the root compiler owns every returned file write.

All balances and positive weekly streams use billion USD. Project quotes only
produce calculation outputs. Commits consume actual used envelopes, never mint
cash. Private capital comes exclusively from the bilateral transaction provider.
"""
from copy import deepcopy
from decimal import Decimal


MARKER = '# IMPERIA COLD WAR — Israel V2 domestic projects and reserve actions.\n'
OWNED = ('absorption_appeal', 'national_bargain', 'gahal_settlement_match',
         'sapir_book', 'sapir_negev', 'development_repayment',
         'reserve_exercise', 'reserve_callup', 'reserve_release',
         'bounded_callup', 'labor_procurement_ceiling', 'home_front', 'security_emergency')


def num(v):
    return format(Decimal(str(v)).quantize(Decimal('.00001')), 'f').rstrip('0').rstrip('.') or '0'


def B(key, body):
    return key + ' = {\n' + '\n'.join('\t' + x for x in body.splitlines()) + '\n}'


def C(*items):
    return '\n'.join(x for x in items if x)


def V(key, value):
    return f'set_variable = {{ {key} = {num(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def A(key, value):
    return f'add_to_variable = {{ {key} = {num(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def S(key, value):
    return f'subtract_from_variable = {{ {key} = {num(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def M(key, value):
    return f'multiply_variable = {{ {key} = {num(value)} }}'


def Q(key, base, rate):
    return C(V(key, base), M(key, rate))


def check(key, op, value):
    value = num(value) if isinstance(value, (float, int, Decimal)) else value
    if op in ('>=', '<='):
        comparison = 'greater_than_or_equals' if op == '>=' else 'less_than_or_equals'
        return f'check_variable = {{ var = {key} value = {value} compare = {comparison} }}'
    return f'check_variable = {{ {key} {op} {value} }}'


def IF(condition, body, other=''):
    return B('if', C(B('limit', condition), body)) + ('\n' + B('else', other) if other else '')


def cash(value, negative=True):
    return C(f'set_temp_variable = {{ treasury_change = {value} }}',
             'multiply_temp_variable = { treasury_change = -1 }' if negative else '',
             'modify_treasury_effect = yes')


def debt(value):
    return C(f'set_temp_variable = {{ debt_change = {value} }}',
             'multiply_temp_variable = { debt_change = -1 }',
             'modify_debt_effect = yes')


def reset(focus):
    return B('uncomplete_national_focus', f'focus = ISR2_{focus}\nuncomplete_children = no\nrefund_political_power = no')


def owned(state):
    return f'owns_state = {state}\ncontrols_state = {state}\nhas_full_control_of_state = {state}'


def extend_data(data):
    """Add the one authorized real provider for the approved RP emergency gate."""
    result = deepcopy(data)
    if any(n['id'] == 'ISR2_security_emergency' for n in result['nodes']):
        return result
    origin = next(g['origin'] for g in result['groups'] if g['id'] == 'reserves')
    result['nodes'].append(dict(id='ISR2_security_emergency', group='reserves',
        label='Authorise a Limited Security Emergency', xy=[origin[0] - 5, origin[1] + 3], days=7,
        pre=[['ISR2_reserve_register']], exclusive=[],
        description='The cabinet can authorise a limited reserve emergency without declaring war. The political cost is paid anew for each authorisation, while foreign relations and borders remain matters for the players.',
        effects=[dict(label='Political Power', value='-30', tone='cost', native_key='political_power', amount=-30),
                 dict(label='Stability', value='-3%', tone='cost', native_key='stability', amount=-.03),
                 dict(label='Cabinet Security Emergency', value='+70 days', tone='neutral')],
        requirements=['No cabinet security-emergency authorisation has been issued in the last 180 days.'],
        icon='GFX_ISR70_focus_isr_independence', modifiers={},
        history=dict(status='RP abstraction', sources=['economy'], note='A bounded playable cabinet authorisation, not a claim that a historical emergency statute lasted 70 days.'),
        mechanics=['A real paid national focus supplies the call-up emergency gate. No war, treaty, border, government or GC privilege changes. Every renewed authorisation pays its full political costs.'],
        programme='Cabinet authorisation: 70 days', action_origin='national_focus',
        focus_cycle=dict(cooldown_days=180, lifetime_limit=None, provider='uncomplete_national_focus',
                         uncomplete_children=False, refund_political_power=False, new_term_costs=True)))
    return result


def _support(effects):
    # Output variables are calculations only. Quote never touches the funding
    # balances, project counts, coupons, Treasury or any construction receipt.
    take = lambda output, balance: C(V(output, 'ISR2_project_net_cost'),
        IF(check(output, '>', balance), V(output, balance)),
        'clamp_variable = { var = ' + output + ' min = 0 }')
    quote = C(V('ISR2_project_net_cost', 'ISR2_project_cost'),
        'clamp_variable = { var = ISR2_project_net_cost min = 0 }',
        V('ISR2_project_absorption_used', 0), V('ISR2_project_match_used', 0), V('ISR2_project_procurement_used', 0),
        Q('ISR2_project_support_cap', 'ISR2_project_quote', .005),
        IF(check('ISR2_project_class', '=', 1), C(
            take('ISR2_project_absorption_used', 'ISR2_domestic_absorption_balance'),
            S('ISR2_project_net_cost', 'ISR2_project_absorption_used'),
            IF(check('ISR2_domestic_civilian_projects', '>', 0), C(
                take('ISR2_project_match_used', 'ISR2_domestic_civilian_balance'),
                IF(check('ISR2_project_match_used', '>', 'ISR2_project_support_cap'), V('ISR2_project_match_used', 'ISR2_project_support_cap')),
                S('ISR2_project_net_cost', 'ISR2_project_match_used'))))),
        IF(check('ISR2_project_class', '=', 2), IF(check('ISR2_domestic_settlement_projects', '>', 0), C(
            take('ISR2_project_match_used', 'ISR2_domestic_settlement_balance'),
            IF(check('ISR2_project_match_used', '>', 'ISR2_project_support_cap'), V('ISR2_project_match_used', 'ISR2_project_support_cap')),
            S('ISR2_project_net_cost', 'ISR2_project_match_used')))),
        IF(check('ISR2_project_class', '=', 0), C(*[
            IF(C(check('ISR2_project_procurement', '=', kind), f'has_country_flag = ISR2_domestic_{slug}_coupon'), C(
                V('ISR2_project_procurement_used', 'ISR2_project_net_cost'),
                IF(check('ISR2_project_procurement_used', '>', 'ISR2_project_support_cap'), V('ISR2_project_procurement_used', 'ISR2_project_support_cap')),
                S('ISR2_project_net_cost', 'ISR2_project_procurement_used')))
            for kind, slug in ((1, 'tank'), (2, 'aircraft'))])))
    effects['ISR2_project_support_quote'] = quote
    effects['ISR2_project_support_commit'] = C('ISR2_project_support_quote = yes',
        IF(check('ISR2_project_absorption_used', '>', 0), S('ISR2_domestic_absorption_balance', 'ISR2_project_absorption_used')),
        *[IF(C(check('ISR2_project_class', '=', kind), check('ISR2_project_match_used', '>', 0)), C(
            S('ISR2_domestic_' + slug + '_balance', 'ISR2_project_match_used'),
            S('ISR2_domestic_' + slug + '_projects', 1)))
          for kind, slug in ((1, 'civilian'), (2, 'settlement'))],
        *[IF(C(check('ISR2_project_procurement', '=', kind), check('ISR2_project_procurement_used', '>', 0)),
             'clr_country_flag = ISR2_domestic_' + slug + '_coupon')
          for kind, slug in ((1, 'tank'), (2, 'aircraft'))])


def build(data):
    """Return files/actions/init/daily/loc; do not mutate or emit the catalogue."""
    before = deepcopy(data)
    nodes = {n['id'][5:]: n for n in data['nodes'] if n['id'][5:] in OWNED}
    assert set(nodes) == set(OWNED), ('Missing domestic actions', set(OWNED) - set(nodes))
    groups = {g['id']: g for g in data['groups']}
    effects, triggers, modifiers, actions, loc = {}, {}, {}, {}, {}
    reopen = []

    def shown(key, value):
        loc['ISR2_domestic_' + key] = value
        return 'custom_effect_tooltip = ISR2_domestic_' + key

    def require(key, value, guard):
        loc['ISR2_domestic_' + key] = value
        return B('custom_trigger_tooltip', 'tooltip = ISR2_domestic_' + key + '\n' + guard)

    def modifier(key, name, values, enable, icon='GFX_idea_reserve_divisions'):
        key = 'ISR2_domestic_' + key
        modifiers[key] = C('icon = ' + icon, B('enable', enable),
                           *(k + ' = ' + num(v) for k, v in values.items()))
        loc[key] = name
        loc[key + '_desc'] = ''
        return key

    def arm(key):
        return 'add_dynamic_modifier = { modifier = ' + key + ' }'

    def action(slug, guard, body, preview, rate=None, repeat=None):
        n = nodes[slug]
        party = groups[n['group']].get('runtime_party_trigger')
        internal = C('ISR2_is_scenario = yes',
            'NOT = { has_country_flag = ISR2_domestic_' + ('cooldown_' if repeat else 'done_') + slug + ' }',
            *(f'NOT = {{ has_completed_focus = {alternative} }}' for alternative in n.get('exclusive', [])),
            *(f'NOT = {{ has_country_flag = ISR2_domestic_done_{alternative[5:]} }}' for alternative in n.get('exclusive', [])))
        can = C(B('hidden_trigger', internal), party + ' = yes' if party else '', guard)
        triggers['ISR2_domestic_can_' + slug] = can
        completed = C(body,
            'set_country_flag = ISR2_domestic_done_' + slug,
            'set_country_flag = { flag = ISR2_domestic_cooldown_' + slug + ' value = 1 days = ' + str(repeat) + ' }' if repeat else '',
            'ISR2_domestic_refresh = yes', 'update_money_dirty_variable = yes')
        effects['ISR2_domestic_complete_' + slug] = C('ISR2_domestic_refresh_prices = yes',
            'ISR2_private_recalculate = yes',
            IF('ISR2_domestic_can_' + slug + ' = yes', completed,
                IF('NOT = { has_country_flag = ISR2_domestic_' + ('cooldown_' if repeat else 'done_') + slug + ' }', reset(slug))))
        actions[n['id']] = dict(available='ISR2_domestic_can_' + slug + ' = yes',
            visible_available=C(guard,
                require('cooldown_' + slug,
                    'At least ' + str(repeat) + ' days since the previous completion.',
                    'NOT = { has_country_flag = ISR2_domestic_cooldown_' + slug + ' }') if repeat else ''),
            reward='ISR2_domestic_complete_' + slug + ' = yes', preview=preview)
        if repeat:
            reopen.append(IF(C('has_completed_focus = ' + n['id'],
                'NOT = { has_country_flag = ISR2_domestic_cooldown_' + slug + ' }'), reset(slug)))

    # Native current-GDP quotes. These cached availability/preview values are
    # refreshed again immediately before every actual completion transaction.
    rates = {'grant': .04, 'match': .005, 'match_total': .01, 'tender': .0075,
             'repayment': .02, 'exercise': .002, 'calendar': .006,
             'procurement': .003, 'homefront': .008, 'reserve_weekly': .0004,
             'homefront_weekly': .0001}
    price_body = [Q('ISR2_domestic_quote_' + key, 'gdp_total', rate) for key, rate in rates.items()]
    price_body += [V('ISR2_domestic_anonymous_debt', 'debt'), S('ISR2_domestic_anonymous_debt', 'ISR2_bilateral_loan_outstanding'),
                   'clamp_variable = { var = ISR2_domestic_anonymous_debt min = 0 }']
    effects['ISR2_domestic_refresh_prices'] = C(*price_body)
    _support(effects)
    funds = lambda key: require('funds_' + key,
        'Treasury: at least $[?ISR2_domestic_quote_' + key + '|3] billion.',
        check('treasury', '>=', 'ISR2_domestic_quote_' + key))
    private = lambda key: require('private_' + key,
        'Partner Project Capital: at least $[?ISR2_domestic_quote_' + key + '|3] billion.',
        check('ISR2_private_available', '>=', 'ISR2_domestic_quote_' + key))
    charge = lambda key: cash('ISR2_domestic_quote_' + key)
    action('absorption_appeal', '', V('ISR2_domestic_absorption_balance', 'ISR2_domestic_quote_grant'),
        shown('absorption_grant_tt', 'Civilian Absorption Appropriation: §G+$[?ISR2_domestic_quote_grant|3] billion§!'))

    for slug, kind, label in (('national_bargain', 'civilian', 'Civilian Housing and Training Appropriation'),
                               ('gahal_settlement_match', 'settlement', 'Controlled Settlement Appropriation')):
        # Consumption is atomic in the real bilateral provider: ready checks the
        # sum of actually funded eligible counterparties before taking anything.
        body = C(V('ISR2_private_required', 'ISR2_domestic_quote_match'),
            'ISR2_private_commit = yes', charge('match'),
            V('ISR2_domestic_' + kind + '_balance', 'ISR2_domestic_quote_match_total'),
            V('ISR2_domestic_' + kind + '_projects', 2))
        preview = C(charge('match'),
            shown('private_match_tt', 'Partner Project Capital: §R-$[?ISR2_domestic_quote_match|3] billion§!'),
            shown(kind + '_match_tt', label + ': §G+$[?ISR2_domestic_quote_match_total|3] billion§!'))
        action(slug, C(funds('match'), private('match')), body, preview)

    for slug, state in (('sapir_book', 205), ('sapir_negev', 206)):
        feasible = C(owned(state), require('factory_staff', 'The new civilian factory can be staffed.', 'can_staff_an_industrial_complex = yes'),
            require('factory_capacity_' + str(state), ('Haifa' if state == 205 else 'Negev') + ' has capacity for one new civilian factory.', B(str(state), C(
            'check_variable = { var = building_level@industrial_complex value = 49 compare = less_than_or_equals }',
            'free_building_slots = { building = industrial_complex size > 0 include_locked = yes }'))))
        building = B(str(state), 'add_extra_state_shared_building_slots = 1\nadd_building_construction = { type = industrial_complex level = 1 instant_build = yes }')
        action(slug, C(feasible, funds('tender'), private('tender')),
            C(V('ISR2_private_required', 'ISR2_domestic_quote_tender'), 'ISR2_private_commit = yes', charge('tender'), building),
            C(charge('tender'), shown('private_tender_tt', 'Partner Project Capital: §R-$[?ISR2_domestic_quote_tender|3] billion§!'), building))

    # Anonymous debt is retired first. Only the shortfall enters the named
    # creditor's guarded early-repayment provider, which credits that creditor.
    repayment_quote = C(V('ISR2_domestic_anonymous_payment', 'ISR2_domestic_quote_repayment'),
        IF(check('ISR2_domestic_anonymous_payment', '>', 'ISR2_domestic_anonymous_debt'), V('ISR2_domestic_anonymous_payment', 'ISR2_domestic_anonymous_debt')),
        V('ISR2_domestic_named_payment', 'ISR2_domestic_quote_repayment'), S('ISR2_domestic_named_payment', 'ISR2_domestic_anonymous_payment'))
    effects['ISR2_domestic_quote_repayment'] = repayment_quote
    # Parent provider exposes the real pair-clear trigger for the Soviet loan.
    eligible = require('eligible_debt', 'Eligible outstanding public debt: at least $[?ISR2_domestic_quote_repayment|3] billion.',
        C(check('debt', '>=', 'ISR2_domestic_quote_repayment'), B('OR', C(
            check('ISR2_domestic_anonymous_debt', '>=', 'ISR2_domestic_quote_repayment'),
            'ISR2_b_eastern_credit_pair_clear = yes'))))
    repay = C('ISR2_domestic_quote_repayment = yes',
        IF(check('ISR2_domestic_named_payment', '>', 0), C(
            'set_temp_variable = { ISR2_bilateral_early_repayment = ISR2_domestic_named_payment }',
            'ISR2_bilateral_loan_early_repay = yes')),
        IF(check('ISR2_domestic_anonymous_payment', '>', 0), C(cash('ISR2_domestic_anonymous_payment'), debt('ISR2_domestic_anonymous_payment'))))
    action('development_repayment', C(funds('repayment'), eligible), repay,
        C(charge('repayment'), debt('ISR2_domestic_quote_repayment')), repeat=182)

    calendar = 'has_country_flag = ISR2_domestic_done_bounded_callup'
    emergency = B('OR', 'has_war = yes\nhas_country_flag = ISR2_domestic_security_emergency')
    callup_guard = C('ISR2_is_scenario = yes', check('ISR2_domestic_callup_days', '>', 0), emergency)
    exercise_key = modifier('exercise', 'Limited Reserve Exercise', {'civilian_factories_productivity': -.05},
        C('ISR2_is_scenario = yes', check('ISR2_domestic_exercise_days', '>', 0), check('ISR2_domestic_callup_days', '<', 1)))
    callup_base = modifier('callup', 'National Reserve Call-Up',
        {'mobilization_speed': .25, 'army_org_factor': .08, 'civilian_factories_productivity': -.12, 'offices_productivity': -.08},
        C(callup_guard, 'NOT = { ' + calendar + ' }'))
    callup_calendar = modifier('callup_calendar', 'National Reserve Call-Up',
        {'mobilization_speed': .25, 'army_org_factor': .08, 'civilian_factories_productivity': -.08, 'offices_productivity': -.08},
        C(callup_guard, calendar))
    end_callup = C(V('ISR2_domestic_callup_days', 0), 'remove_dynamic_modifier = { modifier = ' + callup_base + ' }',
        'remove_dynamic_modifier = { modifier = ' + callup_calendar + ' }')
    effects['ISR2_domestic_end_callup'] = end_callup
    exercise_duration = IF(calendar, V('ISR2_domestic_exercise_days', 28), V('ISR2_domestic_exercise_days', 35))
    action('reserve_exercise', C(funds('exercise'), require('no_callup', 'No national reserve call-up is active.', check('ISR2_domestic_callup_days', '<', 1)),
        require('no_exercise', 'No reserve exercise is active.', check('ISR2_domestic_exercise_days', '<', 1))),
        C(charge('exercise'), 'army_experience = 20', exercise_duration),
        C(charge('exercise'), 'army_experience = 20', shown('exercise_duration_tt', 'Limited Reserve Exercise: civilian industry productivity §R-5%§! for §Y35 days§!, or §Y28 days§! with the readiness calendar.')), repeat=182)
    action('security_emergency', C(require('cabinet_power', 'Political Power: at least 30.', 'NOT = { has_political_power < 30 }'),
        require('cabinet_stability', 'Stability: at least 3%.', 'NOT = { has_stability < 0.03 }'),
        require('cabinet_inactive', 'No cabinet security-emergency authorisation is currently active.', 'NOT = { has_country_flag = ISR2_domestic_security_emergency }')),
        C('add_political_power = -30', 'add_stability = -0.03', 'set_country_flag = { flag = ISR2_domestic_security_emergency value = 1 days = 70 }'),
        C('add_political_power = -30', 'add_stability = -0.03', shown('security_emergency_tt', 'Cabinet Security Emergency: §Y70 days§!')), repeat=180)
    action('reserve_callup', C(require('security_emergency_condition', 'Israel is at war or a cabinet security-emergency authorisation is active.', emergency),
        require('no_callup', 'No national reserve call-up is active.', check('ISR2_domestic_callup_days', '<', 1))),
        C(V('ISR2_domestic_exercise_days', 0), 'remove_dynamic_modifier = { modifier = ' + exercise_key + ' }', V('ISR2_domestic_callup_days', 70)),
        C(shown('callup_term_tt', 'National Reserve Call-Up: §Yat most 70 days§!.'),
          shown('callup_military_tt', 'Mobilization speed: §G+25%§!\nDivision Organisation: §G+8%§!'),
          shown('callup_output_tt', 'Civilian industry productivity: §R-12%§!, or §R-8%§! with the readiness calendar.\nOffice productivity: §R-8%§!'),
          shown('callup_weekly_tt', 'Reserve Call-Up Expense: §R-$[?ISR2_domestic_quote_reserve_weekly|5] billion per week§!')), repeat=70)
    action('reserve_release', require('callup_active', 'A national reserve call-up is active.', check('ISR2_domestic_callup_days', '>', 0)),
        'ISR2_domestic_end_callup = yes', C('remove_dynamic_modifier = { modifier = ' + callup_base + ' }',
            shown('release_tt', 'Mobilization speed: §R-25%§!\nDivision Organisation: §R-8%§!\nCivilian industry productivity: §G+12%§!, or §G+8%§! with the readiness calendar.\nOffice productivity: §G+8%§!'),
            shown('release_weekly_tt', 'Reserve Call-Up Expense Removed: §G+$[?ISR2_domestic_quote_reserve_weekly|5] billion per week§!')), repeat=70)
    action('bounded_callup', funds('calendar'), C(charge('calendar'),
        IF(check('ISR2_domestic_exercise_days', '>', 0), C(S('ISR2_domestic_exercise_days', 7),
            'clamp_variable = { var = ISR2_domestic_exercise_days min = 0 }'))),
        C(charge('calendar'), shown('calendar_tt', 'Limited Reserve Exercise duration: §G-7 days§!\nNational Reserve Call-Up civilian productivity penalty: §R-12%§! becomes §R-8%§!')))
    procurement_guard = B('OR', 'NOT = { has_completed_focus = ISR2_tal_tank }\nNOT = { has_completed_focus = ISR2_nesher }')
    action('labor_procurement_ceiling', C(funds('procurement'), procurement_guard),
        C(charge('procurement'),
            IF('NOT = { has_completed_focus = ISR2_tal_tank }', 'set_country_flag = ISR2_domestic_tank_coupon'),
            IF('NOT = { has_completed_focus = ISR2_nesher }', 'set_country_flag = ISR2_domestic_aircraft_coupon')),
        C(charge('procurement'), shown('procurement_tt', 'Next uncompleted domestic tank project setup cost: §G-0.5% of annual GDP§!\nNext uncompleted domestic aircraft project setup cost: §G-0.5% of annual GDP§!')))

    home_guard = C('ISR2_is_scenario = yes', 'has_country_flag = ISR2_domestic_done_home_front', owned(204))
    home_state = modifier('civil_defence_204', 'Tel Aviv Civil Defence Institution', {},
        C(B('204', 'is_owned_by = ISR\nis_controlled_by = ISR'), B('ISR', C('ISR2_is_scenario = yes', 'has_country_flag = ISR2_domestic_done_home_front'))), 'GFX_idea_health_care')
    home_asset = B('204', 'add_extra_state_shared_building_slots = 1\nadd_dynamic_modifier = { modifier = ' + home_state + ' scope = ISR }')
    loc['ISR2_homefront_medical_protocol'] = 'Civil Defence Medical Protocol'
    loc['ISR2_homefront_medical_protocol_desc'] = 'Medical protocols developed through the civil-defence establishment improve casualty recovery in combat-service-support formations.'
    home_protocol = 'set_technology = { ISR2_homefront_medical_protocol = 1 }'
    action('home_front', C(owned(204), funds('homefront')), C(charge('homefront'), home_asset, home_protocol),
        C(charge('homefront'), home_asset, home_protocol,
            shown('medical_protocol_tt', '$combat_service_support_company$: Casualty Trickleback §G+10%§!\n$helicopter_combat_service_support$: Casualty Trickleback §G+10%§!'),
            shown('homefront_weekly_tt', 'Emergency Medical Establishment: §R-$[?ISR2_domestic_quote_homefront_weekly|5] billion per week§!')))

    def reconcile(key, condition):
        return IF(condition, IF('NOT = { has_dynamic_modifier = { modifier = ' + key + ' } }', arm(key)),
            IF('has_dynamic_modifier = { modifier = ' + key + ' }', 'remove_dynamic_modifier = { modifier = ' + key + ' }'))
    refresh = C('ISR2_domestic_refresh_prices = yes',
        V('ISR2_domestic_previous_expense', 'ISR2_domestic_weekly_expense'),
        V('ISR2_domestic_weekly_income', 0), V('ISR2_domestic_weekly_expense', 0),
        reconcile(exercise_key, C(check('ISR2_domestic_exercise_days', '>', 0), check('ISR2_domestic_callup_days', '<', 1))),
        reconcile(callup_base, C(callup_guard, 'NOT = { ' + calendar + ' }')),
        reconcile(callup_calendar, C(callup_guard, calendar)),
        IF(home_guard, C(A('ISR2_domestic_weekly_expense', 'ISR2_domestic_quote_homefront_weekly'), B('204',
            IF('NOT = { has_dynamic_modifier = { modifier = ' + home_state + ' } }', 'add_dynamic_modifier = { modifier = ' + home_state + ' scope = ISR }')))),
        IF(callup_guard, A('ISR2_domestic_weekly_expense', 'ISR2_domestic_quote_reserve_weekly')),
        IF('NOT = { check_variable = { ISR2_domestic_weekly_expense = ISR2_domestic_previous_expense } }', 'update_money_dirty_variable = yes'))
    effects['ISR2_domestic_refresh'] = IF('ISR2_is_scenario = yes', refresh)
    effects['ISR2_domestic_daily'] = IF('ISR2_is_scenario = yes', C(
        IF(check('ISR2_domestic_exercise_days', '>', 0), S('ISR2_domestic_exercise_days', 1)),
        IF(check('ISR2_domestic_callup_days', '>', 0), C(S('ISR2_domestic_callup_days', 1),
            IF(B('OR', C(B('NOT', emergency), check('ISR2_domestic_callup_days', '<', 1))), 'ISR2_domestic_end_callup = yes'))),
        *reopen, 'ISR2_domestic_refresh = yes'))
    balances = ('absorption_balance', 'civilian_balance', 'civilian_projects', 'settlement_balance', 'settlement_projects',
                'exercise_days', 'callup_days', 'weekly_income', 'weekly_expense')
    effects['ISR2_domestic_init'] = C(IF(C('ISR2_is_scenario = yes', 'NOT = { has_country_flag = ISR2_domestic_initialized }'), C(
        *(V('ISR2_domestic_' + name, 0) for name in balances), 'set_country_flag = ISR2_domestic_initialized')),
        'ISR2_domestic_refresh = yes')
    files = {
        'common/scripted_effects/ISR2_domestic_effects.txt': MARKER + '\n\n'.join(B(k, v) for k, v in effects.items()) + '\n',
        'common/scripted_triggers/ISR2_domestic_triggers.txt': MARKER + '\n\n'.join(B(k, v) for k, v in triggers.items()) + '\n',
        'common/dynamic_modifiers/ISR2_domestic_modifiers.txt': MARKER + '\n\n'.join(B(k, v) for k, v in modifiers.items()) + '\n',
        'common/technologies/ISR2_domestic_technology.txt': MARKER + B('technologies', B('ISR2_homefront_medical_protocol',
            C('allow = { always = no }', 'combat_service_support_company = { casualty_trickleback = 0.1 }',
              'helicopter_combat_service_support = { casualty_trickleback = 0.1 }'))) + '\n',
    }
    assert data == before, 'Domestic emitter changed approved catalogue'
    # Runtime previews must disclose the verified native scope adaptations,
    # while the approved design catalogue itself remains byte-immutable.
    adaptations = {
        'ISR2_home_front': {
            'description': 'The reserve system leaves families and workplaces exposed to the same emergency. A civil-defence and medical institution in Tel Aviv establishes casualty-recovery protocols for combat-service-support formations.',
            'effects': [deepcopy(e) for e in nodes['home_front']['effects'] if e['label'] not in ('Tel Aviv: Civilian Shelter', 'Casualty Trickleback')] + [
                dict(label='Tel Aviv: Civil Defence Institution', value='+1', tone='gain'),
                dict(label='Combat Service Support Company: Casualty Trickleback', value='+10%', tone='gain'),
                dict(label='Helicopter Combat Service Support: Casualty Trickleback', value='+10%', tone='gain')],
        },
        'ISR2_reserve_callup': {
            'requirements': ['Israel is at war or a paid cabinet security-emergency authorisation is active.'],
        },
    }
    for slug, rate in (('national_bargain', .005), ('gahal_settlement_match', .005),
                       ('sapir_book', .0075), ('sapir_negev', .0075)):
        n = nodes[slug]
        rows = deepcopy(n['effects'])
        for row in rows:
            if row['label'] in ('Accepted Private Project Capital', 'Accepted Private Matched Investment'):
                row.update(label='Partner Project Capital', value='-' + num(rate * 100) + '% of annual GDP', tone='cost')
        adaptations['ISR2_' + slug] = dict(effects=rows,
            requirements=[line.replace('Actual matched private investment', 'Accepted partner project co-financing')
                          .replace('actual accepted private capital', 'accepted partner project co-financing')
                          .replace('actual private capital', 'accepted partner project co-financing')
                          for line in n['requirements']])
    return dict(files=files, actions=actions, init='ISR2_domestic_init = yes', daily='ISR2_domestic_daily = yes',
        refresh='ISR2_domestic_refresh = yes', loc=loc,
        preview_adaptations=adaptations,
        metadata=dict(project='IMPERIA COLD WAR', actions=len(actions),
            weekly_income='ISR2_domestic_weekly_income', weekly_expense='ISR2_domestic_weekly_expense',
            support_inputs=['ISR2_project_cost', 'ISR2_project_quote', 'ISR2_project_class', 'ISR2_project_procurement'],
            support_output='ISR2_project_net_cost', native_gameplay_tested=False,
            adaptations={'home_front': 'No civilian_shelter building or valid casualty-trickleback country modifier exists. A named Tel Aviv institution and one urban shared slot replace the building. A focus-granted custom technology gives +10% casualty trickleback to combat_service_support_company and helicopter_combat_service_support, following native KOR_celltrion_tech. The paid weekly establishment remains.',
                         'reserve_callup': 'The approved RP gate is supplied by a separate paid cabinet-authorisation focus, without war, treaty, border or GC changes.'},
            custom_technology_reference='common/technologies/custom_tech.txt:KOR_celltrion_tech'))
