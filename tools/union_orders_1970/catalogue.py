# IMPERIA COLD WAR — Verified annual Union order families and native MD equipment targets.
"""The labels describe actual MD archetypes. Narrow output needs certified returns."""
from dataclasses import dataclass

TAGS = ('UKR', 'BLR', 'EST', 'LAT', 'LIT', 'ARM', 'AZE', 'GEO', 'KAZ', 'KYR', 'TAJ', 'TRK', 'UZB', 'MLV')
PERIOD = 365
OUTCOME_DAYS = 180
PROPOSAL_DAYS = 30


@dataclass(frozen=True)
class Family:
    key: str
    name: str
    group: int
    equipment: tuple[str, ...] = ()
    art: str = 'industry'
    counter: str = ''
    buildings: tuple[str, ...] = ()
    modifiers: tuple[tuple[str, float], ...] = ()
    naval: bool = False
    delivery: bool = True


FAMILIES = (
    Family('rifles', 'Small Arms', 1, ('infantry_weapons_type',), 'army'),
    Family('command', 'C&C Equipment', 1, ('cnc_equipment_type',), 'electronics'),
    Family('utility', 'Utility Vehicles', 1, ('util_vehicle_type',), 'army'),
    Family('heavy_utility', 'Heavy Utility Vehicles', 1, ('heavy_util_vehicle_type',), 'army'),
    Family('mbt', 'Main Battle Tanks', 1, ('medium_tank_chassis',), 'armour'),
    Family('light_tank', 'Light Tanks', 1, ('medium_tank_destroyer_chassis',), 'armour'),
    Family('apc', 'Armoured Personnel Carriers', 1, ('medium_tank_amphibious_chassis',), 'armour'),
    Family('ifv', 'Infantry Fighting Vehicles', 1, ('medium_tank_flame_chassis',), 'armour'),
    Family('towed_artillery', 'Towed Artillery', 2, ('artillery_equipment',), 'artillery'),
    Family('sp_artillery', 'Self-Propelled Artillery', 2, ('medium_tank_artillery_chassis',), 'artillery'),
    Family('mlrs', 'Multiple-Launch Rocket Systems', 2, ('medium_tank_rocket_chassis',), 'artillery'),
    Family('aa', 'Air-Defence Weapons', 2, ('AA_Equipment',), 'army'),
    Family('spaa', 'Self-Propelled Air Defence', 2, ('medium_tank_aa_chassis',), 'armour'),
    Family('light_at', 'Light Anti-Tank Weapons', 2, ('L_AT_Equipment',), 'army'),
    Family('heavy_at', 'Heavy Anti-Tank Weapons', 2, ('H_AT_Equipment',), 'army'),
    Family('light_fighter', 'Light Fighters', 3, ('small_plane_airframe',), 'air'),
    Family('light_multirole', 'Light Multi-Role Fighters', 3, ('small_plane_strike_airframe',), 'air'),
    Family('light_cas', 'Light Close-Support Aircraft', 3, ('small_plane_cas_airframe',), 'air'),
    Family('multirole', 'Multi-Role Fighters', 3, ('medium_plane_airframe',), 'air'),
    Family('air_superiority', 'Air Superiority Fighters', 3, ('medium_plane_fighter_airframe',), 'air'),
    Family('cas', 'Close-Support Aircraft', 3, ('medium_plane_cas_airframe',), 'air'),
    Family('air_transport', 'Heavy Lift Aircraft', 3, ('large_plane_air_transport_airframe',), 'air'),
    Family('attack_helicopter', 'Attack Helicopters', 3, ('heavy_tank_chassis',), 'air'),
    Family('transport_helicopter', 'Transport Helicopters', 3, ('heavy_tank_amphibious_chassis',), 'air'),
    Family('patrol', 'Patrol Boats', 4, ('patrol_boat',), 'navy', naval=True, delivery=False),
    Family('corvette', 'Corvettes', 4, ('corvette',), 'navy', naval=True, delivery=False),
    Family('frigate', 'Frigates', 4, ('frigate',), 'navy', naval=True, delivery=False),
    Family('destroyer', 'Destroyers', 4, ('destroyer',), 'navy', naval=True, delivery=False),
    Family('cruiser', 'Cruisers', 4, ('cruiser',), 'navy', naval=True, delivery=False),
    Family('carrier', 'Aircraft Carriers', 4, ('carrier',), 'navy', naval=True, delivery=False),
    Family('attack_submarine', 'Attack Submarines', 4, ('attack_submarine',), 'navy', naval=True, delivery=False),
    Family('missile_submarine', 'Missile Submarines', 4, ('missile_submarine',), 'navy', naval=True, delivery=False),
    Family('convoy', 'Convoys', 4, ('convoy',), 'navy', counter='total_equipment_produced_convoy', naval=True),
    Family('guided_missile', 'Guided Missiles', 5, ('guided_missile_equipment',), 'artillery', counter='total_equipment_produced_missile'),
    Family('ballistic_missile', 'Ballistic Missiles', 5, ('ballistic_missile_equipment',), 'artillery', counter='total_equipment_produced_ballistic_missile'),
    Family('sam_missile', 'Surface-to-Air Missiles', 5, ('sam_missile_equipment',), 'army', counter='total_equipment_produced_sam_missile'),
    # An honest broad category supplements certified, narrower artillery returns.
    Family('artillery_class', 'Artillery-Class Equipment', 2,
           ('artillery_equipment', 'medium_tank_artillery_chassis'),
           'artillery', counter='total_equipment_produced_artillery', delivery=False),
    Family('civilian', 'Civilian Factories', 6, art='industry', buildings=('industrial_complex',), modifiers=(('civilian_factories_productivity', .05),), delivery=False),
    Family('military', 'Military Factories', 6, art='industry', buildings=('arms_factory',), modifiers=(('industrial_capacity_factory', .05),), delivery=False),
    Family('agriculture', 'Agricultural Districts', 6, art='agriculture', buildings=('agriculture_district',), modifiers=(('agricolture_productivity_modifier', .08),), delivery=False),
    Family('cotton', 'Cotton and Textile Capacity', 6, art='agriculture', buildings=('agriculture_district', 'industrial_complex'), modifiers=(('agricolture_productivity_modifier', .04), ('civilian_factories_productivity', .04)), delivery=False),
    Family('fossil', 'Thermal Power Stations', 6, art='energy', buildings=('fossil_powerplant',), modifiers=(('fossil_pp_energy_generation_modifier', .05),), delivery=False),
    Family('infrastructure', 'Infrastructure', 6, art='trade', buildings=('infrastructure',), modifiers=(('production_speed_infrastructure_factor', .10),), delivery=False),
    Family('dockyard', 'Dockyards', 6, art='navy', buildings=('dockyard',), modifiers=(('industrial_capacity_dockyard', .05),), naval=True, delivery=False),
)
BY_KEY = {f.key: f for f in FAMILIES}
IDS = {f.key: i for i, f in enumerate(FAMILIES, 1)}
GROUPS = {1: 'Land Equipment', 2: 'Artillery and Air Defence', 3: 'Aircraft and Helicopters', 4: 'Naval Construction', 5: 'Missile Production', 6: 'Civil Development'}
# These intersecting programmes cannot reserve the same output twice.
CONFLICTS = {f.key: tuple(g.key for g in FAMILIES if set(f.equipment) & set(g.equipment)) for f in FAMILIES}
# Cotton processing and ordinary construction must not reuse the same new capacity.
for _key in ('civilian', 'agriculture', 'cotton'):
    CONFLICTS[_key] = ('agriculture', 'civilian', 'cotton') if _key == 'cotton' else (_key, 'cotton')

# MD explicitly lists duplicate archetypes separately in its own bonuses.
# Aggregate actual repeated targets; do not infer parent/duplicate propagation.
CHANNELS = tuple(f for f in FAMILIES if len(f.equipment) <= 1)
CHANNEL_TARGETS = {f.equipment[0]: f for f in CHANNELS if f.equipment}
CHANNEL_SOURCES = {f.key: tuple(g for g in FAMILIES if (set(f.equipment) & set(g.equipment)) or g.key == f.key) for f in CHANNELS}


def channels_for(family):
    return tuple(CHANNEL_TARGETS[t] for t in family.equipment) if family.equipment else (family,)

# Existing joint-tree institutions remain useful after retiring fabricated plan
# completion. Values below are gameplay calibration, not historical statistics.
POLICIES = {
    'directive_staff': ('COLDWAR_UNI_cheap_directives', 'Union Commissioning Staff', 'civil_service',
        {'production_factory_efficiency_gain_factor': .05, 'bureaucracy_cost_multiplier_modifier': .02},
        'A permanent commissioning staff standardises republican production schedules. Its specialists improve the next production series while adding to the Union administrative bill.'),
    'production_audit': ('COLDWAR_UNI_peoples_control', 'Union Production Inspectorate', 'administration',
        {'tax_gain_multiplier_modifier': .04, 'bureaucracy_cost_multiplier_modifier': .03},
        'Inspectors reconcile enterprise returns and public receipts. Better accounts recover revenue, but regular inspection requires a larger administrative establishment.'),
    'control_commission': ('COLDWAR_UNI_party_control', 'Union Control Commission', 'discipline',
        {'political_power_factor': .05, 'stability_factor': -.02},
        'The control commission can enforce the centre\'s decisions across ministerial boundaries. Its authority comes at the cost of resentment among officials and enterprise directors.'),
    'counter_plan': ('COLDWAR_UNI_counter_unlocked', 'Counter-Plan Production Standards', 'planning',
        {'production_factory_max_efficiency_factor': .05, 'energy_use_multiplier': .02},
        'Enterprise collectives commit to higher operating standards. Longer standardised production runs raise attainable efficiency and place greater demands on power supplies.'),
}
TEMPORARY_POLICIES = {
    'procurement_agents': ('COLDWAR_UNI_tolkachi_unlocked', 'Republican Procurement Network', 'trade',
        {'production_factory_efficiency_gain_factor': .10, 'production_speed_buildings_factor': .05, 'bureaucracy_cost_multiplier_modifier': .05},
        'Republican procurement agents locate missing components and arrange deliveries between enterprises. Their favours keep work moving while increasing administrative costs.'),
    'overtime': ('COLDWAR_UNI_storming_unlocked', 'Extra Production Shifts', 'industry',
        {'industrial_capacity_factory': .15, 'production_speed_buildings_factor': -.10},
        'Factories work additional shifts to meet the annual commission. Industrial output rises, while construction loses personnel, transport and materials.'),
}
