# IMPERIA CW — Cold War: bucharest landmarks — materials.
"""Independent mipmapped stone/arcade/roof atlas for Casa Scinteii."""
from pathlib import Path
import importlib.util
import math
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'gfx/models/buildings/landmarks'
PREFIX='mdcw_bucharest_scinteii'
spec=importlib.util.spec_from_file_location('warsaw_dds_reuse',ROOT/'tools/warsaw_landmarks/materials.py')
reuse=importlib.util.module_from_spec(spec);spec.loader.exec_module(reuse)
STONE=(178,174,156);TRIM=(204,197,176)


def star_points(cx,cy,r):
    return [(cx+math.cos(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43),cy+math.sin(-math.pi/2+i*math.pi/5)*(r if i%2==0 else r*.43)) for i in range(10)]


def windows(tile,height,cols,rows,rng):
    d=ImageDraw.Draw(tile);h=ImageDraw.Draw(height)
    cw,ch=240/cols,240/rows
    for i in range(cols):
        x=8+(i+.5)*cw
        for j in range(rows):
            y=8+(j+.5)*ch;w=max(3,cw*.35);hh=ch*.62
            box=(int(x-w/2),int(y-hh/2),int(x+w/2),int(y+hh/2))
            a,b,c,e=box;pane=(47+int(rng.integers(-4,5)),55+int(rng.integers(-4,5)),54+int(rng.integers(-4,5)))
            d.rectangle((a-2,b-1,c+2,e+2),fill=(137,131,113))
            if j==0:
                cap=min(w,hh*.65)
                d.ellipse((a,b,c,b+cap),fill=pane);d.rectangle((a,b+cap/2,c,e),fill=pane)
            else:d.rectangle(box,fill=pane)
            h.rectangle(box,fill=95)
            d.line((x,b,x,e),fill=(151,148,129))
            if hh>17:d.line((a,y+1,c,y+1),fill=(134,134,119))
            d.rectangle((a-2,e+1,c+2,e+2),fill=TRIM)
            d.line((c+2,b,c+2,e+1),fill=(195,187,166))
    d.line((8,11,248,11),fill=(140,134,115),width=2)


def create():
    rng=np.random.default_rng(1956)
    colors=[STONE,STONE,STONE,(68,75,74),TRIM,(195,190,169),(83,82,70),(68,60,45),(156,153,138),STONE,(50,53,48),STONE,(111,64,56),STONE,STONE,STONE]
    diffuse=np.zeros((1024,1024,4),dtype=np.uint8);relief=np.full((1024,1024),128,dtype=np.uint8)
    for i,color in enumerate(colors):
        pixels=np.clip(np.array(color)+rng.normal(0,1.2,(256,256,1)),0,255).astype(np.uint8)
        tile=Image.fromarray(pixels);height=Image.new('L',(256,256),128)
        d=ImageDraw.Draw(tile);h=ImageDraw.Draw(height)
        if i in {1,2,9,11,15}:
            cols,rows={1:(13,11),2:(3,12),9:(8,4),11:(3,6),15:(6,11)}[i]
            windows(tile,height,cols,rows,rng)
        elif i==3:
            for x in range(8,249,24):
                d.line((x,8,x,248),fill=(45,52,51),width=2);d.line((x+2,8,x+2,248),fill=(89,94,87))
        elif i==5:
            d.rectangle((101,10,154,246),fill=(122,83,68));d.rectangle((111,10,144,246),fill=(156,109,84))
            d.line((98,10,98,246),fill=TRIM,width=3);d.line((157,10,157,246),fill=TRIM,width=3)
        elif i==12:
            d.rectangle((13,10,242,246),outline=(167,129,91),width=4)
            for x in [50,128,206]:
                d.arc((x-25,66,x+25,185),20,160,fill=(183,151,99),width=5)
                d.arc((x-25,66,x+25,185),200,340,fill=(183,151,99),width=5)
                d.polygon(star_points(x,104,17),fill=(198,171,111))
                d.line((x-8,145,x+9,128),fill=(187,160,103),width=4)
        elif i==14:
            d.rectangle((8,12,248,22),fill=TRIM);d.rectangle((8,231,248,242),fill=TRIM)
            for x in range(23,240,29):
                d.rectangle((x-8,81,x+8,202),fill=(122,116,99));d.ellipse((x-8,63,x+8,91),fill=(122,116,99))
                d.arc((x-11,55,x+11,91),180,360,fill=TRIM,width=4)
                h.rectangle((x-8,81,x+8,202),fill=103)
        elif i==13:
            # Distant courtyard arcades: a painted panel avoids hidden vault geometry.
            for j in range(12):
                x=8+(j+.5)*20
                d.ellipse((x-6,39,x+6,81),fill=(48,52,47))
                d.rectangle((x-6,60,x+6,241),fill=(48,52,47))
                h.rectangle((x-6,60,x+6,241),fill=95)
            d.rectangle((8,9,248,20),fill=TRIM)
        elif i in {0,4,8}:
            for y in range(8,249,28):
                d.line((8,y,248,y),fill=tuple(max(0,c-11) for c in color))
                for x in range(8+(28 if y%56 else 0),249,56):d.line((x,y,x,y+28),fill=tuple(max(0,c-6) for c in color))
        row,col=divmod(i,4);y,x=row*256,col*256
        diffuse[y:y+256,x:x+256,:3]=np.asarray(tile);diffuse[y:y+256,x:x+256,3]=255
        relief[y:y+256,x:x+256]=np.asarray(height)
    gy,gx=np.gradient(relief.astype(float)/255)
    normal=np.zeros_like(diffuse);normal[:,:,0]=np.clip(128-gx*90,30,225).astype(np.uint8)
    normal[:,:,1]=normal[:,:,0];normal[:,:,3]=np.clip(128+gy*90,30,225).astype(np.uint8)
    normal[:,:,2][relief<110]=4
    specular=np.zeros_like(diffuse);specular[:]=[40,40,0,205];specular[relief<110]=[40,80,0,135]
    for i in [3,6]:
        row,col=divmod(i,4);specular[row*256:(row+1)*256,col*256:(col+1)*256]=[40,80,105,165]
    for kind,pixels,codec in [('diffuse',diffuse,'DXT1'),('normal',normal,'DXT5'),('specular',specular,'DXT5')]:
        reuse.save_mipmapped_dds(Image.fromarray(pixels),OUT/f'{PREFIX}_{kind}.dds',codec)


if __name__=='__main__':create()
