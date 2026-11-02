# IMPERIA COLD WAR — Cold War Chile review-only concept and native focus preview.
"""Writes review artifacts only. Never writes common/, events/, history/ or localisation/."""
from pathlib import Path
import json, re, hashlib, base64, io
from collections import Counter
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
VIS=Path(r'C:/Users/sonyz/.codex/visualizations/2026/10/31/01a19248-4ae8-7450-a750-4d23e1673ac8')
DONOR=Path(r'C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3374271790')
P='COLDWAR_CHL_'
D={'project':'IMPERIA COLD WAR','feature':'Cold War Chile 1970-1990','status':'CONCEPT: approval required before implementation','groups':[],'nodes':[],'spirits':[],'agreements':[],'events':[]}
N=D['nodes']; G=D['groups']; B={}
# All values are balance proposals. Native keys are audited separately; no copper resource is invented.
STATS={
'pp':('political_power_factor','Political Power Gain'), 'st':('stability_factor','Stability'),
'res':('research_speed_factor','Research Speed'), 'ag':('agricolture_productivity_modifier','Agriculture Productivity'),
'tax':('tax_gain_multiplier_modifier','Tax Revenue'), 'corp':('corporate_tax_income_multiplier_modifier','Corporate Tax Revenue'),
'exp':('resource_export_multiplier_modifier','Resource Export Revenue'), 'int':('interest_rate_multiplier_modifier','Interest Rate'),
'edu':('education_cost_multiplier_modifier','Education Expenditure'), 'soc':('social_cost_multiplier_modifier','Social Expenditure'),
'health':('health_cost_multiplier_modifier','Health Expenditure'), 'bur':('bureaucracy_cost_multiplier_modifier','Bureaucracy Expenditure'),
'police':('police_cost_multiplier_modifier','Police Expenditure'), 'pers':('army_personnel_cost_multiplier_modifier','Military Personnel Expenditure'),
'build':('production_speed_buildings_factor','Construction Speed'), 'civ':('production_speed_industrial_complex_factor','Civilian Factory Construction Speed'),
'infra':('production_speed_infrastructure_factor','Infrastructure Construction Speed'),
'arms':('production_speed_arms_factory_factor','Military Factory Construction Speed'),
'out':('industrial_capacity_factory','Factory Output'),'dock':('industrial_capacity_dockyard','Dockyard Output'),
'cap':('production_factory_max_efficiency_factor','Production Efficiency Cap'), 'gain':('production_factory_efficiency_gain_factor','Production Efficiency Growth'),
'org':('army_org_factor','Division Organization'), 'rec':('army_morale_factor','Division Recovery Rate'),
'supply':('supply_consumption_factor','Supply Consumption'),'train':('training_time_army_factor','Division Training Time'),
'defense':('army_core_defence_factor','Division Defense on Core Territory'),'speed':('army_speed_factor','Division Speed'),
'arty':('army_artillery_attack_factor','Artillery Attack'),'navy':('navy_org_factor','Naval Organization'),
'air':('air_mission_efficiency','Air Mission Efficiency'),'detect':('air_interception_detect_factor','Interception Detection'),
'influence':('foreign_influence_modifier','Foreign Influence'),'resist':('foreign_influence_defense_modifier','Foreign Influence Defense'),
'trade':('trade_opinion_factor','Trade Opinion'),'sanction':('imp_sanction_resistance','Sanction Resistance'),
}
D['stats']=STATS
def mm(**kw):return {STATS[k][0]:v for k,v in kw.items()}
def spirit(key,name,desc,mods):
    s=dict(id=P+key,name=name,description=desc,modifiers=mods,source='HISTORICAL_RESEARCH.md',kind='national')
    D['spirits'].append(s);return s
spirit('divided_congress','A Republic under Strain','Organized mass parties compete within the 1925 constitutional order, but no bloc can easily secure consent for its programme.',mm(pp=-.12,st=-.06,resist=.05))
spirit('copper_dependence','Copper and the External Account','Copper underpins export earnings. Concentrated markets and dependence on imported machinery leave public finances exposed.',mm(exp=.06,trade=-.08,int=.5))
spirit('rural_conflict','Unfinished Agrarian Reform','Redistribution and rural unionization have opened the countryside to change. Credit, technical assistance and disputed titles lag behind.',mm(ag=-.12,st=-.04))
spirit('inflation','Inflationary Expectations','Persistent price pressure raises the cost of credit and undermines confidence in long public investment programmes.',mm(int=1,build=-.06))
spirit('specialists','Uneven Technical Education','Chile possesses capable universities and engineers, but specialist training does not yet meet the needs of a diversified economy.',mm(res=-.07))
spirit('long_coast','A Long and Uneven Republic','Mines, farms, ports and isolated southern communities depend on transport corridors vulnerable to disruption.',mm(supply=.08,infra=-.10))

def group(key,title,x,y,party=None,desc=''):
    g=dict(id=key,title=title,x=x,y=y,party=party,description=desc,anchor=None)
    G.append(g);return g
def node(key,title,g,x,y,parents=(),mods=None,money=0,weekly=0,desc='',icon='politics',days=35,remove=(),buildings=(),research=(),event=None,decision=None,require=()):
    gg=next(a for a in G if a['id']==g)
    n=dict(key=key,id=P+key,title=title,description=desc or title+'.',group=g,x=gg['x']+x,y=gg['y']+y,
       anchor=gg['anchor'],dx=x,dy=y,prerequisites=[[P+p for p in block] if isinstance(block,(tuple,list)) else [P+block] for block in parents],
       excludes=[],party=gg['party'],modifiers=mods or {},money=money,weekly=weekly,remove=[P+r for r in remove],
       buildings=[dict(state=s,type=t,levels=l,slots=l) for s,t,l in buildings],research=[dict(category=c,bonus=b,uses=u) for c,b,u in research],
       event=event,decision=decision,requirements=list(require),icon=icon,cost=days/7,days=days,
       programme=gg['title']+' Programme',lifetime='party' if gg['party'] is not None else 'national',
       history='HISTORICAL_RESEARCH.md',reference='MD_REFERENCE.md: Russia local anchored programme clusters; France visible party alternatives')
    if gg['anchor'] is None:gg['anchor']=n['id'];n['anchor']=None;n['dx']=n['x'];n['dy']=n['y']
    N.append(n);B[key]=n;return n
def ex(*keys):
    for k in keys:B[k]['excludes'] += [P+j for j in keys if j!=k]
def add_programme(g,title,party,x,y,rows):
    group(g,title,x,y,party)
    for row in rows:
        key,name,xx,yy,parents,mods,money,weekly,desc,*rest=row
        node(key,name,g,xx,yy,parents,mods,money,weekly,desc,**(rest[0] if rest else {}))

# Upper chapters: institutions, national development, armed forces, and reciprocal diplomacy.
group('republic','The Republic and its Institutions',8,0)
node('constitutional_mandate','The Constitutional Mandate','republic',0,0,mods=mm(pp=.06,bur=.02),desc='Fund Congress and the electoral administration to uphold a contested presidential succession.',days=14,event='election')
node('schneider_doctrine','The Schneider Doctrine','republic',-4,2,['constitutional_mandate'],mm(resist=.08,pers=.03),desc='Affirm military subordination to the lawful civilian government and address professional grievances.',icon='army',require=['Civilian constitutional government.'])
node('congressional_guarantees','Congressional Guarantees','republic',0,2,['constitutional_mandate'],mm(st=.05,pp=-.04),desc='Bind the executive to negotiated guarantees for Congress, courts and political organization.')
node('electoral_rolls','Independent Electoral Rolls','republic',4,2,['constitutional_mandate'],mm(st=.03,bur=.03),money=1,desc='Protect registration and scrutiny from intervention by whichever party governs.')
node('cross_party_accord','A Cross-Party Accord','republic',-2,4,['schneider_doctrine','congressional_guarantees'],mm(pp=.08,st=.03),desc='Negotiate a common constitutional floor without requiring agreement on ownership or social policy.',remove=['divided_congress'])
node('presidential_initiative','Presidential Initiative','republic',2,4,['congressional_guarantees','electoral_rolls'],mm(pp=.14,st=-.03),desc='Secure a wider executive legislative mandate, accepting stronger opposition to concentrated authority.')
ex('cross_party_accord','presidential_initiative')
node('civil_service','A Professional Civil Service','republic',0,6,[('cross_party_accord','presidential_initiative')],mm(bur=-.06,res=.02),money=2,desc='Replace patronage appointments with professional examinations and protected technical careers.')
node('housing_services','Neighbourhood Services','republic',-4,8,['civil_service'],mm(st=.05,soc=.05),money=2,desc='Extend water, clinics and public services through municipal and neighbourhood institutions.',icon='social')
node('mapuche_titles','Mapuche Land Guarantees','republic',0,8,['civil_service'],mm(st=.04,ag=-.02,bur=.03),money=1,desc='Recognize indigenous community claims and fund legal settlement of disputed titles.',icon='land')
node('judicial_review','Independent Judicial Review','republic',4,8,['civil_service'],mm(resist=.06,pp=-.03),money=1,desc='Give courts the resources to enforce lawful procedure against both executive and private abuses.')
node('commission_truth','A National Truth Commission','republic',-2,10,['housing_services','mapuche_titles'],mm(st=.06,police=.03),money=1,desc='Document disappearances and repression and provide remedies for victims as civilian institutions recover.',event='truth',require=['Civilian government restored.','Past political repression has occurred.'])
node('civilian_compact','A Durable Civilian Compact','republic',2,10,['judicial_review','mapuche_titles'],mm(pp=.06,st=.03),desc='Secure reciprocal commitments to civilian succession and peaceful opposition.',require=['Civilian constitutional government.'])

group('development','Copper, Credit and National Development',26,0)
node('corfo_plan','CORFO Development Review','development',0,0,mods=mm(build=.04,bur=.02),desc='Audit public enterprises and direct scarce investment toward export capacity, food and transport.',icon='industry',days=21)
node('negotiated_copper','Negotiated Copper Ownership','development',-4,2,['corfo_plan'],mm(exp=.10,trade=.06,corp=-.02),money=4,desc='Settle compensation and retain supplier cooperation while consolidating Chilean public participation.',icon='copper')
node('national_copper','Full Copper Nationalization','development',0,2,['corfo_plan'],mm(exp=.16,res=-.03,trade=-.08),money=2,desc='Bring large-scale copper into public ownership while accepting management and compensation disputes.',icon='copper',event='copper')
node('concession_copper','Regulated Mining Concessions','development',4,2,['corfo_plan'],mm(exp=.08,build=.06,resist=-.06),money=1,desc='Attract private capital under royalty and reinvestment rules, trading some autonomy for new investment.',icon='copper')
ex('negotiated_copper','national_copper','concession_copper')
node('mine_engineers','Train Mine Engineers','development',0,4,[('negotiated_copper','national_copper','concession_copper')],mm(res=.03,edu=.04),money=2,desc='Expand mining engineering, maintenance and technical training so ownership reform can sustain production.',icon='research',remove=['specialists'],research=[('industry',.25,1)])
node('copper_stabilization','A Copper Stabilization Fund','development',-2,6,['mine_engineers'],mm(exp=-.04,int=-.75,st=.02),money=3,desc='Reserve part of export receipts against downturns instead of committing every windfall to current spending.',icon='bank')
node('export_reinvestment','Reinvest the Export Surplus','development',2,6,['mine_engineers'],mm(build=.08,int=.5),money=3,desc='Commit more export receipts immediately to production, accepting greater exposure to the next downturn.',icon='industry',buildings=[(472,'industrial_complex',1)])
ex('copper_stabilization','export_reinvestment')
node('rural_extension','Agricultural Extension','development',-6,4,['corfo_plan'],mm(ag=.06,edu=.02),money=2,desc='Send agronomists, credit officers and irrigation technicians to the reformed countryside.',icon='farm')
node('cooperative_titles','Secure Cooperative Titles','development',-8,6,['rural_extension'],mm(ag=.07,soc=.03),money=2,desc='Secure cooperative holdings and provide common machinery and working capital.',icon='farm',remove=['rural_conflict'])
node('family_farms','Secure Family Holdings','development',-4,6,['rural_extension'],mm(ag=.10,tax=-.02),money=2,desc='Give individual farmers secure holdings, with extension services and enforceable credit obligations.',icon='farm',remove=['rural_conflict'])
ex('cooperative_titles','family_farms')
node('cold_chain','Rural Storage and Transport','development',-6,8,[('cooperative_titles','family_farms')],mm(ag=.05,supply=-.03),money=3,desc='Reduce losses between farms, cities and export ports.',icon='farm',buildings=[(463,'agriculture_district',1)])
node('price_compact','A Wage and Price Compact','development',4,4,['corfo_plan'],mm(st=.04,corp=-.03,pp=-.03),money=1,desc='Negotiate a stabilization pact among employers, unions and the government.',icon='bank',remove=['inflation'])
node('monetary_restraint','Monetary Restraint','development',8,4,['corfo_plan'],mm(int=-.75,build=-.03,st=-.03),money=1,desc='Constrain monetary financing and public demand to restore credit confidence.',icon='bank',remove=['inflation'])
ex('price_compact','monetary_restraint')
node('prudential_banks','Prudential Bank Supervision','development',6,6,[('price_compact','monetary_restraint')],mm(int=-.25,corp=-.02,bur=.02),money=1,desc='Limit connected lending and foreign-currency exposure before a credit boom becomes a public liability.',icon='bank')
node('central_corridor','The Central Transport Corridor','development',0,8,[('copper_stabilization','export_reinvestment')],mm(infra=.08,supply=-.03),money=3,desc='Improve the central rail and road corridor linking production to ports.',icon='infra',remove=['long_coast'],buildings=[(468,'infrastructure',1)])
node('huachipato','Huachipato Supplier Network','development',-2,10,['central_corridor'],mm(out=.05,cap=.04),money=3,desc='Develop steelworking suppliers around existing industrial centers.',icon='industry',buildings=[(463,'industrial_complex',1)])
node('endesas_grid','ENDESA Grid Investment','development',2,10,['central_corridor'],mm(build=.04,infra=.04),money=3,weekly=.002,desc='Expand electricity supply for urban and industrial development.',icon='energy',buildings=[(468,'fossil_powerplant',1)])
node('pacific_ports','Pacific Export Terminals','development',6,8,['prudential_banks'],mm(exp=.06,trade=.03),money=3,weekly=.001,desc='Improve port handling and shipping reliability for a wider range of exports.',icon='navy',buildings=[(949,'infrastructure',1)])
node('forestry_exports','Forestry and Fruit Exports','development',4,10,['pacific_ports'],mm(ag=.06,exp=.03,tax=-.02),money=2,desc='Diversify exports with tax-supported incentives, inspection and rural infrastructure.',icon='forest',buildings=[(463,'agriculture_district',1)])
node('technical_universities','Technical Universities','development',0,12,['huachipato','endesas_grid'],mm(res=.03,edu=.04),money=3,desc='Connect regional technical institutes, public universities and industrial apprenticeships.',icon='research',research=[('computing_tech',.3,1)])

group('defence','The Armed Forces of a Pacific Republic',48,0)
node('professional_review','Professional Readiness Review','defence',0,0,mods=mm(org=.03,pers=.03),desc='Assess readiness across the three services without predetermining their political role.',icon='army',days=21)
node('andean_defence','Andean Territorial Defense','defence',-4,2,['professional_review'],mm(defense=.10,supply=-.06,speed=-.03),money=2,desc='Prioritize prepared mountain positions and reliable local supply over rapid offensive movement.',icon='army')
node('mobile_reserve','A Mobile Strategic Reserve','defence',0,2,['professional_review'],mm(speed=.08,rec=.06,supply=.06),money=3,desc='Build a mobile reserve able to reinforce distant fronts, accepting a larger logistical burden.',icon='army')
ex('andean_defence','mobile_reserve')
node('professional_cadres','Professional Cadres','defence',-4,4,[('andean_defence','mobile_reserve')],mm(org=.06,train=.08,pers=.05),money=2,desc='Retain experienced noncommissioned officers and lengthen unit training.',icon='army')
node('reserve_training','A Trained Reserve','defence',0,4,[('andean_defence','mobile_reserve')],mm(rec=.07,org=-.02,pers=.03),money=1,desc='Favor a broad reserve able to replenish formations over a smaller professional establishment.',icon='army')
ex('professional_cadres','reserve_training')
node('famae','FAMAE Maintenance Capacity','defence',-2,6,[('professional_cadres','reserve_training')],mm(gain=.06,arms=.05),money=3,desc='Expand repair, ammunition and maintenance capacity around FAMAE.',icon='industry',buildings=[(468,'arms_factory',1)])
node('standard_ammunition','Standardized Ammunition','defence',-2,8,['famae'],mm(arty=.06,cap=.04,gain=-.03),money=1,desc='Concentrate production on fewer ammunition standards and more consistent artillery supply.',icon='army')
node('coastal_denial','Coastal Denial Doctrine','defence',4,2,['professional_review'],mm(navy=.08,dock=.04,air=-.02),money=2,desc='Protect ports and sea approaches through a concentrated coastal defense posture.',icon='navy')
node('ocean_escort','Ocean Escort Doctrine','defence',8,2,['professional_review'],mm(navy=.05,trade=.05,pers=.04),money=3,desc='Invest in sustained escort operations to protect a long maritime trading network.',icon='navy')
ex('coastal_denial','ocean_escort')
node('asmar','ASMAR Dockyard Capacity','defence',6,4,[('coastal_denial','ocean_escort')],mm(dock=.05),money=3,weekly=.0015,desc='Expand naval construction and refit capacity at Talcahuano.',icon='navy',buildings=[(463,'dockyard',1)])
node('naval_training','Naval Training Missions','defence',6,6,['asmar'],mm(navy=.04,pers=.02),money=1,desc='Improve damage control, engineering and combined fleet exercises.',icon='navy',research=[('naval_equipment',.25,1)])
node('air_interception','Airspace Interception','defence',-6,10,['standard_ammunition'],mm(detect=.12,air=.04),money=2,weekly=.001,desc='Improve radar coverage and the readiness of interceptor squadrons.',icon='air',buildings=[(472,'radar_station',1)])
node('tactical_air','Tactical Air Cooperation','defence',-2,10,['standard_ammunition'],mm(air=.08,supply=.03),money=2,desc='Train air crews and ground formations to coordinate reconnaissance and tactical support.',icon='air',research=[('air_equipment',.25,1)])
ex('air_interception','tactical_air')
node('enaer','ENAER Industrial Foundations','defence',-4,12,[('air_interception','tactical_air')],mm(arms=.05,res=.015),money=3,desc='Develop the engineering and maintenance base for a national aeronautical industry.',icon='air',research=[('air_equipment',.25,1)])
node('joint_staff','A Joint Professional Staff','defence',2,10,['standard_ammunition','naval_training'],mm(org=.04,navy=.03,bur=.02),money=1,desc='Standardize operational planning while keeping service commands accountable to the lawful government.',icon='army')

# Each party starts with a useful policy, not a focus unlocking its own government.
add_programme('pdc','Christian Democratic Reform',1,74,0,[
('pdc_social','Community Social Development',0,0,(),mm(st=.04,soc=.03),2,.001,'Fund neighbourhood organizations, housing services and local social provision.',{'icon':'social'}),
('pdc_frei','Consolidate Frei\'s Reforms',-4,2,('pdc_social',),mm(ag=.06,st=.02,corp=-.03),2,0,'Consolidate legal land reform and a negotiated mixed economy.',{'icon':'farm'}),
('pdc_tomic','Tomic\'s Popular Convergence',4,2,('pdc_social',),mm(ag=.09,pp=.06,trade=-.04),2,0,'Seek a wider reform alliance with the democratic left, accepting business and centrist resistance.',{'icon':'politics'}),
('pdc_school','The Education Reform',-4,4,('pdc_frei',),mm(res=.035,edu=.05),2,0,'Extend secondary and technical education beyond the established urban schools.',{'icon':'research'}),
('pdc_coops','Peasant Cooperatives',4,4,('pdc_tomic',),mm(ag=.07,soc=.04),2,0,'Back cooperatives with machinery, credit and trained rural organizers.',{'icon':'farm'}),
('pdc_centre','An Independent Christian Center',-6,6,('pdc_school',),mm(resist=.08,pp=.08,st=-.02),0,0,'Preserve an independent center able to negotiate with either parliamentary bloc.'),
('pdc_business','A Social Partnership',-2,6,('pdc_school',),mm(corp=.06,st=.03,soc=.03),1,0,'Trade predictable investment rules for employer support of social provision.'),
('pdc_unions','Christian Trade Unionism',2,6,('pdc_coops',),mm(st=.05,out=.04,corp=-.03),1,0,'Strengthen autonomous Christian unions within an organized labor movement.'),
('pdc_left','A Democratic Reform Coalition',6,6,('pdc_coops',),mm(pp=.12,st=.03,bur=.04),1,0,'Share policy authority with the democratic left rather than governing through a narrow party machine.'),
('pdc_housing','A Ministry for the Neighbourhoods',0,8,(('pdc_centre','pdc_business','pdc_unions','pdc_left'),),mm(st=.04,health=.04),3,.001,'Link housing settlements to clinics and public services.',{'icon':'social'}),
('pdc_enterprise','Community Enterprises',-2,10,('pdc_housing',),mm(out=.06,gain=.04,bur=.03),3,0,'Finance worker and community enterprises within a plural economy.',{'icon':'industry','buildings':[(468,'industrial_complex',1)]}),
('pdc_church','Church and Civic Reconciliation',2,10,('pdc_housing',),mm(st=.05,pp=-.03),1,0,'Support independent civic mediation across polarized communities.',{'icon':'social'}),
('pdc_aylwin','A Civilian Coalition for Chile',0,12,('pdc_enterprise','pdc_church'),mm(st=.05,resist=.05,soc=.02),0,0,'Build a governing coalition committed to peaceful succession and enforceable civil rights.')])
ex('pdc_frei','pdc_tomic');ex('pdc_centre','pdc_business');ex('pdc_unions','pdc_left')

add_programme('pn','National Party and Civilian Conservatism',2,90,0,[
('pn_investment','Guarantees for Productive Investment',0,0,(),mm(build=.06,corp=.03,st=-.02),1,0,'Give private investment predictable rules while retaining parliamentary government.',{'icon':'industry'}),
('pn_alessandri','Alessandri\'s Fiscal Republic',-4,2,('pn_investment',),mm(int=-.75,bur=-.05,soc=-.03,st=-.03),1,0,'Restrain spending and restore private credit through a civilian fiscal programme.',{'icon':'bank'}),
('pn_jarpa','Jarpa\'s National Development',4,2,('pn_investment',),mm(out=.07,cap=.04,trade=-.06),2,0,'Favor domestic producers and provincial industry over a rapid opening of imports.',{'icon':'industry'}),
('pn_compensation','Compensation and Property Courts',-4,4,('pn_alessandri',),mm(corp=.06,st=.02,bur=.03),2,0,'Resolve expropriation claims through compensation and ordinary courts.'),
('pn_suppliers','National Supplier Contracts',4,4,('pn_jarpa',),mm(gain=.06,civ=.05,bur=.02),3,0,'Reserve development contracts for qualified domestic suppliers.',{'icon':'industry','buildings':[(468,'industrial_complex',1)]}),
('pn_liberal','Competitive Private Enterprise',-6,6,('pn_compensation',),mm(build=.08,tax=-.03,trade=.04),2,0,'Favor competition and lower entry barriers while accepting lower immediate tax yield.'),
('pn_social','Conservative Social Provision',-2,6,('pn_compensation',),mm(st=.06,soc=.06),2,.001,'Protect pensions and family assistance to broaden the conservative mandate.',{'icon':'social'}),
('pn_agrarian','Commercial Agriculture',2,6,('pn_suppliers',),mm(ag=.12,corp=.03,st=-.04),2,0,'Prioritize commercially viable farming and private investment over further redistribution.',{'icon':'farm'}),
('pn_provincial','Provincial Industrial Credit',6,6,('pn_suppliers',),mm(out=.07,int=.25),3,0,'Direct credit to provincial manufacturers even where private finance is reluctant.',{'icon':'industry'}),
('pn_compact','A Constitutional Right',0,8,(('pn_liberal','pn_social','pn_agrarian','pn_provincial'),),mm(pp=.08,resist=.06),0,0,'Bind the civilian right to elections and reject an autonomous military political mandate.'),
('pn_portfolio','Diversify the Export Portfolio',-2,10,('pn_compact',),mm(exp=.06,ag=.04,bur=.02),3,0,'Develop agricultural and manufacturing exports alongside copper.',{'icon':'forest'}),
('pn_policing','Accountable Public Order',2,10,('pn_compact',),mm(st=.04,police=.04),1,0,'Improve police readiness under civilian legal supervision.'),
('pn_republic','A Conservative Electoral Mandate',0,12,('pn_portfolio','pn_policing'),mm(st=.04,corp=.04,soc=.02),0,0,'Consolidate a conservative programme that can survive the next competitive election.')])
ex('pn_alessandri','pn_jarpa');ex('pn_liberal','pn_social');ex('pn_agrarian','pn_provincial')

add_programme('pr','Radical Republicanism',3,106,0,[
('pr_teachers','The Teachers\' Republic',0,0,(),mm(res=.025,edu=.04),2,0,'Rebuild the Radical tradition of public education and secular civic service.',{'icon':'research'}),
('pr_baltra','Baltra\'s Planned Development',-4,2,('pr_teachers',),mm(out=.06,civ=.05,bur=.04),3,0,'Use planning and public investment to integrate a plural left governing coalition.',{'icon':'industry'}),
('pr_bridge','A Republican Center-Left',4,2,('pr_teachers',),mm(pp=.12,st=.04,corp=-.02),1,0,'Seek a constitutional center-left coalition with clear limits on unilateral executive action.'),
('pr_corfo','CORFO Regional Projects',-4,4,('pr_baltra',),mm(cap=.05,build=.04),3,.001,'Expand selected regional industrial projects through the development corporation.',{'icon':'industry','buildings':[(463,'industrial_complex',1)]}),
('pr_provinces','The Provincial Civil Service',4,4,('pr_bridge',),mm(bur=-.06,st=.03),2,0,'Strengthen professional administration beyond Santiago.'),
('pr_secular','Secular Public Schools',-6,6,('pr_corfo',),mm(res=.04,edu=.05,st=-.02),2,0,'Direct scarce education funds toward a common secular public system.',{'icon':'research'}),
('pr_plural','Plural Education Agreements',-2,6,('pr_corfo',),mm(res=.025,st=.04,edu=.06),2,0,'Fund public education alongside agreed provision by independent institutions.',{'icon':'research'}),
('pr_planning','An Independent Planning Office',2,6,('pr_provinces',),mm(build=.08,bur=.04,pp=-.03),2,0,'Insulate investment planning from immediate party patronage.',{'icon':'industry'}),
('pr_parliament','Parliamentary Budget Control',6,6,('pr_provinces',),mm(int=-.5,tax=.04,pp=-.04),1,0,'Give parliamentary committees real leverage over expenditure and borrowing.',{'icon':'bank'}),
('pr_health','Provincial Hospitals',0,8,(('pr_secular','pr_plural','pr_planning','pr_parliament'),),mm(st=.05,health=.06),3,.001,'Improve access to health care in the provincial republic.',{'icon':'social'}),
('pr_pluralist','A Pluralist Development State',0,10,('pr_health',),mm(out=.04,pp=.05,bur=.02),0,0,'Keep the development state accountable to a competitive parliamentary coalition.')])
ex('pr_baltra','pr_bridge');ex('pr_secular','pr_plural');ex('pr_planning','pr_parliament')

add_programme('ps','The Socialist Party and the Chilean Road',18,122,0,[
('ps_milk','The National Nutrition Programme',0,0,(),mm(st=.05,health=.04,soc=.03),2,.002,'Provide milk and basic nutrition through schools and public health services.',{'icon':'social'}),
('ps_allende','Allende\'s Constitutional Road',-4,2,('ps_milk',),mm(st=.05,pp=.08,bur=.02),1,0,'Seek a durable socialist mandate through constitutional guarantees and broad electoral support.'),
('ps_cordones','The Industrial Cordons',4,2,('ps_milk',),mm(out=.10,org=-.03,st=-.04),2,0,'Empower industrial coordination committees, accepting a sharper confrontation over authority.',{'icon':'industry'}),
('ps_mixed','A Negotiated Social Property Area',-4,4,('ps_allende',),mm(corp=.04,out=.04,exp=-.02),3,0,'Negotiate the boundaries of public, mixed and private enterprise to keep production and credit flowing.',{'icon':'industry'}),
('ps_control','Workers\' Management Councils',4,4,('ps_cordones',),mm(out=.07,gain=.05,bur=.05),2,0,'Make worker councils responsible for management and production targets.',{'icon':'industry'}),
('ps_cybersyn','Project Cybersyn',-6,6,('ps_mixed',),mm(res=.025,cap=.06,edu=.04),3,.001,'Use telex networks and industrial reporting to coordinate public enterprises.',{'icon':'research','research':[('computing_tech',.35,1)]}),
('ps_decentral','Regional Economic Councils',-2,6,('ps_mixed',),mm(build=.07,st=.03,bur=.04),2,0,'Delegate development priorities to regional councils instead of concentrating every decision in Santiago.'),
('ps_bargain','A Production Bargain with the CUT',2,6,('ps_control',),mm(out=.05,st=.04,soc=.05),1,0,'Trade enforceable social guarantees for agreed production and wage targets.'),
('ps_mobilization','Permanent Popular Mobilization',6,6,('ps_control',),mm(pp=.15,resist=.08,st=-.06,trade=-.04),1,0,'Rely on mass organizations to sustain the government through confrontation.'),
('ps_housing','Housing through Public Enterprise',0,8,(('ps_cybersyn','ps_decentral','ps_bargain','ps_mobilization'),),mm(st=.04,civ=.06,soc=.04),3,.001,'Link public construction and industrial supply to a national housing effort.',{'icon':'social','buildings':[(468,'industrial_complex',1)]}),
('ps_supply','Democratic Distribution Boards',-2,10,('ps_housing',),mm(supply=-.05,ag=.05,bur=.04),2,0,'Make neighborhood distribution accountable and link it to food supply.',{'icon':'farm'}),
('ps_coexistence','A Pact for Democratic Coexistence',2,10,('ps_housing',),mm(st=.07,pp=-.04,trade=.04),1,0,'Accept reciprocal constitutional limits in exchange for recognition of the social programme.'),
('ps_chilean_road','A Sustainable Chilean Road',0,12,('ps_supply','ps_coexistence'),mm(out=.04,st=.04,soc=.02),0,0,'Preserve social gains through a viable, plural and politically accountable economy.')])
ex('ps_allende','ps_cordones');ex('ps_cybersyn','ps_decentral');ex('ps_bargain','ps_mobilization')

add_programme('pcch','Communist Organization and Popular Unity',4,138,0,[
('pcch_unions','The Organized Labour Republic',0,0,(),mm(out=.04,st=.03,soc=.03),1,0,'Build a disciplined production agreement with organized labor and the broader left.',{'icon':'industry'}),
('pcch_front','The Broad Parliamentary Front',-4,2,('pcch_unions',),mm(pp=.10,st=.05,bur=.02),1,0,'Keep Popular Unity open to non-Marxist partners and defend electoral organization.'),
('pcch_cadres','A Party of Industrial Cadres',4,2,('pcch_unions',),mm(cap=.08,gain=.04,pp=-.03),2,0,'Concentrate trained organizers in mines, factories and public enterprises.',{'icon':'industry'}),
('pcch_soviet','Soviet Technical Standards',-4,4,('pcch_front',),mm(res=.025,cap=.04,resist=-.04),2,0,'Adapt supplier standards and technical training to Soviet cooperation.',{'icon':'research'}),
('pcch_domestic','A Domestic Machinery Network',4,4,('pcch_cadres',),mm(out=.06,gain=.04,trade=-.03),3,0,'Build domestic repair and machinery networks instead of relying on a single foreign supplier.',{'icon':'industry','buildings':[(468,'industrial_complex',1)]}),
('pcch_cautious','Production before New Acquisitions',-6,6,('pcch_soviet',),mm(out=.07,trade=.03,pp=-.03),1,0,'Prioritize operating existing public enterprises before widening the social property area.'),
('pcch_public','Consolidate the Public Sector',-2,6,('pcch_soviet',),mm(corp=.07,cap=.06,bur=.05),3,0,'Concentrate investment and management within a larger public-enterprise system.'),
('pcch_local','Autonomous Union Bargaining',2,6,('pcch_domestic',),mm(st=.06,out=.02,soc=.04),1,0,'Preserve bargaining autonomy for organized workers within a left government.'),
('pcch_plan','Binding Production Agreements',6,6,('pcch_domestic',),mm(out=.09,gain=.03,st=-.04),1,0,'Enforce production obligations across public enterprises and organized labor.'),
('pcch_literacy','Workers\' Technical Institutes',0,8,(('pcch_cautious','pcch_public','pcch_local','pcch_plan'),),mm(res=.035,edu=.05),2,.001,'Make technical education accessible to industrial workers and their families.',{'icon':'research'}),
('pcch_pluralism','Popular Unity without a Single Party',0,10,('pcch_literacy',),mm(pp=.05,st=.05,bur=.02),0,0,'Retain a coalition of distinct parties rather than equating socialist development with one-party rule.')])
ex('pcch_front','pcch_cadres');ex('pcch_cautious','pcch_public');ex('pcch_local','pcch_plan')

add_programme('mapu','MAPU and Agrarian Socialism',19,154,0,[
('mapu_extension','Reform from the Countryside',0,0,(),mm(ag=.06,edu=.02),2,0,'Deploy agrarian reform technicians and young professionals alongside peasant organizations.',{'icon':'farm'}),
('mapu_technicians','Chonchol\'s Agrarian Administration',-4,2,('mapu_extension',),mm(ag=.10,bur=.04),2,0,'Make technical support, credit and accountable administration the core of agrarian change.',{'icon':'farm'}),
('mapu_popular','Popular Agrarian Power',4,2,('mapu_extension',),mm(pp=.12,ag=.06,st=-.04),1,0,'Give organized peasants greater authority over the pace and institutions of reform.',{'icon':'farm'}),
('mapu_technical','Cooperative Machinery Pools',-4,4,('mapu_technicians',),mm(ag=.07,cap=.03),3,.001,'Finance common machinery and trained maintenance teams.',{'icon':'farm','buildings':[(463,'agriculture_district',1)]}),
('mapu_land','Land Councils and Legal Titles',4,4,('mapu_popular',),mm(st=.03,ag=.05,bur=.03),1,0,'Make peasant councils responsible for durable titles and conflict resolution.',{'icon':'land'}),
('mapu_christian','Christian Social Radicalism',-6,6,('mapu_technical',),mm(st=.06,health=.04),1,0,'Retain a bridge to Catholic social institutions and the reformist Christian left.',{'icon':'social'}),
('mapu_marxist','An Independent Marxist Programme',-2,6,('mapu_technical',),mm(out=.07,resist=.05,trade=-.04),1,0,'Define an independent Marxist programme beyond Christian Democracy or Soviet tutelage.'),
('mapu_local','Local Cooperative Autonomy',2,6,('mapu_land',),mm(ag=.08,st=.03,tax=-.02),1,0,'Allow local cooperatives discretion over output and retained earnings.',{'icon':'farm'}),
('mapu_delivery','National Food Delivery Contracts',6,6,('mapu_land',),mm(ag=.05,supply=-.05,bur=.04),2,0,'Bind cooperatives to food delivery contracts while improving transport and storage.',{'icon':'farm'}),
('mapu_service','Rural Schools and Clinics',0,8,(('mapu_christian','mapu_marxist','mapu_local','mapu_delivery'),),mm(res=.02,health=.04,edu=.03),2,.001,'Bring health care and technical schooling into the reformed countryside.',{'icon':'social'}),
('mapu_reform','A Productive Agrarian Settlement',0,10,('mapu_service',),mm(ag=.05,st=.04,soc=.02),0,0,'Build a durable settlement around productive land, secure rights and rural institutions.',{'icon':'farm'})])
ex('mapu_technicians','mapu_popular');ex('mapu_christian','mapu_marxist');ex('mapu_local','mapu_delivery')

# Smaller real parties retain compact programmes rather than being inflated into great powers.
add_programme('dr','Radical Democracy',14,74,17,[
('dr_republic','A Secular Republican Center',0,0,(),mm(pp=.08,st=.03),1,0,'Offer a secular, anti-communist parliamentary alternative rooted in the provincial middle classes.'),
('dr_independent','An Independent Republican Bloc',-3,2,('dr_republic',),mm(pp=.10,resist=.06,st=-.02),0,0,'Defend an independent center rather than merging with the National Party.'),
('dr_alliance','A Civilian Center-Right Accord',3,2,('dr_republic',),mm(corp=.05,st=.04,bur=.02),1,0,'Negotiate a civilian coalition with the electoral right.'),
('dr_schools','Public Schools and Examinations',0,4,(('dr_independent','dr_alliance'),),mm(res=.025,bur=-.03,edu=.04),2,0,'Defend secular schools and professional entry to public service.',{'icon':'research'}),
('dr_small_business','Credit for Small Proprietors',-3,6,('dr_schools',),mm(corp=.06,build=.03,tax=-.02),2,0,'Finance small commercial and productive firms without wholesale privatization.',{'icon':'bank'}),
('dr_public','A Reformed Mixed Economy',3,6,('dr_schools',),mm(out=.05,civ=.05,bur=.03),3,0,'Keep a mixed economy under stricter public accounting.',{'icon':'industry','buildings':[(463,'industrial_complex',1)]}),
('dr_provincial','Provincial Municipal Services',0,8,(('dr_small_business','dr_public'),),mm(st=.05,soc=.04),2,.001,'Give provincial municipalities a funded service programme.',{'icon':'social'}),
('dr_constitution','Republican Succession',0,10,('dr_provincial',),mm(st=.04,pp=.05,bur=.01),0,0,'Preserve the parliamentary republic and competitive civilian succession.')])
ex('dr_independent','dr_alliance');ex('dr_small_business','dr_public')

add_programme('padena','PADENA and Provincial Populism',20,90,17,[
('padena_provinces','The Forgotten Provinces',0,0,(),mm(st=.04,soc=.03),2,.001,'Address small farmers, pensioners and employees outside the metropolitan party networks.',{'icon':'social'}),
('padena_coops','A Small-Farmer Credit Bank',-3,2,('padena_provinces',),mm(ag=.10,int=.25),2,0,'Protect small farmers with public credit and common purchasing.',{'icon':'farm'}),
('padena_enterprise','Provincial Enterprise Funds',3,2,('padena_provinces',),mm(civ=.07,corp=.04,bur=.03),3,0,'Back small provincial manufacturers and transport firms.',{'icon':'industry','buildings':[(463,'industrial_complex',1)]}),
('padena_integrity','Public Accounts and Clean Contracts',0,4,(('padena_coops','padena_enterprise'),),mm(bur=-.04,pp=.05),1,0,'Audit local contracts and patronage rather than promise an unexplained end to corruption.'),
('padena_pensions','Protect Pensioner Incomes',-3,6,('padena_integrity',),mm(st=.07,soc=.07),2,.001,'Fund pension protection as a visible social commitment.',{'icon':'social'}),
('padena_roads','A Provincial Roads Programme',3,6,('padena_integrity',),mm(infra=.12,soc=-.02),3,0,'Direct the available budget toward transport links and market access.',{'icon':'infra','buildings':[(463,'infrastructure',1)]}),
('padena_bargain','A Provincial Coalition Bargain',0,8,(('padena_pensions','padena_roads'),),mm(pp=.10,st=.03,bur=.02),0,0,'Turn provincial representation into a negotiated civilian governing coalition.')])
ex('padena_coops','padena_enterprise');ex('padena_pensions','padena_roads')

add_programme('gremial','Gremialist Institutional Conservatism',0,106,17,[
('gremial_guilds','Professional and Civic Associations',0,0,(),mm(cap=.04,pp=.06,st=-.02),1,0,'Bring professional and university associations into a conservative institutional programme.'),
('gremial_subsidiary','The Subsidiary State',-4,2,('gremial_guilds',),mm(build=.08,bur=-.05,tax=-.03),2,0,'Delegate provision to private and civic institutions while limiting direct state management.'),
('gremial_corporate','A Corporatist Social Compact',4,2,('gremial_guilds',),mm(out=.07,st=.03,pp=-.04),2,0,'Organize negotiated representation through professional and employer bodies.'),
('gremial_schools','Independent Education Providers',-4,4,('gremial_subsidiary',),mm(res=.03,edu=-.03,st=-.03),2,0,'Shift provision toward independent institutions while accepting unequal access.',{'icon':'research'}),
('gremial_social','Civic Social Provision',4,4,('gremial_corporate',),mm(st=.05,soc=.05),2,.001,'Finance civic organizations to provide family and neighborhood services.',{'icon':'social'}),
('gremial_tutelage','A Protected Constitutional Order',-4,6,('gremial_schools',),mm(resist=.10,pp=.10,st=-.06,trade=-.04),1,0,'Entrench institutional vetoes against elected opponents, accepting a continuing legitimacy conflict.'),
('gremial_electoral','An Electoral Conservative Party',0,6,(('gremial_schools','gremial_social'),),mm(st=.06,corp=.04,pp=-.03),1,0,'Transform the movement into an accountable electoral organization.'),
('gremial_guildrule','Functional Representation',4,6,('gremial_social',),mm(cap=.07,bur=-.04,st=-.05),1,0,'Prioritize organized professional representation over open partisan competition.'),
('gremial_continuity','Institutional Conservative Continuity',0,8,(('gremial_tutelage','gremial_electoral','gremial_guildrule'),),mm(build=.04,resist=.04,soc=.02),0,0,'Consolidate the selected institutional settlement without erasing its constitutional liabilities.')])
ex('gremial_subsidiary','gremial_corporate');ex('gremial_tutelage','gremial_electoral','gremial_guildrule')

add_programme('mir','MIR and the Revolutionary Left',5,122,17,[
('mir_organize','Popular Organization in the Settlements',0,0,(),mm(pp=.10,st=-.03,soc=.02),1,0,'Organize marginalized urban and rural communities around a revolutionary programme.'),
('mir_civil','An Independent Popular Left',-4,2,('mir_organize',),mm(st=.04,out=.04,bur=.03),2,0,'Seek a legal mass organization independent of both traditional parliamentary parties and foreign tutelage.'),
('mir_vanguard','The Revolutionary Vanguard',4,2,('mir_organize',),mm(org=.06,resist=.08,st=-.08,trade=-.08),2,0,'Build a disciplined revolutionary governing structure amid continuing domestic confrontation.',{'icon':'army'}),
('mir_selfmanagement','Settlement Self-Management',-4,4,('mir_civil',),mm(st=.05,build=.05,tax=-.03),2,0,'Give elected settlement committees responsibility for local public works.',{'icon':'social'}),
('mir_territorial','Territorial Defense Committees',4,4,('mir_vanguard',),mm(defense=.08,supply=.04,police=.05),2,0,'Organize territorial defense through the state while imposing larger security and supply burdens.',{'icon':'army'}),
('mir_agreement','A Plural Popular Congress',-4,6,('mir_selfmanagement',),mm(pp=.08,st=.05,bur=.03),1,0,'Accept a plural political settlement with organized left parties and independent communities.'),
('mir_command','Central Revolutionary Command',0,6,(('mir_selfmanagement','mir_territorial'),),mm(out=.08,org=.03,st=-.05),2,0,'Concentrate production and security authority in the revolutionary state.'),
('mir_nonalign','An Independent Revolutionary Republic',4,6,('mir_territorial',),mm(resist=.10,exp=-.05,trade=-.04),1,0,'Reject external political tutelage while bearing a narrower diplomatic and commercial base.'),
('mir_clinics','Community Schools and Clinics',0,8,(('mir_agreement','mir_command','mir_nonalign'),),mm(res=.025,health=.05,edu=.04),2,.001,'Consolidate material social provision within the selected revolutionary settlement.',{'icon':'social'})])
ex('mir_civil','mir_vanguard');ex('mir_agreement','mir_command','mir_nonalign')

add_programme('military','The Military Government and Pinochet',22,142,17,[
('military_staff','The Service Chiefs\' Administration',0,0,(),mm(org=.04,bur=.04,st=-.04),1,0,'Establish the joint administration after a real military transfer of power.',{'require':['Military government has actually taken office.'],'icon':'army'}),
('military_constitution','A Constitutional Military Exit',-6,2,('military_staff',),mm(st=.07,pp=-.06,pers=.04),1,0,'Set enforceable limits on military rule and open negotiations for an early civilian transfer.',{'require':['A constitutionalist military leadership.']}),
('pinochet_command','Pinochet\'s Personal Command',2,2,('military_staff',),mm(pp=.15,org=.05,st=-.06,res=-.025),0,0,'Concentrate the junta presidency in Augusto Pinochet and bear the institutional consequences.',{'require':['Augusto Pinochet is the actual national leader.']}),
('military_ballot','Guarantee a Civilian Ballot',-6,4,('military_constitution',),mm(st=.06,pp=-.04,bur=.03),1,0,'Restore civilian electoral organization under agreed military withdrawal terms.',{'event':'early_exit'}),
('pinochet_chicago','The Chicago Programme',-2,4,('pinochet_command',),mm(build=.10,int=-.75,st=-.08,trade=.05),3,0,'Apply rapid trade, price and market reforms while bearing severe adjustment and social conflict.',{'icon':'bank','event':'adjustment'}),
('pinochet_state','Strategic State Capitalism',6,4,('pinochet_command',),mm(out=.08,cap=.06,bur=.05,trade=-.03),4,0,'Retain strategic public firms and selective protection rather than adopt a comprehensive market opening.',{'icon':'industry','buildings':[(468,'industrial_complex',1)]}),
('pinochet_pensions','Private Pension Capitalization',-4,6,('pinochet_chicago',),mm(corp=.07,soc=-.05,st=-.04),2,0,'Redirect pension contributions toward private capitalization with a difficult transition burden.',{'icon':'bank'}),
('pinochet_floor','A Funded Social Floor',0,6,('pinochet_chicago',),mm(st=.07,soc=.07,corp=-.02),2,.002,'Retain social protection while pursuing the market programme.',{'icon':'social'}),
('pinochet_codelco','Retain Public Copper',4,6,('pinochet_state',),mm(exp=.10,pers=.04),3,0,'Retain copper revenues under public ownership and sustain military fiscal claims.',{'icon':'copper'}),
('pinochet_private','Mixed Strategic Enterprises',8,6,('pinochet_state',),mm(build=.07,cap=.04,resist=-.05),2,0,'Invite private partners into strategic enterprises while retaining state leverage.',{'icon':'industry'}),
('pinochet_crisis','Banking and External Debt Review',2,8,(('pinochet_pensions','pinochet_floor','pinochet_codelco','pinochet_private'),),mm(bur=.03),1,0,'Review banks and external exposure before deciding how to distribute the costs of a credit crisis.',{'event':'banking','icon':'bank'}),
('pinochet_rescue','Public Bank Intervention',0,10,('pinochet_crisis',),mm(build=.08,int=.5,tax=-.03),6,.003,'Stabilize lending through public intervention and assume a substantial fiscal burden.',{'icon':'bank','require':['A banking crisis is active.']}),
('pinochet_losses','Impose Creditor Losses',4,10,('pinochet_crisis',),mm(int=-.5,build=-.06,st=-.05),2,0,'Limit public rescue costs by imposing losses and accepting a sharper immediate contraction.',{'icon':'bank','require':['A banking crisis is active.']}),
('pinochet_supervision','Prudential Reform before a Crisis',8,10,('pinochet_crisis',),mm(int=-.25,corp=-.03,bur=.03),2,0,'Reduce connected lending and currency exposure while restricting the credit boom.',{'icon':'bank','require':['No active banking crisis.']}),
('pinochet_pragmatic','Pragmatic Export Recovery',2,12,(('pinochet_rescue','pinochet_losses','pinochet_supervision'),),mm(exp=.07,ag=.05,soc=.03),3,0,'Support export recovery and targeted intervention without erasing the costs of the previous programme.',{'icon':'forest'}),
('pinochet_technocrat','Technocratic Constitutional Rule',-2,14,('pinochet_pragmatic',),mm(build=.06,pp=.08,st=-.04),1,0,'Entrench a managed constitutional succession and restricted political competition.'),
('pinochet_security','The National Security State',2,14,('pinochet_pragmatic',),mm(resist=.12,org=.05,st=-.10,res=-.04,trade=-.08,police=.10),2,.002,'Preserve coercive political control at the cost of rights, expertise, international standing and legitimacy.'),
('pinochet_plebiscite','An Enforceable Plebiscite',6,14,('pinochet_pragmatic',),mm(st=.08,pp=-.08,bur=.03),1,0,'Permit credible registration, campaigning and scrutiny under an agreed transfer procedure.',{'event':'plebiscite'}),
('pinochet_handover','Negotiate the Civilian Handover',6,16,('pinochet_plebiscite',),mm(st=.06,pers=.03),1,0,'Implement the civilian electoral result and negotiated constitutional guarantees.',{'event':'handover','require':['The plebiscite rejected continued military rule.']}),
('pinochet_continuity','A Contested Military Continuation',0,16,(('pinochet_technocrat','pinochet_security'),),mm(pp=.06,st=-.04,police=.04),0,0,'Maintain military rule under the selected institutional settlement and its unresolved legitimacy conflict.')])
ex('military_constitution','pinochet_command');ex('pinochet_chicago','pinochet_state');ex('pinochet_pensions','pinochet_floor');ex('pinochet_codelco','pinochet_private');ex('pinochet_rescue','pinochet_losses','pinochet_supervision');ex('pinochet_technocrat','pinochet_security','pinochet_plebiscite')

# Reciprocal offers. Both countries' exact terms are always visible, including while unavailable.
group('diplomacy','Agreements across the Pacific and the Andes',48,17)
node('diplomatic_service','A Professional Diplomatic Service','diplomacy',0,0,mods=mm(trade=.04,bur=.02),money=1,desc='Give Chile the capacity to negotiate with its neighbors and competing Cold War partners.',days=21)
def agreement(key,title,partner,x,y,parents,chile,other,setup_chl,setup_other,wk_chl,wk_other,desc,source,buildings=(),require=(),research=()):
    a=dict(id=P+key,partner=partner,title=title,description=desc,source=source,perpetual=True,pending_days=90,
       chile=dict(spirit=title+': Chile',modifiers=chile,setup=setup_chl,weekly=wk_chl),
       recipient=dict(spirit=title+': '+partner,modifiers=other,setup=setup_other,weekly=wk_other),
       buildings=[dict(country=c,state=s,type=t,levels=l,slots=l) for c,s,t,l in buildings],research=[dict(country=c,category=cat,bonus=b,uses=u) for c,cat,b,u in research],
       decision='Consider the '+title,requirements=list(require),conditions=['Both countries exist.','Both countries have ratified the agreement.','The two countries are at peace with one another.','Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.'],
       implementation='New Chile offer/recipient-decision/synchronization definitions required; use the verified existing MD/Imperia APIs. Fees and assets execute once on acceptance. Both named spirits and weekly flows suspend together and restore without repeating setup. Recipient may refuse. Refusal/90-day expiry has no effect beyond notification; resubmission of the same unratified proposal is permitted after 180 days, without replaying the focus.')
    D['agreements'].append(a)
    n=node(key,title,'diplomacy',x,y,parents,desc=desc,icon='diplomacy',require=require,days=35)
    n['agreement']=a['id'];return a
agreement('usa_mines','Copper Compensation and Engineering','USA',-6,2,['diplomatic_service'],mm(cap=.06,exp=.07,resist=-.04),mm(corp=.015,trade=.02,bur=.01),4,1,.002,.001,'Offer a compensation settlement and technical partnership for the copper industry.','Frei negotiated copper ownership; exact reciprocal contract is alternate-history RP terms.',research=[('CHL','industry',.25,1)])
agreement('soviet_machinery','Soviet Machinery and Technical Credit','SOV',-2,2,['diplomatic_service'],mm(out=.06,cap=.05,resist=-.04),mm(exp=.02,influence=.03,bur=.01),2,3,.003,.001,'Propose machinery deliveries and technical training backed by reciprocal commitments.','Allende visited Moscow in 1972; Soviet supplier credit existed, exact project and price are proposed.',buildings=[('CHL',468,'industrial_complex',1)])
agreement('japan_copper','Pacific Copper Supply and Port Equipment','JAP',2,2,['diplomatic_service'],mm(exp=.08,trade=.04,corp=-.02),mm(out=.02,trade=.03,bur=.01),3,2,.0015,.001,'Offer long-term copper sales in exchange for port equipment and industrial cooperation.','Japan was a diversification partner; this named contract is plausible alternate history.',buildings=[('CHL',949,'infrastructure',1)])
agreement('cuba_clinics','Chilean-Cuban Public Health Exchange','CUB',6,2,['diplomatic_service'],mm(res=.02,health=.03,trade=-.02),mm(res=.01,influence=.03,health=.03),1,1,.001,.0005,'Offer a reciprocal programme of medical training, public health and clinical exchange.','Castro visited Chile in 1971; this specific exchange and reciprocal costs are proposed.',require=['Diplomatic relations with Cuba.'])
agreement('argentina_beagle','Beagle Peace and Maritime Cooperation','ARG',-6,6,['diplomatic_service'],mm(st=.03,supply=-.04,trade=.04,bur=.02),mm(st=.03,supply=-.04,trade=.04,bur=.02),2,2,.001,.001,'Offer a mutually ratified settlement, maritime confidence measures and border cooperation.','1979 papal mediation and the 1984 Treaty of Peace and Friendship; exact economic terms are proposed.',require=['Both governments accept the negotiated maritime settlement.'])
agreement('peru_maritime','Peruvian-Chilean Maritime Confidence Measures','PRU',-2,6,['diplomatic_service'],mm(supply=-.03,trade=.05,bur=.02),mm(supply=-.03,trade=.05,bur=.02),1,1,.0005,.0005,'Offer incident prevention, port contacts and transparent notification of exercises.','Regional tensions and Andean cooperation are historical; this bilateral protocol is alternate history.')
agreement('bolivia_transit','Bolivian-Chilean Transit Facilities','BOL',2,6,['diplomatic_service'],mm(exp=.04,trade=.04,bur=.03),mm(trade=.06,supply=-.04,bur=.02),2,2,.001,.001,'Offer improved bonded transit and commercial handling through Chilean ports.','1904 transit treaty and later negotiations are historical; no sovereignty transfer or corridor is assumed.',buildings=[('CHL',950,'infrastructure',1)])
agreement('france_technical','French-Chilean Technical Cooperation','FRA',6,6,['diplomatic_service'],mm(res=.025,cap=.04,edu=.03),mm(exp=.015,trade=.03,edu=.02),2,2,.001,.001,'Offer university, engineering and industrial technical cooperation.','European diversification is documented; this specific bilateral programme is alternate history.',research=[('CHL','industry',.25,1),('FRA','industry',.15,1)])
andean=spirit('cartagena_member','Cartagena Agreement Participant','Chile is a signatory of the 1969 Cartagena Agreement. Participation requires negotiated regional industrial and trade rules.',mm(trade=.03,bur=.02))
andean['kind']='membership';andean['lifecycle']='Actual membership; suspension or withdrawal removes the spirit and member programmes. It is not granted by a focus name.'
node('andean_admission','Ratify Andean Industrial Commitments','diplomacy',0,4,['diplomatic_service'],desc='Propose a jointly ratified industrial protocol to Bolivia, Colombia, Ecuador and Peru within the Cartagena institutions.',require=['Active Cartagena Agreement Participant spirit.'])
andean_deal=dict(id=P+'andean_protocol',partner='BOL, COL, ECU, PRU',partners=['BOL','COL','ECU','PRU'],title='Andean Industrial Protocol',description='A jointly ratified industrial and technical cooperation protocol among participating Cartagena states.',source='1969 Cartagena Agreement; exact project, costs and national rewards are RP proposals.',perpetual=True,pending_days=90,
    chile=dict(spirit='Andean Industrial Protocol: Chile',modifiers=mm(cap=.04,trade=.03,bur=.02),setup=2,weekly=.001),
    recipient=dict(spirit='Andean Industrial Protocol: Member',modifiers=mm(cap=.025,trade=.03,bur=.02),setup=1,weekly=.0005),buildings=[],research=[],decision='Consider the Andean Industrial Protocol',requirements=['Active Cartagena Agreement Participant spirit in every participant.'],conditions=['All five countries exist and ratify independently.','Every pair remains at peace and free of directed embargoes and all four Imperia sanction classes.','All participants retain actual Cartagena membership.'],implementation='Four separate recipient acceptance/refusal decisions. No setup costs or rewards until all ratify and revalidation succeeds atomically. On loss of any required relation or member, suspend all five spirits and costs without repeating setup on restoration. Withdrawal does not grant assets or refund fees. New shared definition required; no existing Chile/Andean membership integration is certified.')
D['agreements'].append(andean_deal);B['andean_admission']['agreement']=andean_deal['id']
node('andean_industry','Andean Industrial Complementarity','diplomacy',-2,8,['andean_admission'],mm(cap=.06,out=.04,trade=-.03),money=3,weekly=.001,desc='Coordinate industrial specialization with the Andean partners under the actual membership agreement.',icon='industry',require=['Active Cartagena Agreement Participant spirit.','Active Andean Industrial Protocol: Chile spirit.'],buildings=[(468,'industrial_complex',1)])
node('andean_autonomy','Andean Technical Mobility','diplomacy',2,8,['andean_admission'],mm(trade=.06,res=.025,edu=.04),money=2,weekly=.001,desc='Prioritize mobile technical teams and training over domestic industrial specialization.',require=['Active Cartagena Agreement Participant spirit.','Active Andean Industrial Protocol: Chile spirit.'],research=[('industry',.25,1)])
ex('andean_industry','andean_autonomy')
for k in ['andean_industry','andean_autonomy']:B[k]['lifetime']='membership';B[k]['programme']='Andean Member Programme'

# Unavoidable repression liabilities attach to actual authoritarian conduct, not a bonus for a focus name.
D['conditional_spirits']=[dict(id=P+'repression',name='Repression, Exile and Broken Institutions',description='Arbitrary detention, torture, disappearances and exile damage Chilean society and public institutions.',modifiers=mm(st=-.12,res=-.05,trade=-.10,police=.08),activation='Actual repression event or security-state decree; never applied at the January 1970 start.',remedy='Civilian restoration, independent investigation and funded reparations; repeal does not undo one-time human losses.'),
dict(id=P+'bank_crisis',name='Banking and External Debt Crisis',description='External indebtedness and fragile banks transmit a financial shock through the economy.',modifiers=mm(build=-.12,out=-.08,int=1.5,st=-.06),activation='Credit-risk crisis event after fragile financial policy and an external shock, not every government automatically in 1982.',remedy='Chosen intervention or creditor-loss programme replaces this crisis with a 365-day restructuring burden.'),
dict(id=P+'restructuring',name='Financial Restructuring',description='Credit is recovering, but the costs of bank restructuring continue.',modifiers=mm(build=-.04,int=.5,st=-.02),activation='Replacement for an active banking crisis when the selected rescue completes.',remedy='365 days; no repeat crisis replacement payout.')]

def evt(key,title,trigger,desc,options,kind='dilemma'):
    D['events'].append(dict(id=P+'event_'+key,key=key,title=title,trigger=trigger,description=desc,options=options,kind=kind))
def opt(name,mods=None,money=0,weekly=0,**kw):return dict(name=name,modifiers=mods or {},money=money,weekly=weekly,**kw)
evt('election','The Presidential Succession of 1970','Campaign opens in the historical 1970 election calendar; September vote and October congressional ratification read the actual election result.','Chile faces a contested succession. The presidency requires a constitutional result and recognition by Congress.',[
opt('Support Radomiro Tomic',mm(pp=.02),party_support={'party':1,'amount':.03},candidate='Radomiro Tomic'),
opt('Support Salvador Allende',mm(pp=.02),party_support={'party':18,'amount':.03},candidate='Salvador Allende'),
opt('Support Jorge Alessandri',mm(pp=.02),party_support={'party':2,'amount':.03},candidate='Jorge Alessandri')],kind='campaign, not immediate accession')
evt('congress','Congress and the Electoral Plurality','No candidate wins an absolute majority in the 1970 election.','Congress must confirm a lawful president. Constitutional guarantees may secure the decisive votes.',[
opt('Ratify the lawful plurality with guarantees',mm(st=.04,pp=-.04),result='Install the actual confirmed candidate through the corrected native leader system.'),
opt('Seek an alternative constitutional majority',mm(st=-.04,pp=.04),result='Congress considers only constitutionally eligible candidates; failure opens a constitutional crisis, not an automatic coup.')])
evt('copper','Compensation after Nationalization','Full Copper Nationalization completes.','Public ownership is settled. The government must decide how to resolve compensation claims.',[
opt('Negotiate a compensation settlement',mm(trade=.06,int=-.25),money=3),opt('Contest the claims through sovereign law',mm(resist=.06,trade=-.08,int=.5))])
evt('transport','A National Transport Stoppage','A conditional logistics crisis under high political confrontation; historical reference October 1972.','A transport stoppage disrupts supply. Workers, firms and the government demand a response.',[
opt('Negotiate a funded transport compact',mm(st=.03,corp=-.02),money=1,duration=180),
opt('Organize emergency public distribution',mm(supply=-.04,bur=.06),money=2,weekly=.001,duration=180),
opt('Confront the stoppage through emergency powers',mm(pp=.08,st=-.07,police=.06),duration=180)])
evt('rupture','The Constitutional Crisis','High confrontation, failed civilian settlement and a real military intervention condition. Historical reference 1973.','Civilian and military authorities face a choice between negotiated guarantees and a violent rupture.',[
opt('Conclude an enforceable constitutional accord',mm(st=.05,pp=-.08),money=1,result='Retain civilian succession if parliamentary and military participants accept.'),
opt('Permit the service chiefs to seize government',mm(st=-.10,res=-.03),result='Actual military transfer activates the military branch. Pinochet is not automatically commander in January 1970; the later junta leadership event selects the actual leader.')])
evt('junta','The Presidency of the Junta','A military government actually exists after a coup. Historical Pinochet command is a later outcome.','The service chiefs must settle their internal authority and the timetable for civilian rule.',[
opt('Retain collective military authority',mm(org=.03,pp=-.04),result='Preserve the actual constitutionalist or collective leader; early exit remains possible.'),
opt('Concentrate the presidency under Pinochet',mm(pp=.10,st=-.06),result='Install Augusto Pinochet through the corrected slot22 leader route. Requires his actual availability and officer backing; does not create him in January1970.')])
evt('repression','Emergency Security Decrees','An actual coercive security decree or the National Security State focus.','The security apparatus seeks wider powers of detention and political suppression.',[
opt('Authorize the coercive decrees',result='Add Repression, Exile and Broken Institutions.',add_spirit=P+'repression'),
opt('Require civilian legal safeguards',mm(pp=-.08,police=.03),result='Reject exceptional coercive powers and preserve judicial review.')])
evt('adjustment','The Social Cost of Adjustment','The Chicago Programme completes.','The pace of economic adjustment has become a dispute within the government and society.',[
opt('Maintain the rapid programme',mm(build=.04,st=-.06,soc=-.03),duration=365),
opt('Fund a staged adjustment',mm(st=.04,soc=.05),money=2,weekly=.002,duration=365)])
evt('banking','External Credit and the Banks','Financial fragility plus an external credit shock; 1982-83 is the historical reference, not an unconditional country penalty.','Foreign financing tightens and weak balance sheets threaten lending and production.',[
opt('Declare the crisis and prepare restructuring',add_spirit=P+'bank_crisis',result='Unlock Public Bank Intervention and Impose Creditor Losses.'),
opt('Enforce supervision before failures spread',mm(corp=-.04,bur=.04,int=-.25),money=2,require='Prudential Bank Supervision already completed.',result='Prevention is available only before systemic bank failure; it cannot erase an active crisis.')])
evt('early_exit','An Early Civilian Transfer','Guarantee a Civilian Ballot completes under constitutionalist military leadership.','Military and civilian negotiators agree the terms of a return to competitive government.',[
opt('Schedule and enforce the civilian election',mm(st=.05,pers=.03),money=1,result='Restore native elections. Government follows the actual result; military programme deactivates on handover.'),
opt('Delay until the guarantees are ratified',mm(st=-.03,pp=.03),duration=180,result='A new ratification deadline is set; no permanent military bonus.')])
evt('plebiscite','The Continuation Plebiscite','An Enforceable Plebiscite completes and the agreed vote is conducted; 1988 is the historical precedent.','The electorate decides whether military rule may continue under the proposed constitutional terms.',[
opt('Respect a No majority',mm(st=.05,pp=-.05),require='No won the actual vote.',result='Unlock negotiated handover and competitive civilian elections.'),
opt('Respect a Yes majority',mm(st=.02,pp=.03),require='Yes won the actual vote.',result='A counterfactual continuation retains authoritarian liabilities and the need for future constitutional consent.')])
evt('handover','The Civilian Inauguration','Negotiated handover and actual civilian election result. Historical reference March 1990.','A civilian president takes office under a negotiated constitutional settlement.',[
opt('Transfer the presidency to the elected coalition',mm(st=.05),result='Install the actual winning civilian candidate, including Aylwin for an appropriate PDC coalition. Suspend the military programme without replaying assets.')])
evt('truth','Truth, Justice and Reparations','A National Truth Commission completes after a documented repression period.','The commission presents its findings. Civilian authorities must choose how to fund remedies and pursue accountability.',[
opt('Fund reparations and independent prosecutions',mm(st=.04,police=.04),money=3,weekly=.001,remove_spirit=P+'repression'),
opt('Fund reparations under negotiated limits',mm(st=.02,pers=.04),money=2,weekly=.001,replace_spirit={'old':P+'repression','new':P+'limited_accountability'})])
D['conditional_spirits'].append(dict(id=P+'limited_accountability',name='An Unfinished Reckoning',description='Reparations have begun, but negotiated limits leave accountability incomplete.',modifiers=mm(st=-.04,trade=-.03,police=.03),activation='Truth commission negotiated-limits option.',remedy='Later judicial settlement requires a separately funded decision; no repeat reparations payment.'))
D['conditional_spirits'].append(dict(id=P+'lasting_legacy',name='The Legacy of Repression',description='Civilian rights have been restored. Families, exiles and damaged institutions still bear lasting losses.',modifiers=mm(st=-.02,res=-.01,health=.02),activation='Any documented repression period leaves this legacy after active repression ends.',remedy='No focus erases the human losses. Reparations remain a funded national obligation.'))
# Historical dates are precedents rather than arbitrary barriers to explicitly alternate policy sequences.
for g in G:
    if g['id'] in ('mir','gremial'):
        g['description']='Counterfactual governing programme for a real movement; no focus elects or installs it. Actual office must first be obtained through an explicit RP political transition.'
    if g['id'] in ('dr','padena'):
        g['description']='Minority civilian programme. Office requires an actual election or coalition settlement; its construction is one paid regional project, not a great-power industrial plan.'
for ev in D['events']:
    if ev['key']=='rupture':ev['options'][1]['add_spirit']=P+'repression'
    if ev['key']=='truth':
        for o in ev['options']:o['weekly_lifetime']='Standing national reparations, survives party changes; budgeted weekly, no expiry.'
        ev['options'][0]['add_spirit']=P+'lasting_legacy';ev['options'][1]['add_spirit']=P+'lasting_legacy'
    if ev['key']=='junta':ev['description']='The historical junta was chaired by Pinochet from September 1973. Formal executive concentration followed in June and December 1974. An earlier collective constitutionalist government is an alternate outcome.'
    if ev['key']=='banking':ev['trigger']='A fragile domestic banking system meets an external credit shock. The event is evaluated independently of focus completion. 1982-83 supplies the historical precedent.'
B['pinochet_crisis']['event']=None;B['pinochet_crisis']['decision']='Conduct banking stress tests'
B['pinochet_crisis']['modifiers']=mm(int=-.25,bur=.03)
B['mapuche_titles']['description']='Prepare recognition of indigenous community claims and fund legal settlement of disputed titles. The 1972 indigenous law supplies the historical legislative precedent.'
D['events'].append(dict(id=P+'event_andean',key='andean',title='Chile and the Cartagena Commitments',kind='historical policy review',trigger='1976 membership review, or completion of a Chilean trade-policy review under a different historical timetable.',description='The government must decide whether regional industrial rules remain compatible with its national programme.',options=[
opt('Remain within the ratified framework',mm(cap=.02,trade=-.02),result='Retain actual membership and the agreed obligations. Continued membership after 1976 is a counterfactual policy choice.'),
opt('Withdraw under the treaty procedure',mm(build=.03,trade=.02),remove_spirit=P+'cartagena_member',result='Suspend every dependent member programme and the five-country industrial protocol. One-time assets remain; no fees or construction repeat.')]))
D['historical_policy_notes']={'MIR':'Extra-parliamentary movement in actual history. A governing MIR programme is explicitly counterfactual, requires actual rule, and grants no automatic revolution.','Gremialismo':'University movement founded1967; regime influence after1973, UDI movement1983, legal party1988-89. A 1970 governing Gremialist party is counterfactual. Do not reuse the name as a synonym for PN.','civilian_right':'PN1970 programme may continue if civilian rule survives. After the historical dictatorship, RN/UDI successor formations require an explicit period-correct transition; a restored PN is counterfactual.','policy_dates':'Mapuche law1972, Chicago stabilization1975, pension reform1980-81, Cartagena withdrawal1976 and plebiscite1988 are source precedents. Earlier equivalent policies require the stated institutional and political conditions and are alternate history, not a claim those laws existed at the start.'}
# Short English names fit MD's actual single-line title field; narrative detail remains in descriptions.
SHORT={
'constitutional_mandate':'Constitutional Mandate','electoral_rolls':'Independent Electoral Rolls','civil_service':'A Professional Civil Service','mapuche_titles':'Mapuche Land Rights','judicial_review':'Independent Courts','commission_truth':'A Truth Commission','civilian_compact':'A Civilian Compact',
'corfo_plan':'CORFO Investment Review','negotiated_copper':'A Copper Settlement','national_copper':'Nationalize Copper','concession_copper':'Regulated Concessions','copper_stabilization':'Copper Stabilization Fund','export_reinvestment':'Reinvest Export Earnings','cold_chain':'Rural Storage Networks','price_compact':'A Wage and Price Pact','prudential_banks':'Prudential Bank Rules','central_corridor':'The Central Corridor','huachipato':'Huachipato Suppliers',
'professional_review':'Service Readiness Review','mobile_reserve':'A Mobile Reserve','famae':'FAMAE Workshops','asmar':'ASMAR Dockyards','enaer':'ENAER Foundations',
'pdc_social':'Community Development','pdc_tomic':'Tomic\'s Convergence','pdc_centre':'An Independent Center','pdc_left':'A Reform Coalition','pdc_housing':'Neighbourhood Services','pdc_church':'Civic Reconciliation','pdc_aylwin':'A Civilian Coalition',
'pn_investment':'Investment Guarantees','pn_alessandri':'Alessandri\'s Republic','pn_jarpa':'Jarpa\'s Development Plan','pn_compensation':'Compensation Courts','pn_suppliers':'National Supplier Contracts','pn_liberal':'Competitive Enterprise','pn_social':'Conservative Social Policy','pn_portfolio':'Diversify Exports','pn_republic':'A Conservative Mandate',
'pr_baltra':'Baltra\'s Development Plan','pr_provinces':'Provincial Civil Service','pr_plural':'Plural Education Pacts','pr_planning':'An Independent Plan','pr_parliament':'Budgetary Oversight','pr_pluralist':'Pluralist Development',
'ps_milk':'The Nutrition Programme','ps_allende':'Allende\'s Legal Road','ps_mixed':'A Social Property Pact','ps_control':'Workers\' Councils','ps_decentral':'Regional Economic Councils','ps_bargain':'A Bargain with the CUT','ps_mobilization':'Popular Mobilization','ps_housing':'Public Housing Works','ps_supply':'Distribution Boards','ps_coexistence':'Democratic Coexistence','ps_chilean_road':'The Chilean Road',
'pcch_unions':'Organized Labour','pcch_front':'A Broad Popular Front','pcch_cadres':'Industrial Party Cadres','pcch_soviet':'Soviet Technical Standards','pcch_domestic':'Domestic Machinery','pcch_cautious':'Production before Expansion','pcch_public':'Public Sector Consolidation','pcch_local':'Autonomous Union Bargains','pcch_plan':'Production Agreements','pcch_literacy':'Workers\' Technical Institutes','pcch_pluralism':'A Plural Popular Unity',
'mapu_extension':'Rural Reform Service','mapu_technicians':'Chonchol\'s Administration','mapu_technical':'Cooperative Machinery','mapu_land':'Land Councils and Titles','mapu_christian':'Christian Social Radicalism','mapu_marxist':'Independent Marxism','mapu_local':'Cooperative Autonomy','mapu_delivery':'Food Delivery Contracts','mapu_reform':'An Agrarian Settlement',
'dr_republic':'Secular Republicanism','dr_independent':'An Independent Bloc','dr_alliance':'A Civilian Right Accord','dr_schools':'Schools and Examinations','dr_public':'A Reformed Mixed Economy','dr_provincial':'Provincial Services',
'padena_coops':'Small-Farmer Credit','padena_enterprise':'Provincial Enterprise','padena_integrity':'Honest Public Contracts','padena_roads':'Provincial Roads','padena_bargain':'A Provincial Coalition',
'gremial_guilds':'Professional Associations','gremial_corporate':'A Corporatist Compact','gremial_schools':'Independent Schools','gremial_tutelage':'Protected Constitutionalism','gremial_electoral':'An Electoral Right','gremial_continuity':'Conservative Continuity',
'mir_organize':'Settlement Organization','mir_civil':'An Independent Left','mir_vanguard':'Revolutionary Vanguard','mir_selfmanagement':'Settlement Autonomy','mir_territorial':'Defense Committees','mir_command':'Revolutionary Command','mir_nonalign':'Revolutionary Independence','mir_clinics':'Community Public Services',
'military_staff':'The Service Chiefs','military_constitution':'A Constitutional Exit','pinochet_command':'Pinochet\'s Command','pinochet_pensions':'Pension Capitalization','pinochet_private':'Mixed Strategic Firms','pinochet_crisis':'External Debt Review','pinochet_supervision':'Prudential Reform','pinochet_pragmatic':'Pragmatic Export Recovery','pinochet_technocrat':'Technocratic Continuity','pinochet_security':'The Security State','pinochet_handover':'A Civilian Handover','pinochet_continuity':'Military Continuation',
'diplomatic_service':'The Diplomatic Service','usa_mines':'US Copper Protocol','soviet_machinery':'Soviet Machinery Credit','japan_copper':'Pacific Copper Contract','cuba_clinics':'Cuban Health Exchange','argentina_beagle':'Beagle Peace Treaty','peru_maritime':'Pacific Maritime Protocol','bolivia_transit':'Bolivian Transit Protocol','france_technical':'French Technical Accord','andean_admission':'The Andean Protocol','andean_industry':'Andean Specialization'}
for k,title in SHORT.items():B[k]['title']=title
for k,title in {'electoral_rolls':'Electoral Independence','civil_service':'Professional Civil Service','corfo_plan':'CORFO Investment Plan','pn_suppliers':'National Supply Contracts','ps_decentral':'Regional Economic Boards','pcch_soviet':'Soviet Technical Training','pcch_cautious':'Production before Growth','pcch_public':'Public Sector Unity','pcch_local':'Union Autonomy','pcch_literacy':'Workers\' Technical Schools','mapu_christian':'Christian Social Reform','dr_public':'A Reformed Mixed Sector','gremial_tutelage':'Protected Institutions','mir_nonalign':'Revolutionary Autonomy','mir_clinics':'Community Services','pinochet_pragmatic':'Pragmatic Export Policy'}.items():B[k]['title']=title
# Clear skipped-row connector lanes without changing a single logical prerequisite.
for key,x,y in [('rural_extension',18,2),('price_compact',32,2),('monetary_restraint',36,2),('andean_industry',46,27),('andean_autonomy',50,27)]:
    n=B[key];g=next(g for g in G if g['id']==n['group']);n.update(x=x,y=y,dx=x-g['x'],dy=y-g['y'])
# Measured donor evidence: over91% of descending links advance one row. Compact both banks accordingly.
for g in G:
    old_y=g['y'];g['y']=0 if old_y==0 else 9
    for n in [n for n in N if n['group']==g['id']]:
        n['y']=g['y']+(n['y']-old_y)//2
        if n['anchor']:n['dy']=n['y']-g['y']
        else:n['dy']=n['y']
for k in ['andean_industry','andean_autonomy']:B[k]['y']=15;B[k]['dy']=6
for k,icon in {'usa_mines':'copper','soviet_machinery':'industry','japan_copper':'navy','cuba_clinics':'social','argentina_beagle':'navy','peru_maritime':'navy','bolivia_transit':'infra','france_technical':'research','andean_admission':'industry'}.items():B[k]['icon']=icon
B['cooperative_titles']['modifiers'].update(mm(st=.04))
B['pinochet_security']['modifiers'].update(mm(resist=.20,org=.08,sanction=.12))
B['pinochet_security']['description']='Prioritize military organization and resilient domestic supply under permanent security rule, bearing the costs of repression, isolation and lost expertise.'
B['military_ballot']['description']='Restore civilian electoral organization under agreed military withdrawal terms. The national election proceeds even if military leaders subsequently lose office.'

# Correct inherited routing is a required implementation dependency, not silently certified existing behaviour.
D['integration']={
'starting_leader':'Eduardo Frei Montalva, PDC slot1, January1970. Preserve starting technology and deferred OOB choices.',
'routing_fix':'Correct Chile native leader routing: slot18 Socialist Allende; slot3 Radical Baltra; slot1 period-appropriate PDC Tomic/Aylwin after Frei Montalva. Current Allende-slot3 and Frei Ruiz-Tagle early pool are incompatible with the 1970 registry.',
'party_checks':'Use existing exact *_in_power scripted triggers for each numeric subparty. No party-dependent allow_branch; branches remain visible. Military slot22 is not itself proof that Pinochet rules.',
'sync':'Party programmes retain earned variables but their dynamic modifier and weekly expenses apply only while that party actually rules. Recheck on party/leader change, daily fallback and load. Construction, research bonuses and setup payments have independent once-only receipts.',
'finance':'One-time costs use set_temp_variable treasury_change then modify_treasury_effect in the execution guard. Native borrowing remains permitted for own authorized spending. New Chile weekly totals must be integrated into calculate_additional_expenses_rate; not an already-installed Chile API.',
'copper':'Copper is an export-income proxy using resource_export_multiplier_modifier. No local_resources_copper_factor, no extra raw tungsten mislabeled copper, no invented copper building.',
'buildings':'Same-state add_extra_state_shared_building_slots, then add_building_construction instant_build=yes. Completion rechecks actual ownership/control, building native cap, province validity for province buildings and total slot capacity. If any destination is invalid, no charge, no receipt, no completion payout.',
'andean':'Chile is historically a 1969 Cartagena signatory. Seed actual treaty membership at the historical start; future accession requires ratification. Every member-only entry and continuation requires the actual membership spirit in availability and reward guards. The industrial protocol additionally requires all four recipient governments to ratify. No modern Mercosur/EU membership reward.',
'events':'This concept specifies native country-event records, recipient decisions, reply notifications and guarded options. Country-event art is not yet composed. Reinspect current donor frame and full option window before adding event assets.',
'approval':'No runtime tree, localisation, event, history, interface, idea or monetary-system file is emitted or installed by this review generator.'}

# Native snippet previews distinguish proposed new definitions from verified native engine/MD primitives.
TRIGGERS={0:'western_autocrats_are_in_power',1:'western_conservatism_are_in_power',2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',4:'emerging_communist_state_are_in_power',5:'emerging_anarchist_communism_are_in_power',14:'neutrality_neutral_conservatism_are_in_power',18:'neutrality_neutral_social_are_in_power',19:'neutrality_neutral_communism_are_in_power',20:'nationalist_right_wing_populists_are_in_power',22:'nationalist_military_junta_are_in_power'}
for n in N:
    n['party_trigger']=TRIGGERS.get(n['party'])
    if n['key'].startswith('pinochet_'):
        n['leader']='Augusto Pinochet';n['lifetime']='leader';n['programme']='Pinochet Government Programme'
    n['availability_code']=(n['party_trigger']+' = yes' if n['party_trigger'] else '')
    if n.get('leader'):n['availability_code']+='\nhas_country_leader = { name = "Augusto Pinochet" ruling_only = yes }'
    if n['lifetime']=='membership':n['availability_code']+='\nhas_idea = '+P+'cartagena_member\nhas_idea = '+P+'andean_protocol_chile'
    if n['key']=='andean_admission':n['availability_code']+='\nhas_idea = '+P+'cartagena_member'
    if n['key']=='military_staff':n['availability_code']+='\nhas_country_flag = '+P+'military_government'
    if n['key']=='military_constitution':n['availability_code']+='\nhas_country_flag = '+P+'constitutional_military_council'
    if n['key'] in ['pinochet_rescue','pinochet_losses']:n['availability_code']+='\nhas_idea = '+P+'bank_crisis'
    if n['key']=='pinochet_handover':n['availability_code']+='\nhas_country_flag = '+P+'plebiscite_no_won'
D['election_contract']={
    'status':'New Chile integration using the existing MD election/party array; not an existing working Chile election event.',
    'calendar':{'campaign':'1970-01-01 to 1970-09-03','popular_vote':'1970-09-04','congress_if_needed':'1970-10-24','inauguration':'1970-11-03'},
    'native_calendar_correction':'Current Chile1970 history uses generic last_election1968 and48months. Replace that presidential schedule in the future1970 integration with the historical1964 ballot baseline and72-month term, then record the actual1970 ballot. Restore48months for the1990 transitional presidency. Do not emit an extra1972 presidential election from the old generic schedule.',
    'campaign_receipt':'The campaign event fires once; each option calls native party support adjustment for only its stated slot. It never installs the candidate.',
    'count':'At the ballot, normalize eligible civilian party_pop_array support after native campaign/election changes. Save final candidate shares for Tomic1, Alessandri2 and Allende18, plus registered coalition endorsements. Do not count the same coalition share twice.',
    'result_record':{'COLDWAR_CHL_election_winner_slot':'Native ballot winner slot: 1, 2 or 18.','COLDWAR_CHL_election_runner_up_slot':'Runner-up slot for congressional runoff.','COLDWAR_CHL_election_confirmed_slot':'Only the candidate constitutionally confirmed by majority or Congress.','COLDWAR_CHL_election_ratified':'Set only after lawful confirmation; consumed once at inauguration.'},
    'congress':'If no absolute majority, congress event receives saved top two eligible candidates. Ratify plurality confirms stored winner. Alternative majority considers only stored runner-up and requires a real negotiated parliamentary coalition; if absent, the option fails visibly and no president is installed.',
    'inauguration':'Consume confirmed_slot once on 1970-11-03, set native ruling subparty/coalition via existing MD government setter and install period-correct Tomic, Alessandri or Allende. Correct current slot3 Allende routing first. Campaign choices never guarantee victory.',
    'later':'Subsequent ordinary elections use the corrected period-appropriate native pools. Minority PR/PCCh/MAPU/DR/PADENA governments require an actual later election or coalition transition, not a focus reward.'}
D['decision_contracts']=[
dict(id=P+'banking_stress_test',title='Conduct Banking Stress Tests',requirements=['External Debt Review or Prudential Bank Rules completed.','No active banking crisis.'],money=1,modifiers=mm(bur=.02,int=-.25),duration=365,effect='Create the funded stress-test programme for365 days; prevent a first fragile-bank event only while this programme is active. Does not cancel a crisis already active.'),
dict(id=P+'civilian_bank_restructuring',title='Authorize Emergency Bank Restructuring',requirements=['Civilian government.','Banking and External Debt Crisis is active.'],money=6,weekly=.003,modifiers=mm(build=.08,int=.5,tax=-.03),effect='Replace active Banking and External Debt Crisis with Financial Restructuring for365 days. One restructuring receipt. These national crisis remedies remain reachable after a party change, including loss of military rule. No focus completion or building payout is replayed.'),
dict(id=P+'civilian_creditor_losses',title='Restructure Banks through Creditor Losses',requirements=['Civilian government.','Banking and External Debt Crisis is active.'],money=2,weekly=0,modifiers=mm(int=-.5,build=-.06,st=-.05),effect='Replace active Banking and External Debt Crisis with Financial Restructuring for365 days. Mutually exclusive with the funded public intervention for this crisis episode.'),
dict(id=P+'full_judicial_settlement',title='Complete the Judicial Settlement',requirements=['Civilian government.','An Unfinished Reckoning is active.'],money=2,weekly=0,modifiers={},effect='Remove An Unfinished Reckoning. Preserve The Legacy of Repression and existing national reparations. No repeat reparations setup fee, no second weekly reparations obligation.')]
for key in ['pinochet_rescue','pinochet_losses']:
    B[key]['replace_spirit']={'old':P+'bank_crisis','new':P+'restructuring','duration':365}
    B[key]['crisis_receipt']='One national crisis-resolution receipt; no duplicate decision/focus charge.'
    B[key]['lifetime']='national:365 days';B[key]['programme']='Financial Restructuring Programme';B[key]['duration']=365
def snippet(n):
    lines=[]
    if n['money']:lines += ['set_temp_variable = { treasury_change = -'+str(n['money'])+' }','modify_treasury_effect = yes']
    for r in n['remove']:lines.append('remove_ideas = '+r)
    if n.get('replace_spirit'):
        r=n['replace_spirit'];lines += ['remove_ideas = '+r['old'],'add_timed_idea = { idea = '+r['new']+' days = '+str(r['duration'])+' }']
    if n['modifiers']:
        lines += ['# Proposed modifier delta on '+n['programme']]
        lines += [k+' = '+format(v,'.5f').rstrip('0').rstrip('.') for k,v in n['modifiers'].items()]
    if n['weekly']:lines += ['# Proposed weekly expense ledger contribution: '+format(n['weekly'],'.5f')+' billion']
    for b in n['buildings']:
        lines += [str(b['state'])+' = {','  add_extra_state_shared_building_slots = '+str(b['slots']),'  add_building_construction = { type = '+b['type']+' level = '+str(b['levels'])+' instant_build = yes }','}']
    for r in n['research']:lines += ['add_tech_bonus = { name = '+n['id']+'_bonus bonus = '+str(r['bonus'])+' uses = '+str(r['uses'])+' category = '+r['category']+' }']
    if n.get('agreement'):lines += ['# New Chile offer helper required: recipient '+next(a['partner'] for a in D['agreements'] if a['id']==n['agreement'])+' receives acceptance/refusal decision.']
    if n.get('event'):lines += ['country_event = { id = '+P+'event_'+n['event']+' }']
    if n.get('decision'):lines += ['# Unlock proposed decision: '+n['decision']]
    return '\n'.join(lines)
CATS={'industry':'CAT_industry','computing_tech':'CAT_computing','air_equipment':'CAT_aircraft','naval_equipment':'CAT_surface_ships'}
for n in N:
    for r in n['research']:r['category']=CATS.get(r['category'],r['category'])
    n['proposed_code']=snippet(n)
for a in D['agreements']:
    for r in a['research']:r['category']=CATS.get(r['category'],r['category'])
COUNTRIES={'CHL':'Chile','USA':'United States','SOV':'Soviet Union','JAP':'Japan','CUB':'Cuba','ARG':'Argentina','PRU':'Peru','BOL':'Bolivia','COL':'Colombia','ECU':'Ecuador','FRA':'France'}
for a in D['agreements']:
    if a.get('partners'):a['recipient_spirits']={tag:a['title']+': '+COUNTRIES[tag] for tag in a['partners']}
    else:a['recipient']['spirit']=a['title']+': '+COUNTRIES[a['partner']]
    for side in ('chile','recipient'):a[side]['weekly_lifetime']='Standing agreement; applies only while the paired or collective agreement is active.'

# Geometry, graph and exclusion validation. These are source/model checks, not engine tests.
ids={n['id']:n for n in N}; assert len(ids)==len(N)
for n in N:
    assert all(k in ids for ps in n['prerequisites'] for k in ps)
    assert all(n['id'] in ids[k]['excludes'] for k in n['excludes'])
    for ps in n['prerequisites']:assert all(ids[k]['y']<n['y'] for k in ps),(n['key'],ps)
    assert n['money']==0 or 1<=n['money']<=10
    assert not any('workforce' in k and v<0 for k,v in n['modifiers'].items())
    for b in n['buildings']:assert b['slots']==b['levels']
def reachable(n,chosen=frozenset(),visiting=frozenset()):
    # Enumerate mutually compatible receipts recursively, one representative per OR alternative.
    if n['id'] in visiting:return []
    if any(k in chosen for k in n['excludes']):return []
    states=[chosen|{n['id']}]
    for ps in n['prerequisites']:
        nxt=[]
        for st in states:
            for p in ps:nxt += reachable(ids[p],st,visiting|{n['id']})
        states=nxt
        if not states:break
    return states[:2000]
unreachable=[n['key'] for n in N if not reachable(n)]
assert not unreachable,unreachable
collision=[]
for i,a in enumerate(N):
    for b in N[i+1:]:
        if abs(a['x']-b['x'])*96<165 and abs(a['y']-b['y'])*130<128:collision.append([a['key'],b['key']])
assert not collision,collision
D['meta']={'focus_count':len(N),'party_programmes':len([g for g in G if g['party'] is not None]),'exclusive_pairs':sum(len(n['excludes']) for n in N)//2,'starting_spirits':len(D['spirits']),'events':len(D['events']),'agreements':len(D['agreements']),'grid':[96,130],'item':[165,128],'title':[147,20],'span':[min(n['x'] for n in N),max(n['x'] for n in N),min(n['y'] for n in N),max(n['y'] for n in N)],'initial_focus':P+'constitutional_mandate','continuous_panel_proposal':{'x':8*96,'y':9*130},'shared_focuses':'No generic local focuses attached. Existing global organisation features remain separate, with actual membership guards.'}
(HERE/'COLDWAR_CHL_design.json').write_text(json.dumps(D,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(HERE/'MODEL_QA.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','focuses':len(N),'missing_refs':[],'card_collisions':collision,'unreachable':unreachable,'exclusive_pairs':D['meta']['exclusive_pairs'],'status':'PASS: model only, no engine test'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(D['meta']))

def write_dossier():
    labels={k:v for k,v in STATS.values()}
    def stattext(mods):
        return '; '.join(labels.get(k,k)+': '+(f'{v:+g} pp' if k=='interest_rate_multiplier_modifier' else f'{v*100:+g}%') for k,v in mods.items()) or 'None'
    rows=['IMPERIA COLD WAR','', '# Chile, January 1970 to 1990: approval concept','',
    f"{len(N)} focuses, {D['meta']['party_programmes']} political programmes, {D['meta']['exclusive_pairs']} reciprocal exclusion pairs, {len(D['spirits'])} starting spirits, {len(D['events'])} events, eight bilateral offers and one five-country Andean protocol.",'',
    'This is the complete proposed design, not installed game content. All new game text is English. IDs begin COLDWAR_CHL_. All numerical effects and prices are balance proposals, not historical dollar amounts. Approve or amend the concept before implementation.','',
    '## Structure and political scope','',
    'The design uses the installed MD 2.0.4 France/Russia grammar: relative section anchors, local policy forks and OR joins, 96 by130 grid units, 165 by128 item containers and short single-line English titles. Over91% of descending donor links advance one row; ordinary Chile levels now do the same. The complete proposal spans x4..160,y0..17. The two banks are at y0 and9. There are no party-dependent branch visibility rules.','',
    '| Section | Root x,y | Focuses | Ruling subparty |','|---|---:|---:|---:|']
    for g in G:rows.append(f"| {g['title']} | {g['x']},{g['y']} | {sum(n['group']==g['id'] for n in N)} | {g['party'] if g['party'] is not None else 'Shared'} |")
    rows+=['','Initial game camera: Constitutional Mandate. Topic shortcuts: Republic, Development, Armed Forces, Foreign Agreements and the political programme roots. Continuous-focus panel: proposed lower-left pocket at768,1170px. The preview provides a full-tree atlas and native-scale branch navigation. Global shared organisation trees are not transplanted wholesale. Exact game font, connector routing, camera and continuous-panel bounds require HOI4 after approval.','',
    'PDC, PN, PR, PS, PCCh and MAPU have distinct programmes. DR and PADENA retain smaller minority programmes. MIR and Gremialismo are real movements with expressly counterfactual governing alternatives. No focus manufactures office for a minor party or movement. Military rule is an institutional rupture, with a constitutionalist early-exit alternative and a separate actual-Pinochet programme. No Muslim or monarchist filler branches are included.','',
    'PR has11 focuses, DR8 and PADENA7. Historical review suggested a10-12 combined cap, but that cap is a reviewer balance suggestion, not a user requirement: this proposal deliberately preserves separate inspectable programmes for the real parties. DR/PADENA each grant at most one paid regional building; they have less depth and scale than the dominant parties.','',
    '## Starting spirits','']
    for s in D['spirits']:rows += ['### '+s['name'],'',s['description'],'','- '+stattext(s['modifiers']),'']
    rows+=['## Policy trade-offs','',
    '- Copper: negotiated ownership buys supplier access and export gains at a higher setup price; full nationalization gives the strongest export-income proxy with research/trade burdens and compensation choices; regulated concessions favor construction and investment with reduced resistance to foreign influence.',
    '- Rural development: cooperatives offer a social and machinery programme; family holdings favor greater agricultural productivity with a lower tax yield. Both remedy the actual starting agrarian penalty.',
    '- Stabilization: a negotiated wage-price compact protects social cohesion but concedes tax and political capacity; monetary restraint improves interest terms while reducing construction and stability.',
    '- Pinochet: Chicago adjustment favors construction, credit and trade with sharp social costs; strategic state capitalism favors output and production capacity with administrative and commercial burdens. Each has further pension/social-floor or public-copper/mixed-enterprise choices. Later rule divides into managed constitutionalism, security-state continuity or an enforceable continuation plebiscite.',
    '- Constitutional military exit is genuinely separate from personal Pinochet rule. Authoritarian coercion carries Repression, Exile and Broken Institutions, not a hidden free stability gain. Truth and reparations end active repression while preserving The Legacy of Repression.','',
    '## Runtime design contract','']
    for k,v in D['integration'].items():rows+=['- **'+k+':** '+v]
    rows+=['','All Pinochet continuation focuses require his actual leadership in both availability and guarded rewards. Party and leader programmes suspend on loss of office, retaining earned receipts for a return. National assets and paid research bonuses are one-time outcomes. Party reactivation never builds another factory or charges setup again. The national financial restructuring remedy lasts365 days and its liability is retained across government changes.','',
    'Native party requirements reuse the exact existing *_are_in_power triggers, whose tooltip scripted localisation is already routed through the 1970 registry (for example conservatism_L -> MDCW_HP_conservatism -> MDCW_HP_CHL_1_0). Do not replace these with modern Chilean party names or a custom generic governing-current label. Current leader-pool mappings are a separate confirmed defect: PS/Allende belongs to18, PR/Baltra to3, and PDC succession needs Tomic/Aylwin rather than early Frei Ruiz-Tagle.','',
    '**Copper limitation:** the engine has no copper resource. Resource Export Revenue is the existing all-resource weekly export-revenue multiplier, affecting supported native resource exports; it does not create copper tonnage or income from a nonexistent copper export base. Copper institutions are represented through export, tax, engineering, credit and public/private industrial-policy effects. No new unconsumed copper modifier is proposed.','',
    '**Construction contract:** each level adds exactly one shared slot in the same selected Chilean state before instant construction. Ownership, control, native type/level caps, total slot maximum and coastline/province validity are separate guards. The slot and building sit inside one transaction receipt. These checks and the monetary debit must be revalidated together. Native maintenance, workforce and power costs still apply.','',
    '**Finance:** all cash amounts are billions. Ordinary project prices follow the current project convention of1-10billion; own spending uses native borrowing. Weekly literals are already weekly and have at most five fractional places. Rates in this design are balance values, not copied historical budgets. Starting1970 treasury is not established by the later2000 value of22. Simultaneous programme debt/interest affordability remains a required balance test, including19billion setup and0.012billion weekly for all foreign protocols.','',
    '## Election and succession contract','',json.dumps(D['election_contract'],indent=2),'',
    'The historical calendar must run independently of whether the opening focus is taken. Its completion may show the campaign event only while the campaign remains open and its one-time receipt is unset. A late completion never reopens1970 or replaces a sitting president. All internal date/scenario/receipt checks stay hidden in game tooltips.','',
    '## Historical and alternate-history boundaries','']
    rows += ['- '+k+': '+v for k,v in D['historical_policy_notes'].items()]
    rows += ['','Historic dates establish the precedent. Except the actual1970 constitutional ballot and historical1976 membership review, earlier equivalent policy choices can represent explicit alternate history under the required institutions; they do not pretend later statutes existed inJanuary1970. The credible continuation plebiscite is distinct from the contested1980 constitutional vote. A different negotiated timetable is alternate history.','',
    '## Reciprocal agreement terms','',
    'Every offer originates in a separate Chilean national focus. The named RP recipient receives real Accept and Decline decisions. No spirit, fee, research or building is granted on proposal. Native focus tooltips must show these complete If they accept terms while locked, pending or suspended, using display-only effect blocks. All standing agreements have no expiry. Pending offers expire after90 days without payment, and can be resubmitted after180 days if unratified. Accepted records cannot be purchased twice.','',
    'Suspension checks both directions: existence, war with the partner, native embargo and all four Imperia sanction classes (diplomatic,financial,economic,military). Both spirits and their weekly flows suspend/restore together. The five-country protocol checks every participant pair and all memberships. No setup payment, research bonus or asset repeats on restoration. Recipient government changes do not nullify an already ratified treaty.','']
    for a in D['agreements']:
        rows += ['### '+a['title'],'',a['description'],'',a['source'],'']
        for side,tag in [('chile','CHL')]+[('recipient',tag) for tag in a.get('partners',[a['partner']])]:
            t=a[side];name=a.get('recipient_spirits',{}).get(tag,t['spirit'])
            rows += ['**'+COUNTRIES[tag]+'**','',f"- Setup: ${t['setup']:.3f}billion. Weekly: ${t['weekly']:.5f}billion.",'- Add '+name+': '+stattext(t['modifiers'])]
            for b in a['buildings']:
                if b['country']==tag:rows += [f"- State{b['state']}: +{b['slots']}shared slots, then +{b['levels']} {b['type']}."]
            for r in a['research']:
                if r['country']==tag:rows += [f"- {r['uses']} x {r['bonus']*100:g}% research bonus: {r['category']}."]
            rows+=['']
        rows+=['Requirements: '+' '.join(a['requirements']+a['conditions']),'']
    rows+=['## Conditional liabilities and national remedies','']
    for s in D['conditional_spirits']:rows += ['### '+s['name'],'',s['description'],'','- '+stattext(s['modifiers']),'',s['activation'],s['remedy'],'']
    for d in D['decision_contracts']:rows+=['### '+d['title'],'','Requirements: '+' '.join(d['requirements']),f"Cost: ${d['money']:.3f}billion; weekly ${d.get('weekly',0):.5f}billion.",stattext(d['modifiers']),d['effect'],'']
    rows+=['## Events','']
    for e in D['events']:
        rows+=['### '+e['title'],'',e['description'],'','Design trigger: '+e['trigger'],'']
        for o in e['options']:
            rows += ['- **'+o['name']+f"**: setup ${o['money']:.3f}billion; weekly ${o['weekly']:.5f}billion. "+stattext(o['modifiers'])+(' ('+str(o['duration'])+'days)' if o.get('duration') else '')+'.']
            for k in ['party_support','candidate','add_spirit','remove_spirit','replace_spirit','require','result','weekly_lifetime']:
                if k in o:rows+=['  '+k+': '+str(o[k])]
        rows+=['']
    rows+=['## Exact focus catalogue','']
    for g in G:
        rows += ['### '+g['title'],'']
        for n in [n for n in N if n['group']==g['id']]:
            rows += ['#### '+n['title'],'',f"`{n['id']}`. Absolute({n['x']},{n['y']}), anchor`{n['anchor'] or 'none'}`, local({n['dx']},{n['dy']}), cost{n['cost']:g} = {n['days']}days. Lifetime: {n['lifetime']}.",'',n['description'],'']
            if n['prerequisites']:rows+=['Requires: '+' AND '.join('('+' OR '.join(ids[k]['title'] for k in ps)+')' for ps in n['prerequisites'])+'.']
            if n['excludes']:rows+=['Excludes: '+', '.join(ids[k]['title'] for k in n['excludes'])+'.']
            if n['availability_code']:rows+=['Native availability and reward guard: `'+n['availability_code'].replace('\n','; ')+'`.']
            rows+=['- Setup: $'+f"{n['money']:.3f}"+'billion; weekly: $'+f"{n['weekly']:.5f}"+'billion.','- '+stattext(n['modifiers'])]
            for r in n['remove']:rows+=['- Remove '+next(s['name'] for s in D['spirits'] if s['id']==r)+'.']
            if n.get('replace_spirit'):rows+=['- '+str(n['replace_spirit'])]
            for b in n['buildings']:rows += [f"- State{b['state']}: +{b['slots']} shared slots, then +{b['levels']} {b['type']}."]
            for r in n['research']:rows += [f"- {r['uses']} x {r['bonus']*100:g}% research bonus: {r['category']}."]
            for k in ['event','decision','agreement']:
                if n.get(k):rows+=['- '+k+': '+n[k]]
            rows+=['']
    rows+=['## Verification and provenance','',
    'Read MD_REFERENCE.md, HISTORICAL_RESEARCH.md and MECHANICS_AUDIT.md for source paths, direct historical URLs, native provider/consumer traces and units. DESIGN_REVIEW.md, HISTORY_DESIGN_REVIEW.md and LAYOUT_REVIEW.md are independent first-pass reviews; REVIEW_RESOLUTIONS.md records their final disposition.',
    'MODEL_QA.json checks IDs, anchors, card bounds, reciprocal exclusions and compatible prerequisite histories. BROWSER_QA.json checks all184 inspectors, all event options, twelve government variants and complete prospective agreement sides. These are concept/model/browser checks, not HOI4 or multiplayer engine tests.','',
    'No runtime content is installed. Event pictures are not fabricated native screenshots; country-event frame composition remains after approval and requires current donor-window inspection. PREVIEW_PROVENANCE.json records embedded native art and screenshot provenance. Original individual artists and separate redistribution permission are unknown. Existing upstream rights remain separate. No new ownership is claimed by project markers.']
    (HERE/'COLDWAR_CHL_CONCEPT.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
write_dossier()

if __name__=='__main__' and (HERE/'preview.template.html').exists():
    # All donor art is local and embedded; no remote requests in the inline view.
    ART={}; sources=[]
    defs='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for p in (ROOT/'interface').glob('*.gfx'))
    sprite_map={m.group(1):m.group(2) for m in re.finditer(r'name\s*=\s*"([^"]+)"(?:(?!spriteType).)*?texturefile\s*=\s*"([^"]+)"',defs,re.S|re.I)}
    candidates={
    'politics':['Election_graphics','Election'],
    'social':['generic_healthcare','focus_generic_full_social_mobilization'],
    'land':['focus_CHL_expand_the_forestry'],
    'copper':['focus_CHL_high_quality_nitrate','focus_CHL_silverworking'],
    'farm':['focus_CHL_focus_on_cattle_and_wool','farming'],
    'forest':['focus_CHL_expand_the_forestry'],
    'industry':['focus_CHL_enlarge_the_textile_industries'],
    'bank':['focus_CHL_strengthen_the_central_bank'],
    'army':['army_doctrine','army_general_stuff1'],
    'air':['air_doctrine','air_defense'],
    'navy':['naval_doctrine'],
    'energy':['construct_infrastructure'],
    'infra':['infrastructure','construct_infrastructure'],
    'research':['research','science'],
    'diplomacy':['diplomacy','aggressive_diplomacy'],
    'bar':['GFX_focus_can_start','GFX_focus_unavailable'], 'barlocked':['GFX_focus_unavailable']}
    # Some aliases are supplied by base-game GFX definitions. Fallbacks are resolved only to existing local sprites.
    for kind,names in candidates.items():
        for name in names:
            texture=sprite_map.get(name)
            if not texture:continue
            path=ROOT/texture
            if not path.exists():path=DONOR/texture
            if not path.exists():path=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')/texture
            if not path.exists():continue
            try:
                im=Image.open(path).convert('RGBA');im.thumbnail((180,160))
                buf=io.BytesIO();im.save(buf,format='PNG',optimize=True)
                ART[kind]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
                sources.append(dict(kind=kind,sprite=name,path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),author='Millennium Dawn / underlying asset author unknown',licence='Separate redistribution permission unknown',modification='DDS decoded and proportionally reduced to PNG for local review only'))
                break
            except Exception:continue
    missing=[k for k in candidates if k not in ART]
    assert not missing,missing
    D['art_sources']=sources
    (HERE/'COLDWAR_CHL_design.json').write_text(json.dumps(D,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fragment=(HERE/'preview.template.html').read_text(encoding='utf-8').replace('__DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':'))).replace('__ART__',json.dumps(ART,separators=(',',':')))
    (VIS/'coldwar-chile.html').write_text(fragment,encoding='utf-8')
    (HERE/'COLDWAR_CHL_preview.html').write_text(fragment,encoding='utf-8')
    wrapper='<!-- IMPERIA COLD WAR — Cold War Chile standalone review wrapper. -->\n<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fragment+'</body></html>'
    (HERE/'preview-review.html').write_text(wrapper,encoding='utf-8')
    (HERE/'PREVIEW_PROVENANCE.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','source':'Installed MD 2.0.4 donor and target MD Cold War 2.0.3','assets':sources,'renders':'Concept browser composition, not an HOI4 screenshot','screenshot_author':'Generated locally from the proposed concept','screenshot_licence':'Project review artifact; embedded third-party rights remain separate'},indent=2)+'\n',encoding='utf-8')
