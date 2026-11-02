# IMPERIA COLD WAR — Orbital Atlas and Mission Control native presentation.
"""Approved map-led interface and a read-only, runtime-derived flight authority.

Navigation never pays for, qualifies, launches or resolves a mission. Start and
launch controls continue to call the existing per-programme guarded effects.
"""
from PIL import Image,ImageDraw,ImageOps,ImageEnhance
from mission_rules import REQUIREMENTS,qualified
from technology_integration import requirement_parts

MAP=(20,288,856,412)


# IMPERIA COLD WAR — Approved Atlas layout and native command-room controls.
# IMPERIA COLD WAR — International operational cooperation.
def controls(c,a):
    text,icon,button,tab,properties=(a[k] for k in ['text','icon','button','tab','properties'])
    cv,sv,av,clamp,var,block_if,loc=(c[k] for k in ['cv','sv','av','clamp','var','block_if','loc'])
    ps,regions_data=c['PROGRAMMES'],c['DATA']['regions']
    side='OR = { '+''.join(cv('cw_sr_tab','=',t)+' ' for t in [1,4,5,8])+' } NOT = { has_country_flag = cw_sr_requirements_open }'
    def card(name,x,y,w,h,key,size=13,tip=None):text(name,x,y,w,h,key,size,side,tip)
    a['widgets'].append('iconType = { name = "cw_sr_input_surface" position = { x = 0 y = 0 } spriteType = "GFX_cw_sr_panel" alwaysTransparent = no }\n')
    icon('cw_sr_seal',22,18,'seal')
    text('cw_sr_identity',80,15,602,18,'[CW_SR_Agency]',12)
    text('cw_sr_title',80,36,610,37,'S P A C E   R A C E',28)
    # IMPERIA COLD WAR — The campaign date remains in the main game interface.
    button('cw_sr_active_effects',1008,47,185,26,'Active effects','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',1),size=12)
    button('cw_sr_control_open',704,47,278,26,'Mission Control  >','cw_sr_open_control = yes',size=12)
    button('cw_sr_close',1200,6,28,27,'X','clr_country_flag = cw_sr_open clr_country_flag = cw_sr_requirements_open',size=12)
    for t,name in enumerate(['Orbital Atlas','National Brief','Programmes','Budget','Flight Operations','Records','News'],1):
        button('cw_sr_tab_'+str(t),14+(t-1)*174,91,168,34,name,sv('cw_sr_tab',t)+sv('cw_sr_list_page',0)+'clr_country_flag = cw_sr_requirements_open\n',style='nav')
        properties.append(f'cw_sr_tab_{t} = {{ frame = cw_sr_nav_frame_{t} }}\n')
        selected=cv('cw_sr_tab','=',t) if t!=1 else 'OR = { '+cv('cw_sr_tab','=',1)+' '+cv('cw_sr_tab','=',8)+' '+cv('cw_sr_tab','=',9)+' }'
        icon('cw_sr_tab_active_'+str(t),14+(t-1)*174,91,'nav_active',selected)
    text('cw_sr_standings',22,142,180,18,'SPACE PRESTIGE · TOP 3',11)
    # IMPERIA COLD WAR — Native current-country flags in the historical and player standings.
    from crew_ui import flag as country_flag
    for j in range(1,4):
        country_flag(a,'cw_sr_rank_flag_'+str(j),214+(j-1)*335,137,f'cw_sr_flag_rank{j}',f'has_event_target = cw_sr_rank{j}',True)
        # IMPERIA COLD WAR — Long country names may use both lines inside the standings bar.
        text('cw_sr_rank'+str(j),266+(j-1)*335,135,274,34,'[CW_SR_Rank_'+str(j)+']',14,'','cw_sr_leadership_tt')
    for j,(label,value) in enumerate([('Development / week','$[?cw_sr_budget|3]bn'),('Operations / week','$[?cw_sr_weekly_upkeep_m|2]m'),('Space prestige','[?cw_sr_prestige|0]'),('Research data','[?cw_sr_science|0]'),('Crew lost','[?cw_sr_fatalities|0]')]):
        text('cw_sr_metric_label_'+str(j),22+j*243,184,230,16,label,11)
        text('cw_sr_metric_'+str(j),22+j*243,205,230,24,'§H'+value+'§!',16)
    icon('cw_sr_wide_background',0,264,'wide_bg','OR = { '+''.join(cv('cw_sr_tab','=',t)+' ' for t in [2,3,6,7])+' }')
    icon('cw_sr_work_background',0,264,'details_bg','OR = { '+cv('cw_sr_tab','=',4)+' '+cv('cw_sr_tab','=',5)+' }')
    for s,label in enumerate(['Earth Orbital Space','Cislunar Space','Solar System'],1):
        r={1:1,2:7,3:10}[s];p={1:1,2:2,3:31}[s]
        button('cw_sr_system_'+str(s),20+(s-1)*218,248,208,28,label,sv('cw_sr_system',s)+sv('cw_sr_region',r)+sv('cw_sr_selected',p)+sv('cw_sr_page',0),tab(1),style='scale',size=12)
        properties.append(f'cw_sr_system_{s} = {{ frame = cw_sr_scale_frame_{s} }}\n')
        icon('cw_sr_system_active_'+str(s),20+(s-1)*218,248,'scale_active',tab(1)+' '+cv('cw_sr_system','=',s))
        icon('cw_sr_map_'+str(s),MAP[0],MAP[1],'map_'+str(s),tab(1)+' '+cv('cw_sr_system','=',s))
    regions=[]
    for r,region in enumerate(regions_data,1):
        system={'earth':1,'cislunar':2,'deep':3}[region['system']]
        programmes=[(n,p) for n,p in enumerate(ps,1) if p['region']==region['id']]
        x,y=region['x'],region['y']
        if system==1:x,y={1:(47,76),2:(62,53),3:(47,21),4:(15,26),5:(18,66),6:(78,40)}[r]
        x=int(MAP[0]+x/100*MAP[2]-73);y=int(MAP[1]+y/100*MAP[3]-21)
        visible=tab(1)+' '+cv('cw_sr_system','=',system)
        labels={1:'Launch sites & labs',2:'Low Earth orbit',3:'Polar orbit',4:'High Earth orbit',5:'Medium Earth orbit',6:'Geostationary orbit'}
        key=loc(f'cw_sr_region_caption_{r}',labels.get(r,region['shortLabel'])+'\n'+str(len(programmes))+(' programme' if len(programmes)==1 else ' programmes'))
        button('cw_sr_region_'+str(r),x,y,146,43,'',sv('cw_sr_region',r)+sv('cw_sr_selected',programmes[0][0])+sv('cw_sr_page',0),visible,tip=loc(f'cw_sr_region_tip_{r}',region['description'].replace('counterfactual','proposed')),style='node',size=12)
        properties.append(f'cw_sr_region_{r} = {{ frame = cw_sr_node_frame_{r} }}\n')
        text('cw_sr_region_label_'+str(r),x+8,y+4,130,36,key,11,visible)
        icon('cw_sr_region_active_'+str(r),x,y,'node_active',visible+' '+cv('cw_sr_region','=',r))
        regions.append((cv('cw_sr_region','=',r),loc(f'cw_sr_region_name_{r}',region['name'])))
        for idx,(n,p) in enumerate(programmes):
            shown=tab(1)+' '+cv('cw_sr_region','=',r)+' '+cv('cw_sr_page','=',idx//4)
            x=20+(idx%2)*435;y=790+(idx%4//2)*89
            button('cw_sr_select_'+str(n),x,y,421,80,'',sv('cw_sr_selected',n),shown,tip=f'cw_sr_p{n}_detail',style='row',size=13)
            icon('cw_sr_selected_row_'+str(n),x,y,'row_active',shown+' '+cv('cw_sr_selected','=',n))
            text('cw_sr_card_name_'+str(n),x+18,y+10,385,38,f'cw_sr_p{n}_name',13,shown)
            text('cw_sr_card_state_'+str(n),x+18,y+57,385,18,'[CW_SR_ProgrammeState_'+str(n)+']',12,shown)
            icon('cw_sr_card_strip_'+str(n),x,y,'programme_state_strip',shown)
            properties.append(f'cw_sr_card_strip_{n} = {{ frame = cw_sr_p{n}_ui_frame }}\n')
    text('cw_sr_map_legend',36,678,815,17,'MISSION REGIONS · SCHEMATIC DISTANCES',11,tab(1))
    text('cw_sr_region_heading',22,716,615,29,'[CW_SR_Region]',21,tab(1))
    text('cw_sr_region_description',22,752,850,30,'[CW_SR_Region_Brief]',12,tab(1))
    button('cw_sr_browse_region',662,717,214,28,'Browse all programmes',sv('cw_sr_tab',3)+sv('cw_sr_filter_region','cw_sr_region')+sv('cw_sr_filter_kind',0)+sv('cw_sr_filter_national',0)+sv('cw_sr_filter_ready',0)+sv('cw_sr_list_page',0),tab(1),size=12)
    button('cw_sr_page_prev',792,971,36,24,'<',av('cw_sr_page',-1)+clamp('cw_sr_page',0,6),tab(1),cv('cw_sr_page','>',0),size=12)
    pages=''.join(block_if(cv('cw_sr_region','=',r),clamp('cw_sr_page',0,(sum(p['region']==reg['id'] for p in ps)-1)//4)) for r,reg in enumerate(regions_data,1))
    next_page='OR = { '+''.join('AND = { '+cv('cw_sr_region','=',r)+' '+cv('cw_sr_page','<',(sum(p['region']==reg['id'] for p in ps)-1)//4)+' }' for r,reg in enumerate(regions_data,1))+' }'
    button('cw_sr_page_next',840,971,36,24,'>',av('cw_sr_page',1)+pages,tab(1),next_page,size=12)
    text('cw_sr_next_step',22,971,750,46,'[CW_SR_AtlasNext]',13,tab(1))
    # IMPERIA COLD WAR — Compact mission inspector, all values from the real selected programme.
    card('cw_sr_kind',920,250,300,19,'[CW_SR_Selected_Kind]',11)
    card('cw_sr_selected_title',920,277,300,72,'[CW_SR_Selected_name]',21,'cw_sr_selected_detail')
    card('cw_sr_selected_region',920,357,300,20,'§T[CW_SR_Selected_Region]§!',12)
    card('cw_sr_chance_label',920,395,164,36,'[CW_SR_SuccessLabel]',12,'cw_sr_risk_tt')
    card('cw_sr_chance',1090,389,130,43,'§H[?cw_sr_view_full|1]%§!',29,'cw_sr_risk_tt')
    card('cw_sr_risk',920,440,300,20,'Departure [?cw_sr_view_launch|1]% · Objective [?cw_sr_view_objective|1]%',11,'cw_sr_risk_tt')
    card('cw_sr_crew',920,469,300,34,'[CW_SR_CrewSummary]',12)
    facts=[('Development calendar','[?cw_sr_view_months|0] months'),('Development remaining','[?cw_sr_view_remaining|1] months'),('Development still to fund','$[?cw_sr_view_unfunded|2]bn'),('Mission appropriation','$[?cw_sr_view_mission|2]bn'),('Flight / acceptance','[?cw_sr_view_flight|1] months'),('Operations / week','$[?cw_sr_view_upkeep_m|2]m')]
    for j,(label,value) in enumerate(facts):card('cw_sr_fact_'+str(j),920,518+j*23,300,20,label+'   §H'+value+'§!',12)
    card('cw_sr_engineering_label',920,667,300,18,'Qualification completed             [?cw_sr_view_engineering|0]%',11)
    icon('cw_sr_engineering_bar',920,690,'progress_cyan',side);properties.append('cw_sr_engineering_bar = { frame = cw_sr_engineering_frame }\n')
    card('cw_sr_funding_label',920,706,300,18,'Development paid for                  [?cw_sr_view_progress|0]%',11)
    icon('cw_sr_funding_bar',920,730,'progress_gold',side);properties.append('cw_sr_funding_bar = { frame = cw_sr_funding_frame }\n')
    card('cw_sr_phase',920,746,300,22,'[CW_SR_AtlasPhase]',12)
    card('cw_sr_card_next',920,781,300,34,'[CW_SR_Control_Blocker]',12)
    button('cw_sr_card_control',920,823,300,30,'Mission Control · readiness report','cw_sr_open_control = yes',side,size=12)
    card('cw_sr_policy_label',920,861,300,18,'Development approach',11)
    toggle=block_if('has_country_flag = cw_sr_policy_open','clr_country_flag = cw_sr_policy_open\n','set_country_flag = cw_sr_policy_open\n')
    button('cw_sr_policy_cycle',920,883,300,29,'[CW_SR_Selected_Policy]  >',toggle,side,'NOT = { '+cv('cw_sr_view_state','=',4)+' } NOT = { '+cv('cw_sr_view_state','=',6)+' }',tip='cw_sr_policy_explanation',size=12)
    button('cw_sr_requirements',920,921,300,23,'Requirements, modifiers & rewards','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',0),side,style='text',size=12)
    action='if = { limit = { OR = { '+cv('cw_sr_view_state','=',0)+' '+cv('cw_sr_view_state','=',2)+' '+cv('cw_sr_view_state','=',7)+' } } cw_sr_selected_start = yes } else = { if = { limit = { '+cv('cw_sr_view_state','=',1)+' } cw_sr_selected_pause = yes } else = { cw_sr_selected_launch = yes } }'
    enabled='OR = { '+''.join('AND = { '+cv('cw_sr_selected','=',n)+f' OR = {{ cw_sr_p{n}_start_allowed = yes cw_sr_p{n}_launch_allowed = yes '+cv(var(n,'state'),'=',1)+' } }' for n in range(1,85))+' }'
    button('cw_sr_primary',920,958,300,34,'[CW_SR_Primary]',action,side+' '+enabled,enabled,'cw_sr_selected_detail','primary',13)
    button('cw_sr_primary_wait',920,958,300,34,'Review mission readiness','cw_sr_open_control = yes',side+' NOT = { '+enabled+' }',tip='cw_sr_selected_detail',style='control',size=13)
    cancel='OR = { '+''.join(cv('cw_sr_view_state','=',s)+' ' for s in [1,2,3])+' }'
    button('cw_sr_cancel',920,997,145,24,'Cancel programme','cw_sr_selected_cancel = yes',side+' '+cancel,cancel,size=11)
    mothball='OR = { '+''.join('AND = { '+cv('cw_sr_selected','=',n)+f' has_country_flag = cw_sr_p{n}_deployed NOT = {{ '+cv(var(n,'state'),'=',4)+' } }' for n in range(1,85))+' }'
    button('cw_sr_suspend',1075,997,145,24,'Suspend operations','cw_sr_selected_pause = yes',side+' '+mothball,mothball,size=11)
    # IMPERIA COLD WAR — Mission Control: factual approval stages and precursor navigation.
    mc=tab(8)
    icon('cw_sr_control_background',0,238,'control_bg',mc)
    text('cw_sr_control_heading',30,253,600,23,'MISSION CONTROL · FLIGHT AUTHORITY',13,mc)
    button('cw_sr_control_atlas',682,249,194,28,'< Orbital Atlas',sv('cw_sr_tab',1)+'cw_sr_selected_map = yes\n',mc,size=12)
    text('cw_sr_control_name',30,291,846,52,'[CW_SR_Selected_name]',21,mc)
    for j,(label,field,mode) in enumerate([('RESEARCH','Research',2),('ENGINEERING','Engineering',0),('PRECURSOR FLIGHTS','Precursors',0),('MISSION APPROVAL','Authority',0)]):
        button('cw_sr_control_stage_'+str(j),30+j*213,351,207,61,label+'\n[CW_SR_Control_'+field+']','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',mode),mc,style='scale',size=12)
    from illustrations import category
    for kind in ['ground','rocket','satellite','crew','station','probe','lander']:
        choices='OR = { '+''.join(cv('cw_sr_selected','=',n)+' ' for n,p in enumerate(ps,1) if category(p)==kind)+' }'
        icon('cw_sr_programme_art_'+kind,30,430,'programme_'+kind,mc+' '+choices)
    text('cw_sr_control_brief',354,430,522,88,'[CW_SR_Selected_brief]',14,mc)
    text('cw_sr_control_research_title',30,548,360,22,'RESEARCH & NATIONAL CAPACITY',13,mc)
    text('cw_sr_control_research',30,583,365,88,'[CW_SR_Control_ResearchDetail]',13,mc)
    button('cw_sr_control_capabilities',30,674,365,27,'Review missing national capabilities  >','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',0),mc+' '+cv('cw_sr_control_caps_missing','>',0),size=12)
    text('cw_sr_control_operations_title',30,716,365,22,'APPROPRIATION & FLIGHT CONDITIONS',13,mc)
    # IMPERIA COLD WAR — Keep the conditions panel distinct from the operations button.
    text('cw_sr_control_conditions',30,750,365,113,'[CW_SR_Control_Conditions]',13,mc)
    text('cw_sr_control_precursor_title',432,548,444,22,'SUCCESSFUL PRECURSOR FLIGHTS',13,mc)
    for j in range(4):
        text('cw_sr_control_precursor_'+str(j),432,584+j*64,444,57,'[CW_SR_Control_Precursor_'+str(j)+']',13,mc)
    text('cw_sr_control_next',30,880,846,50,'[CW_SR_AtlasNext]',14,mc)
    button('cw_sr_control_precursor_open',30,950,276,35,'Open missing precursor','cw_sr_control_focus_requirement = yes',mc,cv('cw_sr_control_missing','>',0),size=13)
    button('cw_sr_control_return',322,950,264,35,'Return to expedition','cw_sr_control_return = yes',mc+' '+cv('cw_sr_control_parent','>',0),size=13)
    button('cw_sr_control_risks',602,950,274,35,'Safety & contingency plan','set_country_flag = cw_sr_requirements_open\n'+sv('cw_sr_details_mode',3),mc,size=13)
    # IMPERIA COLD WAR — Native international crew selection.
    from crew import controls as crew_controls
    crew_controls(c,a)
    # IMPERIA COLD WAR — Non-crew partner work packages and outbound orders.
    from cooperation_ui import controls as operations_controls
    operations_controls(c,a)
    return regions,side


# IMPERIA COLD WAR — Live read-only readiness definitions and safe programme navigation.
# IMPERIA COLD WAR — International operational cooperation.
def definitions(c):
    cv,sv,av,block_if,effect,var,loc=(c[k] for k in ['cv','sv','av','block_if','effect','var','loc']);ps=c['PROGRAMMES'];ids=c['IDS']
    defs='';selected={k:[] for k in ['Blocker','ResearchDetail','Conditions']};pre=[[] for _ in range(4)];nexts=[];refresh=block_if(cv('cw_sr_control_parent','>',0)+' '+cv('cw_sr_selected','!=','cw_sr_control_child'),sv('cw_sr_control_parent',0));focus=''
    def define(name,entries,fallback):
        return 'defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+condition+' } localization_key = '+key+' }\n' for condition,key in entries)+'text = { localization_key = '+fallback+' } }\n'
    for n,p in enumerate(ps,1):
        sel=cv('cw_sr_selected','=',n);state=var(n,'state');groups=REQUIREMENTS.get(p['id'],[]);assert len(groups)<=4
        body=sv('cw_sr_control_missing',0)+sv('cw_sr_control_caps_missing',0)+sv('cw_sr_control_total',len(groups))+sv('cw_sr_control_accepted',0)
        for capability in p['capabilityRequirements']:body+=block_if('NOT = { has_country_flag = '+c['cap'](capability)+' }',av('cw_sr_control_caps_missing',1))
        for group in groups:body+=block_if(qualified(group,ids),av('cw_sr_control_accepted',1),av('cw_sr_control_missing',1))
        refresh+=block_if(sel,body)
        research=[f'[CW_SR_Tech_{n}_{j}]' for j,_ in enumerate(requirement_parts(p),1)] or ['No orbital-launch research required.']
        research+=['','[CW_SR_Control_Capabilities]']
        selected['ResearchDetail'].append((sel,loc(f'cw_sr_control_research_{n}','\n'.join(research))))
        conditions=[f'[CW_SR_Date_{n}]',f'[CW_SR_Funds_{n}]',f'[CW_SR_Debt_{n}]',f'[CW_SR_Review_{n}]']
        if p.get('windowCycleMonths') or 'fixedWindowStartMonth' in p:conditions+=[f'[CW_SR_Window_{n}]']
        selected['Conditions'].append((sel,loc(f'cw_sr_control_conditions_{n}','\n'.join(conditions))))
        for j in range(4):
            label='No additional precursor required.' if not groups and j==0 else ''
            if j<len(groups):
                group=groups[j];label=ps[ids[group[0]]-1]['name'] if len(group)==1 else ('Accepted orbital station (any architecture)' if group[0]=='salyut' else 'Accepted crewed lunar expedition (either architecture)')
                receipt=f'CW_SR_Control_Receipt_{n}_{j}'
                hist='OR = { '+''.join('has_country_flag = cw_sr_heritage_'+str(ids[item])+' ' for item in group)+' }'
                defs+=define(receipt,[(hist,loc(f'cw_sr_control_history_{n}_{j}','§GACCEPTED BEFORE 1970§!')),(qualified(group,ids),loc('cw_sr_control_met','§GACCEPTED§!'))],loc('cw_sr_control_missing_label','§RREQUIRED§!'))
                label+='\n['+receipt+']'
            pre[j].append((sel,loc(f'cw_sr_control_precursor_{n}_{j}',label)))
        entries=[(f'has_country_flag = cw_sr_institution_{n}',('Established before 1970','This institution is already established. Review the national programme record.')),(('has_country_flag = cw_sr_p'+str(n)+'_awarded has_country_flag = cw_sr_p'+str(n)+'_deployed') if p.get('commissioningOnly') else 'always = no',('Programme completed','Operations are active. Further acceptance is not required.')),(cv(state,'=',4),('Flight in progress','Maintain mission operations. Await the final objective and recovery report.')),(cv(state,'=',6),('Funded investigation required','Provide weekly corrective-engineering funding before another attempt.')),(cv(state,'=',1),('Paid engineering in progress','Maintain the weekly appropriation until engineering and qualification are complete.')),(f'cw_sr_p{n}_launch_allowed = yes',('§GReady for mission authorisation§!','Review the full mission appropriation, safety assessment and required return.')),(f'cw_sr_p{n}_start_allowed = yes',('Development can be authorised','Set the weekly development ceiling. Research and precursor flights may proceed in parallel.')),(f'NOT = {{ cw_sr_p{n}_technology = yes }}',('Required flight research missing','Complete the researched launch vehicle and payload requirements.')),(cv('cw_sr_control_missing','>',0),('Successful precursor flights required','Open the missing precursor programme and complete its accepted mission.')),(cv('cw_sr_control_caps_missing','>',0),('Supporting national capacity required','Review national capabilities and establish the required institutions or support programmes.')),(cv(var(n,'arrears'),'>=',.001),('Unpaid programme charges','Pay outstanding programme invoices before authorising departure.')),(cv('treasury','<',p['missionCostB']),('Mission appropriation unavailable','Provide sufficient treasury funds for the full mission appropriation.'))]
        # IMPERIA COLD WAR — Show the actual outstanding crew agreement.
        from crew import eligible as crew_eligible, funds as crew_funds
        if crew_eligible(p):
            entries.insert(-1,(f'NOT = {{ cw_sr_p{n}_crew_ready = yes }}',('Joint crew not cleared','Open Crew & international participation. Obtain partner approval, funded joint training and departure contributions.')))
            entries[-1]=('NOT = { '+crew_funds(c,n,p)+' }',('Mission appropriation unavailable','Provide the national share of the departure appropriation.'))
        from cooperation import eligible as op_eligible, funds as op_funds
        if op_eligible(p):
            entries.insert(-1,(f'NOT = {{ cw_sr_p{n}_operations_ready = yes }}',('Operational partner not cleared','Review the signed work package, paid interface qualification, partner capabilities and departure allocation.')))
            entries[-1]=('NOT = { '+op_funds(c,n,p)+' }',('Mission appropriation unavailable','Provide the national departure appropriation shown under International operations.'))
        b=[];nt=[]
        for i,(condition,(short,long)) in enumerate(entries):
            b.append((condition,loc(f'cw_sr_control_block_{n}_{i}',short)))
            nt.append((sel+' '+condition,loc(f'cw_sr_control_next_{n}_{i}',short+'\n'+long)))
        fallback=loc('cw_sr_control_review','Review mission authorisation')
        defs+=define(f'CW_SR_Control_Block_{n}',b,fallback);selected['Blocker'].append((sel,loc(f'cw_sr_control_block_pick_{n}',f'[CW_SR_Control_Block_{n}]')));nexts+=nt
        # Choose the first outstanding group. An already-started alternative is
        # preferred, so opening a requirement does not force a different station.
        pick=''
        for group in groups:
            chosen=sv('cw_sr_control_target',ids[group[0]],True)
            for item in reversed(group):chosen+=block_if(cv(var(ids[item],'state'),'>',0),sv('cw_sr_control_target',ids[item],True))
            pick+=block_if(cv('cw_sr_control_found','=',0)+' NOT = { '+qualified(group,ids)+' }',chosen+sv('cw_sr_control_found',1,True))
        focus+=block_if(sel,pick)
    for key,entries in selected.items():defs+=define('CW_SR_Control_'+key,entries,loc('cw_sr_control_empty',''))
    for j,entries in enumerate(pre):defs+=define('CW_SR_Control_Precursor_'+str(j),entries,'cw_sr_control_empty')
    defs+=define('CW_SR_Control_Capabilities',[(cv('cw_sr_control_caps_missing','=',0),loc('cw_sr_control_caps_met','§GMET§!  National capabilities'))],loc('cw_sr_control_caps_missing','§RMISSING§!  [?cw_sr_control_caps_missing|0] national capabilities'))
    defs+=define('CW_SR_Control_Research',[(f'cw_sr_p{n}_technology = yes '+cv('cw_sr_selected','=',n),loc('cw_sr_control_researched','§GAvailable§!')) for n in range(1,85)],loc('cw_sr_control_tech_missing','§RResearch required§!'))
    defs+=define('CW_SR_Control_Engineering',[(cv('cw_sr_selected','=',n)+f' has_country_flag = cw_sr_institution_{n}',loc('cw_sr_control_inherited_engineering','Established before 1970')) for n in range(1,85)]+[(cv('cw_sr_view_state','=',s),loc('cw_sr_control_engineering_'+str(s),label)) for s,label in [(3,'§GQualified§!'),(4,'§GQualified at departure§!'),(5,'§GQualified§!'),(6,'§RInvestigation required§!')]],loc('cw_sr_control_engineering_pending','[?cw_sr_view_progress|0]% funded development'))
    defs+=define('CW_SR_Control_Precursors',[(cv('cw_sr_control_total','=',0),loc('cw_sr_control_no_precursors','No precursor required'))],loc('cw_sr_control_precursors_count','[?cw_sr_control_accepted|0] / [?cw_sr_control_total|0] accepted'))
    defs+=define('CW_SR_Control_Authority',[(cv('cw_sr_selected','=',n)+f' has_country_flag = cw_sr_institution_{n}',loc('cw_sr_control_inherited_authority','No new acceptance required')) for n in range(1,85)]+[(cv('cw_sr_view_state','=',4),loc('cw_sr_control_underway','Mission under way'))]+[(cv('cw_sr_selected','=',n)+f' cw_sr_p{n}_launch_allowed = yes',loc('cw_sr_control_ready','§GReady for authorisation§!')) for n in range(1,85)],loc('cw_sr_control_withheld','Approval withheld'))
    defs+=define('CW_SR_AtlasNext',nexts,loc('cw_sr_control_next_fallback','Review the mission requirements.\nCheck the development calendar, qualification, support systems and departure opportunity.'))
    c['write']('common/scripted_effects/COLDWAR_space_race_control.txt',effect('cw_sr_mission_control_refresh',refresh)+effect('cw_sr_open_control',block_if(c['guard'](),sv('cw_sr_tab',8)+'clr_country_flag = cw_sr_requirements_open\ncw_sr_selected_map = yes\n'))+effect('cw_sr_control_focus_requirement',block_if(c['guard'](),sv('cw_sr_control_found',0,True)+focus+block_if(cv('cw_sr_control_found','=',1),block_if(cv('cw_sr_control_parent','=',0),sv('cw_sr_control_parent','cw_sr_selected'))+sv('cw_sr_control_child','cw_sr_control_target')+sv('cw_sr_selected','cw_sr_control_target')+'cw_sr_selected_map = yes\n'+sv('cw_sr_tab',8))))+effect('cw_sr_control_return',block_if(c['guard']()+' '+cv('cw_sr_control_parent','>',0)+' '+cv('cw_sr_control_parent','<',85),sv('cw_sr_selected','cw_sr_control_parent')+sv('cw_sr_control_parent',0)+'cw_sr_selected_map = yes\n'+sv('cw_sr_tab',8))))
    loc('cw_sr_leadership_tt','[CW_SR_Leader]\n[CW_SR_Leader_Benefit]')
    for n,p in enumerate(ps,1):loc(f'cw_sr_p{n}_atlas_card',p['name']+'\n[CW_SR_Readiness_'+str(n)+']')
    return defs


# IMPERIA COLD WAR — Flat institutional chrome and selected programme surfaces.
def backgrounds(c,texture):
    im=Image.new('RGBA',(1240,1040),'#111b22');d=ImageDraw.Draw(im)
    d.rectangle((0,0,1239,83),fill='#223037');d.rectangle((0,132,1239,171),fill='#1b282e');d.rectangle((0,175,1239,236),fill='#17232a')
    d.rectangle((900,238,1239,1023),fill='#1b292f')
    for y in [83,130,172,236,1023]:d.line((0,y,1239,y),fill='#35454b')
    d.line((900,238,900,1023),fill='#35454b')
    for y in [379,508,659,775,917]:d.line((920,y,1219,y),fill='#35454b')
    d.rectangle((916,778,1223,816),fill='#27302c');d.rectangle((0,0,1239,1039),outline='#5d6d70')
    texture('panel',im)
    texture('details_bg',Image.new('RGBA',(900,760),'#142028'));texture('wide_bg',Image.new('RGBA',(1240,760),'#142028'))
    control=Image.new('RGBA',(900,786),'#142021');dr=ImageDraw.Draw(control)
    for y in [286,632]:dr.line((30,y,876,y),fill='#3b4b48')
    dr.line((410,310,410,625),fill='#3b4b48')
    texture('control_bg',control)
    strip=Image.new('RGBA',(4*6,80),(0,0,0,0));dr=ImageDraw.Draw(strip)
    for i,color in enumerate(['#617178','#91b495','#86b8c2','#cbb580','#ce9682','#b8a478']):dr.rectangle((i*4,0,i*4+3,79),fill=color)
    texture('programme_state_strip',strip,6)
    for name,size in [('row_active',(421,80)),('nav_active',(168,34)),('node_active',(146,43)),('scale_active',(208,28))]:
        active=Image.new('RGBA',size,(0,0,0,0));dr=ImageDraw.Draw(active)
        if name=='nav_active':dr.line((0,size[1]-2,size[0]-1,size[1]-2),fill='#cbb580',width=2)
        else:dr.rectangle((0,0,size[0]-1,size[1]-1),outline='#b8a274');dr.rectangle((0,0,2,size[1]-1),fill='#cbb580')
        texture(name,active)


# IMPERIA COLD WAR — Code-native map composition from existing approved artwork.
def maps(c,texture):
    from illustrations import planet
    import random
    for scale in [1,2,3]:
        im=ImageOps.fit(Image.open(c['ASSETS']/'earth-moon-map-v1.png').convert('RGB'),MAP[2:],method=Image.Resampling.LANCZOS)
        im=ImageEnhance.Brightness(im).enhance(.82 if scale==1 else .9);d=ImageDraw.Draw(im)
        if scale==1:
            for rx,ry in [(206,179),(270,192),(97,200),(335,143)]:d.ellipse((330-rx,220-ry,330+rx,220+ry),outline='#46616a')
        elif scale==2:
            d.arc((490,80,825,286),10,280,fill='#59777c');d.line((430,160,825,160),fill='#425a63')
        else:
            im=Image.new('RGB',MAP[2:],'#081118');d=ImageDraw.Draw(im)
            for x in range(0,856,107):d.line((x,0,x,412),fill='#10232c')
            for y in range(0,412,82):d.line((0,y,856,y),fill='#10232c')
            rng=random.Random(1970)
            for _ in range(230):d.point((rng.randrange(856),rng.randrange(412)),fill=rng.choice(['#1c303b','#3a5059','#647780']))
            for rx,ry in [(118,72),(227,133),(359,187),(547,235)]:d.ellipse((144-rx,242-ry,144+rx,242+ry),outline='#344f5a')
            for x,y,r,color in [(144,242,24,'#ddc286'),(261,216,8,'#b69c78'),(364,223,9,'#77aebc'),(478,148,9,'#c68462'),(659,254,17,'#b8a185'),(765,106,13,'#aca28d')]:planet(d,x,y,r,color)
        d.rectangle((0,0,855,411),outline='#354850')
        texture('map_'+str(scale),im)
