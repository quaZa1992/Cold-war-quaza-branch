# IMPERIA CW — Cold War: iraq 1970 concept — render concept.
"""COLDWAR_IRQ: faithful coordinate preview and source-art provenance; no runtime writes."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64, hashlib, io, json, re
from native_font import GLYPHS,KERNINGS,ATLAS,raster

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'docs/design/iraq_1970'
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
data=json.loads((OUT/'COLDWAR_IRQ_1970_CONCEPT.json').read_text(encoding='utf-8'))

def registry():
    result={}
    for path in (ROOT/'interface').glob('*.gfx'):
        text=path.read_text(encoding='utf-8-sig',errors='replace')
        for match in re.finditer(r'\b(?:spriteType|SpriteType)\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s+texture[Ff]ile\s*=\s*"([^"]+)"',text):
            result[match[1]]=(match[2].replace('\\','/'),str(path.relative_to(ROOT)),text[:match.start()].count('\n')+1)
    return result

def uri(im):
    out=io.BytesIO();im.save(out,format='WEBP',lossless=True)
    return 'data:image/webp;base64,'+base64.b64encode(out.getvalue()).decode('ascii')

reg=registry();used=sorted(set(n['icon'] for n in data['nodes']));icons={};sources={};images={}
concept_art=json.loads((HERE/'assets/concept_art.json').read_text(encoding='utf-8'))
for name in used:
    if name in concept_art:
        art=concept_art[name];path=HERE/'assets'/art['source']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==art['source_sha256'], 'Changed supplied artwork '+name
        im=Image.open(path).convert('RGBA')
        assert list(im.size)==art['source_dimensions']
        im.thumbnail(tuple(art['preview_max_dimensions']),Image.Resampling.LANCZOS)
        sources[name]={**art,'texture':str(path),'definition':'tools/iraq_1970_concept/assets/concept_art.json','dimensions':list(im.size),'registered_in_game':False}
    else:
        assert name in reg, 'Unregistered sprite '+name
        rel,definition,line=reg[name];path=ROOT/rel
        if not path.exists(): path=GAME/rel
        im=Image.open(path).convert('RGBA')
        sources[name]={'texture':str(path),'definition':definition,'line':line,'dimensions':list(im.size)}
    images[name]=im
    icons[name]=uri(im)
assets={'icons':icons}
assets['font_atlas']=uri(Image.open(ATLAS).convert('RGBA'))
assets['font_glyphs']={k:[v['x'],v['y'],v['width'],v['height'],v['xoffset'],v['yoffset'],v['xadvance']] for k,v in GLYPHS.items()}
assets['font_kernings']={str(a)+','+str(b):v for (a,b),v in KERNINGS.items()}
for key,name in [('available','focus_can_start_bg'),('unavailable','focus_unavailable_bg'),('completed','focus_completed_bg')]:
    path=GAME/('gfx/interface/focusview/titlebar/'+name+'.dds')
    im=Image.open(path).convert('RGBA');assets[key]=uri(im)

fields=['id','title','narrative_title','group','xy','days','prerequisites','mutually_exclusive','icon','description','reward_summary','historical_status','available','requirement_contracts','effect_body','modifiers']
preview={k:data[k] for k in ['groups','decisions','starting_spirits','modifier_labels','programme_rules']}
preview['nodes']=[{k:n[k] for k in fields} for n in data['nodes']];preview['assets']=assets
for original,shown in zip(data['nodes'],preview['nodes']):
    if original['active_condition']!=original['available']:shown['active_condition']=original['active_condition']
for n in preview['nodes']:
    n['effect_body']='\n'.join(line for line in n['effect_body'].splitlines() if not line.lstrip().startswith('#'))
fragment=(HERE/'tree_fragment.html').read_text(encoding='utf-8')
fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="irq-data">'+json.dumps(preview,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+'</script>')
assert len(fragment.encode('utf-8'))<1_000_000, len(fragment.encode('utf-8'))
destination=VIZ/'iraq-1970-focus-concept.html';destination.write_text(fragment,encoding='utf-8')
(OUT/'ART_PROVENANCE.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')

# Standalone review copy, separate from the inline fragment; all images already embedded.
wrapper='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Iraq1970 Focus Concept</title><style>html{background:#152026;color:#eee;font:14px/1.4 Arial,sans-serif}body{margin:0;padding:12px}main{max-width:1024px;margin:auto}</style><main>'+fragment+'</main></html>'
(OUT/'PREVIEW.html').write_text(wrapper,encoding='utf-8')

font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
sheet=Image.new('RGB',(800,((len(used)+4)//5)*145),'#1b292f');draw=ImageDraw.Draw(sheet)
for i,name in enumerate(used):
    x=(i%5)*160;y=(i//5)*145;im=images[name]
    sheet.paste(im,(x+(160-im.width)//2,y+10),im)
    label='Saddam (user artwork)' if name in concept_art else name
    draw.text((x+5,y+110),label,font=font,fill='#e8e5d6')
sheet.save(OUT/'COLDWAR_IRQ_ART_CONTACT.png')

# Complete branches at one native pixel per source pixel, with real bitmap titles.
# The same absolute coordinates/edges as the emitted specimen are merely cropped.
titlebar=Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')
for group_key in ['state','baath','bakr','saddam','communists','aziz','oil','industry','agriculture','defence','war','iran_war']:
    selected=[n for n in data['nodes'] if n['group']==group_key]
    left=min(n['xy'][0]*96 for n in selected)-30;top=min(n['xy'][1]*130 for n in selected)-110
    right=max(n['xy'][0]*96 for n in selected)+205;bottom=max(n['xy'][1]*130 for n in selected)+130
    canvas=Image.new('RGBA',(right-left,bottom-top),'#22343c');draw=ImageDraw.Draw(canvas)
    byid={n['id']:n for n in data['nodes']}
    for n in selected:
        x=n['xy'][0]*96-left;y=n['xy'][1]*130-top
        for row in n['prerequisites']:
            for parent in row:
                p=byid[parent];px=p['xy'][0]*96-left;py=p['xy'][1]*130-top
                y1=py+90;y2=y-26;mid=(y1+y2)//2
                draw.line([(px+80,y1),(px+80,mid),(x+80,mid),(x+80,y2)],fill='#a2b2b5',width=2)
        for other in n['mutually_exclusive']:
            if other<n['id']:continue
            q=byid[other];qx=q['xy'][0]*96-left
            a=min(x,qx)+139;b=max(x,qx)+27;yy=y+20
            for xx in range(a,b,9):draw.line([(xx,yy),(min(xx+4,b),yy)],fill='#d9a287',width=2)
            draw.text(((a+b)//2-4,yy-20),'×',font=font,fill='#d9a287')
    for n in selected:
        x=n['xy'][0]*96-left;y=n['xy'][1]*130-top;im=images[n['icon']]
        canvas.alpha_composite(im,(int(x+87.5-im.width/2),int(y+20-im.height/2)))
        canvas.alpha_composite(titlebar,(x+5,y+40));canvas.alpha_composite(raster(n['title']),(x+15,y+58))
    g=next(g for g in data['groups'] if g['id']==group_key)
    draw.text((20,15),g['label']+' · CONCEPT',font=font,fill='#e3cf90')
    draw.text((20,39),'Native 96 × 130 grid · '+str(len(selected))+' focuses · '+g['shape'],font=font,fill='#c4cdcb')
    canvas.convert('RGB').save(OUT/('FULL_BRANCH_'+group_key+'.png'))
print(f'{destination}\n{len(fragment.encode("utf-8"))} bytes; {len(used)} icons, including {len(set(used)&set(concept_art))} concept-local user asset(s)')
