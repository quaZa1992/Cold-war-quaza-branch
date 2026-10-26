# IMPERIA CW — Cold War: uae 1970 — test maritime.
"""Exercise actual maritime income/social relief, oil transition and once-only costs."""
import copy
import json
import math
from pathlib import Path

from test_focus_runtime import World, P, D, T

HERE = Path(__file__).resolve().parent
OIL_PHASES = ('oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase')
SPIRIT = P+'maritime_livelihoods'


def parents(world, key):
    node = next(n for n in D['nodes'] if n['id'] == P+key)
    for row in node['prerequisites']:
        world.flags[P+'done_'+row[0].removeprefix(P)] = None


def earn(world, key):
    parents(world, key)
    assert world.test(T[P+'can_apply_'+key]), key
    world.call('apply_'+key)
    assert world.has_flag(P+'done_'+key), key


def near(actual, expected):
    assert math.isclose(actual, expected, abs_tol=1e-9), (actual, expected)


def balances(world):
    return copy.deepcopy((world.states, world.variables['treasury'], world.queue, world.xp))


def maritime_state(world):
    return tuple(world.variables.get(P+prefix+'_'+modifier, 0) for prefix, modifier in (
        ('maritime_livelihoods', 'agricolture_productivity_modifier'),
        ('maritime_livelihoods', 'offices_productivity'),
        ('maritime_livelihoods', 'social_cost_multiplier_modifier'),
        ('maritime_livelihoods', 'country_productivity_growth_modifier'),
        ('commerce', 'agricolture_productivity_modifier'), ('commerce', 'offices_productivity'),
        ('commerce', 'social_cost_multiplier_modifier'), ('commerce', 'energy_use_multiplier'),
        ('commerce', 'bureaucracy_cost_multiplier_modifier'), ('commerce', 'production_speed_naval_base_factor')))


def run():
    cases = []
    w = World(); w.call('refresh_programmes')
    assert SPIRIT in w.dynamic
    for modifier, expected in [('agricolture_productivity_modifier', .10), ('offices_productivity', .03),
                               ('social_cost_multiplier_modifier', -.05), ('country_productivity_growth_modifier', -.05)]:
        near(w.variables[SPIRIT+'_'+modifier], expected)
    before = balances(w); w.call('refresh_programmes'); assert before == balances(w)
    cases.append('Starting real carrier: primary+10%, commerce+3%, social cost-5% and inherited growth-5%; refresh creates no cash or assets')

    w.variables['treasury'] = -.5
    earn(w, 'trading_coast'); w.call('apply_trading_coast')
    near(w.variables['treasury'], -.60)
    near(w.variables[P+'commerce_agricolture_productivity_modifier'], .10)
    near(w.variables[P+'commerce_offices_productivity'], .06)
    near(w.variables[P+'commerce_social_cost_multiplier_modifier'], -.02)
    near(w.variables[SPIRIT+'_country_productivity_growth_modifier'], -.05)
    earn(w, 'port_planning'); w.call('apply_port_planning')
    near(w.variables['treasury'], -.75)
    near(w.variables[P+'commerce_agricolture_productivity_modifier'], .20)
    near(w.variables[P+'commerce_social_cost_multiplier_modifier'], -.05)
    near(w.variables[P+'commerce_energy_use_multiplier'], .02)
    near(w.variables[SPIRIT+'_country_productivity_growth_modifier'], 0)
    assert SPIRIT in w.dynamic
    cases.append('Two fisheries focuses fully debit0.10/0.15bn once into negative balances, add sector/social benefits and remove only the inherited growth penalty')

    earn(w, 'free_zone')
    # Each phase subtracts20% of ORIGINAL maritime bonuses, not20% of
    # the remaining level. Unrelated new commerce retains its full amount.
    for phase, factor in zip(OIL_PHASES, (.8, .6, .4, .2)):
        earn(w, phase)
        for prefix, modifier, original in [
            ('maritime_livelihoods', 'agricolture_productivity_modifier', .10),
            ('maritime_livelihoods', 'offices_productivity', .03),
            ('maritime_livelihoods', 'social_cost_multiplier_modifier', -.05),
            ('commerce', 'agricolture_productivity_modifier', .20),
            ('commerce', 'social_cost_multiplier_modifier', -.05),
        ]:
            near(w.variables[P+prefix+'_'+modifier], original*factor)
        near(w.variables[P+'commerce_offices_productivity'], .10+.06*factor)
        near(w.variables[P+'commerce_production_speed_naval_base_factor'], .15)
        near(w.variables[P+'commerce_bureaucracy_cost_multiplier_modifier'], .08)
        near(w.variables[P+'commerce_energy_use_multiplier'], .02)
        near(w.variables[SPIRIT+'_country_productivity_growth_modifier'], 0)
        snapshot = balances(w), maritime_state(w)
        w.call('apply_'+phase); w.call('refresh_programmes'); w.call('refresh_programmes')
        assert snapshot == (balances(w), maritime_state(w))
    cases.append('All four actual oil rewards reduce original maritime income/social relief to80/60/40/20%, retaining free-zone commerce, harbour construction/admin/energy and no replay')

    late = World(); late.variables['treasury'] = -.5
    for phase in OIL_PHASES:
        earn(late, phase)
    near(late.variables[SPIRIT+'_country_productivity_growth_modifier'], -.05)
    earn(late, 'trading_coast'); earn(late, 'port_planning'); earn(late, 'free_zone')
    assert all(math.isclose(a, b, abs_tol=1e-9) for a, b in zip(maritime_state(late), maritime_state(w)))
    near(late.variables['treasury'], w.variables['treasury'])
    assert late.states == w.states
    cases.append('Oil-first and fisheries-first orders converge; late fisheries investment receives only the remaining20% scale and still removes the transition penalty')

    snapshot = balances(late), maritime_state(late)
    for party, governments in [(2, {'western_liberals_are_in_power'}), (0, {'western_autocrats_are_in_power'})]:
        late.variables['ruling_party'] = party; late.governments = governments
        late.call('refresh_programmes')
        assert snapshot == (balances(late), maritime_state(late))
    assert late.variables[P+'society_monthly_population'] <= 2
    cases.append('Government departure/return and repeated refresh preserve scaled durable maritime livelihoods without replay or growth-cap leakage')
    report = {'passed': len(cases), 'cases': cases, 'engine_tested': False}
    (HERE/'maritime_validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
