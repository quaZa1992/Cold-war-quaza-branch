# IMPERIA CW — Cold War: egypt 1970 — quality preview 20261020.
"""Source-faithful EGY quality-pass previews, without generating game content.

Resolves live AST coordinates/anchors and native icon/title/font textures.
Connector elbows and two-line label wrapping approximate the closed renderer.
"""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import re
import runpy

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
OUT = ROOT/'docs/tree_quality_audit_20261020/previews'
OUT.mkdir(parents=True,exist_ok=True)
api=runpy.run_path(str(ROOT/'tools/egypt_1970/apply_quality_merges_20261020.py'))
parse,first,values,walk=(api[k] for k in ('parse','first','values','walk'))
tree_path=ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt'
foci={first(n,'id'):n for k,_,n in walk(parse(tree_path.read_text(encoding='utf-8')))
      if k=='focus' and isinstance(n,list)}
loc={}
for p in (ROOT/'localisation/english').glob('*EGY*.yml'):
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        m=re.match(r'\s*([^\s:#]+):\d*\s*"(.*)"\s*$',line)
        if m:loc[m[1]]=m[2]

# Actual grid and item geometry from the loaded mod GUI.
gui=(ROOT/'interface/nationalfocusview.gui').read_text(encoding='utf-8')
m=re.search(r'name\s*=\s*"focus_spacing"\s*position\s*=\s*\{\s*x\s*=\s*(\d+)\s*y\s*=\s*(\d+)',gui)
SX,SY=map(int,m.groups())
sprites={}
for base in [GAME,MD,ROOT]:
    for p in (base/'interface').glob('*.gfx'):
        t=p.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'name\s*=\s*"([^"\n]+)"\s*\n\s*texturefile\s*=\s*"([^"\n]+)"',t,re.I):
            sprites[m[1]]=m[2]


def asset(relative):
    for base in [ROOT,MD,GAME]:
        p=base/relative
        if p.is_file():return p
    raise FileNotFoundError(relative)


@lru_cache(None)
def icon(name):
    path=sprites.get(name) or sprites.get('GFX_goal_'+name) or sprites.get('GFX_'+name)
    if not path:raise KeyError('Unresolved native sprite '+name)
    return Image.open(asset(path)).convert('RGBA')


@lru_cache(None)
def position(fid):
    n=foci[fid];x=float(first(n,'x',0));y=float(first(n,'y',0));a=first(n,'relative_position_id')
    if a:
        ax,ay=position(a);x+=ax;y+=ay
    return x,y


class BitmapFont:
    def __init__(self):
        self.glyphs={};self.kern={}
        p=asset('gfx/fonts/hoi_16mbs.fnt')
        for line in p.read_text(encoding='utf-8').splitlines():
            attrs={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
            if line.startswith('char '):self.glyphs[attrs['id']]=attrs
            elif line.startswith('kerning '):self.kern[(attrs['first'],attrs['second'])]=attrs['amount']
        self.atlas=Image.open(asset('gfx/fonts/hoi_16mbs.dds')).convert('RGBA')
    def width(self,text):
        return sum(self.glyphs.get(ord(c),self.glyphs[ord('?')])['xadvance'] for c in text)+sum(self.kern.get((ord(a),ord(b)),0) for a,b in zip(text,text[1:]))
    def draw(self,im,text,x,y):
        previous=None
        for c in text:
            g=self.glyphs.get(ord(c),self.glyphs[ord('?')]);x+=self.kern.get((previous,ord(c)),0)
            tile=self.atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
            im.alpha_composite(tile,(round(x+g['xoffset']),round(y+g['yoffset'])))
            x+=g['xadvance'];previous=ord(c)
    def wrap(self,text):
        lines=['']
        for word in text.split():
            candidate=(lines[-1]+' '+word).strip()
            if self.width(candidate)>147 and lines[-1]:lines.append(word)
            else:lines[-1]=candidate
        return lines


FONT=BitmapFont()
PLATE=Image.open(asset('gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')).convert('RGBA')
TITLE=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',23)
CAPTION=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
missing=set()


@lru_cache(None)
def tile(fid):
    n=foci[fid];im=Image.new('RGBA',(200,150))
    try:picture=icon(first(n,'icon'))
    except (KeyError,FileNotFoundError) as e:
        missing.add(str(e));picture=Image.new('RGBA',(90,85))
        ImageDraw.Draw(picture).text((15,28),'MISSING',fill='red')
    im.alpha_composite(picture,(round(100-picture.width/2),round(42-picture.height/2)))
    im.alpha_composite(PLATE,(round(100-PLATE.width/2),62))
    lines=FONT.wrap(loc.get(fid,fid));top=82-(len(lines)*16)/2
    for i,line in enumerate(lines):FONT.draw(im,line,100-FONT.width(line)/2,top+i*16)
    return im


def render(name,bounds,scale=1,highlights=()):
    x0,y0,x1,y1=bounds;margin=110;header=100
    w=round((x1-x0)*SX*scale)+2*margin
    h=round((y1-y0)*SY*scale)+header+margin
    im=Image.new('RGBA',(w,h),(31,33,29,255));draw=ImageDraw.Draw(im)
    point=lambda fid:(margin+(position(fid)[0]-x0)*SX*scale,header+(position(fid)[1]-y0)*SY*scale)
    for fid,n in foci.items():
        x,y=position(fid)
        if not x0-2<=x<=x1+2 or not y0-2<=y<=y1+2:continue
        tx,ty=point(fid)
        for group in values(n,'prerequisite'):
            for parent in values(group,'focus'):
                if parent not in foci:continue
                px,py=point(parent);gutter=(py+ty)/2
                draw.line([(px,py+104*scale),(px,gutter),(tx,gutter),(tx,ty+5*scale)],
                          fill=(142,157,163),width=max(1,round(2*scale)))
        for other in values(first(n,'mutually_exclusive',[]),'focus'):
            if other not in foci or other<fid:continue
            ox,oy=point(other)
            if abs(oy-ty)<1:
                left,right=sorted([tx,ox]);line_y=ty+42*scale
                draw.line([(left+58*scale,line_y),(right-58*scale,line_y)],
                          fill=(182,95,70),width=max(1,round(2*scale)))
                for cx,direction in [(left+58*scale,1),(right-58*scale,-1)]:
                    draw.line([(cx+direction*7*scale,line_y-5*scale),(cx,line_y),
                               (cx+direction*7*scale,line_y+5*scale)],
                              fill=(213,126,80),width=max(1,round(2*scale)))
    for fid in foci:
        x,y=position(fid)
        if x0<=x<=x1 and y0<=y<=y1:
            px,py=point(fid);t=tile(fid)
            if scale!=1:t=t.resize((max(1,round(t.width*scale)),max(1,round(t.height*scale))),Image.Resampling.LANCZOS)
            im.alpha_composite(t,(round(px-t.width/2),round(py)))
    for box in highlights:
        ax,ay,bx,by=box
        draw.rectangle((margin+(ax-x0)*SX*scale,header+(ay-y0)*SY*scale,
                        margin+(bx-x0)*SX*scale,header+(by-y0)*SY*scale),outline=(228,182,91),width=2)
    draw.rectangle((0,0,w,82),fill=(20,25,26))
    draw.text((20,12),name.replace('_',' '),font=TITLE,fill=(235,235,222))
    draw.text((20,45),f'Live EGY AST | native icons, titleplate and hoi_16mbs bitmap font | grid {SX} x {SY} px | scale {scale:.3f}',font=CAPTION,fill=(176,195,199))
    draw.text((20,65),'Source preview; connector elbow selection and text wrapping approximate HOI4. No engine rendering claimed.',font=CAPTION,fill=(176,195,199))
    path=OUT/(name+'.png');im.convert('RGB').save(path)
    return dict(file=str(path.relative_to(ROOT)),size=[w,h],world_bounds=bounds,scale=scale)


if __name__=='__main__':
    points=list(map(position,foci));xs,ys=zip(*points)
    full=(min(xs)-1,min(ys)-1,max(xs)+1,max(ys)+1)
    s=min(2400/((full[2]-full[0])*SX),1500/((full[3]-full[1])*SY))
    pages=[render('EGY_full_tree_overview',full,s,[(0,10,68,25)]),
           render('EGY_ASU_TP_neighbors',(0,10,68,25)),
           render('EGY_TP_detail',(22,11,43,25))]
    data=dict(source_sha256=hashlib.sha256(tree_path.read_bytes()).hexdigest(),focuses=len(foci),
              spacing=[SX,SY],gui_source='interface/nationalfocusview.gui:448,574',font='hoi_16mbs',
              font_metadata='Ubuntu16bold bitmap atlas, game source',previews=pages,
              unresolved_sprites=sorted(missing),limits=['Closed-source connector routing approximated by orthogonal midpoint elbows.',
                  'Label wrapping uses native glyph metrics with two-line-style centring; exact engine layout is untested.',
                  'Full-tree overview is deliberately scaled; use detail images for readable labels.',
                  'Off-view prerequisite lines continue beyond branch crops; inspect full overview for context.'])
    (OUT/'EGY_preview_manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data,indent=2))
