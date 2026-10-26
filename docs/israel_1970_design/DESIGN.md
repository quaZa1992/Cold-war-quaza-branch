# Israel 1970: Implemented Focus Tree

389 focuses, 161 decisions, 67 events, twenty political families and thirty-seven named party/list variants. All new game localisation is English.

The compact layout uses relative-position anchors as in the MD Russia tree. Each political family starts directly when its exact party governs. The twelve outlook unlocks and twenty government-mandate focuses have been removed. No party entry requires a focus or a foundation flag. Internal policy choices remain connected within their branches. Shared achievements survive changes of government; party programme modifiers apply only while that party governs.

Rewards were rewritten individually in revision 2. Party policies combine visible MD-style modifier changes with buildings, research, experience, interest-group approval and real constitutional choices. Descriptions contain narrative text; the game shows rewards through completion-effect tooltips. There is no generic 65/35 modifier split.

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

`ISR70_january_1970` | x=34, y=0 | 14 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Set the cabinet agenda for the new decade and release political capital for the first reforms.

- Political Power: +100

```hoi4
add_political_power = 100
```

### The Seventh Knesset

`ISR70_knesset` | x=34, y=1 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

The Seventh Knesset brings together the parties elected in October 1969. Parliamentary committees and a working legislative agenda must give the new government a durable basis for reform.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### Negotiate a Unity Cabinet

`ISR70_unity_cabinet` | x=32, y=2 | 35 days

Prerequisites: (ISR70_knesset).

Exclusive with: ISR70_narrow_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Replace the fragile starting coalition with a negotiated unity agreement. Its broader support improves stability and military confidence.

- The Military Opinion: +5.
- Removes the national spirit "The Unity Government of 1969".
- Removes the national spirit "The Unity Government of 1969".
- National spirit:
- Stability: +5%
- Political Power Gain: +5%
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

### A Parliamentary Working Majority

`ISR70_narrow_cabinet` | x=36, y=2 | 35 days

Prerequisites: (ISR70_knesset).

Exclusive with: ISR70_unity_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

A smaller working majority leaves the cabinet more political room and gives organized labor a clearer role.

- Political Power: +75
- Labor Unions Opinion: +10.
- Removes the national spirit "The Unity Government of 1969".
- Removes the national spirit "The Unity Government of 1969".
- National spirit:
- Political Power Gain: +10%
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

### A Professional Civil Service

`ISR70_civil_service` | x=34, y=3 | 35 days

Prerequisites: (ISR70_unity_cabinet OR ISR70_narrow_cabinet).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Professional recruitment and common procurement rules reduce the recurring cost of the civil service.

- Political Power: +50
- National spirit:
- Bureaucracy Cost: -10%

```hoi4
add_ideas = ISR70_civil_service_idea
add_political_power = 50
```

### The Comptroller and Parliamentary Oversight

`ISR70_oversight` | x=34, y=4 | 35 days

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

### Municipal Freedom of Action

`ISR70_local_councils` | x=31, y=4 | 35 days

Prerequisites: (ISR70_civil_service).

Exclusive with: ISR70_central_planning.

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Let local councils deliver roads and services faster without increasing the central bureaucracy.

- Small and Medium Business Owners Opinion: +5.
- National spirit:
- Infrastructure Construction Speed: +15%
- Bureaucracy Cost: -5%

```hoi4
add_ideas = ISR70_local_councils_idea
set_temp_variable = { temp_opinion = 5 }
change_small_medium_business_owners_opinion = yes
```

### Coordinated State Planning

`ISR70_central_planning` | x=37, y=4 | 35 days

Prerequisites: (ISR70_civil_service).

Exclusive with: ISR70_local_councils.

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Coordinate national tenders and engineering standards for a faster state construction programme.

- 1 x 50% research bonus: Construction.
- National spirit:
- Construction Speed: +5%

```hoi4
add_ideas = ISR70_central_planning_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### The Unfinished Basic Laws

`ISR70_basic_laws` | x=34, y=5 | 35 days

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

`ISR70_p0_institution` | x=11, y=17 | 35 days

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

### Religious Study and Vocational Education

`ISR70_p0_ea` | x=8, y=18 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_eb.

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Connect religious study to vocational education and industrial qualifications.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Religious Study and Vocational Education: Implementation

`ISR70_p0_ea_deepen` | x=8, y=19 | 49 days

Prerequisites: (ISR70_p0_ea).

Artwork: `gfx/interface/goals/coldwar/School_is_in.tga`.

Train technical teachers and improve the productivity of religious vocational graduates.

- Religious Institutions Opinion: +10.
- While this party governs:
- Monthly Productivity Growth: +0.05
- Education Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
add_to_variable = { ISR70_p0_education_cost_multiplier_modifier = -0.05 tooltip = education_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Municipal Religious Welfare

`ISR70_p0_eb` | x=10, y=18 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_ea.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Expand municipal religious welfare institutions and community provision.

- Religious Institutions Opinion: +10.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Municipal Religious Welfare: Implementation

`ISR70_p0_eb_deepen` | x=10, y=19 | 49 days

Prerequisites: (ISR70_p0_eb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund a development-town service network and infrastructure in the Negev.

- Stability: +2%
- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### Bnei Akiva and National Service

`ISR70_p0_ca` | x=12, y=18 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_cb.

Artwork: `gfx/interface/goals/coldwar/conscription.png`.

Link Bnei Akiva and national service to military preparation.

- Army Experience: +25
- While this party governs:
- Mobilization Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_mobilization_speed = 0.1 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### Bnei Akiva and National Service: Implementation

`ISR70_p0_ca_deepen` | x=12, y=19 | 49 days

Prerequisites: (ISR70_p0_ca).

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Professionalize the service framework and reduce the time needed for army training.

- Army Experience: +20
- While this party governs:
- Army Training Time: -5%
- Recruitable Population Factor: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_training_time_army_factor = -0.05 tooltip = training_time_army_factor_tt }
add_to_variable = { ISR70_p0_recruitable_population_factor = 0.03 tooltip = recruitable_population_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### Religious Settlement Policy

`ISR70_p0_cb` | x=14, y=18 | 35 days

Prerequisites: (ISR70_p0_institution).

Exclusive with: ISR70_p0_ca.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Religious Zionist organizations seek a lasting place in the settlement movement. Local organization and defense preparations will shape their contribution to national policy.

- Political Power: +75
- While this party governs:
- Division Defense: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_army_defence_factor = 0.05 tooltip = army_defence_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Religious Settlement Policy: Implementation

`ISR70_p0_cb_deepen` | x=14, y=19 | 49 days

Prerequisites: (ISR70_p0_cb).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Coordinate the defense and supply of border communities.

- Army Experience: +25
- While this party governs:
- Division Organization: +3%
- Supply Consumption: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p0_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p0_army_org_factor = 0.03 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p0_supply_consumption_factor = -0.05 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### Religion and the Republic

`ISR70_p0_finish` | x=11, y=20 | 70 days

Prerequisites: (ISR70_p0_ea_deepen OR ISR70_p0_eb_deepen) AND (ISR70_p0_ca_deepen OR ISR70_p0_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectHapoelHaMizrachi.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p1_institution` | x=21, y=10 | 35 days

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

### An Entrepreneurial Israel

`ISR70_p1_ea` | x=18, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_eb.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

Make private enterprise and commercial employment the engine of development.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### An Entrepreneurial Israel: Implementation

`ISR70_p1_ea_deepen` | x=18, y=12 | 49 days

Prerequisites: (ISR70_p1_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Build a funded commercial office district in Tel Aviv.

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

### Retain Strategic State Enterprises

`ISR70_p1_eb` | x=20, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

Retain strategic public enterprises while improving their industrial methods.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Factory Output: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Retain Strategic State Enterprises: Implementation

`ISR70_p1_eb_deepen` | x=20, y=12 | 49 days

Prerequisites: (ISR70_p1_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Expand Haifa's civilian industrial base under strategic state ownership.

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

### The Rule of Law and Opposition

`ISR70_p1_ca` | x=22, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_cb.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Defend the rule of law and subject the government to effective scrutiny.

- Political Power: +75
- Reduces existing MD corruption by one level, down to its minimum.

```hoi4
decrease_corruption = yes
add_political_power = 75
```

### The Rule of Law and Opposition: Implementation

`ISR70_p1_ca_deepen` | x=22, y=12 | 49 days

Prerequisites: (ISR70_p1_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Entrench parliamentary safeguards and a more efficient civilian administration.

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

### Indivisible Security Interests

`ISR70_p1_cb` | x=24, y=11 | 35 days

Prerequisites: (ISR70_p1_institution).

Exclusive with: ISR70_p1_ca.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Make security interests the center of the government's civic mandate.

- Army Experience: +30
- While this party governs:
- War Support: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_war_support_factor = 0.05 tooltip = war_support_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Indivisible Security Interests: Implementation

`ISR70_p1_cb_deepen` | x=24, y=12 | 49 days

Prerequisites: (ISR70_p1_cb).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Fund a more cohesive force with better operational supply.

- Army Experience: +20
- While this party governs:
- Division Organization: +5%
- Supply Consumption: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p1_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p1_army_org_factor = 0.05 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p1_supply_consumption_factor = -0.05 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### The Conservative Transfer of Power

`ISR70_p1_finish` | x=21, y=13 | 70 days

Prerequisites: (ISR70_p1_ea_deepen OR ISR70_p1_eb_deepen) AND (ISR70_p1_ca_deepen OR ISR70_p1_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_gahal_identity` | x=15, y=11 | 35 days

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

`ISR70_gahal_coalition` | x=14, y=12 | 35 days

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

`ISR70_likud_foundation` | x=16, y=12 | 35 days

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

`ISR70_p2_institution` | x=19, y=17 | 35 days

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

### Small Business over Monopolies

`ISR70_p2_ea` | x=16, y=18 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Prioritize small businesses over protected monopolies.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Small Business over Monopolies: Implementation

`ISR70_p2_ea_deepen` | x=16, y=19 | 49 days

Prerequisites: (ISR70_p2_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Build a Tel Aviv office district serving small firms and local commerce.

- +1 Office District in Tel Aviv.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Capital and Export Industry

`ISR70_p2_eb` | x=18, y=18 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_ea.

Artwork: `gfx/interface/goals/coldwar/export_factories.tga`.

Support capital formation and manufacturers that compete in export markets.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Return on Investment: +0.5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_return_on_investment_modifier = 0.005 tooltip = return_on_investment_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Capital and Export Industry: Implementation

`ISR70_p2_eb_deepen` | x=18, y=19 | 49 days

Prerequisites: (ISR70_p2_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Build a civilian factory in Haifa and modernize production methods.

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

### Entrench Civil Rights

`ISR70_p2_ca` | x=20, y=18 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_cb.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Entrench civil rights through accountable parliamentary institutions.

- Political Power: +50
- Stability: +3%
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
add_political_power = 50
```

### Entrench Civil Rights: Implementation

`ISR70_p2_ca_deepen` | x=20, y=19 | 49 days

Prerequisites: (ISR70_p2_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Enforce those rights through audits and a lower-cost civil service.

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

### A Liberal Security State

`ISR70_p2_cb` | x=22, y=18 | 35 days

Prerequisites: (ISR70_p2_institution).

Exclusive with: ISR70_p2_ca.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

A liberal security policy emphasizes professional planning and trained reserves.

- Army Experience: +30
- While this party governs:
- Planning Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_planning_speed = 0.1 tooltip = planning_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### A Liberal Security State: Implementation

`ISR70_p2_cb_deepen` | x=22, y=19 | 49 days

Prerequisites: (ISR70_p2_cb).

Artwork: `gfx/interface/goals/israel_palestine/the_research_department.dds`.

Invest in defensive analysis and secure communications.

- 1 x 50% research bonus: Encryption.
- While this party governs:
- Foreign Influence Defense: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p2_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p2_foreign_influence_defense_modifier = 0.1 tooltip = foreign_influence_defense_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_encryption uses = 1 bonus = 0.5 }
```

### A Liberal Republic

`ISR70_p2_finish` | x=19, y=20 | 70 days

Prerequisites: (ISR70_p2_ea_deepen OR ISR70_p2_eb_deepen) AND (ISR70_p2_ca_deepen OR ISR70_p2_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p3_institution` | x=9, y=10 | 35 days

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

### Modernize the Histadrut

`ISR70_p3_ea` | x=6, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_eb.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Modernize Histadrut enterprises through negotiated production and workplace reform.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Modernize the Histadrut: Implementation

`ISR70_p3_ea_deepen` | x=6, y=12 | 49 days

Prerequisites: (ISR70_p3_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Add a modern civilian industrial complex in Haifa as the programme's concrete investment.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Kibbutzim as Development Centers

`ISR70_p3_eb` | x=8, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_ea.

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Use kibbutzim as agricultural development and technical-training centers.

- 1 x 50% research bonus: Agriculture.
- Farmers Opinion: +10.
- While this party governs:
- Agricultural District Construction Speed: +15%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_speed_agriculture_district_factor = 0.15 tooltip = production_speed_agriculture_district_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
```

### Kibbutzim as Development Centers: Implementation

`ISR70_p3_eb_deepen` | x=8, y=12 | 49 days

Prerequisites: (ISR70_p3_eb).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Create an irrigated agricultural district in the Negev and improve rural productivity.

- +1 Agricultural District in the Negev.
- Treasury cost on completion: 0.8% of annual GDP.
- While this party governs:
- Monthly Productivity Growth: +0.05

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_productivity_growth_modifier = 0.05 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = agriculture_district level = 1 instant_build = yes }
}
ISR70_pay_0_0080 = yes
```

### Social Balance in the Cities

`ISR70_p3_ca` | x=10, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_cb.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Make urban social balance and development-town provision a cabinet priority.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Social Balance in the Cities: Implementation

`ISR70_p3_ca_deepen` | x=10, y=12 | 49 days

Prerequisites: (ISR70_p3_ca).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Fund local services and development-town infrastructure.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Security through Negotiating Strength

`ISR70_p3_cb` | x=12, y=11 | 35 days

Prerequisites: (ISR70_p3_institution).

Exclusive with: ISR70_p3_ca.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Use organized military readiness as the basis for negotiations from strength.

- Army Experience: +30
- While this party governs:
- Division Organization: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_army_org_factor = 0.05 tooltip = ISR70_army_org_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Security through Negotiating Strength: Implementation

`ISR70_p3_cb_deepen` | x=12, y=12 | 49 days

Prerequisites: (ISR70_p3_cb).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Strengthen diplomatic independence and give the cabinet political room to negotiate.

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

`ISR70_p3_finish` | x=9, y=13 | 70 days

Prerequisites: (ISR70_p3_ea_deepen OR ISR70_p3_eb_deepen) AND (ISR70_p3_ca_deepen OR ISR70_p3_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectMapai.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_alignment_balance` | x=3, y=11 | 35 days

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

### Include the Unions in Modernization

`ISR70_golda_labour` | x=2, y=12 | 35 days

Prerequisites: (ISR70_alignment_balance).

Exclusive with: ISR70_golda_manager.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Modernize Histadrut enterprises through negotiated workplace standards and worker training.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%
- Monthly Productivity Growth: +0.1

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
add_to_variable = { ISR70_p3_productivity_growth_modifier = 0.1 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Professional Enterprise Management

`ISR70_golda_manager` | x=4, y=12 | 35 days

Prerequisites: (ISR70_alignment_balance).

Exclusive with: ISR70_golda_labour.

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Give professional managers clearer production targets and invest in modern industrial methods.

- 1 x 50% research bonus: Industry.
- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Factory Output: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### Take the Social Protest Seriously

`ISR70_golda_panthers` | x=3, y=13 | 35 days

Prerequisites: (ISR70_golda_labour OR ISR70_golda_manager).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

The development towns demand a hearing on housing, schools and access to work. The cabinet must decide how to respond to a growing protest movement.

- Political Power: +50
- Stability: +3%
- Opens the corresponding cabinet or municipal event.

```hoi4
add_political_power = 50
add_stability = 0.03
country_event = { id = ISR70.20 days = 1 }
```

### Housing for the Development Towns

`ISR70_golda_housing` | x=3, y=14 | 35 days

Prerequisites: (ISR70_golda_panthers).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund development-town housing and local infrastructure, reducing the cost of future social provision.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
206 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Leadership after Golda

`ISR70_golda_succession` | x=9, y=14 | 35 days

Prerequisites: (ISR70_p3_finish).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Golda Meir holds the Alignment together, but Rabin and Peres offer different visions for its future. The party must settle who will lead its next cabinet.

- Political Power: +75
- Opens a leadership event: retain Golda Meir, choose Yitzhak Rabin, or choose Shimon Peres.

```hoi4
add_political_power = 75
country_event = { id = ISR70.30 days = 1 }
custom_effect_tooltip = ISR70_golda_succession_outcome_tt
```

### Rabin's Reform Cabinet

`ISR70_rabin_cabinet` | x=8, y=15 | 35 days

Prerequisites: (ISR70_golda_succession).

Exclusive with: ISR70_peres_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

A Rabin cabinet emphasizes professional administration and readiness, with a one-level anti-corruption reform.

- Army Experience: +25
- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
army_experience = 25
```

### Peres and the Industrial Future

`ISR70_peres_cabinet` | x=10, y=15 | 35 days

Prerequisites: (ISR70_golda_succession).

Exclusive with: ISR70_rabin_cabinet.

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

A Peres cabinet emphasizes industrial modernization and domestic defense engineering.

- 1 x 50% research bonus: Armor.
- 1 x 50% research bonus: Aircraft.
- While this party governs:
- Military Factory Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p3_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p3_production_speed_arms_factory_factor = 0.1 tooltip = production_speed_arms_factory_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 1 bonus = 0.5 }
add_tech_bonus = { name = ISR70_research_programme category = CAT_aircraft uses = 1 bonus = 0.5 }
```

## Rakah - The Communist Course

A Jewish-Arab communist government is an alternative electoral outcome. Parliamentary socialism and Soviet alignment remain separate decisions.

### A Jewish-Arab Class Alliance

`ISR70_p4_institution` | x=32, y=7 | 35 days

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

### Parliamentary Communism

`ISR70_p4_ea` | x=29, y=8 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_eb.

Artwork: `gfx/interface/goals/coldwar/Democratic_Socialism.tga`.

Commit parliamentary communism to organized labor and accountable public production.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Parliamentary Communism: Implementation

`ISR70_p4_ea_deepen` | x=29, y=9 | 49 days

Prerequisites: (ISR70_p4_ea).

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Train workers and strengthen the productivity of parliamentary public enterprises.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.1

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_productivity_growth_modifier = 0.1 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### A Central Economic Plan

`ISR70_p4_eb` | x=31, y=8 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_ea.

Artwork: `gfx/interface/goals/coldwar/Centrally_Planned_Economy.tga`.

Coordinate industrial construction through a central economic plan.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Civilian Industry Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_production_speed_industrial_complex_factor = 0.1 tooltip = production_speed_industrial_complex_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### A Central Economic Plan: Implementation

`ISR70_p4_eb_deepen` | x=31, y=9 | 49 days

Prerequisites: (ISR70_p4_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Build a funded public industrial complex in Haifa.

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

### Equal Citizens

`ISR70_p4_ca` | x=33, y=8 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Make equal citizenship the legal basis of the Jewish-Arab class alliance.

- Political Power: +75
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Equal Citizens: Implementation

`ISR70_p4_ca_deepen` | x=33, y=9 | 49 days

Prerequisites: (ISR70_p4_ca).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Improve equal access to municipal social provision.

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

### Soviet Security Cooperation

`ISR70_p4_cb` | x=35, y=8 | 35 days

Prerequisites: (ISR70_p4_institution).

Exclusive with: ISR70_p4_ca.

Artwork: `gfx/interface/goals/coldwar/generic_army_cooperation.png`.

Pursue Soviet-oriented security cooperation through contemporary training and assistance capacity.

- Army Experience: +25
- While this party governs:
- Cold War Assistance Effectiveness: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p4_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p4_mdcw_cw_support_effectiveness = 0.1 tooltip = ISR70_mdcw_cw_support_effectiveness_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 25
```

### Soviet Security Cooperation: Implementation

`ISR70_p4_cb_deepen` | x=35, y=9 | 49 days

Prerequisites: (ISR70_p4_cb).

Artwork: `gfx/interface/goals/coldwar/FocusImportSovietTanks.dds`.

Prepare the armored force for contemporary foreign designs without granting a free tank model.

- Army Experience: +20
- 2 x 50% research bonus: Armor.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 2 bonus = 0.5 }
army_experience = 20
```

### A Socialist Peace Settlement

`ISR70_p4_finish` | x=32, y=10 | 70 days

Prerequisites: (ISR70_p4_ea_deepen OR ISR70_p4_eb_deepen) AND (ISR70_p4_ca_deepen OR ISR70_p4_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p5_institution` | x=40, y=7 | 35 days

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

### Autonomous Producers' Councils

`ISR70_p5_ea` | x=37, y=8 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Give producers' councils practical control of workplace training and production.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Autonomous Producers' Councils: Implementation

`ISR70_p5_ea_deepen` | x=37, y=9 | 49 days

Prerequisites: (ISR70_p5_ea).

Artwork: `gfx/interface/goals/coldwar/generic_market_socialism.png`.

Spread council-led technical training and industrial research.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.1

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_productivity_growth_modifier = 0.1 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### A Coordinated Cooperative Federation

`ISR70_p5_eb` | x=39, y=8 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_ea.

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Coordinate the cooperative federation's agricultural and industrial investment.

- 1 x 50% research bonus: Agriculture.
- While this party governs:
- Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_production_speed_buildings_factor = 0.05 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
```

### A Coordinated Cooperative Federation: Implementation

`ISR70_p5_eb_deepen` | x=39, y=9 | 49 days

Prerequisites: (ISR70_p5_eb).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund a cooperative agricultural district in the Negev.

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

### Jewish-Arab Federalism

`ISR70_p5_ca` | x=41, y=8 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Define Jewish-Arab federalism through accountable municipal powers.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Jewish-Arab Federalism: Implementation

`ISR70_p5_ca_deepen` | x=41, y=9 | 49 days

Prerequisites: (ISR70_p5_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Protect local representation and the stability of the federal settlement.

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

### A Common Civic Republic

`ISR70_p5_cb` | x=43, y=8 | 35 days

Prerequisites: (ISR70_p5_institution).

Exclusive with: ISR70_p5_ca.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Build a common civic republic through equal public institutions.

- Stability: +3%
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p5_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p5_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### A Common Civic Republic: Implementation

`ISR70_p5_cb_deepen` | x=43, y=9 | 49 days

Prerequisites: (ISR70_p5_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Deliver common civic services rather than merely proclaiming them.

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

`ISR70_p5_finish` | x=40, y=10 | 70 days

Prerequisites: (ISR70_p5_ea_deepen OR ISR70_p5_eb_deepen) AND (ISR70_p5_ca_deepen OR ISR70_p5_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p6_institution` | x=32, y=12 | 35 days

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

### Crafts and Family Businesses

`ISR70_p6_ea` | x=29, y=13 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Give craftspeople and family businesses access to productive credit.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Crafts and Family Businesses: Implementation

`ISR70_p6_ea_deepen` | x=29, y=14 | 49 days

Prerequisites: (ISR70_p6_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Create a municipal commercial office district in the Negev.

- +1 Office District in the Negev.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
206 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Municipal Development Funds

`ISR70_p6_eb` | x=31, y=13 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_ea.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Direct development funds toward municipal services in the periphery.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Municipal Development Funds: Implementation

`ISR70_p6_eb_deepen` | x=31, y=14 | 49 days

Prerequisites: (ISR70_p6_eb).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Fund an additional infrastructure level for southern development towns.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Tradition and Shared Education

`ISR70_p6_ca` | x=33, y=13 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_cb.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Combine traditional institutions with shared vocational education.

- Religious Institutions Opinion: +10.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Tradition and Shared Education: Implementation

`ISR70_p6_ca_deepen` | x=33, y=14 | 49 days

Prerequisites: (ISR70_p6_ca).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Train teachers and skilled workers for the development towns.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.1

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_productivity_growth_modifier = 0.1 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Traditional Social Partnership

`ISR70_p6_cb` | x=35, y=13 | 35 days

Prerequisites: (ISR70_p6_institution).

Exclusive with: ISR70_p6_ca.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Negotiate a traditional social partnership between employers, workers and religious institutions.

- Labor Unions Opinion: +10.
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p6_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p6_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
```

### Traditional Social Partnership: Implementation

`ISR70_p6_cb_deepen` | x=35, y=14 | 49 days

Prerequisites: (ISR70_p6_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Use that partnership to improve community welfare administration.

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

`ISR70_p6_finish` | x=32, y=15 | 70 days

Prerequisites: (ISR70_p6_ea_deepen OR ISR70_p6_eb_deepen) AND (ISR70_p6_ca_deepen OR ISR70_p6_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p7_institution` | x=40, y=12 | 35 days

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

### A Technocratic Development Plan

`ISR70_p7_ea` | x=37, y=13 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_eb.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Build a technocratic development plan around transparent procurement and engineering.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### A Technocratic Development Plan: Implementation

`ISR70_p7_ea_deepen` | x=37, y=14 | 49 days

Prerequisites: (ISR70_p7_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Deliver a funded public industrial complex in Haifa.

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

### Patronage through State Corporations

`ISR70_p7_eb` | x=39, y=13 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

Use state corporations and favored contractors for rapid construction. Patronage increases corruption-related costs.

- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Civilian Industry Construction Speed: +15%
- Corruption Cost: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_production_speed_industrial_complex_factor = 0.15 tooltip = production_speed_industrial_complex_factor_tt }
add_to_variable = { ISR70_p7_corruption_cost_factor = 0.05 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### Patronage through State Corporations: Implementation

`ISR70_p7_eb_deepen` | x=39, y=14 | 49 days

Prerequisites: (ISR70_p7_eb).

Artwork: `gfx/interface/goals/coldwar/industrial_subsidies.tga`.

Deliver the state-corporation industrial programme and reward its sponsors.

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

### Return to Parliamentary Government

`ISR70_p7_ca` | x=41, y=13 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Restore elections and commit the directorate to parliamentary government.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = communism elections_allowed = yes }
add_political_power = 75
```

### Return to Parliamentary Government: Implementation

`ISR70_p7_ca_deepen` | x=41, y=14 | 49 days

Prerequisites: (ISR70_p7_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Submit the civilian transition to an effective audit and strengthen public confidence.

- Stability: +3%
- Reduces existing MD corruption by one level, down to its minimum.

```hoi4
decrease_corruption = yes
add_stability = 0.03
```

### Permanent Presidential Rule

`ISR70_p7_cb` | x=43, y=13 | 35 days

Prerequisites: (ISR70_p7_institution).

Exclusive with: ISR70_p7_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

Establish permanent presidential rule and suspend ordinary elections.

- Political Power: +75
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = communism elections_allowed = no }
add_political_power = 75
```

### Permanent Presidential Rule: Implementation

`ISR70_p7_cb_deepen` | x=43, y=14 | 49 days

Prerequisites: (ISR70_p7_cb).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Centralize presidential administration and construction planning.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -5%
- Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p7_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p7_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p7_production_speed_buildings_factor = 0.05 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### The Directorate State

`ISR70_p7_finish` | x=40, y=15 | 70 days

Prerequisites: (ISR70_p7_ea_deepen OR ISR70_p7_eb_deepen) AND (ISR70_p7_ca_deepen OR ISR70_p7_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p12_institution` | x=49, y=7 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Represent municipal interests through parliamentary negotiation and accountable local institutions.

- Political Power: +75
- Stability: +3%

```hoi4
add_stability = 0.03
add_political_power = 75
```

### Arab Commercial Centers

`ISR70_p12_ea` | x=46, y=8 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_eb.

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Build Arab commercial centers around local enterprise and parliamentary representation.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Arab Commercial Centers: Implementation

`ISR70_p12_ea_deepen` | x=46, y=9 | 49 days

Prerequisites: (ISR70_p12_ea).

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

Fund an office district serving northern municipal commerce.

- +1 Office District in Haifa.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### Social Endowments and Municipal Aid

`ISR70_p12_eb` | x=48, y=8 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_ea.

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Use social endowments for municipal welfare and charitable provision.

- Stability: +2%
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.02
```

### Social Endowments and Municipal Aid: Implementation

`ISR70_p12_eb_deepen` | x=48, y=9 | 49 days

Prerequisites: (ISR70_p12_eb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Improve the roads and public-service links used by municipal institutions.

- Stability: +2%
- +1 Infrastructure level in Haifa.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
205 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### Integration into the Civic Order

`ISR70_p12_ca` | x=50, y=8 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_cb.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Integrate the municipal reform movement into common civic institutions.

- Political Power: +75
- Stability: +2%
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
add_stability = 0.02
```

### Integration into the Civic Order: Implementation

`ISR70_p12_ca_deepen` | x=50, y=9 | 49 days

Prerequisites: (ISR70_p12_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Make common civic institutions accountable through a public audit.

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

### Autonomous Municipal Institutions

`ISR70_p12_cb` | x=52, y=8 | 35 days

Prerequisites: (ISR70_p12_institution).

Exclusive with: ISR70_p12_ca.

Artwork: `gfx/interface/goals/israel_palestine/gaza_civic_organizations.dds`.

Give municipal institutions greater administrative autonomy.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Autonomous Municipal Institutions: Implementation

`ISR70_p12_cb_deepen` | x=52, y=9 | 49 days

Prerequisites: (ISR70_p12_cb).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Improve autonomous municipal services and community confidence.

- Stability: +4%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p12_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p12_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.04
```

### A Political Voice for the Municipalities

`ISR70_p12_finish` | x=49, y=10 | 70 days

Prerequisites: (ISR70_p12_ea_deepen OR ISR70_p12_eb_deepen) AND (ISR70_p12_ca_deepen OR ISR70_p12_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p13_institution` | x=57, y=7 | 35 days

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

### Vocational Education and Religious Study

`ISR70_p13_ea` | x=54, y=8 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_eb.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Connect religious study and vocational qualifications without treating Orthodox representation as a dictatorship.

- Religious Institutions Opinion: +10.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Vocational Education and Religious Study: Implementation

`ISR70_p13_ea_deepen` | x=54, y=9 | 49 days

Prerequisites: (ISR70_p13_ea).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Fund technical training alongside religious study.

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

### Community Social Provision

`ISR70_p13_eb` | x=56, y=8 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_ea.

Artwork: `gfx/interface/goals/coldwar/Generic_Working_Class_Family.tga`.

Expand community social provision and local welfare institutions.

- Religious Institutions Opinion: +10.
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_priesthood_opinion = yes
```

### Community Social Provision: Implementation

`ISR70_p13_eb_deepen` | x=56, y=9 | 49 days

Prerequisites: (ISR70_p13_eb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Professionalize community healthcare and charitable administration.

- Stability: +3%
- While this party governs:
- Healthcare Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_health_cost_multiplier_modifier = -0.05 tooltip = health_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### The Religious Status Quo

`ISR70_p13_ca` | x=58, y=8 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_cb.

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Renew the religious status quo through parliamentary negotiation.

- Religious Institutions Opinion: +15.
- While this party governs:
- Stability: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_stability_factor = 0.05 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_the_priesthood_opinion = yes
```

### The Religious Status Quo: Implementation

`ISR70_p13_ca_deepen` | x=58, y=9 | 49 days

Prerequisites: (ISR70_p13_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Give the compromise a durable parliamentary settlement.

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

### Voluntary Civilian Service

`ISR70_p13_cb` | x=60, y=8 | 35 days

Prerequisites: (ISR70_p13_institution).

Exclusive with: ISR70_p13_ca.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Develop voluntary civilian service that respects the movement's religious institutions.

- Stability: +3%
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p13_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p13_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Voluntary Civilian Service: Implementation

`ISR70_p13_cb_deepen` | x=60, y=9 | 49 days

Prerequisites: (ISR70_p13_cb).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund service links for development-town communities.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### A Sustainable Religious Compromise

`ISR70_p13_finish` | x=57, y=10 | 70 days

Prerequisites: (ISR70_p13_ea_deepen OR ISR70_p13_eb_deepen) AND (ISR70_p13_ca_deepen OR ISR70_p13_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p14_institution` | x=65, y=7 | 35 days

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

### Professional State Enterprises

`ISR70_p14_ea` | x=62, y=8 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_eb.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Professionalize state enterprises through clear procurement and production rules.

- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### Professional State Enterprises: Implementation

`ISR70_p14_ea_deepen` | x=62, y=9 | 49 days

Prerequisites: (ISR70_p14_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Expand the civilian industrial base in Haifa under professional management.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Promote Private Enterprise

`ISR70_p14_eb` | x=64, y=8 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_ea.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

Promote private enterprise and competitive investment.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Promote Private Enterprise: Implementation

`ISR70_p14_eb_deepen` | x=64, y=9 | 49 days

Prerequisites: (ISR70_p14_eb).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Fund a Tel Aviv office district for private commerce.

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

### Security Pragmatism

`ISR70_p14_ca` | x=66, y=8 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_cb.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Pursue pragmatic security through trained forces and defensive planning.

- Army Experience: +30
- While this party governs:
- Division Defense: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_army_defence_factor = 0.05 tooltip = army_defence_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Security Pragmatism: Implementation

`ISR70_p14_ca_deepen` | x=66, y=9 | 49 days

Prerequisites: (ISR70_p14_ca).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Improve the practical supply burden of that defensive posture.

- Army Experience: +20
- While this party governs:
- Supply Consumption: -8%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_supply_consumption_factor = -0.08 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 20
```

### Territorial Negotiations

`ISR70_p14_cb` | x=68, y=8 | 35 days

Prerequisites: (ISR70_p14_institution).

Exclusive with: ISR70_p14_ca.

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Give territorial negotiators a pragmatic cabinet mandate. This does not impose an agreement on a neighbor.

- Political Power: +100
- While this party governs:
- Foreign Influence Defense: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p14_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p14_foreign_influence_defense_modifier = 0.1 tooltip = foreign_influence_defense_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### Territorial Negotiations: Implementation

`ISR70_p14_cb_deepen` | x=68, y=9 | 49 days

Prerequisites: (ISR70_p14_cb).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Build public confidence around a negotiated territorial policy.

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

`ISR70_p14_finish` | x=65, y=10 | 70 days

Prerequisites: (ISR70_p14_ea_deepen OR ISR70_p14_eb_deepen) AND (ISR70_p14_ca_deepen OR ISR70_p14_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p15_institution` | x=73, y=7 | 35 days

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

### Diaspora Capital with Oversight

`ISR70_p15_ea` | x=70, y=8 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Channel diaspora capital through supervised and published investment contracts.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Imperia Investment Reward: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_imp_investment_reward = 0.1 tooltip = ISR70_imp_investment_reward_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Diaspora Capital with Oversight: Implementation

`ISR70_p15_ea_deepen` | x=70, y=9 | 49 days

Prerequisites: (ISR70_p15_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Build a supervised commercial office district in Tel Aviv.

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

### Privileged Concessions

`ISR70_p15_eb` | x=72, y=8 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_ea.

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

Accelerate investment through privileged concessions. The price is higher corruption-related expenditure.

- Industrial Conglomerates Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -15%
- Corruption Cost: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_receiving_investment_cost_modifier = -0.15 tooltip = receiving_investment_cost_modifier_tt }
add_to_variable = { ISR70_p15_corruption_cost_factor = 0.05 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_industrial_conglomerates_opinion = yes
```

### Privileged Concessions: Implementation

`ISR70_p15_eb_deepen` | x=72, y=9 | 49 days

Prerequisites: (ISR70_p15_eb).

Artwork: `gfx/interface/goals/coldwar/industrial_subsidies.tga`.

Fund an industrial concession in Haifa and improve the sponsors' production methods.

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

### Transparent Investment Contracts

`ISR70_p15_ca` | x=74, y=8 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_cb.

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Require public oversight of investment contracts and concession income.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Corruption Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_corruption_cost_factor = -0.05 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Transparent Investment Contracts: Implementation

`ISR70_p15_ca_deepen` | x=74, y=9 | 49 days

Prerequisites: (ISR70_p15_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Professionalize contract administration and lower recurring bureaucratic costs.

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

### Political Patronage Networks

`ISR70_p15_cb` | x=76, y=8 | 35 days

Prerequisites: (ISR70_p15_institution).

Exclusive with: ISR70_p15_ca.

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites2.png`.

Build patronage networks that secure political capacity at the expense of clean public spending.

- Political Power: +75
- While this party governs:
- Political Power Gain: +10%
- Corruption Cost: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_political_power_factor = 0.1 tooltip = political_power_factor_tt }
add_to_variable = { ISR70_p15_corruption_cost_factor = 0.05 tooltip = corruption_cost_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Political Patronage Networks: Implementation

`ISR70_p15_cb_deepen` | x=76, y=9 | 49 days

Prerequisites: (ISR70_p15_cb).

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

Consolidate the political investment network and its construction programme.

- Political Power: +50
- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Office Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p15_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p15_production_speed_offices_factor = 0.1 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
add_political_power = 50
```

### The Investment State

`ISR70_p15_finish` | x=73, y=10 | 70 days

Prerequisites: (ISR70_p15_ea_deepen OR ISR70_p15_eb_deepen) AND (ISR70_p15_ca_deepen OR ISR70_p15_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/collaborate_local_elites.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p16_institution` | x=49, y=12 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Defend a free press and open political organization as the foundation of a secular civil-rights programme.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### A Civil-Rights Reform Economy

`ISR70_p16_ea` | x=46, y=13 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Combine a civil-rights reform economy with investment access and public education.

- Small and Medium Business Owners Opinion: +10.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### A Civil-Rights Reform Economy: Implementation

`ISR70_p16_ea_deepen` | x=46, y=14 | 49 days

Prerequisites: (ISR70_p16_ea).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Improve technical qualifications and research in civilian electronics.

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

### Radical Debureaucratization

`ISR70_p16_eb` | x=48, y=13 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_ea.

Artwork: `gfx/interface/goals/coldwar/generic_privatization.png`.

Cut routine bureaucracy and let private firms enter services more easily.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Radical Debureaucratization: Implementation

`ISR70_p16_eb_deepen` | x=48, y=14 | 49 days

Prerequisites: (ISR70_p16_eb).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Create commercial capacity through a funded Tel Aviv office district.

- +1 Office District in Tel Aviv.
- Treasury cost on completion: 1.2% of annual GDP.
- While this party governs:
- Office Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_production_speed_offices_factor = 0.05 tooltip = production_speed_offices_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
```

### A Secular Civic State

`ISR70_p16_ca` | x=50, y=13 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_cb.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Establish secular civic institutions and a free public sphere.

- Stability: +3%
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### A Secular Civic State: Implementation

`ISR70_p16_ca_deepen` | x=50, y=14 | 49 days

Prerequisites: (ISR70_p16_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Enforce secular accountability through an independent public audit.

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

### Decentralized Municipalities

`ISR70_p16_cb` | x=52, y=13 | 35 days

Prerequisites: (ISR70_p16_institution).

Exclusive with: ISR70_p16_ca.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Decentralize public decisions to elected municipalities.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p16_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p16_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Decentralized Municipalities: Implementation

`ISR70_p16_cb_deepen` | x=52, y=14 | 49 days

Prerequisites: (ISR70_p16_cb).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Fund municipal links and practical local services in the Negev.

- Stability: +2%
- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

### A State of Free Citizens

`ISR70_p16_finish` | x=49, y=15 | 70 days

Prerequisites: (ISR70_p16_ea_deepen OR ISR70_p16_eb_deepen) AND (ISR70_p16_ca_deepen OR ISR70_p16_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p17_institution` | x=57, y=12 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

Create professional institutions for landscape protection, water policy and development planning.

- Political Power: +50
- 1 x 50% research bonus: Agriculture.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
add_political_power = 50
```

### Water-Efficient Agriculture

`ISR70_p17_ea` | x=54, y=13 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_eb.

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

Use water-efficient agriculture as the basis of landscape protection.

- 1 x 50% research bonus: Agriculture.
- While this party governs:
- Agricultural District Construction Speed: +15%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_production_speed_agriculture_district_factor = 0.15 tooltip = production_speed_agriculture_district_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }
```

### Water-Efficient Agriculture: Implementation

`ISR70_p17_ea_deepen` | x=54, y=14 | 49 days

Prerequisites: (ISR70_p17_ea).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Fund a carefully planned agricultural district in the Negev.

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

### Clean Industry and Research

`ISR70_p17_eb` | x=56, y=13 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_ea.

Artwork: `gfx/interface/goals/coldwar/generic_electricity.png`.

Invest in cleaner industrial methods and energy-efficiency research.

- 1 x 50% research bonus: Energy Efficiency.
- While this party governs:
- Research Speed: +2%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_research_speed_factor = 0.02 tooltip = ISR70_research_speed_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.5 }
```

### Clean Industry and Research: Implementation

`ISR70_p17_eb_deepen` | x=56, y=14 | 49 days

Prerequisites: (ISR70_p17_eb).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Improve industrial repair and efficient production rather than simply increasing land use.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Industry Repair Speed: +15%
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_industry_repair_factor = 0.15 tooltip = ISR70_industry_repair_factor_tt }
add_to_variable = { ISR70_p17_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Municipal Conservation Planning

`ISR70_p17_ca` | x=58, y=13 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_cb.

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

Give municipalities professional conservation and land-use planning.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Municipal Conservation Planning: Implementation

`ISR70_p17_ca_deepen` | x=58, y=14 | 49 days

Prerequisites: (ISR70_p17_ca).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Apply conservation planning to public infrastructure delivery.

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

### Social and Environmental Infrastructure

`ISR70_p17_cb` | x=60, y=13 | 35 days

Prerequisites: (ISR70_p17_institution).

Exclusive with: ISR70_p17_ca.

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Combine environmental goals with social and public-transport provision.

- Stability: +3%
- While this party governs:
- Social Spending Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p17_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p17_social_cost_multiplier_modifier = -0.05 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
```

### Social and Environmental Infrastructure: Implementation

`ISR70_p17_cb_deepen` | x=60, y=14 | 49 days

Prerequisites: (ISR70_p17_cb).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Fund healthier local services and development-town infrastructure.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### A Livable Development Strategy

`ISR70_p17_finish` | x=57, y=15 | 70 days

Prerequisites: (ISR70_p17_ea_deepen OR ISR70_p17_eb_deepen) AND (ISR70_p17_ca_deepen OR ISR70_p17_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_agriculture.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p18_institution` | x=65, y=12 | 35 days

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

### A Cooperative Welfare State

`ISR70_p18_ea` | x=62, y=13 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_eb.

Artwork: `gfx/interface/goals/coldwar/Democratic_Socialism.tga`.

Build a cooperative welfare economy around organized labor.

- Labor Unions Opinion: +15.
- While this party governs:
- Social Spending Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_social_cost_multiplier_modifier = -0.1 tooltip = social_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### A Cooperative Welfare State: Implementation

`ISR70_p18_ea_deepen` | x=62, y=14 | 49 days

Prerequisites: (ISR70_p18_ea).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Modernization.dds`.

Fund a cooperative agricultural district in the Negev.

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

### Municipal Development and Education

`ISR70_p18_eb` | x=64, y=13 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_ea.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Prioritize municipal development and education over expanding the cooperative production sector.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Municipal Development and Education: Implementation

`ISR70_p18_eb_deepen` | x=64, y=14 | 49 days

Prerequisites: (ISR70_p18_eb).

Artwork: `gfx/interface/goals/coldwar/Universities.dds`.

Fund applied education and local infrastructure in the development towns.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### A Negotiated Peace

`ISR70_p18_ca` | x=66, y=13 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_cb.

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Give negotiated peace a clear parliamentary mandate.

- Political Power: +100
- While this party governs:
- Foreign Influence Defense: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_foreign_influence_defense_modifier = 0.1 tooltip = foreign_influence_defense_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### A Negotiated Peace: Implementation

`ISR70_p18_ca_deepen` | x=66, y=14 | 49 days

Prerequisites: (ISR70_p18_ca).

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Build confidence in the elected institutions that will scrutinize any peace agreement.

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

### A Binational Constitutional Convention

`ISR70_p18_cb` | x=68, y=13 | 35 days

Prerequisites: (ISR70_p18_institution).

Exclusive with: ISR70_p18_ca.

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

A binational constitutional convention would require equal civic institutions and representatives prepared to negotiate a common political settlement.

- Political Power: +100
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 100
```

### A Binational Constitutional Convention: Implementation

`ISR70_p18_cb_deepen` | x=68, y=14 | 49 days

Prerequisites: (ISR70_p18_cb).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Put civil rights and municipal accountability into the proposed constitutional settlement.

- Reduces existing MD corruption by one level, down to its minimum.
- While this party governs:
- Bureaucracy Cost: -5%
- Stability: +3%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p18_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p18_bureaucracy_cost_multiplier_modifier = -0.05 tooltip = bureaucracy_cost_multiplier_modifier_tt }
add_to_variable = { ISR70_p18_stability_factor = 0.03 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
decrease_corruption = yes
```

### Socialism and Equal Rights

`ISR70_p18_finish` | x=65, y=15 | 70 days

Prerequisites: (ISR70_p18_ea_deepen OR ISR70_p18_eb_deepen) AND (ISR70_p18_ca_deepen OR ISR70_p18_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/FocusElectMapam.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p19_institution` | x=73, y=12 | 35 days

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

### Jewish-Arab Industrial Enterprises

`ISR70_p19_ea` | x=70, y=13 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_eb.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Support Jewish-Arab industrial enterprises through common worker training.

- Labor Unions Opinion: +15.
- While this party governs:
- Production Efficiency Cap: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_production_factory_max_efficiency_factor = 0.05 tooltip = ISR70_production_factory_max_efficiency_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_labour_unions_opinion = yes
```

### Jewish-Arab Industrial Enterprises: Implementation

`ISR70_p19_ea_deepen` | x=70, y=14 | 49 days

Prerequisites: (ISR70_p19_ea).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Build a civilian industrial complex in Haifa under the independent workers' programme.

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

### Democratic Economic Planning

`ISR70_p19_eb` | x=72, y=13 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_ea.

Artwork: `gfx/interface/goals/coldwar/generic_market_socialism.png`.

Use democratic economic planning to coordinate public investment.

- 1 x 50% research bonus: Construction.
- While this party governs:
- Construction Speed: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_production_speed_buildings_factor = 0.05 tooltip = production_speed_buildings_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Democratic Economic Planning: Implementation

`ISR70_p19_eb_deepen` | x=72, y=14 | 49 days

Prerequisites: (ISR70_p19_eb).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Improve planning skills and the productivity of public enterprises.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Monthly Productivity Growth: +0.1

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_productivity_growth_modifier = 0.1 tooltip = productivity_growth_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Parliamentary Workers' Rights

`ISR70_p19_ca` | x=74, y=13 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Entrench parliamentary workers' rights and open elections.

- Stability: +3%
- Enables ordinary elections.
- While this party governs:
- Political Power Gain: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_political_power_factor = 0.05 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = neutrality elections_allowed = yes }
add_stability = 0.03
```

### Parliamentary Workers' Rights: Implementation

`ISR70_p19_ca_deepen` | x=74, y=14 | 49 days

Prerequisites: (ISR70_p19_ca).

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Enforce accountable worker representation and audit the state administration.

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

### Constitutionally Limited Councils

`ISR70_p19_cb` | x=76, y=13 | 35 days

Prerequisites: (ISR70_p19_institution).

Exclusive with: ISR70_p19_ca.

Artwork: `gfx/interface/goals/coldwar/generic_workers_democracy.png`.

Give workers' councils constitutionally limited administrative powers.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p19_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p19_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Constitutionally Limited Councils: Implementation

`ISR70_p19_cb_deepen` | x=76, y=14 | 49 days

Prerequisites: (ISR70_p19_cb).

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Negotiate a durable balance between councils and the elected legislature.

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

`ISR70_p19_finish` | x=73, y=15 | 70 days

Prerequisites: (ISR70_p19_ea_deepen OR ISR70_p19_eb_deepen) AND (ISR70_p19_ca_deepen OR ISR70_p19_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p20_institution` | x=82, y=7 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Build a national opposition with enough institutional depth to govern through its chosen constitutional route.

- Political Power: +100
- Army Experience: +15

```hoi4
add_political_power = 100
army_experience = 15
```

### Small Business in Development Towns

`ISR70_p20_ea` | x=79, y=8 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_eb.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Use development-town small businesses as a national economic base.

- Small and Medium Business Owners Opinion: +15.
- While this party governs:
- Incoming Investment Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_receiving_investment_cost_modifier = -0.1 tooltip = receiving_investment_cost_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes
```

### Small Business in Development Towns: Implementation

`ISR70_p20_ea_deepen` | x=79, y=9 | 49 days

Prerequisites: (ISR70_p20_ea).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Build a commercial office district in the Negev.

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

### A National Industrial Pact

`ISR70_p20_eb` | x=81, y=8 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_ea.

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Negotiate a national industrial pact with workers and manufacturers.

- Labor Unions Opinion: +10.
- Industrial Conglomerates Opinion: +10.
- While this party governs:
- Factory Output: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_industrial_capacity_factory = 0.05 tooltip = industrial_capacity_factory_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes
set_temp_variable = { temp_opinion = 10 }
change_industrial_conglomerates_opinion = yes
```

### A National Industrial Pact: Implementation

`ISR70_p20_eb_deepen` | x=81, y=9 | 49 days

Prerequisites: (ISR70_p20_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Deliver the pact through an industrial complex in Haifa.

- +1 Civilian Factory in Haifa.
- Treasury cost on completion: 1.5% of annual GDP.

```hoi4
205 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
ISR70_pay_0_0150 = yes
```

### Parliamentary National Populism

`ISR70_p20_ca` | x=83, y=8 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Keep national populism within a parliamentary system with ordinary elections.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Parliamentary National Populism: Implementation

`ISR70_p20_ca_deepen` | x=83, y=9 | 49 days

Prerequisites: (ISR70_p20_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Professionalize the parliamentary government and its oversight.

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

### A Presidential Popular Mandate

`ISR70_p20_cb` | x=85, y=8 | 35 days

Prerequisites: (ISR70_p20_institution).

Exclusive with: ISR70_p20_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

Seek an elected presidential mandate while preserving elections.

- Political Power: +100
- Enables ordinary elections.
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 100
```

### A Presidential Popular Mandate: Implementation

`ISR70_p20_cb_deepen` | x=85, y=9 | 49 days

Prerequisites: (ISR70_p20_cb).

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Consolidate the popular mandate and national mobilization institutions.

- Stability: +3%
- Army Experience: +20
- While this party governs:
- War Support: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p20_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p20_war_support_factor = 0.05 tooltip = war_support_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
army_experience = 20
```

### A National Majority Movement

`ISR70_p20_finish` | x=82, y=10 | 70 days

Prerequisites: (ISR70_p20_ea_deepen OR ISR70_p20_eb_deepen) AND (ISR70_p20_ca_deepen OR ISR70_p20_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/ISR_independence.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p21_institution` | x=90, y=7 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Organize a radical national alliance. Its later constitutional choice determines whether it accepts legal limits or an authoritarian order.

- Political Power: +50
- Army Experience: +30

```hoi4
army_experience = 30
add_political_power = 50
```

### An Autonomous Defense Industry

`ISR70_p21_ea` | x=87, y=8 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_eb.

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

Build an autonomous domestic defense industry to reduce external dependence.

- 1 x 50% research bonus: Infantry Weapons.
- While this party governs:
- Imperia Sanction Resistance: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_imp_sanction_resistance = 0.1 tooltip = ISR70_imp_sanction_resistance_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_infantry_weapons uses = 1 bonus = 0.5 }
```

### An Autonomous Defense Industry: Implementation

`ISR70_p21_ea_deepen` | x=87, y=9 | 49 days

Prerequisites: (ISR70_p21_ea).

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

Add a military factory in Tel Aviv under a funded domestic-arms programme.

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

### A National Mobilization Fund

`ISR70_p21_eb` | x=89, y=8 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_ea.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Create a mobilization fund for reserve training and military production.

- Army Experience: +35
- While this party governs:
- Mobilization Speed: +15%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_mobilization_speed = 0.15 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 35
```

### A National Mobilization Fund: Implementation

`ISR70_p21_eb_deepen` | x=89, y=9 | 49 days

Prerequisites: (ISR70_p21_eb).

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Expand the practical training programme and support arms-factory construction.

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

### Radical Politics within Legal Limits

`ISR70_p21_ca` | x=91, y=8 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Accept legal limits on radical political organization and retain ordinary elections.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +4%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_stability_factor = 0.04 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### Radical Politics within Legal Limits: Implementation

`ISR70_p21_ca_deepen` | x=91, y=9 | 49 days

Prerequisites: (ISR70_p21_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Give civilian institutions the authority to enforce those limits.

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

### An Authoritarian Security State

`ISR70_p21_cb` | x=93, y=8 | 35 days

Prerequisites: (ISR70_p21_institution).

Exclusive with: ISR70_p21_ca.

Artwork: `gfx/interface/goals/coldwar/generic_police_state.png`.

Establish an authoritarian security order and suspend elections. The constitutional confrontation causes an immediate stability loss.

- Stability: -3%
- Army Experience: +25
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
add_stability = -0.03
army_experience = 25
```

### An Authoritarian Security State: Implementation

`ISR70_p21_cb_deepen` | x=93, y=9 | 49 days

Prerequisites: (ISR70_p21_cb).

Artwork: `gfx/interface/goals/coldwar/generic_officer.png`.

Consolidate the security apparatus and its military organization.

- Political Power: +75
- The Military Opinion: +10.
- While this party governs:
- Division Organization: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p21_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p21_army_org_factor = 0.05 tooltip = ISR70_army_org_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_temp_variable = { temp_opinion = 10 }
change_the_military_opinion = yes
add_political_power = 75
```

### The Radical State Order

`ISR70_p21_finish` | x=90, y=10 | 70 days

Prerequisites: (ISR70_p21_ea_deepen OR ISR70_p21_eb_deepen) AND (ISR70_p21_ca_deepen OR ISR70_p21_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p22_institution` | x=82, y=12 | 35 days

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

### Centralize Defense Logistics

`ISR70_p22_ea` | x=79, y=13 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_eb.

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Centralize defense logistics to reduce the supply burden of the emergency force.

- Army Experience: +30
- While this party governs:
- Supply Consumption: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_supply_consumption_factor = -0.1 tooltip = supply_consumption_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 30
```

### Centralize Defense Logistics: Implementation

`ISR70_p22_ea_deepen` | x=79, y=14 | 49 days

Prerequisites: (ISR70_p22_ea).

Artwork: `gfx/interface/goals/coldwar/generic_artillery_factories.png`.

Create a military factory in Tel Aviv for the emergency procurement programme.

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

### Bring in Civilian Technocrats

`ISR70_p22_eb` | x=81, y=13 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_ea.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Bring civilian technocrats into the emergency government and reduce administrative waste.

- Political Power: +75
- While this party governs:
- Bureaucracy Cost: -10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_bureaucracy_cost_multiplier_modifier = -0.1 tooltip = bureaucracy_cost_multiplier_modifier_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Bring in Civilian Technocrats: Implementation

`ISR70_p22_eb_deepen` | x=81, y=14 | 49 days

Prerequisites: (ISR70_p22_eb).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Apply civilian technical standards to industrial and construction planning.

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

### A Limited Emergency with Elections

`ISR70_p22_ca` | x=83, y=13 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament.png`.

Limit the emergency and restore ordinary elections.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_stability_factor = 0.05 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### A Limited Emergency with Elections: Implementation

`ISR70_p22_ca_deepen` | x=83, y=14 | 49 days

Prerequisites: (ISR70_p22_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Audit emergency procurement and strengthen civilian confidence.

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

### Permanent Military Rule

`ISR70_p22_cb` | x=85, y=13 | 35 days

Prerequisites: (ISR70_p22_institution).

Exclusive with: ISR70_p22_ca.

Artwork: `gfx/interface/goals/coldwar/generic_officer.png`.

Make military rule permanent and suspend ordinary elections.

- The Military Opinion: +10.
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
set_temp_variable = { temp_opinion = 10 }
change_the_military_opinion = yes
```

### Permanent Military Rule: Implementation

`ISR70_p22_cb_deepen` | x=85, y=14 | 49 days

Prerequisites: (ISR70_p22_cb).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Consolidate the standing command structure and military mobilization programme.

- Army Experience: +35
- While this party governs:
- Division Organization: +5%
- Mobilization Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p22_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p22_army_org_factor = 0.05 tooltip = ISR70_army_org_factor_tt }
add_to_variable = { ISR70_p22_mobilization_speed = 0.1 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
army_experience = 35
```

### The Future of the Emergency Cabinet

`ISR70_p22_finish` | x=82, y=15 | 70 days

Prerequisites: (ISR70_p22_ea_deepen OR ISR70_p22_eb_deepen) AND (ISR70_p22_ca_deepen OR ISR70_p22_cb_deepen).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_p23_institution` | x=90, y=12 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Create a constituent assembly for the explicitly chosen crown settlement. Its powers remain subject to the later constitutional choice.

- Political Power: +100
- Stability: +2%

```hoi4
add_political_power = 100
add_stability = 0.02
```

### Endowments and Public Works

`ISR70_p23_ea` | x=87, y=13 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_eb.

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Use public endowments for local works rather than private royal industrial corporations.

- Political Power: +75
- While this party governs:
- Infrastructure Construction Speed: +15%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_production_speed_infrastructure_factor = 0.15 tooltip = ISR70_production_speed_infrastructure_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_political_power = 75
```

### Endowments and Public Works: Implementation

`ISR70_p23_ea_deepen` | x=87, y=14 | 49 days

Prerequisites: (ISR70_p23_ea).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Fund a public-works infrastructure level in the Negev.

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
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Royal Industrial Companies

`ISR70_p23_eb` | x=89, y=13 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_ea.

Artwork: `gfx/interface/goals/coldwar/generic_takeover_industries.png`.

Create professionally run royal industrial companies under the new constitutional settlement.

- 1 x 50% research bonus: Industry.
- While this party governs:
- Civilian Industry Construction Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_production_speed_industrial_complex_factor = 0.1 tooltip = production_speed_industrial_complex_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
```

### Royal Industrial Companies: Implementation

`ISR70_p23_eb_deepen` | x=89, y=14 | 49 days

Prerequisites: (ISR70_p23_eb).

Artwork: `gfx/interface/goals/coldwar/factory_complex.png`.

Build the royal industrial programme's civilian complex in Haifa.

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

### A Parliamentary Crown

`ISR70_p23_ca` | x=91, y=13 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_cb.

Artwork: `gfx/interface/goals/coldwar/generic_parliament2.png`.

Establish a parliamentary crown with ordinary elections and a responsible cabinet.

- Political Power: +75
- Enables ordinary elections.
- While this party governs:
- Stability: +5%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_stability_factor = 0.05 tooltip = stability_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = yes }
add_political_power = 75
```

### A Parliamentary Crown: Implementation

`ISR70_p23_ca_deepen` | x=91, y=14 | 49 days

Prerequisites: (ISR70_p23_ca).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Place crown expenditure and administration under parliamentary scrutiny.

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

### Personal Royal Government

`ISR70_p23_cb` | x=93, y=13 | 35 days

Prerequisites: (ISR70_p23_institution).

Exclusive with: ISR70_p23_ca.

Artwork: `gfx/interface/goals/coldwar/generic_stable_government.png`.

Establish personal royal government and suspend ordinary elections.

- Political Power: +100
- Disables ordinary elections.
- While this party governs:
- Political Power Gain: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_political_power_factor = 0.1 tooltip = political_power_factor_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
set_politics = { ruling_party = nationalist elections_allowed = no }
add_political_power = 100
```

### Personal Royal Government: Implementation

`ISR70_p23_cb_deepen` | x=93, y=14 | 49 days

Prerequisites: (ISR70_p23_cb).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Consolidate the crown's executive institutions and national-service mandate.

- Political Power: +50
- Stability: +3%
- While this party governs:
- Mobilization Speed: +10%

```hoi4
custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = ISR70_p23_programme }
custom_effect_tooltip = ISR70_programme_scope_tt
add_to_variable = { ISR70_p23_mobilization_speed = 0.1 tooltip = mobilization_speed_tt }
hidden_effect = { ISR70_refresh_programmes = yes }
add_stability = 0.03
add_political_power = 50
```

### The Crown and Israeli Statehood

`ISR70_p23_finish` | x=90, y=15 | 70 days

Prerequisites: (ISR70_p23_ea_deepen OR ISR70_p23_eb_deepen) AND (ISR70_p23_ca_deepen OR ISR70_p23_cb_deepen).

Artwork: `gfx/interface/goals/israel_palestine/menorah.dds`.

Consolidate the institutions and the economic and civic choices made in this programme.

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

`ISR70_economic_plan` | x=13, y=1 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/Economic_Protectionism.dds`.

Industry, agriculture and public infrastructure must keep pace with a growing population. A national economic programme will coordinate investment for the coming decade.

- Political Power: +50
- 2 x 50% research bonus: Industry.

```hoi4
add_political_power = 50
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 2 bonus = 0.5 }
```

### Water as a Basis for Development

`ISR70_water` | x=7, y=2 | 35 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

Improve the National Water Carrier and irrigation engineering. Agricultural research supports the next stage.

- 1 x 50% research bonus: Agriculture.
- National spirit:
- Agricultural District Construction Speed: +15%
- Unlocks decisions: Agricultural Advice in Galilee.

```hoi4
add_ideas = ISR70_water_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_agriculture uses = 1 bonus = 0.5 }

unlock_decision_tooltip = ISR70_decision_galilee_productivity
```

### Irrigation and Agronomy in the Negev

`ISR70_negev_agriculture` | x=8, y=3 | 49 days

Prerequisites: (ISR70_water).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Water and agricultural engineering can give southern communities a more secure livelihood. New irrigated districts will bring cultivation and employment to the Negev.

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

### Maintain the Water Network

`ISR70_water_maintenance` | x=5, y=3 | 35 days

Prerequisites: (ISR70_water).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Canals.tga`.

Fund pumps, workshops and repairs so farms and public utilities recover more quickly.

- Farmers Opinion: +10.
- National spirit:
- Industry Repair Speed: +15%

```hoi4
add_ideas = ISR70_water_maintenance_idea
set_temp_variable = { temp_opinion = 10 }
change_farmers_opinion = yes
```

### Haifa as an Industrial Center

`ISR70_haifa_industry` | x=13, y=2 | 49 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Expand the civilian industrial base in Haifa and give the new plant a funded capital budget.

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

### Services in Tel Aviv

`ISR70_tel_aviv_offices` | x=19, y=2 | 49 days

Prerequisites: (ISR70_economic_plan).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Add a commercial office district in Tel Aviv for services, export finance and municipal employment.

- +1 Office District in Tel Aviv.
- Small and Medium Business Owners Opinion: +10.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = offices level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Roads to the Development Towns

`ISR70_negev_roads` | x=8, y=4 | 49 days

Prerequisites: (ISR70_negev_agriculture).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Connect southern development towns with an additional infrastructure level in the Negev.

- +1 Infrastructure level in the Negev.
- 1 x 50% research bonus: Infrastructure.
- Treasury cost on completion: 0.6% of annual GDP.

```hoi4
206 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_infrastructure uses = 1 bonus = 0.5 }
```

### A Reliable Electricity Network

`ISR70_power_grid` | x=13, y=3 | 49 days

Prerequisites: (ISR70_haifa_industry).

Artwork: `gfx/interface/goals/coldwar/1st_Electric_Program.dds`.

Expand fossil electricity generation to serve the growing industrial and office sectors.

- +1 Fossil Fuel Powerplant in Tel Aviv.
- 1 x 50% research bonus: Energy Efficiency.
- Treasury cost on completion: 1.2% of annual GDP.

```hoi4
204 = {
	add_building_construction = { type = fossil_powerplant level = 1 instant_build = yes }
}
ISR70_pay_0_0120 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_energy_efficiency uses = 1 bonus = 0.5 }
```

### Diamonds, Tools and Export Orders

`ISR70_exports` | x=19, y=3 | 35 days

Prerequisites: (ISR70_tel_aviv_offices).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Support diamond cutting, precision tools and export finance. Local businesses gain confidence and offices expand faster.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Office Construction Speed: +10%
- Incoming Investment Cost: -10%
- Unlocks decisions: Send an Export Delegation.

```hoi4
add_ideas = ISR70_exports_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes

unlock_decision_tooltip = ISR70_decision_export_mission
```

### Strategic Import Substitution

`ISR70_import_substitution` | x=11, y=3 | 35 days

Prerequisites: (ISR70_haifa_industry).

Exclusive with: ISR70_export_specialization.

Artwork: `gfx/interface/goals/coldwar/Economic_Protectionism.dds`.

Foreign embargoes expose the vulnerabilities of an economy dependent on imported machinery. Domestic production must be able to sustain essential industries under pressure.

- Industrial Conglomerates Opinion: +5.
- National spirit:
- Imperia Sanction Resistance: +15%
- Factory Output: +5%

```hoi4
add_ideas = ISR70_import_substitution_idea
set_temp_variable = { temp_opinion = 5 }
change_industrial_conglomerates_opinion = yes
```

### Specialize for Export Markets

`ISR70_export_specialization` | x=15, y=3 | 35 days

Prerequisites: (ISR70_haifa_industry).

Exclusive with: ISR70_import_substitution.

Artwork: `gfx/interface/goals/coldwar/export_factories.tga`.

Specialize in higher-value exports and foreign investment. Greater world-market exposure makes external market swings more consequential.

- Small and Medium Business Owners Opinion: +10.
- National spirit:
- Return on Investment: +0.5%
- Incoming Investment Cost: -10%
- World-Market Exposure: +10%

```hoi4
add_ideas = ISR70_export_specialization_idea
set_temp_variable = { temp_opinion = 10 }
change_small_medium_business_owners_opinion = yes
```

### Diaspora Capital for Real Projects

`ISR70_diaspora_bonds` | x=19, y=4 | 35 days

Prerequisites: (ISR70_exports).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Diaspora savings can support public investment through a credible bond programme. Transparent administration and durable projects will be essential to retaining investors' confidence.

- Political Power: +75
- National spirit:
- Imperia Investment Reward: +10%

```hoi4
add_ideas = ISR70_diaspora_bonds_idea
add_political_power = 75
```

### Scrutinize Investment Contracts

`ISR70_investment_scrutiny` | x=19, y=5 | 35 days

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

### Civilian Electronics and Skilled Workers

`ISR70_civil_electronics` | x=13, y=5 | 49 days

Prerequisites: (ISR70_power_grid).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Technical workshops and civilian electronics can become a new foundation for industrial development. Skilled engineers will connect university research with practical manufacturing.

- 2 x 50% research bonus: Electronics.
- National spirit:
- Monthly Productivity Growth: +0.1

```hoi4
add_ideas = ISR70_civil_electronics_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 2 bonus = 0.5 }
```

### Technion and Applied Research

`ISR70_technion` | x=13, y=6 | 35 days

Prerequisites: (ISR70_civil_electronics).

Artwork: `gfx/interface/goals/coldwar/Universities.dds`.

Fund applied research at the Technion. Construction research and a permanent national research improvement support civilian and defense engineering.

- 2 x 50% research bonus: Construction.
- National spirit:
- Research Speed: +3%

```hoi4
add_ideas = ISR70_technion_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 2 bonus = 0.5 }
```

### Credit for Productive Small Businesses

`ISR70_sme_credit` | x=19, y=6 | 35 days

Prerequisites: (ISR70_investment_scrutiny).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Guarantee productive small-business credit and reduce the cost of incoming investment.

- Small and Medium Business Owners Opinion: +15.
- National spirit:
- Incoming Investment Cost: -10%
- Office Construction Speed: +5%
- Unlocks decisions: A Municipal Service Center.

```hoi4
add_ideas = ISR70_sme_credit_idea
set_temp_variable = { temp_opinion = 15 }
change_small_medium_business_owners_opinion = yes

unlock_decision_tooltip = ISR70_decision_office_project
```

### Further Industrial Development

`ISR70_civil_plant` | x=13, y=7 | 70 days

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

### Growth and Public Finances

`ISR70_fiscal_review` | x=19, y=7 | 35 days

Prerequisites: (ISR70_sme_credit).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Prepare a fiscal review and give the cabinet political capital for its budget choice.

- Political Power: +100
- Small and Medium Business Owners Opinion: +5.
- Unlocks decisions: Targeted Debt Repayment.

```hoi4
add_political_power = 100
set_temp_variable = { temp_opinion = 5 }
change_small_medium_business_owners_opinion = yes

unlock_decision_tooltip = ISR70_decision_debt_repayment
```

### Gradual Fiscal Consolidation

`ISR70_steady_budget` | x=18, y=8 | 35 days

Prerequisites: (ISR70_fiscal_review).

Exclusive with: ISR70_development_budget.

Artwork: `gfx/interface/goals/coldwar/generic_tackle_corruption.png`.

Improve sovereign credit through a credible consolidation programme. Interest rates fall without forcing new cuts into unrelated policies.

- Political Power: +50
- National spirit:
- Interest Rate: -0.5 percentage points
- Bureaucracy Cost: -5%

```hoi4
add_ideas = ISR70_steady_budget_idea
add_political_power = 50
```

### Development before Short-Term Consolidation

`ISR70_development_budget` | x=20, y=8 | 35 days

Prerequisites: (ISR70_fiscal_review).

Exclusive with: ISR70_steady_budget.

Artwork: `gfx/interface/goals/coldwar/construction.png`.

Commit a funded development budget to construction and industrial research.

- 1 x 50% research bonus: Construction.
- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Construction Speed: +10%

```hoi4
add_ideas = ISR70_development_budget_idea
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

## Society, Education and Integration

A shared state branch whose institutional achievements survive changes of government.

### A Social Development Compact

`ISR70_social_contract` | x=59, y=1 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/generic_union_agreement.png`.

Agree a social compact between workers, employers and municipalities.

- Political Power: +75
- Labor Unions Opinion: +5.
- Small and Medium Business Owners Opinion: +5.

```hoi4
add_political_power = 75
set_temp_variable = { temp_opinion = 5 }
change_labour_unions_opinion = yes
set_temp_variable = { temp_opinion = 5 }
change_small_medium_business_owners_opinion = yes
```

### Vocational Education for New Citizens

`ISR70_vocational` | x=54, y=2 | 35 days

Prerequisites: (ISR70_social_contract).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Expand vocational schools for new immigrants and industrial workers. Training improves productivity and industrial research.

- 1 x 50% research bonus: Industry.
- Labor Unions Opinion: +10.
- National spirit:
- Monthly Productivity Growth: +0.1
- Unlocks decisions: A Negev Vocational Training Project.

```hoi4
add_ideas = ISR70_vocational_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_industry uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_labour_unions_opinion = yes

unlock_decision_tooltip = ISR70_decision_negev_productivity
```

### Connect the Development Towns

`ISR70_development_towns` | x=54, y=3 | 35 days

Prerequisites: (ISR70_vocational).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Connect development towns to employment and public services with funded infrastructure in the Negev.

- +1 Infrastructure level in the Negev.
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Infrastructure Construction Speed: +10%

```hoi4
add_ideas = ISR70_development_towns_idea
206 = {
	add_building_construction = { type = infrastructure level = 1 instant_build = yes }
}
ISR70_pay_0_0060 = yes
```

### Integrate Immigration for the Long Term

`ISR70_absorption_reform` | x=54, y=4 | 49 days

Prerequisites: (ISR70_development_towns).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

Replace the starting immigration bottleneck with integrated housing, employment and education. Population growth remains while the starting social-cost surcharge is removed.

- Stability: +3%
- Replaces "Immigration and Development Gaps" with "Integrated Immigration"; removes its +5% social-cost surcharge while retaining population growth.

```hoi4
swap_ideas = { remove_idea = ISR70_absorption add_idea = ISR70_integrated_immigration }
add_stability = 0.03
```

### Negotiate Religion and the State

`ISR70_religion_state` | x=64, y=2 | 35 days

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

### Renew the Religious Compromise

`ISR70_religious_compromise` | x=63, y=3 | 35 days

Prerequisites: (ISR70_religion_state).

Exclusive with: ISR70_civil_marriage.

Artwork: `gfx/interface/goals/israel_palestine/Orthodox_jew.dds`.

Renew the parliamentary religious compromise. Religious institutions gain confidence and a more stable settlement supports government.

- Religious Institutions Opinion: +15.
- National spirit:
- Stability: +5%

```hoi4
add_ideas = ISR70_religious_compromise_idea
set_temp_variable = { temp_opinion = 15 }
change_the_priesthood_opinion = yes
```

### Civil Personal-Status Options

`ISR70_civil_marriage` | x=65, y=3 | 35 days

Prerequisites: (ISR70_religion_state).

Exclusive with: ISR70_religious_compromise.

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Introduce civilian personal-status options and strengthen secular civic institutions. This political reform grants a distinct gain in political capacity.

- Political Power: +100
- Stability: +3%
- National spirit:
- Political Power Gain: +5%

```hoi4
add_ideas = ISR70_civil_marriage_idea
add_political_power = 100
add_stability = 0.03
```

### The Question of Shared Service

`ISR70_national_service` | x=64, y=4 | 35 days

Prerequisites: (ISR70_religious_compromise OR ISR70_civil_marriage).

Artwork: `gfx/interface/goals/coldwar/conscription.png`.

Prepare a common public-service framework and strengthen the institutions that organize it.

- Political Power: +75
- Army Experience: +15

```hoi4
add_political_power = 75
army_experience = 15
```

### Voluntary Municipal Civilian Service

`ISR70_volunteer_service` | x=63, y=5 | 35 days

Prerequisites: (ISR70_national_service).

Exclusive with: ISR70_service_expansion.

Artwork: `gfx/interface/goals/coldwar/generic_workers_rights.png`.

Organize voluntary municipal civilian service. Social administration becomes cheaper and the civic settlement gains confidence.

- Stability: +3%
- National spirit:
- Social Spending Cost: -5%
- Bureaucracy Cost: -5%

```hoi4
add_ideas = ISR70_volunteer_service_idea
add_stability = 0.03
```

### Expand Military Training

`ISR70_service_expansion` | x=65, y=5 | 35 days

Prerequisites: (ISR70_national_service).

Exclusive with: ISR70_volunteer_service.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Expand training facilities and improve military call-up speed, with immediate army experience.

- Army Experience: +35
- National spirit:
- Mobilization Speed: +15%
- Army Training Time: -5%

```hoi4
add_ideas = ISR70_service_expansion_idea
army_experience = 35
```

### Research between Jerusalem and Haifa

`ISR70_universities` | x=52, y=3 | 49 days

Prerequisites: (ISR70_vocational).

Artwork: `gfx/interface/goals/coldwar/expand_research_funding.tga`.

Increase university capacity in Jerusalem and Haifa, financing research staff and two electronics projects.

- 2 x 50% research bonus: Electronics.
- Treasury cost on completion: 0.8% of annual GDP.
- National spirit:
- Research Speed: +3%

```hoi4
add_ideas = ISR70_universities_idea
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_electronics uses = 2 bonus = 0.5 }
```

### Healthcare beyond the Metropolises

`ISR70_public_health` | x=56, y=4 | 35 days

Prerequisites: (ISR70_development_towns).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Extend clinics and professional healthcare administration beyond the largest cities.

- Stability: +2%
- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Healthcare Cost: -10%

```hoi4
add_ideas = ISR70_public_health_idea
ISR70_pay_0_0060 = yes
add_stability = 0.02
```

## IDF, Defense Industry and Intelligence

A shared state branch whose institutional achievements survive changes of government.

### The General Staff and the Security Situation

`ISR70_staff` | x=110, y=1 | 14 days

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

### Keep the Reserve Ready

`ISR70_reserve_system` | x=101, y=2 | 35 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/coldwar/AST_upgrade_reserves.png`.

Replace the starting citizen-army spirit with an organized reserve system. Mobilization and unit cohesion improve.

- Army Experience: +25
- Removes the national spirit "Citizen Army and Reserve".
- National spirit:
- Mobilization Speed: +25%
- Division Organization: +5%
- Unlocks decisions: Conduct a Reserve Exercise, Temporary Reserve Readiness.

```hoi4
add_ideas = ISR70_reserve_system_idea
army_experience = 25
remove_ideas = ISR70_citizen_army

unlock_decision_tooltip = ISR70_decision_reserve_exercise
unlock_decision_tooltip = ISR70_decision_reserve_mobilize
```

### Defense in Depth

`ISR70_defensive_depth` | x=99, y=3 | 49 days

Prerequisites: (ISR70_reserve_system).

Exclusive with: ISR70_maneuver.

Artwork: `gfx/interface/goals/coldwar/generic_army_training.png`.

Train layered defenses and improve defensive coordination.

- Army Experience: +30
- National spirit:
- Division Defense: +8%
- Maximum Entrenchment: +2

```hoi4
add_ideas = ISR70_defensive_depth_idea
army_experience = 30
```

### Mobile Operational Reserves

`ISR70_maneuver` | x=101, y=3 | 49 days

Prerequisites: (ISR70_reserve_system).

Exclusive with: ISR70_defensive_depth.

Artwork: `gfx/interface/goals/coldwar/doctrine_tank_warfare.png`.

Build mobile operational reserves around staff exercises and rapid planning.

- Army Experience: +40
- National spirit:
- Planning Speed: +15%
- Division Organization: +5%

```hoi4
add_ideas = ISR70_maneuver_idea
army_experience = 40
```

### Tal and the Domestic Tank Programme

`ISR70_armour_programme` | x=107, y=2 | 49 days

Prerequisites: (ISR70_staff).

Artwork: `gfx/interface/goals/coldwar/generic_army_tanks3.png`.

Israel Tal advocates a tank designed around the needs of Israeli crews and the lessons of recent wars. Domestic engineering and sustained trials will be necessary to carry that ambition forward.

- Army Experience: +25
- 2 x 50% research bonus: Armor.
- Unlocks decisions: Domestic Equipment Trials.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 2 bonus = 0.5 }
army_experience = 25

unlock_decision_tooltip = ISR70_decision_equipment_trials
```

### Crew Protection and Maintenance

`ISR70_survivability` | x=106, y=3 | 35 days

Prerequisites: (ISR70_armour_programme).

Exclusive with: ISR70_armour_mobility.

Artwork: `gfx/interface/goals/coldwar/generic_tank_destroyer.png`.

Prioritize crew protection, repairability and standardized maintenance in the armored force.

- 1 x 50% research bonus: Armor.
- National spirit:
- Armor Division Defense: +10%

```hoi4
add_ideas = ISR70_survivability_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_armor uses = 1 bonus = 0.5 }
```

### Mobility and Tactical Employment

`ISR70_armour_mobility` | x=108, y=3 | 35 days

Prerequisites: (ISR70_armour_programme).

Exclusive with: ISR70_survivability.

Artwork: `gfx/interface/goals/coldwar/generic_army_tanks2.png`.

Prioritize tactical mobility and armored coordination rather than the alternative protection package.

- Army Experience: +35
- National spirit:
- Division Organization: +5%
- Planning Speed: +10%

```hoi4
add_ideas = ISR70_armour_mobility_idea
army_experience = 35
```

### IMI and Domestic Manufacturing

`ISR70_imi` | x=107, y=4 | 70 days

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

`ISR70_artillery` | x=103, y=3 | 35 days

Prerequisites: (ISR70_reserve_system).

Artwork: `gfx/interface/goals/coldwar/artillery.png`.

Recent fighting has demonstrated the importance of responsive fire support and counter-battery work. The artillery arm needs better training and a coherent development programme.

- Army Experience: +20
- 2 x 50% research bonus: Towed Artillery.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_towed_artillery uses = 2 bonus = 0.5 }
army_experience = 20
```

### Engineers and Combat Supply

`ISR70_engineers` | x=103, y=4 | 35 days

Prerequisites: (ISR70_artillery).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Improve field engineering, reconnaissance and combat supply rather than simply expanding the force.

- Army Experience: +25
- National spirit:
- Reconnaissance: +10%
- Supply Consumption: -8%

```hoi4
add_ideas = ISR70_engineers_idea
army_experience = 25
```

### Special Forces with Clear Missions

`ISR70_special_forces` | x=103, y=5 | 35 days

Prerequisites: (ISR70_engineers).

Artwork: `gfx/interface/goals/coldwar/ISR_israel_defense_forces.dds`.

Fund specialist training and contemporary special-forces equipment research.

- Army Experience: +30
- 2 x 50% research bonus: Special Forces Equipment.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_special_forces_equipment uses = 2 bonus = 0.5 }
army_experience = 30
```

### The Air Force after the Embargo

`ISR70_air_staff` | x=115, y=2 | 14 days

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

### Delivery Contracts over Domestic Development

`ISR70_foreign_aircraft` | x=114, y=3 | 49 days

Prerequisites: (ISR70_air_staff).

Exclusive with: ISR70_local_aircraft.

Artwork: `gfx/interface/goals/coldwar/generic_air_fighter_new.png`.

A reliable American supply channel allows the air force to plan its next generation of aircraft. Conversion training and maintenance arrangements must accompany procurement.

- Air Experience: +25
- 2 x 50% research bonus: Medium Aircraft.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_medium_aircraft uses = 2 bonus = 0.5 }
air_experience = 25
```

### IAI and a Domestic Aircraft Industry

`ISR70_local_aircraft` | x=116, y=3 | 49 days

Prerequisites: (ISR70_air_staff).

Exclusive with: ISR70_foreign_aircraft.

Artwork: `gfx/interface/goals/coldwar/Generic_Airline_Industry.tga`.

Israel Aircraft Industries can reduce dependence on foreign suppliers. Domestic design teams, workshops and flight trials will require sustained government backing.

- Air Experience: +20
- 2 x 50% research bonus: Aircraft.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_aircraft uses = 2 bonus = 0.5 }
air_experience = 20
set_country_flag = ISR70_local_aircraft_programme
```

### Training, Maintenance and Spare Parts

`ISR70_air_maintenance` | x=115, y=4 | 35 days

Prerequisites: (ISR70_foreign_aircraft OR ISR70_local_aircraft).

Artwork: `gfx/interface/goals/coldwar/generic_support_equipment.png`.

Improve training, spare parts and maintenance. A completed domestic aircraft programme removes the starting embargo penalty.

- Treasury cost on completion: 0.6% of annual GDP.
- National spirit:
- Air Mission Efficiency: +8%

```hoi4
add_ideas = ISR70_air_maintenance_idea
ISR70_pay_0_0060 = yes
if = { limit = { has_country_flag = ISR70_local_aircraft_programme } remove_ideas = ISR70_embargo }
```

### A Resilient Airfield Network

`ISR70_airfield` | x=115, y=5 | 35 days

Prerequisites: (ISR70_air_maintenance).

Artwork: `gfx/interface/goals/coldwar/generic_air_command.png`.

Expand the southern airfield network by two levels and improve its engineering.

- +2 Air Base levels in the Negev.
- 1 x 50% research bonus: Construction.
- Treasury cost on completion: 0.8% of annual GDP.

```hoi4
206 = {
	add_building_construction = { type = air_base level = 2 instant_build = yes }
}
ISR70_pay_0_0080 = yes
add_tech_bonus = { name = ISR70_research_programme category = CAT_construction uses = 1 bonus = 0.5 }
```

### Radar and Contemporary Air Defense

`ISR70_air_defense` | x=118, y=3 | 35 days

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

`ISR70_naval_staff` | x=122, y=2 | 14 days

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

### Missile Boats and Coastal Operations

`ISR70_missile_boats` | x=121, y=3 | 49 days

Prerequisites: (ISR70_naval_staff).

Exclusive with: ISR70_submarines.

Artwork: `gfx/interface/goals/israel_palestine/isr_navy.dds`.

Develop missile-boat tactics and contemporary corvette research.

- Navy Experience: +30
- 2 x 50% research bonus: Corvettes.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_corvettes uses = 2 bonus = 0.5 }
navy_experience = 30
```

### Submarines and Covert Reconnaissance

`ISR70_submarines` | x=123, y=3 | 49 days

Prerequisites: (ISR70_naval_staff).

Exclusive with: ISR70_missile_boats.

Artwork: `gfx/interface/goals/coldwar/generic_submarine_base.png`.

Train covert naval reconnaissance and support submarine development.

- Navy Experience: +30
- 2 x 50% research bonus: Submarines.

```hoi4
add_tech_bonus = { name = ISR70_research_programme category = CAT_submarines uses = 2 bonus = 0.5 }
navy_experience = 30
```

### Shipbuilding Capacity in Haifa

`ISR70_shipyards` | x=122, y=4 | 70 days

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

`ISR70_intelligence` | x=110, y=6 | 35 days

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

### Analysis before Easy Certainties

`ISR70_intelligence_analysis` | x=108, y=7 | 35 days

Prerequisites: (ISR70_intelligence).

Exclusive with: ISR70_intelligence_operations.

Artwork: `gfx/interface/goals/israel_palestine/the_research_department.dds`.

Prioritize assessment, language training and independent analysis over operational expansion.

- 1 x 50% research bonus: Decryption.
- National spirit:
- Reconnaissance: +10%
- Planning Speed: +10%

```hoi4
add_ideas = ISR70_intelligence_analysis_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_decryption uses = 1 bonus = 0.5 }
```

### Operational Intelligence Networks

`ISR70_intelligence_operations` | x=112, y=7 | 35 days

Prerequisites: (ISR70_intelligence).

Exclusive with: ISR70_intelligence_analysis.

Artwork: `gfx/interface/goals/coldwar/generic_secret_documents.png`.

Build operational networks and secure communications. Foreign influence becomes harder to exert.

- 1 x 50% research bonus: Encryption.
- Intelligence Community Opinion: +10.
- National spirit:
- Foreign Influence Defense: +15%

```hoi4
add_ideas = ISR70_intelligence_operations_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_encryption uses = 1 bonus = 0.5 }
set_temp_variable = { temp_opinion = 10 }
change_intelligence_community_opinion = yes
```

### Civil Defense for Border Communities

`ISR70_civil_defense` | x=95, y=3 | 35 days

Prerequisites: (ISR70_reserve_system).

Artwork: `gfx/interface/goals/coldwar/generic_construct_public_housing.png`.

Build two civilian shelter levels for northern border communities.

- Stability: +2%
- +2 Civilian Shelter levels in Haifa.
- Treasury cost on completion: 0.6% of annual GDP.
- Unlocks decisions: An Additional Civilian Shelter.

```hoi4
205 = {
	add_building_construction = { type = civilian_shelter level = 2 instant_build = yes }
}
ISR70_pay_0_0060 = yes
add_stability = 0.02

unlock_decision_tooltip = ISR70_decision_shelters
```

### A Coordinated Readiness Plan

`ISR70_preparedness` | x=100, y=6 | 35 days

Prerequisites: (ISR70_defensive_depth OR ISR70_maneuver) AND (ISR70_air_defense).

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Integrate the reserve, maintenance and civil-defense programmes into one readiness plan.

- Army Experience: +30
- Air Experience: +20
- Navy Experience: +15
- National spirit:
- Division Organization: +3%
- Supply Consumption: -5%

```hoi4
add_ideas = ISR70_preparedness_idea
army_experience = 30
air_experience = 20
navy_experience = 15
```

## The Cold War and Foreign Policy

A shared state branch whose institutional achievements survive changes of government.

### The Foreign-Policy Situation of 1970

`ISR70_foreign_policy` | x=83, y=1 | 35 days

Prerequisites: (ISR70_january_1970).

Artwork: `gfx/interface/goals/coldwar/foreign_diplomacy.png`.

Give the foreign ministry a cabinet mandate and open the national diplomatic programme.

- Political Power: +100

```hoi4
add_political_power = 100
```

### Strengthen the Washington Channel

`ISR70_us_channel` | x=74, y=2 | 35 days

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

`ISR70_us_security` | x=73, y=3 | 35 days

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

`ISR70_us_civil` | x=75, y=3 | 35 days

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

`ISR70_france_channel` | x=79, y=2 | 35 days

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

`ISR70_european_trade` | x=79, y=3 | 35 days

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

`ISR70_soviet_channel` | x=83, y=2 | 35 days

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

`ISR70_soviet_dialogue` | x=83, y=3 | 35 days

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

`ISR70_independent_diplomacy` | x=88, y=2 | 35 days

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

`ISR70_africa_contacts` | x=87, y=3 | 35 days

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

`ISR70_jordan_backchannel` | x=93, y=2 | 35 days

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

`ISR70_iran_contacts` | x=97, y=2 | 35 days

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

### Contractual Oil-Supply Security

`ISR70_oil_security` | x=97, y=3 | 35 days

Prerequisites: (ISR70_iran_contacts).

Artwork: `gfx/interface/goals/coldwar/Oil_Pipelines.tga`.

Implement the accepted Iranian supply agreement, improving resilience against sanctions and fuel vulnerability.

- 1 x 50% research bonus: Fuel Refining.
- National spirit:
- Imperia Sanction Resistance: +10%

```hoi4
add_ideas = ISR70_oil_security_idea
add_tech_bonus = { name = ISR70_research_programme category = CAT_fuel_refining uses = 1 bonus = 0.5 }
```

### Ambiguity or International Transparency

`ISR70_nuclear_policy` | x=90, y=3 | 35 days

Prerequisites: (ISR70_independent_diplomacy).

Artwork: `gfx/interface/goals/coldwar/generic_secret_documents.png`.

Review the diplomatic implications of ambiguity and international transparency before choosing a policy.

- Political Power: +75

```hoi4
add_political_power = 75
```

### Preserve Nuclear Ambiguity

`ISR70_keep_ambiguity` | x=89, y=4 | 35 days

Prerequisites: (ISR70_nuclear_policy).

Exclusive with: ISR70_nuclear_transparency.

Artwork: `gfx/interface/goals/coldwar/Nuclear_Research_Lab.png`.

Discretion preserves freedom of action in a hostile region. The cabinet will reaffirm a policy of strategic ambiguity and tightly controlled diplomatic communication.

- Political Power: +50
- Removes the national spirit "Nuclear Ambiguity".
- National spirit:
- Foreign Influence Defense: +15%

```hoi4
add_ideas = ISR70_keep_ambiguity_idea
remove_ideas = ISR70_ambiguity
add_political_power = 50
```

### Offer International Transparency

`ISR70_nuclear_transparency` | x=91, y=4 | 35 days

Prerequisites: (ISR70_nuclear_policy).

Exclusive with: ISR70_keep_ambiguity.

Artwork: `gfx/interface/goals/coldwar/Nuclear_Research_Lab.png`.

Civilian nuclear cooperation offers a different diplomatic course. Greater openness would place international research and peaceful technical exchanges at the center of policy.

- 2 x 50% research bonus: Nuclear Reactors.
- Removes the national spirit "Nuclear Ambiguity".
- National spirit:
- Research Speed: +2%

```hoi4
add_ideas = ISR70_nuclear_transparency_idea
remove_ideas = ISR70_ambiguity
add_tech_bonus = { name = ISR70_research_programme category = CAT_nuclear_reactors uses = 2 bonus = 0.5 }
```

## Suez, Borders and Peace

A shared state branch whose institutional achievements survive changes of government.

### Assess the Suez Front

`ISR70_suez` | x=110, y=9 | 35 days

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

`ISR70_limited_attrition` | x=108, y=10 | 35 days

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

`ISR70_deep_raids` | x=112, y=10 | 35 days

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

### Respond to the Rogers Initiative

`ISR70_rogers` | x=110, y=11 | 35 days

Prerequisites: (ISR70_limited_attrition OR ISR70_deep_raids).

Artwork: `gfx/interface/goals/coldwar/BeginNegotiations.dds`.

Choose a response to the Rogers Initiative. An Egyptian reply determines whether a ceasefire can be implemented.

- Political Power: +50
- Opens the Rogers Initiative event. An Egyptian acceptance unlocks the ceasefire route; a proposal alone does not end the War of Attrition.

```hoi4
add_political_power = 50
set_country_flag = ISR70_rogers_offer
country_event = { id = ISR70.10 days = 1 }
custom_effect_tooltip = ISR70_rogers_outcome_tt
```

### A Controlled Ceasefire

`ISR70_ceasefire` | x=108, y=12 | 35 days

Prerequisites: (ISR70_rogers).

Exclusive with: ISR70_armed_stalemate.

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

### Maintain the Armed Stalemate

`ISR70_armed_stalemate` | x=112, y=12 | 35 days

Prerequisites: (ISR70_rogers).

Exclusive with: ISR70_ceasefire.

Artwork: `gfx/interface/goals/coldwar/ISR_Focus_Israeli_Army.dds`.

Maintain a fortified military posture instead of the negotiated ceasefire route. The War of Attrition burden remains.

- Army Experience: +30
- National spirit:
- Division Defense: +8%

```hoi4
add_ideas = ISR70_armed_stalemate_idea
army_experience = 30
```

### The Question of the Controlled Territories

`ISR70_territorial_policy` | x=110, y=13 | 35 days

Prerequisites: (ISR70_ceasefire OR ISR70_armed_stalemate).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Prepare the cabinet's territorial policy. The next choice determines which negotiated or administrative route can proceed.

- Political Power: +100

```hoi4
add_political_power = 100
```

### Defensible Borders: An Allon-Oriented Plan

`ISR70_all_on` | x=105, y=14 | 35 days

Prerequisites: (ISR70_territorial_policy).

Exclusive with: ISR70_territorial_maximalism, ISR70_regional_compromise.

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

Adopt an Allon-oriented security plan. Defensive planning improves while negotiations remain possible.

- Army Experience: +20
- National spirit:
- Division Defense: +5%

```hoi4
add_ideas = ISR70_all_on_idea
army_experience = 20
set_country_flag = ISR70_allon_policy
```

### Permanent Territorial Control

`ISR70_territorial_maximalism` | x=108, y=14 | 35 days

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

`ISR70_regional_compromise` | x=115, y=14 | 35 days

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

`ISR70_sinai_negotiation` | x=104, y=15 | 35 days

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

`ISR70_westbank_autonomy` | x=107, y=15 | 35 days

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

`ISR70_golan_review` | x=113, y=16 | 35 days

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

`ISR70_gaza_services` | x=116, y=16 | 35 days

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

`ISR70_egypt_peace` | x=104, y=16 | 70 days

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

`ISR70_regional_normalization` | x=105, y=17 | 70 days

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

`ISR70_territory_administration` | x=110, y=15 | 35 days

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

`ISR70_annexation_review` | x=110, y=16 | 35 days

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

`ISR70_arab_citizens` | x=4, y=26 | 21 days

Prerequisites: (ISR70_social_contract).

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Set the cabinet programme for Arab citizens of Israel. Equal access and preferential discrimination are exclusive; municipal self-government remains a separate, compatible choice.

- Opens the two exclusive access routes and optional municipal autonomy.

```hoi4
ISR70_policy_complete_citizen_review = yes
```

### Equal Municipal Services

`ISR70_equal_local_services` | x=-4, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Exclusive with: ISR70_preferential_allocations.

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Fund municipal services and transport links in state 205. The stability and continuing service costs begin when the project is completed.

- Fund municipal services and transport links in state 205. The stability and continuing service costs begin when the project is completed.
- Reserve 0.6% of annual GDP at selection. Delivery after 180 days: +1 infrastructure levels in Haifa. Continuing effects: Stability: +2%; Social Spending Cost: +3%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_equal_services = yes
```

### Open Public Employment

`ISR70_equal_employment` | x=-4, y=29 | 35 days

Prerequisites: (ISR70_equal_local_services).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Spend 0.3% of GDP once on training and hiring procedures. Office worker requirement falls by 2%.

- Spend 0.3% of GDP once on training and hiring procedures. Office worker requirement falls by 2%.

```hoi4
ISR70_policy_complete_equal_employment = yes
```

### Equal Access to Land and Credit

`ISR70_equal_access` | x=-4, y=30 | 49 days

Prerequisites: (ISR70_equal_employment).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Spend 50 political power and reserve 1.2% of GDP for a one-factory credit and enterprise programme in Haifa (state 205). Reform effects begin after delivery.

- Spend 50 political power and reserve 1.2% of GDP for a one-factory credit and enterprise programme in Haifa (state 205). Reform effects begin after delivery.
- Reserve 1.2% of annual GDP at selection. Delivery after 270 days: +1 civilian factories in Haifa. Continuing effects: Factory Output: +3%; Incoming Investment Cost: -5%; Bureaucracy Cost: +2%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_equal_access = yes
```

### Municipal Self-Government

`ISR70_local_autonomy` | x=4, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Spend 50 political power to devolve municipal responsibilities. Bureaucracy costs fall 10%; corruption costs rise 3%.

- Spend 50 political power to devolve municipal responsibilities. Bureaucracy costs fall 10%; corruption costs rise 3%.

```hoi4
ISR70_policy_complete_municipal_self = yes
```

### Municipal Infrastructure Grants

`ISR70_municipal_pacts` | x=4, y=29 | 35 days

Prerequisites: (ISR70_local_autonomy).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Opens one joint 1.0% GDP grant programme for states 205 and 206. Both projects must remain deliverable; the shared social cost applies after completion.

- Opens one joint 1.0% GDP grant programme for states 205 and 206. Both projects must remain deliverable; the shared social cost applies after completion.
- Reserve 1% of annual GDP at selection. Delivery after 180 days: +1 infrastructure levels in Haifa; +1 infrastructure levels in the Negev. Continuing effects: Social Spending Cost: +2%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_municipal_pacts = yes
```

### Municipal Development Funds

`ISR70_municipal_representation` | x=4, y=30 | 49 days

Prerequisites: (ISR70_municipal_pacts).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Spend 0.2% of GDP to establish the funds. Infrastructure construction is 15% faster in states 205 and 206 while Israel owns and controls them; internal investment costs fall 10%.

- Spend 0.2% of GDP to establish the funds. Infrastructure construction is 15% faster in states 205 and 206 while Israel owns and controls them; internal investment costs fall 10%.

```hoi4
ISR70_policy_complete_municipal_representation = yes
```

### Preferential Land and Budget Allocation

`ISR70_preferential_allocations` | x=12, y=28 | 35 days

Prerequisites: (ISR70_arab_citizens).

Exclusive with: ISR70_equal_local_services.

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Reserve 0.5% of GDP to open two building slots and deliver one infrastructure level in state 206. Stability falls by 2 percentage points on completion.

- Reserve 0.5% of GDP to open two building slots and deliver one infrastructure level in state 206. Stability falls by 2 percentage points on completion.
- Reserve 0.5% of annual GDP at selection. Delivery after 180 days: +2 building slots in the Negev; +1 infrastructure levels in the Negev. Continuing effects: Stability: -2%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_preferential_allocations = yes
```

### Preferential Development Contracts

`ISR70_restricted_employment` | x=12, y=29 | 35 days

Prerequisites: (ISR70_preferential_allocations).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Reserve 1.2% of GDP for a factory in state 206. Preferential procurement raises corruption costs by 3%; industrial conglomerates gain 10 opinion if active after delivery.

- Reserve 1.2% of GDP for a factory in state 206. Preferential procurement raises corruption costs by 3%; industrial conglomerates gain 10 opinion if active after delivery.
- Reserve 1.2% of annual GDP at selection. Delivery after 270 days: +1 civilian factories in the Negev. Continuing effects: Corruption Cost: +3%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_restricted_employment = yes
```

### Separate Municipal Funding Rules

`ISR70_separate_development` | x=12, y=30 | 49 days

Prerequisites: (ISR70_restricted_employment).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Choose discriminatory funding rules: social costs fall 5%, stability falls 2 percentage points, and corruption costs rise 2%.

- Choose discriminatory funding rules: social costs fall 5%, stability falls 2 percentage points, and corruption costs rise 2%.

```hoi4
ISR70_policy_complete_separate_development = yes
```

## Settlement Projects and Palestinian Relations

Settlement Projects and Palestinian Relations. Each policy retains its own conditions and consequences.

### Survey Land and Existing Communities

`ISR70_land_survey` | x=44, y=26 | 35 days

Prerequisites: (ISR70_territory_administration).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Survey one controlled Palestinian-owned project area. The survey costs 0.1% of GDP; it neither changes ownership nor predetermines Palestinian consent.

- Survey one controlled Palestinian-owned project area. The survey costs 0.1% of GDP; it neither changes ownership nor predetermines Palestinian consent.

```hoi4
ISR70_policy_complete_land_survey = yes
```

### A Budget for Territorial Policy

`ISR70_settlement_budget` | x=44, y=27 | 21 days

Prerequisites: (ISR70_land_survey).

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Choose the settlement project budget for the already selected area. Freeze, limited development and expansion are mutually exclusive; each has its own actual funding and Palestinian consequences.

- Choose the settlement project budget for the already selected area. Freeze, limited development and expansion are mutually exclusive; each has its own actual funding and Palestinian consequences.

```hoi4
ISR70_policy_complete_settlement_budget = yes
```

### Suspend New Settlements

`ISR70_freeze_new` | x=36, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_designated_sites, ISR70_authorize_expansion.

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Pay 75 political power and offer a settlement freeze. Only an accepted offer reduces the local resistance target by 5 points. Rejection changes neither control nor rights.

- Pay 75 political power and offer a settlement freeze. Only an accepted offer reduces the local resistance target by 5 points. Rejection changes neither control nor rights.

```hoi4
ISR70_policy_complete_freeze_new = yes
```

### Joint Municipal Works

`ISR70_municipal_works` | x=36, y=30 | 49 days

Prerequisites: (ISR70_freeze_new).

Artwork: `gfx/interface/goals/israel_palestine/gaza_civic_organizations.dds`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 1.5% of GDP for the chosen project; delivery takes 270 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 1.5% of GDP for the chosen project; delivery takes 270 days. It is not a grant of ownership or a core.
- Reserve 1.5% of annual GDP at selection. Delivery after 270 days: +1 civilian factories in the West Bank; +1 infrastructure levels in the West Bank. Continuing effects: Social Spending Cost: +2%. Local policy effects: Local Supplies for Controller: +10%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 1.5% of annual GDP at selection. Delivery after 270 days: +1 civilian factories in Gaza; +1 infrastructure levels in Gaza. Continuing effects: Social Spending Cost: +2%. Local policy effects: Local Supplies for Controller: +10%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_municipal_works = yes
```

### A Local Administration Compact

`ISR70_land_compact` | x=36, y=31 | 70 days

Prerequisites: (ISR70_municipal_works).

Artwork: `gfx/interface/goals/israel_palestine/olive_branch.dds`.

Open a separate administrative agreement. The transfer and reductions in garrison and administrative costs require actual Palestinian acceptance and implementation.

- Open a separate administrative agreement. The transfer and reductions in garrison and administrative costs require actual Palestinian acceptance and implementation.

```hoi4
ISR70_policy_complete_land_compact = yes
```

### Designate Agricultural-Security Sites

`ISR70_designated_sites` | x=44, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_freeze_new, ISR70_authorize_expansion.

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.8% of GDP for the chosen project; delivery takes 240 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.8% of GDP for the chosen project; delivery takes 240 days. It is not a grant of ownership or a core.
- Reserve 0.8% of annual GDP at selection. Delivery after 240 days: +1 building slots in the West Bank; +1 agricultural districts in the West Bank. Continuing effects: Bureaucracy Cost: +2%. Local policy effects: Relations toward Israel: -10 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 0.8% of annual GDP at selection. Delivery after 240 days: +1 building slots in Gaza; +1 agricultural districts in Gaza. Continuing effects: Bureaucracy Cost: +2%. Local policy effects: Relations toward Israel: -10 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_designated_sites = yes
```

### Roads, Water and Supply Links

`ISR70_settlement_services` | x=44, y=30 | 49 days

Prerequisites: (ISR70_designated_sites).

Artwork: `gfx/interface/goals/coldwar/generic_road_construction.png`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.6% of GDP for the chosen project; delivery takes 180 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.6% of GDP for the chosen project; delivery takes 180 days. It is not a grant of ownership or a core.
- Reserve 0.6% of annual GDP at selection. Delivery after 180 days: +1 infrastructure levels in the West Bank. Local policy effects: Local Supplies for Controller: +15%; Local resistance target: +5 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 0.6% of annual GDP at selection. Delivery after 180 days: +1 infrastructure levels in Gaza. Local policy effects: Local Supplies for Controller: +15%; Local resistance target: +5 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_settlement_services = yes
```

### Fortified Sites and a Binding Ceiling

`ISR70_settlement_ceiling` | x=44, y=31 | 49 days

Prerequisites: (ISR70_settlement_services).

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.4% of GDP for the chosen project; delivery takes 180 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.4% of GDP for the chosen project; delivery takes 180 days. It is not a grant of ownership or a core.
- Reserve 0.4% of annual GDP at selection. Delivery after 180 days: +1 land fort levels in the West Bank. Local policy effects: Local Garrison Requirement: +5%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 0.4% of annual GDP at selection. Delivery after 180 days: +1 land fort levels in Gaza. Local policy effects: Local Garrison Requirement: +5%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_settlement_ceiling = yes
```

### Authorize Civilian Settlement Expansion

`ISR70_authorize_expansion` | x=52, y=29 | 35 days

Prerequisites: (ISR70_settlement_budget).

Exclusive with: ISR70_freeze_new, ISR70_designated_sites.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.3% of GDP for the chosen project; delivery takes 90 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.3% of GDP for the chosen project; delivery takes 90 days. It is not a grant of ownership or a core.
- Reserve 0.3% of annual GDP at selection. Delivery after 90 days: +3 building slots in the West Bank. Continuing effects: Bureaucracy Cost: +2%. Local policy effects: Local Infrastructure Construction Speed: +15%; Relations toward Israel: -25 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 0.3% of annual GDP at selection. Delivery after 90 days: +3 building slots in Gaza. Continuing effects: Bureaucracy Cost: +2%. Local policy effects: Local Infrastructure Construction Speed: +15%; Relations toward Israel: -25 points. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_authorize_expansion = yes
```

### Agricultural and Industrial Settlement Sites

`ISR70_settlement_package` | x=52, y=30 | 70 days

Prerequisites: (ISR70_authorize_expansion).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 2.3% of GDP for the chosen project; delivery takes 300 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 2.3% of GDP for the chosen project; delivery takes 300 days. It is not a grant of ownership or a core.
- Reserve 2.3% of annual GDP at selection. Delivery after 300 days: +1 agricultural districts in the West Bank; +1 civilian factories in the West Bank. Continuing effects: Social Spending Cost: +3%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 2.3% of annual GDP at selection. Delivery after 300 days: +1 agricultural districts in Gaza; +1 civilian factories in Gaza. Continuing effects: Social Spending Cost: +3%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_settlement_package = yes
```

### Roads, Supply Depots and Fortified Positions

`ISR70_entrench_network` | x=52, y=31 | 70 days

Prerequisites: (ISR70_settlement_package).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.9% of GDP for the chosen project; delivery takes 240 days. It is not a grant of ownership or a core.

- One selected Palestinian-owned target: the West Bank or Gaza. Reserve 0.9% of GDP for the chosen project; delivery takes 240 days. It is not a grant of ownership or a core.
- Reserve 0.9% of annual GDP at selection. Delivery after 240 days: +2 infrastructure levels in the West Bank; +2 land fort levels in the West Bank. Continuing effects: Bureaucracy Cost: +3%. Local policy effects: Local Supplies for Controller: +25%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.
- Reserve 0.9% of annual GDP at selection. Delivery after 240 days: +2 infrastructure levels in Gaza; +2 land fort levels in Gaza. Continuing effects: Bureaucracy Cost: +3%. Local policy effects: Local Supplies for Controller: +25%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_entrench_network = yes
```

### Negotiate Limits and Compensation

`ISR70_settlement_compensation` | x=50, y=32 | 49 days

Prerequisites: (ISR70_entrench_network).

Exclusive with: ISR70_settlement_unilateral.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Pay 75 political power to negotiate a binding expansion ceiling. PAL can reject. An accepted arrangement requires a separate 0.6% GDP transfer; then resistance target rises 3 points and garrison need rises 5%, rather than the unilateral penalties.

- Pay 75 political power to negotiate a binding expansion ceiling. PAL can reject. An accepted arrangement requires a separate 0.6% GDP transfer; then resistance target rises 3 points and garrison need rises 5%, rather than the unilateral penalties.

```hoi4
ISR70_policy_complete_settlement_compensation = yes
```

### Impose the Settlement Network Unilaterally

`ISR70_settlement_unilateral` | x=54, y=32 | 35 days

Prerequisites: (ISR70_entrench_network).

Exclusive with: ISR70_settlement_compensation.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Impose the network unilaterally. Pay 50 political power; local resistance target rises 10 points, garrison need 15% and garrison damage 10%. PAL receives an actual response event; war is not declared automatically.

- Impose the network unilaterally. Pay 50 political power; local resistance target rises 10 points, garrison need 15% and garrison damage 10%. PAL receives an actual response event; war is not declared automatically.

```hoi4
ISR70_policy_complete_settlement_unilateral = yes
```

## Development Finance and Office Networks

Development Finance and Office Networks. Each policy retains its own conditions and consequences.

### Finance for National Development

`ISR70_finance_links` | x=84, y=26 | 21 days

Prerequisites: (ISR70_diaspora_bonds).

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Open the domestic, bank-led and international development-finance programmes.

- Open the domestic, bank-led and international development-finance programmes.

```hoi4
ISR70_policy_complete_finance_links = yes
```

### Train Accountants and Office Staff

`ISR70_clerical_training` | x=84, y=27 | 35 days

Prerequisites: (ISR70_finance_links).

Artwork: `gfx/interface/goals/coldwar/BEL_prioritizetechnicaleducation.dds`.

Spend 0.4% of GDP on accounting and office training. Office worker requirement falls 3%.

- Spend 0.4% of GDP on accounting and office training. Office worker requirement falls 3%.

```hoi4
ISR70_policy_complete_clerical_training = yes
```

### Mechanized Clearing and Bookkeeping

`ISR70_clearing_network` | x=84, y=28 | 49 days

Prerequisites: (ISR70_clerical_training).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Spend 0.6% of GDP on mechanized clearing and bookkeeping. Office worker requirement falls a further 3% (6% across this finance route).

- Spend 0.6% of GDP on mechanized clearing and bookkeeping. Office worker requirement falls a further 3% (6% across this finance route).

```hoi4
ISR70_policy_complete_clearing_network = yes
```

### Long-Term Development Bonds

`ISR70_development_bonds` | x=76, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_bank_consortium, ISR70_export_credit.

Artwork: `gfx/interface/goals/coldwar/agricultural_banks.dds`.

Unlock a one-time decision to borrow 1% of GDP. The amount borrowed is added equally to treasury liquidity and public debt; bankruptcy blocks the draw.

- Unlock a one-time decision to borrow 1% of GDP. The amount borrowed is added equally to treasury liquidity and public debt; bankruptcy blocks the draw.

```hoi4
ISR70_policy_complete_development_bonds = yes
```

### Audit the Development Funds

`ISR70_audited_funds` | x=76, y=31 | 35 days

Prerequisites: (ISR70_development_bonds).

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Spend 50 political power on project oversight. Corruption costs fall 3%.

- Spend 50 political power on project oversight. Corruption costs fall 3%.

```hoi4
ISR70_policy_complete_audited_funds = yes
```

### Service Centers for New Towns

`ISR70_development_offices` | x=76, y=32 | 70 days

Prerequisites: (ISR70_audited_funds).

Artwork: `gfx/interface/goals/coldwar/generic_financial_markets.png`.

Reserve 1.2% of GDP for an office level in state 206. On delivery, office worker requirement falls a further 2%, making the route total 8%.

- Reserve 1.2% of GDP for an office level in state 206. On delivery, office worker requirement falls a further 2%, making the route total 8%.
- Reserve 1.2% of annual GDP at selection. Delivery after 240 days: +1 office levels in the Negev. Continuing effects: Office Worker Requirement: -2%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_development_offices = yes
```

### A Domestic Banking Consortium

`ISR70_bank_consortium` | x=84, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_development_bonds, ISR70_export_credit.

Artwork: `gfx/interface/goals/coldwar/generic_banking_legislation.png`.

Office productivity rises 3%; concentration and privileged access raise corruption costs 3%.

- Office productivity rises 3%; concentration and privileged access raise corruption costs 3%.

```hoi4
ISR70_policy_complete_bank_consortium = yes
```

### Shared Back Offices

`ISR70_shared_services` | x=84, y=31 | 49 days

Prerequisites: (ISR70_bank_consortium).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Spend 0.5% of GDP to standardize shared accounting and administration. Office worker requirement falls a further 4%, for 10% across this route.

- Spend 0.5% of GDP to standardize shared accounting and administration. Office worker requirement falls a further 4%, for 10% across this route.

```hoi4
ISR70_policy_complete_shared_services = yes
```

### Bank-Industry Investment Partnerships

`ISR70_industrial_credit` | x=84, y=32 | 70 days

Prerequisites: (ISR70_shared_services).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Reserve 1.2% of GDP for an office level in Tel Aviv (204). Office construction speed rises 5%; corruption costs rise a further 2% on delivery.

- Reserve 1.2% of GDP for an office level in Tel Aviv (204). Office construction speed rises 5%; corruption costs rise a further 2% on delivery.
- Reserve 1.2% of annual GDP at selection. Delivery after 240 days: +1 office levels in Tel Aviv. Continuing effects: Office Construction Speed: +5%; Corruption Cost: +2%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_industrial_credit = yes
```

### Negotiate Export Credit Lines

`ISR70_export_credit` | x=92, y=30 | 35 days

Prerequisites: (ISR70_clearing_network).

Exclusive with: ISR70_development_bonds, ISR70_bank_consortium.

Artwork: `gfx/interface/goals/coldwar/generic_positive_trade_relations_gold.png`.

Unlock a repeatable request costing 50 political power. The United States may accept or decline; a declined request can be renewed after 360 days. An existing military agreement does not block civilian credit.

- Unlock a repeatable request costing 50 political power. The United States may accept or decline; a declined request can be renewed after 360 days. An existing military agreement does not block civilian credit.

```hoi4
ISR70_policy_complete_export_credit = yes
```

### Finance Imported Office Equipment

`ISR70_equipment_finance` | x=92, y=31 | 49 days

Prerequisites: (ISR70_export_credit).

Artwork: `gfx/interface/goals/israel_palestine/isr_computer.dds`.

Spend 0.6% of GDP on imported office equipment. Office productivity rises 5%; Cold War market exposure rises 5%.

- Spend 0.6% of GDP on imported office equipment. Office productivity rises 5%; Cold War market exposure rises 5%.

```hoi4
ISR70_policy_complete_equipment_finance = yes
```

### Build an Export Services Sector

`ISR70_export_services` | x=92, y=32 | 70 days

Prerequisites: (ISR70_equipment_finance).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Requires an accepted export-credit line. Reserve 1.2% of GDP for an office level in Haifa (205); office construction speed rises 10% and market exposure rises a further 5% on delivery.

- Requires an accepted export-credit line. Reserve 1.2% of GDP for an office level in Haifa (205); office construction speed rises 10% and market exposure rises a further 5% on delivery.
- Reserve 1.2% of annual GDP at selection. Delivery after 240 days: +1 office levels in Haifa. Continuing effects: Office Construction Speed: +10%; World-Market Exposure: +5%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_export_services = yes
```

## Greater Israel: Sinai Development and Integration

Greater Israel: Sinai Development and Integration. Each policy retains its own conditions and consequences.

### A Greater Israel Mandate

`ISR70_gi_mandate` | x=4, y=42 | 35 days

Prerequisites: (ISR70_territorial_maximalism).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Pay the shared 100-political-power territorial mandate once. A mandate already paid through Herut covers this focus; it grants neither ownership nor a declaration of war.

- Pay the shared 100-political-power territorial mandate once. A mandate already paid through Herut covers this focus; it grants neither ownership nor a declaration of war.

```hoi4
ISR70_policy_complete_gi_mandate = yes
```

### Borders and Budgets for Sinai

`ISR70_gi_frontier_review` | x=4, y=43 | 35 days

Prerequisites: (ISR70_gi_mandate).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Budget 0.2% of GDP to separate Sinai civilian development, coastal projects, and the later choice of legal status.

- Budget 0.2% of GDP to separate Sinai civilian development, coastal projects, and the later choice of legal status.

```hoi4
ISR70_policy_complete_gi_frontier_review = yes
```

### A Permanent Sinai Administration

`ISR70_gi_sinai_admin` | x=0, y=45 | 35 days

Prerequisites: (ISR70_gi_frontier_review).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Establish permanent Sinai administration at a cost of 0.3% of GDP. Local infrastructure builds 15% faster; bureaucracy costs rise 3%. Egyptian ownership remains until an actual territorial settlement.

- Establish permanent Sinai administration at a cost of 0.3% of GDP. Local infrastructure builds 15% faster; bureaucracy costs rise 3%. Egyptian ownership remains until an actual territorial settlement.

```hoi4
ISR70_policy_complete_gi_sinai_admin = yes
```

### Serviced Settlement Sites in Northern Sinai

`ISR70_gi_sinai_housing` | x=0, y=46 | 49 days

Prerequisites: (ISR70_gi_sinai_admin).

Artwork: `gfx/interface/goals/coldwar/Irrigation_Pipes.dds`.

Fund the specified project through decisions. Reserve 1% of GDP; delivery takes 240 days. Lost requirements refund the original reserved budget.

- Fund the specified project through decisions. Reserve 1% of GDP; delivery takes 240 days. Lost requirements refund the original reserved budget.
- Reserve 1% of annual GDP at selection. Delivery after 240 days: +2 building slots in Sinai; +1 infrastructure levels in Sinai. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_gi_sinai_housing = yes
```

### Voluntary Settlement in the Sinai Towns

`ISR70_gi_sinai_families` | x=0, y=47 | 70 days

Prerequisites: (ISR70_gi_sinai_housing).

Artwork: `gfx/interface/goals/coldwar/Fund_social_integration_Programs.tga`.

Fund a voluntary internal movement of at most 20,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 20,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_gi_sinai_families = yes
```

### Family Services on the Frontier

`ISR70_gi_frontier_families` | x=0, y=48 | 49 days

Prerequisites: (ISR70_gi_sinai_families).

Artwork: `gfx/interface/goals/coldwar/Generic_Healthcare.tga`.

Fund 0.4% of GDP for a single five-year family-service idea: population-growth modifier +5%, healthcare costs +2%. It does not add 5% of the population each month and cannot stack with itself.

- Fund 0.4% of GDP for a single five-year family-service idea: population-growth modifier +5%, healthcare costs +2%. It does not add 5% of the population each month and cannot stack with itself.

```hoi4
ISR70_policy_complete_gi_frontier_families = yes
```

### Agriculture and Industry for the Sinai Towns

`ISR70_gi_sinai_economy` | x=0, y=49 | 70 days

Prerequisites: (ISR70_gi_frontier_families).

Artwork: `gfx/interface/goals/coldwar/Agricultural_Mechanization.dds`.

Fund the specified project through decisions. Reserve 1.8% of GDP; delivery takes 300 days. Lost requirements refund the original reserved budget.

- Fund the specified project through decisions. Reserve 1.8% of GDP; delivery takes 300 days. Lost requirements refund the original reserved budget.
- Reserve 1.8% of annual GDP at selection. Delivery after 300 days: +1 agricultural districts in Sinai; +1 civilian factories in Sinai. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_gi_sinai_economy = yes
```

### Settle Sovereignty over the Sinai

`ISR70_gi_sinai_status` | x=0, y=50 | 70 days

Prerequisites: (ISR70_gi_sinai_economy).

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

After an actual peace settlement has transferred Sinai, pay 150 political power for its sovereignty administration. This focus does not transfer the state or remove the Egyptian core.

- After an actual peace settlement has transferred Sinai, pay 150 political power for its sovereignty administration. This focus does not transfer the state or remove the Egyptian core.

```hoi4
ISR70_policy_complete_gi_sinai_status = yes
```

### Assert the Sinai Territorial Claim

`ISR70_gi_canal_claim` | x=8, y=45 | 70 days

Prerequisites: (ISR70_gi_frontier_review).

Artwork: `gfx/interface/goals/coldwar/generic_air_fighter_new.png`.

Pay 150 political power for a Sinai territorial claim. Relations with Egypt fall 40 and with PAL/Jordan 15. This neither changes ownership nor declares war.

- Pay 150 political power for a Sinai territorial claim. Relations with Egypt fall 40 and with PAL/Jordan 15. This neither changes ownership nor declares war.

```hoi4
ISR70_policy_complete_gi_canal_claim = yes
```

### Develop Sinai Ports and Coastal Roads

`ISR70_gi_canal_repair` | x=8, y=46 | 70 days

Prerequisites: (ISR70_gi_canal_claim).

Artwork: `gfx/interface/goals/coldwar/Drydock_Construction.tga`.

Fund the specified project through decisions. Reserve 1.2% of GDP; delivery takes 240 days. Lost requirements refund the original reserved budget.

- Fund the specified project through decisions. Reserve 1.2% of GDP; delivery takes 240 days. Lost requirements refund the original reserved budget.
- Reserve 1.2% of annual GDP at selection. Delivery after 240 days: +1 infrastructure levels in Sinai; +1 naval base levels in Sinai. Local policy effects: Local Garrison Requirement: +10%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_gi_canal_repair = yes
```

### A Sinai Coastal Settlement Programme

`ISR70_gi_canal_settlers` | x=8, y=47 | 70 days

Prerequisites: (ISR70_gi_canal_repair).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund a voluntary internal movement of at most 15,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 15,000 people over 5 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_gi_canal_settlers = yes
```

### Coastal Industry for Sinai

`ISR70_gi_canal_industry` | x=8, y=48 | 70 days

Prerequisites: (ISR70_gi_canal_settlers).

Artwork: `gfx/interface/goals/coldwar/generic_improve_industry.png`.

Fund the specified project through decisions. Reserve 2% of GDP; delivery takes 360 days. Lost requirements refund the original reserved budget.

- Fund the specified project through decisions. Reserve 2% of GDP; delivery takes 360 days. Lost requirements refund the original reserved budget.
- Reserve 2% of annual GDP at selection. Delivery after 360 days: +2 building slots in Sinai; +1 civilian factories in Sinai; +1 naval dockyards in Sinai. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_gi_canal_industry = yes
```

### Organize Sinai Coastal Logistics

`ISR70_gi_canal_navigation` | x=8, y=49 | 70 days

Prerequisites: (ISR70_gi_canal_industry).

Artwork: `gfx/interface/goals/coldwar/DiamondsAre4ever.dds`.

Fund the specified project through decisions. Reserve 0.8% of GDP; delivery takes 180 days. Lost requirements refund the original reserved budget.

- Fund the specified project through decisions. Reserve 0.8% of GDP; delivery takes 180 days. Lost requirements refund the original reserved budget.
- Reserve 0.8% of annual GDP at selection. Delivery after 180 days: the specified clearance and operating works. Continuing effects: Bureaucracy Cost: +1%. Local policy effects: Local Supplies for Controller: +10%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_gi_canal_navigation = yes
```

### Unify Sinai District Administration

`ISR70_gi_canal_province` | x=8, y=50 | 70 days

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

`ISR70_gi_resident_status` | x=44, y=42 | 35 days

Prerequisites: (ISR70_gi_frontier_review).

Artwork: `gfx/interface/goals/israel_palestine/one_state_isr_pal.dds`.

Pay 50 political power to open the actual choice of equal civil status or an unequal occupation statute. Settlement projects and party affiliation do not select the legal status automatically.

- Pay 50 political power to open the actual choice of equal civil status or an unequal occupation statute. Settlement projects and party affiliation do not select the legal status automatically.

```hoi4
ISR70_policy_complete_gi_resident_status = yes
```

### Equal Civil Status in Sinai

`ISR70_gi_equal_status` | x=40, y=44 | 49 days

Prerequisites: (ISR70_gi_resident_status).

Artwork: `gfx/interface/goals/coldwar/generic_female_rights.png`.

Equal legal rights and service entitlements cost 100 political power and +3% social spending. There is no immediate resistance, compliance, loyalty or sovereignty-consent bonus. A previously chosen unequal regime must first be repealed through the explicit reform decision.

- Equal legal rights and service entitlements cost 100 political power and +3% social spending. There is no immediate resistance, compliance, loyalty or sovereignty-consent bonus. A previously chosen unequal regime must first be repealed through the explicit reform decision.

```hoi4
ISR70_policy_complete_gi_equal_status = yes
```

### Local Councils and Common Services

`ISR70_gi_canal_councils` | x=40, y=45 | 70 days

Prerequisites: (ISR70_gi_equal_status).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Fund civilian services at 0.8% of GDP and +2% bureaucracy costs. A separately accepted and implemented local contract reduces garrison needs only 5%. Rejection grants no bonus and does not repeal equal rights.

- Fund civilian services at 0.8% of GDP and +2% bureaucracy costs. A separately accepted and implemented local contract reduces garrison needs only 5%. Rejection grants no bonus and does not repeal equal rights.

```hoi4
ISR70_policy_complete_gi_canal_councils = yes
```

### Resolve Property Claims and Displacement

`ISR70_gi_property_settlement` | x=40, y=46 | 70 days

Prerequisites: (ISR70_gi_canal_councils).

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Reserve at least 0.7% of GDP for restitution. Only fulfilled, agreed claims can lower resistance target by 2 points. Prior expulsion creates additional obligations; there is no automatic loyalty or compliance reward.

- Reserve at least 0.7% of GDP for restitution. Only fulfilled, agreed claims can lower resistance target by 2 points. Prior expulsion creates additional obligations; there is no automatic loyalty or compliance reward.

```hoi4
ISR70_policy_complete_gi_property_settlement = yes
```

### Negotiate the Sinai Status

`ISR70_gi_core_review` | x=40, y=47 | 70 days

Prerequisites: (ISR70_gi_property_settlement).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

After ten years of real ownership and control and five years of equal rights, pay 100 political power to open a separate local status process. An affirmative result is not guaranteed; rejection leaves civil rights intact and grants no core.

- After ten years of real ownership and control and five years of equal rights, pay 100 political power to open a separate local status process. An affirmative result is not guaranteed; rejection leaves civil rights intact and grants no core.

```hoi4
ISR70_policy_complete_gi_core_review = yes
```

### Integrate the Sinai

`ISR70_gi_canal_core` | x=40, y=48 | 70 days

Prerequisites: (ISR70_gi_core_review).

Artwork: `gfx/interface/goals/coldwar/Adopt_New_Constitiution.tga`.

Pay 150 political power and 0.5% of GDP only after real local and Egyptian status agreements. The core applies solely to Sinai; ordinary core effects replace native occupation mechanics. Egyptian cores and historic claims remain.

- Pay 150 political power and 0.5% of GDP only after real local and Egyptian status agreements. The core applies solely to Sinai; ordinary core effects replace native occupation mechanics. Egyptian cores and historic claims remain.

```hoi4
ISR70_policy_complete_gi_canal_core = yes
```

### Separate Legal Status for Occupied Residents

`ISR70_occ_special_status` | x=48, y=44 | 35 days

Prerequisites: (ISR70_gi_resident_status).

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Choose unequal occupation law. Existing local factory access rises 10 points, garrison needs rise 15%, police costs 3%, and resistance target 8 points; social spending falls 2%. The general and Kach statutes replace each other.

- Choose unequal occupation law. Existing local factory access rises 10 points, garrison needs rise 15%, police costs 3%, and resistance target 8 points; social spending falls 2%. The general and Kach statutes replace each other.

```hoi4
ISR70_policy_complete_occ_special_status = yes
```

### Security Roads and Controlled Access

`ISR70_occ_security_roads` | x=48, y=45 | 49 days

Prerequisites: (ISR70_occ_special_status).

Artwork: `gfx/interface/goals/coldwar/ISR_Israel.dds`.

Fund 0.8% of GDP for one infrastructure level after 180 days. Secured roads add 15% local supplies but also 5% garrison need under the unequal statute.

- Fund 0.8% of GDP for one infrastructure level after 180 days. Secured roads add 15% local supplies but also 5% garrison need under the unequal statute.
- Reserve 0.8% of annual GDP at selection. Delivery after 180 days: +1 infrastructure levels in Sinai. Local policy effects: Local Supplies for Controller: +15%; Local Garrison Requirement: +5%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_occ_security_roads = yes
```

### Delegated Local Administration

`ISR70_occ_delegated_administration` | x=48, y=46 | 49 days

Prerequisites: (ISR70_occ_security_roads).

Artwork: `gfx/interface/goals/coldwar/generic_public_transport.png`.

Request a limited local administrative contract. Only acceptance followed by funding grants the 3% bureaucracy saving and 3% corruption surcharge; refusal is possible.

- Request a limited local administrative contract. Only acceptance followed by funding grants the 3% bureaucracy saving and 3% corruption surcharge; refusal is possible.

```hoi4
ISR70_policy_complete_occ_delegated_administration = yes
```

### Industrial Enclaves under Separate Law

`ISR70_occ_occupation_industry` | x=48, y=47 | 70 days

Prerequisites: (ISR70_occ_delegated_administration).

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Reserve 1.0% of GDP for one building slot and one factory on contractually acquired land. Delivery takes 270 days and adds 5% local garrison need. A local administrative refusal does not block this distinct project.

- Reserve 1.0% of GDP for one building slot and one factory on contractually acquired land. Delivery takes 270 days and adds 5% local garrison need. A local administrative refusal does not block this distinct project.
- Reserve 1% of annual GDP at selection. Delivery after 270 days: +1 building slots in Sinai; +1 civilian factories in Sinai. Local policy effects: Local Garrison Requirement: +5%. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_occ_occupation_industry = yes
```

### A Permanent Occupation Statute

`ISR70_occ_permanent_statute` | x=48, y=48 | 70 days

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

`ISR70_rad_government` | x=84, y=42 | 35 days

Prerequisites: Entry focus.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Pay 75 political power for a radical territorial programme only while its actual party governs. This neither wins an election nor enacts any of the later choices automatically.

- Pay 75 political power for a radical territorial programme only while its actual party governs. This neither wins an election nor enacts any of the later choices automatically.

```hoi4
ISR70_policy_complete_rad_government = yes
```

### An Indivisible Territorial Programme

`ISR70_rad_herut_mandate` | x=76, y=44 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/FocusElectHerut.dds`.

Herut/Gahal adopts the shared territorial mandate after choosing Indivisible Security Interests. Pay its 100-political-power cost once, credited against the Greater Israel entry.

- Herut/Gahal adopts the shared territorial mandate after choosing Indivisible Security Interests. Pay its 100-political-power cost once, credited against the Greater Israel entry.

```hoi4
ISR70_policy_complete_rad_herut_mandate = yes
```

### A National Territorial Development Authority

`ISR70_rad_herut_authority` | x=76, y=45 | 49 days

Prerequisites: (ISR70_rad_herut_mandate).

Artwork: `gfx/interface/goals/coldwar/construction_engineering.png`.

Budget 0.4% of GDP for a territorial authority: local infrastructure construction +10%, bureaucracy costs +2%, only under the programme government.

- Budget 0.4% of GDP for a territorial authority: local infrastructure construction +10%, bureaucracy costs +2%, only under the programme government.

```hoi4
ISR70_policy_complete_rad_herut_authority = yes
```

### Prepare to Hold the New Frontier

`ISR70_rad_herut_preparation` | x=76, y=46 | 49 days

Prerequisites: (ISR70_rad_herut_authority).

Artwork: `gfx/interface/goals/coldwar/Improve_supply_distribution_methods.tga`.

Budget 0.5% of GDP and +3% personnel costs for 30 army experience and 10% local supply support in the controlled Sinai. It is preparation, not a declaration of war.

- Budget 0.5% of GDP and +3% personnel costs for 30 army experience and 10% local supply support in the controlled Sinai. It is preparation, not a declaration of war.

```hoi4
ISR70_policy_complete_rad_herut_preparation = yes
```

### Reject Territorial Withdrawal

`ISR70_rad_herut_retention` | x=76, y=47 | 70 days

Prerequisites: (ISR70_rad_herut_preparation).

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Reject territorial withdrawal as an explicit Herut policy. Egyptian relations fall 20, American relations 15. A later peace requires repeal; the focus does not annex a state.

- Reject territorial withdrawal as an explicit Herut policy. Egyptian relations fall 20, American relations 15. A later peace requires repeal; the focus does not annex a state.

```hoi4
ISR70_policy_complete_rad_herut_retention = yes
```

### Religious Settlement Associations

`ISR70_rad_mafdal_council` | x=84, y=44 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/FocusElectHapoelHaMizrachi.dds`.

After choosing Religious Settlement Policy, pay 50 political power for the religious settlement programme. The later land and legal-binding choices remain separate decisions.

- After choosing Religious Settlement Policy, pay 50 political power for the religious settlement programme. The later land and legal-binding choices remain separate decisions.

```hoi4
ISR70_policy_complete_rad_mafdal_council = yes
```

### State Support for Settlement Communities

`ISR70_rad_mafdal_settlers` | x=84, y=45 | 70 days

Prerequisites: (ISR70_rad_mafdal_council).

Artwork: `gfx/interface/goals/coldwar/focus_public_housing.dds`.

Fund a voluntary internal movement of at most 10,000 people over 3 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

- Fund a voluntary internal movement of at most 10,000 people over 3 years. Every target-state addition is matched by the same subtraction from Tel Aviv; it creates no national population or recruit pool.

```hoi4
ISR70_policy_complete_rad_mafdal_settlers = yes
```

### Compulsory Expropriation of Land

`ISR70_rad_mafdal_land` | x=82, y=46 | 49 days

Prerequisites: (ISR70_rad_mafdal_settlers).

Exclusive with: ISR70_rad_mafdal_purchase.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Choose compulsory land expropriation instead of negotiated purchase: spend 0.4% of GDP for one building slot; local resistance target rises 8 points and property claims remain.

- Choose compulsory land expropriation instead of negotiated purchase: spend 0.4% of GDP for one building slot; local resistance target rises 8 points and property claims remain.

```hoi4
ISR70_policy_complete_rad_mafdal_land = yes
```

### Negotiated Land Purchases

`ISR70_rad_mafdal_purchase` | x=86, y=46 | 70 days

Prerequisites: (ISR70_rad_mafdal_settlers).

Exclusive with: ISR70_rad_mafdal_land.

Artwork: `gfx/interface/goals/coldwar/generic_civilian_oversight.png`.

Seek a voluntary land purchase. Only accepted terms unlock the 1.0%-GDP, 270-day project for the same building slot. No expropriation or automatic resistance rise follows refusal.

- Seek a voluntary land purchase. Only accepted terms unlock the 1.0%-GDP, 270-day project for the same building slot. No expropriation or automatic resistance rise follows refusal.
- Reserve 1% of annual GDP at selection. Delivery after 270 days: +1 building slots in Sinai. Loss of required control or project conditions refunds the exact reserved sum. The project can be completed only once.

```hoi4
ISR70_policy_complete_rad_mafdal_purchase = yes
```

### Declare the Settlement Land Inalienable

`ISR70_rad_mafdal_lock` | x=82, y=47 | 70 days

Prerequisites: (ISR70_rad_mafdal_land OR ISR70_rad_mafdal_purchase).

Exclusive with: ISR70_rad_mafdal_review.

Artwork: `gfx/interface/goals/israel_palestine/Jewish_sites_isr.dds`.

Make settlement land politically inalienable. Gain 50 political power once; stability falls 3 points, and later withdrawal requires a separate repeal. The alternative is a reviewable lease system.

- Make settlement land politically inalienable. Gain 50 political power once; stability falls 3 points, and later withdrawal requires a separate repeal. The alternative is a reviewable lease system.

```hoi4
ISR70_policy_complete_rad_mafdal_lock = yes
```

### Reviewable Leases and Land Registry

`ISR70_rad_mafdal_review` | x=86, y=47 | 49 days

Prerequisites: (ISR70_rad_mafdal_land OR ISR70_rad_mafdal_purchase).

Exclusive with: ISR70_rad_mafdal_lock.

Artwork: `gfx/interface/goals/coldwar/generic_investigate_corruption.png`.

Choose reviewable land leases and a registry instead of inalienability. Pay 50 political power and 0.3% of GDP; internal investment costs fall 5%, and territorial negotiations remain available.

- Choose reviewable land leases and a registry instead of inalienability. Pay 50 political power and 0.3% of GDP; internal investment costs fall 5%, and territorial negotiations remain available.

```hoi4
ISR70_policy_complete_rad_mafdal_review = yes
```

### National Front: Radical Government Programme

`ISR70_rad_kach_government` | x=92, y=44 | 35 days

Prerequisites: (ISR70_rad_government).

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Pay 100 political power for the governing National Front/Kach programme. Before 1971 it uses the existing National Front presentation. Relations with Egypt, PAL and Jordan fall 25; taking office does not automatically expel residents.

- Pay 100 political power for the governing National Front/Kach programme. Before 1971 it uses the existing National Front presentation. Relations with Egypt, PAL and Jordan fall 25; taking office does not automatically expel residents.

```hoi4
ISR70_policy_complete_rad_kach_government = yes
```

### Deny Equal Civil Status

`ISR70_rad_denial` | x=92, y=45 | 49 days

Prerequisites: (ISR70_rad_kach_government).

Artwork: `gfx/interface/goals/coldwar/generic_police_state.png`.

Explicitly deny equal civil status in controlled, non-core Sinai: +10 points of occupied factory access, +10% garrison need and +5% police costs. This replaces the general unequal statute and blocks the civic core route while active.

- Explicitly deny equal civil status in controlled, non-core Sinai: +10 points of occupied factory access, +10% garrison need and +5% police costs. This replaces the general unequal statute and blocks the civic core route while active.

```hoi4
ISR70_policy_complete_rad_denial = yes
```

### Retain Residents under Separate Administration

`ISR70_rad_no_expulsion` | x=90, y=46 | 49 days

Prerequisites: (ISR70_rad_denial).

Exclusive with: ISR70_rad_expulsion.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

Keep residents and their economic activity under unequal administration, with 0.5% of GDP for basic services. No seized-property slots or additional expulsion penalties are awarded; the underlying unequal legal regime remains.

- Keep residents and their economic activity under unequal administration, with 0.5% of GDP for basic services. No seized-property slots or additional expulsion penalties are awarded; the underlying unequal legal regime remains.

```hoi4
ISR70_policy_complete_rad_no_expulsion = yes
```

### Forced Expulsion of Arab Residents

`ISR70_rad_expulsion` | x=94, y=46 | 70 days

Prerequisites: (ISR70_rad_denial).

Exclusive with: ISR70_rad_no_expulsion.

Artwork: `gfx/interface/goals/coldwar/civil_service.png`.

An explicitly chosen, abstract forced-displacement policy. Pay 200 political power; at most two seized-property slots, stability -8 points, local resistance target +25 points and garrison need +20%. Refugees and property claims persist; other states receive actual embargo choices. No expulsion quota, population deletion, or core reward.

- An explicitly chosen, abstract forced-displacement policy. Pay 200 political power; at most two seized-property slots, stability -8 points, local resistance target +25 points and garrison need +20%. Refugees and property claims persist; other states receive actual embargo choices. No expulsion quota, population deletion, or core reward.

```hoi4
ISR70_policy_complete_rad_expulsion = yes
```

### Security Powers with an Electoral Sunset

`ISR70_rad_limited_emergency` | x=90, y=47 | 49 days

Prerequisites: (ISR70_rad_no_expulsion OR ISR70_rad_expulsion).

Exclusive with: ISR70_rad_permanent_emergency.

Artwork: `gfx/interface/goals/israel_palestine/knesset_speech.dds`.

Pay 50 political power for 365 days of +2 occupied factory-access points and +3% police costs. Elections are preserved. Renewal requires another paid government decision; the alternative is permanent emergency.

- Pay 50 political power for 365 days of +2 occupied factory-access points and +3% police costs. Elections are preserved. Renewal requires another paid government decision; the alternative is permanent emergency.

```hoi4
ISR70_policy_complete_rad_limited_emergency = yes
```

### Expansion under Permanent Emergency

`ISR70_rad_permanent_emergency` | x=94, y=47 | 70 days

Prerequisites: (ISR70_rad_no_expulsion OR ISR70_rad_expulsion).

Exclusive with: ISR70_rad_limited_emergency.

Artwork: `gfx/interface/goals/coldwar/generic_paramilitary.png`.

Choose a permanent emergency explicitly. Suspend elections, gain 5 further points of occupied factory access, and pay +10% police and +10% personnel costs. Neither party membership nor the population-policy choice enacts this automatically.

- Choose a permanent emergency explicitly. Suspend elections, gain 5 further points of occupied factory access, and pay +10% police and +10% personnel costs. Neither party membership nor the population-policy choice enacts this automatically.

```hoi4
ISR70_policy_complete_rad_permanent_emergency = yes
```

## Validation

Run `python tools/israel_1970/build_content.py` followed by `python tools/israel_1970/validate_content.py`. Static validation covers references, syntax, assets, party restrictions, programme routes, treasury reservations, negotiations and scenario integration. It does not replace an HOI4 engine test.
