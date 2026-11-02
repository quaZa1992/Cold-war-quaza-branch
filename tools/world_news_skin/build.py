# IMPERIA COLD WAR — Compact World Ledger with original MD news interaction.
"""Build/install the approved layout. No import-time writes or event changes."""
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import re
import struct
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
ARCHIVES=Path('E:/MDColdWar_Backups/Codex_Test_Archives')
PAPER='gfx/interface/event_news_bg.dds'
GFX='interface/ICW_news_skin.gfx'
GUI='interface/eventwindow.gui'
MARK='# IMPERIA COLD WAR — World Ledger world-news integration.\n'
GUI_MARK='# IMPERIA COLD WAR — Custom world-news layout integration; native MD event windows retained.\n'
SHADOW='gfx/interface/popup_window/popup_window_shadow_bd_x79_y107.dds'
LAYOUT=json.loads((HERE/'source/world_ledger_compact_geometry.json').read_text(encoding='utf-8'))
SIZE=tuple(LAYOUT['window'])
GEOMETRY=dict(window=list(SIZE),title=LAYOUT['title'],picture=LAYOUT['picture'],description=LAYOUT['description'],options=[80,-1,300,30],options_scope='Original native bottom_Window positioning',option_slots=[300,47])

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def native_dds(im):
    im=im.convert('RGBA');h=[124,0x100f,im.height,im.width,im.width*4,0,0]+[0]*11
    h += [32,0x41,0,32,0xff0000,0xff00,0xff,0xff000000,0x1000,0,0,0,0]
    result=b'DDS '+struct.pack('<31I',*h)+im.tobytes('raw','BGRA')
    assert Image.open(io.BytesIO(result)).convert('RGBA').tobytes()==im.tobytes()
    return result

def window_span(text,name='EventWindow_News',kind='containerWindowType'):
    match=re.search(r'\bname\s*=\s*"'+re.escape(name)+r'"',text);assert match,name
    start=text.rfind(kind,0,match.start());assert start>=0,(name,kind)
    opening=text.index('{',start)
    depth=0
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[{}]',text[opening:]):
        c=token.group()
        if c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return start,opening+token.end()
    raise ValueError('Unclosed native window: '+name)

def gui_block():
    # Keep the complete native hierarchy and option list. Only visual fields vary.
    donor=(HERE/'source/md_203_news_window.txt').read_text(encoding='utf-8')
    a,b=window_span(donor);text=donor[a:b]
    def change(name,kind,fields):
        nonlocal text
        a,b=window_span(text,name,kind);node=text[a:b]
        for pattern,replacement in fields:
            node,count=re.subn(pattern,lambda match:replacement,node,count=1)
            assert count==1,(name,pattern)
        text=text[:a]+node+text[b:]
    change('event_picture','iconType',[(r'position\s*=\s*\{[^}]*\}','position = { x = 59 y = 158 }')])
    change('event_picture_overlay','iconType',[(r'position\s*=\s*\{[^}]*\}','position = { x = 59 y = 158 }')])
    change('Title','instantTextBoxType',[
        (r'position\s*=\s*\{[^}]*\}','position = { x = 35 y = 94 }'),
        (r'font\s*=\s*"[^"]*"','font = "icw_news_title"'),
        (r'maxHeight\s*=\s*\d+','maxHeight = 52'),
        (r'text\s*=\s*"[^"]*"','text = ""'),
    ])
    a,b=window_span(text,'Title','instantTextBoxType')
    text=text[:b-1]+'\n                scrollbarType = standardtext_slider\n            '+text[b-1:]
    change('Description','instantTextBoxType',[
        (r'position\s*=\s*\{[^}]*\}','position = { x = 52 y = 224 }'),
        (r'font\s*=\s*"[^"]*"','font = "icw_news_body"'),
        (r'maxHeight\s*=\s*\d+','maxHeight = 145'),
        (r'text\s*=\s*"[^"]*"','text = ""'),
    ])
    change('btn_minimize','buttonType',[
        (r'position\s*=\s*\{[^}]*\}','position = { x = 489 y = 18 }'),
        (r'spriteType\s*=\s*"[^"]*"','spriteType = "GFX_icw_news_minimize"'),
    ])
    return text.replace('containerWindowType = {','containerWindowType = {\n        # IMPERIA COLD WAR — Compact World Ledger, native MD dragging and option bindings.',1)


def patch_gui(source):
    text=source.decode('utf-8-sig');start,end=window_span(text)
    result=text[:start]+gui_block()+text[end:]
    if not result.startswith(GUI_MARK):result=GUI_MARK+result
    for name in ('EventWindow','EventWindow_Operative','EventWindow_leader','event_option_entry'):
        a,b=window_span(text,name);c,d=window_span(result,name)
        assert text[a:b]==result[c:d],name
    return result.encode('utf-8')

def paper():
    # Generated from the immutable approved fragment by render_ledger.cjs.
    # Only the masthead, paper, rules, photo mount and shadows are baked.
    im=Image.open(HERE/'source/world_ledger_compact_background.png').convert('RGBA')
    assert im.size==SIZE
    return im

def minimize():
    im=Image.new('RGBA',(24,24));d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,22,22),radius=2,fill=(239,239,239,255),outline=(164,164,164,255))
    d.line((7,12,16,12),fill=(65,65,65,255),width=2)
    return im

def build(source=None):
    source=(ROOT/GUI).read_bytes() if source is None else source
    spec=importlib.util.spec_from_file_location('icw_news_fonts',HERE/'fonts.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    fonts,declarations,font_records=module.build(native_dds)
    gfx=(MARK+'spriteTypes = {\n'
         'spriteType = { name = "GFX_icw_news_minimize" texturefile = "gfx/interface/ICW_news/minimize.dds" }\n}\n'+declarations)
    files={GUI:patch_gui(source),PAPER:native_dds(paper()),GFX:gfx.encode('utf-8'),
           'gfx/interface/ICW_news/minimize.dds':native_dds(minimize()),**fonts}
    report=dict(project='IMPERIA COLD WAR',design='World Ledger',geometry=GEOMETRY,source_gui_sha256=sha(source),fonts=font_records,
                approved_input_sha256=sha((HERE/'source/world_ledger_approved.html').read_bytes()),
                background_source_sha256=sha((HERE/'source/world_ledger_compact_background.png').read_bytes()),
                native_interaction_donor_sha256=sha((HERE/'source/md_203_news_window.txt').read_bytes()),
                native_shadow=dict(path=SHADOW,sha256=sha((GAME/SHADOW).read_bytes())),
                removed_visible_fields=['place','date','photo caption','Illustrative reconstruction','example event prose'],
                preserved=['real event title','real event picture','real event description','news_event_grid','native option list','all non-news event windows','all event scripts','shared native option entry'],
                files={p:sha(v) for p,v in files.items()})
    return files,report

def backup_and_install(files):
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    archive=ARCHIVES/('world_ledger_install_'+stamp)
    assert archive.resolve().is_relative_to(ARCHIVES.resolve())
    archive.mkdir(parents=True,exist_ok=False);old={}
    for rel in files:
        p=ROOT/rel;old[rel]=sha(p.read_bytes()) if p.exists() else None
        if p.exists():
            q=archive/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
            assert sha(q.read_bytes())==old[rel]
    dump(archive/'manifest.json',dict(project='IMPERIA COLD WAR',source_root=str(ROOT),before=old))
    for rel,raw in files.items():
        p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    return archive,old

def validate(files,report):
    for rel,raw in files.items():
        assert (ROOT/rel).read_bytes()==raw,rel
        if rel.endswith(('.gui','.gfx')):
            assert raw.startswith(b'# IMPERIA COLD WAR') and not raw.startswith(b'\xef\xbb\xbf'),rel
        if rel.endswith('.dds'):
            h=struct.unpack('<31I',raw[4:128]);assert h[22:26]==(0xff0000,0xff00,0xff,0xff000000),rel
    text=files[GUI].decode('utf-8');a,b=window_span(text);news=text[a:b]
    assert news.count('name = "Title"')==1 and news.count('name = "Description"')==1
    donor=(HERE/'source/md_203_news_window.txt').read_text(encoding='utf-8')
    for name,kind in [('bottom_Window','containerWindowType'),('news_event_grid','gridBoxType')]:
        a,b=window_span(news,name,kind);c,d=window_span(donor,name,kind)
        assert news[a:b]==donor[c:d],name
    assert 'size = { width = 528 height = 595 }' in news
    assert 'moveable = yes' in news and 'spriteType ="GFX_event_news_bg"' in news
    assert 'clipping = yes' not in news
    assert 'GFX_icw_news_paper' not in files[GFX].decode('utf-8')
    for name in ('Title','Description'):
        a,b=window_span(news,name,'instantTextBoxType');text_control=news[a:b]
        assert 'scrollbarType = standardtext_slider' in text_control,name
        assert 'alwaystransparent = yes' not in text_control,name
    for forbidden in ('JERUSALEM','1986','Illustrative','reconstruction','dateline','WEST BANK'):
        assert forbidden not in news,forbidden
    return dict(project='IMPERIA COLD WAR',status='PASS',
                scope='Source, encoding, deterministic assets and retained native bindings',
                geometry=report['geometry'],files=report['files'],native_md_size_restored=True,native_option_container_and_news_grid_restored=True,background_mouse_passthrough_removed=True,native_ui_tested=False)

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--install',action='store_true');g.add_argument('--check',action='store_true')
    g.add_argument('--export',type=Path,metavar='PRIVATE_DIRECTORY')
    args=p.parse_args();files,report=build()
    if args.export:
        target=args.export.resolve();base=Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime').resolve()
        assert target.is_relative_to(base) and target!=base
        for rel,raw in files.items():
            q=target/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
        dump(target/'world_ledger_build.json',report)
        print(json.dumps(dict(project='IMPERIA COLD WAR',status='EXPORTED',target=str(target),files=len(files))));return
    if args.install:
        archive,before=backup_and_install(files)
        dump(HERE/'install_receipt.json',dict(project='IMPERIA COLD WAR',archive=str(archive),before=before,installed=report['files']))
    result=validate(files,report);dump(HERE/'VALIDATION.json',result)
    for rel,raw in files.items():
        if rel.endswith(('.dds','.fnt')):
            dump(ROOT/(rel+'.provenance.json'),dict(project='IMPERIA COLD WAR',asset=rel,sha256=sha(raw),
                 source_record='tools/world_news_skin/NOTICE.md',source_generator='tools/world_news_skin/build.py',
                 format='BGRA8 DDS' if rel.endswith('.dds') else 'BMFont text',
                 licence_or_permission='See source record; no project-wide redistribution licence asserted'))
    dump(HERE/'BUILD_REPORT.json',report)
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='PASS',files=len(files),native_ui_tested=False)))

if __name__=='__main__':main()
