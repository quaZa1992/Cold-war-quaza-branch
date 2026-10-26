# COLDWAR — DPRK, January 1970–1990: approval concept

**167 focuses. Concept only. No loaded game files have been changed.**

All focus titles and descriptions are proposed English localization. Numerical values are balance proposals; API support is source-audited, engine behavior is not yet tested.

## Decisions to approve

- A historical WPK programme and seven conditional alternatives use the existing government slots, with 30 pairwise mutual exclusions across distinct policy dilemmas.
- KDP and Chondoist party governments, a military or technocratic government, and the smaller civic/left alternatives are explicitly counterfactual. Their branches unlock when the actual registered party governs; a focus does not manufacture that accession.
- Physical development, loan principal and signed interstate obligations survive government changes. Party programme modifiers deactivate on loss of office and return with the party, without replaying factories, money or research bonuses.
- No Salafi, Shia or other Muslim paths; no new independent paths for implausible registry filler. No resurrection of purged leaders, forced reunification, starting OOB changes, free uranium mines or instant weapons.

## Exact spatial plan

Native grid: 96 × 130 px; native item container 165 × 128 px; name field 147 × 20 px. Each section has an absolute root; all other coordinates are emitted relative to that root. Separate prerequisite blocks mean AND; members of one block mean OR. Visible connectors preserve those groups.

| Section | Root | Focuses | Government |
|---|---:|---:|---|
| Workers' Party of Korea | (6, 0) | 24 | slot 4 |
| Planning, Power and Living Standards | (16, 0) | 25 | all governments |
| The Korean People's Army | (30, 0) | 20 | all governments |
| Patrons and the Korean Question | (44, 0) | 18 | all governments |
| Science and the Atomic Question | (54, 0) | 8 | all governments |
| Korean Democratic Party | (4, 17) | 14 | slot 5 |
| Chondoist Chongu Party | (12, 17) | 14 | slot 7 |
| Cabinet and Planning Commission | (20, 17) | 10 | slot 13 |
| Military Emergency Government | (28, 17) | 10 | slot 22 |
| Yan'an Reform Communist Programme | (36, 17) | 8 | slot 2 |
| Industrial Labour Programme | (44, 17) | 8 | slot 3 |
| Christian Federation Programme | (52, 17) | 8 | slot 14 |

Initial camera: WPK root (6,0). Shortcuts: WPK, Economy, Armed Forces, Diplomacy, Atomic Programme, and each alternative programme. Continuous focuses occupy the lower-right pocket after the alternative branches; proposed position (5800,3750) px, pending engine verification. No unapproved shared joint-focus tree is attached.

All-government overview deliberately shows every proposed branch. In the game, native conditional branch visibility is only a presentation aid; actual party availability and reward guards remain authoritative. Dynamic hiding/reappearing of focus nodes is not promised until the native reevaluation mechanism is verified. The inspector includes all government states.

## Starting national spirits

### The Monolithic Ideological System

The purges have secured the Leader’s command while suppressing independent reporting and technical disagreement.

- Political power gain: +10%
- Stability: +6%
- Research speed: -5%
- Weekly administration expenditure: +8%

Replaced, not stacked, by Monolithic Leadership or Collective Deliberation. Party-bound and inactive outside WPK rule.

### Byungjin: Economy and Defence

The parallel build-up strengthens deterrence while defence absorbs labour, capital and public expenditure.

- Army defence on core territory: +8%
- Military factory construction: +8%
- Civilian factory construction: -10%
- Weekly army personnel expenditure: +10%

Army reorganization reduces this to a residual +4% core defence / -4% civilian construction burden; final national arsenal/civilian conversion choice replaces the residual.

### The Extended Seven-Year Plan

A developed industrial base is constrained by missed targets, weak input balances and repeated plan extensions.

- Productivity growth: -12%
- Production efficiency growth: -10%
- Weekly administration expenditure: +8%

Balance the Inputs removes this spirit after one substantive industrial priority and a funded project.

### Power and Imported Inputs

Power shortages and imported machinery and fuel limit the use of installed industrial capacity.

- Factory output: -8%
- Electricity consumption: +8%
- Population non-electric fuel demand: +6%

Repair the Power Grid removes the electricity/output component. Residual imported-input fuel burden remains until external resilience.

### An Uneven Civilian Supply

Civilian supply competes with heavy industry and defence; rural inputs and urban distribution remain uneven.

- Agricultural productivity: -8%
- Stability: -4%
- Weekly social expenditure: +6%

A Sustainable Ration removes this after both irrigation/fertilizer and county clinics. This is not the 1990s famine.

### Juche and the Two Patrons

Political autonomy is defended through cautious access to foreign technology and competition between external patrons.

- Foreign influence defence: +12%
- Trade opinion factor: -8%
- Research speed: -3%

Keep Both Doors Open replaces it with strategic autonomy: +6% influence defence / -3% trade opinion; signed external cooperation offsets selected technical disadvantages.

## Native rewards and integration contract

Country policies use explicit dynamic modifier definitions. Small ongoing expenditure changes are modifiers of the relevant **weekly native budget**, not invented flat daily/monthly fees. Investment costs are one-time billions through `treasury_change` / `modify_treasury_effect`; normal MD borrowing applies. Numeric expense modifiers are relative percentages, not absolute billions. The native budget calculation determines the weekly cash amount.

Buildings are paid grants only if a suitable owned state has actual capacity. Reserve/validate that state before charging the player. The descriptive regional selectors below must be resolved to real state predicates during implementation; no imported foreign state IDs are used.

Foreign agreements are proposed adapters around native effects, not existing named NKO APIs. The recipient sees concrete numeric option effects and may refuse. Charge and grant only at acceptance after both sides are rechecked, once per signed receipt; send accepted/refused/expired feedback and clear pending flags. A government change during negotiations invalidates a party-specific offer. Subsequent cooperation requires a still-valid signed agreement.

Party lifecycle: save completed-focus receipts; reconcile at startup, government change, monthly maintenance and load. Reattach earned conditional modifiers if the engine removes disabled entries. Reconciliation must never run one-time completion rewards. In-progress party focus: cancel on loss of rule, with the same party guard in its actual reward. Retain old branch completion and earned receipts for a later return.

Starting-spirit replacements are conditional on receipts. On load or party return, never restore the original monolithic spirit after one of its two replacements was earned. Shared policy choices remain mutually exclusive across government changes.

## Conditional incidents

### The Machinery Account

730 days after the recorded machinery loan, if its recorded principal remains outstanding.

Only a country that chose the loan can receive this crisis. No automatic historical default in January 1970. Meet the Foreign Bills resolves this account by one chosen response, not necessarily full repayment.

- Settle the account: {"treasury": "-min(7.5, recorded outstanding principal, total debt)", "debt": "Same principal reduction as the cash debit; one transaction. Normal native borrowing may cover the cash payment."}
- Negotiate a rescheduling: {"treasury": -2, "days": 730, "modifiers": {"interest_rate_multiplier_modifier": 1.0, "trade_opinion_factor": -0.1}, "debt": "Principal remains; no debt write-off."}
- Suspend repayments: {"treasury": 0, "days": 730, "modifiers": {"interest_rate_multiplier_modifier": 2.0, "trade_opinion_factor": -0.15, "stability_factor": -0.03}, "debt": "Principal remains; normal interest and credit consequences continue."}

### External Support Disrupted

A real signed supply/support agreement ceases or its provider changes terms; no forced behavior by SOV or CHI and no automatic calendar punishment.

New NKO event adapter around actual accepted/cancelled cooperation. It models late-Cold-War vulnerability without moving the 1990s famine into 1970.

- A signed replacement procurement agreement, or a $2.000 billion spare-parts programme. Patron Resilience halves this temporary penalty.
- {"industrial_capacity_factory": -0.08, "research_speed_factor": -0.03}

## Focus catalogue

### Workers' Party of Korea

Kim Il Sung remains the starting head of government. The heir is cultivated from 1974, not installed as ruler in 1970.

#### The Fifth Congress

`COLDWAR_NKO_fifth_congress` · (6,0) · relative (0,0) · 21 days · Party programme

Set the programme of the party congress after the extended Seven-Year Plan.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 4.

- Political power gain: +5%.
- Weekly administration expenditure: +3% of its native weekly baseline.
- Planning decisions — Open a choice of the already designed national investment programmes; no separate reward for opening the menu.

#### Monolithic Leadership

`COLDWAR_NKO_monolithic` · (4,1) · relative (-2,1) · 35 days · Party programme

Concentrate authority in the Leader and his trusted cadre network.

Prerequisites: (fifth_congress).
Mutually exclusive: COLDWAR_NKO_collective.
Availability and guarded reward: actual ruling subparty = 4.

- Political power gain: +16%.
- Stability: +8%.
- Research speed: -6%.
- Weekly administration expenditure: +10% of its native weekly baseline.
- Starting constraint replaced/removed: monolithic_start.

#### Collective Deliberation

`COLDWAR_NKO_collective` · (8,1) · relative (2,1) · 35 days · Party programme

Restore policy debate within the Workers’ Party while accepting a less unified command.

Prerequisites: (fifth_congress).
Mutually exclusive: COLDWAR_NKO_monolithic.
Availability and guarded reward: actual ruling subparty = 4.

- Research speed: +7%.
- Productivity growth: +6%.
- Stability: -6%.
- Weekly administration expenditure: +8% of its native weekly baseline.
- Starting constraint replaced/removed: monolithic_start.

#### Loyal Appointments

`COLDWAR_NKO_loyalty` · (4,2) · relative (-2,2) · 35 days · Party programme

Promote politically reliable officials, narrowing the pool of technical talent.

Prerequisites: (monolithic).
Availability and guarded reward: actual ruling subparty = 4.

- Foreign influence defence: +10%.
- Productivity growth: -3%.

#### Candid Reports

`COLDWAR_NKO_debate` · (8,2) · relative (2,2) · 35 days · Party programme

Let ministries report missed targets without treating every failure as disloyalty.

Prerequisites: (collective).
Availability and guarded reward: actual ruling subparty = 4.

- Productivity growth: +5%.
- Political power gain: -5%.

#### The Presidential State

`COLDWAR_NKO_presidency` · (4,3) · relative (-2,3) · 35 days · Party programme

Gather constitutional and administrative authority around Kim Il Sung.

Prerequisites: (loyalty).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: Historical timing: 1972 constitution or a separately negotiated earlier constitutional settlement.

- Political power gain: +6%.
- Weekly policing expenditure: +5% of its native weekly baseline.

#### Cabinet Accountability

`COLDWAR_NKO_cabinet_reports` · (8,3) · relative (2,3) · 35 days · Party programme

Require ministers to defend plans and expenditure before a collective party leadership.

Prerequisites: (debate).
Availability and guarded reward: actual ruling subparty = 4.

- Weekly administration expenditure: -6% of its native weekly baseline.
- Political power gain: -3%.

#### The Ten Principles

`COLDWAR_NKO_ten_principles` · (4,4) · relative (-2,4) · 35 days · Party programme

Bind institutions to a uniform ideological hierarchy.

Prerequisites: (presidency).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: Historical timing: 1974; earlier completion would be explicitly alternate history.

- Stability: +4%.
- Research speed: -2%.

#### Professional Cadres

`COLDWAR_NKO_cadre_tenure` · (8,4) · relative (2,4) · 35 days · Party programme

Protect experienced administrators while accepting a more entrenched bureaucracy.

Prerequisites: (cabinet_reports).
Availability and guarded reward: actual ruling subparty = 4.

- Research speed: +4%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### The Party Settlement

`COLDWAR_NKO_party_settlement` · (6,5) · relative (0,5) · 35 days · Party programme

Consolidate the institutional settlement chosen by the congress.

Prerequisites: (ten_principles OR cadre_tenure).
Availability and guarded reward: actual ruling subparty = 4.

- Foreign influence defence: +6%.

#### Campaign Mobilization

`COLDWAR_NKO_campaigns` · (4,6) · relative (-2,6) · 35 days · Party programme

Concentrate labour on visible projects at the expense of routine production and household provision.

Prerequisites: (party_settlement).
Mutually exclusive: COLDWAR_NKO_technical_cadres.
Availability and guarded reward: actual ruling subparty = 4.

- Construction speed: +10%.
- Productivity growth: -4%.
- Weekly social expenditure: +4% of its native weekly baseline.

#### Technical Cadres

`COLDWAR_NKO_technical_cadres` · (8,6) · relative (2,6) · 35 days · Party programme

Replace emergency campaigns with trained supervision and measured investment.

Prerequisites: (party_settlement).
Mutually exclusive: COLDWAR_NKO_campaigns.
Availability and guarded reward: actual ruling subparty = 4.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +8%.
- Construction speed: -5%.
- Weekly education expenditure: +8% of its native weekly baseline.

#### Three Revolutions

`COLDWAR_NKO_three_revolutions` · (4,7) · relative (-2,7) · 35 days · Party programme

Send ideological, technical and cultural teams into workplaces.

Prerequisites: (campaigns).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: Historical timing: movement organized from 1973.

- Production efficiency growth: +8%.
- Weekly administration expenditure: +6% of its native weekly baseline.

#### Ministry Engineers

`COLDWAR_NKO_engineer_commissions` · (8,7) · relative (2,7) · 35 days · Party programme

Give technical commissions the authority to revise unrealistic orders.

Prerequisites: (technical_cadres).
Availability and guarded reward: actual ruling subparty = 4.

- Production efficiency cap: +6%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Red Banner Campaign

`COLDWAR_NKO_red_banner` · (4,8) · relative (-2,8) · 35 days · Party programme

Reward accelerated production and model work teams while placing further pressure on inputs.

Prerequisites: (three_revolutions).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: Historical timing: 1975 campaign.

- Factory output: +6%.
- Electricity consumption: +5%.
- Stability: -2%.

#### Achievable Targets

`COLDWAR_NKO_honest_targets` · (8,8) · relative (2,8) · 35 days · Party programme

Accept less spectacular headlines in return for plans that plants can deliver.

Prerequisites: (engineer_commissions).
Availability and guarded reward: actual ruling subparty = 4.

- Productivity growth: +5%.
- Political power gain: -4%.

#### Discipline in the Plan

`COLDWAR_NKO_plan_discipline` · (6,9) · relative (0,9) · 35 days · Party programme

Carry the chosen management settlement into the next planning period.

Prerequisites: (red_banner OR honest_targets).
Availability and guarded reward: actual ruling subparty = 4.

- Production efficiency growth: +4%.

#### Cultivate the Centre

`COLDWAR_NKO_family_succession` · (4,10) · relative (-2,10) · 35 days · Party programme

Build Kim Jong Il’s authority inside the party without displacing Kim Il Sung.

Prerequisites: (plan_discipline).
Mutually exclusive: COLDWAR_NKO_committee_succession.
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: From 1974; Kim Il Sung in office; successor alive.

- Political power gain: +8%.
- Weekly administration expenditure: +6% of its native weekly baseline.
- Research speed: -2%.

#### A Collective Succession

`COLDWAR_NKO_committee_succession` · (8,10) · relative (2,10) · 35 days · Party programme

Prepare a committee succession instead of a hereditary transfer.

Prerequisites: (plan_discipline).
Mutually exclusive: COLDWAR_NKO_family_succession.
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: From 1974; Kim Il Sung in office; an explicitly counterfactual settlement.

- Research speed: +5%.
- Productivity growth: +4%.
- Stability: -6%.

#### The Party and the Arts

`COLDWAR_NKO_party_media` · (4,11) · relative (-2,11) · 35 days · Party programme

Finance a cultural apparatus that presents the successor as the guardian of continuity.

Prerequisites: (family_succession).
Availability and guarded reward: actual ruling subparty = 4.

- Stability: +5%.
- Weekly social expenditure: +5% of its native weekly baseline.

#### Responsible Secretariat

`COLDWAR_NKO_secretariat` · (8,11) · relative (2,11) · 35 days · Party programme

Distribute appointments among a responsible secretariat rather than the ruling household.

Prerequisites: (committee_succession).
Availability and guarded reward: actual ruling subparty = 4.

- Weekly administration expenditure: -5% of its native weekly baseline.
- Political power gain: -3%.

#### The Sixth Congress

`COLDWAR_NKO_sixth_congress` · (4,12) · relative (-2,12) · 35 days · Party programme

Publicly confirm the successor’s party offices while the founding Leader remains in command.

Prerequisites: (party_media).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: From October 1980; no automatic head-of-state replacement.

- Foreign influence defence: +8%.
- Research speed: -2%.

#### Succession Rules

`COLDWAR_NKO_succession_rules` · (8,12) · relative (2,12) · 35 days · Party programme

Set procedures for a future vacancy and bind commanders to the institutional settlement.

Prerequisites: (secretariat).
Availability and guarded reward: actual ruling subparty = 4.
Additional requirement: Requires an agreed counterfactual succession settlement; no purge victim is resurrected.

- Stability: +4%.
- Weekly administration expenditure: +3% of its native weekly baseline.

#### Beyond the Founder

`COLDWAR_NKO_continuity` · (6,13) · relative (0,13) · 35 days · Party programme

Secure continuity through the leadership settlement the country has chosen.

Prerequisites: (sixth_congress OR succession_rules).
Availability and guarded reward: actual ruling subparty = 4.

- Productivity growth: +4%.
- Weekly administration expenditure: +3% of its native weekly baseline.

### Planning, Power and Living Standards

Industrial Korea with real bottlenecks, not a pre-industrial blank slate. Native building employment, fuel, power and maintenance remain active.

#### Extended Plan Review

`COLDWAR_NKO_plan_review` · (16,0) · relative (0,0) · 21 days · National policy / durable development

Audit the gap between targets, installed capacity and available supplies.

Prerequisites: Section entry.

- Production efficiency growth: +4%.

#### Heavy Industry First

`COLDWAR_NKO_heavy_priority` · (12,1) · relative (-4,1) · 35 days · National policy / durable development

Prioritize metals and machinery while scarce capital is withheld from agriculture and household output.

Prerequisites: (plan_review).
Mutually exclusive: COLDWAR_NKO_light_priority, COLDWAR_NKO_balanced_priority.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Military factory construction: +12%.
- Production efficiency cap: +8%.
- Agricultural productivity: -6%.
- Electricity consumption: +8%.

#### Food and Light Industry

`COLDWAR_NKO_light_priority` · (16,1) · relative (0,1) · 35 days · National policy / durable development

Direct investment toward everyday supply at a cost to the defence-industrial build-up.

Prerequisites: (plan_review).
Mutually exclusive: COLDWAR_NKO_heavy_priority, COLDWAR_NKO_balanced_priority.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Agricultural productivity: +12%.
- Civilian factory construction: +10%.
- Military factory construction: -8%.
- Weekly social expenditure: +5% of its native weekly baseline.

#### Industrial Growth

`COLDWAR_NKO_balanced_priority` · (20,1) · relative (4,1) · 35 days · National policy / durable development

Adopt a slower investment plan with more reliable input balances.

Prerequisites: (plan_review).
Mutually exclusive: COLDWAR_NKO_heavy_priority, COLDWAR_NKO_light_priority.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Productivity growth: +8%.
- Production efficiency growth: +6%.
- Construction speed: -4%.
- Weekly administration expenditure: +5% of its native weekly baseline.

#### Modernize Steelworks

`COLDWAR_NKO_steelworks` · (12,2) · relative (-4,2) · 35 days · National policy / durable development

Refit the established steel and engineering complexes that support national industrialization.

Prerequisites: (heavy_priority).

- Treasury: −$7.500 billion once; native borrowing remains available.
- Fund 1 arms factory level. Candidate states in priority order: 602, 601. Full price $7.500 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Equip the Cooperatives

`COLDWAR_NKO_food_district` · (16,2) · relative (0,2) · 35 days · National policy / durable development

Equip the cooperatives with machinery and storage, and stabilize the delivery of rural inputs.

Prerequisites: (light_priority).

- Treasury: −$3.750 billion once; native borrowing remains available.
- Fund 1 agriculture district level. Candidate states in priority order: 603, 602. Full price $3.750 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Machine Tool Standards

`COLDWAR_NKO_machine_tools` · (20,2) · relative (4,2) · 35 days · National policy / durable development

Improve interchangeability and maintenance rather than chasing gross output totals.

Prerequisites: (balanced_priority).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Production efficiency cap: +6%.
- Weekly education expenditure: +4% of its native weekly baseline.

#### Balance the Inputs

`COLDWAR_NKO_input_balance` · (16,3) · relative (0,3) · 35 days · National policy / durable development

Bring transport, electricity and intermediate supplies into the investment plan.

Prerequisites: (steelworks OR food_district OR machine_tools).

- Productivity growth: +4%.
- Starting constraint replaced/removed: plan_overstretch.

#### Coal-fired Expansion

`COLDWAR_NKO_coal_power` · (14,4) · relative (-2,4) · 49 days · National policy / durable development

Expand coal-fired generating capacity to sustain the industrial plan.

Prerequisites: (input_balance).
Mutually exclusive: COLDWAR_NKO_hydro_power.

- Treasury: −$3.250 billion once; native borrowing remains available.
- Fund 1 fossil powerplant level. Candidate states in priority order: 602, 601. Full price $3.250 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Hydropower Plan

`COLDWAR_NKO_hydro_power` · (18,4) · relative (2,4) · 49 days · National policy / durable development

Invest in inland water power to reduce dependence on imported fossil fuels.

Prerequisites: (input_balance).
Mutually exclusive: COLDWAR_NKO_coal_power.

- Treasury: −$8.500 billion once; native borrowing remains available.
- Fund 1 renewable energy infra level. Candidate states in priority order: 1201, 1199. Full price $8.500 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Repair the Power Grid

`COLDWAR_NKO_power_grid` · (16,5) · relative (0,5) · 35 days · National policy / durable development

Reduce transmission losses through paid grid maintenance.

Prerequisites: (coal_power OR hydro_power).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Electricity consumption: -8%.
- Imported-input residual — Replace the power bottleneck spirit with population non-electric fuel demand +6%; remove this residual at Patron Resilience.
- Starting constraint replaced/removed: power_bottleneck.

#### Industrial Rail Corridor

`COLDWAR_NKO_rail_corridor` · (14,6) · relative (-2,6) · 35 days · National policy / durable development

Increase infrastructure along an owned industrial corridor.

Prerequisites: (power_grid).

- Treasury: −$3.500 billion once; native borrowing remains available.
- Fund 1 infrastructure level. Candidate states in priority order: 602, 1200, 601. Full price $3.500 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Housing near the Plants

`COLDWAR_NKO_housing` · (18,6) · relative (2,6) · 35 days · National policy / durable development

Fund housing and urban services so industrial recruitment can be sustained.

Prerequisites: (power_grid).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Stability: +4%.
- Weekly social expenditure: +6% of its native weekly baseline.

#### Fertilizer and Irrigation

`COLDWAR_NKO_fertilizer` · (14,7) · relative (-2,7) · 35 days · National policy / durable development

Improve yields through inputs that require electricity and dependable distribution.

Prerequisites: (rail_corridor).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Agricultural productivity: +8%.
- Electricity consumption: +4%.

#### County Clinics

`COLDWAR_NKO_public_health` · (18,7) · relative (2,7) · 35 days · National policy / durable development

Expand basic healthcare at a continuing public cost.

Prerequisites: (housing).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +4%.
- Weekly healthcare expenditure: +8% of its native weekly baseline.

#### A Sustainable Ration

`COLDWAR_NKO_living_standards` · (16,8) · relative (0,8) · 35 days · National policy / durable development

Improve the reliability of food distribution after investment in rural and urban supply.

Prerequisites: (fertilizer) AND (public_health).

- Agricultural productivity: +5%.
- Weekly social expenditure: +3% of its native weekly baseline.
- Starting constraint replaced/removed: ration_strain.

#### State Procurement

`COLDWAR_NKO_state_procurement` · (14,9) · relative (-2,9) · 35 days · National policy / durable development

Stabilize procurement through guaranteed state purchasing and closer supervision.

Prerequisites: (living_standards).
Mutually exclusive: COLDWAR_NKO_household_plots.

- Agricultural productivity: +8%.
- Tax revenue: +4%.
- Productivity growth: -3%.
- Weekly administration expenditure: +6% of its native weekly baseline.

#### Household Plots

`COLDWAR_NKO_household_plots` · (18,9) · relative (2,9) · 35 days · National policy / durable development

Let households retain more produce while accepting weaker state extraction.

Prerequisites: (living_standards).
Mutually exclusive: COLDWAR_NKO_state_procurement.

- Agricultural productivity: +12%.
- Productivity growth: +4%.
- Tax revenue: -5%.
- Political power gain: -3%.

#### Distribution Depots

`COLDWAR_NKO_distribution_reform` · (16,10) · relative (0,10) · 35 days · National policy / durable development

Build a distribution network that reduces waste and supplies the army and civilian economy.

Prerequisites: (state_procurement OR household_plots).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Supply consumption: -4%.
- Weekly administration expenditure: +3% of its native weekly baseline.

#### Domestic Savings

`COLDWAR_NKO_domestic_finance` · (14,11) · relative (-2,11) · 35 days · National policy / durable development

Avoid a hard-currency borrowing surge by accepting slower investment.

Prerequisites: (distribution_reform).
Mutually exclusive: COLDWAR_NKO_western_credit.

- Annual interest rate, percentage points: -0.35 percentage points.
- Construction speed: -4%.
- Weekly social expenditure: +4% of its native weekly baseline.

#### Machinery on Credit

`COLDWAR_NKO_western_credit` · (18,11) · relative (2,11) · 35 days · National policy / durable development

Borrow to purchase foreign plant and accept debt service and a weaker credit position.

Prerequisites: (distribution_reform).
Mutually exclusive: COLDWAR_NKO_domestic_finance.

- Productivity growth: +12%.
- Production efficiency cap: +6%.
- Annual interest rate, percentage points: +1.25 percentage points.
- Machinery credit: borrow $7.500 billion, spend the loan on the financed factory; native principal and interest remain.
- Fund 1 industrial complex level. Candidate states in priority order: 602, 1200. Full price $7.500 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Industrial Schools

`COLDWAR_NKO_technical_schools` · (14,12) · relative (-2,12) · 35 days · National policy / durable development

Train technicians domestically instead of relying on a larger foreign-credit package.

Prerequisites: (domestic_finance).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Weekly education expenditure: +6% of its native weekly baseline.

#### Meet the Foreign Bills

`COLDWAR_NKO_credit_reckoning` · (18,12) · relative (2,12) · 35 days · National policy / durable development

Resolve the machinery account through repayment or a negotiated rescheduling.

Prerequisites: (western_credit).

- Productivity growth: +3%.
- Repay at most $7.500 billion of the recorded machinery principal; payment and principal reduction occur once, not twice.

#### Quality for Export

`COLDWAR_NKO_export_quality` · (16,13) · relative (0,13) · 35 days · National policy / durable development

Slow production-line changes to improve the consistency of saleable output.

Prerequisites: (technical_schools OR credit_reckoning).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +4%.
- Production efficiency growth: -3%.

#### Controlled Ventures

`COLDWAR_NKO_joint_ventures` · (16,14) · relative (0,14) · 35 days · National policy / durable development

Offer tightly limited partnerships and tax concessions without assuming foreign investors will provide free capital.

Prerequisites: (export_quality).
Additional requirement: Historical law from 1984, or an explicit earlier alternate reform.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Productivity growth: +6%.
- Corporate tax revenue: -5%.
- Foreign influence defence: -5%.
- Joint venture offers — Recipient-consent investment contracts use existing Imperia investment hooks; no unconditional foreign factory grant.

### The Korean People's Army

Native defense, personnel and equipment costs remain. No starting units, future technology or free stockpiles are granted.

#### Lessons of 1969

`COLDWAR_NKO_lessons_1969` · (30,0) · relative (0,0) · 21 days · National policy / durable development

Review the 1968–69 confrontation and restore professional military reporting.

Prerequisites: Section entry.

- Army experience gain: +6%.
- Weekly army personnel expenditure: +3% of its native weekly baseline.

#### The Fortress State

`COLDWAR_NKO_fortress` · (28,1) · relative (-2,1) · 35 days · National policy / durable development

Prepare an economical territorial defence at the cost of offensive flexibility.

Prerequisites: (lessons_1969).
Mutually exclusive: COLDWAR_NKO_mobile_army.

- Army defence on core territory: +12%.
- Supply consumption: -6%.
- Army attack: -6%.
- Productivity growth: -4%.

#### A Mobile Field Army

`COLDWAR_NKO_mobile_army` · (32,1) · relative (2,1) · 35 days · National policy / durable development

Build a more flexible field army that consumes more equipment and fuel.

Prerequisites: (lessons_1969).
Mutually exclusive: COLDWAR_NKO_fortress.

- Army organization: +8%.
- Maximum planning: +8%.
- Weekly equipment expenditure: +12% of its native weekly baseline.
- Army fuel consumption: +8%.

#### Worker-Peasant Guards

`COLDWAR_NKO_red_guards` · (28,2) · relative (-2,2) · 35 days · National policy / durable development

Expand reserve training while removing civilian labour from regular production.

Prerequisites: (fortress).

- Army defence on core territory: +6%.
- Training time: -8%.
- Productivity growth: -4%.

#### General Staff College

`COLDWAR_NKO_staff_college` · (32,2) · relative (2,2) · 35 days · National policy / durable development

Improve staff work through a paid officer education programme.

Prerequisites: (mobile_army).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Maximum planning: +6%.
- Army experience gain: +6%.
- Weekly education expenditure: +5% of its native weekly baseline.

#### Reorganize Command

`COLDWAR_NKO_army_reorganization` · (30,3) · relative (0,3) · 35 days · National policy / durable development

Translate the selected doctrine into command and logistics procedures.

Prerequisites: (red_guards OR staff_college).

- Army organization: +4%.
- Weekly administration expenditure: +3% of its native weekly baseline.
- Replace Byungjin burden — Replace the starting Byungjin spirit with core defence +4% and civilian factory construction -4%.

#### Artillery Concentration

`COLDWAR_NKO_mass_artillery` · (24,4) · relative (-6,4) · 35 days · National policy / durable development

Concentrate firepower while accepting greater ammunition and transport requirements.

Prerequisites: (army_reorganization).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Army attack: +6%.
- Supply consumption: +8%.
- Weekly equipment expenditure: +5% of its native weekly baseline.

#### Air Defence Commands

`COLDWAR_NKO_air_defence` · (28,4) · relative (-2,4) · 35 days · National policy / durable development

Improve coordination of fighter aviation, warning services and ground-based air defence.

Prerequisites: (army_reorganization).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Air mission efficiency: +6%.
- Weekly equipment expenditure: +6% of its native weekly baseline.

#### Coastal Denial

`COLDWAR_NKO_coastal_denial` · (32,4) · relative (2,4) · 35 days · National policy / durable development

Concentrate naval training on denying coastal access.

Prerequisites: (army_reorganization).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Naval organization: +6%.
- Weekly equipment expenditure: +4% of its native weekly baseline.

#### Special Operations

`COLDWAR_NKO_special_operations` · (36,4) · relative (6,4) · 35 days · National policy / durable development

Train specialist formations at a cost to the regular army’s resources.

Prerequisites: (army_reorganization).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Special forces capacity: +12%.
- Weekly army personnel expenditure: +6% of its native weekly baseline.
- Army organization: -2%.

#### Ammunition Standards

`COLDWAR_NKO_ammunition_standards` · (24,5) · relative (-6,5) · 35 days · National policy / durable development

Standardize ammunition at the expense of flexible production changes.

Prerequisites: (mass_artillery).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Production efficiency cap: +6%.
- Production efficiency growth: -4%.

#### Air Warning Network

`COLDWAR_NKO_air_warning` · (28,5) · relative (-2,5) · 35 days · National policy / durable development

Extend early warning and communications coverage across the northern approaches.

Prerequisites: (air_defence).

- Treasury: −$1.750 billion once; native borrowing remains available.
- Fund 1 radar station level. Candidate states in priority order: 601, 1200. Full price $1.750 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Naval Workshops

`COLDWAR_NKO_naval_workshops` · (32,5) · relative (2,5) · 35 days · National policy / durable development

Expand the coastal yards to maintain the fleet and sustain a modest naval-industrial base.

Prerequisites: (coastal_denial).

- Treasury: −$7.500 billion once; native borrowing remains available.
- Fund 1 dockyard level. Candidate states in priority order: 601, 1199, 602. Full price $7.500 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### Reconnaissance Plan

`COLDWAR_NKO_reconnaissance` · (36,5) · relative (6,5) · 35 days · National policy / durable development

Improve reconnaissance training and the quality of operational preparation.

Prerequisites: (special_operations).

- Maximum planning: +5%.
- Weekly army personnel expenditure: +3% of its native weekly baseline.

#### Joint Logistics

`COLDWAR_NKO_joint_logistics` · (30,6) · relative (0,6) · 35 days · National policy / durable development

Unify logistics across all four service programmes.

Prerequisites: (ammunition_standards) AND (air_warning) AND (naval_workshops) AND (reconnaissance).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Supply consumption: -6%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Workshop Conversion

`COLDWAR_NKO_civilian_conversions` · (28,7) · relative (-2,7) · 35 days · National policy / durable development

Release industrial workshops for civilian production while reducing military expansion.

Prerequisites: (joint_logistics).
Mutually exclusive: COLDWAR_NKO_arsenal_priority.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Civilian factory construction: +10%.
- Military factory construction: -8%.
- Weekly equipment expenditure: +4% of its native weekly baseline.
- Starting constraint replaced/removed: byungjin_residual.

#### Arsenal Priority

`COLDWAR_NKO_arsenal_priority` · (32,7) · relative (2,7) · 35 days · National policy / durable development

Give defence plants priority over civilian construction and power allocation.

Prerequisites: (joint_logistics).
Mutually exclusive: COLDWAR_NKO_civilian_conversions.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Factory output: +8%.
- Civilian factory construction: -8%.
- Electricity consumption: +6%.
- Starting constraint replaced/removed: byungjin_residual.

#### A Maintained Reserve

`COLDWAR_NKO_logistics_reserve` · (30,8) · relative (0,8) · 35 days · National policy / durable development

Maintain a sustainable reserve rather than a paper mobilization total.

Prerequisites: (civilian_conversions OR arsenal_priority).

- Army organization: +4%.
- Weekly army personnel expenditure: +5% of its native weekly baseline.

#### Military Institutes

`COLDWAR_NKO_military_research` · (28,9) · relative (-2,9) · 35 days · National policy / durable development

Improve domestic military engineering and testing.

Prerequisites: (logistics_reserve).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +3%.
- Weekly education expenditure: +4% of its native weekly baseline.

#### Readiness Inspections

`COLDWAR_NKO_readiness_inspections` · (32,9) · relative (2,9) · 35 days · National policy / durable development

Make readiness reporting more demanding and allow more time for effective training.

Prerequisites: (logistics_reserve).

- Army organization: +3%.
- Training time: +4%.

### Patrons and the Korean Question

Every agreement has a recipient-controlled reply. No forced faction membership, annexation, tribute or aid from another player.

#### Independent Diplomacy

`COLDWAR_NKO_independent_diplomacy` · (44,0) · relative (0,0) · 21 days · National policy / durable development

Preserve freedom of action while bargaining with the larger powers.

Prerequisites: Section entry.

- Foreign influence defence: +8%.
- Trade opinion factor: -5%.

#### Soviet Machinery Offer

`COLDWAR_NKO_moscow_offer` · (40,1) · relative (-4,1) · 35 days · National policy / durable development

Request a paid machinery package on terms Moscow can accept or refuse.

Prerequisites: (independent_diplomacy).

- Offer — Soviet machinery contract: NKO receives 1 civilian factory in an eligible owned and controlled industrial state; SOV receives $7.500 billion. No payout on refusal. Payer: NKO, $7.500 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Repair Ties with Beijing

`COLDWAR_NKO_beijing_offer` · (44,1) · relative (0,1) · 35 days · National policy / durable development

Propose a paid agricultural and technical cooperation agreement.

Prerequisites: (independent_diplomacy).

- Offer — Chinese agricultural cooperation: NKO gains agricultural productivity +5% and research speed +2% for 730 days; CHI receives $1.000 billion. Payer: NKO, $1.000 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Chongryon Trade

`COLDWAR_NKO_diaspora_trade` · (48,1) · relative (4,1) · 35 days · National policy / durable development

Use diaspora firms to widen technical and commercial contacts without treating remittances as unlimited income.

Prerequisites: (independent_diplomacy).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +5%.
- Corporate tax revenue: -4%.
- Foreign influence defence: -3%.

#### Soviet Placements

`COLDWAR_NKO_soviet_training` · (40,2) · relative (-4,2) · 35 days · National policy / durable development

Place Korean engineers in Soviet institutions after an agreement is signed.

Prerequisites: (moscow_offer).
Additional requirement: Requires the Soviet machinery agreement, not merely completion of its offer focus.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Foreign influence defence: -4%.
- Weekly education expenditure: +3% of its native weekly baseline.

#### Regularize Border Trade

`COLDWAR_NKO_border_trade` · (44,2) · relative (0,2) · 35 days · National policy / durable development

Provide customs and storage facilities for regulated trade.

Prerequisites: (beijing_offer).
Additional requirement: Requires the Chinese cooperation agreement, not merely completion of its offer focus.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Agricultural productivity: +4%.
- Tax revenue: -2%.

#### Commercial Offices

`COLDWAR_NKO_export_offices` · (48,2) · relative (4,2) · 35 days · National policy / durable development

Fund a professional commercial service rather than relying solely on political delegations.

Prerequisites: (diaspora_trade).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Trade opinion factor: +8%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Keep Both Doors Open

`COLDWAR_NKO_external_balance` · (44,3) · relative (0,3) · 35 days · National policy / durable development

Maintain a diversified foreign procurement policy. Moscow and Beijing remain mixable partners.

Prerequisites: (soviet_training OR border_trade OR export_offices).

- Foreign influence defence: +5%.
- Weekly administration expenditure: +3% of its native weekly baseline.
- Strategic autonomy settlement — Replace Juche and the Two Patrons with foreign influence defence +6% and trade opinion -3%.

#### Inter-Korean Channel

`COLDWAR_NKO_detente` · (42,4) · relative (-2,4) · 35 days · National policy / durable development

Offer talks on divided families, communications and reduced tension.

Prerequisites: (external_balance).
Mutually exclusive: COLDWAR_NKO_coercion.

- Trade opinion factor: +8%.
- Army attack: -4%.
- Weekly policing expenditure: +3% of its native weekly baseline.
- Offer — Inter-Korean channel: Both receive stability +3 percentage points once and a 365-day trade-opinion factor +10%; KOR receives $1.000 billion for joint arrangements. Payer: NKO, $1.000 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Armistice Pressure

`COLDWAR_NKO_coercion` · (46,4) · relative (2,4) · 35 days · National policy / durable development

Use pressure and readiness as bargaining instruments while accepting a more difficult trade environment.

Prerequisites: (external_balance).
Mutually exclusive: COLDWAR_NKO_detente.

- Maximum planning: +8%.
- Trade opinion factor: -15%.
- Weekly policing expenditure: +8% of its native weekly baseline.

#### Divided Families

`COLDWAR_NKO_red_cross` · (42,5) · relative (-2,5) · 35 days · National policy / durable development

Finance contact and travel arrangements only after both governments agree.

Prerequisites: (detente).
Additional requirement: Requires the signed inter-Korean channel.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Stability: +3%.
- Weekly administration expenditure: +3% of its native weekly baseline.

#### Reunification Radio

`COLDWAR_NKO_front_broadcasting` · (46,5) · relative (2,5) · 35 days · National policy / durable development

Strengthen the united front’s radio services and political messaging toward the South.

Prerequisites: (coercion).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Foreign influence defence: +5%.
- Weekly policing expenditure: +4% of its native weekly baseline.

#### Confederation Proposal

`COLDWAR_NKO_confederation_offer` · (42,6) · relative (-2,6) · 35 days · National policy / durable development

Propose a confederal consultative council based on continued sovereignty and negotiated cooperation.

Prerequisites: (red_cross).
Additional requirement: Requires signed channel; both states independent and at peace.

- Offer — Confederal consultative council: KOR receives $2.000 billion. Both countries receive trade opinion +10% and weekly administration expenditure +3% while the council agreement is valid; no annexation or forced alliance. Payer: NKO, $2.000 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Armed Bargaining

`COLDWAR_NKO_armed_bargaining` · (46,6) · relative (2,6) · 35 days · National policy / durable development

Maintain a stronger military negotiating position at a continuing financial cost.

Prerequisites: (front_broadcasting).

- Army defence on core territory: +5%.
- Weekly equipment expenditure: +5% of its native weekly baseline.
- Trade opinion factor: -5%.

#### Non-Aligned Standing

`COLDWAR_NKO_recognition` · (44,7) · relative (0,7) · 35 days · National policy / durable development

Build diplomatic representation among non-aligned states and seek wider recognition of the Republic.

Prerequisites: (confederation_offer OR armed_bargaining).

- Treasury: −$1.000 billion once; native borrowing remains available.
- Trade opinion factor: +6%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Civilian Export Missions

`COLDWAR_NKO_civilian_export` · (42,8) · relative (-2,8) · 35 days · National policy / durable development

Offer commercial concessions to establish dependable markets for civilian exports.

Prerequisites: (recognition).
Mutually exclusive: COLDWAR_NKO_security_export.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Trade opinion factor: +10%.
- Corporate tax revenue: -3%.

#### Military Missions

`COLDWAR_NKO_security_export` · (46,8) · relative (2,8) · 35 days · National policy / durable development

Develop bilateral military training and advisory missions with willing partners.

Prerequisites: (recognition).
Mutually exclusive: COLDWAR_NKO_civilian_export.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Army experience gain: +8%.
- Weekly army personnel expenditure: +6% of its native weekly baseline.
- Trade opinion factor: -6%.

#### Patron Resilience

`COLDWAR_NKO_external_resilience` · (44,9) · relative (0,9) · 35 days · National policy / durable development

Diversify inventories and replacement sources to reduce exposure to external restrictions.

Prerequisites: (civilian_export OR security_export).

- Treasury: −$2.000 billion once; native borrowing remains available.
- Imperia sanction resistance: +6%.
- Productivity growth: -3%.
- Starting constraint replaced/removed: imported_input_residual.

### Science and the Atomic Question

Uses the existing Imperia / Cold War nuclear programme. No automatic uranium output, mines, fissile material or completed weapon.

#### Academy of Sciences

`COLDWAR_NKO_science` · (54,0) · relative (0,0) · 21 days · National policy / durable development

Support the scientific institutions needed for a long technical programme.

Prerequisites: Section entry.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +3%.
- Weekly education expenditure: +5% of its native weekly baseline.

#### Reactor Engineering

`COLDWAR_NKO_reactor_training` · (54,1) · relative (0,1) · 35 days · National policy / durable development

Train engineers in research-reactor operation, radiation science and laboratory practice.

Prerequisites: (science).

- Treasury: −$2.000 billion once; native borrowing remains available.
- CAT_nuclear_reactors: 1 × 50% research bonus; no free technology.

#### Civil Atomic Pact

`COLDWAR_NKO_civil_atom` · (52,2) · relative (-2,2) · 35 days · National policy / durable development

Seek foreign technical cooperation under verifiable limits on the atomic programme.

Prerequisites: (reactor_training).
Mutually exclusive: COLDWAR_NKO_sovereign_atom.

- Research speed: +4%.
- Foreign influence defence: -4%.
- Offer — Civil nuclear engineering contract: SOV receives $3.000 billion; NKO receives one additional 50% reactor research bonus and no free reactor. Payer: NKO, $3.000 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Sovereign Atom Study

`COLDWAR_NKO_sovereign_atom` · (56,2) · relative (2,2) · 35 days · National policy / durable development

Invest in a national nuclear research programme while accepting cost and external suspicion.

Prerequisites: (reactor_training).
Mutually exclusive: COLDWAR_NKO_civil_atom.

- Treasury: −$3.000 billion once; native borrowing remains available.
- Research speed: +3%.
- Weekly education expenditure: +8% of its native weekly baseline.
- Imperia sanction resistance: -6%.

#### Reactor Safeguards

`COLDWAR_NKO_safeguards` · (52,3) · relative (-2,3) · 35 days · National policy / durable development

Register safeguards obligations on the research programme.

Prerequisites: (civil_atom).
Additional requirement: Signed civil cooperation; inspection obligations implemented through a new country adapter, not claimed as an existing NPT system.

- Trade opinion factor: +6%.
- Weekly administration expenditure: +4% of its native weekly baseline.
- Safeguards contract — Recipient-confirmed inspection contract. Violating the agreed terms suspends the contract rewards.

#### The Domestic Fuel Cycle

`COLDWAR_NKO_fuel_studies` · (56,3) · relative (2,3) · 35 days · National policy / durable development

Develop fuel-cycle engineering through a funded national research programme.

Prerequisites: (sovereign_atom).

- Treasury: −$3.000 billion once; native borrowing remains available.
- CAT_nuclear_reactors: 1 × 50% research bonus; no free technology.

#### The NPT Bargain

`COLDWAR_NKO_npt_offer` · (52,4) · relative (-2,4) · 35 days · National policy / durable development

Offer non-proliferation commitments in return for civil technical cooperation.

Prerequisites: (safeguards).
Additional requirement: Historical milestone December 1985, or an earlier negotiated alternate treaty; safeguards contract valid.

- Trade opinion factor: +8%.
- Foreign influence defence: -3%.
- Offer — Civil nuclear research extension: SOV receives $2.000 billion; NKO gains nuclear power generation +8% only while safeguards remain valid. No promised Soviet reactor appears automatically. Payer: NKO, $2.000 billion on acceptance. Recipient may refuse; no reward or charge then. Offer expires after 90 days.

#### Strategic Study

`COLDWAR_NKO_strategic_option` · (56,4) · relative (2,4) · 70 days · National policy / durable development

Direct the Academy and defence establishment to study the strategic applications of nuclear research.

Prerequisites: (fuel_studies).
Additional requirement: Native nuclear programme eligibility and scientific prerequisites; this focus awards no nuclear weapon.

- Treasury: −$4.000 billion once; native borrowing remains available.
- Research speed: +3%.
- Weekly education expenditure: +6% of its native weekly baseline.
- Trade opinion factor: -8%.
- CAT_nuclear_weapons: 1 × 35% research bonus; no free technology.
- Strategic programme — Research still pays the existing GDP/c- and inflation-scaled weekly nuclear development budget. Production still needs real material and native projects.

### Korean Democratic Party

Use KDP until 1981; KSDP thereafter through a name-only update. It is not an anarchist programme despite its inherited MD slot.

#### Patriotic Charter

`COLDWAR_NKO_kdp_charter` · (4,17) · relative (0,0) · 21 days · Party programme

Give the party a governing charter grounded in civil administration and national reconciliation.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 5.

- Stability: +4%.
- Political power gain: -4%.

#### A Social Republic

`COLDWAR_NKO_kdp_social` · (2,18) · relative (-2,1) · 35 days · Party programme

Offer social protection and public investment with a larger recurrent budget.

Prerequisites: (kdp_charter).
Mutually exclusive: COLDWAR_NKO_kdp_enterprise.
Availability and guarded reward: actual ruling subparty = 5.

- Productivity growth: +6%.
- Weekly social expenditure: +10% of its native weekly baseline.
- Corporate tax revenue: -4%.

#### A Republic of Enterprise

`COLDWAR_NKO_kdp_enterprise` · (6,18) · relative (2,1) · 35 days · Party programme

Support enterprise autonomy while accepting weaker revenue and a more unequal transition.

Prerequisites: (kdp_charter).
Mutually exclusive: COLDWAR_NKO_kdp_social.
Availability and guarded reward: actual ruling subparty = 5.

- Productivity growth: +10%.
- Corporate tax revenue: -8%.
- Stability: -4%.

#### Municipal Housing

`COLDWAR_NKO_kdp_housing` · (2,19) · relative (-2,2) · 35 days · Party programme

Delegate housing budgets to municipal boards.

Prerequisites: (kdp_social).
Availability and guarded reward: actual ruling subparty = 5.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Stability: +4%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Legal Small Enterprise

`COLDWAR_NKO_kdp_licenses` · (6,19) · relative (2,2) · 35 days · Party programme

Provide legal registration and supply contracts for small enterprise.

Prerequisites: (kdp_enterprise).
Availability and guarded reward: actual ruling subparty = 5.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Civilian factory construction: +8%.
- Weekly administration expenditure: +5% of its native weekly baseline.

#### A Published Budget

`COLDWAR_NKO_kdp_budget` · (4,20) · relative (0,3) · 35 days · Party programme

Publish state accounts and reduce arbitrary fiscal intervention.

Prerequisites: (kdp_housing OR kdp_licenses).
Availability and guarded reward: actual ruling subparty = 5.

- Annual interest rate, percentage points: -0.25 percentage points.
- Political power gain: -3%.

#### Independent Civil Courts

`COLDWAR_NKO_kdp_courts` · (2,21) · relative (-2,4) · 35 days · Party programme

Make civil contracts enforceable beyond the ruling party’s immediate wishes.

Prerequisites: (kdp_budget).
Mutually exclusive: COLDWAR_NKO_kdp_executive.
Availability and guarded reward: actual ruling subparty = 5.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +5%.
- Weekly administration expenditure: +6% of its native weekly baseline.
- Political power gain: -3%.

#### Elected Executive

`COLDWAR_NKO_kdp_executive` · (6,21) · relative (2,4) · 35 days · Party programme

Prefer a decisive civilian executive to wider institutional checks.

Prerequisites: (kdp_budget).
Mutually exclusive: COLDWAR_NKO_kdp_courts.
Availability and guarded reward: actual ruling subparty = 5.

- Political power gain: +10%.
- Stability: +4%.
- Research speed: -3%.

#### Civic Associations

`COLDWAR_NKO_kdp_civic` · (2,22) · relative (-2,5) · 35 days · Party programme

Permit professional and civic organization with a budget for public order.

Prerequisites: (kdp_courts).
Availability and guarded reward: actual ruling subparty = 5.

- Research speed: +4%.
- Weekly policing expenditure: +4% of its native weekly baseline.

#### A Merit Civil Service

`COLDWAR_NKO_kdp_service` · (6,22) · relative (2,5) · 35 days · Party programme

Recruit civil servants through professional standards.

Prerequisites: (kdp_executive).
Availability and guarded reward: actual ruling subparty = 5.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Weekly administration expenditure: -4% of its native weekly baseline.
- Weekly education expenditure: +4% of its native weekly baseline.

#### Civilian Social Compact

`COLDWAR_NKO_kdp_social_compact` · (4,23) · relative (0,6) · 35 days · Party programme

Bind the civilian government to the public services it has promised.

Prerequisites: (kdp_civic OR kdp_service).
Availability and guarded reward: actual ruling subparty = 5.

- Stability: +4%.
- Weekly social expenditure: +3% of its native weekly baseline.

#### Reconciliation First

`COLDWAR_NKO_kdp_reconciliation` · (2,24) · relative (-2,7) · 35 days · Party programme

Use the party’s civilian identity to support negotiated inter-Korean relations.

Prerequisites: (kdp_social_compact).
Mutually exclusive: COLDWAR_NKO_kdp_sovereignty.
Availability and guarded reward: actual ruling subparty = 5.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Trade opinion factor: +10%.
- Army attack: -4%.
- Foreign influence defence: -3%.

#### Sovereignty First

`COLDWAR_NKO_kdp_sovereignty` · (6,24) · relative (2,7) · 35 days · Party programme

Insist on sovereign equality while preparing a more guarded diplomacy.

Prerequisites: (kdp_social_compact).
Mutually exclusive: COLDWAR_NKO_kdp_reconciliation.
Availability and guarded reward: actual ruling subparty = 5.

- Foreign influence defence: +10%.
- Army defence on core territory: +4%.
- Trade opinion factor: -6%.

#### A Durable Civil Republic

`COLDWAR_NKO_kdp_republic` · (4,25) · relative (0,8) · 35 days · Party programme

Consolidate the institutions of a civilian republic.

Prerequisites: (kdp_reconciliation OR kdp_sovereignty).
Availability and guarded reward: actual ruling subparty = 5.

- Productivity growth: +4%.
- Weekly administration expenditure: +3% of its native weekly baseline.

### Chondoist Chongu Party

Chondoism is an indigenous Korean religion and agrarian tradition, not a Muslim path or an imported theocracy.

#### Humanity Is Heaven

`COLDWAR_NKO_chondo_heaven` · (12,17) · relative (0,0) · 21 days · Party programme

Build a national programme around human dignity, rural community and Korean independence.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 7.

- Stability: +5%.
- Weekly administration expenditure: +3% of its native weekly baseline.

#### The Cooperative Village

`COLDWAR_NKO_chondo_cooperative` · (10,18) · relative (-2,1) · 35 days · Party programme

Retain common agricultural provision under stronger village institutions.

Prerequisites: (chondo_heaven).
Mutually exclusive: COLDWAR_NKO_chondo_household.
Availability and guarded reward: actual ruling subparty = 7.

- Agricultural productivity: +12%.
- Weekly administration expenditure: +8% of its native weekly baseline.
- Productivity growth: -2%.

#### The Family Holding

`COLDWAR_NKO_chondo_household` · (14,18) · relative (2,1) · 35 days · Party programme

Give households greater control of land use and a larger share of their harvest.

Prerequisites: (chondo_heaven).
Mutually exclusive: COLDWAR_NKO_chondo_cooperative.
Availability and guarded reward: actual ruling subparty = 7.

- Agricultural productivity: +15%.
- Tax revenue: -6%.
- Stability: -3%.

#### Village Granaries

`COLDWAR_NKO_chondo_granary` · (10,19) · relative (-2,2) · 35 days · Party programme

Finance local storage and guaranteed village reserves.

Prerequisites: (chondo_cooperative).
Availability and guarded reward: actual ruling subparty = 7.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Agricultural productivity: +5%.
- Weekly social expenditure: +5% of its native weekly baseline.

#### Licensed Rural Markets

`COLDWAR_NKO_chondo_markets` · (14,19) · relative (2,2) · 35 days · Party programme

Legalize local exchange with enforceable market rules.

Prerequisites: (chondo_household).
Availability and guarded reward: actual ruling subparty = 7.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +5%.
- Tax revenue: -3%.
- Weekly policing expenditure: +3% of its native weekly baseline.

#### A Rural Settlement

`COLDWAR_NKO_chondo_land` · (12,20) · relative (0,3) · 35 days · Party programme

Consolidate the chosen rural property and procurement settlement.

Prerequisites: (chondo_granary OR chondo_markets).
Availability and guarded reward: actual ruling subparty = 7.

- Agricultural productivity: +4%.

#### Freedom of Conscience

`COLDWAR_NKO_chondo_tolerance` · (10,21) · relative (-2,4) · 35 days · Party programme

Protect believers and non-believers within a common citizenship.

Prerequisites: (chondo_land).
Mutually exclusive: COLDWAR_NKO_chondo_morality.
Availability and guarded reward: actual ruling subparty = 7.

- Research speed: +5%.
- Stability: +3%.
- Political power gain: -5%.

#### A National Moral Order

`COLDWAR_NKO_chondo_morality` · (14,21) · relative (2,4) · 35 days · Party programme

Use Chondoist moral teaching to strengthen a more uniform national order.

Prerequisites: (chondo_land).
Mutually exclusive: COLDWAR_NKO_chondo_tolerance.
Availability and guarded reward: actual ruling subparty = 7.

- Stability: +8%.
- Political power gain: +5%.
- Research speed: -5%.

#### County Schools

`COLDWAR_NKO_chondo_schools` · (10,22) · relative (-2,5) · 35 days · Party programme

Expand education in neglected rural districts.

Prerequisites: (chondo_tolerance).
Availability and guarded reward: actual ruling subparty = 7.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Weekly education expenditure: +7% of its native weekly baseline.

#### Councils of Community

`COLDWAR_NKO_chondo_councils` · (14,22) · relative (2,5) · 35 days · Party programme

Place local administration in the hands of established community networks.

Prerequisites: (chondo_morality).
Availability and guarded reward: actual ruling subparty = 7.

- Weekly administration expenditure: -4% of its native weekly baseline.
- Productivity growth: -2%.

#### The Donghak Inheritance

`COLDWAR_NKO_chondo_nation` · (12,23) · relative (0,6) · 35 days · Party programme

Present Korean independence as a shared national tradition.

Prerequisites: (chondo_schools OR chondo_councils).
Availability and guarded reward: actual ruling subparty = 7.

- Foreign influence defence: +8%.
- Trade opinion factor: -3%.

#### Protect the Hillsides

`COLDWAR_NKO_chondo_reforestation` · (10,24) · relative (-2,7) · 35 days · Party programme

Protect soil and catchments by limiting further cultivation of slopes.

Prerequisites: (chondo_nation).
Mutually exclusive: COLDWAR_NKO_chondo_reclamation.
Availability and guarded reward: actual ruling subparty = 7.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Agricultural productivity: +6%.
- Agricultural district construction: -5%.

#### Reclaim New Fields

`COLDWAR_NKO_chondo_reclamation` · (14,24) · relative (2,7) · 35 days · Party programme

Finance agricultural capacity while accepting the full construction and staffing burden.

Prerequisites: (chondo_nation).
Mutually exclusive: COLDWAR_NKO_chondo_reforestation.
Availability and guarded reward: actual ruling subparty = 7.

- Treasury: −$3.750 billion once; native borrowing remains available.
- Fund 1 agriculture district level. Candidate states in priority order: 603, 1200. Full price $3.750 billion; ownership, control, free capacity, staffing, power and maintenance apply. No second building charge.

#### A Rural Commonwealth

`COLDWAR_NKO_chondo_commonwealth` · (12,25) · relative (0,8) · 35 days · Party programme

Secure the rural services and institutions promised by the party.

Prerequisites: (chondo_reforestation OR chondo_reclamation).
Availability and guarded reward: actual ruling subparty = 7.

- Stability: +4%.
- Weekly social expenditure: +4% of its native weekly baseline.

### Cabinet and Planning Commission

A cabinet government is alternate history; it is not a new political party. Preserve historical Kim Il Sung at the start.

#### Accounts before Slogans

`COLDWAR_NKO_cabinet_accounts` · (20,17) · relative (0,0) · 21 days · Party programme

Make accurate accounts the basis of cabinet authority.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 13.

- Productivity growth: +6%.
- Political power gain: -5%.

#### Plant Manager Control

`COLDWAR_NKO_cabinet_plant` · (18,18) · relative (-2,1) · 35 days · Party programme

Delegate production decisions and allow plants to retain investment funds.

Prerequisites: (cabinet_accounts).
Mutually exclusive: COLDWAR_NKO_cabinet_plan.
Availability and guarded reward: actual ruling subparty = 13.

- Production efficiency cap: +10%.
- Productivity growth: +6%.
- Corporate tax revenue: -5%.

#### National Plan

`COLDWAR_NKO_cabinet_plan` · (22,18) · relative (2,1) · 35 days · Party programme

Coordinate supplies centrally through a better funded planning apparatus.

Prerequisites: (cabinet_accounts).
Mutually exclusive: COLDWAR_NKO_cabinet_plant.
Availability and guarded reward: actual ruling subparty = 13.

- Construction speed: +10%.
- Production efficiency growth: +8%.
- Weekly administration expenditure: +10% of its native weekly baseline.

#### Supply Contracts

`COLDWAR_NKO_cabinet_contracts` · (18,19) · relative (-2,2) · 35 days · Party programme

Require suppliers and plants to honour realistic delivery contracts.

Prerequisites: (cabinet_plant).
Availability and guarded reward: actual ruling subparty = 13.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +4%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### A Statistical Service

`COLDWAR_NKO_cabinet_statistics` · (22,19) · relative (2,2) · 35 days · Party programme

Build professional statistical capacity throughout the ministries.

Prerequisites: (cabinet_plan).
Availability and guarded reward: actual ruling subparty = 13.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +4%.
- Weekly education expenditure: +4% of its native weekly baseline.

#### A Hard-Currency Budget

`COLDWAR_NKO_cabinet_currency` · (20,20) · relative (0,3) · 35 days · Party programme

Tie foreign procurement to the country’s ability to meet external bills.

Prerequisites: (cabinet_contracts OR cabinet_statistics).
Availability and guarded reward: actual ruling subparty = 13.

- Annual interest rate, percentage points: -0.25 percentage points.
- Construction speed: -3%.

#### Investment Priority

`COLDWAR_NKO_cabinet_austerity` · (18,21) · relative (-2,4) · 35 days · Party programme

Hold down current consumption to fund a higher investment share.

Prerequisites: (cabinet_currency).
Mutually exclusive: COLDWAR_NKO_cabinet_consumption.
Availability and guarded reward: actual ruling subparty = 13.

- Construction speed: +10%.
- Stability: -5%.
- Weekly social expenditure: -4% of its native weekly baseline.

#### A Consumer Recovery

`COLDWAR_NKO_cabinet_consumption` · (22,21) · relative (2,4) · 35 days · Party programme

Use increased consumption to restore confidence while slowing capital formation.

Prerequisites: (cabinet_currency).
Mutually exclusive: COLDWAR_NKO_cabinet_austerity.
Availability and guarded reward: actual ruling subparty = 13.

- Agricultural productivity: +6%.
- Stability: +6%.
- Construction speed: -6%.
- Weekly social expenditure: +6% of its native weekly baseline.

#### Train Administrators

`COLDWAR_NKO_cabinet_training` · (20,22) · relative (0,5) · 35 days · Party programme

Make professional administrative training a durable cabinet priority.

Prerequisites: (cabinet_austerity OR cabinet_consumption).
Availability and guarded reward: actual ruling subparty = 13.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Weekly education expenditure: +5% of its native weekly baseline.

#### A Governable Plan

`COLDWAR_NKO_cabinet_settlement` · (20,23) · relative (0,6) · 35 days · Party programme

Consolidate a plan that the ministries can finance and administer.

Prerequisites: (cabinet_training).
Availability and guarded reward: actual ruling subparty = 13.

- Productivity growth: +4%.
- Weekly administration expenditure: +3% of its native weekly baseline.

### Military Emergency Government

A KPA government is an emergency alternative, not historical Songun in 1970. Officers do not inherit all WPK programme bonuses.

#### The Emergency Council

`COLDWAR_NKO_kpa_council` · (28,17) · relative (0,0) · 21 days · Party programme

Place the officer corps at the centre of an emergency administration.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 22.

- Army organization: +6%.
- Political power gain: +5%.
- Stability: -5%.
- Weekly army personnel expenditure: +6% of its native weekly baseline.

#### Party Commissars

`COLDWAR_NKO_kpa_party` · (26,18) · relative (-2,1) · 35 days · Party programme

Keep party control inside the forces to stabilize an uneasy military government.

Prerequisites: (kpa_council).
Mutually exclusive: COLDWAR_NKO_kpa_professional.
Availability and guarded reward: actual ruling subparty = 22.

- Stability: +6%.
- Army organization: +4%.
- Research speed: -4%.

#### Professional Officers

`COLDWAR_NKO_kpa_professional` · (30,18) · relative (2,1) · 35 days · Party programme

Reduce party interference in command while accepting a political legitimacy problem.

Prerequisites: (kpa_council).
Mutually exclusive: COLDWAR_NKO_kpa_party.
Availability and guarded reward: actual ruling subparty = 22.

- Army organization: +8%.
- Maximum planning: +6%.
- Stability: -4%.
- Weekly army personnel expenditure: +8% of its native weekly baseline.

#### Command Compact

`COLDWAR_NKO_kpa_loyalty` · (26,19) · relative (-2,2) · 35 days · Party programme

Rebuild a compact between commanders and the ruling party apparatus.

Prerequisites: (kpa_party).
Availability and guarded reward: actual ruling subparty = 22.

- Foreign influence defence: +8%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Promotion by Merit

`COLDWAR_NKO_kpa_merit` · (30,19) · relative (2,2) · 35 days · Party programme

Select officers for technical and operational competence.

Prerequisites: (kpa_professional).
Availability and guarded reward: actual ruling subparty = 22.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Army experience gain: +8%.
- Weekly education expenditure: +4% of its native weekly baseline.

#### Military Supply

`COLDWAR_NKO_kpa_rations` · (28,20) · relative (0,3) · 35 days · Party programme

Secure military supply while diverting productive inputs from civilian provision.

Prerequisites: (kpa_loyalty OR kpa_merit).
Availability and guarded reward: actual ruling subparty = 22.

- Supply consumption: -6%.
- Agricultural productivity: -5%.
- Weekly equipment expenditure: +5% of its native weekly baseline.

#### An Entrenched Garrison

`COLDWAR_NKO_kpa_fortress` · (26,21) · relative (-2,4) · 35 days · Party programme

Accept a long military administration and its continuing civilian burden.

Prerequisites: (kpa_rations).
Mutually exclusive: COLDWAR_NKO_kpa_handover.
Availability and guarded reward: actual ruling subparty = 22.

- Army defence on core territory: +10%.
- Productivity growth: -6%.
- Weekly army personnel expenditure: +6% of its native weekly baseline.

#### Civilian Handover

`COLDWAR_NKO_kpa_handover` · (30,21) · relative (2,4) · 35 days · Party programme

Commit the emergency council to an orderly transition under an agreed civilian charter.

Prerequisites: (kpa_rations).
Mutually exclusive: COLDWAR_NKO_kpa_fortress.
Availability and guarded reward: actual ruling subparty = 22.

- Trade opinion factor: +10%.
- Stability: +5%.
- Political power gain: -6%.
- Handover commitment — Opens a political commitment through existing government change rules. A later government change disables this KPA programme.

#### Costed Defence Budget

`COLDWAR_NKO_kpa_budget` · (28,22) · relative (0,5) · 35 days · Party programme

Bring defence procurement under a budget that the treasury can sustain.

Prerequisites: (kpa_fortress OR kpa_handover).
Availability and guarded reward: actual ruling subparty = 22.

- Weekly equipment expenditure: -4% of its native weekly baseline.
- Weekly administration expenditure: +3% of its native weekly baseline.

#### Army and Republic

`COLDWAR_NKO_kpa_legacy` · (28,23) · relative (0,6) · 35 days · Party programme

Settle the role of the armed forces in the chosen political order.

Prerequisites: (kpa_budget).
Availability and guarded reward: actual ruling subparty = 22.

- Army organization: +4%.
- Weekly army personnel expenditure: +3% of its native weekly baseline.

### Yan'an Reform Communist Programme

The purged faction has no domestic organization in 1970. Only an actual government change in the existing outlook system opens this programme; no purged leader is revived.

#### Socialist Reassessment

`COLDWAR_NKO_yanan_return` · (36,17) · relative (0,0) · 21 days · Party programme

Begin a counterfactual reassessment of party rule after a fundamental political change.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 2.

- Research speed: +5%.
- Stability: -6%.

#### Factory Councils

`COLDWAR_NKO_yanan_councils` · (34,18) · relative (-2,1) · 35 days · Party programme

Give workers and technical staff a stronger voice in plant decisions.

Prerequisites: (yanan_return).
Mutually exclusive: COLDWAR_NKO_yanan_discipline.
Availability and guarded reward: actual ruling subparty = 2.

- Productivity growth: +8%.
- Political power gain: -5%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Party Discipline

`COLDWAR_NKO_yanan_discipline` · (38,18) · relative (2,1) · 35 days · Party programme

Retain centralized party command while ending the personal cult.

Prerequisites: (yanan_return).
Mutually exclusive: COLDWAR_NKO_yanan_councils.
Availability and guarded reward: actual ruling subparty = 2.

- Production efficiency growth: +8%.
- Political power gain: +6%.
- Research speed: -3%.

#### Review Sentences

`COLDWAR_NKO_yanan_rehabilitation` · (36,19) · relative (0,2) · 35 days · Party programme

Review political sentences and restore surviving specialists to professional life.

Prerequisites: (yanan_councils OR yanan_discipline).
Availability and guarded reward: actual ruling subparty = 2.

- Research speed: +4%.
- Foreign influence defence: -4%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Foreign Experts

`COLDWAR_NKO_yanan_experts` · (34,20) · relative (-2,3) · 35 days · Party programme

Accept technical assistance and the influence that accompanies it.

Prerequisites: (yanan_rehabilitation).
Mutually exclusive: COLDWAR_NKO_yanan_domestic.
Availability and guarded reward: actual ruling subparty = 2.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Research speed: +7%.
- Productivity growth: +6%.
- Foreign influence defence: -10%.

#### Domestic Expertise

`COLDWAR_NKO_yanan_domestic` · (38,20) · relative (2,3) · 35 days · Party programme

Develop expertise at home with slower returns and higher education expenditure.

Prerequisites: (yanan_rehabilitation).
Mutually exclusive: COLDWAR_NKO_yanan_experts.
Availability and guarded reward: actual ruling subparty = 2.

- Treasury: −$2.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Productivity growth: +4%.
- Weekly education expenditure: +8% of its native weekly baseline.

#### Korean Reform

`COLDWAR_NKO_yanan_socialism` · (36,21) · relative (0,4) · 35 days · Party programme

Combine socialist institutions with a less punitive economic programme.

Prerequisites: (yanan_experts OR yanan_domestic).
Availability and guarded reward: actual ruling subparty = 2.

- Agricultural productivity: +5%.
- Weekly social expenditure: +4% of its native weekly baseline.

#### Anti-Cult Guarantees

`COLDWAR_NKO_yanan_guarantees` · (36,22) · relative (0,5) · 35 days · Party programme

Limit arbitrary appointments and personal command inside the party state.

Prerequisites: (yanan_socialism).
Availability and guarded reward: actual ruling subparty = 2.

- Productivity growth: +4%.
- Political power gain: -4%.

### Industrial Labour Programme

GFTUK is a state-directed federation, not an independent opposition party in the historical start.

#### Workers’ Compact

`COLDWAR_NKO_union_compact` · (44,17) · relative (0,0) · 21 days · Party programme

Base a counterfactual government on wages, rations, safety and industrial representation.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 3.

- Stability: +5%.
- Weekly social expenditure: +4% of its native weekly baseline.

#### Wages and Supply

`COLDWAR_NKO_union_wages` · (42,18) · relative (-2,1) · 35 days · Party programme

Give workers a larger share of output at a higher social cost.

Prerequisites: (union_compact).
Mutually exclusive: COLDWAR_NKO_union_reinvestment.
Availability and guarded reward: actual ruling subparty = 3.

- Productivity growth: +6%.
- Weekly social expenditure: +10% of its native weekly baseline.
- Corporate tax revenue: -4%.

#### Workers’ Investment

`COLDWAR_NKO_union_reinvestment` · (46,18) · relative (2,1) · 35 days · Party programme

Direct retained earnings toward new investment instead of current consumption.

Prerequisites: (union_compact).
Mutually exclusive: COLDWAR_NKO_union_wages.
Availability and guarded reward: actual ruling subparty = 3.

- Civilian factory construction: +10%.
- Stability: -4%.
- Weekly administration expenditure: +6% of its native weekly baseline.

#### Industrial Safety

`COLDWAR_NKO_union_safety` · (44,19) · relative (0,2) · 35 days · Party programme

Allow inspections to slow unsafe production rather than pursuing quotas at any cost.

Prerequisites: (union_wages OR union_reinvestment).
Availability and guarded reward: actual ruling subparty = 3.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +4%.
- Factory output: -3%.
- Weekly administration expenditure: +4% of its native weekly baseline.

#### Production Bargaining

`COLDWAR_NKO_union_bargaining` · (42,20) · relative (-2,3) · 35 days · Party programme

Negotiate achievable work norms with factory representatives.

Prerequisites: (union_safety).
Mutually exclusive: COLDWAR_NKO_union_mobilization.
Availability and guarded reward: actual ruling subparty = 3.

- Productivity growth: +6%.
- Political power gain: -5%.

#### New Chollima Compact

`COLDWAR_NKO_union_mobilization` · (46,20) · relative (2,3) · 35 days · Party programme

Link accelerated output to material provision while keeping the strain of mass mobilization.

Prerequisites: (union_safety).
Mutually exclusive: COLDWAR_NKO_union_bargaining.
Availability and guarded reward: actual ruling subparty = 3.

- Factory output: +8%.
- Productivity growth: -4%.
- Weekly social expenditure: +5% of its native weekly baseline.

#### Paid Technical Training

`COLDWAR_NKO_union_training` · (44,21) · relative (0,4) · 35 days · Party programme

Train skilled workers during paid time away from production.

Prerequisites: (union_bargaining OR union_mobilization).
Availability and guarded reward: actual ruling subparty = 3.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +4%.
- Weekly education expenditure: +6% of its native weekly baseline.

#### Worker Representation

`COLDWAR_NKO_union_representation` · (44,22) · relative (0,5) · 35 days · Party programme

Give industrial representation an enduring place in the governing institutions.

Prerequisites: (union_training).
Availability and guarded reward: actual ruling subparty = 3.

- Stability: +4%.
- Weekly administration expenditure: +4% of its native weekly baseline.

### Christian Federation Programme

KCF is a supervised remnant under Kang Ryang-uk, not a mass Christian party waiting freely to contest power. No automatic conversion of the country.

#### Equal Citizenship

`COLDWAR_NKO_christian_citizenship` · (52,17) · relative (0,0) · 21 days · Party programme

Protect freedom of conscience through a counterfactual civic settlement.

Prerequisites: Section entry.
Availability and guarded reward: actual ruling subparty = 14.

- Stability: +5%.
- Political power gain: -4%.

#### Public Social Provision

`COLDWAR_NKO_christian_welfare` · (50,18) · relative (-2,1) · 35 days · Party programme

Build publicly funded welfare services with room for religious participation.

Prerequisites: (christian_citizenship).
Mutually exclusive: COLDWAR_NKO_christian_community.
Availability and guarded reward: actual ruling subparty = 14.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Productivity growth: +5%.
- Weekly healthcare expenditure: +8% of its native weekly baseline.
- Weekly social expenditure: +6% of its native weekly baseline.

#### Community Associations

`COLDWAR_NKO_christian_community` · (54,18) · relative (2,1) · 35 days · Party programme

Use local associations to provide services with less uniform coverage.

Prerequisites: (christian_citizenship).
Mutually exclusive: COLDWAR_NKO_christian_welfare.
Availability and guarded reward: actual ruling subparty = 14.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Weekly administration expenditure: -6% of its native weekly baseline.
- Stability: +5%.
- Productivity growth: -2%.

#### Schools for Citizenship

`COLDWAR_NKO_christian_education` · (52,19) · relative (0,2) · 35 days · Party programme

Provide education that protects civic equality across beliefs.

Prerequisites: (christian_welfare OR christian_community).
Availability and guarded reward: actual ruling subparty = 14.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Research speed: +5%.
- Weekly education expenditure: +7% of its native weekly baseline.

#### A Plural Civic Compact

`COLDWAR_NKO_christian_tolerance` · (50,20) · relative (-2,3) · 35 days · Party programme

Bind the government to equal citizenship for believers and non-believers.

Prerequisites: (christian_education).
Mutually exclusive: COLDWAR_NKO_christian_moral.
Availability and guarded reward: actual ruling subparty = 14.

- Research speed: +5%.
- Political power gain: -5%.

#### Christian Social Charter

`COLDWAR_NKO_christian_moral` · (54,20) · relative (2,3) · 35 days · Party programme

Make Christian social teaching a stronger public norm while retaining civil protections.

Prerequisites: (christian_education).
Mutually exclusive: COLDWAR_NKO_christian_tolerance.
Availability and guarded reward: actual ruling subparty = 14.

- Stability: +8%.
- Research speed: -4%.
- Weekly policing expenditure: +3% of its native weekly baseline.

#### Religious Contacts

`COLDWAR_NKO_christian_relations` · (52,21) · relative (0,4) · 35 days · Party programme

Support permitted family and religious contacts across the division of Korea.

Prerequisites: (christian_tolerance OR christian_moral).
Availability and guarded reward: actual ruling subparty = 14.

- Treasury: −$1.000 billion once; native borrowing remains available.
- Trade opinion factor: +8%.
- Weekly policing expenditure: +4% of its native weekly baseline.

#### Civic Commonwealth

`COLDWAR_NKO_christian_republic` · (52,22) · relative (0,5) · 35 days · Party programme

Consolidate a civic order without granting any faith ownership of the state.

Prerequisites: (christian_relations).
Availability and guarded reward: actual ruling subparty = 14.

- Productivity growth: +4%.
- Weekly social expenditure: +4% of its native weekly baseline.

## Evidence and remaining validation

See [MD layout reference](md_layout_reference.md), [mechanics trace](mechanics_reference.md) and [historical research](history_research.md). Full design source: `COLDWAR_NKO_1970_design.json`. Preview uses the same resolved coordinates, title strings and dependency groups; genuine local MD art is embedded. Browser typography and connector routing approximate HOI4, and the overview is reduced in scale. Select a section for readable artwork and inspect exact rewards.

Concept validation covers IDs, references, AND/OR histories and full item bounds. It does not establish engine tooltips, save/load timing, balance in a real multiplayer campaign, native branch visibility refresh or nuclear programme availability. These remain implementation/engine checks after approval.

No loaded national focus, history, idea, localization, event, GUI or economic file has been edited. Approval is requested for this concrete design, not for claimed completed implementation.
