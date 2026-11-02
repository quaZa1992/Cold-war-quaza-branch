# IMPERIA COLD WAR — Kurdish movements before regional statehood.
from .shared import *
from . import fiscal


def build(loc,fx,tr,ideas,decisions):
    reconcile=[]
    loc[P+'underground_ready_tt']='The Kurdish networks have room to expand, the 13-week funding interval has elapsed, and no consolidated regional settlement is in force.'
    for h,d in HOSTS.items():
        tag=d['tag'];rebels=['KUR','PUK'] if h=='irq' else [d['rebel']]
        # An underground programme is real expenditure even when there is no
        # regional country to receive a bilateral treasury transfer.
        payees=' '.join('AND = { country_exists = '+r+' is_in_array = { array = '+P+'payees_'+h+' value = '+r+' } }' for r in rebels)
        tiers=[(2,'us_funded',2.85),(3,'us_armed',5.32)]
        if h=='irq':tiers.append(('legacy','us_legacy',5.32))
        for stage,rate,pressure in tiers:
            ident='underground_'+h+'_'+str(stage)
            loc[P+ident]='Kurdish Underground Support: '+d['name']
            loc[P+ident+'_desc']='American covert funding sustains Kurdish political organisers and clandestine supply networks inside '+d['name']+'. The programme supports resistance before an independent Kurdish authority exists. Government deployments, development and political concessions can contain its influence.'
            loc[P+ident+'_weekly_tt']=fiscal.weekly_text(rate)+' Weekly foreign unrest pressure in '+d['name']+': §Y+'+num(pressure)+'§!.'
            ideas.append(idea(ident,'','',{},weekly=True))
            valid=P+'funding_'+h+' = yes\n'+check('stage_'+h,'=',3 if stage=='legacy' else stage)+'\nNOT = { '+P+'settlement_protects_'+h+' = yes }\nNOT = { OR = { '+payees+' } }'
            if h=='irq':valid+='\n'+check('legacy_irq_rate','>' if stage=='legacy' else '=',0)
            ensure=guard('NOT = { has_idea = '+P+ident+' }','add_ideas = '+P+ident)
            reconcile.append(guard(valid,ensure)+'\n'+b('else','remove_ideas = '+P+ident))
        key=P+h+'_finance_networks'
        loc[key]='Finance Kurdish Underground Networks: '+d['name']
        loc[key+'_desc']='Fund Kurdish organisers, clandestine communications and local political networks inside '+d['name']+'. This strengthens the movement while the contested territory remains under the central government. An independent Kurdish state is not required. Arms, sustained organisation and an unresolved mobilisation warning are still needed before an uprising can be supported.'
        loc[key+'_desc']+=' Initial funding: '+num(fiscal.US_SETUP['networks'])+'% of US GDP. A new operation can be authorised after 13 weeks.'
        requirements=P+'usa_actor = yes\n'+flag('contact_'+h)+'\n'+P+'region_'+h+' = yes\n'+P+'confrontation_'+h+' = yes\n'+P+'funding_'+h+' = yes\n'+check('stage_'+h,'>',1)+'\nNOT = { '+P+'settlement_protects_'+h+' = yes }\n'+requirement('underground_ready_tt',tag+' = { '+flag('tracked')+' '+noflag('pacified')+' '+check('network_cooldown','=',0)+' '+check('organisation','<',100)+' }')+'\n'+fiscal.affordable('us_networks_quote')
        local=add('organisation',15)+'\n'+add('unrest',5)+'\n'+v('network_cooldown',13)+f'\nclamp_variable = {{ var = {P}organisation min = 0 max = 100 }}\nclamp_variable = {{ var = {P}unrest min = 0 max = 100 }}\n'+P+'refresh_host = yes'
        execute=fiscal.purchase(fiscal.US_SETUP['networks'],b(tag,local)+'\n'+P+'reconcile_aid = yes\nupdate_money_dirty_variable = yes')
        fx[key]=guard(requirements,execute)
        shown=effect_preview(fiscal.cost_rows(fiscal.US_SETUP['networks'])+'\n'+b(tag,scalar_row('organisation',15)+'\n'+scalar_row('unrest',5)))
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('contact_'+h)),b('available',requirements),'cost = 50','days_re_enable = 91',b('complete_effect',visible_and_hidden(shown,key+' = yes')),'ai_will_do = { factor = 0.3 }']))
        fx[P+'tick_'+h]=fx[P+'tick_'+h]+'\n'+guard('tag = '+tag+'\n'+flag('tracked')+'\n'+check('network_cooldown','>',0),add('network_cooldown',-1))
    fx[P+'reconcile_underground']=guard(P+'usa_actor = yes','\n'.join(reconcile))
    fx[P+'reconcile_aid']+='\n'+P+'reconcile_underground = yes'
