# IMPERIA CW — Cold War: shared Colonial Affairs compilation and bounded integration.
"""Rebuild only this feature; preserve unrelated country, economy and UI edits."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BEGIN = '\t# COLDWAR COLONIAL EXPENSE BEGIN'
END = '\t# COLDWAR COLONIAL EXPENSE END'


def module(name):
    spec = importlib.util.spec_from_file_location('colonial_' + name, HERE / (name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def integrate_money():
    path = ROOT / 'common/scripted_effects/00_money_system.txt'
    before = path.read_bytes()
    if before.startswith(b'\xef\xbb\xbf'):
        raise RuntimeError('Native economy file has a BOM; resolve the existing encoding problem first.')
    source = before.decode('utf-8')
    newline = '\r\n' if '\r\n' in source else '\n'
    text = source.replace('\r\n', '\n')
    hook = '''\t# IMPERIA CW — Cold War: live colonial administrations enter native weekly expenses.
\t# COLDWAR COLONIAL EXPENSE BEGIN
\tif = {
\t\tlimit = { IMP_is_1970_scenario = yes }
\t\tCOLDWAR_COL_recalculate_budget = yes
\t\tadd_to_variable = { additional_expenses_rate = COLDWAR_COL_total_weekly_cost }
\t}
\tif = {
\t\tlimit = { COLDWAR_COL_contacts_scenario = yes }
\t\tCOLDWAR_COL_domestic_budget = yes
\t\tadd_to_variable = { additional_expenses_rate = COLDWAR_COL_domestic_weekly_cost }
\t}
\t# COLDWAR COLONIAL EXPENSE END'''
    marker = '\t# IMPERIA CW — Cold War: live colonial administrations enter native weekly expenses.\n' + BEGIN
    if BEGIN in text:
        if marker not in text or text.count(BEGIN) != 1 or text.count(END) != 1:
            raise RuntimeError('Ambiguous existing colonial finance hook')
        start = text.index(marker)
        finish = text.index(END, start) + len(END)
        text = text[:start] + hook + text[finish:]
    else:
        anchor = '\tadd_to_variable = { additional_expenses_rate = total_subsidies_out }'
        if text.count(anchor) != 1:
            raise RuntimeError('Native weekly-expense entry moved; inspect before integration')
        text = text.replace(anchor, anchor + '\n\n' + hook, 1)
    result = text.replace('\n', newline).encode('utf-8')
    if result != before:
        path.write_bytes(result)


def integrate_sahara():
    """Keep the prior standalone spirit compatible with the shared replacement."""
    path = ROOT / 'common/dynamic_modifiers/COLDWAR_SAHARA_1970.txt'
    if not path.exists():
        return
    data = path.read_bytes()
    if data.startswith(b'\xef\xbb\xbf'):
        raise RuntimeError('Legacy Sahara script must not have a BOM')
    text = data.decode('utf-8').replace('\r\n', '\n')
    if 'NOT = { has_state_flag = COLDWAR_COL_registered }' not in text:
        anchor = '\t\thas_state_flag = COLDWAR_SAHARA_1970_colonial_question'
        if text.count(anchor) != 1:
            raise RuntimeError('Legacy Sahara activation guard moved')
        text = text.replace(anchor, anchor + '\n\t\t# IMPERIA CW — Cold War: shared colonial administration replaces this local spirit.\n\t\tNOT = { has_state_flag = COLDWAR_COL_registered }', 1)
        path.write_text(text, encoding='utf-8')


def merge_localisation(runtime_text):
    extras = json.loads((HERE / 'ui_localisation.json').read_text(encoding='utf-8'))
    pattern = re.compile(r'^\s*([^\s:#]+):\d*\s*"(.*)"\s*$', re.M)
    entries = dict(pattern.findall(runtime_text))
    # UI-only captions may specialize neutral headings; mechanical tooltips belong
    # to runtime and must not be replaced by an old visual demonstration.
    for key, value in extras.items():
        if key in entries and key.endswith('_tt') and entries[key] != value:
            continue
        entries[key] = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return 'l_english:\n # IMPERIA CW — Cold War: Colonial Affairs and cabinet dossier.\n' + ''.join(' ' + key + ':0 "' + value + '"\n' for key, value in sorted(entries.items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-art', action='store_true', help='Keep existing native art; rebuild scripts and localisation only.')
    args = parser.parse_args()
    registry = json.loads((HERE / 'registry.json').read_text(encoding='utf-8'))
    if not args.no_art:
        module('ui').build()
    elif not (HERE / 'ui_localisation.json').exists():
        raise RuntimeError('Build the dossier art once before using --no-art')
    files = module('runtime').build(ROOT, registry)
    contacts_localisation = module('contacts').build(files, registry['administrations'])
    loc = 'localisation/english/COLDWAR_colonial_affairs_l_english.yml'
    files[loc] = merge_localisation(files[loc])
    # New shared contact mechanics own their numeric tooltips.
    for key, value in contacts_localisation.items():
        line = ' ' + key + ':0 "' + value.replace('"', '\\"').replace('\n', '\\n') + '"'
        pattern = re.compile(r'^\s*' + re.escape(key) + r':0 "[^\n]*"$', re.M)
        if pattern.search(files[loc]):
            files[loc] = pattern.sub(lambda _: line, files[loc])
        else:
            files[loc] += line + '\n'
    hashes = {}
    for rel, text in files.items():
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            raise RuntimeError('Invalid output path: ' + rel)
        blob = text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
        if not rel.endswith('.yml') and blob.startswith(b'\xef\xbb\xbf'):
            raise RuntimeError('Script BOM: ' + rel)
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blob)
        hashes[rel] = hashlib.sha256(blob).hexdigest()
    integrate_money()
    integrate_sahara()
    retired_changes = module('retire_ira').run(ROOT)
    ui_paths = [
        'interface/COLDWAR_colonial_affairs.gui',
        'interface/COLDWAR_colonial_affairs.gfx',
        'common/scripted_guis/COLDWAR_colonial_affairs_gui.txt',
        'common/scripted_localisation/COLDWAR_colonial_affairs_gui.txt',
    ]
    for rel in ui_paths:
        hashes[rel] = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
    for path in sorted((ROOT / 'gfx/interface/coldwar_colonial').glob('*.dds')):
        hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(
        schema_version=1, administrations=len(registry['administrations']),
        powers=sorted({r['power'] for r in registry['administrations']}),
        generated=hashes,
        bounded_shared_integrations=['common/scripted_effects/00_money_system.txt', 'common/dynamic_modifiers/COLDWAR_SAHARA_1970.txt'],
        engine_tested=False,
        retired_ira_changes=sorted(set(retired_changes) | set(json.loads((HERE/'manifest.json').read_text(encoding='utf-8')).get('retired_ira_changes', []))) if (HERE/'manifest.json').exists() else retired_changes,
    )
    (HERE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'administrations':manifest['administrations'], 'powers':manifest['powers'], 'outputs':len(hashes)}))


if __name__ == '__main__':
    main()
