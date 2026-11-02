# IMPERIA COLD WAR — Brazil 1970 approval concept, structured content only.
"""Design data. Importing this module never writes loaded game files."""
P='COLDWAR_BRA_'
GROUPS=[]; NODES=[]; DECISIONS=[]; EVENTS=[]
TRIGGERS={1:'western_conservatism_are_in_power',2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',4:'emerging_communist_state_are_in_power',19:'neutrality_neutral_communism_are_in_power',20:'nationalist_right_wing_populists_are_in_power',22:'nationalist_military_junta_are_in_power'}
def M(key,value):return dict(kind='modifier',key=key,value=value)
def C(p):return dict(kind='treasury_gdp',percent=-p)
def W(p):return dict(kind='weekly_gdp_expense',annual_gdp_percent=p,divisor=52)
def B(state,building,amount=1,instant=True):return dict(kind='building',state=state,building=building,amount=amount,slots=amount,instant=instant)
def R(cat,bonus=.5,uses=1):return dict(kind='research',category=cat,bonus=bonus,uses=uses)
def X(service,amount=25):return dict(kind='experience',service=service,amount=amount)
def F(faction,value):
    # Desired applied change. The native helper doubles positive autocrat inputs.
    # A later compiler halves the caller input under that real native condition.
    faction='landowners' if faction=='farmers' else faction
    return dict(kind='faction_opinion',faction=faction,value=value,if_idea=faction,native_input_policy='Target signed delta; halve positive temp_opinion when the native autocrat helper doubles it')
def S(spirit):return dict(kind='remove_spirit',spirit=P+spirit)
def U(key,title,effects,conditions=None):
    DECISIONS.append(dict(id=P+key,title=title,effects=effects,conditions=conditions or [],once=True))
    return dict(kind='unlock_decision',id=P+key,label=title)
def E(key,title,options,context):
    EVENTS.append(dict(id=P+key,title=title,options=options,description=context,art_status='Native framed photograph to be selected after approval; no image installed.'))
    return dict(kind='event',id=P+key,label=title)
def G(key,title,x,y,slot=None,identity=None,context=''):
    GROUPS.append(dict(id=key,title=title,x=x,y=y,slot=slot,identity=identity,context=context))
def N(group,key,title,dx,y,parents=(),effects=(),description='',conditions=(),days=35,basis='Historical policy theme; numerical values are balance proposals.',lifetime=None):
    g=next(g for g in GROUPS if g['id']==group)
    ps=[list(p) if not isinstance(p,str) else [p] for p in parents]
    cond=list(conditions)
    if g['slot'] is not None:
        cond.insert(0,TRIGGERS[g['slot']]+' = yes')
        if g['identity']:cond.insert(1,'Governing party identity: '+g['identity'])
    n=dict(key=key,id=P+key,title=title,group=group,x=g['x']+dx,y=g['y']+y,days=days,cost=days/7,prerequisites=ps,exclusions=[],conditions=cond,effects=list(effects),description=description,basis=basis,lifetime=lifetime or ('government' if g['slot'] is not None else 'national'),spirit_name=title,anchor=None,offset=None)
    local=[a for a in NODES if a['group']==group]
    if local:n['anchor']=local[0]['id'];n['offset']=[n['x']-local[0]['x'],n['y']-local[0]['y']]
    NODES.append(n);return key
def EX(*keys):
    for n in NODES:
        if n['key'] in keys:n['exclusions']+= [k for k in keys if k!=n['key']]
def route(key,title,x,slot,identity,rows,context):
    """Ten-focus programme with two genuine choices, OR joins and one AND join."""
    G(key,title,x,0,slot,identity,context)
    pos=[(0,0),(-2,1),(2,1),(0,2),(-2,3),(2,3),(0,4),(-2,5),(2,5),(0,6)]
    for i,(name,effects,desc) in enumerate(rows):
        parents=[[],[0],[0],[(1,2)],[3],[3],[4,5],[6],[6],[(7,8)]][i]
        pp=[tuple(key+'_'+str(j) for j in p) if isinstance(p,tuple) else key+'_'+str(p) for p in parents]
        N(key,key+'_'+str(i),name,*pos[i],pp,effects,desc)
    EX(key+'_1',key+'_2');EX(key+'_7',key+'_8')

# Political identities are separate even when their MD outlook slot is shared.
# Later identities are explicitly proposed registry work, never assumed live.
route('military','Armed Forces',4,22,'Brazilian Armed Forces',[
('Security Cabinet',[M('political_power_factor',.08),M('bureaucracy_cost_multiplier_modifier',.04)],'Coordinate the presidency, service ministries and national security apparatus under the existing military government.'),
('Retain AI-5',[M('political_power_factor',.12),M('stability_factor',-.05),F('the_military',8)],'Preserve exceptional executive powers and the security services, at the cost of consent and civil liberties.'),
('Controlled Opening',[C(.15),S('ai5'),M('political_power_factor',-.08),M('stability_factor',.05),F('the_military',-8)],'Begin an explicitly alternative early opening, or follow the later Geisel precedent, while containing resistance inside the armed forces.'),
('Presidential Compact',[E('officer_council','The Officer Council',[dict(title='Protect the command hierarchy',effects=[M('army_org_factor',.04),M('political_power_factor',-.04)]),dict(title='Bring civilian specialists into cabinet',effects=[M('research_speed_factor',.03),M('bureaucracy_cost_multiplier_modifier',.04)])],'The services dispute the balance between command authority and specialist administration.')],'Negotiate the composition of the governing coalition without replacing the existing succession system.'),
('Staff Colleges',[C(.3),R('CAT_electronics'),X('army')],'Fund communications, logistics and professional staff instruction.'),
('Defence Engineers',[C(.65),B(884,'arms_factory'),M('equipment_cost_multiplier_modifier',.03)],'Expand a domestic engineering base while accepting the cost of maintaining small production runs.'),
('Service Coordination',[M('army_org_factor',.04),M('military_spending_cost_multiplier_modifier',.04)],'Improve coordination across services while retaining their institutional budgets.'),
('National Champions',[M('industrial_capacity_factory',.07),M('interest_rate_multiplier_modifier',.5),W(.12)],'Concentrate credit in strategic national firms and accept contingent fiscal exposure.'),
('Procurement Discipline',[M('equipment_cost_multiplier_modifier',-.08),M('industrial_capacity_factory',-.03)],'Standardise procurement and end prestige orders at the expense of some domestic production.'),
('A Defined Mandate',[M('army_org_factor',.03),M('political_power_factor',-.04),U('service_mission','Review the Service Mission',[C(.2),X('army',30)],['Military government'])],'Give the service leadership a defined national mission whose programme ends when military rule ends.')
], 'Médici governs in slot 22. The civilian ARENA and the technocratic coalition are separate institutions.')
route('arena','ARENA / PDS',16,1,'ARENA; PDS after its real reorganisation',[
('Governors Compact',[M('political_power_factor',.07),M('bureaucracy_cost_multiplier_modifier',.04)],'Bind state governors and the congressional government bloc through a civilian conservative programme.'),
('Municipal Patronage',[M('stability_factor',.06),M('bureaucracy_cost_multiplier_modifier',.1)],'Use municipal networks to distribute investment and hold the governing coalition together.'),
('Technical Appointments',[M('bureaucracy_cost_multiplier_modifier',-.08),M('political_power_factor',-.07)],'Select administrators for technical competence, weakening the patronage bargain.'),
('Development Caucus',[C(.25),R('CAT_industry')],'Build legislative support for a funded development programme.'),
('Interior Industry',[C(.65),B(884,'industrial_complex')],'Locate a new industrial plant away from the coastal administrative centres.'),
('Farm Credit',[C(.4),M('agricolture_productivity_modifier',.05),F('farmers',8)],'Offer agricultural credit through established rural institutions.'),
('Federal Bargaining',[M('production_speed_buildings_factor',.04),M('bureaucracy_cost_multiplier_modifier',.03)],'Coordinate federal and state investment while accepting a slower bargain over allocations.'),
('Protected Suppliers',[M('industrial_capacity_factory',.07),M('research_speed_factor',-.03)],'Reserve procurement for national suppliers, protecting output but narrowing technological competition.'),
('Export Constituency',[M('resource_export_multiplier_modifier',.1),M('stability_factor',-.03)],'Shift the coalition toward competitive exporters while exposing sheltered domestic interests.'),
('Civilian Conservatism',[M('stability_factor',.04),M('political_power_factor',-.03)],'Build a conservative civilian government rather than treating ARENA as a synonym for the military command.')
], 'ARENA already exists in slot 1. PDS is a later institutional successor, not a free military programme.')
route('mdb','MDB / PMDB',28,2,'MDB; PMDB after its real reorganisation',[
('Congressional Renewal',[C(.15),M('stability_factor',.04),M('political_power_factor',-.04)],'Rebuild parliamentary oversight and a broad civilian government. Governing before the historical transition is alternative history.'),
('Negotiated Amnesty',[C(.2),M('stability_factor',.07),F('the_military',4),M('political_power_factor',-.05)],'Seek a negotiated transition and amnesty, accepting limits on accountability.'),
('Judicial Accountability',[C(.3),M('bureaucracy_cost_multiplier_modifier',.06),F('the_military',-10),M('research_speed_factor',.03)],'Restore judicial independence and investigate state coercion despite military resistance.'),
('Constituent Mandate',[C(.3),S('ai5'),E('constitution','The Constitutional Settlement',[dict(title='Strengthen social guarantees',effects=[M('stability_factor',.06),M('social_cost_multiplier_modifier',.06)]),dict(title='Prioritise governability',effects=[M('political_power_factor',.07),M('stability_factor',-.03)])],'A constituent coalition must settle the balance between social guarantees and executive authority.')],'Give the civilian transition a constitutional framework with competing institutional priorities.'),
('Municipal Autonomy',[C(.35),B(888,'offices')],'Equip elected municipal administrations to manage public services.'),
('Public Accounts',[C(.2),M('bureaucracy_cost_multiplier_modifier',-.04)],'Create professional auditing capacity for public contracts.'),
('Federal Guarantees',[M('stability_factor',.05),M('political_power_factor',-.05)],'Distribute authority across federal institutions and accept the cost of coalition bargaining.'),
('Social Covenant',[M('stability_factor',.06),M('social_cost_multiplier_modifier',.08),F('labour_unions',8)],'Expand social rights through a broad parliamentary compromise.'),
('Fiscal Covenant',[M('interest_rate_multiplier_modifier',-.5),M('production_speed_buildings_factor',-.04),F('labour_unions',-5)],'Constrain unfunded commitments to improve financing conditions.'),
('Civilian Republic',[M('stability_factor',.04),M('political_power_factor',-.03)],'Consolidate civilian institutions without assuming that every later PMDB government follows the same economic course.')
], 'The MDB is the legal opposition in 1970. A governing programme requires its actual accession to government.')
route('ptb','PTB Labourism',40,3,'Old PTB restoration, or separately registered later PTB',[
('Labour Guarantees',[C(.2),M('stability_factor',.04),M('social_cost_multiplier_modifier',.04)],'Rebuild the labour-rights tradition while distinguishing the exiled old PTB from Ivete Vargas’s later party.'),
('Union Mediation',[F('labour_unions',12),M('industrial_capacity_factory',.04),M('bureaucracy_cost_multiplier_modifier',.06)],'Use negotiated corporatist mediation to stabilise industrial relations.'),
('Independent Unions',[F('labour_unions',15),M('stability_factor',.05),M('political_power_factor',-.06)],'Give organised labour greater independence from executive patronage.'),
('Workplace Insurance',[C(.25),M('social_cost_multiplier_modifier',.05),M('stability_factor',.04)],'Extend workplace protection with a visible ongoing social budget.'),
('Industrial Apprentices',[C(.25),R('CAT_industry')],'Fund vocational apprenticeships in established industrial districts.'),
('Labour Courts',[C(.2),M('bureaucracy_cost_multiplier_modifier',.04),M('stability_factor',.03)],'Improve access to labour courts and fund the additional administrative burden.'),
('Wage Settlement',[S('wage_squeeze'),M('consumer_goods_factor',.02)],'End the initial wage squeeze through an institutional settlement.'),
('State Enterprises',[M('industrial_capacity_factory',.06),W(.12)],'Use public firms as employers and investment anchors.'),
('Small Employers',[M('corporate_tax_income_multiplier_modifier',-.05),M('stability_factor',.05)],'Support smaller employers through tax relief and negotiated labour obligations.'),
('Labour Republic',[M('stability_factor',.04),M('political_power_factor',-.03)],'Maintain a distinct labourist programme whose recurring privileges follow the actual government.')
], 'A restored pre-1965 PTB is an alternate route. The 1980 PTB and PDT naming dispute is a real later formation event.')
route('pdt','PDT',52,3,'PDT, formation and separate identity required',[
('Democratic Labourism',[C(.2),M('stability_factor',.05),M('political_power_factor',-.04)],'Build Brizola’s democratic labourist alternative with education and national development at its centre.'),
('Full-Time Schools',[C(.6),M('literacy_rate_education_modifier',.08),M('education_cost_multiplier_modifier',.1)],'Use the CIEP precedent for full-time schooling, with a substantial operating commitment.'),
('Technical Colleges',[C(.45),M('research_speed_factor',.05),M('education_cost_multiplier_modifier',.06)],'Prioritise technical and industrial education over the broader full-time school model.'),
('Teachers Compact',[W(.1),M('stability_factor',.03)],'Secure teachers and local administrators for a sustained education programme.'),
('Public Engineering',[C(.6),B(883,'offices')],'Build a public engineering and planning office in Rio de Janeiro.'),
('Neighbourhood Services',[C(.45),B(879,'infrastructure')],'Extend basic urban networks in Rio Grande do Sul.'),
('Mass Education',[S('skills'),M('education_cost_multiplier_modifier',.03)],'Broaden access to education and remove the initial technical-research bottleneck.'),
('National Ownership',[M('industrial_capacity_factory',.06),M('research_speed_factor',-.025)],'Retain strategic ownership while accepting narrower foreign technology access.'),
('Licensed Development',[R('CAT_industry',.5,2),W(.1),M('foreign_influence_defense_modifier',-.05)],'Acquire licences for national development with a continuing foreign technology relationship.'),
('A National School',[M('literacy_rate_education_modifier',.04),M('bureaucracy_cost_multiplier_modifier',.03)],'Anchor a durable education tradition in a government-bound operating programme.')
], 'PDT forms in 1980 after the dispute over the PTB name. Its own governing identity is not yet installed.')
route('pt','Workers Party',64,3,'PT, formation and separate identity required',[
('Workers Government',[C(.2),F('labour_unions',10),M('political_power_factor',-.04)],'Bring the new union movement and popular organisations into government without importing later Lula-era programmes.'),
('Workers Councils',[M('stability_factor',.07),M('production_factory_efficiency_gain_factor',-.05)],'Give workplace councils authority and accept the coordination costs of negotiated production.'),
('Productive Pact',[M('industrial_capacity_factory',.07),M('stability_factor',-.035)],'Trade workplace autonomy for a negotiated national investment and output agreement.'),
('Union Independence',[C(.2),S('wage_squeeze'),M('consumer_goods_factor',.025)],'Replace wage compression with free collective bargaining.'),
('Urban Health',[C(.5),B(882,'offices'),W(.08)],'Create administrative capacity for universal urban healthcare, using offices rather than an invented hospital building.'),
('Popular Budgeting',[C(.25),M('bureaucracy_cost_multiplier_modifier',.05),M('stability_factor',.04)],'Use the later Porto Alegre participatory-budget precedent for a distinct governing alternative.'),
('Rights in Practice',[M('stability_factor',.04),M('social_cost_multiplier_modifier',.05)],'Fund the institutions required to turn social guarantees into services.'),
('Cooperative Land',[C(.45),M('agricolture_productivity_modifier',.06),F('farmers',-6),W(.08)],'Finance cooperative farming and redistribution while managing conflict with established landowners.'),
('Family Farm Credit',[C(.35),M('agricolture_productivity_modifier',.04),F('farmers',6),M('bureaucracy_cost_multiplier_modifier',.04)],'Expand family-farm credit and extension without a general expropriation programme.'),
('Popular Democracy',[M('stability_factor',.05),M('political_power_factor',-.06)],'Sustain a participatory democratic government whose active policy package ends with its tenure.')
], 'PT is a new party formed in 1980, rooted in the ABC labour movement. Governing in this era is a plausible electoral alternative, not historical fact.')
route('pfl','Liberal Front',76,1,'PFL, formation and separate identity required',[
('Liberal Coalition',[M('political_power_factor',.06),M('bureaucracy_cost_multiplier_modifier',.035)],'Build a conservative civilian coalition from the Liberal Front split, with its own regional and business interests.'),
('Regional Investment',[C(.7),B(887,'industrial_complex'),M('bureaucracy_cost_multiplier_modifier',.04)],'Direct development investment toward the Northeast through regional political bargains.'),
('National Competition',[M('industrial_capacity_factory',.06),M('stability_factor',-.03)],'Expose protected firms to national competition, accepting regional industrial disruption.'),
('Civil Service Review',[C(.2),M('bureaucracy_cost_multiplier_modifier',-.04)],'Professionalise appointments while retaining a parliamentary governing bargain.'),
('Port Services',[C(.4),B(888,'offices')],'Improve commercial and logistics administration in Pernambuco.'),
('Small Business',[M('corporate_tax_income_multiplier_modifier',-.04),M('country_productivity_growth_modifier',.03)],'Reduce the tax burden on firms while sacrificing immediate revenue.'),
('Civilian Coalition',[M('stability_factor',.03),M('political_power_factor',-.03)],'Consolidate an elected civilian centre-right coalition.'),
('Social Partnership',[M('stability_factor',.05),M('social_cost_multiplier_modifier',.06)],'Preserve a social compromise alongside market-oriented development.'),
('Budget Credibility',[M('interest_rate_multiplier_modifier',-.45),M('production_speed_buildings_factor',-.03)],'Limit development credit and improve the government’s financing position.'),
('Liberal Institutions',[M('country_productivity_growth_modifier',.025),M('political_power_factor',-.03)],'Support gradual institutional modernisation rather than reducing liberalism to a single tax bonus.')
], 'PFL emerges in 1985 from PDS dissidents. It is not simply the entire ARENA renamed.')
route('psdb','PSDB',88,2,'PSDB, formation and separate identity required',[
('Social Democracy',[C(.2),M('research_speed_factor',.03),M('bureaucracy_cost_multiplier_modifier',.03)],'Build the 1988 PSDB alternative around democratic institutions, public services and economic modernisation.'),
('Monetary Restraint',[M('inflation_gain_multiplier_modifier',-.1),M('production_speed_buildings_factor',-.05)],'Restrain credit and demand to contain inflation, slowing investment.'),
('Investment Compact',[M('production_speed_buildings_factor',.07),M('inflation_gain_multiplier_modifier',.08)],'Protect productive investment while accepting a more difficult inflation problem.'),
('Professional Treasury',[C(.25),M('interest_rate_multiplier_modifier',-.35)],'Fund professional debt management without granting a free debt cancellation.'),
('Research Networks',[C(.45),R('CAT_electronics',.5,2)],'Connect universities and industrial research through a period-appropriate technology programme.'),
('Public Evaluation',[C(.2),M('education_cost_multiplier_modifier',-.04)],'Use service evaluation and administrative reform to improve education spending efficiency.'),
('Social Guarantees',[W(.08),M('stability_factor',.04)],'Maintain a social budget alongside macroeconomic reform.'),
('Competitive Industry',[M('production_factory_efficiency_gain_factor',.08),M('stability_factor',-.03)],'Use competition to accelerate productivity while accepting firm closures and industrial conflict.'),
('Managed Conversion',[M('industrial_capacity_factory',.04),W(.12)],'Finance a slower industrial transition with explicit public support.'),
('Democratic Modernity',[M('research_speed_factor',.025),M('political_power_factor',-.03)],'Consolidate a late-Cold-War reform programme without importing the 1994 Real Plan.')
], 'PSDB forms in 1988. Its economic branches are period alternatives, not an automatic Real Plan or presidential victory.')
route('pcb','PCB',100,4,'Brazilian Communist Party',[
('Communist Coalition',[C(.2),M('political_power_factor',.06),M('foreign_influence_defense_modifier',-.04)],'Give the PCB a distinct governing alternative rooted in its organisation and Soviet relationship.'),
('Pluralist Transition',[M('stability_factor',.06),M('political_power_factor',-.06)],'Pursue a broad democratic transition while sharing authority with other left parties.'),
('Cadre Direction',[M('industrial_capacity_factory',.07),M('stability_factor',-.045)],'Concentrate authority in party cadres to direct industrial targets.'),
('Planning Institutes',[C(.4),B(883,'offices')],'Build planning expertise as a real administrative asset.'),
('Strategic Production',[C(.6),B(884,'industrial_complex')],'Expand basic industrial production through public investment.'),
('Technical Exchange',[C(.2),R('CAT_industry')],'Fund a technical exchange without assuming a foreign player’s agreement.'),
('Public Ownership',[M('production_factory_max_efficiency_factor',.05),W(.1)],'Support long production runs through public firms and a recurring capital programme.'),
('National Communism',[M('foreign_influence_defense_modifier',.08),M('research_speed_factor',-.025)],'Retain independent direction at the cost of access to some foreign technical networks.'),
('International Links',[M('research_speed_factor',.05),M('foreign_influence_defense_modifier',-.07)],'Use external communist networks while accepting political dependence. A treaty still requires recipient consent.'),
('A Socialist Mandate',[M('stability_factor',.04),M('bureaucracy_cost_multiplier_modifier',.04)],'Sustain a distinct PCB programme, separate from the PCdoB’s rural revolutionary strategy.')
], 'PCB is clandestine in 1970 and later regains legality. A governing path requires genuine legalisation or an explicitly alternate accession.')
route('pcdob','PCdoB',112,19,'Communist Party of Brazil',[
('Rural Revolution',[C(.2),M('political_power_factor',.06),M('stability_factor',-.04)],'Develop a distinct alternate governing programme from the PCdoB’s rural revolutionary tradition.'),
('Peasant Cooperatives',[M('agricolture_productivity_modifier',.07),W(.12),F('farmers',-8)],'Pool equipment and extension services while confronting landholding interests.'),
('Village Land Titles',[M('stability_factor',.07),M('agricolture_productivity_modifier',.035),M('bureaucracy_cost_multiplier_modifier',.06)],'Prioritise secure household titles and local consent over collective ownership.'),
('Rural Administration',[C(.4),B(891,'offices')],'Create a civil administration in Pará instead of treating guerrilla experience as a free army.'),
('Village Instruction',[C(.3),M('literacy_rate_education_modifier',.06),M('education_cost_multiplier_modifier',.06)],'Expand rural instruction under a funded education programme.'),
('Local Workshops',[C(.55),B(888,'industrial_complex')],'Build a regional civilian workshop complex for agricultural and basic industrial tools.'),
('Agrarian Settlement',[S('land_inequality'),M('bureaucracy_cost_multiplier_modifier',.04)],'Replace the initial land inequality burden through a costly agrarian settlement.'),
('People’s Defence',[M('army_infantry_attack_factor',.06),M('army_personnel_cost_multiplier_modifier',.08)],'Develop infantry-oriented territorial defence with a larger personnel bill.'),
('Civil Reconstruction',[M('production_speed_buildings_factor',.06),M('army_org_factor',-.04)],'Prioritise reconstruction while reducing military institutional weight.'),
('A Rural Republic',[M('stability_factor',.04),M('political_power_factor',-.04)],'Turn a revolutionary organisation into an administration whose institutions carry genuine costs.')
], 'The Araguaia campaign is a historical tragedy, not a guaranteed successful revolution. Governing is explicit alternative history.')
route('populist','Lacerdists',124,20,'Lacerdists',[
('Public Probity',[C(.2),M('bureaucracy_cost_multiplier_modifier',-.04),M('political_power_factor',-.03)],'Develop Lacerda’s electoral and anti-corruption alternative while he or a separately registered Lacerdist successor actually governs.'),
('Independent Auditors',[M('bureaucracy_cost_multiplier_modifier',-.06),M('political_power_factor',-.05)],'Give auditors institutional independence at the expense of executive discretion.'),
('Presidential Campaign',[M('political_power_factor',.1),M('stability_factor',-.04)],'Mobilise a personal presidential mandate with greater polarisation.'),
('Administrative Reform',[C(.3),M('country_productivity_growth_modifier',.03)],'Reform purchasing and appointments through functioning administrative institutions.'),
('Competitive Imports',[M('research_speed_factor',.04),M('industrial_capacity_factory',-.04)],'Open access to imported machinery while exposing domestic manufacturers.'),
('Urban Management',[C(.4),B(883,'infrastructure')],'Invest in practical urban transport and basic networks.'),
('Electoral Government',[M('stability_factor',.04),M('political_power_factor',-.03)],'Restore an electoral mandate without imposing a specific presidential winner.'),
('Rapid Competition',[M('production_factory_efficiency_gain_factor',.1),M('stability_factor',-.07)],'Choose a sharp competitive adjustment. This does not implement the later Collor deposit freeze.'),
('Staged Liberalism',[M('production_factory_efficiency_gain_factor',.05),W(.1)],'Subsidise a slower transition with a continuing adjustment budget.'),
('Accountable Executive',[M('bureaucracy_cost_multiplier_modifier',-.035),M('political_power_factor',-.035)],'Make executive authority answerable to oversight instead of granting a free corruption purge.')
], 'Lacerda’s rights were suspended and he died in 1977. Early restoration is alternate history; an earned Lacerdist programme needs a real political successor after his death.')

route('prn','PRN',136,20,'PRN, separate 1989 formation and identity required',[
('A New Presidency',[C(.2),M('political_power_factor',.07),M('stability_factor',-.025)],'Develop a late-1989 personal presidential coalition. PRN is the renamed Party of Youth, not Lacerda’s party.'),
('Competition Shock',[M('production_factory_efficiency_gain_factor',.1),M('stability_factor',-.06)],'Open the economy rapidly, accepting disruption and closures among sheltered firms.'),
('Negotiated Opening',[M('production_factory_efficiency_gain_factor',.05),W(.12)],'Fund a slower competitive adjustment with an explicit transition budget.'),
('Purchasing Reform',[C(.25),M('bureaucracy_cost_multiplier_modifier',-.04)],'Build accountable public purchasing rather than granting a free corruption purge.'),
('Industrial Imports',[C(.3),R('CAT_industry',.5,2),M('foreign_influence_defense_modifier',-.035)],'Buy access to industrial technology while retaining vulnerability to external commercial pressure.'),
('Federal Service Review',[C(.2),M('bureaucracy_cost_multiplier_modifier',-.035),M('stability_factor',-.025)],'Reduce redundant appointments with a real political cost.'),
('Presidential Coalition',[M('political_power_factor',.05),M('bureaucracy_cost_multiplier_modifier',.04)],'Keep a heterogeneous governing coalition functioning through parliamentary bargains.'),
('Price Restraint',[M('inflation_gain_multiplier_modifier',-.1),M('production_speed_buildings_factor',-.05)],'Contain inflation through credit restraint. This does not recreate the 1990 deposit freeze.'),
('Productive Credit',[M('production_speed_buildings_factor',.06),M('interest_rate_multiplier_modifier',.5)],'Protect industrial credit while accepting higher financing pressure.'),
('Executive Accountability',[M('stability_factor',.035),M('political_power_factor',-.04)],'Submit presidential administration to effective oversight and legislative bargaining.')
], 'A separate late-Cold-War programme. Formation in 1989 and an actual PRN government are required; no scripted Collor victory.')

START=[
dict(id=P+'ai5',title='Rule by Institutional Act',description='Exceptional powers support executive control while censorship and repression corrode consent and intellectual freedom.',effects=[M('political_power_factor',.12),M('stability_factor',-.07),M('research_speed_factor',-.03)],remedy='Controlled Opening or Constitutional Guarantees.'),
dict(id=P+'miracle',title='Credit-Fuelled Miracle',description='Public credit and investment sustain rapid industrial expansion while increasing exposure to financing costs.',effects=[M('production_speed_buildings_factor',.08),M('industrial_capacity_factory',.04),M('interest_rate_multiplier_modifier',.5)],remedy='Refinance Development or Export Discipline replaces this mixed starting settlement.'),
dict(id=P+'wage_squeeze',title='Wage Compression',description='Wage restraint protects industrial margins while concentrating the gains from growth.',effects=[M('consumer_goods_factor',-.025),M('stability_factor',-.05)],remedy='A wage settlement or free collective bargaining removes both sides of this starting policy.'),
dict(id=P+'skills',title='Uneven Technical Education',description='Advanced industrial centres coexist with restricted access to schooling and specialist training.',effects=[M('research_speed_factor',-.07)],remedy='Technical Institutes, Mass Education or the shared National Training focus.'),
dict(id=P+'land_inequality',title='Land and Regional Inequality',description='Concentrated landholding and uneven services make rural development politically difficult.',effects=[M('agricolture_productivity_modifier',-.06),M('stability_factor',-.04)],remedy='Rural Settlement, Regional Extension or the PCdoB Agrarian Settlement.'),
dict(id=P+'urban_pressure',title='Cities Beyond Their Services',description='Rapid urbanisation strains housing, public health, transport and municipal administration.',effects=[M('bureaucracy_cost_multiplier_modifier',.08),M('stability_factor',-.035)],remedy='Municipal Networks and Urban Services complete a joint remedy.'),
dict(id=P+'oil_exposure',title='Imported Energy Dependence',description='Industrial expansion depends on imported oil. The later oil shocks have not yet happened.',effects=[M('fuel_gain_factor',-.08),M('inflation_cost_multiplier_modifier',.03)],remedy='Offshore Supply or a diversified energy settlement removes this exposure.'),
dict(id=P+'amazon_pressure',title='A Contested Frontier',description='Roads, settlement and resource ambitions confront weak administration, indigenous rights and ecological limits.',effects=[M('bureaucracy_cost_multiplier_modifier',.05),M('stability_factor',-.03)],remedy='Frontier Safeguards or a funded Territorial Administration replaces the initial burden.')
]

G('society','Institutions and Society',10,8,context='Civilian institutions, churches, workers, schools, cities and rural rights. Available to every government subject to the actual policy choice.')
N('society','constitutional','Constitutional Guarantees',0,0,effects=[C(.25),S('ai5'),M('political_power_factor',-.06)],description='End exceptional powers through a genuine constitutional reform. Early adoption is alternative history.')
N('society','church_dialogue','Church Service Grants',-4,1,[],[C(.15),M('stability_factor',.05),M('political_power_factor',-.03)],'Prioritise public grants to church-linked service organisations and dialogue with the CNBB. This funding priority does not abolish secular provision.')
N('society','secular_services','Public Service Network',0,1,[],[C(.3),M('bureaucracy_cost_multiplier_modifier',.04),M('stability_factor',.04)],'Prioritise a publicly administered service network. This funding priority does not ban church organisations or CNBB dialogue.')
EX('church_dialogue','secular_services')
N('society','legal_parties','Plural Party Law',4,1,['constitutional'],[C(.15),E('party_reform','The Party Reorganisation',[dict(title='Register competing civilian organisations',effects=[M('political_power_factor',-.04),M('stability_factor',.04)]),dict(title='Negotiate a limited transition',effects=[M('stability_factor',.02),F('the_military',5)])],'Reorganisation opens political competition. Specific parties require their genuine organisation and identity, rather than a forced ideological conversion.')],'Replace the imposed two-party framework and make actual new-party formation possible.')
N('society','schools','National Training',-2,2,[('church_dialogue','secular_services')],[C(.5),S('skills'),R('CAT_industry')],'Broaden technical training through public institutions.')
N('society','municipal','Municipal Networks',4,2,['legal_parties'],[C(.6),B(882,'infrastructure'),B(888,'infrastructure')],'Extend basic municipal networks in industrial and northeastern cities.')
N('society','universities','University Research',-4,3,['schools'],[C(.3),R('CAT_electronics',.5,2),W(.08)],'Fund university research with a continuing operating budget.')
N('society','adult_literacy','Adult Literacy',0,3,['schools'],[C(.25),M('literacy_rate_education_modifier',.06),M('education_cost_multiplier_modifier',.05)],'Expand access to literacy without pretending an immediate literacy-rate jump.')
EX('universities','adult_literacy')
N('society','urban_services','Urban Services',4,3,['municipal'],[C(.4),B(883,'offices'),W(.06)],'Provide municipal administrative capacity for health and housing services.')
N('society','city_settlement','Serviced Cities',4,4,['municipal','urban_services'],[S('urban_pressure')],'Complete the joint transport and services remedy for urban pressure.')
N('society','land_titles','Rural Settlement',-4,5,[('universities','adult_literacy')],[C(.4),S('land_inequality'),M('bureaucracy_cost_multiplier_modifier',.04),F('farmers',-7)],'Regularise landholding and expand public extension, accepting conflict and administrative costs.')
N('society','extension','Regional Extension',0,5,[('universities','adult_literacy')],[C(.35),S('land_inequality'),M('agricolture_productivity_modifier',.035),W(.1)],'Use long-term regional extension and cooperative credit without a general land redistribution.')
EX('land_titles','extension')
N('society','wage_bargain','A Wage Bargain',4,5,['city_settlement'],[C(.2),S('wage_squeeze'),M('consumer_goods_factor',.02),F('labour_unions',8)],'Replace wage compression with a funded bargaining framework.')
N('society','territory','Territorial Offices',-4,6,[('land_titles','extension')],[C(.45),B(891,'offices')],'Create civil administrative capacity in the eastern Amazon.')
N('society','frontier_safeguards','Frontier Safeguards',-4,7,['territory'],[C(.2),S('amazon_pressure'),M('production_speed_buildings_factor',-.025)],'Protect indigenous rights and establish project review before frontier expansion.')
N('society','frontier_admin','Frontier Administration',0,7,['territory'],[C(.3),S('amazon_pressure'),W(.12),M('stability_factor',-.015)],'Expand permanent civil administration and compensation in the frontier, accepting continuing contestation.')
EX('frontier_safeguards','frontier_admin')
N('society','service_audit','Public Service Audit',4,7,['wage_bargain'],[C(.2),M('bureaucracy_cost_multiplier_modifier',-.04)],'Fund professional audits rather than a free nationwide corruption-tier reduction.')
N('society','social_settlement','A Social Settlement',0,8,[('frontier_safeguards','frontier_admin'),'service_audit'],[M('stability_factor',.04),W(.08)],'Maintain a national social settlement with an explicit operating appropriation.')

G('economy','Industry and Agriculture',34,8,context='Development finance, Embraer, Embrapa, the industrial triangle and the export frontier.')
N('economy','development_bank','Development Finance',0,0,effects=[C(.3),R('CAT_industry')],description='Strengthen BNDES project appraisal without adding GDP by decree.')
N('economy','refinance','Refinance Development',-4,1,['development_bank'],[C(.65),S('miracle'),M('interest_rate_multiplier_modifier',-.4),M('production_speed_buildings_factor',.035)],'Replace the initial credit surge with better screened long-term investment.')
N('economy','export_discipline','Export Discipline',0,1,['development_bank'],[S('miracle'),M('resource_export_multiplier_modifier',.1),M('stability_factor',-.025)],'Reorient development toward export receipts and abandon the initial indiscriminate credit expansion.')
EX('refinance','export_discipline')
N('economy','industrial_triangle','Industrial Triangle',4,1,['development_bank'],[C(.9),B(882,'industrial_complex'),B(884,'industrial_complex')],'Expand São Paulo and Minas Gerais manufacturing with matched building slots.')
N('economy','embrapa','Tropical Agronomy',-2,2,[('refinance','export_discipline')],[C(.35),R('CAT_agriculture',.5,2)],'Create or expand the agricultural research institution represented historically by Embrapa in 1973.')
N('economy','capital_goods','Capital Goods',4,2,['industrial_triangle'],[C(.65),B(882,'industrial_complex')],'Fund capital-goods manufacturing rather than importing a modern production line for free.')
N('economy','cerrado','Cerrado Agribusiness',-4,3,['embrapa'],[C(.6),B(885,'agriculture_district'),M('agricolture_productivity_modifier',.07),M('stability_factor',-.025)],'Combine tropical agronomy with large-scale commercial farming and acknowledge land concentration.')
N('economy','smallholder','Smallholder Research',0,3,['embrapa'],[C(.4),B(888,'agriculture_district'),M('agricolture_productivity_modifier',.04),W(.08)],'Direct extension and credit toward smaller farmers with a larger service bill.')
EX('cerrado','smallholder')
N('economy','licensed_tools','Licensed Machine Tools',2,3,['capital_goods'],[R('CAT_industry',.5,2),W(.1),M('foreign_influence_defense_modifier',-.035)],'Licence production equipment while accepting recurrent fees and dependence.')
N('economy','national_tools','National Machine Tools',6,3,['capital_goods'],[C(.45),M('production_factory_max_efficiency_factor',.06),M('research_speed_factor',-.025)],'Prioritise a national tooling base with a narrower technology pool.')
EX('licensed_tools','national_tools')
N('economy','storage','Storage and Markets',-2,4,[('cerrado','smallholder')],[C(.4),B(886,'infrastructure')],'Link food-producing districts to storage and wholesale markets.')
N('economy','industrial_standards','Industrial Standards',4,4,[('licensed_tools','national_tools')],[C(.2),M('production_factory_efficiency_gain_factor',.05)],'Create standards and quality-control capacity for national manufacturers.')
N('economy','manaus','Manaus Industrial Zone',-4,5,['storage'],[C(.7),B(892,'industrial_complex'),M('corporate_tax_income_multiplier_modifier',-.025)],'Expand the Manaus zone through real facilities and explicit tax concessions.')
N('economy','regional_industry','Northeast Industry',0,5,['storage'],[C(.7),B(887,'industrial_complex'),W(.06)],'Fund northeastern industry and the administrative support it requires.')
EX('manaus','regional_industry')
N('economy','embraer','Embraer Production',4,5,['industrial_standards'],[C(.75),B(882,'arms_factory'),R('CAT_aircraft')],'Build on Embraer’s 1969 creation with aircraft production and a finite research award.')
N('economy','telebras','National Telecommunications',0,6,[('manaus','regional_industry')],[C(.55),B(883,'offices'),R('CAT_electronics')],'Expand the national telecommunications institution, represented by offices and period electronics research.')
N('economy','trade_fairs','Industrial Export Offices',4,6,['embraer'],[C(.25),M('country_productivity_growth_modifier',.035),W(.04)],'Fund technical export offices. This gives productivity growth, not an invented generic export-volume modifier.')
N('economy','productive_nation','A Productive Nation',0,7,['telebras','trade_fairs'],[M('production_factory_max_efficiency_factor',.04),W(.08)],'Coordinate productive institutions through a funded national programme.')

G('energy','Energy and Resources',58,8,context='Imported oil, Petrobras, hydroelectricity, alcohol fuels, civil nuclear work and paid mineral development.')
N('energy','energy_balance','National Energy Balance',0,0,effects=[C(.15),R('CAT_energy')],description='Measure industrial demand and supply vulnerability before choosing major investments.')
N('energy','offshore','Offshore Petrobras',-4,1,['energy_balance'],[C(.8),R('CAT_excavation'),M('fuel_gain_factor',.05),W(.12)],'Fund offshore exploration and refining expertise without granting unverified state oil deposits.')
N('energy','conservation','Efficient Energy Use',0,1,['energy_balance'],[C(.35),R('CAT_energy_efficiency',.5,2),M('production_speed_buildings_factor',-.025)],'Prioritise conservation and retrofitting rather than rapid supply expansion.')
EX('offshore','conservation')
N('energy','grid','Regional Power Grid',4,1,['energy_balance'],[C(.7),B(884,'infrastructure')],'Improve the regional grid through infrastructure while retaining actual electricity-generation mechanics.')
N('energy','fuel_security','Fuel Security',-2,2,[('offshore','conservation')],[C(.3),S('oil_exposure'),B(882,'fuel_silo')],'Complete storage and substitution measures that remove initial energy vulnerability.')
N('energy','hydro','Domestic Hydropower',4,2,['grid'],[C(1),B(880,'renewable_energy_infra',instant=False),W(.08)],'Build domestic hydroelectric capacity. A cross-border Itaipu project requires Paraguay’s consent in its separate focus.')
N('energy','proalcool','Alcohol Fuel Programme',-4,3,['fuel_security'],[C(.6),M('fuel_gain_factor',.1),M('agricolture_productivity_modifier',-.03),W(.12)],'Use the 1975 Proalcool precedent. Fuel security competes with land and food-sector capacity.')
N('energy','refining','Conventional Refining',0,3,['fuel_security'],[C(.7),B(883,'synthetic_refinery'),M('inflation_cost_multiplier_modifier',.025)],'Expand native refinery capacity while retaining imported-feedstock exposure in public costs.')
EX('proalcool','refining')
N('energy','nuclear_science','Civil Nuclear Science',4,3,['hydro'],[C(.4),R('CAT_nuclear_reactors',.5,2)],'Develop civilian reactor knowledge without granting a bomb or a free reactor.')
N('energy','mineral_survey','Mineral Survey',-2,4,[('proalcool','refining')],[C(.2),R('CAT_excavation'),U('uranium_study','Commission a Uranium Feasibility Study',[C(.15),R('CAT_nuclear_reactors')],['Surveyed deposit','Native paid mine-development requirements'])],'Surveying provides knowledge only. Uranium starts with zero production and zero built mines; actual development remains paid through the existing investment system.')
N('energy','reactor','Domestic Reactor Works',2,4,['nuclear_science'],[C(1.5),B(883,'nuclear_reactor',instant=False),W(.2)],'Build one civilian reactor through a major funded programme with normal native fuel and operating requirements.')
N('energy','grid_diversity','Diverse Generation',6,4,['nuclear_science'],[C(.9),B(887,'renewable_energy_infra'),R('CAT_energy_efficiency')],'Choose domestic generation diversity instead of the reactor works.')
EX('reactor','grid_diversity')
N('energy','carajas','Carajas Logistics',-2,5,['mineral_survey'],[C(.8),B(891,'infrastructure'),M('steel_export_multiplier_modifier',.08),W(.06)],'Fund logistics around the known Carajás mineral frontier. The revenue modifier requires actual exported steel resources.')
N('energy','resource_standards','Resource Standards',4,5,[('reactor','grid_diversity')],[C(.2),M('bureaucracy_cost_multiplier_modifier',.025),M('resource_export_multiplier_modifier',.04)],'Fund technical standards and mineral administration rather than instant resources.')
N('energy','energy_resilience','Energy Resilience',0,6,['carajas','resource_standards'],[M('inflation_cost_multiplier_modifier',-.035),W(.06)],'Maintain a diversified energy and resource system against external cost shocks.')
N('energy','energy_dispatch','Energy Dispatch Centre',0,7,['energy_resilience'],[C(.3),B(885,'offices')],'Coordinate supply dispatch and resource contracts through a concrete administrative facility.')

G('defence','Armed Services',82,8,context='A credible regional force with domestic production, training and explicit procurement trade-offs. No starting OOB changes.')
N('defence','joint_staff','Joint Staff Review',0,0,effects=[C(.2),X('army'),X('navy'),X('air')],description='Review force requirements across services before selecting new commitments.')
N('defence','territorial','Territorial Army',-4,1,['joint_staff'],[M('army_org_factor',.06),M('army_personnel_cost_multiplier_modifier',.08)],'Prioritise a broad territorial army with an appropriate personnel burden.')
N('defence','professional','Professional Cadres',0,1,['joint_staff'],[M('army_org_factor',.035),M('equipment_cost_multiplier_modifier',-.06),M('military_spending_cost_multiplier_modifier',.035)],'Concentrate on trained cadres and maintenance while reducing equipment waste.')
EX('territorial','professional')
N('defence','air_training','Flying Schools',4,1,['joint_staff'],[C(.3),R('CAT_aircraft'),X('air',35)],'Expand flying instruction before committing to new airframes.')
N('defence','imbel','Small Arms Industry',-2,2,[('territorial','professional')],[C(.65),B(884,'arms_factory')],'Develop national small-arms production using the later IMBEL consolidation as a precedent.')
N('defence','air_safety','Flight Safety',4,2,['air_training'],[M('air_accidents_factor',-.1),M('airforce_personnel_cost_multiplier_modifier',.05)],'Fund safety instruction and maintenance with a larger skilled-personnel bill.')
N('defence','jungle','Jungle School',-4,3,['imbel'],[C(.25),X('army',40),R('CAT_electronics',.25)],'Fund jungle communications and staff exercises. No invented jungle combat modifier is promised.')
N('defence','mechanised','Mechanised Workshops',0,3,['imbel'],[C(.6),B(882,'arms_factory'),M('equipment_cost_multiplier_modifier',.035)],'Expand vehicle workshops with an explicit cost for domestic production depth.')
EX('jungle','mechanised')
N('defence','air_support','Tactical Air Support',2,3,['air_safety'],[M('air_mission_efficiency',.06),M('airforce_personnel_cost_multiplier_modifier',.06)],'Build a tactical-support air service with the required specialist staff.')
N('defence','air_defence','Airspace Defence',6,3,['air_safety'],[C(.4),B(885,'air_base'),X('air',30)],'Develop domestic airspace defence through basing and training.')
EX('air_support','air_defence')
N('defence','naval_yards','Naval Workshops',-2,4,[('jungle','mechanised')],[C(.8),B(883,'dockyard')],'Expand naval workshops in Rio without granting completed ships.')
N('defence','joint_exercises','Joint Exercises',4,4,[('air_support','air_defence')],[C(.2),X('army',25),X('air',25)],'Fund joint planning and exercises across services.')
N('defence','ocean_fleet','Oceanic Fleet',-4,5,['naval_yards'],[M('navy_org_factor',.08),M('navy_personnel_cost_multiplier_modifier',.12),W(.1)],'Maintain an oceanic fleet with a large specialist and operating burden.')
N('defence','coastal_fleet','Coastal Escort Fleet',0,5,['naval_yards'],[M('industrial_capacity_dockyard',.08),M('navy_org_factor',-.03)],'Prioritise cheaper escort production over the cohesion of a broader blue-water force.')
EX('ocean_fleet','coastal_fleet')
N('defence','procurement','Procurement Office',4,5,['joint_exercises'],[C(.25),M('equipment_cost_multiplier_modifier',-.05),M('bureaucracy_cost_multiplier_modifier',.025)],'Standardise procurement through a funded contracting office.')
N('defence','avibras','Rocket Engineering',-2,6,[('ocean_fleet','coastal_fleet')],[C(.5),R('CAT_electronics'),X('army',20)],'Develop national guidance and electronics expertise without a free later ASTROS stockpile.')
N('defence','exports_arms','Defence Export Office',4,6,['procurement'],[C(.25),M('industrial_capacity_factory',.035),M('foreign_influence_defense_modifier',-.025)],'Support export-oriented defence production while accepting foreign market dependence.')
N('defence','regional_force','A Regional Force',0,7,['avibras','exports_arms'],[M('army_org_factor',.025),W(.08)],'Maintain a balanced regional force through an explicit staff and readiness budget.')

# Reciprocal offers originate in individual Brazilian focuses. They never activate on completion.
def offer(key,title,dx,y,parents,partner,pname,brazil,other,desc,family='cooperation',conditions=(),basis='Period precedent; RP terms are proposed, not a recreation of historical contractual quantities.'):
    k=N('diplomacy',key,title,dx,y,parents,[],desc,conditions,days=35,basis=basis,lifetime='treaty')
    n=NODES[-1];n['offer']=dict(partner=partner,partner_name=pname,family=family,brazil=dict(name='Brazil: '+title,spirit=P+key+'_BRA',effects=brazil),recipient=dict(name=pname+': '+title,spirit=P+key+'_'+partner,effects=other),no_expiry=True,consent='Named recipient receives separate Accept and Decline decisions.',activation='Both exist; no bilateral war; no embargo either way; no diplomatic, financial, economic or military Imperia sanction either way.',setup='Once at acceptance; each payer uses own current GDP.',weekly='Current own GDP annual share divided by 52; no fee or asset replay on restoration.')
    return k
G('diplomacy','Itamaraty and RP Agreements',112,8,context='Distinct national-focus offers, real recipient decisions, complete prospective two-country rewards and permanent conditional agreements.')
N('diplomacy','itamaraty','Itamaraty Review',0,0,effects=[C(.15),M('bureaucracy_cost_multiplier_modifier',.025)],description='Define practical diplomatic priorities without committing any foreign player.')
N('diplomacy','atlantic','Atlantic Continuity',-6,1,['itamaraty'],[M('research_speed_factor',.025),M('foreign_influence_defense_modifier',-.04)],'Prioritise established Atlantic commercial and technical links.')
N('diplomacy','pragmatism','Responsible Pragmatism',0,1,['itamaraty'],[M('resource_export_multiplier_modifier',.05),M('political_power_factor',-.035)],'Diversify diplomatic partners despite domestic anticommunist opposition.')
EX('atlantic','pragmatism')
N('diplomacy','regional','Regional Accommodation',6,1,['itamaraty'],[C(.15),M('stability_factor',.025)],'Reduce regional rivalry through negotiation while preserving recipient choice.')
offer('us_training','US Training Mission',-8,2,['atlantic'],'USA','United States',[C(.25),W(.06),M('army_org_factor',.04),M('foreign_influence_defense_modifier',-.04),X('army',30)],[C(.04),W(.015),M('army_org_factor',.015),X('army',15)],'Negotiate training and technical cooperation. The 1977 human-rights dispute remains a later event.',family='US defence')
offer('us_industry','US Industrial Licences',-4,2,['atlantic'],'USA','United States',[C(.4),W(.08),M('production_factory_efficiency_gain_factor',.06),M('foreign_influence_defense_modifier',-.05),R('CAT_industry')],[C(.05),W(.015),M('country_productivity_growth_modifier',.015),R('CAT_industry',.25)],'Negotiate industrial licensing rather than assume foreign technology is available.',family='US defence')
EX('us_training','us_industry')
offer('china_trade','China Trade Mission',0,2,['pragmatism'],'CHI','China',[C(.15),W(.035),M('resource_export_multiplier_modifier',.07),M('political_power_factor',-.025)],[C(.08),W(.025),M('resource_export_multiplier_modifier',.04),M('bureaucracy_cost_multiplier_modifier',.015)],'Build a trade relationship from the 1974 recognition precedent. Early mutual recognition is explicit alternative diplomacy.',family='diversification')
offer('ussr_machines','Soviet Machinery Trade',4,2,['pragmatism'],'SOV','Soviet Union',[C(.25),W(.06),R('CAT_industry',.5,2),M('resource_export_multiplier_modifier',.05),M('foreign_influence_defense_modifier',-.03)],[C(.08),W(.025),R('CAT_agriculture'),M('resource_export_multiplier_modifier',.035)],'Exchange agricultural trade access and machinery expertise on the model of the 1975 agreement.',family='diversification')
offer('itaipu','Itaipu Proposal',8,2,['regional'],'PAR','Paraguay',[C(1.5),W(.18),B(880,'renewable_energy_infra',instant=False),M('inflation_cost_multiplier_modifier',-.025),dict(kind='weekly_transfer',source='BRA',target='PAR',annual_gdp_percent=.08,direction='expense')],[C(.65),W(.12),B(895,'renewable_energy_infra',instant=False),M('inflation_cost_multiplier_modifier',-.025),dict(kind='weekly_transfer',source='BRA',target='PAR',annual_gdp_percent=.08,direction='income')],'Negotiate a binational hydropower project from the 1973 treaty precedent. Each funds its own share; Brazil also finances a GDP-indexed royalty stream to Paraguay. The RP royalty models the asymmetric financing and offtake bargain; it does not promise an unimplemented electricity transfer.',family='Parana basin')
offer('japan_agro','Japan Cerrado Research',-6,3,[('us_training','us_industry')],'JAP','Japan',[C(.45),W(.08),M('agricolture_productivity_modifier',.06),R('CAT_agriculture'),M('stability_factor',-.02)],[C(.08),W(.025),R('CAT_agriculture'),M('country_productivity_growth_modifier',.015)],'Negotiate agronomy, finance and extension from the PRODECER precedent, with land pressures made visible.',family='Japan')
offer('japan_steel','Japan Steel Consortium',-2,3,[('us_training','us_industry')],'JAP','Japan',[C(.75),W(.1),B(884,'industrial_complex'),M('steel_export_multiplier_modifier',.05)],[C(.1),W(.035),R('CAT_industry'),M('production_factory_efficiency_gain_factor',.025)],'Use joint industrial investment and long-term market access rather than an automatic foreign resource concession.',family='Japan')
EX('japan_agro','japan_steel')
offer('angola','Angola Technical Pact',2,3,['china_trade'],'AGL','Angola',[C(.12),W(.04),M('country_productivity_growth_modifier',.015),M('bureaucracy_cost_multiplier_modifier',.015)],[C(.15),W(.06),R('CAT_industry'),M('production_speed_buildings_factor',.035),M('foreign_influence_defense_modifier',-.03)],'Offer technical cooperation after independence and recognition. This does not grant Angola’s oil to Brazil.',family='Atlantic South',conditions=['Angola is independent and recognised'])
offer('arg_basin','Parana Basin Accord',6,3,['itaipu'],'ARG','Argentina',[C(.2),W(.035),M('production_speed_buildings_factor',.035),M('bureaucracy_cost_multiplier_modifier',.02)],[C(.2),W(.035),M('production_speed_buildings_factor',.035),M('bureaucracy_cost_multiplier_modifier',.02)],'Resolve river-project conflicts using the 1979 Itaipu-Corpus settlement as precedent. This bilateral proposal cannot bind Paraguay.',family='Parana basin',conditions=['Active Brazil-Paraguay Itaipu agreement'])
offer('germany_nuclear','German Nuclear Accord',-6,4,[('japan_agro','japan_steel')],'GER','Federal Republic of Germany',[C(.9),W(.15),R('CAT_nuclear_reactors',.5,2),M('production_speed_nuclear_reactor_factor',.08),M('foreign_influence_defense_modifier',-.04)],[C(.12),W(.04),R('CAT_nuclear_reactors'),M('industrial_capacity_factory',.02)],'Negotiate technology cooperation from the 1975 treaty. Uranium mining, fuel supply and construction remain separate paid projects.',family='nuclear technology')
N('diplomacy','nuclear_dialogue','Nuclear Transparency',10,3,['regional'],[C(.15),R('CAT_nuclear_reactors',.25)],'Explore civilian nuclear confidence-building independently of river disputes or a German treaty.')
offer('arg_nuclear','Argentine Nuclear Confidence',10,4,['nuclear_dialogue'],'ARG','Argentina',[C(.3),W(.06),R('CAT_nuclear_reactors'),M('research_speed_factor',.025),M('bureaucracy_cost_multiplier_modifier',.025)],[C(.3),W(.06),R('CAT_nuclear_reactors'),M('research_speed_factor',.025),M('bureaucracy_cost_multiplier_modifier',.025)],'Use the 1980 cooperation agreement and 1985 confidence-building precedent for mutual civilian transparency, not a free joint weapons programme.',family='nuclear technology',conditions=[])
offer('arg_integration','Argentine Industrial Protocol',4,5,['arg_nuclear'],'ARG','Argentina',[C(.45),W(.08),M('production_factory_efficiency_gain_factor',.05),M('bureaucracy_cost_multiplier_modifier',.025),R('CAT_industry')],[C(.45),W(.08),M('production_factory_efficiency_gain_factor',.05),M('bureaucracy_cost_multiplier_modifier',.025),R('CAT_industry')],'Use the 1986 integration protocols to coordinate industry. This does not found Mercosur in 1970 or create automatic membership.',family='Southern integration',conditions=['Active Argentine Nuclear Confidence agreement'])
offer('uruguay','Uruguay Port Protocol',-4,6,['arg_integration'],'URG','Uruguay',[C(.2),W(.04),M('resource_export_multiplier_modifier',.045),M('bureaucracy_cost_multiplier_modifier',.02)],[C(.3),W(.055),B(893,'offices'),M('resource_export_multiplier_modifier',.04)],'Negotiate port administration and commercial cooperation as a plausible period RP protocol.',family='Southern integration')
offer('france_aircraft','French Mirage Partnership',-2,4,[('japan_agro','japan_steel')],'FRA','France',[C(.5),W(.08),R('CAT_aircraft',.5,2),M('air_mission_efficiency',.025),M('foreign_influence_defense_modifier',-.035)],[C(.08),W(.025),R('CAT_aircraft'),M('production_factory_efficiency_gain_factor',.02)],'Negotiate Mirage III training, maintenance and technical cooperation from the 1970 procurement precedent. No AMX programme or free aircraft is implied.',family='aerospace')
N('diplomacy','regional_secretariat','Regional Secretariat',0,7,['arg_integration','uruguay'],[C(.25),B(885,'offices'),W(.05)],'Maintain a consultative secretariat. It is not a new economic organisation or an automatic member-only reward.')

# Conditional events are visible design content. Future world shocks are never starting ideas.
E('oil_shock','The Imported Oil Bill',[dict(title='Protect investment',effects=[M('production_speed_buildings_factor',.04),M('inflation_cost_multiplier_modifier',.06),W(.15)]),dict(title='Restrain consumption',effects=[M('inflation_gain_multiplier_modifier',-.08),M('industrial_capacity_factory',-.045)])],'After an actual world oil-price shock or a historical late-1973 event, the cabinet chooses adjustment. If an equivalent native shock exists, replace its Brazil response instead of stacking another global penalty.')
E('debt_crisis','The External Credit Squeeze',[dict(title='Negotiate an adjustment programme',effects=[C(.3),M('interest_rate_multiplier_modifier',-.6),M('production_speed_buildings_factor',-.06)]),dict(title='Defend domestic investment',effects=[M('production_speed_buildings_factor',.05),M('interest_rate_multiplier_modifier',1),M('inflation_gain_multiplier_modifier',.08)])],'A historical 1982 stress event requires actual debt and adverse credit conditions. No automatic 1970 debt crisis or debt principal forgiveness.')
E('us_rights','Military Aid and Human Rights',[dict(title='Retain agreed cooperation',effects=[M('political_power_factor',-.04),M('stability_factor',.02)]),dict(title='Denounce the military arrangement',effects=[dict(kind='suspend_agreement',agreement='us_training',label='Terminate US Training Mission'),M('political_power_factor',.04),M('army_org_factor',-.025)])],'The 1977 dispute can arise if the US agreement is active. Either RP country retains its real treaty and sanction controls.')
E('party_split','The Labourist Naming Dispute',[dict(title='Recognise distinct PTB and PDT organisations',effects=[M('political_power_factor',-.025),M('stability_factor',.025)])],'The later PTB and PDT must be separately registered. The event cannot make both share one ruling-party identity.')
E('inflation_settlement','Prices, Wages and Credit',[dict(title='Negotiated stabilisation',effects=[C(.3),M('inflation_gain_multiplier_modifier',-.1),M('production_speed_buildings_factor',-.04)]),dict(title='Production first',effects=[M('industrial_capacity_factory',.05),M('inflation_gain_multiplier_modifier',.08)])],'A later inflation event requires sustained native inflation. Policy values are temporary for 365 days and replace earlier crisis responses rather than accumulating.')

STATES={895:'Paraguay',879:'Rio Grande do Sul',880:'Parana',882:'Sao Paulo',883:'Rio de Janeiro',884:'Minas Gerais',885:'Goias',886:'Mato Grosso',887:'Bahia',888:'Pernambuco',891:'Para',892:'Amazonas',893:'Uruguay (Rio de la Plata)'}

# Reviewed spatial and institutional revisions, applied to this single design model.
by={n['key']:n for n in NODES}
def revise(key,parents=None,dx=None,y=None,conditions=None):
    n=by[key];g=next(g for g in GROUPS if g['id']==n['group'])
    if parents is not None:n['prerequisites']=[list(p) if not isinstance(p,str) else [p] for p in parents]
    if dx is not None:n['x']=g['x']+dx
    if y is not None:n['y']=g['y']+y
    if conditions is not None:n['conditions']=conditions
def unexclude(a,b):
    by[a]['exclusions'].remove(b);by[b]['exclusions'].remove(a)

# Different political institutions use different substantive dependency structures.
revise('military_4',['military_0'],dx=-4,y=2)
EX('arena_4','arena_5');revise('arena_6',[('arena_4','arena_5')])
revise('mdb_9',['mdb_6',('mdb_7','mdb_8')],dx=0,y=7)
revise('ptb_4',['ptb_3'],dx=-4,y=3);revise('ptb_5',['ptb_0'],dx=4,y=2)
revise('ptb_6',['ptb_4','ptb_5'])
revise('pdt_6',['pdt_3'])
revise('pt_5',['pt_0'],dx=4,y=2);revise('pt_6',['pt_3','pt_4'])
revise('pfl_6',['pfl_3'],dx=-2)
revise('pfl_7',['pfl_5'],dx=0);revise('pfl_8',['pfl_5'],dx=4)
revise('pfl_9',['pfl_6',('pfl_7','pfl_8')],dx=2)
revise('psdb_5',['psdb_3'],dx=4,y=3);revise('psdb_6',['psdb_4'],dx=-2,y=4)
revise('psdb_7',['psdb_3'],dx=2,y=5);revise('psdb_8',['psdb_3'],dx=6,y=5)
revise('psdb_9',['psdb_6',('psdb_7','psdb_8')])
EX('pcb_4','pcb_5');revise('pcb_6',[('pcb_4','pcb_5')])
revise('pcdob_6',['pcdob_3'])
revise('pcdob_7',['pcdob_4']);revise('pcdob_8',['pcdob_5'])
revise('pcdob_9',['pcdob_6',('pcdob_7','pcdob_8')])
revise('populist_6',['populist_3'],y=3)
revise('prn_4',['prn_3']);revise('prn_5',['prn_0'],dx=4,y=2)
revise('prn_6',['prn_3','prn_4']);revise('prn_9',['prn_6',('prn_7','prn_8')],y=7)

# Church dialogue and public administration coexist. Their grants are not a sectarian state choice.
unexclude('church_dialogue','secular_services')
revise('municipal',[]);revise('city_settlement',['urban_services'])

# Foreign partners do not unlock unrelated countries' diplomacy by accepting a deal.
N('diplomacy','technical_desk','Technical Diplomacy',-12,2,[('atlantic','pragmatism')],[C(.12),R('CAT_electronics',.25)],'Fund a technical negotiating desk for independent European industrial and aviation proposals.')
N('diplomacy','pacific_desk','Pacific Commerce',-2,2,[('atlantic','pragmatism')],[C(.12),R('CAT_agriculture',.25)],'Prepare Japanese commercial and agricultural negotiations independently of any US agreement.')
N('diplomacy','commercial_desk','Regional Commerce',6,2,['regional'],[C(.12),R('CAT_industry',.25)],'Prepare regional industrial negotiations independently of nuclear or river treaties.')
N('diplomacy','industrial_talks','Industrial Talks',4,3,['commercial_desk'],[C(.12),R('CAT_industry',.25)],'Draft industrial terms for Argentina without making a nuclear agreement compulsory.')
revise('germany_nuclear',['technical_desk'],dx=-12,y=3)
revise('france_aircraft',['technical_desk'],dx=-8,y=3)
revise('japan_agro',['pacific_desk']);revise('japan_steel',['pacific_desk'])
revise('nuclear_dialogue',['commercial_desk'])
revise('arg_integration',['industrial_talks'],dx=4,y=4,conditions=[])
revise('uruguay',['arg_integration'],dx=2,y=5)
revise('regional_secretariat',['uruguay'],dx=0,y=6)
by['arg_basin']['title']='River Consultations'
by['arg_basin']['description']='Negotiate bilateral river-project consultation, inspired by the conflict resolved in 1979. This RP agreement is not the historical tripartite Itaipu-Corpus settlement and cannot bind Paraguay.'
by['itaipu']['description']='Negotiate a binational capacity project from the 1973 treaty precedent. Each funds its own GDP share. Brazil also makes an RP financial-support payment to Paraguay; this is not the historical Itaipu royalty formula or a promise of physical electricity delivery.'
for side in ('brazil','recipient'):
    for e in by['itaipu']['offer'][side]['effects']:
        if e['kind']=='weekly_transfer':e['purpose']='RP project financing support, not historical royalties or electricity pricing'

# Keep restored pre-coup labourism separate from Ivete Vargas's later registered PTB.
next(g for g in GROUPS if g['id']=='ptb').update(title='Historic PTB',identity='Restored pre-1965 PTB only',context='A counterfactual restoration of the dissolved pre-1965 party. Later PTB and PDT are separate registered organisations.')
by['ptb_0']['description']='Restore the dissolved pre-1965 labourist organisation through a real political opening. This explicitly counterfactual identity is distinct from Ivete Vargas’s later PTB.'
route('ptb_late','PTB',148,3,'Later PTB, separate registration required',[
('A Labour Coalition',[C(.18),M('political_power_factor',.06),M('bureaucracy_cost_multiplier_modifier',.04)],'Build the later PTB as its own labour and regional coalition, distinct from Brizola’s PDT and the dissolved old PTB.'),
('Employer Compact',[M('industrial_capacity_factory',.06),F('labour_unions',-6)],'Support production through an employer-oriented compact at a cost in union confidence.'),
('Union Agreements',[M('stability_factor',.055),F('industrial_conglomerates',-6),M('social_cost_multiplier_modifier',.03)],'Negotiate labour protections while accepting resistance from larger employers.'),
('Benefit Administration',[C(.25),M('bureaucracy_cost_multiplier_modifier',.035),M('stability_factor',.025)],'Fund professional benefit administration rather than promise unfunded social rights.'),
('Vocational Training',[C(.3),R('CAT_industry')],'Expand practical training through the labour and industrial institutions.'),
('Regional Employers',[C(.4),B(887,'offices')],'Provide commercial and labour administration for smaller regional employers.'),
('Workplace Compact',[S('wage_squeeze'),M('consumer_goods_factor',.02)],'Replace wage compression through a negotiated wage and employment settlement.'),
('Social Protection',[M('stability_factor',.05),M('social_cost_multiplier_modifier',.07)],'Expand protection with a clearly visible public-service bill.'),
('Employment Credit',[M('production_speed_buildings_factor',.05),M('interest_rate_multiplier_modifier',.4)],'Protect hiring and investment through credit, accepting greater financing exposure.'),
('Coalition Guarantees',[M('stability_factor',.03),M('political_power_factor',-.03)],'Make labour policy answerable to a working parliamentary coalition.')
], 'The later PTB won its own registration and name during the 1979/80 reorganisation. It is not the old party or the PDT renamed.')

# Short English names fit the native 147-pixel title field without truncation.
SHORT={'military_8':'Procurement Rules','arena_2':'Technical Cabinet','mdb_0':'Congressional Reform','pdt_0':'Labourist Democracy','pdt_5':'Local Services','pdt_8':'Licensed Industry','populist_9':'Executive Oversight','prn_5':'Service Review','prn_9':'Public Accountability','constitutional':'Civil Guarantees','church_dialogue':'Church Grants','secular_services':'Public Service Plan','refinance':'Development Loans','licensed_tools':'Licensed Tooling','national_tools':'National Tooling','manaus':'Manaus Industry','telebras':'Telecommunications','trade_fairs':'Export Offices','energy_balance':'Energy Balance','proalcool':'Alcohol Fuels','reactor':'Reactor Programme','energy_dispatch':'Power Dispatch','mechanised':'Vehicle Workshops','pragmatism':'Pragmatic Diplomacy','regional':'Regional Diplomacy','ussr_machines':'Soviet Machinery','japan_agro':'Cerrado Cooperation','japan_steel':'Japan Steel Pact','germany_nuclear':'German Nuclear Pact','arg_nuclear':'Nuclear Confidence','arg_integration':'Industrial Protocol','france_aircraft':'Mirage Partnership'}
for n in NODES:
    if n['key'] in SHORT:n['title']=SHORT[n['key']]
    n['spirit_name']=n['title']
    if 'offer' in n:
        n['offer']['brazil']['name']='Brazil: '+n['title'];n['offer']['recipient']['name']=n['offer']['partner_name']+': '+n['title']
    if n['anchor']:
        a=next(a for a in NODES if a['id']==n['anchor']);n['offset']=[n['x']-a['x'],n['y']-a['y']]

# Pack complete programme footprints, leaving at least one native card gap between groups.
# The lower band starts after a single clear separation row; no global GUI is changed.
for political in (True,False):
    cursor=0
    for g in sorted([g for g in GROUPS if (g['slot'] is not None)==political],key=lambda g:g['x']):
        ns=[n for n in NODES if n['group']==g['id']]
        shift=cursor-min(n['x'] for n in ns);dy=0 if political else 1
        for n in ns:n['x']+=shift;n['y']+=dy
        g['x']+=shift;g['y']+=dy
        cursor=max(n['x'] for n in ns)+2
for n in NODES:
    if n['anchor']:
        a=next(a for a in NODES if a['id']==n['anchor']);n['offset']=[n['x']-a['x'],n['y']-a['y']]

# Keep mechanical explanations in design records, outside normal player-facing prose.
CLEAN={
'pt_4':'Create the municipal planning and administrative capacity required for broad urban healthcare, with a funded operating budget.',
'mineral_survey':'Survey known mineral prospects and fund feasibility work. Extraction requires a separately financed mine-development project.',
'jungle':'Fund jungle communications, field instruction and staff exercises for Brazil’s difficult interior terrain.',
'grid':'Extend the regional power grid to carry growing industrial and urban demand.',
'energy_balance':'Measure industrial demand and imported-fuel exposure before choosing major investments.',
'hydro':'Build domestic hydroelectric capacity and its operating institutions. Cross-border Itaipu development requires a separate agreement with Paraguay.',
'resource_standards':'Fund technical standards, geological services and the institutions that manage mineral sales.',
'trade_fairs':'Fund technical export offices and quality promotion to strengthen productive firms and their commercial networks.',
'embraer':'Expand aircraft manufacturing from Embraer’s 1969 foundations, funding production capacity and aeronautical research.',
'pcdob_3':'Create a permanent civil administration in Pará to govern and deliver services beyond the revolutionary organisation.',
'pcdob_9':'Turn a rural revolutionary organisation into a working administration with lasting public responsibilities.',
'arg_nuclear':'Negotiate mutual civilian nuclear transparency using the 1980 cooperation and 1985 confidence-building precedents.',
'arg_integration':'Negotiate an industrial integration protocol using the 1986 programme as a precedent. Any earlier signature represents an alternative regional initiative.',
'germany_nuclear':'Negotiate civilian technology cooperation using the 1975 treaty as a precedent. Reactor construction, fuel procurement and mineral development require separate investment.',
'france_aircraft':'Negotiate Mirage III training, maintenance and technical cooperation from the 1970 procurement precedent.',
'regional_secretariat':'Maintain a consultative regional secretariat for the signed commercial protocols.',
'ptb_9':'Maintain a labourist government whose employment and social commitments rest on functioning public institutions.',
'pdt_9':'Anchor education in a sustained national programme with stable administrative support.',
'military_9':'Give the service leadership a defined mission, clear responsibilities and a professional review of its institutional role.'}
for n in NODES:
    if n['key'] in CLEAN:n['description']=CLEAN[n['key']]
    if n['key'] in ('embrapa','proalcool','itaipu','germany_nuclear','japan_agro','japan_steel','arg_nuclear'):
        n['basis']='Documented later-period precedent. Earlier completion is an explicit alternative policy or treaty proposal; the historical outcome is never automatic.'
        if 'earlier' not in n['description'].lower():n['description']+=' An earlier programme is an alternative to the historical sequence.'
    if n['key']=='reactor':n['conditions'].append('has_tech = reactor1')

for s in START:
    if s['id'].endswith('ai5'):s['remedy']='Controlled Opening or Civil Guarantees.'
    if s['id'].endswith('miracle'):s['remedy']='Development Loans or Export Discipline replaces the mixed starting credit settlement.'
    if s['id'].endswith('skills'):s['remedy']='National Training or the PDT Mass Education programme.'
