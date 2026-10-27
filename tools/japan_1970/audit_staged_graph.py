# IMPERIA CW — Cold War: Japan 1970 emitted graph verification.
"""Compare staged focus blocks to the approved positions and prerequisite groups."""
from pathlib import Path
import json
import re
from layout import apply_layout
from presentation import read_focuses

root = Path(__file__).resolve().parent
design = apply_layout(json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design'])
nodes = [n for section in design['sections'] for n in section['nodes']]
text = (root / 'staging' / 'graph' / 'focus_tree.txt').read_text(encoding='utf-8')
prefix = 'COLDWAR_JAP_1970_'
def fid(ident):
    return ident if ident.startswith(prefix) else prefix + ident
def blocks(s):
    pos = 0
    while match := re.search(r'(?m)^\s*focus\s*=\s*\{', s[pos:]):
        start = pos + match.end()
        depth = 1
        i = start
        while i < len(s) and depth:
            depth += (s[i] == '{') - (s[i] == '}')
            i += 1
        if depth:
            raise ValueError('Unbalanced focus block')
        yield s[start:i-1]
        pos = i

parsed = {}
for block in blocks(text):
    ident = re.search(r'(?m)^\s*id\s*=\s*(\S+)', block).group(1)
    if ident in parsed:
        raise ValueError('Duplicate emitted focus: ' + ident)
    parsed[ident] = block
errors = []
resolved = read_focuses(text)
for node in nodes:
    ident = fid(node['id'])
    block = parsed.get(ident)
    if block is None:
        errors.append(f'{ident}: focus missing')
        continue
    for key in ('globalX', 'globalY'):
        if resolved[ident][key] != node[key]:
            errors.append(f'{ident}: resolved {key} differs')
    for key, expected in [('cost', node['duration'] // 7)]:
        match = re.search(r'(?m)^\s*' + key + r'\s*=\s*(-?\d+)\s*$', block)
        if match is None or int(match.group(1)) != expected:
            errors.append(f'{ident}: {key} differs')
    groups = [set(re.findall(r'focus\s*=\s*(\S+)', group)) for group in re.findall(r'prerequisite\s*=\s*\{([^{}]*)\}', block)]
    expected_groups = ([{fid(p) for p in node['parents']}] if node['parents'] and node['parent_mode'] == 'OR'
                       else [{fid(p)} for p in node['parents']])
    if groups != expected_groups:
        errors.append(f'{ident}: prerequisite groups differ')
    matches = re.findall(r'mutually_exclusive\s*=\s*\{([^{}]*)\}', block)
    exclusions = set(re.findall(r'focus\s*=\s*(\S+)', matches[0])) if matches else set()
    if exclusions != {fid(p) for p in node['exclusive']}:
        errors.append(f'{ident}: exclusions differ')
if len(parsed) != len(nodes):
    errors.append(f'Expected {len(nodes)} focus blocks, got {len(parsed)}')
print(f'Compared {len(parsed)} emitted focuses with approved graph; {len(errors)} differences')
for error in errors:
    print('ERROR:', error)
raise SystemExit(bool(errors))
