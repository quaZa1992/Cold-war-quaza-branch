# IMPERIA COLD WAR — Adopt the approved foreign-policy revision without changing its baseline.
"""The reviewable full concept is authoritative. Keep original receipts for merges."""
from copy import deepcopy
from layout_repair import apply_layout_repair
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORIGINAL = json.loads((HERE/'approved_design.json').read_text(encoding='utf-8'))
APPROVAL = json.loads((HERE/'revision_approval.json').read_text(encoding='utf-8'))
SOURCE = ROOT/APPROVAL['approved_design']
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == APPROVAL['sha256']
CONCEPT = json.loads(SOURCE.read_text(encoding='utf-8'))
assert CONCEPT['source_snapshot_sha256'] == hashlib.sha256((HERE/'approved_design.json').read_bytes()).hexdigest()
MODEL = deepcopy(ORIGINAL)
MODEL['nodes'] = deepcopy(CONCEPT['nodes'])
MODEL['groups'] = deepcopy(CONCEPT['groups'])
MODEL = apply_layout_repair(MODEL)
OLD = {n['key']: n for n in ORIGINAL['nodes']}
BY = {n['key']: n for n in MODEL['nodes']}
MERGES = [m for m in CONCEPT['merges'] if not m.get('relocated')]

# IMPERIA COLD WAR — National policy receipts are separate from accepted bilateral terms.
NATIONAL = {
    'foreign_diplomacy': [{'kind': 'treasury', 'amount': -.10}],
    'foreign_overseas': [{'kind': 'treasury', 'amount': -.20}],
    'foreign_advisers': [{'kind': 'treasury', 'amount': -.15},
                         {'kind': 'doctrine', 'category': 'land_doctrine', 'bonus': .50, 'uses': 1}],
    'foreign_expeditionary': [{'kind': 'treasury', 'amount': -.35},
                              {'kind': 'doctrine', 'category': 'land_doctrine', 'bonus': .50, 'uses': 1}],
}
for n in MODEL['nodes']:
    n['base_effects'] = deepcopy(OLD[n['key']]['effects']) if n['key'] in OLD else deepcopy(NATIONAL.get(n['key'], []))
    n['base_effects'] += deepcopy(n.get('additional_effects', []))
    n['base_modifiers'] = deepcopy(OLD[n['key']]['modifiers']) if n['key'] in OLD else deepcopy(n['modifiers'])
    n['bundles'] = [deepcopy(m) for m in MERGES if n['key'] in m['targets']]
    if n['key'] in NATIONAL:
        n['effects'] = deepcopy(NATIONAL[n['key']])
    if n['key'] == 'medical_brigades':
        n['base_effects'] = [e for e in n['base_effects'] if e['kind'] != 'offer']

# Original sources remain earned national contributions in existing saves, and
# new completions write those same receipts. Never replay their assets on load.
COMPONENTS = [deepcopy(OLD[m['source']]) for m in MERGES]

# MD's actual registered party predicates include their native party-name label.
PARTY_TRIGGERS = {
    0: 'western_autocrats_are_in_power', 1: 'western_conservatism_are_in_power',
    2: 'western_liberals_are_in_power', 3: 'western_social_democrats_are_in_power',
    4: 'emerging_communist_state_are_in_power', 5: 'emerging_anarchist_communism_are_in_power',
    6: 'emerging_reactionaries_are_in_power', 7: 'emerging_autocracy_are_in_power',
    13: 'neutrality_neutral_autocracy_are_in_power', 18: 'neutrality_neutral_social_are_in_power',
    19: 'neutrality_neutral_communism_are_in_power', 20: 'nationalist_right_wing_populists_are_in_power',
    22: 'nationalist_military_junta_are_in_power',
}
assert len(MODEL['nodes']) == 120
