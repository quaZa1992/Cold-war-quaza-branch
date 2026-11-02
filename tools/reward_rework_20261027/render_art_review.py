# IMPERIA COLD WAR — Emitted-tree artwork verification views.
"""Use current focus icons, coordinates, English titles and native MD frames.

This is a source-derived preview; line routing and title wrapping approximate
the game. Existing artwork is reused without altering its binary assets.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/tech_art_review_20261027'
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values


def main():
    sprites = {}
    for path in (ROOT / 'interface').glob('*.gfx'):
        sprites.update(re.findall(r'spriteType\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*texture[fF]ile\s*=\s*"([^"]+)"', path.read_text(encoding='utf-8-sig')))
    font = (GAME / 'gfx/fonts/hoi_16mbs.fnt').read_text(encoding='utf-8')
    glyphs = {}
    for line in font.splitlines():
        if line.startswith('char id='):
            record = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
            glyphs[record['id']] = record
    atlas = Image.open(GAME / 'gfx/fonts/hoi_16mbs.dds').convert('RGBA')
    bar = Image.open(GAME / 'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')

    def label(canvas, text, x, y):
        records = [glyphs.get(ord(c), glyphs[ord('?')]) for c in text]
        x -= sum(g['xadvance'] for g in records) // 2
        for g in records:
            tile = atlas.crop((g['x'], g['y'], g['x'] + g['width'], g['y'] + g['height']))
            canvas.alpha_composite(tile, (x + g['xoffset'], y + g['yoffset']))
            x += g['xadvance']

    evidence = []
    for tag, branch, seeds in (
        ('NKO', 'industry', ['COLDWAR_NKO_heavy_priority', 'COLDWAR_NKO_light_priority', 'COLDWAR_NKO_balanced_priority', 'COLDWAR_NKO_steelworks', 'COLDWAR_NKO_food_district', 'COLDWAR_NKO_machine_tools']),
        ('KOR', 'industry', ['COLDWAR_KOR_heavy_chemical_drive', 'COLDWAR_KOR_pohang_foundry', 'COLDWAR_KOR_electronics_priority', 'COLDWAR_KOR_shipbuilding_priority', 'COLDWAR_KOR_machinery_priority']),
        ('JAP', 'technology', ['COLDWAR_JAP_1970_communications_grid', 'COLDWAR_JAP_1970_microelectronics_capacity', 'COLDWAR_JAP_1970_electronics_exports']),
        ('JAP', 'energy', ['COLDWAR_JAP_1970_nuclear_expansion', 'COLDWAR_JAP_1970_distributed_power', 'COLDWAR_JAP_1970_reactor_siting', 'COLDWAR_JAP_1970_grid_storage']),
    ):
        source = ROOT / f'common/national_focus/COLDWAR_{tag}_1970_focus.txt'
        nodes = {first(n, 'id'): n for n in values(first(parse(source.read_text(encoding='utf-8')), 'focus_tree'), 'focus')}
        coordinates = {}

        def xy(identifier):
            if identifier not in coordinates:
                node = nodes[identifier]
                x, y = float(first(node, 'x')), float(first(node, 'y'))
                anchor = first(node, 'relative_position_id')
                if anchor:
                    ax, ay = xy(anchor)
                    x += ax
                    y += ay
                coordinates[identifier] = x, y
            return coordinates[identifier]

        for identifier in nodes:
            xy(identifier)
        xmin, xmax = min(xy(i)[0] for i in seeds) - 1, max(xy(i)[0] for i in seeds) + 1
        ymin, ymax = min(xy(i)[1] for i in seeds) - 1, max(xy(i)[1] for i in seeds) + 1
        selected = {i for i in nodes if xmin <= xy(i)[0] <= xmax and ymin <= xy(i)[1] <= ymax}
        canvas = Image.new('RGBA', (int((xmax-xmin)*96 + 240), int((ymax-ymin)*130 + 205)), (36, 37, 32, 255))
        draw = ImageDraw.Draw(canvas)
        titles = {}
        for path in (ROOT / 'localisation/english').glob(f'COLDWAR_{tag}*.yml'):
            titles.update(re.findall(r'(?m)^\s*(\w+):(?:\d+)?\s*"([^"\n]*)"', path.read_text(encoding='utf-8-sig')))

        def point(identifier):
            x, y = xy(identifier)
            return int((x-xmin)*96 + 120), int((y-ymin)*130 + 65)

        for identifier in selected:
            x, y = point(identifier)
            for group in values(nodes[identifier], 'prerequisite'):
                for parent in values(group, 'focus'):
                    if parent in selected:
                        px, py = point(parent)
                        middle = (py+119+y+5)//2
                        draw.line([(px, py+119), (px, middle), (x, middle), (x, y+5)], fill=(145, 153, 149), width=2)
        for identifier in sorted(selected):
            x, y = point(identifier)
            sprite = first(nodes[identifier], 'icon')
            path = ROOT / sprites[sprite]
            icon = Image.open(path).convert('RGBA')
            icon.thumbnail((112, 98))
            canvas.alpha_composite(icon, (x-icon.width//2, y))
            canvas.alpha_composite(bar, (x-bar.width//2, y+73))
            label(canvas, titles.get(identifier, identifier), x, y+91)
        name = f'{tag}_{branch}_icons.png'
        canvas.convert('RGB').save(OUT / name)
        evidence.append({'image': name, 'focus_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                         'ids': sorted(selected), 'grid': [96, 130]})
    (OUT / 'ART_PREVIEWS.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'engine_render': False,
        'native_art_font_and_titlebar': True, 'approximations': ['Connector routing', 'Title wrapping'],
        'views': evidence}, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
