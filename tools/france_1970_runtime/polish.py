# IMPERIA COLD WAR — France 1970 national focus polish overlay.
"""Apply the approved France tree's AAA layout, prose and native art metadata.

This module does not write game files. The caller supplies the current design,
uses :func:`polish_design`, then merges the dictionaries returned by
:func:`build_art` into its own output plan.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any


PROJECT = "IMPERIA COLD WAR"
MD_SHINE_SOURCE = Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/interface/goals_shine.gfx")

# Each political programme keeps its own recognizable column. This reflows the
# ten upper programme blocks and the three shared lower sections into a tighter
# map while leaving every block's internal geometry, branch spacing and rows
# intact. The UDR NATO block moves with its Gaullist parent.
SECTION_X = {
    "institutions": 6,
    "udr": 18,
    "ri": 29,
    "centre": 39,
    "radical": 49,
    "ps": 59,
    "pcf": 69,
    "psu": 79,
    "ecology": 89,
    "right": 99,
    "economy": 34,
    "defence": 54,
    "diplomacy": 78,
    "udr_nato": 18,
}

TITLE_REVISIONS = {
    "progress": "Social Renewal",
    "new_society": "Chaban's New Deal",
    "ortf": "Public Broadcasting",
    "business": "Independent Firms",
    "radical_enterprise": "Private Innovation",
    "cdp_compromise": "CDP Cooperation",
    "social_contract_ps": "Labour Compact",
    "redistribution": "Household Demand",
    "competitiveness_ps": "Productive Compact",
    "advanced_democracy": "Democratic Advance",
    "grassroots_left": "PSU Grassroots",
    "environment_account": "Ecological Politics",
    "cid_cooperatives": "Shopkeepers' Credit",
    "fn_protection": "National Protection",
    "fn_export": "Export Coalition",
    "regional_links": "Regional Links",
    "plan_calcul": "Plan Calcul Renewal",
    "transport_choice": "Rail or Motorway",
    "energy_review": "Energy Choices",
    "farm_policy": "Farm Settlement",
    "defence_review": "Defence Priorities",
    "service_review": "Conscription Reform",
    "land_procurement": "Armour Procurement",
    "air_programme": "Combat Aircraft",
    "flight_schools": "Flight Safety",
    "diplomatic_review": "An Independent Voice",
    "airbus": "Airbus Partnership",
    "symphonie": "Symphonie Satellite",
    "ariane": "A European Launcher",
    "us_science": "US Research Accord",
    "algeria_energy": "Algerian Energy",
    "iran_energy": "Iranian Energy",
    "algeria_training": "Algerian Institutes",
    "senegal_civil": "Senegal Civil Ties",
    "senegal_defence": "Senegal Defence",
    "rhine": "Rhine Industry Pact",
    "italy": "Italian Cooperation",
    "community_entry": "EEC Cooperation",
    "nato_review": "France and NATO",
    "nato_europe_sea": "European Naval Pact",
    "nato_europe_staff": "Joint Naval Staffs",
}

# These are editorial refinements to the already-approved prose. Each keeps
# the focus's approved institutional subject and reward trade-off intact.
DESCRIPTION_REVISIONS = {
    "public_service": "Pompidou's government inherited a central administration shaped by prefects and powerful ministries. Better local services can make that authority more useful to citizens while preserving the elected role of communes.",
    "executive": "The Fifth Republic gives the presidency decisive authority. Clarifying the statutory limits around emergency powers can protect the mandate while leaving Parliament with fewer checks on executive action.",
    "parliament": "Give deputies and committees a stronger role in questioning ministers and scrutinising appointments. The aim is a more accountable Fifth Republic, not a return to the cabinet instability of the Fourth.",
    "contract": "Bring employers and organised labour into regular national bargaining. Wage gains can support demand and industrial peace, but they require investment and a durable public commitment to social provision.",
    "statute": "Set national minimum protections and clear procedures for industrial action. Statutory rules can make disputes more predictable, although standards imposed from Paris may weaken workplace consent.",
    "housing": "SONACOTRA and local authorities already house workers and families displaced by rapid urban growth. Extend serviced housing around Paris and replace precarious accommodation with lasting municipal services.",
    "memory": "Veterans, harkis, repatriates and Algerian families carry distinct experiences of the war and its aftermath. Public recognition can make room for those histories, but it must be joined to practical support.",
    "amnesty": "Extend the late-1960s amnesties to close some domestic disputes left by the Algerian conflict. Reconciliation can reduce political division, while victims' claims and disagreements over public memory remain unresolved.",
    "civic_settlement": "Build integration and public remembrance into the ordinary work of republican institutions. Citizens need not share one account of the end of empire for public services to treat them fairly.",
    "progress": "Chaban-Delmas wants employers, unions and public enterprises to negotiate change rather than repeat the confrontations of 1968. Pompidou must decide how much authority the government is willing to share.",
    "new_society": "Chaban-Delmas's New Society pairs administrative reform with broader workplace participation. Technical training and bargaining give the proposal material weight, while conservative Gaullists resist a lasting opening to organised labour.",
    "ortf": "The ORTF combines public broadcasting with close executive supervision. Give editors and broadcasters more professional room while retaining public service obligations and limiting the government's influence over the news.",
    "national_champions": "Use Rhone-Alpes production capacity and public contracts to strengthen French suppliers. Scale and export orders can improve industrial depth, but tax concessions reduce public revenue and reinforce established firms.",
    "management": "Let public enterprises set investment and staffing plans with greater commercial independence. Clearer management responsibility can improve performance, but workers lose some protection from political guarantees.",
    "debre": "Debre's Gaullist tradition puts national authority first in defence policy. Preserve a French procurement base and freedom of decision, accepting higher costs than shared development can offer.",
    "pompidou_europe": "The Hague summit reopened enlargement and practical cooperation after years of French obstruction. Use that opening to shape a stronger Community without surrendering France's independent voice.",
    "gaullist_success": "Turn the 1968 parliamentary majority into a programme that can survive de Gaulle's departure. Pompidou and Chaban-Delmas must balance social reform, industrial growth and the authority of the Gaullist movement.",
    "liberal_state": "Giscard's Independent Republicans favour administrative competence and room for private initiative. Reform can widen enterprise while placing limits on established public privileges and discretionary state support.",
    "credit_expansion": "Direct lower-cost credit toward modern equipment, housing and productive investment. Faster renewal supports growth, but the subsidy leaves the Treasury exposed if private projects underperform.",
    "business": "Open credit and public contracts to independent firms and professional services in Rhone-Alpes. A wider enterprise base strengthens local office activity, while tax concessions reduce the immediate return to the state.",
    "public_credit": "Retain public guarantees for major investment while requiring transparent commercial accounts. Credit can reach projects that private lenders avoid, but the state accepts their financial risk.",
    "civil_liberties": "Extend civil rights and remove legal barriers facing women and younger citizens. Equal citizenship strengthens the Republic, while implementation requires continuing legal and social provision.",
    "social_market": "Lecanuet's Democratic Centre joins market initiative to social responsibility and parliamentary government. It offers a distinct Christian democratic programme between presidential concentration and socialist planning.",
    "regional_councils": "Give elected regional councils resources to shape local investment. Decisions closer to residents gain legitimacy, while Paris gives up some control over the timing and direction of development.",
    "cdp_compromise": "The Centre democrats can use coalition influence to secure practical reforms without adopting the full presidential programme. Cooperation gains access to government, but blurs the party's distance from the majority.",
    "mutuals": "Mutual societies and local insurance funds already connect households to health and social provision. Strengthen their administrative capacity while sustaining the wider public contribution on which coverage depends.",
    "federal_europe": "Give European institutions a stronger role in shared decisions. France can shape common capacity through negotiation, but accepts limits on unilateral action when partners disagree.",
    "atlantic_security": "Work more closely with allied governments on European security and direct national resources toward public services. The arrangement improves cooperation while narrowing France's independent military choices.",
    "american_challenge": "Servan-Schreiber argues that France must answer American industrial scale with education, modern management and a larger European market. The effort asks firms and public institutions to change together.",
    "radical_enterprise": "Open credit and public procurement to innovative firms outside the established industrial groups. Faster renewal can widen competition, while tax concessions reduce public income.",
    "left_radicals": "Follow the republican left tradition of secular public services and cooperation with democratic socialists. Reform can advance without abandoning the Radical Party's independent institutional identity.",
    "secular_school": "Strengthen the common public school and technical routes beyond the grandes ecoles. Wider access can reduce inherited barriers, but it depends on sustained funding and trained teachers.",
    "municipal_france": "Aquitaine's market towns, cooperatives and local authorities can bring investment closer to producers. Offices and agricultural processing reinforce municipal services, while regional administration carries a continuing cost.",
    "europe_technology": "Pool research and development across European firms where shared standards lower costs. French companies gain access to larger projects but keep a smaller share of procurement at home.",
    "socialist_refoundation": "The Socialist Party is still rebuilding after the weakening of the SFIO and Guy Mollet's leadership. Alain Savary can broaden the democratic left by negotiating with republican clubs without pretending the 1971 Epinay settlement has already happened.",
    "common_programme": "Negotiate with the PCF and left radicals over public ownership, wages and social rights. A common platform can make the left electable, but every partner must accept limits on its own programme.",
    "democratic_left": "Build a socialist majority through republican alliances and preserve a clear distance from the PCF. Greater room for coalition can attract voters while making labour unity harder to sustain.",
    "public_banks": "Equip public credit institutions to direct investment toward industrial modernisation. Offices and specialist staff expand the state's financial reach, while a larger administrative establishment must be maintained.",
    "social_contract_ps": "Put negotiated wage standards and reliable public services at the centre of a socialist government. Agreement with employers can protect employment, but postpones a broader transfer of ownership.",
    "redistribution": "Raise household purchasing power and expand public employment to sustain domestic demand. The policy broadens social gains, while its tax and wage effects challenge fiscal balance and export competitiveness.",
    "competitiveness_ps": "Slow the expansion of current benefits to direct more resources toward investment, training and export capacity. The compact can strengthen future production, though households see fewer immediate gains.",
    "defferre": "Continue the decentralising reforms associated with Gaston Defferre and give Provence a first regional service programme. Elected institutions gain practical authority as the central state relinquishes some control.",
    "europe_restraint": "Keep a socialist government's finances within a European monetary framework. Credibility can protect the franc and access to markets, but restraint slows the pace of domestic reform.",
    "sovereign_reflation": "Use national control of credit and demand to accelerate investment without an external monetary constraint. Expansion can protect employment, but risks pressure on the franc and friction with European partners.",
    "advanced_democracy": "Build on PCF-led municipalities, unions and parliamentary work to seek national power. Electoral advances broaden the party's reach but do not settle the future balance between party leadership and state institutions.",
    "democratic_road": "Accept pluralist competition and a negotiated transition to socialism. Broader legitimacy can reassure democratic allies, while limiting the authority of the Communist Party apparatus.",
    "party_discipline": "Prioritise cadre cohesion and central direction in a hostile political environment. A disciplined organisation can carry a programme through opposition, but deepens mistrust among potential allies.",
    "municipal_socialism": "Carry the housing, school and cultural-service record of PCF municipalities into a wider investment programme. Local provision grows, while national coordination adds to the public commitment.",
    "workers_control": "Give elected workplace representatives a binding role in company planning. Representation can build consent for change, though shared decisions may take longer to reach.",
    "planned_targets": "Direct investment toward a limited number of industrial priorities. Clear targets can concentrate effort, but compete with household supply, local needs and managers' discretion.",
    "independent_communism": "Set a French course for the PCF and keep national decisions independent of Soviet direction. A distinct line can strengthen domestic legitimacy while loosening ties to orthodox networks.",
    "soviet_friendship": "Build civilian technical and industrial cooperation on the Franco-Soviet relationship. Access to Soviet expertise can support development, while political closeness tests the autonomy of French policy.",
    "communist_settlement": "Consolidate the institutions and economic commitments of the chosen PCF course. The settlement makes its political direction durable and closes room for later reversal.",
    "grassroots_left": "Give local militants, young workers and university activists a route into national decisions outside the larger socialist and communist parties. Participation broadens the PSU's reach but makes coordination harder.",
    "self_management": "Support a cooperative industrial pilot in Bourgogne with credit and technical advice. Workplace self-management needs commercial access and capital as well as the consent of workers.",
    "union_autonomy": "Protect independent unions and negotiate sector agreements without transferring ownership to workplace councils. Organised labour gains room to act while employers retain control of production.",
    "decentralised_services": "Move social and educational services closer to the communities they serve. Local delivery can improve access, but depends on trained staff and reliable funding outside Paris.",
    "civilian_republic": "Reduce the priority accorded to military institutions and direct more attention to social investment. A less militarised public course narrows the resources available for mobilisation.",
    "citizen_defence": "Keep a citizen defence commitment alongside a broad public-service programme. Local organisations can contribute to resilience, while training and readiness remain national obligations.",
    "environment_account": "Make pollution and resource use part of public accounting. Ecological politics is emerging from disputes over the social and environmental costs of rapid postwar development.",
    "efficiency_ecology": "Improve insulation, transport efficiency and industrial processes before expanding supply. Conservation lowers future demand but requires investment before savings appear.",
    "local_generation": "Use engineering and regional coordination to improve existing hydroelectric and distributed generation. Better use of local resources requires trained operators and sustained technical administration.",
    "land_stewardship": "Support rural services and farming that relies less on purchased industrial inputs. Smaller holdings and local employment gain support, though yields may grow more slowly.",
    "ecological_industry": "Help industrial firms convert production and retrain workers rather than simply close. Cleaner processes can open new markets, but transition costs weigh on short-term output.",
    "local_sufficiency": "Prioritise local production and shorter supply chains. Lower transport and energy demand comes at the cost of smaller markets and less industrial scale.",
    "cid_tax": "Pierre Poujade's CID challenges the tax and social-charge burden on independent traders. Relief can protect small shops, but shifts revenue needs onto the wider public budget.",
    "cid_cooperatives": "Give independent shopkeepers access to credit and mutual support as retail distribution concentrates. Cooperation helps local traders compete without turning them into a state-controlled sector.",
    "fn_state": "A marginal nationalist movement seeks national authority through a major alternate-history shift. Central discipline and exclusion carry serious costs to public trust and republican institutions.",
    "fn_protection": "Shelter French producers from external competition. Guaranteed markets can protect employment and output, but reduce pressure to renew technology and improve productivity.",
    "fn_export": "Join export firms to a nationalist economic programme. Foreign sales earn revenue, while dependence on outside markets conflicts with promises of economic closure.",
    "fn_defence": "Prioritise territorial mobilisation and a national armaments base. Sustained readiness raises costs and gives military preparation a larger place in public life.",
    "sixth_plan": "The Sixth Plan, approved in 1970, must balance modern exporters, older industrial districts and underserved regions. Investment choices will shape whether growth reaches beyond the largest firms and cities.",
    "regional_links": "Connect regional producers with ports, railways and industrial markets. Better access can spread employment beyond established centres, but transport investment competes with other public projects.",
    "technical_colleges": "Expand engineering and technician training beyond the elite schools. Practical qualifications can ease bottlenecks in modern industry, while requiring teachers, workshops and lasting education funds.",
    "mass_universities": "Put the Faure reforms into practice and widen access to university study. More open institutions strengthen research and social mobility, but require a larger permanent education budget.",
    "champion_model": "Concentrate public capital and procurement on firms able to compete internationally. Scale supports exports, but raises fiscal exposure and sustains regional concentration.",
    "regional_industry": "Prepare industrial sites in Hauts-de-France and expand port capacity in Provence. Regional investment supports conversion and new suppliers without granting a completed industrial complex by decree.",
    "territorial_balance": "Tie regional transport to the chosen industrial strategy. Investment can narrow the inherited gap in access to modern production, although it cannot remove the advantages of the largest centres at once.",
    "plan_calcul": "Renew the Plan Calcul through IRIA, domestic procurement and trained engineers. French computing needs a dependable market if it is to compete with established foreign suppliers.",
    "national_computers": "Back the domestic computer-systems industry and Grenoble's engineering base with a funded production site. Independent supply requires public orders and continuing fiscal concessions.",
    "open_computers": "Adopt international standards and concentrate French engineering on competitive niches. Compatibility accelerates renewal, while making a fully independent supply chain less likely.",
    "transport_choice": "Choose how to connect a rapidly urbanising country. High-speed rail offers concentrated capacity; motorways reach dispersed industry, and both compete for public investment.",
    "tgv": "Fund SNCF engineering trials and the Lyon terminal and approaches. The 1970 study can prepare an experimental high-speed programme without claiming that commercial service already exists.",
    "motorways": "Extend road access to industrial towns and smaller centres. Flexible routes can support regional growth, while increasing the economy's dependence on imported motor fuel.",
    "energy_review": "Review fuel dependence before an external crisis forces emergency decisions. France must choose between capital-intensive generation and a broader mix of supply and demand measures.",
    "nuclear_scale": "Standardise the civil nuclear supply chain around the reactor choice made in 1970. Engineering and construction performance can improve, while every additional reactor still requires separate public investment.",
    "diverse_energy": "Pair more efficient use with a broader energy portfolio. Varied sources reduce concentration risk, though France remains exposed to imported fuel and supply changes.",
    "oil_resilience": "Reduce the assumption that imported oil will remain cheap and reliable. The programme improves resilience, while power stations and fuel contracts remain distinct national choices.",
    "farm_policy": "Decide how agricultural modernisation should divide its gains between export-scale production and the survival of smaller rural communities.",
    "export_farms": "Support mechanisation and processing for European and world markets. Larger farms can raise output and exports, but intensify pressure on small holdings and farm incomes.",
    "rural_services": "Sustain cooperative services and smaller farms so rural communities remain viable. The policy protects local employment, while accepting slower concentration and lower economies of scale.",
    "telecoms": "Modernise the PTT network through CNET research, switching equipment and long-distance links. New exchanges in Paris and Rhone-Alpes widen service, while demand still exceeds available connections.",
    "conversion": "Prepare coal, textile and steel districts for industrial change before closures become a national emergency. New skills and production can replace some work, but adjustment brings real losses to established communities.",
    "defence_review": "Set the balance between the national deterrent, conventional defence in Europe and overseas commitments. Each choice draws on the same skilled personnel, procurement base and public resources.",
    "nuclear_priority": "Keep the independent deterrent and its engineering base at the centre of defence policy. Conventional procurement and readiness must absorb the resulting pressure on resources.",
    "balanced_forces": "Retain the deterrent while giving deployable conventional forces a larger share of attention. A broader posture improves flexibility but cannot match every strategic priority at once.",
    "service_review": "Decide how conscription should fit a force expected to defend Europe and operate overseas. A broader citizen reserve and a smaller professional core make different claims on the state.",
    "citizen_army": "Improve reserve organisation and useful training for conscripts. Wider territorial readiness strengthens national resilience but requires a longer and more expensive training establishment.",
    "professional_core": "Build a smaller, high-readiness force for demanding deployments. Professional experience improves immediate capability, with a higher wage and support bill.",
    "land_procurement": "Choose the industrial basis of future land equipment. A national platform preserves French design authority; common components can lower costs if partners agree.",
    "national_armour": "Sustain a national armoured design line and its testing base. Domestic production retains expertise and control, but costs more than pooled procurement.",
    "pooled_armour": "Seek common components and negotiated procurement with partners. Lower unit costs depend on consent and leave French influence over the final design smaller.",
    "air_programme": "French air power depends on continuing design, testing and production. A national aircraft line and cooperative development answer different operational and industrial needs.",
    "mirage": "Sustain Dassault's national combat-aircraft design and export capability. A continuing engineering base supports future models without granting technology that has not yet been developed.",
    "jaguar_doctrine": "Build training and procurement arrangements around the Anglo-French Jaguar. Shared standards can lower costs, while operational planning remains subject to both governments' consent.",
    "naval_review": "Choose between distant oceanic presence and the routine work of escorting convoys, protecting approaches and maintaining the fleet.",
    "ocean_navy": "Sustain the dockyards and trained crews required for an oceanic fleet. Overseas presence expands French reach but needs a larger permanent personnel establishment.",
    "escort_navy": "Prioritise escorts, maintenance and protection of French approaches. Reliable routine coverage improves, while distant deployments receive less emphasis.",
    "logistics": "Standardise support across the services so readiness survives deployment. Common routines improve supply, but require a permanent maintenance organisation.",
    "flight_schools": "Train instructors and improve flight safety before increasing operational demands. Skilled crews take time to develop, and training competes with immediate readiness.",
    "diplomatic_review": "France can protect its independence through national capacity or through partnerships negotiated on equal terms. Decide where cooperation strengthens French influence and where it constrains it.",
    "airbus": "France and West Germany already committed to the A300 in 1969. Continue the national work share and industrial capacity through a renewed funding agreement, with both governments deciding whether to accept the new terms.",
    "concorde": "Deepen the Anglo-French supersonic programme. Prestige and advanced engineering support the partnership, while fuel use and uncertain demand threaten its commercial future.",
    "symphonie": "Continue the Franco-German Symphonie satellite programme through telecommunications research and ground applications. Launch access and permitted uses still require diplomatic agreement.",
    "ariane": "Negotiate a French-led European launcher with Germany as an alternate course. Shared engineering can widen access to space, but cannot remove the cost or the need for broader European consent.",
    "jaguar": "Renew Anglo-French cooperation around the Jaguar precedent. Common development and training can serve both air forces, while each government retains control of its own commitments.",
    "atlantic_training": "Negotiate technical training and logistics cooperation with the United States. Practical exchange does not place French forces under NATO's integrated command.",
    "soviet_science": "Build on the 1966 Franco-Soviet cooperation framework and the developing dialogue with Moscow. Civilian science offers room for exchange without imposing military alignment. Opening the programme requires bilateral restrictions to be lifted.",
    "us_science": "Seek a civilian research accord with American institutions as an alternative to Soviet cooperation. Both governments must decide whether shared access justifies its cost and external commitments.",
    "algeria_energy": "Renegotiate energy and industrial cooperation under Algerian sovereignty. The 1965 framework offers a starting point, while development priorities and future returns require mutual agreement.",
    "iran_energy": "Negotiate a separate energy and technical agreement with Iran. Supply diversification brings new commitments and competes with deeper educational cooperation elsewhere.",
    "algeria_training": "Extend the Algerian Petroleum Institute precedent into a lasting technical education partnership. Both governments fund training, and each retains the right to approve its own obligations.",
    "senegal_civil": "Offer Senegal a civilian partnership in public services and development. Dakar can choose this course instead of a relationship centred on French military presence.",
    "senegal_defence": "Renegotiate training and access under explicit Senegalese consent. The security arrangement preserves a defence option but commits both governments to continuing costs.",
    "rhine": "Link industrial conversion and technical training across neighbouring regions. Franco-German cooperation shares the cost of modernisation rather than assigning construction on foreign territory unilaterally.",
    "italy": "Offer Italy a joint machinery and industrial-research programme. Specialisation can benefit both economies, while each accepts a smaller national share of public contracts.",
    "community_entry": "Use the European Communities to shape enlargement and common policy. France acts through existing institutions, where membership rights and the interests of other governments still matter.",
    "nato_review": "France remains in the Atlantic Treaty after withdrawing from NATO's integrated command in 1966. Pompidou can reaffirm national discretion, deepen conditional cooperation or strengthen Europe's contribution without transferring authority over the French deterrent.",
    "nato_nuclear_veto": "Fund an independent assessment and decision system for the force de frappe. National authority reinforces the Gaullist mandate, while France bears the support burden of its separate capability.",
    "nato_nuclear_consult": "Consult allies on deterrence and escalation while reserving the final decision to France. Consultation grants neither Nuclear Planning Group membership nor nuclear sharing or an allied veto.",
    "nato_independent": "Keep Atlantic political solidarity while directing discretionary funds toward capabilities France can control and sustain. Independence reduces outside leverage but duplicates some equipment and support capacity.",
    "nato_pragmatic": "Expand liaison, exercises and contingency preparation under French authority. Practical cooperation improves support without assigning forces automatically to allied command, at the cost of a larger coordination staff.",
    "nato_european": "Concentrate new investment on European capability and compatible equipment. A stronger European voice in the Alliance requires technical preparation and sustained political coordination.",
    "nato_land_priority": "Fund French land equipment and training for an independent continental contribution. Domestic capacity expands while the equipment estate becomes more expensive to maintain.",
    "nato_sea_priority": "Direct the discretionary programme toward French naval construction and support. Greater shipyard capacity still requires crews, training and long-term maintenance.",
    "nato_land_design": "Carry the national land programme through design, testing and engineering. French expertise must be funded rather than granted through an automatic technology award.",
    "nato_sea_design": "Fund design teams and sea trials within French naval institutions. The programme develops expertise without granting ships or future hull technology.",
    "nato_rhine": "Offer West Germany an additional land-exercise programme alongside existing French forces in Germany. Each government retains control of its forces; the agreement creates neither new basing rights nor an automatic wartime commitment.",
    "nato_atlantic_fleet": "Offer Britain a funded programme of naval exercises and fleet-support training. Both governments retain freedom to decide whether to commit ships in a crisis.",
    "nato_conditional_plan": "Train national staffs to coordinate an agreed contingency while preserving France's decision on any military commitment. Reliable planning requires a continuing personnel allocation.",
    "nato_fleet_support": "Apply agreed naval-exercise lessons to French fleet support. More efficient supply can improve routine readiness, but requires a larger trained support establishment.",
    "nato_europe_land": "Offer West Germany a further programme for compatible land equipment and maintenance standards. Both countries can reduce support costs while financing technical work; no force passes to a new command.",
    "nato_europe_sea": "Offer Britain a European naval engineering and production partnership. Shared development supports both shipbuilding sectors and requires continuing public contributions.",
    "nato_common_maintenance": "Turn agreed land-equipment standards into training and support routines for French forces. The partnership provides experience while France funds its own personnel.",
    "nato_europe_staff": "Develop French naval doctrine through the agreed European industrial programme. Staff exchanges and technical analysis require permanent administrative support.",
}

# Source sprite names and native workshop texture paths were checked in the
# installed MD `interface/goals.gfx` and the earlier art contact sheet. The
# Gaullist programme deliberately uses the French Republic emblem, not FRA_cdg
# or a later RPR/UMP party mark. No images are copied or modified.
GOAL_TEXTURES = {
    "french_republic": "gfx/interface/goals/france/french_republic.dds",
    "Generic_French_Republic": "gfx/interface/goals/france/Generic_French_Republic.dds",
    "french_democracy": "gfx/interface/goals/france/french_democracy.dds",
    "liberte_egalite_solidarite": "gfx/interface/goals/france/liberte_egalite_solidarite.dds",
    "french_communist_party": "gfx/interface/goals/france/french_communist_party.dds",
    "french_union": "gfx/interface/goals/france/french_union.dds",
    "economic_prosperity": "gfx/interface/goals/00_economy/economic_prosperity.dds",
    "industry_military": "gfx/interface/goals/00_economy/industry_military.dds",
    "brain_power": "gfx/interface/goals/00_science/brain_power.dds",
    "national_grid": "gfx/interface/goals/00_energy_resources/national_grid.dds",
    "nuclear_energy": "gfx/interface/goals/00_energy_resources/nuclear_energy.dds",
    "powerplant": "gfx/interface/goals/00_energy_resources/powerplant.dds",
    "western_alignment": "gfx/interface/goals/00_align/western_alignment.dds",
    "francosphere": "gfx/interface/goals/france/francosphere.dds",
    "francafrique": "gfx/interface/goals/france/francafrique.dds",
    "economic_railroads": "gfx/interface/goals/00_economy/economic_railroads.dds",
    "economic_roads_new": "gfx/interface/goals/00_economy/economic_roads_new.dds",
    "mechanized_agriculture": "gfx/interface/goals/00_economy/agriculture/mechanized_agriculture.dds",
    "wheat_field": "gfx/interface/goals/00_economy/agriculture/wheat_field.dds",
    "farming_sector": "gfx/interface/goals/00_economy/agriculture/farming_sector.dds",
    "green_projects": "gfx/interface/goals/00_environment/green_projects.dds",
    "green_world": "gfx/interface/goals/00_environment/green_world.dds",
    "hydroelectric": "gfx/interface/goals/00_energy_resources/hydroelectric.dds",
    "economic_civil_industry": "gfx/interface/goals/00_economy/economic_civil_industry.dds",
    "FRA_car_icon": "gfx/interface/goals/france/FRA_car_icon.dds",
    "FRA_cinema": "gfx/interface/goals/france/FRA_cinema.dds",
    "FRA_christian_socialism": "gfx/interface/goals/france/FRA_christian_socialism.dds",
    "FRA_ruralism": "gfx/interface/goals/france/FRA_ruralism.dds",
    "FRA_airforce": "gfx/interface/goals/france/FRA_airforce.dds",
    "FRA_air_fighter": "gfx/interface/goals/france/FRA_air_fighter.dds",
    "FRA_navy": "gfx/interface/goals/france/FRA_navy.dds",
    "french_army": "gfx/interface/goals/france/french_army.dds",
    "french_army_air": "gfx/interface/goals/france/french_army_air.dds",
    "french_army_navy": "gfx/interface/goals/france/french_army_navy.dds",
    "french_gendarmerie": "gfx/interface/goals/france/french_gendarmerie.dds",
    "french_legion": "gfx/interface/goals/france/french_legion.dds",
    "french_space_efforts": "gfx/interface/goals/france/french_space_efforts.dds",
    "french_specialists": "gfx/interface/goals/france/french_specialists.dds",
    "french_wine": "gfx/interface/goals/france/french_wine.dds",
    "fra_senegal": "gfx/interface/goals/france/fra_senegal.dds",
}

GROUP_FOCUS_ICONS = {
    "institutions": "french_republic",
    "udr": "french_republic",
    "ri": "Generic_French_Republic",
    "centre": "french_democracy",
    "radical": "liberte_egalite_solidarite",
    "ps": "liberte_egalite_solidarite",
    "pcf": "french_communist_party",
    "psu": "french_union",
    "ecology": "FRA_ruralism",
    "right": "french_republic",
    "economy": "economic_prosperity",
    "defence": "french_army",
    "diplomacy": "francosphere",
    "udr_nato": "french_army",
}

FOCUS_ICON_OVERRIDES = {
    "parliament": "liberte_egalite_solidarite", "contract": "french_union",
    "statute": "french_union", "housing": "FRA_ruralism",
    "memory": "francafrique", "amnesty": "french_republic",
    "new_society": "french_union", "ortf": "FRA_cinema",
    "presidential_industry": "industry_military", "national_champions": "economic_prosperity",
    "participation": "french_union", "management": "economic_prosperity",
    "debre": "french_army", "pompidou_europe": "francosphere",
    "sound_franc": "economic_prosperity", "credit_expansion": "FRA_car_icon",
    "business": "FRA_car_icon", "public_credit": "economic_prosperity",
    "civil_liberties": "liberte_egalite_solidarite", "atlantic_liberal": "western_alignment",
    "europe_liberal": "francosphere", "regional_councils": "FRA_ruralism",
    "cdp_compromise": "FRA_christian_socialism", "mutuals": "french_union",
    "federal_europe": "francosphere", "atlantic_security": "western_alignment",
    "american_challenge": "western_alignment", "radical_enterprise": "FRA_car_icon",
    "left_radicals": "liberte_egalite_solidarite", "secular_school": "french_specialists",
    "municipal_france": "FRA_ruralism", "europe_technology": "french_space_efforts",
    "common_programme": "french_union", "public_banks": "economic_prosperity",
    "social_contract_ps": "french_union", "redistribution": "economic_prosperity",
    "defferre": "FRA_ruralism", "europe_restraint": "francosphere",
    "sovereign_reflation": "economic_prosperity", "advanced_democracy": "french_communist_party",
    "democratic_road": "liberte_egalite_solidarite", "party_discipline": "french_communist_party",
    "municipal_socialism": "FRA_ruralism", "public_combine": "industry_military",
    "workers_control": "french_union", "planned_targets": "industry_military",
    "independent_communism": "french_communist_party", "soviet_friendship": "western_alignment",
    "self_management": "french_union", "union_autonomy": "french_union",
    "decentralised_services": "FRA_ruralism", "civilian_republic": "french_republic",
    "citizen_defence": "french_army", "environment_account": "FRA_ruralism",
    "efficiency_ecology": "green_projects", "local_generation": "hydroelectric",
    "land_stewardship": "wheat_field", "ecological_industry": "industry_military",
    "local_sufficiency": "green_world", "cid_cooperatives": "FRA_car_icon",
    "fn_protection": "french_republic", "fn_export": "economic_prosperity",
    "fn_defence": "french_army", "regional_links": "economic_railroads",
    "technical_colleges": "french_specialists", "mass_universities": "brain_power",
    "champion_model": "industry_military", "regional_industry": "economic_prosperity",
    "territorial_balance": "FRA_ruralism", "plan_calcul": "brain_power",
    "national_computers": "brain_power", "open_computers": "brain_power",
    "transport_choice": "economic_railroads", "tgv": "economic_railroads",
    "motorways": "economic_roads_new", "energy_review": "national_grid",
    "nuclear_scale": "nuclear_energy", "diverse_energy": "powerplant",
    "oil_resilience": "powerplant", "farm_policy": "FRA_ruralism",
    "export_farms": "mechanized_agriculture", "rural_services": "farming_sector",
    "telecoms": "brain_power", "conversion": "industry_military",
    "defence_review": "french_army", "nuclear_priority": "nuclear_energy",
    "balanced_forces": "french_army", "service_review": "french_army",
    "citizen_army": "french_army", "professional_core": "french_army",
    "land_procurement": "industry_military", "national_armour": "french_army",
    "pooled_armour": "western_alignment", "air_programme": "french_army_air",
    "mirage": "FRA_air_fighter", "jaguar_doctrine": "FRA_airforce",
    "naval_review": "french_army_navy", "ocean_navy": "FRA_navy",
    "escort_navy": "french_army_navy", "logistics": "french_army",
    "flight_schools": "french_army_air", "diplomatic_review": "french_republic",
    "airbus": "FRA_air_fighter", "concorde": "FRA_air_fighter",
    "symphonie": "french_space_efforts", "ariane": "french_space_efforts",
    "jaguar": "FRA_airforce", "atlantic_training": "western_alignment",
    "soviet_science": "francosphere", "us_science": "western_alignment",
    "algeria_energy": "francafrique", "iran_energy": "francosphere",
    "algeria_training": "french_specialists", "senegal_civil": "fra_senegal",
    "senegal_defence": "french_army", "rhine": "economic_prosperity",
    "italy": "francosphere", "community_entry": "francosphere",
    "nato_nuclear_veto": "nuclear_energy", "nato_nuclear_consult": "western_alignment",
    "nato_independent": "french_army", "nato_pragmatic": "western_alignment",
    "nato_european": "francosphere", "nato_land_priority": "french_army",
    "nato_sea_priority": "french_army_navy", "nato_land_design": "industry_military",
    "nato_sea_design": "FRA_navy", "nato_rhine": "western_alignment",
    "nato_atlantic_fleet": "french_army_navy", "nato_conditional_plan": "french_army",
    "nato_fleet_support": "french_army_navy", "nato_europe_land": "industry_military",
    "nato_europe_sea": "french_army_navy", "nato_common_maintenance": "industry_military",
    "nato_europe_staff": "french_army_navy",
}

IDEA_TEXTURES = {
    "political_power_bonus": "gfx/interface/ideas/diplomacy/political_power_bonus.dds",
    "labour_unions": "gfx/interface/ideas/internal_factions/labour_unions.dds",
    "economic_increase": "gfx/interface/ideas/economy/economic_increase.dds",
    "industrial_concern": "gfx/interface/ideas/economy/industrial_concern.dds",
    "energy_preferred_fossils_idea": "gfx/interface/ideas/economy/energy_preferred_fossils_idea.dds",
    "research_minstry": "gfx/interface/ideas/iran/research_minstry.dds",
    "nuclear_power": "gfx/interface/ideas/diplomacy/nuclear_power.dds",
    "economy_housing": "gfx/interface/ideas/economy/economy_housing.dds",
    "economic_road_idea": "gfx/interface/ideas/economy/economic_road_idea.dds",
}

OFFER_IDEA_PICTURES = {
    "airbus": "industrial_concern", "concorde": "industrial_concern",
    "symphonie": "research_minstry", "ariane": "research_minstry",
    "jaguar": "industrial_concern", "atlantic_training": "political_power_bonus",
    "soviet_science": "research_minstry", "us_science": "research_minstry",
    "algeria_energy": "energy_preferred_fossils_idea", "iran_energy": "energy_preferred_fossils_idea",
    "algeria_training": "research_minstry", "senegal_civil": "economy_housing",
    "senegal_defence": "political_power_bonus", "rhine": "industrial_concern",
    "italy": "economic_increase", "nato_rhine": "political_power_bonus",
    "nato_atlantic_fleet": "political_power_bonus", "nato_europe_land": "industrial_concern",
    "nato_europe_sea": "research_minstry",
}

STARTING_IDEA_PICTURES = {
    "presidency": "political_power_bonus",
    "grenelle": "labour_unions",
    "regions": "industrial_concern",
    "oil": "energy_preferred_fossils_idea",
    "education": "research_minstry",
    "deterrent": "nuclear_power",
    "postcolonial": "economy_housing",
    "franc_stabilisation": "economic_road_idea",
}

GROUP_IDEA_PICTURES = {
    "institutions": "political_power_bonus",
    "udr": "political_power_bonus",
    "ri": "economic_increase",
    "centre": "political_power_bonus",
    "radical": "research_minstry",
    "ps": "labour_unions",
    "pcf": "labour_unions",
    "psu": "labour_unions",
    "ecology": "energy_preferred_fossils_idea",
    "right": "economic_road_idea",
    "economy": "industrial_concern",
    "defence": "nuclear_power",
    "diplomacy": "political_power_bonus",
    "udr_nato": "nuclear_power",
}

PROGRAMME_DESCRIPTIONS = {
    "institutions": "A national programme for the authority, accountability and public services of the Fifth Republic.",
    "udr": "The Gaullist government links social participation, national industry and independent French decision-making.",
    "ri": "The Independent Republicans pursue administrative reform, private initiative and responsible public credit.",
    "centre": "The Democratic Centre combines market enterprise, social provision and parliamentary influence.",
    "radical": "The Radical Republicans defend secular institutions, civic equality and practical local development.",
    "ps": "The Socialist Party rebuilds its organisation and debates how to combine social rights, ownership and European commitments.",
    "pcf": "The French Communist Party weighs municipal influence, organised labour and the institutional limits of a national transition.",
    "psu": "The Unified Socialist Party develops local participation, independent unions and civilian public services.",
    "ecology": "An emerging ecological course weighs conservation, rural livelihoods and the costs of industrial growth.",
    "right": "The national right and independent traders pursue protection, tax relief and a stronger central state.",
    "economy": "French economic policy balances regional access, industrial investment, education and secure energy.",
    "defence": "French defence policy balances the independent deterrent, conventional forces and the cost of readiness.",
    "diplomacy": "France negotiates technical and industrial partnerships while preserving each government's authority to consent.",
    "udr_nato": "The UDR government keeps the Atlantic Treaty while defining the limits of military cooperation and national command.",
}

PROGRAMME_TITLE_REVISIONS = {
    # Stable long-term institution labels; dated party identity is resolved
    # through MD's existing party-name registry in the focus shortcuts.
    "udr": "Gaullist Government",
    "ri": "Liberal Republicans",
}


def _stable(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def gameplay_projection(design: dict[str, Any]) -> dict[str, Any]:
    """Return every approved field that this polish overlay must preserve."""
    node_fields = (
        "id", "key", "group", "cost", "days", "effects", "prerequisites",
        "exclusions", "conditions", "basis", "lifetime", "spirit", "spirit_name",
        "reward_guards", "activation_conditions", "offer", "nato_policy",
    )
    spirit_fields = ("id", "effects", "days", "remedy")
    group_fields = ("id", "slot", "trigger", "governing_group", "parent_group", "activation_conditions")
    def offer_projection(offer: dict[str, Any]) -> dict[str, Any]:
        clean = deepcopy(offer)
        for side in ("france", "recipient"):
            if side in clean:
                clean[side].pop("name", None)
                clean[side].pop("picture", None)
        return clean

    nodes = []
    for n in sorted(design["nodes"], key=lambda v: v["id"]):
        item = {k: n[k] for k in node_fields if k in n}
        if "offer" in item:
            item["offer"] = offer_projection(item["offer"])
        nodes.append(item)
    return {
        "nodes": nodes,
        "groups": [{k: g[k] for k in group_fields if k in g} for g in sorted(design["groups"], key=lambda v: v["id"])],
        "starting_spirits": [{k: s[k] for k in spirit_fields if k in s} for s in sorted(design.get("starting_spirits", []), key=lambda v: v["id"])],
        "decisions": design.get("decisions", []),
        "rules": design.get("rules", {}),
        "nato": design.get("nato", {}),
    }


def gameplay_fingerprint(design: dict[str, Any]) -> str:
    return sha256(_stable(gameplay_projection(design))).hexdigest()


def polish_design(base: dict[str, Any]) -> dict[str, Any]:
    """Return a polished deep copy without changing approved gameplay fields."""
    out = deepcopy(base)
    old_fingerprint = gameplay_fingerprint(base)
    if len(out.get("nodes", [])) != 152:
        raise ValueError(f"Expected 152 approved focuses, got {len(out.get('nodes', []))}")
    if set(SECTION_X) != {g["id"] for g in out["groups"]}:
        raise ValueError("Polish geometry must explicitly place all 14 programme sections")
    if set(STARTING_IDEA_PICTURES) != {s["id"].removeprefix("COLDWAR_FRA2_") for s in out.get("starting_spirits", [])}:
        raise ValueError("Starting idea artwork map does not cover the supplied starting spirits")

    for group in out["groups"]:
        dx = SECTION_X[group["id"]] - group["x"]
        group["x"] += dx
        if group["id"] in PROGRAMME_TITLE_REVISIONS:
            group["title"] = PROGRAMME_TITLE_REVISIONS[group["id"]]
        group["idea_picture"] = f"COLDWAR_FRA2_idea_{GROUP_IDEA_PICTURES[group['id']]}"
        group["focus_icon_source"] = GROUP_FOCUS_ICONS[group["id"]]

    for node in out["nodes"]:
        group = next(g for g in out["groups"] if g["id"] == node["group"])
        original_group = next(g for g in base["groups"] if g["id"] == node["group"])
        node["x"] += group["x"] - original_group["x"]
        if node["key"] in TITLE_REVISIONS:
            node["title"] = TITLE_REVISIONS[node["key"]]
            node["full_title"] = node["title"]
        else:
            node["full_title"] = node.get("full_title", node["title"])
        if node["key"] in DESCRIPTION_REVISIONS:
            node["description"] = DESCRIPTION_REVISIONS[node["key"]]
        source_icon = FOCUS_ICON_OVERRIDES.get(node["key"], GROUP_FOCUS_ICONS[node["group"]])
        node["icon"] = f"COLDWAR_FRA2_focus_{source_icon}"
        node["icon_source"] = source_icon
        if node.get("offer"):
            offer_picture = f"COLDWAR_FRA2_idea_{OFFER_IDEA_PICTURES[node['key']]}"
            node["offer"]["france"]["name"] = node["title"] + ": France"
            node["offer"]["france"]["picture"] = offer_picture
            node["offer"]["recipient"]["name"] = node["title"] + ": " + node["offer"]["partner_name"]
            node["offer"]["recipient"]["picture"] = offer_picture

    for spirit in out.get("starting_spirits", []):
        key = spirit["id"].removeprefix("COLDWAR_FRA2_")
        spirit["picture"] = f"COLDWAR_FRA2_idea_{STARTING_IDEA_PICTURES[key]}"

    # Keep anchors and relative offsets consistent with translated sections.
    by_id = {n["id"]: n for n in out["nodes"]}
    for node in out["nodes"]:
        if node.get("anchor"):
            anchor = by_id[node["anchor"]]
            node["offset"] = [node["x"] - anchor["x"], node["y"] - anchor["y"]]
        else:
            # A top-level focus has no relative_position_id, so its emitted
            # offset is its absolute native position, not relative to a group.
            node["offset"] = [node["x"], node["y"]]

    out.setdefault("visual_assets", {})
    out["visual_assets"].update({
        "project": PROJECT,
        "source_profile": "Millennium Dawn Workshop 2777392649 installed art, inspected 2026-10-28",
        "focus_icon_registry": "COLDWAR_FRA2_focus_*",
        "focus_shine_registry": "COLDWAR_FRA2_focus_*_shine",
        "focus_shine_source": "interface/goals_shine.gfx",
        "idea_icon_registry": "GFX_idea_COLDWAR_FRA2_idea_*",
        "focus_texture_sources": deepcopy(GOAL_TEXTURES),
        "idea_texture_sources": deepcopy(IDEA_TEXTURES),
        "art_changes": "Focus and idea aliases plus native focus shine blocks. DDS pixels are reused unchanged; shine blocks are copied verbatim except for project-prefixed sprite names.",
        "historical_branding": "UDR uses the French Republic emblem. Later RPR/UMP, FN and EELV identity artwork is not used for January 1970 party branches.",
    })

    if {n["id"] for n in out["nodes"]} != {n["id"] for n in base["nodes"]}:
        raise AssertionError("Focus IDs changed")
    if gameplay_fingerprint(out) != old_fingerprint:
        raise AssertionError("Polish overlay changed an approved gameplay field")
    xs = [n["x"] for n in out["nodes"]]
    ys = [n["y"] for n in out["nodes"]]
    if (min(xs), max(xs), min(ys), max(ys)) != (4, 103, 0, 13):
        raise AssertionError(f"Unexpected polished footprint: {(min(xs), max(xs), min(ys), max(ys))}")
    return out


def _gfx_sprite(name: str, texture: str) -> str:
    return f'\tspriteType = {{\n\t\tname = "{name}"\n\t\ttexturefile = "{texture}"\n\t}}\n'


def _sprite_blocks(text: str) -> dict[str, str]:
    """Return complete native spriteType blocks keyed by registered sprite name."""
    found: dict[str, str] = {}
    for match in re.finditer(r"spriteType\s*=\s*\{", text):
        open_brace = text.find("{", match.start())
        depth, quoted, escaped = 0, False, False
        end = None
        for index in range(open_brace, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise ValueError("Unclosed spriteType block in native MD shine registry")
        block = text[match.start():end]
        name = re.search(r'\bname\s*=\s*"([^"]+)"', block)
        if name:
            found[name.group(1)] = block
    return found


def build_art(design: dict[str, Any]) -> dict[str, Any]:
    """Build code and English localisation maps for the native aliases.

    The returned GFX aliases point to existing MD texture paths. `art_copies`
    is intentionally empty because the DDS assets remain upstream-owned files.
    """
    if not design.get("visual_assets", {}).get("focus_texture_sources"):
        design = polish_design(design)
    sprites: dict[str, str] = {}
    for native, texture in GOAL_TEXTURES.items():
        if any(n.get("icon_source") == native for n in design["nodes"]):
            sprites[f"COLDWAR_FRA2_focus_{native}"] = texture
    for source in set(STARTING_IDEA_PICTURES.values()) | set(GROUP_IDEA_PICTURES.values()) | set(OFFER_IDEA_PICTURES.values()):
        sprites[f"GFX_idea_COLDWAR_FRA2_idea_{source}"] = IDEA_TEXTURES[source]
    shine_native = sorted({n["icon_source"] for n in design["nodes"]})
    if not MD_SHINE_SOURCE.is_file():
        raise FileNotFoundError(f"Native MD shine sprite registry not found: {MD_SHINE_SOURCE}")
    donor_blocks = _sprite_blocks(MD_SHINE_SOURCE.read_text(encoding="utf-8-sig"))
    shine_blocks = []
    for native in shine_native:
        donor_name = f"{native}_shine"
        if donor_name not in donor_blocks:
            raise KeyError(f"No native MD shine sprite for focus icon {native!r}")
        project_name = f"COLDWAR_FRA2_focus_{native}_shine"
        # Keep every donor animation, texture, flag and whitespace byte as read;
        # only replace the registered sprite name inside the copied block.
        shine_blocks.append(donor_blocks[donor_name].replace(
            f'name = "{donor_name}"', f'name = "{project_name}"', 1))

    gfx = "# IMPERIA COLD WAR — France 1970 focus and idea art aliases.\n"
    gfx += "spriteTypes = {\n" + "".join(_gfx_sprite(name, path) for name, path in sorted(sprites.items()))
    gfx += "\n" + "\n".join(shine_blocks) + "\n}\n"

    loc: dict[str, str] = {}
    for node in design["nodes"]:
        loc[node["id"]] = node["title"]
        loc[node["id"] + "_desc"] = node["description"]
    for spirit in design.get("starting_spirits", []):
        loc[spirit["id"]] = spirit["title"]
        loc[spirit["id"] + "_desc"] = spirit["description"]
    for group in design["groups"]:
        idea_key = f"COLDWAR_FRA2_{group['id']}_programme"
        loc[idea_key] = group["title"] + " Programme"
        loc[idea_key + "_desc"] = PROGRAMME_DESCRIPTIONS.get(group["id"], group["context"])
    for node in design["nodes"]:
        if node.get("offer"):
            for side in ("france", "recipient"):
                terms = node["offer"][side]
                loc[terms["spirit"]] = terms["name"]
                loc[terms["spirit"] + "_desc"] = node["description"]

    return {
        "design": design,
        "files": {"interface/COLDWAR_FRA2_polish_art.gfx": gfx},
        "loc": loc,
        "art_copies": [],
        "art_notice": {
            "project": PROJECT,
            "source": "Millennium Dawn Workshop 2777392649 installed checkout; native focus and idea DDS paths referenced directly; complete focus shine spriteType blocks copied from interface/goals_shine.gfx",
            "author_credit": "Millennium Dawn authors; individual asset authors not identified in inspected files",
            "license_or_permission": "Unknown from the inspected source files",
            "modifications": "No source texture is copied or modified; focus shine spriteType blocks are exact MD definitions with only the registered sprite name changed to the project-prefixed icon alias plus _shine",
        },
    }
