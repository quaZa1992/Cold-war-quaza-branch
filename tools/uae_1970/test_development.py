# IMPERIA CW — Cold War: uae 1970 — test development.
"""Exercise installed costly industrialisation and population route rewards."""
import copy
import json
from pathlib import Path

from test_focus_runtime import World, T, E, P, D, parse, first

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def run():
    cases = []
    def parents(world, key):
        node = next(n for n in D['nodes'] if n['id'] == P+key)
        for row in node['prerequisites']:
            world.flags[P+'done_'+row[0].removeprefix(P)] = None
    w = World(); w.variables['treasury'] = -1; parents(w, 'industrial_port')
    w.call('apply_industrial_port'); w.call('apply_industrial_port')
    assert w.states[179]['industrial_complex'] == 1 and w.variables['treasury'] == -8.5 and not w.queue
    cases.append('The105-day industrial port commissions its first realCIC for7.5bn once even at negative treasury, without a zero-CIC construction deadlock')
    w = World(); parents(w, 'aviation_hub'); w.variables['treasury'] = 2.5
    w.call('apply_aviation_hub'); w.call('apply_aviation_hub')
    assert w.states[179]['air_base'] == 1 and w.states[179]['slots'] == 3 and w.variables['treasury'] == 0 and not w.queue
    assert not w.test(T[P+'can_apply_industrial_port'])
    full = World(); parents(full, 'aviation_hub'); full.states[179]['air_base'] = 10
    full.call('apply_aviation_hub'); assert full.variables['treasury'] == 10
    cases.append('The2.5bn airport commissions one airbase with no shared slot, respects level10, and preserves the exclusive industry choice')
    for key, state, resource, amount, cost, burden in [
        ('jebel_ali_smelter', 179, 'aluminium', 12, 4.5, .12),
        ('steel_rolling_mills', 180, 'steel', 5, 3.0, .06),
    ]:
        w = World(); parents(w, key)
        w.variables['treasury'] = cost
        w.call('apply_'+key)
        assert w.states[state][resource] == 0 and w.variables['treasury'] == cost
        w.states[179]['industrial_complex'] = 1
        w.variables['treasury'] = cost; w.states[state]['controller'] = 'ENG'; w.call('apply_'+key)
        assert w.states[state][resource] == 0 and w.variables['treasury'] == cost
        w.states[state]['controller'] = 'UAE'
        w.variables['treasury'] = -1
        w.call('apply_'+key); w.call('apply_'+key)
        assert w.states[state][resource] == amount and w.variables['treasury'] == -1-cost
        assert abs(w.variables[P+'commerce_energy_use_multiplier']-burden) < 1e-9
        w.states[state]['controller'] = 'ENG'; w.call('refresh_programmes')
        assert w.variables[P+'commerce_energy_use_multiplier'] == 0
        w.states[state]['controller'] = 'UAE'; w.call('refresh_programmes')
        assert w.states[state][resource] == amount and w.variables['treasury'] == -1-cost
        assert abs(w.variables[P+'commerce_energy_use_multiplier']-burden) < 1e-9
    cases.append('Both metals require a finishedCIC and recipient control; full cost debits once even below zero and energy burden suspends under occupation')
    w = World(); w.variables['treasury'] = 7.5; w.states[179]['industrial_complex'] = 1
    for key in ['jebel_ali_smelter', 'steel_rolling_mills']:
        parents(w, key); w.call('apply_'+key)
    assert w.states[179]['aluminium'] == 12 and w.states[180]['steel'] == 5 and w.variables['treasury'] == 0
    assert abs(w.variables[P+'commerce_energy_use_multiplier']-.18) < 1e-9
    before = copy.deepcopy((w.states, w.variables['treasury']))
    w.call('refresh_programmes'); w.call('refresh_programmes')
    assert before == (w.states, w.variables['treasury'])
    cases.append('Complementary metal projects total7.5bn and+18% energy; refresh repeats no resources or payments')
    # Test actual focus-guard chain through each mutually exclusive population
    # route, not only a sum of modifier catalogue rows.
    for workforce, expected_growth, expected_cost in [(False, 1.60, 1.69), (True, 2.00, 1.54)]:
        w = World(); w.variables['treasury'] = 10
        route = ['schools_clinics', 'foreign_specialists' if workforce else 'national_training', 'water_network',
                 'worker_towns' if workforce else 'citizen_housing', 'technical_institutes', 'efficient_services']
        for key in route:
            assert w.test(T[P+'can_apply_'+key]), key
            w.call('apply_'+key)
            assert w.has_flag(P+'done_'+key), key
        assert abs(w.variables[P+'society_monthly_population']-expected_growth) < 1e-9
        assert abs((10-w.variables['treasury'])-expected_cost) < 1e-9
        other = 'citizen_housing' if workforce else 'worker_towns'
        assert not w.test(T[P+'can_apply_'+other])
        before = copy.deepcopy((w.states, w.variables['treasury']))
        w.variables['ruling_party'] = 2; w.governments = {'western_liberals_are_in_power'}; w.call('refresh_programmes')
        assert abs(w.variables[P+'society_monthly_population']-expected_growth) < 1e-9
        assert before == (w.states, w.variables['treasury'])
    cases.append('Reachable exclusive population routes grant+160% or+200% growth at1.69/1.54bn; earned services survive party change without replay')
    w = World()
    for key in ['schools_clinics', 'water_network', 'citizen_housing', 'worker_towns', 'efficient_services']:
        w.flags[P+'done_'+key] = None
    w.call('refresh_programmes')
    assert w.variables[P+'society_monthly_population'] == 2.0
    snapshot = copy.deepcopy((w.states, w.variables['treasury']))
    w.call('refresh_programmes'); w.call('refresh_programmes')
    assert w.variables[P+'society_monthly_population'] == 2.0 and snapshot == (w.states, w.variables['treasury'])
    cases.append('The total tree growth stays capped at+200% even with both normally exclusive housing flags and repeated refresh')
    start = (ROOT/'common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt').read_text(encoding='utf-8')
    effects = {k:v for k,_,v in parse(start)}
    early = first(effects[P+'startup_pre_economy'], 'if')
    keys = [key for key, _, _ in early]
    assert keys.index(P+'startup_industry') < keys.index('if')
    assert 'IMP_1970_gdp_profile_applied' not in str(E[P+'apply_jebel_ali_smelter'])
    tree = first(parse((ROOT/'common/national_focus/COLDWAR_UAE_1970_focus.txt').read_text(encoding='utf-8')), 'focus_tree')
    for _, _, focus in [r for r in tree if r[0] == 'focus']:
        preview = first(first(focus, 'completion_reward'), 'effect_tooltip')
        assert not any(key in {'ingame_update_setup', 'set_country_flag'} for key,_,_ in preview)
    cases.append('Industrial baseline precedes economic freeze; paid expansions preserve GDP offset and native reward previews omit internal refresh/receipt leaves')
    report = {'passed': len(cases), 'cases': cases, 'errors': [], 'engine_tested': False}
    (HERE/'development_validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
