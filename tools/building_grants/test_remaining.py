# IMPERIA COLD WAR — Independent bounded review of remaining building-grant integrations.
"""Pure source/owner checks only. Never run a country build or write runtime files."""
from __future__ import annotations

import ast
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field
from building_grants import grants as G, remaining as R

# All six original blobs were independently checked against the audit SHA256s.
# Pin the object so later commits do not turn the review into a self-comparison.
AUDITED_COMMIT = '2d08dc687d26b9258921870f81d9107446665da0'
AUDIT = ROOT / 'docs/design/building_capacity_audit_20261027'


def read(relative):
    return (ROOT / relative).read_text(encoding='utf-8-sig')


def original(relative):
    data = subprocess.run(['git', 'show', AUDITED_COMMIT + ':' + relative], cwd=ROOT,
                          capture_output=True, check=True).stdout
    expected = json.loads((AUDIT / 'INVENTORY.json').read_text())['source_hashes'][relative]
    assert hashlib.sha256(data).hexdigest() == expected, ('Not the audited baseline', relative)
    return data.decode('utf-8-sig')


def sem(rows):
    return [(node.key, node.op, sem(node.children())
             if isinstance(node.value, list) else node.value) for node in rows]


def focus_map(text):
    tree = next(node for node in nodes(text) if node.key == 'focus_tree')
    return {field(node.children(), 'id'): node for node in tree.children() if node.key == 'focus'}


def meaningful_syria(rows, event22=False, option_name=None):
    """Remove only the three declared overlay operations for an independent diff."""
    result = []
    for node in rows:
        in_event22 = event22 or (node.key == 'country_event' and field(node.children(), 'id') == 'COLDWAR_SYR_FOREIGN.22')
        current_option = field(node.children(), 'name') if node.key == 'option' else option_name
        if in_event22 and node.key == 'custom_effect_tooltip' and str(node.value) in {
                'COLDWAR_SYR_FOREIGN.22.option_' + letter + '_outcome_tt' for letter in 'abc'}:
            continue
        if in_event22 and current_option in {'COLDWAR_SYR_FOREIGN.22.option_b', 'COLDWAR_SYR_FOREIGN.22.option_c'} and node.key == 'effect_tooltip':
            continue
        if node.key == 'add_extra_state_shared_building_slots':
            continue
        if node.key == 'is_owned_and_controlled_by' and node.value == 'SYR':
            continue
        key = field(node.children(), 'tooltip') if node.key == 'custom_trigger_tooltip' else None
        if key and str(key).startswith(G.PREFIX + 'capacity_'):
            building, quantity = key.removeprefix(G.PREFIX + 'capacity_').removesuffix('_tt').rsplit('_', 1)
            raw = next(child for child in node.children() if child.key == 'check_variable')
            maximum = int(G.building_definitions()[building]['state_max'])
            assert field(raw.children(), 'var') == 'building_level@' + building
            assert int(field(raw.children(), 'value')) == maximum - int(quantity)
            assert field(raw.children(), 'compare') == 'less_than_or_equals'
            result.append(('free_building_slots', '=', [
                ('building', '=', building), ('size', '>', str(int(quantity) - 1))]))
            continue
        result.append((node.key, node.op, meaningful_syria(node.children(), in_event22, current_option)
                       if isinstance(node.value, list) else node.value))
    return result


def no_write(*args, **kwargs):
    raise AssertionError('The independent review attempted a filesystem mutation')


class RemainingGrantTests(unittest.TestCase):
    def test_original_md_helpers_selectors_and_all_seven_technology_providers_are_unchanged(self):
        baseline = json.loads((AUDIT / 'INVENTORY.json').read_text())['source_hashes']
        techs = json.loads((AUDIT / 'TECH_UNLOCKS.json').read_text())['enables']
        sources = {row['source'] for row in techs}
        self.assertEqual(len(sources), 7)
        sources.update({'common/scripted_effects/00_scripted_effects.txt',
                        'common/scripted_triggers/00_scripted_triggers.txt'})
        for relative in sources:
            self.assertIn(relative, baseline)
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), baseline[relative], relative)

    def test_syria_all_four_actual_outputs_preserve_every_other_native_statement(self):
        for relative in sorted(R.SYR_PATHS):
            before = original(relative)
            expected = R.repair_syria_output(relative, before)
            actual = read(relative)
            self.assertEqual(sem(nodes(expected)), sem(nodes(actual)), relative)
            self.assertEqual(R.repair_syria_output(relative, expected), expected)
            self.assertEqual(R.repair_syria_output(relative, actual), actual)
            self.assertEqual(meaningful_syria(nodes(before)), meaningful_syria(nodes(actual)), relative)
            self.assertFalse((ROOT / relative).read_bytes().startswith(b'\xef\xbb\xbf'))
        unrelated = 'focus_tree = { focus = { id = OTHER completion_reward = { add_political_power = 7 } } }'
        self.assertEqual(R.repair_syria_output('common/national_focus/OTHER.txt', unrelated), unrelated)

    def test_syria_targets_actual_owner_and_slots_remain_inside_existing_once_only_transactions(self):
        definitions = {node.key: node for node in nodes(read('common/scripted_effects/COLDWAR_SYR_focus_rewards.txt'))}
        for fid, state, building, price in (
                ('COLDWAR_SYR_agriculture_09', '994', 'renewable_energy_infra', '-7'),
                ('COLDWAR_SYR_infrastructure_09', '566', 'infrastructure', '-6.25'),
                ('COLDWAR_SYR_infrastructure_11', '193', 'infrastructure', '-6.25')):
            effect = definitions[fid + '_implement']
            self.assertEqual([node.key for node in effect.children()], ['if'])
            transaction = effect.children()[0]
            gate = transaction.children()[0]
            self.assertEqual(gate.key, 'limit')
            self.assertTrue(any(node.key == 'NOT' and field(node.children(), 'has_country_flag') == fid + '_implemented'
                                for node in gate.children()))
            physical_state = next(node for node in gate.children() if node.key == state)
            self.assertEqual(field(physical_state.children(), 'is_owned_and_controlled_by'), 'SYR')
            self.assertTrue(any(node.key == 'check_variable' and field(node.children(), 'var') == 'building_level@' + building
                                for node in G.walk(physical_state.children())))
            actual_state = next(node for node in transaction.children()[1:] if node.key == state)
            self.assertEqual([node.key for node in actual_state.children()],
                             ['add_extra_state_shared_building_slots', 'add_building_construction'])
            self.assertEqual(actual_state.children()[0].value, '1')
            self.assertEqual(field(actual_state.children()[1].children(), 'type'), building)
            self.assertTrue(any(node.key == 'treasury_change' and node.value == price for node in G.walk(transaction.children()[1:])))
        event = next(node for node in nodes(read('events/COLDWAR_SYR_foreign_events.txt'))
                     if node.key == 'country_event' and field(node.children(), 'id') == 'COLDWAR_SYR_FOREIGN.22')
        deliveries = 0
        for option in [node for node in event.children() if node.key == 'option']:
            hidden = next(node for node in option.children() if node.key == 'hidden_effect')
            transaction = hidden.children()[0]
            buildings = [node for node in G.walk(transaction.children()[1:]) if node.key == 'add_building_construction']
            if not buildings:
                continue
            deliveries += 1
            preview = next(node for node in option.children() if node.key == 'effect_tooltip')
            self.assertTrue(all(node.key.isdecimal() for node in preview.children()))
            actual_assets = [node for node in transaction.children()[1:] if node.key.isdecimal()]
            self.assertEqual(sem(preview.children()), sem(actual_assets))
            self.assertFalse(any(node.key in {'set_country_flag', 'modify_treasury_effect'} for node in G.walk(preview.children())))
            gate = transaction.children()[0]
            self.assertTrue(any(node.key == 'has_country_flag' and node.value == 'COLDWAR_SYR_project_escrow'
                                for node in gate.children()))
            self.assertTrue(any(node.key == 'NOT' and field(node.children(), 'has_country_flag') == 'COLDWAR_SYR_foreign_project_completed'
                                for node in gate.children()))
            for state in [node for node in transaction.children()[1:] if node.key.isdecimal()]:
                for index, node in enumerate(state.children()):
                    if node.key == 'add_building_construction':
                        self.assertGreater(index, 0)
                        self.assertEqual(state.children()[index - 1].key, 'add_extra_state_shared_building_slots')
                        self.assertEqual(state.children()[index - 1].value, field(node.children(), 'level'))
        self.assertEqual(deliveries, 2)

    def test_generic_and_libyan_scope_preserves_original_unrelated_focuses_prices_and_geometry(self):
        for tag, count in (('GENERIC1970', 37), ('LBA', 1)):
            relative = G.scope()[tag]['tree']
            before = original(relative)
            after = G.repair_focus_tree(tag, before)
            self.assertEqual(G.repair_focus_tree(tag, after), after)
            old, new = focus_map(before), focus_map(after)
            installed = focus_map(read(relative))
            self.assertEqual(old.keys(), new.keys())
            self.assertEqual(new.keys(), installed.keys())
            for fid in new:
                self.assertEqual(sem([new[fid]]), sem([installed[fid]]), fid)
            if tag == 'LBA':
                self.assertEqual(sem(nodes(after)), sem(nodes(read(relative))))
            selected = set(G.scope()[tag]['focuses'])
            self.assertEqual(len(selected), count)
            for fid in old:
                if fid not in selected:
                    self.assertEqual(sem([old[fid]]), sem([new[fid]]), fid)
                    continue
                changed = {'available', 'completion_reward', 'cancel_if_invalid', 'continue_if_invalid'}
                self.assertEqual(sem([node for node in old[fid].children() if node.key not in changed]),
                                 sem([node for node in new[fid].children() if node.key not in changed]), fid)
                available = next((node for node in old[fid].children() if node.key == 'available'), None)
                expected_available = nodes(G.rewrite_queries(G._body(before, available))) if available else []
                actual_available = next(node for node in new[fid].children() if node.key == 'available').children()
                self.assertEqual(sem(actual_available[:len(expected_available)]), sem(expected_available), fid)
                completion = next(node for node in old[fid].children() if node.key == 'completion_reward')
                expected = G.add_missing_slots(G.rewrite_queries(G.rewrite_native_calls(G._body(before, completion))))
                if fid == 'GEN_1970_capital_defence_scheme':
                    expected = G.require_physical_owner(expected)
                preview = next(node for node in next(node for node in new[fid].children()
                               if node.key == 'completion_reward').children() if node.key == 'effect_tooltip')
                self.assertEqual(sem(nodes(expected)), sem(preview.children()), fid)

    def test_generic_actual_final_owner_function_calls_repair_after_its_layout_stage(self):
        sys.path.insert(0, str(ROOT / 'Claude outputs/COLDWAR_GEN_generator'))
        ordinary_open = open
        def reader(path, mode='r', *args, **kwargs):
            if any(character in mode for character in 'wax+'):
                no_write(path)
            return ordinary_open(path, mode, *args, **kwargs)
        with ExitStack() as stack:
            stack.enter_context(patch('builtins.open', reader))
            for method in ('write_text', 'write_bytes', 'mkdir', 'unlink', 'rename', 'replace'):
                stack.enter_context(patch.object(Path, method, no_write))
            stack.enter_context(patch('shutil.rmtree', no_write))
            import gen_focus, gen_load
            fixture = original(G.scope()['GENERIC1970']['tree'])
            with patch.object(gen_load, 'read', return_value=(fixture, False)):
                loaded = gen_load.load_focus_file(str(ROOT))
            sections = dict(loaded['sections'])
            political = {outlook: '\n'.join(gen_focus.emit_block(focus['fields']) for focus in sections[name])
                         for outlook, name in gen_focus.POLITICAL_SECTIONS.items()}
            moves, _, _ = gen_focus.domain_moves(loaded['sections'])
            captured = []
            def observe(tag, text):
                self.assertEqual(tag, 'GENERIC1970')
                captured.append(text)
                return G.repair_focus_tree(tag, text)
            with patch.object(gen_focus, '_repair_grants', observe):
                actual = gen_focus.write_focus_file(loaded, political, moves)
            self.assertEqual(len(captured), 1)
            expected = focus_map(G.repair_focus_tree('GENERIC1970', captured[0]))
            self.assertEqual(set(focus_map(actual)), set(expected))
            for fid, focus in focus_map(actual).items():
                self.assertEqual(sem([focus]), sem([expected[fid]]))
            self.assertEqual(set(focus_map(actual)), set(focus_map(loaded['text'])))
            self.assertNotIn('gen_build', sys.modules)

    def test_syrian_canonical_postformat_writers_and_final_streamlining_hook_are_reachable(self):
        relative = 'common/national_focus/COLDWAR_SYR_1970_focus.txt'
        fixture = original(relative)
        module = ast.parse(read('tools/syria_1970/build_content.py'))
        function = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'write')
        order = []
        class Formatter:
            @staticmethod
            def format_script(text):
                order.append('format')
                return text
        def repair(path, text):
            order.append('repair')
            return R.repair_syria_output(path, text)
        namespace = dict(ROOT=ROOT, PROJECT_MARKER='# IMPERIA CW\n', FORMAT=Formatter,
                         repair_syria_output=repair, OUTPUTS=[], Path=Path)
        exec(compile(ast.Module(body=[function], type_ignores=[]), '<isolated Syria write>', 'exec'), namespace)
        expected = R.repair_syria_output(relative, fixture).encode('utf-8')
        with patch.object(Path, 'mkdir', return_value=None), patch.object(Path, 'exists', return_value=True), \
                patch.object(Path, 'read_bytes', return_value=expected), patch.object(Path, 'write_bytes', no_write):
            namespace['write'](relative, fixture)
        self.assertEqual(order, ['format', 'repair'])
        self.assertEqual(namespace['OUTPUTS'], [relative])
        foreign = ast.parse(read('tools/syria_1970/foreign.py'))
        closure = next(node for node in ast.walk(foreign) if isinstance(node, ast.FunctionDef) and node.name == 'write')
        calls = [node for node in ast.walk(closure) if isinstance(node, ast.Call)]
        format_line = next(node.lineno for node in calls if ast.unparse(node.func) == 'formatter.format_script')
        repair_line = next(node.lineno for node in calls if ast.unparse(node.func) == 'repair_syria_output')
        write_line = next(node.lineno for node in calls if ast.unparse(node.func) == 'p.write_text')
        self.assertLess(format_line, repair_line)
        self.assertLess(repair_line, write_line)
        streamline = ast.parse(read('tools/syria_1970/streamlining_build.py'))
        transform = next(node for node in ast.walk(streamline) if isinstance(node, ast.Call)
                         and ast.unparse(node.func) == 'streamlining.transform')
        last_repair = max(node.lineno for node in ast.walk(streamline) if isinstance(node, ast.Call)
                          and ast.unparse(node.func) == 'repair_syria_output')
        self.assertLess(transform.lineno, last_repair)

    def test_generic_dependency_writer_is_after_country_outputs_and_ddr_overlay_hook_is_before_parse(self):
        module = ast.parse(read('Claude outputs/COLDWAR_GEN_generator/gen_build.py'))
        main = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
        runtime = next(node for node in ast.walk(main) if isinstance(node, ast.For)
                       and any(isinstance(call, ast.Call) and ast.unparse(call.func) == 'grant_runtime_outputs' for call in ast.walk(node.iter)))
        local_runtime = next(node for node in ast.walk(main) if isinstance(node, ast.For)
                             and any(isinstance(call, ast.Call) and ast.unparse(call.func) == 'runtime_files' for call in ast.walk(node.iter)))
        self.assertGreater(runtime.lineno, local_runtime.lineno)
        overlay = ast.parse(read('tools/focus_quality_20261020/apply_ddr_reward_overlay.py'))
        repair = next(node for node in ast.walk(overlay) if isinstance(node, ast.Call)
                      and ast.unparse(node.func) == 'repair_focus_tree')
        self.assertEqual(ast.literal_eval(repair.args[0]), 'DDR')
        self.assertEqual([(keyword.arg, ast.unparse(keyword.value)) for keyword in repair.keywords],
                         [('external_triggers', 'triggers_text')])
        parse = next(node for node in ast.walk(overlay) if isinstance(node, ast.Assign)
                     and any(isinstance(target, ast.Name) and target.id == 'focus_ast' for target in node.targets))
        self.assertLess(repair.lineno, parse.lineno)
        self.assertTrue(any(isinstance(node, ast.Call) and ast.unparse(node.func) == 'grant_runtime_outputs'
                            for node in ast.walk(overlay)))

    def test_current_ddr_new_six_recipes_are_kept_inside_all_35_repaired_focuses(self):
        relative = G.scope()['DDR']['tree']
        before = read(relative)
        external = read('common/scripted_triggers/COLDWAR_DDR_20261027_programmes.txt')
        fixed = G.repair_focus_tree('DDR', before, external_triggers=external)
        self.assertEqual(G.repair_focus_tree('DDR', fixed, external_triggers=external), fixed)
        old, new = focus_map(before), focus_map(fixed)
        selected = set(G.scope()['DDR']['focuses'])
        self.assertEqual(len(selected), 35)
        direct = []
        for fid in selected:
            callback = [node for node in G.walk(old[fid].children())
                        if node.key.startswith('COLDWAR_DDR_20261027_run_') and node.value == 'yes']
            if callback:
                self.assertEqual(len(callback), 1)
                direct.append(fid)
                self.assertEqual(sum(node.key == callback[0].key for node in G.walk(new[fid].children())), 1)
                source = next(node for node in old[fid].children() if node.key == 'completion_reward')
                if any(node.key == G.PREFIX + 'complete_' + fid for node in G.walk(source.children())):
                    source = next(node for node in source.children() if node.key == 'effect_tooltip')
                preview = next(node for node in next(node for node in new[fid].children()
                               if node.key == 'completion_reward').children() if node.key == 'effect_tooltip')
                self.assertEqual(sem(nodes(G.add_missing_slots(G._body(before, source)))), sem(preview.children()), fid)
                key = callback[0].key.replace('_run_', '_can_', 1)
                trigger = next(node for node in nodes(external) if node.key == key)
                actual = next(node for node in new[fid].children() if node.key == 'available').children()
                expected = nodes(G.rewrite_queries(G._body(external, trigger)))
                self.assertEqual(sem(actual[:len(expected)]), sem(expected), fid)
            self.assertTrue(any(node.key == G.PREFIX + 'complete_' + fid for node in G.walk(new[fid].children())))
        self.assertEqual(len(direct), 6)
        changed = {'available', 'completion_reward', 'cancel_if_invalid', 'continue_if_invalid'}
        for fid in old:
            self.assertEqual(sem([node for node in old[fid].children() if node.key not in changed]),
                             sem([node for node in new[fid].children() if node.key not in changed]), fid)

    def test_ddr_fresh_atomic_guard_is_not_replaced_by_old_on_disk_guard_in_runtime_pack(self):
        spec = deepcopy(G.scope()['DDR'])
        source = read(spec['tree'])
        external = read('common/scripted_triggers/COLDWAR_DDR_20261027_programmes.txt')
        key = 'COLDWAR_DDR_20261027_can_energy_greifswald_nuclear_power_station'
        trigger = next(node for node in nodes(external) if node.key == key)
        marker = 'COLDWAR_TEST_fresh_atomic_guard'
        fresh = external[:trigger.end - 1] + '\nhas_country_flag = ' + marker + '\n' + external[trigger.end - 1:]
        with patch.dict(G._TREES, {}, clear=True), patch.dict(G._RECORDS, {}, clear=True), \
                patch.object(G, 'scope', return_value={'DDR': spec}):
            repaired = G.repair_focus_tree('DDR', source, external_triggers=fresh)
            record = next(row for row in G._RECORDS['DDR'] if row['id'].endswith('energy_greifswald_nuclear_power_station'))
            self.assertIn(marker, record['available'])
            with patch.object(G, '_external_available', side_effect=AssertionError('A wrapped tree must retain its self-contained fresh guard')):
                outputs = G._programme_outputs()
                self.assertEqual(G.repair_focus_tree('DDR', repaired), repaired)
            record = next(row for row in G._RECORDS['DDR'] if row['id'].endswith('energy_greifswald_nuclear_power_station'))
            self.assertIn(marker, record['available'])
            self.assertTrue(any(marker in payload for payload in outputs[1]))

    def test_generic_current_tree_load_and_roundtrip_preserve_all_focuses_and_cyprus_imports(self):
        sys.path.insert(0, str(ROOT / 'Claude outputs/COLDWAR_GEN_generator'))
        import gen_focus, gen_load
        source = read(G.scope()['GENERIC1970']['tree'])
        loaded = gen_load.load_focus_file(str(ROOT))
        self.assertEqual(loaded['text'], source)
        sections = dict(loaded['sections'])
        political = {outlook: '\n'.join(gen_focus.emit_block(focus['fields']) for focus in sections[name])
                     for outlook, name in gen_focus.POLITICAL_SECTIONS.items()}
        moves, _, _ = gen_focus.domain_moves(loaded['sections'])
        self.assertTrue(all(move[:2] == (0, 0) for move in moves.values()))
        with patch.object(Path, 'write_bytes', no_write), patch.object(Path, 'write_text', no_write):
            actual = gen_focus.write_focus_file(loaded, political, moves)
        old, new = focus_map(source), focus_map(actual)
        self.assertEqual(old.keys(), new.keys())
        for fid in old:
            self.assertEqual(sorted(sem(old[fid].children()), key=repr),
                             sorted(sem(new[fid].children()), key=repr), fid)
        imports = lambda text: sem([node for node in next(node for node in nodes(text) if node.key == 'focus_tree').children()
                                   if node.key in {'shared_focus', 'shortcut'}])
        self.assertEqual(imports(source), imports(actual))
        self.assertEqual(actual.count('# IMPERIA COLD WAR — Cyprus guarantor imports BEGIN'), 1)
        self.assertEqual(actual.count('# IMPERIA COLD WAR — Cyprus guarantor imports END'), 1)
        with patch.object(gen_load, 'read', return_value=(actual, False)):
            second = gen_load.load_focus_file(str(ROOT))
        self.assertEqual({focus['id'] for _, section in second['sections'] for focus in section}, set(old))
        self.assertEqual(gen_load.without_cyprus_import_tail('focus_tree = { focus = { id = OTHER } }'),
                         'focus_tree = { focus = { id = OTHER } }')
        with self.assertRaises(ValueError):
            gen_load.without_cyprus_import_tail(source.replace('Cyprus guarantor imports END', 'Cyprus guarantor imports MISSING'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
