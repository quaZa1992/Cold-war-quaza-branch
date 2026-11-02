# IMPERIA COLD WAR — American triangular strategy and the standing treaty channel.
from .shared import *
from . import fiscal

SNAPSHOT = HERE / 'triangular_approved.json'
SNAPSHOT_SHA = '3f9b9ec75b70ec79b0911c52bb637f848c7c1b5b3493ae7a52b98acf4851c7f2'
assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() == SNAPSHOT_SHA
DESIGN = json.loads(SNAPSHOT.read_text(encoding='utf-8'))
NEW = {n['id']:n for n in DESIGN['nodes'] if not n.get('existing')}
POSITIONS = {'china_exchange':[41,4], 'soviet_exchange':[45,4],
 'china_priority':[41,5], 'soviet_priority':[45,5], 'china_industry':[40,6],
 'china_security':[42,6], 'soviet_trade':[44,6], 'soviet_arms':[46,6],
 'signal_moscow':[41,7], 'wider_settlement':[45,7], 'linkage':[43,8], 'balance':[43,9]}
CAPTIONS = {'wider_settlement':'A Wider Settlement', 'linkage':'Linkage and Restraint', 'balance':'The American Balance'}
ART = {'meeting':'00_politics/Generic_Secret_Meeting', 'exchange':'00_science/scientific_exchange',
 'science':'00_science/research', 'chess':'00_politics/checkmate',
 'concessions':'00_politics/focus_generic_financial_agreement',
 'industry':'00_economy/red_industry', 'secret':'00_security/intelligence_exchange',
 'grain':'00_economy/Wheat_Industry'}
DESCRIPTIONS = {
 'soviet_exchange':'American laboratories and Soviet research institutes can maintain useful contacts even when strategic relations are strained. Scientific exchanges and reciprocal access for civilian investment would give both governments an interest in preserving the opening.',
 'soviet_trade':'Soviet demand for grain gives American exporters a commercial stake in détente. A trade accord can connect dependable civilian supplies with closer economic relations, while credit remains a separate negotiation between the two governments.',
 'soviet_arms':'The strategic arms race absorbs resources and leaves both governments vulnerable to miscalculation. Washington can seek reciprocal limits on nuclear-capable missile reserves and agreed reductions of specified missile stocks, alongside a separate dialogue on strategic defences.'}


def req(loc, name, text, body):
    loc[P+'td_'+name+'_tt'] = text
    return requirement('td_'+name+'_tt',body)


def active_terms(key):
    return {'china_exchange':P+'deal_beijing_active = yes',
      'china_priority':P+'td_exchange_active = yes',
      'soviet_priority':'icwt_programme_1_active = yes',
      'china_industry':P+'td_priority_china_active = yes',
      'china_security':P+'td_priority_china_active = yes',
      'soviet_trade':P+'td_priority_moscow_active = yes',
      'soviet_arms':P+'td_priority_moscow_active = yes',
      'signal_moscow':'OR = { '+P+'td_industry_active = yes '+P+'td_security_active = yes }',
      'wider_settlement':'OR = { icwt_programme_2_active = yes icwt_programme_3_active = yes }',
      'linkage':'OR = { '+flag('td_signal_signed')+' '+flag('td_sov_signal_completed')+' }'}.get(key,'')


def build(loc,fx,tr,ideas,decisions):
    fragments=[];specs={}
    labels={'china_exchange':'An active Beijing Backchannel.',
      'china_priority':'The four-year Chinese trade and production exchange is active.',
      'soviet_priority':'Joint investment cooperation and its signed scientific programme are active.',
      'china_industry':'The Pacific Diplomatic Priority programme is active.',
      'china_security':'The Pacific Diplomatic Priority programme is active.',
      'soviet_trade':'The Priority Détente Programme is active.',
      'soviet_arms':'The Priority Détente Programme is active.',
      'signal_moscow':'An American-Chinese industrial or strategic consultation programme is active.',
      'wider_settlement':'A jointly observed Soviet commercial or SALT programme is active.',
      'linkage':'A joint public statement with China or the Soviet Union has been approved.'}
    for key,node in NEW.items():
        ident=P+key;loc[ident]=CAPTIONS.get(key,node['title']);loc[ident+'_desc']=DESCRIPTIONS.get(key,node['description'])
        requirements=[];shown=[];runtime=[]
        if active_terms(key):requirements.append(req(loc,key,labels[key],active_terms(key)))
        if key in ('soviet_exchange','soviet_trade','soviet_arms','wider_settlement'):
            requirements += ['SOV = { exists = yes NOT = { has_war_with = USA } }']
        if key in ('china_exchange','china_industry','china_security','signal_moscow'):
            requirements += ['CHI = { exists = yes NOT = { has_war_with = USA } }']
        if key in ('china_priority','soviet_priority'):
            route='china' if key=='china_priority' else 'moscow'
            own=node['own'];mods={name:value/100 for name,value in own['mods']}
            idea_key='td_priority_'+route
            ideas.append(idea(idea_key,own['spirit'],'',mods,weekly=True))
            loc[P+idea_key]=own['spirit']
            loc[P+idea_key+'_desc']='Preferential diplomatic commitments depend on continuing cooperation with '+('Beijing.' if route=='china' else 'Moscow.')
            loc[P+idea_key+'_weekly_tt']='Programme balance: §R-0.00002%§! of current US GDP per week (§R-$[?'+P+'td_priority_weekly|5] billion/week§!).'
            runtime += [fiscal.charge(.0005),P+'td_reconcile_priorities = yes']
            shown += [fiscal.cost_rows(.0005),'add_ideas = '+P+idea_key,modifier_rows(mods),fiscal.percentage_row('weekly_gdp',-.00002),
                fiscal.calculate(P+'preview_weekly_amount',-.00002,temporary=True),
                'add_to_variable = { '+P+'preview_weekly = '+P+'preview_weekly_amount tooltip = '+P+'weekly_tt }']
        elif key in ('soviet_exchange','soviet_trade','soviet_arms'):
            slot={'soviet_exchange':9,'soviet_trade':8,'soviet_arms':1}[key]
            shown.append('icwt_focus_preview_'+str(slot)+' = yes')
            runtime.append('icwt_initiative_'+str(slot)+' = yes')
        elif key in ('china_exchange','china_industry','china_security'):
            kind=key.removeprefix('china_')
            shown.append(P+'td_'+kind+'_preview = yes');runtime.append(P+'td_'+kind+'_offer = yes')
        elif key=='signal_moscow':
            shown.append(P+'td_signal_preview = yes');runtime.append(P+'td_signal_offer = yes')
        elif key=='wider_settlement':
            shown.append(P+'td_sov_signal_preview = yes');runtime.append(P+'td_sov_signal_offer = yes')
        elif key=='linkage':
            shown += ['icwt_focus_preview_10 = yes',P+'td_regional_preview = yes',
                'unlock_decision_tooltip = '+P+'td_regional_renew', 'unlock_decision_tooltip = '+P+'td_treaty_regional']
            runtime.append('icwt_initiative_10 = yes')
        elif key=='balance':
            shown += ['unlock_decision_tooltip = '+P+'td_treaty_register',
                'unlock_decision_tooltip = '+P+'td_treaty_economic',
                'unlock_decision_tooltip = '+P+'td_treaty_regional']
            runtime.append('icsd_open = yes')
        tr[P+'ready_'+key]=P+'usa_actor = yes\n'+'\n'.join(requirements)
        fx[P+'execute_'+key]=guard(P+'ready_'+key+' = yes\n'+noflag('done_'+key),
            '\n'.join([setflag('done_'+key),'clr_country_flag = '+P+'pending_'+key,*runtime,'update_money_dirty_variable = yes']))
        fx[P+'complete_'+key]=P+'execute_'+key+' = yes\n'+guard(noflag('done_'+key),setflag('pending_'+key))
        fx[P+'preview_'+key]=effect_preview('\n'.join(shown))
        x,y=POSITIONS[key]
        focus=[f'id = {ident}',f'icon = GFX_goal_{P}td_{node["icon"]}',f'x = {x}',f'y = {y}',f'cost = {node["days"]/7:g}']
        if node.get('parents'):
            groups=[node['parents']] if node.get('parent_mode')=='OR' else [[p] for p in node['parents']]
            focus += [b('prerequisite','\n'.join('focus = '+P+p for p in group)) for group in groups]
        if node.get('exclusive'):focus.append(b('mutually_exclusive','focus = '+P+node['exclusive']))
        focus += [b('available',['hidden_trigger = { '+P+'usa_actor = yes }',*requirements]),
          'cancel_if_invalid = yes','continue_if_invalid = no',
          b('completion_reward',[P+'preview_'+key+' = yes',b('hidden_effect',P+'complete_'+key+' = yes')]),
          'search_filters = { FOCUS_FILTER_POLITICAL FOCUS_FILTER_FOREIGN_POLICY }','ai_will_do = { factor = 1 }']
        fragments.append(b('focus',focus));specs[key]=dict(id=ident,x=x,y=y,requirements=requirements,preview='\n'.join(shown))
        did=P+'enact_'+key;loc[did]='Enact: '+loc[ident];loc[did+'_desc']='Resume the authorised diplomatic initiative when its political conditions are met.'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+flag('pending_'+key)+'\n'+noflag('done_'+key)),b('available',P+'ready_'+key+' = yes'),'cost = 0',b('complete_effect',visible_and_hidden(P+'preview_'+key+' = yes',P+'complete_'+key+' = yes')),'ai_will_do = { factor = 1 }']))
    # The old standalone Moscow channel remains a save-compatible route into
    # the treaty paper. Its old acceptance can never sign new obligations.
    for suffix in ('usa','partner'):
        loc[P+'deal_moscow_'+suffix]='Détente Consultations'
        loc[P+'deal_moscow_'+suffix+'_desc']='The delegations now conduct these consultations through the standing treaty channel.'
        ideas.append(idea('deal_moscow_'+suffix,'','',{'Foreign Influence Defense':.05}))
    fx[P+'deal_moscow_preview']='icwt_focus_preview_7 = yes'
    fx[P+'deal_moscow_offer']='icwt_initiative_7 = yes'
    fx[P+'deal_moscow_accept']='icwt_review_7 = yes'
    fx[P+'deal_moscow_end']=b('USA','clr_country_flag = '+P+'deal_moscow_pending')+'\n'+b('SOV','clr_country_flag = '+P+'deal_moscow_pending')
    tr[P+'deal_moscow_relations']='country_exists = SOV\nNOT = { has_war_with = SOV }'
    tr[P+'deal_moscow_can_offer']=P+'usa_actor = yes\n'+P+'deal_moscow_relations = yes'
    tr[P+'deal_moscow_active']='tag = USA\nUSA = { icwt_member_7 = yes NOT = { has_war_with = SOV } }\nSOV = { exists = yes icwt_member_7 = yes }'
    tr[P+'deal_moscow_accept_valid']='tag = SOV\ncountry_exists = USA\nicwt_pending = yes\ncheck_variable = { global.icwt_pending = 7 }'
    fx[P+'td_migrate_moscow']='\n'.join(b(tag,'\n'.join([
        'remove_ideas = '+P+'deal_moscow_'+suffix,
        'clr_country_flag = '+P+'deal_moscow_signed', 'clr_country_flag = '+P+'deal_moscow_pending'])) for tag,suffix in [('USA','usa'),('SOV','partner')])
    for route,condition in [('china',P+'td_exchange_active = yes'),('moscow','icwt_programme_1_active = yes')]:
        focus='china_priority' if route=='china' else 'soviet_priority'
        tr[P+'td_priority_'+route+'_active']='tag = USA\n'+flag('done_'+focus)+'\n'+condition
    fx[P+'td_reconcile_priorities']=guard(P+'usa_actor = yes',fiscal.calculate(P+'td_priority_weekly',.00002)+'\n'+'\n'.join(
        guard(P+'td_priority_'+route+'_active = yes',guard('NOT = { has_idea = '+P+'td_priority_'+route+' }','add_ideas = '+P+'td_priority_'+route))+'\n'+b('else','remove_ideas = '+P+'td_priority_'+route)
        for route in ('china','moscow')))
    fx[P+'td_strategy_streams']=guard('tag = USA',P+'td_reconcile_priorities = yes\n'+P+'td_sov_signal_quote = yes\n'+'\n'.join(
        guard(P+'td_priority_'+route+'_active = yes','add_to_variable = { '+P+'weekly_expense = '+P+'td_priority_weekly }') for route in ('china','moscow')))
    build_soviet_statement(loc,fx,tr,ideas,decisions)
    for name,title,slot,visible in [
      ('register','Review treaties and commitments',None,flag('done_balance')),
      ('economic','Prepare a Soviet commercial proposal',8,'OR = { '+flag('done_signal_moscow')+' '+flag('done_balance')+' }'),
      ('regional','Prepare a regional stand-down proposal',10,flag('done_linkage'))]:
        did=P+'td_treaty_'+name;loc[did]=title;loc[did+'_desc']='Review the standing commitments and place a new paper before the other delegation. Existing obligations remain subject to their signed terms.'
        action='icsd_open = yes\nset_variable = { icsd_tab = 3 }\nicwt_display = yes' if slot is None else f'icwt_initiative_{slot} = yes'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',P+'usa_actor = yes\n'+visible),b('available','SOV = { exists = yes NOT = { has_war_with = USA } }'),'cost = 0',b('complete_effect',b('hidden_effect',action)),'ai_will_do = { factor = 0 }']))
    return '\n\n'.join(fragments),specs


def build_soviet_statement(loc,fx,tr,ideas,decisions):
    ident=P+'td_sov_signal';pending=flag('td_sov_signal_pending')
    loc[P+'td_sov_signal_spirit']='A Credible Détente Opening'
    loc[P+'td_sov_signal_spirit_desc']='An agreed American-Soviet statement demonstrates the political value of continued negotiations.'
    ideas.append(idea('td_sov_signal_spirit','','',{'Foreign Influence':.03}))
    valid='SOV = { exists = yes NOT = { has_war_with = USA } }\nOR = { icwt_programme_2_active = yes icwt_programme_3_active = yes }'
    tr[ident+'_can_offer']=b('hidden_trigger',P+'usa_actor = yes\n'+flag('done_wider_settlement')+'\n'+noflag('td_sov_signal_pending')+'\n'+noflag('td_sov_signal_completed')+'\n'+noflag('td_sov_signal_cooldown'))+'\n'+req(loc,'sov_statement_programme','A jointly observed commercial or SALT programme is active.',valid)
    invoice=fiscal.calculate(P+'td_statement_quote',.0002)
    fx[ident+'_quote']=invoice
    tr[ident+'_accept_valid']=b('hidden_trigger','tag = SOV\n'+pending+'\nUSA = { '+P+'usa_actor = yes '+pending+' '+noflag('td_sov_signal_completed')+' }')+'\n'+req(loc,'sov_statement_active','A jointly observed commercial or SALT programme is active.','USA = { '+valid+' }')+'\n'+req(loc,'sov_statement_funded','The United States can fund the statement: 0.0002% of current US GDP.','USA = { '+at_least('treasury',P+'td_statement_quote')+' check_variable = { gdp_total > 0 } }')
    preview=b('USA','add_timed_idea = { idea = '+P+'td_sov_signal_spirit days = 180 }\n'+modifier_rows({'Foreign Influence':.03})+'\n'+fiscal.cost_rows(.0002))
    fx[ident+'_preview']=effect_preview('custom_effect_tooltip = '+P+'if_accept_tt\n'+preview)
    fx[ident+'_offer']=guard(ident+'_can_offer = yes',invoice+'\n'+setflag('td_sov_signal_pending')+'\n'+b('SOV',setflag('td_sov_signal_pending')+'\ncountry_event = { id = COLDWAR_USA_TDSP.1 }'))
    clear='\n'.join(b(tag,'clr_country_flag = '+P+'td_sov_signal_pending') for tag in ('USA','SOV'))
    fx[ident+'_accept']='USA = { '+ident+'_quote = yes }\n'+guard(ident+'_accept_valid = yes',b('USA',setflag('td_sov_signal_completed')+'\n'+fiscal.charge(.0002)+'\nadd_timed_idea = { idea = '+P+'td_sov_signal_spirit days = 180 }\nupdate_money_dirty_variable = yes')+'\n'+clear+'\nnews_event = { id = COLDWAR_USA_TDSP.2 }')
    fx[ident+'_end']=guard('OR = { tag = USA tag = SOV }',clear+'\nUSA = { set_country_flag = { flag = '+P+'td_sov_signal_cooldown days = 30 } }')
    for kind,title,visibility,availability,body in [
      ('renew','Propose an American-Soviet joint statement',P+'usa_actor = yes\n'+flag('done_wider_settlement'),ident+'_can_offer = yes',ident+'_offer = yes'),
      ('accept','Approve the American-Soviet statement','tag = SOV\n'+pending,ident+'_accept_valid = yes',ident+'_accept = yes'),
      ('decline','Decline the American-Soviet statement','tag = SOV\n'+pending,'always = yes',ident+'_end = yes'),
      ('cancel','Withdraw the joint statement proposal','tag = USA\n'+pending,'always = yes',ident+'_end = yes')]:
        did=ident+'_'+kind;loc[did]=title;loc[did+'_desc']='Both governments must approve a further public statement on the signed cooperation. The underlying treaty keeps its own agreed terms.'
        decisions.append(b(did,['icon = GFX_decision_generic_political_discourse',b('visible',visibility),b('available',availability),'cost = 0',b('complete_effect',visible_and_hidden(ident+'_preview = yes' if kind in ('renew','accept') else '',body)),'ai_will_do = { factor = '+('0' if kind in ('cancel','decline') else '1')+' }']))


def extra_outputs(loc):
    loc['COLDWAR_USA_TDSP.1.t']='An American-Soviet Joint Statement'
    loc['COLDWAR_USA_TDSP.1.d']='Washington proposes a further public statement on the cooperation already agreed between our governments.'
    loc['COLDWAR_USA_TDSP.1.a']='Approve the statement'
    loc['COLDWAR_USA_TDSP.1.b']='Decline the statement'
    loc['COLDWAR_USA_TDSP.2.t']='Washington and Moscow Announce Further Cooperation'
    loc['COLDWAR_USA_TDSP.2.d']='The United States and Soviet Union have approved a joint statement on their continuing cooperation. The announcement accompanies the agreements negotiated by their delegations.'
    loc['COLDWAR_USA_TDSP.2.a']='A diplomatic opening'
    events=b('country_event',['id = COLDWAR_USA_TDSP.1','title = COLDWAR_USA_TDSP.1.t','desc = COLDWAR_USA_TDSP.1.d','picture = GFX_political_deal','is_triggered_only = yes',b('trigger','tag = SOV\n'+flag('td_sov_signal_pending')),b('option',['name = COLDWAR_USA_TDSP.1.a',b('trigger',P+'td_sov_signal_accept_valid = yes'),visible_and_hidden(P+'td_sov_signal_preview = yes',P+'td_sov_signal_accept = yes'),'ai_chance = { factor = 1 }']),b('option',['name = COLDWAR_USA_TDSP.1.b',b('hidden_effect',P+'td_sov_signal_end = yes'),'ai_chance = { factor = 1 }'])])
    events+='\n'+b('news_event',['id = COLDWAR_USA_TDSP.2','title = COLDWAR_USA_TDSP.2.t','desc = COLDWAR_USA_TDSP.2.d','picture = GFX_icwt_news','major = yes','is_triggered_only = yes',b('option','name = COLDWAR_USA_TDSP.2.a')])
    gfx=[]
    for key,texture in ART.items():
        path='gfx/interface/goals/'+texture+'.dds';assert (ROOT/path).exists()
        for shine in (False,True):
            parts=[f'name = "GFX_goal_{P}td_{key}'+('_shine' if shine else '')+'"',f'texturefile = "{path}"']
            if shine:
                parts.append('effectfile = "gfx/FX/buttonstate.lua"')
                for rotation in (-90,90):parts.append(b('animation',[f'animationmaskfile = "{path}"','animationtexturefile = "gfx/interface/goals/shine_overlay.dds"',f'animationrotation = {rotation}.0','animationlooping = no','animationtime = 0.75','animationdelay = 0','animationblendmode = "add"','animationtype = "scrolling"','animationrotationoffset = { x = 0.0 y = 0.0 }','animationtexturescale = { x = 1.0 y = 1.0 }']))
            gfx.append(b('spriteType',parts))
    return {'events/COLDWAR_USA_triangular_statecraft.txt':MARK+'add_namespace = COLDWAR_USA_TDSP\n'+events+'\n',
      'interface/COLDWAR_USA_triangular.gfx':MARK+b('spriteTypes','\n'.join(gfx))+'\n'}
