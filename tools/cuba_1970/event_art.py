# IMPERIA COLD WAR — Cuba country-event pictures in the exact native MD frame.
"""Package existing art for the country-event viewport; no gameplay mutations."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
OUT=ROOT/'gfx/event_pictures/COLDWAR_CUB_1970'
REVIEW=ROOT/'docs/design/cuba_foreign_1970/event_frames'
PREFIX='GFX_COLDWAR_CUB_1970_event_'
FRAME=MD/'gfx/event_pictures/generic/elections/political_deal.dds'
SOURCES={
    'signing':'gfx/event_pictures/generic/events/treaty.dds',
    'declined':'gfx/event_pictures/generic/events/treaty_rejected.dds',
    'harvest':'gfx/event_pictures/generic/economy/generic_grain_silo.dds',
    'factory':'gfx/event_pictures/generic/economy/generic_factory.dds',
    'cuban_parade':'gfx/event_pictures/americas/carribbean/cuba - CUB/cuba_wants_protec_rus.dds',
    'prisoners':'gfx/event_pictures/americas/carribbean/cuba - CUB/prison_cuba.dds',
}
# These photographs already have the exact MD frame; reuse them directly.
REUSE={
    'soviet':'gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.dds',
    'conference':'gfx/event_pictures/generic/elections/political_deal.dds',
}
BINDINGS={
    'GFX_cuba_constitution':'signing',
    'GFX_cuba_wants_protec_rus':'cuban_parade',
    'GFX_soviet_union_flag':'soviet',
    'GFX_news_us_cuba':'signing',
    'GFX_pol_socialism_event':'signing',
    'GFX_treaty':'signing',
    'GFX_treaty_rejected':'declined',
    'GFX_generic_grain_silo':'harvest',
    'GFX_cuban_prisons_event':'prisoners',
    'GFX_politics_talks':'conference',
    'GFX_generic_factory':'factory',
}


def sprite(key):
    if key.startswith(PREFIX):
        assert key.removeprefix(PREFIX) in SOURCES|REUSE,key
        return key
    return PREFIX+BINDINGS[key]


def bind(text):
    text=re.sub(r'(\bpicture\s*=\s*)(GFX_[A-Za-z0-9_]+)',lambda m:m[1]+sprite(m[2]),text)
    # Retained recipient reply events also need an explicit framed photograph.
    sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
    from script_ast import parse,first
    for kind,op,event in parse(text):
        if kind!='country_event' or first(event,'hidden')=='yes' or first(event,'hide_window')=='yes' or first(event,'picture'):
            continue
        ident=first(event,'id')
        text=re.sub(r'(\bid\s*=\s*'+re.escape(ident)+r')\b',lambda m:m[1]+'\n\tpicture = '+PREFIX+'signing',text,count=1)
    return text


def resolve(rel):
    return next(p for base in (ROOT,MD) if (p:=base/rel).is_file())


def main():
    OUT.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    native=Image.open(FRAME).convert('RGBA');assert native.size==(217,163)
    reference=REVIEW/'md-frame-reference.png';native.save(reference)
    records=[]
    for key,rel in SOURCES.items():
        src=resolve(rel);original=Image.open(src)
        assert original.size==(217,163),(key,original.size)
        png=REVIEW/(key+'.png')
        # FFmpeg does only proportional crop/format packaging of existing MD art.
        # Preserve the MD frame pixel for pixel, including its transparent edges.
        photo='crop=197:147:10:8,scale=180:150:force_original_aspect_ratio=increase:flags=lanczos,crop=180:150,setsar=1,format=rgba'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','1',
                        '-i',str(reference),'-i',str(src),'-filter_complex',
                        '[0:v]format=rgba[frame];[1:v]'+photo+'[photo];[frame][photo]overlay=19:6:format=auto[out]',
                        '-map','[out]','-frames:v','1',str(png)],check=True)
        im=Image.open(png).convert('RGBA');assert im.size==(217,163)
        assert all(im.getpixel((x,y))==native.getpixel((x,y)) for y in range(163) for x in range(217)
                   if not (19<=x<199 and 6<=y<156))
        assert im.crop((19,6,199,156)).getchannel('A').getextrema()==(255,255)
        header=[124,4111,163,217,217*4,0,0]+[0]*11+[32,65,0,32,16711680,65280,255,4278190080,4096,0,0,0,0]
        dest=OUT/(key+'.dds');dest.write_bytes(b'DDS '+struct.pack('<31I',*header)+im.tobytes('raw','BGRA'))
        assert Image.open(dest).convert('RGBA').tobytes()==im.tobytes()
        records.append(dict(sprite=PREFIX+key,source=src.relative_to(ROOT).as_posix() if src.is_relative_to(ROOT) else src.as_posix(),
                            source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),output=dest.relative_to(ROOT).as_posix(),
                            sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),size=[217,163],photo_inset=[19,6,180,150],frame_pixels_unchanged=True))
    gfx=['# IMPERIA COLD WAR — Cuba country-event photos in the native MD frame.','spriteTypes = {']
    for key in SOURCES|REUSE:
        rel=REUSE.get(key,f'gfx/event_pictures/COLDWAR_CUB_1970/{key}.dds')
        gfx+=['\tspriteType = {',f'\t\tname = "{PREFIX+key}"',f'\t\ttexturefile = "{rel}"','\t}']
    gfx+=['}'];(ROOT/'interface/COLDWAR_CUB_1970_eventpictures.gfx').write_text('\n'.join(gfx)+'\n',encoding='utf8')
    notice=('# IMPERIA COLD WAR: Cuba event-picture packaging\n\nExisting Millennium Dawn photographs are packaged in the exact 217 x 163 MD country-event frame, with a proportional central crop into its 180 x 150 photograph area. The frame comes from main MD generic/elections/political_deal.dds. The Soviet meeting picture is the existing user-supplied, restored project photograph; see tools/event_art/export_politburo_session.py and its source records. Individual original MD photographers/authors and applicable licences are unknown here; consult MD and game credits. This record asserts no ownership or redistribution rights. No generated replacement artwork or new historical photograph is claimed. Source paths and hashes are recorded in EVENT_ART_EXPORT.json.\n')
    (OUT/'IMPERIA_COLD_WAR_NOTICE.md').write_text(notice,encoding='utf8');(REVIEW/'IMPERIA_COLD_WAR_NOTICE.md').write_text(notice,encoding='utf8')
    (ROOT/'tools/cuba_1970/EVENT_ART_EXPORT.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','frame':FRAME.as_posix(),'frame_sha256':hashlib.sha256(FRAME.read_bytes()).hexdigest(),'packaged':records,'reused':REUSE},indent=2)+'\n',encoding='utf8')
    print(json.dumps({'packaged':len(records),'reused':len(REUSE),'size':[217,163],'native_frame_pixels_unchanged':True}))


if __name__=='__main__':main()
