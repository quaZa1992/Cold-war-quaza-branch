# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""Authored English narratives for the generic 1970 military programme.

Only descriptions change. Numeric rewards and their conditions remain in the
native focus effects. Apply after old_loc_transform when rebuilding base loc.
"""
import re


NARRATIVES = {
    'GEN_1970_space_research_institute_desc':
        "A permanent research institute will bring mathematicians, engineers and communications specialists into one organisation. Its laboratories can investigate the instruments and launch systems on which a space programme depends. Ambition alone will not put a satellite in orbit; a dependable scientific establishment must come first.",
    'GEN_1970_industrial_research_task_forces_desc':
        "Factory managers and university researchers too often work on different problems. Joint technical teams will take laboratory methods onto the shop floor, where they can be tested against actual materials, machinery and production schedules. Industry needs research that survives contact with an operating plant.",
    'GEN_1970_domestic_vehicle_research_desc':
        "Imported vehicles arrive with answers to someone else's requirements. A domestic research team will examine the protection, mobility and maintenance needs of our own forces and prepare designs around them. Establishing that engineering knowledge is the first step towards a credible armoured-vehicle industry.",
    'GEN_1970_domestic_naval_research_desc':
        "The fleet requires engineers who understand both the sea and the workshops ashore. A naval research programme will examine hulls, propulsion and weapons as parts of a single vessel. Its purpose is to develop designs that our yards and crews can realistically build, maintain and operate.",
    'GEN_1970_domestic_aircraft_research_desc':
        "An aircraft programme needs more than a promising airframe. Engines, instruments and weapons must function together, and test pilots must be able to explain a design's shortcomings to its engineers. Bringing this work into a domestic research organisation will give our air service a more informed voice in future development.",
    'GEN_1970_atomic_research_programme_desc':
        "Atomic research requires specialised laboratories, trained physicists and a government prepared to sustain their work beyond a single experiment. Establishing that foundation will let us investigate the technologies of the nuclear age. Research is a necessary beginning; it is not a substitute for the facilities and further development that follow.",
    'GEN_1970_military_emergency_desc':
        "A worsening security situation has exposed weaknesses that routine peacetime administration could leave unanswered. Army and air-service staffs will review readiness, compare contingency plans and pass practical lessons to their commanders. The immediate task is to make the forces already available more capable of responding together.",
    'GEN_1970_army_reform_desc':
        "The army's establishment, training commitments and budget must describe the same force. A general reform will give commanders the resources and authority to address weaknesses uncovered in service. It also obliges the government to support its military ambitions with a larger spending commitment.",
    'GEN_1970_mass_conscript_army_desc':
        "A broad conscription system can keep formations manned without paying every soldier as a career professional. Training depots must therefore prepare successive intakes quickly and consistently. This course builds an army around the ability to mobilise large numbers, making the organisation of national service a central military responsibility.",
    'GEN_1970_professional_volunteer_force_desc':
        "Long-serving volunteers allow units to retain trained personnel and develop habits of coordinated action. Recruiting and keeping those soldiers will cost more than relying on short-term conscripts, while drawing on a smaller manpower base. The government will accept that expense in exchange for a more cohesive and experienced standing force.",
    'GEN_1970_territorial_defence_force_desc':
        "Local defence formations will prepare to fight on ground their members know. Their organisation must connect mobilisation, stores and defensive planning rather than depend on an improvised response after an invasion begins. This is a commitment to resisting an enemy at home, with the population contributing directly to national defence.",
    'GEN_1970_land_doctrine_innovations_desc':
        "Staff officers will review how our formations move, concentrate fire and communicate under pressure. The aim is to turn practical lessons into a common method that commanders can understand and exercise. Doctrine must guide the employment of the army we possess, rather than remain a collection of borrowed manuals.",
    'GEN_1970_large_scale_manoeuvres_desc':
        "A divisional exercise reveals failures that a headquarters map cannot. Supply columns miss their timings, radio nets become congested and commanders must make decisions with incomplete reports. Large manoeuvres will expose these weaknesses before an enemy does and give the army a shared body of practical experience.",
    'GEN_1970_military_education_reform_desc':
        "Promotion and seniority alone cannot prepare an officer to command modern formations. Military schools will place greater emphasis on staff work, combined operations and the critical study of recent exercises. Serving commanders will take part in this reform so that changes in the classroom also reach the field army.",
    'GEN_1970_arms_procurement_policy_desc':
        "The armed services need a clear answer about where their next generation of equipment will come from. Overseas purchases and domestic manufacture make different demands on the treasury, industry and relations with suppliers. A settled procurement policy will give the government a basis for choosing between those commitments.",
    'GEN_1970_infantry_equipment_development_desc':
        "Small arms are issued in numbers that make reliability and ease of manufacture as important as an impressive prototype. Infantry trials will bring soldiers and manufacturers together to improve the weapons they handle every day. Production preparations must accompany research if new designs are to become practical service equipment.",
    'GEN_1970_land_doctrine_expertise_desc':
        "The first reform produces instructions; repeated application produces judgement. Experienced officers will examine the use of our weapons and formations together, identifying which methods deserve to become established practice. The resulting expertise will help the army turn its chosen doctrine into dependable performance.",
    'GEN_1970_artillery_experiments_desc':
        "An artillery battery is useful only when observers, gun crews and ammunition services can work to the same plan. Trials of towed artillery will examine fire control, handling and the practical demands of keeping guns in action. Better designs must answer the needs of the crews who will serve them.",
    'GEN_1970_buy_abroad_desc':
        "Established foreign manufacturers offer a route to equipment that our own industry cannot yet supply. A concentrated import effort will improve the terms under which the armed forces buy abroad. It commits procurement to external suppliers for this period, rather than immediately creating a domestic manufacturing base.",
    'GEN_1970_build_it_ourselves_desc':
        "Domestic arms manufacture requires workshops, skilled workers and designs that can be produced consistently. Investment in a military factory will give the research programme somewhere to put its results into practice. The initial expense buys an industrial capability that overseas deliveries cannot establish on their own.",
    'GEN_1970_uniform_improvements_desc':
        "Clothing and personal protection must suit the conditions in which our soldiers actually serve. Trials of camouflage and body armour will compare protection with weight, wear and freedom of movement. Equipment that survives a demonstration but exhausts its wearer on a march is no improvement at all.",
    'GEN_1970_utility_vehicles_desc':
        "An army's mobility rests on ordinary vehicles as much as on its fighting machines. Research into utility vehicles will address the movement of men, stores and specialist teams over the routes available to them. Maintenance access and dependable service matter as much as performance on a test track.",
    'GEN_1970_self_propelled_artillery_desc':
        "Fast-moving formations cannot always wait for guns to be unlimbered, brought into action and towed forward again. A programme for self-propelled artillery will investigate how to keep supporting fire close to the advance. Mobility, crew protection and ammunition handling must be developed as a complete system.",
    'GEN_1970_develop_armour_prototypes_desc':
        "Before the army commits itself to a new armoured vehicle, engineers must prove how its protection, armament and running gear work together. Prototype trials will give designers evidence that drawings alone cannot supply. The programme will establish a stronger technical foundation for subsequent armoured development.",
    'GEN_1970_special_forces_training_desc':
        "Special operations depend on preparation across service boundaries. Selected personnel will train for missions that require unusual equipment, careful planning and cooperation between ground, sea and air elements. Selected units will rehearse their tasks together until their commanders can rely on the preparation of the whole force.",
    'GEN_1970_self_propelled_anti_air_desc':
        "The protection of advancing columns cannot depend entirely on fixed batteries far behind them. Research into mobile air-defence vehicles will examine weapons that can accompany the formations they defend. Crews need systems that combine a useful field of fire with the mobility and support arrangements of the field army.",
    'GEN_1970_anti_tank_guided_missiles_desc':
        "Guided anti-tank weapons offer infantry and specialist teams another means of engaging armour. Their value depends on more than the missile itself: sights, launchers and the demands placed on the operator must be considered together. Development trials will establish equipment that our troops can realistically employ.",
    'GEN_1970_helicopter_mobility_desc':
        "Transport helicopters can connect troops with positions that roads do not readily serve. Research must address the aircraft, loading arrangements and support requirements that make such movement dependable. The army will investigate a practical transport capability, recognising that carrying men into a position is only the beginning of sustaining them there.",
    'GEN_1970_rangers_and_light_infantry_desc':
        "Some missions reward disciplined movement and specialist fieldcraft more than heavy equipment. Ranger and light-infantry training will prepare selected troops to operate effectively where ordinary formations struggle to concentrate. Their advantage must come from preparation and a clear tactical purpose, not from being treated as expendable infantry.",
    'GEN_1970_specialised_mechanised_battalions_desc':
        "Mechanised infantry must exploit its vehicles without becoming dependent on remaining inside them. Specialist battalion training will concentrate on the cooperation of mounted movement, dismounted assault and supporting fire. These units will develop the skills needed to turn armoured mobility into effective offensive action.",
    'GEN_1970_main_battle_tank_programme_desc':
        "A main battle tank will influence procurement, maintenance and training for many years. A funded research programme will examine designs that can meet our army's requirements without ignoring what industry can support. Prototype trials and industrial preparation will give procurement officers a firmer basis for choosing the next service tank.",
    'GEN_1970_air_cavalry_doctrine_desc':
        "Attack helicopters require more than new aircraft. Pilots, forward controllers and ground formations must learn to operate as a single force. Dedicated training and development programmes will turn scattered experiments into a dependable battlefield capability, while placing new demands on maintenance and technical education.",
    'GEN_1970_air_force_reform_desc':
        "Modern aircraft will achieve little if the air service cannot organise their employment. A reform of training, staff work and technical development will bring operational requirements into closer contact with research. The aim is an air force capable of learning from experience and directing the next stage of its development.",
    'GEN_1970_jet_fighter_programme_desc':
        "Fighter development must reconcile speed, endurance, weapons and the ability to bring an aircraft home after a demanding sortie. Our engineers will investigate a new generation of combat aircraft around the missions the air force expects to fly. A coherent development effort offers more than isolated purchases of promising components.",
    'GEN_1970_air_doctrine_innovations_desc':
        "Air operations need an agreed method for choosing targets, assigning aircraft and coordinating sorties. Staff exercises and operational reviews will turn competing service ideas into a doctrine that can be practised. The aircraft available to us must shape that method, rather than an imagined fleet we cannot yet field.",
    'GEN_1970_capital_defence_scheme_desc':
        "The seat of government and its surrounding infrastructure present an obvious target for air attack. A capital-defence scheme will strengthen the available ground defences and guide the development of the weapons needed to protect them. Where the capital cannot accommodate another installation, the wider defensive network must carry the investment.",
    'GEN_1970_strategic_bomber_force_desc':
        "Long-range bombing demands aircraft designed around a difficult combination of range, payload and survival. A funded heavy-aircraft programme will examine how such a force could serve our strategic requirements. This is a major development commitment whose eventual value depends on the support and planning built around the aircraft.",
    'GEN_1970_tactical_air_power_desc':
        "Battlefield aviation must answer the ground commander's needs without losing the coordination of the air service. Research into light aircraft and air-to-ground weapons will support that relationship. The task is to develop machines and armament suited to practical attacks on the targets our forces are likely to face.",
    'GEN_1970_countermeasures_against_aircraft_desc':
        "The threat from hostile aircraft requires an answer at more than one level. Development of anti-aircraft weapons will improve the technical foundation of our defences, while suitable installations can extend their reach. The programme will concentrate on equipment that fits the defensive systems we are able to operate.",
    'GEN_1970_surface_to_air_missile_belt_desc':
        "Isolated batteries leave gaps that an attacker can exploit. A wider air-defence belt will combine additional installations with the development of missile equipment for their crews. Its purpose is to protect important areas through a network of positions, rather than place all confidence in a single defended point.",
    'GEN_1970_air_base_expansion_desc':
        "Flying units need more than a strip of usable ground. An air-base expansion will provide additional capacity for the aircraft and support personnel that must operate from it. The location must suit our territory and the practical demands of keeping a military airfield in service.",
    'GEN_1970_air_doctrine_expertise_desc':
        "The air service must retain the lessons gained by its most experienced crews and staffs. Reviews of exercises and operations will turn those lessons into methods that new formations can also apply. A doctrine becomes useful when commanders can exercise judgement within it, rather than merely repeat its terminology.",
    'GEN_1970_integrated_air_defence_desc':
        "Warning and interception must form part of the same defensive plan. Radar coverage will help identify an approaching threat, while additional ground defences give the network a means to answer it. Investing in both elements will establish a more coherent structure for the protection of our airspace.",
    'GEN_1970_air_base_expansion_two_desc':
        "The next stage of air-base development will be accompanied by a sustained commitment to the aircraft sector. Additional operating capacity must be matched by investment in the organisation that equips it. This programme joins physical expansion to a longer period of support for the air service's material needs.",
    'GEN_1970_airborne_early_warning_desc':
        "Ground stations cannot provide the best warning in every direction and at every height. Research into airborne early-warning aircraft will investigate how a mobile observation platform can extend the information available to commanders. The equipment must serve an organised reporting system if its additional reach is to be useful.",
    'GEN_1970_paratrooper_corps_desc':
        "An airborne formation must remain organised after the disruption of a landing. A dedicated paratrooper corps will establish the training and service cooperation needed to recover cohesion and act promptly on the ground. Its value depends on disciplined preparation, suitable missions and a clear understanding of the risks involved.",
    'GEN_1970_naval_reform_desc':
        "The navy's ships, shore establishment and operational doctrine must develop together. A general reform will use fleet experience to guide staff work and the technical study of future vessels. Maritime industry will have a part in the programme, because a fleet cannot be sustained by decisions made at sea alone.",
    'GEN_1970_merchant_marine_desc':
        "Commercial shipping depends on ships that can be built and replaced at an affordable cost. A merchant-marine programme will encourage more economical convoy construction and give the maritime sector a clearer industrial objective. Keeping civilian sea transport viable is a practical foundation for the nation's wider maritime interests.",
    'GEN_1970_naval_bases_desc':
        "A fleet's operating area is constrained by the ports that can support it. Investment in naval-base capacity will give ships a stronger foothold along our coast. Stores, workshops and shore services will have to support the additional berthing capacity throughout its service.",
    'GEN_1970_naval_doctrine_innovations_desc':
        "The fleet must decide how its ships will support one another before they meet an enemy. Exercises and staff studies will examine formations, command arrangements and the employment of available weapons. Those lessons will provide a stronger basis for the navy's chosen operational doctrine.",
    'GEN_1970_blue_water_navy_desc':
        "Operations beyond the immediate coast place demanding requirements on escorts and larger surface combatants. Research into destroyers and cruisers will investigate the vessels needed for that ambition. The aim is to develop a credible ocean-going fleet, beginning with designs that can undertake useful missions together.",
    'GEN_1970_coastal_defence_fleet_desc':
        "Our first maritime task may be to make nearby waters difficult for an enemy to use. Development of smaller combatants and anti-ship missiles will support a fleet organised around that purpose. A coastal strategy allows limited resources to be concentrated on the approaches that matter most to national defence.",
    'GEN_1970_dockyards_desc':
        "Naval plans cannot advance faster than the yards that build their ships. An expansion of dockyard capacity will strengthen the industrial foundation of the fleet, with the scale of construction matched to the economy. Maritime employers will gain orders, while the state accepts the expense of developing the facilities.",
    'GEN_1970_submarine_arm_desc':
        "A submarine service requires specialised engineering and a careful understanding of the missions assigned to it. Research will examine boats that can meet those requirements within the fleet's means. Building the necessary technical knowledge is more valuable than ordering a prestigious design without knowing how it will be supported.",
    'GEN_1970_naval_doctrine_expertise_desc':
        "Fleet experience should outlast the appointments of individual commanders. The naval staff will collect lessons from exercises and service, testing which methods can be relied upon across different formations. This body of expertise will help officers employ their chosen doctrine with greater confidence and consistency.",
    'GEN_1970_aircraft_carriers_desc':
        "A carrier programme begins with difficult questions about the ship, its aircraft and the work of operating them at sea. Research into carrier design will establish the technical knowledge needed to answer those questions. Naval architects, aviators and engineers will have to agree on a design that the fleet can operate and its shore establishment can support.",
    'GEN_1970_helicopter_carriers_desc':
        "A ship designed to operate helicopters offers the fleet a different set of possibilities from a conventional surface combatant. Development work will examine its flight arrangements, support spaces and intended naval role. The design must fit a useful mission before the government commits itself to building it.",
    'GEN_1970_missile_boat_squadrons_desc':
        "Small missile-armed combatants need suitable weapons and an industry able to produce the boats around them. This programme will support both technical development and a period of focused yard activity. The objective is a practical squadron concept whose vessels can operate together in the waters assigned to them.",
    'GEN_1970_vessel_production_desc':
        "The shipbuilding industry will receive a sustained production commitment rather than a succession of disconnected orders. Better coordination of yard schedules and suppliers will support that effort over the coming years. Stable orders will give suppliers and yard managers the confidence to organise work beyond the next individual contract.",
    'GEN_1970_nuclear_submarines_desc':
        "A nuclear-submarine programme demands specialised research and an operational purpose that justifies the effort. Naval engineers will investigate the boats and supporting systems required for extended submerged operations. The studies must also inform the doctrine under which these vessels would eventually serve.",
    'GEN_1970_large_ship_drydocks_desc':
        "Large warships require facilities able to accommodate their construction and heavy work. A further dockyard investment will strengthen that part of the maritime establishment. It gives future building plans a more credible industrial basis, while making a tangible commitment of public resources to the fleet.",
    'GEN_1970_sea_based_deterrent_desc':
        "A deterrent carried at sea depends on a boat, missile system and command arrangement that can function as one. Research into missile submarines will address the vessel component of that undertaking. The programme develops a possible means of delivery; the wider strategic capability still requires its own preparation.",
    'GEN_1970_establish_a_marine_corps_desc':
        "Landing troops from the sea calls for an organisation that trains for the operation as a whole. A marine corps will connect the assault ashore with the naval planning needed to put it there. Its formation will give amphibious operations a permanent institutional home within the armed forces.",
    'GEN_1970_improved_repair_facilities_desc':
        "Damage need not remove a useful ship from service longer than its repair work requires. A focused programme for repair facilities will improve the ability to return vessels to the fleet. Workshops, scheduling and specialised support deserve attention alongside the more conspicuous business of constructing new warships.",
}


def apply_narratives(text):
    """Replace each authored key exactly once; retain all other localisation."""
    for key, description in NARRATIVES.items():
        pattern = r'(?m)^(\s*' + re.escape(key) + r':\d*\s*)".*"\s*$'
        text, count = re.subn(pattern, lambda m: m[1]+'"'+description.replace('"','\\"')+'"', text)
        if count != 1:
            raise ValueError(f'Expected one localisation entry for {key}; got {count}')
    return text
