# IMPERIA CW — Cold War: egypt 1970 — fetch final references.
import json, re
from urllib.parse import urljoin
import requests
from download_portraits import ROOT, OUT
s=requests.Session(); s.headers['User-Agent']='MdcoldwarHistoricalPortraitResearch/1.0'
records={x['key']:x for x in json.loads((OUT/'sources.json').read_text(encoding='utf-8'))}
pages={
 'zakaria_mohieddin':'https://sis.gov.eg/en/egypt/egyptian-figures/zakaria-mohieddin/',
 'hegazy':'https://sis.gov.eg/ar/مصر/المجتمع/أعلام-وشخصيات-مصرية/عبد-العزيز-حجازي/',
 'rushdi_said':'https://twas.org/directory/said-rushdi',
 'hudaybi':'https://www.ikhwan.wiki/index.php?title=ملف:المستشار_الهضيبى.jpg',
}
for key,url in pages.items():
    try:
        r=s.get(url,timeout=45); r.raise_for_status()
        (OUT/(key+'_page.html')).write_text(r.text,encoding='utf-8')
        tags=re.findall(r'<(?:img|meta)\b[^>]+>',r.text,re.I)
        candidates=[]
        for tag in tags:
            if 'og:image' in tag:
                m=re.search(r'content=[\"\']([^\"\']+)',tag)
                if m: candidates.insert(0,urljoin(url,m.group(1)))
            else:
                m=re.search(r'(?:src|data-src)=[\"\']([^\"\']+)',tag)
                if m: candidates.append(urljoin(url,m.group(1)))
        print(key, json.dumps(candidates[:18],ensure_ascii=False),flush=True)
    except Exception as exc: print(key,str(exc)[:200],flush=True)

# Resolve specific military photo files in one Commons metadata call.
files={'fawzi':'General Mohamed Fawzi.jpg','air_defence_fahmy':'Mohamed Ali Fahmi.jpg'}
r=s.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','format':'json',
    'titles':'|'.join('File:'+x for x in files.values()),'prop':'imageinfo',
    'iiprop':'url|extmetadata','iiurlwidth':500},timeout=45)
payload=r.json()
(OUT/'military_imageinfo.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
for page in payload.get('query',{}).get('pages',{}).values():
    key=next((k for k,v in files.items() if page['title']=='File:'+v),None)
    if not key or 'imageinfo' not in page: continue
    info=page['imageinfo'][0]
    urls=[info.get('thumburl'),info.get('url')]
    for url in urls:
        if not url: continue
        try:
            rr=s.get(url,timeout=45); rr.raise_for_status()
            dst=OUT/(key+'.jpg'); dst.write_bytes(rr.content)
            records[key]={'key':key,'source_url':url,'article':info.get('descriptionurl'),
                'image_file':page['title'],'local_path':str(dst.relative_to(ROOT)).replace('\\','/'),
                'status':'downloaded_reference_unreviewed','license':info.get('extmetadata',{})}
            print(key,'downloaded',flush=True); break
        except Exception as exc: print(key,str(exc)[:100],flush=True)
(OUT/'sources.json').write_text(json.dumps(list(records.values()),indent=2,ensure_ascii=False),encoding='utf-8')
