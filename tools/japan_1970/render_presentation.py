# IMPERIA CW — Cold War: Japan focus presentation review from emitted script.
"""Native assets and GUI dimensions; Arial and connector routing approximate."""
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from presentation import read_focuses

root = Path(__file__).resolve().parent
game = root.parents[1]
vanilla = Path('C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')
donor = Path('C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/2777392649')
out = root / 'staging/graph'
source = out / 'focus_tree.txt'
nodes = read_focuses(source.read_text(encoding='utf-8'))
design = json.loads((root / 'approved_design.json').read_text(encoding='utf-8'))['design']
loc = (out / 'focus_l_english.yml').read_text(encoding='utf-8-sig')
titles = dict(re.findall(r'(?m)^\s*(\w+):\s*"([^"\n]*)"', loc))
sprites = {}
for path in (game / 'interface').glob('*.gfx'):
    sprites.update(re.findall(r'spriteType\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*texture[fF]ile\s*=\s*"([^"]+)"', path.read_text(encoding='utf-8-sig')))
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)
heading = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 21)
prefix = 'COLDWAR_JAP_1970_'


def fid(ident):
    return ident if ident.startswith(prefix) else prefix + ident


@lru_cache(None)
def asset(path):
    filename = next((base / path for base in (game, donor, vanilla) if (base / path).exists()), None)
    if not filename:
        raise ValueError('Missing art ' + path)
    return Image.open(filename).convert('RGBA')


def render(chosen, destination, title=None, overview=False):
    xmin, xmax = min(n['globalX'] for n in chosen), max(n['globalX'] for n in chosen)
    ymin, ymax = min(n['globalY'] for n in chosen), max(n['globalY'] for n in chosen)
    canvas = Image.new('RGBA', ((xmax-xmin)*96+220, (ymax-ymin)*130+220), (34, 35, 32, 255))
    draw = ImageDraw.Draw(canvas)
    def point(n):
        return 110+(n['globalX']-xmin)*96, 100+(n['globalY']-ymin)*130
    selected = {n['id'] for n in chosen}
    for n in chosen:
        x, y = point(n)
        for group in n['parents']:
            for ident in group:
                p = nodes[ident]
                px, py = point(p)
                middle = (py+90+y-30)//2
                draw.line([(px, py+90), (px, middle), (x, middle), (x, y-24)], fill='#829aa0', width=2)
        for other in n['exclusive']:
            if other in selected and other > n['id']:
                ox, oy = point(nodes[other])
                draw.line([(min(x,ox)+83,y+67),(max(x,ox)-83,oy+67)], fill='#d8b25c', width=3)
                cx=(x+ox)//2
                draw.polygon([(cx,y+60),(cx+7,y+67),(cx,y+74),(cx-7,y+67)], fill='#b7534d')
    for n in chosen:
        x,y=point(n)
        enabled = not n['parents'] and ('_mandate' not in n['id'] or n['id'].endswith('ldp_mandate'))
        state = 'can_start' if enabled else 'unavailable'
        bar = asset(sprites[f'GFX_focus_{state}'])
        canvas.alpha_composite(bar, (x-82,y+40))
        icon = asset(sprites[n['icon']])
        canvas.alpha_composite(icon, (x-icon.width//2,y+20-icon.height//2))
        draw.text((x,y+68), titles[n['id']], fill='#eee7d7', font=font, anchor='mm')
    if title:
        draw.text((14,10), title, fill='#eee7d7',font=heading)
    if overview:
        for s in design['sections']:
            section_nodes=[nodes[fid(n['id'])] for n in s['nodes']]
            x,y=point(section_nodes[0])
            draw.text((x,y-70),s['name'],fill='#e0c58c',font=heading,anchor='mm')
        canvas.thumbnail((2600,2000),Image.Resampling.LANCZOS)
    canvas.convert('RGB').save(destination)


for index, section in enumerate(design['sections']):
    render([nodes[fid(n['id'])] for n in section['nodes']], out / f'branch_{index}.png', section['name'])
render(list(nodes.values()),out/'overview.png',overview=True)
manifest={
    'focus_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'gui_grid_px':[96,130], 'item_container_px':[165,128],
    'approximations':['Arial 14 for hoi_16mbs','orthogonal connector routing','initial focus availability inferred for preview'],
    'layout_state':'All five party branches visible; governing-party availability still enforced in script',
    'nodes':[{k:v for k,v in n.items() if k!='entries'} for n in nodes.values()],
}
(out/'presentation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(f'Rendered overview and {len(design["sections"])} current branch views from {len(nodes)} emitted focuses.')
