# IMPERIA COLD WAR — Gulf prospective-tooltip purity and contract checks.
"""Read emitted-in-memory source. These checks do not start or emulate HOI4."""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal as D
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from focus_prerequisite_ui import nodes, field
import gulf_previews as preview
import usa_module


def walk(rows):
    for n in rows:
        yield n
        yield from walk(n.children())


def semantic(rows, ignore_preview=False):
    return [(n.key, n.op, semantic(n.children(), ignore_preview) if isinstance(n.value, list) else n.value)
            for n in rows if not (ignore_preview and n.key in ('effect_tooltip', 'custom_effect_tooltip'))]


class GulfPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loc = {}
        cls.preview = preview.previews(cls.loc)
        # Canonical source generation is pure. Block all ordinary file writes.
        with (patch.object(Path, 'write_text', side_effect=AssertionError('Unexpected write')),
              patch.object(Path, 'write_bytes', side_effect=AssertionError('Unexpected write'))):
            with patch.object(preview, 'apply_previews', return_value=None):
                cls.before = usa_module.generate(ROOT)
            cls.after = usa_module.generate(ROOT)
        cls.fragment = 'tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt'
        cls.old_focuses = {field(n.children(), 'id'): n for n in nodes(cls.before[cls.fragment]) if n.key == 'focus'}
        cls.new_focuses = {field(n.children(), 'id'): n for n in nodes(cls.after[cls.fragment]) if n.key == 'focus'}

    def test_actual_runtime_contracts_unchanged(self):
        allowed = {self.fragment, 'localisation/english/COLDWAR_USA_gulf_l_english.yml'}
        self.assertEqual(self.before.keys(), self.after.keys())
        for path in self.before:
            if path not in allowed:
                self.assertEqual(self.before[path], self.after[path], path)

    def test_focus_execution_and_conditions_identical(self):
        self.assertEqual(self.old_focuses.keys(), self.new_focuses.keys())
        for focus in self.old_focuses:
            self.assertEqual(semantic(self.old_focuses[focus].children(), True),
                             semantic(self.new_focuses[focus].children(), True), focus)

    def test_all_new_statements_have_nonexecuting_outer_wrapper(self):
        for key, code in self.preview.items():
            self.assertTrue(nodes(code), key)
            self.assertTrue(all(n.key == 'effect_tooltip' for n in nodes(code)), key)
            forbidden = {'hidden_effect', 'set_country_flag', 'clr_country_flag', 'set_variable',
                         'country_event', 'modify_treasury_effect'}
            self.assertFalse(forbidden & {n.key for n in walk(nodes(code))}, key)

    def test_previews_are_not_hidden_by_recipient_or_receipt_gates(self):
        for key, code in self.preview.items():
            self.assertFalse({'if', 'else_if', 'limit', 'exists', 'has_country_flag',
                              'has_completed_focus'} & {n.key for n in walk(nodes(code))}, key)
        for key in ('arm_front', 'no_fly', 'assembly', 'baghdad_accord', 'self_rule', 'recovery'):
            for tag in preview.LOCAL:
                self.assertIn(preview.Q + 'country_' + tag + '_tt', self.preview[key])

    def test_original_suffix_and_localisation_retained(self):
        rewards = {k: 'hidden_effect = { set_country_flag = original_' + k + ' }' for k in self.preview}
        rewards['no_fly'] += '\ncustom_effect_tooltip = ' + preview.P + 'air_offers_tt'
        original = deepcopy(rewards)
        loc = {'unrelated_existing_key': 'Retained English text'}
        preview.apply_previews(rewards, loc)
        for key in rewards:
            expected = original[key].replace('custom_effect_tooltip = ' + preview.P + 'air_offers_tt', '') if key == 'no_fly' else original[key]
            self.assertTrue(rewards[key].endswith(expected), key)
        self.assertEqual(loc['unrelated_existing_key'], 'Retained English text')
        once = deepcopy(rewards)
        preview.apply_previews(rewards, loc)
        self.assertEqual(rewards, once)

    def test_iran_access_only_northern_and_all_host_invoices(self):
        self.assertIn('country_PER_tt', self.preview['northern_access'])
        self.assertNotIn('country_PER_tt', self.preview['desert_shield'])
        for key, amount, count in [('desert_shield', -2, 4), ('northern_access', -.5, 5)]:
            amounts = [D(n.value) for n in walk(nodes(self.preview[key])) if n.key == preview.Q + 'treasury']
            self.assertEqual(amounts, [D(str(amount))] * count)
            relations = [n for n in walk(nodes(self.preview[key])) if n.key == 'diplomatic_relation']
            self.assertEqual(len(relations), count * 2)

    def test_optional_coalition_cash_is_real_matched_transfer(self):
        amounts = [D(n.value) for n in walk(nodes(self.preview['coalition'])) if n.key == preview.Q + 'treasury']
        self.assertEqual(amounts, [D('.25'), D('-.25')] * 5)
        self.assertNotIn('add_to_faction', self.preview['coalition'])
        self.assertNotIn('declare_war', self.preview['coalition'])

    def test_arms_and_advisers_exact_terms(self):
        code = self.preview['arm_front']
        direct = [n for n in nodes(code) if field(n.children(), 'custom_effect_tooltip') in
                  [preview.Q + 'arms_' + tag + '_tt' for tag in preview.LOCAL]]
        amounts = [D(n.value) for n in walk(direct) if n.key == preview.Q + 'treasury']
        self.assertEqual(amounts, [D('-.25'), D('.25')] * 2)
        weapons = [D(field(n.children(), 'amount')) for n in walk(direct) if n.key == 'add_equipment_to_stockpile']
        self.assertEqual(weapons, [D(-1000), D(1000)] * 2)
        advisory = [n for n in nodes(code) if field(n.children(), 'custom_effect_tooltip') in
                    [preview.Q + 'advisers_' + tag + '_tt' for tag in preview.LOCAL]]
        weekly = [D(n.value) for n in walk(advisory) if n.key == preview.Q + 'weekly']
        self.assertEqual(weekly, [D('-.05'), D('.05')] * 2)
        self.assertEqual(code.count('idea = COLDWAR_KUR_us_advisers days = 90'), 2)

    def test_underground_commitment_and_future_cache_do_not_duplicate_cash(self):
        sections = {field(n.children(), 'custom_effect_tooltip'): n for n in nodes(self.preview['arm_front'])}
        underground = list(walk(sections[preview.Q + 'underground_initial_tt'].children()))
        self.assertEqual([D(n.value) for n in underground if n.key == preview.Q + 'treasury'], [D('-.25')])
        self.assertEqual([D(n.value) for n in underground if n.key == preview.Q + 'weekly'], [D('-.05')])
        self.assertEqual([D(n.value) for n in underground if n.key == preview.Q + 'days'], [D(90)])
        self.assertEqual([D(field(n.children(), 'amount')) for n in underground if n.key == 'add_equipment_to_stockpile'], [D(-1000)])
        for tag in preview.LOCAL:
            cache = list(walk(sections[preview.Q + 'cache_' + tag + '_tt'].children()))
            self.assertIn('TT_IF_THEY_ACCEPT', [n.value for n in cache if n.key == 'custom_effect_tooltip'])
            self.assertNotIn(preview.Q + 'treasury', [n.key for n in cache])
            self.assertEqual([D(field(n.children(), 'amount')) for n in cache if n.key == 'add_equipment_to_stockpile'], [D(1000)])

    def test_every_offered_idea_modifier_matches_native_provider(self):
        idea_source = self.after['common/ideas/COLDWAR_USA_gulf_ideas.txt']
        definitions = {n.key: n for n in walk(nodes(idea_source)) if n.key.startswith(('COLDWAR_KUR_', preview.P))}
        coverage = {'arm_front': ['COLDWAR_KUR_us_advisers'],
                    'no_fly': [preview.P + 'northern_air_readiness', 'COLDWAR_KUR_coalition_air_cover'],
                    'baghdad_accord': [preview.P + 'recognised_budget', preview.P + 'recognised_development'],
                    'self_rule': [preview.P + 'external_guarantee', preview.P + 'northern_air_readiness', 'COLDWAR_KUR_coalition_air_cover']}
        for key, names in coverage.items():
            values = {(n.key.removeprefix(preview.Q), D(n.value)) for n in walk(nodes(self.preview[key]))
                      if n.key.startswith(preview.Q) and isinstance(n.value, str) and n.value.replace('-', '').replace('.', '').isdigit()}
            for name in names:
                for node in definitions[name].children():
                    if node.key in ('modifier', 'targeted_modifier'):
                        for mod in node.children():
                            if mod.key != 'tag':
                                self.assertIn((mod.key, D(mod.value)), values, (key, name, mod.key))

    def test_accord_and_external_terms_no_un_promise(self):
        accord, external = self.preview['baghdad_accord'], self.preview['self_rule']
        self.assertIn(preview.Q + 'gdp = -0.02', accord)
        self.assertIn(preview.Q + 'weekly = -0.025', accord)
        self.assertIn(preview.Q + 'weekly = -0.05', external)
        self.assertIn('autonomy_state = COLDWAR_IRQ_kurdish_autonomy freedom_level = 0.8', accord)
        self.assertNotIn('set_autonomy', external)
        self.assertNotIn('guarantee =', external)
        for code in (accord, external):
            self.assertIn('add_political_power = -25', code)
            self.assertIn('add_political_power = -100', code)
            self.assertIn(preview.Q + 'treasury = -0.25', code)

    def test_recipient_development_slots_before_construction(self):
        rebuilds = [n for n in walk(nodes(self.preview['recovery'])) if n.key in map(str, preview.NORTH)]
        self.assertEqual(len(rebuilds), 8)  # Four prospective states, separately for each local recipient.
        for state in rebuilds:
            keys = [n.key for n in state.children()]
            self.assertLess(keys.index('add_extra_state_shared_building_slots'), keys.index('add_building_construction'))
            self.assertEqual(field(state.children(), 'add_extra_state_shared_building_slots'), '1')

    def test_each_local_project_has_its_own_price_and_single_building(self):
        projects = [n for n in nodes(self.preview['recovery']) if str(field(n.children(), 'custom_effect_tooltip')).startswith(preview.Q + 'local_rebuild_')]
        self.assertEqual(len(projects), 8)
        for project in projects:
            rows = list(walk(project.children()))
            self.assertEqual([D(n.value) for n in rows if n.key == preview.Q + 'treasury'], [D('-.2')])
            self.assertEqual(len([n for n in rows if n.key == 'add_building_construction']), 1)
            self.assertEqual(len([n for n in rows if n.key == 'add_extra_state_shared_building_slots']), 1)

    def test_native_label_reference_closure(self):
        sources = [self.after['localisation/english/COLDWAR_USA_gulf_l_english.yml']]
        for p in [ROOT / 'localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml',
                  ROOT / 'localisation/english/MD_dm_modifiers_l_english.yml',
                  ROOT / 'localisation/english/MD_buildings_l_english.yml',
                  ROOT / 'localisation/english/state_names_l_english.yml',
                  Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/localisation/english/modifiers_l_english.yml')]:
            if p.exists():
                sources.append(p.read_text(encoding='utf-8-sig'))
        registered = set(re.findall(r'^\s*([^\s:#]+):', '\n'.join(sources), re.M))
        required = set(re.findall(r'\$([A-Za-z0-9_]+)\$', '\n'.join(self.loc.values())))
        self.assertFalse(required - registered, required - registered)


if __name__ == '__main__':
    unittest.main(verbosity=2)
