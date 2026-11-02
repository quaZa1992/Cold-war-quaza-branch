# IMPERIA COLD WAR — Scoped country building-grant integration regressions.
"""Pure emitter and preservation checks. No broad country builder is imported."""
from __future__ import annotations

import ast
from contextlib import ExitStack, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'tools'))
from country_integration import SSR_PATHS, ssr_output, ssr_preservation, country_preservation, walk
from building_grants import grants
from focus_prerequisite_ui import nodes, field


def no_mutation(*args, **kwargs):
    raise AssertionError('A scoped pure emitter attempted a filesystem mutation')


def capacity_value(rows, states, current=None):
    """Evaluate only the emitted physical preflight, with strict native >."""
    def one(node):
        if node.key == 'AND':
            return capacity_value(node.children(), states, current)
        if node.key == 'OR':
            return any(capacity_value([child], states, current) for child in node.children())
        if node.key == 'any_owned_state':
            return any(capacity_value(node.children(), states, state) for state in states)
        if node.key == 'is_owned_and_controlled_by':
            return current['owned'] and current['controlled']
        if node.key == 'check_variable':
            body = node.children()
            assert field(body, 'compare') == 'less_than_or_equals'
            building = field(body, 'var').removeprefix('building_level@')
            return current['levels'].get(building, 0) <= int(field(body, 'value'))
        if node.key == 'collection_size':
            body = node.children()
            source = next(child for child in body if child.key == 'input')
            operators = next(child for child in source.children() if child.key == 'operators')
            self_scope = field(source.children(), 'input')
            assert self_scope == 'game:scope'
            assert any(child.key == '_bare' and child.value == 'owned_states' for child in operators.children())
            limit = next(child for child in operators.children() if child.key == 'limit')
            count = sum(capacity_value(limit.children(), states, state) for state in states)
            expected = next(child for child in body if child.key == 'value')
            assert expected.op == '>'
            return count > int(expected.value)
        raise AssertionError(('Unmodelled preflight condition', node.key))
    return all(one(node) for node in rows)


def owner_worker(tag):
    """Run the actual retained focus emitter in a disposable read-only process."""
    assert tag in ('SOV', 'DDR')
    generator = ROOT / ('Claude outputs/COLDWAR_' + tag + '_generator')
    sys.path.insert(0, str(generator))
    original_open = open

    def read_only_open(path, mode='r', *args, **kwargs):
        if any(character in mode for character in 'wax+'):
            no_mutation(path)
        return original_open(path, mode, *args, **kwargs)

    captured = []
    with ExitStack() as stack:
        stack.enter_context(patch('builtins.open', read_only_open))
        for name in ('write_text', 'write_bytes', 'mkdir', 'unlink', 'rename', 'replace'):
            stack.enter_context(patch.object(Path, name, no_mutation))
        for name in ('mkdir', 'makedirs', 'remove', 'unlink', 'rename', 'replace', 'rmdir'):
            stack.enter_context(patch.object(os, name, no_mutation))
        stack.enter_context(patch('shutil.rmtree', no_mutation))
        stack.enter_context(patch('shutil.copyfile', no_mutation))
        with redirect_stdout(io.StringIO()):
            module = __import__('cw_focus' if tag == 'SOV' else 'dg_focus')
            repair = module._grant_api.repair_focus_tree

            def observe(country, text):
                assert country == tag
                captured.append(text)
                return repair(country, text)

            stack.enter_context(patch.object(module._grant_api, 'repair_focus_tree', observe))
            # Naval retention has a separate full-emitter test suite. Capture
            # the actual country output before its independently owned graft.
            stack.enter_context(patch.object(module, '_naval_tree', lambda country, text: text))
            emitted = module.focus_file()
            assert len(captured) == 1
            result = country_preservation(tag, captured[0], emitted)
        assert not {'cw_build', 'dg_build'} & set(sys.modules)
    return dict(country=tag, **result, filesystem_writes=False, broad_builder_imported=False)


class CountryIntegrationTests(unittest.TestCase):
    def test_emitted_egyptian_two_plant_preflight_does_not_reuse_the_last_free_level(self):
        text = (ROOT / 'common/scripted_triggers/COLDWAR_GRANT_programmes.txt').read_text(encoding='utf-8-sig')
        trigger = next(node for node in nodes(text) if node.key == grants.PREFIX + 'capacity_COLDWAR_EGY_fn_shumans_legacy')
        def state(level, controlled=True):
            return dict(owned=True, controlled=controlled, levels={'renewable_energy_infra': level})
        self.assertFalse(capacity_value(trigger.children(), [state(19), state(20)]))
        self.assertTrue(capacity_value(trigger.children(), [state(18), state(20)]))
        self.assertTrue(capacity_value(trigger.children(), [state(19), state(19)]))
        self.assertFalse(capacity_value(trigger.children(), [state(19), state(0, False)]))

    def test_emitted_random_batches_require_two_or_three_distinct_eligible_states(self):
        text = (ROOT / 'common/scripted_triggers/COLDWAR_GRANT_programmes.txt').read_text(encoding='utf-8-sig')
        triggers = {node.key: node for node in nodes(text)}
        for fid, count in (('COLDWAR_SOV_she_the_komsomol_economy', 2),
                           ('COLDWAR_SOV_kv_construction_battalions', 3)):
            trigger = triggers[grants.PREFIX + 'capacity_' + fid]
            many_levels = [dict(owned=True, controlled=True, levels={'infrastructure': 0})]
            self.assertFalse(capacity_value(trigger.children(), many_levels))
            enough = [dict(owned=True, controlled=True, levels={'infrastructure': 5}) for _ in range(count)]
            self.assertTrue(capacity_value(trigger.children(), enough))
            self.assertFalse(capacity_value(trigger.children(), enough[:-1]))
            enough[-1]['controlled'] = False
            self.assertFalse(capacity_value(trigger.children(), enough))

    def test_emitted_egyptian_pending_callback_keeps_the_whole_price_and_receipt_inside_ready(self):
        fid = 'COLDWAR_EGY_fn_shumans_legacy'
        text = (ROOT / 'common/scripted_effects/COLDWAR_GRANT_programmes.txt').read_text(encoding='utf-8-sig')
        effects = {node.key: node for node in nodes(text)}
        complete = effects[grants.PREFIX + 'complete_' + fid]
        outer = complete.children()[0]
        self.assertEqual(outer.key, 'if')
        self.assertEqual([node.key for node in outer.children()], ['limit', 'set_country_flag', 'set_country_flag', 'if'])
        self.assertTrue(any(node.key == 'NOT' and field(node.children(), 'has_country_flag') == grants.PREFIX + 'done_' + fid
                            for node in outer.children()[0].children()))
        actual = outer.children()[-1]
        self.assertEqual([(node.key, node.value) for node in actual.children()[0].children()],
                         [(grants.PREFIX + 'ready_' + fid, 'yes')])
        payload = actual.children()[1:]
        self.assertEqual(sum(node.key == 'COLDWAR_EGY_pay_gdp_share' for node in payload), 1)
        self.assertTrue(any(node.key == 'COLDWAR_EGY_gdp_share' and node.value == '0.01' for node in walk(payload)))
        self.assertEqual(sum(node.key == grants.alias('one_state_renewable_energy_infra') for node in walk(payload)), 2)
        self.assertEqual([(node.key, node.value) for node in payload[-2:]],
                         [('set_country_flag', grants.PREFIX + 'done_' + fid),
                          ('clr_country_flag', grants.PREFIX + 'pending_' + fid)])
        migration = [node for node in effects[grants.PREFIX + 'tick_EGY'].children()
                     if node.key == 'if' and any(child.key == 'has_completed_focus' and child.value == fid
                                                for child in walk(node.children()[0].children()))]
        self.assertEqual(len(migration), 1)
        self.assertEqual([(node.key, node.value) for node in migration[0].children()[1:]],
                         [('set_country_flag', grants.PREFIX + 'done_' + fid)])

    def test_soviet_actual_pure_emitter_retains_the_complete_country_payload(self):
        self.check_owner('SOV', 30, 31)

    def test_east_german_actual_pure_emitter_retains_the_complete_country_payload(self):
        self.check_owner('DDR', 35, 36)

    def check_owner(self, tag, focuses, calls):
        result = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--owner', tag],
                                cwd=ROOT, capture_output=True, text=True, timeout=90,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['adapted_focuses'], focuses)
        self.assertEqual(report['adapted_helper_calls'], calls)
        self.assertFalse(report['filesystem_writes'])
        self.assertFalse(report['broad_builder_imported'])

    def test_egyptian_retained_focus_function_routes_the_final_tree_through_the_shared_repair(self):
        # Its complete legacy import has a pre-existing KeyError18. This test
        # makes the narrower source-hook guarantee without hiding that limit.
        path = ROOT / 'Claude outputs/COLDWAR_EGY_generator/cw_compile.py'
        parsed = ast.parse(path.read_text(encoding='utf-8-sig'))
        function = next(node for node in parsed.body if isinstance(node, ast.FunctionDef) and node.name == 'focus_file')
        returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
        self.assertEqual(len(returns), 1)
        call = returns[0].value
        self.assertIsInstance(call, ast.Call)
        self.assertEqual(ast.unparse(call.func), '_grant_api.repair_focus_tree')
        self.assertEqual(ast.literal_eval(call.args[0]), 'EGY')
        text = (ROOT / 'common/national_focus/COLDWAR_EGY_1970_focus.txt').read_text(encoding='utf-8-sig')
        tree = next(node for node in nodes(text) if node.key == 'focus_tree')
        focus = next(node for node in tree.children() if node.key == 'focus' and field(node.children(), 'id') == 'COLDWAR_EGY_the_el_dabaa_reactor')
        available = next(node for node in focus.children() if node.key == 'available')
        self.assertEqual([(node.key, node.value) for node in available.children()], [('has_tech', 'reactor1')])
        self.assertTrue(any(node.key == 'one_state_nuclear_reactor' for node in walk(focus.children())))
        self.assertFalse(any(node.key.startswith(grants.PREFIX) for node in walk(focus.children())))

    def test_country_build_packs_retain_shared_runtime_after_country_specific_formatting(self):
        for tag, source, owner in (
            ('SOV', 'cw_build.py', 'FO'), ('DDR', 'dg_build.py', 'FO'), ('EGY', 'cw_build.py', 'C')):
            path = ROOT / ('Claude outputs/COLDWAR_' + tag + '_generator') / source
            parsed = ast.parse(path.read_text(encoding='utf-8-sig'))
            updates = [node for node in parsed.body if isinstance(node, ast.Expr)
                       and isinstance(node.value, ast.Call) and ast.unparse(node.value.func) == 'FILES.update']
            self.assertTrue(updates, tag)
            self.assertEqual(ast.unparse(updates[-1].value.args[0]), owner + '._grant_runtime()', tag)
    def test_ssr_source_writer_applies_only_the_two_reviewed_outputs(self):
        source = (ROOT / 'tools/ssr_1970/compile.py').read_text(encoding='utf-8-sig')
        module = ast.parse(source)
        function = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == 'prepare_output')
        namespace = {'_grant_queries': grants.rewrite_queries, 'GRANT_OUTPUTS': set(SSR_PATHS)}
        exec(compile(ast.Module(body=[function], type_ignores=[]), '<isolated SSR writer>', 'exec'), namespace)
        fixture = 'free_building_slots = { building = infrastructure size > 0 }'
        transform = namespace['prepare_output']
        for relative in SSR_PATHS:
            self.assertEqual(transform(relative, fixture), ssr_output(fixture))
        self.assertEqual(transform('common/decisions/unrelated.txt', fixture), fixture)
        self.assertEqual(transform(SSR_PATHS[0], fixture, True), fixture)

    def test_actual_ssr_files_preserve_fossil_queries_and_cap_every_infrastructure_grant(self):
        for relative in SSR_PATHS:
            data = (ROOT / relative).read_bytes()
            self.assertFalse(data.startswith(b'\xef\xbb\xbf'))
            text = data.decode('utf-8')
            self.assertTrue(text.startswith('# IMPERIA COLD WAR'))
            self.assertEqual(ssr_output(text), text)
            caps = [node for node in walk(nodes(text)) if node.key == 'custom_trigger_tooltip'
                    and field(node.children(), 'tooltip') == grants.cap_key('infrastructure', 1)]
            self.assertEqual(len(caps), 34)
            fossils = [node for node in walk(nodes(text)) if node.key == 'free_building_slots'
                       and field(node.children(), 'building') == 'fossil_powerplant']
            self.assertEqual(len(fossils), 2)

    def test_ssr_pure_generate_base_matches_the_loaded_tree_and_rewards(self):
        folder = ROOT / 'tools/ssr_1970'
        sys.path.insert(0, str(folder))
        ordinary_open = open

        def read_only_open(path, mode='r', *args, **kwargs):
            if any(character in mode for character in 'wax+'):
                no_mutation(path)
            return ordinary_open(path, mode, *args, **kwargs)

        with ExitStack() as stack:
            stack.enter_context(patch('builtins.open', read_only_open))
            for name in ('write_text', 'write_bytes', 'mkdir', 'unlink', 'rename', 'replace'):
                stack.enter_context(patch.object(Path, name, no_mutation))
            for name in ('mkdir', 'makedirs', 'remove', 'unlink', 'rename', 'replace', 'rmdir'):
                stack.enter_context(patch.object(os, name, no_mutation))
            stack.enter_context(patch('shutil.rmtree', no_mutation))
            spec = importlib.util.spec_from_file_location('ssr_capacity_owner', folder / 'compile.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            captured = {}

            def capture(relative, body, localisation=False):
                captured[relative] = body
                return relative

            stack.enter_context(patch.object(module.shared, 'write', capture))
            with patch.object(module, '_grant_queries', lambda text, buildings=None: text):
                module.generate_base()
            original = dict(captured)
            captured.clear()
            module.generate_base()

        def semantics(text):
            def one(node):
                return (node.key, node.op, tuple(one(child) for child in node.children())
                        if isinstance(node.value, list) else node.value)
            return [one(node) for node in nodes(text)]

        for relative in SSR_PATHS:
            self.assertEqual(ssr_preservation(original[relative], captured[relative]), 34, relative)
            self.assertEqual(ssr_output(captured[relative]), captured[relative])
            self.assertEqual(semantics(captured[relative]),
                             semantics((ROOT / relative).read_text(encoding='utf-8-sig')), relative)
        self.assertNotIn('cw_build', sys.modules)
        self.assertNotIn('dg_build', sys.modules)


if __name__ == '__main__':
    if sys.argv[1:2] == ['--owner']:
        print(json.dumps(owner_worker(sys.argv[2])))
    else:
        unittest.main(verbosity=2)
