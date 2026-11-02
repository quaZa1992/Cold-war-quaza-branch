# IMPERIA COLD WAR — Period photograph research for German political representatives.
"""Research dated source choices, retaining full Commons metadata and source files."""
from pathlib import Path
import sys,json,re,time,requests
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.prepare import USER_AGENT,targets

YEARS={
 'angela_merkel':1991,'antje_vollmer':1983,'bjorn_engholm':1988,'edmund_stoiber':1993,
 'ernst_goldenbaum':1960,'gerhard_frey':1990,'gerhard_schroder':1990,'gregor_gysi':1990,
 'gunter_deckert':1994,'joachim_gauck':1990,'johannes_rau':1986,'joschka_fischer':1985,
 'jutta_ditfurth':1987,'lothar_bisky':1990,'lothar_de_maiziere':1990,'louis_ferdinand':1968,
 'manfred_stolpe':1990,'markus_meckel':1990,'oskar_lafontaine':1990,'rainer_eppelmann':1990,
 'rudolf_scharping':1994,'theo_waigel':1990,'udo_voigt':1999,'wolf_biermann':1976,
 'wolfgang_schaeuble':1990,'wolfgang_biermann':1970,'werner_lamberz':1971,
 'wolfgang_mischnick':1972,'herbert_mies':1973,
 'SOV_boris_nemtsov':1997,'SOV_gennady_zyuganov':1996,'SOV_grigory_yavlinsky':1997,
 'SOV_maria_vladimirovna':1992,'SOV_vladimir_putin':1999,'SOV_vladimir_zhirinovsky':1993,
 'SOV_yury_luzhkov':1996,
}
def clean(x):return re.sub('<[^>]*>','',str(x))
def get(session,url,**kw):
    time.sleep(.7)
    r=session.get(url,timeout=45,**kw);r.raise_for_status();return r
def main():
    rows=json.loads((HERE/'sources.json').read_text(encoding='utf8'))['portraits'];known={r['id']:r for r in rows}
    for row in targets():
        if row['id'] not in known:rows.append(row)
    session=requests.Session();session.headers['User-Agent']=USER_AGENT
    cache_path=HERE/'period_candidates.json'
    cache=json.loads(cache_path.read_text(encoding='utf8')) if cache_path.exists() else {'project':'IMPERIA COLD WAR','people':{}}
    work=[r for r in rows if r['id'] in YEARS or not r.get('source_url')]
    for row in work:
        key=row['id']
        if key in cache['people']:continue
        year=YEARS.get(key,1970)
        query='"'+row['name']+'" '+str(year)
        if not row.get('source_url'):query='"'+row['name']+'"'
        try:
            params=dict(action='query',format='json',generator='search',gsrsearch=query,gsrnamespace=6,gsrlimit=12,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1000)
            result=get(session,'https://commons.wikimedia.org/w/api.php',params=params).json()
            found=[]
            for page in result.get('query',{}).get('pages',{}).values():
                info=page.get('imageinfo',[{}])[0];ext=info.get('extmetadata',{})
                if not info.get('url','').lower().split('?')[0].endswith(('.jpg','.jpeg','.png','.webp')):continue
                date=clean(ext.get('DateTimeOriginal',{}).get('value','unknown'))
                filename=page['title'];fy=re.search(r'(?:19[5-9]\d)',filename)
                dy=re.search(r'(?:18|19|20)\d\d',date)
                actual=int(fy[0]) if fy else int(dy[0]) if dy else None
                if actual and actual>1999:continue
                score=(30 if fy else 0)+(10 if actual else -50)+(10 if re.search('cropped|portrait|porträt',filename,re.I) else 0)
                if actual:score-=abs(actual-year)/3
                found.append(dict(title=filename,info=info,date=date,year=actual,score=score))
            found.sort(key=lambda r:r['score'],reverse=True)
            cache['people'][key]=found[:6]
            print(key,[(r['title'],r['year']) for r in found[:2]],flush=True)
        except Exception as e:
            print(key,type(e).__name__,str(e)[:120],flush=True);cache['people'][key]=[]
        cache_path.write_text(json.dumps(cache,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Research complete',len(cache['people']),flush=True)
if __name__=='__main__':main()
