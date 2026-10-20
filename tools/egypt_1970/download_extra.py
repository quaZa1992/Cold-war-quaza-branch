"""Resolve missing Arabic references and retain successful earlier downloads."""
import json
from pathlib import Path
import requests
from download_portraits import ROOT, OUT, PEOPLE

AR = {'fuad_mursi':'فؤاد مرسي','hegazy':'عبد العزيز حجازي','rushdi_said':'رشدي سعيد',
      'fawzi':'محمد فوزي (عسكري)','air_defence_fahmy':'محمد علي فهمي',
      'baghdady':'علي مصطفى بغدادي','afifi':'عبد الرزاق عفيفي',
      'fuad_ii':'فؤاد الثاني','hudaybi':'حسن الهضيبي'}
s=requests.Session()
s.headers['User-Agent']='MdcoldwarHistoricalPortraitResearch/1.0'
records={x['key']:x for x in json.loads((OUT/'sources.json').read_text(encoding='utf-8'))}
payload=s.get('https://ar.wikipedia.org/w/api.php',params={'action':'query','format':'json',
    'redirects':1,'titles':'|'.join(AR.values()),'prop':'pageimages',
    'piprop':'thumbnail|original|name','pithumbsize':600,'pilicense':'any'},timeout=60).json()['query']
(OUT/'arabic_metadata.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding='utf-8')
pages={p['title']:p for p in payload['pages'].values()}
for redir in payload.get('redirects',[]): pages[redir['from']]=pages.get(redir['to'],{})
en={p['title']:p for p in json.loads((OUT/'page_metadata.json').read_text())['pages'].values()}
for key,title in PEOPLE.items():
    existing=next(iter(OUT.glob(key+'.*')),None)
    if existing and key not in AR:
        records[key]['local_path']=str(existing.relative_to(ROOT)).replace('\\','/')
        records[key]['status']='downloaded_reference_unreviewed'
        print(key,'existing',flush=True)
        continue
    page=pages.get(AR.get(key,''),{}) or en.get(title,{})
    candidates=[v['source'].split('?')[0] for k,v in page.items() if k in ('thumbnail','original')]
    for url in candidates:
        try:
            r=s.get(url,timeout=45)
            r.raise_for_status()
            dst=OUT/(key+'.'+url.rsplit('.',1)[-1].lower())
            dst.write_bytes(r.content)
            records[key]={'key':key,'title':title,'article':'https://ar.wikipedia.org/wiki/'+AR[key] if key in AR else 'https://en.wikipedia.org/wiki/'+title.replace(' ','_'),
                'source_url':url,'image_file':page.get('pageimage'),
                'local_path':str(dst.relative_to(ROOT)).replace('\\','/'),
                'status':'downloaded_reference_unreviewed'}
            print(key,'downloaded',flush=True)
            break
        except Exception as exc: print(key,str(exc)[:100],flush=True)
    if existing and not records[key].get('local_path'):
        records[key]['local_path']=str(existing.relative_to(ROOT)).replace('\\','/')
        records[key]['status']='downloaded_reference_unreviewed'
(OUT/'sources.json').write_text(json.dumps(list(records.values()),indent=2,ensure_ascii=False),encoding='utf-8')
