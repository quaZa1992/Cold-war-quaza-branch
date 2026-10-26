# IMPERIA CW — Cold War: documented concept-review corrections; no runtime writes.
"""Apply historical, reachability and spatial review to the single design model."""
P='COLDWAR_KOR_'

def refine(d):
    nodes={n['key']:n for n in d['nodes']}
    # An early equivalent is plausible, but 1993's named reform is outside scope.
    nodes['real_name_accounts']['label']='Accountable Banking'
    nodes['real_name_accounts']['description']='Require accountable financial records and transparent corporate ownership. This is an alternate precursor, not Kim Young-sam’s 1993 real-name-finance reform.'
    # History is a route through real institutions, not a railroaded assassination.
    d['transition_events']=[
      {'id':P+'transition_1971','label':'The Presidential Contest','trigger':'Native election/constitutional contest or a player-initiated early constitutional crisis',
       'historical_context':'The 1971 Park–Kim Dae-jung contest follows the 1969 amendment.',
       'choices':[
         {'label':'Respect the Competitive Mandate','effects':'competitive election settlement; stability +3%; PP -50; election resolves through party system'},
         {'label':'Prepare an Executive Emergency','effects':'constitutional crisis receipt; stability -5%; PP +50; permits Yushin proposal, does not enact it automatically'}]},
      {'id':P+'transition_1979','label':'A Presidential Succession Crisis','trigger':'Park dies/leaves office, or a separately resolved leadership crisis; historical branch dated 26 October 1979',
       'historical_context':'Park’s assassination produced Choi Kyu-hah’s interim presidency, not an immediate automatic Chun government.',
       'choices':[
         {'label':'Support the Interim Civilian Government','effects':'install Choi through reconciled native office machinery; 180d interim spirit: PP -10%, stability -3%; open constitutional negotiations'},
         {'label':'Submit to an Officer Council','effects':'open military contest decisions; no automatic coup victory; 90d contested-command spirit: organization -5%, stability -5%'}]},
      {'id':P+'transition_officers','label':'The December Officer Challenge','trigger':'Interim government and active Hanahoe challenge; historical 12 December precedent',
       'historical_context':'Chun’s seizure of military command preceded his presidential rule.',
       'choices':[
         {'label':'Defend Civilian Command','effects':'PP -75; 90d organization -5%; if legitimate command wins, competitive-election route; if defeated, officer-controlled transition'},
         {'label':'Concede Military Command','effects':'party22 transition proposal; stability -5%; retains contested-command burden until settlement'}]},
      {'id':P+'transition_gwangju','label':'The Martial-Law Crisis','trigger':'Officer-controlled transition, unresolved civilian demands; historical May 1980 precedent',
       'historical_context':'Gwangju repression is represented as a legitimacy crisis with lasting costs, never as a rewarded atrocity.',
       'choices':[
         {'label':'Negotiate Civilian Guarantees','effects':'PP -75; 180d organization -3%; restore political participation and open direct-election settlement'},
         {'label':'Extend Nationwide Martial Law','effects':'enable controlled Fifth Republic; persistent legitimacy scar: stability -8%, trade opinion -5%, police expenses +8%; no positive instant reward'}]},
      {'id':P+'transition_1985','label':'The Opposition Reorganizes','trigger':'Legal opposition recovers parliamentary weight; historical 1985 NKDP breakthrough',
       'historical_context':'NKDP organization reconnects the Two Kims and constitutional opposition.',
       'choices':[
         {'label':'A Joint Reform Ticket','effects':'native party2 leadership contest; PP -50; maintains combined reform organization'},
         {'label':'Separate Democratic Organizations','effects':'retain distinct YS/RDP and DJ/PDP identity receipts; split the existing reform vote through native party machinery, never create free popularity'}]},
      {'id':P+'transition_1987','label':'The Direct-Election Settlement','trigger':'Constitutional demand, protest escalation and a real government response; historical June 1987 precedent',
       'historical_context':'Direct elections were a negotiated democratic opening; Roh’s victory was an election outcome, not guaranteed by the declaration.',
       'choices':[
         {'label':'Accept Direct Presidential Elections','effects':'enable competitive elections; PP -75; replace emergency constitution with legal settlement; Roh may become party22 nominee'},
         {'label':'Defend Indirect Selection','effects':'PP +25; stability -8%; police expenses +8%; civic unrest remains and Nordpolitik elected-leader branch unavailable'}]},
      {'id':P+'transition_labour','label':'The Labour Movement Organizes','trigger':'Existing labor law, export-workplace dispute or a native industrial-relations event; distinct stages rooted in Jeon Tae-il 1970, YH 1979, Great Workers’ Struggle 1987',
       'historical_context':'The events are political consequences, not free factories or inevitable mass socialist victory.',
       'choices':[
         {'label':'Recognize Collective Mediation','effects':'replace labor-problem slot with stability +4%, factory output -2%, bureaucracy expenses +3%; independent union route usable'},
         {'label':'Maintain Compulsory Arbitration','effects':'replace labor-problem slot with factory output +4%, stability -8%, police expenses +4%; grievances persist'}]},
      {'id':P+'transition_1990','label':'The Conservative Coalition Talks','trigger':'Actual Roh, YS and KJP party organizations have separately authorized a merger; historical January 1990 precedent',
       'historical_context':'DJP + RDP + NDRP formed the DLP; Kim Dae-jung’s PDP remained outside.',
       'choices':[
         {'label':'Ratify the Conservative Merger','effects':'native coalition/identity update and existing support redistribution only; PP +75, stability -3%; independent DJ opposition preserved'},
         {'label':'Keep the Parties Independent','effects':'no forced transfer of support; PP +25; separate programmes and elections continue'}]},
    ]
    for key in ('yushin','constitutional_drp'):
        nodes[key]['start_replacements']=['presidency']
    nodes['yushin']['requirements']=['A completed presidential contest or genuine constitutional crisis; actual Park/DRP government']
    nodes['yushin']['historicity']='1972 historical settlement; an earlier equivalent is explicitly alternate history.'
    nodes['emergency_decrees']['requirements']=['Yushin constitutional settlement remains in force']
    nodes['dynastic_presidency']['label']='Managed Succession'
    # All programmes require current real settlement, not just a completed ancestor.
    for key in ('yushin','emergency_decrees','dynastic_presidency'):
        nodes[key]['governance_binding']='Active only under the matching emergency constitutional settlement; disabled if competitive civilian rules replace it.'
    for key in ('parliamentary_government','reform_mandate','social_democratic_cabinet','june_declaration'):
        nodes[key]['start_replacements']=['presidency']
    # Native bypass preserves a common OR join when a treaty-only continuation
    # is refused. Bypassed focus receives zero reward and is marked as such.
    bypass={
      'family_reunions':'red_cross_channel',
      'verified_restraint':'nonaggression_compact',
      'confederal_secretariat':'sovereign_confederation',
      'limited_trade':'parallel_recognition',
      'licensed_maintenance':'allied_procurement_contract',
      'burden_sharing':'us_alliance_assurance',
      'joint_technical_training':'japan_technology_finance',
      'southern_guarantees':'sovereign_confederation',
      'joint_planning':'northern_security_compact',
    }
    for key,offer in bypass.items():
        nodes[key]['bypass']={
          'condition':f'Final refusal or 60-day pending expiry of {offer}; dispatch focus earned; not signed',
          'native_pattern':f'OR = {{ has_country_flag = {P}{offer}_refused has_country_flag = {P}{offer}_expired }}',
          'effects':'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}
        nodes[key].pop('response_fallback',None)
    nodes['korean_settlement']['conditional_completion']={
      'signed secretariat or signed limited trade':'Joint ratification decision; no forced annexation',
      'offer conclusively refused/expired':'Unilateral Peninsula Policy Review; +25 political power; no membership or treaty bonuses'}
    nodes['korean_settlement']['effects']['actions']=[{'type':'action','value':'conditional_peninsula_review'}]
    for n in nodes.values():n.pop('response_fallback',None)
    d['refusal_routes']={'mechanism':'Native bypass on treaty-only follow-ups after a recorded refusal/expiry; no payout. Common OR joins remain exact. Final Korean settlement conditionally becomes a domestic review.',
      'graph':'206 focus cards; no invisible alternative prerequisites or unresolved extra review cards.'}
    # Dispatching these offers has no extra setup fee; the contract is the only
    # establishment charge. Own technical colleges etc remain separately priced.
    for key in ('assembly_contracts','family_reunions','confederal_secretariat'):
        nodes[key]['effects']['cost']=0
    # Avoid an indefinite defence bonus from an unaccepted licence offer.
    for key,offer in [('assembly_contracts','technology_licence'),('allied_procurement','allied_procurement_contract'),
                      ('northern_alignment','northern_security_compact')]:
        for policy in nodes[key]['effects']['policies']:policy['active_condition']='accepted '+offer
    # Agency government is explicitly new alternate content, not ordinary 1970.
    nodes['security_cabinet']['requirements']=['Exceptional government transition resolved; actual ruling_party 7; KCIA power-bloc backing alone is insufficient']
    for g in d['groups']:
        if g['id']=='drp':
            g['gate']='check_variable = { ruling_party = 0 } AND actual Park incumbent'
            for n in nodes.values():
                if n['group']=='drp':n['gate']=g['gate'];n['ownership']='leader:Park Chung Hee'
        if g['id']=='kjp':
            for n in nodes.values():
                if n['group']=='kjp':n['ownership']='leader:Kim Jong-pil'
    # Separate future party identities while retaining the 24-slot schema.
    d['party_migration']['identity_receipts']={
      '0':'DRP at start; KJP civilian successor / NDRP after its historical formation or an explicit earlier reorganization',
      '1':'NDP elders / constitutional conservatives; NKDP cooperation is an event, not a free new popularity slot',
      '2':'Forties reform lineage; YS–RDP and DJ–PDP identity plus incumbent checks keep distinct leader programmes; later merger needs agreement',
      '3':'Kim Chul / Unification Socialist Party; never silently reuse DJ’s old pool',
      '22':'Army regime; DJP only after its formation; elected Roh requires the direct-election settlement',
    }
    # Conservative early and later leaders do not inherit each other's personal programme.
    nodes['fifth_republic']['gate']+=' AND incumbent Chun Doo-hwan'
    nodes['press_consolidation']['gate']+=' AND incumbent Chun Doo-hwan'
    nodes['roh_nordpolitik']['gate']+=' AND incumbent Roh Tae-woo AND competitive-election settlement'
    for key in ('fifth_republic','press_consolidation'):
        nodes[key]['ownership']='leader:Chun Doo-hwan'
        nodes[key]['governance_binding']='Controlled Fifth Republic constitutional settlement still active'
    nodes['roh_nordpolitik']['ownership']='leader:Roh Tae-woo'
    # Record starting problem slot state changes without invented remove APIs.
    d['starting_slot_transitions']={
      'presidency':{'start':{'political_power_factor':0.08,'stability_factor':-0.08},'resolved':'0 after a valid replacing constitution; removed on end of Park/DRP office'},
      'finance':{'start':{'industrial_capacity_factory':0.04,'interest_rate_multiplier_modifier':0.5},'resolved':'0 after national finance policy; party-specific credit exposure remains separate'},
      'labour':{'start':{'industrial_capacity_factory':0.03,'stability_factor':-0.08,'research_speed_factor':-0.02},'resolved':'0 after national labor policy or mediation/arbitration event; the replacing policy supplies its own benefits and costs'},
      'rural':{'start':{'production_speed_buildings_factor':-0.07,'stability_factor':-0.03},'freight_corridors':{'production_speed_buildings_factor':-0.03,'stability_factor':-0.02},'urban_services':'0'},
      'alliance':{'start':{'army_core_defence_factor':0.05,'foreign_influence_defense_modifier':-0.1},'resolved':'0 after accepted US assurance or strategic-autonomy doctrine; existing actual treaty stays subject to diplomacy'},
      'energy':{'start':{'industrial_capacity_factory':-0.04,'interest_rate_multiplier_modifier':0.2},'energy_planning':{'industrial_capacity_factory':-0.02,'interest_rate_multiplier_modifier':0.1},'resolved':'0 only after a qualifying existing energy project is completed and funded'},
    }
    for c in d['contracts']:
        if c['key']=='us_alliance_assurance':c['on_accept_start_replacement']='alliance'
    nodes['strategic_autonomy']['start_replacements']=['alliance']
    # Concrete MD geometry refinement: ordinary pairs are two grid cells apart.
    new_anchors={'drp':(4,0),'ndp':(12,0),'reform':(23,0),'army':(34,0),
                 'usp':(4,14),'minjung':(13,14),'rpr':(23,14),'security':(34,14),
                 'economy':(45,0),'defence':(54,0),'foreign':(63,0),'korea':(72,0),'kjp':(45,18)}
    old={g['id']:g['anchor'][:] for g in d['groups']}
    for n in nodes.values():
        gid=n['group']; ax,ay=old[gid];dx=n['xy'][0]-ax;dy=n['xy'][1]-ay
        if gid not in ('reform','minjung') and abs(dx)==2:dx=1 if dx>0 else -1
        if gid=='reform':dx={-6:-5,-2:-3,2:3,6:5}.get(dx,dx)
        if gid=='minjung':dx={-5:-4,-1:-2,1:2,5:4}.get(dx,dx)
        nx,ny=new_anchors[gid];n['xy']=[nx+dx,ny+dy]
    for g in d['groups']:g['anchor']=list(new_anchors[g['id']])
    # Re-resolve all emitted offsets after compaction, including the second
    # minjung root whose geometric anchor is not a prerequisite.
    byid={n['id']:n for n in d['nodes']}
    for n in d['nodes']:
        if n['anchor']:
            a=byid[n['anchor']];n['offset']=[n['xy'][0]-a['xy'][0],n['xy'][1]-a['xy'][1]]
        else:n['offset']=n['xy'][:]
        n['available_if_capitulated']=False;n['cancel_if_invalid']=True;n['continue_if_invalid']=False
        n['requirements']=n.get('requirements',[])+['Actual governing party/leader and legal settlement remain valid at completion'] if n['ownership']!='national' else n.get('requirements',[])
    shortcut_groups=('drp','ndp','reform','army','economy','defence','foreign','korea')
    d['layout']['shortcuts']=[{'name':g['label'],'target':g['root'],'scroll_wheel_factor':0.8} for g in d['groups'] if g['id'] in shortcut_groups]
    d['layout']['shortcut_capacity']=8
    d['layout']['initial_show_position']={'focus':P+'developmental_state'}
    d['layout']['continuous_focus_position']=[5500,3500]
    for n in nodes.values():
        policies=n['effects']['policies']
        if policies:
            # Cost belongs to the focus's single policy slot, not each stat.
            assert len(policies)==1,(n['id'],'give multi-slot focuses an explicit expense owner')
            n['effects']['expense_commitment']={
              'slot':n['ownership']+'|'+policies[0]['qualified_slot'],
              'weekly_bn':n['effects']['weekly'],
              'operation':'replace; zero clears prior commitment in this slot',
              'active_condition':policies[0].get('active_condition','same actual owner as policy')}
            for policy in policies:policy.pop('weekly_cost_bn',None)
    d['rules']['weekly']='One unique owner|qualified_policy_slot expense record per focus, replaced by the latest earned level; zero clears that slot. Sum active expense records once plus separate active contract charges; feed COLDWAR_KOR_weekly_cost to native calculate_additional_expense_rate. NEW adapter required.'
    d['modifier_labels']['interest_rate_multiplier_modifier']='Interest rate (percentage points before native clamps)'
    # Short native focus names; full political meaning remains in descriptions.
    aliases={
      'developmental_state':'Developmental State','yushin':'Yushin Constitution','constitutional_drp':'Civilian Conservatism',
      'assembly_bargain':'Assembly Bargaining','competitive_credit':'Competitive Credit','rural_cooperatives':'Rural Cooperatives',
      'performance_grants':'Village Grants','village_accounts':'Village Elections','parliamentary_government':'Parliamentary Rule',
      'parliamentary_republic':'Parliamentary Republic','social_conservatives':'Social Market Pact','pension_contributions':'Social Contributions',
      'regional_compromise':'Regional Investment','civilian_security':'Security Oversight','security_compromise':'The Security Bargain',
      'democratic_conservatism':'Civic Conservatism','ys_civilian_authority':'Kim Young-sam','dj_people_economy':'Kim Dae-jung',
      'corporate_transition':'Corporate Transition','ys_civil_coalition':'A Reform Coalition','broad_welfare':'Social Insurance',
      'targeted_welfare':'Targeted Protection','national_health_cover':'Health Coverage','dj_civil_coalition':'Regional Inclusion',
      'dj_consolidation':'Labour Mediation','sixth_republic':'The Civilian Republic','democratic_alliance':'A Democratic Alliance',
      'reform_nordpolitik':'Reform Nordpolitik','military_cabinet':'Military Government','professional_officers':'Professional Officers',
      'industrial_continuity':'Industrial Continuity','industrial_rationalization':'Industrial Adjustment','export_recovery':'Export Recovery',
      'hanahoe_compact':'The Officer Networks','civilian_promotions':'Civilian Promotions','olympic_republic':'International Opening',
      'social_democratic_cabinet':'Social Democracy','universal_insurance':'Universal Provision','independent_unions':'Independent Unions',
      'public_credit':'Public Credit','social_market_industry':'A Social Market','balanced_development':'Provincial Opportunity',
      'socialist_alliance':'A Socialist Voice','neutral_peace':'Armed Neutrality','labour_republic':'Social Partnership',
      'student_cabinet':'A Civic Cabinet','national_service_schools':'Service Schools','community_service':'Community Service',
      'student_cabinet_public_accounts':'Investment Accounts','independent_left':'Independent Socialism','strategic_public_sector':'Strategic Public Firms',
      'southern_socialism':'Southern Socialism','independent_left_public_accounts':'Public Accounts','revolutionary_cabinet':'Revolutionary Cabinet',
      'southern_front':'A Southern Front','pluralist_socialism':'Pluralist Socialism','party_cadres':'Cadres in Industry',
      'revolutionary_reconstruction':'Rebuild Industry','confederal_revolution':'A Confederal Route','southern_guarantees':'Southern Guarantees',
      'joint_planning':'Joint Planning','southern_settlement':'A Southern Settlement','revolutionary_diplomacy':'Seek Recognition',
      'external_service':'External Intelligence','national_files':'National Files','warranted_operations':'Warranted Operations',
      'counter_infiltration':'Counter-Infiltration','security_technocrats':'Protected Technocrats','civilian_exit':'A Civilian Exit',
      'protected_planning':'Protected Planning','disclose_archives':'Open the Archives','security_settlement':'Security Settlement',
      'security_handover':'Handover Guarantees','third_plan':'Review the Plan','heavy_chemical_drive':'Heavy Industry Drive',
      'pohang_foundry':'Pohang Steelworks','provincial_export_zones':'Provincial Exports','freight_corridors':'Freight Corridors',
      'assembly_contracts':'Assembly Licences','domestic_engineering':'Domestic Engineering','industrial_skills':'Industrial Skills',
      'labor_discipline':'Wage Discipline','labor_compact':'A Labour Compact','controlled_arbitration':'State Arbitration',
      'safety_inspectorate':'Safety Inspection','urban_services':'Urban Services','export_credit_guarantees':'Export Guarantees',
      'orderly_restructuring':'Orderly Restructuring','energy_planning':'Energy Diversification','civil_nuclear':'Civil Nuclear Power',
      'thermal_diversification':'Diverse Fuel Supplies','advanced_export_economy':'Advanced Exports','defence_review':'Defence Review',
      'counter_infiltration_units':'Infiltration Response','combined_arms_training':'Combined Arms','defence_logistics':'Military Logistics',
      'domestic_defence_industry':'Domestic Armaments','changwon_production':'Changwon Production','defence_quality':'Quality Standards',
      'joint_staff':'The Joint Staff','air_command':'Joint Air Command','alliance_bargain':'The Alliance Bargain',
      'burden_sharing':'Burden Sharing','diverse_partners':'Security Partners','vietnam_legacy':'The Vietnam Legacy',
      'japan_pragmatism':'Pragmatism with Japan','claims_first':'Historical Claims','joint_technical_training':'Technical Exchanges',
      'alternative_capital':'Alternative Capital','overseas_workers':'Overseas Workers','nordpolitik':'Northern Diplomacy',
      'pacific_exports':'Pacific Exports','middle_power':'A Middle Power','family_reunions':'Family Reunions',
      'incident_hotline':'An Incident Hotline','review_korean_policy':'Peninsula Policy','competitive_legitimacy':'Korean Legitimacy',
      'verified_restraint':'Verified Restraint','defector_protection':'Protect Defectors','reciprocal_contacts':'Working Contacts',
      'sovereign_confederation':'Offer a Confederation','two_governments':'Parallel Recognition','confederal_secretariat':'A Joint Secretariat',
      'limited_trade':'Inter-Korean Trade','korean_settlement':'A Korean Settlement','kjp_civilian_cabinet':'Kim Jong-pil',
      'kjp_coalition':'Conservative Coalition','kjp_executive':'Executive Coordination','kjp_provincial_credit':'Provincial Credit',
      'kjp_small_enterprise':'Small-Enterprise Pact','kjp_large_industry':'Strategic Industry','kjp_supplier_networks':'Supplier Networks',
      'kjp_party_settlement':'A Civilian Party','kjp_korean_policy':'Pragmatic Diplomacy',
    }
    for key,label in aliases.items():
        nodes[key]['full_title']=nodes[key]['label'];nodes[key]['label']=label
    for n in nodes.values():
        conditions=[a['value'] for a in n['effects']['actions'] if a['type']=='condition']
        n['requirements']=n.get('requirements',[])+conditions
        if n['group']=='kjp' or n['group']=='drp':
            n['programme_owner']=n['ownership']
    nodes['red_cross_channel']['historicity']='Historical humanitarian opening in 1971–72; a 1970 initiative is an explicitly alternate early offer and requires NKO consent.'
    nodes['red_cross_channel']['description']='Propose humanitarian liaison on separated families. The 1971–72 talks are the historical precedent; an earlier opening depends on Pyongyang’s agreement.'
    nodes['nordpolitik']['historicity']='Historical Soviet normalization in 1990. Chinese normalization historically occurred in 1992, outside this horizon; an earlier CHI contract is alternate history, not an automatic historical reward.'
    nodes['nordpolitik']['description']='Seek reciprocal diplomatic openings with socialist states. Soviet recognition in 1990 is the historical precedent; earlier recognition or Chinese normalization before 1991 is alternate history.'
    nodes['nordpolitik']['requirements']=['At peace with the proposed partner; the partner must agree to a diplomatic opening before recognition is ratified']
    nodes['kjp_civilian_cabinet']['historicity']='Alternate presidential officeholding; Kim Jong-pil was historically prime minister and party leader, not president.'
    nodes['kjp_civilian_cabinet']['description']+=' His presidential office is alternate history, grounded in his actual conservative party and prime-ministerial career.'
    # Country economic productivity is not the engine's military-equipment
    # factory-output/efficiency-cap stat. Use the actual MD civilian GDP reader.
    civilian='civilian_factories_productivity'
    def economic_modifiers(modifiers):
        value=modifiers.pop('industrial_capacity_factory',0)+modifiers.pop('production_factory_max_efficiency_factor',0)
        if value:modifiers[civilian]=round(modifiers.get(civilian,0)+value,5)
    for n in nodes.values():
        if n['group']!='defence':
            for p in n['effects']['policies']:economic_modifiers(p['modifiers'])
    for spirit in d['starting_spirits']:economic_modifiers(spirit['modifiers'])
    for slot in d['starting_slot_transitions'].values():
        for value in slot.values():
            if isinstance(value,dict):economic_modifiers(value)
    for c in d['contracts']:
        for p in c['KOR_policy']:economic_modifiers(p['modifiers'])
        if 'policy' in c['recipient_effects']:economic_modifiers(c['recipient_effects']['policy'])
        c['description']=c['description'].replace('efficiency cap','civilian industrial productivity').replace('Efficiency cap','Civilian industrial productivity')
    d['modifier_labels'][civilian]='Civilian industry productivity'
    d['modifier_labels']['industrial_capacity_factory']='Military factory output'
    d['modifier_labels']['production_factory_max_efficiency_factor']='Military production efficiency cap'
    d['economic_effect_semantics']='Civilian development uses civilian_factories_productivity, consumed in 00_money_system.txt:469 and6027 for civilian tax/GDP calculations. It is not a flat equal percentage increase in national GDP. Military factory output and production efficiency cap are retained only in the actual defence programme.'
    return d
