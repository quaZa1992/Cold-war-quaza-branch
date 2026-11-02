# IMPERIA COLD WAR — Complete the Green and socialist opposition portrait records.
import json
import requests
from prepare import HERE, USER_AGENT, query, download

path=HERE/'sources.json'; data=json.loads(path.read_text(encoding='utf-8')); rows=data['portraits']
if not any(r['id']=='USA_bernie_sanders' for r in rows):
    rows.append(dict(project='IMPERIA COLD WAR', id='USA_bernie_sanders', name='Bernie Sanders',status='reused',
        portrait='gfx/leaders/USA/Bernie_Sanders.dds',source='Existing identified MD portrait',source_author='Original MD contributors; individual artist unknown',licence='unknown'))
if not any(r['id']=='USA_ralph_nader' for r in rows):
    session=requests.Session(); session.headers['User-Agent']=USER_AGENT
    page=query(session,'en',['Ralph Nader'],piprop='original',pilicense='any')('Ralph Nader')
    url=page['original']['source']; filename=url.rsplit('/',1)[1]
    result=session.get('https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',redirects=1,prop='imageinfo',iiprop='url|extmetadata',titles='File:'+requests.utils.unquote(filename)),timeout=45)
    result.raise_for_status(); info=next((p['imageinfo'][0] for p in result.json()['query']['pages'].values() if p.get('imageinfo')),{}); ext=info.get('extmetadata',{})
    row=dict(project='IMPERIA COLD WAR',id='USA_ralph_nader',name='Ralph Nader',source_url=info.get('url',url),source_page=info.get('descriptionurl','https://en.wikipedia.org/wiki/Ralph_Nader'),source_author=ext.get('Artist',{}).get('value','unknown'),licence=ext.get('LicenseShortName',{}).get('value','unknown'),commons_metadata=info)
    download(row); rows.append(row); print(row['status'])
data['portraits']=sorted(rows,key=lambda r:r['id']); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
