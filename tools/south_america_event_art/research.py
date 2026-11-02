# IMPERIA COLD WAR — Historical South American event-photo research.
"""Record Wikimedia Commons metadata for candidate historical photographs."""
from __future__ import annotations
import concurrent.futures
import json
import urllib.parse
import urllib.request
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
AGENT = 'ImperiaColdWarAssetResearch/1.0 (historical game event art)'
QUERIES = {
    'chl_election': 'Allende 1970 filetype:bitmap',
    'chl_copper': 'Chuquicamata 1971 filetype:bitmap',
    'chl_transport': 'Chile camioneros 1972 filetype:bitmap',
    'chl_junta': 'Junta Chile 1973 filetype:bitmap',
    'chl_repression': 'Chile estadio nacional 1973 filetype:bitmap',
    'chl_finance': 'Santiago bolsa 1982 filetype:bitmap',
    'chl_plebiscite': 'Chile plebiscito 1988 filetype:bitmap',
    'chl_handover': 'Aylwin 1990 traspaso filetype:bitmap',
    'chl_truth': 'Rettig 1991 filetype:bitmap',
    'bra_officers': 'Medici posse 1969 filetype:bitmap',
    'bra_party': 'Figueiredo anistia 1979 filetype:bitmap',
    'bra_oil': 'Petrobras refinaria 1970 filetype:bitmap',
    'bra_debt': 'Delfim Netto 1973 filetype:bitmap',
    'bra_rights': 'Carter Geisel 1978 filetype:bitmap',
    'bra_split': 'Brizola 1980 filetype:bitmap',
    'bra_inflation': 'Brasil supermercado 1986 filetype:bitmap',
    'bra_agreement': 'Geisel 1975 nuclear filetype:bitmap',
    'arg_commanders': 'Ongania junta 1970 filetype:bitmap',
    'arg_opening': 'Peron Balbin 1972 filetype:bitmap',
    'arg_peron': 'Peron 1973 filetype:bitmap',
    'arg_labor': 'Cordobazo 1969 filetype:bitmap',
    'arg_accountability': 'Madres Plaza Mayo 1982 filetype:bitmap',
    'arg_economy': 'Martinez Hoz 1976 filetype:bitmap',
    'arg_industry': 'Somisa 1970 filetype:bitmap',
    'arg_grain': 'Argentina silos 1970 filetype:bitmap',
    'arg_beagle': 'Samore 1978 filetype:bitmap',
    'arg_navy': 'ARA Veinticinco Mayo 1979 filetype:bitmap',
    'arg_islands': 'Port Stanley 1982 filetype:bitmap',
    'arg_aviation': 'Argentina Mirage 1982 filetype:bitmap',
}

def request(params):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': AGENT}), timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 4: raise
            time.sleep(3 * (attempt+1))

def search(item):
    key, query = item
    data = request(dict(action='query', generator='search', gsrsearch=query, gsrnamespace=6,
                        gsrlimit=6, prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=1400, format='json'))
    records = []
    for page in sorted(data.get('query', {}).get('pages', {}).values(), key=lambda p:p.get('index',0)):
        info = page.get('imageinfo',[{}])[0]
        records.append({'title':page['title'], 'imageinfo':info})
    return key, records

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    records = {}
    if (BASE/'research.json').exists(): records=json.loads((BASE/'research.json').read_text(encoding='utf-8'))['candidates']
    for item in QUERIES.items():
        if item[0] in records: continue
        key, rows = search(item)
        records[key] = rows
        print(key, json.dumps([{'title':r['title'], 'license':r['imageinfo'].get('extmetadata',{}).get('LicenseShortName',{}).get('value')} for r in rows],ensure_ascii=True),flush=True)
        (BASE/'research.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','queries':QUERIES,'candidates':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        time.sleep(0.8)

if __name__ == '__main__': main()
