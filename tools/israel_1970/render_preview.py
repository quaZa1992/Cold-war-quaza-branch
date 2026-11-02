# IMPERIA COLD WAR — Israel 1970 faithful installed-tree visualisation.
"""Update the spatial preview from the compiled English tree, not the old draft."""
from pathlib import Path
import json,re,argparse

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=ROOT/'docs/israel_1970_design/focus-tree.html')
args=parser.parse_args()
DATA=SOURCE
# The live preview needs focus effects and branch decisions, not the full audit.
DATA={key:DATA[key] for key in ('nodes','groups','layout','starting_spirits','decisions','occupation_profiles')}
node_fields=('id','label','group','days','xy','icon','prerequisites','visual_prerequisites','mutually_exclusive','modifiers','note','reward_summary')
localisation={k:json.loads(v) for k,v in re.findall(r'^ (\S+):0 (".*")$',(ROOT/'localisation/english/ISR70_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}
groups={g['id']:g for g in DATA['groups']}
compact=[]
for original in DATA['nodes']:
    node={key:original[key] for key in node_fields}
    conditions=list(original.get('requirement_summary',[]))
    group=groups[node['group']]
    if group['party'] is not None:conditions.append(localisation.get('ISR70_party_'+str(group['party']),group['label'])+' is in power.')
    for key in re.findall(r'tooltip = (ISR70_\w+_condition_tt)',original['available']):
        label=localisation.get(key)
        if label and label not in conditions:conditions.append(label)
    node['condition_summary']=conditions
    compact.append(node)
DATA['nodes']=compact
from player_rewards import modifier_line
for spirit in DATA['starting_spirits'].values():
    spirit['modifier_summary']=[modifier_line(k,v) for k,v in spirit['modifiers'].items()]
DATA['occupation_profiles']=[dict(label=p['label'],initial_resistance=p['initial_resistance'],initial_compliance=p['initial_compliance'],
    state_effects=[modifier_line(k,v) for k,v in p['state_modifiers'].items()],
    budget_effects=['Israel: '+modifier_line(k,v) for k,v in p['country_modifiers'].items()]) for p in DATA['occupation_profiles']['profiles']]
DATA['decisions']=DATA['decisions']+SOURCE.get('policy_decision_exports',[])
for p in SOURCE['policy_expansion']['projects']:
    did='ISR70_policy_project_'+p['key']
    DATA['decisions'].append(dict(id=did,label=localisation.get(did,p['key']),unlock='ISR70_'+p['unlock'],cost=p.get('political_cost',0),days=p['days'],repeatable=False,cooldown=0,note=p['delivery_summary']))
DATA['decisions']=[{k:d[k] for k in ('id','label','unlock','cost','days','repeatable','cooldown','note')} for d in DATA['decisions']]
DATA['groups']=[{key:g[key] for key in ('id','label','outlook','party')} for g in DATA['groups']]
fragment=(HERE/'tree_fragment.html').read_text(encoding='utf-8')
fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="isr70-data">'+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>')
dest=args.output
dest.parent.mkdir(parents=True,exist_ok=True)
assert len(fragment.encode('utf-8'))<1_000_000
dest.write_text(fragment,encoding='utf-8')
print(str(dest))
