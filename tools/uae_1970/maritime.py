# IMPERIA CW — Cold War: uae 1970 — maritime.
"""Shared native arithmetic for the coastal economy's transition towards oil.

Only the named maritime sources scale. The rest of the commerce programme,
including industrial facilities, remains independent of this transition.
"""
P = 'COLDWAR_UAE_'
OIL_PHASES = ('oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase')
MARITIME_FOCUSES = frozenset(('trading_coast', 'port_planning'))
SCALED_MODIFIERS = ('agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier')
SCALE_FLOOR = .20
SCALE_STEP = .20
LIVE_SCALE = P+'maritime_retained_share'


def scale_effect(variable, *, temporary=False, prospective=None):
    """Count delivered phases once, independent of order, ownership or party."""
    kind = 'temp_variable' if temporary else 'variable'
    rows = [f'set_{kind} = {{ {variable} = 1 }}']
    for phase in OIL_PHASES:
        condition = 'always = yes' if prospective == phase else 'has_country_flag = '+P+'done_'+phase
        rows.append('if = {\n\tlimit = { '+condition+' }\n\t'
                    f'subtract_from_{kind} = {{ {variable} = {SCALE_STEP:g} }}\n'+'}')
    rows.append(f'clamp_{kind} = {{ var = {variable} min = {SCALE_FLOOR:g} max = 1 }}')
    return '\n'.join(rows)


def scaled_value(variable, value, scale, *, temporary=True):
    kind = 'temp_variable' if temporary else 'variable'
    return (f'set_{kind} = {{ {variable} = {value:g} }}\n'
            f'multiply_{kind} = {{ {variable} = {scale} }}')
