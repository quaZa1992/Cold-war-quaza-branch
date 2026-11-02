# IMPERIA COLD WAR — Historically grounded land doctrine expansion design.
"""Approved numeric packages, native scopes, English text and AI preferences."""
from copy import deepcopy

PROJECT = 'IMPERIA COLD WAR'
FEATURE = 'Cold War land doctrine expansion'


def units(names, **stats):
    return {name: deepcopy(stats) for name in names}


MOBILE = ('Mot_Inf_Bat', 'Hvy_Mot_Inf_Bat', 'Mech_Inf_Bat', 'Arm_Inf_Bat')
ASSAULT = ('category_foot_inf', *MOBILE)
AT = ('AT_company', 'Mot_AT_company')
SF = 'category_special_forces'


def reward(key, name, description, effects):
    return dict(key=key, name=name, description=description, effects=effects)


GRANDS = [
    dict(
        id='mdcw_deliberate_firepower', name='Deliberate Firepower',
        description=(
            "Van Fleet's Eighth Army in Korea in 1951 relied on registered artillery fire and forward ammunition stocks. "
            'Deliberate infantry assaults gain prepared fire superiority at the cost of movement speed and a heavier supply burden.'),
        tracks=['structure_doctrine', 'operational_theory', 'dedicated_doctrine', 'training', 'leadership', 'technology'],
        effects=dict(army_artillery_attack_factor=0.10, max_planning_factor=0.05,
                     army_speed_factor=-0.05, supply_consumption_factor=0.10),
        milestones=[
            ('Fire Support Planning', dict(planning_speed=0.10)),
            ('Registered Fire Plans', dict(army_artillery_attack_factor=0.10)),
            ('Timed Assaults', dict(coordination_bonus=0.10)),
            ('Protected Infantry Advance', dict(breakthrough_factor=0.05)),
            ('Consolidation Orders', dict(army_infantry_defence_factor=0.05)),
            ('Surveyed Firing Positions', dict(max_planning_factor=0.10, army_org_regain=0.05)),
        ],
        ai={'base': 1, 'countries': ['EGY', 'RAJ', 'IRQ'], 'country_weight': 8},
    ),
    dict(
        id='mdcw_mobile_raiding_warfare', name='Mobile Raiding Warfare',
        description=(
            'South African battle groups of the 1970s and 1980s used rapid concentration, flanking movement and withdrawal across wide spaces. '
            'Forward loads sustain short advances, while fixed fronts expose weaker defence and limited battle preparation.'),
        tracks=['structure_doctrine', 'operational_theory', 'operational_theory', 'training', 'leadership', 'technology'],
        effects=dict(army_speed_factor=0.05, recon_factor=0.10,
                     max_planning_factor=-0.10, army_defence_factor=-0.05),
        milestones=[
            ('Independent Columns', dict(org_loss_when_moving=-0.10)),
            ('Forward Supply Loads', dict(no_supply_grace=48)),
            ('Mounted Assault Groups', units(MOBILE, soft_attack=0.10, breakthrough=0.10)),
            ('Mobile Fire Coordination', dict(coordination_bonus=0.10)),
            ('Rapid Disengagement', dict(army_speed_factor=0.05)),
            ('Field Recovery Teams', dict(army_org_regain=0.10, org_loss_when_moving=-0.10)),
        ],
        ai={'base': 1, 'countries': ['SAF'], 'country_weight': 20},
    ),
]

SUBS = [
    dict(
        id='mdcw_cohesive_unit_rotation', track='structure_doctrine', name='Cohesive Unit Rotation',
        description=(
            'British unit rotation and the later American COHORT programme kept crews and companies together through training and service. '
            'Stable teams preserve experience and cohesion, but require longer training and a costlier personnel system.'),
        effects=dict(army_org_factor=0.05, experience_loss_factor=-0.10,
                     army_personnel_cost_multiplier_modifier=0.10, training_time_army_factor=0.10),
        rewards=[
            reward('stable_crews', 'Stable Crews', 'Established crews know their equipment and continue to function when casualties disrupt the formation.', dict(army_strength_factor=0.05)),
            reward('collective_recovery', 'Collective Recovery', 'Units restore their command relationships and reorganise as familiar teams after combat.', dict(army_org_regain=0.10)),
            reward('regimental_continuity', 'Regimental Continuity', 'Experienced soldiers remain with their formations and pass on the habits learned in the field.', dict(experience_loss_factor=-0.15)),
            reward('familiar_command_teams', 'Familiar Command Teams', 'Commanders and subordinate leaders rehearse together and understand how neighbouring units operate.', dict(army_org_factor=0.05, coordination_bonus=0.05)),
            reward('unit_rotation_cycle', 'Unit Rotation Cycle', 'Relief and retraining are organised around coherent units rather than a continuous turnover of individuals.', dict(army_org_regain=0.05, land_reinforce_rate=0.02)),
        ],
        ai={'base': 2, 'countries': ['ENG', 'ISR'], 'country_weight': 8},
    ),
    dict(
        id='mdcw_integrated_support_commands', track='structure_doctrine', name='Integrated Support Commands',
        description=(
            'Logistical commands in Korea and corps support commands in the 1960s united supply, workshops, recovery and medical services. '
            'Integrated support sustains the fighting force, but needs more personnel and slows the march column.'),
        effects=dict(supply_consumption_factor=-0.05, coordination_bonus=0.05,
                     army_personnel_cost_multiplier_modifier=0.08, army_speed_factor=-0.05),
        rewards=[
            reward('recovery_sections', 'Recovery Sections', 'Dedicated recovery sections keep damaged formations functioning through extended operations.', dict(army_strength_factor=0.05)),
            reward('consolidated_supply_points', 'Consolidated Supply Points', 'Common distribution points reduce duplication and direct stocks towards the units that need them.', dict(supply_consumption_factor=-0.05)),
            reward('forward_workshops', 'Forward Workshops', 'Combat service support companies carry workshop teams forward to maintain the equipment of their formations.', {'combat_service_support_company': {'reliability_factor': 0.03}}),
            reward('medical_evacuation_chains', 'Medical Evacuation Chains', 'Coordinated evacuation and support arrangements allow exhausted units to reorganise sooner.', dict(army_org_regain=0.10)),
            reward('sustained_support_groups', 'Sustained Support Groups', 'Permanent support groups organise replacement stocks and services for a sustained campaign.', dict(supply_consumption_factor=-0.05, army_strength_factor=0.05)),
        ],
        ai={'base': 2, 'countries': ['RAJ', 'EGY'], 'country_weight': 5},
    ),
    dict(
        id='mdcw_forest_envelopment', track='operational_theory', name='Forest Envelopment',
        description=(
            'Finnish motti operations isolated road-bound columns through forest movement and flank attacks, including summer campaigns in 1941 to 1944. '
            'Light infantry gains local mobility and surprise at the expense of elaborate central battle preparation.'),
        effects={'L_Inf_Bat': {'forest': {'attack': 0.10, 'movement': 0.10}}, 'max_planning_factor': -0.10},
        rewards=[
            reward('local_route_reconnaissance', 'Local Route Reconnaissance', 'Patrols identify tracks and covered approaches beyond the roads used by enemy columns.', dict(recon_factor=0.10)),
            reward('road_column_isolation', 'Road Column Isolation', 'Light infantry establishes local blocking positions and attacks isolated road-bound detachments.', {'L_Inf_Bat': {'forest': {'attack': 0.10, 'defence': 0.10}}}),
            reward('independent_march_groups', 'Independent March Groups', 'Small march groups preserve cohesion while moving between dispersed objectives.', dict(org_loss_when_moving=-0.15)),
            reward('night_flank_marches', 'Night Flank Marches', 'Night movement conceals the approach to vulnerable flanks and rear positions.', dict(land_night_attack=0.10)),
            reward('concentrated_local_attacks', 'Concentrated Local Attacks', 'Local commanders assemble light infantry rapidly at the point chosen for a short attack.', {'L_Inf_Bat': {'forest': {'movement': 0.10}}, 'initiative_factor': 0.10}),
        ],
        ai={'base': 2, 'countries': ['FIN', 'NRY', 'SWE'], 'country_weight': 15},
    ),
    dict(
        id='mdcw_heliborne_reaction_forces', track='operational_theory', name='Heliborne Reaction Forces',
        description=(
            'Rhodesian Fireforce operations from 1974 linked small helicopter-borne blocking groups with reconnaissance and follow-up forces. '
            'Equipped air-assault infantry gains mobility and cohesion, but aircraft upkeep and fuel demand increase.'),
        effects={'L_Air_assault_Bat': {'soft_attack': 0.10}, 'army_fuel_consumption_factor': 0.10, 'equipment_cost_multiplier_modifier': 0.05},
        rewards=[
            reward('lift_coordination', 'Lift Coordination', 'Lift serials and command arrangements keep air-assault infantry together during deployment.', {'L_Air_assault_Bat': {'max_organisation': 3}}),
            reward('blocking_groups', 'Blocking Groups', 'Air-assault infantry practises establishing and fighting from small blocking positions.', {'L_Air_assault_Bat': {'breakthrough': 0.15}}),
            reward('landing_zone_reconnaissance', 'Landing Zone Reconnaissance', 'Reconnaissance identifies suitable approaches and landing areas in broken and wooded terrain.', {'L_Air_assault_Bat': {terrain: {'movement': 0.10} for terrain in ('forest', 'hills', 'jungle')}}),
            reward('air_ground_control_teams', 'Air Ground Control Teams', 'Ground and aviation representatives share reports and coordinate the commitment of reaction forces.', dict(recon_factor=0.10, coordination_bonus=0.05)),
            reward('follow_up_forces', 'Follow Up Forces', 'Follow-up formations relieve the first blocking groups and maintain contact after the initial deployment.', {'L_Air_assault_Bat': {'max_organisation': 2}, 'initiative_factor': 0.10, 'org_loss_when_moving': -0.10}),
        ],
        ai={'base': 1, 'countries': ['ZIM', 'SAF'], 'country_weight': 15},
    ),
    dict(
        id='mdcw_assault_breaching', track='dedicated_doctrine', name='Assault Breaching',
        description=(
            'British specialist formations in 1943 and 1944 and Egyptian engineers at Suez in 1973 demonstrated deliberate obstacle assaults. '
            'Infantry rehearses crossings and attacks on fortified positions, increasing training and supply requirements.'),
        effects={**units(ASSAULT, fort={'attack': 0.05}, river={'attack': 0.05}), 'supply_consumption_factor': 0.10, 'training_time_army_factor': 0.10},
        rewards=[
            reward('obstacle_reconnaissance', 'Obstacle Reconnaissance', 'Reconnaissance records obstacles, approaches and defended crossing points before the assault.', dict(planning_speed=0.10)),
            reward('crossing_teams', 'Crossing Teams', 'Assault troops rehearse their crossing sequence and the formation of a bridgehead.', units(ASSAULT, river={'attack': 0.10})),
            reward('breaching_lanes', 'Breaching Lanes', 'Assault groups train to advance through selected lanes against defended positions.', units(ASSAULT, fort={'attack': 0.15})),
            reward('assault_echelon', 'Assault Echelon', 'The leading infantry echelon concentrates its supporting weapons at the penetration point.', units(ASSAULT, breakthrough=0.10)),
            reward('bridgehead_coordination', 'Bridgehead Coordination', 'Follow-up troops maintain the assault timetable and consolidate the lodgement.', dict(coordination_bonus=0.10, planning_decay_rate_factor=-0.10)),
        ],
        ai={'base': 2, 'countries': ['EGY', 'ENG'], 'country_weight': 12},
    ),
    dict(
        id='mdcw_key_zone_defence', track='dedicated_doctrine', name='Key Zone Defence',
        description=(
            "Austria's 1970s Raumverteidigung concentrated defence in prepared passes and key routes. "
            'Fort and river positions sustain local resistance, but bind troops and supplies. '
            'An alternative to Territorial Defence Forces.'),
        effects=dict(dig_in_speed_factor=0.10, army_attack_speed_factor=-0.10, supply_consumption_factor=0.05),
        excludes=['mdcw_territorial_defence', 'dedicated_mdcw_territorial_defence'],
        rewards=[
            reward('prepared_blocking_positions', 'Prepared Blocking Positions', 'Reconnoitred blocking positions provide a prepared base for local defence.', dict(max_dig_in=1)),
            reward('defended_passes', 'Defended Passes', 'Foot infantry organises the defence of hill routes and mountain passes.', {'category_foot_inf': {'hills': {'defence': 0.15}, 'mountain': {'defence': 0.15}}}),
            reward('local_observation_posts', 'Local Observation Posts', 'Concealed observation posts watch the approaches to occupied defensive positions.', dict(recon_factor_while_entrenched=0.15)),
            reward('covered_obstacles', 'Covered Obstacles', 'Foot infantry covers prepared fortifications and river obstacles with mutually supporting fire.', {'category_foot_inf': {'fort': {'defence': 0.40}, 'river': {'defence': 0.20}}}),
            reward('continued_local_resistance', 'Continued Local Resistance', 'Local defence plans provide alternate positions and orders for continuing resistance under pressure.', dict(max_dig_in=2, dig_in_speed_factor=0.10, org_loss_at_low_org_factor=-0.10)),
        ],
        ai={'base': 2, 'countries': ['AUS', 'SWI'], 'country_weight': 15},
    ),
    dict(
        id='mdcw_coastal_denial', track='dedicated_doctrine', name='Coastal Denial',
        description=(
            'Swedish coastal-defence planning in the 1950s combined protected batteries, local observation and mobile reserves. '
            'Troops contest a landing before a bridgehead forms, trading offensive breakthrough for specialised coastal upkeep.'),
        effects=dict(amphibious_invasion_defence=0.10, breakthrough_factor=-0.05, equipment_cost_multiplier_modifier=0.05),
        rewards=[
            reward('coastal_alert_plans', 'Coastal Alert Plans', 'Local units occupy prepared positions promptly when a landing threatens.', dict(dig_in_speed_factor=0.10)),
            reward('protected_coastal_batteries', 'Protected Coastal Batteries', 'Protected battery positions sustain the fire of existing coastal fortifications.', dict(coastal_bunker_effectiveness_factor=0.15)),
            reward('defended_landing_sectors', 'Defended Landing Sectors', 'Defensive plans coordinate the troops covering likely landing sectors.', dict(amphibious_invasion_defence=0.10)),
            reward('local_counterattack_reserves', 'Local Counterattack Reserves', 'Ready reserves reinforce threatened sectors before the attacker consolidates ashore.', dict(land_reinforce_rate=0.02)),
            reward('integrated_beach_defence', 'Integrated Beach Defence', 'Infantry and coastal defenders combine their resistance against the landing force.', dict(amphibious_invasion_defence=0.05, army_infantry_defence_factor=0.05)),
        ],
        ai={'base': 2, 'countries': ['SWE', 'NRY', 'DEN', 'TAI'], 'country_weight': 12},
    ),
    dict(
        id='mdcw_opposing_force_exercises', track='training', name='Opposing Force Exercises',
        description=(
            'An active opposing force and structured reviews expose weaknesses in field training. '
            'The National Training Center, operational in 1981, became a later instrumented model. '
            'Such proficiency needs more training time and personnel.'),
        effects=dict(experience_gain_army_unit_factor=0.10, training_time_army_factor=0.15, army_personnel_cost_multiplier_modifier=0.05),
        rewards=[
            reward('dedicated_opposing_units', 'Dedicated Opposing Units', 'An organised opposing force challenges the coordination of the entire formation.', dict(coordination_bonus=0.10)),
            reward('after_action_reviews', 'After Action Reviews', 'Units examine their performance and turn the experience of participants into shared practice.', dict(experience_loss_factor=-0.10)),
            reward('continuous_field_exercises', 'Continuous Field Exercises', 'Exercises continue through darkness to expose failures hidden by daylight training.', dict(land_night_attack=0.10)),
            reward('combined_arms_evaluation', 'Combined Arms Evaluation', 'Commanders evaluate the organisation and cooperation of their subordinate elements in the field.', dict(army_org_factor=0.05)),
            reward('corrective_training_cycles', 'Corrective Training Cycles', 'Follow-up exercises revisit the weaknesses identified during each evaluation.', dict(experience_gain_army_unit_factor=0.15, experience_loss_factor=-0.05)),
        ],
        ai={'base': 2, 'countries': ['USA', 'GER', 'ISR'], 'country_weight': 7},
    ),
    dict(
        id='mdcw_mission_rehearsal', track='training', name='Mission Rehearsal',
        description=(
            'Egyptian preparations for the Suez crossing in 1973 demonstrated the value of repeated mission practice. '
            'Specialist formations rehearse routes, timings and assaults, gaining proficiency through longer and more expensive training.'),
        effects=dict(planning_speed=0.05, training_time_army_factor=0.15, army_personnel_cost_multiplier_modifier=0.075),
        rewards=[
            reward('full_scale_rehearsals', 'Full Scale Rehearsals', 'Special forces practise complete missions with their supporting elements.', {SF: {'max_organisation': 3}}),
            reward('detailed_assault_plans', 'Detailed Assault Plans', 'The force prepares routes, timings and contingencies for the intended operation.', dict(max_planning_factor=0.10)),
            reward('night_rehearsals', 'Night Rehearsals', 'Night rehearsals establish recognition, navigation and control procedures before combat.', dict(land_night_attack=0.10)),
            reward('specialist_assault_drills', 'Specialist Assault Drills', 'Special forces repeat the actions required at the decisive point of the assault.', {SF: {'breakthrough': 0.10}}),
            reward('repeated_mission_cycles', 'Repeated Mission Cycles', 'Repeated preparation reinforces the organisation of specialist units and the work of their planners.', {SF: {'max_organisation': 2}, 'planning_speed': 0.10}),
        ],
        ai={'base': 2, 'countries': ['EGY', 'ISR', 'ENG'], 'country_weight': 8},
    ),
    dict(
        id='mdcw_institutional_combat_learning', track='leadership', name='Institutional Combat Learning',
        description=(
            'Korean and Vietnam War lessons systems preceded the permanent Center for Army Lessons Learned established in 1985. '
            'Reports and instructor exchanges spread operational experience, requiring evaluation staff and additional training.'),
        effects=dict(experience_gain_army_factor=0.10, training_time_army_factor=0.10, army_personnel_cost_multiplier_modifier=0.05),
        rewards=[
            reward('combat_reports', 'Combat Reports', 'Structured reports preserve the experience of units returning from operations.', dict(experience_gain_army_unit_factor=0.10)),
            reward('instructor_exchanges', 'Instructor Exchanges', 'Experienced soldiers and instructors transfer practical knowledge between formations.', dict(experience_loss_factor=-0.10)),
            reward('revised_field_manuals', 'Revised Field Manuals', 'Reviewed operational experience informs the next set of field manuals and planning procedures.', dict(max_planning_factor=0.05)),
            reward('reconstitution_studies', 'Reconstitution Studies', 'The army studies how formations recover their organisation after sustained combat.', dict(army_org_regain=0.10)),
            reward('permanent_lessons_directorate', 'Permanent Lessons Directorate', 'A standing directorate collects experience and supports the development of operational methods.', dict(experience_gain_army_factor=0.15, operational_theory_track_mastery_gain_factor=0.10)),
        ],
        ai={'base': 2, 'countries': ['ISR', 'FIN', 'USA'], 'country_weight': 6},
    ),
    dict(
        id='mdcw_guided_anti_armour_integration', track='technology', name='Guided Anti Armour Integration',
        description=(
            'Egyptian defence in 1973 showed the danger to unsupported tanks facing prepared infantry and anti-tank weapons. '
            'Trained crews coordinate observation and fire, while specialist companies incur higher upkeep and sacrifice some fire against soft targets.'),
        effects={**units(AT, hard_attack=0.10, ap_attack=0.10, soft_attack=-0.10), 'equipment_cost_multiplier_modifier': 0.05},
        rewards=[
            reward('infantry_tank_hunter_teams', 'Infantry Tank Hunter Teams', 'Foot infantry practises finding and engaging armoured threats with its existing anti-tank weapons.', {'category_foot_inf': {'hard_attack': 0.05}}),
            reward('prepared_missile_positions', 'Prepared Missile Positions', 'Anti-tank companies prepare covered firing positions with clear engagement sectors.', units(AT, ap_attack=0.15)),
            reward('coordinated_engagement_sectors', 'Coordinated Engagement Sectors', 'Anti-tank crews coordinate their sectors to concentrate effective fire on armoured targets.', units(AT, hard_attack=0.10)),
            reward('target_identification_teams', 'Target Identification Teams', 'Observers identify enemy vehicles and distinguish the most dangerous approaches.', dict(recon_factor=0.10)),
            reward('integrated_infantry_anti_armour', 'Integrated Infantry Anti Armour', 'Infantry and specialist anti-tank companies practise mutually supporting engagements.', {**units(AT, hard_attack=0.10), 'category_foot_inf': {'hard_attack': 0.05, 'ap_attack': 0.05}}),
        ],
        ai={'base': 2, 'countries': ['EGY', 'SYR', 'FIN', 'TAI'], 'country_weight': 10},
    ),
    dict(
        id='mdcw_counterfire_coordination', track='technology', name='Counterfire Coordination',
        description=(
            'Observers, sound ranging and early radars already supported artillery in Vietnam; more capable networks followed later in the Cold War. '
            'Coordinated acquisition improves existing guns, but adds supply demand and specialist equipment upkeep.'),
        effects=dict(army_artillery_attack_factor=0.05, supply_consumption_factor=0.10, equipment_cost_multiplier_modifier=0.05),
        rewards=[
            reward('target_acquisition_teams', 'Target Acquisition Teams', 'Specialist teams combine observation and technical reports to locate firing positions.', dict(recon_factor=0.10)),
            reward('dispersed_gun_positions', 'Dispersed Gun Positions', 'Artillery units prepare dispersed positions and defensive arrangements for their guns.', {'category_artillery': {'defense': 0.15}}),
            reward('counterfire_control_centres', 'Counterfire Control Centres', 'Fire-control staffs collate reports and coordinate the artillery available for the mission.', dict(coordination_bonus=0.10)),
            reward('surveyed_fire_networks', 'Surveyed Fire Networks', 'Surveyed positions and established reporting procedures shorten the preparation of fire plans.', dict(planning_speed=0.10)),
            reward('integrated_target_plotting', 'Integrated Target Plotting', 'Common target plots link acquisition teams to the employment of the available artillery.', dict(army_artillery_attack_factor=0.15, recon_factor=0.10)),
        ],
        ai={'base': 2, 'countries': ['FIN', 'SWE', 'EGY', 'SAF'], 'country_weight': 7},
    ),
]

# IMPERIA COLD WAR — User-authorised stronger trade-offs over the original concept.
from balance_revision import apply_revision
apply_revision([*GRANDS, *SUBS])

# IMPERIA COLD WAR — User-requested foot/SF coverage, all artillery and early planning.
from coverage_revision import apply_expansion
apply_expansion([*GRANDS, *SUBS])
