# IMPERIA COLD WAR — Five reviewed construction-award regressions.
"""Exercise bounded prospective output before installation, then loaded output.

Native queue diagnostics are independent E: fixtures. These tests verify only
the chosen instant award transactions, with manual construction permission zero.
"""
from __future__ import annotations
from pathlib import Path
import copy
import importlib.util
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from building_grants.apply_reviewed_queue import outputs, VIE, walk, get, field, nodes

BEFORE, AFTER = outputs()
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
import test_transactions as viet
viet.E.update({k: v for k, _, v in viet.parse(AFTER['common/scripted_effects/COLDWAR_VIE_1970_effects.txt'])})
sys.path.insert(0, str(ROOT / 'tools/greece_1970'))
spec = importlib.util.spec_from_file_location('queue_greek_validate', ROOT / 'tools/greece_1970/validate.py')
greek = importlib.util.module_from_spec(spec); spec.loader.exec_module(greek)
greek.EFFECTS.update({k: v for k, _, v in greek.parse(AFTER['common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt'])})


class ReviewedAwardTests(unittest.TestCase):
    def viet(self, suffix):
        w = viet.World(); fid = 'COLDWAR_VIE_' + suffix
        w.ready(fid); w.vie.construction_entitlements.update(infrastructure=0, anti_air_building=0)
        if suffix == 'kiet_transport':w.vie.leader = 'Vo Van Kiet'
        state, kind = VIE[suffix]
        w.states[state].levels[kind] = 1 if kind == 'infrastructure' and state != 524 else 0
        return w, fid, state, kind

    def test_all_four_vietnamese_awards_are_exact_real_and_once_only(self):
        for suffix in VIE:
            with self.subTest(suffix=suffix):
                w, fid, sid, kind = self.viet(suffix)
                initial = w.states[sid].levels[kind]
                w.grant(fid)
                self.assertEqual(w.states[sid].levels[kind], initial + 1)
                self.assertEqual(w.states[sid].extra_slots, 1)
                self.assertAlmostEqual(w.vie.variables['treasury'], 1 - viet.N[fid]['cash'])
                self.assertTrue(w.flag(w.vie, fid + '_reward_applied'))
                self.assertFalse(w.flag(w.vie, fid + '_pending'))
                self.assertEqual(w.queue, [(sid, kind, 'yes')])
                self.assertFalse(w.vie.technologies)
                before = copy.deepcopy((w.vie, w.states, w.queue))
                w.grant(fid)
                self.assertEqual((w.vie, w.states, w.queue), before)

    def test_vietnamese_native_guard_failures_cost_nothing_then_retry(self):
        for suffix in VIE:
            for failure in ('owner', 'control', 'full', 'funds', 'parent', 'scenario'):
                with self.subTest(suffix=suffix, failure=failure):
                    w, fid, sid, kind = self.viet(suffix)
                    if failure == 'owner':w.states[sid].owner = 'CHI'
                    if failure == 'control':w.states[sid].controller = 'CHI'
                    if failure == 'full':w.states[sid].levels[kind] = 6 if kind == 'infrastructure' else 5
                    if failure == 'funds':w.vie.variables['treasury'] = viet.N[fid]['cash'] - .00001
                    if failure == 'parent':
                        for group in viet.N[fid]['prerequisites']:
                            for p in group:w.vie.flags.pop(p + '_reward_applied', None)
                    if failure == 'scenario':w.vie.scenario = False
                    cash = w.vie.variables['treasury']
                    w.grant(fid)
                    self.assertAlmostEqual(w.vie.variables['treasury'], cash)
                    self.assertFalse(w.queue)
                    self.assertEqual(w.states[sid].extra_slots, 0)
                    self.assertTrue(w.flag(w.vie, fid + '_pending'))
                    w.states[sid].owner = w.states[sid].controller = 'VIE'
                    w.states[sid].levels[kind] = 1
                    w.vie.variables['treasury'] = 1; w.vie.scenario = True; w.ready(fid)
                    w.grant(fid)
                    self.assertEqual(w.states[sid].levels[kind], 2)
                    self.assertEqual(w.states[sid].extra_slots, 1)

    def test_kiet_keeps_exact_party_and_leader_guards(self):
        for kind in ('leader', 'party'):
            w, fid, sid, building = self.viet('kiet_transport')
            if kind == 'leader':w.vie.leader = 'Le Duan'
            else:w.vie.variables['ruling_party'] = 2
            w.grant(fid)
            self.assertFalse(w.queue); self.assertEqual(w.vie.variables['treasury'], 1)

    def test_preview_is_complete_and_inert_for_all_four_while_locked(self):
        for suffix, (sid, kind) in VIE.items():
            fid = 'COLDWAR_VIE_' + suffix
            for rel, key, focus, reward in (
                ('common/national_focus/COLDWAR_VIE_1970_focus.txt', fid, True, 'completion_reward'),
                ('common/decisions/COLDWAR_VIE_1970_decisions.txt', fid + '_retry', False, 'complete_effect')):
                node = get(AFTER[rel], key, focus)
                completion = next(n for n in node.children() if n.key == reward)
                preview = next(n for n in completion.children() if n.key == 'effect_tooltip')
                text = AFTER[rel][preview.start:preview.end]
                self.assertIn('treasury_change', text)
                self.assertIn('add_extra_state_shared_building_slots = 1', text)
                self.assertIn('instant_build = yes', text)
                self.assertNotIn('COLDWAR_QUEUE_', text)
                w, _, _, _ = self.viet(suffix); w.vie.scenario = False; w.vie.variables['treasury'] = 0
                before = copy.deepcopy(w.__dict__)
                w.run(viet.parse(text))
                self.assertEqual(w.__dict__, before)

    def test_greece_keeps_exact_gdp_quote_and_instant_asset(self):
        for gdp in (20, 100, 230.75):
            w = greek.World(); state = w.states['139']
            state['slots'] = False; state['levels']['infrastructure'] = 2
            w.countries['GRE']['variables'].update(gdp_total=gdp, treasury=100)
            w.call('complete_economy_18')
            self.assertEqual(w.value('building_level@infrastructure', '139'), 3)
            self.assertEqual(state['extra_slots'], 1)
            self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'], 100 - gdp * .015)
            before = copy.deepcopy(w.__dict__); w.call('complete_economy_18')
            self.assertEqual(w.__dict__, before)

    def test_greece_lost_owner_control_capacity_and_funds_retry_safely(self):
        for failure in ('owner', 'control', 'full', 'funds', 'scenario', 'zero_gdp'):
            w = greek.World(); state = w.states['139']; state['levels']['infrastructure'] = 2
            if failure == 'owner':state['owner'] = 'TUR'
            if failure == 'control':state['controller'] = 'TUR'
            if failure == 'full':state['levels']['infrastructure'] = 6
            if failure == 'funds':w.countries['GRE']['variables']['treasury'] = 1.49999
            if failure == 'scenario':w.scenario = False
            if failure == 'zero_gdp':w.countries['GRE']['variables']['gdp_total'] = 0
            cash = w.countries['GRE']['variables']['treasury']; w.call('complete_economy_18')
            self.assertEqual(w.countries['GRE']['variables']['treasury'], cash)
            self.assertEqual(state['extra_slots'], 0); self.assertFalse(state['builds'])
            state.update(owner='GRE', controller='GRE');state['levels']['infrastructure'] = 2
            w.countries['GRE']['variables'].update(treasury=10, gdp_total=200);w.scenario = True
            w.call('complete_economy_18')
            self.assertAlmostEqual(w.countries['GRE']['variables']['treasury'], 7)
            self.assertEqual(state['extra_slots'], 1)

    def test_slot_order_and_no_production_technology_or_queue_remain(self):
        self.assertFalse(any('/technologies/' in rel for rel in AFTER))
        for country, suffixes in (('VIE', VIE), ('GRE', ('economy_18',))):
            rel = 'common/scripted_effects/COLDWAR_' + country + '_1970' + ('_effects.txt' if country == 'VIE' else '_tree_effects.txt')
            for suffix in suffixes:
                name = 'COLDWAR_VIE_apply_' + suffix if country == 'VIE' else 'COLDWAR_GRE_1970_grant_' + suffix
                n = get(AFTER[rel], name)
                text = AFTER[rel][n.start:n.end]
                self.assertNotIn('set_technology', text)
                self.assertNotIn('instant_build = no', text)
                self.assertLess(text.index('add_extra_state_shared_building_slots'), text.index('add_building_construction'))
                self.assertEqual(text.count('add_building_construction'), 1)

    def test_greek_locked_focus_and_retry_previews_are_complete_and_inert(self):
        for rel, key, focus, reward in (
            ('common/national_focus/COLDWAR_GRE_1970_focus.txt', 'COLDWAR_GRE_1970_economy_18', True, 'completion_reward'),
            ('common/decisions/COLDWAR_GRE_1970_tree_decisions.txt', 'COLDWAR_GRE_1970_retry_economy_18', False, 'complete_effect')):
            parent = get(AFTER[rel], key, focus)
            completion = next(n for n in parent.children() if n.key == reward)
            preview = next(n for n in completion.children() if n.key == 'effect_tooltip')
            text = AFTER[rel][preview.start:preview.end]
            for fragment in ('programme_cost', 'modify_treasury_effect', 'add_extra_state_shared_building_slots = 1',
                             'instant_build = yes', 'add_ideas = COLDWAR_GRE_1970_economy_18_programme'):
                self.assertIn(fragment, text)
            w = greek.World(scenario=False);w.states['139']['levels']['infrastructure'] = 6
            w.countries['GRE']['variables']['treasury'] = -100
            before = copy.deepcopy(w.__dict__);w.execute(greek.parse(text))
            self.assertEqual(w.__dict__, before)

    def test_vietnamese_canonical_reward_constructor_matches_actual_payloads(self):
        for suffix in VIE:
            fid = 'COLDWAR_VIE_' + suffix
            self.assertTrue(viet.N[fid]['instant_build'])
            outer = viet.first(viet.E['COLDWAR_VIE_apply_' + suffix], 'if')
            transaction = viet.first(outer, 'if')
            payload = [row for row in transaction if row[0] != 'limit']
            self.assertEqual(payload[-2:], [('set_country_flag', '=', fid + '_reward_applied'),
                                            ('clr_country_flag', '=', fid + '_pending')])
            self.assertEqual(payload[:-2], viet.parse(viet.N[fid]['raw_reward_code']))

    def test_late_source_race_is_detected_before_first_runtime_replacement(self):
        from building_grants import apply_reviewed_queue as patch
        with tempfile.TemporaryDirectory(prefix='.icw_capacity_cas_', dir=Path(__file__).resolve().parent) as directory:
            base = Path(directory)
            self.assertTrue(base.resolve().is_relative_to(Path(__file__).resolve().parent))
            before = {'a.txt': 'a original\n', 'b.txt': 'b original\n'}
            for rel, text in before.items():(base / rel).write_bytes(text.encode())
            original = tempfile.NamedTemporaryFile
            def staged(*args, **kwargs):
                (base / 'b.txt').write_bytes(b'other chat edit\n')
                return original(*args, **kwargs)
            with mock.patch.object(patch, 'ROOT', base), mock.patch.object(patch, 'outputs', return_value=(before, {'a.txt': 'a changed\n', 'b.txt': 'b changed\n'})), mock.patch.object(patch.tempfile, 'NamedTemporaryFile', side_effect=staged):
                with self.assertRaisesRegex(AssertionError, 'Concurrent edit: b.txt'):patch.apply()
            self.assertEqual((base / 'a.txt').read_bytes(), b'a original\n')
            self.assertEqual((base / 'b.txt').read_bytes(), b'other chat edit\n')
            self.assertEqual(sorted(p.name for p in base.iterdir()), ['a.txt', 'b.txt'])

    def test_unrelated_focuses_are_byte_identical(self):
        for country, selected in (('VIE', {'COLDWAR_VIE_' + s for s in VIE}), ('GRE', {'COLDWAR_GRE_1970_economy_18'})):
            rel = f'common/national_focus/COLDWAR_{country}_1970_focus.txt'
            new = {field(n.children(), 'id'): n for n in walk(nodes(AFTER[rel])) if n.key == 'focus'}
            for n in walk(nodes(BEFORE[rel])):
                fid = field(n.children(), 'id') if n.key == 'focus' else None
                if fid and fid not in selected:
                    other = new[fid]
                    self.assertEqual(BEFORE[rel][n.start:n.end], AFTER[rel][other.start:other.end], fid)


if __name__ == '__main__':
    unittest.main()
