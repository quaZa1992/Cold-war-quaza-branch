# IMPERIA COLD WAR — Approved national focuses and concrete programme effects.
import re
from .shared import *
from .deals import DEALS,preview,locals_for,local_relevant
from .aid import preview as aid_preview
from . import fiscal

STAGES={'irq_fund':('irq',2),'irq_front':('irq',3),'irn_fund':('per',2),'irn_front':('per',3),
 'tur_networks':('tur',2),'tur_front':('tur',3),'syr_voice':('syr',2),'syr_front':('syr',3)}
CONTACTS={'irq_contacts':'irq','irn_contacts':'per','tur_networks':'tur','syr_contacts':'syr'}
CLAIMS={d['claim']:h for h,d in HOSTS.items()}
UNLOCKS={'triangular':'deal_beijing_renew','covert':'irq_resume','guarantees':'deal_tur_alliance_renew',
 'clients':'deal_angola_renew','political':'chile_funding','shuttle':'per_mediation',
 'kurds':'per_breach','irq_autonomy':'irq_offer_framework','syr_organisation':'syr_resupply'}

def amount(s):return Decimal(re.search(r'[+-]?\d+(?:\.\d+)?',s.replace(',','').replace('$',''))[0])

def build(loc,fx,tr,ideas,decisions):
    fragments=[];specs={}
    policies={'doctrine':{'Foreign Influence':.05,'Decryption':.05,'Bureaucracy Cost':.01},
      'limited':{'Decryption':.10,'Foreign Influence Defense':.05},
      'expanded':{'Foreign Influence':.10,'Agency Upgrade Time':-.10,'Bureaucracy Cost':.03}}
    for key,mods in policies.items():
        title={'doctrine':'Strategic Flexibility','limited':'Limited Commitments','expanded':'Expanded Mandates'}[key]
        loc[P+'policy_'+key]=title;loc[P+'policy_'+key+'_desc']=FOCUSES[key]['description']
        ideas.append(idea('policy_'+key,title,'',mods))
    loc[P+'credibility_crisis']='Alliance Credibility Crisis';loc[P+'credibility_crisis_desc']='A breach with a regional partner has weakened confidence in American commitments.'
    ideas.append(idea('credibility_crisis','','',{'Foreign Influence':-.10}))
    loc[P+'recognition_cost']='Contested Regional Recognition';loc[P+'recognition_cost_desc']='Recognition of a disputed regional authority complicates American relations with neighbouring governments.'
    ideas.append(idea('recognition_cost','','',{'Foreign Influence':-.10}))
    for key,n in FOCUSES.items():
        loc[n['id']]=CAPTIONS.get(key,n['title']);loc[n['id']+'_desc']=n['description']
        if key in fiscal.US_SETUP:loc[n['id']+'_desc']+=' Initial programme funding: '+num(fiscal.US_SETUP[key])+'% of current US GDP.'
        runtime=[];shown=[];requirements=[]
        if key in DEALS and key!='moscow':
            requirements += [P+'deal_'+key+'_can_offer = yes']
            if key=='angola':requirements.append('UNI = { exists = yes OR = { has_war = yes NOT = { is_subject = yes } } }')
        h=CONTACTS.get(key)
        if h:
            requirements.append(P+'region_'+h+' = yes')
            runtime += [P+'init_'+h+' = yes',setflag('contact_'+h)]
        if key in ('irn_dossier','irn_contacts','irn_fund','irn_front'):
            requirements.append(P+'confrontation_per = yes')
        if key=='irq_fund':requirements.append(P+'confrontation_irq = yes')
        if key=='tur_rights':
            requirements.append(requirement('tur_contacts_tt','OR = { '+P+'deal_tur_alliance_active = yes '+flag('contact_tur')+' }'))
        if key=='syr_front':requirements += [P+'confrontation_syr = yes',requirement('syr_crisis_tt','SYR = { OR = { has_war = yes '+check('unrest','>',64)+' } }')]
        if key in STAGES:
            host,stage=STAGES[key]
            requirements += [P+'route_'+host+' = yes',requirement('slot_available_tt','OR = { '+check('stage_'+host,'>',0)+' '+P+'slot_available = yes }')]
            if host=='irq':
                for t in locals_for('irq'):
                    requirements.append(requirement('liaison_'+t.lower()+'_tt','OR = { NOT = { '+local_relevant(t,'irq')+' } '+t+' = { '+flag('partner_irq')+' } }'))
            runtime += [P+'init_'+host+' = yes',v('stage_'+host,stage),v('max_stage_'+host,stage),P+'count_campaigns = yes']
            if host=='irq':runtime.append(v('legacy_irq_rate',0))
        for e in n['effects']:
            if e['country']!='USA':continue
            if e['label']=='Political Power':
                code='add_political_power = '+num(amount(e['value']));runtime.append(code);shown.append(code)
            elif e['label']=='Treasury':
                percent=fiscal.US_SETUP[key]
                requirements.append('hidden_trigger = { check_variable = { gdp_total > 0 } }')
                runtime.append(fiscal.charge(percent));shown.append(fiscal.cost_rows(percent))
            elif e['label']=='Infantry Equipment':
                requirements.append('custom_trigger_tooltip = { tooltip = '+P+'equipment_tt has_equipment = { infantry_weapons_1 > 999 } }')
                code='add_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }'
                runtime.append(code);shown.append(code)
                host=STAGES[key][0];runtime.append(add('cache_'+host,1000))
                shown.append(scalar_row('material',1000))
                shown.append('unlock_decision_tooltip = '+P+host+'_cache_'+HOSTS[host]['rebel'].lower())
            elif e['value'].endswith('Billion/week') and key not in DEALS:
                rate='us_chile' if key=='chile' else 'us_armed' if STAGES[key][1]==3 else 'us_funded'
                shown.append(fiscal.weekly_rows(rate))
        if key in policies:
            runtime.append('add_ideas = '+P+'policy_'+key);shown += ['add_ideas = '+P+'policy_'+key,modifier_rows(policies[key])]
            if key in ('limited','expanded'):shown.append(scalar_row('slots',2 if key=='limited' else 4))
        if key=='moscow':
            requirements.append('SOV = { exists = yes NOT = { has_war_with = USA } }')
            shown.append('icwt_focus_preview_7 = yes');runtime.append('icwt_initiative_7 = yes')
            loc[n['id']+'_desc']='Establish a regular negotiating channel with Moscow. Delegations may prepare a Nuclear Risk Reduction agreement and review its complete terms before signature. Strategic competition and the Chinese channel continue alongside these talks.'
        elif key in DEALS:
            shown.append(preview(key));runtime.append(P+'deal_'+key+'_offer = yes')
        if key in UNLOCKS:shown.append('unlock_decision_tooltip = '+P+UNLOCKS[key])
        if key in CONTACTS:
            shown.append('unlock_decision_tooltip = '+P+CONTACTS[key]+'_resume')
            shown.append('unlock_decision_tooltip = '+P+CONTACTS[key]+'_finance_networks')
        if key in STAGES:
            host,stage=STAGES[key]
            shown.append('unlock_decision_tooltip = '+P+host+'_pause')
            shown.append('unlock_decision_tooltip = '+P+host+'_finance_networks')
            shown.append(b(HOSTS[host]['tag'],scalar_row('weekly_unrest',5.32 if stage==3 else 2.85)))
        if key in STAGES and any(e['country']=='USA' and e['label']=='Infantry Equipment' for e in n['effects']):
            host,stage=STAGES[key]
            for r in locals_for(host):shown.append(aid_preview(host,r,stage))
        if key=='irq_fund':
            runtime.append('IRQ = { '+add('organisation',10)+' }');shown.append(b('IRQ',scalar_row('organisation',10)))
        if key=='syr_organisation':
            runtime.append('SYR = { '+add('organisation',10)+' }');shown.append(b('SYR',scalar_row('organisation',10)))
        if key=='tur_breach':
            runtime += [setflag('breach_tur'),'add_timed_idea = { idea = '+P+'credibility_crisis days = 180 }',
              'add_opinion_modifier = { target = TUR modifier = '+P+'breach_opinion }','TUR = { add_opinion_modifier = { target = USA modifier = '+P+'breach_opinion } }',P+'reconcile_deals = yes']
            shown += ['add_timed_idea = { idea = '+P+'credibility_crisis days = 180 }',modifier_rows({'Foreign Influence':-.10}),
                'add_opinion_modifier = { target = TUR modifier = '+P+'breach_opinion }','unlock_decision_tooltip = '+P+'tur_resume']
        if key=='irq_settlement':requirements.append(requirement('framework_tt','OR = { IRQ = { '+flag('framework_irq_accepted')+' } COLDWAR_USA_gulf_settlement_respected = yes }'))
        if key in CLAIMS:
            host=CLAIMS[key];d=HOSTS[host];r=d['rebel']
            requirements += [requirement('recognition_tt',f'{r} = {{ exists = yes NOT = {{ is_subject = yes }} {flag("recognition_requested")} any_owned_state = {{ OR = {{ '+ ' '.join('state = '+str(s) for s in d['states'])+' } is_controlled_by = PREV } }')]
            runtime += ['add_timed_idea = { idea = '+P+'recognition_cost days = 180 }',setflag('recognised_'+host),
                f'if = {{ limit = {{ NOT = {{ is_in_array = {{ array = recognised_countries value = {r} }} }} }} add_to_array = {{ array = recognised_countries value = {r} }} }}',
                f'{r} = {{ set_country_flag = {P}recognised_by_usa add_opinion_modifier = {{ target = USA modifier = {P}recognition_opinion }} }}',
                f'add_opinion_modifier = {{ target = {r} modifier = {P}recognition_opinion }}']
            shown += ['add_timed_idea = { idea = '+P+'recognition_cost days = 180 }',modifier_rows({'Foreign Influence':-.10}),
                f'add_opinion_modifier = {{ target = {r} modifier = {P}recognition_opinion }}']
        if key=='chile':
            requirements.append('CHL = { exists = yes OR = { has_opinion = { target = USA value < 0 } has_war_with = USA } }')
            runtime.append(setflag('chile_funding'));shown.append('unlock_decision_tooltip = '+P+'chile_end')
        tr[P+'ready_'+key]=P+'usa_actor = yes\n'+'\n'.join(dict.fromkeys(requirements))
        # Successful execution is receipted once. A rare last-tick resource
        # change leaves a visible enactment decision instead of losing content.
        transaction=setflag('done_'+key)+'\nclr_country_flag = '+P+'pending_'+key+'\n'+'\n'.join(runtime)+'\n'+P+'reconcile_aid = yes\nupdate_money_dirty_variable = yes'
        fx[P+'execute_'+key]=guard(P+'ready_'+key+' = yes\n'+noflag('done_'+key),transaction)
        fx[P+'complete_'+key]=P+'count_campaigns = yes\n'+P+'execute_'+key+' = yes\n'+guard(noflag('done_'+key),setflag('pending_'+key))
        fx[P+'preview_'+key]=effect_preview('\n'.join(shown))
        x,y=COORDS.get(key,n['world']);focus=[f'id = {n["id"]}',f'icon = GFX_goal_{P}{n["icon"]}',f'x = {x}',f'y = {y}',f'cost = {n["days"]/7:g}']
        for group in n['prerequisite_groups']:focus.append(b('prerequisite','\n'.join('focus = '+P+k for k in group)))
        if n['exclusive']:focus.append(b('mutually_exclusive','\n'.join('focus = '+P+k for k in n['exclusive'])))
        focus += [b('available',['hidden_trigger = { '+P+'usa_actor = yes }','\n'.join(dict.fromkeys(requirements))]),
            'cancel_if_invalid = yes','continue_if_invalid = no',
            b('completion_reward',[P+'preview_'+key+' = yes',b('hidden_effect',P+'complete_'+key+' = yes')]),
            'search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_FOREIGN_POLICY }',
            'ai_will_do = { factor = '+('0' if key=='tur_breach' else '0.1' if n['history'].startswith(('Alternate','Alternative')) else '1')+' }']
        fragments.append(b('focus',focus));specs[key]=dict(id=n['id'],x=x,y=y,requirements=requirements,preview='\n'.join(shown))
        did=P+'enact_'+key;loc[did]='Enact: '+CAPTIONS.get(key,n['title']);loc[did+'_desc']='Carry the authorised programme into effect once its political, territorial and material requirements are met.'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('pending_'+key)+'\n'+noflag('done_'+key)),b('available',P+'ready_'+key+' = yes'),'cost = 0',b('complete_effect',visible_and_hidden(P+'preview_'+key+' = yes',P+'complete_'+key+' = yes')),'ai_will_do = { factor = 1 }']))
    return '\n\n'.join(fragments),specs
