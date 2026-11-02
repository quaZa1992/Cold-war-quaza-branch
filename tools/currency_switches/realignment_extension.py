# IMPERIA COLD WAR — Preserve preceding audits around the realignment integration.
from pathlib import Path
import json
from patch import reverse_edits

HERE = Path(__file__).resolve().parent


def reverse_realignment_extension(name, data):
    manifest = HERE / 'changes.json'
    if not manifest.exists():
        return data
    record = json.loads(manifest.read_text(encoding='utf-8'))['files'].get(str(name).replace('\\', '/'))
    return reverse_edits(data, record) if record else data
