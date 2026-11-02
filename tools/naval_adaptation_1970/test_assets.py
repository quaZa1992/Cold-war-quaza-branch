# IMPERIA COLD WAR — Native naval asset transaction source models.
"""Focused emitted-AST checks. No gameplay outputs and no engine claims."""
from __future__ import annotations

import copy
from decimal import Decimal
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.append(str(ROOT / 'tools/vietnam_1970'))
from assets import asset_package
from script_ast import parse, first, walk


class Model:
    def __init__(self, variant='bluewater', treasury='100', gdp='10'):
        self.profile = dict(country='USA', variant=variant,
            port_targets=[dict(state=101, province=1001, name='Primary'), dict(state=102, province=1002, name='Fallback')],
            yard_targets=[dict(state=101, name='Primary'), dict(state=102, name='Fallback')])
        self.country = dict(tag='USA', flags=set(), provinces={1001, 1002}, vars={'treasury': Decimal(treasury), 'gdp_total': Decimal(gdp)})
        self.root = self.country
        self.states = {str(s):dict(state=s, owner='USA', controller='USA', coast=True, free=8,
            levels={'dockyard': 1, 'arms_factory': 1}, ports={p: 1}) for s, p in ((101, 1001), (102, 1002))}
        definitions = first(parse((ROOT / 'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')), 'buildings')
        self.definitions = {k:first(definitions, k) for k in ('dockyard', 'arms_factory', 'naval_base')}
        self.trace = []
        self.quote()

    def quote(self):
        d = self.country['vars'];coastal = self.profile['variant'] == 'coastal'
        d['COLDWAR_NAVY_USA_port_quote'] = d['gdp_total'] * Decimal('.002') if coastal else Decimal('.5')
        d['COLDWAR_NAVY_USA_yard_quote'] = d['gdp_total'] * Decimal('.008') if coastal else Decimal('7.5')
        d['COLDWAR_NAVY_USA_yard_2_quote'] = d['COLDWAR_NAVY_USA_yard_quote'] * 2

    def target(self, key):
        if key == 'ROOT':return self.root
        return self.states.get(key)

    def num(self, value, scope):
        try:return Decimal(str(value))
        except Exception:return scope.get('vars', {}).get(value, Decimal(0))

    def compare(self, a, op, b):
        return {'>':lambda:a>b, '>=':lambda:a>=b, '<':lambda:a<b, '<=':lambda:a<=b, '=':lambda:a==b}[op]()

    def conditions(self, rows, scope):
        for key, op, value in rows:
            if key == 'AND':ok = self.conditions(value, scope)
            elif key == 'OR':ok = any(self.conditions([r], scope) for r in value)
            elif key == 'NOT':ok = not self.conditions(value, scope)
            elif key == 'tag':ok = scope.get('tag') == value
            elif key == 'controls_a_coastal_state':ok = any(s['controller'] == scope['tag'] and s['coast'] for s in self.states.values()) == (value == 'yes')
            elif key == 'has_country_flag':ok = value in scope['flags']
            elif key in ('owns_state', 'controls_state'):ok = self.states[value]['owner' if key == 'owns_state' else 'controller'] == scope['tag']
            elif key == 'controls_province':ok = int(value) in scope['provinces']
            elif key == 'is_owned_and_controlled_by':ok = scope['owner'] == scope['controller'] == value
            elif key == 'is_coastal':ok = scope['coast'] == (value == 'yes')
            elif key == 'check_variable':
                if first(value, 'var') is not None:
                    left = self.num(first(value, 'var'), scope);right = self.num(first(value, 'value'), scope)
                    compare = {'greater_than_or_equals': '>=', 'greater_than': '>', 'equals': '='}[first(value, 'compare')]
                else:
                    ident, compare, amount = value[0];left = self.num(ident, scope);right = self.num(amount, scope)
                ok = self.compare(left, compare, right)
            elif key == 'free_building_slots':
                building = first(value, 'building');definition = first(self.definitions[building], 'level_cap')
                province = first(value, 'province');_, compare, required = next(r for r in value if r[0] == 'size')
                if building == 'naval_base':
                    assert first(value, 'include_locked') is None
                    assert province is not None
                    free = int(first(definition, 'province_max')) - scope['ports'].get(int(province), int(first(definition, 'province_max')))
                else:
                    assert first(definition, 'shares_slots') == 'yes' and first(value, 'include_locked') == 'no'
                    assert province is None
                    free = min(int(first(definition, 'state_max')) - scope['levels'][building], scope['free'])
                ok = self.compare(Decimal(free), compare, Decimal(required))
            elif self.target(key) is not None:ok = self.conditions(value, self.target(key))
            else:raise AssertionError(('Unmodeled trigger', key, op, value))
            if not ok:return False
        return True

    def execute(self, rows, scope):
        branch = False
        for key, _, value in rows:
            if key == 'if':
                branch = self.conditions(first(value, 'limit', []), scope)
                if branch:self.execute([r for r in value if r[0] != 'limit'], scope)
            elif key == 'else_if':
                if not branch and self.conditions(first(value, 'limit', []), scope):
                    self.execute([r for r in value if r[0] != 'limit'], scope);branch = True
            elif key == 'effect_tooltip':pass
            elif self.target(key) is not None:self.execute(value, self.target(key))
            elif key == 'set_temp_variable':
                name, _, amount = value[0];scope['vars'][name] = self.num(amount, scope)
            elif key == 'multiply_temp_variable':
                name, _, amount = value[0];scope['vars'][name] *= self.num(amount, scope)
            elif key == 'modify_treasury_effect':
                assert 'MD_skip_treasury_cost' not in scope['flags']
                scope['vars']['treasury'] += scope['vars']['treasury_change'];self.trace.append(('fee', scope['vars']['treasury_change']))
            elif key == 'add_extra_state_shared_building_slots':
                scope['free'] += int(value);self.trace.append(('slot', scope['state'], int(value)))
            elif key == 'add_building_construction':
                building = first(value, 'type');count = int(first(value, 'level'));assert first(value, 'instant_build') == 'yes'
                self.trace.append(('build', scope['state'], building, count))
                definition = first(self.definitions[building], 'level_cap')
                if building == 'naval_base':
                    province = int(first(value, 'province'));scope['ports'][province] += count
                    assert scope['ports'][province] <= int(first(definition, 'province_max'))
                else:
                    scope['levels'][building] += count;scope['free'] -= count
                    assert scope['levels'][building] <= int(first(definition, 'state_max'))
            else:raise AssertionError(('Unmodeled effect', key, value))

    def package(self, kind, count=1):return asset_package(self.profile, kind, count)
    def ready(self, kind, count=1):return self.conditions(parse(self.package(kind, count)['ready']), self.country)
    def run(self, kind, count=1):self.execute(parse(self.package(kind, count)['execute']), self.country)

    def visible_preview(self, rows, scope=None):
        """Resolve native preview conditions without running material effects."""
        scope = self.country if scope is None else scope
        result = [];branch = False
        for key, op, value in rows:
            if key == 'effect_tooltip':result.extend(self.visible_preview(value, scope))
            elif key == 'if':
                branch = self.conditions(first(value, 'limit', []), scope)
                if branch:result.extend(self.visible_preview([r for r in value if r[0] != 'limit'], scope))
            elif key == 'else_if':
                if not branch and self.conditions(first(value, 'limit', []), scope):
                    result.extend(self.visible_preview([r for r in value if r[0] != 'limit'], scope));branch = True
            elif key == 'else':
                if not branch:result.extend(self.visible_preview(value, scope))
                branch = True
            elif self.target(key) is not None:result.extend(self.visible_preview(value, self.target(key)))
            else:result.append((scope.get('tag', scope.get('state')), key, op, value))
        return result


class AssetTests(unittest.TestCase):
    def test_first_valid_priority_charges_once_and_builds_one_target(self):
        m = Model();m.run('port')
        self.assertEqual(m.country['vars']['treasury'], Decimal('99.5'))
        self.assertEqual(m.states['101']['ports'][1001], 2);self.assertEqual(m.states['102']['ports'][1002], 1)
        self.assertEqual(m.trace, [('fee', Decimal('-.5')), ('slot', 101, 1), ('build', 101, 'naval_base', 1)])

    def test_lost_owner_or_control_uses_only_next_valid_target(self):
        for field in ('owner', 'controller'):
            with self.subTest(field=field):
                m = Model();m.states['101'][field] = 'SOV';m.run('yard')
                self.assertEqual(m.states['101']['levels']['dockyard'], 1);self.assertEqual(m.states['102']['levels']['dockyard'], 2)
                self.assertEqual(m.country['vars']['treasury'], Decimal('92.5'));self.assertEqual(len([t for t in m.trace if t[0] == 'fee']), 1)

    def test_lost_port_province_cannot_grant_the_primary_port(self):
        m = Model();m.country['provinces'].remove(1001);m.run('port')
        self.assertEqual(m.states['101']['ports'][1001], 1);self.assertEqual(m.states['102']['ports'][1002], 2)
        self.assertEqual(m.country['vars']['treasury'], Decimal('99.5'))
        m = Model();m.root = dict(tag='SOV', provinces=set());self.assertFalse(m.ready('port'))

    def test_full_ports_or_shared_state_caps_charge_nothing(self):
        for kind in ('port', 'yard', 'arms'):
            with self.subTest(kind=kind):
                m = Model()
                for state in m.states.values():
                    if kind == 'port':state['ports'] = {p:10 for p in state['ports']}
                    else:
                        building = 'dockyard' if kind == 'yard' else 'arms_factory';definition = first(m.definitions[building], 'level_cap')
                        state['levels'][building] = int(first(definition, 'state_max'))
                before = copy.deepcopy((m.country, m.states));self.assertFalse(m.ready(kind));m.run(kind)
                self.assertEqual(before, (m.country, m.states));self.assertFalse(m.trace)

    def test_two_yards_are_a_complete_same_state_package(self):
        m = Model();m.profile['yard_targets'] = m.profile['yard_targets'][:1];m.run('yard', 2)
        self.assertEqual(m.states['101']['levels']['dockyard'], 3);self.assertEqual(m.states['102']['levels']['dockyard'], 1)
        self.assertEqual(m.country['vars']['treasury'], Decimal(85))
        self.assertEqual(m.trace, [('fee', Decimal(-15)), ('slot', 101, 2), ('build', 101, 'dockyard', 2)])

    def test_two_yards_do_not_split_a_partial_one_level_capacity(self):
        m = Model()
        for state in m.states.values():state['levels']['dockyard'] = 19
        self.assertTrue(m.ready('yard'));self.assertFalse(m.ready('yard', 2))
        before = copy.deepcopy((m.country, m.states));m.run('yard', 2);self.assertEqual(before, (m.country, m.states))

    def test_shared_free_capacity_is_checked_before_promised_extra_slots(self):
        m = Model()
        for state in m.states.values():state['free'] = 0
        self.assertFalse(m.ready('yard'));self.assertFalse(m.ready('arms'));self.assertTrue(m.ready('port'))

    def test_actual_execution_rechecks_funds_and_skip_after_readiness(self):
        for condition in ('funds', 'skip'):
            with self.subTest(condition=condition):
                m = Model();self.assertTrue(m.ready('yard', 2))
                if condition == 'funds':m.country['vars']['treasury'] = Decimal('14.99999')
                else:m.country['flags'].add('MD_skip_treasury_cost')
                before = copy.deepcopy((m.country, m.states));m.run('yard', 2)
                self.assertEqual(before, (m.country, m.states));self.assertFalse(m.trace)

    def test_coastal_prices_and_zero_gdp_fail_closed(self):
        for kind, count, price in [('port', 1, '.02'), ('yard', 1, '.08'), ('yard', 2, '.16')]:
            with self.subTest(kind=kind, count=count):
                m = Model('coastal');m.run(kind, count);self.assertEqual(m.country['vars']['treasury'], Decimal(100) - Decimal(price))
                m = Model('coastal', gdp='0');m.country['vars']['COLDWAR_NAVY_USA_'+('yard_2' if kind == 'yard' and count == 2 else kind)+'_quote'] = Decimal(1)
                self.assertFalse(m.ready(kind, count));m.run(kind, count);self.assertFalse(m.trace)

    def test_uninitialized_quotes_wrong_tag_and_no_coast_grant_nothing(self):
        for condition in ('quote', 'tag', 'coast'):
            m = Model()
            if condition == 'quote':m.country['vars']['COLDWAR_NAVY_USA_port_quote'] = Decimal(0)
            elif condition == 'tag':m.country['tag'] = 'SOV'
            else:
                for state in m.states.values():state['coast'] = False
            before = copy.deepcopy((m.country, m.states));m.run('port');self.assertEqual(before, (m.country, m.states));self.assertFalse(m.trace)

    def test_free_arms_factory_has_no_quote_or_money_transaction(self):
        m = Model('coastal', treasury='0', gdp='0');m.run('arms')
        self.assertEqual(m.country['vars']['treasury'], 0);self.assertEqual(m.states['101']['levels']['arms_factory'], 2)
        self.assertEqual(m.trace, [('slot', 101, 1), ('build', 101, 'arms_factory', 1)])
        m = Model();m.country['flags'].add('MD_skip_treasury_cost');m.run('arms');self.assertFalse(m.trace)

    def test_locked_previews_are_complete_and_nonexecuting(self):
        for kind, count in [('port', 1), ('yard', 2), ('arms', 1)]:
            m = Model(treasury='0');m.country['provinces'].clear()
            for state in m.states.values():state['owner'] = 'SOV'
            package = m.package(kind, count);preview = parse(package['preview'])
            self.assertEqual([k for k, _, v in preview], ['effect_tooltip'])
            visible = m.visible_preview(preview)
            self.assertTrue(any(k == 'add_extra_state_shared_building_slots' and v == str(count) for _, k, _, v in visible))
            self.assertTrue(any(k == 'add_building_construction' and first(v, 'level') == str(count) for _, k, _, v in visible))
            self.assertEqual([s for s, k, _, v in visible if k == 'add_building_construction'], [101])
            if kind != 'arms':self.assertTrue(any(k == 'modify_treasury_effect' for _, k, _, v in visible))
            before = copy.deepcopy((m.country, m.states));m.execute(preview, m.country);self.assertEqual(before, (m.country, m.states));self.assertFalse(m.trace)

    def test_canonical_blue_water_variant_and_legacy_spelling_match(self):
        m = Model();canonical = copy.deepcopy(m.profile);canonical['variant'] = 'blue_water'
        for kind, count in [('port', 1), ('yard', 2), ('arms', 1)]:
            self.assertEqual(asset_package(canonical, kind, count), m.package(kind, count))

    def test_preview_priority_matches_execution_fallback_without_money_gate(self):
        for kind, count in [('port', 1), ('yard', 2), ('arms', 1)]:
            m = Model();m.states['101']['controller'] = 'SOV'
            package = m.package(kind, count);before = copy.deepcopy((m.country, m.states))
            visible = m.visible_preview(parse(package['preview']))
            self.assertEqual([s for s, k, _, v in visible if k == 'add_building_construction'], [102])
            self.assertEqual(before, (m.country, m.states))
            m.run(kind, count)
            self.assertEqual([t[1] for t in m.trace if t[0] == 'build'], [102])
            # The very same candidate remains visible without funds or while
            # runtime bookkeeping blocks execution outside this pure package.
            m = Model(treasury='0');m.states['101']['controller'] = 'SOV'
            m.country['flags'].update({'MD_skip_treasury_cost', 'COLDWAR_NAVY_USA_example_done'})
            visible = m.visible_preview(parse(m.package(kind, count)['preview']))
            self.assertEqual([s for s, k, _, v in visible if k == 'add_building_construction'], [102])
            preview = parse(m.package(kind, count)['preview'])
            for key, _, body in walk(preview):
                if key == 'limit':
                    self.assertFalse(any(k in ('check_variable', 'has_country_flag') for k, _, v in walk(body)))

    def test_explicit_uae_deficit_policy_keeps_the_entire_native_invoice(self):
        for kind, count, price in [('port', 1, '.02'), ('yard', 1, '.08'), ('yard', 2, '.16')]:
            with self.subTest(kind=kind, count=count):
                m = Model('coastal', treasury='-2');m.profile.update(country='UAE', allow_deficit=True);m.country['tag'] = 'UAE'
                for state in m.states.values():state['owner'] = state['controller'] = 'UAE'
                m.country['vars'].update({k.replace('_USA_', '_UAE_'): v for k, v in list(m.country['vars'].items()) if k.startswith('COLDWAR_NAVY_USA_')})
                self.assertTrue(m.ready(kind, count));m.run(kind, count)
                self.assertEqual(m.country['vars']['treasury'], Decimal('-2') - Decimal(price))
                self.assertEqual([t for t in m.trace if t[0] == 'fee'], [('fee', -Decimal(price))])
                package = m.package(kind, count)
                self.assertFalse(any(k == 'check_variable' and first(v, 'var') == 'treasury' for k, _, v in walk(parse(package['ready']))))

    def test_deficit_exception_is_opt_in_and_does_not_bypass_other_guards(self):
        for condition in ('no_opt_in', 'other_country', 'zero_gdp', 'skip', 'cap'):
            with self.subTest(condition=condition):
                m = Model('coastal', treasury='-2');m.profile.update(country='UAE', allow_deficit=True);m.country['tag'] = 'UAE'
                for state in m.states.values():state['owner'] = state['controller'] = 'UAE'
                m.country['vars'].update({k.replace('_USA_', '_UAE_'): v for k, v in list(m.country['vars'].items()) if k.startswith('COLDWAR_NAVY_USA_')})
                if condition == 'no_opt_in':m.profile.pop('allow_deficit')
                elif condition == 'other_country':
                    m.profile['country'] = 'USA';m.country['tag'] = 'USA'
                    for state in m.states.values():state['owner'] = state['controller'] = 'USA'
                elif condition == 'zero_gdp':m.country['vars']['gdp_total'] = Decimal(0)
                elif condition == 'skip':m.country['flags'].add('MD_skip_treasury_cost')
                else:
                    for state in m.states.values():state['ports'] = {p: 10 for p in state['ports']}
                before = copy.deepcopy((m.country, m.states));self.assertFalse(m.ready('port'));m.run('port')
                self.assertEqual(before, (m.country, m.states));self.assertFalse(m.trace)


if __name__ == '__main__':
    unittest.main(verbosity=2)
