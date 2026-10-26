# IMPERIA CW — Cold War: national development, institutions and external programmes.
"""Structured 1970 expansion; all monetary amounts are shares of GDP."""
from copy import deepcopy

def extend(d):
    # Fit each political programme beneath its actual neighbouring footprint.
    lower_roots={'kdp':25,'chondo':29,'cabinet':29,'kpa':17,'yanan':17,'union':13,'christian':25,'jongil':25}
    for g in d['groups']:
        if g['id'] in lower_roots:g['y']=lower_roots[g['id']]
    for n in d['nodes']:
        if n['group'] in lower_roots:n['y']+=lower_roots[n['group']]-17
    before=len(d['nodes'])
    def add(group,key,title,x,y,pre,mods,price,icon,description,mutex=(),extra=(),requirements=()):
        g=group if isinstance(group,dict) else next(g for g in d['groups'] if g['id']==group)
        root=next((n for n in d['nodes'] if n['group']==g['id']),None)
        n=dict(id='COLDWAR_NKO_'+key,key=key,title=title,long_title=title,group=g['id'],x=x,y=y,
          dx=x-(root['x'] if root else x),dy=y-(root['y'] if root else y),anchor=root['id'] if root else None,
          prerequisites=[['COLDWAR_NKO_'+p.removeprefix('COLDWAR_NKO_') for p in pg] for pg in pre],
          mutex=['COLDWAR_NKO_'+p.removeprefix('COLDWAR_NKO_') for p in mutex if p.removeprefix('COLDWAR_NKO_')!=key],cost=5,days=35,cost_gdp_share=price,
          modifiers=deepcopy(mods),labels={},description=description,extra=deepcopy(list(extra)),gate='',slot=g['slot'],icon=icon,
          ownership='Party programme' if g['slot'] is not None else 'National programme',remove=[],duration=None,
          historical_status='Historical institutions and plausible alternative programmes',requirements=list(requirements),player_gate='',eligibility_notes=[])
        if g['id']=='jongil':
            n['leader_bound']='Kim Jong Il';n['requirements'].append('Kim Jong Il is the national leader.')
            n['eligibility_notes'].append('has_country_leader = { name = "Kim Jong-il" ruling_only = yes }')
        assert not any(old['id']==n['id'] for old in d['nodes']),n['id']
        d['nodes'].append(n);return n
    def building(kind,state,level=1):return dict(kind='building',type=kind,levels=level,slots=level,state_ids=state)

    # The second industrial programme moves from recovery to sectoral allocation.
    def E(key,title,x,y,pre,mods,price,icon,desc,mutex=(),extra=()):
        return add('economy',key,title,x,y,pre,mods,price,icon,desc,mutex,extra)
    E('national_investment','Investment Accounts',16,15,[['joint_ventures']],
      {'production_factory_efficiency_gain_factor':.04,'bureaucracy_cost_multiplier_modifier':.025},.00625,'money',
      'Require ministries to distinguish completed capacity from promised output. Better accounts will make investment more dependable, while expanding the statistical service.')
    E('coal_face','Deeper Coal Seams',12,16,[['national_investment']],
      {'fossil_pp_energy_generation_modifier':.06,'health_cost_multiplier_modifier':.03},.01,'coal_mining',
      'Reequip working faces and improve deliveries from established coalfields. Higher throughput can stabilize thermal power, but deeper workings impose additional health and maintenance costs.',extra=[building('infrastructure',[1201,1200])])
    E('chemical_inputs','Chemical Inputs',16,16,[['national_investment']],
      {'agricolture_productivity_modifier':.04,'industrial_capacity_factory':.03,'energy_use_multiplier':.05},.00875,'economic_civil_industry',
      'Coordinate fertilizer, industrial chemicals and spare components around dependable power allocations. More reliable inputs will improve production, while placing greater demands on the electricity network.')
    E('consumer_workshops','Consumer Workshops',20,16,[['national_investment']],
      {'productivity_growth_modifier':.035,'social_cost_multiplier_modifier':-.025,'production_speed_arms_factory_factor':-.04},.0125,'NKO_workers',
      'Restore workshops producing clothing, household goods and repairs. Better civilian supplies can reduce pressure on public provision, while diverting investment from the armaments sector.',extra=[building('industrial_complex',[603,601])])
    E('mine_safety','Mine Safety Teams',12,17,[['coal_face']],
      {'productivity_growth_modifier':.025,'health_cost_multiplier_modifier':-.025,'production_factory_efficiency_gain_factor':-.02},.00625,'NKO_healthcare',
      'Fund inspections, protective equipment and trained rescue teams at working mines. Fewer injuries support reliable employment, while inspections and safer routines slow immediate expansion.')
    E('fertilizer_recovery','Fertilizer Recovery',16,17,[['chemical_inputs']],
      {'agricolture_productivity_modifier':.075,'fossil_pp_energy_generation_modifier':-.03},.00875,'agriculture',
      'Recondition fertilizer equipment and reserve feedstock for the cultivation season. More dependable applications can improve harvests, at the cost of fuel otherwise available for power generation.')
    E('textile_orders','Textile Contracts',20,17,[['consumer_workshops']],
      {'industrial_capacity_factory':.045,'tax_gain_multiplier_modifier':.025,'production_speed_arms_factory_factor':-.03},.0075,'NKO_worker',
      'Give textile plants predictable orders and access to replacement machinery. Larger civilian output and sales broaden revenue, while tying scarce equipment to nonmilitary production.')
    E('industrial_water','Industrial Water',16,18,[['mine_safety'],['fertilizer_recovery'],['textile_orders']],
      {'production_factory_efficiency_gain_factor':.04,'energy_use_multiplier':-.025,'bureaucracy_cost_multiplier_modifier':.025},.01,'hydroelectric',
      'Repair pumping stations and coordinate water use between plants and agriculture. Fewer interruptions improve efficiency, while maintaining common schedules requires additional administration.')
    E('electric_traction','Electric Traction',14,19,[['industrial_water']],
      {'non_electric_fuel_consumption_modifier':-.06,'supply_consumption_factor':-.035,'energy_use_multiplier':.05},.0125,'NKO_railways',
      'Extend electric traction on the busiest industrial routes. Reduced liquid-fuel dependence and steadier freight movements come with a heavier demand on the power grid.',('diesel_flexibility',),[building('infrastructure',[1200,603])])
    E('diesel_flexibility','Diesel Flexibility',18,19,[['industrial_water']],
      {'supply_consumption_factor':-.05,'production_speed_buildings_factor':.04,'non_electric_fuel_consumption_modifier':.06},.01,'NKO_railways',
      'Concentrate diesel locomotives and repair crews where traffic is least predictable. More flexible deliveries help construction and distribution, while increasing the demand for imported fuel.',('electric_traction',))
    E('freight_dispatch','Freight Dispatch',16,20,[['electric_traction','diesel_flexibility']],
      {'supply_consumption_factor':-.04,'bureaucracy_cost_multiplier_modifier':.025},.00625,'focus_generic_supply_line',
      'Give dispatch offices authority to coordinate rolling stock and loading schedules. Better use of existing transport reduces losses and delays, but requires a larger professional staff.')
    E('port_refit','Port Repair Yards',12,21,[['freight_dispatch']],
      {'trade_opinion_factor':.04,'non_electric_fuel_consumption_modifier':.025},.015,'trade',
      'Expand coastal repair capacity and maintain cargo-handling equipment. More dependable port services support trade, while creating a continuing demand for fuel and skilled crews.',extra=[building('dockyard',[601,603])])
    E('rural_distribution','County Distribution',16,21,[['freight_dispatch']],
      {'agricolture_productivity_modifier':.04,'social_cost_multiplier_modifier':-.03,'bureaucracy_cost_multiplier_modifier':.035},.00875,'NKO_food',
      'Connect county stores to reliable transport and inventory records. Less waste eases the burden of public distribution, while rural administration becomes more costly.')
    E('construction_brigades','Building Brigades',20,21,[['freight_dispatch']],
      {'production_speed_buildings_factor':.075,'productivity_growth_modifier':-.025,'social_cost_multiplier_modifier':.03},.01,'NKO_buildings',
      'Organize skilled construction teams with dependable tools and accommodation. Concentrated crews accelerate national projects, while drawing workers away from ordinary production.')
    E('export_inspection','Export Inspection',12,22,[['port_refit']],
      {'trade_opinion_factor':.06,'corporate_tax_income_multiplier_modifier':.03,'production_factory_efficiency_gain_factor':-.025},.0075,'trade',
      'Inspect export consignments before they reach foreign buyers. Greater confidence supports commercial earnings, while stricter tolerances reduce the pace of initial production.')
    E('cold_storage','Cold Stores',16,22,[['rural_distribution']],
      {'agricolture_productivity_modifier':.05,'social_cost_multiplier_modifier':-.025,'energy_use_multiplier':.04},.01,'NKO_food',
      'Fund refrigerated stores and repair existing preservation equipment. Better storage protects food supplies, but requires electricity throughout the distribution season.')
    E('standardized_housing','Standardized Housing',20,22,[['construction_brigades']],
      {'production_speed_buildings_factor':.05,'stability_factor':.025,'production_factory_max_efficiency_factor':-.025},.00875,'NKO_buildings',
      'Standardize building components for workers’ housing and public facilities. Faster provision improves confidence in the plan, while limiting the flexibility of factories supplying it.')
    E('investment_balance','Balance the Accounts',16,23,[['export_inspection'],['cold_storage'],['standardized_housing']],
      {'tax_gain_multiplier_modifier':.04,'bureaucracy_cost_multiplier_modifier':.025},.00625,'money',
      'Match project obligations to expected domestic revenue and export earnings. More disciplined accounts improve collection, while requiring regular ministerial scrutiny.')
    E('industrial_reserves','Industrial Reserves',14,24,[['investment_balance']],
      {'production_factory_max_efficiency_factor':.075,'industrial_capacity_factory':.035,'production_speed_buildings_factor':-.05},.0125,'economic_civil_industry',
      'Retain spare machinery and inventory against interruptions in supply. Better continuity raises dependable output, while capital held in reserve slows new construction.',('investment_turnover',))
    E('investment_turnover','Rapid Reinvestment',18,24,[['investment_balance']],
      {'production_speed_buildings_factor':.085,'productivity_growth_modifier':.04,'interest_rate_multiplier_modifier':.4},.0125,'money',
      'Return available capital quickly to new equipment and construction. Faster turnover supports expansion, but a thinner financial cushion increases the cost of credit.',('industrial_reserves',))
    E('repair_standards','Repair Standards',14,25,[['industrial_reserves']],
      {'equipment_cost_multiplier_modifier':-.04,'production_factory_efficiency_gain_factor':.04,'education_cost_multiplier_modifier':.035},.0075,'NKO_rebuild',
      'Train workshops to restore components to common tolerances. Recovering usable equipment reduces procurement costs, while specialist instruction remains a continuing obligation.')
    E('industrial_apprentices','Plant Apprentices',18,25,[['investment_turnover']],
      {'productivity_growth_modifier':.055,'research_speed_factor':.025,'education_cost_multiplier_modifier':.05},.00875,'education_reform',
      'Combine practical apprenticeships with technical instruction at expanding plants. A broader skilled workforce supports productivity and research, while placing greater demands on education.')
    E('county_care','County Care Network',14,26,[['repair_standards','industrial_apprentices']],
      {'productivity_growth_modifier':.03,'stability_factor':.025,'health_cost_multiplier_modifier':.05},.01,'NKO_healthcare',
      'Staff county clinics and establish regular links with larger hospitals. More dependable treatment supports working households, but requires continuing public expenditure.')
    E('public_maintenance','Public Maintenance',18,26,[['repair_standards','industrial_apprentices']],
      {'production_speed_buildings_factor':.045,'energy_use_multiplier':-.025,'bureaucracy_cost_multiplier_modifier':.035},.00875,'NKO_rebuild',
      'Give local authorities regular maintenance schedules for housing, utilities and workshops. Preventive work improves the use of existing capacity, while enlarging administrative responsibilities.')

    # Institutional competition continues inside the governing party.
    def W(key,title,x,y,pre,mods,cost,icon,desc,mutex=()):return add('wpk',key,title,x,y,pre,mods,cost,icon,desc,mutex)
    W('party_inspection','Party Inspection',6,14,[['continuity']],{'tax_gain_multiplier_modifier':.03,'police_cost_multiplier_modifier':.03},.005,'NKO_anti_corruption',
      'Investigate procurement losses and the use of state property. Stronger inspection can recover revenue, while extending the expense and reach of political supervision.')
    W('cadre_rotation','Rotate Local Cadres',4,15,[['party_inspection']],{'political_power_factor':.06,'tax_gain_multiplier_modifier':.03,'productivity_growth_modifier':-.025},.00625,'WPRG',
      'Rotate officials before local patronage networks become permanent. The centre gains influence and revenue, while disrupted appointments interrupt accumulated expertise.',('cadre_specialization',))
    W('cadre_specialization','Specialist Appointments',8,15,[['party_inspection']],{'research_speed_factor':.04,'productivity_growth_modifier':.04,'political_power_factor':-.05},.00625,'education_reform',
      'Retain experienced administrators and place specialists in technical ministries. Greater competence supports production, while making appointments less responsive to political campaigns.',('cadre_rotation',))
    W('county_reporting','County Reports',4,16,[['cadre_rotation']],{'tax_gain_multiplier_modifier':.04,'bureaucracy_cost_multiplier_modifier':.03},.005,'NKO_party_reform',
      'Require county officials to explain the collection and allocation of state resources. Clearer reporting supports revenue, while generating a larger administrative workload.')
    W('ministerial_training','Ministry Schools',8,16,[['cadre_specialization']],{'productivity_growth_modifier':.04,'research_speed_factor':.025,'education_cost_multiplier_modifier':.04},.00625,'education_reform',
      'Train officials in accounting, engineering administration and practical planning. Better technical judgement can improve policy, but requires sustained instruction and staff time.')
    W('mass_organizations','Mass Organizations',6,17,[['county_reporting','ministerial_training']],{'stability_factor':.035,'social_cost_multiplier_modifier':.03},.005,'NKO_workers',
      'Coordinate workplaces, neighbourhood organizations and local services. Broader participation supports political stability, while increasing the obligations of public provision.')
    W('cultural_direction','Direct Cultural Work',4,18,[['mass_organizations']],{'political_power_factor':.065,'stability_factor':.025,'research_speed_factor':-.03},.00625,'NKO_theatre',
      'Give cultural organizations a common political direction. A consistent public message strengthens authority, while narrowing the space for independent inquiry.',('cultural_professions',))
    W('cultural_professions','Professional Culture',8,18,[['mass_organizations']],{'research_speed_factor':.045,'foreign_influence_defense_modifier':.035,'political_power_factor':-.045},.00625,'NKO_theatre',
      'Give professional institutions greater discretion in education and cultural work. Stronger specialist institutions support intellectual confidence, while limiting direct political direction.',('cultural_direction',))
    W('institutional_memory','Institutional Records',4,19,[['cultural_direction']],{'foreign_influence_defense_modifier':.05,'bureaucracy_cost_multiplier_modifier':.025},.005,'juche',
      'Preserve central records and make local organizations answer for their instructions. A more consistent administrative record protects political continuity, while requiring permanent staff.')
    W('policy_evaluation','Evaluate the Plan',8,19,[['cultural_professions']],{'productivity_growth_modifier':.05,'production_factory_efficiency_gain_factor':.035,'political_power_factor':-.03},.00625,'socialist_science',
      'Allow ministries to compare promised output with practical results. More credible evaluation improves production decisions, while exposing shortcomings that political reports once concealed.')
    W('governing_compact','A Governing Compact',6,20,[['institutional_memory','policy_evaluation']],{'production_factory_max_efficiency_factor':.035,'stability_factor':.03,'bureaucracy_cost_multiplier_modifier':.035},.0075,'WPRG',
      'Settle the relationship between central appointments, specialist ministries and mass organizations. Greater predictability supports production and stability, while retaining a costly institutional structure.')
    W('public_service_ethos','Service to the Republic',6,21,[['governing_compact']],{'tax_gain_multiplier_modifier':.03,'production_speed_buildings_factor':.035,'social_cost_multiplier_modifier':.035},.0075,'NKO_party_reform',
      'Tie official advancement to the dependable provision of national services. Better delivery supports public investment and revenue, while creating continuing obligations to local communities.')

    # Diplomatic work continues beyond the original European and Asian offers.
    def F(key,title,x,y,pre,mods,cost,icon,desc,mutex=()):return add('foreign',key,title,x,y,pre,mods,cost,icon,desc,mutex)
    F('consular_service','Consular Service',68,6,[['egyptian_missions','japan_ports']],{'trade_opinion_factor':.045,'bureaucracy_cost_multiplier_modifier':.025},.005,'trade',
      'Train consular staff to manage shipping documents, commercial disputes and official visits. More reliable representation supports trade, while requiring additional permanent missions.')
    F('export_diplomacy','Commercial Missions',66,7,[['consular_service']],{'corporate_tax_income_multiplier_modifier':.05,'trade_opinion_factor':.04,'foreign_influence_defense_modifier':-.035},.0075,'goal_generic_positive_trade_relations',
      'Give commercial missions wider authority to secure orders and resolve delivery problems. Stronger export earnings require more sustained contact with foreign institutions.',('technical_neutrality',))
    F('technical_neutrality','Technical Neutrality',70,7,[['consular_service']],{'research_speed_factor':.045,'foreign_influence_defense_modifier':.04,'trade_opinion_factor':-.035},.0075,'socialist_science',
      'Separate specialist exchanges from broader political commitments. Greater autonomy protects technical work, while limiting the commercial reach of diplomatic missions.',('export_diplomacy',))
    F('shipping_arbitration','Shipping Arbitration',66,8,[['export_diplomacy']],{'trade_opinion_factor':.06,'equipment_cost_multiplier_modifier':-.025,'bureaucracy_cost_multiplier_modifier':.03},.00625,'trade',
      'Create a professional service for delivery claims and maritime contracts. Fewer disputes improve commercial terms, while a permanent legal staff raises administrative costs.')
    F('translation_institutes','Translation Institutes',70,8,[['technical_neutrality']],{'research_speed_factor':.04,'productivity_growth_modifier':.025,'education_cost_multiplier_modifier':.04},.00625,'education_reform',
      'Train translators in engineering, medicine and international standards. Wider access to specialist knowledge improves research, while requiring sustained educational funding.')
    F('reciprocal_standards','Reciprocal Standards',68,9,[['shipping_arbitration','translation_institutes']],{'production_factory_efficiency_gain_factor':.04,'trade_opinion_factor':.035,'bureaucracy_cost_multiplier_modifier':.025},.0075,'trade',
      'Require external programmes to meet consistent documentation and delivery standards. More dependable exchanges support production, while adding supervision to every agreement.')

    # Early successor rule receives a further institutional choice.
    jy=lower_roots['jongil']
    add('jongil','jongil_enterprise_returns','Enterprise Returns',64,jy+9,[['jongil_recovery_accounts']],{'tax_gain_multiplier_modifier':.035,'bureaucracy_cost_multiplier_modifier':.025},.00625,'money',
      'Require enterprises to distinguish maintenance reserves from current deliveries. Better accounts support state revenue, while adding reporting duties to already strained management.')
    add('jongil','jongil_local_discretion','Local Discretion',62,jy+10,[['jongil_enterprise_returns']],{'productivity_growth_modifier':.05,'supply_consumption_factor':-.03,'political_power_factor':-.045},.0075,'NKO_workers',
      'Allow provincial managers to adjust procurement within agreed obligations. Faster local responses improve production and distribution, while weakening direct central control.',('jongil_central_allocations',))
    add('jongil','jongil_central_allocations','Central Allocations',66,jy+10,[['jongil_enterprise_returns']],{'production_factory_max_efficiency_factor':.06,'army_org_factor':.04,'social_cost_multiplier_modifier':.045,'production_speed_industrial_complex_factor':-.035},.0075,'WPRG',
      'Reserve dependable inputs for centrally selected enterprises and military requirements. Greater continuity strengthens priority production, while imposing heavier obligations on civilian supply.',('jongil_local_discretion',))
    add('jongil','jongil_ministry_compact','A Ministry Compact',64,jy+11,[['jongil_local_discretion','jongil_central_allocations']],{'production_factory_efficiency_gain_factor':.04,'research_speed_factor':.025,'bureaucracy_cost_multiplier_modifier':.035},.0075,'parliament_box',
      'Settle the authority of ministries, provincial managers and the party centre under the chosen recovery policy. More predictable responsibilities support technical work, while preserving a substantial administrative burden.')

    from expansion_politics import extend as politics
    from expansion_defence import extend as defence
    from expansion_patrons import extend as patrons
    politics(d,add);defence(d,add);patrons(d,add)
    by={n['key']:n for n in d['nodes']}
    for key,other in [('soviet_exercise_intensity','soviet_independent_standards'),('soviet_independent_standards','soviet_exercise_intensity')]:
        by[key]['mutex']=['COLDWAR_NKO_'+other]
    by['soviet_independent_standards']['modifiers']['research_speed_factor']=.035
    by['soviet_independent_standards']['required_agreements']=[]
    for key,icon in [('china_partnership','align_to_china'),('china_patron_balance','trade_with_china'),('soviet_partnership','align_to_soviet_union'),('soviet_balanced_security','align_to_soviet_union')]:
        by[key]['icon']=icon
    patron_rows={12:12,14:13,16:14,17:15,18:16,19:17,20:18,21:19,22:20,23:21,24:21}
    for n in d['nodes']:
        if n['group'] in ('china','soviet'):
            n['y']=patron_rows[n['y']];n['dy']=n['y']-12
    for n in d['nodes'][before:]:
        if any(e['kind']=='agreement' for e in n['extra']):
            # The negotiated setup charge belongs to acceptance by both players.
            n['cost_gdp_share']=0
        if n.get('required_agreements'):
            # Agreement conditions have typed guards and one native spirit label.
            n['requirements']=[text for text in n['requirements'] if not text.endswith((' is active.',' are active.'))]
        if 'has_country_flag = COLDWAR_NKO_safeguards_valid' in n.get('policy_enable_guards',[]):
            n.setdefault('visible_guards',[]).append({'condition':'has_country_flag = COLDWAR_NKO_safeguards_valid','text':'International safeguards commitments remain in force.','not_text':'International safeguards commitments are required.'})
    assert len(d['nodes'])-before==162,('Expansion focus budget',len(d['nodes'])-before)
    d['amendments']['national_expansion_focuses']=162
    d['amendments']['previous_focus_limit_waived_by_user']=True
