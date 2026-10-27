# IMPERIA CW — Cold War: review existing MD focus artwork.
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont
root = Path(__file__).resolve().parent
game = root.parents[1]
source = (game / 'interface/goals.gfx').read_text(encoding='utf-8-sig')
sprites = dict(re.findall(r'spriteType\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s*texture[fF]ile\s*=\s*"([^"]+)"', source))
names = ['goal_JAP_budget_check', 'goal_JAP_okinawa_militarism', 'major_alliance3', 'peace', 'focus_drinks_peace', 'focus_JAP_further_urban_investments', 'construction_buldozer', 'crane_and_tower', 'focus_generic_improve_the_administration', 'goverment_building_sheep', 'trade', 'diplomacy']
canvas = Image.new('RGB', (800, 420), '#212528')
d = ImageDraw.Draw(canvas)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)
for i, name in enumerate(names):
    x, y = (i % 5) * 160, (i // 5) * 140
    path = game / sprites.get(name, '')
    if path.is_file():
        icon = Image.open(path).convert('RGBA'); icon.thumbnail((100, 88))
        canvas.paste(icon, (x + 30, y), icon)
    d.text((x + 4, y + 94), name, fill='white', font=font)
canvas.save(root / 'staging/graph/icon_contact_sheet.png')
