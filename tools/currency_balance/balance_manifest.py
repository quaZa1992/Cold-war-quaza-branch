# IMPERIA CW — Cold War: currency balance — balance manifest.
"""Reverse this authorized balance pass for older staged preservation audits."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent


def reverse_if_recorded(name,data):
    path=HERE/'changes.json'
    if not path.exists():return data
    records=json.loads(path.read_text())['files']
    record=records.get(str(name).replace('\\','/'))
    if record is None:return data
    assert hashlib.sha256(data).hexdigest()==record['after_sha256'],f'Balance manifest differs: {name}'
    for edit in reversed(record['edits']):
        offset=edit['offset_after'];after=edit['after'].encode();before=edit['before'].encode()
        assert data[offset:offset+len(after)]==after,f'Balance edit differs: {name}'
        data=data[:offset]+before+data[offset+len(after):]
    assert hashlib.sha256(data).hexdigest()==record['before_sha256'],f'Balance preimage differs: {name}'
    return data
