# IMPERIA COLD WAR — Audit every Space Race event against complete native MD donor windows.
from pathlib import Path
import hashlib,json
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageChops
import validate as V
from event_art import FRAME,INSET,REPORT_SIZE,NEWS_SIZE,SOURCES

ROOT=V.ROOT;OUT=ROOT/'docs/design/space_race_1970/event_review'


def child(body,name):
    return next(v for k,op,v in body if isinstance(v,list) and V.first(v,'name')=='"'+name+'"')


def run():
    windows=V.first(V.parse((ROOT/'interface/eventwindow.gui').read_text(encoding='utf-8-sig')),'guiTypes')
    local=child(windows,'EventWindow');bottom=child(local,'bottom_Window');picture=child(bottom,'event_picture');options=child(bottom,'options_grid');entry=child(windows,'event_option_entry')
    news=child(windows,'EventWindow_News');news_top=child(news,'top_Window');news_picture=child(news_top,'event_picture');overlay=child(news_top,'event_picture_overlay')
    pos=lambda v:tuple(int(V.first(V.first(v,'position'),k)) for k in ['x','y'])
    V.check(pos(picture)==(5,5) and pos(options)==(215,-1),'Native local donor positions changed')
    V.check(V.first(options,'max_slots_horizontal')=='1' and V.first(V.first(options,'slotsize'),'width')=='300','Adjacent option-grid contract changed')
    option_art=Image.open(ROOT/'gfx/interface/event_option_entry.dds')
    V.check(pos(options)[0]+option_art.width<=int(V.first(V.first(local,'size'),'width')),'Native option-entry texture exceeds the donor window')
    V.check(V.first(V.first(entry,'size'),'width')=='300','Native option-entry layout changed')
    V.check(pos(news_picture)==pos(overlay)==(59,91),'News photograph and overlay are misaligned')
    native=Image.open(FRAME).convert('RGBA');V.check(native.size==REPORT_SIZE,'Native frame dimensions changed')
    sprites={V.first(v,'name').strip('"'):v for k,op,group in V.ASTS['interface/COLDWAR_space_race.gfx'] if k=='spriteTypes' for k2,op2,v in group if k2=='spriteType'}
    mask=Image.new('L',REPORT_SIZE,255);ImageDraw.Draw(mask).rectangle((19,6,198,155),fill=0)
    image_info=[]
    for key in SOURCES:
        for kind in ['report','news']:
            sprite=sprites['GFX_cw_sr_'+kind+'_'+key];path=ROOT/V.first(sprite,'texturefile').strip('"');im=Image.open(path).convert('RGBA')
            V.check(im.size==(REPORT_SIZE if kind=='report' else NEWS_SIZE),'Wrong native picture size')
            if kind=='report':
                for channel in ImageChops.difference(im,native).split():V.check(ImageChops.multiply(channel,mask).getbbox() is None,'Native frame pixels changed outside the photo inset')
                V.check(im.crop((19,6,199,156)).getchannel('A').getextrema()==(255,255),'Transparent hole or matte in local photo inset')
                bounds=im.getchannel('A').getbbox();V.check(pos(picture)[0]+bounds[2]<=pos(options)[0],'Photo overlaps the adjacent option buttons')
                V.check(pos(picture)[1]+bounds[3]<=int(V.first(V.first(bottom,'size'),'height')),'Photo extends outside native bottom window')
            else:
                V.check(im.getchannel('A').getextrema()==(255,255),'News image does not fill its photograph area')
                V.check(59+im.width<=int(V.first(V.first(news,'size'),'width')) and 91+im.height<253,'News image overlaps title or leaves window')
            image_info.append({'sprite':V.first(sprite,'name').strip('"'),'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    counts={'country_event':0,'news_event':0}
    for ident,body in V.EVENTS.items():
        if not ident.startswith(('cw_sr_report.','cw_sr_world.','cw_sr_crew.','cw_sr_ops.')):continue
        kind='news_event' if ident.startswith('cw_sr_world.') else 'country_event';counts[kind]+=1
        expected='GFX_cw_sr_report_' if kind=='country_event' else 'GFX_cw_sr_news_';pic=V.first(body,'picture')
        V.check(pic.startswith(expected) and pic in sprites,'Event bound to the wrong native image family: '+ident)
    OUT.mkdir(parents=True,exist_ok=True)
    # Geometry review made from MD's actual header, midsection, bottom and option texture.
    top=Image.open(ROOT/'gfx/interface/event_report_top_win.dds').convert('RGBA');mid=Image.open(ROOT/'gfx/interface/event_report_tileable_midsection.dds').convert('RGBA');foot=Image.open(ROOT/'gfx/interface/event_report_bottom_win.dds').convert('RGBA');option=Image.open(ROOT/'gfx/interface/event_option_entry.dds').convert('RGBA')
    canvas=Image.new('RGBA',(581,427),'#334047');canvas.alpha_composite(top,(0,0));canvas.alpha_composite(mid.resize((580,100)),(0,121));canvas.alpha_composite(foot,(0,221));canvas.alpha_composite(Image.open(ROOT/'gfx/interface/COLDWAR_space_race/report_mission-control.dds').convert('RGBA'),(5,226));canvas.alpha_composite(option,(215,220))
    d=ImageDraw.Draw(canvas);f=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12);white=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)
    d.text((72,72),'Federal Republic of Germany: Space Programme Authorised',font=f,fill='#121212');d.text((31,121),'The government has authorised the national space programme.\nEngineering work requires sustained weekly appropriations.',font=small,fill='#121212');d.text((265,235),'Acknowledge the report.',font=white,fill='white')
    canvas.convert('RGB').save(OUT/'local-news-frame.png')
    sheet=Image.new('RGB',(920,610),'#27323b');d=ImageDraw.Draw(sheet)
    for i,key in enumerate(SOURCES):
        x=(i%4)*230;y=(i//4)*305;d.text((x+10,y+8),key,font=f,fill='#dfdfd2');sheet.paste(Image.open(ROOT/f'gfx/interface/COLDWAR_space_race/report_{key}.dds').convert('RGBA'),(x+5,y+35),Image.open(ROOT/f'gfx/interface/COLDWAR_space_race/report_{key}.dds').convert('RGBA'));sheet.paste(Image.open(ROOT/f'gfx/interface/COLDWAR_space_race/news_{key}.dds').resize((215,83)),(x+5,y+210))
    sheet.save(OUT/'all-event-images.png')
    report={'project':'IMPERIA COLD WAR','status':'passed','checks':V.CHECKS,'events_checked':counts,'local_photo_inset':list(INSET),'native_frame_pixels_unchanged':True,'adjacent_options_clear':True,'images':image_info,'previews':'Native donor geometry review, not a live game capture','in_game_tested':False}
    Path(__file__).with_name('event_art_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='images'}))


if __name__=='__main__':run()
