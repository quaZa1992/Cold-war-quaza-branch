# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Inventory original capture dates; upload dates never count as photo dates.

This preliminary report does not approve portraits. It separates dated sources,
clearly later sources and undated sources for explicit historical review.
"""
import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


def plain(value):
    return html.unescape(re.sub('<[^>]+>', ' ', value or '')).strip()


def normalized(value):
    return unquote(value).replace('_', ' ').casefold()


def audit(jobs_path, cache_path):
    cache = json.loads(cache_path.read_text(encoding='utf-8'))
    rows = []
    for job in json.loads(jobs_path.read_text(encoding='utf-8')):
        url_path = unquote(urlsplit(job.get('source_url', '')).path)
        parts = [normalized(x) for x in url_path.split('/') if x]
        matches = [(k, v) for k, v in cache.items() if normalized(k) in parts]
        if not matches:
            rows.append({**job, 'era_status': 'capture_date_unknown', 'capture_date_raw': None})
            continue
        assert len(matches) == 1, (job['key'], [k for k, _ in matches])
        title, page = matches[0]
        info = page.get('imageinfo', [{}])[0]
        meta = info.get('extmetadata', {})
        raw = meta.get('DateTimeOriginal', {}).get('value', '')
        clean = plain(raw)
        # Omit hidden Wikibase encoding and use only the human capture-date text.
        clean = re.split(r'date QS:', clean)[0].strip()
        years = sorted({int(y) for y in re.findall(r'(?<!\d)((?:18|19|20)\d{2})(?!\d)', clean)})
        status = 'capture_date_unknown'
        if re.search(r'upload|hochgeladen|date of publication|publication date', clean, re.I):
            status = 'upload_or_publication_date_not_capture_date'
        elif years:
            if min(years) > 2000:
                status = 'post_2000_source'
            elif max(years) < 1970:
                status = 'pre_1970_source_needs_role_review'
            elif min(years) >= 1970 and max(years) <= 2000:
                status = 'dated_1970_2000_needs_role_review'
            else:
                status = 'ambiguous_date_range'
        rows.append({**job, 'era_status': status, 'commons_title': title,
            'capture_date_raw': raw, 'capture_date': clean, 'capture_years': years,
            'evidence_url': info.get('descriptionurl'),
            'description': plain(meta.get('ImageDescription', {}).get('value', '')),
            'source_credit': plain(meta.get('Credit', {}).get('value', '')),
            'categories': plain(meta.get('Categories', {}).get('value', '')),
            'upload_date_ignored': meta.get('DateTime', {}).get('value')})
    return {'policy': 'Capture dates only. This inventory is not final historical approval.',
            'counts': dict(Counter(r['era_status'] for r in rows)), 'portraits': rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs', required=True, type=Path)
    ap.add_argument('--commons-cache', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    result = audit(args.jobs, args.commons_cache)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
