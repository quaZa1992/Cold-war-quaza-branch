# IMPERIA CW — Cold War: egypt 1970 — download portraits.
"""Fetch documentary photo references; no AI processing is performed here."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tools/egypt_1970/reference_photos'
PEOPLE = {
    'nasser': 'Gamal Abdel Nasser', 'sadat': 'Anwar Sadat',
    'zakaria_mohieddin': 'Zakaria Mohieddin', 'serageddin': 'Fouad Serageddin',
    'ibrahim_shukri': 'Ibrahim Shukri', 'fuad_mursi': 'Fuad Mursi',
    'henri_curiel': 'Henri Curiel', 'hussein_shafei': 'Hussein el-Shafei',
    'ali_sabri': 'Ali Sabri', 'hudaybi': 'Hassan al-Hudaybi',
    'naguib': 'Muhammad Naguib', 'osman': 'Osman Ahmed Osman',
    'hegazy': 'Abdel Aziz Hegazy', 'rushdi_said': 'Rushdi Said',
    'khaled_mohieddin': 'Khaled Mohieddin', 'ahmed_hussein': 'Ahmed Hussein',
    'kamal_hussein': 'Kamal el-Din Hussein', 'fawzi': 'Mohamed Fawzi',
    'fuad_ii': 'Fuad II', 'sadek': 'Mohammed Ahmed Sadek',
    'shazly': 'Saad el-Shazly', 'gamasy': 'Abdel Ghani el-Gamasy',
    'fahmy': 'Mahmoud Abdel Rahman Fahmy', 'zikri': 'Fouad Mohamed Abou Zikry',
    'baghdady': 'Ali Mustafa Baghdady', 'air_defence_fahmy': 'Mohammed Ali Fahmi',
    'mubarak': 'Hosni Mubarak', 'ahmad_ismail': 'Ahmad Ismail Ali',
    'afifi': 'Abd al-Razzaq Afifi', 'cyril_vi': 'Pope Cyril VI of Alexandria',
}

def fetch(item):
    key, title = item
    s = requests.Session()
    s.headers['User-Agent'] = 'MdcoldwarHistoricalPortraitResearch/1.0'
    page = PAGES.get(title, {})
    record = {'key': key, 'title': page.get('title', title),
              'article': 'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')}
    image = page.get('thumbnail', {}).get('source') or page.get('original', {}).get('source')
    if not image:
        record['status'] = 'no_page_image'
        return record
    image = image.split('?')[0]
    record['source_url'] = image
    record['image_file'] = page.get('pageimage')
    r = s.get(image, timeout=60)
    r.raise_for_status()
    suffix = image.split('?')[0].rsplit('.', 1)[-1].lower()
    dst = OUT / (key + '.' + suffix)
    dst.write_bytes(r.content)
    record['local_path'] = str(dst.relative_to(ROOT)).replace('\\', '/')
    record['status'] = 'downloaded_reference_unreviewed'
    return record

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers['User-Agent'] = 'MdcoldwarHistoricalPortraitResearch/1.0'
    response = session.get('https://en.wikipedia.org/w/api.php', params={
        'action': 'query', 'format': 'json', 'redirects': 1,
        'titles': '|'.join(PEOPLE.values()), 'prop': 'pageimages',
        'piprop': 'thumbnail|name|original', 'pithumbsize': 400, 'pilicense': 'any'}, timeout=60)
    response.raise_for_status()
    payload = response.json()['query']
    PAGES = {p['title']: p for p in payload['pages'].values()}
    for redirect in payload.get('redirects', []):
        PAGES[redirect['from']] = PAGES.get(redirect['to'], {})
    (OUT / 'page_metadata.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    records = []
    with ThreadPoolExecutor(max_workers=1) as pool:
        jobs = {key: pool.submit(fetch, (key, title)) for key, title in PEOPLE.items()}
        for key, job in jobs.items():
            try:
                record = job.result()
            except Exception as exc:
                record = {'key': key, 'status': 'download_failed', 'error': str(exc)}
            records.append(record)
            print(key, record['status'], flush=True)
    (OUT / 'sources.json').write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
