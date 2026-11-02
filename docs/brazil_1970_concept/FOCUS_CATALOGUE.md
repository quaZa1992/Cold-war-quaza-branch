IMPERIA COLD WAR

# Brazil: complete proposed focus catalogue

UNAPPROVED CONCEPT. No tree, national spirit, party, event or localisation is installed.

All player-facing text is English. Coordinates are resolved grid units. Separate prerequisite groups are AND; alternatives inside one group are OR. Every reward magnitude is a balance proposal.

## Armed Forces

Médici governs in slot 22. The civilian ARENA and the technocratic coalition are separate institutions.

### Security Cabinet

`COLDWAR_BRA_military_0` | (4, 0) | 35 days | government

Coordinate the presidency, service ministries and national security apparatus under the existing military government.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: None
Mutually exclusive: None

Effects:

* Political Power Gain: +8%
* Bureaucracy Cost: +4%

### Retain AI-5

`COLDWAR_BRA_military_1` | (2, 1) | 35 days | government

Preserve exceptional executive powers and the security services, at the cost of consent and civil liberties.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Security Cabinet)
Mutually exclusive: Controlled Opening

Effects:

* Political Power Gain: +12%
* Stability: -5%
* If The Military are active: Opinion +8

### Controlled Opening

`COLDWAR_BRA_military_2` | (6, 1) | 35 days | government

Begin an explicitly alternative early opening, or follow the later Geisel precedent, while containing resistance inside the armed forces.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Security Cabinet)
Mutually exclusive: Retain AI-5

Effects:

* Treasury: -0.15% of payer current GDP, once
* Remove Rule by Institutional Act
*   Political Power Gain: -12%
*   Stability: +7%
*   Research Speed: +3%
* Political Power Gain: -8%
* Stability: +5%
* If The Military are active: Opinion -8

### Presidential Compact

`COLDWAR_BRA_military_3` | (4, 2) | 35 days | government

Negotiate the composition of the governing coalition without replacing the existing succession system.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Retain AI-5 OR Controlled Opening)
Mutually exclusive: None

Effects:

* The Officer Council

### Staff Colleges

`COLDWAR_BRA_military_4` | (0, 2) | 35 days | government

Fund communications, logistics and professional staff instruction.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Security Cabinet)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* 1 x 50% Electronics research bonus
* Army experience: +25

### Defence Engineers

`COLDWAR_BRA_military_5` | (6, 3) | 35 days | government

Expand a domestic engineering base while accepting the cost of maintaining small production runs.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Presidential Compact)
Mutually exclusive: None

Effects:

* Treasury: -0.65% of payer current GDP, once
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Military Factory
* Equipment Cost: +3%

### Service Coordination

`COLDWAR_BRA_military_6` | (4, 4) | 35 days | government

Improve coordination across services while retaining their institutional budgets.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Staff Colleges) AND (Defence Engineers)
Mutually exclusive: None

Effects:

* Army Organisation: +4%
* Military Spending Cost: +4%

### National Champions

`COLDWAR_BRA_military_7` | (2, 5) | 35 days | government

Concentrate credit in strategic national firms and accept contingent fiscal exposure.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Service Coordination)
Mutually exclusive: Procurement Rules

Effects:

* Factory Output: +7%
* Interest Rate: +0.5 percentage points
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Procurement Rules

`COLDWAR_BRA_military_8` | (6, 5) | 35 days | government

Standardise procurement and end prestige orders at the expense of some domestic production.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (Service Coordination)
Mutually exclusive: National Champions

Effects:

* Equipment Cost: -8%
* Factory Output: -3%

### A Defined Mandate

`COLDWAR_BRA_military_9` | (4, 6) | 35 days | government

Give the service leadership a defined mission, clear responsibilities and a professional review of its institutional role.

Requirements: nationalist_military_junta_are_in_power = yes; Governing party identity: Brazilian Armed Forces
Prerequisites: (National Champions OR Procurement Rules)
Mutually exclusive: None

Effects:

* Army Organisation: +3%
* Political Power Gain: -4%
* Review the Service Mission

## ARENA / PDS

ARENA already exists in slot 1. PDS is a later institutional successor, not a free military programme.

### Governors Compact

`COLDWAR_BRA_arena_0` | (10, 0) | 35 days | government

Bind state governors and the congressional government bloc through a civilian conservative programme.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: None
Mutually exclusive: None

Effects:

* Political Power Gain: +7%
* Bureaucracy Cost: +4%

### Municipal Patronage

`COLDWAR_BRA_arena_1` | (8, 1) | 35 days | government

Use municipal networks to distribute investment and hold the governing coalition together.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Governors Compact)
Mutually exclusive: Technical Cabinet

Effects:

* Stability: +6%
* Bureaucracy Cost: +10%

### Technical Cabinet

`COLDWAR_BRA_arena_2` | (12, 1) | 35 days | government

Select administrators for technical competence, weakening the patronage bargain.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Governors Compact)
Mutually exclusive: Municipal Patronage

Effects:

* Bureaucracy Cost: -8%
* Political Power Gain: -7%

### Development Caucus

`COLDWAR_BRA_arena_3` | (10, 2) | 35 days | government

Build legislative support for a funded development programme.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Municipal Patronage OR Technical Cabinet)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* 1 x 50% Industrial research bonus

### Interior Industry

`COLDWAR_BRA_arena_4` | (8, 3) | 35 days | government

Locate a new industrial plant away from the coastal administrative centres.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Development Caucus)
Mutually exclusive: Farm Credit

Effects:

* Treasury: -0.65% of payer current GDP, once
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Civilian Factory

### Farm Credit

`COLDWAR_BRA_arena_5` | (12, 3) | 35 days | government

Offer agricultural credit through established rural institutions.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Development Caucus)
Mutually exclusive: Interior Industry

Effects:

* Treasury: -0.4% of payer current GDP, once
* Agricultural Productivity: +5%
* If Landowners are active: Opinion +8

### Federal Bargaining

`COLDWAR_BRA_arena_6` | (10, 4) | 35 days | government

Coordinate federal and state investment while accepting a slower bargain over allocations.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Interior Industry OR Farm Credit)
Mutually exclusive: None

Effects:

* Construction Speed: +4%
* Bureaucracy Cost: +3%

### Protected Suppliers

`COLDWAR_BRA_arena_7` | (8, 5) | 35 days | government

Reserve procurement for national suppliers, protecting output but narrowing technological competition.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Federal Bargaining)
Mutually exclusive: Export Constituency

Effects:

* Factory Output: +7%
* Research Speed: -3%

### Export Constituency

`COLDWAR_BRA_arena_8` | (12, 5) | 35 days | government

Shift the coalition toward competitive exporters while exposing sheltered domestic interests.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Federal Bargaining)
Mutually exclusive: Protected Suppliers

Effects:

* Resource Export Income: +10%
* Stability: -3%

### Civilian Conservatism

`COLDWAR_BRA_arena_9` | (10, 6) | 35 days | government

Build a conservative civilian government rather than treating ARENA as a synonym for the military command.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: ARENA; PDS after its real reorganisation
Prerequisites: (Protected Suppliers OR Export Constituency)
Mutually exclusive: None

Effects:

* Stability: +4%
* Political Power Gain: -3%

## MDB / PMDB

The MDB is the legal opposition in 1970. A governing programme requires its actual accession to government.

### Congressional Reform

`COLDWAR_BRA_mdb_0` | (16, 0) | 35 days | government

Rebuild parliamentary oversight and a broad civilian government. Governing before the historical transition is alternative history.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* Stability: +4%
* Political Power Gain: -4%

### Negotiated Amnesty

`COLDWAR_BRA_mdb_1` | (14, 1) | 35 days | government

Seek a negotiated transition and amnesty, accepting limits on accountability.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Congressional Reform)
Mutually exclusive: Judicial Accountability

Effects:

* Treasury: -0.2% of payer current GDP, once
* Stability: +7%
* If The Military are active: Opinion +4
* Political Power Gain: -5%

### Judicial Accountability

`COLDWAR_BRA_mdb_2` | (18, 1) | 35 days | government

Restore judicial independence and investigate state coercion despite military resistance.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Congressional Reform)
Mutually exclusive: Negotiated Amnesty

Effects:

* Treasury: -0.3% of payer current GDP, once
* Bureaucracy Cost: +6%
* If The Military are active: Opinion -10
* Research Speed: +3%

### Constituent Mandate

`COLDWAR_BRA_mdb_3` | (16, 2) | 35 days | government

Give the civilian transition a constitutional framework with competing institutional priorities.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Negotiated Amnesty OR Judicial Accountability)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Remove Rule by Institutional Act
*   Political Power Gain: -12%
*   Stability: +7%
*   Research Speed: +3%
* The Constitutional Settlement

### Municipal Autonomy

`COLDWAR_BRA_mdb_4` | (14, 3) | 35 days | government

Equip elected municipal administrations to manage public services.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Constituent Mandate)
Mutually exclusive: None

Effects:

* Treasury: -0.35% of payer current GDP, once
* Pernambuco: +1 shared building slots
* Pernambuco: +1 Office

### Public Accounts

`COLDWAR_BRA_mdb_5` | (18, 3) | 35 days | government

Create professional auditing capacity for public contracts.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Constituent Mandate)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: -4%

### Federal Guarantees

`COLDWAR_BRA_mdb_6` | (16, 4) | 35 days | government

Distribute authority across federal institutions and accept the cost of coalition bargaining.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Municipal Autonomy) AND (Public Accounts)
Mutually exclusive: None

Effects:

* Stability: +5%
* Political Power Gain: -5%

### Social Covenant

`COLDWAR_BRA_mdb_7` | (14, 5) | 35 days | government

Expand social rights through a broad parliamentary compromise.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Federal Guarantees)
Mutually exclusive: Fiscal Covenant

Effects:

* Stability: +6%
* Social Spending Cost: +8%
* If Labour Unions are active: Opinion +8

### Fiscal Covenant

`COLDWAR_BRA_mdb_8` | (18, 5) | 35 days | government

Constrain unfunded commitments to improve financing conditions.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Federal Guarantees)
Mutually exclusive: Social Covenant

Effects:

* Interest Rate: -0.5 percentage points
* Construction Speed: -4%
* If Labour Unions are active: Opinion -5

### Civilian Republic

`COLDWAR_BRA_mdb_9` | (16, 7) | 35 days | government

Consolidate civilian institutions without assuming that every later PMDB government follows the same economic course.

Requirements: western_liberals_are_in_power = yes; Governing party identity: MDB; PMDB after its real reorganisation
Prerequisites: (Federal Guarantees) AND (Social Covenant OR Fiscal Covenant)
Mutually exclusive: None

Effects:

* Stability: +4%
* Political Power Gain: -3%

## Historic PTB

A counterfactual restoration of the dissolved pre-1965 party. Later PTB and PDT are separate registered organisations.

### Labour Guarantees

`COLDWAR_BRA_ptb_0` | (24, 0) | 35 days | government

Restore the dissolved pre-1965 labourist organisation through a real political opening. This explicitly counterfactual identity is distinct from Ivete Vargas’s later PTB.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Stability: +4%
* Social Spending Cost: +4%

### Union Mediation

`COLDWAR_BRA_ptb_1` | (22, 1) | 35 days | government

Use negotiated corporatist mediation to stabilise industrial relations.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Labour Guarantees)
Mutually exclusive: Independent Unions

Effects:

* If Labour Unions are active: Opinion +12
* Factory Output: +4%
* Bureaucracy Cost: +6%

### Independent Unions

`COLDWAR_BRA_ptb_2` | (26, 1) | 35 days | government

Give organised labour greater independence from executive patronage.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Labour Guarantees)
Mutually exclusive: Union Mediation

Effects:

* If Labour Unions are active: Opinion +15
* Stability: +5%
* Political Power Gain: -6%

### Workplace Insurance

`COLDWAR_BRA_ptb_3` | (24, 2) | 35 days | government

Extend workplace protection with a visible ongoing social budget.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Union Mediation OR Independent Unions)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Social Spending Cost: +5%
* Stability: +4%

### Industrial Apprentices

`COLDWAR_BRA_ptb_4` | (20, 3) | 35 days | government

Fund vocational apprenticeships in established industrial districts.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Workplace Insurance)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* 1 x 50% Industrial research bonus

### Labour Courts

`COLDWAR_BRA_ptb_5` | (28, 2) | 35 days | government

Improve access to labour courts and fund the additional administrative burden.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Labour Guarantees)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: +4%
* Stability: +3%

### Wage Settlement

`COLDWAR_BRA_ptb_6` | (24, 4) | 35 days | government

End the initial wage squeeze through an institutional settlement.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Industrial Apprentices) AND (Labour Courts)
Mutually exclusive: None

Effects:

* Remove Wage Compression
*   Consumer Goods Factories: +2.5%
*   Stability: +5%
* Consumer Goods Factories: +2%

### State Enterprises

`COLDWAR_BRA_ptb_7` | (22, 5) | 35 days | government

Use public firms as employers and investment anchors.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Wage Settlement)
Mutually exclusive: Small Employers

Effects:

* Factory Output: +6%
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Small Employers

`COLDWAR_BRA_ptb_8` | (26, 5) | 35 days | government

Support smaller employers through tax relief and negotiated labour obligations.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (Wage Settlement)
Mutually exclusive: State Enterprises

Effects:

* Corporate Tax Income: -5%
* Stability: +5%

### Labour Republic

`COLDWAR_BRA_ptb_9` | (24, 6) | 35 days | government

Maintain a labourist government whose employment and social commitments rest on functioning public institutions.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Old PTB restoration, or separately registered later PTB
Prerequisites: (State Enterprises OR Small Employers)
Mutually exclusive: None

Effects:

* Stability: +4%
* Political Power Gain: -3%

## PDT

PDT forms in 1980 after the dispute over the PTB name. Its own governing identity is not yet installed.

### Labourist Democracy

`COLDWAR_BRA_pdt_0` | (32, 0) | 35 days | government

Build Brizola’s democratic labourist alternative with education and national development at its centre.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Stability: +5%
* Political Power Gain: -4%

### Full-Time Schools

`COLDWAR_BRA_pdt_1` | (30, 1) | 35 days | government

Use the CIEP precedent for full-time schooling, with a substantial operating commitment.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Labourist Democracy)
Mutually exclusive: Technical Colleges

Effects:

* Treasury: -0.6% of payer current GDP, once
* Education Literacy Growth: +8%
* Education Cost: +10%

### Technical Colleges

`COLDWAR_BRA_pdt_2` | (34, 1) | 35 days | government

Prioritise technical and industrial education over the broader full-time school model.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Labourist Democracy)
Mutually exclusive: Full-Time Schools

Effects:

* Treasury: -0.45% of payer current GDP, once
* Research Speed: +5%
* Education Cost: +6%

### Teachers Compact

`COLDWAR_BRA_pdt_3` | (32, 2) | 35 days | government

Secure teachers and local administrators for a sustained education programme.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Full-Time Schools OR Technical Colleges)
Mutually exclusive: None

Effects:

* Weekly programme expense: 0.1% of payer current annual GDP / 52
* Stability: +3%

### Public Engineering

`COLDWAR_BRA_pdt_4` | (30, 3) | 35 days | government

Build a public engineering and planning office in Rio de Janeiro.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Teachers Compact)
Mutually exclusive: None

Effects:

* Treasury: -0.6% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Office

### Local Services

`COLDWAR_BRA_pdt_5` | (34, 3) | 35 days | government

Extend basic urban networks in Rio Grande do Sul.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Teachers Compact)
Mutually exclusive: None

Effects:

* Treasury: -0.45% of payer current GDP, once
* Rio Grande do Sul: +1 shared building slots
* Rio Grande do Sul: +1 Infrastructure

### Mass Education

`COLDWAR_BRA_pdt_6` | (32, 4) | 35 days | government

Broaden access to education and remove the initial technical-research bottleneck.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Teachers Compact)
Mutually exclusive: None

Effects:

* Remove Uneven Technical Education
*   Research Speed: +7%
* Education Cost: +3%

### National Ownership

`COLDWAR_BRA_pdt_7` | (30, 5) | 35 days | government

Retain strategic ownership while accepting narrower foreign technology access.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Mass Education)
Mutually exclusive: Licensed Industry

Effects:

* Factory Output: +6%
* Research Speed: -2.5%

### Licensed Industry

`COLDWAR_BRA_pdt_8` | (34, 5) | 35 days | government

Acquire licences for national development with a continuing foreign technology relationship.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (Mass Education)
Mutually exclusive: National Ownership

Effects:

* 2 x 50% Industrial research bonus
* Weekly programme expense: 0.1% of payer current annual GDP / 52
* Foreign Influence Defence: -5%

### A National School

`COLDWAR_BRA_pdt_9` | (32, 6) | 35 days | government

Anchor education in a sustained national programme with stable administrative support.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PDT, formation and separate identity required
Prerequisites: (National Ownership OR Licensed Industry)
Mutually exclusive: None

Effects:

* Education Literacy Growth: +4%
* Bureaucracy Cost: +3%

## Workers Party

PT is a new party formed in 1980, rooted in the ABC labour movement. Governing in this era is a plausible electoral alternative, not historical fact.

### Workers Government

`COLDWAR_BRA_pt_0` | (38, 0) | 35 days | government

Bring the new union movement and popular organisations into government without importing later Lula-era programmes.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* If Labour Unions are active: Opinion +10
* Political Power Gain: -4%

### Workers Councils

`COLDWAR_BRA_pt_1` | (36, 1) | 35 days | government

Give workplace councils authority and accept the coordination costs of negotiated production.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Workers Government)
Mutually exclusive: Productive Pact

Effects:

* Stability: +7%
* Production Efficiency Growth: -5%

### Productive Pact

`COLDWAR_BRA_pt_2` | (40, 1) | 35 days | government

Trade workplace autonomy for a negotiated national investment and output agreement.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Workers Government)
Mutually exclusive: Workers Councils

Effects:

* Factory Output: +7%
* Stability: -3.5%

### Union Independence

`COLDWAR_BRA_pt_3` | (38, 2) | 35 days | government

Replace wage compression with free collective bargaining.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Workers Councils OR Productive Pact)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Remove Wage Compression
*   Consumer Goods Factories: +2.5%
*   Stability: +5%
* Consumer Goods Factories: +2.5%

### Urban Health

`COLDWAR_BRA_pt_4` | (36, 3) | 35 days | government

Create the municipal planning and administrative capacity required for broad urban healthcare, with a funded operating budget.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Union Independence)
Mutually exclusive: None

Effects:

* Treasury: -0.5% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Office
* Weekly programme expense: 0.08% of payer current annual GDP / 52

### Popular Budgeting

`COLDWAR_BRA_pt_5` | (42, 2) | 35 days | government

Use the later Porto Alegre participatory-budget precedent for a distinct governing alternative.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Workers Government)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Bureaucracy Cost: +5%
* Stability: +4%

### Rights in Practice

`COLDWAR_BRA_pt_6` | (38, 4) | 35 days | government

Fund the institutions required to turn social guarantees into services.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Union Independence) AND (Urban Health)
Mutually exclusive: None

Effects:

* Stability: +4%
* Social Spending Cost: +5%

### Cooperative Land

`COLDWAR_BRA_pt_7` | (36, 5) | 35 days | government

Finance cooperative farming and redistribution while managing conflict with established landowners.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Rights in Practice)
Mutually exclusive: Family Farm Credit

Effects:

* Treasury: -0.45% of payer current GDP, once
* Agricultural Productivity: +6%
* If Landowners are active: Opinion -6
* Weekly programme expense: 0.08% of payer current annual GDP / 52

### Family Farm Credit

`COLDWAR_BRA_pt_8` | (40, 5) | 35 days | government

Expand family-farm credit and extension without a general expropriation programme.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Rights in Practice)
Mutually exclusive: Cooperative Land

Effects:

* Treasury: -0.35% of payer current GDP, once
* Agricultural Productivity: +4%
* If Landowners are active: Opinion +6
* Bureaucracy Cost: +4%

### Popular Democracy

`COLDWAR_BRA_pt_9` | (38, 6) | 35 days | government

Sustain a participatory democratic government whose active policy package ends with its tenure.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: PT, formation and separate identity required
Prerequisites: (Cooperative Land OR Family Farm Credit)
Mutually exclusive: None

Effects:

* Stability: +5%
* Political Power Gain: -6%

## Liberal Front

PFL emerges in 1985 from PDS dissidents. It is not simply the entire ARENA renamed.

### Liberal Coalition

`COLDWAR_BRA_pfl_0` | (46, 0) | 35 days | government

Build a conservative civilian coalition from the Liberal Front split, with its own regional and business interests.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: None
Mutually exclusive: None

Effects:

* Political Power Gain: +6%
* Bureaucracy Cost: +3.5%

### Regional Investment

`COLDWAR_BRA_pfl_1` | (44, 1) | 35 days | government

Direct development investment toward the Northeast through regional political bargains.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Liberal Coalition)
Mutually exclusive: National Competition

Effects:

* Treasury: -0.7% of payer current GDP, once
* Bahia: +1 shared building slots
* Bahia: +1 Civilian Factory
* Bureaucracy Cost: +4%

### National Competition

`COLDWAR_BRA_pfl_2` | (48, 1) | 35 days | government

Expose protected firms to national competition, accepting regional industrial disruption.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Liberal Coalition)
Mutually exclusive: Regional Investment

Effects:

* Factory Output: +6%
* Stability: -3%

### Civil Service Review

`COLDWAR_BRA_pfl_3` | (46, 2) | 35 days | government

Professionalise appointments while retaining a parliamentary governing bargain.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Regional Investment OR National Competition)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: -4%

### Port Services

`COLDWAR_BRA_pfl_4` | (44, 3) | 35 days | government

Improve commercial and logistics administration in Pernambuco.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Civil Service Review)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Pernambuco: +1 shared building slots
* Pernambuco: +1 Office

### Small Business

`COLDWAR_BRA_pfl_5` | (48, 3) | 35 days | government

Reduce the tax burden on firms while sacrificing immediate revenue.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Civil Service Review)
Mutually exclusive: None

Effects:

* Corporate Tax Income: -4%
* Productivity Growth: +3%

### Civilian Coalition

`COLDWAR_BRA_pfl_6` | (44, 4) | 35 days | government

Consolidate an elected civilian centre-right coalition.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Civil Service Review)
Mutually exclusive: None

Effects:

* Stability: +3%
* Political Power Gain: -3%

### Social Partnership

`COLDWAR_BRA_pfl_7` | (46, 5) | 35 days | government

Preserve a social compromise alongside market-oriented development.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Small Business)
Mutually exclusive: Budget Credibility

Effects:

* Stability: +5%
* Social Spending Cost: +6%

### Budget Credibility

`COLDWAR_BRA_pfl_8` | (50, 5) | 35 days | government

Limit development credit and improve the government’s financing position.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Small Business)
Mutually exclusive: Social Partnership

Effects:

* Interest Rate: -0.45 percentage points
* Construction Speed: -3%

### Liberal Institutions

`COLDWAR_BRA_pfl_9` | (48, 6) | 35 days | government

Support gradual institutional modernisation rather than reducing liberalism to a single tax bonus.

Requirements: western_conservatism_are_in_power = yes; Governing party identity: PFL, formation and separate identity required
Prerequisites: (Civilian Coalition) AND (Social Partnership OR Budget Credibility)
Mutually exclusive: None

Effects:

* Productivity Growth: +2.5%
* Political Power Gain: -3%

## PSDB

PSDB forms in 1988. Its economic branches are period alternatives, not an automatic Real Plan or presidential victory.

### Social Democracy

`COLDWAR_BRA_psdb_0` | (54, 0) | 35 days | government

Build the 1988 PSDB alternative around democratic institutions, public services and economic modernisation.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Research Speed: +3%
* Bureaucracy Cost: +3%

### Monetary Restraint

`COLDWAR_BRA_psdb_1` | (52, 1) | 35 days | government

Restrain credit and demand to contain inflation, slowing investment.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Social Democracy)
Mutually exclusive: Investment Compact

Effects:

* Inflation Growth: -10%
* Construction Speed: -5%

### Investment Compact

`COLDWAR_BRA_psdb_2` | (56, 1) | 35 days | government

Protect productive investment while accepting a more difficult inflation problem.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Social Democracy)
Mutually exclusive: Monetary Restraint

Effects:

* Construction Speed: +7%
* Inflation Growth: +8%

### Professional Treasury

`COLDWAR_BRA_psdb_3` | (54, 2) | 35 days | government

Fund professional debt management without granting a free debt cancellation.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Monetary Restraint OR Investment Compact)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Interest Rate: -0.35 percentage points

### Research Networks

`COLDWAR_BRA_psdb_4` | (52, 3) | 35 days | government

Connect universities and industrial research through a period-appropriate technology programme.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Professional Treasury)
Mutually exclusive: None

Effects:

* Treasury: -0.45% of payer current GDP, once
* 2 x 50% Electronics research bonus

### Public Evaluation

`COLDWAR_BRA_psdb_5` | (58, 3) | 35 days | government

Use service evaluation and administrative reform to improve education spending efficiency.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Professional Treasury)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Education Cost: -4%

### Social Guarantees

`COLDWAR_BRA_psdb_6` | (52, 4) | 35 days | government

Maintain a social budget alongside macroeconomic reform.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Research Networks)
Mutually exclusive: None

Effects:

* Weekly programme expense: 0.08% of payer current annual GDP / 52
* Stability: +4%

### Competitive Industry

`COLDWAR_BRA_psdb_7` | (56, 5) | 35 days | government

Use competition to accelerate productivity while accepting firm closures and industrial conflict.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Professional Treasury)
Mutually exclusive: Managed Conversion

Effects:

* Production Efficiency Growth: +8%
* Stability: -3%

### Managed Conversion

`COLDWAR_BRA_psdb_8` | (60, 5) | 35 days | government

Finance a slower industrial transition with explicit public support.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Professional Treasury)
Mutually exclusive: Competitive Industry

Effects:

* Factory Output: +4%
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Democratic Modernity

`COLDWAR_BRA_psdb_9` | (54, 6) | 35 days | government

Consolidate a late-Cold-War reform programme without importing the 1994 Real Plan.

Requirements: western_liberals_are_in_power = yes; Governing party identity: PSDB, formation and separate identity required
Prerequisites: (Social Guarantees) AND (Competitive Industry OR Managed Conversion)
Mutually exclusive: None

Effects:

* Research Speed: +2.5%
* Political Power Gain: -3%

## PCB

PCB is clandestine in 1970 and later regains legality. A governing path requires genuine legalisation or an explicitly alternate accession.

### Communist Coalition

`COLDWAR_BRA_pcb_0` | (64, 0) | 35 days | government

Give the PCB a distinct governing alternative rooted in its organisation and Soviet relationship.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Political Power Gain: +6%
* Foreign Influence Defence: -4%

### Pluralist Transition

`COLDWAR_BRA_pcb_1` | (62, 1) | 35 days | government

Pursue a broad democratic transition while sharing authority with other left parties.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Communist Coalition)
Mutually exclusive: Cadre Direction

Effects:

* Stability: +6%
* Political Power Gain: -6%

### Cadre Direction

`COLDWAR_BRA_pcb_2` | (66, 1) | 35 days | government

Concentrate authority in party cadres to direct industrial targets.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Communist Coalition)
Mutually exclusive: Pluralist Transition

Effects:

* Factory Output: +7%
* Stability: -4.5%

### Planning Institutes

`COLDWAR_BRA_pcb_3` | (64, 2) | 35 days | government

Build planning expertise as a real administrative asset.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Pluralist Transition OR Cadre Direction)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Office

### Strategic Production

`COLDWAR_BRA_pcb_4` | (62, 3) | 35 days | government

Expand basic industrial production through public investment.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Planning Institutes)
Mutually exclusive: Technical Exchange

Effects:

* Treasury: -0.6% of payer current GDP, once
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Civilian Factory

### Technical Exchange

`COLDWAR_BRA_pcb_5` | (66, 3) | 35 days | government

Fund a technical exchange without assuming a foreign player’s agreement.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Planning Institutes)
Mutually exclusive: Strategic Production

Effects:

* Treasury: -0.2% of payer current GDP, once
* 1 x 50% Industrial research bonus

### Public Ownership

`COLDWAR_BRA_pcb_6` | (64, 4) | 35 days | government

Support long production runs through public firms and a recurring capital programme.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Strategic Production OR Technical Exchange)
Mutually exclusive: None

Effects:

* Production Efficiency Cap: +5%
* Weekly programme expense: 0.1% of payer current annual GDP / 52

### National Communism

`COLDWAR_BRA_pcb_7` | (62, 5) | 35 days | government

Retain independent direction at the cost of access to some foreign technical networks.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Public Ownership)
Mutually exclusive: International Links

Effects:

* Foreign Influence Defence: +8%
* Research Speed: -2.5%

### International Links

`COLDWAR_BRA_pcb_8` | (66, 5) | 35 days | government

Use external communist networks while accepting political dependence. A treaty still requires recipient consent.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (Public Ownership)
Mutually exclusive: National Communism

Effects:

* Research Speed: +5%
* Foreign Influence Defence: -7%

### A Socialist Mandate

`COLDWAR_BRA_pcb_9` | (64, 6) | 35 days | government

Sustain a distinct PCB programme, separate from the PCdoB’s rural revolutionary strategy.

Requirements: emerging_communist_state_are_in_power = yes; Governing party identity: Brazilian Communist Party
Prerequisites: (National Communism OR International Links)
Mutually exclusive: None

Effects:

* Stability: +4%
* Bureaucracy Cost: +4%

## PCdoB

The Araguaia campaign is a historical tragedy, not a guaranteed successful revolution. Governing is explicit alternative history.

### Rural Revolution

`COLDWAR_BRA_pcdob_0` | (70, 0) | 35 days | government

Develop a distinct alternate governing programme from the PCdoB’s rural revolutionary tradition.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Political Power Gain: +6%
* Stability: -4%

### Peasant Cooperatives

`COLDWAR_BRA_pcdob_1` | (68, 1) | 35 days | government

Pool equipment and extension services while confronting landholding interests.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Rural Revolution)
Mutually exclusive: Village Land Titles

Effects:

* Agricultural Productivity: +7%
* Weekly programme expense: 0.12% of payer current annual GDP / 52
* If Landowners are active: Opinion -8

### Village Land Titles

`COLDWAR_BRA_pcdob_2` | (72, 1) | 35 days | government

Prioritise secure household titles and local consent over collective ownership.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Rural Revolution)
Mutually exclusive: Peasant Cooperatives

Effects:

* Stability: +7%
* Agricultural Productivity: +3.5%
* Bureaucracy Cost: +6%

### Rural Administration

`COLDWAR_BRA_pcdob_3` | (70, 2) | 35 days | government

Create a permanent civil administration in Pará to govern and deliver services beyond the revolutionary organisation.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Peasant Cooperatives OR Village Land Titles)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Para: +1 shared building slots
* Para: +1 Office

### Village Instruction

`COLDWAR_BRA_pcdob_4` | (68, 3) | 35 days | government

Expand rural instruction under a funded education programme.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Rural Administration)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Education Literacy Growth: +6%
* Education Cost: +6%

### Local Workshops

`COLDWAR_BRA_pcdob_5` | (72, 3) | 35 days | government

Build a regional civilian workshop complex for agricultural and basic industrial tools.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Rural Administration)
Mutually exclusive: None

Effects:

* Treasury: -0.55% of payer current GDP, once
* Pernambuco: +1 shared building slots
* Pernambuco: +1 Civilian Factory

### Agrarian Settlement

`COLDWAR_BRA_pcdob_6` | (70, 4) | 35 days | government

Replace the initial land inequality burden through a costly agrarian settlement.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Rural Administration)
Mutually exclusive: None

Effects:

* Remove Land and Regional Inequality
*   Agricultural Productivity: +6%
*   Stability: +4%
* Bureaucracy Cost: +4%

### People’s Defence

`COLDWAR_BRA_pcdob_7` | (68, 5) | 35 days | government

Develop infantry-oriented territorial defence with a larger personnel bill.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Village Instruction)
Mutually exclusive: Civil Reconstruction

Effects:

* Infantry Attack: +6%
* Army Personnel Cost: +8%

### Civil Reconstruction

`COLDWAR_BRA_pcdob_8` | (72, 5) | 35 days | government

Prioritise reconstruction while reducing military institutional weight.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Local Workshops)
Mutually exclusive: People’s Defence

Effects:

* Construction Speed: +6%
* Army Organisation: -4%

### A Rural Republic

`COLDWAR_BRA_pcdob_9` | (70, 6) | 35 days | government

Turn a rural revolutionary organisation into a working administration with lasting public responsibilities.

Requirements: neutrality_neutral_communism_are_in_power = yes; Governing party identity: Communist Party of Brazil
Prerequisites: (Agrarian Settlement) AND (People’s Defence OR Civil Reconstruction)
Mutually exclusive: None

Effects:

* Stability: +4%
* Political Power Gain: -4%

## Lacerdists

Lacerda’s rights were suspended and he died in 1977. Early restoration is alternate history; an earned Lacerdist programme needs a real political successor after his death.

### Public Probity

`COLDWAR_BRA_populist_0` | (76, 0) | 35 days | government

Develop Lacerda’s electoral and anti-corruption alternative while he or a separately registered Lacerdist successor actually governs.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: -4%
* Political Power Gain: -3%

### Independent Auditors

`COLDWAR_BRA_populist_1` | (74, 1) | 35 days | government

Give auditors institutional independence at the expense of executive discretion.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Public Probity)
Mutually exclusive: Presidential Campaign

Effects:

* Bureaucracy Cost: -6%
* Political Power Gain: -5%

### Presidential Campaign

`COLDWAR_BRA_populist_2` | (78, 1) | 35 days | government

Mobilise a personal presidential mandate with greater polarisation.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Public Probity)
Mutually exclusive: Independent Auditors

Effects:

* Political Power Gain: +10%
* Stability: -4%

### Administrative Reform

`COLDWAR_BRA_populist_3` | (76, 2) | 35 days | government

Reform purchasing and appointments through functioning administrative institutions.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Independent Auditors OR Presidential Campaign)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Productivity Growth: +3%

### Competitive Imports

`COLDWAR_BRA_populist_4` | (74, 3) | 35 days | government

Open access to imported machinery while exposing domestic manufacturers.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Administrative Reform)
Mutually exclusive: None

Effects:

* Research Speed: +4%
* Factory Output: -4%

### Urban Management

`COLDWAR_BRA_populist_5` | (78, 3) | 35 days | government

Invest in practical urban transport and basic networks.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Administrative Reform)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Infrastructure

### Electoral Government

`COLDWAR_BRA_populist_6` | (76, 3) | 35 days | government

Restore an electoral mandate without imposing a specific presidential winner.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Administrative Reform)
Mutually exclusive: None

Effects:

* Stability: +4%
* Political Power Gain: -3%

### Rapid Competition

`COLDWAR_BRA_populist_7` | (74, 5) | 35 days | government

Choose a sharp competitive adjustment. This does not implement the later Collor deposit freeze.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Electoral Government)
Mutually exclusive: Staged Liberalism

Effects:

* Production Efficiency Growth: +10%
* Stability: -7%

### Staged Liberalism

`COLDWAR_BRA_populist_8` | (78, 5) | 35 days | government

Subsidise a slower transition with a continuing adjustment budget.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Electoral Government)
Mutually exclusive: Rapid Competition

Effects:

* Production Efficiency Growth: +5%
* Weekly programme expense: 0.1% of payer current annual GDP / 52

### Executive Oversight

`COLDWAR_BRA_populist_9` | (76, 6) | 35 days | government

Make executive authority answerable to oversight instead of granting a free corruption purge.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: Lacerdists
Prerequisites: (Rapid Competition OR Staged Liberalism)
Mutually exclusive: None

Effects:

* Bureaucracy Cost: -3.5%
* Political Power Gain: -3.5%

## PRN

A separate late-Cold-War programme. Formation in 1989 and an actual PRN government are required; no scripted Collor victory.

### A New Presidency

`COLDWAR_BRA_prn_0` | (82, 0) | 35 days | government

Develop a late-1989 personal presidential coalition. PRN is the renamed Party of Youth, not Lacerda’s party.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Political Power Gain: +7%
* Stability: -2.5%

### Competition Shock

`COLDWAR_BRA_prn_1` | (80, 1) | 35 days | government

Open the economy rapidly, accepting disruption and closures among sheltered firms.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (A New Presidency)
Mutually exclusive: Negotiated Opening

Effects:

* Production Efficiency Growth: +10%
* Stability: -6%

### Negotiated Opening

`COLDWAR_BRA_prn_2` | (84, 1) | 35 days | government

Fund a slower competitive adjustment with an explicit transition budget.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (A New Presidency)
Mutually exclusive: Competition Shock

Effects:

* Production Efficiency Growth: +5%
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Purchasing Reform

`COLDWAR_BRA_prn_3` | (82, 2) | 35 days | government

Build accountable public purchasing rather than granting a free corruption purge.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Competition Shock OR Negotiated Opening)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Bureaucracy Cost: -4%

### Industrial Imports

`COLDWAR_BRA_prn_4` | (80, 3) | 35 days | government

Buy access to industrial technology while retaining vulnerability to external commercial pressure.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Purchasing Reform)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* 2 x 50% Industrial research bonus
* Foreign Influence Defence: -3.5%

### Service Review

`COLDWAR_BRA_prn_5` | (86, 2) | 35 days | government

Reduce redundant appointments with a real political cost.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (A New Presidency)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: -3.5%
* Stability: -2.5%

### Presidential Coalition

`COLDWAR_BRA_prn_6` | (82, 4) | 35 days | government

Keep a heterogeneous governing coalition functioning through parliamentary bargains.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Purchasing Reform) AND (Industrial Imports)
Mutually exclusive: None

Effects:

* Political Power Gain: +5%
* Bureaucracy Cost: +4%

### Price Restraint

`COLDWAR_BRA_prn_7` | (80, 5) | 35 days | government

Contain inflation through credit restraint. This does not recreate the 1990 deposit freeze.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Presidential Coalition)
Mutually exclusive: Productive Credit

Effects:

* Inflation Growth: -10%
* Construction Speed: -5%

### Productive Credit

`COLDWAR_BRA_prn_8` | (84, 5) | 35 days | government

Protect industrial credit while accepting higher financing pressure.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Presidential Coalition)
Mutually exclusive: Price Restraint

Effects:

* Construction Speed: +6%
* Interest Rate: +0.5 percentage points

### Public Accountability

`COLDWAR_BRA_prn_9` | (82, 7) | 35 days | government

Submit presidential administration to effective oversight and legislative bargaining.

Requirements: nationalist_right_wing_populists_are_in_power = yes; Governing party identity: PRN, separate 1989 formation and identity required
Prerequisites: (Presidential Coalition) AND (Price Restraint OR Productive Credit)
Mutually exclusive: None

Effects:

* Stability: +3.5%
* Political Power Gain: -4%

## Institutions and Society

Civilian institutions, churches, workers, schools, cities and rural rights. Available to every government subject to the actual policy choice.

### Civil Guarantees

`COLDWAR_BRA_constitutional` | (4, 9) | 35 days | national

End exceptional powers through a genuine constitutional reform. Early adoption is alternative history.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Remove Rule by Institutional Act
*   Political Power Gain: -12%
*   Stability: +7%
*   Research Speed: +3%
* Political Power Gain: -6%

### Church Grants

`COLDWAR_BRA_church_dialogue` | (0, 10) | 35 days | national

Prioritise public grants to church-linked service organisations and dialogue with the CNBB. This funding priority does not abolish secular provision.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* Stability: +5%
* Political Power Gain: -3%

### Public Service Plan

`COLDWAR_BRA_secular_services` | (4, 10) | 35 days | national

Prioritise a publicly administered service network. This funding priority does not ban church organisations or CNBB dialogue.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Bureaucracy Cost: +4%
* Stability: +4%

### Plural Party Law

`COLDWAR_BRA_legal_parties` | (8, 10) | 35 days | national

Replace the imposed two-party framework and make actual new-party formation possible.

Requirements: Shared national programme
Prerequisites: (Civil Guarantees)
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* The Party Reorganisation

### National Training

`COLDWAR_BRA_schools` | (2, 11) | 35 days | national

Broaden technical training through public institutions.

Requirements: Shared national programme
Prerequisites: (Church Grants OR Public Service Plan)
Mutually exclusive: None

Effects:

* Treasury: -0.5% of payer current GDP, once
* Remove Uneven Technical Education
*   Research Speed: +7%
* 1 x 50% Industrial research bonus

### Municipal Networks

`COLDWAR_BRA_municipal` | (8, 11) | 35 days | national

Extend basic municipal networks in industrial and northeastern cities.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.6% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Infrastructure
* Pernambuco: +1 shared building slots
* Pernambuco: +1 Infrastructure

### University Research

`COLDWAR_BRA_universities` | (0, 12) | 35 days | national

Fund university research with a continuing operating budget.

Requirements: Shared national programme
Prerequisites: (National Training)
Mutually exclusive: Adult Literacy

Effects:

* Treasury: -0.3% of payer current GDP, once
* 2 x 50% Electronics research bonus
* Weekly programme expense: 0.08% of payer current annual GDP / 52

### Adult Literacy

`COLDWAR_BRA_adult_literacy` | (4, 12) | 35 days | national

Expand access to literacy without pretending an immediate literacy-rate jump.

Requirements: Shared national programme
Prerequisites: (National Training)
Mutually exclusive: University Research

Effects:

* Treasury: -0.25% of payer current GDP, once
* Education Literacy Growth: +6%
* Education Cost: +5%

### Urban Services

`COLDWAR_BRA_urban_services` | (8, 12) | 35 days | national

Provide municipal administrative capacity for health and housing services.

Requirements: Shared national programme
Prerequisites: (Municipal Networks)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Office
* Weekly programme expense: 0.06% of payer current annual GDP / 52

### Serviced Cities

`COLDWAR_BRA_city_settlement` | (8, 13) | 35 days | national

Complete the joint transport and services remedy for urban pressure.

Requirements: Shared national programme
Prerequisites: (Urban Services)
Mutually exclusive: None

Effects:

* Remove Cities Beyond Their Services
*   Bureaucracy Cost: -8%
*   Stability: +3.5%

### Rural Settlement

`COLDWAR_BRA_land_titles` | (0, 14) | 35 days | national

Regularise landholding and expand public extension, accepting conflict and administrative costs.

Requirements: Shared national programme
Prerequisites: (University Research OR Adult Literacy)
Mutually exclusive: Regional Extension

Effects:

* Treasury: -0.4% of payer current GDP, once
* Remove Land and Regional Inequality
*   Agricultural Productivity: +6%
*   Stability: +4%
* Bureaucracy Cost: +4%
* If Landowners are active: Opinion -7

### Regional Extension

`COLDWAR_BRA_extension` | (4, 14) | 35 days | national

Use long-term regional extension and cooperative credit without a general land redistribution.

Requirements: Shared national programme
Prerequisites: (University Research OR Adult Literacy)
Mutually exclusive: Rural Settlement

Effects:

* Treasury: -0.35% of payer current GDP, once
* Remove Land and Regional Inequality
*   Agricultural Productivity: +6%
*   Stability: +4%
* Agricultural Productivity: +3.5%
* Weekly programme expense: 0.1% of payer current annual GDP / 52

### A Wage Bargain

`COLDWAR_BRA_wage_bargain` | (8, 14) | 35 days | national

Replace wage compression with a funded bargaining framework.

Requirements: Shared national programme
Prerequisites: (Serviced Cities)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Remove Wage Compression
*   Consumer Goods Factories: +2.5%
*   Stability: +5%
* Consumer Goods Factories: +2%
* If Labour Unions are active: Opinion +8

### Territorial Offices

`COLDWAR_BRA_territory` | (0, 15) | 35 days | national

Create civil administrative capacity in the eastern Amazon.

Requirements: Shared national programme
Prerequisites: (Rural Settlement OR Regional Extension)
Mutually exclusive: None

Effects:

* Treasury: -0.45% of payer current GDP, once
* Para: +1 shared building slots
* Para: +1 Office

### Frontier Safeguards

`COLDWAR_BRA_frontier_safeguards` | (0, 16) | 35 days | national

Protect indigenous rights and establish project review before frontier expansion.

Requirements: Shared national programme
Prerequisites: (Territorial Offices)
Mutually exclusive: Frontier Administration

Effects:

* Treasury: -0.2% of payer current GDP, once
* Remove A Contested Frontier
*   Bureaucracy Cost: -5%
*   Stability: +3%
* Construction Speed: -2.5%

### Frontier Administration

`COLDWAR_BRA_frontier_admin` | (4, 16) | 35 days | national

Expand permanent civil administration and compensation in the frontier, accepting continuing contestation.

Requirements: Shared national programme
Prerequisites: (Territorial Offices)
Mutually exclusive: Frontier Safeguards

Effects:

* Treasury: -0.3% of payer current GDP, once
* Remove A Contested Frontier
*   Bureaucracy Cost: -5%
*   Stability: +3%
* Weekly programme expense: 0.12% of payer current annual GDP / 52
* Stability: -1.5%

### Public Service Audit

`COLDWAR_BRA_service_audit` | (8, 16) | 35 days | national

Fund professional audits rather than a free nationwide corruption-tier reduction.

Requirements: Shared national programme
Prerequisites: (A Wage Bargain)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: -4%

### A Social Settlement

`COLDWAR_BRA_social_settlement` | (4, 17) | 35 days | national

Maintain a national social settlement with an explicit operating appropriation.

Requirements: Shared national programme
Prerequisites: (Frontier Safeguards OR Frontier Administration) AND (Public Service Audit)
Mutually exclusive: None

Effects:

* Stability: +4%
* Weekly programme expense: 0.08% of payer current annual GDP / 52

## Industry and Agriculture

Development finance, Embraer, Embrapa, the industrial triangle and the export frontier.

### Development Finance

`COLDWAR_BRA_development_bank` | (14, 9) | 35 days | national

Strengthen BNDES project appraisal without adding GDP by decree.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* 1 x 50% Industrial research bonus

### Development Loans

`COLDWAR_BRA_refinance` | (10, 10) | 35 days | national

Replace the initial credit surge with better screened long-term investment.

Requirements: Shared national programme
Prerequisites: (Development Finance)
Mutually exclusive: Export Discipline

Effects:

* Treasury: -0.65% of payer current GDP, once
* Remove Credit-Fuelled Miracle
*   Construction Speed: -8%
*   Factory Output: -4%
*   Interest Rate: -0.5 percentage points
* Interest Rate: -0.4 percentage points
* Construction Speed: +3.5%

### Export Discipline

`COLDWAR_BRA_export_discipline` | (14, 10) | 35 days | national

Reorient development toward export receipts and abandon the initial indiscriminate credit expansion.

Requirements: Shared national programme
Prerequisites: (Development Finance)
Mutually exclusive: Development Loans

Effects:

* Remove Credit-Fuelled Miracle
*   Construction Speed: -8%
*   Factory Output: -4%
*   Interest Rate: -0.5 percentage points
* Resource Export Income: +10%
* Stability: -2.5%

### Industrial Triangle

`COLDWAR_BRA_industrial_triangle` | (18, 10) | 35 days | national

Expand São Paulo and Minas Gerais manufacturing with matched building slots.

Requirements: Shared national programme
Prerequisites: (Development Finance)
Mutually exclusive: None

Effects:

* Treasury: -0.9% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Civilian Factory
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Civilian Factory

### Tropical Agronomy

`COLDWAR_BRA_embrapa` | (12, 11) | 35 days | national

Create or expand the agricultural research institution represented historically by Embrapa in 1973. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Development Loans OR Export Discipline)
Mutually exclusive: None

Effects:

* Treasury: -0.35% of payer current GDP, once
* 2 x 50% Agricultural research bonus

### Capital Goods

`COLDWAR_BRA_capital_goods` | (18, 11) | 35 days | national

Fund capital-goods manufacturing rather than importing a modern production line for free.

Requirements: Shared national programme
Prerequisites: (Industrial Triangle)
Mutually exclusive: None

Effects:

* Treasury: -0.65% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Civilian Factory

### Cerrado Agribusiness

`COLDWAR_BRA_cerrado` | (10, 12) | 35 days | national

Combine tropical agronomy with large-scale commercial farming and acknowledge land concentration.

Requirements: Shared national programme
Prerequisites: (Tropical Agronomy)
Mutually exclusive: Smallholder Research

Effects:

* Treasury: -0.6% of payer current GDP, once
* Goias: +1 shared building slots
* Goias: +1 Agriculture District
* Agricultural Productivity: +7%
* Stability: -2.5%

### Smallholder Research

`COLDWAR_BRA_smallholder` | (14, 12) | 35 days | national

Direct extension and credit toward smaller farmers with a larger service bill.

Requirements: Shared national programme
Prerequisites: (Tropical Agronomy)
Mutually exclusive: Cerrado Agribusiness

Effects:

* Treasury: -0.4% of payer current GDP, once
* Pernambuco: +1 shared building slots
* Pernambuco: +1 Agriculture District
* Agricultural Productivity: +4%
* Weekly programme expense: 0.08% of payer current annual GDP / 52

### Licensed Tooling

`COLDWAR_BRA_licensed_tools` | (16, 12) | 35 days | national

Licence production equipment while accepting recurrent fees and dependence.

Requirements: Shared national programme
Prerequisites: (Capital Goods)
Mutually exclusive: National Tooling

Effects:

* 2 x 50% Industrial research bonus
* Weekly programme expense: 0.1% of payer current annual GDP / 52
* Foreign Influence Defence: -3.5%

### National Tooling

`COLDWAR_BRA_national_tools` | (20, 12) | 35 days | national

Prioritise a national tooling base with a narrower technology pool.

Requirements: Shared national programme
Prerequisites: (Capital Goods)
Mutually exclusive: Licensed Tooling

Effects:

* Treasury: -0.45% of payer current GDP, once
* Production Efficiency Cap: +6%
* Research Speed: -2.5%

### Storage and Markets

`COLDWAR_BRA_storage` | (12, 13) | 35 days | national

Link food-producing districts to storage and wholesale markets.

Requirements: Shared national programme
Prerequisites: (Cerrado Agribusiness OR Smallholder Research)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Mato Grosso: +1 shared building slots
* Mato Grosso: +1 Infrastructure

### Industrial Standards

`COLDWAR_BRA_industrial_standards` | (18, 13) | 35 days | national

Create standards and quality-control capacity for national manufacturers.

Requirements: Shared national programme
Prerequisites: (Licensed Tooling OR National Tooling)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Production Efficiency Growth: +5%

### Manaus Industry

`COLDWAR_BRA_manaus` | (10, 14) | 35 days | national

Expand the Manaus zone through real facilities and explicit tax concessions.

Requirements: Shared national programme
Prerequisites: (Storage and Markets)
Mutually exclusive: Northeast Industry

Effects:

* Treasury: -0.7% of payer current GDP, once
* Amazonas: +1 shared building slots
* Amazonas: +1 Civilian Factory
* Corporate Tax Income: -2.5%

### Northeast Industry

`COLDWAR_BRA_regional_industry` | (14, 14) | 35 days | national

Fund northeastern industry and the administrative support it requires.

Requirements: Shared national programme
Prerequisites: (Storage and Markets)
Mutually exclusive: Manaus Industry

Effects:

* Treasury: -0.7% of payer current GDP, once
* Bahia: +1 shared building slots
* Bahia: +1 Civilian Factory
* Weekly programme expense: 0.06% of payer current annual GDP / 52

### Embraer Production

`COLDWAR_BRA_embraer` | (18, 14) | 35 days | national

Expand aircraft manufacturing from Embraer’s 1969 foundations, funding production capacity and aeronautical research.

Requirements: Shared national programme
Prerequisites: (Industrial Standards)
Mutually exclusive: None

Effects:

* Treasury: -0.75% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Military Factory
* 1 x 50% Aircraft research bonus

### Telecommunications

`COLDWAR_BRA_telebras` | (14, 15) | 35 days | national

Expand the national telecommunications institution, represented by offices and period electronics research.

Requirements: Shared national programme
Prerequisites: (Manaus Industry OR Northeast Industry)
Mutually exclusive: None

Effects:

* Treasury: -0.55% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Office
* 1 x 50% Electronics research bonus

### Export Offices

`COLDWAR_BRA_trade_fairs` | (18, 15) | 35 days | national

Fund technical export offices and quality promotion to strengthen productive firms and their commercial networks.

Requirements: Shared national programme
Prerequisites: (Embraer Production)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Productivity Growth: +3.5%
* Weekly programme expense: 0.04% of payer current annual GDP / 52

### A Productive Nation

`COLDWAR_BRA_productive_nation` | (14, 16) | 35 days | national

Coordinate productive institutions through a funded national programme.

Requirements: Shared national programme
Prerequisites: (Telecommunications) AND (Export Offices)
Mutually exclusive: None

Effects:

* Production Efficiency Cap: +4%
* Weekly programme expense: 0.08% of payer current annual GDP / 52

## Energy and Resources

Imported oil, Petrobras, hydroelectricity, alcohol fuels, civil nuclear work and paid mineral development.

### Energy Balance

`COLDWAR_BRA_energy_balance` | (26, 9) | 35 days | national

Measure industrial demand and imported-fuel exposure before choosing major investments.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* 1 x 50% Energy research bonus

### Offshore Petrobras

`COLDWAR_BRA_offshore` | (22, 10) | 35 days | national

Fund offshore exploration and refining expertise without granting unverified state oil deposits.

Requirements: Shared national programme
Prerequisites: (Energy Balance)
Mutually exclusive: Efficient Energy Use

Effects:

* Treasury: -0.8% of payer current GDP, once
* 1 x 50% Excavation research bonus
* Fuel Gain: +5%
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Efficient Energy Use

`COLDWAR_BRA_conservation` | (26, 10) | 35 days | national

Prioritise conservation and retrofitting rather than rapid supply expansion.

Requirements: Shared national programme
Prerequisites: (Energy Balance)
Mutually exclusive: Offshore Petrobras

Effects:

* Treasury: -0.35% of payer current GDP, once
* 2 x 50% Energy Efficiency research bonus
* Construction Speed: -2.5%

### Regional Power Grid

`COLDWAR_BRA_grid` | (30, 10) | 35 days | national

Extend the regional power grid to carry growing industrial and urban demand.

Requirements: Shared national programme
Prerequisites: (Energy Balance)
Mutually exclusive: None

Effects:

* Treasury: -0.7% of payer current GDP, once
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Infrastructure

### Fuel Security

`COLDWAR_BRA_fuel_security` | (24, 11) | 35 days | national

Complete storage and substitution measures that remove initial energy vulnerability.

Requirements: Shared national programme
Prerequisites: (Offshore Petrobras OR Efficient Energy Use)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Remove Imported Energy Dependence
*   Fuel Gain: +8%
*   Inflation Cost: -3%
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Fuel Silo

### Domestic Hydropower

`COLDWAR_BRA_hydro` | (30, 11) | 35 days | national

Build domestic hydroelectric capacity and its operating institutions. Cross-border Itaipu development requires a separate agreement with Paraguay.

Requirements: Shared national programme
Prerequisites: (Regional Power Grid)
Mutually exclusive: None

Effects:

* Treasury: -1% of payer current GDP, once
* Parana: +1 shared building slots
* Parana: Start construction: +1 Renewable Energy Infrastructure
* Weekly programme expense: 0.08% of payer current annual GDP / 52

### Alcohol Fuels

`COLDWAR_BRA_proalcool` | (22, 12) | 35 days | national

Use the 1975 Proalcool precedent. Fuel security competes with land and food-sector capacity. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Fuel Security)
Mutually exclusive: Conventional Refining

Effects:

* Treasury: -0.6% of payer current GDP, once
* Fuel Gain: +10%
* Agricultural Productivity: -3%
* Weekly programme expense: 0.12% of payer current annual GDP / 52

### Conventional Refining

`COLDWAR_BRA_refining` | (26, 12) | 35 days | national

Expand native refinery capacity while retaining imported-feedstock exposure in public costs.

Requirements: Shared national programme
Prerequisites: (Fuel Security)
Mutually exclusive: Alcohol Fuels

Effects:

* Treasury: -0.7% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Synthetic Refinery
* Inflation Cost: +2.5%

### Civil Nuclear Science

`COLDWAR_BRA_nuclear_science` | (30, 12) | 35 days | national

Develop civilian reactor knowledge without granting a bomb or a free reactor.

Requirements: Shared national programme
Prerequisites: (Domestic Hydropower)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* 2 x 50% Civil Nuclear research bonus

### Mineral Survey

`COLDWAR_BRA_mineral_survey` | (24, 13) | 35 days | national

Survey known mineral prospects and fund feasibility work. Extraction requires a separately financed mine-development project.

Requirements: Shared national programme
Prerequisites: (Alcohol Fuels OR Conventional Refining)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* 1 x 50% Excavation research bonus
* Commission a Uranium Feasibility Study

### Reactor Programme

`COLDWAR_BRA_reactor` | (28, 13) | 35 days | national

Build one civilian reactor through a major funded programme with normal native fuel and operating requirements.

Requirements: has_tech = reactor1
Prerequisites: (Civil Nuclear Science)
Mutually exclusive: Diverse Generation

Effects:

* Treasury: -1.5% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: Start construction: +1 Nuclear Reactor
* Weekly programme expense: 0.2% of payer current annual GDP / 52

### Diverse Generation

`COLDWAR_BRA_grid_diversity` | (32, 13) | 35 days | national

Choose domestic generation diversity instead of the reactor works.

Requirements: Shared national programme
Prerequisites: (Civil Nuclear Science)
Mutually exclusive: Reactor Programme

Effects:

* Treasury: -0.9% of payer current GDP, once
* Bahia: +1 shared building slots
* Bahia: +1 Renewable Energy Infrastructure
* 1 x 50% Energy Efficiency research bonus

### Carajas Logistics

`COLDWAR_BRA_carajas` | (24, 14) | 35 days | national

Fund logistics around the known Carajás mineral frontier. The revenue modifier requires actual exported steel resources.

Requirements: Shared national programme
Prerequisites: (Mineral Survey)
Mutually exclusive: None

Effects:

* Treasury: -0.8% of payer current GDP, once
* Para: +1 shared building slots
* Para: +1 Infrastructure
* Steel Export Income: +8%
* Weekly programme expense: 0.06% of payer current annual GDP / 52

### Resource Standards

`COLDWAR_BRA_resource_standards` | (30, 14) | 35 days | national

Fund technical standards, geological services and the institutions that manage mineral sales.

Requirements: Shared national programme
Prerequisites: (Reactor Programme OR Diverse Generation)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Bureaucracy Cost: +2.5%
* Resource Export Income: +4%

### Energy Resilience

`COLDWAR_BRA_energy_resilience` | (26, 15) | 35 days | national

Maintain a diversified energy and resource system against external cost shocks.

Requirements: Shared national programme
Prerequisites: (Carajas Logistics) AND (Resource Standards)
Mutually exclusive: None

Effects:

* Inflation Cost: -3.5%
* Weekly programme expense: 0.06% of payer current annual GDP / 52

### Power Dispatch

`COLDWAR_BRA_energy_dispatch` | (26, 16) | 35 days | national

Coordinate supply dispatch and resource contracts through a concrete administrative facility.

Requirements: Shared national programme
Prerequisites: (Energy Resilience)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* Goias: +1 shared building slots
* Goias: +1 Office

## Armed Services

A credible regional force with domestic production, training and explicit procurement trade-offs. No starting OOB changes.

### Joint Staff Review

`COLDWAR_BRA_joint_staff` | (38, 9) | 35 days | national

Review force requirements across services before selecting new commitments.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Army experience: +25
* Navy experience: +25
* Air experience: +25

### Territorial Army

`COLDWAR_BRA_territorial` | (34, 10) | 35 days | national

Prioritise a broad territorial army with an appropriate personnel burden.

Requirements: Shared national programme
Prerequisites: (Joint Staff Review)
Mutually exclusive: Professional Cadres

Effects:

* Army Organisation: +6%
* Army Personnel Cost: +8%

### Professional Cadres

`COLDWAR_BRA_professional` | (38, 10) | 35 days | national

Concentrate on trained cadres and maintenance while reducing equipment waste.

Requirements: Shared national programme
Prerequisites: (Joint Staff Review)
Mutually exclusive: Territorial Army

Effects:

* Army Organisation: +3.5%
* Equipment Cost: -6%
* Military Spending Cost: +3.5%

### Flying Schools

`COLDWAR_BRA_air_training` | (42, 10) | 35 days | national

Expand flying instruction before committing to new airframes.

Requirements: Shared national programme
Prerequisites: (Joint Staff Review)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* 1 x 50% Aircraft research bonus
* Air experience: +35

### Small Arms Industry

`COLDWAR_BRA_imbel` | (36, 11) | 35 days | national

Develop national small-arms production using the later IMBEL consolidation as a precedent.

Requirements: Shared national programme
Prerequisites: (Territorial Army OR Professional Cadres)
Mutually exclusive: None

Effects:

* Treasury: -0.65% of payer current GDP, once
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Military Factory

### Flight Safety

`COLDWAR_BRA_air_safety` | (42, 11) | 35 days | national

Fund safety instruction and maintenance with a larger skilled-personnel bill.

Requirements: Shared national programme
Prerequisites: (Flying Schools)
Mutually exclusive: None

Effects:

* Air Accident Chance: -10%
* Air Force Personnel Cost: +5%

### Jungle School

`COLDWAR_BRA_jungle` | (34, 12) | 35 days | national

Fund jungle communications, field instruction and staff exercises for Brazil’s difficult interior terrain.

Requirements: Shared national programme
Prerequisites: (Small Arms Industry)
Mutually exclusive: Vehicle Workshops

Effects:

* Treasury: -0.25% of payer current GDP, once
* Army experience: +40
* 1 x 25% Electronics research bonus

### Vehicle Workshops

`COLDWAR_BRA_mechanised` | (38, 12) | 35 days | national

Expand vehicle workshops with an explicit cost for domestic production depth.

Requirements: Shared national programme
Prerequisites: (Small Arms Industry)
Mutually exclusive: Jungle School

Effects:

* Treasury: -0.6% of payer current GDP, once
* Sao Paulo: +1 shared building slots
* Sao Paulo: +1 Military Factory
* Equipment Cost: +3.5%

### Tactical Air Support

`COLDWAR_BRA_air_support` | (40, 12) | 35 days | national

Build a tactical-support air service with the required specialist staff.

Requirements: Shared national programme
Prerequisites: (Flight Safety)
Mutually exclusive: Airspace Defence

Effects:

* Air Mission Efficiency: +6%
* Air Force Personnel Cost: +6%

### Airspace Defence

`COLDWAR_BRA_air_defence` | (44, 12) | 35 days | national

Develop domestic airspace defence through basing and training.

Requirements: Shared national programme
Prerequisites: (Flight Safety)
Mutually exclusive: Tactical Air Support

Effects:

* Treasury: -0.4% of payer current GDP, once
* Goias: +1 shared building slots
* Goias: +1 Air Base
* Air experience: +30

### Naval Workshops

`COLDWAR_BRA_naval_yards` | (36, 13) | 35 days | national

Expand naval workshops in Rio without granting completed ships.

Requirements: Shared national programme
Prerequisites: (Jungle School OR Vehicle Workshops)
Mutually exclusive: None

Effects:

* Treasury: -0.8% of payer current GDP, once
* Rio de Janeiro: +1 shared building slots
* Rio de Janeiro: +1 Naval Dockyard

### Joint Exercises

`COLDWAR_BRA_joint_exercises` | (42, 13) | 35 days | national

Fund joint planning and exercises across services.

Requirements: Shared national programme
Prerequisites: (Tactical Air Support OR Airspace Defence)
Mutually exclusive: None

Effects:

* Treasury: -0.2% of payer current GDP, once
* Army experience: +25
* Air experience: +25

### Oceanic Fleet

`COLDWAR_BRA_ocean_fleet` | (34, 14) | 35 days | national

Maintain an oceanic fleet with a large specialist and operating burden.

Requirements: Shared national programme
Prerequisites: (Naval Workshops)
Mutually exclusive: Coastal Escort Fleet

Effects:

* Naval Organisation: +8%
* Navy Personnel Cost: +12%
* Weekly programme expense: 0.1% of payer current annual GDP / 52

### Coastal Escort Fleet

`COLDWAR_BRA_coastal_fleet` | (38, 14) | 35 days | national

Prioritise cheaper escort production over the cohesion of a broader blue-water force.

Requirements: Shared national programme
Prerequisites: (Naval Workshops)
Mutually exclusive: Oceanic Fleet

Effects:

* Dockyard Output: +8%
* Naval Organisation: -3%

### Procurement Office

`COLDWAR_BRA_procurement` | (42, 14) | 35 days | national

Standardise procurement through a funded contracting office.

Requirements: Shared national programme
Prerequisites: (Joint Exercises)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Equipment Cost: -5%
* Bureaucracy Cost: +2.5%

### Rocket Engineering

`COLDWAR_BRA_avibras` | (36, 15) | 35 days | national

Develop national guidance and electronics expertise without a free later ASTROS stockpile.

Requirements: Shared national programme
Prerequisites: (Oceanic Fleet OR Coastal Escort Fleet)
Mutually exclusive: None

Effects:

* Treasury: -0.5% of payer current GDP, once
* 1 x 50% Electronics research bonus
* Army experience: +20

### Defence Export Office

`COLDWAR_BRA_exports_arms` | (42, 15) | 35 days | national

Support export-oriented defence production while accepting foreign market dependence.

Requirements: Shared national programme
Prerequisites: (Procurement Office)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Factory Output: +3.5%
* Foreign Influence Defence: -2.5%

### A Regional Force

`COLDWAR_BRA_regional_force` | (38, 16) | 35 days | national

Maintain a balanced regional force through an explicit staff and readiness budget.

Requirements: Shared national programme
Prerequisites: (Rocket Engineering) AND (Defence Export Office)
Mutually exclusive: None

Effects:

* Army Organisation: +2.5%
* Weekly programme expense: 0.08% of payer current annual GDP / 52

## Itamaraty and RP Agreements

Distinct national-focus offers, real recipient decisions, complete prospective two-country rewards and permanent conditional agreements.

### Itamaraty Review

`COLDWAR_BRA_itamaraty` | (58, 9) | 35 days | national

Define practical diplomatic priorities without committing any foreign player.

Requirements: Shared national programme
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* Bureaucracy Cost: +2.5%

### Atlantic Continuity

`COLDWAR_BRA_atlantic` | (52, 10) | 35 days | national

Prioritise established Atlantic commercial and technical links.

Requirements: Shared national programme
Prerequisites: (Itamaraty Review)
Mutually exclusive: Pragmatic Diplomacy

Effects:

* Research Speed: +2.5%
* Foreign Influence Defence: -4%

### Pragmatic Diplomacy

`COLDWAR_BRA_pragmatism` | (58, 10) | 35 days | national

Diversify diplomatic partners despite domestic anticommunist opposition.

Requirements: Shared national programme
Prerequisites: (Itamaraty Review)
Mutually exclusive: Atlantic Continuity

Effects:

* Resource Export Income: +5%
* Political Power Gain: -3.5%

### Regional Diplomacy

`COLDWAR_BRA_regional` | (64, 10) | 35 days | national

Reduce regional rivalry through negotiation while preserving recipient choice.

Requirements: Shared national programme
Prerequisites: (Itamaraty Review)
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* Stability: +2.5%

### US Training Mission

`COLDWAR_BRA_us_training` | (50, 11) | 35 days | treaty

Negotiate training and technical cooperation. The 1977 human-rights dispute remains a later event.

Requirements: Shared national programme
Prerequisites: (Atlantic Continuity)
Mutually exclusive: US Industrial Licences

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: US Training Mission**

* Treasury: -0.25% of payer current GDP, once
* Weekly programme expense: 0.06% of payer current annual GDP / 52
* Army Organisation: +4%
* Foreign Influence Defence: -4%
* Army experience: +30

**United States: US Training Mission**

* Treasury: -0.04% of payer current GDP, once
* Weekly programme expense: 0.015% of payer current annual GDP / 52
* Army Organisation: +1.5%
* Army experience: +15


### US Industrial Licences

`COLDWAR_BRA_us_industry` | (54, 11) | 35 days | treaty

Negotiate industrial licensing rather than assume foreign technology is available.

Requirements: Shared national programme
Prerequisites: (Atlantic Continuity)
Mutually exclusive: US Training Mission

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: US Industrial Licences**

* Treasury: -0.4% of payer current GDP, once
* Weekly programme expense: 0.08% of payer current annual GDP / 52
* Production Efficiency Growth: +6%
* Foreign Influence Defence: -5%
* 1 x 50% Industrial research bonus

**United States: US Industrial Licences**

* Treasury: -0.05% of payer current GDP, once
* Weekly programme expense: 0.015% of payer current annual GDP / 52
* Productivity Growth: +1.5%
* 1 x 25% Industrial research bonus


### China Trade Mission

`COLDWAR_BRA_china_trade` | (58, 11) | 35 days | treaty

Build a trade relationship from the 1974 recognition precedent. Early mutual recognition is explicit alternative diplomacy.

Requirements: Shared national programme
Prerequisites: (Pragmatic Diplomacy)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: China Trade Mission**

* Treasury: -0.15% of payer current GDP, once
* Weekly programme expense: 0.035% of payer current annual GDP / 52
* Resource Export Income: +7%
* Political Power Gain: -2.5%

**China: China Trade Mission**

* Treasury: -0.08% of payer current GDP, once
* Weekly programme expense: 0.025% of payer current annual GDP / 52
* Resource Export Income: +4%
* Bureaucracy Cost: +1.5%


### Soviet Machinery

`COLDWAR_BRA_ussr_machines` | (62, 11) | 35 days | treaty

Exchange agricultural trade access and machinery expertise on the model of the 1975 agreement.

Requirements: Shared national programme
Prerequisites: (Pragmatic Diplomacy)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Soviet Machinery**

* Treasury: -0.25% of payer current GDP, once
* Weekly programme expense: 0.06% of payer current annual GDP / 52
* 2 x 50% Industrial research bonus
* Resource Export Income: +5%
* Foreign Influence Defence: -3%

**Soviet Union: Soviet Machinery**

* Treasury: -0.08% of payer current GDP, once
* Weekly programme expense: 0.025% of payer current annual GDP / 52
* 1 x 50% Agricultural research bonus
* Resource Export Income: +3.5%


### Itaipu Proposal

`COLDWAR_BRA_itaipu` | (66, 11) | 35 days | treaty

Negotiate a binational capacity project from the 1973 treaty precedent. Each funds its own GDP share. Brazil also makes an RP financial-support payment to Paraguay; this is not the historical Itaipu royalty formula or a promise of physical electricity delivery. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Regional Diplomacy)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Itaipu Proposal**

* Treasury: -1.5% of payer current GDP, once
* Weekly programme expense: 0.18% of payer current annual GDP / 52
* Parana: +1 shared building slots
* Parana: Start construction: +1 Renewable Energy Infrastructure
* Inflation Cost: -2.5%
* Weekly expense: 0.08% of BRA current GDP / 52, paid to PAR

**Paraguay: Itaipu Proposal**

* Treasury: -0.65% of payer current GDP, once
* Weekly programme expense: 0.12% of payer current annual GDP / 52
* Paraguay: +1 shared building slots
* Paraguay: Start construction: +1 Renewable Energy Infrastructure
* Inflation Cost: -2.5%
* Weekly income: 0.08% of BRA current GDP / 52, paid to PAR


### Cerrado Cooperation

`COLDWAR_BRA_japan_agro` | (52, 12) | 35 days | treaty

Negotiate agronomy, finance and extension from the PRODECER precedent, with land pressures made visible. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Pacific Commerce)
Mutually exclusive: Japan Steel Pact

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Cerrado Cooperation**

* Treasury: -0.45% of payer current GDP, once
* Weekly programme expense: 0.08% of payer current annual GDP / 52
* Agricultural Productivity: +6%
* 1 x 50% Agricultural research bonus
* Stability: -2%

**Japan: Cerrado Cooperation**

* Treasury: -0.08% of payer current GDP, once
* Weekly programme expense: 0.025% of payer current annual GDP / 52
* 1 x 50% Agricultural research bonus
* Productivity Growth: +1.5%


### Japan Steel Pact

`COLDWAR_BRA_japan_steel` | (56, 12) | 35 days | treaty

Use joint industrial investment and long-term market access rather than an automatic foreign resource concession. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Pacific Commerce)
Mutually exclusive: Cerrado Cooperation

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Japan Steel Pact**

* Treasury: -0.75% of payer current GDP, once
* Weekly programme expense: 0.1% of payer current annual GDP / 52
* Minas Gerais: +1 shared building slots
* Minas Gerais: +1 Civilian Factory
* Steel Export Income: +5%

**Japan: Japan Steel Pact**

* Treasury: -0.1% of payer current GDP, once
* Weekly programme expense: 0.035% of payer current annual GDP / 52
* 1 x 50% Industrial research bonus
* Production Efficiency Growth: +2.5%


### Angola Technical Pact

`COLDWAR_BRA_angola` | (60, 12) | 35 days | treaty

Offer technical cooperation after independence and recognition. This does not grant Angola’s oil to Brazil.

Requirements: Angola is independent and recognised
Prerequisites: (China Trade Mission)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Angola Technical Pact**

* Treasury: -0.12% of payer current GDP, once
* Weekly programme expense: 0.04% of payer current annual GDP / 52
* Productivity Growth: +1.5%
* Bureaucracy Cost: +1.5%

**Angola: Angola Technical Pact**

* Treasury: -0.15% of payer current GDP, once
* Weekly programme expense: 0.06% of payer current annual GDP / 52
* 1 x 50% Industrial research bonus
* Construction Speed: +3.5%
* Foreign Influence Defence: -3%


### River Consultations

`COLDWAR_BRA_arg_basin` | (64, 12) | 35 days | treaty

Negotiate bilateral river-project consultation, inspired by the conflict resolved in 1979. This RP agreement is not the historical tripartite Itaipu-Corpus settlement and cannot bind Paraguay.

Requirements: Active Brazil-Paraguay Itaipu agreement
Prerequisites: (Itaipu Proposal)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: River Consultations**

* Treasury: -0.2% of payer current GDP, once
* Weekly programme expense: 0.035% of payer current annual GDP / 52
* Construction Speed: +3.5%
* Bureaucracy Cost: +2%

**Argentina: River Consultations**

* Treasury: -0.2% of payer current GDP, once
* Weekly programme expense: 0.035% of payer current annual GDP / 52
* Construction Speed: +3.5%
* Bureaucracy Cost: +2%


### German Nuclear Pact

`COLDWAR_BRA_germany_nuclear` | (46, 12) | 35 days | treaty

Negotiate civilian technology cooperation using the 1975 treaty as a precedent. Reactor construction, fuel procurement and mineral development require separate investment. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Technical Diplomacy)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: German Nuclear Pact**

* Treasury: -0.9% of payer current GDP, once
* Weekly programme expense: 0.15% of payer current annual GDP / 52
* 2 x 50% Civil Nuclear research bonus
* Nuclear Reactor Construction Speed: +8%
* Foreign Influence Defence: -4%

**Federal Republic of Germany: German Nuclear Pact**

* Treasury: -0.12% of payer current GDP, once
* Weekly programme expense: 0.04% of payer current annual GDP / 52
* 1 x 50% Civil Nuclear research bonus
* Factory Output: +2%


### Nuclear Transparency

`COLDWAR_BRA_nuclear_dialogue` | (68, 12) | 35 days | national

Explore civilian nuclear confidence-building independently of river disputes or a German treaty.

Requirements: Shared national programme
Prerequisites: (Regional Commerce)
Mutually exclusive: None

Effects:

* Treasury: -0.15% of payer current GDP, once
* 1 x 25% Civil Nuclear research bonus

### Nuclear Confidence

`COLDWAR_BRA_arg_nuclear` | (68, 13) | 35 days | treaty

Negotiate mutual civilian nuclear transparency using the 1980 cooperation and 1985 confidence-building precedents. An earlier programme is an alternative to the historical sequence.

Requirements: Shared national programme
Prerequisites: (Nuclear Transparency)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Nuclear Confidence**

* Treasury: -0.3% of payer current GDP, once
* Weekly programme expense: 0.06% of payer current annual GDP / 52
* 1 x 50% Civil Nuclear research bonus
* Research Speed: +2.5%
* Bureaucracy Cost: +2.5%

**Argentina: Nuclear Confidence**

* Treasury: -0.3% of payer current GDP, once
* Weekly programme expense: 0.06% of payer current annual GDP / 52
* 1 x 50% Civil Nuclear research bonus
* Research Speed: +2.5%
* Bureaucracy Cost: +2.5%


### Industrial Protocol

`COLDWAR_BRA_arg_integration` | (62, 13) | 35 days | treaty

Negotiate an industrial integration protocol using the 1986 programme as a precedent. Any earlier signature represents an alternative regional initiative.

Requirements: Shared national programme
Prerequisites: (Industrial Talks)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Industrial Protocol**

* Treasury: -0.45% of payer current GDP, once
* Weekly programme expense: 0.08% of payer current annual GDP / 52
* Production Efficiency Growth: +5%
* Bureaucracy Cost: +2.5%
* 1 x 50% Industrial research bonus

**Argentina: Industrial Protocol**

* Treasury: -0.45% of payer current GDP, once
* Weekly programme expense: 0.08% of payer current annual GDP / 52
* Production Efficiency Growth: +5%
* Bureaucracy Cost: +2.5%
* 1 x 50% Industrial research bonus


### Uruguay Port Protocol

`COLDWAR_BRA_uruguay` | (60, 14) | 35 days | treaty

Negotiate port administration and commercial cooperation as a plausible period RP protocol.

Requirements: Shared national programme
Prerequisites: (Industrial Protocol)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Uruguay Port Protocol**

* Treasury: -0.2% of payer current GDP, once
* Weekly programme expense: 0.04% of payer current annual GDP / 52
* Resource Export Income: +4.5%
* Bureaucracy Cost: +2%

**Uruguay: Uruguay Port Protocol**

* Treasury: -0.3% of payer current GDP, once
* Weekly programme expense: 0.055% of payer current annual GDP / 52
* Uruguay (Rio de la Plata): +1 shared building slots
* Uruguay (Rio de la Plata): +1 Office
* Resource Export Income: +4%


### Mirage Partnership

`COLDWAR_BRA_france_aircraft` | (50, 12) | 35 days | treaty

Negotiate Mirage III training, maintenance and technical cooperation from the 1970 procurement precedent.

Requirements: Shared national programme
Prerequisites: (Technical Diplomacy)
Mutually exclusive: None

Effects:

* No direct payout. Recipient offer only.

If they accept:

**Brazil: Mirage Partnership**

* Treasury: -0.5% of payer current GDP, once
* Weekly programme expense: 0.08% of payer current annual GDP / 52
* 2 x 50% Aircraft research bonus
* Air Mission Efficiency: +2.5%
* Foreign Influence Defence: -3.5%

**France: Mirage Partnership**

* Treasury: -0.08% of payer current GDP, once
* Weekly programme expense: 0.025% of payer current annual GDP / 52
* 1 x 50% Aircraft research bonus
* Production Efficiency Growth: +2%


### Regional Secretariat

`COLDWAR_BRA_regional_secretariat` | (58, 15) | 35 days | national

Maintain a consultative regional secretariat for the signed commercial protocols.

Requirements: Shared national programme
Prerequisites: (Uruguay Port Protocol)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Goias: +1 shared building slots
* Goias: +1 Office
* Weekly programme expense: 0.05% of payer current annual GDP / 52

### Technical Diplomacy

`COLDWAR_BRA_technical_desk` | (46, 11) | 35 days | national

Fund a technical negotiating desk for independent European industrial and aviation proposals.

Requirements: Shared national programme
Prerequisites: (Atlantic Continuity OR Pragmatic Diplomacy)
Mutually exclusive: None

Effects:

* Treasury: -0.12% of payer current GDP, once
* 1 x 25% Electronics research bonus

### Pacific Commerce

`COLDWAR_BRA_pacific_desk` | (56, 11) | 35 days | national

Prepare Japanese commercial and agricultural negotiations independently of any US agreement.

Requirements: Shared national programme
Prerequisites: (Atlantic Continuity OR Pragmatic Diplomacy)
Mutually exclusive: None

Effects:

* Treasury: -0.12% of payer current GDP, once
* 1 x 25% Agricultural research bonus

### Regional Commerce

`COLDWAR_BRA_commercial_desk` | (64, 11) | 35 days | national

Prepare regional industrial negotiations independently of nuclear or river treaties.

Requirements: Shared national programme
Prerequisites: (Regional Diplomacy)
Mutually exclusive: None

Effects:

* Treasury: -0.12% of payer current GDP, once
* 1 x 25% Industrial research bonus

### Industrial Talks

`COLDWAR_BRA_industrial_talks` | (62, 12) | 35 days | national

Draft industrial terms for Argentina without making a nuclear agreement compulsory.

Requirements: Shared national programme
Prerequisites: (Regional Commerce)
Mutually exclusive: None

Effects:

* Treasury: -0.12% of payer current GDP, once
* 1 x 25% Industrial research bonus

## PTB

The later PTB won its own registration and name during the 1979/80 reorganisation. It is not the old party or the PDT renamed.

### A Labour Coalition

`COLDWAR_BRA_ptb_late_0` | (90, 0) | 35 days | government

Build the later PTB as its own labour and regional coalition, distinct from Brizola’s PDT and the dissolved old PTB.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: None
Mutually exclusive: None

Effects:

* Treasury: -0.18% of payer current GDP, once
* Political Power Gain: +6%
* Bureaucracy Cost: +4%

### Employer Compact

`COLDWAR_BRA_ptb_late_1` | (88, 1) | 35 days | government

Support production through an employer-oriented compact at a cost in union confidence.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (A Labour Coalition)
Mutually exclusive: Union Agreements

Effects:

* Factory Output: +6%
* If Labour Unions are active: Opinion -6

### Union Agreements

`COLDWAR_BRA_ptb_late_2` | (92, 1) | 35 days | government

Negotiate labour protections while accepting resistance from larger employers.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (A Labour Coalition)
Mutually exclusive: Employer Compact

Effects:

* Stability: +5.5%
* If Industrial Conglomerates are active: Opinion -6
* Social Spending Cost: +3%

### Benefit Administration

`COLDWAR_BRA_ptb_late_3` | (90, 2) | 35 days | government

Fund professional benefit administration rather than promise unfunded social rights.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Employer Compact OR Union Agreements)
Mutually exclusive: None

Effects:

* Treasury: -0.25% of payer current GDP, once
* Bureaucracy Cost: +3.5%
* Stability: +2.5%

### Vocational Training

`COLDWAR_BRA_ptb_late_4` | (88, 3) | 35 days | government

Expand practical training through the labour and industrial institutions.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Benefit Administration)
Mutually exclusive: None

Effects:

* Treasury: -0.3% of payer current GDP, once
* 1 x 50% Industrial research bonus

### Regional Employers

`COLDWAR_BRA_ptb_late_5` | (92, 3) | 35 days | government

Provide commercial and labour administration for smaller regional employers.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Benefit Administration)
Mutually exclusive: None

Effects:

* Treasury: -0.4% of payer current GDP, once
* Bahia: +1 shared building slots
* Bahia: +1 Office

### Workplace Compact

`COLDWAR_BRA_ptb_late_6` | (90, 4) | 35 days | government

Replace wage compression through a negotiated wage and employment settlement.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Vocational Training) AND (Regional Employers)
Mutually exclusive: None

Effects:

* Remove Wage Compression
*   Consumer Goods Factories: +2.5%
*   Stability: +5%
* Consumer Goods Factories: +2%

### Social Protection

`COLDWAR_BRA_ptb_late_7` | (88, 5) | 35 days | government

Expand protection with a clearly visible public-service bill.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Workplace Compact)
Mutually exclusive: Employment Credit

Effects:

* Stability: +5%
* Social Spending Cost: +7%

### Employment Credit

`COLDWAR_BRA_ptb_late_8` | (92, 5) | 35 days | government

Protect hiring and investment through credit, accepting greater financing exposure.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Workplace Compact)
Mutually exclusive: Social Protection

Effects:

* Construction Speed: +5%
* Interest Rate: +0.4 percentage points

### Coalition Guarantees

`COLDWAR_BRA_ptb_late_9` | (90, 6) | 35 days | government

Make labour policy answerable to a working parliamentary coalition.

Requirements: western_social_democrats_are_in_power = yes; Governing party identity: Later PTB, separate registration required
Prerequisites: (Social Protection OR Employment Credit)
Mutually exclusive: None

Effects:

* Stability: +3%
* Political Power Gain: -3%

# Event options

## The Officer Council

The services dispute the balance between command authority and specialist administration.

Policy duration: government

### Protect the command hierarchy

* Army Organisation: +4%
* Political Power Gain: -4%

### Bring civilian specialists into cabinet

* Research Speed: +3%
* Bureaucracy Cost: +4%

## The Constitutional Settlement

A constituent coalition must settle the balance between social guarantees and executive authority.

Policy duration: national

### Strengthen social guarantees

* Stability: +6%
* Social Spending Cost: +6%

### Prioritise governability

* Political Power Gain: +7%
* Stability: -3%

## The Party Reorganisation

Reorganisation opens political competition. Specific parties require their genuine organisation and identity, rather than a forced ideological conversion.

Policy duration: national

### Register competing civilian organisations

* Political Power Gain: -4%
* Stability: +4%

### Negotiate a limited transition

* Stability: +2%
* If The Military are active: Opinion +5

## The Imported Oil Bill

After an actual world oil-price shock or a historical late-1973 event, the cabinet chooses adjustment. If an equivalent native shock exists, replace its Brazil response instead of stacking another global penalty.

Policy duration: 365 days

### Protect investment

* Construction Speed: +4%
* Inflation Cost: +6%
* Weekly programme expense: 0.15% of payer current annual GDP / 52

### Restrain consumption

* Inflation Growth: -8%
* Factory Output: -4.5%

## The External Credit Squeeze

A historical 1982 stress event requires actual debt and adverse credit conditions. No automatic 1970 debt crisis or debt principal forgiveness.

Policy duration: 365 days

### Negotiate an adjustment programme

* Treasury: -0.3% of payer current GDP, once
* Interest Rate: -0.6 percentage points
* Construction Speed: -6%

### Defend domestic investment

* Construction Speed: +5%
* Interest Rate: +1 percentage points
* Inflation Growth: +8%

## Military Aid and Human Rights

The 1977 dispute can arise if the US agreement is active. Either RP country retains its real treaty and sanction controls.

Policy duration: 365 days

### Retain agreed cooperation

* Political Power Gain: -4%
* Stability: +2%

### Denounce the military arrangement

* Terminate US Training Mission
* Political Power Gain: +4%
* Army Organisation: -2.5%

## The Labourist Naming Dispute

The later PTB and PDT must be separately registered. The event cannot make both share one ruling-party identity.

Policy duration: national

### Recognise distinct PTB and PDT organisations

* Political Power Gain: -2.5%
* Stability: +2.5%

## Prices, Wages and Credit

A later inflation event requires sustained native inflation. Policy values are temporary for 365 days and replace earlier crisis responses rather than accumulating.

Policy duration: 365 days

### Negotiated stabilisation

* Treasury: -0.3% of payer current GDP, once
* Inflation Growth: -10%
* Construction Speed: -4%

### Production first

* Factory Output: +5%
* Inflation Growth: +8%
