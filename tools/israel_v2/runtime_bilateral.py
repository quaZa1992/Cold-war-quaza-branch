# IMPERIA COLD WAR — Israel V2 recipient-consented contracts and real project capital.
"""Pure emitter. The root compiler owns writing every returned runtime file.

Currency is billion USD; budget contributions are positive weekly amounts.
Soviet principal/interest settlements are atomic direct weekly transactions,
and are deliberately NOT charged again through additional-expense streams.
"""
from copy import deepcopy
from decimal import Decimal

MARKER = '# IMPERIA COLD WAR — Israel V2 bilateral agreements.\n'
PARTNERS = ('ETH', 'UGA', 'KEN', 'USA', 'ROM', 'EGY', 'PER', 'PAL', 'SOV', 'JOR', 'DRC', 'TUR', 'GER')
FINANCIERS = ('USA', 'GER', 'ROM')
SANCTIONS = tuple(f'imp_{kind}_sanc_{direction}' for kind in ('dip', 'fin', 'eco', 'mil') for direction in ('on_us', 'by_us'))
COUNTRIES = dict(USA='United States', GER='West Germany', ROM='Romania')
MODIFIERS = {
    'irrigation_exports': ({}, {'agricolture_productivity_modifier': .10}, 'Precision Irrigation Contract'),
    'mashav': ({}, {'agricolture_productivity_modifier': .05}, 'MASHAV Agricultural Mission'),
    'mashav_ethiopia': ({}, {'agricolture_productivity_modifier': .05}, 'MASHAV Agricultural Mission'),
    'european_orders': ({'civilian_factories_productivity': .05}, {'civilian_factories_productivity': .05}, 'Civilian Workshop Partnership'),
    'jarring_channel': ({'police_cost_multiplier_modifier': -.03}, {'police_cost_multiplier_modifier': -.03}, 'Military Negotiating Channel'),
    'liaison_limits': ({'foreign_influence_defense_modifier': .10}, {'foreign_influence_defense_modifier': .10}, 'Limited Signals Liaison'),
    'liaison_turkey': ({'foreign_influence_defense_modifier': .10}, {'foreign_influence_defense_modifier': .10}, 'Limited Signals Liaison'),
    'negotiated_terms': ({'police_cost_multiplier_modifier': -.04, 'bureaucracy_cost_multiplier_modifier': -.03}, {}, 'Funded Territorial Service Relief'),
    'labor_jordanian_option': ({'police_cost_multiplier_modifier': -.05, 'personnel_cost_multiplier_modifier': -.03}, {'police_cost_multiplier_modifier': -.05, 'personnel_cost_multiplier_modifier': -.03}, 'Jordanian Border Liaison'),
    'gahal_local_autonomy': ({'bureaucracy_cost_multiplier_modifier': -.06, 'offices_productivity': .04}, {'bureaucracy_cost_multiplier_modifier': -.06, 'offices_productivity': .04}, 'Civil Services Agreement'),
    'haolam_joint_services': ({'industry_repair_factor': .15, 'production_speed_infrastructure_factor': .10}, {'industry_repair_factor': .15, 'production_speed_infrastructure_factor': .10}, 'Joint Municipal Services'),
    'arms_exports': ({'industrial_capacity_factory': -.05}, {}, 'Export Production Commitment'),
    'arms_congo': ({'industrial_capacity_factory': -.05}, {}, 'Export Production Commitment'),
}


def fmt(value):
    """Script literals must never exceed five decimal places."""
    v = Decimal(str(value)).quantize(Decimal('.00001'))
    return format(v, 'f').rstrip('0').rstrip('.') if v else '0'


def B(name, body):
    body = '\n'.join('\t' + line if line else '' for line in body.splitlines())
    return name + ' = {\n' + body + '\n}'


def C(*lines):
    return '\n'.join(x for x in lines if x)


def V(name, value):
    return f'set_variable = {{ {name} = {fmt(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def I(name, value):
    return f'add_to_variable = {{ {name} = {fmt(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def S(name, value):
    return f'subtract_from_variable = {{ {name} = {fmt(value) if isinstance(value, (float, int, Decimal)) else value} }}'


def IF(test, body, other=''):
    result = B('if', B('limit', test) + '\n' + body)
    return result + ('\n' + B('else', other) if other else '')


def cash(value):
    return f'set_temp_variable = {{ treasury_change = {value} }}\nmodify_treasury_effect = yes'


def public_debt(value):
    return f'set_temp_variable = {{ debt_change = {value} }}\nmodify_debt_effect = yes'


def investment(value):
    return f'set_temp_variable = {{ int_investment_change = {value} }}\nmodify_international_investment_effect = yes'


def scoped(tag, body):
    return B(tag, body)


def check(var, op, value):
    if op in ('>=','<='):
        compare = 'greater_than_or_equals' if op == '>=' else 'less_than_or_equals'
        return f'check_variable = {{ var = {var} value = {value} compare = {compare} }}'
    return f'check_variable = {{ {var} {op} {value} }}'


def mathvar(name, base, factor):
    return B('set_variable', B(name, f'value = {base}\nmultiply = {fmt(factor)}'))


def extend_data(data):
    """Add only the three approved, fixed-counterparty financing focuses."""
    data = deepcopy(data)
    existing = {n['id'] for n in data['nodes']}
    capital = next(g for g in data['groups'] if g['id'] == 'capital')['origin']
    for tag, x in zip(FINANCIERS, (-4, 0, 4)):
        key = 'ISR2_financing_' + tag.lower()
        if key in existing:
            continue
        country = COUNTRIES[tag]
        effects = [dict(heading='If they accept: ' + country, label='Treasury', value='-2% of quoted Israeli annual GDP', tone='cost'),
                   dict(heading='If they accept: ' + country, label='International Investment Asset', value='+2% of quoted Israeli annual GDP', tone='gain'),
                   dict(heading='If they accept: Israel', label='Restricted Project Capital', value='+2% of quoted Israeli annual GDP for 52 weeks', tone='gain'),
                   dict(heading='After 52 weeks: ' + country, label='Unused Restricted Capital Returned', value='+100% of the unused balance', tone='gain'),
                   dict(heading='After 52 weeks: ' + country, label='Unused International Investment Asset', value='-100% of the unused balance', tone='cost')]
        data['nodes'].append(dict(id=key, group='capital', label='Offer ' + country + ' a Project Investment',
            xy=[capital[0] + x, capital[1] + 6], days=35, pre=[], exclusive=[],
            description='Offer a defined investment in Israeli civilian and development projects. The investor supplies real capital and acquires an international investment asset. Capital still unallocated after one year returns to its owner.',
            effects=effects, modifiers={}, requirements=['The recipient is ' + country + ', and its government can receive the offer.'],
            icon='GFX_ISR70_focus_generic_financial_markets',
            history=dict(status='Plausible recipient-approved investment', sources=['economy'], note='A new RP investment, using native MD investment assets; no claimed historical invoice or fixed return.'),
            mechanics=['Only an accepted, fully paid investment creates restricted project capital. Native investment income follows the existing MD portfolio calculation. Unallocated capital expires after 52 weeks; deployed capital remains in the investor portfolio.'],
            programme='Restricted project subscription: 52 weeks', action_origin='national_focus',
            offer_target=dict(country=country, tag=tag), offer_origin='focus_completion',
            recipient_response='country_event_accept_or_refuse',
            focus_cycle=dict(cooldown_weeks=52, lifetime_limit=None, provider='uncomplete_national_focus', uncomplete_children=False, refund_political_power=False, new_term_costs=True)))
    return data


def build(data):
    """Return files/actions/daily/init/loc without mutating or writing data."""
    nodes = [deepcopy(n) for n in data['nodes'] if n.get('offer_target')]
    groups = {g['id']: g for g in data['groups']}
    loc = dict(ISR2_bilateral_accept='Accept the agreement.', ISR2_bilateral_refuse='Decline the offer.',
               ISR2_bilateral_cancelled='The proposed agreement could not be concluded.',
               ISR2_bilateral_capital_tt='Restricted project capital: §G+$[?ISR.ISR2_bilateral_preview_amount|3] billion§!',
               ISR2_bilateral_investment_tt='International investment asset: §G+$[?ISR.ISR2_bilateral_preview_amount|3] billion§!',
               ISR2_bilateral_investment_roi_tt='Current annual portfolio return: §Y[?ISR2_bilateral_preview_roi|%2]§!. Additional weekly portfolio return at that rate: §G+$[?ISR2_bilateral_preview_return|5] billion§!.',
               ISR2_bilateral_finance_return_tt='Unused capital after 52 weeks: §G+100%§! to Treasury; international investment asset: §R-100%§! of the unused balance.',
               ISR2_bilateral_weekly_expense_tt='Weekly programme expense: §R-$[?ISR2_bilateral_preview_weekly|5] billion§!',
               ISR2_bilateral_weekly_income_tt='Weekly programme income: §G+$[?ISR2_bilateral_preview_weekly|5] billion§!',
               ISR2_bilateral_pal_pressure_tt='Affected Palestinian area: pressure limited to §Y1 tier§! for §Y52 weeks§!. At tier 2: office productivity §G+4%§!, bureaucracy cost §G-4%§!, stability §G+2%§!.',
               ISR2_bilateral_loan_principal_tt='Public debt principal: §G-$[?ISR.ISR2_bilateral_preview_principal|5] billion per week§! for §Y104 weeks§!.',
               ISR2_bilateral_loan_received_tt='Loan principal received: §G+$[?ISR.ISR2_bilateral_preview_principal|5] billion per week§!; interest received: §G+$[?ISR.ISR2_bilateral_preview_interest|5] billion per week§! for §Y104 weeks§!.',
               ISR2_bilateral_loan_paid_tt='Loan principal payment: §R-$[?ISR.ISR2_bilateral_preview_principal|5] billion per week§!; interest: §R-$[?ISR.ISR2_bilateral_preview_interest|5] billion per week§! for §Y104 weeks§!.')
    effects, triggers, events, ideas, actions = [], [], ['add_namespace = ISR2_bilateral'], [], {}
    opinion = [B('opinion_modifiers', C(B('ISR2_bilateral_opinion_10', 'value = 10\nmonths = 12'), B('ISR2_bilateral_opinion_15', 'value = 15\nmonths = 12')))]
    records = []
    for index, n in enumerate(nodes, 1):
        slug = n['id'][5:]
        p = 'ISR2_b_' + slug
        tag = n['offer_target']['tag']
        country = n['offer_target']['country']
        kind = ('finance' if slug.startswith('financing_') else 'arms' if slug in ('arms_exports', 'arms_congo') else 'loan' if slug == 'eastern_credit' else 'normal')
        duration = 364 if kind == 'finance' else 182 if kind == 'arms' else 728 if kind == 'loan' else max([e['scope'] * 7 for e in n['effects'] if isinstance(e.get('scope'), int)] + [364 if not any('104 weeks' in e['value'] for e in n['effects']) else 728])
        r = dict(node=n, slug=slug, p=p, tag=tag, country=country, kind=kind, duration=duration, index=index)
        records.append(r)
        loc[p+'_research'] = 'Technical Cooperation'
        root_party = groups[n['group']].get('runtime_party_trigger')
        sanction_isr = C(*(f'is_in_array = {{ array = {a} value = {tag} }}' for a in SANCTIONS))
        sanction_partner = C(*(f'is_in_array = {{ array = {a} value = ISR }}' for a in SANCTIONS))
        pair = C('country_exists = ISR', 'country_exists = ' + tag,
                 'NOT = { has_country_flag = disabled_economic_system }',
                 'NOT = { has_country_flag = MD_skip_treasury_cost }',
                 f'NOT = {{ has_war_with = {tag} }}', f'NOT = {{ is_embargoing = {tag} }}',
                 B('NOT', B('OR', sanction_isr)),
                 scoped(tag, C('NOT = { has_country_flag = disabled_economic_system }', 'NOT = { has_country_flag = MD_skip_treasury_cost }', 'NOT = { has_war_with = ISR }', 'NOT = { is_embargoing = ISR }', B('NOT', B('OR', sanction_partner)))))
        triggers.append(B(p + '_pair_clear', pair))
        pressure = B('OR', check('ISR2_territories_pressure_208', '>', 0) + '\n' + check('ISR2_territories_pressure_209', '>', 0)) if slug == 'negotiated_terms' else ''
        available = C('ISR2_is_scenario = yes', p + '_pair_clear = yes', root_party + ' = yes' if root_party else '',
                      f'NOT = {{ has_country_flag = {p}_pending }}', f'NOT = {{ has_country_flag = {p}_signed }}',
                      f'NOT = {{ has_country_flag = {p}_cooldown }}',
                      'NOT = { has_country_flag = ISR2_bilateral_arms_pending }' if kind == 'arms' else '',
                      'NOT = { has_country_flag = '+p+'_refund_due }' if kind == 'finance' else '',
                      'NOT = { has_country_flag = '+p+'_invoice_refund_due }' if kind == 'arms' else '',
                      check('ISR2_bilateral_loan_outstanding', '<', '.00001') if kind == 'loan' else '', pressure)
        triggers.append(B(p + '_can_offer', available))
        # Freeze all GDP-based terms when the focus issues the offer.
        quote = C(V(p + '_gdp', 'gdp_total'), V(p + '_partner_gdp', tag + '.gdp_total'),
                  V(p + '_setup_isr', 0), V(p + '_setup_partner', 0), V(p + '_weekly_isr', 0), V(p + '_weekly_partner', 0))
        setup = {'mashav': (.003, 0), 'mashav_ethiopia': (.003, 0), 'washington': (.008, 0),
                 'european_orders': (.005, .005), 'jarring_channel': (.0015, .0015),
                 'liaison_limits': (.0025, .0025), 'liaison_turkey': (.0025, .0025),
                 'labor_jordanian_option': (.003, .003), 'gahal_local_autonomy': (.004, .004),
                 'haolam_joint_services': (.004, .004)}.get(slug, (0, 0))
        weekly = {'mashav': (.0001, 0), 'mashav_ethiopia': (.0001, 0), 'european_orders': (0, 0),
                  'jarring_channel': (.00003, .00003), 'liaison_limits': (.00005, .00005),
                  'liaison_turkey': (.00005, .00005), 'labor_jordanian_option': (.00005, .00005),
                  'gahal_local_autonomy': (.00005, .00005), 'haolam_joint_services': (.00006, .00006)}.get(slug, (0, 0))
        quote += '\n' + C(*(mathvar(p + '_setup_' + side, base, share) for side, base, share in [('isr', p+'_gdp', setup[0]), ('partner', p+'_partner_gdp', setup[1])]),
                           *(mathvar(p + '_weekly_' + side, base, share) for side, base, share in [('isr', p+'_gdp', weekly[0]), ('partner', p+'_partner_gdp', weekly[1])]))
        if slug == 'irrigation_exports':
            quote += '\n' + C(V(p+'_setup_isr', .002), V(p+'_setup_partner', .006), V(p+'_weekly_isr', .00002))
        if kind == 'arms':
            quote += '\n' + C(V(p+'_setup_isr', .004), V(p+'_setup_partner', .01))
        if kind == 'loan':
            quote += '\n' + mathvar(p+'_setup_partner', p+'_gdp', .04)
        if kind == 'finance':
            quote += '\n' + mathvar(p+'_setup_partner', p+'_gdp', .02)
        if slug == 'negotiated_terms':
            quote += '\n' + mathvar(p+'_weekly_isr', p+'_gdp', .0002)
        r['quote'] = quote
        funds = C(check('treasury', '>=', p+'_setup_isr') if setup[0] or slug=='irrigation_exports' or kind=='arms' else '',
                  scoped(tag, check('treasury', '>=', 'ISR.'+p+'_setup_partner')) if setup[1] or slug=='irrigation_exports' or kind in ('arms','loan','finance') else '')
        accept_valid = C('ISR2_is_scenario = yes', p+'_pair_clear = yes', root_party+' = yes' if root_party else '',
                         f'has_country_flag = {p}_pending', f'NOT = {{ has_country_flag = {p}_signed }}',
                         scoped(tag, 'has_country_flag = '+p+'_pending'), funds, pressure,
                         'has_country_flag = ISR2_bilateral_arms_pending' if kind=='arms' else '')
        triggers.append(B(p+'_accept_valid', accept_valid))
        for side, mods in zip(('isr', 'partner'), MODIFIERS.get(slug, ({}, {}, ''))[:2]):
            if mods:
                idea = p+'_'+side+'_idea'
                ideas.append(B(idea, C('picture = generic_trade', 'allowed = { always = no }', 'allowed_civil_war = { always = yes }', 'removal_cost = -1', B('modifier', C(*(k+' = '+fmt(v) for k,v in mods.items()))))))
                loc[idea] = MODIFIERS[slug][2]
                loc[idea+'_desc'] = 'The funded agreement remains subject to its accepted term.'
        # A native, non-executing numeric preview is used in both focus and event.
        native_isr, native_partner = [], []
        for side, target_list in [('isr', native_isr), ('partner', native_partner)]:
            if (setup[0] if side=='isr' else setup[1]) or (side=='isr' and slug=='irrigation_exports') or (side=='partner' and kind in ('arms','loan','finance')) or (side=='partner' and slug=='irrigation_exports'):
                native = C(f'set_temp_variable = {{ treasury_change = {{ value = ISR.{p}_setup_{side} multiply = -1 }} }}', 'modify_treasury_effect = yes')
                target_list.append(native)
            if MODIFIERS.get(slug, ({}, {}, ''))[0 if side=='isr' else 1]:
                target_list.append(f'add_timed_idea = {{ idea = {p}_{side}_idea days = {duration} }}')
            if weekly[0 if side=='isr' else 1] or (side=='isr' and slug in ('irrigation_exports','negotiated_terms')):
                target_list.append(C(f'set_temp_variable = {{ ISR2_bilateral_preview_weekly = ISR.{p}_weekly_{side} }}', 'custom_effect_tooltip = ISR2_bilateral_weekly_expense_tt'))
        if slug in ('irrigation_exports','arms_exports','arms_congo','washington'):
            # The training fee goes the opposite way to the commercial invoice.
            (native_partner if slug=='washington' else native_isr).append(cash('ISR.'+p+('_setup_isr' if slug=='washington' else '_setup_partner')))
        if kind=='finance':
            native_isr += [f'set_temp_variable = {{ ISR2_bilateral_preview_amount = {p}_setup_partner }}', 'custom_effect_tooltip = ISR2_bilateral_capital_tt']
            native_partner += [investment('ISR.'+p+'_setup_partner'),
                'set_temp_variable = { ISR2_bilateral_preview_roi = { value = 0.04 add = modifier@return_on_investment_modifier clamp = { min = 0 max = global.roi_rate_cap } } }',
                f'set_temp_variable = {{ ISR2_bilateral_preview_return = {{ value = ISR.{p}_setup_partner multiply = ISR2_bilateral_preview_roi multiply = 0.019 }} }}',
                'custom_effect_tooltip = ISR2_bilateral_investment_roi_tt', 'custom_effect_tooltip = ISR2_bilateral_finance_return_tt']
        if kind=='loan':
            native_isr += [cash('ISR.'+p+'_setup_partner'), public_debt('ISR.'+p+'_setup_partner'),
                'custom_effect_tooltip = ISR2_bilateral_loan_principal_tt', 'custom_effect_tooltip = ISR2_bilateral_loan_paid_tt']
            native_partner.append('custom_effect_tooltip = ISR2_bilateral_loan_received_tt')
        if kind=='arms':
            native_isr += [f'send_equipment = {{ type = infantry_weapons_type amount = 1000 target = {tag} }}', 'army_experience = 5']
            loc[p+'_delivery_tt'] = 'Infantry equipment at delivery: §G+1,000§!.'
            native_partner.extend(['custom_effect_tooltip = '+p+'_delivery_tt','army_experience = 10'])
        rewards_isr, rewards_partner = _research_rewards(slug, p)
        if slug in ('mashav','mashav_ethiopia'):
            native_isr.append(IF('NOT = { has_country_flag = ISR2_bilateral_mashav_lesson }',C(*rewards_isr)))
        else:
            native_isr.extend(rewards_isr)
        native_partner.extend(rewards_partner)
        if slug=='washington': native_isr.append('air_experience = 35')
        if slug=='negotiated_terms':
            native_partner += ['custom_effect_tooltip = ISR2_bilateral_pal_pressure_tt', C(f'set_temp_variable = {{ ISR2_bilateral_preview_weekly = ISR.{p}_weekly_isr }}', 'custom_effect_tooltip = ISR2_bilateral_weekly_income_tt')]
        if slug in ('gahal_local_autonomy','haolam_joint_services'):
            other = 'haolam_joint_services' if slug=='gahal_local_autonomy' else 'gahal_local_autonomy'
            old = 'ISR2_b_'+other
            native_isr.insert(0,IF('has_idea = '+old+'_isr_idea','remove_ideas = '+old+'_isr_idea'))
            native_partner.insert(0,IF('has_idea = '+old+'_partner_idea','remove_ideas = '+old+'_partner_idea'))
        op = 15 if slug in ('washington','eastern_credit') else 10
        if any(e['label'].endswith(' Opinion') for e in n['effects']):
            native_isr.append(f'add_opinion_modifier = {{ target = {tag} modifier = ISR2_bilateral_opinion_{op} }}')
            native_partner.append(f'add_opinion_modifier = {{ target = ISR modifier = ISR2_bilateral_opinion_{op} }}')
        quote_names = ('partner_gdp','setup_partner','setup_isr','weekly_partner','weekly_isr','gdp')
        def preview_vars(text):
            for q in quote_names:
                text=text.replace(p+'_'+q,p+'_pv_'+q)
            return text
        preview_quote = preview_vars(quote).replace('set_variable','set_temp_variable')
        frozen_quote = C(*(f'set_temp_variable = {{ {p}_pv_{q} = {p}_{q} }}' for q in quote_names))
        preview_setup = C(IF(B('OR',f'has_country_flag = {p}_pending\nhas_country_flag = {p}_signed'),frozen_quote,preview_quote),
            f'set_temp_variable = {{ ISR2_bilateral_preview_amount = {p}_pv_setup_partner }}',
            B('set_variable', B('ISR2_bilateral_preview_principal', f'value = {p}_pv_setup_partner\ndivide = 104')),
            mathvar('ISR2_bilateral_preview_interest', 'ISR2_bilateral_preview_principal', .08))
        preview_setup=preview_setup.replace('set_variable','set_temp_variable')
        # Quote calculation must not mutate the live frozen offer when previewed.
        preview = B('effect_tooltip', C(scoped('ISR', C(preview_setup, preview_vars(C(*native_isr)))), scoped(tag, preview_vars(C(*native_partner)))))
        r['preview'] = preview
        effects.append(B(p+'_preview', preview))
        visible=[]
        def requirement(suffix,text,condition):
            loc[p+'_'+suffix+'_tt']=text
            visible.append(B('custom_trigger_tooltip','tooltip = '+p+'_'+suffix+'_tt\n'+condition))
        requirement('exists',country+' exists.','country_exists = '+tag)
        requirement('peace','Israel and '+country+' are at peace.',f'NOT = {{ has_war_with = {tag} }}')
        requirement('restrictions','Neither government imposes an embargo or diplomatic, financial, economic or military sanctions on the other.',
            C(f'NOT = {{ is_embargoing = {tag} }}',B('NOT',B('OR',sanction_isr)),
              scoped(tag,C('NOT = { is_embargoing = ISR }',B('NOT',B('OR',sanction_partner))))))
        requirement('pending','No earlier offer of this programme is awaiting a response.',f'NOT = {{ has_country_flag = {p}_pending }}')
        requirement('active','No accepted term of this programme is outstanding.',f'NOT = {{ has_country_flag = {p}_signed }}')
        requirement('cooldown','The diplomatic cooldown has ended.',f'NOT = {{ has_country_flag = {p}_cooldown }}')
        requirement('payments','Both governments can settle actual monetary payments.',C(
            'NOT = { has_country_flag = disabled_economic_system }','NOT = { has_country_flag = MD_skip_treasury_cost }',
            scoped(tag,C('NOT = { has_country_flag = disabled_economic_system }','NOT = { has_country_flag = MD_skip_treasury_cost }'))))
        if kind=='arms':
            requirement('order','No Israeli equipment order is awaiting acceptance or delivery.','NOT = { has_country_flag = ISR2_bilateral_arms_pending }')
            requirement('refund','No earlier invoice return remains outstanding.',f'NOT = {{ has_country_flag = {p}_invoice_refund_due }}')
        if kind=='finance':
            requirement('refund','No earlier unused subscription remains to be returned.',f'NOT = {{ has_country_flag = {p}_refund_due }}')
        if kind=='loan':
            requirement('principal','No earlier Soviet loan principal remains unpaid.',check('ISR2_bilateral_loan_outstanding','<','.00001'))
        if pressure:
            requirement('pressure','An affected Palestinian area has active settlement pressure.',pressure)
        actions[n['id']] = dict(available=p+'_can_offer = yes', visible_available=C(*visible),reward=p+'_offer = yes', preview=p+'_preview = yes')
        effects.append(B(p+'_offer', IF(p+'_can_offer = yes', C(quote, f'set_country_flag = {p}_pending', V(p+'_pending_days', 30),
              'set_country_flag = ISR2_bilateral_arms_pending' if kind=='arms' else '',
              scoped(tag, C('set_country_flag = '+p+'_pending', f'country_event = {{ id = ISR2_bilateral.{index} days = 1 }}'))))))
        clear_pending = C('clr_country_flag = '+p+'_pending', V(p+'_pending_days', 0),
                    scoped(tag, 'clr_country_flag = '+p+'_pending'),
                    'clr_country_flag = ISR2_bilateral_arms_pending' if kind=='arms' else '')
        decline = C(clear_pending, f'set_country_flag = {{ flag = {p}_cooldown value = 1 days = 14 }}', 'set_country_flag = '+p+'_reopen')
        effects.append(B(p+'_decline', IF('has_country_flag = '+p+'_pending',decline)))
        replacement = ''
        if slug in ('gahal_local_autonomy','haolam_joint_services'):
            other = 'haolam_joint_services' if slug=='gahal_local_autonomy' else 'gahal_local_autonomy'
            replacement = f'ISR2_b_{other}_end = yes'
        # Every acceptance is guarded again immediately before its transaction.
        accept_body = C(clear_pending,
            replacement, f'set_country_flag = {p}_signed', V(p+'_days', duration), V(p+'_paid_days', 0), 'clr_country_flag = '+p+'_reopen',
            scoped(tag,'set_country_flag = ISR2_bilateral_recipient'),
            cash('{ value = '+p+'_setup_isr multiply = -1 }') if setup[0] or slug=='irrigation_exports' or kind=='arms' else '',
            scoped(tag, cash('{ value = ISR.'+p+'_setup_partner multiply = -1 }')) if setup[1] or slug=='irrigation_exports' or kind in ('arms','loan','finance') else '')
        if slug in ('irrigation_exports','arms_exports','arms_congo'):
            accept_body += '\n'+cash(p+'_setup_partner')
        if slug=='washington': accept_body += '\n'+scoped(tag, cash('ISR.'+p+'_setup_isr'))
        if kind=='finance':
            accept_body += '\n'+C(V(p+'_unallocated', p+'_setup_partner'), scoped(tag, investment('ISR.'+p+'_setup_partner')), 'ISR2_private_recalculate = yes')
        elif kind=='loan':
            accept_body += '\n'+C(cash(p+'_setup_partner'), public_debt(p+'_setup_partner'), V('ISR2_bilateral_loan_outstanding', p+'_setup_partner'),
                mathvar(p+'_interest_remaining', p+'_setup_partner', .08), V(p+'_weeks_remaining',104), V(p+'_payment_days',0),
                B('set_variable', B(p+'_principal_instalment', f'value = {p}_setup_partner\ndivide = 104')),
                B('set_variable', B(p+'_interest_instalment', f'value = {p}_interest_remaining\ndivide = 104')))
        elif kind=='arms': accept_body += '\n'+C('set_country_flag = ISR2_bilateral_arms_pending','clr_country_flag = '+p+'_delivered')
        if slug=='negotiated_terms':
            accept_body += '\n'+IF(check('ISR2_territories_pressure_208','>=','ISR2_territories_pressure_209'), V(p+'_relief_state',208), V(p+'_relief_state',209))
        if kind not in ('arms','loan','finance'):
            accept_body += '\n'+C(*_actual_research_rewards(slug,p,tag))
            if slug=='washington': accept_body+='\nair_experience = 35'
        op = 15 if slug in ('washington','eastern_credit') else 10
        if any(e['label'].endswith(' Opinion') for e in n['effects']):
            accept_body += '\n'+C(f'add_opinion_modifier = {{ target = {tag} modifier = ISR2_bilateral_opinion_{op} }}', scoped(tag, f'add_opinion_modifier = {{ target = ISR modifier = ISR2_bilateral_opinion_{op} }}'))
        accept_body += '\nISR2_bilateral_reconcile = yes'
        effects.append(B(p+'_accept', IF(p+'_accept_valid = yes',accept_body, p+'_decline = yes')))
        end = C('clr_country_flag = '+p+'_signed', V(p+'_days',0), _remove_ideas(slug,p,tag))
        if kind=='finance':
            # A dead partner retains a return claim. Do not erase its escrow.
            end += '\n'+IF(check(p+'_unallocated','>',0), C(f'set_country_flag = {p}_refund_due',p+'_return_unused = yes'))
        if kind=='arms':
            end += '\n'+C('clr_country_flag = ISR2_bilateral_arms_pending', IF(f'NOT = {{ has_country_flag = {p}_delivered }}', C(
                f'set_country_flag = {p}_invoice_refund_due',p+'_return_invoice = yes')))
            effects.append(B(p+'_return_invoice',IF(C('has_country_flag = '+p+'_invoice_refund_due',
                'country_exists = '+tag,'NOT = { has_country_flag = MD_skip_treasury_cost }',
                scoped(tag,'NOT = { has_country_flag = MD_skip_treasury_cost }')),C(
                    'clr_country_flag = '+p+'_invoice_refund_due',
                    cash('{ value = '+p+'_setup_partner multiply = -1 }'),scoped(tag,cash('ISR.'+p+'_setup_partner'))))))
        end += '\nset_country_flag = '+p+'_reopen'
        effects.append(B(p+'_end', IF('has_country_flag = '+p+'_signed',end)))
        loc['ISR2_bilateral.'+str(index)+'.t'] = n['label']
        loc['ISR2_bilateral.'+str(index)+'.d'] = ('Israel offers funded civilian services in one affected Palestinian area. Both governments retain their positions on territory.' if slug=='negotiated_terms' else n['description'])
        events.append(B('country_event', C('id = ISR2_bilateral.'+str(index), 'title = ISR2_bilateral.'+str(index)+'.t', 'desc = ISR2_bilateral.'+str(index)+'.d',
             'picture = GFX_COLDWAR_CUB_1970_event_signing', 'is_triggered_only = yes',
             B('trigger', C('tag = '+tag, 'has_country_flag = '+p+'_pending', scoped('ISR', C('ISR2_is_scenario = yes','has_country_flag = '+p+'_pending')))),
             B('option', C('name = ISR2_bilateral_accept', B('trigger', scoped('ISR',p+'_accept_valid = yes')), scoped('ISR',p+'_preview = yes'), B('hidden_effect',scoped('ISR',p+'_accept = yes')), 'ai_chance = { factor = 0 }')),
             B('option', C('name = ISR2_bilateral_refuse',B('hidden_effect',scoped('ISR',p+'_decline = yes')), 'ai_chance = { factor = 100 }')))))

    _emit_reconcile(records, effects)
    _emit_daily(records, effects)
    _emit_private(records, effects, triggers)
    _emit_loan(records, effects)
    orphan=C(V('ISR2_bilateral_weekly_income',0),V('ISR2_bilateral_weekly_expense',0),
        *(IF('tag = '+r['tag'],'remove_ideas = '+r['p']+'_partner_idea') for r in records if MODIFIERS.get(r['slug'],({}, {},''))[1]))
    effects.append(B('ISR2_bilateral_orphan_cleanup',orphan))
    effects.append(B('ISR2_bilateral_init', IF(C('ISR2_is_scenario = yes','NOT = { has_country_flag = ISR2_bilateral_initialized }'), C('set_country_flag = ISR2_bilateral_initialized',
        V('ISR2_bilateral_loan_outstanding',0), V('ISR2_private_available',0), V('ISR2_private_paid',0),
        *(V(r['p']+'_days',0) for r in records), *(V(r['p']+'_pending_days',0) for r in records),
        'ISR2_bilateral_reconcile = yes'))))
    files = {
        'common/scripted_effects/ISR2_bilateral_effects.txt':MARKER+'\n\n'.join(effects)+'\n',
        'common/scripted_triggers/ISR2_bilateral_triggers.txt':MARKER+'\n\n'.join(triggers)+'\n',
        'common/ideas/ISR2_bilateral_ideas.txt':MARKER+B('ideas',B('country','\n'.join(ideas)))+'\n',
        'common/opinion_modifiers/ISR2_bilateral_opinions.txt':MARKER+'\n'.join(opinion)+'\n',
        'events/ISR2_bilateral_events.txt':MARKER+'\n\n'.join(events)+'\n',
        'common/on_actions/ISR2_bilateral_orphan_on_actions.txt':MARKER+B('on_actions',B('on_daily',B('effect',IF(C('has_country_flag = ISR2_bilateral_recipient','NOT = { country_exists = ISR }'),'ISR2_bilateral_orphan_cleanup = yes'))))+'\n',
    }
    return dict(files=files, actions=actions, daily='ISR2_bilateral_daily = yes', refresh='ISR2_bilateral_reconcile = yes', init='ISR2_bilateral_init = yes',loc=loc,
                loan_outstanding='ISR2_bilateral_loan_outstanding', early_repayment='ISR2_bilateral_loan_early_repay = yes')


def _research_rewards(slug,p):
    left,right=[],[]
    def tech(cat):return f'add_tech_bonus = {{ name = {p}_research bonus = 0.5 uses = 1 category = {cat} }}'
    if slug in ('mashav','mashav_ethiopia'):
        left.append(tech('CAT_agriculture'));right.append(tech('CAT_agriculture'))
    if slug=='washington':left.append(tech('CAT_aircraft'))
    if slug=='european_orders':left.append(tech('CAT_industry'));right.append(tech('CAT_electronics'))
    if slug in ('liaison_limits','liaison_turkey'):left.append(tech('CAT_encryption'));right.append(tech('CAT_encryption'))
    return left,right


def _actual_research_rewards(slug,p,tag):
    left,right=_research_rewards(slug,p)
    if slug in ('mashav','mashav_ethiopia'):
        left=[IF('NOT = { has_country_flag = ISR2_bilateral_mashav_lesson }',C(*left,'set_country_flag = ISR2_bilateral_mashav_lesson'))]
    return left+([scoped(tag,C(*right))] if right else [])


def _remove_ideas(slug,p,tag):
    mods=MODIFIERS.get(slug,({}, {},''))
    return C('remove_ideas = '+p+'_isr_idea' if mods[0] else '',scoped(tag,'remove_ideas = '+p+'_partner_idea') if mods[1] else '')


def _emit_reconcile(records,effects):
    lines=[V('ISR2_bilateral_weekly_income',0),V('ISR2_bilateral_weekly_expense',0),'clr_country_flag = ISR2_pal_service_relief_active']
    for tag in PARTNERS:lines.append(scoped(tag,C(V('ISR2_bilateral_weekly_income',0),V('ISR2_bilateral_weekly_expense',0))))
    for r in records:
        p,slug,tag,kind=r['p'],r['slug'],r['tag'],r['kind']
        mods=MODIFIERS.get(slug,({}, {},''))
        valid=C('has_country_flag = '+p+'_signed',p+'_pair_clear = yes',check(p+'_days','>',0))
        if kind=='loan':valid=C('has_country_flag = '+p+'_signed',p+'_pair_clear = yes',check('ISR2_bilateral_loan_outstanding','>',0))
        if slug=='negotiated_terms':
            valid+='\n'+B('OR',C(B('AND',C(check(p+'_relief_state','=',208),check('ISR2_territories_pressure_208','>',0))),B('AND',C(check(p+'_relief_state','=',209),check('ISR2_territories_pressure_209','>',0)))))
        active=C('set_country_flag = '+p+'_active',
            IF('NOT = { has_idea = '+p+'_isr_idea }','add_ideas = '+p+'_isr_idea') if mods[0] else '',
            scoped(tag,IF('NOT = { has_idea = '+p+'_partner_idea }','add_ideas = '+p+'_partner_idea')) if mods[1] else '')
        if kind=='normal':
            active+='\n'+C(I('ISR2_bilateral_weekly_expense',p+'_weekly_isr'), scoped(tag,I('ISR2_bilateral_weekly_expense','ISR.'+p+'_weekly_partner')))
        if slug=='negotiated_terms':
            active+='\n'+C('set_country_flag = ISR2_pal_service_relief_active',V('ISR2_pal_service_relief_state',p+'_relief_state'),scoped(tag,I('ISR2_bilateral_weekly_income','ISR.'+p+'_weekly_isr')))
        lines.append(IF(valid,active,C('clr_country_flag = '+p+'_active',_remove_ideas(slug,p,tag))))
    lines.append('ISR2_private_recalculate = yes')
    effects.append(B('ISR2_bilateral_reconcile',C(*lines)))


def _emit_daily(records,effects):
    lines=['ISR2_private_claim_settle = yes']
    for r in records:
        p,slug,tag,kind=r['p'],r['slug'],r['tag'],r['kind']
        if kind=='finance':
            # Return the exact unused subscription once; deployed assets survive.
            # A country which temporarily disappears receives this on restoration.
            lines.append(p+'_return_unused = yes')
        lines.append(IF('has_country_flag = '+p+'_pending',C(S(p+'_pending_days',1),IF(check(p+'_pending_days','<',1),p+'_decline = yes'))))
        lines.append(IF(C('has_country_flag = '+p+'_reopen','NOT = { has_country_flag = '+p+'_cooldown }','NOT = { has_country_flag = '+p+'_signed }','NOT = { has_country_flag = '+p+'_pending }'),C(f'uncomplete_national_focus = {{ focus = {r["node"]["id"]} uncomplete_children = no refund_political_power = no }}','clr_country_flag = '+p+'_reopen')))
        if kind=='loan':
            lines.append(IF('has_country_flag = '+p+'_signed','ISR2_bilateral_loan_tick = yes'));continue
        if kind=='arms':
            lines.append(p+'_return_invoice = yes')
            deliver=C(f'send_equipment = {{ type = infantry_weapons_type amount = 1000 target = {tag} }}','army_experience = 5',scoped(tag,'army_experience = 10'),'set_country_flag = '+p+'_delivered', f'set_country_flag = {{ flag = {p}_cooldown value = 1 days = 364 }}',p+'_end = yes')
            lines.append(IF(C('has_country_flag = '+p+'_signed',p+'_pair_clear = yes','has_equipment = { infantry_weapons_type > 999 }'),deliver))
        lines.append(IF('has_country_flag = '+p+'_signed',C(S(p+'_days',1),IF(check(p+'_days','<',1),p+'_end = yes'))))
    lines.append('ISR2_bilateral_reconcile = yes')
    effects.append(B('ISR2_bilateral_daily',IF(C('ISR2_is_scenario = yes','NOT = { has_country_flag = ISR2_bilateral_day_processed }'),C(
        'set_country_flag = { flag = ISR2_bilateral_day_processed value = 1 days = 1 }', 'ISR2_bilateral_init = yes',*lines))))


def _emit_private(records,effects,triggers):
    financiers=[r for r in records if r['kind']=='finance']
    for r in financiers:
        p,tag=r['p'],r['tag']
        effects.append(B(p+'_return_unused',IF(C('has_country_flag = '+p+'_refund_due','country_exists = '+tag,
            scoped(tag,'NOT = { has_country_flag = MD_skip_treasury_cost }')),C(
            scoped(tag,C(cash('ISR.'+p+'_unallocated'),investment('{ value = ISR.'+p+'_unallocated multiply = -1 }'),
                         'clamp_variable = { var = int_investments min = 0 }')),
            V(p+'_unallocated',0),'clr_country_flag = '+p+'_refund_due','ISR2_private_recalculate = yes'))))
    eligible=lambda r:C('has_country_flag = '+r['p']+'_signed',r['p']+'_pair_clear = yes',check(r['p']+'_days','>',0))
    effects.append(B('ISR2_private_recalculate',C(V('ISR2_private_available',0),*(IF(eligible(r),I('ISR2_private_available',r['p']+'_unallocated')) for r in financiers))))
    triggers.append(B('ISR2_private_ready',C('ISR2_is_scenario = yes',check('ISR2_private_required','>=',0),check('ISR2_private_available','>=','ISR2_private_required'))))
    # Oldest remaining capital first: lower expiry counter wins; tag order breaks ties.
    commit=[V('ISR2_private_paid',0),*(V('ISR2_private_paid_'+tag,0) for tag in FINANCIERS),'ISR2_private_recalculate = yes']
    take=[]
    for _ in range(len(financiers)):
        take.extend([V('ISR2_private_oldest_days',99999),V('ISR2_private_oldest_index',0)])
        for i,r in enumerate(financiers,1):
            take.append(IF(C(eligible(r),check(r['p']+'_unallocated','>',0),check(r['p']+'_days','<','ISR2_private_oldest_days')),C(V('ISR2_private_oldest_days',r['p']+'_days'),V('ISR2_private_oldest_index',i))))
        for i,r in enumerate(financiers,1):
            take.append(IF(check('ISR2_private_oldest_index','=',i),C(V('ISR2_private_take','ISR2_private_required'),S('ISR2_private_take','ISR2_private_paid'),
                IF(check('ISR2_private_take','>',r['p']+'_unallocated'),V('ISR2_private_take',r['p']+'_unallocated')),
                S(r['p']+'_unallocated','ISR2_private_take'),I('ISR2_private_paid','ISR2_private_take'),
                I('ISR2_private_paid_'+r['tag'],'ISR2_private_take'))))
    commit.append(IF('ISR2_private_ready = yes',C(*take,'ISR2_private_recalculate = yes')))
    effects.append(B('ISR2_private_commit',C(*commit)))
    _emit_claims(effects)


def _emit_claims(effects):
    """Settle the insured investor's cash claim and retire its lost principal.

    Territory has already charged exactly one gross claim to its held reserve
    and Treasury. This provider never charges Israel again. Project IDs are
    fixed: Yanai slots 1/2 and the hotel project 3. The project-level receipt
    prevents replay; absent investors retain both cash and retirement claims.
    """
    settle=[]
    for tag in FINANCIERS:
        due,retire='ISR2_private_claim_due_'+tag,'ISR2_private_retire_due_'+tag
        settle.append(IF(C('country_exists = '+tag,scoped(tag,'NOT = { has_country_flag = MD_skip_treasury_cost }'),B('OR',C(check(due,'>',0),check(retire,'>',0)))),C(
            scoped(tag,C(cash('ISR.'+due),investment('{ value = ISR.'+retire+' multiply = -1 }'),
                         'clamp_variable = { var = int_investments min = 0 }')),
            V(due,0),V(retire,0))))
    effects.append(B('ISR2_private_claim_settle',C(*settle)))
    total=V('ISR2_private_claim_total_share',0)
    total+='\n'+C(*(I('ISR2_private_claim_total_share','ISR2_private_claim_share_'+tag) for tag in FINANCIERS))
    dispatch=[]
    # The final nonzero investor receives the exact remainder of the gross
    # claim, rather than three independently rounded proportional payments.
    allocate=[V('ISR2_private_claim_remainder','ISR2_private_claim_amount'),V('ISR2_private_claim_last_index',0)]
    for i,tag in enumerate(FINANCIERS,1):
        allocate.append(IF(check('ISR2_private_claim_share_'+tag,'>',0),V('ISR2_private_claim_last_index',i)))
    for i,tag in enumerate(FINANCIERS,1):
        share='ISR2_private_claim_share_'+tag
        portion=IF(check('ISR2_private_claim_last_index','=',i),V('ISR2_private_claim_portion','ISR2_private_claim_remainder'),
            B('set_variable',B('ISR2_private_claim_portion',f'value = ISR2_private_claim_amount\nmultiply = {share}\ndivide = ISR2_private_claim_total_share')))
        allocate.append(IF(check(share,'>',0),C(portion,
            S('ISR2_private_claim_remainder','ISR2_private_claim_portion'),
            I('ISR2_private_claim_due_'+tag,'ISR2_private_claim_portion'),I('ISR2_private_retire_due_'+tag,share))))
    for project in (1,2,3):
        dispatch.append(IF(C(check('ISR2_private_claim_id','=',project),f'NOT = {{ has_country_flag = ISR2_private_claim_registered_{project} }}'),C(
            f'set_country_flag = ISR2_private_claim_registered_{project}',*allocate,
            V('ISR2_private_claim_registered_amount','ISR2_private_claim_amount'),'ISR2_private_claim_settle = yes')))
    valid=C(check('ISR2_private_claim_amount','>',0),check('ISR2_private_claim_total_share','>',0),
        *(check('ISR2_private_claim_share_'+tag,'>=',0) for tag in FINANCIERS))
    effects.append(B('ISR2_private_claim_credit',C(V('ISR2_private_claim_registered_amount',0),total,
        IF(C('ISR2_is_scenario = yes',valid),C(*dispatch)))))


def _emit_loan(records,effects):
    r=next(r for r in records if r['kind']=='loan');p=r['p']
    effects.append(B('ISR2_bilateral_apply_principal_reduction',C(
        'set_country_flag = ISR2_bilateral_authorized_principal',
        public_debt('{ value = ISR2_bilateral_principal_reduction multiply = -1 }'),
        'clr_country_flag = ISR2_bilateral_authorized_principal')))
    payment=C(V('ISR2_bilateral_loan_principal_due',p+'_principal_instalment'),V('ISR2_bilateral_loan_interest_due',p+'_interest_instalment'),
        IF(check(p+'_weeks_remaining','<',2),C(V('ISR2_bilateral_loan_principal_due','ISR2_bilateral_loan_outstanding'),V('ISR2_bilateral_loan_interest_due',p+'_interest_remaining'))),
        V('ISR2_bilateral_loan_bill','ISR2_bilateral_loan_principal_due'),I('ISR2_bilateral_loan_bill','ISR2_bilateral_loan_interest_due'))
    pay=C(cash('{ value = ISR2_bilateral_loan_bill multiply = -1 }'),scoped('SOV',cash('ISR.ISR2_bilateral_loan_bill')),
        V('ISR2_bilateral_principal_reduction','ISR2_bilateral_loan_principal_due'),'ISR2_bilateral_apply_principal_reduction = yes',
        S('ISR2_bilateral_loan_outstanding','ISR2_bilateral_loan_principal_due'),S(p+'_interest_remaining','ISR2_bilateral_loan_interest_due'),S(p+'_weeks_remaining',1),V(p+'_payment_days',0),
        IF(check(p+'_weeks_remaining','<',1),C(V('ISR2_bilateral_loan_outstanding',0),V(p+'_interest_remaining',0),p+'_end = yes')))
    tick=IF(p+'_pair_clear = yes',C(I(p+'_payment_days',1),IF(check(p+'_payment_days','>=',7),C(payment,IF(check('treasury','>=','ISR2_bilateral_loan_bill'),pay)))))
    effects.append(B('ISR2_bilateral_loan_tick',tick))
    early=C(V('ISR2_bilateral_early_paid',0),V('ISR2_bilateral_early_due','ISR2_bilateral_early_repayment'),
        IF(check('ISR2_bilateral_early_due','>','ISR2_bilateral_loan_outstanding'),V('ISR2_bilateral_early_due','ISR2_bilateral_loan_outstanding')),
        IF(C(p+'_pair_clear = yes',check('ISR2_bilateral_early_due','>',0),check('treasury','>=','ISR2_bilateral_early_due')),
           C(V('ISR2_bilateral_loan_old_principal','ISR2_bilateral_loan_outstanding'),
             cash('{ value = ISR2_bilateral_early_due multiply = -1 }'),scoped('SOV',cash('ISR.ISR2_bilateral_early_due')),
             V('ISR2_bilateral_principal_reduction','ISR2_bilateral_early_due'),'ISR2_bilateral_apply_principal_reduction = yes',S('ISR2_bilateral_loan_outstanding','ISR2_bilateral_early_due'),
             V('ISR2_bilateral_early_paid','ISR2_bilateral_early_due'),
             B('set_variable',B(p+'_interest_remaining',f'value = {p}_interest_remaining\nmultiply = ISR2_bilateral_loan_outstanding\ndivide = ISR2_bilateral_loan_old_principal')),
             IF(check('ISR2_bilateral_loan_outstanding','<','.00001'),C(V('ISR2_bilateral_loan_outstanding',0),V(p+'_interest_remaining',0),p+'_end = yes'),
                 C(B('set_variable',B(p+'_principal_instalment',f'value = ISR2_bilateral_loan_outstanding\ndivide = {p}_weeks_remaining')),B('set_variable',B(p+'_interest_instalment',f'value = {p}_interest_remaining\ndivide = {p}_weeks_remaining')))))))
    effects.append(B('ISR2_bilateral_loan_early_repay',early))
