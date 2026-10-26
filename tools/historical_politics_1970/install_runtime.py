# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Build, validate and optionally install the historical-politics runtime.

Shared inputs are hashed before and after generation and checked again before
replacement. This prevents a stale stage from reverting concurrent mod work.
Every changed destination is recoverable; portrait generation is separate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import uuid
from pathlib import Path

from build import Builder, HERE, ROOT, load_catalog
from validate import validate


SHARED = (
    'common/scripted_effects/00_leader_setup_scripted_effects.txt',
    'common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt',
    'common/scripted_effects/ISR70_effects.txt',
    'common/scripted_effects/COLDWAR_SPR_politics.txt',
    'common/scripted_effects/USA_1970_scripted_effects.txt',
    'common/scripted_effects/COLDWAR_EGY_1970_roster_effects.txt',
    'common/scripted_guis/00_MD_politicsview_scripted_guis.txt',
    'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt',
)
DATA = ('data/world.json', 'portrait_manifest.json', 'party_icon_manifest.json',
        'special_portraits.json', 'party_inventory.json', 'party_md_reference.json')

# Exact outputs of the validated, now withdrawn decision-based implementation.
# An edited file must never be silently removed on the strength of its name.
RETIRED_OUTPUTS = {
    'common/decisions/categories/mdcw_historical_leadership.txt': 'a8f01f6b99c13af629fd15d9ccc1c06820524468a08a752b0cd15dfb5035e9e0',
    'common/decisions/mdcw_historical_leadership.txt': 'f9d2a4c1a1612733a6e063651f64e5b89922a61ad55d368572590312a1f202fb',
    'common/scripted_effects/mdcw_historical_leadership.txt': 'b02e3ecb590a01f6046e4fa584265fd8945ab8b1cb663c62c954dd1b40d19537',
    'common/scripted_triggers/mdcw_historical_dispatch.txt': '76ec55f8e85e90ed7a6158b03da970908a88636d6f6dfb6020bbf9f365f9b7e0',
    'common/scripted_effects/mdcw_historical_dispatch.txt': '2de62a8853ebc37d67983bc5662bae10690c2fa4fd995e5f4d62a361105bcf41',
}


def digest(path):
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir():
        # Pin glob membership too: new country data/localisation added after
        # snapshot must invalidate a stage built before that file existed.
        members = sorted(child.name + ('/' if child.is_dir() else '') for child in path.iterdir())
        return hashlib.sha256('\n'.join(members).encode('utf-8')).hexdigest()
    return None


def snapshot():
    initial_data = {str(HERE / name): digest(HERE / name) for name in DATA}
    presentation_inputs = [HERE, ROOT / 'localisation/english',
                           ROOT / 'common/scripted_localisation/mdcw_historical_parties.txt',
                           HERE / 'party_presentation.py', HERE / 'capture_party_reference.py']
    presentation_inputs += sorted(HERE.glob('data_party_names_*.json'))
    presentation_inputs += sorted((ROOT / 'localisation/english').glob('*.yml'))
    initial_data.update({str(path): digest(path) for path in presentation_inputs})
    paths = [ROOT / name for name in SHARED]
    # Native country selectors become build inputs when extending MD's pools.
    paths += sorted((ROOT / 'common/scripted_effects').glob('*_political_leaders.txt'))
    # Exact historical starter spellings are aliases for incumbent matching.
    paths += sorted((ROOT / 'history/countries').glob('*.txt'))
    countries = json.loads((HERE / 'data/world.json').read_text(encoding='utf-8-sig'))['countries']
    paths += [ROOT / 'common/scripted_effects' / (row['tag'] + '_political_leaders.txt')
              for row in countries]
    paths += [ROOT / name for name in RETIRED_OUTPUTS]
    paths += [ROOT / 'localisation/english/0_political_system_l_english.yml']
    paths += [HERE / name for name in DATA]
    paths += presentation_inputs
    paths += [HERE / name for name in ('build.py', 'dispatch.py', 'leader_segments.py',
              'special_successors.py', 'sov_egy_successors.py', 'native_retirement.py',
              'special_portraits.py', 'validate.py', 'install_runtime.py')]
    # Assets are build inputs too. Pin content, including absent paths, so a
    # concurrent portrait/icon replacement cannot invalidate completed QA.
    manifest = json.loads((HERE / 'portrait_manifest.json').read_text(encoding='utf-8'))
    icons = json.loads((HERE / 'party_icon_manifest.json').read_text(encoding='utf-8'))
    assets = set()
    for record in manifest.values():
        if isinstance(record, dict) and record.get('portrait'):
            assets.add(record['portrait'])
    for record in icons.values():
        if record.get('texture_path'):
            assets.add(record['texture_path'])
    for name in SHARED:
        path = ROOT / name
        if path.is_file():
            assets.update(re.findall(r'\bpicture\s*=\s*"([^"\r\n]+)"',
                                     path.read_text(encoding='utf-8-sig')))
    paths += [inside(ROOT, name) for name in assets]
    result = {str(path): digest(path) for path in paths}
    if any(result[path] != value for path, value in initial_data.items()):
        raise RuntimeError('Manifest/data changed while collecting build inputs; rebuild required')
    return result


def unchanged(expected):
    changed = [path for path, value in expected.items() if digest(Path(path)) != value]
    if changed:
        raise RuntimeError('Inputs changed concurrently; rebuild required: ' + ', '.join(changed))


def inside(root, name):
    rel = Path(name.replace('\\', '/'))
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError(name)
    path = (root / rel).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(name)
    return path


def run(output, install=False):
    output = output.resolve()
    if output.is_relative_to(ROOT.resolve()):
        raise ValueError('Build/recovery directory must be outside the loaded mod')
    before = snapshot()
    builder = Builder(load_catalog())
    report = builder.build()
    unchanged(before)
    stage = output / 'staged'
    for name, value in builder.outputs.items():
        path = inside(stage, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding='utf-8', newline='\n')
    staged_files = {str(path.relative_to(stage)).replace('\\', '/')
                    for path in stage.rglob('*') if path.is_file()}
    unexpected = staged_files - set(builder.outputs)
    if unexpected:
        raise RuntimeError('Stale/unplanned staged files; use a fresh build directory: ' + ', '.join(sorted(unexpected)))
    qa = validate(stage, HERE / 'data/world.json', HERE / 'portrait_manifest.json', ROOT)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'build_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (output / 'validation.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    (output / 'source_snapshot.json').write_text(json.dumps(before, indent=2), encoding='utf-8')
    if not qa['ok']:
        raise RuntimeError('Runtime validation failed; inspect validation.json')
    unchanged(before)
    targets = {name: digest(inside(ROOT, name)) for name in builder.outputs}
    retired = {}
    for name, expected in RETIRED_OUTPUTS.items():
        if name in builder.outputs:
            raise RuntimeError('Build resurrected withdrawn runtime file: ' + name)
        actual = digest(inside(ROOT, name))
        if actual is not None:
            if actual != expected:
                raise RuntimeError('Withdrawn generated file has independent edits; preserve it for review: ' + name)
            retired[name] = actual
    result = {'installed': False, 'countries': report['countries'],
              'ready_leaders': report['ready_leaders'],
              'pending_leaders': len(report['pending_leaders']),
              'pending_native_portraits': len(report['pending_native_portraits']),
              'files': report['files'], 'retired_files': list(retired), 'recovery': None}
    if not install:
        return result
    recovery = output / ('runtime_recovery_' + uuid.uuid4().hex)
    recovery.mkdir()
    changed = [name for name, old_hash in targets.items() if old_hash != report['files'][name]]
    all_targets = {**targets, **retired}
    for name in changed + list(retired):
        if all_targets[name] is not None:
            dest = inside(recovery, name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(inside(ROOT, name), dest)
            if digest(dest) != all_targets[name]:
                raise RuntimeError('Destination changed during recovery snapshot: ' + name)
    (recovery / 'before.json').write_text(json.dumps(all_targets, indent=2), encoding='utf-8')
    unchanged(before)
    written = []
    removed = []
    try:
        for name in changed:
            target = inside(ROOT, name)
            if digest(target) != targets[name]:
                raise RuntimeError('Destination changed concurrently: ' + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_suffix(target.suffix + '.mdcw_install_tmp')
            shutil.copy2(inside(stage, name), temporary)
            if digest(temporary) != report['files'][name]:
                raise RuntimeError('Staged output changed: ' + name)
            if digest(target) != targets[name]:
                temporary.unlink()
                raise RuntimeError('Destination changed concurrently: ' + name)
            temporary.replace(target)
            written.append(name)
        for name, expected in retired.items():
            target = inside(ROOT, name)
            if digest(target) != expected:
                raise RuntimeError('Withdrawn file changed concurrently: ' + name)
            target.unlink()
            removed.append(name)
        for name in builder.outputs:
            if digest(inside(ROOT, name)) != report['files'][name]:
                raise RuntimeError('Installed output changed: ' + name)
        for name in RETIRED_OUTPUTS:
            if inside(ROOT, name).exists():
                raise RuntimeError('Withdrawn runtime file remains loaded: ' + name)
        result.update(installed=True, changed_files=len(changed), removed_files=len(removed), recovery=str(recovery))
        (output / 'install_report.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    except Exception:
        for name in reversed(removed):
            target = inside(ROOT, name)
            try:
                # Exclusive creation preserves an independent replacement.
                with target.open('xb') as dest, inside(recovery, name).open('rb') as source:
                    shutil.copyfileobj(source, dest)
            except FileExistsError:
                pass
        for name in reversed(written):
            target = inside(ROOT, name)
            if digest(target) != report['files'][name]:
                continue  # Do not overwrite an independent edit made after our write.
            original = inside(recovery, name)
            if targets[name] is None:
                if digest(target) == report['files'][name]:
                    target.unlink()
            else:
                temporary = target.with_suffix(target.suffix + '.mdcw_rollback_tmp')
                shutil.copy2(original, temporary)
                if digest(target) == report['files'][name]:
                    temporary.replace(target)
                else:
                    temporary.unlink()
        raise
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    report = run(args.output, args.install)
    print(json.dumps({key: value for key, value in report.items() if key != 'files'}))


if __name__ == '__main__':
    main()
