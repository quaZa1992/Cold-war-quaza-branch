# IMPERIA CW — Cold War: skill updates — verify impact update.
"""Verify the installed, authorized skill edits without writing skill files."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = Path('C:/Users/Enes/.codex/skills')
updates = json.loads((HERE/'impact_updates.json').read_text(encoding='utf-8'))
prior = {}
for bundle in ('updates.json', 'clarification_updates.json', 'reference_pool_updates.json'):
    for row in json.loads((HERE/bundle).read_text(encoding='utf-8')):
        prior[hashlib.sha256(row['after'].encode()).hexdigest()] = row['after']

checks = []
for row in updates:
    actual = (BASE/row['relative']).read_bytes()
    assert actual == row['after'].encode('utf-8'), row['relative']
    before = prior[row['before_sha256']]
    if row['relative'].endswith('SKILL.md'):
        assert before.split('---', 2)[:2] == row['after'].split('---', 2)[:2]
        assert row['after'].startswith('---\nname: ')
        assert '\ndescription: ' in row['after'].split('---', 2)[1]
    assert 'TODO' not in row['after']
    checks.append({'path':str(BASE/row['relative']), 'sha256':hashlib.sha256(actual).hexdigest(), 'exact_staged_match':True, 'existing_metadata_preserved':True})

report = {'checks':checks, 'scope':'Exact installed/staged content, original frontmatter and scaffold checks. Official quick_validate could not run because PyYAML is absent; no environment dependency was installed.'}
(HERE/'IMPACT_INSTALL_VERIFICATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
