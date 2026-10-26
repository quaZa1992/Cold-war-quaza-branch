# IMPERIA CW — Cold War: berlin landmarks — build.
"""Author and export Berlin landmarks in the installed Blender runtime."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CFG=json.loads((HERE/'config.json').read_text())
OUT=ROOT/'gfx/models/buildings/landmarks'
# Shared with the native Blender wall module. Surface colors stay restrained.
COLORS=[(184,181,172),(190,197,201),(27,41,48),(172,42,35),
        (226,224,213),(77,84,86),(172,159,132),(78,82,82),
        (86,103,65),(195,193,184),(164,178,181),(100,121,111),
        (190,197,201),(190,197,201),(190,197,201),(122,130,133)]


def textures():
    rng=np.random.default_rng(1969)
    diffuse=np.zeros((512,512,4),dtype=np.uint8)
    # HoI4's Advanced shader stores emissive strength in B, not normal Z.
    normal=np.zeros_like(diffuse);normal[:]=[128,128,0,128]
    specular=np.zeros_like(diffuse)
    for k,color in enumerate(COLORS):
        row,col=divmod(k,4);y,x=row*128,col*128
        noise=rng.normal(0,.6 if k in [1,2,3,4,12,13,14] else 1.8,(128,128,1))
        tile=np.clip(np.array(color)+noise,0,255).astype(np.uint8)
        if k==2:
            tile[:,::16]=[104,115,117]
            tile[:2]=[98,110,113];tile[-2:]=[98,110,113]
        if k in [0,9]:
            # Subtle casting seams, with no black checkerboard or random plates.
            tile[::64]=np.maximum(tile[::64].astype(int)-5,0)
        diffuse[y:y+128,x:x+128,:3]=tile
        diffuse[y:y+128,x:x+128,3]=255
        metal=k in [1,5,12,13,14,15]
        roughness=100 if k in [1,12,13,14] else 60 if k==2 else 160 if metal else 205
        specular[y:y+128,x:x+128]=[40,145 if metal or k==2 else 45,210 if metal else 0,roughness]
        if k==1:
            # Fine pyramidal metal cladding affects normals, never panel colors.
            yy,xx=np.mgrid[0:128,0:128]
            u=(xx/128*24)%1-.5;v=(yy/128*12)%1-.5
            nx=np.where(abs(u)>abs(v),np.sign(u)*.055,0)
            ny=np.where(abs(v)>=abs(u),np.sign(v)*.055,0)
            normal[y:y+128,x:x+128,0]=np.clip(128+nx*127,0,255).astype(np.uint8)
            normal[y:y+128,x:x+128,1]=np.clip(128+nx*127,0,255).astype(np.uint8)
            normal[y:y+128,x:x+128,3]=np.clip(128+ny*127,0,255).astype(np.uint8)
    for name,pixels in [('diffuse',diffuse),('normal',normal),('specular',specular)]:
        Image.fromarray(pixels).save(OUT/f'mdcw_berlin_landmarks_{name}.dds')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--blender',type=Path,default=Path(CFG['blender']))
    parser.add_argument('--game',type=Path,help='Accepted for compatibility; Blender export does not need game files.')
    args=parser.parse_args()
    assert args.blender.is_file(),f'Blender not found: {args.blender}'
    textures()
    runtime=HERE/'runtime';runtime.mkdir(exist_ok=True)
    environment=os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE']='1'
    environment['BLENDER_USER_CONFIG']=str(runtime)
    subprocess.run([str(args.blender),'--background','--factory-startup','--python-exit-code','1','--python',str(HERE/'blender_landmarks.py')],
                   cwd=ROOT,env=environment,check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    subprocess.run([str(args.blender),'--background',str(HERE/'source/tv_tower.blend'),
                    '--python-exit-code','1','--python',str(HERE/'blender_render_icon.py')],
                   cwd=ROOT,env=environment,check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    subprocess.run([str(args.blender),'--background','--factory-startup','--python-exit-code','1',
                    '--python',str(HERE/'blender_verify_export.py')],
                   cwd=ROOT,env=environment,check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
