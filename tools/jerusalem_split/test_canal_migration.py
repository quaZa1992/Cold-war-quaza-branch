# IMPERIA COLD WAR — Protect independent map additions from legacy canal migration.
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / '.fixtures'
SPEC = importlib.util.spec_from_file_location('israel_canal_migration', ROOT / 'tools/israel_1970/policy_map.py')
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)
ORIGINAL = json.loads((ROOT / 'tools/israel_1970/policy_map_source.json').read_text())['original_state_214']


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        FIXTURES.mkdir(exist_ok=True)

    def prepare(self, directory, *, legacy=False, cayo=False):
        root = Path(directory).resolve()
        assert root.parent == FIXTURES.resolve() and not root.is_junction() and not root.is_symlink()
        (root / 'history/states').mkdir(parents=True)
        (root / 'map').mkdir()
        (root / 'history/states/214-Suez.txt').write_text(ORIGINAL, encoding='utf-8')
        if legacy:
            (root / 'history/states/1252-Suez Canal.txt').write_text('# Narrow canal district.\nstate = { id = 1252 }', encoding='utf-8')
        if cayo:
            (root / 'history/states/1252-Cayo Blanco del Sur.txt').write_text('# IMPERIA COLD WAR — Island fixture.\nstate = { id = 1252 provinces = { 16537 } }', encoding='utf-8')
        # Real independent island and new Jerusalem records, plus a canal port.
        records = '214;floating_harbor;3000;10;1000;0;4073\n1252;industrial_complex;1535.50;10;1225.50;0;0\n1253;industrial_complex;3350;9.80;1173;0;0\n'
        (root / 'map/buildings.txt').write_text(records, encoding='utf-8')
        writes = {}

        def write(relative, content, **kwargs):
            writes[relative] = content

        return root, records, writes, write

    def test_reused_island_and_jerusalem_locators_survive_rebuild(self):
        with tempfile.TemporaryDirectory(prefix='icw_canal_', dir=FIXTURES) as directory:
            root, records, writes, write = self.prepare(directory, cayo=True)
            result = POLICY.apply(root, write, None)
            self.assertEqual(writes['map/buildings.txt'], records)
            self.assertTrue((root / 'history/states/1252-Cayo Blanco del Sur.txt').exists())
            self.assertFalse(result['borders_changed'])

    def test_actual_legacy_canal_still_migrates(self):
        with tempfile.TemporaryDirectory(prefix='icw_canal_', dir=FIXTURES) as directory:
            root, records, writes, write = self.prepare(directory, legacy=True)
            POLICY.apply(root, write, None)
            self.assertIn('214;industrial_complex;1535.50;', writes['map/buildings.txt'])
            self.assertIn('1253;industrial_complex;', writes['map/buildings.txt'])
            self.assertFalse((root / 'history/states/1252-Suez Canal.txt').exists())

    def test_collision_refuses_before_writes_or_deletion(self):
        with tempfile.TemporaryDirectory(prefix='icw_canal_', dir=FIXTURES) as directory:
            root, records, writes, write = self.prepare(directory, legacy=True, cayo=True)
            with self.assertRaisesRegex(AssertionError, 'independent map feature'):
                POLICY.apply(root, write, None)
            self.assertEqual(writes, {})
            self.assertTrue((root / 'history/states/1252-Suez Canal.txt').exists())
            self.assertEqual((root / 'map/buildings.txt').read_text(), records)

    def test_unknown_obsolete_file_refuses_before_writes(self):
        with tempfile.TemporaryDirectory(prefix='icw_canal_', dir=FIXTURES) as directory:
            root, records, writes, write = self.prepare(directory)
            category = root / 'common/state_category/ISR70_delta_remainder.txt'
            category.parent.mkdir(parents=True)
            category.write_text('# An independently authored replacement\n', encoding='utf-8')
            with self.assertRaises(AssertionError):
                POLICY.apply(root, write, None)
            self.assertEqual(writes, {})
            self.assertTrue(category.exists())


if __name__ == '__main__':
    unittest.main()
