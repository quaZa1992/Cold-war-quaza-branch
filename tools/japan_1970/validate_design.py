# IMPERIA CW — Cold War: Japan 1970 design and graph validation.
"""Check the approved graph without writing to loaded game files."""
from collections import Counter
from pathlib import Path
import json
from functools import lru_cache

root = Path(__file__).resolve().parent
design = json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design']
nodes = [node for section in design['sections'] for node in section['nodes']]
by_id = {n['id']: n for n in nodes}
errors = []
if len(nodes) != len(by_id):
    errors.append('Duplicate focus IDs')
coordinates = Counter((n['globalX'], n['globalY']) for n in nodes)
errors.extend(f'Duplicate position {p}' for p, count in coordinates.items() if count > 1)
for node in nodes:
    ident = node['id']
    if node['duration'] not in (35, 70):
        errors.append(f'{ident}: unexpected duration')
    if node['parent_mode'] not in ('AND', 'OR'):
        errors.append(f'{ident}: unknown prerequisite grouping')
    for parent in node['parents']:
        if parent not in by_id:
            errors.append(f'{ident}: missing prerequisite {parent}')
        elif by_id[parent]['globalY'] >= node['globalY']:
            errors.append(f'{ident}: prerequisite {parent} does not precede it vertically')
    for other in node['exclusive']:
        if other not in by_id:
            errors.append(f'{ident}: missing exclusion {other}')
        elif ident not in by_id[other]['exclusive']:
            errors.append(f'{ident}: exclusion is not reciprocal with {other}')
    if node['parent_mode'] == 'AND':
        for parent in node['parents']:
            for other in node['parents']:
                if other in by_id.get(parent, {}).get('exclusive', []):
                    errors.append(f'{ident}: AND requires mutually exclusive {parent} and {other}')

def compatible(history):
    return all(not (set(by_id[focus]['exclusive']) & history) for focus in history)

@lru_cache(None)
def paths(ident):
    node = by_id[ident]
    parents = node['parents']
    if not parents:
        return (frozenset((ident,)),)
    if node['parent_mode'] == 'OR':
        candidate = [p | {ident} for parent in parents for p in paths(parent)]
    else:
        candidate = [frozenset((ident,))]
        for parent in parents:
            candidate = [a | b for a in candidate for b in paths(parent) if compatible(a | b)]
    candidate = sorted({p for p in candidate if compatible(p)}, key=len)
    minimal = []
    for p in candidate:
        if not any(previous <= p for previous in minimal):
            minimal.append(p)
    return tuple(minimal)

if not errors:
    for node in nodes:
        if not paths(node['id']):
            errors.append(f'{node["id"]}: no satisfiable prerequisite path under exclusions')

print(f'{len(nodes)} focuses; {len(design["sections"])} sections; '
      f'{sum(not n["parents"] for n in nodes)} independent roots')
for error in errors:
    print('ERROR:', error)
print(f'{len(errors)} structural findings')
raise SystemExit(bool(errors))
