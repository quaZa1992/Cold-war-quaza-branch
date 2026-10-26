# IMPERIA CW — Cold War: Execute emitted lottery branches and verify the retained monthly contract.
from pathlib import Path
from collections import deque
from copy import deepcopy
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('clausewitz_ast', ROOT / 'tools/spain_1970_v2/script_ast.py')
AST = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AST)


def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')


EFFECTS = dict((k, v) for k, _, v in AST.parse(read('common/scripted_effects/COLDWAR_resource_discoveries.txt')))
TRIGGERS = dict((k, v) for k, _, v in AST.parse(read('common/scripted_triggers/COLDWAR_resource_discoveries.txt')))
DATA = json.loads((HERE / 'balance.json').read_text())
ROLL = 'COLDWAR_resource_discovery_roll'
CLAIM = 'COLDWAR_resource_discovery_claim'
PENDING = 'COLDWAR_resource_discovery_pending'


class State:
    """Only the emitted helper subset is supported; unknown commands fail the test."""
    def __init__(self, region=147, counter=41):
        self.region = region
        self.variables = {}
        self.resources = {}
        self.flags = set()
        self.global_values = {'global.resource_spawner_counter': counter}
        self.draws = deque()

    def number(self, value):
        if value in self.global_values:
            return self.global_values[value]
        if value in self.variables:
            return self.variables[value]
        return float(value)

    def condition(self, rows):
        results = []
        for key, op, value in rows:
            if key == 'NOT':
                result = not self.condition(value)
            elif key == 'OR':
                result = any(self.condition([row]) for row in value)
            elif key == 'hidden_trigger':
                result = self.condition(value)
            elif key == 'check_variable':
                name, relation, rhs = value[0]
                left = self.variables.get(name, self.global_values.get(name, 0))
                right = self.number(rhs)
                result = {'=': left == right, '>': left > right}[relation]
            elif key == 'has_variable':
                result = value in self.variables
            elif key == 'has_state_flag':
                result = value in self.flags
            elif key == 'region':
                result = self.region == int(value)
            elif key == 'has_resources_amount':
                name = AST.first(value, 'resource')
                _, relation, quantity = next(row for row in value if row[0] == 'amount')
                assert relation == '>'
                result = self.resources.get(name, 0) > float(quantity)
            elif key in TRIGGERS:
                result = self.condition(TRIGGERS[key])
            else:
                raise AssertionError('Unsupported trigger ' + key)
            results.append(result)
        return all(results)

    def run(self, rows):
        taken = False
        for key, op, value in rows:
            if key in ['limit', 'modifier']:
                continue
            if key in ['if', 'else_if']:
                if key == 'if':
                    taken = False
                if not taken and self.condition(AST.first(value, 'limit', [])):
                    taken = True
                    self.run(value)
            elif key == 'hidden_effect':
                self.run(value)
            elif key in ['set_variable', 'multiply_variable']:
                name, _, rhs = value[0]
                table = self.global_values if name.startswith('global.') else self.variables
                amount = self.number(rhs)
                table[name] = amount if key == 'set_variable' else table.get(name, 0) * amount
            elif key == 'random_list':
                choices = []
                for weight, _, body in value:
                    total = float(weight)
                    for modifier in AST.values(body, 'modifier'):
                        conditions = [row for row in modifier if row[0] != 'factor']
                        if self.condition(conditions):
                            total *= float(AST.first(modifier, 'factor'))
                    if total:
                        choices.append((total, body))
                draw = self.draws.popleft()
                assert 0 <= draw < sum(weight for weight, _ in choices)
                for weight, body in choices:
                    if draw < weight:
                        self.run(body)
                        break
                    draw -= weight
            elif key == 'set_state_flag':
                self.flags.add(value)
            elif key == 'clr_state_flag':
                self.flags.discard(value)
            elif key == 'add_resource':
                name = AST.first(value, 'type')
                self.resources[name] = self.resources.get(name, 0) + self.number(AST.first(value, 'amount'))
            elif key in EFFECTS:
                self.run(EFFECTS[key])
            else:
                raise AssertionError('Unsupported effect ' + key)

    def roll(self, resource_draw, size_draw):
        self.draws.extend([resource_draw, size_draw])
        self.run(EFFECTS[ROLL])

    def claim(self):
        self.run(EFFECTS[CLAIM])


def strip_snapshot_guards(rows):
    result = []
    for key, op, value in rows:
        if key == ROLL:
            continue
        if key == 'NOT' and value == [('has_state_flag', '=', PENDING)]:
            continue
        result.append((key, op, strip_snapshot_guards(value) if isinstance(value, list) else value))
    return result


# IMPERIA COLD WAR: Check the explicit mandate exception against the unchanged original lottery.
def owner_conditions(rows):
    result = []
    for key, _, value in rows:
        if key == 'OWNER':
            result.append(value)
        elif isinstance(value, list):
            result.extend(owner_conditions(value))
    return result


def country_eligible(rows, *, developed=False, mandate=False, gdp=500, ai=False, war=False):
    for key, _, value in rows:
        if key == 'NOT':
            passed = not country_eligible(value, developed=developed, mandate=mandate, gdp=gdp, ai=ai, war=war)
        elif key == 'is_ai':
            passed = ai == (value == 'yes')
        elif key == 'has_war':
            passed = war == (value == 'yes')
        elif key == 'has_idea':
            assert value == 'imp_ni_resource_extraction_mandate'
            passed = mandate
        elif key == 'has_dynamic_modifier':
            assert AST.first(value, 'modifier') == 'imp_eco_1_dynamic_modifier'
            passed = developed
        elif key == 'check_variable':
            assert value[0][:2] == ('gdp_total', '<')
            passed = gdp < float(value[0][2])
        else:
            raise AssertionError('Unsupported country eligibility condition ' + key)
        if not passed:
            return False
    return True


class DiscoveryChecks(unittest.TestCase):
    def test_all_eighteen_outcomes_match_the_approved_table(self):
        # Fixed fixture rather than deriving the expected amounts from generator data.
        approved = [('oil', [16, 32, 48]), ('steel', [12, 24, 36]),
                    ('aluminium', [8, 16, 24]), ('tungsten', [8, 16, 24]),
                    ('chromium', [4, 8, 12]), ('rubber', [8, 16, 24])]
        for index, (name, amounts) in enumerate(approved):
            for draw, expected in zip([0, 65, 95], amounts):
                with self.subTest(resource=name, size_draw=draw):
                    state = State()
                    state.roll(index * 100, draw)
                    self.assertFalse(state.resources)
                    state.claim()
                    self.assertEqual(state.resources, {name: expected})

    def test_size_weights_are_exactly_65_30_5(self):
        outcomes = []
        for draw in range(100):
            state = State()
            state.roll(0, draw)
            outcomes.append(state.variables['COLDWAR_discovery_amount'])
        self.assertEqual({n: outcomes.count(n) for n in set(outcomes)}, {16: 65, 32: 30, 48: 5})

    def test_delayed_counter_never_inflates_the_frozen_reward(self):
        for counter in [41, 100, 99999]:
            state = State(counter=counter)
            state.roll(300, 95)
            state.global_values['global.resource_spawner_counter'] += 6000
            state.claim()
            self.assertEqual(state.resources, {'tungsten': 24})
            self.assertEqual(state.global_values['global.resource_spawner_counter'], 0)

    def test_reward_cannot_be_claimed_twice(self):
        state = State()
        state.roll(400, 65)
        state.claim()
        receipt = deepcopy(state.variables)
        for _ in range(20):
            state.claim()
        self.assertEqual(state.resources, {'chromium': 8})
        self.assertEqual(state.variables, receipt)
        self.assertNotIn(PENDING, state.flags)

    def test_separate_pending_results_survive_other_countries_claims(self):
        first, second = State(), State()
        second.global_values = first.global_values
        first.roll(0, 0)
        second.roll(100, 95)
        first.claim()
        second.claim()
        self.assertEqual(first.resources, {'oil': 16})
        self.assertEqual(second.resources, {'steel': 36})

    def test_existing_save_event_gets_a_bounded_result(self):
        state = State(counter=1000)
        state.draws.extend([0, 95])
        state.claim()
        state.claim()
        self.assertEqual(state.resources, {'oil': 48})

    def test_rubber_region_and_existing_production_gate(self):
        arctic, tropical = State(region=120), State(region=147)
        self.assertFalse(arctic.condition(TRIGGERS['COLDWAR_resource_rubber_region']))
        self.assertTrue(tropical.condition(TRIGGERS['COLDWAR_resource_rubber_region']))
        arctic.resources['rubber'] = 1
        self.assertTrue(arctic.condition(TRIGGERS['COLDWAR_resource_rubber_region']))
        tropical.roll(500, 0)
        self.assertEqual(tropical.variables['COLDWAR_discovery_type'], 6)

    def test_all_ineligible_resource_draws_exclude_rubber(self):
        for draw in range(500):
            state = State(region=120)
            state.roll(draw, 0)
            self.assertNotEqual(state.variables['COLDWAR_discovery_type'], 6)

    def test_monthly_eligibility_frequency_and_other_hooks_are_preserved(self):
        path = 'common/on_actions/zzzzzz_imp_minis_on_actions.txt'
        base = json.loads((HERE / 'baseline.json').read_text())['monthly_lottery']
        # The only intentional eligibility change: the mandate route includes developed economies.
        owners = owner_conditions(base)
        self.assertEqual(len(owners), 2)
        exclusion = ['NOT', '=', [['has_dynamic_modifier', '=', [['modifier', '=', 'imp_eco_1_dynamic_modifier']]]]]
        self.assertIn(['has_idea', '=', 'imp_ni_resource_extraction_mandate'], owners[1])
        self.assertIn(exclusion, owners[1])
        owners[1].remove(exclusion)
        current = AST.values(AST.first(AST.parse(read(path)), 'on_actions'), 'on_monthly_LUX')[0]
        self.assertEqual(json.loads(json.dumps(strip_snapshot_guards(current))), base)
        source = read(path)
        self.assertEqual(source.count('COLDWAR_resource_discovery_roll = yes'), 2)
        self.assertEqual(source.count('has_state_flag = ' + PENDING), 2)

    def test_developed_countries_need_the_mandate_and_keep_other_eligibility_guards(self):
        hooks = AST.first(AST.parse(read('common/on_actions/zzzzzz_imp_minis_on_actions.txt')), 'on_actions')
        normal, mandate = owner_conditions(AST.values(hooks, 'on_monthly_LUX')[0])
        self.assertTrue(country_eligible(normal))
        self.assertFalse(country_eligible(normal, developed=True))
        self.assertFalse(country_eligible(normal, gdp=1000))
        self.assertFalse(country_eligible(mandate, developed=True))
        for developed in [False, True]:
            for gdp in [500, 100000]:
                self.assertTrue(country_eligible(mandate, developed=developed, mandate=True, gdp=gdp))
                self.assertFalse(country_eligible(mandate, developed=developed, mandate=True, gdp=gdp, ai=True))
                self.assertFalse(country_eligible(mandate, developed=developed, mandate=True, gdp=gdp, war=True))

    def test_mandate_selection_includes_developed_countries_and_retains_costs_and_commitment(self):
        ideas = AST.first(AST.parse(read('common/ideas/mdcw_imperia_national_ideas_2.txt')), 'ideas')
        spirit = next(AST.first(category, 'imp_ni_resource_extraction_mandate')
                      for _, _, category in ideas
                      if isinstance(category, list) and AST.first(category, 'imp_ni_resource_extraction_mandate') is not None)
        self.assertEqual(AST.first(spirit, 'available'), [])
        self.assertEqual(AST.first(spirit, 'cost'), '150')
        self.assertEqual(AST.first(spirit, 'removal_cost'), '150')
        flag = AST.first(AST.first(spirit, 'on_add'), 'set_country_flag')
        self.assertEqual(AST.first(flag, 'days'), '1440')

    def test_observer_receives_news_only_and_owner_uses_the_state_receipt(self):
        event = next(v for k, _, v in AST.parse(read('events/imp_minis_events.txt'))
                     if k == 'news_event' and AST.first(v, 'id') == 'imp_minis.2')
        options = AST.values(event, 'option')
        self.assertEqual([k for k, _, _ in options[0]], ['name', 'trigger'])
        self.assertEqual(AST.first(options[1], 'event_target:target_state'), [(CLAIM, '=', 'yes')])
        self.assertEqual(AST.first(event, 'major'), 'yes')
        self.assertEqual(AST.first(event, 'is_triggered_only'), 'yes')

    def test_resource_reports_distinguish_all_six_outcomes_and_rubber(self):
        source = read('events/imp_minis_events.txt')
        event = next(v for k, _, v in AST.parse(source)
                     if k == 'news_event' and AST.first(v, 'id') == 'imp_minis.2')
        titles = AST.values(event, 'title')
        self.assertEqual(len(titles), 7)  # Six resources and the old-save fallback.
        for resource_id in range(1, 7):
            title = titles[resource_id - 1]
            self.assertEqual(AST.first(title, 'text'), 'COLDWAR_resource_discovery_' + str(resource_id) + '_title')
            state = State()
            state.variables['COLDWAR_discovery_type'] = resource_id
            conditions = AST.first(AST.first(title, 'trigger'), 'event_target:target_state')
            self.assertTrue(state.condition(conditions))
        self.assertEqual(len(AST.values(event, 'desc')), 2)

    def test_native_resource_names_regions_and_encodings_resolve(self):
        resources = read('common/resources/00_resources.txt')
        region_ids = {int(p.name.split('-')[0]) for p in (ROOT / 'map/strategicregions').glob('*.txt')}
        for row in DATA['resources']:
            self.assertIn(row['resource'] + ' = {', resources)
        self.assertTrue(set(map(int, DATA['rubber_regions'])) <= region_ids)
        for path in ['common/scripted_effects/COLDWAR_resource_discoveries.txt',
                     'common/scripted_triggers/COLDWAR_resource_discoveries.txt']:
            self.assertFalse((ROOT / path).read_bytes().startswith(b'\xef\xbb\xbf'))
            AST.parse(read(path))
        loc = ROOT / 'localisation/english/COLDWAR_resource_discoveries_l_english.yml'
        self.assertTrue(loc.read_bytes().startswith(b'\xef\xbb\xbf'))
        for row in DATA['resources']:
            self.assertIn('COLDWAR_resource_discovery_' + str(row['id']) + '_title:', loc.read_text(encoding='utf-8-sig'))

    def test_no_uranium_or_manufactured_goods_and_no_new_loops(self):
        resources = {r['resource'] for r in DATA['resources']}
        self.assertFalse(resources & {'uranium', 'microchips', 'composites'})
        source = read('common/scripted_effects/COLDWAR_resource_discoveries.txt')
        self.assertNotIn('amount = global.resource_spawner_counter', source)
        for command in ['every_country', 'every_state', 'on_daily', 'on_weekly', 'on_monthly']:
            self.assertNotIn(command + ' =', source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
