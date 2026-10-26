# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Prepare native-size portrait candidates and contact sheets for visual review.

Only --install-reviewed promotes portraits listed in visual_review.json. Existing
MD portraits remain untouched. Documentary masters and previews stay outside mod.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from prepare_catalog import ROOT, normalized


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--research', type=Path, required=True)
    ap.add_argument('--catalogue', type=Path, required=True)
    ap.add_argument('--install-reviewed', action='store_true')
    args = ap.parse_args()
    out = args.research / 'portrait_previews'
    out.mkdir(exist_ok=True)
    references = json.loads((args.research / 'photo_research/portrait_references.json').read_text(encoding='utf-8'))
    catalogue = json.loads(args.catalogue.read_text(encoding='utf-8'))
    review_path = out / 'visual_review.json'
    review = json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
    by_title = {normalized(title.replace('_', ' ')): ref for title, ref in references.items()}
    rows = []
    manifest = {}
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 12)
    for c in catalogue['countries']:
        for person in c.get('leaders', []):
            key = c['tag'] + '_' + person['id']
            portrait = person.get('portrait')
            if portrait and (ROOT / portrait).is_file():
                manifest[key] = {'portrait': portrait, 'provenance': 'existing exact-name MD reference'}
                continue
            title = person.get('wikipedia_title') or person['name']
            ref = references.get(title) or by_title.get(normalized(title.replace('_', ' '))) or {}
            local = {u.get('local_portrait') for u in ref.get('uses', []) if u.get('tag') == c['tag'] and u.get('id') == person['id'] and u.get('local_portrait')}
            if len(local) == 1:
                portrait = next(iter(local))
                if (ROOT / portrait).is_file():
                    manifest[key] = {'portrait': portrait, 'provenance': 'existing exact-name MD reference'}
                    continue
            source = ref.get('reference')
            if not source or not Path(source).is_file():
                rows.append({'key': key, 'name': person['name'], 'title': title, 'status': 'missing_reference'})
                continue
            with Image.open(source) as im:
                im = ImageOps.exif_transpose(im).convert('RGB')
                centering = tuple(review.get(key, {}).get('centering', [0.5, 0.2]))
                preview = ImageOps.fit(im, (156, 210), Image.Resampling.LANCZOS, centering=centering).convert('RGBA')
            digest = hashlib.sha256(preview.tobytes()).hexdigest()
            staged = out / 'dds' / (key + '.dds')
            staged.parent.mkdir(exist_ok=True)
            preview.save(staged, format='DDS')
            relative = 'gfx/leaders/mdcw_historical_pool/' + key + '.dds'
            record = {'key': key, 'name': person['name'], 'title': title, 'status': 'requires_visual_review',
                'portrait': relative, 'staged': str(staged), 'source': source, 'source_url': ref.get('source_url'),
                'article': ref.get('article'), 'license': ref.get('license'), 'source_sha256': ref.get('sha256'),
                'render_sha256': digest, 'centering': list(centering)}
            approval = review.get(key, {})
            if approval.get('approved') and approval.get('render_sha256') == digest:
                record['status'] = 'visually_reviewed'
                if args.install_reviewed:
                    destination = ROOT / relative
                    destination.parent.mkdir(exist_ok=True)
                    destination.write_bytes(staged.read_bytes())
                manifest[key] = record
            rows.append(record)
    rendered = [r for r in rows if r.get('staged')]
    for offset in range(0, len(rendered), 42):
        batch = rendered[offset:offset + 42]
        sheet = Image.new('RGB', (7 * 164, math.ceil(len(batch) / 7) * 250), (38, 40, 43))
        draw = ImageDraw.Draw(sheet)
        for i, r in enumerate(batch):
            x, y = (i % 7) * 164 + 4, (i // 7) * 250 + 4
            with Image.open(r['staged']) as portrait:
                sheet.paste(portrait.convert('RGB'), (x, y))
            label = r['key'].split('_', 1)[0] + ' ' + r['name']
            words = label.split()
            lines = ['']
            for word in words:
                if len(lines[-1]) + len(word) > 23:
                    lines.append('')
                lines[-1] += (' ' if lines[-1] else '') + word
            draw.text((x, y + 212), '\n'.join(lines[:3]), font=font, fill=(245, 245, 245))
        sheet.save(out / ('sheet_' + str(offset // 42 + 1).zfill(2) + '.png'))
    (out / 'candidates.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
    (out / 'prepared_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    if args.install_reviewed:
        target = ROOT / 'tools/historical_politics_1970/portrait_manifest.json'
        target.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'native_reuse': sum(1 for x in manifest.values() if 'provenance' in x),
        'prepared': len(rendered), 'approved': sum(x['status'] == 'visually_reviewed' for x in rows),
        'missing': sum(x['status'] == 'missing_reference' for x in rows), 'sheets': math.ceil(len(rendered) / 42)}))


if __name__ == '__main__':
    main()
