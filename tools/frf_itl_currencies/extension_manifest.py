# IMPERIA COLD WAR — Preserve earlier currency audits around the authorised Franc/Lira extension.
"""Reverse only this extension's recorded insertions for earlier preservation proofs."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
# IMPERIA COLD WAR — Retain the Franc/Lira proof after the researched 1970 history extension.
sys.path.insert(0, str(HERE.parent / 'world_1970_society'))
from history_extension import reverse_history_extension
# IMPERIA COLD WAR — Reverse only the subsequent recorded realignment integration.
sys.path.insert(0, str(HERE.parent / 'currency_switches'))
from realignment_extension import reverse_realignment_extension


def reverse_extension(name, data):
    # IMPERIA COLD WAR — Preserve the original proof beneath the paid-switch extension.
    data = reverse_realignment_extension(name, data)
    # IMPERIA COLD WAR — Verify and reverse only the later recorded history insertion first.
    data = reverse_history_extension(name, data)
    manifest = HERE / 'changes.json'
    if not manifest.exists():
        return data
    record = json.loads(manifest.read_text(encoding='utf-8'))['files'].get(str(name).replace('\\', '/'))
    if record is None:
        return data
    assert hashlib.sha256(data).hexdigest() == record['after_sha256'], f'Currency extension differs: {name}'
    for edit in reversed(record['edits']):
        offset = edit['offset_after']
        after = edit['after'].encode('utf-8')
        assert data[offset:offset + len(after)] == after
        data = data[:offset] + edit['before'].encode('utf-8') + data[offset + len(after):]
    assert hashlib.sha256(data).hexdigest() == record['before_sha256'], f'Currency extension preimage differs: {name}'
    return data
