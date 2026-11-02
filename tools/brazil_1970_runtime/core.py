# IMPERIA COLD WAR — Brazil 1970 national tree and domestic implementation.
from common import *

def build_core(d):
    loc={};files={};effects=[];triggers=[];ideas=[];focuses=[]
    groups={g['id']:g for g in d['groups']};by={n['key']:n for n in d['nodes']}
    triggers.append(block(P+'campaign','tag = BRA','exists = yes','IMP_is_1970_scenario = yes'))
    loc.update({P+'if_accept_tt':'§YIf they accept:§!',P+'assets_ready_tt':'Own and fully control the named state, with room under its building limit.',P+'assets_ready_tt_NOT':'The required state control or building capacity is missing.',P+'uranium_study_ready_tt':'Control a surveyed uranium deposit with available paid development capacity.',P+'uranium_study_ready_tt_NOT':'No controlled surveyed uranium deposit has development capacity.',P+'decisions':'National Programmes',P+'decisions_desc':'Fund the institutions, studies and service commitments authorised by national policy.'})
    for s in d['starting_spirits']:
        mods=[e['key']+' = '+num(e['value']) for e in s['effects']]
        loc[s['id']]=s['title'];loc[s['id']+'_desc']=s['description']
        ideas.append(block(s['id'],'picture = '+s['id'],'allowed = { original_tag = BRA }','removal_cost = -1',block('modifier',*mods)))

    def policy(effects_list,key,title,group,description=''):
        if any(e['kind']=='modifier' for e in effects_list):
            i=idea_id(key);ideas.append(idea_def(i,title,effects_list,group,loc,description));return i
        return None
    policy_ids={n['key']:policy(n['effects'],n['key'],n['spirit_name'],n['group'],n['description']) for n in d['nodes']}
    modifiers={s['id']:s for s in d['starting_spirits']}

    def preview(effects_list,key,pol=None):
        rows=[]
        if pol:rows.append('add_ideas = '+pol)
        for ix,e in enumerate(effects_list):
            if e['kind']=='modifier':continue
            if e['kind']=='weekly_gdp_expense':rows.append(weekly_preview(e,key+'_'+str(ix),loc))
            elif e['kind']=='event':rows.append('country_event = { id = '+event_ids[e['id']]+' }')
            elif e['kind']=='suspend_agreement':rows.append(P+'preview_termination_'+e['agreement']+' = yes')
            else:rows.append(finite_effect(e,key,ix))
        return '\n'.join(rows)

    # Native event namespace and mutually exclusive response receipts.
    event_ids={e['id']:'COLDWAR_BRA.'+str(i+1) for i,e in enumerate(d['events'])}
    event_nodes={e['id']:n for n in d['nodes'] for e in n['effects'] if e['kind']=='event'}
    events=['add_namespace = COLDWAR_BRA'];event_sync=[]
    event_weekly=[]
    event_map={e['id']:e for e in d['events']}
    for ev in d['events']:
        key=ev['id'].removeprefix(P);eid=event_ids[ev['id']]
        loc[eid+'.t']=ev['title'];loc[eid+'.d']=ev['description']
        node=event_nodes.get(ev['id']);group=node['group'] if node else 'society'
        options=[]
        for ix,o in enumerate(ev['options']):
            op=key+'_option_'+str(ix);oid=idea_id('event_'+op)
            ideas.append(idea_def(oid,o['spirit_name'],o['effects'],group,loc,'The current cabinet settlement and its public commitments.'))
            loc[eid+'.option_'+str(ix)]=o['title']
            poladd=('add_timed_idea = { idea = '+oid+' days = 365 }') if ev['lifetime']=='365 days' else 'add_ideas = '+oid
            option_preview=[]
            # Timed spirit previews show the actual 365-day lifetime through the native effect.
            option_preview.append(poladd)
            if key=='party_reform' and ix==0:option_preview.append('enable_elections_with_no_leader_change = yes')
            if key=='party_reform':option_preview.append(P+'1970_preview_party_reform_'+str(ix)+' = yes')
            if key=='party_split':option_preview += [P+'1970_preview_register_ptb_late = yes',P+'1970_preview_register_pdt = yes']
            for j,e in enumerate(o['effects']):
                if e['kind']=='modifier':continue
                if e['kind']=='weekly_gdp_expense':option_preview.append(weekly_preview(e,'event_'+op,loc))
                elif e['kind']=='suspend_agreement':option_preview.append(P+'preview_termination_'+e['agreement']+' = yes')
                else:option_preview.append(finite_effect(e,'event_'+op,j))
            actual=[setflag('event_chosen_'+key),setflag('event_'+op)]
            actual+=['remove_ideas = '+idea_id('event_'+key+'_option_'+str(j)) for j in range(len(ev['options']))]
            actual.append(poladd)
            for j,e in enumerate(o['effects']):
                if e['kind'] not in ('modifier','weekly_gdp_expense'):actual.append(finite_effect(e,'event_'+op,j))
            if key=='party_reform':
                actual.append(P+'1970_open_party_reform = yes')
                if ix==0:actual += [setflag('1970_democratic_pluralism'),'enable_elections_with_no_leader_change = yes']
                actual.append(P+'open_organisation_stages = yes')
            if key=='party_split':actual += [P+'1970_form_ptb_late = yes',P+'1970_form_pdt = yes']
            optionguard=P+'campaign = yes\n'+once('event_chosen_'+key)
            if any(e['kind']=='treasury_gdp' for e in o['effects']):optionguard+='\ncheck_variable = { gdp_total > 0 }'
            actual.append(P+'sync_programmes = yes')
            helper=P+'event_apply_'+op;effects.append(block(helper,iff(optionguard,*actual)))
            options.append(block('option','name = '+eid+'.option_'+str(ix),block('ai_chance','factor = 1'),block('effect_tooltip',*option_preview),block('hidden_effect',helper+' = yes')))
            if ev['lifetime']=='government':
                active=flag('event_'+op)+'\n'+P+'military_in_power = yes'
                event_sync.extend([iff(active,iff(neg('has_idea = '+oid),'add_ideas = '+oid)),block('else',iff('has_idea = '+oid,'remove_ideas = '+oid))])
            for e in o['effects']:
                if e['kind']=='weekly_gdp_expense':event_weekly.append(('has_idea = '+oid,e))
        events.append(block('country_event','id = '+eid,'title = '+eid+'.t','desc = '+eid+'.d','picture = '+picture_for(eid),'is_triggered_only = yes','fire_only_once = yes',*options))
        effects.append(block(P+'fire_'+key,iff(P+'campaign = yes\n'+once('event_sent_'+key),setflag('event_sent_'+key),'country_event = { id = '+eid+' days = 1 }')))

    # Real prerequisites stay in the runtime transaction, but redundant receipts are hidden in availability.
    def checks(n,transaction=True):
        rows=[P+'campaign = yes']
        if transaction:rows.append(once('earned_'+n['key']))
        if groups[n['group']]['slot'] is not None:rows.append(P+n['group']+'_in_power = yes')
        rows.extend(node_conditions(n))
        if n.get('offer'):rows.append(P+'can_propose_'+n['key']+' = yes')
        if any(e['kind']=='treasury_gdp' for e in n['effects']):rows.append('check_variable = { gdp_total > 0 }')
        for e in n['effects']:
            if e['kind']=='building':rows.append(asset_checks(e))
        if transaction:
            rows.extend(block('OR',*['has_completed_focus = '+by[k]['id'] for k in ps]) for ps in n['prerequisites'])
            rows.extend(neg('has_completed_focus = '+by[k]['id']) for k in n['exclusions'])
        return rows

    sync=[];domestic_weekly=[]
    for n in d['nodes']:
        key=n['key'];g=groups[n['group']];pol=policy_ids[key]
        if pol:
            active=earned(key)+(('\n'+P+n['group']+'_in_power = yes') if g['slot'] is not None else '')
            sync.extend([iff(active,iff(neg('has_idea = '+pol),'add_ideas = '+pol)),block('else',iff('has_idea = '+pol,'remove_ideas = '+pol))])
        for e in n['effects']:
            if e['kind']=='weekly_gdp_expense':
                active=earned(key)+(('\n'+P+n['group']+'_in_power = yes') if g['slot'] is not None else '')
                domestic_weekly.append((active,e))
        nid=n['id'];loc[nid]=n['title'];loc[nid+'_desc']=n['description']
        loc[nid+'_research_0']=n['title'];loc[nid+'_research_1']=n['title'];loc[nid+'_research_2']=n['title']
        coords=n['offset'] if n['anchor'] else [n['x'],n['y']]
        body=['id = '+nid,'icon = COLDWAR_BRA_focus_'+n['icon'],f'x = {coords[0]}',f'y = {coords[1]}']
        if n['anchor']:body.append('relative_position_id = '+n['anchor'])
        body+=['cost = '+num(n['cost']),'cancel_if_invalid = yes','continue_if_invalid = no']
        filters={'society':'FOCUS_FILTER_POLITICAL','economy':'FOCUS_FILTER_INDUSTRY','energy':'FOCUS_FILTER_INDUSTRY FOCUS_FILTER_RESEARCH','defence':'FOCUS_FILTER_ARMY FOCUS_FILTER_RESEARCH','diplomacy':'FOCUS_FILTER_POLITICAL'}.get(n['group'],'FOCUS_FILTER_POLITICAL')
        body.append(block('search_filters',filters))
        for ps in n['prerequisites']:body.append(block('prerequisite',*['focus = '+by[k]['id'] for k in ps]))
        if n['exclusions']:body.append(block('mutually_exclusive',*['focus = '+by[k]['id'] for k in n['exclusions']]))
        visible=[]
        if g['slot'] is not None:
            visible.append(P+n['group']+'_in_power = yes')
        for c in node_conditions(n):visible.append(c)
        if any(e['kind']=='building' for e in n['effects']):
            visible.append(block('custom_trigger_tooltip','tooltip = '+P+'assets_ready_tt',*[asset_checks(e) for e in n['effects'] if e['kind']=='building']))
        if n.get('offer'):visible.append(P+'can_propose_'+key+' = yes')
        hidden=[P+'campaign = yes',once('earned_'+key)]
        if any(e['kind']=='treasury_gdp' for e in n['effects']):hidden.append('check_variable = { gdp_total > 0 }')
        body.append(block('available',block('hidden_trigger',*hidden),*visible))
        actual=[setflag('earned_'+key)]
        for ix,e in enumerate(n['effects']):
            if e['kind'] in ('modifier','weekly_gdp_expense'):continue
            if e['kind']=='event':actual.append(P+'fire_'+e['id'].removeprefix(P)+' = yes')
            elif e['kind']=='unlock_decision':actual.append(setflag('unlock_'+e['id'].removeprefix(P)))
            elif e['kind']=='building':actual.append(construction(e))
            else:actual.append(finite_effect(e,key,ix))
        if n.get('offer'):actual.append(P+'propose_'+key+' = yes')
        actual.append(P+'sync_programmes = yes')
        effects.append(block(P+'complete_'+key,iff('\n'.join(checks(n)),asset_transaction([('BRA',e) for e in n['effects'] if e['kind']=='building'],actual))))
        pre=(P+'offer_preview_'+key+' = yes') if n.get('offer') else preview(n['effects'],key,pol)
        body.append(block('completion_reward',block('effect_tooltip',pre),block('hidden_effect',P+'complete_'+key+' = yes')))
        body.append(block('ai_will_do','factor = 1'))
        focuses.append(block('focus',*body))

    # Two approved domestic decisions, both once-only and paid through native borrowing.
    decisions=[]
    for de in d['decisions']:
        key=de['id'].removeprefix(P);loc[de['id']]=de['title']
        loc[de['id']+'_desc']='Fund the authorised national programme and its technical work.'
        ready=[P+'campaign = yes',flag('unlock_'+key),once('decision_'+key),'check_variable = { gdp_total > 0 }']
        if key=='service_mission':ready.append(P+'military_in_power = yes')
        elif key=='uranium_study':
            ready.append(block('any_owned_state','is_controlled_by = BRA','has_dynamic_modifier = { modifier = imp_uranium_deposit }','has_variable = imp_uranium_per_level','imp_uranium_investment_one_level_available = yes'))
        else:raise ValueError(key)
        effects.append(block(P+'decision_apply_'+key,iff('\n'.join(ready),setflag('decision_'+key),*[finite_effect(e,'decision_'+key,i) for i,e in enumerate(de['effects'])])))
        decisions.append(block(de['id'],'icon = generic_research',block('visible',P+'campaign = yes',flag('unlock_'+key),once('decision_'+key)),block('available',*ready),'cost = 0','days_remove = 1',block('complete_effect',block('effect_tooltip',preview(de['effects'],'decision_'+key)),block('hidden_effect',P+'decision_apply_'+key+' = yes')),block('ai_will_do','factor = 1')))

    effects.append(block(P+'sync_programmes',iff(P+'campaign = yes',*sync,*event_sync)))
    init=[P+'init_politics = yes']
    init.append(iff(once('initialized'),*[ 'add_ideas = '+s['id'] for s in d['starting_spirits']],setflag('initialized')))
    init += [P+'reconcile_politics = yes',P+'sync_programmes = yes',P+'sync_agreements = yes']
    effects.append(block(P+'initialize',iff(P+'campaign = yes',*init)))
    budget=['set_variable = { '+P+'domestic_weekly = 0 }']
    for active,e in domestic_weekly+event_weekly:
        calc='set_temp_variable = { '+P+'stream = { value = gdp_total multiply = '+share(e['annual_gdp_percent'])+' divide = 52 } }\nadd_to_variable = { '+P+'domestic_weekly = '+P+'stream }'
        budget.append(iff(active,calc))
    budget.append('add_to_variable = { additional_expenses_rate = '+P+'domestic_weekly }')
    effects.append(block(P+'add_domestic_weekly_expenses',iff(P+'campaign = yes',*budget)))
    catchup=[iff('has_completed_focus = '+n['id']+'\n'+once('earned_'+n['key']),P+'complete_'+n['key']+' = yes') for n in d['nodes']]
    effects.append(block(P+'reconcile_focus_receipts',iff(P+'campaign = yes',*catchup)))
    # Crisis responses depend on observed native Imperia/MD pressure, not date alone.
    pulses=[iff(once('event_sent_oil_shock')+'\nhas_dynamic_modifier = { modifier = imp_oil_prices_high }',P+'fire_oil_shock = yes'),iff(once('event_sent_debt_crisis')+'\ndate > 1981.12.31\ncheck_variable = { debt_ratio > 0.25 }\ncheck_variable = { interest_rate > 6 }',P+'fire_debt_crisis = yes'),iff(once('event_sent_inflation_settlement')+'\ninflation_rate_higher_than_3 = yes',P+'fire_inflation_settlement = yes'),iff(once('event_sent_us_rights')+'\ndate > 1976.12.31\nhas_idea = '+P+'us_training_BRA',P+'fire_us_rights = yes')]
    effects.append(block(P+'political_pressure_pulse',iff(P+'campaign = yes',*pulses)))
    # A real reform opens registration; it never assigns a government or an outlook.
    stages=[iff(flag('1970_party_reform_open'),setflag('1970_labourist_restoration_open'),setflag('1970_labourist_reorganization_open'),iff(block('OR',flag('1970_democratic_pluralism'),'date > 1984.12.31'),setflag('1970_communist_legalization_open'),iff(flag('1970_party_pds_registered'),setflag('1970_pds_split_authorized'))),iff(block('OR',flag('1970_democratic_pluralism'),'date > 1987.12.31'),iff(flag('1970_party_pmdb_registered'),setflag('1970_pmdb_split_authorized'))),iff('date > 1988.12.31',setflag('1970_prn_formation_open')))]
    # Actual accession is proof that a previously excluded organisation now governs.
    stages += [iff('check_variable = { ruling_party = 3 }\ncheck_variable = { '+P+'1970_party_identity_3 = 0 }','set_variable = { '+P+'1970_party_identity_3 = 1 }',setflag('1970_party_historic_ptb_restored')),iff('check_variable = { ruling_party = 4 }',setflag('1970_pcb_alternative_accession')),iff('check_variable = { ruling_party = 19 }',setflag('1970_pcdob_alternative_accession'))]
    effects.append(block(P+'open_organisation_stages',iff(P+'campaign = yes',*stages)))

    shortcuts=[block('shortcut','name = '+x['focus'],'target = '+x['focus'],'scroll_wheel_factor = 0.8') for x in d['navigation']['shortcuts']]
    tree=block('focus_tree','id = '+TREE,'default = no',block('country','factor = 0',block('modifier','add = 100','tag = BRA','IMP_is_1970_scenario = yes')),'initial_show_position = { x = 4 y = 0 }','continuous_focus_position = { x = 0 y = 2500 }',*shortcuts,*focuses)
    files.update(output('common/national_focus/COLDWAR_BRA_1970_focus.txt',tree))
    files.update(output('common/ideas/COLDWAR_BRA_1970_ideas.txt',block('ideas',block('country',*ideas))))
    files.update(output('common/scripted_effects/COLDWAR_BRA_1970_effects.txt','\n\n'.join(effects)))
    files.update(output('common/scripted_triggers/COLDWAR_BRA_1970_triggers.txt','\n\n'.join(triggers)))
    files.update(output('events/COLDWAR_BRA_1970_events.txt','\n\n'.join(events)))
    files.update(output('common/decisions/categories/COLDWAR_BRA_1970_categories.txt',block(P+'decisions','icon = GFX_decision_category_generic_industry','allowed = { original_tag = BRA }','visible = { '+P+'campaign = yes }')))
    files.update(output('common/decisions/COLDWAR_BRA_1970_decisions.txt',block(P+'decisions',*decisions)))
    return dict(files=files,loc=loc,metadata=dict(policy_ids=policy_ids,event_ids=event_ids))
