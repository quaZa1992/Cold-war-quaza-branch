# IMPERIA COLD WAR — German two-player sandbox historical rail regressions
"""Check emitted script for retired DDR rails and human-country safeguards."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/colonial_affairs'))
from test_runtime import Model, Scope, parse, first


def load(rel):
    return parse((ROOT / rel).read_text(encoding='utf-8-sig'))


def provider_map(rel):
    return {key: value for key, _op, value in load(rel)}


def events_by_id(rel):
    return {
        first(body, 'id'): body
        for key, _op, body in load(rel)
        if key == 'country_event' and first(body, 'id') is not None
    }


def deep_rows(rows):
    metadata = {'ai_chance', 'trigger', 'available', 'limit', 'mean_time_to_happen'}
    for key, _op, value in rows:
        yield key, value
        if isinstance(value, list) and key not in metadata:
            yield from deep_rows(value)


class SandboxHistory(unittest.TestCase):
    def test_retired_collapse_spirits_are_inert_and_startup_cleans_attachments(self):
        ideas = first(first(load('common/ideas/COLDWAR_GER_1970_ideas.txt'), 'ideas'), 'country')
        migration = first(load('common/scripted_effects/COLDWAR_GER_1970_sandbox.txt'), 'COLDWAR_GER_1970_sandbox_migrate')
        removed = {v for key,v in deep_rows(migration) if key == 'remove_ideas'}
        for key in ('COLDWAR_GER_1970_idea_ddr_crackdown','COLDWAR_GER_1970_idea_ddr_round_table'):
            spirit = first(ideas,key)
            self.assertEqual(first(spirit,'modifier'),[])
            self.assertEqual(first(spirit,'allowed'), [('always','=','no')])
            self.assertIn(key,removed)

    def test_border_availability_reads_native_policy_instead_of_legacy_outcome_flag(self):
        m=Model();ger=m.c['GER']=Scope('GER');ddr=m.c['DDR']=Scope('DDR')
        m.triggers.update(provider_map('common/scripted_triggers/COLDWAR_GER_1970_sandbox.txt'))
        native=provider_map('common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt')
        m.triggers['COLDWAR_DDR_ladder_border_active']=native['COLDWAR_DDR_ladder_border_active']
        trigger=m.triggers['COLDWAR_GER_1970_border_open']
        ddr.flags.add('COLDWAR_DDR_initialized')
        ddr.ideas.add('COLDWAR_DDR_border_the_iron_border')
        m.g.flags.add('COLDWAR_GER_1970_wall_open')
        self.assertFalse(m.condition(trigger,ger))
        ddr.ideas.clear();m.g.flags.clear()
        self.assertTrue(m.condition(trigger,ger))

    def setUp(self):
        self.ger_effects = provider_map('common/scripted_effects/COLDWAR_GER_1970_effects.txt')
        self.ddr_effects = provider_map('common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt')
        self.ddr_events = events_by_id('events/COLDWAR_DDR_1970_events.txt')
        self.ger_events = events_by_id('events/COLDWAR_GER_1970_events.txt')
        self.model = Model()
        self.ddr = self.model.c['DDR'] = Scope('DDR')
        self.ger = self.model.c['GER'] = Scope('GER')
        self.model.root = self.ddr
        self.model.effects.update(self.ddr_effects)

    def test_legacy_ger_control_providers_are_absent(self):
        retired = (
            'check_wende', 'wall_opens', 'ddr_crackdown_roll',
            'request_two_plus_four', 'complete_unity', 'leadership_tick',
            'unity_neutral',
        )
        names = set(self.ger_effects)
        for suffix in retired:
            self.assertNotIn('COLDWAR_GER_1970_' + suffix, names)
        self.assertFalse(any(
            'COLDWAR_GER_1970_' + suffix in repr(body)
            for suffix in retired for body in self.ger_effects.values()
        ))

    def test_queued_legacy_ddr_events_are_hidden_empty_stubs(self):
        retired_ids = [1, *range(30, 35), *range(36, 40)]
        for number in retired_ids:
            event_id = f'COLDWAR_GER_DDR.{number}'
            with self.subTest(event=event_id):
                event = next(body for body in load('events/COLDWAR_GER_1970_events.txt')
                             if body[0] == 'country_event' and first(body[2], 'id') == event_id)[2]
                self.assertEqual(first(event, 'hidden'), 'yes')
                self.assertIsNone(first(event, 'title'))
                options = [value for key, _op, value in event if key == 'option']
                self.assertEqual(len(options), 1)
                effects = [(key, value) for key, value in deep_rows(options[0])
                           if key not in ('name', 'ai_chance', 'log')]
                self.assertEqual(effects, [])
                before = deepcopy((self.ddr.vars, self.ddr.flags, self.ddr.overlord))
                actions = [(key, op, value) for key, op, value in options[0]
                           if key not in ('name', 'ai_chance', 'log')]
                self.model.execute(actions, self.ddr, self.ddr, None)
                self.assertEqual(before, (self.ddr.vars, self.ddr.flags, self.ddr.overlord))

    def test_honecker_scheduled_provider_is_inert(self):
        # EVD.1 lives in the GER-to-DDR compatibility namespace.
        event = next(body for key, _op, body in load('events/COLDWAR_GER_1970_events.txt')
                     if key == 'country_event' and first(body, 'id') == 'COLDWAR_GER_DDR.1')
        self.assertEqual(first(event, 'hidden'), 'yes')
        self.assertIsNone(first(event, 'title'))
        option = first(event, 'option')
        self.assertEqual([(key, value) for key, value in deep_rows(option)
                          if key not in ('name', 'ai_chance', 'log')], [])
        actions = [(key, op, value) for key, op, value in option
                   if key not in ('name', 'ai_chance', 'log')]
        before = deepcopy((self.ddr.vars, self.ddr.flags, self.ddr.overlord))
        self.model.execute(actions, self.ddr, self.ddr, None)
        self.assertEqual(before, (self.ddr.vars, self.ddr.flags, self.ddr.overlord))

    def test_no_calendar_tick_schedules_retired_bonn_political_events(self):
        retired_ids = {f'COLDWAR_GER.{number}' for number in (26, 28, 30, 31, 34, 37, 38)}
        for provider in self.ger_effects.values():
            for key, value in deep_rows(provider):
                if key == 'country_event' and isinstance(value, list):
                    self.assertNotIn(first(value, 'id'), retired_ids)

    def test_safe_first_options_do_not_change_government_or_leadership(self):
        forbidden_commands = {
            'set_country_leader', 'retire_character', 'set_ruling_party',
            'set_politics', 'change_government', 'annex_country',
            'set_autonomy', 'leave_faction', 'puppet', 'change_tag',
        }
        political_vars = ('leader', 'ruling_party', 'gov_coalition_array')
        for number in (26, 28, 30, 31, 34, 37, 38):
            event = self.ger_events[f'COLDWAR_GER.{number}']
            option = next(value for key, _op, value in event if key == 'option')
            for key, value in deep_rows(option):
                self.assertNotIn(key, forbidden_commands, f'COLDWAR_GER.{number}: {key}')
                if key in ('set_variable', 'add_to_variable', 'subtract_from_variable') and value:
                    var = str(value[0][0])
                    self.assertFalse(any(token in var for token in political_vars),
                                     f'COLDWAR_GER.{number}: {var}')

    def test_native_ddr_mortality_events_are_ineligible_for_human_ddr(self):
        self.ddr.flags.add('COLDWAR_DDR_initialized')
        self.model.date = '1990.1.1'
        for event_id in ('COLDWAR_DDR.40', 'COLDWAR_DDR.41', 'COLDWAR_DDR.42'):
            event = self.ddr_events[event_id]
            with self.subTest(event=event_id):
                self.assertFalse(self.model.condition(first(event, 'trigger'), self.ddr))
                option = first(event, 'option')
                self.assertFalse(self.model.condition(first(option, 'trigger'), self.ddr))

    def test_native_mortality_effects_are_human_noops_and_remain_ai_enabled(self):
        death_effects = ('COLDWAR_DDR_leader_dies_ulb', 'COLDWAR_DDR_leader_dies_lam',
                         'COLDWAR_DDR_leader_dies_hof')
        before = deepcopy((self.ddr.vars, self.ddr.flags, self.model.events))
        for effect in death_effects:
            self.model.run(effect, self.ddr)
        self.assertEqual(before, (self.ddr.vars, self.ddr.flags, self.model.events))

        self.ddr.ai = True
        self.model.run('COLDWAR_DDR_leader_dies_lam', self.ddr)
        self.assertIn('COLDWAR_DDR_dead_lam', self.ddr.flags)


if __name__ == '__main__':
    unittest.main(verbosity=2)
