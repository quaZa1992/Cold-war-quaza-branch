# IMPERIA CW — Cold War: gcc 1970 — preview.
"""Independent emitted GCC geometry and native-art preview; no game writes.

Reads loaded host trees, shared focuses, native GUI/font/titlebars and actual
sprite textures. Lines simulate native orthogonal routing; engine unverified.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PREFIX = 'COLDWAR_GCC_'

spec = importlib.util.spec_from_file_location('gcc_independent_native_art', ROOT / 'tools/uae_1970/audit_layout.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
parse, one, fields = native.parse, native.one, native.fields


def source(path):
    return parse((ROOT / path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_loc(paths):
    result = {}
    for path in paths:
        result.update(native.read_loc(path))
    return result


def resolve(rows, tag):
    by = {one(f, 'id'): f for f in rows}
    result = {}
    def position(ident, trail=()):
        if ident in result:
            return result[ident]
        if ident in trail:
            raise ValueError('Cyclic anchor: ' + str(trail))
        focus = by[ident]
        xy = [float(one(focus, 'x', 0)), float(one(focus, 'y', 0))]
        if anchor := one(focus, 'relative_position_id'):
            parent = position(anchor, trail + (ident,))
            xy = [a + b for a, b in zip(xy, parent)]
        for offset in fields(focus, 'offset'):
            trigger = one(offset, 'trigger', [])
            if len(trigger) == 1 and trigger[0][0] == 'tag':
                if trigger[0][1] == tag:
                    xy[0] += float(one(offset, 'x', 0))
                    xy[1] += float(one(offset, 'y', 0))
            else:
                raise ValueError('Unmodelled conditional offset: ' + repr(trigger))
        result[ident] = xy
        return xy
    for ident in by:
        position(ident)
    return result


def overlap(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def main():
    shared_path = 'common/national_focus/COLDWAR_GCC_1970_shared.txt'
    shared = fields(source(shared_path), 'shared_focus')
    shared_by = {one(f, 'id'): f for f in shared}
    manifest = json.loads((HERE / 'manifest.json').read_text())
    expected = {n['id']: n for n in manifest['nodes']}
    original = {one(f, 'id'): f for f in fields(source('common/national_focus/gulf_shared.txt'), 'shared_focus')}
    translated = {n['native']: n['id'] for n in manifest['nodes']}
    errors, checked, positions, host_reports, images = [], [], {}, {}, []
    gulf_tags = {'SAU','KUW','QAT','BHR','OMA','UAE'}
    union_tags = set(fields(one(one(source('common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt'),
                                    'COLDWAR_UNI_union_tag'), 'OR'), 'original_tag'))
    if gulf_tags & union_tags:
        errors.append('Unexpected co-visible Union shared tree for Gulf tags')
    if set(shared_by) != set(expected):
        errors.append('Emitted/manifest ID mismatch')

    loc = load_loc(['localisation/english/COLDWAR_GCC_1970_l_english.yml',
                    'localisation/english/mdcw_1970_generic_focus_l_english.yml',
                    'localisation/english/COLDWAR_UAE_1970_focus_l_english.yml'])
    sprites = {}
    for path in ['interface/goals.gfx', 'interface/COLDWAR_GCC_1970.gfx',
                 'interface/COLDWAR_UAE_1970_goals.gfx']:
        for sprite in fields(one(source(path), 'spriteTypes'), 'spriteType'):
            sprites[one(sprite, 'name')] = one(sprite, 'texturefile', one(sprite, 'textureFile'))
    glyphs, kernings, atlas = native.glyph_data()
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
    bar_path = native.asset('gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')
    bar = Image.open(bar_path).convert('RGBA')
    art = {}
    for ident, focus in shared_by.items():
        expected_node = expected[ident]
        prereqs = [fields(c, 'focus') for c in fields(focus, 'prerequisite')]
        if prereqs != expected_node['prerequisites']:
            errors.append('Changed prerequisite groups: ' + ident)
        native_focus = original[expected_node['native']]
        native_prereqs = [[translated[parent] for parent in fields(c, 'focus')]
                          for c in fields(native_focus, 'prerequisite')]
        if prereqs != native_prereqs:
            errors.append('Native MD prerequisite groups not retained: ' + ident)
        if ident != 'COLDWAR_GCC_council' and any(one(focus, axis) != one(native_focus, axis) for axis in ['x', 'y']):
            errors.append('Relative fan differs from actual native MD: ' + ident)
        if float(one(focus, 'cost')) != expected_node['cost']:
            errors.append('Changed duration: ' + ident)
        title = loc[ident]
        if native.width(title, glyphs, kernings) > 147:
            errors.append('Title exceeds native147px field: ' + ident + ' ' + title)
        icon = one(focus, 'icon')
        path = ROOT / sprites[icon]
        if not path.is_file():
            errors.append('Missing texture: ' + icon)
        else:
            art[icon] = Image.open(path).convert('RGBA')

    def nodes(rows, tag):
        xy = resolve(rows, tag)
        return [{'id': one(f, 'id'), 'xy': xy[one(f, 'id')],
                 'title': loc.get(one(f, 'id'), one(f, 'id')),
                 'icon': one(f, 'icon'),
                 'prerequisites': [fields(c, 'focus') for c in fields(f, 'prerequisite')]} for f in rows]

    def icon_for(node):
        key = node['icon']
        if not isinstance(key, str):
            raise ValueError('Unmodelled conditional icon: ' + node['id'])
        if key not in art:
            texture = sprites.get(key)
            if texture is None:
                raise ValueError('Missing native sprite: ' + key)
            art[key] = Image.open(native.asset(texture)).convert('RGBA')
        return art[key]

    def render(rows, filename, heading, thumbnail=None):
        minx = min(n['xy'][0] for n in rows) * 96 - 35
        miny = min(n['xy'][1] for n in rows) * 130 - 110
        maxx = max(n['xy'][0] for n in rows) * 96 + 205
        maxy = max(n['xy'][1] for n in rows) * 130 + 140
        canvas = Image.new('RGBA', (round(maxx-minx), round(maxy-miny)), '#22343c')
        draw = ImageDraw.Draw(canvas)
        by = {n['id']: n for n in rows}
        for node in rows:
            x, y = node['xy'][0]*96-minx, node['xy'][1]*130-miny
            for clause in node['prerequisites']:
                for parent in clause:
                    if parent not in by:
                        continue
                    px, py = by[parent]['xy'][0]*96-minx, by[parent]['xy'][1]*130-miny
                    middle = (py+90+y-26)//2
                    draw.line([(px+80,py+90),(px+80,middle),(x+80,middle),(x+80,y-26)], fill='#9aabad', width=2)
        for node in rows:
            x, y = node['xy'][0]*96-minx, node['xy'][1]*130-miny
            icon = icon_for(node)
            canvas.alpha_composite(icon, (round(x+87.5-icon.width/2),round(y+20-icon.height/2)))
            canvas.alpha_composite(bar, (round(x+5),round(y+40)))
            # Host-title clipping is native behaviour for preexisting content;
            # the new GCC titles are independently required to fit the field.
            canvas.alpha_composite(native.label_image(node['title'], glyphs, kernings, atlas), (round(x+15),round(y+58)))
        draw.text((18,12), heading, font=font, fill='#e3cf90')
        draw.text((18,38), 'Installed code and native assets; simulated connectors, no engine test', font=font, fill='#c4cdcb')
        if thumbnail:
            canvas.thumbnail(thumbnail, Image.Resampling.LANCZOS)
        canvas.convert('RGB').save(HERE / filename)
        images.append(filename)

    gcc = nodes(shared, 'SAU')
    render(gcc, 'GCC_BRANCH_NATIVE.png', 'Cold War GCC -14shared focuses -native spacing')
    for tag, path in [('SAU','common/national_focus/mdcw_1970_generic_focus.txt'),
                      ('UAE','common/national_focus/COLDWAR_UAE_1970_focus.txt')]:
        tree = one(source(path), 'focus_tree')
        if 'COLDWAR_GCC_council' not in fields(tree, 'shared_focus'):
            errors.append('Host lacks shared GCC attachment: ' + tag)
        if not any(one(s, 'target') == 'COLDWAR_GCC_council' for s in fields(tree, 'shortcut')):
            errors.append('Host lacks GCC shortcut: ' + tag)
        ordinary = fields(tree, 'focus')
        all_nodes = nodes(ordinary + shared, tag)
        positions[tag] = {n['id']:n['xy'] for n in all_nodes}
        collisions = []
        rectangles = {}
        for node in all_nodes:
            x, y = node['xy'][0]*96, node['xy'][1]*130
            icon = icon_for(node)
            rectangles[node['id']] = (min(x+5,x+87.5-icon.width/2),min(y+40,y+20-icon.height/2),
                                     max(x+5+bar.width,x+87.5+icon.width/2),max(y+40+bar.height,y+20+icon.height/2))
        for new in shared_by:
            for other in rectangles:
                if new == other or other in shared_by and other < new:
                    continue
                if overlap(rectangles[new], rectangles[other]):
                    collisions.append([new,other])
        if collisions:
            errors.append('Visible GCC/host card overlap for ' + tag + ': ' + str(collisions))
        line_hits = []
        by = {n['id']:n for n in all_nodes}
        for node in all_nodes:
            x,y=node['xy'][0]*96,node['xy'][1]*130
            for clause in node['prerequisites']:
                for parent_id in clause:
                    parent=by[parent_id];px,py=parent['xy'][0]*96,parent['xy'][1]*130
                    mid=(py+90+y-26)//2
                    segments=[(px+80,py+90,px+80,mid),(px+80,mid,x+80,mid),(x+80,mid,x+80,y-26)]
                    for other,rect in rectangles.items():
                        if other in {node['id'],parent_id}:
                            continue
                        if not (node['id'] in shared_by or other in shared_by):
                            continue
                        if any(native.crosses(*segment,*rect) for segment in segments):
                            line_hits.append([node['id'],parent_id,other])
        if line_hits:
            errors.append('Unrelated GCC/host card crossed by simulated link for ' + tag + ': ' + str(line_hits))
        host_reports[tag] = dict(ordinary_focuses=len(ordinary), shared_gcc=len(shared), root=positions[tag]['COLDWAR_GCC_council'],
                                 visible_card_overlaps=collisions, unrelated_connector_intersections=line_hits,
                                 continuous_position=one(tree,'continuous_focus_position'),
                                 initial_position=one(tree,'initial_show_position'))
        render(all_nodes, tag+'_HOST_OVERVIEW.png', tag+' complete national host and additional GCC branch', (2300,1800))
        if tag == 'SAU':
            close = [n for n in all_nodes if 22 <= n['xy'][0] <= 43]
        else:
            close = [n for n in all_nodes if n['xy'][0] >= 22 and n['xy'][1] >= 16]
        render(close, tag+'_GCC_NEIGHBOURS_NATIVE.png', tag+' GCC branch with actual neighbouring focuses')
    report = dict(status='pass' if not errors else 'fail', errors=errors, native_spacing=[96,130],
                  native_title_field=147, shared_focus_count=len(shared), hosts=host_reports,
                  native_relative_positions_and_grouped_prerequisites_preserved=not errors,
                  title_widths={ident:native.width(loc[ident],glyphs,kernings) for ident in shared_by},
                  generic_host_coverage=['SAU','KUW','QAT','BHR','OMA'],
                  excluded_shared_content={'COLDWAR_UNI_the_union_plan':'Its actual allow_branch country trigger excludes every Gulf tag'},
                  source_hashes={p:digest(ROOT/p) for p in [shared_path,'interface/COLDWAR_GCC_1970.gfx',
                  'common/national_focus/mdcw_1970_generic_focus.txt','common/national_focus/COLDWAR_UAE_1970_focus.txt',
                  'localisation/english/COLDWAR_GCC_1970_l_english.yml']},
                  native_font='hoi_16mbs', native_assets=True, engine_tested=False,
                  approximate='Orthogonal connectors and unavailable cards; no in-game routing, clipping or hover claim.',
                  images=images, resolved_positions=positions)
    (HERE/'LAYOUT_REVIEW.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='resolved_positions'},indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
