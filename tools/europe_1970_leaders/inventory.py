# IMPERIA COLD WAR — German, Soviet republic and Eastern Bloc portrait inventory.
from pathlib import Path
import json
import re
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from multiplayer_quality.audit import parse

TAGS=['GER','DDR','SOV','UKR','BLR','EST','LAT','LIT','ARM','AZE','GEO','KAZ','KYR','TAJ','TRK','UZB','MLV','POL','CZE','HUN','ROM','BUL','ALB','YUG','MON']
def walk(tree):
    for k,o,v in tree:
        yield k,o,v
        if isinstance(v,list):yield from walk(v)
def first(tree,key,default=None):return next((v for k,o,v in tree if k==key),default)
def value(v):return v.strip('"') if isinstance(v,str) else v
def resolve(picture,tag):
    for p in [ROOT/picture,ROOT/'gfx/leaders'/tag/picture,ROOT/'gfx/leaders'/picture]:
        if p.is_file():return p.relative_to(ROOT).as_posix()
    return None

def main():
    HERE.mkdir(exist_ok=True)
    known=json.loads((ROOT/'tools/historical_politics_1970/portrait_sources.json').read_text(encoding='utf-8'))['assets']
    manifest=json.loads((ROOT/'tools/historical_politics_1970/portrait_manifest.json').read_text(encoding='utf-8'))
    loc={}
    for path in (ROOT/'localisation/english').glob('*DDR*.yml'):
        for k,v in re.findall(r'^\s*([^\s:#]+):\d*\s*"(.*)"',path.read_text(encoding='utf-8-sig'),re.M):loc[k]=v
    rows=[]
    for tag in TAGS:
        history=next((p for p in (ROOT/'history/countries').glob(tag+' - *.txt')),None)
        if not history:continue
        tree=parse(history.read_text(encoding='utf-8-sig'))
        start=first(tree,'1970.1.1',[])
        for k,o,v in walk(start):
            if k!='create_country_leader':continue
            name=value(first(v,'name',''));picture=value(first(v,'picture',''))
            rows.append(dict(tag=tag,name=loc.get(name,name),runtime_name=name,portrait=resolve(picture,tag),picture_literal=picture,
                ideology=value(first(v,'ideology','')),provider=history.relative_to(ROOT).as_posix(),kind='1970 history'))
        if tag in ('GER','DDR'):
            files=list((ROOT/'common/scripted_effects').glob('COLDWAR_'+tag+'_1970*effects.txt'))
            files+=list((ROOT/'common/national_focus').glob('COLDWAR_'+tag+'_1970*.txt'))
            for path in files:
                for k,o,v in walk(parse(path.read_text(encoding='utf-8-sig'))):
                    if k!='create_country_leader':continue
                    name=value(first(v,'name',''));picture=value(first(v,'picture',''))
                    rows.append(dict(tag=tag,name=loc.get(name,name),runtime_name=name,portrait=resolve(picture,tag) if picture else None,
                        picture_literal=picture,ideology=value(first(v,'ideology','')),provider=path.relative_to(ROOT).as_posix(),kind='1970 tree provider'))
    unique={}
    for r in rows:
        key=(r['tag'],r['name'])
        if key not in unique or not unique[key]['portrait']:unique[key]=r
    people=list(unique.values())
    for r in people:
        matches=[(k,v) for k,v in known.items() if (v.get('name')==r['name'] or v.get('portrait','').lower()==(r['portrait'] or '').lower()) and k.startswith(r['tag']+'_')]
        if matches:r['known_key'],r['known_source']=matches[0]
    (HERE/'INVENTORY.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',people=people,all_bindings=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for group,subset in [('GER',[r for r in people if r['tag']=='GER']),('DDR',[r for r in people if r['tag']=='DDR']),('BLOC',[r for r in people if r['tag'] not in ('GER','DDR')])]:
        sheet=Image.new('RGB',(1360,((len(subset)+7)//8)*240),'#20272b');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
        for i,r in enumerate(subset):
            x,y=i%8*170,i//8*240
            if r['portrait']:
                sheet.paste(ImageOps.fit(Image.open(ROOT/r['portrait']).convert('RGB'),(156,210)),(x,y))
            draw.text((x+78,y+222),(r['tag']+' '+r['name'])[:25],font=font,fill='white',anchor='mm')
        sheet.save(HERE/(group+'_BEFORE.png'))
        print(group,len(subset))
        for r in subset:print(r['tag'],r['name'],r['ideology'],r['portrait'])

if __name__=='__main__':main()
