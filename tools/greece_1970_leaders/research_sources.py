# IMPERIA COLD WAR — Greek political portrait source inventory.
"""Download named reference photographs and retain their source metadata."""
from pathlib import Path
import json
import requests
from urllib.parse import urlsplit, unquote

HERE = Path(__file__).resolve().parent
PEOPLE = {
    'rallis': 'Georgios Rallis',
    'averoff': 'Evangelos Averoff',
    'mitsotakis': 'Konstantinos Mitsotakis',
    'evert': 'Miltiadis Evert',
    'farakos': 'Grigoris Farakos',
    'kyrkos': 'Leonidas Kyrkos',
    'drakopoulos': 'Charalampos Drakopoulos',
    'markezinis': 'Spyros Markezinis',
    'androutsopoulos': 'Adamantios Androutsopoulos',
    'pattakos': 'Stylianos Pattakos',
    'tzannetakis': 'Tzannis Tzannetakis',
    'zolotas': 'Xenophon Zolotas',
    'tsatsos': 'Konstantinos Tsatsos',
    'sartzetakis': 'Christos Sartzetakis',
    'stephanopoulos': 'Konstantinos Stephanopoulos',
    'damanaki': 'Maria Damanaki',
    'konstantopoulos': 'Nikos Konstantopoulos',
    'simitis': 'Costas Simitis',
    'papariga': 'Aleka Papariga',
    'kostas_karamanlis': 'Kostas Karamanlis',
}

EXTRA_SOURCES = {
    'kyrkos': ('https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Leonidas_KYRKOS_%281%29.jpg/960px-Leonidas_KYRKOS_%281%29.jpg',
               'https://commons.wikimedia.org/wiki/File:Leonidas_KYRKOS_(1).jpg', 'European Union - EP', 'European Parliament legal notice'),
    'evert': ('https://www.huffingtonpost.gr/wp-content/uploads/2015/11/5d867d102300005700d2fe29.jpg',
              'https://www.huffingtonpost.gr/idisis/nd-apo-ton-konstantino-mitsotaki-ston-miltiadi-evert-1993-1997/', 'unknown', 'unknown'),
    'damanaki': ('https://www.kathimerini.gr/resources/2019-12/1991_06_28.jpg',
                 'https://www.kathimerini.gr/k/100yk/1056455/to-kke-apochorei-apo-ton-synaspismo/', 'unknown', 'unknown'),
}


def main():
    session = requests.Session()
    session.headers['User-Agent'] = 'ImperiaColdWarHistoricalPortraitResearch/1.0 (local historical mod research)'
    out = HERE / 'sources'
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    page_response = session.get('https://en.wikipedia.org/w/api.php', params={
        'action': 'query', 'titles': '|'.join(PEOPLE.values()), 'prop': 'pageimages',
        'piprop': 'original', 'pilicense': 'any', 'format': 'json', 'redirects': 1}, timeout=45)
    page_response.raise_for_status()
    pages = {p['title']: p for p in page_response.json()['query']['pages'].values()}
    greek = {'evert': 'Μιλτιάδης Έβερτ', 'farakos': 'Γρηγόρης Φαράκος',
             'drakopoulos': 'Μπάμπης Δρακόπουλος', 'tzannetakis': 'Τζαννής Τζαννετάκης'}
    greek_response = session.get('https://el.wikipedia.org/w/api.php', params={
        'action': 'query', 'titles': '|'.join(greek.values()), 'prop': 'pageimages',
        'piprop': 'original', 'pilicense': 'any', 'format': 'json', 'redirects': 1}, timeout=45)
    greek_response.raise_for_status()
    gp = greek_response.json()['query']['pages'].values()
    by_greek_title = {p['title']: p for p in gp}
    for key, title in greek.items():
        if title in by_greek_title:
            pages[PEOPLE[key]] = by_greek_title[title]
    files = ['File:' + unquote(urlsplit(p['original']['source']).path.split('/')[-1])
             for p in pages.values() if 'original' in p]
    metadata_response = session.get('https://commons.wikimedia.org/w/api.php', params={
        'action': 'query', 'titles': '|'.join(files), 'prop': 'imageinfo',
        'iiprop': 'url|extmetadata', 'format': 'json'}, timeout=45)
    metadata_response.raise_for_status()
    metadata_pages = metadata_response.json()['query']['pages']
    infos = {p['title'].replace('_', ' '): p.get('imageinfo', [{}])[0]
             for p in metadata_pages.values()}
    for key, title in PEOPLE.items():
        cached = out / (key + '.json')
        row = {'project': 'IMPERIA COLD WAR', 'key': key, 'name': title,
               'source_author': 'unknown', 'licence': 'unknown'}
        try:
            page = pages.get(title, {})
            url = page.get('original', {}).get('source')
            row['discovery_page'] = 'https://en.wikipedia.org/wiki/' + title.replace(' ', '_')
            if not url:
                row['status'] = 'no_page_image'
            else:
                filename = unquote(urlsplit(url).path.split('/')[-1])
                info = infos.get(('File:' + filename).replace('_', ' '), {})
                row['commons_metadata'] = info
                ext = info.get('extmetadata', {})
                row.update(source_url=url, source_page=info.get('descriptionurl', row['discovery_page']),
                           source_author=ext.get('Artist', {}).get('value', 'unknown'),
                           licence=ext.get('LicenseShortName', {}).get('value', 'unknown'),
                           licence_url=ext.get('LicenseUrl', {}).get('value', 'unknown'))
                clean_url = urlsplit(url)._replace(query='').geturl()
                destination = out / (key + Path(filename).suffix.lower())
                image = session.get(clean_url, timeout=45) if not destination.exists() else None
                if image is not None:
                    image.raise_for_status()
                    destination.write_bytes(image.content)
                row.update(local_source=destination.relative_to(HERE).as_posix(), status='downloaded')
        except Exception as exc:
            row.update(status='failed', error=str(exc))
        cached.write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        rows.append(row)
        print(key, row['status'], row.get('local_source', ''), flush=True)
    for key, (url, page, author, licence) in EXTRA_SOURCES.items():
        destination = out / (key + '_selected.jpg')
        if not destination.exists():
            try:
                response = session.get(url, timeout=45)
                response.raise_for_status()
                destination.write_bytes(response.content)
            except requests.RequestException as exc:
                print('alternate', key, str(exc), flush=True)
                continue
        row = {'project': 'IMPERIA COLD WAR', 'key': key, 'name': PEOPLE[key],
               'source_url': url, 'source_page': page, 'source_author': author,
               'licence': licence, 'local_source': destination.relative_to(HERE).as_posix(),
               'status': 'downloaded', 'note': 'Selected alternate photograph; earlier discovery photo retained separately.'}
        (out / (key + '_selected.json')).write_text(json.dumps(row, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        rows = [row if r['key'] == key else r for r in rows]
    pdf = out / 'hellenic_parliament.pdf'
    if not pdf.exists():
        response = session.get('https://www.hellenicparliament.gr/UserFiles/8c3e9046-78fb-48f4-bd82-bbba28ca1ef5/vouli_en_low_28_1_09.pdf', timeout=45)
        response.raise_for_status()
        pdf.write_bytes(response.content)
    (HERE / 'source_inventory.json').write_text(json.dumps({
        'project': 'IMPERIA COLD WAR', 'portraits': rows}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
