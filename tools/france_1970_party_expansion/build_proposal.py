# IMPERIA COLD WAR — France additional party programmes, design only.
"""Freeze the installed design and emit an uninstalled 20-focus proposal."""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'tools/france_1970_runtime/runtime_design.json'
EXPECTED = '00d5e2721934ad527360ce0265f1213e345a1df8b0f1999c22599f23199dbbe9'
STATE_NAMES={54:'Hauts-de-France',55:'Normandie',56:'Ile-de-France',57:'Alsace-Lorraine',58:'Bourgogne',59:'Loire',60:'Aquitaine',61:'Midi-Pyrenees',62:'Rhone-Alpes',63:'Provence',64:'Bretagne',959:'Pays de la Loire',962:'Auvergne'}
CAPS={'industrial_complex':50,'offices':50,'infrastructure':6,'agriculture_district':10,'arms_factory':35,'fossil_powerplant':20}


def fee(percent):
    value = -Decimal(str(percent)) / 100
    return dict(kind='treasury_gdp', percent=-percent, gdp_fraction=float(value),
                runtime_share_literal=format(value,'.5f'),base='gdp_total',payer='own_country',valuation='at_payment',once=True)


def building(state, kind):
    return dict(kind='building',state=state,building=kind,amount=1,slots=1,slots_before_construction=True,once=True)


def slots(state, amount):
    return dict(kind='state_slots',state=state,amount=amount,once=True,
                native_effect='add_extra_state_shared_building_slots')


def mod(key, value): return dict(kind='modifier',key=key,value=value)
def study(category, bonus=.5, uses=1): return dict(kind='research',category=category,bonus=bonus,uses=uses,once=True)
def opinion(faction,value): return dict(kind='faction_opinion',faction=faction,value=value,provider='change_'+faction+'_opinion',parameter='temp_opinion',once=True)


def build():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED, 'Installed baseline changed; review it before updating this proposal.'
    baseline = json.loads(raw)
    design = deepcopy(baseline)
    bykey = {n['key']:n for n in design['nodes']}
    groups = {g['id']:g for g in design['groups']}
    added = []
    focus_changes=[]
    for key in ('cid_tax','cid_cooperatives'):
        old=deepcopy(bykey[key])
        bykey[key].update(modifier_pool='CID',spirit='COLDWAR_FRA2_CID_programme',spirit_name='CID Programme',
            programme_activation_conditions=['nationalist_right_wing_populists_are_in_power = yes','date < 1972.10.5'])
        focus_changes.append(dict(before=old,after=deepcopy(bykey[key]),reason='CID programme modifiers end when its dated identity is replaced; assets and earned values do not replay.'))

    def add(key,group,title,x,y,parents,effects,description,icon,precedent,days=49,phase=None):
        g = groups[group]
        entry = next(n for n in baseline['nodes'] if n['group']==group and not n.get('anchor'))
        if phase == 'cid': entry = bykey['cid_tax']
        if phase == 'fn': entry = bykey['fn_state']
        conditions = [g['trigger']+' = yes']
        if phase == 'cid': conditions.append('CID dated identity; before 5 October 1972')
        if phase == 'fn': conditions.append('FN identity')
        n = dict(id='COLDWAR_FRA2_'+key,key=key,group=group,title=title,full_title=title,
            x=x,y=y,anchor=entry['id'],offset=[x-entry['x'],y-entry['y']],cost=days/7,days=days,
            prerequisites=parents,exclusions=[],conditions=conditions,reward_guards=deepcopy(conditions),
            effects=effects,description=description,icon='COLDWAR_FRA2_focus_'+icon,icon_source=icon,
            lifetime='government',spirit='COLDWAR_FRA2_'+group+'_programme',spirit_name=g['title']+' Programme',
            proposal_change='new',expansion_change='new',historical_status='Counterfactual governing programme grounded in documented institutions.',
            historical_precedent=precedent,md_reference='Verified MD palette and comparable focus bundles in MECHANICS.md',
            transaction='Charge own current GDP once after exact party, state ownership/control and native capacity checks. Grant slots before buildings. Never replay finite awards on party return.')
        if phase == 'cid':
            n['spirit']='COLDWAR_FRA2_CID_programme'
            n['spirit_name']='CID Programme'
            n['modifier_pool']='CID'
            n['programme_activation_conditions']=[g['trigger']+' = yes','date < 1972.10.5']
        n['reward_guards'] += ['COLDWAR_FRA2_is_1970 = yes','NOT = { has_country_flag = COLDWAR_FRA2_earned_'+key+' }','check_variable = { gdp_total > 0 }']
        n['asset_requirements']=[]
        for state in sorted({e['state'] for e in effects if e['kind'] in ('building','state_slots')}):
            n['reward_guards'] += [f'owns_state = {state}',f'controls_state = {state}',f'has_full_control_of_state = {state}']
            n['asset_requirements'].append(f'France must own and fully control {STATE_NAMES[state]} (state {state}).')
        for e in effects:
            if e['kind']=='building':
                cap=CAPS[e['building']]
                n['reward_guards'].append(f'{e["state"]} = {{ check_variable = {{ var = building_level@{e["building"]} value = {cap-e["amount"]} compare = less_than_or_equals }} }}')
                n['asset_requirements'].append(f'{e["building"].replace("_"," ").title()} in {STATE_NAMES[e["state"]]} is below level {cap}.')
        bykey[key]=n;design['nodes'].append(n);added.append(n)
        return n

    def exclude(a,b):
        bykey[a]['exclusions'].append(b);bykey[b]['exclusions'].append(a)

    add('ri_sme_capital','ri','SME Risk Capital',27,5,[['atlantic_liberal','europe_liberal']],
        [fee(.50),building(60,'industrial_complex'),building(58,'offices'),study('CAT_industry',.5,2),mod('corporate_tax_income_multiplier_modifier',-.03)],
        'Direct long-term credit toward independent suppliers in Aquitaine and a business-support office in Bourgogne. Smaller firms gain productive capacity and technical advice, while public guarantees and tax concessions reduce the revenue retained by the state.',
        'economic_prosperity','SME capital shortages and equipment credit: Senate 1961 report; COFACE and FDES institutional precedents.')
    add('ri_export_finance','ri','Export Finance',31,5,[['atlantic_liberal','europe_liberal']],
        [fee(.40),building(56,'offices'),building(63,'offices'),study('CAT_electronics',.25),mod('corporate_tax_income_multiplier_modifier',.04),mod('education_cost_multiplier_modifier',.04)],
        'Concentrate commercial finance and export certification in the Paris region and Provence. Stronger international business can broaden taxable returns, but maintaining specialised financial and technical staff raises the education bill.',
        'economic_prosperity','COFACE export-credit institutions and commercial certification; alternative allocation of scarce guarantee capital.')
    exclude('ri_sme_capital','ri_export_finance')

    add('centre_family_services','centre','Family Services',37,5,[['centrist_covenant']],
        [fee(.40),building(58,'offices'),building(61,'infrastructure'),opinion('labour_unions',5),mod('social_cost_multiplier_modifier',.04)],
        'Co-finance family-service offices in Bourgogne and local access works in Midi-Pyrenees. Practical childcare and neighbourhood provision strengthen the social-market settlement, while service staffing requires continuing public expenditure.',
        'FRA_christian_socialism','Lecanuet family-service proposals in 1965 and CD municipal/regional proposals in July 1970.')
    add('centre_mutual_districts','centre','Mutual Districts',41,5,[['centrist_covenant']],
        [fee(.35),building(62,'offices'),mod('health_cost_multiplier_modifier',-.04),mod('corporate_tax_income_multiplier_modifier',-.03)],
        'Organise local mutual-insurance administration around a Rhone-Alpes service office. Coordinated purchasing and claims can lower health expenditure, at the cost of tax concessions supporting the participating schemes.',
        'FRA_christian_socialism','Christian-democratic social insurance and regional mutual administration. A proposed governing settlement, not an enacted 1970 entitlement.')
    exclude('centre_family_services','centre_mutual_districts')

    add('radical_civic_service','radical','Civil Service Trials',47,4,[['municipal_france','europe_technology']],
        [fee(.40),building(59,'offices'),building(962,'infrastructure'),study('CAT_infrastructure',.25),mod('training_time_army_factor',.06)],
        'Pilot civilian technical service through a Loire office and public works in Auvergne. Young participants gain practical skills outside the barracks, while a smaller pool of continuously trained recruits lengthens army training.',
        'french_democracy','The contested 1970 Radical Manifesto proposed civilian service and changes to education and workplace authority.')
    add('radical_open_orders','radical','Open Public Orders',51,4,[['municipal_france','europe_technology']],
        [fee(.45),building(60,'industrial_complex'),study('CAT_industry',.5,2),opinion('industrial_conglomerates',-5),mod('corporate_tax_income_multiplier_modifier',-.03)],
        'Open public procurement to new producers rather than reserve orders for established groups. An Aquitaine production site and technical studies widen the supplier base, while incumbents resist and concessions reduce corporate-tax receipts.',
        'industry_military','Radical Manifesto debate over subsidies, individual initiative and enterprise access in 1970.')
    exclude('radical_civic_service','radical_open_orders')

    add('ps_basin_conversion','ps','Basin Conversion',57,6,[['public_banks','social_contract_ps']],
        [fee(.65),building(54,'industrial_complex'),building(55,'infrastructure'),study('CAT_industry',.25),mod('social_cost_multiplier_modifier',.04)],
        'Rebuild productive capacity in Hauts-de-France and improve connecting infrastructure in Normandie. Industrial conversion offers tangible employment sites, while retraining and transitional support enlarge the social budget.',
        'industry_military','Public investment, industrial restructuring and decentralised implementation in Socialist programmes of the 1970s and 1980s.')
    add('ps_workplace_charters','ps','Workplace Charters',61,6,[['public_banks','social_contract_ps']],
        [fee(.50),building(62,'offices'),building(57,'offices'),mod('health_cost_multiplier_modifier',-.03),mod('production_speed_industrial_complex_factor',-.05)],
        'Equip workplace-information and prevention services in Rhone-Alpes and Alsace-Lorraine. Stronger consultation can reduce health costs, but compulsory review gives investment decisions a longer timetable.',
        'french_union','Workplace freedoms, consultation and bargaining: the 1982 Auroux laws provide a later precedent. Earlier enactment is counterfactual.')
    exclude('ps_basin_conversion','ps_workplace_charters')
    add('ps_conversion_boards','ps','Conversion Boards',59,7,[['ps_basin_conversion','ps_workplace_charters']],
        [fee(.08),slots(54,2),study('CAT_industry',.25),dict(kind='unlock_decision',id='COLDWAR_FRA2P_regional_conversion',label='Regional Conversion Fund')],
        'Authorise regional boards to commission an industrial-renewal project. Prepared sites and technical studies support the Regional Conversion Fund when a separate project budget is committed.',
        'french_republic','Defferre decentralisation and public-bank regional investment; a proposed concrete implementation mandate.',days=28)

    add('pcf_municipal_health','pcf','Municipal Health',67,7,[['communist_settlement']],
        [fee(.45),building(58,'offices'),building(62,'offices'),mod('health_cost_multiplier_modifier',-.04),mod('social_cost_multiplier_modifier',.05)],
        'Extend the municipal health and prevention tradition through service centres in Bourgogne and Rhone-Alpes. Better access and prevention lower health expenditure, while permanent local provision carries a larger social bill.',
        'french_communist_party','Saint-Denis municipal health and maternal-child provision; documented communist municipal practice.')
    add('pcf_supply_contracts','pcf','Supply Contracts',71,7,[['communist_settlement']],
        [fee(.55),building(55,'industrial_complex'),building(59,'agriculture_district'),study('CAT_industry',.25),mod('corporate_tax_income_multiplier_modifier',-.04)],
        'Link food processing and productive orders through a Normandie plant and a Loire agricultural district. Public procurement builds practical capacity, but guaranteed terms and concessions reduce corporate-tax receipts.',
        'farming_sector','Municipal provisioning, public-enterprise purchasing and the PCF debate over household supply versus central industrial priorities.')
    exclude('pcf_municipal_health','pcf_supply_contracts')

    add('psu_cooperative_markets','psu','Cooperative Markets',75,4,[['psu_cooperative_exchange','psu_union_institutes']],
        [fee(.30),building(60,'offices'),study('CAT_industry'),mod('corporate_tax_income_multiplier_modifier',-.03)],
        'Give worker-managed enterprises a shared Aquitaine sales and accounting office. A market-facing federation can spread practical experience, but preferential finance and retained earnings reduce tax receipts.',
        'french_union','PSU self-management debates and the Lip production-and-sales experiment of 1973; a national version is counterfactual.')
    add('psu_tenants_councils','psu',"Tenants' Councils",83,4,[['psu_cooperative_exchange','psu_union_institutes']],
        [fee(.35),building(64,'offices'),building(959,'infrastructure'),mod('social_cost_multiplier_modifier',.04)],
        'Let residents and service users share responsibility for a Bretagne neighbourhood office and access works in Pays de la Loire. Local participation receives concrete institutions, alongside a lasting public-service commitment.',
        'french_democracy','PSU anti-authoritarian local participation and user-managed neighbourhood services, distinguished from ownership of industrial firms.')
    exclude('psu_cooperative_markets','psu_tenants_councils')
    add('psu_land_banks','psu','Cooperative Land',79,5,[['psu_cooperative_markets','psu_tenants_councils']],
        [fee(.35),building(58,'offices'),slots(60,3),study('CAT_industry',.25),mod('corporate_tax_income_multiplier_modifier',-.02)],
        'Create a Bourgogne land-credit office and prepare serviced sites in Aquitaine for cooperative enterprise and community facilities. Below-market terms broaden access, while reducing the taxable returns captured from development.',
        'economic_roads_new','A counterfactual land-and-credit instrument for PSU self-management and municipal participation; the site capacity is an MD abstraction.')

    add('ecology_river_basins','ecology','River Basin Works',87,4,[['ecological_industry','local_sufficiency']],
        [fee(.45),building(57,'offices'),building(55,'infrastructure'),study('CAT_infrastructure'),mod('health_cost_multiplier_modifier',-.02),mod('production_speed_industrial_complex_factor',-.03)],
        'Strengthen river-basin inspection in Alsace-Lorraine and sanitation infrastructure in Normandie. Prevention and cleaner services can reduce health costs, while discharge standards slow the approval of new industrial sites.',
        'green_world','The 1964 water law, basin agencies and the June 1970 environmental measures programme; no separate water-treatment building is invented.')
    add('ecology_municipal_heat','ecology','Municipal Heat',91,4,[['ecological_industry','local_sufficiency']],
        [fee(.55),building(62,'fossil_powerplant'),building(58,'infrastructure'),mod('energy_use_modifier_civs',-.03),mod('education_cost_multiplier_modifier',.05)],
        'Fund a Rhone-Alpes combined heat-and-power site and connected local infrastructure in Bourgogne. Shared heat distribution reduces waste, but operation requires trained staff and does not make fossil generation carbon-free.',
        'powerplant','French heat-network expansion during 1955-75 and later fuel-diversification programmes; earlier networks often used coal or fuel oil.')
    exclude('ecology_river_basins','ecology_municipal_heat')

    add('cid_wholesale_cooperatives','right','Mutual Purchasing',95,3,[['cid_cooperatives']],
        [fee(.30),building(60,'offices'),study('CAT_industry',.25),mod('corporate_tax_income_multiplier_modifier',-.03)],
        'Pool independent traders\' purchasing, accounts and equipment advice through an Aquitaine office. Collective scale can help small firms, while preferential terms reduce corporate-tax receipts.',
        'economic_prosperity','Independent-trader mutual support as a counterfactual CID programme, not the later FN platform or the 1973 Royer law.',phase='cid')
    add('cid_rural_networks','right','Rural Shop Grants',97,3,[['cid_cooperatives']],
        [fee(.45),building(59,'agriculture_district'),building(61,'infrastructure'),opinion('farmers',10),mod('social_cost_multiplier_modifier',.03)],
        'Support rural processing, regular markets and distribution through a Loire agricultural district and Midi-Pyrenees access works. The network assists farming communities but requires continuing local-service support.',
        'FRA_ruralism','Rural commercial-life concerns and independent-trader mobilisation; proposed early CID support, distinct from later commercial-zoning legislation.',phase='cid')
    exclude('cid_wholesale_cooperatives','cid_rural_networks')
    add('fn_arsenal_orders','right','Arsenal Renewal',99,3,[['fn_defence']],
        [fee(.65),building(54,'arms_factory'),building(60,'industrial_complex'),study('CAT_armor',.25),mod('equipment_cost_multiplier_modifier',.04)],
        'Direct defence orders toward domestic production in Hauts-de-France and Aquitaine. Additional industrial capacity supports the armed nation, while protected procurement raises the equipment bill.',
        'french_army','Counterfactual FN industrial-national programme after its actual party identity exists; no claim of a historical FN national government.',phase='fn')
    add('fn_contract_inspection','right','Export Inspection',103,3,[['fn_defence']],
        [fee(.40),building(63,'offices'),dict(kind='experience',service='air',amount=15,once=True),study('CAT_aircraft'),mod('airforce_personnel_cost_multiplier_modifier',.05)],
        'Build a Provence office for military aviation certification and technical export support. Evaluation flights and specialist studies improve expertise, while instructor and inspection posts enlarge the air personnel bill.',
        'french_army_air','French aircraft-export and technical-support institutions provide a precedent; this party-government allocation is counterfactual.',phase='fn')
    exclude('fn_arsenal_orders','fn_contract_inspection')

    # Reuse the existing one-time fund. A second identical project menu would
    # duplicate its real asset; this route widens authority, not the award count.
    decision = next(d for d in design['decisions'] if d['id']=='COLDWAR_FRA2P_regional_conversion')
    decision_before = deepcopy(decision)
    decision['conditions'] = [c.replace('Public Bank Credit completed','Public Bank Credit or Conversion Boards completed') for c in decision['conditions']]
    decision['runtime_guards'] = [g.replace('has_completed_focus = COLDWAR_FRA2_public_banks','OR = { has_completed_focus = COLDWAR_FRA2_public_banks has_completed_focus = COLDWAR_FRA2_ps_conversion_boards }') for g in decision['runtime_guards']]
    design['project']='IMPERIA COLD WAR'
    design['status']='DESIGN PROPOSAL ONLY. Additional party programmes are not installed.'
    design['revision']='France 1970 party expansion: twenty additional policy focuses'
    design['proposal_baseline_sha256']=EXPECTED
    design['expansion_focus_keys']=[n['key'] for n in added]
    design['navigation']['preview_section']='ri'
    design['navigation']['initial_focus']='COLDWAR_FRA2_ri_sme_capital'
    design['navigation']['initial_government']='ri'
    before=HERE/'BASELINE.json'
    assert not before.exists() or before.read_bytes()==raw, 'Frozen baseline drift'
    before.write_bytes(raw)
    def write(name,value):
        (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write('proposal.json',design)
    write('ADDITIONS.json',dict(project='IMPERIA COLD WAR',baseline_sha256=EXPECTED,added_focuses=added,focus_changes=focus_changes,new_decisions=[],decision_changes=[dict(before=decision_before,after=decision)]))
    manifest=json.loads((ROOT/'tools/france_1970_runtime/manifest.json').read_text())
    files={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in manifest['files']}
    runtime_before=HERE/'RUNTIME_BASELINE.json'
    assert not runtime_before.exists() or json.loads(runtime_before.read_text(encoding='utf-8'))['files']==files, 'Loaded runtime changed during design work.'
    write('RUNTIME_BASELINE.json',dict(project='IMPERIA COLD WAR',files=files,phase='Before uninstalled party expansion'))
    print(json.dumps(dict(project='IMPERIA COLD WAR',status='Proposal only',baseline_focuses=len(baseline['nodes']),proposed_focuses=len(design['nodes']),added=len(added),offers=sum('offer' in n for n in design['nodes']),new_decisions=0,broadened_existing_funds=1),indent=2))


if __name__=='__main__': build()
