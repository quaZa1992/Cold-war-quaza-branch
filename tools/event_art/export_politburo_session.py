# IMPERIA CW — Cold War: event art — export politburo session.
"""Package the ImageGen restoration in the exact native MD country-event frame.

FFmpeg handles image scaling and frame composition. Pillow only decodes pixels
for the lossless DDS container and verifies the unchanged native frame pixels.
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
MASTER = ROOT/'tools/event_art/source/COLDWAR_SOV_politburo_session_master.png'
FRAME = MD/'gfx/event_pictures/generic/elections/political_deal.dds'
OUTPUT = ROOT/'gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.png'


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame_png = ROOT/'tools/event_art/source/MD_country_event_frame_reference.png'
    with Image.open(FRAME) as reference:
        reference.convert('RGBA').save(frame_png)
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-i', str(frame_png), '-i', str(MASTER),
                    '-filter_complex', '[0:v]format=rgba[frame];'
                    '[1:v]scale=180:150:flags=lanczos,format=rgba[photo];'
                    '[frame][photo]overlay=19:6:format=auto[out]',
                    '-map', '[out]', '-frames:v', '1', str(OUTPUT)], check=True)
    with Image.open(OUTPUT) as image:
        image = image.convert('RGBA')
        assert image.size == (217, 163)
        pixels = image.tobytes()
        native = Image.open(frame_png).convert('RGBA')
        assert all(image.getpixel((x,y)) == native.getpixel((x,y))
                   for y in range(163) for x in range(217)
                   if not (19 <= x < 199 and 6 <= y < 156)), 'Native MD frame changed'
    header = [124,4111,163,217,217*4,0,0]+[0]*11+[32,65,0,32,255,65280,16711680,4278190080,4096,0,0,0,0]
    dds = OUTPUT.with_suffix('.dds')
    dds.write_bytes(b'DDS '+struct.pack('<31I', *header)+pixels)
    assert Image.open(dds).convert('RGBA').tobytes() == pixels
    # The Soviet generator stages its own binary; a later tree build must retain it.
    generator_copy = ROOT/'Claude outputs/COLDWAR_SOV_generator/art/dds/COLDWAR_SOV_politburo_session.dds'
    generator_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(dds, generator_copy)
    report = {'image_tool': 'built-in image_gen', 'master': str(MASTER.relative_to(ROOT)),
              'source_photo': 'tools/event_art/source/COLDWAR_SOV_politburo_session_original.png',
              'prompt_file': 'tools/event_art/politburo_prompt.txt',
              'runtime_event_ids': ['COLDWAR_SOV.10', 'COLDWAR_SOV.11'],
              'output': str(dds.relative_to(ROOT)), 'size': [217,163],
              'photo_inset': [19,6,180,150], 'format': 'DDS uncompressed RGBA32',
              'native_frame_pixels_unchanged': True, 'dds_matches_preview': True,
              'master_sha256': hashlib.sha256(MASTER.read_bytes()).hexdigest(),
              'dds_sha256': hashlib.sha256(dds.read_bytes()).hexdigest()}
    (ROOT/'docs/event_art_review/politburo_export.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
