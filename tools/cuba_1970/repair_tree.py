# IMPERIA COLD WAR — Bounded Cuba layout and medical continuation integration.
"""Capture the canonical compiler; validate the complete diff before writing."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values


def main():
    backup_record = json.loads((HERE/'LAYOUT_REPAIR_BACKUP.json').read_text(encoding='utf8'))
    backup = ROOT/backup_record['backup']
    spec = importlib.util.spec_from_file_location('cuba_layout_repair_compiler', HERE/'compile.py')
    compiler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compiler)
    captured = {}

    def capture(rel, text, localisation=False):
        assert not localisation
        captured[rel] = compiler.HEADER + compiler.format_code(text)

    compiler.emit = capture
    compiler.make_tree()
    compiler.make_effects()
    assert set(captured) == {
        'common/national_focus/COLDWAR_CUB_1970_focus.txt',
        'common/scripted_triggers/COLDWAR_CUB_1970_triggers.txt',
        'common/scripted_effects/COLDWAR_CUB_1970_effects.txt',
    }
    medical = {'COLDWAR_CUB_medical_brigades', 'COLDWAR_CUB_retain_doctors'}
    staged, records = {}, []
    for rel, new_text in captured.items():
        old_bytes = (backup/rel).read_bytes()
        old, new, live = (parse(text) for text in (
            old_bytes.decode('utf-8'), new_text, (ROOT/rel).read_text(encoding='utf8')))
        assert live == old or live == new, ('Preserve unexpected live changes', rel)
        if '/national_focus/' in rel:
            ta, tb = first(old, 'focus_tree'), first(new, 'focus_tree')
            aa = {first(n, 'id'): n for n in values(ta, 'focus')}
            bb = {first(n, 'id'): n for n in values(tb, 'focus')}
            assert aa.keys() == bb.keys() and len(aa) == 120
            for key in aa:
                fields = {'x', 'y', 'relative_position_id'} | ({'prerequisite'} if key in medical else set())
                assert [r for r in aa[key] if r[0] not in fields] == [r for r in bb[key] if r[0] not in fields], ('Unexpected focus semantics', key)
                if key in medical:
                    assert [values(p, 'focus') for p in values(bb[key], 'prerequisite')] == [['COLDWAR_CUB_rural_clinics', 'COLDWAR_CUB_teaching_hospitals']]
            assert [r for r in ta if r[0] != 'focus'] == [r for r in tb if r[0] != 'focus']
        elif '/scripted_triggers/' in rel:
            aa, bb = ({k: v for k, _, v in ast} for ast in (old, new))
            assert aa.keys() == bb.keys()
            changed = {k for k in aa if aa[k] != bb[k]}
            assert changed == {'COLDWAR_CUB_can_medical_brigades', 'COLDWAR_CUB_can_retain_doctors'}, changed
            predecessor = parse('OR = { has_country_flag = COLDWAR_CUB_rural_clinics_applied has_country_flag = COLDWAR_CUB_teaching_hospitals_applied }')[0]
            for key in changed:
                original = first(aa[key], 'hidden_trigger')
                repaired = list(first(bb[key], 'hidden_trigger'))
                repaired.remove(predecessor)
                assert repaired == original
                assert [r for r in aa[key] if r[0] != 'hidden_trigger'] == [r for r in bb[key] if r[0] != 'hidden_trigger']
        else:
            assert old == new, 'Reward effects changed during a layout repair'
        if (ROOT/rel).read_text(encoding='utf8') != new_text:
            staged[rel] = new_text
        records.append(dict(path=rel, before_sha256=hashlib.sha256(old_bytes).hexdigest(), sha256=hashlib.sha256(new_text.encode('utf8')).hexdigest()))

    # IMPERIA COLD WAR — All checks above pass before any runtime file is written.
    for rel, text in staged.items():
        (ROOT/rel).write_text(text, encoding='utf8', newline='\n')
    hashes = {r['path']: r['sha256'] for r in records}
    manifest_path = HERE/'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    for entry in manifest:
        entry['project'] = 'IMPERIA COLD WAR'
        if entry['path'] in hashes:
            entry['sha256'] = hashes[entry['path']]
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf8')
    manifest_path = HERE/'integration_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    manifest['project'] = 'IMPERIA COLD WAR'
    for entry in manifest['owned']:
        if entry['path'] in hashes:
            entry['sha256'] = hashes[entry['path']]
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf8')
    report = dict(project='IMPERIA COLD WAR', backup=backup_record['backup'], focuses=120,
                  changed_runtime_files=[r['path'] for r in records if r['before_sha256'] != r['sha256']],
                  written_this_run=list(staged), files=records,
                  rewards_costs_exclusions_and_consent_unchanged=True,
                  medical_or_prerequisites_restored=True)
    (HERE/'LAYOUT_REPAIR_INTEGRATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
