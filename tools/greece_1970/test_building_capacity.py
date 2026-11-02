# IMPERIA COLD WAR — Greece physical radar capacity and preview regressions.
"""Read emitted transactions and the canonical pure preview functions only."""
from pathlib import Path
import ast
import copy
import unittest
from validate import World, P, EFFECTS, FOCUSES, AST, first, vals, walk, parse

HERE = Path(__file__).resolve().parent

class RadarCapacityTests(unittest.TestCase):
    def world(self):
        w = World()
        w.countries['GRE']['variables'].update(gdp_total=100, treasury=1)
        w.call('complete_air_0')
        for s in w.states.values():
            # Original free_building_slots fixture deliberately denies manual
            # construction. Physical radar room remains a separate predicate.
            s['slots'] = False
            s['levels']['radar_station'] = 6
        return w

    def test_manual_permission_zero_does_not_block_one_real_site(self):
        w = self.world()
        w.states['139']['levels']['radar_station'] = 5
        available = first(FOCUSES[P + 'air_1'], 'available')
        self.assertTrue(w.condition(available))
        w.call('complete_air_1')
        self.assertEqual(w.value('building_level@radar_station', '139'), 6)
        self.assertEqual(w.states['139']['extra_slots'], 1)
        self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'], .75)
        snapshot = copy.deepcopy(w.__dict__)
        w.call('complete_air_1')
        self.assertEqual(w.__dict__, snapshot)

    def test_full_or_lost_site_does_not_charge_and_can_retry_after_restoration(self):
        for failure in ('full', 'owner', 'control', 'scenario', 'funds'):
            with self.subTest(failure=failure):
                w = self.world()
                if failure != 'full':
                    w.states['139']['levels']['radar_station'] = 5
                if failure == 'owner':
                    w.states['139']['owner'] = 'TUR'
                if failure == 'control':
                    w.states['139']['controller'] = 'TUR'
                if failure == 'scenario':
                    w.scenario = False
                if failure == 'funds':
                    w.countries['GRE']['variables']['treasury'] = .249
                cash = w.countries['GRE']['variables']['treasury']
                w.call('complete_air_1')
                self.assertEqual(sum(len(s['builds']) for s in w.states.values()), 0)
                self.assertEqual(w.countries['GRE']['variables']['treasury'], cash)
                w.states['139'].update(owner='GRE', controller='GRE')
                w.states['139']['levels']['radar_station'] = 5
                w.scenario = True
                w.countries['GRE']['variables']['treasury'] = 1
                w.call('complete_air_1')
                self.assertEqual(sum(len(s['builds']) for s in w.states.values()), 1)

    def test_slot_precedes_construction_in_the_paid_once_guard(self):
        grant = EFFECTS[P + 'grant_air_1']
        selected = next(v for k, _, v in walk(grant) if k == 'random_owned_controlled_state')
        keys = [k for k, _, _ in selected]
        self.assertLess(keys.index('add_extra_state_shared_building_slots'), keys.index('add_building_construction'))
        self.assertEqual(first(selected, 'add_extra_state_shared_building_slots'), '1')
        self.assertEqual(first(first(selected, 'add_building_construction'), 'instant_build'), 'yes')

    def test_complete_native_preview_is_inert_while_all_sites_are_locked(self):
        w = self.world()
        w.countries['GRE']['variables']['treasury'] = 0
        focus = first(FOCUSES[P + 'air_1'], 'completion_reward')
        preview = next(v for k, _, v in focus if k == 'effect_tooltip')
        keys = {k for k, _, _ in walk(preview)}
        self.assertTrue({'modify_treasury_effect', 'add_extra_state_shared_building_slots', 'add_building_construction'} <= keys)
        self.assertNotIn('free_building_slots', keys)
        before = copy.deepcopy(w.__dict__)
        w.execute([('effect_tooltip', '=', preview)])
        self.assertEqual(w.__dict__, before)

    def test_canonical_focus_and_retry_previews_match_emitted_source(self):
        source = HERE / 'compile.py'
        module = ast.parse(source.read_text(encoding='utf-8-sig'))
        names = {'block', 'radar_assets', 'radar_reward'}
        ns = {'P': P}
        exec(compile(ast.Module(body=[n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]), str(source), 'exec'), ns)
        expected = parse(ns['radar_reward'](P + 'complete_air_1 = yes'))
        self.assertEqual(first(FOCUSES[P + 'air_1'], 'completion_reward'), expected)
        decisions = AST['common/decisions/COLDWAR_GRE_1970_tree_decisions.txt']
        category = first(decisions, P + 'tree_programmes')
        retry = first(category, P + 'retry_air_1')
        self.assertEqual(first(retry, 'complete_effect'), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
