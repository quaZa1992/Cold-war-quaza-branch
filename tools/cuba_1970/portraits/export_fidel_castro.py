# IMPERIA COLD WAR — export the user-selected Fidel Castro photograph.
"""Convert the supplied photograph to native leader textures without restyling."""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIZE = (156, 210)
TARGETS = (
    ROOT / 'gfx/leaders/CUB/CUB_Coldwar_Fidel_Castro.dds',
    ROOT / 'gfx/leaders/CUB/fidel_castro.dds',
)


def main():
    with Image.open(HERE / 'fidel_castro_source.png') as source:
        # Keep the complete hairline and face; trim only the lower shirt to fit.
        crop_height = round(source.width * SIZE[1] / SIZE[0])
        assert crop_height <= source.height
        portrait = source.convert('RGBA').crop((0, 0, source.width, crop_height))
        portrait = portrait.resize(SIZE, Image.Resampling.LANCZOS)
    for target in TARGETS:
        portrait.save(target, format='DDS')
        with Image.open(target) as exported:
            assert exported.format == 'DDS' and exported.size == SIZE
            assert exported.convert('RGBA').tobytes() == portrait.tobytes()
        print(target.relative_to(ROOT))
    portrait.save(HERE / 'fidel_castro_preview.png')


if __name__ == '__main__':
    main()
