# IMPERIA COLD WAR — export Imagegen colourisations with the native size and alpha.
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
NATIVE = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/event_pictures')
MASTERS = ROOT / 'docs/nuclear_intelligence/art'
OUT = ROOT / 'gfx/event_pictures/coldwar_nuclear_intelligence'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, original in [('enrichment', 'report_event_generic_construction_site.dds'), ('weapons', 'report_event_generic_research_lab.dds')]:
        source = Image.open(NATIVE / original).convert('RGBA')
        colour = Image.open(MASTERS / (key + '_color_master.png')).convert('RGBA')
        # Packaging only: the generative edit supplies the colours. Keep the native
        # footprint and original alpha so the photograph fits the existing event frame.
        colour = colour.resize(source.size, Image.Resampling.LANCZOS)
        colour.putalpha(source.getchannel('A'))
        destination = OUT / ('COLDWAR_NI_' + key + '_color.dds')
        colour.save(destination)
        exported = Image.open(destination).convert('RGBA')
        assert exported.size == source.size
        assert exported.getchannel('A').tobytes() == source.getchannel('A').tobytes()
        assert len(set(zip(*[exported.getchannel(c).tobytes() for c in 'RGB']))) > 256
        print(f'{destination.relative_to(ROOT)}: {source.width}x{source.height}, native alpha preserved')


if __name__ == '__main__':
    main()
