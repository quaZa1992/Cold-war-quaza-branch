# IMPERIA CW — Cold War: Strategic Command instrument-panel presentation.
"""Native, localised widgets over deterministic machined-metal instrument artwork."""
from pathlib import Path
import random
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 780, 700
COLOURS = {5: '#94b6a0', 4: '#b2c395', 3: '#d1bc7c', 2: '#d6a06b', 1: '#d58273'}
FONTS = {
    'micro': (11, '#889b94'), 'label': (12, '#a3b2a5'),
    'section': (13, '#c8b47e'), 'body': (14, '#d4dcd0'),
    'status': (17, '#d4dcd0'), 'value': (24, '#bed7b7'),
    'title': (29, '#e2dfcf'), 'launcher': (19, '#d5d6bc'),
}
FONTS.update({f'level_{n}': (29, colour) for n, colour in COLOURS.items()})
WIDGETS = []


def gui_source(loc, levels):
    WIDGETS.clear()
    chunks = ['''guiTypes = {
containerWindowType = { name = "nr_launcher" position = { x = -272 y = 88 } orientation = upper_right size = { width = 56 height = 26 }
    buttonType = { name = "nr_launch" position = { x = 0 y = 0 } spriteType = "GFX_nr_launcher" pdx_tooltip = "nr_launcher_tt" clicksound = click_default }
    iconType = { name = "nr_launcher_icon" spriteType = "GFX_nr_logo_small" position = { x = 3 y = 1 } alwaysTransparent = yes }
    instantTextBoxType = { name = "nr_launcher_text" position = { x = 30 y = 2 } font = "nr_font_launcher" text = "nr_launcher_value" maxWidth = 20 maxHeight = 23 format = center alwaysTransparent = yes }
}
containerWindowType = { name = "nr_window" position = { x = 0 y = 0 } orientation = center origo = center moveable = yes size = { width = 780 height = 700 }
    background = { name = "nr_background" quadTextureSprite = "GFX_nr_frame" }
    iconType = { name = "nr_input_surface" position = { x = 0 y = 0 } spriteType = "GFX_nr_frame" alwaysTransparent = no }
''']

    def icon(name, x, y, sprite, condition=None):
        chunks.append(f'iconType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "GFX_nr_{sprite}" alwaysTransparent = yes }}\n')
        WIDGETS.append(dict(kind='icon', name=name, x=x, y=y, sprite=sprite, condition=condition))

    def text(name, x, y, w, h, font='body', key=None, tip=None, align='left', condition=None):
        key = key or name
        chunks.append(f'instantTextBoxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "nr_font_{font}" text = "{key}" maxWidth = {w} maxHeight = {h} format = {align} fixedsize = yes alwaysTransparent = {"no" if tip else "yes"} '+(f'pdx_tooltip = "{tip}" ' if tip else '')+'}\n')
        WIDGETS.append(dict(kind='text', name=name, x=x, y=y, w=w, h=h, font=font, key=key, align=align, condition=condition))

    def button(name, x, y, sprite, key=None, tip=None, close=False, condition=None):
        chunks.append(f'buttonType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "GFX_nr_{sprite}" '+(f'buttonText = "{key}" buttonFont = "nr_font_body" ' if key else '')+(f'pdx_tooltip = "{tip}" ' if tip else '')+('shortcut = "ESCAPE" ' if close else '')+f'clicksound = {"click_close" if close else "click_default"} }}\n')
        WIDGETS.append(dict(kind='button', name=name, x=x, y=y, sprite=sprite, key=key, font='body', condition=condition))

    icon('nr_insignia', 27, 14, 'logo')
    button('nr_close', 738, 16, 'close', close=True)
    text('nr_title', 105, 20, 510, 35, 'title')
    text('nr_subtitle', 107, 58, 548, 19, 'label')
    text('nr_posture_label', 30, 96, 420, 17, 'section')
    text('nr_current', 30, 116, 520, 30, 'value')
    text('nr_posture_notice', 536, 112, 212, 21, 'label', key='[nr_posture_notice_L]', align='right')
    for i, level in enumerate(levels):
        x = 24 + i * 148
        button(f'nr_level_{level}', x, 151, f'card_{level}', tip=f'nr_level_{level}_tt')
        icon(f'nr_active_{level}', x, 151, f'active_{level}', condition=f'active_{level}')
        icon(f'nr_pending_{level}', x, 151, 'pending', condition=f'pending_{level}')
        loc(f'nr_digit_{level}', str(level))
        first_line, second_line = levels[level][0].split(' ', 1)
        loc(f'nr_card_first_{level}', first_line)
        loc(f'nr_card_second_{level}', second_line)
        text(f'nr_digit_{level}', x+8, 160, 124, 32, f'level_{level}', align='center')
        text(f'nr_card_name_{level}', x+6, 193, 128, 17, key=f'nr_card_first_{level}', align='center')
        text(f'nr_card_suffix_{level}', x+6, 210, 128, 17, key=f'nr_card_second_{level}', align='center')
        text(f'nr_in_force_{level}', x+6, 228, 128, 14, 'micro', key='nr_in_force', align='center', condition=f'active_{level}')
        text(f'nr_preparing_{level}', x+6, 228, 128, 14, 'micro', key='nr_preparing', align='center', condition=f'pending_{level}')
    text('nr_order_status', 30, 258, 526, 21, key='[nr_order_status_L]')
    button('nr_cancel', 574, 252, 'button', 'nr_cancel_order', 'nr_cancel_tt', condition='order')
    text('nr_arsenal_title', 30, 290, 720, 18, 'section')
    for i, (name, tip) in enumerate([('stock', 'stock'), ('ready', 'ready'), ('reserve', 'reserve')]):
        x = 38 + i*248
        text(f'nr_{name}_label', x, 323, 208, 17, 'label', tip=f'nr_{tip}_tt')
        text(f'nr_{name}_value', x, 343, 208, 30, 'value', tip=f'nr_{tip}_tt')
    for i, (name, tip) in enumerate([('forces', 'budget'), ('civil', 'budget'), ('fatigue', 'fatigue')]):
        x = 38 + i*248
        text(f'nr_{name}_label', x, 397, 208, 17, 'label', tip=f'nr_{tip}_tt')
        text(f'nr_{name}_value', x, 417, 208, 23, 'status', key='[nr_fatigue_value_L]' if name == 'fatigue' else None, tip=f'nr_{tip}_tt')
    text('nr_civil_title', 40, 466, 500, 18, 'section', tip='nr_civil_tt')
    text('nr_civil_status', 40, 493, 506, 31, key='[nr_civil_status_L]', tip='nr_civil_tt')
    button('nr_civil_start', 574, 463, 'button', 'nr_civil_start', 'nr_civil_tt')
    button('nr_civil_stop', 574, 495, 'button', 'nr_civil_stop', 'nr_civil_tt')
    text('nr_crisis_title', 40, 552, 500, 18, 'section')
    text('nr_crisis_status', 40, 577, 514, 24, 'status', key='[nr_crisis_status_L]')
    button('nr_consult', 574, 574, 'button', 'nr_consult', 'nr_consult_tt', condition='crisis')
    text('nr_hotline_status', 40, 607, 692, 19, key='[nr_hotline_status_L]', condition='crisis')
    icon('nr_escalation_alert', 34, 634, 'escalation_alert', condition='escalation')
    text('nr_crisis_hint', 46, 640, 688, 20, key='[nr_escalation_status_L]', tip='nr_escalation_tt')
    text('nr_footer', 30, 679, 720, 15, 'micro', align='center')
    chunks.append('} }')
    return ''.join(chunks)


def visibility_triggers():
    out = []
    for n in COLOURS:
        pending = f'check_variable = {{ nr_build_days > 0 }} check_variable = {{ nr_order = {n} }}'
        out.extend([
            f'nr_pending_{n}_visible = {{ {pending} }}',
            f'nr_preparing_{n}_visible = {{ {pending} }}',
            f'nr_in_force_{n}_visible = {{ check_variable = {{ nr_level = {n} }} }}',
        ])
    out.append('nr_escalation_alert_visible = { OR = { has_country_flag = nr_fu_waiting has_country_flag = nr_fu_authorised nr_foreign_ultimatum = yes nr_foreign_release = yes } }')
    return '\n'.join(out)


SCRIPTED_TEXT = '''
defined_text = { name = nr_fatigue_value_L
    text = { trigger = { check_variable = { nr_fatigue > 74.99999 } } localization_key = nr_fatigue_high }
    text = { trigger = { check_variable = { nr_fatigue > 49.99999 } } localization_key = nr_fatigue_elevated }
    text = { localization_key = nr_fatigue_value }
}
defined_text = { name = nr_posture_notice_L
    text = { trigger = { has_country_flag = nr_standdown } localization_key = nr_notice_standdown }
    text = { trigger = { check_variable = { nr_build_days > 0 } } localization_key = nr_notice_orders }
    text = { localization_key = nr_notice_ready }
}
'''


def _rgb(colour):
    return tuple(bytes.fromhex(colour.lstrip('#')))


def _metal(size, top, bottom, seed=17):
    """One-pixel brushed finish; no bitmap text is embedded into runtime assets."""
    w, h = size
    a, b = _rgb(top), _rgb(bottom)
    rng = random.Random(seed)
    pixels = []
    for y in range(h):
        t = y/max(1, h-1)
        brush = rng.choice([-1, 0, 0, 0, 1])
        for x in range(w):
            noise = rng.choice([-1, 0, 0, 0, 1]) + brush
            pixels.append(tuple(max(0, min(255, round(c*(1-t)+d*t)+noise)) for c, d in zip(a, b))+(255,))
    im = Image.new('RGBA', size)
    im.putdata(pixels)
    return im


def _bevel(d, box, rim='#53625b', light='#283730'):
    x, y, r, b = box
    d.rectangle(box, fill='#0e1917', outline=rim)
    d.line((x+1, b-1, x+1, y+1, r-1, y+1), fill=light)


def artwork(root):
    folder = root/'gfx/interface/COLDWAR_nuclear_readiness'
    folder.mkdir(parents=True, exist_ok=True)
    sprites = []

    def save(name, im, frames=1, shader=False):
        im.save(folder/(name+'.dds'))
        sprites.append(f'spriteType = {{ name = "GFX_nr_{name}" texturefile = "gfx/interface/COLDWAR_nuclear_readiness/{name}.dds" noOfFrames = {frames} legacy_lazy_load = no '+('effectFile = "gfx/FX/buttonstate.lua" ' if shader else '')+'}')

    frame = _metal((WIDTH, HEIGHT), '#25332e', '#15231f')
    d = ImageDraw.Draw(frame)
    d.rectangle((0, 0, 779, 699), outline='#070e0c', width=2)
    d.rectangle((2, 2, 777, 697), outline='#809080')
    d.rectangle((5, 5, 774, 694), outline='#0a1511', width=2)
    d.rectangle((9, 9, 770, 86), fill='#172621', outline='#45584a')
    d.line((17, 87, 762, 87), fill='#ad9866')
    d.line((17, 89, 762, 89), fill='#080f0d')
    # Radar engraving is deliberately confined to the empty header margin.
    for radius in [14, 27, 39]:
        d.ellipse((689-radius, 47-radius, 689+radius, 47+radius), outline='#2a3f33')
    d.line((650, 47, 728, 47), fill='#2a3f33')
    d.line((689, 10, 689, 84), fill='#2a3f33')
    d.line((689, 47, 716, 23), fill='#4c614a')
    d.ellipse((703, 31, 706, 34), fill='#b7b178')
    d.rectangle((24, 94, 756, 146), fill='#192a23')
    d.line((25, 146, 755, 146), fill='#33463a')
    for x in [24, 272, 520]:
        _bevel(d, (x, 313, x+235, 378), '#475a4e')
        d.line((x+12, 315, x+222, 315), fill='#22382c')
        _bevel(d, (x, 388, x+235, 443), '#394d42')
        d.line((x+12, 441, x+222, 441), fill='#20372a')
    for y, bottom in [(455, 529), (541, 669)]:
        _bevel(d, (24, y, 756, bottom), '#4b5b4d')
        d.rectangle((25, y+1, 27, bottom-1), fill='#a18e62')
        d.line((40, y+29, 739, y+29), fill='#344538')
    _bevel(d, (34, 634, 746, 662), '#304a3b', '#142a20')
    d.line((30, 675, 750, 675), fill='#52604d')
    for x, y in [(13, 14), (767, 14), (13, 686), (767, 686)]:
        d.ellipse((x-3, y-3, x+3, y+3), fill='#111b17', outline='#63705f')
        d.line((x-1, y+1, x+1, y-1), fill='#84917a')
    save('frame', frame)
    for n, colour in COLOURS.items():
        im = _metal((140, 94), '#304034', '#1e2c25', n)
        cd = ImageDraw.Draw(im)
        cd.rectangle((0, 0, 139, 93), outline='#576553')
        cd.rectangle((2, 2, 137, 91), outline='#101d16')
        cd.rectangle((4, 4, 135, 6), fill=colour)
        cd.line((12, 40, 127, 40), fill='#495642')
        cd.rectangle((3, 74, 136, 90), fill='#14231a')
        # Each instrument carries a distinct number of lit segments as well as colour.
        for segment in range(5):
            left = 13+segment*24
            cd.rectangle((left, 8, left+16, 9), fill=colour if segment < 6-n else '#17251e')
        save(f'card_{n}', im, shader=True)
        active = Image.new('RGBA', (140, 94))
        ad = ImageDraw.Draw(active)
        ad.rectangle((0, 0, 139, 93), outline=colour, width=2)
        ad.line((3, 92, 136, 92), fill='#e0d3a1')
        ad.ellipse((9, 81, 13, 85), fill=colour)
        save(f'active_{n}', active)
    pending = Image.new('RGBA', (140, 94))
    pd = ImageDraw.Draw(pending)
    for x in range(2, 138, 10):
        pd.line((x, 1, min(x+5, 137), 1), fill='#cfb87c', width=2)
        pd.line((x, 92, min(x+5, 137), 92), fill='#cfb87c', width=2)
    for y in range(3, 91, 10):
        pd.line((1, y, 1, min(y+5, 91)), fill='#cfb87c', width=2)
        pd.line((138, y, 138, min(y+5, 91)), fill='#cfb87c', width=2)
    save('pending', pending)
    alert = Image.new('RGBA', (712, 28), '#311e19')
    ad = ImageDraw.Draw(alert)
    ad.rectangle((0, 0, 711, 27), outline='#a56c51')
    ad.rectangle((1, 1, 3, 26), fill='#d39170')
    save('escalation_alert', alert)
    for name, size in [('button', (180, 28)), ('launcher', (56, 26)), ('close', (24, 24))]:
        strip = Image.new('RGBA', (size[0]*3, size[1]))
        for index, (top, bottom, edge) in enumerate([
            ('#354438', '#223026', '#7e825e'),
            ('#4a5c45', '#2e4130', '#c0b07b'),
            ('#1d2d22', '#344332', '#aa9a66'),
        ]):
            im = _metal(size, top, bottom)
            bd = ImageDraw.Draw(im)
            bd.rectangle((0, 0, size[0]-1, size[1]-1), outline='#08120c')
            bd.rectangle((1, 1, size[0]-2, size[1]-2), outline=edge)
            bd.line((3, size[1]-3, size[0]-4, size[1]-3), fill='#142117')
            if name == 'close':
                bd.line((8, 8, 15, 15), fill='#e0d8bd', width=2)
                bd.line((15, 8, 8, 15), fill='#e0d8bd', width=2)
            elif name == 'launcher':
                bd.line((28, 4, 28, 21), fill='#788064')
            strip.alpha_composite(im, (size[0]*index, 0))
        save(name, strip, frames=3)
    master = Image.open(Path(__file__).parent/'art/command_emblem_master.png').convert('RGBA')
    bounds = master.getchannel('A').getbbox()
    # Size/export only: generated design and alpha remain intact.
    master = master.crop(bounds)
    for name, side in [('logo', 64), ('logo_small', 24)]:
        im = master.copy()
        im.thumbnail((side, side), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (side, side))
        canvas.alpha_composite(im, ((side-im.width)//2, (side-im.height)//2))
        save(name, canvas)
    fonts = ['bitmapfonts = {']
    for name, (size, colour) in FONTS.items():
        r, g, b = _rgb(colour)
        fonts.append(f'bitmapfont = {{ name = "nr_font_{name}" path = "gfx/fonts/COLDWAR_space_race/cw_sr_ui_{size}" color = 0xff{r:02x}{g:02x}{b:02x} textcolors = {{ Y = {{ 212 190 127 }} H = {{ 212 190 127 }} G = {{ 156 199 158 }} R = {{ 226 143 124 }} g = {{ 141 163 148 }} T = {{ 212 220 208 }} }} }}')
    fonts.append('}')
    return 'spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n'+'\n'.join(fonts)
