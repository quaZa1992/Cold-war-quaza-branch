# IMPERIA COLD WAR — Install only validated and hash-checked requested Codex skills.
"""Install this prepared bundle without overwriting concurrent skill changes."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

from validate_bundle import validate

HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    validation = validate()
    if not validation['passed']:
        raise RuntimeError(json.dumps(validation['errors']))
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    destination = Path(manifest['destination']).resolve()
    expected = {entry['path']: entry for entry in manifest['files']}
    for record in manifest['skills']:
        name = record['skill']
        if not name.startswith('mdcw-') or '/' in name or '\\' in name:
            raise RuntimeError('Unexpected skill name: ' + name)
        folder = destination / name
        if folder.is_symlink() or (folder.exists() and folder.is_junction()):
            raise RuntimeError('Refusing a linked destination: ' + str(folder))
        if record['kind'] == 'new' and folder.exists():
            actual = {name + '/' + p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
            packaged = {p for p in expected if p.startswith(name + '/')}
            if actual != packaged:
                raise RuntimeError('Existing skill differs from prepared package: ' + name)
    for entry in manifest['files']:
        source = (HERE / entry['source']).resolve()
        target = destination / entry['path']
        resolved = target.resolve()
        if not source.is_relative_to(HERE) or not resolved.is_relative_to(destination):
            raise RuntimeError('Unsafe path: ' + entry['path'])
        for ancestor in [target, *target.parents]:
            if ancestor == destination:
                break
            if ancestor.is_symlink() or (ancestor.exists() and ancestor.is_dir() and ancestor.is_junction()):
                raise RuntimeError('Refusing linked skill path: ' + str(ancestor))
        current = digest(target) if target.exists() else None
        if current not in {entry['before_sha256'], entry['after_sha256']}:
            raise RuntimeError('Concurrent skill change: ' + entry['path'])
        if digest(source) != entry['after_sha256']:
            raise RuntimeError('Prepared source changed: ' + entry['source'])

    # Use the bundled installer for new skill path validation and copying.
    scripts = destination / '.system/skill-installer/scripts'
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location('mdcw_official_skill_installer', scripts / 'install-skill-from-github.py')
    assert spec and spec.loader
    official = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = official
    spec.loader.exec_module(official)
    backup = HERE / 'install-backups' / datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    changed = []
    for record in manifest['skills']:
        name = record['skill']
        folder = destination / name
        if record['kind'] == 'new' and not folder.exists():
            source = HERE / 'skills' / name
            official._validate_skill(str(source), str(HERE / 'skills'))
            official._copy_skill(str(source), str(folder))
            changed += [e['path'] for e in manifest['files'] if e['path'].startswith(name + '/')]
        elif record['kind'] == 'update':
            for entry in manifest['files']:
                if not entry['path'].startswith(name + '/'):
                    continue
                source = HERE / entry['source']
                target = destination / entry['path']
                if target.exists() and digest(target) == entry['after_sha256']:
                    continue
                if target.exists():
                    saved = backup / entry['path']
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, saved)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                changed.append(entry['path'])
    result = validate(installed=True)
    result['changed_files'] = changed
    result['backup_directory'] = str(backup) if backup.exists() else None
    (HERE / 'installation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    if not result['passed']:
        raise RuntimeError(json.dumps(result['errors']))
    print(json.dumps({'project': 'IMPERIA COLD WAR', 'new_skills': result['new_skills'], 'updated_skills': result['updated_skills'],
                      'changed_files': len(changed), 'installed_files_verified': result['package_files'], 'passed': True}, indent=2))


if __name__ == '__main__':
    main()
