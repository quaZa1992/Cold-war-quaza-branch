# IMPERIA COLD WAR — Explicit retirement of the previous France 1970 tree.
"""Archive the exact former runtime before removing its isolated files and hooks."""
from pathlib import Path
import hashlib
import json
import os
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ARCHIVE_ROOT = Path('E:/MDColdWar_Backups/Codex_Test_Archives').resolve()
ARCHIVE = ARCHIVE_ROOT / 'france_tree_retired_20261028.zip'
manifest = json.loads((ROOT / 'tools/france_1970/manifest.json').read_text(encoding='utf-8-sig'))
runtime = list(manifest['generated'])
hooks = manifest['hooks']

def contained(p, base):
    p.resolve().relative_to(base.resolve())
    if p.is_junction() or p.is_symlink():
        raise RuntimeError(f'Refusing junction/symlink: {p}')

if sys.argv[1:] == ['--archive']:
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)
    contained(ARCHIVE, ARCHIVE_ROOT)
    if ARCHIVE.exists():
        raise RuntimeError('Archive already exists; do not overwrite a retained snapshot')
    files = [ROOT / s for s in runtime + hooks]
    for folder, dirs, names in os.walk(ROOT / 'tools/france_1970', followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(folder)/d).is_junction() and not (Path(folder)/d).is_symlink() and d != '__pycache__']
        files.extend(Path(folder)/n for n in names)
    hashes = {}
    with zipfile.ZipFile(ARCHIVE, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:
            contained(p, ROOT)
            name = p.relative_to(ROOT).as_posix()
            blob = p.read_bytes()
            hashes[name] = hashlib.sha256(blob).hexdigest()
            z.writestr(name, blob)
        z.writestr('RETIREMENT_NOTICE.md', 'IMPERIA COLD WAR\n\nPrevious France tree retired on explicit user instruction, 28 October 2026. Sources: prior project runtime and generator. Original MD credits and licences remain separate; individual artwork authors and separate permissions are unknown. Archived bytes are unmodified. This snapshot grants no new rights.\n')
    with zipfile.ZipFile(ARCHIVE) as z:
        assert all(hashlib.sha256(z.read(k)).hexdigest() == h for k,h in hashes.items())
    (OUT/'retirement_archive.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','archive':str(ARCHIVE),'sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),'files':hashes},indent=2),encoding='utf-8')
    print(f'Archived and byte-verified {len(hashes)} files: {ARCHIVE}')
elif sys.argv[1:] == ['--retire']:
    record = json.loads((OUT/'retirement_archive.json').read_text(encoding='utf-8'))
    assert str(ARCHIVE) == record['archive']
    assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == record['sha256']
    for name in runtime + hooks:
        p = ROOT/name
        contained(p,ROOT)
        assert hashlib.sha256(p.read_bytes()).hexdigest() == record['files'][name], name
    edits = {}
    p = ROOT/hooks[0]
    old = p.read_text(encoding='utf-8-sig')
    new = old.replace('\t\tload_focus_tree = COLDWAR_FRA_1970_focus\n\t\tCOLDWAR_FRA_1970_initialize = yes','\t\t# IMPERIA COLD WAR — Previous France tree retired pending replacement approval.\n\t\tmdcw_load_1970_fallback_tree = yes')
    assert new != old
    edits[p] = '# IMPERIA COLD WAR — France 1970 history and retired-tree integration.\n' + new
    p = ROOT/hooks[1]
    old = p.read_text(encoding='utf-8-sig')
    start = old.index('\t# IMPERIA COLD WAR — France 1970 authored tree fallback routing.')
    end = old.index('\n\t}\n',start)+4
    new = old[:start] + old[end:]
    new = new.replace('\t\t\t\t\t# IMPERIA COLD WAR — France authored 1970 tree exemption.\n\t\t\t\t\tAND = { original_tag = FRA IMP_is_1970_scenario = yes }\n','')
    assert 'COLDWAR_FRA_' not in new
    edits[p] = '# IMPERIA COLD WAR — France retired-tree fallback cleanup.\n' + new
    p = ROOT/hooks[2]
    old = p.read_text(encoding='utf-8-sig')
    target = '\t# IMPERIA COLD WAR — France 1970 exact subparty programme refresh delegation.\n\tif = {\n\t\tlimit = { IMP_is_1970_scenario = yes }\n\t\tCOLDWAR_FRA_refresh_programmes = yes\n\t}\n\telse = {'
    assert target in old
    new = old.replace(target,'\t# IMPERIA COLD WAR — Modern programme callback excludes the 1970 campaign.\n\tif = {\n\t\tlimit = { NOT = { IMP_is_1970_scenario = yes } }')
    assert 'COLDWAR_FRA_' not in new
    edits[p] = '# IMPERIA COLD WAR — France retired-tree callback integration.\n' + new
    # All exact edit preconditions and archive bytes have been checked before mutation.
    for p, text in edits.items():
        p.write_text(text, encoding='utf-8',newline='\n')
    for name in runtime:
        p = ROOT/name
        contained(p,ROOT)
        p.unlink()
    (OUT/'retirement_result.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','removed_runtime_files':runtime,'updated_hooks':hooks,'archive':str(ARCHIVE),'new_concept_installed':False,'fallback':'mdcw_1970_generic_focus','old_save_migration':'Not provided; old live saves require a separate migration or archived runtime.'},indent=2),encoding='utf-8')
    print(f'Removed {len(runtime)} previous runtime files and detached three hooks. New starts use the existing generic 1970 fallback.')
else:
    raise SystemExit('Use --archive or --retire')
