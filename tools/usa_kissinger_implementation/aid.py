# IMPERIA COLD WAR — Recipient-approved material assistance and visible paired budgets.
from .shared import *
from . import fiscal

def preview(h,r,tier,amount=1000):
    suffix=h+'_'+r.lower()+'_'+str(tier);rate='us_legacy' if tier=='legacy' else 'us_armed' if tier==3 else 'us_funded'
    more=''
    if tier=='legacy':more='\nadd_to_variable = { '+P+'preview_defense_bonus_against = .08 tooltip = COLDWAR_USA_gulf_preview_mod_defense_bonus_against_tt }'
    setup=''
    if isinstance(amount,int):
        setup='USA = { set_temp_variable = { '+P+'preview_material = '+P+'cache_'+h+' } add_to_temp_variable = { '+P+'preview_material = '+str(amount)+' } }\n'
        amount='USA.'+P+'preview_material'
        if h=='irq':more+='\n'+(fiscal.charge(-Decimal(str(fiscal.US_SETUP['legacy'])),'USA.gdp_total') if tier=='legacy' else 'set_temp_variable = { treasury_change = USA.'+P+'legacy_irq_cash }\nmodify_treasury_effect = yes')
    return effect_preview(setup+'custom_effect_tooltip = '+P+'if_accept_'+r.lower()+'_tt\nUSA = { add_ideas = '+P+'aid_'+suffix+'_usa\n'+fiscal.weekly_rows(rate)+' }\n'+r+' = { add_ideas = '+P+'aid_'+suffix+'_partner\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = '+str(amount)+' producer = USA }\n'+fiscal.weekly_rows(rate,1,'USA.gdp_total',True)+more+' }')

def build(loc,fx,tr,ideas):
    reconcile=[]
    for h,d in HOSTS.items():
        for r in (['KUR','PUK'] if h=='irq' else [d['rebel']]):
            key=h+'_'+r.lower();valid='country_exists = '+r+'\n'+P+'funding_'+h+' = yes\nNOT = { '+P+'settlement_protects_'+h+' = yes }\nis_in_array = { array = '+P+'payees_'+h+' value = '+r+' }'
            loc[P+'if_accept_'+r.lower()+'_tt']='If ['+r+'.GetNameDef] accepts:'
            for tier in ((2,3,'legacy') if h=='irq' else (2,3)):
                suffix=key+'_'+str(tier);rate='us_legacy' if tier=='legacy' else 'us_armed' if tier==3 else 'us_funded'
                for who,sign in (('usa',-1),('partner',1)):
                    ident='aid_'+suffix+'_'+who;loc[P+ident]='Regional Assistance Budget' if who=='usa' else 'American Material Assistance'
                    loc[P+ident+'_desc']='The accepted liaison arrangement provides continuing American financial support and access to material assistance.'
                    loc[P+ident+'_weekly_tt']=fiscal.weekly_text(rate,sign,True)
                    raw=idea(ident,'','',{},weekly=True)
                    if tier=='legacy' and who=='partner':raw=raw[:-1]+b('targeted_modifier','tag = IRQ\ndefense_bonus_against = .08')+'\n}'
                    ideas.append(raw)
                condition=valid+'\n'+(check('legacy_irq_rate','>',0) if tier=='legacy' else check('stage_'+h,'=',tier))
                if h=='irq' and tier!='legacy':condition+='\n'+check('legacy_irq_rate','=',0)
                ensure='if = { limit = { NOT = { has_idea = '+P+'aid_'+suffix+'_usa } } add_ideas = '+P+'aid_'+suffix+'_usa }\n'+r+' = { if = { limit = { NOT = { has_idea = '+P+'aid_'+suffix+'_partner } } add_ideas = '+P+'aid_'+suffix+'_partner } }'
                remove='remove_ideas = '+P+'aid_'+suffix+'_usa\n'+r+' = { remove_ideas = '+P+'aid_'+suffix+'_partner }'
                reconcile.append(guard(condition,ensure)+'\n'+b('else',remove))
            normal=guard('USA = { OR = { '+check('stage_'+h,'>',2)+' AND = { '+check('stage_'+h,'=',0)+' '+check('max_stage_'+h,'>',2)+' } } }',preview(h,r,3,'USA.'+P+'cache_'+h))+'\n'+b('else',preview(h,r,2,'USA.'+P+'cache_'+h))
            if h=='irq':normal=guard('USA = { '+check('legacy_irq_rate','>',0)+' }',preview(h,r,'legacy','USA.'+P+'cache_'+h))+'\n'+b('else',normal)
            if h=='irq':normal+='\n'+effect_preview('set_temp_variable = { treasury_change = USA.'+P+'legacy_irq_cash }\nmodify_treasury_effect = yes')
            fx[P+'cache_preview_'+key]=normal
    fx[P+'reconcile_aid']=guard(P+'usa_actor = yes','\n'.join(reconcile))
