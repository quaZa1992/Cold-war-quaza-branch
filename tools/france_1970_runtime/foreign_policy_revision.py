# IMPERIA COLD WAR — Authorized French foreign-policy expansion integration.
"""Merge researched additional policy instruments without changing prior content."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE_SHA256 = '57b479c47dafef3d83917931994617bf08c1467d8a00175aa28da957a7518628'
APPROVED_SHA256 = '7bd27bfa457cda2c8443a4252150ed806396a5cc7adb4353a3e5ddaad0f3785f'


def apply_foreign_policy_revision(design):
    baseline = (json.dumps(design, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    assert hashlib.sha256(baseline).hexdigest() == BASELINE_SHA256, 'Foreign-policy baseline changed; review the integration.'
    raw = (HERE/'approved_foreign_policy.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == APPROVED_SHA256, 'Frozen foreign-policy input changed.'
    target = json.loads(raw)
    approval = json.loads((HERE/'FOREIGN_POLICY_APPROVAL.json').read_text(encoding='utf-8'))
    assert approval['project'] == 'IMPERIA COLD WAR'
    assert approval['approved_input_sha256'] == APPROVED_SHA256
    assert target['foreign_policy_baseline_sha256'] == BASELINE_SHA256
    added = [n for n in target['nodes'] if n.get('foreign_policy_change') == 'new']
    groups = [g for g in target['groups'] if g['id'] in target['foreign_policy_new_groups']]
    assert len(added) == 37 and sum('offer' in n for n in added) == 32 and len(groups) == 4
    old_keys = {n['key'] for n in design['nodes']}
    assert not old_keys.intersection(n['key'] for n in added)
    assert [n for n in target['nodes'] if n['key'] in old_keys] == design['nodes'], 'An existing focus changed.'
    assert target['decisions'] == design['decisions'], 'An existing domestic decision changed.'
    assert [g for g in target['groups'] if g['id'] not in target['foreign_policy_new_groups']] == design['groups']
    out = deepcopy(design)
    out['groups'].extend(deepcopy(groups))
    out['nodes'].extend(deepcopy(added))
    out['foreign_policy_revision'] = dict(project='IMPERIA COLD WAR',approved_input_sha256=APPROVED_SHA256,
        baseline_runtime_design_sha256=BASELINE_SHA256,added_focus_keys=[n['key'] for n in added],
        added_group_ids=[g['id'] for g in groups],added_focus_count=37,added_offer_count=32)
    return out
