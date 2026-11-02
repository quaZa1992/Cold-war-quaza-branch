# IMPERIA COLD WAR — Recipient-owned statecraft and regional agreements.
from .shared import *
from . import fiscal

DEALS={
 'beijing':dict(tag='CHI',name='Beijing Backchannel',partner='Washington Backchannel',us={'Foreign Influence':.05,'Decryption':.05},them={'Encryption':.05,'Agency Upgrade Time':-.05}),
 'moscow':dict(tag='SOV',name='Détente Consultations',partner='Détente Consultations',us={'Foreign Influence Defense':.05},them={'Foreign Influence Defense':.05},balance_mode='own_cost'),
 'irq_transit':dict(tag='PER',name='Tehran Transit Channel',partner='American Liaison Mission',us={'Decryption':.05},them={'Encryption':.05,'Bureaucracy Cost':.01},balance_mode='transfer'),
 'irq_anatolia':dict(tag='TUR',name='Anatolian Transit Channel',partner='American Border Liaison',us={'Decryption':.05},them={'Encryption':.05,'Police Cost':.01},balance_mode='transfer'),
 'tur_alliance':dict(tag='TUR',name='Ankara Intelligence Partnership',partner='Ankara Intelligence Partnership',us={'Decryption':.05},them={'Foreign Influence Defense':.10,'Police Cost':-.03},nato=True),
 'irq_settlement':dict(tag='IRQ',name='Northern Settlement Guarantees',partner='Northern Regional Accord',us={'Foreign Influence Defense':.05},them={'Stability':.03,'Police Cost':-.05,'Bureaucracy Cost':.02},rights='irq'),
 'irn_rights':dict(tag='PER',name='Zagros Settlement Guarantees',partner='Kurdish Regional Rights',us={'Foreign Influence Defense':.05},them={'Stability':.03,'Police Cost':-.05,'Bureaucracy Cost':.02},rights='per'),
 'tur_rights':dict(tag='TUR',name='Anatolian Rights Consultations',partner='Southeastern Regional Rights',us={'Foreign Influence Defense':.05},them={'Stability':.03,'Police Cost':-.05,'Bureaucracy Cost':.02},rights='tur'),
 'syr_rights':dict(tag='SYR',name='Jazira Settlement Consultations',partner='Citizenship and Regional Rights',us={'Foreign Influence Defense':.05},them={'Stability':.03,'Police Cost':-.05,'Bureaucracy Cost':.02},rights='syr'),
 'angola':dict(tag='UNI',name='Angolan Partner Liaison',partner='American Military Liaison',us={},them={'Division Organisation':.03,'Army Experience Gain':.05,'Bureaucracy Cost':.01}),
}

def clear(tag):
    bans=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = {tag} }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    reverse=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = USA }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    return f'country_exists = {tag}\nNOT = {{ has_war_with = {tag} }}\nNOT = {{ is_embargoing = {tag} }}\nNOT = {{ OR = {{ {bans} }} }}\n{tag} = {{ NOT = {{ has_war_with = USA }} NOT = {{ is_embargoing = USA }} NOT = {{ OR = {{ {reverse} }} }} }}'

def locals_for(host):return ['KUR','PUK'] if host=='irq' else [HOSTS[host]['rebel']]
def local_relevant(tag,host):return f'{tag} = {{ exists = yes any_owned_state = {{ OR = {{ '+ ' '.join(f'state = {s}' for s in HOSTS[host]['states'])+' } is_controlled_by = PREV } }'

def preview(key):
    d=DEALS[key];tag=d['tag'];i=P+'deal_'+key
    us=f'add_ideas = {i}_usa\n'+modifier_rows(d['us'])+'\n'+fiscal.weekly_rows('deal_'+key+'_usa')
    partner=f'add_ideas = {i}_partner\n'+modifier_rows(d['them'])
    if d.get('balance_mode')=='transfer':partner+='\n'+fiscal.weekly_rows('deal_'+key+'_usa',1,'USA.gdp_total',True)
    if d.get('balance_mode')=='own_cost':partner+='\n'+fiscal.weekly_rows('deal_'+key+'_partner')
    return effect_preview(f'custom_effect_tooltip = {P}if_accept_tt\nUSA = {{ {us} }}\n{tag} = {{ {partner} }}')

def build(loc,effects,triggers,ideas,decisions):
    reconcile=[];weekly=[]
    for index,(key,d) in enumerate(DEALS.items()):
        # IMPERIA COLD WAR — Moscow now negotiates through the standing treaty paper.
        if key=='moscow':continue
        tag=d['tag'];i=P+'deal_'+key
        loc[i+'_usa']=d['name'];loc[i+'_partner']=d['partner']
        for suffix in ('usa','partner'):loc[i+'_'+suffix+'_desc']='Regular political and institutional cooperation supports the agreed regional settlement and consultation arrangements.'
        ideas.append(idea('deal_'+key+'_usa',d['name'],'',d['us'],weekly=True))
        loc[i+'_usa_weekly_tt']=fiscal.weekly_text('deal_'+key+'_usa',donor=True)
        mode=d.get('balance_mode')
        ideas.append(idea('deal_'+key+'_partner',d['partner'],'',d['them'],weekly=True if mode else None))
        if mode=='transfer':loc[i+'_partner_weekly_tt']=fiscal.weekly_text('deal_'+key+'_usa',1,True)
        if mode=='own_cost':loc[i+'_partner_weekly_tt']=fiscal.weekly_text('deal_'+key+'_partner')
        extra=''
        if d.get('nato'):extra+='\nhas_idea = NATO_member\nTUR = { has_idea = NATO_member }'
        if key in ('irq_transit','irq_anatolia','tur_alliance'):
            breach='per' if tag=='PER' else 'tur'
            extra+='\n'+noflag('breach_'+breach)
        active_local=''
        if d.get('rights'):
            h=d['rights'];active_local='\n'.join('OR = { NOT = { '+local_relevant(t,h)+' } '+t+' = { '+flag('rights_'+h+'_consent')+' } }' for t in locals_for(h))
        triggers[i+'_relations']=clear(tag)+extra
        triggers[i+'_active']='tag = USA\nIMP_is_1970_scenario = yes\n'+flag('deal_'+key+'_signed')+'\n'+i+'_relations = yes\n'+active_local
        triggers[i+'_can_offer']=b('hidden_trigger','tag = USA\nIMP_is_1970_scenario = yes\n'+noflag('deal_'+key+'_signed')+'\n'+noflag('deal_'+key+'_pending')+'\n'+noflag('deal_'+key+'_cooldown'))+'\n'+i+'_relations = yes'
        pending=flag('deal_'+key+'_pending')
        valid=f'tag = {tag}\ncountry_exists = USA\n{pending}\nUSA = {{ {flag("deal_"+key+"_authorised")} {pending} {i}_relations = yes }}'
        triggers[i+'_accept_valid']=valid
        effects[i+'_preview']=preview(key)
        effects[i+'_offer']=guard(i+'_can_offer = yes','\n'.join([setflag('deal_'+key+'_authorised'),setflag('deal_'+key+'_pending'),b(tag,setflag('deal_'+key+'_pending')+'\ncountry_event = { id = COLDWAR_USA_KS.'+str(index+1)+' }')]))
        accept=[setflag('deal_'+key+'_signed'),f'clr_country_flag = {P}deal_{key}_pending',
            b('USA',[setflag('deal_'+key+'_signed'),f'clr_country_flag = {P}deal_{key}_pending'])]
        if d.get('rights'):
            h=d['rights']
            accept += [setflag('rights_'+h+'_accepted')]
            for t in locals_for(h):accept.append(guard(local_relevant(t,h),b(t,f'clr_country_flag = {P}rights_{h}_consent\n'+setflag('rights_'+h+'_pending'))))
        accept.append('USA = { '+P+'reconcile_deals = yes }')
        effects[i+'_accept']=guard(i+'_accept_valid = yes','\n'.join(accept))
        end='\n'.join([f'clr_country_flag = {P}deal_{key}_pending',f'clr_country_flag = {P}deal_{key}_signed',
            b('USA',[f'clr_country_flag = {P}deal_{key}_pending',f'clr_country_flag = {P}deal_{key}_signed',f'set_country_flag = {{ flag = {P}deal_{key}_cooldown value = 1 days = 60 }}',f'remove_ideas = {i}_usa']),
            b(tag,[f'clr_country_flag = {P}deal_{key}_pending',f'clr_country_flag = {P}deal_{key}_signed',f'remove_ideas = {i}_partner'])])
        if d.get('rights'):
            h=d['rights'];end+='\n'+b(tag,f'clr_country_flag = {P}rights_{h}_accepted')
            end+='\n'+'\n'.join(b(t,f'clr_country_flag = {P}rights_{h}_pending\nclr_country_flag = {P}rights_{h}_consent') for t in locals_for(h))
        effects[i+'_end']=guard(f'OR = {{ tag = USA tag = {tag} }}',end)
        ensure=f'if = {{ limit = {{ NOT = {{ has_idea = {i}_usa }} }} add_ideas = {i}_usa }}\n{tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = {i}_partner }} }} add_ideas = {i}_partner }} }}'
        remove=f'remove_ideas = {i}_usa\n{tag} = {{ remove_ideas = {i}_partner }}'
        reconcile.append(guard(i+'_active = yes',ensure)+'\n'+b('else',remove))
        weekly.append(guard('tag = USA\nUSA = { '+i+'_active = yes }',fiscal.stream('expense','deal_'+key+'_usa')))
        if mode=='transfer':weekly.append(guard(f'tag = {tag}\nUSA = {{ {i}_active = yes }}',fiscal.stream('income','deal_'+key+'_usa',True)))
        if mode=='own_cost':weekly.append(guard(f'tag = {tag}\nUSA = {{ {i}_active = yes }}',fiscal.stream('expense','deal_'+key+'_partner')))
        def decision(name,title,visible,available,body,desc):
            did=i+'_'+name;loc[did]=title;loc[did+'_desc']=desc
            # Standing arrangements are not disposable daily AI actions.
            # Actual war/embargo/sanction guards suspend them independently.
            weight=0 if name in ('cancel','terminate') else 1
            decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',visible),b('available',available),'cost = 0',b('complete_effect',body),f'ai_will_do = {{ factor = {weight} }}']))
        decision('accept','Accept: '+d['name'],f'tag = {tag}\n{pending}',i+'_accept_valid = yes',visible_and_hidden(preview(key),i+'_accept = yes'),'Washington proposes regular consultation and the associated regional arrangements. Acceptance establishes the terms shown below.')
        decision('decline','Decline: '+d['name'],f'tag = {tag}\n{pending}','always = yes',b('hidden_effect',i+'_end = yes'),'We are unwilling to accept the proposed commitments.')
        decision('cancel','Withdraw proposal: '+d['name'],'tag = USA\n'+pending,'always = yes',b('hidden_effect',i+'_end = yes'),'Withdraw the unsigned proposal and leave the recipient free of its proposed obligations.')
        decision('renew','Renew proposal: '+d['name'],'tag = USA\n'+flag('deal_'+key+'_authorised'),i+'_can_offer = yes',visible_and_hidden(preview(key),i+'_offer = yes'),'Reopen the proposed consultations with the named government.')
        decision('terminate','End: '+d['name'],f'OR = {{ tag = USA tag = {tag} }}\nUSA = {{ {flag("deal_"+key+"_signed")} }}','always = yes',visible_and_hidden(effect_preview(f'USA = {{ remove_ideas = {i}_usa }} {tag} = {{ remove_ideas = {i}_partner }}'),i+'_end = yes'),'Bring the standing arrangement to an end.')
    effects[P+'reconcile_deals']=guard('tag = USA\nIMP_is_1970_scenario = yes','\n'.join(reconcile))
    effects[P+'deal_streams']='\n'.join(weekly)
    # Existing local RP authorities approve their own settlement. An underground
    # political network is represented by its completed contact programme.
    for h,d in HOSTS.items():
        for t in locals_for(h):
            did=P+'rights_'+h+'_local_'+t.lower();loc[did]='Accept regional settlement';loc[did+'_desc']='The regional government has accepted the proposed political terms. Our representatives must decide whether those terms provide an acceptable settlement.'
            valid=f'tag = {t}\n{flag("rights_"+h+"_pending")}\n{d["tag"]} = {{ {flag("rights_"+h+"_accepted")} }}'
            effect=setflag('rights_'+h+'_consent')+f'\nclr_country_flag = {P}rights_{h}_pending\n{HOSTS[h]["tag"]} = {{ {P}reconcile_domestic = yes }}\nUSA = {{ {P}reconcile_deals = yes }}'
            decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',valid),b('available',valid),'cost = 0',b('complete_effect',visible_and_hidden(P+'local_rights_preview_'+h+' = yes',guard(valid,effect))),'ai_will_do = { factor = 1 }']))
            loc[did+'_decline']='Refuse regional settlement';loc[did+'_decline_desc']='The proposed arrangement does not meet our political requirements.'
            key='irq_settlement' if h=='irq' else HOSTS[h]['rights']
            decisions.append(b(did+'_decline',['icon = GFX_decision_generic_political_discourse',b('visible',valid),'cost = 0',b('complete_effect',b('hidden_effect',P+'local_rights_end_'+h+' = yes')),'ai_will_do = { factor = 0.2 }']))
