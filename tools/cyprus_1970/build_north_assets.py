# IMPERIA CW — Cold War: cyprus 1970 — build north assets.
"""Encode individually restored, source-verified historical portraits as DDS.

All creative edits are performed by image_gen. This step copies selected masters
and encodes native frames. A named historical person MUST have their own restored
photo reference. There is no generic-person or native-portrait fallback.
"""
from pathlib import Path
import json
import shutil
import hashlib
from PIL import Image, ImageOps, ImageDraw, ImageFont
from north import POLITICIANS, TMT

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent/'north'
OUT=ROOT/'gfx/leaders/NCY/1970'
DISPLAY={1976:'Hayri Ündül',1978:'Atilla Erdoğan',1980:'Kemal Yavuz',
         1982:'Hikmet Köksal',1984:'Y. Selçuk Saka',1986:'Bilgi Büyükünal',
         1988:'Ali Yalçın',1990:'Erdoğan Dirik'}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'small').mkdir(exist_ok=True)
    (HERE/'masters').mkdir(exist_ok=True)
    records=json.loads((HERE/'generation.json').read_text(encoding='utf-8'))
    generated={p['key']:p for p in records['assets']}
    officers=json.loads((HERE/'references/gkk_metadata.json').read_text(encoding='utf-8'))
    for p in officers:p['display_name']=DISPLAY[int(p['key'].split('_')[-1])]
    (HERE/'references/gkk_metadata.json').write_text(json.dumps(officers,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    gkk={p['key']:p for p in officers}
    names={p[0]:p[1] for p in POLITICIANS+TMT}
    names.update({p['key']:p['display_name'] for p in officers})
    missing=set(names)-set(generated)
    assert not missing,'Historical people without restored reference photos: '+', '.join(sorted(missing))
    assert 'generic' in generated,'Collective administrations require their neutral institutional emblem.'
    assets={}
    for key,name in list(names.items())+[('generic','Collective Administration')]:
        item=generated[key]
        master=HERE/item.get('project_master','masters/COLDWAR_NCY_1970_'+key+'.png')
        master.parent.mkdir(parents=True,exist_ok=True)
        if not master.exists():shutil.copy2(item['generated_source'],master)
        source=master
        status='collective_institution_emblem' if key=='generic' else 'image_gen_restored_historical_reference'
        provenance=[('tools/cyprus_1970/north/references/'+p) for p in item['files']]
        provenance.extend(item.get('source_urls',[]))
        if key in gkk:provenance.extend([gkk[key]['url'],gkk[key]['source']])
        with Image.open(source) as im:
            im=im.convert('RGB')
            image=ImageOps.fit(im.convert('RGBA'),(156,210),method=Image.Resampling.LANCZOS,centering=(.5,.4))
            large=OUT/('COLDWAR_NCY_1970_'+key+'.dds')
            small=OUT/'small'/('COLDWAR_NCY_1970_'+key+'_small.dds')
            image.save(large,format='DDS')
            image.resize((38,51),Image.Resampling.LANCZOS).save(small,format='DDS')
        assets[key]={'name':name,'portrait':large.relative_to(ROOT).as_posix(),
                     'small':small.relative_to(ROOT).as_posix(),'status':status,
                     'source':str(source.relative_to(ROOT)).replace('\\','/'),
                     'provenance':provenance,'source_crop':None,
                     'sha256':hashlib.sha256(large.read_bytes()).hexdigest()}
    sheet=Image.new('RGB',(6*205,4*270),(29,34,42));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)
    for i,(key,a) in enumerate((k,a) for k,a in assets.items() if k!='generic'):
        x=(i%6)*205;y=(i//6)*270
        with Image.open(ROOT/a['portrait']) as im:sheet.paste(im.convert('RGB'),(x+24,y+8))
        draw.text((x+102,y+232),a['name'],font=font,fill='white',anchor='mm')
    sheet.save(HERE/'portrait_preview.png')
    sheet.save(HERE/'portrait_preview_v2.png')
    (HERE/'assets.json').write_text(json.dumps({'assets':assets},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'people':len(names),'restored_historical_portraits':len(names),'collective_emblems':1,'placeholders':0}))


if __name__=='__main__':main()
