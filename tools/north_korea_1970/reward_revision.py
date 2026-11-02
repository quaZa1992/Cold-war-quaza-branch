# IMPERIA COLD WAR — North Korea reward revision overlay.
"""Apply the authorized DPRK programme reward rebalance after all expansions.

This is deliberately an overlay on the computed design: it preserves IDs,
geometry, prerequisites, exclusions, leader identity and succession wiring.
Only the native reward bundle, its price, and related player-facing text are
changed here. Guarded building grants, limited-use technology bonuses and
focused equipment designer bonuses are emitted in both the focus Effects
preview and one-time executor.
"""

from copy import deepcopy


# Explicit field deltas are recorded for the post-overlay audit report. These
# are intentional changes to the implemented tree, not changes to its approved
# immutable snapshot.
REVISIONS = {
    "heavy_priority": {
        "description": "Concentrate scarce investment on steel, machine tools and heavy plant. The programme raises military production and factory ceilings, while reducing food productivity and increasing demand on the coal-powered grid.",
        "equipment": {"targets": {"artillery_equipment": {"build_cost_ic": -0.05},
                                    "medium_tank_chassis": {"build_cost_ic": -0.04}}},
    },
    "light_priority": {
        "description": "Direct the next plan toward farm equipment, food processing and household necessities. Higher harvests and civilian output relieve immediate shortages, while military production receives fewer inputs.",
        "cost_add": 0.00125,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "balanced_priority": {
        "description": "Set a measured programme for machine tools and broad industrial reliability. Modernized equipment supports balanced output, while additional inspection and maintenance slow construction.",
        "cost_add": 0.00125,
        "building": {"type": "industrial_complex", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 1200],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "steelworks": {
        "description": "Rebuild the steel and machine-building complex around dependable heavy presses and machine tools. New factory capacity gives the plan a concrete industrial base, but competing construction must wait.",
        "cost_add": 0.00375,
        "building": {"type": "arms_factory", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 601],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "food_district": {
        "description": "Equip cooperatives with tractors, threshers and food-processing capacity. More reliable harvest handling supports household supplies, while the expanded system requires fuel, spare parts and state procurement.",
        "cost_add": 0.0025,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "machine_tools": {
        "description": "Standardize machine tools and train maintenance teams at the plant level. Higher efficiency and technical training strengthen domestic engineering, while technical schools require continuing expenditure.",
        "research": {"category": "CAT_industry", "uses": 1, "bonus": 0.5},
    },
    "power_grid": {
        "description": "Coordinate repairs across transmission lines, substations and hydroelectric works. Better dispatch reduces wasted power, though repairs depend on imported components.",
        "research": {"category": "CAT_renewable_energy", "uses": 1, "bonus": 0.5},
    },
    "fertilizer": {
        "description": "Combine irrigation maintenance with fertilizer and mechanized field work. More dependable inputs raise farm productivity, while electrification adds to the grid's seasonal load.",
        "cost_add": 0.00125,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "technical_schools": {
        "description": "Expand polytechnic places for engineers, electricians and production technicians. Research and technical training improve industrial skills, at the cost of larger education budgets and laboratory expenses.",
        "research": {"category": "CAT_electronics", "uses": 1, "bonus": 0.5},
    },
    "lessons_1969": {
        "description": "Use the 1968-69 security crisis to revise command instruction and field procedures. Army experience improves, while professional training raises personnel costs.",
    },
    "munitions_directorate": {
        "description": "Give the munitions board responsibility for artillery specifications, ammunition lots and repair schedules. Standardized shells improve fire support, while stockpiles and production draw on civilian energy.",
        "equipment": {"targets": {"artillery_equipment": {"build_cost_ic": -0.05}}},
    },
    "artillery_works": {
        "description": "Expand the arsenal workshops for guns, shells and replacement barrels. The additional arms capacity and industrial output strengthen sustained fire support, while machinery and ammunition production increase grid demand.",
        "cost_add": 0.0025,
        "building": {"type": "arms_factory", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 601],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "kpa_engineer_corps": {
        "description": "Train sappers to prepare fieldworks, maintain bridges and restore roads under fire. Defensive readiness and supply efficiency improve, while central instruction adds to administrative costs.",
    },
    "kpa_command_schools": {
        "description": "Expand command schools for junior officers and staff planning. Army experience improves coordination, while instructor training and equipment increase education costs.",
    },
    "soviet_machine_standards": {
        "description": "Adopt Soviet machine-tool standards while training local inspectors to maintain imported equipment. Continued supply ties make the programme dependent on Soviet components.",
        "research": {"category": "CAT_industry", "uses": 1, "bonus": 0.5},
    },
    "three_revolutions": {
        "description": "Connect technical education, ideological campaigns and labour mobilization in the Three Revolutions Movement. Factory efficiency supports modernization, while a larger administrative apparatus raises operating costs.",
        "research": {"category": "CAT_electronics", "uses": 1, "bonus": 0.5},
    },
    "engineer_commissions": {
        "description": "Place engineering commissions in ministries and major plants to solve bottlenecks directly. Production ceilings rise at the cost of more centralized reporting.",
    },
    "cabinet_engineering_colleges": {
        "description": "Expand engineering colleges under the civilian cabinet and planning institutions. Laboratory equipment and tuition increase education costs.",
        "research": {"category": "CAT_electronics", "uses": 1, "bonus": 0.5},
    },
    "yanan_machine_repair": {
        "description": "Give plant-level repair teams authority to restore production equipment and adapt technical instructions to local conditions. A new civilian factory supports repair capacity, while less centralized reporting reduces direct plan control.",
        "cost_add": 0.00125,
        "building": {"type": "industrial_complex", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 1200],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "jongil_industrial_repair": {
        "description": "Restore idle machinery through repair depots and factory maintenance teams. Recovered capacity improves output before costly new plant is built, while the repaired equipment places additional strain on fuel and power supplies.",
        "cost_add": 0.00125,
        "building": {"type": "industrial_complex", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 1200],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "jongil_distribution": {
        "description": "Protect priority rations through staffed grain stores, local transport and farm inputs. A new agricultural district strengthens public food deliveries, while its fuel and maintenance needs deepen the continuing subsidy burden.",
        "cost_add": 0.0025,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "kdp_industrial_standards": {
        "description": "Standardize quality control and maintenance schedules across priority plants. More reliable production supports the civilian republic, while compliance checks limit managerial discretion.",
        "research": {"category": "CAT_industry", "uses": 1, "bonus": 0.5},
    },
    "chondo_cooperative_irrigation": {
        "description": "Pool labor and equipment through cooperative irrigation boards. A new agricultural district extends shared waterworks and raises yields, while its maintenance requires sustained state supervision and farm contributions.",
        "cost_add": 0.00125,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "chondo_granary": {
        "description": "Maintain staffed grain stores, seed reserves and local transport links through the cooperative system. Reserve stocks improve delivery reliability, while storage and distribution require continuing public expenditure.",
        "cost_add": 0.00125,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "mobile_army": {
        "description": "Build a mobile field army around motor transport and medium armour. Higher organization and planning support rapid concentration, while fuel, equipment and maintenance remain expensive.",
        "equipment": {"targets": {"medium_tank_chassis": {"build_cost_ic": -0.07}}},
    },
    "mass_artillery": {
        "description": "Concentrate artillery units and ammunition stocks along the principal approaches. Greater firepower strengthens prepared operations, while supply use and ammunition costs rise.",
        "equipment": {"targets": {"artillery_equipment": {"build_cost_ic": -0.05}}},
    },
    "ammunition_standards": {
        "description": "Standardize artillery ammunition and depot inspection across the KPA. Reliable fire support improves, although factory efficiency growth slows during the transition to common specifications.",
        "equipment": {"targets": {"artillery_equipment": {"build_cost_ic": -0.04}}},
    },
    "fighter_conversion": {
        "description": "Convert fighter units to standardized procedures and improve pilot conversion training. Fewer accidents and stronger air-superiority performance come at the cost of additional instructor and fuel requirements.",
        "equipment": {"targets": {"fighter": {"build_cost_ic": -0.07}}},
    },
    "dispersed_airfields": {
        "description": "Disperse fighter operations across auxiliary strips and improve ground servicing procedures. Aircraft availability improves, while dispersed basing slows civilian industrial construction.",
        "equipment": {"targets": {"fighter": {"build_cost_ic": -0.05}}},
    },
    "naval_workshops": {
        "description": "Equip coastal repair yards to service patrol craft, engines and naval aviation. The workshops support a stronger littoral force, while imported components and skilled labour raise programme costs.",
        "cost_add": 0.00125,
        "building": {"type": "dockyard", "levels": 1, "slots": 1,
                     "region": "owned coastal state", "state_ids": [601, 1199],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
        "equipment": {"targets": {"naval_bomber": {"build_cost_ic": -0.06}}},
    },
    "armour_mobility_drills": {
        "description": "Train mobile support groups to keep medium armour supplied on the move. Faster manoeuvre and better support improve operational reach, while fuel use remains higher.",
        "equipment": {"targets": {"medium_tank_chassis": {"build_cost_ic": -0.05}}},
    },
    "air_warning_network": {
        "description": "Connect coastal observers, air-defense commands and radar operators. Earlier warning improves interception, while stations require electricity, imported parts and specialist staff.",
        "cost_add": 0.00125,
        "building": {"type": "radar_station", "levels": 1, "slots": 1,
                     "region": "owned northern state", "state_ids": [601, 1200],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "cabinet_imported_generators": {
        "description": "Import generator sets and retain foreign technicians until local crews can maintain the plant. The power station raises dependable supply, while fuel demand and outside influence become more difficult to manage.",
        "cost_add": 0.0025,
        "building": {"type": "fossil_powerplant", "levels": 1, "slots": 1,
                     "region": "owned industrial state", "state_ids": [602, 601],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
    "christian_clinic_service": {
        "description": "Expand community clinics and train volunteer support staff alongside state physicians. Better local care reduces public health expenditure, while the service requires a larger administrative network.",
        "modifiers": {"health_cost_multiplier_modifier": -0.02},
    },
    "christian_welfare": {
        "description": "Extend community relief through clinics and locally administered welfare funds. Public health spending falls as care reaches more households, while welfare commitments continue to draw on the public budget.",
        "modifiers": {"health_cost_multiplier_modifier": 0.04},
    },
    "union_apprenticeships": {
        "description": "Create skilled apprenticeships for machinists, electricians and maintenance workers through factory committees. Education budgets grow to cover tools and instruction.",
        "research": {"category": "CAT_industry", "uses": 1, "bonus": 0.5},
    },
    "yanan_experts": {
        "description": "Invite returning technical cadres to adapt local repair methods and train workshop supervisors. Domestic expertise expands, while foreign contacts increase external influence exposure.",
        "equipment": {"targets": {"infantry_weapons_type": {"build_cost_ic": -0.05}}},
    },
    "kpa_maintenance_battalions": {
        "description": "Organize maintenance battalions to recover small arms, overhaul equipment and keep depots serviceable. Lower replacement costs come with additional personnel and instructor commitments.",
        "equipment": {"targets": {"infantry_weapons_type": {"build_cost_ic": -0.04}}},
    },
    "jongil_supply_commission": {
        "description": "Coordinate grain movement, depot repairs and priority deliveries through a standing supply commission. Food reliability improves, while administrators and transport crews increase ongoing costs.",
        "cost_add": 0.00125,
        "building": {"type": "agriculture_district", "levels": 1, "slots": 1,
                     "region": "owned agricultural state", "state_ids": [603, 602],
                     "slot_rule": "Add the stated number of shared slots, then the building, in the same selected state."},
    },
}


FOREIGN_REVISIONS = {
    "soviet_industry": {
        "nko": {"industrial_capacity_factory": 0.04},
        "description": "Negotiate Soviet machinery deliveries, power engineering and technical training. The protocol improves factory output and energy supply, while imported equipment, advisers and annual payments deepen technical dependence.",
    },
    "china_farm_supply": {
        "building": {"recipient": "NKO", "type": "agriculture_district", "levels": 1,
                     "slots": 1, "state_ids": [603, 602]},
        "description": "Secure regular grain, fertilizer and farm machinery deliveries through the Chinese frontier. Better harvest inputs and a new agricultural district ease supply pressure, while export concessions and procurement reliance reduce fiscal autonomy.",
    },
    "soviet_energy_projects": {
        "building": {"recipient": "NKO", "type": "fossil_powerplant", "levels": 1,
                     "slots": 1, "state_ids": [602, 1200]},
        "description": "Negotiate Soviet coal-power equipment, grid engineering and technician placements. A new power station and stronger generation support industrial recovery, while annual fees and imported components add to dependence on Moscow.",
    },
    "japan_fisheries": {
        "building": {"recipient": "NKO", "type": "dockyard", "levels": 1,
                     "slots": 1, "state_ids": [601, 1199]},
        "nko": {"agricolture_productivity_modifier": 0.06,
                "corporate_tax_income_multiplier_modifier": 0.02},
        "description": "Negotiate fishing equipment, vessel repair and commercial access with Japan. A new coastal dockyard supports fisheries and repair capacity, while supervision and unresolved political obligations make the agreement sensitive.",
    },
}


def apply(design):
    by_key = {node["key"]: node for node in design["nodes"]}
    if len(by_key) != len(design["nodes"]):
        raise ValueError("NKO reward overlay requires unique focus keys")
    for key, revision in REVISIONS.items():
        node = by_key[key]
        node["description"] = revision["description"]
        for modifier, value in revision.get("modifiers", {}).items():
            node["modifiers"][modifier] = value
        node["cost_gdp_share"] = round(node["cost_gdp_share"] + revision.get("cost_add", 0), 5)
        for kind in ("building", "research", "equipment"):
            if kind in revision:
                node["extra"].append({"kind": kind, **deepcopy(revision[kind])})
    agreements = {agreement["key"]: agreement for agreement in design["agreements"]}
    for key, revision in FOREIGN_REVISIONS.items():
        agreement = agreements[key]
        agreement["description"] = revision["description"]
        for modifier, value in revision.get("nko", {}).items():
            agreement["nko"]["modifiers"][modifier] = value
        if "building" in revision:
            agreement.setdefault("buildings", []).append(deepcopy(revision["building"]))
    for node in design["nodes"]:
        offer = next((effect for effect in node["extra"] if effect["kind"] == "agreement"), None)
        if offer and offer["agreement"] in FOREIGN_REVISIONS and offer["stage"] == "base":
            node["description"] = agreements[offer["agreement"]]["description"]
    design["reward_revision"] = {
        "project": "IMPERIA COLD WAR",
        "id": "NKO_REWARD_REWORK_20261027",
        "focus_count": len(REVISIONS),
        "focus_keys": list(REVISIONS),
        "foreign_agreements": list(FOREIGN_REVISIONS),
        "geometry_or_graph_changes": False,
    }
    return design
