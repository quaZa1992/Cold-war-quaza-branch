# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Record visually reviewed built-in image edits and compile native DDS assets.

This script does not generate or restyle images. It only compiles the individually
reviewed image_gen outputs, preserving source and generation provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

from prepare_catalog import ROOT

PROMPT = 'Kolorisiere das Bild und mache es wie ein Handyfoto.'


def record(jobs, key, generated, note):
    jobs = Path(jobs)
    rows = json.loads(jobs.read_text(encoding='utf-8'))
    matches = [r for r in rows if r['key'] == key]
    assert len(matches) == 1, key
    job = matches[0]
    reference = Path(job['source'])
    assert reference.is_file(), reference
    actual_reference_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    if job.get('source_sha256'):
        assert job['source_sha256'] == actual_reference_hash, ('Reference changed', key)
    job['source_sha256'] = actual_reference_hash
    source = Path(generated)
    assert source.is_file(), source
    out = jobs.parent / 'dds' / (key + '.dds')
    out.parent.mkdir(exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image).convert('RGBA')
        image = ImageOps.fit(image, (156, 210), Image.Resampling.LANCZOS, centering=(0.5, 0.35))
        image.save(out, format='DDS')
    with Image.open(out) as image:
        assert image.size == (156, 210)
    record = {**job, 'status': 'edited_visually_reviewed', 'tool': 'built-in image_gen',
        'user_prompt': PROMPT, 'generated': str(source), 'generated_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'staged_dds': str(out), 'dds_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
        'review_note': note}
    target = jobs.parent / 'results' / (key + '.json')
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(target)
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs', required=True, type=Path)
    ap.add_argument('--key', required=True)
    ap.add_argument('--generated', required=True, type=Path)
    ap.add_argument('--review-note', required=True)
    args = ap.parse_args()
    result = record(args.jobs, args.key, args.generated, args.review_note)
    print(json.dumps({'key': result['key'], 'status': result['status'], 'dds': result['staged_dds']}))


if __name__ == '__main__':
    main()
