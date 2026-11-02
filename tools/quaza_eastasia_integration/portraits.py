# IMPERIA COLD WAR — User-photo Kim Il Sung leader and mourning portrait exports.
"""Convert the approved image-generation outputs to native MD portrait DDS files."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
from PIL import Image
from source import ROOT,HERE,REPORT,SNAPSHOT

USER_PHOTO=Path('C:/Users/Enes/AppData/Local/Temp/codex-clipboard-db14cba7-7a69-49b4-be22-472b544e0d57.png')
TARGETS={'leader':'gfx/Leaders/NKO/NKO_Coldwar_Kim_Il_Sung.dds',
         'memorial':'gfx/Leaders/NKO/COLDWAR_NKO_Kim_Il_Sung_memorial.dds'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--leader',type=Path,required=True);ap.add_argument('--memorial',type=Path,required=True);args=ap.parse_args()
    art=HERE/'art';art.mkdir(exist_ok=True)
    if not (art/'kim_il_sung_user_photo.png').exists():shutil.copyfile(USER_PHOTO,art/'kim_il_sung_user_photo.png')
    rows={}
    for kind in ('leader','memorial'):
        source=getattr(args,kind);master=art/('kim_il_sung_'+kind+'_master.png')
        shutil.copyfile(source,master)
        target=ROOT/TARGETS[kind]
        if target.exists():
            backup=SNAPSHOT.parent/'before'/TARGETS[kind]
            if not backup.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(target,backup)
        with Image.open(master) as im:
            assert abs(im.width/im.height-156/210)<.06,'Unexpected portrait aspect ratio'
            native=im.convert('RGBA').resize((156,210),Image.Resampling.LANCZOS)
            native.save(target,format='DDS',pixel_format='DXT5')
            # HOI4 expects a concrete legacy format and one declared mip level.
            raw=bytearray(target.read_bytes())
            struct.pack_into('<I',raw,20,((156+3)//4)*((210+3)//4)*16)
            struct.pack_into('<I',raw,28,1)
            target.write_bytes(raw)
        with Image.open(target) as check:assert check.size==(156,210) and check.mode=='RGBA'
        rows[kind]={'source_master':str(master.relative_to(ROOT)),'target':TARGETS[kind],
                    'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'dimensions':[156,210],'format':'DDS legacy DXT5 RGBA, one mip level'}
    record={'project':'IMPERIA COLD WAR','date':'2026-10-27','source':'User-supplied archival Kim Il Sung photograph',
            'original_author':'Unknown','original_licence_or_permission':'Unknown; supplied by the user for this modification',
            'frame_source':'gfx/Leaders/NKO/Kim_Jong_il_death.dds, inherited MD mourning-frame composition; individual original author and licence unknown',
            'method':'Built-in image_gen edits. Original photograph colourised and zoomed to head-and-shoulders, then composited into the existing MD mourning-frame style. Native DDS resize/encoding follows generation. No ownership of the original photograph or frame asserted.',
            'prompt_leader':'Preserve the exact older smiling Kim Il Sung, glasses, age and Mao jacket from the user photograph; natural colourisation; tight vertical head-and-shoulders MD leader portrait; neutral blurred background; no frame or text.',
            'prompt_memorial':'Replace only the photograph inside the existing gold MD mourning frame with the final colourised user-photo portrait. Preserve older face, glasses, smile, frame, ribbons, flowers and outer alpha. No text or dates.',
            'assets':rows}
    (REPORT/'PORTRAITS.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    notice='IMPERIA COLD WAR\n\nKim Il Sung portraits, 27 October 2026.\n\nThe user supplied the archival source photograph. Its original author and licence are unknown. The inherited MD mourning-frame source is `Kim_Jong_il_death.dds`; individual author and applicable permission are unknown. No ownership is asserted.\n\nThe built-in image_gen tool colourised and cropped the photograph and composed the memorial variant. Native game exports are 156 x 210 legacy DDS DXT5 with one mip level. Editable raster masters, the source photograph, prompt specification and hashes are recorded under `tools/quaza_eastasia_integration/art` and `docs/quaza_eastasia_integration_20261027/PORTRAITS.json`.\n'
    (ROOT/'gfx/Leaders/NKO/COLDWAR_NKO_PORTRAIT_NOTICE.md').write_text(notice,encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','portraits':rows}))


if __name__=='__main__':main()
