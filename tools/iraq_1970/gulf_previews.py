# IMPERIA COLD WAR — Prospective Gulf partnership focus effects.
"""Pure additions to already initialized focus rewards and English localisation.

Every new effect is enclosed in effect_tooltip. Country headings deliberately
use native country getters without entering a possibly absent country's scope.
Preview variables use the native add_to_variable tooltip RIGHT formatter and
never become a provider, money transfer, receipt or pending offer.
"""
from __future__ import annotations

P = 'COLDWAR_USA_gulf_'
Q = P + 'preview_'
HOSTS = ('TUR', 'SAU', 'ENG', 'FRA')
NORTH_HOSTS = (*HOSTS, 'PER')
LOCAL = ('KUR', 'PUK')
NORTH = (164, 633, 630, 1078)
MARK = '# IMPERIA COLD WAR — Non-executing prospective Gulf terms.'

# Labels and signed numeric formatters follow installed native MD modifier rows.
MODIFIERS = {
    'air_intercept_efficiency': ('$MODIFIER_AIR_INTERCEPT_EFFICIENCY$', '+=%1'),
    'air_superiority_efficiency': ('$MODIFIER_AIR_SUPERIORITY_EFFICIENCY$', '+=%1'),
    'airforce_personnel_cost_multiplier_modifier': ('$airforce_personnel_cost_multiplier_modifier$', '-=%1'),
    'cas_damage_reduction': ('$MODIFIER_CAS_DAMAGE_REDUCTION$', '+=%1'),
    'enemy_army_bonus_air_superiority_factor': ('$MODIFIER_ENEMY_ARMY_BONUS_AIR_SUPERIORITY_FACTOR$', '-=%1'),
    'army_personnel_cost_multiplier_modifier': ('$army_personnel_cost_multiplier_modifier$', '-=%1'),
    'defense_bonus_against': ('$MODIFIER_DEFENSE_BONUS_AGAINST_A_COUNTRY$ ([IRQ.GetNameDef])', '+=%1'),
    'production_speed_buildings_factor': ('$MODIFIER_PRODUCTION_SPEED_BUILDINGS_FACTOR$', '+=%1'),
    'bureaucracy_cost_multiplier_modifier': ('$bureaucracy_cost_multiplier_modifier$', '-=%1'),
    'tax_gain_multiplier_modifier': ('$tax_gain_multiplier_modifier$', '+=%1'),
    'state_repair_speed_infrastructure_factor': ('$modifier_state_repair_speed_infrastructure_factor$', '+=%1'),
    'local_supplies_for_controller': ('$MODIFIER_LOCAL_SUPPLIES_FOR_CONTROLLER$', '+=2'),
}


def _block(key, text):
    return key + ' = {\n' + '\n'.join('\t' + x for x in text.strip().splitlines()) + '\n}'


def _number(variable, value, tooltip):
    return f'add_to_variable = {{ {Q}{variable} = {value} tooltip = {Q}{tooltip}_tt }}'


def _cash(value):
    return _number('treasury', value, 'treasury')


def _weekly(value):
    return _number('weekly', value, 'weekly')


def _mods(values):
    return '\n'.join(_number(k, v, 'mod_' + k) for k, v in values.items())


def _idea(name, modifiers, days=None):
    effect = f'add_timed_idea = {{ idea = {name} days = {days} }}' if days else f'add_ideas = {name}'
    return effect + '\n' + _mods(modifiers)


def _country(tag, text):
    return f'custom_effect_tooltip = {Q}country_{tag}_tt\n' + text


def _section(loc, key, title, text, *, acceptance=True):
    loc[Q + key + '_tt'] = title
    lines = f'custom_effect_tooltip = {Q}{key}_tt\n'
    if acceptance:
        lines += 'custom_effect_tooltip = TT_IF_THEY_ACCEPT\n'
    return _block('effect_tooltip', lines + text)


def previews(loc):
    """Return source-derived, unconditional prospective effects by bare focus ID."""
    loc[Q + 'treasury_tt'] = 'Treasury: $RIGHT|+=2$ billion'
    loc[Q + 'weekly_tt'] = 'Weekly expenditure or income: $RIGHT|+=3$ billion/week'
    loc[Q + 'days_tt'] = 'Programme term: $RIGHT|0$ days'
    loc[Q + 'gdp_tt'] = 'Treasury contribution: $RIGHT|+=%1$ of annual GDP'
    loc[Q + 'autonomy_tt'] = '$COLDWAR_IRQ_kurdish_autonomy$: $RIGHT|%0$ autonomy'
    for tag in ('USA', 'IRQ', *NORTH_HOSTS, 'KUW', *LOCAL):
        loc[Q + 'country_' + tag + '_tt'] = '§Y[' + tag + '.GetNameDef]§!:'
    for key, (label, formatter) in MODIFIERS.items():
        loc[Q + 'mod_' + key + '_tt'] = label + ': $RIGHT|' + formatter + '$'
    out = {}
    # Each host contract has its own first invoice. The host receives access
    # commitments, not a cash transfer, idea, factory or automatic alliance.
    for focus, amount, kind in [('desert_shield', -2, 'Staging agreement'),
                                ('northern_access', -.5, 'Northern access agreement')]:
        groups = []
        for host in NORTH_HOSTS if focus == 'northern_access' else HOSTS:
            access = '\n'.join(f'diplomatic_relation = {{ country = {host} relation = {relation} active = yes }}'
                               for relation in ('military_access', 'air_base_access'))
            groups.append(_section(loc, focus + '_' + host,
                                   kind + ': [' + host + '.GetNameDef]',
                                   _country('USA', _cash(amount)) + '\n' + _country(host, access)))
        out[focus] = '\n'.join(groups)
    groups = []
    for tag in ('SAU', 'ENG', 'FRA', 'TUR', 'KUW'):
        groups.append(_section(loc, 'pledge_' + tag,
                               'Optional financial pledge: [' + tag + '.GetNameDef]',
                               _country('USA', _cash(.25)) + '\n' + _country(tag, _cash(-.25))))
    out['coalition'] = '\n'.join(groups)
    groups = []
    groups.append(_section(loc, 'arms_preparation', 'Initial arms offer preparation:',
                           'add_political_power = -25', acceptance=False))
    for tag in LOCAL:
        equipment = f'add_equipment_to_stockpile = {{ type = infantry_weapons_1 amount = 1000 producer = USA }}'
        groups.append(_section(loc, 'arms_' + tag, 'Initial arms package: [' + tag + '.GetNameDef]',
                               _country('USA', _cash(-.25) + '\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 producer = USA }')
                               + '\n' + _country(tag, _cash(.25) + '\n' + equipment)))
        groups.append(_section(loc, 'advisers_' + tag, 'Advisory contract: [' + tag + '.GetNameDef]',
                               _country('USA', _weekly(-.05) + '\n' + _number('days', 90, 'days'))
                               + '\n' + _country(tag, _weekly(.05) + '\n' + _idea('COLDWAR_KUR_us_advisers', {'defense_bonus_against': .08}, 90))))
    # The initial underground is an alternative to direct-country aid. Equipment
    # is already debited here; eventual cache acceptance must not repeat cash or
    # the donor deduction, and never invents a recipient before one exists.
    groups.append(_section(loc, 'underground_initial', 'Initial underground supply programme:',
        _country('USA', _cash(-.25)
                 + '\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 producer = USA }'
                 + '\n' + _weekly(-.05) + '\n' + _number('days', 90, 'days')), acceptance=False))
    for tag in LOCAL:
        groups.append(_section(loc, 'cache_' + tag, 'Recorded cache after a local rising: [' + tag + '.GetNameDef]',
            _country(tag, 'add_equipment_to_stockpile = { type = infantry_weapons_1 amount = 1000 producer = USA }')))
    out['arm_front'] = '\n'.join(groups)
    # The original No Fly reward already previews/starts the USA readiness idea.
    # Add its signed rows here without another Add Idea row; retain its original
    # native idea name/duration preview and real hidden start_air call unchanged.
    groups = [_section(loc, 'air_readiness', '$COLDWAR_USA_gulf_northern_air_readiness$:',
                       _country('USA', _mods({'air_intercept_efficiency': .15,
                                              'air_superiority_efficiency': .10,
                                              'airforce_personnel_cost_multiplier_modifier': .15})),
                       acceptance=False)]
    for tag in LOCAL:
        groups.append(_section(loc, 'air_cover_' + tag, 'Air-cover agreement: [' + tag + '.GetNameDef]',
                               _country(tag, _idea('COLDWAR_KUR_coalition_air_cover', {
                                   'cas_damage_reduction': .25, 'enemy_army_bonus_air_superiority_factor': -.20,
                                   'army_personnel_cost_multiplier_modifier': .05}, 90))))
    out['no_fly'] = '\n'.join(groups)
    for focus, amount, title in [('assembly', .25, 'Regional administration grant'),
                                 ('recovery', .5, 'Regional reconstruction grant')]:
        out[focus] = '\n'.join(_section(loc, focus + '_' + tag, title + ': [' + tag + '.GetNameDef]',
                                         _country('USA', _cash(-amount)) + '\n' + _country(tag, _cash(amount)))
                                for tag in LOCAL)
    # First-time Iraqi agreement invoice is 2% of GDP, committed by quote_accord.
    # An existing invoice is not invented as a zero-valued preview variable.
    iraq = _number('gdp', -.02, 'gdp') + '\n' + _idea(P + 'recognised_budget', {
        'army_personnel_cost_multiplier_modifier': -.08, 'tax_gain_multiplier_modifier': -.02})
    iraq += '\n' + _block('IRQ', '\n'.join(
        f'set_autonomy = {{ target = {tag} autonomy_state = COLDWAR_IRQ_kurdish_autonomy freedom_level = 0.8 end_wars = yes end_civil_wars = yes }}'
        for tag in LOCAL))
    local = []
    for tag in LOCAL:
        local.append(_country(tag, _number('autonomy', .8, 'autonomy') + '\n' + _idea(P + 'recognised_development', {
            'production_speed_buildings_factor': .08, 'bureaucracy_cost_multiplier_modifier': .03})))
    out['baghdad_accord'] = _section(loc, 'accord_preparation', 'Autonomy negotiations:',
                                     'add_political_power = -25', acceptance=False)
    out['baghdad_accord'] += '\n' + _section(loc, 'recognised_settlement', 'Recognised northern settlement:',
                                            _country('USA', _weekly(-.025) + '\n' + _number('days', 90, 'days'))
                                            + '\n' + _country('IRQ', iraq) + '\n' + '\n'.join(local))
    protected = '\n'.join(_country(tag, _idea(P + 'external_guarantee', {
        'army_personnel_cost_multiplier_modifier': .05, 'defense_bonus_against': .05})) for tag in LOCAL)
    # External ratification starts the same actual American readiness programme.
    readiness = _idea(P + 'northern_air_readiness', {
        'air_intercept_efficiency': .15, 'air_superiority_efficiency': .10,
        'airforce_personnel_cost_multiplier_modifier': .15}, 90)
    out['self_rule'] = _section(loc, 'external_preparation', 'Protection negotiations:',
                               'add_political_power = -25', acceptance=False)
    out['self_rule'] += '\n' + _section(loc, 'external_protection', 'External protection commitment:',
                                       _country('USA', _weekly(-.05) + '\n' + _number('days', 90, 'days') + '\n' + readiness)
                                       + '\n' + protected)
    out['self_rule'] += '\n' + _section(loc, 'external_logistics', '$COLDWAR_USA_gulf_protection_local$:',
        '\n'.join(_block(str(state), f'add_dynamic_modifier = {{ modifier = {P}protection_local days = 90 }}\n'
                              + _mods({'local_supplies_for_controller': .10})) for state in NORTH))
    for tag in LOCAL:
        out['self_rule'] += '\n' + _section(loc, 'external_air_cover_' + tag,
            'Air-cover agreement: [' + tag + '.GetNameDef]',
            _country(tag, _idea('COLDWAR_KUR_coalition_air_cover', {
                'cas_damage_reduction': .25, 'enemy_army_bonus_air_superiority_factor': -.20,
                'army_personnel_cost_multiplier_modifier': .05}, 90)))
    for key in ('baghdad_accord', 'self_rule'):
        # Both initial negotiations are25PP; switching an already selected policy
        # costs100PP and.25 only at actual new commitment, not on focus completion.
        out[key] += '\n' + _section(loc, key + '_revision_preparation', 'Negotiations to change the northern commitment:',
                                    _country('USA', 'add_political_power = -100'), acceptance=False)
        out[key] += '\n' + _section(loc, key + '_revision', 'Change of northern commitment:',
                                    _country('USA', _cash(-.25)))
    out['self_rule'] += '\n' + _section(loc, 'escalation', 'Expanded protection mandate:',
        _country('USA', 'add_political_power = -100\n' + _cash(-.5)
                 + '\ncreate_wargoal = { type = liberate_wargoal target = IRQ expire = 60 }'), acceptance=False)
    # Recovery unlocks each local authority's separately paid development.
    for tag in LOCAL:
        for state in NORTH:
            development = _block(str(state), 'add_extra_state_shared_building_slots = 1\nadd_building_construction = { type = infrastructure level = 1 instant_build = yes }')
            out['recovery'] += '\n' + _section(loc, 'local_rebuild_' + tag + '_' + str(state),
                'Local reconstruction: [' + tag + '.GetNameDef], $STATE_' + str(state) + '$',
                _country(tag, _cash(-.2)) + '\n' + development, acceptance=False)
    for key, rate in [('comfort', -.025), ('limited_war', -.02)]:
        out[key] = _section(loc, key + '_relief', ('Standard refugee relief:' if key == 'comfort' else 'Limited-war refugee relief:'),
                            _country('USA', _cash(-.5) + '\n' + _weekly(rate) + '\n' + _number('days', 90, 'days'))
                            + '\n' + '\n'.join(_block(str(state), f'add_dynamic_modifier = {{ modifier = {P}relief_local days = 90 }}\n'
                                                               + _mods({'state_repair_speed_infrastructure_factor': .25})) for state in NORTH),
                            acceptance=False)
    out['comfort'] += '\n' + _section(loc, 'comfort_limited_relief', 'Limited-war refugee relief:',
        _country('USA', _cash(-.5) + '\n' + _weekly(-.02) + '\n' + _number('days', 90, 'days')),
        acceptance=False)
    out['safe_haven'] = _section(loc, 'safe_haven', 'Northern safe-haven logistics:',
                                 _country('USA', _weekly(-.05) + '\n' + _number('days', 90, 'days'))
                                 + '\n' + '\n'.join(_block(str(state), f'add_dynamic_modifier = {{ modifier = {P}protection_local days = 90 }}\n'
                                                                    + _mods({'local_supplies_for_controller': .10})) for state in NORTH),
                                 acceptance=False)
    return out


def apply_previews(rewards: dict[str, str], loc: dict[str, str]) -> None:
    """Prefix full non-executing terms; all original execution remains intact."""
    additions = previews(loc)
    missing = additions.keys() - rewards.keys()
    if missing:
        raise ValueError('Initialize the original focus rewards before previews: ' + ', '.join(sorted(missing)))
    for key, prefix in additions.items():
        if MARK in rewards[key]:
            continue
        original = rewards[key]
        if key == 'no_fly':
            original = original.replace('custom_effect_tooltip = ' + P + 'air_offers_tt', '')
        rewards[key] = MARK + '\n' + prefix + '\n' + original
