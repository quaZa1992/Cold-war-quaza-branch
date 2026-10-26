# IMPERIA COLD WAR: Audit project source references without relabelling upstream MD or vendor snapshots.
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN_MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
MARKER = re.compile(r'IMPERIA\s+(?:CW|COLD\s*WAR)', re.I)
RUNTIME_ROOTS = ['common', 'events', 'interface', 'history', 'localisation/english', 'gfx']
RUNTIME_SUFFIXES = {'.txt', '.gui', '.gfx', '.yml', '.asset', '.lua'}
SOURCE_SUFFIXES = {'.py', '.ps1', '.js', '.mjs', '.ts', '.sh', '.bat', '.cmd', '.lua'}
EXCLUDED = {'.vendor', 'stage', 'review_stage_latest', 'node_modules', '__pycache__'}


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def standalone_runtime():
    for area in RUNTIME_ROOTS:
        for path in sorted((ROOT / area).rglob('*')):
            if path.suffix in RUNTIME_SUFFIXES and not (MAIN_MD / path.relative_to(ROOT)).exists():
                yield path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fill-known-gaps', action='store_true')
    args = parser.parse_args()
    if not MAIN_MD.is_dir():
        raise SystemExit('Main MD installation is required for the provenance boundary.')
    report = {
        'project': 'IMPERIA COLD WAR',
        'scope': 'Standalone integration scripts absent from installed main MD; owned tools; previously audited shared custom blocks',
        'accepted_markers': ['IMPERIA COLD WAR', 'IMPERIA CW — Cold War'],
        'attribution_policy': 'Integration reference only; existing authorship retained. Unmodified main-MD files and vendor snapshots are excluded.',
        'standalone_runtime_checked': 0,
        'owned_tool_sources_checked': 0,
        'shared_files_checked': 0,
        'missing_runtime': [], 'missing_tools': [], 'missing_shared': [],
        'encoding_errors': [], 'added_markers': [],
    }
    for path in standalone_runtime():
        report['standalone_runtime_checked'] += 1
        blob = path.read_bytes()
        text = blob.decode('utf-8-sig')
        if not MARKER.search(text):
            rel = path.relative_to(ROOT).as_posix()
            # Only explicit project file names may receive a new integration header.
            owned_name = re.match(r'(?:COLDWAR_|mdcw_|zz.*(?:imp|mdcw))', path.name, re.I)
            if args.fill_known_gaps and owned_name:
                prefix = '--' if path.suffix == '.lua' else '#'
                header = prefix + ' IMPERIA COLD WAR: Project-specific integration; preserve existing author credits.\n'
                if path.suffix == '.yml':
                    lines = text.splitlines(keepends=True)
                    if not lines or lines[0].strip() != 'l_english:':
                        raise AssertionError('Unexpected localisation header: ' + rel)
                    lines.insert(1, ' ' + header)
                    updated = ''.join(lines)
                else:
                    updated = header + text
                encoded = updated.encode('utf-8-sig' if path.suffix == '.yml' else 'utf-8')
                # Verify exact original text survives after removing only the inserted comment.
                assert updated.replace((' ' if path.suffix == '.yml' else '') + header, '', 1) == text
                path.write_bytes(encoded)
                report['added_markers'].append({
                    'path': rel, 'before_sha256': digest(blob), 'after_sha256': digest(encoded),
                    'comment_only': True,
                })
                blob, text = encoded, updated
            else:
                report['missing_runtime'].append(rel)
        wants_bom = path.suffix == '.yml'
        if blob.startswith(b'\xef\xbb\xbf') != wants_bom:
            report['encoding_errors'].append(path.relative_to(ROOT).as_posix())
    for path in sorted((ROOT / 'tools').rglob('*')):
        if path.suffix not in SOURCE_SUFFIXES or EXCLUDED.intersection(path.relative_to(ROOT).parts):
            continue
        report['owned_tool_sources_checked'] += 1
        if not MARKER.search(path.read_text(encoding='utf-8-sig')):
            report['missing_tools'].append(path.relative_to(ROOT).as_posix())
    manifest = json.loads((ROOT / 'docs/imperia_cw_markers_shared_20261021.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        path = ROOT / row['path']
        if not path.exists():
            continue  # Retired content does not need resurrecting for an attribution check.
        report['shared_files_checked'] += 1
        if not MARKER.search(path.read_text(encoding='utf-8-sig')):
            report['missing_shared'].append(row['path'])
    destination = ROOT / 'docs/imperia_cold_war_markers_latest.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {key: value for key, value in report.items() if key.endswith('_checked')}
    summary['markers_added'] = len(report['added_markers'])
    for key in ['missing_runtime', 'missing_tools', 'missing_shared', 'encoding_errors']:
        summary[key] = report[key]
    print(json.dumps(summary, indent=2))
    if any(report[key] for key in ['missing_runtime', 'missing_tools', 'missing_shared', 'encoding_errors']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
