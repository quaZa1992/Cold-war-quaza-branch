# IMPERIA COLD WAR — France 1970 replacement concept, approval phase only.
"""Single spatial and numeric source for the review catalogue. Writes no runtime files."""
from pathlib import Path
from decimal import Decimal
import json

OUT=Path(__file__).resolve().parent
groups=[]
nodes=[]
spirits=[]

def mod(key,value): return dict(kind='modifier',key=key,value=value)
def gdp(percent):
    fraction=Decimal(str(percent))/100
    literal=format(fraction,'.5f')
    assert fraction and Decimal(literal)==fraction, 'Treasury GDP share needs an exact nonzero literal with at most five fractional digits'
    return dict(kind='treasury_gdp',percent=percent,gdp_fraction=float(fraction),runtime_share_literal=literal,base='gdp_total',payer='own_country',valuation='at_payment',once=True)
def pp(value): return dict(kind='political_power',value=value)
def asset(state,building,amount=1,province=None):
    effect=dict(kind='building',state=state,building=building,amount=amount,slots=amount,slots_before_construction=True,once=True)
    if province is not None:effect['province']=province
    return effect
def research(category,bonus=.5,uses=1):
    tags={'industry':'CAT_industry','electronics':'CAT_electronics','armor':'CAT_armor','nuclear':'CAT_nuclear_reactors','light_air':'CAT_aircraft','air_equipment':'CAT_aircraft','naval':'CAT_naval'}
    return dict(kind='research',category=tags.get(category,category),bonus=bonus,uses=uses)
def xp(service,amount): return dict(kind='experience',service=service,amount=amount)
def remove(key): return dict(kind='remove_spirit',spirit='COLDWAR_FRA2_'+key)
def unlock(key,label): return dict(kind='unlock_decision',id='COLDWAR_FRA2_'+key,label=label)
def weekly(annual_gdp_percent):
    fraction=Decimal(str(annual_gdp_percent))/100
    literal=format(fraction,'.5f')
    assert fraction>0 and Decimal(literal)==fraction, 'Weekly appropriation needs an exact positive GDP-share literal with at most five fractional digits'
    return dict(kind='weekly_gdp_expense',annual_gdp_percent=annual_gdp_percent,gdp_fraction=float(fraction),runtime_share_literal=literal,divisor=52,base='gdp_total',payer='own_country',valuation='weekly_recalculation')

def group(key,title,x,y,slot=None,trigger=None,context=''):
    g=dict(id=key,title=title,x=x,y=y,slot=slot,trigger=trigger,context=context)
    groups.append(g)
    return g

def focus(g,key,title,x,y,description,effects,parents=(),cost=7,conditions=(),basis='historical policy precedent',lifetime=None):
    f=dict(id='COLDWAR_FRA2_'+key,key=key,group=g['id'],title=title,x=g['x']+x,y=g['y']+y//2,
           description=description,effects=effects,prerequisites=[[p] if isinstance(p,str) else list(p) for p in parents],
           exclusions=[],cost=cost,days=cost*7,conditions=list(conditions),basis=basis,
           lifetime=lifetime or ('government' if g['slot'] is not None else 'national'),
           spirit='COLDWAR_FRA2_'+g['id']+'_programme',icon=g['id'])
    if g['trigger']: f['conditions'].insert(0,g['trigger']+' = yes')
    nodes.append(f)
    return key

def choice(a,b):
    aa=next(n for n in nodes if n['key']==a);bb=next(n for n in nodes if n['key']==b)
    aa['exclusions'].append(b);bb['exclusions'].append(a)

def start(key,title,description,effects,remedy):
    spirits.append(dict(id='COLDWAR_FRA2_'+key,title=title,description=description,effects=effects,remedy=remedy))

start('presidency','The Fifth Republic','Pompidou inherits a powerful presidency and a large Gaullist majority. Administrative concentration gives the executive room to act while narrowing parliamentary and local influence.',[mod('political_power_factor',.10),mod('bureaucracy_cost_multiplier_modifier',.05),mod('stability_factor',-.02)],'Executive Guarantees or Parliamentary Responsibility replaces this spirit.')
start('grenelle','The Unfinished Settlement of Grenelle','The wage settlement ended a national confrontation without resolving disputes over management, representation and the distribution of growth.',[mod('stability_factor',-.04),mod('production_factory_efficiency_gain_factor',-.05),mod('social_cost_multiplier_modifier',.05)],'A shared negotiated or statutory settlement replaces this spirit; party spending alone does not erase it.')
start('regions','Uneven Modernisation','Competitive firms and ambitious public projects coexist with crowded cities, remote rural communities and vulnerable industrial districts.',[mod('production_speed_industrial_complex_factor',.05),mod('production_speed_infrastructure_factor',-.08)],'Regional Connections and an industrial strategy remove the starting imbalance.')
start('oil','Oil-Intensive Growth','Cheap imported oil sustains transport and industry. High demand leaves national prosperity exposed to supply disputes, price changes and the exchange rate.',[mod('energy_use_modifier_civs',.08)],'The selected energy programme reduces the burden; no automatic 1973 shock is applied in 1970.')
start('education','A Narrow Route to Expertise','Elite schools and national laboratories support advanced science, while technical training and mass university provision struggle to keep pace.',[mod('research_speed_factor',.03),mod('education_cost_multiplier_modifier',.10),mod('production_factory_efficiency_gain_factor',-.03)],'Technical Colleges or Mass University Funding replaces this spirit with its stated outcome.')
start('deterrent','The Price of Independence','The national deterrent and an independent procurement system preserve strategic freedom while drawing resources from conventional forces and civilian investment.',[mod('war_support_factor',.05),mod('equipment_cost_multiplier_modifier',.05)],'The defence chapter replaces this inherited strategic settlement, preserving actual native nuclear running costs.')
start('postcolonial','The Postcolonial Settlement','Repatriation, migrant housing and competing memories of Algeria burden public trust. Overseas commitments also test the reach of a centralised state.',[mod('stability_factor',-.02),mod('bureaucracy_cost_multiplier_modifier',.05)],'Housing and Integration plus either Memory and Recognition or Republican Amnesties replaces this spirit.')
start('franc_stabilisation','After the 1969 Devaluation','The franc adjustment supports export orders, while the credit restraint used to stabilise demand weighs on construction and domestic investment.',[mod('industrial_capacity_factory',.03),mod('production_speed_buildings_factor',-.04)],'Temporary opening condition: ends after 270 days, representing the easing of 1970 restrictions; never re-applied.')
spirits[-1]['days']=270

g=group('institutions','Republic and Society',6,0,context='Shared institutions. Pompidou remains the historical starting president.')
focus(g,'public_service','A State Within Reach',0,0,'Prefects and central ministries possess formidable authority. A practical administrative reform can shorten the distance between citizens and public services.',[gdp(-.08),mod('bureaucracy_cost_multiplier_modifier',-.03)],cost=5)
focus(g,'executive','Executive Guarantees',-2,2,'Defend the presidential mandate while placing the emergency machinery of the Fifth Republic on a clearer statutory footing.',[remove('presidency'),mod('political_power_factor',.12),mod('stability_factor',-.02),mod('bureaucracy_cost_multiplier_modifier',.03)],['public_service'])
focus(g,'parliament','Parliamentary Responsibility',2,2,'Strengthen scrutiny of ministers and public appointments without returning France to the unstable cabinet arithmetic of the Fourth Republic.',[remove('presidency'),mod('stability_factor',.05),mod('political_power_factor',-.05),mod('bureaucracy_cost_multiplier_modifier',-.03)],['public_service'])
choice('executive','parliament')
focus(g,'contract','A Negotiated Social Settlement',-2,4,'Bring employers and unions into regular national bargaining. Wage assurances must be matched by investment and reliable public financing.',[gdp(-.10),remove('grenelle'),mod('stability_factor',.05),mod('production_factory_efficiency_gain_factor',.03),mod('social_cost_multiplier_modifier',.08)],['executive' if False else ('executive','parliament')])
focus(g,'statute','A Statutory Social Settlement',2,4,'Legislate minimum protections and clear strike procedures. National standards can secure continuity, but imposed terms risk weakening workplace consent.',[gdp(-.06),remove('grenelle'),mod('production_factory_efficiency_gain_factor',.06),mod('stability_factor',-.02),mod('police_cost_multiplier_modifier',.04)],[('executive','parliament')])
choice('contract','statute')
focus(g,'housing','Housing and Integration',0,6,'Replace precarious accommodation with serviced housing and open municipal services to families already sustaining the industrial workforce.',[gdp(-.20),mod('stability_factor',.03),mod('social_cost_multiplier_modifier',.05)], [('contract','statute')])
focus(g,'memory','Memory and Recognition',-2,8,'Recognise the distinct experiences of veterans, harkis, repatriates and Algerian families. Public recognition commits the state to support as well as remembrance.',[pp(-50),mod('stability_factor',.04),mod('social_cost_multiplier_modifier',.03)],['housing'])
focus(g,'amnesty','Republican Amnesties',2,8,'Extend the logic of the late-1960s amnesties to close domestic conflicts over Algeria. Reconciliation with former opponents leaves other claims unresolved.',[pp(60),mod('war_support_factor',.03),mod('stability_factor',-.02)],['housing'])
choice('memory','amnesty')
focus(g,'civic_settlement','A Common Civic Settlement',0,10,'Give public institutions a durable basis for integration and remembrance, without requiring citizens to share a single account of the end of empire.',[remove('postcolonial'),mod('bureaucracy_cost_multiplier_modifier',-.02)], [('memory','amnesty')],cost=5)

g=group('udr','UDR: Gaullist Government',20,0,1,'western_conservatism_are_in_power','Pompidou and Chaban-Delmas. UDR becomes RPR only through actual dated party identity changes.')
focus(g,'progress','Contracts for Progress',0,0,'Chaban-Delmas proposes to replace entrenched confrontation with negotiated progress in public enterprises. The presidency must decide how far that opening should go.',[gdp(-.10),mod('production_factory_efficiency_gain_factor',.04),mod('bureaucracy_cost_multiplier_modifier',.03)],cost=5)
focus(g,'new_society','The New Society',-3,2,'Give the prime minister a mandate for social negotiation, technical education and a less hierarchical public sphere.',[mod('stability_factor',.06),mod('education_cost_multiplier_modifier',.06),mod('political_power_factor',-.04)],['progress'])
focus(g,'presidential_industry','The Industrial Presidency',3,2,'Concentrate the presidency on industrial scale, exports and decisive administration. Social opening yields to the priorities of productive investment.',[mod('civilian_factories_productivity',.07),mod('production_factory_max_efficiency_factor',.04),mod('stability_factor',-.03)],['progress'])
choice('new_society','presidential_industry')
focus(g,'ortf','An Independent Public Broadcaster',-3,4,'Loosen direct ministerial supervision of the ORTF. A more credible public service limits the executive influence that Gaullist government has long enjoyed.',[mod('stability_factor',.04),mod('political_power_factor',-.04)],['new_society'])
focus(g,'national_champions','National Industrial Champions',3,4,'Support concentrated national firms capable of entering international markets. The state accepts greater financial exposure and less domestic competition.',[gdp(-.25),mod('industrial_capacity_factory',.06),mod('production_factory_efficiency_gain_factor',.04),mod('corporate_tax_income_multiplier_modifier',-.04)],['presidential_industry'])
focus(g,'participation','Participation in the Enterprise',-2,6,'Turn Gaullist participation into a funded system of profit sharing and workplace representation. Wage earners gain a stake at a cost to retained profits.',[mod('stability_factor',.05),mod('production_factory_efficiency_gain_factor',.03),mod('corporate_tax_income_multiplier_modifier',-.05)],[('ortf','national_champions')])
focus(g,'management','Managerial Autonomy',2,6,'Give public enterprises room to set investment and employment priorities. Commercial discipline can improve output while weakening political guarantees to workers.',[mod('civilian_factories_productivity',.06),mod('corporate_tax_income_multiplier_modifier',.05),mod('stability_factor',-.04)],[('ortf','national_champions')])
choice('participation','management')
focus(g,'debre','Debre and Strategic Sovereignty',-2,8,'Support an orthodox defence of national decision-making inside Gaullism. Domestic armament capacity is prioritised over cheaper pooled procurement.',[mod('industrial_capacity_factory',.05),mod('equipment_cost_multiplier_modifier',.06),research('armor',.5)],['participation'])
focus(g,'pompidou_europe','Pompidou at The Hague',2,8,'Use the opening achieved at The Hague to pursue enlargement and practical European cooperation, while preserving a French voice within it.',[mod('foreign_influence_modifier',.08),mod('political_power_factor',-.03),unlock('hague_talks','European enlargement talks')],['management'])
focus(g,'gaullist_success','A Renewed Gaullist Majority',0,10,'Rebuild the governing movement around a social and industrial programme that can outlast its founding president.',[mod('political_power_factor',.06),mod('bureaucracy_cost_multiplier_modifier',.03)],[('debre','pompidou_europe')],cost=5)

g=group('ri','Independent Republicans',36,0,2,'western_liberals_are_in_power','Giscard leads a distinct liberal conservative programme. Governing requires native slot 2, not coalition membership.')
focus(g,'liberal_state','A Modern Liberal State',0,0,'Giscardian reform links administrative competence to private initiative. Support for enterprise requires visible restraints on public privilege.',[gdp(-.08),mod('bureaucracy_cost_multiplier_modifier',-.05),mod('political_power_factor',-.03)],cost=5)
focus(g,'sound_franc','A Sound Franc',-2,2,'Defend monetary credibility through tighter public demand and a consistent budget. Investors gain confidence while domestic expansion slows.',[mod('tax_gain_multiplier_modifier',.06),mod('production_speed_buildings_factor',-.04),mod('stability_factor',.02)],['liberal_state'])
focus(g,'credit_expansion','Credit for Modernisation',2,2,'Direct cheaper credit toward modern equipment and housing. Faster construction brings a continuing subsidy bill and a looser claim on fiscal restraint.',[mod('production_speed_buildings_factor',.08),mod('civilian_factories_productivity',.03),mod('tax_gain_multiplier_modifier',-.05)],['liberal_state'])
choice('sound_franc','credit_expansion')
focus(g,'business','Enterprise Beyond the State',-2,4,'Reduce barriers facing smaller firms and challenge established public monopolies. A broader investment base requires surrendering some fiscal privileges.',[gdp(-.12),mod('corporate_tax_income_multiplier_modifier',-.06),mod('country_productivity_growth_modifier',.05)],['sound_franc'])
focus(g,'public_credit','Public Credit Guarantees',2,4,'Keep public guarantees behind major projects while requiring commercial accounts. The Treasury carries the risk of supporting rapid investment.',[gdp(-.18),mod('production_factory_max_efficiency_factor',.05),mod('bureaucracy_cost_multiplier_modifier',.04)],['credit_expansion'])
focus(g,'civil_liberties','Civil Liberties and Equal Citizenship',0,6,'Extend civil rights and remove barriers facing women and younger citizens. A broader public settlement demands new legal and social provision.',[gdp(-.08),mod('stability_factor',.05),mod('social_cost_multiplier_modifier',.04)],[('business','public_credit')])
focus(g,'atlantic_liberal','An Atlantic Commercial Opening',-2,8,'Seek a close commercial and technical relationship with the United States. Standardisation can reduce costs while tying French firms more closely to external suppliers.',[mod('equipment_cost_multiplier_modifier',-.05),mod('foreign_influence_modifier',-.04),unlock('atlantic_licensing','Atlantic licensing negotiations')],['civil_liberties'])
focus(g,'europe_liberal','A Competitive European Market',2,8,'Build a European market large enough for competitive French firms. The benefits of scale require costly adjustment for sheltered producers.',[mod('civilian_factories_productivity',.06),mod('industrial_capacity_factory',.03),mod('stability_factor',-.03)],['civil_liberties'])
choice('atlantic_liberal','europe_liberal')

g=group('centre','Democratic Centre',48,0,14,'neutrality_neutral_conservatism_are_in_power','CD governs this branch. CDP is a real separate coalition current, represented by an internal cooperation choice until a registry change is approved.')
focus(g,'social_market','A Social Market Republic',0,0,'Lecanuet and the Christian democrats seek to combine enterprise, social responsibility and parliamentary government.',[mod('stability_factor',.04),mod('bureaucracy_cost_multiplier_modifier',.03)],cost=5)
focus(g,'regional_councils','Elected Regional Councils',-2,2,'Give regions a mandate and resources of their own. Local investment gains legitimacy while national direction becomes less immediate.',[gdp(-.12),mod('production_speed_infrastructure_factor',.10),mod('political_power_factor',-.05)],['social_market'])
focus(g,'cdp_compromise','The Duhamel Compromise',2,2,'Follow the CDP precedent of cooperation with the presidential majority, using ministerial influence to secure practical social reforms.',[mod('political_power_factor',.08),mod('education_cost_multiplier_modifier',-.04),mod('bureaucracy_cost_multiplier_modifier',.04)],['social_market'])
choice('regional_councils','cdp_compromise')
focus(g,'mutuals','Mutual Societies and Social Insurance',0,4,'Strengthen non-state social institutions and local provision. Their independence comes with a sustained public contribution.',[gdp(-.08),mod('stability_factor',.05),mod('social_cost_multiplier_modifier',.06)],[('regional_councils','cdp_compromise')])
focus(g,'federal_europe','A Federal European Commitment',-2,6,'Pursue a stronger community of European institutions. Shared capacity gives France influence through agreement rather than unilateral freedom.',[mod('foreign_influence_modifier',.10),mod('political_power_factor',-.05),unlock('community_talks','Community institutional talks')],['mutuals'])
focus(g,'atlantic_security','Atlantic Security and Social Investment',2,6,'Seek allied security cooperation and direct more domestic resources toward public services. France accepts a smaller margin of independent military choice.',[mod('army_personnel_cost_multiplier_modifier',-.06),mod('education_cost_multiplier_modifier',-.03),mod('war_support_factor',-.04)],['mutuals'])
choice('federal_europe','atlantic_security')
focus(g,'centrist_covenant','The Centrist Covenant',0,8,'Bind regional notables, social organisations and parliamentary reformers to a durable governing agreement.',[mod('stability_factor',.03),mod('political_power_factor',.03)],[('federal_europe','atlantic_security')],cost=5)

g=group('radical','Radical Republicans',60,0,16,'neutrality_neutral_libertarians_are_in_power','The unified Radical Party exists in January 1970. Left-radical separation is a later political choice, not a starting party.')
focus(g,'american_challenge','The American Challenge',0,0,'Servan-Schreiber argues that France must answer American scale through education, modern management and a larger European market.',[gdp(-.10),research('electronics'),mod('education_cost_multiplier_modifier',.04)],cost=5)
focus(g,'radical_enterprise','A Republic of Enterprise',-2,2,'Give innovative private firms access to credit and public contracts. Faster renewal requires concessions to business income.',[mod('country_productivity_growth_modifier',.07),mod('corporate_tax_income_multiplier_modifier',-.05)],['american_challenge'])
focus(g,'left_radicals','A Republican Left Alliance',2,2,'Choose the left-radical precedent of social reform and cooperation with the socialist movement, retaining secular republican priorities.',[mod('stability_factor',.06),mod('social_cost_multiplier_modifier',.06),mod('political_power_factor',-.03)],['american_challenge'],basis='Plausible early choice; historical split occurred in 1972.')
choice('radical_enterprise','left_radicals')
focus(g,'secular_school','The Secular School',0,4,'Invest in a common public school system and technical routes beyond the grandes ecoles. The promise of equal access requires sustained funding.',[gdp(-.15),research('industry'),mod('education_cost_multiplier_modifier',.06)],[('radical_enterprise','left_radicals')])
focus(g,'municipal_france','Municipal France',-2,6,'Let towns shape the services and workshops on which local prosperity rests, accepting a less uniform national investment pattern.',[mod('production_speed_infrastructure_factor',.08),mod('bureaucracy_cost_multiplier_modifier',.04)],['secular_school'])
focus(g,'europe_technology','European Technology Ventures',2,6,'Pool development programmes across European firms. Joint standards offer scale while reducing the share of contracts kept within France.',[research('electronics',.75),mod('research_speed_factor',.02),mod('corporate_tax_income_multiplier_modifier',-.03)],['secular_school'])
choice('municipal_france','europe_technology')

g=group('ps','Socialist Party',74,0,3,'western_social_democrats_are_in_power','PS exists under Alain Savary in 1970. CIR and the 1971 Epinay refoundation belong to its development, not an invented 1970 Mitterrand PS presidency.')
focus(g,'socialist_refoundation','Refound the Socialist Movement',0,0,'Rebuild a disoriented socialist movement and negotiate with the republican clubs. A democratic alternative requires agreement on both institutions and ownership.',[pp(-40),mod('political_power_factor',.06),mod('bureaucracy_cost_multiplier_modifier',.03)],cost=5)
focus(g,'common_programme','The Common Programme',-3,2,'Negotiate a governing programme with the Communists and left radicals, placing public ownership and social rights at the centre of the alliance.',[mod('stability_factor',.05),mod('industrial_capacity_factory',.05),mod('bureaucracy_cost_multiplier_modifier',.07)],['socialist_refoundation'])
focus(g,'democratic_left','An Independent Democratic Left',3,2,'Seek a socialist majority through republican alliances and a clearer distance from the PCF. Greater flexibility comes at the cost of labour unity.',[mod('political_power_factor',.08),mod('tax_gain_multiplier_modifier',.04),mod('stability_factor',-.03)],['socialist_refoundation'])
choice('common_programme','democratic_left')
focus(g,'public_banks','Public Banks and Industrial Credit',-3,4,'Bring the commanding channels of credit into public ownership. Directed investment demands capital and a larger administrative apparatus.',[gdp(-.35),mod('production_speed_buildings_factor',.08),mod('bureaucracy_cost_multiplier_modifier',.06)],['common_programme'])
focus(g,'social_contract_ps','Collective Bargaining and Public Services',3,4,'Put negotiated wage standards and dependable services ahead of a general transfer of ownership.',[gdp(-.18),mod('stability_factor',.06),mod('social_cost_multiplier_modifier',.08)],['democratic_left'])
focus(g,'redistribution','Redistribution and Demand',-2,6,'Expand household purchasing power and public employment. Domestic demand strengthens while tax receipts and external competitiveness come under pressure.',[mod('stability_factor',.06),mod('production_speed_industrial_complex_factor',.06),mod('tax_gain_multiplier_modifier',-.06)],[('public_banks','social_contract_ps')])
focus(g,'competitiveness_ps','A Productive Social Compact',2,6,'Trade a slower expansion of current benefits for investment, training and a more resilient export sector.',[mod('civilian_factories_productivity',.07),mod('production_factory_efficiency_gain_factor',.04),mod('education_cost_multiplier_modifier',.05)],[('public_banks','social_contract_ps')])
choice('redistribution','competitiveness_ps')
focus(g,'defferre','The Defferre Reforms',0,8,'Transfer practical authority from prefects to elected territorial institutions. Public investment gains local direction at the cost of central coordination.',[gdp(-.15),mod('production_speed_infrastructure_factor',.08),mod('political_power_factor',-.04)],[('redistribution','competitiveness_ps')])
focus(g,'europe_restraint','European Monetary Discipline',-2,10,'Keep a socialist government within a European monetary framework. Fiscal restraint protects credibility while limiting the pace of domestic reform.',[mod('tax_gain_multiplier_modifier',.07),mod('social_cost_multiplier_modifier',-.03),mod('stability_factor',-.04)],['defferre'])
focus(g,'sovereign_reflation','A Sovereign Reflation',2,10,'Retain national control of demand and credit instead of accepting an external monetary constraint. Productive expansion risks fiscal and diplomatic friction.',[mod('production_speed_buildings_factor',.08),mod('tax_gain_multiplier_modifier',-.06),mod('foreign_influence_modifier',-.04)],['defferre'])
choice('europe_restraint','sovereign_reflation')

g=group('pcf','French Communist Party',90,0,4,'emerging_communist_state_are_in_power','PCF under Rochet, with Marchais rising. Eurocommunist and orthodox options are real internal tensions, not separate invented mass parties.')
focus(g,'advanced_democracy','An Advanced Democracy',0,0,'Build on communist municipalities and organised labour to seek national power. Parliamentary advances do not settle the argument over the party and the state.',[mod('stability_factor',.04),mod('bureaucracy_cost_multiplier_modifier',.04)],cost=5)
focus(g,'democratic_road','A Democratic Road to Socialism',-3,2,'Accept political pluralism and a negotiated socialist transition. Wider legitimacy requires limits on the authority of the party apparatus.',[mod('stability_factor',.07),mod('political_power_factor',-.05)],['advanced_democracy'])
focus(g,'party_discipline','The Discipline of the Party',3,2,'Prioritise cadre cohesion and central direction. A stronger apparatus can carry a programme through opposition while deepening political mistrust.',[mod('political_power_factor',.12),mod('industrial_capacity_factory',.04),mod('stability_factor',-.06)],['advanced_democracy'])
choice('democratic_road','party_discipline')
focus(g,'municipal_socialism','Municipal Socialism on a National Scale',-3,4,'Extend the service and housing practices of communist municipalities through a national investment programme.',[gdp(-.25),mod('stability_factor',.04),mod('social_cost_multiplier_modifier',.06)],['democratic_road'])
focus(g,'public_combine','Public Industrial Combines',3,4,'Coordinate production, credit and procurement through large public groups. Scale is purchased with administrative cost and less managerial flexibility.',[gdp(-.30),mod('industrial_capacity_factory',.07),mod('production_factory_efficiency_gain_factor',-.04),mod('bureaucracy_cost_multiplier_modifier',.07)],['party_discipline'])
focus(g,'workers_control','Workers in the Boardroom',-2,6,'Give elected workplace representatives binding authority over company planning. Consent can improve implementation while slowing central decisions.',[mod('stability_factor',.06),mod('production_factory_efficiency_gain_factor',.05),mod('political_power_factor',-.04)],[('municipal_socialism','public_combine')])
focus(g,'planned_targets','National Production Targets',2,6,'Direct resources toward a limited set of industrial targets. Higher output must compete with civilian provision and local priorities.',[mod('industrial_capacity_factory',.08),mod('civilian_factories_productivity',-.03),mod('stability_factor',-.03)],[('municipal_socialism','public_combine')])
choice('workers_control','planned_targets')
focus(g,'independent_communism','An Independent French Communism',-2,8,'Affirm a French political course and distance the programme from Soviet direction. Pluralist legitimacy reduces the cohesion of orthodox networks.',[mod('foreign_influence_modifier',.07),mod('stability_factor',.04),mod('political_power_factor',-.04)],['workers_control'])
focus(g,'soviet_friendship','The Soviet Partnership',2,8,'Seek Soviet technical and industrial cooperation while defending the national programme. Access to a partner brings a continuing claim on independent influence.',[mod('land_doctrine_cost_factor',-.06),mod('foreign_influence_modifier',-.05),unlock('soviet_industry_talks','Franco-Soviet industrial talks')],['planned_targets'])
focus(g,'communist_settlement','A French Socialist Settlement',0,10,'Consolidate the institutions of the chosen socialist course, retaining its political and economic commitments.',[mod('stability_factor',.03),mod('bureaucracy_cost_multiplier_modifier',.02)],[('independent_communism','soviet_friendship')],cost=5)

g=group('psu','Unified Socialist Party',106,0,18,'neutrality_neutral_social_are_in_power','PSU has a distinct anti-authoritarian socialist programme. Autogestion is developed as a policy option, not claimed as its settled January 1970 doctrine.')
focus(g,'grassroots_left','The Left Beyond the Apparatus',0,0,'Give local militants, younger workers and university activists a route into national decisions outside the dominant socialist and communist machines.',[mod('stability_factor',.04),mod('political_power_factor',-.03)],cost=5)
focus(g,'self_management','Factories Under Self-Management',-2,2,'Support worker-run firms and cooperative credit, extending experiments in control over production into a national policy.',[gdp(-.18),mod('production_factory_efficiency_gain_factor',.08),mod('bureaucracy_cost_multiplier_modifier',.05)],['grassroots_left'])
focus(g,'union_autonomy','Independent Unions and Sector Bargaining',2,2,'Protect independent unions and negotiate sector settlements without making workplace councils the owners of production.',[mod('stability_factor',.07),mod('social_cost_multiplier_modifier',.07),mod('industrial_capacity_factory',.03)],['grassroots_left'])
choice('self_management','union_autonomy')
focus(g,'decentralised_services','Services Through Local Communities',0,4,'Bring social and educational provision closer to the communities it serves. Local control needs trained personnel and reliable funding.',[gdp(-.12),research('industry'),mod('education_cost_multiplier_modifier',.06)],[('self_management','union_autonomy')])
focus(g,'civilian_republic','A Civilian Social Republic',-2,6,'Reduce the priority of military institutions and redirect attention to social investment. A quieter strategic posture weakens military mobilisation.',[mod('army_personnel_cost_multiplier_modifier',-.07),mod('social_cost_multiplier_modifier',-.03),mod('war_support_factor',-.06)],['decentralised_services'])
focus(g,'citizen_defence','Citizen Defence and Public Service',2,6,'Retain a citizen defence commitment alongside a broad public-service programme, giving local organisations a practical role in national resilience.',[mod('army_core_defence_factor',.06),mod('training_time_army_factor',.05),mod('bureaucracy_cost_multiplier_modifier',.04)],['decentralised_services'])
choice('civilian_republic','citizen_defence')

g=group('ecology','Political Ecology',118,0,17,'neutrality_neutral_green_are_in_power','A future ecological governing alternative, grounded in Dumont 1974 and later movements. Not a mass governing party in January 1970.')
focus(g,'environment_account','The Environmental Account',0,0,'Measure pollution and resource use as public costs. Ecological politics grows from opposition to the social and environmental price of rapid development.',[gdp(-.08),mod('energy_use_modifier_civs',-.04),mod('bureaucracy_cost_multiplier_modifier',.04)],cost=5,basis='Later historical movement; alternate-history electoral accession required.')
focus(g,'efficiency_ecology','Energy Through Conservation',-2,2,'Invest in insulation, efficient transport and less wasteful industry. Reducing demand requires capital before it relieves operating costs.',[gdp(-.22),mod('energy_use_modifier_civs',-.10),mod('production_speed_buildings_factor',-.03)],['environment_account'])
focus(g,'local_generation','Diversified Local Generation',2,2,'Build a decentralised electricity programme around regional resources. A broader supply base requires more coordination and higher initial investment.',[gdp(-.30),mod('energy_gain_multiplier',.08),mod('bureaucracy_cost_multiplier_modifier',.05)],['environment_account'])
choice('efficiency_ecology','local_generation')
focus(g,'land_stewardship','Land and Rural Stewardship',0,4,'Protect rural services and support farming that uses fewer industrial inputs. Lower dependence on scale must be balanced against yields.',[mod('agricolture_productivity_modifier',.05),mod('social_cost_multiplier_modifier',.04)],[('efficiency_ecology','local_generation')])
focus(g,'ecological_industry','An Industrial Conversion',-2,6,'Help firms convert rather than simply close. Cleaner production and new skills demand a costly transition away from the fastest possible output growth.',[gdp(-.20),mod('country_productivity_growth_modifier',.07),mod('industrial_capacity_factory',-.03)],['land_stewardship'])
focus(g,'local_sufficiency','Local Sufficiency',2,6,'Prioritise local production and short supply chains. Less demand on energy and transport comes with a narrower industrial scale.',[mod('energy_use_modifier_civs',-.06),mod('stability_factor',.04),mod('industrial_capacity_factory',-.04)],['land_stewardship'])
choice('ecological_industry','local_sufficiency')

g=group('right','Shopkeepers and the National Right',130,0,20,'nationalist_right_wing_populists_are_in_power','CID is the actual 1970 slot identity. FN requires its real foundation on 5 October 1972 and an alternate-history accession. Separate receipts prevent CID policies becoming FN rewards automatically.')
focus(g,'cid_tax','The Shopkeepers Tax Revolt',-2,0,'Nicoud and the CID challenge taxation and social charges on independent traders. Relief for small business transfers the cost to public finances.',[mod('corporate_tax_income_multiplier_modifier',-.07),mod('stability_factor',.04)],cost=5,conditions=['CID dated identity; before 5 October 1972'])
focus(g,'cid_cooperatives','Cooperative Credit for Small Traders',-2,2,'Create a protected channel of credit and mutual assistance for independent shops facing concentration in distribution.',[gdp(-.12),mod('civilian_factories_productivity',.05),mod('bureaucracy_cost_multiplier_modifier',.04)],['cid_tax'],conditions=['CID dated identity; before 5 October 1972'])
focus(g,'fn_state','An Authoritarian National Programme',2,0,'A marginal nationalist movement seeks governing authority through a major alternate-history shift. Central discipline and exclusion carry serious costs to public trust.',[mod('political_power_factor',.10),mod('stability_factor',-.06),mod('police_cost_multiplier_modifier',.08)],cost=5,conditions=['FN identity; founded on or after 5 October 1972'],basis='Explicit alternate history; not a major January 1970 party.')
focus(g,'fn_protection','Protected National Industry',0,2,'Shelter national producers from external competition. Guaranteed markets can support output while weakening productivity renewal.',[mod('industrial_capacity_factory',.08),mod('production_factory_efficiency_gain_factor',-.05),mod('foreign_influence_modifier',-.05)],['fn_state'],conditions=['FN identity'])
focus(g,'fn_export','A National Export Coalition',4,2,'Build an alliance of export firms and the nationalist state. International sales provide income but make the economy dependent on the markets it claims to resist.',[mod('corporate_tax_income_multiplier_modifier',.08),mod('foreign_influence_modifier',-.04),mod('stability_factor',-.03)],['fn_state'],conditions=['FN identity'])
choice('fn_protection','fn_export')
focus(g,'fn_defence','The Armed Nation',2,4,'Prioritise territorial mobilisation and a national armament base, accepting the cost of sustained preparation and a more militarised public life.',[mod('army_core_defence_factor',.08),mod('army_personnel_cost_multiplier_modifier',.08),mod('social_cost_multiplier_modifier',.03)],[('fn_protection','fn_export')],conditions=['FN identity'])

# Shared national investment is kept out of repeatable party programmes.
g=group('economy','Industry, Regions and Energy',18,8,context='Shared national assets and persistent reforms. No date barrier except technology, survey and real external crisis conditions.')
focus(g,'sixth_plan','Prepare the Sixth Plan',0,0,'Set national investment priorities for the coming decade. Planning must confront the different needs of modern exporters, older industrial districts and underserved regions.',[gdp(-.08),mod('country_productivity_growth_modifier',.03)],cost=5)
focus(g,'regional_links','Regional Connections',-7,2,'Connect underserved regions to ports and industrial markets. Transport investment gives smaller centres access to the national economy.',[gdp(-.30),asset(60,'infrastructure'),asset(61,'infrastructure')],['sixth_plan'])
focus(g,'technical_colleges','Technical Colleges',-2,2,'Expand routes into engineering and industrial skills beyond the elite schools, concentrating funding on the practical bottlenecks of modernisation.',[gdp(-.20),remove('education'),research('industry',.5,2),mod('production_factory_efficiency_gain_factor',.05),mod('education_cost_multiplier_modifier',.05)],['sixth_plan'])
focus(g,'mass_universities','Mass University Funding',2,2,'Fund the institutions created by the Faure reforms and widen access to advanced study. More open universities require a larger permanent education budget.',[gdp(-.25),remove('education'),mod('research_speed_factor',.05),mod('education_cost_multiplier_modifier',.12)],['sixth_plan'])
choice('technical_colleges','mass_universities')
focus(g,'champion_model','Concentrate Industrial Champions',-7,4,'Focus public capital on firms large enough to compete internationally. Faster output is purchased with fiscal exposure and continued regional concentration.',[gdp(-.35),asset(55,'industrial_complex'),mod('industrial_capacity_factory',.05),mod('bureaucracy_cost_multiplier_modifier',.04)],['regional_links'])
focus(g,'regional_industry','Regional Industrial Renewal',-3,4,'Back modern workshops and conversion projects in less favoured districts. A wider base sacrifices some concentration in flagship firms.',[gdp(-.35),asset(54,'industrial_complex'),mod('civilian_factories_productivity',.06),mod('social_cost_multiplier_modifier',.04)],['regional_links'])
choice('champion_model','regional_industry')
focus(g,'territorial_balance','A Broader Industrial Nation',-5,6,'Bring the chosen industrial strategy together with regional transport investment, reducing the inherited gap in access to modern production.',[remove('regions'),mod('production_speed_infrastructure_factor',.03)],[('champion_model','regional_industry')],cost=5)
focus(g,'plan_calcul','Renew Plan Calcul',0,4,'Support a French computing capability after the first Plan Calcul. Public procurement and research must overcome the scale of established foreign suppliers.',[gdp(-.25),research('electronics',.5,2),mod('bureaucracy_cost_multiplier_modifier',.03)],[('technical_colleges','mass_universities')])
focus(g,'national_computers','A National Computer Industry',-2,6,'Sustain a domestic systems producer through public demand. Technical autonomy requires a smaller market and continuing public support.',[gdp(-.15),mod('research_speed_factor',.03),mod('corporate_tax_income_multiplier_modifier',-.03)],['plan_calcul'])
focus(g,'open_computers','Compatible International Systems',2,6,'Adopt international standards and concentrate French engineering on competitive niches. Compatibility accelerates renewal while weakening a fully independent supply chain.',[mod('production_factory_efficiency_gain_factor',.06),mod('research_speed_factor',.02),mod('foreign_influence_modifier',-.03)],['plan_calcul'])
choice('national_computers','open_computers')
focus(g,'transport_choice','Transport for a New Decade',6,2,'Choose how to connect a rapidly urbanising country. National rail capacity and dispersed road access compete for the same public investment.',[gdp(-.06)],['sixth_plan'],cost=5)
focus(g,'tgv','The High-Speed Rail Programme',4,4,'Commit to the development and construction of high-speed rail. Concentrated corridors promise efficient movement at a substantial capital cost.',[gdp(-.40),asset(62,'infrastructure'),mod('energy_use_modifier_civs',-.04),mod('bureaucracy_cost_multiplier_modifier',.02)],['transport_choice'])
focus(g,'motorways','Motorways and Regional Access',8,4,'Expand the road network serving dispersed industry and smaller towns. Flexible access increases the economy reliance on motor fuel.',[gdp(-.30),asset(62,'infrastructure'),mod('production_speed_infrastructure_factor',.07),mod('energy_use_modifier_civs',.04)],['transport_choice'])
choice('tgv','motorways')
focus(g,'energy_review','A National Energy Review',7,6,'Review fuel dependence before an external crisis forces the issue. France must choose between capital-intensive generation and a wider portfolio of supply and demand measures.',[gdp(-.05),unlock('energy_audit','Energy contingency planning')],[('tgv','motorways')],cost=5)
focus(g,'nuclear_scale','An Accelerated Nuclear Programme',4,8,'Develop a standardised civil nuclear programme using real research and construction capacity. Strategic resilience comes with a heavy capital and operating commitment.',[gdp(-.50),research('nuclear',.5,2),unlock('fund_reactor','Fund the first approved reactor project'),mod('energy_use_modifier_civs',-.04),mod('bureaucracy_cost_multiplier_modifier',.04)],['energy_review'],conditions=['Actual civil nuclear technology and reactor construction capacity'])
focus(g,'diverse_energy','Diversified Supply and Conservation',10,8,'Combine efficient use with a more varied supply portfolio. Smaller commitments reduce concentration risk while leaving a larger role for imported energy.',[gdp(-.30),mod('energy_use_modifier_civs',-.06),mod('energy_gain_multiplier',.04),mod('civilian_factories_productivity',-.02)],['energy_review'])
choice('nuclear_scale','diverse_energy')
focus(g,'oil_resilience','Reduce Oil Dependence',7,10,'Complete the funded energy strategy and replace the inherited assumption of permanently cheap fuel. Actual power stations and fuel contracts remain separate national assets.',[remove('oil')],[('nuclear_scale','diverse_energy')],cost=5)
focus(g,'farm_policy','The Agricultural Settlement',-6,8,'Choose how to distribute the gains of agricultural modernisation between export-scale farms and the survival of smaller rural communities.',[gdp(-.05)],['territorial_balance'],cost=5)
focus(g,'export_farms','Export Agriculture',-8,10,'Back mechanisation and large-scale processing for European and world markets. Scale improves output while sharpening pressure on smaller holdings.',[gdp(-.18),mod('agricolture_productivity_modifier',.10),mod('stability_factor',-.03)],['farm_policy'])
focus(g,'rural_services','Rural Services and Family Farms',-4,10,'Support cooperative services and smaller farms, keeping rural communities viable despite a slower concentration of production.',[gdp(-.18),mod('agricolture_productivity_modifier',.05),mod('stability_factor',.04),mod('social_cost_multiplier_modifier',.04)],['farm_policy'])
choice('export_farms','rural_services')
focus(g,'telecoms','A National Telecommunications Network',0,8,'Expand reliable telephone and data services for firms, administrations and households. A modern network requires patient public capital.',[gdp(-.28),research('electronics'),mod('civilian_factories_productivity',.03)], [('national_computers','open_computers')])
focus(g,'conversion','Convert the Vulnerable Industrial Basins',0,10,'Prepare older coal, textile and steel districts for industrial change before closures become a national emergency.',[gdp(-.25),mod('production_factory_efficiency_gain_factor',.04),mod('social_cost_multiplier_modifier',.05)],['telecoms'])

g=group('defence','Independent Defence',62,8,context='Shared armed forces. Real platforms, nuclear stockpiles and technology are never awarded by a ceremonial focus.')
focus(g,'defence_review','The Defence White Paper',0,0,'Define the relationship between the national deterrent, conventional defence in Europe and commitments overseas.',[gdp(-.05),xp('army',20)],cost=5)
focus(g,'nuclear_priority','Priority to the Deterrent',-3,2,'Maintain a high priority for the independent deterrent and the engineering base behind it. Conventional procurement must absorb the pressure.',[remove('deterrent'),research('nuclear'),mod('war_support_factor',.06),mod('equipment_cost_multiplier_modifier',.08)],['defence_review'])
focus(g,'balanced_forces','A Balanced Conventional Force',3,2,'Retain the deterrent while moderating its priority in the defence programme, directing more effort toward deployable conventional forces.',[remove('deterrent'),mod('army_org_factor',.05),mod('equipment_cost_multiplier_modifier',.03),mod('war_support_factor',-.02)],['defence_review'])
choice('nuclear_priority','balanced_forces')
focus(g,'service_review','Reform National Service',0,4,'Choose the role of conscription in a force expected to defend Europe and operate beyond it.',[xp('army',15)],[('nuclear_priority','balanced_forces')],cost=5)
focus(g,'citizen_army','A Trained Citizen Army',-3,6,'Invest in reserves and useful training for conscripts. Broad territorial readiness requires a longer and more expensive training establishment.',[mod('army_core_defence_factor',.08),mod('land_reinforce_rate',.02),mod('training_time_army_factor',.08),mod('army_personnel_cost_multiplier_modifier',.04)],['service_review'])
focus(g,'professional_core','A Professional Intervention Core',3,6,'Build a smaller high-readiness core for demanding deployments. Experience and preparation come with a higher wage and support bill.',[mod('army_org_factor',.06),mod('army_org_regain',.05),mod('army_personnel_cost_multiplier_modifier',.10)],['service_review'])
choice('citizen_army','professional_core')
focus(g,'land_procurement','Armoured Procurement',-7,4,'Choose the industrial basis of future land equipment, balancing a national platform against the economies of cooperation.',[gdp(-.08),xp('army',15)],[('nuclear_priority','balanced_forces')],cost=5)
focus(g,'national_armour','AMX and National Design',-9,6,'Fund a continuing national armoured design capability. Domestic production retains expertise but carries a higher procurement cost.',[gdp(-.25),asset(55,'arms_factory'),research('armor',.75),mod('equipment_cost_multiplier_modifier',.03)],['land_procurement'])
focus(g,'pooled_armour','Pooled Land Procurement',-5,6,'Pursue common components and externally agreed procurement. Lower unit costs leave French influence dependent on partner consent.',[mod('equipment_cost_multiplier_modifier',-.05),mod('foreign_influence_modifier',-.04),unlock('pooled_land','Joint land-equipment talks')],['land_procurement'])
choice('national_armour','pooled_armour')
focus(g,'air_programme','The Combat Aircraft Programme',7,4,'French air power depends on continuing design, testing and production. A domestic priority and cooperative development offer different strengths.',[gdp(-.08),xp('air',20)],[('nuclear_priority','balanced_forces')],cost=5)
focus(g,'mirage','The Mirage Design Line',5,6,'Sustain the national combat-aircraft design line and its export potential without skipping the technologies required for a new aircraft.',[gdp(-.25),research('light_air',.75),mod('air_accidents_factor',-.05),mod('equipment_cost_multiplier_modifier',.03)],['air_programme'])
focus(g,'jaguar_doctrine','Cooperative Tactical Aviation',9,6,'Develop the training and procurement arrangements needed for cooperative tactical aircraft. Standardisation reduces cost at a price in autonomy.',[mod('air_training_xp_gain_factor',.08),mod('air_fuel_consumption_factor',-.05),mod('foreign_influence_modifier',-.03),unlock('jaguar_talks','Franco-British tactical aviation talks')],['air_programme'])
choice('mirage','jaguar_doctrine')
focus(g,'naval_review','A Navy for French Commitments',0,8,'Choose between sustained oceanic presence and concentration on escorts, approaches and sea-lane protection.',[gdp(-.08),xp('navy',20)],[('citizen_army','professional_core')],cost=5)
focus(g,'ocean_navy','An Ocean-Going Fleet',-3,10,'Maintain the dockyards and trained crews needed for an oceanic fleet. Presence overseas requires a larger permanent personnel establishment.',[gdp(-.30),asset(64,'dockyard'),mod('industrial_capacity_dockyard',.06),mod('navy_personnel_cost_multiplier_modifier',.08)],['naval_review'])
focus(g,'escort_navy','Escorts and Maritime Approaches',3,10,'Prioritise dependable escorts, maintenance and coastal protection. Concentration improves routine performance while narrowing distant commitments.',[gdp(-.18),mod('naval_accidents_chance',-.08),mod('industrial_capacity_dockyard',.04),mod('foreign_influence_modifier',-.03)],['naval_review'])
choice('ocean_navy','escort_navy')
focus(g,'logistics','Joint Logistics and Maintenance',-7,8,'Standardise support between the services so that readiness is sustained after deployment, with a larger permanent maintenance apparatus.',[gdp(-.12),mod('supply_consumption_factor',-.06),mod('bureaucracy_cost_multiplier_modifier',.04)],[('national_armour','pooled_armour')])
focus(g,'flight_schools','Modern Flight Schools',7,8,'Train instructors and improve flight safety before expanding operational demands on new aircraft.',[gdp(-.12),mod('air_accidents_factor',-.08),mod('airforce_personnel_cost_multiplier_modifier',.05)],[('mirage','jaguar_doctrine')])

g=group('diplomacy','Partnerships by Consent',104,8,context='Distinct French proposal focuses. Named recipients receive Accept and Decline decisions. All terms stay inspectable while locked.')
focus(g,'diplomatic_review','An Independent Voice',0,0,'France must choose where independence is best defended through national capacity and where negotiated partnerships offer a stronger result.',[pp(50)],cost=5)

offers=[]
def offer(key,title,x,y,partner,desc,fr,other,parents,setup_fr=.10,setup_other=.08,family=None,conditions=(),basis='Historical bilateral precedent; proposed RP renegotiation'):
    focus(g,key,title,x,y,desc,[unlock(key+'_response',partner+' acceptance or refusal')],parents,cost=7,conditions=conditions,basis=basis,lifetime='treaty')
    n=nodes[-1]
    n['offer']=dict(partner=partner,family=family or key,france=dict(spirit='COLDWAR_FRA2_'+key+'_france',name=title+': France',effects=[gdp(-setup_fr)]+fr),recipient=dict(spirit='COLDWAR_FRA2_'+key+'_'+partner,name=title+': '+partner,effects=[gdp(-setup_other)]+other))
    offers.append(key)

offer('airbus','The Airbus Partnership',-10,2,'GER','Renew the Franco-German A300 commitment as a joint civil aviation programme. Neither government obtains its partner resources without a new signed agreement.',[research('air_equipment',.5),mod('civilian_factories_productivity',.03),weekly(0.06)],[research('air_equipment',.5),mod('civilian_factories_productivity',.03),weekly(0.06)],['diplomatic_review'],family='civil_aerospace')
offer('concorde','Concorde and Supersonic Aviation',-6,2,'ENG','Deepen the Anglo-French supersonic programme. Prestige and advanced engineering compete with a costly and uncertain commercial future.',[research('air_equipment',.75),mod('research_speed_factor',.03),weekly(0.1)],[research('air_equipment',.75),mod('research_speed_factor',.03),weekly(0.1)],['diplomatic_review'],family='civil_aerospace')
choice('airbus','concorde')
offer('symphonie','The Symphonie Satellite Programme',-10,4,'GER','Use the Franco-German satellite project as the basis of a continuing telecommunications partnership.',[research('electronics',.5),mod('research_speed_factor',.01),weekly(0.04)],[research('electronics',.5),mod('research_speed_factor',.01),weekly(0.04)],[('airbus','concorde')],family='space')
offer('ariane','An Independent European Launcher',-6,4,'GER','Negotiate a French-led European launcher programme with a German partner. Shared engineering does not remove the high cost of independent access to space.',[research('electronics',.75),mod('foreign_influence_modifier',.04),weekly(0.08)],[research('electronics',.75),mod('foreign_influence_modifier',.02),weekly(0.06)],[('airbus','concorde')],family='space',basis='Later Ariane precedent; deliberately alternate Franco-German bilateral implementation.')
choice('symphonie','ariane')
offer('jaguar','The Jaguar Partnership',-2,2,'ENG','Renew cooperation in tactical aviation around the Jaguar precedent, combining common development with national operational requirements.',[research('light_air',.5),mod('air_training_xp_gain_factor',.04),weekly(0.04)],[research('light_air',.5),mod('air_training_xp_gain_factor',.04),weekly(0.04)],['diplomatic_review'],family='military_technology')
offer('atlantic_training','Atlantic Training and Logistics',2,2,'USA','Negotiate technical training and logistics cooperation while remaining outside NATO integrated command unless France separately chooses to rejoin it.',[mod('army_org_regain',.04),mod('air_training_xp_gain_factor',.04),mod('foreign_influence_modifier',-.02),weekly(0.04)],[mod('land_reinforce_rate',.01),mod('foreign_influence_modifier',.02),weekly(0.02)],['diplomatic_review'],family='military_technology',setup_fr=.08,setup_other=.06)
choice('jaguar','atlantic_training')
offer('soviet_science','Franco-Soviet Scientific Cooperation',-2,4,'SOV','Build on the 1966 cooperation framework and the developing dialogue with Moscow, concentrating on civilian science rather than an imposed military alignment.',[research('electronics',.5),mod('research_speed_factor',.01),weekly(0.04)],[research('electronics',.5),mod('research_speed_factor',.01),weekly(0.04)],[('jaguar','atlantic_training')],family='civil_science')
offer('us_science','An Atlantic Research Accord',2,4,'USA','Seek an alternative civilian research accord with American institutions. Both governments decide whether shared access justifies the funding and external commitments.',[research('electronics',.5),mod('production_factory_efficiency_gain_factor',.02),weekly(0.04)],[research('electronics',.5),mod('production_factory_efficiency_gain_factor',.02),weekly(0.04)],[('jaguar','atlantic_training')],family='civil_science',basis='Plausible alternate agreement, not a claim that this exact treaty was signed.')
choice('soviet_science','us_science')
offer('algeria_energy','Algerian Energy and Industrial Cooperation',6,2,'ALG','Renegotiate energy and industrial cooperation from the 1965 agreement on the basis of Algerian sovereignty and a mutually agreed development programme.',[mod('energy_gain_multiplier',.04),weekly(0.08)],[mod('civilian_factories_productivity',.04),mod('bureaucracy_cost_multiplier_modifier',.02),weekly(0.04)],['diplomatic_review'],setup_fr=.20,setup_other=.10,family='mediterranean_energy')
offer('iran_energy','A Diversified Iranian Supply',10,2,'PER','Negotiate a separate energy and technical agreement with Iran. A larger supply commitment offers an alternative to the deeper educational partnership proposed to Algeria.',[mod('energy_gain_multiplier',.06),mod('foreign_influence_modifier',-.02),weekly(0.07)],[mod('civilian_factories_productivity',.05),mod('bureaucracy_cost_multiplier_modifier',.02),weekly(0.03)],['diplomatic_review'],setup_fr=.20,setup_other=.10,family='mediterranean_energy',basis='Alternate supply diversification drawing on actual French energy and industrial interests.')
choice('algeria_energy','iran_energy')
offer('algeria_training','Algerian Technical Institutes',6,4,'ALG','Extend the Algerian Petroleum Institute assistance precedent into a continuing technical education partnership.',[mod('research_speed_factor',.01),weekly(0.06)],[mod('production_factory_efficiency_gain_factor',.04),mod('education_cost_multiplier_modifier',.03),weekly(0.02)],['algeria_energy'],setup_fr=.15,setup_other=.06,family='technical_education',conditions=['Both countries have the actual active Algerian Energy and Industrial Cooperation spirit'])
offer('senegal_civil','Civil Partnership with Senegal',10,4,'SEN','Offer a civilian partnership that gives Senegal a negotiated alternative to a relationship centred on French military presence.',[mod('foreign_influence_modifier',.04),weekly(0.06)],[mod('civilian_factories_productivity',.03),mod('education_cost_multiplier_modifier',.02),weekly(0.02)],[('algeria_energy','iran_energy')],setup_fr=.15,setup_other=.04,family='senegal',basis='Plausible renegotiated equal partnership, not a copy of an existing treaty.')
offer('senegal_defence','A Renewed Senegalese Defence Accord',10,6,'SEN','Renegotiate training and access on the basis of explicit Senegalese consent. The defence precedent creates a security option with continuing costs for both governments.',[mod('foreign_influence_modifier',.05),mod('supply_consumption_factor',-.02),weekly(0.06)],[mod('army_org_factor',.04),mod('army_personnel_cost_multiplier_modifier',.03),weekly(0.02)],[('algeria_energy','iran_energy')],setup_fr=.12,setup_other=.04,family='senegal')
choice('senegal_civil','senegal_defence')
offer('rhine','Franco-German Industrial Regions',-8,6,'GER','Link conversion and technical training in neighbouring industrial regions, sharing the cost of modernisation rather than assigning foreign construction unilaterally.',[gdp(-.15),asset(57,'industrial_complex'),mod('production_factory_efficiency_gain_factor',.02),weekly(0.04)],[gdp(-.15),mod('production_factory_efficiency_gain_factor',.04),weekly(0.04)],[('symphonie','ariane')],setup_fr=.10,setup_other=.10,family='regional_industry',basis='Plausible RP regional conversion agreement; asset state is in France, no foreign state guessed.')
offer('italy','Franco-Italian Industrial Cooperation',-4,6,'ITA','Offer Italy a joint machinery and industrial research programme. Both economies gain from specialisation while accepting a smaller national share of public contracts.',[research('industry',.5),mod('civilian_factories_productivity',.02),weekly(0.04)],[research('industry',.5),mod('civilian_factories_productivity',.02),weekly(0.04)],[('symphonie','ariane')],family='regional_industry',basis='Plausible alternate RP industrial partnership.')
choice('rhine','italy')
focus(g,'community_entry','The Hague and the Communities',0,6,'Work through the European Communities to shape enlargement and cooperation. Membership rights and the interests of other RP governments remain part of the existing institutions.',[unlock('community_negotiations','Community enlargement and institutional negotiations')],[('soviet_science','us_science')],cost=5,conditions=['Actual active European Communities membership spirit'])

from gaullist_nato import append_nato
nato_design=append_nato(globals())

design=dict(project='IMPERIA COLD WAR',revision='FRA2 concept 1.2: GDP funding and differentiated rewards',status='UNAPPROVED CONCEPT. No replacement focus tree installed.',
date='2026-10-28',start='1970-01-01',horizon='1970-1990',groups=groups,nodes=nodes,starting_spirits=spirits,
rules=dict(party_visibility='All branches always visible; exact native ruling-party requirements gate execution and programme activation.',
party_lifecycle='Earned party modifier deltas detach when the party leaves and return on re-entry. Monetary transactions, assets, XP and research never replay. Shared institutions and national assets persist.',
offers='A French focus sends a fixed-partner recipient-owned Accept/Decline decision. No benefit before acceptance. Both signatories pay once on acceptance. Seven proposal days per focus cost unit.',
treaty_lifecycle='Signed agreements have no expiry. Both countries must exist, remain at peace with one another, and impose neither native embargo nor any diplomatic, financial, economic or military Imperia sanction in either direction. Suspend both spirits and their running streams while invalid; restore both without repeating setup or finite awards. Actual active parent spirits are required for dependent agreements.',
family_limit='One signed agreement per named family. An exclusive focus choice remains a sovereign French policy choice even after refusal; a recipient can always decline. Reissues preserve the fixed partner and require fresh consent.',
weekly='Standing programme budgets are annual percentages of each payer own current gdp_total, divided by 52 and recalculated in the native weekly expense stream. Store share literals with at most five fractional digits and divide by integer 52. Expense multipliers change the corresponding existing weekly bill. All percentages are game-balance proposals, not reconstructed historical budgets.',
assets='One extra shared slot per building level in the same state, before construction, under a single one-time guard. Actual ownership, control and native capacity checked separately. No automatic uranium production or free technology.',
politics='Succession and elections remain native. No automatic coup, forced recipient government, annexation or treaty acceptance. CIR/CDP representation needs historical registry refinement before implementation.',
preview='External concept using native art; routing/font/frames are approximations. This is not a running-game screenshot.'),
history_source='history_research.md',md_source='md_layout_reference.md',mechanics_source='verified_effects.json')
design['nato']=nato_design
design['rules']['treasury']='Every one-time Treasury charge is a signed percentage of the payer own current annual gdp_total at the actual payment. Bilateral signatories use separate GDP bases in their own country scopes. The percentage is agreed; the amount updates with GDP. Previews never execute costs. No Treasury-balance availability or delivery gate is added. GDP availability is an internal initialisation guard, never a fixed-price fallback.'
design['rules']['nato_lifecycle']='NATO-specific agreements additionally require NATO_member on both signatories. Losing membership suspends both spirits and weekly streams while preserving signatures; return restores them without setup, XP or research replay. Membership itself is never restored by this subsystem. Government-bound NATO programme modifiers require current UDR rule, NATO_member and any actual active parent agreement. Signed bilateral treaties do not require UDR to remain in government.'
design['decisions']=[
 dict(id='COLDWAR_FRA2_energy_audit',title='Energy Contingency Planning',conditions=['Energy Review completed','Once only'],effects=[gdp(-.06),pp(-40),mod('energy_use_modifier_civs',-.03)],days=730),
 dict(id='COLDWAR_FRA2_fund_reactor',title='Fund the First Approved Reactor Project',conditions=['Accelerated Nuclear Programme completed','Actual reactor construction technology','Own and control Loire (59)','Native reactor and shared-slot capacity','Once only'],effects=[gdp(-1.00),asset(59,'nuclear_reactor')],days=None),
 dict(id='COLDWAR_FRA2_community_negotiations',title='Community Enlargement and Institutional Negotiations',conditions=['has_idea = EU_member','Uses existing native Community voting and admission decisions; no unilateral membership award'],effects=[pp(-50),mod('foreign_influence_modifier',.04),mod('political_power_factor',-.02)],days=730)
]

from reward_revision import revise_rewards
revise_rewards(globals(),design)

known={n['key']:n for n in nodes}
country_names={'GER':'Federal Republic of Germany','ENG':'United Kingdom','USA':'United States','SOV':'Soviet Union','ALG':'Algeria','PER':'Iran','SEN':'Senegal','ITA':'Italy'}
# Keep the strongest compatible political route below the original stability ceiling.
stability_revision={'new_society':.04,'ortf':.02,'participation':.03,'advanced_democracy':.02,'democratic_road':.04,'municipal_socialism':.02,'workers_control':.03,'independent_communism':.02,'communist_settlement':.02}
for n in nodes:
    if n['key'] in stability_revision:
        for e in n['effects']:
            if e['kind']=='modifier' and e['key']=='stability_factor':
                e['value']=stability_revision[n['key']]
for n in nodes:
    for p in [p for group in n['prerequisites'] for p in group]+n['exclusions']:
        assert p in known,(n['key'],p)
    anchor=next((q for q in nodes if q['group']==n['group']),None)
    n['anchor']=None if n is anchor else anchor['id']
    n['offset']=[n['x']-(anchor['x'] if n is not anchor else 0),n['y']-(anchor['y'] if n is not anchor else 0)]
    if n['key'] in ('pompidou_europe','federal_europe','community_entry','europe_restraint'):
        n['conditions'].append('has_idea = EU_member')
    if n['key']=='community_entry':
        n['conditions']=[c for c in n['conditions'] if c!='Actual active European Communities membership spirit']
        n['prerequisites']=[['diplomatic_review']]
    if n['key']=='senegal_civil':
        n['prerequisites']=[['diplomatic_review']]
    if n['key']=='senegal_defence':
        n['prerequisites']=[['diplomatic_review']]
        n['x']=118
        n['y']=10
        n['offset']=[14,2]
    # Policy orientations do not create a second sender-side foreign offer menu.
    if n['key'] in ('pompidou_europe','atlantic_liberal','federal_europe','soviet_friendship','pooled_armour','jaguar_doctrine'):
        n['effects']=[e for e in n['effects'] if e['kind']!='unlock_decision']
    if n['key']=='jaguar_doctrine':
        n['conditions'].append('has_idea = COLDWAR_FRA2_jaguar_france')
    if n['key']=='soviet_friendship':
        n['conditions'].append('has_idea = COLDWAR_FRA2_soviet_science_france')
    n['spirit_name']=next(g['title'] for g in groups if g['id']==n['group'])+' Programme'
    if 'offer' in n:
        n['offer']['partner_name']=country_names[n['offer']['partner']]
        n['offer']['recipient']['name']=n['title']+': '+n['offer']['partner_name']
        n['effects'][0]['label']=n['offer']['partner_name']+': acceptance or refusal'

# Short native title-field labels preserve the full policy title and description.
short_path=OUT/'short_titles.json'
if short_path.exists():
    shorts=json.loads(short_path.read_text(encoding='utf-8'))['short_titles']
    revisions={'housing':'Housing and Rights','participation':'Gaullist Participation','debre':'Strategic Sovereignty','pompidou_europe':'The Hague Opening','mutuals':'Social Insurance','competitiveness_ps':'Investment Compact','cid_tax':"Traders' Tax Revolt",'oil_resilience':'Cut Oil Dependence','naval_review':'Naval Commitments','pooled_armour':'Shared Components'}
    for n in nodes:
        n['full_title']=n['title']
        if n['key'] in shorts:
            n['title']=revisions.get(n['key'],shorts[n['key']]['recommended'])
    for s in spirits:
        for n in nodes:
            s['remedy']=s['remedy'].replace(n['full_title'],n['title'])

design['navigation']={'initial_focus':'COLDWAR_FRA2_nato_review','initial_government':'udr','preview_section':'udr_nato','shortcuts':[{'name':g['title'],'focus':next(n['id'] for n in nodes if n['group']==g['id'])} for g in groups],'continuous_focus_position':{'x':4*96,'y':16*130},'grid_stride':[96,130],'focus_item':[165,128]}

for n in nodes:
    n['reward_guards']=list(n['conditions'])
    if n.get('offer'):
        n['offer']['payment_contract']='French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.'
        n['offer']['france']['payer']='FRA'
        n['offer']['recipient']['payer']=n['offer']['partner']
        n['offer']['acceptance_conditions']=list(n['conditions'])+['Named recipient chooses Accept','Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes','The proposal and one-time transaction are still valid','Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available']
        n['offer']['acceptance_transaction']='Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.'
        if n['key']=='algeria_training':
            n['offer']['activation_conditions']=['FRA = { has_idea = COLDWAR_FRA2_algeria_energy_france }','ALG = { has_idea = COLDWAR_FRA2_algeria_energy_ALG }']

(OUT/'concept.json').write_text(json.dumps(design,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(nodes)} focuses, {len(groups)} sections, {sum(len(n["exclusions"]) for n in nodes)//2} exclusive pairs, {len(offers)} recipient-approved offers, {len(spirits)} starting spirits')
