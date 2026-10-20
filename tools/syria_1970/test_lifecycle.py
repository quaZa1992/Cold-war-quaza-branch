"""Regression scenarios against emitted scripts, not an HOI4 engine substitute.

Exercises earned programme ownership, independent reform stages, one-time
implementation and changed funding/control. Native money/building calls are
modelled only at their documented interface; actual economic simulation is not.
"""
from copy import deepcopy
from itertools import permutations
from pathlib import Path
import json
import unittest
from validate_content import parse, first, vals

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'COLDWAR_SYR_'


class Country:
    def __init__(self, bodies):
        self.bodies = bodies
        self.flags = {PREFIX+'initialized', PREFIX+'leader_atassi'}
        self.variables = {'ruling_party': 7, 'treasury': 100, 'debt': 0}
        self.temp = {}
        self.dynamic = set()
        self.ideas = set()
        self.control = {186, 188, 189, 193, 566, 994}
        self.buildings = []
        self.date = (1970, 1, 1)
        self.leader = None

    def number(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return self.temp.get(value, self.variables.get(value, 0))

    def condition(self, body):
        outcomes = []
        for key, op, value in body:
            if key in ('AND', 'hidden_trigger'):
                outcomes.append(self.condition(value))
            elif key == 'custom_trigger_tooltip':
                outcomes.append(self.condition([clause for clause in value if clause[0] != 'tooltip']))
            elif key == 'OR':
                outcomes.append(any(self.condition([clause]) for clause in value))
            elif key == 'NOT':
                outcomes.append(not self.condition(value))
            elif key == 'original_tag':
                outcomes.append(value == 'SYR')
            elif key == 'IMP_is_1970_scenario':
                outcomes.append(value == 'yes')
            elif key == 'has_country_flag':
                outcomes.append(value in self.flags)
            elif key == 'has_variable':
                outcomes.append(value in self.variables)
            elif key == 'has_dynamic_modifier':
                outcomes.append(value in self.dynamic)
            elif key == 'has_idea':
                outcomes.append(value in self.ideas)
            elif key == 'has_country_leader':
                outcomes.append(self.leader == first(value, 'name', '').strip('"'))
            elif key == 'check_variable':
                var, comparison, target = value[0]
                a, b = self.variables.get(var, 0), self.number(target)
                outcomes.append({'=': abs(a-b) < 1e-8, '>': a > b, '<': a < b}[comparison])
            elif key == 'controls_state':
                outcomes.append(int(value) in self.control)
            elif key.isdigit():
                # Test fixtures provide capacity in these controlled states.
                outcomes.append(int(key) in self.control)
            elif key == 'always':
                outcomes.append(value == 'yes')
            elif key == 'date':
                other = tuple(int(part) for part in value.split('.'))
                outcomes.append(self.date < other if op == '<' else self.date > other if op == '>' else self.date == other)
            elif key == 'has_global_flag':
                outcomes.append(False)
            else:
                raise AssertionError('Unmodelled test condition: '+str((key, op, value)))
        return all(outcomes)

    def execute(self, body):
        branch = None
        for key, op, value in body:
            if key == 'if':
                branch = self.condition(first(value, 'limit', []))
                if branch:
                    self.execute([x for x in value if x[0] != 'limit'])
            elif key == 'else_if':
                if not branch:
                    branch = self.condition(first(value, 'limit', []))
                    if branch:
                        self.execute([x for x in value if x[0] != 'limit'])
            elif key == 'else':
                if not branch:
                    self.execute(value)
            elif key in ('set_variable', 'add_to_variable', 'subtract_from_variable', 'set_temp_variable'):
                variable, _, number = value[0]
                target = self.temp if key == 'set_temp_variable' else self.variables
                amount = self.number(number)
                target[variable] = amount if key.startswith('set_') else target.get(variable, 0)+amount*(-1 if key == 'subtract_from_variable' else 1)
            elif key == 'set_country_flag':
                self.flags.add(first(value, 'flag') if isinstance(value, list) else value)
            elif key == 'clr_country_flag':
                self.flags.discard(value)
            elif key == 'add_dynamic_modifier':
                self.dynamic.add(first(value, 'modifier'))
            elif key == 'remove_dynamic_modifier':
                self.dynamic.discard(first(value, 'modifier'))
            elif key == 'effect_tooltip':
                continue
            elif key == 'modify_treasury_effect':
                self.variables['treasury'] += self.temp['treasury_change']
            elif key == 'create_country_leader':
                self.leader = first(value, 'name').strip('"')
            elif key in self.bodies and value == 'yes':
                self.execute(self.bodies[key])
            elif key.isdigit():
                for child in vals(value, 'add_building_construction'):
                    self.buildings.append((int(key), first(child, 'type')))
            elif key in ('hidden_effect',):
                self.execute(value)
            elif key in ('log', 'custom_effect_tooltip', 'unlock_decision_tooltip',
                         'force_update_dynamic_modifier', 'update_money_dirty_variable',
                         'update_state_variables', 'calculate_energy_use',
                         'kill_country_leader', 'retire_country_leader', 'update_set_politics'):
                continue
            else:
                raise AssertionError('Unmodelled test effect: '+str((key, op, value)))


class LifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bodies = {}
        for path in (ROOT/'common/scripted_effects').glob('COLDWAR_SYR*.txt'):
            cls.bodies.update({k: v for k, _, v in parse(path.read_text(encoding='utf-8-sig')) if isinstance(v, list)})
        tree = parse((ROOT/'common/national_focus/COLDWAR_SYR_1970_focus.txt').read_text(encoding='utf-8'))
        cls.focus = {first(f, 'id'): f for f in vals(first(tree, 'focus_tree'), 'focus')}
        politics_decisions = parse((ROOT/'common/decisions/COLDWAR_SYR_politics_decisions.txt').read_text(encoding='utf-8'))
        cls.decisions = {k: body for _, _, category in politics_decisions for k, _, body in category}

    def country(self):
        c = Country(self.bodies)
        c.execute(self.bodies[PREFIX+'initialize_programme_variables'])
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        return c

    def test_seven_initial_problems(self):
        c = self.country()
        expected = set(s['id'] for s in json.loads((ROOT/'tools/syria_1970/manifest.json').read_text(encoding='utf-8'))['starting_spirits'])
        self.assertEqual(c.dynamic, expected)
        self.assertAlmostEqual(c.variables[PREFIX+'state_sector_strain_bureaucracy_cost_multiplier_modifier'], .08)

    def test_agreement_needs_implementation_and_civilian_transition_has_exit(self):
        c = self.country()
        c.flags.add(PREFIX+'dual_command_resolved')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertIn(PREFIX+'divided_command', c.dynamic)
        c.execute(self.bodies[PREFIX+'opening_settlement_implement'])
        self.assertNotIn(PREFIX+'divided_command', c.dynamic)
        c = self.country()
        c.variables['ruling_party'] = 1
        c.flags.add(PREFIX+'parliament_05_implemented')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertNotIn(PREFIX+'divided_command', c.dynamic)

    def test_party_leaves_and_returns_without_replaying_rewards(self):
        c = self.country()
        for focus in ('baath_01', 'atassi_01', 'industry_01'):
            c.execute(self.bodies[PREFIX+focus+'_implement'])
        saved = deepcopy(c.variables)
        self.assertIn(PREFIX+'baath_programme', c.dynamic)
        self.assertIn(PREFIX+'atassi_programme', c.dynamic)
        c.variables['ruling_party'] = 1
        c.flags.discard(PREFIX+'leader_atassi')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertNotIn(PREFIX+'baath_programme', c.dynamic)
        self.assertNotIn(PREFIX+'atassi_programme', c.dynamic)
        self.assertIn(PREFIX+'industry_programme', c.dynamic)
        c.variables['ruling_party'] = 7
        c.flags.add(PREFIX+'leader_atassi')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertIn(PREFIX+'baath_programme', c.dynamic)
        self.assertIn(PREFIX+'atassi_programme', c.dynamic)
        self.assertEqual(c.variables, saved)

    def test_late_collective_stewardship_never_reinstalls_khatib(self):
        c = self.country()
        c.variables[PREFIX+'baath_head'] = 1
        c.execute(self.bodies[PREFIX+'1970_set_leader'])
        self.assertEqual(c.leader, 'Ahmad al-Khatib')
        c.date = (1983, 1, 1)
        c.execute(self.bodies[PREFIX+'1970_set_leader'])
        self.assertEqual(c.leader, 'Civilian Stewardship Council')
        self.assertEqual(c.variables[PREFIX+'baath_head'], 4)

    def test_independent_audits_commute(self):
        for order in permutations(('industry_12', 'fiscal_12')):
            c = self.country()
            for index, focus in enumerate(order):
                c.flags.add(PREFIX+focus+'_implemented')
                c.execute(self.bodies[PREFIX+'refresh_programmes'])
                self.assertAlmostEqual(c.variables[PREFIX+'state_sector_strain_bureaucracy_cost_multiplier_modifier'], .04 if index == 0 else 0)
            c.execute(self.bodies[PREFIX+'refresh_programmes'])
            self.assertAlmostEqual(c.variables[PREFIX+'state_sector_strain_bureaucracy_cost_multiplier_modifier'], 0)

    def test_education_and_construction_are_separate(self):
        c = self.country()
        c.flags.add(PREFIX+'fiscal_09_implemented')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertEqual(c.variables[PREFIX+'uneven_services_research_speed_factor'], 0)
        self.assertEqual(c.variables[PREFIX+'uneven_services_production_speed_buildings_factor'], -.05)
        c.flags.add(PREFIX+'infrastructure_12_implemented')
        c.execute(self.bodies[PREFIX+'refresh_programmes'])
        self.assertNotIn(PREFIX+'uneven_services', c.dynamic)

    def test_project_borrows_rechecks_control_and_grants_once(self):
        c = self.country()
        focus = PREFIX+'industry_09'
        c.variables['treasury'] = 0
        c.control.discard(566)
        c.execute(first(self.focus[focus], 'completion_reward'))
        self.assertIn(focus+'_pending', c.flags)
        self.assertNotIn(focus+'_implemented', c.flags)
        self.assertEqual(c.buildings, [])
        c.variables['treasury'] = -1
        c.execute(self.bodies[focus+'_implement'])
        self.assertEqual(c.variables['treasury'], -1)
        c.control.add(566)
        c.execute(self.bodies[focus+'_implement'])
        self.assertEqual(c.variables['treasury'], -8)
        self.assertEqual(c.buildings, [(566, 'industrial_complex')])
        self.assertNotIn(focus+'_pending', c.flags)
        c.variables['treasury'] = -12
        c.execute(self.bodies[focus+'_implement'])
        self.assertEqual(c.variables['treasury'], -12)
        self.assertEqual(len(c.buildings), 1)

    def test_officer_negotiations_can_overdraw_the_treasury(self):
        decision = self.decisions[PREFIX+'decision_officer_bargain']
        for balance in (0, -.1):
            with self.subTest(balance=balance):
                c = self.country()
                c.flags.add(PREFIX+'opening_entry_implemented')
                c.variables['treasury'] = balance
                self.assertTrue(c.condition(first(decision, 'available')))
                c.execute(first(decision, 'complete_effect'))
                self.assertAlmostEqual(c.variables['treasury'], balance - 2)
                # The native budget tick handles the deficit; no duplicate debt charge.
                self.assertEqual(c.variables['debt'], 0)

    def test_existing_completed_entry_receives_new_bonus_once(self):
        c = self.country()
        focus = PREFIX+'army_entry'
        c.flags.add(focus+'_implemented')
        c.execute(self.bodies[PREFIX+'migrate_entry_rewards_20261019'])
        self.assertEqual(c.variables[PREFIX+'army_programme_army_org_factor'], .02)
        self.assertEqual(c.variables[PREFIX+'army_programme_supply_consumption_factor'], .01)
        self.assertIn(PREFIX+'army_programme_earned', c.flags)
        saved = c.variables.copy()
        c.execute(self.bodies[PREFIX+'migrate_entry_rewards_20261019'])
        self.assertEqual(c.variables, saved)


if __name__ == '__main__':
    unittest.main(verbosity=2)
