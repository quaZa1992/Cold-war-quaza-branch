# IMPERIA CW — Cold War: Guest Worker Administration
"""Native RGBA DDS stationery and controls for the Ministry dossier."""
from PIL import Image, ImageDraw
import random


def build(assets):
    assets.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1970)
    panel = Image.new('RGBA', (510, 740))
    pixels = panel.load()
    for y in range(740):
        for x in range(510):
            grain = rng.choice((-2, -1, 0, 0, 0, 1, 2))
            edge = min(x, 509-x, y, 739-y)
            shade = max(0, 7-edge) * 2
            pixels[x, y] = (229+grain-shade, 220+grain-shade, 193+grain-shade, 255)
    d = ImageDraw.Draw(panel)
    d.rounded_rectangle((2, 2, 507, 737), 5, outline='#26352a', width=4)
    d.rectangle((8, 8, 501, 731), outline='#a39879')
    d.rectangle((10, 10, 499, 91), fill='#263d30')
    d.line((10, 92, 499, 92), fill='#9f8351', width=2)
    d.line((10, 96, 499, 96), fill='#a39571')
    for x in (180, 328):
        d.line((x, 132, x, 175), fill='#b6ab8d')
    d.line((22, 184, 487, 184), fill='#a39879')
    d.line((22, 231, 487, 231), fill='#a39879')
    d.line((22, 686, 487, 686), fill='#a39879')
    panel.save(assets/'dashboard.png')
    panel.save(assets/'dashboard.dds')
    specs = {'wide':(228,30),'medium':(148,30),'small':(110,30),'page':(35,26),
             'tab':(148,32),'country':(460,36),'danger':(228,30),'muted':(148,30),'wide_muted':(228,30),'nav':(110,32)}
    for name,(width,height) in specs.items():
        image = Image.new('RGBA',(width*3,height))
        draw = ImageDraw.Draw(image)
        for frame,fill in enumerate(('#304d3b','#46654b','#243b2d')):
            if name == 'country': fill = ('#eee7d1','#d7dfc2','#d1d7bd')[frame]
            if name in ('tab','nav'): fill = ('#3c5140','#506b4c','#2c4432')[frame]
            if name == 'danger': fill = ('#734638','#8b5944','#59382e')[frame]
            # IMPERIA CW — Cold War: Explicit inactive recruitment artwork,
            # independent of the engine's optional disabled-button shader.
            if name in ('muted','wide_muted'): fill = ('#686860','#686860','#686860')[frame]
            left=frame*width
            draw.rounded_rectangle((left,0,left+width-1,height-1),2,fill=fill,outline='#99988f' if name=='muted' else '#9b9d80')
            draw.line((left+3,2,left+width-4,2),fill='#929189' if name=='muted' else '#89967b')
        image.save(assets/(name+'.dds'))
    # Native frames: empty, 10%, ... 100%. No shaders, animation or per-frame script.
    for name,width,height,frames in [('coverage',284,5,11),('progress',460,5,5)]:
        image=Image.new('RGBA',(width*frames,height))
        draw=ImageDraw.Draw(image)
        for frame in range(frames):
            left=width*frame
            draw.rectangle((left,0,left+width-1,height-1),fill='#c6c5aa')
            amount=round(width*frame/(frames-1))
            if amount:draw.rectangle((left,0,left+amount-1,height-1),fill='#446648')
        image.save(assets/(name+'.dds'))
    # Highlight is separate from the native button hover/pressed frames.
    image=Image.new('RGBA',(4,36),'#547143');image.save(assets/'selection.dds')
    image=Image.new('RGBA',(148,3),'#cdbb80');image.save(assets/'tab_selection.dds')
    # IMPERIA CW — Cold War: Four compact policy/navigation tabs.
    image=Image.new('RGBA',(110,3),'#cdbb80');image.save(assets/'nav_selection.dds')
