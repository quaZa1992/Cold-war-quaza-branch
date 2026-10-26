# IMPERIA CW — Cold War: Arab coalition startup regression checks.
"""Check actual startup scripts, without pretending to simulate capitulation.

The small strict runner executes only the regional setup and its real once guard.
Native war merging, faction capitulation and peace conferences require HOI4.
"""
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    'arab_startup_ast', ROOT / 'tools/vietnam_1970/script_ast.py')
AST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AST)
EFFECT_PATH = ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt'
EFFECTS = dict((key, value) for key, _, value in
               AST.parse(EFFECT_PATH.read_text(encoding='utf-8')))
INTERNAL = EFFECTS['IMP_1970_setup_global_alignment_internal']
WRAPPER = EFFECTS['IMP_1970_setup_global_alignment']
MEMBERS = {'EGY', 'SYR', 'JOR', 'IRQ', 'PAL'}
FACTION = 'faction_template_1970_arab_joint_defense_command'


def contains(rows, key, expected=None):
    return any(k == key and (expected is None or v == expected)
               for k, _, v in AST.walk(rows))


# Select the authored coalition transaction, not earlier identity setup blocks.
EGYPT_INDEX = next(index for index, (key, _, body) in enumerate(INTERNAL)
                   if key == 'EGY' and isinstance(body, list)
                   and AST.first(body, 'create_faction_from_template') == FACTION)
REGIONAL = INTERNAL[EGYPT_INDEX:EGYPT_INDEX + 5]


class RegionalRunner:
    """Execute the supported startup statements; fail on unknown semantics."""

    def __init__(self, israel_exists=True):
        self.existing = MEMBERS | ({'ISR'} if israel_exists else set())
        self.flags = set()
        self.faction = set()
        self.war_sides = {}
        self.events = []

    def condition(self, rows, country):
        for key, op, value in rows:
            if op != '=':
                raise AssertionError(('Unsupported condition operator', key, op))
            if key == 'NOT':
                valid = not self.condition(value, country)
            elif key in self.existing or key == 'ISR':
                valid = self.condition(value, key)
            elif key == 'exists':
                valid = (country in self.existing) == (value == 'yes')
            elif key == 'has_global_flag':
                valid = value in self.flags
            elif key == 'has_war_with':
                valid = ((country, value) in self.war_sides)
            else:
                raise AssertionError(('Unsupported startup condition', key))
            if not valid:
                return False
        return True

    def execute(self, rows, country='USA'):
        for key, op, value in rows:
            if op != '=':
                raise AssertionError(('Unsupported effect operator', key, op))
            if key in MEMBERS:
                self.execute(value, key)
            elif key == 'if':
                if self.condition(AST.first(value, 'limit'), country):
                    self.execute([row for row in value if row[0] != 'limit'], country)
            elif key == 'set_global_flag':
                self.flags.add(value)
            elif key == 'IMP_1970_setup_global_alignment_internal':
                self.execute(REGIONAL, country)
            elif key == 'create_faction_from_template':
                if value != FACTION:
                    raise AssertionError(('Unexpected faction', value))
                self.faction = {country}
            elif key == 'add_to_faction':
                self.faction.add(value)
            elif key == 'declare_war_on':
                enemy = AST.first(value, 'target')
                self.events.append(('declaration', country, enemy,
                                    frozenset(self.faction)))
                self.war_sides[country, enemy] = (country, enemy)
            elif key == 'add_to_war':
                ally = AST.first(value, 'targeted_alliance')
                enemy = AST.first(value, 'enemy')
                self.war_sides[country, enemy] = self.war_sides[ally, enemy]
                self.events.append(('join', country, ally, enemy))
            else:
                raise AssertionError(('Unsupported startup effect', key))


class ArabCoalitionStartupTests(unittest.TestCase):
    def test_all_five_members_are_in_faction_before_the_declaration(self):
        runner = RegionalRunner()
        runner.execute(WRAPPER)
        declarations = [event for event in runner.events if event[0] == 'declaration']
        self.assertEqual(declarations,
                         [('declaration', 'EGY', 'ISR', frozenset(MEMBERS))])
        self.assertEqual(runner.faction, MEMBERS)

    def test_all_four_partners_join_egypts_existing_war(self):
        self.assertEqual([key for key, _, _ in REGIONAL],
                         ['EGY', 'SYR', 'JOR', 'IRQ', 'PAL'])
        runner = RegionalRunner()
        runner.execute(WRAPPER)
        self.assertEqual([event for event in runner.events if event[0] == 'join'],
                         [('join', tag, 'EGY', 'ISR')
                          for tag in ('SYR', 'JOR', 'IRQ', 'PAL')])
        self.assertEqual(set(runner.war_sides), {(tag, 'ISR') for tag in MEMBERS})
        self.assertEqual(set(runner.war_sides.values()), {('EGY', 'ISR')})

    def test_missing_israel_does_not_create_wars(self):
        runner = RegionalRunner(israel_exists=False)
        runner.execute(WRAPPER)
        self.assertEqual(runner.events, [])
        self.assertEqual(runner.war_sides, {})

    def test_repeat_initialization_is_inert_even_after_later_peace(self):
        runner = RegionalRunner()
        runner.execute(WRAPPER)
        snapshot = deepcopy((runner.flags, runner.faction,
                             runner.war_sides, runner.events))
        runner.execute(WRAPPER)
        self.assertEqual((runner.flags, runner.faction,
                          runner.war_sides, runner.events), snapshot)
        runner.war_sides.clear()  # A later legitimate peace must stay in force.
        events_before = list(runner.events)
        runner.execute(WRAPPER)
        self.assertEqual(runner.war_sides, {})
        self.assertEqual(runner.events, events_before)

    def test_palestinian_ownership_and_israeli_occupation_are_retained(self):
        for state, filename in ((208, '208-West Bank.txt'), (209, '209-Gaza.txt')):
            with self.subTest(state=state):
                tree = AST.parse((ROOT / 'history/states' / filename).read_text(
                    encoding='utf-8'))
                history = AST.first(AST.first(tree, 'state'), 'history')
                start = AST.first(history, '1970.1.1')
                self.assertEqual(AST.first(start, 'owner'), 'PAL')
                self.assertEqual(AST.first(start, 'controller'), 'ISR')
        for operation in ('transfer_state', 'set_state_owner', 'set_state_controller',
                          'annex_country', 'white_peace'):
            self.assertFalse(contains(REGIONAL, operation), operation)

    def test_native_goal_and_guarded_startup_hook_are_preserved(self):
        self.assertTrue(contains(REGIONAL, 'type', 'IMP_1970_war_of_attrition'))
        path = ROOT / 'common/on_actions/99_IMP_1970_world_on_actions.txt'
        actions = AST.first(AST.parse(path.read_text(encoding='utf-8')), 'on_actions')
        start = AST.first(AST.first(actions, 'on_startup'), 'effect')
        branch = AST.first(start, 'if')
        self.assertTrue(contains(AST.first(branch, 'limit'),
                                 'IMP_is_1970_scenario', 'yes'))
        self.assertTrue(contains(branch, 'IMP_1970_setup_global_alignment', 'yes'))

    def test_changed_runtime_script_is_utf8_without_bom(self):
        raw = EFFECT_PATH.read_bytes()
        self.assertFalse(raw.startswith(b'\xef\xbb\xbf'))
        raw.decode('utf-8')
        self.assertIn('IMPERIA CW', raw.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
