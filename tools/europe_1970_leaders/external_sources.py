# IMPERIA COLD WAR — Research rare German party representatives in dated archives.
from pathlib import Path
from urllib.parse import urljoin
import json,requests,time
from html.parser import HTMLParser
class Images(HTMLParser):
    def __init__(self):super().__init__();self.rows=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img':self.rows.append(dict(attrs))
HERE=Path(__file__).resolve().parent
PAGES={
 'frey':'https://www.deutsche-biographie.de/dbo047515.html',
 'frey_museum':'https://www.nsdoku.de/lexikon/artikel/frey-gerhard-240',
 'schlierer':'https://www.leo-bw.de/en/detail/-/Detail/details/DOKUMENT/lmz_bilddatenbank/LMZ002311/MdL%20Dr%20Rolf%20Schlierer%20REP%201996',
 'bachmann':'https://www.unsere-zeit.de/der-erste-vorsitzende-47892/',
 'stehr':'https://www.kommunisten.de/rubriken/kultur/9435-erinnerungen-des-kommunisten-heinz-stehr',
}
DIRECT={
 'antje_vollmer':('https://germanhistorydocs.org/media/volume-9/image-5054/90427_ca_object_representations_media_2738_frontend.jpg','https://germanhistorydocs.org/de/zwei-deutsche-staaten-1961-1989/feminat-weiblicher-fraktionsvorsitz-der-gruenen-im-bundestag-1984'),
 'martin_mussgnug':('https://antifainfoblatt.de/sites/default/files/styles/responsive_2_1_600w/public/2025-11/martin-mu%C3%9Fgnug-npd.jpg?h=77ce5aad&itok=KUnBiywV','https://antifainfoblatt.de/aib38/tuttlingen-martin-mussgnug-gestorben'),
 'schlierer_1998_pdf':('https://archiv.preussische-allgemeine.de/1998/1998_09_12_37.pdf','https://archiv.preussische-allgemeine.de/1998/1998_09_12_37.pdf'),
 'stehr_recollections_pdf':('https://www.spurensuche-kreis-pinneberg.de/wp-content/uploads/2025/01/Heinz_Stehr_Erinnerungen_KPD-Verbot_Pinneberg_50er_Restauration_und_Antikommunismus.pdf','https://www.spurensuche-kreis-pinneberg.de/wp-content/uploads/2025/01/Heinz_Stehr_Erinnerungen_KPD-Verbot_Pinneberg_50er_Restauration_und_Antikommunismus.pdf'),
}
def main():
    session=requests.Session();session.headers['User-Agent']='ImperiaColdWarPortraitResearch/1.0 (https://github.com/Imperia-MD/mdcoldwar)'
    record={'project':'IMPERIA COLD WAR','pages':{},'downloads':{}}
    for key,url in PAGES.items():
        try:
            r=session.get(url,timeout=45);r.raise_for_status();(HERE/'references'/(key+'_page.html')).write_text(r.text,encoding='utf8')
            parser=Images();parser.feed(r.text);images=[dict(url=urljoin(url,i.get('src','')),alt=i.get('alt',''),srcset=i.get('srcset','')) for i in parser.rows]
            record['pages'][key]=dict(url=url,images=images);print(key,json.dumps(images,ensure_ascii=False)[:5000],flush=True)
        except Exception as e:print(key,str(e)[:180],flush=True)
        time.sleep(.7)
    for key,(url,page) in DIRECT.items():
        try:
            r=session.get(url,timeout=60);r.raise_for_status();suffix='.pdf' if key.endswith('_pdf') else '.jpg';dest=HERE/'references'/(key+'_external'+suffix);dest.write_bytes(r.content)
            record['downloads'][key]=dict(url=url,page=page,file=dest.relative_to(HERE).as_posix(),author='unknown',licence='unknown')
            print(key,'downloaded',len(r.content),flush=True)
        except Exception as e:print(key,str(e)[:180],flush=True)
    (HERE/'external_sources.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if __name__=='__main__':main()
