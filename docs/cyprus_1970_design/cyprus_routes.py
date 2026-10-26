"""Six historically relevant political routes, each with a bespoke economic wing."""

def M(**values):
    return {'mods':values}

def add_routes(section, focus, either, exclusive):
    parties=[]
    def route(index,ideology,outlook,title,leader,status,formation,politics,policies,economics,effects,note,indices=None):
        slot=len(parties);sec=f'party_{index}'
        parties.append(dict(index=index,indices=indices or [index],ideology=ideology,outlook=outlook,
                            title=title,leader=leader,status=status,formation=formation,note=note))
        section(sec,title,(114+slot*22,0),note)
        suffix=['mandate','organisation','first_a','first_b','follow_a','follow_b','institutions','second_a','second_b','settlement']
        xy=[(0,0),(0,1),(-4,2),(4,2),(-4,3),(4,3),(0,4),(-4,5),(4,5),(0,6)]
        pre=[[],[0],[1],[1],[2],[3],[],[6],[6],[]]
        for k,label in enumerate(politics):
            opts=dict(policies[k]);mods=opts.pop('mods',{})
            node=focus(f'p{index}_{suffix[k]}',label,sec,xy[k],[f'p{index}_{suffix[j]}' for j in pre[k]],
                       mods=mods,party=index,scope='party programme',days=opts.pop('days',35 if k in (0,1,4,5) else 50),
                       requires='Governing subparty '+('/'.join(map(str,indices or [index])))+'; '+formation,**opts)
            node['party_indices']=indices or [index]
        exclusive(f'p{index}_first_a',f'p{index}_first_b');exclusive(f'p{index}_second_a',f'p{index}_second_b')
        # The institution and political settlement are explicit OR joins.
        from_names={n['key']:n for n in focus.__globals__['nodes']}
        either(from_names[f'p{index}_institutions'],f'p{index}_follow_a',f'p{index}_follow_b')
        either(from_names[f'p{index}_settlement'],f'p{index}_second_a',f'p{index}_second_b')
        names=['economic_mandate','economic_a','economic_b','project_a1','project_a2','project_b1','project_b2',
               'finance_review','finance_a','finance_b','finance_a_follow','finance_b_follow','social_investment','national_programme']
        loc=[(0,8),(-6,9),(6,9),(-8,10),(-4,10),(4,10),(8,10),(0,11),(-4,12),(4,12),(-4,13),(4,13),(0,14),(0,15)]
        parents=[['settlement'],['economic_mandate'],['economic_mandate'],['economic_a'],['economic_a'],['economic_b'],['economic_b'],[],
                 ['finance_review'],['finance_review'],['finance_a'],['finance_b'],[],['social_investment']]
        for k,label in enumerate(economics):
            opts=dict(effects[k]);mods=opts.pop('mods',{})
            node=focus(f'p{index}_{names[k]}',label,sec,loc[k],[f'p{index}_{p}' for p in parents[k]],
                       mods=mods,party=index,scope='party economic programme',days=opts.pop('days',50 if k in (1,2,7,12,13) else 35),
                       requires='Governing subparty '+('/'.join(map(str,indices or [index])))+'; '+formation,**opts)
            node['party_indices']=indices or [index]
            if k==7:
                either(node,*[f'p{index}_{p}' for p in ('project_a1','project_a2','project_b1','project_b2')])
            if k==12:
                either(node,f'p{index}_finance_a_follow',f'p{index}_finance_b_follow')
        exclusive(f'p{index}_economic_a',f'p{index}_economic_b');exclusive(f'p{index}_finance_a',f'p{index}_finance_b')

    route(1,'conservatism','Western','Makarios: An Independent Developmental Republic','Makarios III; lawful succession after1977.',
      'Historical government; independent foreign policy despite the current conservative engine slot.',
      'Makarios government or its explicitly designated independent-republic successor.',
      ['The Archbishop-President\'s Mandate','Renew the Makarios Coalition','A Broad Republican Coalition','A Presidential Inner Circle',
       'Keep the Left in the Coalition','Strengthen Presidential Coordination','The Independence Programme',
       'A Secular Civil Service','Retain Church Mediation','A Republic beyond the Presidency'],
      [{},M(stability_factor=.03),{'cost':.5,'mods':{'stability_factor':.04,'political_power_factor':-.02}},M(political_power_factor=.07),
       M(foreign_influence_defense_modifier=.05),M(bureaucracy_cost_multiplier_modifier=-.06),{'settlement':5},
       M(bureaucracy_cost_multiplier_modifier=-.05,research_speed_factor=.02),M(stability_factor=.04,education_cost_multiplier_modifier=.03),M(foreign_influence_defense_modifier=.05)],
      ['The President\'s Development Programme','A Cooperative Rural Economy','Tourism under National Stewardship',
       'Agricultural Cooperative Marketing','Village Roads and Rural Contractors','Cypriot-Owned Coastal Hotels','Local Suppliers for the Visitor Economy',
       'Finance without Political Subordination','Non-Aligned Development Credit','Domestic Cooperative Savings',
       'Publish the Terms of External Loans','Expand Village Credit Societies','Technical Education beyond the Capital','The Independent Development Compact'],
      [{'cost':1}, {'cost':1.5,'mods':{'production_speed_buildings_factor':.06}},
       {'cost':1,'mods':{'office_park_income_tax_modifier':.07,'mdcw_cw_market_exposure':.04}},
       {'cost':.5,'research':'CAT_agriculture'},M(production_speed_infrastructure_factor=.06),M(office_park_income_tax_modifier=.04),M(bureaucracy_cost_multiplier_modifier=-.03),
       {'cost':.5}, {'event':'nonaligned_credit_offer','mods':{'receiving_investment_cost_modifier':-.08,'foreign_influence_defense_modifier':-.03}},
       {'cost':1,'mods':{'interest_rate_multiplier_modifier':-.25,'bureaucracy_cost_multiplier_modifier':.03}},
       M(bureaucracy_cost_multiplier_modifier=-.04),M(stability_factor=.03),{'cost':1,'mods':{'research_speed_factor':.02,'education_cost_multiplier_modifier':.03}},
       {'cost':1.5,'mods':{'production_speed_buildings_factor':.04}}],
      'Cooperative rural development or nationally controlled tourism, then external non-aligned credit versus domestic savings. Political concessions to patrons remain real.')

    route(2,'liberalism','Western','Clerides: A Commercial and Constitutional Republic','Glafkos Clerides; Eniaion milieu, DISY name only from1976.',
      'Historical political milieu; liberal engine mapping is a design abstraction.',
      'A lawful Eniaion/republican mandate; not a rival presidency merely because Clerides negotiates for Makarios.',
      ['A Liberal Republican Mandate','The Eniaion Reform Wing','An Open Commercial Economy','A Regulated Social Market',
       'Commercial Arbitration','Independent Public Regulators','A State Governed by Law',
       'Negotiate Bicommunal Guarantees','Prioritise Central Institutions','A Constitutional Liberal Republic'],
      [{},M(political_power_factor=.03),M(receiving_investment_cost_modifier=-.08,foreign_influence_defense_modifier=-.04),
       {'cost':1,'mods':{'stability_factor':.04}},M(office_park_income_tax_modifier=.04),M(bureaucracy_cost_multiplier_modifier=-.05),
       {'cost':.5,'mods':{'research_speed_factor':.02}},{'settlement':10,'cost':.5},M(bureaucracy_cost_multiplier_modifier=-.05),M(stability_factor=.03)],
      ['A Commercial Strategy for the Island','Shipping, Trade and Professional Services','Competitive Small Manufacturing',
       'Modern Commercial and Shipping Law','Cypriot Accounting and Insurance','Export-Oriented Workshops','Competitive Industrial Supply Contracts',
       'The Rules of Commercial Finance','Open the Door to Foreign Investors','A Domestic Development Bank',
       'Independent Audits and Contract Enforcement','Loans for Cypriot Small Enterprises','Train a Skilled Commercial Workforce','A Mediterranean Commercial Republic'],
      [{'cost':1},{'cost':1,'mods':{'office_park_income_tax_modifier':.07}},
       {'cost':1.5,'mods':{'production_speed_industrial_complex_factor':.07}},
       M(office_park_income_tax_modifier=.03),M(office_park_income_tax_modifier=.03),M(industrial_capacity_factory=.06),M(production_factory_max_efficiency_factor=.05),
       {'cost':.5},{'event':'commercial_investment_offer','mods':{'receiving_investment_cost_modifier':-.10,'foreign_influence_defense_modifier':-.05}},
       {'cost':1.5,'mods':{'interest_rate_multiplier_modifier':-.25,'bureaucracy_cost_multiplier_modifier':.03}},
       M(bureaucracy_cost_multiplier_modifier=-.05),M(production_speed_buildings_factor=.04),
       {'cost':1,'mods':{'research_speed_factor':.04,'education_cost_multiplier_modifier':.04}},
       {'cost':1.5,'mods':{'office_park_income_tax_modifier':.03}}],
      'Services and shipping versus export workshops; international capital versus a domestic lender. Office-income bonuses require actual staffed offices and are not GDP bonuses.')

    route(3,'socialism','Western','EDEK: A Democratic Social Republic','Vassos Lyssarides.',
      'Historical party founded1969.', 'EDEK wins an electoral or constitutional coalition mandate.',
      ['EDEK\'s Democratic Mandate','Organise the Social Movement','Universal Social Provision','Cooperative Self-Help',
       'Community Health Clinics','Worker-Owned Local Enterprises','A Democratic Social Charter',
       'Non-Aligned Solidarity','A European Democratic Opening','A Social Republic of Cyprus'],
      [{},M(stability_factor=.03),{'cost':1,'mods':{'stability_factor':.05,'social_cost_multiplier_modifier':.06}},
       {'cost':.5,'mods':{'production_speed_buildings_factor':.04}},M(stability_factor=.03),M(industrial_capacity_factory=.04),
       {'settlement':5},M(foreign_influence_defense_modifier=.05),M(research_speed_factor=.02),M(stability_factor=.03)],
      ['A Social Development Plan','Public Works and Common Services','A Worker-Cooperative Economy',
       'Municipal Housing and Sanitation','Rural Clinics and Local Transport','Cooperative Workshops','Credit for Worker-Run Enterprises',
       'Paying for Social Development','A Broad-Based Social Development Fund','Borrow for the First Development Plan',
       'Professional Public Procurement','Publish a Repayment and Spending Schedule','Technical Schools and Adult Training','A Productive Social Compact'],
      [{'cost':1},{'cost':1.5,'mods':{'production_speed_buildings_factor':.07,'social_cost_multiplier_modifier':.04}},
       {'cost':1,'mods':{'industrial_capacity_factory':.07}},
       M(stability_factor=.03),M(production_speed_infrastructure_factor=.02),M(production_factory_max_efficiency_factor=.05),M(interest_rate_multiplier_modifier=-.15),
       {'cost':.5},{'cost':1,'mods':{'tax_gain_multiplier_modifier':.05,'political_power_factor':-.03}},
       {'event':'social_development_loan','mods':{'receiving_investment_cost_modifier':-.08,'foreign_influence_defense_modifier':-.03}},
       M(bureaucracy_cost_multiplier_modifier=-.06),M(interest_rate_multiplier_modifier=-.15),
       {'cost':1.5,'mods':{'research_speed_factor':.03,'education_cost_multiplier_modifier':.05}},
       {'cost':1,'mods':{'production_speed_buildings_factor':.04,'stability_factor':.02}}],
      'Funded public works or worker cooperatives; a tax-backed development fund or an actual loan with debt and repayment. Additional services have visible fiscal cost.')

    route(4,'communist_state','Emerging','AKEL: Labour, Industry and Independence','Ezekias Papaioannou.',
      'Historical party; one-party rupture is explicitly alternate history.',
      'AKEL wins office; monopoly-party rule requires a separately chosen constitutional rupture.',
      ['An AKEL Government','The Organised Workers\' Movement','A Parliamentary Left Coalition','A Single-Party Transformation',
       'Trade Unions within the Republic','Centralise Party Administration','Control of the Commanding Heights',
       'An Independent Cypriot Left','A Soviet Economic Compact','A Workers\' Republic on the Island'],
      [{},M(political_power_factor=.04),{'cost':.5,'mods':{'stability_factor':.04}},
       {'stability':-.04,'tension':5,'mods':{'political_power_factor':.07,'research_speed_factor':-.01},'note':'Explicit alternate authoritarian break; not a claim that historical AKEL automatically pursued dictatorship.'},
       M(industrial_capacity_factory=.04),M(bureaucracy_cost_multiplier_modifier=-.05),{'cost':1},
       M(foreign_influence_defense_modifier=.06),{'event':'soviet_compact_offer','mods':{'production_speed_industrial_complex_factor':.05,'foreign_influence_defense_modifier':-.06}},M(stability_factor=.03)],
      ['A Workers\' Development Programme','A Public Light-Industry Plan','A Cooperative Mixed Economy',
       'Food Processing under Public Ownership','A Small Engineering and Repair Sector','Worker-Managed Production Boards','Agricultural Producer Cooperatives',
       'Finance the Productive Economy','Eastern Equipment and Credit Agreements','An Island-Funded Development Budget',
       'A Transparent Equipment Procurement Office','Reinvest Public Enterprise Surpluses','Workers\' Technical Education','Labour and Production on Cypriot Terms'],
      [{'cost':1},{'cost':1.5,'mods':{'production_speed_industrial_complex_factor':.06,'bureaucracy_cost_multiplier_modifier':.04}},
       {'cost':1,'mods':{'industrial_capacity_factory':.06,'stability_factor':.02}},
       M(industrial_capacity_factory=.04),M(production_factory_max_efficiency_factor=.06),M(production_factory_max_efficiency_factor=.05),{'cost':.5,'research':'CAT_agriculture'},
       {'cost':.5},{'event':'eastern_equipment_credit','mods':{'receiving_investment_cost_modifier':-.10,'foreign_influence_defense_modifier':-.05}},
       {'cost':1.5,'mods':{'foreign_influence_defense_modifier':.05,'political_power_factor':-.03}},
       M(production_speed_industrial_complex_factor=.02),M(production_speed_buildings_factor=.04),
       {'cost':1,'mods':{'research_speed_factor':.03,'education_cost_multiplier_modifier':.04}},
       {'cost':1.5,'mods':{'industrial_capacity_factory':.05}}],
      'Public food processing and repair industry versus worker-managed cooperatives; Eastern credit versus domestic funding. No heavy-industrial great power or free factories.')

    route(20,'Nat_Populism','Nationalist','The Progressive Front: A Civilian Enosis Mandate','Nikos Sampson and the Progressive Front milieu.',
      'Historical hardline electoral milieu; engine category is an abstraction.',
      'An electoral mandate; winning office does not itself authorise a coup or violence.',
      ['A National Popular Mandate','Mobilise the Progressive Front','Pursue Enosis through Negotiation','Build a Confrontational Mass Campaign',
       'Submit Terms to a Conference','Mobilise the Street Organisations','A National Programme before Parliament',
       'Accept a Protected Independent Republic','Continue the Enosis Campaign','A National Mandate Put to the Test'],
      [{},M(political_power_factor=.04),{'cost':.5,'event':'enosis_debate'},{'tension':10,'mods':{'war_support_factor':.06,'foreign_influence_defense_modifier':-.04}},
       {'settlement':5},M(political_power_factor=.03,police_cost_multiplier_modifier=.06),{'cost':.5},M(stability_factor=.04),{'tension':5,'event':'enosis_debate'},M(political_power_factor=.03)],
      ['A National Enterprise Programme','Cypriot Small Enterprise First','An Economic Bridge to Greece',
       'Local Building and Repair Firms','Support Rural Producer Associations','Harmonise Commercial Standards','Seek Greek Supplier Agreements',
       'The Terms of National Development','Transparent National Development Tenders','Concessions to Loyal Commercial Patrons',
       'An Independent Contracts Inspectorate','Consolidate the Government\'s Business Base','Vocational Training for Local Enterprise','A National Enterprise Compact'],
      [{'cost':1},{'cost':1,'mods':{'production_speed_buildings_factor':.06}},
       {'event':'greek_commercial_offer','mods':{'receiving_investment_cost_modifier':-.07,'foreign_influence_defense_modifier':-.05}},
       M(production_speed_industrial_complex_factor=.05),{'cost':.5,'research':'CAT_agriculture'},M(office_park_income_tax_modifier=.05),M(industrial_capacity_factory=.05),
       {'cost':.5},{'cost':1,'mods':{'bureaucracy_cost_multiplier_modifier':-.05}},M(political_power_factor=.06,bureaucracy_cost_multiplier_modifier=.06),
       M(production_speed_buildings_factor=.03),M(office_park_income_tax_modifier=.04,stability_factor=-.02),
       {'cost':1,'mods':{'research_speed_factor':.02,'education_cost_multiplier_modifier':.03}},
       {'cost':1.5,'mods':{'production_speed_buildings_factor':.01}}],
      'A genuinely civilian nationalist alternative: local enterprise or Greek integration, then open tenders versus patronage. Enosis remains contingent on negotiation or a separately chosen confrontation.')

    route(22,'Nat_Autocracy / Nat_Fascism','Nationalist','The Enosis Coup and Security Regime','Georgios Grivas in the armed-movement phase; Nikos Sampson for the historical1974 coup presidency.',
      'Historical armed and coup milieu combined into one extensive route.',
      'Successful coup/revolutionary regime; EOKA B only from1971, Grivas succession after January1974; historical1974 coup requires Greek-junta involvement.',
      ['A Presidency Born of the Coup','The Emergency Command Council','Rely on Mainland Officers','Appoint an Island-Based Command',
       'Coordinate with the Greek Junta','Consolidate a Domestic Officer Corps','The Coup Government\'s Claim to Rule',
       'Restore Constitutional Government','Entrench the Emergency Regime','The Future of the Coup Presidency'],
      [{},M(political_power_factor=.04),M(army_org_factor=.05,foreign_influence_defense_modifier=-.08),{'cost':1,'mods':{'army_org_factor':.03}},
       M(planning_speed=.08),M(foreign_influence_defense_modifier=.04),{'stability':-.05,'tension':15,'event':'turkish_crisis_response'},
       M(stability_factor=.04),M(political_power_factor=.04,police_cost_multiplier_modifier=.12),M(drift_defence_factor=.06)],
      ['An Emergency Economic Directorate','Secure Civilian Supply First','Prioritise Military Readiness',
       'Food and Fuel Distribution Contracts','Keep Essential Civil Works Running','Dispersed Arms Repair Workshops','Pay and Train the Emergency Reserve',
       'Who Pays for the Emergency State?','A Temporary Reconstruction Levy','Seek Mainland Emergency Credit',
       'Publish an Emergency Budget and Sunset Date','Accept the Conditions of Mainland Credit','Repair Transport and Medical Supply Networks','From Emergency Rule to a Sustainable State'],
      [{'cost':1},{'cost':1.5,'mods':{'stability_factor':.03,'production_speed_buildings_factor':.05}},
       {'cost':1,'mods':{'army_defence_factor':.06,'army_personnel_cost_multiplier_modifier':.08,'production_speed_buildings_factor':-.04}},
       M(fuel_gain_factor=.06),M(production_speed_infrastructure_factor=.06),M(industrial_capacity_factory=.08),M(army_org_factor=.03),
       {'cost':.5},{'cost':1,'mods':{'tax_gain_multiplier_modifier':.05,'stability_factor':-.02}},
       {'event':'mainland_emergency_loan','mods':{'receiving_investment_cost_modifier':-.10,'foreign_influence_defense_modifier':-.08}},
       M(bureaucracy_cost_multiplier_modifier=-.05),M(political_power_factor=.03),
       {'cost':1,'mods':{'army_org_factor':.02,'social_cost_multiplier_modifier':.03}},
       {'cost':1.5,'mods':{'army_defence_factor':.03}}],
      'A hardline regime can preserve civilian supply or divert capacity to readiness; taxes versus foreign dependence. Violence and expulsion retain separate lasting consequences, never economic rewards.',indices=[21,22])
    return parties
