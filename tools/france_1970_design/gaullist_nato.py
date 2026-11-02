# IMPERIA COLD WAR — Gaullist NATO strategy concept for France, 1970-1990.
"""Append a historically grounded policy subtree without touching loaded mod files."""

def append_nato(ns):
    group,focus,choice,offer=(ns[k] for k in ('group','focus','choice','offer'))
    mod,gdp,pp,research,xp,weekly=(ns[k] for k in ('mod','gdp','pp','research','xp','weekly'))
    def doctrine(category,reduction=.25):
        return dict(kind='doctrine',category=category,reduction=reduction,uses=1)

    # Translate only the shared economy footprint to reserve the full Gaullist extension.
    economy=next(g for g in ns['groups'] if g['id']=='economy')
    economy['x']+=20
    for n in ns['nodes']:
        if n['group']=='economy':n['x']+=20

    g=group('udr_nato','Gaullist NATO Strategy',20,7,1,'western_conservatism_are_in_power',
            'A UDR sub-tree. France remains a NATO treaty member outside integrated military command. The three strategies prioritise different funded capabilities and partnerships, not three fictional accession statuses.')
    g['parent_group']='udr'
    g['governing_group']='udr'
    g['activation_conditions']=['western_conservatism_are_in_power = yes','has_idea = NATO_member']
    ns['g']=g # The existing consent-offer helper uses the active section.
    begin=len(ns['nodes'])

    focus(g,'nato_review','France and NATO',0,0,
          'France remains bound by the Atlantic Treaty after the 1966 command withdrawal. Pompidou can reaffirm national discretion, deepen conditional military cooperation or concentrate on a European contribution to the Alliance. None of these choices transfers authority over the French deterrent.',
          [gdp(-.05),pp(-35),xp('army',10),xp('navy',10)],['gaullist_success'],cost=5,
          basis='NATO historical account; Ailleret-Lemnitzer exchange of letters, 1967.')

    focus(g,'nato_nuclear_veto','National Nuclear Veto',-2,2,
          'Finance an independent assessment and decision system for the force de frappe. National authority strengthens the Gaullist mandate while France bears the full equipment-support burden of its separate capability.',
          [pp(-40),mod('political_power_factor',.05),mod('equipment_cost_multiplier_modifier',.02)],['nato_review'],cost=5,
          basis='Gaullist national nuclear authority. The cost modifier changes the recurring MD equipment bill, not factory IC.')
    focus(g,'nato_nuclear_consult','Consult, Never Delegate',2,2,
          'Consult allies about deterrence and escalation while reserving the final decision to France. Better understanding of allied doctrine does not entail NPG membership, nuclear sharing or an allied veto over French weapons.',
          [pp(-40),doctrine('land_doctrine',.25),mod('foreign_influence_modifier',.03),mod('political_power_factor',-.03)],['nato_review'],cost=5,
          basis='NATO consultation and France national-command reservations; Ottawa 1974 as a later precedent, not a treaty already signed in 1970.')
    choice('nato_nuclear_veto','nato_nuclear_consult')

    nuclear=[('nato_nuclear_veto','nato_nuclear_consult')]
    focus(g,'nato_independent','An Independent Ally',-4,4,
          'Keep Atlantic political solidarity while concentrating discretionary defence funds on capabilities controlled and sustained by France. A stronger independent position reduces outside leverage but duplicates part of the equipment-support establishment.',
          [gdp(-.10),mod('foreign_influence_defense_modifier',.05),mod('equipment_cost_multiplier_modifier',.02)],nuclear,
          basis='Historical Gaullist position: treaty solidarity and national command. Exclusive choice allocates an additional programme budget, not a legal ban on other cooperation.')
    focus(g,'nato_pragmatic','Selective Cooperation',0,4,
          'Extend liaison, exercises and contingency preparation under national authority. France can improve practical support without assigning forces automatically to allied command, at the cost of a larger coordination staff.',
          [gdp(-.08),mod('supply_consumption_factor',-.02),mod('bureaucracy_cost_multiplier_modifier',.02)],nuclear,
          basis='Ailleret-Lemnitzer 1967; Valentin-Ferber 1974 as a later expansion precedent.')
    focus(g,'nato_european','A European Pillar',4,4,
          'Concentrate the new programme on European capability and compatible equipment. A larger European voice within the Alliance requires technical preparation and sustained political coordination.',
          [gdp(-.12),research('electronics',.25),mod('foreign_influence_modifier',.04),mod('bureaucracy_cost_multiplier_modifier',.03)],nuclear,
          basis='Elysee Treaty 1963; Ottawa Declaration 1974; later bilateral defence cooperation. This is a policy direction, not a 1970 Franco-German brigade.')
    for a,b in [('nato_independent','nato_pragmatic'),('nato_independent','nato_european'),('nato_pragmatic','nato_european')]:choice(a,b)

    focus(g,'nato_land_priority','National Land Forces',-5,6,
          'Fund the French land-equipment base and the training needed for an independent continental contribution. Domestic output expands while sustaining the equipment estate becomes more expensive.',
          [gdp(-.15),mod('industrial_capacity_factory',.04),mod('equipment_cost_multiplier_modifier',.03)],['nato_independent'])
    focus(g,'nato_sea_priority','Independent Sea Power',-3,6,
          'Give the discretionary programme to national naval construction and support. More shipyard capacity requires a larger naval personnel establishment.',
          [gdp(-.15),mod('industrial_capacity_dockyard',.05),mod('navy_personnel_cost_multiplier_modifier',.05)],['nato_independent'])
    choice('nato_land_priority','nato_sea_priority')
    focus(g,'nato_land_design','National Armour Design',-5,8,
          'Carry the national land programme through testing and engineering. Independent design expertise must be financed rather than obtained through an automatic technology award.',
          [gdp(-.15),research('armor',.50),doctrine('land_doctrine',.25)],['nato_land_priority'])
    focus(g,'nato_sea_design','National Naval Design',-3,8,
          'Fund design teams and sea trials for a fleet sustained by French institutions. The programme develops knowledge without granting ships or future hull technology.',
          [gdp(-.15),research('naval',.50),doctrine('naval_doctrine',.25)],['nato_sea_priority'])

    offer('nato_rhine','Rhine Field Exercises',-1,6,'GER',
          'Offer an additional Franco-German land-exercise programme alongside the existing arrangements for French forces in Germany. Each government retains control of its forces; no new basing rights or automatic wartime commitment are imposed.',
          [mod('army_org_regain',.02),weekly(0.03)],
          [mod('army_org_regain',.02),weekly(0.02)],['nato_pragmatic'],
          setup_fr=.08,setup_other=.08,family='gaullist_operational_cooperation',
          conditions=['GER = { has_idea = NATO_member }'],
          basis='Additional RP programme based on the 1966 stationing settlement and 1967 conditional cooperation. German acceptance approves this bilateral exercise package only.')
    offer('nato_atlantic_fleet','Atlantic Naval Exercises',1,6,'ENG',
          'Offer Britain a funded programme of sea exercises and fleet-support training. Its authority is bilateral and leaves both governments free to decide whether to commit ships in a crisis.',
          [mod('naval_accidents_chance',-.05),xp('navy',15),weekly(0.03)],
          [mod('naval_accidents_chance',-.05),xp('navy',15),weekly(0.02)],['nato_pragmatic'],
          setup_fr=.08,setup_other=.08,family='gaullist_operational_cooperation',
          conditions=['ENG = { has_idea = NATO_member }'],
          basis='Plausible additional Franco-British naval training agreement, not a claim of a NATO-wide decision.')
    choice('nato_rhine','nato_atlantic_fleet')
    focus(g,'nato_conditional_plan','Conditional War Plans',-1,8,
          'Train national staffs to coordinate an agreed contingency while preserving the French decision to commit forces. Reliable planning requires a continuing personnel allocation.',
          [gdp(-.06),mod('max_planning',.03),mod('army_personnel_cost_multiplier_modifier',.03)],['nato_rhine'],
          conditions=['has_idea = COLDWAR_FRA2_nato_rhine_france'],basis='Ailleret-Lemnitzer model; Valentin-Ferber provides a later extension precedent.')
    focus(g,'nato_fleet_support','Compatible Fleet Support',1,8,
          'Apply the lessons of the agreed naval exercises to French fleet support. More efficient supply comes with a larger trained support establishment.',
          [gdp(-.06),mod('supply_consumption_factor',-.03),mod('navy_personnel_cost_multiplier_modifier',.03)],['nato_atlantic_fleet'],
          conditions=['has_idea = COLDWAR_FRA2_nato_atlantic_fleet_france'],basis='National training follow-through under the active recipient-approved bilateral programme.')

    offer('nato_europe_land','European Land Standards',3,6,'GER',
          'Offer West Germany an additional programme for compatible land equipment and maintenance standards. Both states can reduce their equipment-support bills while financing common technical work; no national force is transferred to a new command.',
          [research('armor',.50),mod('equipment_cost_multiplier_modifier',-.04),weekly(0.04)],
          [research('armor',.50),mod('equipment_cost_multiplier_modifier',-.04),weekly(0.04)],['nato_european'],
          setup_fr=.12,setup_other=.12,family='gaullist_european_pillar',
          conditions=['GER = { has_idea = NATO_member }'],
          basis='Plausible earlier bilateral standardisation programme. The Franco-German Defence Council of 1988 and brigade of 1989 are later precedents, not starting institutions.')
    offer('nato_europe_sea','European Naval Industry',5,6,'ENG',
          'Offer Britain a European naval engineering and production partnership. Shared development helps both shipbuilding sectors while requiring a continuing public contribution.',
          [research('naval',.50),mod('industrial_capacity_dockyard',.04),weekly(0.04)],
          [research('naval',.50),mod('industrial_capacity_dockyard',.04),weekly(0.04)],['nato_european'],
          setup_fr=.12,setup_other=.12,family='gaullist_european_pillar',
          conditions=['ENG = { has_idea = NATO_member }'],
          basis='Plausible Franco-British European capability agreement; Britain was already a NATO ally in 1970. EEC membership is not required.')
    choice('nato_europe_land','nato_europe_sea')
    focus(g,'nato_common_maintenance','Common Maintenance',3,8,
          'Turn agreed land-equipment standards into training and support routines within the French forces. The partnership provides experience while France funds its own personnel.',
          [gdp(-.08),doctrine('land_doctrine',.25),mod('army_personnel_cost_multiplier_modifier',.02)],['nato_europe_land'],
          conditions=['has_idea = COLDWAR_FRA2_nato_europe_land_france'],basis='National implementation of an accepted bilateral standardisation programme.')
    focus(g,'nato_europe_staff','European Naval Staffs',5,8,
          'Develop French naval doctrine through the agreed European industrial programme. Staff exchanges and technical analysis require a permanent administrative effort.',
          [gdp(-.08),doctrine('naval_doctrine',.50),mod('bureaucracy_cost_multiplier_modifier',.02)],['nato_europe_sea'],
          conditions=['has_idea = COLDWAR_FRA2_nato_europe_sea_france'],basis='National follow-through under an actual active Franco-British agreement.')

    for n in ns['nodes'][begin:]:
        n['conditions'].insert(1,'has_idea = NATO_member')
        n['source_refs']=['NATO_HISTORY.md','NATO_MECHANICS.md']
        n['nato_policy']='Treaty membership retained; national command and nuclear decision remain French.'
        # Membership gates current programmes as well as focus completion.
        n['reward_guards']=list(n['conditions'])
        n['activation_conditions']=[c for c in n['conditions'] if c.startswith('has_idea = ')]+['western_conservatism_are_in_power = yes']
        if n.get('offer'):
            n['offer']['activation_conditions']=['FRA = { has_idea = NATO_member }',n['offer']['partner']+' = { has_idea = NATO_member }']
            n['offer']['activation_note']='Membership requirements supplement the bilateral peace, embargo and four mirrored sanction guards. Current French party is not a condition of an already signed treaty.'
            n['offer']['acceptance_conditions']=list(n['conditions'])+['Both signatories exist','Bilateral peace','No native embargo in either direction','No diplomatic, financial, economic or military Imperia sanction in either direction','Named recipient chooses Accept','The proposal has not been declined, expired or already applied']
            n['offer']['acceptance_transaction']='Recheck all conditions on response. Charge both displayed setup amounts and award both sides atomically once. Record signed receipts before issuing finite XP or research. Reconciliation never repeats setup or finite awards.'
    return dict(nodes=len(ns['nodes'])-begin,group='udr_nato',main_paths=['nato_independent','nato_pragmatic','nato_european'],
                membership='All paths require and retain NATO_member. No NATO_join or NATO_leave call is proposed.',
                nuclear='Independent nuclear authority remains in every path; consultation grants neither NPG membership nor nuclear sharing.',
                parent_activation='Cooperation-derived party programmes require both current UDR government and the actual active parent agreement. Treaties survive government change; no finite award replays.',
                baseline='Existing 1967 arrangements remain historical starting context; offers fund additional activity, not retroactive consent for signed agreements.')
