# IMPERIA COLD WAR — Historical event-photo source acquisition and attribution.
"""Download explicitly selected Commons photographs and preserve source metadata."""
import json
import sys
import time
import urllib.request
from pathlib import Path
from research import BASE, AGENT, request

def main():
    path=BASE/'sources.json'
    data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'project':'IMPERIA COLD WAR','photos':{}}
    for argument in sys.argv[1:]:
        key,title=argument.split('=',1)
        if key in data['photos'] and (BASE/data['photos'][key]['original']).is_file():
            print(key,'already downloaded',flush=True)
            continue
        title=title if title.startswith('File:') else 'File:'+title
        result=request(dict(action='query',titles=title,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=330,format='json'))
        page=next(iter(result['query']['pages'].values()))
        info=page['imageinfo'][0]
        url=info.get('thumburl',info['url']).split('?')[0]
        suffix=Path(url).suffix.lower()
        target=BASE/'originals'/(key+suffix)
        target.parent.mkdir(exist_ok=True)
        downloaded=False
        for attempt in range(2):
            try:
                with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':AGENT}),timeout=60) as response:
                    target.write_bytes(response.read())
                downloaded=True
                break
            except urllib.error.HTTPError as error:
                if error.code != 429: raise
                time.sleep(5*(attempt+1))
        if not downloaded:
            print(key,'download throttled, skipped',flush=True)
            continue
        data['photos'][key]={'commons_title':page['title'],'source_page':info['descriptionurl'],'download_url':url,'original':target.relative_to(BASE).as_posix(),'metadata':info.get('extmetadata',{})}
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(key,str(target),flush=True)
        time.sleep(2)

if __name__=='__main__': main()
