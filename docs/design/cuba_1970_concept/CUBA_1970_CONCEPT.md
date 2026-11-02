# COLDWAR_CUB — Cuba 1970–1990 approval concept

120 focuses; 13 governing programmes; 7 initial spirits. English localisation only. No runtime installation.

All numerical values are proposed balance values, not historical measurements. Sources verify institutions, constraints and API support.

## Programme structure

| Programme | Root x,y | Focuses | Ruling slot |
|---|---|---:|---:|
| The Harvest and the Economy | 8,0 | 15 | Shared |
| The Social State | 20,0 | 7 | Shared |
| The Revolutionary Armed Forces | 30,0 | 8 | Shared |
| Cuba and the Cold War | 42,0 | 13 | Shared |
| PCC · Fidel Castro | 6,10 | 13 | 4 |
| Orthodox Planning Cadres | 14,10 | 7 | 6 |
| Guevarist Mobilisation | 22,10 | 6 | 19 |
| FAR · National Administration | 30,10 | 7 | 22 |
| Auténtico · Social Republic | 38,10 | 6 | 3 |
| Ortodoxo · Sovereign Republic | 6,18 | 6 | 18 |
| Christian Democratic Movement | 14,18 | 6 | 1 |
| Constitutional Liberal Republic | 22,18 | 7 | 2 |
| RECE · Exile Directorate | 30,18 | 5 | 0 |
| Alpha 66 · National Liberation | 38,18 | 5 | 20 |
| OSPAAAL · Tricontinental Solidarity | 46,10 | 3 | 5 |
| MININT · Interior Administration | 46,18 | 3 | 7 |
| JUCEPLAN · Central Planning Board | 54,10 | 3 | 13 |

## Initial situation

Fidel Castro is Prime Minister; the PCC governs through exact subparty slot 4. No starting army, industry, money or party popularity is invented by this design.

The existing 1970 Cuba history has no education, health or corruption idea tiers. The edu_02/health_02 entries belong to 2000. This concept proposes edu_02, health_02 and corruption_level_04 when the corresponding category is genuinely uninitialized; preserve a valid existing tier. These are balance baselines for broad public provision and bureaucratic constraints, not historical statistical measurements. No 2000 Special Period or migration-crisis spirit is imported.

1970 scenario, original CUB, one-time setup receipt; initialize only missing categories, recalculate native budget/law variables afterward.

### The Ten Million Ton Campaign

A record harvest is being pursued through an extraordinary diversion of labour, transport and fuel. The campaign is still under way on 1 January 1970; its historical shortfall must not be treated as a completed event.

Construction speed -12%; Civilian industry productivity -10%; Available workforce +3%.

Resolution: Harvest choices set the course. On 26 July 1970 replace, never stack, the campaign with a smaller recovery burden; the rebalancing programme clears it sooner.

### The Revolutionary Offensive

The 1968 nationalisations extended state control deep into small enterprise. Political control is strong, but administrative overload and the disappearance of local initiative weigh on civilian production.

Civilian industry productivity -12%; Tax revenue multiplier -5%; Ideology drift defence +10%.

Resolution: Protected Enterprises or Joint Ventures replaces this with a defined reformed institution; no duplicate command-economy penalty.

### Sugar and Soviet Oil

Sugar provides an export livelihood, while machinery and oil depend heavily on foreign partners. This is a structural exposure, not a guarantee of outside support.

Agricultural productivity +10%; Imperia sanction resistance -10%; Foreign influence defence -10%.

Resolution: Food before Sugar and diversified industry reduce this exposure. A Soviet support withdrawal worsens the remaining dependency instead of imposing a scripted collapse regardless of prior policy.

### The American Embargo

Restricted access to the American market and trade finance narrows Cuba's commercial options. The economic burden belongs to the continuing dispute and ends only through a real settlement or a change in the legal sanctions regime.

Resource export revenue -20%; Civilian industry productivity -5%.

Resolution: An accepted US executive settlement may ease or end the 1970–90 trade embargo. Separate tariff, official credit and territorial issues remain subject to their own terms; do not apply later 1996 restrictions retroactively or duplicate a native/Imperia sanction.

### Committees of Defence

The CDRs and security apparatus reach into daily life. Their defensive intelligence advantage is accompanied by political conformity and a narrower space for independent technical discussion.

Counterintelligence defence +15%; Political power gain -8%; Research speed -3%.

Resolution: A constitutional/civic security settlement replaces, rather than silently retains, this institution. Historical PCC/FAR reform may professionalise it without claiming instant pluralism.

### Literacy and Public Medicine

Literacy and public medicine have widened access to essential services. Maintaining that provision requires a lasting commitment of teachers, medical staff and public income.

Research speed +4%; Available workforce +2%; Weekly education expenditure +10%; Weekly healthcare expenditure +10%.

Resolution: Shared social programmes improve provision through actual native budget tiers. Protect these accumulated services across government changes.

### A Revolution in Exile

Exile has fractured families and removed professional networks. The continuing disruption of skills and confidence weighs on an already demanding economic transformation.

Available workforce -4%; Stability -3%.

Resolution: Negotiated dialogue and registered voluntary return agreements through the existing diaspora system reduce the burden. No focus invents a mass return or coerced migration count.

## Complete focus matrix

### The Harvest and the Economy

Mobilisation, sugar versus food, infrastructure and ownership priorities.

#### Harvest Accounts · 21 days · (8,0)

The target of ten million tons has drawn workers, lorries and fuel away from the rest of the economy. JUCEPLAN needs reliable accounts before ministers can distinguish a genuine production gain from a transfer of shortages.

`COLDWAR_CUB_harvest_accounts` · Native card title: Harvest Accounts.

Prerequisite: Programme root.

Effects: Civilian industry productivity +4%; Weekly bureaucracy expenditure +3%; Treasury -0.15 (one time).

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Finish the Zafra · 35 days · (6,1)

The leadership can still concentrate the nation on the cane fields. Finishing the campaign preserves revolutionary authority and raises farm output, but workshops and housing must wait for their workers to return.

`COLDWAR_CUB_finish_zafra` · Native card title: Finish the Zafra.

Prerequisite: Harvest Accounts.

Effects: Agricultural productivity +12%; Available workforce +2%; Construction speed -4%; Record harvest course: mobilisation; campaign modifiers expire with the July 1970 harvest settlement.

Lifetime: Temporary harvest programme; all listed programme modifiers expire on 26 July 1970.

Requirements: Shared national programme.

Excludes: Restore the Sectors.

#### Restore the Sectors · 35 days · (10,1)

Transport depots, repairs and consumer production cannot remain subordinate to a single target. Returning labour to those sectors offers a broader recovery, at the political cost of admitting that willpower has limits.

`COLDWAR_CUB_restore_sectors` · Native card title: Restore the Sectors.

Prerequisite: Harvest Accounts.

Effects: Construction speed +10%; Civilian industry productivity +8%; Agricultural productivity -4%; Record harvest course: rebalance; campaign modifiers expire with the July 1970 harvest settlement; Stability -3 percentage points.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Finish the Zafra.

#### Rail and Lorries · 49 days · (8,2)

Cane left beside a broken railway earns no foreign exchange. A coordinated programme for rail sidings, lorry repairs and port approaches will serve the entire economy after the harvest has ended.

`COLDWAR_CUB_rail_lorries` · Native card title: Rail and Lorries.

Prerequisite: Finish the Zafra OR Restore the Sectors.

Effects: Treasury -0.60 (one time); State 854: +1 infrastructure; 1 × 25% research bonus · CAT_infrastructure.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Sugar for Export · 35 days · (4,3)

Reliable sugar exports can purchase machinery and fuel that Cuba cannot yet produce. This programme protects the cash-crop economy, accepting greater exposure to foreign buyers instead of promising that specialization is free.

`COLDWAR_CUB_sugar_exports` · Native card title: Sugar for Export.

Prerequisite: Rail and Lorries.

Effects: Agricultural productivity +15%; Agricultural district tax income +8%; Imperia sanction resistance -5%; .

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Food before Sugar.

#### Food before Sugar · 35 days · (8,3)

Vegetables, dairy herds and domestic staples compete with sugar for land and skilled labour. Greater food security offers resilience under pressure, while reducing the export receipts available for imported equipment.

`COLDWAR_CUB_food_first` · Native card title: Food before Sugar.

Prerequisite: Rail and Lorries.

Effects: Agricultural productivity +10%; Imperia sanction resistance +12%; Agricultural district tax income -10%; Reduce the Sugar and Soviet Oil dependency to the exact variant in Integration & Balance.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Sugar for Export.

#### Mill Mechanisation · 49 days · (4,4)

Investment must reach the mills and their agricultural hinterland together. Mechanisation can make an export priority productive without relying on another nationwide diversion of unpaid labour.

`COLDWAR_CUB_mill_mechanisation` · Native card title: Mill Mechanisation.

Prerequisite: Sugar for Export.

Effects: Treasury -0.70 (one time); State 854: +1 agriculture district.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### ANAP Cooperatives · 49 days · (8,4)

ANAP's small farmers need purchasing arrangements and a credible return for their work. Cooperative development will strengthen local food production while leaving a larger share of its proceeds with producers.

`COLDWAR_CUB_anap_cooperatives` · Native card title: ANAP Cooperatives.

Prerequisite: Food before Sugar.

Effects: Available workforce +2%; Agricultural district tax income -6%; Treasury -0.70 (one time); State 1121: +1 agriculture district.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Moa's Refinery · 49 days · (12,3)

The nickel industry around Moa gives eastern Cuba an industrial role beyond sugar. Refining and maintenance capacity should be expanded before another prestige project competes for imported machinery and trained technicians.

`COLDWAR_CUB_moa_refinery` · Native card title: Moa's Refinery.

Prerequisite: Rail and Lorries.

Effects: Treasury -0.90 (one time); State 855: +1 industrial complex.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Repair the Grid · 49 days · (12,4)

Industrial expansion requires dependable electricity. Restoring generation in central Cuba will reduce interruptions, but the new plant will consume fuel through the existing national energy system.

`COLDWAR_CUB_repair_grid` · Native card title: Repair the Grid.

Prerequisite: Moa's Refinery.

Effects: Treasury -0.65 (one time); State 1121: +1 fossil powerplant.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Light Industry · 49 days · (12,5)

Textiles, food processing and household goods deserve an industrial programme of their own. A civilian factory in central Cuba will support a more diversified economy rather than another promise of immediate abundance.

`COLDWAR_CUB_light_industry` · Native card title: Light Industry.

Prerequisite: Repair the Grid.

Effects: Civilian industry productivity +6%; Treasury -0.90 (one time); State 1121: +1 industrial complex; Reduce the Sugar and Soviet Oil dependency to the exact variant in Integration & Balance.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Protected Enterprises · 35 days · (10,6)

State enterprises can retain their domestic market while being held to production and maintenance targets. Protection reduces external exposure, but it also leaves investment dependent on domestic resources and administrative discipline.

`COLDWAR_CUB_protected_enterprises` · Native card title: Protected Firms.

Prerequisite: Light Industry.

Effects: Civilian industry productivity +12%; Imperia sanction resistance +10%; Construction speed -5%; Replace The Revolutionary Offensive; retain national assets across later governments.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Joint Ventures.

#### Joint Ventures · 35 days · (14,6)

Foreign partners can supply equipment and market access under negotiated Cuban ownership rules. Their participation accelerates investment, while profit concessions and outside leverage limit the state's freedom of action.

`COLDWAR_CUB_joint_ventures` · Native card title: Joint Ventures.

Prerequisite: Light Industry.

Effects: Construction speed +12%; Civilian industry productivity +6%; Production efficiency growth +8%; Tax revenue multiplier -4%; Foreign influence defence -10%; Replace The Revolutionary Offensive; retain national assets across later governments.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Protected Enterprises.

#### Havana's Ports · 49 days · (0,3)

Cuba's foreign trade depends on a small number of harbours and their approaches. Improvements around Havana will support commercial traffic and coastal supply without granting the island a new battle fleet.

`COLDWAR_CUB_havana_ports` · Native card title: Havana's Ports.

Prerequisite: Rail and Lorries.

Effects: Treasury -0.55 (one time); State 854: +1 naval base · province 7622.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Oil Shock Reserve · 35 days · (0,4)

A disruption in imported oil would reach farms, electricity and transport together. Storage is a practical insurance policy; it creates reserve capacity rather than fuel that has never been purchased.

`COLDWAR_CUB_oil_reserve` · Native card title: Oil Shock Reserve.

Prerequisite: Havana's Ports.

Effects: Treasury -0.35 (one time); State 854: +1 fuel silo.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

### The Social State

Preserve achievements while choosing how to fund and distribute scarce skilled labour.

#### The Social Promise · 35 days · (20,0)

Literacy and public medicine are among the revolution's strongest claims to legitimacy. Maintaining those achievements requires an honest commitment of teachers, doctors and national income, even when consumer supplies remain scarce.

`COLDWAR_CUB_social_promise` · Native card title: The Social Promise.

Prerequisite: Programme root.

Effects: Research speed +3%; Weekly education expenditure +5%; Education budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Rural Clinics · 35 days · (18,1)

Rural families need regular access to trained medical staff, not simply a distant hospital on paper. Local clinics use scarce personnel efficiently, but their staffing and supplies remain a recurring public expense.

`COLDWAR_CUB_rural_clinics` · Native card title: Rural Clinics.

Prerequisite: The Social Promise.

Effects: Healthcare workforce requirement -8%; Monthly population growth factor +3%; Weekly healthcare expenditure +8%; Treasury -0.45 (one time).

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Teaching Hospitals.

#### Teaching Hospitals · 35 days · (22,1)

Concentrating equipment and specialist training in major hospitals can develop a stronger medical profession. It improves research and sector output, while requiring more expensive facilities than a dispersed basic service.

`COLDWAR_CUB_teaching_hospitals` · Native card title: Teaching Hospitals.

Prerequisite: The Social Promise.

Effects: Research speed +6%; Healthcare sector income +8%; Weekly healthcare expenditure +12%; Treasury -0.55 (one time).

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Rural Clinics.

#### Health Workforce · 35 days · (20,2)

The health service needs a sustainable establishment of doctors, nurses and technical staff. Its next budget settlement should fund actual provision through the existing spending system, rather than disguise expenditure as a free national bonus.

`COLDWAR_CUB_health_workforce` · Native card title: Health Workforce.

Prerequisite: Rural Clinics OR Teaching Hospitals.

Effects: Healthcare budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment; Treasury -0.15 (one time).

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Medical Brigades · 35 days · (18,3)

Cuban doctors can build durable relationships where military assistance cannot. A partner must request the mission and share its terms. Overseas accommodation, medical supplies and replacement coverage require a larger public healthcare budget.

`COLDWAR_CUB_medical_brigades` · Native card title: Medical Brigades.

Prerequisite: Health Workforce.

Effects: Foreign influence +12%; Weekly healthcare expenditure +10%; Propose Requested Medical Mission; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Retain the Doctors.

#### Retain the Doctors · 35 days · (22,3)

Keeping newly trained medical staff at home will strengthen ordinary public provision. The policy forgoes some international influence in return for a service that reaches more Cuban households.

`COLDWAR_CUB_retain_doctors` · Native card title: Retain the Doctors.

Prerequisite: Health Workforce.

Effects: Healthcare sector income +12%; Available workforce +2%; Foreign influence -4%; .

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Medical Brigades.

#### Schools of Science · 49 days · (20,4)

Universities and technical schools must produce the engineers and laboratory staff required by a modern economy. Their graduates will improve research and available skills, while the expanded education budget continues to be paid each week.

`COLDWAR_CUB_science_schools` · Native card title: Schools of Science.

Prerequisite: Medical Brigades OR Retain the Doctors.

Effects: Available workforce +3%; Weekly education expenditure +6%; Treasury -0.30 (one time); 2 × 25% research bonus · CAT_electronics.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

### The Revolutionary Armed Forces

A credible defence, or a costly expeditionary establishment; no free starting army.

#### Reorganise the FAR · 35 days · (30,0)

The guerrilla victory of 1959 is not a substitute for a professional staff, dependable logistics and modern training. The FAR must prepare for the threats Cuba actually faces rather than measure prestige by the size of its equipment requests.

`COLDWAR_CUB_far_reorganisation` · Native card title: Reorganise the FAR.

Prerequisite: Programme root.

Effects: Treasury -0.25 (one time); Army experience +25; 1 × 25% land doctrine cost reduction.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Territorial Defence · 35 days · (28,1)

Dispersed positions, trained reserves and knowledge of the island favour a defensive war. This doctrine makes Cuba harder to invade while accepting less emphasis on offensive operations beyond its shores.

`COLDWAR_CUB_territorial_defence` · Native card title: Territorial Defence.

Prerequisite: Reorganise the FAR.

Effects: Core territory defence +10%; Division organisation +4%; Division attack -3%; .

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Expeditionary Forces.

#### Expeditionary Forces · 35 days · (32,1)

An overseas commitment needs deployable formations and a permanent support establishment. Sustaining trained contingents increases the military wage bill and requires larger stocks, maintenance reserves and supply shipments.

`COLDWAR_CUB_expeditionary_forces` · Native card title: Overseas Forces.

Prerequisite: Reorganise the FAR.

Effects: Volunteer division limit +2; Division organisation +6%; Weekly army personnel expenditure +12%; Supply consumption +5%; .

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Territorial Defence.

#### Militia Logistics · 35 days · (28,2)

Militia units need common stores, communications and manageable supply requirements. Standardisation improves defensive endurance while preserving the limitations of a locally organised force.

`COLDWAR_CUB_militia_logistics` · Native card title: Militia Logistics.

Prerequisite: Territorial Defence.

Effects: Division defence +3%; Supply consumption -5%; Division organisation -2%; 1 × 25% research bonus · CAT_small_arms.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Mission Schools · 35 days · (32,2)

Officers assigned abroad need language preparation, staff training and experience of long supply lines. An expeditionary school develops specialist capacity at the cost of a more fuel-intensive force.

`COLDWAR_CUB_mission_schools` · Native card title: Mission Schools.

Prerequisite: Expeditionary Forces.

Effects: Special forces capacity +3%; Army fuel consumption +5%; 1 × 50% land doctrine cost reduction.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Soviet Air Defence · 35 days · (30,3)

Soviet equipment can strengthen Cuban air surveillance when both governments agree on assistance. The proposal concerns training and a limited radar installation, not the return of strategic nuclear weapons to the island.

`COLDWAR_CUB_air_defence` · Native card title: Soviet Air Defence.

Prerequisite: Militia Logistics OR Mission Schools.

Effects: Air experience +25; Propose Air Defence Training; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: SOV exists; Cuba and the Soviet Union are not at war.

#### Coastal Patrols · 35 days · (28,4)

Protecting approaches and identifying suspicious traffic is a realistic task for Cuba's navy. Training and coastal ship design will improve that service without pretending the country fields a blue-water fleet.

`COLDWAR_CUB_coastal_patrols` · Native card title: Coastal Patrols.

Prerequisite: Soviet Air Defence.

Effects: Treasury -0.25 (one time); Navy experience +25; 1 × 25% research bonus · CAT_corvettes.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Civil Military Pact · 35 days · (32,4)

Commanders need a settled relationship with the civilian administration. A permanent defence settlement improves organisation, while consultation and oversight reduce the executive's freedom to act alone.

`COLDWAR_CUB_civil_military_pact` · Native card title: Civil–Military Pact.

Prerequisite: Soviet Air Defence.

Effects: Division organisation +5%; Political power gain -5%; .

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

### Cuba and the Cold War

Soviet alignment, independent diplomacy, recipient consent, and the Thälmann island.

#### An Island's Diplomacy · 21 days · (42,0)

Cuba's security depends on more than its distance from Florida. Diplomatic relations with neighbours and distant partners can widen its room for manoeuvre without requiring another country to accept Cuban leadership.

`COLDWAR_CUB_island_diplomacy` · Native card title: Island Diplomacy.

Prerequisite: Programme root.

Effects: Treasury -0.10 (one time); Opinion 10 · MEX, JAM.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Soviet Assistance · 35 days · (38,1)

Closer Soviet cooperation offers equipment, technical expertise and diplomatic support against isolation. Accepting assistance also gives Moscow greater influence over choices Havana would prefer to make independently.

`COLDWAR_CUB_moscow_guarantee` · Native card title: Soviet Assistance.

Prerequisite: An Island's Diplomacy.

Effects: Propose Soviet Technical Assistance; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: SOV exists; not at war with SOV.

Excludes: Havana's Own Voice.

#### Havana's Own Voice · 35 days · (46,1)

Cuba can remain socialist or sovereign without allowing a single patron to define every relationship. Independent diplomacy improves resilience and influence, while sacrificing some of the commercial advantages of bloc discipline.

`COLDWAR_CUB_havana_voice` · Native card title: Havana's Own Voice.

Prerequisite: An Island's Diplomacy.

Effects: Imperia sanction resistance +10%; Foreign influence +10%; Resource export revenue -5%; Treasury -0.25 (one time).

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

Excludes: Soviet Assistance.

#### Apply to COMECON · 35 days · (38,2)

Admission to the Council for Mutual Economic Assistance would place Cuba's economic relationship with the socialist states on a more formal footing. Membership requires an accepted agreement; an application is not a receipt for subsidised imports.

`COLDWAR_CUB_cmea_application` · Native card title: Apply to COMECON.

Prerequisite: Soviet Assistance.

Effects: Propose CMEA Admission; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: SOV exists; admission agreement is reachable before all member-only content.

#### Division of Labour · 35 days · (38,3)

Member states can coordinate specialisation and technical standards instead of duplicating every industry. Cuba gains a more secure place for agricultural exports, while accepting less freedom to diversify its own civilian production.

`COLDWAR_CUB_division_labour` · Native card title: Division of Labour.

Prerequisite: Apply to COMECON.

Effects: Agricultural district tax income +10%; Civilian industry productivity -5%; 1 × 25% research bonus · CAT_industry.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Has actual COLDWAR_CUB_cmea_member spirit; rechecked in the reward guard.

#### Caribbean Neighbours · 35 days · (46,2)

Jamaica, Guyana and the Dominican Republic face their own political constraints. Cuba can pursue normal relations and practical cooperation without treating every neighbouring government as a future revolutionary dependency.

`COLDWAR_CUB_caribbean_neighbours` · Native card title: Our Neighbours.

Prerequisite: Soviet Assistance OR Havana's Own Voice.

Effects: Treasury -0.15 (one time); Opinion 15 · JAM, GUY, DOM.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### An African Mandate · 35 days · (46,3)

Any government seeking Cuban assistance must define what it needs and what Cuba can sustain. Training and medical cooperation can accompany military aid; the scope and terms depend on the recipient's request and the resources Havana can commit.

`COLDWAR_CUB_african_mandate` · Native card title: An African Mandate.

Prerequisite: Caribbean Neighbours.

Effects: Propose Requested Overseas Assistance; acceptance is a separate decision; Army experience +15.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Shared national programme.

#### Talks with Washington · 35 days · (50,3)

Migration, prisoners, property claims and trade stand between Havana and Washington. Negotiations can open a limited diplomatic channel or a broader trade settlement, with the United States deciding its own terms. Guantánamo's status remains a separate question.

`COLDWAR_CUB_washington_talks` · Native card title: Washington Talks.

Prerequisite: Caribbean Neighbours.

Effects: Propose A Cuban–American Settlement; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: USA exists; not at war with USA.

#### Berlin and Havana · 35 days · (42,4)

The German Democratic Republic offers an industrial partner whose relationship with Cuba need not be reduced to Soviet instructions. A bilateral commission can discuss technical education, public symbolism and the future of Cayo Blanco del Sur.

`COLDWAR_CUB_berlin_havana` · Native card title: Berlin and Havana.

Prerequisite: An Island's Diplomacy.

Effects: Propose Berlin–Havana Commission; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: DDR exists; Cuba owns and controls State 1252; not at war with DDR.

#### A Name for Thälmann · 35 days · (40,5)

Naming Cayo Blanco del Sur after Ernst Thälmann would honour a communist martyr and the friendship between the two republics. As in the historical gesture of 1972, the island would remain Cuban territory.

`COLDWAR_CUB_thaelmann_name` · Native card title: A Name for Thälmann.

Prerequisite: Berlin and Havana.

Effects: State 1252 → Ernst Thälmann Island; ownership remains CUB; Opinion 20 · DDR.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Date on/after 19 June 1972; DDR exists; Cuba owns and controls State 1252.

Excludes: A Territorial Agreement.

#### A Territorial Agreement · 35 days · (44,5)

Havana may instead propose a genuine territorial agreement over the island. This would be an alternative to the historical symbolic gesture, requiring an explicit East German decision on compensation and responsibility.

`COLDWAR_CUB_caribbean_treaty` · Native card title: A Territorial Agreement.

Prerequisite: Berlin and Havana.

Effects: Propose Actual Island Cession · Alternate History; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: Date on/after 19 June 1972; DDR exists; Cuba owns and controls State 1252.

Excludes: A Name for Thälmann.

#### Playa RDA · 35 days · (40,6)

A modest cultural and scientific programme can make the renamed island a symbol of cooperation. Both countries must approve any expenditure; a commemorative beach is not a ready-made naval base.

`COLDWAR_CUB_playa_rda` · Native card title: Playa RDA.

Prerequisite: A Name for Thälmann.

Effects: Propose Playa RDA Cultural Programme; acceptance is a separate decision.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: DDR exists; Cuba still owns and controls State 1252.

#### Development Protocol · 35 days · (44,6)

A territorial agreement needs a clear protocol for payment, handover and permitted development. Compensation belongs to Cuba, responsibility passes to the DDR, and neither side obtains an automatic industrial complex or a new core claim.

`COLDWAR_CUB_development_protocol` · Native card title: Use and Handover.

Prerequisite: A Territorial Agreement.

Effects: Publish ratified island use protocol; compensation and research are NOT paid a second time.

Lifetime: Persistent national reform; one-time assets remain national.

Requirements: COLDWAR_CUB_island_cession_ratified receipt; State 1252 is owned by DDR; no duplicate payment.

### PCC · Fidel Castro

Popular power, family law, community medicine and biotechnology; markets or mobilised construction.

#### People's Power · 35 days · (6,10)

Fidel's authority can be given a more durable institutional base through local assemblies and the mass organisations. A stronger party-state coordinates decisions, but it also carries a larger administrative establishment.

`COLDWAR_CUB_popular_power` · Native card title: People's Power.

Prerequisite: Programme root.

Effects: Stability +4%; Political power gain +8%; Weekly bureaucracy expenditure +6%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### Party over Ministry · 35 days · (4,11)

Party cadres can ensure that ministries obey a common political direction. Their intervention strengthens the leadership's authority and ideological discipline while reducing the discretion of enterprise managers.

`COLDWAR_CUB_party_ministries` · Native card title: Party over Ministry.

Prerequisite: People's Power.

Effects: Political power gain +12%; Ideology drift defence +8%; Civilian industry productivity -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

Excludes: JUCEPLAN's Mandate.

#### JUCEPLAN's Mandate · 35 days · (8,11)

Economic targets need the authority of an institution capable of refusing impossible promises. Giving JUCEPLAN a stronger mandate improves coordination and investment, at the cost of bureaucracy and personal executive freedom.

`COLDWAR_CUB_juceplan_mandate` · Native card title: JUCEPLAN's Mandate.

Prerequisite: People's Power.

Effects: Civilian industry productivity +12%; Construction speed +8%; Weekly bureaucracy expenditure +8%; Political power gain -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

Excludes: Party over Ministry.

#### The First Congress · 35 days · (6,12)

A party congress can settle responsibilities that have depended on Fidel's personal intervention. Cadre rules and a recorded programme will make the state more predictable without converting it into a multiparty republic.

`COLDWAR_CUB_first_congress` · Native card title: The First Congress.

Prerequisite: Party over Ministry OR JUCEPLAN's Mandate.

Effects: Treasury -0.20 (one time); Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### Socialist Constitution · 35 days · (6,13)

The constitution will define the party's leading role and the place of the assemblies, ministries and social organisations. Constitutional order lends stability while making the administrative costs of the settlement permanent.

`COLDWAR_CUB_socialist_constitution` · Native card title: The Constitution.

Prerequisite: The First Congress.

Effects: Stability +6%; Weekly bureaucracy expenditure +4%; Professional Security replaces Committees of Defence: counterintelligence +10%, political power gain −4%, research −2% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### The Family Code · 35 days · (2,11)

The Federation of Cuban Women has brought the division of work within the home into the revolutionary debate. Equal responsibilities between spouses must be backed by childcare, maternity protection and opportunities to study and work. Those commitments widen participation while making social provision a continuing public obligation.

`COLDWAR_CUB_family_code` · Native card title: The Family Code.

Prerequisite: People's Power.

Effects: Available workforce +2%; Weekly welfare expenditure +6%; Treasury -0.20 (one time).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### Family Doctor Teams · 35 days · (2,12)

A doctor and a nurse assigned to a neighbourhood can follow families between illness, prevention and recovery. The Lawton experiment will become a programme of community teams linked to the polyclinics. Continuity of care requires training and a larger health budget, while coordinated referrals reduce duplicated work.

`COLDWAR_CUB_family_doctor_teams` · Native card title: Family Doctor Teams.

Prerequisite: The Family Code.

Effects: Healthcare workforce requirement -6%; Weekly healthcare expenditure +5%; Treasury -0.25 (one time); Healthcare budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### The Biological Front · 49 days · (10,13)

Interferon research has shown what a small, coordinated scientific team can attempt. A Biological Front linking the CIB and the new CIGB will connect laboratory research with industrial production in Havana. Genetic research needs protected funding and imported equipment, even when ordinary services compete for the same resources.

`COLDWAR_CUB_biological_front` · Native card title: The Biological Front.

Prerequisite: The First Congress.

Effects: Weekly education expenditure +8%; Treasury -0.90 (one time); State 854: +1 industrial complex; 1 × 50% research bonus · CAT_genetics.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### Continue the SDPE · 35 days · (4,14)

Enterprise accounts and material incentives can remain part of socialist planning. Keeping the system rewards efficient managers and producers, but leaves the state a smaller share of the income it generates.

`COLDWAR_CUB_sdpe_continuity` · Native card title: Continue the SDPE.

Prerequisite: Socialist Constitution.

Effects: Civilian industry productivity +10%; Agricultural productivity +10%; Tax revenue multiplier -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

Excludes: Rectify the Revolution.

#### Rectify the Revolution · 35 days · (8,14)

The leadership can reject what it regards as narrow material self-interest and return to mass mobilisation. Public works gain labour and urgency, while managers and researchers lose some autonomy and predictability.

`COLDWAR_CUB_rectification` · Native card title: Rectification.

Prerequisite: Socialist Constitution.

Effects: Available workforce +4%; Construction speed +8%; Civilian industry productivity -6%; Research speed -3%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

Excludes: Continue the SDPE.

#### Peasant Markets · 35 days · (4,15)

Farmers who fulfil state procurement quotas may sell eligible surplus directly to consumers. Keeping these markets preserves an incentive to produce food that rationed shops struggle to supply. Higher private returns and unequal purchasing power make the policy contentious, while a smaller share of agricultural receipts passes through the state.

`COLDWAR_CUB_peasant_markets` · Native card title: Peasant Markets.

Prerequisite: Continue the SDPE.

Effects: Agricultural productivity +12%; Agricultural district tax income -8%; Stability -2%; Treasury -0.20 (one time).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### Revive Microbrigades · 49 days · (8,15)

Workplaces can again release teams for housing, childcare centres and neighbourhood improvements. The microbrigades make social construction a visible collective project, supported by Havana's utilities and access works. Materials, supervision and time away from ordinary production remain real costs of mobilisation.

`COLDWAR_CUB_revive_microbrigades` · Native card title: Revive Microbrigades.

Prerequisite: Rectify the Revolution.

Effects: Construction speed +8%; Civilian industry productivity -3%; Weekly welfare expenditure +5%; Treasury -0.45 (one time); State 854: +1 infrastructure.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

#### A Cuban Socialism · 49 days · (6,16)

The revolution's social settlement should be able to survive a change of office-holder. A renewed education commitment and technical training will preserve national skills without pretending that social provision finances itself.

`COLDWAR_CUB_cuban_socialism` · Native card title: Cuban Socialism.

Prerequisite: Peasant Markets OR Revive Microbrigades.

Effects: Weekly education expenditure +5%; Treasury -0.30 (one time); Education budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment; 1 × 25% research bonus · CAT_electronics.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 4.

### Orthodox Planning Cadres

A post-purge Soviet-oriented cadre coalition, not an intact Microfracción in 1970.

#### Old Party Cadres · 35 days · (14,10)

The purge of the Microfracción did not erase the older communist administrative tradition. A rehabilitated Soviet-oriented coalition would promise disciplined government and expertise, while accepting greater exposure to Moscow's influence.

`COLDWAR_CUB_old_party` · Native card title: Old Party Cadres.

Prerequisite: Programme root.

Effects: Political power gain +8%; Research speed +3%; Foreign influence defence -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

#### Five-Year Balances · 35 days · (12,11)

A national plan can protect farms and factories from abrupt changes of priority. Stable allocations improve output but leave less room to redirect investment when local conditions change.

`COLDWAR_CUB_five_year_balances` · Native card title: Five-Year Balances.

Prerequisite: Old Party Cadres.

Effects: Agricultural productivity +15%; Civilian industry productivity +8%; Construction speed -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

Excludes: Enterprise Accounts.

#### Enterprise Accounts · 35 days · (16,11)

Production targets should be backed by accounts that expose waste and reward delivery. Enterprise responsibility improves industrial efficiency while diverting resources from agricultural mobilisation and reducing immediate revenue extraction.

`COLDWAR_CUB_enterprise_accounts` · Native card title: Enterprise Accounts.

Prerequisite: Old Party Cadres.

Effects: Civilian industry productivity +12%; Production efficiency growth +10%; Agricultural productivity -3%; Tax revenue multiplier -3%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

Excludes: Five-Year Balances.

#### Cadre Schools · 35 days · (12,12)

The plan needs administrators able to read technical reports and manage institutions. Specialised schools strengthen research capacity, while adding to the education establishment that the state must maintain.

`COLDWAR_CUB_cadre_schools` · Native card title: Cadre Schools.

Prerequisite: Five-Year Balances.

Effects: Research speed +4%; Weekly education expenditure +6%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

#### Managerial Duty · 35 days · (16,12)

Managers should be accountable for results rather than merely for optimistic reports. The resulting flexibility improves production and technical work, but unsettles cadres who relied on political protection.

`COLDWAR_CUB_manager_responsibility` · Native card title: Managerial Duty.

Prerequisite: Enterprise Accounts.

Effects: Civilian industry productivity +6%; Research speed +2%; Stability -2%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

#### Common Standards · 35 days · (14,13)

Common engineering standards will make imported machinery easier to maintain. Technical education offers a durable national gain while the current coalition remains responsible for the political terms of cooperation.

`COLDWAR_CUB_soviet_standards` · Native card title: Common Standards.

Prerequisite: Cadre Schools OR Managerial Duty.

Effects: Treasury -0.35 (one time); 2 × 25% research bonus · CAT_industry.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

#### A Planned Republic · 49 days · (14,14)

A disciplined planning republic can deliver a larger and more dependable agricultural surplus. Achieving it requires a permanent administrative network, not an assumption that every local producer will obey without supervision.

`COLDWAR_CUB_planned_republic` · Native card title: A Planned Republic.

Prerequisite: Common Standards.

Effects: Agricultural productivity +5%; Tax revenue multiplier +5%; Weekly bureaucracy expenditure +4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 6.

### Guevarist Mobilisation

Moral incentives or worker participation; a living political current, not Che's return.

#### The New Man · 35 days · (22,10)

Che's death left an ideal that still commands loyalty among militants and young volunteers. A government built around revolutionary commitment can mobilise labour, while its suspicion of technocratic autonomy constrains research.

`COLDWAR_CUB_unfinished_revolution` · Native card title: The New Man.

Prerequisite: Programme root.

Effects: Available workforce +3%; Ideology drift defence +10%; Research speed -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

#### Moral Incentives · 35 days · (20,11)

Public recognition and collective duty will take precedence over individual material rewards. Brigades can build and harvest quickly, but industrial managers cannot rely on the same incentives as a wage-led enterprise.

`COLDWAR_CUB_moral_incentives` · Native card title: Moral Incentives.

Prerequisite: The New Man.

Effects: Construction speed +14%; Agricultural productivity +8%; Civilian industry productivity -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

Excludes: Workers' Assemblies.

#### Workers' Assemblies · 35 days · (24,11)

A more participatory socialism would place workplace debates inside the production process. Worker initiative and available skills can improve output, while consultation reduces the government's ability to issue rapid commands.

`COLDWAR_CUB_workers_assemblies` · Native card title: Workers' Assemblies.

Prerequisite: The New Man.

Effects: Civilian industry productivity +10%; Available workforce +2%; Political power gain -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

Excludes: Moral Incentives.

#### The Young Brigades · 49 days · (20,12)

Young volunteers can be assigned a defined infrastructure project instead of another limitless campaign. The work remains a national asset after political fashions change, and the construction budget must still be paid.

`COLDWAR_CUB_young_brigades` · Native card title: The Young Brigades.

Prerequisite: Moral Incentives.

Effects: Treasury -0.50 (one time); State 1121: +1 infrastructure.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

#### Factory Councils · 35 days · (24,12)

Councils can take responsibility for maintenance and training at the factory floor. Local initiative improves civilian production, while less uniform working methods limit the gains available from a single national production standard.

`COLDWAR_CUB_factory_councils` · Native card title: Factory Councils.

Prerequisite: Workers' Assemblies.

Effects: Civilian industry productivity +8%; Weekly education expenditure +6%; Production efficiency cap -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

#### Solidarity First · 49 days · (22,13)

International solidarity is a commitment of people and resources rather than an export commodity. The government can sustain an additional volunteer formation, while accepting higher recurring military personnel expenditure.

`COLDWAR_CUB_solidarity_profit` · Native card title: Solidarity First.

Prerequisite: The Young Brigades OR Factory Councils.

Effects: Volunteer division limit +1; Weekly army personnel expenditure +5%; Army experience +25.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 19.

### FAR · National Administration

Raúl's professional military current, administrative engineering or a combat-first force.

#### Professional Rule · 35 days · (30,10)

The FAR's professional officers can promise a disciplined succession and a state that carries out its decisions. Military management improves organisation and administrative efficiency while narrowing civilian political autonomy.

`COLDWAR_CUB_professional_revolution` · Native card title: Professional Rule.

Prerequisite: Programme root.

Effects: Division organisation +6%; Weekly bureaucracy expenditure -4%; Political power gain -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

#### Barracks and Works · 35 days · (28,11)

Military engineering and procurement organisations can be used to deliver civilian projects. Their discipline accelerates construction and production, but a larger permanent military establishment draws labour away from other work.

`COLDWAR_CUB_barracks_workshops` · Native card title: Barracks and Works.

Prerequisite: Professional Rule.

Effects: Construction speed +12%; Civilian industry productivity +6%; Available workforce -2%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

Excludes: Soldiers, Not Firms.

#### Soldiers, Not Firms · 35 days · (32,11)

The armed forces can refuse a permanent role in commercial management and concentrate on readiness. Better organisation and faster training then come at the expense of the engineering capacity that civilian projects might have borrowed.

`COLDWAR_CUB_soldiers_not_managers` · Native card title: Soldiers, Not Firms.

Prerequisite: Professional Rule.

Effects: Division organisation +10%; Division training time -8%; Construction speed -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

Excludes: Barracks and Works.

#### Military Engineers · 49 days · (28,12)

An eastern infrastructure programme gives military engineers a concrete civilian assignment. The investment improves national connections without turning the armed forces into an unlimited source of free construction.

`COLDWAR_CUB_military_engineering` · Native card title: Military Engineers.

Prerequisite: Barracks and Works.

Effects: Treasury -0.55 (one time); State 855: +1 infrastructure; Army experience +15.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

#### A Command College · 35 days · (32,12)

A professional command college can turn operational experience into a common doctrine. Its instructors and facilities require funding, while the knowledge earned by the officer corps remains a national asset.

`COLDWAR_CUB_command_college` · Native card title: A Command College.

Prerequisite: Soldiers, Not Firms.

Effects: Treasury -0.30 (one time); Army experience +25; 1 × 50% land doctrine cost reduction.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

#### Accountable Officers · 35 days · (30,13)

Procurement and promotion need standards that bind commanders as well as civilians. Audits reduce corruption and improve confidence, while a professional establishment carries a higher personnel bill than informal revolutionary service.

`COLDWAR_CUB_accountable_officers` · Native card title: Officer Standards.

Prerequisite: Military Engineers OR A Command College.

Effects: Stability +3%; Weekly army personnel expenditure +5%; Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment; Professional Security replaces Committees of Defence: counterintelligence +10%, political power gain −4%, research −2% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

#### Orderly Succession · 49 days · (30,14)

The government will define how authority passes between offices instead of leaving succession to personal allegiance. The settlement improves continuity, while a less personalised revolutionary identity offers weaker protection against ideological drift.

`COLDWAR_CUB_orderly_succession` · Native card title: Orderly Succession.

Prerequisite: Accountable Officers.

Effects: Political power gain +8%; Stability +6%; Division organisation +3%; Ideology drift defence -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 22.

### Auténtico · Social Republic

Labour guarantees or a negotiated investment settlement under the republican tradition.

#### The Social Republic · 35 days · (38,10)

The Auténtico tradition can reclaim the republic without abandoning social insurance and national sovereignty. A negotiated return broadens confidence and inward migration, but rebuilding civilian institutions requires an administrative settlement.

`COLDWAR_CUB_authentic_republic` · Native card title: The Social Republic.

Prerequisite: Programme root.

Effects: Native migration rate +3%; Stability +4%; Weekly bureaucracy expenditure +5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

#### Labour's Guarantee · 35 days · (36,11)

Trade unions and workers need enforceable guarantees that political change will not erase the revolution's social gains. Those guarantees widen participation and confidence, while raising the cost of the welfare settlement.

`COLDWAR_CUB_labour_guarantee` · Native card title: Labour's Guarantee.

Prerequisite: The Social Republic.

Effects: Available workforce +5%; Stability +6%; Weekly welfare expenditure +10%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

Excludes: Investment with Rights.

#### Investment with Rights · 35 days · (40,11)

Investment can be welcomed without restoring an unrestricted pre-revolutionary property order. Production and construction benefit, while negotiated concessions reduce the revenue immediately captured by the state.

`COLDWAR_CUB_investment_rights` · Native card title: Investment Rights.

Prerequisite: The Social Republic.

Effects: Civilian industry productivity +12%; Construction speed +8%; Tax revenue multiplier -6%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

Excludes: Labour's Guarantee.

#### Social Insurance · 35 days · (36,12)

A republican government will fund a health service that survives a change of party. Expanding public healthcare is a lasting institutional commitment with a continuing fiscal cost.

`COLDWAR_CUB_social_insurance` · Native card title: Social Insurance.

Prerequisite: Labour's Guarantee.

Effects: Weekly healthcare expenditure +5%; Treasury -0.30 (one time); Healthcare budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

#### A Mixed Economy · 35 days · (40,12)

Private enterprise, cooperatives and a public sector can coexist under a common administrative framework. Integrating displaced families into ordinary work is a practical test of that promise, and requires more than a declaration of reconciliation.

`COLDWAR_CUB_mixed_economy` · Native card title: A Mixed Economy.

Prerequisite: Investment with Rights.

Effects: Refugee integration rate +20%; Civilian industry productivity +5%; Weekly bureaucracy expenditure +6%; Treasury -0.25 (one time).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

#### An Authentic Pact · 49 days · (38,13)

The settlement should bind labour leaders, public officials and enterprise managers to transparent rules. Reducing corruption and sustaining education give the restored republic substance beyond an anti-Castro coalition.

`COLDWAR_CUB_authentic_settlement` · Native card title: An Authentic Pact.

Prerequisite: Social Insurance OR A Mixed Economy.

Effects: Treasury -0.30 (one time); Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment; Education budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 3.

### Ortodoxo · Sovereign Republic

Chibás's anti-corruption and social-national tradition, separate from the Auténticos.

#### Integrity over Money · 35 days · (6,18)

The moral authority of Chibás rests on honest government rather than another patronage machine. An Ortodoxo cabinet will begin by confronting corruption, accepting the cost of an administration capable of investigating its own supporters.

`COLDWAR_CUB_shame_money` · Native card title: Integrity over Money.

Prerequisite: Programme root.

Effects: Weekly bureaucracy expenditure +3%; Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

#### Sovereign Republic · 35 days · (4,19)

Neither Soviet tutelage nor a return to American predominance can define the new republic. A sovereign course strengthens resistance to outside pressure, while limiting some opportunities for foreign commerce.

`COLDWAR_CUB_independent_republic` · Native card title: Independent Cuba.

Prerequisite: Integrity over Money.

Effects: Foreign influence defence +20%; Imperia sanction resistance +10%; Resource export revenue -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

Excludes: Social Citizenship.

#### Social Citizenship · 35 days · (8,19)

National independence must have a social purpose. Education and access to work can widen the republic's domestic foundation, while a larger welfare settlement makes demands on the weekly budget.

`COLDWAR_CUB_social_republic` · Native card title: Social Citizenship.

Prerequisite: Integrity over Money.

Effects: Research speed +6%; Available workforce +3%; Weekly welfare expenditure +12%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

Excludes: Sovereign Republic.

#### Public Accounts · 35 days · (4,20)

An honest revenue system needs published accounts and officials who can resist discretionary favours. Tax collection and administrative efficiency improve, while stronger oversight constrains executive political freedom.

`COLDWAR_CUB_public_accounts` · Native card title: Public Accounts.

Prerequisite: Sovereign Republic.

Effects: Tax revenue multiplier +8%; Weekly bureaucracy expenditure -5%; Political power gain -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

#### Land and Labour · 35 days · (8,20)

Agrarian reform can be defended without allowing every farm decision to be made in Havana. Better incentives raise output and available work, while the treasury relinquishes part of its agricultural district receipts.

`COLDWAR_CUB_land_labour` · Native card title: Land and Labour.

Prerequisite: Social Citizenship.

Effects: Agricultural productivity +14%; Available workforce +2%; Agricultural district tax income -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

#### The Promise of 1940 · 49 days · (6,21)

The constitution's social and national promises need courts, public scrutiny and a government willing to be bound by them. Stability and research benefit from predictable institutions, while executive bargaining becomes more demanding.

`COLDWAR_CUB_promise_1940` · Native card title: The Promise of 1940.

Prerequisite: Public Accounts OR Land and Labour.

Effects: Stability +6%; Research speed +4%; Political power gain -4%; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 18.

### Christian Democratic Movement

Subsidiarity or a national social-market compact; church mediation without a theocracy.

#### Civic Reconciliation · 35 days · (14,18)

Christian democrats can offer an institutional bridge between religious citizens, moderate exiles and a population dependent on public services. Reconciliation strengthens confidence and inward migration, while rebuilding municipal administration has a cost.

`COLDWAR_CUB_civic_reconciliation` · Native card title: Civic Reconciliation.

Prerequisite: Programme root.

Effects: Native migration rate +3%; Stability +3%; Weekly bureaucracy expenditure +5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

#### Subsidiarity · 35 days · (12,19)

Municipalities and voluntary institutions should carry responsibilities they can fulfil locally. A smaller central bureaucracy and more responsive enterprises come at the price of a narrower national tax base.

`COLDWAR_CUB_subsidiarity` · Native card title: Subsidiarity.

Prerequisite: Civic Reconciliation.

Effects: Weekly bureaucracy expenditure -12%; Civilian industry productivity +8%; Tax revenue multiplier -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

Excludes: Social-Market Pact.

#### Social-Market Pact · 35 days · (16,19)

Employers, workers and the government can bargain over a shared social-market settlement. Participation and reliable revenue improve, while nationally guaranteed benefits remain an obligation of the weekly budget.

`COLDWAR_CUB_social_market` · Native card title: Social-Market Pact.

Prerequisite: Civic Reconciliation.

Effects: Available workforce +3%; Tax revenue multiplier +8%; Weekly welfare expenditure +10%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

Excludes: Subsidiarity.

#### Parish and Town · 35 days · (12,20)

Local schools and voluntary associations can help displaced families enter ordinary civic life. Their contribution reduces public provision costs, while concentrating resources on basic services rather than specialist research.

`COLDWAR_CUB_parish_municipality` · Native card title: Parish and Town.

Prerequisite: Subsidiarity.

Effects: Weekly education expenditure -8%; Refugee integration rate +15%; Research speed -1%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

#### Family and Wages · 35 days · (16,20)

A family policy needs healthcare and a dependable social wage rather than slogans about morality. Public healthcare receives additional funding, with population and fiscal effects that develop over time.

`COLDWAR_CUB_family_wages` · Native card title: Family and Wages.

Prerequisite: Social-Market Pact.

Effects: Monthly population growth factor +3%; Weekly healthcare expenditure +5%; Healthcare budget +1 native tier; at maximum: named service efficiency (weekly sector expenditure −3%); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

#### Pluralist Covenant · 49 days · (14,21)

A durable covenant must protect believers and non-believers and bind the government to constitutional rights. Broader legitimacy strengthens the country against outside pressure, while negotiation limits the executive's personal freedom.

`COLDWAR_CUB_pluralist_covenant` · Native card title: Pluralist Covenant.

Prerequisite: Parish and Town OR Family and Wages.

Effects: Stability +5%; Foreign influence defence +10%; Political power gain -5%; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 1.

### Constitutional Liberal Republic

Claims bonds or property restitution, courts and a free public sphere.

#### Courts before Factions · 35 days · (22,18)

The constitutionalists' first task is to bind the victors to rules they cannot change for private advantage. Independent courts improve confidence in research and administration, while limiting executive political discretion.

`COLDWAR_CUB_courts_factions` · Native card title: Courts before Factions.

Prerequisite: Programme root.

Effects: Research speed +3%; Political power gain -6%; Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

#### Claims Bonds · 35 days · (20,19)

Compensation bonds can acknowledge lawful claims without evicting every current occupier. The settlement protects stability and resilience, while adding a real public debt obligation; it is not a cash windfall for the government.

`COLDWAR_CUB_compensation_bonds` · Native card title: Claims and Bonds.

Prerequisite: Courts before Factions.

Effects: Stability +7%; Imperia sanction resistance +8%; Debt principal +0.50; cash is a separate effect.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

Excludes: Guarded Restitution.

#### Guarded Restitution · 35 days · (24,19)

Restitution under judicial safeguards can attract exile capital more quickly than a long bond settlement. It also reopens disputes over homes, farms and employment, with an immediate social cost.

`COLDWAR_CUB_restitution` · Native card title: Guarded Restitution.

Prerequisite: Courts before Factions.

Effects: Civilian industry productivity +15%; Construction speed +8%; Stability -5%; Available workforce -1%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

Excludes: Claims Bonds.

#### Judicial Guarantees · 35 days · (20,20)

Enforceable rights will make it easier to integrate displaced people and replace discretionary administrative decisions. Judicial independence improves that process, while restricting the government's political leverage over individual cases.

`COLDWAR_CUB_judicial_guarantees` · Native card title: Judicial Guarantees.

Prerequisite: Claims Bonds.

Effects: Refugee integration rate +20%; Weekly bureaucracy expenditure -8%; Political power gain -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

#### Commercial Courts · 35 days · (24,20)

Commercial courts can make investment contracts credible without surrendering the right to regulate them. Construction and enterprise output benefit, while tax concessions form part of the negotiated settlement.

`COLDWAR_CUB_commercial_courts` · Native card title: Commercial Courts.

Prerequisite: Guarded Restitution.

Effects: Construction speed +10%; Civilian industry productivity +6%; Tax revenue multiplier -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

#### An Open Press · 35 days · (22,21)

An open press can expose official failure and widen technical debate. Research benefits from the circulation of ideas, while a less controlled public sphere is also more accessible to foreign influence.

`COLDWAR_CUB_open_press` · Native card title: An Open Press.

Prerequisite: Judicial Guarantees OR Commercial Courts.

Effects: Research speed +7%; Foreign influence defence -10%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

#### Constitutional Order · 49 days · (22,22)

A competitive republic needs a revenue system and an administration that can serve an opposition government as well as the current cabinet. Better collection and expertise require maintaining that public establishment.

`COLDWAR_CUB_constitutional_order` · Native card title: Civil Government.

Prerequisite: An Open Press.

Effects: Tax revenue multiplier +8%; Research speed +3%; Weekly bureaucracy expenditure +4%; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 2.

### RECE · Exile Directorate

A hard anti-communist transition with a choice between restoration and state-led rebuilding.

#### Exile Directorate · 35 days · (30,18)

An exile directorate would bring organised outside contacts and a command structure to a fractured transition. Its authority improves military coordination and diplomacy, while lacking the domestic legitimacy of a settled constitutional order.

`COLDWAR_CUB_exile_directorate` · Native card title: Exile Directorate.

Prerequisite: Programme root.

Effects: Division organisation +5%; Foreign influence +10%; Stability -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 0.

#### Restoration First · 35 days · (28,19)

Returning capital and commercial networks can rebuild civilian production quickly. An uncompromising restoration also deepens property conflict and makes the new order more vulnerable to the patrons on which it relies.

`COLDWAR_CUB_restoration_first` · Native card title: Restoration First.

Prerequisite: Exile Directorate.

Effects: Civilian industry productivity +18%; Construction speed +10%; Foreign influence defence -12%; Stability -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 0.

Excludes: Development First.

#### Development First · 35 days · (32,19)

The directorate can postpone full restitution and make reconstruction its first claim to authority. Publicly directed investment improves construction and resilience, while maintaining a costly administrative machine.

`COLDWAR_CUB_development_first` · Native card title: Development First.

Prerequisite: Exile Directorate.

Effects: Construction speed +18%; Imperia sanction resistance +8%; Weekly bureaucracy expenditure +8%; Civilian industry productivity -2%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 0.

Excludes: Restoration First.

#### National Settlement · 35 days · (30,20)

The transition cannot be governed indefinitely by rival exile committees. A settlement against patronage and private revenge improves confidence, while requiring the directorate to surrender some of its discretion.

`COLDWAR_CUB_national_settlement` · Native card title: National Settlement.

Prerequisite: Restoration First OR Development First.

Effects: Stability +5%; Political power gain -4%; Treasury -0.30 (one time); Corruption −1 native tier; at tier 1: named Public Oversight (weekly bureaucracy expenditure −3%, once, non-stacking); missing tier blocks enactment.

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 0.

#### Provisional Charter · 49 days · (30,21)

A provisional charter must say who will govern after the emergency. A civilian timetable and an extended directorate are different settlements, to be resolved through the existing party system rather than by replaying reconstruction rewards.

`COLDWAR_CUB_provisional_charter` · Native card title: Civilian Transition.

Prerequisite: National Settlement.

Effects: Enact a 365-day civilian transition charter; oversight: Stability +3 points, Political power gain −5%; expiry opens a civilian governing settlement; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 0.

### Alpha 66 · National Liberation

Civic demobilisation or an armed nationalist settlement; distinct from RECE and Batista.

#### Cuban-Led Liberation · 35 days · (38,18)

Alpha 66's armed exile networks would need to form a governing coalition after Castro's fall. A nationalist cabinet could defend sovereignty while placing stricter conditions on outside commerce, reducing resource export earnings.

`COLDWAR_CUB_cuban_liberation` · Native card title: Cuban Liberation.

Prerequisite: Programme root.

Effects: Core territory defence +8%; Foreign influence defence +15%; Resource export revenue -6%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 20.

#### A Civic Resistance · 35 days · (36,19)

The movement can convert resistance networks into civilian organisations and seek the return of families abroad. Research and inward migration benefit, while the armed establishment loses some of its cohesion and priority.

`COLDWAR_CUB_civic_resistance` · Native card title: A Civic Resistance.

Prerequisite: Cuban-Led Liberation.

Effects: Research speed +5%; Native migration rate +5%; Division organisation -3%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 20.

Excludes: Veterans' Directorate.

#### Veterans' Directorate · 35 days · (40,19)

Veterans can instead retain a central role in the state and build a professional nationalist force. Readiness improves, while military priorities constrain civilian enterprise and political bargaining.

`COLDWAR_CUB_veterans_directorate` · Native card title: Veterans in Office.

Prerequisite: Cuban-Led Liberation.

Effects: Division organisation +12%; Division training time -8%; Civilian industry productivity -6%; Political power gain -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 20.

Excludes: A Civic Resistance.

#### Veterans into Work · 35 days · (36,20)

Demobilisation should provide ordinary work rather than abandon veterans to factional patrons. The economy gains labour and the army budget contracts, at the cost of a smaller specialist military establishment.

`COLDWAR_CUB_veterans_civil_life` · Native card title: Veterans into Work.

Prerequisite: A Civic Resistance.

Effects: Available workforce +4%; Weekly army personnel expenditure -8%; Special forces capacity -2%; Civilian Security replaces the earlier security institution: counterintelligence +5%, weekly bureaucracy expenditure +3% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 20.

#### Armed Sovereignty · 49 days · (40,20)

A fortified sovereign republic can resist pressure from old patrons as well as new enemies. Its defensive strength and resilience come with a larger supervisory state and less room for independent research.

`COLDWAR_CUB_armed_sovereignty` · Native card title: Armed Sovereignty.

Prerequisite: Veterans' Directorate.

Effects: Core territory defence +10%; Imperia sanction resistance +12%; Research speed -4%; Weekly bureaucracy expenditure +4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 20.

### OSPAAAL · Tricontinental Solidarity

Diplomatic solidarity or a larger overseas cadre network.

#### Tricontinental Secretariat · 35 days · (46,10)

An OSPAAAL-led governing alignment would place the Tricontinental network at the centre of Cuban diplomacy. Its established channels increase international influence, while coordinating them adds to the administrative burden.

`COLDWAR_CUB_tricontinental_secretariat` · Native card title: Tricontinental Office.

Prerequisite: Programme root.

Effects: Foreign influence +6%; Weekly bureaucracy expenditure +3%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 5.

#### Diplomatic Solidarity · 35 days · (44,11)

Political solidarity can be carried through conferences, public campaigns and non-military exchanges. Cuba gains influence among partners without diverting a large share of trained labour into permanent overseas missions.

`COLDWAR_CUB_diplomatic_solidarity` · Native card title: Diplomatic Solidarity.

Prerequisite: Tricontinental Secretariat.

Effects: Foreign influence +10%; Foreign influence defence +5%; Available workforce -0%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 5.

Excludes: Foreign Cadres.

#### Foreign Cadres · 35 days · (48,11)

Havana can instead expand the cadres assigned to liberation movements and allied institutions. The wider network strengthens Cuban influence, but takes trained staff from domestic services and makes independent diplomacy harder.

`COLDWAR_CUB_foreign_cadres` · Native card title: Foreign Cadres.

Prerequisite: Tricontinental Secretariat.

Effects: Foreign influence +18%; Available workforce -2%; Weekly bureaucracy expenditure +8%; Foreign influence defence -5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 5.

Excludes: Diplomatic Solidarity.

### MININT · Interior Administration

Professional intelligence or intensive mass surveillance.

#### The Interior Ministry · 35 days · (46,18)

A MININT-led administration would make internal security the first responsibility of the state. Counterintelligence and executive coordination improve, while the larger security apparatus raises bureaucratic costs and narrows political discretion.

`COLDWAR_CUB_interior_ministry` · Native card title: The Interior Ministry.

Prerequisite: Programme root.

Effects: Counterintelligence defence +15%; Weekly bureaucracy expenditure +6%; Political power gain -3%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 7.

#### Professional Intelligence · 35 days · (44,19)

A smaller professional service can concentrate on foreign penetration, critical infrastructure and accountable investigations. Better analysis aids research and defensive security, though specialised personnel and oversight remain costly.

`COLDWAR_CUB_professional_intelligence` · Native card title: Intelligence Service.

Prerequisite: The Interior Ministry.

Effects: Counterintelligence defence +10%; Research speed +3%; Weekly bureaucracy expenditure +4%; Available workforce -0%; Professional Security replaces Committees of Defence: counterintelligence +10%, political power gain −4%, research −2% (one national institution).

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 7.

Excludes: Mass Surveillance.

#### Mass Surveillance · 35 days · (48,19)

The ministry can instead expand local surveillance and political reporting through mass organisations. This increases the state's capacity to watch and control, while skilled workers leave productive services and public debate becomes more restricted.

`COLDWAR_CUB_mass_surveillance` · Native card title: Mass Surveillance.

Prerequisite: The Interior Ministry.

Effects: Counterintelligence defence +20%; Political power gain -8%; Research speed -5%; Available workforce -2%; Foreign influence defence -8%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 7.

Excludes: Professional Intelligence.

### JUCEPLAN · Central Planning Board

Balanced national plans or enterprise incentives and delegated initiative.

#### National Plan Balances · 35 days · (54,10)

A JUCEPLAN-led government would begin by reconciling production targets with transport, labour and imported inputs. Better coordination supports civilian output, while the planning apparatus adds a permanent administrative cost.

`COLDWAR_CUB_plan_balances` · Native card title: National Plan Balances.

Prerequisite: Programme root.

Effects: Civilian industry productivity +5%; Agricultural productivity +4%; Weekly bureaucracy expenditure +5%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 13.

#### Balanced Targets · 35 days · (52,11)

Investment plans can protect maintenance, food production and consumer goods alongside export targets. Agricultural and civilian output improve together, while slower capital concentration limits construction speed.

`COLDWAR_CUB_balanced_targets` · Native card title: Balanced Targets.

Prerequisite: National Plan Balances.

Effects: Agricultural productivity +10%; Civilian industry productivity +6%; Construction speed -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 13.

Excludes: Enterprise Incentives.

#### Enterprise Incentives · 35 days · (56,11)

Managers and work collectives can receive clearer production targets and retain a larger role in local decisions. Factory efficiency and civilian output rise, while agricultural planning and central tax receipts lose some priority.

`COLDWAR_CUB_enterprise_incentives` · Native card title: Enterprise Incentives.

Prerequisite: National Plan Balances.

Effects: Civilian industry productivity +10%; Production efficiency growth +5%; Agricultural productivity -4%; Tax revenue multiplier -4%; .

Lifetime: Party programme; inactive outside its exact governing subparty.

Requirements: Exact governing subparty 13.

Excludes: Balanced Targets.

## Bilateral agreements

### Soviet Technical Assistance

- SOV pays 0.30 Treasury; CUB pays 0.10 Treasury on acceptance.
- CUB receives one 25% industry research bonus and an active assistance programme: sanction resistance +15%, foreign influence defence -15%.
- SOV receives +15 bilateral opinion; no subject status, forced faction membership or automatic funding stream.

Guard: Both exist and are at peace with each other; pending offer expires after 90 days; repeat acceptance cannot repeat payment or research.

Implementation: New bilateral event/receipt glue using native money, opinion and research APIs.

### CMEA Admission

- Acceptance grants the actual COLDWAR_CUB_cmea_member idea; no automatic money or factories.
- Application costs CUB 0.10 Treasury only on accepted admission; member content requires this spirit in availability and reward guards.

Guard: Admission is before the member-only focus. Exit removes membership and suspends its active programme without replaying grants on readmission.

Implementation: Cuba-specific admission contract. Main MD 2000 has no reusable general CMEA membership provider; integrate with Cold War Soviet commonwealth content rather than inventing a parallel economic simulator.

### Air Defence Training

- CUB pays 0.45 Treasury; SOV pays 0.15 Treasury on acceptance.
- CUB receives one radar level in a legal Cuban state and one 25% radar research use; no aircraft or missiles are spawned.

Guard: Both governments consent; verify owned/controlled target and radar level cap before either charge.

Implementation: New agreement glue; native building/research providers.

### Requested Medical Mission

- CUB pays 0.15 Treasury; recipient pays 0.10 Treasury on acceptance.
- Recipient receives healthcare expenditure -5% for 365 days; Cuba receives +15 bilateral opinion.
- Cuba's Medical Brigades programme raises weekly healthcare expenditure by 10%; no workforce reduction or second flat upkeep debit.

Guard: Recipient requests or accepts the mission, is not at war with Cuba, and has a working health budget. Refusal/expiry charges nobody.

Implementation: New Cuba diplomatic offer; does not treat a generic health-cost reduction as literal donated hospital equipment.

### Requested Overseas Assistance

- An accepted request opens ordinary native military/volunteer diplomacy and a scoped advisory decision.
- CUB pays 0.20 Treasury and recipient receives 15 army experience once; troop/equipment transfers use actual native stocks and consent.
- No annexation, invented divisions, automatic war or generic occupation-state support shortcut.

Guard: Recipient controls its response. Angola/Ethiopia/Grenada are historical contexts, not 1970 pre-annexation targets. Recheck independence, war and available troops at use.

Implementation: New recipient-owned request/receipt; no general Cuban Colonial Affairs provider currently exists.

### A Cuban–American Settlement

- USA may refuse, accept limited easing, or negotiate a full executive trade settlement.
- Limited easing: CUB Treasury -0.10; reciprocal opinion +10. Residual embargo burden: resource export revenue -10%, civilian productivity -3%.
- Full settlement: total CUB Treasury -0.25 (-0.15 further if the commission already cost -0.10); reciprocal opinion +20. Remove the actual US trade embargo and its Cuban fallback burden.
- The 1970–90 executive may alter or end the embargo. MFN tariff treatment, official credits, private claims and Guantánamo require separate terms; later 1996 legislation is not applied retroactively.

Guard: Explicit US acceptance; check actual native US embargo/Imperia sanction state and remove only agreed restrictions. Exactly-once commission receipt prevents repeat payment. Neither talks nor Interests Sections alone remove the embargo.

Implementation: Bilateral acceptance and sanction reconciliation using existing embargo/opinion APIs; new event/receipt logic. Historical authority: Ford Library 1976 transition report Appendix I and State Department LIBERTAD history.

### Berlin–Havana Commission

- On acceptance CUB and DDR each pay 0.10 Treasury and receive one 25% electronics research use.
- Both receive +15 opinion. No island transfer or building is included.

Guard: DDR exists, peace, pending transaction fresh, each grant exactly once. Island diplomacy remains reachable before CMEA membership.

Implementation: New Cuba–DDR agreement with acceptance revalidation.

### Playa RDA Cultural Programme

- The island is renamed while Cuban sovereignty remains unchanged, as in the historical gesture.
- If the optional programme is accepted: the GDR pays 0.20 Treasury, Cuba pays 0.05 Treasury; each receives one 25% electronics research use.
- Cuba's cooperation programme gives research speed +2% and education expenditure +3%; no naval base is built.

Guard: Cuba owns and administers State 1252, the GDR exists, and no cession has been ratified. A symbolic name does not change sovereignty.

Implementation: Cultural cooperation agreement with costs displayed in the decision.

### Actual Island Cession · Alternate History

- DDR acceptance: Treasury -0.40; Cuba: Treasury +0.40 and Stability -3 percentage points.
- Rename State 1252 to Ernst Thälmann Island; DDR receives only State 1252. Retain CUB core; add no automatic DDR core.
- Cuba: one 50% industry research use after ratification. DDR obtains a strategic location, but all future facilities require normal paid construction.
- Refusal leaves Cuba's ownership and Treasury unchanged. Development Protocol ratifies use rights; it pays no second compensation.

Guard: Explicit DDR acceptance; recheck Cuba owns/controls 1252, peace and pending offer at handover. Charge and transfer atomically; no capital move, mainland transfer or automatic port.

Implementation: New one-time cession event chain using native transfer_state, set_state_name and Treasury APIs.

## Historical event layer

### The Ten Million Ton Harvest · 1970-05-19 to 1970-07-26

The harvest campaign is unresolved; final national results are recorded at the July 26 review.

July 26 settlement: economic adjustments last 180 days; stability changes once. Remove the original campaign first; the separate recovery burden lasts 90/180 days by the completed harvest course.

- Concentrate Through the Final Cut: Agricultural productivity +8% for 180 days; Construction speed -5% for 180 days; Stability +2 percentage points
- Return Labour to the Wider Economy: Civilian industry productivity +5% for 180 days; Agricultural productivity -3% for 180 days; Stability -2 percentage points

On 19 May 1970 Fidel Castro publicly acknowledged that the ten-million-ton target would not be met. The 1970 harvest reached about 8.54 million metric tons, a record but short of the goal; final results were announced at the 26 July celebration. The campaign's labour and transport diversion left broader economic costs. Sources: https://cubanstudies.history.ufl.edu/gems-of-the-archive/the-ten-million-ton-harvest-of-1970/ ; https://ascecubadatabase.org/asce_proceedings/cubas-sugar-industry-in-the-1990s-potential-exports-to-the-u-s-and-world-markets/

### Cuban Forces in Angola · 1975-11 onward

Angola approaches independence amid civil war; the MPLA requests Cuban assistance and a lawful recipient relationship is available. The historical conflict and an independent consenting recipient must actually exist; the calendar alone cannot create either.

Active only while the accepted mission is operating. Withdraw or terminate the recipient agreement to remove both its benefits and recurring burdens; no free troops are created.

- Commit Expeditionary Forces: Foreign influence +8%; Army personnel expenditure +8%; Civilian industry productivity -3%; Stability -2 percentage points
- Limit the Commitment to Advisers and Medical Teams: Foreign influence +4%; Army personnel expenditure +3%; Stability +1 percentage point

Cuba began a large military intervention in Angola in November 1975 after the MPLA sought its assistance; Cuban troops helped defend Luanda before independence on 11 November. This was an expeditionary commitment with substantial military and economic costs, not simply a volunteer programme. The scale and continuation remain contingent on Cuban decisions in alternate history. Source: https://history.state.gov/milestones/1969-1976/angola ; https://history.state.gov/historicaldocuments/frus1969-76v28/d132

### Interests Sections in Havana and Washington · 1977-07-01 / 1977-09-01

Both governments consent to a limited diplomatic arrangement while the broader dispute remains unsettled.

365 days for the influence adjustment; offices and agreement receipt persist until mutually closed.

- Open Reciprocal Interests Sections: CUB and USA each pay 0.05 Treasury on mutual acceptance; Bilateral opinion +10 in both directions; Foreign influence defence -2% for 365 days; Stability +1 percentage point; The embargo remains in force
- Defer the Arrangement: Stability +1 percentage point; No change to the embargo or diplomatic status

On 1 July 1977, both governments announced reciprocal Interests Sections, which opened on 1 September in the Swiss and Czechoslovak embassies respectively. This restored limited official contact; it did not normalize relations or end the statutory embargo. Source: https://history.state.gov/historicaldocuments/frus1977-80v23/d18

### The Ogaden War · 1977-11 onward

The Somali invasion of Ethiopia intensifies; Ethiopia requests Cuban assistance and the government must choose its level of commitment. The historical conflict and an independent consenting recipient must actually exist; the calendar alone cannot create either.

Active only while the accepted mission is operating. Withdraw or terminate the recipient agreement to remove both its benefits and recurring burdens; no free troops are created.

- Deploy a Combat Force: Foreign influence +8%; Army personnel expenditure +7%; Civilian industry productivity -3%; Stability -2 percentage points
- Provide Advisers and Medical Support: Foreign influence +4%; Army personnel expenditure +2%; Stability +1 percentage point
- Decline a New Deployment: Army personnel expenditure -1%; Foreign influence -2%

Cuban forces were deployed to Ethiopia during the 1977–78 Ogaden War, alongside Soviet support for Mengistu's government. The deployment followed earlier Cuban activity in Africa and carried real personnel and logistical costs. Source: https://history.state.gov/historicaldocuments/frus1977-80v17/d103

### Dialogue with the Cuban Community Abroad · 1978-11 to 1979

Representatives of the government and Cuban communities abroad agree to meet and define a limited humanitarian and family agenda.

One-time humanitarian/legitimacy settlement. Programme effects do not repeat on reopening talks; any physical return requires a registered voluntary migration transaction.

- Implement the December Agreement: Pardon 3,000 prisoners convicted of state-security offences and 600 convicted of emigration-law violations, as stated in the agreement; Stability +3 percentage points; Foreign influence defence -2%; Register actual family migration through the existing migration ledger
- Keep Dialogue Narrow: Stability +1 percentage point; Foreign influence defence +1%; No additional migration is recorded

On 8 December 1978, the Committee of 75 and Cuban government representatives signed an agreement on prisoners, family reunification and visits. The government announced pardon of 3,000 prisoners convicted of offences against state security or national integrity and 600 convicted under emigration provisions. It did not create a multiparty system or end political restrictions. Migration counts must use the existing ledger and must not subtract the same people twice. Source: https://cidh.oas.org/countryrep/Cuba79eng/chap.4.htm

### The Havana Non-Aligned Summit · 1979-09-03 to 1979-09-09

Cuba has accepted the 1979 summit hosting role through diplomacy. Cuba is already a NAM founding participant; no accession or guaranteed Soviet allegiance is implied.

365 days for programme modifiers; opinion/stability are one-time effects.

- Build a Broad Conference: Foreign influence +6%; Stability +2 percentage points; Weekly bureaucracy expenditure +2%
- Press the Anti-Imperialist Platform: Foreign influence +10%; Foreign influence defence -3%; Bilateral opinion with the Soviet Union +5

Cuba was a founding participant in the Non-Aligned Movement in 1961; the Havana summit of 3–9 September 1979 was a major expression of its chairmanship, not accession. Source: https://www.nam.go.ug/history ; https://www.nam.go.ug/previous-chairmanship-documents

### The Mariel Exodus · 1980-04-04 to 1980-09-26

Only if a comparable asylum crisis and pent-up departure pressure actually arise under the revolutionary government. USA must consent to the reception/transport arrangement; no fixed historical total is removed automatically.

Stability is a one-time political effect; influence-defence adjustments last 180 days. Actual migration occurs only once through the population ledger.

- Open Mariel for an Organised Departure: Stability -5 percentage points; Foreign influence defence -3%; Record actual emigrants once through the existing migration ledger
- Restrict Departures to Negotiated Cases: Stability -2 percentage points; Foreign influence defence +1%; Record only departures that actually occur

Cuban guards were withdrawn from the Peruvian embassy on 4 April 1980; the asylum crowd then grew rapidly. On 20 April Fidel Castro announced that the port of Mariel would be opened for departures, and the exodus continued until 26 September. About 125,000 people left; political coercion accompanied some departures. Historical totals belong in the existing migration ledger and should not also be removed by this event. Sources: https://history.state.gov/historicaldocuments/frus1977-80v23/d89 ; https://www.washingtonpost.com/archive/politics/1980/04/06/cuba-to-allow-exodus-of-1500-in-asylum-at-peruvian-embassy/b7b27181-ebfd-4dd8-960b-a4981c6497dd

### Rectification of Errors and Negative Tendencies · 1986-02 onward

Only under a PCC government. An earlier completed SDPE/Rectification verdict is respected; the congress cannot grant its economic programme again or bypass a mutually exclusive focus.

One-time congress settlement; focus programmes are never granted twice.

- Reaffirm the Mobilisation Programme: Requires the Rectification verdict; Stability +2 percentage points once; No additional economic modifiers: the focus programme already supplies workforce +4%, construction +8%, civilian productivity -6%, research -3%
- Defend Enterprise Accounting: Requires the Continue the SDPE verdict; Stability -1 percentage point and Political power +35 once; No additional economic modifiers: the focus programme already supplies civilian productivity +10%, agricultural productivity +10%, tax revenue -5%
- Refer the Question to the Economic Commission: If no verdict is completed: Political power +15 once; the normal focus choice remains available; No automatic focus completion, duplicate programme or change of ruling party

At the Third PCC Congress in February 1986, the leadership began rectification, criticizing material incentives and aspects of the Soviet-inspired economic management system. It was a policy shift within one-party rule, not a return to Che Guevara or an automatic economic collapse. Source: https://www.jstor.org/stable/10.2307/45194255

### A Contraction in Soviet Trade and Supply · 1990-08 to 1990-09 onward

Only fire if actual Soviet deliveries, oil supply, or trade support to Cuba have materially fallen below the agreed scenario baseline; otherwise this contingency remains dormant.

Emergency-choice modifiers last 365 days, with a separate exposure-scaled shortage spirit only for the verified duration of disrupted supply. Renewals require an explicit new policy decision and cannot stack.

- Protect Food, Health and Essential Transport: Agricultural productivity +4%; Weekly education and healthcare expenditure +5%; Construction speed -8%; Stability -3 percentage points
- Seek Emergency Trade and Reschedule Imports: Foreign influence +4%; Resource export revenue +5%; Foreign influence defence -4%; Stability -1 percentage point

Soviet supply cuts intensified in August 1990; Fidel Castro formally declared the Special Period in September. Trade and credit disruption had begun earlier and deepened through the following years. This was not a complete Soviet cutoff on 1 January 1990 and should not impose inevitable collapse. Any resulting migration must pass through existing migration accounting. Dollar legalisation and major reforms associated with 1993 belong to later developments, not to this 1990 event. Sources: https://repositorio.cepal.org/bitstream/handle/11362/1030/4/ESLA1991v2_en.pdf ; https://ascecubadatabase.org/asce_proceedings/the-cuban-economic-crisis-of-the-1990s-and-the-external-sector/

## Fidel-era expansion: historical research

The five added PCC focuses cover the Family Code and employment supports (1975), family doctor-and-nurse teams (1984), the Biological Front/CIB/CIGB programme (1981–86), free peasant markets (1980–86) and the microbrigade revival (1986–87). The market experiment existed historically; keeping it after the rectification turn is the alternate continuation. The funded social and scientific programmes are complementary, while the two economic follow-ups inherit the existing SDPE/Rectification exclusion.

See [the dedicated research memo](FIDEL_EXPANSION_RESEARCH.md), [mechanics and reference review](FIDEL_EXPANSION_MECHANICS_REVIEW.md), and [layout review](FIDEL_EXPANSION_LAYOUT_REVIEW.md). The First PCC Congress is not a predecessor to the Family Code, which historically came first. Numerical rewards are balance proposals, not historical budget/output measurements.

## Integration contract

- Approval concept only: no live focus, idea, event, party registry or country history is changed.
- Government branches use exact ruling_party slots 4,6,19,22,3,18,1,2,0,20,5,7,13. Slot4/Fidel is the historical start. No already-ruling-party unlock focus.
- Exile governments require an actual existing-party transition through negotiated opening, elite/security rupture, or externally settled conflict. A focus does not create a domestic opposition majority.
- Programme receipts persist. Active party modifiers turn off when that subparty leaves office and reactivate on return. Physical assets, research grants and payments execute once only, outside refresh helpers.
- Shared national institutions remain unless explicitly repealed. Knowledge and healthcare do not vanish merely because a party loses office.
- Native budget tier upgrades use actual below-cap checks. At the cap show and apply a defined service-efficiency alternative, not the helper's unrelated PP fallback.
- Construction rechecks actual owned/controlled state, slots or building cap before charging; native cancel_if_invalid remains enabled. A changed target cannot consume money without delivery.
- Money costs are one-time MD Treasury units unless explicitly labelled weekly. Percentage expenditure effects modify the existing weekly native budget; no annual literal is copied into a weekly tick.
- All counterpart offers are recipient-owned, expire after 90 days, revalidate on acceptance and have explicit refusal. A completed proposal focus is never an accepted treaty receipt.
- The early harvest cannot be declared failed on 1 January. 26 July1970 resolves the campaign; 1972 island naming is a genuine dated commemorative action. Other chapter dates are historical notes, not arbitrary tree locks.
- Soviet trade contraction triggers exposure-sensitive emergency choices; there is no inevitable 1990 collapse if the player diversified. Dollar legalisation and post-1993 tourism systems are not historical 1970–90 rewards.
- OSPAAAL, MININT and JUCEPLAN have compact programmes for their registered governing slots; these are alternate institutional governments, not claims that they were independent mass parties. CTC, FMC, CDRs, Church and scientists enter as institutions. Tiny registry-only religious/monarchist/neo-fascist circles receive no national branch.

### The 1970 harvest

- The initial campaign is active on 1 January. Finish the Zafra programme modifiers expire at the 26 July review; Restore the Sectors is a lasting national reallocation.
- The May announcement is informational. At the July review remove the original campaign and any temporary Finish the Zafra programme before applying the selected 180-day settlement.
- Mobilisation or no completed harvest verdict: recovery burden = civilian industry productivity −6%, construction speed −4%, for 180 days. Rebalanced course: civilian industry productivity −3%, construction speed −2%, for 90 days. The timed July event choice is additional and explicitly listed.
- A player starting late can resolve an overdue historical harvest once. There is no permanent +12% farm mobilisation from a finished 1970 campaign.

### Ownership and the Revolutionary Offensive

- Protected Enterprises or Joint Ventures removes the original Revolutionary Offensive spirit. Its replacement is the chosen national economic programme with exactly the focus deltas; there is no second hidden reform bonus.
- Shared ownership priorities survive a government change until formally repealed. Party-specific tax/incentive programmes follow the governing subparty. Built factories and infrastructure remain national assets.

### Sugar, diversification and Soviet supply

- Default Sugar and Soviet Oil: agriculture +10%, sanction resistance −10%, foreign influence defence −10%.
- Food before Sugar only: replace it with Imported Machinery, agriculture +0%, sanction resistance −4%, foreign influence defence −5%. Light Industry only: agriculture +5%, sanction resistance −6%, foreign influence defence −6%. Both completed: agriculture +0%, sanction resistance −2%, foreign influence defence −3%. Exactly one variant is active.
- A Soviet supply shock requires an actual withdrawal of a recorded support/supply commitment or a verified contraction of bilateral fuel/trade deliveries. Calendar year 1990 and CMEA exit alone are insufficient. The counterpart must control withdrawal; no new autonomous annual subsidy is assumed.
- While the verified shortage remains: no diversification gives civilian productivity −20%, construction −15%, agriculture −8%; one of Food before Sugar/Light Industry gives −12%, −10%, −4%; both gives −6%, −5%, −2%. These replace one another and clear when deliveries recover or a substitute supply accord actually takes effect.
- The 1990 emergency choice adds only its stated 365-day adjustment. It does not add the modern Special Period idea or repeat the shock under another name.

### The embargo and diplomatic easing

- The custom embargo spirit is the fallback representation of the US restriction. If an active native US embargo or an Imperia comprehensive US economic sanction already supplies that restriction, suspend this fallback and use that system. Third-country sanctions remain separate.
- Limited accepted easing: replace the fallback with resource export revenue −10%, civilian productivity −3%; reciprocal opinion +10. Claims commission costs CUB 0.10 Treasury.
- Full accepted executive trade settlement in 1970–90: remove actual US embargo restrictions and this fallback, reciprocal opinion +20. CUB pays a total 0.25 Treasury (only a further 0.15 if the earlier 0.10 commission was paid). Restore the fallback if comprehensive restrictions are subsequently reimposed.
- MFN tariff treatment, official credits, private claims and Guantánamo require their own terms. The later 1996 statutory codification is not a retroactive Congress-only embargo gate.

### Security institutions

- The initial CDR/security institution remains a national starting constraint. A professional settlement through Socialist Constitution, Accountable Officers or Professional Intelligence replaces it with counterintelligence defence +10%, political power gain −4%, research −2%.
- A completed civilian constitutional settlement (Auténtico, Ortodoxo, Christian Democrat, Liberal, RECE charter or Alpha civic-demobilisation endpoint) replaces that institution with civilian counterintelligence defence +5% and weekly bureaucracy expenditure +3%. The institutional replacement is persistent, not a second party buff.
- An explicit later surveillance-restoration decision must replace the institution again and pay its political cost; merely changing a party does not resurrect dismantled institutions. Party programme modifiers still deactivate/reactivate with the exact current slot.

### Exile and dialogue

- The exile spirit begins at workforce −4%, stability −3%. A completed voluntary family/return agreement plus actual registered returns reduces it to workforce −2%, stability −1%. A dialogue announcement alone grants only its listed event effects.
- Historical migration totals are context, not an automatic population debit. All departures and returns pass once through the existing native/Imperia migration ledger; forced removal is not a selectable development reward.

### Budget and corruption caps

- A valid budget tier is required in availability and completion. Below cap use the native +1 tier helper. At edu_05/health_06 use one named sector-efficiency idea giving −3% weekly sector expenditure. Repeated cap rewards reuse that same idea and never stack.
- Corruption reform calls decrease_corruption only at corruption_level_02 through _10. At _01 use a single named Public Oversight idea: weekly bureaucracy expenditure −3%. Missing law category blocks enactment and requests initialization; no helper is allowed to fall through to unrelated +150 political power.
- These national service/oversight institutions remain after a government leaves. Their recurring budget obligations remain real; completed grants cannot be farmed by switching parties.

### Fidel-era social, scientific and economic programmes

- The Family Code completion records a legal reform. Its funded childcare/work-participation modifier is a governing programme; switching parties does not automatically repeal family rights. Actual repeal requires its own political decision.
- Family Doctor Teams grants a native healthcare budget tier once, after the same valid-tier and cap guards as other health reforms. The law tier persists across governments; the PCC coordination/cost modifiers follow the exact governing slot. No healthcare tax-income modifier is described as clinical care.
- The Biological Front grants a single 50% CAT_genetics research bonus and one civilian factory in State 854 after legal construction/payment checks. Both are durable national gains; the weekly research-training expenditure is part of the current PCC programme. Refresh never repeats the factory or research use.
- Peasant Markets follows continued SDPE; Revive Microbrigades follows Rectification. Their ancestors are mutually exclusive, so both economic programmes cannot stack. The 1986 congress event respects the completed verdict and never grants either new follow-up as a second bonus.
- The microbrigade infrastructure level represents Havana neighbourhood utilities/access works. Construction speed, redirected civilian output and welfare expenditure model the mobilisation programme; no apartment count or housing-stock system is invented.

### Government lifecycle and international agreements

- Each governmental programme uses the exact ruling_party slot in availability and reward. Completed receipts persist; current modifiers are rebuilt from the receipts of the current slot only.
- Government change refresh, initial load and weekly reconciliation remove inactive party dynamic modifiers and restore eligible ones. Refresh contains no Treasury, debt, construction, research, experience, law-tier or migration grant.
- CMEA member programme requires the actual admission spirit, including in the reward and subsequent refresh. Leaving suspends it; readmission restores the programme but never repeats its research grant.
- Accepted technical/cultural support runs until terminated by its diplomatic terms. An offer focus only creates a 90-day recipient-owned proposal; refusal or expiry charges nobody. Every accepted transaction has a once-only receipt and validates ownership/control/caps before charging.

## Review and limits

The structure and effects were checked separately against main MD Cuba/Russia, January 1970 country history, party registry, current modifier readers and historical research. Read `history_research.md`, `HISTORICAL_REVIEW.md`, `md_reference_profile.md`, `effect_api_audit.md`, `MECHANICS_REVIEW.md` and `LAYOUT_REVIEW.md` for source evidence and independent findings.

This directory is an approval design. The native excerpts deliberately comment out custom contract calls and dynamic programme updates. They are not a runnable tree and must never be copied into game folders as-is. Bilateral event handlers, receipts, conditional starting-spirit replacements, on-change cleanup and English effect localisation require implementation after approval. No engine or multiplayer test is claimed.

Government availability and reward guards use exact ruling subparty. Existing native government-change callbacks must invoke the Cuba refresh. Refresh recalculates only active modifiers from completed receipts. It never repeats construction, money, research or treaty payments. Run at initialization, government change and a weekly reconciliation. The party programme is removed when its slot leaves office and restored when the same slot returns. Construction and international contracts revalidate before any payment.

Historical branching uses political conditions rather than mandatory dates, except genuinely commemorative actions. Counterfactual governments require an actual negotiated, elite/security or conflict settlement; no focus manufactures domestic electoral support.

Static checks: {"errors": [], "focuses": 120, "groups": 17, "government_programmes": 13, "exclusive_pairs": 22, "prerequisite_edges": 118, "native_title_max": 143}.
