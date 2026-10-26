# IMPERIA CW — Cold War: iraq 1970 — decisions module.
"""COLDWAR Iraq: approved decision providers. Pure generator, no runtime writes.

Public IRQ helpers: begin_kurdish_negotiations, decision_tick,
apply_decision_leader_choices. CONTRACTS supplies the focus compiler's actual
agreement predicates. All political offers keep MD's ruling_party authoritative.
"""
from pathlib import Path
import json,re
from common import P, ROOT, PARTIES, GROUP_SLOTS, block, locline, group_gate, invoice, pay_var, check, parse, emit, first

CONTRACTS = {
 'Accepted and maintained legalization':'has_country_flag = COLDWAR_IRQ_legalization_accepted',
 'Accepted autonomy contract':'has_country_flag = COLDWAR_IRQ_autonomy_accepted COLDWAR_IRQ_northern_settlement_active = yes',
 'Active autonomy guarantees':'COLDWAR_IRQ_northern_settlement_active = yes',
 'Northern guarantees fulfilled':'COLDWAR_IRQ_northern_settlement_active = yes',
 'Accepted federal contract':'has_country_flag = COLDWAR_IRQ_federal_settlement COLDWAR_IRQ_northern_settlement_active = yes',
 'Accepted federal revenue settlement':'has_country_flag = COLDWAR_IRQ_federal_settlement COLDWAR_IRQ_northern_settlement_active = yes',
 'Accepted front charter':'has_country_flag = COLDWAR_IRQ_front_accepted has_country_flag = COLDWAR_IRQ_legalization_accepted OR = { AND = { check_variable = { ruling_party = 21 } is_in_array = { array = gov_coalition_array value = 4 } } AND = { check_variable = { ruling_party = 4 } is_in_array = { array = gov_coalition_array value = 21 } } }',
 'Accepted transition charter':'has_country_flag = COLDWAR_IRQ_transition_accepted',
 'Accepted Syrian conference; charter consent':'has_country_flag = COLDWAR_IRQ_syria_charter_accepted country_exists = SYR NOT = { has_war_with = SYR } SYR = { has_country_flag = COLDWAR_IRQ_syria_charter_partner }',
 'Accepted development or convention agreement':'has_country_flag = COLDWAR_IRQ_arab_compact_accepted OR = { AND = { country_exists = EGY NOT = { has_war_with = EGY } OR = { has_country_flag = COLDWAR_IRQ_accepted_arab_development_offer_EGY has_country_flag = COLDWAR_IRQ_accepted_arab_union_offer_EGY } } AND = { country_exists = SYR NOT = { has_war_with = SYR } OR = { has_country_flag = COLDWAR_IRQ_accepted_arab_development_offer_SYR has_country_flag = COLDWAR_IRQ_accepted_arab_union_offer_SYR } } }',
 'Accepted KDP-PUK cooperation pact':'has_country_flag = COLDWAR_IRQ_kdp_puk_pact has_country_flag = COLDWAR_IRQ_puk_formed NOT = { has_war_with = KUR } NOT = { has_war_with = PUK }',
 'Accepted Kirkuk or federal revenue agreement':'COLDWAR_IRQ_northern_settlement_active = yes OR = { AND = { has_country_flag = COLDWAR_IRQ_kirkuk_revenue_accepted 165 = { is_owned_and_controlled_by = IRQ } } has_country_flag = COLDWAR_IRQ_federal_settlement }',
 'Accepted revised oil concession':'COLDWAR_IRQ_oil_concession_active = yes',
 'Accepted and fulfilled Iran border/navigation settlement':'COLDWAR_IRQ_border_settlement_active = yes',
}

# Constitutional authority is one current contract, not a lifetime ban on other
# parties. Permanent earned packages survive and resume under compatible terms.
CONSTITUTION_CHOICES = {
 'state': ('executive_state', 'civic_compact'),
 'communists': ('icp_vanguard', 'icp_democratic_front'),
 'officers': ('officer_permanent', 'officer_caretaker'),
 'monarchy': ('royal_executive', 'royal_ceremonial'),
 'dawa': ('dawa_directorial', 'dawa_constitutional'),
 'sciri': ('sciri_clerical_executive', 'sciri_iraqi_charter'),
 'sunni': ('iip_directorial', 'iip_parliamentary'),
}
POLICY_CONTRACT_GATES = {
 P + key: P + 'constitution_' + kind + '_active = yes'
 for pair in CONSTITUTION_CHOICES.values()
 for key, kind in zip(pair, ('executive', 'representative'))
}
PROGRAMME_CONTRACT_GATES = {
 P+'national_front': P+'front_contract_active = yes',
 P+'baath_monopoly': 'NOT = { has_country_flag = COLDWAR_IRQ_front_accepted }',
}


def extra_focus_decisions(data):
    """Pure catalogue extension; loader calls this once after structural edits."""
    specifications = [
      ('icp_preaccession', 'The Communist Question', 'START', 'state', 60, 90,
       'Negotiate legal activity and Front participation, or organize an independent opposition. Government remains in the hands of the incumbent.'),
      ('constitutional_settlement_review', 'Convene a Constitutional Conference', 'START', 'state', 100, 180,
       'Choose the current constitutional settlement. Ratification costs 1% of GDP and replaces incompatible programme authority.'),
      ('front_labour_terms', 'Negotiate the Front Labour Charter', 'COLDWAR_IRQ_national_front', 'baath', 50, 180,
       'Independent workplace representation supports industrial cooperation while requiring funded social commitments.'),
      ('party_state_mobilization', 'Mobilize the Party Organizations', 'COLDWAR_IRQ_baath_monopoly', 'baath', 50, 180,
       'Coordinate the party organizations through the executive, with a funded administrative commitment.'),
      ('army_priority_review', 'Review the Army Priority', 'COLDWAR_IRQ_saddam_guard', 'saddam', 75, 180,
       'Redistribute the current military priority between the Guard and the regular army. The review costs 1% of GDP.'),
      ('defence_diversified_offer', 'Negotiate a Second Advisory Mission', 'COLDWAR_IRQ_defence_mixed_supply', 'defence', 60, 90,
       'Invite a French or British advisory mission on agreed terms. The partner can refuse; accepted advisers require Iraqi funding.'),
      ('agriculture_priority_review', 'Review the Rural Credit Priority', 'COLDWAR_IRQ_agri_land_survey', 'agriculture', 75, 180,
       'Redistribute future rural credit between cooperative machinery and smallholder guarantees. Review costs 1% of GDP; existing farms and completed investments remain.'),
      ('oil_revenue_priority_review', 'Review the Oil Revenue Priority', 'COLDWAR_IRQ_oil_technical_training', 'oil', 75, 180,
       'Reallocate the next planning round between export revenue and non-oil development. Review costs 1% of GDP; completed investment remains in place.'),
      ('north_fiscal_settlement', 'Negotiate the Northern Revenue Settlement', 'COLDWAR_IRQ_north_talks', 'state', 75, 90,
       'Negotiate revenue-sharing or central administration with local guarantees. Ratification costs 2% of GDP; regional governments control their response.'),
    ]
    existing = {d['id']: d for d in data['decisions']}
    nodes = {n['id']: n for n in data['nodes']}
    for key, label, unlock, group, pp, days, summary in specifications:
        spec = dict(id=P+'decision_'+key, label=label, unlock=unlock,
                    group=group, pp=pp, days=days, cooldown=days, summary=summary)
        if spec['id'] not in existing:
            data['decisions'].append(spec)
            existing[spec['id']] = spec
        if unlock in nodes and not any(x['id']==spec['id'] for x in nodes[unlock]['decisions']):
            nodes[unlock]['decisions'].append(spec)
    readiness = existing.get(P+'decision_defence_readiness_cycle')
    if readiness:
        readiness.update(summary='Fund 90 days of readiness: organization +4%, organization recovery +4%, army personnel costs +4%. Cost: 0.5% of GDP; 180-day cooldown.', cooldown=180)
    return data


def generate(root: Path = ROOT) -> dict[str, str]:
    root=Path(root)
    from audit_design import load_design
    data=load_design()
    decs={d['id'].removeprefix(P+'decision_'):d for d in data['decisions']}
    nodes={n['id']:n for n in data['nodes']}
    event_contract=json.loads(Path(__file__).with_name('decision_event_ids.json').read_text(encoding='utf-8'))
    stable_event_ids={(r['title'],r['occurrence']):r['id'] for r in event_contract['events']+event_contract['new_events']}
    event_occurrences={}
    loc={};effects=[];events=[];triggers=[];decision_blocks=[];ideas=[];counter=100
    handled=set();event_authority={};quotes={};direct_quote_actions=[];organization_ticks=[]

    def L(k,v):loc[k]=v;return k
    def E(k,body,guard=True):
        if guard:body=block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+body)
        effects.append(block(P+k,body));return P+k+' = yes'
    def opt(label,body='',gate='',ai=50):
        nonlocal counter
        counter+=1;key=L(P+'option_'+str(counter),label)
        return block('option','name = '+key+'\n'+(block('trigger',gate) if gate else '')+block('ai_chance',f'factor = {ai}')+body)
    def event(title,desc,options,gate='COLDWAR_IRQ_campaign_active = yes'):
        nonlocal counter
        counter+=1
        event_occurrences[title]=event_occurrences.get(title,0)+1
        contract_title=event_contract.get('aliases',{}).get(title,title)
        eid=stable_event_ids.get((contract_title,event_occurrences[title]))
        if eid is None:raise ValueError('Reserve a stable decision-event ID before adding '+repr((title,event_occurrences[title])))
        tk=L(eid+'.t',title);dk=L(eid+'.d',desc)
        # Freeze every quoted option before its native tooltip is displayed.
        # The execution branch below still rechecks positive quote and funds.
        immediate=[];shown='\n'.join(options)
        for _,q in quotes.values():
            if q in shown:immediate.append(q);shown=shown.replace(q,'')
        events.append(block('country_event',f'id = {eid}\ntitle = {tk}\ndesc = {dk}\nis_triggered_only = yes\n'+block('trigger',gate)+(block('immediate','\n'.join(immediate)) if immediate else '')+shown))
        return f'country_event = {{ id = {eid} }}'
    def menu(title,desc,options,gate='COLDWAR_IRQ_campaign_active = yes'):
        return event(title,desc,options+[opt('Close the conference.')],gate)
    def dg(key):
        # IMPERIA CW — Cold War: consolidated actions retain each original authority.
        from decision_streamlining import authority
        combined=authority(data,key)
        if combined:return combined
        if key in ['icp_preaccession', 'icp_front_terms']:
            return 'COLDWAR_IRQ_campaign_active = yes\nOR = { check_variable = { ruling_party = 21 } check_variable = { ruling_party = 4 } }'
        if key=='army_priority_review':
            return group_gate('saddam')+'\nOR = { has_country_flag = COLDWAR_IRQ_saddam_guard_implemented has_country_flag = COLDWAR_IRQ_saddam_regular_army_implemented }'
        d=decs[key]
        if d['unlock']=='START':return group_gate(d['group'])+'\nalways = yes'
        providers=d.get('audit_providers',[d['unlock']])
        reached='\n'.join(f'has_country_flag = {fid}_implemented' for fid in providers)
        if len(providers)>1:reached=block('OR',reached)
        return group_gate(d['group'])+f'\nhas_country_flag = {d["id"]}_unlocked\n'+reached
    def quote(k,share):
        q=invoice(P+'D_'+k,share);quotes[k]=(share,q);return q
    def cashgate(k):return f'has_country_flag = {P}D_{k}_quoted\ncheck_variable = {{ {P}D_{k}_invoice > 0 }}\n'+check('treasury',P+'D_'+k+'_invoice')+'\ncheck_variable = { gdp_total > 0 }\nNOT = { has_country_flag = MD_skip_treasury_cost }'
    def paid(k,share,payload,gate='',once=False):
        used=P+'D_'+k+'_used'
        body=quote(k,share)+block('if',block('limit',cashgate(k)+'\n'+gate+'\n'+(f'NOT = {{ has_country_flag = {used} }}' if once else ''))+pay_var(P+'D_'+k+'_invoice')+'\n'+payload+'\n'+(f'set_country_flag = {used}' if once else f'clr_country_flag = {P}D_{k}_quoted'))
        return body
    def register(key,payload,extra='',cooldown=None):
        d=decs[key];handled.add(key)
        # An already-open menu cannot preserve a former government's authority.
        # Shared menus accept the OR of their genuine, still-active providers.
        for eid in re.findall(r'country_event\s*=\s*\{\s*id\s*=\s*(COLDWAR_IRQ_decision_events\.\d+)',payload):
            event_authority.setdefault(eid,[]).append(dg(key)+'\n'+extra)
        helper=E('do_'+key,block('if',block('limit',dg(key)+'\n'+extra)+payload))
        body='icon = generic_political_discourse\n'+block('visible',dg(key))+'\n'+block('available',dg(key)+'\n'+extra)+f'\ncost = {d["pp"]}\ndays_re_enable = {d.get("cooldown",cooldown if cooldown is not None else max(d["days"],30))}\n'+block('complete_effect',helper)+'\nai_will_do = { factor = 1 }'
        decision_blocks.append(block(d['id'],body))
        L(d['id'],d['label']);L(d['id']+'_desc',d['summary'])
    def popularity(slot,amount=.03):
        return f'set_temp_variable = {{ party_index = {slot} }}\nset_temp_variable = {{ party_popularity_increase = {amount:g} }}\nset_temp_variable = {{ temp_outlook_increase = {amount:g} }}\nchange_relative_party_popularity = yes\nset_temp_variable = {{ temp_outlook_increase = 0 }}'
    def native_party(slot,elections=False):
        return f'set_temp_variable = {{ rul_party_temp = {slot} }}\nset_temp_variable = {{ change_leader_temp = 1 }}\nset_temp_variable = {{ disable_elections = {0 if elections else 1} }}\nchange_ruling_party_effect = yes'
    def sync():return 'COLDWAR_IRQ_reconcile_programmes = yes\nupdate_dirty_politicsview_expanded = yes'

    # Local ideas are real, time-bounded costs/rewards, not unconsumed counters.
    idea_specs={
      'negotiation_cost':('Constitutional Administration',{'bureaucracy_cost_multiplier_modifier':.04,'political_power_factor':-.03}),
      'technical_exchange':('Funded Technical Exchange',{'research_speed_factor':.03,'bureaucracy_cost_multiplier_modifier':.04}),
      'advisers':('Contracted Army Advisers',{'army_org_factor':.03,'army_personnel_cost_multiplier_modifier':.05}),
      'readiness_cycle':('Funded Readiness Cycle',{'army_org_factor':.04,'army_morale_factor':.04,'army_personnel_cost_multiplier_modifier':.04}),
      'autonomy_guarantee_cost':('Northern Constitutional Guarantees',{'bureaucracy_cost_multiplier_modifier':.04,'political_power_factor':-.02}),
      'civil_rights_cost':('Maintaining Political Guarantees',{'bureaucracy_cost_multiplier_modifier':.03,'drift_defence_factor':-.04}),
      'border_navigation':('Reciprocal River Navigation',{'political_power_factor':.03,'bureaucracy_cost_multiplier_modifier':.03}),
      'current_export_contract':('Current Oil Export Contract',{'oil_export_multiplier_modifier':.03,'tax_gain_multiplier_modifier':-.02,'bureaucracy_cost_multiplier_modifier':.02}),
      'front_labour_charter':('Front Labour Charter',{'production_factory_efficiency_gain_factor':.05,'social_cost_multiplier_modifier':.02}),
      'party_mobilization':('Party Organization Drive',{'political_power_factor':.05,'bureaucracy_cost_multiplier_modifier':.02}),
      'north_revenue_sharing':('Northern Revenue-Sharing Settlement',{'tax_gain_multiplier_modifier':-.05,'bureaucracy_cost_multiplier_modifier':.02}),
      'north_central_administration':('Central Administration and Local Guarantees',{'army_personnel_cost_multiplier_modifier':.03,'bureaucracy_cost_multiplier_modifier':.01}),
    }
    idea_art={'negotiation_cost':'government_beu','technical_exchange':'generic_university','advisers':'army_reform','readiness_cycle':'army_reform','autonomy_guarantee_cost':'focus_generic_court','civil_rights_cost':'focus_generic_court','border_navigation':'diplomatic_treaty','current_export_contract':'diplomatic_treaty','front_labour_charter':'government_beu','party_mobilization':'government_beu'}
    idea_art.update(north_revenue_sharing='diplomatic_treaty',north_central_administration='government_beu')
    gfx=[];native_gfx=(root/'interface/goals.gfx').read_text(encoding='utf-8-sig')
    for key,(title,mods) in idea_specs.items():
        cancel=''
        if key=='autonomy_guarantee_cost':cancel='cancel = { NOT = { IRQ = { COLDWAR_IRQ_northern_settlement_active = yes } } }'
        if key=='civil_rights_cost':cancel='cancel = { NOT = { IRQ = { has_country_flag = COLDWAR_IRQ_legalization_accepted } } }'
        if key=='border_navigation':cancel='cancel = { NOT = { IRQ = { COLDWAR_IRQ_border_settlement_active = yes } } }'
        if key=='front_labour_charter':cancel='cancel = { NOT = { IRQ = { COLDWAR_IRQ_front_contract_active = yes } } }'
        if key=='party_mobilization':cancel='cancel = { NOT = { IRQ = { check_variable = { ruling_party = 21 } has_country_flag = COLDWAR_IRQ_policy_baath_baath_monopoly NOT = { has_country_flag = COLDWAR_IRQ_front_accepted } } } }'
        if key.startswith('north_'):cancel='cancel = { NOT = { IRQ = { COLDWAR_IRQ_northern_settlement_active = yes } } }'
        texture=re.search(r'name\s*=\s*"'+re.escape(idea_art[key])+r'"\s+texturefile\s*=\s*"([^"]+)"',native_gfx,re.I)
        if not texture:raise ValueError('Missing native idea-art source '+idea_art[key])
        gfx.append(block('spriteType',f'name = "GFX_idea_{P+key}"\ntexturefile = "{texture[1]}"'))
        ideas.append(block(P+key,'picture = '+P+key+'\n'+cancel+'\n'+block('modifier','\n'.join(f'{k} = {v:g}' for k,v in mods.items()))))
        descriptions={
          'negotiation_cost':'New guarantees need offices, legal expertise and an administration capable of carrying them into effect.',
          'technical_exchange':'Foreign specialists and Iraqi engineers work together under a funded exchange programme.',
          'advisers':'An agreed foreign mission supports Iraqi training while its upkeep remains a charge on the military budget.',
          'readiness_cycle':'Units return to training grounds for staff exercises, maintenance and rehearsals. Higher readiness depends on a temporary personnel commitment.',
          'autonomy_guarantee_cost':'Local civil administration and negotiated language rights depend on a sustained public commitment to the northern settlement.',
          'civil_rights_cost':'Legal political activity requires enforceable safeguards and leaves the government less free to silence organized opposition.',
          'border_navigation':'The reciprocal river settlement supports regular navigation and requires the continuing cooperation of both governments.',
          'current_export_contract':'A negotiated export arrangement secures an agreed outlet for Iraqi oil while imposing its own commercial and administrative obligations.',
          'front_labour_charter':'Independent workplace delegates help settle disputes and organize production. Their cooperation rests on funded social commitments and meaningful participation.',
          'party_mobilization':'The executive coordinates party unions and mass organizations through a common campaign, supported by additional administrative staff.',
          'north_revenue_sharing':'Regional authorities receive a guaranteed share of public revenue. Baghdad relinquishes part of its central receipts in return for the broader settlement of northern administration and security.',
          'north_central_administration':'Baghdad retains central fiscal administration while maintaining agreed local guarantees. This narrower settlement continues to require a larger security and administrative presence.',
        }
        L(P+key,title);L(P+key+'_desc',descriptions[key])
    triggers.append(block(P+'border_settlement_active','COLDWAR_IRQ_campaign_active = yes\nhas_country_flag = COLDWAR_IRQ_border_accepted\ncountry_exists = PER\nNOT = { has_war_with = PER }\nPER = { has_country_flag = COLDWAR_IRQ_border_partner }'))
    triggers.append(block(P+'oil_concession_active','COLDWAR_IRQ_campaign_active = yes\nhas_country_flag = COLDWAR_IRQ_oil_concession_accepted\ncountry_exists = ENG\nNOT = { has_war_with = ENG }\nENG = { has_country_flag = COLDWAR_IRQ_oil_concession_partner }'))
    L(P+'front_contract_active_tt','The Front charter and coalition guarantees are being respected')
    triggers.append(block(P+'front_contract_active',block('custom_trigger_tooltip','tooltip = '+P+'front_contract_active_tt\n'+CONTRACTS['Accepted front charter'])))
    for kind in ['executive','representative']:
        title=P+'constitution_'+kind+'_active_tt'
        L(title,'The current constitutional settlement permits '+kind+' authority')
        triggers.append(block(P+'constitution_'+kind+'_active',block('custom_trigger_tooltip','tooltip = '+title+'\nCOLDWAR_IRQ_campaign_active = yes\nOR = { NOT = { has_country_flag = COLDWAR_IRQ_constitution_bound } has_country_flag = COLDWAR_IRQ_constitution_'+kind+' }')))
        other='representative' if kind=='executive' else 'executive'
        E('adopt_constitution_'+kind,'set_country_flag = COLDWAR_IRQ_constitution_bound\nset_country_flag = COLDWAR_IRQ_constitution_'+kind+'\nclr_country_flag = COLDWAR_IRQ_constitution_'+other)
    settle=[]
    # A newly selected first constitutional focus can establish authority.
    # Once bound, only the paid conference changes this current contract.
    for use_selection in [True,False]:
        for group,pair in sorted(CONSTITUTION_CHOICES.items(),key=lambda row:row[0]=='state'):
            for key,kind in zip(pair,['executive','representative']):
                if P+key not in nodes:
                    raise ValueError('Unknown constitutional focus '+P+key)
                evidence=f'has_country_flag = {P}policy_{group}_{key}' if use_selection else f'has_country_flag = {P+key}_implemented'
                settle.append(block('if',block('limit','NOT = { has_country_flag = COLDWAR_IRQ_constitution_bound }\n'+group_gate(group)+'\n'+evidence)+P+'adopt_constitution_'+kind+' = yes'))
    settle.append(block('if',block('limit','NOT = { COLDWAR_IRQ_front_contract_active = yes }')+'remove_ideas = COLDWAR_IRQ_front_labour_charter'))
    settle.append(block('if',block('limit','OR = { has_country_flag = COLDWAR_IRQ_front_accepted NOT = { check_variable = { ruling_party = 21 } } NOT = { has_country_flag = COLDWAR_IRQ_policy_baath_baath_monopoly } }')+'remove_ideas = COLDWAR_IRQ_party_mobilization'))
    # Existing ratified federal/local guarantees migrate to the corresponding
    # current fiscal terms. This adds no one-time reward and makes their ongoing
    # real revenue/security costs explicit.
    settle.append(block('if',block('limit','COLDWAR_IRQ_northern_settlement_active = yes\nNOT = { has_country_flag = COLDWAR_IRQ_north_terms_revenue }\nNOT = { has_country_flag = COLDWAR_IRQ_north_terms_central }')+block('if',block('limit','has_country_flag = COLDWAR_IRQ_federal_settlement')+'set_country_flag = COLDWAR_IRQ_north_terms_revenue')+block('else','set_country_flag = COLDWAR_IRQ_north_terms_central')))
    for terms,idea,other in [('revenue','north_revenue_sharing','north_central_administration'),('central','north_central_administration','north_revenue_sharing')]:
        settle.append(block('if',block('limit','COLDWAR_IRQ_northern_settlement_active = yes\nhas_country_flag = COLDWAR_IRQ_north_terms_'+terms)+'remove_ideas = '+P+other+'\n'+block('if',block('limit','NOT = { has_idea = '+P+idea+' }')+'add_ideas = '+P+idea)))
    settle.append(block('if',block('limit','NOT = { COLDWAR_IRQ_northern_settlement_active = yes }')+'remove_ideas = COLDWAR_IRQ_north_revenue_sharing\nremove_ideas = COLDWAR_IRQ_north_central_administration'))
    settle.append(block('if',block('limit','NOT = { has_country_flag = COLDWAR_IRQ_autonomy_accepted }')+'clr_country_flag = COLDWAR_IRQ_north_terms_revenue\nclr_country_flag = COLDWAR_IRQ_north_terms_central'))
    E('reconcile_political_contracts','\n'.join(settle))
    register('constitutional_settlement_review',menu('The constitutional settlement','The distribution of executive authority must be agreed before incompatible programmes can operate together. A new conference can replace the settlement after a change of government.',[
      opt('Ratify executive constitutional authority.',paid('constitution_executive',.01,P+'adopt_constitution_executive = yes\n'+sync())),
      opt('Ratify representative constitutional authority.',paid('constitution_representative',.01,P+'adopt_constitution_representative = yes\n'+sync()))]))

    # Earned programme review never executes a focus reward or rewinds completion.
    def policy_menu(group,onlykeys=None):
        pairs=[];seen=set()
        for n in data['nodes']:
            if n['group']!=group or (onlykeys and n['key'] not in onlykeys):continue
            for other in n['mutually_exclusive']:
                pair=tuple(sorted([n['id'],other]))
                if pair not in seen:pairs.append(pair);seen.add(pair)
        options=[]
        for pair in pairs:
            for fid in pair:
                n=nodes[fid];other=next(p for p in pair if p!=fid)
                flag=P+'policy_'+group+'_'+n['key'];opposite=P+'policy_'+group+'_'+nodes[other]['key']
                gate=group_gate(group)+f'\nOR = {{ has_completed_focus = {pair[0]} has_completed_focus = {pair[1]} }}\nOR = {{ has_country_flag = {pair[0]}_implemented has_country_flag = {pair[1]}_implemented }}\n'+POLICY_CONTRACT_GATES.get(fid,'')
                payload=f'clr_country_flag = {opposite}\nset_country_flag = {flag}\nset_country_flag = {fid}_package_earned\n'+sync()
                options.append(opt('Adopt the programme: '+n['title'],paid('policy_'+n['key'],.01,payload,gate),gate))
        titles={'state':'The constitutional programme','civic':'The cabinet programme','foreign':'External commitments','industry':'The next investment round','society':'Social coverage and services','saddam':'The Guard and the General Staff','agriculture':'Rural credit and machinery','oil':'The oil revenue programme'}
        descriptions={
          'state':'Ministers must reconcile the current settlement of authority with the institutions they intend to strengthen. Reopening that settlement requires a funded political conference.',
          'civic':'The cabinet must agree which commitments take priority in its next programme. Coalition partners expect the new allocation to be reflected in ministerial policy.',
          'foreign':'External commitments should serve Iraq’s current interests. Revising our diplomatic priorities requires consultation and a clear division of responsibilities.',
          'industry':'The next round of investment can concentrate on basic industry or on wider civilian production. The chosen priority will direct public planning and support.',
          'society':'Public services must match the government’s commitments to households and neglected districts. Ministers can revise the priorities that guide social provision.',
          'saddam':'Modern equipment, trained officers and premium pay cannot be concentrated everywhere. The presidency must decide whether the Guard or the regular army receives priority.',
          'agriculture':'Rural lenders and machinery services must decide how to divide support between cooperative equipment pools and individual cultivators.',
          'oil':'The next planning round must decide how much to emphasize export receipts and how much to develop the non-oil economy. This allocation operates within the existing ownership settlement.',
        }
        return menu(titles[group],descriptions[group],options,group_gate(group))
    for key,group in [('constitutional_revision','state'),('civic_policy_review','civic'),('foreign_policy_review','foreign'),('industry_reallocate','industry'),('society_revision','society')]:register(key,policy_menu(group))
    register('army_priority_review',policy_menu('saddam',{'saddam_guard','saddam_regular_army'}))
    register('agriculture_priority_review',policy_menu('agriculture',{'agri_cooperatives','agri_smallholders'}))
    register('oil_revenue_priority_review',policy_menu('oil',{'oil_revenue_state','oil_diversification'}))

    # Domestic consent is an explicit response, followed by a paid implementation.
    legal_body='set_country_flag = COLDWAR_IRQ_legalization_accepted\nif = { limit = { date < 1971.11.28 NOT = { has_country_flag = COLDWAR_IRQ_rikabi_dead } } set_country_flag = COLDWAR_IRQ_rikabi_rehabilitated }\nif = { limit = { date < 1971.1.1 } set_country_flag = COLDWAR_IRQ_dawa_cadres_protected }\nset_temp_variable = { party_index = 4 }\nunban_party_scripted_call = yes\nadd_ideas = COLDWAR_IRQ_civil_rights_cost\n'+sync()
    legal_offer=menu('A political opening','Opposition parties want more than permission to meet. Legal protection needs enforceable safeguards, while the government must decide whether it will accept organized criticism of its policies.',[
        opt('Accept legal rights and fund their implementation.',paid('legalization',.01,legal_body)),
        opt('Reject the proposed guarantees.','add_stability = -0.01'),
        opt('End the government guarantees.', 'COLDWAR_IRQ_leave_front = yes\nclr_country_flag = COLDWAR_IRQ_legalization_accepted\nremove_ideas = COLDWAR_IRQ_civil_rights_cost\n'+sync(),'has_country_flag = COLDWAR_IRQ_legalization_accepted')])
    register('political_opening',legal_offer)
    register('prison_review',menu('Individual prisoner review','Review political detention without promising a party accession. Earlier protection is needed to retain historically persecuted candidates after their historical disappearance.',[
      opt('Release and rehabilitate detained political organizers.',paid('prison_review',.005,'if = { limit = { date < 1971.1.1 NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } } set_country_flag = COLDWAR_IRQ_dawa_cadres_protected }\nif = { limit = { date < 1973.1.1 NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } } set_country_flag = COLDWAR_IRQ_dukhayl_released clr_country_flag = COLDWAR_IRQ_dukhayl_unavailable }\n'+block('if',block('limit','date < 1971.11.28 NOT = { has_country_flag = COLDWAR_IRQ_rikabi_dead }')+'set_country_flag = COLDWAR_IRQ_rikabi_rehabilitated')+'\nadd_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 90 }')),
      opt('Retain detention subject to judicial review.','add_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 60 }')]))

    # USA already owns existing-country reciprocal consent/payment; use it.
    domestic_autonomy=menu('The northern constitutional offer','The regional delegates choose whether to accept defined local civil administration, language rights and a negotiated budget within Iraq. No state is transferred and no country is released. Delivery costs 2% of frozen Iraqi GDP.',[
      opt('The delegates accept; fund the guarantees.',paid('domestic_autonomy',.02,'set_country_flag = COLDWAR_IRQ_autonomy_accepted\nset_country_flag = COLDWAR_IRQ_autonomy_fulfilled\nadd_ideas = COLDWAR_IRQ_autonomy_guarantee_cost\n'+sync(),gate='OR = { 164 = { is_owned_and_controlled_by = IRQ } 633 = { is_owned_and_controlled_by = IRQ } 630 = { is_owned_and_controlled_by = IRQ } }',once=True)),
      opt('The delegates reject the terms.','add_stability = -0.01'),
      opt('Revoke the agreement and its guarantees.','clr_country_flag = COLDWAR_IRQ_autonomy_accepted\nclr_country_flag = COLDWAR_IRQ_autonomy_fulfilled\nclr_country_flag = COLDWAR_IRQ_federal_settlement\nremove_ideas = COLDWAR_IRQ_autonomy_guarantee_cost\n'+sync(),'has_country_flag = COLDWAR_IRQ_autonomy_accepted')])
    E('begin_kurdish_negotiations','if = { limit = { OR = { country_exists = KUR country_exists = PUK } } country_event = { id = COLDWAR_USA_gulf_events.30 } }\nelse = { '+domestic_autonomy+' }')
    register('march_offer','COLDWAR_IRQ_begin_kurdish_negotiations = yes')
    for key in ['icp_federal_talks','puk_federal_convention','kdp_kirkuk_talks']:
        register(key,block('if',block('limit','COLDWAR_IRQ_northern_settlement_active = yes')+'COLDWAR_IRQ_begin_north_fiscal_conference = yes')+block('else','COLDWAR_IRQ_begin_kurdish_negotiations = yes'))

    # A regional government is an actual recipient: Iraq cannot accept its own
    # fiscal proposal for a player-controlled Kurdistan. Every existing partner
    # must consent before the one Iraqi payment and replacement occur.
    north_authority=block('OR','\n'.join(block('AND',dg(key)) for key in ['north_fiscal_settlement','icp_federal_talks','puk_federal_convention','kdp_kirkuk_talks']))
    north_live=north_authority+'\nCOLDWAR_IRQ_northern_settlement_active = yes\n165 = { is_owned_and_controlled_by = IRQ }'
    northchoices=[];northfinish=[]
    for terms,title in [('revenue','Revenue-sharing and regional authority'),('central','Central administration with local guarantees')]:
        pending=P+'north_offer_'+terms
        quotation=f'has_country_flag = {P}D_north_{terms}_quoted\ncheck_variable = {{ {P}D_north_{terms}_invoice > 0 }}\ncheck_variable = {{ gdp_total > 0 }}\nNOT = {{ has_country_flag = MD_skip_treasury_cost }}'
        approve=[f'OR = {{ NOT = {{ country_exists = {tag} }} has_country_flag = {P}north_{terms}_accepted_{tag} }}' for tag in ['KUR','PUK']]
        payload='set_country_flag = COLDWAR_IRQ_north_terms_'+terms+'\nclr_country_flag = COLDWAR_IRQ_north_terms_'+('central' if terms=='revenue' else 'revenue')+'\n'
        if terms=='revenue':payload+='set_country_flag = COLDWAR_IRQ_federal_settlement\nset_country_flag = COLDWAR_IRQ_kirkuk_revenue_accepted\n'
        else:payload+='clr_country_flag = COLDWAR_IRQ_federal_settlement\nclr_country_flag = COLDWAR_IRQ_kirkuk_revenue_accepted\n'
        payload+='clr_country_flag = '+pending+'\nCOLDWAR_IRQ_reconcile_political_contracts = yes\n'+sync()
        finalgate=north_live+'\nhas_country_flag = '+pending+'\n'+quotation+'\n'+'\n'.join(approve)
        northfinish.append(block('if',block('limit',finalgate)+paid('north_'+terms,.02,payload,finalgate)))
        request=quote('north_'+terms,.02)+'set_country_flag = { flag = '+pending+' days = 60 value = 1 }\n'
        for tag in ['KUR','PUK']:
            accepted=P+'north_'+terms+'_accepted_'+tag
            replygate=f'tag = {tag}\ncountry_exists = IRQ\nNOT = {{ has_war_with = IRQ }}\nIRQ = {{ {north_live}\nhas_country_flag = {pending}\n{quotation} }}'
            reply=event(title,'Baghdad proposes a new division of northern authority and public revenue. Your government may accept the terms or reject the proposal. Ratification proceeds only after every participating regional government agrees.',[
              opt('Accept the proposed settlement.',f'IRQ = {{ set_country_flag = {accepted} COLDWAR_IRQ_finalize_north_terms = yes }}',replygate),
              opt('Reject the proposed settlement.',f'IRQ = {{ clr_country_flag = {pending} clr_country_flag = {P}D_north_{terms}_quoted }}',replygate)],gate=replygate)
            request+='clr_country_flag = '+accepted+'\n'+block('if',block('limit','country_exists = '+tag)+block(tag,reply))
        request+='COLDWAR_IRQ_finalize_north_terms = yes'
        # Where no Kurdish state exists, a domestic response remains explicit.
        domestic=menu(title,'The regional delegates must agree to the proposed fiscal settlement before it can replace the existing guarantees.',[
          opt('The delegates ratify the settlement.',request,'NOT = { country_exists = KUR } NOT = { country_exists = PUK }\n'+quotation),
          opt('The delegates reject the proposal.')],gate=north_live)
        action=block('if',block('limit','OR = { country_exists = KUR country_exists = PUK }')+request)+block('else',domestic)
        L(P+'north_ratification_tt','If the settlement is ratified:')
        idea=P+('north_revenue_sharing' if terms=='revenue' else 'north_central_administration')
        other=P+('north_central_administration' if terms=='revenue' else 'north_revenue_sharing')
        preview='custom_effect_tooltip = COLDWAR_IRQ_north_ratification_tt\n'+block('effect_tooltip','remove_ideas = '+other+'\nadd_ideas = '+idea)
        northchoices.append(opt(title,preview+'\n'+action,north_live+'\n'+quotation+'\nNOT = { has_country_flag = COLDWAR_IRQ_north_offer_revenue }\nNOT = { has_country_flag = COLDWAR_IRQ_north_offer_central }'))
        for eid in re.findall(r'country_event\s*=\s*\{\s*id\s*=\s*(COLDWAR_IRQ_decision_events\.\d+)',domestic):
            event_authority.setdefault(eid,[]).append(north_live)
    E('finalize_north_terms','\n'.join(northfinish))
    north_menu=menu('Northern revenue and authority','A broader revenue-sharing settlement gives regional administration a larger role. Central administration retains the existing local guarantees but requires a greater continuing security presence. Kirkuk must remain under Iraqi control; the agreement grants no territory.',northchoices,gate=north_live)
    E('begin_north_fiscal_conference',block('if',block('limit',north_live)+north_menu))
    register('north_fiscal_settlement','COLDWAR_IRQ_begin_north_fiscal_conference = yes', 'COLDWAR_IRQ_northern_settlement_active = yes\n165 = { is_owned_and_controlled_by = IRQ }')
    front=menu('National Front terms','The prospective partners demand ministries, legal protections and a voice in public policy. The Baath leadership must decide whether to offer genuine cooperation or retain an arrangement in which its partners have little influence.',[
      opt('Accept the charter and legal guarantees.',paid('front',.01,'set_country_flag = COLDWAR_IRQ_front_accepted\nset_country_flag = COLDWAR_IRQ_legalization_accepted\nset_country_flag = COLDWAR_IRQ_icp_strategy_front\nclr_country_flag = COLDWAR_IRQ_icp_strategy_independent\nset_temp_variable = { party_index = 4 }\nunban_party_scripted_call = yes\nremove_ideas = COLDWAR_IRQ_party_mobilization\nadd_ideas = COLDWAR_IRQ_civil_rights_cost\nif = { limit = { check_variable = { ruling_party = 21 } NOT = { is_in_array = { array = gov_coalition_array value = 4 } } } add_to_array = { gov_coalition_array = 4 } }\nif = { limit = { check_variable = { ruling_party = 4 } NOT = { is_in_array = { array = gov_coalition_array value = 21 } } } add_to_array = { gov_coalition_array = 21 } }\nupdate_government_coalition_strength = yes\n'+sync())),
      opt('Refuse an unequal front.','add_stability = -0.01'),
      opt('Leave the existing front.','COLDWAR_IRQ_leave_front = yes','has_country_flag = COLDWAR_IRQ_front_accepted')])
    E('leave_front','clr_country_flag = COLDWAR_IRQ_front_accepted\nclr_country_flag = COLDWAR_IRQ_icp_strategy_front\nremove_ideas = COLDWAR_IRQ_front_labour_charter\nif = { limit = { check_variable = { ruling_party = 21 } } remove_from_array = { gov_coalition_array = 4 } }\nif = { limit = { check_variable = { ruling_party = 4 } } remove_from_array = { gov_coalition_array = 21 } }\nupdate_government_coalition_strength = yes\n'+sync())
    for key in ['front_offer','icp_front_terms']:register(key,front)
    preaccession=menu('The Communist question','The Communists have a choice between participation under negotiated guarantees and an independent political organization. Baghdad must decide how much legal space it is prepared to allow.',[
      opt('Negotiate ministries and a Front charter.',front),
      opt('Discuss legal political activity.',legal_offer),
      opt('Organize an independent opposition.',paid('independent_opposition',.005,'COLDWAR_IRQ_leave_front = yes\nset_country_flag = COLDWAR_IRQ_icp_strategy_independent\n'+popularity(4,.02)+'\nset_country_flag = { flag = COLDWAR_IRQ_D_opposition_cooldown days = 180 value = 1 }',gate='NOT = { has_country_flag = COLDWAR_IRQ_D_opposition_cooldown }')+'\n', 'NOT = { has_country_flag = COLDWAR_IRQ_D_opposition_cooldown }'),
      opt('Leave the Front but retain legal rights.','COLDWAR_IRQ_leave_front = yes','has_country_flag = COLDWAR_IRQ_front_accepted')])
    register('icp_preaccession',preaccession)
    for payload in [front,legal_offer]:
        for eid in re.findall(r'country_event\s*=\s*\{\s*id\s*=\s*(COLDWAR_IRQ_decision_events\.\d+)',payload):
            event_authority.setdefault(eid,[]).append(dg('icp_preaccession'))
    labourgate='COLDWAR_IRQ_front_contract_active = yes\nNOT = { has_idea = COLDWAR_IRQ_party_mobilization } NOT = { has_country_flag = COLDWAR_IRQ_D_front_labour_cooldown }'
    register('front_labour_terms',paid('front_labour',.01,'add_timed_idea = { idea = COLDWAR_IRQ_front_labour_charter days = 180 }\nset_country_flag = { flag = COLDWAR_IRQ_D_front_labour_cooldown days = 180 value = 1 }',labourgate),labourgate+'\n'+cashgate('front_labour'),cooldown=180)
    direct_quote_actions.append(('front_labour_terms','front_labour',.01,labourgate))
    monopolygate='has_country_flag = COLDWAR_IRQ_policy_baath_baath_monopoly\nNOT = { has_country_flag = COLDWAR_IRQ_front_accepted }\nNOT = { has_idea = COLDWAR_IRQ_front_labour_charter } NOT = { has_country_flag = COLDWAR_IRQ_D_party_drive_cooldown }'
    register('party_state_mobilization',paid('party_drive',.01,'add_timed_idea = { idea = COLDWAR_IRQ_party_mobilization days = 180 }\nset_country_flag = { flag = COLDWAR_IRQ_D_party_drive_cooldown days = 180 value = 1 }',monopolygate),monopolygate+'\n'+cashgate('party_drive'),cooldown=180)
    direct_quote_actions.append(('party_state_mobilization','party_drive',.01,monopolygate))
    # IMPERIA CW — Cold War: political narratives for retained party consultations.
    register('aziz_exit_front',menu('Continued front participation','The Front has given the party a place in government, but its ministers must answer to members who question the terms of cooperation. The leadership must decide whether continued participation still serves its programme or whether the party should withdraw from the coalition.',[opt('End participation.','COLDWAR_IRQ_leave_front = yes'),opt('Maintain the existing terms.',sync(),'has_country_flag = COLDWAR_IRQ_front_accepted')]))
    register('aziz_charter',legal_offer)
    register('officer_amnesty_offer',legal_offer)
    transition=menu('The constitutional vote','The transition charter would bind the officers to an electoral timetable and give civilian parties a lawful route to government. Ratification now depends on whether the leadership will accept a contest whose result it cannot dictate.',[
      opt('Ratify the transition charter.',paid('transition',.02,'set_country_flag = COLDWAR_IRQ_transition_accepted\nset_country_flag = COLDWAR_IRQ_legalization_accepted\nset_politics = { elections_allowed = yes }\nadd_ideas = COLDWAR_IRQ_civil_rights_cost\n'+sync(),once=True)),
      opt('The constitutional vote fails.','add_stability = -0.02')])
    register('officer_transition',transition)
    election='hold_elections = yes\nset_variable = { COLDWAR_IRQ_last_election_winner = max_index_1 }\nset_temp_variable = { rul_party_temp = max_index_1 }\nset_temp_variable = { change_leader_temp = 1 }\nset_temp_variable = { disable_elections = 0 }\nchange_ruling_party_effect = yes\n'+sync()
    register('civic_election',menu('A contested parliamentary election','The campaign has brought competing programmes before the electorate. The count will determine which eligible party receives the mandate to govern, while parliamentary negotiations will shape the coalition that follows. Ministers must now submit their record to the voters.',[opt('Count the votes and form the elected government.',election)]),'has_elections = yes')

    # Native leadership choices. Alternative national mandates are explicitly ALT.
    leader_choices={
      'arab_leadership':(18,[('haseeb','Khair al-Din Haseeb','',False),('rikabi','Fuad al-Rikabi','OR = { date < 1971.11.28 has_country_flag = COLDWAR_IRQ_rikabi_rehabilitated } NOT = { has_country_flag = COLDWAR_IRQ_rikabi_dead }',True)]),
      'icp_leadership_vote':(4,[('aziz','Aziz Muhammad','',False),('amir','Amir Abdullah','',True),('zaki','Zaki Khairi','',True)]),
      'aziz_renewal':(4,[('aziz','Aziz Muhammad','',False),('amir','Amir Abdullah','',True),('zaki','Zaki Khairi','',True)]),
      'dawa_leadership':(8,[('subayti','Muhammad Hadi al-Subayti','NOT = { has_country_flag = COLDWAR_IRQ_subayti_dead }',True),('dukhayl','Abd al-Sahib Dukhayl','NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_unavailable } NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead }',True),('jaafari','Ibrahim al-Jaafari','OR = { date > 1987.12.31 has_country_flag = COLDWAR_IRQ_subayti_dead }',True)]),
      'iip_congress':(12,[('numan','Numan al-Samarrai','',True),('ayad','Ayad al-Samarrai','date > 1989.1.1',True)]),
    }
    installed={}
    for key,(slot,choices) in leader_choices.items():
        opts=[]
        for short,name,gate,alternate in choices:
            flag=P+'leader_choice_'+str(slot)+'_'+short;installed[(slot,short)]=(name,flag,gate)
            clear='\n'.join('clr_country_flag = '+P+'leader_choice_'+str(slot)+'_'+v[0] for v in choices)
            body=clear+'\nset_country_flag = '+flag+'\nCOLDWAR_IRQ_set_leader = yes'
            opts.append(opt(('Alternate national mandate: ' if alternate else 'Confirm the historical party leadership: ')+name,block('if',block('limit',group_gate(decs[key]['group'])+'\n'+gate)+body),gate))
        register(key,menu('The party leadership congress','Delegates must choose a leadership capable of carrying the party programme into government. Experience, regional loyalties and competing views of the republic will shape the mandate entrusted to the next executive.',opts,group_gate(decs[key]['group'])))
    apply=[]
    for (slot,short),(name,flag,gate) in installed.items():
        ideology=PARTIES[slot][1]
        apply.append(block('if',block('limit',f'check_variable = {{ ruling_party = {slot} }} has_country_flag = {flag}\n'+gate+f'\nNOT = {{ has_country_leader = {{ name = "{name}" ruling_only = yes }} }}')+'kill_country_leader = yes\n'+block('create_country_leader',f'name = "{name}"\npicture = "gfx/leaders/EGY/Portrait_Arabia_Generic_1.dds"\nideology = {ideology}\ntraits = {{ }}')+'set_correct_ideology_trait = yes'))
    E('apply_decision_leader_choices','\n'.join(apply))
    roster='''# A recorded death is permanent; an earlier alternate government or legal
# protection can avert the historical coercion, never resurrect its victim.
if = { limit = { date < 1971.11.28 NOT = { has_country_flag = COLDWAR_IRQ_rikabi_dead }
 OR = { has_country_leader = { name = "Fuad al-Rikabi" ruling_only = yes } has_country_flag = COLDWAR_IRQ_rikabi_rehabilitated } }
 set_country_flag = COLDWAR_IRQ_rikabi_rehabilitated
}
if = { limit = { date < 1971.1.1 check_variable = { ruling_party = 8 } NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } }
 set_country_flag = COLDWAR_IRQ_dawa_cadres_protected
}
if = { limit = { date < 1973.1.1 check_variable = { ruling_party = 8 } NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } }
 set_country_flag = COLDWAR_IRQ_dukhayl_released
}
if = { limit = { date < 1980.1.1 NOT = { has_country_flag = COLDWAR_IRQ_subayti_dead }
 OR = { check_variable = { ruling_party = 8 } has_country_flag = COLDWAR_IRQ_dawa_cadres_protected } }
 set_country_flag = COLDWAR_IRQ_subayti_protected
}
if = { limit = { date > 1971.11.27 NOT = { has_country_flag = COLDWAR_IRQ_rikabi_rehabilitated } } set_country_flag = COLDWAR_IRQ_rikabi_dead }
if = { limit = { date > 1971.12.31 NOT = { has_country_flag = COLDWAR_IRQ_dawa_cadres_protected } NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_released } } set_country_flag = COLDWAR_IRQ_dukhayl_unavailable }
if = { limit = { NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_dead } OR = { has_country_flag = COLDWAR_IRQ_dawa_cadres_protected has_country_flag = COLDWAR_IRQ_dukhayl_released } } clr_country_flag = COLDWAR_IRQ_dukhayl_unavailable }
# Dukhayl: autumn1971 detention, death in1973; year precision avoids a false
# exact death date. Subayti: party memorial records9November1988.
if = { limit = { date > 1973.12.31 NOT = { has_country_flag = COLDWAR_IRQ_dawa_cadres_protected } NOT = { has_country_flag = COLDWAR_IRQ_dukhayl_released } } set_country_flag = COLDWAR_IRQ_dukhayl_dead }
if = { limit = { date > 1988.11.8 NOT = { has_country_flag = COLDWAR_IRQ_subayti_protected } } set_country_flag = COLDWAR_IRQ_subayti_dead }
'''
    E('reconcile_historical_roster',roster)
    def succession(kind):
        opts=[]
        if kind=='baath':
            candidates=[(0,'Ahmed Hassan al-Bakr','date < 1982.10.4'),(1,'Saddam Hussein',''),(2,'Tariq Aziz','')]
        else:candidates=[(0,'Mustafa Barzani','date < 1979.3.1'),(1,'Idris Barzani','date < 1987.1.31'),(2,'Masoud Barzani','')]
        for ordinal,name,gate in candidates:
            body=f'set_variable = {{ {P}install_{kind} = {ordinal} }}\n'
            if kind=='baath':body+='set_country_flag = COLDWAR_IRQ_baath_alternate_succession\n'+('set_country_flag = COLDWAR_IRQ_bakr_retained\n' if ordinal==0 else 'clr_country_flag = COLDWAR_IRQ_bakr_retained\n')
            body+='COLDWAR_IRQ_set_leader = yes'
            opts.append(opt('Agree the mandate of '+name,body,gate))
        return menu('A leadership settlement','The senior leadership must settle the distribution of national authority. Continuity offers familiar loyalties, while a new mandate would give another figure responsibility for the government and its programme.',opts)
    for key in ['baath_succession','baath_continuity_cabinet','bakr_power_settlement','bakr_retire']:register(key,succession('baath'))
    register('kdp_succession_vote',succession('kdp'))
    register('puk_kdp_offer',menu('Regional cooperation','The KDP and PUK delegates may cooperate without merging parties or transferring government. A paid constitutional working group requires their acceptance.',[opt('Both delegations accept a joint working group.',paid('kdp_puk',.01,'set_country_flag = COLDWAR_IRQ_kdp_puk_pact\n'+sync(),gate='has_country_flag = COLDWAR_IRQ_puk_formed',once=True),'has_country_flag = COLDWAR_IRQ_puk_formed'),opt('The KDP delegation refuses.','add_stability = -0.01')]))

    # Bilateral offers: pending flags expire, acceptance rechecks sender authority,
    # frozen invoice, recipient treasury/stockpile and current peace. No auto-consent.
    credit_contracts=[]
    def international(key,targets,kind='cooperation',flag=None,share=.01):
        choices=[];d=decs[key]
        for tag in targets:
            k=key+'_'+tag;pending=P+'offer_'+k;accepted=P+'accepted_'+k
            irqgate=dg(key)+f'\nhas_country_flag = {pending}\nNOT = {{ has_country_flag = {accepted} }}\ncountry_exists = {tag}\nNOT = {{ has_war_with = {tag} }}'
            fee=share
            if kind=='loan':fee=.05
            elif kind=='arms':fee=.01
            accept_gate=f'tag = {tag}\nIRQ = {{ {irqgate} }}'
            if kind=='loan':accept_gate+='\nNOT = { has_country_flag = MD_skip_treasury_cost }\n'+check('treasury','IRQ.'+P+'D_'+k+'_invoice')+f'\nIRQ = {{ has_country_flag = {P}D_{k}_quoted check_variable = {{ {P}D_{k}_invoice > 0 }} check_variable = {{ gdp_total > 0 }} NOT = {{ has_country_flag = MD_skip_treasury_cost }} }}'
            else:accept_gate+='\nIRQ = { '+cashgate(k)+' }'
            if kind in ['development','concession','grant','oil_contract']:accept_gate+='\nNOT = { has_country_flag = MD_skip_treasury_cost }'
            if kind=='concession':
                # The accepted contract now promises a physical improvement.
                # Check its actual authored state/type/count before either
                # treasury changes. Infrastructure uses its own state cap,
                # so the native non-shared-slot form has no include_locked.
                state,building,level=nodes[P+'oil_concession_delivery']['building']
                assert building=='infrastructure',('Concession capacity API changed',building)
                accept_gate+=f'\nIRQ = {{ {state} = {{ is_owned_and_controlled_by = IRQ free_building_slots = {{ building = {building} size > {level-1} }} }} }}'
            if kind=='arms':accept_gate+='\nhas_equipment = { infantry_weapons_1 > 999 }'
            payload=f'clr_country_flag = {pending}\nset_country_flag = {accepted}\n'
            if flag:payload+='set_country_flag = '+flag+'\n'
            if kind=='loan':
                principal=P+'principal_'+k;credit_contracts.append((k,tag,principal))
                payload+=f'COLDWAR_IRQ_reconcile_contract_credit = yes\nset_temp_variable = {{ COLDWAR_IRQ_gulf_other_debt_change = {P}D_{k}_invoice }}\nCOLDWAR_IRQ_gulf_change_other_debt = yes\nset_temp_variable = {{ treasury_change = COLDWAR_IRQ_gulf_other_debt_applied }}\nmodify_treasury_effect = yes\nset_variable = {{ {principal} = COLDWAR_IRQ_gulf_other_debt_applied }}\n'
                partnerpay=pay_var('IRQ.'+P+'D_'+k+'_invoice')
            else:
                payload+=pay_var(P+'D_'+k+'_invoice')+'\n';partnerpay=''
                if kind in ['development','concession','grant','oil_contract']:partnerpay=f'set_temp_variable = {{ treasury_change = IRQ.{P}D_{k}_invoice }}\nmodify_treasury_effect = yes'
            if kind=='exchange':payload+='add_timed_idea = { idea = COLDWAR_IRQ_technical_exchange days = 365 }\n'
            if kind=='advisers':payload+='add_timed_idea = { idea = COLDWAR_IRQ_advisers days = 180 }\n'
            if kind=='advisers' and key=='defence_diversified_offer':
                bonus=P+'diversified_artillery_instruction'
                L(bonus,'Iraqi Artillery Instruction')
                payload+=block('if',block('limit','NOT = { has_country_flag = COLDWAR_IRQ_diversified_artillery_instruction_delivered }')+
                    'add_tech_bonus = { name = '+bonus+' bonus = 0.25 uses = 1 category = CAT_artillery }\nset_country_flag = COLDWAR_IRQ_diversified_artillery_instruction_delivered')
            if kind=='border':
                payload+='set_country_flag = COLDWAR_IRQ_border_accepted\n'
                partnerpay+='\nset_country_flag = COLDWAR_IRQ_border_partner\nadd_ideas = COLDWAR_IRQ_border_navigation'
            if kind=='syria':partnerpay+='\nset_country_flag = COLDWAR_IRQ_syria_charter_partner'
            if kind=='concession':partnerpay+='\nset_country_flag = COLDWAR_IRQ_oil_concession_partner'
            if kind=='arms':partnerpay+='\nsend_equipment = { equipment = infantry_weapons_1 amount = 1000 target = IRQ }'
            if kind=='oil_contract':
                for other in ['ENG','USA','FRA']:
                    payload+=f'clr_country_flag = COLDWAR_IRQ_oil_export_contract_{other}\nclr_country_flag = COLDWAR_IRQ_accepted_oil_contract_review_{other}\nclr_country_flag = COLDWAR_IRQ_offer_oil_contract_review_{other}\n'
                payload+=f'set_country_flag = {{ flag = COLDWAR_IRQ_oil_export_contract_{tag} days = 365 value = 1 }}\nset_country_flag = {accepted}\nclr_country_flag = {P}D_{k}_quoted\nremove_ideas = COLDWAR_IRQ_current_export_contract\nadd_timed_idea = {{ idea = COLDWAR_IRQ_current_export_contract days = 365 }}\n'
            payload+=f'add_opinion_modifier = {{ target = {tag} modifier = COLDWAR_IRQ_agreement_opinion }}\n'+sync()
            accept=f'if = {{ limit = {{ {accept_gate} }}\n{partnerpay}\nIRQ = {{ {payload} }}\nadd_opinion_modifier = {{ target = IRQ modifier = COLDWAR_IRQ_agreement_opinion }}\n}}'
            refusal=f'IRQ = {{ clr_country_flag = {pending} add_opinion_modifier = {{ target = {tag} modifier = COLDWAR_IRQ_refused_opinion }} }}'
            # IMPERIA CW — Cold War: agreement narratives leave numeric terms in option effects.
            terms={
                'cooperation':'Baghdad proposes a formal channel for cooperation between our governments. The arrangement would give officials a common basis for further talks while leaving each government responsible for the commitments it accepts.',
                'syria':'Baghdad proposes a conference on closer Syrian-Iraqi cooperation. Acceptance would allow the two governments to develop a common charter and examine the institutions through which their competing claims to Arab leadership might be reconciled.',
                'development':'Baghdad offers financial support for an agreed programme of cooperation. Our ministers must judge whether the proposed assistance serves national priorities and whether a closer working relationship with Iraq is desirable.',
                'loan':'Baghdad requests a loan to finance its government programme. Acceptance would commit our treasury as Iraq\'s creditor, with the expectation that the funds will be repaid under the agreed terms.',
                'exchange':'Baghdad requests a technical exchange involving Iraqi specialists and our own institutions. The programme would support practical instruction and professional contacts, with Iraq meeting the agreed expenses.',
                'advisers':'Baghdad requests an advisory mission to assist its armed forces. Our officers would provide instruction under an agreed Iraqi funding commitment, while the Iraqi command retains responsibility for its forces.',
                'border':'Baghdad proposes a reciprocal arrangement for frontier consultation and river navigation. Our government must decide whether the terms provide a sound basis for managing disputes and maintaining working relations along the border.',
                'concession':'Baghdad proposes revised terms for the Iraqi oil concession. The settlement would define a continuing commercial relationship and provide support for the associated Iraqi infrastructure programme.',
                'arms':'Baghdad requests an infantry-arms shipment from our existing stores. The proposed sale would supply Iraqi units under an agreed payment, committing equipment that our own forces may also require.',
                'oil_contract':'Baghdad proposes a renewed oil-export contract. The agreement would give Iraqi exporters a dependable commercial channel for the coming year, with a contracting payment and continuing obligations for Iraqi revenue administration.',
                'grant':'Baghdad offers financial assistance for an agreed public programme. Our ministers must decide whether the proposal meets the country\'s needs and provides a useful basis for cooperation.',
            }[kind]
            response=event(d['label'],terms,[
                opt('Ratify the agreement.',accept,accept_gate,60),opt('Decline the proposed commitment.',refusal)],gate=f'tag = {tag} country_exists = IRQ IRQ = {{ has_country_flag = {pending} }}')
            request=quote(k,fee)+f'set_country_flag = {{ flag = {pending} days = 60 }}\n{tag} = {{ {response} }}'
            gate=f'country_exists = {tag}\nNOT = {{ has_war_with = {tag} }}\nNOT = {{ has_country_flag = {pending} }}\nNOT = {{ has_country_flag = {accepted} }}'
            choices.append(opt('Send the negotiated offer to '+tag+'.',request,gate))
        register(key,menu(d['label'],'The cabinet must select a government to approach. Its delegation will consider the proposed terms before either country undertakes the commitment.',choices))
    specs=[
      ('bakr_soviet_offer',['SOV'],'cooperation',None),('bakr_syria_offer',['SYR'],'syria',P+'syria_charter_accepted'),
      ('arab_development_offer',['EGY','SYR'],'development',P+'arab_compact_accepted'),('arab_support_offer',['PAL'],'development',None),
      ('arab_union_offer',['EGY','SYR'],'cooperation',P+'arab_compact_accepted'),('icp_soviet_exchange',['SOV'],'exchange',None),
      ('civic_credit_offer',['ENG','USA','SOV'],'loan',None),('royal_jordan_offer',['JOR'],'cooperation',None),('royal_trade_offer',['JOR','ENG'],'cooperation',None),
      ('foreign_partner_offer',['SOV','USA','ENG','FRA'],'cooperation',None),('foreign_shatt_offer',['PER'],'border',None),
      ('foreign_syria_offer',['SYR'],'cooperation',None),('foreign_kuwait_offer',['KUW'],'cooperation',None),('foreign_arab_conference',['EGY','SYR','JOR'],'cooperation',None),
      ('dawa_iran_offer',['PER'],'border',None),('sciri_border_offer',['PER'],'border',None),('sciri_aid_offer',['PER'],'loan',None),
      ('iip_arab_offer',['JOR','EGY'],'cooperation',None),('oil_concession_offer',['ENG'],'concession',P+'oil_concession_accepted'),
      ('oil_contract_review',['ENG','USA','FRA'],'oil_contract',None),('industry_credit',['SOV','USA','ENG'],'loan',None),
      ('agri_water_offer',['TUR','SYR'],'cooperation',None),('defence_soviet_advisers',['SOV'],'advisers',None),('iran_supplier',['SOV','USA','FRA'],'arms',None),
      ('defence_diversified_offer',['FRA','ENG'],'advisers',None),
    ]
    for key,targets,kind,flag in specs:international(key,targets,kind,flag)

    # Unknown native repayments can retire named debt without identifying a
    # creditor. Consume the Gulf ledger's monotonic counter before reborrowing,
    # conservatively reducing claims once without fabricating creditor cash.
    reconcile='COLDWAR_IRQ_gulf_reconcile_debt = yes\nset_temp_variable = { COLDWAR_IRQ_credit_retirement_delta = COLDWAR_IRQ_gulf_other_retirement_total }\nsubtract_from_temp_variable = { COLDWAR_IRQ_credit_retirement_delta = COLDWAR_IRQ_credit_retirement_seen }\n'
    for _,_,principal in sorted(credit_contracts):
        row=f'set_temp_variable = {{ COLDWAR_IRQ_credit_retire = {principal} }}\nif = {{ limit = {{ check_variable = {{ COLDWAR_IRQ_credit_retire > COLDWAR_IRQ_credit_retirement_delta }} }} set_temp_variable = {{ COLDWAR_IRQ_credit_retire = COLDWAR_IRQ_credit_retirement_delta }} }}\nsubtract_from_variable = {{ {principal} = COLDWAR_IRQ_credit_retire }}\nsubtract_from_temp_variable = {{ COLDWAR_IRQ_credit_retirement_delta = COLDWAR_IRQ_credit_retire }}'
        reconcile+=block('if',block('limit',f'check_variable = {{ COLDWAR_IRQ_credit_retirement_delta > 0 }} check_variable = {{ {principal} > 0 }}')+row)
    reconcile+='set_variable = { COLDWAR_IRQ_credit_retirement_seen = COLDWAR_IRQ_gulf_other_retirement_total }'
    E('reconcile_contract_credit',reconcile)

    # Gulf principal is owned by gulf_module; do not create a parallel war ledger.
    gulfmenu=menu('Gulf credit','Choose an actual creditor. Its existing Gulf-finance offer freezes the approved amount and requires that creditor’s acceptance. The active Iran-war condition remains authoritative.',[
      opt('Request Kuwait’s war credit.','COLDWAR_IRQ_gulf_unlock_credit = yes\nCOLDWAR_IRQ_gulf_offer_KUW = yes','country_exists = KUW has_war_with = PER'),
      opt('Request Saudi war credit.','COLDWAR_IRQ_gulf_unlock_credit = yes\nCOLDWAR_IRQ_gulf_offer_SAU = yes','country_exists = SAU has_war_with = PER'),
      opt('Request Emirati war credit.','COLDWAR_IRQ_gulf_unlock_credit = yes\nCOLDWAR_IRQ_gulf_offer_UAE = yes','country_exists = UAE has_war_with = PER')])
    for key in ['gulf_credit','iran_gulf_credit']:register(key,gulfmenu,'has_war_with = PER')
    repayopts=[opt('Repay the named '+tag+' war principal.','COLDWAR_IRQ_gulf_repay_'+tag+' = yes','COLDWAR_IRQ_gulf_can_repay_'+tag+' = yes') for tag in ['KUW','SAU','UAE']]
    for k,tag,principal in credit_contracts:
        amount=P+'repayment_'+k
        payload=f'COLDWAR_IRQ_reconcile_contract_credit = yes\nset_variable = {{ {amount} = gdp_total }}\nmultiply_variable = {{ {amount} = 0.02 }}\n'
        for ceiling in [principal,'COLDWAR_IRQ_gulf_other_debt','debt','treasury']:
            payload+=f'if = {{ limit = {{ check_variable = {{ var = {amount} value = {ceiling} compare = greater_than }} }} set_variable = {{ {amount} = {ceiling} }} }}\n'
        payload+=f'if = {{ limit = {{ check_variable = {{ {amount} > 0 }} }}\nset_temp_variable = {{ COLDWAR_IRQ_gulf_other_debt_change = {amount} }}\nmultiply_temp_variable = {{ COLDWAR_IRQ_gulf_other_debt_change = -1 }}\nCOLDWAR_IRQ_gulf_change_other_debt = yes\nset_variable = {{ {amount} = COLDWAR_IRQ_gulf_other_debt_applied }}\nmultiply_variable = {{ {amount} = -1 }}\n'+pay_var(amount)+f'\nsubtract_from_variable = {{ {principal} = {amount} }}\n{tag} = {{ set_temp_variable = {{ treasury_change = IRQ.{amount} }} modify_treasury_effect = yes }}\n}}'
        # IMPERIA CW — Cold War: repayment labels identify the public purpose of the loan.
        purpose={'civic_credit_offer':'parliamentary loan','sciri_aid_offer':'reconstruction loan','industry_credit':'industrial development loan'}[k.rsplit('_',1)[0]]
        repayopts.append(opt('Repay the '+tag+' '+purpose+'.',payload,f'country_exists = {tag} NOT = {{ has_country_flag = MD_skip_treasury_cost }} {tag} = {{ NOT = {{ has_country_flag = MD_skip_treasury_cost }} }} check_variable = {{ {principal} > 0 }} check_variable = {{ COLDWAR_IRQ_gulf_other_debt > 0 }} check_variable = {{ debt > 0 }} check_variable = {{ treasury > 0 }}'))
    # IMPERIA CW — Cold War: retained fiscal and diplomatic consultations use institutional prose.
    repaymenu=menu('Credit accounts','The treasury can retire part of its outstanding foreign borrowing. Each repayment is limited to the debt still owed, the funds available and 2% of current GDP, with the payment returned to the lending government.',repayopts)
    for key in ['saddam_repay','industry_repay','foreign_credit_review']:register(key,repaymenu)
    register('war_debt_conference','COLDWAR_IRQ_gulf_request_kuwait_forgiveness = yes','COLDWAR_IRQ_gulf_postwar = yes')

    # Paid readiness and the finite Iranian campaign contracts.
    readiness_extra='NOT = { has_idea = COLDWAR_IRQ_readiness_cycle } NOT = { has_country_flag = COLDWAR_IRQ_D_readiness_cycle_cooldown }'
    register('defence_readiness_cycle',paid('readiness_cycle',.005,'add_timed_idea = { idea = COLDWAR_IRQ_readiness_cycle days = 90 }\nset_country_flag = { flag = COLDWAR_IRQ_D_readiness_cycle_cooldown days = 180 value = 1 }',readiness_extra), readiness_extra+'\n'+cashgate('readiness_cycle'),cooldown=180)
    direct_quote_actions.append(('defence_readiness_cycle','readiness_cycle',.005,readiness_extra))
    for key in ['iran_opening','iran_followup','iran_disarray']:
        d=decs[key];extra='';payload=d['effect_code']
        if key=='iran_opening':extra='has_war_with = PER has_country_flag = COLDWAR_IRQ_iran_campaign_window_open NOT = { has_country_flag = COLDWAR_IRQ_iran_opening_used } has_country_flag = COLDWAR_IRQ_iran_launch_campaign_implemented'
        elif key=='iran_followup':
            extra='has_war_with = PER has_country_flag = { flag = COLDWAR_IRQ_iran_current_war_start days > 89 } NOT = { has_idea = COLDWAR_IRQ_iran_opening_offensive } NOT = { has_idea = COLDWAR_IRQ_iran_sustained_offensive } NOT = { has_idea = COLDWAR_IRQ_iran_followup_offensive } NOT = { has_idea = COLDWAR_IRQ_iran_followup_bill } NOT = { has_country_flag = COLDWAR_IRQ_D_iran_followup_cooldown }'
            payload+='\nset_country_flag = { flag = COLDWAR_IRQ_D_iran_followup_cooldown days = 180 value = 1 }'
        else:extra='country_exists = PER PER = { OR = { has_civil_war = yes has_stability < 0.40 } } NOT = { has_country_flag = COLDWAR_IRQ_iran_disarray_used }'
        register(key,paid(key,d['budget_gdp_share'],payload,extra,once=not d.get('repeatable',False)),extra+'\n'+cashgate(key))
        direct_quote_actions.append((key,key,d['budget_gdp_share'],extra))
    E('refresh_decision_quotes','\n'.join(block('if',block('limit',dg(key)+'\n'+extra)+quote(k,share)) for key,k,share,extra in direct_quote_actions))
    revoke='clr_country_flag = COLDWAR_IRQ_border_accepted\nif = { limit = { country_exists = PER } PER = { clr_country_flag = COLDWAR_IRQ_border_partner remove_ideas = COLDWAR_IRQ_border_navigation add_opinion_modifier = { target = IRQ modifier = COLDWAR_IRQ_refused_opinion } } }\n'+sync()
    E('revoke_actual_iran_settlement',revoke)
    register('iran_revoke_settlement','COLDWAR_IRQ_revoke_actual_iran_settlement = yes','COLDWAR_IRQ_border_settlement_active = yes')

    # Existing diplomatic/sanctions interfaces remain player-owned; actual Iraqi
    # sanctions can be lifted only by the sanctioning country's response.
    sancgate='OR = { is_in_array = { array = IRQ.imp_dip_sanc_on_us value = THIS } is_in_array = { array = IRQ.imp_fin_sanc_on_us value = THIS } is_in_array = { array = IRQ.imp_eco_sanc_on_us value = THIS } is_in_array = { array = IRQ.imp_mil_sanc_on_us value = THIS } }'
    lift=[]
    for typ in ['dip','fin','eco','mil']:
        lift.append(f'remove_from_array = {{ array = imp_{typ}_sanc_by_us value = IRQ }}\nIRQ = {{ remove_from_array = {{ array = imp_{typ}_sanc_on_us value = PREV }} remove_opinion_modifier = {{ target = PREV modifier = opinion_{typ}_sanctioned_us }} }}')
    lift.append('IMP_sanctions_refresh_world = yes')
    sancresponse=event('Iraqi sanctions review','Baghdad has asked our government to reconsider its sanctions. Ministers must weigh the reasons for maintaining pressure against the diplomatic and commercial value of reopening relations.',[opt('Lift our own sanctions.','\n'.join(lift),sancgate),opt('Maintain the sanctions.')],gate='country_exists = IRQ\n'+sancgate)
    register('war_sanctions_diplomacy',block('every_other_country',block('limit',sancgate)+sancresponse),'OR = { check_variable = { imp_dip_sanc_on_us^num > 0 } check_variable = { imp_fin_sanc_on_us^num > 0 } check_variable = { imp_eco_sanc_on_us^num > 0 } check_variable = { imp_mil_sanc_on_us^num > 0 } }')

    # Explicit target war authority grants a goal, never declares automatically.
    waropts=[]
    for tag,state in [('PER',399),('KUW',172),('SYR',554)]:
        gate=f'country_exists = {tag}\nNOT = {{ has_war_with = {tag} }}\nNOT = {{ is_in_faction_with = {tag} }}\n{state} = {{ is_claimed_by = IRQ is_owned_by = {tag} }}'
        waropts.append(opt('Authorize the claimed-state proposal against '+tag+'.',f'create_wargoal = {{ type = take_state_focus target = {tag} generator = {{ {state} }} expire = 180 }}',gate))
    register('war_authorization',menu('Specific war authority','The cabinet must decide whether Iraq\'s territorial claims justify preparations for military action. Authorization gives the government 180 days to pursue the selected objective; a declaration of war remains a separate decision.',waropts))
    mediation=[];mediation_pending=[]
    medsource=block('OR',block('AND',dg('war_mediation'))+block('AND',dg('iran_war_aims')))
    for tag in ['PER','KUW','SYR']:
        pending=P+'mediation_pending_'+tag;mediation_pending.append((tag,pending))
        responsegate=f'tag = {tag} country_exists = IRQ has_war_with = IRQ IRQ = {{ has_country_flag = {pending}\n{medsource} }}'
        response=event('A bilateral ceasefire offer','Baghdad proposes peace on the basis of the existing territorial settlement. The two governments can conclude a separate peace when their conflict involves no other belligerents; a wider war will require negotiations that address the other participants.',[
          opt('Accept bilateral peace if no other participant is bound.',f'IRQ = {{ clr_country_flag = {pending} }}\nif = {{ limit = {{ has_war_with = IRQ NOT = {{ any_country = {{ has_war_with = IRQ NOT = {{ tag = {tag} }} }} }} NOT = {{ any_country = {{ has_war_with = {tag} NOT = {{ tag = IRQ }} }} }} }} white_peace = IRQ }}\nadd_opinion_modifier = {{ target = IRQ modifier = COLDWAR_IRQ_agreement_opinion }}'),opt('Refuse the proposed terms.',f'IRQ = {{ clr_country_flag = {pending} }}')],gate=responsegate)
        mediation.append(opt('Send a mediation proposal to '+tag+'.',f'set_country_flag = {{ flag = {pending} days = 30 value = 1 }}\n{tag} = {{ {response} }}',f'country_exists = {tag} has_war_with = {tag} NOT = {{ has_country_flag = {pending} }}'))
    mediation += [opt('Continue the existing war plan without a new subsidy.','COLDWAR_IRQ_reconcile_programmes = yes','has_war = yes'),opt('Fund another eligible Iranian offensive.','COLDWAR_IRQ_do_iran_followup = yes',dg('iran_followup')+'\nhas_war_with = PER NOT = { has_idea = COLDWAR_IRQ_iran_followup_bill }')]
    mediated=menu('War aims and mediation','The government must judge whether the military position still serves its political objectives. Ministers can seek a negotiated end to the fighting or continue the campaign, while any peace proposal must be accepted by the opposing government.',mediation)
    for key in ['war_mediation','iran_war_aims']:register(key,mediated)
    register('war_emergency_review',menu('Remaining emergency measures','Only emergency programme selections are suspended. Permanent national development and fixed-duration personnel invoices remain delivered/payable.',[opt('Return to the civilian budget.', 'set_country_flag = COLDWAR_IRQ_emergency_ended\n'+sync())]),'has_war = no')
    register('iran_policy_review',menu('Iran policy dossier','An actual Iranian regime change or a published player dossier is needed. Negotiation, deterrence and a separately authorized war remain distinct choices.',[
      opt('Publish the current diplomatic dossier.','set_country_flag = COLDWAR_IRQ_iran_rp_dossier\nadd_timed_idea = { idea = COLDWAR_IRQ_negotiation_cost days = 60 }'),
      opt('Prepare a negotiated river settlement.',f'{P}do_foreign_shatt_offer = yes','has_country_flag = COLDWAR_IRQ_decision_foreign_shatt_offer_unlocked OR = { has_country_flag = COLDWAR_IRQ_iran_regime_changed has_country_flag = COLDWAR_IRQ_iran_rp_dossier }'),
      opt('Retain a policy of deterrence.',paid('iran_deterrence',.01,'add_timed_idea = { idea = COLDWAR_IRQ_advisers days = 90 }'),'OR = { has_country_flag = COLDWAR_IRQ_iran_regime_changed has_country_flag = COLDWAR_IRQ_iran_rp_dossier }')]))

    # Reports read actual native values; they do not grant dummy rewards.
    incident=[]
    for tag in ['PER','SYR','KUW','JOR','SAU','TUR']:
        pending=P+'incident_review_'+tag
        reply=event('An Iraqi incident-review request','Iraq asks your government to review a recorded frontier or diplomatic incident. You retain control of the response; no territory or war status changes.',[opt('Accept a reciprocal incident channel.',f'IRQ = {{ clr_country_flag = {pending} add_opinion_modifier = {{ target = {tag} modifier = COLDWAR_IRQ_agreement_opinion }} }}\nadd_opinion_modifier = {{ target = IRQ modifier = COLDWAR_IRQ_agreement_opinion }}'),opt('Reject the proposed channel.',f'IRQ = {{ clr_country_flag = {pending} add_opinion_modifier = {{ target = {tag} modifier = COLDWAR_IRQ_refused_opinion }} }}')],gate=f'tag = {tag} country_exists = IRQ IRQ = {{ {dg("foreign_incident_review")} has_country_flag = {pending} }}')
        incident.append(opt('Request '+tag+' participation.',f'set_country_flag = {{ flag = {pending} days = 30 value = 1 }}\n{tag} = {{ {reply} }}',f'country_exists = {tag} NOT = {{ has_country_flag = {pending} }}'))
    register('foreign_incident_review',menu('Reciprocal incident channels','Both states receive a response opportunity. Choose an actual neighbouring government; it may accept a channel or refuse without an automatic territorial or military consequence.',incident))
    reportkeys=['oil_market_review','industry_pipeline','society_audit','iran_frontier_review']
    for key in reportkeys:
        options=[]
        if key=='industry_pipeline':
            for n in data['nodes']:
                if n['group']=='industry':options.append(opt('Retry the funded project: '+n['title'],P+'apply_'+n['key']+' = yes',f'has_country_flag = {n["id"]}_pending'))
        if key=='iran_frontier_review':
            options += [opt('Iran has an active civil conflict.','','country_exists = PER PER = { has_civil_war = yes }'),opt('Iranian stability is below 40%.','','country_exists = PER PER = { has_stability < 0.40 }'),opt('Iranian forces currently face Iraq in war.','','has_war_with = PER'),opt('Khuzestan is still Iranian-owned.','','399 = { is_owned_by = PER }')]
        register(key,menu(decs[key]['label'],'Native accounts: GDP $[?gdp_total|2]bn; treasury $[?treasury|2]bn; debt $[?debt|2]bn. This review reads live native data and current conditions. It neither fixes the world oil price nor resets literacy or construction. Conditions and eligible pending projects are listed below.',options))

    # Starting opposition organization uses registered native slots, then the
    # normal array normalization. No decision installs a government.
    outlooks={'western':[2,3],'emerging':[4,6,8,9],'nonaligned':[12,18,19],'nationalist':[21,22,23]}
    for outlook,slots in outlooks.items():
        opts=[]
        for slot in slots:
            gate='always = yes'
            if slot==9:gate='has_country_flag = COLDWAR_IRQ_sciri_formed'
            if slot==19:gate='has_country_flag = COLDWAR_IRQ_puk_formed'
            opts.append(opt('Organize '+PARTIES[slot][0]+'.',f'set_variable = {{ {P}organization_{outlook}_party = {slot} }}\nset_country_flag = {P}organization_{outlook}_running',gate))
        # IMPERIA CW — Cold War: party organization is described as a political campaign.
        register('organize_'+outlook,menu('Organize the '+outlook+' outlook','A 90-day organizing campaign will bring party representatives into workplaces, neighbourhoods and provincial associations. The selected organization will use those contacts to build public support for its programme and the wider political current it represents.',opts),f'NOT = {{ has_country_flag = {P}organization_{outlook}_running }}')
        finished=f'set_temp_variable = {{ party_index = {P}organization_{outlook}_party }}\nset_temp_variable = {{ party_popularity_increase = 0.03 }}\nset_temp_variable = {{ temp_outlook_increase = 0.03 }}\nchange_relative_party_popularity = yes\nset_temp_variable = {{ temp_outlook_increase = 0 }}\nclr_country_flag = {P}organization_{outlook}_running\nclear_variable = {P}organization_{outlook}_party'
        organization_ticks.append(block('if',block('limit',f'has_country_flag = {{ flag = {P}organization_{outlook}_running days > 89 }}')+finished))

    # Root owns the start-wide per-node pending retry selector; do not duplicate it.
    handled.add('retry_pending')
    missing=set(decs)-handled
    if missing:raise ValueError('Unimplemented approved decision providers: '+', '.join(sorted(missing)))
    cleanup='\n'.join(f'if = {{ limit = {{ NOT = {{ has_war_with = {tag} }} }} clr_country_flag = {pending} }}' for tag,pending in mediation_pending)
    for terms in ['revenue','central']:
        cleanup+='\n'+block('if',block('limit','NOT = { has_country_flag = '+P+'north_offer_'+terms+' }')+'clr_country_flag = '+P+'D_north_'+terms+'_quoted\n'+'\n'.join('clr_country_flag = '+P+'north_'+terms+'_accepted_'+tag for tag in ['KUR','PUK']))
    oilvalid=[]
    for tag in ['ENG','USA','FRA']:
        live=f'has_country_flag = COLDWAR_IRQ_oil_export_contract_{tag} country_exists = {tag} NOT = {{ has_war_with = {tag} }}'
        oilvalid.append(block('AND',live))
        cleanup+=f'\nif = {{ limit = {{ NOT = {{ {live} }} }} clr_country_flag = COLDWAR_IRQ_oil_export_contract_{tag} clr_country_flag = COLDWAR_IRQ_accepted_oil_contract_review_{tag} }}'
    cleanup+='\n'+block('if',block('limit',block('NOT',block('OR','\n'.join(oilvalid))))+'remove_ideas = COLDWAR_IRQ_current_export_contract')
    E('decision_tick','COLDWAR_IRQ_reconcile_contract_credit = yes\nCOLDWAR_IRQ_reconcile_historical_roster = yes\nCOLDWAR_IRQ_finalize_north_terms = yes\nCOLDWAR_IRQ_reconcile_political_contracts = yes\nif = { limit = { has_war_with = PER } clr_country_flag = COLDWAR_IRQ_border_accepted if = { limit = { country_exists = PER } PER = { clr_country_flag = COLDWAR_IRQ_border_partner remove_ideas = COLDWAR_IRQ_border_navigation } } }\n'+'\n'.join(organization_ticks)+'\n'+cleanup+'\nCOLDWAR_IRQ_refresh_decision_quotes = yes\n'+sync())
    category=P+'1970_decisions'
    L(category,'Iraqi National Programme');L(category+'_desc','Political mandates, domestic guarantees, funded projects and recipient-owned international agreements. Current government and contract eligibility remain binding.')
    opinion='opinion_modifiers = {\nCOLDWAR_IRQ_agreement_opinion = { value = 25 decay = 1 }\nCOLDWAR_IRQ_refused_opinion = { value = -15 decay = 1 }\n}\n'
    # Recheck source government/unlock at BOTH option visibility and execution.
    # Recipient-owned foreign callbacks already carry their explicit IRQ gate.
    rendered_events=[]
    for source in events:
        ast=parse(source);body=first(ast,'country_event');eid=first(body,'id')
        providers=event_authority.get(eid,[])
        if True:
            authority=providers[0] if len(providers)==1 else (block('OR','\n'.join(block('AND',v) for v in providers)) if providers else '')
            ar=first(body,'trigger',[])+parse(authority);new=[]
            for k,o,v in body:
                if k!='option':new.append((k,o,v));continue
                metadata=[(a,b,c) for a,b,c in v if a in ['name','ai_chance']]
                original=first(v,'trigger',[])
                actions=[(a,b,c) for a,b,c in v if a not in ['name','ai_chance','trigger']]
                if actions:
                    v=metadata+[('trigger','=',original+ar),('if','=',[('limit','=',original+ar)]+actions)]
                new.append((k,o,v))
            source=emit([('country_event','=',new)])+'\n'
        rendered_events.append(source)
    from prison_review import apply as apply_prison_review_contract
    return apply_prison_review_contract({
      'common/decisions/categories/COLDWAR_IRQ_1970_decisions.txt':block(category,'icon = GFX_decision_category_generic_political_actions\n'+block('allowed','original_tag = IRQ')+block('visible','COLDWAR_IRQ_campaign_active = yes')),
      'common/decisions/COLDWAR_IRQ_1970_decisions.txt':block(category,'\n'.join(decision_blocks)),
      'common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt':'\n'.join(effects),
      'common/scripted_triggers/COLDWAR_IRQ_1970_decision_triggers.txt':'\n'.join(triggers),
      'common/ideas/COLDWAR_IRQ_1970_decision_ideas.txt':block('ideas',block('country','\n'.join(ideas))),
      'common/opinion_modifiers/COLDWAR_IRQ_1970_decision_opinions.txt':opinion,
      'interface/COLDWAR_IRQ_1970_decision_ideas.gfx':block('spriteTypes','\n'.join(gfx)),
      'events/COLDWAR_IRQ_1970_decisions.txt':'add_namespace = COLDWAR_IRQ_decision_events\n\n'+'\n'.join(rendered_events),
      'localisation/english/COLDWAR_IRQ_1970_decisions_l_english.yml':'l_english:\n# IMPERIA CW — Cold War: iraq 1970 English localisation.\n'+'\n'.join(locline(k,v) for k,v in loc.items())+'\n',
    })
