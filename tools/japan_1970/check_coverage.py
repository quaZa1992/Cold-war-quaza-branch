# IMPERIA COLD WAR — Cold War: Japan 1970 staged content coverage.
"""List focuses without even a staged reward provider; coverage is not validation."""
import json
from pathlib import Path
from reward_revision import effective_design, effective_inventory, effective_party_map

root = Path(__file__).resolve().parent
design = effective_design(json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design'])
nodes = [n for s in design['sections'] for n in s['nodes']]
groups = {n['id']: s['category'] for s in design['sections'] for n in s['nodes']}
party = effective_party_map(json.loads((root / 'party_map.json').read_text(encoding='utf-8')))['focus_helpers']
general = list(effective_inventory(json.loads((root / 'effect_inventory.json').read_text(encoding='utf-8'))).values())
foreign_root = root / 'staging' / 'foreign'
domestic = json.loads((foreign_root / 'manifest.json').read_text(encoding='utf-8'))
bilateral = [json.loads(line) for line in (foreign_root / 'bilateral_manifest.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
covered = set(party) | {x['id'] for x in general} | {x['focus'] for x in domestic + bilateral}
covered |= {n['id'] for n in nodes if n['id'].startswith('COLDWAR_JAP_1970_article9_')}
missing = [n['id'] for n in nodes if n['id'] not in covered]
print(f'{len(covered)} of {len(nodes)} focuses have a mapped or staged reward; '
      'mapping does not establish correctness or game integration.')
for ident in missing:
    print(f'UNMAPPED [{groups[ident]}] {ident}')
print(f'{len(missing)} unmapped focuses')
