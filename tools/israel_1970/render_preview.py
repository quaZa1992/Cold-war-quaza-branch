"""Update the spatial preview from the compiled English tree, not the old draft."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'english_design.json').read_text(encoding='utf-8'))
# The live preview needs focus effects and branch decisions, not the full audit.
DATA={key:DATA[key] for key in ('nodes','groups','layout','starting_spirits','decisions')}
node_fields=('id','label','group','days','xy','icon','prerequisites','visual_prerequisites','mutually_exclusive','modifiers','note','available','completion_reward_code','reward_summary')
DATA['nodes']=[{key:n[key] for key in node_fields} for n in DATA['nodes']]
DATA['groups']=[{key:g[key] for key in ('id','label','outlook','party')} for g in DATA['groups']]
fragment=(HERE/'tree_fragment.html').read_text(encoding='utf-8')
fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="isr70-data">'+json.dumps(DATA,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>')
dest=Path('C:/Users/Enes/.codex/visualizations/2026/10/14/01a13b3e-0590-76b1-9860-e229bfe76415/israel-1970-focus-tree.html')
assert len(fragment.encode('utf-8'))<1_000_000
dest.write_text(fragment,encoding='utf-8')
print(str(dest))
