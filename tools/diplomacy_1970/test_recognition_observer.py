# IMPERIA COLD WAR — Real German recognition transitions and crisis routing.
"""Execute emitted ledger transactions. Does not emulate GUI rendering, event delivery or multiplayer."""
import copy
from pathlib import Path
import unittest

from test_diplomacy import DiplomacyModel, ROOT, load, first, walk, D
from build import files


class RecognitionModel(DiplomacyModel):
    def __init__(self):
        super().__init__()
        windows = load('common/scripted_effects/COLDWAR_GER_1970_windows_effects.txt')
        self.effects['COLDWAR_GER_1970_rv_start_crisis'] = first(windows, 'COLDWAR_GER_1970_rv_start_crisis')
        # Response prompt and presentation have separate native providers, not emulated here.
        self.effects['COLDWAR_GER_1970_rv_ask_east_berlin'] = []
        self.effects['COLDWAR_GER_1970_rv_gui_refresh'] = []
        self.from_country = None

    def scope(self, name, current, root, prev):
        if name == 'FROM': return self.from_country
        return super().scope(name, current, root, prev)

    def value(self, name, current, root, prev):
        if name == 'FROM': return self.from_country
        return super().value(name, current, root, prev)


class RecognitionObserver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = RecognitionModel()

    def setUp(self):
        self.m = copy.deepcopy(self.template)
        self.g, self.d = self.m.c['GER'], self.m.c['DDR']
        self.g.flags.add('cwgg_initialized')
        self.g.ideas.add('COLDWAR_GER_1970_idea_hallstein_legacy')
        self.g.vars.update(cwgg_vertrag_3=D(0), cwgg_hebel_recht=D(2), cwgg_krise_typ=D(0))
        self.m.run('COLDWAR_Germany_recount_recognition', self.d)

    def grant(self, tag='SWI'):
        self.m.run('COLDWAR_Germany_recognise_DDR', self.m.c[tag])

    def notices(self, number=1):
        return [e for e in self.m.events if e[0] == 'COLDWAR_GERMAN_RECOGNITION.' + str(number)]

    def withdraw(self, tag='SWI'):
        self.m.c[tag].vars['recognised_countries'].remove(self.d)
        self.m.run('COLDWAR_Germany_recount_recognition', self.d)

    def test_historical_seed_is_silent_even_after_early_empty_startup_recount(self):
        self.m.run('COLDWAR_UN_1970_initialize')
        self.assertEqual(self.d.vars['Granted_Recognition'], 19)
        self.assertFalse(self.notices())
        self.assertFalse(self.notices(2))
        self.assertEqual(self.g.vars['cwgg_krise_typ'], 0)
        self.grant()
        self.assertEqual(self.d.vars['Granted_Recognition'], 20)
        self.assertEqual(len(self.notices()), 1)

    def test_existing_save_baselines_current_ledger_without_retrospective_popups(self):
        self.d.flags.discard('COLDWAR_DDR_recognition_watch_initialized')
        self.m.c['SWI'].vars['recognised_countries'] = [self.d]
        self.m.run('COLDWAR_Germany_recount_recognition', self.d)
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertFalse(self.notices())
        self.grant('ENG')
        self.assertEqual(len(self.notices()), 1)

    def test_new_recognition_notifies_bonn_and_starts_existing_native_crisis_once(self):
        self.grant()
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertEqual(self.g.vars['cwgg_krise_typ'], 5)
        self.assertEqual(self.g.vars['cwgg_krise_int'], 30)
        self.assertEqual(self.g.vars['cwgg_krise_max'], 3)
        self.assertEqual(self.g.vars['cwgg_druck'], 10)
        self.assertEqual(self.notices()[0][1], 'GER')
        self.assertEqual(self.notices()[0][2]['COLDWAR_Germany_recogniser'].id, 'SWI')
        before = (self.g.pp, self.d.pp)
        self.grant()
        self.m.run('COLDWAR_Germany_recount_recognition', self.d)
        self.assertEqual(len(self.notices()), 1)
        self.assertEqual(self.g.vars['cwgg_crises_total'], 1)
        self.assertEqual((self.g.pp, self.d.pp), before)

    def test_two_different_recognisers_keep_distinct_notification_targets(self):
        self.grant('SWI')
        self.grant('ENG')
        self.assertEqual(self.d.vars['Granted_Recognition'], 2)
        self.assertEqual([e[2]['COLDWAR_Germany_recogniser'].id for e in self.notices()], ['SWI', 'ENG'])
        self.assertEqual(self.g.vars['cwgg_crises_total'], 1)

    def test_withdrawal_and_regrant_notify_without_farming_another_crisis(self):
        self.grant()
        self.withdraw()
        self.assertEqual(self.d.vars['Granted_Recognition'], 0)
        self.assertEqual(len(self.notices(2)), 1)
        self.g.vars['cwgg_krise_typ'] = D(0)
        self.grant()
        self.assertEqual(len(self.notices()), 2)
        self.assertEqual(self.g.vars['cwgg_krise_typ'], 0)
        self.assertEqual(self.g.vars['cwgg_crises_total'], 1)

    def test_treaty_policy_cooldown_war_and_terminal_guards_preserve_notices(self):
        for condition in ('treaty', 'doctrine', 'cooldown', 'war', 'unity', 'other_crisis', 'legal_position', 'strike', 'dialogue'):
            with self.subTest(condition=condition):
                self.setUp()
                if condition == 'treaty': self.g.vars['cwgg_vertrag_3'] = D(1)
                if condition == 'doctrine': self.g.ideas.clear()
                if condition == 'cooldown': self.g.flags.add('cwgg_crisis_cd')
                if condition == 'war': self.g.wars.add('DDR')
                if condition == 'unity': self.m.g.flags.add('COLDWAR_GER_1970_unity_achieved')
                if condition == 'other_crisis': self.g.vars['cwgg_krise_typ'] = D(2)
                if condition == 'legal_position': self.g.vars['cwgg_hebel_recht'] = D(1)
                if condition == 'strike': self.g.flags.add('cwgg_strike_ordered')
                if condition == 'dialogue': self.d.flags.add('cwgg_ddr_countdown_dialogue_open')
                before = self.g.vars['cwgg_krise_typ']
                self.grant()
                self.assertEqual(self.d.vars['Granted_Recognition'], 1)
                self.assertEqual(len(self.notices()), 1)
                self.assertEqual(self.g.vars['cwgg_krise_typ'], before)

    def test_absent_bonn_and_non_1970_campaigns_are_safe(self):
        del self.m.c['GER']
        self.grant()
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertFalse(self.notices())
        self.setUp()
        self.m.scenario = False
        self.grant()
        self.assertFalse(self.notices())
        self.assertEqual(self.d.vars['Granted_Recognition'], 0)

    def test_full_native_grant_and_withdraw_buttons_route_through_observer(self):
        gui = first(first(load('common/scripted_guis/00_missiles_scripted_guis.txt'), 'scripted_gui'), 'MD_UN_system_gui')
        actions = first(gui, 'effects')
        actor = self.m.c['SWI']
        actor.pp = D(100)
        actor.vars['open_state'] = self.d
        for _ in range(2): self.m.execute(first(actions, 'grant_recog_button_click'), actor, actor, None)
        self.assertEqual(actor.pp, 75)
        self.assertEqual(len(self.notices()), 1)
        self.m.execute(first(actions, 'rescind_recog_button_click'), actor, actor, None)
        self.assertEqual(len(self.notices(2)), 1)
        self.assertEqual(self.d.vars['Granted_Recognition'], 0)

    def test_pressure_response_writes_ledger_before_recount(self):
        event = next(v for k, o, v in load('events/International Recognition.txt') if k == 'country_event' and first(v, 'id') == 'recognition.8')
        self.d.flags.add('pressured_to_recognize_@ROOT')
        actor = self.m.c['SWI']
        rows = [row for row in first(event, 'option') if row[0] not in ('name', 'ai_chance')]
        self.m.execute(rows, actor, actor, None)
        self.assertIn(self.d, actor.vars['recognised_countries'])
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertEqual(len(self.notices()), 1)

    def test_independence_response_updates_immediately_before_reply(self):
        event = next(v for k, o, v in load('events/International Recognition.txt') if k == 'country_event' and first(v, 'id') == 'recognition.31')
        option = next(v for k, o, v in event if k == 'option' and first(v, 'name') == 'recognition.31.b')
        actor = self.m.c['SWI']
        self.m.from_country = self.d
        self.m.execute([r for r in option if r[0] not in ('name', 'ai_chance')], actor, actor, self.d)
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertEqual(len(self.notices()), 1)

    def test_mutual_recognition_counts_bonn_without_starting_a_crisis(self):
        self.m.run('COLDWAR_Germany_mutual_recognition', self.g)
        self.assertEqual(len(self.notices()), 1)
        self.assertEqual(self.g.vars['cwgg_krise_typ'], 0)
        self.assertEqual(self.d.vars['Granted_Recognition'], 1)
        self.assertEqual(self.g.vars['Granted_Recognition'], 1)

    def test_rendered_sources_events_encoding_and_real_crisis_providers(self):
        for rel, source in files().items():
            self.assertEqual((ROOT / rel).read_text(encoding='utf-8-sig'), source)
            self.assertEqual((ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf'), rel.endswith('.yml'))
        windows = load('common/scripted_effects/COLDWAR_GER_1970_windows_effects.txt')
        for key in ('COLDWAR_GER_1970_rv_pick_crisis', 'COLDWAR_GER_1970_rv_ddr_ai'):
            self.assertNotIn(('cwgg_t_typ', '=', '5'), [v[0] for k, o, v in walk(first(windows, key)) if k == 'set_temp_variable'])
        events = load('events/COLDWAR_German_recognition_1970.txt')
        self.assertEqual([first(v, 'id') for k, o, v in events if k == 'country_event'], ['COLDWAR_GERMAN_RECOGNITION.1', 'COLDWAR_GERMAN_RECOGNITION.2'])
        self.assertTrue(all(first(v, 'picture') == 'GFX_political_deal' for k, o, v in events if k == 'country_event'))


if __name__ == '__main__': unittest.main(verbosity=2)
