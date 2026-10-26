# IMPERIA CW — Cold War: uae 1970 — flags.
"""Export the public-domain Council SVG to native HOI4 flag resolutions.

This is a deterministic vector export, not a generated reconstruction. The
source's colours, stripe heights and seven-point star path remain unchanged.
Only the engine's required aspect ratios differ from the source artwork.
"""
from pathlib import Path
import io
import re
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE/'art/source/COLDWAR_UAE_trucial_council.svg'
SIZES = {'': (82, 52), 'medium': (41, 26), 'small': (10, 7)}
OUTLOOKS = ('', '_democratic', '_communism', '_fascism', '_neutrality', '_nationalist')


def render(size):
    svg = ET.fromstring(SOURCE.read_bytes())
    width, height = float(svg.attrib['width']), float(svg.attrib['height'])
    scale = 8
    image = Image.new('RGBA', (size[0]*scale, size[1]*scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    sx, sy = image.width/width, image.height/height
    for element in svg:
        attrs = element.attrib
        if element.tag.endswith('rect'):
            x, y = float(attrs.get('x', 0)), float(attrs.get('y', 0))
            w, h = float(attrs['width']), float(attrs['height'])
            draw.rectangle((x*sx, y*sy, (x+w)*sx-1, (y+h)*sy-1), fill=attrs['fill'])
        elif element.tag.endswith('path'):
            # The vendored SVG contains one closed straight-line star path.
            assert not re.search(r'[ACHQSTVachqstv]', attrs['d'])
            coords = [float(v) for v in re.findall(r'-?(?:\d*\.\d+|\d+)', attrs['d'])]
            a, b, c, d, e, f = [float(v) for v in re.findall(r'-?(?:\d*\.\d+|\d+)', attrs['transform'])]
            points = [((a*x+c*y+e)*sx, (b*x+d*y+f)*sy) for x, y in zip(coords[::2], coords[1::2])]
            draw.polygon(points, fill=attrs['fill'])
        else:
            raise ValueError('Unexpected source SVG shape: '+element.tag)
    return image.resize(size, Image.Resampling.LANCZOS)


def outputs():
    result = {}
    for directory, size in SIZES.items():
        image = render(size)
        buffer = io.BytesIO()
        image.save(buffer, format='TGA', compression=None)
        for outlook in OUTLOOKS:
            path = Path('gfx/flags')/directory/('UAE_TRUCIAL_1970'+outlook+'.tga')
            result[path.as_posix()] = buffer.getvalue()
    return result


def install():
    result = outputs()
    for relative, payload in result.items():
        path = ROOT/relative
        if not path.exists() or path.read_bytes() != payload:
            path.write_bytes(payload)
    return result


if __name__ == '__main__':
    print('Exported', len(install()), 'Council flags')
