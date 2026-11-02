# IMPERIA COLD WAR — USA and Soviet portrait source preparation.
"""Prepare explicit reuse and photograph records; never generate guessed faces."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import shutil
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageOps, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from catalogue import PEOPLE
USER_AGENT = 'ImperiaColdWarPortraitResearchBot/1.0 (https://github.com/Imperia-MD/mdcoldwar) requests/2'

REUSE = {
 'USA_bernie_sanders': 'gfx/leaders/USA/Bernie_Sanders.dds',
 'USA_richard_nixon': 'gfx/leaders/USA/USA_Coldwar_Nixon.dds',
 'USA_gerald_ford': 'gfx/leaders/mdcw_historical_pool/USA_gerald_ford.dds',
 'USA_ronald_reagan': 'gfx/leaders/USA/ronald.dds',
 'USA_george_mcgovern': 'gfx/leaders/mdcw_historical_pool/USA_george_mcgovern.dds',
 'USA_jimmy_carter': 'gfx/leaders/mdcw_historical_pool/USA_jimmy_carter.dds',
 'USA_walter_mondale': 'gfx/leaders/mdcw_historical_pool/USA_walter_mondale.dds',
 'USA_bill_clinton': 'gfx/leaders/USA/bill_clinton.dds',
 'USA_pat_buchanan': 'gfx/leaders/USA/Pat_Buchanan.dds',
 'USA_colin_powell': 'gfx/leaders/USA/Colin_Powell.dds',
 'USA_al_gore': 'gfx/leaders/USA/al_gore.dds',
 'USA_harry_browne': 'gfx/leaders/USA/harry_browne.dds',
 'SOV_leonid_brezhnev': 'gfx/leaders/SOV/SOV_Coldwar_Brezhnev.dds',
 'SOV_nikolai_ryzhkov': 'gfx/leaders/mdcw_historical_pool/SOV_nikolai_ryzhkov.dds',
 'SOV_yuri_andropov': 'gfx/leaders/mdcw_historical_pool/SOV_yuri_andropov.dds',
 'SOV_heydar_aliyev': 'gfx/leaders/AZE/AZE_Coldwar_Heydar_Aliyev.dds',
 'SOV_dmitry_ustinov': 'gfx/leaders/mdcw_historical_pool/SOV_dmitry_ustinov.dds',
 'SOV_konstantin_chernenko': 'gfx/leaders/coldwar/chernenko.dds',
 'SOV_mikhail_gorbachev': 'gfx/leaders/SOV/mikhail_gorbachev.dds',
 'SOV_pyotr_shelest': 'gfx/leaders/UKR/UKR_Coldwar_Petro_Shelest.dds',
 'SOV_boris_yeltsin': 'gfx/leaders/mdcw_historical_pool/SOV_boris_yeltsin.dds',
 'SOV_grigory_yavlinsky': 'gfx/leaders/SOV/Grigory_Yavlinsky.dds',
 'SOV_boris_nemtsov': 'gfx/leaders/SOV/nemtsov.dds',
 'SOV_vladimir_zhirinovsky': 'gfx/leaders/SOV/Vladimir_Zhirinovsky.dds',
 'SOV_gennady_zyuganov': 'gfx/leaders/SOV/Gennady_Zyuganov.dds',
 'SOV_maria_vladimirovna': 'gfx/leaders/SOV/maria_vladimirovna.dds',
 'SOV_yury_luzhkov': 'gfx/leaders/SOV/luzhkov.dds',
 'SOV_vladimir_putin': 'gfx/leaders/SOV/Vladimir_Putin.dds',
}
RU_TITLES = {
 'SOV_pyotr_siuda': 'Сиуда, Пётр Петрович',
 'SOV_sergei_trapeznikov': 'Трапезников, Сергей Павлович',
 'SOV_grigory_galazy': 'Галазий, Григорий Иванович',
 'SOV_vladimir_poremsky': 'Поремский, Владимир Дмитриевич',
 'SOV_leonid_smirnov': 'Смирнов, Леонид Васильевич',
 'SOV_nikolai_shmelyov': 'Шмелёв, Николай Петрович',
    'SOV_dzhermen_gvishiani': 'Гвишиани, Джермен Михайлович',
    'SOV_gavriil_popov': 'Попов, Гавриил Харитонович',
    'SOV_mikhail_zimyanin': 'Зимянин, Михаил Васильевич',
}


def query(session, language, titles, prop='pageimages', **extra):
    pages, redirects = {}, {}
    for start in range(0, len(titles), 45):
        args = dict(action='query', titles='|'.join(titles[start:start + 45]),
                    prop=prop, format='json', redirects=1, **extra)
        r = session.get('https://' + language + '.wikipedia.org/w/api.php', params=args, timeout=45)
        r.raise_for_status()
        data = r.json()['query']
        for row in data.get('normalized', []) + data.get('redirects', []):
            redirects[row['from']] = row['to']
        pages.update({p['title']: p for p in data['pages'].values()})
    def page(title):
        for _ in range(5):
            if title in redirects:
                title = redirects[title]
        return pages.get(title, {})
    return page


def download(row):
    if row.get('status') == 'reused':
        return row
    url = row.get('source_url')
    if not url:
        row['status'] = 'missing_identified_photograph'
        return row
    suffix = Path(unquote(urlsplit(url).path)).suffix.lower()
    if suffix not in ('.jpg', '.jpeg', '.png', '.webp'):
        row['status'] = 'unsupported_source_format'
        return row
    target = HERE / 'references' / (row['id'] + suffix)
    try:
        if not target.exists():
            r = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=45)
            r.raise_for_status()
            target.write_bytes(r.content)
        with Image.open(target) as im:
            row['source_dimensions'] = list(im.size)
        row.update(reference=target.relative_to(HERE).as_posix(), status='reference_ready')
    except Exception as exc:
        row.update(status='download_failed', error=str(exc))
    return row


def main():
    (HERE / 'references').mkdir(exist_ok=True)
    known = json.loads((ROOT / 'tools/historical_politics_1970/portrait_sources.json').read_text(encoding='utf-8'))['assets']
    old = json.loads((HERE / 'sources.json').read_text(encoding='utf-8'))['portraits'] if (HERE / 'sources.json').exists() else []
    old = {r['id']: r for r in old}
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    needed = [p for p in PEOPLE if p['tag'] + '_' + p['key'] not in REUSE]
    en = query(session, 'en', [p['wikipedia_title'] for p in needed], piprop='original', pilicense='any')
    ru = query(session, 'ru', list(RU_TITLES.values()), piprop='original', pilicense='any')
    rows = []
    for p in PEOPLE:
        key = p['tag'] + '_' + p['key']
        row = {'project': 'IMPERIA COLD WAR', 'id': key, 'name': p['name'],
               'source_author': 'unknown', 'licence': 'unknown'}
        if key in REUSE:
            assert (ROOT / REUSE[key]).is_file(), key
            row.update(status='reused', portrait=REUSE[key], source='Existing correct-person mod portrait',
                       provenance=known.get(key, {'author': 'original MD contributors, individual artist unknown', 'licence': 'unknown'}))
        elif key in known and Path(known[key].get('source', '')).is_file():
            meta = known[key]
            path = Path(meta['source'])
            target = HERE / 'references' / (key + path.suffix.lower())
            if not target.exists():
                shutil.copy2(path, target)
            row.update(status='reference_ready', reference=target.relative_to(HERE).as_posix(),
                       source_url=meta.get('source_url'), source_page=meta.get('article'), provenance=meta)
        else:
            page = ru(RU_TITLES[key]) if key in RU_TITLES else en(p['wikipedia_title'])
            url = page.get('original', {}).get('source')
            row.update(source_page=('https://ru.wikipedia.org/wiki/' + RU_TITLES[key].replace(' ', '_')) if key in RU_TITLES
                       else p['source_urls'][0])
            if url:
                url = urlsplit(url)._replace(query='').geturl()
                # Wikimedia's standard 960px thumbnail avoids oversized originals.
                if '/wikipedia/commons/' in url and '/thumb/' not in url:
                    tail = url.split('/wikipedia/commons/', 1)[1]
                    url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/' + tail + '/960px-' + tail.rsplit('/', 1)[1]
                row['source_url'] = url
            if key in old and old[key].get('status') == 'reference_ready':
                row = old[key]
        rows.append(row)
    # One metadata query per batch of Commons files, rather than one API call per person.
    names = []
    for row in rows:
        url = row.get('source_url', '') or ''
        if '/commons/' in url:
            tail = urlsplit(url).path.split('/commons/', 1)[1]
            filename = tail.split('/')[-2] if tail.startswith('thumb/') else tail.split('/')[-1]
            row['commons_file'] = 'File:' + unquote(filename)
            names.append(row['commons_file'])
    meta_pages = {}
    for start in range(0, len(names), 45):
        r = session.get('https://commons.wikimedia.org/w/api.php', params=dict(action='query',
            titles='|'.join(names[start:start + 45]), prop='imageinfo', iiprop='url|extmetadata', format='json'), timeout=45)
        r.raise_for_status()
        for page in r.json()['query']['pages'].values():
            meta_pages[page['title'].replace('_', ' ')] = page.get('imageinfo', [{}])[0]
    for row in rows:
        info = meta_pages.get(row.get('commons_file', '').replace('_', ' '), {})
        ext = info.get('extmetadata', {})
        if ext:
            row.update(source_author=ext.get('Artist', {}).get('value', 'unknown'),
                licence=ext.get('LicenseShortName', {}).get('value', 'unknown'),
                licence_url=ext.get('LicenseUrl', {}).get('value', 'unknown'),
                photograph_date=ext.get('DateTimeOriginal', {}).get('value', 'unknown'), commons_metadata=info,
                source_page=info.get('descriptionurl', row.get('source_page')))
        if info.get('url') and row.get('status') not in ('reused', 'reference_ready'):
            row['source_url'] = urlsplit(info['url'])._replace(query='').geturl()
    ready, pending = [], []
    for row in rows:
        (ready if row.get('status') in ('reused', 'reference_ready') else pending).append(row)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(download, row) for row in pending]):
            ready.append(future.result())
    ready.sort(key=lambda r: r['id'])
    (HERE / 'sources.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'portraits': ready}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for row in ready:
        print(row['id'], row['status'], row.get('reference', ''))
    for tag in ('USA', 'SOV'):
        items = [r for r in ready if r['id'].startswith(tag + '_')]
        sheet = Image.new('RGB', (1200, ((len(items) + 7) // 8) * 185), '#20272b')
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 11)
        for i, row in enumerate(items):
            x, y = (i % 8) * 150, (i // 8) * 185
            path = ROOT / row['portrait'] if row.get('status') == 'reused' else HERE / row.get('reference', 'absent')
            if path.is_file():
                sheet.paste(ImageOps.fit(Image.open(path).convert('RGB'), (112, 150)), (x + 19, y + 2))
            draw.text((x + 75, y + 166), row['id'].split('_', 1)[1][:23], font=font, fill='white', anchor='mm')
        sheet.save(HERE / (tag + '_SOURCE_REVIEW.png'))


if __name__ == '__main__':
    main()
