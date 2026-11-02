IMPERIA COLD WAR

# Greece 1970 replacement concept

Status: approval proposal only. No loaded runtime files changed. 100 focuses, 11 sections, 12 standing agreements, 1 military transfer, 2 territorial offers and 9 starting spirits.

## Historical premise

January 1970
Prime Minister Georgios Papadopoulos; Regent Georgios Zoitakis; King Constantine II in exile.
Domestic parties are banned. ERE, Centre Union, EDA and KKE represent historical constituencies. PAK is an exile resistance movement. ND and PASOK are founded in 1974, not lawful parties in January 1970. KKE Interior constituencies appear inside the broad-left alternative, not an invented MD party slot.
Greece remains a NATO member and a kingdom. EEC association is restricted, not membership. Withdrawal from the Council of Europe was notified in December 1969; legal membership ends in December 1970.
Strong shipping, tourism and growth coexist with regional inequality, emigration and shortages of technical expertise. No custom workforce-size penalties.
The Ioannidis takeover, the July 1974 Cyprus coup, democratization, European accession and the 1983 health-system precedent inform reachable alternatives rather than scripted inevitabilities.

All modifier amounts and package prices below are proposed game balance, not historical economic estimates. Benefits use verified native keys; recorded historical precedents justify institutions and tradeoffs. Later policies are reachable alternatives, not an automatic timeline.

## Starting national spirits

### Emergency Rule

Exceptional powers give the officer government administrative freedom while reducing political legitimacy and intellectual openness.

- Political power gain: +15%
- Stability: -10%
- Research speed: -3%

Remedy: Ends with an actual civilian handover; not merely a different cabinet label.

### Divided Officer Corps

Personal loyalties and the failed royal countercoup divide the services. Neither navy professionalism nor army political power guarantees joint command.

- Army organization: -10%
- Naval organization: -10%
- Planning speed: -10%

Remedy: A Joint Defence Staff replaces the divided command arrangement.

### Suppressed Political Life

Parties cannot compete freely, political detention continues and exceptional jurisdiction constrains public life. The formal easing of prior press censorship in late 1969 did not establish a free political system.

- Stability: -8%
- Research speed: -3%
- Political power gain: -5%

Remedy: Complete Amnesty and Open Courts, or enact the Social Contract under an actual civilian mandate.

### Civil War Inheritance

Exclusion, memories of the Civil War and conflicts over royal authority continue to divide public institutions.

- Stability: -5%
- Foreign influence defence: -5%

Remedy: An accepted parliamentary constitutional settlement or Rehabilitate the Excluded.

### Uneven Development

Rapid aggregate growth coexists with uneven regional infrastructure and less productive rural districts.

- Agricultural productivity: -8%
- Construction speed: -5%
- Office income tax yield: -5%

Remedy: Complete Water and Rural Productivity.

### Emigration and Technical Gaps

Emigration brings remittances but makes technical capacity at home harder to maintain. Education and returning expertise are essential to a broader domestic productive base.

- Research speed: -5%
- Education budget cost: +5%

Remedy: Complete Technical Skills at Home or Free and Capable Universities.

### Restricted European Association

Association continues in limited treaty form, while further political integration and new Community financing are restricted. Greece is associated with the Community, without being a member.

- Office income tax yield: -8%
- Foreign influence: -10%

Remedy: Restore European Association through democratic reform and actual member-state approval.

### Maritime and Tourism Expansion

Shipping, tourism and external earnings are real strengths of the economy. Their international exposure also limits economic autonomy.

- Dockyard productivity: +10%
- Office income tax yield: +10%
- Foreign influence defence: -5%

Remedy: A continuing structural strength with a continuing external dependence.

### 1960 Treaty of Guarantee

The 1960 settlement recognizes the independent Republic of Cyprus and the guarantee roles of Greece, Turkey and the United Kingdom. Consultation and the obligations of the settlement give each government a stake in Cypriot security.


Remedy: Retained as the treaty basis of the guarantor paths. No automatic annexation, partition or sovereign control.

## Exact focus structure and prospective effects

Coordinates are resolved HOI4 grid positions; pitch 96 x 130 px. Each prerequisite group is OR internally; groups combine with AND. Mutual exclusions are reciprocal. Every party branch remains visible. Modifier entries are signed deltas to the named programme, not replacement totals. Money below is percentage of Greek GDP unless explicitly another basis. Recurring amounts are per week.

### The Constitutional Question (8)

#### The Constitution in Abeyance

`COLDWAR_GRE_R2_constitution`. Position (4, 0). 14 days.
Predecessors: None. Excludes: None.

The regime invokes the 1968 constitution while retaining exceptional powers. A functioning administration cannot settle the unresolved question of who may govern.

- Constitutional Administration
- Political power gain: +10%
- Bureaucracy budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Entrench the Revolution

`COLDWAR_GRE_R2_entrench`. Position (2, 1). 35 days.
Predecessors: (constitution). Excludes: handover.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.

The officers retain the final political veto. Their command becomes firmer while the exclusion of civilian constituencies deepens.

- Constitutional Administration
- Political power gain: +15%
- Stability: -5%
- Army experience +25

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Negotiate a Civilian Handover

`COLDWAR_GRE_R2_handover`. Position (6, 1). 35 days.
Predecessors: (constitution). Excludes: entrench.
Requirements: The actual military government accepts a civilian transfer, or a civilian cabinet already governs. Greece is at peace.

A negotiated transfer allows a constitutional civilian cabinet to replace military rule. Kanellopoulos or Mavros can lead the transition; amnesty and free parliamentary competition must still follow. The services retain funded institutional guarantees, but no political veto.

- Form a civilian caretaker cabinet: Panagiotis Kanellopoulos or Georgios Mavros
- Negotiated Military Withdrawal (180 days)
- Army organization: -5%
- Political power gain: -10%
- Constitutional Administration
- Stability: +8%
- Remove Emergency Rule
- Political power gain: -15%
- Stability: +10%
- Research speed: +3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Retain the Exceptional Courts

`COLDWAR_GRE_R2_tribunals`. Position (2, 2). 35 days.
Predecessors: (entrench). Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.

Military jurisdiction protects the government from organized opposition. The same restrictions isolate universities and weaken the free circulation of expertise.

- Constitutional Administration
- Foreign influence defence: +15%
- Research speed: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Amnesty and Open Courts

`COLDWAR_GRE_R2_amnesty`. Position (6, 2). 35 days.
Predecessors: (handover). Excludes: None.

Political prisoners must be released and ordinary jurisdiction over political cases restored before parliamentary competition can be credible. The executive relinquishes instruments that made governing without consent easier.

- Remove Suppressed Political Life
- Stability: +8%
- Research speed: +3%
- Political power gain: +5%
- Constitutional Administration
- Political power gain: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Free Parliamentary Mandate

`COLDWAR_GRE_R2_election`. Position (6, 3). 35 days.
Predecessors: (amnesty). Excludes: None.
Requirements: Exceptional military rule has ended and legal political competition has been restored.

Legal political competition restores the distinction between a government and the state. Parties return to public life, voters choose a parliament and the cabinet must answer to it. The transition gives up the certainty of military appointment for the legitimacy of an elected mandate.

- Enable free elections
- 1 x 50% research bonus: Industry

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Parliamentary Republic

`COLDWAR_GRE_R2_republic`. Position (4, 5). 35 days.
Predecessors: (election). Excludes: constitutional_crown.

A free constitutional settlement removes the Crown as an independent center of executive authority. The change resolves one old division while alienating committed royalists.

- Constitutional Settlement
- Political power gain: +15%
- Foreign influence defence: +10%
- Stability: -3%
- Remove Civil War Inheritance
- Stability: +5%
- Foreign influence defence: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Crown Bound by Parliament

`COLDWAR_GRE_R2_constitutional_crown`. Position (8, 5). 35 days.
Predecessors: (election). Excludes: republic.

A freely accepted monarchy can offer continuity only if its powers are defined by parliament. Restraint on the government is the price of reconciling royalist institutions with elected authority.

- Constitutional Settlement
- Stability: +10%
- Naval organization: +5%
- Political power gain: -10%
- Remove Civil War Inheritance
- Stability: +5%
- Foreign influence defence: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### Growth and Development (12)

#### The Development Programme

`COLDWAR_GRE_R2_development`. Position (12, 0). 35 days.
Predecessors: None. Excludes: None.

Public coordination has supported rapid expansion, but production and infrastructure remain unevenly distributed. The development programme must turn investment into a broader productive base.

- Treasury: -1% Greek GDP once
- Development Strategy
- Construction speed: +10%
- Bureaucracy budget cost: +5%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Technical Skills at Home

`COLDWAR_GRE_R2_technical`. Position (12, 1). 35 days.
Predecessors: (development). Excludes: None.

Greece needs technicians at home as well as the remittances of workers abroad. Technical schools and recognition of returning workers' skills reduce dependence on a narrow pool of specialists.

- Treasury: -2% Greek GDP once
- Remove Emigration and Technical Gaps
- Research speed: +5%
- Education budget cost: -5%
- 2 x 50% research bonus: Industry

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Credit for the Visitor Economy

`COLDWAR_GRE_R2_visitor_credit`. Position (10, 2). 35 days.
Predecessors: (technical). Excludes: industrial_credit.

Hotels, transport services and coastal businesses earn foreign exchange quickly. Directing scarce credit toward visitors leaves less capital for industrial diversification.

- Treasury: -2% Greek GDP once
- Development Strategy
- Office income tax yield: +15%
- Civilian factory construction: -5%
- Aegean Islands: State shared building slots +1
- Aegean Islands: Office park +1

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Credit for Industry

`COLDWAR_GRE_R2_industrial_credit`. Position (14, 2). 35 days.
Predecessors: (technical). Excludes: visitor_credit.

Manufacturing offers a broader export base and less seasonal employment. Its equipment and long construction schedules tie up credit that could otherwise serve commerce and tourism.

- Treasury: -4.5% Greek GDP once
- Development Strategy
- Factory output: +15%
- Office income tax yield: -5%
- Southern Macedonia: State shared building slots +1
- Southern Macedonia: Civilian factory +1

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Island Transport and Services

`COLDWAR_GRE_R2_island_links`. Position (10, 3). 35 days.
Predecessors: (visitor_credit). Excludes: None.

Island communities need reliable links to the mainland before visitor spending can sustain local businesses. Maintaining those links remains a public obligation beyond the summer season.

- Treasury: -1.5% Greek GDP once
- Aegean Islands: State shared building slots +1
- Aegean Islands: Infrastructure +1
- Development Strategy
- Office income tax yield: +5%
- Bureaucracy budget cost: +2%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Standards and Suppliers

`COLDWAR_GRE_R2_industrial_standards`. Position (14, 3). 35 days.
Predecessors: (industrial_credit). Excludes: None.

Greek manufacturers must meet consistent standards and develop domestic suppliers. Better production discipline depends on continuing technical instruction.

- Treasury: -1% Greek GDP once
- 1 x 50% research bonus: Industry
- Development Strategy
- Production efficiency cap: +10%
- Education budget cost: +3%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Water and Rural Productivity

`COLDWAR_GRE_R2_rural_water`. Position (12, 4). 35 days.
Predecessors: (island_links OR industrial_standards). Excludes: None.

Irrigation, local roads and storage can connect agricultural districts to expanding urban markets. These works broaden the gains of growth without treating rural Greece as a reserve of departing labor.

- Treasury: -2% Greek GDP once
- Thessaly: State shared building slots +1
- Thessaly: Infrastructure +1
- Remove Uneven Development
- Agricultural productivity: +8%
- Construction speed: +5%
- Office income tax yield: +5%
- Development Strategy
- Agricultural productivity: +10%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Modernize the Cooperatives

`COLDWAR_GRE_R2_farm_cooperatives`. Position (10, 5). 35 days.
Predecessors: (rural_water). Excludes: commercial_farming.

Cooperative purchasing and processing give smaller farmers access to equipment and distribution. Public supervision also carries administrative costs and risks protecting inefficient organizations.

- Treasury: -1% Greek GDP once
- Development Strategy
- Agricultural productivity: +15%
- Bureaucracy budget cost: +5%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Competitive Farm Credit

`COLDWAR_GRE_R2_commercial_farming`. Position (14, 5). 35 days.
Predecessors: (rural_water). Excludes: farm_cooperatives.

Commercial credit rewards farms able to mechanize and sell at scale. The strongest producers gain quickly while smaller households face a harsher adjustment.

- Treasury: -1% Greek GDP once
- Development Strategy
- Agricultural productivity: +10%
- Office income tax yield: +8%
- Stability: -3%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### The Piraeus Shipyards

`COLDWAR_GRE_R2_shipyards`. Position (12, 6). 35 days.
Predecessors: (farm_cooperatives OR commercial_farming). Excludes: None.

A maritime country should retain more repair, engineering and construction work in its own ports. The shipbuilding base needs dependable public infrastructure as well as private orders.

- Treasury: -4.5% Greek GDP once
- Central Greece: State shared building slots +1
- Central Greece: Dockyard +1
- Development Strategy
- Dockyard productivity: +10%
- Bureaucracy budget cost: +2%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### Merchant Shipping Services

`COLDWAR_GRE_R2_shipping`. Position (10, 7). 35 days.
Predecessors: (shipyards). Excludes: domestic_marine_supply.

Shipping services bring earnings and expertise from a world-spanning Greek fleet. Dependence on international owners and foreign demand limits the state influence over those earnings.

- Treasury: -1% Greek GDP once
- Development Strategy
- Office income tax yield: +12%
- Foreign influence defence: -8%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

#### A Domestic Marine Supply Chain

`COLDWAR_GRE_R2_domestic_marine_supply`. Position (14, 7). 35 days.
Predecessors: (shipyards). Excludes: shipping.

Domestic equipment and maintenance suppliers can keep more value in Greek yards. Building this network costs more than relying on established international suppliers.

- Treasury: -3% Greek GDP once
- Peloponnese: State shared building slots +1
- Peloponnese: Civilian factory +1
- Development Strategy
- Dockyard output: +12%
- Office income tax yield: -4%

Historical basis: [OECD Economic Survey: Greece 1972, retrospective 1969-71 tables](https://www.oecd.org/content/dam/oecd/en/publications/reports/1972/11/oecd-economic-surveys-greece-1972_g1g16e97/eco_surveys-grc-1972-en.pdf).

### Armed Forces (12)

#### A Joint Defence Staff

`COLDWAR_GRE_R2_joint_staff`. Position (22, 0). 35 days.
Predecessors: None. Excludes: None.

Political rivalries inside the services have damaged confidence in joint command. A professional planning staff can restore coordination while enlarging the permanent military administration.

- Treasury: -1% Greek GDP once
- Remove Divided Officer Corps
- Army organization: +10%
- Naval organization: +10%
- Planning speed: +10%
- Defence Programme
- Planning speed: +15%
- Bureaucracy budget cost: +5%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Army Schools and Staff Courses

`COLDWAR_GRE_R2_army_school`. Position (18, 1). 35 days.
Predecessors: (joint_staff). Excludes: None.

A cohort of officers receives training in combined operations. A 180-day appropriation pays instructors and facilities; the completed staff education endures after the appropriation ends.

- Treasury: -1% Greek GDP once
- Weekly expense: +0.004% Greek GDP
- 1 x 25% doctrine cost reduction: Land doctrine
- Army experience +25
- Staff College Funding (180 days)

Lifetime: Only while Staff College Funding is active, for at most 180 days from its original issue. Removal or cancellation stops the expense immediately.

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### An Aegean Command

`COLDWAR_GRE_R2_aegean_command`. Position (26, 1). 35 days.
Predecessors: (joint_staff). Excludes: None.

Naval and air staffs prepare a common defence plan for the islands and sea lanes. A 180-day appropriation funds the initial coordination. The technical preparation and staff experience endure after that funding period.

- Treasury: -1% Greek GDP once
- Weekly expense: +0.006% Greek GDP
- 1 x 50% research bonus: Naval technology
- Navy experience +25
- Aegean Staff Funding (180 days)

Lifetime: Only while Aegean Staff Funding is active, for at most 180 days from its original issue. Removal or cancellation stops the expense immediately.

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Territorial Defence

`COLDWAR_GRE_R2_territorial_army`. Position (16, 2). 35 days.
Predecessors: (army_school). Excludes: professional_cadres.

Territorial formations provide a resilient framework for defending difficult ground. Their wider intake takes longer to train to a common standard.

- Treasury: -1% Greek GDP once
- Defence Programme
- Army organization: +15%
- Training time: +15%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Professional Cadres

`COLDWAR_GRE_R2_professional_cadres`. Position (20, 2). 35 days.
Predecessors: (army_school). Excludes: territorial_army.

A stronger professional cadre accelerates training and improves detailed preparation. Maintaining that cadre is more expensive than relying on a broad territorial establishment.

- Treasury: -1.5% Greek GDP once
- Weekly expense: +0.01% Greek GDP
- Defence Programme
- Army organization: +5%
- Training time: -15%
- Maximum planning: +10%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Sea Denial and Coastal Defence

`COLDWAR_GRE_R2_sea_denial`. Position (24, 2). 35 days.
Predecessors: (aegean_command). Excludes: sea_control.

Coastal defence and dispersed naval forces make hostile access to the Aegean costly. Concentration on denial leaves less capacity for expeditionary landings.

- Treasury: -1.5% Greek GDP once
- Defence Programme
- Naval organization: +15%
- Naval invasion preparation speed: -20%
- 1 x 50% research bonus: Naval technology

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### A Fleet for Sea Control

`COLDWAR_GRE_R2_sea_control`. Position (28, 2). 35 days.
Predecessors: (aegean_command). Excludes: sea_denial.

A fleet able to operate beyond the immediate coast can protect shipping and support distant forces. Its readiness and logistics consume a larger share of national resources.

- Treasury: -2% Greek GDP once
- Weekly expense: +0.015% Greek GDP
- Defence Programme
- Naval organization: +8%
- Naval speed: +10%
- Amphibious invasion attack: +10%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Army Workshops and Maintenance

`COLDWAR_GRE_R2_army_industry`. Position (18, 3). 35 days.
Predecessors: (territorial_army OR professional_cadres). Excludes: None.

Repair capacity and domestic workshops reduce the distance between an equipment order and a field formation. Their value depends on sustained technical competence, not a political procurement announcement.

- Treasury: -3% Greek GDP once
- Southern Macedonia: State shared building slots +1
- Southern Macedonia: Military factory +1
- 1 x 50% research bonus: Infantry

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Air Defence of the Aegean

`COLDWAR_GRE_R2_air_command`. Position (26, 4). 35 days.
Predecessors: (aegean_command). Excludes: None.

Control of the air is inseparable from the defence of islands and sea lanes. Air staffs must choose where a limited force can achieve the greatest effect.

- Treasury: -1.5% Greek GDP once
- Air experience +35
- 1 x 50% research bonus: Aircraft

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Concentrate on Interception

`COLDWAR_GRE_R2_interceptors`. Position (24, 5). 35 days.
Predecessors: (air_command). Excludes: close_support.

Interceptor training and aircraft development prioritize the protection of national airspace. The supporting radar and technical establishment must be maintained continuously.

- Treasury: -1% Greek GDP once
- 2 x 50% research bonus: Light aircraft
- Defence Programme
- Research speed: +3%
- Bureaucracy budget cost: +2%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Battlefield Air Support

`COLDWAR_GRE_R2_close_support`. Position (28, 5). 35 days.
Predecessors: (air_command). Excludes: interceptors.

An air arm trained closely with land and naval forces can support a rapid operational decision. This approach accepts the continuing expense of specialized coordination.

- Treasury: -1.5% Greek GDP once
- Weekly expense: +0.01% Greek GDP
- 2 x 50% research bonus: Air-to-ground weapons
- Defence Programme
- Planning speed: +20%
- Naval invasion preparation speed: +15%

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Link the Radar Stations

`COLDWAR_GRE_R2_radar`. Position (26, 6). 35 days.
Predecessors: (interceptors OR close_support). Excludes: None.

Linked reporting stations make a scattered island defence less fragmented. Radar works must be placed where Greece actually controls the land and can maintain the equipment.

- Treasury: -1.5% Greek GDP once
- Crete: State shared building slots +1
- Crete: Radar station +1
- 1 x 50% research bonus: Electronics

Historical basis: [NATO: Greece and the Alliance](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

### External Relations (11)

#### Recover Room for Diplomacy

`COLDWAR_GRE_R2_external_room`. Position (34, 0). 35 days.
Predecessors: None. Excludes: None.

Greece occupies an important strategic position but cannot assume that foreign governments will overlook its domestic settlement. Diplomatic room requires sustained attention and resources.

- Weekly expense: +0.003% Greek GDP
- External Relations
- Foreign influence: +10%
- Political power gain: -5%

Historical basis: [US-Greek relations and political reform, January 1969](https://history.state.gov/historicaldocuments/frus1969-76v29/d239).

#### American Standardization

`COLDWAR_GRE_R2_american_standard`. Position (32, 1). 35 days.
Predecessors: (external_room). Excludes: french_option.

American facilities and equipment have long shaped the Greek defence establishment. A renewed agreement trades access and dependence for training, technical support and revenue.

- If they accept: Hellenic-American Facilities and Training

Historical basis: [US-Greek relationship, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The French Defence Option

`COLDWAR_GRE_R2_french_option`. Position (36, 1). 35 days.
Predecessors: (external_room). Excludes: american_standard.

French procurement and training offer a second route to modern equipment. Diversification reduces reliance on one supplier while increasing the demands of technical support.

- If they accept: Hellenic-French Defence Diversification

Historical basis: [Dassault: Greece ordered Mirage F1 aircraft in 1974](https://www.dassault-aviation.com/en/group/press/press-kits/greece-and-the-rafale/).

#### Negotiate Aegean Procedures

`COLDWAR_GRE_R2_aegean_talks`. Position (32, 2). 35 days.
Predecessors: (american_standard OR french_option). Excludes: aegean_deterrence.

Working procedures at sea and in the air can reduce the risk of an accidental confrontation. Each government must accept restraints on how it demonstrates its claims.

- If they accept: Aegean Working Procedures

Historical basis: [NATO: alliance, Aegean tensions and the 1974 command withdrawal](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Deterrence in the Aegean

`COLDWAR_GRE_R2_aegean_deterrence`. Position (36, 2). 35 days.
Predecessors: (american_standard OR french_option). Excludes: aegean_talks.

Greece can invest in a more visible posture instead of a bilateral restraint agreement. Readiness carries economic costs and does not settle the underlying maritime disputes.

- Treasury: -1% Greek GDP once
- Weekly expense: +0.01% Greek GDP
- External Relations
- Naval organization: +8%
- Planning speed: +20%
- Office income tax yield: -5%

Historical basis: [NATO: alliance, Aegean tensions and the 1974 command withdrawal](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

#### Restore European Association

`COLDWAR_GRE_R2_association`. Position (34, 3). 35 days.
Predecessors: (aegean_talks OR aegean_deterrence). Excludes: None.
Requirements: Representative institutions, legal political competition and all current EC member governments approval.

The association signed in 1961 survived in restricted form after the coup, but its political and financial development stalled. Restoration requires a credible democratic settlement and agreement from the Community governments.

- If they accept: Restored European Association

Historical basis: [European Parliament: association, suspension and Greek accession](https://www.europarl.europa.eu/RegData/etudes/BRIE/2021/679064/EPRS_BRI%282021%29679064_EN.pdf).

#### Apply for Community Membership

`COLDWAR_GRE_R2_accession`. Position (34, 4). 35 days.
Predecessors: (association). Excludes: None.
Requirements: European association is active. Greece meets native membership conditions. Every current Community member consents.

Membership offers Greek producers wider markets and gives Greece a voice in common institutions. Accession also binds the government to shared rules and continuing financial obligations. Admission depends on representative government and the agreement of the current members.

- If they accept: Greek Community Accession

Historical basis: [European Parliament: association, suspension and Greek accession](https://www.europarl.europa.eu/RegData/etudes/BRIE/2021/679064/EPRS_BRI%282021%29679064_EN.pdf).

#### A Balkan Transit Understanding

`COLDWAR_GRE_R2_yugoslav_corridor`. Position (30, 5). 35 days.
Predecessors: (external_room). Excludes: None.

Transit through Yugoslavia links Greek ports with markets beyond the northern frontier. Reliable infrastructure benefits both sides but requires each government to commit to practical cooperation.

- If they accept: Greek-Yugoslav Transit Compact

Historical basis: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

#### A Northern Commercial Opening

`COLDWAR_GRE_R2_bulgarian_trade`. Position (38, 5). 35 days.
Predecessors: (external_room). Excludes: None.

The disappearance of Bulgarian territorial claims created space for more ordinary relations. Commercial cooperation can broaden trade without pretending that the two alliance systems have merged.

- If they accept: Greek-Bulgarian Commercial Protocol

Historical basis: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

#### British Guarantor Liaison

`COLDWAR_GRE_R2_british_guarantee`. Position (32, 6). 35 days.
Predecessors: (yugoslav_corridor). Excludes: None.

Britain remains a guarantor of Cyprus and holds sovereign base areas on the island. Coordination can strengthen crisis communications without granting Greece control of British forces or bases.

- If they accept: Guarantor Naval Communications

Historical basis: [UN Treaty Series 382: the 1960 settlement](https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf).

#### A German Technical Exchange

`COLDWAR_GRE_R2_skills_return`. Position (36, 6). 35 days.
Predecessors: (bulgarian_trade). Excludes: None.

The labor relationship with West Germany can support technical instruction and the return of skills to Greece. A funded exchange gives Greek institutions access to expertise and gives German industry a reliable partner, while requiring sustained education spending.

- If they accept: Greek-German Technical Exchange

Historical basis: [German Foreign Office: the 1960 recruitment relationship](https://www.auswaertiges-amt.de/de/newsroom/100430-stm-h-festakt-d-grc-223588).

### Cyprus and the Guarantors (17)

#### Officers on Cyprus

`COLDWAR_GRE_CYP_R2_gre_officers`. Position (44, 0). 35 days.
Predecessors: None. Excludes: None.
Requirements: Greece and Cyprus exist; an actual Greek officer footprint exists.

The Greek mission has institutional influence inside the Cypriot National Guard. Professional cooperation and political intervention are different uses of the same presence.

- Army organization +2%
- Training time -5%

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Honour the Republic

`COLDWAR_GRE_CYP_R2_gre_treaty`. Position (42, 1). 35 days.
Predecessors: (gre_officers). Excludes: gre_network.
Requirements: No war with Cyprus.

Respect for the Republic protects a cooperative Greek position without attempting to command Cypriot political life. Influence is exercised through accepted institutions rather than a clandestine veto.

- Foreign influence defence +5%
- Stability +2%
- Officer penetration in Cyprus -10

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### The Officer Network

`COLDWAR_GRE_CYP_R2_gre_network`. Position (46, 1). 35 days.
Predecessors: (gre_officers). Excludes: gre_treaty.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Requirements: Greece is ruled by the actual military-junta party. Greek officer footprint remains. Once per campaign.

An officer network offers leverage over the government in Nicosia. Supporting it spends Greek political capital and creates a crisis which the other guarantors can answer.

- Political power -50
- Treasury -0.75% of current Greek GDP
- Officer penetration in Cyprus +20
- Stability -2%

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### A Guarantor Settlement

`COLDWAR_GRE_CYP_R2_gre_consult`. Position (40, 2). 35 days.
Predecessors: (gre_treaty). Excludes: None.
Requirements: An actual constitutional crisis exists.

The guarantors receive a real request for consultation. Neither Turkey nor Britain is assumed to agree with the Greek government merely because Athens completed a focus.

- Greece, Turkey and Britain receive Guarantor Consultations
- Political power +50

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Withdraw the Network

`COLDWAR_GRE_CYP_R2_gre_withdraw`. Position (44, 3). 35 days.
Predecessors: (gre_network). Excludes: gre_coup.
Requirements: The coup has not launched.

Withdrawing support for the clandestine network reduces Greek leverage but gives the Republic room to restore confidence. This choice is available before a coup attempt is launched.

- Officer penetration in Cyprus -20
- Stability +3%
- If Greek staff preparation is active: Cyprus officer penetration -10; remove Forward Operational Planning

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Overthrow Makarios

`COLDWAR_GRE_CYP_R2_gre_coup`. Position (46, 3). 14 days.
Predecessors: (gre_network). Excludes: gre_withdraw.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Requirements: Actual Greek junta remains in power. Officer penetration at least 60. Officer footprint exists. Cyprus remains independent and at peace with Greece. Once per campaign.

A coup can replace the Cypriot government if the officer network overcomes its prepared defence. Success creates a short strategic opening, not Greek ownership or a guaranteed victory over Turkey.

- Political power -100
- Treasury -1.5% of current Greek GDP
- Cyprus receives Coup Warning
- If successful: Sampson becomes the coup-government leader

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### The Turkish Landing

`COLDWAR_GRE_CYP_R2_gre_response`. Position (44, 7). 7 days.
Predecessors: None. Excludes: None.
Requirements: An actual Turkey-Cyprus war from this crisis is active. Greece and Cyprus are independent. Greece is not already fighting Cyprus.

An actual war between Turkey and the Republic of Cyprus confronts Athens with a distinct choice. Limited aid and direct participation offer different benefits and dangers.

- Political power +25
- Cyprus receives Greek Assistance Consultations

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Volunteers for Cyprus

`COLDWAR_GRE_CYP_R2_gre_volunteers`. Position (42, 8). 7 days.
Predecessors: (gre_response). Excludes: gre_escalate.
Requirements: Turkey is at war with Cyprus. Greece is not at war with either country. Cyprus consents through the real volunteer diplomatic action. Native volunteer and diplomatic-action rules still apply.

A volunteer mission lets Greece support the Republic without committing the entire armed forces. Athens supplies trained formations and staff while Nicosia authorizes their deployment. Limited numbers and continuing funding constrain how much aid can reach the island.

- Political power -50
- Expense +0.02% of Greek GDP per week while the mission remains active
- If Cyprus accepts:
- Cyprus Volunteer Mission (while the Cyprus mission remains eligible)
- Volunteer division limit +2
- Minimum army size for volunteers -100%
- World tension requirement for volunteers -100%
- Political power gain -5%
- Cyprus: accepted Greek volunteer deployment
- NATO membership unchanged

Lifetime: Only while the actual volunteer mission exists and real deployment remains active. Removing the mission stops this expense.

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Fight Beside Cyprus

`COLDWAR_GRE_CYP_R2_gre_escalate`. Position (46, 8). 7 days.
Predecessors: (gre_response). Excludes: gre_volunteers.
Requirements: The Turkey-Cyprus war is active. Greece is not already at war with Turkey or Cyprus. Entry must place Greece alongside Cyprus. The temporary NATO exit and return are disclosed to both countries before entry.

Greece enters the war as a full belligerent on the Cypriot side and commits its army, air force and navy against Turkey. A joint expeditionary command rewards decisive intervention, while concentrated readiness reduces commercial earnings and requires additional funding. Both countries leave NATO before Greek entry. Former members return once Greek-Turkish and Cypriot-Turkish hostilities have ended.

- Political power -100
- Treasury -1.5% of current Greek GDP
- Greece: Leave NATO
- Turkey: Leave NATO
- Greece: remove NATO Membership
- Greece: Daily Pro-Western Support -0.02
- Greece: Defensive war stability -3%
- Greece: War support -2%
- Turkey: remove NATO Membership
- Turkey: Daily Pro-Western Support -0.02
- Turkey: Defensive war stability -3%
- Turkey: War support -2%
- Greece and Turkey leave NATO technology sharing and mutual military access
- Other NATO members: opinion of Greece -20
- Other NATO members: opinion of Turkey -20
- Greece joins Cyprus in the war against Turkey
- After Greece-Turkey and Cyprus-Turkey peace: Greece returns to NATO
- After Greece-Turkey and Cyprus-Turkey peace: Turkey returns to NATO
- After related peace, Greece: Daily Pro-Western Support +0.02
- After related peace, Greece: Defensive war stability +3%
- After related peace, Greece: War support +2%
- After related peace, Turkey: Daily Pro-Western Support +0.02
- After related peace, Turkey: Defensive war stability +3%
- After related peace, Turkey: War support +2%
- After related peace: both return to NATO technology sharing and mutual military access
- Upon Greek entry on the Cypriot side
- Weekly expense: +0.05% Greek GDP
- Aegean Expeditionary Command (180 days)
- Army organization: +10%
- Naval organization: +10%
- Planning speed: +25%
- Maximum planning: +15%
- Amphibious invasion attack: +20%
- Naval invasion preparation speed: +30%
- Office income tax yield: -10%

Completion guard: Grant the new expeditionary package only after existing CYP_R2 entry succeeded, Greece is actually at war with Turkey on Cyprus side, and the unique direct-entry receipt exists. Once per crisis; no reapplication or renewed duration. Do not call the Greek government or NATO helpers from a free reward preview.

Lifetime: The expeditionary charge and spirit last until the first of 180 days or the end of Greek-Turkish hostilities in this intervention. NATO separation lasts for the whole related war, even after this combat package expires.

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Civilian Ties with Cyprus

`COLDWAR_GRE_R2_island_trade`. Position (42, 3). 35 days.
Predecessors: (gre_treaty). Excludes: None.

Civilian trade and technical cooperation give Greece an enduring stake in a stable Republic. Cyprus receives the actual terms and may accept or refuse them.

- If they accept: Hellenic-Cypriot Civilian Cooperation

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### Prepare the Officer Network

`COLDWAR_GRE_R2_staff_network`. Position (48, 2). 35 days.
Predecessors: (gre_network). Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Requirements: The Greek network and officer footprint are active. No coup has yet been launched. The preparation receipt has not previously been issued.

A prepared network strengthens the coup attempt for 180 days. Withdrawing support also withdraws this preparation. Cypriot safeguards can still defeat the attempt.

- Treasury: -1.5% Greek GDP once
- Weekly expense: +0.01% Greek GDP
- Cyprus officer penetration +10
- Forward Operational Planning (180 days)
- Planning speed: +20%
- Office income tax yield: -5%

Lifecycle: The extra +10 penetration lasts at most 180 days. Withdraw the Network also removes this separate +10 receipt, in addition to its existing -20, and removes Forward Operational Planning. Crisis cancellation does the same. Successful resolution consumes the receipt so no later double subtraction occurs. Departure of the actual Greek junta also cancels the preparation through the party-change hook.

Lifetime: Only while Forward Operational Planning is active, for at most 180 days from its original issue. Removal or cancellation stops the expense immediately.

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### The Operational Initiative

`COLDWAR_GRE_R2_operational_initiative`. Position (48, 5). 35 days.
Predecessors: (gre_coup). Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Requirements: The actual coup succeeded, the coup government remains in power in Cyprus, and the two countries are at peace. Once only.

A successful coup briefly gives the Greek command greater freedom to prepare its next move. The advantage expires, while diplomatic exposure and the cost of readiness make delay expensive.

- Weekly expense: +0.03% Greek GDP
- Operational Initiative in Cyprus (180 days)
- Planning speed: +25%
- Maximum planning: +10%
- Naval invasion preparation speed: +15%
- Office income tax yield: -10%
- Foreign influence defence: -10%
- 1 x 50% doctrine cost reduction: Land doctrine

Lifetime: Only while Operational Initiative in Cyprus is active, for at most 180 days from its original issue. Removal or cancellation stops the expense immediately.

Historical basis: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

#### An Agreed Guarantor Settlement

`COLDWAR_GRE_R2_guarantee_settlement`. Position (40, 4). 35 days.
Predecessors: (gre_consult). Excludes: None.
Requirements: The Cypriot constitutional government is in office. Greece, Turkey, Britain and Cyprus must accept the security settlement.

A negotiated security settlement offers a durable alternative to a short military opening. It preserves Cypriot sovereignty and requires all four governments to accept their obligations.

- If they accept: Cypriot Security Settlement

Historical basis: [UN Treaty Series 382: the 1960 settlement](https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf).

#### Reinforce the National Guard

`COLDWAR_GRE_R2_reinforce_guard`. Position (40, 0). 7 days.
Predecessors: None. Excludes: None.
Requirements: Cyprus is independent and consents. Greece has the complete personnel and equipment reserve. Cyprus owns and controls a valid deployment location. Greece and Cyprus are at peace and impose no embargo or sanctions on each other.

Greek personnel and arms can reinforce the Cypriot National Guard before a landing decides the crisis. Two formed light infantry divisions pass into Cypriot command as soon as the Republic accepts. Greece gives up the men and weapons from its own reserves. The contribution supports the island while leaving Athens free to choose limited aid or full military intervention later.

- If they accept: Greek Reinforcements for Cyprus

Historical basis: [FRUS: Greek personnel and Cypriot National Guard, September 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d152).

#### Proclaim Full Enosis

`COLDWAR_GRE_R2_enosis_full`. Position (46, 6). 35 days.
Predecessors: (operational_initiative). Excludes: enosis_compromise.
Requirements: The independent Cypriot coup government remains in office and holds both island states. Cyprus receives the union demand. Peaceful annexation requires Cypriot acceptance and resolution of the Turkish reaction.

The coup can become the opening for Enosis itself. A union ratified in Athens and Nicosia brings Cypriot territory, ports, airfields and armed forces into Greece. The Turkish Cypriot question and opposition from Ankara make this the most ambitious and exposed course. An explicit Cypriot rejection instead gives Athens an annexation war goal. Until a civil settlement takes root, Greece must carry the cost of governing a divided society.

- If they accept: Full Enosis

Historical basis: [FRUS: Acheson union and security proposals, July 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d85).

#### Negotiate Southern Enosis

`COLDWAR_GRE_R2_enosis_compromise`. Position (50, 6). 35 days.
Predecessors: (operational_initiative). Excludes: enosis_full.
Requirements: A real territorial partition has already been settled. The independent Cypriot coup government holds only the south, while Turkey or Northern Cyprus holds the north.

A government unable to unite the island may instead negotiate union of the south with Greece. Recognizing the northern settlement gives Ankara a concrete concession and reduces the burden on Athens. Greece obtains Nicosia and the remaining Cypriot institutions while surrendering the full-island objective. An explicit refusal by Nicosia allows Athens to pursue the southern claim by force. The British sovereign bases lie outside the bargain.

- If they accept: A Negotiated Southern Union

Historical basis: [FRUS: Acheson union and security proposals, July 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d85).

#### A Civil Settlement for Cyprus

`COLDWAR_GRE_R2_cypriot_settlement`. Position (48, 7). 35 days.
Predecessors: (enosis_full OR enosis_compromise). Excludes: None.
Requirements: The selected union or recorded postwar incorporation has actually taken effect at least 730 days ago. Greece owns and controls every transferred state, compliance is at least 70 in each, Greece and Turkey are at peace, and the binding regional representation/minority-rights charter will be enacted by this settlement.

A flag change cannot settle the Cypriot question. Regional representation, enforceable minority rights and a funded civil administration must turn the union into a durable constitutional arrangement. Established consent and compliance permit full integration, while local institutions remain a continuing obligation of the Greek state.

- After full Enosis
- Political power -100
- Treasury: -2% Greek GDP
- Remove Unsettled Enosis
- War support: -5%
- Stability: +10%
- Bureaucracy budget cost: -10%
- Office income tax yield: +8%
- Foreign influence defence: +10%
- Weekly expense: -0.03% Greek GDP
- Greek core: Nicosia and southern Cyprus
- Greek core: Famagusta and northern Cyprus
- After southern Enosis
- Political power -100
- Treasury: -1% Greek GDP
- Remove Southern Union Administration
- Stability: +5%
- Bureaucracy budget cost: -5%
- Office income tax yield: +4%
- Foreign influence defence: +5%
- Weekly expense: -0.015% Greek GDP
- Greek core: Nicosia and southern Cyprus
- Cypriot Regional Representation
- Stability: +5%
- Naval organization: +5%
- Office income tax yield: +5%
- Bureaucracy budget cost: +3%
- Political power gain: -5%
- Weekly expense: +0.004% Greek GDP

Historical basis: [FRUS: Acheson union and security proposals, July 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d85).

### The Military Government (9)

#### The Officer Compact

`COLDWAR_GRE_R2_officer_compact`. Position (4, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.

The dictatorship rests on an officer coalition rather than an ordinary governing party. Preserving that coalition strengthens command but keeps the state dependent on military arbitration.

- Military Government Programme
- Army organization: +8%
- Political power gain: +10%
- Research speed: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Papadopoulos and the Cabinet

`COLDWAR_GRE_R2_papadopoulos`. Position (2, 12). 35 days.
Predecessors: (officer_compact). Excludes: security_directorate.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Georgios Papadopoulos.

Papadopoulos concentrates political authority around his cabinet and the development administration. Economic coordination offers a positive programme, while patronage makes that apparatus costly.

- Military Government Programme
- Construction speed: +10%
- Bureaucracy budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The Security Directorate

`COLDWAR_GRE_R2_security_directorate`. Position (6, 12). 35 days.
Predecessors: (officer_compact). Excludes: papadopoulos.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Requirements: The hardliners have secured control of the military government. This is an alternative leadership struggle, not the January 1970 starting leader.

Ioannidis and the security apparatus reject a civilian political opening. Their ascent must be a real change of leadership, with the diplomatic exposure that a harder dictatorship entails.

- Dimitrios Ioannidis takes power
- Military Government Programme
- Foreign influence defence: +15%
- Office income tax yield: -8%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Managed Political Opening

`COLDWAR_GRE_R2_managed_opening`. Position (0, 13). 35 days.
Predecessors: (papadopoulos). Excludes: military_technocrats.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Georgios Papadopoulos.

A controlled opening seeks expertise and international credibility without immediately surrendering the regime. Every concession also loosens the instruments of personal command.

- Military Government Programme
- Research speed: +8%
- Foreign influence: +10%
- Political power gain: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Military Technocrats

`COLDWAR_GRE_R2_military_technocrats`. Position (4, 13). 35 days.
Predecessors: (papadopoulos). Excludes: managed_opening.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Georgios Papadopoulos.

The cabinet can instead make development the substitute for political participation. Industrial expertise grows inside an administration whose military sponsors retain the final veto.

- Treasury: -3% Greek GDP once
- Central Greece: State shared building slots +1
- Central Greece: Civilian factory +1
- Military Government Programme
- Production efficiency growth: +15%
- Education budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Promotion Through Loyalty

`COLDWAR_GRE_R2_loyal_command`. Position (6, 14). 35 days.
Predecessors: (security_directorate). Excludes: service_council.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Dimitrios Ioannidis.
Requirements: Dimitrios Ioannidis actually controls the government.

A loyal army command is less likely to challenge the security leadership. The price is renewed distrust from naval officers and other institutions excluded from promotion.

- Military Government Programme
- Army organization: +10%
- Naval organization: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Bargain with the Services

`COLDWAR_GRE_R2_service_council`. Position (8, 14). 35 days.
Predecessors: (security_directorate). Excludes: loyal_command.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Dimitrios Ioannidis.
Requirements: Dimitrios Ioannidis actually controls the government.

An inter-service settlement gives naval professionalism room to recover. The army security network must accept that it cannot monopolize every appointment.

- Military Government Programme
- Naval organization: +12%
- Army organization: -5%
- Navy experience +25

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Ministries Under Tutelage

`COLDWAR_GRE_R2_civil_ministries`. Position (2, 15). 35 days.
Predecessors: (managed_opening OR military_technocrats). Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Georgios Papadopoulos.

Civilian specialists can administer complex programmes without holding sovereign political authority. Their inclusion makes the state more capable, not yet representative.

- Treasury: -2% Greek GDP once
- 2 x 50% research bonus: Industry
- Military Government Programme
- Bureaucracy budget cost: +3%
- Stability: +8%
- Research speed: +3%
- Political power gain: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The Security Establishment

`COLDWAR_GRE_R2_security_budget`. Position (8, 16). 35 days.
Predecessors: (loyal_command OR service_council). Excludes: None.
Party requirement: Military Government of 21 April via `nationalist_military_junta_are_in_power = yes`. Dated native party names apply.
Leader requirement: Dimitrios Ioannidis.
Requirements: Dimitrios Ioannidis actually controls the government.

A permanent security establishment offers the leadership a stronger instrument for ambitious foreign policy. It also absorbs resources and increases the economic cost of political isolation.

- Treasury: -1% Greek GDP once
- Weekly expense: +0.01% Greek GDP
- Military Government Programme
- Maximum planning: +15%
- Office income tax yield: -5%
- Stability: +8%
- Research speed: +3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### The Conservative Right (8)

#### The Conservative Mandate

`COLDWAR_GRE_R2_conservative_mandate`. Position (12, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

The conservative tradition must prove that civilian authority can deliver stability without a military veto. Economic confidence and institutional credibility become the basis of its mandate.

- Conservative Reconstruction
- Foreign influence defence: +10%
- Office income tax yield: +8%
- Bureaucracy budget cost: +3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Call Karamanlis Home

`COLDWAR_GRE_R2_karamanlis`. Position (10, 12). 35 days.
Predecessors: (conservative_mandate). Excludes: kanellopoulos.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

Karamanlis offers international standing and an established conservative constituency. His return also challenges politicians who kept the party tradition alive during exile.

- Konstantinos Karamanlis becomes Prime Minister
- Conservative Reconstruction
- Foreign influence: +15%
- Political power gain: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The Kanellopoulos Tradition

`COLDWAR_GRE_R2_kanellopoulos`. Position (14, 12). 35 days.
Predecessors: (conservative_mandate). Excludes: karamanlis.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

A constitutional conservative leadership can build on Kanellopoulos and the pre-coup parliamentary tradition. Its reassuring continuity also leaves less room for a decisive break with older institutions.

- Conservative Reconstruction
- Stability: +8%
- Army organization: +5%
- Research speed: -3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Restore European Credit

`COLDWAR_GRE_R2_european_credit`. Position (10, 13). 35 days.
Predecessors: (karamanlis). Excludes: None.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

European confidence rests on political credibility and concrete reforms. The conservative government prepares the economy for a negotiated relationship rather than treating admission as a unilateral right.

- Treasury: -1% Greek GDP once
- 2 x 50% research bonus: Industry
- Conservative Reconstruction
- Bureaucracy budget cost: +3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Constitutional Conservatism

`COLDWAR_GRE_R2_constitutional_right`. Position (14, 13). 35 days.
Predecessors: (kanellopoulos). Excludes: None.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

Conservative authority is rooted in law, parliament and a disciplined administration. The same formal safeguards slow decisions that an authoritarian cabinet could simply impose.

- Conservative Reconstruction
- Political power gain: +10%
- Foreign influence defence: +10%
- Bureaucracy budget cost: +3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Competitive Greek Enterprise

`COLDWAR_GRE_R2_enterprise`. Position (12, 14). 35 days.
Predecessors: (european_credit OR constitutional_right). Excludes: None.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

Competitive firms need productive investment rather than permanent protection from change. A stronger manufacturing base gives the civilian right a tangible economic programme.

- Treasury: -3% Greek GDP once
- Southern Macedonia: State shared building slots +1
- Southern Macedonia: Civilian factory +1
- Conservative Reconstruction
- Production efficiency cap: +10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Tax Compliance

`COLDWAR_GRE_R2_tax_compliance`. Position (10, 15). 35 days.
Predecessors: (enterprise). Excludes: productive_credit.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

Reliable tax collection strengthens public finances without relying on emergency levies. The bureaucracy needed to enforce the rules must itself be funded.

- Treasury: -1% Greek GDP once
- Conservative Reconstruction
- Office income tax yield: +12%
- Bureaucracy budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Productive Investment

`COLDWAR_GRE_R2_productive_credit`. Position (14, 15). 35 days.
Predecessors: (enterprise). Excludes: tax_compliance.
Party requirement: National Radical Union via `western_conservatism_are_in_power = yes`. Dated native party names apply.

Preferential credit can accelerate investment in productive firms. Its benefits arrive before the state recovers the revenue it has forgone.

- Treasury: -2% Greek GDP once
- Conservative Reconstruction
- Civilian factory construction: +18%
- Office income tax yield: -6%
- 1 x 50% research bonus: Industry

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### The Liberal Centre (5)

#### Rebuild the Liberal Centre

`COLDWAR_GRE_R2_liberal_mandate`. Position (20, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: Centre Union via `western_liberals_are_in_power = yes`. Dated native party names apply.

The Centre Union tradition joins parliamentary legitimacy with administrative reform. Rebuilding that coalition requires institutions able to mediate its many constituencies.

- Liberal Reconstruction
- Stability: +5%
- Foreign influence defence: +10%
- Bureaucracy budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Professional Civil Service

`COLDWAR_GRE_R2_professional_service`. Position (20, 12). 35 days.
Predecessors: (liberal_mandate). Excludes: None.
Party requirement: Centre Union via `western_liberals_are_in_power = yes`. Dated native party names apply.

Professional recruitment and reliable public records reduce the role of personal patronage. Ministers lose some discretion as expertise and procedure gain authority.

- Treasury: -1.5% Greek GDP once
- 2 x 50% research bonus: Industry
- Liberal Reconstruction
- Research speed: +5%
- Political power gain: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Parliament Before Palace

`COLDWAR_GRE_R2_parliament_first`. Position (18, 13). 35 days.
Predecessors: (professional_service). Excludes: liberal_compromise.
Party requirement: Centre Union via `western_liberals_are_in_power = yes`. Dated native party names apply.

Parliamentary supremacy promises a clear answer to the conflicts of the 1960s. It also forces a confrontation with constituencies attached to an independent royal role.

- Liberal Reconstruction
- Political power gain: +15%
- Foreign influence defence: +10%
- Stability: -3%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Constitutional Compromise

`COLDWAR_GRE_R2_liberal_compromise`. Position (22, 13). 35 days.
Predecessors: (professional_service). Excludes: parliament_first.
Party requirement: Centre Union via `western_liberals_are_in_power = yes`. Dated native party names apply.

A broad settlement can reassure the services and constitutional conservatives. Its breadth limits the freedom of the government that must uphold it.

- Liberal Reconstruction
- Stability: +10%
- Army organization: +5%
- Political power gain: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Free and Capable Universities

`COLDWAR_GRE_R2_universities`. Position (20, 14). 35 days.
Predecessors: (parliament_first OR liberal_compromise). Excludes: None.
Party requirement: Centre Union via `western_liberals_are_in_power = yes`. Dated native party names apply.

Free universities and provincial infrastructure must carry expertise beyond Athens. Funding local connections and capable institutions can narrow the technical gap while giving regional communities a stake in parliamentary government. The education budget must sustain that commitment.

- Treasury: -3.5% Greek GDP once
- Remove Emigration and Technical Gaps
- Research speed: +5%
- Education budget cost: -5%
- Thessaly: State shared building slots +1
- Thessaly: Infrastructure +1
- Liberal Reconstruction
- Research speed: +8%
- Education budget cost: +10%
- Agricultural productivity: +8%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### National and Social Change (7)

#### National and Social Change

`COLDWAR_GRE_R2_national_change`. Position (28, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

The Papandreou movement connects social reform with independence from external tutelage. Its programme deliberately challenges established owners and foreign partners.

- National and Social Programme
- Foreign influence defence: +15%
- Stability: +5%
- Office income tax yield: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Social Contract

`COLDWAR_GRE_R2_social_contract`. Position (28, 12). 35 days.
Predecessors: (national_change). Excludes: None.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

Labor and previously excluded constituencies gain a legal voice and representation in public administration. Technical instruction helps translate participation into productive reform. The government accepts the cost of consultation and a larger administration in return for a broader social mandate.

- Treasury: -2.5% Greek GDP once
- Remove Suppressed Political Life
- Stability: +8%
- Research speed: +3%
- Political power gain: +5%
- 1 x 50% research bonus: Industry
- National and Social Programme
- Stability: +8%
- Bureaucracy budget cost: +10%
- Political power gain: +10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Public Control of Credit

`COLDWAR_GRE_R2_public_credit`. Position (26, 13). 35 days.
Predecessors: (social_contract). Excludes: negotiated_development.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

Public control directs credit toward sectors the government considers strategic. It can expand industrial output while reducing private financial earnings and increasing administrative exposure.

- Treasury: -6% Greek GDP once
- Central Greece: State shared building slots +1
- Central Greece: Civilian factory +1
- National and Social Programme
- Factory output: +15%
- Office income tax yield: -10%
- Bureaucracy budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Development Compact

`COLDWAR_GRE_R2_negotiated_development`. Position (30, 13). 35 days.
Predecessors: (social_contract). Excludes: public_credit.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

A negotiated compact draws investment from private enterprise while securing public commitments. The state gains a wider economic coalition but accepts continued dependence on its partners.

- Treasury: -3% Greek GDP once
- Southern Macedonia: State shared building slots +1
- Southern Macedonia: Office park +1
- National and Social Programme
- Civilian factory construction: +15%
- Office income tax yield: +8%
- Foreign influence defence: -8%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A National Health Service

`COLDWAR_GRE_R2_national_health`. Position (28, 14). 35 days.
Predecessors: (public_credit OR negotiated_development). Excludes: None.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

A national health service makes access to care a public responsibility rather than an accident of locality or income. The resulting security and productive gains require a larger recurring health budget.

- Treasury: -6% Greek GDP once
- National and Social Programme
- Stability: +8%
- Factory output: +5%
- Health budget cost: +15%

Historical basis: [Greek electronic health record: the 1983 National Health System precedent](https://www.ehealthrecord.gov.gr/first-degree-health-care).

#### An Independent Foreign Policy

`COLDWAR_GRE_R2_independent_diplomacy`. Position (26, 15). 35 days.
Predecessors: (national_health). Excludes: western_bargain.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

A more independent policy reduces the influence of established patrons without assuming that alliance membership must vanish. Greater autonomy can restrict access to some external expertise.

- National and Social Programme
- Foreign influence defence: +15%
- Naval organization: +5%
- Research speed: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The Western Bargain

`COLDWAR_GRE_R2_western_bargain`. Position (30, 15). 35 days.
Predecessors: (national_health). Excludes: independent_diplomacy.
Party requirement: Panhellenic Liberation Movement via `western_social_democrats_are_in_power = yes`. Dated native party names apply.

The government can instead use its social mandate to seek better terms within the Western relationship. Access to capital and technology comes with continued external influence.

- National and Social Programme
- Research speed: +8%
- Office income tax yield: +5%
- Foreign influence defence: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### The Communist Left (6)

#### The Left in Government

`COLDWAR_GRE_R2_left_mandate`. Position (36, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

A legal communist government must translate an underground tradition into public institutions. Industrial planning and research take precedence over established commercial interests.

- Left Government Programme
- Factory output: +8%
- Research speed: +5%
- Office income tax yield: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Rehabilitate the Excluded

`COLDWAR_GRE_R2_civil_war_families`. Position (36, 12). 35 days.
Predecessors: (left_mandate). Excludes: None.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

Rehabilitation addresses exclusions that outlasted the fighting itself. The settlement strengthens civic belonging while restricting the partisan use of the state.

- Remove Civil War Inheritance
- Stability: +5%
- Foreign influence defence: +5%
- Left Government Programme
- Stability: +8%
- Political power gain: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### An Orthodox Planning Line

`COLDWAR_GRE_R2_orthodox_plan`. Position (34, 13). 35 days.
Predecessors: (civil_war_families). Excludes: left_front.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

A more orthodox line concentrates authority over industrial priorities. It delivers a stronger production programme at the expense of commercial flexibility.

- Treasury: -4.5% Greek GDP once
- Left Government Programme
- Factory output: +15%
- Dockyard productivity: +5%
- Office income tax yield: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Broad Democratic Left Front

`COLDWAR_GRE_R2_left_front`. Position (38, 13). 35 days.
Predecessors: (civil_war_families). Excludes: orthodox_plan.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

Cooperation with the non-orthodox left, including KKE Interior constituencies, broadens the political base. Pluralism brings expertise and legitimacy while limiting the governing party's freedom of command.

- Left Government Programme
- Research speed: +10%
- Stability: +8%
- Political power gain: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Industrial Research Institutes

`COLDWAR_GRE_R2_research_institutes`. Position (36, 14). 35 days.
Predecessors: (orthodox_plan OR left_front). Excludes: None.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

Applied research can connect the planned industrial base with sustained technical progress. Institutes need stable funding and genuine professional competence.

- Treasury: -2% Greek GDP once
- 2 x 50% research bonus: Industry
- Left Government Programme
- Education budget cost: +5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Eastern Industrial Terms

`COLDWAR_GRE_R2_eastern_terms`. Position (36, 15). 35 days.
Predecessors: (research_institutes). Excludes: None.
Party requirement: Communist Party of Greece via `emerging_communist_state_are_in_power = yes`. Dated native party names apply.

An industrial agreement with the Soviet Union gives Greece access to technical training outside its usual Western channels. The partnership strengthens factory production while exposing domestic policy to another external patron.

- If they accept: Eastern Industrial Cooperation

Historical basis: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

### The Crown (5)

#### The Crown and the Nation

`COLDWAR_GRE_R2_royal_mandate`. Position (44, 11). 35 days.
Predecessors: None. Excludes: None.
Party requirement: Royalists via `nationalist_monarchists_are_in_power = yes`. Dated native party names apply.

Royalists claim a source of legitimacy above ordinary party competition. That claim can rally supporters while reviving arguments over the Crown's foreign connections.

- Royal Constitutional Programme
- Political power gain: +10%
- Army organization: +5%
- Foreign influence defence: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### The Return of Constantine

`COLDWAR_GRE_R2_constantine`. Position (44, 12). 35 days.
Predecessors: (royal_mandate). Excludes: None.
Party requirement: Royalists via `nationalist_monarchists_are_in_power = yes`. Dated native party names apply.
Requirements: A publicly accepted return of the King from exile; a restoration settlement is additionally required only if the monarchy has actually been abolished.

Constantine returns to exercise his constitutional role in the existing kingdom, or through an agreed restoration if the monarchy has since been abolished. The invitation must define his authority rather than pretend the failed countercoup never happened.

- Constantine II returns from exile
- Royal Constitutional Programme
- Stability: +5%
- Political power gain: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### A Crown under Parliament

`COLDWAR_GRE_R2_parliamentary_king`. Position (42, 13). 35 days.
Predecessors: (constantine). Excludes: royal_veto.
Party requirement: Royalists via `nationalist_monarchists_are_in_power = yes`. Dated native party names apply.

A restrained monarchy can offer continuity without competing with the cabinet. The elected government gains confidence by accepting firm limits on executive discretion.

- Royal Constitutional Programme
- Stability: +10%
- Research speed: +5%
- Political power gain: -10%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### An Active Royal Executive

`COLDWAR_GRE_R2_royal_veto`. Position (46, 13). 35 days.
Predecessors: (constantine). Excludes: parliamentary_king.
Party requirement: Royalists via `nationalist_monarchists_are_in_power = yes`. Dated native party names apply.

An active Crown offers a more decisive executive center. Reopening the question of royal intervention also revives the polarization that destabilized earlier parliamentary government.

- Royal Constitutional Programme
- Political power gain: +20%
- Army organization: +5%
- Stability: -8%
- Research speed: -5%

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

#### Reconcile the Services

`COLDWAR_GRE_R2_services_reconciled`. Position (44, 14). 35 days.
Predecessors: (parliamentary_king OR royal_veto). Excludes: None.
Party requirement: Royalists via `nationalist_monarchists_are_in_power = yes`. Dated native party names apply.

The royalist tradition is strongest in parts of the naval establishment but cannot substitute for inter-service confidence. Reconciliation requires professional representation and a funded command structure.

- Treasury: -1% Greek GDP once
- Royal Constitutional Programme
- Naval organization: +10%
- Bureaucracy budget cost: +3%
- Navy experience +30

Historical basis: [US diplomatic reporting: Greece, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

## Complete recipient-approved packages

All packages below are proposed, not historical contract transcripts. Show all prospective terms in the originating focus and recipient decisions before acceptance, including while locked. Recipient decisions are the only new decision surface. Standing spirits have no fixed expiry.

### Hellenic-American Facilities and Training

The actual United States government approves. No war, embargo or sanctions between the participants. No automatic units or base ownership.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Hellenic-American Facilities

- Treasury: -1% of Greek GDP once
- Weekly income: +0.012% of Greek GDP
- Training time: -10%
- Foreign influence defence: -10%
- 1 x 50% research bonus: Infantry
- 1 x 50% research bonus: Aircraft

**United States**: Greek Facilities Access

- Weekly expense: +0.012% of Greek GDP
- Naval organization: +3%
- Bureaucracy budget cost: +1%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [US-Greek relationship, January 1970](https://history.state.gov/historicaldocuments/frus1969-76v29/d268).

### Hellenic-French Defence Diversification

France approves the proposed training and technical relationship. The later Mirage relationship is a precedent, not an assertion that the 1974 contract already exists in 1970.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Hellenic-French Technical Partnership

- Treasury: -2% of Greek GDP once
- Weekly expense: +0.008% of Greek GDP
- Research speed: +5%
- Education budget cost: +5%
- 2 x 50% research bonus: Light aircraft

**France**: Greek Defence Cooperation

- Weekly income: +0.008% of Greek GDP
- Research speed: +1%
- Bureaucracy budget cost: +1%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [Dassault: Greece ordered Mirage F1 aircraft in 1974](https://www.dassault-aviation.com/en/group/press/press-kits/greece-and-the-rafale/).

### Aegean Working Procedures

Turkey approves reciprocal restraint. Sovereignty claims, borders and control of islands do not change.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Aegean Working Procedures

- Treasury: -0.5% of Greek GDP once
- Stability: +5%
- Naval organization: +5%
- Maximum planning: -5%

**Turkey**: Aegean Working Procedures

- Treasury: -0.5% of own GDP once
- Stability: +5%
- Naval organization: +5%
- Maximum planning: -5%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [NATO: alliance, Aegean tensions and the 1974 command withdrawal](https://www.nato.int/en/about-us/nato-history/history-by-theme/my-country-and-nato/greece-and-nato).

### Restored European Association

Representative institutions and all current Community members consent. Each partner must actually hold EU_member. Greek weekly funding is 0.004% of Greek GDP per signed member; 0.024% for the six-country 1970 preview. Greece does not gain membership here.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Restored European Association

- Treasury: -2% of Greek GDP once
- Weekly expense: +0.004% of Greek GDP per actual member; +0.024% for six members in the January 1970 preview.
- Office income tax yield: +8%
- Civilian factory construction: +5%
- Bureaucracy budget cost: +3%
- Remove Restricted European Association
- Office income tax yield: +8%
- Foreign influence: +10%

**Each actual Community member**: Greek Association Market Access

- Weekly income: +0.004% of Greek GDP
- Office income tax yield: +1%
- Bureaucracy budget cost: +0.5%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [European Parliament: association, suspension and Greek accession](https://www.europarl.europa.eu/RegData/etudes/BRIE/2021/679064/EPRS_BRI%282021%29679064_EN.pdf).

### Greek Community Accession

Active association, native admission conditions and every current member government approval. Association spirits and their charges are replaced, not stacked. Current native Community laws apply. Member-only programmes require actual EU_member thereafter.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Greek Common Market Integration

- Treasury: -3% of Greek GDP once
- Weekly expense: +0.004% of Greek GDP per actual member; +0.024% for six members in the January 1970 preview.
- Office income tax yield: +8%
- Civilian factory construction: +8%
- Bureaucracy budget cost: +5%
- Gain native European Communities membership
- 1 x 50% research bonus: Industry

**Each actual Community member**: Greek Common Market Integration

- Weekly income: +0.004% of Greek GDP
- Office income tax yield: +1%
- Bureaucracy budget cost: +0.5%

**Additional native EU_member base effects for Greece**

- Daily Pro-Western support: +0.05
- Daily Non-Aligned support: +0.03
- Political power gain: -20%
- War support: -5%
- Trade opinion: +15%
- Stability: +5%
- Tax cost: -5%

Required native preview helper must enumerate the actual current global.EU_passed_votes and show each applicable idea modifier, tech sharing, stability and party-popularity delta alongside EU_member base effects. Recompute at proposal and revalidate on acceptance; changed legal terms invalidate the pending offer. Do not substitute prose for those numbers.

Remove both association spirits and their weekly charges before activating accession; never stack association and membership packages.

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [European Parliament: association, suspension and Greek accession](https://www.europarl.europa.eu/RegData/etudes/BRIE/2021/679064/EPRS_BRI%282021%29679064_EN.pdf).

### Greek-Yugoslav Transit Compact

Yugoslavia approves. Both target states must be owned and controlled and have native infrastructure capacity.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Balkan Transit Compact

- Treasury: -1.5% of Greek GDP once
- Office income tax yield: +6%
- Bureaucracy budget cost: +2%
- Southern Macedonia: State shared building slots +1
- Southern Macedonia: Infrastructure +1

**Yugoslavia**: Balkan Transit Compact

- Treasury: -1% of own GDP once
- Office income tax yield: +4%
- Bureaucracy budget cost: +2%
- Eastern Serbia: State shared building slots +1
- Eastern Serbia: Infrastructure +1

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

### Greek-Bulgarian Commercial Protocol

Bulgaria approves. The protocol does not change alliances, borders or military access.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Northern Commercial Protocol

- Treasury: -0.5% of Greek GDP once
- Office income tax yield: +5%
- Foreign influence defence: -3%

**Bulgaria**: Northern Commercial Protocol

- Treasury: -0.5% of own GDP once
- Office income tax yield: +5%
- Foreign influence defence: -3%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

### Guarantor Naval Communications

Britain approves liaison terms. The treaty spirit is required; no Greek control of British bases is granted.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Guarantor Naval Liaison

- Treasury: -0.5% of Greek GDP once
- Weekly expense: +0.004% of Greek GDP
- Naval organization: +5%
- Foreign influence defence: +5%
- Bureaucracy budget cost: +2%

**United Kingdom**: Guarantor Naval Liaison

- Weekly income: +0.004% of Greek GDP
- Naval organization: +2%
- Bureaucracy budget cost: +1%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [UN Treaty Series 382: the 1960 settlement](https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf).

### Greek-German Technical Exchange

West Germany approves. Uses the historical labor and education relationship as a precedent. No workforce penalty or scripted population transfer.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Greek-German Technical Exchange

- Treasury: -1% of Greek GDP once
- Weekly expense: +0.008% of Greek GDP
- Research speed: +5%
- Education budget cost: +3%
- 1 x 50% research bonus: Industry

**West Germany**: Greek-German Technical Exchange

- Weekly income: +0.008% of Greek GDP
- Production efficiency growth: +2%
- Bureaucracy budget cost: +1%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [German Foreign Office: the 1960 recruitment relationship](https://www.auswaertiges-amt.de/de/newsroom/100430-stm-h-festakt-d-grc-223588).

### Eastern Industrial Cooperation

The Soviet government approves. The Greek proposer must actually be the KKE government; the signed state agreement survives a later party change while relations remain eligible.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Eastern Industrial Cooperation

- Treasury: -1.5% of Greek GDP once
- Weekly expense: +0.008% of Greek GDP
- Factory output: +10%
- Foreign influence defence: -10%
- 2 x 50% research bonus: Industry

**Soviet Union**: Eastern Industrial Cooperation

- Weekly income: +0.008% of Greek GDP
- Research speed: +1%
- Bureaucracy budget cost: +1%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [FRUS: Greece and the eastern Mediterranean, 1969-1972](https://history.state.gov/historicaldocuments/frus1969-76v29).

### Hellenic-Cypriot Civilian Cooperation

Cyprus approves. The constitutional guarantee is respected. This does not replace or replay the existing Cyprus-origin Greek training agreement.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Hellenic-Cypriot Civilian Cooperation

- Treasury: -1% of Greek GDP once
- Weekly expense: +0.004% of Greek GDP
- Office income tax yield: +8%
- Research speed: +2%
- Bureaucracy budget cost: +2%

**Cyprus**: Hellenic-Cypriot Civilian Cooperation

- Weekly income: +0.004% of Greek GDP
- Office income tax yield: +10%
- Research speed: +3%
- Foreign influence defence: -5%

No fixed spirit expiry. Both sides exist, remain at peace and impose neither native embargo nor any of the four mirrored Imperia sanction classes on one another. Suspend and restore without replaying fees or assets.

Historical precedent: [UNFICYP: events in summer 1974](https://unficyp.unmissions.org/en/events-summer-1974).

### Cypriot Security Settlement

The Republic of Cyprus and all three guarantor governments agree. Separate Greek Cypriot and Turkish Cypriot safeguard assents must both exist through the existing Cypriot communal programme; Turkish government consent never substitutes for Turkish Cypriot assent. The constitutional Cypriot government is in office and participants are at peace. No forced partition, Enosis, annexation or military access. The existing security-crisis resolution receipt closes the intervention window.

Named recipient countries receive accept/refuse decisions. No Greek offer menu.

**Greece**: Agreed Cypriot Security Settlement

- Treasury: -0.5% of Greek GDP once
- Stability: +8%
- Foreign influence defence: +8%
- Maximum planning: -5%

**Cyprus**: Agreed Cypriot Security Settlement

- Treasury: -0.5% of own GDP once
- Stability: +10%
- Foreign influence defence: +10%
- Bureaucracy budget cost: +5%

**Turkey**: Agreed Cypriot Security Settlement

- Treasury: -0.5% of own GDP once
- Stability: +5%
- Foreign influence defence: +8%
- Maximum planning: -5%

**United Kingdom**: Agreed Cypriot Security Settlement

- Foreign influence defence: +5%
- Bureaucracy budget cost: +1%

All four participants must exist. All six pairs must remain at peace, with neither native embargo nor any of the four mirrored Imperia sanction classes in either direction. Suspend all four settlement spirits if any pair fails; restore all four together when all six pairs qualify. Never repeat setup fees or assets.

Historical precedent: [UN Treaty Series 382: the 1960 settlement](https://treaties.un.org/doc/Publication/UNTS/Volume%20382/v382.pdf).

### Greek Reinforcements for Cyprus

Greece has at least 2,400 free military manpower, 2,400 infantry weapons, 240 light anti-tank weapons, 240 anti-air weapons and 240 command and control equipment in reserve. Cyprus is independent, has not capitulated and owns and controls a deployment location. Greece and Cyprus remain at peace, with no embargo or sanctions against each other.

The Greek focus offers the complete formation package. Cyprus receives one accept/refuse decision. All assets commit immediately together on acceptance, including before war. No recruitment or transport queue. No separate Greek decision menu.

**Greece**: Personnel and equipment contribution

- Military manpower -2,400
- Infantry weapons -2,400
- Light anti-tank weapons -240
- Anti-air weapons -240
- Command and control equipment -240

**Cyprus**: Two fully supplied light infantry divisions

- Cyprus: +2 divisions, Greek-Supplied Light Infantry
- Per division: 1,200 manpower; 18 combat width; 6 light infantry battalions
- Full manpower and equipment on arrival
- Per division: Infantry weapons +1,200
- Per division: Light anti-tank weapons +120
- Per division: Anti-air weapons +120
- Per division: Command and control equipment +120

**Transaction**

- once: True
- receipt: COLDWAR_GRE_R2_CYP_reinforcements_delivered
- debit_country: GRE
- unit_owner: CYP
- manpower: 2400
- equipment: {'infantry_weapons_type': 2400, 'L_AT_Equipment': 240, 'AA_Equipment': 240, 'cnc_equipment_type': 240}
- model: Explicit Greek manpower and stockpile debit pays for two generated CYP units. Do not also send_equipment or add a free Cypriot stockpile package.
- spawn: One division in CYP-owned, CYP-controlled Nicosia11984/state145 and one in Famagusta7193/state146 when both are valid. If only one is valid, place both there. Set allow_spawning_on_enemy_provs = no. Never British state812. Abort before all debits if neither location is valid.
- receipt_order: Validate all costs, recipient consent, template and spawn location before applying any debit. Debit once, create exactly two full-strength CYP-owned formations, then record delivery. Verify postconditions and account for partial failure without charging twice or leaving free units.
- quality: Consume actual compatible Greek variants and preserve their equipment tier. Unit creation must not upgrade old donated weapons into newer Cypriot models.
- engine_check: Before release prove GRE manpower -2400 and exact equipment debits, CYP unit count +2, each unit fully staffed/equipped and CYP free manpower/stockpile unchanged. If native create_unit consumes CYP reserves, compensate only that measured withdrawal. No send-plus-spawn duplication. This behavior requires a native engine fixture.
- reserves: Audited 1970 land OOBs and stockpiles start empty. The focus can be prepared in peacetime, but delivery requires Greece first to produce or acquire the real reserves. No new starting army or free reserve grant is part of this proposal.

One-time irreversible material transfer. The divisions belong to Cyprus and use its ordinary military upkeep. No standing spirit or extra recurring transfer charge is created. Later party changes or suspended diplomatic agreements do not remove the formations or refund the Greek personnel and weapons. Volunteers and direct Greek entry remain independent choices.

Historical precedent: [FRUS: Greek personnel and Cypriot National Guard, September 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d152).

### Full Enosis

The coup succeeded and its Cypriot government remains in office. Cyprus is independent and owns and controls exactly states 145 and 146. A separate 30-day Turkish reaction window must resolve before transfer. Any resulting war must end in real peace first.

Cyprus receives a real accept/refuse decision explicitly disclosing that its country ceases to exist. Turkish objection can open a genuine intervention before transfer; Greek victory followed by actual peace can resume the same signed proposal once. No transfer during war.

**Greece**: Unsettled Enosis

- Treasury: -5% of Greek GDP once
- Weekly expense: +0.03% of Greek GDP
- War support: +5%
- Stability: -10%
- Bureaucracy budget cost: +10%
- Office income tax yield: -8%
- Foreign influence defence: -10%
- Political power -150
- Treasury: add current signed Cypriot treasury
- National debt: add current Cypriot debt
- International investments: transfer current Cypriot assets and liabilities
- Annex Cyprus
- Nicosia and southern Cyprus: ownership to Greece
- Famagusta and northern Cyprus: ownership to Greece
- Transfer existing Cyprus-owned forces to Greece

**Cyprus**: Sovereignty, forces and public accounts

- Cyprus is annexed by Greece
- Nicosia and southern Cyprus: ownership to Greece
- Famagusta and northern Cyprus: ownership to Greece
- Cypriot forces and public accounts transfer to Greece

**Transaction**

- execution_guards: {'CYP_exists': True, 'CYP_is_subject': False, 'requires_actual_coup_government': True, 'CYP_coup_flag': 'COLDWAR_CYP_R2_coup_government', 'CYP_exact_party_trigger': 'nationalist_right_wing_populists_are_in_power', 'CYP_ruling_party_slot': 20, 'CYP_owned_states_exact': [145, 146], 'CYP_controlled_states': [145, 146], 'CYP_at_war': False, 'GRE_at_war_with_TUR': False, 'unresolved_army_crisis': False, 'foreign_volunteers_in_CYP': False, 'current_offer_instance_must_match': True, 'receipt_must_be_unspent': True}
- commit_order: ['Validate current consent, exact state set, peace, independence, cash and unused receipt', 'Capture CYP and GRE signed ledger snapshots and exact troop identities while CYP exists', 'Charge the captured Greek setup price and PP once', 'Migrate and net the complete CYP/GRE ledger and bilateral positions while CYP still exists', 'Execute native annex_country with transfer_troops=yes', 'Verify selected states and carried forces, record union and apply its interim spirit/weekly stream', 'Clear superseded independent-CYP treaties, pending offers and paired programmes; refresh native economy/NATO bookkeeping']
- failure_policy: If annexation fails, restore the captured ledgers and this transaction charges/positions only. No partial inherited cash, lost CYP accounts, extra units or spent-success receipt may remain. Verify the complete transaction in the native engine before release.
- peace_gate: Cyprus must be at peace with every country and Greece must be at peace with Turkey. No active Turkish intervention or army-crisis instance, unresolved coup, active territorial warning or foreign volunteers in Cyprus at final handover. Recall Greek and other foreign volunteers before CYP disappears. Tag deletion never substitutes for peace.
- independence_guard: CYP exists and is_subject = no at offer, every acceptance, renewed ratification and final handover. Subject annexation and its automatic cores/ledger callbacks are outside this transaction.
- territory: CYP owned-state set must be exactly145+146, both fully CYP-controlled.
- consent: The Greek focus commits only to an offer. Snapshot final terms including the binding regional-representation and minority-rights settlement. Require fresh Cypriot assent if government, borders, costs or peace status changes before commitment. The coup itself is not consent to annexation. Southern-union communal assents must concern these exact union terms, not be borrowed from a prior independent-Republic security agreement. Both offers are permanently exclusive after commitment.
- ledger: Snapshot current CYP treasury, national debt and international investment assets/liabilities before annex. Add each signed balance to GRE exactly once through the MD ledger helpers and migrate creditor/investment counterpart records. Include negative treasury and all inherited debt, never only positive assets. Suppress or reconcile any native callback that already transfers a balance, so each entry moves once. No automatic independent-CYP money handler is assumed. Refresh Greek state-based GDP/productivity and budgets; do not grant extra GDP, buildings, resources, slots or population.
- bonds: Migrate each existing MD given_bonds@TAG position in both issuer/holder directions, preserving nominal value and counterparties. Net GRE-CYP internal positions before scalar merging, clear replaced CYP entries, and recompute calculate_new_bonds_held / calculate_new_bonds_owed on GRE and actual affected counterparties. Migrate int_investments counterpart positions similarly and mark the native money state dirty. Do this once at commit, not as a recurring global scan; no new creditor roster. The integration fixture must reconcile all scalar and bilateral totals.
- preview: Before both governments commit, show exact current CYP treasury/debt/investment balances, Greek setup and weekly charges, selected states, current troop/ship/air-wing counts, and every signed interim modifier. The concept gives the territorial and price formula; live asset and ledger amounts require a non-executing native snapshot preview. Changed terms invalidate prior assent.
- live_preview_fields: {'source_country': 'CYP', 'balances': ['treasury', 'debt', 'int_investments'], 'bilateral_positions': 'Both directions of given_bonds@TAG and existing investment counterparty positions, net of GRE-CYP internal balances', 'forces': 'Current Cyprus-owned divisions, ship assets and aircraft, preserving their identities and previous Greek reinforcement receipts', 'quote_lifetime': 'Same signed snapshot and instance shown to Greek and Cypriot players. Requote changed balances before renewed consent; no invented zero values.', 'implementation_boundary': 'A live native snapshot tooltip must show the actual values. This external design view shows the exact formula, not a connected game-state quotation.'}
- core_policy: No add_state_core in the annex reward. Preserve CYP and NCY identity cores. Only the later Civil Settlement focus can add GRE cores to this recorded state set after actual compliance, rights and elapsed-time conditions.
- cleanup: Run CYP-R2 agreement and crisis cleanup immediately after annex; close all pending offers addressed to independent CYP, remove its paired spirits and streams from surviving partners, and end the independent-Republic Treaty of Guarantee marker on GRE/TUR/ENG. On the south route replace it only with the signed partition-settlement receipt. Preserve genuine war/NATO restoration records until real peace. Cancel Greek staff-preparation and coup-initiative streams once their independent-CYP conditions cease.
- rollback: Validate all flags, controlled states, finance snapshots and native target eligibility before any debit. Store the union receipt, balances and troop identities for exactly-once execution and save/rehost safety. No repeat payouts or new reinforcement creation.
- scheduler: Only targeted offer/war/annex/peace callbacks, one-shot 30-day outcome and existing fixed-GRE monthly fallback. No daily/weekly relationship polling.
- budget_lifecycle: Charge the new setup once on actual incorporation. Weekly unsettled-administration expense requires the actual interim spirit and ownership, and stops on integration/removal. After integration replace it with the0.004% weekly regional programme, never stack both charges.

**Pending and resumed ratification**

- initial_expiry_days: 90
- war_paused_receipt: COLDWAR_GRE_R2_enosis_war_paused
- resume_used_receipt: COLDWAR_GRE_R2_enosis_resume_used
- resume_count_max: 1
- resume_expiry_days: 90
- paused_offer_charges: False
- pause: A real Turkish military challenge closes the initial unsigned deadline, stores the exact offered state set and pauses the offer without costs or annexation. The one-shot expiry requires the current non-paused instance and cannot expire the paused-war proposal.
- resume: A targeted peace callback, or fixed GRE monthly fallback, may create one fresh 90-day ratification round after real GRE-TUR/CYP-TUR peace and successful ownership/control checks. Set resume_used before routing it. Require new Greek and CYP approval with freshly quoted balances and the same state set. Never reuse pre-war assent. No second Turkish window. Explicit CYP refusal of the resumed round follows the shared once-only war-goal outcome. Expiry only closes the proposal. Neither creates another retry menu.

**Turkish reaction window**

- days: 30
- receipt: COLDWAR_GRE_R2_enosis_warning_used
- options: ['Recognize the union proposal', 'Protest without military intervention', 'Challenge the proposed union militarily']
- military_response: Challenge pauses the territorial transaction and starts an actual Turkish-Cypriot war through a new single-use Enosis episode. Greece receives one explicit escalation or renunciation event. Escalation snapshots and removes actual GRE/TUR NATO membership before native Greek entry on Cyprus side. Its restoration uses real GRE-TUR and CYP-TUR peace. The existing once-per-campaign army-crisis flags are never cleared or restarted, and used 180-day combat buffs are not renewed or stacked.
- resume: After a military challenge, resume this same proposal at most once, after both actual peace pairs, full Cypriot control of145+146 and renewed Greek/Cypriot ratification. A second Turkish window is not created. Loss of territory leaves full Enosis unavailable; choosing this claim excludes the negotiated southern focus.
- protest: Nonmilitary rejection does not veto a Greek-Cypriot union but keeps it internationally contested and imposes the stated full interim penalties. No automatic diplomatic recognition or Turkish-Cypriot approval is invented.

**If Cyprus refuses**

- Greece: gain Annexation war goal against Cyprus

- declining_country: CYP
- beneficiary: GRE
- option_title: Reject the Union Demand
- shared_once_receipt: COLDWAR_GRE_R2_enosis_refusal_wargoal_issued
- guards: {'explicit_response': 'refuse', 'recipient_must_be': 'CYP', 'current_pending_instance': True, 'government_snapshot_matches': True, 'route_must_match': 'enosis_full', 'CYP_exists': True, 'CYP_is_subject': False, 'CYP_owned_states_exact': [145, 146], 'GRE_exists': True, 'GRE_at_war_with_CYP': False, 'union_already_committed': False, 'shared_receipt_unused': True}
- excluded_triggers: ['offer timeout', 'offer cancellation', 'stale or superseded option', 'Turkish refusal', 'British refusal', 'Northern Cypriot refusal', 'communal non-assent without an actual CYP rejection']
- execution_order: ['Validate the explicit CYP refusal and current country/offer instance', 'Close the pending peaceful offer and cancel only its unresolved warning/ratification callbacks', 'Consume the shared once-only GRE receipt', 'In fixed GRE scope create the route-appropriate war goal against CYP']
- preview: Show this exact Greek war-goal effect under If Cyprus refuses in the originating focus and on the Cypriot refusal option before the player chooses. No agreement setup costs, territorial transfer, troop transfer, core or administration spirit apply merely on refusal.
- duplicates: One refusal goal per campaign across both Enosis routes and any resumed ratification. Do not duplicate an equivalent existing goal or refresh it through a repeat offer. No scripted inline expiry field: use the native goal types and their native lifetime.
- war_policy: The goal permits a later native declaration, not an automatic war. Ordinary faction and declaration rules still apply. Its issuance does not remove anyone from NATO. A GRE-against-CYP war is a separate conflict from Greek aid to CYP against TUR.
- turkish_entry: {'when': 'After an actual GRE-CYP refusal war, Turkey may choose to defend Cyprus through a separate guarantor response.', 'native_join': 'TUR = { add_to_war = { targeted_alliance = CYP enemy = GRE hostility_reason = asked_to_join } }', 'nato': 'Snapshot actual GRE/TUR memberships for this refusal-conflict instance, call native NATO_leave for those actual members before Turkish entry against GRE, and preserve unrelated faction choices. Do not call the opposite-side COLDWAR_CYP_R2_ACT_gre_escalate_apply.', 'restoration_peace_pairs': [['GRE', 'CYP'], ['GRE', 'TUR']], 'restore_only_prior_members': True, 'readmission_guard': 'Block NATO_join, NATO_join_via_event and stale invitations while either actual refusal-war pair remains at war. The older CYP-TUR peace guard is insufficient. Separate receipts and targeted peace callbacks plus the existing monthly fallback handle restoration. Never reset the old army-crisis instance or replay used combat buffs.'}
- conquest_followthrough: {'trigger': 'Recorded use of this refusal goal in a real GRE-CYP war, actual native peace settlement, CYP no longer exists, and GRE actually owns and controls the original target-state set. Capture the conflict and pre-removal accounts through tested native war/annex/peace callbacks. A war goal alone never qualifies.', 'effects': 'Record the same route-specific unsettled incorporation and its date only after actual conquest. Apply its original PP/setup costs and interim weekly burden once, taking any unavoidable treasury shortfall into properly recorded MD public debt. No free peaceful-annex transfer, added units or extra cash. Preserve exactly the assets and forces actually acquired in the native settlement, reconciling the existing ledger/annex handlers once.', 'core': 'The common Civil Settlement focus becomes reachable after730 days,70 compliance, actual peace and enacted minority/representation safeguards. It grants cores only in the original target states actually acquired. Territory merely occupied during an ongoing war never qualifies.'}

One-time territorial union, not a suspendable bilateral spirit. Greece receives the current territories, existing state assets and existing Cyprus-owned forces once. Greek-supplied divisions already in CYP service transfer with those forces and are never respawned. Existing British sovereign bases remain British. No Greek cores on union. The interim administration and weekly funding last until the separate integration settlement, or while Greece retains the transferred territory.

Historical precedent: [FRUS: Acheson union and security proposals, July 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d85).

### A Negotiated Southern Union

The coup succeeded and the independent Cypriot coup government remains in office. An actual settled partition exists: CYP owns and controls only 145, while 146 belongs to and is controlled by Turkey or Northern Cyprus. Peaceful incorporation requires approval from Cyprus, Turkey and Britain; Northern Cyprus must separately agree if it owns 146. Distinct Greek Cypriot and Turkish Cypriot safeguards are agreed.

Cyprus receives a real accept/refuse decision explicitly disclosing that its remaining country is incorporated into Greece. Turkey, Britain and, where applicable, Northern Cyprus must independently approve identical terms. All signatories remain at peace and sanction-free with one another. No transfer on refusal.

**Greece**: Southern Union Administration

- Treasury: -2.5% of Greek GDP once
- Weekly expense: +0.015% of Greek GDP
- Stability: -5%
- Bureaucracy budget cost: +5%
- Office income tax yield: -4%
- Foreign influence defence: -5%
- Political power -100
- Treasury: add current signed Cypriot treasury
- National debt: add current Cypriot debt
- International investments: transfer current Cypriot assets and liabilities
- Annex Cyprus
- Nicosia and southern Cyprus: ownership to Greece
- Transfer existing Cyprus-owned forces to Greece

**Cyprus**: Sovereignty, forces and public accounts

- Cyprus is annexed by Greece
- Nicosia and southern Cyprus: ownership to Greece
- Cypriot forces and public accounts transfer to Greece

**Turkey**: Recognition of the northern settlement

- Political power -25
- Opinion of Greece +25 (730 days)

**United Kingdom**: Guarantor settlement

- Political power -10
- Opinion of Greece +15 (730 days)

**Northern Cyprus**: If Northern Cyprus owns state 146 and signs

- Opinion of Greece +25 (730 days)

**Transaction**

- execution_guards: {'CYP_exists': True, 'CYP_is_subject': False, 'requires_actual_coup_government': True, 'CYP_coup_flag': 'COLDWAR_CYP_R2_coup_government', 'CYP_exact_party_trigger': 'nationalist_right_wing_populists_are_in_power', 'CYP_ruling_party_slot': 20, 'CYP_owned_states_exact': [145], 'CYP_controlled_states': [145], 'CYP_at_war': False, 'GRE_at_war_with_TUR': False, 'unresolved_army_crisis': False, 'foreign_volunteers_in_CYP': False, 'current_offer_instance_must_match': True, 'receipt_must_be_unspent': True}
- commit_order: ['Validate current consent, exact state set, peace, independence, cash and unused receipt', 'Capture CYP and GRE signed ledger snapshots and exact troop identities while CYP exists', 'Charge the captured Greek setup price and PP once', 'Migrate and net the complete CYP/GRE ledger and bilateral positions while CYP still exists', 'Execute native annex_country with transfer_troops=yes', 'Verify selected states and carried forces, record union and apply its interim spirit/weekly stream', 'Clear superseded independent-CYP treaties, pending offers and paired programmes; refresh native economy/NATO bookkeeping']
- failure_policy: If annexation fails, restore the captured ledgers and this transaction charges/positions only. No partial inherited cash, lost CYP accounts, extra units or spent-success receipt may remain. Verify the complete transaction in the native engine before release.
- peace_gate: Cyprus must be at peace with every country and Greece must be at peace with Turkey. No active Turkish intervention or army-crisis instance, unresolved coup, active territorial warning or foreign volunteers in Cyprus at final handover. Recall Greek and other foreign volunteers before CYP disappears. Tag deletion never substitutes for peace.
- independence_guard: CYP exists and is_subject = no at offer, every acceptance, renewed ratification and final handover. Subject annexation and its automatic cores/ledger callbacks are outside this transaction.
- territory: CYP owned-state set must be exactly145, CYP-controlled. Northern146 already belongs to and is controlled by TUR or NCY. Do not manufacture a new northern owner or leave a Greek-Cypriot CYP government in the north.
- consent: The Greek focus commits only to an offer. Snapshot final terms including the binding regional-representation and minority-rights settlement. Require fresh Cypriot assent if government, borders, costs or peace status changes before commitment. The coup itself is not consent to annexation. Southern-union communal assents must concern these exact union terms, not be borrowed from a prior independent-Republic security agreement. Both offers are permanently exclusive after commitment.
- ledger: Snapshot current CYP treasury, national debt and international investment assets/liabilities before annex. Add each signed balance to GRE exactly once through the MD ledger helpers and migrate creditor/investment counterpart records. Include negative treasury and all inherited debt, never only positive assets. Suppress or reconcile any native callback that already transfers a balance, so each entry moves once. No automatic independent-CYP money handler is assumed. Refresh Greek state-based GDP/productivity and budgets; do not grant extra GDP, buildings, resources, slots or population.
- bonds: Migrate each existing MD given_bonds@TAG position in both issuer/holder directions, preserving nominal value and counterparties. Net GRE-CYP internal positions before scalar merging, clear replaced CYP entries, and recompute calculate_new_bonds_held / calculate_new_bonds_owed on GRE and actual affected counterparties. Migrate int_investments counterpart positions similarly and mark the native money state dirty. Do this once at commit, not as a recurring global scan; no new creditor roster. The integration fixture must reconcile all scalar and bilateral totals.
- preview: Before both governments commit, show exact current CYP treasury/debt/investment balances, Greek setup and weekly charges, selected states, current troop/ship/air-wing counts, and every signed interim modifier. The concept gives the territorial and price formula; live asset and ledger amounts require a non-executing native snapshot preview. Changed terms invalidate prior assent.
- live_preview_fields: {'source_country': 'CYP', 'balances': ['treasury', 'debt', 'int_investments'], 'bilateral_positions': 'Both directions of given_bonds@TAG and existing investment counterparty positions, net of GRE-CYP internal balances', 'forces': 'Current Cyprus-owned divisions, ship assets and aircraft, preserving their identities and previous Greek reinforcement receipts', 'quote_lifetime': 'Same signed snapshot and instance shown to Greek and Cypriot players. Requote changed balances before renewed consent; no invented zero values.', 'implementation_boundary': 'A live native snapshot tooltip must show the actual values. This external design view shows the exact formula, not a connected game-state quotation.'}
- core_policy: No add_state_core in the annex reward. Preserve CYP and NCY identity cores. Only the later Civil Settlement focus can add GRE cores to this recorded state set after actual compliance, rights and elapsed-time conditions.
- cleanup: Run CYP-R2 agreement and crisis cleanup immediately after annex; close all pending offers addressed to independent CYP, remove its paired spirits and streams from surviving partners, and end the independent-Republic Treaty of Guarantee marker on GRE/TUR/ENG. On the south route replace it only with the signed partition-settlement receipt. Preserve genuine war/NATO restoration records until real peace. Cancel Greek staff-preparation and coup-initiative streams once their independent-CYP conditions cease.
- rollback: Validate all flags, controlled states, finance snapshots and native target eligibility before any debit. Store the union receipt, balances and troop identities for exactly-once execution and save/rehost safety. No repeat payouts or new reinforcement creation.
- scheduler: Only targeted offer/war/annex/peace callbacks, one-shot 30-day outcome and existing fixed-GRE monthly fallback. No daily/weekly relationship polling.
- budget_lifecycle: Charge the new setup once on actual incorporation. Weekly unsettled-administration expense requires the actual interim spirit and ownership, and stops on integration/removal. After integration replace it with the0.004% weekly regional programme, never stack both charges.

**If Cyprus refuses**

- Greece: gain Take State war goal against Cyprus: Nicosia and southern Cyprus (730 days)

- declining_country: CYP
- beneficiary: GRE
- option_title: Reject the Union Demand
- shared_once_receipt: COLDWAR_GRE_R2_enosis_refusal_wargoal_issued
- guards: {'explicit_response': 'refuse', 'recipient_must_be': 'CYP', 'current_pending_instance': True, 'government_snapshot_matches': True, 'route_must_match': 'enosis_south', 'CYP_exists': True, 'CYP_is_subject': False, 'CYP_owned_states_exact': [145], 'GRE_exists': True, 'GRE_at_war_with_CYP': False, 'union_already_committed': False, 'shared_receipt_unused': True}
- excluded_triggers: ['offer timeout', 'offer cancellation', 'stale or superseded option', 'Turkish refusal', 'British refusal', 'Northern Cypriot refusal', 'communal non-assent without an actual CYP rejection']
- execution_order: ['Validate the explicit CYP refusal and current country/offer instance', 'Close the pending peaceful offer and cancel only its unresolved warning/ratification callbacks', 'Consume the shared once-only GRE receipt', 'In fixed GRE scope create the route-appropriate war goal against CYP']
- preview: Show this exact Greek war-goal effect under If Cyprus refuses in the originating focus and on the Cypriot refusal option before the player chooses. No agreement setup costs, territorial transfer, troop transfer, core or administration spirit apply merely on refusal.
- duplicates: One refusal goal per campaign across both Enosis routes and any resumed ratification. Do not duplicate an equivalent existing goal or refresh it through a repeat offer. No scripted inline expiry field: use the native goal types and their native lifetime.
- war_policy: The goal permits a later native declaration, not an automatic war. Ordinary faction and declaration rules still apply. Its issuance does not remove anyone from NATO. A GRE-against-CYP war is a separate conflict from Greek aid to CYP against TUR.
- turkish_entry: {'when': 'After an actual GRE-CYP refusal war, Turkey may choose to defend Cyprus through a separate guarantor response.', 'native_join': 'TUR = { add_to_war = { targeted_alliance = CYP enemy = GRE hostility_reason = asked_to_join } }', 'nato': 'Snapshot actual GRE/TUR memberships for this refusal-conflict instance, call native NATO_leave for those actual members before Turkish entry against GRE, and preserve unrelated faction choices. Do not call the opposite-side COLDWAR_CYP_R2_ACT_gre_escalate_apply.', 'restoration_peace_pairs': [['GRE', 'CYP'], ['GRE', 'TUR']], 'restore_only_prior_members': True, 'readmission_guard': 'Block NATO_join, NATO_join_via_event and stale invitations while either actual refusal-war pair remains at war. The older CYP-TUR peace guard is insufficient. Separate receipts and targeted peace callbacks plus the existing monthly fallback handle restoration. Never reset the old army-crisis instance or replay used combat buffs.'}
- conquest_followthrough: {'trigger': 'Recorded use of this refusal goal in a real GRE-CYP war, actual native peace settlement, CYP no longer exists, and GRE actually owns and controls the original target-state set. Capture the conflict and pre-removal accounts through tested native war/annex/peace callbacks. A war goal alone never qualifies.', 'effects': 'Record the same route-specific unsettled incorporation and its date only after actual conquest. Apply its original PP/setup costs and interim weekly burden once, taking any unavoidable treasury shortfall into properly recorded MD public debt. No free peaceful-annex transfer, added units or extra cash. Preserve exactly the assets and forces actually acquired in the native settlement, reconciling the existing ledger/annex handlers once.', 'core': 'The common Civil Settlement focus becomes reachable after730 days,70 compliance, actual peace and enacted minority/representation safeguards. It grants cores only in the original target states actually acquired. Territory merely occupied during an ongoing war never qualifies.'}

One-time territorial union, not a suspendable bilateral spirit. Greece receives the current territories, existing state assets and existing Cyprus-owned forces once. Greek-supplied divisions already in CYP service transfer with those forces and are never respawned. Existing British sovereign bases remain British. No Greek cores on union. The interim administration and weekly funding last until the separate integration settlement, or while Greece retains the transferred territory.

Historical precedent: [FRUS: Acheson union and security proposals, July 1964](https://history.state.gov/historicaldocuments/frus1964-68v16/d85).

## Implementation and performance contract

**Approval**: Design only. Current Greek runtime tree and all loaded files are retained until approval.

**Party programmes**: Keep all branches visible. Exact existing native party-in-power triggers gate availability and execution. Rebuild each party-owned dynamic modifier from earned receipts only while that party governs; named leader subprogrammes require that leader as well. Disable their weekly streams on departure; restore on return. Never replay buildings, slots, research, XP, setup fees or one-time starting-spirit remedies. State constitutional settlements and signed bilateral agreements retain their separate state conditions.

**Refresh**: Existing party/leader change callbacks plus one GRE monthly reconciliation. Fixed CYP/GRE crisis participants and explicit offer partners only. No new daily or weekly script observer, no every_country loops or global monthly offer searches. Budget streams use existing MD weekly accounting, with literals of at most five decimal places.

**Party identity**: Use actual native party-name localisation keys. Slot 1 uses the dated ERE/ND identity; slot 3 the dated PAK/PASOK identity. Correct the native 1970 slot23 display to Royalists because the kingdom still exists; reserve restoration language for an actual subsequent abolition. Preserve existing slot alignment, including slot7 State Emergency Hardliners. Do not activate banned parties automatically.

**Civilian transfer**: Negotiate a Civilian Handover proposes a one-time domestic event with actual Kanellopoulos conservative or Mavros Centre Union caretaker cabinets, preserving the existing native party/leader dispatcher. A cabinet already under civilian rule is not overwritten. This is a hypothetical negotiated alternative, not a claim of a real January 1970 deal. Actual civilian authority ends Emergency Rule. The following amnesty and election focuses restore competition; PAK/PASOK and KKE may later govern through the native party system. The Crown remains constitutionally unsettled until the explicit settlement fork. Papadopoulos and Ioannidis internal choices also route to real government/leader snapshots rather than cosmetic names.

**Offer lifecycle**: A Greek national focus proposes each unique contract. Named RP recipients receive accept/refuse decisions with full prospective numeric effects for all participants. The pending offer expires after 90 days, cleaned by monthly/event callbacks. An unpaid declined or expired offer may be resent once by a single Greek event option with no home-country decision menu; one active offer per contract. Every required recipient must agree to identical terms. Payment, ownership, capacity, existence, independence where required, party proposer and relation guards recheck at acceptance. No unilateral rewards. Setup and one-time assets commit atomically only once all approvals and all guards succeed. Permanent standing spirits suspend and restore together without repeating charges or assets.

**Community**: Snapshot only the current native global.EU_member, excluding GRE, for one proposal round. Use exact count N for Greek expense N x 0.004% Greek GDP per week and each member income 0.004%. Six is only the January 1970 preview. Membership or passed-law changes invalidate pending terms. Accession replaces association spirits and charges. Before consent, a native preview helper enumerates every applicable effect of current EU_passed_votes as well as all seven base EU_member modifiers, research and money. At concept snapshot no specific passed laws are assumed. Add EU_member through its native on_add only after admission. No EU_join helper or custom membership roster.

**Community setup correction**: After the erroneous inherited Greek EU_member is removed through its native on_remove, synchronize native member/law/tech-sharing cleanup and explicitly clear the artificial EU_former_member and EU_rejoin_cooldown flags. Greece was never a former member. Prevent the history/generator from restoring the error. Begin with Restricted European Association. Do not touch other actual members.

**Buildings**: Every building level first adds one shared slot in the same state inside the same asset receipt. Actual target ownership, control, native building cap and available state capacity are separate guards. Failure never charges setup money or creates orphan slots. A recipient asset uses that recipient ownership, not Greek ownership.

**Cyprus preparation**: The extra +10 staff penetration uses a unique timed receipt and clamp 0..100. It expires after 180 days or on network withdrawal/crisis cancellation; remove the contribution once and clear the receipt. Existing withdrawal remains -20, plus -10 when preparation is active. A resolved coup consumes the contribution receipt. No double subtraction after resolution. Remove Forward Operational Planning when cancelled.

**Cyprus resolution**: Reuse the existing deterministic 14-day warning: captured defence is 40 plus Cypriot preparedness, and Greek penetration must strictly exceed it. A tie defends. No random roll or periodic roll. Operational Initiative is once only after real coup success with the coup government still in power, peaceful GRE-CYP relations and no sanctions/embargo. Completion rechecks these guards. Its weekly charge stops on loss of eligibility or the 180-day expiry.

**Settlement**: The four governments are Cyprus plus the three guarantors, not four guarantors. Require separate Greek Cypriot and Turkish Cypriot assent receipts from the Cypriot communal programme. All six state pairs are checked in both sanction directions. Suspend and restore all four settlement spirits collectively. Close the existing security-crisis receipt on successful settlement.

**Nato**: Retain installed CYP_R2 war and NATO APIs and all nine existing Greek shared-focus IDs, relocating their anchors after approval. Direct Greek entry removes prior GRE/TUR NATO memberships before joining the actual CYP-TUR war. Return each prior member only after both GRE-TUR and CYP-TUR peace. This is the requested alternative-history full Alliance exit; historical Greece withdrew only from integrated military command in 1974. New Aegean Expeditionary Command is a once-only 180-day direct-entry reward: +10% army and navy organization, +25% planning, +15% maximum planning, +20% amphibious attack, +30% invasion preparation, -10% office income and +0.05% Greek GDP weekly expense. Require actual successful entry on Cyprus side. End that package on related Greek-Turkish peace or 180 days; never end NATO separation merely because the reward expires. No automatic divisions, aircraft or ships are created. Real volunteer formations still require the actual native deployment action and Cypriot approval. Same-faction deployment compatibility remains a live-engine check.

**New helpers**: COLDWAR_GRE_R2_politics events, programme refresh, recipient offers, dynamic law preview, staff receipt cleanup and post-coup reward helpers are proposed new work. Their names in this concept do not imply installed definitions.

**Entry transaction**: Wrap the existing escalation helper in a single guarded completion transaction. Verify independence, war sides, funds and native entry eligibility before snapshots and debit. After add_to_war, require actual GRE-TUR war, CYP-TUR war, no GRE-CYP war and the entry receipt before issuing the separate expeditionary package receipt and weekly active receipt. The previous helper entry flag alone does not prove success. If native entry fails, grant no package or stream, refund exactly the captured 100 PP and 1.5% Greek-GDP debit and undo only this attempt NATO changes through native helpers with the saved prior memberships. Clear the failed attempt separation receipts before rollback, not an unrelated active crisis. No permanent faction loss after a failed war join. Do not replay a completed successful entry.

**Reinforcements**: New independent 7-day Reinforce the National Guard focus offers two CYP-owned 18-width light infantry divisions. Six L_Inf_Bat each, exactly1200 manpower and1200 infantry weapons,120 light anti-tank,120 anti-air and120 CNC equipment per division. Greece loses the complete two-division reserve, Cyprus receives fully formed units immediately on consent. Available before Turkish intervention; no dependency or exclusion with Volunteers or Fight Beside Cyprus. This is a one-time paid unit transfer, not a starting OOB, free reserve, standing spirit or change of belligerent status. Use explicit Greek stockpile debit plus unit generation; do not also transfer a second equipment package. The new transaction data and REINFORCEMENT_REFERENCE.md define the native engine conservation fixture. No extra monthly observer. Independent Cypriot consent and controlled landing area are required. Historical precedent is the exceptional1964-67 deployment, not an automatic Treaty of Guarantee entitlement.

**Replacement**: After approval: archive old Greek content outside the mod on E:, update its original generator and emitted tree, remove stale custom focus/idea/event references, integrate the approved data and preserve the existing Cyprus shared-focus identities. No deletion or installation performed by this concept build.

**Fiscal revision**: General one-time commitments x2, selected major capital programmes x3; larger differentiated recurring budgets and explicit crisis-helper replacement prices. Modifier percentages, focus times, material requirements and PP prices are unchanged. Temporary charges require actual spirit presence and the original live instance in the existing money calculation; resetting contributions to zero prevents stale cached expenses. No weekly relationship observer is added.

## Fiscal revision

Budget changes are proposed game balance. Native rates and stream gates still require implementation and engine testing. One-time crisis-helper overrides replace old fees rather than add another charge.

General one-time commitments x2, selected major capital programmes x3; larger differentiated recurring budgets and explicit crisis-helper replacement prices. Modifier percentages, focus times, material requirements and PP prices are unchanged.

- Army Schools and Staff Courses: {"spirit": "Staff College Funding", "required_idea_id": "COLDWAR_GRE_R2_idea_staff_college_funding", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.004, "native_weekly_fraction": "0.00004", "active_instance_receipt": "COLDWAR_GRE_R2_army_school_budget_episode", "original_issue_receipt": "COLDWAR_GRE_R2_army_school_budget_episode_issued_once", "original_expiry_receipt": "COLDWAR_GRE_R2_army_school_budget_episode_expired", "required_flags": [], "maximum_days": 180, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans."}
- An Aegean Command: {"spirit": "Aegean Staff Funding", "required_idea_id": "COLDWAR_GRE_R2_idea_aegean_staff_funding", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.006, "native_weekly_fraction": "0.00006", "active_instance_receipt": "COLDWAR_GRE_R2_aegean_command_budget_episode", "original_issue_receipt": "COLDWAR_GRE_R2_aegean_command_budget_episode_issued_once", "original_expiry_receipt": "COLDWAR_GRE_R2_aegean_command_budget_episode_expired", "required_flags": [], "maximum_days": 180, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans."}
- Professional Cadres: {"weekly_gdp_percent": 0.01, "native_weekly_fraction": "0.0001", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_professional_cadres"}
- A Fleet for Sea Control: {"weekly_gdp_percent": 0.015, "native_weekly_fraction": "0.00015", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_sea_control"}
- Battlefield Air Support: {"weekly_gdp_percent": 0.01, "native_weekly_fraction": "0.0001", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_close_support"}
- Recover Room for Diplomacy: {"weekly_gdp_percent": 0.003, "native_weekly_fraction": "0.00003", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_external_room"}
- Deterrence in the Aegean: {"weekly_gdp_percent": 0.01, "native_weekly_fraction": "0.0001", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_aegean_deterrence"}
- The Security Establishment: {"weekly_gdp_percent": 0.01, "native_weekly_fraction": "0.0001", "gate": "Earned programme active under its actual party/leader requirements, where applicable. Clear to zero when inactive. Permanent programmes continue while eligible; they are not incorrectly given a 180-day expiry.", "source_receipt": "COLDWAR_GRE_R2_security_budget"}
- Volunteers for Cyprus: {"spirit": "COLDWAR_CYP_R2_cyprus_volunteer_mission", "required_idea_id": "COLDWAR_CYP_R2_cyprus_volunteer_mission", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.02, "native_weekly_fraction": "0.0002", "active_instance_receipt": "COLDWAR_CYP_R2_volunteer_mission_authorized", "original_issue_receipt": "COLDWAR_CYP_R2_volunteer_mission_authorized_issued_once", "original_expiry_receipt": null, "required_flags": ["COLDWAR_CYP_R2_volunteer_expense_active"], "maximum_days": null, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans.", "replaces_native_stream": "Replace the existing Greek volunteer contribution in COLDWAR_CYP_R2_crisis_weekly_streams with 0.0002 and its has_idea gate. Do not also add it as a second Greek programme."}
- Prepare the Officer Network: {"spirit": "Forward Operational Planning", "required_idea_id": "COLDWAR_GRE_R2_idea_forward_operational_planning", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.01, "native_weekly_fraction": "0.0001", "active_instance_receipt": "COLDWAR_GRE_R2_staff_network_budget_episode", "original_issue_receipt": "COLDWAR_GRE_R2_staff_network_budget_episode_issued_once", "original_expiry_receipt": "COLDWAR_GRE_R2_staff_network_budget_episode_expired", "required_flags": [], "maximum_days": 180, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans.", "separate_from_penetration_receipt": true}
- The Operational Initiative: {"spirit": "Operational Initiative in Cyprus", "required_idea_id": "COLDWAR_GRE_R2_idea_operational_initiative", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.03, "native_weekly_fraction": "0.0003", "active_instance_receipt": "COLDWAR_GRE_R2_operational_initiative_budget_episode", "original_issue_receipt": "COLDWAR_GRE_R2_operational_initiative_budget_episode_issued_once", "original_expiry_receipt": "COLDWAR_GRE_R2_operational_initiative_budget_episode_expired", "required_flags": [], "maximum_days": 180, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans."}

- Direct-entry expeditionary stream: {"spirit": "Aegean Expeditionary Command", "required_idea_id": "COLDWAR_GRE_R2_idea_aegean_expeditionary_command", "idea_definition_status": "New Greek IDs are required outputs of approved implementation; existing CYP volunteer ID is reused.", "weekly_gdp_percent": 0.05, "native_weekly_fraction": "0.0005", "active_instance_receipt": "COLDWAR_GRE_R2_expeditionary_command_active", "original_issue_receipt": "COLDWAR_GRE_R2_expeditionary_command_active_issued_once", "original_expiry_receipt": "COLDWAR_GRE_R2_expeditionary_command_active_expired", "required_flags": [], "maximum_days": 180, "gate": "Read actual has_idea plus this active episode and its original deadline in the existing local money-rate calculation. Missing spirit, expired deadline or cancelled episode contributes zero even if a monthly cache is stale.", "cleanup": "On removal, expiry, cancellation or loss of programme eligibility, remove the stream immediately. On return of a party restore only the remaining original lifetime, never another full duration. Never replay setup fees, doctrine, XP or units.", "refresh_on_removal": "Idea on_remove and the original one-shot expiry callback clear this contribution and request a refresh of native expense/display rates before the next treasury application. Do not wait for monthly reconciliation or run an extra treasury debit. Repeated cleanup is a no-op.", "removal_order": ["Clear only the active budget episode, preserving the original issue/expiry clock", "Set this stream contribution to zero", "Refresh calculate_additional_expense_rate, update_display and update_money_dirty_variable without applying treasury a second time"], "expiry_clock": "Schedule one hidden expiry event at original issue for the stated maximum duration. It marks the immutable instance expired even while the spirit is absent. Party restoration before that event may restore only the remaining lifetime; after that event it restores neither spirit nor cost. Never reschedule the original expiry. Mission-bound programmes without a fixed maximum end on actual mission closure instead.", "calculation": "Reset this contribution to zero before every calculation. Add it to the country expense accumulator exactly once; repeated recalculation must not accumulate a previous total. No weekly world, sanctions or relationship scans."}

- Native Turkish stream guard: Preserve its separately approved rate, but require COLDWAR_CYP_R2_cyprus_intervention_forces plus the active intervention receipt in the existing local accumulator. A stale intervention_expense_cached flag must not charge after the 180-day spirit expires. No new Turkish fee or duplicated stream.

## Approval boundary

Static graph, data, native API and geometry review establish a reviewable proposal. They do not establish in-game loading, native tooltips, volunteer compatibility or multiplayer execution. Those checks follow approved implementation. See RESEARCH_HISTORY.md, HISTORY_REVIEW.md, MD_REFERENCE_LAYOUT.md, COORDINATE_REVIEW.json and MECHANICS_REVIEW.md for independent evidence.
