"""Read the three requested MD reference trees and inventory existing artwork."""
from pathlib import Path
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DOC=ROOT/'docs/israel_1970_design'
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
def blocks(source,key):
    clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',lambda m:' '*len(m[0]),source)
    for match in re.finditer(r'\b'+key+r'\s*=\s*\{',clean):
        start=match.end();end=start;depth=1
        while depth:
            depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
        yield source[start:end-1].strip()
audit={}
for name,file in [('generic','00_generic.txt'),('russia','05_russia.txt'),('israel','05_israel.txt')]:
    source=(MD/'common/national_focus'/file).read_text(encoding='utf-8-sig')
    records=[]
    for block in blocks(source,'focus'):
        records.append({'id':re.search(r'\bid\s*=\s*(\w+)',block)[1],
                        'icon':re.search(r'\bicon\s*=\s*(\w+)',block)[1],
                        'rewards':list(blocks(block,'completion_reward'))})
    audit[name]={'source':str(MD/'common/national_focus'/file),'focuses':records}
(DOC/'reward_reference_review.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
data=json.loads((HERE/'design_source.json').read_text(encoding='utf-8'))
baseline=HERE/'reward_revision_baseline.json'
if not baseline.exists():baseline.write_text(json.dumps({n['id']:{k:n[k] for k in ('xy','group','prerequisites','mutually_exclusive','reward','modifiers','icon')} for n in data['nodes']},indent=2),encoding='utf-8')
for group in ('state','economy','society','defense','diplomacy','territories'):
    print('\n'+group.upper())
    for n in (n for n in data['nodes'] if n['group']==group):print(n['id'].removeprefix('ISR70_')+' | '+n['label']+' | '+str(n['modifiers'])+' | '+n['reward'].replace('\n','; '))
print('\nReferences: '+', '.join(k+': '+str(len(v['focuses'])) for k,v in audit.items()))
