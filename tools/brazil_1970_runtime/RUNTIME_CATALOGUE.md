IMPERIA COLD WAR

# Brazil 1970 installed effects

Generated from the installed runtime model. Spatial approval remains immutable. Modifier translations are recorded in `native_adjustments.py` and `runtime_design.json`. These rows describe authored effects; native engine results are recorded separately.

## Starting spirits

### Rule by Institutional Act

Exceptional powers support executive control while censorship and repression corrode consent and intellectual freedom.

- Political Power Gain: +12%
- Stability: -7%
- Research Speed: -3%

### Credit-Fuelled Miracle

Public credit and investment sustain rapid industrial expansion while increasing exposure to financing costs.

- Construction Speed: +8%
- Factory Output: +4%
- Interest Rate: +0.5 percentage points

### Wage Compression

Wage restraint protects industrial margins while concentrating the gains from growth.

- Consumer Goods Factories: -2.5%
- Stability: -5%

### Uneven Technical Education

Advanced industrial centres coexist with restricted access to schooling and specialist training.

- Research Speed: -7%

### Land and Regional Inequality

Concentrated landholding and uneven services make rural development politically difficult.

- Agricultural Productivity: -6%
- Stability: -4%

### Cities Beyond Their Services

Rapid urbanisation strains housing, public health, transport and municipal administration.

- Bureaucracy Cost: +8%
- Stability: -3.5%

### Imported Energy Dependence

Brazilian industry depends heavily on imported oil, leaving production exposed to world prices and supply disruptions.

- Fuel Gain: -8%
- Inflation Cost: +3%

### A Contested Frontier

Road building, settlement and resource extraction confront limited administration, Indigenous rights and ecological constraints.

- Bureaucracy Cost: +5%
- Stability: -3%

## Armed Forces

### Security Cabinet

`COLDWAR_BRA_military_0`, grid (4, 0), focus cost 5.
Coordinate the presidency, service ministries and national security apparatus under the existing military government.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +8%
- Bureaucracy Cost: +4%

### Retain AI-5

`COLDWAR_BRA_military_1`, grid (2, 1), focus cost 5.
Preserve exceptional executive powers and the security services, at the cost of consent and civil liberties.

Prerequisites: (Security Cabinet).

Mutually exclusive with: Controlled Opening.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +12%
- Stability: -5%
- The Military opinion: +8 points, if that native faction is active

### Controlled Opening

`COLDWAR_BRA_military_2`, grid (6, 1), focus cost 5.
Accelerate political reform under military supervision, while retaining leverage for officers who oppose a rapid transition.

Prerequisites: (Security Cabinet).

Mutually exclusive with: Retain AI-5.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.15% of payer current GDP, once
- Remove COLDWAR_BRA_ai5
- Political Power Gain: -8%
- Stability: +5%
- The Military opinion: -8 points, if that native faction is active

### Presidential Compact

`COLDWAR_BRA_military_3`, grid (4, 2), focus cost 5.
Negotiate the composition of the governing coalition without replacing the existing succession system.

Prerequisites: (Retain AI-5 OR Controlled Opening).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Event: COLDWAR_BRA_officer_council

### Staff Colleges

`COLDWAR_BRA_military_4`, grid (0, 2), focus cost 5.
Fund communications, logistics and professional staff instruction.

Prerequisites: (Security Cabinet).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Electronics research bonus: +50%, 1 use(s)
- Army experience: +25

### Defence Engineers

`COLDWAR_BRA_military_5`, grid (6, 3), focus cost 5.
Expand a domestic engineering base while accepting the cost of maintaining small production runs.

Prerequisites: (Presidential Compact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.65% of payer current GDP, once
- Minas Gerais: +1 shared slots, then +1 Military Factory completed
- Equipment Cost: +3%

### Service Coordination

`COLDWAR_BRA_military_6`, grid (4, 4), focus cost 5.
Improve coordination across services while retaining their institutional budgets.

Prerequisites: (Staff Colleges) AND (Defence Engineers).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Army Organisation: +4%
- Personnel Cost: +4%

### National Champions

`COLDWAR_BRA_military_7`, grid (2, 5), focus cost 5.
Concentrate credit in strategic national firms and accept contingent fiscal exposure.

Prerequisites: (Service Coordination).

Mutually exclusive with: Procurement Rules.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +7%
- Interest Rate: +0.5 percentage points
- Weekly expense: 0.12% of payer current annual GDP / 52

### Procurement Rules

`COLDWAR_BRA_military_8`, grid (6, 5), focus cost 5.
Standardise procurement and end prestige orders at the expense of some domestic production.

Prerequisites: (Service Coordination).

Mutually exclusive with: National Champions.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Equipment Cost: -8%
- Factory Output: -3%

### A Defined Mandate

`COLDWAR_BRA_military_9`, grid (4, 6), focus cost 5.
Give the service leadership a defined mission, clear responsibilities and a professional review of its institutional role.

Prerequisites: (National Champions OR Procurement Rules).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Army Organisation: +3%
- Political Power Gain: -4%
- Unlock decision COLDWAR_BRA_service_mission

## ARENA / PDS

### Governors Compact

`COLDWAR_BRA_arena_0`, grid (10, 0), focus cost 5.
Bind state governors and the congressional government bloc through a civilian conservative programme.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +7%
- Bureaucracy Cost: +4%

### Municipal Patronage

`COLDWAR_BRA_arena_1`, grid (8, 1), focus cost 5.
Use municipal networks to distribute investment and hold the governing coalition together.

Prerequisites: (Governors Compact).

Mutually exclusive with: Technical Cabinet.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +6%
- Bureaucracy Cost: +10%

### Technical Cabinet

`COLDWAR_BRA_arena_2`, grid (12, 1), focus cost 5.
Select administrators for technical competence, weakening the patronage bargain.

Prerequisites: (Governors Compact).

Mutually exclusive with: Municipal Patronage.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Bureaucracy Cost: -8%
- Political Power Gain: -7%

### Development Caucus

`COLDWAR_BRA_arena_3`, grid (10, 2), focus cost 5.
Build legislative support for a funded development programme.

Prerequisites: (Municipal Patronage OR Technical Cabinet).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Industrial research bonus: +50%, 1 use(s)

### Interior Industry

`COLDWAR_BRA_arena_4`, grid (8, 3), focus cost 5.
Locate a new industrial plant away from the coastal administrative centres.

Prerequisites: (Development Caucus).

Mutually exclusive with: Farm Credit.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.65% of payer current GDP, once
- Minas Gerais: +1 shared slots, then +1 Civilian Factory completed

### Farm Credit

`COLDWAR_BRA_arena_5`, grid (12, 3), focus cost 5.
Offer agricultural credit through established rural institutions.

Prerequisites: (Development Caucus).

Mutually exclusive with: Interior Industry.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Agricultural Productivity: +5%
- Landowners opinion: +8 points, if that native faction is active

### Federal Bargaining

`COLDWAR_BRA_arena_6`, grid (10, 4), focus cost 5.
Coordinate federal and state investment while accepting a slower bargain over allocations.

Prerequisites: (Interior Industry OR Farm Credit).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Construction Speed: +4%
- Bureaucracy Cost: +3%

### Protected Suppliers

`COLDWAR_BRA_arena_7`, grid (8, 5), focus cost 5.
Reserve procurement for national suppliers, protecting output but narrowing technological competition.

Prerequisites: (Federal Bargaining).

Mutually exclusive with: Export Constituency.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +7%
- Research Speed: -3%

### Export Constituency

`COLDWAR_BRA_arena_8`, grid (12, 5), focus cost 5.
Shift the coalition toward competitive exporters while exposing sheltered domestic interests.

Prerequisites: (Federal Bargaining).

Mutually exclusive with: Protected Suppliers.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Resource Export Income: +10%
- Stability: -3%

### Civilian Conservatism

`COLDWAR_BRA_arena_9`, grid (10, 6), focus cost 5.
Build a conservative civilian government within ARENA, the regime’s governing party, while keeping it institutionally distinct from the armed forces command.

Prerequisites: (Protected Suppliers OR Export Constituency).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Political Power Gain: -3%

## MDB / PMDB

### Congressional Reform

`COLDWAR_BRA_mdb_0`, grid (16, 0), focus cost 5.
Rebuild parliamentary oversight and a broad civilian government. Governing before the historical transition is alternative history.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.15% of payer current GDP, once
- Stability: +4%
- Political Power Gain: -4%

### Negotiated Amnesty

`COLDWAR_BRA_mdb_1`, grid (14, 1), focus cost 5.
Seek a negotiated transition and amnesty, accepting limits on accountability.

Prerequisites: (Congressional Reform).

Mutually exclusive with: Judicial Accountability.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Stability: +7%
- The Military opinion: +4 points, if that native faction is active
- Political Power Gain: -5%

### Judicial Accountability

`COLDWAR_BRA_mdb_2`, grid (18, 1), focus cost 5.
Restore judicial independence and investigate state coercion despite military resistance.

Prerequisites: (Congressional Reform).

Mutually exclusive with: Negotiated Amnesty.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Bureaucracy Cost: +6%
- The Military opinion: -10 points, if that native faction is active
- Research Speed: +3%

### Constituent Mandate

`COLDWAR_BRA_mdb_3`, grid (16, 2), focus cost 5.
Give the civilian transition a constitutional framework with competing institutional priorities.

Prerequisites: (Negotiated Amnesty OR Judicial Accountability).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Remove COLDWAR_BRA_ai5
- Event: COLDWAR_BRA_constitution

### Municipal Autonomy

`COLDWAR_BRA_mdb_4`, grid (14, 3), focus cost 5.
Equip elected municipal administrations to manage public services.

Prerequisites: (Constituent Mandate).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.35% of payer current GDP, once
- Pernambuco: +1 shared slots, then +1 Office completed

### Public Accounts

`COLDWAR_BRA_mdb_5`, grid (18, 3), focus cost 5.
Create professional auditing capacity for public contracts.

Prerequisites: (Constituent Mandate).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: -4%

### Federal Guarantees

`COLDWAR_BRA_mdb_6`, grid (16, 4), focus cost 5.
Distribute authority across federal institutions and accept the cost of coalition bargaining.

Prerequisites: (Municipal Autonomy) AND (Public Accounts).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +5%
- Political Power Gain: -5%

### Social Covenant

`COLDWAR_BRA_mdb_7`, grid (14, 5), focus cost 5.
Expand social rights through a broad parliamentary compromise.

Prerequisites: (Federal Guarantees).

Mutually exclusive with: Fiscal Covenant.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +6%
- Social Spending Cost: +8%
- Labour Unions opinion: +8 points, if that native faction is active

### Fiscal Covenant

`COLDWAR_BRA_mdb_8`, grid (18, 5), focus cost 5.
Constrain unfunded commitments to improve financing conditions.

Prerequisites: (Federal Guarantees).

Mutually exclusive with: Social Covenant.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Interest Rate: -0.5 percentage points
- Construction Speed: -4%
- Labour Unions opinion: -5 points, if that native faction is active

### Civilian Republic

`COLDWAR_BRA_mdb_9`, grid (16, 7), focus cost 5.
Consolidate civilian institutions while leaving room for distinct economic choices within the PMDB.

Prerequisites: (Federal Guarantees) AND (Social Covenant OR Fiscal Covenant).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Political Power Gain: -3%

## Historic PTB

### Labour Guarantees

`COLDWAR_BRA_ptb_0`, grid (24, 0), focus cost 5.
Restore the dissolved pre-1965 labourist organisation as an alternative outcome, distinct from Ivete Vargas’s later PTB.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Stability: +4%
- Social Spending Cost: +4%

### Union Mediation

`COLDWAR_BRA_ptb_1`, grid (22, 1), focus cost 5.
Use negotiated corporatist mediation to stabilise industrial relations.

Prerequisites: (Labour Guarantees).

Mutually exclusive with: Independent Unions.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Labour Unions opinion: +12 points, if that native faction is active
- Factory Output: +4%
- Bureaucracy Cost: +6%

### Independent Unions

`COLDWAR_BRA_ptb_2`, grid (26, 1), focus cost 5.
Give organised labour greater independence from executive patronage.

Prerequisites: (Labour Guarantees).

Mutually exclusive with: Union Mediation.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Labour Unions opinion: +15 points, if that native faction is active
- Stability: +5%
- Political Power Gain: -6%

### Workplace Insurance

`COLDWAR_BRA_ptb_3`, grid (24, 2), focus cost 5.
Extend workplace protection with a visible ongoing social budget.

Prerequisites: (Union Mediation OR Independent Unions).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Social Spending Cost: +5%
- Stability: +4%

### Industrial Apprentices

`COLDWAR_BRA_ptb_4`, grid (20, 3), focus cost 5.
Fund vocational apprenticeships in established industrial districts.

Prerequisites: (Workplace Insurance).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Industrial research bonus: +50%, 1 use(s)

### Labour Courts

`COLDWAR_BRA_ptb_5`, grid (28, 2), focus cost 5.
Improve access to labour courts and fund the additional administrative burden.

Prerequisites: (Labour Guarantees).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: +4%
- Stability: +3%

### Wage Settlement

`COLDWAR_BRA_ptb_6`, grid (24, 4), focus cost 5.
End the initial wage squeeze through an institutional settlement.

Prerequisites: (Industrial Apprentices) AND (Labour Courts).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Remove COLDWAR_BRA_wage_squeeze
- Consumer Goods Factories: +2%

### State Enterprises

`COLDWAR_BRA_ptb_7`, grid (22, 5), focus cost 5.
Use public firms as employers and investment anchors.

Prerequisites: (Wage Settlement).

Mutually exclusive with: Small Employers.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +6%
- Weekly expense: 0.12% of payer current annual GDP / 52

### Small Employers

`COLDWAR_BRA_ptb_8`, grid (26, 5), focus cost 5.
Support smaller employers through tax relief and negotiated labour obligations.

Prerequisites: (Wage Settlement).

Mutually exclusive with: State Enterprises.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Corporate Tax Income: -5%
- Stability: +5%

### Labour Republic

`COLDWAR_BRA_ptb_9`, grid (24, 6), focus cost 5.
Maintain a labourist government whose employment and social commitments rest on functioning public institutions.

Prerequisites: (State Enterprises OR Small Employers).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Political Power Gain: -3%

## PDT

### Labourist Democracy

`COLDWAR_BRA_pdt_0`, grid (32, 0), focus cost 5.
Build Brizola’s democratic labourist alternative with education and national development at its centre.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Stability: +5%
- Political Power Gain: -4%

### Full-Time Schools

`COLDWAR_BRA_pdt_1`, grid (30, 1), focus cost 5.
Use the CIEP precedent for full-time schooling, with a substantial operating commitment.

Prerequisites: (Labourist Democracy).

Mutually exclusive with: Technical Colleges.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.6% of payer current GDP, once
- Education Literacy Growth: +8%
- Education Cost: +10%

### Technical Colleges

`COLDWAR_BRA_pdt_2`, grid (34, 1), focus cost 5.
Prioritise technical and industrial education over the broader full-time school model.

Prerequisites: (Labourist Democracy).

Mutually exclusive with: Full-Time Schools.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.45% of payer current GDP, once
- Research Speed: +5%
- Education Cost: +6%

### Teachers Compact

`COLDWAR_BRA_pdt_3`, grid (32, 2), focus cost 5.
Secure teachers and local administrators for a sustained education programme.

Prerequisites: (Full-Time Schools OR Technical Colleges).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Weekly expense: 0.1% of payer current annual GDP / 52
- Stability: +3%

### Public Engineering

`COLDWAR_BRA_pdt_4`, grid (30, 3), focus cost 5.
Build a public engineering and planning office in Rio de Janeiro.

Prerequisites: (Teachers Compact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.6% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Office completed

### Local Services

`COLDWAR_BRA_pdt_5`, grid (34, 3), focus cost 5.
Extend basic urban networks in Rio Grande do Sul.

Prerequisites: (Teachers Compact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.45% of payer current GDP, once
- Rio Grande do Sul: +1 shared slots, then +1 Infrastructure completed

### Mass Education

`COLDWAR_BRA_pdt_6`, grid (32, 4), focus cost 5.
Broaden access to education and remove the initial technical-research bottleneck.

Prerequisites: (Teachers Compact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Remove COLDWAR_BRA_skills
- Education Cost: +3%

### National Ownership

`COLDWAR_BRA_pdt_7`, grid (30, 5), focus cost 5.
Retain strategic ownership while accepting narrower foreign technology access.

Prerequisites: (Mass Education).

Mutually exclusive with: Licensed Industry.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +6%
- Research Speed: -2.5%

### Licensed Industry

`COLDWAR_BRA_pdt_8`, grid (34, 5), focus cost 5.
Acquire licences for national development with a continuing foreign technology relationship.

Prerequisites: (Mass Education).

Mutually exclusive with: National Ownership.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Industrial research bonus: +50%, 2 use(s)
- Weekly expense: 0.1% of payer current annual GDP / 52
- Foreign Influence Defence: -5%

### A National School

`COLDWAR_BRA_pdt_9`, grid (32, 6), focus cost 5.
Anchor education in a sustained national programme with stable administrative support.

Prerequisites: (National Ownership OR Licensed Industry).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Education Literacy Growth: +4%
- Bureaucracy Cost: +3%

## Workers Party

### Workers Government

`COLDWAR_BRA_pt_0`, grid (38, 0), focus cost 5.
Bring the new union movement and popular organisations into government, grounded in the PT’s late-dictatorship origins.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Labour Unions opinion: +10 points, if that native faction is active
- Political Power Gain: -4%

### Workers Councils

`COLDWAR_BRA_pt_1`, grid (36, 1), focus cost 5.
Give workplace councils authority and accept the coordination costs of negotiated production.

Prerequisites: (Workers Government).

Mutually exclusive with: Productive Pact.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +7%
- Production Efficiency Growth: -5%

### Productive Pact

`COLDWAR_BRA_pt_2`, grid (40, 1), focus cost 5.
Trade workplace autonomy for a negotiated national investment and output agreement.

Prerequisites: (Workers Government).

Mutually exclusive with: Workers Councils.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +7%
- Stability: -3.5%

### Union Independence

`COLDWAR_BRA_pt_3`, grid (38, 2), focus cost 5.
Allow unions and employers to negotiate wages under enforceable labour law.

Prerequisites: (Workers Councils OR Productive Pact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Remove COLDWAR_BRA_wage_squeeze
- Consumer Goods Factories: +2.5%

### Urban Health

`COLDWAR_BRA_pt_4`, grid (36, 3), focus cost 5.
Create the municipal planning and administrative capacity required for broad urban healthcare, with a funded operating budget.

Prerequisites: (Union Independence).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.5% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Office completed
- Weekly expense: 0.08% of payer current annual GDP / 52

### Popular Budgeting

`COLDWAR_BRA_pt_5`, grid (42, 2), focus cost 5.
Adapt participatory budgeting, later associated with Porto Alegre, as an alternative approach to local government.

Prerequisites: (Workers Government).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Bureaucracy Cost: +5%
- Stability: +4%

### Rights in Practice

`COLDWAR_BRA_pt_6`, grid (38, 4), focus cost 5.
Fund the institutions required to turn social guarantees into services.

Prerequisites: (Union Independence) AND (Urban Health).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Social Spending Cost: +5%

### Cooperative Land

`COLDWAR_BRA_pt_7`, grid (36, 5), focus cost 5.
Finance cooperative farming and redistribution while managing conflict with established landowners.

Prerequisites: (Rights in Practice).

Mutually exclusive with: Family Farm Credit.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.45% of payer current GDP, once
- Agricultural Productivity: +6%
- Landowners opinion: -6 points, if that native faction is active
- Weekly expense: 0.08% of payer current annual GDP / 52

### Family Farm Credit

`COLDWAR_BRA_pt_8`, grid (40, 5), focus cost 5.
Expand family-farm credit and extension without a general expropriation programme.

Prerequisites: (Rights in Practice).

Mutually exclusive with: Cooperative Land.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.35% of payer current GDP, once
- Agricultural Productivity: +4%
- Landowners opinion: +6 points, if that native faction is active
- Bureaucracy Cost: +4%

### Popular Democracy

`COLDWAR_BRA_pt_9`, grid (38, 6), focus cost 5.
Sustain a participatory democratic government whose active policy package ends with its tenure.

Prerequisites: (Cooperative Land OR Family Farm Credit).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +5%
- Political Power Gain: -6%

## Liberal Front

### Liberal Coalition

`COLDWAR_BRA_pfl_0`, grid (46, 0), focus cost 5.
Build a conservative civilian coalition from the Liberal Front split, with its own regional and business interests.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +6%
- Bureaucracy Cost: +3.5%

### Regional Investment

`COLDWAR_BRA_pfl_1`, grid (44, 1), focus cost 5.
Direct development investment toward the Northeast through regional political bargains.

Prerequisites: (Liberal Coalition).

Mutually exclusive with: National Competition.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.7% of payer current GDP, once
- Bahia: +1 shared slots, then +1 Civilian Factory completed
- Bureaucracy Cost: +4%

### National Competition

`COLDWAR_BRA_pfl_2`, grid (48, 1), focus cost 5.
Expose protected firms to national competition, accepting regional industrial disruption.

Prerequisites: (Liberal Coalition).

Mutually exclusive with: Regional Investment.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +6%
- Stability: -3%

### Civil Service Review

`COLDWAR_BRA_pfl_3`, grid (46, 2), focus cost 5.
Professionalise appointments while retaining a parliamentary governing bargain.

Prerequisites: (Regional Investment OR National Competition).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: -4%

### Port Services

`COLDWAR_BRA_pfl_4`, grid (44, 3), focus cost 5.
Improve commercial and logistics administration in Pernambuco.

Prerequisites: (Civil Service Review).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Pernambuco: +1 shared slots, then +1 Office completed

### Small Business

`COLDWAR_BRA_pfl_5`, grid (48, 3), focus cost 5.
Reduce the tax burden on firms while sacrificing immediate revenue.

Prerequisites: (Civil Service Review).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Corporate Tax Income: -4%
- Productivity Growth: +3%

### Civilian Coalition

`COLDWAR_BRA_pfl_6`, grid (44, 4), focus cost 5.
Consolidate an elected civilian centre-right coalition.

Prerequisites: (Civil Service Review).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +3%
- Political Power Gain: -3%

### Social Partnership

`COLDWAR_BRA_pfl_7`, grid (46, 5), focus cost 5.
Preserve a social compromise alongside market-oriented development.

Prerequisites: (Small Business).

Mutually exclusive with: Budget Credibility.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +5%
- Social Spending Cost: +6%

### Budget Credibility

`COLDWAR_BRA_pfl_8`, grid (50, 5), focus cost 5.
Limit development credit and improve the government’s financing position.

Prerequisites: (Small Business).

Mutually exclusive with: Social Partnership.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Interest Rate: -0.45 percentage points
- Construction Speed: -3%

### Liberal Institutions

`COLDWAR_BRA_pfl_9`, grid (48, 6), focus cost 5.
Support gradual institutional modernisation rather than reducing liberalism to a single tax bonus.

Prerequisites: (Civilian Coalition) AND (Social Partnership OR Budget Credibility).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Productivity Growth: +2.5%
- Political Power Gain: -3%

## PSDB

### Social Democracy

`COLDWAR_BRA_psdb_0`, grid (54, 0), focus cost 5.
Build the 1988 PSDB alternative around democratic institutions, public services and economic modernisation.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Research Speed: +3%
- Bureaucracy Cost: +3%

### Monetary Restraint

`COLDWAR_BRA_psdb_1`, grid (52, 1), focus cost 5.
Restrain public commitments and reduce the fiscal cost of inflation. Tighter demand slows investment.

Prerequisites: (Social Democracy).

Mutually exclusive with: Investment Compact.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Inflation Cost: -10%
- Construction Speed: -5%

### Investment Compact

`COLDWAR_BRA_psdb_2`, grid (56, 1), focus cost 5.
Protect productive investment while accepting more expensive public commitments during inflation.

Prerequisites: (Social Democracy).

Mutually exclusive with: Monetary Restraint.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Construction Speed: +7%
- Inflation Cost: +8%

### Professional Treasury

`COLDWAR_BRA_psdb_3`, grid (54, 2), focus cost 5.
Fund professional debt management without cancelling public obligations.

Prerequisites: (Monetary Restraint OR Investment Compact).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Interest Rate: -0.35 percentage points

### Research Networks

`COLDWAR_BRA_psdb_4`, grid (52, 3), focus cost 5.
Connect universities and industrial research through a period-appropriate technology programme.

Prerequisites: (Professional Treasury).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.45% of payer current GDP, once
- Electronics research bonus: +50%, 2 use(s)

### Public Evaluation

`COLDWAR_BRA_psdb_5`, grid (58, 3), focus cost 5.
Use service evaluation and administrative reform to improve education spending efficiency.

Prerequisites: (Professional Treasury).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Education Cost: -4%

### Social Guarantees

`COLDWAR_BRA_psdb_6`, grid (52, 4), focus cost 5.
Maintain a social budget alongside macroeconomic reform.

Prerequisites: (Research Networks).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Weekly expense: 0.08% of payer current annual GDP / 52
- Stability: +4%

### Competitive Industry

`COLDWAR_BRA_psdb_7`, grid (56, 5), focus cost 5.
Use competition to accelerate productivity while accepting firm closures and industrial conflict.

Prerequisites: (Professional Treasury).

Mutually exclusive with: Managed Conversion.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Growth: +8%
- Stability: -3%

### Managed Conversion

`COLDWAR_BRA_psdb_8`, grid (60, 5), focus cost 5.
Finance a slower industrial transition with explicit public support.

Prerequisites: (Professional Treasury).

Mutually exclusive with: Competitive Industry.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +4%
- Weekly expense: 0.12% of payer current annual GDP / 52

### Democratic Modernity

`COLDWAR_BRA_psdb_9`, grid (54, 6), focus cost 5.
Consolidate a late-Cold-War reform programme without importing the 1994 Real Plan.

Prerequisites: (Social Guarantees) AND (Competitive Industry OR Managed Conversion).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Research Speed: +2.5%
- Political Power Gain: -3%

## PCB

### Communist Coalition

`COLDWAR_BRA_pcb_0`, grid (64, 0), focus cost 5.
Give the PCB a distinct governing alternative rooted in its organisation and Soviet relationship.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Political Power Gain: +6%
- Foreign Influence Defence: -4%

### Pluralist Transition

`COLDWAR_BRA_pcb_1`, grid (62, 1), focus cost 5.
Pursue a broad democratic transition while sharing authority with other left parties.

Prerequisites: (Communist Coalition).

Mutually exclusive with: Cadre Direction.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +6%
- Political Power Gain: -6%

### Cadre Direction

`COLDWAR_BRA_pcb_2`, grid (66, 1), focus cost 5.
Concentrate authority in party cadres to direct industrial targets.

Prerequisites: (Communist Coalition).

Mutually exclusive with: Pluralist Transition.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +7%
- Stability: -4.5%

### Planning Institutes

`COLDWAR_BRA_pcb_3`, grid (64, 2), focus cost 5.
Build planning expertise as a real administrative asset.

Prerequisites: (Pluralist Transition OR Cadre Direction).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Office completed

### Strategic Production

`COLDWAR_BRA_pcb_4`, grid (62, 3), focus cost 5.
Expand basic industrial production through public investment.

Prerequisites: (Planning Institutes).

Mutually exclusive with: Technical Exchange.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.6% of payer current GDP, once
- Minas Gerais: +1 shared slots, then +1 Civilian Factory completed

### Technical Exchange

`COLDWAR_BRA_pcb_5`, grid (66, 3), focus cost 5.
Exchange political and organisational experience with international communist movements.

Prerequisites: (Planning Institutes).

Mutually exclusive with: Strategic Production.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Industrial research bonus: +50%, 1 use(s)

### Public Ownership

`COLDWAR_BRA_pcb_6`, grid (64, 4), focus cost 5.
Support long production runs through public firms and a recurring capital programme.

Prerequisites: (Strategic Production OR Technical Exchange).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Cap: +5%
- Weekly expense: 0.1% of payer current annual GDP / 52

### National Communism

`COLDWAR_BRA_pcb_7`, grid (62, 5), focus cost 5.
Retain independent direction at the cost of access to some foreign technical networks.

Prerequisites: (Public Ownership).

Mutually exclusive with: International Links.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Foreign Influence Defence: +8%
- Research Speed: -2.5%

### International Links

`COLDWAR_BRA_pcb_8`, grid (66, 5), focus cost 5.
Use external communist networks while accepting political dependence. A treaty still requires recipient consent.

Prerequisites: (Public Ownership).

Mutually exclusive with: National Communism.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Research Speed: +5%
- Foreign Influence Defence: -7%

### A Socialist Mandate

`COLDWAR_BRA_pcb_9`, grid (64, 6), focus cost 5.
Sustain a distinct PCB programme, separate from the PCdoB’s rural revolutionary strategy.

Prerequisites: (National Communism OR International Links).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Bureaucracy Cost: +4%

## PCdoB

### Rural Revolution

`COLDWAR_BRA_pcdob_0`, grid (70, 0), focus cost 5.
Develop a distinct alternate governing programme from the PCdoB’s rural revolutionary tradition.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Political Power Gain: +6%
- Stability: -4%

### Peasant Cooperatives

`COLDWAR_BRA_pcdob_1`, grid (68, 1), focus cost 5.
Pool equipment and extension services while confronting landholding interests.

Prerequisites: (Rural Revolution).

Mutually exclusive with: Village Land Titles.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Agricultural Productivity: +7%
- Weekly expense: 0.12% of payer current annual GDP / 52
- Landowners opinion: -8 points, if that native faction is active

### Village Land Titles

`COLDWAR_BRA_pcdob_2`, grid (72, 1), focus cost 5.
Prioritise secure household titles and local consent over collective ownership.

Prerequisites: (Rural Revolution).

Mutually exclusive with: Peasant Cooperatives.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +7%
- Agricultural Productivity: +3.5%
- Bureaucracy Cost: +6%

### Rural Administration

`COLDWAR_BRA_pcdob_3`, grid (70, 2), focus cost 5.
Create a permanent civil administration in Pará to govern and deliver services beyond the revolutionary organisation.

Prerequisites: (Peasant Cooperatives OR Village Land Titles).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Para: +1 shared slots, then +1 Office completed

### Village Instruction

`COLDWAR_BRA_pcdob_4`, grid (68, 3), focus cost 5.
Expand rural instruction under a funded education programme.

Prerequisites: (Rural Administration).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Education Literacy Growth: +6%
- Education Cost: +6%

### Local Workshops

`COLDWAR_BRA_pcdob_5`, grid (72, 3), focus cost 5.
Build a regional civilian workshop complex for agricultural and basic industrial tools.

Prerequisites: (Rural Administration).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.55% of payer current GDP, once
- Pernambuco: +1 shared slots, then +1 Civilian Factory completed

### Agrarian Settlement

`COLDWAR_BRA_pcdob_6`, grid (70, 4), focus cost 5.
Replace the initial land inequality burden through a costly agrarian settlement.

Prerequisites: (Rural Administration).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Remove COLDWAR_BRA_land_inequality
- Bureaucracy Cost: +4%

### People’s Defence

`COLDWAR_BRA_pcdob_7`, grid (68, 5), focus cost 5.
Develop infantry-oriented territorial defence with a larger personnel bill.

Prerequisites: (Village Instruction).

Mutually exclusive with: Civil Reconstruction.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Infantry Attack: +6%
- Army Personnel Cost: +8%

### Civil Reconstruction

`COLDWAR_BRA_pcdob_8`, grid (72, 5), focus cost 5.
Prioritise reconstruction while reducing military institutional weight.

Prerequisites: (Local Workshops).

Mutually exclusive with: People’s Defence.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Construction Speed: +6%
- Army Organisation: -4%

### A Rural Republic

`COLDWAR_BRA_pcdob_9`, grid (70, 6), focus cost 5.
Turn a rural revolutionary organisation into a working administration with lasting public responsibilities.

Prerequisites: (Agrarian Settlement) AND (People’s Defence OR Civil Reconstruction).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Political Power Gain: -4%

## Lacerdists

### Public Probity

`COLDWAR_BRA_populist_0`, grid (76, 0), focus cost 5.
Build Lacerda’s electoral programme around accountable government and public integrity.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: -4%
- Political Power Gain: -3%

### Independent Auditors

`COLDWAR_BRA_populist_1`, grid (74, 1), focus cost 5.
Give auditors institutional independence at the expense of executive discretion.

Prerequisites: (Public Probity).

Mutually exclusive with: Presidential Campaign.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Bureaucracy Cost: -6%
- Political Power Gain: -5%

### Presidential Campaign

`COLDWAR_BRA_populist_2`, grid (78, 1), focus cost 5.
Mobilise a personal presidential mandate with greater polarisation.

Prerequisites: (Public Probity).

Mutually exclusive with: Independent Auditors.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +10%
- Stability: -4%

### Administrative Reform

`COLDWAR_BRA_populist_3`, grid (76, 2), focus cost 5.
Reform purchasing and appointments through functioning administrative institutions.

Prerequisites: (Independent Auditors OR Presidential Campaign).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Productivity Growth: +3%

### Competitive Imports

`COLDWAR_BRA_populist_4`, grid (74, 3), focus cost 5.
Open access to imported machinery while exposing domestic manufacturers.

Prerequisites: (Administrative Reform).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Research Speed: +4%
- Factory Output: -4%

### Urban Management

`COLDWAR_BRA_populist_5`, grid (78, 3), focus cost 5.
Invest in practical urban transport and basic networks.

Prerequisites: (Administrative Reform).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Infrastructure completed

### Electoral Government

`COLDWAR_BRA_populist_6`, grid (76, 3), focus cost 5.
Restore an electoral mandate without imposing a specific presidential winner.

Prerequisites: (Administrative Reform).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +4%
- Political Power Gain: -3%

### Rapid Competition

`COLDWAR_BRA_populist_7`, grid (74, 5), focus cost 5.
Open protected markets to sharper competition. More efficient production brings resistance from established firms and their political allies.

Prerequisites: (Electoral Government).

Mutually exclusive with: Staged Liberalism.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Growth: +10%
- Stability: -7%

### Staged Liberalism

`COLDWAR_BRA_populist_8`, grid (78, 5), focus cost 5.
Subsidise a slower transition with a continuing adjustment budget.

Prerequisites: (Electoral Government).

Mutually exclusive with: Rapid Competition.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Growth: +5%
- Weekly expense: 0.1% of payer current annual GDP / 52

### Executive Oversight

`COLDWAR_BRA_populist_9`, grid (76, 6), focus cost 5.
Make executive authority answerable to independent oversight.

Prerequisites: (Rapid Competition OR Staged Liberalism).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Bureaucracy Cost: -3.5%
- Political Power Gain: -3.5%

## PRN

### A New Presidency

`COLDWAR_BRA_prn_0`, grid (82, 0), focus cost 5.
Develop a late-1989 personal presidential coalition. PRN is the renamed Party of Youth, not Lacerda’s party.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Political Power Gain: +7%
- Stability: -2.5%

### Competition Shock

`COLDWAR_BRA_prn_1`, grid (80, 1), focus cost 5.
Open the economy rapidly, accepting disruption and closures among sheltered firms.

Prerequisites: (A New Presidency).

Mutually exclusive with: Negotiated Opening.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Growth: +10%
- Stability: -6%

### Negotiated Opening

`COLDWAR_BRA_prn_2`, grid (84, 1), focus cost 5.
Fund a slower competitive adjustment with an explicit transition budget.

Prerequisites: (A New Presidency).

Mutually exclusive with: Competition Shock.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Production Efficiency Growth: +5%
- Weekly expense: 0.12% of payer current annual GDP / 52

### Purchasing Reform

`COLDWAR_BRA_prn_3`, grid (82, 2), focus cost 5.
Strengthen accountability in public purchasing through functioning oversight institutions.

Prerequisites: (Competition Shock OR Negotiated Opening).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Bureaucracy Cost: -4%

### Industrial Imports

`COLDWAR_BRA_prn_4`, grid (80, 3), focus cost 5.
Buy access to industrial technology while retaining vulnerability to external commercial pressure.

Prerequisites: (Purchasing Reform).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Industrial research bonus: +50%, 2 use(s)
- Foreign Influence Defence: -3.5%

### Service Review

`COLDWAR_BRA_prn_5`, grid (86, 2), focus cost 5.
Reduce redundant appointments with a real political cost.

Prerequisites: (A New Presidency).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: -3.5%
- Stability: -2.5%

### Presidential Coalition

`COLDWAR_BRA_prn_6`, grid (82, 4), focus cost 5.
Keep a heterogeneous governing coalition functioning through parliamentary bargains.

Prerequisites: (Purchasing Reform) AND (Industrial Imports).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Political Power Gain: +5%
- Bureaucracy Cost: +4%

### Price Restraint

`COLDWAR_BRA_prn_7`, grid (80, 5), focus cost 5.
Tighten indexation and credit commitments to reduce inflation’s public cost, accepting slower investment. This does not adopt the 1990 deposit freeze.

Prerequisites: (Presidential Coalition).

Mutually exclusive with: Productive Credit.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Inflation Cost: -10%
- Construction Speed: -5%

### Productive Credit

`COLDWAR_BRA_prn_8`, grid (84, 5), focus cost 5.
Protect industrial credit while accepting higher financing pressure.

Prerequisites: (Presidential Coalition).

Mutually exclusive with: Price Restraint.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Construction Speed: +6%
- Interest Rate: +0.5 percentage points

### Public Accountability

`COLDWAR_BRA_prn_9`, grid (82, 7), focus cost 5.
Submit presidential administration to effective oversight and legislative bargaining.

Prerequisites: (Presidential Coalition) AND (Price Restraint OR Productive Credit).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +3.5%
- Political Power Gain: -4%

## PTB

### A Labour Coalition

`COLDWAR_BRA_ptb_late_0`, grid (90, 0), focus cost 5.
Build Ivete Vargas’s PTB as a distinct labour and regional coalition, separate from Brizola’s PDT and the dissolved pre-1965 party.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.18% of payer current GDP, once
- Political Power Gain: +6%
- Bureaucracy Cost: +4%

### Employer Compact

`COLDWAR_BRA_ptb_late_1`, grid (88, 1), focus cost 5.
Support production through an employer-oriented compact at a cost in union confidence.

Prerequisites: (A Labour Coalition).

Mutually exclusive with: Union Agreements.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Factory Output: +6%
- Labour Unions opinion: -6 points, if that native faction is active

### Union Agreements

`COLDWAR_BRA_ptb_late_2`, grid (92, 1), focus cost 5.
Negotiate labour protections while accepting resistance from larger employers.

Prerequisites: (A Labour Coalition).

Mutually exclusive with: Employer Compact.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +5.5%
- Industrial Conglomerates opinion: -6 points, if that native faction is active
- Social Spending Cost: +3%

### Benefit Administration

`COLDWAR_BRA_ptb_late_3`, grid (90, 2), focus cost 5.
Match benefit coverage and service levels to the revenue available for administration.

Prerequisites: (Employer Compact OR Union Agreements).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.25% of payer current GDP, once
- Bureaucracy Cost: +3.5%
- Stability: +2.5%

### Vocational Training

`COLDWAR_BRA_ptb_late_4`, grid (88, 3), focus cost 5.
Expand practical training through the labour and industrial institutions.

Prerequisites: (Benefit Administration).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.3% of payer current GDP, once
- Industrial research bonus: +50%, 1 use(s)

### Regional Employers

`COLDWAR_BRA_ptb_late_5`, grid (92, 3), focus cost 5.
Provide commercial and labour administration for smaller regional employers.

Prerequisites: (Benefit Administration).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Treasury: -0.4% of payer current GDP, once
- Bahia: +1 shared slots, then +1 Office completed

### Workplace Compact

`COLDWAR_BRA_ptb_late_6`, grid (90, 4), focus cost 5.
Replace wage compression through a negotiated wage and employment settlement.

Prerequisites: (Vocational Training) AND (Regional Employers).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Remove COLDWAR_BRA_wage_squeeze
- Consumer Goods Factories: +2%

### Social Protection

`COLDWAR_BRA_ptb_late_7`, grid (88, 5), focus cost 5.
Expand protection with a clearly visible public-service bill.

Prerequisites: (Workplace Compact).

Mutually exclusive with: Employment Credit.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +5%
- Social Spending Cost: +7%

### Employment Credit

`COLDWAR_BRA_ptb_late_8`, grid (92, 5), focus cost 5.
Protect hiring and investment through credit, accepting greater financing exposure.

Prerequisites: (Workplace Compact).

Mutually exclusive with: Social Protection.

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Construction Speed: +5%
- Interest Rate: +0.4 percentage points

### Coalition Guarantees

`COLDWAR_BRA_ptb_late_9`, grid (90, 6), focus cost 5.
Make labour policy answerable to a working parliamentary coalition.

Prerequisites: (Social Protection OR Employment Credit).

Party programme: active only for its actual governing identity. Earned programme spirits return without repeating finite rewards.

- Stability: +3%
- Political Power Gain: -3%

## Institutions and Society

### Civil Guarantees

`COLDWAR_BRA_constitutional`, grid (4, 9), focus cost 5.
End exceptional powers through a genuine constitutional reform. Early adoption is alternative history.

- Treasury: -0.25% of payer current GDP, once
- Remove COLDWAR_BRA_ai5
- Political Power Gain: -6%

### Church Grants

`COLDWAR_BRA_church_dialogue`, grid (0, 10), focus cost 5.
Direct public grants to church-linked service organisations and sustain dialogue with the CNBB, alongside secular provision.

- Treasury: -0.15% of payer current GDP, once
- Stability: +5%
- Political Power Gain: -3%

### Public Service Plan

`COLDWAR_BRA_secular_services`, grid (4, 10), focus cost 5.
Prioritise publicly administered services while keeping dialogue with the CNBB and church organisations open.

- Treasury: -0.3% of payer current GDP, once
- Bureaucracy Cost: +4%
- Stability: +4%

### Plural Party Law

`COLDWAR_BRA_legal_parties`, grid (8, 10), focus cost 5.
Replace the imposed two-party framework and make actual new-party formation possible.

Prerequisites: (Civil Guarantees).

- Treasury: -0.15% of payer current GDP, once
- Event: COLDWAR_BRA_party_reform

### National Training

`COLDWAR_BRA_schools`, grid (2, 11), focus cost 5.
Broaden technical training through public institutions.

Prerequisites: (Church Grants OR Public Service Plan).

- Treasury: -0.5% of payer current GDP, once
- Remove COLDWAR_BRA_skills
- Industrial research bonus: +50%, 1 use(s)

### Municipal Networks

`COLDWAR_BRA_municipal`, grid (8, 11), focus cost 5.
Extend basic municipal networks in industrial and northeastern cities.

- Treasury: -0.6% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Infrastructure completed
- Pernambuco: +1 shared slots, then +1 Infrastructure completed

### University Research

`COLDWAR_BRA_universities`, grid (0, 12), focus cost 5.
Fund university research with a continuing operating budget.

Prerequisites: (National Training).

Mutually exclusive with: Adult Literacy.

- Treasury: -0.3% of payer current GDP, once
- Electronics research bonus: +50%, 2 use(s)
- Weekly expense: 0.08% of payer current annual GDP / 52

### Adult Literacy

`COLDWAR_BRA_adult_literacy`, grid (4, 12), focus cost 5.
Expand adult literacy through sustained instruction and stronger local access.

Prerequisites: (National Training).

Mutually exclusive with: University Research.

- Treasury: -0.25% of payer current GDP, once
- Education Literacy Growth: +6%
- Education Cost: +5%

### Urban Services

`COLDWAR_BRA_urban_services`, grid (8, 12), focus cost 5.
Provide municipal administrative capacity for health and housing services.

Prerequisites: (Municipal Networks).

- Treasury: -0.4% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Office completed
- Weekly expense: 0.06% of payer current annual GDP / 52

### Serviced Cities

`COLDWAR_BRA_city_settlement`, grid (8, 13), focus cost 5.
Complete the joint transport and services remedy for urban pressure.

Prerequisites: (Urban Services).

- Remove COLDWAR_BRA_urban_pressure

### Rural Settlement

`COLDWAR_BRA_land_titles`, grid (0, 14), focus cost 5.
Regularise landholding and expand public extension, accepting conflict and administrative costs.

Prerequisites: (University Research OR Adult Literacy).

Mutually exclusive with: Regional Extension.

- Treasury: -0.4% of payer current GDP, once
- Remove COLDWAR_BRA_land_inequality
- Bureaucracy Cost: +4%
- Landowners opinion: -7 points, if that native faction is active

### Regional Extension

`COLDWAR_BRA_extension`, grid (4, 14), focus cost 5.
Use long-term regional extension and cooperative credit without a general land redistribution.

Prerequisites: (University Research OR Adult Literacy).

Mutually exclusive with: Rural Settlement.

- Treasury: -0.35% of payer current GDP, once
- Remove COLDWAR_BRA_land_inequality
- Agricultural Productivity: +3.5%
- Weekly expense: 0.1% of payer current annual GDP / 52

### A Wage Bargain

`COLDWAR_BRA_wage_bargain`, grid (8, 14), focus cost 5.
Replace wage compression with a funded bargaining framework.

Prerequisites: (Serviced Cities).

- Treasury: -0.2% of payer current GDP, once
- Remove COLDWAR_BRA_wage_squeeze
- Consumer Goods Factories: +2%
- Labour Unions opinion: +8 points, if that native faction is active

### Territorial Offices

`COLDWAR_BRA_territory`, grid (0, 15), focus cost 5.
Create civil administrative capacity in the eastern Amazon.

Prerequisites: (Rural Settlement OR Regional Extension).

- Treasury: -0.45% of payer current GDP, once
- Para: +1 shared slots, then +1 Office completed

### Frontier Safeguards

`COLDWAR_BRA_frontier_safeguards`, grid (0, 16), focus cost 5.
Protect indigenous rights and establish project review before frontier expansion.

Prerequisites: (Territorial Offices).

Mutually exclusive with: Frontier Administration.

- Treasury: -0.2% of payer current GDP, once
- Remove COLDWAR_BRA_amazon_pressure
- Construction Speed: -2.5%

### Frontier Administration

`COLDWAR_BRA_frontier_admin`, grid (4, 16), focus cost 5.
Expand permanent civil administration and compensation in the frontier, accepting continuing contestation.

Prerequisites: (Territorial Offices).

Mutually exclusive with: Frontier Safeguards.

- Treasury: -0.3% of payer current GDP, once
- Remove COLDWAR_BRA_amazon_pressure
- Weekly expense: 0.12% of payer current annual GDP / 52
- Stability: -1.5%

### Public Service Audit

`COLDWAR_BRA_service_audit`, grid (8, 16), focus cost 5.
Fund professional audits and strengthen oversight of public services.

Prerequisites: (A Wage Bargain).

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: -4%

### A Social Settlement

`COLDWAR_BRA_social_settlement`, grid (4, 17), focus cost 5.
Maintain a national social settlement with an explicit operating appropriation.

Prerequisites: (Frontier Safeguards OR Frontier Administration) AND (Public Service Audit).

- Stability: +4%
- Weekly expense: 0.08% of payer current annual GDP / 52

## Industry and Agriculture

### Development Finance

`COLDWAR_BRA_development_bank`, grid (14, 9), focus cost 5.
Strengthen BNDES project appraisal without adding GDP by decree.

- Treasury: -0.3% of payer current GDP, once
- Industrial research bonus: +50%, 1 use(s)

### Development Loans

`COLDWAR_BRA_refinance`, grid (10, 10), focus cost 5.
Replace the initial credit surge with better screened long-term investment.

Prerequisites: (Development Finance).

Mutually exclusive with: Export Discipline.

- Treasury: -0.65% of payer current GDP, once
- Remove COLDWAR_BRA_miracle
- Interest Rate: -0.4 percentage points
- Construction Speed: +3.5%

### Export Discipline

`COLDWAR_BRA_export_discipline`, grid (14, 10), focus cost 5.
Reorient development toward export receipts and abandon the initial indiscriminate credit expansion.

Prerequisites: (Development Finance).

Mutually exclusive with: Development Loans.

- Remove COLDWAR_BRA_miracle
- Resource Export Income: +10%
- Stability: -2.5%

### Industrial Triangle

`COLDWAR_BRA_industrial_triangle`, grid (18, 10), focus cost 5.
Expand São Paulo and Minas Gerais manufacturing with matched building slots.

Prerequisites: (Development Finance).

- Treasury: -0.9% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Civilian Factory completed
- Minas Gerais: +1 shared slots, then +1 Civilian Factory completed

### Tropical Agronomy

`COLDWAR_BRA_embrapa`, grid (12, 11), focus cost 5.
Build agricultural research capacity through Embrapa, founded in 1973, and strengthen the technical basis for higher farm productivity.

Prerequisites: (Development Loans OR Export Discipline).

- Treasury: -0.35% of payer current GDP, once
- Agricultural research bonus: +50%, 2 use(s)

### Capital Goods

`COLDWAR_BRA_capital_goods`, grid (18, 11), focus cost 5.
Fund capital-goods manufacturing rather than importing a modern production line for free.

Prerequisites: (Industrial Triangle).

- Treasury: -0.65% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Civilian Factory completed

### Cerrado Agribusiness

`COLDWAR_BRA_cerrado`, grid (10, 12), focus cost 5.
Combine tropical agronomy with large-scale commercial farming and acknowledge land concentration.

Prerequisites: (Tropical Agronomy).

Mutually exclusive with: Smallholder Research.

- Treasury: -0.6% of payer current GDP, once
- Goias: +1 shared slots, then +1 Agriculture District completed
- Agricultural Productivity: +7%
- Stability: -2.5%

### Smallholder Research

`COLDWAR_BRA_smallholder`, grid (14, 12), focus cost 5.
Direct extension and credit toward smaller farmers with a larger service bill.

Prerequisites: (Tropical Agronomy).

Mutually exclusive with: Cerrado Agribusiness.

- Treasury: -0.4% of payer current GDP, once
- Pernambuco: +1 shared slots, then +1 Agriculture District completed
- Agricultural Productivity: +4%
- Weekly expense: 0.08% of payer current annual GDP / 52

### Licensed Tooling

`COLDWAR_BRA_licensed_tools`, grid (16, 12), focus cost 5.
Licence production equipment while accepting recurrent fees and dependence.

Prerequisites: (Capital Goods).

Mutually exclusive with: National Tooling.

- Industrial research bonus: +50%, 2 use(s)
- Weekly expense: 0.1% of payer current annual GDP / 52
- Foreign Influence Defence: -3.5%

### National Tooling

`COLDWAR_BRA_national_tools`, grid (20, 12), focus cost 5.
Prioritise a national tooling base with a narrower technology pool.

Prerequisites: (Capital Goods).

Mutually exclusive with: Licensed Tooling.

- Treasury: -0.45% of payer current GDP, once
- Production Efficiency Cap: +6%
- Research Speed: -2.5%

### Storage and Markets

`COLDWAR_BRA_storage`, grid (12, 13), focus cost 5.
Link food-producing districts to storage and wholesale markets.

Prerequisites: (Cerrado Agribusiness OR Smallholder Research).

- Treasury: -0.4% of payer current GDP, once
- Mato Grosso: +1 shared slots, then +1 Infrastructure completed

### Industrial Standards

`COLDWAR_BRA_industrial_standards`, grid (18, 13), focus cost 5.
Create standards and quality-control capacity for national manufacturers.

Prerequisites: (Licensed Tooling OR National Tooling).

- Treasury: -0.2% of payer current GDP, once
- Production Efficiency Growth: +5%

### Manaus Industry

`COLDWAR_BRA_manaus`, grid (10, 14), focus cost 5.
Expand the Manaus zone through real facilities and explicit tax concessions.

Prerequisites: (Storage and Markets).

Mutually exclusive with: Northeast Industry.

- Treasury: -0.7% of payer current GDP, once
- Amazonas: +1 shared slots, then +1 Civilian Factory completed
- Corporate Tax Income: -2.5%

### Northeast Industry

`COLDWAR_BRA_regional_industry`, grid (14, 14), focus cost 5.
Fund northeastern industry and the administrative support it requires.

Prerequisites: (Storage and Markets).

Mutually exclusive with: Manaus Industry.

- Treasury: -0.7% of payer current GDP, once
- Bahia: +1 shared slots, then +1 Civilian Factory completed
- Weekly expense: 0.06% of payer current annual GDP / 52

### Embraer Production

`COLDWAR_BRA_embraer`, grid (18, 14), focus cost 5.
Expand aircraft manufacturing from Embraer, founded in 1969, by investing in production capacity and aeronautical research.

Prerequisites: (Industrial Standards).

- Treasury: -0.75% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Military Factory completed
- Aircraft research bonus: +50%, 1 use(s)

### Telecommunications

`COLDWAR_BRA_telebras`, grid (14, 15), focus cost 5.
Expand the national telecommunications institution, represented by offices and period electronics research.

Prerequisites: (Manaus Industry OR Northeast Industry).

- Treasury: -0.55% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Office completed
- Electronics research bonus: +50%, 1 use(s)

### Export Offices

`COLDWAR_BRA_trade_fairs`, grid (18, 15), focus cost 5.
Fund technical export offices and quality promotion to strengthen productive firms and their commercial networks.

Prerequisites: (Embraer Production).

- Treasury: -0.25% of payer current GDP, once
- Productivity Growth: +3.5%
- Weekly expense: 0.04% of payer current annual GDP / 52

### A Productive Nation

`COLDWAR_BRA_productive_nation`, grid (14, 16), focus cost 5.
Coordinate productive institutions through a funded national programme.

Prerequisites: (Telecommunications) AND (Export Offices).

- Production Efficiency Cap: +4%
- Weekly expense: 0.08% of payer current annual GDP / 52

## Energy and Resources

### Energy Balance

`COLDWAR_BRA_energy_balance`, grid (26, 9), focus cost 5.
Assess industrial demand and imported-fuel exposure before committing to new energy projects.

- Treasury: -0.15% of payer current GDP, once
- Energy research bonus: +50%, 1 use(s)

### Offshore Petrobras

`COLDWAR_BRA_offshore`, grid (22, 10), focus cost 5.
Fund offshore exploration and refining expertise, accepting the risk that reserves may not prove commercially viable.

Prerequisites: (Energy Balance).

Mutually exclusive with: Efficient Energy Use.

- Treasury: -0.8% of payer current GDP, once
- Excavation research bonus: +50%, 1 use(s)
- Fuel Gain: +5%
- Weekly expense: 0.12% of payer current annual GDP / 52

### Efficient Energy Use

`COLDWAR_BRA_conservation`, grid (26, 10), focus cost 5.
Prioritise conservation and retrofitting rather than rapid supply expansion.

Prerequisites: (Energy Balance).

Mutually exclusive with: Offshore Petrobras.

- Treasury: -0.35% of payer current GDP, once
- Energy Efficiency research bonus: +50%, 2 use(s)
- Construction Speed: -2.5%

### Regional Power Grid

`COLDWAR_BRA_grid`, grid (30, 10), focus cost 5.
Extend the regional power grid to carry growing industrial and urban demand.

Prerequisites: (Energy Balance).

- Treasury: -0.7% of payer current GDP, once
- Minas Gerais: +1 shared slots, then +1 Infrastructure completed

### Fuel Security

`COLDWAR_BRA_fuel_security`, grid (24, 11), focus cost 5.
Complete storage and substitution measures that remove initial energy vulnerability.

Prerequisites: (Offshore Petrobras OR Efficient Energy Use).

- Treasury: -0.3% of payer current GDP, once
- Remove COLDWAR_BRA_oil_exposure
- Sao Paulo: +1 shared slots, then +1 Fuel Silo completed

### Domestic Hydropower

`COLDWAR_BRA_hydro`, grid (30, 11), focus cost 5.
Build domestic hydroelectric capacity and its operating institutions. Cross-border Itaipu development requires a separate agreement with Paraguay.

Prerequisites: (Regional Power Grid).

- Treasury: -1% of payer current GDP, once
- Parana: +1 shared slots, then +1 Renewable Energy Infrastructure construction
- Weekly expense: 0.08% of payer current annual GDP / 52

### Alcohol Fuels

`COLDWAR_BRA_proalcool`, grid (22, 12), focus cost 5.
Expand ethanol production through Proálcool, diversifying fuel supply while competing for land and food production.

Prerequisites: (Fuel Security).

Mutually exclusive with: Conventional Refining.

- Treasury: -0.6% of payer current GDP, once
- Fuel Gain: +10%
- Agricultural Productivity: -3%
- Weekly expense: 0.12% of payer current annual GDP / 52

### Conventional Refining

`COLDWAR_BRA_refining`, grid (26, 12), focus cost 5.
Expand native refinery capacity while retaining imported-feedstock exposure in public costs.

Prerequisites: (Fuel Security).

Mutually exclusive with: Alcohol Fuels.

- Treasury: -0.7% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Synthetic Refinery completed
- Inflation Cost: +2.5%

### Civil Nuclear Science

`COLDWAR_BRA_nuclear_science`, grid (30, 12), focus cost 5.
Build scientific expertise and trained personnel for a civilian nuclear programme.

Prerequisites: (Domestic Hydropower).

- Treasury: -0.4% of payer current GDP, once
- Civil Nuclear research bonus: +50%, 2 use(s)

### Mineral Survey

`COLDWAR_BRA_mineral_survey`, grid (24, 13), focus cost 5.
Survey known mineral prospects and fund feasibility work. Extraction requires a separately financed mine-development project.

Prerequisites: (Alcohol Fuels OR Conventional Refining).

- Treasury: -0.2% of payer current GDP, once
- Excavation research bonus: +50%, 1 use(s)
- Unlock decision COLDWAR_BRA_uranium_study

### Reactor Programme

`COLDWAR_BRA_reactor`, grid (28, 13), focus cost 5.
Build a civilian reactor programme, with construction and fuel-cycle expertise demanding sustained capital.

Prerequisites: (Civil Nuclear Science).

Mutually exclusive with: Diverse Generation.

- Treasury: -1.5% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Nuclear Reactor construction
- Weekly expense: 0.2% of payer current annual GDP / 52

### Diverse Generation

`COLDWAR_BRA_grid_diversity`, grid (32, 13), focus cost 5.
Choose domestic generation diversity instead of the reactor works.

Prerequisites: (Civil Nuclear Science).

Mutually exclusive with: Reactor Programme.

- Treasury: -0.9% of payer current GDP, once
- Bahia: +1 shared slots, then +1 Renewable Energy Infrastructure completed
- Energy Efficiency research bonus: +50%, 1 use(s)

### Carajas Logistics

`COLDWAR_BRA_carajas`, grid (24, 14), focus cost 5.
Fund rail, port and administrative capacity for the Carajás mineral frontier. Resource revenues depend on exports.

Prerequisites: (Mineral Survey).

- Treasury: -0.8% of payer current GDP, once
- Para: +1 shared slots, then +1 Infrastructure completed
- Steel Export Income: +8%
- Weekly expense: 0.06% of payer current annual GDP / 52

### Resource Standards

`COLDWAR_BRA_resource_standards`, grid (30, 14), focus cost 5.
Fund technical standards, geological services and the institutions that manage mineral sales.

Prerequisites: (Reactor Programme OR Diverse Generation).

- Treasury: -0.2% of payer current GDP, once
- Bureaucracy Cost: +2.5%
- Resource Export Income: +4%

### Energy Resilience

`COLDWAR_BRA_energy_resilience`, grid (26, 15), focus cost 5.
Maintain a diversified energy and resource system against external cost shocks.

Prerequisites: (Carajas Logistics) AND (Resource Standards).

- Inflation Cost: -3.5%
- Weekly expense: 0.06% of payer current annual GDP / 52

### Power Dispatch

`COLDWAR_BRA_energy_dispatch`, grid (26, 16), focus cost 5.
Coordinate supply dispatch and resource contracts through a concrete administrative facility.

Prerequisites: (Energy Resilience).

- Treasury: -0.3% of payer current GDP, once
- Goias: +1 shared slots, then +1 Office completed

## Armed Services

### Joint Staff Review

`COLDWAR_BRA_joint_staff`, grid (38, 9), focus cost 5.
Review force requirements across services before selecting new commitments.

- Treasury: -0.2% of payer current GDP, once
- Army experience: +25
- Navy experience: +25
- Air experience: +25

### Territorial Army

`COLDWAR_BRA_territorial`, grid (34, 10), focus cost 5.
Prioritise a broad territorial army with an appropriate personnel burden.

Prerequisites: (Joint Staff Review).

Mutually exclusive with: Professional Cadres.

- Army Organisation: +6%
- Army Personnel Cost: +8%

### Professional Cadres

`COLDWAR_BRA_professional`, grid (38, 10), focus cost 5.
Concentrate on trained cadres and maintenance while reducing equipment waste.

Prerequisites: (Joint Staff Review).

Mutually exclusive with: Territorial Army.

- Army Organisation: +3.5%
- Equipment Cost: -6%
- Personnel Cost: +3.5%

### Flying Schools

`COLDWAR_BRA_air_training`, grid (42, 10), focus cost 5.
Expand flying instruction before committing to new airframes.

Prerequisites: (Joint Staff Review).

- Treasury: -0.3% of payer current GDP, once
- Aircraft research bonus: +50%, 1 use(s)
- Air experience: +35

### Small Arms Industry

`COLDWAR_BRA_imbel`, grid (36, 11), focus cost 5.
Develop national small-arms production, building on the later consolidation of IMBEL.

Prerequisites: (Territorial Army OR Professional Cadres).

- Treasury: -0.65% of payer current GDP, once
- Minas Gerais: +1 shared slots, then +1 Military Factory completed

### Flight Safety

`COLDWAR_BRA_air_safety`, grid (42, 11), focus cost 5.
Fund safety instruction and maintenance with a larger skilled-personnel bill.

Prerequisites: (Flying Schools).

- Air Accident Chance: -10%
- Air Force Personnel Cost: +5%

### Jungle School

`COLDWAR_BRA_jungle`, grid (34, 12), focus cost 5.
Fund jungle communications, field instruction and staff exercises for Brazil’s difficult interior terrain.

Prerequisites: (Small Arms Industry).

Mutually exclusive with: Vehicle Workshops.

- Treasury: -0.25% of payer current GDP, once
- Army experience: +40
- Electronics research bonus: +25%, 1 use(s)

### Vehicle Workshops

`COLDWAR_BRA_mechanised`, grid (38, 12), focus cost 5.
Expand vehicle workshops with an explicit cost for domestic production depth.

Prerequisites: (Small Arms Industry).

Mutually exclusive with: Jungle School.

- Treasury: -0.6% of payer current GDP, once
- Sao Paulo: +1 shared slots, then +1 Military Factory completed
- Equipment Cost: +3.5%

### Tactical Air Support

`COLDWAR_BRA_air_support`, grid (40, 12), focus cost 5.
Build a tactical-support air service with the required specialist staff.

Prerequisites: (Flight Safety).

Mutually exclusive with: Airspace Defence.

- Air Mission Efficiency: +6%
- Air Force Personnel Cost: +6%

### Airspace Defence

`COLDWAR_BRA_air_defence`, grid (44, 12), focus cost 5.
Develop domestic airspace defence through basing and training.

Prerequisites: (Flight Safety).

Mutually exclusive with: Tactical Air Support.

- Treasury: -0.4% of payer current GDP, once
- Goias: +1 shared slots, then +1 Air Base completed
- Air experience: +30

### Naval Workshops

`COLDWAR_BRA_naval_yards`, grid (36, 13), focus cost 5.
Expand naval repair and construction capacity in Rio, building local maintenance skills and industrial depth.

Prerequisites: (Jungle School OR Vehicle Workshops).

- Treasury: -0.8% of payer current GDP, once
- Rio de Janeiro: +1 shared slots, then +1 Naval Dockyard completed

### Joint Exercises

`COLDWAR_BRA_joint_exercises`, grid (42, 13), focus cost 5.
Fund joint planning and exercises across services.

Prerequisites: (Tactical Air Support OR Airspace Defence).

- Treasury: -0.2% of payer current GDP, once
- Army experience: +25
- Air experience: +25

### Oceanic Fleet

`COLDWAR_BRA_ocean_fleet`, grid (34, 14), focus cost 5.
Maintain an oceanic fleet with a large specialist and operating burden.

Prerequisites: (Naval Workshops).

Mutually exclusive with: Coastal Escort Fleet.

- Naval Organisation: +8%
- Navy Personnel Cost: +12%
- Weekly expense: 0.1% of payer current annual GDP / 52

### Coastal Escort Fleet

`COLDWAR_BRA_coastal_fleet`, grid (38, 14), focus cost 5.
Prioritise cheaper escort production over the cohesion of a broader blue-water force.

Prerequisites: (Naval Workshops).

Mutually exclusive with: Oceanic Fleet.

- Dockyard Output: +8%
- Naval Organisation: -3%

### Procurement Office

`COLDWAR_BRA_procurement`, grid (42, 14), focus cost 5.
Standardise procurement through a funded contracting office.

Prerequisites: (Joint Exercises).

- Treasury: -0.25% of payer current GDP, once
- Equipment Cost: -5%
- Bureaucracy Cost: +2.5%

### Rocket Engineering

`COLDWAR_BRA_avibras`, grid (36, 15), focus cost 5.
Build national guidance and electronics expertise as a foundation for Brazil’s later rocket artillery industry.

Prerequisites: (Oceanic Fleet OR Coastal Escort Fleet).

- Treasury: -0.5% of payer current GDP, once
- Electronics research bonus: +50%, 1 use(s)
- Army experience: +20

### Defence Export Office

`COLDWAR_BRA_exports_arms`, grid (42, 15), focus cost 5.
Support export-oriented defence production while accepting foreign market dependence.

Prerequisites: (Procurement Office).

- Treasury: -0.25% of payer current GDP, once
- Factory Output: +3.5%
- Foreign Influence Defence: -2.5%

### A Regional Force

`COLDWAR_BRA_regional_force`, grid (38, 16), focus cost 5.
Maintain a balanced regional force through an explicit staff and readiness budget.

Prerequisites: (Rocket Engineering) AND (Defence Export Office).

- Army Organisation: +2.5%
- Weekly expense: 0.08% of payer current annual GDP / 52

## Itamaraty and RP Agreements

### Itamaraty Review

`COLDWAR_BRA_itamaraty`, grid (58, 9), focus cost 5.
Define practical diplomatic priorities without committing any foreign player.

- Treasury: -0.15% of payer current GDP, once
- Bureaucracy Cost: +2.5%

### Atlantic Continuity

`COLDWAR_BRA_atlantic`, grid (52, 10), focus cost 5.
Prioritise established Atlantic commercial and technical links.

Prerequisites: (Itamaraty Review).

Mutually exclusive with: Pragmatic Diplomacy.

- Research Speed: +2.5%
- Foreign Influence Defence: -4%

### Pragmatic Diplomacy

`COLDWAR_BRA_pragmatism`, grid (58, 10), focus cost 5.
Diversify diplomatic partners despite domestic anticommunist opposition.

Prerequisites: (Itamaraty Review).

Mutually exclusive with: Atlantic Continuity.

- Resource Export Income: +5%
- Political Power Gain: -3.5%

### Regional Diplomacy

`COLDWAR_BRA_regional`, grid (64, 10), focus cost 5.
Reduce regional rivalry through negotiation while preserving recipient choice.

Prerequisites: (Itamaraty Review).

- Treasury: -0.15% of payer current GDP, once
- Stability: +2.5%

### US Training Mission

`COLDWAR_BRA_us_training`, grid (50, 11), focus cost 5.
Expand military training and technical exchange with the United States, while human-rights policy remains a potential source of friction.

Prerequisites: (Atlantic Continuity).

Mutually exclusive with: US Industrial Licences.


Recipient: United States. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: US Training Mission**

- Treasury: -0.25% of payer current GDP, once
- Weekly expense: 0.06% of payer current annual GDP / 52
- Army Organisation: +4%
- Foreign Influence Defence: -4%
- Army experience: +30

**United States: US Training Mission**

- Treasury: -0.04% of payer current GDP, once
- Weekly expense: 0.015% of payer current annual GDP / 52
- Army Organisation: +1.5%
- Army experience: +15

### US Industrial Licences

`COLDWAR_BRA_us_industry`, grid (54, 11), focus cost 5.
Negotiate industrial licences with US firms and set terms for access to technology.

Prerequisites: (Atlantic Continuity).

Mutually exclusive with: US Training Mission.


Recipient: United States. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: US Industrial Licences**

- Treasury: -0.4% of payer current GDP, once
- Weekly expense: 0.08% of payer current annual GDP / 52
- Production Efficiency Growth: +6%
- Foreign Influence Defence: -5%
- Industrial research bonus: +50%, 1 use(s)

**United States: US Industrial Licences**

- Treasury: -0.05% of payer current GDP, once
- Weekly expense: 0.015% of payer current annual GDP / 52
- Productivity Growth: +1.5%
- Industrial research bonus: +25%, 1 use(s)

### China Trade Mission

`COLDWAR_BRA_china_trade`, grid (58, 11), focus cost 5.
Build trade ties alongside diplomatic recognition, opening new markets amid domestic anti-communist opposition.

Prerequisites: (Pragmatic Diplomacy).


Recipient: China. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: China Trade Mission**

- Treasury: -0.15% of payer current GDP, once
- Weekly expense: 0.035% of payer current annual GDP / 52
- Resource Export Income: +7%
- Political Power Gain: -2.5%

**China: China Trade Mission**

- Treasury: -0.08% of payer current GDP, once
- Weekly expense: 0.025% of payer current annual GDP / 52
- Resource Export Income: +4%
- Bureaucracy Cost: +1.5%

### Soviet Machinery

`COLDWAR_BRA_ussr_machines`, grid (62, 11), focus cost 5.
Exchange Brazilian goods for Soviet machinery and equipment, extending trade without a security alliance.

Prerequisites: (Pragmatic Diplomacy).


Recipient: Soviet Union. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Soviet Machinery**

- Treasury: -0.25% of payer current GDP, once
- Weekly expense: 0.06% of payer current annual GDP / 52
- Industrial research bonus: +50%, 2 use(s)
- Resource Export Income: +5%
- Foreign Influence Defence: -3%

**Soviet Union: Soviet Machinery**

- Treasury: -0.08% of payer current GDP, once
- Weekly expense: 0.025% of payer current annual GDP / 52
- Agricultural research bonus: +50%, 1 use(s)
- Resource Export Income: +3.5%

### Itaipu Proposal

`COLDWAR_BRA_itaipu`, grid (66, 11), focus cost 5.
Negotiate a binational hydroelectric project with Paraguay. Each country funds its own share, and Brazil provides financial support to Paraguay. The terms establish neither historical Itaipu royalties nor guaranteed electricity deliveries.

Prerequisites: (Regional Diplomacy).


Recipient: Paraguay. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Itaipu Proposal**

- Treasury: -1.5% of payer current GDP, once
- Weekly expense: 0.18% of payer current annual GDP / 52
- Parana: +1 shared slots, then +1 Renewable Energy Infrastructure construction
- Inflation Cost: -2.5%
- Weekly expense: 0.08% of Brazil current annual GDP / 52

**Paraguay: Itaipu Proposal**

- Treasury: -0.65% of payer current GDP, once
- Weekly expense: 0.12% of payer current annual GDP / 52
- Paraguay: +1 shared slots, then +1 Renewable Energy Infrastructure construction
- Inflation Cost: -2.5%
- Weekly income: 0.08% of Brazil current annual GDP / 52

### Cerrado Cooperation

`COLDWAR_BRA_japan_agro`, grid (52, 12), focus cost 5.
Expand Cerrado agriculture through research, credit and extension, while addressing concentrated landholding and ecological pressures.

Prerequisites: (Pacific Commerce).

Mutually exclusive with: Japan Steel Pact.


Recipient: Japan. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Cerrado Cooperation**

- Treasury: -0.45% of payer current GDP, once
- Weekly expense: 0.08% of payer current annual GDP / 52
- Agricultural Productivity: +6%
- Agricultural research bonus: +50%, 1 use(s)
- Stability: -2%

**Japan: Cerrado Cooperation**

- Treasury: -0.08% of payer current GDP, once
- Weekly expense: 0.025% of payer current annual GDP / 52
- Agricultural research bonus: +50%, 1 use(s)
- Productivity Growth: +1.5%

### Japan Steel Pact

`COLDWAR_BRA_japan_steel`, grid (56, 12), focus cost 5.
Negotiate Japanese investment and long-term market access for Brazilian steel producers, balancing industrial capacity against foreign financing and market dependence.

Prerequisites: (Pacific Commerce).

Mutually exclusive with: Cerrado Cooperation.


Recipient: Japan. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Japan Steel Pact**

- Treasury: -0.75% of payer current GDP, once
- Weekly expense: 0.1% of payer current annual GDP / 52
- Minas Gerais: +1 shared slots, then +1 Civilian Factory completed
- Steel Export Income: +5%

**Japan: Japan Steel Pact**

- Treasury: -0.1% of payer current GDP, once
- Weekly expense: 0.035% of payer current annual GDP / 52
- Industrial research bonus: +50%, 1 use(s)
- Production Efficiency Growth: +2.5%

### Angola Technical Pact

`COLDWAR_BRA_angola`, grid (60, 12), focus cost 5.
Offer technical cooperation to independent Angola and its MPLA government, following Brazil’s recognition in 1975.

Prerequisites: (China Trade Mission).


Recipient: Angola. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Angola Technical Pact**

- Treasury: -0.12% of payer current GDP, once
- Weekly expense: 0.04% of payer current annual GDP / 52
- Productivity Growth: +1.5%
- Bureaucracy Cost: +1.5%

**Angola: Angola Technical Pact**

- Treasury: -0.15% of payer current GDP, once
- Weekly expense: 0.06% of payer current annual GDP / 52
- Industrial research bonus: +50%, 1 use(s)
- Construction Speed: +3.5%
- Foreign Influence Defence: -3%

### River Consultations

`COLDWAR_BRA_arg_basin`, grid (64, 12), focus cost 5.
Consult with Argentina on the effects of planned hydroelectric projects in the Paraná basin, using the 1979 Itaipu-Corpus settlement as a precedent.

Prerequisites: (Itaipu Proposal).


Recipient: Argentina. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: River Consultations**

- Treasury: -0.2% of payer current GDP, once
- Weekly expense: 0.035% of payer current annual GDP / 52
- Construction Speed: +3.5%
- Bureaucracy Cost: +2%

**Argentina: River Consultations**

- Treasury: -0.2% of payer current GDP, once
- Weekly expense: 0.035% of payer current annual GDP / 52
- Construction Speed: +3.5%
- Bureaucracy Cost: +2%

### German Nuclear Pact

`COLDWAR_BRA_germany_nuclear`, grid (46, 12), focus cost 5.
Pursue civilian technology cooperation under the 1975 agreement, including reactor projects and fuel-cycle expertise. The programme requires substantial capital and specialist capacity.

Prerequisites: (Technical Diplomacy).


Recipient: Federal Republic of Germany. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: German Nuclear Pact**

- Treasury: -0.9% of payer current GDP, once
- Weekly expense: 0.15% of payer current annual GDP / 52
- Civil Nuclear research bonus: +50%, 2 use(s)
- Nuclear Reactor Construction Speed: +8%
- Foreign Influence Defence: -4%

**Federal Republic of Germany: German Nuclear Pact**

- Treasury: -0.12% of payer current GDP, once
- Weekly expense: 0.04% of payer current annual GDP / 52
- Civil Nuclear research bonus: +50%, 1 use(s)
- Factory Output: +2%

### Nuclear Transparency

`COLDWAR_BRA_nuclear_dialogue`, grid (68, 12), focus cost 5.
Explore civilian nuclear confidence-building independently of river disputes or a German treaty.

Prerequisites: (Regional Commerce).

- Treasury: -0.15% of payer current GDP, once
- Civil Nuclear research bonus: +25%, 1 use(s)

### Nuclear Confidence

`COLDWAR_BRA_arg_nuclear`, grid (68, 13), focus cost 5.
Strengthen peaceful nuclear cooperation through transparency and regular contact between the two national programmes.

Prerequisites: (Nuclear Transparency).


Recipient: Argentina. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Nuclear Confidence**

- Treasury: -0.3% of payer current GDP, once
- Weekly expense: 0.06% of payer current annual GDP / 52
- Civil Nuclear research bonus: +50%, 1 use(s)
- Research Speed: +2.5%
- Bureaucracy Cost: +2.5%

**Argentina: Nuclear Confidence**

- Treasury: -0.3% of payer current GDP, once
- Weekly expense: 0.06% of payer current annual GDP / 52
- Civil Nuclear research bonus: +50%, 1 use(s)
- Research Speed: +2.5%
- Bureaucracy Cost: +2.5%

### Industrial Protocol

`COLDWAR_BRA_arg_integration`, grid (62, 13), focus cost 5.
Coordinate industrial policy and trade with Argentina through sectoral work programmes and deeper bilateral commerce.

Prerequisites: (Industrial Talks).


Recipient: Argentina. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Industrial Protocol**

- Treasury: -0.45% of payer current GDP, once
- Weekly expense: 0.08% of payer current annual GDP / 52
- Production Efficiency Growth: +5%
- Bureaucracy Cost: +2.5%
- Industrial research bonus: +50%, 1 use(s)

**Argentina: Industrial Protocol**

- Treasury: -0.45% of payer current GDP, once
- Weekly expense: 0.08% of payer current annual GDP / 52
- Production Efficiency Growth: +5%
- Bureaucracy Cost: +2.5%
- Industrial research bonus: +50%, 1 use(s)

### Uruguay Port Protocol

`COLDWAR_BRA_uruguay`, grid (60, 14), focus cost 5.
Establish joint administration of port facilities and commercial routes with Uruguay.

Prerequisites: (Industrial Protocol).


Recipient: Uruguay. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Uruguay Port Protocol**

- Treasury: -0.2% of payer current GDP, once
- Weekly expense: 0.04% of payer current annual GDP / 52
- Resource Export Income: +4.5%
- Bureaucracy Cost: +2%

**Uruguay: Uruguay Port Protocol**

- Treasury: -0.3% of payer current GDP, once
- Weekly expense: 0.055% of payer current annual GDP / 52
- Uruguay (Rio de la Plata): +1 shared slots, then +1 Office completed
- Resource Export Income: +4%

### Mirage Partnership

`COLDWAR_BRA_france_aircraft`, grid (50, 12), focus cost 5.
Negotiate Mirage III training and maintenance with France, building on Brazil’s 1970 procurement.

Prerequisites: (Technical Diplomacy).


Recipient: France. Recipient Accept and Decline decisions. No expiry; both sides suspend on war, embargo or any mirrored Imperia sanction.

**Brazil: Mirage Partnership**

- Treasury: -0.5% of payer current GDP, once
- Weekly expense: 0.08% of payer current annual GDP / 52
- Aircraft research bonus: +50%, 2 use(s)
- Air Mission Efficiency: +2.5%
- Foreign Influence Defence: -3.5%

**France: Mirage Partnership**

- Treasury: -0.08% of payer current GDP, once
- Weekly expense: 0.025% of payer current annual GDP / 52
- Aircraft research bonus: +50%, 1 use(s)
- Production Efficiency Growth: +2%

### Regional Secretariat

`COLDWAR_BRA_regional_secretariat`, grid (58, 15), focus cost 5.
Maintain a consultative regional secretariat for the signed commercial protocols.

Prerequisites: (Uruguay Port Protocol).

- Treasury: -0.25% of payer current GDP, once
- Goias: +1 shared slots, then +1 Office completed
- Weekly expense: 0.05% of payer current annual GDP / 52

### Technical Diplomacy

`COLDWAR_BRA_technical_desk`, grid (46, 11), focus cost 5.
Fund a technical negotiating desk for independent European industrial and aviation proposals.

Prerequisites: (Atlantic Continuity OR Pragmatic Diplomacy).

- Treasury: -0.12% of payer current GDP, once
- Electronics research bonus: +25%, 1 use(s)

### Pacific Commerce

`COLDWAR_BRA_pacific_desk`, grid (56, 11), focus cost 5.
Prepare Japanese commercial and agricultural negotiations independently of any US agreement.

Prerequisites: (Atlantic Continuity OR Pragmatic Diplomacy).

- Treasury: -0.12% of payer current GDP, once
- Agricultural research bonus: +25%, 1 use(s)

### Regional Commerce

`COLDWAR_BRA_commercial_desk`, grid (64, 11), focus cost 5.
Prepare regional industrial negotiations independently of nuclear or river treaties.

Prerequisites: (Regional Diplomacy).

- Treasury: -0.12% of payer current GDP, once
- Industrial research bonus: +25%, 1 use(s)

### Industrial Talks

`COLDWAR_BRA_industrial_talks`, grid (62, 12), focus cost 5.
Draft industrial terms for Argentina without making a nuclear agreement compulsory.

Prerequisites: (Regional Commerce).

- Treasury: -0.12% of payer current GDP, once
- Industrial research bonus: +25%, 1 use(s)

## Domestic decisions

### Review the Service Mission

- Treasury: -0.2% of payer current GDP, once
- Army experience: +30

### Commission a Uranium Feasibility Study

- Treasury: -0.15% of payer current GDP, once
- Civil Nuclear research bonus: +50%, 1 use(s)

## Domestic events

### The Officer Council

Senior officers debate the balance between command authority and civilian expertise.

Lifetime: government.

**Protect the command hierarchy**

- Army Organisation: +4%
- Political Power Gain: -4%

**Bring civilian specialists into cabinet**

- Research Speed: +3%
- Bureaucracy Cost: +4%

### The Constitutional Settlement

A constituent settlement must balance social guarantees with executive authority.

Lifetime: national.

**Strengthen social guarantees**

- Stability: +6%
- Social Spending Cost: +6%

**Prioritise governability**

- Political Power Gain: +7%
- Stability: -3%

### The Party Reorganisation

A political opening brings pressure to reorganise the party system and widen civilian competition.

Lifetime: national.

**Register competing civilian organisations**

- Political Power Gain: -4%
- Stability: +4%

**Negotiate a limited transition**

- Stability: +2%
- The Military opinion: +5 points, if that native faction is active

### The Imported Oil Bill

Surging world oil prices raise the cost of imported fuel. The cabinet must decide how to protect investment and manage consumption.

Lifetime: 365 days.

**Protect investment**

- Construction Speed: +4%
- Inflation Cost: +6%
- Weekly expense: 0.15% of payer current annual GDP / 52

**Restrain consumption**

- Inflation Cost: -8%
- Factory Output: -4.5%

### The External Credit Squeeze

The debt and credit crisis puts public investment under pressure. The cabinet must decide how to negotiate with creditors and protect domestic priorities.

Lifetime: 365 days.

**Negotiate an adjustment programme**

- Treasury: -0.3% of payer current GDP, once
- Interest Rate: -0.6 percentage points
- Construction Speed: -6%

**Defend domestic investment**

- Construction Speed: +5%
- Interest Rate: +1 percentage points
- Inflation Cost: +8%

### Military Aid and Human Rights

Disagreement over human-rights conditions in US security cooperation puts the military relationship under strain. Brasília must decide whether to retain the agreement.

Lifetime: 365 days.

**Retain agreed cooperation**

- Political Power Gain: -4%
- Stability: +2%

**Denounce the military arrangement**

- Terminate agreement us_training and remove both spirits
- Political Power Gain: +4%
- Army Organisation: -2.5%

### The Labourist Naming Dispute

The labourist movement divides over control of the PTB name, prompting Brizola’s supporters to organise the PDT.

Lifetime: national.

**Recognise distinct PTB and PDT organisations**

- Political Power Gain: -2.5%
- Stability: +2.5%

### Prices, Wages and Credit

Persistent inflation forces a choice between negotiated stabilisation and continued production-led policy.

Lifetime: 365 days.

**Negotiated stabilisation**

- Treasury: -0.3% of payer current GDP, once
- Inflation Cost: -10%
- Construction Speed: -4%

**Production first**

- Factory Output: +5%
- Inflation Cost: +8%

