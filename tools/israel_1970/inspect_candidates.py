from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
names=['FocusElectHerut.dds','FocusElectMapai.dds','FocusElectMapam.dds','FocusElectHapoelHaMizrachi.dds',
       'ISR_Focus_Israeli_Army.dds','ISR_israel_defense_forces.dds','ISR_Israel.dds','ben_gurion.dds',
       'ISR_Focus_Egypt-Israeli_Tension.dds','suez_crisis.dds','Suez_Debate.dds','israeli_cooperation.dds',
       'Irrigation_Pipes.dds','Irrigation_Canals.tga','Import_water.tga','PAL_Irrigation_Program.png',
       'DiamondsAre4ever.dds','Expand_the_Flemish_Diamond.dds','Improve_supply_distribution_methods.tga',
       'military_research.png','double_research.png','Nuclear_Energy.dds','Nuclear_Research_Lab.png',
       'generic_secret_documents.png','generic_army_cooperation.png','generic_air_command.png',
       'generic_support_equipment.png','generic_mobile_artillery_light.png','generic_railway_construction.png','focus_world_peace.dds']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
sheet=Image.new('RGB',(1200,1000),'#202b30');d=ImageDraw.Draw(sheet)
for i,name in enumerate(names):
    im=Image.open(ROOT/'gfx/interface/goals/coldwar'/name).convert('RGBA');im.thumbnail((110,100))
    x=i%6*200;y=i//6*200;sheet.paste(im,(x+(200-im.width)//2,y+6),im)
    for j in range((len(name)+22)//23):d.text((x+5,y+115+j*18),name[j*23:(j+1)*23],font=font,fill='#e4e4d7')
sheet.save(ROOT/'docs/israel_1970_design/period_art_candidates.png')
