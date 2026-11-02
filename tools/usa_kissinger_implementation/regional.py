# IMPERIA COLD WAR — Persistent regional unrest and lasting stabilisation.
from .shared import *
from .deals import clear
from . import fiscal

def build(loc,fx,tr,ideas,decisions,categories):
    loc[P+'regional_category']='Regional Security'
    loc[P+'security_programme']='Regional Security Operation'
    loc[P+'security_programme_desc']='A sustained deployment supports the regional authorities. Successful operations leave a period of calm that can outlast the deployment.'
    loc[P+'security_programme_weekly_tt']=fiscal.weekly_text('security')
    loc[P+'investment_programme']='Regional Development Programme'
    loc[P+'investment_programme_desc']='Local institutions, public investment and recognised rights offer a slower and less coercive answer to regional grievances.'
    loc[P+'investment_programme_weekly_tt']=fiscal.weekly_text('investment')
    ideas.append(idea('security_programme','','',{'Army Personnel Cost':.05},'generic_military_reform',weekly=True))
    ideas.append(idea('investment_programme','','',{'Bureaucracy Cost':.01},'COLDWAR_USA_KS_institutions',weekly=True))
    tr[P+'usa_actor']='hidden_trigger = { tag = USA IMP_is_1970_scenario = yes NOT = { has_country_flag = MD_skip_treasury_cost } }'
    tr[P+'slot_available']='custom_trigger_tooltip = { tooltip = '+P+'slot_available_tt OR = { check_variable = { '+P+'campaign_count < 2 } AND = { has_completed_focus = '+P+'expanded check_variable = { '+P+'campaign_count < 4 } } } }'
    slot_count=[];streams=[];observers=[]
    for h,d in HOSTS.items():
        tag=d['tag'];states=d['states'];rebels=['KUR','PUK'] if h=='irq' else [d['rebel']]
        region=state_test(tag,states)
        tr[P+'region_'+h]='country_exists = '+tag+'\ncustom_trigger_tooltip = { tooltip = '+P+'eligible_region_tt '+region+' }'
        tr[P+'forces_'+h]='custom_trigger_tooltip = { tooltip = '+P+'field_forces_tt '+tag+' = { num_divisions_in_states = { count > 1 states = { '+' '.join(map(str,states))+' } } } }'
        tr[P+'confrontation_'+h]='custom_trigger_tooltip = { tooltip = '+P+'confrontation_tt '+tag+' = { OR = { has_war_with = USA has_opinion = { target = USA value < 0 } USA = { '+flag('breach_'+h)+' } } } }'
        # Actual access is accepted by a distinct border government. Existing
        # Gulf access remains a valid Iraqi route, retaining its real consent.
        routes=['AND = { USA = { '+P+'deal_irq_transit_active = yes } '+tag+' = { is_neighbor_of = PER } }',
                'AND = { USA = { '+P+'deal_irq_anatolia_active = yes } '+tag+' = { is_neighbor_of = TUR } }']
        if h=='irq':routes.append('COLDWAR_USA_gulf_clandestine_route_open = yes')
        tr[P+'route_'+h]=requirement('route_tt','OR = { '+' '.join(routes)+' AND = { USA = { '+flag('air_route_'+h)+' has_equipment = { transport_plane1 > 4 } any_owned_state = { air_base > 0 is_controlled_by = USA } } } }')
        partner_active=' '.join(r+' = { exists = yes '+flag('partner_'+h)+' any_owned_state = { OR = { '+' '.join('state = '+str(s) for s in states)+' } is_controlled_by = PREV } }' for r in rebels)
        payee_tests=[]
        for r in rebels:
            tr[P+'payee_clear_'+r.lower()]=clear(r)
            payee_tests.append('OR = { USA = { NOT = { is_in_array = { array = '+P+'payees_'+h+' value = '+r+' } } } NOT = { country_exists = '+r+' } USA = { '+P+'payee_clear_'+r.lower()+' = yes } }')
        tr[P+'funding_'+h]='USA = { '+P+'usa_actor = yes '+check('stage_'+h,'>',0)+' '+P+'route_'+h+' = yes }\nOR = { '+P+'region_'+h+' = yes '+partner_active+' }\n'+'\n'.join(payee_tests)
        tr[P+'material_'+h]='USA = { OR = { '+check('cache_'+h,'>',999)+' '+ ' '.join('AND = { '+check('delivered_'+h+'_'+r.lower(),'>',999)+' '+r+' = { exists = yes '+flag('partner_'+h)+' } }' for r in rebels)+' } }'
        if h=='irq':rights='OR = { USA = { '+P+'deal_irq_settlement_active = yes } COLDWAR_USA_gulf_settlement_respected = yes }'
        else:rights='USA = { '+P+'deal_'+d['rights']+'_active = yes }'
        tr[P+'rights_'+h]=rights
        fx[P+'init_'+h]=guard('tag = USA\ncountry_exists = '+tag,b(tag,guard(noflag('tracked'),setflag('tracked')+'\n'+v('unrest',d['base'])+'\n'+v('stabilisation',0)+'\n'+v('organisation',0)+'\n'+v('qualifying_days',0)+'\n'+v('warning_days',0)+'\n'+P+'refresh_host = yes')))
        stage_exists=check('stage_'+h,'>',0)
        slot_count.append(guard(stage_exists,add('campaign_count',1)))
        payer=guard(check('stage_'+h,'>',2),fiscal.stream('expense','us_armed'))+'\n'+b('else_if',[b('limit',check('stage_'+h,'>',1)),fiscal.stream('expense','us_funded')])
        if h=='irq':payer=guard(check('legacy_irq_rate','>',0),fiscal.stream('expense','us_legacy'))+'\n'+b('else',payer)
        streams.append(guard('tag = USA\n'+P+'funding_'+h+' = yes\nNOT = { '+P+'settlement_protects_'+h+' = yes }',payer))
        streams.append(guard('tag = USA\n'+P+'pressure_'+h+' = yes',fiscal.stream('expense','us_surge')))
        streams.append(guard('tag = USA\n'+flag('air_route_'+h)+'\n'+P+'funding_'+h+' = yes',fiscal.stream('expense','us_air')))
        # Contact programmes without a paid stage still preserve their ledger.
        # Weekly updating is country-local and bounded to these four hosts.
        tick=[v('drift',0),guard(noflag('pacified'),v('drift',1)),v('support',0)]
        for stage,amount in ((3,5.32),(2,2.85),(1,1.33)):
            tick.append(guard('USA = { '+check('stage_'+h,'=',stage)+' }\n'+P+'funding_'+h+' = yes\nNOT = { '+P+'settlement_protects_'+h+' = yes }',v('support',amount)))
        tick.append(guard(P+'pressure_'+h+' = yes',add('drift',9)))
        tick.append(guard(check('trauma_weeks','>',0),'add_to_variable = { '+P+'drift = '+P+'trauma_drift }'))
        tick.append(f'add_to_variable = {{ {P}drift = {P}support }}\nset_temp_variable = {{ {P}organisation_effect = {P}organisation }}\nmultiply_temp_variable = {{ {P}organisation_effect = .01 }}\nadd_to_variable = {{ {P}drift = {P}organisation_effect }}')
        # Two divisions count as a meaningful field commitment. Four offers
        # additional containment, but no permanent end to regional politics.
        for count in range(1,5):tick.append(guard('num_divisions_in_states = { count > '+str(count-1)+' states = { '+' '.join(map(str,states))+' } }',add('drift',-1.2)))
        tick += [guard(flag('security')+'\n'+P+'forces_'+h+' = yes',add('drift',-3)),
          guard(flag('security')+'\n'+P+'forces_'+h+' = yes',add('stabilisation',3.5))+'\n'+b('else_if',[b('limit',flag('investment')),add('stabilisation',.98)])+'\n'+b('else',[add('stabilisation',-.7)]),
          f'clamp_variable = {{ var = {P}stabilisation min = 0 max = 100 }}',
          f'set_temp_variable = {{ {P}legacy_effect = {P}stabilisation }}',
          f'multiply_temp_variable = {{ {P}legacy_effect = -.08 }}',
          f'add_to_variable = {{ {P}drift = {P}legacy_effect }}',
          guard(flag('investment'),add('investment_weeks',1)+'\n'+guard(check('investment_weeks','>',5),add('drift',-2.1))),
          guard(P+'rights_'+h+' = yes',add('drift',-4.5)+'\n'+add('stabilisation',1.4)),
          f'add_to_variable = {{ {P}unrest = {P}drift }}',f'clamp_variable = {{ var = {P}unrest min = 0 max = 100 }}',
          f'clamp_variable = {{ var = {P}stabilisation min = 0 max = 100 }}',
          P+'peace_tick_'+h+' = yes',P+'repression_tick = yes',add('ui_dirty',1)]
        # A visible warning gives the defending player time to react. The
        # campaign continues after containment, war and reconquest.
        eligible=P+'region_'+h+' = yes\n'+check('unrest','>',79)+'\nNOT = { '+P+'settlement_protects_'+h+' = yes }\n'+P+'material_'+h+' = yes\n'+P+'funding_'+h+' = yes\nUSA = { '+check('stage_'+h,'>',2)+' }'
        for r in rebels:eligible+='\nNOT = { has_war_with = '+r+' }'
        tr[P+'mobilisation_'+h]=eligible
        advance_warning=guard(check('qualifying_days','>',29),
            guard(noflag('warning'),setflag('warning')+'\ncountry_event = { id = COLDWAR_USA_KS.'+str(110+list(HOSTS).index(h))+' }')+'\n'+add('warning_days',7)+'\n'+guard(check('warning_days','>',44),setflag('mobilisation_ready')))+'\n'+b('else',add('qualifying_days',7))
        tick.append(guard(eligible,v('below_days',0)+'\n'+advance_warning)+'\n'+b('else',[add('below_days',7),guard(check('below_days','>',14),v('qualifying_days',0)+'\n'+v('warning_days',0)+f'\nclr_country_flag = {P}warning\nclr_country_flag = {P}mobilisation_ready')]))
        # Historical/legacy campaign migration is run only for Iraq. No broad
        # world scan and no replayed focus or equipment grant on reload.
        fx[P+'tick_'+h]=guard(f'tag = {tag}\nIMP_is_1970_scenario = yes\n{flag("tracked")}', '\n'.join(tick))
        observers.append(guard('tag = '+tag,P+'tick_'+h+' = yes'))
        streams += [guard('tag = '+tag+'\n'+flag('security'),fiscal.stream('expense','security')),guard('tag = '+tag+'\n'+flag('investment'),fiscal.stream('expense','investment'))]
        for r in rebels:
            payee=f'tag = {r}\n{P}funding_{h} = yes\nNOT = {{ {P}settlement_protects_{h} = yes }}\nUSA = {{ is_in_array = {{ array = {P}payees_{h} value = PREV }} }}'
            income=guard('USA = { '+check('stage_'+h,'>',2)+' }',fiscal.stream('income','us_armed',True))+'\n'+b('else_if',[b('limit','USA = { '+check('stage_'+h,'>',1)+' }'),fiscal.stream('income','us_funded',True)])
            if h=='irq':income=guard('USA = { '+check('legacy_irq_rate','>',0)+' }',fiscal.stream('income','us_legacy',True))+'\n'+b('else',income)
            streams.append(guard(payee,income))
        # The host pays a substantial setup invoice, then a small standing
        # weekly budget. Repeating a security decision never stacks its spirit.
        for policy,title,share in (('security','Regional Security Operation',.02),('investment','Regional Investment',.01)):
            did=P+h+'_'+policy;loc[did]=title
            loc[did+'_desc']=('A sustained, funded field operation can break up armed networks and leave a lasting period of calm after the troops depart.' if policy=='security' else 'Investment in local institutions and public services addresses regional grievances without relying on a permanent field deployment.')
            loc[did+'_desc']+=' Initial funding: '+num(Decimal(str(share))*100)+'% of current GDP. Weekly funding: '+num(fiscal.WEEKLY[policy])+'% of current GDP.'
            valid='tag = '+tag+'\n'+flag('tracked')+'\n'+noflag(policy)
            if policy=='security':valid+='\n'+P+'forces_'+h+' = yes'
            invoice=fiscal.calculate(P+'invoice',Decimal(str(share))*100,temporary=True)
            affordable=at_least('treasury',P+'invoice')
            body=invoice+'\n'+guard(valid+'\ncheck_variable = { '+P+policy+'_quote > 0 }\n'+affordable,f'set_temp_variable = {{ treasury_change = {P}invoice }}\nmultiply_temp_variable = {{ treasury_change = -1 }}\nmodify_treasury_effect = yes\n'+setflag(policy)+f'\nclr_country_flag = {P}'+('investment' if policy=='security' else 'security')+f'\nremove_ideas = {P}security_programme\nremove_ideas = {P}investment_programme\nadd_ideas = {P}{policy}_programme\nupdate_money_dirty_variable = yes')
            fx[did]=body
            preview=effect_preview(fiscal.cost_rows(Decimal(str(share))*100)+'\nadd_ideas = '+P+policy+'_programme\n'+modifier_rows({'Army Personnel Cost':.05} if policy=='security' else {'Bureaucracy Cost':.01})+'\n'+fiscal.weekly_rows(policy))
            available=valid+'\ncheck_variable = { '+P+policy+'_quote > 0 }\n'+at_least('treasury',P+policy+'_quote')
            other='investment' if policy=='security' else 'security'
            ai=b('ai_will_do',['factor = 2',b('modifier','factor = 0\n'+flag(other)),b('modifier','factor = 0\nhas_active_mission = bankruptcy_incoming_collapse')])
            decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\n'+flag('tracked')),b('available',available),'cost = 0',b('complete_effect',visible_and_hidden(preview,did+' = yes')),ai]))
        did=P+h+'_end_programme';loc[did]='End the regional programme';loc[did+'_desc']='Conclude the exceptional regional expenditure. Stabilisation already achieved remains and gradually fades over time.'
        ending=f'clr_country_flag = {P}security\nclr_country_flag = {P}investment\nremove_ideas = {P}security_programme\nremove_ideas = {P}investment_programme\nupdate_money_dirty_variable = yes'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible','tag = '+tag+'\nOR = { '+flag('security')+' '+flag('investment')+' }'),'cost = 0',b('complete_effect',b('hidden_effect',guard('tag = '+tag,ending))),'ai_will_do = { factor = 0 }']))
        # Pause and resume do not create cash or another equipment cache.
        for key,title,level in (('pause','Suspend regional assistance',0),('resume','Resume regional assistance',2)):
            did=P+h+'_'+key;loc[did]=title+': '+d['name'];loc[did+'_desc']='Adjust the continuing American commitment. The local political situation and material already delivered remain in place.'
            available=P+'usa_actor = yes\n'+flag('contact_'+h)
            if key=='pause':available+='\n'+check('stage_'+h,'>',0)
            else:available+='\n'+check('stage_'+h,'=',0)+'\n'+P+'route_'+h+' = yes\n'+P+'slot_available = yes\n'+check('max_stage_'+h,'>',1)
            execution=v('stage_'+h,level)
            if key=='resume':execution=f'set_variable = {{ {P}stage_{h} = {P}max_stage_{h} }}'
            execution+='\n'+P+'count_campaigns = yes\nupdate_money_dirty_variable = yes'
            decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('contact_'+h)),b('available',available),'cost = 0',b('complete_effect',b('hidden_effect',guard(available,execution))),f'ai_will_do = {{ factor = {0 if key=="pause" else 1} }}']))
        cat=P+'region_'+h;loc[cat]=d['name']+': The Kurdish Question'
        loc[cat+'_desc']='Regional unrest: §Y[?'+tag+'.'+P+'unrest|0]/100§!.\nDeployment and funded programmes contain unrest and build lasting calm. Political rights support reconciliation, but renewed American escalation can contest the settlement. Consolidation requires 520 qualifying weeks of rights, development and regional security.'
        categories.append(b(cat,['icon = generic_political_discourse','priority = 170','visible_when_empty = yes',f'scripted_gui = {P}region_{h}_gui',b('visible','IMP_is_1970_scenario = yes\n'+tag+' = { '+flag('tracked')+' }\nOR = { tag = USA tag = '+tag+' '+' '.join('tag = '+r for r in rebels)+' }')]))
        did=P+h+'_provoke';loc[did]='Support an armed mobilisation';loc[did+'_desc']='Authorise support for an organised local rising after the regional warning. An existing regional authority must approve its own participation.'
        valid=P+'usa_actor = yes\n'+tag+' = { '+P+'mobilisation_'+h+' = yes\n'+check('qualifying_days','>',29)+'\n'+check('warning_days','>',44)+' }'
        if h=='irq':
            valid+='\nOR = { NOT = { country_exists = KUR } KUR = { '+flag('participate_irq')+' } }'
            pairs=[b('AND',[str(a)+' = { is_owned_and_controlled_by = IRQ is_fully_controlled_by = IRQ }',str(z)+' = { is_owned_and_controlled_by = IRQ is_fully_controlled_by = IRQ }']) for a,z in ((164,633),(164,630),(633,630))]
            valid+='\n'+requirement('irq_territory_tt',b('IRQ',b('OR',pairs)))
        else:valid+='\nNOT = { country_exists = '+d['rebel']+' }'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+tag+' = { '+flag('warning')+' }'),b('available',valid),'cost = 75',b('complete_effect',b('hidden_effect',guard(valid,tag+' = { '+P+'uprising_'+h+' = yes }'))),'ai_will_do = { factor = 1 }']))
    fx[P+'count_campaigns']=v('campaign_count',0)+'\n'+'\n'.join(slot_count)
    fx[P+'regional_streams']='\n'.join(streams)
    fx[P+'regional_weekly']='\n'.join(observers)
    for h,d in HOSTS.items():
        tag=d['tag']
        if h!='irq':fx[P+'uprising_'+h]=birth_effect(h,d)
        else:
            # Existing Iraqi identities are retained. An already existing
            # authority has to approve participation before gaining territory.
            valid='tag = IRQ\n'+P+'mobilisation_irq = yes\n'+check('qualifying_days','>',29)+'\n'+check('warning_days','>',44)
            count='set_temp_variable = { '+P+'held_states = 0 }\n'+'\n'.join(b(str(s),guard('is_owned_and_controlled_by = IRQ is_fully_controlled_by = IRQ',b('IRQ','add_to_temp_variable = { '+P+'held_states = 1 }'))) for s in (164,633,630))
            valid_kur='OR = { NOT = { country_exists = KUR } KUR = { '+flag('participate_irq')+' } }'
            new_kur=guard('NOT = { country_exists = KUR }',setflag('new_kur'))
            transfer='\n'.join(b(str(s),guard('is_owned_and_controlled_by = IRQ is_fully_controlled_by = IRQ','add_core_of = KUR\nKUR = { transfer_state = '+str(s)+' }')) for s in (164,633,630))
            capitals=''
            for i,sid in enumerate((164,633,630)):
                child=b('limit',str(sid)+' = { is_owned_and_controlled_by = KUR }')+'\nset_capital = { state = '+str(sid)+' remember_old_capital = no }\n'+local_column('KUR',sid)
                capitals+=b('if' if i==0 else 'else_if',child)+'\n'
            begin=b('KUR',[setflag('regional_actor'),setflag('cache_offer_irq'),
                guard('IRQ = { '+flag('new_kur')+' }',P+'initialize_new_actor = yes\n'+setflag('recognition_requested')+'\n'+capitals),
                guard('NOT = { has_war_with = IRQ }','declare_war_on = { target = IRQ type = annex_everything }')])
            puk=guard('COLDWAR_USA_gulf_puk_formed = yes\n1078 = { is_owned_and_controlled_by = IRQ is_fully_controlled_by = IRQ }\nOR = { NOT = { country_exists = PUK } PUK = { '+flag('participate_irq')+' } }',
                guard('NOT = { country_exists = PUK }',setflag('new_puk'))+'\n1078 = { add_core_of = PUK }\nPUK = { transfer_state = 1078\n'+guard('IRQ = { '+flag('new_puk')+' }',P+'initialize_new_actor = yes\nset_capital = { state = 1078 remember_old_capital = no }\n'+local_column('PUK',1078))+'\n'+setflag('regional_actor')+'\n'+setflag('cache_offer_irq')+'\n'+guard('NOT = { has_war_with = IRQ }','declare_war_on = { target = IRQ type = annex_everything }')+' }')
            fx[P+'uprising_irq']=guard(valid+'\n'+valid_kur,count+'\n'+guard('check_variable = { '+P+'held_states > 1 }',new_kur+'\n'+transfer+'\n'+begin+'\n'+puk+'\n'+setflag('uprising_occurred')+'\nset_country_flag = COLDWAR_USA_gulf_uprising_fired\n'+v('qualifying_days',0)+'\n'+v('warning_days',0)+f'\nclr_country_flag = {P}warning\nclr_country_flag = {P}new_kur\nclr_country_flag = {P}new_puk'))
        # Finite caches were deducted from the donor's real stockpile by the
        # funding focus or a paid resupply decision. Receiving them never
        # deducts the same equipment a second time.
        for recipient in (['KUR','PUK'] if h=='irq' else [d['rebel']]):
            key=P+h+'_cache_'+recipient.lower();loc[key]='Accept American material assistance';loc[key+'_desc']='Our representatives can accept the equipment already committed to this regional programme.'
            valid=f'tag = {recipient}\ncountry_exists = USA\n{P}funding_{h} = yes\nUSA = {{ {P}payee_clear_{recipient.lower()} = yes {check("cache_"+h,">",0)} {P}route_{h} = yes }}\nany_owned_state = {{ OR = {{ '+' '.join('state = '+str(s) for s in d['states'])+' } is_controlled_by = PREV }'
            preview=P+'cache_preview_'+h+'_'+recipient.lower()+' = yes'
            execute='add_equipment_to_stockpile = { type = infantry_weapons_1 amount = USA.'+P+'cache_'+h+' producer = USA }\n'+setflag('partner_'+h)+'\nUSA = { add_to_variable = { '+P+'delivered_'+h+'_'+recipient.lower()+' = '+P+'cache_'+h+' }\nclear_array = '+P+'payees_'+h+'\nadd_to_array = { array = '+P+'payees_'+h+' value = PREV }\n'+v('cache_'+h,0)+'\n'+P+'reconcile_aid = yes }'
            if h=='irq':execute+='\nset_temp_variable = { treasury_change = USA.'+P+'legacy_irq_cash }\nmodify_treasury_effect = yes\nUSA = { '+v('legacy_irq_cash',0)+' }'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',f'tag = {recipient}\nUSA = {{ {check("cache_"+h,">",0)} }}'),b('available',valid),'cost = 0',b('complete_effect',visible_and_hidden(preview,guard(valid,execute))),'ai_will_do = { factor = 5 }']))
            key=P+h+'_liaison_'+recipient.lower();loc[key]='Accept regional political liaison';loc[key+'_desc']='Permit cooperation with Washington on political contacts and material assistance. Participation in any future uprising remains a separate decision.'
            liaison=f'tag = {recipient}\nUSA = {{ {flag("contact_"+h)} {P}payee_clear_{recipient.lower()} = yes }}'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',liaison+'\n'+noflag('partner_'+h)),'cost = 0',b('complete_effect',b('hidden_effect',guard(liaison,setflag('partner_'+h)))),'ai_will_do = { factor = 1 }']))
            key=P+h+'_end_liaison_'+recipient.lower();loc[key]='End American regional liaison';loc[key+'_desc']='End our participation in the American assistance programme. Equipment already delivered remains ours.'
            end=f'clr_country_flag = {P}partner_{h}\nclr_country_flag = {P}participate_{h}\nUSA = {{ remove_from_array = {{ array = {P}payees_{h} value = PREV }} {P}reconcile_aid = yes }}'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',f'tag = {recipient}\n'+flag('partner_'+h)),'cost = 0',b('complete_effect',b('hidden_effect',guard('tag = '+recipient,end))),'ai_will_do = { factor = 0 }']))
            key=P+h+'_participate_'+recipient.lower();loc[key]='Support a local uprising';loc[key+'_desc']='Agree to receive a local revolt into our regional administration if its organisation and territorial position permit it.'
            valid=f'tag = {recipient}\nNOT = {{ has_war_with = USA }}\nUSA = {{ {flag("contact_"+h)} }}'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',valid+'\n'+noflag('participate_'+h)),'cost = 0',b('complete_effect',b('hidden_effect',guard(valid,setflag('participate_'+h)))),'ai_will_do = { factor = 1 }']))
            key=P+h+'_stand_down_'+recipient.lower();loc[key]='Withdraw uprising participation';loc[key+'_desc']='Withdraw our agreement to receive a future local uprising into our administration. Other assistance arrangements remain separate.'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',f'tag = {recipient}\n'+flag('participate_'+h)),'cost = 0',b('complete_effect',b('hidden_effect',guard('tag = '+recipient,f'clr_country_flag = {P}participate_{h}'))),'ai_will_do = { factor = 0 }']))
            key=P+h+'_request_'+recipient.lower();loc[key]='Request American recognition';loc[key+'_desc']='Ask Washington to recognise the regional authority that our representatives actually administer.'
            valid=f'tag = {recipient}\nNOT = {{ is_subject = yes }}\nNOT = {{ has_war_with = USA }}\nany_owned_state = {{ OR = {{ '+' '.join('state = '+str(s) for s in d['states'])+' } is_controlled_by = PREV }'
            decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',valid+'\n'+noflag('recognition_requested')),'cost = 25',b('complete_effect',b('hidden_effect',guard(valid,setflag('recognition_requested')))),'ai_will_do = { factor = 1 }']))
        key=P+h+'_resupply';loc[key]='Arm Kurdish Underground Cells: '+d['name'];loc[key+'_desc']='Supply clandestine Kurdish cells inside '+d['name']+' from the American stockpile. The operation strengthens local organisation and unrest before statehood. The weapons remain committed to the movement until a cooperating regional authority can accept their delivery.'
        valid=P+'usa_actor = yes\n'+check('stage_'+h,'>',2)+'\n'+P+'route_'+h+' = yes\ncustom_trigger_tooltip = { tooltip = '+P+'equipment_tt has_equipment = { infantry_weapons_1 > 999 } }'
        valid+='\n'+fiscal.affordable('us_resupply_quote')
        local=add('organisation',5)+'\n'+add('unrest',3)+f'\nclamp_variable = {{ var = {P}organisation min = 0 max = 100 }}\nclamp_variable = {{ var = {P}unrest min = 0 max = 100 }}\n'+P+'refresh_host = yes'
        assets='add_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+add('cache_'+h,1000)+'\n'+b(tag,local)
        execution=fiscal.purchase(fiscal.US_SETUP['resupply'],assets)
        shown=fiscal.cost_rows(fiscal.US_SETUP['resupply'])+'\nadd_equipment_to_stockpile = { type = infantry_weapons_1 amount = -1000 }\n'+scalar_row('material',1000)+'\n'+b(tag,scalar_row('organisation',5)+'\n'+scalar_row('unrest',3))
        decisions.append(b(key,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\nhas_completed_focus = '+P+d['front']),b('available',valid),'cost = 25','days_re_enable = 90',b('complete_effect',visible_and_hidden(effect_preview(shown),guard(valid,execution))),'ai_will_do = { factor = 0.5 }']))

def local_column(rebel,target):
    # Every caller is inside a genuinely new-actor branch. Native create_unit
    # can fill the new column despite the zero OOB factor, so clear its generated
    # stores before any recipient-approved shipment is delivered.
    return 'division_template = { name = "Regional Defence Column" is_locked = yes regiments = { Militia_Bat = { x = 0 y = 0 } Militia_Bat = { x = 0 y = 1 } } }\n'+str(target)+' = { create_unit = { division = "division_template = \\\"Regional Defence Column\\\" start_experience_factor = 0.1 start_equipment_factor = 0 start_manpower_factor = 0" owner = '+rebel+' } }\n'+b(rebel,'set_equipment_fraction = 0')

def birth_effect(h,d):
    tag=d['tag'];rebel=d['rebel'];states=d['states']
    if h=='irq':return ''
    # This is an actual local rising after a completed warning, not a focus
    # handing another player's states to the US or to an Iraqi Kurdish tag.
    target=states[0]
    init=f'{P}initialize_new_actor = yes\nset_capital = {{ state = {target} remember_old_capital = no }}\n'+setflag('recognition_requested')
    column=local_column(rebel,target)
    transfer=f'{target} = {{ add_core_of = {rebel} }}\n{rebel} = {{ transfer_state = {target} }}\n{rebel} = {{ {init}\n{column}\nset_country_flag = {P}cache_offer_{h}\ndeclare_war_on = {{ target = {tag} type = annex_everything }} }}'
    valid=f'tag = {tag}\n{P}mobilisation_{h} = yes\n{check("qualifying_days",">",29)}\n{check("warning_days",">",44)}\nNOT = {{ country_exists = {rebel} }}'
    return guard(valid,transfer+'\n'+setflag('uprising_occurred')+'\n'+v('qualifying_days',0)+'\n'+v('warning_days',0)+f'\nclr_country_flag = {P}warning')
