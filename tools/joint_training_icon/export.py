# IMPERIA CW — Cold War: Export the Imagegen military badge to native idea-icon size.
from pathlib import Path
import hashlib
import json
import struct
import subprocess
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = HERE/'master.png'
OUTPUT = ROOT/'gfx/interface/ideas/nat_ideas/COLDWAR_IMPERIA_joint_training_command.png'


def main():
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(MASTER),
                    '-vf','scale=64:64:flags=lanczos,format=rgba','-frames:v','1',str(OUTPUT)],check=True)
    with Image.open(OUTPUT) as decoded:
        image = decoded.convert('RGBA')
        assert image.size == (64,64)
        assert image.getchannel('A').getextrema() == (0,255)
        assert image.getpixel((0,0))[3] == 0
        pixels = image.tobytes()
    header = [124,4111,64,64,64*4,0,0]+[0]*11+[32,65,0,32,255,65280,16711680,4278190080,4096,0,0,0,0]
    dds = OUTPUT.with_suffix('.dds')
    dds.write_bytes(b'DDS '+struct.pack('<31I',*header)+pixels)
    assert Image.open(dds).convert('RGBA').tobytes() == pixels
    report = dict(tool='Built-in image_gen, precise-object-edit',
                  master='tools/joint_training_icon/master.png',prompt='tools/joint_training_icon/prompt.txt',
                  output=str(dds.relative_to(ROOT)),size=[64,64],format='Uncompressed RGBA32 DDS',
                  alpha_preserved=True,lossless_dds_matches_png=True,
                  master_sha256=hashlib.sha256(MASTER.read_bytes()).hexdigest(),
                  dds_sha256=hashlib.sha256(dds.read_bytes()).hexdigest(),engine_tested=False)
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
