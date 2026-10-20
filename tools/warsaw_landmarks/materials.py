"""Mipmapped facade atlas; texture panels replace per-window geometry."""
from io import BytesIO
from pathlib import Path
import struct
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'gfx/models/buildings/landmarks'
PREFIX='mdcw_warsaw_palace'
SIZE=1024
CELL=SIZE//4
STONE=(169,159,138)
TRIM=(191,180,156)
SHADE=(113,106,91)


def save_mipmapped_dds(image,path,codec):
    levels=[]
    while True:
        buffer=BytesIO();image.save(buffer,format='DDS',pixel_format=codec)
        levels.append(buffer.getvalue())
        if image.size==(1,1):break
        image=image.resize((max(1,image.width//2),max(1,image.height//2)),Image.Resampling.BOX)
    header=bytearray(levels[0][:128])
    struct.pack_into('<I',header,8,struct.unpack_from('<I',header,8)[0]|0x20000)
    struct.pack_into('<I',header,28,len(levels))
    struct.pack_into('<I',header,20,len(levels[0])-128)
    struct.pack_into('<I',header,108,0x1000|0x8|0x400000)
    path.write_bytes(bytes(header)+b''.join(level[128:] for level in levels))


def facade(tile,height,cols,rows,rng,slender=.40,ground=False):
    d=ImageDraw.Draw(tile);hmap=ImageDraw.Draw(height)
    cw,ch=240/cols,240/rows
    for col in range(cols):
        cx=8+(col+.5)*cw
        if not ground:d.line((cx-cw*.48,8,cx-cw*.48,248),fill=(187,177,154),width=2)
        for row in range(rows):
            cy=8+(row+.5)*ch;w=cw*slender;h=ch*(.67 if ground else .57)
            a,b,c,e=int(cx-w/2),int(cy-h/2),int(cx+w/2),int(cy+h/2)
            d.rectangle((a-2,b-1,c+2,e+2),fill=SHADE)
            pane=(50+int(rng.integers(-6,7)),56+int(rng.integers(-4,5)),55+int(rng.integers(-4,5)))
            d.rectangle((a,b,c,e),fill=pane);hmap.rectangle((a,b,c,e),fill=90)
            d.line((a,b,a,e),fill=(145,139,121));d.line((c,b,c,e),fill=TRIM)
            d.line((cx,b,cx,e),fill=(136,133,115))
            if h>12:d.line((a,cy+1,c,cy+1),fill=(128,128,111))
            d.rectangle((a-2,e+1,c+2,e+3),fill=TRIM);hmap.rectangle((a-2,e+1,c+2,e+3),fill=150)
    d.rectangle((8,8,247,11),fill=SHADE);d.rectangle((8,12,247,15),fill=TRIM)


def create():
    rng=np.random.default_rng(1955)
    colors=[STONE,STONE,STONE,(78,83,77),TRIM,(126,115,83),(76,78,72),(67,54,40),(157,151,134),STONE,STONE,(146,138,120),STONE,STONE,STONE,STONE]
    diffuse=np.zeros((SIZE,SIZE,4),dtype=np.uint8);relief=np.full((SIZE,SIZE),128,dtype=np.uint8)
    for i,color in enumerate(colors):
        pixels=np.clip(np.array(color)+rng.normal(0,1.3,(CELL,CELL,1)),0,255).astype(np.uint8)
        tile=Image.fromarray(pixels);height=Image.new('L',(CELL,CELL),128)
        d=ImageDraw.Draw(tile);hmap=ImageDraw.Draw(height)
        if i in {1,2,9,10,15}:
            cols,rows,slender={1:(7,18,.40),2:(5,10,.38),9:(8,5,.32),10:(6,1,.52),15:(5,7,.36)}[i]
            facade(tile,height,cols,rows,rng,slender,i==10)
        elif i==12:
            # Original clockless cap: solid upper field and tall openings below.
            d.rectangle((18,18,238,145),outline=(150,141,121),width=3)
            d.rectangle((23,23,233,140),outline=(188,177,151),width=2)
            for x in [58,106,154,202]:
                d.rectangle((x-9,163,x+9,237),fill=(49,54,50));d.line((x,163,x,237),fill=(145,139,118),width=2)
                d.rectangle((x-12,238,x+12,241),fill=TRIM);hmap.rectangle((x-9,163,x+9,237),fill=90)
            d.rectangle((8,148,248,154),fill=TRIM)
        elif i==13:
            for y in range(8,249,19):
                d.line((8,y,248,y),fill=(124,117,101),width=2);d.line((8,y+3,248,y+3),fill=(186,175,149))
            for x in [47,101,155,209]:
                d.rectangle((x-13,63,x+13,231),fill=(56,57,49));d.rectangle((x-17,57,x+17,64),fill=TRIM)
                hmap.rectangle((x-13,63,x+13,231),fill=85)
        elif i==14:
            d.rectangle((8,9,248,24),fill=TRIM);d.rectangle((8,27,248,34),fill=SHADE);d.rectangle((8,226,248,240),fill=TRIM)
            for x in range(24,240,29):
                d.rectangle((x-8,65,x+8,200),fill=(124,116,99));d.rectangle((x-5,70,x+5,194),fill=(151,141,119))
                d.ellipse((x-9,49,x+9,85),fill=TRIM);d.polygon([(x-11,51),(x,29),(x+11,51)],fill=TRIM)
                hmap.rectangle((x-8,65,x+8,200),fill=100)
        elif i==3:
            for x in range(8,249,24):
                d.line((x,8,x,248),fill=(61,66,60),width=2);d.line((x+2,8,x+2,248),fill=(95,99,88))
        elif i in {0,4,8,11}:
            for y in range(8,249,30):
                d.line((8,y,248,y),fill=tuple(max(0,c-10) for c in color))
                for x in range(8+(15 if y%60 else 0),249,60):d.line((x,y,x,y+30),fill=tuple(max(0,c-7) for c in color))
        row,col=divmod(i,4);y,x=row*CELL,col*CELL
        diffuse[y:y+CELL,x:x+CELL,:3]=np.asarray(tile);diffuse[y:y+CELL,x:x+CELL,3]=255
        relief[y:y+CELL,x:x+CELL]=np.asarray(height)
    gy,gx=np.gradient(relief.astype(float)/255)
    normal=np.zeros_like(diffuse);nx=np.clip(128-gx*100,24,232).astype(np.uint8);ny=np.clip(128+gy*100,24,232).astype(np.uint8)
    normal[:,:,0]=nx;normal[:,:,1]=nx;normal[:,:,3]=ny
    # HoI4 packs emission in blue, normal Y in alpha.
    windows=relief<110;normal[:,:,2][windows]=6
    specular=np.zeros_like(diffuse);specular[:]=[40,38,0,205];specular[windows]=[40,90,0,125]
    for i in [3,5,6]:
        row,col=divmod(i,4);specular[row*CELL:(row+1)*CELL,col*CELL:(col+1)*CELL]=[40,75,100,165]
    for name,pixels,codec in [('diffuse',diffuse,'DXT1'),('normal',normal,'DXT5'),('specular',specular,'DXT5')]:
        save_mipmapped_dds(Image.fromarray(pixels),OUT/f'{PREFIX}_{name}.dds',codec)


if __name__=='__main__':create()
