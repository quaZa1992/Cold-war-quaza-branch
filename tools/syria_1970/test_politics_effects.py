"""Small counterexamples for the native-politics source contract, not HOI4."""
from copy import deepcopy
import unittest

from validate_content import first, parse
from validate_politics_effects import country_context, pact_errors, politics_errors

GROUPS = {'democratic', 'communism', 'fascism', 'neutrality', 'nationalist'}
PACT = '''
pact = {
    set_country_flag = COLDWAR_SYR_national_pact
    clr_country_flag = COLDWAR_SYR_pact_rejected
    set_variable = { disable_elections = 0 }
    set_country_flag = no_leader_change
    set_politics = { ruling_party = ROOT elections_allowed = yes election_frequency = 48 }
    clr_country_flag = no_leader_change
    set_variable = { party_banned_array^7 = 0 }
    update_set_politics = yes
}
'''


class NativePoliticsContract(unittest.TestCase):
    def politics(self, text, **context):
        return politics_errors(first(parse('set_politics = ' + text), 'set_politics'), GROUPS,
                               country_effect_scope=context.pop('country_effect_scope', True), **context)

    def test_native_group_literals_are_accepted(self):
        for group in sorted(GROUPS):
            with self.subTest(group=group):
                self.assertEqual(self.politics('{ ruling_party = ' + group + ' elections_allowed = no }'), [])

    def test_old_incomplete_election_effect_is_rejected(self):
        old = '{ elections_allowed = yes election_frequency = 48 }'
        self.assertIn('set_politics requires exactly one ruling_party', self.politics(old))

    def test_md_slot_and_subideology_are_not_native_groups(self):
        for invalid in ('7', 'ruling_party', 'Autocracy', 'communist_state'):
            with self.subTest(invalid=invalid):
                self.assertTrue(self.politics('{ ruling_party = ' + invalid + ' }'))

    def test_country_references_require_explicit_context(self):
        for scope in ('ROOT', 'THIS', 'FROM', 'PREV'):
            with self.subTest(scope=scope):
                effect = '{ ruling_party = ' + scope + ' }'
                self.assertTrue(self.politics(effect))
                self.assertEqual(self.politics(effect, known_country_scopes={scope}), [])

    def test_argument_shape_duplicates_and_wrong_current_scope_are_rejected(self):
        self.assertTrue(self.politics('yes'))
        self.assertTrue(self.politics('{ ruling_party = ROOT ruling_party = communism }',
                                      known_country_scopes={'ROOT'}))
        self.assertTrue(self.politics('{ ruling_party = communism }', country_effect_scope=False))
        self.assertTrue(country_context(('if', 'hidden_effect')))
        self.assertFalse(country_context(('if', 'every_owned_state')))
        self.assertFalse(country_context(('if', '587')))

    def test_native_preserving_pact_with_four_year_elections_passes(self):
        body = first(parse(PACT), 'pact')
        self.assertEqual(pact_errors(body), [])
        self.assertEqual(politics_errors(first(body, 'set_politics'), GROUPS,
                                         country_effect_scope=True, known_country_scopes={'ROOT'}), [])

    def test_election_guard_must_precede_call_and_be_cleared(self):
        body = first(parse(PACT), 'pact')
        for mutation in ('missing_guard', 'late_guard', 'missing_cleanup'):
            changed = deepcopy(body)
            guard = ('set_country_flag', '=', 'no_leader_change')
            cleanup = ('clr_country_flag', '=', 'no_leader_change')
            if mutation == 'missing_guard':
                changed.remove(guard)
            elif mutation == 'late_guard':
                changed.remove(guard)
                changed.append(guard)
            else:
                changed.remove(cleanup)
            with self.subTest(mutation=mutation):
                self.assertTrue(pact_errors(changed))

    def test_pact_preserves_outlook_md_slot_and_incumbent(self):
        variants = {
            'forced_outlook': PACT.replace('ruling_party = ROOT', 'ruling_party = communism'),
            'wrong_frequency': PACT.replace('election_frequency = 48', 'election_frequency = 60'),
            'elections_disabled': PACT.replace('elections_allowed = yes', 'elections_allowed = no'),
            'forced_slot': PACT.replace('update_set_politics = yes', 'set_variable = { ruling_party = 7 }'),
            'removed_incumbent': PACT.replace('update_set_politics = yes', 'retire_country_leader = yes'),
        }
        for name, text in variants.items():
            with self.subTest(name=name):
                self.assertTrue(pact_errors(first(parse(text), 'pact')))


if __name__ == '__main__':
    unittest.main()
