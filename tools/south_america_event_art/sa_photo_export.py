# IMPERIA COLD WAR — Native MD packaging of restored South American event photos.
"""Lossless frame composition, native BGRA DDS export and bounded integration."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import shutil
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from sa_photo_catalogue import *

FRAME = 'gfx/event_pictures/generic/elections/political_deal.dds'
BOX = (19,6,199,156)
SIZE = (217,163)
REVIEW = 'docs/event_art_review/south_america_1970'
MARK = '# IMPERIA COLD WAR — Restored South American event photographs.\n'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def plain(value):
    value=re.sub(r'<div\b[^>]*style="[^"]*display:\s*none[^>]*>.*?</div>','',str(value),flags=re.S)
    return html.unescape(re.sub('<[^>]*>','',value)).strip()
def font(size): return ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',size)

def write_dds(im,path):
    # Native A8R8G8B8 DDS. The encoded BGRA masks avoid red/blue reversal.
    head=[124,4111,163,217,868,0,0]+[0]*11+[32,65,0,32,16711680,65280,255,4278190080,4096,0,0,0,0]
    path.write_bytes(b'DDS '+struct.pack('<31I',*head)+im.tobytes('raw','BGRA'))
    assert Image.open(path).convert('RGBA').tobytes()==im.tobytes()

def inspect_gui(root):
    text=(root/'interface/eventwindow.gui').read_text(encoding='utf-8-sig')
    # The complete EventWindow and adjacent option entry are checked, not a diff hunk.
    main=text[text.index('name = "EventWindow"'):text.index('@fade_time')]
    option=text[text.index('name = "event_option_entry"'):]
    for token in ['width = 581 height =427','x=0 y=221','width = 581 height = 206',
                  'x = 5 y = 5','x = -3 y = 35','x = 215 y = -1',
                  'width = 300 height = 30','width = 300 height = 47','max_slots_horizontal = 1']:
        assert token in main,('Changed native EventWindow',token)
    for token in ['width = 300 height = 47','x = 5 y = 0','maxWidth = 340','maxHeight = 40']:
        assert token in option,('Changed native option entry',token)
    return {'gui_sha256':sha(root/'interface/eventwindow.gui'),'window':[581,427],
            'bottom_window':[0,221,581,206],'photo_position':[5,5],'clip_position':[-3,35],
            'option_grid':[215,-1,300,30],'option_slot':[300,47],'max_horizontal_slots':1,
            'option_entry':[300,47],'option_text_position':[5,0],'option_text_max_width':340,
            'option_text_max_height':40,'complete_blocks_inspected':True}

def attribution(records):
    lines=['IMPERIA COLD WAR','', '# Restored South American event photographs','',
           'AI restoration and colorization: built-in OpenAI image_gen, requested by the project owner on 2 November 2026. These are interpreted restorations, not untouched documentary photographs. Colors and reconstructed detail are inferred. Exact prompts are in `tools/south_america_event_art/generations.json`.','',
           'The native MD frame is inherited from `'+FRAME+'`. Original frame artist and separate redistribution permission are unknown. Every pixel outside x=19..198, y=6..155 remains unchanged. No third-party ownership is claimed.','',
           'The source licences below apply to their respective photographs and derivatives, not to unrelated frame material. CC BY-SA derivatives remain subject to the named ShareAlike licence. Metadata not supplied by the source is explicitly unknown. No photographer or institution endorses the project.','',
           'Historical images illustrate the subject of a choice, including alternate outcomes. SOMISA is a 1960 plant photograph. The stock-exchange facade and Angra plant are later architectural/facility photographs, used as institutional illustrations, not claimed as 1970 captures. The medical illustration is a 1973 Senegalese ward, not a photograph of a Chilean, Argentine or Cuban delegation. The oil photo depicts the US fuel crisis of 1973-74 and illustrates imported fuel prices. The Rosario source date is retained as supplied and is not inferred to be 1970.','']
    for r in records:
        lines += ['## '+r['asset'],'','Source: '+r['source_page'],'',
                  'Credit: '+r['credit'],'','Licence/permission: '+r['licence']+(' ('+r['licence_url']+')' if r['licence_url'] else ''),
                  '','Source date: '+r['source_date'],'','Changes: AI colorization or color restoration, scan cleanup and inferred detail; selected photo crop and downsampling to the native 180 x 150 inset. '+r.get('additional_changes',''),
                  '','Output: `'+r['output']+'`.','']
    return '\n'.join(lines)

def build_assets(root=ROOT):
    root=Path(root);source=json.loads((HERE/'sources.json').read_text(encoding='utf-8'))['photos']
    generation=json.loads((HERE/'generations.json').read_text(encoding='utf-8'))['photos']
    rows={r['key']:r for r in generation}
    needed=set(EVENT_ASSETS.values())
    assert needed<=rows.keys(),('Missing generated masters',sorted(needed-rows.keys()))
    native=Image.open(root/FRAME).convert('RGBA');assert native.size==SIZE
    gui=inspect_gui(root)
    dest=root/ASSET_DIR;dest.mkdir(parents=True,exist_ok=True)
    review=root/REVIEW;review.mkdir(parents=True,exist_ok=True)
    masters=HERE/'masters';masters.mkdir(exist_ok=True)
    images={};records=[]
    # Retain every requested restoration, including supporting subjects.
    for key,row in sorted(rows.items()):
        master=masters/(key+'.png')
        if not master.exists(): shutil.copyfile(row['path'],master)
        image=Image.open(master).convert('RGB')
        if key=='shared_treaty':
            image=image.crop((0,round(image.height*.10),image.width,round(image.height*.90)))
        photo=ImageOps.fit(image,(180,150),Image.Resampling.LANCZOS,centering=CENTERS.get(key,(.5,.5))).convert('RGBA')
        composed=native.copy();composed.paste(photo,(19,6))
        assert all(composed.getpixel((x,y))==native.getpixel((x,y)) for y in range(163) for x in range(217) if not (19<=x<199 and 6<=y<156))
        out=dest/(key+'.dds');write_dds(composed,out)
        composed.save(review/(key+'.png'));images[key]=composed
        if key in source:
            meta=source[key]['metadata'];get=lambda n:plain(meta.get(n,{}).get('value',''))
            credit=get('Artist') or 'Unknown original photographer/author.'
            licence=get('LicenseShortName') or 'Unknown licence/permission.'
            info={'source_page':source[key]['source_page'],'credit':credit,'licence':licence,'licence_url':get('LicenseUrl'),
                  'source_date':get('DateTimeOriginal') or 'Unknown date.','source':('tools/south_america_event_art/'+source[key]['original'])}
        else:
            assert key=='shared_contract'
            info={'source_page':'Local Millennium Dawn asset: gfx/event_pictures/generic/events/treaty.dds',
                  'credit':'Millennium Dawn / underlying game asset; individual photographer unknown.',
                  'licence':'Separate redistribution permission unknown. Existing MD/game notices apply.','licence_url':'',
                  'source_date':'Unknown date.','source':'gfx/event_pictures/generic/events/treaty.dds'}
        info.update({'asset':key,'master':master.relative_to(ROOT).as_posix(),'master_sha256':sha(master),
                     'source_sha256':sha(ROOT/info['source']),'output':out.relative_to(root).as_posix(),'output_sha256':sha(out),
                     'frame_pixels_unchanged':True,'dimensions':[217,163],'inset':[19,6,180,150]})
        if key=='bra_split': info['additional_changes']='Only the upper photograph of the two-photo original is used.'
        if key=='chl_finance': info['additional_changes']='Upper architectural facade crop excludes modern pedestrians.'
        if key=='shared_aviation': info['additional_changes']='AI outpainting above and below the aircraft fits the complete plane to a 6:5 canvas; original subject is retained.'
        if key=='shared_treaty': info['additional_changes']='Top and bottom matte fringes are cropped before the native inset composition.'
        records.append(info)
    (root/GFX).write_text(registry_text(images),encoding='utf-8',newline='\n')
    notice=attribution(records)
    (HERE/'ASSET_NOTICE.md').write_text(notice,encoding='utf-8',newline='\n')
    (dest/'IMPERIA_COLD_WAR_NOTICE.md').write_text(notice,encoding='utf-8',newline='\n')
    for country in ['chl','bra','arg','shared']:
        keys=[k for k in images if k.startswith(country+'_')]
        sheet=Image.new('RGB',(4*237,((len(keys)+3)//4)*206+40),'#252c35');draw=ImageDraw.Draw(sheet)
        draw.text((10,8),'IMPERIA COLD WAR: '+country.upper()+' restored event photos',font=font(14),fill='white')
        for i,key in enumerate(keys):
            x=(i%4)*237+10;y=(i//4)*206+40
            draw.text((x,y),key,font=font(12),fill='white');sheet.paste(images[key],(x,y+22),images[key])
        sheet.save(review/(country+'-contact-sheet.jpg'),quality=92)
    # Donor-composed UI illustration, explicitly not a live engine screenshot.
    window=Image.new('RGBA',(581,427),(42,45,51,255))
    for file,position in [('event_report_top_win.dds',(0,0)),('event_report_bottom_win.dds',(0,221))]:
        path=root/'gfx/interface'/file
        if path.exists():window.alpha_composite(Image.open(path).convert('RGBA'),position)
    path=root/'gfx/interface/event_report_tileable_midsection.dds'
    if path.exists():window.alpha_composite(Image.open(path).convert('RGBA').resize((580,100)),(0,121))
    window.alpha_composite(images['chl_handover'],(5,226))
    path=root/'gfx/interface/event_pic_clip.dds'
    if path.exists():window.alpha_composite(Image.open(path).convert('RGBA'),(-3,256))
    path=root/'gfx/interface/event_option_entry.dds'
    if path.exists():
        for y in [220,267]:window.alpha_composite(Image.open(path).convert('RGBA'),(215,y))
    draw=ImageDraw.Draw(window);draw.text((160,72),'The Civilian Inauguration',font=font(17),fill='#1b1b1b')
    draw.text((31,127),'A civilian president takes office under a negotiated\nconstitutional settlement.',font=font(14),fill='#1b1b1b')
    draw.text((240,230),'Confirm the constitutional transfer',font=font(12),fill='white')
    draw.text((240,277),'Review the transition terms',font=font(12),fill='white')
    window.convert('RGB').save(review/'native-window-donor-composed.jpg',quality=95)
    manifest={'project':'IMPERIA COLD WAR','image_tool':'built-in image_gen','frame':FRAME,'frame_sha256':sha(root/FRAME),
              'native_gui':gui,'assets':records,'events':EVENT_ASSETS,'preview_type':'Donor-composed, not a live HOI4 screenshot.'}
    save_json(review/'manifest.json',manifest)
    return manifest

def patch_events(root=ROOT):
    root=Path(root);records=[];seen=set()
    files=sorted(p for p in (root/'events').glob('COLDWAR_*_1970*.txt') if re.match('COLDWAR_(CHL|BRA|ARG)_',p.name))
    pattern=re.compile(r'(country_event\s*=\s*\{\s*id\s*=\s*)([\w.]+)([\s\S]*?\bpicture\s*=\s*)([\w]+)')
    for path in files:
        before=path.read_bytes();text=before.decode('utf-8');assert not text.startswith('\ufeff')
        changes=[]
        def replace(m):
            event=m[2];sprite=picture_for(event);seen.add(event)
            changes.append({'event':event,'previous':m[4],'picture':sprite,'asset':EVENT_ASSETS[event]})
            return m[1]+event+m[3]+sprite
        after=pattern.sub(replace,text)
        strip=lambda s:re.sub(r'(\bpicture\s*=\s*)\w+',r'\1PHOTO',s)
        assert strip(text)==strip(after),'Only event pictures may change'
        if after!=text:path.write_bytes(after.encode('utf-8'))
        records.append({'file':path.relative_to(root).as_posix(),'before_sha256':hashlib.sha256(before).hexdigest(),
                        'after_sha256':sha(path),'only_picture_references_changed':True,'events':changes})
    assert seen==set(EVENT_ASSETS),(sorted(set(EVENT_ASSETS)-seen),sorted(seen-set(EVENT_ASSETS)))
    save_json(root/REVIEW/'integration.json',{'project':'IMPERIA COLD WAR','event_count':len(seen),'files':records})
    return len(seen)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');args=parser.parse_args()
    data=build_assets()
    count=patch_events() if args.install else 0
    print(json.dumps({'assets':len(data['assets']),'events_installed':count,'native_frame_unchanged':True}))
