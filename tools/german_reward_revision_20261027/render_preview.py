# IMPERIA COLD WAR — Source-derived German focus reward review views.
"""Render loaded coordinates, icons and English titles with native art.

These are review diagrams, not engine screenshots. Connector routing and title
wrapping approximate the game. Existing binary artwork is not modified.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/german_reward_revision_20261027'
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values


def main():
    sprites = {}
    for base in (GAME, MD, ROOT):
        for path in (base / 'interface').glob('*.gfx'):
            for name, texture in re.findall(r'spriteType\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*texturefile\s*=\s*"([^"]+)"', path.read_text(encoding='utf-8-sig'), re.I):
                sprites[name] = texture
    glyphs = {}
    for line in (GAME / 'gfx/fonts/hoi_16mbs.fnt').read_text(encoding='utf-8').splitlines():
        if line.startswith('char id='):
            g = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
            glyphs[g['id']] = g
    atlas = Image.open(GAME / 'gfx/fonts/hoi_16mbs.dds').convert('RGBA')
    bar = Image.open(GAME / 'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')
    icons = {}

    def icon(name):
        if name not in icons:
            texture = sprites[name]
            path = next(base / texture for base in (ROOT, MD, GAME) if (base / texture).is_file())
            item = Image.open(path).convert('RGBA')
            item.thumbnail((112, 98))
            icons[name] = item
        return icons[name]

    def text_width(text):
        return sum(glyphs.get(ord(c), glyphs[63])['xadvance'] for c in text)

    def label(text):
        canvas = Image.new('RGBA', (147, 40))
        lines = ['']
        for word in text.split():
            candidate = (lines[-1] + ' ' + word).strip()
            if text_width(candidate) > 147 and lines[-1]:
                lines.append(word)
            else:
                lines[-1] = candidate
        for row, line in enumerate(lines[:2]):
            x = (147-text_width(line))//2
            for c in line:
                g = glyphs.get(ord(c), glyphs[63])
                tile = atlas.crop((g['x'], g['y'], g['x']+g['width'], g['y']+g['height']))
                canvas.alpha_composite(tile, (x+g['xoffset'], row*16+g['yoffset']))
                x += g['xadvance']
        return canvas

    evidence = []
    for tag, windows in (
        ('GER', [('economy', (86, 99, 1, 7)), ('energy', (110, 121, 1, 7))]),
        ('DDR', [('economic_reform', (323, 337, 4, 10)), ('energy', (28, 39, 11, 17))]),
    ):
        path = ROOT / f'common/national_focus/COLDWAR_{tag}_1970_focus.txt'
        nodes = {first(n, 'id'): n for n in values(first(parse(path.read_text(encoding='utf-8')), 'focus_tree'), 'focus')}
        titles = {}
        for loc in (ROOT / 'localisation/english').glob(f'COLDWAR_{tag}*.yml'):
            titles.update(re.findall(r'(?m)^\s*(\w+):(?:\d+)?\s*"([^"\n]*)"', loc.read_text(encoding='utf-8-sig')))
        coords = {}

        def xy(identifier):
            if identifier not in coords:
                node = nodes[identifier]
                x, y = float(first(node, 'x')), float(first(node, 'y'))
                anchor = first(node, 'relative_position_id')
                if anchor:
                    ax, ay = xy(anchor)
                    x += ax
                    y += ay
                coords[identifier] = x, y
            return coords[identifier]

        for identifier in nodes:
            xy(identifier)
        overview = (min(x for x, y in coords.values())-1, max(x for x, y in coords.values())+1,
                    min(y for x, y in coords.values()), max(y for x, y in coords.values())+1)
        for branch, bounds in [('overview', overview)] + windows:
            xmin, xmax, ymin, ymax = bounds
            scale = min(1, 3600/((xmax-xmin)*96+240)) if branch == 'overview' else 1
            ids = {i for i in nodes if xmin <= xy(i)[0] <= xmax and ymin <= xy(i)[1] <= ymax}
            width, height = int(((xmax-xmin)*96+240)*scale), int(((ymax-ymin)*130+205)*scale)
            canvas = Image.new('RGBA', (width, height), (36, 37, 32, 255))
            draw = ImageDraw.Draw(canvas)

            def point(i):
                x, y = xy(i)
                return round(((x-xmin)*96+120)*scale), round(((y-ymin)*130+65)*scale)

            for i in sorted(ids):
                x, y = point(i)
                for group in values(nodes[i], 'prerequisite'):
                    for parent in values(group, 'focus'):
                        if parent in ids:
                            px, py = point(parent)
                            start, end = py+round(119*scale), y+round(5*scale)
                            middle = (start+end)//2
                            draw.line([(px, start), (px, middle), (x, middle), (x, end)], fill=(145, 153, 149), width=max(1, round(2*scale)))
                for group in values(nodes[i], 'mutually_exclusive'):
                    for other in values(group, 'focus'):
                        if other in ids and other > i:
                            ox, oy = point(other)
                            yy = y+round(100*scale)
                            draw.line([(min(x, ox)+round(84*scale), yy), (max(x, ox)-round(84*scale), yy)], fill=(166, 81, 66), width=max(1, round(2*scale)))
            for i in sorted(ids):
                x, y = point(i)
                item = icon(first(nodes[i], 'icon'))
                for art, dx, dy in ((item, -item.width/2, 0), (bar, -bar.width/2, 73), (label(titles.get(i, i)), -73.5, 91)):
                    if scale != 1:
                        art = art.resize((max(1, round(art.width*scale)), max(1, round(art.height*scale))), Image.Resampling.LANCZOS)
                    canvas.alpha_composite(art, (x+round(dx*scale), y+round(dy*scale)))
            filename = f'{tag}_{branch}.png'
            canvas.convert('RGB').save(OUT / filename)
            evidence.append({'image': filename, 'focus_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                             'ids': sorted(ids), 'scale': scale, 'grid': [96, 130], 'bounds': bounds})
    (OUT / 'PREVIEWS.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'engine_render': False,
        'native_art_font_and_titlebar': True, 'new_or_modified_binary_assets': False,
        'approximations': ['Connector routing', 'Two-line title wrapping'], 'views': evidence}, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'images': [view['image'] for view in evidence]}))


if __name__ == '__main__':
    main()
