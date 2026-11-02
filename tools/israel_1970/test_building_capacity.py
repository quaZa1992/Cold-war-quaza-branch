# IMPERIA COLD WAR — Israel instant-grant physical-capacity regressions.
"""Exercise actual emitted focus and delayed-project AST, without generation.

Manual construction entitlement is explicitly zero. Staffing/province predicates
and the MD treasury adapter retain the existing bounded fixture's scope. This
does not emulate native construction, event scheduling, saves or multiplayer.
"""
from pathlib import Path
import ast
import copy
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'tools'))
import validate_rework as base
from building_grants.grants import rewrite_queries

FOCUSES = (
    'ISR70_p0_eb_deepen', 'ISR70_p3_ca_deepen', 'ISR70_p6_eb_deepen',
    'ISR70_p12_eb_deepen', 'ISR70_p13_cb_deepen', 'ISR70_p16_cb_deepen',
    'ISR70_p17_cb_deepen', 'ISR70_p18_eb_deepen', 'ISR70_p23_ea_deepen',
    'ISR70_golda_housing', 'ISR70_negev_roads', 'ISR70_development_towns',
)

def parsed(rel):
    return base.read((ROOT / rel).read_text(encoding='utf-8-sig'))

REGULAR = {k: v for k, _, v in parsed('common/scripted_effects/ISR70_effects.txt') if isinstance(v, list)}
base.EFFECTS.update(REGULAR)
base.TRIGGERS.update({k: v for k, _, v in parsed('common/scripted_triggers/ISR70_triggers.txt') if isinstance(v, list)})
PARTIES = {k: v for k, _, v in parsed('common/scripted_triggers/01_political_triggers.txt') if k.endswith('_are_in_power')}
base.TRIGGERS.update(PARTIES)
PROJECTS = {
    p['key']: p for p in base.DATA['policy_expansion']['projects']
    if any(b['type'] == 'infrastructure' for b in p['buildings'])
}


class PhysicalFixture(base.Fixture):
    def __init__(self):
        super().__init__()
        self.states = {
            s: dict(owner='ISR' if s in (204, 205, 206) else 'PAL' if s in (208, 209) else 'SYR' if s == 587 else 'EGY',
                    controller='ISR', full_control=True, capacity=True, slots=0,
                    buildings={}, dynamic=set(), resistance={}, manual_max=0)
            for s in (204, 205, 206, 208, 209, 213, 214, 587)
        }
        self.vars['ruling_party'] = 3
        self.credit = {s: 0 for s in self.states}
        self.grants = []
        self.native_receipts = []

    def condition(self, block, state=None, any_of=False):
        answers = []
        for k, op, v in block:
            if k in ('original_tag', 'tag'):
                answers.append(v == 'ISR')
                continue
            if k == 'IMP_is_1970_scenario':
                answers.append(self.scenario == (v == 'yes'))
                continue
            if k in ('is_owned_by', 'is_controlled_by') and v == 'ROOT':
                v = 'ISR'
            if k == 'free_building_slots' and base.scalar(v, 'building') == 'infrastructure':
                current = self.states[state]['buildings'].get('infrastructure', 0)
                needed = int(base.scalar(v, 'size'))
                answers.append(self.states[state]['manual_max'] - current > needed)
            else:
                answers.append(super().condition([(k, op, v)], state))
        return any(answers) if any_of else all(answers)

    def native_adapter(self, k, v, state):
        # Execute the real nested control flow in the existing strict fixture.
        # These three native systems are outside this asset/money regression.
        if k in ('ISR70_refresh_programmes', 'add_tech_bonus', 'add_stability'):
            self.native_receipts.append((k, copy.deepcopy(v)))
            return True
        if k == 'clamp_variable':
            key = base.scalar(v, 'var')
            minimum = base.scalar(v, 'min')
            maximum = base.scalar(v, 'max')
            if minimum is not None:
                self.vars[key] = max(self.vars[key], self.value(minimum))
            if maximum is not None:
                self.vars[key] = min(self.vars[key], self.value(maximum))
            return True
        if k == 'add_extra_state_shared_building_slots':
            self.credit[state] += int(v)
        if k == 'add_building_construction':
            count = int(base.scalar(v, 'level'))
            self.credit[state] -= count
            assert self.credit[state] >= 0, ('Construction preceded its slots', state, v)
            assert base.scalar(v, 'instant_build') == 'yes', v
            self.grants.append((state, base.scalar(v, 'type'), count))
        return False

    def complete_focus(self, identifier):
        if identifier in self.focuses:
            return
        focus = base.FOCUSES[identifier]
        if self.condition(base.child(focus, 'available', [])):
            self.focuses.add(identifier)
            self.execute(base.child(focus, 'completion_reward'))


def seed_positive(game, block):
    """Fixture only the actual positive prerequisites, never their NOT clauses."""
    for k, _, v in block:
        if k == 'NOT':
            continue
        if k == 'has_country_flag':
            game.flags.add(v)
        elif k == 'has_idea':
            game.ideas.add(v)
        elif k == 'has_completed_focus':
            game.focuses.add(v)
        elif isinstance(v, list):
            seed_positive(game, v)


def project_fixture(key):
    game = PhysicalFixture()
    start = base.EFFECTS['ISR70_policy_start_' + key]
    seed_positive(game, base.child(start, 'if'))
    game.execute(base.EFFECTS['ISR70_policy_refresh_costs'])
    return game


class BuildingCapacityTests(unittest.TestCase):
    def focus_fixture(self, identifier):
        game = PhysicalFixture()
        focus = base.FOCUSES[identifier]
        for k, _, _ in base.walk(base.child(focus, 'available', [])):
            if k in PARTIES:
                slot = next(v for a, _, v in base.walk(PARTIES[k]) if a == 'ruling_party')
                game.vars['ruling_party'] = float(slot)
        game.execute(REGULAR['ISR70_refresh_costs'])
        return game

    def test_all_twelve_focuses_allow_physical_room_without_manual_technology(self):
        for identifier in FOCUSES:
            with self.subTest(focus=identifier):
                game = self.focus_fixture(identifier)
                for state in game.states.values():
                    state['buildings']['infrastructure'] = 3
                game.complete_focus(identifier)
                self.assertEqual(len(game.grants), 1)
                state, kind, quantity = game.grants[0]
                self.assertEqual((kind, quantity), ('infrastructure', 1))
                self.assertEqual(game.states[state]['buildings'][kind], 4)
                self.assertEqual(game.states[state]['slots'], 1)
                self.assertEqual(game.vars['treasury'], 999.4)
                before = copy.deepcopy((game.vars, game.grants, game.states))
                game.complete_focus(identifier)
                self.assertEqual((game.vars, game.grants, game.states), before)

    def test_focus_exact_ceiling_and_lost_control_remain_blocking(self):
        for identifier in FOCUSES:
            for failure in ('full', 'owner', 'control'):
                with self.subTest(focus=identifier, failure=failure):
                    game = self.focus_fixture(identifier)
                    for state in game.states.values():
                        state['buildings']['infrastructure'] = 6 if failure == 'full' else 3
                        if failure == 'owner':
                            state['owner'] = 'EGY'
                        if failure == 'control':
                            state['controller'] = 'EGY'
                    game.complete_focus(identifier)
                    self.assertFalse(game.grants)
                    self.assertEqual(game.vars['treasury'], 1000)

    def test_actual_native_party_and_existing_funding_guards_remain(self):
        for identifier in FOCUSES:
            for failure in ('money', 'party'):
                game = self.focus_fixture(identifier)
                has_party = any(k in PARTIES for k, _, _ in base.walk(base.child(base.FOCUSES[identifier], 'available', [])))
                if failure == 'party' and not has_party:
                    continue
                if failure == 'money':
                    game.vars['treasury'] = .599
                else:
                    game.vars['ruling_party'] = 99
                before = game.vars['treasury']
                game.complete_focus(identifier)
                self.assertFalse(game.grants, (identifier, failure))
                self.assertEqual(game.vars['treasury'], before)

    def test_all_twenty_two_delayed_projects_pay_once_and_deliver_exact_assets(self):
        self.assertEqual(len(PROJECTS), 22)
        for key, project in PROJECTS.items():
            with self.subTest(project=key):
                game = project_fixture(key)
                start = base.EFFECTS['ISR70_policy_start_' + key]
                callback = base.child(base.EVENTS[project['callback']], 'immediate')
                game.execute(start)
                self.assertEqual(game.events, [(project['callback'], project['days'])])
                paid = game.vars[project['paid']]
                self.assertAlmostEqual(paid, 100 * project['share'])
                self.assertFalse(game.grants)
                before = base.snapshot(game)
                game.execute(start)
                self.assertEqual(base.snapshot(game), before)
                game.vars['gdp_total'] = 700
                game.execute(base.EFFECTS['ISR70_policy_refresh_costs'])
                game.execute(callback)
                self.assertIn(project['done'], game.flags)
                self.assertAlmostEqual(game.vars['treasury'], 1000 - paid)
                expected = sorted((int(b.get('state', project['states'][0])), b['type'], b.get('levels', b.get('level', 1))) for b in project['buildings'] if b['type'] != 'shared_slots')
                self.assertEqual(sorted(game.grants), expected)
                self.assertEqual(sum(s['slots'] for s in game.states.values()), project['slot_total'])
                delivered = base.snapshot(game)
                game.execute(callback)
                game.execute(start)
                self.assertEqual(base.snapshot(game), delivered)

    def test_delivery_rechecks_physical_cap_and_refunds_original_quote_once(self):
        for key, project in PROJECTS.items():
            for failure in ('capacity', 'control'):
                with self.subTest(project=key, failure=failure):
                    game = project_fixture(key)
                    game.execute(base.EFFECTS['ISR70_policy_start_' + key])
                    for state in project['states']:
                        if failure == 'capacity':
                            game.states[state]['buildings']['infrastructure'] = 6
                        else:
                            game.states[state]['controller'] = 'EGY'
                    game.vars['gdp_total'] = 700
                    game.execute(base.EFFECTS['ISR70_policy_refresh_costs'])
                    callback = base.child(base.EVENTS[project['callback']], 'immediate')
                    game.execute(callback)
                    self.assertEqual(game.vars['treasury'], 1000)
                    self.assertFalse(game.grants)
                    self.assertNotIn(project['done'], game.flags)
                    before = base.snapshot(game)
                    game.execute(callback)
                    self.assertEqual(base.snapshot(game), before)

    def test_two_level_grants_require_room_for_both_levels(self):
        for state in (208, 209):
            key = 'entrench_network_' + str(state)
            project = PROJECTS[key]
            for current, succeeds in ((4, True), (5, False), (6, False)):
                with self.subTest(state=state, current=current):
                    game = project_fixture(key)
                    game.states[state]['buildings']['infrastructure'] = current
                    game.execute(base.EFFECTS['ISR70_policy_start_' + key])
                    self.assertEqual(bool(game.events), succeeds)
                    if succeeds:
                        game.execute(base.child(base.EVENTS[project['callback']], 'immediate'))
                        self.assertEqual(game.states[state]['buildings']['infrastructure'], 6)

    def test_multi_state_package_cannot_pay_for_partial_delivery(self):
        game = project_fixture('municipal_pacts')
        game.states[206]['buildings']['infrastructure'] = 6
        game.execute(base.EFFECTS['ISR70_policy_start_municipal_pacts'])
        self.assertFalse(game.events)
        self.assertFalse(game.grants)
        self.assertEqual(game.vars['treasury'], 1000)

    def test_actual_project_scenario_funding_and_extra_receipts_still_gate_start(self):
        checked_receipts = 0
        for key, project in PROJECTS.items():
            start = base.EFFECTS['ISR70_policy_start_' + key]
            for failure in ('scenario', 'funds', 'bankruptcy'):
                with self.subTest(project=key, failure=failure):
                    game = project_fixture(key)
                    if failure == 'scenario':
                        game.scenario = False
                    elif failure == 'funds':
                        game.vars['treasury'] = 0
                    else:
                        game.bankrupt = True
                    before = base.snapshot(game)
                    game.execute(start)
                    self.assertEqual(base.snapshot(game), before)
            seeded = project_fixture(key)
            for receipt in sorted(seeded.flags):
                game = project_fixture(key)
                game.flags.remove(receipt)
                if game.condition(base.child(base.child(start, 'if'), 'limit')):
                    continue  # An actual OR alternative remains sufficient.
                checked_receipts += 1
                before = base.snapshot(game)
                game.execute(start)
                self.assertEqual(base.snapshot(game), before, (key, receipt))
        self.assertGreater(checked_receipts, 10)

    def test_canonical_focus_constructor_uses_the_same_shared_provider(self):
        path = HERE / 'build_content.py'
        source = ast.parse(path.read_text(encoding='utf-8-sig'))
        function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'building_gate')
        namespace = {'STAFF': {}, 'rewrite_queries': rewrite_queries, 're': __import__('re')}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
        result = namespace['building_gate']('206 = { add_extra_state_shared_building_slots = 2 add_building_construction = { type = infrastructure level = 2 instant_build = yes } }')
        self.assertIn('building_level@infrastructure', ' '.join(result))
        self.assertNotIn('free_building_slots', ' '.join(result))

    def test_canonical_project_constructor_reuses_physical_guard_at_both_boundaries(self):
        from policy_common import PolicyCompiler
        api = PolicyCompiler.__new__(PolicyCompiler)
        api.costs = set()
        api.projects = []
        api.nodes = {'ISR70_land_survey': {'label': 'Capacity Fixture'}}
        api.effects = {}
        api.events = []
        api.decisions = []
        api.localisation = {}
        api.opinions = {}
        api.data = {'idea_definitions': {}}
        api.tick = []
        api.decision_exports = []
        api.project('capacity_fixture', 208, [{'type': 'infrastructure', 'levels': 2}], .009, 240, unlock='land_survey')
        guard = api.projects[0]['guard']
        self.assertIn('building_level@infrastructure value = 4', guard)
        self.assertNotIn('free_building_slots', guard)
        self.assertIn(guard, api.effects['ISR70_policy_start_capacity_fixture'])
        self.assertIn(guard, api.events[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
