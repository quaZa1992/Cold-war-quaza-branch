# IMPERIA COLD WAR — Install Cyprus focus artwork without gameplay or position changes.
from pathlib import Path
import argparse,base64,datetime,hashlib,io,json,re,sys,zipfile
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
VIS=Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef0-dd9d-7a11-b0e5-985305e237a1')
sys.path.insert(0,str(ROOT/'tools'));sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse
from cyprus_1970_rework.compile import generate
from cyprus_1970_rework.compact_layout import positions
TREE='common/national_focus/COLDWAR_CYP_1970_focus.txt'

def semantic(text):
 rows=parse(text)
 for k,o,tree in rows:
  if k!='focus_tree':continue
  for key,op,focus in tree:
   if key=='focus':focus[:]=[(a,b,c)for a,b,c in focus if a!='icon']
 return rows

def write(path,text):
 temp=path.with_suffix(path.suffix+'.cyprus-staged');temp.write_text(text,encoding='utf8',newline='\n');temp.replace(path)

def preview(design):
 path=VIS/'cyprus-1970-rework.html';s=path.read_text('utf8');m=re.search(r'const D=(\{[^\n]+\});',s);assert m
 d=json.loads(m[1]);by={f['key']:f for f in design['focuses']};d['icon_images']={};d['art']={}
 for f in d['focuses']:
  source=by[f['key']];f['sprite']=source['sprite'];f['icon']=source['icon']
  if source['sprite']in d['icon_images']:continue
  im=Image.open(ROOT/source['icon']).convert('RGBA');im.thumbnail((96,96),Image.Resampling.LANCZOS)
  im=im.quantize(colors=128,method=Image.Quantize.FASTOCTREE)
  data=io.BytesIO();im.save(data,format='PNG',optimize=True)
  d['icon_images'][source['sprite']]='data:image/png;base64,'+base64.b64encode(data.getvalue()).decode('ascii')
 d['geometry']['grid_x_px']=96
 s=s[:m.start(1)]+json.dumps(d,separators=(',',':'),ensure_ascii=False)+s[m.end(1):]
 s=s.replace('${D.art[f.group]}','${D.icon_images[f.sprite]}')
 # Match the actual installed nationalfocusview.gui focus_spacing x96/y130.
 s=s.replace('f.x*85','f.x*96')
 s=s.replace('width:4900px;height:2500px','width:5500px;height:2500px').replace('width="4900" height="2500"','width="5500" height="2500"')
 assert len(s.encode('utf8'))<1000000
 write(path,s)
 write(HERE/'compact-preview.html','<!doctype html><html lang="en"><meta charset="utf-8"><title>IMPERIA COLD WAR: Cyprus focus art</title><body style="margin:0">'+s+'</body></html>')
 return len(s.encode('utf8'))

def contact(design):
 sheet=Image.new('RGB',(1200,1500),'#20282a');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
 for i,f in enumerate(design['focuses']):
  x=i%10*120;y=i//10*150;im=Image.open(ROOT/f['icon']).convert('RGBA');im.thumbnail((96,96),Image.Resampling.LANCZOS)
  sheet.paste(im,(x+(120-im.width)//2,y+2),im)
  words=f['title'].split();lines=['']
  for word in words:
   if draw.textlength((lines[-1]+' '+word).strip(),font=font)>114:lines.append(word)
   else:lines[-1]=(lines[-1]+' '+word).strip()
  for j,line in enumerate(lines[:3]):draw.text((x+3,y+100+j*15),line,font=font,fill='#ece4c8')
 sheet.save(HERE/'focus-icons-review.png')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');args=parser.parse_args()
 design,files,loc,meta=generate();old=(ROOT/TREE).read_text('utf8');new=files[TREE]
 assert semantic(old)==semantic(new),'Non-icon changes would be installed.'
 assert positions(old)[0]==positions(new)[0],'Compact geometry changed.'
 own=[TREE,'interface/COLDWAR_CYP_R2_focus_icons.gfx','interface/COLDWAR_CYP_R2_focus_shine.gfx']
 for path,text in files.items():
  if path not in own:assert (ROOT/path).read_text('utf-8-sig')==text,('Unrelated generator drift',path)
 ids=re.findall(r'\bicon = (GFX_COLDWAR_CYP_R2_art_\w+)',new);assert len(ids)==100
 for sprite in ids:
  assert 'name = "'+sprite+'"'in files[own[1]]
  assert 'name = "'+sprite+'_shine"'in files[own[2]]
 clearance=[]
 for item in design['focus_art'].values():
  im=Image.open(ROOT/item['texture']).convert('RGBA');box=im.getbbox();assert box
  gap=58-(20-im.height/2+box[3]);assert gap>=1,(item['texture'],gap)
  clearance.append(gap)
 report={'project':'IMPERIA COLD WAR','focuses':100,'distinct_icons':meta['art']['distinct_icons'],'generated_icons':3,'custom_focuses':meta['art']['custom_focuses'],'gameplay_unchanged':True,'compact_positions_unchanged':True,'sprites_and_shine_resolve':True,'native_title_clearance_px_min':min(clearance),'native_art_retested_in_game':False,'assignments':design['focus_art'],'tree_sha256':hashlib.sha256(new.encode()).hexdigest()}
 if args.install:
  archive=Path('E:/MDColdWar_Backups/Codex_Test_Archives')/('CYP_art_before_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.zip')
  with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED)as z:
   for rel in own+['tools/cyprus_1970_rework/manifest.json']:
    if (ROOT/rel).is_file():z.writestr(rel,(ROOT/rel).read_bytes())
   z.writestr('cyprus-1970-rework.html',(VIS/'cyprus-1970-rework.html').read_bytes())
  for rel in own:write(ROOT/rel,files[rel])
  report['archive']=archive.as_posix();report['installed']=True;report['preview_bytes']=preview(design)
  contact(design)
  manifest=json.loads((HERE/'manifest.json').read_text('utf8'))
  manifest['generated_files']=list(files);manifest['meta']['art']=meta['art'];manifest['art_revision']={'project':'IMPERIA COLD WAR','report':'tools/cyprus_1970_rework/ART_REPORT.json','native_art_retested':False}
  write(HERE/'manifest.json',json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
  layout=json.loads((HERE/'LAYOUT_REPORT.json').read_text('utf8'));layout.setdefault('pre_icon_tree_sha256',layout['tree_sha256']);layout['tree_sha256']=report['tree_sha256'];layout['icon_only_refresh']=True
  write(HERE/'LAYOUT_REPORT.json',json.dumps(layout,indent=2)+'\n')
 write(HERE/'ART_REPORT.json',json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:report[k]for k in ['focuses','distinct_icons','generated_icons','custom_focuses','gameplay_unchanged','compact_positions_unchanged','sprites_and_shine_resolve']}))

if __name__=='__main__':main()
