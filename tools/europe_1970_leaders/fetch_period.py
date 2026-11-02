# IMPERIA COLD WAR — Fetch and record period-specific portrait reference choices.
from pathlib import Path
import sys,json,re,time,requests,unicodedata
from urllib.parse import urlsplit,unquote
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.prepare import USER_AGENT,targets
from europe_1970_leaders.period_sources import YEARS,clean,get

EXACT={
 'edmund_stoiber':'File:Bundesarchiv B 145 Bild-F061788-0036, Hamburg, CDU-Bundesparteitag, Stoiber.jpg',
 'franz_schoenhuber':'File:Bundesarchiv B 145 Bild-F081850-0029, Europawahl, Wahlplakat "Die Republikaner".jpg',
 'joschka_fischer':'File:28. Internationales Management Symposium 1998-Joschka Fischer, deutscher Bundesminister des Auswärtigen Amtes-HSGH 022-000755-02.jpg',
 'jutta_ditfurth':'File:BDK Grüne Duisburg Mrz 1989 Jutta Ditfurth.jpg',
 'rudolf_scharping':'File:Freiburg im Breisgau- SPD-Kanzlerkandidat Rudolf Scharping auf dem Rathausplatz (mit Gernot Erler) - LABW - Staatsarchiv Freiburg W 140 Nr. 12380.jpeg',
 'wolfgang_mischnick':'File:Bundesarchiv B 145 Bild-F049586-0026, Frankfurt, FDP-Bundesparteitag, Mischnick.jpg',
 'johannes_rau':'File:Bundesarchiv B 145 Bild-F062774-0033, München, SPD-Parteitag, Johannes Rau.jpg',
 'oskar_lafontaine':'File:Bundesarchiv B 145 Bild-F079276-0010 Lafontaine (cropped).jpg',
 'bjorn_engholm':'File:Bundesarchiv B 145 Bild-F080691-0010, Björn Engholm (cropped).jpg',
 'lothar_de_maiziere':'File:Bundesarchiv Bild 183-1990-1202-014, Berlin, Bundestagswahl, Lothar de Maiziere.jpg',
 'petra_kelly':'File:Petra Kelly, 1987 (cropped).jpg',
 'markus_meckel':'File:Bundesarchiv Bild 183-1990-0119-314, Markus Meckel.jpg',
 'stephan_hilsberg':'File:Bundesarchiv Bild 183-1990-0215-304, Stephan Hilsberg.jpg',
 'herbert_mies':'File:Bundesarchiv Bild 183-1986-0226-325, Bonn, Besuch Volkskammer-Delegation, Sindermann (cropped).jpg',
 'louis_ferdinand':'File:Prinz Louis Ferdinand von Preußen, Patenschaftstreffen Schleswig-Holstein und Pommern in der Ostseehalle (Kiel 43.695) (cropped).jpg',
 'gregor_gysi':'File:Bundesarchiv Bild 183-1990-1202-011, Berlin, Bundestagswahl, Gregor Gysi (cropped).jpg',
 'lothar_bisky':'File:Bundesarchiv Bild 183-1990-0705-333, Dr. Lothar Bisky.jpg',
 'SOV_vladimir_putin':'File:Putin in Government House 1999 (cropped).jpg',
 'angela_merkel':'File:Angela Merkel (1990).jpg',
}
def fold(x):return ''.join(c for c in unicodedata.normalize('NFKD',x.lower().replace('ß','ss')) if not unicodedata.combining(c))
def main():
    rows=json.loads((HERE/'sources.json').read_text(encoding='utf8'))['portraits'];known={r['id']:r for r in rows}
    for row in targets():
        if row['id'] not in known:rows.append(row)
    session=requests.Session();session.headers['User-Agent']=USER_AGENT
    cache=json.loads((HERE/'period_candidates.json').read_text(encoding='utf8'))['people']
    choices={}
    for row in rows:
        key=row['id'];candidates=cache.get(key,[])
        if row.get('period_choice')=='Verified external period source' or row.get('native_reference'):continue
        if key in EXACT:choices[key]=EXACT[key];continue
        if candidates and (key in YEARS or not row.get('source_url')):
            surname=fold(row['name'].split()[-1])
            filtered=[r for r in candidates if surname in fold(r['title'])]
            if filtered:choices[key]=filtered[0]['title']
    metadata={}
    names=list(dict.fromkeys(choices.values()+[])) if False else list(dict.fromkeys(choices.values()))
    for i in range(0,len(names),35):
        result=get(session,'https://commons.wikimedia.org/w/api.php',params=dict(action='query',format='json',redirects=1,titles='|'.join(names[i:i+35]),prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1000)).json()
        for page in result.get('query',{}).get('pages',{}).values():metadata[page['title'].replace('_',' ')]=page.get('imageinfo',[{}])[0]
    for row in rows:
        key=row['id'];selected=choices.get(key)
        if selected:
            info=metadata.get(selected.replace('_',' '),{});ext=info.get('extmetadata',{})
            if not info.get('url'):print('missing selected file',key,selected,flush=True);continue
            prior=row.copy();row.update(commons_file=selected,commons_metadata=info,source_url=info['url'],source_page=info.get('descriptionurl','unknown'),source_author=ext.get('Artist',{}).get('value','unknown'),licence=ext.get('LicenseShortName',{}).get('value','unknown'),licence_url=ext.get('LicenseUrl',{}).get('value','unknown'),date=clean(ext.get('DateTimeOriginal',{}).get('value','unknown')))
            if prior.get('source_url')!=row['source_url']:
                row['superseded_source']=prior.get('source_url');row['status']='period_reference_pending'
        if row.get('status')=='reference_ready':continue
        info=row.get('commons_metadata',{});url=info.get('thumburl') or row.get('source_url')
        if not url:continue
        try:
            time.sleep(1.2)
            response=session.get(url,timeout=45);response.raise_for_status()
            suffix=Path(unquote(urlsplit(url).path)).suffix.lower()
            target=HERE/'references'/(key+'_period'+suffix);target.write_bytes(response.content)
            im=ImageOps.exif_transpose(Image.open(target)).convert('RGB');row['dimensions']=list(im.size)
            preview=HERE/'inputs'/(key+'.jpg');im.thumbnail((1600,1600));im.save(preview,quality=95)
            row.update(status='reference_ready',reference=target.relative_to(HERE).as_posix(),generation_input=preview.relative_to(HERE).as_posix())
            if selected:row['period_choice']=selected
            print(key,'ready',flush=True)
        except Exception as e:row.update(status='download_failed',error=str(e));print(key,str(e)[:110],flush=True)
        (HERE/'sources.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (HERE/'sources.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    items=[r for r in rows if r.get('generation_input')]
    sheet=Image.new('RGB',(1280,((len(items)+7)//8)*230),'#20272b');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',11)
    for i,r in enumerate(items):
        x,y=i%8*160,i//8*230;sheet.paste(ImageOps.fit(Image.open(HERE/r['generation_input']),(148,200),centering=(.5,.1)),(x,y));draw.text((x+74,y+215),r['id'][:24],font=font,fill='white',anchor='mm')
    sheet.save(HERE/'PERIOD_SOURCE_REVIEW.png')
if __name__=='__main__':main()
