# IMPERIA COLD WAR — Brazil recipient-controlled standing agreements and weekly budgets.
from common import *

def build_diplomacy(d):
    files={};loc={};triggers=[];effects=[];ideas=[];decisions=[];renew=[];events=['add_namespace = COLDWAR_BRA_AGREEMENTS']
    offers=[n for n in d['nodes'] if 'offer' in n];by={n['key']:n for n in d['nodes']}
    loc.update({P+'agreements':'Brazilian Cooperation Proposals',P+'agreements_desc':'Review the terms proposed by the Brazilian government.',P+'renewals':'Existing Diplomatic Proposals',P+'renewals_desc':'Renew an unanswered or declined proposal already authorised by a national focus.'})
    partners=sorted(set(n['offer']['partner'] for n in offers))
    sanc=['imp_'+c+'_sanc_'+di for c in ('dip','fin','eco','mil') for di in ('on_us','by_us')]
    def no_sanctions(tag):return neg(block('OR',*['is_in_array = { array = '+a+' value = '+tag+' }' for a in sanc]))
    for tag in partners:
        checks=['country_exists = BRA','country_exists = '+tag,neg('has_war_with = '+tag),neg('is_embargoing = '+tag),no_sanctions(tag),country(tag,neg('has_war_with = BRA')+'\n'+neg('is_embargoing = BRA')+'\n'+no_sanctions('BRA'))]
        triggers.append(block(P+'pair_'+tag+'_clear',*checks))
        title=next(n['offer']['partner_name'] for n in offers if n['offer']['partner']==tag)
        tt=P+'pair_'+tag+'_clear_tt'
        loc[tt]='Brazil and '+title+' exist, are at peace with one another and impose no bilateral embargoes or sanctions.'
        loc[tt+'_NOT']='Brazil and '+title+' must exist and end any bilateral war, embargoes or sanctions.'
        triggers.append(block(P+'pair_'+tag+'_clear_visible',block('custom_trigger_tooltip','tooltip = '+tt,P+'pair_'+tag+'_clear = yes')))
    def scope(tag,body):return country(tag,body)
    def setup_checks(n):
        rows=[]
        for side in ('brazil','recipient'):
            tag='BRA' if side=='brazil' else n['offer']['partner']
            checks=['check_variable = { gdp_total > 0 }']
            checks.extend(asset_checks(e) for e in n['offer'][side]['effects'] if e['kind']=='building')
            rows.append(scope(tag,'\n'.join(checks)))
        return rows
    def parent_active(n):
        out=[]
        for c in n['conditions']:
            if c=='Active Brazil-Paraguay Itaipu agreement':out.append(P+'itaipu_active = yes')
            elif c=='Angola is independent and recognised':out.append('AGL = { is_subject = no }')
            elif c.startswith('Active '):raise ValueError((n['key'],c))
        return out
    def prospective(n):
        rows=['custom_effect_tooltip = '+P+'if_accept_tt']
        for side in ('brazil','recipient'):
            data=n['offer'][side];tag='BRA' if side=='brazil' else n['offer']['partner'];sr=[]
            for ix,e in enumerate(data['effects']):
                if e['kind']=='modifier':continue
                if e['kind']=='weekly_gdp_expense':sr.append(weekly_preview(e,n['key']+'_'+side+'_'+str(ix),loc))
                elif e['kind']=='weekly_transfer':sr.append(weekly_preview(e,n['key']+'_'+side+'_transfer',loc,'BRA.gdp_total',income=e['direction']=='income'))
                else:sr.append(finite_effect(e,n['key']+'_'+side,ix))
            sr.append('add_ideas = '+data['spirit']);rows.append(scope(tag,'\n'.join(sr)))
        return '\n'.join(rows)
    sync=[];orphan=[];expense=[];income=[]
    for i,n in enumerate(offers):
        k=n['key'];o=n['offer'];tag=o['partner'];eid='COLDWAR_BRA_AGREEMENTS.'+str(i+1)
        for side in ('brazil','recipient'):
            data=o[side];ideas.append(idea_def(data['spirit'],data['name'],data['effects'],'diplomacy',loc,n['description']))
        eligible=[P+'campaign = yes',flag('signed_'+k),scope(tag,flag('signed_'+k)),once('terminated_'+k),P+'pair_'+tag+'_clear = yes',*parent_active(n)]
        triggers.append(block(P+k+'_eligible',*eligible))
        triggers.append(block(P+k+'_active',P+k+'_eligible = yes','has_idea = '+o['brazil']['spirit'],scope(tag,'has_idea = '+o['recipient']['spirit'])))
        send=[P+'campaign = yes',P+'pair_'+tag+'_clear = yes',once('signed_'+k),once('terminated_'+k),*parent_active(n)]
        send.extend(once('signed_'+x) for x in n['exclusions'] if by[x].get('offer'))
        triggers.append(block(P+'can_propose_'+k,block('hidden_trigger',*[x for x in send if x!=P+'pair_'+tag+'_clear = yes']),P+'pair_'+tag+'_clear_visible = yes',*node_conditions(n)))
        accept=[P+'can_propose_'+k+' = yes',block('hidden_trigger',flag('pending_'+k),scope(tag,flag('pending_'+k)),*setup_checks(n))]
        for side in ('brazil','recipient'):
            assets=[asset_checks(e) for e in o[side]['effects'] if e['kind']=='building']
            if assets:accept.append(scope('BRA' if side=='brazil' else tag,block('custom_trigger_tooltip','tooltip = '+P+'assets_ready_tt',*assets)))
        triggers.append(block(P+'can_accept_'+k,*accept))
        effects.append(block(P+'offer_preview_'+k,prospective(n)))
        pending=[setflag('pending_'+k),scope(tag,setflag('pending_'+k)+'\ncountry_event = { id = '+eid+' days = 1 }')]
        effects.append(block(P+'propose_'+k,iff(P+'can_propose_'+k+' = yes\n'+once('pending_'+k),*pending)))
        # The sole acceptance transaction runs in BRA scope after both payers are validated.
        actual=[]
        for side in ('brazil','recipient'):
            data=o[side];payer='BRA' if side=='brazil' else tag
            awards=[]
            for ix,e in enumerate(data['effects']):
                if e['kind']=='building':awards.append(construction(e))
                elif e['kind'] not in ('modifier','weekly_gdp_expense','weekly_transfer'):awards.append(finite_effect(e,k+'_'+side,ix))
            actual.append(scope(payer,iff(once('paid_'+k),*awards,setflag('paid_'+k))))
        actual += [setflag('signed_'+k),clearflag('pending_'+k),scope(tag,setflag('signed_'+k)+'\n'+clearflag('pending_'+k)),P+'sync_agreements = yes']
        assets=[('BRA' if side=='brazil' else tag,e) for side in ('brazil','recipient') for e in o[side]['effects'] if e['kind']=='building']
        effects.append(block(P+'accept_initiator_'+k,iff(P+'can_accept_'+k+' = yes',asset_transaction(assets,actual))))
        effects.append(block(P+'accept_'+k,iff('tag = '+tag+'\n'+flag('pending_'+k),scope('BRA',P+'accept_initiator_'+k+' = yes'))))
        decline=[scope('BRA',clearflag('pending_'+k)+'\nset_country_flag = { flag = '+P+'proposal_cooldown_'+k+' days = 90 }'),clearflag('pending_'+k)]
        effects.append(block(P+'decline_'+k,iff('tag = '+tag+'\n'+flag('pending_'+k),*decline)))
        activate=[iff(neg('has_idea = '+o['brazil']['spirit']),'add_ideas = '+o['brazil']['spirit']),scope(tag,iff(neg('has_idea = '+o['recipient']['spirit']),'add_ideas = '+o['recipient']['spirit']))]
        deactivate=[iff('has_idea = '+o['brazil']['spirit'],'remove_ideas = '+o['brazil']['spirit']),scope(tag,iff('has_idea = '+o['recipient']['spirit'],'remove_ideas = '+o['recipient']['spirit']))]
        sync.extend([iff(P+k+'_eligible = yes',*activate),block('else',*deactivate)])
        effects.append(block(P+'terminate_'+k,iff(P+'campaign = yes',setflag('terminated_'+k),clearflag('signed_'+k),clearflag('pending_'+k),scope(tag,clearflag('signed_'+k)+'\n'+clearflag('pending_'+k)),*deactivate)))
        effects.append(block(P+'preview_termination_'+k,scope('BRA','remove_ideas = '+o['brazil']['spirit']),scope(tag,'remove_ideas = '+o['recipient']['spirit'])))
        orphan.append(iff('tag = '+tag+'\nNOT = { country_exists = BRA }','remove_ideas = '+o['recipient']['spirit'],clearflag('pending_'+k)))
        for side in ('brazil','recipient'):
            payer='BRA' if side=='brazil' else tag
            for ix,e in enumerate(o[side]['effects']):
                if e['kind']=='weekly_gdp_expense':
                    active='tag = '+payer+'\nBRA = { '+P+k+'_active = yes }'
                    body='set_temp_variable = { '+P+'stream = { value = gdp_total multiply = '+share(e['annual_gdp_percent'])+' divide = 52 } }\nadd_to_variable = { '+P+'cooperation_weekly_expense = '+P+'stream }'
                    expense.append(iff(active,body))
                elif e['kind']=='weekly_transfer':
                    is_income=e['direction']=='income';agg='cooperation_weekly_income' if is_income else 'cooperation_weekly_expense'
                    body='set_temp_variable = { '+P+'stream = { value = BRA.gdp_total multiply = '+share(e['annual_gdp_percent'])+' divide = 52 } }\nadd_to_variable = { '+P+agg+' = '+P+'stream }'
                    (income if is_income else expense).append(iff('tag = '+payer+'\nBRA = { '+P+k+'_active = yes }',body))
        loc[P+'accept_'+k]='Accept: '+n['title'];loc[P+'accept_'+k+'_desc']=n['description']
        loc[P+'decline_'+k]='Decline: '+n['title'];loc[P+'decline_'+k+'_desc']='Decline this proposal without undertaking its financial or institutional commitments.'
        loc[P+'renew_'+k]='Renew: '+n['title'];loc[P+'renew_'+k+'_desc']='Present the existing national proposal again for the other government’s consideration.'
        decisions += [block(P+'accept_'+k,'icon = generic_diplomacy',block('visible','tag = '+tag,flag('pending_'+k)),block('available','tag = '+tag,scope('BRA',P+'can_accept_'+k+' = yes')),'cost = 0','days_remove = 1',block('complete_effect',block('effect_tooltip',P+'offer_preview_'+k+' = yes'),block('hidden_effect',P+'accept_'+k+' = yes')),block('ai_will_do','factor = 1')),block(P+'decline_'+k,'icon = generic_diplomacy',block('visible','tag = '+tag,flag('pending_'+k)),block('available','tag = '+tag,flag('pending_'+k)),'cost = 0','days_remove = 1',block('complete_effect',block('hidden_effect',P+'decline_'+k+' = yes')),block('ai_will_do','factor = 0.25'))]
        renewal=[P+'campaign = yes','has_completed_focus = '+n['id'],once('pending_'+k),once('signed_'+k),once('terminated_'+k)]
        renew.append(block(P+'renew_'+k,'icon = generic_diplomacy',block('visible',*renewal),block('available',*renewal,once('proposal_cooldown_'+k),P+'can_propose_'+k+' = yes'),'cost = 0','days_remove = 1',block('complete_effect',block('effect_tooltip',P+'offer_preview_'+k+' = yes'),block('hidden_effect',P+'propose_'+k+' = yes')),block('ai_will_do','factor = 0')))
        loc[eid+'.t']=n['title'];loc[eid+'.d']='Brazil has proposed a standing cooperation agreement. The government must decide whether to undertake the terms.';loc[eid+'.review']='Review the proposal'
        events.append(block('country_event','id = '+eid,'title = '+eid+'.t','desc = '+eid+'.d','picture = '+picture_for(eid),'is_triggered_only = yes',block('option','name = '+eid+'.review',block('effect_tooltip',P+'offer_preview_'+k+' = yes'))))

    effects.append(block(P+'sync_agreements',iff(P+'campaign = yes',*sync)))
    effects.append(block(P+'cleanup_orphaned_agreements',*orphan))
    expense_body=['set_variable = { '+P+'cooperation_weekly_expense = 0 }',*expense,'add_to_variable = { additional_expenses_rate = '+P+'cooperation_weekly_expense }',P+'add_domestic_weekly_expenses = yes','set_variable = { '+P+'total_weekly_expense = '+P+'cooperation_weekly_expense }',iff(P+'campaign = yes','add_to_variable = { '+P+'total_weekly_expense = '+P+'domestic_weekly }'),'set_variable = { '+P+'total_weekly_expense_millions = { value = '+P+'total_weekly_expense multiply = 1000 } }']
    income_body=['set_variable = { '+P+'cooperation_weekly_income = 0 }',*income,'add_to_variable = { additional_income_rate = '+P+'cooperation_weekly_income }','set_variable = { '+P+'cooperation_weekly_income_millions = { value = '+P+'cooperation_weekly_income multiply = 1000 } }']
    effects.append(block(P+'add_weekly_expenses',*expense_body))
    effects.append(block(P+'add_weekly_income',*income_body))
    # Native monetary breakdown strings are additive hooks, not extra debits.
    displays=[]
    for field,label,color in [('expense','Additional Expenses','R'),('income','Additional Income','G')]:
        variable=P+('total_weekly_expense' if field=='expense' else 'cooperation_weekly_income')
        loc[variable+'_line']='\n'+('Brazilian Programmes' if field=='expense' else 'Brazilian Cooperation')+': $$[?'+variable+'_millions|'+color+'2] Million/week'
        displays.append(block('defined_text','name = '+P+'weekly_'+field+'_display',block('text',block('trigger','check_variable = { '+variable+' > 0 }'),'localization_key = '+variable+'_line'),block('text','localization_key = '+P+'empty')))
    loc[P+'empty']=''
    files.update(output('common/scripted_localisation/COLDWAR_BRA_1970_money.txt','\n\n'.join(displays)))
    files.update(output('common/scripted_effects/COLDWAR_BRA_1970_diplomacy_effects.txt','\n\n'.join(effects)))
    files.update(output('common/scripted_triggers/COLDWAR_BRA_1970_diplomacy_triggers.txt','\n\n'.join(triggers)))
    files.update(output('common/ideas/COLDWAR_BRA_1970_diplomacy_ideas.txt',block('ideas',block('country',*ideas))))
    files.update(output('common/decisions/COLDWAR_BRA_1970_agreements.txt',block(P+'agreements',*decisions)+'\n\n'+block(P+'renewals',*renew)))
    pending=block('OR',*[flag('pending_'+n['key']) for n in offers])
    cats=[block(P+'agreements','icon = GFX_decision_category_generic_foreign_policy','allowed = { always = yes }',block('visible',pending)),block(P+'renewals','icon = GFX_decision_category_generic_foreign_policy','allowed = { original_tag = BRA }',block('visible',P+'campaign = yes'))]
    files.update(output('common/decisions/categories/COLDWAR_BRA_1970_agreements_categories.txt','\n\n'.join(cats)))
    files.update(output('events/COLDWAR_BRA_1970_agreement_events.txt','\n\n'.join(events)))
    return dict(files=files,loc=loc)
