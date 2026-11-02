# IMPERIA COLD WAR — USA programme source and transaction regression checks.
"""Execute emitted domestic transactions in a bounded source model, not HOI4."""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal as D
import importlib.util
import json
from pathlib import Path
import re
import unittest

HERE = Path(__file__).resolve().parent
module_spec = importlib.util.spec_from_file_location('domestic', HERE / 'domestic.py')
domestic = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(domestic)
ROOT = domestic.ROOT
parse, first = domestic.parser()
PREFIX = domestic.PREFIX
from usa_building_capacity import building_definitions


class Model:
    def __init__(self):
        self.effects = dict((k, v) for k, _, v in parse((ROOT / 'common/scripted_effects/COLDWAR_USA_1970_programmes.txt').read_text()))
        self.triggers = dict((k, v) for k, _, v in parse((ROOT / 'common/scripted_triggers/COLDWAR_USA_1970_programmes.txt').read_text()))
        self.vars = {'treasury': D(2000), 'additional_expenses_rate': D(0)}
        self.flags, self.ideas, self.focuses, self.doctrines = set(), {}, set(), set()
        self.party, self.tag, self.scenario = 1, 'USA', True
        self.original_tag = 'USA'
        self.date = (1975, 1, 1)
        self.congress = True
        self.law = 'draft_army'
        self.bonuses, self.xp = [], {'army': 0, 'air': 0, 'navy': 0}
        self.states = [dict(id=778, owner='USA', controller='USA', core=True, slots=10,
                            industrial_complex=2, offices=1, infrastructure=2)]

    def condition(self, body, state=None):
        for k, op, v in body:
            if k in self.triggers:
                ok = self.condition(self.triggers[k], state) == (v == 'yes')
            elif k == 'OR':
                ok = any(self.condition([node], state) for node in v)
            elif k == 'NOT':
                ok = not self.condition(v, state)
            elif k == 'AND':
                ok = self.condition(v, state)
            elif k == 'original_tag':
                ok = self.original_tag == v
            elif k == 'tag':
                ok = self.tag == v
            elif k == 'IMP_is_1970_scenario':
                ok = self.scenario == (v == 'yes')
            elif k == 'has_country_flag':
                ok = v in self.flags
            elif k == 'has_idea':
                ok = v in self.ideas or v == self.law
            elif k == 'has_doctrine':
                ok = v in self.doctrines
            elif k == 'date':
                ok = self.date > tuple(int(x) for x in v.split('.'))
            elif k in ('congress_high_support_trigger', 'congress_low_support_trigger'):
                ok = self.congress
            elif k == 'has_completed_focus':
                ok = v in self.focuses
            elif k in ('western_liberals_are_in_power', 'western_conservatism_are_in_power'):
                ok = self.party == (2 if k == 'western_liberals_are_in_power' else 1)
            elif k == 'any_owned_state':
                ok = any(s['owner'] == self.tag and self.condition(v, s) for s in self.states)
            elif k == 'is_core_of':
                ok = state['core'] and v == 'USA'
            elif k == 'is_owned_and_controlled_by':
                ok = state['owner'] == self.tag and state['controller'] == self.tag
            elif k == 'state':
                ok = state['id'] == int(v)
            elif k == 'free_building_slots':
                b = first(v, 'building')
                _, sign, amount = next(x for x in v if x[0] == 'size')
                definition = building_definitions()[b]
                if not definition['shares_slots']:
                    assert first(v, 'include_locked') is None, 'include_locked is only native for shared-slot buildings'
                native = int(definition['state_max']) - state.get(b, 0)
                room = min(native, state['slots']) if definition['shares_slots'] else native
                ok = room > int(amount) if sign == '>' else room >= int(amount)
            elif k == 'custom_trigger_tooltip':
                ok = self.condition([x for x in v if x[0] != 'tooltip'], state)
            elif k == 'check_variable':
                variable = first(v, 'var')
                if variable.startswith('building_level@'):
                    assert state is not None, 'building_level is a native state-scope dynamic variable'
                    value = D(state.get(variable.split('@', 1)[1], 0))
                else:
                    value = self.vars.get(variable, D(0))
                comparison = first(v, 'compare')
                right = D(first(v, 'value'))
                assert comparison in ('greater_than_or_equals', 'less_than_or_equals'), comparison
                ok = value >= right if comparison == 'greater_than_or_equals' else value <= right
            else:
                raise AssertionError(('unsupported condition', k, op, v))
            if not ok:
                return False
        return True

    def run(self, body, state=None):
        branch = False
        for k, _, v in body:
            if k == 'if':
                branch = self.condition(first(v, 'limit', []), state)
                if branch:
                    self.run([x for x in v if x[0] != 'limit'], state)
            elif k == 'else_if':
                if not branch and self.condition(first(v, 'limit', []), state):
                    self.run([x for x in v if x[0] != 'limit'], state)
                    branch = True
            elif k == 'else':
                if not branch:
                    self.run(v, state)
                branch = True
            elif k in self.effects:
                self.run(self.effects[k], state)
            elif k in ('set_variable', 'set_temp_variable', 'add_to_variable'):
                name, _, value = v[0]
                amount = self.vars[value] if value in self.vars else D(value)
                self.vars[name] = (self.vars.get(name, D(0)) if k == 'add_to_variable' else D(0)) + amount
            elif k == 'modify_treasury_effect':
                self.vars['treasury'] += self.vars['treasury_change']
            elif k == 'set_country_flag':
                self.flags.add(v)
            elif k == 'clr_country_flag':
                self.flags.discard(v)
            elif k == 'add_ideas':
                self.ideas[v] = None
            elif k == 'remove_ideas':
                self.ideas.pop(v, None)
            elif k == 'add_timed_idea':
                self.ideas[first(v, 'idea')] = int(first(v, 'days'))
            elif k == 'random_owned_state':
                found = next((s for s in self.states if s['owner'] == self.tag and self.condition(first(v, 'limit', []), s)), None)
                if found is not None:
                    self.run([x for x in v if x[0] != 'limit'], found)
            elif k == 'add_extra_state_shared_building_slots':
                state['slots'] += int(v)
            elif k == 'add_building_construction':
                b, q = first(v, 'type'), int(first(v, 'level'))
                state[b] = state.get(b, 0) + q
                if b != 'infrastructure':
                    state['slots'] -= q
            elif k in ('add_tech_bonus', 'add_doctrine_cost_reduction'):
                self.bonuses.append((k, deepcopy(v)))
            elif k in ('army_experience', 'air_experience', 'navy_experience'):
                self.xp[k.split('_')[0]] += int(v)
            elif k == 'add_political_power':
                self.vars['political_power'] = self.vars.get('political_power', D(0)) + D(v)
            elif k == 'set_volunteer_army_effect':
                if self.law == 'volunteer_army':
                    self.xp['army'] += 20
                else:
                    self.law = 'volunteer_army'
            elif k == 'set_draft_army_effect':
                if self.law == 'draft_army':
                    self.xp['army'] += 20
                else:
                    self.law = 'draft_army'
            elif k in ('effect_tooltip', 'unlock_decision_tooltip', 'force_update_dynamic_modifier'):
                pass
            elif k == 'hidden_effect':
                self.run(v, state)
            else:
                raise AssertionError(('unsupported effect', k, v))

    def call(self, name):
        self.run(self.effects[name])


class DomesticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        domestic.build()
        cls.specs = json.loads((HERE / 'domestic_focus_specs.json').read_text())['focuses']
        cls.by_id = {s['id']: s for s in cls.specs}

    def prepare(self, focus_id, model=None):
        m = model or Model()
        spec = self.by_id[focus_id]
        seen = set()
        def ancestors(ident):
            if ident in seen:
                return
            seen.add(ident)
            entry = self.by_id.get(ident)
            if not entry:
                m.focuses.add(ident)
                return
            for group in entry['prerequisites']:
                ancestors(group[0])
            if ident != focus_id:
                m.focuses.add(ident)
                m.flags.add(entry['done_flag'])
                if ident == 'USA_1970_D1':
                    m.law = 'volunteer_army'
        ancestors(focus_id)
        m.party = 2 if spec['party_trigger'] == 'western_liberals_are_in_power' else 1
        m.flags.add('COLDWAR_USA_domestic_v1_initialized')
        m.call(PREFIX + 'reconcile')
        return m, spec

    def snapshot(self, m):
        return deepcopy((m.vars, m.flags, m.ideas, m.states, m.bonuses, m.xp, m.law))

    def test_every_focus_completion_is_once_and_nationally_scoped(self):
        for spec in self.specs:
            with self.subTest(focus=spec['id']):
                m, s = self.prepare(spec['id'])
                m.call(s['completion_effect'])
                self.assertIn(s['done_flag'], m.flags)
                self.assertNotIn(s['pending_flag'], m.flags)
                before = self.snapshot(m)
                m.call(s['completion_effect'])
                m.call(s['apply_effect'])
                m.call(PREFIX + 'reconcile')
                self.assertEqual(before, self.snapshot(m))
                other, _ = self.prepare(spec['id'])
                other.tag = 'CAN'
                before = self.snapshot(other)
                other.call(s['completion_effect'])
                self.assertEqual(before, self.snapshot(other))

    def test_inspection_does_not_execute_previews(self):
        for s in self.specs:
            m, _ = self.prepare(s['id'])
            before = self.snapshot(m)
            m.run(parse(s['completion_reward'].split('hidden_effect')[0]))
            self.assertEqual(before, self.snapshot(m))

    def test_lost_control_defers_whole_transaction_then_recovers_once(self):
        m, s = self.prepare('USA_1970_E1')
        m.states[0]['controller'] = 'CAN'
        money, state = m.vars['treasury'], deepcopy(m.states)
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)
        self.assertIn(s['pending_flag'], m.flags)
        self.assertEqual(money, m.vars['treasury'])
        self.assertEqual(state, m.states)
        m.states[0]['controller'] = 'USA'
        m.call(s['apply_effect'])
        self.assertIn(s['done_flag'], m.flags)
        self.assertEqual(m.vars['treasury'], money - 30)
        self.assertEqual(m.states[0]['industrial_complex'], 4)

    def test_native_building_cap_is_independent_of_slots(self):
        native = first(parse((ROOT / 'common/buildings/00_buildings.txt').read_text()), 'buildings')
        for kind, ceiling in [('industrial_complex', 50), ('offices', 50), ('infrastructure', 6)]:
            self.assertEqual(int(first(first(first(native, kind), 'level_cap'), 'state_max')), ceiling)
        emitted = (ROOT / 'common/scripted_triggers/COLDWAR_USA_1970_programmes.txt').read_text()
        self.assertNotRegex(emitted, r'\bhas_building\s*=')
        self.assertIn('var = building_level@industrial_complex value = 48 compare = less_than_or_equals', emitted)
        self.assertIn('var = building_level@infrastructure value = 4 compare = less_than_or_equals', emitted)
        m, s = self.prepare('USA_1970_E1')
        m.states[0]['industrial_complex'] = 49
        m.states[0]['slots'] = 99
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)
        self.assertEqual(m.vars['treasury'], D(2000))
        m.states[0]['industrial_complex'] = 48
        m.call(s['apply_effect'])
        self.assertEqual(m.states[0]['industrial_complex'], 50)
        # A two-level infrastructure grant cannot overrun its native six-level
        # ceiling, even though infrastructure does not consume shared slots.
        infra, s = self.prepare('USA_X_dem72_public')
        infra.states[0]['infrastructure'] = 5
        infra.states[0]['slots'] = 99
        infra.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], infra.flags)
        self.assertEqual(infra.vars['treasury'], D(2000))
        infra.states[0]['infrastructure'] = 4
        infra.states[0]['slots'] = 0
        infra.call(s['apply_effect'])
        self.assertEqual(infra.states[0]['infrastructure'], 6)
        self.assertEqual(infra.states[0]['slots'], 2)

    def test_energy_audits_use_independent_infrastructure_capacity(self):
        m, s = self.prepare('USA_X_efficiency_priority')
        m.states[0]['infrastructure'] = 3
        m.states[0]['slots'] = 0
        capacity = next(k for k in m.triggers if k.startswith(PREFIX + 'capacity_') and 'efficiency_priority' in k)
        self.assertTrue(m.condition(m.triggers[capacity]))
        m.call(s['completion_effect'])
        self.assertIn(s['done_flag'], m.flags)
        self.assertEqual(m.states[0]['infrastructure'], 5)
        self.assertEqual(m.states[0]['slots'], 2)
        earned = self.snapshot(m)
        m.call(s['completion_effect'])
        self.assertEqual(earned, self.snapshot(m))

    def test_shared_industry_still_checks_actual_shared_space(self):
        m, s = self.prepare('USA_1970_E1')
        m.states[0]['slots'] = 0
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)
        self.assertEqual(m.vars['treasury'], D(2000))

    def test_party_departure_restores_earned_tier_without_assets(self):
        m, s = self.prepare('USA_X_dem72_public_follow')
        m.call(s['completion_effect'])
        self.assertIn(s['programme_ideas'][-1], m.ideas)
        assets = deepcopy((m.vars['treasury'], m.states, m.bonuses, m.xp))
        m.party = 1
        m.call(PREFIX + 'reconcile')
        self.assertFalse(set(s['programme_ideas']) & set(m.ideas))
        m.party = 2
        m.call(PREFIX + 'reconcile')
        self.assertIn(s['programme_ideas'][-1], m.ideas)
        self.assertEqual(assets, (m.vars['treasury'], m.states, m.bonuses, m.xp))

    def test_wrong_party_during_completion_never_receives_assets(self):
        m, s = self.prepare('USA_X_dem72_public')
        m.party = 1
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)
        self.assertEqual(m.vars['treasury'], D(2000))
        m.party = 2
        m.call(s['apply_effect'])
        self.assertIn(s['done_flag'], m.flags)

    def test_deficit_does_not_block_native_focus_payment(self):
        m, s = self.prepare('USA_X_nuclear_priority')
        m.vars['treasury'] = D(-5)
        m.call(s['completion_effect'])
        self.assertEqual(m.vars['treasury'], D(-35))
        self.assertIn(s['done_flag'], m.flags)

    def test_native_military_law_controls_establishment(self):
        m, s = self.prepare('USA_1970_D1')
        m.call(s['completion_effect'])
        self.assertIn(s['programme_ideas'][0], m.ideas)
        m.law = 'draft_army'
        m.call(PREFIX + 'reconcile')
        self.assertNotIn(s['programme_ideas'][0], m.ideas)
        m.law = 'volunteer_army'
        m.call(PREFIX + 'reconcile')
        self.assertIn(s['programme_ideas'][0], m.ideas)
        draft, s = self.prepare('USA_1970_D2')
        draft.doctrines.add('mdcw_all_volunteer_force')
        draft.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], draft.flags)
        self.assertEqual(draft.vars['treasury'], D(2000))

    def test_legacy_congress_and_force_model_guards_rechecked(self):
        m, s = self.prepare('USA_1970_D3')
        m.congress = False
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)
        self.assertEqual(m.vars['treasury'], D(2000))
        m.congress = True
        m.call(s['apply_effect'])
        self.assertIn(s['done_flag'], m.flags)
        m, s = self.prepare('USA_1970_D2')
        m.flags.add('USA_1970_force_model_selected')
        m.flags.add('USA_1970_all_volunteer_transition_started')
        m.call(s['completion_effect'])
        self.assertNotIn(s['done_flag'], m.flags)

    def test_export_guarantees_are_funded_and_rechecked(self):
        m, s = self.prepare('USA_X_export_credit')
        m.call(s['completion_effect'])
        decisions = dict((k, v) for k, _, v in parse((ROOT / 'common/decisions/COLDWAR_USA_1970_programmes.txt').read_text()))
        category = decisions[PREFIX + 'credit_category']
        decision = first(category, PREFIX + 'export_credit_guarantees')
        m.vars['treasury'] = D('4.99999')
        self.assertFalse(m.condition(first(decision, 'available')))
        m.vars['treasury'] = D(5)
        self.assertTrue(m.condition(first(decision, 'available')))
        m.run(first(decision, 'complete_effect'))
        self.assertEqual(m.vars['treasury'], 0)
        self.assertEqual(m.ideas[PREFIX + 'export_guarantees'], 180)
        self.assertFalse(m.condition(first(decision, 'available')))

    def test_migration_removes_only_recorded_policy_once(self):
        m = Model()
        m.focuses.add('USA_1970_E1')
        m.vars['econ_factory_output'] = D('0.53')
        before = deepcopy((m.vars['treasury'], m.states, m.bonuses, m.xp))
        m.call(PREFIX + 'initialize')
        self.assertEqual(m.vars['econ_factory_output'], D('0.50'))
        self.assertIn(PREFIX + 'E1_s0', m.ideas)
        self.assertEqual(before, (m.vars['treasury'], m.states, m.bonuses, m.xp))
        first_snapshot = self.snapshot(m)
        m.call(PREFIX + 'initialize')
        self.assertEqual(first_snapshot, self.snapshot(m))

    def test_nuclear_weekly_hook_is_reset_then_recomputed(self):
        m, s = self.prepare('USA_X_nuclear_priority')
        m.call(s['completion_effect'])
        for _ in range(3):
            m.vars['additional_expenses_rate'] = D(10)
            m.call(PREFIX + 'add_expense_rate')
            self.assertEqual(m.vars['COLDWAR_USA_domestic_weekly_expense'], D('0.03'))
            self.assertEqual(m.vars['additional_expenses_rate'], D('10.03'))
        m.ideas.clear()
        m.call(PREFIX + 'recalculate_weekly_expense')
        self.assertEqual(m.vars['COLDWAR_USA_domestic_weekly_expense'], 0)

    def test_native_references_encodings_and_preview_effects(self):
        owned = [ROOT / p for p in [
            'common/ideas/COLDWAR_USA_1970_programmes.txt',
            'common/scripted_effects/COLDWAR_USA_1970_programmes.txt',
            'common/scripted_triggers/COLDWAR_USA_1970_programmes.txt',
            'common/decisions/COLDWAR_USA_1970_programmes.txt',
            'common/decisions/categories/COLDWAR_USA_1970_programmes.txt']]
        for path in owned:
            data = path.read_bytes()
            self.assertFalse(data.startswith(b'\xef\xbb\xbf'), path)
            self.assertTrue(data.decode().startswith('# IMPERIA COLD WAR \u2014 '), path)
            parse(data.decode())
        loc = ROOT / 'localisation/english/COLDWAR_USA_1970_programmes_l_english.yml'
        self.assertTrue(loc.read_bytes().startswith(b'\xef\xbb\xbfl_english:\n# IMPERIA COLD WAR'))
        text = loc.read_text(encoding='utf-8-sig')
        keys = re.findall(r'^\s+(\S+):0 ', text, re.M)
        self.assertEqual(len(keys), len(set(keys)))
        for s in self.specs:
            if s['id'].startswith('USA_1970_'):
                self.assertNotIn(s['id'], keys)
        titles_path = HERE / 'focus_titles.json'
        if titles_path.exists():
            titles = json.loads(titles_path.read_text())['titles']
            for s in self.specs:
                if s['id'] in titles:
                    self.assertEqual(s['name'], titles[s['id']])
                    if s['id'].startswith('USA_X_'):
                        self.assertIn(' ' + s['id'] + ':0 ' + json.dumps(titles[s['id']]), text)
        native = '\n'.join(p.read_text(encoding='utf-8-sig') for folder in ('common/ideas', 'common/dynamic_modifiers', 'common/modifier_definitions') for p in (ROOT / folder).glob('*.txt') if p.name != 'COLDWAR_USA_1970_programmes.txt')
        for modifier in domestic.MODIFIERS.values():
            self.assertRegex(native, r'\b' + modifier + r'\s*=')
        idea_text = (ROOT / 'common/ideas/COLDWAR_USA_1970_programmes.txt').read_text()
        self.assertNotIn('allowed_civil_war = { always = yes }', idea_text)
        idea_definitions = first(first(parse(idea_text), 'ideas'), 'country')
        for ident, _, definition in idea_definitions:
            self.assertEqual(first(first(definition, 'allowed'), 'tag'), 'USA', ident)
            self.assertIsNotNone(first(definition, 'cancel'), ident)
        gfx = '\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT / 'interface').glob('*.gfx'))
        for icon in set(s['icon'] for s in self.specs):
            self.assertIn('name = "' + icon + '"', gfx)
        for picture in set(domestic.PICTURES.values()) | {'USA_capitol_building'}:
            self.assertIn('name = "GFX_idea_' + picture + '"', gfx)
        technology = '\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT / 'common/technologies').glob('*.txt'))
        for category in ('CAT_industry', 'CAT_electronics', 'CAT_nuclear_reactors', 'CAT_aircraft', 'CAT_destroyers', 'CAT_submarines'):
            self.assertIn(category, technology)


if __name__ == '__main__':
    unittest.main(verbosity=2)
