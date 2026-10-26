# IMPERIA CW — Cold War: iraq 1970 concept — native font.
"""Read the inherited native MD/HOI4 UbuntuBold16 atlas without changing game fonts."""
from pathlib import Path
from PIL import Image
import re
from functools import lru_cache

FONT=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt')
ATLAS=FONT.with_suffix('.dds')
GLYPHS={};KERNINGS={}
for line in FONT.read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('char '):
        row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};GLYPHS[row['id']]=row
    if line.startswith('kerning '):
        row={k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)};KERNINGS[(row['first'],row['second'])]=row['amount']

def width(s):
    return sum(GLYPHS.get(ord(c),GLYPHS[63])['xadvance'] for c in s)+sum(KERNINGS.get((ord(a),ord(b)),0) for a,b in zip(s,s[1:]))

def concise(s):
    candidates=[s]
    for prefix in ['The ','A ','An ','Negotiate ','Offer ','Build ','Fund ','Review ','Protect ','Train ','Organize ','Convene ','Expand ','Develop ','Maintain ','Publish ','Recognize ','Appoint ','Enforce ','Support ','Restore ','Improve ','Count ','Survey ','Connect ','Retain ','Explore ','Implement ','Guarantee ','Prepare ','Require ','Bring ','Measure ','Select ','Return ','Open ','Debate ','Define ','Renew ','Deliver ','Separate ','Audit ','Rebuild ','Seek ']:
        for value in list(candidates):
            if value.startswith(prefix):candidates.append(value[len(prefix):])
    for value in list(candidates):
        for prefix in ['A Working ','A Common ','A National ','A Professional ','A Permanent ','A Costed ','A Funded ','A Published ','A Negotiated ','An Audited ','A Limited ','A Defined ','An Iraqi ','A Budget for ','A Register of ','A Policy of ','The Cost of ','A Network of ','The Presidency of ','A Crown under ','The Surviving ']:
            if value.startswith(prefix):candidates.append(value[len(prefix):])
    return next((v for v in candidates if width(v)<=143),min(candidates,key=width))

@lru_cache(maxsize=1)
def font_atlas():return Image.open(ATLAS).convert('RGBA')

@lru_cache(maxsize=512)
def raster(s):
    atlas=font_atlas();image=Image.new('RGBA',(147,20))
    x=(147-width(s))//2;previous=None
    for c in s:
        cp=ord(c);g=GLYPHS.get(cp,GLYPHS[63]);x+=KERNINGS.get((previous,cp),0)
        crop=atlas.crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
        image.alpha_composite(crop,(x+g['xoffset'],2+g['yoffset']))
        x+=g['xadvance'];previous=cp
    return image
