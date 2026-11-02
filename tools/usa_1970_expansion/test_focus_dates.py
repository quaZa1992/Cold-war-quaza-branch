# IMPERIA COLD WAR — Focused USA calendar-lock transformation checks.
"""Read-only tests: no compiler, runtime writes or game process is invoked."""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import focus_dates as d


def focuses(text):
    tree = next(n for n in d.nodes(text) if n.key == 'focus_tree')
    return {d.field(n.children(), 'id'): n for n in tree.children() if n.key == 'focus'}


def raw(text, node):
    return text[node.start:node.end]


def evaluate(rows, *, now='1970.1.1', flags=frozenset(), party=1,
             completed=frozenset(), congress=False, doctrines=frozenset()):
    def one(n):
        if n.key in {'tooltip'}:
            return True
        if n.key in {'available', 'AND', 'hidden_trigger', 'custom_trigger_tooltip'}:
            return all(one(c) for c in n.children())
        if n.key == 'OR':
            return any(one(c) for c in n.children())
        if n.key == 'NOT':
            return not all(one(c) for c in n.children())
        if n.key == 'always':
            return n.value == 'yes'
        if n.key == 'date':
            a = date(*map(int, now.split('.')))
            b = date(*map(int, str(n.value).split('.')))
            return {'<': a < b, '>': a > b, '<=': a <= b, '>=': a >= b, '=': a == b}[n.op]
        if n.key == 'has_country_flag':
            return n.value in flags
        if n.key == 'has_completed_focus':
            return n.value in completed
        if n.key == 'western_conservatism_are_in_power':
            return party == 1
        if n.key == 'western_liberals_are_in_power':
            return party == 2
        if n.key == 'has_variable':
            return n.value == 'ruling_party'
        if n.key == 'check_variable':
            return party == int(d.field(n.children(), 'ruling_party'))
        if n.key == 'congress_high_support_trigger':
            return congress
        if n.key == 'has_doctrine':
            return n.value in doctrines
        if n.key in {'tag', 'original_tag'}:
            return n.value == 'USA'
        if n.key == 'IMP_is_1970_scenario':
            return n.value == 'yes'
        raise AssertionError(('Unsupported focused model predicate', n.key))
    return all(one(n) for n in rows)


class FocusDatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = (d.ROOT / d.TREE_PATH).read_text(encoding='utf-8-sig')
        cls.after = d.patch_focus_tree(cls.tree)
        cls.before_nodes = focuses(cls.tree)
        cls.after_nodes = focuses(cls.after)

    def test_all_301_availability_and_historical_receipts(self):
        self.assertEqual(len(self.before_nodes), 301)
        self.assertEqual(set(self.before_nodes), set(self.after_nodes))
        for fid, focus in self.after_nodes.items():
            if fid in d.ELECTION_RECEIPTS:
                self.assertEqual(raw(self.tree, self.before_nodes[fid]), raw(self.after, focus))
                self.assertTrue(any(n.key == 'date' for n in d.walk(focus.children())))
            else:
                available = next((n for n in focus.children() if n.key == 'available'), None)
                self.assertFalse(any(n.key == 'date' for n in d.walk(available.children() if available else [])), fid)

    def test_costs_coordinates_rewards_choices_and_policy_links_unchanged(self):
        for fid, original in self.before_nodes.items():
            changed = self.after_nodes[fid]
            a = [n for n in original.children() if n.key not in {'available', 'prerequisite'}]
            b = [n for n in changed.children() if n.key not in {'available', 'prerequisite'}]
            self.assertEqual(d._shape(a), d._shape(b), fid)
            wanted = []
            for p in original.children():
                if p.key != 'prerequisite':
                    continue
                refs = [c.value for c in p.children() if c.key == 'focus']
                if not refs or not all(ref in d.ELECTION_RECEIPTS for ref in refs):
                    wanted.append(p)
                else:
                    available = next(n for n in changed.children() if n.key == 'available')
                    self.assertIn(d.party_gate(fid), {n.key for n in d.walk(available.children())})
            self.assertEqual(d._shape(wanted), d._shape([n for n in changed.children() if n.key == 'prerequisite']), fid)

    def test_reform_under_fire_available_in_1970(self):
        # Keep the dated regression input after the coordinator has installed
        # the fix. The immutable source is read, never rewritten.
        snapshot = json.loads((Path(__file__).resolve().parent / 'source_snapshot.json').read_text(encoding='utf-8'))
        baseline = focuses(snapshot['files'][d.TREE_PATH]['text'])
        original = next(n for n in baseline['USA_1970_D0'].children() if n.key == 'available')
        changed = next(n for n in self.after_nodes['USA_1970_D0'].children() if n.key == 'available')
        self.assertFalse(evaluate([original]))
        self.assertTrue(evaluate([changed]))

    def test_nixon_retains_actual_presidency_without_first_term_expiry(self):
        changed = next(n for n in self.after_nodes['USA_1970_NIX_F1'].children() if n.key == 'available')
        for now in ['1970.1.1', '1973.1.21', '1976.1.1']:
            self.assertTrue(evaluate([changed], now=now, flags={'USA_1970_nixon_presidency'}))
            self.assertFalse(evaluate([changed], now=now))

    def test_pentagon_papers_retains_real_publication_state(self):
        changed = next(n for n in self.after_nodes['USA_1970_NIX_A5'].children() if n.key == 'available')
        self.assertFalse(evaluate([changed], flags={'USA_1970_nixon_presidency'}))
        self.assertTrue(evaluate([changed], flags={'USA_1970_nixon_presidency', 'USA_1970_pentagon_papers_published'}))

    def test_force_law_and_congress_still_gate_in_1970(self):
        available = next(n for n in self.after_nodes['USA_1970_D2'].children() if n.key == 'available')
        self.assertFalse(evaluate([available], congress=False))
        self.assertTrue(evaluate([available], congress=True))
        self.assertFalse(evaluate([available], congress=True, doctrines={'mdcw_all_volunteer_force'}))
        self.assertFalse(evaluate([available], congress=True, flags={'USA_1970_force_model_selected'}))

    def test_party_programmes_available_without_fabricated_election(self):
        fid = 'USA_1970_1972_rep_1_a_strategy_of_leverage_in_vietnam'
        f = self.after_nodes[fid]
        self.assertFalse(any(p.key == 'prerequisite' for p in f.children()))
        available = next(n for n in f.children() if n.key == 'available')
        self.assertTrue(evaluate([available], party=1, completed=frozenset()))
        self.assertFalse(evaluate([available], party=2, completed=frozenset()))
        for fid in d.ELECTION_RECEIPTS:
            bypass = next(n for n in self.after_nodes[fid].children() if n.key == 'bypass')
            self.assertFalse(evaluate(bypass.children(), party=1))
            self.assertFalse(evaluate(bypass.children(), party=2))

    def test_real_execution_and_retry_helpers_have_no_dates(self):
        for path in d.TRIGGER_PATHS:
            text = (d.ROOT / path).read_text(encoding='utf-8-sig')
            after = d.patch_ready_triggers(text)
            original = {n.key: n for n in d.nodes(text)}
            for n in d.nodes(after):
                if n.key.startswith(d.READY_PREFIXES):
                    self.assertFalse(any(c.key == 'date' for c in d.walk(n.children())), n.key)
                    self.assertEqual(d._shape(d.nodes(d.strip_condition_dates(raw(text, original[n.key]), detach_election_receipts=True))), d._shape([n]))
                else:
                    self.assertEqual(raw(text, original[n.key]), raw(after, n))

    def test_pending_application_checks_preserve_party_and_receipt_guard(self):
        body = ('tag = USA IMP_is_1970_scenario = yes date > 1973.1.20 '
                'western_conservatism_are_in_power = yes '
                'has_country_flag = pending NOT = { has_country_flag = done } '
                'OR = { has_completed_focus = USA_1970_1972_republican_victory }')
        changed = d.patch_trigger_bodies({'COLDWAR_USA_legacy_ready_test': body})['COLDWAR_USA_legacy_ready_test']
        self.assertTrue(evaluate(d.nodes(changed), flags={'pending'}, party=1))
        self.assertFalse(evaluate(d.nodes(changed), flags={'pending'}, party=2))
        self.assertFalse(evaluate(d.nodes(changed), flags={'pending', 'done'}, party=1))

    def test_empty_groups_and_tooltip_metadata_are_removed(self):
        body = 'AND = { date > 1972.1.1 } OR = { date > 1972.1.1 } NOT = { date < 1973.1.1 } custom_trigger_tooltip = { tooltip = old date > 1972.1.1 }'
        self.assertEqual(d.strip_condition_dates(body), '')
        body = 'OR = { has_country_flag = published date > 1972.1.1 }'
        self.assertEqual(d.strip_condition_dates(body), 'OR = { has_country_flag = published }')

    def test_mixed_receipt_policy_prerequisite_requires_explicit_review(self):
        synthetic = ('focus_tree = { id = USA_1970_focus focus = { id = USA_1970_1972_rep_test cost = 4 '
                     'prerequisite = { focus = USA_1970_1972_republican_victory focus = actual_policy } } }')
        with self.assertRaises(AssertionError):
            d.patch_focus_tree(synthetic)

    def test_all_hooks_are_pure_idempotent_and_preserve_event_chronology(self):
        inputs = {d.TREE_PATH: self.tree, **{p: (d.ROOT / p).read_text(encoding='utf-8-sig') for p in d.TRIGGER_PATHS}}
        inputs[d.LOCALE_PATH] = (d.ROOT / d.LOCALE_PATH).read_text(encoding='utf-8-sig')
        for path in ['common/scripted_effects/USA_1970_scripted_effects.txt', 'events/USA_1970_nixon_events.txt', 'events/USA_1970_events.txt']:
            inputs[path] = (d.ROOT / path).read_text(encoding='utf-8-sig')
        with patch.object(Path, 'write_text', side_effect=AssertionError('Unexpected file write')), patch.object(Path, 'write_bytes', side_effect=AssertionError('Unexpected file write')):
            result = d.patch_outputs(inputs)
            self.assertEqual(result, d.patch_outputs(result))
        for path in inputs:
            if path not in {d.TREE_PATH, d.LOCALE_PATH} | d.TRIGGER_PATHS:
                self.assertEqual(inputs[path], result[path])
        self.assertIn('Nixon is President.', result[d.LOCALE_PATH])
        self.assertNotIn('opening administration programme has not ended', result[d.LOCALE_PATH])
        self.assertTrue(result[d.LOCALE_PATH].startswith('l_english:'))


if __name__ == '__main__':
    unittest.main()
