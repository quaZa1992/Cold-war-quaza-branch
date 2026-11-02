# IMPERIA COLD WAR — Build the interactive France concept and complete numeric catalogue.
from pathlib import Path
import base64
import json

OUT=Path(__file__).resolve().parent
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/28/01a183df-ceae-74b3-b1f4-d519f043ee74')
d=json.loads((OUT/'concept.json').read_text(encoding='utf-8'))
names=['french_republic','FRA_cdg','economic_prosperity','brain_power','FRA_ps_party','french_communist_party','national_grid','nuclear_energy','french_army','french_army_navy','french_army_air','industry_military','francosphere','francafrique','nato','GFX_focus_unavailable','GFX_focus_can_start']
art={name:'data:image/png;base64,'+base64.b64encode((OUT/'art'/f'{name}.png').read_bytes()).decode() for name in names}
template=(OUT/'preview_template.html').read_text(encoding='utf-8')
fragment=template.replace('__DESIGN__',json.dumps(d,ensure_ascii=False,separators=(',',':'))).replace('__ART__',json.dumps(art,separators=(',',':')))
assert len(fragment.encode())<1024*1024
VIZ.mkdir(parents=True,exist_ok=True)
(VIZ/'france-cold-war.html').write_text(fragment,encoding='utf-8')
(OUT/'PREVIEW.html').write_text('<!doctype html>\n<!-- IMPERIA COLD WAR — France 1970 external approval preview. -->\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>IMPERIA COLD WAR: France concept</title><style>body{margin:0;background:#151916}</style></head><body>'+fragment+'</body></html>',encoding='utf-8')
catalog=['IMPERIA COLD WAR','', '# France 1970 replacement concept: complete focus catalogue','',d['status'],'','All amounts are proposed balance. Coordinates use the current native 96 x 130 focus grid. All prerequisites inside a group are OR; separate groups are AND. Programmes are not runtime implementation.','']
for g in d['groups']:
    catalog+=['## '+g['title'],'',g['context'],'']
    for n in [n for n in d['nodes'] if n['group']==g['id']]:
        catalog+=['### '+n['title'],'',f"`{n['id']}` | ({n['x']}, {n['y']}) | {n['days']} days | {n['lifetime']}",'',n['description'],'','Requirements: '+('; '.join(n['conditions']) or 'Shared national programme')+'.', 'Prerequisites: '+(' AND '.join('('+' OR '.join(p)+')' for p in n['prerequisites']) or 'None')+'.','Exclusive: '+(', '.join(n['exclusions']) or 'None')+'.','', '```json',json.dumps(n['effects'],ensure_ascii=False,indent=2),'```','']
        if n.get('offer'):
            catalog+=['**If they accept**','', '```json',json.dumps(n['offer'],ensure_ascii=False,indent=2),'```','']
(OUT/'FOCUS_CATALOGUE.md').write_text('\n'.join(catalog),encoding='utf-8')
print(f'Preview: {len(fragment.encode()):,} bytes; {len(d["nodes"])} inspectable focuses. Catalogue updated.')
