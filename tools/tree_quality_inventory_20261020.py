# IMPERIA CW — Cold War: tools — tree quality inventory 20261020.
"""Read-only focus inventory for the 2026-10-20 quality audit."""
import ast
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/tree_quality_audit_20261020'
ns = {'re': re}
source = ROOT / 'tools/israel_1970/validate_content.py'
module = ast.parse(source.read_text(encoding='utf-8'))
functions = [n for n in module.body if isinstance(n, ast.FunctionDef)
             and n.name in {'tokens', 'parse', 'values', 'first', 'walk'}]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), ns)
parse, first, values, walk = (ns[n] for n in ('parse', 'first', 'values', 'walk'))

localisation = {}
for path in sorted((ROOT / 'localisation/english').rglob('*.yml')):
    for line, text in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        match = re.match(r'\s*([^\s:#]+):\d*\s*"(.*)"\s*$', text)
        if match:
            localisation[match[1]] = (match[2], str(path.relative_to(ROOT)), line)

names = ['COLDWAR_CYP_1970_focus.txt', 'COLDWAR_DDR_1970_focus.txt',
         'COLDWAR_EGY_1970_focus.txt', 'COLDWAR_GCC_1970_shared.txt',
         'COLDWAR_GRE_1970_focus.txt', 'COLDWAR_IRQ_1970_focus.txt',
         'COLDWAR_SOV_1970_focus.txt', 'COLDWAR_UAE_1970_focus.txt',
         'COLDWAR_UNI_1970_union_joint.txt', 'COLDWAR_VIE_1970_focus.txt',
         'ISR70_focus.txt', 'libya_1970.txt', 'mdcw_1970_generic_focus.txt',
         'spain_1970.txt', 'USA_1970.txt']
rows, summaries = [], []
for name in names:
    path = ROOT / 'common/national_focus' / name
    raw = path.read_text(encoding='utf-8-sig')
    data = parse(raw)
    own = []
    for key, op, node in walk(data):
        if key not in {'focus', 'shared_focus', 'joint_focus'} or not isinstance(node, list):
            continue
        fid = first(node, 'id')
        if not fid:
            continue
        desc, locfile, locline = localisation.get(fid + '_desc', ('', '', 0))
        reward = first(node, 'completion_reward', [])
        # Counts are screening metadata, not pass/fail quality criteria.
        keys = Counter(k for k, _, v in walk(reward) if not isinstance(v, list))
        row = dict(file=str(path.relative_to(ROOT)), id=fid,
                   line=raw[:re.search(r'\bid\s*=\s*' + re.escape(fid) + r'\b', raw).start()].count('\n') + 1,
                   cost=float(first(node, 'cost', 10)),
                   description_words=len(re.findall(r"[\w'-]+", desc)),
                   description=desc, localisation_file=locfile, localisation_line=locline,
                   prerequisite_groups=[values(n, 'focus') for n in values(node, 'prerequisite')],
                   exclusive=values(first(node, 'mutually_exclusive', []), 'focus'),
                   reward_leaf_keys=dict(keys))
        own.append(row)
        rows.append(row)
    costs = Counter(r['cost'] for r in own)
    summaries.append(dict(file=str(path.relative_to(ROOT)), count=len(own),
                          sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          cost_distribution=dict(sorted(costs.items())),
                          missing_descriptions=sum(not r['description'] for r in own),
                          description_median=sorted(r['description_words'] for r in own)[len(own)//2] if own else None))
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'inventory.json').write_text(json.dumps({'date':'2026-10-20', 'summaries':summaries, 'focuses':rows}, ensure_ascii=False, indent=2), encoding='utf-8')
with (OUT / 'inventory.csv').open('w', encoding='utf-8-sig', newline='') as stream:
    fields=['file','id','line','cost','description_words','description','localisation_file','localisation_line']
    writer=csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
print(json.dumps(summaries, indent=2))
