# IMPERIA COLD WAR — Recipient-approved Chinese exchanges and regional concessions.
"""Emit paired programmes. UI previews never execute their paid transactions."""
from .shared import P, MARK, ROOT, b, guard, num, flag, setflag, noflag, at_least, effect_preview, visible_and_hidden
from . import fiscal

T = P + 'td_'
NAMESPACE = 'COLDWAR_USA_TD'
MODS = {
    'Foreign Influence': ('foreign_influence_modifier', False),
    'Foreign Influence Defense': ('foreign_influence_defense_modifier', False),
    'Decryption': ('decryption_factor', False), 'Encryption': ('encryption_factor', False),
    'Bureaucracy Cost': ('bureaucracy_cost_multiplier_modifier', True),
    'Consumer Goods Factor': ('consumer_goods_factor', True),
    'Productivity Growth': ('country_productivity_growth_modifier', False),
    'Construction Speed': ('production_speed_buildings_factor', False),
    'Research Speed': ('research_speed_factor', False),
}
DEALS = {
    'exchange': dict(title='Four-Year Trade and Production Exchange', us='Chinese Consumer Imports', them='American Production Exchanges',
        us_mods={'Consumer Goods Factor': -.03, 'Bureaucracy Cost': .01}, them_mods={'Productivity Growth': .1, 'Bureaucracy Cost': .01},
        setup=.0003, us_week=.00002, china_week=.0002, focus='china_exchange', days=1460,
        desc='Washington proposes four years of trade and production exchanges. American access to Chinese consumer goods and Chinese access to production expertise give both governments a stake in the opening.'),
    'industry': dict(title='Priority Industrial Mission', us='China Industrial Mission', them='American Civilian Technical Mission',
        us_mods={'Foreign Influence': .05}, them_mods={'Construction Speed': .05, 'Research Speed': .03, 'Bureaucracy Cost': .01, 'Foreign Influence Defense': -.03},
        setup=.001, us_week=.00005, transfer=True, focus='china_industry',
        desc='An American-financed civilian technical mission would support Chinese industrial development. Beijing retains responsibility for the mission and may end its participation.'),
    'security': dict(title='Sino-American Strategic Consultations', us='Sino-American Strategic Consultations', them='Sino-American Strategic Consultations',
        us_mods={'Decryption': .05, 'Foreign Influence': .03, 'Bureaucracy Cost': .01}, them_mods={'Encryption': .05, 'Foreign Influence Defense': .05, 'Bureaucracy Cost': .01},
        setup=.0005, us_week=.00004, china_week=.0004, focus='china_security',
        desc='Regular strategic consultations would allow Washington and Beijing to exchange assessments of regional pressure. Each government remains responsible for its own foreign policy.'),
    'regional': dict(title='Chinese Regional Restraint Package', us='Negotiated Regional Understanding', them='American Economic Cooperation Programme',
        us_mods={'Foreign Influence': .05}, them_mods={'Construction Speed': .05, 'Research Speed': .02, 'Bureaucracy Cost': .01},
        setup=.0005, us_week=.00005, transfer=True, focus='linkage',
        desc='Economic cooperation is offered for the withdrawal of Chinese military missions from an agreed recipient. Beijing names the recipient, Washington approves that choice, and both governments review the resulting commitment.'),
}


def fv(name): return T + name
def cf(name): return 'has_country_flag = ' + T + name
def nf(name): return 'NOT = { ' + cf(name) + ' }'
def sf(name): return 'set_country_flag = ' + T + name
def eq(left, right): return 'check_variable = { ' + left + ' = ' + right + ' }'
def rows(mods):
    return '\n'.join('add_to_variable = { '+T+'preview_'+MODS[label][0]+' = '+num(value)+' tooltip = '+T+'mod_'+MODS[label][0]+'_tt }' for label,value in mods.items())


def relations():
    own=' '.join('is_in_array = { array = imp_'+kind+'_sanc_'+direction+'_us value = CHI }' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    other=' '.join('is_in_array = { array = imp_'+kind+'_sanc_'+direction+'_us value = USA }' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    return 'country_exists = USA\ncountry_exists = CHI\nUSA = { NOT = { has_war_with = CHI } NOT = { is_embargoing = CHI } NOT = { OR = { '+own+' } } }\nCHI = { NOT = { has_war_with = USA } NOT = { is_embargoing = USA } NOT = { OR = { '+other+' } } }'


def parent(key):
    if key in ('industry','security'):
        return 'USA = { '+flag('done_china_priority')+' '+T+'exchange_active = yes }'
    return 'USA = { '+P+'deal_beijing_active = yes }'


def quote(key): return T + key + '_setup_quote'
def spirit(key,side): return 'icwt_programme_4_usa' if key=='regional' and side=='usa' else T+key+'_'+side
def tooltip(name,condition): return b('custom_trigger_tooltip',['tooltip = '+T+name,condition])
def funded(variable):
    return b('USA',tooltip('funding_tt','check_variable = { gdp_total > 0 }\ncheck_variable = { '+variable+' > 0 }\n'+at_least('treasury',variable)))


def weekly_preview(rate, donor=False, sign=-1):
    return fiscal.percentage_row('weekly_usa_gdp' if donor else 'weekly_gdp', rate*sign)+'\n'+fiscal.calculate(T+'preview_weekly_amount', rate*sign, 'USA.gdp_total' if donor else 'gdp_total', True)+'\nadd_to_variable = { '+T+'preview_weekly = '+T+'preview_weekly_amount tooltip = '+P+'weekly_tt }'


def preview(key):
    d=DEALS[key];ident=T+key
    us_spirit='add_timed_idea = { idea = '+spirit(key,'usa')+' days = '+str(d['days'])+' }' if d.get('days') else 'add_ideas = '+spirit(key,'usa')
    chi_spirit='add_timed_idea = { idea = '+ident+'_china days = '+str(d['days'])+' }' if d.get('days') else 'add_ideas = '+ident+'_china'
    us=us_spirit+'\n'+rows(d['us_mods'])+'\n'+fiscal.cost_rows(d['setup'])+'\n'+weekly_preview(d['us_week'])
    chi=chi_spirit+'\n'+rows(d['them_mods'])
    if d.get('transfer'): chi+='\n'+weekly_preview(d['us_week'],True,1)
    if d.get('china_week'): chi+='\n'+weekly_preview(d['china_week'])
    if key=='regional':
        # The concrete recipient is chosen before either government approves it.
        chi+='\nif = { limit = { check_variable = { USA.'+T+'regional_target > 0 } var:USA.'+T+'regional_target = { exists = yes } } recall_attache = var:USA.'+T+'regional_target }'
        chi+='\ncustom_effect_tooltip = '+T+'volunteer_cost_condition_tt\nadd_political_power = -50\nadd_command_power = -15'
        chi+='\nif = { limit = { check_variable = { USA.'+T+'regional_target > 0 } var:USA.'+T+'regional_target = { exists = yes } } recall_volunteers_from = var:USA.'+T+'regional_target }'
    return effect_preview('custom_effect_tooltip = '+P+'if_accept_tt\nUSA = { '+us+' }\nCHI = { '+chi+' }')


def decision(loc, decisions, ident, title, visible, available, reward, desc, ai=0, extra=''):
    loc[ident]=title;loc[ident+'_desc']=desc
    decisions.append(b(ident,['icon = GFX_decision_generic_political_discourse',b('visible',visible),b('available',available),'cost = 0',extra,b('complete_effect',reward),'ai_will_do = { factor = '+str(ai)+' }']))


def build(loc, fx, tr, ideas, decisions):
    for label,(token,cost) in MODS.items():loc[T+'mod_'+token+'_tt']=label+': $RIGHT|'+('-=' if cost else '+=')+'%1$'
    loc[T+'volunteer_cost_condition_tt']='If Chinese volunteers are deployed to the agreed recipient:'
    loc[T+'regional_target_tt']='Agreed mission recipient: [?USA.'+T+'regional_target.GetName]'
    loc[T+'current_review_tt']='The Chinese delegation has reviewed the current proposal.'
    loc[T+'regional_approved_tt']='Washington has approved the named Chinese mission recipient.'
    loc[T+'recall_permission_tt']='Volunteer recall is permitted and China has 50 Political Power and 15 Command Power if volunteers are deployed.'
    loc[T+'funding_tt']='Sufficient American treasury for the current GDP-based programme cost.'
    loc[T+'relations_tt']='China and the United States exist, remain at peace and impose no bilateral embargo or diplomatic, financial, economic or military sanctions.'
    loc[T+'regional_target_valid_tt']='The agreed mission recipient exists and has Chinese military missions to withdraw.'
    tr[T+'relations']=relations()
    refresh=[];reconcile=[];streams=[]
    for index,(key,d) in enumerate(DEALS.items(),1):
        ident=T+key
        for side,label,mods in (('usa',d['us'],d['us_mods']),('china',d['them'],d['them_mods'])):
            idea_id=spirit(key,side)
            if key=='regional' and side=='usa':continue
            loc[idea_id]=label
            description=d['desc']
            if d.get('days'):description+=' The agreed term is four years from acceptance, including any period in which cooperation is suspended.'
            rate=d['us_week'] if side=='usa' or d.get('transfer') else d['china_week']
            positive=side=='china' and d.get('transfer')
            description+=' Programme balance: '+('+' if positive else '-')+num(rate)+'% of '+('US GDP' if side=='usa' or d.get('transfer') else 'Chinese GDP')+' per week.'
            loc[idea_id+'_desc']=description
            ideas.append(b(idea_id,['picture = COLDWAR_USA_KS_consultations','allowed = { always = no }','allowed_civil_war = { always = no }',b('modifier','\n'.join(MODS[k][0]+' = '+num(v) for k,v in mods.items()))]))
        refresh.append(fiscal.calculate(quote(key),d['setup']))
        tr[ident+'_parent']=parent(key)
        loc[ident+'_parent_tt']='An active four-year Chinese exchange and the Pacific Diplomatic Priority programme.' if key in ('industry','security') else 'An active Beijing Backchannel.'
        parent_requirement=b('custom_trigger_tooltip',['tooltip = '+ident+'_parent_tt',ident+'_parent = yes'])
        relations_requirement=tooltip('relations_tt',T+'relations = yes')
        common='tag = USA\nIMP_is_1970_scenario = yes\n'+T+'relations = yes\n'+ident+'_parent = yes'
        active=common+'\n'+cf(key+'_signed')
        if d.get('days'):
            active+='\ncheck_variable = { var = '+T+key+'_end value = global.num_days compare = greater_than }'
        if key=='regional':
            active+='\ncheck_variable = { '+T+'regional_target > 0 }\nvar:'+T+'regional_target = { exists = yes NOT = { has_attache_from = CHI } NOT = { has_volunteers_amount_from = { tag = CHI count > 0 } } }'
        tr[ident+'_active']=active
        tr[ident+'_can_offer']=b('hidden_trigger','tag = USA\nIMP_is_1970_scenario = yes\n'+flag('done_'+d['focus'])+'\n'+nf(key+'_signed')+'\n'+nf(key+'_pending')+'\n'+nf(key+'_cooldown'))+'\n'+relations_requirement+'\n'+parent_requirement
        review='custom_trigger_tooltip = { tooltip = '+T+'current_review_tt '+eq(ident+'_review_revision','USA.'+ident+'_revision')+' check_variable = { '+ident+'_review_revision > 0 } }'
        accept=b('hidden_trigger','tag = CHI\ncountry_exists = USA\n'+cf(key+'_pending')+'\nUSA = { '+cf(key+'_pending')+' '+nf(key+'_signed')+' }')+'\n'+relations_requirement+'\n'+parent_requirement+'\n'+review+'\n'+funded(quote(key))
        if key=='regional':
            accept+='\ncustom_trigger_tooltip = { tooltip = '+T+'regional_approved_tt USA = { '+eq(ident+'_approved_revision',ident+'_revision')+' check_variable = { '+ident+'_approved_revision > 0 } } }'
            accept+='\n'+tooltip('regional_target_valid_tt','check_variable = { USA.'+T+'regional_target > 0 }\nvar:USA.'+T+'regional_target = { exists = yes OR = { has_attache_from = CHI has_volunteers_amount_from = { tag = CHI count > 0 } } }')
            accept+='\ncustom_trigger_tooltip = { tooltip = '+T+'recall_permission_tt OR = { var:USA.'+T+'regional_target = { NOT = { has_volunteers_amount_from = { tag = CHI count > 0 } } } AND = { has_game_rule = { rule = allow_recall_intervention_forces option = yes } has_political_power > 49 command_power > 14 } } }'
        tr[ident+'_accept_valid']=accept
        fx[ident+'_preview']=preview(key)
        prepared=sf(key+'_authorised')+'\n'+sf(key+'_pending')+'\nadd_to_variable = { '+ident+'_revision = 1 }\n'+T+'refresh_quotes = yes\nCHI = { '+sf(key+'_pending')+' clear_variable = '+ident+'_review_revision country_event = { id = '+NAMESPACE+'.'+str(index)+' } }'
        if key=='regional':prepared+='\nclear_variable = '+T+'regional_target\nclear_variable = '+ident+'_approved_revision'
        fx[ident+'_offer']=guard(ident+'_can_offer = yes',prepared)
        fx[ident+'_review']=guard('tag = CHI\n'+cf(key+'_pending')+'\nUSA = { '+cf(key+'_pending')+' }','set_variable = { '+ident+'_review_revision = USA.'+ident+'_revision }')
        accepted='USA = { '+fiscal.charge(d['setup'])+' '+sf(key+'_signed')+' clr_country_flag = '+ident+'_pending }\n'+sf(key+'_signed')+'\nclr_country_flag = '+ident+'_pending'
        if d.get('days'):
            accepted+='\nUSA = { set_variable = { '+ident+'_end = global.num_days } add_to_variable = { '+ident+'_end = '+str(d['days'])+' } country_event = { id = '+NAMESPACE+'.11 days = '+str(d['days'])+' } }'
        if key=='regional':
            accepted+='\nrecall_attache = var:USA.'+T+'regional_target\n'+guard('var:USA.'+T+'regional_target = { has_volunteers_amount_from = { tag = CHI count > 0 } }','add_political_power = -50\nadd_command_power = -15\nrecall_volunteers_from = var:USA.'+T+'regional_target')
        accepted+='\nUSA = { '+T+'reconcile = yes }\nUSA = { update_money_dirty_variable = yes }\nupdate_money_dirty_variable = yes'
        funding='USA = { check_variable = { gdp_total > 0 } check_variable = { '+quote(key)+' > 0 } '+at_least('treasury',quote(key))+' }'
        fx[ident+'_accept']='USA = { '+T+'refresh_quotes = yes }\n'+guard(ident+'_accept_valid = yes\n'+funding,accepted)
        removal=guard('icwt_programme_4_active = no','remove_ideas = '+spirit(key,'usa')) if key=='regional' else 'remove_ideas = '+spirit(key,'usa')
        ended='USA = { clr_country_flag = '+ident+'_signed clr_country_flag = '+ident+'_pending set_country_flag = { flag = '+ident+'_cooldown days = 60 value = 1 } '+removal+' update_money_dirty_variable = yes }\nCHI = { clr_country_flag = '+ident+'_signed clr_country_flag = '+ident+'_pending clear_variable = '+ident+'_review_revision remove_ideas = '+ident+'_china update_money_dirty_variable = yes }'
        fx[ident+'_end']=guard('OR = { tag = USA tag = CHI }',ended)
        if d.get('days'):
            reconcile.append(guard(cf(key+'_signed')+'\ncheck_variable = { var = global.num_days value = '+ident+'_end compare = greater_than_or_equals }',ident+'_end = yes'))
        ensure=guard('NOT = { has_idea = '+spirit(key,'usa')+' }','add_ideas = '+spirit(key,'usa'))+'\nCHI = { '+guard('NOT = { has_idea = '+ident+'_china }','add_ideas = '+ident+'_china')+' }'
        remove=removal+'\nCHI = { remove_ideas = '+ident+'_china }'
        reconcile.append(guard(ident+'_active = yes',ensure)+'\n'+b('else',remove))
        usamount=fiscal.calculate(T+'weekly_amount',d['us_week'],'gdp_total',True)
        streams.append(guard('tag = USA\n'+ident+'_active = yes',usamount+'\nadd_to_variable = { '+P+'weekly_expense = '+T+'weekly_amount }'))
        if d.get('transfer'):
            streams.append(guard('tag = CHI\nUSA = { '+ident+'_active = yes }',fiscal.calculate(T+'weekly_amount',d['us_week'],'USA.gdp_total',True)+'\nadd_to_variable = { '+P+'weekly_income = '+T+'weekly_amount }'))
        if d.get('china_week'):
            streams.append(guard('tag = CHI\nUSA = { '+ident+'_active = yes }',fiscal.calculate(T+'weekly_amount',d['china_week'],'gdp_total',True)+'\nadd_to_variable = { '+P+'weekly_expense = '+T+'weekly_amount }'))
        vis='tag = CHI\n'+cf(key+'_pending')
        decision(loc,decisions,ident+'_review_decision','Review: '+d['title'],vis,'always = yes',visible_and_hidden(preview(key),ident+'_review = yes'),d['desc'],1)
        decision(loc,decisions,ident+'_accept_decision','Accept: '+d['title'],vis,ident+'_accept_valid = yes',visible_and_hidden(preview(key),ident+'_accept = yes'),d['desc'],1)
        decision(loc,decisions,ident+'_decline_decision','Decline: '+d['title'],vis,'always = yes',b('hidden_effect',ident+'_end = yes'),'Decline the proposed commitments.')
        decision(loc,decisions,ident+'_renew','Propose: '+d['title'],'tag = USA\n'+flag('done_'+d['focus']),ident+'_can_offer = yes',visible_and_hidden(preview(key),ident+'_offer = yes'),d['desc'],.1)
        decision(loc,decisions,ident+'_withdraw','End: '+d['title'],'OR = { tag = USA tag = CHI }\nUSA = { '+cf(key+'_signed')+' }','always = yes',visible_and_hidden(effect_preview('USA = { '+removal+' }\nCHI = { remove_ideas = '+ident+'_china }'),ident+'_end = yes'),'End our participation in the programme.')
        decision(loc,decisions,ident+'_cancel','Withdraw proposal: '+d['title'],'tag = USA\n'+cf(key+'_pending'),'always = yes',b('hidden_effect',ident+'_end = yes'),'Withdraw the unsigned paper.')
    fx[T+'refresh_quotes']='\n'.join(refresh+[fiscal.calculate(T+'signal_quote',.0002)])
    fx[T+'exchange_expire']=guard('tag = USA\n'+cf('exchange_signed')+'\ncheck_variable = { var = global.num_days value = '+T+'exchange_end compare = greater_than_or_equals }',T+'exchange_end = yes')
    fx[T+'reconcile']=guard('tag = USA\nIMP_is_1970_scenario = yes',T+'refresh_quotes = yes\n'+'\n'.join(reconcile))
    # A dead named country scope does not execute native effects. The surviving
    # Chinese partner must therefore clear its own benefits locally. Keep the
    # signed record and absolute exchange deadline for possible restoration.
    fx[T+'missing_usa_cleanup']=guard('tag = CHI\nNOT = { country_exists = USA }','\n'.join('remove_ideas = '+T+key+'_china' for key in DEALS))
    fx[T+'streams']=guard('OR = { tag = USA tag = CHI }',T+'missing_usa_cleanup = yes\nif = { limit = { country_exists = USA } USA = { '+T+'reconcile = yes } }\n'+'\n'.join(streams))
    regional(loc,fx,tr,decisions)
    signalling(loc,fx,tr,ideas,decisions)


def regional(loc,fx,tr,decisions):
    ident=T+'regional'
    valid='tag = CHI\n'+cf('regional_pending')+'\nUSA = { '+cf('regional_pending')+' '+nf('regional_signed')+' '+T+'relations = yes '+ident+'_parent = yes }'
    target='FROM = { exists = yes NOT = { tag = CHI } NOT = { tag = USA } OR = { has_attache_from = ROOT has_volunteers_amount_from = { tag = ROOT count > 0 } } }'
    loc[ident+'_select']='Propose mission withdrawal from [FROM.GetName]'
    loc[ident+'_select_desc']='Name the recipient of Chinese military missions to be withdrawn. Washington must approve this recipient before the complete agreement can be accepted.'
    choose='USA = { set_variable = { '+ident+'_target = FROM.id } add_to_variable = { '+ident+'_revision = 1 } clear_variable = '+ident+'_approved_revision country_event = { id = '+NAMESPACE+'.10 } }\nclear_variable = '+ident+'_review_revision'
    decisions.append(b(ident+'_select',['icon = GFX_decision_generic_political_discourse',b('target_root_trigger',valid),b('target_trigger',target),'cost = 0',b('complete_effect',b('hidden_effect',guard(valid+'\n'+target,choose))),'ai_will_do = { factor = 0.1 }']))
    tr[ident+'_approve_valid']=b('hidden_trigger','tag = USA\n'+cf('regional_pending'))+'\n'+tooltip('regional_target_valid_tt','check_variable = { '+ident+'_target > 0 }\nvar:'+ident+'_target = { exists = yes OR = { has_attache_from = CHI has_volunteers_amount_from = { tag = CHI count > 0 } } }')+'\n'+tooltip('relations_tt',T+'relations = yes')+'\n'+b('custom_trigger_tooltip',['tooltip = '+ident+'_parent_tt',ident+'_parent = yes'])
    fx[ident+'_approve']=guard(ident+'_approve_valid = yes','set_variable = { '+ident+'_approved_revision = '+ident+'_revision }\nCHI = { clear_variable = '+ident+'_review_revision country_event = { id = '+NAMESPACE+'.4 } }')
    decision(loc,decisions,ident+'_approve_decision','Approve the named Chinese withdrawal','tag = USA\n'+cf('regional_pending')+'\ncheck_variable = { '+ident+'_target > 0 }',ident+'_approve_valid = yes',visible_and_hidden(preview('regional'),ident+'_approve = yes'),'China proposes withdrawing its military missions from [?'+ident+'_target.GetName]. Approve this recipient before Beijing reviews the final paper.')


def signalling(loc,fx,tr,ideas,decisions):
    ident=T+'signal'
    loc[T+'signal_partner_tt']='An American-Chinese industrial or strategic consultation programme is active.'
    gate=tooltip('relations_tt',T+'relations = yes')+'\n'+tooltip('signal_partner_tt','USA = { OR = { '+T+'industry_active = yes '+T+'security_active = yes } }')
    tr[ident+'_can_offer']=b('hidden_trigger','tag = USA\nIMP_is_1970_scenario = yes\n'+flag('done_signal_moscow')+'\n'+nf('signal_pending')+'\n'+nf('signal_signed'))+'\n'+gate
    tr[ident+'_accept_valid']=b('hidden_trigger','tag = CHI\n'+cf('signal_pending')+'\nUSA = { '+cf('signal_pending')+' '+nf('signal_signed')+' }')+'\n'+gate+'\n'+funded(T+'signal_quote')
    loc[ident+'_usa']='A Credible Pacific Opening';loc[ident+'_usa_desc']='A jointly approved public statement demonstrates that the American opening to China has produced a substantive agreement.'
    ideas.append(b(ident+'_usa',['picture = COLDWAR_USA_KS_consultations','allowed = { always = no }','allowed_civil_war = { always = no }',b('modifier','foreign_influence_modifier = 0.03')]))
    fx[ident+'_preview']=effect_preview('custom_effect_tooltip = '+P+'if_accept_tt\nUSA = { add_timed_idea = { idea = '+ident+'_usa days = 180 }\n'+rows({'Foreign Influence':.03})+'\n'+fiscal.cost_rows(.0002)+' }')
    fx[ident+'_offer']=guard(ident+'_can_offer = yes',T+'refresh_quotes = yes\n'+sf('signal_pending')+'\nCHI = { '+sf('signal_pending')+' country_event = { id = '+NAMESPACE+'.5 } }')
    invoice=fiscal.calculate(T+'signal_quote',.0002,'gdp_total')
    fx[ident+'_accept']='USA = { '+invoice+' }\n'+guard(ident+'_accept_valid = yes\nUSA = { check_variable = { '+T+'signal_quote > 0 } '+at_least('treasury',T+'signal_quote')+' }','USA = { '+sf('signal_signed')+' clr_country_flag = '+ident+'_pending '+fiscal.charge(.0002)+' add_timed_idea = { idea = '+ident+'_usa days = 180 } news_event = { id = '+NAMESPACE+'.101 } }\n'+sf('signal_signed')+'\nclr_country_flag = '+ident+'_pending')
    fx[ident+'_end']='USA = { clr_country_flag = '+ident+'_pending }\nCHI = { clr_country_flag = '+ident+'_pending }'
    decision(loc,decisions,ident+'_accept_decision','Approve the joint Sino-American statement','tag = CHI\n'+cf('signal_pending'),ident+'_accept_valid = yes',visible_and_hidden(ident+'_preview = yes',ident+'_accept = yes'),'Approve publication of the agreed civilian or strategic cooperation and the American invitation to further negotiations.',1)
    decision(loc,decisions,ident+'_decline_decision','Decline the joint statement','tag = CHI\n'+cf('signal_pending'),'always = yes',b('hidden_effect',ident+'_end = yes'),'Keep the standing cooperation separate from the proposed public statement.')
    decision(loc,decisions,ident+'_renew','Request a joint Sino-American statement','tag = USA\n'+flag('done_signal_moscow'),ident+'_can_offer = yes',visible_and_hidden(ident+'_preview = yes',ident+'_offer = yes'),'Request Chinese approval for the public statement.',.1)


def extra_outputs(loc):
    events=[]
    def event(eid,title,desc,options):
        key=NAMESPACE+'.'+str(eid);loc[key+'.t']=title;loc[key+'.d']=desc
        body=['id = '+key,'title = '+key+'.t','desc = '+key+'.d','picture = GFX_political_deal','is_triggered_only = yes']
        for index,(label,effect) in enumerate(options):
            name=key+'.'+str(index);loc[name]=label;body.append(b('option',['name = '+name,effect]))
        events.append(b('country_event',body))
    for index,(key,d) in enumerate(DEALS.items(),1):
        event(index,d['title'],d['desc'],[('Review the complete proposal',visible_and_hidden(preview(key),T+key+'_review = yes')),('Leave the proposal for the delegation','')])
    event(5,'A Joint Sino-American Statement','Washington requests Chinese approval to announce the public scope of the agreed cooperation and invite further negotiations.',[('Review the proposed statement',T+'signal_preview = yes'),('Consult the delegation','')])
    event(10,'A Chinese Regional Counterproposal','Beijing proposes withdrawing its military missions from [?'+T+'regional_target.GetName]. Washington must decide whether that recipient satisfies the proposed regional bargain.',[('Review the named recipient',preview('regional')),('Consult the delegation','')])
    events.append(b('country_event',['id = '+NAMESPACE+'.11','hidden = yes','is_triggered_only = yes',b('immediate',T+'exchange_expire = yes')]))
    loc[NAMESPACE+'.101.t']='Washington and Beijing Announce Cooperation'
    loc[NAMESPACE+'.101.d']='The United States and China have jointly announced a substantive cooperation programme. Washington has invited further negotiations while both governments retain their own diplomatic commitments.'
    loc[NAMESPACE+'.101.a']='A significant diplomatic opening.'
    events.append(b('news_event',['id = '+NAMESPACE+'.101','title = '+NAMESPACE+'.101.t','desc = '+NAMESPACE+'.101.d','picture = GFX_icwt_news','is_triggered_only = yes','major = yes',b('option','name = '+NAMESPACE+'.101.a')]))
    return {'events/COLDWAR_USA_triangular.txt':MARK+'add_namespace = '+NAMESPACE+'\n'+'\n'.join(events)+'\n'}
