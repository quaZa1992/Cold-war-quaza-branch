# IMPERIA COLD WAR — Researched French foreign-policy and African cooperation design.
"""Emit the complete spatial design before installing its authorized extension."""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASELINE = '57b479c47dafef3d83917931994617bf08c1467d8a00175aa28da957a7518628'
P = 'COLDWAR_FRA2_'
TAG_NAMES = {'SEN':'Senegal','CAM':'Cameroon','GAB':'Gabon','NGR':'Niger','CDI':"Cote d'Ivoire",'CHA':'Chad','LBA':'Libya','EGY':'Egypt','IRQ':'Iraq','SAU':'Saudi Arabia','LEB':'Lebanon','RAJ':'India','VIE':'Vietnam','MRT':'Mauritius','DJI':'Djibouti'}


def money(kind, percent):
    fraction = Decimal(str(percent)) / 100
    return dict(kind=kind, percent=percent, gdp_fraction=float(fraction),
        runtime_share_literal=format(fraction, '.5f'), base='gdp_total', payer='own_country',
        valuation='at_payment' if kind == 'treasury_gdp' else 'weekly_recalculation',
        **({'once':True} if kind == 'treasury_gdp' else {'annual_gdp_percent':percent,'divisor':52}))


def fee(percent): return money('treasury_gdp', -abs(percent))
def weekly(percent): return money('weekly_gdp_expense', percent)
def b(state, building, amount=1):
    return dict(kind='building', state=state, building=building, amount=amount, slots=amount, slots_before_construction=True, once=True)
def r(category, bonus=.5, uses=1): return dict(kind='research', category=category, bonus=bonus, uses=uses, once=True)
def doctrine(category, reduction=.5, uses=1): return dict(kind='doctrine', category=category, reduction=reduction, uses=uses, once=True)
def m(key, value): return dict(kind='modifier', key=key, value=value)
def xp(service, amount): return dict(kind='experience', service=service, amount=amount, once=True)
def transfer(payer, recipient, percent, flow):
    return dict(kind='weekly_transfer', payer=payer, recipient=recipient, annual_gdp_percent=percent,
        gdp_fraction=float(Decimal(str(percent))/100), runtime_share_literal=format(Decimal(str(percent))/100,'.5f'),
        divisor=52, base='gdp_total', valuation='weekly_recalculation', flow=flow)
def access(tag): return dict(kind='access',grantor=tag,beneficiary='FRA',relation='military_access',lifecycle='standing_agreement')
def rights(): return dict(kind='resource_rights',grantor='NGR',beneficiary='FRA',state=329,resources=['uranium'],lifecycle='standing_agreement')


def main():
    raw = (ROOT/'tools/france_1970_runtime/runtime_design.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASELINE, 'Current tree changed. Review before replacing the pinned design.'
    baseline = json.loads(raw)
    design = deepcopy(baseline)
    plan = json.loads((HERE/'LAYOUT_PLAN.json').read_text(encoding='utf-8'))
    chapters = {c['group']:c for c in plan['chapters']}
    groups = [
        ('african_finance','African Economic Networks',16,'economic_prosperity','industrial_concern'),
        ('african_security','African Security and Development',42,'french_army','political_power_bonus'),
        ('arab_contracts','Arab Contracts and the Mediterranean',68,'french_army_navy','industrial_concern'),
        ('global_partnerships','Global Technical Partnerships',94,'francosphere','research_minstry'),
    ]
    for index,(key,title,x,icon,idea) in enumerate(groups):
        entry=chapters[key]['entry']
        design['groups'].append(dict(id=key,title=title,x=entry['x'],y=entry['y'],slot=None,trigger=None,
            context='French national policy and individually negotiated standing agreements. Partner governments retain their own authority.',
            idea_picture='COLDWAR_FRA2_idea_'+idea,focus_icon_source=icon))
    added = []
    group_map = {g['id']:g for g in design['groups']}
    def node(key,title,description,group,x,y,parent,effects,icon='francosphere',cost=7):
        is_entry = key == 'fp_'+group
        anchor = P+'diplomatic_review' if key == 'fp_foreign_service' else P+'fp_foreign_service' if is_entry else P+'fp_'+group
        ax,ay = (78,8) if key=='fp_foreign_service' else (94,9) if is_entry else (group_map[group]['x'],group_map[group]['y'])
        n = dict(id=P+key,key=key,group=group,title=title,full_title=title,description=description,
            x=x,y=y,anchor=anchor,offset=[x-ax,y-ay],cost=cost,days=cost*7,
            prerequisites=[[parent]],exclusions=[],conditions=[],reward_guards=[],effects=effects,
            spirit=P+group+'_programme',spirit_name=group_map[group]['title']+' Programme',
            modifier_pool=group,icon='COLDWAR_FRA2_focus_'+icon,icon_source=icon,foreign_policy_change='new',
            historical_basis='tools/france_1970_foreign_policy/HISTORY_AFRICA.md; HISTORY_GLOBAL.md',
            md_reference='MD France francosphere; UK-Egypt acceptance contract; Russia native numeric programme rewards')
        added.append(n);return n
    node('fp_foreign_service','Foreign Commercial Service',
        'Reinforce the Quai d\'Orsay and commercial missions with a Paris service office. Contracts, technical missions and overseas commitments require permanent administrative staff as well as diplomatic ambition.',
        'diplomacy',94,9,'diplomatic_review',[fee(.20),b(56,'offices'),m('bureaucracy_cost_multiplier_modifier',.02)],'francosphere')
    entry_data = [
        ('african_finance','African Credit Office','Equip a Marseille financing office to service African investment and monetary cooperation. French firms gain a practical base for contracts, while public guarantees expose the budget to partner-country risks.',[fee(.18),b(63,'offices'),r('CAT_industry',.25),m('corporate_tax_income_multiplier_modifier',-.01)]),
        ('african_security','Cooperation Missions','Expand a Loire training and liaison office for overseas missions. Professional instruction and medical, transport and maintenance arrangements must accompany any promise of French support.',[fee(.18),b(59,'offices'),doctrine('land_doctrine',.25),m('army_personnel_cost_multiplier_modifier',.02)]),
        ('arab_contracts','Export Support Office','Concentrate aircraft, naval and engineering support in Provence. French exports depend on technicians and long support commitments, rather than a signature followed by an effortless windfall.',[fee(.25),b(63,'industrial_complex'),r('CAT_electronics',.25),m('equipment_cost_multiplier_modifier',.02)]),
        ('global_partnerships','Technical Missions','Build a Bourgogne office for scholarships, engineering and technical missions beyond the former empire. French technical cooperation must serve enduring institutions and practical skills while reaching governments outside the French-speaking world.',[fee(.18),b(58,'offices'),r('CAT_infrastructure',.25),m('education_cost_multiplier_modifier',.02)]),
    ]
    for g,title,desc,effects in entry_data:
        node('fp_'+g,title,desc,g,group_map[g]['x'],group_map[g]['y'],'fp_foreign_service',effects,group_map[g]['focus_icon_source'])

    def offer(key,title,description,group,tag,fr,other,setup=(.25,.15),operating=(.001,.02),flow=None,extra=None,icon='francosphere'):
        n = dict(key=key,title=title,description=description,group=group,tag=tag,fr=fr,other=other,
                 setup=setup,operating=operating,flow=flow,extra=extra or [],icon=icon)
        return n
    pairs = []
    def pair(group, a, z): pairs.append((group,a,z))
    g='african_finance'
    pair(g,
        offer('fp_senegal_clearing','Dakar Clearing Services','Offer Dakar French-backed clearing and banking services on privileged commercial terms. Senegal receives practical financial capacity, while contracted service fees and tax concessions favour the French providers.',g,'SEN',
            [b(56,'offices'),r('CAT_electronics',.5),m('bureaucracy_cost_multiplier_modifier',.02)],
            [b(364,'offices'),r('CAT_industry',.5),m('corporate_tax_income_multiplier_modifier',-.03)],flow=('SEN','FRA',.20)),
        offer('fp_senegal_boards','African Banking Boards','Support greater African control of monetary administration through local boards and technical training. French banking services and investment-goods suppliers expand alongside Senegalese institutions, with a larger continuing French contribution.',g,'SEN',
            [b(58,'offices'),b(60,'industrial_complex'),r('CAT_electronics',.5,2),m('education_cost_multiplier_modifier',.03)],
            [b(364,'offices',2),r('CAT_industry',.5,2),m('bureaucracy_cost_multiplier_modifier',.03)],setup=(.35,.15),flow=('FRA','SEN',.015)))
    pair(g,
        offer('fp_cameroon_guarantee','Central Franc Services','Negotiate a French-backed settlement-service programme with Cameroon. The guarantee supports local institutions, while fees, reporting requirements and French technical personnel preserve a privileged commercial relationship.',g,'CAM',
            [b(56,'offices'),r('CAT_industry',.5),m('bureaucracy_cost_multiplier_modifier',.02)],
            [b(321,'offices'),r('CAT_electronics',.5),m('corporate_tax_income_multiplier_modifier',-.03)],flow=('CAM','FRA',.20)),
        offer('fp_cameroon_treasury','African Treasury Seats','Finance treasury training and local financial offices while conceding more management authority to Cameroon. French equipment suppliers and technical services expand, but Paris accepts larger financing obligations and less direct fee income.',g,'CAM',
            [b(57,'offices'),b(59,'industrial_complex'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.03)],
            [b(321,'offices',2),r('CAT_electronics',.5,2),m('bureaucracy_cost_multiplier_modifier',.03)],setup=(.35,.15),flow=('FRA','CAM',.015)))
    pair(g,
        offer('fp_gabon_elf','Gabon Oil Services','Offer an Elf-style petroleum services and investment settlement. Gabon receives transport works and technical assistance, while fees support French contractors and concessions reduce the host treasury\'s share of the returns.',g,'GAB',
            [b(55,'industrial_complex'),r('CAT_energy',.5),m('equipment_cost_multiplier_modifier',.02)],
            [b(317,'infrastructure'),r('CAT_energy',.5),m('oil_export_multiplier_modifier',.08),m('corporate_tax_income_multiplier_modifier',-.04)],flow=('GAB','FRA',.25),icon='powerplant'),
        offer('fp_gabon_processing','Gabon Processing Compact','Prioritise processing and local industrial skills rather than a narrower extractive relationship. French engineering orders expand, but France funds more of the programme and Gabon bears the cost of training a larger industrial workforce.',g,'GAB',
            [b(60,'industrial_complex'),r('CAT_industry',.5,2),m('corporate_tax_income_multiplier_modifier',-.02)],
            [b(317,'industrial_complex',2),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.05)],setup=(.50,.25),flow=('FRA','GAB',.02),icon='economic_prosperity'))
    pair(g,
        offer('fp_niger_rights','Uranium Investment Rights','Propose French financing and access to investment in Niger\'s surveyed uranium districts, following the SOMAIR precedent. Niger retains sovereignty and receives transport support; France receives negotiated uranium rights, while actual mine development remains a separate paid investment.',g,'NGR',
            [r('CAT_nuclear_reactors',.5,2),rights(),m('equipment_cost_multiplier_modifier',.02)],
            [b(329,'infrastructure'),r('CAT_industry',.5),rights(),m('corporate_tax_income_multiplier_modifier',-.03)],setup=(.30,.10),flow=('FRA','NGR',.02),icon='nuclear_energy'),
        offer('fp_niger_processing','Niger Processing Charter','Leave uranium investment rights with Niger and support local processing and technical institutions. French firms gain engineering work and research experience, while a larger French contribution finances the host\'s industrial ambitions.',g,'NGR',
            [b(58,'offices'),b(60,'industrial_complex'),r('CAT_nuclear_reactors',.5,2),m('education_cost_multiplier_modifier',.03)],
            [b(329,'industrial_complex'),b(329,'infrastructure'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.45,.15),flow=('FRA','NGR',.03),icon='nuclear_energy'))

    g='african_security'
    pair(g,
        offer('fp_abidjan_transit','Abidjan Transit Mission','Negotiate land and air transit through Cote d\'Ivoire, supported by local transport works and French payments. Actual host-approved access improves deployment options, while French personnel and equipment support become continuing obligations.',g,'CDI',
            [access('CDI'),xp('army',20),m('supply_consumption_factor',-.03),m('army_personnel_cost_multiplier_modifier',.03)],
            [access('CDI'),b(352,'infrastructure'),doctrine('land_doctrine',.5),m('army_org_factor',.04),m('equipment_cost_multiplier_modifier',.03)],setup=(.25,.15),flow=('FRA','CDI',.015),icon='french_army'),
        offer('fp_abidjan_port','Abidjan Commercial Port','Support repair, cargo and logistics services on a commercial basis without a French military access term. Ivorian maritime capacity expands and French yards receive work, while the two governments finance training and administration.',g,'CDI',
            [b(64,'dockyard'),r('CAT_naval',.5),m('navy_personnel_cost_multiplier_modifier',.03)],
            [b(352,'dockyard'),b(352,'offices'),r('CAT_naval',.5),m('education_cost_multiplier_modifier',.04)],setup=(.40,.25),flow=('FRA','CDI',.02),icon='french_army_navy'))
    pair(g,
        offer('fp_libreville_station','Libreville Station','Negotiate a supported French ground and air presence at Libreville. Gabon receives infrastructure, instruction and regular funding, while France gains access and operational experience at the cost of an enduring deployment budget.',g,'GAB',
            [access('GAB'),xp('army',25),m('army_org_regain',.03),m('army_personnel_cost_multiplier_modifier',.04)],
            [access('GAB'),b(317,'infrastructure'),doctrine('land_doctrine',.5),m('army_org_factor',.04),m('equipment_cost_multiplier_modifier',.03)],setup=(.30,.15),flow=('FRA','GAB',.02),icon='french_army'),
        offer('fp_gabon_officers','Gabon Officer Schools','Replace a basing priority with stronger Gabonese military institutions. Local workshops and officer training offer a different form of security cooperation, while French advisers remain responsible for a sustained instructional commitment.',g,'GAB',
            [doctrine('land_doctrine',.5,2),r('CAT_armor',.5),m('training_time_army_factor',.04)],
            [b(317,'arms_factory'),b(317,'offices'),doctrine('land_doctrine',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.40,.20),flow=('FRA','GAB',.02),icon='french_specialists'))
    pair(g,
        offer('fp_chad_airlift','Chadian Airlift Mission','Offer an airfield and advisory arrangement informed by the repeated French interventions in Chad. The host authorises access and receives funded support; France gains expeditionary experience while committing aircraft crews and logistics capacity.',g,'CHA',
            [access('CHA'),xp('air',25),doctrine('air_doctrine',.5),m('supply_consumption_factor',-.03),m('airforce_personnel_cost_multiplier_modifier',.05)],
            [access('CHA'),b(328,'air_base'),doctrine('land_doctrine',.5),m('army_org_factor',.05),m('equipment_cost_multiplier_modifier',.04)],setup=(.35,.10),flow=('FRA','CHA',.025),icon='french_army_air'),
        offer('fp_chad_cadres','Chadian National Cadres','Prioritise local maintenance and military training without a French transit entitlement. Chad develops a stronger domestic force, while France funds the instruction and diverts officers from its own training system.',g,'CHA',
            [r('CAT_armor',.5),doctrine('land_doctrine',.5),m('army_org_factor',.03),m('training_time_army_factor',.04)],
            [b(328,'arms_factory'),doctrine('land_doctrine',.5,2),m('training_time_army_factor',-.05),m('education_cost_multiplier_modifier',.04)],setup=(.35,.15),flow=('FRA','CHA',.025),icon='french_specialists'))
    pair(g,
        offer('fp_niger_field_services','Sahel Field Services','Support Nigerien patrol, transport and maintenance services in the difficult Sahelian environment. French instructors learn alongside their partners, but specialist support and local army upkeep carry continuing costs.',g,'NGR',
            [xp('army',20),doctrine('land_doctrine',.5),m('supply_consumption_factor',-.02),m('army_personnel_cost_multiplier_modifier',.03)],
            [b(331,'offices'),b(331,'infrastructure'),doctrine('land_doctrine',.5),m('army_org_regain',.04),m('equipment_cost_multiplier_modifier',.03)],setup=(.30,.10),flow=('FRA','NGR',.02),icon='french_army'),
        offer('fp_niger_rural','Sahel Rural Compact','Fund rural access and agricultural extension rather than expanding a military support network. Niger receives productive facilities and practical training, while French agricultural equipment firms benefit from a larger development commitment.',g,'NGR',
            [b(59,'industrial_complex'),r('CAT_industry',.5),m('corporate_tax_income_multiplier_modifier',-.02)],
            [b(331,'agriculture_district',2),b(331,'infrastructure'),r('CAT_industry',.5,2),m('social_cost_multiplier_modifier',.04)],setup=(.45,.15),flow=('FRA','NGR',.025),icon='FRA_ruralism'))

    g='arab_contracts'
    pair(g,
        offer('fp_libya_aviation','Libyan Aviation Contract','Pursue the aviation export market opened by the 1970 Mirage agreement. A funded support package builds French production and Libyan training capacity, while France accepts maintenance obligations and Libya pays recurring service charges.',g,'LBA',
            [b(55,'arms_factory'),r('CAT_aircraft',.5),m('airforce_personnel_cost_multiplier_modifier',.04)],
            [b(391,'air_base'),r('CAT_aircraft',.5,2),doctrine('air_doctrine',.5),m('airforce_personnel_cost_multiplier_modifier',.05)],setup=(.45,.60),flow=('LBA','FRA',.25),operating=(.008,.03),icon='FRA_air_fighter'),
        offer('fp_egypt_aviation','Egyptian Air Support','Make Egypt the priority aviation support market instead. Cairo gains technical and operational training, while French manufacturers expand the support base and accept a smaller fee stream in exchange for the long-term relationship.',g,'EGY',
            [b(60,'industrial_complex'),r('CAT_aircraft',.5,2),m('education_cost_multiplier_modifier',.04)],
            [b(216,'air_base'),r('CAT_aircraft',.5,2),doctrine('air_doctrine',.5),m('equipment_cost_multiplier_modifier',.04)],setup=(.40,.35),flow=('EGY','FRA',.12),operating=(.008,.03),icon='FRA_airforce'))
    pair(g,
        offer('fp_iraq_energy','Iraqi Energy Services','Offer hydrocarbon engineering and field-service cooperation on the basis of the 1972 agreement. Iraqi export earnings and local transport capacity improve, while French contractors receive service payments and undertake technical support obligations.',g,'IRQ',
            [b(63,'offices'),r('CAT_energy',.5,2),m('equipment_cost_multiplier_modifier',.03)],
            [b(171,'infrastructure'),r('CAT_energy',.5),m('oil_export_multiplier_modifier',.08),m('corporate_tax_income_multiplier_modifier',-.03)],setup=(.35,.35),flow=('IRQ','FRA',.20),operating=(.006,.03),icon='powerplant'),
        offer('fp_iraq_industry','Iraqi Industrial Localisation','Emphasise the economic, technical and computing cooperation developed in the mid-1970s. Iraq obtains more local productive capacity, while French engineering firms gain research and orders but accept greater public financing and training costs.',g,'IRQ',
            [b(57,'industrial_complex'),r('CAT_electronics',.5,2),m('education_cost_multiplier_modifier',.04)],
            [b(557,'industrial_complex'),b(557,'offices'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.50,.35),flow=('FRA','IRQ',.01),icon='economic_prosperity'))
    pair(g,
        offer('fp_saudi_naval','Sawari Support Package','Negotiate an integrated Saudi naval-support programme with repair facilities and technical training. French yards and sensor specialists gain sustained orders, while Saudi Arabia develops local capabilities with long-term service charges.',g,'SAU',
            [b(64,'dockyard'),r('CAT_naval',.5,2),m('navy_personnel_cost_multiplier_modifier',.04)],
            [b(177,'dockyard'),r('CAT_naval',.5,2),doctrine('naval_doctrine',.5),m('equipment_cost_multiplier_modifier',.05)],setup=(.50,.75),flow=('SAU','FRA',.30),operating=(.008,.04),icon='FRA_navy'),
        offer('fp_saudi_civil','Saudi Civil Engineering','Pursue a larger civilian engineering market instead of the naval-support priority. French firms gain industrial orders and Saudi Arabia develops domestic facilities, while specialist training and public commercial support absorb resources.',g,'SAU',
            [b(60,'industrial_complex'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.03)],
            [b(176,'industrial_complex'),b(176,'infrastructure'),r('CAT_infrastructure',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.45,.60),flow=('SAU','FRA',.15),operating=(.005,.03),icon='economic_prosperity'))
    pair(g,
        offer('fp_lebanon_field','Beirut Field Mission','Offer the Lebanese government a French engineering and military liaison presence under agreed stationing conditions. Local services and training support the host institutions, while French troops and specialists undertake a difficult overseas commitment.',g,'LEB',
            [access('LEB'),xp('army',20),doctrine('land_doctrine',.5),m('army_org_regain',.03),m('army_personnel_cost_multiplier_modifier',.04)],
            [access('LEB'),b(202,'offices'),doctrine('land_doctrine',.5),m('army_org_factor',.04),m('bureaucracy_cost_multiplier_modifier',.03)],setup=(.30,.10),flow=('FRA','LEB',.02),icon='french_army'),
        offer('fp_lebanon_recovery','Lebanese Recovery Works','Concentrate French support on civilian engineering and services without a military access term. Lebanese capacity and French reconstruction experience expand, while the programme carries training costs and substantial continuing aid.',g,'LEB',
            [b(63,'offices'),r('CAT_infrastructure',.5,2),m('corporate_tax_income_multiplier_modifier',-.02)],
            [b(202,'industrial_complex'),b(202,'infrastructure'),r('CAT_infrastructure',.5,2),m('social_cost_multiplier_modifier',.04)],setup=(.45,.20),flow=('FRA','LEB',.025),icon='economic_roads_new'))

    g='global_partnerships'
    pair(g,
        offer('fp_india_aviation','Indian Aviation Orders','Develop an Indian aviation and technical-support market with local workshops and specialist training. Industrial support creates practical capabilities, while service charges and French personnel commitments bind both sides to a demanding relationship.',g,'RAJ',
            [b(55,'arms_factory'),r('CAT_aircraft',.5,2),m('airforce_personnel_cost_multiplier_modifier',.04)],
            [b(431,'arms_factory'),r('CAT_aircraft',.5,2),doctrine('air_doctrine',.5),m('equipment_cost_multiplier_modifier',.04)],setup=(.50,.35),flow=('RAJ','FRA',.10),operating=(.008,.03),icon='FRA_air_fighter'),
        offer('fp_india_power','Indian Power Engineering','Offer civilian power engineering and industrial training rather than a French aviation-market priority. India retains its own procurement choices, while both countries invest in productive capacity and the skills needed to operate it.',g,'RAJ',
            [b(57,'industrial_complex'),r('CAT_energy',.5,2),m('education_cost_multiplier_modifier',.03)],
            [b(431,'industrial_complex'),r('CAT_energy',.5,2),r('CAT_industry',.5),m('education_cost_multiplier_modifier',.04)],setup=(.45,.35),flow=('RAJ','FRA',.05),operating=(.006,.03),icon='powerplant'))
    pair(g,
        offer('fp_vietnam_engineering','Vietnam Engineering Accord','Offer a civilian engineering programme centred on productive works, maintenance and technical training. Vietnam retains its own development priorities, while French firms and institutes gain experience at the cost of sustained aid and expert missions.',g,'VIE',
            [b(58,'offices'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.04)],
            [b(522,'industrial_complex'),b(522,'infrastructure'),r('CAT_industry',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.40,.15),flow=('FRA','VIE',.02),icon='economic_prosperity'),
        offer('fp_vietnam_health','Vietnam Medical Institutes','Prioritise medical administration, prevention and technical training rather than a larger industrial programme. Vietnam gains useful local services and France develops medical-equipment expertise, with a lasting burden of grants and expert missions.',g,'VIE',
            [b(56,'offices'),r('CAT_electronics',.5,2),m('health_cost_multiplier_modifier',-.02),m('education_cost_multiplier_modifier',.04)],
            [b(522,'offices',2),m('health_cost_multiplier_modifier',-.06),m('bureaucracy_cost_multiplier_modifier',.03)],setup=(.35,.10),flow=('FRA','VIE',.02),icon='french_specialists'))
    pair(g,
        offer('fp_mauritius_agriculture','Mauritius Rural Services','Develop the agricultural, irrigation and technical cooperation agreed with Mauritius in 1970. Productive island facilities and French equipment orders expand, while field services and farm support require continuing public expenditure.',g,'MRT',
            [b(59,'industrial_complex'),r('CAT_industry',.5),m('corporate_tax_income_multiplier_modifier',-.02)],
            [b(270,'agriculture_district',2),b(270,'infrastructure'),r('CAT_industry',.5,2),m('social_cost_multiplier_modifier',.04)],setup=(.35,.10),flow=('FRA','MRT',.015),icon='FRA_ruralism'),
        offer('fp_mauritius_marine','Mauritius Marine Services','Redirect cooperation towards island maritime services, technical training and repair. Local facilities and French shipbuilding orders support a commercial partnership, while dispersed island operations require trained staff and continuing public support.',g,'MRT',
            [b(64,'dockyard'),r('CAT_naval',.5),m('navy_personnel_cost_multiplier_modifier',.03)],
            [b(270,'dockyard'),b(270,'offices'),r('CAT_naval',.5,2),m('education_cost_multiplier_modifier',.04)],setup=(.40,.15),flow=('FRA','MRT',.015),icon='FRA_navy'))
    independent_dji = ['DJI = { is_subject = no owns_state = 230 controls_state = 230 has_full_control_of_state = 230 }']
    pair(g,
        offer('fp_djibouti_defence','Djibouti Defence Protocol','Once Djibouti is sovereign, negotiate stationing conditions and a military cooperation protocol. The host authorises French land and air access and receives funding and facilities, while France accepts a permanent personnel commitment.',g,'DJI',
            [access('DJI'),xp('air',20),doctrine('air_doctrine',.5),m('supply_consumption_factor',-.03),m('army_personnel_cost_multiplier_modifier',.04)],
            [access('DJI'),b(230,'air_base'),b(230,'infrastructure'),doctrine('land_doctrine',.5),m('army_org_factor',.04),m('equipment_cost_multiplier_modifier',.03)],setup=(.35,.10),flow=('FRA','DJI',.025),extra=independent_dji,icon='french_army_air'),
        offer('fp_djibouti_civil','Djibouti Civil Compact','Offer a sovereign Djibouti civilian services and technical training instead of a French military access term. Local productive capacity expands and French civilian missions gain experience, while grants and expert staffing create an enduring fiscal obligation.',g,'DJI',
            [b(63,'offices'),r('CAT_infrastructure',.5,2),m('education_cost_multiplier_modifier',.04)],
            [b(230,'offices'),b(230,'industrial_complex'),r('CAT_industry',.5,2),m('bureaucracy_cost_multiplier_modifier',.03)],setup=(.40,.15),flow=('FRA','DJI',.025),extra=independent_dji,icon='francosphere'))

    pair_index = {g[0]:0 for g in groups}
    for group,a,z in pairs:
        slot = pair_index[group];pair_index[group] += 1
        coords = chapters[group]['offer_pairs'][slot]['coordinates']
        for spec, (x,y), other in ((a,coords[0],z),(z,coords[1],a)):
            key,tag=spec['key'],spec['tag']
            n=node(key,spec['title'],spec['description'],group,x,y,'fp_'+group,[],spec['icon'])
            n['exclusions']=[other['key']]
            n['effects']=[dict(kind='unlock_decision',decision=P+'accept_'+key)]
            n['spirit']=None;n['spirit_name']=None
            sides={}
            for side,payer,terms,setup,op in (
                ('france','FRA',spec['fr'],spec['setup'][0],spec['operating'][0]),
                ('recipient',tag,spec['other'],spec['setup'][1],spec['operating'][1])):
                eff=[fee(setup),weekly(op),*deepcopy(terms)]
                if spec['flow']:
                    pay,receive,percent=spec['flow']
                    eff.append(transfer(pay,receive,percent,'expense' if payer==pay else 'income'))
                sides[side]=dict(spirit=P+key+('_france' if side=='france' else '_'+tag),
                    name=spec['title']+': '+('France' if side=='france' else TAG_NAMES[tag]),effects=eff,payer=payer,
                    picture='COLDWAR_FRA2_idea_industrial_concern')
            n['offer']=dict(partner=tag,partner_name=TAG_NAMES[tag],family='fp_'+group+'_'+str(slot),
                **sides,activation_conditions=spec['extra'],source_focus=n['id'],
                historical_basis=n['historical_basis'],delivery='recipient_acceptance_decision',
                suspension='Both exist, bilateral peace, no embargo or any mirrored Imperia sanction. Parent and granted-right territory conditions remain real.',
                no_expiry=True)
            if key=='fp_niger_rights':
                n['conditions'].append('NOT = { FRA = { has_resources_rights = { state = 329 } } }')
                n['offer']['activation_conditions'] += ['NGR = { owns_state = 329 controls_state = 329 has_full_control_of_state = 329 }','329 = { check_variable = { imp_uranium_deposit_kt > 0 } }']
    short_titles = {
        'fp_foreign_service':'Foreign Trade', 'fp_african_finance':'African Credit Office',
        'fp_african_security':'Cooperation Missions', 'fp_arab_contracts':'Export Support Office',
        'fp_senegal_clearing':'Dakar Clearing', 'fp_senegal_boards':'African Bank Boards',
        'fp_cameroon_guarantee':'Franc Zone Services', 'fp_cameroon_treasury':'African Treasuries',
        'fp_gabon_processing':'Gabon Processing', 'fp_niger_rights':'Uranium Concession',
        'fp_niger_processing':'Niger Processing', 'fp_abidjan_transit':'Abidjan Transit',
        'fp_abidjan_port':'Abidjan Port', 'fp_gabon_officers':'Gabon Officers',
        'fp_chad_airlift':'Chadian Airlift', 'fp_chad_cadres':'Chadian Cadres',
        'fp_niger_field_services':'Sahel Field Teams', 'fp_libya_aviation':'Libyan Air Contract',
        'fp_iraq_energy':'Iraqi Energy Work', 'fp_iraq_industry':'Iraqi Local Industry',
        'fp_saudi_naval':'Sawari Support', 'fp_saudi_civil':'Saudi Civil Works',
        'fp_lebanon_recovery':'Lebanese Recovery', 'fp_india_aviation':'Indian Air Orders',
        'fp_india_power':'Indian Power Works', 'fp_vietnam_engineering':'Vietnam Engineering',
        'fp_vietnam_health':'Vietnam Medicine', 'fp_mauritius_agriculture':'Mauritius Rural Aid',
        'fp_mauritius_marine':'Mauritius Marine', 'fp_djibouti_defence':'Djibouti Defence',
        'fp_djibouti_civil':'Djibouti Civil Pact',
    }
    for n in added:
        n['title'] = short_titles.get(n['key'], n['title'])
    assert len(added)==37 and sum('offer' in n for n in added)==32
    assert len({n['key'] for n in added})==37
    design['nodes'].extend(added)
    design['project']='IMPERIA COLD WAR'
    design['status']='RESEARCHED SPATIAL DESIGN. Implementation authorized in the same request; no extra approval checkpoint.'
    design['foreign_policy_baseline_sha256']=BASELINE
    design['foreign_policy_added_keys']=[n['key'] for n in added]
    design['foreign_policy_new_groups']=[g[0] for g in groups]
    design['foreign_policy_source_records']=['HISTORY_AFRICA.md','HISTORY_GLOBAL.md','MECHANICS.md','LAYOUT_PLAN.json']
    out=json.dumps(design,ensure_ascii=False,indent=2)+'\n'
    (HERE/'foreign_policy_design.json').write_bytes(out.encode('utf-8'))
    (HERE/'ADDITIONS.json').write_bytes((json.dumps(dict(project='IMPERIA COLD WAR',baseline_sha256=BASELINE,
        added_groups=design['groups'][-4:],added_focuses=added),ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(dict(project='IMPERIA COLD WAR',new_focuses=37,new_offers=32,total_focuses=len(design['nodes']),
        total_offers=sum('offer' in n for n in design['nodes']),sha256=hashlib.sha256(out.encode()).hexdigest()),indent=2))


if __name__=='__main__':main()
