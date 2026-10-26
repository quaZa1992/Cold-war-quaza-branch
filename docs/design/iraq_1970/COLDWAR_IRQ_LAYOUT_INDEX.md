# COLDWAR_IRQ — exact layout index

Approval concept; resolved coordinates are the source of both preview and emitted specimen.

JSON SHA256: `82deef2b498d5e67d2b5dc157eda3ba534c2a8d35de215e7f7de679ffcc24eff`

| Area | Root | Full X range | Full Y range | Geometry |
|---|---|---|---|---|
| The Iraqi State | [4, 2] | 2..6 | 2..11 | compact |
| The Baath Party | [12, 2] | 10..16 | 2..10 | institutional-delivery-spurs |
| Ahmad Hasan al-Bakr | [20, 2] | 17..21 | 2..11 | left-offset |
| Saddam Hussein | [28, 2] | 26..30 | 2..11 | broad-fork |
| Abd al-Rahman Arif · Officer Republic | [36, 2] | 34..38 | 2..11 | compact |
| Arab Socialists · al-Rikabi / Haseeb | [44, 2] | 42..46 | 2..11 | compact |
| The Iraqi Communist Party | [52, 2] | 50..56 | 2..10 | institutional-delivery-spurs |
| Aziz Muhammad | [60, 2] | 57..61 | 2..11 | left-offset |
| National Democrats · Hadid | [68, 2] | 66..72 | 2..10 | conditional-delivery-spurs |
| Hashemite Restoration · Raad | [76, 2] | 74..78 | 2..11 | broad-fork |
| Iraq in the Cold War | [84, 2] | 82..86 | 2..11 | compact |
| The Barzani Leadership · KDP | [4, 15] | 1..7 | 15..23 | institutional-delivery-spurs |
| Jalal Talabani · PUK | [12, 15] | 8..14 | 15..23 | conditional-delivery-spurs |
| Islamic Dawa | [20, 15] | 17..21 | 15..24 | left-offset |
| Muhammad Baqir al-Hakim · SCIRI | [28, 15] | 26..30 | 15..24 | compact |
| The Iraqi Islamic Party | [36, 15] | 34..38 | 15..24 | compact |
| Oil, Revenue and Sovereignty | [44, 15] | 42..48 | 15..22 | conditional-delivery-spurs / two stages |
| Industry, Power and Infrastructure | [52, 15] | 50..55 | 15..23 | institutional-delivery-spurs |
| Land, Water and Rural Iraq | [60, 15] | 58..64 | 15..23 | conditional-delivery-spurs |
| Education and the Social Bargain | [68, 15] | 66..70 | 15..24 | broad-fork |
| The Armed Forces | [76, 15] | 73..77 | 15..24 | left-offset |
| War, Restraint and Reconstruction | [84, 15] | 82..86 | 15..24 | broad-fork |
| Iran: Road to War | [94, 15] | 90..98 | 15..30 | campaign-spine / optional-credit-spurs / two war doctrines |

## The Iraqi State

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_rcc_rules` | State of January 1970 | [4, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_executive_state` | Executive Authority | [3, 3] | 35 | (State of January 1970) | A Civic Compact |
| `COLDWAR_IRQ_civic_compact` | A Civic Compact | [5, 3] | 35 | (State of January 1970) | Executive Authority |
| `COLDWAR_IRQ_provincial_agents` | Provincial Offices | [3, 4] | 35 | (Executive Authority) | — |
| `COLDWAR_IRQ_elected_councils` | Provincial Councils | [5, 4] | 35 | (A Civic Compact) | — |
| `COLDWAR_IRQ_civil_register` | Common Civil Register | [4, 5] | 35 | (Provincial Offices OR Provincial Councils) | — |
| `COLDWAR_IRQ_security_priority` | Fund the Security State | [3, 6] | 35 | (Common Civil Register) | Protect Judicial Review |
| `COLDWAR_IRQ_judicial_priority` | Protect Judicial Review | [5, 6] | 35 | (Common Civil Register) | Fund the Security State |
| `COLDWAR_IRQ_review_detentions` | Political Detentions | [3, 7] | 35 | (Fund the Security State) | — |
| `COLDWAR_IRQ_courts_budget` | An Independent Bench | [5, 7] | 35 | (Protect Judicial Review) | — |
| `COLDWAR_IRQ_ministerial_audit` | Ministerial Payrolls | [4, 8] | 35 | (Political Detentions OR An Independent Bench) | — |
| `COLDWAR_IRQ_north_talks` | Kurdish Negotiations | [2, 9] | 21 | (Ministerial Payrolls) | — |
| `COLDWAR_IRQ_army_command_review` | Parallel Commands | [4, 9] | 35 | (Ministerial Payrolls) | — |
| `COLDWAR_IRQ_budget_accounts` | The State Accounts | [6, 9] | 35 | (Ministerial Payrolls) | — |
| `COLDWAR_IRQ_autonomy_guarantees` | Funded Guarantees | [2, 10] | 35 | (Kurdish Negotiations) | — |
| `COLDWAR_IRQ_professional_command` | Chain of Command | [4, 10] | 35 | (Parallel Commands) | — |
| `COLDWAR_IRQ_tax_registry` | A Tax Administration | [6, 10] | 35 | (The State Accounts) | — |
| `COLDWAR_IRQ_state_compact` | A Workable Iraqi State | [4, 11] | 49 | (Funded Guarantees OR Chain of Command OR A Tax Administration) | — |

## The Baath Party

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_regional_command` | The Regional Command | [12, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_national_front` | National Front | [12, 3] | 35 | (The Regional Command) | Exclusive Party State |
| `COLDWAR_IRQ_baath_monopoly` | Exclusive Party State | [14, 3] | 35 | (The Regional Command) | National Front |
| `COLDWAR_IRQ_front_guarantees` | The Coalition Charter | [10, 4] | 35 | (National Front) | — |
| `COLDWAR_IRQ_party_screening` | Screen the Ministries | [16, 4] | 35 | (Exclusive Party State) | — |
| `COLDWAR_IRQ_baath_congress` | A Regional Congress | [13, 4] | 35 | (National Front OR Exclusive Party State) | — |
| `COLDWAR_IRQ_mass_party` | A Mass Party | [12, 5] | 35 | (A Regional Congress) | A Cadre Party |
| `COLDWAR_IRQ_cadre_party` | A Cadre Party | [14, 5] | 35 | (A Regional Congress) | A Mass Party |
| `COLDWAR_IRQ_popular_organizations` | Popular Organizations | [12, 6] | 35 | (A Mass Party) | — |
| `COLDWAR_IRQ_party_schools` | Expand Party Schools | [14, 6] | 35 | (A Cadre Party) | — |
| `COLDWAR_IRQ_baath_accounts` | Separate Accounts | [13, 7] | 35 | (Popular Organizations OR Expand Party Schools) | — |
| `COLDWAR_IRQ_arab_socialism` | Arab Socialism | [11, 8] | 35 | (Separate Accounts) | — |
| `COLDWAR_IRQ_secular_state` | Secular State Service | [13, 8] | 35 | (Separate Accounts) | — |
| `COLDWAR_IRQ_women_unions` | Women in State Service | [15, 8] | 35 | (Separate Accounts) | — |
| `COLDWAR_IRQ_enterprise_accounts` | Audit Public Enterprises | [11, 9] | 35 | (Arab Socialism) | — |
| `COLDWAR_IRQ_baath_citizenship` | Common Citizenship | [13, 9] | 35 | (Secular State Service) | — |
| `COLDWAR_IRQ_party_social_bargain` | Party Social Bargain | [15, 9] | 35 | (Women in State Service) | — |
| `COLDWAR_IRQ_baath_future` | The Baathist Republic | [13, 10] | 49 | (Audit Public Enterprises OR Common Citizenship OR Party Social Bargain) | — |

## Ahmad Hasan al-Bakr

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_bakr_presidency` | Presidency of al-Bakr | [20, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_bakr_collective` | Collective Leadership | [18, 3] | 35 | (Presidency of al-Bakr) | Presidential Arbitration |
| `COLDWAR_IRQ_bakr_presidential` | Presidential Arbitration | [20, 3] | 35 | (Presidency of al-Bakr) | Collective Leadership |
| `COLDWAR_IRQ_bakr_council` | Command Council | [18, 4] | 35 | (Collective Leadership) | — |
| `COLDWAR_IRQ_bakr_loyal_officers` | Trusted Officers | [20, 4] | 35 | (Presidential Arbitration) | — |
| `COLDWAR_IRQ_bakr_continuity` | Continuity Secretariat | [19, 5] | 35 | (Command Council OR Trusted Officers) | — |
| `COLDWAR_IRQ_bakr_contain_deputy` | Limit the Deputy | [18, 6] | 35 | (Continuity Secretariat) | Delegate to Saddam |
| `COLDWAR_IRQ_bakr_delegate` | Delegate to Saddam | [20, 6] | 35 | (Continuity Secretariat) | Limit the Deputy |
| `COLDWAR_IRQ_bakr_guarantees` | Old Guard Guarantees | [18, 7] | 35 | (Limit the Deputy) | — |
| `COLDWAR_IRQ_bakr_deputy_budget` | Executive Coordination | [20, 7] | 35 | (Delegate to Saddam) | — |
| `COLDWAR_IRQ_bakr_development` | Development Priorities | [19, 8] | 35 | (Old Guard Guarantees OR Executive Coordination) | — |
| `COLDWAR_IRQ_bakr_treaty` | Soviet Friendship | [17, 9] | 35 | (Development Priorities) | — |
| `COLDWAR_IRQ_bakr_north` | Northern Guarantees | [19, 9] | 35 | (Development Priorities) | — |
| `COLDWAR_IRQ_bakr_unity` | Explore Arab Unity | [21, 9] | 35 | (Development Priorities) | — |
| `COLDWAR_IRQ_bakr_technical_mission` | Technical Missions | [17, 10] | 35 | (Soviet Friendship) | — |
| `COLDWAR_IRQ_bakr_compromise` | A Durable Compromise | [19, 10] | 35 | (Northern Guarantees) | — |
| `COLDWAR_IRQ_bakr_union_charter` | Union Charter | [21, 10] | 35 | (Explore Arab Unity) | — |
| `COLDWAR_IRQ_bakr_succession_plan` | Negotiated Succession | [19, 11] | 49 | (Technical Missions OR A Durable Compromise OR Union Charter) | — |

## Saddam Hussein

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_saddam_presidency` | Saddam's Presidency | [28, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_saddam_personal_state` | Personal Rule | [26, 3] | 35 | (Saddam's Presidency) | The Party Cabinet |
| `COLDWAR_IRQ_saddam_party_cabinet` | The Party Cabinet | [30, 3] | 35 | (Saddam's Presidency) | Personal Rule |
| `COLDWAR_IRQ_saddam_security_bureau` | Security Bureau | [26, 4] | 35 | (Personal Rule) | — |
| `COLDWAR_IRQ_saddam_technocrats` | Retain the Technocrats | [30, 4] | 35 | (The Party Cabinet) | — |
| `COLDWAR_IRQ_saddam_social_contract` | Oil and Legitimacy | [28, 5] | 35 | (Security Bureau OR Retain the Technocrats) | — |
| `COLDWAR_IRQ_saddam_guard` | Presidential Guard | [26, 6] | 35 | (Oil and Legitimacy) | The Regular Army |
| `COLDWAR_IRQ_saddam_regular_army` | The Regular Army | [30, 6] | 35 | (Oil and Legitimacy) | Presidential Guard |
| `COLDWAR_IRQ_saddam_guard_supply` | Guard Logistics | [26, 7] | 35 | (Presidential Guard) | — |
| `COLDWAR_IRQ_saddam_staff_college` | Staff Appointments | [30, 7] | 35 | (The Regular Army) | — |
| `COLDWAR_IRQ_saddam_regional_role` | A Regional Role for Iraq | [28, 8] | 35 | (Guard Logistics OR Staff Appointments) | — |
| `COLDWAR_IRQ_saddam_iran_dossier` | Iranian Revolution | [26, 9] | 35 | (A Regional Role for Iraq) | — |
| `COLDWAR_IRQ_saddam_industry` | Presidential Projects | [28, 9] | 49 | (A Regional Role for Iraq) | — |
| `COLDWAR_IRQ_saddam_credit` | Negotiate Gulf Credit | [30, 9] | 35 | (A Regional Role for Iraq) | — |
| `COLDWAR_IRQ_saddam_bounded_deterrence` | A Costed Deterrent | [26, 10] | 35 | (Iranian Revolution) | — |
| `COLDWAR_IRQ_saddam_local_procurement` | Local Procurement | [28, 10] | 35 | (Presidential Projects) | — |
| `COLDWAR_IRQ_saddam_debt_service` | The Credit Burden | [30, 10] | 35 | (Negotiate Gulf Credit) | — |
| `COLDWAR_IRQ_saddam_legacy` | Presidential Power | [28, 11] | 49 | (A Costed Deterrent OR Local Procurement OR The Credit Burden) | — |

## Abd al-Rahman Arif · Officer Republic

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_officer_council` | An Officer Council | [36, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_officer_caretaker` | Caretaker Government | [35, 3] | 35 | (An Officer Council) | Military Presidency |
| `COLDWAR_IRQ_officer_permanent` | Military Presidency | [37, 3] | 35 | (An Officer Council) | Caretaker Government |
| `COLDWAR_IRQ_officer_civilian_cabinet` | Civilian Cabinet | [35, 4] | 35 | (Caretaker Government) | — |
| `COLDWAR_IRQ_officer_garrisons` | Garrison Government | [37, 4] | 35 | (Military Presidency) | — |
| `COLDWAR_IRQ_officer_procurement` | Military Procurement | [36, 5] | 35 | (Civilian Cabinet OR Garrison Government) | — |
| `COLDWAR_IRQ_officer_merit` | Merit Promotions | [35, 6] | 35 | (Military Procurement) | Promotion by Loyalty |
| `COLDWAR_IRQ_officer_loyalty` | Promotion by Loyalty | [37, 6] | 35 | (Military Procurement) | Merit Promotions |
| `COLDWAR_IRQ_officer_staff` | A National Staff College | [35, 7] | 35 | (Merit Promotions) | — |
| `COLDWAR_IRQ_officer_commissars` | Ministerial Officers | [37, 7] | 35 | (Promotion by Loyalty) | — |
| `COLDWAR_IRQ_officer_state_budget` | Defence Accounts | [36, 8] | 35 | (A National Staff College OR Ministerial Officers) | — |
| `COLDWAR_IRQ_officer_amnesty` | Conditional Amnesty | [34, 9] | 35 | (Defence Accounts) | — |
| `COLDWAR_IRQ_officer_border_force` | Border Forces | [36, 9] | 35 | (Defence Accounts) | — |
| `COLDWAR_IRQ_officer_civic_timetable` | Transition Timetable | [38, 9] | 35 | (Defence Accounts) | — |
| `COLDWAR_IRQ_officer_reintegration` | Officers to Barracks | [34, 10] | 35 | (Conditional Amnesty) | — |
| `COLDWAR_IRQ_officer_logistics` | Unified Logistics | [36, 10] | 35 | (Border Forces) | — |
| `COLDWAR_IRQ_officer_continuity` | Civilian Guarantees | [38, 10] | 35 | (Transition Timetable) | — |
| `COLDWAR_IRQ_officer_settlement` | Civil-Military Order | [36, 11] | 49 | (Officers to Barracks OR Unified Logistics OR Civilian Guarantees) | — |

## Arab Socialists · al-Rikabi / Haseeb

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_arab_republican_movement` | Arab Republicanism | [44, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_arab_cairo` | Cooperate with Cairo | [43, 3] | 35 | (Arab Republicanism) | An Iraqi Arab Republic |
| `COLDWAR_IRQ_arab_iraqi_sovereignty` | An Iraqi Arab Republic | [45, 3] | 35 | (Arab Republicanism) | Cooperate with Cairo |
| `COLDWAR_IRQ_arab_joint_planning` | Joint Planning | [43, 4] | 35 | (Cooperate with Cairo) | — |
| `COLDWAR_IRQ_arab_public_service` | Republican Service | [45, 4] | 35 | (An Iraqi Arab Republic) | — |
| `COLDWAR_IRQ_arab_social_charter` | Social Charter | [44, 5] | 35 | (Joint Planning OR Republican Service) | — |
| `COLDWAR_IRQ_arab_state_sector` | Leading Public Sector | [43, 6] | 35 | (Social Charter) | An Arab Mixed Economy |
| `COLDWAR_IRQ_arab_mixed_sector` | An Arab Mixed Economy | [45, 6] | 35 | (Social Charter) | Leading Public Sector |
| `COLDWAR_IRQ_arab_state_contracts` | Public Contracts | [43, 7] | 35 | (Leading Public Sector) | — |
| `COLDWAR_IRQ_arab_credit_coops` | Cooperative Credit | [45, 7] | 35 | (An Arab Mixed Economy) | — |
| `COLDWAR_IRQ_arab_citizenship` | Equal Citizens | [44, 8] | 35 | (Public Contracts OR Cooperative Credit) | — |
| `COLDWAR_IRQ_arab_palestine` | Palestinian Solidarity | [42, 9] | 35 | (Equal Citizens) | — |
| `COLDWAR_IRQ_arab_technical_exchange` | Technical Exchanges | [44, 9] | 35 | (Equal Citizens) | — |
| `COLDWAR_IRQ_arab_union_convention` | A Union by Convention | [46, 9] | 35 | (Equal Citizens) | — |
| `COLDWAR_IRQ_arab_civil_diplomacy` | Civilian Solidarity | [42, 10] | 35 | (Palestinian Solidarity) | — |
| `COLDWAR_IRQ_arab_training_network` | Training Network | [44, 10] | 35 | (Technical Exchanges) | — |
| `COLDWAR_IRQ_arab_union_accounts` | Arab Partnership | [46, 10] | 35 | (A Union by Convention) | — |
| `COLDWAR_IRQ_arab_republic_endures` | Enduring Arab Republic | [44, 11] | 49 | (Civilian Solidarity OR Training Network OR Arab Partnership) | — |

## The Iraqi Communist Party

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_icp_congress` | Congress after Terror | [52, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_icp_front_strategy` | A Conditional Front | [52, 3] | 35 | (Congress after Terror) | Independent Party |
| `COLDWAR_IRQ_icp_independent_strategy` | Independent Party | [54, 3] | 35 | (Congress after Terror) | A Conditional Front |
| `COLDWAR_IRQ_icp_legal_cells` | A Legal Party Network | [50, 4] | 35 | (A Conditional Front) | — |
| `COLDWAR_IRQ_icp_underground` | The Underground | [56, 4] | 35 | (Independent Party) | — |
| `COLDWAR_IRQ_icp_membership` | Membership Records | [53, 4] | 35 | (A Conditional Front OR Independent Party) | — |
| `COLDWAR_IRQ_icp_democratic_front` | Pluralist Socialist Front | [52, 5] | 35 | (Membership Records) | A Vanguard State |
| `COLDWAR_IRQ_icp_vanguard` | A Vanguard State | [54, 5] | 35 | (Membership Records) | Pluralist Socialist Front |
| `COLDWAR_IRQ_icp_union_autonomy` | Independent Unions | [52, 6] | 35 | (Pluralist Socialist Front) | — |
| `COLDWAR_IRQ_icp_state_unions` | Unions of the Plan | [54, 6] | 35 | (A Vanguard State) | — |
| `COLDWAR_IRQ_icp_national_question` | Nationalities Charter | [53, 7] | 35 | (Independent Unions OR Unions of the Plan) | — |
| `COLDWAR_IRQ_icp_industrial_workers` | Workers Councils | [51, 8] | 35 | (Nationalities Charter) | — |
| `COLDWAR_IRQ_icp_soviet_relations` | Soviet Party Relations | [53, 8] | 35 | (Nationalities Charter) | — |
| `COLDWAR_IRQ_icp_rural_cells` | Organize the Rural Poor | [55, 8] | 35 | (Nationalities Charter) | — |
| `COLDWAR_IRQ_icp_safety_inspection` | Safety Inspectors | [51, 9] | 35 | (Workers Councils) | — |
| `COLDWAR_IRQ_icp_cadre_schools` | Train Technical Cadres | [53, 9] | 35 | (Soviet Party Relations) | — |
| `COLDWAR_IRQ_icp_peasant_credit` | Rural Credit Reform | [55, 9] | 35 | (Organize the Rural Poor) | — |
| `COLDWAR_IRQ_icp_socialist_republic` | The Socialist Republic | [53, 10] | 49 | (Safety Inspectors OR Train Technical Cadres OR Rural Credit Reform) | — |

## Aziz Muhammad

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_aziz_secretariat` | Aziz Muhammad | [60, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_aziz_negotiated_road` | Road to Power | [58, 3] | 35 | (Aziz Muhammad) | Build an Opposition Bloc |
| `COLDWAR_IRQ_aziz_opposition_road` | Build an Opposition Bloc | [60, 3] | 35 | (Aziz Muhammad) | Road to Power |
| `COLDWAR_IRQ_aziz_front_red_lines` | Coalition Red Lines | [58, 4] | 35 | (Road to Power) | — |
| `COLDWAR_IRQ_aziz_resilient_networks` | Resilient Networks | [60, 4] | 35 | (Build an Opposition Bloc) | — |
| `COLDWAR_IRQ_aziz_congress_accounts` | Congress Oversight | [59, 5] | 35 | (Coalition Red Lines OR Resilient Networks) | — |
| `COLDWAR_IRQ_aziz_federal_guarantees` | Federal Guarantees | [58, 6] | 35 | (Congress Oversight) | Unitary Socialism |
| `COLDWAR_IRQ_aziz_unitary_left` | Unitary Socialism | [60, 6] | 35 | (Congress Oversight) | Federal Guarantees |
| `COLDWAR_IRQ_aziz_regional_budget` | The Regional Compact | [58, 7] | 35 | (Federal Guarantees) | — |
| `COLDWAR_IRQ_aziz_language_rights` | Language in Schools | [60, 7] | 35 | (Unitary Socialism) | — |
| `COLDWAR_IRQ_aziz_soviet_distance` | Room to Disagree | [59, 8] | 35 | (The Regional Compact OR Language in Schools) | — |
| `COLDWAR_IRQ_aziz_worker_training` | Workers Training | [57, 9] | 35 | (Room to Disagree) | — |
| `COLDWAR_IRQ_aziz_united_opposition` | Democratic Opposition | [59, 9] | 35 | (Room to Disagree) | — |
| `COLDWAR_IRQ_aziz_civilian_welfare` | Welfare before Prestige | [61, 9] | 35 | (Room to Disagree) | — |
| `COLDWAR_IRQ_aziz_workplace_delegates` | Workplace Delegates | [57, 10] | 35 | (Workers Training) | — |
| `COLDWAR_IRQ_aziz_safe_return` | Return from Exile | [59, 10] | 35 | (Democratic Opposition) | — |
| `COLDWAR_IRQ_aziz_rural_services` | Rural Services | [61, 10] | 35 | (Welfare before Prestige) | — |
| `COLDWAR_IRQ_aziz_party_renewal` | The Party Mandate | [59, 11] | 49 | (Workplace Delegates OR Return from Exile OR Rural Services) | — |

## National Democrats · Hadid

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_civic_reconstitution` | Civilian Politics | [68, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_civic_social_republic` | Social Republic | [68, 3] | 35 | (Civilian Politics) | Liberal Republic |
| `COLDWAR_IRQ_civic_liberal_republic` | Liberal Republic | [70, 3] | 35 | (Civilian Politics) | Social Republic |
| `COLDWAR_IRQ_civic_social_budget` | Budget for Social Rights | [68, 4] | 35 | (Social Republic) | — |
| `COLDWAR_IRQ_civic_commercial_courts` | Commercial Courts | [70, 4] | 35 | (Liberal Republic) | — |
| `COLDWAR_IRQ_civic_electoral_register` | An Electoral Register | [69, 5] | 35 | (Budget for Social Rights OR Commercial Courts) | — |
| `COLDWAR_IRQ_civic_federal` | A Federal Constitution | [68, 6] | 35 | (An Electoral Register) | A Unitary Republic |
| `COLDWAR_IRQ_civic_unitary` | A Unitary Republic | [70, 6] | 35 | (An Electoral Register) | A Federal Constitution |
| `COLDWAR_IRQ_civic_fiscal_federalism` | Agree Fiscal Federalism | [66, 7] | 35 | (A Federal Constitution) | — |
| `COLDWAR_IRQ_civic_local_accounts` | Municipal Accounts | [72, 7] | 35 | (A Unitary Republic) | — |
| `COLDWAR_IRQ_civic_security_oversight` | Security Oversight | [69, 7] | 35 | (A Federal Constitution OR A Unitary Republic) | — |
| `COLDWAR_IRQ_civic_education` | Republican Schools | [67, 8] | 35 | (Security Oversight) | — |
| `COLDWAR_IRQ_civic_non_alignment` | Independent Diplomacy | [69, 8] | 35 | (Security Oversight) | — |
| `COLDWAR_IRQ_civic_labour_bargain` | Labour Bargain | [71, 8] | 35 | (Security Oversight) | — |
| `COLDWAR_IRQ_civic_universities` | University Autonomy | [67, 9] | 35 | (Republican Schools) | — |
| `COLDWAR_IRQ_civic_credit_terms` | Transparent Finance | [69, 9] | 35 | (Independent Diplomacy) | — |
| `COLDWAR_IRQ_civic_union_compact` | Labour Rights Compact | [71, 9] | 35 | (Labour Bargain) | — |
| `COLDWAR_IRQ_civic_mandate` | A Civilian Mandate | [69, 10] | 49 | (University Autonomy OR Transparent Finance OR Labour Rights Compact) | — |

## Hashemite Restoration · Raad

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_royal_charter` | A New Charter | [76, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_royal_ceremonial` | A Ceremonial Crown | [74, 3] | 35 | (A New Charter) | An Executive Crown |
| `COLDWAR_IRQ_royal_executive` | An Executive Crown | [78, 3] | 35 | (A New Charter) | A Ceremonial Crown |
| `COLDWAR_IRQ_royal_parliament` | Responsible Parliament | [74, 4] | 35 | (A Ceremonial Crown) | — |
| `COLDWAR_IRQ_royal_council` | Royal Advisory Council | [78, 4] | 35 | (An Executive Crown) | — |
| `COLDWAR_IRQ_royal_accounts` | Crown and Treasury | [76, 5] | 35 | (Responsible Parliament OR Royal Advisory Council) | — |
| `COLDWAR_IRQ_royal_land_review` | Review Land Claims | [74, 6] | 35 | (Crown and Treasury) | Existing Property |
| `COLDWAR_IRQ_royal_property_guarantees` | Existing Property | [78, 6] | 35 | (Crown and Treasury) | Review Land Claims |
| `COLDWAR_IRQ_royal_compensation` | Compensation Tribunal | [74, 7] | 35 | (Review Land Claims) | — |
| `COLDWAR_IRQ_royal_rural_contracts` | Rural Contract Law | [78, 7] | 35 | (Existing Property) | — |
| `COLDWAR_IRQ_royal_citizenship` | A Common Crown | [76, 8] | 35 | (Compensation Tribunal OR Rural Contract Law) | — |
| `COLDWAR_IRQ_royal_jordan` | Open Talks with Jordan | [74, 9] | 35 | (A Common Crown) | — |
| `COLDWAR_IRQ_royal_service` | Royal Civil Service | [76, 9] | 35 | (A Common Crown) | — |
| `COLDWAR_IRQ_royal_education` | Schools and Citizenship | [78, 9] | 35 | (A Common Crown) | — |
| `COLDWAR_IRQ_royal_commerce` | Commercial Partnership | [74, 10] | 35 | (Open Talks with Jordan) | — |
| `COLDWAR_IRQ_royal_public_works` | Royal Public Works | [76, 10] | 35 | (Royal Civil Service) | — |
| `COLDWAR_IRQ_royal_budget_review` | Budget Review | [78, 10] | 35 | (Schools and Citizenship) | — |
| `COLDWAR_IRQ_royal_settlement` | Constitutional Charter | [76, 11] | 49 | (Commercial Partnership OR Royal Public Works OR Budget Review) | — |

## Iraq in the Cold War

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_foreign_dossier` | Foreign Policy Dossier | [84, 2] | 21 | Entry | — |
| `COLDWAR_IRQ_foreign_treaty_partner` | Seek a Treaty Partner | [83, 3] | 35 | (Foreign Policy Dossier) | Active Non-Alignment |
| `COLDWAR_IRQ_foreign_non_alignment` | Active Non-Alignment | [85, 3] | 35 | (Foreign Policy Dossier) | Seek a Treaty Partner |
| `COLDWAR_IRQ_foreign_partner_offer` | The Partner Treaty | [83, 4] | 35 | (Seek a Treaty Partner) | — |
| `COLDWAR_IRQ_foreign_multiple_offers` | Open Cooperation | [85, 4] | 35 | (Active Non-Alignment) | — |
| `COLDWAR_IRQ_foreign_treaty_register` | External Obligations | [84, 5] | 35 | (The Partner Treaty OR Open Cooperation) | — |
| `COLDWAR_IRQ_foreign_border_settlement` | The Shatt al-Arab | [83, 6] | 35 | (External Obligations) | Armed Deterrence |
| `COLDWAR_IRQ_foreign_armed_deterrence` | Armed Deterrence | [85, 6] | 35 | (External Obligations) | The Shatt al-Arab |
| `COLDWAR_IRQ_foreign_border_delivery` | Deliver the Settlement | [83, 7] | 35 | (The Shatt al-Arab) | — |
| `COLDWAR_IRQ_foreign_incident_channel` | Frontier Crisis Channel | [85, 7] | 35 | (Armed Deterrence) | — |
| `COLDWAR_IRQ_foreign_regional_diplomacy` | Regional Diplomacy | [84, 8] | 35 | (Deliver the Settlement OR Frontier Crisis Channel) | — |
| `COLDWAR_IRQ_foreign_syria` | The Syrian Dossier | [82, 9] | 35 | (Regional Diplomacy) | — |
| `COLDWAR_IRQ_foreign_kuwait` | The Kuwaiti Dossier | [84, 9] | 35 | (Regional Diplomacy) | — |
| `COLDWAR_IRQ_foreign_party_support` | Foreign Party Support | [86, 9] | 35 | (Regional Diplomacy) | — |
| `COLDWAR_IRQ_foreign_arab_reconciliation` | Arab Reconciliation | [82, 10] | 35 | (The Syrian Dossier) | — |
| `COLDWAR_IRQ_foreign_debt_diplomacy` | Credit from Territory | [84, 10] | 35 | (The Kuwaiti Dossier) | — |
| `COLDWAR_IRQ_foreign_support_accounts` | Support Commitments | [86, 10] | 35 | (Foreign Party Support) | — |
| `COLDWAR_IRQ_foreign_review` | External Commitments | [84, 11] | 49 | (Arab Reconciliation OR Credit from Territory OR Support Commitments) | — |

## The Barzani Leadership · KDP

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_kdp_national_government` | The KDP Cabinet | [4, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_kdp_autonomy` | The Autonomy Accord | [3, 16] | 35 | (The KDP Cabinet) | A Federal Republic |
| `COLDWAR_IRQ_kdp_federal_republic` | A Federal Republic | [5, 16] | 35 | (The KDP Cabinet) | The Autonomy Accord |
| `COLDWAR_IRQ_kdp_autonomy_budget` | Autonomous Services | [1, 17] | 35 | (The Autonomy Accord) | — |
| `COLDWAR_IRQ_kdp_federal_budget` | Federal Revenue | [7, 17] | 35 | (A Federal Republic) | — |
| `COLDWAR_IRQ_kdp_government_accounts` | Regional Accounts | [4, 17] | 35 | (The Autonomy Accord OR A Federal Republic) | — |
| `COLDWAR_IRQ_kdp_barzani_continuity` | Barzani Continuity | [3, 18] | 35 | (Regional Accounts) | A Civic KDP |
| `COLDWAR_IRQ_kdp_civic_party` | A Civic KDP | [5, 18] | 35 | (Regional Accounts) | Barzani Continuity |
| `COLDWAR_IRQ_kdp_succession` | Barzani Succession | [3, 19] | 35 | (Barzani Continuity) | — |
| `COLDWAR_IRQ_kdp_civic_councils` | Regional Councils | [5, 19] | 35 | (A Civic KDP) | — |
| `COLDWAR_IRQ_kdp_language` | Language Rights | [4, 20] | 35 | (Barzani Succession OR Regional Councils) | — |
| `COLDWAR_IRQ_kdp_mountain_routes` | Mountain Roads | [2, 21] | 49 | (Language Rights) | — |
| `COLDWAR_IRQ_kdp_oil_status` | Negotiate Kirkuk Status | [4, 21] | 35 | (Language Rights) | — |
| `COLDWAR_IRQ_kdp_security_integration` | Security Integration | [6, 21] | 35 | (Language Rights) | — |
| `COLDWAR_IRQ_kdp_rural_credit` | Mountain Farm Credit | [2, 22] | 35 | (Mountain Roads) | — |
| `COLDWAR_IRQ_kdp_shared_revenue` | Shared Oil Revenue | [4, 22] | 35 | (Negotiate Kirkuk Status) | — |
| `COLDWAR_IRQ_kdp_local_policing` | Local Police Charter | [6, 22] | 35 | (Security Integration) | — |
| `COLDWAR_IRQ_kdp_common_republic` | Federal Republic | [4, 23] | 49 | (Mountain Farm Credit OR Shared Oil Revenue OR Local Police Charter) | — |

## Jalal Talabani · PUK

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_puk_government` | Jalal Talabani | [12, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_puk_pluralist_left` | A Pluralist Kurdish Left | [10, 16] | 35 | (Jalal Talabani) | Party Discipline |
| `COLDWAR_IRQ_puk_disciplined_party` | Party Discipline | [12, 16] | 35 | (Jalal Talabani) | A Pluralist Kurdish Left |
| `COLDWAR_IRQ_puk_local_assemblies` | Funded Assemblies | [10, 17] | 35 | (A Pluralist Kurdish Left) | — |
| `COLDWAR_IRQ_puk_cadre_training` | A Progressive Cadre | [12, 17] | 35 | (Party Discipline) | — |
| `COLDWAR_IRQ_puk_federal_platform` | Federal Platform | [11, 18] | 35 | (Funded Assemblies OR A Progressive Cadre) | — |
| `COLDWAR_IRQ_puk_regional_cooperation` | Kurdish Cooperation | [10, 19] | 35 | (Federal Platform) | Independent Movement |
| `COLDWAR_IRQ_puk_independent_movement` | Independent Movement | [12, 19] | 35 | (Federal Platform) | Kurdish Cooperation |
| `COLDWAR_IRQ_puk_joint_services` | Joint Regional Services | [8, 20] | 35 | (Kurdish Cooperation) | — |
| `COLDWAR_IRQ_puk_party_municipalities` | Municipal Networks | [14, 20] | 35 | (Independent Movement) | — |
| `COLDWAR_IRQ_puk_constitution` | Federal Iraq | [11, 20] | 35 | (Kurdish Cooperation OR Independent Movement) | — |
| `COLDWAR_IRQ_puk_sulaymaniyah` | Develop Sulaymaniyah | [9, 21] | 49 | (Federal Iraq) | — |
| `COLDWAR_IRQ_puk_universities` | Regional Universities | [11, 21] | 35 | (Federal Iraq) | — |
| `COLDWAR_IRQ_puk_security_compact` | A Security Compact | [13, 21] | 35 | (Federal Iraq) | — |
| `COLDWAR_IRQ_puk_trade_routes` | Mountain Trade Routes | [9, 22] | 35 | (Develop Sulaymaniyah) | — |
| `COLDWAR_IRQ_puk_student_exchange` | Iraqi Student Exchange | [11, 22] | 35 | (Regional Universities) | — |
| `COLDWAR_IRQ_puk_payroll` | Security Payroll | [13, 22] | 35 | (A Security Compact) | — |
| `COLDWAR_IRQ_puk_federal_mandate` | A Federal Mandate | [11, 23] | 49 | (Mountain Trade Routes OR Iraqi Student Exchange OR Security Payroll) | — |

## Islamic Dawa

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_dawa_civil_government` | Dawa in Government | [20, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_dawa_constitutional` | An Islamic Cabinet | [18, 16] | 35 | (Dawa in Government) | Party-Directed Rule |
| `COLDWAR_IRQ_dawa_directorial` | Party-Directed Rule | [20, 16] | 35 | (Dawa in Government) | An Islamic Cabinet |
| `COLDWAR_IRQ_dawa_legal_review` | Religious Legal Review | [18, 17] | 35 | (An Islamic Cabinet) | — |
| `COLDWAR_IRQ_dawa_party_service` | Party Service Network | [20, 17] | 35 | (Party-Directed Rule) | — |
| `COLDWAR_IRQ_dawa_sadr_thought` | The Thought of al-Sadr | [19, 18] | 35 | (Religious Legal Review OR Party Service Network) | — |
| `COLDWAR_IRQ_dawa_social_justice` | Islamic Social Justice | [18, 19] | 35 | (The Thought of al-Sadr) | Enterprise and Waqf |
| `COLDWAR_IRQ_dawa_small_enterprise` | Enterprise and Waqf | [20, 19] | 35 | (The Thought of al-Sadr) | Islamic Social Justice |
| `COLDWAR_IRQ_dawa_social_accounts` | Audited Welfare Funds | [18, 20] | 35 | (Islamic Social Justice) | — |
| `COLDWAR_IRQ_dawa_endowment_accounts` | Endowment Accounts | [20, 20] | 35 | (Enterprise and Waqf) | — |
| `COLDWAR_IRQ_dawa_citizenship` | Equal Citizenship | [19, 21] | 35 | (Audited Welfare Funds OR Endowment Accounts) | — |
| `COLDWAR_IRQ_dawa_najaf_schools` | Najaf Technical Skills | [17, 22] | 35 | (Equal Citizenship) | — |
| `COLDWAR_IRQ_dawa_independent_iraq` | An Iraqi Programme | [19, 22] | 35 | (Equal Citizenship) | — |
| `COLDWAR_IRQ_dawa_trade_unions` | Labour Associations | [21, 22] | 35 | (Equal Citizenship) | — |
| `COLDWAR_IRQ_dawa_literacy` | Community Literacy | [17, 23] | 35 | (Najaf Technical Skills) | — |
| `COLDWAR_IRQ_dawa_neighbour_talks` | Sovereign Diplomacy | [19, 23] | 35 | (An Iraqi Programme) | — |
| `COLDWAR_IRQ_dawa_medical_network` | Community Medicine | [21, 23] | 35 | (Labour Associations) | — |
| `COLDWAR_IRQ_dawa_government_review` | The Islamic Cabinet | [19, 24] | 49 | (Community Literacy OR Sovereign Diplomacy OR Community Medicine) | — |

## Muhammad Baqir al-Hakim · SCIRI

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_sciri_exile_council` | The Exile Council | [28, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_sciri_iraqi_charter` | Constitutional Charter | [27, 16] | 35 | (The Exile Council) | A Clerical Executive |
| `COLDWAR_IRQ_sciri_clerical_executive` | A Clerical Executive | [29, 16] | 35 | (The Exile Council) | Constitutional Charter |
| `COLDWAR_IRQ_sciri_representative_cabinet` | Representative Cabinet | [27, 17] | 35 | (Constitutional Charter) | — |
| `COLDWAR_IRQ_sciri_revolutionary_courts` | Revolutionary Courts | [29, 17] | 35 | (A Clerical Executive) | — |
| `COLDWAR_IRQ_sciri_returnees` | The Return from Exile | [28, 18] | 35 | (Representative Cabinet OR Revolutionary Courts) | — |
| `COLDWAR_IRQ_sciri_independent_relations` | Relations with Iran | [27, 19] | 35 | (The Return from Exile) | Patronage Compact |
| `COLDWAR_IRQ_sciri_patron_compact` | Patronage Compact | [29, 19] | 35 | (The Return from Exile) | Relations with Iran |
| `COLDWAR_IRQ_sciri_border_agreement` | Non-Interference | [27, 20] | 35 | (Relations with Iran) | — |
| `COLDWAR_IRQ_sciri_aid_terms` | Publish the Aid Terms | [29, 20] | 35 | (Patronage Compact) | — |
| `COLDWAR_IRQ_sciri_security_state` | Civilian Force Control | [28, 21] | 35 | (Non-Interference OR Publish the Aid Terms) | — |
| `COLDWAR_IRQ_sciri_southern_reconstruction` | Southern Recovery | [26, 22] | 49 | (Civilian Force Control) | — |
| `COLDWAR_IRQ_sciri_religious_education` | Religion and Skills | [28, 22] | 35 | (Civilian Force Control) | — |
| `COLDWAR_IRQ_sciri_minority_charter` | Minority Rights Charter | [30, 22] | 35 | (Civilian Force Control) | — |
| `COLDWAR_IRQ_sciri_water_services` | Southern Water | [26, 23] | 35 | (Southern Recovery) | — |
| `COLDWAR_IRQ_sciri_school_access` | Equal School Access | [28, 23] | 35 | (Religion and Skills) | — |
| `COLDWAR_IRQ_sciri_civil_review` | Civilian Review | [30, 23] | 35 | (Minority Rights Charter) | — |
| `COLDWAR_IRQ_sciri_iraqi_mandate` | Governing Mandate | [28, 24] | 49 | (Southern Water OR Equal School Access OR Civilian Review) | — |

## The Iraqi Islamic Party

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_iip_return` | The IIP Returns | [36, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_iip_parliamentary` | Parliamentary Islamism | [35, 16] | 35 | (The IIP Returns) | Party-Directed State |
| `COLDWAR_IRQ_iip_directorial` | Party-Directed State | [37, 16] | 35 | (The IIP Returns) | Parliamentary Islamism |
| `COLDWAR_IRQ_iip_law` | Religious Law | [35, 17] | 35 | (Parliamentary Islamism) | — |
| `COLDWAR_IRQ_iip_associations` | Association Network | [37, 17] | 35 | (Party-Directed State) | — |
| `COLDWAR_IRQ_iip_civil_service` | Conservative Cabinet | [36, 18] | 35 | (Religious Law OR Association Network) | — |
| `COLDWAR_IRQ_iip_social_market` | Islamic Social Market | [35, 19] | 35 | (Conservative Cabinet) | Conservative Welfare |
| `COLDWAR_IRQ_iip_welfare` | Conservative Welfare | [37, 19] | 35 | (Conservative Cabinet) | Islamic Social Market |
| `COLDWAR_IRQ_iip_business_law` | Small Business Law | [35, 20] | 35 | (Islamic Social Market) | — |
| `COLDWAR_IRQ_iip_charity_accounts` | Charity Accounts | [37, 20] | 35 | (Conservative Welfare) | — |
| `COLDWAR_IRQ_iip_national_compact` | Citizenship Compact | [36, 21] | 35 | (Small Business Law OR Charity Accounts) | — |
| `COLDWAR_IRQ_iip_education` | Community Education | [34, 22] | 35 | (Citizenship Compact) | — |
| `COLDWAR_IRQ_iip_foreign_policy` | IIP Foreign Policy | [36, 22] | 35 | (Citizenship Compact) | — |
| `COLDWAR_IRQ_iip_labour_compromise` | A Labour Compromise | [38, 22] | 35 | (Citizenship Compact) | — |
| `COLDWAR_IRQ_iip_public_service` | Service Examinations | [34, 23] | 35 | (Community Education) | — |
| `COLDWAR_IRQ_iip_arab_offer` | Arab Civil Partnership | [36, 23] | 35 | (IIP Foreign Policy) | — |
| `COLDWAR_IRQ_iip_medical_welfare` | Community Welfare | [38, 23] | 35 | (A Labour Compromise) | — |
| `COLDWAR_IRQ_iip_government_mandate` | Renew the Mandate | [36, 24] | 49 | (Service Examinations OR Arab Civil Partnership OR Community Welfare) | — |

## Oil, Revenue and Sovereignty

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_oil_accounts` | Concession Accounts | [44, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_oil_nationalize` | Nationalize the IPC | [44, 16] | 35 | (Concession Accounts) | New Concession Terms |
| `COLDWAR_IRQ_oil_renegotiate` | New Concession Terms | [46, 16] | 35 | (Concession Accounts) | Nationalize the IPC |
| `COLDWAR_IRQ_oil_state_company` | National Oil Service | [42, 17] | 35 | (Nationalize the IPC) | — |
| `COLDWAR_IRQ_oil_concession_delivery` | Revised Oil Contract | [48, 17] | 35 | (New Concession Terms) | — |
| `COLDWAR_IRQ_oil_technical_training` | Train Iraqi Oil Engineers | [45, 17] | 35 | (Nationalize the IPC OR New Concession Terms) | — |
| `COLDWAR_IRQ_oil_revenue_state` | An Oil Revenue State | [44, 18] | 35 | (Train Iraqi Oil Engineers) | Beyond Oil |
| `COLDWAR_IRQ_oil_diversification` | Beyond Oil | [46, 18] | 35 | (Train Iraqi Oil Engineers) | An Oil Revenue State |
| `COLDWAR_IRQ_oil_export_terminals` | Expand Export Handling | [42, 19] | 49 | (An Oil Revenue State) | — |
| `COLDWAR_IRQ_oil_industrial_fund` | Non-Oil Industry | [48, 19] | 49 | (Beyond Oil) | — |
| `COLDWAR_IRQ_oil_revenue_ledger` | One Oil Revenue Ledger | [45, 19] | 35 | (An Oil Revenue State OR Beyond Oil) | — |
| `COLDWAR_IRQ_oil_kirkuk_survey` | Kirkuk Production | [43, 20] | 35 | (One Oil Revenue Ledger) | — |
| `COLDWAR_IRQ_oil_baiji` | Baiji Refining | [45, 20] | 35 | (One Oil Revenue Ledger) | — |
| `COLDWAR_IRQ_oil_reserve_policy` | Petroleum Reserves | [47, 20] | 35 | (One Oil Revenue Ledger) | — |
| `COLDWAR_IRQ_oil_field_maintenance` | The Producing Fields | [43, 21] | 35 | (Kirkuk Production) | — |
| `COLDWAR_IRQ_oil_operators` | Refinery Operators | [45, 21] | 35 | (Baiji Refining) | — |
| `COLDWAR_IRQ_oil_contract_review` | Export Contract Review | [47, 21] | 35 | (Petroleum Reserves) | — |
| `COLDWAR_IRQ_oil_sovereignty` | Sovereign Accounts | [45, 22] | 49 | (The Producing Fields OR Refinery Operators OR Export Contract Review) | — |

## Industry, Power and Infrastructure

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_industry_survey` | Industrial Capacity | [52, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_industry_heavy` | Heavy Industry | [50, 16] | 35 | (Industrial Capacity) | Light Industry |
| `COLDWAR_IRQ_industry_light` | Light Industry | [54, 16] | 35 | (Industrial Capacity) | Heavy Industry |
| `COLDWAR_IRQ_industry_steel` | Industrial Workshops | [50, 17] | 49 | (Heavy Industry) | — |
| `COLDWAR_IRQ_industry_consumers` | Consumer Industry | [55, 17] | 49 | (Light Industry) | — |
| `COLDWAR_IRQ_industry_power_grid` | Industrial Power Grid | [52, 17] | 35 | (Heavy Industry OR Light Industry) | — |
| `COLDWAR_IRQ_industry_public_finance` | Public Finance | [50, 18] | 35 | (Industrial Power Grid) | Development Credit |
| `COLDWAR_IRQ_industry_credit_finance` | Development Credit | [54, 18] | 35 | (Industrial Power Grid) | Public Finance |
| `COLDWAR_IRQ_industry_public_accounts` | Audit State Investment | [50, 19] | 35 | (Public Finance) | — |
| `COLDWAR_IRQ_industry_debt_accounts` | Industrial Debt Service | [54, 19] | 35 | (Development Credit) | — |
| `COLDWAR_IRQ_industry_maintenance` | Industrial Maintenance | [52, 20] | 35 | (Audit State Investment OR Industrial Debt Service) | — |
| `COLDWAR_IRQ_industry_power` | Thermal Power Project | [50, 21] | 49 | (Industrial Maintenance) | — |
| `COLDWAR_IRQ_industry_machine_tools` | Machine-Tool Skills | [52, 21] | 35 | (Industrial Maintenance) | — |
| `COLDWAR_IRQ_industry_commercial_services` | Commercial Services | [54, 21] | 49 | (Industrial Maintenance) | — |
| `COLDWAR_IRQ_industry_grid_management` | Power Dispatch | [50, 22] | 35 | (Thermal Power Project) | — |
| `COLDWAR_IRQ_industry_quality` | Quality Inspection | [52, 22] | 35 | (Machine-Tool Skills) | — |
| `COLDWAR_IRQ_industry_tax_service` | Tax Records | [54, 22] | 35 | (Commercial Services) | — |
| `COLDWAR_IRQ_industry_delivery_review` | Industrial Review | [52, 23] | 49 | (Power Dispatch) AND (Quality Inspection) AND (Tax Records) | — |

## Land, Water and Rural Iraq

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_agri_land_survey` | Survey the Land Reform | [60, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_agri_cooperatives` | Farm Cooperatives | [60, 16] | 35 | (Survey the Land Reform) | Support Smallholders |
| `COLDWAR_IRQ_agri_smallholders` | Support Smallholders | [62, 16] | 35 | (Survey the Land Reform) | Farm Cooperatives |
| `COLDWAR_IRQ_agri_cooperative_credit` | Cooperative Equipment | [60, 17] | 35 | (Farm Cooperatives) | — |
| `COLDWAR_IRQ_agri_smallholder_credit` | Rural Credit Guarantee | [62, 17] | 35 | (Support Smallholders) | — |
| `COLDWAR_IRQ_agri_water_accounts` | Two Rivers Accounts | [61, 18] | 35 | (Cooperative Equipment OR Rural Credit Guarantee) | — |
| `COLDWAR_IRQ_agri_large_irrigation` | Large Irrigation Works | [60, 19] | 35 | (Two Rivers Accounts) | Local Irrigation |
| `COLDWAR_IRQ_agri_local_irrigation` | Local Irrigation | [62, 19] | 35 | (Two Rivers Accounts) | Large Irrigation Works |
| `COLDWAR_IRQ_agri_wasit` | Fund Works in Wasit | [58, 20] | 49 | (Large Irrigation Works) | — |
| `COLDWAR_IRQ_agri_dhiqar` | Fund Works in Dhi Qar | [64, 20] | 49 | (Local Irrigation) | — |
| `COLDWAR_IRQ_agri_extension` | Rural Extension Service | [61, 20] | 35 | (Large Irrigation Works OR Local Irrigation) | — |
| `COLDWAR_IRQ_agri_grain_storage` | Grain and Rural Roads | [59, 21] | 35 | (Rural Extension Service) | — |
| `COLDWAR_IRQ_agri_river_talks` | Upstream Water Rules | [61, 21] | 35 | (Rural Extension Service) | — |
| `COLDWAR_IRQ_agri_marsh_livelihoods` | Marsh Livelihoods | [63, 21] | 35 | (Rural Extension Service) | — |
| `COLDWAR_IRQ_agri_distribution` | Rural Distribution | [59, 22] | 35 | (Grain and Rural Roads) | — |
| `COLDWAR_IRQ_agri_water_inspection` | Water Inspectorate | [61, 22] | 35 | (Upstream Water Rules) | — |
| `COLDWAR_IRQ_agri_clinics` | Mobile Rural Clinics | [63, 22] | 35 | (Marsh Livelihoods) | — |
| `COLDWAR_IRQ_agri_reform_delivery` | The Rural Reform | [61, 23] | 49 | (Rural Distribution) AND (Water Inspectorate) AND (Mobile Rural Clinics) | — |

## Education and the Social Bargain

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_society_baseline` | Schools and Skills | [68, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_society_mass_literacy` | Mass Literacy | [66, 16] | 35 | (Schools and Skills) | Train Teachers First |
| `COLDWAR_IRQ_society_teacher_first` | Train Teachers First | [70, 16] | 35 | (Schools and Skills) | Mass Literacy |
| `COLDWAR_IRQ_society_evening_classes` | Adult Evening Classes | [66, 17] | 35 | (Mass Literacy) | — |
| `COLDWAR_IRQ_society_teacher_deployment` | Deploy the Teachers | [70, 17] | 35 | (Train Teachers First) | — |
| `COLDWAR_IRQ_society_literacy_accounts` | Measure Literacy Gains | [68, 18] | 35 | (Adult Evening Classes OR Deploy the Teachers) | — |
| `COLDWAR_IRQ_society_universal_services` | Universal Services | [66, 19] | 35 | (Measure Literacy Gains) | Targeted Services |
| `COLDWAR_IRQ_society_targeted_services` | Targeted Services | [70, 19] | 35 | (Measure Literacy Gains) | Universal Services |
| `COLDWAR_IRQ_society_primary_care` | Provincial Primary Care | [66, 20] | 35 | (Universal Services) | — |
| `COLDWAR_IRQ_society_priority_districts` | Neglected Districts | [70, 20] | 35 | (Targeted Services) | — |
| `COLDWAR_IRQ_society_budget_review` | A Funded Social Budget | [68, 21] | 35 | (Provincial Primary Care OR Neglected Districts) | — |
| `COLDWAR_IRQ_society_women_education` | Women and Skills | [66, 22] | 35 | (A Funded Social Budget) | — |
| `COLDWAR_IRQ_society_housing` | Housing and Services | [68, 22] | 49 | (A Funded Social Budget) | — |
| `COLDWAR_IRQ_society_technical_colleges` | Technical Colleges | [70, 22] | 35 | (A Funded Social Budget) | — |
| `COLDWAR_IRQ_society_rural_schooling` | Rural School Access | [66, 23] | 35 | (Women and Skills) | — |
| `COLDWAR_IRQ_society_municipal_finance` | Municipal Revenue | [68, 23] | 35 | (Housing and Services) | — |
| `COLDWAR_IRQ_society_science_maintenance` | Maintain Laboratories | [70, 23] | 35 | (Technical Colleges) | — |
| `COLDWAR_IRQ_society_service_compact` | A Service Compact | [68, 24] | 49 | (Rural School Access) AND (Municipal Revenue) AND (Maintain Laboratories) | — |

## The Armed Forces

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_defence_accounts` | Audit the Armed Forces | [76, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_defence_professional` | A Professional Core | [74, 16] | 35 | (Audit the Armed Forces) | A Mass Reserve Army |
| `COLDWAR_IRQ_defence_mass` | A Mass Reserve Army | [76, 16] | 35 | (Audit the Armed Forces) | A Professional Core |
| `COLDWAR_IRQ_defence_staff_training` | Fund Staff Training | [74, 17] | 35 | (A Professional Core) | — |
| `COLDWAR_IRQ_defence_reserve_training` | Train the Reserves | [76, 17] | 35 | (A Mass Reserve Army) | — |
| `COLDWAR_IRQ_defence_procurement_board` | Procurement Board | [75, 18] | 35 | (Fund Staff Training OR Train the Reserves) | — |
| `COLDWAR_IRQ_defence_soviet_standard` | Soviet Supply Standards | [74, 19] | 35 | (Procurement Board) | Diverse Suppliers |
| `COLDWAR_IRQ_defence_mixed_supply` | Diverse Suppliers | [76, 19] | 35 | (Procurement Board) | Soviet Supply Standards |
| `COLDWAR_IRQ_defence_soviet_offer` | Advisory Mission | [74, 20] | 35 | (Soviet Supply Standards) | — |
| `COLDWAR_IRQ_defence_maintenance_manuals` | Maintenance System | [76, 20] | 35 | (Diverse Suppliers) | — |
| `COLDWAR_IRQ_defence_logistics` | Unified Logistics | [75, 21] | 35 | (Advisory Mission OR Maintenance System) | — |
| `COLDWAR_IRQ_defence_land_schools` | Army Training Schools | [73, 22] | 35 | (Unified Logistics) | — |
| `COLDWAR_IRQ_defence_air_maintenance` | Air Maintenance | [75, 22] | 35 | (Unified Logistics) | — |
| `COLDWAR_IRQ_defence_coastal` | Coastal Defence | [77, 22] | 49 | (Unified Logistics) | — |
| `COLDWAR_IRQ_defence_armaments` | Local Armaments | [73, 23] | 49 | (Army Training Schools) | — |
| `COLDWAR_IRQ_defence_fuel_discipline` | Fuel Discipline | [75, 23] | 35 | (Air Maintenance) | — |
| `COLDWAR_IRQ_defence_ship_maintenance` | The Coastal Fleet | [77, 23] | 35 | (Coastal Defence) | — |
| `COLDWAR_IRQ_defence_readiness` | Sustainable Readiness | [75, 24] | 49 | (Local Armaments OR The Coastal Fleet) AND (Fuel Discipline) | — |

## War, Restraint and Reconstruction

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_war_contingency` | Contingency Planning | [84, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_war_restraint` | Armed Restraint | [82, 16] | 35 | (Contingency Planning) | An Offensive Option |
| `COLDWAR_IRQ_war_offensive_option` | An Offensive Option | [86, 16] | 35 | (Contingency Planning) | Armed Restraint |
| `COLDWAR_IRQ_war_crisis_channel` | Crisis Channel | [82, 17] | 35 | (Armed Restraint) | — |
| `COLDWAR_IRQ_war_deliberate_authority` | Authorize War | [86, 17] | 35 | (An Offensive Option) | — |
| `COLDWAR_IRQ_war_civil_continuity` | Civil Crisis Authority | [84, 18] | 35 | (Crisis Channel OR Authorize War) | — |
| `COLDWAR_IRQ_war_economy` | War Economy | [82, 19] | 35 | (Civil Crisis Authority) | A Civilian Budget Floor |
| `COLDWAR_IRQ_war_civilian_floor` | A Civilian Budget Floor | [86, 19] | 35 | (Civil Crisis Authority) | War Economy |
| `COLDWAR_IRQ_war_procurement_cycle` | Wartime Procurement | [82, 20] | 35 | (War Economy) | — |
| `COLDWAR_IRQ_war_services_continuity` | Civilian Services | [86, 20] | 35 | (A Civilian Budget Floor) | — |
| `COLDWAR_IRQ_war_accounts` | Emergency Accounts | [84, 21] | 35 | (Wartime Procurement OR Civilian Services) | — |
| `COLDWAR_IRQ_war_veterans` | Veterans and Victims | [82, 22] | 35 | (Emergency Accounts) | — |
| `COLDWAR_IRQ_war_reconstruction` | Civilian Reconstruction | [84, 22] | 49 | (Emergency Accounts) | — |
| `COLDWAR_IRQ_war_credit_burden` | Confront Postwar Debt | [86, 22] | 35 | (Emergency Accounts) | — |
| `COLDWAR_IRQ_war_reintegration` | Reintegration | [82, 23] | 35 | (Veterans and Victims) | — |
| `COLDWAR_IRQ_war_recovery_contracts` | Recovery Contracts | [84, 23] | 35 | (Civilian Reconstruction) | — |
| `COLDWAR_IRQ_war_sanctions_response` | Sanctions Response | [86, 23] | 35 | (Confront Postwar Debt) | — |
| `COLDWAR_IRQ_war_peace_dividend` | Peace Settlement | [84, 24] | 49 | (Reintegration OR Recovery Contracts OR Sanctions Response) | — |

## Iran: Road to War

| Focus ID | English title | x,y | Days | Prerequisite groups | Exclusive with |
|---|---|---|---|---|---|
| `COLDWAR_IRQ_iran_frontier` | The Iranian Frontier | [94, 15] | 21 | Entry | — |
| `COLDWAR_IRQ_iran_shatt_demand` | Enforce the Shatt Claim | [92, 16] | 21 | (The Iranian Frontier) | — |
| `COLDWAR_IRQ_iran_arabistan_claim` | The Arabistan Claim | [96, 16] | 21 | (The Iranian Frontier) | — |
| `COLDWAR_IRQ_iran_southern_command` | Southern Command | [92, 17] | 35 | (Enforce the Shatt Claim) | — |
| `COLDWAR_IRQ_iran_tehran_assessment` | Assess Tehran's Army | [96, 17] | 21 | (The Arabistan Claim) | — |
| `COLDWAR_IRQ_iran_operational_plan` | The Southern War Plan | [94, 18] | 35 | (Southern Command) AND (Assess Tehran's Army) | — |
| `COLDWAR_IRQ_iran_short_war` | A Short Sharp War | [92, 19] | 35 | (The Southern War Plan) | Prepare a Long War |
| `COLDWAR_IRQ_iran_sustained_war` | Prepare a Long War | [96, 19] | 35 | (The Southern War Plan) | A Short Sharp War |
| `COLDWAR_IRQ_iran_fuel_spares` | Fuel and Spares | [92, 20] | 35 | (A Short Sharp War) | — |
| `COLDWAR_IRQ_iran_mobilisation_base` | Build the War Reserve | [96, 20] | 49 | (Prepare a Long War) | — |
| `COLDWAR_IRQ_iran_gulf_credit` | Seek Gulf Backing | [90, 21] | 21 | (Fuel and Spares) | — |
| `COLDWAR_IRQ_iran_forward_depots` | Forward Supply Depots | [92, 21] | 35 | (Fuel and Spares) | — |
| `COLDWAR_IRQ_iran_war_contracts` | Mobilise War Contracts | [96, 21] | 35 | (Build the War Reserve) | — |
| `COLDWAR_IRQ_iran_supplier_access` | Secure Foreign Spares | [98, 21] | 21 | (Build the War Reserve) | — |
| `COLDWAR_IRQ_iran_final_ultimatum` | The Final Ultimatum | [94, 22] | 21 | (Forward Supply Depots OR Mobilise War Contracts) | — |
| `COLDWAR_IRQ_iran_launch_campaign` | Execute the War Plan | [92, 23] | 21 | (The Final Ultimatum) | — |
| `COLDWAR_IRQ_iran_home_front` | Mobilise the Nation | [96, 23] | 35 | (The Final Ultimatum) | — |
| `COLDWAR_IRQ_iran_campaign_accounts` | The Campaign Ledger | [94, 24] | 21 | (Execute the War Plan OR Mobilise the Nation) | — |
| `COLDWAR_IRQ_iran_secure_khuzestan` | Secure Khuzestan | [92, 25] | 35 | (The Campaign Ledger) | — |
| `COLDWAR_IRQ_iran_long_war` | Fight Through Attrition | [96, 25] | 21 | (The Campaign Ledger) | — |
| `COLDWAR_IRQ_iran_oil_rehabilitation` | Khuzestan Oilworks | [90, 26] | 49 | (Secure Khuzestan) | — |
| `COLDWAR_IRQ_iran_civil_administration` | Administer Arabistan | [92, 26] | 35 | (Secure Khuzestan) | — |
| `COLDWAR_IRQ_iran_war_of_reserves` | An Army of Reserves | [96, 26] | 35 | (Fight Through Attrition) | — |
| `COLDWAR_IRQ_iran_another_offensive` | Prepare Another Blow | [98, 26] | 21 | (Fight Through Attrition) | — |
| `COLDWAR_IRQ_iran_regional_power` | Arabistan Secured | [92, 27] | 49 | (Khuzestan Oilworks) AND (Administer Arabistan) | — |
| `COLDWAR_IRQ_iran_no_easy_exit` | Victory at Any Cost | [96, 27] | 49 | (An Army of Reserves) AND (Prepare Another Blow) | — |
| `COLDWAR_IRQ_iran_provincial_settlement` | A Provincial Settlement | [92, 28] | 49 | (Arabistan Secured) | — |
| `COLDWAR_IRQ_iran_equal_citizenship` | Equal Citizenship | [90, 29] | 49 | (A Provincial Settlement) | Central State Rule |
| `COLDWAR_IRQ_iran_central_administration` | Central State Rule | [94, 29] | 49 | (A Provincial Settlement) | Equal Citizenship |
| `COLDWAR_IRQ_iran_core_khuzestan` | An Iraqi Province | [92, 30] | 70 | (Equal Citizenship OR Central State Rule) | — |
