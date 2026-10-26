# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Validate and optionally install individually reviewed image_gen portraits.

This copies approved native DDS files only. It never generates or edits images.
Blocked or unfinished jobs retain their original portrait and remain explicit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from collections import Counter
from pathlib import Path

from PIL import Image

from build import HERE, ROOT

ORIGINAL_EXCEPTIONS = {
    'MNC_jean_louis_campora': (
        'Historisches Original von 1999 verwenden.',
        '216cec6fe3e7eb69636a2599601eda3493338870068ddc4897ee6be1e3ff4a0a',
    ),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


SOURCE_METADATA_FIELDS = (
    'source', 'source_url', 'source_page', 'source_sha256', 'reference_page',
    'reference_caption', 'original_license', 'license', 'source_credit',
    'source_rights_status', 'title', 'article', 'capture_date', 'staged',
    'render_sha256',
)


def source_snapshot(record, source_hash=None, replacement=None):
    """Keep displaced source-specific provenance without presenting it as current."""
    snapshot = {key: record[key] for key in SOURCE_METADATA_FIELDS if key in record}
    for key, current_value in (replacement or {}).items():
        if key in snapshot and snapshot[key] == current_value:
            snapshot.pop(key)
    if source_hash and 'source_sha256' not in snapshot:
        snapshot['source_sha256'] = source_hash
    return snapshot


def add_archive(rows, item):
    if not item:
        return
    source_hash = item.get('source_sha256')
    if source_hash:
        for existing in rows:
            if existing.get('source_sha256') == source_hash:
                for key, value in item.items():
                    existing.setdefault(key, value)
                return
    if item not in rows:
        rows.append(item)


def inside(root, relative):
    relative = Path(relative.replace('\\', '/'))
    assert not relative.is_absolute() and '..' not in relative.parts, relative
    result = (root / relative).resolve()
    assert result.is_relative_to(root.resolve()), result
    return result


def prepare(jobs_file, backup, era_review=None, identity_review=None):
    jobs = json.loads(jobs_file.read_text(encoding='utf-8'))
    manifest_path = HERE / 'portrait_manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert len({x['key'] for x in jobs}) == len(jobs), 'Duplicate portrait job'
    backup_rows = json.loads((backup / 'manifest.json').read_text(encoding='utf-8'))
    if isinstance(backup_rows, dict):
        backup_rows = backup_rows.get('files', backup_rows)
    if isinstance(backup_rows, dict):
        backup_rows = [dict(relative_path=k, **v) for k, v in backup_rows.items()]
    backups = {r.get('relative_path', r.get('path', r.get('relative'))).replace('\\', '/'): r for r in backup_rows}
    approved, statuses = [], Counter()
    era = json.loads(era_review.read_text(encoding='utf-8')) if era_review else {}
    era = era.get('portraits', era)
    if isinstance(era, list):
        era = {r['key']: r for r in era}
    identities = json.loads(identity_review.read_text(encoding='utf-8')) if identity_review else {}
    identities = identities.get('portraits', identities)
    if isinstance(identities, list):
        identities = {r['key']: r for r in identities}
    for job in jobs:
        old = manifest.get(job['key'], {})
        manifest[job['key']] = {**old, 'portrait': None,
            'held_portrait': old.get('portrait') or old.get('held_portrait') or job['original_dds'],
            'status': 'pending_individual_era_identity_and_style_review'}
        result_file = jobs_file.parent / 'results' / (job['key'] + '.json')
        if not result_file.is_file():
            statuses['pending'] += 1
            continue
        result = json.loads(result_file.read_text(encoding='utf-8'))
        assert result['key'] == job['key'], result_file
        status = result['status']
        statuses[status] += 1
        if status not in {'edited_visually_reviewed', 'original_historical_user_approved'}:
            assert status in {'blocked_by_image_tool', 'held_visual_review'}, (job['key'], status)
            continue
        historical = era.get(job['key'], {})
        if historical.get('status') != 'historically_reviewed' or historical.get('source_sha256') != digest(Path(job['source'])):
            statuses['era_review_pending'] += 1
            continue
        assert historical.get('evidence_url') and historical.get('role_fit_note'), job['key']
        identity = identities.get(job['key'], {})
        if identity.get('identity_status') != 'caption_verified' or identity.get('source_sha256') != digest(Path(job['source'])):
            statuses['identity_review_pending'] += 1
            continue
        assert identity.get('identity_evidence_url') and identity.get('identity_note'), job['key']
        assert result.get('review_note'), job['key']
        if status == 'original_historical_user_approved':
            assert result.get('tool') == 'native DDS conversion of user-approved original', job['key']
            assert job['key'] in ORIGINAL_EXCEPTIONS, job['key']
            approval, reference_hash = ORIGINAL_EXCEPTIONS[job['key']]
            assert result.get('user_approval') == approval, job['key']
            assert digest(Path(job['source'])) == reference_hash, job['key']
        else:
            assert result['tool'] == 'built-in image_gen', job['key']
            assert digest(Path(result['generated'])) == result['generated_sha256'], job['key']
        assert Path(result['source']).resolve() == Path(job['source']).resolve(), ('Review source changed', job['key'])
        actual_source_hash = digest(Path(job['source']))
        assert not job.get('source_sha256') or job['source_sha256'] == actual_source_hash, ('Job source hash changed', job['key'])
        recorded_hash = result.get('source_sha256') or digest(Path(result['source']))
        assert recorded_hash == actual_source_hash, ('Review refers to another source', job['key'])
        source = Path(result['staged_dds'])
        assert source.resolve() == (jobs_file.parent / 'dds' / (job['key'] + '.dds')).resolve(), source
        assert digest(source) == result['dds_sha256'], source
        with Image.open(source) as image:
            assert image.format == 'DDS' and image.size == (156, 210), source
        assert result['original_dds'] == job['original_dds'], job['key']
        target = inside(ROOT, job['original_dds'])
        if old.get('portrait'):
            assert old['portrait'].replace('\\', '/') == job['original_dds'], job['key']
        if target.exists() and digest(target) != result['dds_sha256']:
            # Every existing asset being overwritten must have an intact backup.
            row = backups.get(job['original_dds'])
            prior_installed = old.get('style_edit', {}).get('dds_sha256')
            if row:
                original = inside(backup, job['original_dds'])
                assert digest(original) == row['sha256'].lower(), original
                assert digest(target) in {row['sha256'].lower(), prior_installed}, ('Unrelated portrait change', target)
            else:
                # Assets created by an earlier approved run did not exist in
                # the original E: backup. Their exact prior hash is known;
                # install() snapshots them before any replacement.
                assert prior_installed and digest(target) == prior_installed, ('Unbacked unrelated asset', target)
        entry = dict(old)
        archived_sources = list(old.get('superseded_sources', []))
        old_source_hash = old.get('source_sha256') or old.get('style_edit', {}).get('era_review', {}).get('source_sha256')
        incoming_archive = job.get('superseded_source_metadata') or result.get('superseded_source_metadata')
        if incoming_archive:
            add_archive(archived_sources, incoming_archive)
        source_changed = bool(old_source_hash and old_source_hash != actual_source_hash) or bool(incoming_archive)
        if old_source_hash and old_source_hash != actual_source_hash:
            replacement_metadata = {
                'source': job.get('source'),
                'source_url': job.get('source_url'),
                'source_page': job.get('source_page'),
                'reference_page': job.get('reference_page') or job.get('source_page'),
                'reference_caption': job.get('reference_caption'),
                'original_license': job.get('original_license'),
                'license': job.get('license', job.get('original_license')),
                'source_credit': job.get('source_credit'),
                'source_rights_status': job.get('source_rights_status'),
                'title': job.get('title'),
                'article': job.get('article'),
                'capture_date': job.get('capture_date'),
                'staged': str(source),
                'render_sha256': result['dds_sha256'],
            }
            add_archive(archived_sources, source_snapshot(old, old_source_hash, replacement_metadata))
        if source_changed:
            # Clear source-specific fields before overlaying current metadata so
            # old captions, rights notes, titles, or links cannot leak forward.
            for field in SOURCE_METADATA_FIELDS:
                entry.pop(field, None)
        current_fields = {
            'source': job.get('source'),
            'source_url': job.get('source_url'),
            'source_page': job.get('source_page'),
            'source_sha256': actual_source_hash,
            'reference_page': job.get('reference_page') or job.get('source_page'),
            'reference_caption': job.get('reference_caption'),
            'original_license': job.get('original_license'),
            'license': job.get('license', job.get('original_license')),
            'source_credit': job.get('source_credit'),
            'source_rights_status': job.get('source_rights_status'),
            'title': job.get('title'),
            'article': job.get('article'),
            'capture_date': job.get('capture_date'),
            'staged': str(source),
            'render_sha256': result['dds_sha256'],
        }
        for field, value in current_fields.items():
            if value is not None:
                entry[field] = value
            elif source_changed:
                entry.pop(field, None)
        if archived_sources:
            entry['superseded_sources'] = archived_sources
        manifest[job['key']] = {
            **entry, 'key': job['key'], 'name': job['name'],
            'portrait': job['original_dds'], 'status': status,
            'provenance': ('User-approved original historical photo, native crop/format conversion only.'
                if status == 'original_historical_user_approved' else 'Documentary reference individually edited using built-in image_gen and visually reviewed.'),
            'style_edit': {
                'tool': result['tool'], 'user_prompt': result.get('user_prompt'),
                'user_approval': result.get('user_approval'),
                'generated_sha256': result.get('generated_sha256'),
                'dds_sha256': result['dds_sha256'],
                'review_note': result['review_note'],
                'era_review': historical,
                'identity_review': identity,
            },
        }
        approved.append((source, target))
    return manifest_path, manifest, approved, statuses


def install(manifest_path, manifest, approved, recovery_root):
    """Recover the complete previous asset/manifest state on a failed write."""
    recovery = recovery_root / ('install_recovery_' + uuid.uuid4().hex)
    recovery.mkdir(parents=True)
    manifest_backup = recovery / 'portrait_manifest.json'
    shutil.copyfile(manifest_path, manifest_backup)
    changes = [(source, target) for source, target in approved if not target.exists() or digest(source) != digest(target)]
    previous = []
    for _, target in changes:
        assert target.resolve().is_relative_to(ROOT.resolve()), target
        saved = recovery / 'before' / target.relative_to(ROOT)
        if target.exists():
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(target, saved)
            previous.append((target, saved))
        else:
            previous.append((target, None))
    try:
        for source, target in changes:
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + '.mdcw_install_tmp')
            shutil.copyfile(source, temporary)
            assert digest(temporary) == digest(source), target
            temporary.replace(target)
        temporary = manifest_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temporary.replace(manifest_path)
    except BaseException:
        for target, saved in previous:
            assert target.resolve().is_relative_to(ROOT.resolve()), target
            if saved:
                shutil.copyfile(saved, target)
            elif target.exists():
                target.unlink()
        shutil.copyfile(manifest_backup, manifest_path)
        raise
    return recovery


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs', type=Path, required=True)
    ap.add_argument('--backup', type=Path, required=True)
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--install', action='store_true')
    ap.add_argument('--era-review', type=Path)
    ap.add_argument('--identity-review', type=Path)
    args = ap.parse_args()
    if args.install:
        assert args.era_review, 'An explicit historical source-era review is required before installation.'
        assert args.identity_review, 'A source-caption identity review is required before installation.'
    manifest_path, manifest, approved, statuses = prepare(args.jobs, args.backup, args.era_review, args.identity_review)
    recovery = None
    if args.install:
        recovery = install(manifest_path, manifest, approved, args.jobs.parent)
    report = {'installed': args.install, 'approved': len(approved),
              'status_counts': dict(statuses), 'recovery': str(recovery) if recovery else None,
              'targets': [str(t.relative_to(ROOT)).replace('\\', '/') for _, t in approved]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'targets'}))


if __name__ == '__main__':
    main()
