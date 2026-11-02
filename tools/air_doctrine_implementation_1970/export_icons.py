# IMPERIA COLD WAR — Native transparent DDS doctrine icon export.
"""Copy ImageGen masters and export unchanged artwork in native MD BGRA storage."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import struct
import textwrap
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools/air_doctrine_design_1970'))
from design import GRANDS, SUBS
PROJECT = 'IMPERIA COLD WAR'

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DEST = ROOT / 'gfx/interface/doctrines/icons/air/mdcw_expansion'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def native_dds(image, path):
    """Uncompressed BGRA32 with native channel masks, no DX10/sRGB header."""
    width, height = image.size
    header = [124, 0x100F, height, width, width * 4, 0, 0] + [0] * 11
    header += [32, 0x41, 0, 32, 0xFF0000, 0xFF00, 0xFF, 0xFF000000]
    header += [0x1000, 0, 0, 0, 0]
    path.write_bytes(b'DDS ' + struct.pack('<31I', *header) + image.tobytes('raw', 'BGRA'))
    decoded = Image.open(path).convert('RGBA')
    assert decoded.tobytes() == image.tobytes(), f'Colour or alpha storage mismatch: {path}'


def main():
    source_record = json.loads((HERE / 'imagegen_sources.json').read_text(encoding='utf-8'))
    masters = HERE / 'masters'
    masters.mkdir(exist_ok=True)
    DEST.mkdir(parents=True, exist_ok=True)
    records = []
    for record in source_record['generated_assets']:
        source = Path(re.search(r'as (C:.*?\.png) by default', record['source_hint']).group(1))
        target = masters / (record['id'] + '.png')
        if not target.exists():
            assert source.is_file(), source
            shutil.copy2(source, target)
        raw = Image.open(target)
        assert raw.mode == 'RGBA', f'No alpha: {target}'
        image = raw.copy()
        bounds = image.getchannel('A').getbbox()
        assert bounds and image.getchannel('A').getextrema()[0] == 0, f'Nontransparent master: {target}'
        image = image.crop(bounds)
        image.thumbnail((60, 60), Image.Resampling.LANCZOS)
        icon = Image.new('RGBA', (64, 64))
        icon.alpha_composite(image, ((64 - image.width) // 2, (64 - image.height) // 2))
        icon.save(masters / (record['id'] + '_64.png'))
        output = DEST / (record['id'] + '.dds')
        native_dds(icon, output)
        records.append({'id': record['id'], 'master': target.relative_to(ROOT).as_posix(),
                        'master_sha256': digest(target), 'texture': output.relative_to(ROOT).as_posix(),
                        'texture_sha256': digest(output), 'size': list(icon.size), 'master_alpha_bounds': list(bounds),
                        'icon_alpha_bounds': list(icon.getchannel('A').getbbox()), 'format': 'DDS BGRA32',
                        'author_credit': 'OpenAI built-in ImageGen, directed by Codex for the user',
                        'reference_author': 'Existing Millennium Dawn artwork; individual artist unknown',
                        'reference_licence_or_separate_permission': 'unknown',
                        'modifications': 'Transparent bounds crop, aspect-preserving downscale, centering and native DDS encoding only'})
    names = {item['id']: item['name'] for item in [*GRANDS, *SUBS]}
    sheet = Image.new('RGB', (1200, 710), (30, 33, 29))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
        small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
    except OSError:
        font = small = ImageFont.load_default()
    draw.text((20, 12), 'IMPERIA COLD WAR: Doctrine icons at native 64 px and enlarged 96 px', font=font, fill=(231, 225, 204))
    draw.text((20, 35), 'Asset review composition. The in-game window is not shown.', font=small, fill=(171, 175, 160))
    for index, record in enumerate(records):
        x = (index % 5) * 240
        y = (index // 5) * 145 + 65
        draw.rounded_rectangle((x + 5, y, x + 234, y + 138), radius=5, fill=(40, 43, 38), outline=(72, 76, 65))
        icon = Image.open(DEST / (record['id'] + '.dds')).convert('RGBA')
        sheet.paste(icon, (x + 18, y + 15), icon)
        enlarged = icon.resize((96, 96), Image.Resampling.NEAREST)
        sheet.paste(enlarged, (x + 116, y + 3), enlarged)
        for line_index, line in enumerate(textwrap.wrap(names[record['id']], 28)):
            draw.text((x + 12, y + 101 + 17 * line_index), line, font=small, fill=(230, 228, 213))
    draw.text((20, 660), 'Style donors: existing MD blue-grey/black/orange air doctrine pictograms. New artwork: built-in ImageGen.', font=small, fill=(171, 175, 160))
    draw.text((20, 682), 'Runtime DDS: 64 x 64, transparent BGRA32. Original transparent masters and prompts retained.', font=small, fill=(171, 175, 160))
    sheet.save(HERE / 'icon_review.png')
    (HERE / 'icon_manifest.json').write_text(json.dumps({'project': PROJECT, 'assets': records}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'project': PROJECT, 'exported': len(records), 'review': str(HERE / 'icon_review.png')}))


if __name__ == '__main__':
    main()
