# IMPERIA COLD WAR — Independent installed military-transition regression checks.
"""Exercise emitted guards and transactions in a bounded source model, not HOI4."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import first, parse, values

P = 'COLDWAR_CHL_'


def read(relative):
    return parse((ROOT / relative).read_text(encoding='utf-8'))


TRIGGERS = dict((k, v) for part in ('core', 'politics') for k, _, v in read(f'common/scripted_triggers/COLDWAR_CHL_1970_{part}.txt'))
TRIGGERS['nationalist_military_junta_are_in_power'] = first(read('common/scripted_triggers/01_political_triggers.txt'), 'nationalist_military_junta_are_in_power')
EFFECTS = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_CHL_1970_politics.txt'))
EVENTS = {first(v, 'id'): v for k, _, v in read('events/COLDWAR_CHL_1970_politics.txt') if k == 'country_event'}
DECISION = first(first(read('common/decisions/COLDWAR_CHL_1970_politics.txt'), P + 'political_transition'), P + 'prepare_military_intervention')


class Country:
    """Only the source subset needed for this transition; reject unknown actions."""
    def __init__(self, slot=1, date='1970.1.1'):
        self.variables = {'ruling_party': slot}
        self.flags = set()
        self.ideas = set()
        self.focuses = set()
        self.leader = 'Eduardo Frei Montalva'
        self.date = date
        self.properties = {'tag': 'CHL', 'exists': 'yes', 'is_dynamic_country': 'no', 'IMP_is_1970_scenario': 'yes',
                           'is_subject': 'no', 'has_civil_war': 'no', 'has_capitulated': 'no'}
        self.owns_santiago = self.controls_santiago = True
        self.elections_allowed = False
        self.queued = []
        self.payments = []
        self.refreshes = 0

    def number(self, value):
        try:
            return float(value)
        except ValueError:
            return self.variables.get(value, 0)

    @staticmethod
    def compare(a, operation, b):
        return {'=': a == b, '>': a > b, '<': a < b, '>=': a >= b, '<=': a <= b}[operation]

    def condition(self, rows):
        def row(k, op, v):
            if k in ('hidden_trigger', 'AND', 'custom_trigger_tooltip'):
                return self.condition([r for r in v if r[0] not in ('tooltip', 'not_tooltip')])
            if k == 'OR':
                return any(row(*r) for r in v)
            if k == 'NOT':
                return not self.condition(v)
            if k in TRIGGERS:
                return self.condition(TRIGGERS[k]) == (v == 'yes')
            if k == 'has_country_flag':
                return v in self.flags
            if k == 'check_variable':
                return all(self.compare(self.number(a), comparison, self.number(b)) for a, comparison, b in v)
            if k == 'has_completed_focus':
                return v in self.focuses
            if k == 'has_country_leader':
                return self.leader == first(v, 'name').strip('"')
            if k == 'owns_state':
                assert v == '468'
                return self.owns_santiago
            if k == 'controls_state':
                assert v == '468'
                return self.controls_santiago
            if k == 'date':
                return self.compare(tuple(map(int, self.date.split('.'))), op, tuple(map(int, v.split('.'))))
            if k in self.properties:
                return self.properties[k] == v
            raise AssertionError('Unsupported source-model predicate ' + k)
        return all(row(*r) for r in rows)

    def eligible(self, trigger):
        return self.condition(TRIGGERS[P + trigger])

    def run(self, rows):
        taken = False
        for k, _, v in rows:
            if k == 'if':
                taken = self.condition(first(v, 'limit', []))
                if taken:
                    self.run([r for r in v if r[0] != 'limit'])
            elif k == 'else_if':
                if not taken and self.condition(first(v, 'limit', [])):
                    self.run([r for r in v if r[0] != 'limit'])
                    taken = True
            elif k == 'else':
                if not taken:
                    self.run(v)
                taken = True
            elif k == 'effect_tooltip' or k in ('name', 'trigger'):
                pass
            elif k == 'hidden_effect':
                self.run(v)
            elif k == 'set_country_flag':
                self.flags.add(first(v, 'flag') if isinstance(v, list) else v)
            elif k == 'clr_country_flag':
                self.flags.discard(v)
            elif k in ('set_variable', 'set_temp_variable'):
                for name, _, value in v:
                    self.variables[name] = self.number(value)
            elif k == 'clear_variable':
                self.variables.pop(v, None)
            elif k == 'change_ruling_party_effect':
                # External native MD setter, inspected at 00_MD_politicsview_scripted_effects.txt:1987.
                self.variables['ruling_party'] = self.variables['rul_party_temp']
                self.elections_allowed = self.variables['disable_elections'] == 0
            elif k == 'update_set_politics':
                pass  # External native outlook synchronization, no reward here.
            elif k == P + 'refresh_programmes':
                self.refreshes += 1  # Core programme rebuilding has separate source checks.
            elif k in EFFECTS:
                self.run(EFFECTS[k])
            elif k in ('add_ideas', 'remove_ideas'):
                (self.ideas.add if k == 'add_ideas' else self.ideas.discard)(v)
            elif k == 'country_event':
                event_id = first(v, 'id')
                self.queued.append(event_id)
                self.run(first(EVENTS[event_id], 'immediate', []))
            elif k == 'modify_treasury_effect':
                self.payments.append(self.variables['treasury_change'])
            elif k == 'kill_country_leader':
                self.leader = None
            elif k == 'create_country_leader':
                self.leader = first(v, 'name').strip('"')
            else:
                raise AssertionError('Unsupported source-model action ' + k)

    def option(self, event_id, option_name):
        return next(v for v in values(EVENTS[event_id], 'option') if first(v, 'name') == P + option_name)

    def choose(self, event_id, option_name):
        option = self.option(event_id, option_name)
        assert self.condition(first(option, 'trigger', [])), option_name
        self.run(option)

    def prepare(self):
        assert self.condition(first(DECISION, 'available'))
        self.run(first(DECISION, 'complete_effect'))
        self.run(first(DECISION, 'remove_effect'))

    def coup(self):
        self.prepare()
        self.choose('COLDWAR_CHL.5', 'event_rupture_option_2')
        self.run(EFFECTS[P + 'trigger_event_junta'])


class MilitaryTransitionTests(unittest.TestCase):
    def test_frei_and_each_civilian_party_can_prepare_without_an_election(self):
        for slot in (0, 1, 2, 3, 4, 5, 14, 18, 19, 20):
            country = Country(slot)
            self.assertFalse(country.elections_allowed)
            self.assertTrue(country.eligible('can_prepare_intervention'), slot)
            self.assertFalse(country.eligible('can_event_rupture'))
        self.assertEqual(first(DECISION, 'cost'), '100')
        self.assertEqual(first(DECISION, 'days_remove'), '90')
        self.assertEqual(first(first(DECISION, 'ai_will_do'), 'base'), '0')

    def test_complete_only_prepares_then_remove_opens_crisis_without_granting_a_coup(self):
        country = Country()
        country.run(first(DECISION, 'complete_effect'))
        self.assertEqual(country.queued, [])
        self.assertEqual(country.leader, 'Eduardo Frei Montalva')
        self.assertFalse(country.eligible('can_prepare_intervention'))
        country.run(first(DECISION, 'remove_effect'))
        self.assertEqual(country.queued, ['COLDWAR_CHL.5'])
        self.assertEqual(country.ideas, set())
        self.assertEqual(country.payments, [])
        country.run(first(DECISION, 'remove_effect'))
        country.run(EFFECTS[P + 'trigger_event_rupture'])
        self.assertEqual(country.queued, ['COLDWAR_CHL.5'])

    def test_takeover_then_pinochet_opens_actual_focus_branch_with_existing_burdens(self):
        country = Country()
        country.coup()
        self.assertEqual(country.variables['ruling_party'], 22)
        self.assertFalse(country.elections_allowed)
        self.assertIn(P + 'repression', country.ideas)
        self.assertIn(P + 'choice_rupture_2', country.ideas)
        self.assertTrue(country.eligible('can_complete_military_staff'))
        self.assertFalse(country.eligible('can_complete_pinochet_command'))
        country.choose('COLDWAR_CHL.6', 'event_junta_option_2')
        self.assertEqual(country.leader, 'Augusto Pinochet')
        country.focuses.add(P + 'military_staff')
        self.assertTrue(country.eligible('can_complete_pinochet_command'))
        self.assertFalse(country.eligible('can_complete_military_constitution'))
        self.assertGreater(country.refreshes, 0)
        self.assertFalse(country.eligible('can_prepare_intervention'))

    def test_collective_council_and_civilian_accord_remain_real_alternatives(self):
        council = Country()
        council.coup()
        council.choose('COLDWAR_CHL.6', 'event_junta_option_1')
        council.focuses.add(P + 'military_staff')
        self.assertEqual(council.leader, 'Chilean Military Council')
        self.assertTrue(council.eligible('can_complete_military_constitution'))
        self.assertFalse(council.eligible('can_complete_pinochet_command'))
        civilian = Country()
        civilian.prepare()
        civilian.choose('COLDWAR_CHL.5', 'event_rupture_option_1')
        self.assertEqual(civilian.leader, 'Eduardo Frei Montalva')
        self.assertEqual(civilian.variables['ruling_party'], 1)
        self.assertNotIn(P + 'repression', civilian.ideas)
        self.assertEqual(civilian.payments, [-.05])
        self.assertTrue(civilian.eligible('civilian_calendar_active'))
        self.assertFalse(civilian.eligible('can_prepare_intervention'))

    def test_cancellation_and_context_changes_cannot_complete_or_grant_rewards(self):
        for property_name in ('is_subject', 'has_civil_war', 'has_capitulated', 'santiago', 'government'):
            country = Country()
            country.run(first(DECISION, 'complete_effect'))
            if property_name == 'santiago':
                country.controls_santiago = False
            elif property_name == 'government':
                country.variables['ruling_party'] = 22
            else:
                country.properties[property_name] = 'yes'
            self.assertTrue(country.condition(first(DECISION, 'cancel_trigger')), property_name)
            country.run(first(DECISION, 'cancel_effect'))
            country.run(first(DECISION, 'remove_effect'))
            self.assertEqual(country.queued, [])
            self.assertEqual(country.ideas, set())

    def test_early_coup_supersedes_counted_and_ratified_ballots_and_stale_popups(self):
        country = Country(date='1970.10.25')
        country.flags.update((P + 'election_ballot_counted', P + 'election_ratified'))
        country.variables[P + 'election_confirmed_slot'] = 18
        country.coup()
        country.choose('COLDWAR_CHL.6', 'event_junta_option_2')
        country.date = '1970.11.4'
        country.run(EFFECTS[P + 'install_confirmed_candidate'])
        country.run(EFFECTS[P + 'election_count'])
        self.assertEqual(country.leader, 'Augusto Pinochet')
        self.assertEqual(country.variables['ruling_party'], 22)
        self.assertFalse(country.eligible('can_event_election'))
        self.assertFalse(country.eligible('can_event_congress'))
        for event in ('COLDWAR_CHL.1', 'COLDWAR_CHL.2', 'COLDWAR_CHL.5', 'COLDWAR_CHL.6'):
            live = [option for option in values(EVENTS[event], 'option') if country.condition(first(option, 'trigger', []))]
            self.assertEqual([first(option, 'name') for option in live], [P + 'event_political_context_changed'])
        # Returning to civilian office cannot revive an already superseded 1970 mandate.
        country.variables['ruling_party'] = 1
        country.flags.discard(P + 'military_government')
        self.assertFalse(country.eligible('civilian_calendar_active'))

    def test_historical_crisis_still_works_but_is_not_required_for_new_route(self):
        country = Country(18, '1973.9.11')
        country.flags.update(P + name for name in ('constitutional_crisis', 'high_confrontation', 'military_intervention_condition'))
        self.assertTrue(country.eligible('can_event_rupture'))
        country.flags.clear()
        self.assertFalse(country.eligible('can_event_rupture'))
        country.flags.add(P + 'intervention_prepared')
        country.date = '1975.1.1'
        country.variables['ruling_party'] = 1
        self.assertTrue(country.eligible('can_event_rupture'))

    def test_historical_trigger_does_not_skip_active_ninety_day_preparation(self):
        country = Country(18, '1973.9.11')
        country.flags.update(P + name for name in ('constitutional_crisis', 'high_confrontation', 'military_intervention_condition'))
        country.run(first(DECISION, 'complete_effect'))
        self.assertFalse(country.eligible('can_event_rupture'))
        country.run(EFFECTS[P + 'trigger_event_rupture'])
        self.assertEqual(country.queued, [])
        country.run(first(DECISION, 'remove_effect'))
        self.assertEqual(country.queued, ['COLDWAR_CHL.5'])

    def test_stale_crisis_dismissal_allows_a_paid_retry_after_context_recovers(self):
        country = Country()
        country.prepare()
        country.controls_santiago = False
        country.choose('COLDWAR_CHL.5', 'event_political_context_changed')
        self.assertEqual(country.ideas, set())
        self.assertEqual(country.payments, [])
        country.controls_santiago = True
        self.assertTrue(country.eligible('can_prepare_intervention'))
        country.coup()
        country.choose('COLDWAR_CHL.6', 'event_junta_option_2')
        self.assertEqual(country.leader, 'Augusto Pinochet')

    def test_stale_campaign_or_congress_options_cannot_execute_after_takeover(self):
        country = Country()
        country.coup()
        country.choose('COLDWAR_CHL.6', 'event_junta_option_2')
        before = country.flags.copy(), country.ideas.copy(), country.payments.copy()
        for event, name in (('COLDWAR_CHL.1', 'event_election_option_1'), ('COLDWAR_CHL.2', 'event_congress_option_1')):
            country.run(country.option(event, name))
        self.assertEqual((country.flags, country.ideas, country.payments), before)
        self.assertEqual(country.leader, 'Augusto Pinochet')


if __name__ == '__main__':
    unittest.main()
