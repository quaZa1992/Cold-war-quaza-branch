# IMPERIA CW — Cold War: warsaw landmarks — icons.
"""Create two-frame building UI atlases from the native Blender icon render."""
from pathlib import Path
from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def create():
    source = Image.open(HERE/'previews/palace_icon.png').convert('RGBA')
    for size, directory, filename in [
        (64, 'large', 'warsaw_palace_icon.dds'),
        (32, 'small', 'warsaw_palace_icon_small.dds'),
    ]:
        normal = source.resize((size, size), Image.Resampling.LANCZOS)
        disabled = ImageOps.grayscale(normal).convert('RGBA')
        disabled.putalpha(normal.getchannel('A'))
        atlas = Image.new('RGBA', (size*2, size))
        atlas.paste(normal, (0, 0)); atlas.paste(disabled, (size, 0))
        atlas.save(ROOT/'gfx/interface/buildings/historical_buildings'/directory/filename)


if __name__ == '__main__':
    create()
