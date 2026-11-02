# IMPERIA COLD WAR — One-time German recognition political power regression checks.
"""Verify emitted recognition providers and the replay-safe political-power contract."""
from pathlib import Path
import unittest

from build import files
from test_diplomacy import DiplomacyModel, D, first, parse

ROOT = Path(__file__).resolve().parents[2]


class RecognitionPoliticalPower(unittest.TestCase):
    def setUp(self):
        self.m = DiplomacyModel()
        emitted = files()
        self.m.effects.update((key, value) for key, _, value in parse(emitted['common/scripted_effects/COLDWAR_diplomacy_1970.txt']))
        self.m.triggers.update((key, value) for key, _, value in parse(emitted['common/scripted_triggers/COLDWAR_diplomacy_1970.txt']))
        self.ger, self.ddr = self.m.c['GER'], self.m.c['DDR']

    def run_effect(self, effect_name, recipient, recogniser=None):
        self.m.execute(self.m.effects[effect_name], recipient, recipient, recogniser)

    def test_emitted_provider_has_seeded_recogniser_ledger_and_scenario_gate(self):
        generated = files()
        script = generated['common/scripted_effects/COLDWAR_diplomacy_1970.txt']
        parsed = parse(script)
        emitted_keys = {key for key, _, _ in parsed}
        self.assertIn('COLDWAR_Germany_seed_recognition_pp', emitted_keys)
        self.assertIn('COLDWAR_Germany_recognition_pp_once', emitted_keys)
        self.assertIn('COLDWAR_Germany_seed_recognition_pp = {', script)
        self.assertIn('COLDWAR_Germany_recognition_pp_once = {', script)
        self.assertIn('cwgg_recognition_pp_paid = PREV', script)
        self.assertIn('IMP_is_1970_scenario = yes', script)
        startup = generated['common/on_actions/COLDWAR_diplomacy_1970.txt']
        self.assertIn('COLDWAR_Germany_retire_recognition_points = yes COLDWAR_Germany_seed_recognition_pp = yes', startup)

    def test_emitted_tier_values_are_native_and_unchanged(self):
        script = files()['common/scripted_effects/COLDWAR_diplomacy_1970.txt']
        native = (ROOT / 'common/scripted_effects/01_international_systems_effects.txt').read_text(encoding='utf-8-sig')
        tier_values = [5, 10, 15, 25, 50, 100]
        for value in tier_values:
            self.assertIn(f'add_political_power = {value}', script)
            self.assertIn(f'add_political_power = {value}', native)
        self.assertIn('COLDWAR_Germany_recognition_pp_once = yes', native)
        self.assertRegex(native, r'COLDWAR_Germany_recognition_subject = yes IMP_is_1970_scenario = yes\s*\} COLDWAR_Germany_recognition_pp_once = yes \}\s*else = \{')

    def test_distinct_recogniser_and_recipient_ledgers_prevent_replay(self):
        tiers = {'non_power': 5, 'minor_power': 10, 'regional_power': 15,
                 'large_power': 25, 'great_power': 50, 'super_power': 100}
        for tier, amount in tiers.items():
            with self.subTest(tier=tier):
                recipient, recogniser = self.ger, self.m.c['SWI']
                recipient.flags.add('COLDWAR_Germany_recognition_pp_seeded')
                recipient.vars['cwgg_recognition_pp_paid'] = []
                recogniser.ideas = {tier}
                recogniser.vars['recognised_countries'] = [recipient]
                start = recipient.pp
                self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
                self.assertEqual(recipient.pp - start, D(amount))
                # Duplicate callback, withdrawal and restoration retain the paid receipt.
                for _ in range(2):
                    self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
                recogniser.vars['recognised_countries'] = []
                self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
                recogniser.vars['recognised_countries'] = [recipient]
                self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
                self.assertEqual(recipient.pp - start, D(amount))
                self.assertEqual(recipient.vars['cwgg_recognition_pp_paid'], [recogniser])

    def test_historical_baseline_pays_no_backdated_award_but_new_country_does(self):
        recipient = self.ger
        historical = [self.m.c[tag] for tag in ('SOV', 'POL', 'ROM')]
        for recogniser in historical:
            recogniser.vars['recognised_countries'] = [recipient]
        start = recipient.pp
        self.run_effect('COLDWAR_Germany_seed_recognition_pp', recipient)
        self.assertEqual(recipient.pp, start)
        self.assertEqual(set(recipient.vars['cwgg_recognition_pp_paid']), set(historical))
        self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, historical[0])
        self.assertEqual(recipient.pp, start)
        new = self.m.c['ENG']
        new.ideas = {'large_power'}
        new.vars['recognised_countries'] = [recipient]
        self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, new)
        self.assertEqual(recipient.pp - start, D(25))

    def test_ger_and_ddr_have_independent_ledgers_and_non_1970_uses_native_tier(self):
        recogniser = self.m.c['ENG']
        recogniser.ideas = {'large_power'}
        recogniser.vars['recognised_countries'] = [self.ger, self.ddr]
        for recipient in (self.ger, self.ddr):
            recipient.flags.add('COLDWAR_Germany_recognition_pp_seeded')
            recipient.vars['cwgg_recognition_pp_paid'] = []
        ger_start, ddr_start = self.ger.pp, self.ddr.pp
        for recipient in (self.ger, self.ddr):
            self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
            self.run_effect('COLDWAR_Germany_recognition_pp_once', recipient, recogniser)
        self.assertEqual(self.ger.pp - ger_start, D(25))
        self.assertEqual(self.ddr.pp - ddr_start, D(25))
        # A false claimant and self-recognition are both rejected by the emitted provider.
        false_claimant = self.m.c['QAT']
        false_claimant.ideas = {'super_power'}
        false_claimant.vars['recognised_countries'] = []
        self.run_effect('COLDWAR_Germany_recognition_pp_once', self.ger, false_claimant)
        self.run_effect('COLDWAR_Germany_recognition_pp_once', self.ger, self.ger)
        self.assertEqual(self.ger.pp - ger_start, D(25))
        native = (ROOT / 'common/scripted_effects/01_international_systems_effects.txt').read_text(encoding='utf-8-sig')
        self.assertIn('else = {\n\t\tif = { limit = { PREV = { has_idea = non_power } } add_political_power = 5 }', native)
        self.m.scenario = False
        non_1970 = self.m.c['QAT']
        start = non_1970.pp
        non_1970.vars['recognised_countries'] = [self.ger]
        self.m.c['GER'].ideas = {'non_power'}
        native_increment = first(parse(native), 'recognition_grant_increment')
        self.m.execute(native_increment[:4], non_1970, non_1970, self.ger)
        self.assertEqual(non_1970.pp - start, D(5))

    def test_crisis_claimant_capture_is_inside_new_crisis_start_guard(self):
        effect = files()['common/scripted_effects/COLDWAR_diplomacy_1970.txt']
        observer = effect.split('COLDWAR_Germany_observe_DDR_recognition = {', 1)[1].split('\n}', 1)[0]
        guard = observer.index('check_variable = { cwgg_krise_typ = 0 }')
        capture = observer.index('cwgg_recognition_country = PREV')
        start = observer.index('set_temp_variable = { cwgg_t_typ = 5 }')
        self.assertLess(guard, capture)
        self.assertLess(capture, start)
        self.assertIn('event_target:COLDWAR_Germany_recogniser', observer)
        self.assertNotIn('cwgg_recognition_country', effect.split('COLDWAR_Germany_observe_DDR_recognition = {', 1)[0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
