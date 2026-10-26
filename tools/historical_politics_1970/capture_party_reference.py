# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Capture native MD family explanations and exact-organization text icons.

Only display metadata is imported. Modern parties, popularity and ideology
assignments never replace the historical catalogue.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import unicodedata

from build import HERE, IDEOLOGIES, load_catalog


def normalize(value):
    value = unicodedata.normalize('NFKD', value).casefold()
    return re.sub(r'[^a-z0-9]', '', value)


def organization(value):
    value = re.sub(r'£\w+', '', value)
    return re.sub(r'^\s*\([^)]*\)\s*(?:-\s*)?', '', value).strip()


def read_loc(path):
    return dict(re.findall(r'^\s+([^\s:]+):(?:\d+)?\s*"(.*)"\s*$',
                           path.read_text(encoding='utf-8-sig'), re.M))


def capture(main):
    family_path = main / 'localisation/english/0_political_system_l_english.yml'
    party_path = main / 'localisation/english/MD_politics_view_parties_l_english.yml'
    families, parties = read_loc(family_path), read_loc(party_path)
    result = {'source_root': str(main), 'source_sha256': {
        str(path.relative_to(main)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (family_path, party_path)}, 'families': {}, 'icons': {}, 'native_icons': {}}
    for ideology in IDEOLOGIES:
        key = 'generic.' + ideology
        result['families'][ideology] = {
            'name': re.sub(r'^£\w+\s*', '', families[key]),
            'description': families[key + '_desc'],
            'icon': families[key + '_icon']}
    for key, value in parties.items():
        if not re.match(r'^[A-Z0-9]{3}\.', key) or key.endswith(('_desc', '_icon')):
            continue
        icon = re.search(r'£(\w+)', value)
        if not icon or icon[1].startswith(('generic_', 'muslim_brotherhood')):
            continue
        result['native_icons'].setdefault(key[:3], []).append({
            'source_key': key, 'source_name': value,
            'organization': organization(value), 'text_icon': '£' + icon[1]})
    for tag, country in load_catalog().items():
        for party in country.get('parties', []):
            name = party['name']
            wanted = {normalize(name), normalize(re.sub(r'\s*\([^)]*\)', '', name))}
            candidates = []
            for key, value in parties.items():
                if not key.startswith(tag + '.') or key.endswith(('_desc', '_icon')):
                    continue
                icon = re.search(r'£(\w+)', value)
                if not icon or icon[1].startswith(('generic_', 'muslim_brotherhood')):
                    continue
                if normalize(organization(value)) in wanted:
                    candidates.append({'source_key': key, 'source_name': value,
                                       'text_icon': '£' + icon[1]})
            # Several date aliases may use one emblem; conflicting emblems are
            # deliberately left for the reviewed historical icon manifest.
            if candidates and len({row['text_icon'] for row in candidates}) == 1:
                result['icons'].setdefault(tag, {})[name] = candidates[0]
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('main_md', type=Path)
    args = parser.parse_args()
    output = capture(args.main_md)
    (HERE / 'party_md_reference.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'families': len(output['families']),
                      'exact_organization_icons': sum(map(len, output['icons'].values()))}))
