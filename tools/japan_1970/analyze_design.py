# IMPERIA CW — Cold War: Japan 1970 approved design effect inventory.
"""Translate explicit general-policy rewards into reviewable MD effect records.

This is a read-only analysis step; it never writes loaded mod content.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'approved_design.json').read_text(encoding='utf-8'))['design']

# Labels are resolved to keys with a country-scope use in current MD Japan or
# current MD modifier definitions and consumers. Percent values remain fractions.
KEYS = {
 'stability factor':'stability_factor', 'stability':'stability_factor',
 'bureaucracy spending':'bureaucracy_cost_multiplier_modifier', 'bureaucracy expenditure':'bureaucracy_cost_multiplier_modifier',
 'social spending':'social_cost_multiplier_modifier', 'social expenditure':'social_cost_multiplier_modifier',
 'health spending':'health_cost_multiplier_modifier', 'health expenditure':'health_cost_multiplier_modifier',
 'education spending':'education_cost_multiplier_modifier', 'education expenditure':'education_cost_multiplier_modifier',
 'army personnel spending':'army_personnel_cost_multiplier_modifier', 'army personnel expenditure':'army_personnel_cost_multiplier_modifier',
 'civilian-sector productivity':'civilian_factories_productivity', 'military factory output':'industrial_capacity_factory',
 'dockyard-sector productivity':'dockyard_productivity', 'office-sector productivity':'offices_productivity',
 'agricultural productivity':'agricolture_productivity_modifier', 'research speed':'research_speed_factor',
 'army core defence':'army_core_defence_factor', 'army defence':'army_defence_factor', 'army attack':'army_attack_factor',
 'army training time':'training_time_factor', 'training time':'training_time_factor',
 'army experience gain factor':'experience_gain_army_factor', 'air experience gain factor':'experience_gain_air_factor',
 'navy organisation':'navy_org_factor', 'submarine detection':'navy_submarine_detection_factor',
 'naval range':'navy_max_range_factor', 'air detection':'air_detection', 'air mission efficiency':'air_mission_efficiency',
 'air range':'air_range_factor', 'planning speed':'planning_speed', 'recruitable population factor':'recruitable_population_factor',
 'dockyard output':'industrial_capacity_dockyard', 'military factory energy use':'energy_use_modifier_mils',
 'dockyard energy use':'energy_use_modifier_dockyards', 'civilian factory energy use':'energy_use_modifier_civs',
 'office energy use':'energy_use_modifier_offices', 'non-electric fuel consumption':'non_electric_fuel_consumption_modifier',
 'fossil power-plant fuel consumption':'fossil_pp_fuel_consumption_modifier', 'fossil power generation':'fossil_pp_energy_generation_modifier',
 'nuclear fuel consumption':'nuclear_fuel_consumption_modifier', 'nuclear electricity generation':'nuclear_energy_generation_modifier',
 'renewable electricity generation':'renewable_energy_gain_multiplier', 'electricity generation':'energy_gain_multiplier',
 'maximum fuel capacity':'max_fuel_factor', 'fuel capacity':'max_fuel_factor',
 'productivity growth multiplier':'country_productivity_growth_modifier', 'productivity growth':'country_productivity_growth_modifier',
 'civilian factory construction speed':'production_speed_industrial_complex_factor',
 'industrial capacity construction speed':'production_speed_industrial_complex_factor',
 'dockyard construction speed':'production_speed_dockyard_factor',
}

# ID -> list of (state, building, count, added shared slots).
BUILDINGS = {
 'national_4_escort_yard_modernisation':[(611,'dockyard',1,1)], 'national_4_factory_modernisation':[(615,'arms_factory',1,1)],
 'coal_transition':[(617,'fossil_powerplant',1,0)], 'fuel_reserves':[(615,'fuel_silo',2,0)],
 'liquefied_gas':[(612,'fossil_powerplant',1,0)], 'resilient_energy_network':[(613,'energy_infrastructure',1,0)],
 'nuclear_expansion':[(612,'nuclear_reactor',1,0)], 'distributed_power':[(609,'renewable_energy_infra',1,0)],
 'reactor_siting':[(616,'nuclear_reactor',1,0)], 'grid_storage':[(616,'energy_infrastructure',1,0)],
 'electricity_reliability':[(615,'industrial_infrastructure',1,0)],
 'shinkansen_capacity':[(615,'rail_terminal',1,0),(612,'rail_terminal',1,0)],
 'freight_rail':[(613,'rail_terminal',1,0),(609,'rail_terminal',1,0)],
 'tokyo_commuter':[(615,'infrastructure',1,0)], 'kansai_redevelopment':[(612,'industrial_complex',1,1)],
 'regional_airports':[(616,'infrastructure',1,0)], 'industrial_freight':[(613,'rail_terminal',1,0)],
 'regional_port_links':[(609,'infrastructure',1,0),(610,'infrastructure',1,0)],
 'complete_corridors':[(611,'infrastructure',1,0),(617,'infrastructure',1,0)],
 'financial_centres':[(615,'offices',1,1)], 'regional_services':[(616,'offices',1,1)],
 'regional_banking':[(613,'offices',1,1)], 'communications_grid':[(612,'internet_station',1,0)],
 'knowledge_economy':[(615,'offices',1,1)], 'tohoku_development':[(616,'industrial_complex',1,1)],
 'hokkaido_development':[(617,'industrial_complex',1,1)], 'tohoku_rail_link':[(616,'rail_terminal',1,0)],
 'tohoku_supply_firms':[(616,'industrial_complex',1,1)], 'hokkaido_ports':[(617,'infrastructure',1,0)],
 'hokkaido_processing':[(617,'industrial_complex',1,1)], 'regional_growth_agreement':[(611,'offices',1,1)],
 'microelectronics_capacity':[(615,'microchip_plant',1,1)], 'precision_tools':[(613,'industrial_complex',1,1)],
}

SPECIAL={
 'national_5_the_pollution_diet':{'pollution_stability':0.02},
 'national_5_compensate_affected_communities':{'pollution_stability':0.02},
 'national_5_water_quality_inspections':{'pollution_health':-0.03},
 'national_5_medical_certification':{'pollution_health':-0.02},
 'efficient_factories':{'energy_use_civs':-0.05},
}

def parse(node):
 text=node['effects']; normal=text.lower().replace('−','-').replace('–','-')
 matches=[]
 # Matched spans are recorded to expose accidentally double-counted phrases.
 for label,key in sorted(KEYS.items(),key=lambda kv:-len(kv[0])):
  expr=r'(?<![a-z-])'+re.escape(label)+r'\s*([+-])\s*(\d+(?:\.\d+)?)\s*%|([+-])\s*(\d+(?:\.\d+)?)\s*%\s*'+re.escape(label)+r'(?![a-z-])'
  for m in re.finditer(expr,normal):
   if any(m.start()<end and start<m.end() for start,end in (p[0] for p in matches)):continue
   sign=m.group(1) or m.group(3);amount=m.group(2) or m.group(4)
   matches.append(((m.start(),m.end()),key,(-1 if sign=='-' else 1)*float(amount)/100))
 costs=re.findall(r'treasury\s*-\s*\$\s*(\d+(?:\.\d+)?)\s*billion',normal)
 bonuses=[]
 for category in ('industry','agriculture'):
  if '25% research bonus for one '+category+' technology' in normal:bonuses.append({'category':'CAT_'+category,'uses':1,'bonus':0.25})
 duration=730 if 'for 730 days' in normal else (365 if 'for 365 days' in normal else None)
 return {'id':node['id'],'effects_text':text,'modifiers':{key:sum(m[2] for m in matches if m[1]==key) for _,key,_ in matches},
         'treasury_cost':sum(map(float,costs)),'buildings':BUILDINGS.get(node['id'],[]),'bonuses':bonuses,
         'duration':duration,'special':SPECIAL.get(node['id'],{}),'matched':len(matches)}

def main():
 records=[]
 for section in DATA['sections']:
  if section['category'] not in ('National life','Economy'):continue
  for n in section['nodes']:
   if n['id'].startswith('COLDWAR_JAP_1970_article9_'):continue
   record=parse(n); records.append(record)
   if not (record['matched'] or record['treasury_cost'] or record['buildings'] or record['bonuses'] or record['special']):
    print('UNRESOLVED',record['id'],record['effects_text'])
 (ROOT/'effect_inventory.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
 print('Inventoried',len(records),'general-policy focuses; human review required before use.')

if __name__=='__main__':main()
