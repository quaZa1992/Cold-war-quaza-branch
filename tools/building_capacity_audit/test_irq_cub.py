# IMPERIA COLD WAR — Iraqi and Cuban physical-gift boundary regressions.
"""Pure tests: no country compiler, runtime writer, native process or snapshot."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from building_capacity_audit.irq_cub import (
    FILES, SLOT_FILES, cub_radar_queries, cub_silo_queries, irq_queries, irq_slots, proof, rewrite_selected,
)
from building_grants.grants import capacity_localisation
from vietnam_1970.script_ast import first, parse, walk


def isolated_function(relative, name, namespace):
    """Load only a pure function AST, never a country's top-level builder."""
    path = ROOT / relative
    module = ast.parse(path.read_text(encoding='utf-8'))
    function = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])), str(path), 'exec'), namespace)
    return namespace[name]


def checks(text):
    return [value for key, _, value in walk(parse(text)) if key == 'check_variable']


class PhysicalScopeTests(unittest.TestCase):
    def test_single_and_multiple_level_physical_limits(self):
        for kind, cap, quantity in [('infrastructure', 6, 1), ('fuel_silo', 5, 1),
                                    ('fuel_silo', 5, 2), ('radar_station', 6, 1)]:
            source = f'854 = {{ free_building_slots = {{ building = {kind} size > {quantity - 1} include_locked = no }} }}'
            rewritten = rewrite_selected(source, frozenset((kind,)))
            row = next(c for c in checks(rewritten) if first(c, 'var') == 'building_level@' + kind)
            self.assertEqual(first(row, 'compare'), 'less_than_or_equals')
            self.assertEqual(int(first(row, 'value')), cap - quantity)
            self.assertIn(f'COLDWAR_GRANT_capacity_{kind}_{quantity}_tt', rewritten)

    def test_shared_province_and_other_types_are_unchanged(self):
        source = ('171 = { free_building_slots = { building = dockyard size > 0 include_locked = no } '
                  'free_building_slots = { building = naval_base size > 0 province = 9045 } '
                  'free_building_slots = { building = fuel_silo size > 0 province = 9045 } '
                  'free_building_slots = { building = fossil_powerplant size > 0 } }')
        self.assertEqual(irq_queries(source), source)
        self.assertEqual(cub_silo_queries(source), source)
        self.assertEqual(cub_radar_queries(source), source)

    def test_country_filters_do_not_expand_scope(self):
        fuel = 'free_building_slots = { building = fuel_silo size > 0 }'
        radar = 'free_building_slots = { building = radar_station size > 0 }'
        infra = 'free_building_slots = { building = infrastructure size > 0 }'
        self.assertEqual(irq_queries(radar), radar)
        self.assertEqual(cub_silo_queries(radar + '\n' + infra), radar + '\n' + infra)
        self.assertEqual(cub_radar_queries(fuel + '\n' + infra), fuel + '\n' + infra)

    def test_inverse_proof_preserves_credit_fee_and_consented_transaction(self):
        source = '''test = {
 if = { limit = { CUB = { has_country_flag = offer_open } has_country_flag = pending
 NOT = { has_war_with = CUB } NOT = { has_country_flag = done }
 OR = { has_country_flag = old_component
  AND = { check_variable = { credit = 0 } 854 = { free_building_slots = { building = radar_station size > 0 } } }
  AND = { check_variable = { credit = 1 } } }
 }
 set_temp_variable = { treasury_change = -.15 }
 modify_treasury_effect = yes
 CUB = { set_temp_variable = { treasury_change = -.45 } modify_treasury_effect = yes
 854 = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = radar_station level = 1 instant_build = yes } }
 set_country_flag = done country_event = { id = test.1 days = 1 } }
 } }
'''
        changes = []
        rewritten = rewrite_selected(source, frozenset(('radar_station',)), changes=changes)
        proof(source, rewritten, changes)
        self.assertEqual(len(changes), 1)
        self.assertEqual(cub_radar_queries(rewritten), rewritten)

    def test_capacity_labels_are_provided_centrally(self):
        locale = capacity_localisation()
        for kind in ['infrastructure', 'fuel_silo', 'radar_station']:
            self.assertIn(f'COLDWAR_GRANT_capacity_{kind}_1_tt', locale)

    def test_slots_follow_only_the_remaining_positive_instant_quantity(self):
        raw = isolated_function('tools/iraq_1970/reward_overhaul.py', '_raw', {'P': 'COLDWAR_IRQ_'})
        component = {'kind': 'building', 'state': 171, 'building_type': 'fuel_silo', 'amount': 3,
                     'receipt': 'test_component'}
        self.assertEqual(irq_slots(raw(component, 0)), '')
        for remaining in [1, 2, 3]:
            result = irq_slots(raw(component, remaining))
            self.assertIn(f'add_extra_state_shared_building_slots = {remaining}', result)
            self.assertIn(f'level = {remaining}', result)
            self.assertEqual(result.count('add_extra_state_shared_building_slots'), 1)

    def test_existing_slots_and_normal_queues_are_not_duplicated(self):
        paired = '166 = { add_extra_state_shared_building_slots = 1 add_building_construction = { type = infrastructure level = 1 instant_build = yes } }'
        queued = '166 = { add_building_construction = { type = infrastructure level = 1 instant_build = no } }'
        self.assertEqual(irq_slots(paired), paired)
        self.assertEqual(irq_slots(queued), queued)


class CanonicalAndInstalledTests(unittest.TestCase):
    def test_irq_canonical_all_twenty_target_nodes_keep_full_credit_alternative(self):
        b = first(parse((ROOT / 'common/buildings/00_buildings.txt').read_text(encoding='utf-8')), 'buildings')
        namespace = {'BUILDINGS': {k: v for k, _, v in b}, 'first': first,
                     'flag': lambda name: 'has_country_flag = ' + name,
                     'check': lambda var, value: f'check_variable = {{ var = {var} value = {value} compare = greater_than_or_equals }}',
                     'block': lambda key, body: key + ' = {\n' + body + '\n}',
                     '_gift_capacity_queries': irq_queries}
        capacity = isolated_function('tools/iraq_1970/compile.py', 'capacity', namespace)
        model = json.loads((ROOT / 'tools/iraq_1970/current_design.json').read_text(encoding='utf-8'))
        targets = [n for n in model['nodes'] if n.get('overhaul_changed') and
                   any(c['kind'] == 'building' and c['building_type'] in ('infrastructure', 'fuel_silo')
                       for c in n['overhaul_components'])]
        self.assertEqual(len(targets), 20)
        for node in targets:
            text = capacity(node)
            for component in node['overhaul_components']:
                if component['kind'] != 'building': continue
                if component['building_type'] not in ('infrastructure', 'fuel_silo'): continue
                self.assertIn('has_country_flag = ' + component['receipt'], text)
                self.assertIn(component['credit'], text)
                self.assertIn(f'building_level@{component["building_type"]}', text)
                self.assertIn('is_owned_and_controlled_by = IRQ', text)
            self.assertEqual(irq_queries(text), text)

    def test_irq_canonical_legacy_component_keeps_receipt(self):
        b = first(parse((ROOT / 'common/buildings/00_buildings.txt').read_text(encoding='utf-8')), 'buildings')
        ns = {'BUILDINGS': {k: v for k, _, v in b}, 'first': first,
              'flag': lambda name: 'has_country_flag = ' + name,
              'block': lambda key, body: key + ' = {\n' + body + '\n}', '_gift_capacity_queries': irq_queries}
        f = isolated_function('tools/iraq_1970/compile.py', 'capacity', ns)
        result = f({'building': [166, 'infrastructure', 1], 'audit_delivery_components': [{'kind': 'building', 'receipt': 'old_delivery'}]})
        self.assertIn('has_country_flag = old_delivery', result)
        self.assertIn('building_level@infrastructure value = 5', result)

    def test_irq_final_emission_pairs_slots_without_running_compiler(self):
        output = {}
        ns = {'OUTPUTS': output, 'HEADER': '# IMPERIA COLD WAR — Test.\n',
              'format_code': lambda text: text, '_gift_slots': irq_slots,
              '_naval_strip': lambda tag, text: text, '_naval_tree': lambda tag, text: text}
        code = isolated_function('tools/iraq_1970/compile.py', 'code', ns)
        code('common/scripted_effects/test.txt', '166 = { add_building_construction = { type = infrastructure level = 2 instant_build = yes } }')
        self.assertIn('add_extra_state_shared_building_slots = 2', output['common/scripted_effects/test.txt'])

    def test_cuba_canonical_silo_and_province_exclusion(self):
        f = isolated_function('tools/cuba_1970/compile.py', 'economic_guard', {'cub_silo_queries': cub_silo_queries})
        for kind, province in [('fuel_silo', None), ('naval_base', 7622), ('fossil_powerplant', None)]:
            effect = {'kind': 'building', 'building': kind, 'state': 854, 'level': 1}
            if province: effect['province'] = province
            result = '\n'.join(f({'effects': [effect]}))
            self.assertIn('owns_state = 854', result)
            self.assertIn('controls_state = 854', result)
            if kind == 'fuel_silo': self.assertIn('building_level@fuel_silo value = 4', result)
            else: self.assertIn('free_building_slots', result)
            if province: self.assertIn('controls_province = 7622', result)

    def test_all_seven_installed_files_are_idempotent_and_have_valid_encoding(self):
        for rel, kinds in FILES.items():
            raw = (ROOT / rel).read_bytes()
            self.assertFalse(raw.startswith(b'\xef\xbb\xbf'), rel)
            text = raw.decode('utf-8')
            self.assertTrue(text.startswith('# IMPERIA COLD WAR — '), rel)
            self.assertEqual(rewrite_selected(text, kinds), text, rel)
            self.assertTrue(parse(text), rel)

    def test_all_five_installed_slot_paths_are_paired_and_idempotent(self):
        for rel in SLOT_FILES:
            text = (ROOT / rel).read_text(encoding='utf-8')
            self.assertEqual(irq_slots(text), text, rel)


if __name__ == '__main__':
    unittest.main()
