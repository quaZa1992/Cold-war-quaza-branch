# IMPERIA COLD WAR — Verified external portrait references and technical crop preparation.
from pathlib import Path
import json,sys,requests
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from europe_1970_leaders.prepare import USER_AGENT,query
EXTERNAL={
 'AZE_heydar_aliyev':dict(reference='references/aliyev_1972_preview.jpg',date='1972-12-22, Kremlin Palace of Congresses, Moscow',source_url='https://fs.netfilm.store/fs/fs219598b.jpg',source_page='https://www.net-film.ru/en/photo-129598/',source_author='Valentin Sobolev and Vladimir Musaelyan, TASS / Net-Film, photo 129598',licence='In copyright; separate redistribution permission unknown'),
 'heinz_stehr':dict(reference='references/heinz_stehr_book.jpg',date='1994 meeting with Fidel Castro, also recalled as 1996 in the later memoir; exact year uncertain within the 1990s',source_url='https://www.kommunisten.de/images/stories/2026/Literatur-Kultur/Buch_Stehr-Der-rote-Faden_Cover.jpg',source_page='https://www.kommunisten.de/rubriken/kultur/9435-erinnerungen-des-kommunisten-heinz-stehr',source_author='Cover photograph from Heinz Stehr, Der rote Faden; original photographer unknown',licence='unknown'),
 'gunter_deckert':dict(reference='references/gunter_deckert_external.jpg',date='Published July/August 1993, Journal of Historical Review 13(4); exact photograph date unknown',source_url='https://codoh.com/media/files/jhr-13-4-weber4.jpg',source_page='https://codoh.com/library/document/political-leader-punished-german-sentenced-for/',source_author='Original photographer unknown; portrait reproduced in the cited 1993 issue. Used only for person identification and restoration, with no text or political claims adopted.',licence='unknown'),
 'udo_voigt':dict(reference='references/udo_voigt_congress_1998.jpg',date='NPD congress, Passau, 1998; source caption identifies Udo Voigt as the second man from the left',source_url='https://antifainfoblatt.de/sites/default/files/styles/responsive_3_2_600w/public/NPD-Kongress-Passau-1998.jpg?h=ab5f34af&itok=ie90nyxH',source_page='https://antifainfoblatt.de/aib43/npd-kongress-passau-die-nsdap-vor-augen',source_author='Antifaschistisches Infoblatt photo archive; original photographer unknown',licence='unknown'),
 'antje_vollmer':dict(reference='references/antje_vollmer_external.jpg',date='1984-04-04',source_url='https://germanhistorydocs.org/media/volume-9/image-5054/90427_ca_object_representations_media_2738_frontend.jpg',source_page='https://germanhistorydocs.org/de/zwei-deutsche-staaten-1961-1989/feminat-weiblicher-fraktionsvorsitz-der-gruenen-im-bundestag-1984',source_author='Egon Steiner, picture-alliance/dpa',licence='In copyright; separate redistribution permission unknown'),
 'martin_mussgnug':dict(reference='references/martin_mussgnug_external.jpg',date='Before the source publication of 1997-07-19',source_url='https://antifainfoblatt.de/sites/default/files/styles/responsive_2_1_600w/public/2025-11/martin-mu%C3%9Fgnug-npd.jpg?h=77ce5aad&itok=KUnBiywV',source_page='https://antifainfoblatt.de/aib38/tuttlingen-martin-mussgnug-gestorben',source_author='NPD publicity photograph reproduced by Antifaschistisches Infoblatt; photographer unknown',licence='unknown'),
 'gerhard_frey':dict(reference='references/gerhard_frey_external.jpg',date='1976-11-07',source_url='https://www.deutsche-biographie.de/downloadImage?image=/images/e/e1/Gerhard-frey-1976-klein.jpg',source_page='https://www.deutsche-biographie.de/dbo047515.html',source_author='Klaus Rose, Imago Images',licence='In copyright; separate redistribution permission unknown'),
 'kurt_bachmann':dict(reference='references/kurt_bachmann_external.jpg',date='During the overlap of DKP chairman Bachmann and honorary chairman Reimann, 1968-1973; exact date unknown',source_url='https://www.unsere-zeit.de/wp-content/uploads/2019/10/der-erste-vorsitzende.jpg',source_page='https://www.unsere-zeit.de/der-erste-vorsitzende-47892/',source_author='UZ-Archiv; photographer unknown',licence='unknown'),
 'rolf_schlierer':dict(reference='references/schlierer_1998_page6.jpg',date='Published 1998-09-12; exact photograph date unknown',source_url='https://archiv.preussische-allgemeine.de/1998/1998_09_12_37.pdf',source_page='https://archiv.preussische-allgemeine.de/1998/1998_09_12_37.pdf',source_author='Ostpreussenblatt archive, 12 September 1998, page 6; photographer unknown',licence='unknown'),
}
def main():
    path=HERE/'sources.json';rows=json.loads(path.read_text(encoding='utf8'))['portraits'];by={r['id']:r for r in rows}
    session=requests.Session();session.headers['User-Agent']=USER_AGENT
    for key,record in EXTERNAL.items():
        target=HERE/record['reference']
        if not target.exists():r=session.get(record['source_url'],timeout=45);r.raise_for_status();target.write_bytes(r.content)
        by[key].update(record,status='reference_ready',generation_input='inputs/'+key+'.jpg',period_choice='Verified external period source',commons_metadata={})
        by[key].pop('native_reference',None)
        by[key].pop('commons_file',None)
        by[key].pop('error',None)
        by[key]['licence_url']=record.get('licence_url','unknown')
    titles={'TAJ_jabbor_rasulov':('ru','Расулов, Джаббар Расулович'),'TRK_muhammetnazar_gapurov':('ru','Гапуров, Мухамедназар')}
    for key,(lang,title) in titles.items():
        if by[key].get('native_reference') or by[key].get('period_choice')=='Verified existing portrait; original photographic date unknown':continue
        p=query(session,lang,[title],piprop='original',pilicense='any')(title);url=p.get('original',{}).get('source')
        if not url:continue
        target=HERE/'references'/(key+'_language.jpg')
        if not target.exists():r=session.get(url,timeout=45);r.raise_for_status();target.write_bytes(r.content)
        by[key].update(reference=target.relative_to(HERE).as_posix(),source_url=url,source_page='https://'+lang+'.wikipedia.org/wiki/'+title.replace(' ','_'),source_author='unknown',licence='unknown',status='reference_ready',generation_input='inputs/'+key+'.jpg',date='Unknown; pending period verification')
    crops=json.loads((HERE/'input_crops.json').read_text(encoding='utf8'))['crops']
    for row in rows:
        if not row.get('reference'):continue
        if row['id'] not in EXTERNAL and row['id'] not in crops and row['id'] not in titles:continue
        reference=(ROOT if row.get('native_reference') else HERE)/row['reference']
        im=ImageOps.exif_transpose(Image.open(reference)).convert('RGB')
        if row['id'] in crops:im=im.crop(tuple(round(v*im.size[i%2]) for i,v in enumerate(crops[row['id']])))
        im.thumbnail((1600,1600));dest=HERE/'inputs'/(row['id']+'.jpg');im.save(dest,quality=95)
        row['generation_input']=dest.relative_to(HERE).as_posix()
    path.write_text(json.dumps(dict(project='IMPERIA COLD WAR',portraits=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Registered external historical sources',len(EXTERNAL))
if __name__=='__main__':main()
