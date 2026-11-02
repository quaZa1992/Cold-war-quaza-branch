# IMPERIA COLD WAR — approval preview using the installed native font.
from pathlib import Path
from functools import lru_cache
import re
from PIL import Image

FONT = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt')
GLYPHS, KERNINGS = {}, {}
for line in FONT.read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('char '):
        row = {k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
        GLYPHS[row['id']] = row
    elif line.startswith('kerning '):
        row = {k:int(v) for k,v in re.findall(r'(\w+)=(-?\d+)',line)}
        KERNINGS[row['first'], row['second']] = row['amount']

def width(s):
    return sum(GLYPHS.get(ord(c),GLYPHS[63])['xadvance'] for c in s) + sum(KERNINGS.get((ord(a),ord(b)),0) for a,b in zip(s,s[1:]))

@lru_cache(maxsize=1)
def atlas():
    return Image.open(FONT.with_suffix('.dds')).convert('RGBA')

def raster(s):
    assert width(s) <= 143, (s,width(s))
    image = Image.new('RGBA',(147,20))
    x, previous = (147-width(s))//2, None
    for c in s:
        cp = ord(c); g = GLYPHS.get(cp,GLYPHS[63]); x += KERNINGS.get((previous,cp),0)
        crop = atlas().crop((g['x'],g['y'],g['x']+g['width'],g['y']+g['height']))
        image.alpha_composite(crop,(x+g['xoffset'],2+g['yoffset']))
        x += g['xadvance']; previous = cp
    return image
