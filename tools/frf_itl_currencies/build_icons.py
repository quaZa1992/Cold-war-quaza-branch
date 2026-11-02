# IMPERIA COLD WAR — Package approved Franc and Lira art in the native currency footprint.
"""Fit retained transparent Imagegen masters and export lossless BGRA currency icons."""
from pathlib import Path
import hashlib
import importlib.util
import json
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('native_currency_dds', ROOT / 'tools/ddr_currency/build_icon.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def main():
    records = {}
    preview = HERE / 'previews'
    preview.mkdir(exist_ok=True)
    for currency in ('french_franc', 'italian_lira'):
        source = HERE / 'source' / (currency + '.png')
        image = Image.open(source).convert('RGBA')
        assert image.getchannel('A').getextrema() == (0, 255)
        visible = image.getchannel('A').point(lambda value: 255 if value > 4 else 0).getbbox()
        assert visible
        bounds = (max(0, visible[0] - 2), max(0, visible[1] - 2),
                  min(image.width, visible[2] + 2), min(image.height, visible[3] + 2))
        subject = image.crop(bounds)
        subject.thumbnail((58, 60), Image.Resampling.LANCZOS)
        frame = Image.new('RGBA', (72, 64), (0, 0, 0, 0))
        frame.paste(subject, (9 + (58 - subject.width) // 2, 3 + (60 - subject.height) // 2))
        output = ROOT / 'gfx/interface/ideas/laws' / ('COLDWAR_' + currency + '.dds')
        native.write_native_dds(frame, output)
        assert Image.open(output).convert('RGBA').tobytes() == frame.tobytes()
        frame.save(preview / (currency + '.png'))
        records[currency] = {
            'source': source.relative_to(ROOT).as_posix(),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'texture': output.relative_to(ROOT).as_posix(),
            'texture_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'dimensions': [72, 64], 'format': 'BGRA8/A8R8G8B8', 'frames': 1,
        }
    comparison = Image.new('RGB', (360, 210), '#252824')
    draw = ImageDraw.Draw(comparison)
    for index, currency in enumerate(records):
        image = Image.open(preview / (currency + '.png')).convert('RGBA')
        comparison.paste(image.resize((144, 128), Image.Resampling.NEAREST), (index * 180 + 18, 10),
                         image.resize((144, 128), Image.Resampling.NEAREST))
        comparison.paste(image, (index * 180 + 54, 143), image)
    comparison.save(preview / 'comparison.png')
    (HERE / 'asset_manifest.json').write_text(json.dumps({
        'project': 'IMPERIA COLD WAR', 'tool': 'built-in image_gen', 'assets': records,
    }, indent=2) + '\n', encoding='utf-8')
    print('Packaged and decoded two native 72x64 BGRA currency icons.')


if __name__ == '__main__':
    main()
