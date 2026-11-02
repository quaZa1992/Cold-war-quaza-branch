# IMPERIA COLD WAR — COMECON read-only dossier data and numeric card text
from build import *
from mechanics import participants,recipients
import re
from PIL import ImageFont

def native_wrap(text,width=622,size=12,face='segoeui.ttf'):
    font=ImageFont.truetype('C:/Windows/Fonts/'+face,size)
    def measure(value):
        value=re.sub(r'\[\?[^\]]+\]','3',value)
        return sum(round(font.getlength(ch)) for ch in value)
    lines=[];line=''
    for word in text.split():
        trial=(line+' '+word).strip()
        if line and measure(trial)>width:
            lines.append(line);line=word
        else:line=trial
    if line:lines.append(line)
    return '\n'.join(lines)

def compact_rewards(s,p,o,t,host):
    buildings=base_assets(p,o,t,host);tokens=[];lines=[]
    names={'industrial_complex':'CIV','infrastructure':'INFRA','agriculture_district':'AGRI','offices':'office','supply_node':'hub'}
    if buildings:
        lines.append(' · '.join([f'+{v} {names[b]}' for b,v in buildings]+[f'+{sum(v for b,v in buildings)} slots']))
    labels={'agriculture_district_income_tax_modifier':'farm income','civilian_factories_productivity':'civilian productivity',
        'country_productivity_growth_modifier':'productivity growth','fossil_infra_cost_multiplier_modifier':'thermal upkeep',
        'fossil_pp_fuel_consumption_modifier':'thermal fuel use','local_resources_factor':'resource extraction',
        'mdcw_nuclear_safety_target':'nuclear safety','non_electric_fuel_consumption_modifier':'fuel use',
        'nuclear_fuel_consumption_modifier':'nuclear fuel use','nuclear_infra_cost_multiplier_modifier':'nuclear upkeep',
        'production_factory_efficiency_gain_factor':'production efficiency growth','production_factory_max_efficiency_factor':'production efficiency cap',
        'production_lack_of_resource_penalty_factor':'resource shortage penalty','production_speed_industrial_complex_factor':'CIV construction',
        'production_speed_infrastructure_factor':'INFRA construction','production_speed_nuclear_reactor_factor':'reactor construction',
        'production_speed_supply_node_factor':'hub construction','state_productivity_growth_modifier':'plant growth'}
    mods,research,states=offer_effects(p,o,t,host)
    for key,value in mods.items():
        number=round(value if key=='mdcw_nuclear_safety_target' else value*100);unit='' if key=='mdcw_nuclear_safety_target' else '%'
        tokens.append(f'{number:+d}{unit} {labels[key]}'+(f' ({states} '+('state' if states==1 else 'states')+')' if key=='state_productivity_growth_modifier' else ''))
    for category,value in research.items():tokens.append(f'+{value}% '+('reactor' if category=='Civilian Reactor' else category.lower())+' research')
    if o['kind']=='resource' and (not host or o.get('includeHost')):tokens.append('+1 steel')
    if o['kind']=='equipment':tokens.append(('-[?global.cc_'+str(s)+'_train_need|0]' if host else '+[?cc_'+str(s)+'_train_quota|0]')+' trains')
    if tokens:lines.extend(native_wrap(' · '.join(tokens),300,11,'cour.ttf').splitlines())
    assert len(lines)<=2,(p,o['id'],host,lines)
    return '§R'+'\n'.join(lines)+'§!'

def service_rates(p,o,t,host):
    h=DATA['hostPlans'].get(p,{})
    specialist=o['kind'] in ('modifier','shared','resource')
    national=(specialist and (not host or o['kind']=='shared' or o.get('includeHost'))) or (host and bool(h.get('programme')))
    support=host and not DATA['catalogue'][p].get('campaign') and (specialist or bool(h.get('programme')))
    return ([.006,.010,.016][t] if national else 0,[12,20,32][t] if support else 0)

def reward_lines(s,p,o,t,host=False):
    lines=[]
    buildings=base_assets(p,o,t,host)
    if buildings:
        slots=sum(v for b,v in buildings);lines.append(f'+{slots} shared building slot'+('s' if slots!=1 else ''))
        names={'industrial_complex':'civilian factory','infrastructure':'infrastructure level','agriculture_district':'agricultural district','offices':'office','supply_node':'supply hub'}
        for b,count in buildings:lines.append(f'+{count} '+names[b]+('s' if count!=1 else ''))
    mods,research,states=offer_effects(p,o,t,host)
    lookup={e['nativeKey']:e['label'] for e in o.get('effects',[])}
    lookup.update({v:k for k,v in HOST_KEYS.items()})
    days=180 if DATA['catalogue'][p].get('campaign') else 90
    for key,value in mods.items():
        numeric=round(value if key=='mdcw_nuclear_safety_target' else value*100)
        unit='' if key=='mdcw_nuclear_safety_target' else '%'
        label=lookup.get(key,key.replace('_',' '))
        target=f' in {states} selected state'+('s' if states!=1 else '') if states else ''
        lines.append(f'{numeric:+d}{unit} {label}{target} ({days} active days)')
    for category,value in research.items():lines.append(f'+{value}% {category} research speed ({days} active days)')
    if o['kind']=='resource' and (not host or o.get('includeHost')):lines.append(f'+1 steel in [?cc_{s}_site1.GetName] (permanent)')
    if o['kind']=='equipment':lines.append(('-[?global.cc_'+str(s)+'_train_need|0]' if host else '+[?cc_'+str(s)+'_train_quota|0]')+' existing trains')
    return lines

def defined(name,branches,default='cc_empty'):
    return block('defined_text','name = '+name+'\n'+'\n'.join('text = { trigger = { '+condition+' } localization_key = '+key+' }' for condition,key in branches)+'\ntext = { localization_key = '+default+' }')

def compile_view():
    local=[];effects=[MARK+' display-only dossier caches']
    for s in range(1,5):
        cards=[];fees=[];compact=[];compact_fees=[];descs=[];requires=[];headings=[];choices=[[] for _ in range(4)];summaries=[[] for _ in range(4)]
        setup=[];deliveries=[];host_requires=[]
        for i,(p,o) in enumerate(OFFERS,1):
            condition=cv(f'global.cc_{s}_offer','=',i)
            headings.append((condition,loc('cc_project_'+p,DATA['catalogue'][p]['title'])))
            descs.append((condition,loc('cc_description_'+p,native_wrap(DATA['catalogue'][p]['description']))))
            req=o['requires'].replace('[states]',f'[?global.cc_{s}_tier|0]').replace('state(s)','states')
            requires.append((condition,loc(f'cc_{s}_requires_{i}',native_wrap(req,size=11))))
            if o['kind']=='shared' or o.get('all'):
                delivery='Joint delivery: The same agreed programme for each participating country.'
                host_requirement='Participation requirements: '+req
            else:
                h=DATA['hostPlans'][p]
                delivery='Host delivery: '+h['kind']+'.'
                host_requirement='Host requirements: '+h['requires'].replace('[states]',f'[?global.cc_{s}_tier|0]').replace('state(s)','states')
            if o['kind']=='equipment':host_requirement+=' Human supplier with existing train stock.'
            deliveries.append((condition,loc(f'cc_{s}_delivery_{i}',delivery)))
            host_requires.append((condition,loc(f'cc_{s}_host_requires_{i}',native_wrap(host_requirement,size=11))))
            family=[j for j,(q,r) in enumerate(OFFERS,1) if q==p]
            number=family.index(i)
            for j,(_,choice) in enumerate([(q,r) for q,r in OFFERS if q==p]):
                choices[j].append((condition,loc('cc_offer_'+choice['id'],choice['name'].upper())))
                for t in range(3):
                    summary=reward_lines(s,p,choice,t,False)
                    summaries[j].append((condition+' '+cv(f'global.cc_{s}_tier','=',t+1),loc(f'cc_{s}_offer_summary_{i}_{j}_{t}',native_wrap(' · '.join(summary),570))))
            for t in range(3):
                for host in (True,False):
                    role=cv('THIS.id','=',f'global.cc_{s}_host')
                    role=role if host else 'NOT = { '+role+' }'
                    check=condition+' '+cv(f'global.cc_{s}_tier','=',t+1)+' '+role
                    lines=reward_lines(s,p,o,t,host)
                    cards.append((check,loc(f'cc_{s}_card_{i}_{t}_{int(host)}','\\n'.join(lines))))
                    compact.append((check,loc(f'cc_{s}_compact_{i}_{t}_{int(host)}',compact_rewards(s,p,o,t,host))))
                    national,support=service_rates(p,o,t,host)
                    detail=[]
                    if national:detail.append(f'National programme: -{national:.3f}% GDP/week')
                    if support:detail.append(f'Host support: -${support}M/week')
                    fees.append((check,loc(f'cc_{s}_fee_{i}_{t}_{int(host)}',' · '.join(detail))))
                    short=[]
                    if national:short.append(f'-{national:.3f}% GDP/w')
                    if support:short.append(f'-${support}M/w')
                    compact_fees.append((check,loc(f'cc_{s}_compact_fee_{i}_{t}_{int(host)}','\n'.join(short) if short else '0')))
                    setup.append(f'if = {{ limit = {{ {check} }} set_variable = {{ cc_{s}_detail_y = {40+21*len(lines)+5} }} }}')
        fees.insert(0,('is_ai = yes',loc('cc_passive_services','Passive recipient: no programme charge')))
        compact_fees.insert(0,('is_ai = yes',loc('cc_passive_zero','0')))
        local += [defined(f'cc_{s}_card_effects',cards),defined(f'cc_{s}_card_fees',fees),defined(f'cc_{s}_programme_name',headings),defined(f'cc_{s}_description',descs),defined(f'cc_{s}_requirements',requires),defined(f'cc_{s}_delivery',deliveries),defined(f'cc_{s}_host_requires',host_requires)]
        local += [defined(f'cc_{s}_card_compact',compact),defined(f'cc_{s}_card_compact_fees',compact_fees)]
        for j in range(4):local += [defined(f'cc_{s}_offer_name_{j}',choices[j]),defined(f'cc_{s}_offer_summary_{j}',summaries[j])]
        local.append(defined(f'cc_{s}_vote_status',[(f'is_ai = yes cc_{s}_receiving_country = yes',loc('cc_passive_recipient','Passive recipient')),(f'NOT = {{ cc_{s}_voter = yes }}',loc('cc_not_participating','Not participating')),(cv(f'cc_{s}_vote_revision','=',f'global.cc_{s}_revision'),loc('cc_yes','Approved')),(cv(f'cc_{s}_vote_revision','=',-1),loc('cc_no','Declined'))],loc('cc_wait','Awaiting signature')))
        effects.append(block(f'cc_{s}_prepare_cards',f'for_each_scope_loop = {{ array = global.cc_members set_variable = {{ cc_{s}_funding_frame = cc_{s}_share }} divide_variable = {{ cc_{s}_funding_frame = 5 }} add_to_variable = {{ cc_{s}_funding_frame = 1 }} if = {{ limit = {{ is_ai = yes }} set_variable = {{ cc_{s}_funding_frame = 1 }} }} }} clear_array = global.cc_{s}_view_recipients '+recipients(s,f'if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.cc_{s}_view_recipients value = THIS }} }} }} add_to_array = {{ global.cc_{s}_view_recipients = THIS }} }} '+' '.join(setup))))
    refresh=[]
    fields={'offer':'offer','project':'project','tier':'tier','host':'host','union':'union','cost':'cost','days':'days','weekly':'weekly','coverage':'coverage','participants':'participants','phase':'phase','remaining':'remaining','revision':'revision','period_left':'period_left'}
    for s in range(1,5):
        body=[var('cc_ui_'+name,f'global.cc_{s}_{source}') for name,source in fields.items()]
        body += [var('cc_ui_share',f'cc_{s}_share'),var('cc_ui_own_weekly',f'cc_{s}_weekly')]
        for i,(p,o) in enumerate(OFFERS,1):
            family=[r for q,r in OFFERS if q==p]
            icons=' '.join(var('cc_ui_offer_icon_'+str(j),next(k for k,(q,r) in enumerate(OFFERS,1) if r is choice)) for j,choice in enumerate(family))
            body.append(choose(f'global.cc_{s}_offer',i,var('cc_ui_offer_count',len(family))+' '+var('cc_ui_choice',family.index(o)+1)+' '+icons))
        refresh.append(choose('cc_view_slot',s,' '.join(body)))
    refresh.append('cc_ui_paginate = yes cc_office_refresh = yes')
    for pidx,p in enumerate(PROJECTS,1):refresh += [var(f'cc_ui_project_frame_{pidx}',1),choose('cc_ui_project',pidx,var(f'cc_ui_project_frame_{pidx}',2))]
    for j in range(5):refresh += [var(f'cc_ui_tab_frame_{j}',1),choose('cc_view_tab',j,var(f'cc_ui_tab_frame_{j}',2))]
    for j in range(4):refresh += [var(f'cc_ui_offer_frame_{j}',1),choose('cc_ui_choice',j+1,var(f'cc_ui_offer_frame_{j}',2))]
    for j in range(2):refresh += [var(f'cc_ui_register_frame_{j}',1),choose('cc_register',j,var(f'cc_ui_register_frame_{j}',2))]
    refresh += [var('cc_ui_stamp',1),f'if = {{ limit = {{ {cv("cc_ui_phase",">",1)} }} {var("cc_ui_stamp",2)} }}']
    effects.append(block('cc_ui_refresh','\n'.join(refresh)))
    from pagination import compile_pagination
    effects.append(compile_pagination())
    effects.append(block('cc_refresh_open_views','for_each_scope_loop = { array = global.cc_members if = { limit = { is_ai = no has_country_flag = cc_open } cc_ui_refresh = yes } } for_each_scope_loop = { array = global.cc_union_hosts if = { limit = { COLDWAR_SOV_is_union_republic = yes is_ai = no has_country_flag = cc_open } cc_ui_refresh = yes } } for_each_scope_loop = { array = global.cc_observers if = { limit = { exists = yes is_ai = no NOT = { cc_access = yes } has_country_flag = cc_open } cc_ui_refresh = yes } }'))
    effects.append(block('cc_ui_choices','clear_array = cc_ui_choices save_event_target_as = cc_ui_actor if = { limit = { check_variable = { cc_ui_popup = 1 } } for_each_scope_loop = { array = global.cc_hosts if = { limit = { cc_access = yes } event_target:cc_ui_actor = { add_to_array = { cc_ui_choices = PREV } } } } } else = { for_each_scope_loop = { array = global.cc_union_hosts if = { limit = { OR = { tag = SOV COLDWAR_SOV_is_union_republic = yes } } event_target:cc_ui_actor = { add_to_array = { cc_ui_choices = PREV } } } } }'))
    write('common/scripted_effects/ICW_COMECON_view.txt','\n'.join(effects))
    return local
