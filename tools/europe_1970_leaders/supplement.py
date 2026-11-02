# IMPERIA COLD WAR — Resolve ambiguous identities and missing period photographs.
from pathlib import Path
import sys,json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.period_sources import get,clean
from europe_1970_leaders.prepare import USER_AGENT
import requests
NAMES=['Antje Vollmer','Edmund Stoiber','Joschka Fischer','Jutta Ditfurth','Günter Deckert','Gerhard Frey politician','SOV Maria Vladimirovna','Rolf Schlierer','Udo Voigt','Heinz Stehr','Kurt Bachmann','Martin Mußgnug','Boris Nemtsov','Ernst Goldenbaum','Wolfgang Mischnick']
def main():
    session=requests.Session();session.headers['User-Agent']=USER_AGENT
    path=HERE/'supplement_candidates.json';result=json.loads(path.read_text(encoding='utf8')) if path.exists() else {'project':'IMPERIA COLD WAR','people':{}}
    for name in NAMES:
        if result['people'].get(name):continue
        query='"'+name.replace('SOV ','').replace(' politician','')+'"'
        data=get(session,'https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',generator='search',gsrsearch=query,gsrnamespace=6,gsrlimit=50,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1000)).json()
        rows=[]
        for page in data.get('query',{}).get('pages',{}).values():
            info=page.get('imageinfo',[{}])[0];ext=info.get('extmetadata',{})
            date=clean(ext.get('DateTimeOriginal',{}).get('value','unknown'));desc=clean(ext.get('ImageDescription',{}).get('value','unknown'))
            fy=re.search(r'19[5-9]\d',page['title']);dy=re.search(r'(?:19|20)\d\d',date)
            year=int(fy[0]) if fy else int(dy[0]) if dy else None
            if year and year>1999:continue
            if not info.get('url','').lower().split('?')[0].endswith(('.jpg','.jpeg','.png')):continue
            rows.append(dict(title=page['title'],date=date,year=year,description=desc,info=info))
        result['people'][name]=rows;print(name,[(r['title'],r['year']) for r in rows[:12]],flush=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':main()
