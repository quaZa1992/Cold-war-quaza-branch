# IMPERIA CW — Cold War: cyprus 1970 — build portraits.
"""Copy image_gen masters into the project and export native MD portrait DDSs.

Creative restoration/colourisation is performed by image_gen, not this script.
This step only preserves masters, fits the native portrait frame and encodes DDS.
"""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent/'portraits'
PEOPLE={'lyssarides':'Vassos Lyssarides','papaioannou':'Ezekias Papaioannou',
        'grivas':'Georgios Grivas','sampson':'Nikos Sampson','kyprianou':'Spyros Kyprianou'}


def main():
    records=json.loads((HERE/'generation.json').read_text(encoding='utf-8'))
    masters=HERE/'masters';masters.mkdir(parents=True,exist_ok=True)
    output=ROOT/'gfx/leaders/CYP/1970';output.mkdir(parents=True,exist_ok=True)
    assets={}
    for item in records['assets']:
        key=item['key'];name=PEOPLE[key];stem='COLDWAR_CYP_1970_'+name.replace(' ','_')
        master=masters/(stem+'.png')
        if not master.exists():shutil.copy2(item['generated_source'],master)
        with Image.open(master) as image:
            portrait=ImageOps.fit(image.convert('RGBA'),(156,210),method=Image.Resampling.LANCZOS,centering=(.5,.4))
            dst=output/(stem+'.dds');portrait.save(dst,format='DDS')
        with Image.open(dst) as check:
            assert check.format=='DDS' and check.size==(156,210) and check.mode=='RGBA'
        assets[key]={'name':name,'portrait':dst.relative_to(ROOT).as_posix(),
                     'master':master.relative_to(ROOT).as_posix(),'dimensions':[156,210],
                     'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()}
    sheet=Image.new('RGB',(1050,275),(29,34,42));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',15)
    for i,key in enumerate(PEOPLE):
        asset=assets[key]
        with Image.open(ROOT/asset['portrait']) as portrait:sheet.paste(portrait.convert('RGB'),(i*210+27,20))
        draw.text((i*210+105,247),asset['name'],font=font,fill=(230,232,237),anchor='mm')
    sheet.save(HERE/'portrait_preview.png')
    result={'tool':'built-in image_gen','export_format':'DDS RGBA uncompressed',
            'requested_prompt':records['requested_prompt'],'portraits':assets,
            'preview':'tools/cyprus_1970/portraits/portrait_preview.png'}
    (HERE/'assets.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'exported':len(assets),'dimensions':[156,210],'folder':output.relative_to(ROOT).as_posix()}))


if __name__=='__main__':main()
