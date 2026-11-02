# IMPERIA COLD WAR — Regional repression, civilian losses and player aftermath events.
from .shared import *
from .deals import locals_for
from . import fiscal


def population_change(tag,states,loss,record=False):
    """One deterministic, owned and fully controlled state, never every state."""
    rows=[]
    for index,state in enumerate(states):
        valid=f'{state} = {{ is_owned_and_controlled_by = {tag} is_fully_controlled_by = {tag} state_population > {loss} }}'
        receipt=b(tag,v('incident_state',state))+'\n' if record else ''
        rows.append(b('if' if index==0 else 'else_if',[b('limit',valid),b(str(state),receipt+'add_manpower = -'+str(loss))]))
    return '\n'.join(rows)


def build(loc,fx,tr,ideas,decisions):
    mods={'Stability':-.05,'Foreign Influence Defense':-.10,'Police Cost':.05,'Bureaucracy Cost':.03}
    loc[P+'repression_legacy']='Legacy of Regional Repression'
    loc[P+'repression_legacy_desc']='Civilian deaths and coercive emergency rule have damaged public trust and international credibility. Trauma obstructs reconciliation and helps armed networks rebuild.\nRemaining regional trauma: §Y[?'+P+'trauma_weeks|0] weeks§!.'
    ideas.append(idea('repression_legacy','','',mods,'COLDWAR_USA_KS_institutions'))
    loc[P+'civilian_losses_tt']='Recorded civilian deaths: $RIGHT|0$'
    loc[P+'trauma_pressure_tt']='Weekly unrest from repression: $RIGHT|+2$'
    loc[P+'trauma_duration_tt']='Legacy of repression: $RIGHT|0$ weeks'
    loc[P+'qualifying_weeks_tt']='Sustained regional policy: $RIGHT|+=0$ weeks'
    loc[P+'repression_requirements_tt']='At least four divisions are deployed in the region, unrest exceeds 39, no previous emergency is on cooldown, and an eligible state has sufficient population under full government control.'
    loc[P+'trauma_clear_tt']='No unresolved legacy of regional repression.'
    loc[P+'international_censure']='International Censure'
    loc[P+'international_censure_desc']='Public condemnation of civilian killings has damaged this government\'s international standing.'
    ideas.append(idea('international_censure','','',{'Foreign Influence':-.10}))
    fx[P+'repression_tick']=guard(check('repression_cooldown','>',0),add('repression_cooldown',-1))+'\n'+guard(check('trauma_weeks','>',0),add('trauma_weeks',-1)+'\n'+guard(check('trauma_weeks','=',0),'remove_ideas = '+P+'repression_legacy\n'+v('trauma_drift',0)))
    for index,(h,d) in enumerate(HOSTS.items()):
        tag=d['tag'];deal='irq_settlement' if h=='irq' else d['rights']
        for policy,title,loss,reduction,stabilisation,weeks,drift in (
          ('emergency','Impose Emergency Military Rule',1000,-25,10,104,.75),
          ('repression','Authorise Indiscriminate Repression',10000,-50,20,156,1.5)):
            key=P+h+'_'+policy
            loc[key]=title
            loc[key+'_desc']=('Place the contested region under coercive military administration.' if policy=='emergency' else 'Authorise indiscriminate repression of the regional population. Mass civilian killings will be reported to the government, Washington and existing regional authorities.')+' This action causes '+format(loss,',')+' civilian deaths, removed from the population of one controlled regional state. Immediate containment comes at the cost of political rights, public trust and long-term reconciliation. Trauma prevents consolidation for '+str(weeks)+' weeks and gives foreign sponsors an opportunity to rebuild resistance.'
            eligible='OR = { '+' '.join(f'{s} = {{ is_owned_and_controlled_by = {tag} is_fully_controlled_by = {tag} state_population > {loss} }}' for s in d['states'])+' }'
            readiness='num_divisions_in_states = { count > 3 states = { '+' '.join(map(str,d['states']))+' } }\n'+check('unrest','>',39)+'\n'+check('repression_cooldown','=',0)+'\n'+eligible
            valid='tag = '+tag+'\n'+flag('tracked')+'\n'+requirement('repression_requirements_tt',readiness)+'\n'+at_least('treasury',P+policy+'_quote')+'\ncheck_variable = { '+P+policy+'_quote > 0 }'
            percent=2 if policy=='emergency' else 4
            pay=fiscal.cost_rows(percent)
            politics='add_stability = '+num(-.04 if policy=='emergency' else -.12)
            losses=population_change(tag,d['states'],loss,True)
            rights=f'clr_country_flag = {P}domestic_rights_signed\nremove_ideas = {P}domestic_rights\n{P}deal_{deal}_end = yes\nUSA = {{ {P}reconcile_deals = yes {P}reconcile_aid = yes }}'
            if h=='irq':rights+='\nclr_country_flag = COLDWAR_IRQ_autonomy_fulfilled'
            penalties=add('qualifying_weeks',-52 if policy=='emergency' else -104)+f'\nclamp_variable = {{ var = {P}qualifying_weeks min = 0 max = 520 }}\nclr_country_flag = {P}pacified\nremove_ideas = {P}consolidated_compact\n'+P+'reconciliation_total = yes'
            consequences=v('last_civilian_losses',loss)+'\n'+add('civilian_losses',loss)+'\n'+v('trauma_weeks',weeks)+'\n'+v('trauma_drift',drift)+'\n'+v('repression_cooldown',104)+'\nadd_ideas = '+P+'repression_legacy'
            aftermath='country_event = { id = COLDWAR_USA_KS.'+str(210+index)+' }\nUSA = { if = { limit = { exists = yes } country_event = { id = COLDWAR_USA_KS.'+str(220+index)+' } } }'
            for r in locals_for(h):aftermath+='\n'+b(r,guard('exists = yes','country_event = { id = COLDWAR_USA_KS.'+str(230+index)+' }'))
            # A single action-time dispatch, never a recurring world scan.
            # Every other existing country receives the international report.
            excluded=' '.join('NOT = { tag = '+t+' }' for t in [tag,'USA',*locals_for(h)])
            aftermath+='\n'+b('every_country',[b('limit','exists = yes\n'+excluded),'country_event = { id = COLDWAR_USA_KS.'+str(240+index)+' }'])
            execute='\n'.join([losses,politics,add('unrest',reduction),add('stabilisation',stabilisation),add('organisation',-10 if policy=='emergency' else -20),
              f'clamp_variable = {{ var = {P}unrest min = 0 max = 100 }}',f'clamp_variable = {{ var = {P}stabilisation min = 0 max = 100 }}',f'clamp_variable = {{ var = {P}organisation min = 0 max = 100 }}',rights,penalties,consequences,aftermath,P+'refresh_host = yes','update_money_dirty_variable = yes'])
            fx[key]=guard(valid,fiscal.purchase(percent,execute))
            shown=effect_preview('\n'.join([pay,population_change(tag,d['states'],loss),politics,scalar_row('unrest',reduction),scalar_row('stabilisation',stabilisation),scalar_row('organisation',-10 if policy=='emergency' else -20),scalar_row('qualifying_weeks',-52 if policy=='emergency' else -104),scalar_row('trauma_pressure',drift),f'set_variable = {{ {P}preview_trauma = {weeks} tooltip = {P}trauma_duration_tt }}','remove_ideas = '+P+'domestic_rights','remove_ideas = '+P+'consolidated_compact','remove_ideas = '+P+'deal_'+deal+'_partner','USA = { remove_ideas = '+P+'deal_'+deal+'_usa }','add_ideas = '+P+'repression_legacy',modifier_rows(mods)]))
            # Deliberate human RP choice. Ordinary host AI retains the security,
            # development and political-settlement alternatives.
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('tracked')),b('available',valid),'cost = '+str(100 if policy=='emergency' else 150),b('complete_effect',visible_and_hidden(shown,key+' = yes')),'ai_will_do = { factor = 0 }']))


def events(loc,event):
    rows=[]
    for index,(h,d) in enumerate(HOSTS.items()):
        tag=d['tag'];losses='[?'+tag+'.'+P+'last_civilian_losses|0]'
        region='['+P+'GetIncidentRegion_'+h+']'
        description='Government troops and security forces of ['+tag+'.GetNameDef] have killed '+losses+' Kurdish civilians in '+region+' during the government crackdown. Reports from the affected communities describe civilian killings and families fleeing their homes. Kurdish representatives are demanding accountability and international attention.'
        title='Kurdish Civilians Killed in '+d['name']
        picture='GFX_'+P+'aftermath_'+h
        rows.append(event(210+index,title,description,[('The government must face the consequences.',None,'')],loc,immediate=setflag('host_report_'+h),picture=picture))
        cost='add_political_power = -25\n'+b(tag,'add_timed_idea = { idea = '+P+'international_censure days = 365 }\nadd_opinion_modifier = { target = USA modifier = '+P+'censure_opinion }')+'\nadd_opinion_modifier = { target = '+tag+' modifier = '+P+'censure_opinion }'
        rows.append(event(220+index,title,description,[('Publicly condemn the crackdown.','tag = USA\nhas_political_power > 24',cost),('Review our Kurdish policy.',None,'')],loc,immediate=setflag('usa_report_'+h),picture=picture))
        rows.append(event(230+index,title,description,[('Document the victims and appeal abroad.',None,'add_political_power = 25')],loc,immediate=setflag('local_report_'+h),picture=picture))
        rows.append(event(240+index,title,description,[('The international community is watching.',None,'')],loc,immediate=setflag('international_report_'+h),picture=picture))
        areas={'irq':'Erbil, Dohuk, Sulaymaniyah and Halabja','per':'Kordestan','tur':'Diyarbakir','syr':'Al-Hasakah'}
        warning='Kurdish networks in '+areas[h]+', '+d['name']+', are preparing an armed rising against ['+tag+'.GetNameDef]. American covert support is strengthening their organisation and supply networks. Government deployments, funded regional programmes and political concessions can still prevent the mobilisation from becoming an uprising.'
        rows.append(event(110+index,'Kurdish Mobilisation in '+d['name'],warning,[('Review our Kurdish policy.',None,'')],loc,picture=picture))
    return rows


def incident_texts(loc):
    rows=[]
    for h,d in HOSTS.items():
        name=P+'GetIncidentRegion_'+h;texts=[]
        for state in d['states']:
            key=P+'incident_region_'+str(state);loc[key]='['+str(state)+'.GetName]'
            texts.append(b('text',[b('trigger',b(d['tag'],check('incident_state','=',state))),'localization_key = '+key]))
        key=P+'incident_region_'+h;loc[key]='the Kurdish-inhabited districts of '+d['name']
        rows.append(b('defined_text',['name = '+name,*texts,b('text','localization_key = '+key)]))
    return '\n'.join(rows)
