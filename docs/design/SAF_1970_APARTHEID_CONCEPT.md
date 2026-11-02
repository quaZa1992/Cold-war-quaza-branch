# IMPERIA COLD WAR South Africa 1970 apartheid implementation

This record implements the user's revised base of 27 October 2026. Every numerical contribution below is a requested game-balance value, not a measured historical percentage. The earlier three-spirit tax-income proposal is superseded by one dynamic spirit with five independently adjustable policy domains.

## Starting countries and identity

The independent starting hosts are South Africa (`SAF`) and Rhodesia (`ZIM`). Namibia's two starting states are owned and controlled by South Africa, so the South African spirit already covers their administration. A NAM country actually released under an unreformed South African administration can initialize the system. Independent Namibia does not receive apartheid automatically. Portuguese colonies receive no apartheid spirit merely because they are colonies.

The title is `Apartheid` in South Africa and `Racial Minority Rule` in Rhodesia, reflecting different legal systems. After the political domain reaches zero, remaining institutional and demographic contributions appear as `Legacy of Racial Segregation`. The dynamic spirit disappears when every domain reaches zero. Restoration remains possible through the retained national policy decisions.

## Exact requested base

| Domain | Contribution at full intensity | Native implementation |
| --- | --- | --- |
| Political controls | Stability -30 percentage points | `stability_factor = -0.30` |
| Public services | Welfare cost -50% | `social_cost_multiplier_modifier = -0.50` |
| Public services | Healthcare cost -75% | `health_cost_multiplier_modifier = -0.75` |
| Public services | Education cost -75% | `education_cost_multiplier_modifier = -0.75` |
| Political controls | Administration cost +25% | `bureaucracy_cost_multiplier_modifier = 0.25` |
| Political controls | Police cost +100% | `police_cost_multiplier_modifier = 1` |
| Political controls | Police spending expectations +3 | `expected_police_modifier = 3` |
| Public services | Welfare spending expectations +3 | `expected_welfare_modifier = 3` |
| Military privileges | Defence spending expectations +3 | `expected_mil_modifier = 3` |
| Public services | Education spending expectations +3 | `expected_education_modifier = 3` |
| Public services | Healthcare spending expectations +3 | `expected_healthcare_modifier = 3` |
| Labour and land | Incoming investment cost -20% | `receiving_investment_cost_modifier = -0.20` |
| Labour and land | Construction speed +10% | `production_speed_buildings_factor = 0.10` |
| Population policy | Migration rate +25% | `migration_rate_value_factor = 0.25` |
| Population policy | Monthly population growth modifier +50% | `monthly_population = 0.50` |
| Military privileges | Military personnel costs +50% | `personnel_cost_multiplier_modifier = 0.50` |
| Labour and land | Office workers required +10% | `offices_worker_requirement_modifier = 0.10` |
| Political controls | Worldwide incoming trade opinion -20 points | Fixed native trade-opinion modifiers |
| Political controls | Regional trade opinion -50 points in both directions | Separate fixed native trade-opinion modifiers |
| Political controls | Regional diplomatic opinion -50 points in both directions | Separate fixed native diplomatic-opinion modifiers |
| Labour and land | Commercial agriculture productivity +25% | Dedicated commercial-only country modifier and two native consumers |

Welfare and social spending are one native budget category, so the expectation contribution is applied once. Native expected-spending calculations retain their existing rounding and caps. The requested +3 contribution is preserved even where a national expectation reaches its cap. Monthly population growth is a modifier to natural growth, not an increase of 50% in total population each month. Native migration handling increases positive migration and moderates a negative migration baseline.

The commercial agriculture modifier enters only `agriculture_district_tax` and `gdp_from_agriculture_district` in the money system, alongside its existing agriculture-productivity term. Subsistence agriculture is unchanged. Native GDP coefficients still determine how a productivity contribution translates into GDP. The modifier does not grant land, buildings, resources or additional workers.

## Historical rationale and limits of the abstraction

Racial classification, restrictions on residence and political exclusion sustained minority control and generated resistance. Separate institutions and extensive enforcement explain the administration, police and stability burdens. Public services were severely unequal: lower expenditure on the excluded majority coexisted with highly resourced white institutions. This supports the combination of budget discounts and high spending demands from the privileged electorate. The exact discounts and expectation levels remain balance choices. [Truth and Reconciliation Commission health-sector hearing](https://omalley.nelsonmandela.org/index.php/site/q/03lv02167/04lv02264/05lv02335/06lv02357/07lv02387/08lv02392.htm)

Restrictions on bargaining, movement and employment weakened workers' bargaining position. Employers did not benefit uniformly: controls could also obstruct recruitment and industrial expansion. Cheaper investment and construction are game abstractions of lower labour costs. The extra office staffing requirement represents the inefficiencies of exclusion from skilled occupations, not a reduction in the national workforce. [Deborah Posel, 1984](https://wiredspace.wits.ac.za/bitstreams/c72725b4-8d8f-4257-af5b-c03ff37100c5/download), [Corker and Bayoumi, 1991](https://www.imf.org/en/publications/wp/issues/2016/12/30/apartheid-growth-and-income-distribution-in-south-africa-past-history-and-future-prospects-992)

Commercial farming received protected land access, credit, infrastructure, subsidies and services while African producers faced severe restrictions. The agricultural advantage represents that institutional support together with access to low-paid labour. It does not claim that racial exclusion intrinsically increased technical efficiency. The military premium and defence expectation represent the requested balance premise of privileged service arrangements and a narrow skilled recruitment pool; +50% is not a measured historical wage differential. [South African Department of Agriculture, 1998](https://www.nda.gov.za/phocadownloadpap/Policy_Documents/Agricultural%20policy%20in%20South%20Africa%201998.pdf)

Selective white immigration and contract labour recruitment coexisted with high natural growth in a youthful population. Fertility reflected age structure, poverty, education and access to services. It was not an inherent racial characteristic or a direct benefit created by apartheid. The demographic contributions are therefore adjusted through their own settlement and voluntary family-planning programme, rather than disappearing with a constitutional reform. The government's later policy review records the selective immigration programme and the family-planning programme established in 1974. Earlier implementation in a 1970 campaign is an alternate policy choice. [Population Policy White Paper draft, 1997](https://www.gov.za/documents/white-papers/population-policy-white-paper-draft-20-aug-1997)

Rhodesia is included as a racial minority regime, rather than treated as having identical South African legislation. Contemporary diplomatic reporting documents the racially restricted franchise and the constitutional attempt to prevent majority rule. Using the same numerical base for both hosts follows the user's requested common base. [US Department of State, 18 February 1969](https://history.state.gov/historicaldocuments/frus1969-76v28/d3)

## Reforms and reversals

Each policy domain has five intensities: 100%, 75%, 50%, 25% and 0%. One reform removes one quarter of that domain's base contribution, including its advantages. One restoration reinstates one quarter. No earlier tax-income bonus, research penalty or productivity-growth penalty from the superseded concept is added on top.

Five 35-day focuses perform the first reform in their domain and unlock further decisions:

1. `Revise the Racial Settlement` changes political controls and opens normalisation proposals.
2. `Broaden Access to Public Services` changes service costs and their spending expectations.
3. `Negotiate Labour and Land Reform` changes investment costs, construction, office staffing and commercial agriculture.
4. `Revise Military Service and Pay` changes personnel costs and defence expectations.
5. `Reconsider Settlement and Family Policy` changes migration and natural-growth contributions.

Further decisions cost 75 political power and use a shared cooldown within their domain: 90 days, or 180 days for population policy. These are implementation balance choices. Every focus and decision previews the signed contribution change through native numeric formatters. The actual state change executes separately under runtime guards. The branch is visible independently of the governing party, and a government change alone does not repeal policy.

The branch is attached to the existing generic tree without replacing its 685 focuses. Its root is at (8,23), with four branches at (2,25), (6,25), (10,25) and (14,25). Existing content ends at y20. [Full-tree and branch preview](apartheid_1970/FOCUS_PREVIEW.html). This is a generated layout preview, not a game screenshot.

## Regional relations and historical exceptions

The worldwide -20 modifier is literal incoming trade-opinion points, not a -20% trade-opinion factor. The separate regional trade penalty is additive: at full intensity a non-exempt African partner has -70 trade opinion toward the regime, while the regime has the regional -50 toward that partner. Diplomatic opposition is -50 in both directions. Their intensity follows the political domain.

Sub-Saharan eligibility uses the country's actual African capital location and excludes the northern African countries. A regime's active minority government and actual colonial dependencies are exempt from the additional regional penalties. Known dependencies cease to qualify after independence. Authored future colonial or settler governments have explicit political-state flags; these are not inferred from a leader's ethnicity or a general ideology slot.

Malawi has a historical, revocable regional exception with South Africa. Contemporary US reporting describes Banda's willingness to deal with both Pretoria and Rhodesia; the implementation grants the starting exception only to the specifically established South African relationship. [US Department of State, 9 June 1967](https://history.state.gov/historicaldocuments/frus1964-68v24/d407)

Botswana, Lesotho and Swaziland have South African trade-only exceptions, while diplomatic opposition remains. Customs arrangements preceded their independence and continued through the renegotiated agreement signed on 11 December 1969, which entered into operation on 1 March 1970. The exception represents continuity of trade, not endorsement of apartheid. [1969 SACU agreement](https://www.sacu.int/uploads/documents/125758223bab6bd920ecdffe36a45553cf257e50.pdf)

After two political or public-service concessions, a host can propose normalisation for 50 political power. The named recipient receives acceptance and refusal decisions; previewing or sending an offer does not improve relations. A received offer lasts 180 days. Acceptance removes the regional trade and diplomatic penalties while peace and concessions continue. Worldwide trade opposition remains. War or policy backtracking suspends the exception, and the recipient can withdraw it. All three countries' independent origin namespaces prevent one refresh from erasing another country's modifiers.

## Verification and source credits

The scoped validator parses 13 runtime files and exercises all 3,125 policy combinations using emitted effects. It also checks repeated refresh, reversals, full removal, recipient-root acceptance, duplicate delivery, historical exceptions, colonial independence, dead senders, war, backtracking, save-model restoration, tag references, encoding and localisation escapes. The independent mechanics and layout review findings were incorporated. Native hovers, weekly engine calculations and multiplayer behavior still require an in-game rehearsal.

Sources are paraphrased. Original credits: Truth and Reconciliation Commission; Deborah Posel and the University of the Witwatersrand; Robert J. Corker and Tamim Bayoumi, IMF; South African Department of Agriculture; South African Department of Welfare and Population Development; US Department of State; and the signatory governments of the SACU agreement. Applicable licences or additional reproduction permissions are unknown. No source text, photographs or font files are redistributed. The design and calculations are original IMPERIA COLD WAR adaptation. Existing icon provenance is recorded in [the asset notice](apartheid_1970/ASSET_NOTICE.md).
