# IMPERIA COLD WAR — Identified photographs for German and Eastern portrait restorations.
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageOps, ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.catalogue import PEOPLE
from superpower_1970_leaders.prepare import USER_AGENT, query

TITLE_FIX={
 'wolfgang_biermann':('de','Wolfgang Biermann'),
 'otto_lambsdorff':('en','Otto Graf Lambsdorff'),
 'louis_ferdinand':('en','Louis Ferdinand, Prince of Prussia'),
 'wolfgang_harich':('en','Wolfgang Harich'),
 'SOV_grigory_yavlinsky':('en','Grigory Yavlinsky'),
 'SOV_maria_vladimirovna':('en','Grand Duchess Maria Vladimirovna of Russia'),
}

def slug(name):
    name=name.replace('ß','ss')
    import unicodedata
    return re.sub('[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',name) if not unicodedata.combining(c)).lower()).strip('_')

def targets():
    rows={}
    for p in PEOPLE:
        key=p['key']
        if key not in rows:
            rows[key]=dict(project='IMPERIA COLD WAR',id=key,name=p['name'],language='en',title=p['wikipedia_title'],groups=['Germany'],bindings=[],source_author='unknown',licence='unknown')
    inventory=json.loads((HERE/'INVENTORY.json').read_text(encoding='utf-8'))['people']
    for r in inventory:
        if r['tag'] in ('GER','DDR'):continue
        key=r['tag']+'_'+slug(r['name'])
        rows[key]=dict(project='IMPERIA COLD WAR',id=key,name=r['name'],language='en',title=r['name'],groups=['SSR and Eastern Bloc'],bindings=[r['portrait']],source_author='unknown',licence='unknown')
    sov=json.loads((ROOT/'tools/superpower_1970_leaders/runtime_roster.json').read_text(encoding='utf-8'))['people']
    already={r['portrait']:key for key,r in [(k,v) for k,v in rows.items()] if r.get('portrait')}
    for r in sov:
        if r['tag']!='SOV' or r['method']!='Existing identified mod portrait':continue
        # These three are already clear photographic portraits, inspected in the superpower review.
        if r['key'] in ('nikolai_ryzhkov','yuri_andropov','boris_yeltsin'):continue
        same=next((x for x in rows.values() if r['portrait'].lower() in [p.lower() for p in x['bindings'] if p]),None)
        if same:
            same['groups'].append('Soviet leadership');continue
        key=r['id']
        rows[key]=dict(project='IMPERIA COLD WAR',id=key,name=r['name'],language='en',title=r['wikipedia_title'],groups=['Soviet leadership'],bindings=[r['portrait']],source_author='unknown',licence='unknown')
    for key,row in rows.items():
        if key in TITLE_FIX:row['language'],row['title']=TITLE_FIX[key]
    return list(rows.values())

def download(row):
    if row.get('status')=='reference_ready' and (HERE/row['reference']).is_file():return row
    url=row.get('source_url')
    if not url:
        row['status']='missing_identified_photograph';return row
    suffix=Path(unquote(urlsplit(url).path)).suffix.lower()
    if suffix not in ('.jpg','.jpeg','.png','.webp'):row['status']='unsupported_format';return row
    target=HERE/'references'/(row['id']+suffix)
    try:
        if not target.exists():
            response=requests.get(url,headers={'User-Agent':USER_AGENT},timeout=45);response.raise_for_status();target.write_bytes(response.content)
        with Image.open(target) as im:
            row['dimensions']=list(im.size)
            # Technical downsampling only. Original photographs remain intact.
            preview=HERE/'inputs'/(row['id']+'.jpg');im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((1600,1600));im.save(preview,quality=95)
        row.update(status='reference_ready',reference=target.relative_to(HERE).as_posix(),generation_input=preview.relative_to(HERE).as_posix())
    except Exception as e:row.update(status='download_failed',error=str(e))
    return row

def main():
    for directory in ('references','inputs','masters','generated'):(HERE/directory).mkdir(exist_ok=True)
    old=json.loads((HERE/'sources.json').read_text(encoding='utf-8'))['portraits'] if (HERE/'sources.json').exists() else []
    old={r['id']:r for r in old};rows=targets()
    session=requests.Session();session.headers['User-Agent']=USER_AGENT
    for language in ('en','de'):
        required=[r for r in rows if r['language']==language and r['id'] not in old]
        pages=query(session,language,[r['title'] for r in required],piprop='original',pilicense='any') if required else lambda _:{}
        for row in required:
            p=pages(row['title']);row['source_url']=p.get('original',{}).get('source');row['source_page']='https://'+language+'.wikipedia.org/wiki/'+row['title'].replace(' ','_')
    needed=[]
    for i,row in enumerate(rows):
        if row['id'] in old:
            rows[i]={**row,**old[row['id']]};continue
        url=row.get('source_url') or ''
        if '/commons/' in url:
            tail=urlsplit(url).path.split('/commons/',1)[1]
            name=tail.split('/')[-2] if tail.startswith('thumb/') else tail.split('/')[-1]
            row['commons_file']='File:'+unquote(name);needed.append(row['commons_file'])
    metadata={}
    for i in range(0,len(needed),45):
        response=session.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',redirects=1,titles='|'.join(needed[i:i+45]),prop='imageinfo',iiprop='url|extmetadata'),timeout=45)
        response.raise_for_status()
        for p in response.json()['query']['pages'].values():metadata[p['title'].replace('_',' ')]=p.get('imageinfo',[{}])[0]
    for row in rows:
        info=metadata.get(row.get('commons_file','').replace('_',' '),{});ext=info.get('extmetadata',{})
        if info:
            row.update(source_url=info.get('url',row.get('source_url')),source_page=info.get('descriptionurl',row.get('source_page')),
                source_author=ext.get('Artist',{}).get('value','unknown'),licence=ext.get('LicenseShortName',{}).get('value','unknown'),licence_url=ext.get('LicenseUrl',{}).get('value','unknown'),commons_metadata=info)
    with ThreadPoolExecutor(max_workers=2) as pool:
        complete=[]
        for future in as_completed([pool.submit(download,row) for row in rows]):
            row=future.result();complete.append(row);print(row['id'],row['status'],flush=True)
    complete.sort(key=lambda r:r['id'])
    (HERE/'sources.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=complete),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for group,predicate in [('Germany',lambda r:'Germany' in r['groups']),('East',lambda r:'Germany' not in r['groups'])]:
        items=[r for r in complete if predicate(r)];sheet=Image.new('RGB',(1280,((len(items)+7)//8)*230),'#20272b');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',11)
        for i,row in enumerate(items):
            x,y=i%8*160,i//8*230
            if row.get('generation_input'):sheet.paste(ImageOps.fit(Image.open(HERE/row['generation_input']),(148,200),centering=(.5,.1)),(x,y))
            draw.text((x+74,y+215),row['id'][:24],font=font,fill='white',anchor='mm')
        sheet.save(HERE/(group+'_SOURCE_REVIEW.png'))

if __name__=='__main__':main()
