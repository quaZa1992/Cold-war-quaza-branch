# IMPERIA COLD WAR — Read-only canonical naval emitter retention checks.
"""Exercise pure focus emitters, never broad country builders or game launches.

Each legacy emitter gets a fresh process so its registries cannot contaminate
another country or a second emission. The naval hook records the original
emitter string before adding its chapter. All ordinary filesystem writes are
blocked while imports and the pure focus function execute.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
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


def _worker(tag: str) -> dict:
    assert tag in {"SOV", "DDR"}
    generator = ROOT / f"Claude outputs/COLDWAR_{tag}_generator"
    sys.path.insert(0, str(ROOT / "tools"))
    sys.path.insert(0, str(generator))
    module_name = "cw_focus" if tag == "SOV" else "dg_focus"
    expected = 20 if tag == "SOV" else 15
    captured = []
    ordinary_open = open

    def guarded_open(path, mode="r", *args, **kwargs):
        if any(character in mode for character in "wax+"):
            raise AssertionError(f"Emitter attempted a filesystem write: {path}")
        return ordinary_open(path, mode, *args, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError("Pure emitter attempted a filesystem mutation")

    with contextlib.ExitStack() as stack:
        stack.enter_context(patch("builtins.open", guarded_open))
        for method in ("write_text", "write_bytes", "mkdir", "unlink", "rename", "replace"):
            stack.enter_context(patch.object(Path, method, forbidden))
        for method in ("mkdir", "makedirs", "remove", "unlink", "rename", "replace", "rmdir"):
            stack.enter_context(patch.object(os, method, forbidden))
        stack.enter_context(patch("shutil.rmtree", forbidden))
        stack.enter_context(patch("shutil.copyfile", forbidden))
        with contextlib.redirect_stdout(io.StringIO()):
            module = __import__(module_name)
            original_hook = module._naval_tree

            def observing_hook(country, text):
                assert country == tag
                captured.append(text)
                return original_hook(country, text)

            with patch.object(module, "_naval_tree", observing_hook):
                emitted = module.focus_file()
            assert len(captured) == 1
            assert not {"cw_build", "dg_build"} & set(sys.modules)
            from focus_prerequisite_ui import nodes, field

            def focus_map(text):
                tree = next(node for node in nodes(text) if node.key == "focus_tree")
                return {field(node.children(), "id"): text[node.start:node.end]
                        for node in tree.children() if node.key == "focus"}

            baseline = captured[0]
            before, after = focus_map(baseline), focus_map(emitted)
            prefix = f"COLDWAR_NAVY_{tag}_"
            new_ids = {key for key in after if key.startswith(prefix)}
            assert len(new_ids) == expected
            assert {key: value for key, value in after.items() if key not in new_ids} == before
            begin = f"# IMPERIA COLD WAR — {tag} naval adaptation BEGIN"
            end = f"# IMPERIA COLD WAR — {tag} naval adaptation END"
            assert emitted.count(begin) == emitted.count(end) == 1
            stripped = re.sub(r"(?ms)^[\t ]*" + re.escape(begin)
                              + r".*?^[\t ]*" + re.escape(end) + r"\n?", "", emitted)

            def semantics(items):
                return [(node.key, node.op, semantics(node.children())
                         if isinstance(node.value, list) else node.value) for node in items]

            assert semantics(nodes(stripped)) == semantics(nodes(baseline))
            assert original_hook(tag, emitted) == emitted
    return {"country": tag, "existing_focuses_preserved_byte_for_byte": len(before),
            "new_focuses": len(new_ids), "marked_block_count": 1,
            "original_tree_semantics_preserved": True, "idempotent": True,
            "broad_build_imported": False, "filesystem_writes": False}


class OwnerHookTests(unittest.TestCase):
    def run_emitter(self, country):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", country],
                                cwd=ROOT, env=env, capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["original_tree_semantics_preserved"])
        self.assertTrue(report["idempotent"])
        return report

    def test_soviet_pure_emitter_preserves_original_country_tree(self):
        report = self.run_emitter("SOV")
        self.assertEqual(report["new_focuses"], 20)

    def test_ddr_pure_emitter_preserves_original_country_tree(self):
        report = self.run_emitter("DDR")
        self.assertEqual(report["new_focuses"], 15)

    def test_legacy_emitter_tools_paths_resolve_to_actual_workspace(self):
        for relative in ("Claude outputs/COLDWAR_SOV_generator/cw_focus.py",
                         "Claude outputs/COLDWAR_DDR_generator/dg_focus.py",
                         "tools/iraq_1970/compile.py", "tools/uae_1970/compile.py"):
            with self.subTest(path=relative):
                source = (ROOT / relative).read_text(encoding="utf-8-sig")
                ast.parse(source, filename=relative)
                self.assertIn('_NavalPath(__file__).resolve().parents[2] / "tools"', source)
                self.assertEqual((ROOT / relative).resolve().parents[2] / "tools", ROOT / "tools")

    def test_iraqi_and_emirati_focus_hooks_are_in_the_real_pure_emission_path(self):
        for tag, relative, function in (("IRQ", "tools/iraq_1970/compile.py", "generate_focuses"),
                                       ("UAE", "tools/uae_1970/compile.py", "focus_outputs")):
            with self.subTest(country=tag):
                tree = ast.parse((ROOT / relative).read_text(encoding="utf-8-sig"))
                emitter = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                               and node.name == function)
                hooks = [node for node in ast.walk(emitter) if isinstance(node, ast.Call)
                         and isinstance(node.func, ast.Name) and node.func.id == "_naval_tree"]
                if tag == "UAE":
                    self.assertEqual(len(hooks), 1)
                    self.assertEqual(hooks[0].args[0].value, tag)
                else:
                    # IRQ's code() formats after generate_focuses. The hook
                    # belongs after that formatter, never inside its input.
                    self.assertEqual(hooks, [])
                    deliveries = [node for node in ast.walk(emitter)
                                  if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                                  and node.func.id == "code" and node.args
                                  and isinstance(node.args[0], ast.Constant)
                                  and node.args[0].value == "common/national_focus/COLDWAR_IRQ_1970_focus.txt"]
                    self.assertEqual(len(deliveries), 1)

    def test_irq_code_preserves_markers_across_real_formatter_and_repeat_delivery(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from naval_adaptation_1970 import naval_adapter
        from focus_prerequisite_ui import nodes, field

        source_path = ROOT / "tools/iraq_1970/compile.py"
        python_tree = ast.parse(source_path.read_text(encoding="utf-8-sig"))
        code_function = next(node for node in python_tree.body
                             if isinstance(node, ast.FunctionDef) and node.name == "code")
        header_assignment = next(node for node in python_tree.body
                                 if isinstance(node, ast.Assign)
                                 and any(isinstance(target, ast.Name) and target.id == "HEADER"
                                         for target in node.targets))
        header = ast.literal_eval(header_assignment.value)
        spec = importlib.util.spec_from_file_location(
            "native_irq_formatter_retention_test", ROOT / "tools/vietnam_1970/script_ast.py")
        formatter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(formatter)
        from building_capacity_audit.irq_cub import irq_slots
        namespace = {"HEADER": header, "OUTPUTS": {}, "format_code": formatter.format_code,
                     "_naval_tree": naval_adapter.integrate_tree,
                     "_naval_strip": naval_adapter.strip_tree,
                     "_gift_slots": irq_slots}
        # Execute only this captured function definition. Do not import compile.py.
        isolated = ast.Module(body=[code_function], type_ignores=[])
        exec(compile(isolated, str(source_path) + ":code_only", "exec"), namespace)
        relative = "common/national_focus/COLDWAR_IRQ_1970_focus.txt"
        current = (ROOT / relative).read_text(encoding="utf-8-sig")
        base = naval_adapter.strip_tree("IRQ", current)
        begin = "# IMPERIA COLD WAR — IRQ naval adaptation BEGIN"
        end = "# IMPERIA COLD WAR — IRQ naval adaptation END"

        def semantics(text):
            def visit(items):
                return [(node.key, node.op, visit(node.children())
                         if isinstance(node.value, list) else node.value) for node in items]
            return visit(nodes(text))

        def verify(text):
            self.assertEqual(text.count(begin), 1)
            self.assertEqual(text.count(end), 1)
            tree = next(node for node in nodes(text) if node.key == "focus_tree")
            new = [node for node in tree.children() if node.key == "focus"
                   and str(field(node.children(), "id")).startswith("COLDWAR_NAVY_IRQ_")]
            self.assertEqual(len(new), 15)
            self.assertEqual(semantics(naval_adapter.strip_tree("IRQ", text)), semantics(base))

        with patch.object(Path, "write_text", side_effect=AssertionError("Review forbids writes")), \
                patch.object(Path, "write_bytes", side_effect=AssertionError("Review forbids writes")):
            # Counterexample: the former order loses markers but retains IDs,
            # which makes the next ordinary integration reject duplicates.
            broken = header + formatter.format_code(naval_adapter.integrate_tree("IRQ", base))
            self.assertNotIn(begin, broken)
            with self.assertRaises(AssertionError):
                naval_adapter.integrate_tree("IRQ", broken)

            namespace["code"](relative, current)
            first = namespace["OUTPUTS"][relative]
            verify(first)
            for _ in range(3):
                namespace["code"](relative, namespace["OUTPUTS"][relative])
                self.assertEqual(namespace["OUTPUTS"][relative], first)
                verify(namespace["OUTPUTS"][relative])
            namespace["code"](relative, base)
            self.assertEqual(namespace["OUTPUTS"][relative], first)
            other = "common/scripted_effects/COLDWAR_IRQ_retention_fixture.txt"
            fixture = "fixture = { set_country_flag = fixture_done }"
            namespace["code"](other, fixture)
            self.assertEqual(namespace["OUTPUTS"][other], header + formatter.format_code(fixture))
            self.assertNotIn(begin, namespace["OUTPUTS"][other])
        self.assertNotIn("cw_build", sys.modules)
        self.assertNotIn("dg_build", sys.modules)

    def test_runtime_pack_is_last_dictionary_update_in_each_owner(self):
        for relative, dictionary, legacy in (
                ("Claude outputs/COLDWAR_SOV_generator/cw_build.py", "FILES", True),
                ("Claude outputs/COLDWAR_DDR_generator/dg_build.py", "FILES", True),
                ("tools/iraq_1970/compile.py", "OUTPUTS", False),
                ("tools/uae_1970/compile.py", "outputs", False)):
            with self.subTest(path=relative):
                tree = ast.parse((ROOT / relative).read_text(encoding="utf-8-sig"))
                updates = sorted((node for node in ast.walk(tree) if isinstance(node, ast.Call)
                                  and isinstance(node.func, ast.Attribute)
                                  and isinstance(node.func.value, ast.Name)
                                  and node.func.value.id == dictionary and node.func.attr == "update"),
                                 key=lambda node: node.lineno)
                self.assertTrue(updates)
                call = updates[-1].args[0]
                self.assertIsInstance(call, ast.Call)
                if legacy:
                    self.assertIsInstance(call.func, ast.Attribute)
                    self.assertEqual(call.func.value.id, "FO")
                    self.assertEqual(call.func.attr, "_grant_runtime")
                    # Both independently owned runtime packs follow local
                    # country formatting. The grant dependency now comes last.
                    naval = updates[-2].args[0]
                    self.assertIsInstance(naval, ast.Call)
                    self.assertEqual(ast.unparse(naval.func), "FO._naval_runtime")
                else:
                    self.assertIsInstance(call.func, ast.Name)
                    self.assertEqual(call.func.id, "_naval_runtime")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        print(json.dumps(_worker(sys.argv[2])))
    else:
        unittest.main(verbosity=2)
