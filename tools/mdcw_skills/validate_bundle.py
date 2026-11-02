# IMPERIA COLD WAR — Validate portable skill packages, references and installation hashes.
"""Run the official skill validator plus package integrity checks, without installing."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MARKER = '# IMPERIA COLD WAR — '


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(installed: bool = False) -> dict:
    manifest = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
    destination = Path(manifest['destination']).resolve()
    codex_skills = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    assert destination == codex_skills.resolve(), 'Unexpected installation root'
    sys.path.insert(0, str(ROOT / 'tools/preference_updates/20261023/validator_dependencies'))
    import yaml
    module_path = codex_skills / '.system/skill-creator/scripts/quick_validate.py'
    spec = importlib.util.spec_from_file_location('mdcw_official_quick_validate', module_path)
    assert spec and spec.loader
    official = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(official)
    errors = []
    official_results = []
    manifest_paths = {entry['path'] for entry in manifest['files']}
    actual_sources = {p.relative_to(HERE).as_posix() for parent in ['skills', 'updates']
                      for p in (HERE / parent).rglob('*') if p.is_file()}
    expected_sources = {entry['source'] for entry in manifest['files']}
    if actual_sources != expected_sources:
        errors.append('Prepared package contains missing or unmanifested files')
    for entry in manifest['files']:
        source = (HERE / entry['source']).resolve()
        target = (destination / entry['path']).resolve()
        if not source.is_relative_to(HERE) or not target.is_relative_to(destination):
            errors.append('Unsafe manifest path: ' + entry['path'])
            continue
        if digest(source) != entry['after_sha256']:
            errors.append('Changed package file: ' + entry['source'])
        if installed and (not target.is_file() or digest(target) != entry['after_sha256']):
            errors.append('Installed hash mismatch: ' + entry['path'])
        data = source.read_bytes()
        if data.startswith(b'\xef\xbb\xbf'):
            errors.append('Skill package unexpectedly has a BOM: ' + entry['source'])
        text = data.decode('utf-8')
        body = text
        if source.name == 'SKILL.md':
            parts = text.split('---', 2)
            if len(parts) != 3:
                errors.append('Invalid frontmatter: ' + entry['source'])
                continue
            body = parts[2].lstrip('\r\n')
            fm = yaml.safe_load(parts[1])
            if fm.get('name') != Path(entry['path']).parts[0]:
                errors.append('Name/folder mismatch: ' + entry['source'])
            if fm.get('metadata', {}).get('project') != 'IMPERIA COLD WAR':
                errors.append('Project metadata missing: ' + entry['source'])
        if not body.startswith(MARKER):
            errors.append('First project marker missing: ' + entry['source'])
        if source.suffix == '.md':
            for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
                if re.match(r'^[a-z][a-z0-9+.-]*:', link, flags=re.I) or link.startswith('#'):
                    continue
                rel = link.split('#', 1)[0]
                referenced = (source.parent / rel).resolve()
                if referenced.is_file():
                    continue
                # A minimal update can reference unchanged files in its installed skill.
                installed_ref = (target.parent / rel).resolve()
                if entry['kind'] == 'update' and installed_ref.is_relative_to(destination) and installed_ref.is_file():
                    continue
                errors.append('Broken local link: ' + entry['source'] + ' -> ' + rel)
    covered = []
    for record in manifest['skills']:
        name = record['skill']
        folder = destination / name if installed else HERE / ('skills' if record['kind'] == 'new' else 'updates') / name
        valid, message = official.validate_skill(folder)
        official_results.append({'skill': name, 'passed': valid, 'message': message})
        if not valid:
            errors.append(name + ': ' + message)
        covered.extend(record['upstream_skills'])
        if record['kind'] == 'new':
            ui = yaml.safe_load((folder / 'agents/openai.yaml').read_text(encoding='utf-8'))
            interface = ui['interface']
            if not 25 <= len(interface['short_description']) <= 64:
                errors.append(name + ': Invalid UI description length')
            if '$' + name not in interface['default_prompt']:
                errors.append(name + ': Prompt lacks the actual skill name')
            if ui.get('policy', {}).get('allow_implicit_invocation', True) is not True:
                errors.append(name + ': Automatic discovery unexpectedly disabled')
    inventory = json.loads((HERE / 'upstream_inventory.json').read_text(encoding='utf-8'))
    upstream_skills = sorted(Path(e['path']).parts[2] for e in inventory['entries'] if e['path'].endswith('/SKILL.md'))
    if sorted(covered) != upstream_skills:
        errors.append('Upstream skill coverage mismatch')
    # These are core operational dependencies of the adapters, checked as paths rather than assumed commands.
    dependencies = ['AGENTS.md', 'common/scripted_effects/00_money_system.txt',
                    'tools/multiplayer_quality/audit.py', 'tools/multiplayer_quality/native_probe.py',
                    'tools/preference_updates/20261023/validator_dependencies/yaml/__init__.py']
    missing_dependencies = [p for p in dependencies if not (ROOT / p).is_file()]
    errors += ['Missing dependency: ' + p for p in missing_dependencies]
    return {'project': 'IMPERIA COLD WAR', 'mode': 'installed' if installed else 'prepared',
            'upstream_commit': manifest['upstream_commit'], 'upstream_skills_covered': len(covered),
            'new_skills': sum(s['kind'] == 'new' for s in manifest['skills']),
            'updated_skills': sum(s['kind'] == 'update' for s in manifest['skills']),
            'package_files': len(manifest_paths), 'official_validation': official_results,
            'dependencies_checked': dependencies, 'errors': errors, 'passed': not errors}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installed', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = validate(args.installed)
    if args.out:
        target = args.out.resolve()
        if not target.is_relative_to(HERE):
            parser.error('Validation output must stay within the skill bundle directory')
        target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k not in {'official_validation', 'dependencies_checked'}}, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
