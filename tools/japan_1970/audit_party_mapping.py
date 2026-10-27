# IMPERIA CW — Cold War: Japan 1970 party-effect numeric coverage audit.
"""Flag unaccounted numeric effects for review; this does not prove semantics."""
from collections import Counter
from decimal import Decimal
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parent
design = json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design']
mapping = json.loads((root / 'party_map.json').read_text(encoding='utf-8'))['focus_helpers']
nodes = [n for section in design['sections'] if section['category'] == 'Political parties' for n in section['nodes']]
findings = []
for node in nodes:
    ident = node['id']
    if ident not in mapping:
        findings.append(f'{ident}: helper missing')
        continue
    record = mapping[ident]
    text = node['effects'].replace('−', '-').replace('–', '-')
    promised = Counter(Decimal(sign + amount) / 100 for sign, amount in re.findall(r'([+-])\s*(\d+(?:\.\d+)?)\s*%', text))
    provided = Counter(Decimal(str(value)) for value in record.get('modifier_increments', {}).values())
    missing = promised - provided
    if missing:
        findings.append(f'{ident}: unaccounted signed percentage quantities {dict(missing)}')
    costs = re.findall(r'spend\s*\$([\d.]+)\s*billion', text, re.I)
    actual = [-Decimal(str(x['amount'])) for x in record.get('one_time_effects', []) if x['type'] == 'treasury']
    if Counter(map(Decimal, costs)) != Counter(actual):
        findings.append(f'{ident}: treasury cost mismatch: design={costs}, mapped={actual}')

print(f'{len(nodes)} political focuses, {len(mapping)} mappings; numeric quantity comparison only')
for finding in findings:
    print('REVIEW:', finding)
print(f'{len(findings)} findings')
