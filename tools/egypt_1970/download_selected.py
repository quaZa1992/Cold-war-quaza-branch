# IMPERIA CW — Cold War: egypt 1970 — download selected.
import json
import requests
from download_portraits import ROOT, OUT
s=requests.Session(); s.headers['User-Agent']='MdcoldwarHistoricalPortraitResearch/1.0'
urls={
 'rushdi_said':('https://twas.org/sites/default/files/cropped_said_rushdi.jpg','https://twas.org/directory/said-rushdi'),
 'hudaybi':('https://www.ikhwan.wiki/images/5/5f/المستشار_الهضيبى.jpg','https://www.ikhwan.wiki/index.php?title=ملف:المستشار_الهضيبى.jpg'),
}
files={'hegazy':'Abdel Aziz Hegazy.jpg','zakaria_mohieddin':'Zakaria Mohiedin as Interior Minister.jpg'}
r=s.get('https://commons.wikimedia.org/w/api.php',params={'action':'query','format':'json',
    'titles':'|'.join('File:'+v for v in files.values()),'prop':'imageinfo',
    'iiprop':'url|extmetadata','iiurlwidth':500},timeout=45)
for page in r.json().get('query',{}).get('pages',{}).values():
    key=next((k for k,v in files.items() if 'File:'+v==page['title']),None)
    if key and 'imageinfo' in page:
        info=page['imageinfo'][0]
        urls[key]=(info.get('thumburl',info['url']),info['descriptionurl'])
records={x['key']:x for x in json.loads((OUT/'sources.json').read_text(encoding='utf-8'))}
for key,(url,article) in urls.items():
    try:
        r=s.get(url,timeout=45); r.raise_for_status()
        dst=OUT/(key+'.jpg'); dst.write_bytes(r.content)
        records[key]={'key':key,'source_url':url,'article':article,
            'local_path':str(dst.relative_to(ROOT)).replace('\\','/'),
            'status':'downloaded_reference_unreviewed'}
        print(key,'downloaded',flush=True)
    except Exception as exc: print(key,str(exc)[:150],flush=True)
(OUT/'sources.json').write_text(json.dumps(list(records.values()),indent=2,ensure_ascii=False),encoding='utf-8')
