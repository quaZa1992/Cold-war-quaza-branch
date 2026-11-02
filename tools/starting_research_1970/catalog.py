# IMPERIA COLD WAR — Worldwide January 1970 technology catalogue.
"""Read the live technology definitions without changing runtime files."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools.multiplayer_quality.audit import parse


def values(rows, key):
    return [value for name, op, value in rows if name == key]


def first(rows, key, default=None):
    return next(iter(values(rows, key)), default)


def bare(rows):
    return [value for name, op, value in rows if name == '_bare']


def catalogue():
    data = {}
    duplicates = []
    for path in sorted((ROOT / 'common/technologies').glob('*.txt')):
        for name, op, rows in parse(path.read_text(encoding='utf-8-sig')):
            if name != 'technologies' or not isinstance(rows, list):
                continue
            for key, op, block in rows:
                if not isinstance(block, list) or key.startswith('@'):
                    continue
                if key in data:
                    duplicates.append(key)
                year = first(block, 'start_year')
                data[key] = {
                    'file': path.relative_to(ROOT).as_posix(),
                    'year': int(float(year)) if year is not None else None,
                    'folders': [first(x, 'name') for x in values(block, 'folder')],
                    'categories': bare(first(block, 'categories', [])),
                    'paths': [first(x, 'leads_to_tech') for x in values(block, 'path')],
                    'xor': [v for x in values(block, 'xor') for v in bare(x)],
                    'dependencies': [name for x in values(block, 'dependencies') for name, operator, value in x if name != '_bare'],
                    'allow': first(block, 'allow', []),
                    'allow_branch': first(block, 'allow_branch', []),
                    'doctrine': first(block, 'doctrine'),
                    'enable_equipments': bare(first(block, 'enable_equipments', [])),
                    'enable_equipment_modules': bare(first(block, 'enable_equipment_modules', [])),
                    'special_projects': values(block, 'special_project'),
                }
    return data, duplicates


if __name__ == '__main__':
    data, duplicates = catalogue()
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / 'technology_catalog.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'technologies': data, 'duplicates': duplicates}, indent=2) + '\n', encoding='utf-8')
    lines = ['IMPERIA COLD WAR: available pre-1971 technologies', 'ID\tYEAR\tFILE\tFOLDERS']
    for key, row in data.items():
        if row['year'] is not None and row['year'] <= 1970:
            lines.append(f"{key}\t{row['year']}\t{Path(row['file']).name}\t{','.join(str(x) for x in row['folders'])}")
    (HERE / 'technology_catalog.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'tech_count': len(data), 'pre1971': len(lines)-2, 'duplicates': duplicates}))
