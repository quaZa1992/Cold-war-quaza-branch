# IMPERIA COLD WAR — Generic focus slider integration behaviour and preservation checks.
import copy
import re
import unittest
from pathlib import Path

import validate as V
import focus_integration as F

V.EFFECTS.update({k: v for k, op, v in V.parse((F.ROOT/F.EFFECTS).read_text(encoding='utf-8'))})


def country(position=0):
    result = V.Country()
    result.variables.update(gdp_total=100, treasury=10)
    result.call('icw_econ_initialize')
    result.variables.update(icw_econ_position=position, icw_econ_market_high_water=position)
    result.call('icw_econ_refresh_tier')
    return result


class GenericEconomicFocusTests(unittest.TestCase):
    def test_every_focus_at_every_integer_position_moves_correctly(self):
        for slug, step in F.STEPS.items():
            for position in range(-100, 101):
                with self.subTest(focus=slug, position=position):
                    c = country(position)
                    delta = max(-20, min(20, -position)) if step == 'mixed' else step
                    expected = max(-100, min(100, position + delta))
                    c.call(F.effect_name(slug))
                    self.assertEqual(c.number('icw_econ_position'), expected)
                    tier = next(t for t in V.TIERS if t[2] <= expected < t[3])
                    self.assertIn('icw_econ_' + tier[0], c.ideas)
                    self.assertEqual(len([i for i in c.ideas if i.startswith('icw_econ_')]), 1)
                    self.assertAlmostEqual(c.number('icw_econ_needle_x'), round((expected+100)*2.7+59))
                    self.assertEqual(c.number('treasury'), 10)

    def test_completed_focus_cannot_reapply_movement(self):
        for slug in F.STEPS:
            c = country(37)
            c.call(F.effect_name(slug))
            before = copy.deepcopy(c.__dict__)
            c.call(F.effect_name(slug))
            self.assertEqual(c.__dict__, before)

    def test_complete_routes(self):
        for slugs, expected in [([s for s,n in F.STEPS.items() if isinstance(n,int) and n>0], 50),
                                ([s for s,n in F.STEPS.items() if isinstance(n,int) and n<0], -60)]:
            c = country()
            for slug in slugs:
                c.call(F.effect_name(slug))
            self.assertEqual(c.number('icw_econ_position'), expected)
        mandatory = ['the_mixed_economy','indicative_planning','national_champions','social_partnership','planned_prosperity']
        for start in (-100, -80, -1, 0, 1, 80, 100):
            c = country(start)
            for slug in mandatory:
                old = c.number('icw_econ_position')
                c.call(F.effect_name(slug))
                self.assertLessEqual(abs(c.number('icw_econ_position')), abs(old))
            self.assertEqual(c.number('icw_econ_position'), 0)

    def test_running_reform_preserves_focus_step_and_frozen_finances(self):
        for reform in ('ownership','targets','autonomy','privatisation','capital'):
            c = country(20)
            c.call('icw_econ_start_' + reform)
            old_target = c.number('icw_econ_pending_position')
            old_days = c.number('icw_econ_days_remaining')
            c.call(F.effect_name('market_liberalisation'))
            self.assertEqual(c.number('icw_econ_pending_position'), old_target + 10)
            self.assertEqual(c.number('icw_econ_days_remaining'), old_days)
            c.call('icw_econ_complete_reform')
            self.assertEqual(c.number('icw_econ_position'), old_target + 10)
            self.assertAlmostEqual(c.number('treasury'), 10.5 if reform=='privatisation' else 10)

    def test_sale_is_reduced_at_ceiling_and_previous_market_high_water(self):
        for start, slug, expected_position, expected_cash in [
            (90,'market_liberalisation',100,0),
            (85,'market_liberalisation',100,.25),
            (0,'central_planning',0,0),
            (0,'collectivise_agriculture',0,0),
            (0,'socialist_industrialisation',-5,0),
            (0,'simplify_the_tax_code',15,.5),
        ]:
            c = country(start)
            c.call('icw_econ_start_privatisation')
            c.variables['gdp_total'] = 999
            c.call(F.effect_name(slug))
            c.call('icw_econ_complete_reform')
            self.assertEqual(c.number('icw_econ_position'), expected_position)
            self.assertAlmostEqual(c.number('treasury'), 10+expected_cash)

    def test_focus_progress_never_creates_a_repeat_sale_receipt(self):
        c = country()
        c.call(F.effect_name('market_liberalisation'))
        self.assertEqual(c.number('icw_econ_market_high_water'), 10)
        c.call('icw_econ_start_ownership'); c.call('icw_econ_complete_reform')
        c.variables['icw_econ_cooldown_days'] = 0
        c.call('icw_econ_start_privatisation'); c.call('icw_econ_complete_reform')
        self.assertEqual(c.number('treasury'), 10)

    def test_pending_overlord_request_is_invalidated_instead_of_auto_approved(self):
        c, parent = country(20), V.Country('AAA')
        world = {c.tag:c, parent.tag:parent}
        c.context.update(world=world, parent=parent.tag)
        parent.context.update(world=world)
        c.call('icw_econ_start_privatisation')
        self.assertIn('icw_econ_approval_pending', c.flags)
        c.call(F.effect_name('market_liberalisation'))
        self.assertNotIn('icw_econ_approval_pending', c.flags)
        self.assertNotIn('icw_econ_reform_active', c.flags)
        self.assertEqual(c.number('icw_econ_position'), 30)
        self.assertEqual(c.number('treasury'), 10)

    def test_missing_initialisation_and_near_zero_mixed_steps(self):
        c = V.Country()
        c.call(F.effect_name('central_planning'))
        self.assertEqual(c.number('icw_econ_position'), -10)
        for position in (-19.5, -0.01, 0, 0.01, 19.5):
            c = country(position)
            c.call(F.effect_name('the_mixed_economy'))
            self.assertAlmostEqual(c.number('icw_econ_position'), 0)

    def test_tooltip_evaluation_does_not_execute_the_focus(self):
        c = country(20)
        before = copy.deepcopy(c.__dict__)
        c.run([('effect_tooltip','=',[(F.effect_name('central_planning'),'=','yes')])])
        self.assertEqual(c.__dict__, before)

    def test_runtime_generation_encoding_and_only_targeted_rewards(self):
        text = (F.ROOT/F.TREE).read_text(encoding='utf-8')
        self.assertEqual(F.patch_generic_tree(text), text)
        for slug in F.STEPS:
            start, end = F.focus_span(text, 'GEN_1970_' + slug)
            self.assertEqual(text[start:end].count(F.effect_name(slug)+' = yes'), 1)
        self.assertEqual(len(re.findall(r'icw_gen_econ_focus_\w+ = yes', text)), 17)
        self.assertNotIn('icw_econ_position', text)
        for rel, expected in F.runtime_files().items():
            raw = (F.ROOT/rel).read_bytes()
            self.assertEqual(raw, expected.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8'))
            if not rel.endswith('.yml'):
                self.assertTrue(V.parse(raw.decode('utf-8')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
