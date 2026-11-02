# IMPERIA COLD WAR — Install and inspect Cyprus spacing without gameplay changes.
from pathlib import Path
import argparse, datetime, hashlib, json, re, sys, zipfile

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
VIS=Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef0-dd9d-7a11-b0e5-985305e237a1')
TREE='common/national_focus/COLDWAR_CYP_1970_focus.txt'
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse
from cyprus_1970_rework.compile import generate

def semantic(text):
 rows=parse(text)
 for key,op,tree in rows:
  if key!='focus_tree':continue
  tree[:]=[(k,o,v)for k,o,v in tree if k!='continuous_focus_position']
  for k,o,v in tree:
   if k=='focus':v[:]=[(a,b,c)for a,b,c in v if a not in('x','y','relative_position_id')]
 return rows

def positions(text):
 tree=next(v for k,o,v in parse(text)if k=='focus_tree')
 result={};order=[];nodes={}
 for k,o,v in tree:
  if k!='focus':continue
  def one(key,default=None):return next((c for a,b,c in v if a==key),default)
  ident=one('id');anchor=one('relative_position_id');x=int(one('x'));y=int(one('y'))
  if anchor:
   assert anchor in result,('forward or missing anchor',ident,anchor)
   x+=result[anchor][0];y+=result[anchor][1]
  result[ident]=(x,y);order.append(ident);nodes[ident]=v
 return result,nodes

def audit(before,after,design):
 old,_=positions(before);new,nodes=positions(after)
 assert semantic(before)==semantic(after),'Gameplay changed during a spacing-only operation.'
 assert len(old)==len(new)==100 and old.keys()==new.keys()
 assert new=={n['id']:(n['x'],n['y'])for n in design['focuses']}
 rectangles={k:(x*85,y*130,x*85+165,y*130+128)for k,(x,y)in new.items()}
 overlaps=[];hits=[]
 items=list(rectangles.items())
 for i,(a,r)in enumerate(items):
  for b,s in items[i+1:]:
   if max(r[0],s[0])<min(r[2],s[2])and max(r[1],s[1])<min(r[3],s[3]):overlaps.append([a,b])
 def hit(segment,rect):
  x1,y1,x2,y2=segment;l,t,r,b=rect
  return (l<x1<r and max(min(y1,y2),t)<min(max(y1,y2),b))if x1==x2 else(t<y1<b and max(min(x1,x2),l)<min(max(x1,x2),r))
 for f in design['focuses']:
  x,y=new[f['id']]
  for group in f['prerequisites']:
   for key in group:
    parent='COLDWAR_CYP_R2_'+key;px,py=new[parent]
    start=(px*85+82,py*130+108);end=(x*85+82,y*130+5);mid=(start[1]+end[1])/2
    segs=[(*start,start[0],mid),(start[0],mid,end[0],mid),(end[0],mid,*end)]
    for other,rect in rectangles.items():
     if other not in(parent,f['id'])and any(hit(s,rect)for s in segs):hits.append([parent,f['id'],other])
 assert not overlaps,overlaps
 assert not hits,hits
 def bounds(p):
  xs=[v[0]for v in p.values()];ys=[v[1]for v in p.values()]
  return [min(xs),max(xs),min(ys),max(ys)]
 a,b=bounds(old),bounds(new)
 return {'project':'IMPERIA COLD WAR','focuses':100,'old_bounds':a,'new_bounds':b,
  'horizontal_span_reduction_percent':round((1-(b[1]-b[0])/(a[1]-a[0]))*100,1)if a[1]!=b[1]else 0,
  'semantics_unchanged':True,'card_overlaps':overlaps,'approximate_connector_card_collisions':hits,
  'card_pixels':[165,128],'grid_pixels':[85,130],
  'limits':'External native-card reconstruction. Grid pitch, font and connector routing are approximations; no new in-engine layout inspection.',
  'positions':{k:{'before':list(old[k]),'after':list(new[k])}for k in old},
  'tree_sha256':hashlib.sha256(after.encode('utf8')).hexdigest()}

def preview(design):
 path=VIS/'cyprus-1970-rework.html';s=path.read_text('utf8')
 match=re.search(r'const D=(\{[^\n]+\});',s);assert match
 data=json.loads(match[1]);by={n['id']:n for n in design['focuses']}
 for f in data['focuses']:
  n=by[f['id']]
  for key in('x','y','anchor','emitted_xy'):f[key]=n[key]
  if 'offset'in f:f['offset']=n['emitted_xy']
 data['groups']=design['groups'];data['status']='Installed compact spacing revision'
 s=s[:match.start(1)]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+s[match.end(1):]
 s=s.replace('Concept awaiting approval','Installed compact layout').replace('aria-label="Concept views"','aria-label="Cyprus views"')
 s=s.replace('width:8500px;height:2800px','width:4900px;height:2500px').replace('width="8500" height="2800"','width="4900" height="2500"')
 s=s.replace('let middle=(a.y+85+p.y)/2','let middle=(a.y+108+p.y+5)/2')
 old="camera.s=Math.min((stage.clientWidth-30)/8500,(stage.clientHeight-55)/2800);camera.x=0;camera.y=30;paint()"
 new="let xs=D.focuses.map(f=>f.x*85+30),ys=D.focuses.map(f=>f.y*130+65);let left=Math.min(...xs),top=Math.min(...ys),width=Math.max(...xs)-left+165,height=Math.max(...ys)-top+128;camera.s=Math.min((stage.clientWidth-40)/width,(stage.clientHeight-45)/height);camera.x=20-left*camera.s;camera.y=25-top*camera.s;paint()"
 assert old in s or new in s or new.replace('f.x*85','f.x*96')in s
 s=s.replace(old,new)
 s=s.replace("activeTab='cw-escalation';all('[role=tab]')","activeTab='cw-tree';all('[role=tab]')")
 s=s.replace('white-space:nowrap;line-height:1.1;min-height:20px','white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.1;min-height:20px')
 s=s.replace("b.setAttribute('aria-label',f.title);b.setAttribute('aria-pressed'","b.setAttribute('aria-label',f.title);b.setAttribute('data-tooltip',f.title);b.setAttribute('aria-pressed'")
 path.write_text(s,encoding='utf8')
 (HERE/'compact-preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>IMPERIA COLD WAR: Cyprus compact spacing</title><body style="margin:0">'+s+'</body></html>',encoding='utf8')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');args=parser.parse_args()
 design,files,loc,meta=generate();before=(ROOT/TREE).read_text('utf8');after=files[TREE]
 report=audit(before,after,design)
 if args.install:
  stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
  archive=Path('E:/MDColdWar_Backups/Codex_Test_Archives')/('CYP_spacing_before_'+stamp+'.zip')
  with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED)as z:
   for rel in [TREE,'tools/cyprus_1970_rework/manifest.json']:z.writestr(rel,(ROOT/rel).read_bytes())
   z.writestr('cyprus-1970-rework.html',(VIS/'cyprus-1970-rework.html').read_bytes())
  staged=(ROOT/TREE).with_suffix('.cyprus-staged');staged.write_text(after,encoding='utf8',newline='\n');staged.replace(ROOT/TREE)
  assert positions((ROOT/TREE).read_text('utf8'))[0]==positions(after)[0]
  report['archive']=archive.as_posix();report['installed']=True
  preview(design)
  manifest=json.loads((HERE/'manifest.json').read_text('utf8'))
  manifest['layout_revision']={'project':'IMPERIA COLD WAR','id':'compact_spacing_20261028','report':'tools/cyprus_1970_rework/LAYOUT_REPORT.json','native_layout_retested':False}
  (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 (HERE/'LAYOUT_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 print(json.dumps({k:report[k]for k in ['focuses','old_bounds','new_bounds','horizontal_span_reduction_percent','semantics_unchanged','card_overlaps','approximate_connector_card_collisions']}))

if __name__=='__main__':main()
