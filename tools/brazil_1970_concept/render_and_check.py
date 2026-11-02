# IMPERIA COLD WAR — Source-bound native-art renders and independent concept checks.
from pathlib import Path
from collections import defaultdict
from functools import lru_cache
import hashlib, json, re
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parents[2]/'docs/brazil_1970_concept'
D=json.loads((OUT/'concept.json').read_text(encoding='utf-8'))
N={n['key']:n for n in D['nodes']}
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
heading=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12)
COL=(23,29,27,255);INK=(233,228,213,255);LINE=(169,155,117,255)
title_issues=[dict(key=n['key'],title=n['title'],width=round(font.getlength(n['title']),2)) for n in N.values() if font.getlength(n['title'])>147]

@lru_cache(None)
def histories(k):
    n=N[k];sets=[frozenset([k])]
    for block in n['prerequisites']:
        choices=[s for parent in block for s in histories(parent)]
        merged=[]
        for s in sets:
            for t in choices:
                u=s|t
                if all(not (set(N[a]['exclusions'])&u) for a in u):merged.append(u)
        sets=list(set(merged))
    return tuple(sets)
unreachable=[k for k in N if not histories(k)]

def segments(n,p):
    x1,y1=p['x']*96+82.5,p['y']*130+111
    x2,y2=n['x']*96+82.5,n['y']*130
    return [((x1,y1),(x1,y2-1)),((x1,y2-1),(x2,y2-1)),((x2,y2-1),(x2,y2))]
def hits(s,r):
    (ax,ay),(bx,by)=s;l,t,rgt,b=r
    return (l<ax<rgt and max(min(ay,by),t)<min(max(ay,by),b)) if ax==bx else (t<ay<b and max(min(ax,bx),l)<min(max(ax,bx),rgt))
cross=[]
for n in N.values():
    for parent in n['prerequisites']:
        for k in parent:
            ss=segments(n,N[k])
            for third in N.values():
                if third['key'] in (k,n['key']):continue
                box=(third['x']*96,third['y']*130,third['x']*96+165,third['y']*130+128)
                if any(hits(s,box) for s in ss):cross.append(dict(parent=k,child=n['key'],through=third['key']))

topologies=defaultdict(list)
for g in D['groups']:
    if g['slot'] is None:continue
    ns=[n for n in N.values() if n['group']==g['id']];ix={n['key']:i for i,n in enumerate(ns)}
    signature=json.dumps([dict(parents=[[ix[k] for k in p] for p in n['prerequisites']],ex=[ix[k] for k in n['exclusions']],x=n['x']-g['x'],y=n['y']-g['y']) for n in ns],sort_keys=True)
    topologies[signature].append(g['id'])
copies=[v for v in topologies.values() if len(v)>1]

art={p.stem:Image.open(p).convert('RGBA') for p in (OUT/'art').glob('*.png')}
def render(keys,name,scale=1,labels=True):
    ns=[N[k] for k in keys]
    minx=min(n['x']*96 for n in ns)-24;miny=min(n['y']*130 for n in ns)-88
    maxx=max(n['x']*96 for n in ns)+189;maxy=max(n['y']*130 for n in ns)+160
    im=Image.new('RGBA',(round(maxx-minx),round(maxy-miny)),COL);draw=ImageDraw.Draw(im)
    def pt(x,y):return (round(x-minx),round(y-miny))
    for n in ns:
        for block in n['prerequisites']:
            for k in block:
                if k in keys:
                    for a,b in segments(n,N[k]):draw.line([pt(*a),pt(*b)],fill=LINE,width=2)
        for k in n['exclusions']:
            if k in keys and n['key']<k:
                a=N[k];left,right=sorted([n,a],key=lambda a:a['x'])
                draw.line([pt(left['x']*96+166,left['y']*130+91),pt(right['x']*96-2,right['y']*130+91)],fill=(207,145,126),width=2)
    for n in ns:
        x,y=n['x']*96,n['y']*130
        sprite=art[n['icon']].copy();sprite.thumbnail((108,82),Image.Resampling.LANCZOS)
        im.alpha_composite(sprite,pt(x+82.5-sprite.width/2,y))
        if labels:
            bar=art['GFX_focus_can_start' if n['group']=='military' or next(g for g in D['groups'] if g['id']==n['group'])['slot'] is None else 'GFX_focus_unavailable'].resize((164,50),Image.Resampling.LANCZOS)
            im.alpha_composite(bar,pt(x,y+60));draw.text(pt(x+82.5,y+85),n['title'],font=font,fill=INK,anchor='mm',stroke_width=0)
    if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);draw=ImageDraw.Draw(im)
    for g in D['groups']:
        visible=[n for n in ns if n['group']==g['id']]
        if not visible:continue
        x=(min(n['x'] for n in visible)*96-minx)*scale;y=(min(n['y'] for n in visible)*130-miny)*scale
        draw.text((round(x),round(y)-20),g['title'],font=small if scale<1 else heading,fill=INK)
    im.convert('RGB').save(OUT/name,optimize=True)
    return dict(file=name,width=im.width,height=im.height)
renders=[]
renders.append(render(set(N),'PREVIEW_OVERVIEW.png',.25,False))
for key in ('military','mdb','pt','pdt','psdb','pcb','prn','ptb_late','society','economy','energy','defence','diplomacy'):
    renders.append(render({n['key'] for n in N.values() if n['group']==key},'PREVIEW_'+key+'.png'))
renders.append(render({n['key'] for n in N.values() if n['group'] in ('military','arena','mdb')},'PREVIEW_POLITICAL_NEIGHBOURS.png'))
summary=dict(project='IMPERIA COLD WAR',concept_sha256=hashlib.sha256((OUT/'concept.json').read_bytes()).hexdigest(),kind='Static source and Pillow native-art reconstruction. No browser or HOI4 test.',focuses=len(N),title_overflow=title_issues,unreachable=unreachable,connector_through_third_party_card=cross,duplicate_political_topologies=copies,native_shortcuts=len(D['navigation']['shortcuts']),renders=renders)
(OUT/'RENDER_CHECKS.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='renders'},indent=2))
