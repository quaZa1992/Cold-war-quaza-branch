# IMPERIA CW — Cold War: North Korea 1970 reciprocal patron programmes.
"""Add consent-based PRC and Soviet branches to the NKO 1970 design model."""
from copy import deepcopy


AGREEMENT_KEYS = (
    "china_industrial_exchange",
    "china_farm_supply",
    "china_staff_training",
    "soviet_energy_projects",
    "soviet_fuel_contract",
    "soviet_staff_training",
)


def _agreement(base, key, partner, title, description, nko_spirit,
               recipient_spirit, nko_description, recipient_description,
               nko_modifiers, recipient_modifiers, nko_setup, recipient_setup,
               nko_annual, recipient_annual, provenance, building=None):
    """Clone the established bilateral schema and replace all identity fields."""
    item = deepcopy(base)
    item.update(
        id="COLDWAR_NKO_" + key,
        key=key,
        partner=partner,
        title=title,
        description=description,
        recipient_decision="Consider " + title,
        accept="Accept the Agreement",
        decline="Decline the Proposal",
        pending_days=90,
        perpetual=True,
        party_bound=False,
        resubmission=(
            "After refusal or expiry, a sender decision may reopen a completed "
            "focus proposal with fresh GDP quotes; no repeat completed-focus reward."
        ),
        conditions=[
            "Both countries exist.",
            "Both countries have accepted the agreement.",
            "Neither country is at war with the other.",
            "Neither country imposes diplomatic, financial, economic or military sanctions on the other.",
        ],
        provenance=provenance,
        buildings=[deepcopy(building)] if building else [],
        upgrades=[],
        spirit_descriptions=[nko_description, recipient_description],
    )
    item["nko"] = {
        "spirit": nko_spirit,
        "modifiers": dict(nko_modifiers),
        "setup_gdp_share": nko_setup,
        "annual_commitment_gdp_share": nko_annual,
        "weekly_formula": "current GDP × annual commitment ÷ 52",
    }
    item["recipient"] = {
        "spirit": recipient_spirit,
        "modifiers": dict(recipient_modifiers),
        "setup_gdp_share": recipient_setup,
        "annual_commitment_gdp_share": recipient_annual,
        "weekly_formula": "current GDP × annual commitment ÷ 52",
    }
    item["receipts"] = {
        "accepted": "COLDWAR_NKO_" + key + "_accepted",
        "initial_grant": "COLDWAR_NKO_" + key + "_initial_grant_applied",
        "pending": "COLDWAR_NKO_" + key + "_pending",
        "quote": "Saved payer-specific setup amounts; validity checked again on acceptance.",
        "rule": (
            "Accepted and initial-grant receipts are immutable and shared on both tags. "
            "Reconciliation never repeats a setup fee, building, slots or one-time grant. "
            "Pending state is cleared on accept, decline, expiry or invalidation."
        ),
    }
    return item


def _focus(add, group, key, title, x, y, prerequisites, modifiers, price,
           icon, description, *, agreement=None, required=(), mutex=(),
           requirements=(), long_cost=False):
    extra = []
    if agreement:
        extra.append({
            "kind": "agreement",
            "agreement": agreement,
            "stage": "base",
        })
    node = add(
        group, key, title, x, y, prerequisites, modifiers, price, icon,
        description, mutex=mutex, extra=extra, requirements=list(requirements),
    )
    if required:
        node["required_agreements"] = list(required)
    if long_cost:
        node["days"] = 49
        node["cost"] = 7
    return node


def extend(d, add):
    """Append exactly 16 PRC and 16 Soviet focuses plus six agreements."""
    groups = {g["id"]: g for g in d["groups"]}
    china = {
        "id": "china",
        "title": "China: Frontier and Technical Cooperation",
        "x": 54,
        "y": 12,
        "slot": None,
        "status": "Recipient-controlled bilateral alternatives",
        "icon": "trade",
        "note": "Build on the accepted border protocol; each new exchange needs both governments' consent.",
    }
    soviet = {
        "id": "soviet",
        "title": "Soviet Union: Industry and Security",
        "x": 70,
        "y": 12,
        "slot": None,
        "status": "Recipient-controlled bilateral alternatives",
        "icon": "economic_civil_industry",
        "note": "Build on the accepted industrial protocol; each new exchange needs both governments' consent.",
    }
    d["groups"].extend([china, soviet])
    base = {a["key"]: a for a in d["agreements"]}
    border = base["china_border"]
    industry = base["soviet_industry"]

    industrial_building = {
        "recipient": "NKO",
        "type": "industrial_complex",
        "levels": 1,
        "slots": 1,
        "state_ids": [602, 1200],
    }
    agreements = [
        _agreement(
            border, "china_industrial_exchange", "CHI",
            "Sino-Korean Industrial Exchange",
            "Arrange machine-tool, quality-control and engineering cooperation. Better factory performance supports domestic production, while imported standards and specialist access increase dependence.",
            "Industrial Standards and Engineering Exchange",
            "Korean Industrial Procurement",
            "Chinese machine-tool standards and engineering placements improve factory performance. Imported components and continued specialist access limit procurement autonomy.",
            "Industrial orders and technical placements expand Chinese commercial access. Training and servicing obligations require additional staff.",
            {"productivity_growth_modifier": 0.04, "production_factory_max_efficiency_factor": 0.05,
             "foreign_influence_defense_modifier": -0.04, "education_cost_multiplier_modifier": 0.025},
            {"trade_opinion_factor": 0.05, "corporate_tax_income_multiplier_modifier": 0.02,
             "bureaucracy_cost_multiplier_modifier": 0.02},
            0.0125, 0.00075, 0.00125, 0.0003,
            ["1961 PRC–DPRK Treaty, economic and technical cooperation clause",
             "CIA, North Korea: Jet Fighter Production (April 1984), on assessed Chinese technical aid"],
            industrial_building,
        ),
        _agreement(
            border, "china_farm_supply", "CHI",
            "Frontier Agricultural Supply Compact",
            "Arrange reciprocal farm-input and border-supply schedules. Fertilizer, machinery and reliable transport would support cultivation, while export commitments and external dependence narrow local choices.",
            "Frontier Farm Inputs and Distribution",
            "Korean Mineral and Agricultural Exchange",
            "Agreed farm inputs and transport schedules support cultivation and border distribution. Export obligations and administrative supervision reduce room for local priorities.",
            "Regular commodity deliveries and border commerce support Chinese trade. Customs staffing and supply coordination require continuing resources.",
            {"agricolture_productivity_modifier": 0.06, "supply_consumption_factor": -0.03,
             "tax_gain_multiplier_modifier": -0.02, "foreign_influence_defense_modifier": -0.03},
            {"trade_opinion_factor": 0.04, "resource_export_multiplier_modifier": 0.02,
             "bureaucracy_cost_multiplier_modifier": 0.015},
            0.00875, 0.0005, 0.001, 0.00025,
            ["1961 PRC–DPRK Treaty, Article 5 on economic and technical aid",
             "Contemporary 1970s trade and aid context; proposed sectoral schedule is alternate history"],
        ),
        _agreement(
            border, "china_staff_training", "CHI",
            "Korean-Chinese Staff and Maintenance Exchange",
            "Offer reciprocal specialist courses in air defence, aircraft maintenance and command procedure. Better-trained staffs improve readiness, but instructors, imported spares and repeated exercises draw on scarce resources.",
            "Air Defence Staff and Maintenance Courses",
            "Korean-Chinese Military Technical Exchange",
            "Chinese instructors support air-defence and maintenance courses; Korean officers share selected operational experience. The programme raises training and personnel costs.",
            "Korean technical placements and reciprocal staff study broaden Chinese military experience. Adviser time and training facilities carry a continuing cost.",
            {"experience_gain_army": 0.035, "army_attack_factor": 0.015,
             "education_cost_multiplier_modifier": 0.04, "army_personnel_cost_multiplier_modifier": 0.03},
            {"experience_gain_army": 0.015, "trade_opinion_factor": 0.04,
             "education_cost_multiplier_modifier": 0.02},
            0.0075, 0.0004, 0.00075, 0.0002,
            ["1961 PRC–DPRK mutual-assistance treaty",
             "CIA, North Korea: Jet Fighter Production (April 1984), on F-6 support and overhaul",
             "Proposed reciprocal staff programme; recurring joint exercises are not verified"],
        ),
        _agreement(
            industry, "soviet_energy_projects", "SOV",
            "Soviet Power and Engineering Projects",
            "Extend power engineering, machinery deliveries and technical placements to priority plants. Reliable equipment and specialist support raise output, while credit, imported parts and outside influence carry a cost.",
            "Power Engineering and Industrial Modernization",
            "Soviet Engineering and Machinery Programme",
            "Soviet equipment and technical placements support power generation and industrial reliability. Import dependence and ongoing commitments reduce independent planning.",
            "Machinery orders, training placements and engineering contracts support Soviet industry and influence. Specialist dispatch and servicing obligations require resources.",
            {"fossil_pp_energy_generation_modifier": 0.06, "production_factory_max_efficiency_factor": 0.05,
             "productivity_growth_modifier": 0.04, "foreign_influence_defense_modifier": -0.04},
            {"corporate_tax_income_multiplier_modifier": 0.02, "foreign_influence_modifier": 0.03,
             "education_cost_multiplier_modifier": 0.02},
            0.015, 0.001, 0.0015, 0.0004,
            ["1961 USSR–DPRK Treaty, Article 4",
             "Soviet MFA Far East Department report on 1968 industrial projects and specialists"],
            industrial_building,
        ),
        _agreement(
            industry, "soviet_fuel_contract", "SOV",
            "Soviet Fuel and Transport Schedule",
            "Negotiate a measured oil and rail-input schedule against North Korean exports. More dependable supplies ease industrial bottlenecks, while repayment, delivery targets and fuel dependence constrain policy.",
            "Fuel, Rail and Export Settlement",
            "Soviet-Korean Trade and Transport Schedule",
            "Scheduled fuel and rail inputs ease production bottlenecks. Export repayment and administrative commitments leave less room for domestic allocation.",
            "Regular mineral and manufactured imports support Soviet trade. Contract monitoring and credit exposure require additional administration.",
            {"productivity_growth_modifier": 0.035, "supply_consumption_factor": -0.03,
             "tax_gain_multiplier_modifier": -0.025, "foreign_influence_defense_modifier": -0.025},
            {"trade_opinion_factor": 0.04, "corporate_tax_income_multiplier_modifier": 0.02,
             "bureaucracy_cost_multiplier_modifier": 0.02},
            0.01, 0.0006, 0.0015, 0.00035,
            ["Russian federal-archives bulletin, 1971–75 and 1976–80 trade plans; 1972 debt deferment",
             "CIA, Soviet-North Korean Relations in the 1980s (June 1984), on export-paid oil and loan terms"],
        ),
        _agreement(
            industry, "soviet_staff_training", "SOV",
            "Soviet Air Defence and Staff Exchange",
            "Arrange reciprocal staff courses in air defence, logistics and command procedure. Specialist access can improve readiness and coordination, while imported systems, fuel and adviser commitments increase costs.",
            "Air Defence and Command Staff Exchange",
            "Soviet-Korean Security Cooperation",
            "Soviet staff instruction supports air-defence planning and logistics. Foreign standards and specialist missions bring continuing costs and influence.",
            "Korean observers and reciprocal technical study support Soviet regional experience. Training and adviser access draw on personnel and facilities.",
            {"army_attack_factor": 0.025, "experience_gain_army": 0.025,
             "army_personnel_cost_multiplier_modifier": 0.035,
             "foreign_influence_defense_modifier": -0.03},
            {"experience_gain_army": 0.015, "trade_opinion_factor": 0.04,
             "army_personnel_cost_multiplier_modifier": 0.02},
            0.01, 0.0007, 0.001, 0.00025,
            ["1961 USSR–DPRK mutual-assistance treaty",
             "CIA, North Korea: New Weapons in the Military Forces (October 1985), on MiG-23 and SA-3 deliveries",
             "Proposed reciprocal staff programme; recurring joint exercises are not verified"],
        ),
    ]
    d["agreements"].extend(agreements)

    # China: each policy stage is available only while its actual bilateral
    # agreement is active on both endpoints. The branch does not compel a
    # choice between Beijing, Moscow, or an independent course.
    _focus(add, china, "china_partnership", "The Yalu Partnership", 54, 12, [],
           {"productivity_growth_modifier": 0.025, "supply_consumption_factor": -0.02,
            "foreign_influence_defense_modifier": -0.025}, 0.0075, "trade",
           "Build a practical partnership around the accepted frontier protocol. Better supplies and production support national plans, while deeper exchange gives Beijing greater influence.",
           required=("china_border",),
           requirements=("The Border Cooperation Protocol is active.",))
    _focus(add, china, "china_industrial_protocol", "Industrial Exchange", 52, 14,
           [["china_partnership"]], {}, 0.01, "economic_civil_industry",
           "Invite Chinese engineers to advise on machine tools, production standards and factory maintenance. Industrial cooperation can improve output, while imported components and access arrangements limit autonomy.",
           agreement="china_industrial_exchange", required=("china_border",),
           requirements=("The Border Cooperation Protocol is active.",))
    _focus(add, china, "china_agricultural_protocol", "Farm Supply Compact", 56, 14,
           [["china_partnership"]], {}, 0.00875, "agriculture",
           "Negotiate a reciprocal schedule for farm machinery, fertilizer and frontier transport. More dependable rural inputs support harvest planning, while exports and customs obligations must be met.",
           agreement="china_farm_supply", required=("china_border",),
           requirements=("The Border Cooperation Protocol is active.",))
    _focus(add, china, "china_factory_accounts", "Factory Accounts", 52, 16,
           [["china_industrial_protocol"]], {"production_factory_max_efficiency_factor": 0.04,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.0075, "parliament_box",
           "Require enterprises receiving imported machine tools to report output, repairs and replacement needs. Better oversight protects investment, while accounting expands the administrative burden.",
           required=("china_industrial_exchange",),
           requirements=("The Industrial Exchange is active.",))
    _focus(add, china, "china_machine_teams", "Machine Repair Teams", 50, 17,
           [["china_factory_accounts"]], {"production_factory_efficiency_gain_factor": 0.05,
            "education_cost_multiplier_modifier": 0.03}, 0.00875, "economic_civil_industry",
           "Train plant teams to repair and calibrate machine tools supplied under the exchange. More reliable equipment supports production, while technical instruction competes for skilled labour.",
           required=("china_industrial_exchange",),
           requirements=("The Industrial Exchange is active.",))
    _focus(add, china, "china_engineering_colleges", "Engineering Courses", 54, 17,
           [["china_factory_accounts"]], {"research_speed_factor": 0.03,
            "education_cost_multiplier_modifier": 0.05}, 0.00875, "education_reform",
           "Expand applied engineering courses linked to imported equipment and local production. Technical capacity can improve adaptation, at the cost of classrooms, instructors and time away from industry.",
           required=("china_industrial_exchange",),
           requirements=("The Industrial Exchange is active.",))
    _focus(add, china, "china_farm_machinery", "Farm Service", 56, 16,
           [["china_agricultural_protocol"]], {"agricolture_productivity_modifier": 0.05,
            "production_speed_agriculture_district_factor": 0.03,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.00875, "agriculture",
           "Coordinate machinery repair and seasonal delivery through provincial farm offices. Better service supports cultivation, while transport, replacement parts and local supervision absorb resources.",
           required=("china_farm_supply",),
           requirements=("The Frontier Agricultural Supply Compact is active.",))
    _focus(add, china, "china_harvest_reserves", "Harvest Reserves", 58, 17,
           [["china_farm_machinery"]], {"agricolture_productivity_modifier": 0.04,
            "stability_factor": 0.03, "tax_gain_multiplier_modifier": -0.025}, 0.0075, "NKO_food",
           "Retain limited grain and seed reserves to stabilize provincial distribution after poor harvests. More dependable stores can ease rural pressure, while guarantees reduce receipts to the central budget.",
           required=("china_farm_supply",),
           requirements=("The Frontier Agricultural Supply Compact is active.",))
    _focus(add, china, "china_border_rail", "Frontier Freight", 56, 18,
           [["china_farm_machinery"]], {"supply_consumption_factor": -0.03,
            "production_speed_industrial_complex_factor": 0.03,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.00875, "trade",
           "Coordinate freight priorities at agreed frontier crossings. More regular deliveries support industry and farms, while customs administration and export commitments grow.",
           required=("china_farm_supply",),
           requirements=("The Frontier Agricultural Supply Compact is active.",))
    _focus(add, china, "china_staff_training", "Staff Cooperation", 54, 19,
           [["china_machine_teams", "china_farm_machinery"]], {}, 0.01, "NKO_defence",
           "Propose reciprocal courses in aircraft maintenance, air defence and command procedure. Shared instruction can improve readiness, while each government must commit instructors and equipment.",
           agreement="china_staff_training", required=("china_border",),
           requirements=("The Border Cooperation Protocol is active.",))
    _focus(add, china, "china_air_defence_courses", "Air Defence Courses", 52, 20,
           [["china_staff_training"]], {"air_interception_detect_factor": 0.04,
            "education_cost_multiplier_modifier": 0.04}, 0.00875, "NKO_defence",
           "Train staff to connect warning posts, fighter commands and maintenance units. A more coordinated air-defence service requires sustained instruction and technical support.",
           required=("china_staff_training",),
           requirements=("The Korean-Chinese Staff and Maintenance Exchange is active.",),
           mutex=("china_air_defence_courses", "china_command_college"))
    _focus(add, china, "china_command_college", "Command College", 56, 20,
           [["china_staff_training"]], {"army_org_factor": 0.03,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.00875, "education_reform",
           "Standardize staff courses for logistics, mobilization and field coordination. Better preparation can strengthen readiness, while expanding the military education establishment.",
           required=("china_staff_training",),
           requirements=("The Korean-Chinese Staff and Maintenance Exchange is active.",),
           mutex=("china_air_defence_courses", "china_command_college"))
    _focus(add, china, "china_field_coordination", "Field Coordination", 50, 21,
           [["china_air_defence_courses"]], {"experience_gain_army": 0.025,
            "army_personnel_cost_multiplier_modifier": 0.03}, 0.00875, "dprk_army",
           "Coordinate command-post instruction between selected border and air-defence staffs. Practical preparation improves experience, while repeated courses consume personnel time.",
           required=("china_staff_training",),
           requirements=("The Korean-Chinese Staff and Maintenance Exchange is active.",))
    _focus(add, china, "china_joint_manoeuvres", "Joint Command Drills", 52, 22,
           [["china_field_coordination"]], {"army_org_factor": 0.035,
            "supply_consumption_factor": 0.04, "army_personnel_cost_multiplier_modifier": 0.04}, 0.01,
           "NKO_defence",
           "Invite reciprocal command-post and border-defence manoeuvres under the agreement. Combined procedures may improve readiness, while logistics and force commitments are costly.",
           required=("china_staff_training",),
           requirements=("The Korean-Chinese Staff and Maintenance Exchange is active.",),
           long_cost=True)
    _focus(add, china, "china_independent_procurement", "Domestic Procurement", 58, 21,
           [["china_command_college"]], {"foreign_influence_defense_modifier": 0.05,
            "production_speed_arms_factory_factor": -0.03,
            "trade_opinion_factor": -0.03}, 0.00875, "NKO_party_reform",
           "Limit the imported share of replacement parts and build domestic procurement capacity. Greater autonomy protects national discretion, but slows modernization and narrows trade access.")
    _focus(add, china, "china_patron_balance", "Balance of Relations", 54, 24,
           [["china_joint_manoeuvres", "china_independent_procurement"]],
           {"foreign_influence_defense_modifier": 0.04, "bureaucracy_cost_multiplier_modifier": 0.04},
           0.0125, "NKO_38_parallel",
           "Set a durable policy of reciprocal exchange while preserving the right to negotiate separately with every partner. Balanced diplomacy protects room for action, though it requires careful coordination.",
           required=("china_border",),
           requirements=("The Border Cooperation Protocol is active.",), long_cost=True)

    # Soviet Union: industrial and energy cooperation remain consent-based.
    # Late security cooperation is offered as a negotiated alternate-history
    # programme and has explicit recipient and partner costs.
    _focus(add, soviet, "soviet_partnership", "Soviet Partnership", 70, 12, [],
           {"productivity_growth_modifier": 0.025, "fossil_pp_energy_generation_modifier": 0.03,
            "foreign_influence_defense_modifier": -0.025}, 0.0075, "economic_civil_industry",
           "Build on the accepted industrial protocol to secure power engineering and reciprocal specialist access. Better output and energy reliability support national plans, while Moscow gains greater influence.",
           required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",))
    _focus(add, soviet, "soviet_power_projects", "Power Engineering", 68, 14,
           [["soviet_partnership"]], {}, 0.0125, "NKO_buildings",
           "Invite Soviet engineers to improve generating capacity and industrial maintenance. Reliable power can strengthen production, while machinery credit and continuing technical access carry costs.",
           agreement="soviet_energy_projects", required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",))
    _focus(add, soviet, "soviet_fuel_schedule", "Fuel-Rail Schedule", 72, 14,
           [["soviet_partnership"]], {}, 0.01, "trade",
           "Negotiate measured fuel and rail deliveries against contracted North Korean exports. More predictable inputs support production, while repayment and delivery targets limit domestic choices.",
           agreement="soviet_fuel_contract", required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",))
    _focus(add, soviet, "soviet_plant_accounts", "Plant Accounts", 68, 16,
           [["soviet_power_projects"]], {"production_factory_max_efficiency_factor": 0.04,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.0075, "parliament_box",
           "Require priority enterprises to publish repair schedules and power targets. Better reporting can protect new investment, while increasing the work of planning offices.",
           required=("soviet_energy_projects",),
           requirements=("Soviet Power and Engineering Projects are active.",))
    _focus(add, soviet, "soviet_turbine_service", "Turbine Workshops", 66, 17,
           [["soviet_plant_accounts"]], {"fossil_pp_energy_generation_modifier": 0.03,
            "education_cost_multiplier_modifier": 0.04}, 0.00875, "economic_civil_industry",
           "Train domestic crews to maintain imported turbines and industrial generators. More dependable service supports production, while training and replacement parts raise costs.",
           required=("soviet_energy_projects",),
           requirements=("Soviet Power and Engineering Projects are active.",))
    _focus(add, soviet, "soviet_machine_standards", "Machine Standards", 70, 17,
           [["soviet_plant_accounts"]], {"production_factory_efficiency_gain_factor": 0.05,
            "research_speed_factor": 0.025, "foreign_influence_defense_modifier": -0.03}, 0.00875,
           "education_reform",
           "Adopt shared inspection standards for Soviet machinery and train Korean engineers to apply them. Equipment adapts more quickly, while service contracts and outside standards deepen dependence.",
           required=("soviet_energy_projects",),
           requirements=("Soviet Power and Engineering Projects are active.",))
    _focus(add, soviet, "soviet_export_ledger", "Export Accounts", 72, 16,
           [["soviet_fuel_schedule"]], {"resource_export_multiplier_modifier": 0.025,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.0075, "trade",
           "Reconcile mineral and manufactured exports against fuel and rail deliveries. Clearer accounts sustain credit, while more output is committed to external repayment.",
           required=("soviet_fuel_contract",),
           requirements=("The Soviet Fuel and Transport Schedule is active.",))
    _focus(add, soviet, "soviet_freight_priorities", "Freight Priorities", 74, 17,
           [["soviet_export_ledger"]], {"supply_consumption_factor": -0.03,
            "production_speed_industrial_complex_factor": 0.03,
            "tax_gain_multiplier_modifier": -0.02}, 0.00875, "trade",
           "Give priority to freight corridors serving agreed deliveries and critical industrial inputs. Better coordination eases bottlenecks, while export revenue and administrative capacity are committed.",
           required=("soviet_fuel_contract",),
           requirements=("The Soviet Fuel and Transport Schedule is active.",))
    _focus(add, soviet, "soviet_domestic_efficiency", "Energy Efficiency", 72, 18,
           [["soviet_freight_priorities"]], {"non_electric_fuel_consumption_modifier": -0.03,
            "energy_use_multiplier": -0.03, "education_cost_multiplier_modifier": 0.03}, 0.00875,
           "economic_civil_industry",
           "Reduce waste in boilers, rail depots and priority plants. Better fuel economy can preserve imported supplies, while new standards and maintenance require trained crews.",
           required=("soviet_fuel_contract",),
           requirements=("The Soviet Fuel and Transport Schedule is active.",))
    _focus(add, soviet, "soviet_staff_exchange", "Staff Cooperation", 70, 19,
           [["soviet_machine_standards", "soviet_freight_priorities"]], {}, 0.01, "NKO_defence",
           "Propose reciprocal staff courses in air defence, logistics and command procedure. Soviet equipment and expertise can improve readiness, while both governments must commit instructors and facilities.",
           agreement="soviet_staff_training", required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",))
    _focus(add, soviet, "soviet_air_defence_school", "Air Defence School", 68, 20,
           [["soviet_staff_exchange"]], {"air_interception_detect_factor": 0.04,
            "static_anti_air_damage_factor": 0.03, "education_cost_multiplier_modifier": 0.04}, 0.00875,
           "NKO_defence",
           "Train Korean radar, interceptor and surface-defence staffs under the reciprocal programme. Better coordination strengthens warning and response, while technical courses require imported expertise.",
           required=("soviet_staff_training",),
           requirements=("The Soviet Air Defence and Staff Exchange is active.",),
           mutex=("soviet_air_defence_school", "soviet_command_college"))
    _focus(add, soviet, "soviet_command_college", "Command College", 72, 20,
           [["soviet_staff_exchange"]], {"army_org_factor": 0.03,
            "bureaucracy_cost_multiplier_modifier": 0.03}, 0.00875, "education_reform",
           "Standardize courses in logistics, readiness and command procedure. Better staff work supports coordination, while enlarging the military education establishment.",
           required=("soviet_staff_training",),
           requirements=("The Soviet Air Defence and Staff Exchange is active.",),
           mutex=("soviet_air_defence_school", "soviet_command_college"))
    _focus(add, soviet, "soviet_air_defence_coordination", "Air Defence Link", 66, 21,
           [["soviet_air_defence_school"]], {"air_interception_detect_factor": 0.04,
            "army_org_factor": 0.025, "bureaucracy_cost_multiplier_modifier": 0.03}, 0.00875,
           "NKO_defence",
           "Connect radar reporting, regional commands and repair depots in a common readiness plan. More reliable coordination requires continuing technical support and supervision.",
           required=("soviet_staff_training",),
           requirements=("The Soviet Air Defence and Staff Exchange is active.",))
    _focus(add, soviet, "soviet_exercise_intensity", "Command Exercises", 70, 21,
           [["soviet_command_college"]], {"experience_gain_army": 0.025,
            "army_org_factor": 0.03,
            "army_fuel_consumption_factor": 0.04,
            "army_personnel_cost_multiplier_modifier": 0.04}, 0.01, "dprk_army",
           "Set a regular schedule for reciprocal command-post and readiness exercises. Better coordination improves preparedness, while fuel and reserve commitments rise.",
           required=("soviet_staff_training",),
           requirements=("The Soviet Air Defence and Staff Exchange is active.",),
           long_cost=True)
    _focus(add, soviet, "soviet_independent_standards", "National Standards", 74, 21,
           [["soviet_command_college"]], {"foreign_influence_defense_modifier": 0.05,
            "production_factory_max_efficiency_factor": -0.03,
            "trade_opinion_factor": -0.03}, 0.00875, "NKO_party_reform",
           "Develop domestic maintenance standards and separate selected procurement lines from Soviet schedules. Greater autonomy protects political discretion, but slows technical modernization.",
           required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",))
    _focus(add, soviet, "soviet_balanced_security", "Security Compact", 70, 23,
           [["soviet_air_defence_coordination", "soviet_exercise_intensity", "soviet_independent_standards"]],
           {"foreign_influence_defense_modifier": 0.04,
            "bureaucracy_cost_multiplier_modifier": 0.04}, 0.0125, "NKO_38_parallel",
           "Maintain useful technical exchange while preserving the right to negotiate separately with Beijing and other partners. Balanced security protects room for action, though it requires careful coordination.",
           required=("soviet_industry",),
           requirements=("The Industrial Cooperation Protocol is active.",), long_cost=True)

    return d
