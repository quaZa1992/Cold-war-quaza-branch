# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Bind reviewed symbols to dated party rows; keep source masters external."""
from __future__ import annotations

import argparse
import copy
import json
from datetime import date
from pathlib import Path

from prepare_catalog import ROOT, normalized


def day(value):
    return date(*map(int, value.split('.')))


def fmt(value):
    return f'{value.year}.{value.month}.{value.day}'


def bind(world, package, staged, install=False):
    world = copy.deepcopy(world)
    countries = {c['tag']: c for c in world['countries']}
    manifest, sprites, skipped = {}, [], []
    for icon in package['icons']:
        binding = icon.get('binding', {})
        if binding.get('status') != 'confirmed':
            continue
        tag = binding['tag']
        country = countries.get(tag)
        matches = [] if not country else [p for p in country['parties'] if p['index'] == binding['index'] and normalized(p['name']) == normalized(binding['match_normalized_name'])]
        if not matches:
            skipped.append({'icon': icon['iconid'], 'reason': 'Existing bespoke country registry owns this party, or no matched catalogue row.'})
            continue
        ident = icon['iconid']
        marker = binding['text_icon'].replace('£GFX_', '£')
        record = {**icon, 'text_icon': marker}
        if binding['install_action'] == 'add_staged':
            rel = 'gfx/texticons/parties_icons/1970_historical/' + ident + '.dds'
            source = staged / 'dds' / (ident + '.dds')
            assert source.is_file(), source
            from PIL import Image
            with Image.open(source) as image:
                assert image.size == (22, 22)
            if install:
                destination = ROOT / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
            record['texture_path'] = rel
            sprites.append(f'\tspriteType = {{ name = "GFX_{ident}" texturefile = "{rel}" legacy_lazy_load = no }}')
        else:
            assert (ROOT / binding['existing_texture']).is_file()
        manifest[ident] = record
        for party in matches:
            a, b = max(day(party.get('from', '1970.1.1')), day(binding['valid_from'])), min(day(party.get('until') or '2001.1.1'), day(binding.get('valid_until') or '2001.1.1'))
            if a >= b:
                continue
            country['parties'].remove(party)
            cuts = [(day(party.get('from', '1970.1.1')), a, False), (a, b, True), (b, day(party.get('until') or '2001.1.1'), False)]
            for start, end, active in cuts:
                if start < end:
                    row = {**party, 'from': fmt(start), 'until': fmt(end)}
                    if active:
                        row['icon_id'] = ident
                    country['parties'].append(row)
    registry = '# Historical party symbols; source/license metadata is in tools/historical_politics_1970/party_icon_manifest.json\nspriteTypes = {\n' + '\n'.join(sprites) + '\n}\n'
    return world, manifest, registry, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--research', type=Path, required=True)
    ap.add_argument('--catalogue', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--install-assets', action='store_true')
    args = ap.parse_args()
    load = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
    world, manifest, registry, skipped = bind(load(args.catalogue), load(args.research / 'party_icon_manifest.json'), args.research / 'party_icons_staged', args.install_assets)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'world.json').write_text(json.dumps(world, indent=2, ensure_ascii=False), encoding='utf-8')
    (args.output / 'party_icon_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    (args.output / 'mdcw_historical_parties.gfx').write_text(registry, encoding='utf-8')
    (args.output / 'icon_binding_report.json').write_text(json.dumps({'bound': len(manifest), 'new_sprites': registry.count('spriteType ='), 'skipped': skipped}, indent=2), encoding='utf-8')
    print('Bound symbols:', len(manifest), 'new sprites:', registry.count('spriteType ='), 'bespoke/unbound:', len(skipped))


if __name__ == '__main__':
    main()
