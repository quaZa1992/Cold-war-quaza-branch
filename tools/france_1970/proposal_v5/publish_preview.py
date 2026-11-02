# IMPERIA COLD WAR — Package proposal data and existing focus art for inline review.
import base64
import io
import json
import re
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=Path('C:/Users/Enes/.codex/visualizations/2026/10/23/01a16840-34d5-7e60-8c3d-134a5e042a6a/coldwar_france_politics/france-programmes-v5.html')
D=json.loads((HERE/'proposal.json').read_text(encoding='utf-8'))
I=json.loads((HERE.parent/'icons.json').read_text(encoding='utf-8'))
D['icons']={}
for alias,art in I['focus_art'].items():
    path=ROOT/art['texture']
    im=Image.open(path).convert('RGBA')
    im.thumbnail((72,66),Image.Resampling.LANCZOS)
    buf=io.BytesIO();im.save(buf,format='PNG',optimize=True)
    D['icons'][alias]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode('ascii')
for n in D['nodes']:
    if n.get('offer_id'):
        o=next(o for o in D['offers'] if o['id']==n['offer_id'])
        suffix={'military_industry':'cooperation','civil_industry':'industry','science_energy':'research','civil_resilience':'civil_defence','commerce':'market','training':'army'}[o['family']]
        if o['partner']=='GER':suffix='germany'
        n['sprite']='GFX_COLDWAR_FRA_1970_'+suffix
    else:n['sprite']=I['focus_icons'][n['id']]
template=(HERE/'preview_template.html').read_text(encoding='utf-8')
assert template.count('__COLDWAR_DATA__')==1
text=template.replace('__COLDWAR_DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
assert len(text.encode('utf-8'))<1_000_000
OUT.write_text(text,encoding='utf-8',newline='\n')
print(json.dumps({'preview':str(OUT),'bytes':OUT.stat().st_size,'focuses':len(D['nodes']),'offers':len(D['offers'])}))
