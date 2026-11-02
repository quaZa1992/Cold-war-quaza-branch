# IMPERIA COLD WAR — Native translation of the approved CIA and KGB dossier
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from typography import build_fonts
from runtime import PAGE

WIDTH,HEIGHT=790,794
SIDES={
 'usa':dict(tag='USA',paper='#f0ebdc',cover='#aa9270',edge='#706246',ink='#34342f',line='#c2bcaa',stamp='#8c3730',active='#ded7c3',button='#3d4b48',source='gfx/interface/operatives/agencies/agency_logo_usa.dds'),
 'sov':dict(tag='SOV',paper='#eae4d5',cover='#846054',edge='#6e3330',ink='#39352f',line='#beb3a0',stamp='#8f3029',active='#ddcdbb',button='#6d3832',source='gfx/interface/ideas/russia/SOV_kgb_idea.dds'),
}


def font(name,size):return ImageFont.truetype('C:/Windows/Fonts/'+name,size)


def tracked(draw,xy,value,typeface,fill,spacing=1):
    x,y=xy
    for char in value:
        draw.text((x,y),char,font=typeface,fill=fill)
        x+=typeface.getlength(char)+spacing


def make_art(root,here,mark,write):
    folder=root/'gfx/interface/superpower_dossier';folder.mkdir(parents=True,exist_ok=True)
    sprites=[];records=[]
    def save(key,im,button=False):
        im.save(folder/(key+'.dds'))
        sprites.append(f'spriteType = {{ name = GFX_icsd_{key} texturefile = "gfx/interface/superpower_dossier/{key}.dds"'+(' effectFile = "gfx/FX/buttonstate.lua"' if button else '')+' }')
    for side,p in SIDES.items():
        src=root/p['source'];logo=Image.open(src).convert('RGBA')
        if side=='usa':logo=logo.crop((0,0,116,119))
        logo=logo.crop(logo.getchannel('A').getbbox())
        im=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0));d=ImageDraw.Draw(im)
        # Same two-layer cover and narrow paper margin as the approved browser file.
        d.rounded_rectangle((0,0,726 if side=='usa' else 656,53),radius=4,fill=p['edge'])
        d.rectangle((0,38,789,793),fill=p['cover'],outline='#8e7958')
        d.rectangle((13,70,776,780),fill=p['paper'],outline='#d6cebb')
        if side=='sov':d.rectangle((13,70,776,74),fill='#7a342d')
        d.line((25,71,25,779),fill='#d9c3b1')
        tracked(d,(18,10),'EXECUTIVE FILE' if side=='usa' else 'SPECIAL FILE',font('cour.ttf',11),'#f5e8c9',1.2)
        tracked(d,(486 if side=='usa' else 444,10),'UNITED STATES / CIA' if side=='usa' else 'SOVIET UNION / KGB',font('cour.ttf',11),'#f5e8c9',1.2)
        tracked(d,(21,47),'FOREIGN INTELLIGENCE' if side=='usa' else 'FIRST CHIEF DIRECTORATE',font('cour.ttf',11),p['ink'] if side=='usa' else '#f7e6cd',1)
        # Paperclip, ink stamp and watermark are part of each independent country image.
        bounds=(170,170) if side=='usa' else (115,186)
        factor=min(bounds[0]/logo.width,bounds[1]/logo.height)
        watermark=logo.resize((round(logo.width*factor),round(logo.height*factor)),Image.Resampling.LANCZOS)
        watermark.putalpha(watermark.getchannel('A').point(lambda a:round(a*0.035)))
        im.alpha_composite(watermark,(578 if side=='usa' else 610,345))
        bounds=(74,80) if side=='usa' else (55,86);factor=min(bounds[0]/logo.width,bounds[1]/logo.height)
        header=logo.resize((round(logo.width*factor),round(logo.height*factor)),Image.Resampling.LANCZOS)
        im.alpha_composite(header,(42+(74-header.width)//2,87+(86-header.height)//2))
        heading_x=133 if side=='usa' else 115
        tracked(d,(heading_x,94),'CENTRAL INTELLIGENCE AGENCY' if side=='usa' else 'COMMITTEE FOR STATE SECURITY',font('segoeui.ttf',11),p['ink'],1.35 if side=='usa' else 1.05)
        d.text((heading_x,112),'Soviet Affairs' if side=='usa' else 'American Affairs',font=font('georgia.ttf',25 if side=='usa' else 23),fill=p['ink'])
        d.text((heading_x,149),'Directorate of Intelligence' if side=='usa' else 'First Chief Directorate',font=font('cour.ttf',11),fill='#66675e')
        stamp=Image.new('RGBA',(145,82),(0,0,0,0));sd=ImageDraw.Draw(stamp)
        sd.rectangle((1,1,143,80),outline=p['stamp']);sd.rectangle((4,4,140,77),outline=p['stamp'])
        if side=='usa':
            tracked(sd,(17,16),'TOP SECRET',font('cour.ttf',14),p['stamp'],1)
        else:
            tracked(sd,(33,12),'STRICTLY',font('cour.ttf',12),p['stamp'],1)
            tracked(sd,(43,28),'SECRET',font('cour.ttf',12),p['stamp'],1)
        sd.line((13,49,130,49),fill=p['stamp'])
        tracked(sd,(24 if side=='usa' else 16,58),'EYES ONLY' if side=='usa' else 'PERSONAL COPY',font('cour.ttf',10),p['stamp'],0.9)
        stamp=stamp.rotate(7 if side=='usa' else -4,expand=True,resample=Image.Resampling.BICUBIC)
        im.alpha_composite(stamp,(611 if side=='usa' else 604,88))
        clip=Image.new('RGBA',(24,57),(0,0,0,0));cd=ImageDraw.Draw(clip)
        cd.rounded_rectangle((5,2,20,51),radius=8,outline='#8e9390',width=3)
        cd.rounded_rectangle((9,6,16,46),radius=4,outline='#dce0d9',width=1)
        im.alpha_composite(clip.rotate(-7 if side=='usa' else 8,expand=True,resample=Image.Resampling.BICUBIC),(397 if side=='usa' else 499,54))
        d.line((41,183,752,183),fill=p['ink']);d.line((41,213,752,213),fill=p['ink'])
        d.text((41,190),'TO: THE PRESIDENT' if side=='usa' else 'TO: THE GENERAL SECRETARY',font=font('cour.ttf',11),fill=p['ink'])
        d.text((354,190),'FOREIGN AFFAIRS / SPECIAL FILE',font=font('cour.ttf',11),fill=p['ink'])
        d.text((705,190),'COPY 01',font=font('cour.ttf',11),fill=p['ink'])
        d.line((14,262,775,262),fill=p['line']);d.line((223,262,223,744),fill=p['line']);d.line((41,744,752,744),fill=p['line'])
        d.text((41,750),'CONTROLLED DISTRIBUTION' if side=='usa' else 'RETURN TO REGISTRY',font=font('cour.ttf',11),fill='#66675e')
        tiny=Image.new('RGBA',(97,27),(0,0,0,0));td=ImageDraw.Draw(tiny)
        td.rectangle((1,1,95,25),outline=p['stamp']);tracked(td,(8,7),'FILE COPY' if side=='usa' else 'REGISTERED',font('cour.ttf',10),p['stamp'],0.8)
        im.alpha_composite(tiny.rotate(-4 if side=='usa' else 4,expand=True,resample=Image.Resampling.BICUBIC),(656,742))
        save('dossier_'+side,im)
        launcher=Image.new('RGBA',(46,46),(0,0,0,0));logo.thumbnail((36,39),Image.Resampling.LANCZOS)
        launcher.alpha_composite(logo,((46-logo.width)//2,(46-logo.height)//2));save('launcher_'+side,launcher)
        primary=Image.new('RGBA',(238,37),p['button']);save('primary_'+side,primary,True)
        selected=Image.new('RGBA',(174,72),p['active']);ImageDraw.Draw(selected).line((1,0,1,71),fill=p['stamp'],width=3);save('selected_'+side,selected)
        for state,label in enumerate(('ACTIVE','PROPOSAL SENT','ACCEPTED','DECLINED','SUSPENDED','RECORDED')):
            status=Image.new('RGBA',(142,29),(0,0,0,0));sd=ImageDraw.Draw(status)
            width=round(font('cour.ttf',11).getlength(label))+15
            sd.rectangle((1,2,width,25),outline=p['stamp']);sd.text((8,8),label,font=font('cour.ttf',11),fill=p['stamp'])
            save(f'status_{side}_{state}',status.rotate(2,resample=Image.Resampling.BICUBIC))
        records.append(dict(project='IMPERIA COLD WAR',source=p['source'],source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),original_author='Unknown individual artist; existing Millennium Dawn / IMPERIA COLD WAR asset',licence_or_permission='Unknown asset-specific terms; upstream ownership retained',modifications='CIA first frame or KGB emblem cropped and composed in an original native rendering of the approved dossier design.'))
    for key,size in [('row',(174,72)),('tab',(204,36)),('action',(238,37)),('page',(46,24)),('more',(91,24)),('modal_button',(210,37)),('response',(408,24)),('index_button',(174,24)),('category',(58,24))]:
        im=Image.new('RGBA',size,(0,0,0,0));d=ImageDraw.Draw(im)
        if key=='row':d.line((0,71,173,71),fill='#c8c0ab')
        elif key!='response':
            d.rectangle((0,0,size[0]-1,size[1]-1),fill='#e5dfce' if key in ('action','modal_button') else '#e2dbc9',outline='#c2bcaa')
        save(key,im,True)
    for side,p in SIDES.items():
        im=Image.new('RGBA',(204,36),p['paper']);d=ImageDraw.Draw(im);d.rectangle((0,0,203,35),outline=p['line'])
        d.line((1,35,202,35),fill=p['paper'])
        if side=='sov':d.line((0,0,203,0),fill=p['stamp'],width=2)
        save('tab_active_'+side,im)
    close=Image.new('RGBA',(24,24),(0,0,0,0));d=ImageDraw.Draw(close);d.line((6,6,18,18),fill='#665b4b',width=1);d.line((6,18,18,6),fill='#665b4b',width=1);save('close',close,True)
    foldericon=Image.new('RGBA',(46,46),(0,0,0,0));d=ImageDraw.Draw(foldericon);d.rectangle((7,7,25,13),fill='#aa9270');d.rectangle((5,12,41,39),fill='#d2bd90',outline='#625234',width=1)
    foldericon.save(folder/'file_icon.dds');sprites.append('spriteType = { name = GFX_decision_icsd_file texturefile = "gfx/interface/superpower_dossier/file_icon.dds" }')
    sprites += ['spriteType = { name = GFX_icsd_treaty_spirit texturefile = \"gfx/interface/ideas/diplomacy/international_treaty2.dds\" }', 'spriteType = { name = GFX_icwt_country texturefile = \"gfx/event_pictures/generic/elections/political_deal.dds\" }', 'spriteType = { name = GFX_icwt_news texturefile = \"gfx/event_pictures/americas/north_america/united_states - USA/news_american_defence_treaty.dds\" }']
    for source in ('gfx/interface/ideas/diplomacy/international_treaty2.dds','gfx/event_pictures/generic/elections/political_deal.dds','gfx/event_pictures/americas/north_america/united_states - USA/news_american_defence_treaty.dds'):
        raw=(root/source).read_bytes();size=Image.open(root/source).size
        records.append(dict(project='IMPERIA COLD WAR',source=source,source_sha256=hashlib.sha256(raw).hexdigest(),dimensions=list(size),original_author='Unknown individual artist; existing Millennium Dawn / IMPERIA COLD WAR asset',licence_or_permission='Unknown asset-specific terms; upstream ownership retained',modifications='Reused intact. Country photo retains its native 217 x 163 outer frame and 180 x 150 inset; news image uses its separate native news viewport.' if 'event_pictures' in source else 'Reused intact for treaty spirits and dossier previews.'))
    gfx=mark+'spriteTypes = {\n'+'\n'.join(sprites)+'\n}\n'+build_fonts(root,mark)+'\n'
    write('interface/ICW_superpower_dossier.gfx',gfx)
    (here/'art_notice.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',assets=records,approved_reference='superpower-briefings.html, with intelligence-dossiers.html and the original CIA/KGB approved snapshots preserved, 24 October 2026',event_geometry=dict(donor='interface/eventwindow.gui',country_picture=[217,163],country_photo_inset=[180,150],country_picture_position=[5,5],country_option_position=[215,-1],country_option_width=300,country_option_slots=47,news_picture=[397,153],news_window=[528,595],news_picture_position=[59,91],news_title_position=[35,253],news_title_width=444,verification='Donor blocks and adjacent options inspected; source assets reused byte-for-byte. Dossier compositions are not native event screenshots.'),typography=dict(source='Local Windows Courier New, Segoe UI and Georgia fonts',original_author='Original font designers and Microsoft / respective rights holders',licence_or_permission='Asset-specific redistribution terms unknown; source TTF files are not copied',modifications='Rendered glyph atlases for private dossier bitmap fonts'),original_work='Native folder, paper, clip, stamps and controls drawn from the approved code-native interface. No global font definitions modified.'),indent=2)+'\n',encoding='utf-8')


def txt(name,x,y,value,width,height=20,font='icsd_body'):
    return f'instantTextboxType = {{ name = "{name}" position = {{ x={x} y={y} }} text = "{value}" font = "{font}" maxWidth = {width} maxHeight = {height} fixedsize = yes format = left alwaystransparent = yes }}'


def icon(name,x,y,sprite):return f'iconType = {{ name = "{name}" position = {{ x={x} y={y} }} spriteType = GFX_icsd_{sprite} alwaystransparent = yes }}'


def btn(name,x,y,value,sprite='action',typeface='icsd_button',tip=None,shortcut=None):
    return f'buttonType = {{ name = "{name}" position = {{ x={x} y={y} }} quadTextureSprite = GFX_icsd_{sprite} buttonFont = {typeface} buttonText = "{value}" clicksound = click_default'+(f' pdx_tooltip = {tip}' if tip else '')+(f' shortcut = {shortcut}' if shortcut else '')+' }'


def build_ui(write,loc,defined,mark):
    from treaty_ui import build
    build(write,loc,defined,mark)


def localisation(loc,defined):
    values={'icsd_file_index':'FILE INDEX','icsd_responsible':'Responsible','icsd_record_type':'Source',
            'icsd_doc_kicker':'COUNTERPART ACTIVITY',
            'icsd_review':'Records reviewed weekly','icsd_response_options':'RESPONSE OPTIONS / [icsd_response_name]',
            'icsd_header_date':'',
            'icsd_response_choose':'CHOOSE COUNTRY','icsd_response_country':'[?icsd_response_target.GetName]',
            'icsd_tab_1':'Field reports','icsd_tab_2':'Diplomatic offers','icsd_tab_3':'Current commitments',
            'icsd_route_kicker':'DIPLOMATIC ACTION','icsd_back':'Return to file','icsd_more':'More...','icsd_basic':'Basic',
            'icsd_lend':'Send lend-lease','icsd_volunteers':'Send volunteers','icsd_attache':'Send military attache',
            'icsd_row_actor_usa':'USA','icsd_row_actor_sov':'USSR','icsd_row_actor_other':'RECEIVED',
            'icsd_known_1':'Connection confirmed; quantities unavailable.',
            'icsd_known_2':'Volunteer forces are present in the recipient country.',
            'icsd_known_3':'A military attache is assigned to the recipient.',
            'icsd_known_4':'Existing sanctions imposed by the provider.',
            'icsd_known_5':'An improved trade agreement is recorded.',
            'icsd_select_prompt':'No document is selected. Choose a record from the file index.',
            'icsd_no_records':'No records available in this section.'}
    for key,value in values.items():loc(key,value)
    for i in range(1,13):loc(f'icsd_action_tip_{i}',f'Go to [?icsd_response_target.GetName]. Right-click the country to open diplomacy.\n\n$icsd_route_{i}$')
    result=[]
    for i in range(PAGE):
        loc(f'icsd_row_mark_{i}',f'ANNEX [?icsd_r{i}_number|0] / [icsd_row_{i}_actor]')
        result.append(defined(f'icsd_row_{i}_actor',[(f'check_variable = {{ icsd_r{i}_actor = USA.id }}','icsd_row_actor_usa'),(f'check_variable = {{ icsd_r{i}_actor = SOV.id }}','icsd_row_actor_sov')],'icsd_row_actor_other'))
    result.append(defined('icsd_response_name',[('check_variable = { icsd_response_target > 0 }','icsd_response_country')],'icsd_response_choose'))
    result.append(defined('icsd_route_title',[(f'check_variable = {{ icsd_route = {i} }}','icsd_'+key) for i,key in enumerate(('lend','volunteers','attache','money','sanctions','trade','invest','assist','party_action','politics','aid','subsidy'),1)]))
    return result
