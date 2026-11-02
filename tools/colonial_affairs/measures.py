# IMPERIA COLD WAR — Native trigger compatibility integration.
# IMPERIA CW — Cold War: differentiated domestic security and political measures.
"""Historically grounded cabinet choices. See MEASURES_HISTORY.md.

All numbers are authored gameplay values. Existing German RAF simulation and
action providers remain authoritative; no parallel arrest/hostage model exists.
"""
from runtime import HEADER, block, iff


IRA = [
 dict(id='casework',name='Evidence-led Casework',pp=20,cash='.025',days=180,cd=180,weekly='.003',
      guard='has_intelligence_agency = yes',
      result='17 = { add_to_variable = { COLDWAR_COL_cells = -2 } }',
      terms='20 PP / $0.025bn + $0.003bn/week\n180 days / Organisation -2, then -0.5/month',
      detail='Requires an intelligence agency. Fund evidence-led investigations for 180 days. Organisation strength −2 immediately and −0.5 each month. Cooldown: 180 days.'),
 dict(id='reform',name='Fair Employment and Complaints',pp=30,cash='.04',days=180,cd=365,weekly='.004',
      guard='17 = { NOT = { has_state_flag = COLDWAR_COL_measure_internment_live } check_variable = { COLDWAR_COL_tension > 27 } }',
      result='17 = { add_to_variable = { COLDWAR_COL_tension = -8 } }',
      terms='30 PP / $0.040bn + $0.004bn/week\n180 days / Tension -8, then -1/month',
      detail='Employment review and an independent complaints process address community grievances. Tension −8 immediately and −1 each month for 180 days. Cannot begin during internment. Cooldown: 365 days.'),
 dict(id='internment',name='Emergency Internment',pp=45,cash='.02',days=90,cd=365,weekly='.006',
      guard='17 = { check_variable = { COLDWAR_COL_cells > 44 } NOT = { has_state_flag = COLDWAR_COL_measure_ceasefire_live } NOT = { has_state_flag = COLDWAR_COL_measure_roundtable_live } NOT = { has_state_flag = COLDWAR_COL_measure_reform_live } }',
      result='add_stability = -0.01\n17 = { add_to_variable = { COLDWAR_COL_cells = -8 } add_to_variable = { COLDWAR_COL_tension = 15 } }',
      terms='45 PP / $0.020bn + $0.006bn/week\n90 days / Organisation -8; tension +15',
      detail='Requires organisation strength above 44 and no ceasefire, constitutional roundtable or active employment reform. Detention without trial: organisation −8 immediately; tension +15; national stability −1%; local manpower −3% for 90 days. Recruitment pressure adds +1.5 organisation per month during detention. Cooldown: 365 days.'),
 dict(id='release',name='Review Emergency Detention',pp=15,cash='0',days=0,cd=0,weekly='0',
      guard='17 = { has_state_flag = COLDWAR_COL_measure_internment_live }',
      result='17 = { clr_state_flag = COLDWAR_COL_measure_internment_live add_to_variable = { COLDWAR_COL_cells = 3 } add_to_variable = { COLDWAR_COL_tension = -8 } }',
      terms='15 PP / End internment and its weekly cost\nOrganisation +3 / Community tension -8',
      detail='End the current emergency detention programme. Its weekly appropriation, local manpower restriction and recruitment penalty end. Organisation +3 as detainees return; community tension −8. The original internment cooldown remains.'),
 dict(id='backchannel',name='Confidential Ceasefire Contacts',pp=25,cash='.015',days=0,cd=180,weekly='0',
      guard='17 = { NOT = { has_state_flag = COLDWAR_COL_measure_internment_live } NOT = { has_state_flag = COLDWAR_COL_measure_ceasefire_live } check_variable = { COLDWAR_COL_tension < 71 } }',
      result='''random_list = {
60 = { 17 = { set_state_flag = { flag = COLDWAR_COL_measure_ceasefire_live days = 90 } add_to_variable = { COLDWAR_COL_tension = -5 } } country_event = { id = COLDWAR_colonial_contacts.4 } }
40 = { add_stability = -0.005 17 = { add_to_variable = { COLDWAR_COL_tension = 5 } } country_event = { id = COLDWAR_colonial_contacts.5 } }
}''',
      terms='25 PP / $0.015bn / 60% ceasefire chance\nSuccess: 90 days, $0.002bn/week; tension -5',
      detail='Requires tension below 71 and no internment or active ceasefire. 60%: a 90-day ceasefire, tension −5, organisation −0.5/month and a reduced monthly incident risk of 2%. Ceasefire liaison costs $0.002bn/week. 40%: talks fail, tension +5 and national stability −0.5%. External aid and recruitment remain active. Cooldown: 180 days.'),
 dict(id='roundtable',name='Constitutional Power-sharing Talks',pp=60,cash='.08',days=180,cd=365,weekly='.006',
      guard='17 = { has_state_flag = COLDWAR_COL_measure_ceasefire_live check_variable = { COLDWAR_COL_tension < 46 } check_variable = { COLDWAR_COL_local_aid < 6 } NOT = { has_state_flag = COLDWAR_COL_measure_internment_live } }',
      result='add_stability = -0.015\n17 = { add_to_variable = { COLDWAR_COL_tension = -10 } }\ncountry_event = { id = COLDWAR_colonial_contacts.6 days = 60 }',
      terms='60 PP / $0.080bn + $0.006bn/week\n180 days / Tension -10; stability -1.5%',
      detail='Convene constitutional parties around power-sharing. Requires an active ceasefire, tension below 46, foreign aid below 6 and no internment. Tension −10 immediately, then −1/month; organisation −0.5/month for 180 days. National stability −1.5%. After 60 days: 30% chance of obstruction ending talks and the ceasefire, adding +10 tension and +3 organisation. This is not an IRA disarmament agreement. Cooldown: 365 days.'),
]
# IMPERIA CW — Cold War: one programme catalogue shared with the German security cabinet.
import json
from pathlib import Path
RAF = json.loads((Path(__file__).parent/'raf_programmes.json').read_text(encoding='utf-8'))

# Existing native actions: their own effects, unlocks, prices and cooldowns apply.
NATIVE = [
 dict(id='posters',name='Publish Wanted Notices',terms='40 PP / 180-day cooldown\nTrace +4 / Cadres -1 / Milieu +1'),
 dict(id='raster',name='Computer Dragnet',terms='50 PP / BKA level 3 / 240-day cooldown\nTrace +10 / Rule of law -3 / Security +2'),
 dict(id='kronzeuge',name='Crown Witness Cooperation',terms='50 PP / Witness provision / 365-day cooldown\nBest wanted trace +25 / Milieu -2'),
 dict(id='dropout',name='Offer an Exit Programme',terms='50 PP / Exit provision / 365-day cooldown\nCadres -2 / Milieu -5 / One member leaves'),
]
for row in IRA+RAF:
    for key in ('cash','weekly'):
        if row[key].startswith('.'):row[key]='0'+row[key]


def change(name, amount, low=0, high=100):
    return f'add_to_variable = {{ {name} = {amount} }}\nclamp_variable = {{ var = {name} min = {low} max = {high} }}\n'


def build(files, local):
    trig=[];effects=[]
    add_effect=lambda name,code:effects.append(block(name,code))
    add_trigger=lambda name,code:trig.append(block(name,code))
    add_trigger('COLDWAR_COL_measure_ira_available','COLDWAR_COL_contacts_scenario = yes\ntag = ENG\nCOLDWAR_COL_ira_active = yes')
    add_trigger('COLDWAR_COL_measure_raf_available','COLDWAR_COL_contacts_scenario = yes\nCOLDWAR_COL_can_open_raf = yes')
    add_effect('COLDWAR_COL_measures_initialize',iff('NOT = { has_variable = COLDWAR_COL_tension }','set_variable = { COLDWAR_COL_tension = 55 }'))
    clamp_ira='17 = { clamp_variable = { var = COLDWAR_COL_cells min = 25 max = 90 } clamp_variable = { var = COLDWAR_COL_tension min = 20 max = 95 } COLDWAR_COL_measure_state_budget = yes COLDWAR_COL_apply_domestic = yes }\nCOLDWAR_COL_refresh_case = yes'
    clamp_raf='\n'.join(f'clamp_variable = {{ var = {var} min = 0 max = 100 }}' for var in ('cwger_raf_milieu','cwger_rechtsstaat','cwger_security','cwsec_hunger'))
    trace=lambda amount:'\n'.join(iff(f'check_variable = {{ cwsec_w{i}_st < 2 }}',change(f'cwsec_w{i}_ort',amount)) for i in range(1,7))
    for group,actions in [('ira',IRA),('raf',RAF)]:
        for row in actions:
            key=row['id'];name='COLDWAR_COL_measure_'+key
            if group=='raf':
                # The German cabinet owns payment, flags, focus unlock and effects.
                add_trigger(name+'_available','COLDWAR_GER_1970_sec_can_'+key+' = yes')
                add_effect(name,'COLDWAR_GER_1970_sec_act_'+key+' = yes')
                local[name]=row['name'];local[name+'_terms']=row['terms']
                local[name+'_label']='[COLDWAR_COL_GetMeasure_'+key+'_Label]'
                local[name+'_active']=row['name']+' [active]'
                focus={'bka_expansion':'BKA Expansion','data_protection':'Data Protection','stammheim_trial':'The Stammheim Trial'}[row['focus']]
                local[name+'_tt']=row['terms'].replace('\n','; ')+'. '+row['detail']+' Requires §Y'+focus+'§!.'
                continue
            cooldown=f'NOT = {{ has_{"state" if group=="ira" else "country"}_flag = {name}_cooldown }}'
            if group=='ira':cooldown='17 = { '+cooldown+' }'
            gate=f'COLDWAR_COL_measure_{group}_available = yes\n{cooldown}\nNOT = {{ has_political_power < {row["pp"]} }}\n'+row['guard']
            if row['cash']!='0':gate+=f'\nNOT = {{ has_country_flag = MD_skip_treasury_cost }}\ncheck_variable = {{ var = treasury value = {row["cash"]} compare = greater_than_or_equals }}'
            add_trigger(name+'_available',gate)
            code=f'add_political_power = -{row["pp"]}\n'
            if row['cash']!='0':code+=f'set_temp_variable = {{ treasury_change = -{row["cash"]} }}\nmodify_treasury_effect = yes\n'
            flags=''
            for suffix,days in [('cooldown',row['cd']),('live',row['days'])]:
                if days:flags+=f'set_{"state" if group=="ira" else "country"}_flag = {{ flag = {name}_{suffix} days = {days} }}\n'
            code+=block('17',flags) if group=='ira' and flags else flags
            code+=row['result']+'\n'
            if key=='coordination':code+=trace(8)
            if group=='ira':code+=clamp_ira
            else:code+=clamp_raf
            # Reconcile flags/aid again at payment, not only at dossier open.
            prepare='COLDWAR_COL_prepare_measures = yes\n'
            add_effect(name,prepare+iff(name+'_available = yes',code))
            local[name]=row['name'];local[name+'_terms']=row['terms']
            if row['days'] or key=='backchannel':
                local[name+'_label']='[COLDWAR_COL_GetMeasure_'+key+'_Label]'
                local[name+'_active']=row['name']+' [active]'
            local[name+'_tt']=f'§Y{row["pp"]} Political Power'+(f'; ${float(row["cash"]):.3f}bn' if row['cash']!='0' else '')+'§!. '+row['detail']+(f' Standing appropriation: §Y${float(row["weekly"]):.3f}bn/week§!.' if row['weekly']!='0' else '')
    for row in NATIVE:
        key=row['id'];name='COLDWAR_COL_measure_native_'+key
        add_trigger(name+'_available','COLDWAR_COL_measure_raf_available = yes\nCOLDWAR_GER_1970_sec_can_'+key+' = yes')
        add_effect(name,iff(name+'_available = yes','COLDWAR_GER_1970_sec_act_'+key+' = yes'))
        local[name]=row['name'];local[name+'_terms']=row['terms']
        local[name+'_tt']=row['terms'].replace('\n','; ')+'. '+{
            'posters':'Requires left-wing terror pressure above 20. Security +2. Only wanted persons still at large gain trace.',
            'raster':'Requires the dragnet doctrine, BKA level 3 and more than 3 cadres. Only wanted persons still at large gain trace.',
            'kronzeuge':'Requires the crown-witness provision and more than 1 RAF prisoner. Rule of law −1. The existing German investigation identifies the best lead.',
            'dropout':'Requires the exit provision and more than 2 cadres. The existing wanted-person record is updated; this does not dissolve the organisation.',
        }[key]

    state_budget='set_variable = { COLDWAR_COL_measure_cost = 0 }\n'
    for row in IRA:
        if row['days']:state_budget+=iff(f'has_state_flag = COLDWAR_COL_measure_{row["id"]}_live',f'add_to_variable = {{ COLDWAR_COL_measure_cost = {row["weekly"]} }}')
    state_budget+=iff('has_state_flag = COLDWAR_COL_measure_ceasefire_live','add_to_variable = { COLDWAR_COL_measure_cost = 0.002 }')
    add_effect('COLDWAR_COL_measure_state_budget',state_budget)
    add_effect('COLDWAR_COL_prepare_measures',iff('COLDWAR_COL_measure_ira_available = yes','17 = { COLDWAR_COL_measures_initialize = yes COLDWAR_COL_refresh_local_aid = yes COLDWAR_COL_measure_state_budget = yes }'))
    add_effect('COLDWAR_COL_measures_budget',iff('COLDWAR_COL_measure_ira_available = yes','17 = { COLDWAR_COL_measure_state_budget = yes }\nadd_to_variable = { COLDWAR_COL_domestic_weekly_cost = 17.COLDWAR_COL_measure_cost }')+'\n'+iff('tag = GER','COLDWAR_GER_1970_security_weekly_budget = yes\nadd_to_variable = { COLDWAR_COL_domestic_weekly_cost = cwsec_program_weekly_cost }'))
    add_effect('COLDWAR_COL_refresh_measures_view',iff('COLDWAR_COL_case_target_available = yes','var:COLDWAR_COL_case_target = { COLDWAR_COL_measures_initialize = yes COLDWAR_COL_measure_state_budget = yes set_variable = { PREV.COLDWAR_COL_case_tension = COLDWAR_COL_tension } set_variable = { PREV.COLDWAR_COL_case_measure_cost = COLDWAR_COL_measure_cost } }\nadd_to_variable = { COLDWAR_COL_case_cost = COLDWAR_COL_case_measure_cost }'))
    ira_month=''
    for key,drift in [('casework',-.5),('internment',1.5),('ceasefire',-.5),('roundtable',-.5)]:
        ira_month+=iff(f'has_state_flag = COLDWAR_COL_measure_{key}_live',f'add_to_temp_variable = {{ COLDWAR_COL_case_drift = {drift} }}')
    for key in ('reform','roundtable'):
        ira_month+=iff(f'has_state_flag = COLDWAR_COL_measure_{key}_live','add_to_variable = { COLDWAR_COL_tension = -1 }')
    ira_month+=iff('check_variable = { COLDWAR_COL_tension > 69 }','add_to_temp_variable = { COLDWAR_COL_case_drift = 0.5 }')
    ira_month+=iff('check_variable = { COLDWAR_COL_tension < 36 }','add_to_temp_variable = { COLDWAR_COL_case_drift = -0.5 }')
    ira_month+='clamp_variable = { var = COLDWAR_COL_tension min = 20 max = 95 }'
    add_effect('COLDWAR_COL_measures_ira_monthly',ira_month)
    # A ceasefire reduces, rather than eliminates, the chance of spoiler violence.
    incident='controller = { set_country_flag = { flag = COLDWAR_COL_incident_recent days = 90 } country_event = { id = COLDWAR_colonial_contacts.3 } }'
    add_effect('COLDWAR_COL_measures_incident',iff('check_variable = { COLDWAR_COL_cells > 44 }\ncontroller = { NOT = { has_country_flag = COLDWAR_COL_incident_recent } }',iff('has_state_flag = COLDWAR_COL_measure_ceasefire_live',block('random_list',block('98','')+block('2',incident)),iff('check_variable = { COLDWAR_COL_tension > 69 }',block('random_list',block('75','')+block('25',incident)),block('random_list',block('85','')+block('15',incident))))))
    add_effect('COLDWAR_COL_measures_country_monthly','# RAF programmes have one dispatcher: COLDWAR_GER_1970_monthly.')
    cleanup='17 = { '+ ' '.join('clr_state_flag = COLDWAR_COL_measure_'+key+'_live' for key in [r['id'] for r in IRA]+['ceasefire'])+' set_variable = { COLDWAR_COL_measure_cost = 0 } }'
    add_effect('COLDWAR_COL_measures_daily',iff('tag = ENG\nCOLDWAR_COL_ira_active = no',cleanup))
    add_effect('COLDWAR_COL_measures_local_restrictions',iff('has_state_flag = COLDWAR_COL_measure_internment_live','add_to_variable = { COLDWAR_COL_domestic_workforce = -0.03 }'))

    events='''country_event = {
id = COLDWAR_colonial_contacts.4
title = COLDWAR_COL_ceasefire_title
desc = COLDWAR_COL_ceasefire_desc
is_triggered_only = yes
option = { name = COLDWAR_COL_measure_acknowledge }
}
country_event = {
id = COLDWAR_colonial_contacts.5
title = COLDWAR_COL_talks_failed_title
desc = COLDWAR_COL_talks_failed_desc
is_triggered_only = yes
option = { name = COLDWAR_COL_measure_acknowledge }
}
country_event = {
id = COLDWAR_colonial_contacts.6
title = COLDWAR_COL_roundtable_title
desc = COLDWAR_COL_roundtable_desc
is_triggered_only = yes
hidden = yes
immediate = {
 if = {
 limit = { COLDWAR_COL_measure_ira_available = yes 17 = { has_state_flag = COLDWAR_COL_measure_roundtable_live } }
 random_list = {
 70 = { }
 30 = { 17 = { clr_state_flag = COLDWAR_COL_measure_roundtable_live clr_state_flag = COLDWAR_COL_measure_ceasefire_live add_to_variable = { COLDWAR_COL_tension = 10 } add_to_variable = { COLDWAR_COL_cells = 3 } clamp_variable = { var = COLDWAR_COL_tension min = 20 max = 95 } clamp_variable = { var = COLDWAR_COL_cells min = 25 max = 90 } } COLDWAR_COL_refresh_case = yes country_event = { id = COLDWAR_colonial_contacts.7 } }
 }
 }
}
}
country_event = {
id = COLDWAR_colonial_contacts.7
title = COLDWAR_COL_roundtable_title
desc = COLDWAR_COL_roundtable_desc
is_triggered_only = yes
option = { name = COLDWAR_COL_measure_acknowledge }
}
'''
    files['events/COLDWAR_colonial_contacts.txt']+='\n'+HEADER+events
    files['common/scripted_effects/COLDWAR_colonial_measures.txt']=HEADER+'\n'.join(effects)
    files['common/scripted_triggers/COLDWAR_colonial_measures.txt']=HEADER+'\n'.join(trig)
    local.update({
      'COLDWAR_COL_measures_toggle':'[COLDWAR_COL_GetMeasuresLabel]',
      'COLDWAR_COL_measures_open':'Measures','COLDWAR_COL_measures_close':'Overview',
      'COLDWAR_COL_measures_toggle_tt':'Review organisation-specific security measures and political initiatives. Costs, commitments, requirements and consequences appear on each file.',
      'COLDWAR_COL_measures_heading':'SECURITY AND POLITICAL MEASURES',
      'COLDWAR_COL_measures_page':'MEASURES / [COLDWAR_COL_GetMeasuresPage]',
      'COLDWAR_COL_measures_page_1':'FILE 1 OF 2','COLDWAR_COL_measures_page_2':'FILE 2 OF 2',
      'COLDWAR_COL_measures_previous_tt':'Previous measures file','COLDWAR_COL_measures_next_tt':'Next measures file',
      'COLDWAR_COL_case_tension':'Community tension [?COLDWAR_COL_case_tension|0]%',
      'COLDWAR_COL_case_tension_tt':'Community tension is distinct from IRA organisation strength. Above 69: recruitment +0.5/month and monthly incident risk 25%, if organisation is above 44. Below 36: recruitment −0.5/month. A ceasefire reduces the incident risk to 2%. Otherwise the risk is 15%. Each incident imposes a 90-day cooldown. Tension is bounded between 20 and 95.',
      'COLDWAR_COL_ceasefire_title':'A provisional ceasefire',
      'COLDWAR_COL_ceasefire_desc':'Intermediaries have secured a temporary cessation. Constitutional negotiations remain separate, and neither disarmament nor a final settlement has been agreed.',
      'COLDWAR_COL_talks_failed_title':'Contacts break down',
      'COLDWAR_COL_talks_failed_desc':'The intermediaries cannot secure agreement on a cessation. The government faces criticism for a contact process that has yielded no result.',
      'COLDWAR_COL_roundtable_title':'Power-sharing talks obstructed',
      'COLDWAR_COL_roundtable_desc':'Political opposition has broken the proposed constitutional process. The ceasefire has ended and community tensions are rising again.',
      'COLDWAR_COL_measure_acknowledge':'Review the security assessment.',
      'COLDWAR_COL_case_assessment':'Community tension [?COLDWAR_COL_case_tension|0]%',
    })
    return local


def add_ui(ui):
    """Two paged measures files, reached from the organisation's own dossier."""
    import json
    from PIL import ImageDraw
    from security import ROOT,HERE,save,append,setval
    from script_ast import parse,first
    gui=parse((ROOT/'interface/COLDWAR_colonial_affairs.gui').read_text())
    main=next(v for k,o,v in first(gui,'guiTypes') if first(v,'name')=='"COLDWAR_colonial_affairs_window"')
    script=parse((ROOT/'common/scripted_guis/COLDWAR_colonial_affairs_gui.txt').read_text())
    g=first(first(script,'scripted_gui'),'COLDWAR_colonial_affairs_gui')
    guards=first(g,'triggers');effects=first(g,'effects');properties=first(g,'properties')
    im=ui.paper(510,740,'SECURITY AFFAIRS','CABINET SECRETARIAT  /  TERRITORIES AND INTERNAL SECURITY')
    d=ImageDraw.Draw(im)
    ui.txt(d,(20,108),'INTERNAL SECURITY / MEASURES',11,ui.LABEL,'label')
    d.rectangle((18,138,491,229),outline='#b69a73')
    ui.line(d,254,color=ui.RUST);ui.line(d,277,color=ui.RUST)
    ui.txt(d,(20,259),'SECURITY AND POLITICAL MEASURES',13,ui.RUST,'label')
    ui.line(d,686);ui.txt(d,(20,705),'CABINET SECURITY REGISTER  /  RESTRICTED CIRCULATION',10,ui.LABEL)
    ui.save_asset('measures_sheet',im)
    gfx=parse((ROOT/'interface/COLDWAR_colonial_affairs.gfx').read_text())
    first(gfx,'spriteTypes').extend(parse('spriteType = { name = "GFX_COLDWAR_COL_measures_sheet" texturefile = "gfx/interface/coldwar_colonial/measures_sheet.dds" }'))
    save('interface/COLDWAR_colonial_affairs.gfx',gfx)
    properties.extend(parse('COLDWAR_COL_internal_page = { image = "[COLDWAR_COL_GetInternalPage]" }'))
    body=ui.button('COLDWAR_COL_measures_toggle',338,106,'section_tab','COLDWAR_COL_measures_toggle','COLDWAR_COL_measures_toggle_tt')
    common='COLDWAR_COL_tab_internal = yes OR = { COLDWAR_COL_measure_ira_available = yes COLDWAR_COL_own_raf = yes }'
    guards.extend(parse('COLDWAR_COL_measures_toggle_visible = { '+common+' }'))
    effects.extend(parse('COLDWAR_COL_measures_toggle_click = { COLDWAR_COL_prepare_measures = yes COLDWAR_COL_refresh_case = yes set_variable = { COLDWAR_COL_measure_page = 0 } if = { limit = { has_country_flag = COLDWAR_COL_measures_open } clr_country_flag = COLDWAR_COL_measures_open } else = { set_country_flag = COLDWAR_COL_measures_open } }'))
    overview=[f'COLDWAR_COL_case_{i}' for i in range(3)]+[f'COLDWAR_COL_case_caption_{i}' for i in range(3)]+['COLDWAR_COL_case_budget','COLDWAR_COL_case_lock','COLDWAR_COL_case_footer','COLDWAR_COL_open_raf','COLDWAR_COL_raf_note','COLDWAR_COL_raf_budget']
    for widget in overview:
        old=first(guards,widget+'_visible',[])
        setval(guards,widget+'_visible',old+parse('NOT = { has_country_flag = COLDWAR_COL_measures_open }'))
    for k,o,node in main:
        if k=='instantTextBoxType' and first(node,'name')=='"COLDWAR_COL_case_assessment"':
            setval(node,'pdx_tooltip','"COLDWAR_COL_case_tension_tt"')
    widgets={};labels=''
    for group,rows in [('ira',IRA),('raf',RAF+NATIVE)]:
        for index,row in enumerate(rows):
            native=group=='raf' and row in NATIVE
            name='COLDWAR_COL_measure_'+('native_' if native else '')+row['id']
            page=index//4;y=360+(index%4)*74
            label=name
            if not native and (row['days'] or row['id']=='backchannel'):
                label=name+'_label'
                flag='COLDWAR_COL_measure_'+('ceasefire' if row['id']=='backchannel' else row['id'])+'_live'
                condition=f'has_{"state" if group=="ira" else "country"}_flag = {flag}'
                if group=='ira':condition='17 = { '+condition+' }'
                labels+=ui.defined('COLDWAR_COL_GetMeasure_'+row['id']+'_Label',[(condition,name+'_active')],name)
            body+=ui.button(name,20,y,'wide',label,name+'_tt')
            body+=ui.text(name+'_terms',20,y+32,470,34)
            guard=f'COLDWAR_COL_tab_internal = yes COLDWAR_COL_measure_{group}_available = yes has_country_flag = COLDWAR_COL_measures_open '
            guard+=('NOT = { check_variable = { COLDWAR_COL_measure_page = 1 } }' if page==0 else 'check_variable = { COLDWAR_COL_measure_page = 1 }')
            for widget in (name,name+'_terms'):
                guards.extend(parse(widget+'_visible = { '+guard+' }'))
                widgets[widget]=dict(group=group,page=page)
            guards.extend(parse(name+'_click_enabled = { '+name+'_available = yes }'))
            effects.extend(parse(name+'_click = { '+name+' = yes }'))
            ui.LOC[name]=row['name'];ui.LOC[name+'_terms']=row['terms']
    navigation=['COLDWAR_COL_measures_page','COLDWAR_COL_measures_previous','COLDWAR_COL_measures_next']
    body+=ui.text('COLDWAR_COL_measures_page',20,661,360,20)
    for key,x in [('previous',421),('next',459)]:
        name='COLDWAR_COL_measures_'+key
        body+=ui.button(name,x,655,'nav','COLDWAR_COL_'+key+'_short',name+'_tt')
        effects.extend(parse(name+'_click = { if = { limit = { check_variable = { COLDWAR_COL_measure_page = 1 } } set_variable = { COLDWAR_COL_measure_page = 0 } } else = { set_variable = { COLDWAR_COL_measure_page = 1 } } }'))
    for name in navigation:guards.extend(parse(name+'_visible = { '+common+' has_country_flag = COLDWAR_COL_measures_open }'))
    main.extend(parse(body));save('interface/COLDWAR_colonial_affairs.gui',gui)
    save('common/scripted_guis/COLDWAR_colonial_affairs_gui.txt',script)
    loc=ui.defined('COLDWAR_COL_GetInternalPage',[('has_country_flag = COLDWAR_COL_measures_open','GFX_COLDWAR_COL_measures_sheet')],'GFX_COLDWAR_COL_register_internal')
    loc+=ui.defined('COLDWAR_COL_GetMeasuresLabel',[('has_country_flag = COLDWAR_COL_measures_open','COLDWAR_COL_measures_close')],'COLDWAR_COL_measures_open')
    loc+=ui.defined('COLDWAR_COL_GetMeasuresPage',[('check_variable = { COLDWAR_COL_measure_page = 1 }','COLDWAR_COL_measures_page_2')],'COLDWAR_COL_measures_page_1')
    append('common/scripted_localisation/COLDWAR_colonial_affairs_gui.txt',loc+labels)
    ui.LOC.update(COLDWAR_COL_case_assessment='Community tension [?COLDWAR_COL_case_tension|0]%')
    (HERE/'ui_localisation.json').write_text(json.dumps(ui.LOC,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (HERE/'ui_measures.json').write_text(json.dumps(dict(widgets=widgets,overview=overview,navigation=navigation),indent=2)+'\n')
