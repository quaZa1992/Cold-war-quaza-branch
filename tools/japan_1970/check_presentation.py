# IMPERIA CW — Cold War: Japan presentation regressions and gameplay preservation.
"""Bounded static QA; native connector routing and hover still need the engine."""
import json
from pathlib import Path
from PIL import ImageFont
from check_script_grammar import parse
from presentation import read_focuses, semantic, field
from layout import CONTINUOUS_POSITION
import re

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'staging/graph'


def intersects(a,b,box):
    """Open interior segment/rectangle overlap, using a Liang–Barsky clip."""
    lo,hi=0.,1.
    x0,y0,x1,y1=box
    for p,q in ((-(b[0]-a[0]),a[0]-x0), (b[0]-a[0],x1-a[0]),
                (-(b[1]-a[1]),a[1]-y0), (b[1]-a[1],y1-a[1])):
        if p==0:
            if q<=0:return False
        elif p<0:lo=max(lo,q/p)
        else:hi=min(hi,q/p)
    return lo<hi and hi>0 and lo<1


def main():
    errors=[]
    before=read_focuses((STAGE/'before_polish_focus_tree.txt').read_text(encoding='utf-8'))
    current=read_focuses((STAGE/'focus_tree.txt').read_text(encoding='utf-8'))
    if before.keys()!=current.keys(): errors.append('Focus IDs changed')
    for ident,n in current.items():
        old=before[ident]
        if semantic(old['entries'],('x','y','relative_position_id','completion_reward','icon')) != semantic(n['entries'],('x','y','relative_position_id','completion_reward','icon')):
            errors.append(ident+': gameplay/gates changed')
        for data in (old,n):
            reward=field(data['entries'],'completion_reward')
            data['payout']=semantic([e for e in reward if e.key=='hidden_effect'])
        if old['payout']!=n['payout']:errors.append(ident+': guarded payout changed')
    boxes={k:(n['globalX']*96-82.5,n['globalY']*130,n['globalX']*96+82.5,n['globalY']*130+128) for k,n in current.items()}
    keys=list(current)
    for i,k in enumerate(keys):
        a=boxes[k]
        for other in keys[i+1:]:
            b=boxes[other]
            if max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3]):
                errors.append(f'Card overlap: {k} / {other}')
    exclusive=[]
    for k,n in current.items():
        x,y=n['globalX']*96,n['globalY']*130
        for other in n['exclusive']:
            if other<k:continue
            o=current[other]; ox,oy=o['globalX']*96,o['globalY']*130
            if y!=oy:errors.append('Uneven exclusive row: '+k)
            a,b=(min(x,ox)+83,y+68),(max(x,ox)-83,y+68)
            exclusive.append((k,other,a,b))
            for third,box in boxes.items():
                if third not in (k,other) and intersects(a,b,box):errors.append(f'Exclusion crosses card: {k} / {other} through {third}')
    # Straight center routes are a conservative diagnostic, not the engine path.
    for k,n in current.items():
        b=(n['globalX']*96,n['globalY']*130)
        for group in n['parents']:
            for parent in group:
                p=current[parent];a=(p['globalX']*96,p['globalY']*130+128)
                if p['globalY']>=n['globalY']:errors.append('Backward prerequisite: '+k)
                for third,box in boxes.items():
                    if third not in (k,parent) and intersects(a,b,box):errors.append(f'Prerequisite crosses card: {parent} -> {k} through {third}')
                for left,right,e1,e2 in exclusive:
                    if k in (left,right) or parent in (left,right):continue
                    if a[1]<e1[1]<b[1]:
                        t=(e1[1]-a[1])/(b[1]-a[1]); x=a[0]+t*(b[0]-a[0])
                        if e1[0]<x<e2[0]:errors.append(f'Prerequisite crosses exclusion: {parent} -> {k}')
    px,py=CONTINUOUS_POSITION
    panel=(px,py,px+770,py+380)
    for ident,box in boxes.items():
        if max(box[0],panel[0])<min(box[2],panel[2]) and max(box[1],panel[1])<min(box[3],panel[3]):errors.append('Continuous panel covers '+ident)
    loc=dict(re.findall(r'(?m)^\s*(\w+):\s*"([^"\n]*)"',(STAGE/'focus_l_english.yml').read_text(encoding='utf-8-sig')))
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for ident in current:
        if font.getlength(loc[ident])>147:errors.append('Title exceeds approximate 147px name field: '+ident)
    manifest=json.loads((STAGE/'presentation_manifest.json').read_text(encoding='utf-8'))
    import hashlib
    if manifest['focus_sha256']!=hashlib.sha256((STAGE/'focus_tree.txt').read_bytes()).hexdigest():errors.append('Preview is stale')
    print(f'Presentation: {len(current)} focuses; protected gameplay/payouts, cards, exclusions, routes, panel and titles; {len(errors)} findings')
    for error in errors:print('ERROR:',error)
    return bool(errors)


if __name__=='__main__':raise SystemExit(main())
