# IMPERIA COLD WAR — Real archival photos in the native MD country-event frame.
from .shared import *
import struct
import subprocess
from PIL import Image


def emit():
    source=HERE/'source/event_photos'
    notice=json.loads((source/'NOTICE.json').read_text(encoding='utf-8'))
    donor=ROOT/'gfx/event_pictures/generic/elections/political_deal.dds'
    if not donor.exists():donor=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')/'gfx/event_pictures/generic/elections/political_deal.dds'
    frame=Image.open(donor).convert('RGBA');assert frame.size==(217,163)
    reference=Image.open(ROOT/'tools/event_art/source/MD_country_event_frame_reference.png').convert('RGBA')
    assert frame.tobytes()==reference.tobytes(),'Current MD frame differs from inspected donor'
    gui=(ROOT/'interface/eventwindow.gui').read_text(encoding='utf-8')
    for token in ('width = 581 height = 206','x = 215 y = -1','width = 300 height = 47','max_slots_horizontal = 1'):assert token in gui,token
    folder=ROOT/'gfx/event_pictures/COLDWAR_USA_KS';folder.mkdir(parents=True,exist_ok=True)
    changed=[];records=[]
    # Native 180x150 photo inset; outer frame and alpha remain byte-identical.
    frame_path=ROOT/'tools/event_art/source/MD_country_event_frame_reference.png'
    for h,name in notice['regional_files'].items():
        original=source/name;relative=f'gfx/event_pictures/COLDWAR_USA_KS/aftermath_{h}.dds'
        output=ROOT/relative;preview=folder/f'aftermath_{h}.png'
        anchor=notice['vertical_crop_anchor'][h]
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(frame_path),'-i',str(original),'-filter_complex',f'[0:v]format=rgba[frame];[1:v]scale=180:150:force_original_aspect_ratio=increase:flags=lanczos,crop=180:150:(in_w-out_w)/2:(in_h-out_h)*{anchor},format=rgba[photo];[frame][photo]overlay=19:6:format=auto[out]','-map','[out]','-frames:v','1',str(preview)],check=True)
        image=Image.open(preview).convert('RGBA');assert image.size==(217,163)
        assert all(image.getpixel((x,y))==frame.getpixel((x,y)) for y in range(163) for x in range(217) if not (19<=x<199 and 6<=y<156))
        header=[124,4111,163,217,868,0,0]+[0]*11+[32,65,0,32,16711680,65280,255,4278190080,4096,0,0,0,0]
        data=b'DDS '+struct.pack('<31I',*header)+image.tobytes('raw','BGRA')
        if not output.exists() or output.read_bytes()!=data:output.write_bytes(data);changed.append(relative)
        assert Image.open(output).convert('RGBA').tobytes()==image.tobytes()
        records.append(dict(region=h,source_photo=name,source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),vertical_crop_anchor=anchor,output=relative,output_sha256=hashlib.sha256(data).hexdigest(),native_frame_unchanged=True))
    provenance=dict(project='IMPERIA COLD WAR',source_record='tools/usa_kissinger_implementation/source/event_photos/NOTICE.json',photos=notice['photos'],context=notice['context'],modifications=notice['modifications'],native_frame=dict(source=str(donor),credit='Paradox / Millennium Dawn artists; individual author unknown',licence_or_permission='Unknown; upstream rights retained',size=[217,163],photo_inset=[19,6,180,150],sha256=hashlib.sha256(donor.read_bytes()).hexdigest()),event_window=dict(bottom=[581,206],picture_offset=[5,5],options_offset=[215,-1],option_slot=[300,47],horizontal_slots=1),assets=records)
    relative='gfx/event_pictures/COLDWAR_USA_KS/NOTICE.json'
    if write(relative,json.dumps(provenance,indent=2)+'\n'):changed.append(relative)
    return changed
