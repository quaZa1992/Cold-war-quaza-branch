"""Document and download party logo references, keeping later parties playable."""
import json
import requests
from pathlib import Path
from PIL import Image
from download_portraits import ROOT

HERE=Path(__file__).resolve().parent
OUT=HERE/'party_logo_sources'
TITLES={0:'National Democratic Party (Egypt)',1:'Conservative Party (Egypt)',
 2:'Free Egyptians Party',3:'Egyptian Social Democratic Party',
 4:'Egyptian Communist Party',5:'Revolutionary Socialists (Egypt)',
 6:'Dignity Party (Egypt)',7:'Arab Democratic Nasserist Party',
 10:'Al-Nour Party',11:'Ansar Bayt al-Maqdis',12:'Muslim Brotherhood',
 14:'New Wafd Party',15:"Republican People's Party (Egypt)",
 16:'Reform and Development Misruna Party',17:'Egyptian Green Party',
 18:'Arab Socialist Union (Egypt)',19:'National Progressive Unionist Party',
 20:'Homeland Defenders Party',21:"Arab Socialist Ba'ath Party – Egypt Region",
 24:'Socialist Popular Alliance Party',25:"Nation's Future Party"}

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    session=requests.Session(); session.headers['User-Agent']='MdcoldwarHistoricalPortraitResearch/1.0'
    r=session.get('https://en.wikipedia.org/w/api.php',params={'action':'query','format':'json',
        'redirects':1,'titles':'|'.join(TITLES.values()),'prop':'pageimages',
        'piprop':'thumbnail|original|name','pithumbsize':128,'pilicense':'any'},timeout=60)
    r.raise_for_status(); data=r.json()['query']
    (OUT/'metadata.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    pages={p['title']:p for p in data['pages'].values()}
    for redir in data.get('redirects',[]): pages[redir['from']]=pages.get(redir['to'],{})
    results=[]
    for idx,title in TITLES.items():
        page=pages.get(title,{})
        record={'slot':idx,'title':title,'file':page.get('pageimage'),
                'article':'https://en.wikipedia.org/wiki/'+title.replace(' ','_')}
        url=page.get('thumbnail',{}).get('source')
        if url:
            try:
                url=url.split('?')[0]
                rr=session.get(url,timeout=40); rr.raise_for_status()
                suffix=url.rsplit('.',1)[-1].lower()
                path=OUT/f'{idx}.{suffix}'; path.write_bytes(rr.content)
                with Image.open(path) as im: im.verify()
                record.update(source_url=url,path=str(path.relative_to(ROOT)).replace('\\','/'),status='unreviewed')
            except Exception as exc: record.update(status='failed',error=str(exc)[:160])
        else: record['status']='no_image'
        results.append(record); print(idx,record['file'],record['status'],flush=True)
    (OUT/'sources.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
