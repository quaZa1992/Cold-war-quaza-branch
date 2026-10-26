# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Collect real documentary portrait references and their Wikimedia provenance.

References stay outside the runtime mod. Downloading never marks a photo as
visually approved and never installs or changes a political definition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import threading
import urllib.parse
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

UA = 'MDColdWarHistoricalPortraitResearch/1.0 (https://github.com/Imperia-MD/mdcoldwar)'
RATE_LOCK = threading.Lock()
NEXT_REQUEST = {}


def get(url, params=None, binary=False):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            host = urllib.parse.urlsplit(url).netloc
            with RATE_LOCK:
                pause = NEXT_REQUEST.get(host, 0) - time.monotonic()
                if pause > 0:
                    time.sleep(pause)
                NEXT_REQUEST[host] = time.monotonic() + (2.0 if binary else 1.5)
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as response:
                data = response.read()
            return data if binary else json.loads(data)
        except Exception as exc:
            if attempt == 4:
                raise
            if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
                delay = max(30, min(60, int(exc.headers.get('Retry-After', '30'))))
                print('Public source rate limit; waiting', delay, 'seconds', flush=True)
                with RATE_LOCK:
                    NEXT_REQUEST[host] = max(NEXT_REQUEST.get(host, 0), time.monotonic() + delay)
                time.sleep(delay)
            else:
                time.sleep(2 + attempt * 3)


def dump(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    temporary.replace(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalog-dir', type=Path, required=True)
    ap.add_argument('--catalogue', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--download', action='store_true')
    args = ap.parse_args()
    from prepare_catalog import existing_portraits, normalized, ROOT
    native_portraits = existing_portraits()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    people = {}
    files = ['americas_oceania.json', 'european_asian_majors.json', 'africa.json', 'asia_middleeast_ssr.json']
    inputs = [args.catalogue] if args.catalogue else [args.catalog_dir / name for name in files]
    for path in inputs:
        if not path.exists():
            continue
        for country in json.loads(path.read_text(encoding='utf-8-sig'))['countries']:
            for row in country.get('leaders', []):
                title = row.get('wikipedia_title')
                if not title:
                    title = row['name']
                local = row.get('portrait')
                matches = native_portraits[normalized(row['name'])]
                if not local and len(matches) == 1:
                    local = next(iter(matches))
                people.setdefault(title, []).append({'tag': country['tag'], 'id': row['id'], 'name': row['name'], 'local_portrait': local})
    pages_file = out / 'wikipedia_pages.json'
    pages = json.loads(pages_file.read_text(encoding='utf-8')) if pages_file.exists() else {}
    missing = sorted(set(people) - set(pages))
    for offset in range(0, len(missing), 35):
        batch = missing[offset:offset + 35]
        payload = get('https://en.wikipedia.org/w/api.php', {
            'action': 'query', 'format': 'json', 'redirects': 1, 'titles': '|'.join(batch),
            'prop': 'pageimages|pageprops', 'piprop': 'thumbnail|name',
            'pithumbsize': 250, 'pilicense': 'free'})['query']
        actual = {p['title']: p for p in payload['pages'].values()}
        aliases = {p['from']: p['to'] for k in ('normalized', 'redirects') for p in payload.get(k, [])}
        for title in batch:
            key = title
            for _ in range(5):
                if key not in aliases:
                    break
                key = aliases[key]
            pages[title] = actual.get(key, {'title': title, 'missing': True})
        dump(pages_file, pages)
        print('Page metadata', min(offset + 35, len(missing)), '/', len(missing), flush=True)
        time.sleep(1.2)
    # PageImages returns the original URL when it is smaller than the requested
    # preview. Wikimedia now directs automated clients to standard thumb sizes.
    # Ask the API for a smaller supported size instead of retrying originals.
    for width in (250, 120, 60):
        originals = [t for t in people if pages.get(t, {}).get('thumbnail', {}).get('source') and '/thumb/' not in pages[t]['thumbnail']['source'] and not all(u['local_portrait'] for u in people[t])]
        for offset in range(0, len(originals), 30):
            batch = originals[offset:offset + 30]
            payload = get('https://en.wikipedia.org/w/api.php', {'action': 'query', 'format': 'json',
                'redirects': 1, 'titles': '|'.join(batch), 'prop': 'pageimages',
                'piprop': 'thumbnail|name', 'pithumbsize': width, 'pilicense': 'free'})['query']
            actual = {p['title']: p for p in payload['pages'].values()}
            for title in batch:
                resolved = pages[title].get('title', title)
                candidate = actual.get(resolved, {}).get('thumbnail', {})
                if '/thumb/' in candidate.get('source', ''):
                    pages[title]['thumbnail'] = candidate
            dump(pages_file, pages)
    entity_file = out / 'wikidata_entities.json'
    entities = json.loads(entity_file.read_text(encoding='utf-8')) if entity_file.exists() else {}
    ids = sorted({p.get('pageprops', {}).get('wikibase_item') for p in pages.values()} - {None} - set(entities))
    for offset in range(0, len(ids), 40):
        payload = get('https://www.wikidata.org/w/api.php', {'action': 'wbgetentities', 'format': 'json',
            'ids': '|'.join(ids[offset:offset + 40]), 'props': 'labels|descriptions|claims', 'languages': 'en'})
        entities.update(payload['entities'])
        dump(entity_file, entities)
        print('Entity metadata', min(offset + 40, len(ids)), '/', len(ids), flush=True)
        time.sleep(1.2)
    records = {}
    for title, uses in people.items():
        page = pages.get(title, {})
        qid = page.get('pageprops', {}).get('wikibase_item')
        entity = entities.get(qid, {})
        def times(prop):
            return [x['mainsnak']['datavalue']['value'] for x in entity.get('claims', {}).get(prop, []) if 'datavalue' in x.get('mainsnak', {})]
        image = page.get('thumbnail', {}).get('source', '').split('?')[0]
        filename = page.get('pageimage', '')
        # A biography can use a locally hosted fair-use image while Wikidata
        # links a separately licensed Commons photograph of the same person.
        if not filename:
            images = [x['mainsnak']['datavalue']['value'] for x in entity.get('claims', {}).get('P18', []) if 'datavalue' in x.get('mainsnak', {})]
            if images:
                filename = images[0]
        reject = bool(re.search(r'(?i)(signature|grave|tomb|statue|monument|flag|map\.|coat.of.arms|logo)', filename))
        records[title] = {'article': 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(page.get('title', title).replace(' ', '_')),
            'resolved_title': page.get('title', title), 'qid': qid,
            'description': entity.get('descriptions', {}).get('en', {}).get('value', ''),
            'birth': times('P569'), 'death': times('P570'), 'filename': filename,
            'source_url': image, 'uses': uses,
            'status': 'metadata_only' if filename and not reject else 'image_missing_or_unsuitable'}
        if all(u['local_portrait'] and (ROOT / u['local_portrait']).is_file() for u in uses):
            records[title]['status'] = 'local_portrait_reused'
    files_meta = out / 'commons_files.json'
    commons = json.loads(files_meta.read_text(encoding='utf-8')) if files_meta.exists() else {}
    names = sorted({r['filename'] for r in records.values() if r['filename']} - set(commons))
    for offset in range(0, len(names), 30):
        batch = names[offset:offset + 30]
        payload = get('https://commons.wikimedia.org/w/api.php', {'action': 'query', 'format': 'json',
            'titles': '|'.join('File:' + name for name in batch), 'prop': 'imageinfo',
            'iiprop': 'url|extmetadata', 'iiurlwidth': 250})['query']
        for p in payload['pages'].values():
            commons[p['title'].removeprefix('File:')] = p
        dump(files_meta, commons)
        time.sleep(1.2)
    for title, r in records.items():
        info = commons.get(r['filename'], {}).get('imageinfo', [{}])[0]
        if not r['source_url'] and info.get('thumburl'):
            r['source_url'] = info['thumburl']
        if r['status'] == 'metadata_only' and not r['source_url']:
            r['status'] = 'image_missing_or_unsuitable'
        r['commons_description_url'] = info.get('descriptionurl')
        r['license'] = {k: info.get('extmetadata', {}).get(k, {}).get('value') for k in ['LicenseShortName', 'LicenseUrl', 'Artist', 'Credit', 'AttributionRequired']}
    target = out / 'portrait_references.json'
    dump(target, records)
    if args.download:
        photos = out / 'references'
        photos.mkdir(exist_ok=True)
        def fetch(title):
            r = records[title]
            if r['status'] in {'image_missing_or_unsuitable', 'local_portrait_reused'}:
                return title, r
            key = hashlib.sha256(r['source_url'].encode()).hexdigest()[:20]
            destination = photos / (key + '.' + r['source_url'].rsplit('.', 1)[-1].lower())
            try:
                if not destination.exists():
                    destination.write_bytes(get(r['source_url'], binary=True))
                from PIL import Image
                with Image.open(destination) as image:
                    image.verify()
                r.update(reference=str(destination), sha256=hashlib.sha256(destination.read_bytes()).hexdigest(), status='downloaded_unreviewed')
            except Exception as exc:
                r.update(status='download_failed', error=str(exc))
            return title, r
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(fetch, title) for title in records]
            for i, future in enumerate(as_completed(futures), 1):
                title, record = future.result()
                records[title] = record
                if i % 20 == 0:
                    dump(target, records)
                    print('Documentary references', i, '/', len(records), flush=True)
        dump(target, records)
    from collections import Counter
    print(json.dumps(dict(Counter(x['status'] for x in records.values()))), flush=True)


if __name__ == '__main__':
    main()
