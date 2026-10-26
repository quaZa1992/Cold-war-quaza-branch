# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Normalize independently researched catalogues; never install runtime files."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILES = ['americas_oceania.json', 'european_asian_majors.json', 'africa.json', 'asia_middleeast_ssr.json']


def normalized(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub('[^a-z0-9]', '', value)


def day(value):
    return date(*map(int, value.split('.')))


def fmt(value):
    return f'{value.year}.{value.month}.{value.day}'


def overlay(catalogues, path):
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding='utf-8'))
    for name, expected in payload.get('input_sha256', {}).items():
        source = path.parent / name
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        assert actual == expected, ('QA snapshot changed; rebase overlay', name)
    patches = payload['patches']
    for patch in patches:
        file, pointer = patch['path'].split('#', 1)
        obj = catalogues[file]
        bits = pointer.lstrip('/').split('/')
        for part in bits[:-1]:
            obj = obj[int(part)] if isinstance(obj, list) else obj[part]
        key = int(bits[-1]) if isinstance(obj, list) and bits[-1] != '-' else bits[-1]
        if patch['op'] == 'remove':
            del obj[key]
        elif patch['op'] == 'add' and key == '-':
            obj.append(patch['value'])
        else:
            obj[key] = patch['value']
    return patches


def existing_portraits():
    """Use a local image only when a script links that exact person's name."""
    by_name = defaultdict(set)
    files = list((ROOT / 'common/scripted_effects').glob('*.txt')) + list((ROOT / 'history/countries').glob('*.txt'))
    by_basename = defaultdict(list)
    for f in (ROOT / 'gfx/leaders').rglob('*.dds'):
        by_basename[f.name.lower()].append(f.relative_to(ROOT).as_posix())
    pattern = re.compile(r'create_country_leader\s*=\s*\{((?:"[^"\n]*"|[^{}]|\{[^{}]*\})*)\}', re.S)
    for f in files:
        text = f.read_text(encoding='utf-8-sig')
        for match in pattern.finditer(text):
            body = match[1]
            name = re.search(r'\bname\s*=\s*"([^"]+)"', body)
            picture = re.search(r'\bpicture\s*=\s*"([^"]+)"', body)
            if not name or not picture:
                continue
            path = picture[1].replace('\\', '/')
            if any(x in path.lower() for x in ('/generic', 'imp_white_', 'unknown', 'placeholder', 'default')):
                continue
            if not (ROOT / path).is_file():
                hits = by_basename[Path(path).name.lower()]
                country = f.name[:3].lower()
                local = [x for x in hits if '/' + country + '/' in x.lower()]
                path = local[0] if len(local) == 1 else hits[0] if len(hits) == 1 else ''
            if path:
                by_name[normalized(name[1])].add(path)
    return by_name


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--research', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = {name: json.loads((args.research / name).read_text(encoding='utf-8-sig')) for name in FILES}
    patches = overlay(raw, args.research / 'qa_corrections.json')
    inventory = json.loads((args.research / 'party_inventory.json').read_text(encoding='utf-8'))['countries']
    baseline = {c['tag']: c for c in inventory}
    refs_file = args.research / 'photo_research/portrait_references.json'
    references = json.loads(refs_file.read_text(encoding='utf-8')) if refs_file.exists() else {}
    aliases = existing_portraits()
    world = {}
    notes = []
    for file, payload in raw.items():
        for original in payload['countries']:
            c = copy.deepcopy(original)
            tag = c['tag']
            assert tag not in world, tag
            c['source_catalogue'] = file
            parties = c.setdefault('parties', [])
            # The reviewed start label is a fallback, not a second vote-bearing
            # organization or a change to the historical government's index.
            b = baseline[tag]
            start_index = b['ruling_party_index']
            at_start = [p for p in parties if p['index'] == start_index and day(p.get('from', '1970.1.1')) <= date(1970, 1, 1)]
            if not at_start:
                label = b['effective_ruling_party_name']
                if tag == 'PER':
                    label = 'Pahlavi Dynasty'
                if tag == 'NAU':
                    label = 'Independent Parliamentary Group'
                parties.insert(0, {'index': start_index, 'name': label, 'from': '1970.1.1', 'until': None,
                    'source_urls': ['local:IMP_1970_starting_parties_l_english.yml'],
                    'description': 'The historical governing party or institution at the 1970 bookmark.'})
            unique = {}
            for p in c.get('leaders', []):
                index = p['party_index']
                if index is None:
                    c.setdefault('non_party_figures', []).append(p)
                    notes.append({'tag': tag, 'name': p['name'], 'issue': 'ceremonial/nonparty office; not appointed as a party government leader'})
                    continue
                assert isinstance(index, int) and 0 <= index < 24, (tag, p)
                original_id = p['id']
                p['id'] = re.sub('[^a-z0-9_]', '', p['id'].lower())
                assert p['id'], (tag, original_id)
                title = p.get('wikipedia_title') or p['name']
                ref = references.get(title, {})
                life_end = date(2001, 1, 1)
                deaths = [x for x in ref.get('death', []) if x.get('precision', 0) >= 11]
                if deaths:
                    value = deaths[0]['time'].split('T')[0].lstrip('+')
                    life_end = min(life_end, date.fromisoformat(value) + timedelta(days=1))
                start = max(date(1970, 1, 1), day(p.get('available_from') or '1970.1.1'))
                precision = p.get('available_from_precision', p.get('date_precision', 'day'))
                if precision == 'year' and start > date(1970, 1, 1):
                    start = date(start.year + 1, 1, 1)
                    p['availability_note'] = 'Available after the documented entry year; the source does not establish a day within that year.'
                if life_end <= start:
                    notes.append({'tag': tag, 'name': p['name'], 'issue': 'no living eligible interval', 'source': title})
                    continue
                # Removal from a historical government is not a calendar ban on
                # an alternate-history politician remaining politically active.
                p['documented_interval'] = {'from': p.get('available_from'), 'until': p.get('available_until')}
                p['available_from'], p['available_until'] = fmt(start), fmt(life_end)
                if not p.get('portrait'):
                    matches = aliases[normalized(p['name'])]
                    if len(matches) == 1:
                        p['portrait'] = next(iter(matches))
                if p.get('portrait'):
                    assert (ROOT / p['portrait']).is_file(), (tag, p['portrait'])
                key = (normalized(p['name']), index)
                if key in unique:
                    prior = unique[key]
                    prior['available_from'] = fmt(min(day(prior['available_from']), start))
                    prior['available_until'] = fmt(max(day(prior['available_until']), life_end))
                    prior['source_urls'] = sorted(set(prior['source_urls'] + p['source_urls']))
                    if not prior.get('portrait'):
                        prior['portrait'] = p.get('portrait')
                else:
                    unique[key] = p
            c['leaders'] = list(unique.values())
            used_ids = set()
            for p in c['leaders']:
                if p['id'] in used_ids:
                    p['id'] += '_p' + str(p['party_index'])
                assert p['id'] not in used_ids, (tag, p['id'])
                used_ids.add(p['id'])
            world[tag] = c
    for tag in sorted(set(baseline) - set(world)):
        world[tag] = {'tag': tag, 'parties': [], 'leaders': [], 'managed_by_existing_system': True}
    report = {'countries': [world[tag] for tag in sorted(world)], 'notes': notes,
        'scope': 'All 163 active 1970 countries; dated manual candidates through 2000.',
        'qa_patch_count': len(patches)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'countries': len(world), 'leaders': sum(len(c['leaders']) for c in world.values()),
        'parties': sum(len(c['parties']) for c in world.values()), 'qa_patches': len(patches), 'notes': len(notes)}))


if __name__ == '__main__':
    main()
