# IMPERIA CW — Cold War: independent Spain v2 emitted-script syntax review.
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / 'tools' / 'spain_1970_v2' / 'stage'
sys.path.insert(0, str(ROOT / 'tools' / 'vietnam_1970'))
from script_ast import parse

files = list(STAGE.rglob('*.txt'))
errors = []
for path in files:
    try:
        parse(path.read_text(encoding='utf-8-sig'))
    except Exception as error:
        errors.append((path.relative_to(STAGE).as_posix(), str(error)))
print(f'Parsed {len(files)} staged .txt files; syntax errors: {len(errors)}')
for rel, error in errors:
    print(f'{rel}: {error}')
