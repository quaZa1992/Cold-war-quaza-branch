# IMPERIA CW — Cold War: emitted North Korea tree preview with native title glyphs.
"""Render actual emitted coordinates/icons/localisation; connectors approximate HOI4."""
from pathlib import Path
import re,json,sys,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values
OUT=ROOT/'docs/COLDWAR_NKO_1970_concept/expansion'
OUT.mkdir(exist_ok=True)
GAME=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
source=ROOT/'common/national_focus/COLDWAR_NKO_1970_focus.txt'
rows=first(parse(source.read_text(encoding='utf-8')),'focus_tree')
nodes={first(v,'id'):v for k,_,v in rows if k=='focus'}
design=json.loads((Path(__file__).with_name('current_design.json')).read_text(encoding='utf-8'))
titles={n['id']:n['title'] for n in design['nodes']}
sprites=dict(re.findall(r'name\s*=\s*"([^"]+)"\s*\n\s*texturefile\s*=\s*"([^"]+)"',(ROOT/'interface/goals.gfx').read_text(encoding='utf-8-sig'),re.I))
fonttext=(GAME/'gfx/fonts/hoi_16mbs.fnt').read_text(encoding='utf-8')
glyphs={}
for line in fonttext.splitlines():
    if line.startswith('char id='):
        data={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};glyphs[data['id']]=data
atlas=Image.open(GAME/'gfx/fonts/hoi_16mbs.dds').convert('RGBA')
bar=Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')
coords={}
def xy(nid):
    if nid in coords:return coords[nid]
    n=nodes[nid];x=int(first(n,'x'));y=int(first(n,'y'));a=first(n,'relative_position_id')
    if a:ax,ay=xy(a);x+=ax;y+=ay
    coords[nid]=(x,y);return x,y
for nid in nodes:xy(nid)
def textwidth(text):return sum(glyphs[ord(c)]['xadvance'] for c in text)
def label(im,text,x,y):
    x-=textwidth(text)//2
    for c in text:
        g=glyphs[ord(c)];tile=atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
        im.alpha_composite(tile,(x+g['xoffset'],y+g['yoffset']));x+=g['xadvance']
def render(ids,name,scale=1):
    minx=min(coords[i][0] for i in ids);maxx=max(coords[i][0] for i in ids)
    miny=min(coords[i][1] for i in ids);maxy=max(coords[i][1] for i in ids)
    im=Image.new('RGBA',((maxx-minx)*96+240,(maxy-miny)*130+205),(36,37,32,255));draw=ImageDraw.Draw(im)
    def pos(i):x,y=coords[i];return (x-minx)*96+120,(y-miny)*130+65
    for i in ids:
        x,y=pos(i)
        for pg in values(nodes[i],'prerequisite'):
            for p in values(pg,'focus'):
                if p not in ids:continue
                px,py=pos(p);start=py+119;end=y+5;mid=(start+end)//2
                draw.line([(px,start),(px,mid),(x,mid),(x,end)],fill=(145,153,149),width=2)
        for other in values(first(nodes[i],'mutually_exclusive',[]),'focus'):
            if other not in ids or other<i:continue
            ox,oy=pos(other);yy=y+100
            draw.line([(min(x,ox)+84,yy),(max(x,ox)-84,yy)],fill=(116,151,126),width=2)
            cx=(x+ox)//2;draw.polygon([(cx,yy-6),(cx+5,yy),(cx,yy+6),(cx-5,yy)],fill=(177,73,62))
    for i in ids:
        x,y=pos(i);icon=Image.open(ROOT/sprites[first(nodes[i],'icon')]).convert('RGBA');icon.thumbnail((112,98))
        im.alpha_composite(icon,(x-icon.width//2,y));im.alpha_composite(bar,(x-bar.width//2,y+73));label(im,titles[i],x,y+91)
    if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    im.convert('RGB').save(OUT/name)
for group in design['groups']:
    render([n['id'] for n in design['nodes'] if n['group']==group['id']],'COLDWAR_NKO_'+group['id']+'.png')
render(list(nodes),'COLDWAR_NKO_current_overview.png',.24)
manifest={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'focuses':len(nodes),'leader_branch_focuses':sum(n['group']=='jongil' for n in design['nodes']),'grid':[96,130],'card_bounds':[165,128],'title_field':[147,20],'native_font':'hoi_16mbs','connector_routing':'approximate','engine_render':False,'positions':coords}
(OUT/'preview_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(OUT/'COLDWAR_NKO_current_overview.png')
