# IMPERIA COLD WAR — Orbital Atlas and Mission Control presentation.
from pathlib import Path
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

W,H=1240,1040
FONT_PATH=Path('C:/Windows/Fonts/bahnschrift.ttf')


def save_dds(path,im):
    data=BytesIO();im.save(data,format='DDS');raw=data.getvalue()
    if path.exists() and path.read_bytes()==raw:return
    temporary=path.with_suffix(path.suffix+'.cw_sr_tmp');temporary.write_bytes(raw);temporary.replace(path)


# IMPERIA COLD WAR — Approved native interface assembly.
# IMPERIA COLD WAR — International operational cooperation.
def build(c):
    globals().update({k:c[k] for k in ['ROOT','HERE','DATA','PROGRAMMES','IDS','ASSETS','OUTPUTS','loc','write','num','sv','av','cv','block_if','effect','clamp','guard','var']})
    widgets=[];triggers=[];clicks=[];properties=[];sprites=[]
    def texture(name,im,frames=1):
        path=f'gfx/interface/COLDWAR_space_race/{name}.dds'
        (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
        save_dds(ROOT/path,im.convert('RGBA'));OUTPUTS.append(path)
        sprites.append(f'spriteType = {{ name = "GFX_cw_sr_{name}" texturefile = "{path}" noOfFrames = {frames} }}\n')
    sizes=set()
    def text(name,x,y,w,h,key,size=13,condition=None,tip=None,color=None):
        key=loc(name,key) if not key.startswith('cw_sr_') else key
        widgets.append(f'instantTextBoxType = {{ name = "{name}" position = {{ x = {x} y = {y} }} font = "cw_sr_ui_{size}" text = "{key}" maxWidth = {w} maxHeight = {h} fixedsize = yes format = left '+(f'pdx_tooltip = "{tip}" ' if tip else 'alwaysTransparent = yes ')+'}\n')
        if condition:triggers.append(f'{name}_visible = {{ {condition} }}\n')
    def icon(name,x,y,sprite,condition=None):
        widgets.append(f'iconType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "GFX_cw_sr_{sprite}" alwaysTransparent = yes }}\n')
        if condition:triggers.append(f'{name}_visible = {{ {condition} }}\n')
    def button(name,x,y,w,h,label,action,condition=None,enabled=None,tip=None,style='control',size=13):
        sizes.add((style,w,h))
        key=label if label.startswith('cw_sr_') else loc(name,label)
        font_name=f'cw_sr_dark_{size}' if style=='primary' else f'cw_sr_muted_{size}' if style=='locked' else f'cw_sr_ui_{size}'
        widgets.append(f'buttonType = {{ name = "{name}" position = {{ x = {x} y = {y} }} spriteType = "GFX_cw_sr_{style}_{w}_{h}" buttonText = "{key}" buttonFont = "{font_name}" clicksound = click_default '+(f'pdx_tooltip = "{tip}" ' if tip else '')+('shortcut = "ESCAPE" ' if name=='cw_sr_close' else '')+'}\n')
        dismiss='' if name=='cw_sr_policy_cycle' or name.startswith('cw_sr_policy_option_') else 'clr_country_flag = cw_sr_policy_open\n'
        clicks.append(f'{name}_click = {{ if = {{ limit = {{ {guard()} }} {dismiss}{action} cw_sr_refresh = yes cw_sr_touch = yes }} }}\n')
        if condition:triggers.append(f'{name}_visible = {{ {condition} }}\n')
        if enabled:triggers.append(f'{name}_click_enabled = {{ {enabled} }}\n')
    tab=lambda n:cv('cw_sr_tab','=',n)+' NOT = { has_country_flag = cw_sr_requirements_open }'
    side='OR = { '+cv('cw_sr_tab','=',1)+' '+cv('cw_sr_tab','=',4)+' '+cv('cw_sr_tab','=',5)+' }'
    def sidebar(name,x,y,w,h,key,size=13,tip=None):text(name,x,y,w,h,key,size,side,tip)
    from orbital_atlas import controls
    regions,side=controls(c,locals())
    # Full-width briefing, catalogue, record and news views match the reference tabs.
    text('cw_sr_brief_title',26,288,1175,32,'National Starting Position',23,tab(2))
    text('cw_sr_brief_text',26,336,1175,95,'[CW_SR_Starting]',15,tab(2))
    text('cw_sr_brief_caps_title',26,454,1160,23,'ESTABLISHED NATIONAL CAPABILITIES · JANUARY 1970',12,tab(2))
    text('cw_sr_brief_caps',26,492,1160,100,'[CW_SR_Inherited]',14,tab(2))
    text('cw_sr_brief_infra_title',26,624,555,25,'Inherited infrastructure & experience',19,tab(2))
    text('cw_sr_brief_infra',26,669,555,200,'[CW_SR_Infrastructure]',15,tab(2))
    text('cw_sr_brief_focus_title',651,624,555,25,'Strategic opportunities',19,tab(2))
    text('cw_sr_brief_focus',651,669,555,200,'[CW_SR_Opportunities]',15,tab(2))
    button('cw_sr_brief_programmes',26,926,380,36,'Review National Programmes',sv('cw_sr_tab',3)+sv('cw_sr_filter_national',1)+sv('cw_sr_filter_region',0)+sv('cw_sr_filter_kind',0)+sv('cw_sr_list_page',0),tab(2),size=14)
    # List views share twelve native slots; filtered rows are packed without gaps.
    for t,title,intro in [(3,'Programme Catalogue','Historical programmes, studied proposals and plausible long-term extensions.'),(4,'Development & National Allocation','Weekly appropriations support paid engineering work and corrective investigations.'),(5,'Flight Manifest','Qualified hardware, launches, operating campaigns and safe Earth recovery.'),(6,'History & Programme Record','Accepted missions and the permanent record of national and international achievements.')]:
        text('cw_sr_view_title_'+str(t),26,286,850,33,title,23,tab(t))
        text('cw_sr_view_intro_'+str(t),26,333,840,42,intro,14,tab(t))
    text('cw_sr_records_firsts',26,387,1180,23,'WORLDWIDE ACHIEVEMENTS  >',12,tab(6),'cw_sr_world_first_register')
    # IMPERIA COLD WAR — Weekly budget quick adjustments.
    text('cw_sr_budget',26,388,500,27,'Weekly development ceiling: §H$[?cw_sr_budget|3]bn§!',19,tab(4),'cw_sr_budget_tt')
    for name,x,label,delta in [('down_large',550,'-0.50',-.5),('down',630,'-0.05',-.05),('up',710,'+0.05',.05),('up_large',790,'+0.50',.5)]:
        enabled=cv('cw_sr_budget','>',0) if delta<0 else cv('cw_sr_budget','<',11.53846)
        button('cw_sr_budget_'+name,x,385,70,29,label,av('cw_sr_budget',delta)+clamp('cw_sr_budget',0,11.53846),tab(4),enabled,tip='cw_sr_budget_tt',size=12)
    button('cw_sr_filter_region',26,386,410,29,'Region: [CW_SR_FilterRegion]  >',av('cw_sr_filter_region',1)+'modulo_variable = { cw_sr_filter_region = 16 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_kind',456,386,410,29,'Type: [CW_SR_FilterKind]  >',av('cw_sr_filter_kind',1)+'modulo_variable = { cw_sr_filter_kind = 4 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_ready',886,386,320,29,'[CW_SR_ReadyFilter]',av('cw_sr_filter_ready',1)+'modulo_variable = { cw_sr_filter_ready = 2 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_national',1016,290,190,29,'All Programmes',sv('cw_sr_filter_national',0)+sv('cw_sr_list_page',0),tab(3)+' '+cv('cw_sr_filter_national','=',1),size=12)
    list_visible='OR = { '+' '.join(cv('cw_sr_tab','=',t) for t in [3,4,5,6])+' } NOT = { has_country_flag = cw_sr_requirements_open }'
    for slot in range(12):
        full='OR = { '+cv('cw_sr_tab','=',3)+' '+cv('cw_sr_tab','=',6)+' }'
        compact='OR = { '+cv('cw_sr_tab','=',4)+' '+cv('cw_sr_tab','=',5)+' }'
        for suffix,width,vis in [('wide',1180,full),('side',850,compact)]:
            button(f'cw_sr_slot_{slot}_{suffix}',26,433+slot*43,width,40,'',sv('cw_sr_selected','cw_sr_slot_'+str(slot))+block_if(full,sv('cw_sr_tab',1)+'cw_sr_selected_map = yes\n'),list_visible+' '+vis+' '+cv('cw_sr_slot_'+str(slot),'>',0),style='row',size=13)
            text(f'cw_sr_slot_text_{slot}_{suffix}',40,436+slot*43,width-28,34,f'[CW_SR_Slot_{slot}]',12,list_visible+' '+vis+' '+cv('cw_sr_slot_'+str(slot),'>',0))
    button('cw_sr_list_prev',26,965,110,30,'< Previous',av('cw_sr_list_page',-1)+clamp('cw_sr_list_page',0,6),list_visible,cv('cw_sr_list_page','>',0),size=12)
    button('cw_sr_list_next',150,965,110,30,'Next >',av('cw_sr_list_page',1)+clamp('cw_sr_list_page',0,6),list_visible,cv('cw_sr_list_count','>','cw_sr_list_end'),size=12)
    text('cw_sr_list_count',286,972,580,22,'[?cw_sr_list_count|0] programmes · Page [?cw_sr_list_page_display|0]',12,list_visible)
    text('cw_sr_list_empty',26,452,820,96,'[CW_SR_EmptyList]',16,list_visible+' '+cv('cw_sr_list_count','=',0))
    # Actual national bulletins, including the supplied country-specific landing art.
    # IMPERIA COLD WAR — Recent news with a visible retention policy.
    text('cw_sr_news_title',26,286,1175,29,'International News Service',23,tab(7))
    text('cw_sr_news_retention',26,316,1175,17,'Recent bulletins: [?cw_sr_news_count|0] · Routine reports: 180 days · Successes and disasters: 365 days',12,tab(7))
    text('cw_sr_news_selector',26,340,1000,27,'[CW_SR_Selected_name]',17,tab(7))
    button('cw_sr_news_prev',1054,329,70,29,'<','cw_sr_previous_bulletin = yes',tab(7),cv('cw_sr_news_count','>',1),size=12)
    button('cw_sr_news_next',1138,329,70,29,'>','cw_sr_next_bulletin = yes',tab(7),cv('cw_sr_news_count','>',1),size=12)
    news=tab(7)+' '+cv('cw_sr_view_report','>',0)
    text('cw_sr_news_headline',120,378,1000,42,'[CW_SR_NewsTitle]',24,news)
    for key in ['mission-control','station','mars','soviet-lunar','french-lunar','saudi-lunar','us-mars','soviet-mars']:
        icon('cw_sr_news_image_'+key,120,435,'article_'+key,news+' '+f'cw_sr_picture_{key.replace("-","_")} = yes')
    text('cw_sr_news_body',120,841,1000,130,'[CW_SR_NewsBody]',16,news)
    button('cw_sr_news_read',120,980,1000,35,'Read Mission Report','cw_sr_replay_bulletin = yes',news,size=14,style='primary')
    text('cw_sr_news_empty',26,422,1175,120,'No recent space bulletins are available for [ROOT.GetName]. Older reports leave this archive automatically. Completed programmes and national achievements remain in Records.',16,tab(7)+' '+cv('cw_sr_view_report','=',0))
    # Full-width, readable eligibility and effects instead of an undifferentiated tooltip.
    details='has_country_flag = cw_sr_requirements_open'
    icon('cw_sr_requirements_bg',0,264,'wide_bg',details)
    text('cw_sr_requirements_title',26,283,1180,32,'[CW_SR_Selected_name]',23,details)
    button('cw_sr_readiness_mode',26,330,280,32,'Mission requirements',sv('cw_sr_details_mode',0),details,size=13)
    button('cw_sr_effects_mode',320,330,280,32,'National effects',sv('cw_sr_details_mode',1),details,size=13)
    button('cw_sr_hardware_mode',614,330,280,32,'Research & hardware',sv('cw_sr_details_mode',2),details,size=13)
    button('cw_sr_risks_mode',908,330,280,32,'Mission risks',sv('cw_sr_details_mode',3),details,size=13)
    text('cw_sr_requirements_body',26,385,575,566,'[CW_SR_Selected_Checklist]',13,details+' '+cv('cw_sr_details_mode','=',0))
    text('cw_sr_national_effects_body',26,385,575,566,'cw_sr_national_effects',14,details+' '+cv('cw_sr_details_mode','=',1))
    text('cw_sr_hardware_body',26,385,575,566,'[CW_SR_Selected_Hardware]',14,details+' '+cv('cw_sr_details_mode','=',2))
    text('cw_sr_risks_body',26,385,575,566,'[CW_SR_Selected_Risks]',14,details+' '+cv('cw_sr_details_mode','=',3))
    text('cw_sr_modifiers_heading',644,385,560,23,'MISSION PROBABILITY MODIFIERS',15,details)
    text('cw_sr_modifiers_body',644,418,560,365,'[CW_SR_ModifierTable]',13,details)
    text('cw_sr_rewards_heading',644,805,560,23,'PROGRAMME REWARDS',15,details)
    text('cw_sr_rewards_body',644,838,560,165,'[CW_SR_VisibleRewards]',13,details)
    button('cw_sr_requirements_close',26,964,300,31,'Return to programme','clr_country_flag = cw_sr_requirements_open',details,size=13)
    # IMPERIA COLD WAR — Footer retains programme states without a duplicate date.
    text('cw_sr_state_legend',480,1025,736,14,'§GAvailable§!   §TActive§!   §HCompleted / heritage§!   §gLocked§!   §RInvestigation§!',11)
    # Native popup choices appear above the card controls, as in the reference select.
    popup=side+' has_country_flag = cw_sr_policy_open'
    for policy,label in enumerate(['Standard Programme','Extended Assurance','Accelerated Schedule','Reduced Expenditure']):
        choice=''.join(block_if(cv('cw_sr_selected','=',n)+' NOT = { '+cv(var(n,'state'),'=',4)+' } NOT = { '+cv(var(n,'state'),'=',6)+' }',sv(var(n,'policy'),policy)) for n in range(1,85))+'clr_country_flag = cw_sr_policy_open\n'
        button('cw_sr_policy_option_'+str(policy),920,883+policy*28,300,28,label,choice,popup,style='control',size=12)
    # IMPERIA COLD WAR — A duplicate widget name also overwrites its localisation.
    from collections import Counter
    import re
    widget_names=Counter(re.findall(r'\bname\s*=\s*"([^"]+)"',''.join(widgets)))
    assert not [name for name,count in widget_names.items() if count>1], 'Duplicate native widgets: '+str([name for name,count in widget_names.items() if count>1])
    gui='guiTypes = { containerWindowType = { name = "cw_sr_main_window" position = { x = 0 y = 0 } size = { width = 1240 height = 1040 } orientation = center origo = center moveable = yes click_to_front = yes clipping = no background = { name = "cw_sr_background" quadTextureSprite = "GFX_cw_sr_panel" }\n'+''.join(widgets)+'} }\n'
    write('interface/COLDWAR_space_race.gui',gui)
    scripted='scripted_gui = { cw_sr_main = { context_type = player_context window_name = "cw_sr_main_window" dirty = global.cw_sr_dirty ai_enabled = { always = no } visible = { '+guard()+' has_country_flag = cw_sr_open }\ntriggers = {\n'+''.join(triggers)+'}\neffects = {\n'+''.join(clicks)+'}\nproperties = {\n'+''.join(properties)+'}\n} }\n'
    write('common/scripted_guis/COLDWAR_space_race_gui.txt',scripted)
    extra_definitions(c,regions)
    native_graphics(texture,sizes)
    from cooperation_ui import graphics as operations_graphics
    operations_graphics(texture)
    write('interface/COLDWAR_space_race_command.gfx','spriteTypes = {\n'+''.join(sprites)+'}\n'+font_graphics())


# IMPERIA COLD WAR — Native image and control atlases.
def native_graphics(texture,sizes):
    from illustrations import programme_art, planet
    for kind in ['ground','rocket','satellite','crew','station','probe','lander']:
        texture('programme_'+kind,programme_art(kind,FONT_PATH))
    from orbital_atlas import backgrounds
    backgrounds(globals(),texture)
    for style,w,h in sorted(sizes):
        im=Image.new('RGBA',(w*3,h),(0,0,0,0));dr=ImageDraw.Draw(im)
        colors={'control':['#23343d','#34474d','#263237'],'nav':['#1b272d','#33413c','#111a1f'],'scale':['#142129','#33413c','#263237'],'node':['#0c1a22','#2a3937','#182327'],'row':['#142028','#24373c','#172026'],'primary':['#a89260','#c1ad77','#344146'],'locked':['#344146']*3,'text':['#1d292e','#2a3b40','#1d292e']}[style]
        for f,color in enumerate(colors):
            dr.rectangle((f*w,0,(f+1)*w-1,h-1),fill=color,outline='#4e646b' if style!='primary' else '#a99b72')
            if style=='node':dr.rectangle((f*w,0,f*w+1,h-1),fill='#83a8ae')
            if style=='row':dr.line((f*w,h-1,(f+1)*w-1,h-1),fill='#34484f')
        texture(f'{style}_{w}_{h}',im,3)
    im=Image.new('RGBA',(44,44),'#192326');dr=ImageDraw.Draw(im);dr.rectangle((0,0,43,43),outline='#7d846e');dr.ellipse((7,15,36,29),outline='#d0b77c',width=1);dr.ellipse((14,6,28,37),outline='#d0b77c',width=1);dr.ellipse((19,19,24,24),fill='#d0b77c');texture('seal',im)
    for t in range(1,8):
        im=Image.new('RGBA',(14,14),(0,0,0,0));dr=ImageDraw.Draw(im);color='#b0c0c0'
        if t==1:dr.ellipse((0,4,13,10),outline=color);dr.ellipse((4,0,10,13),outline=color);dr.ellipse((6,6,8,8),fill=color)
        elif t==2:
            dr.line([(0,4),(7,0),(13,4),(0,4)],fill=color);dr.line((0,13,13,13),fill=color)
            for x in [2,6,11]:dr.line((x,6,x,11),fill=color)
        elif t==3:
            dr.line((2,2,11,11),fill=color);dr.line((2,11,11,2),fill=color)
            for x,y in [(0,0),(10,0),(5,5),(0,10),(10,10)]:dr.rectangle((x,y,x+3,y+3),outline=color)
        elif t==4:
            for y,x in [(2,4),(7,9),(12,5)]:dr.line((0,y,13,y),fill=color);dr.rectangle((x-1,y-1,x+1,y+1),fill='#1b272d',outline=color)
        elif t==5:dr.polygon([(4,10),(6,3),(13,0),(11,7)],outline=color);dr.line((4,10,1,13),fill=color);dr.ellipse((8,3,10,5),outline=color)
        elif t==6:dr.rectangle((3,0,11,12),outline=color);dr.line((5,4,9,4),fill=color);dr.line((5,7,9,7),fill=color);dr.line((1,3,1,13,10,13),fill=color)
        else:dr.ellipse((5,5,8,8),fill=color);dr.arc((1,1,12,12),-60,60,fill=color);dr.arc((1,1,12,12),120,240,fill=color);dr.line((6,9,4,13),fill=color);dr.line((7,9,9,13),fill=color)
        texture('nav_icon_'+str(t),im)
    for name,color in [('progress_cyan','#91c1c5'),('progress_gold','#d0b77c')]:
        im=Image.new('RGBA',(300*51,4),'#344448');dr=ImageDraw.Draw(im)
        for f in range(51):
            if f:dr.rectangle((f*300,0,f*300+int(f*6)-1,3),fill=color)
        texture(name,im,51)
    # IMPERIA COLD WAR — Original flight-manifest surfaces and state badges.
    from crew_ui import graphics as crew_graphics
    crew_graphics(texture)
    from orbital_atlas import maps
    maps(globals(),texture)
    images={'mission-control':'apollo13-mission-control-colourised-v1.png','station':'skylab-original.jpg','mars':'viking-first-surface-colourised-v1.png','soviet-lunar':'soviet-lunar-landing-user-v1.png','french-lunar':'french-lunar-landing-user-v1.png','saudi-lunar':'saudi-lunar-landing-user-v1.png','us-mars':'us-mars-landing-user-v1.png','soviet-mars':'soviet-mars-landing-user-v1.png'}
    for key,file in images.items():texture('article_'+key,ImageOps.fit(Image.open(ASSETS/file),(1000,386),method=Image.Resampling.LANCZOS,centering=(.5,.12) if key.endswith(('lunar','mars')) and key!='mars' else (.5,.5)))
    # Replacement icon in the former Antarctica slot, with the same 24px footprint.
    icon=Image.new('RGBA',(24,24),(0,0,0,0));dr=ImageDraw.Draw(icon);dr.ellipse((1,7,22,17),outline='#bfa45a',width=2);dr.ellipse((7,1,17,22),outline='#bfa45a',width=1);dr.ellipse((9,9,14,14),fill='#bfa45a');texture('ledger_orbit',icon)


def font_graphics():
    out='bitmapfonts = {\n'
    for size in [11,12,13,14,15,16,17,19,21,23,24,28,29]:
        name=f'cw_sr_ui_{size}';font=ImageFont.truetype(str(FONT_PATH),size)
        cell=size+12;cols=16;chars=[0,8,9,10,13,29,31]+list(range(32,256))+[8211,8212,8216,8217,8230,65279];rows=math.ceil(len(chars)/cols);atlas=Image.new('RGBA',(cols*cell,rows*cell),(255,255,255,0));dr=ImageDraw.Draw(atlas)
        lines=[f'info face="Bahnschrift" size={size} bold=0 italic=0 unicode=1',f'common lineHeight={size+3} base={size} scaleW={atlas.width} scaleH={atlas.height} pages=1 packed=0',f'page id=0 file="{name}.dds"',f'chars count={len(chars)}']
        for idx,ch in enumerate(chars):
            # The engine can request control/terminator glyphs after every string.
            # Never rasterise NUL as Bahnschrift's visible missing-character box.
            if ch<32 or ch==65279:
                lines.append(f'char id={ch} x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={round(font.getlength(" ")) if ch==9 else 0} page=0 chnl=15')
                continue
            char=chr(ch);box=font.getbbox(char);x=idx%cols*cell;y=idx//cols*cell;advance=round(font.getlength(char))
            dr.text((x-box[0]+2,y-box[1]+2),char,font=font,fill=(255,255,255,255))
            lines.append(f'char id={ch} x={x} y={y} width={max(1,box[2]-box[0]+4)} height={max(1,box[3]-box[1]+4)} xoffset={box[0]-2} yoffset={box[1]-2} xadvance={advance} page=0 chnl=15')
        directory=ROOT/'gfx/fonts/COLDWAR_space_race';directory.mkdir(parents=True,exist_ok=True)
        save_dds(directory/(name+'.dds'),atlas);(directory/(name+'.fnt')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        OUTPUTS.extend([f'gfx/fonts/COLDWAR_space_race/{name}.dds',f'gfx/fonts/COLDWAR_space_race/{name}.fnt'])
        out+=f'bitmapfont = {{ name = "{name}" path = "gfx/fonts/COLDWAR_space_race/{name}" color = 0xffdce4df textcolors = {{ H = {{ 208 183 124 }} G = {{ 169 198 173 }} T = {{ 145 193 197 }} g = {{ 164 183 188 }} R = {{ 212 149 132 }} }} }}\n'
        if size in [13,14]:out+=f'bitmapfont = {{ name = "cw_sr_dark_{size}" path = "gfx/fonts/COLDWAR_space_race/{name}" color = 0xff182026 }}\n'
        if size==13:out+=f'bitmapfont = {{ name = "cw_sr_muted_{size}" path = "gfx/fonts/COLDWAR_space_race/{name}" color = 0xff9caaaa }}\n'
    return out+'}\n'


# IMPERIA COLD WAR — Live readiness, reports and safe navigation.
# IMPERIA COLD WAR — International operational cooperation.
def extra_definitions(c,regions):
    def define(name,entries,fallback):
        return 'defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+condition+' } localization_key = '+key+' }\n' for condition,key in entries)+'text = { localization_key = '+fallback+' } }\n'
    from readiness import definitions
    from orbital_atlas import definitions as atlas_definitions
    from programme_states import build as state_definitions
    # IMPERIA COLD WAR — Crew agreements and country-seat presentation.
    from crew import build as crew_definitions
    # IMPERIA COLD WAR — Operational contracts share the native command room.
    from cooperation import build as operations_definitions
    defs=definitions(c)+atlas_definitions(c)+state_definitions(c)+crew_definitions(c)+operations_definitions(c)+define('CW_SR_Region',regions,'cw_sr_region_name_1')
    ground='OR = { '+' '.join(cv('cw_sr_selected','=',n) for n,p in enumerate(PROGRAMMES,1) if p['region']=='ground')+' }'
    defs+=define('CW_SR_SuccessLabel',[(ground,loc('cw_sr_acceptance_chance','Estimated programme\nacceptance chance'))],loc('cw_sr_flight_chance','Estimated full\nmission success'))
    defs+=define('CW_SR_CrewSummary',[(ground,loc('cw_sr_ground_crew','Ground programme · No flight crew'))],loc('cw_sr_flight_crew','Crew [?cw_sr_view_crew|0] · Flight remaining [?cw_sr_view_days|0] days'))
    defs+=define('CW_SR_BlockedAction',[(cv('cw_sr_view_state','=',s),loc('cw_sr_blocked_'+str(s),label)) for s,label in [(1,'Weekly funding required'),(4,'Mission in flight'),(6,'Investigation in progress')]],loc('cw_sr_blocked_requirements','Requirements not met'))
    for n,p in enumerate(PROGRAMMES,1):
        defs+=define('CW_SR_Readiness_'+str(n),[(f'cw_sr_p{n}_launch_allowed = yes',loc('cw_sr_ready_launch','§GReady for mission authorisation§!')),(f'cw_sr_p{n}_start_allowed = yes',loc('cw_sr_ready_development','§GReady for development§!')),(cv(var(n,'state'),'=',0),loc('cw_sr_needs_requirements','§gSupporting capabilities or funding required§!'))],loc(f'cw_sr_row_progress_{n}',f'§g[CW_SR_Status_{n}] · [?{var(n,"work")}|0]% development§!'))
        loc(f'cw_sr_p{n}_row',p['name']+'\n[CW_SR_ProgrammeState_'+str(n)+']')
    defs+=define('CW_SR_ReadyFilter',[(cv('cw_sr_filter_ready','=',1),loc('cw_sr_ready_only','Show: Ready to begin'))],loc('cw_sr_ready_all','Show: All readiness levels'))
    next_entries=[]
    for n in range(1,85):
        next_entries.extend([(cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_launch_allowed = yes',loc('cw_sr_next_launch','§GNEXT STEP: Authorise the mission.§!\nThe full launch appropriation is paid when you authorise departure.')),(cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_start_allowed = yes',loc('cw_sr_next_start','§GNEXT STEP: Authorise development.§!\nEngineering advances with paid weekly funding. Adjust your ceiling in Budget.'))])
    for state,message in [(1,'NEXT STEP: Maintain weekly funding.\nQualification and paid development must both finish before departure.'),(2,'NEXT STEP: Resume development when funding is available.\nExisting paid work is retained.'),(3,'NEXT STEP: Review the programme requirements.\nCheck mission funds, supporting systems, unpaid costs and launch opportunities.'),(4,'MISSION IN FLIGHT\nWait for the mission report. Departure probabilities are already fixed.'),(5,'PROGRAMME OPERATIONAL\nWeekly operating costs maintain this capability. Further missions may be available.'),(6,'INVESTIGATION IN PROGRESS\nCorrective engineering requires weekly funding before missions can resume.')]:
        next_entries.append((cv('cw_sr_view_state','=',state),loc('cw_sr_next_state_'+str(state),message)))
    defs+=define('CW_SR_NextStep',next_entries,loc('cw_sr_next_blocked','NEXT STEP: Open Programme requirements.\nDevelop the required supporting capabilities and provide sufficient funding.'))
    defs+=define('CW_SR_EmptyList',[(cv('cw_sr_tab','=',3),loc('cw_sr_empty_catalogue','No programmes match these filters.\nChoose another region or switch to All readiness levels.')),(cv('cw_sr_tab','=',4),loc('cw_sr_empty_budget','No programmes currently need development funding.\nChoose a programme on the Space Map and authorise development.')),(cv('cw_sr_tab','=',5),loc('cw_sr_empty_flights','No flight hardware is ready yet.\nComplete funded development and qualification before authorising a mission.'))],loc('cw_sr_empty_records','No national missions have been recorded yet.\nCompleted missions and achievements will appear here.'))
    defs+=define('CW_SR_Region_Brief',[(cv('cw_sr_region','=',r),loc(f'cw_sr_region_brief_{r}',region['description'].split('. ')[0]+'.')) for r,region in enumerate(DATA['regions'],1)],'cw_sr_region_brief_1')
    defs+=define('CW_SR_FilterRegion',[(cv('cw_sr_filter_region','=',r),f'cw_sr_region_name_{r}') for r in range(1,16)],loc('cw_sr_all_regions','All regions'))
    defs+=define('CW_SR_NationalFilter',[(cv('cw_sr_filter_national','=',1),loc('cw_sr_national_only','National programmes & entry options'))],loc('cw_sr_all_programmes','All programmes'))
    defs+=define('CW_SR_FilterKind',[(cv('cw_sr_filter_kind','=',i),loc('cw_sr_filter_kind_'+str(i),name)) for i,name in enumerate(['All programme types','Historical programmes','Studied or cancelled','Plausible extensions'])],'cw_sr_filter_kind_0')
    for field,profile_field in [('Agency','agency'),('Infrastructure','inheritedInfrastructure'),('Opportunities','strategicFocus'),('Inherited','capabilities')]:
        entries=[]
        for p in DATA['profiles']:
            value=p.get(profile_field,[] if field!='Agency' else 'National Space Commission')
            if field=='Agency' and p['id']=='CUSTOM':value='National Space Institutions'
            if isinstance(value,list):value=(' · ' if field=='Inherited' else '\n\n').join(v.replace('-',' ').title() if field=='Inherited' else v for v in value) or 'No inherited space infrastructure.'
            key=loc(f'cw_sr_profile_{p["id"]}_{field}',value)
            if p['id']!='CUSTOM':entries.append((f'original_tag = {p["id"]}',key))
        defs+=define('CW_SR_'+field,entries,'cw_sr_profile_CUSTOM_'+field)
    defs+=define('CW_SR_Primary',[(cv('cw_sr_view_state','=',s),loc('cw_sr_primary_'+str(s),label)) for s,label in [(0,'Authorise Development'),(1,'Suspend Development'),(2,'Resume Development'),(3,'Authorise Mission'),(4,'Mission Under Way'),(5,'Authorise New Mission'),(6,'Investigation Under Way'),(7,'Restart Development')]],'cw_sr_primary_0')
    for field in ['Kind','Region']:
        defs+=define('CW_SR_Selected_'+field,[(cv('cw_sr_selected','=',n),loc(f'cw_sr_p{n}_{field}',p['kind'].upper()+' PROGRAMME' if field=='Kind' else next(r['name'] for r in DATA['regions'] if r['id']==p['region']))) for n,p in enumerate(PROGRAMMES,1)],f'cw_sr_p47_{field}')
    for slot in range(12):defs+=define('CW_SR_Slot_'+str(slot),[(cv('cw_sr_slot_'+str(slot),'=',n),f'cw_sr_p{n}_row') for n in range(1,85)],loc('cw_sr_slot_empty',''))
    # Reports use immutable programme-specific localisation, not a shared latest-mission name.
    for field,ending in [('NewsTitle','t'),('NewsBody','d')]:
        entries=[]
        for n,p in enumerate(PROGRAMMES,1):
            for stage in c['STAGES']:
                condition=cv('cw_sr_selected','=',n)+' '+cv(var(n,'last_report'),'=',stage)
                if stage==8:
                    special=[('SOV',8001),('FRA',8002),('SAU',8003)] if 'lunar-landing' in p['grants'] else [('USA',8004),('SOV',8005)] if p['id']=='mars-crewed-landing' else []
                    for tag,ident in special:entries.append((condition+' original_tag = '+tag,f'cw_sr_report.{ident}.{ending}'))
                entries.append((condition,f'cw_sr_report.{c["stage_id"](n,stage)}.{ending}'))
        defs+=define('CW_SR_'+field,entries,loc('cw_sr_no_bulletin','No mission bulletin.'))
    # IMPERIA COLD WAR — Event targets use the native localisation scope syntax.
    for i,milestone in enumerate(DATA['milestones'],1):
        history=next((h for h in DATA['historicalFirsts'] if h['milestoneId']==milestone['id']),None)
        fallback=loc('cw_sr_first_status_'+str(i),milestone['title']+': '+((next(p['name'] for p in DATA['profiles'] if p['id']==history['country'])+' · '+history['date']) if history else 'Unclaimed'))
        entries=[(f'has_event_target = cw_sr_first_holder_{i}',loc('cw_sr_first_holder_'+str(i),milestone['title']+f': [cw_sr_first_holder_{i}.GetName]'))]
        defs+=define('CW_SR_First_'+str(i),entries,fallback)
    loc('cw_sr_world_first_register','\n\n'.join('[CW_SR_First_'+str(i)+']' for i in range(1,len(DATA['milestones'])+1)))
    loc('cw_sr_starting_tooltip','[CW_SR_Starting]')
    loc('cw_sr_ledger_name','SPACE RACE')
    loc('cw_sr_ledger_tt','Space Race')
    loc('cw_sr_ledger_delayed','Open the Space Race command room. Review national programmes, launch readiness, weekly appropriations and the leading space powers.')
    loc('cw_sr_selected_detail','[CW_SR_Selected_detail]')
    loc('cw_sr_policy_explanation','Standard: planned engineering cost and calendar.\nAssurance: +18% cost and calendar; up to +2.5 pp departure and +4 pp objective chance.\nAccelerated: +25% cost, -15% calendar; up to -4.5 pp departure and -3.5 pp objective chance.\nReduced: -20% cost, +35% calendar; up to -2.5 pp departure and -2 pp objective chance.\nSelect a policy for future paid engineering work.')
    loc('cw_sr_budget_tt','Weekly development ceiling, shared between active programmes and investigations. Operating charges are additional and paid first.\nLast weekly engineering spending: $[?cw_sr_week_spent|3]bn.\nTotal programme spending: $[?cw_sr_spent|2]bn.\nUnpaid operating charges remain payable and block new launches.\n[CW_SR_Leader_Benefit]')
    loc('cw_sr_risk_tt','Estimates include funded qualification, maintained supporting programmes, relevant flight experience, interrupted funding, completed investigations, research analysis and space leadership.\nFull success requires departure and accepted mission objectives. Probabilities are frozen at departure.\nResearch data: +0.02 pp objective chance per point, capped at +2 pp.\nInvestigations require 3, 6 or 12 funded months, with weekly corrective-engineering charges.\nCrew losses remain possible.')
    path=ROOT/'common/scripted_localisation/COLDWAR_space_race_localisation.txt'
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(defs)
    # IMPERIA COLD WAR — Expire news before copying the selected report.
    effects='';refresh='cw_sr_news_cleanup = yes\n'
    selected_report='OR = { '+' '.join('AND = { '+cv('cw_sr_selected','=',n)+' '+cv(var(n,'last_report'),'>',0)+' }' for n in range(1,85))+' }'
    refresh+=block_if(cv('cw_sr_tab','=',7)+' '+cv('cw_sr_news_count','>',0)+' NOT = { '+selected_report+' }','cw_sr_next_bulletin = yes\n')
    refresh+=sv('cw_sr_analysis_current','cw_sr_science')+'multiply_variable = { cw_sr_analysis_current = 0.02 }\n'+clamp('cw_sr_analysis_current',0,2)
    effects+=effect('cw_sr_open_from_ledger',block_if('is_ai = no IMP_is_1970_scenario = yes','cw_sr_initialize = yes\ncw_sr_seed_world = yes\ncw_sr_windows = yes\ncw_sr_rank = yes\nset_country_flag = cw_sr_open\nclr_country_flag = open_MD_countrymissilesview\n'+''.join(sv(x,0) for x in ['var_open_MD_antarctica_gui','var_open_MD_space_gui','var_open_MD_PMC_gui','var_open_MD_CT_gui','var_open_MD_UN_gui','var_open_MD_cyber_gui'])+sv('cw_sr_tab',1)+'cw_sr_selected_map = yes\ncw_sr_refresh = yes\ninternational_systems_update = yes\ncw_sr_touch = yes\n'))
    for n,p in enumerate(PROGRAMMES,1):
        body=sv('cw_sr_view_report',var(n,'last_report'))+sv('cw_sr_view_flight',num(p['flightMonths']))+sv('cw_sr_view_upkeep_m',num(p['upkeepB']*1000/52))+sv('cw_sr_view_crew',p['crewSize'])+sv('cw_sr_view_policy',var(n,'policy'))
        body+=sv('cw_sr_view_engineering',var(n,'months'))+f'divide_variable = {{ cw_sr_view_engineering = {p["durationMonths"]} }}\nmultiply_variable = {{ cw_sr_view_engineering = 100 }}\n'+clamp('cw_sr_view_engineering',0,100)
        body+=sv('cw_sr_view_remaining',100)+f'subtract_from_variable = {{ cw_sr_view_remaining = {var(n,"work")} }}\n'+sv('cw_sr_view_unfunded','cw_sr_view_remaining')+f'multiply_variable = {{ cw_sr_view_unfunded = {num(p["totalCostB"])} }}\ndivide_variable = {{ cw_sr_view_unfunded = 100 }}\nmultiply_variable = {{ cw_sr_view_remaining = {p["durationMonths"]} }}\ndivide_variable = {{ cw_sr_view_remaining = 100 }}\n'
        key=p.get('imageKey','mission-control');picture={'station':2,'mars':3}.get(key,1)
        body+=sv('cw_sr_view_picture',1)+block_if(cv(var(n,'last_report'),'=',8),sv('cw_sr_view_picture',picture))
        if 'lunar-landing' in p['grants']:
            for tag,pic in [('SOV',4),('FRA',5),('SAU',6)]:body+=block_if(cv(var(n,'last_report'),'=',8)+' original_tag = '+tag,sv('cw_sr_view_picture',pic))
        if p['id']=='mars-crewed-landing':
            for tag,pic in [('USA',7),('SOV',8)]:body+=block_if(cv(var(n,'last_report'),'=',8)+' original_tag = '+tag,sv('cw_sr_view_picture',pic))
        refresh+=block_if(cv('cw_sr_selected','=',n),body)
    for policy,time,cost in [(1,1.18,1.18),(2,.85,1.25),(3,1.35,.8)]:
        refresh+=block_if(cv('cw_sr_view_policy','=',policy),f'multiply_variable = {{ cw_sr_view_remaining = {time} }}\nmultiply_variable = {{ cw_sr_view_unfunded = {cost} }}\n')
    refresh+=block_if('has_country_flag = cw_sr_leader','multiply_variable = { cw_sr_view_upkeep_m = 0.95 }\n')
    refresh+=sv('cw_sr_engineering_frame','cw_sr_view_engineering')+'divide_variable = { cw_sr_engineering_frame = 2 }\n'+av('cw_sr_engineering_frame',1)+sv('cw_sr_funding_frame','cw_sr_view_progress')+'divide_variable = { cw_sr_funding_frame = 2 }\n'+av('cw_sr_funding_frame',1)
    for kind,selector,count in [('nav','cw_sr_tab',7),('scale','cw_sr_system',3),('node','cw_sr_region',15)]:
        for i in range(1,count+1):refresh+=sv(f'cw_sr_{kind}_frame_{i}',1)+block_if(cv(selector,'=',i),sv(f'cw_sr_{kind}_frame_{i}',2))
    refresh+=block_if('OR = { check_variable = { cw_sr_tab = 8 } check_variable = { cw_sr_tab = 9 } }',sv('cw_sr_nav_frame_1',2))
    # IMPERIA COLD WAR — Read-only crew shares and frozen flight roster.
    refresh+='cw_sr_mission_control_refresh = yes\ncw_sr_crew_refresh = yes\ncw_sr_op_refresh = yes\n'
    refresh+=block_if('has_country_flag = cw_sr_open','cw_sr_programme_states_refresh = yes\n')
    refresh+=block_if('has_country_flag = cw_sr_open OR = { '+' '.join(cv('cw_sr_tab','=',t) for t in [3,4,5,6])+' }','cw_sr_build_list = yes\n')
    effects+=effect('cw_sr_presentation_refresh',refresh)
    buildlist=sv('cw_sr_list_count',0)+sv('cw_sr_list_start','cw_sr_list_page')+'multiply_variable = { cw_sr_list_start = 12 }\n'+sv('cw_sr_list_end','cw_sr_list_start')+av('cw_sr_list_end',12)+sv('cw_sr_list_page_display','cw_sr_list_page')+av('cw_sr_list_page_display',1)+''.join(sv('cw_sr_slot_'+str(i),0) for i in range(12))
    for n,p in enumerate(PROGRAMMES,1):
        r=next(i for i,x in enumerate(DATA['regions'],1) if x['id']==p['region'])
        owners='OR = { always = '+('yes' if p.get('entryProgramme') else 'no')+' '+' '.join('original_tag = '+tag for tag in sorted(set(p.get('owners',[]))|set(p.get('initialProgress',{}))))+' }'
        condition='OR = { AND = { '+cv('cw_sr_tab','=',3)+' OR = { '+cv('cw_sr_filter_region','=',0)+' '+cv('cw_sr_filter_region','=',r)+' } OR = { '+cv('cw_sr_filter_national','=',0)+' '+owners+' } } AND = { '+cv('cw_sr_tab','=',4)+' OR = { '+' '.join(cv(var(n,'state'),'=',s) for s in [1,2,6])+f' has_country_flag = cw_sr_p{n}_deployed'+' } } AND = { '+cv('cw_sr_tab','=',5)+' OR = { '+' '.join(cv(var(n,'state'),'=',s) for s in [3,4,5])+' } } AND = { '+cv('cw_sr_tab','=',6)+' OR = { '+cv(var(n,'launches'),'>',0)+f' has_country_flag = cw_sr_p{n}_awarded has_country_flag = cw_sr_institution_{n} has_country_flag = cw_sr_heritage_{n} has_country_flag = cw_sr_guest_p{n}_completed has_country_flag = cw_sr_op_p{n}_completed'+' } } }'
        kind={'historical':1,'cancelled':2,'plausible':3}[p['kind']]
        condition=condition.replace(cv('cw_sr_tab','=',3),cv('cw_sr_tab','=',3)+' OR = { '+cv('cw_sr_filter_kind','=',0)+' '+cv('cw_sr_filter_kind','=',kind)+' }',1)
        condition=condition.replace(cv('cw_sr_tab','=',3),cv('cw_sr_tab','=',3)+' OR = { '+cv('cw_sr_filter_ready','=',0)+f' cw_sr_p{n}_start_allowed = yes cw_sr_p{n}_launch_allowed = yes'+' }',1)
        body=sv('cw_sr_list_position','cw_sr_list_count',True)+'subtract_from_temp_variable = { cw_sr_list_position = cw_sr_list_start }\n'
        body+=''.join(block_if(cv('cw_sr_list_position','=',slot),sv('cw_sr_slot_'+str(slot),n)) for slot in range(12))+av('cw_sr_list_count',1)
        buildlist+=block_if(condition,body)
    effects+=effect('cw_sr_build_list',buildlist)
    mapping=''
    for n,p in enumerate(PROGRAMMES,1):
        r=next(i for i,x in enumerate(DATA['regions'],1) if x['id']==p['region']);same=[q for q in PROGRAMMES if q['region']==p['region']]
        mapping+=block_if(cv('cw_sr_selected','=',n),sv('cw_sr_region',r)+sv('cw_sr_system',{'earth':1,'cislunar':2,'deep':3}[DATA['regions'][r-1]['system']])+sv('cw_sr_page',same.index(p)//4))
    effects+=effect('cw_sr_selected_map',mapping)
    for direction in ['next','previous']:
        # IMPERIA COLD WAR — Navigation skips expired bulletins.
        body='cw_sr_news_cleanup = yes\n'+sv('cw_sr_found',0,True)
        order=range(1,85) if direction=='next' else range(84,0,-1)
        comparison='<' if direction=='next' else '>'
        for n in order:body+=block_if(cv('cw_sr_found','=',0)+' '+cv('cw_sr_selected',comparison,n)+' '+cv(var(n,'last_report'),'>',0),sv('cw_sr_selected',n)+sv('cw_sr_found',1,True))
        for n in order:body+=block_if(cv('cw_sr_found','=',0)+' '+cv(var(n,'last_report'),'>',0),sv('cw_sr_selected',n)+sv('cw_sr_found',1,True))
        effects+=effect('cw_sr_'+direction+'_bulletin',body)
    # IMPERIA COLD WAR — Reading an archive item never renews its lease.
    replay='cw_sr_news_cleanup = yes\n'
    for n in range(1,85):
        for stage in c['STAGES']:replay+=block_if(cv('cw_sr_selected','=',n)+' '+cv(var(n,'last_report'),'=',stage),c['bulletin_event'](n,stage))
    effects+=effect('cw_sr_replay_bulletin',replay)
    write('common/scripted_effects/COLDWAR_space_race_presentation.txt',effects)
    write('common/scripted_triggers/COLDWAR_space_race_pictures.txt',''.join(effect('cw_sr_picture_'+key.replace('-','_'),cv('cw_sr_view_picture','=',i)) for i,key in enumerate(['mission-control','station','mars','soviet-lunar','french-lunar','saudi-lunar','us-mars','soviet-mars'],1)))
