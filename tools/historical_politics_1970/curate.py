# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Apply keyed historical corrections without changing frozen source drafts."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from periods import apply_period_labels


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def apply_monaco(world, proposal):
    country = next(c for c in world['countries'] if c['tag'] == 'MNC')
    country['parties'] = [p for p in country['parties'] if p['index'] != 1]
    country['parties'].append({'index': 1, 'name': proposal['party_proposal']['name'],
        'from': '1970.1.1', 'source_urls': proposal['party_proposal']['source_urls'],
        'description': 'National and Democratic Union (UND), founded in 1962. A parliamentary conservative organization distinct from the reigning House of Grimaldi.'})
    ids = {x['id'] for x in proposal['leaders']}
    country['leaders'] = [x for x in country['leaders'] if x['id'] not in ids]
    for row in proposal['leaders']:
        country['leaders'].append({**row, 'party_name': proposal['party_proposal']['name'],
            'description': row['role_basis']})
    return world


def curate(world, review, egypt, inventory):
    countries = {c['tag']: c for c in world['countries']}
    for patch in review['corrections']:
        country = countries[patch['tag']]
        target = patch['target']
        rows = country['parties' if target['type'] == 'party' else 'leaders']
        matches = [p for p in rows if all(p.get(k) == v for k, v in target.items() if k != 'type')]
        if patch['operation'] == 'add_leader':
            assert not matches, (patch['tag'], target)
            rows.append({**patch['add'], 'source_urls': patch['source_urls']})
            continue
        assert len(matches) == 1, (patch['tag'], target, len(matches))
        row = matches[0]
        if patch['operation'] == 'delete':
            rows.remove(row)
        elif patch['operation'] == 'review_remove_or_relabel':
            row.update(name='Constitutional Opposition', description='Independent constitutional and parliamentary opposition; not a claim that a named legal party existed under the party ban.', source_urls=patch['source_urls'])
        elif patch['operation'] == 'review_affiliation':
            # U Nu's documented 1969 exile party, rather than the unrelated NLD.
            assert patch['tag'] == 'BRM' and row['id'] == 'u_nu'
            row['party_name'] = 'Parliamentary Democracy Party / Democratic Opposition'
            row['party_index'] = 3
            row['source_urls'] += ['https://files.eric.ed.gov/fulltext/ED059142.pdf']
            country['parties'].append({'index': 3, 'name': 'Parliamentary Democracy Party', 'from': '1969.8.29', 'until': '1974.1.1', 'source_urls': ['https://files.eric.ed.gov/fulltext/ED059142.pdf'], 'date_policy': 'Dissolution year boundary, not an asserted dissolution day.'})
        else:
            row.update(patch.get('replace', {}))
            row['source_urls'] = sorted(set(row.get('source_urls', []) + patch['source_urls']))
        country['parties'].extend(patch.get('add', []))
        if patch.get('add_party'):
            country['parties'].append(patch['add_party'])
    def transition(tag, name, earlier, when, sources, later=None):
        rows = countries[tag]['parties']
        match = [p for p in rows if p['name'] == name]
        assert len(match) == 1, (tag, name)
        row = match[0]
        old_start = row.get('from', '1970.1.1')
        row.update(name=later or name, **{'from': when, 'from_precision': 'day', 'date_precision': 'day'})
        row['source_urls'] = sources
        rows.append({'index': row['index'], 'name': earlier, 'from': min(old_start, '1970.1.1'), 'until': when, 'source_urls': sources})
    transition('POR', 'Socialist Party (PS)', 'Portuguese Socialist Action (ASP)', '1973.4.19', ['https://ps.pt/a-nossa-historia/'])
    transition('POR', 'Social Democratic Party (PSD)', 'Liberal Wing (Ala Liberal)', '1974.5.6', ['https://www.psd.pt/pt/cronologia'], 'Popular Democratic Party (PPD/PSD)')
    transition('SWI', "Swiss People's Party (SVP/UDC)", "Party of Farmers, Traders and Independents (BGB)", '1971.9.22', ['https://www.svp.ch/partei/geschichte/'])
    transition('SWI', 'Christian Democratic People’s Party (CVP/PDC)', 'Conservative-Christian Social People’s Party', '1971.1.1', ['https://www.parlament.ch/de/über-das-parlament/Seiten/Rollen-Parteien.aspx'])
    for row in countries['NAU']['parties']:
        if row['name'] == 'Nauru Party':
            row.update({'from': '1977.1.1', 'date_precision': 'day', 'from_precision': 'day', 'date_policy': 'Available after the documented foundation year 1976; exact day not evidenced.', 'source_urls': ['https://data.ipu.org/election-summary/PDF/NAURU_1987_E.PDF']})
    # Formal foundation years do not become invented January-1 dates. Reveal
    # the name after the documented year unless a precise day is evidenced.
    for country in countries.values():
        seen = set()
        distinct = []
        for party in country['parties']:
            start = date(*map(int, party.get('from', '1970.1.1').split('.')))
            if party.get('from_precision', party.get('date_precision')) == 'year' and start > date(1970, 1, 1):
                party['documented_from'] = party['from']
                party['from'] = f'{start.year + 1}.1.1'
                party['date_policy'] = 'Conservative availability after the evidenced foundation year; exact day unknown.'
            signature = (party['index'], party['name'], party.get('from'), party.get('until'))
            if signature not in seen:
                distinct.append(party)
                seen.add(signature)
        country['parties'] = distinct
    # Correcting a foundation date can expose an earlier gap. Preserve the
    # original, separately inventoried 1970 institution in that interval.
    for baseline in inventory['countries']:
        country = countries[baseline['tag']]
        if country.get('managed_by_existing_system'):
            continue
        index = baseline['ruling_party_index']
        starts = [p for p in country['parties'] if p['index'] == index]
        if not any(date(*map(int, p.get('from', '1970.1.1').split('.'))) <= date(1970, 1, 1) and (not p.get('until') or date(1970, 1, 1) < date(*map(int, p['until'].split('.')))) for p in starts):
            later = sorted([p['from'] for p in starts], key=lambda s: tuple(map(int, s.split('.'))))
            label = baseline['effective_ruling_party_name']
            if baseline['tag'] == 'SYE':
                label = 'National Liberation Front (NLF)'
            country['parties'].append({'index': index, 'name': label, 'from': '1970.1.1', 'until': later[0] if later else None,
                'source_urls': ['local:IMP_1970_starting_parties_l_english.yml'], 'description': 'The governing institution at the 1970 bookmark.'})
    world = apply_period_labels(world, egypt)
    world['review_note'] = 'Research draft plus keyed corrections. Exact primary evidence and coarse date precision remain recorded per row; no automatic political changes.'
    return world


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--research', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    world = curate(load(args.research / 'normalized_world.json'), load(args.research / 'final_catalog_review.json'), load(args.research / 'egypt_period_labels.json'), load(args.research / 'party_inventory.json'))
    monaco = args.research / 'ART/monaco_references/monaco_data_proposal.json'
    if monaco.is_file():
        world = apply_monaco(world, load(monaco))
    alignment = Path(__file__).resolve().parent / 'party_family_alignment.json'
    if alignment.is_file():
        from align import apply_alignment
        world = apply_alignment(world, load(alignment))
    from monarchy_alignment import apply_world
    world = apply_world(world)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(world, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Curated', len(world['countries']), 'countries')


if __name__ == '__main__':
    main()
