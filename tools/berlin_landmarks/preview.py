# IMPERIA CW — Cold War: berlin landmarks — preview.
"""Assemble native Blender renders and update the small landmark UI icon."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CFG=json.loads((HERE/'config.json').read_text())
PREVIEW=HERE/'previews'


def main():
    canvas=Image.new('RGB',(1700,1100),(236,237,235))
    draw=ImageDraw.Draw(canvas)
    try:font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',26)
    except OSError:font=ImageFont.load_default()
    panels=[('blender_tower.png',(0,70,460,1100),'Fernsehturm · neues Blender-Modell'),
            ('blender_tower_detail.png',(465,70,1000,650),'Kugel und Antenne'),
            ('blender_wall.png',(1000,70,1700,650),'Mauer · vier lange Abschnitte'),
            ('blender_export_verification.png' if (PREVIEW/'blender_export_verification.png').exists() else 'blender_map_scale.png',(465,660,1700,1100),'')]
    for name,box,label in panels:
        im=Image.open(PREVIEW/name).convert('RGB')
        im.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
        canvas.paste(im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]+(box[3]-box[1]-im.height)//2))
        if label:draw.text((box[0]+15,25),label,font=font,fill=(42,46,48))
    canvas.save(PREVIEW/'berlin_landmarks.png')

    a=np.asarray(Image.open(ROOT/'map/provinces.bmp'));crop=a[471:486,3003:3021].copy()
    e=np.all(crop==[86,99,46],2);w=np.all(crop==[167,217,90],2)
    crop[:]=[215,216,207];crop[e]=[213,142,139];crop[w]=[131,162,197]
    fig,ax=plt.subplots(figsize=(8,8));ax.imshow(crop,extent=[3003,3021,1562,1577],origin='upper')
    p=np.asarray(CFG['wall_world']);ax.plot(*p.T,color='#343b3d',linewidth=3,label='Geglätteter Mauerverlauf')
    ax.scatter(*CFG['tower_anchor'],marker='^',s=130,c='#f0e9d3',edgecolors='#353b3d',label='Fernsehturm')
    ax.scatter([3015.5],[1569],s=65,c='#778792',label='Radar-Anlage')
    ax.text(3007,1572,'West',ha='center');ax.text(3016,1572,'Ost',ha='center')
    ax.set_aspect('equal');ax.legend(loc='upper right');ax.set_title('Lange Mauerzüge entlang der Sektorengrenze')
    fig.savefig(PREVIEW/'border_placement.png',dpi=140);plt.close(fig)

    icon_path=PREVIEW/'blender_tower_icon.png'
    if icon_path.exists():
        icon=Image.open(icon_path).convert('RGBA');icon=icon.crop(icon.getbbox())
        for size,folder,suffix in [(64,'large',''),(32,'small','_small')]:
            canvas=Image.new('RGBA',(size*2,size))
            height=size-4;width=max(5,round(icon.width/icon.height*height*1.6))
            frame=icon.resize((width,height),Image.Resampling.LANCZOS)
            canvas.alpha_composite(frame,((size-width)//2,2))
            grey=ImageOps.grayscale(frame).convert('RGBA');grey.putalpha(frame.getchannel('A'))
            canvas.alpha_composite(grey,(size+(size-width)//2,2))
            canvas.save(ROOT/f'gfx/interface/buildings/historical_buildings/{folder}/berlin_tv_tower_icon{suffix}.dds')
    print(PREVIEW/'berlin_landmarks.png')


if __name__=='__main__':main()
