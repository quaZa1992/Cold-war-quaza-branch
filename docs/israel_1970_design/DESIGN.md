# IMPERIA COLD WAR: Israel 1970 Implemented Focus Tree

399 focuses, 182 decisions, 77 events, twenty political families and thirty-seven named party/list variants. All new game localisation is English.

The compact layout uses relative-position anchors as in the MD Russia tree. Each political family starts directly when its exact party governs. The twelve outlook unlocks and twenty government-mandate focuses have been removed. No party entry requires a focus or a foundation flag. Internal policy choices remain connected within their branches. Shared achievements survive changes of government; party programme modifiers apply only while that party governs.

The 27 October 2026 revision adds distinct institutional rewards, stronger civilian productivity and diaspora finance, a shared workforce route capped at +15%, and three bounded settlement extensions. Ceasefire talks are player-initiated and territorial administration opens independently of military outcomes. See REWORK_20261027.md for history, numerical routes, provenance and validation limits.

The corrected settlement-presence extension separates unilateral footholds under foreign control from controlled-state construction, with regional occupation costs. The affected controller receives production, stability and budget penalties without a consent decision or payment. An existing Palestine also receives bounded West Bank/Gaza institutional and commercial pressure from actual settlement programmes, with selected funded compensation relief. See UNILATERAL_SETTLEMENTS.md, PRESENCE_AND_OCCUPATION.md and PALESTINIAN_PRESSURE.md for conditions, numeric terms, period sources and verification limits.

The retained outlooks are Western, Emerging, Non-Aligned and Nationalist. There are no Shiite or Salafist paths, foundations, campaigns or government programmes. Their four native slots are disabled for the 1970 Israel scenario.

Golda Meir and the Alignment lead the January 1970 coalition. Religious Zionist and Orthodox parliamentary parties retain their own programmes. Later named parties require their dated or explicitly alternative foundations. Generic MD symbols and portraits are used when period assets are absent.

## Starting Spirits

### Citizen Army and Reserve

The citizen army combines a small standing force with a trained reserve. Readiness and civilian employment must be balanced.

`mobilization_speed`: +0.15, `army_org_factor`: +0.03

### Histadrut and the Building Society

The labor federation and cooperative institutions remain major pillars of industrial development and social provision.

`production_speed_industrial_complex_factor`: +0.05, `social_cost_multiplier_modifier`: -0.03

### The Unity Government of 1969

A broad parliamentary majority provides stability but requires sustained negotiation between distinct political partners.

`stability_factor`: +0.04, `political_power_factor`: -0.05

### The War of Attrition

An unresolved conflict consumes personnel resources. A mutually accepted ceasefire can remove this burden.

`war_support_factor`: +0.03, `mobilization_speed`: +0.05, `personnel_cost_multiplier_modifier`: +0.08

### Lessons of the French Embargo

Restricted external deliveries make defense manufacturing harder until reliable contracts or a domestic production programme are established.

`production_speed_arms_factory_factor`: -0.05

### Immigration and Development Gaps

Immigration sustains population growth but requires housing, education and social provision.

`monthly_population`: +0.05, `social_cost_multiplier_modifier`: +0.05

### Nuclear Ambiguity

A policy of ambiguity supports diplomatic independence without granting weapons or bypassing technology and material requirements.

`foreign_influence_defense_modifier`: +0.05

## State and Knesset

A shared state branch whose institutional achievements survive changes of government.

### Israel in January 1970

`ISR70_january_1970` | x=53, y=0 | 14 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Set the cabinet agenda for the new decade and release political capital for the first reforms.

- Political Power: +100

```hoi4
add_political_power = 100
```

### The Seventh Knesset

`ISR70_knesset` | x=53, y=1 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

The Seventh Knesset brings together the parties elected in October 1969. Parliamentary committees and a working legislative agenda must give the new government a durable basis for reform.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### A Cabinet across the Party Lines

`ISR70_unity_cabinet` | x=50, y=2 | 35 days

Prerequisites: (ISR70_knesset).

Exclusive with: ISR70_narrow_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

A broad coalition can distribute responsibility for national security across the major parties. Its members will expect a say in appointments and spending, slowing the passage of a common legislative programme.

- The Military Opinion: +5.
- Removes the national spirit "The Unity Government of 1969".
- Removes the national spirit "The Unity Government of 1969".
- National spirit:
- Stability: +5%
- Political Power Gain: -3%
- Planning Speed: +5%
- Opens the corresponding cabinet or municipal event.

```hoi4
add_ideas = ISR70_unity_cabinet_idea
remove_ideas = ISR70_unity
set_temp_variable = { temp_opinion = 5 }
change_the_military_opinion = yes
remove_ideas = ISR70_unity
ISR70_form_unity_coalition = yes
country_event = { id = ISR70.1 days = 1 }
```

### A Disciplined Parliamentary Majority

`ISR70_narrow_cabinet` | x=56, y=2 | 35 days

Prerequisites: (ISR70_knesset).

Exclusive with: ISR70_unity_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

A smaller coalition gives ministers clearer authority over the legislative agenda. Dependence on fewer parliamentary partners leaves the government more exposed to every dispute within its majority.

- Political Power: +75
- Labor Unions Opinion: +10.
- Removes the national spirit "The Unity Government of 1969".
- Removes the national spirit "The Unity Government of 1969".
- National spirit:
- Political Power Gain: +10%
- Stability: -2%
- Opens the corresponding cabinet or municipal event.

```hoi4
add_ideas = ISR70_narrow_cabinet_idea
remove_ideas = ISR70_unity
add_political_power = 75
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
remove_ideas = ISR70_unity
ISR70_form_working_coalition = yes
country_event = { id = ISR70.1 days = 1 }
```

### The Civil Service Commission

`ISR70_civil_service` | x=53, y=3 | 35 days

Prerequisites: (ISR70_unity_cabinet OR ISR70_narrow_cabinet).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Merit examinations and common personnel standards can make a young state less dependent on party appointments. Professional administration will be cheaper to sustain, but the coalition will lose some of the patronage through which it has held together.

- 1 x 25% research bonus: Industry.
- National spirit:
- Bureaucracy Cost: -8%
- Political Power Gain: -2%

```hoi4
add_ideas = ISR70_civil_service_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.25 }
```

### The Comptroller and Parliamentary Oversight

`ISR70_oversight` | x=53, y=4 | 35 days

Prerequisites: (ISR70_civil_service).

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

The State Comptroller must be able to follow public money from the cabinet to local administrations. Independent audits will make officials answer for misuse of their offices.

- Reduces existing MD corruption by one level, down to its minimum.
- National spirit:
- Corruption Cost: -5%

```hoi4
add_ideas = ISR70_oversight_idea
decrease_corruption = yes
```

### Municipal Engineering Offices

`ISR70_local_councils` | x=49, y=4 | 35 days

Prerequisites: (ISR70_civil_service).

Exclusive with: ISR70_central_planning.

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Local councils know which roads and service connections their communities need. Permanent engineering offices will speed municipal works while adding a modest standing administrative commitment.

- Small and Medium Business Owners Opinion: +5.
- National spirit:
- Infrastructure Construction Speed: +15%
- Bureaucracy Cost: +2%

```hoi4
add_ideas = ISR70_local_councils_idea
set_temp_variable = { temp_opinion = 5 }
change_small_medium_business_owners_opinion = yes
```

### Sapir's Development Tenders

`ISR70_central_planning` | x=57, y=4 | 35 days

Prerequisites: (ISR70_civil_service).

Exclusive with: ISR70_local_councils.

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Central tenders can concentrate scarce engineers and capital on projects that private investors would otherwise overlook. The same priority system gives established contractors greater protection from competition.

- 1 x 50% research bonus: Construction.
- National spirit:
- Construction Speed: +7%
- Incoming Investment Cost: +4%

```hoi4
add_ideas = ISR70_central_planning_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### The Unfinished Basic Laws

`ISR70_basic_laws` | x=53, y=5 | 35 days

Prerequisites: (ISR70_oversight).

Artwork: `gfx/interface/goals/coldwar/Adopt_New_Constitiution.tga`.

Strengthen the Basic Law framework and open the constitutional convention decision.

- Political Power: +100
- Stability: +3%
- Unlocks decisions: Convene a Constitutional Convention.

```hoi4
add_political_power = 100
add_stability = 0.03

unlock_decision_tooltip = ISR70_decision_constitutional_convention
```

## Mafdal - Religious Zionism

Parliamentary religious Zionism links public institutions, national service and the religious status quo.

### Religion in the Public State

`ISR70_p0_institution` | x=12, y=18 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/FocusElectHapoelHaMizrachi.dds`.

Anchor religious Zionism in parliamentary institutions and strengthen its public-service organizations.

- Religious Institutions Opinion: +10.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Religious Workshops and Technical Schools

`ISR70_p0_ea` | x=9, y=19 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_eb.

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Mafdal will connect religious study to industrial qualifications. Technical training can broaden skilled employment, while separate educational institutions require additional funding.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Research Speed: +1.5%
- Education Cost: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_research_speed_factor = 0.015 tooltip = ISR70_research_speed_factor_tt }
add_to_variable = { ISR70_p0_education_cost_multiplier_modifier = 0.03 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Teachers for Religious Vocational Schools

`ISR70_p0_ea_deepen` | x=9, y=20 | 49 days

Prerequisites: (ISR70_p0_ea).

Artwork: `gfx/interface/goals/coldwar/School_is_in.tga`.

Religious vocational schools need instructors who can teach industrial skills without abandoning their communities' educational commitments. Preparing those teachers will connect workshop qualifications to the institutions through which Mafdal already organises public life.

- Religious Institutions Opinion: +10.
- While this party governs:
- Monthly Productivity Growth: +0.05
- Education Cost: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
add_to_variable = { ISR70_p0_education_cost_multiplier_modifier = -0.015 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Community Welfare through Religious Councils

`ISR70_p0_eb` | x=11, y=19 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_ea.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Mafdal will use religious councils to coordinate community welfare. Social provision can become less costly, at the price of maintaining a larger local administrative network.

- Religious Institutions Opinion: +10.
- While this party governs:
- Social Spending Cost: -6%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_social_cost_multiplier_modifier = -0.06 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p0_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Services for the Southern Communities

`ISR70_p0_eb_deepen` | x=11, y=20 | 49 days

Prerequisites: (ISR70_p0_eb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Religious welfare organisations cannot serve the development towns without dependable roads and local facilities. Connecting these communities to public services will give the municipal network a practical foundation beyond charitable appeals.

- Stability: +2%
- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### Bnei Akiva and Prepared National Service

`ISR70_p0_ca` | x=13, y=19 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_cb.

Artwork: `gfx/interface/goals/coldwar/conscription.png`.

Religious-Zionist youth organisations can prepare recruits for national service. Quicker mobilisation gives the state trained cadres while increasing expenditure on preparation and personnel.

- Army Experience: +25
- While this party governs:
- Mobilization Speed: +10%
- Personnel Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_mobilization_speed = 0.1 tooltip = mobilization_speed_tt }
add_to_variable = { ISR70_p0_personnel_cost_multiplier_modifier = 0.02 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### A Trained National-Service Cadre

`ISR70_p0_ca_deepen` | x=13, y=20 | 49 days

Prerequisites: (ISR70_p0_ca).

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Bnei Akiva and the service institutions must prepare young people for responsibilities that extend beyond mobilisation. Common training standards will make the religious-Zionist service framework a more dependable part of national defence.

- Army Experience: +20
- While this party governs:
- Army Training Time: -5%
- Recruitable Population Factor: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_training_time_army_factor = -0.05 tooltip = training_time_army_factor_tt }
add_to_variable = { ISR70_p0_recruitable_population_factor = 0.02 tooltip = recruitable_population_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### A Religious Settlement Security Network

`ISR70_p0_cb` | x=15, y=19 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_ca.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Religious Zionist organizations seek a lasting place in the settlement movement. Local organization and defense preparations will shape their contribution to national policy.

- Political Power: +75
- Small and Medium Business Owners Opinion: -5.
- While this party governs:
- Division Defense: +4%
- Supply Consumption: +2%
- Personnel Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_army_defence_factor = 0.04 tooltip = army_defence_factor_tt }
add_to_variable = { ISR70_p0_supply_consumption_factor = 0.02 tooltip = supply_consumption_factor_tt }
add_to_variable = { ISR70_p0_personnel_cost_multiplier_modifier = 0.015 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
set_temp_variable = { temp_opinion = -5 }
change_small_medium_business_owners_opinion = yes
```

### Supply the Border Communities

`ISR70_p0_cb_deepen` | x=15, y=20 | 49 days

Prerequisites: (ISR70_p0_cb).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Border communities need reliable connections to the forces responsible for their defence. Coordinating supplies and local preparations will turn the settlement movement's security claims into an organisation that can sustain its responsibilities.

- Army Experience: +25
- While this party governs:
- Division Organization: +2.5%
- Supply Consumption: -3.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_army_org_factor = 0.025 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p0_supply_consumption_factor = -0.035 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### Religion and the Republic

`ISR70_p0_finish` | x=12, y=21 | 70 days

Prerequisites: (ISR70_p0_ea_deepen OR ISR70_p0_eb_deepen) AND (ISR70_p0_ca_deepen OR ISR70_p0_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectHapoelHaMizrachi.dds`.

Mafdal must show that religious education, community organisation and national service can support the same state. The cabinet's chosen settlement will determine how those obligations are shared without dissolving the movement's distinctive institutions into the larger parties.

- Political Power: +75
- Stability: +3%
- While this party governs:
- Mobilization Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_mobilization_speed = 0.05 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
add_stability = 0.03
```

## Gahal - Herut and the Liberals

Begin must hold together the revisionist and liberal wings of Gahal. A later Likud foundation is a choice, not an anachronistic starting party.

### Hold Herut and the Liberals Together

`ISR70_p1_institution` | x=29, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Coordinate Herut and Liberal representatives around a durable parliamentary leadership.

- Political Power: +75
- Small and Medium Business Owners Opinion: +5.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
set_temp_variable = { temp_opinion = 5 }
change_small_medium_business_owners_opinion = yes
```

### The Liberal Wing's Commercial Programme

`ISR70_p1_ea` | x=26, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_eb.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

Gahal's Liberals will open more opportunities for private enterprise. Incoming investment can expand commerce, while a greater reliance on overseas capital increases exposure to external markets.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -10%
- World-Market Exposure: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p1_mdcw_cw_market_exposure = 0.04 tooltip = ISR70_mdcw_cw_market_exposure_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Commerce on the Tel Aviv Model

`ISR70_p1_ea_deepen` | x=26, y=12 | 49 days

Prerequisites: (ISR70_p1_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

The Liberal wing of Gahal sees commercial employment as a route to prosperity beyond protected enterprises. A new office district in Tel Aviv will give that argument a concrete base of firms, services and technical work.

- +1 Office District in Tel Aviv.
- 1 x 50% research bonus: Industry.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Herut's Strategic Public Enterprises

`ISR70_p1_eb` | x=28, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

Herut will retain selected public enterprises as instruments of national development. Protected production can sustain industrial capacity while making competing commercial investment more difficult.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Factory Output: +5%
- Incoming Investment Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
add_to_variable = { ISR70_p1_receiving_investment_cost_modifier = 0.04 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Strategic Industry in Haifa

`ISR70_p1_eb_deepen` | x=28, y=12 | 49 days

Prerequisites: (ISR70_p1_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Gahal's economic debate need not end with the disposal of every public enterprise. Investment in Haifa will demonstrate whether strategic state ownership can coexist with a cabinet otherwise committed to greater scope for private initiative.

- +1 Civilian Factory in Haifa.
- Labor Unions Opinion: +5.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
set_temp_variable = { temp_opinion = 5 }
change_labour_unions_opinion = yes
```

### The Opposition's Parliamentary Safeguards

`ISR70_p1_ca` | x=30, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_cb.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Gahal can carry its opposition experience into government by defending parliamentary scrutiny. Independent scrutiny will make administration more credible while limiting the executive's immediate political freedom.

- Political Power: +75
- The Military Opinion: -5.
- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Corruption Cost: -3%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_corruption_cost_factor = -0.03 tooltip = corruption_cost_factor_tt }
add_to_variable = { ISR70_p1_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
add_political_power = 75
set_temp_variable = { temp_opinion = -5 }
change_the_military_opinion = yes
```

### Parliamentary Scrutiny of the Executive

`ISR70_p1_ca_deepen` | x=30, y=12 | 49 days

Prerequisites: (ISR70_p1_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Herut's experience in opposition gives parliamentary scrutiny a particular importance within Gahal. Stronger safeguards and a more capable civil administration will require ministers to accept procedures that constrain their own government as well as its opponents.

- Political Power: +50
- While this party governs:
- Bureaucracy Cost: -5%
- Stability: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p1_stability_factor = 0.03 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 50
```

### A Cabinet of Security Priorities

`ISR70_p1_cb` | x=32, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_ca.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Gahal will give military readiness a larger share of the cabinet's attention and budget. Units gain a clearer mandate, while permanent security commitments make military personnel more expensive.

- Army Experience: +30
- While this party governs:
- War Support: +5%
- Personnel Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_war_support_factor = 0.05 tooltip = war_support_factor_tt }
add_to_variable = { ISR70_p1_personnel_cost_multiplier_modifier = 0.025 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### A Cohesive Security Establishment

`ISR70_p1_cb_deepen` | x=32, y=12 | 49 days

Prerequisites: (ISR70_p1_cb).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

A firm security policy requires units that can remain organised and supplied in the field. Gahal will direct attention towards the daily work of sustaining the force, giving its political commitments an operational foundation.

- Army Experience: +20
- While this party governs:
- Production Efficiency Growth: +5%
- Supply Consumption: -3.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_production_factory_efficiency_gain_factor = 0.05 tooltip = ISR70_production_factory_efficiency_gain_factor_tt }
add_to_variable = { ISR70_p1_supply_consumption_factor = -0.035 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### The Conservative Transfer of Power

`ISR70_p1_finish` | x=29, y=13 | 70 days

Prerequisites: (ISR70_p1_ea_deepen OR ISR70_p1_eb_deepen) AND (ISR70_p1_ca_deepen OR ISR70_p1_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Herut and the Liberals must turn an opposition alliance into a government that can endure. Their chosen economic programme and civic settlement will shape a common record of administration, while their separate traditions continue to test the cabinet's cohesion.

- Political Power: +75
- Army Experience: +25
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
add_political_power = 75
```

### Herut and the Liberals: The Identity Question

`ISR70_gahal_identity` | x=23, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Settle the working relationship between Herut and the Liberal Party before choosing a broad alliance or a united party.

- Political Power: +100
- Strengthens this party through the MD popularity system by 3 percentage points before relative rebalancing.
- Unlocks decisions: An Early Alternative Likud Foundation.

```hoi4
add_political_power = 100
set_temp_variable = { party_index = 1 }
set_temp_variable = { party_popularity_increase = 0.03 }
set_temp_variable = { temp_outlook_increase = 0.03 }
change_relative_party_popularity = yes

unlock_decision_tooltip = ISR70_decision_roster_likud
```

### Retain Gahal as a Broad Alliance

`ISR70_gahal_coalition` | x=22, y=12 | 35 days

Prerequisites: (ISR70_gahal_identity).

Exclusive with: ISR70_likud_foundation.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Keep Gahal as a broad alliance with room for its constituent parties.

- Political Power: +75
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Found a United Likud List

`ISR70_likud_foundation` | x=24, y=12 | 35 days

Prerequisites: (ISR70_gahal_identity).

Exclusive with: ISR70_gahal_coalition.

Artwork: `gfx/interface/goals/israel_palestine/Likud.dds`.

Form a united Likud list as an explicit political foundation, increase its support and update its displayed identity.

- Strengthens this party through the MD popularity system by 5 percentage points before relative rebalancing.

```hoi4
set_country_flag = ISR70_likud_founded
set_temp_variable = { party_index = 1 }
set_temp_variable = { party_popularity_increase = 0.05 }
set_temp_variable = { temp_outlook_increase = 0.05 }
change_relative_party_popularity = yes
update_party_name = yes
update_dirty_politicsview_expanded = yes
```

## Independent Liberals

An independent liberal cabinet can promote small business, civil rights or a pragmatic security policy without importing parties from the twenty-first century.

### Liberal Government Responsibility

`ISR70_p2_institution` | x=25, y=18 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Strengthen independent liberal institutions and build business confidence without merging into a larger bloc.

- Political Power: +75
- Small and Medium Business Owners Opinion: +10.

```hoi4
add_political_power = 75
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Independent Credit for Small Firms

`ISR70_p2_ea` | x=22, y=19 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

The Independent Liberals will favour small firms over protected concentrations of capital. Broader access to investment requires officials to supervise a larger number of borrowers and guarantees.

- Small and Medium Business Owners Opinion: +15.
- Industrial Conglomerates Opinion: -5.
- While this party governs:
- Incoming Investment Cost: -10%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p2_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
set_temp_variable = { temp_opinion = -5 }
change_industrial_conglomerates_opinion = yes
```

### Room for Independent Businesses

`ISR70_p2_ea_deepen` | x=22, y=20 | 49 days

Prerequisites: (ISR70_p2_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Independent shopkeepers and service firms need commercial space that is not reserved for the largest political or economic organisations. A Tel Aviv office district will support the Liberals' promise to broaden access to productive private enterprise.

- +1 Office District in Tel Aviv.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Manufacturers in Overseas Markets

`ISR70_p2_eb` | x=24, y=19 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_ea.

Artwork: `gfx/interface/goals/coldwar/export_factories.tga`.

Export-oriented manufacturers will receive the Liberals' support for capital formation. Better returns will connect productive firms more closely to foreign orders and international market risk.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Return on Investment: +0.5%
- World-Market Exposure: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_return_on_investment_modifier = 0.005 tooltip = return_on_investment_modifier_tt }
add_to_variable = { ISR70_p2_mdcw_cw_market_exposure = 0.05 tooltip = ISR70_mdcw_cw_market_exposure_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Export Production in Haifa

`ISR70_p2_eb_deepen` | x=24, y=20 | 49 days

Prerequisites: (ISR70_p2_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Liberal support for enterprise must also reach firms that manufacture rather than merely trade. A modern industrial investment in Haifa will connect capital formation to production methods capable of sustaining competitive export employment.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Civil Rights with Independent Review

`ISR70_p2_ca` | x=26, y=19 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_cb.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Liberal ministers will accept review of their own decisions as the price of enforceable civil rights. More accountable institutions will be harder to direct as a single partisan instrument.

- Political Power: +50
- Stability: +3%
- While this party governs:
- Stability: +2.5%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_stability_factor = 0.025 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p2_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
add_political_power = 50
```

### An Accountable Liberal Civil Service

`ISR70_p2_ca_deepen` | x=26, y=20 | 49 days

Prerequisites: (ISR70_p2_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Civil rights need officials who apply public rules consistently. Auditing the administration will bring the Independent Liberals' constitutional commitments into everyday dealings with the state and reduce the burden of unnecessary bureaucracy.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### A Professional Liberal Defence Policy

`ISR70_p2_cb` | x=28, y=19 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_ca.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

A liberal security policy will rely on trained planners and carefully assessed missions. Better staff preparation will require a small but continuing commitment to professional personnel.

- Army Experience: +30
- While this party governs:
- Planning Speed: +10%
- Personnel Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_planning_speed = 0.1 tooltip = planning_speed_tt }
add_to_variable = { ISR70_p2_personnel_cost_multiplier_modifier = 0.015 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Defensive Analysis and Secure Communications

`ISR70_p2_cb_deepen` | x=28, y=20 | 49 days

Prerequisites: (ISR70_p2_cb).

Artwork: `gfx/interface/goals/israel_palestine/the_research_department.dds`.

A liberal government cannot neglect national defence, but it can insist on careful assessment rather than political reflex. Technical preparation and secure communications will support a security policy grounded in professional judgement.

- 1 x 50% research bonus: Encryption.
- While this party governs:
- Foreign Influence Defense: +8%
- Reconnaissance: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_foreign_influence_defense_modifier = 0.08 tooltip = foreign_influence_defense_modifier_tt }
add_to_variable = { ISR70_p2_recon_factor = 0.04 tooltip = recon_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_encryption uses = 1 bonus = 0.5 }
```

### A Liberal Republic

`ISR70_p2_finish` | x=25, y=21 | 70 days

Prerequisites: (ISR70_p2_ea_deepen OR ISR70_p2_eb_deepen) AND (ISR70_p2_ca_deepen OR ISR70_p2_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

The Independent Liberals seek a place for rights, research and productive enterprise outside the larger political blocs. Their programme must demonstrate that an independent parliamentary voice can administer the state and sustain confidence without surrendering its principles to coalition convenience.

- Stability: +3%
- 1 x 50% research bonus: Electronics.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 1 bonus = 0.5 }
add_stability = 0.03
```

## Alignment - Golda's Israel

The Labor Party and Mapam share the Alignment. Golda Meir governs through a broad coalition, a citizen army and the institutions of Labor Zionism.

### The Labor Zionist Alliance

`ISR70_p3_institution` | x=14, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/FocusElectMapai.dds`.

Reconcile Labor and Mapam around a cabinet programme rooted in the Histadrut and cooperative institutions.

- Labor Unions Opinion: +15.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### The Histadrut Industrial Bargain

`ISR70_p3_ea` | x=11, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_eb.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

The Alignment will modernise Histadrut enterprises through negotiated changes in production. Factory efficiency can improve while a stronger role for organised labour limits unilateral ministerial decisions.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p3_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Modern Workshops for the Histadrut Economy

`ISR70_p3_ea_deepen` | x=11, y=12 | 49 days

Prerequisites: (ISR70_p3_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

The institutions of Labor Zionism must adapt their industrial base to a changing economy. Investment in Haifa will give workers and managers a practical test of modernisation within the enterprises around which the Alignment's social influence has grown.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Monthly Productivity Growth: +0.04

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_productivity_growth_modifier = 0.04 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Kibbutz Workshops and Irrigation

`ISR70_p3_eb` | x=13, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_ea.

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Cooperative farms can combine agricultural production with technical instruction. Faster rural investment requires maintenance, extension staff and a lasting public commitment to the cooperative network.

- 1 x 50% research bonus: Agriculture.
- Farmers Opinion: +10.
- While this party governs:
- Agricultural District Construction Speed: +15%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_speed_agriculture_district_factor = 0.15 tooltip = production_speed_agriculture_district_factor_tt }
add_to_variable = { ISR70_p3_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
```

### Irrigation for Cooperative Development

`ISR70_p3_eb_deepen` | x=13, y=12 | 49 days

Prerequisites: (ISR70_p3_eb).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Cooperative settlement depends on productive land and dependable water rather than political symbolism alone. An irrigated district in the Negev will connect the Alignment's rural institutions to a renewed programme of agricultural development.

- +1 Agricultural District in the Negev.
- Treasury cost on completion: 0.8% of annual GDP.
- While this party governs:
- Production Efficiency Growth: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_factory_efficiency_gain_factor = 0.03 tooltip = ISR70_production_factory_efficiency_gain_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
```

### Development-Town Services before Prestige Projects

`ISR70_p3_ca` | x=15, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_cb.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

The Alignment will direct greater attention to municipal services in the periphery. Dependable services can ease social expenditure, while redirecting engineering capacity slows the expansion of military industry.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -5%
- Military Factory Construction Speed: -3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p3_production_speed_arms_factory_factor = -0.03 tooltip = production_speed_arms_factory_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Public Services in the Development Towns

`ISR70_p3_ca_deepen` | x=15, y=12 | 49 days

Prerequisites: (ISR70_p3_ca).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

The social compact must reach households beyond the established metropolitan centres. Better local connections and public-service provision will give the development towns a more tangible share in the prosperity promised by the Alignment.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Healthcare Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_health_cost_multiplier_modifier = -0.05 tooltip = health_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Negotiations from a Prepared Reserve

`ISR70_p3_cb` | x=17, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_ca.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

The Alignment will sustain military readiness as the basis for its negotiating position. Better organised units give the cabinet options, at the cost of more expensive reserve preparation.

- Army Experience: +30
- While this party governs:
- Division Organization: +4%
- Personnel Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_army_org_factor = 0.04 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p3_personnel_cost_multiplier_modifier = 0.025 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Room for Negotiating Strength

`ISR70_p3_cb_deepen` | x=17, y=12 | 49 days

Prerequisites: (ISR70_p3_cb).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

A cabinet that relies on negotiating strength must retain the freedom to choose its own position. Political consolidation and greater diplomatic independence will help the Alignment conduct talks without treating every outside preference as an instruction.

- Political Power: +100
- While this party governs:
- Foreign Influence Defense: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_foreign_influence_defense_modifier = 0.1 tooltip = foreign_influence_defense_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### A Second Building of Israel

`ISR70_p3_finish` | x=14, y=13 | 70 days

Prerequisites: (ISR70_p3_ea_deepen OR ISR70_p3_eb_deepen) AND (ISR70_p3_ca_deepen OR ISR70_p3_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectMapai.dds`.

Labor and Mapam must reconcile industrial modernisation, cooperative traditions and the needs of communities that feel excluded from both. The government will be judged on whether its chosen programme renews the institutions of Labor Zionism rather than merely preserving their authority.

- Political Power: +100
- Stability: +3%
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
add_stability = 0.03
```

### Labor and Mapam in the Alliance

`ISR70_alignment_balance` | x=8, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Artwork: `gfx/interface/goals/coldwar/FocusElectMapai.dds`.

Negotiate a workable Labor-Mapam balance and improve union confidence inside the Alignment.

- Political Power: +75
- Labor Unions Opinion: +10.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
```

### Renegotiate the Histadrut Production Compact

`ISR70_golda_labour` | x=7, y=12 | 35 days

Prerequisites: (ISR70_alignment_balance).

Exclusive with: ISR70_golda_manager.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

The Alignment can ask Histadrut enterprises to modernise in exchange for negotiated wages and training. More efficient production will require ministers to share decisions with organised labour rather than direct the enterprises alone.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Monthly Productivity Growth: +0.06
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p3_productivity_growth_modifier = 0.06 tooltip = productivity_growth_modifier_tt }
add_to_variable = { ISR70_p3_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Commercial Accounts for Public Enterprises

`ISR70_golda_manager` | x=9, y=12 | 35 days

Prerequisites: (ISR70_alignment_balance).

Exclusive with: ISR70_golda_labour.

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Professional managers can give public enterprises clearer responsibility for production and investment. Stronger commercial discipline will improve output while testing the cabinet's relationship with workers who expect political protection.

- 1 x 50% research bonus: Industry.
- Industrial Conglomerates Opinion: +10.
- Labor Unions Opinion: -5.
- While this party governs:
- Factory Output: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_industrial_capacity_factory = 0.04 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
set_temp_variable = { temp_opinion = -5 }
change_labour_unions_opinion = yes
```

### Hear Development-Town Representatives

`ISR70_golda_panthers` | x=8, y=13 | 35 days

Prerequisites: (ISR70_golda_labour OR ISR70_golda_manager).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

Housing, education and employment grievances give municipal activists reason to approach the cabinet. A hearing can respond to those demands before frustration grows into a wider political confrontation.

- Political Power: +50
- Stability: +3%
- Opens the corresponding cabinet or municipal event.

```hoi4
add_political_power = 50
add_stability = 0.03
country_event = { id = ISR70.20 days = 1 }
```

### Housing with Municipal Services

`ISR70_golda_housing` | x=8, y=14 | 35 days

Prerequisites: (ISR70_golda_panthers).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

New housing must be connected to work, schools and treatment rather than standing alone at the edge of a development town. Maintaining those services will cost more, but dependable links give the next building programme a stronger base.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Infrastructure Construction Speed: +8%
- Social Spending Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_speed_infrastructure_factor = 0.08 tooltip = ISR70_production_speed_infrastructure_factor_tt }
add_to_variable = { ISR70_p3_social_cost_multiplier_modifier = 0.02 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Choose the Alignment Leadership

`ISR70_golda_succession` | x=14, y=14 | 35 days

Prerequisites: (ISR70_p3_finish).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

The governing Alignment can retain Golda Meir or seek a cabinet led by Yitzhak Rabin or Shimon Peres. Parliamentary and party support determine the choice; the government need not wait for a historical succession date.

- Political Power: +75
- Opens a leadership event: retain Golda Meir, choose Yitzhak Rabin, or choose Shimon Peres.

```hoi4
add_political_power = 75
country_event = { id = ISR70.30 days = 1 }
custom_effect_tooltip = ISR70_golda_succession_outcome_tt
```

### Rabin's Professional Cabinet

`ISR70_rabin_cabinet` | x=13, y=15 | 35 days

Prerequisites: (ISR70_golda_succession).

Exclusive with: ISR70_peres_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A Rabin cabinet will place professional responsibility and reserve readiness above a wider system of political appointments. Administrative savings and faster mobilisation will come with a larger continuing personnel commitment.

- Army Experience: +25
- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%
- Mobilization Speed: +5%
- Personnel Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p3_mobilization_speed = 0.05 tooltip = mobilization_speed_tt }
add_to_variable = { ISR70_p3_personnel_cost_multiplier_modifier = 0.015 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
army_experience = 25
```

### Peres's Industrial Cabinet

`ISR70_peres_cabinet` | x=15, y=15 | 35 days

Prerequisites: (ISR70_golda_succession).

Exclusive with: ISR70_rabin_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

A Peres cabinet will give domestic defence engineering a larger place in national investment. Faster military-industrial construction will require funds and contracts that might otherwise have expanded civilian commercial activity.

- 1 x 50% research bonus: Armor.
- 1 x 50% research bonus: Aircraft.
- Treasury cost on completion: 0.4% of annual GDP.
- While this party governs:
- Military Factory Construction Speed: +10%
- Office Construction Speed: -4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_speed_arms_factory_factor = 0.1 tooltip = production_speed_arms_factory_factor_tt }
add_to_variable = { ISR70_p3_production_speed_offices_factor = -0.04 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 1 bonus = 0.5 }
add_tech_bonus = { name = ISR70_research_programme category = CAT_aircraft uses = 1 bonus = 0.5 }
ISR70_pay_0_0040 = yes
```

## Rakah - The Communist Course

A Jewish-Arab communist government is an alternative electoral outcome. Parliamentary socialism and Soviet alignment remain separate decisions.

### A Jewish-Arab Class Alliance

`ISR70_p4_institution` | x=44, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Organize a Jewish-Arab class alliance through workers' organizations and public institutions.

- Stability: +2%
- Labor Unions Opinion: +15.

```hoi4
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
add_stability = 0.02
```

### An Accountable Public-Enterprise Sector

`ISR70_p4_ea` | x=41, y=11 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_eb.

Artwork: `gfx/interface/goals/coldwar/Democratic_Socialism.tga`.

The communist parliamentary cabinet will invest in public enterprises with organised worker representation. Improved industrial routines will require ministers to negotiate rather than issue every instruction directly.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p4_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Workers Trained for Public Enterprise

`ISR70_p4_ea_deepen` | x=41, y=12 | 49 days

Prerequisites: (ISR70_p4_ea).

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Parliamentary communism must show that public ownership can improve work as well as change its formal direction. Technical education and stronger enterprise productivity will give the Jewish-Arab workers' alliance a practical economic record.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.07

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_productivity_growth_modifier = 0.07 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### A State Plan for Industrial Construction

`ISR70_p4_eb` | x=43, y=11 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_ea.

Artwork: `gfx/interface/goals/coldwar/Centrally_Planned_Economy.tga`.

Central planners will concentrate engineering and credit on industrial construction. New production capacity comes ahead of the commercial services that independent firms would otherwise have expanded.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Civilian Industry Construction Speed: +12%
- Office Construction Speed: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_production_speed_industrial_complex_factor = 0.12 tooltip = production_speed_industrial_complex_factor_tt }
add_to_variable = { ISR70_p4_production_speed_offices_factor = -0.05 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### A Public Industrial Base in Haifa

`ISR70_p4_eb_deepen` | x=43, y=12 | 49 days

Prerequisites: (ISR70_p4_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Central planning requires factories capable of carrying out its priorities. A public industrial investment in Haifa will place responsibility for employment and production directly on the government and the workers' organisations that support it.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Common Citizenship and Public Provision

`ISR70_p4_ca` | x=45, y=11 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Equal citizenship will be supported through common public provision. Stable civic institutions require a greater educational commitment if formal equality is to become practical access.

- Political Power: +75
- While this party governs:
- Stability: +4%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_stability_factor = 0.04 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p4_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Equal Access to Municipal Services

`ISR70_p4_ca_deepen` | x=45, y=12 | 49 days

Prerequisites: (ISR70_p4_ca).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Equal citizenship will remain an abstraction if neighbourhoods receive unequal public services. The communist cabinet will strengthen municipal provision so that cooperation between Jewish and Arab workers has an everyday institutional basis.

- Stability: +2%
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.02
```

### Training for a Soviet Supply Relationship

`ISR70_p4_cb` | x=47, y=11 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_ca.

Artwork: `gfx/interface/goals/coldwar/generic_army_cooperation.png`.

A Soviet-oriented security programme will prepare technical personnel for foreign equipment and assistance. Improved support capacity also makes the army more dependent on the continuing foreign relationship.

- Army Experience: +25
- While this party governs:
- Cold War Assistance Effectiveness: +10%
- Imperia Sanction Resistance: -4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_mdcw_cw_support_effectiveness = 0.1 tooltip = ISR70_mdcw_cw_support_effectiveness_tt }
add_to_variable = { ISR70_p4_imp_sanction_resistance = -0.04 tooltip = ISR70_imp_sanction_resistance_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### Technical Preparation for Soviet Armour

`ISR70_p4_cb_deepen` | x=47, y=12 | 49 days

Prerequisites: (ISR70_p4_cb).

Artwork: `gfx/interface/goals/coldwar/FocusImportSovietTanks.dds`.

Closer military cooperation with Moscow requires crews and technical organisations able to understand contemporary armoured designs. Research preparation will develop that competence without assuming that a diplomatic orientation alone delivers finished equipment.

- Army Experience: +20
- 2 x 50% research bonus: Armor.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 2 bonus = 0.5 }
army_experience = 20
```

### A Socialist Peace Settlement

`ISR70_p4_finish` | x=44, y=13 | 70 days

Prerequisites: (ISR70_p4_ea_deepen OR ISR70_p4_eb_deepen) AND (ISR70_p4_ca_deepen OR ISR70_p4_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Rakah's government must hold together its class programme, Jewish-Arab equality and the security choices made during its term. A socialist settlement will depend on capable public institutions and services that make cooperation more durable than a parliamentary declaration.

- Political Power: +75
- 1 x 50% research bonus: Industry.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
add_political_power = 75
```

## Federative Council Left

An explicitly alternative council-socialist movement can decentralize production and negotiate a federal or common civic constitution.

### Communes over Party Headquarters

`ISR70_p5_institution` | x=55, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Give municipal and producers' councils a defined role in a federative political system.

- Political Power: +75
- Labor Unions Opinion: +10.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
```

### Producers' Councils in the Workshops

`ISR70_p5_ea` | x=52, y=11 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

The council left will place workplace training in producers' hands. Sharing practical knowledge can improve industrial efficiency, while negotiating between autonomous workplaces slows central direction.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p5_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Technical Knowledge between Councils

`ISR70_p5_ea_deepen` | x=52, y=12 | 49 days

Prerequisites: (ISR70_p5_ea).

Artwork: `gfx/interface/goals/coldwar/generic_market_socialism.png`.

Autonomous producers' councils need ways to share expertise without surrendering every decision to a central ministry. Joint technical training and industrial research will help local workplaces learn from one another's experience.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.07

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_productivity_growth_modifier = 0.07 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### A Cooperative Investment Federation

`ISR70_p5_eb` | x=54, y=11 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_ea.

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

The federation will pool investment for projects that individual cooperatives cannot undertake. Faster construction requires a standing organisation to settle priorities among its members.

- 1 x 50% research bonus: Agriculture.
- While this party governs:
- Construction Speed: +6%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_production_speed_buildings_factor = 0.06 tooltip = production_speed_buildings_factor_tt }
add_to_variable = { ISR70_p5_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
```

### Cooperative Cultivation in the Negev

`ISR70_p5_eb_deepen` | x=54, y=12 | 49 days

Prerequisites: (ISR70_p5_eb).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

A cooperative federation needs a rural economy alongside its municipal councils. Investment in a Negev agricultural district will give producers a common project whose operation depends on sustained coordination rather than a hierarchy of ministerial orders.

- +1 Agricultural District in the Negev.
- Farmers Opinion: +10.
- Treasury cost on completion: 0.8% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
```

### Municipal Powers in a Federal Charter

`ISR70_p5_ca` | x=56, y=11 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

A federal charter will place defined powers in local institutions. Less routine work falls on the central administration, while national construction programmes must accept additional local negotiation.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Construction Speed: -3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p5_production_speed_buildings_factor = -0.03 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Local Representation within the Federation

`ISR70_p5_ca_deepen` | x=56, y=12 | 49 days

Prerequisites: (ISR70_p5_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

A federal settlement will endure only if communities trust the bodies that represent them. Clear local responsibilities and dependable institutions can protect the agreement against the suspicion that one centre will eventually take back the authority it has promised.

- Political Power: +75
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Shared Civic Services across Communities

`ISR70_p5_cb` | x=58, y=11 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_ca.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Common civic services will give the federation a practical national role. Shared provision can reduce social costs, while coordination across autonomous councils requires more public administration.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -6%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_social_cost_multiplier_modifier = -0.06 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p5_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Shared Services for a Common Republic

`ISR70_p5_cb_deepen` | x=58, y=12 | 49 days

Prerequisites: (ISR70_p5_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

A common civic republic must provide services that residents can use regardless of community. Building that administrative capacity will give the council left's constitutional ambitions a practical test in daily public provision.

- Stability: +2%
- Treasury cost on completion: 0.5% of annual GDP.
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
ISR70_pay_0_0050 = yes
add_stability = 0.02
```

### A Federation of Municipalities

`ISR70_p5_finish` | x=55, y=13 | 70 days

Prerequisites: (ISR70_p5_ea_deepen OR ISR70_p5_eb_deepen) AND (ISR70_p5_ca_deepen OR ISR70_p5_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

The council left seeks a federation held together by cooperation among producers and municipalities. Its chosen economic and civic institutions must provide enough coordination to sustain development while leaving local bodies with a meaningful role in their own affairs.

- Political Power: +75
- Stability: +4%
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.04
add_political_power = 75
```

## Mizrahi Traditionalist Alliance

An alternative traditionalist movement gives development towns an independent voice. Shas remains a later foundation rather than a party transplanted into 1970.

### Represent the Periphery

`ISR70_p6_institution` | x=44, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Build an independent political voice for traditional families and the development towns.

- Stability: +3%
- Religious Institutions Opinion: +10.

```hoi4
add_stability = 0.03
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Family Workshops in the Development Towns

`ISR70_p6_ea` | x=41, y=18 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

The traditionalist alliance will broaden credit for family businesses and craftspeople. Local enterprise gains room to grow while small-loan supervision places new demands on the municipal administration.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p6_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Commercial Space in the Negev

`ISR70_p6_ea_deepen` | x=41, y=19 | 49 days

Prerequisites: (ISR70_p6_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Family firms in the development towns need premises and business services as well as political recognition. A municipal office district will give the traditionalist alliance a concrete investment in the southern communities it claims to represent.

- +1 Office District in the Negev.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Municipal Services for the Periphery

`ISR70_p6_eb` | x=43, y=18 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_ea.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Southern municipalities will receive priority for public works and services. Faster local connections will require a greater continuing commitment to social provision.

- Stability: +3%
- While this party governs:
- Infrastructure Construction Speed: +12%
- Social Spending Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_production_speed_infrastructure_factor = 0.12 tooltip = ISR70_production_speed_infrastructure_factor_tt }
add_to_variable = { ISR70_p6_social_cost_multiplier_modifier = 0.02 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Connect the Southern Development Towns

`ISR70_p6_eb_deepen` | x=43, y=19 | 49 days

Prerequisites: (ISR70_p6_eb).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Municipal development funds must reach communities whose distance from established centres raises the cost of work and public services. Better infrastructure will make those towns a more practical base for households and local employers.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Infrastructure Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_production_speed_infrastructure_factor = 0.1 tooltip = ISR70_production_speed_infrastructure_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### A Traditional Path into Skilled Work

`ISR70_p6_ca` | x=45, y=18 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_cb.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Community teachers and technical schools will offer qualifications without requiring young people to leave their social institutions. The resulting skills will require sustained expenditure on education.

- Religious Institutions Opinion: +10.
- While this party governs:
- Research Speed: +1.5%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_research_speed_factor = 0.015 tooltip = ISR70_research_speed_factor_tt }
add_to_variable = { ISR70_p6_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Teachers and Trades for the Periphery

`ISR70_p6_ca_deepen` | x=45, y=19 | 49 days

Prerequisites: (ISR70_p6_ca).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Young people in traditional communities should not have to choose between retaining their social ties and acquiring useful qualifications. Teacher preparation and vocational education will broaden their opportunities within the development towns.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.07

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_productivity_growth_modifier = 0.07 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Community Institutions at the Bargaining Table

`ISR70_p6_cb` | x=47, y=18 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_ca.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Workers, employers and religious institutions will negotiate the social partnership together. A stable settlement gives each institution influence and leaves the cabinet less freedom to act alone.

- Labor Unions Opinion: +10.
- While this party governs:
- Stability: +4%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_stability_factor = 0.04 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p6_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
```

### Community Welfare Administration

`ISR70_p6_cb_deepen` | x=47, y=19 | 49 days

Prerequisites: (ISR70_p6_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Traditional social partnership needs organisations that can administer help reliably. Strengthening community welfare will allow local institutions to respond to households without making every need depend on a personal connection to a political intermediary.

- Religious Institutions Opinion: +5.
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 5 }
change_the_priesthood_opinion = yes
```

### The Rise of the Development Towns

`ISR70_p6_finish` | x=44, y=20 | 70 days

Prerequisites: (ISR70_p6_ea_deepen OR ISR70_p6_eb_deepen) AND (ISR70_p6_ca_deepen OR ISR70_p6_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

The traditionalist alliance must turn the periphery's political voice into dependable work and services. Its programme will be judged by whether development towns gain institutions of their own, rather than another channel through which established centres distribute favours.

- Political Power: +75
- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

## Development Directorate

An explicitly alternative emergency directorate must choose between professional administration and patronage, and between a civilian transition and enduring presidential power.

### A Limited Directorate

`ISR70_p7_institution` | x=55, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Give the directorate a professional administrative core before choosing its economic and constitutional direction.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Procurement under Engineering Standards

`ISR70_p7_ea` | x=52, y=18 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_eb.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

The directorate will use professional engineering rules to reduce administrative waste. Transparent tendering can make the state less costly while slowing contracts that previously moved through favoured channels.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Bureaucracy Cost: -8%
- Construction Speed: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p7_production_speed_buildings_factor = -0.02 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Industry under Professional Direction

`ISR70_p7_ea_deepen` | x=52, y=19 | 49 days

Prerequisites: (ISR70_p7_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

The directorate's claim to competence will be tested by the enterprises it develops. A public industrial investment in Haifa will give its planners a clear responsibility for production and employment beyond the language of emergency administration.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Corporations for Accelerated Construction

`ISR70_p7_eb` | x=54, y=18 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

The directorate will concentrate construction in state corporations and favoured contractors. Faster industrial development makes the state more dependent on politically protected suppliers.

- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Civilian Industry Construction Speed: +15%
- Corruption Cost: +6%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_production_speed_industrial_complex_factor = 0.15 tooltip = production_speed_industrial_complex_factor_tt }
add_to_variable = { ISR70_p7_corruption_cost_factor = 0.06 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### The State Corporations' Building Programme

`ISR70_p7_eb_deepen` | x=54, y=19 | 49 days

Prerequisites: (ISR70_p7_eb).

Artwork: `gfx/interface/goals/coldwar/industrial_subsidies.tga`.

The directorate will channel industrial investment through the corporations and interests that sustain its authority. New capacity can strengthen production, but the distribution of its benefits will also expose the relationship between economic development and political patronage.

- +1 Civilian Factory in the Negev.
- Industrial Conglomerates Opinion: +10.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### Return the Budget to Parliament

`ISR70_p7_ca` | x=56, y=18 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Restored elections will give public expenditure a broader mandate and expose it to parliamentary scrutiny. Civilian legitimacy will limit the speed with which the directorate can command new projects.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_stability_factor = 0.04 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p7_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = communism elections_allowed = yes }
add_political_power = 75
```

### Audit the Civilian Transition

`ISR70_p7_ca_deepen` | x=56, y=19 | 49 days

Prerequisites: (ISR70_p7_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A promised return to civilian government needs credible scrutiny of the administration that manages it. An effective audit will test the directorate's willingness to submit its record to standards that are independent of its own claims.

- Stability: +3%
- Reduces existing MD corruption by one level, down to its minimum.

```hoi4
decrease_corruption = yes
add_stability = 0.03
```

### The Permanent Presidential Planning Office

`ISR70_p7_cb` | x=58, y=18 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

A permanent presidency can concentrate authority over appointments and planning. Clearer command will be accompanied by a larger protected administrative establishment.

- Political Power: +75
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%
- Bureaucracy Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p7_bureaucracy_cost_multiplier_modifier = 0.04 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = communism elections_allowed = no }
add_political_power = 75
```

### The Presidential Planning Office

`ISR70_p7_cb_deepen` | x=58, y=19 | 49 days

Prerequisites: (ISR70_p7_cb).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

An enduring presidency will bring administration and construction planning closer to the executive. Ministers and technical staff will work through a more concentrated centre, tying the development programme to the president's continued authority. Presidential discretion also leaves more room for politically favoured contracts.

- Political Power: +75
- While this party governs:
- Construction Speed: +6%
- Corruption Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_production_speed_buildings_factor = 0.06 tooltip = production_speed_buildings_factor_tt }
add_to_variable = { ISR70_p7_corruption_cost_factor = 0.015 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### The Directorate State

`ISR70_p7_finish` | x=55, y=20 | 70 days

Prerequisites: (ISR70_p7_ea_deepen OR ISR70_p7_eb_deepen) AND (ISR70_p7_ca_deepen OR ISR70_p7_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

The directorate must now answer for the institutions built under its exceptional authority. Its economic priorities and constitutional choice will determine whether technical administration prepares a civilian settlement or becomes the foundation of a lasting presidential order.

- Political Power: +75
- 1 x 50% research bonus: Construction.
- While this party governs:
- Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_production_speed_buildings_factor = 0.05 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
add_political_power = 75
```

## Islamic Municipal Reform List

A parliamentary organization of Arab municipalities can prioritize trade, charitable provision or a common civic settlement.

### Municipal Interests in the Knesset

`ISR70_p12_institution` | x=71, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Represent municipal interests through parliamentary negotiation and accountable local institutions.

- Political Power: +75
- Stability: +3%

```hoi4
add_stability = 0.03
add_political_power = 75
```

### Commercial Credit for Arab Municipalities

`ISR70_p12_ea` | x=68, y=11 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_eb.

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Municipal representatives will connect local firms to commercial credit. More investment can support employment while requiring additional offices to supervise a wider network of borrowers.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -10%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Commerce for the Northern Municipalities

`ISR70_p12_ea_deepen` | x=68, y=12 | 49 days

Prerequisites: (ISR70_p12_ea).

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

Arab municipalities need a stronger commercial base alongside their public institutions. New office capacity in the north will support local firms and give municipal representatives a practical answer to the demand for productive employment.

- +1 Office District in Haifa.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Local Endowments and Welfare Boards

`ISR70_p12_eb` | x=70, y=11 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_ea.

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Community endowments will help councils organise welfare services. Lower social costs will be accompanied by the administrative work of coordinating public and charitable provision.

- Stability: +2%
- While this party governs:
- Social Spending Cost: -8%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_social_cost_multiplier_modifier = -0.08 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.02
```

### Roads between Communities and Services

`ISR70_p12_eb_deepen` | x=70, y=12 | 49 days

Prerequisites: (ISR70_p12_eb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Municipal welfare organisations cannot compensate indefinitely for weak physical connections. Improvements to roads and service links will help local institutions reach residents and make their public responsibilities easier to sustain.

- Stability: +2%
- +1 Infrastructure level in Haifa.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### A Place in Common Civic Institutions

`ISR70_p12_ca` | x=72, y=11 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Municipal representatives will seek enforceable participation in national institutions. Civic confidence can improve, while ministers must accept a more negotiated parliamentary agenda.

- Political Power: +75
- Stability: +2%
- While this party governs:
- Stability: +3%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_stability_factor = 0.03 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p12_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
add_stability = 0.02
```

### Public Scrutiny of Civic Institutions

`ISR70_p12_ca_deepen` | x=72, y=12 | 49 days

Prerequisites: (ISR70_p12_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Participation in common civic institutions must include the power to question their administration. Public scrutiny will give municipal representatives a way to insist that equal citizenship is reflected in the state's everyday conduct.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Autonomous Municipal Administration

`ISR70_p12_cb` | x=74, y=11 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_ca.

Artwork: `gfx/interface/goals/israel_palestine/gaza_civic_organizations.dds`.

Councils will take responsibility for more routine administration. Central costs can fall while national infrastructure planning must accommodate a larger number of local decisions.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Infrastructure Construction Speed: -4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p12_production_speed_infrastructure_factor = -0.04 tooltip = ISR70_production_speed_infrastructure_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Capable Autonomous Municipal Services

`ISR70_p12_cb_deepen` | x=74, y=12 | 49 days

Prerequisites: (ISR70_p12_cb).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Local autonomy requires more than a legal boundary around municipal powers. Better organised services will give councils the capacity to exercise those powers and build residents' confidence in their community institutions.

- Stability: +4%
- While this party governs:
- Social Spending Cost: -5%
- Infrastructure Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p12_production_speed_infrastructure_factor = 0.05 tooltip = ISR70_production_speed_infrastructure_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.04
```

### A Political Voice for the Municipalities

`ISR70_p12_finish` | x=71, y=13 | 70 days

Prerequisites: (ISR70_p12_ea_deepen OR ISR70_p12_eb_deepen) AND (ISR70_p12_ca_deepen OR ISR70_p12_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

The municipal reform list must translate parliamentary influence into institutions that residents can rely on. Its chosen settlement between common citizenship and local authority will define how Arab municipalities participate in the wider political order.

- Political Power: +75
- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
add_political_power = 75
```

## Agudat Israel and Poalei Agudat

The Orthodox parties defend their communities through parliamentary bargaining, religious education and local social institutions.

### The Orthodox Parliamentary Bloc

`ISR70_p13_institution` | x=82, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Organize an Orthodox parliamentary bloc that negotiates education, community services and religious practice.

- Political Power: +50
- Religious Institutions Opinion: +15.

```hoi4
set_temp_variable = { temp_opinion = 15 }
change_the_priesthood_opinion = yes
add_political_power = 50
```

### Trades alongside the Yeshiva

`ISR70_p13_ea` | x=79, y=11 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_eb.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Orthodox representatives will connect religious learning with practical qualifications. New skills can serve community employment, with separate training arrangements raising educational expenditure.

- Religious Institutions Opinion: +10.
- While this party governs:
- Research Speed: +1.5%
- Education Cost: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_research_speed_factor = 0.015 tooltip = ISR70_research_speed_factor_tt }
add_to_variable = { ISR70_p13_education_cost_multiplier_modifier = 0.03 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Trades alongside Religious Learning

`ISR70_p13_ea_deepen` | x=79, y=12 | 49 days

Prerequisites: (ISR70_p13_ea).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Orthodox families need ways to acquire technical qualifications without abandoning religious study. A sustained training framework will allow community institutions to support productive work while retaining the educational commitments at the heart of the parliamentary bloc.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Community Welfare and Charitable Accounts

`ISR70_p13_eb` | x=81, y=11 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_ea.

Artwork: `gfx/interface/goals/coldwar/Generic_Working_Class_Family.tga`.

Religious welfare organisations will receive a larger role under published accounts. More efficient social provision will require officials to coordinate a more complex network of institutions.

- Religious Institutions Opinion: +10.
- While this party governs:
- Social Spending Cost: -8%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_social_cost_multiplier_modifier = -0.08 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p13_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Professional Community Care

`ISR70_p13_eb_deepen` | x=81, y=12 | 49 days

Prerequisites: (ISR70_p13_eb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Charitable provision must manage increasingly complex health and welfare needs. Better administration will help community organisations use their resources consistently and reduce dependence on improvised arrangements when households require continuing assistance.

- Stability: +3%
- While this party governs:
- Healthcare Cost: -5%
- Education Cost: +1%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_health_cost_multiplier_modifier = -0.05 tooltip = health_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p13_education_cost_multiplier_modifier = 0.01 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Protect the Parliamentary Status Quo

`ISR70_p13_ca` | x=83, y=11 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_cb.

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

The bloc will negotiate religious accommodation through parliament. A steadier coalition will require the state to sustain the separate educational institutions protected by the settlement.

- Religious Institutions Opinion: +15.
- While this party governs:
- Stability: +5%
- Education Cost: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_stability_factor = 0.05 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p13_education_cost_multiplier_modifier = 0.03 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_the_priesthood_opinion = yes
```

### A Parliamentary Religious Settlement

`ISR70_p13_ca_deepen` | x=83, y=12 | 49 days

Prerequisites: (ISR70_p13_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

The religious status quo needs a workable agreement among parties that disagree about the state's character. A durable parliamentary settlement will give Orthodox representatives a basis for defending their institutions while sustaining the government they have helped to form.

- Political Power: +75
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Voluntary Service through Community Institutions

`ISR70_p13_cb` | x=85, y=11 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_ca.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Community organisations will provide civilian placements and local supervision. The programme can support social services while requiring a continuing administrative commitment.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -4%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_social_cost_multiplier_modifier = -0.04 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p13_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Civilian Service Links for Communities

`ISR70_p13_cb_deepen` | x=85, y=12 | 49 days

Prerequisites: (ISR70_p13_cb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Voluntary service will be useful only if it connects participants to real local needs. Better links between development-town communities and their service organisations will give the Orthodox compromise a practical public purpose.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### A Sustainable Religious Compromise

`ISR70_p13_finish` | x=82, y=13 | 70 days

Prerequisites: (ISR70_p13_ea_deepen OR ISR70_p13_eb_deepen) AND (ISR70_p13_ca_deepen OR ISR70_p13_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Agudat Israel and Poalei Agudat must defend their communities while meeting the responsibilities of parliamentary government. Their chosen balance of education, welfare and public service will determine whether religious accommodation can sustain confidence beyond the immediate coalition bargain.

- Political Power: +75
- Stability: +4%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.04
add_political_power = 75
```

## State List and Pragmatic Right

A pragmatic cabinet can professionalize public enterprises or encourage private business, while choosing between defensive pragmatism and territorial negotiations.

### Pragmatic State Leadership

`ISR70_p14_institution` | x=93, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Build a pragmatic state leadership around professional administration and workable parliamentary support.

- Political Power: +100
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### Commercial Discipline in Public Enterprises

`ISR70_p14_ea` | x=90, y=11 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_eb.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

The State List will ask public managers to answer for production and costs. Efficient industrial routines will come with fewer political guarantees for the workers and interests accustomed to them.

- Industrial Conglomerates Opinion: +10.
- Labor Unions Opinion: -5.
- While this party governs:
- Production Efficiency Growth: +7%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_production_factory_efficiency_gain_factor = 0.07 tooltip = ISR70_production_factory_efficiency_gain_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
set_temp_variable = { temp_opinion = -5 }
change_labour_unions_opinion = yes
```

### Professional Management in Haifa

`ISR70_p14_ea_deepen` | x=90, y=12 | 49 days

Prerequisites: (ISR70_p14_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Public enterprises need managers able to answer for production rather than political sponsorship. Industrial investment in Haifa will give the pragmatic right an opportunity to demonstrate that the state's economic role can be administered with clear commercial responsibilities.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### A Competitive Private Sector

`ISR70_p14_eb` | x=92, y=11 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_ea.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

A pragmatic cabinet will open commercial opportunities beyond the established enterprises. Foreign investment can become more attractive while a greater part of development depends on external market conditions.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%
- World-Market Exposure: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p14_mdcw_cw_market_exposure = 0.04 tooltip = ISR70_mdcw_cw_market_exposure_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Commercial Initiative in Tel Aviv

`ISR70_p14_eb_deepen` | x=92, y=12 | 49 days

Prerequisites: (ISR70_p14_eb).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Private commerce offers the pragmatic cabinet another route to employment and development. A Tel Aviv office district will create room for that initiative while testing the government's ability to support enterprise without extending unnecessary administrative control.

- +1 Office District in Tel Aviv.
- Treasury cost on completion: 1.2% of annual GDP.
- While this party governs:
- Return on Investment: +0.3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_return_on_investment_modifier = 0.003 tooltip = return_on_investment_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### A Sustainable Defensive Posture

`ISR70_p14_ca` | x=94, y=11 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_cb.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Professional preparation will support a defensive posture with limited objectives. Better coordination improves defence, while trained readiness continues to cost money between crises.

- Army Experience: +30
- While this party governs:
- Division Defense: +5%
- Personnel Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_army_defence_factor = 0.05 tooltip = army_defence_factor_tt }
add_to_variable = { ISR70_p14_personnel_cost_multiplier_modifier = 0.02 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Sustain a Defensive Posture

`ISR70_p14_ca_deepen` | x=94, y=12 | 49 days

Prerequisites: (ISR70_p14_ca).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

A restrained security policy still requires reliable supplies and a force organised for its assigned tasks. Reducing the practical burden of sustaining that posture will help the cabinet keep readiness within its economic means.

- Army Experience: +20
- While this party governs:
- Supply Consumption: -6%
- Planning Speed: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_supply_consumption_factor = -0.06 tooltip = supply_consumption_factor_tt }
add_to_variable = { ISR70_p14_planning_speed = 0.04 tooltip = planning_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### Cabinet Authority for Territorial Talks

`ISR70_p14_cb` | x=96, y=11 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_ca.

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Negotiators will receive a clear cabinet mandate to explore territorial agreements. Diplomatic freedom will require a domestic political effort that leaves less room for unrelated legislation.

- Political Power: +100
- While this party governs:
- Foreign Influence Defense: +8%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_foreign_influence_defense_modifier = 0.08 tooltip = foreign_influence_defense_modifier_tt }
add_to_variable = { ISR70_p14_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### Public Confidence for Negotiations

`ISR70_p14_cb_deepen` | x=96, y=12 | 49 days

Prerequisites: (ISR70_p14_cb).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Territorial negotiations require a domestic political foundation as well as diplomatic contacts. The pragmatic cabinet will build confidence in its approach so that talks can proceed without every concession becoming a crisis of authority.

- Political Power: +75
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Pragmatism as Statecraft

`ISR70_p14_finish` | x=93, y=13 | 70 days

Prerequisites: (ISR70_p14_ea_deepen OR ISR70_p14_eb_deepen) AND (ISR70_p14_ca_deepen OR ISR70_p14_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

The State List and its partners seek a government judged by workable administration rather than a comprehensive ideological programme. Their record in enterprise management and security policy will determine whether pragmatism can command a stable parliamentary constituency.

- Political Power: +75
- Army Experience: +20
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
add_political_power = 75
```

## Development and Enterprise Bloc

An explicitly alternative alliance of entrepreneurs and municipal notables must choose transparent investment or privileged concessions and patronage.

### An Elite Development Alliance

`ISR70_p15_institution` | x=104, y=10 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

Create a development alliance between municipal notables and productive investment interests.

- Political Power: +50
- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Office Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_production_speed_offices_factor = 0.05 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
add_political_power = 50
```

### Published Contracts for Diaspora Capital

`ISR70_p15_ea` | x=101, y=11 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Investors will receive clear contracts and public reporting. Better use of development capital requires officials to supervise the terms instead of leaving them to personal connections.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Imperia Investment Reward: +10%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_imp_investment_reward = 0.1 tooltip = ISR70_imp_investment_reward_tt }
add_to_variable = { ISR70_p15_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Supervised Investment in Tel Aviv

`ISR70_p15_ea_deepen` | x=101, y=12 | 49 days

Prerequisites: (ISR70_p15_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Diaspora investment must create productive facilities under terms the state can supervise. A new Tel Aviv office district will test whether the development alliance can attract capital while keeping public responsibilities separate from the interests of its sponsors.

- +1 Office District in Tel Aviv.
- 1 x 50% research bonus: Industry.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Concessions for the Development Sponsors

`ISR70_p15_eb` | x=103, y=11 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_ea.

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

The alliance will accelerate development through favoured investors and concessions. Attractive terms will bring investment while raising the public cost of politically protected business.

- Industrial Conglomerates Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -15%
- Corruption Cost: +6%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_receiving_investment_cost_modifier = -0.15 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p15_corruption_cost_factor = 0.06 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_industrial_conglomerates_opinion = yes
```

### The Haifa Industrial Concession

`ISR70_p15_eb_deepen` | x=103, y=12 | 49 days

Prerequisites: (ISR70_p15_eb).

Artwork: `gfx/interface/goals/coldwar/industrial_subsidies.tga`.

Privileged concessions will be justified by their supporters as a faster route to industrial development. Investment in Haifa will give the sponsors new productive capacity while making the political distribution of opportunity increasingly visible.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Independent Review of Investment Contracts

`ISR70_p15_ca` | x=105, y=11 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_cb.

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Independent reviewers will inspect the alliance's contracts. Lower corruption costs will require governing politicians to surrender some control over the allocation of favours.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Corruption Cost: -5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_corruption_cost_factor = -0.05 tooltip = corruption_cost_factor_tt }
add_to_variable = { ISR70_p15_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### A Professional Contract Administration

`ISR70_p15_ca_deepen` | x=105, y=12 | 49 days

Prerequisites: (ISR70_p15_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Transparent investment contracts depend on officials who can inspect and enforce them. A more capable administration will reduce routine burdens while giving the development alliance a credible alternative to informal bargains with favoured investors.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### The Notables' Investment Network

`ISR70_p15_cb` | x=107, y=11 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_ca.

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites2.png`.

The alliance will use municipal notables and investors to consolidate its governing network. Stronger political organisation will carry the cost of public spending shaped by patronage.

- Political Power: +75
- While this party governs:
- Political Power Gain: +10%
- Corruption Cost: +6%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p15_corruption_cost_factor = 0.06 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Construction through the Patronage Network

`ISR70_p15_cb_deepen` | x=107, y=12 | 49 days

Prerequisites: (ISR70_p15_cb).

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

The alliance will consolidate the network of notables and investors through which its building programme operates. This can strengthen its political organisation and delivery capacity, while tying development more closely to continued access to the governing coalition. The privileged network increases the cost of patronage as its reach expands.

- Political Power: +50
- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Office Construction Speed: +10%
- Corruption Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_production_speed_offices_factor = 0.1 tooltip = production_speed_offices_factor_tt }
add_to_variable = { ISR70_p15_corruption_cost_factor = 0.02 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
add_political_power = 50
```

### The Investment State

`ISR70_p15_finish` | x=104, y=13 | 70 days

Prerequisites: (ISR70_p15_ea_deepen OR ISR70_p15_eb_deepen) AND (ISR70_p15_ca_deepen OR ISR70_p15_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

The development alliance must decide what its investment record says about the state it governs. Supervised capital and privileged concessions lead to different relationships between public authority and private wealth, even when both promise growth and new employment.

- Political Power: +75
- 1 x 50% research bonus: Industry.
- While this party governs:
- Imperia Investment Reward: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_imp_investment_reward = 0.05 tooltip = ISR70_imp_investment_reward_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
add_political_power = 75
```

## HaOlam HaZeh - Free Citizens

A secular civil-rights movement can defend a free press and equal citizenship. Radical market reform is a separate alternative policy.

### A Free Press and Political Public Life

`ISR70_p16_institution` | x=71, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Defend a free press and open political organization as the foundation of a secular civil-rights programme.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### Education for a Civilian Economy

`ISR70_p16_ea` | x=68, y=18 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

The civil-rights movement will connect investment access to public technical education. Civilian opportunity will broaden, while educational expenditure rises to support the new qualifications.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -8%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_receiving_investment_cost_modifier = -0.08 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p16_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Qualifications for Civilian Electronics

`ISR70_p16_ea_deepen` | x=68, y=19 | 49 days

Prerequisites: (ISR70_p16_ea).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

A civil-rights economy needs productive opportunities alongside constitutional promises. Technical qualifications and research in civilian electronics will give the Free Citizens movement a development programme that reaches beyond the defence establishment and established political enterprises.

- 1 x 50% research bonus: Electronics.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 1 bonus = 0.5 }
```

### Service Firms beyond Party Patronage

`ISR70_p16_eb` | x=70, y=18 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_ea.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

The movement will simplify entry into services and commercial work. A cheaper central administration will leave municipalities with more responsibility for maintaining local provision.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Social Spending Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p16_social_cost_multiplier_modifier = 0.015 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Commercial Capacity without the Old Bureaucracy

`ISR70_p16_eb_deepen` | x=70, y=19 | 49 days

Prerequisites: (ISR70_p16_eb).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Removing administrative barriers must be followed by opportunities for firms to operate. New commercial offices in Tel Aviv will give the movement's economic alternative a practical base rather than leaving reform confined to the repeal of rules.

- +1 Office District in Tel Aviv.
- Treasury cost on completion: 1.2% of annual GDP.
- While this party governs:
- Office Construction Speed: +8%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_production_speed_offices_factor = 0.08 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### A Secular Public Sphere

`ISR70_p16_ca` | x=72, y=18 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_cb.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

A free public sphere will let citizens challenge ministers and religious authorities. Greater political initiative will provoke resistance among institutions that regard the change as a threat to their established role.

- Stability: +3%
- Religious Institutions Opinion: -10.
- While this party governs:
- Political Power Gain: +8%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_political_power_factor = 0.08 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
set_temp_variable = { temp_opinion = -10 }
change_the_priesthood_opinion = yes
```

### Independent Scrutiny of the Secular State

`ISR70_p16_ca_deepen` | x=72, y=19 | 49 days

Prerequisites: (ISR70_p16_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Secular government must be accountable in practice, including when its ministers claim to act in the name of civil freedom. An independent public audit will test the administration against standards that do not depend on loyalty to the movement.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Stability: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_stability_factor = 0.03 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Power to the Elected Municipalities

`ISR70_p16_cb` | x=74, y=18 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_ca.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Elected municipalities will receive more responsibility for local decisions. Less central administration will be offset by slower agreement on construction that crosses municipal boundaries.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Construction Speed: -3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p16_production_speed_buildings_factor = -0.03 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Municipal Connections in the Negev

`ISR70_p16_cb_deepen` | x=74, y=19 | 49 days

Prerequisites: (ISR70_p16_cb).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Decentralisation will fail if local institutions lack the means to deliver services. Better municipal connections in the Negev will give councils practical responsibilities and resources, rather than merely transferring obligations away from the centre.

- Stability: +2%
- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### A State of Free Citizens

`ISR70_p16_finish` | x=71, y=20 | 70 days

Prerequisites: (ISR70_p16_ea_deepen OR ISR70_p16_eb_deepen) AND (ISR70_p16_ca_deepen OR ISR70_p16_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

HaOlam HaZeh's programme seeks a political public life in which citizens can question the state without losing their place in it. Its chosen economic and municipal institutions must show that civil freedom can also support competent government and useful development.

- Political Power: +75
- 1 x 50% research bonus: Electronics.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 1 bonus = 0.5 }
add_political_power = 75
```

## Landscape and Environment League

An alternative early environmental organization addresses the real development choices of land, water, industry and public infrastructure.

### Development and Landscape Protection

`ISR70_p17_institution` | x=82, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

Create professional institutions for landscape protection, water policy and development planning.

- Political Power: +50
- 1 x 50% research bonus: Agriculture.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
add_political_power = 50
```

### Water Budgets for Cultivation

`ISR70_p17_ea` | x=79, y=18 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_eb.

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

Conservation planners will favour cultivation that can justify its water requirements. Faster agricultural investment will depend on a standing service of surveyors and extension officers.

- 1 x 50% research bonus: Agriculture.
- While this party governs:
- Agricultural District Construction Speed: +15%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_production_speed_agriculture_district_factor = 0.15 tooltip = production_speed_agriculture_district_factor_tt }
add_to_variable = { ISR70_p17_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
```

### Planned Cultivation in the Negev

`ISR70_p17_ea_deepen` | x=79, y=19 | 49 days

Prerequisites: (ISR70_p17_ea).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Agricultural expansion must account for water and land constraints before new districts are laid out. A carefully planned Negev investment will test whether productive cultivation can proceed without treating the landscape as an unlimited reserve for development.

- +1 Agricultural District in the Negev.
- Treasury cost on completion: 0.8% of annual GDP.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
```

### Engineering for Energy Efficiency

`ISR70_p17_eb` | x=81, y=18 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_ea.

Artwork: `gfx/interface/goals/coldwar/generic_electricity.png`.

Cleaner industrial methods will become a technical research priority. Better efficiency will require dedicated laboratories and higher expenditure on scientific education.

- 1 x 50% research bonus: Energy Efficiency.
- While this party governs:
- Research Speed: +2%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
add_to_variable = { ISR70_p17_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.5 }
```

### Industrial Repair and Resource Efficiency

`ISR70_p17_eb_deepen` | x=81, y=19 | 49 days

Prerequisites: (ISR70_p17_eb).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

An environmental programme can improve existing industry rather than simply oppose further building. Better repair and production methods will seek more useful output from the facilities already in place and strengthen the case for technically informed conservation.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Industry Repair Speed: +12%
- Production Efficiency Cap: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_industry_repair_factor = 0.12 tooltip = ISR70_industry_repair_factor_tt }
add_to_variable = { ISR70_p17_production_factory_max_efficiency_factor = 0.04 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Landscape Review before Construction

`ISR70_p17_ca` | x=83, y=18 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_cb.

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

Municipal planners will review land use before approving major works. More careful public administration can improve repair and maintenance, while slowing new construction.

- Political Power: +75
- While this party governs:
- Industry Repair Speed: +10%
- Construction Speed: -3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_industry_repair_factor = 0.1 tooltip = ISR70_industry_repair_factor_tt }
add_to_variable = { ISR70_p17_production_speed_buildings_factor = -0.03 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Conservation in Public Works

`ISR70_p17_ca_deepen` | x=83, y=19 | 49 days

Prerequisites: (ISR70_p17_ca).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Municipal conservation plans need to influence how infrastructure is actually delivered. Applying them to public works will connect the environmental league's proposals to the decisions through which towns use land, services and building resources.

- 1 x 50% research bonus: Infrastructure.
- While this party governs:
- Infrastructure Construction Speed: +15%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_production_speed_infrastructure_factor = 0.15 tooltip = ISR70_production_speed_infrastructure_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_infrastructure uses = 1 bonus = 0.5 }
```

### Public Transport and Healthy Communities

`ISR70_p17_cb` | x=85, y=18 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_ca.

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

The environmental alternative will connect public transport to local health and social provision. Services can become less costly when coordinated, but the network needs additional public administration.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -5%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p17_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Healthier Services for the Development Towns

`ISR70_p17_cb_deepen` | x=85, y=19 | 49 days

Prerequisites: (ISR70_p17_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

The quality of local services is part of the environment in which people live. Investment in development-town infrastructure and health administration will give the league's social programme a practical connection to household needs.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Healthcare Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_health_cost_multiplier_modifier = -0.05 tooltip = health_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### A Livable Development Strategy

`ISR70_p17_finish` | x=82, y=20 | 70 days

Prerequisites: (ISR70_p17_ea_deepen OR ISR70_p17_eb_deepen) AND (ISR70_p17_ca_deepen OR ISR70_p17_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

The environmental league must show that protection of land and water can guide development rather than suspend it. Its record in agriculture, industrial methods and municipal provision will determine whether conservation becomes a dependable part of public administration.

- Stability: +3%
- 1 x 50% research bonus: Energy Efficiency.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.5 }
add_stability = 0.03
```

## Mapam and the Independent Left

Mapam brings the cooperative movement, organized workers and a commitment to Jewish-Arab equality into the debate over Israel's future.

### An Independent Socialist Left

`ISR70_p18_institution` | x=93, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/FocusElectMapam.dds`.

Establish Mapam's independent political institutions after its separation from the Alignment.

- Political Power: +50
- Labor Unions Opinion: +15.

```hoi4
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
add_political_power = 50
```

### Mapam's Cooperative Social Compact

`ISR70_p18_ea` | x=90, y=18 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_eb.

Artwork: `gfx/interface/goals/coldwar/Democratic_Socialism.tga`.

An independent Mapam will defend cooperative production and a broad welfare commitment. Efficient social provision will depend on collective bargaining that limits unilateral cabinet action.

- Labor Unions Opinion: +15.
- While this party governs:
- Social Spending Cost: -8%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_social_cost_multiplier_modifier = -0.08 tooltip = social_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p18_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Cooperative Production in the Negev

`ISR70_p18_ea_deepen` | x=90, y=19 | 49 days

Prerequisites: (ISR70_p18_ea).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Mapam's cooperative commitments require investment in the institutions that sustain rural work. A Negev agricultural district will give the independent left a concrete project through which shared ownership can be judged by practical production and local development.

- +1 Agricultural District in the Negev.
- Treasury cost on completion: 0.8% of annual GDP.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
```

### Schools and Services in the Periphery

`ISR70_p18_eb` | x=92, y=18 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_ea.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Mapam will favour municipal services and education over another round of prestige industrial projects. Administrative savings will accompany a greater educational commitment.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -5%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p18_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Applied Education for the Development Towns

`ISR70_p18_eb_deepen` | x=92, y=19 | 49 days

Prerequisites: (ISR70_p18_eb).

Artwork: `gfx/interface/goals/coldwar/Universities.dds`.

Education must connect neglected communities to the skills and services needed for productive work. Applied teaching and local infrastructure will give Mapam's municipal programme a stronger foundation in the development towns.

- +1 Infrastructure level in the Negev.
- 1 x 50% research bonus: Construction.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### A Parliamentary Mandate for Peace

`ISR70_p18_ca` | x=94, y=18 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_cb.

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

The government will establish a negotiating mandate through public and parliamentary debate. Greater diplomatic independence will cost political attention before an agreement is within reach.

- Political Power: +100
- While this party governs:
- Foreign Influence Defense: +8%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_foreign_influence_defense_modifier = 0.08 tooltip = foreign_influence_defense_modifier_tt }
add_to_variable = { ISR70_p18_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### Elected Scrutiny of a Peace Settlement

`ISR70_p18_ca_deepen` | x=94, y=19 | 49 days

Prerequisites: (ISR70_p18_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

A negotiated peace must rest on public institutions able to scrutinise its terms. Strengthening confidence in elected government will give the independent left a domestic basis for diplomacy without assuming that negotiations themselves guarantee agreement.

- Political Power: +75
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Equal Institutions before a Binational Convention

`ISR70_p18_cb` | x=96, y=18 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_ca.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

A binational constitutional convention would require equal civic institutions and representatives prepared to negotiate a common political settlement.

- Political Power: +100
- While this party governs:
- Political Power Gain: +5%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_political_power_factor = 0.05 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p18_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### Municipal Rights in the Constitutional Convention

`ISR70_p18_cb_deepen` | x=96, y=19 | 49 days

Prerequisites: (ISR70_p18_cb).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A binational constitutional project must address who can question public officials and how communities are represented. Civil rights and municipal accountability will give the proposed settlement a practical institutional content beyond its founding declaration.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -4%
- Stability: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_bureaucracy_cost_multiplier_modifier = -0.04 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p18_stability_factor = 0.025 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Socialism and Equal Rights

`ISR70_p18_finish` | x=93, y=20 | 70 days

Prerequisites: (ISR70_p18_ea_deepen OR ISR70_p18_eb_deepen) AND (ISR70_p18_ca_deepen OR ISR70_p18_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectMapam.dds`.

Mapam's independent programme links cooperative production to Jewish-Arab equality and an alternative diplomatic course. It must demonstrate that these commitments can support the same government, rather than leave social policy, citizenship and peace as separate aspirations.

- Political Power: +75
- Stability: +4%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.04
add_political_power = 75
```

## Maki - Independent Communism

An independent communist cabinet chooses its own relationship between workers' institutions, parliamentary rights and economic planning.

### Independent Workers' Politics

`ISR70_p19_institution` | x=104, y=17 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Build independent communist institutions around workers' representation and Jewish-Arab cooperation.

- Political Power: +75
- Labor Unions Opinion: +10.

```hoi4
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
add_political_power = 75
```

### Joint Jewish-Arab Industrial Training

`ISR70_p19_ea` | x=101, y=18 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Independent communist institutions will organise common worker training across community lines. Factory routines can improve while industrial education becomes a larger public commitment.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Education Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p19_education_cost_multiplier_modifier = 0.025 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Workers' Industry in Haifa

`ISR70_p19_ea_deepen` | x=101, y=19 | 49 days

Prerequisites: (ISR70_p19_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Independent communist policy must create productive work without relying on another bloc's industrial institutions. A Haifa complex will provide a practical base for the workers' programme and expose its managers to the responsibilities of sustained production.

- +1 Civilian Factory in Haifa.
- 1 x 50% research bonus: Industry.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Public Investment through an Elected Plan

`ISR70_p19_eb` | x=103, y=18 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_ea.

Artwork: `gfx/interface/goals/coldwar/generic_market_socialism.png`.

An elected planning process will coordinate public investment. Faster building requires additional staff to reconcile enterprise and municipal priorities.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Construction Speed: +6%
- Bureaucracy Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_production_speed_buildings_factor = 0.06 tooltip = production_speed_buildings_factor_tt }
add_to_variable = { ISR70_p19_bureaucracy_cost_multiplier_modifier = 0.02 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Planning Skills for Public Enterprises

`ISR70_p19_eb_deepen` | x=103, y=19 | 49 days

Prerequisites: (ISR70_p19_eb).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Democratic planning requires information and technical judgement as well as assemblies. Improving those skills will help public enterprises coordinate production while giving workers a clearer understanding of the decisions made in their name.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.07

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_productivity_growth_modifier = 0.07 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Workers' Rights under Ordinary Elections

`ISR70_p19_ca` | x=105, y=18 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Workers' rights will be secured through parliament and ordinary elections. Accountable government can be more stable while leaving ministers less freedom to bypass negotiated procedures.

- Stability: +3%
- Enables ordinary elections.
- While this party governs:
- Stability: +3.5%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_stability_factor = 0.035 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p19_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = neutrality elections_allowed = yes }
add_stability = 0.03
```

### Accountable Workers' Representation

`ISR70_p19_ca_deepen` | x=105, y=19 | 49 days

Prerequisites: (ISR70_p19_ca).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Workers' representatives need institutions through which they can question administrators rather than merely endorse them. Auditing the state will test the independent communist commitment to parliamentary rights and the accountability of its own officeholders.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Limited Powers for Workers' Councils

`ISR70_p19_cb` | x=107, y=18 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_ca.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Workers' councils will receive defined administrative powers alongside the elected legislature. Less central bureaucracy will be accompanied by slower coordination of national building priorities.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Construction Speed: -3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p19_production_speed_buildings_factor = -0.03 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Councils and the Elected Legislature

`ISR70_p19_cb_deepen` | x=107, y=19 | 49 days

Prerequisites: (ISR70_p19_cb).

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Councils cannot provide a durable constitutional alternative if their authority remains undefined. A negotiated division of responsibilities with the elected legislature will give the workers' institutions a place within government while limiting rival claims to unrestricted power.

- Labor Unions Opinion: +10.
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
```

### An Independent Workers' Republic

`ISR70_p19_finish` | x=104, y=20 | 70 days

Prerequisites: (ISR70_p19_ea_deepen OR ISR70_p19_eb_deepen) AND (ISR70_p19_ca_deepen OR ISR70_p19_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Maki's independent course must reconcile workers' organisation with the practical demands of governing a divided society. Its economic and constitutional choices will determine whether public enterprise and political accountability can reinforce one another without submitting to an outside model.

- Stability: +3%
- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
add_stability = 0.03
```

## Free Center and National Alliance

A national opposition can remain parliamentary or seek a presidential mandate. It is not a later national-religious party transplanted into 1970.

### A New National Opposition

`ISR70_p20_institution` | x=119, y=18 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Build a national opposition with enough institutional depth to govern through its chosen constitutional route.

- Political Power: +100
- Army Experience: +15

```hoi4
add_political_power = 100
army_experience = 15
```

### Local Enterprise as a National Programme

`ISR70_p20_ea` | x=116, y=19 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

The national opposition will promote workshops and small businesses in the development towns. New investment opportunities will require a larger network of credit supervision.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%
- Bureaucracy Cost: +1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p20_bureaucracy_cost_multiplier_modifier = 0.015 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Enterprise in the Development Towns

`ISR70_p20_ea_deepen` | x=116, y=20 | 49 days

Prerequisites: (ISR70_p20_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

The national opposition's economic promises must reach smaller firms outside established centres. A commercial office district in the Negev will give the development towns a concrete stake in the proposed national majority.

- +1 Office District in the Negev.
- Treasury cost on completion: 1.2% of annual GDP.
- While this party governs:
- Office Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_production_speed_offices_factor = 0.05 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### A National Pact for Industrial Production

`ISR70_p20_eb` | x=118, y=19 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_ea.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Workers and manufacturers will be brought into a national production pact. Better output depends on negotiated obligations that reduce the cabinet's freedom to settle industrial disputes alone.

- Labor Unions Opinion: +10.
- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Factory Output: +5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
add_to_variable = { ISR70_p20_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### The Haifa Industrial Pact

`ISR70_p20_eb_deepen` | x=118, y=20 | 49 days

Prerequisites: (ISR70_p20_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

A national industrial pact needs productive capacity behind its political commitments. Investment in Haifa will test whether employers and public authorities can carry a common development programme beyond campaign declarations.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### A National Opposition under Parliamentary Rules

`ISR70_p20_ca` | x=120, y=19 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

National populism will accept ordinary elections and parliamentary accountability. A stable constitutional position requires ministers to share power with institutions outside the movement.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%
- Political Power Gain: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_stability_factor = 0.04 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p20_political_power_factor = -0.015 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Oversight of a National Parliamentary Cabinet

`ISR70_p20_ca_deepen` | x=120, y=20 | 49 days

Prerequisites: (ISR70_p20_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A national majority can strengthen government without removing parliamentary restraints. More professional administration and oversight will require the cabinet to accept scrutiny even when it claims a broad popular mandate.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### An Elected Presidency with a Popular Mandate

`ISR70_p20_cb` | x=122, y=19 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

The movement will seek an elected president while preserving competition for office. Concentrated political authority requires a larger presidency and administrative staff.

- Political Power: +100
- Enables ordinary elections.
- While this party governs:
- Political Power Gain: +10%
- Bureaucracy Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p20_bureaucracy_cost_multiplier_modifier = 0.025 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 100
```

### Institutions for the Popular Mandate

`ISR70_p20_cb_deepen` | x=122, y=20 | 49 days

Prerequisites: (ISR70_p20_cb).

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

A presidential popular mandate needs organisations able to sustain national mobilisation beyond an election campaign. Consolidating those institutions will strengthen the executive's political reach and bind its programme more closely to continuing popular support.

- Stability: +3%
- Army Experience: +20
- While this party governs:
- War Support: +4%
- Mobilization Speed: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_war_support_factor = 0.04 tooltip = war_support_factor_tt }
add_to_variable = { ISR70_p20_mobilization_speed = 0.04 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
army_experience = 20
```

### A National Majority Movement

`ISR70_p20_finish` | x=119, y=21 | 70 days

Prerequisites: (ISR70_p20_ea_deepen OR ISR70_p20_eb_deepen) AND (ISR70_p20_ca_deepen OR ISR70_p20_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

The Free Center and its partners seek to turn a national opposition into a governing majority. Their chosen relationship between industry, small enterprise and executive authority will determine whether that majority remains a parliamentary coalition or becomes a presidential movement.

- Political Power: +75
- Stability: +3%
- While this party governs:
- War Support: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_war_support_factor = 0.05 tooltip = war_support_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
add_stability = 0.03
```

## Radical National Front

An explicit alternative radicalization precedes this movement. Autarky, mobilization and an authoritarian security order have real economic consequences.

### Form a Radical Alliance

`ISR70_p21_institution` | x=130, y=18 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Organize a radical national alliance. Its later constitutional choice determines whether it accepts legal limits or an authoritarian order.

- Political Power: +50
- Army Experience: +30

```hoi4
army_experience = 30
add_political_power = 50
```

### A Domestic Arms-Supply Network

`ISR70_p21_ea` | x=127, y=19 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_eb.

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

The radical national alliance will support domestic suppliers to resist external pressure. Greater resilience will protect strategic work while making foreign commercial investment less attractive.

- 1 x 50% research bonus: Infantry Weapons.
- While this party governs:
- Imperia Sanction Resistance: +10%
- Incoming Investment Cost: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_imp_sanction_resistance = 0.1 tooltip = ISR70_imp_sanction_resistance_tt }
add_to_variable = { ISR70_p21_receiving_investment_cost_modifier = 0.05 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_infantry_weapons uses = 1 bonus = 0.5 }
```

### Domestic Arms Production in Tel Aviv

`ISR70_p21_ea_deepen` | x=127, y=20 | 49 days

Prerequisites: (ISR70_p21_ea).

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

An autonomous defence economy requires factories as well as political resolve. A funded arms facility in Tel Aviv will give the radical alliance a concrete industrial commitment, with resources that cannot simultaneously be spent on civilian development.

- +1 Military Factory in Tel Aviv.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Factory Output: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = arms_factory level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### The Reserve Mobilisation Fund

`ISR70_p21_eb` | x=129, y=19 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_ea.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

The alliance will keep more of the reserve establishment ready for mobilisation. Faster call-ups require recurring expenditure on personnel and training.

- Army Experience: +35
- While this party governs:
- Mobilization Speed: +15%
- Personnel Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_mobilization_speed = 0.15 tooltip = mobilization_speed_tt }
add_to_variable = { ISR70_p21_personnel_cost_multiplier_modifier = 0.04 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 35
```

### Training for National Mobilisation

`ISR70_p21_eb_deepen` | x=129, y=20 | 49 days

Prerequisites: (ISR70_p21_eb).

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

A mobilisation fund must prepare people and production to meet its demands. Practical training and support for arms construction will strengthen the radical movement's capacity to organise the country around its military priorities.

- Army Experience: +25
- Treasury cost on completion: 0.8% of annual GDP.
- While this party governs:
- Army Training Time: -5%
- Military Factory Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_training_time_army_factor = -0.05 tooltip = training_time_army_factor_tt }
add_to_variable = { ISR70_p21_production_speed_arms_factory_factor = 0.1 tooltip = production_speed_arms_factory_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
ISR70_pay_0_0080 = yes
army_experience = 25
```

### Legal Limits on the National Movement

`ISR70_p21_ca` | x=131, y=19 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

The alliance will accept ordinary elections and legal limits on political organisation. Civilian confidence can improve, but its leaders will lose some freedom to act through the movement alone.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_stability_factor = 0.04 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p21_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Civil Authority over Radical Politics

`ISR70_p21_ca_deepen` | x=131, y=20 | 49 days

Prerequisites: (ISR70_p21_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Legal limits require civilian institutions with the authority to enforce them. Strengthening those bodies will test whether the radical alliance accepts constitutional restraint when it obstructs the ambitions of its own supporters.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### A Permanent Security Executive

`ISR70_p21_cb` | x=133, y=19 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_ca.

Artwork: `gfx/interface/goals/coldwar/generic_police_state.png`.

An authoritarian security executive will suspend ordinary political competition. Concentrated authority will make the government more forceful while the expanded apparatus consumes public funds.

- Stability: -3%
- Army Experience: +25
- Labor Unions Opinion: -10.
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%
- Bureaucracy Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p21_bureaucracy_cost_multiplier_modifier = 0.04 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
add_stability = -0.03
army_experience = 25
set_temp_variable = { temp_opinion = -10 }
change_labour_unions_opinion = yes
```

### The Security Apparatus of the Radical State

`ISR70_p21_cb_deepen` | x=133, y=20 | 49 days

Prerequisites: (ISR70_p21_cb).

Artwork: `gfx/interface/goals/coldwar/generic_officer.png`.

An authoritarian security course will concentrate attention on the institutions that organise and protect the regime. Military coordination and the security apparatus will become a stronger foundation of political authority, binding mobilisation to the survival of the governing movement. Permanent exceptional powers continue to erode civilian confidence.

- Political Power: +75
- The Military Opinion: +10.
- While this party governs:
- Division Organization: +4%
- Stability: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_army_org_factor = 0.04 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p21_stability_factor = -0.015 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_military_opinion = yes
add_political_power = 75
```

### The Radical State Order

`ISR70_p21_finish` | x=130, y=21 | 70 days

Prerequisites: (ISR70_p21_ea_deepen OR ISR70_p21_eb_deepen) AND (ISR70_p21_ca_deepen OR ISR70_p21_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

The radical alliance has chosen how far mobilisation should reshape public authority and the economy. Its final settlement must give that choice institutional form, whether through accepted legal limits or an enduring security order centred on the movement itself.

- Political Power: +75
- Army Experience: +30
- While this party governs:
- Mobilization Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_mobilization_speed = 0.1 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
add_political_power = 75
```

## Military Emergency Cabinet

A genuine constitutional emergency is required. The armed forces are not treated as an ordinary electoral party in January 1970.

### The Emergency Mandate

`ISR70_p22_institution` | x=119, y=22 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Organize an emergency cabinet around defined military responsibilities and a genuine constitutional crisis.

- Army Experience: +35
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 35
```

### One Emergency Logistics Command

`ISR70_p22_ea` | x=116, y=23 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_eb.

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

The emergency cabinet will centralise logistics and procurement. More efficient field supply will rely on a professional establishment with a larger continuing personnel bill.

- Army Experience: +30
- While this party governs:
- Supply Consumption: -8%
- Personnel Cost: +2.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_supply_consumption_factor = -0.08 tooltip = supply_consumption_factor_tt }
add_to_variable = { ISR70_p22_personnel_cost_multiplier_modifier = 0.025 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Emergency Procurement at Home

`ISR70_p22_ea_deepen` | x=116, y=24 | 49 days

Prerequisites: (ISR70_p22_ea).

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

The emergency cabinet cannot rely entirely on supply decisions made abroad. A military factory in Tel Aviv will strengthen the domestic procurement base while committing resources to the priorities set by the armed forces.

- +1 Military Factory in Tel Aviv.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Military Factory Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_production_speed_arms_factory_factor = 0.1 tooltip = production_speed_arms_factory_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = arms_factory level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Civilian Technocrats in the Emergency Cabinet

`ISR70_p22_eb` | x=118, y=23 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_ea.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Civilian specialists will take responsibility for procurement and industrial planning. A cheaper administration will come with more review before new projects are authorised.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -8%
- Construction Speed: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_bureaucracy_cost_multiplier_modifier = -0.08 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p22_production_speed_buildings_factor = -0.02 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Civilian Standards for Emergency Industry

`ISR70_p22_eb_deepen` | x=118, y=24 | 49 days

Prerequisites: (ISR70_p22_eb).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Civilian engineers bring methods that the emergency administration cannot provide through command alone. Applying their standards to industrial and construction planning will help the cabinet turn urgent orders into projects that can be reliably delivered.

- 1 x 50% research bonus: Industry.
- 1 x 50% research bonus: Construction.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Return the Emergency Budget to Civilian Control

`ISR70_p22_ca` | x=120, y=23 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Ordinary elections will restore a civilian mandate for the emergency budget. Confidence can recover while officers and ministers accept limits on unilateral action.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_stability_factor = 0.05 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p22_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Scrutinise Emergency Procurement

`ISR70_p22_ca_deepen` | x=120, y=24 | 49 days

Prerequisites: (ISR70_p22_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Emergency authority must not make procurement immune to inspection. An audit of contracts and administration will help restore civilian confidence and test whether the cabinet is preparing to return exceptional powers rather than make them permanent.

- Stability: +2%
- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
add_stability = 0.02
```

### Permanent Rule by the Command Council

`ISR70_p22_cb` | x=122, y=23 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_ca.

Artwork: `gfx/interface/goals/coldwar/generic_officer.png`.

The command council will retain authority beyond the emergency. Concentrated political control will require a standing military and administrative establishment.

- The Military Opinion: +10.
- Small and Medium Business Owners Opinion: -10.
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%
- Personnel Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p22_personnel_cost_multiplier_modifier = 0.04 tooltip = personnel_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
set_temp_variable = { temp_opinion = 10 }
change_the_military_opinion = yes
set_temp_variable = { temp_opinion = -10 }
change_small_medium_business_owners_opinion = yes
```

### A Standing Military Command Structure

`ISR70_p22_cb_deepen` | x=122, y=24 | 49 days

Prerequisites: (ISR70_p22_cb).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Permanent military rule requires a command system able to govern beyond the immediate crisis. Consolidating that structure and its mobilisation programme will strengthen the armed forces' hold on responsibilities normally exercised by civilian institutions. Prolonged military government continues to weaken civilian confidence.

- Army Experience: +35
- While this party governs:
- Division Organization: +4%
- Mobilization Speed: +8%
- Stability: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_army_org_factor = 0.04 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p22_mobilization_speed = 0.08 tooltip = mobilization_speed_tt }
add_to_variable = { ISR70_p22_stability_factor = -0.015 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 35
```

### The Future of the Emergency Cabinet

`ISR70_p22_finish` | x=119, y=25 | 70 days

Prerequisites: (ISR70_p22_ea_deepen OR ISR70_p22_eb_deepen) AND (ISR70_p22_ca_deepen OR ISR70_p22_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

The emergency cabinet must now give effect to its constitutional choice. A return to civilian rule and a permanent military order require different institutions, but neither can avoid answering for the procurement and mobilisation programme conducted under exceptional authority.

- Political Power: +75
- Army Experience: +25
- While this party governs:
- Supply Consumption: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_supply_consumption_factor = -0.05 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
add_political_power = 75
```

## Constitutional Hebrew Crown

A freely selected constitutional founding process is required. A crown is an explicit alternative, not a reinterpretation of a modern religious party.

### A Constituent Crown Assembly

`ISR70_p23_institution` | x=130, y=22 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Create a constituent assembly for the explicitly chosen crown settlement. Its powers remain subject to the later constitutional choice.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### Public Endowments for Local Works

`ISR70_p23_ea` | x=127, y=23 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_eb.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Under the alternate crown settlement, public endowments will finance local works. Faster infrastructure development will bring a continuing commitment to social provision.

- Political Power: +75
- While this party governs:
- Infrastructure Construction Speed: +15%
- Social Spending Cost: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_production_speed_infrastructure_factor = 0.15 tooltip = ISR70_production_speed_infrastructure_factor_tt }
add_to_variable = { ISR70_p23_social_cost_multiplier_modifier = 0.02 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Public Works for the Southern Communities

`ISR70_p23_ea_deepen` | x=127, y=24 | 49 days

Prerequisites: (ISR70_p23_ea).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

The proposed crown must establish a public purpose beyond its ceremonial foundation. Infrastructure in the Negev will give its endowments and public-works programme a concrete connection to communities whose support cannot be secured by constitutional symbolism alone.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Industrial Companies under the Crown

`ISR70_p23_eb` | x=129, y=23 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

The crown's industrial alternative will concentrate investment in public companies. Faster industrial construction will compete with private commercial development for capital.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Civilian Industry Construction Speed: +12%
- Incoming Investment Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_production_speed_industrial_complex_factor = 0.12 tooltip = production_speed_industrial_complex_factor_tt }
add_to_variable = { ISR70_p23_receiving_investment_cost_modifier = 0.04 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Royal Industry in Haifa

`ISR70_p23_eb_deepen` | x=129, y=24 | 49 days

Prerequisites: (ISR70_p23_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Royal industrial companies will be expected to support the new settlement through productive investment. A Haifa complex will test whether enterprises associated with the crown can serve a national development purpose rather than merely provide another source of patronage.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Factory Output: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_industrial_capacity_factory = 0.03 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### A Crown Responsible to Parliament

`ISR70_p23_ca` | x=131, y=23 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

A parliamentary crown will accept ordinary elections and a responsible cabinet. A stable constitutional settlement will limit the executive's freedom to direct public affairs alone.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +5%
- Political Power Gain: -2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_stability_factor = 0.05 tooltip = stability_factor_tt }
add_to_variable = { ISR70_p23_political_power_factor = -0.02 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Parliamentary Scrutiny of Crown Expenditure

`ISR70_p23_ca_deepen` | x=131, y=24 | 49 days

Prerequisites: (ISR70_p23_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A parliamentary crown must accept scrutiny of the money and officials attached to it. Clear oversight will make the constitutional settlement credible by applying public standards to the institutions through which royal authority is exercised.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Personal Government from the Crown

`ISR70_p23_cb` | x=133, y=23 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

Personal royal government will suspend ordinary elections and concentrate executive power. A larger household and central administration will make that authority more costly to sustain.

- Political Power: +100
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%
- Bureaucracy Cost: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p23_bureaucracy_cost_multiplier_modifier = 0.04 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
add_political_power = 100
```

### The Crown's Executive Institutions

`ISR70_p23_cb_deepen` | x=133, y=24 | 49 days

Prerequisites: (ISR70_p23_cb).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Personal royal government requires an administration that answers directly to the sovereign. Consolidating executive institutions and national service will give that choice practical force, while making the crown responsible for the results of its own governing programme. Personal executive authority continues to divide public opinion.

- Political Power: +50
- Stability: +3%
- While this party governs:
- Mobilization Speed: +8%
- Stability: -1.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_mobilization_speed = 0.08 tooltip = mobilization_speed_tt }
add_to_variable = { ISR70_p23_stability_factor = -0.015 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
add_political_power = 50
```

### The Crown and Israeli Statehood

`ISR70_p23_finish` | x=130, y=25 | 70 days

Prerequisites: (ISR70_p23_ea_deepen OR ISR70_p23_eb_deepen) AND (ISR70_p23_ca_deepen OR ISR70_p23_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

The new crown must live within the constitutional settlement chosen at its foundation. Its economic and public-service record will determine whether it becomes an institution sustained by parliamentary confidence or the centre of a more personal form of government.

- Political Power: +100
- Stability: +3%
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
add_stability = 0.03
```

## Economy and Imperia

A shared state branch whose institutional achievements survive changes of government.

### An Economic Plan for the Seventies

`ISR70_economic_plan` | x=15, y=0 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/Economic_Protectionism.dds`.

Industry, agriculture and public infrastructure must keep pace with a growing population. A national economic programme will coordinate investment for the coming decade.

- Political Power: +50
- 2 x 50% research bonus: Industry.
- National spirit:
- Factory Output: +5%
- Civilian Industry Productivity: +8%

```hoi4
add_ideas = ISR70_economic_plan_idea
add_political_power = 50
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 2 bonus = 0.5 }
```

### Pumps for the National Water Carrier

`ISR70_water` | x=8, y=1 | 35 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

The National Water Carrier already links northern water sources to the south. New pumping equipment and irrigation connections can support more cultivation, provided the treasury accepts the cost of operating an increasingly complex network.

- 1 x 50% research bonus: Agriculture.
- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Agricultural District Construction Speed: +15%
- Industry Repair Speed: +5%
- Bureaucracy Cost: +1.5%
- Unlocks decisions: Agricultural Advice in Galilee.

```hoi4
add_ideas = ISR70_water_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
ISR70_pay_0_0040 = yes

unlock_decision_tooltip = ISR70_decision_galilee_productivity
```

### Irrigation and Agronomy in the Negev

`ISR70_negev_agriculture` | x=9, y=2 | 49 days

Prerequisites: (ISR70_water).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Water and agricultural engineering can give southern communities a more secure livelihood. New irrigated districts will bring cultivation and employment to the Negev.

- +1 Agricultural District in the Negev.
- Farmers Opinion: +10.
- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Agricultural Productivity: +12%

```hoi4
add_ideas = ISR70_negev_agriculture_idea
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
```

### Mekorot's Workshops and Reservoirs

`ISR70_water_maintenance` | x=6, y=2 | 35 days

Prerequisites: (ISR70_water).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Canals.tga`.

A water network is only as dependable as its pumps, repair crews and reserve storage. Dedicated workshops will restore damaged utilities more quickly and protect investment in irrigation, at the price of a continuing maintenance establishment.

- 1 x 25% research bonus: Energy Efficiency.
- Farmers Opinion: +10.
- National spirit:
- Industry Repair Speed: +15%
- Agricultural District Construction Speed: +5%
- Bureaucracy Cost: +1%
- Agricultural Productivity: +6%

```hoi4
add_ideas = ISR70_water_maintenance_idea
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.25 }
```

### Haifa as an Industrial Center

`ISR70_haifa_industry` | x=15, y=1 | 49 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Expand the civilian industrial base in Haifa and give the new plant a funded capital budget.

- +1 Civilian Factory in Haifa.
- 1 x 50% research bonus: Industry.
- Treasury cost on completion: 1.5% of annual GDP.
- National spirit:
- Factory Output: +5%
- Civilian Industry Productivity: +10%

```hoi4
add_ideas = ISR70_haifa_industry_idea
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Services in Tel Aviv

`ISR70_tel_aviv_offices` | x=22, y=1 | 49 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Commercial offices in Tel Aviv will bring export finance, technical services and accounting into a more productive urban network. The investment strengthens the service economy while competing with industrial and peripheral projects for capital.

- +1 Office District in Tel Aviv.
- Small and Medium Business Owners Opinion: +10.
- Treasury cost on completion: 1.2% of annual GDP.
- National spirit:
- Office Productivity: +12%

```hoi4
add_ideas = ISR70_tel_aviv_offices_idea
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Roads to the Development Towns

`ISR70_negev_roads` | x=9, y=3 | 49 days

Prerequisites: (ISR70_negev_agriculture).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Connect southern development towns with an additional infrastructure level in the Negev.

- +1 Infrastructure level in the Negev.
- 1 x 50% research bonus: Infrastructure.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_infrastructure uses = 1 bonus = 0.5 }
```

### A Reliable Electricity Network

`ISR70_power_grid` | x=15, y=2 | 49 days

Prerequisites: (ISR70_haifa_industry).

Artwork: `gfx/interface/goals/coldwar/1st_Electric_Program.dds`.

Expand fossil electricity generation to serve the growing industrial and office sectors.

- +1 Fossil Fuel Powerplant in Tel Aviv.
- 1 x 50% research bonus: Energy Efficiency.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = fossil_powerplant level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.5 }
```

### Diamonds, Citrus and Precision Workshops

`ISR70_exports` | x=22, y=2 | 35 days

Prerequisites: (ISR70_tel_aviv_offices).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Established exporters can introduce smaller workshops to overseas orders and commercial credit. A stronger export network will draw investment into services while making those firms more sensitive to conditions beyond Israel.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Office Construction Speed: +10%
- Incoming Investment Cost: -6%
- World-Market Exposure: +4%
- Office Productivity: +10%
- Unlocks decisions: Send an Export Delegation.

```hoi4
add_ideas = ISR70_exports_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes

unlock_decision_tooltip = ISR70_decision_export_mission
```

### Produce What the Embargo Denies

`ISR70_import_substitution` | x=13, y=2 | 35 days

Prerequisites: (ISR70_haifa_industry).

Exclusive with: ISR70_export_specialization.

Artwork: `gfx/interface/goals/coldwar/Economic_Protectionism.dds`.

Foreign embargoes expose the vulnerabilities of an economy dependent on imported machinery. Domestic production must be able to sustain essential industries under pressure.

- 1 x 25% research bonus: Industry.
- Industrial Conglomerates Opinion: +5.
- National spirit:
- Imperia Sanction Resistance: +15%
- Production Efficiency Cap: +5%
- Incoming Investment Cost: +6%

```hoi4
add_ideas = ISR70_import_substitution_idea
set_temp_variable = { temp_opinion = 5 }
change_industrial_conglomerates_opinion = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.25 }
```

### An Economy of Specialist Exporters

`ISR70_export_specialization` | x=17, y=2 | 35 days

Prerequisites: (ISR70_haifa_industry).

Exclusive with: ISR70_import_substitution.

Artwork: `gfx/interface/goals/coldwar/export_factories.tga`.

A small domestic market cannot absorb every product of modern engineering. Specialised exporters will gain from international investment and orders, while relying more heavily on access to foreign customers.

- 1 x 25% research bonus: Electronics.
- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Return on Investment: +1%
- Incoming Investment Cost: -10%
- World-Market Exposure: +12%
- Office Productivity: +8%

```hoi4
add_ideas = ISR70_export_specialization_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 1 bonus = 0.25 }
```

### Israel Bonds Development Offices

`ISR70_diaspora_bonds` | x=22, y=3 | 35 days

Prerequisites: (ISR70_exports).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Diaspora savings can support public investment through a credible bond programme. Transparent administration and durable projects will be essential to retaining investors' confidence.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Imperia Investment Reward: +10%
- Bureaucracy Cost: +1.5%
- Unlocks Israel Bonds: Treasury +8% of annual GDP and debt +8% of annual GDP, once. Normal MD debt interest applies.

```hoi4
add_ideas = ISR70_diaspora_bonds_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
unlock_decision_tooltip = ISR70_policy_decision_diaspora_development_bonds
effect_tooltip = {
set_temp_variable = { treasury_change = gdp_total }
multiply_temp_variable = { treasury_change = 0.08 }
modify_treasury_effect = yes
set_temp_variable = { debt_change = gdp_total }
multiply_temp_variable = { debt_change = 0.08 }
modify_debt_effect = yes
}
```

### Scrutinize Investment Contracts

`ISR70_investment_scrutiny` | x=22, y=4 | 35 days

Prerequisites: (ISR70_diaspora_bonds).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Publish investment contracts and subject concessions to independent audits. Public confidence requires clear terms and officials who can be held accountable.

- Reduces existing MD corruption by one level, down to its minimum.
- National spirit:
- Corruption Cost: -5%

```hoi4
add_ideas = ISR70_investment_scrutiny_idea
decrease_corruption = yes
```

### ELTA's Civilian Suppliers

`ISR70_civil_electronics` | x=15, y=3 | 49 days

Prerequisites: (ISR70_power_grid).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Technical workshops and civilian electronics can become a new foundation for industrial development. Skilled engineers will connect university research with practical manufacturing.

- 2 x 50% research bonus: Electronics.
- Treasury cost on completion: 0.5% of annual GDP.
- National spirit:
- Monthly Productivity Growth: +0.2
- Production Efficiency Growth: +8%
- Military Factory Construction Speed: -3%

```hoi4
add_ideas = ISR70_civil_electronics_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 2 bonus = 0.5 }
ISR70_pay_0_0050 = yes
```

### The Technion's New Computing Faculty

`ISR70_technion` | x=15, y=4 | 35 days

Prerequisites: (ISR70_civil_electronics).

Artwork: `gfx/interface/goals/coldwar/Universities.dds`.

The new computer-science faculty gives Israel a place to train specialists for research and industrial work. Sustained support for laboratories and academic staff will broaden technical capability, with higher education becoming a larger public commitment.

- 2 x 50% research bonus: Electronics.
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Research Speed: +2.5%
- Education Cost: +4%

```hoi4
add_ideas = ISR70_technion_idea
ISR70_pay_0_0060 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 2 bonus = 0.5 }
```

### Credit beyond the Large Enterprises

`ISR70_sme_credit` | x=22, y=5 | 35 days

Prerequisites: (ISR70_investment_scrutiny).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Small workshops and family firms need credit outside the networks of the largest public and private employers. Loan guarantees can broaden commercial opportunity, while exposing the public administration to supervision and recovery costs.

- Small and Medium Business Owners Opinion: +15.
- National spirit:
- Incoming Investment Cost: -8%
- Office Construction Speed: +8%
- Bureaucracy Cost: +1.5%
- Office Productivity: +6%
- Unlocks decisions: A Municipal Service Center.

```hoi4
add_ideas = ISR70_sme_credit_idea
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes

unlock_decision_tooltip = ISR70_decision_office_project
```

### Further Industrial Development

`ISR70_civil_plant` | x=15, y=5 | 70 days

Prerequisites: (ISR70_technion).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Establish a civilian industrial complex in the Negev and develop its production methods.

- +1 Civilian Factory in the Negev.
- 1 x 50% research bonus: Industry.
- Treasury cost on completion: 1.5% of annual GDP.
- Unlocks decisions: A Civilian Development Project.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }

unlock_decision_tooltip = ISR70_decision_civil_industry
```

### Sapir's Budget Conference

`ISR70_fiscal_review` | x=22, y=6 | 35 days

Prerequisites: (ISR70_sme_credit).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Defence orders, immigrant housing and industrial investment all compete for the same public funds. A common budget conference will identify priorities before the cabinet chooses between credit restraint and accelerated development.

- Political Power: +50
- 1 x 25% research bonus: Industry.
- Unlocks decisions: Targeted Debt Repayment.

```hoi4
add_political_power = 50
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.25 }

unlock_decision_tooltip = ISR70_decision_debt_repayment
```

### Credit before New Commitments

`ISR70_steady_budget` | x=21, y=7 | 35 days

Prerequisites: (ISR70_fiscal_review).

Exclusive with: ISR70_development_budget.

Artwork: `gfx/interface/goals/coldwar/generic_tackle_corruption.png`.

A credible budget can improve the state's borrowing terms and protect essential services. Restraining new commitments also slows public construction, making the cabinet choose which projects can wait.

- Political Power: +50
- National spirit:
- Interest Rate: -0.5 percentage points
- Construction Speed: -4%
- Bureaucracy Cost: -3%

```hoi4
add_ideas = ISR70_steady_budget_idea
add_political_power = 50
```

### A Treasury for Development

`ISR70_development_budget` | x=23, y=7 | 35 days

Prerequisites: (ISR70_fiscal_review).

Exclusive with: ISR70_steady_budget.

Artwork: `gfx/interface/goals/coldwar/construction.png`.

The treasury will sustain a faster programme of housing, infrastructure and industrial construction. The productive assets will take time to earn their keep, while the new commitments make public credit more expensive.

- 1 x 50% research bonus: Construction.
- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Construction Speed: +10%
- Interest Rate: +0.2 percentage points

```hoi4
add_ideas = ISR70_development_budget_idea
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

## Society, Education and Integration

A shared state branch whose institutional achievements survive changes of government.

### Wages, Prices and the Histadrut

`ISR70_social_contract` | x=37, y=0 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Ministers, employers and the Histadrut can settle wage disputes before they interrupt production. A negotiated compact will make industrial change more predictable, while narrowing the cabinet's freedom to impose a settlement of its own. Agreed recruitment and working arrangements will also bring more adults into regular employment.

- Labor Unions Opinion: +10.
- Industrial Conglomerates Opinion: +5.
- National spirit:
- Production Efficiency Growth: +4%
- Political Power Gain: -1.5%
- Available Workforce: +2%

```hoi4
add_ideas = ISR70_social_contract_idea
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
set_temp_variable = { temp_opinion = 5 }
change_industrial_conglomerates_opinion = yes
```

### ORT Workshops for a Changing Economy

`ISR70_vocational` | x=33, y=1 | 35 days

Prerequisites: (ISR70_social_contract).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Practical instruction can help immigrants and development-town residents enter skilled industrial work. Teacher preparation and workshop equipment will cost more than a general promise of employment, but they give modernisation a broader social foundation. Retraining women and adults outside skilled employment will expand the available labour force.

- 1 x 50% research bonus: Industry.
- Labor Unions Opinion: +10.
- National spirit:
- Monthly Productivity Growth: +0.08
- Education Cost: +3%
- Available Workforce: +3%
- Unlocks decisions: A Negev Vocational Training Project.

```hoi4
add_ideas = ISR70_vocational_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes

unlock_decision_tooltip = ISR70_decision_negev_productivity
```

### Work within Reach of the Development Towns

`ISR70_development_towns` | x=33, y=2 | 35 days

Prerequisites: (ISR70_vocational).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Roads can connect the development towns to jobs and public services instead of leaving housing isolated from the wider economy. The cabinet must fund and maintain those links even where the immediate commercial return is modest. Bringing jobs within reach allows more residents to enter paid employment.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Infrastructure Construction Speed: +10%
- Social Spending Cost: +1.5%
- Available Workforce: +2%

```hoi4
add_ideas = ISR70_development_towns_idea
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Ulpan, Qualifications and a First Job

`ISR70_absorption_reform` | x=33, y=3 | 49 days

Prerequisites: (ISR70_development_towns).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

Language instruction and recognition of qualifications will connect immigrants to work that uses their skills. Housing, job placement and bridging courses can turn an absorption system into a route to regular employment, while the state accepts continuing educational obligations.

- Stability: +3%
- Replaces "Immigration and Development Gaps" with "Integrated Immigration"; removes its +5% social-cost surcharge while retaining population growth.
- National spirit:
- Available Workforce: +4%
- Education Cost: +2.5%
- Unlocks the United Jewish Appeal campaign: Treasury +4% of annual GDP once; social costs +3%, education costs +2%. Requires the diaspora financing programme.

```hoi4
add_ideas = ISR70_absorption_reform_idea
swap_ideas = { remove_idea = ISR70_absorption add_idea = ISR70_integrated_immigration }
add_stability = 0.03
unlock_decision_tooltip = ISR70_policy_decision_uja_absorption_campaign
effect_tooltip = {
set_temp_variable = { treasury_change = gdp_total }
multiply_temp_variable = { treasury_change = 0.04 }
modify_treasury_effect = yes
add_ideas = ISR70_policy_diaspora_absorption_services
}
```

### Negotiate Religion and the State

`ISR70_religion_state` | x=41, y=1 | 35 days

Prerequisites: (ISR70_social_contract).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Open negotiations over personal status, religious education and public service before choosing a settlement.

- Political Power: +75
- Religious Institutions Opinion: +5.

```hoi4
add_political_power = 75
set_temp_variable = { temp_opinion = 5 }
change_the_priesthood_opinion = yes
```

### Renew the Status Quo Agreement

`ISR70_religious_compromise` | x=40, y=2 | 35 days

Prerequisites: (ISR70_religion_state).

Exclusive with: ISR70_civil_marriage.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Religious parties will accept a parliamentary settlement that protects their institutions and communal services. The compromise can steady the coalition, while support for separate educational provision places a lasting claim on public funds.

- Religious Institutions Opinion: +15.
- National spirit:
- Stability: +5%
- Education Cost: +3%

```hoi4
add_ideas = ISR70_religious_compromise_idea
set_temp_variable = { temp_opinion = 15 }
change_the_priesthood_opinion = yes
```

### A Civil Personal-Status Register

`ISR70_civil_marriage` | x=42, y=2 | 35 days

Prerequisites: (ISR70_religion_state).

Exclusive with: ISR70_religious_compromise.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

A civil register would let households settle their personal status outside religious jurisdiction. It will broaden civil choice while bringing the government into direct conflict with those who regard religious authority as part of the founding compact.

- Political Power: +100
- Stability: +3%
- Religious Institutions Opinion: -15.
- National spirit:
- Political Power Gain: +5%
- Stability: -1.5%

```hoi4
add_ideas = ISR70_civil_marriage_idea
add_political_power = 100
add_stability = 0.03
set_temp_variable = { temp_opinion = -15 }
change_the_priesthood_opinion = yes
```

### The Question of Shared Service

`ISR70_national_service` | x=41, y=3 | 35 days

Prerequisites: (ISR70_religious_compromise OR ISR70_civil_marriage).

Artwork: `gfx/interface/goals/coldwar/conscription.png`.

Prepare a common public-service framework and strengthen the institutions that organize it.

- Political Power: +75
- Army Experience: +15

```hoi4
add_political_power = 75
army_experience = 15
```

### Municipal Volunteers and Emergency Aid

`ISR70_volunteer_service` | x=40, y=4 | 35 days

Prerequisites: (ISR70_national_service).

Exclusive with: ISR70_service_expansion.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Volunteer placements can strengthen local emergency and welfare services without extending military obligation. Councils will need supervisors and dependable placements if the programme is to deliver more than a symbolic national gesture.

- Stability: +3%
- Labor Unions Opinion: +5.
- National spirit:
- Social Spending Cost: -5%
- Bureaucracy Cost: +1.5%

```hoi4
add_ideas = ISR70_volunteer_service_idea
add_stability = 0.03
set_temp_variable = { temp_opinion = 5 }
change_labour_unions_opinion = yes
```

### A Wider Call-Up and Training System

`ISR70_service_expansion` | x=42, y=4 | 35 days

Prerequisites: (ISR70_national_service).

Exclusive with: ISR70_volunteer_service.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

A broader service framework can bring trained recruits to their units more quickly. Larger training establishments and more frequent call-ups will also increase the continuing cost of military personnel.

- Army Experience: +35
- National spirit:
- Mobilization Speed: +15%
- Army Training Time: -5%
- Personnel Cost: +3.5%

```hoi4
add_ideas = ISR70_service_expansion_idea
army_experience = 35
```

### Laboratories beyond the Defence Establishment

`ISR70_universities` | x=30, y=2 | 49 days

Prerequisites: (ISR70_vocational).

Artwork: `gfx/interface/goals/coldwar/expand_research_funding.tga`.

Universities in Jerusalem and Haifa need laboratories capable of supporting an independent civilian research agenda. Greater academic capacity will widen the country's technical choices while increasing the cost of maintaining its education system. Qualifications and specialist conversion courses will broaden access to professional work.

- 2 x 50% research bonus: Electronics.
- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Research Speed: +2.5%
- Education Cost: +3.5%
- Available Workforce: +2%

```hoi4
add_ideas = ISR70_universities_idea
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 2 bonus = 0.5 }
```

### Clinics and the New Medical Faculties

`ISR70_public_health` | x=36, y=3 | 35 days

Prerequisites: (ISR70_development_towns).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

More clinics and medical training can bring qualified care beyond the largest urban centres. Better administration will make treatment less costly, but training the additional professionals requires a stronger educational commitment. Dependable treatment and community care also help more adults remain in paid work.

- Stability: +2%
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Healthcare Cost: -8%
- Education Cost: +2%
- Available Workforce: +2%

```hoi4
add_ideas = ISR70_public_health_idea
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

## IDF, Defense Industry and Intelligence

A shared state branch whose institutional achievements survive changes of government.

### The General Staff and the Security Situation

`ISR70_staff` | x=83, y=0 | 14 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Review the General Staff organization and turn the experience of the previous war into usable planning capacity.

- Army Experience: +40
- The Military Opinion: +10.

```hoi4
army_experience = 40
set_temp_variable = { temp_opinion = 10 }
change_the_military_opinion = yes
```

### Miluim: A Trained Reserve

`ISR70_reserve_system` | x=71, y=1 | 35 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/coldwar/AST_upgrade_reserves.png`.

The reserve system depends on civilian specialists arriving at the right units with usable equipment and current training. Reliable mobilisation improves readiness, while employers and the defence budget must absorb more frequent periods of service.

- Army Experience: +25
- Removes the national spirit "Citizen Army and Reserve".
- National spirit:
- Mobilization Speed: +20%
- Division Organization: +4%
- Personnel Cost: +4%
- Unlocks decisions: Conduct a Reserve Exercise, Temporary Reserve Readiness.

```hoi4
add_ideas = ISR70_reserve_system_idea
army_experience = 25
remove_ideas = ISR70_citizen_army

unlock_decision_tooltip = ISR70_decision_reserve_exercise
unlock_decision_tooltip = ISR70_decision_reserve_mobilize
```

### A Fortified Screen and Local Reserves

`ISR70_defensive_depth` | x=69, y=2 | 49 days

Prerequisites: (ISR70_reserve_system).

Exclusive with: ISR70_maneuver.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Prepared positions and rehearsed relief plans can hold a front while reserves assemble. A force organised around that screen will dig in effectively, but its planning routines will be less suited to sudden changes of axis.

- Army Experience: +30
- National spirit:
- Division Defense: +7%
- Maximum Entrenchment: +2
- Planning Speed: -6%

```hoi4
add_ideas = ISR70_defensive_depth_idea
army_experience = 30
```

### Operational Reserves for Mobile War

`ISR70_maneuver` | x=71, y=2 | 49 days

Prerequisites: (ISR70_reserve_system).

Exclusive with: ISR70_defensive_depth.

Artwork: `gfx/interface/goals/coldwar/doctrine_tank_warfare.png`.

Mobile reserves must practise changing direction and concentrating before an opponent can react. Faster planning and armoured movement will give the staff more options, at the cost of a heavier field-supply requirement.

- Army Experience: +40
- National spirit:
- Planning Speed: +15%
- Armor Division Speed: +5%
- Supply Consumption: +4%

```hoi4
add_ideas = ISR70_maneuver_idea
army_experience = 40
```

### Tal's Tank Development Directorate

`ISR70_armour_programme` | x=81, y=1 | 49 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/coldwar/generic_army_tanks3.png`.

Israel Tal advocates a tank designed around the needs of Israeli crews and the lessons of recent wars. Domestic engineering and sustained trials will be necessary to carry that ambition forward.

- Army Experience: +25
- 2 x 50% research bonus: Armor.
- Treasury cost on completion: 1.2% of annual GDP.
- Unlocks decisions: Domestic Equipment Trials.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 2 bonus = 0.5 }
army_experience = 25
ISR70_pay_0_0120 = yes

unlock_decision_tooltip = ISR70_decision_equipment_trials
```

### The Crew Comes First

`ISR70_survivability` | x=80, y=2 | 35 days

Prerequisites: (ISR70_armour_programme).

Exclusive with: ISR70_armour_mobility.

Artwork: `gfx/interface/goals/coldwar/generic_tank_destroyer.png`.

Armour design and field repair will prioritise keeping experienced crews alive. Additional protection can strengthen the force's staying power, with weight and servicing demands limiting its tactical speed.

- 1 x 50% research bonus: Armor.
- National spirit:
- Armor Division Defense: +10%
- Armor Division Speed: -4%

```hoi4
add_ideas = ISR70_survivability_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 1 bonus = 0.5 }
```

### Armoured Tempo and Recovery Teams

`ISR70_armour_mobility` | x=82, y=2 | 35 days

Prerequisites: (ISR70_armour_programme).

Exclusive with: ISR70_survivability.

Artwork: `gfx/interface/goals/coldwar/generic_army_tanks2.png`.

A mobile armoured force needs crews and recovery teams able to sustain rapid movement. Faster vehicles and planning give the staff a different instrument from heavier protection, while consuming more supplies on campaign.

- Army Experience: +35
- National spirit:
- Armor Division Speed: +8%
- Planning Speed: +8%
- Supply Consumption: +2.5%

```hoi4
add_ideas = ISR70_armour_mobility_idea
army_experience = 35
```

### IMI and Domestic Manufacturing

`ISR70_imi` | x=81, y=3 | 70 days

Prerequisites: (ISR70_survivability OR ISR70_armour_mobility).

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

Add an IMI military factory in Tel Aviv and support contemporary infantry-weapons development.

- +1 Military Factory in Tel Aviv.
- 1 x 50% research bonus: Infantry Weapons.
- Treasury cost on completion: 1.5% of annual GDP.
- Unlocks decisions: Expand Defense Manufacturing.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = arms_factory level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_infantry_weapons uses = 1 bonus = 0.5 }

unlock_decision_tooltip = ISR70_decision_armi_project
```

### Artillery and Counter-Battery Reconnaissance

`ISR70_artillery` | x=77, y=2 | 35 days

Prerequisites: (ISR70_reserve_system).

Artwork: `gfx/interface/goals/coldwar/artillery.png`.

Recent fighting has demonstrated the importance of responsive fire support and counter-battery work. The artillery arm needs better training and a coherent development programme.

- Army Experience: +20
- 2 x 50% research bonus: Towed Artillery.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_towed_artillery uses = 2 bonus = 0.5 }
army_experience = 20
```

### Bridging Columns and Field Workshops

`ISR70_engineers` | x=77, y=3 | 35 days

Prerequisites: (ISR70_artillery).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Bridging crews and field workshops can keep a small army moving through damaged routes and difficult terrain. Concentrating specialists on those tasks improves supply economy, while leaving fewer resources for rapid entrenchment.

- Army Experience: +25
- National spirit:
- Reconnaissance: +8%
- Supply Consumption: -6%
- Maximum Entrenchment: -1

```hoi4
add_ideas = ISR70_engineers_idea
army_experience = 25
```

### Selection and Long-Range Patrol Schools

`ISR70_special_forces` | x=77, y=4 | 35 days

Prerequisites: (ISR70_engineers).

Artwork: `gfx/interface/goals/coldwar/ISR_israel_defense_forces.dds`.

Specialist patrols need careful selection, language preparation and sustained field training. Their experience will improve the army's specialist capability, while small professional establishments carry a higher personnel cost.

- Army Experience: +30
- 2 x 50% research bonus: Special Forces Equipment.
- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Special Forces Capacity: +2%
- Personnel Cost: +1.5%

```hoi4
add_ideas = ISR70_special_forces_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_special_forces_equipment uses = 2 bonus = 0.5 }
army_experience = 30
ISR70_pay_0_0040 = yes
```

### The Air Force after the Embargo

`ISR70_air_staff` | x=90, y=1 | 14 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/israel_palestine/goal_ISR_israeli_air_force.dds`.

Reorganize the air staff around sortie generation, training and the lessons of the arms embargo.

- Air Experience: +40
- The Military Opinion: +5.

```hoi4
air_experience = 40
set_temp_variable = { temp_opinion = 5 }
change_the_military_opinion = yes
```

### Conversion Schools for American Aircraft

`ISR70_foreign_aircraft` | x=89, y=2 | 49 days

Prerequisites: (ISR70_air_staff).

Exclusive with: ISR70_local_aircraft.

Artwork: `gfx/interface/goals/coldwar/generic_air_fighter_new.png`.

A reliable American supply channel allows the air force to plan its next generation of aircraft. Conversion training and maintenance arrangements must accompany procurement.

- Air Experience: +25
- 2 x 50% research bonus: Medium Aircraft.
- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Air Mission Efficiency: +4%
- Imperia Sanction Resistance: -4%

```hoi4
add_ideas = ISR70_foreign_aircraft_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_medium_aircraft uses = 2 bonus = 0.5 }
air_experience = 25
ISR70_pay_0_0040 = yes
```

### From Bedek Workshops to Israeli Designs

`ISR70_local_aircraft` | x=91, y=2 | 49 days

Prerequisites: (ISR70_air_staff).

Exclusive with: ISR70_foreign_aircraft.

Artwork: `gfx/interface/goals/coldwar/Generic_Airline_Industry.tga`.

Israel Aircraft Industries can reduce dependence on foreign suppliers. Domestic design teams, workshops and flight trials will require sustained government backing.

- Air Experience: +20
- 2 x 50% research bonus: Aircraft.
- Treasury cost on completion: 1% of annual GDP.
- National spirit:
- Imperia Sanction Resistance: +5%
- Military Factory Construction Speed: -3%

```hoi4
add_ideas = ISR70_local_aircraft_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_aircraft uses = 2 bonus = 0.5 }
air_experience = 20
set_country_flag = ISR70_local_aircraft_programme
ISR70_pay_0_0100 = yes
```

### Spare Engines and Dispersed Workshops

`ISR70_air_maintenance` | x=90, y=3 | 35 days

Prerequisites: (ISR70_foreign_aircraft OR ISR70_local_aircraft).

Artwork: `gfx/interface/goals/coldwar/generic_support_equipment.png`.

Spare engines and dispersed workshops can turn aircraft on the inventory into aircraft ready for missions. Better servicing will improve operational availability, while the air force must maintain a larger technical establishment.

- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Air Mission Efficiency: +6%
- Air Accident Chance: -8%
- Air Force Personnel Cost: +4%

```hoi4
add_ideas = ISR70_air_maintenance_idea
ISR70_pay_0_0060 = yes
if = { limit = { has_country_flag = ISR70_local_aircraft_programme } remove_ideas = ISR70_embargo }
```

### A Resilient Airfield Network

`ISR70_airfield` | x=90, y=4 | 35 days

Prerequisites: (ISR70_air_maintenance).

Artwork: `gfx/interface/goals/coldwar/generic_air_command.png`.

Expand the southern airfield network by two levels and improve its engineering.

- +2 Air Base levels in the Negev.
- 1 x 50% research bonus: Construction.
- Treasury cost on completion: 0.8% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = { type = air_base level = 2 instant_build = yes }
}
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Radar and Contemporary Air Defense

`ISR70_air_defense` | x=74, y=2 | 35 days

Prerequisites: (ISR70_air_staff).

Artwork: `gfx/interface/goals/coldwar/generic_radar_instillation.png`.

Improve contemporary ground-based air defense and military electronics.

- Air Experience: +15
- 1 x 50% research bonus: Anti-Air.
- 1 x 50% research bonus: Military Electronics.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_anti_air uses = 1 bonus = 0.5 }
add_tech_bonus = { name = ISR70_research_programme category = CAT_military_electronics uses = 1 bonus = 0.5 }
air_experience = 15
```

### Secure the Coast and Sea Lanes

`ISR70_naval_staff` | x=97, y=1 | 14 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/israel_palestine/goal_ISR_israeli_navy.dds`.

Reorganize coastal operations and naval staff training.

- Navy Experience: +40
- The Military Opinion: +5.

```hoi4
navy_experience = 40
set_temp_variable = { temp_opinion = 5 }
change_the_military_opinion = yes
```

### Gabriel and the Missile-Boat Flotilla

`ISR70_missile_boats` | x=96, y=2 | 49 days

Prerequisites: (ISR70_naval_staff).

Exclusive with: ISR70_submarines.

Artwork: `gfx/interface/goals/israel_palestine/isr_navy.dds`.

Small missile boats need coordinated manoeuvre and crews able to fight in coastal waters. Concentrating the navy on this flotilla will improve its tactical organisation while requiring intensive training and specialist upkeep.

- Navy Experience: +30
- 2 x 50% research bonus: Corvettes.
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Fleet Coordination: +6%
- Naval Positioning: +4%
- Navy Personnel Cost: +4%

```hoi4
add_ideas = ISR70_missile_boats_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_corvettes uses = 2 bonus = 0.5 }
navy_experience = 30
ISR70_pay_0_0060 = yes
```

### A School for Submarine Crews

`ISR70_submarines` | x=98, y=2 | 49 days

Prerequisites: (ISR70_naval_staff).

Exclusive with: ISR70_missile_boats.

Artwork: `gfx/interface/goals/coldwar/generic_submarine_base.png`.

Submarine operations demand a long apprenticeship in navigation, machinery and concealment. Dedicated instruction will support contemporary submarine research, with the navy accepting higher personnel expenditure for a small force.

- Navy Experience: +30
- 2 x 50% research bonus: Submarines.
- Treasury cost on completion: 0.5% of annual GDP.
- National spirit:
- Fleet Coordination: +4%
- Navy Personnel Cost: +2.5%

```hoi4
add_ideas = ISR70_submarines_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_submarines uses = 2 bonus = 0.5 }
navy_experience = 30
ISR70_pay_0_0050 = yes
```

### Shipbuilding Capacity in Haifa

`ISR70_shipyards` | x=97, y=3 | 70 days

Prerequisites: (ISR70_missile_boats OR ISR70_submarines).

Artwork: `gfx/interface/goals/coldwar/Drydock_Construction.tga`.

Build a funded naval dockyard in Haifa and improve shipbuilding practice.

- Navy Experience: +20
- +1 Naval Dockyard in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = dockyard level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
navy_experience = 20
```

### Mossad and Military Intelligence

`ISR70_intelligence` | x=83, y=5 | 35 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/israel_palestine/isr_mossad.dds`.

Mossad and military intelligence need experienced analysts, secure communications and a clear division of responsibilities. Reliable assessments must inform both diplomacy and defense.

- 1 x 50% research bonus: Decryption.
- Intelligence Community Opinion: +15.
- With La Resistance, creates Mossad if Israel has no intelligence agency.

```hoi4
set_temp_variable = { temp_opinion = 15 }
change_intelligence_community_opinion = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_decryption uses = 1 bonus = 0.5 }
if = { limit = { has_dlc = "La Resistance" NOT = { has_intelligence_agency = yes } } create_intelligence_agency = { name = "Mossad" icon = GFX_intelligence_agency_logo_isr } }
custom_effect_tooltip = ISR70_intelligence_outcome_tt
```

### An Independent Assessment Desk

`ISR70_intelligence_analysis` | x=80, y=6 | 35 days

Prerequisites: (ISR70_intelligence).

Exclusive with: ISR70_intelligence_operations.

Artwork: `gfx/interface/goals/israel_palestine/the_research_department.dds`.

Language specialists and competing assessments can give the cabinet a less complacent picture of its neighbours. Careful evaluation improves reconnaissance and planning, while independent review slows the immediate political use of intelligence.

- 1 x 50% research bonus: Decryption.
- National spirit:
- Reconnaissance: +10%
- Planning Speed: +8%
- Political Power Gain: -2%

```hoi4
add_ideas = ISR70_intelligence_analysis_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_decryption uses = 1 bonus = 0.5 }
```

### Networks beyond the Frontier

`ISR70_intelligence_operations` | x=86, y=6 | 35 days

Prerequisites: (ISR70_intelligence).

Exclusive with: ISR70_intelligence_analysis.

Artwork: `gfx/interface/goals/coldwar/generic_secret_documents.png`.

Operational stations and secure communications can strengthen foreign networks and protect the state from outside influence. The cabinet must sustain the administrative cost and political responsibility of a larger clandestine establishment.

- 1 x 50% research bonus: Encryption.
- Intelligence Community Opinion: +10.
- National spirit:
- Foreign Influence Defense: +15%
- Bureaucracy Cost: +2.5%

```hoi4
add_ideas = ISR70_intelligence_operations_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_encryption uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_intelligence_community_opinion = yes
```

### Civil Defense for Border Communities

`ISR70_civil_defense` | x=66, y=2 | 35 days

Prerequisites: (ISR70_reserve_system).

Artwork: `gfx/interface/goals/coldwar/generic_construct_public_housing.png`.

Build two civilian shelter levels for northern border communities.

- Stability: +2%
- +2 Civilian Shelter levels in Haifa.
- Treasury cost on completion: 0.6% of annual GDP.
- Unlocks decisions: An Additional Civilian Shelter.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 2
	add_building_construction = { type = civilian_shelter level = 2 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02

unlock_decision_tooltip = ISR70_decision_shelters
```

### Readiness within the National Budget

`ISR70_preparedness` | x=71, y=4 | 35 days

Prerequisites: (ISR70_defensive_depth OR ISR70_maneuver) AND (ISR70_air_defense).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

The General Staff must bring reserve call-ups, servicing and civilian protection into one sustainable plan. Better coordination reduces waste in field supply, while the commitment to keep trained forces ready continues in peacetime.

- Army Experience: +30
- Air Experience: +20
- Navy Experience: +15
- National spirit:
- Division Organization: +2.5%
- Supply Consumption: -3.5%
- Personnel Cost: +2%

```hoi4
add_ideas = ISR70_preparedness_idea
army_experience = 30
air_experience = 20
navy_experience = 15
```

## The Cold War and Foreign Policy

A shared state branch whose institutional achievements survive changes of government.

### The Foreign-Policy Situation of 1970

`ISR70_foreign_policy` | x=121, y=0 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/foreign_diplomacy.png`.

Give the foreign ministry a cabinet mandate and open the national diplomatic programme.

- Political Power: +100

```hoi4
add_political_power = 100
```

### Strengthen the Washington Channel

`ISR70_us_channel` | x=111, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/coldwar/ArmIsrael.dds`.

Organize the Washington channel and unlock the American military or civilian cooperation proposal.

- Political Power: +50
- Unlocks decisions: Send a Delivery Proposal to Washington.

```hoi4
add_political_power = 50
set_country_flag = ISR70_us_talks

unlock_decision_tooltip = ISR70_decision_talks_us
```

### Negotiate Security Cooperation

`ISR70_us_security` | x=110, y=2 | 35 days

Prerequisites: (ISR70_us_channel).

Exclusive with: ISR70_us_civil.

Artwork: `gfx/interface/goals/coldwar/ArmIsrael.dds`.

An agreement with Washington gives military planners a dependable basis for cooperation. Training and procurement offices must turn diplomatic commitments into lasting working arrangements.

- Army Experience: +25
- Air Experience: +25
- National spirit:
- Cold War Assistance Effectiveness: +10%

```hoi4
add_ideas = ISR70_us_security_idea
army_experience = 25
air_experience = 25
```

### Negotiate Civilian Economic Cooperation

`ISR70_us_civil` | x=112, y=2 | 35 days

Prerequisites: (ISR70_us_channel).

Exclusive with: ISR70_us_security.

Artwork: `gfx/interface/goals/coldwar/generic_positive_trade_relations_gold.png`.

Implement an accepted civilian agreement through investment access and industrial research.

- 1 x 50% research bonus: Industry.
- National spirit:
- Incoming Investment Cost: -15%

```hoi4
add_ideas = ISR70_us_civil_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Approach Paris Again

`ISR70_france_channel` | x=116, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Ask Paris to reopen a commercial channel. The French government must accept before European cooperation can deepen.

- Political Power: +50
- Sends France a commercial proposal. France may accept or decline. Acceptance is required for the European trade focus.

```hoi4
add_political_power = 50
set_country_flag = ISR70_france_talks
if = { limit = { FRA = { exists = yes } } FRA = { country_event = { id = ISR70.45 days = 1 } } }
custom_effect_tooltip = ISR70_france_channel_outcome_tt
```

### Develop European Export Markets

`ISR70_european_trade` | x=116, y=2 | 35 days

Prerequisites: (ISR70_france_channel).

Artwork: `gfx/interface/goals/coldwar/europe_trade.tga`.

Use the accepted European trade channel to improve investment returns and support commercial institutions.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Return on Investment: +0.5%
- Office Construction Speed: +10%

```hoi4
add_ideas = ISR70_european_trade_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### A Cautious Opening to Moscow

`ISR70_soviet_channel` | x=121, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Open a cautious channel to Moscow and unlock a proposal on emigration and diplomatic contacts.

- Political Power: +50
- Unlocks decisions: Send a Dialogue Proposal to Moscow.

```hoi4
add_political_power = 50
set_country_flag = ISR70_soviet_talks

unlock_decision_tooltip = ISR70_decision_talks_sov
```

### Emigration and Diplomatic Contacts

`ISR70_soviet_dialogue` | x=121, y=2 | 35 days

Prerequisites: (ISR70_soviet_channel).

Artwork: `gfx/interface/goals/coldwar/Generic_Refugee_Focus.tga`.

An agreed emigration framework opens a new chapter in relations with Moscow. Israel must prepare housing, employment and local services for the families who arrive.

- Political Power: +50
- Stability: +3%

```hoi4
add_stability = 0.03
add_political_power = 50
```

### An Independent Diplomacy

`ISR70_independent_diplomacy` | x=126, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Maintain independent negotiating room and protect domestic decision making against foreign influence.

- Political Power: +75
- National spirit:
- Foreign Influence Defense: +10%

```hoi4
add_ideas = ISR70_independent_diplomacy_idea
add_political_power = 75
```

### Maintain African Contacts

`ISR70_africa_contacts` | x=125, y=2 | 35 days

Prerequisites: (ISR70_independent_diplomacy).

Artwork: `gfx/interface/goals/coldwar/african_diplomacy.dds`.

Technical missions abroad offer cooperation in agriculture, training and public works. Lasting partnerships will depend on useful expertise and reliable commitments.

- 1 x 50% research bonus: Agriculture.
- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Cold War Assistance Effectiveness: +10%

```hoi4
add_ideas = ISR70_africa_contacts_idea
ISR70_pay_0_0040 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
```

### Confidential Talks with Amman

`ISR70_jordan_backchannel` | x=131, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/israel_palestine/israel_jordan_flags.dds`.

Send a confidential border proposal to Amman. Jordan decides whether the channel becomes an agreement.

- Political Power: +50
- Sends Jordan a border-talks proposal. Jordan may accept or decline; no territory changes hands.

```hoi4
add_political_power = 50
set_country_flag = ISR70_jordan_talks
if = { limit = { JOR = { exists = yes } } JOR = { country_event = { id = ISR70.77 days = 1 } } }
custom_effect_tooltip = ISR70_jordan_backchannel_outcome_tt
```

### Relations with the Shah's Iran

`ISR70_iran_contacts` | x=135, y=1 | 35 days

Prerequisites: (ISR70_foreign_policy).

Artwork: `gfx/interface/goals/coldwar/Oil_Deal.dds`.

The relationship with the Shah's Iran offers opportunities in supply and commerce. A lasting arrangement will require agreement in Tehran as well as Jerusalem.

- Political Power: +50
- Sends Iran a supply proposal. Iranian acceptance under a compatible government unlocks Oil-Supply Security.

```hoi4
add_political_power = 50
set_country_flag = ISR70_iran_talks
if = { limit = { PER = { exists = yes } } PER = { country_event = { id = ISR70.76 days = 1 } } }
custom_effect_tooltip = ISR70_iran_contacts_outcome_tt
```

### Stocks for the Iranian Supply Route

`ISR70_oil_security` | x=135, y=2 | 35 days

Prerequisites: (ISR70_iran_contacts).

Artwork: `gfx/interface/goals/coldwar/Oil_Pipelines.tga`.

An accepted Iranian arrangement can support fuel stocks and more reliable supply planning. Storage and distribution reduce vulnerability to interruption, but dedicated facilities will require continuing administration.

- 1 x 50% research bonus: Fuel Refining.
- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Imperia Sanction Resistance: +8%
- Fuel Gain: +5%
- Bureaucracy Cost: +1.5%

```hoi4
add_ideas = ISR70_oil_security_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_fuel_refining uses = 1 bonus = 0.5 }
ISR70_pay_0_0040 = yes
```

### Ambiguity or International Transparency

`ISR70_nuclear_policy` | x=128, y=2 | 35 days

Prerequisites: (ISR70_independent_diplomacy).

Artwork: `gfx/interface/goals/coldwar/generic_secret_documents.png`.

Review the diplomatic implications of ambiguity and international transparency before choosing a policy.

- Political Power: +75

```hoi4
add_political_power = 75
```

### Amimut and Cabinet Discipline

`ISR70_keep_ambiguity` | x=127, y=3 | 35 days

Prerequisites: (ISR70_nuclear_policy).

Exclusive with: ISR70_nuclear_transparency.

Artwork: `gfx/interface/goals/coldwar/Nuclear_Research_Lab.png`.

Discretion preserves freedom of action in a hostile region. The cabinet will reaffirm a policy of strategic ambiguity and tightly controlled diplomatic communication.

- Political Power: +50
- Removes the national spirit "Nuclear Ambiguity".
- National spirit:
- Foreign Influence Defense: +12%
- Research Speed: -1%

```hoi4
add_ideas = ISR70_keep_ambiguity_idea
remove_ideas = ISR70_ambiguity
add_political_power = 50
```

### A Civilian Research Accounting

`ISR70_nuclear_transparency` | x=129, y=3 | 35 days

Prerequisites: (ISR70_nuclear_policy).

Exclusive with: ISR70_keep_ambiguity.

Artwork: `gfx/interface/goals/coldwar/Nuclear_Research_Lab.png`.

Civilian nuclear cooperation offers a different diplomatic course. Greater openness would place international research and peaceful technical exchanges at the center of policy.

- 2 x 50% research bonus: Nuclear Reactors.
- Removes the national spirit "Nuclear Ambiguity".
- National spirit:
- Research Speed: +2.5%
- Foreign Influence Defense: -5%

```hoi4
add_ideas = ISR70_nuclear_transparency_idea
remove_ideas = ISR70_ambiguity
add_tech_bonus = { name = ISR70_research_programme category = CAT_nuclear_reactors uses = 2 bonus = 0.5 }
```

## Suez, Borders and Peace

A shared state branch whose institutional achievements survive changes of government.

### Assess the Suez Front

`ISR70_suez` | x=111, y=7 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Egypt-Israeli_Tension.dds`.

Assess the Suez front and give the cabinet a concrete military and political assessment.

- Political Power: +75
- Army Experience: +25

```hoi4
army_experience = 25
add_political_power = 75
```

### Limit the Conflict

`ISR70_limited_attrition` | x=106, y=8 | 35 days

Prerequisites: (ISR70_suez).

Exclusive with: ISR70_deep_raids.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Limit the conflict to a defensive posture with better field coordination and manageable supply use.

- Army Experience: +20
- National spirit:
- Division Defense: +5%
- Supply Consumption: -5%

```hoi4
add_ideas = ISR70_limited_attrition_idea
army_experience = 20
```

### Increase Military Pressure

`ISR70_deep_raids` | x=110, y=8 | 35 days

Prerequisites: (ISR70_suez).

Exclusive with: ISR70_limited_attrition.

Artwork: `gfx/interface/goals/coldwar/generic_air_fighter_new.png`.

Deep raids promise to disrupt the enemy's preparations beyond the front line. The cabinet must commit aircraft and trained personnel while accepting the diplomatic consequences of escalation.

- Army Experience: +20
- Air Experience: +35
- Treasury cost on completion: 0.6% of annual GDP.
- Imperia Cold War Tension: +2 points.

```hoi4
air_experience = 35
army_experience = 20
ISR70_pay_0_0060 = yes
set_temp_variable = { mdcw_cw_tension_delta = 2 }
custom_effect_tooltip = ISR70_cold_war_tension_tt
hidden_effect = { mdcw_cw_add_tension = yes }
```

### Open Ceasefire Negotiations

`ISR70_rogers` | x=114, y=8 | 35 days

Prerequisites: (ISR70_suez).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

The cabinet can propose a ceasefire on terms it is willing to defend. A military posture and negotiations can proceed in parallel. Egypt decides whether to accept the proposal; broader territorial questions remain for separate talks.

- Political Power: +50
- Opens a cabinet proposal for ceasefire negotiations. Egyptian acceptance is required for the agreement.

```hoi4
add_political_power = 50
set_country_flag = ISR70_rogers_offer
country_event = { id = ISR70.10 days = 1 }
custom_effect_tooltip = ISR70_rogers_outcome_tt
```

### A Controlled Ceasefire

`ISR70_ceasefire` | x=114, y=9 | 35 days

Prerequisites: (ISR70_rogers).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Consolidate an accepted ceasefire, remove the starting War of Attrition costs and restore public confidence.

- Political Power: +50
- Stability: +5%
- Removes the national spirit "The War of Attrition".

```hoi4
remove_ideas = ISR70_attrition
add_stability = 0.05
add_political_power = 50
ISR70_end_attrition = yes
```

### Forward Defensive Readiness

`ISR70_armed_stalemate` | x=108, y=9 | 35 days

Prerequisites: (ISR70_limited_attrition OR ISR70_deep_raids).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Prepared positions, supply reserves and trained headquarters can support the cabinet during a confrontation or while negotiations proceed. Maintaining the posture demands a continuing personnel commitment.

- Army Experience: +30
- National spirit:
- Division Defense: +8%
- Personnel Cost: +3%

```hoi4
add_ideas = ISR70_armed_stalemate_idea
army_experience = 30
```

### Set the Territorial Programme

`ISR70_territorial_policy` | x=125, y=7 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

The cabinet must decide how to administer the territories under its control and what it is prepared to negotiate. Civil administration, development and diplomacy can begin alongside the military policy at the Suez front.

- Political Power: +100

```hoi4
add_political_power = 100
```

### Defensible Frontiers and Negotiating Reserves

`ISR70_all_on` | x=121, y=8 | 35 days

Prerequisites: (ISR70_territorial_policy).

Exclusive with: ISR70_territorial_maximalism, ISR70_regional_compromise.

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Agricultural security zones and retained negotiating reserves offer one approach to territorial policy. Allon and other cabinet ministers have advanced competing proposals; the government must choose its own balance between a defensible frontier and room for agreement.

- Army Experience: +20
- National spirit:
- Division Defense: +5%

```hoi4
add_ideas = ISR70_all_on_idea
army_experience = 20
set_country_flag = ISR70_allon_policy
```

### Permanent Territorial Control

`ISR70_territorial_maximalism` | x=125, y=8 | 35 days

Prerequisites: (ISR70_territorial_policy).

Exclusive with: ISR70_all_on, ISR70_regional_compromise.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Supporters of permanent territorial control want the cabinet to commit to a lasting administrative presence. Their programme will shape relations with neighboring states and the communities under Israeli control.

- Political Power: +75
- National spirit:
- War Support: +5%

```hoi4
add_ideas = ISR70_territorial_maximalism_idea
add_political_power = 75
set_country_flag = ISR70_territorial_policy
```

### Negotiate Territorial Compromises

`ISR70_regional_compromise` | x=131, y=8 | 35 days

Prerequisites: (ISR70_territorial_policy).

Exclusive with: ISR70_all_on, ISR70_territorial_maximalism.

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Authorize territorial compromise and give the negotiating team political capital for the peace route.

- Political Power: +100
- National spirit:
- Foreign Influence Defense: +5%

```hoi4
add_ideas = ISR70_regional_compromise_idea
add_political_power = 100
set_country_flag = ISR70_peace_policy
```

### Sinai and Egyptian Security Interests

`ISR70_sinai_negotiation` | x=121, y=9 | 35 days

Prerequisites: (ISR70_all_on OR ISR70_regional_compromise).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Prepare Sinai security guarantees and unlock the Egyptian peace proposal. Egypt must agree before implementation.

- Political Power: +75
- Unlocks decisions: A Round of Security Talks.

```hoi4
add_political_power = 75
set_country_flag = ISR70_sinai_talks

unlock_decision_tooltip = ISR70_decision_talks_egypt
```

### Autonomy in the West Bank

`ISR70_westbank_autonomy` | x=124, y=9 | 35 days

Prerequisites: (ISR70_all_on OR ISR70_regional_compromise).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Prepare a municipal autonomy proposal and unlock Palestinian negotiations. Local representatives retain the right to reject the offer.

- Political Power: +75
- Unlocks decisions: Include Municipal Representatives and Palestine.

```hoi4
add_political_power = 75
set_country_flag = ISR70_westbank_talks

unlock_decision_tooltip = ISR70_decision_talks_pal
```

### A Security Settlement for the Golan

`ISR70_golan_review` | x=134, y=8 | 35 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Send Syria a proposal for a Golan security framework. Talks do not transfer ownership or grant cores.

- Political Power: +50
- Sends Syria a security proposal. Syria may accept or decline; this focus grants no cores or automatic land transfer.

```hoi4
add_political_power = 50
set_country_flag = ISR70_golan_talks
if = { limit = { SYR = { exists = yes } } SYR = { country_event = { id = ISR70.73 days = 1 } } }
custom_effect_tooltip = ISR70_golan_review_outcome_tt
```

### A Civil Administration for Gaza

`ISR70_gaza_services` | x=137, y=8 | 35 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/israel_palestine/gaza_civic_organizations.dds`.

Civilian administration in Gaza depends on functioning local services. Work with municipal institutions to improve provision and the practical conditions of daily life.

- Treasury cost on completion: 0.4% of annual GDP.
- National spirit:
- Bureaucracy Cost: -5%
- While Israel controls Palestinian-owned Gaza, adds a local administrative compact: Local Supplies for Controller +1.5%.

```hoi4
add_ideas = ISR70_gaza_services_idea
ISR70_pay_0_0040 = yes
set_country_flag = ISR70_gaza_services
if = { limit = { 209 = { is_owned_by = PAL is_controlled_by = ROOT } } 209 = { add_dynamic_modifier = { modifier = ISR70_municipal_agreement } } }
custom_effect_tooltip = ISR70_gaza_services_outcome_tt
```

### A Negotiated Peace with Egypt

`ISR70_egypt_peace` | x=121, y=10 | 70 days

Prerequisites: (ISR70_sinai_negotiation).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Implement an accepted Egyptian peace agreement, end the War of Attrition and improve the climate for civilian investment. Sinai control returns only under the agreed ownership checks.

- Political Power: +100
- Stability: +5%
- Removes the national spirit "The War of Attrition".
- National spirit:
- Incoming Investment Cost: -10%

```hoi4
add_ideas = ISR70_egypt_peace_idea
remove_ideas = ISR70_attrition
add_stability = 0.05
add_political_power = 100
ISR70_implement_egypt_peace = yes
```

### A Regional Peace Framework

`ISR70_regional_normalization` | x=123, y=11 | 70 days

Prerequisites: (ISR70_egypt_peace) AND (ISR70_westbank_autonomy).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Build commercial and diplomatic institutions on the peace framework. Investment returns and office construction improve.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Return on Investment: +0.5%
- Office Construction Speed: +10%

```hoi4
add_ideas = ISR70_regional_normalization_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### The Costs of Permanent Administration

`ISR70_territory_administration` | x=127, y=9 | 35 days

Prerequisites: (ISR70_territorial_maximalism).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Fund a permanent administrative apparatus. It reduces garrison losses but has an explicit recurring bureaucratic cost.

- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Damage to Garrisons: -15%
- Bureaucracy Cost: +5%

```hoi4
add_ideas = ISR70_territory_administration_idea
ISR70_pay_0_0080 = yes
```

### Submit Annexation to Parliament

`ISR70_annexation_review` | x=127, y=10 | 35 days

Prerequisites: (ISR70_territory_administration).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Parliament must debate the future of the territories under Israeli control. Administrative continuity, municipal negotiations and sovereignty claims present different political commitments.

- Political Power: +75
- Opens a parliamentary event: retain administration, offer municipal talks, or adopt sovereignty claims. No automatic cores are granted.

```hoi4
add_political_power = 75
set_country_flag = ISR70_annexation_review
country_event = { id = ISR70.81 days = 1 }
custom_effect_tooltip = ISR70_annexation_review_outcome_tt
```

## Citizenship and Municipal Development

Citizenship and Municipal Development. Each policy retains its own conditions and consequences.

### Arab Citizens and the State

`ISR70_arab_citizens` | x=12, y=26 | 21 days

Prerequisites: (ISR70_social_contract).

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Set the cabinet programme for Arab citizens of Israel. Equal access and preferential discrimination are exclusive; municipal self-government remains a separate, compatible choice.

- Opens the two exclusive access routes and optional municipal autonomy.

```hoi4
ISR70_policy_complete_citizen_review = yes
```

### Equal Municipal Services

`ISR70_equal_local_services` | x=4, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Exclusive with: ISR70_preferential_allocations.

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Fund municipal services and transport links in state 205. The stability and continuing service costs begin when the project is completed.

- Fund municipal services and transport links in state 205. The stability and continuing service costs begin when the project is completed.
- Treasury: -0.6% of annual GDP. Completion: 180 days. +1 infrastructure levels in Haifa; +1 shared building slots. Continuing effects: Stability: +2%; Social Spending Cost: +3%.

```hoi4
ISR70_policy_complete_equal_services = yes
```

### Open Public Employment

`ISR70_equal_employment` | x=4, y=29 | 35 days

Prerequisites: (ISR70_equal_local_services).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Spend 0.3% of GDP once on training and hiring procedures. Office worker requirement falls by 2%.

- Spend 0.3% of GDP once on training and hiring procedures. Office worker requirement falls by 2%.

```hoi4
ISR70_policy_complete_equal_employment = yes
```

### Equal Access to Land and Credit

`ISR70_equal_access` | x=4, y=30 | 49 days

Prerequisites: (ISR70_equal_employment).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Spend 50 political power and reserve 1.2% of GDP for a one-factory credit and enterprise programme in Haifa (state 205). Reform effects begin after delivery.

- Spend 50 political power and reserve 1.2% of GDP for a one-factory credit and enterprise programme in Haifa (state 205). Reform effects begin after delivery.
- Treasury: -1.2% of annual GDP. Completion: 270 days. +1 civilian factories in Haifa; +1 shared building slots. Continuing effects: Factory Output: +3%; Incoming Investment Cost: -5%; Bureaucracy Cost: +2%.

```hoi4
ISR70_policy_complete_equal_access = yes
```

### Municipal Self-Government

`ISR70_local_autonomy` | x=12, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Spend 50 political power to devolve municipal responsibilities. Bureaucracy costs fall 10%; corruption costs rise 3%.

- Spend 50 political power to devolve municipal responsibilities. Bureaucracy costs fall 10%; corruption costs rise 3%.

```hoi4
ISR70_policy_complete_municipal_self = yes
```

### Municipal Infrastructure Grants

`ISR70_municipal_pacts` | x=12, y=29 | 35 days

Prerequisites: (ISR70_local_autonomy).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Opens one joint 1.0% GDP grant programme for states 205 and 206. Both projects must remain deliverable; the shared social cost applies after completion.

- Opens one joint 1.0% GDP grant programme for states 205 and 206. Both projects must remain deliverable; the shared social cost applies after completion.
- Treasury: -1% of annual GDP. Completion: 180 days. +1 infrastructure levels in Haifa; +1 infrastructure levels in the Negev; +2 shared building slots. Continuing effects: Social Spending Cost: +2%.

```hoi4
ISR70_policy_complete_municipal_pacts = yes
```

### Municipal Development Funds

`ISR70_municipal_representation` | x=12, y=30 | 49 days

Prerequisites: (ISR70_municipal_pacts).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Spend 0.2% of GDP to establish the funds. Infrastructure construction is 15% faster in states 205 and 206 while Israel owns and controls them; internal investment costs fall 10%.

- Spend 0.2% of GDP to establish the funds. Infrastructure construction is 15% faster in states 205 and 206 while Israel owns and controls them; internal investment costs fall 10%.

```hoi4
ISR70_policy_complete_municipal_representation = yes
```

### Preferential Land and Budget Allocation

`ISR70_preferential_allocations` | x=20, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Exclusive with: ISR70_equal_local_services.

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Reserve 0.5% of GDP to open two building slots and deliver one infrastructure level in state 206. Stability falls by 2 percentage points on completion.

- Reserve 0.5% of GDP to open two building slots and deliver one infrastructure level in state 206. Stability falls by 2 percentage points on completion.
- Treasury: -0.5% of annual GDP. Completion: 180 days. +2 building slots in the Negev; +1 infrastructure levels in the Negev; +3 shared building slots. Continuing effects: Stability: -2%.

```hoi4
ISR70_policy_complete_preferential_allocations = yes
```

### Preferential Development Contracts

`ISR70_restricted_employment` | x=20, y=29 | 35 days

Prerequisites: (ISR70_preferential_allocations).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Reserve 1.2% of GDP for a factory in state 206. Preferential procurement raises corruption costs by 3%; industrial conglomerates gain 10 opinion if active after delivery.

- Reserve 1.2% of GDP for a factory in state 206. Preferential procurement raises corruption costs by 3%; industrial conglomerates gain 10 opinion if active after delivery.
- Treasury: -1.2% of annual GDP. Completion: 270 days. +1 civilian factories in the Negev; +1 shared building slots. Continuing effects: Corruption Cost: +3%.

```hoi4
ISR70_policy_complete_restricted_employment = yes
```

### Separate Municipal Funding Rules

`ISR70_separate_development` | x=20, y=30 | 49 days

Prerequisites: (ISR70_restricted_employment).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Choose discriminatory funding rules: social costs fall 5%, stability falls 2 percentage points, and corruption costs rise 2%.

- Choose discriminatory funding rules: social costs fall 5%, stability falls 2 percentage points, and corruption costs rise 2%.

```hoi4
ISR70_policy_complete_separate_development = yes
```

## Settlement Projects and Palestinian Relations

Settlement Projects and Palestinian Relations. Each policy retains its own conditions and consequences.

### The Interministerial Settlement Committee

`ISR70_land_survey` | x=67, y=26 | 35 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

The cabinet must reconcile agricultural development, military plans and the claims of Palestinian landowners. A survey of the West Bank or Gaza will define the area in which the government commits its settlement budget.

- Treasury cost: 0.1% of annual GDP. Select the West Bank or Gaza as the project area.

```hoi4
ISR70_policy_complete_land_survey = yes
```

### Land, Security and the Development Budget

`ISR70_settlement_budget` | x=67, y=27 | 21 days

Prerequisites: (ISR70_land_survey).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

The settlement departments compete with development towns and immigrant housing for engineers, credit and public services. Choose a negotiated freeze, a limited group of agricultural sites or a larger civilian settlement network.

- Choose one programme: negotiated freeze, limited agricultural sites or civilian settlement expansion.

```hoi4
ISR70_policy_complete_settlement_budget = yes
```

### Offer a Settlement Freeze

`ISR70_freeze_new` | x=59, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_designated_sites, ISR70_authorize_expansion.

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

A halt to new settlement construction would leave more room for civilian administration and negotiations with Palestinian representatives. The cabinet must secure acceptance before it can rely on a local administrative arrangement.

- Political Power: -75. Palestinian acceptance: local resistance target -5 points in the selected project area; Palestinian opinion of Israel +15.

```hoi4
ISR70_policy_complete_freeze_new = yes
```

### Municipal Works Across the Green Line

`ISR70_municipal_works` | x=59, y=30 | 49 days

Prerequisites: (ISR70_freeze_new).

Artwork: `gfx/interface/goals/israel_palestine/gaza_civic_organizations.dds`.

Roads, workshops and civilian services can support the existing population without opening another settlement frontier. This programme ties Israeli investment to the negotiated freeze and requires continuing public expenditure.

- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 civilian factories in the West Bank; +1 infrastructure levels in the West Bank; +2 shared building slots. Continuing effects: Social Spending Cost: +2%. Local effects: Local Supplies for Controller: +10%.
- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 civilian factories in Gaza; +1 infrastructure levels in Gaza; +2 shared building slots. Continuing effects: Social Spending Cost: +2%. Local effects: Local Supplies for Controller: +10%.

```hoi4
ISR70_policy_complete_municipal_works = yes
```

### Negotiate a Civil Administration Compact

`ISR70_land_compact` | x=59, y=31 | 70 days

Prerequisites: (ISR70_municipal_works).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Palestinian representatives must decide whether to cooperate with a funded municipal administration. A practical agreement can reduce the burden on Israeli ministries and garrisons, while leaving the political dispute unresolved.

- Palestinian acceptance unlocks the funded compact: Treasury -0.3% of annual GDP, transferred to Palestine; bureaucracy cost -5%, local garrison requirement -20%, resistance target -5 points.

```hoi4
ISR70_policy_complete_land_compact = yes
```

### Nahal Agricultural Sites

`ISR70_designated_sites` | x=67, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_freeze_new, ISR70_authorize_expansion.

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Nahal combines agricultural training with military service. A limited group of sites can improve irrigation practice and frontier supply, but even a geographically restrained programme requires land administration and strains relations with Palestinian institutions.

- Treasury: -0.8% of annual GDP. Completion: 240 days. +1 building slots in the West Bank; +1 agricultural districts in the West Bank; +2 shared building slots. Continuing effects: Agricultural Productivity: +6%; Bureaucracy Cost: +2%. Local effects: Relations toward Israel: -10 points. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -0.8% of annual GDP. Completion: 240 days. +1 building slots in Gaza; +1 agricultural districts in Gaza; +2 shared building slots. Continuing effects: Agricultural Productivity: +6%; Bureaucracy Cost: +2%. Local effects: Relations toward Israel: -10 points. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_designated_sites = yes
```

### Mekorot and Regional Service Roads

`ISR70_settlement_services` | x=67, y=30 | 49 days

Prerequisites: (ISR70_designated_sites).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Water connections, repair crews and reliable road access turn isolated sites into workable communities. The logistical gain is real, while the extension of the settlement footprint increases local opposition.

- Treasury: -0.6% of annual GDP. Completion: 180 days. +1 infrastructure levels in the West Bank; +1 shared building slots. Local effects: Local Supplies for Controller: +15%; Local resistance target: +5 points. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -0.6% of annual GDP. Completion: 180 days. +1 infrastructure levels in Gaza; +1 shared building slots. Local effects: Local Supplies for Controller: +15%; Local resistance target: +5 points. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_settlement_services = yes
```

### Consolidate a Limited Settlement Perimeter

`ISR70_settlement_ceiling` | x=67, y=31 | 49 days

Prerequisites: (ISR70_settlement_services).

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Protect the existing sites and their workshops while ruling out another wave of expansion. A smaller perimeter is easier to maintain, although guarding civilian communities still adds to the security budget.

- Treasury: -0.4% of annual GDP. Completion: 180 days. +1 land fort levels in the West Bank; +1 shared building slots. Continuing effects: Industry Repair Speed: +5%; Police Cost: +1%. Local effects: Local Garrison Requirement: +5%. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -0.4% of annual GDP. Completion: 180 days. +1 land fort levels in Gaza; +1 shared building slots. Continuing effects: Industry Repair Speed: +5%; Police Cost: +1%. Local effects: Local Garrison Requirement: +5%. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_settlement_ceiling = yes
```

### A Civilian Settlement Programme

`ISR70_authorize_expansion` | x=75, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_freeze_new, ISR70_designated_sites.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

The cabinet can place the settlement departments behind a broader civilian programme. Preparing development land and access routes will accelerate construction, while increasing administrative commitments and the dispute over the territory.

- Treasury: -0.3% of annual GDP. Completion: 90 days. +3 building slots in the West Bank; +3 shared building slots. Continuing effects: Bureaucracy Cost: +2%. Local effects: Local Infrastructure Construction Speed: +15%; Relations toward Israel: -25 points.
- Treasury: -0.3% of annual GDP. Completion: 90 days. +3 building slots in Gaza; +3 shared building slots. Continuing effects: Bureaucracy Cost: +2%. Local effects: Local Infrastructure Construction Speed: +15%; Relations toward Israel: -25 points.

```hoi4
ISR70_policy_complete_authorize_expansion = yes
```

### Cooperative Farms and Settlement Workshops

`ISR70_settlement_package` | x=75, y=30 | 70 days

Prerequisites: (ISR70_authorize_expansion).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Cooperative farms, packing facilities and workshops will connect the new communities to Israeli production networks. Agricultural and manufacturing gains come with subsidised housing, public services and a larger capital commitment.

- Treasury: -2.3% of annual GDP. Completion: 300 days. +1 agricultural districts in the West Bank; +1 civilian factories in the West Bank; +2 shared building slots. Continuing effects: Agricultural Productivity: +10%; Factory Output: +3%; Social Spending Cost: +4%. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -2.3% of annual GDP. Completion: 300 days. +1 agricultural districts in Gaza; +1 civilian factories in Gaza; +2 shared building slots. Continuing effects: Agricultural Productivity: +10%; Factory Output: +3%; Social Spending Cost: +4%. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_settlement_package = yes
```

### Regional Roads and Protected Supply Routes

`ISR70_entrench_network` | x=75, y=31 | 70 days

Prerequisites: (ISR70_settlement_package).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

A connected road network and prepared defensive positions make the settlement programme easier to supply and repair. The same network extends the area that the government must administer and protect.

- Treasury: -0.9% of annual GDP. Completion: 240 days. +2 infrastructure levels in the West Bank; +2 land fort levels in the West Bank; +4 shared building slots. Continuing effects: Industry Repair Speed: +10%; Bureaucracy Cost: +3%; Police Cost: +2%. Local effects: Local Supplies for Controller: +25%. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -0.9% of annual GDP. Completion: 240 days. +2 infrastructure levels in Gaza; +2 land fort levels in Gaza; +4 shared building slots. Continuing effects: Industry Repair Speed: +10%; Bureaucracy Cost: +3%; Police Cost: +2%. Local effects: Local Supplies for Controller: +25%. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_entrench_network = yes
```

### Negotiate a Settlement Ceiling and Compensation

`ISR70_settlement_compensation` | x=73, y=32 | 49 days

Prerequisites: (ISR70_entrench_network).

Exclusive with: ISR70_settlement_unilateral.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Offer an Israeli-funded property compensation programme and a binding ceiling on further settlement construction. Palestinian representatives decide whether the local terms are acceptable. The Israeli treasury funds the domestic compensation programme after acceptance. Funded compensation also eases the pressure on Palestinian administration and commerce.

- Political Power: -75. If accepted and funded: Treasury -0.6% of annual GDP; local garrison requirement +5%, resistance target +3 points. Further settlement extensions are barred.
- Palestine, if present: the selected "West Bank: Territorial and Settlement Pressures" or "Gaza: Territorial and Settlement Pressures" programme retains Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%.

```hoi4
ISR70_policy_complete_settlement_compensation = yes
```

### Maintain the Unilateral Settlement Programme

`ISR70_settlement_unilateral` | x=77, y=32 | 35 days

Prerequisites: (ISR70_entrench_network).

Exclusive with: ISR70_settlement_compensation.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

The government can keep building without an agreed territorial settlement. Further agricultural and workshop projects remain possible, at the price of a wider garrison commitment, persistent local opposition and continuing public subsidies.

- Political Power: -50. Local garrison requirement +15%, damage to garrisons +10%, resistance target +10 points. Unlocks up to three additional paid settlement phases in the selected area.
- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in the West Bank; +1 infrastructure levels in the West Bank; +1 land fort levels in the West Bank; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -1.8% of annual GDP. Completion: 300 days. +1 agricultural districts in the West Bank; +1 infrastructure levels in the West Bank; +1 land fort levels in the West Bank; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -2.1% of annual GDP. Completion: 330 days. +1 agricultural districts in the West Bank; +1 infrastructure levels in the West Bank; +1 land fort levels in the West Bank; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in Gaza; +1 infrastructure levels in Gaza; +1 land fort levels in Gaza; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -1.8% of annual GDP. Completion: 300 days. +1 agricultural districts in Gaza; +1 infrastructure levels in Gaza; +1 land fort levels in Gaza; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.
- Treasury: -2.1% of annual GDP. Completion: 330 days. +1 agricultural districts in Gaza; +1 infrastructure levels in Gaza; +1 land fort levels in Gaza; +3 shared building slots. Continuing effects: Agricultural Productivity: +4%; Factory Output: +1%; Social Spending Cost: +2%; Police Cost: +2%. Local effects: Local Supplies for Controller: +5%; Local Garrison Requirement: +5%; Local resistance target: +4 points. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_settlement_unilateral = yes
```

## Development Finance and Office Networks

Development Finance and Office Networks. Each policy retains its own conditions and consequences.

### Finance for National Development

`ISR70_finance_links` | x=39, y=26 | 21 days

Prerequisites: (ISR70_diaspora_bonds).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Open the domestic, bank-led and international development-finance programmes.

- Open the domestic, bank-led and international development-finance programmes.

```hoi4
ISR70_policy_complete_finance_links = yes
```

### Train Accountants and Office Staff

`ISR70_clerical_training` | x=39, y=27 | 35 days

Prerequisites: (ISR70_finance_links).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Spend 0.4% of GDP on accounting and office training. Office worker requirement falls 3%.

- Spend 0.4% of GDP on accounting and office training. Office worker requirement falls 3%.

```hoi4
ISR70_policy_complete_clerical_training = yes
```

### Mechanized Clearing and Bookkeeping

`ISR70_clearing_network` | x=39, y=28 | 49 days

Prerequisites: (ISR70_clerical_training).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Spend 0.6% of GDP on mechanized clearing and bookkeeping. Office worker requirement falls a further 3% (6% across this finance route).

- Spend 0.6% of GDP on mechanized clearing and bookkeeping. Office worker requirement falls a further 3% (6% across this finance route).

```hoi4
ISR70_policy_complete_clearing_network = yes
```

### Long-Term Development Bonds

`ISR70_development_bonds` | x=31, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_bank_consortium, ISR70_export_credit.

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Unlock a one-time decision to borrow 1% of GDP. The amount borrowed is added equally to treasury liquidity and public debt; bankruptcy blocks the draw.

- Unlock a one-time decision to borrow 1% of GDP. The amount borrowed is added equally to treasury liquidity and public debt; bankruptcy blocks the draw.

```hoi4
ISR70_policy_complete_development_bonds = yes
```

### Audit the Development Funds

`ISR70_audited_funds` | x=31, y=31 | 35 days

Prerequisites: (ISR70_development_bonds).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Spend 50 political power on project oversight. Corruption costs fall 3%.

- Spend 50 political power on project oversight. Corruption costs fall 3%.

```hoi4
ISR70_policy_complete_audited_funds = yes
```

### Service Centers for New Towns

`ISR70_development_offices` | x=31, y=32 | 70 days

Prerequisites: (ISR70_audited_funds).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Reserve 1.2% of GDP for an office level in state 206. On delivery, office worker requirement falls a further 2%, making the route total 8%.

- Reserve 1.2% of GDP for an office level in state 206. On delivery, office worker requirement falls a further 2%, making the route total 8%.
- Treasury: -1.2% of annual GDP. Completion: 240 days. +1 office levels in the Negev; +1 shared building slots. Continuing effects: Office Worker Requirement: -2%.

```hoi4
ISR70_policy_complete_development_offices = yes
```

### A Domestic Banking Consortium

`ISR70_bank_consortium` | x=39, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_development_bonds, ISR70_export_credit.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Office productivity rises 3%; concentration and privileged access raise corruption costs 3%.

- Office productivity rises 3%; concentration and privileged access raise corruption costs 3%.

```hoi4
ISR70_policy_complete_bank_consortium = yes
```

### Shared Back Offices

`ISR70_shared_services` | x=39, y=31 | 49 days

Prerequisites: (ISR70_bank_consortium).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Spend 0.5% of GDP to standardize shared accounting and administration. Office worker requirement falls a further 4%, for 10% across this route.

- Spend 0.5% of GDP to standardize shared accounting and administration. Office worker requirement falls a further 4%, for 10% across this route.

```hoi4
ISR70_policy_complete_shared_services = yes
```

### Bank-Industry Investment Partnerships

`ISR70_industrial_credit` | x=39, y=32 | 70 days

Prerequisites: (ISR70_shared_services).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Reserve 1.2% of GDP for an office level in Tel Aviv (204). Office construction speed rises 5%; corruption costs rise a further 2% on delivery.

- Reserve 1.2% of GDP for an office level in Tel Aviv (204). Office construction speed rises 5%; corruption costs rise a further 2% on delivery.
- Treasury: -1.2% of annual GDP. Completion: 240 days. +1 office levels in Tel Aviv; +1 shared building slots. Continuing effects: Office Construction Speed: +5%; Corruption Cost: +2%.

```hoi4
ISR70_policy_complete_industrial_credit = yes
```

### Negotiate Export Credit Lines

`ISR70_export_credit` | x=47, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_development_bonds, ISR70_bank_consortium.

Artwork: `gfx/interface/goals/coldwar/generic_positive_trade_relations_gold.png`.

Unlock a repeatable request costing 50 political power. The United States may accept or decline; a declined request can be renewed after 360 days. An existing military agreement does not block civilian credit.

- Unlock a repeatable request costing 50 political power. The United States may accept or decline; a declined request can be renewed after 360 days. An existing military agreement does not block civilian credit.

```hoi4
ISR70_policy_complete_export_credit = yes
```

### Finance Imported Office Equipment

`ISR70_equipment_finance` | x=47, y=31 | 49 days

Prerequisites: (ISR70_export_credit).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Spend 0.6% of GDP on imported office equipment. Office productivity rises 5%; Cold War market exposure rises 5%.

- Spend 0.6% of GDP on imported office equipment. Office productivity rises 5%; Cold War market exposure rises 5%.

```hoi4
ISR70_policy_complete_equipment_finance = yes
```

### Build an Export Services Sector

`ISR70_export_services` | x=47, y=32 | 70 days

Prerequisites: (ISR70_equipment_finance).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Requires an accepted export-credit line. Reserve 1.2% of GDP for an office level in Haifa (205); office construction speed rises 10% and market exposure rises a further 5% on delivery.

- Requires an accepted export-credit line. Reserve 1.2% of GDP for an office level in Haifa (205); office construction speed rises 10% and market exposure rises a further 5% on delivery.
- Treasury: -1.2% of annual GDP. Completion: 240 days. +1 office levels in Haifa; +1 shared building slots. Continuing effects: Office Construction Speed: +10%; World-Market Exposure: +5%.

```hoi4
ISR70_policy_complete_export_services = yes
```

## Greater Israel: Sinai Development and Integration

Greater Israel: Sinai Development and Integration. Each policy retains its own conditions and consequences.

### A Greater Israel Mandate

`ISR70_gi_mandate` | x=92, y=26 | 35 days

Prerequisites: (ISR70_territorial_maximalism).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Pay the shared 100-political-power territorial mandate once. A mandate already paid through Herut covers this focus; it grants neither ownership nor a declaration of war.

- Pay the shared 100-political-power territorial mandate once. A mandate already paid through Herut covers this focus; it grants neither ownership nor a declaration of war.

```hoi4
ISR70_policy_complete_gi_mandate = yes
```

### Borders and Budgets for Sinai

`ISR70_gi_frontier_review` | x=92, y=27 | 35 days

Prerequisites: (ISR70_gi_mandate).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Budget 0.2% of GDP to separate Sinai civilian development, coastal projects, and the later choice of legal status.

- Budget 0.2% of GDP to separate Sinai civilian development, coastal projects, and the later choice of legal status.

```hoi4
ISR70_policy_complete_gi_frontier_review = yes
```

### A Sinai Development Authority

`ISR70_gi_sinai_admin` | x=88, y=29 | 35 days

Prerequisites: (ISR70_gi_frontier_review).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

A permanent development authority can coordinate the roads and services required by the Sinai programme. Distance and the unresolved Egyptian territorial claim make the administrative commitment expensive.

- Establish permanent Sinai administration at a cost of 0.3% of GDP. Local infrastructure builds 15% faster; bureaucracy costs rise 3%. Egyptian ownership remains until an actual territorial settlement.

```hoi4
ISR70_policy_complete_gi_sinai_admin = yes
```

### Housing on the Sinai Frontier

`ISR70_gi_sinai_housing` | x=88, y=30 | 49 days

Prerequisites: (ISR70_gi_sinai_admin).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

Settlement housing requires access roads and serviced land before families can move. The construction programme commits resources that could otherwise serve development towns within Israel.

- Treasury: -1% of annual GDP. Completion: 240 days. +2 building slots in Sinai; +1 infrastructure levels in Sinai; +3 shared building slots.

```hoi4
ISR70_policy_complete_gi_sinai_housing = yes
```

### Voluntary Settlement in the Sinai Towns

`ISR70_gi_sinai_families` | x=88, y=31 | 70 days

Prerequisites: (ISR70_gi_sinai_housing).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

Fund a voluntary internal movement of at most 20,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 20,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_gi_sinai_families = yes
```

### Family Services for Frontier Communities

`ISR70_gi_frontier_families` | x=88, y=32 | 49 days

Prerequisites: (ISR70_gi_sinai_families).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Clinics and family services can make remote communities more viable. A five-year commitment supports household growth while increasing the healthcare budget.

- Fund 0.4% of GDP for a single five-year family-service idea: population-growth modifier +5%, healthcare costs +2%. It does not add 5% of the population each month and cannot stack with itself.

```hoi4
ISR70_policy_complete_gi_frontier_families = yes
```

### Sinai Farms and Civilian Workshops

`ISR70_gi_sinai_economy` | x=88, y=33 | 70 days

Prerequisites: (ISR70_gi_frontier_families).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Agricultural sites and repair workshops offer a civilian economic base for the Sinai programme. Their viability depends on reliable supply links and continued Israeli control.

- Treasury: -1.8% of annual GDP. Completion: 300 days. +1 agricultural districts in Sinai; +1 civilian factories in Sinai; +2 shared building slots.

```hoi4
ISR70_policy_complete_gi_sinai_economy = yes
```

### Settle Sovereignty over the Sinai

`ISR70_gi_sinai_status` | x=88, y=34 | 70 days

Prerequisites: (ISR70_gi_sinai_economy).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

After an actual peace settlement has transferred Sinai, pay 150 political power for its sovereignty administration. This focus does not transfer the state or remove the Egyptian core.

- After an actual peace settlement has transferred Sinai, pay 150 political power for its sovereignty administration. This focus does not transfer the state or remove the Egyptian core.

```hoi4
ISR70_policy_complete_gi_sinai_status = yes
```

### Assert the Sinai Territorial Claim

`ISR70_gi_canal_claim` | x=96, y=29 | 70 days

Prerequisites: (ISR70_gi_frontier_review).

Artwork: `gfx/interface/goals/coldwar/generic_air_fighter_new.png`.

Pay 150 political power for a Sinai territorial claim. Relations with Egypt fall 40 and with PAL/Jordan 15. This neither changes ownership nor declares war.

- Pay 150 political power for a Sinai territorial claim. Relations with Egypt fall 40 and with PAL/Jordan 15. This neither changes ownership nor declares war.

```hoi4
ISR70_policy_complete_gi_canal_claim = yes
```

### Sinai Coastal Supply Stations

`ISR70_gi_canal_repair` | x=96, y=30 | 70 days

Prerequisites: (ISR70_gi_canal_claim).

Artwork: `gfx/interface/goals/coldwar/Drydock_Construction.tga`.

Repair the coastal road and its supply stations so civilian and military traffic can reach remote communities. Protecting those links adds another duty for the regional garrison.

- Treasury: -1.2% of annual GDP. Completion: 240 days. +1 infrastructure levels in Sinai; +1 naval base levels in Sinai; +2 shared building slots. Local effects: Local Garrison Requirement: +10%.

```hoi4
ISR70_policy_complete_gi_canal_repair = yes
```

### A Sinai Coastal Settlement Programme

`ISR70_gi_canal_settlers` | x=96, y=31 | 70 days

Prerequisites: (ISR70_gi_canal_repair).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund a voluntary internal movement of at most 15,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 15,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_gi_canal_settlers = yes
```

### Sinai Coastal Workshops

`ISR70_gi_canal_industry` | x=96, y=32 | 70 days

Prerequisites: (ISR70_gi_canal_settlers).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Civilian workshops and a small dockyard can maintain vehicles, vessels and coastal installations closer to where they operate. The programme requires a substantial capital budget and dependable control of the coast.

- Treasury: -2% of annual GDP. Completion: 360 days. +2 building slots in Sinai; +1 civilian factories in Sinai; +1 naval dockyards in Sinai; +4 shared building slots.

```hoi4
ISR70_policy_complete_gi_canal_industry = yes
```

### Sinai Coastal Logistics

`ISR70_gi_canal_navigation` | x=96, y=33 | 70 days

Prerequisites: (ISR70_gi_canal_industry).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Coastal handling facilities and maintenance crews can improve local supply without depending on traffic through the Suez Canal. Running the service adds to the civil administration budget.

- Treasury: -0.8% of annual GDP. Completion: 180 days. the specified clearance and operating works. Continuing effects: Bureaucracy Cost: +1%. Local effects: Local Supplies for Controller: +10%.

```hoi4
ISR70_policy_complete_gi_canal_navigation = yes
```

### Unify Sinai District Administration

`ISR70_gi_canal_province` | x=96, y=34 | 70 days

Prerequisites: (ISR70_gi_canal_navigation).

Artwork: `gfx/interface/goals/coldwar/Adopt_New_Constitiution.tga`.

Constitute the Sinai province only after actual Israeli ownership and control. Pay 150 political power and 0.3% of GDP; bureaucracy costs rise 3%. No core is granted.

- Constitute the Sinai province only after actual Israeli ownership and control. Pay 150 political power and 0.3% of GDP; bureaucracy costs rise 3%. No core is granted.

```hoi4
ISR70_policy_complete_gi_canal_province = yes
```

## Civil Rights and Occupation Status

Civil Rights and Occupation Status. Each policy retains its own conditions and consequences.

### The Status of the Existing Residents

`ISR70_gi_resident_status` | x=110, y=26 | 35 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Pay 50 political power to open the actual choice of equal civil status or an unequal occupation statute. Settlement projects and party affiliation do not select the legal status automatically.

- Pay 50 political power to open the actual choice of equal civil status or an unequal occupation statute. Settlement projects and party affiliation do not select the legal status automatically.

```hoi4
ISR70_policy_complete_gi_resident_status = yes
```

### Equal Civil Status in Sinai

`ISR70_gi_equal_status` | x=106, y=28 | 49 days

Prerequisites: (ISR70_gi_resident_status).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Equal legal rights and service entitlements cost 100 political power and +3% social spending. There is no immediate resistance, compliance, loyalty or sovereignty-consent bonus. A previously chosen unequal regime must first be repealed through the explicit reform decision.

- Equal legal rights and service entitlements cost 100 political power and +3% social spending. There is no immediate resistance, compliance, loyalty or sovereignty-consent bonus. A previously chosen unequal regime must first be repealed through the explicit reform decision.

```hoi4
ISR70_policy_complete_gi_equal_status = yes
```

### Local Councils and Common Services

`ISR70_gi_canal_councils` | x=106, y=29 | 70 days

Prerequisites: (ISR70_gi_equal_status).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Fund civilian services at 0.8% of GDP and +2% bureaucracy costs. A separately accepted and implemented local contract reduces garrison needs only 5%. Rejection grants no bonus and does not repeal equal rights.

- Fund civilian services at 0.8% of GDP and +2% bureaucracy costs. A separately accepted and implemented local contract reduces garrison needs only 5%. Rejection grants no bonus and does not repeal equal rights.

```hoi4
ISR70_policy_complete_gi_canal_councils = yes
```

### Resolve Property Claims and Displacement

`ISR70_gi_property_settlement` | x=106, y=30 | 70 days

Prerequisites: (ISR70_gi_canal_councils).

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Reserve at least 0.7% of GDP for restitution. Only fulfilled, agreed claims can lower resistance target by 2 points. Prior expulsion creates additional obligations; there is no automatic loyalty or compliance reward.

- Reserve at least 0.7% of GDP for restitution. Only fulfilled, agreed claims can lower resistance target by 2 points. Prior expulsion creates additional obligations; there is no automatic loyalty or compliance reward.

```hoi4
ISR70_policy_complete_gi_property_settlement = yes
```

### Negotiate the Sinai Status

`ISR70_gi_core_review` | x=106, y=31 | 70 days

Prerequisites: (ISR70_gi_property_settlement).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

After ten years of real ownership and control and five years of equal rights, pay 100 political power to open a separate local status process. An affirmative result is not guaranteed; rejection leaves civil rights intact and grants no core.

- After ten years of real ownership and control and five years of equal rights, pay 100 political power to open a separate local status process. An affirmative result is not guaranteed; rejection leaves civil rights intact and grants no core.

```hoi4
ISR70_policy_complete_gi_core_review = yes
```

### Integrate the Sinai

`ISR70_gi_canal_core` | x=106, y=32 | 70 days

Prerequisites: (ISR70_gi_core_review).

Artwork: `gfx/interface/goals/coldwar/Adopt_New_Constitiution.tga`.

Pay 150 political power and 0.5% of GDP only after real local and Egyptian status agreements. The core applies solely to Sinai; ordinary core effects replace native occupation mechanics. Egyptian cores and historic claims remain.

- Pay 150 political power and 0.5% of GDP only after real local and Egyptian status agreements. The core applies solely to Sinai; ordinary core effects replace native occupation mechanics. Egyptian cores and historic claims remain.

```hoi4
ISR70_policy_complete_gi_canal_core = yes
```

### Separate Legal Status for Occupied Residents

`ISR70_occ_special_status` | x=114, y=28 | 35 days

Prerequisites: (ISR70_gi_resident_status).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Choose unequal occupation law. Existing local factory access rises 10 points, garrison needs rise 15%, police costs 3%, and resistance target 8 points; social spending falls 2%. The general and Kach statutes replace each other.

- Choose unequal occupation law. Existing local factory access rises 10 points, garrison needs rise 15%, police costs 3%, and resistance target 8 points; social spending falls 2%. The general and Kach statutes replace each other.

```hoi4
ISR70_policy_complete_occ_special_status = yes
```

### Security Roads and Controlled Access

`ISR70_occ_security_roads` | x=114, y=29 | 49 days

Prerequisites: (ISR70_occ_special_status).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Fund 0.8% of GDP for one infrastructure level after 180 days. Secured roads add 15% local supplies but also 5% garrison need under the unequal statute.

- Fund 0.8% of GDP for one infrastructure level after 180 days. Secured roads add 15% local supplies but also 5% garrison need under the unequal statute.
- Treasury: -0.8% of annual GDP. Completion: 180 days. +1 infrastructure levels in Sinai; +1 shared building slots. Local effects: Local Supplies for Controller: +15%; Local Garrison Requirement: +5%.

```hoi4
ISR70_policy_complete_occ_security_roads = yes
```

### Delegated Local Administration

`ISR70_occ_delegated_administration` | x=114, y=30 | 49 days

Prerequisites: (ISR70_occ_security_roads).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Request a limited local administrative contract. Only acceptance followed by funding grants the 3% bureaucracy saving and 3% corruption surcharge; refusal is possible.

- Request a limited local administrative contract. Only acceptance followed by funding grants the 3% bureaucracy saving and 3% corruption surcharge; refusal is possible.

```hoi4
ISR70_policy_complete_occ_delegated_administration = yes
```

### Industrial Enclaves under Separate Law

`ISR70_occ_occupation_industry` | x=114, y=31 | 70 days

Prerequisites: (ISR70_occ_delegated_administration).

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Reserve 1.0% of GDP for one building slot and one factory on contractually acquired land. Delivery takes 270 days and adds 5% local garrison need. A local administrative refusal does not block this distinct project.

- Reserve 1.0% of GDP for one building slot and one factory on contractually acquired land. Delivery takes 270 days and adds 5% local garrison need. A local administrative refusal does not block this distinct project.
- Treasury: -1% of annual GDP. Completion: 270 days. +1 building slots in Sinai; +1 civilian factories in Sinai; +2 shared building slots. Local effects: Local Garrison Requirement: +5%.

```hoi4
ISR70_policy_complete_occ_occupation_industry = yes
```

### A Permanent Occupation Statute

`ISR70_occ_permanent_statute` | x=114, y=32 | 70 days

Prerequisites: (ISR70_occ_occupation_industry).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Pay 100 political power to make the unequal statute permanent. Add 5 points of factory access, 2% police costs and 4 resistance-target points; stability falls 2 points. It remains an occupation, with no core.

- Pay 100 political power to make the unequal statute permanent. Add 5 points of factory access, 2% police costs and 4 resistance-target points; stability falls 2 points. It remains an occupation, with no core.

```hoi4
ISR70_policy_complete_occ_permanent_statute = yes
```

## Radical Territorial Programmes

Radical Territorial Programmes. Each policy retains its own conditions and consequences.

### A Radical Programme in Government

`ISR70_rad_government` | x=135, y=26 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Pay 75 political power for a radical territorial programme only while its actual party governs. This neither wins an election nor enacts any of the later choices automatically.

- Pay 75 political power for a radical territorial programme only while its actual party governs. This neither wins an election nor enacts any of the later choices automatically.

```hoi4
ISR70_policy_complete_rad_government = yes
```

### An Indivisible Territorial Programme

`ISR70_rad_herut_mandate` | x=127, y=28 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Herut/Gahal adopts the shared territorial mandate after choosing Indivisible Security Interests. Pay its 100-political-power cost once, credited against the Greater Israel entry.

- Herut/Gahal adopts the shared territorial mandate after choosing Indivisible Security Interests. Pay its 100-political-power cost once, credited against the Greater Israel entry.

```hoi4
ISR70_policy_complete_rad_herut_mandate = yes
```

### A National Territorial Development Authority

`ISR70_rad_herut_authority` | x=127, y=29 | 49 days

Prerequisites: (ISR70_rad_herut_mandate).

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Budget 0.4% of GDP for a territorial authority: local infrastructure construction +10%, bureaucracy costs +2%, only under the programme government.

- Budget 0.4% of GDP for a territorial authority: local infrastructure construction +10%, bureaucracy costs +2%, only under the programme government.

```hoi4
ISR70_policy_complete_rad_herut_authority = yes
```

### Prepare to Hold the New Frontier

`ISR70_rad_herut_preparation` | x=127, y=30 | 49 days

Prerequisites: (ISR70_rad_herut_authority).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Budget 0.5% of GDP and +3% personnel costs for 30 army experience and 10% local supply support in the controlled Sinai. It is preparation, not a declaration of war.

- Budget 0.5% of GDP and +3% personnel costs for 30 army experience and 10% local supply support in the controlled Sinai. It is preparation, not a declaration of war.

```hoi4
ISR70_policy_complete_rad_herut_preparation = yes
```

### Reject Territorial Withdrawal

`ISR70_rad_herut_retention` | x=127, y=31 | 70 days

Prerequisites: (ISR70_rad_herut_preparation).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Reject territorial withdrawal as an explicit Herut policy. Egyptian relations fall 20, American relations 15. A later peace requires repeal; the focus does not annex a state.

- Reject territorial withdrawal as an explicit Herut policy. Egyptian relations fall 20, American relations 15. A later peace requires repeal; the focus does not annex a state.

```hoi4
ISR70_policy_complete_rad_herut_retention = yes
```

### Religious Settlement Associations

`ISR70_rad_mafdal_council` | x=135, y=28 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/FocusElectHapoelHaMizrachi.dds`.

After choosing Religious Settlement Policy, pay 50 political power for the religious settlement programme. The later land and legal-binding choices remain separate decisions.

- After choosing Religious Settlement Policy, pay 50 political power for the religious settlement programme. The later land and legal-binding choices remain separate decisions.

```hoi4
ISR70_policy_complete_rad_mafdal_council = yes
```

### State Support for Settlement Communities

`ISR70_rad_mafdal_settlers` | x=135, y=29 | 70 days

Prerequisites: (ISR70_rad_mafdal_council).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund a voluntary internal movement of at most 10,000 people over 3 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 10,000 people over 3 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_rad_mafdal_settlers = yes
```

### Compulsory Expropriation of Land

`ISR70_rad_mafdal_land` | x=133, y=30 | 49 days

Prerequisites: (ISR70_rad_mafdal_settlers).

Exclusive with: ISR70_rad_mafdal_purchase.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Choose compulsory land expropriation instead of negotiated purchase: spend 0.4% of GDP for one building slot; local resistance target rises 8 points and property claims remain.

- Choose compulsory land expropriation instead of negotiated purchase: spend 0.4% of GDP for one building slot; local resistance target rises 8 points and property claims remain.

```hoi4
ISR70_policy_complete_rad_mafdal_land = yes
```

### Negotiated Land Purchases

`ISR70_rad_mafdal_purchase` | x=137, y=30 | 70 days

Prerequisites: (ISR70_rad_mafdal_settlers).

Exclusive with: ISR70_rad_mafdal_land.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Seek a voluntary land purchase. Only accepted terms unlock the 1.0%-GDP, 270-day project for the same building slot. No expropriation or automatic resistance rise follows refusal.

- Seek a voluntary land purchase. Only accepted terms unlock the 1.0%-GDP, 270-day project for the same building slot. No expropriation or automatic resistance rise follows refusal.
- Treasury: -1% of annual GDP. Completion: 270 days. +1 building slots in Sinai; +1 shared building slots.

```hoi4
ISR70_policy_complete_rad_mafdal_purchase = yes
```

### Declare the Settlement Land Inalienable

`ISR70_rad_mafdal_lock` | x=133, y=31 | 70 days

Prerequisites: (ISR70_rad_mafdal_land OR ISR70_rad_mafdal_purchase).

Exclusive with: ISR70_rad_mafdal_review.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Make settlement land politically inalienable. Gain 50 political power once; stability falls 3 points, and later withdrawal requires a separate repeal. The alternative is a reviewable lease system.

- Make settlement land politically inalienable. Gain 50 political power once; stability falls 3 points, and later withdrawal requires a separate repeal. The alternative is a reviewable lease system.

```hoi4
ISR70_policy_complete_rad_mafdal_lock = yes
```

### Reviewable Leases and Land Registry

`ISR70_rad_mafdal_review` | x=137, y=31 | 49 days

Prerequisites: (ISR70_rad_mafdal_land OR ISR70_rad_mafdal_purchase).

Exclusive with: ISR70_rad_mafdal_lock.

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Choose reviewable land leases and a registry instead of inalienability. Pay 50 political power and 0.3% of GDP; internal investment costs fall 5%, and territorial negotiations remain available.

- Choose reviewable land leases and a registry instead of inalienability. Pay 50 political power and 0.3% of GDP; internal investment costs fall 5%, and territorial negotiations remain available.

```hoi4
ISR70_policy_complete_rad_mafdal_review = yes
```

### National Front: Radical Government Programme

`ISR70_rad_kach_government` | x=143, y=28 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Pay 100 political power for the governing National Front/Kach programme. Before 1971 it uses the existing National Front presentation. Relations with Egypt, PAL and Jordan fall 25; taking office does not automatically expel residents.

- Pay 100 political power for the governing National Front/Kach programme. Before 1971 it uses the existing National Front presentation. Relations with Egypt, PAL and Jordan fall 25; taking office does not automatically expel residents.

```hoi4
ISR70_policy_complete_rad_kach_government = yes
```

### Deny Equal Civil Status

`ISR70_rad_denial` | x=143, y=29 | 49 days

Prerequisites: (ISR70_rad_kach_government).

Artwork: `gfx/interface/goals/coldwar/generic_police_state.png`.

Explicitly deny equal civil status in controlled, non-core Sinai: +10 points of occupied factory access, +10% garrison need and +5% police costs. This replaces the general unequal statute and blocks the civic core route while active.

- Explicitly deny equal civil status in controlled, non-core Sinai: +10 points of occupied factory access, +10% garrison need and +5% police costs. This replaces the general unequal statute and blocks the civic core route while active.

```hoi4
ISR70_policy_complete_rad_denial = yes
```

### Retain Residents under Separate Administration

`ISR70_rad_no_expulsion` | x=141, y=30 | 49 days

Prerequisites: (ISR70_rad_denial).

Exclusive with: ISR70_rad_expulsion.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Keep residents and their economic activity under unequal administration, with 0.5% of GDP for basic services. No seized-property slots or additional expulsion penalties are awarded; the underlying unequal legal regime remains.

- Keep residents and their economic activity under unequal administration, with 0.5% of GDP for basic services. No seized-property slots or additional expulsion penalties are awarded; the underlying unequal legal regime remains.

```hoi4
ISR70_policy_complete_rad_no_expulsion = yes
```

### Forced Expulsion of Arab Residents

`ISR70_rad_expulsion` | x=145, y=30 | 70 days

Prerequisites: (ISR70_rad_denial).

Exclusive with: ISR70_rad_no_expulsion.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

An explicitly chosen, abstract forced-displacement policy. Pay 200 political power; at most two seized-property slots, stability -8 points, local resistance target +25 points and garrison need +20%. Refugees and property claims persist; other states receive actual embargo choices. No expulsion quota, population deletion, or core reward.

- An explicitly chosen, abstract forced-displacement policy. Pay 200 political power; at most two seized-property slots, stability -8 points, local resistance target +25 points and garrison need +20%. Refugees and property claims persist; other states receive actual embargo choices. No expulsion quota, population deletion, or core reward.

```hoi4
ISR70_policy_complete_rad_expulsion = yes
```

### Security Powers with an Electoral Sunset

`ISR70_rad_limited_emergency` | x=141, y=31 | 49 days

Prerequisites: (ISR70_rad_no_expulsion OR ISR70_rad_expulsion).

Exclusive with: ISR70_rad_permanent_emergency.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Pay 50 political power for 365 days of +2 occupied factory-access points and +3% police costs. Elections are preserved. Renewal requires another paid government decision; the alternative is permanent emergency.

- Pay 50 political power for 365 days of +2 occupied factory-access points and +3% police costs. Elections are preserved. Renewal requires another paid government decision; the alternative is permanent emergency.

```hoi4
ISR70_policy_complete_rad_limited_emergency = yes
```

### Expansion under Permanent Emergency

`ISR70_rad_permanent_emergency` | x=145, y=31 | 70 days

Prerequisites: (ISR70_rad_no_expulsion OR ISR70_rad_expulsion).

Exclusive with: ISR70_rad_limited_emergency.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Choose a permanent emergency explicitly. Suspend elections, gain 5 further points of occupied factory access, and pay +10% police and +10% personnel costs. Neither party membership nor the population-policy choice enacts this automatically.

- Choose a permanent emergency explicitly. Suspend elections, gain 5 further points of occupied factory access, and pay +10% police and +10% personnel costs. Neither party membership nor the population-policy choice enacts this automatically.

```hoi4
ISR70_policy_complete_rad_permanent_emergency = yes
```

## Settlement Presence and Territorial Development

Unilateral settlement encroachment beyond Israeli control, or funded development under Israeli control.

### Settlement Division Networks

`ISR70_external_associations` | x=67, y=36 | 21 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Settlement departments, cooperative associations and private patrons can finance civilian footholds beyond Israel's military perimeter. Unilateral expansion creates competing land claims and imposes costs on the affected administration.

- Treasury: -0.2% of annual GDP.
- Small and Medium Business Owners Opinion: +5.

```hoi4
ISR70_policy_complete_external_associations = yes
```

### Settlement Engineering Department

`ISR70_controlled_settlement_engineering` | x=67, y=40 | 21 days

Prerequisites: (ISR70_territorial_policy).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Surveyors, water engineers and settlement departments can prepare funded agricultural sites and access roads in areas under Israeli control. Each project carries its own security and public-service commitment.

- Treasury: -0.2% of annual GDP.
- 1 x 25% construction research bonus.

```hoi4
ISR70_policy_complete_controlled_settlement_engineering = yes
```

### Establish a West Bank Settlement Foothold

`ISR70_presence_west_bank` | x=61, y=38 | 35 days

Prerequisites: (ISR70_external_associations).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Finance Israeli settlement holdings and protected commercial links in West Bank without the consent of the government controlling the area. These illegal settlements impose land, production and administrative burdens on that government. Israel assumes the financial and security commitment.

- Israel: "West Bank: Israeli Settlement Holdings": Office Productivity +4%, Agricultural Productivity +3%, Social Costs +1%, Bureaucracy Cost +1%, Police Cost +2%, Personnel Cost +1%.
- Affected government: "West Bank: Settlement Encroachment": Agricultural Productivity -3%, Bureaucracy Cost +2.5%, Police Cost +2%, Stability -1%.
- West Bank: "Israeli Settlement Encroachment": Local Infrastructure Construction Speed -10%, Local Factory Access -5%, Local Supplies -5%.
- Israel Treasury: -1% of annual GDP for initial establishment.
- Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%.

```hoi4
ISR70_policy_complete_presence_west_bank = yes
```

### Develop Settlement Sites in West Bank

`ISR70_develop_west_bank` | x=61, y=42 | 35 days

Prerequisites: (ISR70_controlled_settlement_engineering).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund an agricultural site, an access road and a protected local position in West Bank. The resulting assets remain in the state; their security perimeter adds to the burden of occupation.

- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in the West Bank; +1 infrastructure levels in the West Bank; +1 land fort levels in the West Bank; +3 shared building slots. Local effects: Local Supplies for Controller: +10%; Local Garrison Requirement: +10%. Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "West Bank: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_develop_west_bank = yes
```

### Establish a Gaza Settlement Foothold

`ISR70_presence_gaza` | x=65, y=38 | 35 days

Prerequisites: (ISR70_external_associations).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Finance Israeli settlement holdings and protected commercial links in Gaza without the consent of the government controlling the area. These illegal settlements impose land, production and administrative burdens on that government. Israel assumes the financial and security commitment.

- Israel: "Gaza: Israeli Settlement Holdings": Office Productivity +4%, Agricultural Productivity +3%, Social Costs +1%, Bureaucracy Cost +1%, Police Cost +2%, Personnel Cost +1%.
- Affected government: "Gaza: Settlement Encroachment": Agricultural Productivity -3%, Bureaucracy Cost +2.5%, Police Cost +2%, Stability -1%.
- Gaza: "Israeli Settlement Encroachment": Local Infrastructure Construction Speed -10%, Local Factory Access -5%, Local Supplies -5%.
- Israel Treasury: -1% of annual GDP for initial establishment.
- Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%.

```hoi4
ISR70_policy_complete_presence_gaza = yes
```

### Develop Settlement Sites in Gaza

`ISR70_develop_gaza` | x=65, y=42 | 35 days

Prerequisites: (ISR70_controlled_settlement_engineering).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund an agricultural site, an access road and a protected local position in Gaza. The resulting assets remain in the state; their security perimeter adds to the burden of occupation.

- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in Gaza; +1 infrastructure levels in Gaza; +1 land fort levels in Gaza; +3 shared building slots. Local effects: Local Supplies for Controller: +10%; Local Garrison Requirement: +10%. Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -2%, Political Power Gain -2.5%, Office Productivity -4%, Bureaucracy Cost +4%, Social Costs +3%. Extensive settlement network: Palestine, if present: "Gaza: Territorial and Settlement Pressures": Stability -4%, Political Power Gain -5%, Office Productivity -8%, Bureaucracy Cost +8%, Social Costs +6%.

```hoi4
ISR70_policy_complete_develop_gaza = yes
```

### Establish a Sinai Settlement Foothold

`ISR70_presence_sinai` | x=69, y=38 | 35 days

Prerequisites: (ISR70_external_associations).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Finance Israeli settlement holdings and protected commercial links in Sinai without the consent of the government controlling the area. These illegal settlements impose land, production and administrative burdens on that government. Israel assumes the financial and security commitment.

- Israel: "Sinai: Israeli Settlement Holdings": Office Productivity +4%, Agricultural Productivity +3%, Social Costs +1%, Bureaucracy Cost +1%, Police Cost +2%, Personnel Cost +1%.
- Affected government: "Sinai: Settlement Encroachment": Agricultural Productivity -3%, Bureaucracy Cost +2.5%, Police Cost +2%, Stability -1%.
- Sinai: "Israeli Settlement Encroachment": Local Infrastructure Construction Speed -10%, Local Factory Access -5%, Local Supplies -5%.
- Israel Treasury: -1% of annual GDP for initial establishment.

```hoi4
ISR70_policy_complete_presence_sinai = yes
```

### Develop Settlement Sites in Sinai

`ISR70_develop_sinai` | x=69, y=42 | 35 days

Prerequisites: (ISR70_controlled_settlement_engineering).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund an agricultural site, an access road and a protected local position in Sinai. The resulting assets remain in the state; their security perimeter adds to the burden of occupation.

- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in Sinai; +1 infrastructure levels in Sinai; +1 land fort levels in Sinai; +3 shared building slots. Local effects: Local Supplies for Controller: +10%; Local Garrison Requirement: +10%.

```hoi4
ISR70_policy_complete_develop_sinai = yes
```

### Establish a Golan Settlement Foothold

`ISR70_presence_golan` | x=73, y=38 | 35 days

Prerequisites: (ISR70_external_associations).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Finance Israeli settlement holdings and protected commercial links in Golan without the consent of the government controlling the area. These illegal settlements impose land, production and administrative burdens on that government. Israel assumes the financial and security commitment.

- Israel: "Golan: Israeli Settlement Holdings": Office Productivity +4%, Agricultural Productivity +3%, Social Costs +1%, Bureaucracy Cost +1%, Police Cost +2%, Personnel Cost +1%.
- Affected government: "Golan: Settlement Encroachment": Agricultural Productivity -3%, Bureaucracy Cost +2.5%, Police Cost +2%, Stability -1%.
- Golan: "Israeli Settlement Encroachment": Local Infrastructure Construction Speed -10%, Local Factory Access -5%, Local Supplies -5%.
- Israel Treasury: -1% of annual GDP for initial establishment.

```hoi4
ISR70_policy_complete_presence_golan = yes
```

### Develop Settlement Sites in Golan

`ISR70_develop_golan` | x=73, y=42 | 35 days

Prerequisites: (ISR70_controlled_settlement_engineering).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund an agricultural site, an access road and a protected local position in Golan. The resulting assets remain in the state; their security perimeter adds to the burden of occupation.

- Treasury: -1.5% of annual GDP. Completion: 270 days. +1 agricultural districts in 587; +1 infrastructure levels in 587; +1 land fort levels in 587; +3 shared building slots. Local effects: Local Supplies for Controller: +10%; Local Garrison Requirement: +10%.

```hoi4
ISR70_policy_complete_develop_golan = yes
```

## Validation

Run `python tools/israel_1970/build_content.py` followed by `python tools/israel_1970/validate_content.py`. Static validation covers references, syntax, assets, party restrictions, programme routes, treasury reservations, negotiations and scenario integration. It does not replace an HOI4 engine test.
