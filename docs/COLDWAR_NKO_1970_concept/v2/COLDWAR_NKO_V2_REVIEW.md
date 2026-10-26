# COLDWAR — DPRK concept, revision 2

**189 focuses. Design and preview only; no loaded game files changed.**

## Revision requested

- Every cash price is a GDP share. Normal project prices range from 0.20% to 2.00% of the payer’s current internal GDP; agreements quote each payer separately. The user’s GDP pricing instruction supersedes the earlier fixed-dollar preference.
- Artillery and comparable specialist programmes use the actual relevant MD combat modifiers. Towed/self-propelled artillery use `army_artillery_attack_factor`; rocket artillery uses its separately registered battalion key. No artillery programme grants a general army attack bonus.
- Every building level, including infrastructure, energy and radar, grants one additional shared building slot in the same selected state. Slots and the building are a single one-time reward. Check ownership/control, coastline and hard type/level caps before charging; missing existing shared slots are supplied by this reward.
- Foreign Diplomacy adds five new country programmes (East Germany, Bulgaria, Romania, Egypt and Japan), alongside four base packages in the patron, Korean and atomic sections: nine base agreements with eight partner countries in total. All bilateral offer focuses create acceptance and refusal decisions for the recipient country; an information event may notify but never accepts the agreement.
- Accepted agreements grant both countries persistent contract spirits with reciprocal benefits and burdens; the Inter-Korean package is symmetric. They do not expire or depend on a domestic governing party. All four direct sanction classes in either direction or mutual war suspend BOTH spirits and their weekly contract costs. Both resume when those conditions clear, without replaying buildings, cash or research grants.
- The Korean policy fork now offers negotiated exchange, coercive pressure and armed reunification. The final military focus grants a war goal against KOR. It does not automatically declare war, annex territory, or involve other players.
- Kim Il Sung dies on 8 July 1994 and one major global news event is broadcast. Kim Jong Il succeeds only the incumbent Kim regime, as explicitly confirmed by the user. Other governments remain. Existing leader expiry and the succession event share one receipt to avoid an empty leader slot or duplicate transfer.
- English focus descriptions follow native MD’s short narrative style. Prices, requirements and effects are separate tooltip lines. Internal flags, state-routing and implementation notes are excluded from ordinary player text.

## GDP accounting

{
  "one_off": "Current payer gdp_total \u00d7 chosen share; no fixed-dollar floor.",
  "quote": "Save both countries\u2019 GDP-based setup quotes when the offer is sent; charge exactly those saved amounts only on recipient acceptance.",
  "weekly": "Current payer GDP \u00d7 annual commitment \u00f7 52. Aggregate once in the native weekly expense system only while the paired agreement is active.",
  "borrowing": "Normal MD weekly automatic borrowing remains available; no added current-cash gate.",
  "slots": "Every building level grants the same number of extra shared slots in the same owned and controlled state; enforce non-slot caps and placement rules."
}

The saved machinery loan principal is `GDP × 0.015` at completion. Book principal and cash proceeds once, then spend that same quote on the factory. Later repayment uses the saved outstanding cash amount, not a newly calculated GDP fraction. Rescheduling charges 0.20% of then-current GDP. Fees use fractions with at most five fractional digits and a separate divide-by-52 operation, never a long weekly literal.

## Exact spatial plan

| Section | Root | Focuses |
|---|---:|---:|
| Workers' Party of Korea | (6,0) | 24 |
| Planning, Power and Living Standards | (16,0) | 25 |
| The Korean People's Army | (30,0) | 20 |
| Patrons and the Korean Question | (44,0) | 24 |
| Science and the Atomic Question | (54,0) | 8 |
| Korean Democratic Party | (4,17) | 14 |
| Chondoist Chongu Party | (12,17) | 14 |
| Cabinet and Planning Commission | (20,17) | 10 |
| Military Emergency Government | (28,17) | 10 |
| Yan'an Reform Communist Programme | (36,17) | 8 |
| Industrial Labour Programme | (44,17) | 8 |
| Christian Federation Programme | (52,17) | 8 |
| Foreign Diplomacy | (68,0) | 12 |
| Kim Jong Il’s Leadership | (64,17) | 4 |

Initial camera: WPK (6,0). Continuous focuses: reserved at (7300,3750) px beyond the full tree; engine position remains to be checked. All graph data and previews share the same resolved coordinates and grouped prerequisites.

## Recipient decision and paired spirits

On offer, save both countries’ GDP quotes and a pending receipt on both tags for 90 days. The foreign player receives **Accept the Agreement** and **Decline the Proposal** decisions. Acceptance rechecks peace, all four sanction arrays, existence, prerequisites and any project cap, then clears pending state, pays the saved setup amounts, records a durable receipt in both countries and grants both spirits. Refusal/expiry makes no charge. Upgrade offers use the same recipient process and replace/extend the existing package rather than stacking duplicate base modifiers.

The same active predicate is evaluated at both endpoints: both signed receipts, both countries exist, no mutual war, no diplomatic/financial/economic/military sanctions from NKO to partner and no such sanctions from partner to NKO. Call bilateral reconciliation on acceptance, war/peace and sanctions add/remove, plus monthly/save-load backstops. An `enable` block alone is not assumed to reattach an engine-removed modifier.

After refusal or expiry, the sending country may resubmit through a decision unlocked by the completed offer focus. A fresh 90-day offer receives fresh quotes; no reapplication of completed-focus rewards. Pending offers are unique per agreement and stage. An accepted base or upgrade cannot be purchased twice.

## Starting national spirits

### The Monolithic Ideological System

The purges have secured the Leader’s command while suppressing independent reporting and technical disagreement.

- Political Power Gain: +10%
- Stability: +6%
- Research Speed: -5%
- Bureaucracy Cost Multiplier: +8%

Replaced by Monolithic Leadership or Collective Deliberation. Earned WPK policies apply while the WPK governs and return with that government.

### Economic and Defence Construction

The parallel build-up strengthens deterrence while defence absorbs labour, capital and public expenditure.

- Army defence on core territory: +8%
- Military factory construction: +8%
- Civilian factory construction: -10%
- Army Cost Multiplier: +10%

Army reorganization reduces this to a residual +4% core defence / -4% civilian construction burden; final national arsenal/civilian conversion choice replaces the residual.

### The Extended Seven-Year Plan

A developed industrial base is constrained by missed targets, weak input balances and repeated plan extensions.

- Monthly Productivity Growth: -12%
- Production Efficiency growth: -10%
- Bureaucracy Cost Multiplier: +8%

Balance the Inputs removes this spirit after one substantive industrial priority and a funded project.

### Power and Imported Inputs

Power shortages and imported machinery and fuel limit the use of installed industrial capacity.

- Factory output: -8%
- All Sources of Power Use Multiplier: +8%
- Population Fuel Consumption Factor: +6%

Repair the Power Grid removes the electricity/output component. Residual imported-input fuel burden remains until external resilience.

### An Uneven Civilian Supply

Civilian supply competes with heavy industry and defence; rural inputs and urban distribution remain uneven.

- Agricultural District Productivity: -8%
- Stability: -4%
- Social Spending Cost Multiplier: +6%

A Sustainable Ration removes this after both irrigation/fertilizer and county clinics. This is not the 1990s famine.

### Juche and the Two Patrons

Political autonomy is defended through cautious access to foreign technology and competition between external patrons.

- Foreign Influence Defense Multiplier: +12%
- Trade deal opinion factor: -8%
- Research Speed: -3%

External Channels replaces this with strategic autonomy: +6% influence defense / −3% trade opinion. Signed cooperation provides additional technical benefits.

## Guarded 1970 initialization

{
  "status": "Implementation after approval only.",
  "scenario": "Attach this tree and the six defined opening spirit packages in the guarded 1970 NKO startup. Existing 2000 add_ideas are not the 1970 starting package.",
  "guards": "original_tag = NKO; IMP_is_1970_scenario = yes; existing governing-party variable. The monolithic starting policy is WPK-bound; the other five opening constraints are national.",
  "reconciliation": "A one-time initialization receipt plus earned replacement receipts prevents duplicate startup or restoration of a removed opening constraint. Reconcile on load without rerunning buildings, cash or research grants.",
  "scope": "No starting OOB, troops, ships, aircraft, uranium production or built uranium mines are added."
}

## Policy lifecycle

{
  "party": "Earned policies apply only under their registered governing party or institution; reconcile on government change, monthly maintenance and load. Return earned spirits without repeating one-time rewards.",
  "leader": "Kim-family and Kim Jong Il policies also require their respective leader conditions. Kim Jong Il succession on 8 July 1994 replaces only the incumbent Kim regime.",
  "treaties": "Signed bilateral agreements survive government changes. Suspend both copies and weekly fees together during mutual war or bilateral sanctions; resume without repeating setup grants.",
  "resubmission": "Completed offer focuses unlock sender decisions to resubmit after refusal or expiry, with fresh quotes and a new 90-day response period. Only one offer per agreement/stage may be pending."
}

## Conditional credit and supply incidents

[
  {
    "id": "COLDWAR_NKO_machinery_account",
    "name": "The Machinery Account",
    "trigger": "730 days after the saved 1.50%-of-GDP machinery loan, if recorded principal remains.",
    "choices": [
      {
        "name": "Settle the Account",
        "payment": "Recorded outstanding principal, paid once; matched debt reduction."
      },
      {
        "name": "Reschedule the Account",
        "cost_gdp_share": 0.002,
        "days": 730,
        "modifiers": {
          "interest_rate_multiplier_modifier": 1.0,
          "trade_opinion_factor": -0.1
        }
      },
      {
        "name": "Suspend Repayments",
        "cost_gdp_share": 0,
        "days": 730,
        "modifiers": {
          "interest_rate_multiplier_modifier": 2.0,
          "trade_opinion_factor": -0.15,
          "stability_factor": -0.03
        }
      }
    ]
  },
  {
    "id": "COLDWAR_NKO_patron_disruption",
    "name": "External Support Disrupted",
    "trigger": "A real accepted supply agreement becomes inactive through war, bilateral sanctions, or the loss of its partner.",
    "agreement_keys": [
      "soviet_industry",
      "china_border"
    ],
    "transition": "Active to inactive only. One non-stacking adjustment penalty; monthly maintenance never retriggers it.",
    "days": 365,
    "modifiers": {
      "industrial_capacity_factory": -0.08,
      "research_speed_factor": -0.03
    },
    "mitigation_cost_gdp_share": 0.004,
    "note": "The agreement itself does not expire. Both spirits and ongoing agreement fees suspend together; restoration never repeats one-time grants."
  }
]

## Agreement catalogue

### Industrial Cooperation Protocol — Soviet Union

Pyongyang proposes a programme of machinery deliveries, power engineering and technical training under the existing treaty relationship.

**North Korea**

- Setup: 1.00% of own quoted GDP
- Weekly cost: current GDP × 0.00150 ÷ 52
- Monthly Productivity Growth: +6%
- Production Efficiency Cap: +6%
- Fossil Power Generation: +8%
- Foreign Influence Defense Multiplier: -4%

**Soviet Union**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00020 ÷ 52
- Corporate Tax Revenue Multiplier: +1.5%
- Foreign Influence Multiplier: +5%
- Education Cost Multiplier: +2%

- On first acceptance: 1 Civilian Factory and 1 building slot in the same NKO state (Pyongyang, North Pyongan).
- Recipient-approved upgrade: Technical Placements; added NKO effects {"research_speed_factor": 0.03}; added partner effects {"research_speed_factor": 0.01}. Base effects are included once, not duplicated.

Historical precedent: 1961 Soviet–DPRK treaty, articles 3–6. https://treaties.un.org/doc/Publication/UNTS/Volume%20420/volume-420-I-6045-English.pdf

### Border Cooperation Protocol — China

Pyongyang proposes regular agricultural exchange and border supply arrangements as relations with Beijing recover.

**North Korea**

- Setup: 0.15% of own quoted GDP
- Weekly cost: current GDP × 0.00100 ÷ 52
- Agricultural District Productivity: +8%
- Supply Consumption: -4%
- Foreign Influence Defense Multiplier: -3%
- Tax Revenue Multiplier: -2%

**China**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00030 ÷ 52
- Tax Revenue Multiplier: +1%
- Trade deal opinion factor: +5%
- Bureaucracy Cost Multiplier: +1.5%

- Recipient-approved upgrade: Border Logistics; added NKO effects {"agricolture_productivity_modifier": 0.02, "supply_consumption_factor": -0.02}; added partner effects {"trade_opinion_factor": 0.02}. Base effects are included once, not duplicated.

Historical precedent: 1961 PRC–DPRK treaty; 1970 rapprochement. https://worldjpn.net/documents/texts/docs/19610711.T1E.html

### Inter-Korean Exchange Agreement — South Korea

Pyongyang proposes a permanent channel for family contacts, communications and peaceful exchange under the principles of the July Joint Statement.

**North Korea**

- Setup: 0.10% of own quoted GDP
- Weekly cost: current GDP × 0.00050 ÷ 52
- Stability: +4%
- Trade deal opinion factor: +10%
- Army attack: -3%
- Bureaucracy Cost Multiplier: +2%

**South Korea**

- Setup: 0.10% of own quoted GDP
- Weekly cost: current GDP × 0.00050 ÷ 52
- Stability: +4%
- Trade deal opinion factor: +10%
- Army attack: -3%
- Bureaucracy Cost Multiplier: +2%

- Recipient-approved upgrade: Inter-Korean Consultative Council; added NKO effects {"productivity_growth_modifier": 0.03, "trade_opinion_factor": 0.04, "bureaucracy_cost_multiplier_modifier": 0.02}; added partner effects {"productivity_growth_modifier": 0.03, "trade_opinion_factor": 0.04, "bureaucracy_cost_multiplier_modifier": 0.02}. Base effects are included once, not duplicated.

Historical precedent: 1972 joint statement; this permanent compact is an alternate agreement. https://history.state.gov/historicaldocuments/frus1969-76v19p1/d151

### Civil Atomic Cooperation — Soviet Union

Pyongyang proposes research and reactor-engineering cooperation under agreed safeguards.

**North Korea**

- Setup: 0.50% of own quoted GDP
- Weekly cost: current GDP × 0.00050 ÷ 52
- Research Speed: +4%
- Foreign Influence Defense Multiplier: -3%
- Education Cost Multiplier: +2%

**Soviet Union**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00010 ÷ 52
- Research Speed: +1%
- Foreign Influence Multiplier: +3%
- Education Cost Multiplier: +2%

- Recipient-approved upgrade: Civil Nuclear Power Protocol; added NKO effects {"nuclear_energy_generation_modifier": 0.08, "bureaucracy_cost_multiplier_modifier": 0.025}; added partner effects {"foreign_influence_modifier": 0.02, "bureaucracy_cost_multiplier_modifier": 0.015}. Base effects are included once, not duplicated.

Historical precedent: Soviet reactor cooperation and the 1985 NPT bargain. https://www.iaea.org/sites/default/files/dprk.pdf

### Machinery and Materials Protocol — East Germany

Pyongyang proposes East German machinery and specialist training in exchange for reliable industrial deliveries.

**North Korea**

- Setup: 0.20% of own quoted GDP
- Weekly cost: current GDP × 0.00120 ÷ 52
- Production Efficiency growth: +8%
- Monthly Productivity Growth: +5%
- resource_export_multiplier_modifier: -3%

**East Germany**

- Setup: 0.03% of own quoted GDP
- Weekly cost: current GDP × 0.00020 ÷ 52
- Factory output: +3%
- Corporate Tax Revenue Multiplier: +2%
- Education Cost Multiplier: +3%

- Recipient-approved upgrade: Machine-Tool Standards; added NKO effects {"production_factory_max_efficiency_factor": 0.04}; added partner effects {"research_speed_factor": 0.015}. Base effects are included once, not duplicated.

Historical precedent: 1977 GDR–DPRK agreement for economic, scientific and technical cooperation. https://www.wilsoncenter.org/sites/default/files/media/documents/publication/CWIHP_Bulletin_14-15.pdf

### Engineering Cooperation Agreement — Bulgaria

Pyongyang proposes joint work on milling, communications and agricultural engineering, with deliveries linked to agreed project schedules.

**North Korea**

- Setup: 0.12% of own quoted GDP
- Weekly cost: current GDP × 0.00080 ÷ 52
- Agricultural District Productivity: +6%
- Research Speed: +2.5%
- Bureaucracy Cost Multiplier: +3%

**Bulgaria**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00010 ÷ 52
- Corporate Tax Revenue Multiplier: +1.5%
- Research Speed: +1%
- Education Cost Multiplier: +2%

- Recipient-approved upgrade: Agricultural Laboratories; added NKO effects {"agricolture_productivity_modifier": 0.04}; added partner effects {"agricolture_productivity_modifier": 0.02}. Base effects are included once, not duplicated.

Historical precedent: 1972 Bulgarian credit and later engineering/agrobiology programmes. https://www.wilsoncenter.org/publication/korea-the-bulgarian-archives-1945-1995-introduction

### Industrial Exchange Agreement — Romania

Pyongyang proposes a modest programme of industrial and agricultural exchange to diversify its socialist trading partners.

**North Korea**

- Setup: 0.10% of own quoted GDP
- Weekly cost: current GDP × 0.00060 ÷ 52
- Monthly Productivity Growth: +4%
- Trade deal opinion factor: +5%
- Bureaucracy Cost Multiplier: +2.5%

**Romania**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00015 ÷ 52
- Corporate Tax Revenue Multiplier: +1%
- Trade deal opinion factor: +4%
- Bureaucracy Cost Multiplier: +2%

- Recipient-approved upgrade: Reciprocal Trade Schedules; added NKO effects {"trade_opinion_factor": 0.04}; added partner effects {"trade_opinion_factor": 0.03}. Base effects are included once, not duplicated.

Historical precedent: 1970s Romanian–DPRK trade diversification; conservative abstraction. https://www.wilsoncenter.org/publication/korea-the-bulgarian-archives-1945-1995-introduction

### Scientific and Technical Accord — Egypt

Pyongyang proposes scientific exchange, technical placements and maintenance training under the bilateral cooperation framework.

**North Korea**

- Setup: 0.10% of own quoted GDP
- Weekly cost: current GDP × 0.00050 ÷ 52
- Research Speed: +2.5%
- Army experience gain: +4%
- Army Cost Multiplier: +3%

**Egypt**

- Setup: 0.03% of own quoted GDP
- Weekly cost: current GDP × 0.00030 ÷ 52
- Research Speed: +2.5%
- Equipment Cost Multiplier: -3%
- Education Cost Multiplier: +3%

- Recipient-approved upgrade: Technical Missions; added NKO effects {"experience_gain_army": 0.04}; added partner effects {"equipment_cost_multiplier_modifier": -0.02}. Base effects are included once, not duplicated.

Historical precedent: 1969 scientific agreement and 1983 Egyptian–DPRK cooperation accord. https://sis.gov.eg/en/international-relations/bilateral-relations/north-korea/

### Fisheries and Commerce Protocol — Japan

Pyongyang proposes government authorization for a limited fisheries and commercial arrangement without diplomatic recognition.

**North Korea**

- Setup: 0.10% of own quoted GDP
- Weekly cost: current GDP × 0.00030 ÷ 52
- Agricultural District Productivity: +4%
- Corporate Tax Revenue Multiplier: +1%
- Police Cost Multiplier: +2%

**Japan**

- Setup: 0.02% of own quoted GDP
- Weekly cost: current GDP × 0.00010 ÷ 52
- Agricultural District Productivity: +2%
- Trade deal opinion factor: +3%
- Bureaucracy Cost Multiplier: +1%

- Recipient-approved upgrade: Commercial Port Access; added NKO effects {"productivity_growth_modifier": 0.025, "police_cost_multiplier_modifier": 0.01}; added partner effects {"corporate_tax_income_multiplier_modifier": 0.005, "bureaucracy_cost_multiplier_modifier": 0.01}. Base effects are included once, not duplicated.

Historical precedent: Private fisheries arrangements reported in Japan’s 1980 Bluebook; a new state-approved protocol is alternate history. https://www.mofa.go.jp/mofaj/gaiko/bluebook/1980/s55-2010101-3.htm

## Global death event and succession

{
  "date": "8 July 1994",
  "id": "COLDWAR_NKO_world_news_kim_il_sung_dies",
  "title": "Kim Il Sung Has Died",
  "description": "Pyongyang has announced the death of Kim Il Sung at the age of 82. Kim Jong Il has assumed the leadership of North Korea, ending the founder’s forty-six years in power.",
  "alternative_description": "Kim Il Sung, North Korea’s former leader, has died at the age of 82. His death closes the era of the Republic’s founding generation.",
  "option": "The end of an era.",
  "broadcast": "One global major news event, visible to all countries.",
  "succession": "Install Kim Jong Il only if the incumbent Kim regime was in office immediately before the death. Alternative governments remain in office.",
  "succession_guard": "Record incumbent Kim Il Sung before his existing 1994.7.8 leader expiry; a one-time global receipt prevents duplicate death / succession events.",
  "formal_titles": "National leader from July 1994; not automatically President or WPK General Secretary in 1994.",
  "native_leader_name": "Kim Jong-il",
  "native_portrait": "gfx/Leaders/NKO/Kim_Jong_il.dds",
  "native_ideology": "communist_state",
  "availability_receipt": {
    "id": "COLDWAR_NKO_kim_jong_il_unavailable",
    "status": "Proposed country lifecycle receipt, not an existing MD API.",
    "producer": "Normally absent in the historical 1970–1994 course. Explicit RP mortality or permanent retirement of the successor must set it; family promotion and succession recheck it."
  },
  "image": "assets/COLDWAR_NKO_1994_funeral_colorized.png",
  "source_image": "assets/kim_il_sung_funeral_1994_source.jpg",
  "image_credit": "KCNA / Korea News Service via Associated Press; July 1994 funeral procession. AI color restoration for concept review.",
  "image_source": "https://www.dailyherald.com/20111226/news/what-to-look-for-at-north-koreas-funeral-for-kim-jong-il/"
}

The illustrative source photograph depicts the funeral procession later in July 1994, not the moment of death. The source caption identifies KCNA / Korea News Service via AP. The color treatment is an AI restoration; retain source and prompt provenance. No open-license claim is made for the press photograph.

## Focus catalogue

### Workers' Party of Korea

#### The Fifth Congress

`COLDWAR_NKO_fifth_congress` · (6,0) · 21 days

Set the programme of the party congress after the extended Seven-Year Plan.

- Political Power Gain: +5%
- Bureaucracy Cost Multiplier: +3%
- Open the National Investment Programme

#### Monolithic Leadership

`COLDWAR_NKO_monolithic` · (4,1) · 35 days

Concentrate authority in the Leader and his trusted cadre network.

Requires: (The Fifth Congress).
Excludes: Collective Deliberation.
- Political Power Gain: +16%
- Stability: +8%
- Research Speed: -6%
- Bureaucracy Cost Multiplier: +10%
- Remove The Monolithic Ideological System

#### Collective Deliberation

`COLDWAR_NKO_collective` · (8,1) · 35 days

Restore policy debate within the Workers’ Party while accepting a less unified command.

Requires: (The Fifth Congress).
Excludes: Monolithic Leadership.
- Research Speed: +7%
- Monthly Productivity Growth: +6%
- Stability: -6%
- Bureaucracy Cost Multiplier: +8%
- Remove The Monolithic Ideological System

#### Loyal Appointments

`COLDWAR_NKO_loyalty` · (4,2) · 35 days

Promote politically reliable officials, narrowing the pool of technical talent.

Requires: (Monolithic Leadership).
- Foreign Influence Defense Multiplier: +10%
- Monthly Productivity Growth: -3%

#### Candid Reports

`COLDWAR_NKO_debate` · (8,2) · 35 days

Let ministries report missed targets without treating every failure as disloyalty.

Requires: (Collective Deliberation).
- Monthly Productivity Growth: +5%
- Political Power Gain: -5%

#### The Presidential State

`COLDWAR_NKO_presidency` · (4,3) · 35 days

Gather constitutional and administrative authority around Kim Il Sung.

Requires: (Loyal Appointments).
- Political Power Gain: +6%
- Police Cost Multiplier: +5%

#### Cabinet Accountability

`COLDWAR_NKO_cabinet_reports` · (8,3) · 35 days

Require ministers to defend plans and expenditure before a collective party leadership.

Requires: (Candid Reports).
- Bureaucracy Cost Multiplier: -6%
- Political Power Gain: -3%

#### The Ten Principles

`COLDWAR_NKO_ten_principles` · (4,4) · 35 days

Bind institutions to a uniform ideological hierarchy.

Requires: (The Presidential State).
- Stability: +4%
- Research Speed: -2%

#### Professional Cadres

`COLDWAR_NKO_cadre_tenure` · (8,4) · 35 days

Protect experienced administrators while accepting a more entrenched bureaucracy.

Requires: (Cabinet Accountability).
- Research Speed: +4%
- Bureaucracy Cost Multiplier: +4%

#### The Party Settlement

`COLDWAR_NKO_party_settlement` · (6,5) · 35 days

Consolidate the institutional settlement chosen by the congress.

Requires: (The Ten Principles OR Professional Cadres).
- Foreign Influence Defense Multiplier: +6%

#### Campaign Mobilization

`COLDWAR_NKO_campaigns` · (4,6) · 35 days

Concentrate labour on visible projects at the expense of routine production and household provision.

Requires: (The Party Settlement).
Excludes: Technical Cadres.
- Construction Speed: +10%
- Monthly Productivity Growth: -4%
- Social Spending Cost Multiplier: +4%

#### Technical Cadres

`COLDWAR_NKO_technical_cadres` · (8,6) · 35 days

Replace emergency campaigns with trained supervision and measured investment.

Requires: (The Party Settlement).
Excludes: Campaign Mobilization.
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +8%
- Construction Speed: -5%
- Education Cost Multiplier: +8%

#### Three Revolutions

`COLDWAR_NKO_three_revolutions` · (4,7) · 35 days

Send ideological, technical and cultural teams into workplaces.

Requires: (Campaign Mobilization).
- Production Efficiency growth: +8%
- Bureaucracy Cost Multiplier: +6%

#### Ministry Engineers

`COLDWAR_NKO_engineer_commissions` · (8,7) · 35 days

Give technical commissions the authority to revise unrealistic orders.

Requires: (Technical Cadres).
- Production Efficiency Cap: +6%
- Bureaucracy Cost Multiplier: +4%

#### Red Banner Campaign

`COLDWAR_NKO_red_banner` · (4,8) · 35 days

Reward accelerated production and model work teams while placing further pressure on inputs.

Requires: (Three Revolutions).
- Factory output: +6%
- All Sources of Power Use Multiplier: +5%
- Stability: -2%

#### Achievable Targets

`COLDWAR_NKO_honest_targets` · (8,8) · 35 days

Accept less spectacular headlines in return for plans that plants can deliver.

Requires: (Ministry Engineers).
- Monthly Productivity Growth: +5%
- Political Power Gain: -4%

#### Discipline in the Plan

`COLDWAR_NKO_plan_discipline` · (6,9) · 35 days

Carry the chosen management settlement into the next planning period.

Requires: (Red Banner Campaign OR Achievable Targets).
- Production Efficiency growth: +4%

#### Cultivate the Centre

`COLDWAR_NKO_family_succession` · (4,10) · 35 days

Build Kim Jong Il’s authority inside the party without displacing Kim Il Sung.

Requires: (Discipline in the Plan).
Excludes: Collective Oversight.
- Political Power Gain: +8%
- Bureaucracy Cost Multiplier: +6%
- Research Speed: -2%

#### Collective Oversight

`COLDWAR_NKO_committee_succession` · (8,10) · 35 days

A stronger secretariat can restrain personal appointments and give the cabinet a larger role in governing the state.

Requires: (Discipline in the Plan).
Excludes: Cultivate the Centre.
- Research Speed: +5%
- Monthly Productivity Growth: +4%
- Stability: -6%

#### The Party and the Arts

`COLDWAR_NKO_party_media` · (4,11) · 35 days

Finance a cultural apparatus that presents the successor as the guardian of continuity.

Requires: (Cultivate the Centre).
- Stability: +5%
- Social Spending Cost Multiplier: +5%

#### Responsible Secretariat

`COLDWAR_NKO_secretariat` · (8,11) · 35 days

Distribute appointments among a responsible secretariat rather than the ruling household.

Requires: (Collective Oversight).
- Bureaucracy Cost Multiplier: -5%
- Political Power Gain: -3%

#### The Sixth Congress

`COLDWAR_NKO_sixth_congress` · (4,12) · 35 days

Publicly confirm the successor’s party offices while the founding Leader remains in command.

Requires: (The Party and the Arts).
- Foreign Influence Defense Multiplier: +8%
- Research Speed: -2%

#### Cabinet Continuity

`COLDWAR_NKO_succession_rules` · (8,12) · 35 days

Preserve the cabinet’s authority through the next leadership transition without abandoning the party’s governing institutions.

Requires: (Responsible Secretariat).
- Stability: +4%
- Bureaucracy Cost Multiplier: +3%

#### Beyond the Founder

`COLDWAR_NKO_continuity` · (6,13) · 35 days

Secure continuity through the leadership settlement the country has chosen.

Requires: (The Sixth Congress OR Cabinet Continuity).
- Monthly Productivity Growth: +4%
- Bureaucracy Cost Multiplier: +3%

### Planning, Power and Living Standards

#### Extended Plan Review

`COLDWAR_NKO_plan_review` · (16,0) · 21 days

Audit the gap between targets, installed capacity and available supplies.

- Production Efficiency growth: +4%

#### Heavy Industry First

`COLDWAR_NKO_heavy_priority` · (12,1) · 35 days

Prioritize metals and machinery while scarce capital is withheld from agriculture and household output.

Requires: (Extended Plan Review).
Excludes: Food and Light Industry, Industrial Growth.
- Expenditure: 0.40% of GDP
- Military factory construction: +12%
- Production Efficiency Cap: +8%
- Agricultural District Productivity: -6%
- All Sources of Power Use Multiplier: +8%

#### Food and Light Industry

`COLDWAR_NKO_light_priority` · (16,1) · 35 days

Direct investment toward everyday supply at a cost to the defence-industrial build-up.

Requires: (Extended Plan Review).
Excludes: Heavy Industry First, Industrial Growth.
- Expenditure: 0.40% of GDP
- Agricultural District Productivity: +12%
- Civilian factory construction: +10%
- Military factory construction: -8%
- Social Spending Cost Multiplier: +5%

#### Industrial Growth

`COLDWAR_NKO_balanced_priority` · (20,1) · 35 days

Adopt a slower investment plan with more reliable input balances.

Requires: (Extended Plan Review).
Excludes: Heavy Industry First, Food and Light Industry.
- Expenditure: 0.40% of GDP
- Monthly Productivity Growth: +8%
- Production Efficiency growth: +6%
- Construction Speed: -4%
- Bureaucracy Cost Multiplier: +5%

#### Modernize Steelworks

`COLDWAR_NKO_steelworks` · (12,2) · 35 days

Refit the established steel and engineering complexes that support national industrialization.

Requires: (Heavy Industry First).
- Expenditure: 1.50% of GDP
- Add 1 Military Factory and 1 Building Slot in Pyongyang or Hamgyong

#### Equip the Cooperatives

`COLDWAR_NKO_food_district` · (16,2) · 35 days

Equip the cooperatives with machinery and storage, and stabilize the delivery of rural inputs.

Requires: (Food and Light Industry).
- Expenditure: 1.00% of GDP
- Add 1 Agricultural District and 1 Building Slot in Hwanghae or Pyongyang

#### Machine Tool Standards

`COLDWAR_NKO_machine_tools` · (20,2) · 35 days

Improve interchangeability and maintenance rather than chasing gross output totals.

Requires: (Industrial Growth).
- Expenditure: 0.40% of GDP
- Production Efficiency Cap: +6%
- Education Cost Multiplier: +4%

#### Balance the Inputs

`COLDWAR_NKO_input_balance` · (16,3) · 35 days

Bring transport, electricity and intermediate supplies into the investment plan.

Requires: (Modernize Steelworks OR Equip the Cooperatives OR Machine Tool Standards).
- Monthly Productivity Growth: +4%
- Remove The Extended Seven-Year Plan

#### Coal-fired Expansion

`COLDWAR_NKO_coal_power` · (14,4) · 49 days

Expand coal-fired generating capacity to sustain the industrial plan.

Requires: (Balance the Inputs).
Excludes: Hydropower Plan.
- Expenditure: 1.00% of GDP
- Add 1 Fossil Power Plant and 1 Building Slot in Pyongyang or Hamgyong

#### Hydropower Plan

`COLDWAR_NKO_hydro_power` · (18,4) · 49 days

Invest in inland water power to reduce dependence on imported fossil fuels.

Requires: (Balance the Inputs).
Excludes: Coal-fired Expansion.
- Expenditure: 2.00% of GDP
- Add 1 Renewable Energy Infrastructure and 1 Building Slot in Chagang or Kangwon

#### Repair the Power Grid

`COLDWAR_NKO_power_grid` · (16,5) · 35 days

Reduce transmission losses through paid grid maintenance.

Requires: (Coal-fired Expansion OR Hydropower Plan).
- Expenditure: 0.40% of GDP
- All Sources of Power Use Multiplier: -8%
- Replace Power and Imported Inputs: Population Non-Electric Fuel Demand +6%
- Remove Power and Imported Inputs

#### Industrial Rail Corridor

`COLDWAR_NKO_rail_corridor` · (14,6) · 35 days

Increase infrastructure along an owned industrial corridor.

Requires: (Repair the Power Grid).
- Expenditure: 0.75% of GDP
- Add 1 Infrastructure and 1 Building Slot in Pyongyang or North Pyongan or Hamgyong

#### Housing near the Plants

`COLDWAR_NKO_housing` · (18,6) · 35 days

Fund housing and urban services so industrial recruitment can be sustained.

Requires: (Repair the Power Grid).
- Expenditure: 0.40% of GDP
- Stability: +4%
- Social Spending Cost Multiplier: +6%

#### Fertilizer and Irrigation

`COLDWAR_NKO_fertilizer` · (14,7) · 35 days

Improve yields through inputs that require electricity and dependable distribution.

Requires: (Industrial Rail Corridor).
- Expenditure: 0.40% of GDP
- Agricultural District Productivity: +8%
- All Sources of Power Use Multiplier: +4%

#### County Clinics

`COLDWAR_NKO_public_health` · (18,7) · 35 days

Expand basic healthcare at a continuing public cost.

Requires: (Housing near the Plants).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +4%
- Health Cost Multiplier: +8%

#### A Sustainable Ration

`COLDWAR_NKO_living_standards` · (16,8) · 35 days

Improve the reliability of food distribution after investment in rural and urban supply.

Requires: (Fertilizer and Irrigation) AND (County Clinics).
- Agricultural District Productivity: +5%
- Social Spending Cost Multiplier: +3%
- Remove An Uneven Civilian Supply

#### State Procurement

`COLDWAR_NKO_state_procurement` · (14,9) · 35 days

Stabilize procurement through guaranteed state purchasing and closer supervision.

Requires: (A Sustainable Ration).
Excludes: Household Plots.
- Agricultural District Productivity: +8%
- Tax Revenue Multiplier: +4%
- Monthly Productivity Growth: -3%
- Bureaucracy Cost Multiplier: +6%

#### Household Plots

`COLDWAR_NKO_household_plots` · (18,9) · 35 days

Let households retain more produce while accepting weaker state extraction.

Requires: (A Sustainable Ration).
Excludes: State Procurement.
- Agricultural District Productivity: +12%
- Monthly Productivity Growth: +4%
- Tax Revenue Multiplier: -5%
- Political Power Gain: -3%

#### Distribution Depots

`COLDWAR_NKO_distribution_reform` · (16,10) · 35 days

Build a distribution network that reduces waste and supplies the army and civilian economy.

Requires: (State Procurement OR Household Plots).
- Expenditure: 0.40% of GDP
- Supply Consumption: -4%
- Bureaucracy Cost Multiplier: +3%

#### Domestic Savings

`COLDWAR_NKO_domestic_finance` · (14,11) · 35 days

Avoid a hard-currency borrowing surge by accepting slower investment.

Requires: (Distribution Depots).
Excludes: Machinery on Credit.
- Interest Rate (percentage points): -0.35 percentage points
- Construction Speed: -4%
- Social Spending Cost Multiplier: +4%

#### Machinery on Credit

`COLDWAR_NKO_western_credit` · (18,11) · 35 days

Borrow to purchase foreign plant and accept debt service and a weaker credit position.

Requires: (Distribution Depots).
Excludes: Domestic Savings.
- Monthly Productivity Growth: +12%
- Production Efficiency Cap: +6%
- While the machinery account is outstanding: Interest Rate (percentage points): +1.25 percentage points
- Machinery credit: +1.50% of GDP in treasury and debt
- Machinery procurement: −1.50% of GDP
- Add 1 Civilian Factory and 1 Building Slot in Pyongyang or North Pyongan

#### Industrial Schools

`COLDWAR_NKO_technical_schools` · (14,12) · 35 days

Train technicians domestically instead of relying on a larger foreign-credit package.

Requires: (Domestic Savings).
- Expenditure: 0.20% of GDP
- Research Speed: +4%
- Education Cost Multiplier: +6%

#### Meet the Foreign Bills

`COLDWAR_NKO_credit_reckoning` · (18,12) · 35 days

Settle the machinery account or seek a revised schedule that the country can sustain.

Requires: (Machinery on Credit).
- Monthly Productivity Growth: +3%
- Resolve the recorded machinery account

#### Quality for Export

`COLDWAR_NKO_export_quality` · (16,13) · 35 days

Slow production-line changes to improve the consistency of saleable output.

Requires: (Industrial Schools OR Meet the Foreign Bills).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +4%
- Production Efficiency growth: -3%

#### Controlled Ventures

`COLDWAR_NKO_joint_ventures` · (16,14) · 35 days

Offer tightly controlled partnerships and tax concessions to attract foreign machinery and management expertise.

Requires: (Quality for Export).
- Expenditure: 0.40% of GDP
- Monthly Productivity Growth: +6%
- Corporate Tax Revenue Multiplier: -5%
- Foreign Influence Defense Multiplier: -5%
- Open foreign investment proposals

### The Korean People's Army

#### Lessons of 1969

`COLDWAR_NKO_lessons_1969` · (30,0) · 21 days

Review the 1968–69 confrontation and restore professional military reporting.

- Army experience gain: +6%
- Army Cost Multiplier: +3%

#### The Fortress State

`COLDWAR_NKO_fortress` · (28,1) · 35 days

Prepare an economical territorial defence at the cost of offensive flexibility.

Requires: (Lessons of 1969).
Excludes: A Mobile Field Army.
- Army defence on core territory: +12%
- Supply Consumption: -6%
- Army attack: -6%
- Monthly Productivity Growth: -4%

#### A Mobile Field Army

`COLDWAR_NKO_mobile_army` · (32,1) · 35 days

Build a more flexible field army that consumes more equipment and fuel.

Requires: (Lessons of 1969).
Excludes: The Fortress State.
- Division Organization: +8%
- Max planning factor: +8%
- Equipment Cost Multiplier: +12%
- Army Fuel Consumption: +8%
- Motorized Infantry Attack: +6%
- Mechanized Infantry Attack: +6%

#### Worker-Peasant Guards

`COLDWAR_NKO_red_guards` · (28,2) · 35 days

Expand reserve training while removing civilian labour from regular production.

Requires: (The Fortress State).
- Training time: -8%
- Monthly Productivity Growth: -4%
- Militia Defense: +10%
- Motorized Militia Defense: +10%

#### General Staff College

`COLDWAR_NKO_staff_college` · (32,2) · 35 days

Improve staff work through a paid officer education programme.

Requires: (A Mobile Field Army).
- Expenditure: 0.20% of GDP
- Max planning factor: +6%
- Army experience gain: +6%
- Education Cost Multiplier: +5%

#### Reorganize Command

`COLDWAR_NKO_army_reorganization` · (30,3) · 35 days

Translate the selected doctrine into command and logistics procedures.

Requires: (Worker-Peasant Guards OR General Staff College).
- Division Organization: +4%
- Bureaucracy Cost Multiplier: +3%
- Replace Economic and Defence Construction: Core Defense +4%; Civilian Factory Construction Speed −4%

#### Artillery Concentration

`COLDWAR_NKO_mass_artillery` · (24,4) · 35 days

Concentrated artillery can overwhelm prepared positions, but it will require larger stocks of ammunition and dependable transport.

Requires: (Reorganize Command).
- Expenditure: 0.40% of GDP
- Supply Consumption: +8%
- Equipment Cost Multiplier: +5%
- Artillery Attack: +6%
- Rocket Artillery Attack: +6%

#### Air Defence Commands

`COLDWAR_NKO_air_defence` · (28,4) · 35 days

Improve coordination of fighter aviation, warning services and ground-based air defence.

Requires: (Reorganize Command).
- Expenditure: 0.40% of GDP
- Equipment Cost Multiplier: +6%
- Interception Detection: +10%
- Static Anti Air damage factor: +5%

#### Coastal Denial

`COLDWAR_NKO_coastal_denial` · (32,4) · 35 days

Concentrate naval training on denying coastal access.

Requires: (Reorganize Command).
- Expenditure: 0.40% of GDP
- Equipment Cost Multiplier: +4%
- Submarine Attack: +8%
- Screen Defense: +6%

#### Special Operations

`COLDWAR_NKO_special_operations` · (36,4) · 35 days

Train specialist formations at a cost to the regular army’s resources.

Requires: (Reorganize Command).
- Expenditure: 0.20% of GDP
- Special Forces Capacity Multiplier: +12%
- Army Cost Multiplier: +6%
- Division Organization: -2%
- Special Forces Attack: +8%
- Special Forces Defense: +5%

#### Ammunition Standards

`COLDWAR_NKO_ammunition_standards` · (24,5) · 35 days

Standardized shells and consistent charges will improve the reliability of artillery fire while limiting production flexibility.

Requires: (Artillery Concentration).
- Expenditure: 0.20% of GDP
- Production Efficiency Cap: +6%
- Production Efficiency growth: -4%
- Artillery Attack: +4%
- Rocket Artillery Attack: +4%

#### Air Warning Network

`COLDWAR_NKO_air_warning` · (28,5) · 35 days

Extend early warning and communications coverage across the northern approaches.

Requires: (Air Defence Commands).
- Expenditure: 0.50% of GDP
- Add 1 Radar Station and 1 Building Slot in Hamgyong or North Pyongan

#### Naval Workshops

`COLDWAR_NKO_naval_workshops` · (32,5) · 35 days

Expand the coastal yards to maintain the fleet and sustain a modest naval-industrial base.

Requires: (Coastal Denial).
- Expenditure: 1.50% of GDP
- Add 1 Naval Dockyard and 1 Building Slot in Hamgyong or Kangwon or Pyongyang

#### Reconnaissance Plan

`COLDWAR_NKO_reconnaissance` · (36,5) · 35 days

Improve reconnaissance training and the quality of operational preparation.

Requires: (Special Operations).
- Max planning factor: +5%
- Army Cost Multiplier: +3%

#### Joint Logistics

`COLDWAR_NKO_joint_logistics` · (30,6) · 35 days

Unify logistics across all four service programmes.

Requires: (Ammunition Standards) AND (Air Warning Network) AND (Naval Workshops) AND (Reconnaissance Plan).
- Expenditure: 0.40% of GDP
- Supply Consumption: -6%
- Bureaucracy Cost Multiplier: +4%

#### Workshop Conversion

`COLDWAR_NKO_civilian_conversions` · (28,7) · 35 days

Release industrial workshops for civilian production while reducing military expansion.

Requires: (Joint Logistics).
Excludes: Arsenal Priority.
- Expenditure: 0.40% of GDP
- Civilian factory construction: +10%
- Military factory construction: -8%
- Equipment Cost Multiplier: +4%
- Remove the remaining Byungjin burden

#### Arsenal Priority

`COLDWAR_NKO_arsenal_priority` · (32,7) · 35 days

Give defence plants priority over civilian construction and power allocation.

Requires: (Joint Logistics).
Excludes: Workshop Conversion.
- Expenditure: 0.40% of GDP
- Factory output: +8%
- Civilian factory construction: -8%
- All Sources of Power Use Multiplier: +6%
- Remove the remaining Byungjin burden

#### A Maintained Reserve

`COLDWAR_NKO_logistics_reserve` · (30,8) · 35 days

Maintain a sustainable reserve rather than a paper mobilization total.

Requires: (Workshop Conversion OR Arsenal Priority).
- Division Organization: +4%
- Army Cost Multiplier: +5%

#### Military Institutes

`COLDWAR_NKO_military_research` · (28,9) · 35 days

Improve domestic military engineering and testing.

Requires: (A Maintained Reserve).
- Expenditure: 0.20% of GDP
- Research Speed: +3%
- Education Cost Multiplier: +4%

#### Readiness Inspections

`COLDWAR_NKO_readiness_inspections` · (32,9) · 35 days

Regular inspections will expose gaps in readiness and require units to spend longer meeting their training standards.

Requires: (A Maintained Reserve).
- Division Organization: +3%
- Training time: +4%

### Patrons and the Korean Question

#### Independent Diplomacy

`COLDWAR_NKO_independent_diplomacy` · (44,0) · 21 days

Preserve freedom of action while bargaining with the larger powers.

- Foreign Influence Defense Multiplier: +8%
- Trade deal opinion factor: -5%

#### Soviet Machinery Offer

`COLDWAR_NKO_moscow_offer` · (40,1) · 35 days

Request a paid machinery package on terms Moscow can accept or refuse.

Requires: (Independent Diplomacy).
- Send a cooperation proposal to Soviet Union
- Agreement: Industrial Cooperation Protocol

#### Repair Ties with Beijing

`COLDWAR_NKO_beijing_offer` · (44,1) · 35 days

Propose a paid agricultural and technical cooperation agreement.

Requires: (Independent Diplomacy).
- Send a cooperation proposal to China
- Agreement: Border Cooperation Protocol

#### Chongryon Trade

`COLDWAR_NKO_diaspora_trade` · (48,1) · 35 days

Overseas Koreans provide a bridge for commerce and family contacts despite the absence of formal relations with Tokyo.

Requires: (Independent Diplomacy).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +5%
- Corporate Tax Revenue Multiplier: -4%
- Foreign Influence Defense Multiplier: -3%

#### Soviet Placements

`COLDWAR_NKO_soviet_training` · (40,2) · 35 days

Place Korean engineers in Soviet institutions after an agreement is signed.

Requires: (Soviet Machinery Offer).
- Send a cooperation proposal to Soviet Union
- Agreement: Technical Placements

#### Regularize Border Trade

`COLDWAR_NKO_border_trade` · (44,2) · 35 days

Provide customs and storage facilities for regulated trade.

Requires: (Repair Ties with Beijing).
- Send a cooperation proposal to China
- Agreement: Border Logistics

#### Commercial Offices

`COLDWAR_NKO_export_offices` · (48,2) · 35 days

Fund a professional commercial service rather than relying solely on political delegations.

Requires: (Chongryon Trade).
- Expenditure: 0.20% of GDP
- Trade deal opinion factor: +8%
- Bureaucracy Cost Multiplier: +4%

#### External Channels

`COLDWAR_NKO_external_balance` · (44,3) · 35 days

Maintain diplomatic and commercial channels to secure machinery and markets while preserving freedom of action.

Requires: (Soviet Placements OR Regularize Border Trade OR Commercial Offices).
- Foreign Influence Defense Multiplier: +5%
- Bureaucracy Cost Multiplier: +3%
- Replace Juche and the Two Patrons: Foreign Influence Defense +6%; Trade Opinion −3%

#### Inter-Korean Channel

`COLDWAR_NKO_detente` · (40,4) · 35 days

Offer talks on divided families, communications and reduced tension.

Requires: (External Channels).
Excludes: Armistice Pressure, The Liberation Line.
- Send a cooperation proposal to South Korea
- Agreement: Inter-Korean Exchange Agreement

#### Armistice Pressure

`COLDWAR_NKO_coercion` · (44,4) · 35 days

Use pressure and readiness as bargaining instruments while accepting a more difficult trade environment.

Requires: (External Channels).
Excludes: Inter-Korean Channel, The Liberation Line.
- Max planning factor: +8%
- Trade deal opinion factor: -15%
- Police Cost Multiplier: +8%

#### Divided Families

`COLDWAR_NKO_red_cross` · (40,5) · 35 days

Finance contact and travel arrangements only after both governments agree.

Requires: (Inter-Korean Channel).
- Expenditure: 0.20% of GDP
- Stability: +3%
- Bureaucracy Cost Multiplier: +3%

#### Reunification Radio

`COLDWAR_NKO_front_broadcasting` · (44,5) · 35 days

Strengthen the united front’s radio services and political messaging toward the South.

Requires: (Armistice Pressure).
- Expenditure: 0.20% of GDP
- Foreign Influence Defense Multiplier: +5%
- Police Cost Multiplier: +4%

#### Confederation Proposal

`COLDWAR_NKO_confederation_offer` · (40,6) · 35 days

Propose a confederal consultative council based on continued sovereignty and negotiated cooperation.

Requires: (Divided Families).
- Send a cooperation proposal to South Korea
- Agreement: Inter-Korean Consultative Council

#### Armed Bargaining

`COLDWAR_NKO_armed_bargaining` · (44,6) · 35 days

Maintain a stronger military negotiating position at a continuing financial cost.

Requires: (Reunification Radio).
- Army defence on core territory: +5%
- Equipment Cost Multiplier: +5%
- Trade deal opinion factor: -5%

#### Non-Aligned Standing

`COLDWAR_NKO_recognition` · (42,7) · 35 days

Build diplomatic representation among non-aligned states and seek wider recognition of the Republic.

Requires: (Confederation Proposal OR Armed Bargaining).
- Expenditure: 0.20% of GDP
- Trade deal opinion factor: +6%
- Bureaucracy Cost Multiplier: +4%

#### Civilian Export Missions

`COLDWAR_NKO_civilian_export` · (40,8) · 35 days

Offer commercial concessions to establish dependable markets for civilian exports.

Requires: (Non-Aligned Standing).
Excludes: Military Missions.
- Expenditure: 0.20% of GDP
- Trade deal opinion factor: +10%
- Corporate Tax Revenue Multiplier: -3%

#### Military Missions

`COLDWAR_NKO_security_export` · (44,8) · 35 days

Develop bilateral military training and advisory missions with willing partners.

Requires: (Non-Aligned Standing).
Excludes: Civilian Export Missions.
- Expenditure: 0.20% of GDP
- Army experience gain: +8%
- Army Cost Multiplier: +6%
- Trade deal opinion factor: -6%

#### Patron Resilience

`COLDWAR_NKO_external_resilience` · (42,9) · 35 days

Diversify inventories and replacement sources to reduce exposure to external restrictions.

Requires: (Civilian Export Missions OR Military Missions).
- Expenditure: 0.40% of GDP
- Imperia sanction resistance: +6%
- Monthly Productivity Growth: -3%
- Remove the imported-input constraint

#### The Liberation Line

`COLDWAR_NKO_war_line` · (48,4) · 35 days

Reunification by force will demand a costly concentration of military power and the abandonment of a negotiated settlement.

Requires: (External Channels).
Excludes: Inter-Korean Channel, Armistice Pressure.
- Expenditure: 0.50% of GDP
- Infantry Division Attack: +6%
- Civilian factory construction: -10%
- Trade deal opinion factor: -15%

#### Forward Artillery

`COLDWAR_NKO_forward_batteries` · (48,5) · 35 days

Forward batteries can strike southern defensive positions, but their deployment and ammunition stocks will be difficult to conceal.

Requires: (The Liberation Line).
- Expenditure: 0.75% of GDP
- Artillery Attack: +10%
- Rocket Artillery Attack: +10%
- Supply Consumption: +6%
- Equipment Cost Multiplier: +5%

#### Forward Supply Depots

`COLDWAR_NKO_forward_supply` · (48,6) · 35 days

Concentrate transport and stores behind the armistice line to sustain an offensive beyond its opening phase.

Requires: (Forward Artillery).
- Expenditure: 0.75% of GDP
- Supply Consumption: -8%
- Army Cost Multiplier: +4%

#### General Mobilization

`COLDWAR_NKO_war_mobilization` · (48,7) · 35 days

Mobilize reserves and place industry on a war footing, drawing skilled workers away from civilian production.

Requires: (Forward Supply Depots).
- Expenditure: 1.00% of GDP
- Infantry Division Attack: +6%
- Armor Division Attack: +6%
- Monthly Productivity Growth: -8%
- Army Cost Multiplier: +8%

#### A Southern Command

`COLDWAR_NKO_campaign_command` · (48,8) · 35 days

Establish the command arrangements needed to coordinate a sustained campaign south of the armistice line.

Requires: (General Mobilization).
- Expenditure: 0.50% of GDP
- Max planning factor: +8%
- Division Organization: +4%
- Bureaucracy Cost Multiplier: +4%

#### Reunification by Force

`COLDWAR_NKO_armed_reunification` · (48,9) · 70 days

The leadership has resolved to pursue reunification through a renewed campaign against the South.

Requires: (A Southern Command).
- Expenditure: 2.00% of GDP
- Gain an Annexation War Goal against South Korea

### Science and the Atomic Question

#### Academy of Sciences

`COLDWAR_NKO_science` · (54,0) · 21 days

Support the scientific institutions needed for a long technical programme.

- Expenditure: 0.20% of GDP
- Research Speed: +3%
- Education Cost Multiplier: +5%

#### Reactor Engineering

`COLDWAR_NKO_reactor_training` · (54,1) · 35 days

Train engineers in research-reactor operation, radiation science and laboratory practice.

Requires: (Academy of Sciences).
- Expenditure: 0.40% of GDP
- 50% research bonus (1 use): Nuclear Reactors

#### Civil Atomic Pact

`COLDWAR_NKO_civil_atom` · (52,2) · 35 days

Seek foreign technical cooperation under verifiable limits on the atomic programme.

Requires: (Reactor Engineering).
Excludes: Sovereign Atom Study.
- Send a cooperation proposal to Soviet Union
- Agreement: Civil Atomic Cooperation

#### Sovereign Atom Study

`COLDWAR_NKO_sovereign_atom` · (56,2) · 35 days

Invest in a national nuclear research programme while accepting cost and external suspicion.

Requires: (Reactor Engineering).
Excludes: Civil Atomic Pact.
- Expenditure: 0.75% of GDP
- Research Speed: +3%
- Education Cost Multiplier: +8%
- Imperia sanction resistance: -6%

#### Reactor Safeguards

`COLDWAR_NKO_safeguards` · (52,3) · 35 days

Register safeguards obligations on the research programme.

Requires: (Civil Atomic Pact).
- Trade deal opinion factor: +6%
- Bureaucracy Cost Multiplier: +4%
- Record the agreed safeguards commitments.

#### The Domestic Fuel Cycle

`COLDWAR_NKO_fuel_studies` · (56,3) · 35 days

Develop fuel-cycle engineering through a funded national research programme.

Requires: (Sovereign Atom Study).
- Expenditure: 0.75% of GDP
- 50% research bonus (1 use): Nuclear Reactors

#### The NPT Bargain

`COLDWAR_NKO_npt_offer` · (52,4) · 35 days

Offer non-proliferation commitments in return for civil technical cooperation.

Requires: (Reactor Safeguards).
- Send a cooperation proposal to Soviet Union
- Agreement: Civil Nuclear Power Protocol

#### Strategic Study

`COLDWAR_NKO_strategic_option` · (56,4) · 70 days

Direct the Academy and defence establishment to study the strategic applications of nuclear research.

Requires: (The Domestic Fuel Cycle).
- Expenditure: 1.00% of GDP
- Research Speed: +3%
- Education Cost Multiplier: +6%
- Trade deal opinion factor: -8%
- 35% research bonus (1 use): Nuclear Weapons
- Support the strategic nuclear research programme

### Korean Democratic Party

#### Patriotic Charter

`COLDWAR_NKO_kdp_charter` · (4,17) · 21 days

Give the party a governing charter grounded in civil administration and national reconciliation.

- Stability: +4%
- Political Power Gain: -4%

#### A Social Republic

`COLDWAR_NKO_kdp_social` · (2,18) · 35 days

Offer social protection and public investment with a larger recurrent budget.

Requires: (Patriotic Charter).
Excludes: A Republic of Enterprise.
- Monthly Productivity Growth: +6%
- Social Spending Cost Multiplier: +10%
- Corporate Tax Revenue Multiplier: -4%

#### A Republic of Enterprise

`COLDWAR_NKO_kdp_enterprise` · (6,18) · 35 days

Support enterprise autonomy while accepting weaker revenue and a more unequal transition.

Requires: (Patriotic Charter).
Excludes: A Social Republic.
- Monthly Productivity Growth: +10%
- Corporate Tax Revenue Multiplier: -8%
- Stability: -4%

#### Municipal Housing

`COLDWAR_NKO_kdp_housing` · (2,19) · 35 days

Delegate housing budgets to municipal boards.

Requires: (A Social Republic).
- Expenditure: 0.40% of GDP
- Stability: +4%
- Bureaucracy Cost Multiplier: +4%

#### Legal Small Enterprise

`COLDWAR_NKO_kdp_licenses` · (6,19) · 35 days

Provide legal registration and supply contracts for small enterprise.

Requires: (A Republic of Enterprise).
- Expenditure: 0.20% of GDP
- Civilian factory construction: +8%
- Bureaucracy Cost Multiplier: +5%

#### A Published Budget

`COLDWAR_NKO_kdp_budget` · (4,20) · 35 days

Publish state accounts and reduce arbitrary fiscal intervention.

Requires: (Municipal Housing OR Legal Small Enterprise).
- Interest Rate (percentage points): -0.25 percentage points
- Political Power Gain: -3%

#### Independent Civil Courts

`COLDWAR_NKO_kdp_courts` · (2,21) · 35 days

Make civil contracts enforceable beyond the ruling party’s immediate wishes.

Requires: (A Published Budget).
Excludes: Elected Executive.
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +5%
- Bureaucracy Cost Multiplier: +6%
- Political Power Gain: -3%

#### Elected Executive

`COLDWAR_NKO_kdp_executive` · (6,21) · 35 days

Prefer a decisive civilian executive to wider institutional checks.

Requires: (A Published Budget).
Excludes: Independent Civil Courts.
- Political Power Gain: +10%
- Stability: +4%
- Research Speed: -3%

#### Civic Associations

`COLDWAR_NKO_kdp_civic` · (2,22) · 35 days

Permit professional and civic organization with a budget for public order.

Requires: (Independent Civil Courts).
- Research Speed: +4%
- Police Cost Multiplier: +4%

#### A Merit Civil Service

`COLDWAR_NKO_kdp_service` · (6,22) · 35 days

Recruit civil servants through professional standards.

Requires: (Elected Executive).
- Expenditure: 0.20% of GDP
- Bureaucracy Cost Multiplier: -4%
- Education Cost Multiplier: +4%

#### Civilian Social Compact

`COLDWAR_NKO_kdp_social_compact` · (4,23) · 35 days

Bind the civilian government to the public services it has promised.

Requires: (Civic Associations OR A Merit Civil Service).
- Stability: +4%
- Social Spending Cost Multiplier: +3%

#### Reconciliation First

`COLDWAR_NKO_kdp_reconciliation` · (2,24) · 35 days

Use the party’s civilian identity to support negotiated inter-Korean relations.

Requires: (Civilian Social Compact).
Excludes: Sovereignty First.
- Expenditure: 0.20% of GDP
- Trade deal opinion factor: +10%
- Army attack: -4%
- Foreign Influence Defense Multiplier: -3%

#### Sovereignty First

`COLDWAR_NKO_kdp_sovereignty` · (6,24) · 35 days

Insist on sovereign equality while preparing a more guarded diplomacy.

Requires: (Civilian Social Compact).
Excludes: Reconciliation First.
- Foreign Influence Defense Multiplier: +10%
- Army defence on core territory: +4%
- Trade deal opinion factor: -6%

#### A Durable Civil Republic

`COLDWAR_NKO_kdp_republic` · (4,25) · 35 days

Consolidate the institutions of a civilian republic.

Requires: (Reconciliation First OR Sovereignty First).
- Monthly Productivity Growth: +4%
- Bureaucracy Cost Multiplier: +3%

### Chondoist Chongu Party

#### Humanity Is Heaven

`COLDWAR_NKO_chondo_heaven` · (12,17) · 21 days

Build a national programme around human dignity, rural community and Korean independence.

- Stability: +5%
- Bureaucracy Cost Multiplier: +3%

#### The Cooperative Village

`COLDWAR_NKO_chondo_cooperative` · (10,18) · 35 days

Retain common agricultural provision under stronger village institutions.

Requires: (Humanity Is Heaven).
Excludes: The Family Holding.
- Agricultural District Productivity: +12%
- Bureaucracy Cost Multiplier: +8%
- Monthly Productivity Growth: -2%

#### The Family Holding

`COLDWAR_NKO_chondo_household` · (14,18) · 35 days

Give households greater control of land use and a larger share of their harvest.

Requires: (Humanity Is Heaven).
Excludes: The Cooperative Village.
- Agricultural District Productivity: +15%
- Tax Revenue Multiplier: -6%
- Stability: -3%

#### Village Granaries

`COLDWAR_NKO_chondo_granary` · (10,19) · 35 days

Finance local storage and guaranteed village reserves.

Requires: (The Cooperative Village).
- Expenditure: 0.40% of GDP
- Agricultural District Productivity: +5%
- Social Spending Cost Multiplier: +5%

#### Licensed Rural Markets

`COLDWAR_NKO_chondo_markets` · (14,19) · 35 days

Legalize local exchange with enforceable market rules.

Requires: (The Family Holding).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +5%
- Tax Revenue Multiplier: -3%
- Police Cost Multiplier: +3%

#### A Rural Settlement

`COLDWAR_NKO_chondo_land` · (12,20) · 35 days

Consolidate the chosen rural property and procurement settlement.

Requires: (Village Granaries OR Licensed Rural Markets).
- Agricultural District Productivity: +4%

#### Freedom of Conscience

`COLDWAR_NKO_chondo_tolerance` · (10,21) · 35 days

Protect believers and non-believers within a common citizenship.

Requires: (A Rural Settlement).
Excludes: A National Moral Order.
- Research Speed: +5%
- Stability: +3%
- Political Power Gain: -5%

#### A National Moral Order

`COLDWAR_NKO_chondo_morality` · (14,21) · 35 days

Use Chondoist moral teaching to strengthen a more uniform national order.

Requires: (A Rural Settlement).
Excludes: Freedom of Conscience.
- Stability: +8%
- Political Power Gain: +5%
- Research Speed: -5%

#### County Schools

`COLDWAR_NKO_chondo_schools` · (10,22) · 35 days

Expand education in neglected rural districts.

Requires: (Freedom of Conscience).
- Expenditure: 0.20% of GDP
- Research Speed: +4%
- Education Cost Multiplier: +7%

#### Councils of Community

`COLDWAR_NKO_chondo_councils` · (14,22) · 35 days

Place local administration in the hands of established community networks.

Requires: (A National Moral Order).
- Bureaucracy Cost Multiplier: -4%
- Monthly Productivity Growth: -2%

#### The Donghak Inheritance

`COLDWAR_NKO_chondo_nation` · (12,23) · 35 days

Present Korean independence as a shared national tradition.

Requires: (County Schools OR Councils of Community).
- Foreign Influence Defense Multiplier: +8%
- Trade deal opinion factor: -3%

#### Protect the Hillsides

`COLDWAR_NKO_chondo_reforestation` · (10,24) · 35 days

Protect soil and catchments by limiting further cultivation of slopes.

Requires: (The Donghak Inheritance).
Excludes: Reclaim New Fields.
- Expenditure: 0.40% of GDP
- Agricultural District Productivity: +6%
- Agricultural district construction: -5%

#### Reclaim New Fields

`COLDWAR_NKO_chondo_reclamation` · (14,24) · 35 days

Finance agricultural capacity while accepting the full construction and staffing burden.

Requires: (The Donghak Inheritance).
Excludes: Protect the Hillsides.
- Expenditure: 1.00% of GDP
- Add 1 Agricultural District and 1 Building Slot in Hwanghae or North Pyongan

#### A Rural Commonwealth

`COLDWAR_NKO_chondo_commonwealth` · (12,25) · 35 days

Secure the rural services and institutions promised by the party.

Requires: (Protect the Hillsides OR Reclaim New Fields).
- Stability: +4%
- Social Spending Cost Multiplier: +4%

### Cabinet and Planning Commission

#### Accounts before Slogans

`COLDWAR_NKO_cabinet_accounts` · (20,17) · 21 days

Make accurate accounts the basis of cabinet authority.

- Monthly Productivity Growth: +6%
- Political Power Gain: -5%

#### Plant Manager Control

`COLDWAR_NKO_cabinet_plant` · (18,18) · 35 days

Delegate production decisions and allow plants to retain investment funds.

Requires: (Accounts before Slogans).
Excludes: National Plan.
- Production Efficiency Cap: +10%
- Monthly Productivity Growth: +6%
- Corporate Tax Revenue Multiplier: -5%

#### National Plan

`COLDWAR_NKO_cabinet_plan` · (22,18) · 35 days

Coordinate supplies centrally through a better funded planning apparatus.

Requires: (Accounts before Slogans).
Excludes: Plant Manager Control.
- Construction Speed: +10%
- Production Efficiency growth: +8%
- Bureaucracy Cost Multiplier: +10%

#### Supply Contracts

`COLDWAR_NKO_cabinet_contracts` · (18,19) · 35 days

Require suppliers and plants to honour realistic delivery contracts.

Requires: (Plant Manager Control).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +4%
- Bureaucracy Cost Multiplier: +4%

#### A Statistical Service

`COLDWAR_NKO_cabinet_statistics` · (22,19) · 35 days

Build professional statistical capacity throughout the ministries.

Requires: (National Plan).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +4%
- Education Cost Multiplier: +4%

#### A Hard-Currency Budget

`COLDWAR_NKO_cabinet_currency` · (20,20) · 35 days

Tie foreign procurement to the country’s ability to meet external bills.

Requires: (Supply Contracts OR A Statistical Service).
- Interest Rate (percentage points): -0.25 percentage points
- Construction Speed: -3%

#### Investment Priority

`COLDWAR_NKO_cabinet_austerity` · (18,21) · 35 days

Hold down current consumption to fund a higher investment share.

Requires: (A Hard-Currency Budget).
Excludes: A Consumer Recovery.
- Construction Speed: +10%
- Stability: -5%
- Social Spending Cost Multiplier: -4%

#### A Consumer Recovery

`COLDWAR_NKO_cabinet_consumption` · (22,21) · 35 days

Use increased consumption to restore confidence while slowing capital formation.

Requires: (A Hard-Currency Budget).
Excludes: Investment Priority.
- Agricultural District Productivity: +6%
- Stability: +6%
- Construction Speed: -6%
- Social Spending Cost Multiplier: +6%

#### Train Administrators

`COLDWAR_NKO_cabinet_training` · (20,22) · 35 days

Make professional administrative training a durable cabinet priority.

Requires: (Investment Priority OR A Consumer Recovery).
- Expenditure: 0.20% of GDP
- Research Speed: +4%
- Education Cost Multiplier: +5%

#### A Governable Plan

`COLDWAR_NKO_cabinet_settlement` · (20,23) · 35 days

Consolidate a plan that the ministries can finance and administer.

Requires: (Train Administrators).
- Monthly Productivity Growth: +4%
- Bureaucracy Cost Multiplier: +3%

### Military Emergency Government

#### The Emergency Council

`COLDWAR_NKO_kpa_council` · (28,17) · 21 days

Place the officer corps at the centre of an emergency administration.

- Division Organization: +6%
- Political Power Gain: +5%
- Stability: -5%
- Army Cost Multiplier: +6%

#### Party Commissars

`COLDWAR_NKO_kpa_party` · (26,18) · 35 days

Keep party control inside the forces to stabilize an uneasy military government.

Requires: (The Emergency Council).
Excludes: Professional Officers.
- Stability: +6%
- Division Organization: +4%
- Research Speed: -4%

#### Professional Officers

`COLDWAR_NKO_kpa_professional` · (30,18) · 35 days

Reduce party interference in command while accepting a political legitimacy problem.

Requires: (The Emergency Council).
Excludes: Party Commissars.
- Division Organization: +8%
- Max planning factor: +6%
- Stability: -4%
- Army Cost Multiplier: +8%

#### Command Compact

`COLDWAR_NKO_kpa_loyalty` · (26,19) · 35 days

Rebuild a compact between commanders and the ruling party apparatus.

Requires: (Party Commissars).
- Foreign Influence Defense Multiplier: +8%
- Bureaucracy Cost Multiplier: +4%

#### Promotion by Merit

`COLDWAR_NKO_kpa_merit` · (30,19) · 35 days

Select officers for technical and operational competence.

Requires: (Professional Officers).
- Expenditure: 0.20% of GDP
- Army experience gain: +8%
- Education Cost Multiplier: +4%

#### Military Supply

`COLDWAR_NKO_kpa_rations` · (28,20) · 35 days

Secure military supply while diverting productive inputs from civilian provision.

Requires: (Command Compact OR Promotion by Merit).
- Supply Consumption: -6%
- Agricultural District Productivity: -5%
- Equipment Cost Multiplier: +5%

#### An Entrenched Garrison

`COLDWAR_NKO_kpa_fortress` · (26,21) · 35 days

Accept a long military administration and its continuing civilian burden.

Requires: (Military Supply).
Excludes: Civilian Handover.
- Army defence on core territory: +10%
- Monthly Productivity Growth: -6%
- Army Cost Multiplier: +6%

#### Civilian Handover

`COLDWAR_NKO_kpa_handover` · (30,21) · 35 days

Commit the emergency council to an orderly transition under an agreed civilian charter.

Requires: (Military Supply).
Excludes: An Entrenched Garrison.
- Trade deal opinion factor: +10%
- Stability: +5%
- Political Power Gain: -6%
- Open negotiations for a civilian transition.

#### Costed Defence Budget

`COLDWAR_NKO_kpa_budget` · (28,22) · 35 days

Bring defence procurement under a budget that the treasury can sustain.

Requires: (An Entrenched Garrison OR Civilian Handover).
- Equipment Cost Multiplier: -4%
- Bureaucracy Cost Multiplier: +3%

#### Army and Republic

`COLDWAR_NKO_kpa_legacy` · (28,23) · 35 days

Settle the role of the armed forces in the chosen political order.

Requires: (Costed Defence Budget).
- Division Organization: +4%
- Army Cost Multiplier: +3%

### Yan'an Reform Communist Programme

#### Socialist Reassessment

`COLDWAR_NKO_yanan_return` · (36,17) · 21 days

Begin a counterfactual reassessment of party rule after a fundamental political change.

- Research Speed: +5%
- Stability: -6%

#### Factory Councils

`COLDWAR_NKO_yanan_councils` · (34,18) · 35 days

Give workers and technical staff a stronger voice in plant decisions.

Requires: (Socialist Reassessment).
Excludes: Party Discipline.
- Monthly Productivity Growth: +8%
- Political Power Gain: -5%
- Bureaucracy Cost Multiplier: +4%

#### Party Discipline

`COLDWAR_NKO_yanan_discipline` · (38,18) · 35 days

Retain centralized party command while ending the personal cult.

Requires: (Socialist Reassessment).
Excludes: Factory Councils.
- Production Efficiency growth: +8%
- Political Power Gain: +6%
- Research Speed: -3%

#### Review Sentences

`COLDWAR_NKO_yanan_rehabilitation` · (36,19) · 35 days

Review political sentences and restore surviving specialists to professional life.

Requires: (Factory Councils OR Party Discipline).
- Research Speed: +4%
- Foreign Influence Defense Multiplier: -4%
- Bureaucracy Cost Multiplier: +4%

#### Foreign Experts

`COLDWAR_NKO_yanan_experts` · (34,20) · 35 days

Accept technical assistance and the influence that accompanies it.

Requires: (Review Sentences).
Excludes: Domestic Expertise.
- Expenditure: 0.40% of GDP
- Research Speed: +7%
- Monthly Productivity Growth: +6%
- Foreign Influence Defense Multiplier: -10%

#### Domestic Expertise

`COLDWAR_NKO_yanan_domestic` · (38,20) · 35 days

Develop expertise at home with slower returns and higher education expenditure.

Requires: (Review Sentences).
Excludes: Foreign Experts.
- Expenditure: 0.40% of GDP
- Research Speed: +4%
- Monthly Productivity Growth: +4%
- Education Cost Multiplier: +8%

#### Korean Reform

`COLDWAR_NKO_yanan_socialism` · (36,21) · 35 days

Combine socialist institutions with a less punitive economic programme.

Requires: (Foreign Experts OR Domestic Expertise).
- Agricultural District Productivity: +5%
- Social Spending Cost Multiplier: +4%

#### Anti-Cult Guarantees

`COLDWAR_NKO_yanan_guarantees` · (36,22) · 35 days

Limit arbitrary appointments and personal command inside the party state.

Requires: (Korean Reform).
- Monthly Productivity Growth: +4%
- Political Power Gain: -4%

### Industrial Labour Programme

#### Workers’ Compact

`COLDWAR_NKO_union_compact` · (44,17) · 21 days

Base a counterfactual government on wages, rations, safety and industrial representation.

- Stability: +5%
- Social Spending Cost Multiplier: +4%

#### Wages and Supply

`COLDWAR_NKO_union_wages` · (42,18) · 35 days

Give workers a larger share of output at a higher social cost.

Requires: (Workers’ Compact).
Excludes: Workers’ Investment.
- Monthly Productivity Growth: +6%
- Social Spending Cost Multiplier: +10%
- Corporate Tax Revenue Multiplier: -4%

#### Workers’ Investment

`COLDWAR_NKO_union_reinvestment` · (46,18) · 35 days

Direct retained earnings toward new investment instead of current consumption.

Requires: (Workers’ Compact).
Excludes: Wages and Supply.
- Civilian factory construction: +10%
- Stability: -4%
- Bureaucracy Cost Multiplier: +6%

#### Industrial Safety

`COLDWAR_NKO_union_safety` · (44,19) · 35 days

Allow inspections to slow unsafe production rather than pursuing quotas at any cost.

Requires: (Wages and Supply OR Workers’ Investment).
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +4%
- Factory output: -3%
- Bureaucracy Cost Multiplier: +4%

#### Production Bargaining

`COLDWAR_NKO_union_bargaining` · (42,20) · 35 days

Negotiate achievable work norms with factory representatives.

Requires: (Industrial Safety).
Excludes: New Chollima Compact.
- Monthly Productivity Growth: +6%
- Political Power Gain: -5%

#### New Chollima Compact

`COLDWAR_NKO_union_mobilization` · (46,20) · 35 days

Link accelerated output to material provision while keeping the strain of mass mobilization.

Requires: (Industrial Safety).
Excludes: Production Bargaining.
- Factory output: +8%
- Monthly Productivity Growth: -4%
- Social Spending Cost Multiplier: +5%

#### Paid Technical Training

`COLDWAR_NKO_union_training` · (44,21) · 35 days

Train skilled workers during paid time away from production.

Requires: (Production Bargaining OR New Chollima Compact).
- Expenditure: 0.20% of GDP
- Research Speed: +4%
- Education Cost Multiplier: +6%

#### Worker Representation

`COLDWAR_NKO_union_representation` · (44,22) · 35 days

Give industrial representation an enduring place in the governing institutions.

Requires: (Paid Technical Training).
- Stability: +4%
- Bureaucracy Cost Multiplier: +4%

### Christian Federation Programme

#### Equal Citizenship

`COLDWAR_NKO_christian_citizenship` · (52,17) · 21 days

Protect freedom of conscience through a counterfactual civic settlement.

- Stability: +5%
- Political Power Gain: -4%

#### Public Social Provision

`COLDWAR_NKO_christian_welfare` · (50,18) · 35 days

Build publicly funded welfare services with room for religious participation.

Requires: (Equal Citizenship).
Excludes: Community Associations.
- Expenditure: 0.20% of GDP
- Monthly Productivity Growth: +5%
- Health Cost Multiplier: +8%
- Social Spending Cost Multiplier: +6%

#### Community Associations

`COLDWAR_NKO_christian_community` · (54,18) · 35 days

Use local associations to provide services with less uniform coverage.

Requires: (Equal Citizenship).
Excludes: Public Social Provision.
- Expenditure: 0.20% of GDP
- Bureaucracy Cost Multiplier: -6%
- Stability: +5%
- Monthly Productivity Growth: -2%

#### Schools for Citizenship

`COLDWAR_NKO_christian_education` · (52,19) · 35 days

Provide education that protects civic equality across beliefs.

Requires: (Public Social Provision OR Community Associations).
- Expenditure: 0.20% of GDP
- Research Speed: +5%
- Education Cost Multiplier: +7%

#### A Plural Civic Compact

`COLDWAR_NKO_christian_tolerance` · (50,20) · 35 days

Bind the government to equal citizenship for believers and non-believers.

Requires: (Schools for Citizenship).
Excludes: Christian Social Charter.
- Research Speed: +5%
- Political Power Gain: -5%

#### Christian Social Charter

`COLDWAR_NKO_christian_moral` · (54,20) · 35 days

Make Christian social teaching a stronger public norm while retaining civil protections.

Requires: (Schools for Citizenship).
Excludes: A Plural Civic Compact.
- Stability: +8%
- Research Speed: -4%
- Police Cost Multiplier: +3%

#### Religious Contacts

`COLDWAR_NKO_christian_relations` · (52,21) · 35 days

Support permitted family and religious contacts across the division of Korea.

Requires: (A Plural Civic Compact OR Christian Social Charter).
- Expenditure: 0.20% of GDP
- Trade deal opinion factor: +8%
- Police Cost Multiplier: +4%

#### Civic Commonwealth

`COLDWAR_NKO_christian_republic` · (52,22) · 35 days

Consolidate a civic order without granting any faith ownership of the state.

Requires: (Religious Contacts).
- Monthly Productivity Growth: +4%
- Social Spending Cost Multiplier: +4%

### Foreign Diplomacy

#### A Wider Foreign Service

`COLDWAR_NKO_foreign_missions` · (68,0) · 21 days

A professional foreign service can pursue trade and technical exchange while defending the republic’s freedom of action.

- Expenditure: 0.20% of GDP
- Foreign Influence Multiplier: +5%
- Bureaucracy Cost Multiplier: +4%

#### East German Machinery

`COLDWAR_NKO_gdr_machinery` · (64,1) · 35 days

Pyongyang proposes East German machinery and specialist training in exchange for reliable industrial deliveries.

Requires: (A Wider Foreign Service).
- Send a cooperation proposal to East Germany
- Agreement: Machinery and Materials Protocol

#### Bulgarian Engineering

`COLDWAR_NKO_bulgarian_engineering` · (68,1) · 35 days

Pyongyang proposes joint work on milling, communications and agricultural engineering, with deliveries linked to agreed project schedules.

Requires: (A Wider Foreign Service).
- Send a cooperation proposal to Bulgaria
- Agreement: Engineering Cooperation Agreement

#### Romanian Exchange

`COLDWAR_NKO_romanian_exchange` · (72,1) · 35 days

Pyongyang proposes a modest programme of industrial and agricultural exchange to diversify its socialist trading partners.

Requires: (A Wider Foreign Service).
- Send a cooperation proposal to Romania
- Agreement: Industrial Exchange Agreement

#### Machine-Tool Standards

`COLDWAR_NKO_gdr_training` · (64,2) · 35 days

Agree machine-tool standards and specialist placements to make imported East German plant easier to operate and maintain.

Requires: (East German Machinery).
- Send a cooperation proposal to East Germany
- Agreement: Machine-Tool Standards

#### Agricultural Science

`COLDWAR_NKO_bulgarian_agrobiology` · (68,2) · 35 days

Arrange field trials and exchanges with Bulgarian agronomists to improve the use of fertilizer, seed and agricultural machinery.

Requires: (Bulgarian Engineering).
- Send a cooperation proposal to Bulgaria
- Agreement: Agricultural Laboratories

#### Reciprocal Trade

`COLDWAR_NKO_romanian_trade` · (72,2) · 35 days

Agree reciprocal industrial and agricultural delivery schedules that both trading partners can sustain.

Requires: (Romanian Exchange).
- Send a cooperation proposal to Romania
- Agreement: Reciprocal Trade Schedules

#### Technical Exchange

`COLDWAR_NKO_technical_exchange` · (68,3) · 35 days

Put foreign technical placements and agreed standards to work in domestic production.

Requires: (Machine-Tool Standards OR Agricultural Science OR Reciprocal Trade).
- Expenditure: 0.20% of GDP
- Research Speed: +2.5%
- Education Cost Multiplier: +3%

#### The Egyptian Accord

`COLDWAR_NKO_egyptian_technical` · (66,4) · 35 days

Pyongyang proposes scientific exchange, technical placements and maintenance training under the bilateral cooperation framework.

Requires: (Technical Exchange).
- Send a cooperation proposal to Egypt
- Agreement: Scientific and Technical Accord

#### Fisheries Negotiations

`COLDWAR_NKO_japan_fisheries` · (70,4) · 35 days

Pyongyang proposes government authorization for a limited fisheries and commercial arrangement without diplomatic recognition.

Requires: (Technical Exchange).
- Send a cooperation proposal to Japan
- Agreement: Fisheries and Commerce Protocol

#### Technical Missions

`COLDWAR_NKO_egyptian_missions` · (66,5) · 35 days

Exchange technical missions and maintenance specialists to improve equipment support and practical training.

Requires: (The Egyptian Accord).
- Send a cooperation proposal to Egypt
- Agreement: Technical Missions

#### Commercial Port Access

`COLDWAR_NKO_japan_ports` · (70,5) · 35 days

Negotiate limited port access and commercial services for authorized fisheries and trade without diplomatic recognition.

Requires: (Fisheries Negotiations).
- Send a cooperation proposal to Japan
- Agreement: Commercial Port Access

### Kim Jong Il’s Leadership

#### Succession Authority

`COLDWAR_NKO_jongil_authority` · (64,17) · 21 days

Kim Jong Il must turn the authority accumulated under his father into an enduring command over party and state.

- Political Power Gain: +6%
- Bureaucracy Cost Multiplier: +4%

#### The Party Centre

`COLDWAR_NKO_jongil_cadres` · (62,18) · 35 days

Rely on the established party apparatus to preserve discipline and continuity through the transition.

Requires: (Succession Authority).
Excludes: A Cabinet Mandate.
- Expenditure: 0.30% of GDP
- Stability: +6%
- Political Power Gain: +5%
- Research Speed: -3%

#### A Cabinet Mandate

`COLDWAR_NKO_jongil_cabinet` · (66,18) · 35 days

Give the cabinet greater authority to manage production and external procurement under the new leadership.

Requires: (Succession Authority).
Excludes: The Party Centre.
- Expenditure: 0.30% of GDP
- Monthly Productivity Growth: +6%
- Research Speed: +3%
- Political Power Gain: -5%
- Bureaucracy Cost Multiplier: +4%

#### The New Leadership

`COLDWAR_NKO_jongil_settlement` · (64,19) · 35 days

Consolidate the leadership settlement chosen for the Republic after the founding generation.

Requires: (The Party Centre OR A Cabinet Mandate).
- Stability: +3%
- Bureaucracy Cost Multiplier: +2%

## Verification

Source references: parent-folder mechanics_revision_v2.md, mechanics_revision_v2_addendum.md, history_revision_v2.md and localization_layout_revision_v2.md. The v2 structural report checks all IDs, reciprocal exclusions, AND/OR histories, full card overlap, GDP pricing fields and equal slots. External browser typography and line routing approximate HOI4. This is neither installed nor engine tested. No gameplay script or game localization has been emitted for this revision.
