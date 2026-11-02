# IMPERIA COLD WAR — Israel V2 territorial administration and settlement runtime.
"""Compile native territorial mechanics without writing the returned game files.

All public actions originate in national focuses. Country and state modifiers
use separate native enable scopes. Paid assets and site costs survive elections;
foreign footholds contain no physical building grants or host consent menu.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from textwrap import indent
from pathlib import Path
import re
import sys

MARK = '# IMPERIA COLD WAR — Israel V2 territorial administration and settlements.\n'
AREAS = {'West Bank': 208, 'Gaza': 209, 'Sinai': 213, 'Golan': 587}
PROVINCES = {208: 11620, 209: 13207, 213: 4161, 587: 13205}
OCCUPIERS = {208: 'PAL', 209: 'PAL', 213: 'EGY', 587: 'SYR'}


def _preview_adaptations(data):
    """Describe real partner escrow use without changing the approved catalogue."""
    catalogue = {n['id']: n for n in data['nodes']}
    adapted = {}
    for slug in ('controlled_sites', 'west_bank_projects', 'sinai_projects',
                 'gaza_projects', 'golan_projects'):
        fid = 'ISR2_' + slug
        rows = deepcopy(catalogue[fid]['effects'])
        for row in rows:
            if row['label'] == 'Actual Private Project Capital':
                row.update(label='Partner Project Capital', value='-0.5% of annual GDP', tone='cost')
        adapted[fid] = dict(effects=rows)

    fid = 'ISR2_labor_yanai'
    adapted[fid] = dict(
        effects=[deepcopy(e) for e in catalogue[fid]['effects']
                 if e['label'] != 'Required Private Project Capital'],
        requirements=['Alignment is in Power.'],
        programme='Funded guarantee book: 52 weeks. Each insured project requires partner capital of 0.5% of annual GDP.',
        description='Political uncertainty deters investment in occupied territory. A state guarantee lowers the public share of later controlled-territory projects backed by an accepting partner. The Treasury holds a reserve and meets covered claims if a funded project is lost or relinquished.')

    fid = 'ISR2_mafdal_land_committee'
    adapted[fid] = dict(
        effects=[deepcopy(e) for e in catalogue[fid]['effects']
                 if e['label'] not in ('Required Accepted Private Tier Contribution',
                                       'Next Paid Tier of This Site: Public Contribution')],
        programme='Funded committee: 52 weeks. Partner capital of 0.3% of annual GDP may replace the same public contribution to the next paid tier.',
        description='Place the sponsored site\'s security and investment accounts under a funded committee. Administrative coordination lowers its existing security bill. An accepting partner may co-finance a later building stage; the committee itself provides no construction capital.')

    fid = 'ISR2_mafdal_regularise_sites'
    heading = 'With the Funded Committee and Partner Capital: Replaces the 1.4% Public Price'
    adapted[fid] = dict(effects=deepcopy(catalogue[fid]['effects']) + [
        dict(label='Treasury', value='-1.1% of annual GDP', tone='cost', heading=heading),
        dict(label='Partner Project Capital', value='-0.3% of annual GDP', tone='cost', heading=heading)])

    fid = 'ISR2_liberal_hotel_credit'
    adapted[fid] = dict(
        effects=[deepcopy(e) for e in catalogue[fid]['effects']
                 if e['label'] not in ('Required Accepted Private Resort Capital',
                                       'First Guaranteed Resort: Public Financing Share')],
        requirements=['Independent Liberals is in Power.',
                      'Accepted partner project capital of at least 0.6% of annual GDP is available.'],
        programme='Hotel guarantee book: 104 weeks. Partner capital is drawn when a resort is funded.',
        description='Use a limited public guarantee to support a resort financed jointly with an accepting partner. Its capital is drawn when construction is funded. The Treasury maintains a reserve and pays administration while carrying the insured liability.')
    for slug in ('liberal_sinai_resort', 'liberal_coastal_resort'):
        fid = 'ISR2_' + slug
        rows = deepcopy(catalogue[fid]['effects'])
        rows.insert(1, dict(label='Partner Project Capital', value='-0.6% of annual GDP', tone='cost'))
        adapted[fid] = dict(effects=rows, requirements=deepcopy(catalogue[fid]['requirements']) + [
            'The funded hotel guarantee book has an unused resort commitment.',
            'Accepted partner project capital of at least 0.6% of annual GDP is available.'])
    return adapted


STATE_PROFILES = {
    208: dict(resistance_target=.15, required_garrison_factor=.40,
              resistance_damage_to_garrison=.20, local_factories=-.15),
    209: dict(resistance_target=.25, required_garrison_factor=.60,
              resistance_damage_to_garrison=.35, local_factories=-.20),
    213: dict(resistance_target=.05, required_garrison_factor=.20,
              local_supplies_for_controller=-.12, local_factories=-.10),
    587: dict(resistance_target=.08, required_garrison_factor=.25,
              local_supplies_for_controller=-.05, local_factories=-.10),
}
COUNTRY_PROFILES = {
    208: dict(police_cost_multiplier_modifier=.05, bureaucracy_cost_multiplier_modifier=.03,
              personnel_cost_multiplier_modifier=.02),
    209: dict(police_cost_multiplier_modifier=.08, bureaucracy_cost_multiplier_modifier=.04,
              personnel_cost_multiplier_modifier=.03),
    213: dict(police_cost_multiplier_modifier=.02, bureaucracy_cost_multiplier_modifier=.03,
              personnel_cost_multiplier_modifier=.08),
    587: dict(police_cost_multiplier_modifier=.02, bureaucracy_cost_multiplier_modifier=.02,
              personnel_cost_multiplier_modifier=.05),
}
EXTRA = {'ISR2_labor_yanai', 'ISR2_labor_valley', 'ISR2_gahal_settler_entitlement',
         'ISR2_mafdal_activist_current', 'ISR2_mafdal_regularise_sites',
         'ISR2_mafdal_land_westbank', 'ISR2_mafdal_land_gaza',
         'ISR2_mafdal_land_committee', 'ISR2_mafdal_restrain_sites',
         'ISR2_liberal_sinai_resort', 'ISR2_liberal_hotel_credit', 'ISR2_liberal_coastal_resort',
         'ISR2_labor_permit_market', 'ISR2_labor_functional_rule', 'ISR2_mafdal_planning_appeals'}


def block(key, body):
    return key + ' = {\n' + indent(body.strip(), '\t') + '\n}'


def num(value):
    return f'{value:.5f}'.rstrip('0').rstrip('.') or '0'


def var(name, value):
    return f'set_variable = {{ {name} = {value} }}'


def add(name, value):
    return f'add_to_variable = {{ {name} = {value} }}'


def mul(name, value):
    return f'multiply_variable = {{ {name} = {num(value)} }}'


def if_(guard, body, other=''):
    value = block('if', block('limit', guard) + '\n' + body)
    return value + ('\n' + block('else', other) if other else '')


def pay(value):
    return (f'set_temp_variable = {{ treasury_change = {value} }}\n'
            'multiply_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes')


def receive(value):
    return f'set_temp_variable = {{ treasury_change = {value} }}\nmodify_treasury_effect = yes'


def controlled(state):
    return (f'controls_state = {state}\nhas_full_control_of_state = {state}\n'
            f'{state} = {{ owner = {{ exists = yes }} }}')


def build(data):
    """Return complete territorial actions and their provider files."""
    nodes = {n['id']: n for n in data['nodes']}
    groups = {g['id']: g for g in data['groups']}
    mine = [n for n in data['nodes'] if
            (n['group'] == 'territories' and n['id'] != 'ISR2_negotiated_terms') or n['id'] in EXTRA]
    effects, triggers, dynamic, ideas, loc, actions = {}, {}, {}, {}, {}, {}
    # The shared read-only Clausewitz parser preserves the actual condition
    # operators while replacing only internal presentation with readable labels.
    tools_path = str(Path(__file__).resolve().parents[1])
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
    from focus_prerequisite_ui import nodes as parse_conditions, field
    requirement_keys = {}
    tick, init, reopen, project_quotes = [], [], [], []
    names = {v: k for k, v in AREAS.items()}
    rates = set()

    def effect(name, body):
        key = 'ISR2_territories_' + name
        assert key not in effects, key
        effects[key] = body
        return key + ' = yes'

    def modifier(name, title, mods, enable='ISR2_is_scenario = yes', state=False):
        key = 'ISR2_territories_' + name
        assert key not in dynamic, key
        dynamic[key] = block(key, 'icon = GFX_idea_political_establishment\n' +
            block('enable', enable) + '\n' + '\n'.join(k + ' = ' + num(v) for k, v in mods.items()))
        loc[key] = title
        return key

    def shown(text):
        if '||' in text:
            return '\n'.join(shown(part.strip()) for part in text.split('||'))
        key = 'ISR2_territories_numeric_' + str(len([k for k in loc if k.startswith('ISR2_territories_numeric_')]))
        loc[key] = text
        return 'custom_effect_tooltip = ' + key

    def mod_rows(mods, heading=None):
        labels = {'offices_productivity': 'Office Productivity', 'agricolture_productivity_modifier': 'Agricultural Productivity',
            'police_cost_multiplier_modifier': 'Police Cost', 'bureaucracy_cost_multiplier_modifier': 'Bureaucracy Cost',
            'personnel_cost_multiplier_modifier': 'Personnel Cost', 'stability_factor': 'Stability',
            'local_factories': 'Local Factory Access', 'local_supplies_for_controller': 'Local Supplies',
            'resistance_target': 'Resistance Target', 'required_garrison_factor': 'Local Garrison Requirement',
            'state_production_speed_infrastructure_factor': 'Infrastructure Construction Speed'}
        rows = [shown('§Y' + heading + '§!')] if heading else []
        inverse = {'resistance_target', 'required_garrison_factor', 'resistance_damage_to_garrison'}
        for key, value in mods.items():
            tooltip = 'ISR2_territories_display_' + key + '_tt'
            fmt = '-=' if key.endswith('_cost_multiplier_modifier') or key in inverse else '+='
            loc[tooltip] = labels.get(key, key) + ': $RIGHT|' + fmt + '%1$'
            rows.append('add_to_variable = { ISR2_territories_preview_' + key + ' = ' + num(value) + ' tooltip = ' + tooltip + ' }')
        return '\n'.join(rows)

    pressure_mods = {'offices_productivity': -.04, 'bureaucracy_cost_multiplier_modifier': .04, 'stability_factor': -.02}

    def quote(rate):
        rates.add(rate)
        return 'ISR2_territories_cost_' + num(rate).replace('.', '_')

    def native_pay(rate):
        return pay(quote(rate))

    def support_payment(price_var):
        return '\n'.join([var('ISR2_project_cost', price_var), var('ISR2_project_class', 2),
            var('ISR2_project_quote', 'gdp_total'), var('ISR2_project_procurement', 0), 'ISR2_project_support_commit = yes',
            pay('ISR2_project_net_cost')])

    def project_preview(n, rate, insurance=False, committee=False):
        """A no-consumption price quote for this exact prospective focus."""
        output = 'ISR2_territories_preview_cost_' + n['id'][5:]
        body = var('ISR2_territories_preview_public_price', 'gdp_total') + '\n' + mul('ISR2_territories_preview_public_price', rate)
        if insurance:
            body += '\n' + var('ISR2_private_required', 'gdp_total') + '\n' + mul('ISR2_private_required', .005)
            body += '\n' + if_('has_country_flag = ISR2_territories_yanai_term\nwestern_social_democrats_are_in_power = yes\ncheck_variable = { ISR2_territories_yanai_used < 2 }\nISR2_private_ready = yes',
                var('ISR2_territories_preview_public_price', 'gdp_total') + '\n' + mul('ISR2_territories_preview_public_price', .01))
        if committee:
            body += '\n' + var('ISR2_private_required', 'gdp_total') + '\n' + mul('ISR2_private_required', .003)
            body += '\n' + if_('has_country_flag = ISR2_territories_committee_term\nNOT = { has_country_flag = ISR2_territories_committee_match_used }\nISR2_private_ready = yes',
                var('ISR2_territories_preview_public_price', 'gdp_total') + '\n' + mul('ISR2_territories_preview_public_price', rate-.003))
        body += '\n' + var('ISR2_project_cost', 'ISR2_territories_preview_public_price')
        body += '\n' + var('ISR2_project_class', 2) + '\n' + var('ISR2_project_quote', 'gdp_total')
        body += '\n' + var('ISR2_project_procurement', 0)
        body += '\nISR2_project_support_quote = yes\n' + var(output, 'ISR2_project_net_cost')
        project_quotes.append(effect('quote_' + n['id'][5:], body))
        return pay(output)

    def party(n):
        return (groups[n['group']]['runtime_party_trigger'] + ' = yes'
                if groups[n['group']]['kind'] == 'party' else '')

    def visible_conditions(n, eligibility, repeat):
        def raw(row):
            return block(row.key, '\n'.join(raw(c) for c in row.children())) if row.children() else row.key + ' ' + row.op + ' ' + str(row.value)

        def requirement(text, condition):
            signature = (text, condition)
            if signature not in requirement_keys:
                key = 'ISR2_territories_requirement_' + str(len(requirement_keys))
                requirement_keys[signature] = key
                loc[key] = text
            return block('custom_trigger_tooltip', 'tooltip = ' + requirement_keys[signature] + '\n' + condition)

        def flag_label(flag, negated=False):
            if flag.startswith('ISR2_territories_cooldown_'):
                return 'The 26-week appropriation cooldown has ended.' if negated else 'The 26-week appropriation cooldown is active.'
            if flag.startswith('ISR2_territories_foreign_'):
                state = int(flag.rsplit('_', 1)[1])
                return ('No foreign foothold funding is already assigned to ' if negated else 'Foreign foothold funding is assigned to ') + names[state] + '.'
            if flag == 'ISR2_territories_freeze_parliament':
                return 'No parliamentary settlement freeze is already active.' if negated else 'A parliamentary settlement freeze is in force.'
            if flag == 'ISR2_territories_freeze_mafdal':
                return 'No unrescinded Mafdal commitment restriction remains.' if negated else 'Mafdal\'s commitment restriction has not been rescinded.'
            if flag == 'ISR2_territories_hotel_term':
                return 'The 104-week hotel investment guarantee is active.'
            if flag == 'ISR2_hotel_resort_committed':
                return 'The first guaranteed resort has not already been funded.' if negated else 'The first guaranteed resort has been funded.'
            if flag == 'ISR2_territories_done_mafdal_activist_current':
                return 'The sponsored West Bank site has received its initial funding.'
            raise AssertionError(('Unlabelled territorial requirement', n['id'], flag))

        def show(row, state=None):
            key, children = row.key, row.children()
            if key in ('owner',):
                assert state is not None
                return requirement('The owner of ' + ({205: 'Haifa', 206: 'the Negev'} | names)[state] + ' exists.', raw(row))
            if key == 'controller':
                assert state is not None
                return requirement('An existing government controls ' + names[state] + '.', raw(row))
            if key == 'NOT' and len(children) == 1 and children[0].key == 'ISR2_territories_no_new_starts':
                return requirement('New settlement appropriations are permitted.', raw(row))
            if key == 'NOT' and len(children) == 1 and children[0].key == 'has_country_flag':
                return requirement(flag_label(children[0].value, True), raw(row))
            if key == 'has_country_flag':
                return requirement(flag_label(row.value), raw(row))
            if key == 'check_variable':
                named = field(children, 'var')
                if named and str(named).startswith('building_level@'):
                    assert state is not None
                    kind = named.split('@', 1)[1]
                    cap = {'agriculture_district': 10, 'offices': 50, 'infrastructure': 6}[kind]
                    quantity = cap - int(field(children, 'value'))
                    return requirement('Room for §Y' + str(quantity) + '§! additional $' + kind + '$ ' + ('level' if quantity == 1 else 'levels') + ' in ' +
                        ({205: 'Haifa', 206: 'the Negev'} | names)[state] + '.', raw(row))
                if named == 'ISR2_private_available':
                    price_var = field(children, 'value')
                    assert price_var == 'ISR2_territories_cost_0_006', (n['id'], price_var)
                    return requirement('Accepted external project capital covers §Y0.6%§! of annual GDP.', raw(row))
                assert not named, ('Unlabelled variable requirement', n['id'], named)
                test = children[0]
                if test.key.startswith('ISR2_territories_tiers_'):
                    area = names[int(test.key.rsplit('_', 1)[1])]
                    label = ('Fewer than §Y3§! paid controlled settlement tiers in ' + area + '.'
                             if test.op == '<' else 'A paid controlled settlement tier exists in ' + area + '.')
                    return requirement(label, raw(row))
                if test.key == 'ISR2_territories_foreign_count':
                    label = ('Fewer than §Y2§! areas are assigned foreign foothold funding.' if test.op == '<'
                             else 'At least one area is assigned foreign foothold funding.')
                    return requirement(label, raw(row))
                raise AssertionError(('Unlabelled direct variable requirement', n['id'], test.key))
            if key == 'free_building_slots':
                assert state is not None
                size = next(c for c in children if c.key == 'size')
                quantity = int(size.value) + 1
                return requirement('Room for §Y' + str(quantity) + '§! additional $bunker$ ' +
                    ('level' if quantity == 1 else 'levels') + ' in the selected ' + names[state] + ' province.', raw(row))
            if children:
                result = [show(c, int(key) if key.isdigit() else state) for c in children]
                result = [c for c in result if c]
                return block(key, '\n'.join(result)) if result else ''
            return raw(row)

        shown_conditions = [show(row) for row in parse_conditions(eligibility)]
        if repeat:
            cooldown = 'ISR2_territories_cooldown_' + n['id'][5:]
            shown_conditions.append(requirement(flag_label(cooldown, True), 'NOT = { has_country_flag = ' + cooldown + ' }'))
        return '\n'.join(value for value in shown_conditions if value)

    def action(n, eligibility, body, preview, repeat=False, success_guard=''):
        key = n['id'][5:]
        receipt = 'ISR2_territories_done_' + key
        cooldown = 'ISR2_territories_cooldown_' + key
        guard = '\n'.join(x for x in ['ISR2_is_scenario = yes', 'has_variable = gdp_total',
            'check_variable = { gdp_total > 0 }', party(n), eligibility,
            f'NOT = {{ has_country_flag = {cooldown} }}' if repeat else
            f'NOT = {{ has_country_flag = {receipt} }}'] if x)
        # Recheck all material guards in the transaction, including actual party.
        completion = 'ISR2_territories_refresh_prices = yes\n' + body
        receipt_effect = 'set_country_flag = ' + receipt
        if repeat:
            receipt_effect += '\nset_country_flag = { flag = ' + cooldown + ' days = 182 value = 1 }'
        if success_guard:
            completion += '\n' + if_(success_guard, receipt_effect, block('uncomplete_national_focus',
                'focus = ' + n['id'] + '\nuncomplete_children = no\nrefund_political_power = no'))
        else:
            completion += '\n' + receipt_effect
        completion += '\nISR2_territories_refresh = yes\nupdate_money_dirty_variable = yes'
        reopen_invalid = block('uncomplete_national_focus',
            'focus = ' + n['id'] + '\nuncomplete_children = no\nrefund_political_power = no')
        call = effect('complete_' + key, if_('ISR2_is_scenario = yes\nhas_variable = gdp_total\ncheck_variable = { gdp_total > 0 }',
            'ISR2_private_recalculate = yes\nISR2_territories_refresh_prices = yes\n' + if_(guard, completion, reopen_invalid), reopen_invalid))
        actions[n['id']] = dict(available=guard, visible_available=visible_conditions(n, eligibility, repeat), reward=call, preview=preview)
        if repeat:
            reset_guard = f'has_completed_focus = {n["id"]}\nNOT = {{ has_country_flag = {cooldown} }}'
            if n.get('settlement_action') == 'foreign_foothold':
                reset_guard += f'\nNOT = {{ has_country_flag = ISR2_territories_foreign_{AREAS[n["settlement_area"]]} }}'
            if n.get('settlement_action') == 'controlled_development':
                reset_guard += f'\ncheck_variable = {{ ISR2_territories_tiers_{AREAS[n["settlement_area"]]} < 3 }}'
            reopen.append(if_(reset_guard, block('uncomplete_national_focus',
                'focus = ' + n['id'] + '\nuncomplete_children = no\nrefund_political_power = no')))
        return receipt

    def enable_country_mod(key, guard):
        return if_(guard, if_('NOT = { has_dynamic_modifier = { modifier = ' + key + ' } }',
            'add_dynamic_modifier = { modifier = ' + key + ' }\nupdate_money_dirty_variable = yes'),
            if_('has_dynamic_modifier = { modifier = ' + key + ' }',
                'remove_dynamic_modifier = { modifier = ' + key + ' }\nupdate_money_dirty_variable = yes'))

    def enable_state_mod(state, key):
        return block(str(state), if_('NOT = { has_dynamic_modifier = { modifier = ' + key + ' scope = ISR } }',
            'add_dynamic_modifier = { modifier = ' + key + ' scope = ISR }'))

    def cost_stream(rate, quote_var, guard, discount=True):
        body = var('ISR2_territories_stream', quote_var) + '\n' + mul('ISR2_territories_stream', rate)
        if discount:
            body += '\n' + if_('has_country_flag = ISR2_territories_freeze_parliament', mul('ISR2_territories_stream', .8))
        body += '\n' + add('ISR2_territories_weekly_expense', 'ISR2_territories_stream')
        return if_(guard, body)

    def capacity(state, buildings):
        checks = [controlled(state)]
        caps = {'agriculture_district': 10, 'offices': 50, 'infrastructure': 6}
        staff = {'agriculture_district': 'can_staff_an_agriculture_district', 'offices': 'can_staff_an_offices'}
        for kind, levels in buildings.items():
            if kind == 'bunker':
                checks.append(f'{state} = {{ free_building_slots = {{ building = bunker size > {levels-1} province = {PROVINCES[state]} }} }}')
            else:
                checks.append(f'{state} = {{ check_variable = {{ var = building_level@{kind} value = {caps[kind]-levels} compare = less_than_or_equals }} }}')
            if kind in staff:
                checks.append(staff[kind] + ' = yes')
        return '\n'.join(checks)

    def buildings(state, package):
        commands = [f'add_extra_state_shared_building_slots = {sum(package.values())}']
        for kind, levels in package.items():
            province = f' province = {{ id = {PROVINCES[state]} }}' if kind == 'bunker' else ''
            commands.append(f'add_building_construction = {{ type = {kind} level = {levels} instant_build = yes{province} }}')
        return block(str(state), '\n'.join(commands))

    def site_modifiers(n, state, country_mods, local_mods):
        receipt = 'ISR2_territories_done_' + n['id'][5:]
        guard = f'has_country_flag = {receipt}\ncontrols_state = {state}'
        preview = []
        if country_mods:
            key = modifier(n['id'][5:] + '_budget', n['label'] + ': Security Establishment', country_mods,
                'ISR2_is_scenario = yes\n' + guard)
            tick.append(enable_country_mod(key, guard))
            preview.append('add_dynamic_modifier = { modifier = ' + key + ' }')
        if local_mods:
            key = modifier(n['id'][5:] + '_local', n['label'], local_mods,
                f'{state} = {{ is_controlled_by = ISR }}\nISR = {{ ISR2_is_scenario = yes has_country_flag = {receipt} }}', state=True)
            tick.append(enable_state_mod(state, key))
            preview.append(block(str(state), 'add_dynamic_modifier = { modifier = ' + key + ' scope = ISR }'))
        return '\n'.join(preview)

    # Four expensive occupation profiles precede any player investment.
    for state in AREAS.values():
        label = names[state]
        local = modifier(f'occupation_{state}_local', label + ': Military Administration', STATE_PROFILES[state],
            f'{state} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}\nISR = {{ ISR2_is_scenario = yes }}', state=True)
        national = modifier(f'occupation_{state}_budget', label + ': Administration and Security Budget', COUNTRY_PROFILES[state],
            f'ISR2_is_scenario = yes\ncontrols_state = {state}\n{state} = {{ NOT = {{ is_core_of = ISR }} }}')
        tick += [enable_state_mod(state, local), enable_country_mod(national,
            f'controls_state = {state}\n{state} = {{ NOT = {{ is_core_of = ISR }} }}')]
        resistance, compliance = {208: (18, 25), 209: (25, 15), 213: (8, 30), 587: (10, 20)}[state]
        init.append(if_(f'date < 1970.2.1\ncontrols_state = {state}\n{state} = {{ NOT = {{ is_core_of = ISR }} }}',
            block(str(state), if_('NOT = { has_resistance = yes }', 'start_resistance = ' + OCCUPIERS[state]) +
                f'\nset_resistance = {resistance}\nset_compliance = {compliance}')))

    # Actual local factories carry the income; their paid security remains too.
    nahal_country, nahal_local = {}, {}
    for state in AREAS.values():
        for tier in range(1, 4):
            guard = f'controls_state = {state}\ncheck_variable = {{ ISR2_territories_nahal_{state} > {tier-1} }}'
            c = modifier(f'nahal_{state}_{tier}_budget', names[state] + ': Nahal Security Establishment',
                {'police_cost_multiplier_modifier': .03, 'personnel_cost_multiplier_modifier': .02},
                'ISR2_is_scenario = yes\n' + guard)
            s = modifier(f'nahal_{state}_{tier}_local', names[state] + ': Nahal Site Protection',
                {'required_garrison_factor': .10},
                f'{state} = {{ is_controlled_by = ISR }}\nISR = {{ ISR2_is_scenario = yes check_variable = {{ ISR2_territories_nahal_{state} > {tier-1} }} }}', state=True)
            tick += [enable_country_mod(c, guard), enable_state_mod(state, s)]
            nahal_country[state, tier] = c; nahal_local[state, tier] = s

    # Foreign programmes bind mirrored costs to the actual controller.
    foreign_count = []
    for state in AREAS.values():
        active = f'has_country_flag = ISR2_territories_foreign_{state}\nNOT = {{ controls_state = {state} }}'
        country_enable = 'ISR2_is_scenario = yes\n' + active
        home = modifier(f'foreign_{state}_israel', names[state] + ' Public Settlement Sponsorship',
            {'offices_productivity': .04, 'agricolture_productivity_modifier': .03}, country_enable)
        network = modifier(f'foreign_{state}_network', names[state] + ': External Support Network',
            {'offices_productivity': .02}, country_enable + '\nhas_country_flag = ISR2_territories_network')
        host = modifier(f'foreign_{state}_host', names[state] + ': Unilateral Settlement Burden',
            {'agricolture_productivity_modifier': -.03, 'police_cost_multiplier_modifier': .04,
             'bureaucracy_cost_multiplier_modifier': .03},
            f'NOT = {{ tag = ISR }}\ncontrols_state = {state}\nISR = {{ exists = yes ISR2_is_scenario = yes has_country_flag = ISR2_territories_foreign_{state} }}')
        local = modifier(f'foreign_{state}_local', names[state] + ': Contested Settlement Presence',
            {'local_factories': -.05, 'local_supplies_for_controller': -.08},
            f'{state} = {{ NOT = {{ is_controlled_by = ISR }} }}\nISR = {{ exists = yes ISR2_is_scenario = yes has_country_flag = ISR2_territories_foreign_{state} }}', state=True)
        tick += [enable_country_mod(home, active),
            enable_country_mod(network, active + '\nhas_country_flag = ISR2_territories_network'),
            enable_state_mod(state, local),
            block(str(state), block('controller', if_('NOT = { tag = ISR }\nexists = yes\nISR = { has_country_flag = ISR2_territories_foreign_' + str(state) + ' }',
                if_('NOT = { has_dynamic_modifier = { modifier = ' + host + ' } }',
                    'add_dynamic_modifier = { modifier = ' + host + ' }\nupdate_money_dirty_variable = yes'))))]
        foreign_count.append(if_(f'has_country_flag = ISR2_territories_foreign_{state}',
            add('ISR2_territories_foreign_count', 1)))
        tick.append(cost_stream(.00015, f'ISR2_territories_foreign_quote_{state}', active))
        tick.append(cost_stream(.00005, f'ISR2_territories_foreign_quote_{state}',
            active + '\nhas_country_flag = ISR2_territories_network'))

    triggers['ISR2_territories_no_new_starts'] = ('OR = { has_country_flag = ISR2_territories_freeze_parliament '
        'AND = { has_country_flag = ISR2_territories_freeze_mafdal western_autocrats_are_in_power = yes } }')
    no_freeze = 'NOT = { ISR2_territories_no_new_starts = yes }'
    for n in mine:
        kind = n.get('settlement_action')
        if kind not in ['foreign_foothold', 'end_sponsorship', 'controlled_development']:
            continue
        state = AREAS[n['settlement_area']]
        if kind == 'foreign_foothold':
            guard = (f'NOT = {{ controls_state = {state} }}\n{state} = {{ controller = {{ exists = yes }} }}\n'
                f'NOT = {{ has_country_flag = ISR2_territories_foreign_{state} }}\n'
                'check_variable = { ISR2_territories_foreign_count < 2 }\n' + no_freeze)
            body = native_pay(.01) + '\n' + var(f'ISR2_territories_foreign_quote_{state}', 'gdp_total')
            body += f'\nset_country_flag = ISR2_territories_foreign_{state}'
            preview = native_pay(.01) + '\n' + shown('Foothold Funding: §R-0.015%§! of annual GDP per week.')
            preview += '\nadd_dynamic_modifier = { modifier = ISR2_territories_foreign_' + str(state) + '_israel }'
            preview += '\n' + mod_rows({'agricolture_productivity_modifier': -.03, 'police_cost_multiplier_modifier': .04,
                'bureaucracy_cost_multiplier_modifier': .03}, 'Actual Host')
            preview += '\n' + block(str(state), f'add_dynamic_modifier = {{ modifier = ISR2_territories_foreign_{state}_local scope = ISR }}')
            if state in (208, 209):
                preview += '\n' + mod_rows(pressure_mods, 'Palestine: New Pressure Tier')
            action(n, guard, body, preview, repeat=True)
        elif kind == 'end_sponsorship':
            guard = f'has_country_flag = ISR2_territories_foreign_{state}\nNOT = {{ controls_state = {state} }}'
            body = f'clr_country_flag = ISR2_territories_foreign_{state}'
            preview = f'remove_dynamic_modifier = {{ modifier = ISR2_territories_foreign_{state}_israel }}\n'
            preview += mod_rows({'offices_productivity': -.04, 'agricolture_productivity_modifier': -.03}, 'Israel')
            preview += '\n' + mod_rows({'offices_productivity': -.02}, 'Additional Removal with the Funded Network')
            preview += '\n' + shown('Weekly Foothold Expense Removed: §G+0.015%§! of quoted GDP, or §G+0.012%§! with the maintenance discount.')
            preview += '\n' + shown('Network Supplement Removed if Active: §G+0.005%§! of quoted GDP per week, or §G+0.004%§! with the maintenance discount.')
            preview += '\n' + block(str(state), 'remove_dynamic_modifier = { modifier = ISR2_territories_foreign_' + str(state) + '_local scope = ISR }')
            preview += '\n' + block(str(state), block('controller', f'remove_dynamic_modifier = {{ modifier = ISR2_territories_foreign_{state}_host }}'))
            preview += '\n' + mod_rows({'agricolture_productivity_modifier': .03, 'police_cost_multiplier_modifier': -.04,
                'bureaucracy_cost_multiplier_modifier': -.03}, 'Actual Host')
            preview += '\n' + mod_rows({'local_factories': .05, 'local_supplies_for_controller': .08}, names[state])
            if state in (208, 209):
                preview += '\n' + mod_rows({k: -v for k, v in pressure_mods.items()}, 'Palestine: Removed Pressure Tier')
            action(n, guard, body, preview, repeat=True)
        else:
            package = {'agriculture_district': 1, 'infrastructure': 1, 'bunker': 1}
            guard = capacity(state, package) + f'\ncheck_variable = {{ ISR2_territories_tiers_{state} < 3 }}\n' + no_freeze
            body = var('ISR2_territories_project_quote', 'gdp_total')
            body += '\n' + var('ISR2_territories_project_price', 'gdp_total') + '\n' + mul('ISR2_territories_project_price', .015)
            # Insurance discounts are genuine co-financing, never free grants.
            insured = ('has_country_flag = ISR2_territories_yanai_term\nwestern_social_democrats_are_in_power = yes\n'
                'check_variable = { ISR2_territories_yanai_used < 2 }\nISR2_private_ready = yes')
            body += '\n' + var('ISR2_private_required', 'ISR2_territories_project_quote') + '\n' + mul('ISR2_private_required', .005)
            private = 'ISR2_private_commit = yes\n' + if_(
                'check_variable = { var = ISR2_private_paid value = ISR2_private_required compare = greater_than_or_equals }',
                var('ISR2_territories_project_price', 'ISR2_territories_project_quote') + '\n' + mul('ISR2_territories_project_price', .01) + '\n' +
                add('ISR2_territories_yanai_used', 1) + '\n' +
                '\n'.join(if_(f'check_variable = {{ ISR2_territories_yanai_used = {slot} }}',
                    var(f'ISR2_territories_yanai_state_{slot}', state) + '\n' +
                    '\n'.join(var(f'ISR2_territories_yanai_{tag}_{slot}', 'ISR2_private_paid_' + tag)
                        for tag in ('USA', 'GER', 'ROM'))) for slot in (1, 2)))
            body += '\n' + if_(insured, private)
            body += '\n' + support_payment('ISR2_territories_project_price') + '\n' + buildings(state, package)
            body += '\n' + add(f'ISR2_territories_tiers_{state}', 1) + '\n' + add(f'ISR2_territories_nahal_{state}', 1)
            preview = project_preview(n, .015, insurance=True) + '\n' + buildings(state, package)
            preview += '\nadd_dynamic_modifier = { modifier = ' + nahal_country[state, 1] + ' }'
            preview += '\n' + block(str(state), 'add_dynamic_modifier = { modifier = ' + nahal_local[state, 1] + ' scope = ISR }')
            preview += '\n' + shown('§YWith Funded Political-Risk Cover§! || Public Price: §R-1.0%§! of annual GDP. || Partner Project Capital: §R-0.5%§! of annual GDP.')
            if state in (208, 209):
                preview += '\n' + mod_rows(pressure_mods, 'Palestine: New Pressure Tier')
            action(n, guard, body, preview, repeat=True)

    # Additional party-specific physical programmes use the same area receipts.
    site_packages = {
        'ISR2_labor_valley': (208, .016, {'agriculture_district': 1, 'bunker': 2}, {}, {'resistance_target': .05, 'required_garrison_factor': .15}, .00015),
        'ISR2_gahal_settler_entitlement': (208, .021, {'agriculture_district': 1, 'offices': 1, 'infrastructure': 1}, {}, {'resistance_target': .08, 'required_garrison_factor': .20}, .0002),
        'ISR2_mafdal_activist_current': (208, .016, {'agriculture_district': 1, 'infrastructure': 1}, {}, {'resistance_target': .08, 'required_garrison_factor': .20}, .0002),
        'ISR2_mafdal_regularise_sites': (208, .014, {'agriculture_district': 1, 'infrastructure': 1}, {}, {'resistance_target': .05, 'required_garrison_factor': .10}, .00015),
        'ISR2_mafdal_land_westbank': (208, .01, {'agriculture_district': 1}, {}, {'required_garrison_factor': .05}, .00005),
        'ISR2_mafdal_land_gaza': (209, .01, {'agriculture_district': 1}, {}, {'required_garrison_factor': .05}, .00005),
    }
    for key, (state, rate, package, country_mods, local_mods, stream) in site_packages.items():
        n = nodes[key]
        is_settlement = True
        guard = capacity(state, package)
        if is_settlement:
            guard += f'\ncheck_variable = {{ ISR2_territories_tiers_{state} < 3 }}\n' + no_freeze
        if key == 'ISR2_mafdal_regularise_sites':
            guard += '\nhas_country_flag = ISR2_territories_done_mafdal_activist_current'
        preview_mod = site_modifiers(n, state, country_mods, local_mods)
        receipt = 'ISR2_territories_done_' + key[5:]
        body = var('ISR2_territories_project_price', 'gdp_total') + '\n' + mul('ISR2_territories_project_price', rate)
        if key == 'ISR2_mafdal_regularise_sites':
            # A funded committee may match the next tier with real private capital.
            rebate = var('ISR2_private_required', 'gdp_total') + '\n' + mul('ISR2_private_required', .003)
            rebate += '\n' + if_('ISR2_private_ready = yes', 'ISR2_private_commit = yes\n' + if_(
                'check_variable = { var = ISR2_private_paid value = ISR2_private_required compare = greater_than_or_equals }',
                'subtract_from_variable = { ISR2_territories_project_price = ISR2_private_paid }\n' +
                '\nset_country_flag = ISR2_territories_committee_match_used')
                )
            body += '\n' + if_('has_country_flag = ISR2_territories_committee_term\nNOT = { has_country_flag = ISR2_territories_committee_match_used }', rebate)
        body += '\n' + support_payment('ISR2_territories_project_price') + '\n' + buildings(state, package)
        body += '\n' + var('ISR2_territories_quote_' + key[5:], 'gdp_total')
        if is_settlement:
            body += '\n' + add(f'ISR2_territories_tiers_{state}', 1)
        preview = project_preview(n, rate, committee=key=='ISR2_mafdal_regularise_sites') + '\n' + buildings(state, package) + '\n' + preview_mod
        if stream:
            preview += '\n' + shown(n['label'] + ': §R-' + num(stream*100) + '%§! of annual GDP per week.')
            tick.append(cost_stream(stream, 'ISR2_territories_quote_' + key[5:],
                f'has_country_flag = {receipt}\ncontrols_state = {state}'))
        if is_settlement and state in (208, 209):
            preview += '\n' + mod_rows(pressure_mods, 'Palestine: New Pressure Tier')
        action(n, guard, body, preview)

    # Cleanup considers only countries carrying one of these four host mods.
    host_cleanup = []
    for state in AREAS.values():
        host = f'ISR2_territories_foreign_{state}_host'
        invalid = f'has_dynamic_modifier = {{ modifier = {host} }}\nOR = {{ NOT = {{ controls_state = {state} }} tag = ISR ISR = {{ NOT = {{ has_country_flag = ISR2_territories_foreign_{state} }} }} }}'
        host_cleanup.append(if_(invalid, f'remove_dynamic_modifier = {{ modifier = {host} }}\nupdate_money_dirty_variable = yes'))
    present_host = 'OR = { ' + ' '.join(f'has_dynamic_modifier = {{ modifier = ISR2_territories_foreign_{s}_host }}' for s in AREAS.values()) + ' }'
    tick.append(block('every_country', block('limit', present_host) + '\n' + '\n'.join(host_cleanup)))

    # Remaining administration and funding policies are assembled separately.
    return _finish(data, nodes, groups, mine, effects, triggers, dynamic, ideas, loc,
                   actions, tick, init, reopen, project_quotes, rates, effect, modifier, shown,
                   quote, native_pay, mod_rows, action, enable_country_mod, enable_state_mod,
                   cost_stream, no_freeze)


def _finish(data, nodes, groups, mine, effects, triggers, dynamic, ideas, loc,
            actions, tick, init, reopen, project_quotes, rates, effect, modifier, shown,
            quote, native_pay, mod_rows, action, enable_country_mod, enable_state_mod,
            cost_stream, no_freeze):
    """Complete administrative, insurance and pressure providers."""
    def party(n):
        return (groups[n['group']]['runtime_party_trigger'] + ' = yes'
                if groups[n['group']]['kind'] == 'party' else '')

    def finish_policy(key, rate, mods, *, guard='', active_guard='', body='', stream=0, period=None):
        n = nodes['ISR2_' + key]
        receipt = 'ISR2_territories_done_' + key
        active = 'has_country_flag = ' + receipt
        if party(n):
            active += '\n' + party(n)
        if active_guard:
            active += '\n' + active_guard
        if period:
            active += '\nhas_country_flag = ISR2_territories_term_' + key
            body += '\nset_country_flag = { flag = ISR2_territories_term_' + key + ' days = ' + str(period) + ' value = 1 }'
        key_mod = modifier(key, n['label'], mods, 'ISR2_is_scenario = yes\n' + active)
        tick.append(enable_country_mod(key_mod, active))
        after = native_pay(rate) if rate else ''
        after += '\n' + var('ISR2_territories_quote_' + key, 'gdp_total') + '\n' + body
        preview = (native_pay(rate) + '\n' if rate else '') + 'add_dynamic_modifier = { modifier = ' + key_mod + ' }'
        if stream:
            tick.append(cost_stream(stream, 'ISR2_territories_quote_' + key, active, discount=False))
            preview += '\n' + shown(n['label'] + ': §R-' + num(stream*100) + '%§! of annual GDP per week.')
        action(n, guard, after, preview)

    finish_policy('occupation_accounts', .0025, {'compliance_gain': .05})
    finish_policy('civil_admin', .006, {'compliance_gain': .10}, stream=.0002)
    for state in AREAS.values():
        key = modifier(f'civil_admin_{state}', 'Territorial Civil Administration',
            {'required_garrison_factor': -.10},
            f'{state} = {{ is_controlled_by = ISR }}\nISR = {{ ISR2_is_scenario = yes has_country_flag = ISR2_territories_done_civil_admin }}', state=True)
        tick.append(enable_state_mod(state, key))
        actions['ISR2_civil_admin']['preview'] += '\n' + block(str(state),
            'add_dynamic_modifier = { modifier = ' + key + ' scope = ISR }')

    for name, rate, cmods, smods, states in [
        ('labor_permit_market', .005, {'offices_productivity': .04, 'bureaucracy_cost_multiplier_modifier': .04},
         {'resistance_target': .04, 'required_garrison_factor': .05}, (208, 209)),
        ('labor_functional_rule', .006, {'offices_productivity': .05, 'police_cost_multiplier_modifier': .06,
         'bureaucracy_cost_multiplier_modifier': .04}, {'resistance_target': .06, 'required_garrison_factor': .10}, (208, 209, 213, 587)),
    ]:
        eligible = 'OR = { ' + ' '.join('AND = { controls_state = ' + str(s) + ' ' + str(s) + ' = { NOT = { is_core_of = ISR } } }' for s in states) + ' }'
        finish_policy(name, rate, cmods, guard=eligible, active_guard=eligible)
        receipt = 'ISR2_territories_done_' + name
        for state in states:
            enable = f'{state} = {{ is_controlled_by = ISR NOT = {{ is_core_of = ISR }} }}\nISR = {{ exists = yes ISR2_is_scenario = yes has_country_flag = {receipt} western_social_democrats_are_in_power = yes }}'
            m = modifier(name + '_' + str(state), nodes['ISR2_' + name]['label'], smods, enable, state=True)
            tick.append(enable_state_mod(state, m))
        actions['ISR2_' + name]['preview'] += '\n' + mod_rows(smods, 'Participating Controlled Non-Core Territory')

    # Planning has one actual state, selected in a fixed transparent priority.
    name = 'mafdal_planning_appeals'
    planning_states = (208, 209, 206, 205)
    planning_body = ''
    for state in reversed(planning_states):
        place = block(str(state), 'set_state_flag = ISR2_territories_planning_appeals')
        planning_body = if_('controls_state = ' + str(state), place, planning_body)
    finish_policy(name, .004, {'bureaucracy_cost_multiplier_modifier': .03},
        guard='OR = { ' + ' '.join('controls_state = ' + str(s) for s in planning_states) + ' }', body=planning_body)
    for state in planning_states:
        enable = f'{state} = {{ is_controlled_by = ISR has_state_flag = ISR2_territories_planning_appeals }}\nISR = {{ exists = yes ISR2_is_scenario = yes western_autocrats_are_in_power = yes }}'
        m = modifier(name + '_' + str(state), 'Municipal Infrastructure Planning',
            {'state_production_speed_infrastructure_factor': .15}, enable, state=True)
        tick.append(enable_state_mod(state, m))
    actions['ISR2_' + name]['preview'] += '\n' + mod_rows({'state_production_speed_infrastructure_factor': .15}, 'Selected Controlled State')

    # Two independent freeze sources share the same actual start restriction.
    n = nodes['ISR2_funded_network']
    action(n, 'check_variable = { ISR2_territories_foreign_count > 0 }',
        native_pay(.004) + '\nset_country_flag = ISR2_territories_network',
        native_pay(.004) + '\n' + mod_rows({'offices_productivity': .02}, 'Per Funded Foreign Foothold') +
        '\n' + shown('Weekly Cost per Funded Foothold: §R0.015% becomes 0.020%§! of quoted annual GDP.'))
    active_any = 'OR = { check_variable = { ISR2_territories_foreign_count > 0 } ' + ' '.join(
        f'check_variable = {{ ISR2_territories_tiers_{s} > 0 }}' for s in AREAS.values()) + ' }'
    action(nodes['ISR2_cap_projects'], active_any + '\nNOT = { has_country_flag = ISR2_territories_freeze_parliament }',
        'set_country_flag = ISR2_territories_freeze_parliament',
        shown('Existing Settlement Maintenance: §G-20%§!.'), repeat=True)
    mafdal_mod = modifier('mafdal_restrain_sites', 'Refusal of New Unauthorised Commitments',
        {'police_cost_multiplier_modifier': -.06, 'personnel_cost_multiplier_modifier': -.03},
        'ISR2_is_scenario = yes\nhas_country_flag = ISR2_territories_freeze_mafdal\nwestern_autocrats_are_in_power = yes')
    tick.append(enable_country_mod(mafdal_mod,
        'has_country_flag = ISR2_territories_freeze_mafdal\nwestern_autocrats_are_in_power = yes'))
    action(nodes['ISR2_mafdal_restrain_sites'], 'NOT = { has_country_flag = ISR2_territories_freeze_mafdal }',
        'set_country_flag = ISR2_territories_freeze_mafdal',
        'add_dynamic_modifier = { modifier = ' + mafdal_mod + ' }\n' + shown('New Settlement Project Starts: §RSuspended§!.'), repeat=True)
    lift_body = native_pay(.001) + '\nclr_country_flag = ISR2_territories_freeze_parliament\n'
    lift_body += 'clr_country_flag = ISR2_territories_freeze_mafdal\nremove_dynamic_modifier = { modifier = ' + mafdal_mod + ' }'
    # The old stance is reopened, without uncompleting its continuation or assets.
    lift_body += '\n' + block('uncomplete_national_focus', 'focus = ISR2_mafdal_restrain_sites\nuncomplete_children = no\nrefund_political_power = no')
    action(nodes['ISR2_lift_freeze'], 'OR = { has_country_flag = ISR2_territories_freeze_parliament has_country_flag = ISR2_territories_freeze_mafdal }',
        lift_body, native_pay(.001) + '\n' + shown('Parliamentary Maintenance Discount, if active: §R-20% becomes 0%§!.') +
        '\nremove_dynamic_modifier = { modifier = ' + mafdal_mod + ' }\n' +
        mod_rows({'police_cost_multiplier_modifier': .06, 'personnel_cost_multiplier_modifier': .03}, 'If the Mafdal Commitment Policy Is Active'), repeat=True)

    # A real temporary committee reduces its actual existing paid-site expense.
    committee_guard = 'has_country_flag = ISR2_territories_done_mafdal_activist_current\ncontrols_state = 208'
    committee_body = native_pay(.001) + '\n' + var('ISR2_territories_committee_quote', 'gdp_total')
    committee_body += '\nset_country_flag = { flag = ISR2_territories_committee_term days = 364 value = 1 }'
    committee_preview = native_pay(.001) + '\n' + shown('Sponsored Site Security Expense: §G0.020% becomes 0.016%§! of quoted GDP per week for 52 weeks.')
    committee_preview += '\n' + shown('Committee Expense: §R-0.001%§! of quoted GDP per week for 52 weeks.')
    committee_preview += '\n' + shown('§YNext Paid Tier§! || Public Price with Committed Capital: §G1.4% becomes 1.1%§! of GDP. || External Tier Contribution: §Y0.3%§! of GDP.')
    action(nodes['ISR2_mafdal_land_committee'], committee_guard, committee_body, committee_preview)
    tick.append(cost_stream(-.00004, 'ISR2_territories_quote_mafdal_activist_current',
        'has_country_flag = ISR2_territories_committee_term\ncontrols_state = 208'))
    tick.append(cost_stream(.00001, 'ISR2_territories_committee_quote',
        'has_country_flag = ISR2_territories_committee_term', discount=False))

    # Insurance holds a cash reserve, pays bounded actual losses, then returns
    # only unused reserve. Administration is spent separately, not accumulated.
    yanai_body = native_pay(.002) + '\n' + var('ISR2_territories_yanai_quote', 'gdp_total')
    yanai_body += '\n' + var('ISR2_territories_yanai_reserve', 'gdp_total') + '\n' + mul('ISR2_territories_yanai_reserve', .002)
    yanai_body += '\nset_country_flag = { flag = ISR2_territories_yanai_term days = 364 value = 1 }'
    yanai_preview = native_pay(.002) + '\n' + shown('Political-Risk Guarantee Administration: §R-0.01%§! of quoted annual GDP per week for 52 weeks.')
    yanai_preview += '\n' + shown('Guaranteed Projects: §Y2§! || Public Price per Project: §G1.5% becomes 1.0%§! of GDP. || Committed Capital per Project: §Y0.5%§! of GDP.')
    yanai_preview += '\n' + shown('Gross Maximum Insured Claim: §R1.6%§! of quoted GDP. || Cash Reserve Included: §Y0.2%§! of quoted GDP. || Maximum Additional Treasury Call: §R1.4%§! of quoted GDP.')
    action(nodes['ISR2_labor_yanai'], '', yanai_body, yanai_preview)
    tick.append(cost_stream(.0001, 'ISR2_territories_yanai_quote',
        'has_country_flag = ISR2_territories_yanai_term', discount=False))

    def claim(book, loss_guard, fraction, claim_flag, claim_id, share_prefix):
        amount = f'ISR2_territories_{book}_claim'
        gross = f'ISR2_territories_{book}_gross_claim'
        reserve = f'ISR2_territories_{book}_reserve'
        body = 'set_country_flag = ' + claim_flag + '\n' + var(amount, f'ISR2_territories_{book}_quote') + '\n' + mul(amount, fraction)
        body += '\n' + var(gross, amount)
        body += '\n' + if_(f'check_variable = {{ var = {reserve} value = {amount} compare = greater_than_or_equals }}',
            f'subtract_from_variable = {{ {reserve} = {amount} }}',
            f'subtract_from_variable = {{ {amount} = {reserve} }}\n' + var(reserve, 0) + '\n' + pay(amount))
        body += '\n' + var('ISR2_private_claim_id', claim_id) + '\n' + var('ISR2_private_claim_amount', gross)
        body += '\n' + '\n'.join(var('ISR2_private_claim_share_' + tag, share_prefix.format(tag=tag))
            for tag in ('USA', 'GER', 'ROM'))
        body += '\nISR2_private_claim_credit = yes'
        return if_(f'has_country_flag = ISR2_territories_{book}_term\nNOT = {{ has_country_flag = {claim_flag} }}\n' + loss_guard, body)

    for slot in (1, 2):
        loss = 'OR = { ' + ' '.join('AND = { check_variable = { ISR2_territories_yanai_state_' + str(slot) + ' = ' + str(s) + ' } NOT = { controls_state = ' + str(s) + ' } }' for s in AREAS.values()) + ' }'
        tick.append(claim('yanai', loss, .008, f'ISR2_territories_yanai_claimed_{slot}', slot,
            'ISR2_territories_yanai_{tag}_' + str(slot)))
    tick.append(if_('has_country_flag = ISR2_territories_done_labor_yanai\nNOT = { has_country_flag = ISR2_territories_yanai_term }\nNOT = { has_country_flag = ISR2_territories_yanai_settled }',
        'set_country_flag = ISR2_territories_yanai_settled\n' +
        var('ISR2_territories_yanai_refund', 'ISR2_territories_yanai_reserve') + '\n' +
        var('ISR2_territories_yanai_reserve', 0) + '\n' + receive('ISR2_territories_yanai_refund')))

    # One resort guarantee, shared by the two competing physical focus projects.
    hotel_required = quote(.006)
    guard = f'check_variable = {{ var = ISR2_private_available value = {hotel_required} compare = greater_than_or_equals }}'
    hotel_body = native_pay(.001) + '\n' + var('ISR2_territories_hotel_quote', 'gdp_total')
    hotel_body += '\n' + var('ISR2_territories_hotel_reserve', 'gdp_total') + '\n' + mul('ISR2_territories_hotel_reserve', .001)
    hotel_body += '\nset_country_flag = { flag = ISR2_territories_hotel_term days = 728 value = 1 }'
    hotel_preview = native_pay(.001) + '\n' + shown('Required Committed Resort Capital: §Y0.6%§! of annual GDP.')
    hotel_preview += '\n' + shown('Hotel Guarantee Administration: §R-0.003%§! of quoted GDP per week for 104 weeks.')
    hotel_preview += '\n' + shown('Gross Maximum Insured Claim: §R0.8%§! of quoted GDP. || Cash Reserve Included: §Y0.1%§! of quoted GDP. || Maximum Additional Treasury Call: §R0.7%§! of quoted GDP.')
    action(nodes['ISR2_liberal_hotel_credit'], guard, hotel_body, hotel_preview)
    tick.append(cost_stream(.00003, 'ISR2_territories_hotel_quote', 'has_country_flag = ISR2_territories_hotel_term', discount=False))
    for key, state, price, package, cmods, smods in [
        ('liberal_sinai_resort', 213, .012, {'offices': 2, 'infrastructure': 1},
         {'police_cost_multiplier_modifier': .03, 'personnel_cost_multiplier_modifier': .02},
         {'resistance_target': .05, 'required_garrison_factor': .10}),
        ('liberal_coastal_resort', 205, .009, {'offices': 1, 'infrastructure': 1},
         {'mdcw_cw_market_exposure': .05}, {}),
    ]:
        n = nodes['ISR2_' + key]
        limits = [f'controls_state = {state}', f'has_full_control_of_state = {state}',
            f'{state} = {{ owner = {{ exists = yes }} }}',
            f'{state} = {{ check_variable = {{ var = building_level@offices value = {50-package["offices"]} compare = less_than_or_equals }} }}',
            f'{state} = {{ check_variable = {{ var = building_level@infrastructure value = 5 compare = less_than_or_equals }} }}',
            'can_staff_an_offices = yes', 'has_country_flag = ISR2_territories_hotel_term',
            'NOT = { has_country_flag = ISR2_hotel_resort_committed }',
            f'check_variable = {{ var = ISR2_private_available value = {hotel_required} compare = greater_than_or_equals }}']
        if state == 205:
            limits.append('owns_state = 205')
        body = var('ISR2_private_required', 'gdp_total') + '\n' + mul('ISR2_private_required', .006)
        body += '\nISR2_private_commit = yes\n'
        build_commands = ['add_extra_state_shared_building_slots = ' + str(sum(package.values()))]
        build_commands += ['add_building_construction = { type = ' + kind + ' level = ' + str(level) + ' instant_build = yes }' for kind, level in package.items()]
        success = native_pay(price) + '\n' + block(str(state), '\n'.join(build_commands))
        success += '\nset_country_flag = ISR2_hotel_resort_committed\n' + var('ISR2_territories_hotel_state', state)
        success += '\n' + '\n'.join(var('ISR2_territories_hotel_' + tag, 'ISR2_private_paid_' + tag)
            for tag in ('USA', 'GER', 'ROM'))
        body += if_('check_variable = { var = ISR2_private_paid value = ISR2_private_required compare = greater_than_or_equals }', success)
        receipt = 'ISR2_territories_done_' + key
        modpreview = ''
        if cmods:
            m = modifier(key + '_budget', n['label'], cmods,
                f'ISR2_is_scenario = yes has_country_flag = {receipt} controls_state = {state}')
            tick.append(enable_country_mod(m, f'has_country_flag = {receipt} controls_state = {state}'))
            modpreview += '\nadd_dynamic_modifier = { modifier = ' + m + ' }'
        if smods:
            m = modifier(key + '_local', n['label'], smods,
                f'{state} = {{ is_controlled_by = ISR }}\nISR = {{ ISR2_is_scenario = yes has_country_flag = {receipt} }}', state=True)
            tick.append(enable_state_mod(state, m))
            modpreview += '\n' + block(str(state), 'add_dynamic_modifier = { modifier = ' + m + ' scope = ISR }')
        preview = native_pay(price) + '\n' + shown('Partner Project Capital: §R-0.6%§! of annual GDP.') + '\n' + block(str(state), '\n'.join(build_commands)) + modpreview
        action(n, '\n'.join(limits), body, preview, success_guard='has_country_flag = ISR2_hotel_resort_committed')
    hotel_loss = 'has_country_flag = ISR2_hotel_resort_committed\nOR = { AND = { check_variable = { ISR2_territories_hotel_state = 213 } NOT = { controls_state = 213 } } AND = { check_variable = { ISR2_territories_hotel_state = 205 } NOT = { controls_state = 205 } } }'
    tick.append(claim('hotel', hotel_loss, .008, 'ISR2_territories_hotel_claimed', 3,
        'ISR2_territories_hotel_{tag}'))
    tick.append(if_('has_country_flag = ISR2_territories_done_liberal_hotel_credit\nNOT = { has_country_flag = ISR2_territories_hotel_term }\nNOT = { has_country_flag = ISR2_territories_hotel_settled }',
        'set_country_flag = ISR2_territories_hotel_settled\n' +
        var('ISR2_territories_hotel_refund', 'ISR2_territories_hotel_reserve') + '\n' +
        var('ISR2_territories_hotel_reserve', 0) + '\n' + receive('ISR2_territories_hotel_refund')))

    # PAL pressure has four bounded native increments. Inputs are raw pressure
    # before relief, allowing bilateral selector logic to choose the actual area.
    pressure = []
    for state in (208, 209):
        raw = f'ISR2_territories_pressure_{state}'
        effective = f'ISR2_territories_effective_pressure_{state}'
        p = var(raw, 0)
        eligible = f'PAL = {{ exists = yes }}\n{state} = {{ is_core_of = PAL }}'
        p += '\n' + if_(eligible, if_(f'controls_state = {state}',
            var(raw, f'ISR2_territories_tiers_{state}'),
            if_(f'has_country_flag = ISR2_territories_foreign_{state}', var(raw, 1))))
        p += '\n' + if_(f'check_variable = {{ {raw} > 2 }}', var(raw, 2))
        p += '\n' + var(effective, raw)
        p += '\n' + if_(f'has_country_flag = ISR2_pal_service_relief_active\ncheck_variable = {{ ISR2_pal_service_relief_state = {state} }}\ncheck_variable = {{ {effective} > 1 }}', var(effective, 1))
        pressure.append(p)
    pressure.append(var('ISR2_territories_effective_pressure_total', 'ISR2_territories_effective_pressure_208'))
    pressure.append(add('ISR2_territories_effective_pressure_total', 'ISR2_territories_effective_pressure_209'))
    for tier in range(1, 5):
        m = modifier('pal_pressure_' + str(tier), 'Palestinian Institutional Pressure',
            {'offices_productivity': -.04, 'bureaucracy_cost_multiplier_modifier': .04, 'stability_factor': -.02},
            'tag = PAL\nISR = { exists = yes ISR2_is_scenario = yes check_variable = { ISR2_territories_effective_pressure_total > ' + str(tier-1) + ' } }')
        pressure.append(block('PAL', if_('exists = yes', enable_country_mod(m,
            'ISR = { check_variable = { ISR2_territories_effective_pressure_total > ' + str(tier-1) + ' } }'))))
    effects['ISR2_territories_pressure_reconcile'] = '\n'.join(pressure)

    # Native weekly amounts are recomputed, never compounded. Cash/principal
    # transactions above are separate from the weekly MD budget contribution.
    price_body = []
    for rate in sorted(rates):
        price_body += [var(quote(rate), 'gdp_total'), mul(quote(rate), rate)]
    effects['ISR2_territories_refresh_prices'] = '\n'.join(price_body)
    foreign_count_body = var('ISR2_territories_foreign_count', 0) + '\n' + '\n'.join(
        if_(f'has_country_flag = ISR2_territories_foreign_{s}', add('ISR2_territories_foreign_count', 1))
        for s in AREAS.values())
    daily = 'ISR2_private_recalculate = yes\nISR2_territories_refresh_prices = yes\n' + '\n'.join(project_quotes) + '\n' + foreign_count_body
    daily += '\n' + var('ISR2_territories_previous_weekly_expense', 'ISR2_territories_weekly_expense')
    daily += '\n' + var('ISR2_territories_weekly_income', 0) + '\n' + var('ISR2_territories_weekly_expense', 0)
    daily += '\n' + '\n'.join(tick) + '\nISR2_territories_pressure_reconcile = yes\n' + '\n'.join(reopen)
    daily += '\n' + if_('NOT = { check_variable = { ISR2_territories_weekly_expense = ISR2_territories_previous_weekly_expense } }',
        'update_money_dirty_variable = yes')
    effects['ISR2_territories_refresh'] = if_('ISR2_is_scenario = yes', daily)
    effects['ISR2_territories_daily'] = 'ISR2_territories_refresh = yes'
    initialized_vars = ['foreign_count', 'weekly_income', 'weekly_expense', 'previous_weekly_expense',
        'yanai_used', 'yanai_quote', 'yanai_reserve', 'yanai_claim', 'yanai_gross_claim', 'yanai_refund',
        'hotel_quote', 'hotel_reserve', 'hotel_claim', 'hotel_gross_claim', 'hotel_refund', 'hotel_state',
        'committee_quote', 'effective_pressure_total']
    initialized_vars += [f'{kind}_{s}' for s in AREAS.values() for kind in ('tiers', 'nahal', 'foreign_quote')]
    initialized_vars += [f'{kind}_{s}' for s in (208, 209) for kind in ('pressure', 'effective_pressure')]
    initialized_vars += [f'yanai_state_{slot}' for slot in (1, 2)]
    initialized_vars += [f'yanai_{tag}_{slot}' for slot in (1, 2) for tag in ('USA', 'GER', 'ROM')]
    initialized_vars += ['hotel_' + tag for tag in ('USA', 'GER', 'ROM')]
    initialized_vars += ['quote_' + key for key in ('labor_valley', 'gahal_settler_entitlement',
        'mafdal_activist_current', 'mafdal_regularise_sites', 'mafdal_land_westbank', 'mafdal_land_gaza')]
    initial_values = '\n'.join(var('ISR2_territories_' + key, 0) for key in initialized_vars)
    effects['ISR2_territories_init'] = if_('ISR2_is_scenario = yes\nNOT = { has_country_flag = ISR2_territories_initialized }',
        initial_values + '\n' + '\n'.join(init) + '\nset_country_flag = ISR2_territories_initialized') + '\nISR2_territories_refresh = yes'

    assert set(actions) == {n['id'] for n in mine}, (set(n['id'] for n in mine) - set(actions), set(actions) - set(n['id'] for n in mine))
    for key in dynamic:
        loc.setdefault(key + '_desc', '')
    files = {
        'common/scripted_effects/ISR2_territories_effects.txt': MARK + '\n\n'.join(block(k, v) for k, v in effects.items()) + '\n',
        'common/scripted_triggers/ISR2_territories_triggers.txt': MARK + '\n\n'.join(block(k, v) for k, v in triggers.items()) + '\n',
        'common/dynamic_modifiers/ISR2_territories_modifiers.txt': MARK + '\n\n'.join(dynamic.values()) + '\n',
    }
    return dict(files=files, actions=actions, daily='ISR2_territories_daily = yes',
                init='ISR2_territories_init = yes', refresh='ISR2_territories_refresh = yes', loc=loc,
                preview_adaptations=_preview_adaptations(data),
                metadata=dict(project='IMPERIA COLD WAR', actions=len(actions), state_ids=AREAS,
                    weekly_income='ISR2_territories_weekly_income', weekly_expense='ISR2_territories_weekly_expense',
                    private_commit='ISR2_private_commit', native_gameplay_tested=False))
