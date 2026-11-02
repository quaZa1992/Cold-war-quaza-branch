# IMPERIA COLD WAR — Long-term regional reconciliation and paid foreign pressure.
from .shared import *
from .deals import locals_for
from . import fiscal


def build(loc,fx,tr,ideas,decisions):
    mods={'Stability':.02,'Foreign Influence Defense':.05,'Bureaucracy Cost':.01}
    loc[P+'consolidated_compact']='Consolidated Regional Institutions'
    loc[P+'consolidated_compact_desc']='Years of local rights, funded development and sustained security have consolidated the regional settlement. Renewed foreign intervention or the abandonment of its political foundations can still undermine it.'
    ideas.append(idea('consolidated_compact','','',mods,'COLDWAR_USA_KS_institutions'))
    loc[P+'reconciliation_tt']='Reconciliation progress is at least 520 weeks, including at least 312 weeks of sustained regional policy.'
    loc[P+'reconciliation_conditions_tt']='Regional rights are respected, unrest is below 10, lasting stabilisation is at least 80, development is funded, at least two divisions are stationed in the region, all contested states remain under peaceful government control, and no legacy of repression remains.'
    loc[P+'pressure_clear_tt']='No active American campaign to intensify regional resistance.'
    loc[P+'pressure_ready_tt']='Armed regional assistance is active and no American-guaranteed political settlement is in force.'
    loc[P+'pressure_duration_tt']='Intensified regional support: $RIGHT|0$ weeks'
    loc[P+'weekly_unrest_tt']='Weekly foreign unrest pressure: $RIGHT|+2$'
    loc[P+'reconciliation_weeks_tt']='Regional reconciliation credit: $RIGHT|+=0$ weeks'
    fx[P+'reconciliation_total']=f'set_variable = {{ {P}reconciliation_weeks = {P}qualifying_weeks }}\nadd_to_variable = {{ {P}reconciliation_weeks = {P}reform_credit }}\nclamp_variable = {{ var = {P}reconciliation_weeks min = 0 max = 520 }}'
    for h,d in HOSTS.items():
        tag=d['tag'];deal='irq_settlement' if h=='irq' else d['rights']
        tr[P+'pressure_'+h]=b(tag,check('pressure_weeks','>',0))+'\n'+P+'funding_'+h+' = yes\nUSA = { '+check('stage_'+h,'>',2)+' NOT = { '+P+'deal_'+deal+'_active = yes } }'
        tr[P+'settlement_protects_'+h]=P+'rights_'+h+' = yes\nNOT = { '+P+'pressure_'+h+' = yes }'
        controlled='\n'.join(str(s)+' = { is_owned_and_controlled_by = '+tag+' is_fully_controlled_by = '+tag+' }' for s in d['states'])
        peace='\n'.join('NOT = { has_war_with = '+r+' }' for r in locals_for(h))
        conditions='tag = '+tag+'\n'+flag('tracked')+'\n'+P+'rights_'+h+' = yes\n'+flag('investment')+'\n'+P+'forces_'+h+' = yes\n'+check('unrest','<',10)+'\n'+at_least(P+'stabilisation',80)+'\n'+check('trauma_weeks','=',0)+'\n'+controlled+'\nNOT = { has_war_with = USA }\n'+peace
        tr[P+'reconciliation_conditions_'+h]=requirement('reconciliation_conditions_tt',conditions)
        # Qualifying time is earned, never a calendar gate or a one-click reset.
        # A foreign surge prevents consolidation even when troops contain unrest.
        valid_compact=P+'rights_'+h+' = yes\n'+controlled+'\nNOT = { has_war_with = USA }\n'+peace
        fracture=f'clr_country_flag = {P}pacified\nremove_ideas = {P}consolidated_compact\n'+v('qualifying_weeks',156)+'\n'+v('breakdown_weeks',0)
        progress=guard(noflag('pacified'),
          guard(P+'reconciliation_conditions_'+h+' = yes\nNOT = { '+P+'pressure_'+h+' = yes }',add('qualifying_weeks',1))+'\n'+b('else',add('qualifying_weeks',-2)))
        strain=guard(flag('pacified')+'\n'+P+'pressure_'+h+' = yes\n'+check('unrest','>',19),add('breakdown_weeks',1)+'\n'+guard(check('breakdown_weeks','>',25),fracture))+'\n'+b('else',v('breakdown_weeks',0))
        fx[P+'peace_tick_'+h]='\n'.join([guard(flag('pacified')+'\nNOT = { '+valid_compact+' }',fracture),progress,
          f'clamp_variable = {{ var = {P}qualifying_weeks min = 0 max = 520 }}',strain,P+'reconciliation_total = yes',
          guard(check('pressure_weeks','>',0),add('pressure_weeks',-1))])

        key=P+h+'_consolidate';loc[key]='Consolidate the regional settlement'
        loc[key+'_desc']='Reconciliation: §Y[?'+tag+'.'+P+'reconciliation_weeks|0]/520 weeks§!. Sustained policy: §Y[?'+tag+'.'+P+'qualifying_weeks|0] weeks§!. Major reforms can contribute up to 208 weeks, reducing the minimum from ten to six years. Maintain rights, funded development, two deployed divisions, stabilisation of at least 80 and unrest below 10. Setbacks cost two weeks of sustained progress per week. Consolidation ends spontaneous unrest and ordinary foreign agitation; a major foreign campaign can reopen the dispute after prolonged deterioration.'
        valid='tag = '+tag+'\n'+flag('tracked')+'\n'+noflag('pacified')+'\n'+P+'reconciliation_conditions_'+h+' = yes\n'+requirement('pressure_clear_tt','NOT = { '+P+'pressure_'+h+' = yes }')+'\n'+requirement('reconciliation_tt',at_least(P+'reconciliation_weeks',520)+'\n'+at_least(P+'qualifying_weeks',312))+'\ncheck_variable = { '+P+'settlement_quote > 0 }\n'+at_least('treasury',P+'settlement_quote')
        shown=effect_preview(fiscal.cost_rows(10)+'\nadd_ideas = '+P+'consolidated_compact\n'+modifier_rows(mods))
        execute=fiscal.purchase(10,setflag('pacified')+'\n'+v('unrest',0)+'\n'+v('organisation',0)+'\n'+v('breakdown_weeks',0)+'\nadd_ideas = '+P+'consolidated_compact\n'+P+'refresh_host = yes\nupdate_money_dirty_variable = yes')
        fx[key]=guard(valid,execute)
        ai=b('ai_will_do',['factor = 1',b('modifier','factor = 0\nhas_active_mission = bankruptcy_incoming_collapse')])
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('tracked')+'\n'+noflag('pacified')),b('available',valid),'cost = 200',b('complete_effect',visible_and_hidden(shown,key+' = yes')),ai]))

        reforms=[('rights_charter','Entrench Regional Rights',52,.10,'Constitutional guarantees, recognised language rights and enforceable local representation give regional institutions a lasting foundation.'),
          ('revenue','Regional Revenue Settlement',104,.12,'A funded revenue-sharing compact transfers a substantial fiscal reserve to regional institutions and public services.'),
          ('integration','Integrate Regional Public Institutions',156,.15,'Recruit local civil servants and accountable police, recognise qualifications and build a common regional administration.'),
          ('reconstruction','Civilian Reconstruction Commission',208,.18,'Fund a major civilian reconstruction programme, independent auditing and compensation for communities affected by the conflict.')]
        for index,(suffix,title,weeks,share,description) in enumerate(reforms,1):
            key=P+h+'_reform_'+suffix;receipt='reform_'+str(index)
            loc[key]=title;loc[key+'_desc']=description+' Each completed programme contributes 52 weeks towards reconciliation. The four programmes cost 55% of current annual GDP in total at unchanged GDP, before the final settlement. Sustained deployment, local rights and development remain necessary.'
            milestone=P+'reform_milestone_'+str(index)+'_tt';loc[milestone]=str(weeks)+' weeks of sustained regional policy have been completed.'
            valid='tag = '+tag+'\n'+flag('tracked')+'\n'+noflag('pacified')+'\n'+noflag(receipt)+'\n'+P+'reconciliation_conditions_'+h+' = yes\n'+requirement('pressure_clear_tt','NOT = { '+P+'pressure_'+h+' = yes }')+'\ncustom_trigger_tooltip = { tooltip = '+milestone+' '+at_least(P+'qualifying_weeks',weeks)+' }\n'+at_least('treasury',P+'reform_quote_'+str(index))+'\ncheck_variable = { '+P+'reform_quote_'+str(index)+' > 0 }'
            if index>1:
                previous=P+'reform_previous_'+str(index)+'_tt';loc[previous]=reforms[index-2][1]+' has been completed.'
                valid+='\ncustom_trigger_tooltip = { tooltip = '+previous+' '+flag('reform_'+str(index-1))+' }'
            percent=Decimal(str(share))*100
            execute=fiscal.purchase(percent,setflag(receipt)+'\n'+add('reform_credit',52)+f'\nclamp_variable = {{ var = {P}reform_credit min = 0 max = 208 }}\n'+P+'reconciliation_total = yes\n'+P+'refresh_host = yes')
            fx[key]=guard(valid,execute)
            shown=effect_preview(fiscal.cost_rows(percent)+'\n'+scalar_row('reconciliation_weeks',52))
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('tracked')+'\n'+noflag(receipt)+'\n'+noflag('pacified')),b('available',valid),'cost = 100',b('complete_effect',visible_and_hidden(shown,key+' = yes')),ai]))

        key=P+h+'_intensify';loc[key]='Fuel the Kurdish Insurgency: '+d['name']
        loc[key+'_desc']='Finance six months of intensified Kurdish organisation and clandestine arms support inside '+d['name']+'. The resistance can be strengthened before a Kurdish state exists. Respected local rights remain a source of calm, but no longer guarantee immunity from an armed mobilisation during the campaign. Government deployments and sustained regional spending can contain the pressure. A consolidated settlement only breaks after 26 consecutive weeks of unrest above 19 under active foreign pressure.'
        loc[key+'_desc']+=' Initial funding: '+num(fiscal.US_SETUP['intensify'])+'% of US GDP. Additional weekly funding: '+num(fiscal.WEEKLY['us_surge'])+'% of US GDP.'
        valid=P+'usa_actor = yes\n'+flag('contact_'+h)+'\n'+tag+' = { '+flag('tracked')+' '+check('pressure_weeks','=',0)+' }\n'+P+'region_'+h+' = yes\n'+P+'confrontation_'+h+' = yes\n'+requirement('pressure_ready_tt',P+'funding_'+h+' = yes\n'+check('stage_'+h,'>',2)+'\nNOT = { '+P+'deal_'+deal+'_active = yes }')+'\n'+P+'route_'+h+' = yes\n'+fiscal.affordable('us_intensify_quote')+'\ncustom_trigger_tooltip = { tooltip = '+P+'equipment_tt has_equipment = { infantry_weapons_1 > 999 } }'
        execute=fiscal.purchase(fiscal.US_SETUP['intensify'],'add_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+add('cache_'+h,1000)+'\n'+b(tag,v('pressure_weeks',26)+'\n'+add('organisation',10)+f'\nclamp_variable = {{ var = {P}organisation min = 0 max = 100 }}\n'+P+'refresh_host = yes')+'\n'+P+'reconcile_aid = yes\nupdate_money_dirty_variable = yes')
        shown=effect_preview(fiscal.cost_rows(fiscal.US_SETUP['intensify'])+'\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+scalar_row('material',1000)+'\n'+fiscal.weekly_rows('us_surge')+'\n'+b(tag,scalar_row('organisation',10)+'\n'+scalar_row('weekly_unrest',9)+'\n'+f'set_variable = {{ {P}preview_pressure = 26 tooltip = {P}pressure_duration_tt }}'))
        # This unilateral operation changes the host's underground movement.
        # A future state's separate material-acceptance decision previews its
        # own complete bilateral terms when it can actually receive a shipment.
        fx[key]=guard(valid,execute)
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('contact_'+h)+'\n'+check('max_stage_'+h,'>',2)),b('available',valid),'cost = 75',b('complete_effect',visible_and_hidden(shown,key+' = yes')),'ai_will_do = { factor = 0.2 }']))
