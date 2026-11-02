# IMPERIA COLD WAR — Execute GC session seats and native UN lifecycle integration
"""Bounded source interpreter. Does not emulate HOI4 UI, saves or MP netcode."""
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/colonial_affairs'))
from test_runtime import Model, Scope, parse, first

D = Decimal
SEATS = ('europe', 'americas', 'africa', 'middle_east', 'asia')
PREFIX = 'COLDWAR_gc_un_'
FLAG = PREFIX + 'session_seats'
NATIVE = 'common/scripted_effects/01_international_systems_effects.txt'
FILES = ('common/decisions/COLDWAR_gc_unsc.txt',
         'common/scripted_effects/COLDWAR_gc_unsc.txt',
         'common/scripted_triggers/COLDWAR_gc_unsc.txt',
         'common/scripted_localisation/COLDWAR_gc_unsc.txt')


def load(path):
    return parse((ROOT / path).read_text(encoding='utf-8-sig'))


def expand(rows, arguments):
    def sub(text):
        for key, value in arguments.items():
            text = text.replace('$' + key + '$', value)
        if '$' in text:
            raise ValueError('Unexpanded parameter: ' + text)
        return text
    return [(sub(k), op, expand(v, arguments) if isinstance(v, list) else sub(v))
            for k, op, v in rows]


class Machine(Model):
    def __init__(self):
        self.effects = dict((k, v) for path in (NATIVE, FILES[1]) for k, _, v in load(path))
        self.triggers = dict((k, v) for path in ('common/scripted_triggers/01_international_triggers.txt', FILES[2])
                             for k, _, v in load(path))
        tags = 'LUX TAI FRA SOV USA ENG COL FIN NEP SPR ZAM BRD NIC POL SIE SYR ARG BEL GHA IRQ JAP SWI'
        self.c = {tag: Scope(tag) for tag in tags.split()}
        self.ids = {tag: D(i + 1) for i, tag in enumerate(self.c)}
        self.by_id = {self.ids[tag]: country for tag, country in self.c.items()}
        self.s = {}
        self.g = Scope('global', 'global')
        self.root = self.c['LUX']
        self.root.ideas.add('imp_gc_nation')
        self.scenario = True
        self.date = '1972.1.1'
        self.api_calls = []
        self.events = []
        self.random_calls = 0
        self.saved_targets = {}
        self.decisions = dict((k, v) for k, _, v in first(load(FILES[0]), 'imp_gc_tools_decisions'))
        self.p5 = first(first(first(load('common/ideas/Organizations.txt'), 'ideas'), 'country'), 'p5_member')
        self.permanent = [self.ids[tag] for tag in 'TAI FRA SOV USA ENG'.split()]
        self.original_elected = [self.ids[tag] for tag in 'COL FIN NEP SPR ZAM BRD NIC POL SIE SYR'.split()]
        self.g.vars.update(UN_general_assembly=list(self.by_id), p5_sc_members=self.permanent.copy(),
                           security_council_members=self.original_elected + self.permanent,
                           ga_vote_type_tracker=[], ga_vote_nation_tracker=[])
        for tag in 'TAI FRA SOV USA ENG'.split():
            self.c[tag].ideas.add('p5_member')
        self.c['SWI'].modifiers.clear()
        self.g.vars['UN_general_assembly'].remove(self.ids['SWI'])

    def scope(self, name, current, root, prev):
        if name.startswith('var:'):
            return self.by_id.get(self.value(name[4:], current, root, prev))
        return super().scope(name, current, root, prev)

    def value(self, name, current, root, prev):
        if isinstance(name, D):
            return name
        if name in ('THIS', 'ROOT', 'PREV'):
            target = self.scope(name, current, root, prev)
            return self.ids[target.id] if target else D(0)
        if name.endswith('.id'):
            return self.value(name[:-3], current, root, prev)
        if name in self.ids:
            return self.ids[name]
        if '^' in name:
            base, index = name.rsplit('^', 1)
            obj, key = self.variable(base, current, root, prev)
            values = obj.vars.get(key, [])
            if index == 'num':
                return D(len(values))
            offset = int(self.value(index, current, root, prev))
            if not 0 <= offset < len(values):
                raise ValueError('Out-of-range array read: ' + name)
            return values[offset]
        return super().value(name, current, root, prev)

    def condition(self, rows, current, root=None, prev=None):
        root = root or current
        for k, op, v in rows:
            if k == 'is_in_array':
                obj, key = self.variable(v[0][0], current, root, prev)
                ok = self.value(v[0][2], current, root, prev) in obj.vars.get(key, [])
            elif k == 'has_variable':
                obj, key = self.variable(v, current, root, prev)
                ok = key in obj.vars
            elif k == 'exists':
                ok = (current is not None and '_dead' not in current.flags) == (v == 'yes')
            elif k == 'has_capitulated':
                ok = ('_capitulated' in current.flags) == (v == 'yes')
            else:
                ok = super().condition([(k, op, v)], current, root, prev)
            if not ok:
                return False
        return True

    def execute(self, rows, current, root, prev):
        last_if = None
        for k, op, v in rows:
            if k in self.effects:
                args = dict((key, value) for key, _, value in v) if isinstance(v, list) else {}
                self.execute(expand(self.effects[k], args), current, root, prev)
            elif k == 'if':
                last_if = self.condition(first(v, 'limit', []), current, root, prev)
                if last_if:
                    self.execute([row for row in v if row[0] != 'limit'], current, root, prev)
            elif k == 'else_if':
                if last_if is False:
                    last_if = self.condition(first(v, 'limit', []), current, root, prev)
                    if last_if:
                        self.execute([row for row in v if row[0] != 'limit'], current, root, prev)
            elif k == 'else':
                if last_if is False:
                    self.execute(v, current, root, prev)
                last_if = None
            elif k == 'for_each_loop':
                obj, key = self.variable(first(v, 'array'), current, root, prev)
                for i, number in enumerate(obj.vars.get(key, []).copy()):
                    current.vars[first(v, 'value', 'v')] = number
                    current.vars[first(v, 'index', 'i')] = D(i)
                    self.execute([row for row in v if row[0] not in ('array', 'value', 'index')], current, root, prev)
            elif k == 'for_loop_effect':
                for _ in range(int(self.value(first(v, 'end'), current, root, prev))):
                    self.execute([row for row in v if row[0] != 'end'], current, root, prev)
            elif k == 'random_scope_in_array':
                self.random_calls += 1
                obj, key = self.variable(first(v, 'array'), current, root, prev)
                for number in obj.vars.get(key, []):
                    target = self.by_id[number]
                    if self.condition(first(v, 'limit', []), target, root, current):
                        self.execute([row for row in v if row[0] not in ('array', 'limit')], target, root, current)
                        break
            elif k in ('add_to_array', 'remove_from_array'):
                obj, key = self.variable(v[0][0], current, root, prev)
                number = self.value(v[0][2], current, root, prev)
                values = obj.vars.setdefault(key, [])
                if k == 'add_to_array':
                    values.append(number)
                else:
                    values[:] = [item for item in values if item != number]
            elif k == 'clear_array':
                obj, key = self.variable(v, current, root, prev)
                obj.vars[key] = []
            elif k in ('set_global_flag', 'clr_global_flag'):
                flag = first(v, 'flag') if isinstance(v, list) else v
                self.g.flags.add(flag) if k == 'set_global_flag' else self.g.flags.discard(flag)
            elif k in ('add_ideas', 'remove_ideas'):
                changed = (v in current.ideas) != (k == 'add_ideas')
                current.ideas.add(v) if k == 'add_ideas' else current.ideas.discard(v)
                if v == 'p5_member' and changed:
                    self.execute(first(self.p5, 'on_add' if k == 'add_ideas' else 'on_remove'), current, root, prev)
            elif k in ('set_variable', 'set_temp_variable') and '^' in v[0][0]:
                base, index = v[0][0].rsplit('^', 1)
                obj, key = self.variable(base, current, root, prev)
                offset = int(self.value(index, current, root, prev))
                obj.vars[key][offset] = self.value(v[0][2], current, root, prev)
            elif k in ('set_variable', 'set_temp_variable') and isinstance(v[0][2], list):
                obj, key = self.variable(v[0][0], current, root, prev)
                formula = v[0][2]
                number = self.value(first(formula, 'value'), current, root, prev)
                number *= D(first(formula, 'multiply', '1'))
                number += D(first(formula, 'add', '0'))
                if first(formula, 'round') == 'yes':
                    number = number.quantize(D(1), rounding=ROUND_HALF_UP)
                obj.vars[key] = number
            elif k in ('COLDWAR_Germany_un_status_changed', 'revoke_un_esco_subsidies',
                       'revoke_un_ido_subsidies', 'revoke_un_cdf_subsidies', 'activate_mission',
                       'unlock_decision_tooltip'):
                self.api_calls.append(k)
            elif k in ('country_event', 'news_event'):
                self.events.append((k, v, current.id))
            else:
                super().execute([(k, op, v)], current, root, prev)

    def decision(self, suffix, check=True):
        body = self.decisions[PREFIX + suffix]
        if check:
            assert self.condition(first(body, 'visible', []), self.root)
            assert self.condition(first(body, 'available', []), self.root)
        self.execute(first(body, 'complete_effect'), self.root, self.root, None)

    def ready(self):
        self.decision('expand')
        self.decision('enable')
        return self

    def assign(self, seat, tag, check=True):
        self.root.vars['gc_tool_target_country'] = self.ids[tag]
        self.decision('assign_' + seat, check)


class SessionSeats(unittest.TestCase):
    def test_activation_replaces_ten_elected_seats_and_preserves_permanent_members(self):
        m = Machine().ready()
        self.assertEqual(m.g.vars['security_council_members'], m.permanent)
        self.assertEqual(m.g.vars['p5_sc_members'], m.permanent)
        self.assertTrue(all('p5_member' in m.by_id[n].ideas for n in m.permanent))
        self.assertEqual(m.g.vars['un_sc_required_yes'], 3)
        m.assign(SEATS[0], 'ARG')
        m.decision('enable', check=False)
        self.assertEqual(m.g.vars[PREFIX + 'seat_' + SEATS[0]], m.ids['ARG'])

    def test_all_five_seats_grant_actual_voting_rights_and_replacement_revokes_old_member(self):
        m = Machine().ready()
        for seat, tag in zip(SEATS, ('ARG', 'BEL', 'GHA', 'IRQ', 'JAP')):
            m.assign(seat, tag)
            self.assertTrue(m.condition([('is_on_un_sec_council', '=', 'yes')], m.c[tag]))
        self.assertEqual(len(m.g.vars['security_council_members']), 10)
        self.assertEqual(m.g.vars['un_sc_required_yes'], 6)
        m.assign('africa', 'COL')
        self.assertNotIn(m.ids['GHA'], m.g.vars['security_council_members'])
        self.assertIn(m.ids['GHA'], m.g.vars['UN_general_assembly'])
        self.assertEqual(m.g.vars[PREFIX + 'seat_africa'], m.ids['COL'])
        self.assertEqual(m.random_calls, 0)

    # IMPERIA COLD WAR — Europe and Americas have independent GC mandates.
    def test_europe_and_americas_can_be_replaced_and_vacated_independently(self):
        m = Machine().ready()
        m.assign('europe', 'BEL')
        m.assign('americas', 'ARG')
        m.assign('europe', 'FIN')
        self.assertEqual(m.g.vars[PREFIX + 'seat_europe'], m.ids['FIN'])
        self.assertEqual(m.g.vars[PREFIX + 'seat_americas'], m.ids['ARG'])
        self.assertNotIn(m.ids['BEL'], m.g.vars['security_council_members'])
        m.decision('clear_europe')
        self.assertNotIn(PREFIX + 'seat_europe', m.g.vars)
        self.assertEqual(m.g.vars['security_council_members'], [m.ids['ARG']] + m.permanent)
        m.assign('europe', 'BEL')
        m.decision('clear_americas')
        self.assertEqual(m.g.vars['security_council_members'], [m.ids['BEL']] + m.permanent)

    def test_vacancies_have_no_zero_or_duplicate_flags_and_can_be_filled_again(self):
        m = Machine().ready()
        for seat, tag in zip(SEATS, ('ARG', 'BEL', 'GHA', 'IRQ', 'JAP')):
            m.assign(seat, tag)
        for seat in SEATS:
            m.decision('clear_' + seat)
        self.assertEqual(m.g.vars['security_council_members'], m.permanent)
        self.assertFalse(any(PREFIX + 'seat_' + seat in m.g.vars for seat in SEATS))
        m.assign('asia', 'ARG')
        self.assertNotIn(D(0), m.g.vars['security_council_members'])
        self.assertEqual(len(set(m.g.vars['security_council_members'])), 6)

    def test_authority_is_enforced_inside_effects_even_for_stale_decisions(self):
        for ai, gc in ((True, True), (False, False), (True, False)):
            m = Machine().ready()
            m.assign('asia', 'JAP')
            m.root.ai = ai
            m.root.ideas = {'imp_gc_nation'} if gc else set()
            before = deepcopy(m.g.vars)
            for suffix in ('enable', 'assign_africa', 'clear_asia'):
                m.root.vars['gc_tool_target_country'] = m.ids['GHA']
                m.decision(suffix, check=False)
            self.assertEqual(m.g.vars, before)
            self.assertTrue(all(not m.condition(first(body, 'visible', []), m.root)
                                for body in m.decisions.values()))

    def test_live_votes_block_activation_and_edits_without_changing_ballots(self):
        for live, vote_type in (('current_ongoing_sc_vote', 2), ('current_ongoing_ga_vote', 6)):
            m = Machine()
            m.g.flags.add(live)
            m.g.vars['current_ga_vote_type'] = D(vote_type)
            m.decision('enable', check=False)
            self.assertNotIn(FLAG, m.g.flags)
            m.g.flags.discard(live)
            m.ready()
            m.assign('asia', 'JAP')
            m.g.flags.add(live)
            m.g.vars['security_council_vote_yes'] = [m.ids['JAP']]
            before = deepcopy(m.g.vars)
            m.assign('asia', 'ARG', check=False)
            m.decision('clear_asia', check=False)
            self.assertEqual(m.g.vars, before)

    def test_other_general_assembly_business_does_not_block_session_edits(self):
        m = Machine().ready()
        m.g.flags.add('current_ongoing_ga_vote')
        m.g.vars['current_ga_vote_type'] = D(5)
        m.assign('africa', 'GHA')
        self.assertEqual(m.g.vars['current_ga_vote_type'], 5)
        self.assertIn('current_ongoing_ga_vote', m.g.flags)

    def test_invalid_targets_and_duplicate_seats_are_rejected_at_execution(self):
        for invalid in ('permanent', 'dead', 'unrecognised', 'nonstate', 'capitulated', 'nonmember', 'unset', 'duplicate'):
            m = Machine().ready()
            m.assign('africa', 'GHA')
            m.root.vars['gc_tool_target_country'] = m.ids['ARG']
            if invalid == 'permanent':
                m.root.vars['gc_tool_target_country'] = m.ids['TAI']
            elif invalid == 'nonmember':
                m.root.vars['gc_tool_target_country'] = m.ids['SWI']
            elif invalid == 'unset':
                del m.root.vars['gc_tool_target_country']
            elif invalid == 'duplicate':
                m.root.vars['gc_tool_target_country'] = m.ids['GHA']
            elif invalid in ('dead', 'capitulated'):
                m.c['ARG'].flags.add('_' + invalid)
            else:
                m.c['ARG'].ideas.add('lacks_international_recognition' if invalid == 'unrecognised' else 'non_state_actor')
            before = deepcopy(m.g.vars)
            self.assertFalse(m.condition(m.triggers[PREFIX + 'valid_target'], m.root), invalid)
            m.decision('assign_asia', check=False)
            self.assertEqual(m.g.vars, before, invalid)

    def test_activation_purges_only_election_queue_entries_in_parallel(self):
        m = Machine()
        m.g.flags.add('electing_new_unsc_members')
        m.g.vars.update(ga_vote_type_tracker=list(map(D, (5, 6, 22, 6, 3))),
                        ga_vote_nation_tracker=[m.ids[t] for t in ('ARG', 'GHA', 'JAP', 'IRQ', 'BEL')],
                        confirmed_new_council_members=[m.ids['GHA']], new_council_members=[m.ids['IRQ']])
        m.ready()
        self.assertEqual(m.g.vars['ga_vote_type_tracker'], [5, 22, 3])
        self.assertEqual(m.g.vars['ga_vote_nation_tracker'], [m.ids[t] for t in ('ARG', 'JAP', 'BEL')])
        self.assertNotIn('electing_new_unsc_members', m.g.flags)
        self.assertEqual(m.g.vars['new_council_members'], [])
        self.assertEqual(m.g.vars['confirmed_new_council_members'], [])

    def test_native_rotation_election_and_late_callbacks_are_inert_in_rp_mode(self):
        m = Machine().ready()
        m.assign('africa', 'GHA')
        before = deepcopy(m.g.vars)
        for effect in ('start_unsc_next_term_voting', 'update_security_council_peeps',
                       'un_sc_new_members_step_next', 'un_sc_new_members_re_roll'):
            m.run(effect)
            self.assertEqual(m.g.vars, before, effect)
        m.root.vars['ga_new_vote_type'] = D(6)
        m.root.vars['ga_new_vote_nation'] = m.ids['JAP']
        m.run('update_ga_vote')
        self.assertEqual(m.g.vars, before)
        self.assertEqual(m.random_calls, 0)

    def test_calendar_rotation_remains_available_outside_rp_mode(self):
        m = Machine()
        new = [m.ids[t] for t in ('ARG', 'BEL', 'GHA', 'IRQ', 'JAP')]
        m.g.vars['confirmed_new_council_members'] = new.copy()
        m.run('update_security_council_peeps')
        self.assertEqual(m.g.vars['security_council_members'], m.original_elected[5:] + new + m.permanent)

    def test_native_membership_loss_vacates_only_its_rp_seat_and_removes_vote(self):
        m = Machine().ready()
        m.assign('africa', 'GHA')
        m.assign('asia', 'JAP')
        m.g.flags.add('current_ongoing_sc_vote')
        m.g.vars['security_council_vote_yes'] = [m.ids['GHA'], m.ids['JAP']]
        m.run('clear_united_nations_member_state', m.c['GHA'])
        self.assertNotIn(PREFIX + 'seat_africa', m.g.vars)
        self.assertEqual(m.g.vars['security_council_vote_yes'], [m.ids['JAP']])
        self.assertEqual(m.g.vars['security_council_members'], [m.ids['JAP']] + m.permanent)
        self.assertNotIn(m.ids['GHA'], m.g.vars['UN_general_assembly'])
        self.assertEqual(m.random_calls, 0)

    def test_native_permanent_admission_does_not_randomly_fill_the_freed_rp_seat(self):
        m = Machine().ready()
        m.assign('asia', 'JAP')
        m.run('unsc_promote_permanent_member', m.c['JAP'])
        self.assertIn('p5_member', m.c['JAP'].ideas)
        self.assertNotIn(PREFIX + 'seat_asia', m.g.vars)
        self.assertEqual(m.g.vars['security_council_members'], m.permanent + [m.ids['JAP']])
        self.assertEqual(m.random_calls, 0)

    def test_native_permanent_removal_keeps_other_members_and_rp_seats(self):
        m = Machine().ready()
        m.assign('africa', 'GHA')
        m.run('clear_united_nations_member_state', m.c['FRA'])
        self.assertEqual(m.g.vars[PREFIX + 'seat_africa'], m.ids['GHA'])
        self.assertNotIn(m.ids['FRA'], m.g.vars['security_council_members'])
        self.assertNotIn(m.ids['FRA'], m.g.vars['p5_sc_members'])
        self.assertEqual(m.random_calls, 0)

    def test_threshold_excludes_vote_subject_and_retains_native_veto(self):
        m = Machine().ready()
        for seat, tag in zip(SEATS, ('ARG', 'BEL', 'GHA', 'IRQ', 'JAP')):
            m.assign(seat, tag)
        m.g.vars['current_sc_vote_nation'] = m.ids['ARG']
        m.run('recompute_un_sc_required_yes')
        self.assertEqual(m.g.vars['un_sc_required_yes'], 6)
        m.g.vars['security_council_vote_yes'] = m.g.vars['security_council_members'][1:]
        self.assertTrue(m.condition([('has_passed_sc_vote', '=', 'yes')], m.root))
        m.g.flags.add('security_council_veto')
        self.assertFalse(m.condition([('has_passed_sc_vote', '=', 'yes')], m.root))

    def test_persisted_country_variables_rebuild_the_same_roster_for_another_gc(self):
        m = Machine().ready()
        m.assign('africa', 'GHA')
        m.assign('asia', 'JAP')
        expected = m.g.vars['security_council_members'].copy()
        m.root = m.c['BEL']
        m.root.ideas.add('imp_gc_nation')
        m.g.vars['security_council_members'] = []
        m.run(PREFIX + 'refresh')
        self.assertEqual(m.g.vars['security_council_members'], expected)
        m.root.vars['gc_tool_target_country'] = m.ids['ARG']
        m.decision('assign_africa', check=False)
        self.assertEqual(m.g.vars[PREFIX + 'seat_africa'], m.ids['ARG'])

    def test_scripts_localisation_references_and_encoding(self):
        for path in (*FILES, NATIVE, 'common/ideas/Organizations.txt'):
            load(path)
            self.assertFalse((ROOT / path).read_bytes().startswith(b'\xef\xbb\xbf'), path)
        locpath = ROOT / 'localisation/english/COLDWAR_gc_unsc_l_english.yml'
        self.assertTrue(locpath.read_bytes().startswith(b'\xef\xbb\xbf'))
        loc = locpath.read_text(encoding='utf-8-sig')
        keys = re.findall(r'^ ([\w.]+):', loc, re.M)
        self.assertEqual(len(keys), len(set(keys)))
        self.assertNotRegex('\n'.join(line for line in loc.splitlines() if not line.startswith('#')), '[\u2013\u2014]')
        self.assertTrue(loc.startswith('# IMPERIA COLD WAR'))
        for name in Machine().decisions:
            self.assertIn(name, keys)
            self.assertIn(name + '_desc', keys)
        for key in re.findall(r'\$([\w.]+)\$', loc):
            self.assertIn(key, keys)


if __name__ == '__main__':
    unittest.main(verbosity=2)
