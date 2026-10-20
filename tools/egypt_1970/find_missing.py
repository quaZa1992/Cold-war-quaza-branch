import json
import requests
from download_portraits import OUT
s=requests.Session()
s.headers['User-Agent']='MdcoldwarHistoricalPortraitResearch/1.0'
titles={'fawzi':('en','Mohamed Fawzi (general)'),
 'fuad_mursi':('ar','فؤاد مرسي'),'rushdi_said':('ar','رشدي سعيد'),
 'hegazy':('ar','عبد العزيز حجازي'),'fuad_ii':('ar','فؤاد الثاني'),
 'air_defence_fahmy':('en','Mohammed Aly Fahmy')}
records={}
for key,(lang,title) in titles.items():
    r=s.get(f'https://{lang}.wikipedia.org/w/api.php',params={
        'action':'parse','format':'json','page':title,'prop':'images'},timeout=40)
    try:
        data=r.json()['parse']
        records[key]=data
        print(key,data.get('images',[])[:18],flush=True)
    except Exception: print(key,r.status_code,r.text[:100],flush=True)
(OUT/'missing_image_names.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
