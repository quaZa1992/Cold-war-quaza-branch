# IMPERIA CW — Cold War: event art — export ddr intro.
"""Package the unchanged MD photograph in its native country-event frame.

FFmpeg performs the proportional photo fit and native frame composition.
Pillow only decodes DDS/PNG and verifies the lossless asset export.
"""
from pathlib import Path
import hashlib
import json
import shutil
import struct
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MD = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
PHOTO = ROOT/'gfx/event_pictures/europe/russia - SOV/warsaw1_gdr.dds'
FRAME = MD/'gfx/event_pictures/generic/elections/political_deal.dds'
OUTPUT = ROOT/'gfx/event_pictures/coldwar_1970/COLDWAR_DDR_intro.png'


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    source = ROOT/'tools/event_art/source'
    photo_png = source/'COLDWAR_DDR_intro_original.png'
    frame_png = source/'MD_country_event_frame_reference.png'
    with Image.open(PHOTO) as image:
        image.convert('RGBA').save(photo_png)
    with Image.open(FRAME) as image:
        image.convert('RGBA').save(frame_png)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                    '-i',str(frame_png),'-i',str(photo_png),
                    '-filter_complex','[0:v]format=rgba[frame];'
                    '[1:v]scale=180:150:force_original_aspect_ratio=increase:flags=lanczos,'
                    'crop=180:150,format=rgba[photo];'
                    '[frame][photo]overlay=19:6:format=auto[out]',
                    '-map','[out]','-frames:v','1',str(OUTPUT)],check=True)
    with Image.open(OUTPUT) as decoded:
        image = decoded.convert('RGBA')
        assert image.size == (217,163)
        pixels = image.tobytes()
    with Image.open(frame_png) as decoded:
        native = decoded.convert('RGBA')
        assert all(image.getpixel((x,y)) == native.getpixel((x,y))
                   for y in range(163) for x in range(217)
                   if not (19 <= x < 199 and 6 <= y < 156))
    header = [124,4111,163,217,217*4,0,0]+[0]*11+[32,65,0,32,255,65280,16711680,4278190080,4096,0,0,0,0]
    dds = OUTPUT.with_suffix('.dds')
    dds.write_bytes(b'DDS '+struct.pack('<31I',*header)+pixels)
    assert Image.open(dds).convert('RGBA').tobytes() == pixels
    archived = ROOT/'Claude outputs/COLDWAR_DDR_generator/art/dds/COLDWAR_DDR_intro.dds'
    archived.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(dds,archived)
    report = dict(event='COLDWAR_DDR.1', size=[217,163], photo_inset=[19,6,180,150],
                  fit='Proportional central crop, no stretching or generated replacement artwork',
                  native_frame_pixels_unchanged=True, lossless_dds_matches_png=True,
                  source=str(PHOTO.relative_to(ROOT)),
                  source_sha256=hashlib.sha256(PHOTO.read_bytes()).hexdigest(),
                  dds_sha256=hashlib.sha256(dds.read_bytes()).hexdigest(), engine_tested=False)
    (source/'COLDWAR_DDR_intro_export.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
