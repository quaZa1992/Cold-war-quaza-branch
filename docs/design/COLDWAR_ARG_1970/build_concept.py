# IMPERIA COLD WAR — Argentina 1970-1990 approval concept and native MD preview.
"""Review-only builder. Never writes loaded common/events/history/localisation files."""
from pathlib import Path
import base64, hashlib, io, json, re
from collections import Counter
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DONOR = Path(r'C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/3374271790')
VIS = Path(r'C:/Users/sonyz/.codex/visualizations/2026/11/01/01a1965e-461e-7a62-bf09-f7c2727528c8')
P = 'COLDWAR_ARG_'
D = dict(project='IMPERIA COLD WAR', feature='Argentina 1970-1990', status='CONCEPT: awaiting approval; no runtime implementation',
         groups=[], nodes=[], spirits=[], conditional_spirits=[], agreements=[], events=[], decisions=[])
STATS = {
 'pp':('political_power_factor','Political Power Gain'), 'st':('stability_factor','Stability'),
 'res':('research_speed_factor','Research Speed'), 'ag':('agricolture_productivity_modifier','Agricultural Productivity'),
 'cprod':('civilian_factories_productivity','Civilian Industry Productivity'),
 'tax':('tax_gain_multiplier_modifier','Tax Revenue'), 'corp':('corporate_tax_income_multiplier_modifier','Corporate Tax Revenue'),
 'exp':('resource_export_multiplier_modifier','Resource Export Revenue'), 'int':('interest_rate_multiplier_modifier','Interest Rate'),
 'edu':('education_cost_multiplier_modifier','Education Expenditure'), 'soc':('social_cost_multiplier_modifier','Social Expenditure'),
 'health':('health_cost_multiplier_modifier','Health Expenditure'), 'bur':('bureaucracy_cost_multiplier_modifier','Bureaucracy Expenditure'),
 'police':('police_cost_multiplier_modifier','Police Expenditure'), 'pers':('army_personnel_cost_multiplier_modifier','Army Personnel Expenditure'),
 'milcost':('equipment_cost_multiplier_modifier','Equipment Operating Expenditure'),
 'build':('production_speed_buildings_factor','Construction Speed'), 'civ':('production_speed_industrial_complex_factor','Civilian Factory Construction Speed'),
 'infra':('production_speed_infrastructure_factor','Infrastructure Construction Speed'),
 'arms':('production_speed_arms_factory_factor','Military Factory Construction Speed'),
 'reactor':('production_speed_nuclear_reactor_factor','Nuclear Reactor Construction Speed'),
 'out':('industrial_capacity_factory','Factory Output'), 'dock':('industrial_capacity_dockyard','Dockyard Output'),
 'cap':('production_factory_max_efficiency_factor','Production Efficiency Cap'), 'gain':('production_factory_efficiency_gain_factor','Production Efficiency Growth'),
 'org':('army_org_factor','Division Organization'), 'rec':('army_morale_factor','Division Recovery Rate'),
 'supply':('supply_consumption_factor','Supply Consumption'), 'train':('training_time_army_factor','Division Training Time'),
 'defense':('army_core_defence_factor','Division Defense on Core Territory'), 'speed':('army_speed_factor','Division Speed'),
 'attack':('army_attack_factor','Division Attack'), 'navy':('navy_org_factor','Naval Organization'),
 'air':('air_mission_efficiency','Air Mission Efficiency'), 'detect':('air_interception_detect_factor','Interception Detection'),
 'resist':('foreign_influence_defense_modifier','Foreign Influence Defense'), 'trade':('trade_opinion_factor','Trade Opinion'),
 'sanction':('imp_sanction_resistance','Sanction Resistance'),
}
D['stats'] = STATS
PARTIES = {
 '22':'Argentine Armed Forces', '13':'Justicialist Party', '3':"People's Radical Civic Union", '2':'Integration and Development Movement',
 '16':'Independent Civic Party', '1':'Democratic Party of Mendoza', '14':'Christian Democratic Party', '4':'Communist Party of Argentina',
 '5':'Montoneros', '19':"Workers' Revolutionary Party", '18':'CGT of the Argentines', '20':'62 Organizations',
 '6':'Athenaeum of the Republic', '0':'Union of the Argentine People', '15':'Argentine Rural Society', 'PS':'Socialist constitutional coalition',
}
TRIGGERS = {0:'western_autocrats_are_in_power',1:'western_conservatism_are_in_power',2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',
 4:'emerging_communist_state_are_in_power',5:'emerging_anarchist_communism_are_in_power',6:'emerging_reactionaries_are_in_power',
 13:'neutrality_neutral_autocracy_are_in_power',14:'neutrality_neutral_conservatism_are_in_power',15:'neutrality_neutral_oligarch_are_in_power',
 16:'neutrality_neutral_libertarians_are_in_power',18:'neutrality_neutral_social_are_in_power',19:'neutrality_neutral_communism_are_in_power',
 20:'nationalist_right_wing_populists_are_in_power',22:'nationalist_military_junta_are_in_power'}
D['parties'] = PARTIES
def mm(**kw): return {STATS[k][0]:v for k,v in kw.items()}
def spirit(key,name,desc,mods,conditional=False,activation='',remedy=''):
    s=dict(id=P+key,name=name,description=desc,modifiers=mods,activation=activation,remedy=remedy)
    D['conditional_spirits' if conditional else 'spirits'].append(s)
    return s

spirit('start_regime','A Revolution without Consent','The presidency claims a mandate to reorganize society while parties remain dissolved and the largest popular movement is excluded.',mm(pp=.08,st=-.10),remedy='Constitutional restoration removes this spirit. A corporatist settlement replaces it with its own benefits and liabilities.')
spirit('start_cordobazo','The Cordobazo Aftermath','Worker and student mobilization has broken the promise of social peace. Disputes at the industrial centers continue to disrupt production.',mm(st=-.07,out=-.06,police=.04),remedy='National labor settlement or a completed party labor compact removes it. Repression replaces it with a different burden.')
spirit('start_stopgo','The Stop-Go Economy','Imported capital goods, contested incomes policy and uneven foreign exchange earnings make sustained industrial expansion difficult.',mm(build=-.07,int=.75),remedy='A funded stabilization programme replaces this problem. This does not reset native inflation or public debt.')
spirit('start_university','Universities after Intervention','Intervention and the departure of researchers have damaged an established scientific community. Argentina retains considerable technical capacity.',mm(res=-.07),remedy='University autonomy, technical restoration or a party science programme removes it. No workforce-size penalty.')
spirit('start_command','Competing Service Commands','The services remain political arbiters as well as military institutions. Rival chains of influence complicate common doctrine and budgets.',mm(org=-.05,navy=-.05,milcost=.06),remedy='Joint staff reform removes the operational penalty; civilian control separately settles political authority.')
spirit('start_geography','A Republic of Uneven Corridors','Industrial concentration in the littoral contrasts with distant northern and southern communities and expensive transport connections.',mm(infra=-.08,supply=.06),remedy='Funded north-south transport and provincial services remove this burden.')
spirit('wage_freeze','Order under Wage Restraint','The government holds down nominal demands through administrative discipline, leaving industrial opposition unresolved.',mm(out=.04,st=-.09,police=.08),True,'Chosen coercive labor settlement.','A later constitutional labor settlement replaces it.')
spirit('debt_crisis','A Foreign-Currency Debt Crisis','External borrowing and refinancing exposure have become a fiscal emergency. Import compression and costly credit now reinforce the contraction.',mm(int=2,build=-.10,cprod=-.06),True,'Native debt ratio above 75% and a recorded external-finance shock, never automatic on 1 January 1970.','Restructuring or a funded adjustment programme replaces the spirit; debt principal remains in the MD economy.')
spirit('adjustment','Austerity and Adjustment','Credit discipline improves refinancing prospects while unemployment fears and public cuts weaken support for the government.',mm(int=-.75,st=-.07,soc=-.04),True,'Debt-crisis adjustment decision, 730 days.','Expires after 730 days; no automatic repayment of debt.')
spirit('war_mobilization','South Atlantic Mobilization','An expeditionary commitment draws on limited trained personnel, spare parts and maritime supply.',mm(org=.06,navy=.05,supply=.12,milcost=.15,st=-.05),True,'Chosen mobilization while at war with the United Kingdom.','Removed when the war ends. Standing peacetime agreements suspend during the war.')
spirit('war_defeat','The Cost of Defeat','A failed South Atlantic campaign leaves the armed forces discredited and families demanding an account of the losses.',mm(st=-.10,pp=-.08,milcost=.06),True,'Peace after actual defeat in the South Atlantic campaign.','Civilian inquiry and veterans settlement remove it; a propaganda focus cannot declare a victory.')
spirit('transition_resistance','Barracks Resistance','Civilian investigations and budget control provoke resistance inside parts of the officer corps.',mm(st=-.05,org=-.04),True,'Accountability option after documented repression, 365 days.','Expires after 365 days or is replaced by a negotiated constitutional settlement.')

def group(key,title,x,y,party=None,description=''):
    g=dict(id=key,title=title,x=x,y=y,party=party,description=description,anchor=None)
    D['groups'].append(g)
    return g
def node(key,title,g,x,y,parents=(),mods=None,money=0,weekly=0,desc='',icon='politics',days=35,remove=(),buildings=(),research=(),event=None,decision=None,require=(),leader=None,temporary=None,replace=None,xp=None,doctrine=None,wargoal=None):
    gg=next(a for a in D['groups'] if a['id']==g)
    n=dict(key=key,id=P+key,title=title,description=desc or title+'.',group=g,x=gg['x']+x,y=gg['y']+y,dx=x,dy=y,anchor=gg['anchor'],
           prerequisites=[[P+p for p in block] if isinstance(block,(tuple,list)) else [P+block] for block in parents],excludes=[],party=gg['party'],
           modifiers=mods or {},money=money,weekly=weekly,remove=[P+r for r in remove],
           buildings=[dict(state=s,type=t,levels=l,slots=l,country='ARG') for s,t,l in buildings],
           research=[dict(category=c,bonus=b,uses=u) for c,b,u in research],event=event,decision=decision,requirements=list(require),icon=icon,
           days=days,cost=days/7,leader=leader,temporary=temporary,replace=replace,xp=xp or {},doctrine=doctrine,wargoal=wargoal,
           lifetime='party' if gg['party'] is not None else 'national',programme=gg['title'],source='history_research.md')
    D['nodes'].append(n)
    if gg['anchor'] is None: gg['anchor']=n['id']
    return n
def ex(*keys):
    for a in keys:
        n=next(n for n in D['nodes'] if n['key']==a)
        n['excludes'] += [P+b for b in keys if b!=a]
def prog(key,title,party,x,y,rows,choices=(),description=''):
    group(key,title,x,y,party,description)
    for row in rows:
        k,t,xx,yy,ps,m,c,w,d,*opts=row
        node(k,t,key,xx,yy,ps,mm(**m),c,w,d,**(opts[0] if opts else {}))
    for pair in choices: ex(*pair)

# Common institutions stand beside party programmes. They do not unlock an already governing party.
group('institutions','The Constitutional Question',136,0,description='Political transitions integrate with the existing leader and election framework. Named leadership changes require a real incumbent transition, not a policy reward.')
node('governability','The Governability Crisis','institutions',0,0,mods=mm(pp=.04,bur=.02),desc='Convene the presidency, provincial authorities and service commanders to assess the political settlement after the Cordobazo.',event='commanders',days=21)
node('electoral_opening','An Electoral Opening','institutions',-4,2,['governability'],mm(st=.04,pp=-.04),money=1,desc='Restore political organization and negotiate a genuinely competitive electoral timetable.',event='opening',require=['Government accepts competitive civilian elections.'])
node('corporate_charter','A Corporate Charter','institutions',4,2,['governability'],mm(pp=.12,st=-.05,bur=.04),money=1,desc='Entrench functional representation under the executive instead of restoring party competition.',replace=('start_regime',None),require=['Authoritarian government.'])
ex('electoral_opening','corporate_charter')
node('hora_pueblo','The Hour of the People','institutions',-6,4,['electoral_opening'],mm(st=.05,pp=-.03),desc='Negotiate an interparty commitment to elections without exclusions and rights for the opposition.',icon='democracy',event='popular_hour')
node('guarded_ballot','A Guarded Ballot','institutions',-2,4,['electoral_opening'],mm(pp=.08,st=-.03),money=1,desc='Offer a competitive ballot with negotiated military guarantees, accepting a less complete break with tutelage.',icon='democracy')
ex('hora_pueblo','guarded_ballot')
node('electoral_register','Restore the Electoral Roll','institutions',-4,6,[('hora_pueblo','guarded_ballot')],mm(bur=.02),money=1,desc='Fund voter registration, scrutiny and a published electoral calendar.',decision='constitutional_election',icon='democracy')
node('functional_councils','Functional Councils','institutions',4,4,['corporate_charter'],mm(cprod=.04,pp=.05,st=-.03),money=2,desc='Give employer, professional and selected labor bodies a place in a state-directed consultative structure.')
node('state_appointments','A Technical State','institutions',4,6,['functional_councils'],mm(build=.04,res=.02,bur=.04),money=2,desc='Protect technical appointments within an authoritarian presidency while concentrating final political authority.')
node('civil_service','Professional Administration','institutions',0,8,[('electoral_register','state_appointments')],mm(bur=-.06),money=2,desc='Set recruitment standards and audit contracts across the national administration.')
node('university_autonomy','University Autonomy','institutions',-4,10,['civil_service'],mm(res=.02,edu=.04),money=2,desc='End political intervention in universities and rebuild protected academic careers.',remove=['start_university'],icon='research')
node('technical_institutes','Technical Institutes','institutions',4,10,['civil_service'],mm(cprod=.04,edu=.03),money=2,desc='Concentrate funding on technical institutes and applied laboratories while retaining closer state direction.',remove=['start_university'],research=[('CAT_industry',.30,1)],icon='research')
ex('university_autonomy','technical_institutes')
node('labor_congress','A National Labor Congress','institutions',0,12,[('university_autonomy','technical_institutes')],mm(st=.03,soc=.03),money=1,desc='Bring unions and employers into a funded settlement on bargaining rights and industrial disputes.',event='labor',remove=['start_cordobazo'])
node('federal_accord','A Federal Fiscal Accord','institutions',0,14,['labor_congress'],mm(tax=.04,bur=.03),money=2,desc='Agree transparent national-provincial transfers and fund the administration needed to enforce them.',icon='bank')
node('civilian_control','Civilian Budget Control','institutions',-4,16,['federal_accord'],mm(milcost=-.06,org=-.02),money=1,desc='Put service procurement and appointments under accountable civilian budget authority.',require=['Competitive constitutional civilian government.'],icon='army')
node('service_guarantees','Service Guarantees','institutions',4,16,['federal_accord'],mm(org=.04,milcost=.05,pp=-.04),desc='Trade protected service budgets for an orderly settlement of the political command question.',icon='army')
ex('civilian_control','service_guarantees')
node('archives','Open the State Archives','institutions',-4,18,['civilian_control'],mm(st=.03,bur=.03),money=1,desc='Preserve and release records of unlawful repression and missing persons.',event='accountability',require=['Documented political repression.','Civilian constitutional government.'])
node('institutional_continuity','Institutional Continuity','institutions',4,18,['service_guarantees'],mm(st=.04,pp=-.03),money=1,desc='Agree a lawful succession and an independent review of service privileges without reopening the entire settlement.')

prog('military','FFAA: Order and Development',22,8,0,[
 ('army_directives','The Commanders\' Directives',0,0,(),{'org':.03,'bur':.02},1,0,'Commission a joint political and readiness review under the actual military government.',{'icon':'army','days':21}),
 ('ongania_corporate','The Organized Community',-4,2,('army_directives',),{'pp':.10,'st':-.04,'cprod':.03},2,0,'Pursue Ongania\'s corporate conception of a disciplined national community.',{'leader':'Juan Carlos Ongania'}),
 ('ferrer_industry','National Industrial Capital',0,2,('army_directives',),{'cprod':.06,'int':.5},3,.002,'Back the nationalist-developmental current associated with Levingston and Aldo Ferrer, prioritizing Argentine suppliers.',{'icon':'industry'}),
 ('lanusse_exit','A Negotiated Exit',4,2,('army_directives',),{'st':.04,'pp':-.03},1,0,'Negotiate a return to civilian competition while seeking defined guarantees for the armed forces.',{'event':'opening'}),
 ('presidency_discipline','Presidential Discipline',-6,4,('ongania_corporate',),{'pp':.08,'police':.06,'st':-.04},1,0,'Expand executive inspection and censorship to enforce a single administrative line.'),
 ('corporate_labor','Recognized Labor Councils',-2,4,('ongania_corporate',),{'out':.04,'soc':.04,'pp':-.03},2,0,'Allow controlled bargaining through recognized industrial councils rather than direct presidential compulsion.'),
 ('local_content','A Local Content Rule',0,4,('ferrer_industry',),{'cap':.05,'gain':-.03},2,0,'Favor local component makers even when the transition slows production.',{'icon':'industry'}),
 ('gran_acuerdo','A Great National Accord',4,4,('lanusse_exit',),{'st':.05,'pp':-.04},1,0,'Offer an enforceable electoral pact to civilian party leaders.',{'decision':'constitutional_election'}),
 ('state_steel','Steel for Development',0,6,('local_content',),{'out':.03,'exp':-.02},4,.001,'Fund heavy industrial suppliers while reserving more output for domestic development.',{'icon':'industry','buildings':[(453,'industrial_complex',1)]}),
 ('order_universities','Applied Research Boards',-4,6,(('presidency_discipline','corporate_labor'),),{'res':.03,'edu':.04},2,0,'Rebuild applied laboratories without granting full academic autonomy.',{'icon':'research','remove':['start_university']}),
 ('legal_parties','Legal Parties and Unions',4,6,('gran_acuerdo',),{'st':.04,'police':-.03},1,0,'Restore lawful organization as a condition of a credible electoral exit.'),
 ('career_officers','A Career Officer Corps',-4,8,('order_universities',),{'org':.05,'pers':.05},2,.001,'Favor predictable promotion and professional tenure over factional appointments.',{'icon':'army'}),
 ('military_factories','Military Factory Network',0,8,('state_steel',),{'arms':.05,'milcost':.03},4,.0015,'Expand Fabricaciones Militares repair and production capacity.',{'icon':'industry','buildings':[(450,'arms_factory',1)]}),
 ('barracks_return','A Return to the Barracks',4,8,('legal_parties',),{'milcost':-.04,'org':.03},1,0,'Arrange professional guarantees and an orderly transfer to the elected government.',{'decision':'civilian_handover'}),
 ('service_rotation','Rotate the Service Commands',-6,10,('career_officers',),{'org':.03,'navy':.03,'pp':-.04},1,0,'Reduce personal command fiefdoms through joint appointments and rotation.',{'icon':'army'}),
 ('presidential_guard','A Presidential Command',-2,10,('career_officers',),{'pp':.10,'org':-.03,'police':.04},1,0,'Centralize command around the presidency at the expense of independent professional initiative.',{'icon':'army'}),
 ('supplier_standard','Supplier Standards',0,10,('military_factories',),{'cap':.04,'gain':-.02},2,0,'Concentrate military procurement on tested domestic components.',{'research':[('CAT_industry',.25,1)],'icon':'industry'}),
 ('continuity_cabinet','A Civilian Technical Cabinet',4,10,('barracks_return',),{'bur':-.04,'res':.02},1,0,'Preserve technical expertise during the handover without preserving military rule.'),
],choices=[('ongania_corporate','ferrer_industry','lanusse_exit'),('presidency_discipline','corporate_labor'),('service_rotation','presidential_guard')])

prog('pj','PJ: The Justicialist Movement',13,24,0,[
 ('social_pact','Negotiate the Social Pact',0,0,(),{'st':.04,'corp':-.02},2,.001,'Bring organized labor, domestic business and the government into a negotiated incomes pact.',{'event':'peronism','remove':['start_cordobazo']}),
 ('union_orthodoxy','The Organized Workers',-4,2,('social_pact',),{'out':.05,'soc':.04},2,.001,'Anchor the movement in recognized unions and enforceable collective agreements.'),
 ('popular_front','A Popular Front',0,2,('social_pact',),{'st':.05,'pp':-.04,'edu':.03},2,.001,'Give youth, neighborhood organizations and reformers a larger place within a civilian mass movement.'),
 ('productive_compact','A Productive Compact',4,2,('social_pact',),{'cprod':.05,'corp':-.03},2,.001,'Make the domestic business sector a formal partner in wages, investment and industrial upgrading.',{'icon':'industry'}),
 ('collective_bargaining','Sector Bargaining',-4,4,('union_orthodoxy',),{'st':.04,'out':.03,'cap':-.02},1,0,'Trade industrial peace and income recovery for less managerial freedom to reorganize production.'),
 ('social_housing','Neighborhood Housing',0,4,('popular_front',),{'st':.04,'soc':.04},3,.002,'Extend housing and local services through accountable neighborhood organizations.',{'icon':'social'}),
 ('gelbard_credit','Credit for National Firms',4,4,('productive_compact',),{'civ':.06,'int':.5},3,.0015,'Direct subsidized credit to domestic small and medium firms, accepting financing pressure.',{'icon':'bank'}),
 ('peron_arbitration','Peron\'s Arbitration',-2,6,(('collective_bargaining','social_housing','gelbard_credit'),),{'pp':.10,'st':.03,'bur':.03},1,0,'Concentrate dispute resolution in Peron\'s personal authority while he is actually in office.',{'leader':'Juan Domingo Peron'}),
 ('cabinet_rules','A Cabinet beyond the Leader',2,6,(('collective_bargaining','social_housing','gelbard_credit'),),{'st':.04,'pp':-.03,'bur':-.02},2,0,'Create collective cabinet and party procedures able to survive a leadership succession.'),
 ('state_enterprises','Public Enterprise Investment',-4,8,(('peron_arbitration','cabinet_rules'),),{'cprod':.04,'bur':.04},4,.002,'Reinvest in publicly controlled suppliers and retain their social obligations.',{'buildings':[(453,'industrial_complex',1)],'icon':'industry'}),
 ('mixed_enterprises','Mixed Enterprise Charters',0,8,(('peron_arbitration','cabinet_rules'),),{'cprod':.03,'trade':.04,'resist':-.04},3,0,'Use mixed ownership and supplier contracts to share investment costs and political influence.',{'icon':'industry'}),
 ('provincial_pj','The Provincial Movement',4,8,(('peron_arbitration','cabinet_rules'),),{'st':.04,'tax':-.03},2,.001,'Fund provincial party and municipal agreements, accepting greater fiscal concessions.'),
 ('workers_training','Union Technical Schools',-2,10,(('state_enterprises','mixed_enterprises'),),{'res':.02,'edu':.04},2,.001,'Link apprenticeships, technical schools and union training.',{'icon':'research','research':[('CAT_industry',.30,1)]}),
 ('food_compact','Food for the Home Market',2,10,('provincial_pj',),{'ag':.05,'exp':-.03,'st':.02},2,.001,'Support domestic food supply while reserving a larger share of output from export channels.',{'icon':'farm'}),
 ('renewal_movement','The Renewal Movement',0,12,('workers_training','food_compact'),{'pp':.05,'st':.03,'bur':.02},1,0,'Reorganize the movement after its succession and electoral crises.',{'require':['A real post-Peron leadership transition has occurred.']}),
 ('renewed_social_pact','Renew the Social Contract',-4,14,('renewal_movement',),{'st':.05,'cprod':.03,'soc':.05},3,.002,'Retain labor guarantees and domestic industry as the core of renewed Justicialism.'),
 ('menem_reform','Popular Market Reform',4,14,('renewal_movement',),{'cprod':.08,'int':-.5,'st':-.05,'corp':-.04},2,0,'Pursue Menem\'s later market turn through an elected Peronist government, accepting conflict with the movement\'s social base.',{'leader':'Carlos Menem','require':['Carlos Menem has actually assumed the presidency; historical route 1989.'],'event':'privatization'}),
 ('welfare_foundations','Public Health Foundations',-4,16,('renewed_social_pact',),{'health':.06,'st':.04},3,.002,'Rebuild hospitals, clinics and a universal public service commitment.',{'icon':'social'}),
 ('regulated_concessions','Regulated Concessions',2,16,('menem_reform',),{'build':.05,'tax':.03,'bur':.03},2,0,'Use enforceable concession contracts and service obligations rather than unconditional asset sales.',{'icon':'bank'}),
 ('rapid_sales','Rapid Asset Sales',6,16,('menem_reform',),{'cprod':.04,'tax':-.04,'st':-.03},0,0,'Raise an immediate receipt by accepting lower retained public income and faster restructuring.',{'decision':'asset_sales','icon':'bank'}),
],choices=[('union_orthodoxy','popular_front','productive_compact'),('peron_arbitration','cabinet_rules'),('state_enterprises','mixed_enterprises'),('renewed_social_pact','menem_reform'),('regulated_concessions','rapid_sales')])

prog('ucr','UCR: A Constitutional Republic',3,40,0,[
 ('radical_committees','Restore the Committees',0,0,(),{'pp':.05,'bur':.02},1,0,'Rebuild the Radical committees as accountable organs of a governing constitutional party.'),
 ('balbin_compromise','Balbin\'s Civic Compromise',-4,2,('radical_committees',),{'st':.05,'pp':-.03},1,0,'Seek a broad civic agreement with the Peronist movement while limiting confrontation with the services.'),
 ('renewal_change','Renewal and Change',4,2,('radical_committees',),{'resist':.06,'pp':.04,'st':-.03},1,0,'Build a reforming Radical current around constitutional rights and resistance to military tutelage.'),
 ('civic_congress','A Congress of Agreements',-4,4,('balbin_compromise',),{'st':.04,'bur':-.03},1,0,'Use committee bargaining and opposition guarantees to secure durable legislation.'),
 ('rights_lawyers','Constitutional Rights',4,4,('renewal_change',),{'st':.03,'police':-.03,'bur':.03},2,0,'Fund legal defense and independent review of detention and censorship.'),
 ('illia_medicines','Medicines and Public Health',-6,6,('civic_congress',),{'health':-.04,'corp':-.03},2,.001,'Use transparent procurement and drug regulation to protect public access.',{'icon':'social'}),
 ('public_oil_rules','Public Oil Contracts',-2,6,('civic_congress',),{'exp':.04,'trade':-.03},2,0,'Renegotiate oil contracts around public oversight and enforceable domestic obligations.',{'icon':'energy'}),
 ('autonomous_campus','The Autonomous Campus',2,6,('rights_lawyers',),{'res':.03,'edu':.05},2,.001,'Restore academic autonomy and scientific appointments.',{'remove':['start_university'],'icon':'research'}),
 ('municipal_republic','A Municipal Republic',6,6,('rights_lawyers',),{'st':.04,'tax':-.02},2,.001,'Strengthen elected local authorities and publish their budgets.'),
 ('republican_school','The Republican School',0,8,(('illia_medicines','public_oil_rules','autonomous_campus','municipal_republic'),),{'res':.02,'edu':.03},2,.001,'Extend civic and technical education without party control of the curriculum.',{'icon':'research'}),
 ('alfonsin_mandate','An Alfonsin Mandate',0,10,('republican_school',),{'st':.04,'pp':.04},1,0,'Use an actual elected Alfonsin presidency to rebuild civilian authority.',{'leader':'Raul Alfonsin','require':['Raul Alfonsin has actually won or lawfully succeeded to the presidency.'],'event':'accountability'}),
 ('conadep','A National Inquiry',-4,12,('alfonsin_mandate',),{'st':.04,'bur':.04},1,0,'Establish an independent commission on disappearances and preserve testimony.',{'require':['Documented disappearances or unlawful repression.'],'event':'accountability'}),
 ('military_accommodation','A Negotiated Reckoning',4,12,('alfonsin_mandate',),{'st':.05,'org':.02,'pp':-.04},1,0,'Prioritize civilian succession through a negotiated settlement that narrows immediate prosecutions.'),
 ('austral_compact','A Stabilization Compact',-4,14,('conadep',),{'int':-.5,'st':-.03,'corp':-.03},2,0,'Seek a negotiated incomes and fiscal stabilization programme; a currency name alone cannot end inflation.',{'event':'stabilization','icon':'bank'}),
 ('fiscal_republic','A Fiscal Republic',4,14,('military_accommodation',),{'tax':.06,'build':-.03,'st':-.02},2,0,'Raise recurring revenue and constrain unfunded promises, accepting resistance from beneficiaries.',{'icon':'bank'}),
 ('democratic_persistence','Democracy under Pressure',0,16,(('austral_compact','fiscal_republic'),),{'st':.04,'pp':.04,'bur':.02},1,0,'Build cross-party commitments to resolve military and economic crises within the constitutional order.'),
],choices=[('balbin_compromise','renewal_change'),('conadep','military_accommodation')])

prog('mid','MID: Integration and Development',2,56,0,[
 ('development_agenda','The Development Agenda',0,0,(),{'cprod':.03,'bur':.02},2,.001,'Make industrial integration, energy and capital formation the governing programme.',{'icon':'industry'}),
 ('foreign_capital','Contract Foreign Capital',-4,2,('development_agenda',),{'civ':.08,'resist':-.06},2,0,'Exchange clear investment contracts and profit remittance rights for industrial capital.',{'icon':'industry'}),
 ('national_savings','Mobilize National Savings',4,2,('development_agenda',),{'cprod':.05,'int':.5,'exp':-.02},3,.001,'Mobilize domestic savings for longer industrial projects with tighter external financing.',{'icon':'bank'}),
 ('petrochemical_chain','The Petrochemical Chain',-4,4,('foreign_capital',),{'cap':.05,'corp':-.03},4,.001,'Develop integrated feedstock and component contracts around the national oil sector.',{'buildings':[(453,'industrial_complex',1)],'icon':'industry'}),
 ('capital_goods','Argentine Capital Goods',4,4,('national_savings',),{'out':.05,'gain':-.03},4,.001,'Invest in machine tools and complex domestic components despite slower initial production.',{'buildings':[(450,'industrial_complex',1)],'icon':'industry'}),
 ('frondizi_bridges','Bridge the Political Divide',0,6,(('petrochemical_chain','capital_goods'),),{'st':.04,'pp':-.04},1,0,'Use developmentalism as a basis for agreements with labor and the mass parties.'),
 ('federal_industry','Federal Industrial Promotion',-4,8,('frondizi_bridges',),{'infra':.06,'tax':-.04},4,.0015,'Distribute industrial incentives and transport investment to regional centers.',{'buildings':[(454,'industrial_complex',1)],'icon':'industry'}),
 ('industrial_corridors','Concentrate the Corridors',4,8,('frondizi_bridges',),{'cprod':.06,'st':-.02},3,.001,'Concentrate limited capital in established industrial corridors instead of equal geographic grants.',{'buildings':[(450,'infrastructure',1)],'icon':'infra'}),
 ('technical_contracts','Technical Training Contracts',0,10,(('federal_industry','industrial_corridors'),),{'res':.03,'edu':.04},2,.001,'Require technology transfer and apprenticeships as part of public contracts.',{'research':[('CAT_industry',.35,1)],'icon':'research'}),
 ('export_manufactures','Export Manufactures',-2,12,('technical_contracts',),{'cprod':.03,'trade':.06,'corp':-.02},2,0,'Provide export certification and credit for manufactures, beyond primary commodity sales.',{'icon':'industry'}),
 ('strategic_substitution','Strategic Substitution',2,12,('technical_contracts',),{'cap':.06,'trade':-.04},2,.001,'Protect selected capital-goods production while accepting a smaller competitive export market.',{'icon':'industry'}),
 ('development_bank','A Development Bank',0,14,(('export_manufactures','strategic_substitution'),),{'build':.04,'bur':.03,'int':.25},3,.0015,'Fund long-maturity productive credit with published selection rules.',{'icon':'bank'}),
],choices=[('foreign_capital','national_savings'),('federal_industry','industrial_corridors'),('export_manufactures','strategic_substitution')])

prog('liberal','PCI: A Liberal Economy',16,72,0,[
 ('liberal_budget','Publish the Real Budget',0,0,(),{'tax':.03,'bur':.02},1,0,'Publish subsidies, guarantees and public liabilities before promising a stable currency.',{'icon':'bank'}),
 ('gradual_opening','A Gradual Opening',-4,2,('liberal_budget',),{'cprod':.04,'trade':.03,'corp':-.02},2,0,'Phase tariff reductions and investment liberalization to limit the shock to domestic industry.'),
 ('shock_opening','Rapid Liberalization',4,2,('liberal_budget',),{'cprod':.07,'trade':.05,'out':-.04,'st':-.05},1,0,'Open credit and product markets rapidly, accepting a difficult industrial adjustment.',{'event':'liberalization'}),
 ('bank_supervision','Prudential Supervision',-4,4,('gradual_opening',),{'int':-.5,'bur':.03},2,0,'Limit connected lending and foreign-currency mismatches before expanding finance.',{'icon':'bank'}),
 ('financial_liberalism','Liberal Financial Markets',4,4,('shock_opening',),{'civ':.07,'int':.75,'resist':-.04},1,0,'Use market credit to mobilize capital while accepting refinancing and foreign-currency exposure.',{'icon':'bank'}),
 ('contract_courts','Enforce the Contracts',0,6,(('bank_supervision','financial_liberalism'),),{'cprod':.03,'bur':.03},2,0,'Provide commercial courts and transparent concession rules.'),
 ('targeted_safety','A Targeted Safety Net',-4,8,('contract_courts',),{'st':.04,'soc':.04,'tax':-.02},2,.001,'Protect households displaced by restructuring without restoring every industrial subsidy.',{'icon':'social'}),
 ('strict_subsidies','End Open-Ended Subsidies',4,8,('contract_courts',),{'tax':.05,'st':-.04,'build':-.02},1,0,'Close recurring industrial support commitments and accept the immediate social backlash.'),
 ('ucede_formation','A Liberal Party Congress',0,10,(('targeted_safety','strict_subsidies'),),{'pp':.07,'bur':.02},1,0,'Create a lawful national liberal party organization from the Alsogaray tradition.',{'require':['Competitive civilian politics.','UCeDe identity requires its actual post-1982 formation, or an explicitly approved earlier divergence.']}),
 ('private_infrastructure','Private Infrastructure',-2,12,('ucede_formation',),{'infra':.07,'tax':-.03},3,0,'Offer time-limited concession incentives with published maintenance obligations.',{'buildings':[(453,'infrastructure',1)],'icon':'infra'}),
 ('productive_tax','A Productive Tax Code',2,12,('ucede_formation',),{'cprod':.04,'corp':-.04},1,0,'Simplify business taxation in exchange for a smaller immediate corporate take.',{'icon':'bank'}),
 ('liberal_republic','The Social Market Republic',0,14,('private_infrastructure','productive_tax'),{'st':.03,'int':-.25,'bur':.02},2,0,'Anchor liberal rules in competitive institutions and enforceable public service contracts.'),
],choices=[('gradual_opening','shock_opening'),('targeted_safety','strict_subsidies')],description='The January 1970 owner is PCI. UCeDe is a later successor identity requiring an explicit approved party reorganization, not an automatic replacement of PD Mendoza.')

prog('conservative','PD: The Provincial Republic',1,88,0,[
 ('cuyo_cabinet','A Cabinet from Cuyo',0,0,(),{'st':.03,'tax':-.02},1,0,'Bring provincial conservative networks into a lawful governing coalition.'),
 ('provincial_autonomy','Provincial Autonomy',-4,2,('cuyo_cabinet',),{'st':.05,'tax':-.04},2,.001,'Strengthen provincial fiscal discretion and accept a smaller national revenue share.'),
 ('commercial_republic','A Commercial Republic',4,2,('cuyo_cabinet',),{'trade':.06,'cprod':.04,'resist':-.03},2,0,'Make clear commercial rules and external market access the basis of conservative government.'),
 ('wine_standards','Wine and Fruit Standards',-4,4,('provincial_autonomy',),{'ag':.06,'bur':.02},2,.001,'Fund inspection, storage and quality control for regional producers.',{'icon':'farm'}),
 ('provincial_credit','Provincial Enterprise Credit',4,4,('commercial_republic',),{'civ':.05,'int':.25},2,.001,'Lend to regional enterprise under audited provincial guarantees.',{'icon':'bank'}),
 ('property_register','A Reliable Property Register',0,6,(('wine_standards','provincial_credit'),),{'tax':.03,'bur':.02},1,0,'Improve land registration and commercial enforcement while exposing privileged holdings.'),
 ('notables_compact','A Compact of Notables',-4,8,('property_register',),{'pp':.09,'st':-.03,'bur':.02},1,0,'Govern through trusted provincial families and established machines.'),
 ('open_councils','Open Provincial Councils',4,8,('property_register',),{'st':.05,'pp':-.03},1,0,'Broaden conservative representation through competitive local councils.'),
 ('cuyo_transport','Cuyo Freight Links',0,10,(('notables_compact','open_councils'),),{'infra':.05,'corp':-.02},3,.001,'Connect regional industry and agriculture to national freight routes.',{'buildings':[(450,'infrastructure',1)],'icon':'infra'}),
 ('federal_conservatism','A Federal Conservatism',0,12,('cuyo_transport',),{'cprod':.03,'st':.02,'bur':.02},1,0,'Bind provincial autonomy to constitutional succession and public accounts.'),
],choices=[('provincial_autonomy','commercial_republic'),('notables_compact','open_councils')])

prog('pdc','PDC: Social Christianity',14,104,0,[
 ('christian_social','A Christian Social Cabinet',0,0,(),{'st':.03,'soc':.03},1,.001,'Build a civilian social programme from Christian-democratic organizations rather than military corporatism.'),
 ('community_reform','Community Reform',-4,2,('christian_social',),{'st':.05,'corp':-.03},2,.001,'Support worker participation and neighborhood organizations through a broad reform coalition.'),
 ('christian_center','An Independent Center',4,2,('christian_social',),{'resist':.07,'pp':-.03},1,0,'Keep an autonomous Christian-democratic center able to bargain with the mass parties.'),
 ('rural_cooperatives','Rural Cooperatives',-4,4,('community_reform',),{'ag':.06,'soc':.03},2,.001,'Fund cooperative machinery, legal titles and extension officers.',{'icon':'farm'}),
 ('social_mediation','Social Mediation Boards',4,4,('christian_center',),{'st':.04,'bur':.03},1,0,'Provide mediation among employers, unions and local communities.'),
 ('plural_schools','Plural Schools',0,6,(('rural_cooperatives','social_mediation'),),{'res':.025,'edu':.04},2,.001,'Fund public and recognized nonprofit schools under common educational standards.',{'icon':'research'}),
 ('worker_ownership','Worker Participation',-4,8,('plural_schools',),{'out':.04,'st':.03,'cap':-.03},2,0,'Give employees formal participation in enterprise decisions.'),
 ('family_enterprise','Family Enterprise Credit',4,8,('plural_schools',),{'cprod':.05,'tax':-.02,'int':.25},2,.001,'Prioritize small family firms and local employment.',{'icon':'bank'}),
 ('community_clinics','Community Clinics',0,10,(('worker_ownership','family_enterprise'),),{'st':.04,'health':.05},3,.002,'Extend primary care through municipal and nonprofit providers.',{'icon':'social'}),
 ('social_republic','A Social Republic',0,12,('community_clinics',),{'st':.03,'resist':.04,'bur':.03},1,0,'Bind social reform to civil liberties and constitutional succession.'),
],choices=[('community_reform','christian_center'),('worker_ownership','family_enterprise')])

prog('pca','PCA: A Workers\' Republic',4,120,0,[
 ('pca_front','A Democratic Workers\' Front',0,0,(),{'st':.03,'pp':.04,'bur':.02},1,0,'Build a civilian governing front with unions, cooperatives and lawful opposition parties.'),
 ('pca_coalition','A Plural Workers\' Coalition',-4,2,('pca_front',),{'st':.05,'pp':-.04,'resist':.03},1,0,'Accept coalition restraints and competitive institutions in exchange for a wider social base.'),
 ('pca_vanguard','A Vanguard State',4,2,('pca_front',),{'pp':.12,'st':-.05,'trade':-.04},1,0,'Concentrate authority in the party, accepting domestic opposition and external distrust.'),
 ('pca_cooperatives','Cooperative Distribution',-4,4,('pca_coalition',),{'ag':.06,'bur':.03},2,.001,'Link producer cooperatives and urban distribution under transparent accounts.',{'icon':'farm'}),
 ('pca_planning','A National Planning Board',4,4,('pca_vanguard',),{'cprod':.06,'bur':.06,'gain':-.03},2,.002,'Direct industrial investment through a centralized plan.',{'icon':'industry'}),
 ('pca_engineers','Engineers for Public Industry',0,6,(('pca_cooperatives','pca_planning'),),{'res':.03,'edu':.05},3,.001,'Expand engineering training for public firms and cooperatives.',{'remove':['start_university'],'icon':'research','research':[('CAT_industry',.35,1)]}),
 ('pca_compensation','Negotiated Public Ownership',-4,8,('pca_engineers',),{'cprod':.04,'int':.25,'trade':.02},4,0,'Compensate transfers of strategic assets and retain commercial access.',{'icon':'industry'}),
 ('pca_expropriation','Immediate Expropriation',4,8,('pca_engineers',),{'cprod':.07,'trade':-.07,'int':.75},1,0,'Transfer major enterprises immediately while accepting legal, management and credit disputes.',{'event':'ownership','icon':'industry'}),
 ('pca_welfare','Universal Public Provision',0,10,(('pca_compensation','pca_expropriation'),),{'st':.04,'health':.04,'soc':.04},3,.002,'Expand universal health and welfare through funded institutions.',{'icon':'social'}),
 ('pca_sovereign','An Independent Socialist Line',-4,12,('pca_welfare',),{'resist':.08,'trade':-.03},1,0,'Keep domestic policy independent of Soviet direction while maintaining commercial ties.'),
 ('pca_moscow','A Soviet Technical Orientation',4,12,('pca_welfare',),{'res':.025,'resist':-.06,'edu':.03},1,0,'Orient training toward Soviet institutions while accepting political and technical dependence.',{'require':['Active Argentine-Soviet academic agreement.']}),
 ('pca_review','Public Plan Review',0,14,(('pca_sovereign','pca_moscow'),),{'cprod':.02,'bur':.02,'pp':-.03},1,0,'Publish enterprise targets and permit workers to challenge failures in the plan.'),
],choices=[('pca_coalition','pca_vanguard'),('pca_compensation','pca_expropriation'),('pca_sovereign','pca_moscow')])

prog('montoneros','Montoneros: Revolutionary Peronism',5,8,18,[
 ('mont_civic','Neighborhood Committees',0,0,(),{'st':.03,'soc':.03},1,.001,'Convert a revolutionary governing mandate into accountable neighborhood organization.'),
 ('mont_ballot','A Civilian Mass Movement',-4,2,('mont_civic',),{'st':.05,'pp':-.04},1,0,'Demobilize clandestine structures and compete through open civilian institutions.'),
 ('mont_command','The Revolutionary Command',4,2,('mont_civic',),{'pp':.10,'st':-.06,'police':.06},1,0,'Retain a centralized revolutionary command and accept continuing political conflict.'),
 ('mont_workplace','Workplace Councils',-4,4,('mont_ballot',),{'out':.04,'soc':.03,'cap':-.02},2,.001,'Give workplace organizations an enforceable role within a constitutional settlement.'),
 ('mont_state','A Revolutionary State Sector',4,4,('mont_command',),{'cprod':.06,'trade':-.05,'bur':.04},2,.001,'Concentrate strategic firms under a revolutionary administration.',{'icon':'industry'}),
 ('mont_schools','Youth Technical Brigades',0,6,(('mont_workplace','mont_state'),),{'res':.025,'edu':.04},2,.001,'Turn youth mobilization toward technical education and public services.',{'icon':'research'}),
 ('mont_church','Social Christian Networks',-4,8,('mont_schools',),{'st':.04,'health':.04},2,.001,'Work with progressive clergy and lay networks without making the Church a single political bloc.',{'icon':'social'}),
 ('mont_secular','A Secular Popular Front',4,8,('mont_schools',),{'pp':.07,'bur':.03,'st':-.02},1,0,'Build a secular coalition able to incorporate independent revolutionary currents.'),
 ('mont_civic_services','Municipal Public Works',0,10,(('mont_church','mont_secular'),),{'infra':.04,'soc':.03},3,.001,'Fund municipal services under published local accounts.',{'buildings':[(453,'infrastructure',1)],'icon':'infra'}),
 ('mont_pluralism','A Popular Constitution',0,12,('mont_civic_services',),{'st':.04,'pp':-.03,'resist':.04},1,0,'Submit the governing settlement to a real constitutional process rather than claiming permanent revolutionary authority.'),
],choices=[('mont_ballot','mont_command'),('mont_church','mont_secular')],description='Major alternate history: an armed movement is not a normal 1970 electoral party. Government requires an approved real settlement, victory or transition through existing politics, never a focus-only coup.')

prog('prt','PRT: The Revolutionary Left',19,24,18,[
 ('prt_congress','A Workers\' Congress',0,0,(),{'pp':.05,'bur':.03},1,0,'Convene a governing workers\' congress after a real political transition.'),
 ('prt_pluralism','A Plural Workers\' Government',-4,2,('prt_congress',),{'st':.05,'pp':-.04},1,0,'Accept independent unions and open political competition.'),
 ('prt_revolution','Permanent Revolutionary Rule',4,2,('prt_congress',),{'pp':.12,'trade':-.06,'st':-.05},1,0,'Concentrate revolutionary authority at the cost of pluralism and market access.'),
 ('prt_factory_councils','Factory Councils',-4,4,('prt_pluralism',),{'out':.05,'cap':-.03,'soc':.02},2,.001,'Give elected councils control over workplace standards and production plans.'),
 ('prt_central_plan','A Central Industrial Plan',4,4,('prt_revolution',),{'cprod':.07,'bur':.06,'gain':-.03},3,.001,'Use a central authority to allocate industrial capital and inputs.',{'icon':'industry'}),
 ('prt_literacy','Workers\' Technical Education',0,6,(('prt_factory_councils','prt_central_plan'),),{'res':.03,'edu':.05},2,.001,'Expand technical education without treating Argentina as an illiterate agrarian society.',{'icon':'research'}),
 ('prt_land_coops','Agricultural Cooperatives',-4,8,('prt_literacy',),{'ag':.07,'bur':.03,'exp':-.02},2,.001,'Fund cooperative production and domestic food supply.',{'icon':'farm'}),
 ('prt_city_industry','Concentrate Urban Industry',4,8,('prt_literacy',),{'out':.05,'ag':-.03,'soc':.03},3,.001,'Prioritize the industrial working class while accepting weaker agricultural incentives.',{'icon':'industry'}),
 ('prt_nonalignment','Revolutionary Nonalignment',0,10,(('prt_land_coops','prt_city_industry'),),{'resist':.08,'trade':-.03},1,0,'Seek foreign contacts without accepting another power\'s control over domestic policy.'),
 ('prt_civil_administration','A Civil Administration',0,12,('prt_nonalignment',),{'bur':-.04,'pp':-.03,'st':.03},2,0,'Replace emergency command with a documented and reviewable civil administration.'),
],choices=[('prt_pluralism','prt_revolution'),('prt_land_coops','prt_city_industry')],description='PRT exists in January 1970. ERP is a later 1970 formation and is not retroactively treated as a starting regular army or party. This governing route is a large alternate-history divergence.')

prog('cgta','CGTA: Combative Labor',18,40,18,[
 ('cgta_mandate','A Shop-Floor Mandate',0,0,(),{'st':.04,'soc':.03},1,.001,'Make independent workplace representation a governing commitment.',{'remove':['start_cordobazo']}),
 ('cgta_councils','Independent Workers\' Councils',-4,2,('cgta_mandate',),{'out':.05,'cap':-.03},2,0,'Give shop-floor delegates a binding role in enterprise policy.'),
 ('cgta_coalition','A Democratic Labor Coalition',4,2,('cgta_mandate',),{'st':.05,'pp':-.04},1,0,'Share government with independent civilian reformers rather than subordinating them to the confederation.'),
 ('cgta_cordoba','Cordoba Industrial Skills',-4,4,('cgta_councils',),{'res':.025,'edu':.04},2,.001,'Fund skilled apprenticeships in the industrial interior.',{'icon':'research','research':[('CAT_industry',.25,1)]}),
 ('cgta_local','Elected Municipal Services',4,4,('cgta_coalition',),{'st':.03,'soc':.04},2,.001,'Put local services under elected and audited administration.',{'icon':'social'}),
 ('cgta_public_credit','Public Credit for Cooperatives',0,6,(('cgta_cordoba','cgta_local'),),{'cprod':.04,'int':.25},2,.001,'Provide accountable credit to worker cooperatives.',{'icon':'bank'}),
 ('cgta_independent','Autonomous Unions',-4,8,('cgta_public_credit',),{'st':.04,'pp':-.04},1,0,'Protect unions from control by the governing movement itself.'),
 ('cgta_corporate','A Labor State',4,8,('cgta_public_credit',),{'pp':.09,'bur':.04,'st':-.03},1,0,'Give labor institutions a permanent privileged role in state authority.'),
 ('cgta_health','Occupational Health',0,10,(('cgta_independent','cgta_corporate'),),{'st':.03,'health':.05},2,.0015,'Fund industrial clinics and enforce workplace health standards.',{'icon':'social'}),
 ('cgta_front','A Republic of Labor',0,12,('cgta_health',),{'out':.03,'soc':.02,'bur':.02},1,0,'Bind the labor programme to durable civil institutions.'),
],choices=[('cgta_councils','cgta_coalition'),('cgta_independent','cgta_corporate')])

prog('unions','62 Organizations: Organized Labor',20,56,18,[
 ('union_mandate','The Union Mandate',0,0,(),{'st':.04,'soc':.03},1,.001,'Make collective bargaining and employment guarantees the basis of a union-led government.',{'remove':['start_cordobazo']}),
 ('union_pact','A Bargained Production Pact',-4,2,('union_mandate',),{'out':.05,'corp':-.03},2,.001,'Offer disciplined production in exchange for wages, benefits and recognition.'),
 ('union_primacy','Union Primacy',4,2,('union_mandate',),{'pp':.10,'cap':-.03,'bur':.03},1,0,'Give recognized confederations privileged influence over appointments and industrial decisions.'),
 ('union_insurance','Union Social Insurance',-4,4,('union_pact',),{'health':.05,'st':.04},2,.0015,'Expand union health and insurance institutions with enforceable accounts.',{'icon':'social'}),
 ('union_officials','Train Union Administrators',4,4,('union_primacy',),{'bur':-.03,'edu':.03},2,.001,'Train the administrators needed to run a powerful union apparatus.',{'icon':'research'}),
 ('union_industry','Industrial Bargaining Boards',0,6,(('union_insurance','union_officials'),),{'gain':.04,'soc':.03},1,0,'Coordinate retraining and investment within sector agreements.',{'icon':'industry'}),
 ('union_democracy','Secret-Ballot Union Elections',-4,8,('union_industry',),{'st':.05,'pp':-.04},1,0,'Make union office dependent on a genuine membership ballot.'),
 ('union_apparatus','A Disciplined Confederation',4,8,('union_industry',),{'pp':.09,'st':-.03,'bur':.03},1,0,'Preserve a unified bargaining apparatus under established officials.'),
 ('union_apprentices','Apprenticeship Guarantees',0,10,(('union_democracy','union_apparatus'),),{'res':.02,'edu':.04},2,.001,'Tie protected jobs to funded technical training.',{'icon':'research'}),
 ('union_welfare','A Durable Labor Settlement',0,12,('union_apprentices',),{'st':.03,'out':.02,'soc':.03},1,.001,'Finance the obligations that make the labor compact credible beyond one administration.'),
],choices=[('union_pact','union_primacy'),('union_democracy','union_apparatus')])

prog('catholic','Ateneo: Catholic Corporatism',6,72,18,[
 ('athenaeum','The Athenaeum Cabinet',0,0,(),{'pp':.06,'bur':.03},1,0,'Turn the Catholic corporatist intellectual network into a governing programme without claiming to speak for all Argentine Catholics.'),
 ('subsidiarity','Subsidiarity in Practice',-4,2,('athenaeum',),{'st':.04,'tax':-.03},2,.001,'Delegate social provision to municipalities, families and nonprofit institutions.'),
 ('corporate_state','A Corporate State',4,2,('athenaeum',),{'pp':.10,'st':-.04,'bur':.03},1,0,'Organize recognized social corporations under a strong national executive.'),
 ('social_catholic','Catholic Social Institutions',-4,4,('subsidiarity',),{'health':.04,'soc':.03,'st':.03},2,.001,'Fund plural social institutions under public service standards.',{'icon':'social'}),
 ('professional_orders','Professional Orders',4,4,('corporate_state',),{'cprod':.04,'res':-.02,'bur':.03},2,0,'Give recognized professional bodies authority over entry and certification.'),
 ('catholic_technical','Technical Colleges',0,6,(('social_catholic','professional_orders'),),{'res':.025,'edu':.04},2,.001,'Expand technical colleges while maintaining public qualification standards.',{'icon':'research'}),
 ('church_mediation','A Social Mediation Charter',0,8,('catholic_technical',),{'st':.04,'pp':-.03,'bur':.02},1,0,'Protect mediation among labor, business and religious social institutions.'),
 ('corporatist_settlement','The Corporate Settlement',0,10,('church_mediation',),{'cprod':.03,'soc':.03,'trade':-.02},2,.001,'Fund the obligations of a negotiated corporate order.'),
],choices=[('subsidiarity','corporate_state')],description='An alternate governing intellectual network, distinct from the Christian Democratic Party and from Church hierarchy as a whole.')

prog('udelpa','UDELPA: An Ordered Republic',0,88,18,[
 ('udelpa_order','Order and the Republic',0,0,(),{'pp':.06,'st':-.02},1,0,'Build a civilian anti-Peronist governing coalition from UDELPA\'s existing networks.'),
 ('udelpa_competition','Accept Open Competition',-4,2,('udelpa_order',),{'st':.05,'pp':-.04},1,0,'Accept Peronist participation under constitutional guarantees.'),
 ('udelpa_exclusion','Retain Political Exclusions',4,2,('udelpa_order',),{'pp':.10,'st':-.07,'police':.04},1,0,'Keep the mass Peronist movement outside normal competition and carry the legitimacy cost.'),
 ('udelpa_courts','Courts above the Executive',-4,4,('udelpa_competition',),{'bur':.03,'st':.03},1,0,'Protect legal review of executive decisions and detention.'),
 ('udelpa_guardians','Guardians of Public Order',4,4,('udelpa_exclusion',),{'police':.06,'pp':.06,'st':-.03},1,.001,'Expand security administration under a restrictive political settlement.'),
 ('udelpa_commerce','Commercial Rehabilitation',0,6,(('udelpa_courts','udelpa_guardians'),),{'cprod':.04,'trade':.03,'resist':-.03},2,0,'Offer predictable commercial contracts and external investment rules.'),
 ('udelpa_profession','Professional Public Service',0,8,('udelpa_commerce',),{'bur':-.04,'edu':.02},2,0,'Use open qualifications for technical administration.',{'icon':'research'}),
 ('udelpa_succession','A Lawful Succession',0,10,('udelpa_profession',),{'st':.03,'pp':-.02},1,0,'Bind the executive to a published succession procedure rather than a permanent personal mandate.'),
],choices=[('udelpa_competition','udelpa_exclusion')],description='Aramburu is an early historical actor, not an immortal route requirement. A real death or leadership succession continues through the party network.')

prog('sra','SRA: The Exporting Countryside',15,104,18,[
 ('rural_cabinet','The Exporting Countryside',0,0,(),{'ag':.04,'corp':-.02},1,0,'Give organized agricultural interests a governing voice without treating the rural association as a mass electoral party.',{'icon':'farm'}),
 ('export_incentives','Lower Export Levies',-4,2,('rural_cabinet',),{'ag':.07,'tax':-.05},2,0,'Improve incentives to expand agricultural output at a cost to retained public revenue.',{'icon':'farm'}),
 ('rural_revenue','A Productive Revenue Pact',4,2,('rural_cabinet',),{'ag':.04,'tax':.03,'bur':.02},2,.001,'Trade stable levies for extension services and predictable export rules.',{'icon':'farm'}),
 ('cattle_health','Animal Health and Cold Storage',-4,4,('export_incentives',),{'ag':.05,'health':.02},3,.001,'Fund veterinary inspection and reliable meat handling.',{'buildings':[(453,'agriculture_district',1)],'icon':'farm'}),
 ('rural_roads','Rural Freight Roads',4,4,('rural_revenue',),{'infra':.05,'bur':.02},3,.001,'Connect grain and livestock producers to storage and ports.',{'buildings':[(453,'infrastructure',1)],'icon':'infra'}),
 ('rural_land','A Published Land Register',0,6,(('cattle_health','rural_roads'),),{'ag':.03,'tax':.02,'bur':.02},1,0,'Make property, irrigation and credit claims legible to the state.',{'icon':'farm'}),
 ('estate_services','Estate-Led Modernization',-4,8,('rural_land',),{'ag':.06,'st':-.03,'corp':-.02},2,0,'Concentrate incentives in large efficient operations and accept opposition from smaller producers.',{'icon':'farm'}),
 ('small_producer','Small Producer Extension',4,8,('rural_land',),{'ag':.04,'st':.03,'soc':.03},2,.001,'Spread agronomy and machinery access to smaller producers.',{'icon':'farm'}),
],choices=[('export_incentives','rural_revenue'),('estate_services','small_producer')])

prog('socialist','PSD: Democratic Socialism','PS',120,18,[
 ('socialist_coalition','A Socialist Coalition',0,0,(),{'st':.04,'pp':-.03},1,0,'Form a constitutional governing coalition around the Democratic Socialist tradition, not a renamed labor confederation.'),
 ('socialist_parliament','Parliamentary Socialism',-4,2,('socialist_coalition',),{'st':.05,'bur':.02,'pp':-.03},1,0,'Build reform through parliamentary agreements and independent civil associations.'),
 ('socialist_labor','A Labor-Socialist Cabinet',4,2,('socialist_coalition',),{'out':.04,'soc':.03,'corp':-.02},2,.001,'Give independent unions a wider role without handing the confederation exclusive state authority.'),
 ('socialist_coops','Municipal Cooperatives',-4,4,('socialist_parliament',),{'cprod':.04,'bur':.03},2,.001,'Expand cooperative utilities and publish their accounts.'),
 ('socialist_insurance','Public Social Insurance',4,4,('socialist_labor',),{'st':.04,'health':.05},2,.002,'Extend social insurance to workers outside the strongest organized sectors.',{'icon':'social'}),
 ('socialist_school','Secular Public Education',0,6,(('socialist_coops','socialist_insurance'),),{'res':.03,'edu':.05},2,.001,'Rebuild public education and academic freedom.',{'remove':['start_university'],'icon':'research'}),
 ('socialist_tax','A Progressive Revenue Law',-4,8,('socialist_school',),{'tax':.05,'cprod':-.02,'bur':.02},1,0,'Finance redistribution through a broader and more progressive revenue base.',{'icon':'bank'}),
 ('socialist_growth','A Cooperative Growth Pact',4,8,('socialist_school',),{'cprod':.05,'corp':-.03},2,.001,'Trade targeted incentives for cooperative ownership and formal employment.'),
 ('socialist_housing','Municipal Housing Funds',0,10,(('socialist_tax','socialist_growth'),),{'st':.04,'soc':.04},3,.0015,'Finance housing and basic local services under elected municipal control.',{'icon':'social'}),
 ('socialist_audit','Audit Public Enterprise',0,12,('socialist_housing',),{'bur':-.03,'pp':-.02,'cprod':.02},1,0,'Give parliament and independent auditors access to public enterprise accounts.'),
],choices=[('socialist_parliament','socialist_labor'),('socialist_tax','socialist_growth')],description='PROVISIONAL identity integration: PSD is absent from current registry. Design uses a distinct approved incumbent identity under slot 18, mutually exclusive with CGTA as incumbent. No fictitious live ideology/party slot is created. PSP is only a later 1972 formation, not the January 1970 name.')

group('economy','Industry, Food and the External Account',154,0)
node('economic_survey','The National Economic Survey','economy',0,0,mods=mm(bur=.02),money=1,desc='Audit industrial capacity, external finance and regional services before allocating scarce public investment.',icon='bank',days=21)
node('incomes_compact','An Incomes Compact','economy',-4,2,['economic_survey'],mm(st=.03,corp=-.03,bur=.02),money=2,desc='Negotiate wages, prices and fiscal restraint with employers and labor.',remove=['start_stopgo'],event='stabilization',icon='bank')
node('monetary_discipline','Monetary Discipline','economy',4,2,['economic_survey'],mm(int=-.5,cprod=-.02,st=-.03),money=2,desc='Restrict inflationary financing while accepting slower activity and resistance from affected groups.',remove=['start_stopgo'],event='stabilization',icon='bank')
ex('incomes_compact','monetary_discipline')
node('banking_rules','Foreign-Currency Bank Rules','economy',0,4,[('incomes_compact','monetary_discipline')],mm(int=-.25,bur=.02),money=1,desc='Audit foreign-currency liabilities, connected lending and public guarantees.',icon='bank')
node('public_integration','Integrated Public Industry','economy',-6,6,['banking_rules'],mm(cprod=.05,bur=.04),money=5,weekly=.002,desc='Coordinate steel, machine tools and public enterprise investment around enforceable industrial targets.',buildings=[(453,'industrial_complex',1)],icon='industry')
node('mixed_industry','A Mixed Industrial System','economy',0,6,['banking_rules'],mm(cprod=.04,corp=-.02,resist=-.02),money=4,weekly=.001,desc='Share industrial expansion among public firms, domestic private capital and selected external suppliers.',buildings=[(450,'industrial_complex',1)],icon='industry')
node('export_industry','Export-Oriented Industry','economy',6,6,['banking_rules'],mm(cprod=.05,trade=.05,out=-.03),money=3,desc='Prioritize competitive export manufacturers while withdrawing protection from less efficient producers.',buildings=[(453,'industrial_complex',1)],icon='industry')
ex('public_integration','mixed_industry','export_industry')
node('public_suppliers','Public Supplier Contracts','economy',-6,8,['public_integration'],mm(cap=.04,bur=.02),money=2,desc='Use published contracts to strengthen technical standards in public procurement.',research=[('CAT_industry',.25,1)],icon='industry')
node('supplier_jointventures','Supplier Joint Ventures','economy',0,8,['mixed_industry'],mm(gain=.04,resist=-.03),money=2,desc='Require local supplier training in mixed industrial ventures.',research=[('CAT_industry',.30,1)],icon='industry')
node('export_certification','Export Certification','economy',6,8,['export_industry'],mm(cprod=.02,bur=.02),money=1,desc='Fund quality assurance, testing and export documentation.',research=[('CAT_industry',.25,1)],icon='industry')
node('rail_freight','Rail Freight Rehabilitation','economy',0,10,[('public_suppliers','supplier_jointventures','export_certification')],mm(supply=-.03),money=4,weekly=.001,desc='Rehabilitate the freight corridors that connect inland industry and farms to the ports.',buildings=[(450,'infrastructure',1),(453,'infrastructure',1)],icon='infra')
node('export_farms','Competitive Export Farms','economy',-4,12,['rail_freight'],mm(ag=.07,tax=-.03),money=3,desc='Support agronomy, storage and export quality while limiting the fiscal burden on producers.',buildings=[(453,'agriculture_district',1)],icon='farm')
node('food_security','Food and Small Producers','economy',4,12,['rail_freight'],mm(ag=.05,st=.03,soc=.03),money=3,weekly=.001,desc='Prioritize extension, food access and smaller producers over the largest export operations.',buildings=[(448,'agriculture_district',1)],icon='farm')
ex('export_farms','food_security')
node('cold_chain','Cold Storage and Inspection','economy',-4,14,['export_farms'],mm(ag=.03,health=.02),money=2,weekly=.001,desc='Reduce losses and maintain export access through refrigeration and veterinary inspection.',icon='farm')
node('rural_credit','Rural Extension Credit','economy',4,14,['food_security'],mm(ag=.03,bur=.03),money=2,weekly=.001,desc='Link agricultural credit to extension support and reliable producer records.',icon='farm')
node('federal_corridors','Northern and Southern Links','economy',0,16,[('cold_chain','rural_credit')],mm(infra=.03),money=5,weekly=.0015,desc='Fund freight and public services beyond the established littoral corridors.',remove=['start_geography'],buildings=[(449,'infrastructure',1),(454,'infrastructure',1)],icon='infra')
node('fuego_incentives','The Fuegian Promotion Zone','economy',-4,18,['federal_corridors'],mm(civ=.05,tax=-.04,soc=.02),money=4,weekly=.0015,desc='Create an industrial promotion area in Tierra del Fuego through tax privileges and public services.',buildings=[(457,'industrial_complex',1)],icon='industry')
node('regional_equalization','Regional Service Equalization','economy',4,18,['federal_corridors'],mm(st=.04,soc=.04,infra=.03),money=4,weekly=.002,desc='Distribute service and infrastructure grants across the interior instead of concentrating a special customs regime.',buildings=[(449,'infrastructure',1)],icon='infra')
ex('fuego_incentives','regional_equalization')
node('gas_network','A National Gas Network','economy',-4,20,['fuego_incentives'],mm(cprod=.03,bur=.02),money=4,weekly=.0015,desc='Improve gas distribution and industrial supply; the focus does not invent automatic raw gas production.',buildings=[(454,'fossil_powerplant',1)],icon='energy')
node('grid_security','Grid and Energy Reliability','economy',4,20,['regional_equalization'],mm(build=.03,bur=.02),money=4,weekly=.0015,desc='Fund firm power and distribution reliability for regional development.',buildings=[(450,'fossil_powerplant',1)],icon='energy')
node('statistical_office','Independent Economic Statistics','economy',0,22,[('gas_network','grid_security')],mm(bur=.02,int=-.25),money=1,desc='Publish consistent budget, debt and national-account statistics without resetting the actual MD economy.',icon='bank')
node('reserve_buffer','An External Reserve Buffer','economy',-4,24,['statistical_office'],mm(int=-.5,build=-.03),money=5,desc='Commit fiscal space to resilience instead of immediate capital spending.',decision='debt_restructuring',icon='bank')
node('investment_push','A New Investment Push','economy',4,24,['statistical_office'],mm(build=.06,int=.5),money=5,weekly=.0015,desc='Commit resources to another investment cycle while accepting financing exposure.',buildings=[(450,'industrial_complex',1)],decision='crisis_adjustment',icon='industry')
ex('reserve_buffer','investment_push')

group('defence','The Armed Forces and National Industry',174,0)
node('joint_review','A Joint Readiness Review','defence',0,0,mods=mm(bur=.02),money=1,desc='Review the three services\' logistics, procurement and readiness requirements.',icon='army',days=21)
node('territorial_army','Territorial Deterrence','defence',-6,2,['joint_review'],mm(defense=.10,supply=-.04,speed=-.03),money=2,desc='Favor prepared positions and reliable regional supply over expeditionary reach.',icon='army',doctrine=('land_doctrine',.25,1))
node('mobile_army','A Mobile Strategic Reserve','defence',-2,2,['joint_review'],mm(speed=.07,rec=.04,supply=.06),money=3,weekly=.001,desc='Build a mobile response force that can reinforce distant provinces.',icon='army',doctrine=('land_doctrine',.25,1))
ex('territorial_army','mobile_army')
node('coastal_navy','A Sea-Denial Navy','defence',2,2,['joint_review'],mm(navy=.06,dock=.04,milcost=.03),money=3,weekly=.001,desc='Concentrate on coastal defense, submarines and maritime denial rather than sustained ocean presence.',icon='navy',doctrine=('naval_doctrine',.25,1))
node('ocean_navy','An Ocean-Going Navy','defence',6,2,['joint_review'],mm(navy=.08,milcost=.07,supply=.03),money=5,weekly=.002,desc='Fund sustained fleet operations and escort training for wider South Atlantic reach.',icon='navy',doctrine=('naval_doctrine',.25,1))
ex('coastal_navy','ocean_navy')
node('professional_ncos','Professional NCOs','defence',-4,4,[('territorial_army','mobile_army')],mm(org=.06,train=.06,pers=.05),money=2,weekly=.001,desc='Retain experienced small-unit leaders through longer training and professional careers.',icon='army',xp={'army':20})
node('naval_maintenance','Naval Maintenance Standards','defence',4,4,[('coastal_navy','ocean_navy')],mm(dock=.05,bur=.02),money=3,weekly=.001,desc='Fund planned refits and common maintenance standards across the fleet.',buildings=[(453,'dockyard',1)],icon='navy',xp={'navy':20})
node('joint_staff','A Permanent Joint Staff','defence',0,6,['professional_ncos','naval_maintenance'],mm(org=.02,navy=.02,bur=.03),money=2,desc='Give the services a common operational planning and logistics staff.',remove=['start_command'],icon='army')
node('tam_programme','The Medium Tank Programme','defence',-6,8,['joint_staff'],mm(cap=.05,gain=-.03),money=4,weekly=.001,desc='Develop the industrial and testing base for a domestically supported medium tank.',research=[('CAT_tanks',.35,1)],icon='tank')
node('military_repairs','Distributed Repair Depots','defence',-2,8,['joint_staff'],mm(rec=.05,supply=-.03,bur=.03),money=3,weekly=.001,desc='Prioritize repair and sustainment rather than a new armored production line.',buildings=[(450,'arms_factory',1)],icon='industry')
ex('tam_programme','military_repairs')
node('air_interception','Airspace Interception','defence',2,8,['joint_staff'],mm(detect=.10,air=.03,milcost=.03),money=3,weekly=.001,desc='Improve warning, radar coverage and interceptor readiness.',buildings=[(454,'radar_station',1)],icon='air')
node('naval_air','Naval Air Cooperation','defence',6,8,['joint_staff'],mm(air=.06,navy=.02,supply=.04),money=3,weekly=.001,desc='Train the air and naval services for reconnaissance and maritime operations.',research=[('CAT_aircraft',.25,1)],icon='air')
ex('air_interception','naval_air')
node('fma_engineers','FMA Engineering Capacity','defence',-4,10,[('tam_programme','military_repairs')],mm(res=.02,edu=.03),money=3,weekly=.001,desc='Expand design, tooling and maintenance skills around the existing aeronautical industry.',research=[('CAT_aircraft',.35,1)],icon='air')
node('spares_stock','A Strategic Spare-Parts Stock','defence',4,10,[('air_interception','naval_air')],mm(air=.03,navy=.03,milcost=.04),money=3,weekly=.001,desc='Fund the maintenance reserve needed when foreign supply becomes politically uncertain.',icon='industry')
node('supplier_review','Choose a Procurement Basis','defence',0,12,['fma_engineers','spares_stock'],mm(bur=.02),money=1,desc='Compare complete lifecycle costs and supplier conditions before signing the next procurement programme.',icon='industry')
node('french_standard','A French Technical Standard','defence',-4,14,['supplier_review'],mm(air=.04,resist=-.03,milcost=.03),money=2,desc='Standardize maintenance and training around accepted French cooperation.',require=['Active Franco-Argentine aviation agreement.'],research=[('CAT_aircraft',.30,1)],icon='air')
node('american_standard','An American Technical Standard','defence',0,14,['supplier_review'],mm(org=.04,resist=-.04,pers=.02),money=2,desc='Adopt the training and maintenance arrangements agreed with the United States.',require=['Active US-Argentine training agreement.'],xp={'army':20},icon='army')
node('domestic_standard','A Sovereign Supplier Base','defence',4,14,['supplier_review'],mm(out=.05,cap=.04,int=.25),money=5,weekly=.0015,desc='Pay the higher development cost of a more autonomous domestic supplier network.',buildings=[(450,'arms_factory',1)],icon='industry')
ex('french_standard','american_standard','domestic_standard')
node('defence_accounts','Published Defense Accounts','defence',0,16,[('french_standard','american_standard','domestic_standard')],mm(milcost=-.04,bur=.02),money=1,desc='Publish audited lifecycle budgets and prevent procurement promises from exceeding the funded force.',icon='army')

group('science','CNEA, Universities and the Fuel Cycle',174,20)
node('cnea_mandate','The CNEA Mandate','science',0,0,mods=mm(reactor=.05,edu=.02),money=2,weekly=.001,desc='Fund the established civilian nuclear institution and the engineers needed for power and fuel development.',icon='nuclear')
node('reactor_partners','International Reactor Contracts','science',-4,2,['cnea_mandate'],mm(reactor=.10,resist=-.04),money=3,desc='Use commercial reactor contracts and safeguards to accelerate civilian deployment.',research=[('CAT_nuclear_reactors',.35,1)],icon='nuclear')
node('national_fuel','A National Fuel Capability','science',4,2,['cnea_mandate'],mm(res=.025,reactor=.05,bur=.04),money=4,weekly=.0015,desc='Invest in indigenous civilian fuel expertise while bearing higher technical and diplomatic costs.',research=[('CAT_nuclear_reactors',.25,1)],icon='nuclear')
ex('reactor_partners','national_fuel')
node('atucha_training','Atucha Operations Training','science',-4,4,['reactor_partners'],mm(res=.02,edu=.03),money=2,weekly=.001,desc='Train operators, inspectors and maintenance engineers for civilian reactors. No completed plant is granted by a historical name.',icon='nuclear')
node('fuel_laboratories','Fuel Laboratories','science',4,4,['national_fuel'],mm(res=.025,edu=.04),money=3,weekly=.0015,desc='Develop civilian fuel testing, materials and quality assurance.',icon='nuclear')
node('uranium_survey','Survey the Uranium Deposits','science',0,6,[('atucha_training','fuel_laboratories')],money=2,desc='Finance a geological survey of the Los Gigantes area before any paid mine development.',decision='uranium_survey',icon='nuclear')
node('uranium_development','Develop a Surveyed Mine','science',-4,8,['uranium_survey'],money=4,weekly=.001,desc='Fund a mine only after a successful survey and an approved environmental and capacity review.',decision='uranium_mine',require=['A surveyed deposit exists in Cordoba.','Argentina owns and controls the target state.'],icon='nuclear')
node('uranium_imports','Diversify Fuel Imports','science',4,8,['uranium_survey'],mm(reactor=.05,trade=.03,resist=-.03),money=2,weekly=.002,desc='Prefer diversified fuel purchasing to a new domestic mine, accepting external dependence.',icon='nuclear')
ex('uranium_development','uranium_imports')
node('civil_safeguards','Civilian Safeguards','science',0,10,[('uranium_development','uranium_imports')],mm(trade=.03,bur=.03),money=1,desc='Publish civilian accounting and inspection commitments; this programme grants no nuclear weapon.',icon='nuclear')
node('brazil_inspections','Reciprocal Nuclear Visits','science',-4,12,['civil_safeguards'],mm(res=.02,resist=.03,bur=.02),money=1,desc='Build mutual confidence through the actual active nuclear cooperation with Brazil.',require=['Active Argentine-Brazilian nuclear cooperation spirit.'],icon='nuclear')
node('scientific_autonomy','Scientific Autonomy','science',4,12,['civil_safeguards'],mm(res=.03,edu=.05,trade=-.03),money=3,weekly=.0015,desc='Retain a more autonomous civilian research programme and accept its higher cost and diplomatic friction.',icon='research')
ex('brazil_inspections','scientific_autonomy')
node('computing_institutes','Computing Institutes','science',0,14,[('brazil_inspections','scientific_autonomy')],mm(res=.02,edu=.03),money=3,weekly=.001,desc='Rebuild university computing and public scientific data services.',research=[('CAT_computing',.35,1)],icon='research')
node('research_exchange','An Academic Exchange Office','science',0,16,['computing_institutes'],mm(res=.015,bur=.02),money=1,desc='Coordinate scholarships and research access under signed bilateral academic agreements.',icon='research')

group('diplomacy','Partners across the Cold War',194,0)
node('sanmartin_desk','The San Martin Palace Desk','diplomacy',0,0,mods=mm(bur=.02),money=1,desc='Equip the foreign ministry to negotiate commercial, technical and security agreements with actual partner governments.',icon='diplomacy',days=21)
node('continental_cooperation','Continental Cooperation','diplomacy',-4,2,['sanmartin_desk'],mm(trade=.05,resist=-.03),money=1,desc='Prioritize reciprocal regional agreements and accept constraints on unilateral policy.',icon='diplomacy')
node('continental_balance','A Continental Balance','diplomacy',4,2,['sanmartin_desk'],mm(resist=.07,trade=-.03),money=1,desc='Keep greater national discretion and negotiate individual agreements without a regional integration commitment.',icon='diplomacy')
ex('continental_cooperation','continental_balance')
node('brazil_trade','A Brazilian Industrial Accord','diplomacy',-6,4,['continental_cooperation'],desc='Offer reciprocal industrial standards, supplier exchanges and funded customs administration to Brazil.',icon='brazil')
node('brazil_nuclear','A Brazilian Nuclear Accord','diplomacy',-6,6,['brazil_trade'],desc='Offer Brazil civilian nuclear cooperation and reciprocal visits without claiming a 1991 agency already exists.',require=['Active Argentine-Brazilian industrial cooperation.'],icon='brazil')
node('plata_navigation','River Plate Navigation','diplomacy',-2,4,[('continental_cooperation','continental_balance')],desc='Offer Uruguay joint navigation safety, port coordination and inspection capacity.',icon='diplomacy')
node('bolivian_gas','Bolivian Gas Cooperation','diplomacy',2,4,[('continental_cooperation','continental_balance')],desc='Offer Bolivia funded gas transport and technical cooperation on mutually accepted terms.',icon='energy')
node('chile_beagle','The Beagle Mediation','diplomacy',6,4,[('continental_cooperation','continental_balance')],desc='Offer Chile a binding diplomatic and navigation settlement under accepted mediation.',event='beagle',icon='chile')
node('chile_passes','Open the Andean Passes','diplomacy',6,6,['chile_beagle'],desc='Offer Chile joint freight and mountain-route administration after the peace settlement is actually active.',require=['Active Beagle peace and navigation agreement.'],icon='chile')
node('soviet_grain','A Soviet Grain Protocol','diplomacy',-6,10,['sanmartin_desk'],desc='Offer a funded Soviet grain-purchasing protocol with transparent weekly transfers and agricultural cooperation.',event='grain_pressure',icon='soviet')
node('soviet_science','Soviet Academic Exchanges','diplomacy',-6,12,['soviet_grain'],desc='Offer reciprocal scholarships, technical translation and academic access to the Soviet Union.',require=['Active Argentine-Soviet grain protocol.'],icon='soviet')
node('us_training','A US Training Mission','diplomacy',-2,10,['sanmartin_desk'],desc='Offer the United States an accountable training and maintenance mission with explicit costs and political conditions.',icon='usa')
node('us_credit','US Industrial Credit','diplomacy',-2,12,['us_training'],desc='Offer a reciprocal industrial-credit framework rather than a free loan or guaranteed alliance.',require=['Active US-Argentine training agreement.'],icon='usa')
node('french_aviation','French Aviation Cooperation','diplomacy',2,10,['sanmartin_desk'],desc='Offer France an aviation training, testing and supplier agreement rooted in the Mirage procurement relationship.',icon='france')
node('spanish_industry','Spanish Industrial Links','diplomacy',6,10,['sanmartin_desk'],desc='Offer Spain industrial training and supplier partnerships without dictating its domestic political order.',icon='diplomacy')
node('nonaligned_medical','Cuban Public Health Exchange','diplomacy',2,14,['sanmartin_desk'],desc='Offer Cuba a reciprocal civilian medical-training exchange with funded teaching places.',icon='social')
node('peruvian_maintenance','A Peruvian Maintenance Accord','diplomacy',6,14,['sanmartin_desk'],desc='Offer Peru shared military maintenance courses and depot standards while retaining national command.',icon='army')
node('southatlantic_science','South Atlantic Research','diplomacy',0,18,['sanmartin_desk'],mm(res=.02,bur=.03),money=3,weekly=.0015,desc='Fund hydrography and Antarctic science using existing civilian institutions, without granting claims or a space-launch capability.',research=[('CAT_computing',.25,1)],icon='research')
node('regional_protocols','Regional Integration Protocols','diplomacy',0,20,['brazil_nuclear','chile_passes','plata_navigation'],mm(trade=.04,bur=.03),money=2,desc='Coordinate signed regional protocols while leaving a future customs union and its membership to a separate agreement.',require=['Active agreements with Brazil, Chile and Uruguay.'],icon='diplomacy')

group('falklands','The Malvinas and the South Atlantic',216,0)
node('sovereignty_dossier','A Sovereignty Dossier','falklands',0,0,money=1,desc='Prepare the legal, diplomatic and logistical record of the Malvinas claim while recognizing that the islands remain under British administration.',icon='argentina',days=21)
node('sovereignty_talks','Negotiations under Reservation','falklands',-4,2,['sovereignty_dossier'],mm(trade=.03,pp=-.03),money=1,desc='Pursue negotiations while preserving both states\' legal positions and accepting domestic criticism.',icon='diplomacy')
node('coercive_strategy','A Coercive South Atlantic Policy','falklands',4,2,['sovereignty_dossier'],mm(resist=.06,trade=-.04,milcost=.03),money=2,desc='Prepare a coercive policy with its diplomatic and logistical burden made explicit.',icon='navy')
ex('sovereignty_talks','coercive_strategy')
node('islands_links','Air and Postal Links','falklands',-4,4,['sovereignty_talks'],desc='Offer Britain regular air, mail and communications links under a sovereignty reservation.',icon='britain')
node('sovereignty_conference','A Sovereignty Conference','falklands',-4,6,['islands_links'],mm(bur=.02),money=1,desc='Prepare a substantive conference once the communications agreement is active.',require=['Active UK-Argentine communications agreement.'],event='islands_conference',icon='diplomacy')
node('leaseback_framework','A Leaseback Framework','falklands',-6,8,['sovereignty_conference'],desc='Offer a negotiated sovereignty framework with British administration and residents\' safeguards. Territorial settlement requires a separate explicit treaty response.',icon='britain')
node('joint_services','Joint Civilian Services','falklands',-2,8,['sovereignty_conference'],desc='Offer shared civil services and fisheries research while leaving sovereignty unresolved.',icon='britain')
ex('leaseback_framework','joint_services')
node('peaceful_patrols','Search and Rescue Patrols','falklands',-4,10,[('leaseback_framework','joint_services')],mm(navy=.03,milcost=.02),money=2,weekly=.001,desc='Fund national search-and-rescue readiness alongside the active civilian arrangement.',require=['Active UK leaseback-framework or joint-services agreement.'],icon='navy')
node('southern_logistics','Southern Logistics Review','falklands',4,4,['coercive_strategy'],mm(supply=-.03,milcost=.03),money=3,weekly=.001,desc='Fund the transport and maintenance preparations needed for a South Atlantic contingency.',buildings=[(457,'infrastructure',1)],icon='infra')
node('rosario_plan','Plan Operation Rosario','falklands',2,6,['southern_logistics'],money=2,desc='Prepare an island occupation plan and authorize a claim to the islands by force, weighing the risk of open war against British naval and air power.',
     require=['Britain owns and controls the Falkland Islands.','At peace with the United Kingdom.'],icon='navy',
     wargoal=dict(type='take_state_focus',target='ENG',states=[26],expire=730,reference='common/wargoals/00_invasion.txt:15-29; common/national_focus/01_EU_USoE_shared.txt:1051-1057'))
node('armed_demonstration','An Armed Demonstration','falklands',6,6,['southern_logistics'],mm(navy=.04,trade=-.03,milcost=.04),money=2,weekly=.001,desc='Use a funded naval demonstration and another diplomatic offer rather than an automatic invasion.',event='naval_demonstration',icon='navy')
ex('rosario_plan','armed_demonstration')
node('war_cabinet','A South Atlantic War Cabinet','falklands',2,8,['rosario_plan'],money=2,desc='Mobilize the state for the real war, accepting the operational and fiscal liabilities of expeditionary combat.',require=['At war with the United Kingdom over the islands.'],decision='war_mobilization',icon='army')
node('islands_supply','Sustain the Island Garrison','falklands',0,10,['war_cabinet'],mm(supply=-.05,milcost=.07),money=3,weekly=.003,desc='Prioritize costly resupply and damage repair for forces already fighting on the islands.',require=['At war with the United Kingdom.','Argentina controls the Falkland Islands state.'],temporary='war',icon='navy')
node('mainland_cover','Preserve the Mainland Reserve','falklands',4,10,['war_cabinet'],mm(defense=.08,navy=-.03,milcost=.03),money=2,weekly=.001,desc='Retain mainland air and ground reserves instead of committing every available asset to the islands.',require=['At war with the United Kingdom.'],temporary='war',icon='army')
ex('islands_supply','mainland_cover')
node('wartime_assessment','The Campaign Assessment','falklands',2,12,[('islands_supply','mainland_cover')],money=1,desc='Assess the actual campaign and the feasibility of a negotiated end. Outcomes follow the real war and peace settlement.',event='war_outcome',require=['A South Atlantic campaign actually occurred.'],icon='army')
node('veterans_programme','A Veterans\' Settlement','falklands',0,16,mods=mm(st=.03,health=.04,soc=.03),money=3,weekly=.002,desc='Fund physical and psychological care, pensions and the identification of the missing after the real war.',require=['The South Atlantic war has ended.','A South Atlantic campaign actually occurred.'],remove=['war_defeat'],icon='social')
node('campaign_inquiry','A Public Campaign Inquiry','falklands',-4,18,['veterans_programme'],mm(st=.04,bur=.03,org=-.02),money=1,desc='Publish the operational record and examine the conduct of senior commanders.',require=['Civilian constitutional government.'],event='campaign_inquiry')
node('service_rehabilitation','Professional Rehabilitation','falklands',4,18,['veterans_programme'],mm(org=.04,navy=.03,milcost=.04),money=3,weekly=.001,desc='Prioritize training, maintenance and professional recovery while leaving the campaign record to ordinary institutions.',icon='army')
ex('campaign_inquiry','service_rehabilitation')
node('madrid_contacts','Madrid Confidence Measures','falklands',0,20,[('campaign_inquiry','service_rehabilitation')],desc='Offer Britain the restoration of consular links and maritime confidence measures after peace.',icon='britain')
node('madrid_normalization','Restore Diplomatic Relations','falklands',0,22,['madrid_contacts'],desc='Offer full diplomatic restoration without requiring either side to surrender its sovereignty position.',require=['Active Madrid consular and confidence agreement.'],icon='britain')
node('atlantic_reconstruction','South Atlantic Reconstruction','falklands',0,24,['madrid_normalization'],mm(infra=.04,st=.02,soc=.02),money=4,weekly=.001,desc='Reinvest in southern civilian transport and services after diplomatic restoration.',require=['Active UK-Argentine diplomatic normalization spirit.'],buildings=[(457,'infrastructure',1)],icon='infra')

# Every bilateral proposal has one originating national focus and explicit recipient decisions.
def deal(key,title,focus,partner,description,own,other,setup,other_setup,weekly=0,other_weekly=0,credit=0,other_credit=0,buildings=(),research=(),parent=None,source='',requirements=()):
    n=next(n for n in D['nodes'] if n['key']==focus)
    n['agreement']=key
    a=dict(id=key,title=title,focus=n['id'],partner=partner,description=description,decision='Consider '+title,
           argentina=dict(spirit=title+': Argentina',modifiers=mm(**own),setup=setup,weekly=weekly,credit=credit),
           recipient=dict(spirit=title+': '+partner,modifiers=mm(**other),setup=other_setup,weekly=other_weekly,credit=other_credit),
           buildings=[dict(country=c,state=s,type=t,levels=l,slots=l) for c,s,t,l in buildings],
           research=[dict(country=c,category=t,bonus=b,uses=u) for c,t,b,u in research],parent=parent,source=source,
           requirements=list(requirements),conditions=['Both countries exist and are at peace with one another.','Neither country embargoes the other.','No diplomatic, financial, economic or military Imperia sanctions in either direction.'],
           pending_days=90,reoffer_days=180,lifetime='Standing, no expiry. Both national spirits and weekly flows suspend and restore together.',
           implementation='Recipient controls Accept or Decline. Execute only after consent and one-time contract guard. Parent agreement must actually be active. Show the complete display-only native If they accept effects even while locked, pending or suspended. Restoration never repeats setup, assets or research.')
    if parent:a['conditions'].append('The actual active parent agreement is '+parent+'.')
    D['agreements'].append(a)
    return a

deal('brazil_industry','Argentine-Brazilian Industrial Cooperation','brazil_trade','BRA','Industrial standards and supplier exchanges support the late Cold War rapprochement.',
 {'cprod':.04,'bur':.02},{'cprod':.03,'bur':.02},3,3,.001,.001,research=[('ARG','CAT_industry',.30,1),('BRA','CAT_industry',.25,1)],source='1985-1986 rapprochement and integration protocols; accelerated cooperation is alternate history.')
deal('brazil_atom','Argentine-Brazilian Nuclear Cooperation','brazil_nuclear','BRA','Reciprocal civilian research and facility visits build confidence without inventing early ABACC membership.',
 {'res':.025,'reactor':.05,'bur':.02},{'res':.025,'reactor':.05,'bur':.02},3,3,.0015,.0015,parent='brazil_industry',research=[('ARG','CAT_nuclear_reactors',.35,1),('BRA','CAT_nuclear_reactors',.35,1)],source='Civilian nuclear agreement of 17 May 1980; 1990 Foz declaration. ABACC itself remains outside the 1990 horizon.')
deal('uruguay_navigation','River Plate Navigation Protocol','plata_navigation','URG','Joint navigation administration and freight coordination improve an existing river economy.',
 {'trade':.04,'supply':-.02,'bur':.02},{'trade':.04,'cprod':.03,'bur':.02},2,1,.001,.0005,buildings=[('ARG',453,'infrastructure',1),('URG',893,'infrastructure',1)],source='1973 Treaty of the River Plate and its Maritime Front. Uruguay recipient state 893 is Rio de la Plata in the current target map.')
deal('bolivia_gas','Argentine-Bolivian Gas Cooperation','bolivian_gas','BOL','A funded transport and payment framework supports gas trade without creating automatic resource output.',
 {'cprod':.03,'bur':.02},{'tax':.03,'bur':.02},3,2,.001,.0005,credit=0,other_credit=.002,source='Gas exports to Argentina began in 1972; financing and exact game terms are design proposals.')
deal('beagle_peace','Beagle Peace and Navigation','chile_beagle','CHL','Accept a mediated peace and safe navigation regime with a visible nationalist political cost.',
 {'trade':.05,'milcost':-.03,'pp':-.03},{'trade':.05,'milcost':-.03,'pp':-.02},2,2,.0005,.0005,source='Papal mediation after 1978 near-war; 1984 Treaty of Peace and Friendship. No map transfer is hidden in these rewards.')
deal('andean_passes','Andean Freight Cooperation','chile_passes','CHL','Joint route administration supports cross-border freight after the peace settlement.',
 {'trade':.03,'supply':-.02,'bur':.02},{'trade':.03,'supply':-.02,'bur':.02},3,3,.001,.001,parent='beagle_peace',buildings=[('ARG',450,'infrastructure',1),('CHL',468,'infrastructure',1)],source='Commercial continuation inferred from bilateral peace; exact infrastructure grants are proposed balance values.')
deal('soviet_grain','Argentine-Soviet Grain Purchasing','soviet_grain','SOV','The buyer funds weekly purchases while the exporter invests in reliable agricultural supply.',
 {'ag':.04,'bur':.02},{'soc':-.025,'bur':.01},2,2,.001,.007,credit=.006,source='Argentine grain sales during the 1980 US embargo. Grain revenue uses an explicit weekly transfer, not the mineral-export revenue modifier.')
deal('soviet_academic','Argentine-Soviet Academic Exchange','soviet_science','SOV','Fund reciprocal teaching places and technical exchange without committing to a military bloc.',
 {'res':.025,'edu':.03,'resist':-.03},{'res':.01,'edu':.015},2,2,.001,.001,parent='soviet_grain',research=[('ARG','CAT_industry',.30,1),('SOV','CAT_industry',.15,1)],source='Technical cooperation inferred from the commercial relationship; both governments retain consent.')
deal('us_training','US-Argentine Training Mission','us_training','USA','Fund training, maintenance courses and accountable command arrangements.',
 {'org':.04,'pers':.03,'resist':-.04},{'navy':.015,'milcost':.015},2,2,.0015,.001,source='US military training relationship; restrictions and the 1982 US tilt to Britain show that it is not an alliance guarantee.')
deal('us_credit','US-Argentine Industrial Credit','us_credit','USA','Create a funded commercial-credit framework with explicit political and fiscal exposure.',
 {'civ':.06,'int':-.25,'resist':-.04},{'corp':.02,'bur':.01},3,3,.001,.001,parent='us_training',research=[('ARG','CAT_industry',.30,1)],source='Historical US investment/credit relationship. No debt principal is silently forgiven and no automatic loan is created.')
deal('french_aviation','Franco-Argentine Aviation Cooperation','french_aviation','FRA','Joint training and supplier testing improve readiness while retaining the supplier relationship.',
 {'air':.04,'milcost':.025,'resist':-.03},{'out':.015,'bur':.01},3,2,.0015,.0005,research=[('ARG','CAT_aircraft',.35,1),('FRA','CAT_aircraft',.20,1)],source='Mirage procurement relationship beginning in 1970; later Super Etendard and supply restrictions are separate historical developments.')
deal('spain_industry','Argentine-Spanish Industrial Exchange','spanish_industry','SPR','Fund industrial instruction and commercial supplier links across the Atlantic.',
 {'cprod':.03,'edu':.02},{'cprod':.02,'edu':.02},2,2,.001,.001,research=[('ARG','CAT_industry',.25,1),('SPR','CAT_industry',.20,1)],source='Bilateral commercial and cultural relationship, with exact programme as plausible alternate-history proposal.')
deal('cuba_health','Argentine-Cuban Medical Exchange','nonaligned_medical','CUB','Provide reciprocal public-health training and funded teaching places without reducing workforce size.',
 {'res':.015,'health':-.02,'edu':.02},{'res':.015,'edu':.03},2,2,.001,.001,source='1973 diplomatic and trade opening to Cuba. Medical exchange is a proposed civilian continuation, not an automatic export of personnel.')
deal('peru_depots','Argentine-Peruvian Maintenance Cooperation','peruvian_maintenance','PRU','Share depot practice, maintenance instruction and tested component standards.',
 {'gain':.03,'milcost':.02},{'gain':.03,'milcost':.02},2,2,.001,.001,research=[('ARG','CAT_industry',.20,1),('PRU','CAT_industry',.20,1)],source='Military links and later Peruvian support; peacetime maintenance protocol is an alternate-history design inference.')
deal('uk_links','UK-Argentine Communications','islands_links','ENG','Regular air, postal and telephone links improve civilian access under a sovereignty reservation.',
 {'trade':.04,'bur':.02},{'trade':.025,'bur':.015},2,1,.001,.0005,source='1971 communications agreement and sovereignty umbrella.',requirements=['The islands are British-owned and controlled at signature.'])
deal('uk_leaseback','Malvinas Leaseback Negotiating Framework','leaseback_framework','ENG','Create a negotiation mandate and residents\' safeguards. This contract itself transfers no territory or ownership.',
 {'trade':.05,'pp':-.04,'bur':.02},{'trade':.03,'pp':-.03,'bur':.02},2,2,.001,.001,parent='uk_links',source='Leaseback proposals considered in the late 1970s and 1980. The successful framework is alternate history.',requirements=['UK-Argentine communications active.','No transfer occurs without a separate explicit treaty accepted by the territorial owner.'])
deal('uk_services','Malvinas Joint Civilian Services','joint_services','ENG','Fund shared transport, scientific and fisheries services while preserving both sovereignty positions.',
 {'trade':.04,'res':.015,'bur':.02},{'trade':.03,'res':.015,'bur':.02},3,2,.001,.001,parent='uk_links',source='1971 communications precedent; expanded civilian services are an alternate-history offer.')
deal('madrid_consular','Madrid Consular and Maritime Measures','madrid_contacts','ENG','Restore consular contacts and reduce maritime misunderstanding after a real peace.',
 {'trade':.03,'bur':.02},{'trade':.02,'bur':.01},1,1,.0005,.0005,source='Madrid declaration of 1989.',requirements=['The South Atlantic war is over.'])
deal('madrid_diplomatic','UK-Argentine Diplomatic Normalization','madrid_normalization','ENG','Restore full diplomatic relations under an explicit sovereignty reservation.',
 {'trade':.04,'int':-.25,'pp':-.02},{'trade':.025,'bur':.01},2,1,.0005,.0005,parent='madrid_consular',source='Madrid II declaration of 1990.',requirements=['Active Madrid consular and maritime measures.'])

def option(name,mods=None,money=0,weekly=0,duration=None,**kw):
    return dict(name=name,modifiers=mm(**(mods or {})),money=money,weekly=weekly,duration=duration,**kw)
def event(key,title,description,trigger,options):
    D['events'].append(dict(key=key,id=P+key,title=title,description=description,trigger=trigger,options=options))
event('commanders','The Commanders and the President','The service chiefs demand a decision on the political future of the revolution.',
 'Actual command crisis with Ongania still incumbent; historical date 9 June 1970. The introductory focus previews this event but does not prematurely execute the historical succession.',[
 option('Back the presidential project',{'pp':.08,'st':-.05,'police':.04},1,duration=365,require='Ongania is incumbent.',leader='Retain Juan Carlos Ongania'),
 option('Appoint a nationalist-developmental cabinet',{'cprod':.03,'int':.25},2,duration=365,leader='Roberto Marcelo Levingston becomes national leader'),
 option('Authorize a negotiated opening',{'st':.04,'pp':-.03},1,duration=365,leader='Alejandro Agustin Lanusse becomes national leader',require='Army command supports a negotiated opening; an earlier-than-1971 appointment is alternate history.'),
])
event('opening','Terms of an Electoral Opening','Civilian parties seek a published timetable and guarantees that the result will be respected.',
 'Previewed by electoral-opening focuses. Each focus has its own once-only policy receipt; the actual election uses the existing election system.',[
 option('Guarantee unrestricted competition',{'st':.04,'pp':-.04},1,duration=365,decision='constitutional_election'),
 option('Negotiate service guarantees first',{'org':.03,'st':-.03,'milcost':.03},1,duration=365,decision='constitutional_election'),
])
event('popular_hour','The Hour of the People','The mass parties can agree on constitutional competition without agreeing on a government programme.',
 'Interparty initiative after a genuine electoral opening; historical precedent 11 November 1970.',[
 option('Guarantee opposition rights',{'st':.05,'pp':-.04},1,duration=365),
 option('A narrower governing accord',{'pp':.07,'st':-.02,'bur':.02},1,duration=365),
])
event('peronism','Who Speaks for the Movement?','Union leaders, provincial organizers and the youth demand a place in the governing movement.',
 'First PJ Social Pact. No choice installs Peron without an actual leadership transition.',[
 option('Give unions a larger delegation',{'out':.03,'soc':.03},1,duration=365),
 option('Balance provinces and the youth',{'st':.04,'pp':-.03,'bur':.02},1,duration=365),
])
event('labor','The Labor Settlement','An enforceable settlement must reconcile wages, production and the freedom to organize.',
 'National Labor Congress, once; prior Cordobazo spirit is removed by the focus.',[
 option('Independent collective bargaining',{'st':.05,'cap':-.02,'soc':.03},1,duration=730,remove_spirit=P+'wage_freeze'),
 option('Reimpose administrative restraint',money=1,add_spirit=P+'wage_freeze',require='Authoritarian labor policy.'),
])
event('accountability','The Record of Repression','Victims and institutions demand an account of unlawful detention, disappearance and political violence.',
 'Documented repression and actual civilian government. A single shared receipt prevents successive national/UCR focuses from replaying the same inquiry.',[
 option('An independent public inquiry',{'st':.05,'bur':.03},1,duration=730,add_spirit=P+'transition_resistance'),
 option('A limited judicial settlement',{'st':.03,'pp':-.04},1,duration=730),
])
event('stabilization','A Stabilization Programme','The government must decide how to share the burden of restoring predictable finance.',
 'Once per approved national stabilization programme. Existing MD inflation, debt and borrowing remain authoritative.',[
 option('Fund a negotiated incomes accord',{'int':-.25,'corp':-.03,'bur':.02},2,duration=730),
 option('Prioritize fiscal restraint',{'int':-.5,'build':-.03,'st':-.03},1,duration=730),
])
event('privatization','The Terms of Restructuring','Buyers seek commercial freedom while workers and provinces seek service and employment guarantees.',
 'Menem actually incumbent, post-renewal market reform. This event authorizes policy only. The later approved asset-sale decision is the single source of sale proceeds.',[
 option('Retain public service obligations',{'cprod':.02,'bur':.03},money=1,duration=730),
 option('Authorize a rapid sale timetable',{'tax':-.02,'st':-.03},money=1,duration=730),
])
event('liberalization','The Adjustment Debate','Manufacturers and labor organizations demand protection from the pace of liberalization.',
 'Rapid Liberalization, once.',[
 option('Fund temporary retraining',{'res':.015,'edu':.04,'st':.02},2,duration=365),
 option('Keep the adjustment timetable',{'cprod':.03,'st':-.04,'soc':-.02},1,duration=365),
])
event('ownership','Disputed Enterprise Transfers','The government has acquired strategic firms, but managers and creditors dispute the terms.',
 'Immediate Expropriation, once.',[
 option('Negotiate compensation bonds',{'int':.5,'trade':.03},3,duration=730),
 option('Retain immediate state control',{'cprod':.03,'trade':-.04,'bur':.03},1,duration=730),
])
event('beagle','A Cabinet for Mediation','Diplomacy can avoid a southern war, but the domestic politics of compromise remain difficult.',
 'Beagle Mediation focus. Chile still receives its own independent acceptance/refusal decisions.',[
 option('Fund a technical mediation team',{'bur':.02,'trade':.03},1,duration=365),
 option('Publish a firm national reservation',{'pp':.05,'trade':-.02},1,duration=365),
])
event('grain_pressure','Grain and the Superpowers','A commercial opening to the Soviet Union may bring pressure from Washington.',
 'Historical-type external embargo crisis while a Soviet grain offer or agreement exists. Not an automatic January 1970 event.',[
 option('Defend commercial independence',{'resist':.05,'trade':-.03},1,duration=365),
 option('Offer parallel Western consultations',{'trade':.04,'pp':-.03,'bur':.02},1,duration=365),
])
event('islands_conference','Terms for the Island Conference','Both states require a credible agenda and safeguards for residents before discussing a settlement.',
 'Sovereignty Conference, active communications agreement.',[
 option('Prioritize a leaseback mandate',{'trade':.03,'pp':-.03},1,duration=365),
 option('Prioritize civilian cooperation',{'res':.01,'bur':.02},1,duration=365),
])
event('naval_demonstration','The Limits of a Demonstration','The fleet can signal resolve, but a prolonged deployment has real operational costs.',
 'Armed Demonstration, while no war exists with Britain.',[
 option('End the demonstration on schedule',{'trade':.02,'pp':-.03},1,duration=180),
 option('Maintain the naval presence',{'navy':.03,'milcost':.06,'trade':-.03},2,weekly=.002,duration=180),
])
event('war_outcome','The South Atlantic Campaign','The military and diplomatic balance must be judged from the campaign that actually occurred.',
 'Campaign Assessment. Outcome options check real war status, island control and a recorded negotiated peace. No focus script can award a fictional victory.',[
 option('Continue the funded campaign',{'org':.03,'milcost':.08,'supply':.04},2,weekly=.002,duration=180,require='War continues.'),
 option('Record the negotiated settlement',{'st':.03,'bur':.02},1,duration=365,require='War ended and the actual settlement is recorded.'),
 option('Recognize the military defeat',money=1,add_spirit=P+'war_defeat',require='War ended after Argentina lost island control and the campaign defeat is recorded.'),
])
event('campaign_inquiry','The Campaign Record','Families, veterans and service personnel seek a public account of decisions made during the war.',
 'Public Campaign Inquiry after the war, once.',[
 option('Publish the full operational record',{'st':.04,'bur':.02},1,duration=365,add_spirit=P+'transition_resistance'),
 option('Publish a professional service report',{'org':.03,'pp':-.03},1,duration=365),
])

def decision(key,title,requirements,money=0,weekly=0,mods=None,**kw):
    D['decisions'].append(dict(key=key,title=title,requirements=requirements,money=money,weekly=weekly,modifiers=mm(**(mods or {})),**kw))
decision('constitutional_election','Hold the Constitutional Election',['Political organization legalized.','Published electoral timetable.','Actual election framework ready.'],1,
         actions=['Conduct one real election through the existing MD/Imperia political framework.','Enable constitutional succession.','Remove A Revolution without Consent only after the elected government takes office.'],replay='One receipt per actual election; no focus-only party installation.')
decision('civilian_handover','Transfer Authority to the Elected Government',['A real constitutional election has completed.','A lawful winner is recorded.'],1,
         actions=['Install the actual elected winner through the existing leader framework.','Remove A Revolution without Consent.'],replay='One actual handover; no forced beneficiary or invented leader flag.')
decision('asset_sales','Execute the Approved Asset Sale',['Menem is actually incumbent.','Approved public asset sale not previously executed.'],money=-3,mods={'tax':-.025,'st':-.02},
         actions=['Add one national Asset Sale Settlement spirit with the listed modifiers.'],replay='One permanent sale receipt. The spirit and treasury proceeds do not replay on re-election.')
decision('debt_restructuring','Restructure the External Debt',['A Foreign-Currency Debt Crisis is active.','MD debt ratio remains above 75%.'],3,mods={'int':.5,'build':-.03},
         remove=[P+'debt_crisis'],duration=730,actions=['Add Restructuring under Creditor Review for 730 days.','Remove A Foreign-Currency Debt Crisis.'],replay='Once per recorded crisis. No debt principal is silently removed.')
decision('crisis_adjustment','Fund a Debt Adjustment Programme',['A Foreign-Currency Debt Crisis is active.'],3,remove=[P+'debt_crisis'],add_spirit=P+'adjustment',duration=730,
         actions=['Remove A Foreign-Currency Debt Crisis.','Add Austerity and Adjustment for 730 days.'],replay='Once per recorded crisis; no automatic debt repayment.')
decision('uranium_survey','Complete the Los Gigantes Survey',['Survey focus completed.','Argentina owns and controls Cordoba.','No survey receipt already exists.'],
         actions=['Register one surveyed Los Gigantes deposit through the existing Imperia deposit system.','Uranium production remains 0.','No uranium mine is built.'],replay='Survey is already financed by its $2.000 billion focus; no second survey fee.',state=450)
decision('uranium_mine','Construct the Surveyed Uranium Mine',['Los Gigantes survey completed.','Correct deposit modifier and mine-per-level data exist.','Argentina owns and controls Cordoba.','Native mine capacity and shared capacity checks pass.'],
         actions=['Cordoba: +1 shared building slot, then +1 uranium mine using the existing mine system.','Production follows the native mine calculation, never a raw state-history grant.'],
         buildings=[dict(country='ARG',state=450,type='uranium_mine',levels=1,slots=1)],replay='The $4.000 billion development focus funds the project. One construction receipt prevents a second mine grant; no second setup fee.')
decision('war_mobilization','Fund South Atlantic Mobilization',['Actual war with Britain.','Mobilization has not already been funded for this campaign.'],2,weekly=.004,add_spirit=P+'war_mobilization',
         actions=['Add South Atlantic Mobilization while the war lasts.','Additional expenses: +$0.00400 billion weekly.'],replay='One setup payment per actual campaign. Remove spirit and weekly burden at peace.')

COUNTRIES=dict(ARG='Argentina',BRA='Brazil',CHL='Chile',URG='Uruguay',BOL='Bolivia',SOV='Soviet Union',USA='United States',FRA='France',SPR='Spain',CUB='Cuba',PRU='Peru',ENG='United Kingdom')
STATES={26:'Falkland Islands',893:'Rio de la Plata',448:'Mesopotamia',449:'Gran Chaco',450:'Cordoba',453:'Pampas and Buenos Aires',454:'Patagonia',457:'Tierra del Fuego',468:'Central Chile'}
D['countries']=COUNTRIES; D['states']=STATES
D['integration']=dict(
 sync='Proposed: preserve earned values per exact party and leader. Refresh on government/leader changes, weekly tick and load. Only the current owner contributes its programme spirit and weekly costs; earned buildings, cash, XP, research and ratified contracts never replay.',
 policy='National economic/institutional choices remain earned across governments. A government change is not a free policy reset. Programme-level exclusions remain saved and visible.',
 agreements='One Argentine focus per offer; recipient Accept/Decline decisions. Both parties receive complete prospective native effects in locked focus tooltips. A signed contract has no expiry. Active state and weekly transfers suspend and restore in both countries on war, embargo, any mirrored sanction or inactive required parent. No setup, buildings or research repeat.',
 finance='Billion-dollar MD units. Weekly income/expense aggregates require explicit consumer integration in 00_money_system.txt. Modifier percentages and fixed weekly expenses are separate cumulative burdens. Interest changes are percentage points before native clamps.',
 buildings='For every building level, first add one shared state slot in the same transaction. Check owner, controller, correct province for province buildings, native building level limit and actual capacity separately. No construction on proposal or preview.',
 unresolved=['PSD incumbent identity and exclusive slot-18 routing require approval and integration.','UCeDe is a post-1982 successor identity within the PCI political tradition; exact identity must be approved, without replacing PD Mendoza.','Native Argentina leader/succession mapping is inconsistent with registry identities: historical pools include slots 2,20,22, while UCR is registry slot3 and PJ slot13. Route all real transitions through reconciled identity checks.','Ongania start expiry is 18 June 1970, while historical removal was 9 June. The concept proposes a real conditional June crisis, not an automatic silent history edit.','Loaded 1970 states already contain nuclear reactors in Cordoba and Pampas despite historical commissioning dates. This concept gives training/construction capability and no free Atucha reactor; baseline correction is a separate review.','Non-BBA aircraft category fallback must be verified against the loaded Cold War aircraft technology branch.','All Argentina-specific contract and programme providers remain proposed. No runtime game or multiplayer test has been performed.'])

# Corrections discovered during reference review, applied to design data before emission.
# A final territorial offer is a distinct Argentine focus with British consent and compensation.
node('sovereignty_treaty','A Sovereignty Treaty','falklands',-6,10,['leaseback_framework'],
     desc='Offer Britain a negotiated transfer of sovereignty with compensation and continuing civilian access guarantees. This is an explicit alternate-history settlement.',
     require=['Active UK leaseback negotiating framework.','Britain still owns and controls the Falkland Islands.'],icon='britain')
node('fisheries_science','Joint Fisheries Research','falklands',-2,10,['joint_services'],mm(res=.015,bur=.02),money=2,weekly=.001,
     desc='Fund fisheries and hydrographic research under the active shared civilian-services agreement.',require=['Active Malvinas joint civilian-services agreement.'],icon='research')
patrol=next(n for n in D['nodes'] if n['key']=='peaceful_patrols')
patrol['y']=12;patrol['dy']=12;patrol['prerequisites']=[[P+'sovereignty_treaty',P+'fisheries_science']]
patrol['requirements']=['Active UK-Argentine sovereignty treaty or joint civilian-services agreement.']
settlement=deal('uk_sovereignty','Malvinas Sovereignty and Civilian Access','sovereignty_treaty','ENG',
     'A separately accepted territorial settlement transfers sovereignty to Argentina and compensates Britain while preserving agreed civilian access. No core is granted.',
     {'trade':.04,'st':.03,'bur':.025},{'trade':.03,'pp':-.04,'bur':.015},6,1,.0015,.0005,parent='uk_leaseback',
     source='Alternate-history negotiated outcome inspired by the late-1970s/1980 leaseback discussions; this accepted cession did not occur historically.',
     requirements=['Britain owns and controls state 26 at signature.','Both governments explicitly approve the territorial settlement.','No ongoing war or occupation of the islands.'])
settlement['recipient']['grant']=5
settlement['territory']=dict(state=26,from_country='ENG',to_country='ARG',core=False,code='ARG = { transfer_state = 26 }')
settlement['implementation']+=' The Argentine $6.000 billion charge includes $5.000 billion compensation credited once to Britain plus $1.000 billion setup. Britain pays its own $1.000 billion setup. Transfer and all payments share the same consent/ownership/one-time guard; suspension does not reverse territory or repeat compensation.'

# The deposit is ALREADY surveyed at the scenario start. Feasibility adds research, never a duplicate deposit.
feasibility=next(n for n in D['nodes'] if n['key']=='uranium_survey')
feasibility.update(title='The Los Gigantes Reserve',description='Review the already surveyed Los Gigantes reserve, mine safety and fuel-testing requirements. The existing native paid investment remains available independently.',
                   modifiers=mm(res=.01,edu=.02),decision=None,research=[dict(category='CAT_nuclear_reactors',bonus=.20,uses=1)])
mine=next(n for n in D['nodes'] if n['key']=='uranium_development')
mine['title']='Fund the Uranium Mine'
mine['description']='Sponsor one mine from the national development budget if the registered deposit still has unused capacity. An earlier native investment cannot earn a second grant.'
mine['requirements']=['Existing Los Gigantes surveyed deposit.','No uranium mine is already built or under construction in Cordoba.','Argentina owns and controls Cordoba.','Native mine capacity and building capacity pass before funding.']
D['decisions']=[d for d in D['decisions'] if d['key']!='uranium_survey']
mine_decision=next(d for d in D['decisions'] if d['key']=='uranium_mine')
mine_decision['requirements']=['The already registered Los Gigantes deposit exists.','Correct deposit modifier and mine-per-level data exist.','No mine is built or under construction in Cordoba.','Argentina owns and controls Cordoba.','Native mine and shared capacity checks pass.']
mine_decision['replay']='The $4.000 billion focus funds exactly one sponsored mine. An existing native mine or prior sponsored construction bypasses this focus with no payment or reward. The native paid-investment route is never gated behind this focus; both routes check the same remaining capacity and construction receipt.'
D['integration']['unresolved']=[s for s in D['integration']['unresolved'] if not s.startswith('Non-BBA')]
D['integration']['uranium']='The 1970 startup already registers Los Gigantes in state450: one mine slot, three uranium per level. Raw production and built mines start at zero. Feasibility adds no deposit and never gates native investment; the sponsored mine checks existing construction and capacity before its payment. No automatic raw state-history production.'
for s in D['conditional_spirits']:
    s['duration']=365 if s['id']==P+'transition_resistance' else 730 if s['id']==P+'adjustment' else None
for e in D['events']:
    if e['key']=='privatization':e['title']='The Privatization Mandate'
    e['ownership']='party' if e['key'] in ['peronism','privatization','liberalization','ownership'] else 'national'
    e['party']={'peronism':13,'privatization':13,'liberalization':16,'ownership':4}.get(e['key'])
    e['leader']='Carlos Menem' if e['key']=='privatization' else None
    for o in e['options']:
        if o.get('add_spirit')==P+'transition_resistance':o['add_spirit_duration']=365
e=next(e for e in D['events'] if e['key']=='accountability')
e['trigger']+=' Option modifiers last 730 days; the separate Barracks Resistance spirit lasts 365 days.'
for n in D['nodes']:
    n['leader_names']={'Juan Carlos Ongania':['Juan Carlos Ongania','Juan Carlos Ongánía'],
                       'Juan Domingo Peron':['Juan Perón'], 'Raul Alfonsin':['Raúl Alfonsín'],'Carlos Menem':['Carlos Menem']}.get(n['leader'],[])
    if n['key']=='balbin_compromise':n['title']='A Civic Compromise'
    if n['key']=='rosario_plan':n['description']+=' The historical operation occurred in April 1982; an earlier launch is a deliberate major alternate-history escalation.'
    if n['key']=='madrid_contacts':n['requirements']+=['A South Atlantic war with Britain actually occurred and has ended.']
    if n['key']=='atucha_training':n['description']='Train future operators, inspectors and maintenance engineers for civilian reactors, including the Atucha project. Training can precede commissioning; no completed reactor or early commercial operation is granted.'
    if n['party']==5:n['requirements']+=['The revolutionary Peronist movement has actually organized and reached government through a real political settlement.']
for a in D['agreements']:
    a['historical_mode']='Historical precedent; signing earlier than its precedent is a negotiated alternate-history acceleration, with no arbitrary date lock.'
    if a['id']=='soviet_grain':a['source']+=' The historical 1980 arrangement covered 1980-1984. This RP offer deliberately negotiates a new standing, renewable-by-continuation protocol with no spirit expiry, rather than claiming those were the historical legal terms.'
    if a['id'] in ['madrid_consular','madrid_diplomatic']:a['requirements']+=['A recorded South Atlantic war and its subsequent peace.']
    if a['id'] in ['us_training','us_credit','french_aviation']:
        a['source']+=' Historical supplier restrictions are roleplay choices through the existing native embargo and Imperia military-sanction system; a contract is not a guaranteed alliance or unconditional wartime supply promise.'
    if a['id']=='beagle_peace':a['description']+=' An earlier agreement represents accelerated preventive mediation, not a claim that the 1978 crisis or 1984 treaty already occurred in January 1970.'
for n in D['nodes']:
    if n['key']=='chile_beagle':n['description']+=' Before the historical crisis, this is an alternate preventive mediation initiative.'
    if n['key'] in ['corporate_charter','functional_councils','state_appointments']:
        n['active_requirements']=['The corporate constitutional settlement remains in force.']
D['integration']['constitutional']='The corporate-charter modifiers operate only while that constitutional settlement remains in force. Actual constitutional restoration removes A Revolution without Consent and deactivates the corporate institutional programme, even if a different party conducts the transition. Earned technical skills and one-time assets retain their separate ownership.'
# Keep normal focus prose political. Technical guarantees belong to the review record.
PLAYER_DESCRIPTIONS={
 'army_directives':'Commission a joint political and readiness review under the military government.',
 'peron_arbitration':'Concentrate dispute resolution in Peron\'s personal authority, balancing the movement\'s competing institutions.',
 'socialist_coalition':'Form a constitutional governing coalition around the Democratic Socialist tradition and independent civic organizations.',
 'prt_literacy':'Expand technical education for industrial workers and connect vocational training to public enterprise.',
 'statistical_office':'Publish consistent budget, debt and national-account statistics to restore public and creditor confidence.',
 'gas_network':'Improve gas distribution and the reliability of industrial energy supply.',
 'uranium_survey':'Review the surveyed Los Gigantes reserve, mine safety and the technical requirements of the civilian fuel programme.',
 'uranium_development':'Sponsor a mine at the surveyed Los Gigantes reserve under funded safety, engineering and environmental standards.',
 'civil_safeguards':'Commit civilian nuclear development to transparent accounting, inspection and peaceful use.',
 'southatlantic_science':'Fund hydrography and Antarctic science through civilian institutions and professional research teams.',
 'brazil_nuclear':'Offer Brazil civilian nuclear cooperation, technical exchange and reciprocal facility visits.',
 'us_credit':'Offer a reciprocal industrial-credit framework with clear commercial obligations and political conditions.',
 'soviet_grain':'Offer the Soviet Union a funded grain-purchasing protocol with reliable supply commitments and agricultural cooperation.',
 'regional_protocols':'Coordinate signed regional protocols and build a political foundation for deeper economic integration.',
 'rosario_plan':'Prepare an island occupation plan and authorize a claim to the islands by force, weighing the risk of open war against British naval and air power.',
 'war_cabinet':'Mobilize the state for the South Atlantic war and accept the operational and fiscal burden of expeditionary combat.',
 'wartime_assessment':'Assess the campaign and the feasibility of a negotiated end within the military and diplomatic balance.',
 'sovereignty_treaty':'Offer Britain a negotiated transfer of sovereignty with compensation, residents\' safeguards and continuing civilian access guarantees.',
 'madrid_contacts':'Offer Britain the restoration of consular links and maritime confidence measures after the South Atlantic war.',
}
for n in D['nodes']:
    n['description']=PLAYER_DESCRIPTIONS.get(n['key'],n['description'])
    if n['key'] in ['menem_reform','alfonsin_mandate']:n['requirements']=[]
    if n['key']=='uranium_development':n['requirements']=['Surveyed Los Gigantes deposit.','No uranium mine is built or under construction in Cordoba.','Argentina owns and controls Cordoba.','The deposit and the state have capacity for one mine.']
    n['requirements']=[r.replace('A South Atlantic war with Britain actually occurred and has ended.','A South Atlantic war with Britain has ended.').replace('A South Atlantic campaign actually occurred.','A South Atlantic campaign has taken place.').replace('A real post-Peron leadership transition has occurred.','The movement has completed its post-Peron leadership transition.') for r in n['requirements']]
for a in D['agreements']:
    a['conditions']=[c for c in a['conditions'] if not c.startswith('The actual active parent agreement')]
    if a['parent']:
        parent=next(b for b in D['agreements'] if b['id']==a['parent'])
        a['conditions'].append('Active agreement: '+parent['title']+'.')
    a['requirements']=[r.replace('Britain owns and controls state 26 at signature.','Britain owns and controls the Falkland Islands.').replace('A recorded South Atlantic war and its subsequent peace.','A South Atlantic war between Argentina and Britain has ended.') for r in a['requirements']]
D['integration']['chronology']='Precedent dates are research anchors, not automatic unlock dates for every negotiated policy. Earlier bilateral agreements are explicit alternate-history accelerations requiring both players. Named formations and leaders still require real organizational/leadership transitions. Native party trigger ideology names identify engine array slots, while visible Argentine names come from the actual local registry.'
D['integration']['timed']='Party-sourced event programmes require their exact incumbent party and, for the Menem mandate, exact leader. They deactivate when the owner leaves; a return before fixed expiry restores only the remaining term. National crises and already incurred liabilities follow their separately stated lifetimes. Event option modifiers and an additional attached spirit have separate explicit durations.'
for d in D['decisions']:
    d['effect_lines']={'constitutional_election':['Hold a national election.'],
        'civilian_handover':['Install the elected national leader.']}.get(d['key'],[])
    d['modifier_spirit']={'asset_sales':'Asset Sale Settlement','debt_restructuring':'Restructuring under Creditor Review'}.get(d['key'],d['title'])
    if d['key'] in ['constitutional_election','civilian_handover']:d['remove']=[P+'start_regime']
    if d['key']=='constitutional_election':d['requirements']+=['The elected government takes office before the regime spirit is removed.']
PARTY_ART={22:'army',13:'peronism',3:'ucr',2:'industry',16:'bank',1:'conservatism',14:'christian',4:'communist',
           5:'revolution',19:'revolution',18:'labor',20:'labor',6:'christian',0:'conservatism',15:'farm','PS':'socialism'}
for n in D['nodes']:
    if n['icon']=='politics' and n['party'] is not None:n['icon']=PARTY_ART[n['party']]
# Keep the regional and overseas diplomatic fans distinct, with a real funded commercial-mission root.
node('overseas_missions','Overseas Trade Missions','diplomacy',0,10,mods=mm(trade=.02,bur=.02),money=2,
     desc='Fund commercial attaches, technical translation and partner-country offices for overseas agreements.',icon='diplomacy')
for n in D['nodes']:
    if n['key'] in ['soviet_grain','us_training','french_aviation','spanish_industry']:
        n['y']+=2;n['dy']+=2;n['prerequisites']=[[P+'overseas_missions']]
    if n['key'] in ['soviet_science','us_credit','nonaligned_medical','peruvian_maintenance']:
        n['y']+=2;n['dy']+=2
        if n['key'] in ['nonaligned_medical','peruvian_maintenance']:n['prerequisites']=[[P+'overseas_missions']]
    if n['key']=='southatlantic_science':n['y']=20;n['dy']=20;n['prerequisites']=[[P+'overseas_missions']]
    if n['key']=='regional_protocols':n['y']=8;n['dy']=8
TITLE_EDITS={
 'army_directives':'Command Directives','service_rotation':'Rotate the Commands','cabinet_rules':'Collective Cabinet Rules',
 'state_enterprises':'Public Enterprise Fund','illia_medicines':'Medicines and Health','federal_industry':'Federal Industry Zones',
 'technical_contracts':'Technical Contracts','strict_subsidies':'End Untargeted Subsidies','property_register':'Reliable Property Titles',
 'pca_front':"A Workers' Front",'pca_engineers':'Public Industry Engineers','pca_compensation':'Negotiated Ownership',
 'pca_sovereign':'Socialist Independence','pca_moscow':'Soviet Technical Links','mont_command':'Revolutionary Command',
 'mont_state':'Revolutionary Industry','prt_pluralism':"Plural Workers' Rule",'prt_revolution':'Revolutionary Rule',
 'prt_literacy':"Workers' Skills",'prt_nonalignment':'Revolutionary Autonomy','cgta_councils':'Independent Councils',
 'cgta_coalition':'Democratic Labor Front','cgta_public_credit':'Cooperative Credit','union_pact':'Bargained Production',
 'union_industry':'Industrial Bargaining','union_democracy':'Secret Union Ballots','cattle_health':'Veterinary Standards',
 'socialist_tax':'Progressive Revenue','economic_survey':'National Economic Survey','banking_rules':'Bank Currency Rules',
 'cold_chain':'Cold Storage Standards','federal_corridors':'North-South Connections','fuego_incentives':'Fuegian Promotion Zone',
 'regional_equalization':'Regional Services','statistical_office':'Independent Statistics','naval_maintenance':'Naval Maintenance',
 'tam_programme':'Medium Tank Programme','spares_stock':'Strategic Spare Parts','supplier_review':'Procurement Basis',
 'french_standard':'French Technical Basis','american_standard':'US Technical Basis','defence_accounts':'Audited Defense Accounts',
 'reactor_partners':'Reactor Contracts','research_exchange':'Academic Exchange Office',
 'sanmartin_desk':'San Martin Palace Desk','brazil_trade':'Brazilian Industrial Pact','soviet_science':'Soviet Academic Links',
 'french_aviation':'French Aviation Links','nonaligned_medical':'Cuban Health Exchange','peruvian_maintenance':'Peruvian Depot Accord',
 'regional_protocols':'Regional Protocols','sovereignty_talks':'Talks under Reservation','coercive_strategy':'South Atlantic Coercion',
 'war_cabinet':'South Atlantic Cabinet','mainland_cover':'Retain Mainland Reserves','madrid_contacts':'Madrid Confidence Pact',
 'madrid_normalization':'Diplomatic Restoration','atlantic_reconstruction':'Atlantic Reconstruction',
}
for n in D['nodes']:n['title']=TITLE_EDITS.get(n['key'],n['title'])
# Gas purchase transfers: Argentina pays 0.002 to Bolivia plus 0.001 operating cost.
next(a for a in D['agreements'] if a['id']=='bolivia_gas')['argentina']['weekly']=.003
for a in D['agreements']:
    a['recipient']['spirit']=a['title']+': '+COUNTRIES[a['partner']]
    if a['id']=='uruguay_navigation':a['source']='1973 Treaty of the River Plate and its Maritime Front. State ownership checked against current target history.'
for n in D['nodes']:
    g=next(g for g in D['groups'] if g['id']==n['group'])
    if n['id']==g['anchor']:n['anchor']=None;n['dx']=n['x'];n['dy']=n['y']
    else:n['anchor']=g['anchor']
    if n['leader']:n['lifetime']='leader'
    if n['temporary']:n['lifetime']=n['temporary']
    n['availability_code']=((TRIGGERS[n['party']]+' = yes') if isinstance(n['party'],int) else
       ('neutrality_neutral_social_are_in_power = yes\n# Proposed exclusive PSD incumbent identity, not yet registered' if n['party']=='PS' else ''))
    if n['party']==18:n['availability_code']+='\n# CGTA incumbent identity; excludes proposed PSD incumbent alias'
    if n['leader']:n['availability_code']+='\n# Actual incumbent must be '+n['leader']
    if n.get('leader_names'):n['availability_code']+='\n# Exact existing leader names: '+json.dumps(n['leader_names'],ensure_ascii=False)
    if n['requirements']:n['availability_code']+='\n# Gameplay requirements: '+'; '.join(n['requirements'])
    if n['wargoal']:n['availability_code']+='\nhidden_trigger = { country_exists = ENG NOT = { has_war_with = ENG } ENG = { owns_state = 26 controls_state = 26 } }'
    n['proposed_code']='\n'.join(
        ([f'set_temp_variable = {{ treasury_change = {-n["money"]:g} }}','modify_treasury_effect = yes'] if n['money'] else [])+
        [f'# Proposed {n["lifetime"]} programme modifier: {k} = {v:g}' for k,v in n['modifiers'].items()]+
        ([f'# Weekly additional_expenses_rate contribution, once active: {n["weekly"]:.5f}'] if n['weekly'] else [])+
        [f'{b["state"]} = {{ add_extra_state_shared_building_slots = {b["slots"]} add_building_construction = {{ type = {b["type"]} level = {b["levels"]} instant_build = yes }} }}' for b in n['buildings']]+
        [f'add_tech_bonus = {{ name = {n["id"]} category = {r["category"]} bonus = {r["bonus"]:g} uses = {r["uses"]} }}' for r in n['research']]+
        [f'{k}_experience = {v}' for k,v in n['xp'].items()]+
        ([f'add_doctrine_cost_reduction = {{ name = {n["id"]} category = {n["doctrine"][0]} cost_reduction = {n["doctrine"][1]:g} uses = {n["doctrine"][2]} }}'] if n['doctrine'] else [])+
        ([f'create_wargoal = {{ type = {n["wargoal"]["type"]} target = {n["wargoal"]["target"]} generator = {{ '+ ' '.join(map(str,n['wargoal']['states']))+f' }} expire = {n["wargoal"]["expire"]} }}'] if n['wargoal'] else [])+
        ([f'# Recipient-controlled proposal: {n["agreement"]}'] if n.get('agreement') else [])+
        ([f'# Unlock decision contract: {n["decision"]}'] if n['decision'] else []))

def fmt_mods(mods):
    labels={v[0]:v[1] for v in STATS.values()}
    return '; '.join(f'{labels[k]} {v:+g} pp' if k=='interest_rate_multiplier_modifier' else f'{labels[k]} {v*100:+g}%' for k,v in mods.items()) or 'No direct modifier change'

def validate():
    nodes=D['nodes']; ids={n['id']:n for n in nodes}; errors=[]
    if len(ids)!=len(nodes):errors.append('Duplicate focus IDs')
    for n in nodes:
        for ps in n['prerequisites']:
            for p in ps:
                if p not in ids:errors.append('Missing parent '+p)
        for p in n['excludes']:
            if p not in ids or n['id'] not in ids[p]['excludes']:errors.append('Asymmetric exclusion '+n['id'])
        if n['anchor']:
            a=ids[n['anchor']]
            if (a['x']+n['dx'],a['y']+n['dy'])!=(n['x'],n['y']):errors.append('Bad resolved anchor '+n['id'])
        for b in n['buildings']:
            if b['slots']!=b['levels']:errors.append('Missing slots '+n['id'])
        for field in ('decision','event'):
            if n.get(field) and not any(r['key']==n[field] for r in D[field+'s']):errors.append('Missing '+field+' '+n[field])
        if n['wargoal']:
            if any(n['wargoal'].get(k)!=v for k,v in dict(type='take_state_focus',target='ENG',states=[26],expire=730).items()) or n['decision']:
                errors.append('Incorrect Falklands war-goal contract '+n['id'])
    coords=Counter((n['x'],n['y']) for n in nodes)
    if any(v>1 for v in coords.values()):errors.append('Duplicate coordinates')
    # Compatible-history solver keeps full chosen ancestry, including reciprocal exclusions.
    cache={}; visiting=set()
    def paths(key):
        if key in cache:return cache[key]
        if key in visiting:raise ValueError('Cycle '+key)
        visiting.add(key);n=ids[key];plans=[frozenset([key])]
        for ps in n['prerequisites']:
            choices=[plan for pid in ps for plan in paths(pid)]
            merged=[]
            for a in plans:
                for b in choices:
                    c=a|b
                    if not any(set(ids[p]['excludes'])&c for p in c):merged.append(c)
            # Minimal compatible ancestor sets suffice; bound duplicate OR histories.
            plans=list(set(merged))
        visiting.remove(key);cache[key]=plans;return plans
    for key in ids:
        if not paths(key):errors.append('Impossible prerequisite history '+key)
    for a in D['agreements']:
        if a['parent'] and not any(b['id']==a['parent'] for b in D['agreements']):errors.append('Missing agreement parent')
        for side in ('argentina','recipient'):
            for f in ('weekly','credit'):
                if len(str(a[side][f]).split('.')[-1])>5:errors.append('Long budget literal')
        if a['argentina']['credit']>a['recipient']['weekly'] or a['recipient']['credit']>a['argentina']['weekly']:errors.append('Unfunded transfer '+a['id'])
    report=dict(project='IMPERIA COLD WAR',focuses=len(nodes),groups=len(D['groups']),party_programmes=sum(g['party'] is not None for g in D['groups']),
                exclusive_pairs=sum(len(n['excludes']) for n in nodes)//2,agreements=len(D['agreements']),events=len(D['events']),errors=errors,
                all_prerequisite_histories_satisfiable=not any('history' in e for e in errors),bounds=dict(x=[min(n['x'] for n in nodes),max(n['x'] for n in nodes)],y=[min(n['y'] for n in nodes),max(n['y'] for n in nodes)]),
                limits='Model/source checks only. Gameplay gates, leader installation, native route rendering and multiplayer need implementation and engine validation.')
    D['meta']=report
    (HERE/'MODEL_QA.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if errors:raise ValueError(errors)
    return report

def emit_fixture():
    lines=['# IMPERIA COLD WAR — Argentina review-only spatial focus fixture. Not loaded or approved runtime code.',
           '# Rewards are specified in COLDWAR_ARG_design.json and the inspector. This fixture independently checks only native graph grammar.',
           'focus_tree = {',' id = COLDWAR_ARG_1970_REVIEW_ONLY']
    for n in D['nodes']:
        lines += [' focus = {',f'  id = {n["id"]}',f'  x = {n["dx"]}',f'  y = {n["dy"]}',f'  cost = {n["cost"]:g}']
        if n['anchor']:lines += [f'  relative_position_id = {n["anchor"]}']
        for ps in n['prerequisites']:lines += ['  prerequisite = { '+' '.join('focus = '+p for p in ps)+' }']
        if n['excludes']:lines += ['  mutually_exclusive = { '+' '.join('focus = '+p for p in n['excludes'])+' }']
        if isinstance(n['party'],int):lines += ['  available = { '+TRIGGERS[n['party']]+' = yes }']
        lines += [' }']
    lines += ['}']
    (HERE/'proposal_graph_fixture.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def dossier():
    rows=['IMPERIA COLD WAR','# Argentina: January 1970 to 1990','',
          '**Approval-stage concept. '+str(len(D['nodes']))+' focuses, '+str(D['meta']['exclusive_pairs'])+' mutual-exclusion pairs, '+str(len(D['agreements']))+' bilateral offers and '+str(len(D['events']))+' events. No loaded game files have been changed.**','',
          'The preview, catalogue and spatial fixture share one coordinate model. Default focus cost 5 means 35 days; selected reviews cost 3 means 21 days. Values are proposed multiplayer balance, not measurements of historical causal effects.','',
          'Native MD comparison: installed workshop version 2.0.4, local Cold War base metadata 2.0.3, HOI4 1.19. France and Russia are reference trees; Argentina uses its own institutions, parties and budget. All player-facing language is English.','',
          '## Reading and political ownership','',D['integration']['sync'],'',D['integration']['policy'],'',
          'All party branches remain visible. Exact native current-party triggers gate execution, and actual leader identity additionally gates named leader programmes. CGTA and the provisional PSD alias cannot be incumbents simultaneously. The native Yes/No party requirement resolves the actual Argentine party name, without inventing a governing-current label.','',
          D['integration']['constitutional'],'',D['integration']['timed'],'',D['integration']['chronology'],'',D['integration']['uranium'],'',
          '## Sections and exact anchor positions','', '| Section | Anchor | Focuses | Governing owner |','|---|---:|---:|---|']
    for g in D['groups']:
        rows += [f'| {g["title"]} | ({g["x"]},{g["y"]}) | {sum(n["group"]==g["id"] for n in D["nodes"])} | {PARTIES.get(str(g["party"]),"National")} |']
    rows += ['','## Starting spirits','']
    for s in D['spirits']:rows += ['### '+s['name'],'',s['description'],'','- '+fmt_mods(s['modifiers']),'- Remedy: '+s['remedy'],'']
    rows += ['## Bilateral contracts','',D['integration']['agreements'],'',D['integration']['finance'],'',D['integration']['buildings'],'']
    for a in D['agreements']:
        rows += ['### '+a['title'],'',a['description'],'','Historical precedent: '+a['source'],'']
        for side,tag in [('argentina','ARG'),('recipient',a['partner'])]:
            t=a[side]
            rows += [f'**{COUNTRIES[tag]}**: treasury -${t["setup"]:.3f} billion; additional expenses +${t["weekly"]:.5f} billion weekly; additional income +${t["credit"]:.5f} billion weekly.',
                     '- Add '+t['spirit']+': '+fmt_mods(t['modifiers'])]
            if t.get('grant'):rows += [f'- Treasury: +${t["grant"]:.3f} billion once.']
            if a.get('territory'):rows += [f'- {STATES[a["territory"]["state"]]}: '+('gain state ownership, without a core.' if tag==a['territory']['to_country'] else 'transfer state ownership to Argentina.')]
            for b in a['buildings']:
                if b['country']==tag:rows += [f'- {STATES[b["state"]]}: +{b["slots"]} shared building slots, then +{b["levels"]} {b["type"]}.']
            for r in a['research']:
                if r['country']==tag:rows += [f'- {r["uses"]} x {r["bonus"]*100:g}% research bonus: {r["category"]}.']
        rows += ['','Requirements: '+' '.join(a['requirements']+a['conditions']),'',a['historical_mode'],'']
    rows += ['## Conditional crises','']
    for s in D['conditional_spirits']:rows += ['### '+s['name'],'',s['description'],'',fmt_mods(s['modifiers']),'',s['activation'],'',s['remedy'],'']
    rows += ['## Decision contracts','']
    for d in D['decisions']:
        rows += ['### '+d['title'],'','Requirements: '+' '.join(d['requirements']),f'Treasury {-d["money"]:+.3f} billion; expenses +${d["weekly"]:.5f} billion weekly.',fmt_mods(d['modifiers'])]
        rows += ['- '+a for a in d.get('actions',[])]+['',d['replay'],'']
    rows += ['## Events','']
    for e in D['events']:
        rows += ['### '+e['title'],'',e['description'],'','Trigger: '+e['trigger'],'']
        for o in e['options']:
            rows += [f'- **{o["name"]}**: treasury {-o["money"]:+.3f} billion; expenses +${o["weekly"]:.5f} billion weekly; '+fmt_mods(o['modifiers'])+(f'; {o["duration"]} days.' if o['duration'] else '.')]
            for k in ['require','leader','decision','add_spirit','remove_spirit']:
                if k in o:rows += ['  '+k+': '+o[k]]
            if o.get('add_spirit_duration'):rows += [f'  Separate attached spirit duration: {o["add_spirit_duration"]} days.']
        rows += ['']
    rows += ['## Exact focus catalogue','']
    ids={n['id']:n for n in D['nodes']}
    for g in D['groups']:
        rows += ['### '+g['title'],'',g['description'],'']
        for n in [n for n in D['nodes'] if n['group']==g['id']]:
            rows += ['#### '+n['title'],'',f'`{n["id"]}`. Absolute ({n["x"]},{n["y"]}); relative anchor `{n["anchor"] or "none"}`; emitted offset ({n["dx"]},{n["dy"]}); {n["days"]} days; {n["lifetime"]} programme.','',n['description'],'']
            if n['prerequisites']:rows += ['Prerequisites: '+' AND '.join('('+' OR '.join(ids[p]['title'] for p in ps)+')' for ps in n['prerequisites'])+'.']
            if n['excludes']:rows += ['Exclusions: '+', '.join(ids[p]['title'] for p in n['excludes'])+'.']
            if n['availability_code']:rows += ['Availability/reward guard: `'+n['availability_code'].replace('\n','; ')+'`.']
            rows += [f'- Treasury -${n["money"]:.3f} billion; expenses +${n["weekly"]:.5f} billion weekly.','- '+fmt_mods(n['modifiers'])]
            for k in ['remove','replace','buildings','research','xp','doctrine','wargoal','decision','event','agreement']:
                if n.get(k):rows += ['- '+k+': '+json.dumps(n[k],ensure_ascii=False)]
            rows += ['']
    rows += ['## Approval and verification boundary','',
             'Read history_research.md, md_reference_profile.md and mechanics_reference.md for source evidence. Each proposed policy family is tied to the historical institutions in those records. Layout and mechanics reviewers inspect the concept independently. Numeric values remain balance proposals.','',
             'No event photo is represented as a native screenshot. Country-event art composition requires full live donor-window inspection after approval, preserving the original outer frame and alpha pixels. The current preview uses focus sprites only.','',
             'Static model, emitted spatial fixture and browser checks do not prove HOI4 load behavior, native tooltip formatting or multiplayer synchronization. No engine test has been performed.','',
             '### Explicit integration decisions remaining','']+['- '+s for s in D['integration']['unresolved']]
    (HERE/'COLDWAR_ARG_CONCEPT.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')

def art_and_preview():
    ART={};sources=[]
    defs='\n'.join(p.read_text(encoding='utf-8-sig',errors='replace') for p in (ROOT/'interface').glob('*.gfx'))
    sprites={m.group(1):m.group(2) for m in re.finditer(r'name\s*=\s*"([^"\n]+)"(?:(?!spriteType).)*?texturefile\s*=\s*"([^"\n]+)"',defs,re.S|re.I)}
    candidates={'politics':['government_beu','Election_graphics'],'democracy':['elections_01','election2'],'ucr':['focus_ARG_the_clean_election'],
      'social':['generic_healthcare','focus_generic_full_social_mobilization'], 'farm':['farming','focus_CHL_focus_on_cattle_and_wool'],
      'industry':['industrial_complexes','focus_CHL_enlarge_the_textile_industries'], 'bank':['focus_ARG_banco_central_de_la_republica_argentina','focus_CHL_strengthen_the_central_bank'],
      'army':['Argentine_Army','army_doctrine','army_general_stuff1'],'tank':['army_tank_industry'],'air':['Argentine_Air_Force','air_doctrine','air_defense'],
      'navy':['Argentine_Navy','naval_doctrine'],'energy':['focus_ARG_develop_the_electricity_sector','electricity'],'infra':['infrastructure','construct_infrastructure'],
      'nuclear':['nuclear_energy','nuclear_science'],'research':['research','science'],'diplomacy':['diplomacy','aggressive_diplomacy'],
      'argentina':['focus_ARG_argentine_island_sovereignty','flag_argentina','align_to_argentina'],'brazil':['align_to_brazil','diplomacy'],'chile':['align_to_chile','diplomacy'],
      'soviet':['align_to_soviet_union','diplomacy'],'usa':['align_to_america','diplomacy'],'france':['align_to_france','diplomacy'],'britain':['focus_ARG_envoy_to_london','diplomacy'],
      'peronism':['focus_ARG_peronism','flag_argentina'],'communist':['focus_ARG_legitimize_the_PCA','democratic_communism'],
      'conservatism':['focus_ARG_maintain_the_status_quo','government_beu'],'christian':['catholicism_new','christianity'],
      'revolution':['focus_generic_workers_and_farmers_rise','labor_unions'],'labor':['labor_unions','union_negotiations'],'socialism':['social_democracy','democracy'],
      'bar':['GFX_focus_can_start','GFX_focus_unavailable'],'barlocked':['GFX_focus_unavailable']}
    # Fallbacks remain real registered local sprites. Every selected source is recorded.
    candidates['tank'] += ['army_doctrine']
    for kind,names in candidates.items():
        for name in names:
            tex=sprites.get(name)
            if not tex:continue
            path=ROOT/tex
            if not path.exists():path=DONOR/tex
            if not path.exists():path=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV')/tex
            if not path.exists():continue
            try:
                im=Image.open(path).convert('RGBA');im.thumbnail((165,128) if kind.startswith('bar') else (110,100))
                buf=io.BytesIO();im.quantize(colors=128,method=Image.Quantize.FASTOCTREE).save(buf,format='PNG',optimize=True)
                ART[kind]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
                sources.append(dict(kind=kind,sprite=name,path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),author='Millennium Dawn or underlying game asset; individual original artist unknown',licence='Separate redistribution permission unknown',modifications='DDS decoded, proportionally reduced and PNG palette limited to 128 colors for local concept review. No ownership claim.'))
                break
            except (OSError,ValueError):continue
    assert not set(candidates)-set(ART),set(candidates)-set(ART)
    sheet=Image.new('RGB',(720,((len(ART)+5)//6)*150),(33,45,36)); draw=ImageDraw.Draw(sheet)
    for i,(kind,url) in enumerate(ART.items()):
        thumbnail=Image.open(io.BytesIO(base64.b64decode(url.split(',',1)[1]))).convert('RGBA')
        thumbnail.thumbnail((98,88))
        xx=(i%6)*120+(120-thumbnail.width)//2;yy=(i//6)*150+8
        sheet.paste(thumbnail,(xx,yy),thumbnail)
        draw.text(((i%6)*120+4,(i//6)*150+102),kind,fill=(240,230,205))
    sheet.save(HERE/'preview-art-contact.png')
    D['art_sources']=sources
    (HERE/'COLDWAR_ARG_design.json').write_text(json.dumps(D,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    fragment=(HERE/'preview.template.html').read_text(encoding='utf-8').replace('__DATA__',json.dumps(D,ensure_ascii=False,separators=(',',':'))).replace('__ART__',json.dumps(ART,separators=(',',':')))
    assert len(fragment.encode())<1000000,len(fragment.encode())
    (VIS/'argentina-coldwar.html').write_text(fragment,encoding='utf-8')
    (HERE/'COLDWAR_ARG_preview.html').write_text(fragment,encoding='utf-8')
    wrapper='<!-- IMPERIA COLD WAR — Argentina standalone concept review wrapper. -->\n<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+fragment+'</body></html>'
    (HERE/'preview-review.html').write_text(wrapper,encoding='utf-8')
    (HERE/'PREVIEW_PROVENANCE.json').write_text(json.dumps(dict(project='IMPERIA COLD WAR',source_version='Installed MD 2.0.4, target Cold War metadata 2.0.3',assets=sources,
        preview='Concept donor-art composition, not an HOI4 screenshot. Browser font and connector routing approximate native rendering.',
        credit='Concept and local rendered review by project assistant. Third-party authors/permissions remain as individually recorded; missing information is unknown.'),indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    print(json.dumps(validate()));emit_fixture();dossier()
    if (HERE/'preview.template.html').exists():art_and_preview()
