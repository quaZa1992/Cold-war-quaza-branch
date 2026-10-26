"""Explicit common-focus reward redesign. This writes a design catalogue only."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
P='COLDWAR_VIE_'
KEYS=dict(pp='political_power_factor',stab='stability_factor',war='war_support_factor',research='research_speed_factor',build='production_speed_buildings_factor',civbuild='production_speed_industrial_complex_factor',infra='production_speed_infrastructure_factor',mil='industrial_capacity_factory',cap='production_factory_max_efficiency_factor',gain='production_factory_efficiency_gain_factor',repair='industry_repair_factor',bomb='industry_air_damage_factor',core='army_core_defence_factor',supply='supply_consumption_factor',recruit='conscription_factor',training='training_time_army_factor',org='army_org_factor',bureau='bureaucracy_cost_multiplier_modifier',education='education_cost_multiplier_modifier',social='social_cost_multiplier_modifier',agri='agricolture_productivity_modifier',market='mdcw_cw_market_exposure',sanctions='imp_sanction_resistance',tax='corporate_tax_income_multiplier_modifier',planning='max_planning_factor',entrench='max_dig_in',entrench_speed='dig_in_speed_factor',morale='army_morale_factor')
patches=[]
def bonus(category,uses=1,amount=.5):return dict(type='research_bonus',category=category,uses=uses,bonus=amount)
def doctrine(amount=.25,uses=1,category='land_doctrine'):return dict(type='doctrine_bonus',category=category,uses=uses,cost_reduction=amount)
def xp(amount,kind='army'):return dict(type=kind+'_xp',amount=amount)
def put(suffix,why,rewards=None,**mods):
    row=dict(id=P+suffix,group=suffix.split('_')[0],modifiers={KEYS[k]:v for k,v in mods.items()},rewards=rewards or [],why_player_wants_it=why,role='Institutional national development; finite rewards are one-time',lifecycle='national_persistent')
    patches.append(row);return row

# State formation is a choice of institutions rather than a bill for an unlock.
put('state_root','A functioning secretariat reduces administration costs immediately and opens actual political consultations.',bureau=-.04,pp=.08)
r=put('state_emerging','The next extraordinary cadre budget pays for a trained reserve network and wartime cohesion.',war=.10,training=-.04,social=.01)
r.update(label='Fund Reserve Training Networks',support=None,description='Assign the next extraordinary cadre, salary and transport allocation to district reserve instructors. Local mobilisation will be better prepared, while provincial civilian offices must wait for their own expansion programme.')
r=put('state_western','The same cadre budget can instead fund functioning provincial offices and predictable public services.',stab=.06,bureau=-.04,war=-.02)
r.update(label='Fund Provincial Civil Offices',support=None,description='Assign the next extraordinary cadre, salary and transport allocation to provincial civil offices. Better local records and public services reduce administrative waste, while the reserve training network receives no equivalent expansion from this allocation.')
r=put('state_neutral','A rural advisory compact brings cooperative administrators and local producers into practical input and distribution planning.',agri=.05,stab=.04,pp=-.03)
r['description']='A broader Front must offer rural representatives a practical role. Establish an advisory compact on farm inputs and local distribution, using their knowledge to improve deliveries while accepting that the Party cannot dictate every recommendation.'
r=put('state_national','Sovereign procurement develops spare-part stocks and repair organisation instead of relying on a declaration of independence.',sanctions=.10,core=.04,bureau=.01)
r['description']='Sovereignty must be supported by the ability to keep workshops and defensive units supplied. Establish domestic spare-part stocks, repair arrangements and alternative procurement contacts, accepting the cost of maintaining this independent organisation.'
put('state_cadres','A professional civil service substantially reduces bureaucracy and improves technical administration.',bureau=-.08,research=.03,education=.02)
put('state_mass','Mass organisations provide wartime cohesion and an organised reserve network.',war=.08,org=.04,pp=.12,bureau=.02)
put('state_school','Basic rural literacy supports recruit training and improves the national base for further education.',research=.03,training=-.04)
put('state_women','Participation by women expands agricultural and workshop labour rather than multiplying a signed growth rate.',agri=.04,mil=.04,social=.02)
put('state_assembly','An accountable assembly improves the existing cadre-state spirit and cuts recurring administration.',stab=.04,bureau=-.03)
put('state_discipline','Central inspection raises collection from enterprises and makes procurement more reliable.',tax=.08,cap=.04,research=-.01)
put('state_criticism','Protected criticism exposes failed projects and improves technical problem solving.',[bonus('CAT_construction')],research=.03,build=.04,pp=-.03)
put('state_provincial','Provincial offices cut duplication and deliver local roads faster.',bureau=-.04,infra=.10)
put('state_religion','Religious accommodation improves social stability while reducing costly civic disputes.',stab=.05,social=-.03)
put('state_charter','The charter completes another cadre-state recovery stage and stabilises government beyond one leader.',stab=.04,pp=.06)

# Reconstruction: one rehabilitated civilian complex, then normal paid projects.
r=put('industry_root','Rehabilitation delivers the first real civilian workshop and reduces the war-damage spirit.')
r.update(label='Rehabilitate Hanoi Workshops',cash=.15,building=[522,'industrial_complex'],instant_build=True,days=70,description='Bombing and interrupted supply have left workshops idle. Restore a working civilian production centre in Hanoi, put its machinery back into use and establish the base from which wider reconstruction can proceed.')
put('industry_disperse','Dispersed workshops survive bombing and can be repaired quickly.',bomb=-.20,repair=.10,build=-.03)
put('industry_concentrate','Concentrated industrial centres build faster and sustain longer production runs.',build=.08,cap=.08,bomb=.05)
put('industry_repair','Mobile crews restore damaged factories and transport without drawing a permanent penalty from farms.',repair=.15,infra=.10)
put('industry_power','The paid power-plant project creates actual generation capacity; it also speeds later utility works.',infra=.06)
put('industry_roads','The road project improves a physical state and the war-damage recovery stage.',supply=-.03)
put('industry_capital','Machine-building research and better project execution support investment rather than pretending capital goods are munitions.',[bonus('CAT_industry')],build=.08,cap=.06,civbuild=-.03)
put('industry_consumer','Civilian production supplies faster investment and cheaper social provision.',civbuild=.12,social=-.04,mil=-.03)
r=put('industry_machine','The northern workshop network receives a funded armament production line rather than another percentage on zero military capacity.')
r.update(building=[524,'arms_factory'],label='Equip the Northern Workshops',description='The northern workshop network must be able to repair and produce the equipment the army consumes. Equip a military production line within the reconstruction programme while the rest of the country continues to demand scarce machinery.')
r=put('industry_goods','The restored Hanoi workshops now expand tools and civilian construction capacity.',civbuild=.08,gain=.05)
r.update(building=None,cash=.04,label='Expand Civilian Toolmaking',description='A working workshop is only the beginning. Expand the supply of tools, spare parts and trained supervisors needed by civilian construction, rather than forcing every project to compete for the same imported equipment.')
put('industry_skills','Technicians bring a finite industrial research breakthrough and faster rebuilding.',[bonus('CAT_industry')],research=.03,education=.02)
put('industry_self','Domestic components keep production running through restrictions and missing imports.',sanctions=.10,gain=.10,build=-.02)
put('industry_imports','Specialist imports deliver two industrial research opportunities and faster modernisation.',[bonus('CAT_industry',uses=2)],build=.06,market=.05)
put('industry_depot','A national repair depot restores industrial capacity and retains usable production techniques.',repair=.12,cap=.05)
put('industry_engineers','Engineering contracts provide construction research and better project execution.',[bonus('CAT_construction')],build=.04,bureau=.01)
put('industry_recovery','The final recovery stage removes the remaining approved war-damage burden and improves normal construction.',build=.04)

# Food policy has output, distribution and insurance outcomes, not invented grain.
put('farm_root','Rice supply administration now raises actual agricultural productivity.',agri=.06,social=.01)
put('farm_procure','Predictable procurement supports ration stability and military distribution.',stab=.06,supply=-.06,agri=-.02)
put('farm_plots','Household surplus incentives deliver a substantially larger harvest.',agri=.10,pp=-.03)
put('farm_irrigate','Irrigation creates the paid agricultural district and protects subsequent repair work.',repair=.05)
put('farm_market','Market access improves the taxable rural trading network as well as the harvest.',agri=.03,tax=.06)
put('farm_reserves','A reserve system reduces the rationing spirit and emergency social expenditure.',stab=.04,social=-.04)
r=put('farm_inputs','Capital-intensive inputs improve yields and bring a practical industrial research application.',[bonus('CAT_industry',amount=.35)],agri=.07,market=.03)
r.update(label='Prioritize Fertiliser and Tools',description='Allocate the next rural investment programme to fertiliser, tools and repair capacity. Better inputs can raise yields without transferring still more labour into the fields, although imported supplies expose the programme to external disruption.')
r=put('farm_labour','Labour-intensive rural teams improve yields and road building without waiting for imported machinery.',agri=.06,infra=.12,mil=-.02)
r.update(label='Expand Rural Labour Teams',description='Allocate the next rural investment programme to organised labour, drainage and local access roads. It can proceed with fewer imported inputs, but the workers assigned to it cannot simultaneously fill the northern workshops.')
put('farm_district','The second agricultural district is a physical funded expansion of food production.')
put('farm_dykes','Dykes and roads create the paid infrastructure project and faster flood recovery.',repair=.08)
put('farm_health','Better nutrition and rural services support social stability and recruit health.',stab=.05,training=-.04,social=.01)
r=put('farm_ration','Universal price support provides strong stability and lower emergency welfare pressure.',stab=.08,social=-.05,bureau=.02)
r.update(label='Fund Universal Food Support',description='Use the next food-security allocation to protect basic consumption and predictable prices. Broad support cushions households when distribution fails, while its administration must reach far beyond the most productive villages.')
r=put('farm_contract','Production contracts raise output and formal taxable rural trade.',agri=.08,tax=.05,market=.02)
r.update(label='Fund Household Production Contracts',description='Use the next food-security allocation to reward additional household deliveries. Contracted surplus can rebuild supplies and rural trade, but incomes become more exposed to prices and uneven market access.')
put('farm_distribution','Distribution reform removes recurring administrative waste and improves transport.',bureau=-.06,supply=-.03)
put('farm_surplus','Marketed surplus improves agricultural returns and develops taxable enterprise.',agri=.04,tax=.06)
put('farm_security','Food security improves the final rationing stage and reduces emergency welfare needs.',agri=.03,social=-.03)

# Every service receives its own finite professional reward.
put('army_root','The doctrinal review gives experience that can actually be spent and a finite doctrine discount.',[xp(25),doctrine()])
put('army_local','Territorial institutions provide entrenchment and strong homeland defence.',[doctrine()],core=.10,entrench=2,planning=-.03)
put('army_combined','Combined-arms organisation improves the main army and offensive preparation.',[doctrine()],org=.08,planning=.05,supply=.03)
put('army_supply','Redundant routes reduce the army supply burden rather than simply moving a construction penalty.',[xp(15)],supply=-.08,repair=.05)
put('army_staff','A working general staff improves planning and provides usable doctrinal training.',[xp(20),doctrine()],org=.04,planning=.04,education=.01)
put('army_airdefence','The Hanoi anti-aircraft project is backed by trained air-defence personnel.',[xp(15,'air')])
put('army_austerity','A smaller professional establishment is cheaper to supply and better organised.',supply=-.07,org=.04,recruit=-.04)
put('army_reserve','A genuine reserve provides more available manpower and faster training.',recruit=.12,training=-.08,agri=-.03)
put('army_repair','Refurbishment gives an infantry research opportunity and more efficient production.',[bonus('CAT_infantry_weapons')],cap=.06,gain=.08)
put('army_drill','Reserve cadres provide immediate experience and reduce training time.',[xp(25),doctrine()],training=-.06,education=.01)
put('army_coast','The common coastal survey trains both services before their specialised programmes.',[xp(15,'navy'),xp(15,'air')])
put('army_coastal','Coastal fortification gains entrenchment and manpower-efficient defence.',[doctrine(category='naval_doctrine')],core=.05,entrench=1)
put('army_fleet','The paid dockyard is accompanied by useful naval experience and doctrine development.',[xp(25,'navy'),doctrine(category='naval_doctrine')])
put('army_civil','Civil-defence teams improve mobilisation recovery and restore bombed installations.',repair=.10,bomb=-.10,social=.01)
r=put('army_aircrew','Aircrew training gives air experience and a real air-doctrine discount, independent of buying a dockyard.',[xp(35,'air'),doctrine(category='air_doctrine')],education=.02)
r['prerequisites']=[[P+'army_coast']]
r.update(x=32,y=20,emitted_x=4,emitted_y=7,anchor=P+'army_root')
put('army_postwar','The service settlement reduces the mobilisation burden and returns labour to reconstruction.',build=.05,agri=.03,recruit=-.04)

# Negotiating and fighting can coexist; the fork allocates additional effort.
put('unity_root','A common war-and-peace mandate offers cohesion and real operational study.',[xp(15)],war=.08)
r=put('unity_pressure','Concentrated battlefield effort improves organisation and planning.',[doctrine()],org=.06,planning=.04,supply=.03)
r.update(label='Concentrate Battlefield Pressure',description='Concentrate additional staff work and supplies on battlefield pressure. Negotiations remain possible, but this allocation seeks leverage through the army and commits resources that cannot also enlarge the diplomatic effort.')
r=put('unity_paris','A strengthened negotiating mandate improves stability and homeland staying power.',stab=.06,core=.04,bureau=.01)
r.update(label='Strengthen the Negotiating Mandate',description='Concentrate additional staff and political effort on a credible negotiating position. The armed struggle need not cease, but the delegation must be able to defend specific terms and maintain confidence that a settlement will be honoured.')
put('unity_corridors','Southern corridors lower supply demand and train infrastructure planners.',[bonus('CAT_construction',amount=.35)],supply=-.06)
put('unity_terms','Guarantees improve public confidence and reduce the cost of administering a settlement.',stab=.04,bureau=-.03)
put('unity_aftermath','Recovery after fighting restores damaged buildings rather than adding another administrative bill.',repair=.15,agri=.04,social=.01)
put('unity_united','Unified administration cuts duplicated offices and expands taxable enterprise.',bureau=-.06,tax=.08)
put('unity_coexist','Peaceful coexistence releases resources for civilian reconstruction without annexing the South.',civbuild=.08,social=-.04,war=-.03)
put('unity_rehabilitate','Southern recovery repairs real productive networks under actual control.',repair=.12,agri=.04)
put('unity_contact','Family contacts improve social confidence while limiting humanitarian expense.',stab=.05,social=-.03)
put('unity_citizens','A civil settlement provides stability and functioning local administration.',stab=.04,bureau=-.03)
put('unity_strict','Screened appointments strengthen the existing command network but impose real administrative costs.',pp=.12,war=.05,bureau=.03)
put('unity_amnesty','Conditional amnesty brings skilled labour back into reconstruction with political uncertainty.',civbuild=.08,mil=.05,stab=-.02)
put('unity_registry','A civil register cuts duplicated administration and improves collection without an arbitrary stability loss.',bureau=-.05,tax=.05)
put('unity_resettle','Resettlement stabilises communities and restores rural production.',stab=.05,agri=.04,social=.02)
put('unity_peace','A sustained settlement improves the division spirit and frees funds for reconstruction.',civbuild=.05,social=-.03)

# Foreign programmes remain recipient-approved and do not share unrelated locks.
put('diplomacy_root','A staffed foreign service sustains technical exchanges and cheaper procurement administration.',bureau=-.03,research=.02)
put('diplomacy_moscow','Soviet technical orientation brings an industrial research opportunity and specialist capacity.',[bonus('CAT_industry')],research=.03,bureau=.01)
put('diplomacy_balance','Diversified procurement makes restrictions less damaging and keeps supplies usable.',sanctions=.10,supply=-.04,bureau=.02)
put('diplomacy_specialists','Specialists translate imported knowledge into practical electronics research.',[bonus('CAT_electronics')],research=.02)
put('diplomacy_autonomy','An independent procurement administration builds domestic competence.',gain=.08,sanctions=.05,education=.01)
put('diplomacy_laos','Regional liaison provides useful staff experience and coordinated transport.',[xp(20)],supply=-.03)
put('diplomacy_security','A larger regional security commitment improves the deployable army.',[doctrine()],org=.06,planning=.04,supply=.03)
put('diplomacy_restraint','A restrained regional posture directs money and machinery into civilian reconstruction.',civbuild=.10,social=-.04,war=-.03)
put('diplomacy_border','Border preparation gives entrenchment and practical defensive training.',[xp(20)],core=.05,entrench=1)
put('diplomacy_confidence','Regional confidence supports commerce and administrative cooperation.',tax=.06,bureau=-.03)
put('diplomacy_isolation','Trading under restrictions improves the patron-dependence spirit and domestic resilience.',sanctions=.06)
put('diplomacy_autarky','Strategic self-reliance improves sanctions resilience and equipment production efficiency.',sanctions=.12,gain=.10,build=-.03)
put('diplomacy_opening','A controlled opening brings construction research and faster investment, with genuine market exposure.',[bonus('CAT_construction')],build=.08,research=.02,market=.06)
put('diplomacy_alternatives','Alternative suppliers reduce supply demand and improve repair capability.',supply=-.05,repair=.08)
put('diplomacy_normalise','Normalisation prepares civilian research and reduces the administrative burden of trade.',[bonus('CAT_electronics',amount=.35)],bureau=-.04,tax=.04)
put('diplomacy_transition','The bloc transition improves the patron-dependence spirit and civilian investment resilience.',civbuild=.06,bureau=-.03)

def main():
    d=json.loads((ROOT/'tools/vietnam_1970/approved_design.json').read_text(encoding='utf-8'))
    expected={n['id'] for n in d['nodes'] if n['group'] in {'state','industry','farm','army','unity','diplomacy'}}
    assert len(patches)==95 and {p['id'] for p in patches}==expected
    data=dict(schema=1,status='Implementation design requested by user',patches=patches,
        new_exclusive_sets=[[P+'state_emerging',P+'state_western']],
        rules=['One extraordinary cadre allocation funds reserve networks or provincial offices; Front participation and sovereignty remain compatible.','Food production and rations are a shared funding priority, not a claim that the other activity is illegal.','One completed Hanoi rehabilitation replaces the old later civilian building, not a free starting industry grant.','Research grants are finite, do not remove ahead-of-time penalties and do not award technologies.'],
        native_reference_profile='See prior mechanics.json 29 native references plus MD technologies/industry.txt CAT_industry, engineering.txt CAT_electronics and infantry.txt CAT_infantry_weapons; normal MD Benelux/Ukraine dynamic industry_air_damage_factor and production_factory_efficiency_gain_factor.')
    (HERE/'common.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Common nodes:',len(patches))

if __name__=='__main__':main()
