# IMPERIA CW — Cold War: stage current generated politics for independent review.
"""Refresh only reviewer-owned stage files from politics.py; never writes to mod."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TARGET = HERE / 'review_stage_latest'
spec = importlib.util.spec_from_file_location('spain_v2_politics', HERE / 'politics.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
design = json.loads((HERE / 'approved_design.json').read_text(encoding='utf-8-sig'))
files = module.build(ROOT, design)
for rel, data in files.items():
    path = TARGET / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
print(f'Refreshed {len(files)} current politics outputs into {TARGET}')
