# IMPERIA CW — Cold War: israel 1970 — validate design.
"""Static graph and source API validation of the design, not an HOI4 runtime test."""
from pathlib import Path
import collections
import itertools
import json
import re

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/israel_1970_design'
design=json.loads((OUT/'israel_1970_tree_design.json').read_text(encoding='utf-8'))
api=json.loads((OUT/'effect_api_audit.json').read_text(encoding='utf-8'))
nodes={n['id']:n for n in design['nodes']}
assert len(nodes)==len(design['nodes']), 'duplicate focus id'
active_slots=set(range(24))-{8,9,10,11}
assert {g['party'] for g in design['groups'] if g['party'] is not None}==active_slots
assert len({d['id'] for d in design['decisions']})==len(design['decisions'])
assert len(design['starting_spirits'])==7
assert len({tuple(n['xy']) for n in nodes.values()})==len(nodes),'duplicate focus position'
assert all(n['xy'] and n['local_xy'] for n in nodes.values()),'missing fixed position'
for n in nodes.values():
    for row in n['prerequisites']:
        assert all(nodes[pre]['xy'][1]<n['xy'][1] for pre in row),('backward focus edge',n['id'])
assert all(v['evidence'] for v in api.values()), 'missing existing API definition/example'
for n in nodes.values():
    assert all(pre in nodes for row in n['prerequisites'] for pre in row),n['id']
    for other in n['mutually_exclusive']:
        assert other in nodes and n['id'] in nodes[other]['mutually_exclusive'], (n['id'],other)
for d in design['decisions']:assert d['unlock'] is None or d['unlock'] in nodes,d['id']

# A focus can only complete when every prerequisite block has at least one completed entry.
# Check the whole graph, and all four internal economy/society combinations for every slot.
def reachable(excluded=frozenset()):
    complete=set()
    while True:
        added={n['id'] for n in nodes.values() if n['id'] not in complete|set(excluded)
               and all(any(p in complete for p in row) for row in n['prerequisites'])}
        if not added:return complete
        complete|=added
assert reachable()==set(nodes),'cycle or impossible prerequisite'
for slot in sorted(active_slots):
    for econ,civic in itertools.product(('ea','eb'),('ca','cb')):
        opposite={'ea':'eb','eb':'ea','ca':'cb','cb':'ca'}
        exclude={f'ISR70_p{slot}_{opposite[econ]}',f'ISR70_p{slot}_{opposite[civic]}'}
        assert f'ISR70_p{slot}_finish' in reachable(exclude),(slot,econ,civic)

# Research categories must not merely exist as empty category declarations: actual techs use them.
technology_text='\n'.join(p.read_text(encoding='utf-8-sig') for p in (ROOT/'common/technologies').glob('*.txt'))
used_categories=set(re.findall(r'category = (CAT_\w+)', '\n'.join(n['completion_reward_code'] for n in nodes.values())))
category_blocks=re.findall(r'categories\s*=\s*\{([^}]+)\}',technology_text)
assert all(any(re.search(r'\b'+re.escape(cat)+r'\b',b) for b in category_blocks) for cat in used_categories)
code=(OUT/'md_style_code_drafts.txt').read_text(encoding='utf-8')
clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*','',code)
depth=0
for c in clean:
    depth+=(c=='{')-(c=='}')
    assert depth>=0,'unbalanced Clausewitz draft'
assert depth==0,'unbalanced Clausewitz draft'

# Every new referenced idea has an explicit draft definition; do not call a nonexistent vanilla spirit.
definitions=set(re.findall(r'(?m)^\s*(ISR70_\w+)\s*=\s*\{',code))
references=set(re.findall(r'(?:add_ideas|remove_ideas|idea)\s*=\s*(ISR70_\w+)',code))
assert references<=definitions,references-definitions
buildings=collections.Counter()
for reward in [n['reward'] for n in nodes.values()]+[d['reward'] for d in design['decisions']]:
    for kind,num in re.findall(r'add_building_construction = \{ type = (\w+) level = (\d+)',reward):buildings[kind]+=int(num)
result={'status':'PASS','focuses':len(nodes),'base_decisions':len(design['decisions']),'party_slots':len(active_slots),
        'programme_combinations_checked':len(active_slots)*4,'existing_apis':len(api),'research_categories':sorted(used_categories),
        'direct_building_totals':dict(buildings),'limits':'Static graph and API audit. See implementation_validation.json for live script/reference validation; HOI4 runtime behavior remains untested.'}
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
