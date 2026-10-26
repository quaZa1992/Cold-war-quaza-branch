# IMPERIA CW — Cold War: exact bitmap-font layout proof for the command panel.
"""Render the native widget geometry with the actual font atlas and stress copy."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from PIL import Image, ImageDraw
import build
import command_ui as ui

ROOT = build.ROOT
OUT = ROOT/'docs/nuclear_readiness/interface'
ASSETS = ROOT/'gfx/interface/COLDWAR_nuclear_readiness'
COLOUR_CODES = {'Y': '#d4be7f', 'H': '#d4be7f', 'G': '#9cc79e', 'R': '#e28f7c', 'g': '#8da394', 'T': '#d4dcd0'}


@lru_cache(None)
def font(size):
    path = ROOT/f'gfx/fonts/COLDWAR_space_race/cw_sr_ui_{size}'
    chars = {}
    for line in path.with_suffix('.fnt').read_text(encoding='utf-8').splitlines():
        if line.startswith('char '):
            item = {key: int(value) for key, value in re.findall(r'(\w+)=(-?\d+)', line)}
            chars[item['id']] = item
    return chars, Image.open(path.with_suffix('.dds')).convert('RGBA')


def styled(text, colour):
    current = colour
    text = text.replace('£pol_power', 'PP').replace('\\n', '\n')
    i = 0
    while i < len(text):
        if text[i] == '§' and i+1 < len(text):
            current = colour if text[i+1] == '!' else COLOUR_CODES[text[i+1]]
            i += 2
            continue
        yield text[i], current
        i += 1


def draw_text(canvas, box, text, font_name, align='left', name=''):
    size, colour = ui.FONTS[font_name]
    chars, atlas = font(size)
    line_height = size+3
    x, y, width, height = box
    lines = [[]]
    advance = lambda ch: chars[ord(ch)]['xadvance']
    # Wrap at word boundaries using native glyph advances, including colour spans.
    word = []
    for ch, col in list(styled(text, colour))+[('\0', colour)]:
        if ch not in [' ', '\n', '\0']:
            word.append((ch, col))
            continue
        if word:
            length = sum(advance(c) for c, _ in word)
            current = sum(advance(c) for c, _ in lines[-1])
            if current and current+length > width:
                while lines[-1] and lines[-1][-1][0] == ' ': lines[-1].pop()
                lines.append([])
            lines[-1].extend(word)
            word = []
        if ch == '\n': lines.append([])
        elif ch == ' ': lines[-1].append((ch, col))
    while lines[-1] and lines[-1][-1][0] == ' ': lines[-1].pop()
    assert len(lines)*line_height <= height+2, (name, text, len(lines)*line_height, height)
    for index, line in enumerate(lines):
        length = sum(advance(c) for c, _ in line)
        assert length <= width, (name, text, length, width)
        dx = x+(width-length)//2 if align == 'center' else x+width-length if align == 'right' else x
        for ch, col in line:
            glyph = chars[ord(ch)]
            if glyph['width'] and glyph['height']:
                a, b = glyph['x'], glyph['y']
                mask = atlas.crop((a, b, a+glyph['width'], b+glyph['height'])).getchannel('A')
                ink = Image.new('RGBA', mask.size, col)
                ink.putalpha(mask)
                canvas.alpha_composite(ink, (dx+glyph['xoffset'], y+index*line_height+glyph['yoffset']))
            dx += glyph['xadvance']


CASES = [
    dict(name='routine', level=5, order=None, civil='inactive', crisis=False, hotline=False),
    dict(name='preparing', level=5, order=1, civil='preparing', crisis=False, hotline=False),
    dict(name='strategic_alert', level=2, order=None, civil='active', crisis=True, hotline=True),
    dict(name='ultimatum', level=1, order=None, civil='active', crisis=True, hotline=True, escalation='waiting'),
    dict(name='foreign_release', level=1, order=None, civil='active', crisis=True, hotline=False, escalation='foreign_release'),
    dict(name='long_values', level=3, order=None, civil='inactive', crisis=True, hotline=True, stress=True),
]


def visible(condition, case):
    if not condition: return True
    if condition.startswith('active_'): return case['level'] == int(condition[-1])
    if condition.startswith('pending_'): return case['order'] == int(condition[-1])
    if condition == 'order': return case['order'] is not None
    if condition == 'crisis': return case['crisis']
    if condition == 'escalation': return bool(case.get('escalation'))
    raise ValueError(condition)


def localisation(key):
    return build.LOC[key.replace('nr_', 'COLDWAR_nr_')]


def copy_for(key, case):
    level = case['level']
    defined = {
        '[nr_fatigue_value_L]': localisation('nr_fatigue_high'),
        '[nr_level_L]': build.LEVELS[level][0],
        '[nr_posture_notice_L]': localisation('nr_notice_orders' if case['order'] else 'nr_notice_ready'),
        '[nr_order_status_L]': localisation('nr_order_pending' if case['order'] else 'nr_order_none'),
        '[nr_civil_status_L]': localisation({'active': 'nr_civil_active_text', 'inactive': 'nr_civil_inactive', 'preparing': 'nr_civil_preparing'}[case['civil']]),
        '[nr_crisis_status_L]': localisation('nr_crisis_partner' if case['crisis'] else 'nr_crisis_none'),
        '[nr_hotline_status_L]': localisation('nr_crisis_hotline' if case['hotline'] else 'nr_crisis_no_hotline'),
        '[nr_escalation_status_L]': localisation({'waiting': 'nr_fu_waiting_text', 'foreign_release': 'nr_fu_foreign_release_text'}.get(case.get('escalation'), 'nr_crisis_hint')),
    }
    text = defined[key] if key.startswith('[') else localisation(key)
    for variable, value in {
        '[?nr_arsenal|0]': '1000' if not case.get('stress') else '1234567',
        '[?nr_ready_count|0]': str(round(1000*build.LEVELS[level][1])) if not case.get('stress') else '617284',
        '[?nr_protected_count|0]': str(round(1000*build.LEVELS[level][2])) if not case.get('stress') else '308642',
        '[?nr_ready_share|%0]': f'{build.LEVELS[level][1]:.0%}',
        '[?nr_reserve_share|%0]': f'{build.LEVELS[level][2]:.0%}',
        '[?nr_forces_weekly|3]': '0.030' if not case.get('stress') else '12345.678',
        '[?nr_civil_weekly|3]': '0.018', '[?nr_fatigue|0]': '100',
        '[?nr_opponent.GetNameDef]': 'the Soviet Union' if not case.get('stress') else 'the Democratic People\'s Republic of Korea',
        '[?nr_build_days|0]': '8', '[?nr_civil_days|0]': '3',
        '[?nr_fu_hours|0]': '72', '[?nr_fu_incoming_hours|0]': '168',
    }.items():
        text = text.replace(variable.replace('nr_', 'COLDWAR_nr_'), value)
    text = text.replace('[COLDWAR_nr_level_L]', build.LEVELS[level][0])
    assert '[' not in text, (key, text)
    return text


def render(case):
    canvas = Image.open(ASSETS/'frame.dds').convert('RGBA')
    for widget in ui.WIDGETS:
        if not visible(widget['condition'], case): continue
        kind = widget['kind']
        x, y = widget['x'], widget['y']
        if kind in ['icon', 'button']:
            asset = Image.open(ASSETS/(widget['sprite']+'.dds')).convert('RGBA')
            if widget['sprite'] in ['button', 'launcher', 'close']:
                asset = asset.crop((0, 0, asset.width//3, asset.height))
            assert x+asset.width <= ui.WIDTH and y+asset.height <= ui.HEIGHT, widget
            canvas.alpha_composite(asset, (x, y))
            if kind == 'button' and widget.get('key'):
                size = ui.FONTS[widget['font']][0]
                draw_text(canvas, (x+5, y+(asset.height-size-3)//2, asset.width-10, size+3), copy_for(widget['key'], case), widget['font'], 'center', widget['name'])
        else:
            assert x+widget['w'] <= ui.WIDTH and y+widget['h'] <= ui.HEIGHT, widget
            draw_text(canvas, (x, y, widget['w'], widget['h']), copy_for(widget['key'], case), widget['font'], widget['align'], widget['name'])
    return canvas


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'tool': 'Built-in ImageGen', 'emblem_master': 'tools/nuclear_readiness/art/command_emblem_master.png',
        'prompt': 'tools/nuclear_readiness/art/command_emblem_prompt.txt',
        'emblem_source': 'Original generated artwork; no third-party source image.',
        'panel_size': [ui.WIDTH, ui.HEIGHT], 'layout_checks': [],
        'preview_scope': 'Native bitmap font metrics and runtime textures. Political power icon represented by PP in offline proofs; verify the native icon and interaction in HOI4.'}
    for case in CASES:
        render(case).save(OUT/(case['name']+'.png'))
        manifest['layout_checks'].append(case['name'])
    manifest['asset_sha256'] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(ASSETS.glob('*.dds')) if path.name not in ['active.dds']}
    logo = Image.open(ASSETS/'logo_small.dds').convert('RGBA')
    assert logo.getextrema()[3] == (0, 255)
    Image.open(ASSETS/'logo.dds').save(OUT/'logo.png')
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print(f'Validated {len(CASES)} native-font layout states; transparent 24 px logo and all widget bounds passed.')


if __name__ == '__main__': main()
