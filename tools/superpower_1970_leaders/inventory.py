# IMPERIA COLD WAR — USA and Soviet political leadership inventory.
from pathlib import Path
import json
import re
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
from multiplayer_quality.audit import parse


def walk(tree):
    for key, op, value in tree:
        yield key, op, value
        if isinstance(value, list):
            yield from walk(value)


def main():
    manifest = json.loads((ROOT / 'tools/historical_politics_1970/portrait_manifest.json').read_text(encoding='utf-8'))
    world = json.loads((ROOT / 'tools/historical_politics_1970/data/world.json').read_text(encoding='utf-8'))
    special = json.loads((ROOT / 'tools/historical_politics_1970/special_portraits.json').read_text(encoding='utf-8'))
    sources = json.loads((ROOT / 'tools/historical_politics_1970/portrait_sources.json').read_text(encoding='utf-8')).get('assets', {})
    result = {'project': 'IMPERIA COLD WAR', 'countries': {}}
    for tag in ('USA', 'SOV'):
        country = next(c for c in world['countries'] if c['tag'] == tag)
        extra = next(c for c in special['countries'] if c['tag'] == tag)
        people = []
        for r in [*country.get('leaders', []), *extra.get('leaders', [])]:
            key = tag + '_' + r['id']
            ready = manifest.get(key, {})
            people.append({'id': r['id'], 'name': r['name'], 'slot': r.get('party_index'),
                'portrait': ready.get('portrait'), 'portrait_status': ready.get('status'),
                'source_portrait': ready.get('source'), 'record': r})
        creations = []
        files = [ROOT / ('common/scripted_effects/' + tag + '_political_leaders.txt')]
        files += [ROOT / 'common/scripted_effects/USA_1970_scripted_effects.txt'] if tag == 'USA' else [ROOT / 'common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt']
        files += [ROOT / ('common/national_focus/' + ('USA_1970.txt' if tag == 'USA' else 'COLDWAR_SOV_1970_focus.txt'))]
        for path in files:
            source = path.read_text(encoding='utf-8-sig')
            for k, op, v in walk(parse(source)):
                if k == 'create_country_leader':
                    fields = {key: val.strip('"') for key, op, val in v if isinstance(val, str)}
                    creations.append({**fields, 'file': path.relative_to(ROOT).as_posix()})
        samples = {r['name']: r for r in creations if r['file'].split('/')[-1] != tag + '_political_leaders.txt'}
        for r in people:
            if r['name'] not in samples:
                samples[r['name']] = r
        sheet = Image.new('RGB', (1000, ((len(samples) + 5) // 6) * 198), '#20272b')
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 11)
        for index, (name, row) in enumerate(samples.items()):
            x, y = (index % 6) * 166, (index // 6) * 198
            candidate = row.get('picture') or row.get('portrait')
            if candidate:
                path = ROOT / candidate
                if not path.exists():
                    path = ROOT / 'gfx/leaders' / tag / candidate
                if path.is_file():
                    draw.rectangle((x, y, x + 165, y + 197), fill='#30393a')
                    sheet.paste(ImageOps.fit(Image.open(path).convert('RGB'), (120, 160)), (x + 23, y + 2))
            draw.text((x + 83, y + 175), name[:28], font=font, fill='white', anchor='mm')
        sheet.save(HERE / (tag + '_EXISTING.png'))
        result['countries'][tag] = {'people': people, 'parties': country.get('parties'), 'creations': creations}
        result['countries'][tag]['known_photographs'] = {key: row for key, row in sources.items() if key.startswith(tag + '_')}
    (HERE / 'INVENTORY.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for tag, rows in result['countries'].items():
        print(tag, 'reviewed people:')
        for r in rows['people']:
            print(r['id'], r['name'], 'slot', r['slot'], 'portrait', r['portrait_status'], r['portrait'])
        print(tag, 'existing creations:', sorted({r['name'] for r in rows['creations']}))
        print(tag, 'parties:', [(r.get('index'), r.get('name')) for r in rows['parties']])
        print(tag, 'known photographs:', [(key, bool(row.get('source') and Path(row['source']).is_file())) for key, row in rows['known_photographs'].items()])


if __name__ == '__main__':
    main()
