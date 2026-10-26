# IMPERIA CW — Cold War: historical currencies — build icons.
"""Encode approved transparent currency art as native single-frame DDS icons."""
from pathlib import Path
import hashlib
import importlib.util
import json
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'gfx/interface/ideas/laws'
spec=importlib.util.spec_from_file_location('native_currency_dds',ROOT/'tools/ddr_currency/build_icon.py')
native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
ASSETS={'soviet_rouble':'mdcw_soviet_rouble','guilder':'mdcw_dutch_guilder'}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    preview=HERE/'previews';preview.mkdir(exist_ok=True)
    records={}
    for name,stem in ASSETS.items():
        source=HERE/f'source/{name}_generated.png'
        image=Image.open(source).convert('RGBA')
        alpha=image.getchannel('A')
        assert alpha.getextrema()==(0,255), 'Imagegen source must already be transparent'
        # Ignore near-invisible generation noise only when measuring padding.
        # The original RGBA pixels inside the measured crop are preserved.
        visible=alpha.point(lambda value:255 if value>4 else 0).getbbox()
        assert visible
        bounds=(max(0,visible[0]-2),max(0,visible[1]-2),
                min(image.width,visible[2]+2),min(image.height,visible[3]+2))
        subject=image.crop(bounds)
        subject.thumbnail((58,60),Image.Resampling.LANCZOS)
        frame=Image.new('RGBA',(72,64),(0,0,0,0))
        frame.paste(subject,(9+(58-subject.width)//2,3+(60-subject.height)//2))
        target=OUT/f'{stem}.dds';native.write_native_dds(frame,target)
        decoded=Image.open(target).convert('RGBA')
        assert decoded.tobytes()==frame.tobytes()
        frame.save(preview/f'{name}.png')
        records[name]={'source':source.relative_to(ROOT).as_posix(),'source_sha256':sha(source),
                       'texture':target.relative_to(ROOT).as_posix(),'texture_sha256':sha(target),
                       'dimensions':[72,64],'format':'uncompressed A8R8G8B8','frames':1,
                       'padding_measurement_alpha_threshold':4,'source_crop':list(bounds),
                       'alpha_bbox':list(frame.getchannel('A').getbbox())}
    labels=[('Soviet Rouble','mdcw_soviet_rouble'),('Dutch Guilder','mdcw_dutch_guilder'),
            ('Swiss Franc','swiss_frank'),('Chinese Yuan','chinese_yuan'),('East German Mark','currency_ddr_mark')]
    sheet=Image.new('RGB',(220*len(labels),280),(37,40,36));draw=ImageDraw.Draw(sheet)
    for index,(label,stem) in enumerate(labels):
        icon=Image.open(OUT/f'{stem}.dds').convert('RGBA')
        enlarged=icon.resize((216,192),Image.Resampling.BILINEAR)
        sheet.paste(enlarged,(index*220+2,5),enlarged)
        sheet.paste(icon,(index*220+74,201),icon)
        draw.text((index*220+8,267),label,fill=(235,235,230))
    sheet.save(preview/'currency_comparison.png')
    (HERE/'asset_manifest.json').write_text(json.dumps({'tool':'built-in image_gen','assets':records},indent=2)+'\n')
    print('PASS: Two native 72x64 transparent currency icons packaged; DDS round trips exact.')


if __name__=='__main__':main()
