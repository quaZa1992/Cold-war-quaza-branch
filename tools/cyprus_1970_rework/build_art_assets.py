# IMPERIA COLD WAR — Convert selected generated icon sources to native DDS.
"""Mechanical format conversion only; never redraw or remove generated alpha."""
from pathlib import Path
import hashlib,json
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from cyprus_1970_rework.art import CUSTOM,native_copy

def frame(image):
 """Fit the native symbol above its y58 title, without changing the global GUI."""
 image=image.copy();image.thumbnail((96,74),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(100,78),(0,0,0,0))
 canvas.paste(image,((100-image.width)//2,(78-image.height)//2))
 return canvas

def main():
 records=json.loads((HERE/'art_sources/sources.json').read_text('utf8'))
 out=ROOT/'gfx/interface/goals/coldwar_cyprus_r2';out.mkdir(parents=True,exist_ok=True)
 for key,item in records['assets'].items():
  source=HERE/'art_sources'/(key+'.png')
  image=Image.open(source).convert('RGBA')
  assert image.getextrema()[3][0]==0 and image.getextrema()[3][1]==255
  native=frame(image)
  destination=out/(key+'.dds');native.save(destination,format='DDS')
  reopened=Image.open(destination).convert('RGBA')
  assert reopened.tobytes()==native.tobytes() and destination.read_bytes()[:4]==b'DDS '
  item.update({'workspace_source':source.relative_to(ROOT).as_posix(),'runtime_asset':destination.relative_to(ROOT).as_posix(),'native_size':[100,78],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'alpha_preserved':True,'modifications':'Aspect-preserving downscaling, transparent padding and lossless RGBA DDS conversion. Source unchanged.'})
 choices=json.loads((HERE/'native_icon_choices.json').read_text('utf8'))['focuses'];copies={}
 for key,item in choices.items():
  if key in CUSTOM:continue
  source=ROOT/item['texture'];destination=ROOT/native_copy(item['texture'])
  if destination.as_posix()in copies:continue
  destination.parent.mkdir(parents=True,exist_ok=True)
  native=frame(Image.open(source).convert('RGBA'));native.save(destination,format='DDS')
  copies[destination.as_posix()]={'source':item['texture'],'runtime':destination.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'size':[100,78],'alpha_bounds':native.getbbox(),'modifications':'Country-local copy, scaled to fit native focus symbol. Original unchanged.','original_author':'Unknown in available MD snapshot','separate_permission':'Unknown; original asset rights remain applicable.'}
 (HERE/'NATIVE_ART_COPIES.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','copies':list(copies.values())},indent=2)+'\n',encoding='utf8')
 (HERE/'art_sources/sources.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf8')
 print(json.dumps({'project':'IMPERIA COLD WAR','generated_converted':len(records['assets']),'native_copies':len(copies),'alpha_preserved':True}))

if __name__=='__main__':main()
