# IMPERIA CW — Cold War: israel 1970 — validate layout.
"""Check compact layout, relative anchors and preserved gameplay dependencies."""
from pathlib import Path
from itertools import combinations
import json
import re
import sys
from script_format import read

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
old=json.loads((HERE/'reward_revision_baseline.json').read_text(encoding='utf-8'))
manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
nodes={n['id']:n for n in data['nodes']}
errors=[]
def check(ok,message):
    if not ok:errors.append(message)
def box(items):
    xy=[n['xy'] for n in items]
    return {'left':min(x for x,y in xy),'right':max(x for x,y in xy),
            'top':min(y for x,y in xy),'bottom':max(y for x,y in xy),
            'width':max(x for x,y in xy)-min(x for x,y in xy)+2,
            'height':max(y for x,y in xy)-min(y for x,y in xy)+1}
before=box(old.values());after=box(nodes.values())
check(after['width']<before['width']*.35,'Tree still spans an unnecessarily wide horizontal strip')
# New focus groups increase the tree's total footprint. Compare area per focus
# so a larger tree can still pass when the added content is laid out densely.
before_density=before['width']*before['height']/len(old)
after_density=after['width']*after['height']/len(nodes)
check(after_density<before_density*.8,'Compact layout did not reduce average occupied area per focus enough')
for a,b in combinations(nodes.values(),2):
    check(a['xy'][1]!=b['xy'][1] or abs(a['xy'][0]-b['xy'][0])>=2,'Overlapping focus cards: '+a['id']+'/'+b['id'])
for key,n in nodes.items():
    if key in old and not n.get('policy_extension'):
        expected=[[p for p in row if p not in data['removed_unlock_focuses']] for row in old[key]['prerequisites']]
        check(n['prerequisites']==[row for row in expected if row],'Policy prerequisites changed: '+key)
    else:
        check(all(parent in nodes for row in n['prerequisites'] for parent in row),'Missing policy prerequisite: '+key)
    drawn=n['visual_prerequisites'];gates=n['availability_prerequisites']
    check(sorted(drawn+gates)==sorted(n['prerequisites']),'Missing logical requirement: '+key)
    for row in drawn:
        check(all(nodes[p]['group']==n['group'] for p in row),'Long cross-block connector remains: '+key)
        for parent in row:
            check(nodes[parent]['xy'][1]<n['xy'][1],'Prerequisite connector does not descend: '+parent+'/'+key)
    for row in gates:
        clause=' '.join('has_completed_focus = '+p for p in row)
        if len(row)>1:clause='OR = { '+clause+' }'
        check(clause in n['available'],'Cross-block requirement lost from available: '+key)
    anchor=n['relative_position_id']
    xy=n['script_xy'] if anchor is None else [nodes[anchor]['xy'][i]+n['script_xy'][i] for i in (0,1)]
    check(xy==n['xy'],'Relative offset resolves incorrectly: '+key)

policy_groups={g['id']:g for g in data['groups'] if g['id'].startswith('policy_')}
for group_id,group in policy_groups.items():
    origin=group.get('layout_origin')
    check(origin is not None,'Missing policy block origin: '+group_id)
    if origin is not None:
        check(origin[1]>=26,'Policy block is not below the existing tree: '+group_id)
    for node in (n for n in nodes.values() if n['group']==group_id):
        if 'policy_local_xy' in node:
            check(node['local_xy']==node['policy_local_xy'],'Policy local coordinate ignored: '+node['id'])
        check(node['local_xy'] is not None,'Policy node has no local position: '+node['id'])

# Visible choice groups must form an actual horizontal alternative row. Each
# alternative remains a separate focus and its local prerequisites are checked
# by the same connector simulation below.
choice_groups={}
for node in nodes.values():
    choice=node.get('choice_group')
    if choice:choice_groups.setdefault((node['group'],choice),[]).append(node)
for (group_id,choice),members in choice_groups.items():
    check(len(members)>=2,'Choice group has fewer than two alternatives: '+group_id+'/'+choice)
    ys={n['xy'][1] for n in members}
    check(len(ys)==1,'Choice alternatives are not on one visual row: '+group_id+'/'+choice)
    xs=sorted(n['xy'][0] for n in members)
    check(all(b-a>=2 for a,b in zip(xs,xs[1:])),'Choice alternatives overlap: '+group_id+'/'+choice)

# Inspect what HOI4 actually loads as well as the design metadata. An edited or
# stale generated file can otherwise pass every layout check above.
def values(ast,key):return [value for name,operator,value in ast if name==key]
def one(ast,key,default=None):return next(iter(values(ast,key)),default)

trees=values(read((ROOT/'common/national_focus/ISR70_focus.txt').read_text(encoding='utf-8-sig')),'focus_tree')
check(len(trees)==1,'Expected exactly one generated focus tree')
script_nodes={}
for tree in trees:
    for focus in values(tree,'focus'):
        key=one(focus,'id')
        check(key not in script_nodes,'Duplicate generated focus: '+str(key))
        script_nodes[key]=focus
check(script_nodes.keys()==nodes.keys(),'Generated focus IDs differ from the layout design')
resolved={}
def resolve(key,trail=()):
    if key in resolved:return resolved[key]
    if key in trail or key not in script_nodes:
        check(False,'Missing or cyclic generated relative anchor: '+' -> '.join((*trail,key)))
        return None
    focus=script_nodes[key]
    try:xy=[float(one(focus,axis)) for axis in ('x','y')]
    except (TypeError,ValueError):
        check(False,'Invalid generated focus position: '+key)
        return None
    anchor=one(focus,'relative_position_id')
    if anchor:
        origin=resolve(anchor,(*trail,key))
        if origin is None:return None
        xy=[origin[i]+xy[i] for i in (0,1)]
    resolved[key]=xy
    return xy
for key,focus in script_nodes.items():
    xy=resolve(key)
    if key not in nodes:continue
    check(xy==nodes[key]['xy'],'Generated focus position differs from preview: '+key)
    drawn=[values(row,'focus') for row in values(focus,'prerequisite')]
    check(drawn==nodes[key]['visual_prerequisites'],'Generated connectors differ from preview: '+key)

# Match tree_fragment.html's three orthogonal prerequisite segments. This is a
# preview readability check, not a claim about the engine's connector routing.
layout=data['layout']
unit_x,unit_y=layout['x_unit'],layout['y_unit']
width,height=layout['node_width'],layout['node_height']
def segment_hits_card(a,b,node):
    x,y=node['xy'];left,top=x*unit_x,y*unit_y
    right,bottom=left+width,top+height
    if a[0]==b[0]:
        return left<a[0]<right and max(min(a[1],b[1]),top)<min(max(a[1],b[1]),bottom)
    return top<a[1]<bottom and max(min(a[0],b[0]),left)<min(max(a[0],b[0]),right)

connectors_checked=0
local_or_rows=[]
for key,node in nodes.items():
    for row in node['visual_prerequisites']:
        if len(row)>1:
            alternatives=[nodes[parent] for parent in row]
            if all(parent['group']==node['group'] for parent in alternatives):
                local_or_rows.append((key,row))
                check(len({parent['xy'][1] for parent in alternatives})==1,
                      'Local ODER alternatives are not on one row: '+key)
                xs=sorted(parent['xy'][0] for parent in alternatives)
                check(all(b-a>=2 for a,b in zip(xs,xs[1:])),
                      'Local ODER alternatives overlap: '+key)
    for row in node['visual_prerequisites']:
        for parent in row:
            source=nodes[parent]
            x1=source['xy'][0]*unit_x+width/2;y1=source['xy'][1]*unit_y+height
            x2=node['xy'][0]*unit_x+width/2;y2=node['xy'][1]*unit_y-8
            middle=(y1+y2)/2
            points=((x1,y1),(x1,middle),(x2,middle),(x2,y2))
            hits=[other for other,card in nodes.items() if other not in (key,parent)
                  and any(segment_hits_card(a,b,card) for a,b in zip(points,points[1:]))]
            check(not hits,'Preview connector crosses focus cards: '+parent+' -> '+key+' / '+', '.join(hits))
            connectors_checked+=1
loc=(ROOT/'localisation/english/ISR70_l_english.yml').read_text(encoding='utf-8-sig')
check('Rewards on completion:' not in loc,'Duplicate reward list remains in game descriptions')
expected_focus_count=manifest.get('focuses',len(nodes))
check(len(nodes)==expected_focus_count,'Design focus count differs from manifest: '+str(len(nodes))+'/'+str(expected_focus_count))
check(sum(n['relative_position_id'] is None for n in nodes.values())==1,'Expected exactly one absolute focus root')
russia=(ROOT/'common/national_focus/05_russia.txt').read_text(encoding='utf-8-sig')
result={'status':'FAIL' if errors else 'PASS','errors':errors,'before':before,'after':after,
        'width_reduction_percent':round((1-after['width']/before['width'])*100,1),
        'bounding_area_reduction_percent':round((1-after['width']*after['height']/(before['width']*before['height']))*100,1),
        'before_area_per_focus':round(before_density,2),
        'after_area_per_focus':round(after_density,2),
        'local_oder_rows_checked':len(local_or_rows),
        'relative_anchors':sum(n['relative_position_id'] is not None for n in nodes.values()),
        'expected_focus_count':expected_focus_count,
        'policy_groups_checked':len(policy_groups),
        'policy_choice_groups_checked':len(choice_groups),
        'cross_block_requirements_preserved':sum(len(n['availability_prerequisites']) for n in nodes.values()),
        'generated_positions_checked':len(resolved),
        'preview_connectors_checked':connectors_checked,
        'md_russia_relative_position_examples':len(re.findall(r'\brelative_position_id\s*=',russia)),
        'duplicate_description_rewards':False,'runtime_test':False}
if '--no-report' not in sys.argv:
    (ROOT/'docs/israel_1970_design/layout_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
