# IMPERIA CW — Cold War: jerusalem landmarks — icons.
"""Create two-frame UI atlases from the transparent native Blender render."""
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def create():
    source = Image.open(HERE/'previews/western_wall_icon.png').convert('RGBA')
    for size, directory, filename in [
        (64, 'large', 'western_wall_icon.dds'),
        (32, 'small', 'western_wall_icon_small.dds'),
    ]:
        normal = source.resize((size, size), Image.Resampling.LANCZOS)
        disabled = ImageOps.grayscale(normal).convert('RGBA')
        disabled.putalpha(normal.getchannel('A'))
        atlas = Image.new('RGBA', (size*2, size))
        atlas.paste(normal, (0, 0))
        atlas.paste(disabled, (size, 0))
        target = ROOT/'gfx/interface/buildings/historical_buildings'/directory/filename
        target.parent.mkdir(parents=True, exist_ok=True)
        atlas.save(target)


if __name__ == '__main__':
    create()
