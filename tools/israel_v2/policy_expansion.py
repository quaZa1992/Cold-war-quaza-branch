# IMPERIA COLD WAR — Deeper Israeli party policies and substantive rewards.
"""Expand the review-only 1970 design. No loaded mod file is written here.

Historical acts, contemporary proposals, later precedents and RP alternatives
are distinguished. Opinion is supplementary, never a domestic main reward.
"""
def expand(api):
    nodes,groups,sources=api['NODES'],api['GROUPS'],api['SOURCES']
    f,E,asset,paid,cash,debt,research,budget,unlock,exclusive=(api[k] for k in ('f','E','asset','paid','cash','debt','research','budget','unlock','exclusive'))
    by={n['id']:n for n in nodes}
    internal={'Labor Unions Opinion','Small and Medium Business Owners Opinion','Industrial Conglomerates Opinion','Religious Institutions Opinion','Farmers Opinion','The Military Opinion','Intelligence Community Opinion'}
    removed=[]
    for n in nodes:
        old=n['effects']
        dropped=[e for e in old if e['label'] in internal and e.get('tone')=='gain']
        if dropped:removed.append(dict(focus=n['id'],effects=dropped))
        n['effects']=[e for e in old if e not in dropped]

    def m(key,value,label,unit='%'):
        inverse=key in {'inflation_cost_multiplier_modifier','bureaucracy_cost_multiplier_modifier','education_cost_multiplier_modifier','social_cost_multiplier_modifier','health_cost_multiplier_modifier'}
        return E(label,f'{value*100:+g}{unit}','gain' if (value<0 if inverse else value>0) else 'cost',native_key=key,amount=value,scope='programme')
    def change(key,mods=None,effects=None,description=None,label=None,cost=0):
        n=by['ISR2_'+key]
        if label:n['label']=label
        if description:n['description']=description
        if effects is not None:n['effects']=paid(cost)+effects
        if mods is not None:
            n['modifiers']=mods
            if mods and n['programme']=='One-time achievement; national assets remain':n['programme']='Governing programme'
        return n
    def add(g,key,label,x,y,description,**kwargs):
        f(g,key,label,x,y,description,**kwargs)
        n=nodes[-1]
        for e in n['effects']:
            if e.get('scope')=='programme' and e.get('native_key'):
                n['modifiers'][e['native_key']]=e['amount']
        return n
    def heading(rows,text):return [dict(e,heading=text) for e in rows]
    def state_burden(resistance=5,garrison=15):
        return [E('Selected Occupied State: Resistance Target',f'+{resistance} percentage points','cost'),E('Selected Occupied State: Local Garrison Requirement',f'+{garrison}%','cost')]
    def pal_pressure():
        return heading([E('Office Productivity','-4% per pressure tier','cost'),E('Bureaucracy Cost','+4% per pressure tier','cost'),E('Stability','-2% per pressure tier','cost')],'Palestine: Affected West Bank or Gaza Core')

    sources.extend([
        dict(id='yanai',title='Akevot: original political-risk guarantee records, 1967-1984',url='https://www.akevot.org.il/en/article/political-guarantee/',note='1967-1969 guarantees and cabinet decisions, 1970 draft and later Yanai activity. The company name is not backdated as an established 1970 operator.'),
        dict(id='begin77',title='Begin archive: prospective government programme, 18 January 1977',url='https://db.begincenter.org.il/en/article/likud-govts-vision-for-israel/',note='Later policy proposals, including welfare, housing, investor access and essential-service arbitration; not an enacted 1970 Gahal programme.'),
        dict(id='fx77',title='Bank of Israel: Annual Report 1977, external reform',url='https://www.boi.org.il/media/3ywhodod/pe_3.pdf',note='Contemporaneous account of the 1977 currency reform, float and liberalisation; adopting it earlier is an RP alternative.'),
        dict(id='tax75',title='Bank of Israel: Annual Report 1975, public sector',url='https://www.boi.org.il/media/01hdep0x/pe_10.pdf',note='1975 direct-tax reform, broader base and family-transfer reform. Later precedent, not automatic 1970 law.'),
        dict(id='nii',title='National Insurance Institute: operative dates of child benefits',url='https://www.btl.gov.il/Publications/Habituah_haleumi/Documents/charth11-e.pdf',note='Large-family benefits from 1959, employees benefits from 1965, veterans benefits from April 1970, general reform in 1975.'),
        dict(id='registration70',title='JTA: Law of Return amendment debate, 12 March 1970',url='https://www.jta.org/archive/law-of-return-amendment-adopted-by-51-14-vote-passage-stirs-stormy-debate',note='Contemporaneous compromise and Orthodox objections. Certification of status is distinct from citizenship eligibility.'),
        dict(id='biu',title='Bar-Ilan University: historical milestones',url='https://www.biu.ac.il/en/about-bar-ilan/overview/historical-milestones',note='Established in 1955, recognised in 1969, with science/mathematics and regional teaching. These are the basis of the funded laboratory policy.'),
        dict(id='mafdal_history',title='Israel Democracy Institute: National Religious Party',url='https://en.idi.org.il/israeli-elections-and-parties/parties/national-religious-party/',note='Religious services, welfare, Interior Ministry and the changing balance between established leadership and territorial activists. Retrospective institutional history.'),
        dict(id='gush_archive',title='National Library of Israel: Gush Emunim collection, 1974-1978',url='https://www.nli.org.il/he/archives/nnl_archive_al990032468800205171/NLI',note='The named organisation is later. Early Mafdal activism does not imply Gush Emunim exists in January 1970.'),
        dict(id='allon',title='US FRUS: the Allon territorial concept and Jordanian talks',url='https://history.state.gov/historicaldocuments/frus1969-76v26/d168',note='Official record and notes describing earlier Allon ideas. Proposals were contested, not an automatic adopted peace settlement.'),
        dict(id='kol70',title='JTA: Moshe Kol tourism and investor programme, 1 April 1970',url='https://www.jta.org/archive/moshe-kol-outlines-plans-for-tourist-resorts-and-program-for-investors-in-tourism',note='Contemporary resort plans in Sinai and hotel-financing guarantees. A proposal is not a completed resort or Egyptian consent.'),
        dict(id='renewal',title='JDC Archives: Project Renewal files, 1978 onward',url='https://archives.jdc.org/our-collections/finding-aids/new-york-office/1975-1989/countries-and-regions-israel-zim/',note='Primary archival holdings distinguish the later programme from the 1970 start. Earlier neighbourhood renewal is a counterfactual choice.'),
        dict(id='unemployment',title='National Insurance Institute: unemployment-insurance operative dates',url='https://www.btl.gov.il/SiteCollectionDocuments/chart-e-08.pdf',note='Contributions began in April 1970, benefits in January 1973. The funded insurance programme is later than the starting campaign date.'),
        dict(id='civil_service71',title='State Comptroller: voluntary national service in education',url='https://library.mevaker.gov.il/sites/DigitalLibrary/Pages/Reports/2641-33.aspx?AspxAutoDetectCookieSupport=1',note='Official retrospective describes the NRP initiative in 1971, government instructions and the organisation operating from 1972.'),
        dict(id='dayan_bridges',title='JTA: Dayan and open bridges, 21 August 1969',url='https://www.jta.org/archive/dayan-says-open-bridges-policy-is-serving-west-bank-arab-population-well',note='Contemporaneous account of crossings and trade; a reported ministerial claim, not proof that all residents benefited or that Jordan must cooperate in RP.'),
    ])

    # Replace weak early rewards before extending the programmes.
    change('package_deal',mods={'production_factory_efficiency_gain_factor':.05,'social_cost_multiplier_modifier':.02},cost=.3,
        effects=[m('production_factory_efficiency_gain_factor',.05,'Production Efficiency Growth'),E('Social Spending Cost','+2%','cost',native_key='social_cost_multiplier_modifier',amount=.02,scope='programme'),unlock('Conclude a Tripartite Wage Settlement')])
    change('cash_wages',mods={'stability_factor':.06,'offices_productivity':.04},cost=1.5,
        effects=[E('Stability','+6%','gain',native_key='stability_factor',amount=.06,scope='programme'),m('offices_productivity',.04,'Office Productivity')],
        description='A cash wage settlement sustains household purchasing power and the local service economy. The treasury pays immediately, using money that could otherwise finance the development programme.')
    change('herut_charter',mods={'stability_factor':.05,'social_cost_multiplier_modifier':.06},cost=.8,
        effects=asset('Selected Israeli Core State','Infrastructure')+[m('stability_factor',.05,'Stability'),E('Social Spending Cost','+6%','cost',native_key='social_cost_multiplier_modifier',amount=.06,scope='programme')],
        description='Tie Herut\'s social appeal to a paid connection for a development-town neighbourhood. The road and public-service obligation remain more useful than a passing improvement in business sentiment.')
    by['ISR2_herut_charter']['requirements'].append('An eligible owned and controlled Israeli core state.')
    change('mafdal_budget',label='Religious-Zionist Development Credit',mods={'education_cost_multiplier_modifier':.04},cost=1.8,
        effects=asset('Negev','Agricultural District')+asset('Negev','Civilian Factory')+[E('Education Cost','+4%','cost',native_key='education_cost_multiplier_modifier',amount=.04,scope='programme')],
        description='Fund the religious workers\' agricultural and manufacturing institutions alongside the party\'s educational commitments. Development credit buys a productive cooperative base and leaves a continuing school budget.')
    change('mizrahi_coops',label='Packing Stations for the Cooperatives',cost=1.1,mods={},
        effects=asset('Negev','Office District')+[research('Agriculture')],
        description='Cooperative farmers need packing, marketing and a dependable commercial office. Extend the network beyond its first workshop rather than announcing the same loan twice.')
    change('communal_budget',mods={'stability_factor':.05,'education_cost_multiplier_modifier':.08,'social_cost_multiplier_modifier':-.05},cost=.5,
        effects=[m('stability_factor',.05,'Stability'),E('Education Cost','+8%','cost',native_key='education_cost_multiplier_modifier',amount=.08,scope='programme'),E('Social Spending Cost','-5%','gain',native_key='social_cost_multiplier_modifier',amount=-.05,scope='programme')])
    change('community_clinics',mods={'stability_factor':.05,'health_cost_multiplier_modifier':-.06},cost=.6,
        effects=[m('stability_factor',.05,'Stability'),m('health_cost_multiplier_modifier',-.06,'Healthcare Cost'),budget('Development-Town Clinic Grant',-.005)],
        description='Coordinate neighbourhood clinics, referral services and purchasing instead of sending every case to a distant central facility. The health service saves part of its bill while the treasury funds a standing local grant.')
    by['ISR2_mashav']['effects'].append(dict(research('Agriculture'),heading='If they accept: Israel'))

    # Leave real parties visible, but reserve vertical space for unequal depth.
    for g in groups:
        if g['id'] in ['liberals','haolam','rakah','state_list']:new_row=34
        elif g['id'] in ['mapam','maki','free_center']:new_row=44
        else:continue
        delta=new_row-g['origin'][1]
        g['origin'][1]=new_row
        for n in nodes:
            if n['group']==g['id']:n['xy'][1]+=delta

    # Alignment: social development, public finance and contested territorial rule.
    add('alignment','labor_social_review','Hear the Neighbourhood Protest',0,5,
        'The development programme has left some households outside its benefits. Fund local repairs and publish a response to neighbourhood demands rather than reducing them to a dispute with party organisers.',
        pre=['histadrut_balance'],cost=.7,effects=asset('Selected Israeli Core State','Infrastructure'),icon='generic_working_class_family',sources=['labour','economy'],status='Plausible alternative',history_note='Draws on the social conflict of the early 1970s. No protest movement or 1971 crisis is forced into existence.')
    add('alignment','labor_social_priority','A Development-Town Employment Budget',-3,6,
        'Put the next major appropriation into civilian employment in the development towns. It creates workplaces and an enduring public-service bill instead of another territorial commitment.',
        pre=['labor_social_review'],cost=2,effects=asset('Negev','Office District',2),mods={'social_cost_multiplier_modifier':.04},icon='focus_public_housing',sources=['economy'],programme='Development priority')
    add('alignment','labor_yanai','Guarantee Investment across the Green Line',3,6,
        'Political uncertainty makes banks reluctant to finance projects in occupied territory. A state guarantee lowers the initial bill while putting the treasury at risk if the project is later lost or relinquished.',
        pre=['labor_social_review'],cost=.2,effects=[unlock('Territorial Political-Risk Insurance'),E('Public Share of Each of Two 1.5%-GDP Projects','1.5% becomes 1.0% of annual GDP','gain'),E('Required Private Project Capital','+0.5% of annual GDP per project','neutral'),budget('Guarantee Administration Expense',-.01,52),E('Gross Maximum Insured Claim','1.6% of annual GDP','cost'),E('Maximum Additional Treasury Call after Full Cash Reserve','1.4% of annual GDP','cost')],
        icon='agricultural_banks',sources=['yanai'],status='Contemporary policy proposal',programme='Funded guarantee book: 52 weeks',
        requirements=['Israel controls at least one eligible non-core settlement area.','Each project requires actual accepted private financing of 0.5% of annual GDP.'],mechanics=['A guarantee is not construction money: each 1.5%-GDP project needs 1.0% from the treasury and 0.5% actually committed through the investment system. It cannot be delivered while the private share is missing. At most two insured projects in one national book; each can trigger up to 0.8% of quoted GDP in liability after actual loss of control or agreed withdrawal. No withdrawal is forced. The 0.2%-GDP cash reserve is held, not also spent as a premium. The weekly provision is an expense. After cover and outstanding claims end, only the unused actual cash reserve returns once. No new cover after leaving office, but completed contracts run to expiry and honour claims. Host penalties and shared settlement caps remain. The 1967-1969 guarantees precede the later operating company Yanai.'])
    exclusive('labor_social_priority','labor_yanai')
    add('alignment','labor_long_schoolday','Keep the Development-Town School Open Longer',-3,7,
        'A longer school day and funded technical teaching help children whose families cannot buy private support. The benefit is a larger trained cohort, paid through the education budget.',
        pre=['labor_social_priority'],cost=.8,effects=[research('Industry',2)],mods={'education_cost_multiplier_modifier':.06},icon='school_is_in',sources=['labour'],status='Plausible alternative')
    add('alignment','labor_permit_market','Dayan\'s Employment Permit Market',3,7,
        'Permit employment in Israel while retaining a separate military administration in the occupied territories. Israeli firms gain access to labour and commerce, while unequal access and policing remain a burden.',
        pre=['labor_yanai'],cost=.5,mods={'offices_productivity':.04,'bureaucracy_cost_multiplier_modifier':.04},effects=state_burden(4,5),icon='gaza_civic_organizations',sources=['labour','dayan_bridges','occupation'],status='Contemporary policy',
        requirements=['Israel controls the West Bank or Gaza.'],mechanics=['Applies the state burden only in participating controlled non-core areas. No population or workforce-size change. Crossings into Jordan remain dependent on that government actually opening its side.'])
    add('alignment','labor_tax_base','The Ben-Shahar Tax Base',-3,8,
        'Broaden the recorded tax base and replace special exemptions with a more legible system. Collection improves, but the reform needs assessors and confronts households accustomed to the old allowances.',
        pre=[],cost=.7,effects=[m('population_tax_income_multiplier_modifier',.08,'Personal Tax Income'),m('corporate_tax_income_multiplier_modifier',.05,'Corporate Tax Income')],mods={'bureaucracy_cost_multiplier_modifier':.03},icon='generic_banking_legislation',sources=['tax75'],status='Later historical precedent',history_note='The enacted reform belongs to 1975. Choosing it earlier is an alternate policy, not a 1970 starting law. It does not require a social-spending or settlement priority.')
    add('alignment','labor_valley','Fortified Communities in the Jordan Valley',3,8,
        'Concentrate the territorial programme on a defended valley corridor. Agricultural and military installations create a durable commitment whose expense and Palestinian consequences survive the construction ceremony.',
        pre=['labor_permit_market'],cost=1.6,effects=asset('West Bank','Agricultural District')+asset('West Bank','Land Fort',2)+state_burden(5,15)+pal_pressure()+[budget('Valley Community Security',-.015)],icon='generic_paramilitary',sources=['allon','occupation'],status='Contemporary policy proposal',requirements=['Israel controls the West Bank and an eligible fort province.'],mechanics=['Fort slots are granted to the state before province construction. This is one controlled settlement tier within the shared tier/pressure caps. It does not annex the whole West Bank or force a Jordanian agreement.'])
    add('alignment','labor_indexed_savings','Offer an Indexed Development Note',-3,9,
        'Put a defined subscription behind a funded construction programme while protecting its subscribers. Capital and faster works arrive together, with an explicit additional debt-service bill on this issue.',
        pre=['labor_tax_base'],cost=.4,effects=[cash(2),debt(2),budget('Indexed Note Service Supplement',-.001,104)],mods={'production_speed_buildings_factor':.10},icon='generic_financial_markets',sources=['economy','tax75'],status='Plausible alternative',programme='Funded construction programme: 104 weeks',mechanics=['The supplement applies to this issue, not the entire national debt stock. Construction support expires after 104 weeks. The public principal and ordinary MD debt interest remain until repayment; neither is cancelled by a change of government.'])
    add('alignment','labor_procurement_ceiling','Compare the Defence Development Bills',3,9,
        'Ask the finance ministry and defence engineers to compare the next major development commitments. A real procurement review can reduce two project bills without creating weapons through an accounting entry.',
        pre=[],cost=.3,effects=[E('Next Domestic Tank Project: Setup Cost','-0.5% of annual GDP','gain'),E('Next Domestic Aircraft Project: Setup Cost','-0.5% of annual GDP','gain')],icon='generic_investigate_corruption',sources=['economy','merkava'],mechanics=['Each discount is used once against an actual paid project. No cash refund for an already completed project and no recurring free grant. No settlement project is required to review national procurement.'])
    add('alignment','labor_family_payments','Unify the Family Payment System',-3,10,
        'Replace overlapping allowances with a common payment system. Simpler administration and a wider social settlement come with larger continuing family commitments.',
        pre=['labor_tax_base'],cost=.5,mods={'bureaucracy_cost_multiplier_modifier':-.04,'social_cost_multiplier_modifier':.08,'stability_factor':.08},icon='generic_working_class_family',sources=['nii','tax75'],status='Later historical precedent',history_note='Uses the 1975 family-transfer reform as a later precedent. The 1970 veterans allowance and earlier family allowances are different schemes.')
    jordan=add('alignment','labor_jordanian_option','Negotiate the Jordanian Option',0,10,
        'Seek a Jordanian partner for a territorial settlement rather than treating continued military rule as the permanent answer. The opening offer funds border liaison; actual borders require a separately agreed treaty.',
        pre=[],effects=[unlock('Offer a Jordanian Border Liaison')],icon='israel_jordan_flags',sources=['allon'],status='Contemporary policy proposal',programme='Territorial mandate',
        mechanics=['No prescribed state transfer or automatic peace. If accepted, the limited liaison lasts 104 weeks. Future territorial terms must be accepted by the actual RP governments.'])
    for country in ['Israel','Jordan']:
        jordan['effects']+=heading(paid(.3)+[budget('Border Liaison Expense',-.005,104),E('National Spirit','Jordanian Border Liaison, 104 weeks','gain'),E('Police Cost','-5%','gain'),E('Personnel Cost','-3%','gain')],'If they accept: '+country)
    add('alignment','labor_functional_rule','Dayan\'s Functional Administration',3,10,
        'Retain military authority while connecting the occupied economy more closely to Israel. Commercial benefits do not resolve political status, and continuing coercive administration carries its own security bill.',
        pre=[],cost=.6,mods={'offices_productivity':.05,'police_cost_multiplier_modifier':.06,'bureaucracy_cost_multiplier_modifier':.04},effects=state_burden(6,10),icon='collaborate_local_elites',sources=['labour','occupation'],status='Plausible alternative',programme='Territorial mandate',requirements=['Israel controls the West Bank or Gaza.'],mechanics=['No automatic naturalisation, core or sovereignty transfer. The state effects apply only in participating controlled non-core territories. The mandate does not require earlier settlement construction or a compulsory historical sequence.'])
    exclusive('labor_jordanian_option','labor_functional_rule')
    add('alignment','labor_job_insurance','Fund Unemployment Insurance',-3,11,
        'Insure workers against the interruption of employment rather than promising that no job can ever disappear. A funded transition gives retraining a practical place in industrial change.',
        pre=['labor_family_payments'],cost=.6,mods={'production_factory_efficiency_gain_factor':.05,'social_cost_multiplier_modifier':.05},effects=[research('Industry')],icon='generic_workers_rights',sources=['unemployment','labour'],status='Later historical precedent',history_note='Contributions started in April 1970 and benefits in January 1973. Earlier introduction of the full benefit is an alternative, not an automatic starting entitlement.')
    add('alignment','labor_urban_works','A Second Employment Centre in the South',-3,12,
        'The social programme now has schools, insurance and a tax base. Complete it with a paid commercial and industrial connection in the south, rather than a final declaration of party unity.',
        pre=['labor_job_insurance'],cost=2.2,effects=asset('Negev','Civilian Factory')+asset('Negev','Office District')+asset('Negev','Infrastructure'),icon='construction_engineering',sources=['economy'],days=70)

    # Gahal: liberal reform, a social legislative programme and territorial choices.
    add('gahal','gahal_investors','Convene the Overseas Investors',-3,4,
        'Present investors with defined tenders and transparent access to government contracts. A conference can improve the terms of investment only while its service and guarantee commitments remain funded.',
        pre=['national_bargain'],cost=.5,mods={'receiving_investment_cost_modifier':-.08},effects=[research('Industry')],icon='foreign_diplomacy',sources=['begin77'],status='Later historical proposal',history_note='A 1977 programme proposal adapted as an earlier alternative for a Gahal cabinet.')
    add('gahal','gahal_arbitration','Compulsory Arbitration in Essential Services',3,4,
        'Send essential-service wage disputes to binding national arbitration. Production and repairs become more predictable at the price of curtailing strike action and provoking organised resistance.',
        pre=['supplier_competition'],cost=.4,mods={'industrial_capacity_factory':.05,'industry_repair_factor':.15,'stability_factor':-.04},icon='generic_union_agreement',sources=['begin77'],status='Later historical proposal')
    add('gahal','gahal_rental_sites','Connect the Rental-Housing Sites',-3,5,
        'Private rental construction still needs roads and public utilities. Put the public part of the housing programme into the ground instead of treating an investors conference as completed homes.',
        pre=['gahal_investors'],cost=.9,effects=asset('Selected Israeli Core State','Infrastructure',2),icon='generic_construct_public_housing',sources=['begin77'],status='Later historical proposal',requirements=['An eligible owned and controlled Israeli core state.'])
    add('gahal','gahal_health_bill','A National Health Insurance Bill',3,5,
        'Offer a common insurance arrangement beyond compulsory membership in a party-linked health network. Consolidated administration can save money, but extending cover requires a continuing public provision.',
        pre=['herut_charter'],cost=1,mods={'health_cost_multiplier_modifier':-.10},effects=[budget('Extended Health Cover Provision',-.015)],icon='generic_healthcare',sources=['begin77'],status='Later historical proposal')
    add('gahal','gahal_big_bang','Ehrlich\'s Currency Liberalisation',-3,6,
        'Open access to foreign currency and borrowing in one decisive reform. Capital access improves, while the economy assumes greater market exposure and a higher cost of inflation.',
        pre=['gahal_rental_sites'],cost=.6,mods={'receiving_investment_cost_modifier':-.12,'offices_productivity':.05,'mdcw_cw_market_exposure':.15},effects=[m('inflation_cost_multiplier_modifier',.08,'Inflation Spending Multiplier')],icon='generic_financial_markets',sources=['fx77'],status='Later historical precedent',programme='Currency reform',history_note='Based on the October 1977 reform. Its historical risks are part of the choice; no exchange rate or war is forced in 1970.')
    add('gahal','gahal_managed_credit','Keep a Managed Capital Account',0,6,
        'Preserve controlled access to external credit while widening domestic borrowing. The treasury accepts the licensing establishment in exchange for less exposure to sudden movements of capital.',
        pre=['gahal_rental_sites'],cost=.4,mods={'interest_rate_multiplier_modifier':-.25,'mdcw_cw_market_exposure':-.08,'bureaucracy_cost_multiplier_modifier':.04},icon='economic_protectionism',sources=['fx77'],status='Plausible alternative',programme='Currency reform')
    exclusive('gahal_big_bang','gahal_managed_credit')
    add('gahal','gahal_daily_workers','Equal Terms for Daily and Monthly Workers',3,6,
        'Give daily-paid workers enforceable contract and insurance terms instead of a weaker route into the same workplace. More predictable employment improves industrial organisation while increasing social commitments.',
        pre=['gahal_health_bill'],cost=.5,mods={'production_factory_efficiency_gain_factor':.06,'social_cost_multiplier_modifier':.05},icon='generic_workers_rights',sources=['begin77'],status='Later historical proposal')
    add('gahal','gahal_renewal','Renew a Distressed Neighbourhood',-3,7,
        'Work on the neighbourhood as a whole: transport, employment services and public facilities. A local partnership can make the programme more effective without sending its civilian funds into the arms budget.',
        pre=['gahal_rental_sites'],cost=1.8,effects=asset('Selected Israeli Core State','Office District')+asset('Selected Israeli Core State','Infrastructure'),mods={'stability_factor':.06,'social_cost_multiplier_modifier':.04},icon='focus_public_housing',sources=['renewal','begin77'],status='Later historical precedent',history_note='The later Project Renewal precedent belongs to 1977-1978 onward. Earlier adoption is counterfactual and does not rename the 1970 government.')
    add('gahal','gahal_disposal','Sell a Second Commercial Holding',0,7,
        'A second disposal brings another immediate receipt and gives up another future public dividend. Publishing the sale does not make the state richer by the same amount every time a cabinet returns to office.',
        pre=[['gahal_big_bang','gahal_managed_credit']],effects=[cash(2),budget('Lost Public Enterprise Dividend',-.015)],icon='generic_privatization',sources=['begin77','fx77'],status='Plausible alternative',programme='One-time sale; permanent dividend loss',mechanics=['A second specified existing holding, sold once. The recurring loss persists after a government change. No arbitrary deletion of an actual industrial building.'])
    add('gahal','gahal_settler_entitlement','Civilian Settlement Entitlements',3,7,
        'Give civilian settlers a funded farm, a commercial office and access infrastructure in territory Israel controls. The state gains productive assets while hardening a costly and contested territorial commitment.',
        pre=['national_bargain'],cost=2.1,effects=asset('West Bank','Agricultural District')+asset('West Bank','Office District')+asset('West Bank','Infrastructure')+state_burden(8,20)+pal_pressure()+[budget('Civilian Settlement Security',-.02)],icon='jewish_sites_isr',sources=['begin77','occupation'],status='Later historical proposal',requirements=['Israel controls the West Bank.'],mechanics=['Counts as one tier in the common controlled settlement/Palestinian-pressure system. No host consent, host benefit, free core or automatic annexation.'])
    add('gahal','gahal_ministries','Merge Overlapping Government Departments',0,8,
        'Reduce overlapping ministerial establishments while retaining the service desks that firms and households actually use. Reorganisation costs money before the smaller establishment begins to save it.',
        pre=['gahal_disposal'],cost=.7,mods={'bureaucracy_cost_multiplier_modifier':-.08},icon='civil_service',sources=['begin77'],status='Later historical proposal')
    add('gahal','gahal_pensions','A Portable Pension Commitment',3,8,
        'Employment should not trap a household inside a particular party-linked institution. A portable pension commitment broadens economic mobility while leaving the state to fund its guarantees.',
        pre=['gahal_daily_workers'],cost=.6,mods={'civilian_factories_productivity':.05,'social_cost_multiplier_modifier':.06},icon='generic_working_class_family',sources=['begin77'],status='Later historical proposal')
    autonomy=add('gahal','gahal_local_autonomy','Offer Local Autonomy without a Border Verdict',3,9,
        'A civilian autonomy offer can separate municipal powers from the cabinet\'s sovereignty claim. A Palestinian RP government decides whether the proposed service agreement is worth accepting; settlement permission is not part of it.',
        pre=[],effects=[unlock('Offer a Palestinian Civil Services Agreement')],icon='one_state_isr_pal',sources=['begin77'],status='Plausible alternative',requirements=['Palestine exists.'],mechanics=['No automatic state, recognition, naturalisation, core or border change. No previous settlement project or pension legislation is required. Both countries must agree to the service contract. Palestine does not receive a veto on unilateral illegal settlement establishment.'])
    for country in ['Israel','Palestine']:
        autonomy['effects']+=heading(paid(.4)+[budget('Civil Services Liaison',-.005,104),E('National Spirit','Civil Services Agreement, 104 weeks','gain'),E('Bureaucracy Cost','-6%','gain'),E('Office Productivity','+4%','gain')],'If they accept: '+country)
    add('gahal','gahal_tax_cut','Cut the Corporate Burden',-2,10,
        'Use the smaller ministerial establishment to reduce the tax burden on firms. The private economy gains commercial room while the treasury deliberately forgoes part of its corporate revenue.',
        pre=['gahal_ministries','gahal_renewal'],mods={'offices_productivity':.08},effects=[E('Corporate Tax Income','-8%','cost',native_key='corporate_tax_income_multiplier_modifier',amount=-.08,scope='programme')],icon='generic_banking_legislation',sources=['begin77'],status='Plausible alternative',programme='Fiscal priority')
    add('gahal','gahal_development_receipts','Keep the Development Revenue',2,10,
        'Retain a broad corporate contribution while financing public commitments. The budget becomes less dependent on another sale, at the cost of a slower private office-construction programme.',
        pre=['gahal_ministries'],effects=[m('corporate_tax_income_multiplier_modifier',.08,'Corporate Tax Income')],mods={'production_speed_offices_factor':-.06},icon='industrial_subsidies',sources=['economy','begin77'],status='Plausible alternative',programme='Fiscal priority')
    exclusive('gahal_tax_cut','gahal_development_receipts')

    # Mafdal: real registration controversy, funded academic/service work,
    # and the argument between coalition institutions and settler activism.
    add('mafdal','mafdal_interior','An Interior Ministry for the Municipalities',0,4,
        'Use the party\'s municipal and welfare responsibilities to organise permanent planning and service teams. A functioning local establishment should remain useful beyond the immediate coalition bargain.',
        pre=['service_bargain'],cost=.7,mods={'production_speed_infrastructure_factor':.12,'bureaucracy_cost_multiplier_modifier':.03},icon='civil_service',sources=['mafdal_history'])
    add('mafdal','mafdal_registration_compromise','Keep the 1970 Registration Compromise',-2,5,
        'Maintain a distinction between the religious registration of Jewish status and the citizenship rights of an immigrant\'s family. The absorption service receives a funded office and a broader service commitment.',
        pre=['mafdal_interior'],cost=.8,effects=asset('Tel Aviv','Office District'),mods={'social_cost_multiplier_modifier':.04},icon='generic_refugee_focus',sources=['registration70'],status='Contemporary policy',programme='Registration policy',history_note='The March 1970 compromise did not require Orthodox-only conversions. Some Orthodox parties opposed it; the alternatives must not be presented as the same historical position.')
    add('mafdal','mafdal_strict_certification','Demand Orthodox Conversion Certification',2,5,
        'Give recognised rabbinical authorities exclusive certification powers. A cabinet built on this arrangement gains institutional cohesion while applicants, investors and public offices face more restrictive procedures.',
        pre=['mafdal_interior'],cost=.4,mods={'political_power_factor':.10,'stability_factor':.05,'receiving_investment_cost_modifier':.05,'bureaucracy_cost_multiplier_modifier':.04},icon='orthodox_jew',sources=['registration70'],status='Contemporary contested proposal',programme='Registration policy',mechanics=['A selective political alternative, not the text enacted in March 1970. The political effect represents the governing compact, not universal approval or a measured economic gain. No certification-fee windfall, population removal or cancellation of another country\'s citizenship.'])
    exclusive('mafdal_registration_compromise','mafdal_strict_certification')
    add('mafdal','mafdal_bar_ilan','Laboratories at Bar-Ilan',-3,6,
        'Expand the natural-science and mathematics establishment of an existing university. Laboratories, equipment and staff produce limited research gains because the state pays for them, not because a religious party governs.',
        pre=['mafdal_interior'],cost=.9,effects=[research('Electronics'),research('Industry')],mods={'education_cost_multiplier_modifier':.04},icon='universities',sources=['biu'],days=49)
    add('mafdal','mafdal_cooperative_bank','A Loan Desk for Religious Workers\' Cooperatives',3,6,
        'A dedicated commercial desk can help existing cooperatives purchase and market together. It adds a real office and a defined guarantee reserve instead of another passing improvement in faction sentiment.',
        pre=['mafdal_interior'],cost=1.1,effects=asset('Negev','Office District')+[budget('Cooperative Credit Reserve',-.005,52)],icon='agricultural_banks',sources=['mafdal_history','economy'])
    add('mafdal','mafdal_old_guard','Keep the Coalition Bargain in Parliament',-3,7,
        'The established leadership can protect religious institutions through a negotiated municipal budget. It gives local services another connection without making territorial expansion the party\'s only purpose.',
        pre=['mafdal_bar_ilan'],cost=.9,effects=asset('Selected Israeli Core State','Infrastructure'),mods={'health_cost_multiplier_modifier':-.04},icon='knesset_speech',sources=['mafdal_history'],status='Plausible alternative',requirements=['An eligible owned and controlled Israeli core state.'])
    add('mafdal','mafdal_activist_current','Back the Religious Settler Current',3,7,
        'The younger territorial current wants resources beyond the older coalition bargain. A sponsored agricultural site gains a road and a real economic foothold while imposing a higher security burden on occupied territory.',
        pre=['mafdal_cooperative_bank'],cost=1.6,effects=asset('West Bank','Agricultural District')+asset('West Bank','Infrastructure')+state_burden(8,20)+pal_pressure()+[budget('Sponsored Site Security',-.02)],icon='jewish_sites_isr',sources=['mafdal_history','gush_archive','occupation'],status='Later historical precedent',requirements=['Israel controls the West Bank.'],history_note='The younger current exists before the named Gush Emunim organisation, which was founded in 1974. Earlier adoption is an explicit alternative, not a 1970 Gush apparatus.',mechanics=['One site within the common settlement tier cap. No free core or host establishment vote.'])
    add('mafdal','mafdal_service_volunteers','Religious Women\'s Civilian Service',-3,8,
        'Fund trained civilian volunteers in clinics and community services. Their contribution helps the health establishment while instructors and supervision become another public commitment.',
        pre=['mafdal_old_guard'],cost=.6,mods={'health_cost_multiplier_modifier':-.08,'education_cost_multiplier_modifier':.03},icon='generic_female_rights',sources=['civil_service71'],status='Later historical precedent',history_note='The NRP initiative belongs to 1971 and the operating association to 1972. Earlier adoption is an alternative. No new population, workforce-size bonus or military elite unit.')
    add('mafdal','mafdal_planning_appeals','Planning Appeals before Another Site',0,8,
        'A common appeals procedure can resolve the next land and access dispute before contractors arrive. The procedure costs administrative time and can make actually authorised works easier to build.',
        pre=['mafdal_interior'],cost=.4,effects=[E('Selected Controlled State: Infrastructure Construction Speed','+15%','gain'),E('Bureaucracy Cost','+3%','cost',native_key='bureaucracy_cost_multiplier_modifier',amount=.03,scope='programme')],icon='generic_investigate_corruption',sources=['occupation'],status='Plausible alternative',requirements=['A selected state is actually controlled by Israel.'])
    add('mafdal','mafdal_land_committee','A State-Funded Settlement Committee',3,8,
        'Bring the activist programme into a funded committee with declared accounts. The state takes responsibility for one operating commitment instead of treating private political initiative as free national infrastructure.',
        pre=['mafdal_activist_current'],cost=.1,effects=[E('Sponsored Site Security Expense','0.020% becomes 0.016% of annual GDP per week for 52 weeks','gain'),E('Next Paid Tier of This Site: Public Contribution','-0.3% of annual GDP','gain'),E('Required Accepted Private Tier Contribution','+0.3% of annual GDP','neutral'),budget('Settlement Committee Establishment',-.001,52)],icon='collaborate_local_elites2',sources=['yanai','occupation'],status='Plausible alternative',programme='Funded committee: 52 weeks',mechanics=['One funded site with an existing 0.020%-GDP weekly security bill. Its temporary reduction saves 0.208% GDP over 52 weeks; committee upkeep costs 0.052% and setup 0.1%. The next-tier 0.3%-GDP contribution requires an actual paid tier and an accepted corresponding private investment contribution; it is not free cash. No repeated discount on government change.'])
    add('mafdal','mafdal_restrain_sites','Refuse New Unauthorised Commitments',-3,9,
        'Keep faith with the coalition institutions while refusing new unauthorised sites. The cabinet saves part of its security establishment only while it actually maintains the freeze.',
        pre=['mafdal_service_volunteers'],mods={'police_cost_multiplier_modifier':-.06,'personnel_cost_multiplier_modifier':-.03},effects=[E('New Settlement Project Starts','Suspended while policy is active','cost')],icon='generic_civilian_oversight',sources=['mafdal_history'],status='Plausible alternative',programme='Territorial commitment policy',mechanics=['Starting another site ends these savings. Existing settlers and local population are not forcibly moved, and ongoing foreign footholds retain their actual bill.'])
    add('mafdal','mafdal_regularise_sites','Provide Public Works to the Sponsored Site',3,9,
        'Regularise the state\'s financial involvement by funding the sponsored site\'s next farm and access improvement. Public support leaves productive assets, a continuing security expense and costs for Palestinian institutions.',
        pre=['mafdal_land_committee'],cost=1.4,effects=asset('West Bank','Agricultural District')+asset('West Bank','Infrastructure')+state_burden(5,10)+pal_pressure()+[budget('Regularised Site Security',-.015)],icon='generic_road_construction',sources=['gush_archive','occupation'],status='Later historical precedent',requirements=['Israel controls the West Bank and the sponsored site exists.'],programme='Territorial commitment policy',mechanics=['A second paid tier of the same site within shared caps, not free validation of uncontrolled buildings. No automatic annexation or core.'])
    exclusive('mafdal_restrain_sites','mafdal_regularise_sites')
    add('mafdal','mafdal_working_communities','Working Communities in the South',0,10,
        'A lasting party programme needs employment and practical skills as well as a position on territory. Finance another working community in the Israeli core economy.',
        pre=[['mafdal_restrain_sites','mafdal_regularise_sites']],cost=2,effects=asset('Negev','Civilian Factory')+asset('Negev','Agricultural District'),icon='generic_working_class_family',sources=['mafdal_history','economy'],days=70)

    # Real coalition partners receive smaller, individually motivated continuations.
    add('orthodox','orthodox_study_budget','A Protected Budget for Torah Study',0,3,
        'Specify what the state will support in the study network and what the communities themselves will supply. Protected grants gain predictable purchasing and service arrangements without an imaginary research windfall.',
        pre=['communal_welfare'],cost=.5,mods={'education_cost_multiplier_modifier':-.06},effects=[budget('Protected Study Grant',-.005)],icon='orthodox_jew',sources=['election','mafdal_history'],status='Plausible alternative')
    add('orthodox','orthodox_deferments','Negotiate Full-Time Student Deferments',-2,4,
        'An expanded study-deferment settlement protects the funded network. The army must rely more heavily on its paid establishment, making the arrangement a fiscal choice rather than free social harmony.',
        pre=['orthodox_study_budget'],cost=.4,mods={'stability_factor':.06,'political_power_factor':.08,'personnel_cost_multiplier_modifier':.06,'education_cost_multiplier_modifier':.04},icon='school_is_in',sources=['election'],status='Plausible alternative',mechanics=['The benefit is a governing institutional compact, not an invented saving from more full-time study. Study and army staffing are actually funded. No negative workforce-size modifier or automatic new 1970 law.'])
    add('orthodox','orthodox_evening_trade','Poalei Agudat Evening Trade Courses',2,4,
        'Keep a route into skilled work alongside religious study for the workers\' communities. Workshops and instructors deliver practical gains without treating Poalei Agudat as identical to every Orthodox faction.',
        pre=['poalei_workshops'],cost=.7,effects=[research('Industry',2)],mods={'industry_repair_factor':.10,'education_cost_multiplier_modifier':.03},icon='bel_prioritizetechnicaleducation',sources=['election'],status='Plausible alternative',requirements=['Poalei Agudat has actual governing representation.'])
    add('orthodox','orthodox_large_families','Extend the Large-Family Allowance',0,5,
        'Simplify and extend family support through a defined public allowance. The result is a durable social commitment with a clearer administrative route, rather than a temporary rise in religious-institution opinion.',
        pre=[['orthodox_deferments','orthodox_evening_trade']],cost=.5,mods={'stability_factor':.08,'social_cost_multiplier_modifier':.06,'bureaucracy_cost_multiplier_modifier':-.03},icon='generic_working_class_family',sources=['nii'],status='Plausible alternative',history_note='Large-family allowances predate 1970. This selectable extension is not confused with the separate 1975 universal reform.')
    add('orthodox','orthodox_cooperative_plant','A Plant for the Religious Workers\' Communities',0,6,
        'Complete the productive continuation with a paid cooperative plant. Its construction does not depend on every Orthodox party sharing the same view of employment, schooling or military service.',
        pre=['orthodox_evening_trade','orthodox_large_families'],cost=1.7,effects=asset('Negev','Civilian Factory'),icon='factory_complex',sources=['election','histadrut'],status='Plausible alternative',requirements=['Poalei Agudat has actual governing representation.'],days=49)

    add('liberals','liberal_hotel_credit','Kol\'s Hotel Investment Guarantees',0,4,
        'Use a limited public guarantee to finance the first major hotel-development programme. The state makes construction more affordable while carrying a reserve and a claim if the insured project fails.',
        pre=['export_services'],cost=.1,effects=[E('Required Accepted Private Resort Capital','+0.6% of annual GDP','neutral'),E('First Guaranteed Resort: Public Financing Share','-0.6% of annual GDP from its normal contribution','gain'),budget('Hotel Guarantee Administration Expense',-.003,104),E('Gross Maximum Insured Claim','0.8% of annual GDP','cost'),E('Maximum Additional Treasury Call after Full Cash Reserve','0.7% of annual GDP','cost')],icon='agricultural_banks',sources=['kol70'],status='Contemporary policy proposal',programme='Hotel guarantee book: 104 weeks',requirements=['The resort has actual accepted private investment of 0.6% of annual GDP.'],mechanics=['One guaranteed resort, one national book. Insurance does not pay for construction: the lower public contribution requires an actual 0.6%-GDP private contribution. The funded prices below already include that share, never twice. The gross claim includes the 0.1%-GDP cash reserve; the treasury never pays that reserve twice. No closure is forced. Any unused actual cash reserve returns once only after cover and claims end. Weekly administration is spent, not accumulated as a second reserve. A government change closes new quotes but does not cancel existing 104-week cover or outstanding claims.'])
    add('liberals','liberal_sinai_resort','Tourist Resorts on the Sinai Coast',-2,5,
        'Pursue the tourism minister\'s resort programme on a coast Israel controls but does not own. The offices and access road can earn income, while occupation, protection and the guarantee remain real liabilities.',
        pre=['liberal_hotel_credit'],cost=1.2,effects=asset('Sinai','Office District',2)+asset('Sinai','Infrastructure')+state_burden(5,10),mods={'police_cost_multiplier_modifier':.03,'personnel_cost_multiplier_modifier':.02},icon='generic_airline_industry',sources=['kol70','occupation'],status='Contemporary policy proposal',requirements=['Israel controls Sinai.'],mechanics=['A tourist/commercial project, not a core or free property transfer. The normal pre-guarantee contribution is 1.8% GDP. Controlled office buildings enter the existing MD controlled-state economic totals. No Egyptian benefit or approval is presumed.'])
    add('liberals','liberal_coastal_resort','Fund the First Resort on the Israeli Coast',2,5,
        'Put the first guaranteed resort on the domestic coast instead. It is smaller but avoids adding another occupied-territory security establishment.',
        pre=['liberal_hotel_credit'],cost=.9,effects=asset('Haifa','Office District')+asset('Haifa','Infrastructure'),mods={'mdcw_cw_market_exposure':.05},icon='generic_airline_industry',sources=['kol70','economy'],status='Plausible alternative',mechanics=['Uses the same one-resort guarantee book. The normal pre-guarantee contribution is 1.5% GDP. Ordinary later construction remains possible; this choice allocates the first guarantee.'])
    exclusive('liberal_sinai_resort','liberal_coastal_resort')
    add('liberals','liberal_tourism_trades','A Trade School for the Visitor Economy',0,6,
        'Hotels and travel firms need trained managers, technicians and commercial services. Fund that establishment so the visitor economy produces more than a real-estate opening ceremony.',
        pre=[['liberal_sinai_resort','liberal_coastal_resort']],cost=.7,mods={'offices_productivity':.06,'education_cost_multiplier_modifier':.03},effects=[research('Industry')],icon='bel_prioritizetechnicaleducation',sources=['kol70'],status='Plausible alternative')

    add('haolam','haolam_complaints','A Commission for Police Complaints',0,4,
        'Put complaints and procurement records before a public commission with powers to investigate. Correcting abuse and waste requires a paid inquiry rather than merely improving the government\'s public image.',
        pre=['civil_equalities'],cost=.5,effects=[E('Corruption','-1 level','gain')],mods={'police_cost_multiplier_modifier':-.05},icon='generic_investigate_corruption',sources=['election'],status='Plausible alternative')
    add('haolam','haolam_detention_review','Judicial Review of Military Detention',0,5,
        'Require a funded legal review of military detention and access to defence. A less arbitrary administration can reduce friction in controlled territory while increasing court and police expenditure.',
        pre=['haolam_complaints'],cost=.5,effects=[E('Controlled Non-Core Territory: Compliance Gain','+15%','gain'),E('Controlled Non-Core Territory: Damage to Garrisons','-10%','gain')],mods={'police_cost_multiplier_modifier':.05},icon='generic_civilian_oversight',sources=['election','occupation'],status='Plausible alternative',requirements=['At least one non-core territory is controlled by Israel.'])
    services=add('haolam','haolam_joint_services','Direct Contacts for Municipal Services',0,6,
        'Make a concrete service proposal to a Palestinian RP government without requiring either side to accept a final territorial settlement. The partner decides whether to join a paid shared-service arrangement.',
        pre=['haolam_detention_review'],effects=[unlock('Offer Joint Municipal Services')],icon='one_state_isr_pal',sources=['election'],status='Plausible alternative',mechanics=['Does not grant permission for settlements, transfer territory or force recognition. A real recipient response is required.'])
    for country in ['Israel','Palestine']:
        services['effects']+=heading(paid(.4)+[budget('Joint Municipal Services',-.006,52),E('National Spirit','Joint Municipal Services, 52 weeks','gain'),E('Industry Repair Speed','+15%','gain'),E('Infrastructure Construction Speed','+10%','gain')],'If they accept: '+country)

    # Real sites, debts and accepted contracts outlive their initiating cabinet.
    by={n['id']:n for n in nodes}
    bound_sites={'ISR2_labor_valley','ISR2_gahal_settler_entitlement','ISR2_mafdal_activist_current','ISR2_mafdal_regularise_sites','ISR2_liberal_sinai_resort'}
    for n in nodes:
        if n['id'] in bound_sites:
            n['programme']='Paid site: assets and obligations follow actual control'
            n['effect_owner']='controlled_site'
            n['mechanics'].append('The buildings remain after government change. Existing security and administrative commitments follow the funded site and actual Israeli control, not the ruling party. They cannot be cancelled by an election alone.')
        if n['id'] in ['ISR2_gahal_local_autonomy','ISR2_haolam_joint_services']:
            n['agreement_family']='palestinian_civil_services'
            n['mechanics'].append('One civil-services agreement family per pair of countries. A newly accepted replacement removes the old programme and its running charge before starting the new one. Elections alone do not restore or duplicate setup payments. The Gahal arrangement supplies administration and commerce; the joint-services arrangement supplies engineering and repair.')
    compensation=by['ISR2_negotiated_terms']
    compensation['effects']+=heading([E('National Spirit','Funded Territorial Service Relief, 52 weeks','gain'),E('Police Cost','-4%','gain'),E('Bureaucracy Cost','-3%','gain')],'If they accept: Israel')
    compensation['mechanics'].append('Funded Palestinian services take over a defined share of the civil burden for 52 weeks, producing the listed Israeli administration savings while paid. No settlement authorisation or unilateral host right is created.')
    by['ISR2_labor_yanai']['mechanics'].append('Gross claim 1.6% includes the 0.2% cash reserve: at full reserve the extra treasury call is at most 1.4%, not 1.6% again. Weekly administration charges are expenses, not additional reserve deposits.')

    # Retain exact party gates and separate Poalei's representation from Agudat.
    orthodox=next(g for g in groups if g['id']=='orthodox')
    orthodox['subtitle']='Communal schooling and welfare, with a separate religious workers\' continuation.'
    old_gate=orthodox['gate']
    orthodox['gate']='Agudat Israel is in Power.'
    orthodox['identity_note']='Design correction: the native slot13 party identity must display Agudat Israel. Poalei Agudat is separately represented through actual coalition/list data, not an invented new outlook slot.'
    for n in nodes:
        if n['group']=='orthodox':
            n['requirements']=[orthodox['gate'] if text==old_gate else text for text in n['requirements']]
        if n['group']=='orthodox' and n['id'] in ['ISR2_poalei_workshops','ISR2_religious_agriculture']:
            n['requirements'].append('Poalei Agudat has actual governing representation.')
        n['effects']=[e for e in n['effects'] if not(e['label'] in internal and e.get('tone')=='gain')]
        if next(g for g in groups if g['id']==n['group'])['kind']=='party' and n['programme']=='Governing programme' and not n['modifiers']:
            n['programme']='One-time achievement; national assets remain'
        # Keep complete acceptance outcomes grouped by the country affected.
        common=[e for e in n['effects'] if not e.get('heading','').startswith('If they accept: ')]
        headings=list(dict.fromkeys(e['heading'] for e in n['effects'] if e.get('heading','').startswith('If they accept: ')))
        n['effects']=common+[e for h in headings for e in n['effects'] if e.get('heading')==h]
    by={n['id']:n for n in nodes}
    return dict(project='IMPERIA COLD WAR',revision='2.1-expanded-20261028',
        original_focuses=138,added_focuses=len(nodes)-138,
        positive_internal_opinions_removed=removed,
        expanded_groups=['alignment','gahal','mafdal','orthodox','liberals','haolam'],
        classification='Historical policy/proposal, later precedent, or explicit plausible alternative; all numeric effects are authored balance.',
        new_bilateral_previews=['ISR2_labor_jordanian_option','ISR2_gahal_local_autonomy','ISR2_haolam_joint_services'])
