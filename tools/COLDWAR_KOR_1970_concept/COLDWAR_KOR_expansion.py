# IMPERIA CW — Cold War: researched second concept revision, no runtime installation.
"""Add92 focus designs, including36 institutional transition focuses.

Called after reviewed base refinement and before native recipe declaration.
Historical and mechanical research was completed before authoring this module.
"""
from copy import deepcopy
P='COLDWAR_KOR_'

def expand(d,parse_effects):
    base_count=len(d['nodes']);groups={g['id']:g for g in d['groups']}
    nodes={n['key']:n for n in d['nodes']}
    baseline={g['id']:sum(n['group']==g['id'] for n in d['nodes']) for g in d['groups']}
    d['revision']=2
    d['modifier_labels']['dockyard_productivity']='Commercial dockyard productivity'
    d['modifier_labels']['drift_defence_factor']='Ideological drift defence'

    def make(group,key,label,xy,fx,description,pre=(),owner=None,code=(),state=(),active=None,icon=None,days=35):
        g=groups[group];e=parse_effects(fx)
        # Civilian development uses actual MD civilian tax/GDP readers.
        for p in e['policies']:
            if group!='defence':
                value=p['modifiers'].pop('industrial_capacity_factory',0)+p['modifiers'].pop('production_factory_max_efficiency_factor',0)
                if value:p['modifiers']['civilian_factories_productivity']=round(value,5)
            p['qualified_slot']=group+':'+p['slot']
            if active:p['active_condition']=active;p['active_trigger']=active
        own=owner or g['ownership']
        n={'id':P+key,'key':key,'group':group,'label':label,'description':description,'xy':list(xy),
           'days':49 if e['buildings'] else days,'cost':7 if e['buildings'] else days/7,
           'prerequisites':[[P+x for x in row] for row in pre],'mutually_exclusive':[],
           'gate':g['gate'],'ownership':own,'effects':e,'icon_family':icon or g['icon'],
           'history':'research_democratic_transition_expansion.md; mechanics_expansion_research.md',
           'reference':'MD KOR two-column forks, Russia three-outcome policy rows; layout_expansion_research.md',
           'condition_code':list(code),'state_effects':list(state),'requirements':[],
           'available_if_capitulated':False,'cancel_if_invalid':True,'continue_if_invalid':False,
           'receipt_policy':'One-time outcomes never replay. Latest earned level replaces its qualified policy and expense slot.',
           'added_in_revision':2}
        if e['policies']:
            assert len(e['policies'])==1
            n['effects']['expense_commitment']={'slot':own+'|'+e['policies'][0]['qualified_slot'],
              'weekly_bn':e['weekly'],'operation':'replace; zero clears prior slot commitment',
              'active_condition':active or 'same actual owner as policy'}
        d['nodes'].append(n);nodes[key]=n;return n

    def pair(group,keys,labels,x,y,fx,descs,pre,**kw):
        a=make(group,keys[0],labels[0],(x-1,y),fx[0],descs[0],pre=pre,**kw)
        b=make(group,keys[1],labels[1],(x+1,y),fx[1],descs[1],pre=pre,**kw)
        a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']];return a,b

    # Extend each existing political programme in its own local footprint.
    # No long connector is drawn through the lower political tier.
    make('drp','drp_budget_charter','Development Accounts',(4,11),'cost:1;p:oversight:build=0.04,bureau=0.05',
      'Publish the development budget and subject credit guarantees to a defined approval process.',
      pre=[['dynastic_presidency','civilian_handover']],owner='leader:Park Chung Hee',icon='state')
    pair('drp',('drp_technocrats','drp_provincial_brokers'),('Technocratic Mandates','Provincial Bargains'),4,12,
      ('p:administrative_base:research=0.04,education=0.06,pp=-0.04;cost:1',
       'p:administrative_base:agri=0.08,stab=0.04,bureau=0.06;weekly:0.002'),
      ('Give the planners professional discretion while limiting presidential patronage.',
       'Trade central discretion for provincial cooperation and funded rural administration.'),[['drp_budget_charter']],owner='leader:Park Chung Hee')
    a,b=pair('ndp',('ndp_tax_transparency','ndp_tax_compromise'),('Transparent Taxation','A Taxpayer Compact'),12,9,
      ('p:revenue:interest=-0.25,bureau=0.05,pp=-0.04;cost:1',
       'p:revenue:civ=0.06,stab=0.03,interest=0.15'),
      ('Audit politically connected revenue arrangements; the review costs time and administrative resources.',
       'Preserve investment through negotiated taxation, accepting narrower fiscal discipline.'),[['democratic_conservatism']])
    make('ndp','ndp_municipal_services','Provincial Services',(12,10),'cost:2;b:607,infrastructure,1;p:local_admin:agri=0.04,bureau=0.04',
      'Fund provincial services and prepare local administration. Nationwide local elections are not claimed before1991.',pre=[['ndp_tax_transparency','ndp_tax_compromise']],icon='rural')
    make('reform','reform_party_accounts','Party Finance Rules',(23,9),'cost:1;p:party_finance:interest=-0.2,pp=-0.04,bureau=0.03',
      'Make reform-party financing accountable without granting popularity or selecting the election winner.',pre=[['democratic_alliance','reform_nordpolitik']],icon='oversight')
    make('reform','ys_civilian_contracts','Public Contract Rules',(19,10),'cost:1;p:ys_contracts:civ=0.06,bureau=0.04,pp=-0.03',
      'Use competitive contracts and disclosure to constrain the old patronage networks.',pre=[['reform_party_accounts']],owner='leader:Kim Young-sam',
      code=['has_country_leader = { name = "Kim Young-sam" ruling_only = yes }'],icon='oversight')
    make('reform','dj_social_dialogue','A Social Dialogue',(27,10),'p:dj_dialogue:stab=0.04,ic=0.03,social=0.08;weekly:0.002',
      'Bring employers, independent unions and excluded provinces into a funded social bargain.',pre=[['reform_party_accounts']],owner='leader:Kim Dae-jung',
      code=['has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }'],icon='labour')
    make('reform','reform_lawful_succession','Lawful Succession',(23,11),'p:succession:stab=0.04,pp=-0.04;action:bind_electoral_succession',
      'Bind the reform government to the same rules that made its accession possible. The other reform leader may govern later.',
      pre=[['ys_civilian_contracts','dj_social_dialogue']],code=['has_country_flag = '+P+'constitutional_order'],icon='elections')
    # Roh actually pursued Nordpolitik AND the1990 merger. They are not a real exclusion.
    for key,other in [('roh_nordpolitik','conservative_merger'),('conservative_merger','roh_nordpolitik')]:
        nodes[key]['mutually_exclusive']=[x for x in nodes[key]['mutually_exclusive'] if x!=P+other]
    make('army','army_constitutional_service','Constitutional Service',(34,11),'p:service_law:org=0.03,pp=-0.03,bureau=0.03',
      'Define the legal duties of the armed forces under the actual constitutional settlement.',pre=[['roh_nordpolitik','conservative_merger']],icon='army')
    pair('army',('army_civilian_ministry','army_advisory_council'),('A Civilian Ministry','An Advisory Council'),34,12,
      ('p:command_settlement:stab=0.05,org=-0.02,personnel=0.05;cost:1',
       'p:command_settlement:org=0.06,stab=-0.03,bureau=0.05;weekly:0.001'),
      ('Put ministerial appointments under lawful civilian authority; command adaptation has a short-run cost.',
       'Retain formal military advice while accepting a slower and politically contested civilianization.'),[['army_constitutional_service']],
      code=['has_country_flag = '+P+'constitutional_order'])
    pair('usp',('usp_national_wage_floor','usp_sectoral_bargaining'),('A National Wage Floor','Sectoral Bargaining'),4,23,
      ('p:wage_settlement:stab=0.05,ic=-0.03,social=0.06;cost:1',
       'p:wage_settlement:ic=0.04,stab=0.02,bureau=0.05;weekly:0.001'),
      ('Set an enforceable minimum floor, accepting costs in low-margin export firms.',
       'Negotiate sector agreements that suit different industries, accepting uneven coverage and administrative complexity.'),[['labour_republic']],icon='labour')
    make('minjung','student_workplace_alliance','Campus and Workplace',(10,19),'p:civic_training:research=0.03,education=0.05,pp=-0.04;cost:1',
      'Link civic education to actual workplace representation without claiming that workers form one party.',pre=[['student_cabinet_public_accounts']],owner='party:5',icon='students')
    make('minjung','left_public_procurement','Public Procurement',(16,19),'p:left_procurement:ic=0.05,bureau=0.05,interest=0.15;cost:1',
      'Give public enterprises accountable procurement instead of insider allocation.',pre=[['independent_left_public_accounts']],owner='party:19',icon='industry')
    make('minjung','civic_association_law','Civic Association Law',(13,20),'p:associations:research=0.02,pp=-0.03,bureau=0.04;action:legal_civic_associations',
      'Protect plural civic associations as a national legal institution that survives ordinary cabinet changes.',
      pre=[['student_workplace_alliance','left_public_procurement']],owner='national',
      code=['OR = { check_variable = { ruling_party = 5 } check_variable = { ruling_party = 19 } }'],
      active='has_country_flag = '+P+'constitutional_order',icon='parliament')
    pair('rpr',('rpr_worker_elections','rpr_production_cadres'),('Workplace Elections','Production Cadres'),23,22,
      ('p:workplace:ic=0.05,stab=0.03,pp=-0.05;cost:1',
       'p:workplace:ic=0.08,stab=-0.04,interest=0.2;cost:1'),
      ('Give workers an independent say in public enterprises, at a cost to central directive power.',
       'Concentrate production authority in party cadres, accepting legitimacy and credit costs.'),[['revolutionary_diplomacy']],icon='labour')
    pair('security',('security_due_process','security_protected_archives'),('Legal Warrants','Protected Archives'),34,22,
      ('p:legal_settlement:stab=0.04,research=0.02,intel=-0.04,bureau=0.04;action:warranted_security_operations',
       'p:legal_settlement:intel=0.1,stab=-0.05,police=0.06'),
      ('Subject operations to warrants and review. The institutional rules remain separate from this caretaker’s active programme.',
       'Retain extensive classified political files at the cost of public trust and police expenditure.'),[['security_handover']],icon='security')
    pair('kjp',('kjp_coalition_broker','kjp_independent_party'),('Coalition Brokerage','Independent Conservatives'),45,26,
      ('p:coalition_identity:pp=0.12,stab=-0.03,bureau=0.04',
       'p:coalition_identity:stab=0.05,civ=0.04,pp=-0.06;cost:1'),
      ('Trade a distinct party identity for influence inside a negotiated governing coalition.',
       'Preserve an independent conservative organization and accept reduced executive leverage.'),[['kjp_korean_policy']],owner='leader:Kim Jong-pil',icon='parliament')

    # National economy: a priority budget, not a claim that Korea could develop
    # only one of the three sectors historically.
    make('economy','sector_investment_review','Sector Investment',(45,15),'cost:1;action:sector_investment_priority',
      'Choose the next priority investment package. Other industries may still be built and researched normally.',pre=[['advanced_export_economy']],icon='industry')
    sector=[
      ('electronics_priority','Electronics Priority',43,'cost:3;p:sector:ic=0.05,research=0.03,education=0.07,workers=0.03;weekly:0.001',
       'Prioritize electronics and technical skills, accepting a demanding education budget and skilled-labor needs.',
       'electronics_capability','Electronics Capability','cost:2;p:sector:ic=0.08,research=0.04,education=0.1,workers=0.03;weekly:0.002',
       'Build absorptive capability for advanced components without granting a future technology or a free semiconductor plant.'),
      ('machinery_priority','Machinery Priority',45,'cost:3;p:sector:ic=0.07,build=0.03,interest=0.25,workers=0.03',
       'Prioritize machine tools and automotive suppliers at a capital and workforce cost.',
       'supplier_engineering','Supplier Engineering','cost:2;b:606,industrial_complex,1;p:sector:ic=0.1,build=0.04,interest=0.35,workers=0.04',
       'Fund a supplier-engineering complex and its continuing credit exposure.'),
      ('shipbuilding_priority','Shipbuilding Priority',47,'cost:3;p:sector:ic=0.03,workers=0.04,interest=0.2;weekly:0.001',
       'Prioritize commercial shipbuilding, accepting capital and labor demands.',
       'commercial_shipyards','Commercial Shipyards','cost:2;b:605,dockyard,1;p:sector:ic=0.05,workers=0.04,interest=0.3;weekly:0.002',
       'Fund commercial shipyard capacity. Commercial GDP productivity and naval production output remain different systems.'),
    ]
    sector_ids=[];ends=[]
    for key,label,x,fx,desc,end,title,efx,edesc in sector:
        a=make('economy',key,label,(x,16),fx,desc,pre=[['sector_investment_review']],icon='research' if x==43 else 'industry')
        b=make('economy',end,title,(x,17),efx,edesc,pre=[[key]],icon='research' if x==43 else ('navy' if x==47 else 'industry'))
        if x==47:
            a['effects']['policies'][0]['modifiers']['dockyard_productivity']=0.12
            b['effects']['policies'][0]['modifiers']['dockyard_productivity']=0.18
        sector_ids.append(a['id']);ends.append(end)
    for id in sector_ids:nodes[id.removeprefix(P)]['mutually_exclusive']=[x for x in sector_ids if x!=id]
    make('economy','industrial_quality_service','Industrial Standards',(45,18),'cost:1;p:standards:workers=-0.02,education=0.04,bureau=0.03',
      'Fund quality standards and vocational services across the chosen sector.',pre=[ends],icon='research')
    pair('economy',('urban_insurance_network','rural_insurance_network'),('Urban Social Insurance','Rural Social Insurance'),45,19,
      ('cost:2;p:social_network:stab=0.04,health=0.08,social=0.06,workers=-0.02;weekly:0.002;action:extend_social_insurance',
       'cost:2;p:social_network:agri=0.07,stab=0.03,health=0.06,bureau=0.04;weekly:0.001;action:extend_social_insurance'),
      ('Extend coverage to urban households outside large-company employment. Contributions and administrative costs remain real.',
       'Prioritize farming and fishing households, accepting a slower urban extension.'),[['industrial_quality_service']],icon='welfare')

    make('defence','yulgok_readiness_review','Yulgok Readiness',(54,12),'cost:1;xp:15;p:readiness_audit:org=0.02,personnel=0.03',
      'Review the modernization programme and the existing force. No starting divisions or equipment are created.',pre=[['coastal_logistics','air_command']],icon='army')
    defence=[
      ('air_cover_priority','Air Cover Priority',52,'cost:2;p:mission_priority:air_eff=0.06,equipment=0.06;weekly:0.001',
       'Prioritize coordinated air cover over spending on other service missions.',
       'aircrew_training','Aircrew Training','cost:1;p:mission_priority:air_eff=0.09,equipment=0.08,personnel=0.04;weekly:0.002'),
      ('escort_priority','Escort Priority',54,'cost:2;p:mission_priority:naval_org=0.08,supply=0.04,equipment=0.04;weekly:0.001',
       'Prioritize escorts and maritime coordination with a continuing operating burden.',
       'escort_staff','An Escort Staff','cost:1;p:mission_priority:naval_org=0.12,supply=0.05,equipment=0.06;weekly:0.002'),
      ('counterbattery_priority','Counter-Battery Fire',56,'cost:2;p:mission_priority:defence=0.05,attack=0.03,supply=0.05;weekly:0.001',
       'Prioritize land-fire coordination and survivability rather than a free artillery stockpile.',
       'fire_direction','Fire Direction','cost:1;p:mission_priority:defence=0.07,attack=0.04,supply=0.07;weekly:0.002'),
    ]
    choices=[];tails=[]
    for key,label,x,fx,desc,end,title,efx in defence:
        a=make('defence',key,label,(x,13),fx,desc,pre=[['yulgok_readiness_review']],icon='air' if x==52 else 'navy' if x==54 else 'army')
        make('defence',end,title,(x,14),efx,'Fund training and staff work for the chosen mission; technologies and equipment still follow the existing systems.',pre=[[key]],icon='training')
        choices.append(a['id']);tails.append(end)
    for id in choices:nodes[id.removeprefix(P)]['mutually_exclusive']=[x for x in choices if x!=id]
    make('defence','joint_readiness_audits','Joint Readiness Audits',(54,15),'cost:1;p:joint_audit:supply=-0.03,bureau=0.04;xp:15',
      'Audit readiness and logistics across all services, using the actual force rather than spawning formations.',pre=[tails],icon='oversight')

    make('foreign','overseas_commercial_service','Commercial Missions',(63,9),'cost:1;p:commercial_service:trade=0.04,bureau=0.04',
      'Create a professional service for overseas contracts and export standards.',pre=[['middle_power']],icon='diplomacy')
    a,b=pair('foreign',('middle_east_bids','pacific_standards'),('Middle Eastern Bids','Pacific Standards'),63,10,
      ('action:native_construction_contract_bids;p:commercial_orientation:trade=0.05,bureau=0.04;cost:1',
       'offer:pacific_trade_contacts;p:commercial_orientation:research=0.02,foreign_def=-0.03;cost:1'),
      ('Bid for construction work through actual partner contracts. No remittance or foreign payment is granted on dispatch.',
       'Prioritize technology-intensive Pacific markets while accepting dependence on external standards.'),[['overseas_commercial_service']],icon='diplomacy')
    make('foreign','contract_worker_protection','Contract Labour Rights',(62,11),'cost:1;p:commercial_orientation:trade=0.07,stab=0.02,bureau=0.06;action:existing_guest_worker_contracts',
      'Negotiate worker protection using the existing overseas-employment and remittance system.',pre=[['middle_east_bids']],icon='labour')
    make('foreign','international_quality','Export Quality Rules',(64,11),'cost:1;p:commercial_orientation:ic=0.03,research=0.02,education=0.04,foreign_def=-0.03',
      'Improve the domestic ability to meet contracted quality standards without a free technology transfer.',pre=[['pacific_standards']],icon='research')
    make('foreign','professional_trade_missions','Professional Missions',(63,12),'cost:1;p:missions:trade=0.05,bureau=0.05',
      'Maintain specialist missions rather than rely solely on personal diplomacy.',pre=[['contract_worker_protection','international_quality']],icon='diplomacy')
    make('foreign','public_treaty_process','Public Treaty Rules',(63,13),'p:treaty_rules:foreign_def=0.05,trade=0.03,pp=-0.04,bureau=0.03;action:publish_treaty_obligations',
      'Publish treaty obligations and require the lawful approval procedure before major commitments.',pre=[['professional_trade_missions']],icon='oversight')
    make('korea','korean_implementation_review','Reciprocal Commitments',(72,10),'cost:1;p:liaison_admin:bureau=0.04;action:verify_korean_signatures',
      'Review which commitments were actually accepted. A failed settlement leaves a domestic liaison office, not a fictitious joint institution.',pre=[['korean_settlement']],icon='korea')
    pair('korea',('civilian_exchange_priority','verification_priority'),('Civilian Exchanges','Verification First'),72,11,
      ('p:contact_priority:trade=0.05,foreign_def=-0.03,bureau=0.03;offer:cultural_exchanges',
       'p:contact_priority:core_def=0.04,pp=-0.03;offer:border_notifications'),
      ('Prioritize human contacts with an agreed exchange programme and exposure to external influence.',
       'Prioritize reciprocal notification and incident management; Pyongyang may refuse.'),[['korean_implementation_review']],icon='cooperation')
    make('korea','cultural_visits','Agreed Cultural Visits',(71,12),'offer:cultural_visits;condition:accepted cultural_exchanges',
      'Offer limited educational and cultural visits under a separately signed programme.',pre=[['civilian_exchange_priority']],icon='students')
    make('korea','border_notice_protocol','Border Notice Rules',(73,12),'offer:border_notice_protocol;condition:accepted border_notifications',
      'Offer reciprocal notification procedures without granting military access or control.',pre=[['verification_priority']],icon='security')
    make('korea','peninsula_liaison_office','Peninsula Liaison',(72,13),'cost:1;p:liaison_admin:trade=0.03,bureau=0.05;weekly:0.001',
      'Fund the Southern liaison service. Partner participation still depends on signed agreements.',pre=[['cultural_visits','border_notice_protocol']],icon='diplomacy')
    make('korea','community_dialogue','A Korean Community',(72,14),'offer:korean_community_dialogue',
      'Offer a common-community dialogue grounded in the1989 proposal. Earlier initiatives are alternate history; no merger, territorial transfer or1991 treaty is automatic.',
      pre=[['peninsula_liaison_office']],code=['OR = { has_country_flag = '+P+'working_contacts_signed has_country_flag = '+P+'sovereign_confederation_signed }'],icon='korea')
    for key,contract in [('cultural_visits','cultural_exchanges'),('border_notice_protocol','border_notifications')]:
        nodes[key]['bypass']={'condition':'Final refusal or expiry of '+contract,
          'native_pattern':'OR = { has_country_flag = '+P+contract+'_refused has_country_flag = '+P+contract+'_expired }',
          'effects':'No payment or agreement reward. Domestic liaison continuation remains available.'}

    #36-card cross-party transition, grounded in the researched1971/1979–80/1985–90 windows.
    groups['transition']={'id':'transition','label':'From military rule to democracy','anchor':[82,0],'party':None,
      'icon':'parliament','history':'research_democratic_transition_expansion.md','gate':'Independent KOR; actual crisis, mandate and constitutional states',
      'ownership':'national','root':P+'constitutional_question'}
    d['groups'].insert(0,groups['transition'])
    T='transition';order='has_country_flag = '+P+'constitutional_order'
    def tr(key,label,x,y,fx,desc,pre=(),flags=(),code=(),active=None,icon=None,days=35):
        return make(T,key,label,(x,y),fx,desc,pre=pre,code=code,state=flags,active=active,icon=icon,days=days)
    tr('constitutional_question','Constitutional Authority',82,0,'pp_once:-50;p:constitutional_audit:pp=0.03,bureau=0.03;action:open_constitutional_dossier',
       'Review who may command, legislate and amend the constitution. This opens a real negotiation process, not an automatic regime change.',days=14)
    tr('electoral_opening','An Electoral Opening',78,1,'p:transition_phase:pp=-0.03,stab=-0.02',
       'Use a genuine electoral or constitutional contest to negotiate enforceable limits on the incumbent.',[['constitutional_question']],
       code=['has_country_flag = '+P+'electoral_opening'],flags=['set_country_flag = '+P+'transition_open'])
    tr('interim_cabinet','An Interim Cabinet',82,1,'p:transition_phase:pp=-0.06,org=-0.02',
       'Support Choi Kyu-hah’s historical caretaker window, or an explicitly negotiated civilian succession. Formal office and coercive command remain separate.',[['constitutional_question']],
       code=['has_country_flag = '+P+'caretaker_installed'],flags=['set_country_flag = '+P+'transition_open'])
    tr('negotiated_withdrawal','Negotiated Withdrawal',86,1,'p:transition_phase:pp=-0.04,personnel=0.04',
       'Open talks with a military-led government under organized civilian pressure; no date or party popularity alone completes the handover.',[['constitutional_question']],
       code=['has_country_flag = '+P+'military_opening_authorized'],flags=['set_country_flag = '+P+'transition_open'])
    tr('bind_incumbent','Bind the Incumbent',78,2,'p:transition_phase:pp=-0.05,bureau=0.03',
       'Obtain a binding commitment to constitutional talks rather than a personal promise of reform.',[['electoral_opening']],flags=['set_country_flag = '+P+'negotiating_commitment'])
    tr('defend_civil_command','Defend Civilian Command',82,2,'p:transition_phase:org=-0.03,pp=-0.04;action:resolve_command_challenge',
       'Resolve the officer challenge to legitimate command. A failed Seoul Spring may lead to renewed military rule and a later opening.',[['interim_cabinet']],
       flags=['set_country_flag = '+P+'command_settlement_pending'])
    tr('retirement_guarantees','Retirement Guarantees',86,2,'p:retirement_promise:org=0.02,personnel=0.08;weekly:0.003',
       'Offer funded retirement guarantees to remove officers from executive politics. The pension obligation survives an ordinary cabinet change.',[['negotiated_withdrawal']],
       flags=['set_country_flag = '+P+'negotiating_commitment'])
    tr('authorize_talks','Constitutional Talks',82,3,'p:transition_phase:pp=-0.04,bureau=0.04;action:authorize_constitutional_talks',
       'Authorize talks with a real mandate and a resolved command or retirement bargain.',[['bind_incumbent','defend_civil_command','retirement_guarantees']],
       code=['has_country_flag = '+P+'negotiating_commitment'],flags=['set_country_flag = '+P+'talks_authorized'])
    tr('open_civic_space','Open Civic Space',82,4,'cost:1;action:legal_civic_associations',
       'Restore lawful meetings, political organization and access to constitutional debate; no party receives free votes.',[['authorize_talks']],
       flags=['set_country_flag = '+P+'civic_space_open','set_country_flag = '+P+'civic_legal_5','set_country_flag = '+P+'civic_legal_19'])
    tr('broad_democratic_coalition','A Broad Coalition',80,5,'p:coalition_forum:pp=-0.04,bureau=0.03;action:register_charter_participants',
       'Bring parliamentary opposition, religious groups, students and workers into a negotiating forum without pretending they are one party.',[['open_civic_space']],icon='cooperation')
    tr('open_security_records','Security Records',84,5,'cost:1;p:records:intel=-0.02,bureau=0.03;action:preserve_case_records',
       'Preserve records of emergency rule and state violence. If Gwangju or other repression occurred, their cases enter this process.',[['open_civic_space']],icon='security')
    a=tr('unity_ticket','An Electoral Unity Pact',79,6,'p:campaign_settlement:stab=0.03,pp=-0.05;action:negotiate_unity_ticket',
       'Negotiate a common electoral ticket. Both Kims retain political careers; neither is automatically appointed or permanently excluded.',[['broad_democratic_coalition']],
       flags=['set_country_flag = '+P+'unified_ticket'],icon='elections')
    b=tr('independent_tickets','Independent Tickets',81,6,'p:campaign_settlement:pp=0.08,stab=-0.02;action:retain_separate_tickets',
       'Preserve separate party organizations and programme autonomy, accepting electoral fragmentation and coalition tension.',[['broad_democratic_coalition']],
       flags=['set_country_flag = '+P+'separate_tickets'],icon='elections')
    a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']]
    a=tr('independent_inquiry','An Independent Inquiry',83,6,'cost:1;p:accountability:stab=0.04,bureau=0.07,intel=-0.03;action:independent_repression_inquiry',
       'Investigate responsibility through civilian evidence and due process, at administrative and security-transition cost.',[['open_security_records']],icon='oversight')
    b=tr('conditional_amnesty','Conditional Amnesty',85,6,'p:accountability:org=0.03,stab=-0.02,trade=-0.02,bureau=0.03;action:conditional_disclosure_compact',
       'Trade limited, conditional guarantees and disclosure for officer cooperation. Credibility and accountability remain contested.',[['open_security_records']],icon='state')
    a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']]
    tr('negotiating_mandate','A Negotiating Mandate',82,7,'action:ratify_negotiating_mandate',
       'Reconcile the electoral pact and accountability terms before agreeing a constitutional model.',
       [['unity_ticket','independent_tickets'],['independent_inquiry','conditional_amnesty']],flags=['set_country_flag = '+P+'charter_mandate'])
    constitution=[
      ('presidential_democracy','Presidential Democracy',80,'p:constitution:pp=0.08,stab=0.03,bureau=0.03',
       'Retain an effective directly elected presidency under binding rights, term and oversight limits.',
       'one_term_presidency','One-Term Presidency','p:constitution:pp=0.1,stab=0.04,bureau=0.03','presidential'),
      ('parliamentary_democracy','Parliamentary Cabinet',82,'p:constitution:pp=-0.08,stab=0.07,bureau=0.04',
       'Make the cabinet responsible to an elected Assembly. This is an alternate settlement grounded in Korean parliamentary experience and constitutional debates.',
       'cabinet_responsibility','Cabinet Responsibility','p:constitution:pp=-0.1,stab=0.08,bureau=0.04','parliamentary'),
      ('consensus_presidency','A Consensus Presidency',84,'p:constitution:pp=0.02,stab=0.05,bureau=0.08',
       'Retain direct election while binding executive action to a broad cabinet and parliamentary bargain. This is an alternate compromise, not the historical1987 constitution.',
       'coalition_veto_rules','Coalition Assent Rules','p:constitution:pp=0.03,stab=0.06,bureau=0.08','consensus'),
    ]
    ids=[];ends=[]
    for key,label,x,fx,desc,end,title,efx,model in constitution:
        a=tr(key,label,x,8,fx,desc,[['negotiating_mandate']],flags=['set_country_flag = '+P+'draft_'+model],active=order,days=49)
        tr(end,title,x,9,efx,'Define enforceable terms, cabinet responsibility and appointment rules for the chosen constitutional model.',[[key]],active=order)
        ids.append(a['id']);ends.append(end)
    for id in ids:nodes[id.removeprefix(P)]['mutually_exclusive']=[x for x in ids if x!=id]
    tr('constitution_referendum','Submit the Constitution',82,10,'pp_once:-75;action:submit_constitutional_ballot',
       'Submit the agreed text to a real ratification process. Rejection does not enable elections or grant the constitutional programme.',[ends],days=49)
    tr('impartial_election_board','An Impartial Ballot',82,11,'cost:1;p:election_administration:stab=0.02,pp=-0.03,bureau=0.04;action:configure_lawful_election',
       'Restore lawful electoral competition using the actual party and coalition system; the result may return Roh, either Kim, or another eligible government.',
       [['constitution_referendum']],code=['has_country_flag = '+P+'constitutional_ratification_passed'],flags=['set_country_flag = '+P+'constitutional_order'])
    tr('uncensored_press','An Uncensored Press',80,12,'p:press_rights:research=0.03,trade=0.04,pp=-0.04;action:protect_civil_press',
       'Protect publication and criticism. These legal rules have enforcement and rollback conditions, not an invented press-freedom meter.',[['impartial_election_board']],flags=['set_country_flag = '+P+'press_protected'],active=order,icon='state')
    tr('accountable_intelligence','Accountable Intelligence',84,12,'p:intelligence_law:encryption=0.04,intel=-0.04,bureau=0.04;action:warranted_security_operations',
       'Separate external intelligence from political surveillance and require warrants and civilian review.',[['impartial_election_board']],flags=['set_country_flag = '+P+'security_warrants'],active=order,icon='security')
    tr('independent_constitutional_court','Constitutional Review',80,13,'cost:1;p:court:stab=0.03,pp=-0.04,bureau=0.04;action:constitutional_review_rules',
       'Create enforceable constitutional review of exceptional powers. The court is a national institution, not a party-specific research bonus.',[['uncensored_press']],flags=['set_country_flag = '+P+'judicial_review'],active=order,icon='oversight')
    tr('civilian_appointments','Civilian Appointments',84,13,'p:appointment_law:org=-0.02,stab=0.02,personnel=0.04;action:bind_civilian_appointments',
       'Put command appointments under the lawful civilian government without claiming that officer networks disappear immediately.',[['accountable_intelligence']],flags=['set_country_flag = '+P+'civilian_appointments'],active=order,icon='army')
    a=tr('retire_political_networks','Retire Political Clubs',83,14,'cost:2;p:officer_settlement:org=0.05,stab=0.03,personnel=0.08;weekly:0.001;action:accelerated_officer_retirement',
       'Retire political officer networks with pensions and a temporary command disruption. Dismantling Hanahoe before1993 is an explicit alternate outcome.',[['civilian_appointments']],
       flags=['set_country_flag = '+P+'officer_networks_retired'],active=order,icon='army')
    a['temporary_effect']={'id':P+'officer_retirement_disruption','days':180,'modifiers':{'army_org_factor':-0.05,'political_power_factor':-0.05}}
    b=tr('staged_officer_retirement','Staged Officer Retirement',85,14,'p:officer_settlement:org=0.06,stab=0.01,personnel=0.12;weekly:0.002;action:staged_officer_retirement',
       'Preserve near-term command continuity through phased retirement, larger pension obligations and an enforceable review timetable.',[['civilian_appointments']],
       flags=['set_country_flag = '+P+'officer_retirement_schedule'],active=order,icon='army')
    a['mutually_exclusive']=[b['id']];b['mutually_exclusive']=[a['id']]
    tr('parliamentary_audits','Parliamentary Audits',82,15,'cost:1;p:budget_oversight:interest=-0.2,pp=-0.03,bureau=0.04;action:restore_assembly_audits',
       'Restore legislative scrutiny over public finance and state abuses, including hearings when the historical cases exist.',
       [['retire_political_networks','staged_officer_retirement'],['independent_constitutional_court']],flags=['set_country_flag = '+P+'assembly_audit_rights'],active=order,icon='oversight')
    tr('restore_labour_bargaining','Lawful Labour Bargaining',80,16,'p:labour_law:ic=-0.02,stab=0.03,social=0.04;action:register_native_labor_faction',
       'Establish lawful independent representation and then use the actual MD labor-faction opinion effect. Existing faction state is never reset.',[['parliamentary_audits']],
       flags=['set_country_flag = '+P+'lawful_labour_bargaining'],active=order,icon='labour')
    tr('prepare_local_councils','Prepare Local Councils',84,16,'cost:1;p:local_government:agri=0.03,stab=0.02,bureau=0.04;action:prepare_local_autonomy_law',
       'Restore the legal basis and timetable for local councils. Historical council elections in1991 and executive elections in1995 remain outside this horizon.',[['parliamentary_audits']],
       flags=['set_country_flag = '+P+'local_autonomy_prepared'],active=order,icon='rural')
    tr('constitutional_security','Constitutional Security',82,17,'p:transition_phase:pp=0,bureau=0',
       'Bind public security to constitutional law. Legal civilian control is distinct from removing every military-era political network.',
       [['restore_labour_bargaining'],['prepare_local_councils']],flags=['set_country_flag = '+P+'civilian_control','clr_country_flag = '+P+'transition_open'],active=order)
    # Only one policy slot per focus: zero clears the transitional burden.
    nodes['constitutional_security']['effects']['policies']=nodes['constitutional_security']['effects']['policies'][:1]
    nodes['constitutional_security']['effects']['expense_commitment']['slot']='national|transition:transition_phase'
    tr('orderly_handover','An Orderly Handover',80,18,'pp_once:75;action:confirm_native_handover',
       'Recognize an actual lawful election and transfer. The constitutional branch never appoints a predetermined winner.',[['constitutional_security']],
       code=['has_country_flag = '+P+'lawful_election_completed'],flags=['set_country_flag = '+P+'lawful_handover'],icon='elections')
    tr('defend_new_order','Defend the New Order',84,18,'p:democratic_safeguards:pp=-0.03,police=0.03;action:enforce_democratic_safeguards',
       'Require lawful authorization for emergency powers and a recorded public constitutional process for reversal. A coup or rollback can still occur, with explicit costs.',[['constitutional_security']],
       flags=['set_country_flag = '+P+'democratic_safeguards'],active=order,icon='oversight')
    nodes['defend_new_order']['effects']['policies'][0]['modifiers']['drift_defence_factor']=0.08

    # Expansion-level institutional action catalogue. These are proposed NEW
    # handlers built from native flags, ideas, politics, costs and event APIs.
    action_ids=sorted({a['value'] for n in d['nodes'] if n.get('added_in_revision')==2 for a in n['effects']['actions'] if a['type']=='action'})
    d['actions']['expansion_institutions']={'ids':action_ids,
      'design':'Implement through transition_system and existing political/economic systems. No label or country flag alone is a judicial, press, command or legitimacy statistic.'}
    d['transition_system']={
      'root':P+'constitutional_question','focuses':36,
      'entry_routes':'Electoral contest; legitimate caretaker succession; negotiated military withdrawal. Entries are not permanently mutually exclusive: a failed early window may be followed by later talks.',
      'military_failure':'The command-challenge action sends a real resolution event. Successful civilian command sets negotiating_commitment. Failure sets military_reconsolidation, retains command burden and allows a later authorized military opening. It does not install Chun before a separate actual office transition.',
      'ratification':{'event':'COLDWAR_KOR_transition.30','pending_days':30,'reject_retry_days':90,
        'vote_model':'Gameplay abstraction: charter supporters are a unique set of actual party/organization slots. Sum their current native party_pop_array shares divided by the sum of current legal participating shares. Passing requires strictly more than50%; no bonus popularity is created.',
        'accept':'Set constitutional_ratification_passed and exactly one selected constitutional model; call the actual politics/election configuration. No leader is installed by this vote.',
        'reject':'No constitutional programme or election-rule grant. Keep the chosen model; return to negotiation through a repeatable50PP redraft decision after90d. Do not reset focuses or replay rewards.'},
      'election':'Only the actual native election/coalition result sets lawful_election_completed and installs the corresponding incumbent via the reconciled KOR router. Unity-ticket agreement redistributes existing candidacy/support only; it never ensures victory.',
      'national_institutions':'Court, press, electoral administration, lawful unions, local-autonomy preparation and civilian appointment rights survive ordinary cabinet change. Their policy effects require the constitutional_order receipt where specified.',
      'rollback':{'decision':P+'constitutional_rollback','cost':'100PP; stability -10%; requires a resolved coup or a lawful, publicly ratified constitutional reversal',
        'effect':'Disable constitutional_order and safeguards, lawful union/press/command dependent effects; retain earned focus receipts. No institutional bonuses under emergency rule.',
        'restoration':'A public constitutional restoration vote and genuine lawful mandate can restore active earned institutions. No focus reset, cash, factories, experience or one-time PP replay.'},
      'court_reader':'When judicial_review and constitutional_order are active, unlawful emergency/press-ban/security-decree actions are unavailable. A lawful emergency needs the defined Assembly approval and review event; constitutional repeal follows the explicit rollback route.',
      'civil_command_reader':'With civilian_appointments and constitutional_order, the military caretaker/coup entry cannot claim lawful appointment. Its initiator must resolve the actual extra-constitutional challenge and its costs; senior appointment actions require the lawful cabinet authority.',
      'labor_provider':'If lawful_labour_bargaining is enacted, register labour_unions only if absent, initialize its native state once and call change_labour_unions_opinion with temp_opinion=10. Reconcile IP_idea_configuration so lawful recognition survives ordinary government changes. Never reset existing faction opinion or infer legality from the faction idea alone.',
      'historical_dates':'Historical milestones remain1971/1972/1979–80/1985/1987/1988–90. Earlier negotiated settlements and parliamentary/consensus constitutions are clearly alternate history. Local elections1991/1995 and Hanahoe dissolution1993 are not historical pre1991 rewards.'}

    # Correct old shortcuts that previously made a declaration do the work of
    # the whole constitutional transition.
    replacements={'constitutional_drp':'constitutional_reform_commitment','managed_liberalization':'open_constitutional_negotiations',
                  'june_declaration':'accept_direct_election_principle','sixth_republic':'confirm_constitutional_settlement'}
    for key,action in replacements.items():
        n=nodes[key]
        n['effects']['actions']=[a for a in n['effects']['actions'] if a['type']!='action']+[{'type':'action','value':action}]
        n['transition_link']='This is a mandate or commitment. Actual constitutional ratification, elections and office changes run through the shared transition process.'
    d['actions']['transition_links']={'ids':list(replacements.values()),'design':'Set an authorized negotiation/commitment receipt. No automatic democracy, leader, referendum result or election-rule grant.'}
    # Neither constitutional method nor Roh’s cooperation requires an ahistorical
    # forced break between contemporaneous policies.
    for key in ('parliamentary_republic','checked_presidency','constitutional_court','civilian_security'):
        nodes[key]['transition_link']='Party programme implementing institutions already lawfully enacted or negotiated in the shared constitutional transition.'
    for key in ('uncensored_press','accountable_intelligence','independent_constitutional_court','civilian_appointments','parliamentary_audits','restore_labour_bargaining','prepare_local_councils','constitutional_security','orderly_handover','defend_new_order'):
        nodes[key]['condition_code'].append(order)
    # Cabinet/election-board completion is what activates the national order.
    nodes['impartial_election_board']['condition_code'].append('has_country_flag = '+P+'constitutional_ratification_passed')
    nodes['civil_nuclear'].setdefault('condition_code',[]).extend([
      'COLDWAR_nuc_economy_allows = yes','has_tech = reactor1','country_can_build_nuclear_reactors = yes'])
    nodes['civil_nuclear']['requirements']=['Actual eligible Imperia development tier, reactor technology and native reactor-building permission; native paid projects and safeguards remain mandatory']

    # New political and welfare starting constraints have real removal readers.
    d['starting_spirits'] += [
      {'id':P+'start_political_command','label':'Political Officer Networks','owner':'national command problem; active until lawful civilian control',
       'modifiers':{'army_org_factor':0.04,'political_power_factor':0.03,'stability_factor':-0.04,'personnel_cost_multiplier_modifier':0.04},
       'history':'The army, security agencies and private officer networks sustain the developmental state while undermining neutral civilian command.',
       'resolution':'Civilian Appointments plus Constitutional Security remove the command-problem slot. An extra-constitutional rollback restores the unresolved political-command state, not free transition rewards.'},
      {'id':P+'start_social_insurance','label':'Fragmented Social Protection','owner':'national welfare problem slot',
       'modifiers':{'stability_factor':-0.04,'social_cost_multiplier_modifier':0.05},
       'history':'Coverage remained fragmented and excluded many rural, informal and urban households; broad national coverage was a late1980s achievement.',
       'resolution':'The funded social-insurance network establishes the new framework and resolves this administrative fragmentation; it does not claim all households were historically insured before1989.'}]
    nodes['constitutional_security']['start_replacements']=['political_command']
    for key in ('urban_insurance_network','rural_insurance_network'):nodes[key]['start_replacements']=['social_insurance']
    d['starting_slot_transitions']['political_command']={'start':deepcopy(d['starting_spirits'][-2]['modifiers']),'resolved':'0 while constitutional_order and civilian_control are both active; ordinary party change does not restore it'}
    d['starting_slot_transitions']['social_insurance']={'start':deepcopy(d['starting_spirits'][-1]['modifiers']),'resolved':'0 after a funded social-insurance network; preserve the earned national framework across ordinary governments'}

    # Four concrete new inter-Korean offers plus the1989 community framework.
    from COLDWAR_KOR_contracts import contract,policy
    new_contracts=[
      contract('cultural_exchanges','NKO',0,0,[],{},'Agree a limited civilian-exchange framework. No automatic visits or passive stat bonus.',0),
      contract('cultural_visits','NKO',1,0.001,[policy('visits',trade_opinion_factor=0.04,foreign_influence_defense_modifier=-0.02)],
        {'treasury_change':-1,'weekly_expense_bn':0.001,'policy':{'trade_opinion_factor':0.04,'foreign_influence_defense_modifier':-0.02}},
        'Each country pays $1bn plus $0.001bn weekly for agreed cultural and educational visits; trade opinion +4%, influence defence -2%.'),
      contract('border_notifications','NKO',0,0,[],{},'Agree a framework for military incident notifications. No automatic military access or disarmament.',0),
      contract('border_notice_protocol','NKO',1,0.001,[policy('notices',army_core_defence_factor=0.025,bureaucracy_cost_multiplier_modifier=0.03)],
        {'treasury_change':-1,'weekly_expense_bn':0.001,'policy':{'army_core_defence_factor':0.025,'bureaucracy_cost_multiplier_modifier':0.03}},
        'Each country pays $1bn plus $0.001bn weekly for reciprocal notifications; core defence +2.5%, bureaucracy expenses +3%.'),
      contract('korean_community_dialogue','NKO',0,0,[],{},'Negotiate a common-community agenda inspired by the1989 formula. Separate governments and armed forces remain; neither side is forced to unify or sign the1991 Basic Agreement.',0),
    ]
    d['contracts'].extend(new_contracts)
    # Reposition KJP below the now longer economy; reserve the complete subtree.
    for n in d['nodes']:
        if n['group']=='kjp':n['xy'][0]+=9;n['xy'][1]+=1
    groups['kjp']['anchor']=[54,19]
    d['layout']['continuous_focus_position']=[7100,3300]
    # Eight native slots; make the requested transition easy to reach.
    shortcuts=('drp','transition','reform','army','economy','defence','foreign','korea')
    d['layout']['shortcuts']=[{'name':groups[k]['label'],'target':groups[k]['root'],'scroll_wheel_factor':0.8} for k in shortcuts]
    # Resolve every old and new offset from one final absolute-coordinate model.
    for n in d['nodes']:
        g=groups[n['group']];a=next(x for x in d['nodes'] if x['id']==g['root'])
        n['anchor']=None if n['id']==a['id'] else a['id']
        n['offset']=n['xy'][:] if not n['anchor'] else [n['xy'][0]-a['xy'][0],n['xy'][1]-a['xy'][1]]
    d['expansion_summary']={'previous_focuses':base_count,'focuses':len(d['nodes']),'added':len(d['nodes'])-base_count,
      'transition_focuses':36,'group_deltas':{g['id']:sum(n['group']==g['id'] for n in d['nodes'])-baseline.get(g['id'],0) for g in d['groups']},
      'research_first':['research_democratic_transition_expansion.md','mechanics_expansion_research.md','layout_expansion_research.md'],
      'historical_corrections':['Nordpolitik and1990 merger no longer falsely exclude one another','Local councils prepared, not historically elected before1991','Hanahoe dismantling before1993 explicitly alternate','Direct-election commitment no longer skips the actual constitutional process']}
    assert len(d['nodes'])==298,(len(d['nodes']),d['expansion_summary'])
    return d
