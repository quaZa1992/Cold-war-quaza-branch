# IMPERIA CW — Cold War: uae 1970 — export event picture.
"""Package the ImageGen colourisation as native217x163 RGBA DDS.

FFmpeg owns proportional resizing/padding; this writes only a lossless DDS
container around that PNG's existing pixels. It does not generate artwork.
"""
from pathlib import Path
import hashlib
import json
import struct
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT/'tools/uae_1970/art/source/COLDWAR_UAE_rulers_colour_master.png'
OUTPUT = ROOT/'gfx/event_pictures/COLDWAR_UAE/COLDWAR_UAE_rulers_colour.png'


def main():
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(MASTER),
                    '-vf','scale=217:-1:flags=lanczos,pad=217:163:0:(oh-ih)/2:color=black,format=rgba',
                    '-frames:v','1',str(OUTPUT)],check=True)
    image = Image.open(OUTPUT).convert('RGBA')
    assert image.size == (217,163)
    assert image.getchannel('A').getextrema() == (255,255)
    header = [124,4111,163,217,217*4,0,0]+[0]*11+[32,65,0,32,255,65280,16711680,4278190080,4096,0,0,0,0]
    dds = OUTPUT.with_suffix('.dds')
    dds.write_bytes(b'DDS '+struct.pack('<31I',*header)+image.tobytes())
    assert Image.open(dds).convert('RGBA').tobytes() == image.tobytes()
    result = {'size':list(image.size),'format':'DDS uncompressed RGBA32','opaque':True,
              'decoded_dds_matches_png':True,'all_seven_people_retained':True,
              'fit':'Proportional full-width fit with top/bottom black matte; no crop or stretch',
              'master_sha256':hashlib.sha256(MASTER.read_bytes()).hexdigest(),
              'dds_sha256':hashlib.sha256(dds.read_bytes()).hexdigest()}
    (ROOT/'tools/uae_1970/art/EVENT_PICTURE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
