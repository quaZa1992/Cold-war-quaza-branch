# IMPERIA COLD WAR — GDP-funded and differentiated France 1970 focus rewards.
"""Review-stage reward design only. No loaded game content is emitted here."""
def revise_rewards(ns,design):
    gdp,asset,mod,research,xp,weekly=(ns[k] for k in ('gdp','asset','mod','research','xp','weekly'))
    nodes={n['key']:n for n in ns['nodes']}
    changed=[]
    def faction(name,amount):
        return dict(kind='faction_opinion',faction=name,value=amount,provider='change_'+name+'_opinion',parameter='temp_opinion',once=True)
    def doctrine(service,reduction=.25):
        return dict(kind='doctrine',category=service+'_doctrine',reduction=reduction,uses=1,once=True)
    def replace(key,effects,description=None):
        n=nodes[key]
        n['effects']=effects
        n['reward_revision']='GDP-funded institutional, sector or physical outcome; see REWARD_PRECEDENTS.md and GDP_COST_REFERENCE.md.'
        if description:n['description']=description
        changed.append(key)

    replace('housing',[gdp(-.30),asset(56,'infrastructure'),mod('stability_factor',.03),mod('social_cost_multiplier_modifier',.05)],
            'Fund serviced housing and the local networks needed to replace precarious accommodation around Paris. The programme supports families already sustaining industrial growth and commits the state to continuing municipal services.')
    replace('contract',[gdp(-.10),ns['remove']('grenelle'),faction('labour_unions',10),faction('industrial_conglomerates',-5),mod('production_factory_efficiency_gain_factor',.03),mod('social_cost_multiplier_modifier',.08)])
    replace('statute',[gdp(-.10),ns['remove']('grenelle'),faction('industrial_conglomerates',10),faction('labour_unions',-10),mod('production_factory_efficiency_gain_factor',.06),mod('police_cost_multiplier_modifier',.04)])

    replace('new_society',[gdp(-.20),research('industry',.50),faction('labour_unions',10),mod('education_cost_multiplier_modifier',.06),mod('political_power_factor',-.04)],
            'Back Chaban-Delmas with a funded expansion of technical training and negotiated reform. Unions gain a place in the governing bargain while conservative Gaullists resist the prime minister opening.')
    replace('presidential_industry',[gdp(-.40),asset(55,'industrial_complex'),mod('production_factory_max_efficiency_factor',.04),faction('labour_unions',-5)],
            'Concentrate public investment in export-capable industrial groups and new productive capacity in Normandie. A stronger presidency secures scale and investment discipline while narrowing the social opening sought by organised labour.')
    replace('national_champions',[gdp(-.40),asset(62,'industrial_complex'),mod('civilian_factories_productivity',.04),mod('corporate_tax_income_multiplier_modifier',-.04)],
            'Finance a new production programme in Rhone-Alpes and back national firms with public contracts. The Treasury accepts tax concessions in exchange for industrial scale and a stronger domestic supplier base.')
    replace('participation',[gdp(-.10),faction('labour_unions',10),faction('industrial_conglomerates',-5),mod('production_factory_efficiency_gain_factor',.04),mod('corporate_tax_income_multiplier_modifier',-.04)],
            'Extend the profit-sharing instruments established in 1959 and 1967, pairing employee savings with representation. Workers gain a stake in results without replacing management with collective ownership.')
    replace('management',[faction('industrial_conglomerates',10),faction('labour_unions',-10),mod('civilian_factories_productivity',.06),mod('corporate_tax_income_multiplier_modifier',.05)])

    replace('business',[gdp(-.30),asset(62,'offices'),mod('offices_productivity',.04),mod('corporate_tax_income_multiplier_modifier',-.06)],
            'Open credit and public contracts to independent businesses and professional services in Rhone-Alpes. A wider enterprise base strengthens office-sector output while tax concessions reduce the immediate fiscal return.')
    replace('public_credit',[gdp(-.30),research('industry',.50),mod('production_factory_max_efficiency_factor',.05),mod('bureaucracy_cost_multiplier_modifier',.04)])
    replace('regional_councils',[gdp(-.30),asset(59,'infrastructure'),mod('production_speed_infrastructure_factor',.06),mod('political_power_factor',-.05)])
    replace('cdp_compromise',[gdp(-.15),research('industry',.50),mod('political_power_factor',.06),mod('education_cost_multiplier_modifier',.04)])
    replace('mutuals',[gdp(-.15),mod('health_cost_multiplier_modifier',-.04),mod('social_cost_multiplier_modifier',.05),faction('labour_unions',5)],
            'Strengthen the mutual societies and local insurance funds that connect households to health and social provision. Better administration reduces the health-service bill while the state sustains a larger social contribution.')
    replace('municipal_france',[gdp(-.45),asset(60,'offices'),asset(60,'agriculture_district'),mod('bureaucracy_cost_multiplier_modifier',.04)],
            'Back the market towns and cooperative services of Aquitaine with professional services and agricultural processing. Municipal direction brings investment closer to producers while retaining a public administrative cost.')
    replace('secular_school',[gdp(-.20),research('industry',.50),research('electronics',.50),mod('education_cost_multiplier_modifier',.06)])

    replace('socialist_refoundation',[ns['pp'](-40),faction('labour_unions',10),mod('political_power_factor',.05),mod('bureaucracy_cost_multiplier_modifier',.03)])
    replace('public_banks',[gdp(-.50),asset(56,'offices'),mod('offices_productivity',.05),mod('bureaucracy_cost_multiplier_modifier',.06)],
            'Give public credit institutions the staff and offices needed to direct industrial investment. The state gains a stronger financial-services base while accepting a permanent administrative establishment.')
    replace('defferre',[gdp(-.30),asset(63,'infrastructure'),mod('production_speed_infrastructure_factor',.05),mod('political_power_factor',-.04)],
            'Transfer practical authority to elected territorial institutions and finance a first regional services programme in Provence. Local direction gains substance while the central government gives up part of its immediate control.')
    replace('municipal_socialism',[gdp(-.35),asset(56,'infrastructure'),faction('labour_unions',10),mod('social_cost_multiplier_modifier',.06)])
    replace('public_combine',[gdp(-.80),asset(57,'industrial_complex'),asset(54,'arms_factory'),mod('production_factory_max_efficiency_factor',.05),mod('production_factory_efficiency_gain_factor',-.04),mod('bureaucracy_cost_multiplier_modifier',.07)],
            'Coordinate credit and procurement through public industrial groups, funding civilian capacity in Alsace-Lorraine and an armament programme in the north. Concentration supports scale but can slow adaptation and enlarge the planning apparatus.')
    replace('workers_control',[faction('labour_unions',15),faction('industrial_conglomerates',-10),mod('production_factory_efficiency_gain_factor',.05),mod('political_power_factor',-.04)])
    replace('self_management',[gdp(-.40),asset(58,'industrial_complex'),mod('production_factory_efficiency_gain_factor',.06),mod('bureaucracy_cost_multiplier_modifier',.05)],
            'Finance a worker-managed industrial pilot in Bourgogne with cooperative credit and technical advice. Experiments in self-management need capital and market access as well as workplace consent.')
    replace('union_autonomy',[faction('labour_unions',15),mod('stability_factor',.04),mod('social_cost_multiplier_modifier',.07),mod('industrial_capacity_factory',.03)])
    replace('land_stewardship',[gdp(-.20),asset(59,'agriculture_district'),faction('farmers',10),mod('social_cost_multiplier_modifier',.04)])
    replace('local_generation',[gdp(-.30),research('CAT_energy',.75),mod('energy_gain_multiplier',.06),mod('energy_use_modifier_civs',-.03),mod('bureaucracy_cost_multiplier_modifier',.05)],
            'Fund the engineering programme and regional coordination needed to improve existing hydroelectric and distributed generation. Better use of local resources requires trained operators and a continuing technical administration.')
    replace('cid_cooperatives',[gdp(-.20),asset(60,'offices'),mod('offices_productivity',.04),mod('bureaucracy_cost_multiplier_modifier',.04)])

    replace('technical_colleges',[gdp(-.25),ns['remove']('education'),research('industry',.50,2),research('electronics',.50),mod('production_factory_efficiency_gain_factor',.06),mod('education_cost_multiplier_modifier',.05)])
    replace('mass_universities',[gdp(-.40),ns['remove']('education'),research('electronics',.75),research('nuclear',.50),mod('research_speed_factor',.04),mod('education_cost_multiplier_modifier',.12)])
    replace('regional_industry',[gdp(-.60),asset(54,'industrial_complex'),asset(63,'naval_base',province=11834),mod('civilian_factories_productivity',.04),mod('social_cost_multiplier_modifier',.04)],
            'Prepare a modern industrial site in Hauts-de-France and expand port capacity serving the industrial economy of Provence. Regional conversion needs practical connections as well as new factory buildings.')
    replace('champion_model',[gdp(-.60),asset(55,'industrial_complex'),mod('civilian_factories_productivity',.06),mod('bureaucracy_cost_multiplier_modifier',.04)])
    replace('plan_calcul',[gdp(-.30),research('electronics',.50,2),mod('education_cost_multiplier_modifier',.04)],
            'Fund IRIA and the research programme supporting French computing. Public procurement and trained engineers must sustain a domestic capability against established foreign suppliers.')
    replace('national_computers',[gdp(-.35),asset(62,'industrial_complex'),research('electronics',.50),mod('corporate_tax_income_multiplier_modifier',-.03)],
            'Back the domestic computer-systems industry and its Grenoble engineering base with a funded production site. Independent supply requires public orders and continuing fiscal concessions.')
    replace('open_computers',[gdp(-.15),research('electronics',.75),mod('production_factory_efficiency_gain_factor',.06),mod('foreign_influence_modifier',-.03)])
    replace('transport_choice',[gdp(-.06),research('industry',.25)])
    replace('tgv',[gdp(-.60),asset(62,'infrastructure'),research('CAT_infrastructure',.75),mod('energy_use_modifier_civs',-.03)],
            'Fund SNCF engineering trials and expand the Lyon terminal and its approaches. Prototype work and a stronger station network prepare the high-speed programme for future commercial service.')
    replace('motorways',[gdp(-.60),asset(60,'infrastructure'),asset(59,'infrastructure'),mod('production_speed_infrastructure_factor',.07),mod('energy_use_modifier_civs',.04)])
    replace('nuclear_scale',[gdp(-.75),research('nuclear',.50,2),ns['unlock']('fund_reactor','Fund the first approved reactor project'),mod('production_speed_nuclear_reactor_factor',.08),mod('nuclear_energy_generation_modifier',.06),mod('bureaucracy_cost_multiplier_modifier',.04)],
            'Standardise the civil nuclear supply chain around the reactor choice made in 1970 and train the engineering establishment needed for expansion. The programme improves construction and operating performance while the Treasury separately funds each new reactor.')
    replace('diverse_energy',[gdp(-.60),asset(55,'fossil_powerplant'),mod('energy_use_modifier_civs',-.05),mod('civilian_factories_productivity',-.02)])
    replace('export_farms',[gdp(-.30),asset(60,'agriculture_district'),mod('agricolture_productivity_modifier',.08),faction('farmers',-5)])
    replace('rural_services',[gdp(-.30),asset(59,'agriculture_district'),mod('agricolture_productivity_modifier',.04),faction('farmers',10),mod('social_cost_multiplier_modifier',.04)])
    replace('telecoms',[gdp(-.45),asset(56,'internet_station'),asset(62,'internet_station'),research('electronics',.50)],
            'Fund PTT and CNET network equipment, switching research and long-distance connections. New exchanges in the Paris and Rhone-Alpes service areas strengthen a telephone network that still falls short of public demand.')
    replace('conversion',[gdp(-.35),research('industry',.50),faction('labour_unions',10),mod('production_factory_efficiency_gain_factor',.04),mod('social_cost_multiplier_modifier',.05)])

    replace('citizen_army',[doctrine('land',.25),xp('army',20),mod('army_core_defence_factor',.06),mod('land_reinforce_rate',.02),mod('training_time_army_factor',.08),mod('army_personnel_cost_multiplier_modifier',.04)])
    replace('professional_core',[doctrine('land',.50),xp('army',25),mod('army_org_factor',.04),mod('army_personnel_cost_multiplier_modifier',.10)])
    replace('escort_navy',[gdp(-.35),asset(63,'naval_base',province=11834),research('naval',.50),mod('naval_accidents_chance',-.08),mod('foreign_influence_modifier',-.03)])
    replace('logistics',[gdp(-.30),asset(55,'naval_base',province=6449),mod('supply_consumption_factor',-.05),mod('bureaucracy_cost_multiplier_modifier',.04)])
    replace('flight_schools',[gdp(-.20),xp('air',25),doctrine('air',.25),mod('air_accidents_factor',-.08),mod('airforce_personnel_cost_multiplier_modifier',.05)])
    replace('mirage',[gdp(-.35),research('air_equipment',.75),xp('air',20),mod('air_accidents_factor',-.05),mod('equipment_cost_multiplier_modifier',.03)])
    replace('nato_land_priority',[gdp(-.50),asset(54,'arms_factory'),mod('military_factories_productivity',.04),mod('equipment_cost_multiplier_modifier',.03)])
    replace('nato_sea_priority',[gdp(-.50),asset(64,'dockyard'),mod('dockyard_productivity',.05),mod('navy_personnel_cost_multiplier_modifier',.05)])
    replace('nato_conditional_plan',[gdp(-.10),doctrine('land',.25),mod('max_planning',.03),mod('army_personnel_cost_multiplier_modifier',.03)])
    replace('nato_fleet_support',[gdp(-.25),asset(64,'naval_base',province=6536),mod('supply_consumption_factor',-.03),mod('navy_personnel_cost_multiplier_modifier',.03)])

    # New foreign assets remain solely in the recipient-approved prospective terms.
    offer_changes=[]
    def offer_terms(key,france,recipient):
        n=nodes[key];n['offer']['france']['effects']=france;n['offer']['recipient']['effects']=recipient
        offer_changes.append(key)
    offer_terms('airbus',
                [gdp(-.50),asset(61,'industrial_complex'),research('air_equipment',.50),weekly(.06)],
                [gdp(-.50),asset(1080,'industrial_complex'),research('air_equipment',.50),weekly(.06)])
    offer_terms('concorde',
                [gdp(-.35),research('air_equipment',.75),research('electronics',.50),mod('research_speed_factor',.03),weekly(.10)],
                [gdp(-.35),research('air_equipment',.75),research('electronics',.50),mod('research_speed_factor',.03),weekly(.10)])
    offer_terms('symphonie',
                [gdp(-.20),asset(56,'internet_station'),research('electronics',.50),weekly(.04)],
                [gdp(-.20),asset(42,'internet_station'),research('electronics',.50),weekly(.04)])
    offer_terms('rhine',
                [gdp(-.50),asset(57,'industrial_complex'),research('industry',.50),weekly(.04)],
                [gdp(-.50),asset(42,'industrial_complex'),research('industry',.50),weekly(.04)])
    for key,service in [('nato_rhine','land'),('nato_atlantic_fleet','naval')]:
        for side in ('france','recipient'):
            nodes[key]['offer'][side]['effects'].append(doctrine(service,.25))
        offer_changes.append(key)

    # Normalise every asset and one-time debit, including untouched focus/decision/offer rows.
    def normalise(effects):
        out=[];fee=sum(e['percent'] for e in effects if e['kind']=='treasury_gdp')
        if fee:out.append(gdp(round(fee,5)))
        for e in effects:
            if e['kind']=='treasury_gdp':continue
            if e['kind']=='building':
                e['slots']=e['amount'];e['slots_before_construction']=True;e['once']=True
                e['transaction']='Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit.'
            if e['kind'] in ('research','doctrine','experience','faction_opinion'):e['once']=True
            out.append(e)
        return out
    for n in ns['nodes']:
        n['effects']=normalise(n['effects'])
        n['reward_guards']=list(n['conditions'])
        if n.get('offer'):
            for side in ('france','recipient'):
                n['offer'][side]['effects']=normalise(n['offer'][side]['effects'])
            n['offer']['cost_basis']='Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.'
            n['offer']['asset_execution']='Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.'
    for decision in design['decisions']:decision['effects']=normalise(decision['effects'])
    nodes['oil_resilience']['conditions'].append('Chosen civil nuclear strategy: a supplied French reactor operates; or the funded diversified generation and conservation programme is in place')
    for key in ('telecoms','symphonie'):
        nodes[key]['conditions'].append('has_tech = internet_1')
    nodes['symphonie']['conditions'].append('GER = { has_tech = internet_1 }')
    design['reward_revision']=dict(source='reward_revision.py',changed_focuses=changed,changed_offers=offer_changes,
        historical_basis='REWARD_PRECEDENTS.md',native_evidence=['GDP_COST_REFERENCE.md','REWARD_ASSET_REFERENCE.md'],
        research_slots='No extra untracked research slot: native MD GDP/GDP-per-capita slot management remains authoritative.',
        one_time='Buildings, extra slots, experience, research, doctrine uses and faction-opinion changes never replay on party return or treaty restoration.')
    return design['reward_revision']
