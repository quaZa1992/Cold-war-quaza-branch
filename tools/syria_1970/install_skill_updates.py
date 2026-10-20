"""Install only reviewed skill amendments; requires access to installed skills."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
STAGE = HERE/'skill_updates'
TARGET = Path('C:/Users/sonyz/.codex/skills').resolve()
assert json.loads((STAGE/'validation.json').read_text(encoding='utf-8'))['status'] == 'PASS'
entries = json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
for entry in entries:
    destination = (TARGET/entry['relative']).resolve()
    assert destination.is_relative_to(TARGET)
    staged = (STAGE/entry['relative']).read_bytes()
    previous = destination.read_bytes() if destination.exists() else None
    if previous == staged:
        continue
    assert (hashlib.sha256(previous).hexdigest() if previous is not None else None) == entry['previous_sha256'], entry['relative']
for entry in entries:
    destination = TARGET/entry['relative']
    staged = (STAGE/entry['relative']).read_bytes()
    if destination.exists() and destination.read_bytes() != staged:
        backup = STAGE/'previous'/entry['relative']
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            backup.write_bytes(destination.read_bytes())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(staged)
    assert destination.read_bytes() == staged
print(f'Installed and byte-verified {len(entries)} exact skill files.')
