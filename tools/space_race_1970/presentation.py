# IMPERIA CW — Cold War: native counterpart of the approved Space Race visualisation.
from pathlib import Path
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

W,H=1240,1040
MAP=(0,302,900,440)
FONT_PATH=Path('C:/Windows/Fonts/bahnschrift.ttf')


def save_dds(path,im):
    data=BytesIO();im.save(data,format='DDS');raw=data.getvalue()
    if path.exists() and path.read_bytes()==raw:return
    temporary=path.with_suffix(path.suffix+'.cw_sr_tmp');temporary.write_bytes(raw);temporary.replace(path)


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
    # Intercept the underlying topbar/map in the empty parts of this floating panel.
    widgets.append('iconType = { name = "cw_sr_input_surface" position = { x = 0 y = 0 } spriteType = "GFX_cw_sr_panel" alwaysTransparent = no }\n')
    icon('cw_sr_seal',22,22,'seal')
    text('cw_sr_identity',80,19,880,18,'[CW_SR_Agency]',12)
    text('cw_sr_title',80,42,650,36,'S P A C E   R A C E',28)
    text('cw_sr_date',1008,20,185,23,'[CW_SR_Month] [?global.year|0]',15)
    button('cw_sr_active_effects',1008,49,185,26,'Active effects','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',1),size=12)
    button('cw_sr_close',1200,6,28,27,'X','clr_country_flag = cw_sr_open clr_country_flag = cw_sr_requirements_open',size=12)
    fields=[('Development ceiling / week','$[?cw_sr_budget|3]bn'),('Operating costs / week','$[?cw_sr_weekly_upkeep_m|2]m'),('Space prestige','[?cw_sr_prestige|0]'),('Research data','[?cw_sr_science|0]'),('Crew lost','[?cw_sr_fatalities|0]')]
    for j,(label,value) in enumerate(fields):
        x=22+j*243;text('cw_sr_metric_label_'+str(j),x,94,230,17,label,11)
        text('cw_sr_metric_'+str(j),x,115,230,23,'§H'+value+'§!',16)
    text('cw_sr_standings',23,153,410,17,'SPACE PRESTIGE · TOP 3',11)
    for j in range(1,4):text('cw_sr_rank'+str(j),23+(j-1)*405,177,395,23,'[CW_SR_Rank_'+str(j)+']',15)
    text('cw_sr_leader',23,202,1190,18,'[CW_SR_Leader] · [CW_SR_Leader_Benefit]',11)
    names=['Space Map','National Brief','Programmes','Budget','Flights','Achievements','News']
    for t,name in enumerate(names,1):
        button('cw_sr_tab_'+str(t),14+(t-1)*174,225,168,34,'      '+name,sv('cw_sr_tab',t)+sv('cw_sr_list_page',0)+'clr_country_flag = cw_sr_requirements_open\n',style='nav')
        group=ImageFont.truetype(str(FONT_PATH),13).getlength(name)+21
        icon('cw_sr_nav_icon_'+str(t),14+(t-1)*174+round((168-group)/2),235,'nav_icon_'+str(t))
        properties.append(f'cw_sr_tab_{t} = {{ frame = cw_sr_nav_frame_{t} }}\n')
        icon('cw_sr_tab_active_'+str(t),14+(t-1)*174,225,'nav_active',cv('cw_sr_tab','=',t))
    icon('cw_sr_wide_background',0,264,'wide_bg','OR = { '+' '.join(cv('cw_sr_tab','=',t) for t in [2,3,6,7])+' }')
    icon('cw_sr_work_background',0,264,'details_bg','OR = { '+cv('cw_sr_tab','=',4)+' '+cv('cw_sr_tab','=',5)+' }')
    # Operations: same map artwork, scale controls, destination markers and right card.
    for s,label in enumerate(['Earth Orbital Space','Cislunar Space','Solar System'],1):
        r={1:1,2:7,3:10}[s];p={1:1,2:2,3:31}[s]
        button('cw_sr_system_'+str(s),16+(s-1)*226,271,220,26,label,sv('cw_sr_system',s)+sv('cw_sr_region',r)+sv('cw_sr_selected',p)+sv('cw_sr_page',0),tab(1),style='scale',size=12)
        properties.append(f'cw_sr_system_{s} = {{ frame = cw_sr_scale_frame_{s} }}\n')
        icon('cw_sr_system_active_'+str(s),16+(s-1)*226,271,'scale_active',tab(1)+' '+cv('cw_sr_system','=',s))
        icon('cw_sr_map_'+str(s),MAP[0],MAP[1],'map_'+str(s),tab(1)+' '+cv('cw_sr_system','=',s))
    regions=[]
    for r,region in enumerate(DATA['regions'],1):
        system={'earth':1,'cislunar':2,'deep':3}[region['system']]
        ps=[(n,p) for n,p in enumerate(PROGRAMMES,1) if p['region']==region['id']]
        x,y=region['x'],region['y']
        if system==1:x,y={1:(47,76),2:(62,53),3:(47,21),4:(15,26),5:(18,66),6:(78,40)}[r]
        x=int(MAP[0]+x/100*MAP[2]-73);y=int(MAP[1]+y/100*MAP[3]-18)
        visible=tab(1)+' '+cv('cw_sr_system','=',system)
        labels={1:'Launch sites & labs',2:'Low Earth orbit',3:'Polar orbit',4:'High Earth orbit',5:'Medium Earth orbit',6:'Geostationary orbit'}
        key=loc(f'cw_sr_region_{r}',labels.get(r,region['shortLabel'])+'\n'+str(len(ps))+' programme'+('s' if len(ps)!=1 else ''))
        button('cw_sr_region_'+str(r),x,y,146,43,key,sv('cw_sr_region',r)+sv('cw_sr_selected',ps[0][0])+sv('cw_sr_page',0),visible,tip=loc(f'cw_sr_region_tip_{r}',region['description'].replace('counterfactual','proposed')),style='node',size=12)
        properties.append(f'cw_sr_region_{r} = {{ frame = cw_sr_node_frame_{r} }}\n')
        icon('cw_sr_region_active_'+str(r),x,y,'node_active',visible+' '+cv('cw_sr_region','=',r))
        regions.append((cv('cw_sr_region','=',r),loc(f'cw_sr_region_name_{r}',region['name'])))
        for idx,(n,p) in enumerate(ps):
            visible=tab(1)+' '+cv('cw_sr_region','=',r)+' '+cv('cw_sr_page','=',idx//4)
            button('cw_sr_select_'+str(n),20,822+(idx%4)*38,858,35,f'cw_sr_p{n}_row',sv('cw_sr_selected',n),visible,tip=f'cw_sr_p{n}_detail',style='row',size=13)
            icon('cw_sr_selected_row_'+str(n),20,822+(idx%4)*38,'row_active',visible+' '+cv('cw_sr_selected','=',n))
    text('cw_sr_map_legend',20,718,865,18,'1  Choose a destination       2  Select a programme       3  Develop, qualify and launch',12,tab(1))
    text('cw_sr_region_heading',22,751,620,27,'[CW_SR_Region]',19,tab(1))
    text('cw_sr_region_description',22,781,850,22,'[CW_SR_Region_Brief]',12,tab(1))
    text('cw_sr_region_programmes',22,807,750,16,'PROGRAMMES IN THIS REGION',11,tab(1))
    button('cw_sr_page_prev',800,804,34,24,'<',av('cw_sr_page',-1)+clamp('cw_sr_page',0,6),tab(1),cv('cw_sr_page','>',0),size=12)
    pages=''.join(block_if(cv('cw_sr_region','=',r),clamp('cw_sr_page',0,(sum(p['region']==reg['id'] for p in PROGRAMMES)-1)//4)) for r,reg in enumerate(DATA['regions'],1))
    next_page='OR = { '+''.join('AND = { '+cv('cw_sr_region','=',r)+' '+cv('cw_sr_page','<',(sum(p['region']==reg['id'] for p in PROGRAMMES)-1)//4)+' }' for r,reg in enumerate(DATA['regions'],1))+' }'
    button('cw_sr_page_next',842,804,34,24,'>',av('cw_sr_page',1)+pages,tab(1),next_page,size=12)
    text('cw_sr_next_step',22,977,850,43,'[CW_SR_NextStep]',13,tab(1))
    button('cw_sr_browse_region',665,751,211,28,'Browse all programmes',sv('cw_sr_tab',3)+sv('cw_sr_filter_region','cw_sr_region')+sv('cw_sr_filter_kind',0)+sv('cw_sr_filter_national',0)+sv('cw_sr_filter_ready',0)+sv('cw_sr_list_page',0),tab(1),size=12)
    # Mission card follows the prototype's typographic hierarchy and control order.
    sidebar('cw_sr_kind',920,280,300,19,'[CW_SR_Selected_Kind]',11)
    sidebar('cw_sr_selected_title',920,306,300,66,'[CW_SR_Selected_name]',21,'cw_sr_selected_detail')
    from illustrations import category
    for key in ['ground','rocket','satellite','crew','station','probe','lander']:
        choices='OR = { '+' '.join(cv('cw_sr_selected','=',n) for n,p in enumerate(PROGRAMMES,1) if category(p)==key)+' }'
        icon('cw_sr_programme_art_'+key,920,376,'programme_'+key,side+' '+choices)
    sidebar('cw_sr_selected_region',920,466,300,19,'§T[CW_SR_Selected_Region]§!',12,'cw_sr_selected_detail')
    facts=[('Development from scratch','[?cw_sr_view_months|0] months'),('Time still required','[?cw_sr_view_remaining|1] months'),('Development still to fund','$[?cw_sr_view_unfunded|2]bn'),('Launch & mission cost','$[?cw_sr_view_mission|2]bn'),('Flight / acceptance time','[?cw_sr_view_flight|1] months'),('Operating cost / week','$[?cw_sr_view_upkeep_m|2]m')]
    for j,(label,value) in enumerate(facts):sidebar('cw_sr_fact_'+str(j),920,492+j*23,300,20,label+'   §H'+value+'§!',12)
    sidebar('cw_sr_engineering_label',920,640,300,17,'Qualification completed             [?cw_sr_view_engineering|0]%',11)
    sidebar('cw_sr_funding_label',920,675,300,17,'Development paid for                  [?cw_sr_view_progress|0]%',11)
    icon('cw_sr_engineering_bar',920,663,'progress_cyan',side);properties.append('cw_sr_engineering_bar = { frame = cw_sr_engineering_frame }\n')
    icon('cw_sr_funding_bar',920,698,'progress_gold',side);properties.append('cw_sr_funding_bar = { frame = cw_sr_funding_frame }\n')
    sidebar('cw_sr_phase',920,711,300,21,'[CW_SR_Selected_Status]',12)
    sidebar('cw_sr_chance_label',920,750,165,34,'[CW_SR_SuccessLabel]',12,'cw_sr_risk_tt')
    sidebar('cw_sr_chance',1090,747,130,40,'§T[?cw_sr_view_full|1]%§!',29,'cw_sr_risk_tt')
    sidebar('cw_sr_risk',920,791,300,24,'Departure [?cw_sr_view_launch|1]% · Objective [?cw_sr_view_objective|1]%',11,'cw_sr_risk_tt')
    sidebar('cw_sr_crew',920,820,300,25,'[CW_SR_CrewSummary]',12)
    sidebar('cw_sr_policy_label',920,859,300,18,'Development approach',11)
    toggle=block_if('has_country_flag = cw_sr_policy_open','clr_country_flag = cw_sr_policy_open\n','set_country_flag = cw_sr_policy_open\n')
    button('cw_sr_policy_cycle',920,883,300,29,'[CW_SR_Selected_Policy]  >',toggle,side,'NOT = { '+cv('cw_sr_view_state','=',4)+' } NOT = { '+cv('cw_sr_view_state','=',6)+' }',tip='cw_sr_policy_explanation',size=12)
    button('cw_sr_requirements',920,921,300,23,'Requirements, modifiers & rewards','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',0),side,style='text',size=12)
    action='if = { limit = { OR = { '+cv('cw_sr_view_state','=',0)+' '+cv('cw_sr_view_state','=',2)+' '+cv('cw_sr_view_state','=',7)+' } } cw_sr_selected_start = yes } else = { if = { limit = { '+cv('cw_sr_view_state','=',1)+' } cw_sr_selected_pause = yes } else = { cw_sr_selected_launch = yes } }'
    enabled='OR = { '+''.join('AND = { '+cv('cw_sr_selected','=',n)+f' OR = {{ cw_sr_p{n}_start_allowed = yes cw_sr_p{n}_launch_allowed = yes '+cv(var(n,'state'),'=',1)+' } }' for n in range(1,85))+' }'
    button('cw_sr_primary',920,958,300,34,'[CW_SR_Primary]',action,side+' '+enabled,enabled,'cw_sr_selected_detail','primary',13)
    button('cw_sr_primary_wait',920,958,300,34,'[CW_SR_BlockedAction]','',side+' NOT = { '+enabled+' }','always = no','cw_sr_selected_detail','locked',13)
    button('cw_sr_cancel',920,997,145,24,'Cancel programme','cw_sr_selected_cancel = yes',side+' OR = { '+cv('cw_sr_view_state','=',1)+' '+cv('cw_sr_view_state','=',2)+' '+cv('cw_sr_view_state','=',3)+' }','OR = { '+cv('cw_sr_view_state','=',1)+' '+cv('cw_sr_view_state','=',2)+' '+cv('cw_sr_view_state','=',3)+' }',size=11)
    mothball='OR = { '+''.join('AND = { '+cv('cw_sr_selected','=',n)+f' has_country_flag = cw_sr_p{n}_deployed NOT = {{ '+cv(var(n,'state'),'=',4)+' } }' for n in range(1,85))+' }'
    button('cw_sr_suspend',1075,997,145,24,'Suspend operations','cw_sr_selected_pause = yes',side+' '+mothball,mothball,size=11)
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
    text('cw_sr_budget',26,388,840,27,'Weekly development ceiling: §H$[?cw_sr_budget|3]bn§!',19,tab(4),'cw_sr_budget_tt')
    button('cw_sr_budget_down',710,385,70,29,'-0.05',av('cw_sr_budget',-.05)+clamp('cw_sr_budget',0,11.53846),tab(4),size=12)
    button('cw_sr_budget_up',790,385,70,29,'+0.05',av('cw_sr_budget',.05)+clamp('cw_sr_budget',0,11.53846),tab(4),size=12)
    button('cw_sr_filter_region',26,386,410,29,'Region: [CW_SR_FilterRegion]  >',av('cw_sr_filter_region',1)+'modulo_variable = { cw_sr_filter_region = 16 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_kind',456,386,410,29,'Type: [CW_SR_FilterKind]  >',av('cw_sr_filter_kind',1)+'modulo_variable = { cw_sr_filter_kind = 4 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_ready',886,386,320,29,'[CW_SR_ReadyFilter]',av('cw_sr_filter_ready',1)+'modulo_variable = { cw_sr_filter_ready = 2 }\n'+sv('cw_sr_list_page',0),tab(3),size=12)
    button('cw_sr_filter_national',1016,290,190,29,'All Programmes',sv('cw_sr_filter_national',0)+sv('cw_sr_list_page',0),tab(3)+' '+cv('cw_sr_filter_national','=',1),size=12)
    list_visible='OR = { '+' '.join(cv('cw_sr_tab','=',t) for t in [3,4,5,6])+' } NOT = { has_country_flag = cw_sr_requirements_open }'
    for slot in range(12):
        full='OR = { '+cv('cw_sr_tab','=',3)+' '+cv('cw_sr_tab','=',6)+' }'
        compact='OR = { '+cv('cw_sr_tab','=',4)+' '+cv('cw_sr_tab','=',5)+' }'
        for suffix,width,vis in [('wide',1180,full),('side',850,compact)]:
            button(f'cw_sr_slot_{slot}_{suffix}',26,433+slot*43,width,40,loc(f'cw_sr_slot_{slot}_label',f'[CW_SR_Slot_{slot}]'),sv('cw_sr_selected','cw_sr_slot_'+str(slot))+block_if(full,sv('cw_sr_tab',1)+'cw_sr_selected_map = yes\n'),list_visible+' '+vis+' '+cv('cw_sr_slot_'+str(slot),'>',0),style='row',size=13)
    button('cw_sr_list_prev',26,965,110,30,'< Previous',av('cw_sr_list_page',-1)+clamp('cw_sr_list_page',0,6),list_visible,cv('cw_sr_list_page','>',0),size=12)
    button('cw_sr_list_next',150,965,110,30,'Next >',av('cw_sr_list_page',1)+clamp('cw_sr_list_page',0,6),list_visible,cv('cw_sr_list_count','>','cw_sr_list_end'),size=12)
    text('cw_sr_list_count',286,972,580,22,'[?cw_sr_list_count|0] programmes · Page [?cw_sr_list_page_display|0]',12,list_visible)
    text('cw_sr_list_empty',26,452,820,96,'[CW_SR_EmptyList]',16,list_visible+' '+cv('cw_sr_list_count','=',0))
    # Actual national bulletins, including the supplied country-specific landing art.
    text('cw_sr_news_title',26,286,1175,33,'International News Service',23,tab(7))
    text('cw_sr_news_selector',26,332,1000,30,'[CW_SR_Selected_name]',17,tab(7))
    button('cw_sr_news_prev',1054,329,70,29,'<','cw_sr_previous_bulletin = yes',tab(7),size=12)
    button('cw_sr_news_next',1138,329,70,29,'>','cw_sr_next_bulletin = yes',tab(7),size=12)
    news=tab(7)+' '+cv('cw_sr_view_report','>',0)
    text('cw_sr_news_headline',120,378,1000,42,'[CW_SR_NewsTitle]',24,news)
    for key in ['mission-control','station','mars','soviet-lunar','french-lunar','saudi-lunar','us-mars','soviet-mars']:
        icon('cw_sr_news_image_'+key,120,435,'article_'+key,news+' '+f'cw_sr_picture_{key.replace("-","_")} = yes')
    text('cw_sr_news_body',120,841,1000,130,'[CW_SR_NewsBody]',16,news)
    button('cw_sr_news_read',120,980,1000,35,'Read Mission Report','cw_sr_replay_bulletin = yes',news,size=14,style='primary')
    text('cw_sr_news_empty',26,422,1175,120,'No mission bulletins have been issued by [ROOT.GetName]. Programme authorisations, launches, investigations and mission outcomes will be recorded here.',16,tab(7)+' '+cv('cw_sr_view_report','=',0))
    # Full-width, readable eligibility and effects instead of an undifferentiated tooltip.
    details='has_country_flag = cw_sr_requirements_open'
    icon('cw_sr_requirements_bg',0,264,'wide_bg',details)
    text('cw_sr_requirements_title',26,283,1180,32,'[CW_SR_Selected_name]',23,details)
    button('cw_sr_readiness_mode',26,330,280,32,'Mission requirements',sv('cw_sr_details_mode',0),details,size=13)
    button('cw_sr_effects_mode',320,330,280,32,'National effects',sv('cw_sr_details_mode',1),details,size=13)
    text('cw_sr_requirements_body',26,385,575,566,'[CW_SR_Selected_Checklist]',13,details+' '+cv('cw_sr_details_mode','=',0))
    text('cw_sr_national_effects_body',26,385,575,566,'cw_sr_national_effects',14,details+' '+cv('cw_sr_details_mode','=',1))
    text('cw_sr_modifiers_heading',644,385,560,23,'MISSION PROBABILITY MODIFIERS',15,details)
    text('cw_sr_modifiers_body',644,418,560,365,'[CW_SR_ModifierTable]',13,details)
    text('cw_sr_rewards_heading',644,805,560,23,'PROGRAMME REWARDS',15,details)
    text('cw_sr_rewards_body',644,838,560,165,'[CW_SR_VisibleRewards]',13,details)
    button('cw_sr_requirements_close',26,964,300,31,'Return to Operations','clr_country_flag = cw_sr_requirements_open',details,size=13)
    # Footer has the real game calendar; prototype time-advance controls are not game actions.
    text('cw_sr_footer',20,1025,870,14,'PROGRAMME CALENDAR · [GetDateText]',11)
    # Native popup choices appear above the card controls, as in the reference select.
    popup=side+' has_country_flag = cw_sr_policy_open'
    for policy,label in enumerate(['Standard Programme','Extended Assurance','Accelerated Schedule','Reduced Expenditure']):
        choice=''.join(block_if(cv('cw_sr_selected','=',n)+' NOT = { '+cv(var(n,'state'),'=',4)+' } NOT = { '+cv(var(n,'state'),'=',6)+' }',sv(var(n,'policy'),policy)) for n in range(1,85))+'clr_country_flag = cw_sr_policy_open\n'
        button('cw_sr_policy_option_'+str(policy),920,883+policy*28,300,28,label,choice,popup,style='control',size=12)
    gui='guiTypes = { containerWindowType = { name = "cw_sr_main_window" position = { x = 0 y = 0 } size = { width = 1240 height = 1040 } orientation = center origo = center moveable = yes click_to_front = yes clipping = no background = { name = "cw_sr_background" quadTextureSprite = "GFX_cw_sr_panel" }\n'+''.join(widgets)+'} }\n'
    write('interface/COLDWAR_space_race.gui',gui)
    scripted='scripted_gui = { cw_sr_main = { context_type = player_context window_name = "cw_sr_main_window" dirty = global.cw_sr_dirty ai_enabled = { always = no } visible = { '+guard()+' has_country_flag = cw_sr_open }\ntriggers = {\n'+''.join(triggers)+'}\neffects = {\n'+''.join(clicks)+'}\nproperties = {\n'+''.join(properties)+'}\n} }\n'
    write('common/scripted_guis/COLDWAR_space_race_gui.txt',scripted)
    extra_definitions(c,regions)
    native_graphics(texture,sizes)
    write('interface/COLDWAR_space_race_command.gfx','spriteTypes = {\n'+''.join(sprites)+'}\n'+font_graphics())


def native_graphics(texture,sizes):
    from illustrations import programme_art, planet
    for kind in ['ground','rocket','satellite','crew','station','probe','lander']:
        texture('programme_'+kind,programme_art(kind,FONT_PATH))
    panel=Image.new('RGBA',(W,H),'#111719');d=ImageDraw.Draw(panel)
    d.rectangle((0,0,W-1,85),fill='#263337');d.rectangle((0,86,W-1,141),fill='#182328')
    d.rectangle((0,142,W-1,219),fill='#1c282b');d.rectangle((0,220,W-1,263),fill='#111a1f')
    d.rectangle((0,264,899,1023),fill='#0c1419');d.rectangle((900,264,1239,1023),fill='#1d292e')
    d.rectangle((0,742,899,800),fill='#213038');d.rectangle((0,1024,1239,1039),fill='#1d2a30')
    for y in [85,141,219,263,1023]:d.line((0,y,W-1,y),fill='#48595d')
    for y in [742,800]:d.line((0,y,899,y),fill='#48595d')
    for j in range(1,5):d.line((j*243+10,96,j*243+10,132),fill='#3b484b')
    d.line((900,264,900,1023),fill='#536166')
    for y in [482,632,740,850]:d.line((920,y,1220,y),fill='#49595d')
    d.rectangle((916,816,1222,846),fill='#111d22');d.rectangle((0,0,W-1,H-1),outline='#667171',width=1)
    texture('panel',panel)
    texture('details_bg',Image.new('RGBA',(900,760),'#142028'))
    texture('wide_bg',Image.new('RGBA',(1240,760),'#142028'))
    for name,size in [('row_active',(858,35)),('nav_active',(168,34)),('node_active',(146,43)),('scale_active',(220,26))]:
        im=Image.new('RGBA',size,(0,0,0,0));dr=ImageDraw.Draw(im)
        if name=='node_active':dr.rectangle((0,0,1,size[1]-1),fill='#d0b77c')
        else:dr.rectangle((0,0,size[0]-1,size[1]-1),outline='#c5ae77',width=1);dr.line((0,size[1]-2,size[0]-1,size[1]-2),fill='#d0b77c',width=2)
        texture(name,im)
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
    for scale in [1,2,3]:
        im=ImageOps.fit(Image.open(ASSETS/'earth-moon-map-v1.png').convert('RGB'),(900,515),method=Image.Resampling.LANCZOS)
        im=ImageEnhance.Brightness(im).enhance(.84 if scale==1 else .92);dr=ImageDraw.Draw(im)
        if scale==1:
            for rx,ry in [(220,220),(280,231),(104,238),(358,171)]:dr.ellipse((350-rx,254-ry,350+rx,254+ry),outline='#47636b',width=1)
        elif scale==2:
            dr.ellipse((647,113,806,244),outline='#627e80');dr.line((569,179,879,179),fill='#627e80')
        else:
            im=Image.new('RGB',(900,515),'#02090f');dr=ImageDraw.Draw(im)
            for x in range(0,900,180):dr.line((x,0,x,515),fill='#15272d')
            for y in range(0,515,129):dr.line((0,y,900,y),fill='#15272d')
            for rx,ry in [(126,88),(243,162),(387,234),(589,297)]:dr.ellipse((153-rx,302-ry,153+rx,302+ry),outline='#425e67')
            import random
            rng=random.Random(1970)
            for _ in range(330):dr.point((rng.randrange(900),rng.randrange(515)),fill=rng.choice(['#1a303c','#2c404b','#526472']))
            for x,y,r,color in [(153,302,26,'#edcc82'),(279,270,9,'#c7a880'),(390,279,10,'#7cbbcb'),(513,185,9,'#ce8d66'),(707,317,18,'#c0ab8c'),(820,132,14,'#b6ad94')]:planet(dr,x,y,r,color)
            f=ImageFont.truetype(str(FONT_PATH),13)
            for x,y,label in [(124,352,'SUN'),(366,316,'EARTH'),(491,162,'MARS'),(673,355,'JUPITER')]:dr.text((x,y),label,font=f,fill='#bdcccf')
        texture('map_'+str(scale),ImageOps.fit(im,MAP[2:],method=Image.Resampling.LANCZOS))
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


def extra_definitions(c,regions):
    def define(name,entries,fallback):
        return 'defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+condition+' } localization_key = '+key+' }\n' for condition,key in entries)+'text = { localization_key = '+fallback+' } }\n'
    from readiness import definitions
    defs=definitions(c)+define('CW_SR_Region',regions,'cw_sr_region_name_1')
    ground='OR = { '+' '.join(cv('cw_sr_selected','=',n) for n,p in enumerate(PROGRAMMES,1) if p['region']=='ground')+' }'
    defs+=define('CW_SR_SuccessLabel',[(ground,loc('cw_sr_acceptance_chance','Estimated programme\nacceptance chance'))],loc('cw_sr_flight_chance','Estimated full\nmission success'))
    defs+=define('CW_SR_CrewSummary',[(ground,loc('cw_sr_ground_crew','Ground programme · No flight crew'))],loc('cw_sr_flight_crew','Crew [?cw_sr_view_crew|0] · Flight remaining [?cw_sr_view_days|0] days'))
    defs+=define('CW_SR_BlockedAction',[(cv('cw_sr_view_state','=',s),loc('cw_sr_blocked_'+str(s),label)) for s,label in [(1,'Weekly funding required'),(4,'Mission in flight'),(6,'Investigation in progress')]],loc('cw_sr_blocked_requirements','Requirements not met'))
    for n,p in enumerate(PROGRAMMES,1):
        defs+=define('CW_SR_Readiness_'+str(n),[(f'cw_sr_p{n}_launch_allowed = yes',loc('cw_sr_ready_launch','§GReady for mission authorisation§!')),(f'cw_sr_p{n}_start_allowed = yes',loc('cw_sr_ready_development','§GReady for development§!')),(cv(var(n,'state'),'=',0),loc('cw_sr_needs_requirements','§gSupporting capabilities or funding required§!'))],loc(f'cw_sr_row_progress_{n}',f'§g[CW_SR_Status_{n}] · [?{var(n,"work")}|0]% development§!'))
        loc(f'cw_sr_p{n}_row',p['name']+'\n[CW_SR_Readiness_'+str(n)+']')
    defs+=define('CW_SR_ReadyFilter',[(cv('cw_sr_filter_ready','=',1),loc('cw_sr_ready_only','Show: Ready to begin'))],loc('cw_sr_ready_all','Show: All readiness levels'))
    next_entries=[]
    for n in range(1,85):
        next_entries.extend([(cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_launch_allowed = yes',loc('cw_sr_next_launch','§GNEXT STEP: Authorise the mission.§!\nThe full launch appropriation is paid when you authorise departure.')),(cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_start_allowed = yes',loc('cw_sr_next_start','§GNEXT STEP: Authorise development.§!\nEngineering advances with paid weekly funding. Adjust your ceiling in Budget.'))])
    for state,message in [(1,'NEXT STEP: Maintain weekly funding.\nQualification and paid development must both finish before departure.'),(2,'NEXT STEP: Resume development when funding is available.\nExisting paid work is retained.'),(3,'NEXT STEP: Review the programme requirements.\nCheck mission funds, supporting systems, unpaid costs and launch opportunities.'),(4,'MISSION IN FLIGHT\nWait for the mission report. Departure probabilities are already fixed.'),(5,'PROGRAMME OPERATIONAL\nWeekly operating costs maintain this capability. Further missions may be available.'),(6,'INVESTIGATION IN PROGRESS\nCorrective engineering requires weekly funding before missions can resume.')]:
        next_entries.append((cv('cw_sr_view_state','=',state),loc('cw_sr_next_state_'+str(state),message)))
    defs+=define('CW_SR_NextStep',next_entries,loc('cw_sr_next_blocked','NEXT STEP: Open Programme requirements.\nDevelop the required supporting capabilities and provide sufficient funding.'))
    defs+=define('CW_SR_EmptyList',[(cv('cw_sr_tab','=',3),loc('cw_sr_empty_catalogue','No programmes match these filters.\nChoose another region or switch to All readiness levels.')),(cv('cw_sr_tab','=',4),loc('cw_sr_empty_budget','No programmes currently need development funding.\nChoose a programme on the Space Map and authorise development.')),(cv('cw_sr_tab','=',5),loc('cw_sr_empty_flights','No flight hardware is ready yet.\nComplete funded development and qualification before authorising a mission.'))],loc('cw_sr_empty_records','No national missions have been recorded yet.\nCompleted missions and achievements will appear here.'))
    defs+=define('CW_SR_Month',[(cv('global.month','=',i),loc('cw_sr_month_'+str(i),month)) for i,month in enumerate(['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'],1)],'cw_sr_month_1')
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
    for i,milestone in enumerate(DATA['milestones'],1):
        history=next((h for h in DATA['historicalFirsts'] if h['milestoneId']==milestone['id']),None)
        fallback=loc('cw_sr_first_status_'+str(i),milestone['title']+': '+((next(p['name'] for p in DATA['profiles'] if p['id']==history['country'])+' · '+history['date']) if history else 'Unclaimed'))
        entries=[(f'has_event_target = cw_sr_first_holder_{i}',loc('cw_sr_first_holder_'+str(i),milestone['title']+f': [event_target:cw_sr_first_holder_{i}.GetName]'))]
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
    effects='';refresh=sv('cw_sr_analysis_current','cw_sr_science')+'multiply_variable = { cw_sr_analysis_current = 0.02 }\n'+clamp('cw_sr_analysis_current',0,2)
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
    refresh+=block_if('has_country_flag = cw_sr_open OR = { '+' '.join(cv('cw_sr_tab','=',t) for t in [3,4,5,6])+' }','cw_sr_build_list = yes\n')
    effects+=effect('cw_sr_presentation_refresh',refresh)
    buildlist=sv('cw_sr_list_count',0)+sv('cw_sr_list_start','cw_sr_list_page')+'multiply_variable = { cw_sr_list_start = 12 }\n'+sv('cw_sr_list_end','cw_sr_list_start')+av('cw_sr_list_end',12)+sv('cw_sr_list_page_display','cw_sr_list_page')+av('cw_sr_list_page_display',1)+''.join(sv('cw_sr_slot_'+str(i),0) for i in range(12))
    for n,p in enumerate(PROGRAMMES,1):
        r=next(i for i,x in enumerate(DATA['regions'],1) if x['id']==p['region'])
        owners='OR = { always = '+('yes' if p.get('entryProgramme') else 'no')+' '+' '.join('original_tag = '+tag for tag in sorted(set(p.get('owners',[]))|set(p.get('initialProgress',{}))))+' }'
        condition='OR = { AND = { '+cv('cw_sr_tab','=',3)+' OR = { '+cv('cw_sr_filter_region','=',0)+' '+cv('cw_sr_filter_region','=',r)+' } OR = { '+cv('cw_sr_filter_national','=',0)+' '+owners+' } } AND = { '+cv('cw_sr_tab','=',4)+' OR = { '+' '.join(cv(var(n,'state'),'=',s) for s in [1,2,6])+f' has_country_flag = cw_sr_p{n}_deployed'+' } } AND = { '+cv('cw_sr_tab','=',5)+' OR = { '+' '.join(cv(var(n,'state'),'=',s) for s in [3,4,5])+' } } AND = { '+cv('cw_sr_tab','=',6)+' OR = { '+cv(var(n,'launches'),'>',0)+f' has_country_flag = cw_sr_p{n}_awarded'+' } } }'
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
        body=sv('cw_sr_found',0,True)
        order=range(1,85) if direction=='next' else range(84,0,-1)
        comparison='<' if direction=='next' else '>'
        for n in order:body+=block_if(cv('cw_sr_found','=',0)+' '+cv('cw_sr_selected',comparison,n)+' '+cv(var(n,'last_report'),'>',0),sv('cw_sr_selected',n)+sv('cw_sr_found',1,True))
        for n in order:body+=block_if(cv('cw_sr_found','=',0)+' '+cv(var(n,'last_report'),'>',0),sv('cw_sr_selected',n)+sv('cw_sr_found',1,True))
        effects+=effect('cw_sr_'+direction+'_bulletin',body)
    replay=''
    for n in range(1,85):
        for stage in c['STAGES']:replay+=block_if(cv('cw_sr_selected','=',n)+' '+cv(var(n,'last_report'),'=',stage),c['bulletin'](n,stage))
    effects+=effect('cw_sr_replay_bulletin',replay)
    write('common/scripted_effects/COLDWAR_space_race_presentation.txt',effects)
    write('common/scripted_triggers/COLDWAR_space_race_pictures.txt',''.join(effect('cw_sr_picture_'+key.replace('-','_'),cv('cw_sr_view_picture','=',i)) for i,key in enumerate(['mission-control','station','mars','soviet-lunar','french-lunar','saudi-lunar','us-mars','soviet-mars'],1)))
