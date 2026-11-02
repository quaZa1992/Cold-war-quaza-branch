# IMPERIA COLD WAR — Static checks of the unexecuted private native fixture.
"""These tests do not prepare E: directories or launch Hearts of Iron IV."""
from pathlib import Path
import importlib.util
import re
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import stat

import compile as compiler
import runtime_native_probe as probe


class ProbePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload=compiler.build()
        cls.fixture=probe.fixture(cls.payload)

    def test_import_has_no_profile_write_scan_or_process_launch(self):
        spec=importlib.util.spec_from_file_location('isolated_probe_import_check',Path(probe.__file__))
        module=importlib.util.module_from_spec(spec)
        with patch('subprocess.Popen',side_effect=AssertionError('Import launched process')),patch.object(Path,'write_bytes',side_effect=AssertionError('Import wrote file')),patch('os.scandir',side_effect=AssertionError('Import scanned source')):
            spec.loader.exec_module(module)

    def test_fixture_parses_and_baseline_precedes_synthetic_values(self):
        rows=probe._read_script(self.fixture['events'])
        events=[v for k,_,v in rows if k=='country_event']
        self.assertEqual(len(events),5)
        self.assertEqual(len(self.fixture['checks']),28)
        for event in events[:2]:
            for key,_,value in probe._walk(event):
                if key=='set_variable' and isinstance(value,list):
                    self.assertNotIn(value[0][0],('gdp_total','treasury','debt','int_investments','total_unemployed_k'))
        for focus in self.fixture['workforce_actions']:
            self.assertIn(probe.action_call(self.payload,focus),self.fixture['events'])
        self.assertTrue(all(row['status']=='PASS_SOURCE' and row['slots']==row['levels'] for row in self.fixture['slot_source']))
        self.assertIn('country_event = { id = ICW_ISR2_NATIVE.5 days = 4 }',self.fixture['events'])

    def test_event_instrumentation_changes_only_logs_not_offer_mechanics(self):
        source=self.payload['files']['events/ISR2_bilateral_events.txt'].decode('utf-8')
        changed,ids=probe.instrument_recipient_events(source)
        pattern=r'\nimmediate = \{\nlog = "ICW_ISR2_NATIVE ARRIVAL ISR2_bilateral\.\d+ tag=\[THIS.GetTag\]"\n\}\n'
        restored,count=re.subn(pattern,'',changed)
        self.assertEqual(count,18);self.assertEqual(restored,source)
        self.assertEqual(len(ids),18)
        probe._read_script(changed)

    def test_paths_reject_fixture_escape(self):
        base=probe.RUNTIME/'not_created_test'/'profile'/'fixture'
        for relative in ('../real_saves/a.txt','C:/Users/Enes/settings.txt','/absolute'):
            with self.assertRaises(ValueError):probe.destination(base,relative)
        self.assertEqual(probe.destination(base,'gfx/interface/goals/ISR2/test.dds'),base/'gfx/interface/goals/ISR2/test.dds')

    def test_trace_changes_only_logging_without_call_reordering(self):
        files,receipts=probe.instrument_startup_calls(self.payload['files'])
        self.assertEqual(set(files),set(self.payload['files']))
        def without_logs(rows):
            result=[]
            for key,op,value in rows:
                if key=='log':continue
                if isinstance(value,list):
                    value=without_logs(value)
                    if key=='if' and all(x[0]=='limit' for x in value):continue
                result.append((key,op,value))
            return result
        for path,receipt in receipts.items():
            before=probe._read_script(self.payload['files'][path].decode('utf-8'))
            after=probe._read_script(files[path].decode('utf-8'))
            self.assertEqual(without_logs(before),without_logs(after),path)
            self.assertNotEqual(receipt['source_sha256'],receipt['instrumented_sha256'])
        self.assertIn('ISR2_initialize',{name for r in receipts.values()for name in r['functions']})

    def test_reuse_rejects_uncovered_base_changes_and_keeps_baseline_separate(self):
        self.assertEqual(probe.uncovered_base_changes({'a':'new','b':'same'},{'a':'old','b':'same'},{'a':b'override'}),[])
        self.assertEqual(probe.uncovered_base_changes({'a':'new','b':'same'},{'a':'old','b':'same'},{}),['a'])
        control=probe.baseline_fixture()
        probe._read_script(control['events']);probe._read_script(control['onactions'])
        self.assertIsNone(control['event_arrival'])
        self.assertNotIn('ISR2_is_scenario',control['events'])
        self.assertEqual(len(control['checks']),3)

    def test_five_fresh_base_texts_freeze_exactly_but_removals_binary_and_reparse_refuse(self):
        paths=['common/decisions/USA_kissinger.txt','common/scripted_effects/USA_kissinger.txt',
            'history/countries/KPI - Israel.txt','history/countries/KPS - South.txt','history/countries/KPT - Trucial.txt']
        contents={p:('# IMPERIA COLD WAR: private source fixture '+str(i)+'\r\na = yes\n').encode('utf-8') for i,p in enumerate(paths)}
        current={p:probe.sha(raw)for p,raw in contents.items()}
        frozen={p:'old_hash'for p in paths[:-1]}  # Includes a genuinely added file.
        def read(path):return contents[path.relative_to(probe.ROOT).as_posix()]
        metadata=SimpleNamespace(st_file_attributes=0)
        with patch.object(Path,'stat',return_value=metadata),patch.object(Path,'is_symlink',return_value=False),patch.object(Path,'read_bytes',read),patch.object(Path,'write_bytes',side_effect=AssertionError('Base delta wrote source')):
            self.assertEqual(probe.freeze_base_delta(current,frozen,{}),contents)
            owned={paths[0]:b'canonical_override'}
            self.assertEqual(set(probe.freeze_base_delta(current,frozen,owned)),set(paths[1:]))
            with self.assertRaises(ValueError):probe.freeze_base_delta({p:d for p,d in current.items()if p!=paths[0]},frozen,{})
            contents[paths[0]]=b'bad\0binary';current[paths[0]]=probe.sha(contents[paths[0]])
            with self.assertRaises(ValueError):probe.freeze_base_delta(current,frozen,{})
        with self.assertRaises(ValueError):probe.freeze_base_delta({'map/provinces.bmp':'new'},{'map/provinces.bmp':'old'},{})
        with patch.object(Path,'stat',return_value=SimpleNamespace(st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)):
            with self.assertRaises(ValueError):probe.freeze_base_delta({paths[0]:'new'},{paths[0]:'old'},{})


if __name__=='__main__':unittest.main(verbosity=2)
