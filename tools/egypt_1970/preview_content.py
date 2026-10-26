# IMPERIA CW — Cold War: egypt 1970 — preview content.
"""Render the actual DDS assets for visual QA and a compact roster overview."""
from pathlib import Path
import json
import math
import re
import textwrap
from PIL import Image, ImageDraw, ImageFont
from roster import PARTIES, NAMES, MILITARY

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
FONT=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
SMALL=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',11)
sprites=(ROOT/'interface/COLDWAR_EGY_1970_parties.gfx').read_text()
icons={name:path for name,path in re.findall(r'name = "([^"]+)"\s+texturefile = "([^"]+)"',sprites)}

def gallery(rows,columns,path):
    card_w,card_h=210,320
    canvas=Image.new('RGB',(columns*card_w,math.ceil(len(rows)/columns)*card_h),(25,29,36))
    draw=ImageDraw.Draw(canvas)
    for i,(title,key,status,icon) in enumerate(rows):
        x,y=(i%columns)*card_w,(i//columns)*card_h
        draw.rounded_rectangle((x+3,y+3,x+card_w-4,y+card_h-4),6,fill=(38,44,54))
        draw.multiline_text((x+9,y+7),'\n'.join(textwrap.wrap(title,29)[:3]),font=FONT,fill=(240,241,245),spacing=1)
        portrait=Image.open(ROOT/f'gfx/leaders/EGY/1970/{key}.dds').convert('RGB')
        canvas.paste(portrait,(x+27,y+60))
        if icon:
            emblem=Image.open(ROOT/icon).convert('RGBA')
            canvas.paste(emblem,(x+6,y+246),emblem)
        draw.multiline_text((x+9,y+274),'\n'.join(textwrap.wrap(NAMES[key],29)),font=FONT,fill=(225,232,241),spacing=0)
        if status: draw.text((x+9,y+307),status,font=SMALL,fill=(168,190,208))
    canvas.save(HERE/path)

gallery([(f'{i:02d}  {party[1]}',party[2],'',icons[f'GFX_COLDWAR_EGY_1970_party_{i}']) for i,party in enumerate(PARTIES)],6,'party_portraits.png')
roles={'field_marshal':'Strategische Heeresführung','corps_commander':'General','navy_leader':'Admiral'}
gallery([(roles.get(role,'Luftwaffe / Luftverteidigung'),key,
          'Reserve ab '+date if date else 'Zu Spielbeginn verfügbar','') for key,role,skills,slot,trait,date in MILITARY],5,'military_portraits.png')

# An inventory makes it clear which later focus-story leaders are outside this
# January 1970 roster; this does not rewrite unrelated later succession content.
t=(ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt').read_text()
inventory=[]
for block in re.split(r'(?m)^\tfocus = \{',t)[1:]:
    match=re.search(r'id = (\w+)',block)
    if not match: continue
    for line in re.findall(r'create_country_leader = \{[^\n]+',block):
        name=re.search(r'name = "([^"]+)"',line)
        if name: inventory.append({'focus':match[1],'leader':name[1],'explicit_portrait':'picture =' in line})
(HERE/'focus_leader_inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
print('Rendered party_portraits.png and military_portraits.png from actual DDS assets.')
