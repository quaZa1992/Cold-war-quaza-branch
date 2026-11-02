# IMPERIA COLD WAR — Audit Cuba pictures against MD's complete native event window.
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image,ImageChops,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first
import event_art as A


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def named(rows,key):return next(v for k,op,v in rows if isinstance(v,list) and first(v,'name')=='"'+key+'"')
def pos(row):return tuple(int(first(first(row,'position'),k)) for k in ('x','y'))
def without_pictures(rows):return [(k,op,without_pictures(v) if isinstance(v,list) else v) for k,op,v in rows if k!='picture']


def main():
    checks=[]
    def check(value,label):
        assert value,label
        checks.append(label)
    backup=ROOT/json.loads((HERE/'event_frame_backup.json').read_text())['path']
    manifest=json.loads((backup/'BACKUP_MANIFEST.json').read_text())
    check(all(digest(backup/e['path'])==e['sha256'] for e in manifest['files']),'All pre-edit backup hashes match')
    local_gui=ROOT/'interface/eventwindow.gui';md_gui=A.MD/'interface/eventwindow.gui'
    gui=first(parse(local_gui.read_text(encoding='utf8')),'guiTypes');nativegui=first(parse(md_gui.read_text(encoding='utf8')),'guiTypes')
    local=named(gui,'EventWindow');native=named(nativegui,'EventWindow')
    check(local==native,'Complete native EventWindow remains identical to main MD')
    bottom=named(local,'bottom_Window');picture=named(bottom,'event_picture');options=named(bottom,'options_grid');entry=named(gui,'event_option_entry')
    check(pos(picture)==(5,5) and pos(options)==(215,-1),'Native picture and adjacent option positions')
    check(first(first(entry,'size'),'width')=='300' and first(options,'max_slots_horizontal')=='1','Native option width and slot limit')
    option_image=Image.open(ROOT/'gfx/interface/event_option_entry.dds')
    check(pos(options)[0]+option_image.width<=int(first(first(local,'size'),'width')),'Complete adjacent option texture fits the window')
    frame=Image.open(A.FRAME).convert('RGBA');mask=Image.new('L',frame.size,255)
    ImageDraw.Draw(mask).rectangle((19,6,198,155),fill=0)
    records=[]
    for key in A.SOURCES|A.REUSE:
        rel=A.REUSE.get(key,f'gfx/event_pictures/COLDWAR_CUB_1970/{key}.dds');path=A.resolve(rel);im=Image.open(path).convert('RGBA')
        check(im.size==(217,163),key+': native country-picture dimensions')
        for channel in ImageChops.difference(im,frame).split():
            check(ImageChops.multiply(channel,mask).getbbox() is None,key+': native frame channel unchanged')
        check(im.crop((19,6,199,156)).getchannel('A').getextrema()==(255,255),key+': opaque photo inset')
        bounds=im.getchannel('A').getbbox()
        check(pos(picture)[0]+bounds[2]<=pos(options)[0],key+': photo does not overlap options')
        check(pos(picture)[1]+bounds[3]<=int(first(first(bottom,'size'),'height')),key+': photo fits bottom window')
        records.append(dict(sprite=A.PREFIX+key,path=rel,sha256=digest(path)))
    bindings=[]
    for p in sorted((ROOT/'events').glob('COLDWAR_CUB_1970*.txt')):
        check(without_pictures(parse(p.read_text(encoding='utf8')))==without_pictures(parse((backup/p.relative_to(ROOT)).read_text(encoding='utf8'))),p.name+': gameplay AST identical to pre-edit backup')
        for k,op,event in parse(p.read_text(encoding='utf8')):
            if k!='country_event' or first(event,'hidden')=='yes':continue
            ident=first(event,'id');pic=first(event,'picture')
            check(pic in {e['sprite'] for e in records},ident+': correct framed country-event family')
            bindings.append(dict(event=ident,picture=pic))
    old_runtime=json.loads((backup/'tools/cuba_1970/integration_manifest.json').read_text())
    comment_only_files=[]
    for e in old_runtime['owned']+old_runtime['shared_integrations']:
        if not e['path'].startswith('events/'):
            path=ROOT/e['path']
            if digest(path)!=e['sha256']:
                before=(backup/e['path']).read_text(encoding='utf-8-sig');after=path.read_text(encoding='utf-8-sig')
                if path.suffix=='.yml':
                    content=lambda text:[line for line in text.splitlines() if not line.lstrip().startswith('#')]
                    check(content(before)==content(after),e['path']+': localization values unchanged')
                else:
                    check(parse(before)==parse(after),e['path']+': gameplay unchanged after comment refresh')
                comment_only_files.append(e['path'])
            else:
                check(True,e['path']+': non-event runtime unchanged')
    check(not (ROOT/'interface/COLDWAR_CUB_1970_eventpictures.gfx').read_bytes().startswith(b'\xef\xbb\xbf'),'New GFX registry has no BOM')
    A.REVIEW.mkdir(parents=True,exist_ok=True)
    # Native assets and donor positions: this is a geometry review, not a live capture.
    canvas=Image.new('RGBA',(581,427),(48,58,65,255))
    for name,xy in [('event_report_top_win',(0,0)),('event_report_bottom_win',(0,221))]:
        canvas.alpha_composite(Image.open(ROOT/f'gfx/interface/{name}.dds').convert('RGBA'),xy)
    mid=Image.open(ROOT/'gfx/interface/event_report_tileable_midsection.dds').convert('RGBA');canvas.alpha_composite(mid.resize((580,100)),(0,121))
    photo=Image.open(A.OUT/'signing.dds').convert('RGBA');canvas.alpha_composite(photo,(5,226))
    for y in (220,267):canvas.alpha_composite(option_image.convert('RGBA'),(215,y))
    clip=Image.open(ROOT/'gfx/interface/event_pic_clip.dds').convert('RGBA');canvas.alpha_composite(clip,(-3,256))
    draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
    draw.text((181,73),'Cayo Blanco Agreement',font=font,fill='#161616')
    draw.text((31,124),'Cuba has presented the Cayo Blanco Agreement proposal.\nThe German Democratic Republic may accept or decline.',font=small,fill='#161616')
    draw.text((255,235),'Accept the Agreement',font=font,fill='white');draw.text((255,282),'Decline the Proposal',font=font,fill='white')
    canvas.convert('RGB').save(A.REVIEW/'native-window.png')
    sheet=Image.new('RGB',(920,410),'#303a41');d=ImageDraw.Draw(sheet)
    for i,e in enumerate(records):
        x=(i%4)*230;y=(i//4)*205;d.text((x+8,y+8),e['sprite'].removeprefix(A.PREFIX),font=font,fill='white');im=Image.open(A.resolve(e['path'])).convert('RGBA');sheet.paste(im,(x+5,y+35),im)
    sheet.save(A.REVIEW/'all-framed-pictures.png')
    current=json.loads((HERE/'integration_manifest.json').read_text())
    check(all(digest(ROOT/e['path'])==e['sha256'] for e in current['owned']+current['shared_integrations']+current.get('binary_assets',[])),'Current integration manifest matches every runtime file and packaged asset')
    report=dict(project='IMPERIA COLD WAR',status='pass',checks=len(checks),visible_country_events=len(bindings),pictures=len(records),
                native_size=[217,163],photo_inset=[19,6,180,150],native_frame_pixels_unchanged=True,adjacent_options_clear=True,
                gameplay_ast_unchanged=True,all_prior_non_event_runtime_unchanged=not comment_only_files,all_prior_non_event_gameplay_unchanged=True,
                comment_only_followup=comment_only_files,backup=str(backup.relative_to(ROOT)).replace('\\','/'),backup_files=len(manifest['files']),
                native_window_preview='Native MD assets and exact donor positions, not a live HOI4 screenshot.',fresh_engine_test=False,
                preserved_native_mechanics_evidence='The previous 221 native assertions remain a record of the pre-picture build; this follow-up proves all gameplay ASTs and non-event runtime remain identical.',
                bindings=bindings,assets=records,runtime=current['owned']+current['shared_integrations'])
    (HERE/'EVENT_FRAME_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:report[k] for k in ('status','checks','visible_country_events','pictures','native_frame_pixels_unchanged','adjacent_options_clear','gameplay_ast_unchanged')}))


if __name__=='__main__':main()
