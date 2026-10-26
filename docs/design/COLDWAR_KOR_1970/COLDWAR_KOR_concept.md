# South Korea — January 1970–1990 national focus concept

**298 focuses; 61 mutual-exclusion links; 14 programme clusters. Approval-stage design only.**

All names, descriptions, conditions and effect text below are English. Numbers are multiplayer balance proposals grounded in documented institutions, not estimates of historical causal effects. The historical starting leader remains Park Chung Hee. No loaded game content has been edited.

The complete spatial preview and catalogue use the same resolved JSON coordinates. Native MD grid is 96×130 pixels, item 165×128, name field 147×20. Browser fonts and connector routing approximate the game; final engine appearance requires an in-game check.

## Programme map

| Programme | Anchor | Focuses | Government |
|---|---:|---:|---|
| From military rule to democracy | (82, 0) | 36 | Independent KOR; actual crisis, mandate and constitutional states |
| DRP · Park and the developmental state | (4, 0) | 21 | check_variable = { ruling_party = 0 } AND actual Park incumbent |
| NDP · constitutional opposition | (12, 0) | 17 | check_variable = { ruling_party = 1 } |
| Reform liberals · the Two Kims | (23, 0) | 22 | check_variable = { ruling_party = 2 } |
| Army / DJP · Chun and Roh | (34, 0) | 21 | check_variable = { ruling_party = 22 } |
| USP · social democracy | (4, 14) | 16 | check_variable = { ruling_party = 3 } |
| Students and independent Marxists | (13, 14) | 17 | Exact governing slot 5 or 19; separate roots below |
| RPR · revolutionary reunification | (23, 14) | 14 | check_variable = { ruling_party = 4 } |
| KCIA · an exceptional security cabinet | (34, 14) | 14 | check_variable = { ruling_party = 7 } |
| National development · industry and society | (45, 0) | 34 | Independent KOR; 1970 scenario |
| Defence · deterrence and autonomy | (54, 0) | 28 | Independent KOR; 1970 scenario |
| Foreign policy · alliances and markets | (63, 0) | 21 | Independent KOR; 1970 scenario |
| North Korea · rivalry, dialogue and settlement | (72, 0) | 23 | Independent KOR; 1970 scenario |
| Kim Jong-pil · civilian conservatism | (54, 19) | 14 | ruling_party = 0 AND incumbent Kim Jong-pil; NDRP identity after reorganization |

## Important design decisions

- Park/DRP, NDP, the Two Kims, Chun/Roh, USP, students, independent Marxists, RPR, exceptional KCIA rule and Kim Jong-pil have playable continuations. Fringe religious, monarchy and Ilmin paths are excluded.
- The Two Kims are possible successive incumbents. Their policy choices are exclusive; becoming president does not permanently ban the other person from returning later.
- A36-focus national transition programme now connects the historical succession, opposition coalition, constitutional negotiations, ratification, election and civilian institutions; all actual crises and ballots still resolve through events/decisions and native politics.
- Political programmes deactivate when their exact owner leaves government; earned policy values return with that owner. Buildings, cash, XP and other one-time outcomes never replay.
- National economic choices remain earned institutions across ordinary government changes. A separately approved policy-reversal decision would be needed to undo an exclusive national choice; changing party is not a free respec.
- A government adopting competitive civilian institutions cannot retain emergency-constitution bonuses, even if the same individual remains president.
- Offers require the other player’s response. Refused treaty-only follow-ups bypass with no payout, allowing common domestic continuation. No automatic annexation, unification, equipment shipment, treaty withdrawal or troop deployment.
- National development uses supported MD/Imperia modifiers and paid construction. No focus directly assigns a development tier, resets debt, reruns GDP initialization, grants future technology or creates starting armed forces.

## Starting national spirits

### A Contested Presidential Mandate

1969 third-term amendment; Yushin is not yet in force.

`COLDWAR_KOR_start_presidency` — incumbent Park / DRP; reform replaces it

- Political power gain: +8%
- Stability: -8%

First DRP constitutional choice replaces this slot; a constitutional opposition settlement removes it.

### Concentrated Development Credit

State-directed credit mobilizes industrial capital but concentrates leverage and guarantees.

`COLDWAR_KOR_start_finance` — national problem slot finance

- Interest rate (percentage points before native clamps): +0.5 percentage points
- Civilian industry productivity: +4%

National finance policy replaces this slot. Party credit policies can coexist and show their extra exposure.

### The Human Cost of Export Growth

Restricted bargaining, long hours and unsafe workplaces undermine legitimacy and skills.

`COLDWAR_KOR_start_labour` — national problem slot labour

- Stability: -8%
- Research speed: -2%
- Civilian industry productivity: +3%

Either national labor policy replaces it: discipline retains a legitimacy malus; compromise sacrifices output.

### An Unevenly Developed Republic

Rural infrastructure gaps and rapid urban migration constrain balanced development.

`COLDWAR_KOR_start_rural` — national problem slot rural

- Construction speed: -7%
- Stability: -3%

Freight corridors improve it to construction -3%, stability -2%; urban services remove the remainder.

### An Alliance under Adjustment

The US commitment deters attack while the Nixon Doctrine raises uncertainty and demands local responsibility.

`COLDWAR_KOR_start_alliance` — national external exposure

- Division defence on core territory: +5%
- Foreign influence defence: -10%

An accepted US assurance deal replaces it; strategic autonomy trades defense backing for independence.

### Imported Energy, Imported Risk

Rapid industrialization depends on imported fuel and external finance; this is exposure, not a 1973 shock in 1970.

`COLDWAR_KOR_start_energy` — national problem slot energy

- Interest rate (percentage points before native clamps): +0.2 percentage points
- Civilian industry productivity: -4%

Diversified energy planning reduces it; completed and funded existing energy projects remove remaining exposure.

### Overseas Employment Programme

Government-organized miners and nurses in West Germany; already granted in KOR country history.

`mdcw_ni_overseas_employment_programme` — existing starting idea; preserve actual code

- Preserve the actual existing idea and remittance system; no invented duplicate values.

Use existing guest-worker contracts and remittance accounting; never grant remittances twice.

### Political Officer Networks

The army, security agencies and private officer networks sustain the developmental state while undermining neutral civilian command.

`COLDWAR_KOR_start_political_command` — national command problem; active until lawful civilian control

- Division organization: +4%
- Political power gain: +3%
- Stability: -4%
- Weekly personnel expenses: +4%

Civilian Appointments plus Constitutional Security remove the command-problem slot. An extra-constitutional rollback restores the unresolved political-command state, not free transition rewards.

### Fragmented Social Protection

Coverage remained fragmented and excluded many rural, informal and urban households; broad national coverage was a late 1980s achievement.

`COLDWAR_KOR_start_social_insurance` — national welfare problem slot

- Stability: -4%
- Weekly social expenses: +5%

The funded social-insurance network establishes the new framework and resolves this administrative fragmentation; it does not claim all households were historically insured before 1989.

## Party integration before implementation

Registry has NDP=1, Forties=2, USP=3; native leader pools/retirement alternatives still put Kim Young-sam at1, Kim Dae-jung at3. Roh absent.

Preserve Park and start DRP=0/EPB coalition13. Reconcile leader pools and retirement alternatives to the registry: both reform Kims in2, Kim Chul/USP in3; NDP elders1; Chun and new Roh in22 with dated identity labels DJP. This is a proposed migration, not existing runtime behavior.

Roh is not a 1970 alternate starting leader. Add nomination/office transitions through current native political machinery. All Kim/Chun/Roh office flags read actual incumbent; future RDP/PDP/DJP labels reflect real office/history, not invented ideology tokens.

## From military rule to democracy

Entry condition: Independent KOR; actual crisis, mandate and constitutional states.

### Constitutional Review

`COLDWAR_KOR_constitutional_question` · **14 days** · grid (82, 0) · owner: national

Review who may command, legislate and amend the constitution. This opens a real negotiation process, not an automatic regime change.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace transition:constitutional_audit:
- Political power gain: +3%
- Weekly bureaucracy expenses: +3%
- pp_once: -50 (once)
- action: open_constitutional_dossier

### An Electoral Opening

`COLDWAR_KOR_electoral_opening` · **35 days** · grid (78, 1) · owner: national

Use a genuine electoral or constitutional contest to negotiate enforceable limits on the incumbent.

Prerequisites: (constitutional_question).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: -3%
- Stability: -2%

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_transition_open"]`

### An Interim Cabinet

`COLDWAR_KOR_interim_cabinet` · **35 days** · grid (82, 1) · owner: national

Support Choi Kyu-hah’s historical caretaker window, or an explicitly negotiated civilian succession. Formal office and coercive command remain separate.

Prerequisites: (constitutional_question).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: -6%
- Division organization: -2%

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_transition_open"]`

### Negotiated Withdrawal

`COLDWAR_KOR_negotiated_withdrawal` · **35 days** · grid (86, 1) · owner: national

Open talks with a military-led government under organized civilian pressure; no date or party popularity alone completes the handover.

Prerequisites: (constitutional_question).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: -4%
- Weekly personnel expenses: +4%

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_transition_open"]`

### Bind the Incumbent

`COLDWAR_KOR_bind_incumbent` · **35 days** · grid (78, 2) · owner: national

Obtain a binding commitment to constitutional talks rather than a personal promise of reform.

Prerequisites: (electoral_opening).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: -5%
- Weekly bureaucracy expenses: +3%

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_negotiating_commitment"]`

### Uphold Civil Command

`COLDWAR_KOR_defend_civil_command` · **35 days** · grid (82, 2) · owner: national

Resolve the officer challenge to legitimate command. A failed Seoul Spring may lead to renewed military rule and a later opening.

Prerequisites: (interim_cabinet).
Exclusive with: none.

- Replace transition:transition_phase:
- Division organization: -3%
- Political power gain: -4%
- action: resolve_command_challenge

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_command_settlement_pending", "country_event = { id = COLDWAR_KOR_transition.12 days = 1 }"]`

### Retirement Guarantees

`COLDWAR_KOR_retirement_guarantees` · **35 days** · grid (86, 2) · owner: national

Offer funded retirement guarantees to remove officers from executive politics. The pension obligation survives an ordinary cabinet change.

Prerequisites: (negotiated_withdrawal).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace transition:retirement_promise:
- Division organization: +2%
- Weekly personnel expenses: +8%

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_negotiating_commitment"]`

### Constitutional Talks

`COLDWAR_KOR_authorize_talks` · **35 days** · grid (82, 3) · owner: national

Authorize talks with a real mandate and a resolved command or retirement bargain.

Prerequisites: (bind_incumbent OR defend_civil_command OR retirement_guarantees).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: -4%
- Weekly bureaucracy expenses: +4%
- action: authorize_constitutional_talks

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_talks_authorized"]`

### Open Civic Space

`COLDWAR_KOR_open_civic_space` · **35 days** · grid (82, 4) · owner: national

Restore lawful meetings, political organization and access to constitutional debate; no party receives free votes.

Prerequisites: (authorize_talks).
Exclusive with: none.

- Treasury: -$1bn (once)
- action: legal_civic_associations

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_civic_space_open", "set_country_flag = COLDWAR_KOR_civic_legal_5", "set_country_flag = COLDWAR_KOR_civic_legal_19"]`

### A Broad Coalition

`COLDWAR_KOR_broad_democratic_coalition` · **35 days** · grid (80, 5) · owner: national

Bring parliamentary opposition, religious groups, students and workers into a negotiating forum without pretending they are one party.

Prerequisites: (open_civic_space).
Exclusive with: none.

- Replace transition:coalition_forum:
- Political power gain: -4%
- Weekly bureaucracy expenses: +3%
- action: register_charter_participants

### Security Records

`COLDWAR_KOR_open_security_records` · **35 days** · grid (84, 5) · owner: national

Preserve records of emergency rule and state violence. If Gwangju or other repression occurred, their cases enter this process.

Prerequisites: (open_civic_space).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace transition:records:
- Intelligence network gain: -2%
- Weekly bureaucracy expenses: +3%
- action: preserve_case_records

### An Electoral Unity Pact

`COLDWAR_KOR_unity_ticket` · **35 days** · grid (79, 6) · owner: national

Negotiate a common electoral ticket. Both Kims retain political careers; neither is automatically appointed or permanently excluded.

Prerequisites: (broad_democratic_coalition).
Exclusive with: independent_tickets.

- Replace transition:campaign_settlement:
- Stability: +3%
- Political power gain: -5%
- action: negotiate_unity_ticket

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_unified_ticket"]`

### Independent Tickets

`COLDWAR_KOR_independent_tickets` · **35 days** · grid (81, 6) · owner: national

Preserve separate party organizations and programme autonomy, accepting electoral fragmentation and coalition tension.

Prerequisites: (broad_democratic_coalition).
Exclusive with: unity_ticket.

- Replace transition:campaign_settlement:
- Political power gain: +8%
- Stability: -2%
- action: retain_separate_tickets

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_separate_tickets"]`

### Independent Inquiry

`COLDWAR_KOR_independent_inquiry` · **35 days** · grid (83, 6) · owner: national

Investigate responsibility through civilian evidence and due process, at administrative and security-transition cost.

Prerequisites: (open_security_records).
Exclusive with: conditional_amnesty.

- Treasury: -$1bn (once)
- Replace transition:accountability:
- Stability: +4%
- Weekly bureaucracy expenses: +7%
- Intelligence network gain: -3%
- action: independent_repression_inquiry

### Conditional Amnesty

`COLDWAR_KOR_conditional_amnesty` · **35 days** · grid (85, 6) · owner: national

Trade limited, conditional guarantees and disclosure for officer cooperation. Credibility and accountability remain contested.

Prerequisites: (open_security_records).
Exclusive with: independent_inquiry.

- Replace transition:accountability:
- Division organization: +3%
- Stability: -2%
- Trade opinion factor: -2%
- Weekly bureaucracy expenses: +3%
- action: conditional_disclosure_compact

### A Negotiating Mandate

`COLDWAR_KOR_negotiating_mandate` · **35 days** · grid (82, 7) · owner: national

Reconcile the electoral pact and accountability terms before agreeing a constitutional model.

Prerequisites: (unity_ticket OR independent_tickets) AND (independent_inquiry OR conditional_amnesty).
Exclusive with: none.

- action: ratify_negotiating_mandate

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_charter_mandate"]`

### Presidential Democracy

`COLDWAR_KOR_presidential_democracy` · **49 days** · grid (80, 8) · owner: national

Retain an effective directly elected presidency under binding rights, term and oversight limits.

Prerequisites: (negotiating_mandate).
Exclusive with: parliamentary_democracy, consensus_presidency.

- Replace transition:constitution:
- Political power gain: +8%
- Stability: +3%
- Weekly bureaucracy expenses: +3%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_draft_presidential", "set_variable = { COLDWAR_KOR_charter_model = 1 }"]`

### One-Term Presidency

`COLDWAR_KOR_one_term_presidency` · **35 days** · grid (80, 9) · owner: national

Define enforceable terms, cabinet responsibility and appointment rules for the chosen constitutional model.

Prerequisites: (presidential_democracy).
Exclusive with: none.

- Replace transition:constitution:
- Political power gain: +10%
- Stability: +4%
- Weekly bureaucracy expenses: +3%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- Requirement: The chosen model remains a draft until the actual ratification event passes

### Parliamentary Cabinet

`COLDWAR_KOR_parliamentary_democracy` · **49 days** · grid (82, 8) · owner: national

Make the cabinet responsible to an elected Assembly. This is an alternate settlement grounded in Korean parliamentary experience and constitutional debates.

Prerequisites: (negotiating_mandate).
Exclusive with: presidential_democracy, consensus_presidency.

- Replace transition:constitution:
- Political power gain: -8%
- Stability: +7%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_draft_parliamentary", "set_variable = { COLDWAR_KOR_charter_model = 2 }"]`

### Cabinet Responsibility

`COLDWAR_KOR_cabinet_responsibility` · **35 days** · grid (82, 9) · owner: national

Define enforceable terms, cabinet responsibility and appointment rules for the chosen constitutional model.

Prerequisites: (parliamentary_democracy).
Exclusive with: none.

- Replace transition:constitution:
- Political power gain: -10%
- Stability: +8%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- Requirement: The chosen model remains a draft until the actual ratification event passes

### Consensus Presidency

`COLDWAR_KOR_consensus_presidency` · **49 days** · grid (84, 8) · owner: national

Retain direct election while binding executive action to a broad cabinet and parliamentary bargain. This is an alternate compromise, not the historical 1987 constitution.

Prerequisites: (negotiating_mandate).
Exclusive with: presidential_democracy, parliamentary_democracy.

- Replace transition:constitution:
- Political power gain: +2%
- Stability: +5%
- Weekly bureaucracy expenses: +8%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_draft_consensus", "set_variable = { COLDWAR_KOR_charter_model = 3 }"]`

### Coalition Assent Rules

`COLDWAR_KOR_coalition_veto_rules` · **35 days** · grid (84, 9) · owner: national

Define enforceable terms, cabinet responsibility and appointment rules for the chosen constitutional model.

Prerequisites: (consensus_presidency).
Exclusive with: none.

- Replace transition:constitution:
- Political power gain: +3%
- Stability: +6%
- Weekly bureaucracy expenses: +8%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- Requirement: The chosen model remains a draft until the actual ratification event passes

### Submit the Charter

`COLDWAR_KOR_constitution_referendum` · **49 days** · grid (82, 10) · owner: national

Submit the agreed text to a real ratification process. Rejection does not enable elections or grant the constitutional programme.

Prerequisites: (one_term_presidency OR cabinet_responsibility OR coalition_veto_rules).
Exclusive with: none.

- pp_once: -75 (once)
- action: submit_constitutional_ballot

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_ballot_pending", "country_event = { id = COLDWAR_KOR_transition.30 days = 30 }"]`

### An Impartial Ballot

`COLDWAR_KOR_impartial_election_board` · **35 days** · grid (82, 11) · owner: national

Restore lawful electoral competition using the actual party and coalition system; the result may return Roh, either Kim, or another eligible government.

Prerequisites: (constitution_referendum).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace transition:election_administration:
- Stability: +2%
- Political power gain: -3%
- Weekly bureaucracy expenses: +4%
- action: configure_lawful_election

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_constitutional_order", "clr_country_flag = COLDWAR_KOR_constitution_yushin", "clr_country_flag = COLDWAR_KOR_constitution_controlled_fifth", "clr_country_flag = COLDWAR_KOR_nationwide_martial_law"]`

### An Uncensored Press

`COLDWAR_KOR_uncensored_press` · **35 days** · grid (80, 12) · owner: national

Protect publication and criticism. These legal rules have enforcement and rollback conditions, not an invented press-freedom meter.

Prerequisites: (impartial_election_board).
Exclusive with: none.

- Replace transition:press_rights:
- Research speed: +3%
- Trade opinion factor: +4%
- Political power gain: -4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: protect_civil_press

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_press_protected"]`

### Security Accountability

`COLDWAR_KOR_accountable_intelligence` · **35 days** · grid (84, 12) · owner: national

Separate external intelligence from political surveillance and require warrants and civilian review.

Prerequisites: (impartial_election_board).
Exclusive with: none.

- Replace transition:intelligence_law:
- Encryption: +4%
- Intelligence network gain: -4%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: warranted_security_operations

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_security_warrants"]`

### Constitutional Court

`COLDWAR_KOR_independent_constitutional_court` · **35 days** · grid (80, 13) · owner: national

Create enforceable constitutional review of exceptional powers. The court is a national institution, not a party-specific research bonus.

Prerequisites: (uncensored_press).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace transition:court:
- Stability: +3%
- Political power gain: -4%
- Weekly bureaucracy expenses: +4%
- Active only after Constitutional order and actually operational judicial review
- action: constitutional_review_rules
- Requirement: Enacts the court mandate; appointments and funded implementation must then be completed by decision before judicial review operates

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_judicial_review"]`

### Civilian Appointments

`COLDWAR_KOR_civilian_appointments` · **35 days** · grid (84, 13) · owner: national

Put command appointments under the lawful civilian government without claiming that officer networks disappear immediately.

Prerequisites: (accountable_intelligence).
Exclusive with: none.

- Replace transition:appointment_law:
- Division organization: -2%
- Stability: +2%
- Weekly personnel expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: bind_civilian_appointments

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_civilian_appointments"]`

### Retire Political Clubs

`COLDWAR_KOR_retire_political_networks` · **35 days** · grid (83, 14) · owner: national

Retire political officer networks with pensions and a temporary command disruption. Dismantling Hanahoe before 1993 is an explicit alternate outcome.

Prerequisites: (civilian_appointments).
Exclusive with: staged_officer_retirement.

- Treasury: -$2bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace transition:officer_settlement:
- Division organization: +5%
- Stability: +3%
- Weekly personnel expenses: +8%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: accelerated_officer_retirement

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_officer_networks_retired"]`

Temporary adjustment: `{"id": "COLDWAR_KOR_officer_retirement_disruption", "days": 180, "modifiers": {"army_org_factor": -0.05, "political_power_factor": -0.05}}`

### Phased Retirement

`COLDWAR_KOR_staged_officer_retirement` · **35 days** · grid (85, 14) · owner: national

Preserve near-term command continuity through phased retirement, larger pension obligations and an enforceable review timetable.

Prerequisites: (civilian_appointments).
Exclusive with: retire_political_networks.

- Active programme: $0.00200bn/week (replacement slot)
- Replace transition:officer_settlement:
- Division organization: +6%
- Stability: +1%
- Weekly personnel expenses: +12%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: staged_officer_retirement

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_officer_retirement_schedule"]`

### Parliamentary Audits

`COLDWAR_KOR_parliamentary_audits` · **35 days** · grid (82, 15) · owner: national

Restore legislative scrutiny over public finance and state abuses, including hearings when the historical cases exist.

Prerequisites: (retire_political_networks OR staged_officer_retirement) AND (independent_constitutional_court).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace transition:budget_oversight:
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Political power gain: -3%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: restore_assembly_audits

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_assembly_audit_rights"]`

### Labour Bargaining

`COLDWAR_KOR_restore_labour_bargaining` · **35 days** · grid (80, 16) · owner: national

Establish lawful independent representation and then use the actual MD labor-faction opinion effect. Existing faction state is never reset.

Prerequisites: (parliamentary_audits).
Exclusive with: none.

- Replace transition:labour_law:
- Stability: +3%
- Weekly social expenses: +4%
- Civilian industry productivity: -2%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: register_native_labor_faction

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_lawful_labour_bargaining"]`

### Prepare Local Councils

`COLDWAR_KOR_prepare_local_councils` · **35 days** · grid (84, 16) · owner: national

Restore the legal basis and timetable for local councils. Historical council elections in 1991 and executive elections in 1995 remain outside this horizon.

Prerequisites: (parliamentary_audits).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace transition:local_government:
- Agricultural productivity: +3%
- Stability: +2%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: prepare_local_autonomy_law

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_local_autonomy_prepared"]`

### Constitutional Security

`COLDWAR_KOR_constitutional_security` · **35 days** · grid (82, 17) · owner: national

Bind public security to constitutional law. Legal civilian control is distinct from removing every military-era political network.

Prerequisites: (restore_labour_bargaining) AND (prepare_local_councils).
Exclusive with: none.

- Replace transition:transition_phase:
- Political power gain: +0%
- Weekly bureaucracy expenses: +0%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- Replace starting problem: political_command

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_civilian_control", "clr_country_flag = COLDWAR_KOR_transition_open"]`

### An Orderly Handover

`COLDWAR_KOR_orderly_handover` · **35 days** · grid (80, 18) · owner: national

Recognize an actual lawful election and transfer. The constitutional branch never appoints a predetermined winner.

Prerequisites: (constitutional_security).
Exclusive with: none.

- pp_once: +75 (once)
- action: confirm_native_handover

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_lawful_handover"]`

### Defend the New Order

`COLDWAR_KOR_defend_new_order` · **35 days** · grid (84, 18) · owner: national

Require lawful authorization for emergency powers and a recorded public constitutional process for reversal. A coup or rollback can still occur, with explicit costs.

Prerequisites: (constitutional_security).
Exclusive with: none.

- Replace transition:democratic_safeguards:
- Political power gain: -3%
- Weekly police expenses: +3%
- Ideological drift defence: +8%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: enforce_democratic_safeguards

Institutional outcomes: `["set_country_flag = COLDWAR_KOR_democratic_safeguards"]`

## DRP · Park and the developmental state

Entry condition: check_variable = { ruling_party = 0 } AND actual Park incumbent.

### Developmental State

`COLDWAR_KOR_developmental_state` · **14 days** · grid (4, 0) · owner: leader:Park Chung Hee

Park directs the ministries through the Economic Planning Board. Rapid execution rests on a contested presidential mandate.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace drp:mandate:
- Construction speed: +4%
- Stability: -3%
- pp_once: +50 (once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Yushin Constitution

`COLDWAR_KOR_yushin` · **70 days** · grid (3, 1) · owner: leader:Park Chung Hee

Concentrate executive authority and replace direct presidential competition with controlled institutions.

Prerequisites: (developmental_state).
Exclusive with: constitutional_drp.

- Replace drp:constitution:
- Political power gain: +18%
- Stability: -8%
- Trade opinion factor: -5%
- action: yushin_institutions
- Replace starting problem: presidency
- Requirement: A completed presidential contest or genuine constitutional crisis; actual Park/DRP government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Civilian Conservatism

`COLDWAR_KOR_constitutional_drp` · **35 days** · grid (5, 1) · owner: leader:Park Chung Hee

Retain conservative development policy under a competitive constitutional settlement.

Prerequisites: (developmental_state).
Exclusive with: yushin.

- Replace drp:constitution:
- Stability: +5%
- Political power gain: -8%
- action: constitutional_reform_commitment
- Replace starting problem: presidency
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Emergency Decrees

`COLDWAR_KOR_emergency_decrees` · **35 days** · grid (3, 2) · owner: leader:Park Chung Hee

Emergency powers accelerate decisions while surveillance and repression widen the legitimacy crisis.

Prerequisites: (yushin).
Exclusive with: none.

- Replace drp:constitution:
- Political power gain: +23%
- Stability: -10%
- Weekly police expenses: +8%
- Trade opinion factor: -5%
- Requirement: Yushin constitutional settlement remains in force
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Assembly Bargaining

`COLDWAR_KOR_assembly_bargain` · **35 days** · grid (5, 2) · owner: leader:Park Chung Hee

Accept legislative bargaining and scrutiny in return for a more durable civilian mandate.

Prerequisites: (constitutional_drp).
Exclusive with: none.

- Replace drp:constitution:
- Stability: +8%
- Political power gain: -10%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Professional Cabinet

`COLDWAR_KOR_presidential_administration` · **35 days** · grid (4, 3) · owner: leader:Park Chung Hee

A professional cabinet gives either constitutional settlement an administrative foundation.

Prerequisites: (emergency_decrees OR assembly_bargain).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace drp:cabinet:
- Construction speed: +4%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### The Chaebol Compact

`COLDWAR_KOR_chaebol_compact` · **35 days** · grid (3, 4) · owner: leader:Park Chung Hee

Channel policy credit through major business groups; concentrated guarantees deepen financial exposure.

Prerequisites: (presidential_administration).
Exclusive with: competitive_credit.

- Active programme: $0.00300bn/week (replacement slot)
- Replace drp:credit:
- Interest rate (percentage points before native clamps): +0.35 percentage points
- Civilian industry productivity: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Competitive Credit

`COLDWAR_KOR_competitive_credit` · **35 days** · grid (5, 4) · owner: leader:Park Chung Hee

Distribute development finance to smaller exporters, sacrificing conglomerate economies of scale.

Prerequisites: (presidential_administration).
Exclusive with: chaebol_compact.

- Treasury: -$1bn (once)
- Replace drp:credit:
- Civilian factory construction: +8%
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Civilian industry productivity: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Enforce Export Targets

`COLDWAR_KOR_export_targets` · **35 days** · grid (3, 5) · owner: leader:Park Chung Hee

Reward firms that meet overseas sales targets, at the cost of leverage and workplace pressure.

Prerequisites: (chaebol_compact).
Exclusive with: none.

- Active programme: $0.00400bn/week (replacement slot)
- Replace drp:credit:
- Interest rate (percentage points before native clamps): +0.45 percentage points
- Stability: -3%
- Civilian industry productivity: +12%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Protect Subcontractors

`COLDWAR_KOR_subcontractor_guarantees` · **35 days** · grid (5, 5) · owner: leader:Park Chung Hee

Enforce contracts and protect provincial suppliers from dominant buyers.

Prerequisites: (competitive_credit).
Exclusive with: none.

- Replace drp:credit:
- Civilian factory construction: +10%
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Weekly bureaucracy expenses: +4%
- Civilian industry productivity: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Strengthen the EPB

`COLDWAR_KOR_planning_board` · **35 days** · grid (4, 6) · owner: leader:Park Chung Hee

Strengthen the existing Economic Planning Board rather than create a parallel economic authority.

Prerequisites: (export_targets OR subcontractor_guarantees).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace drp:planning:
- Construction speed: +3%
- Weekly bureaucracy expenses: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Mobilize the Villages

`COLDWAR_KOR_mobilized_villages` · **35 days** · grid (3, 7) · owner: leader:Park Chung Hee

Use state-led village mobilization to deliver rural development and extend presidential influence.

Prerequisites: (planning_board).
Exclusive with: rural_cooperatives.

- Active programme: $0.00200bn/week (replacement slot)
- Replace drp:rural:
- Agricultural productivity: +8%
- Political power gain: +4%
- Stability: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Rural Cooperatives

`COLDWAR_KOR_rural_cooperatives` · **35 days** · grid (5, 7) · owner: leader:Park Chung Hee

Give cooperatives control over rural credit and priorities, limiting central mobilization.

Prerequisites: (planning_board).
Exclusive with: mobilized_villages.

- Active programme: $0.00200bn/week (replacement slot)
- Replace drp:rural:
- Agricultural productivity: +7%
- Stability: +3%
- Political power gain: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Village Grants

`COLDWAR_KOR_performance_grants` · **35 days** · grid (3, 8) · owner: leader:Park Chung Hee

Reward successful villages, accepting uneven access and political dependence.

Prerequisites: (mobilized_villages).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace drp:rural:
- Agricultural productivity: +12%
- Political power gain: +4%
- Stability: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Village Elections

`COLDWAR_KOR_village_accounts` · **35 days** · grid (5, 8) · owner: leader:Park Chung Hee

Local audits improve trust while slowing central allocation.

Prerequisites: (rural_cooperatives).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace drp:rural:
- Agricultural productivity: +9%
- Stability: +5%
- Political power gain: -5%
- Weekly bureaucracy expenses: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Connect the Provinces

`COLDWAR_KOR_balanced_provinces` · **49 days** · grid (4, 9) · owner: leader:Park Chung Hee

Extend transport links beyond the dominant southeastern corridor.

Prerequisites: (performance_grants OR village_accounts).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 606: +1 infrastructure (paid, once)
- State 607: +1 infrastructure (paid, once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Managed Succession

`COLDWAR_KOR_dynastic_presidency` · **35 days** · grid (3, 10) · owner: leader:Park Chung Hee

Entrench continuity through a managed civilian succession; no hereditary transfer or automatic incumbent replacement.

Prerequisites: (balanced_provinces).
Exclusive with: civilian_handover.

- Replace drp:succession:
- Political power gain: +12%
- Stability: -5%
- condition: Yushin settlement
- action: managed_succession
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: Yushin settlement

### A Civilian Handover

`COLDWAR_KOR_civilian_handover` · **35 days** · grid (5, 10) · owner: leader:Park Chung Hee

Prepare a constitutional transfer, trading presidential discretion for legitimacy.

Prerequisites: (balanced_provinces).
Exclusive with: dynastic_presidency.

- Replace drp:succession:
- Stability: +6%
- Political power gain: -8%
- action: open_succession
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Development Accounts

`COLDWAR_KOR_drp_budget_charter` · **35 days** · grid (4, 11) · owner: leader:Park Chung Hee

Publish the development budget and subject credit guarantees to a defined approval process.

Prerequisites: (dynastic_presidency OR civilian_handover).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace drp:oversight:
- Construction speed: +4%
- Weekly bureaucracy expenses: +5%

### Technocratic Mandates

`COLDWAR_KOR_drp_technocrats` · **35 days** · grid (3, 12) · owner: leader:Park Chung Hee

Give the planners professional discretion while limiting presidential patronage.

Prerequisites: (drp_budget_charter).
Exclusive with: drp_provincial_brokers.

- Treasury: -$1bn (once)
- Replace drp:administrative_base:
- Research speed: +4%
- Weekly education expenses: +6%
- Political power gain: -4%

### Provincial Bargains

`COLDWAR_KOR_drp_provincial_brokers` · **35 days** · grid (5, 12) · owner: leader:Park Chung Hee

Trade central discretion for provincial cooperation and funded rural administration.

Prerequisites: (drp_budget_charter).
Exclusive with: drp_technocrats.

- Active programme: $0.00200bn/week (replacement slot)
- Replace drp:administrative_base:
- Agricultural productivity: +8%
- Stability: +4%
- Weekly bureaucracy expenses: +6%

## NDP · constitutional opposition

Entry condition: check_variable = { ruling_party = 1 }.

### Parliamentary Rule

`COLDWAR_KOR_parliamentary_government` · **14 days** · grid (12, 0) · owner: party:1

A governing New Democratic Party restores parliamentary opposition rights and independent political association.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace ndp:mandate:
- Stability: +4%
- Political power gain: -5%
- action: restore_civil_liberties
- Replace starting problem: presidency
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Parliamentary Republic

`COLDWAR_KOR_parliamentary_republic` · **70 days** · grid (11, 1) · owner: party:1

Build a cabinet responsible to the Assembly; coalition bargaining constrains executive speed.

Prerequisites: (parliamentary_government).
Exclusive with: checked_presidency.

- Replace ndp:constitution:
- Stability: +7%
- Political power gain: -10%
- action: parliamentary_republic
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Checked Presidency

`COLDWAR_KOR_checked_presidency` · **70 days** · grid (13, 1) · owner: party:1

Keep an effective presidency subject to term limits and parliamentary scrutiny.

Prerequisites: (parliamentary_government).
Exclusive with: parliamentary_republic.

- Replace ndp:constitution:
- Political power gain: +6%
- Stability: +2%
- action: presidential_term_limits
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Coalition Committees

`COLDWAR_KOR_coalition_committees` · **35 days** · grid (11, 2) · owner: party:1

Make committee oversight permanent despite the administrative cost.

Prerequisites: (parliamentary_republic).
Exclusive with: none.

- Replace ndp:constitution:
- Stability: +9%
- Political power gain: -12%
- Weekly bureaucracy expenses: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### An Independent Court

`COLDWAR_KOR_constitutional_court` · **35 days** · grid (13, 2) · owner: party:1

Judicial review strengthens rights while imposing an additional administrative burden.

Prerequisites: (checked_presidency).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace ndp:constitution:
- Political power gain: +4%
- Stability: +6%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Review the Civil Service

`COLDWAR_KOR_civil_service_review` · **35 days** · grid (12, 3) · owner: party:1

Replace political appointments with accountable professional administration.

Prerequisites: (coalition_committees OR constitutional_court).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace ndp:service:
- Weekly bureaucracy expenses: -4%
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Competitive Market

`COLDWAR_KOR_market_conservatives` · **35 days** · grid (11, 4) · owner: party:1

Open credit allocation and restrain preferential guarantees, accepting slower conglomerate expansion.

Prerequisites: (civil_service_review).
Exclusive with: social_conservatives.

- Replace ndp:enterprise:
- Interest rate (percentage points before native clamps): -0.35 percentage points
- Civilian factory construction: +6%
- Civilian industry productivity: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Social Market Pact

`COLDWAR_KOR_social_conservatives` · **35 days** · grid (13, 4) · owner: party:1

Preserve private enterprise while underwriting social compromise.

Prerequisites: (civil_service_review).
Exclusive with: market_conservatives.

- Active programme: $0.00200bn/week (replacement slot)
- Replace ndp:enterprise:
- Stability: +6%
- Weekly social expenses: +8%
- Civilian industry productivity: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Open Public Tenders

`COLDWAR_KOR_open_tenders` · **35 days** · grid (11, 5) · owner: party:1

Transparent procurement benefits new suppliers at an administrative cost.

Prerequisites: (market_conservatives).
Exclusive with: none.

- Replace ndp:enterprise:
- Interest rate (percentage points before native clamps): -0.4 percentage points
- Civilian factory construction: +9%
- Weekly bureaucracy expenses: +3%
- Civilian industry productivity: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Social Contributions

`COLDWAR_KOR_pension_contributions` · **35 days** · grid (13, 5) · owner: party:1

Contributory benefits broaden security but reduce resources available for immediate investment.

Prerequisites: (social_conservatives).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace ndp:enterprise:
- Stability: +8%
- Weekly social expenses: +10%
- Consumer goods factor: +1%
- Civilian industry productivity: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Regional Investment

`COLDWAR_KOR_regional_compromise` · **49 days** · grid (12, 6) · owner: party:1

Fund an industrial project in Honam to reduce the regional imbalance.

Prerequisites: (open_tenders OR pension_contributions).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 607: +1 industrial_complex (paid, once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Security Oversight

`COLDWAR_KOR_civilian_security` · **35 days** · grid (11, 7) · owner: party:1

Subject security agencies to civilian warrants and legislative oversight.

Prerequisites: (regional_compromise).
Exclusive with: security_compromise.

- Replace ndp:security:
- Stability: +5%
- Intelligence network gain: -4%
- action: intelligence_oversight
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### The Security Bargain

`COLDWAR_KOR_security_compromise` · **35 days** · grid (13, 7) · owner: party:1

Retain parts of the security apparatus, accepting continued civic distrust.

Prerequisites: (regional_compromise).
Exclusive with: civilian_security.

- Replace ndp:security:
- Intelligence network gain: +8%
- Stability: -4%
- Weekly police expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Civic Conservatism

`COLDWAR_KOR_democratic_conservatism` · **35 days** · grid (12, 8) · owner: party:1

Consolidate a constitutional conservative government with a credible international reputation.

Prerequisites: (civilian_security OR security_compromise).
Exclusive with: none.

- Replace ndp:settlement:
- Trade opinion factor: +8%
- Political power gain: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Transparent Taxation

`COLDWAR_KOR_ndp_tax_transparency` · **35 days** · grid (11, 9) · owner: party:1

Audit politically connected revenue arrangements; the review costs time and administrative resources.

Prerequisites: (democratic_conservatism).
Exclusive with: ndp_tax_compromise.

- Treasury: -$1bn (once)
- Replace ndp:revenue:
- Interest rate (percentage points before native clamps): -0.25 percentage points
- Weekly bureaucracy expenses: +5%
- Political power gain: -4%

### A Taxpayer Compact

`COLDWAR_KOR_ndp_tax_compromise` · **35 days** · grid (13, 9) · owner: party:1

Preserve investment through negotiated taxation, accepting narrower fiscal discipline.

Prerequisites: (democratic_conservatism).
Exclusive with: ndp_tax_transparency.

- Replace ndp:revenue:
- Civilian factory construction: +6%
- Stability: +3%
- Interest rate (percentage points before native clamps): +0.15 percentage points

### Provincial Services

`COLDWAR_KOR_ndp_municipal_services` · **49 days** · grid (12, 10) · owner: party:1

Fund provincial services and prepare local administration. Nationwide local elections are not claimed before 1991.

Prerequisites: (ndp_tax_transparency OR ndp_tax_compromise).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace ndp:local_admin:
- Agricultural productivity: +4%
- Weekly bureaucracy expenses: +4%
- State 607: +1 infrastructure (paid, once)

## Reform liberals · the Two Kims

Entry condition: check_variable = { ruling_party = 2 }.

### A Reform Mandate

`COLDWAR_KOR_reform_mandate` · **14 days** · grid (23, 0) · owner: party:2

A reform government reopens civic politics and reviews political imprisonment.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace reform:mandate:
- Stability: +5%
- Political power gain: -5%
- action: political_prisoner_review
- Replace starting problem: presidency
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Kim Young-sam

`COLDWAR_KOR_ys_civilian_authority` · **35 days** · grid (19, 1) · owner: leader:Kim Young-sam

Assert civilian authority over the officer corps, accepting a difficult transition in command.

Prerequisites: (reform_mandate).
Exclusive with: none.

- Replace reform:ys_base:
- Political power gain: +6%
- Division organization: -3%
- leader: Kim Young-sam
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Kim Dae-jung

`COLDWAR_KOR_dj_people_economy` · **35 days** · grid (27, 1) · owner: leader:Kim Dae-jung

Link civil rights to household welfare and regional inclusion.

Prerequisites: (reform_mandate).
Exclusive with: none.

- Replace reform:dj_base:
- Stability: +6%
- Weekly social expenses: +6%
- leader: Kim Dae-jung
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Financial Disclosure

`COLDWAR_KOR_financial_disclosure` · **35 days** · grid (18, 2) · owner: leader:Kim Young-sam

Require disclosure and curb hidden political finance.

Prerequisites: (ys_civilian_authority).
Exclusive with: negotiated_cleanup.

- Treasury: -$1bn (once)
- Replace reform:ys_finance:
- Interest rate (percentage points before native clamps): -0.4 percentage points
- Political power gain: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Negotiated Cleanup

`COLDWAR_KOR_negotiated_cleanup` · **35 days** · grid (20, 2) · owner: leader:Kim Young-sam

Secure business cooperation through phased accountability.

Prerequisites: (ys_civilian_authority).
Exclusive with: financial_disclosure.

- Replace reform:ys_finance:
- Construction speed: +6%
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Accountable Banking

`COLDWAR_KOR_real_name_accounts` · **35 days** · grid (18, 3) · owner: leader:Kim Young-sam

Require accountable financial records and transparent corporate ownership. This is an alternate precursor, not Kim Young-sam’s 1993 real-name-finance reform.

Prerequisites: (financial_disclosure).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace reform:ys_finance:
- Interest rate (percentage points before native clamps): -0.55 percentage points
- Political power gain: -7%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Corporate Transition

`COLDWAR_KOR_corporate_transition` · **35 days** · grid (20, 3) · owner: leader:Kim Young-sam

Preserve investment momentum while deferring part of the cleanup.

Prerequisites: (negotiated_cleanup).
Exclusive with: none.

- Replace reform:ys_finance:
- Construction speed: +8%
- Interest rate (percentage points before native clamps): +0.25 percentage points
- Stability: -2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Reform Coalition

`COLDWAR_KOR_ys_civil_coalition` · **35 days** · grid (19, 4) · owner: leader:Kim Young-sam

Build a durable civilian reform coalition with an ongoing cost in political bargaining.

Prerequisites: (real_name_accounts OR corporate_transition).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace reform:ys_coalition:
- Trade opinion factor: +6%
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Civilian Appointments

`COLDWAR_KOR_ys_consolidation` · **35 days** · grid (19, 5) · owner: leader:Kim Young-sam

Entrench accountable institutions rather than personal patronage.

Prerequisites: (ys_civil_coalition).
Exclusive with: none.

- Replace reform:ys_consolidation:
- Stability: +4%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Social Insurance

`COLDWAR_KOR_broad_welfare` · **35 days** · grid (26, 2) · owner: leader:Kim Dae-jung

Build broad social protection with a substantial recurring public commitment.

Prerequisites: (dj_people_economy).
Exclusive with: targeted_welfare.

- Active programme: $0.00300bn/week (replacement slot)
- Replace reform:dj_welfare:
- Stability: +8%
- Weekly social expenses: +15%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Targeted Protection

`COLDWAR_KOR_targeted_welfare` · **35 days** · grid (28, 2) · owner: leader:Kim Dae-jung

Target vulnerable households while keeping the fiscal commitment narrower.

Prerequisites: (dj_people_economy).
Exclusive with: broad_welfare.

- Active programme: $0.00100bn/week (replacement slot)
- Replace reform:dj_welfare:
- Stability: +4%
- Weekly bureaucracy expenses: +6%
- Civilian industry productivity: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Health Coverage

`COLDWAR_KOR_national_health_cover` · **35 days** · grid (26, 3) · owner: leader:Kim Dae-jung

Extend coverage to groups left outside employment-based protection.

Prerequisites: (broad_welfare).
Exclusive with: none.

- Active programme: $0.00400bn/week (replacement slot)
- Replace reform:dj_welfare:
- Stability: +10%
- Weekly social expenses: +15%
- Weekly health expenses: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Regional Equalization

`COLDWAR_KOR_regional_equalization` · **35 days** · grid (28, 3) · owner: leader:Kim Dae-jung

Direct assistance to excluded regions, accepting administrative complexity.

Prerequisites: (targeted_welfare).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace reform:dj_welfare:
- Stability: +6%
- Weekly bureaucracy expenses: +8%
- Civilian industry productivity: +5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Regional Inclusion

`COLDWAR_KOR_dj_civil_coalition` · **35 days** · grid (27, 4) · owner: leader:Kim Dae-jung

Build a durable civilian reform coalition with an ongoing cost in political bargaining.

Prerequisites: (national_health_cover OR regional_equalization).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace reform:dj_coalition:
- Trade opinion factor: +6%
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Labour Mediation

`COLDWAR_KOR_dj_consolidation` · **35 days** · grid (27, 5) · owner: leader:Kim Dae-jung

Entrench accountable institutions rather than personal patronage.

Prerequisites: (dj_civil_coalition).
Exclusive with: none.

- Replace reform:dj_consolidation:
- Stability: +4%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### The Civilian Republic

`COLDWAR_KOR_sixth_republic` · **49 days** · grid (23, 7) · owner: party:2

Consolidate competitive institutions under either reform leader.

Prerequisites: (ys_consolidation OR dj_consolidation).
Exclusive with: none.

- Replace reform:republic:
- Stability: +5%
- Political power gain: -4%
- action: confirm_constitutional_settlement
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Democratic Alliance

`COLDWAR_KOR_democratic_alliance` · **35 days** · grid (20, 8) · owner: party:2

Use democratic credibility to deepen the US alliance while accepting closer external influence.

Prerequisites: (sixth_republic).
Exclusive with: reform_nordpolitik.

- Replace reform:foreign:
- Trade opinion factor: +10%
- Foreign influence defence: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Reform Nordpolitik

`COLDWAR_KOR_reform_nordpolitik` · **35 days** · grid (26, 8) · owner: party:2

Explore northern diplomatic openings while keeping decisions under civilian oversight.

Prerequisites: (sixth_republic).
Exclusive with: democratic_alliance.

- Replace reform:foreign:
- Trade opinion factor: +6%
- Foreign influence defence: +6%
- Political power gain: -6%
- action: nordpolitik_negotiations
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Party Finance Rules

`COLDWAR_KOR_reform_party_accounts` · **35 days** · grid (23, 9) · owner: party:2

Make reform-party financing accountable without granting popularity or selecting the election winner.

Prerequisites: (democratic_alliance OR reform_nordpolitik).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace reform:party_finance:
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Political power gain: -4%
- Weekly bureaucracy expenses: +3%

### Public Contract Rules

`COLDWAR_KOR_ys_civilian_contracts` · **35 days** · grid (19, 10) · owner: leader:Kim Young-sam

Use competitive contracts and disclosure to constrain the old patronage networks.

Prerequisites: (reform_party_accounts).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace reform:ys_contracts:
- Civilian factory construction: +6%
- Weekly bureaucracy expenses: +4%
- Political power gain: -3%

### A Social Dialogue

`COLDWAR_KOR_dj_social_dialogue` · **35 days** · grid (27, 10) · owner: leader:Kim Dae-jung

Bring employers, independent unions and excluded provinces into a funded social bargain.

Prerequisites: (reform_party_accounts).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace reform:dj_dialogue:
- Stability: +4%
- Weekly social expenses: +8%
- Civilian industry productivity: +3%

### Lawful Succession

`COLDWAR_KOR_reform_lawful_succession` · **35 days** · grid (23, 11) · owner: party:2

Bind the reform government to the same rules that made its accession possible. The other reform leader may govern later.

Prerequisites: (ys_civilian_contracts OR dj_social_dialogue).
Exclusive with: none.

- Replace reform:succession:
- Stability: +4%
- Political power gain: -4%
- action: bind_electoral_succession

## Army / DJP · Chun and Roh

Entry condition: check_variable = { ruling_party = 22 }.

### Military Government

`COLDWAR_KOR_military_cabinet` · **14 days** · grid (34, 0) · owner: party:22

A military-led government relies on discipline and command networks rather than a civilian mandate.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace army:mandate:
- Division organization: +5%
- Stability: -5%
- xp: +15 (once)
- condition: actual military government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: actual military government

### The Fifth Republic

`COLDWAR_KOR_fifth_republic` · **70 days** · grid (33, 1) · owner: leader:Chun Doo-hwan

Institutionalize Chun’s controlled presidency and civilian party vehicle.

Prerequisites: (military_cabinet).
Exclusive with: managed_liberalization.

- Replace army:constitution:
- Political power gain: +15%
- Stability: -7%
- Weekly police expenses: +8%
- condition: Chun incumbent
- action: controlled_constitution
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: Chun incumbent

### Managed Liberalization

`COLDWAR_KOR_managed_liberalization` · **70 days** · grid (35, 1) · owner: party:22

Accept a negotiated constitutional opening while retaining conservative institutions.

Prerequisites: (military_cabinet).
Exclusive with: fifth_republic.

- Replace army:constitution:
- Stability: +6%
- Political power gain: -7%
- action: open_constitutional_negotiations
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Consolidate the Press

`COLDWAR_KOR_press_consolidation` · **35 days** · grid (33, 2) · owner: leader:Chun Doo-hwan

Centralize media and political supervision at a lasting cost to credibility.

Prerequisites: (fifth_republic).
Exclusive with: none.

- Replace army:constitution:
- Political power gain: +19%
- Stability: -9%
- Weekly police expenses: +10%
- Trade opinion factor: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Accept Direct Elections

`COLDWAR_KOR_june_declaration` · **35 days** · grid (35, 2) · owner: party:22

Restore direct presidential competition; this changes election rules rather than installing a predetermined winner.

Prerequisites: (managed_liberalization).
Exclusive with: none.

- Replace army:constitution:
- Stability: +10%
- Political power gain: -10%
- action: accept_direct_election_principle
- Replace starting problem: presidency
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Professional Officers

`COLDWAR_KOR_professional_officers` · **35 days** · grid (34, 3) · owner: party:22

Promote professional competence while funding a better paid officer corps.

Prerequisites: (press_consolidation OR june_declaration).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace army:officers:
- Division organization: +4%
- Weekly personnel expenses: +5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Stabilization First

`COLDWAR_KOR_stabilization_first` · **35 days** · grid (33, 4) · owner: party:22

Restrain inflation and implicit guarantees through a difficult industrial adjustment.

Prerequisites: (professional_officers).
Exclusive with: industrial_continuity.

- Replace army:stabilize:
- Interest rate (percentage points before native clamps): -0.6 percentage points
- Stability: -2%
- Civilian industry productivity: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Industrial Continuity

`COLDWAR_KOR_industrial_continuity` · **35 days** · grid (35, 4) · owner: party:22

Support strategic enterprises through the downturn, accepting renewed financial exposure.

Prerequisites: (professional_officers).
Exclusive with: stabilization_first.

- Active programme: $0.00300bn/week (replacement slot)
- Replace army:stabilize:
- Interest rate (percentage points before native clamps): +0.45 percentage points
- Civilian industry productivity: +7%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Industrial Adjustment

`COLDWAR_KOR_industrial_rationalization` · **35 days** · grid (33, 5) · owner: party:22

Restructure overextended industrial groups while preserving viable plants.

Prerequisites: (stabilization_first).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace army:stabilize:
- Interest rate (percentage points before native clamps): -0.7 percentage points
- Civilian industry productivity: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Export Recovery

`COLDWAR_KOR_export_recovery` · **35 days** · grid (35, 5) · owner: party:22

Coordinate export recovery through wage restraint and public support.

Prerequisites: (industrial_continuity).
Exclusive with: none.

- Active programme: $0.00400bn/week (replacement slot)
- Replace army:stabilize:
- Interest rate (percentage points before native clamps): +0.5 percentage points
- Stability: -3%
- Civilian industry productivity: +10%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Civil Administration

`COLDWAR_KOR_civil_administration` · **35 days** · grid (34, 6) · owner: party:22

Put routine administration in professional civilian hands.

Prerequisites: (industrial_rationalization OR export_recovery).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace army:administration:
- Weekly bureaucracy expenses: -4%
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### The Officer Networks

`COLDWAR_KOR_hanahoe_compact` · **35 days** · grid (33, 7) · owner: party:22

Preserve loyal command networks, accepting political interference and civic distrust.

Prerequisites: (civil_administration).
Exclusive with: retire_political_officers.

- Replace army:command:
- Division organization: +6%
- Political power gain: +4%
- Stability: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Retire Political Officers

`COLDWAR_KOR_retire_political_officers` · **35 days** · grid (35, 7) · owner: party:22

Remove political commands, accepting temporary disruption in exchange for public trust.

Prerequisites: (civil_administration).
Exclusive with: hanahoe_compact.

- Treasury: -$1bn (once)
- Replace army:command:
- Stability: +6%
- Division organization: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Security Continuity

`COLDWAR_KOR_security_continuity` · **35 days** · grid (33, 8) · owner: party:22

Retain coordinated security control under military-linked leadership.

Prerequisites: (hanahoe_compact).
Exclusive with: none.

- Replace army:command:
- Division organization: +8%
- Intelligence network gain: +6%
- Stability: -7%
- Weekly police expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Civilian Promotions

`COLDWAR_KOR_civilian_promotions` · **35 days** · grid (35, 8) · owner: party:22

Make promotion accountable to civilian institutions rather than private officer clubs.

Prerequisites: (retire_political_officers).
Exclusive with: none.

- Replace army:command:
- Stability: +9%
- Division organization: -2%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### International Opening

`COLDWAR_KOR_olympic_republic` · **35 days** · grid (34, 9) · owner: party:22

Use international engagement to improve access and recognition; sporting prestige cannot erase repression.

Prerequisites: (security_continuity OR civilian_promotions).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace army:opening:
- Trade opinion factor: +8%
- Weekly bureaucracy expenses: +3%
- condition: no active nationwide martial law
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: no active nationwide martial law

### Roh’s Nordpolitik

`COLDWAR_KOR_roh_nordpolitik` · **35 days** · grid (33, 10) · owner: leader:Roh Tae-woo

An elected Roh government explores diplomatic recognition and northern trade.

Prerequisites: (olympic_republic).
Exclusive with: none.

- Replace army:nordpolitik:
- Trade opinion factor: +10%
- Political power gain: -6%
- condition: Roh incumbent and competitive elections
- action: nordpolitik_negotiations
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: Roh incumbent and competitive elections

### A Conservative Merger

`COLDWAR_KOR_conservative_merger` · **35 days** · grid (35, 10) · owner: party:22

Negotiate an elite conservative coalition. No opposition party or incumbent is transferred without political agreement.

Prerequisites: (olympic_republic).
Exclusive with: none.

- Replace army:coalition:
- Political power gain: +12%
- Stability: -4%
- Active only after Actual conservative coalition agreement ratified by the participating party organizations
- action: conservative_merger
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Constitutional Service

`COLDWAR_KOR_army_constitutional_service` · **35 days** · grid (34, 11) · owner: party:22

Define the legal duties of the armed forces under the actual constitutional settlement.

Prerequisites: (roh_nordpolitik OR conservative_merger).
Exclusive with: none.

- Replace army:service_law:
- Division organization: +3%
- Political power gain: -3%
- Weekly bureaucracy expenses: +3%

### A Civilian Ministry

`COLDWAR_KOR_army_civilian_ministry` · **35 days** · grid (33, 12) · owner: party:22

Put ministerial appointments under lawful civilian authority; command adaptation has a short-run cost.

Prerequisites: (army_constitutional_service).
Exclusive with: army_advisory_council.

- Treasury: -$1bn (once)
- Replace army:command_settlement:
- Stability: +5%
- Division organization: -2%
- Weekly personnel expenses: +5%

### An Advisory Council

`COLDWAR_KOR_army_advisory_council` · **35 days** · grid (35, 12) · owner: party:22

Retain formal military advice while accepting a slower and politically contested civilianization.

Prerequisites: (army_constitutional_service).
Exclusive with: army_civilian_ministry.

- Active programme: $0.00100bn/week (replacement slot)
- Replace army:command_settlement:
- Division organization: +6%
- Stability: -3%
- Weekly bureaucracy expenses: +5%

## USP · social democracy

Entry condition: check_variable = { ruling_party = 3 }.

### Social Democracy

`COLDWAR_KOR_social_democratic_cabinet` · **14 days** · grid (4, 14) · owner: party:3

Kim Chul’s small socialist tradition becomes a governing coalition through a credible democratic opening.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace usp:mandate:
- Stability: +4%
- Weekly social expenses: +5%
- condition: legal USP government
- Replace starting problem: presidency
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: legal USP government

### Universal Provision

`COLDWAR_KOR_universal_insurance` · **35 days** · grid (3, 15) · owner: party:3

Make social protection a national entitlement financed by a broad public commitment.

Prerequisites: (social_democratic_cabinet).
Exclusive with: contributory_welfare.

- Active programme: $0.00300bn/week (replacement slot)
- Replace usp:welfare:
- Stability: +8%
- Weekly social expenses: +16%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Contributory Welfare

`COLDWAR_KOR_contributory_welfare` · **35 days** · grid (5, 15) · owner: party:3

Build a narrower, employment-funded system with lower immediate public spending.

Prerequisites: (social_democratic_cabinet).
Exclusive with: universal_insurance.

- Active programme: $0.00100bn/week (replacement slot)
- Replace usp:welfare:
- Stability: +5%
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Rural Health Provision

`COLDWAR_KOR_rural_health` · **35 days** · grid (3, 16) · owner: party:3

Extend protection to farming and informal households outside large-company employment.

Prerequisites: (universal_insurance).
Exclusive with: none.

- Active programme: $0.00400bn/week (replacement slot)
- Replace usp:welfare:
- Stability: +10%
- Weekly social expenses: +16%
- Weekly health expenses: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Portable Benefits

`COLDWAR_KOR_portable_benefits` · **35 days** · grid (5, 16) · owner: party:3

Carry benefits across employers while accepting a complex contribution system.

Prerequisites: (contributory_welfare).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace usp:welfare:
- Stability: +7%
- Weekly bureaucracy expenses: +7%
- Civilian industry productivity: +5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Independent Unions

`COLDWAR_KOR_independent_unions` · **35 days** · grid (4, 17) · owner: party:3

Legalize independent collective organization; exporters must accommodate bargaining.

Prerequisites: (rural_health OR portable_benefits).
Exclusive with: none.

- Replace usp:labour:
- Stability: +5%
- Civilian industry productivity: -3%
- action: independent_union_law
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Public Credit

`COLDWAR_KOR_public_credit` · **35 days** · grid (3, 18) · owner: party:3

Keep credit allocation accountable to public institutions rather than conglomerates.

Prerequisites: (independent_unions).
Exclusive with: social_market_industry.

- Treasury: -$1bn (once)
- Replace usp:ownership:
- Civilian factory construction: +8%
- Interest rate (percentage points before native clamps): +0.25 percentage points
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Social Market

`COLDWAR_KOR_social_market_industry` · **35 days** · grid (5, 18) · owner: party:3

Preserve private industry under binding employment and wage agreements.

Prerequisites: (independent_unions).
Exclusive with: public_credit.

- Replace usp:ownership:
- Weekly social expenses: +5%
- Civilian industry productivity: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Cooperative Industry

`COLDWAR_KOR_cooperative_industry` · **35 days** · grid (3, 19) · owner: party:3

Support producer cooperatives at the cost of capital and administrative effort.

Prerequisites: (public_credit).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace usp:ownership:
- Civilian factory construction: +10%
- Interest rate (percentage points before native clamps): +0.3 percentage points
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Works Councils

`COLDWAR_KOR_works_councils` · **35 days** · grid (5, 19) · owner: party:3

Give labor representation in company decisions, exchanging speed for coordination.

Prerequisites: (social_market_industry).
Exclusive with: none.

- Replace usp:ownership:
- Political power gain: -4%
- Weekly social expenses: +5%
- Civilian industry productivity: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Provincial Opportunity

`COLDWAR_KOR_balanced_development` · **49 days** · grid (4, 20) · owner: party:3

Support industrial employment outside established corporate centers.

Prerequisites: (cooperative_industry OR works_councils).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 607: +1 industrial_complex (paid, once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Socialist Voice

`COLDWAR_KOR_socialist_alliance` · **35 days** · grid (3, 21) · owner: party:3

Maintain an independent democratic left and cultivate foreign social-democratic contacts.

Prerequisites: (balanced_development).
Exclusive with: neutral_peace.

- Replace usp:external:
- Foreign influence defence: +10%
- Trade opinion factor: -4%
- action: socialist_international_contacts
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Armed Neutrality

`COLDWAR_KOR_neutral_peace` · **35 days** · grid (5, 21) · owner: party:3

Negotiate international neutrality while maintaining a funded defense. Treaty withdrawal needs a separate accepted settlement.

Prerequisites: (balanced_development).
Exclusive with: socialist_alliance.

- Replace usp:external:
- Foreign influence defence: +6%
- Division defence: +4%
- Weekly personnel expenses: +6%
- offer: neutrality_guarantees
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Social Partnership

`COLDWAR_KOR_labour_republic` · **35 days** · grid (4, 22) · owner: party:3

Consolidate a democratic labor settlement without adopting Pyongyang’s political system.

Prerequisites: (socialist_alliance OR neutral_peace).
Exclusive with: none.

- Replace usp:settlement:
- Stability: +5%
- Political power gain: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A National Wage Floor

`COLDWAR_KOR_usp_national_wage_floor` · **35 days** · grid (3, 23) · owner: party:3

Set an enforceable minimum floor, accepting costs in low-margin export firms.

Prerequisites: (labour_republic).
Exclusive with: usp_sectoral_bargaining.

- Treasury: -$1bn (once)
- Replace usp:wage_settlement:
- Stability: +5%
- Weekly social expenses: +6%
- Civilian industry productivity: -3%

### Sectoral Bargaining

`COLDWAR_KOR_usp_sectoral_bargaining` · **35 days** · grid (5, 23) · owner: party:3

Negotiate sector agreements that suit different industries, accepting uneven coverage and administrative complexity.

Prerequisites: (labour_republic).
Exclusive with: usp_national_wage_floor.

- Active programme: $0.00100bn/week (replacement slot)
- Replace usp:wage_settlement:
- Stability: +2%
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +4%

## Students and independent Marxists

Entry condition: Exact governing slot 5 or 19; separate roots below.

### A Civic Cabinet

`COLDWAR_KOR_student_cabinet` · **14 days** · grid (10, 14) · owner: party:5

A radical civic coalition turns campus mobilization into accountable government; this is alternate history.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace minjung:student_base:
- Research speed: +3%
- Political power gain: -7%
- condition: legalized student-led civilian government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: legalized student-led civilian government

### Campus Pluralism

`COLDWAR_KOR_campus_pluralism` · **35 days** · grid (9, 15) · owner: party:5

Protect universities and open debate while funding a wider educational mission.

Prerequisites: (student_cabinet).
Exclusive with: national_service_schools.

- Replace minjung:student_education:
- Research speed: +5%
- Weekly education expenses: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Service Schools

`COLDWAR_KOR_national_service_schools` · **35 days** · grid (11, 15) · owner: party:5

Link civic service to technical education, diverting young people from civilian careers.

Prerequisites: (student_cabinet).
Exclusive with: campus_pluralism.

- Replace minjung:student_education:
- Army training time: -8%
- Recruitable population factor: +4%
- Weekly education expenses: +6%
- Political power gain: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Technical Scholarships

`COLDWAR_KOR_technical_scholarships` · **35 days** · grid (9, 16) · owner: party:5

Widen technical education instead of relying only on elite institutions.

Prerequisites: (campus_pluralism).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace minjung:student_education:
- Research speed: +7%
- Weekly education expenses: +10%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Community Service

`COLDWAR_KOR_community_service` · **35 days** · grid (11, 16) · owner: party:5

Expand a compulsory service programme with practical training and a wider obligation.

Prerequisites: (national_service_schools).
Exclusive with: none.

- Replace minjung:student_education:
- Army training time: -10%
- Recruitable population factor: +6%
- Weekly education expenses: +8%
- Political power gain: -5%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Civic Charter

`COLDWAR_KOR_civic_charter` · **35 days** · grid (10, 17) · owner: party:5

Make the civic coalition constitutional rather than a permanent campus emergency.

Prerequisites: (technical_scholarships OR community_service).
Exclusive with: none.

- Replace minjung:student_charter:
- Stability: +6%
- Political power gain: -5%
- action: civic_pluralism
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Investment Accounts

`COLDWAR_KOR_student_cabinet_public_accounts` · **35 days** · grid (10, 18) · owner: party:5

Publish investment accounts to constrain insider privilege and improve public credit.

Prerequisites: (civic_charter).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace minjung:student_cabinet_accounts:
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Independent Socialism

`COLDWAR_KOR_independent_left` · **14 days** · grid (16, 14) · owner: party:19

A southern socialist coalition claims independence from both blocs; it is an explicitly alternate route.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace minjung:left_base:
- Foreign influence defence: +8%
- Trade opinion factor: -5%
- condition: legal independent Marxist government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: legal independent Marxist government

### Worker Management

`COLDWAR_KOR_worker_management` · **35 days** · grid (15, 15) · owner: party:19

Give workplace councils managerial authority, accepting slower investment decisions.

Prerequisites: (independent_left).
Exclusive with: strategic_public_sector.

- Replace minjung:left_ownership:
- Political power gain: -8%
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +7%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Strategic Public Firms

`COLDWAR_KOR_strategic_public_sector` · **35 days** · grid (17, 15) · owner: party:19

Nationalize strategic credit and infrastructure without absorbing every small enterprise.

Prerequisites: (independent_left).
Exclusive with: worker_management.

- Treasury: -$2bn (once)
- Replace minjung:left_ownership:
- Interest rate (percentage points before native clamps): +0.3 percentage points
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Industrial Councils

`COLDWAR_KOR_industrial_councils` · **35 days** · grid (15, 16) · owner: party:19

Coordinate sector-wide worker management under a public investment plan.

Prerequisites: (worker_management).
Exclusive with: none.

- Replace minjung:left_ownership:
- Political power gain: -10%
- Weekly bureaucracy expenses: +7%
- Civilian industry productivity: +10%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Public Holding Fund

`COLDWAR_KOR_public_holding_fund` · **35 days** · grid (17, 16) · owner: party:19

Concentrate capital in publicly owned industrial holdings with explicit financial exposure.

Prerequisites: (strategic_public_sector).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace minjung:left_ownership:
- Interest rate (percentage points before native clamps): +0.4 percentage points
- Weekly bureaucracy expenses: +7%
- Civilian industry productivity: +9%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Southern Socialism

`COLDWAR_KOR_southern_socialism` · **35 days** · grid (16, 17) · owner: party:19

Open dialogue with the North without conceding Southern sovereignty or automatic annexation.

Prerequisites: (industrial_councils OR public_holding_fund).
Exclusive with: none.

- Replace minjung:left_charter:
- Foreign influence defence: +8%
- Division defence: +4%
- Trade opinion factor: -4%
- offer: independent_left_dialogue
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Public Accounts

`COLDWAR_KOR_independent_left_public_accounts` · **35 days** · grid (16, 18) · owner: party:19

Publish investment accounts to constrain insider privilege and improve public credit.

Prerequisites: (southern_socialism).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace minjung:independent_left_accounts:
- Interest rate (percentage points before native clamps): -0.2 percentage points
- Political power gain: -3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Campus and Workplace

`COLDWAR_KOR_student_workplace_alliance` · **35 days** · grid (10, 19) · owner: party:5

Link civic education to actual workplace representation without claiming that workers form one party.

Prerequisites: (student_cabinet_public_accounts).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace minjung:civic_training:
- Research speed: +3%
- Weekly education expenses: +5%
- Political power gain: -4%

### Public Procurement

`COLDWAR_KOR_left_public_procurement` · **35 days** · grid (16, 19) · owner: party:19

Give public enterprises accountable procurement instead of insider allocation.

Prerequisites: (independent_left_public_accounts).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace minjung:left_procurement:
- Weekly bureaucracy expenses: +5%
- Interest rate (percentage points before native clamps): +0.15 percentage points
- Civilian industry productivity: +5%

### Civic Association Law

`COLDWAR_KOR_civic_association_law` · **35 days** · grid (13, 20) · owner: national

Protect plural civic associations as a national legal institution that survives ordinary cabinet changes.

Prerequisites: (student_workplace_alliance OR left_public_procurement).
Exclusive with: none.

- Replace minjung:associations:
- Research speed: +2%
- Political power gain: -3%
- Weekly bureaucracy expenses: +4%
- Active only after has_country_flag = COLDWAR_KOR_constitutional_order
- action: legal_civic_associations

## RPR · revolutionary reunification

Entry condition: check_variable = { ruling_party = 4 }.

### Revolutionary Cabinet

`COLDWAR_KOR_revolutionary_cabinet` · **14 days** · grid (23, 14) · owner: party:4

An underground movement becomes a government only after a resolved revolutionary or political transition. This is a difficult alternate history.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace rpr:mandate:
- Stability: -8%
- Trade opinion factor: -8%
- Civilian industry productivity: +4%
- condition: actual revolutionary government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: actual revolutionary government

### A Southern Front

`COLDWAR_KOR_southern_front` · **35 days** · grid (22, 15) · owner: party:4

Broaden the revolutionary coalition while protecting a separate Southern government.

Prerequisites: (revolutionary_cabinet).
Exclusive with: vanguard_party.

- Replace rpr:front:
- Stability: +6%
- Political power gain: -8%
- Foreign influence defence: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Vanguard Party

`COLDWAR_KOR_vanguard_party` · **35 days** · grid (24, 15) · owner: party:4

Centralize the revolution under a disciplined party-state.

Prerequisites: (revolutionary_cabinet).
Exclusive with: southern_front.

- Replace rpr:front:
- Political power gain: +18%
- Stability: -7%
- Weekly police expenses: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Pluralist Socialism

`COLDWAR_KOR_pluralist_socialism` · **35 days** · grid (22, 16) · owner: party:4

Accept independent socialist and civic representation rather than a monopoly party.

Prerequisites: (southern_front).
Exclusive with: none.

- Replace rpr:front:
- Stability: +9%
- Political power gain: -10%
- Foreign influence defence: +6%
- action: left_pluralism
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Cadres in Industry

`COLDWAR_KOR_party_cadres` · **35 days** · grid (24, 16) · owner: party:4

Embed cadres in workplaces while accepting coercion and managerial interference.

Prerequisites: (vanguard_party).
Exclusive with: none.

- Replace rpr:front:
- Political power gain: +20%
- Stability: -9%
- Weekly police expenses: +10%
- Civilian industry productivity: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Rebuild Industry

`COLDWAR_KOR_revolutionary_reconstruction` · **49 days** · grid (23, 17) · owner: party:4

Rebuild production under a public investment guarantee.

Prerequisites: (pluralist_socialism OR party_cadres).
Exclusive with: none.

- Treasury: -$3bn (once)
- Replace rpr:rebuild:
- Interest rate (percentage points before native clamps): +0.35 percentage points
- State 606: +1 industrial_complex (paid, once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Confederal Route

`COLDWAR_KOR_confederal_revolution` · **35 days** · grid (22, 18) · owner: party:4

Offer Pyongyang a sovereign confederation. The other Korea may reject every constitutional concession.

Prerequisites: (revolutionary_reconstruction).
Exclusive with: northern_alignment.

- Replace rpr:korea:
- Foreign influence defence: +8%
- Political power gain: -6%
- offer: sovereign_confederation
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Align with Pyongyang

`COLDWAR_KOR_northern_alignment` · **35 days** · grid (24, 18) · owner: party:4

Seek a Northern security compact at the cost of external access and policy autonomy.

Prerequisites: (revolutionary_reconstruction).
Exclusive with: confederal_revolution.

- Replace rpr:korea:
- Division organization: +6%
- Trade opinion factor: -10%
- Foreign influence defence: -8%
- Active only after accepted northern_security_compact
- offer: northern_security_compact
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Southern Guarantees

`COLDWAR_KOR_southern_guarantees` · **35 days** · grid (22, 19) · owner: party:4

Entrench separate Southern institutions inside an accepted inter-Korean framework.

Prerequisites: (confederal_revolution).
Exclusive with: none.

- Replace rpr:korea:
- Foreign influence defence: +10%
- Stability: +4%
- Political power gain: -8%
- condition: accepted sovereign_confederation
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: accepted sovereign_confederation

Bypass: {'condition': 'Final refusal or 60-day pending expiry of sovereign_confederation; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_sovereign_confederation_refused has_country_flag = COLDWAR_KOR_sovereign_confederation_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Joint Planning

`COLDWAR_KOR_joint_planning` · **35 days** · grid (24, 19) · owner: party:4

Coordinate selected industrial plans after bilateral agreement, without a free transfer of territory.

Prerequisites: (northern_alignment).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace rpr:korea:
- Trade opinion factor: -10%
- Foreign influence defence: -10%
- Civilian industry productivity: +8%
- condition: accepted northern_security_compact
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: accepted northern_security_compact

Bypass: {'condition': 'Final refusal or 60-day pending expiry of northern_security_compact; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_northern_security_compact_refused has_country_flag = COLDWAR_KOR_northern_security_compact_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### A Southern Settlement

`COLDWAR_KOR_southern_settlement` · **35 days** · grid (23, 20) · owner: party:4

Ratify the Southern settlement; any eventual unified state still requires both players’ approval.

Prerequisites: (southern_guarantees OR joint_planning).
Exclusive with: none.

- Replace rpr:settlement:
- Stability: +5%
- Weekly bureaucracy expenses: +5%
- action: southern_ratification
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Seek Recognition

`COLDWAR_KOR_revolutionary_diplomacy` · **35 days** · grid (23, 21) · owner: party:4

Seek external recognition of the new government. Recognition does not force a partner into an alliance.

Prerequisites: (southern_settlement).
Exclusive with: none.

- offer: revolutionary_recognition
- note: No guaranteed grants or treaty removal
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Workplace Elections

`COLDWAR_KOR_rpr_worker_elections` · **35 days** · grid (22, 22) · owner: party:4

Give workers an independent say in public enterprises, at a cost to central directive power.

Prerequisites: (revolutionary_diplomacy).
Exclusive with: rpr_production_cadres.

- Treasury: -$1bn (once)
- Replace rpr:workplace:
- Stability: +3%
- Political power gain: -5%
- Civilian industry productivity: +5%

### Production Cadres

`COLDWAR_KOR_rpr_production_cadres` · **35 days** · grid (24, 22) · owner: party:4

Concentrate production authority in party cadres, accepting legitimacy and credit costs.

Prerequisites: (revolutionary_diplomacy).
Exclusive with: rpr_worker_elections.

- Treasury: -$1bn (once)
- Replace rpr:workplace:
- Stability: -4%
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Civilian industry productivity: +8%

## KCIA · an exceptional security cabinet

Entry condition: check_variable = { ruling_party = 7 }.

### A Security Directorate

`COLDWAR_KOR_security_cabinet` · **14 days** · grid (34, 14) · owner: party:7

A security agency governing directly is an exceptional alternate outcome, not the normal Park starting government.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace security:mandate:
- Intelligence network gain: +8%
- Stability: -8%
- Weekly police expenses: +8%
- condition: actual KCIA-led government
- Requirement: Exceptional government transition resolved; actual ruling_party 7; KCIA power-bloc backing alone is insufficient
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: actual KCIA-led government

### An Internal Directorate

`COLDWAR_KOR_internal_directorate` · **35 days** · grid (33, 15) · owner: party:7

Concentrate domestic intelligence and political surveillance.

Prerequisites: (security_cabinet).
Exclusive with: external_service.

- Replace security:service:
- Intelligence network gain: +10%
- Political power gain: +8%
- Stability: -8%
- Weekly police expenses: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### External Intelligence

`COLDWAR_KOR_external_service` · **35 days** · grid (35, 15) · owner: party:7

Redirect resources toward counterintelligence and external threats.

Prerequisites: (security_cabinet).
Exclusive with: internal_directorate.

- Replace security:service:
- Intelligence network gain: +8%
- Encryption: +5%
- Weekly bureaucracy expenses: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### National Files

`COLDWAR_KOR_national_files` · **35 days** · grid (33, 16) · owner: party:7

Central records improve surveillance while extending arbitrary state power.

Prerequisites: (internal_directorate).
Exclusive with: none.

- Replace security:service:
- Intelligence network gain: +14%
- Political power gain: +10%
- Stability: -10%
- Weekly police expenses: +10%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Warranted Operations

`COLDWAR_KOR_warranted_operations` · **35 days** · grid (35, 16) · owner: party:7

Professional safeguards limit political operations and require oversight.

Prerequisites: (external_service).
Exclusive with: none.

- Replace security:service:
- Intelligence network gain: +10%
- Encryption: +8%
- Weekly bureaucracy expenses: +8%
- Political power gain: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Counter-Infiltration

`COLDWAR_KOR_counter_infiltration` · **35 days** · grid (34, 17) · owner: party:7

Coordinate border intelligence without creating a parallel combat force.

Prerequisites: (national_files OR warranted_operations).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace security:border:
- Division defence on core territory: +4%
- Weekly police expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Protected Technocrats

`COLDWAR_KOR_security_technocrats` · **35 days** · grid (33, 18) · owner: party:7

Protect a technocratic cabinet through the security apparatus.

Prerequisites: (counter_infiltration).
Exclusive with: civilian_exit.

- Replace security:governance:
- Construction speed: +7%
- Stability: -4%
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Civilian Exit

`COLDWAR_KOR_civilian_exit` · **35 days** · grid (35, 18) · owner: party:7

Negotiate safeguards for a return to civilian politics.

Prerequisites: (counter_infiltration).
Exclusive with: security_technocrats.

- Replace security:governance:
- Stability: +7%
- Political power gain: -10%
- action: civilian_transition_agreement
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Protected Planning

`COLDWAR_KOR_protected_planning` · **35 days** · grid (33, 19) · owner: party:7

Guarantee strategic planning at a political and financial cost.

Prerequisites: (security_technocrats).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace security:governance:
- Construction speed: +10%
- Stability: -6%
- Interest rate (percentage points before native clamps): +0.3 percentage points
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Open the Archives

`COLDWAR_KOR_disclose_archives` · **35 days** · grid (35, 19) · owner: party:7

Accept a controlled disclosure process and the loss of political intelligence assets.

Prerequisites: (civilian_exit).
Exclusive with: none.

- Replace security:governance:
- Stability: +10%
- Political power gain: -12%
- Intelligence network gain: -3%
- action: political_case_review
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Security Settlement

`COLDWAR_KOR_security_settlement` · **35 days** · grid (34, 20) · owner: party:7

Institutionalize security responsibilities under the chosen governing settlement.

Prerequisites: (protected_planning OR disclose_archives).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace security:settlement:
- Division defence on core territory: +4%
- Weekly bureaucracy expenses: +4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Handover Guarantees

`COLDWAR_KOR_security_handover` · **35 days** · grid (34, 21) · owner: party:7

Offer a concrete transition compact. A change of government ends this directorate’s active programme.

Prerequisites: (security_settlement).
Exclusive with: none.

- pp_once: +75 (once)
- stability: -0.03 (once)
- action: security_transition_terms
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Legal Warrants

`COLDWAR_KOR_security_due_process` · **35 days** · grid (33, 22) · owner: party:7

Subject operations to warrants and review. The institutional rules remain separate from this caretaker’s active programme.

Prerequisites: (security_handover).
Exclusive with: security_protected_archives.

- Replace security:legal_settlement:
- Stability: +4%
- Research speed: +2%
- Intelligence network gain: -4%
- Weekly bureaucracy expenses: +4%
- action: warranted_security_operations

### Protected Archives

`COLDWAR_KOR_security_protected_archives` · **35 days** · grid (35, 22) · owner: party:7

Retain extensive classified political files at the cost of public trust and police expenditure.

Prerequisites: (security_handover).
Exclusive with: security_due_process.

- Replace security:legal_settlement:
- Intelligence network gain: +10%
- Stability: -5%
- Weekly police expenses: +6%

## National development · industry and society

Entry condition: Independent KOR; 1970 scenario.

### Review the Plan

`COLDWAR_KOR_third_plan` · **21 days** · grid (45, 0) · owner: national

Review the next development plan against credit, workforce and energy constraints.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace economy:planning:
- Construction speed: +4%
- Weekly bureaucracy expenses: +3%

### Heavy Industry Drive

`COLDWAR_KOR_heavy_chemical_drive` · **35 days** · grid (44, 1) · owner: national

Commit to capital-intensive steel, machinery and chemicals, increasing credit concentration.

Prerequisites: (third_plan).
Exclusive with: light_export_model.

- Treasury: -$3bn (once)
- Replace economy:industrial_model:
- Interest rate (percentage points before native clamps): +0.4 percentage points
- Civilian industry productivity: +9%

### Diversify Light Exports

`COLDWAR_KOR_light_export_model` · **35 days** · grid (46, 1) · owner: national

Expand labor-intensive exports and smaller firms rather than concentrating on heavy plants.

Prerequisites: (third_plan).
Exclusive with: heavy_chemical_drive.

- Treasury: -$2bn (once)
- Replace economy:industrial_model:
- Civilian factory construction: +9%
- Building workforce requirement: +3%
- Civilian industry productivity: -2%

### Pohang Steelworks

`COLDWAR_KOR_pohang_foundry` · **49 days** · grid (44, 2) · owner: national

Bring paid industrial capacity into operation; no free raw resource or uranium grant.

Prerequisites: (heavy_chemical_drive).
Exclusive with: none.

- Treasury: -$3bn (once)
- Replace economy:industrial_model:
- Interest rate (percentage points before native clamps): +0.5 percentage points
- Civilian industry productivity: +12%
- State 605: +1 industrial_complex (paid, once)

### Provincial Exports

`COLDWAR_KOR_provincial_export_zones` · **49 days** · grid (46, 2) · owner: national

Create a paid provincial export base with a continuing demand for labor.

Prerequisites: (light_export_model).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:industrial_model:
- Civilian factory construction: +11%
- Building workforce requirement: +4%
- Civilian industry productivity: -2%
- State 606: +1 industrial_complex (paid, once)

### Freight Corridors

`COLDWAR_KOR_freight_corridors` · **49 days** · grid (45, 3) · owner: national

Improve the Seoul–southeast transport corridor and reduce the infrastructure gap.

Prerequisites: (pohang_foundry OR provincial_export_zones).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 604: +1 infrastructure (paid, once)
- State 605: +1 infrastructure (paid, once)
- start_replace: rural

### Assembly Licences

`COLDWAR_KOR_assembly_contracts` · **35 days** · grid (44, 4) · owner: national

Negotiate imported production knowledge. A signed licence provides access, not a free future technology.

Prerequisites: (freight_corridors).
Exclusive with: domestic_engineering.

- Replace economy:technology:
- Foreign influence defence: -5%
- Civilian industry productivity: +5%
- Active only after accepted technology_licence
- offer: technology_licence

### Domestic Engineering

`COLDWAR_KOR_domestic_engineering` · **35 days** · grid (46, 4) · owner: national

Fund local engineering capacity, accepting higher costs and a slower initial industrial payoff.

Prerequisites: (freight_corridors).
Exclusive with: assembly_contracts.

- Treasury: -$2bn (once)
- Replace economy:technology:
- Research speed: +4%
- Weekly education expenses: +8%

### Technical Colleges

`COLDWAR_KOR_technical_colleges` · **35 days** · grid (44, 5) · owner: national

Train technicians to absorb licensed production methods.

Prerequisites: (assembly_contracts).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace economy:technology:
- Research speed: +2%
- Weekly education expenses: +6%
- Foreign influence defence: -5%
- Civilian industry productivity: +7%

### Industrial Laboratories

`COLDWAR_KOR_industrial_laboratories` · **35 days** · grid (46, 5) · owner: national

Develop local laboratories without bypassing research-year or special-project restrictions.

Prerequisites: (domestic_engineering).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:technology:
- Research speed: +6%
- Weekly education expenses: +10%

### Industrial Skills

`COLDWAR_KOR_industrial_skills` · **35 days** · grid (45, 6) · owner: national

Raise workforce efficiency through vocational training; this does not force an Imperia development tier.

Prerequisites: (technical_colleges OR industrial_laboratories).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace economy:skills:
- Building workforce requirement: -3%
- Weekly education expenses: +4%

### Wage Discipline

`COLDWAR_KOR_labor_discipline` · **35 days** · grid (44, 7) · owner: national

Preserve export margins through constrained bargaining, leaving a continuing legitimacy cost.

Prerequisites: (industrial_skills).
Exclusive with: labor_compact.

- Replace economy:labour:
- Stability: -6%
- Civilian industry productivity: +7%
- start_replace: labour

### A Labour Compact

`COLDWAR_KOR_labor_compact` · **35 days** · grid (46, 7) · owner: national

Accept wage bargaining and labor protection in exchange for cooperation and social trust.

Prerequisites: (industrial_skills).
Exclusive with: labor_discipline.

- Replace economy:labour:
- Stability: +6%
- Civilian industry productivity: +1%
- start_replace: labour

### State Arbitration

`COLDWAR_KOR_controlled_arbitration` · **35 days** · grid (44, 8) · owner: national

Resolve disputes through state arbitration and security pressure.

Prerequisites: (labor_discipline).
Exclusive with: none.

- Replace economy:labour:
- Stability: -7%
- Weekly police expenses: +4%
- Civilian industry productivity: +9%

### Safety Inspection

`COLDWAR_KOR_safety_inspectorate` · **35 days** · grid (46, 8) · owner: national

Enforce workplace safety through an independent public service.

Prerequisites: (labor_compact).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace economy:labour:
- Stability: +8%
- Weekly bureaucracy expenses: +5%
- Civilian industry productivity: +2%

### Urban Services

`COLDWAR_KOR_urban_services` · **35 days** · grid (45, 9) · owner: national

Reduce the social burden of migration through paid urban services.

Prerequisites: (controlled_arbitration OR safety_inspectorate).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:urban:
- Stability: +3%
- Consumer goods factor: +1%
- start_replace: rural

### Export Guarantees

`COLDWAR_KOR_export_credit_guarantees` · **35 days** · grid (44, 10) · owner: national

Use state guarantees to sustain export investment through external shocks.

Prerequisites: (urban_services).
Exclusive with: banking_discipline.

- Active programme: $0.00200bn/week (replacement slot)
- Replace economy:finance:
- Interest rate (percentage points before native clamps): +0.4 percentage points
- Civilian industry productivity: +6%
- start_replace: finance

### Discipline the Banks

`COLDWAR_KOR_banking_discipline` · **35 days** · grid (46, 10) · owner: national

Restrain connected lending and hidden guarantees, accepting slower near-term industrial expansion.

Prerequisites: (urban_services).
Exclusive with: export_credit_guarantees.

- Replace economy:finance:
- Interest rate (percentage points before native clamps): -0.5 percentage points
- Civilian industry productivity: -3%
- start_replace: finance

### Strategic Refinancing

`COLDWAR_KOR_strategic_refinancing` · **35 days** · grid (44, 11) · owner: national

Keep strategic firms operating at the cost of larger public exposure.

Prerequisites: (export_credit_guarantees).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace economy:finance:
- Interest rate (percentage points before native clamps): +0.5 percentage points
- Civilian industry productivity: +8%

### Orderly Restructuring

`COLDWAR_KOR_orderly_restructuring` · **35 days** · grid (46, 11) · owner: national

Restructure overextended firms without a direct debt reset.

Prerequisites: (banking_discipline).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:finance:
- Interest rate (percentage points before native clamps): -0.6 percentage points
- Civilian industry productivity: +2%

### Energy Diversification

`COLDWAR_KOR_energy_planning` · **35 days** · grid (45, 12) · owner: national

Open existing energy-project decisions and reduce reliance on a single imported fuel route.

Prerequisites: (strategic_refinancing OR orderly_restructuring).
Exclusive with: none.

- Treasury: -$1bn (once)
- action: energy_project_options
- start_replace: energy

### Civil Nuclear Power

`COLDWAR_KOR_civil_nuclear` · **35 days** · grid (44, 13) · owner: national

Fund access to the existing civilian nuclear programme. Reactors, fuel and running costs follow current Imperia rules.

Prerequisites: (energy_planning).
Exclusive with: thermal_diversification.

- Treasury: -$2bn (once)
- action: existing_civil_nuclear_projects
- condition: native safeguards, technology and projects
- Requirement: Actual eligible Imperia development tier, reactor technology and native reactor-building permission; native paid projects and safeguards remain mandatory

### Diverse Fuel Supplies

`COLDWAR_KOR_thermal_diversification` · **35 days** · grid (46, 13) · owner: national

Diversify imported fuel and thermal generation; supply contracts still require a willing partner.

Prerequisites: (energy_planning).
Exclusive with: civil_nuclear.

- Treasury: -$2bn (once)
- Replace economy:energy:
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Civilian industry productivity: +4%
- action: existing_energy_purchase_options

### Advanced Exports

`COLDWAR_KOR_advanced_export_economy` · **35 days** · grid (45, 14) · owner: national

Consolidate industrial skills and quality control through the existing development system.

Prerequisites: (civil_nuclear OR thermal_diversification).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:maturity:
- Building workforce requirement: -3%
- Weekly education expenses: +4%
- Civilian industry productivity: +4%

### Sector Investment

`COLDWAR_KOR_sector_investment_review` · **35 days** · grid (45, 15) · owner: national

Choose the next priority investment package. Other industries may still be built and researched normally.

Prerequisites: (advanced_export_economy).
Exclusive with: none.

- Treasury: -$1bn (once)
- action: sector_investment_priority

### Electronics Priority

`COLDWAR_KOR_electronics_priority` · **35 days** · grid (43, 16) · owner: national

Prioritize electronics and technical skills, accepting a demanding education budget and skilled-labor needs.

Prerequisites: (sector_investment_review).
Exclusive with: machinery_priority, shipbuilding_priority.

- Treasury: -$3bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace economy:sector:
- Research speed: +3%
- Weekly education expenses: +7%
- Building workforce requirement: +3%
- Civilian industry productivity: +5%

### Electronics Capability

`COLDWAR_KOR_electronics_capability` · **35 days** · grid (43, 17) · owner: national

Build absorptive capability for advanced components without granting a future technology or a free semiconductor plant.

Prerequisites: (electronics_priority).
Exclusive with: none.

- Treasury: -$2bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace economy:sector:
- Research speed: +4%
- Weekly education expenses: +10%
- Building workforce requirement: +3%
- Civilian industry productivity: +8%

### Machinery Priority

`COLDWAR_KOR_machinery_priority` · **35 days** · grid (45, 16) · owner: national

Prioritize machine tools and automotive suppliers at a capital and workforce cost.

Prerequisites: (sector_investment_review).
Exclusive with: electronics_priority, shipbuilding_priority.

- Treasury: -$3bn (once)
- Replace economy:sector:
- Construction speed: +3%
- Interest rate (percentage points before native clamps): +0.25 percentage points
- Building workforce requirement: +3%
- Civilian industry productivity: +7%

### Supplier Engineering

`COLDWAR_KOR_supplier_engineering` · **49 days** · grid (45, 17) · owner: national

Fund a supplier-engineering complex and its continuing credit exposure.

Prerequisites: (machinery_priority).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace economy:sector:
- Construction speed: +4%
- Interest rate (percentage points before native clamps): +0.35 percentage points
- Building workforce requirement: +4%
- Civilian industry productivity: +10%
- State 606: +1 industrial_complex (paid, once)

### Shipbuilding Priority

`COLDWAR_KOR_shipbuilding_priority` · **35 days** · grid (47, 16) · owner: national

Prioritize commercial shipbuilding, accepting capital and labor demands.

Prerequisites: (sector_investment_review).
Exclusive with: electronics_priority, machinery_priority.

- Treasury: -$3bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace economy:sector:
- Building workforce requirement: +4%
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Civilian industry productivity: +3%
- Commercial dockyard productivity: +12%

### Commercial Shipyards

`COLDWAR_KOR_commercial_shipyards` · **49 days** · grid (47, 17) · owner: national

Fund commercial shipyard capacity. Commercial GDP productivity and naval production output remain different systems.

Prerequisites: (shipbuilding_priority).
Exclusive with: none.

- Treasury: -$2bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace economy:sector:
- Building workforce requirement: +4%
- Interest rate (percentage points before native clamps): +0.3 percentage points
- Civilian industry productivity: +5%
- Commercial dockyard productivity: +18%
- State 605: +1 dockyard (paid, once)

### Industrial Standards

`COLDWAR_KOR_industrial_quality_service` · **35 days** · grid (45, 18) · owner: national

Fund quality standards and vocational services across the chosen sector.

Prerequisites: (electronics_capability OR supplier_engineering OR commercial_shipyards).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace economy:standards:
- Building workforce requirement: -2%
- Weekly education expenses: +4%
- Weekly bureaucracy expenses: +3%

### Urban Social Insurance

`COLDWAR_KOR_urban_insurance_network` · **35 days** · grid (44, 19) · owner: national

Extend coverage to urban households outside large-company employment. Contributions and administrative costs remain real.

Prerequisites: (industrial_quality_service).
Exclusive with: rural_insurance_network.

- Treasury: -$2bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace economy:social_network:
- Stability: +4%
- Weekly health expenses: +8%
- Weekly social expenses: +6%
- Building workforce requirement: -2%
- action: extend_social_insurance
- Replace starting problem: social_insurance

### Rural Social Insurance

`COLDWAR_KOR_rural_insurance_network` · **35 days** · grid (46, 19) · owner: national

Prioritize farming and fishing households, accepting a slower urban extension.

Prerequisites: (industrial_quality_service).
Exclusive with: urban_insurance_network.

- Treasury: -$2bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace economy:social_network:
- Agricultural productivity: +7%
- Stability: +3%
- Weekly health expenses: +6%
- Weekly bureaucracy expenses: +4%
- action: extend_social_insurance
- Replace starting problem: social_insurance

## Defence · deterrence and autonomy

Entry condition: Independent KOR; 1970 scenario.

### Defence Review

`COLDWAR_KOR_defence_review` · **21 days** · grid (54, 0) · owner: national

Review readiness after the 1968 raids and the Nixon Doctrine. No starting units or stockpiles are created.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:readiness:
- Division defence on core territory: +4%
- Weekly personnel expenses: +4%
- xp: +25 (once)

### A Fortified DMZ

`COLDWAR_KOR_dmz_deterrence` · **35 days** · grid (53, 1) · owner: national

Prioritize prepared positions and defensive depth over offensive maneuver.

Prerequisites: (defence_review).
Exclusive with: mobile_deterrence.

- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:posture:
- Division defence on core territory: +8%
- Division attack: -3%

### A Mobile Deterrent

`COLDWAR_KOR_mobile_deterrence` · **35 days** · grid (55, 1) · owner: national

Keep a mobile reserve and limited offensive options at greater logistical cost.

Prerequisites: (defence_review).
Exclusive with: dmz_deterrence.

- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:posture:
- Division attack: +5%
- Division organization: +4%
- Supply consumption: +5%

### Infiltration Response

`COLDWAR_KOR_counter_infiltration_units` · **35 days** · grid (53, 2) · owner: national

Train the existing force to respond to infiltration and local attacks.

Prerequisites: (dmz_deterrence).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace defence:posture:
- Division defence on core territory: +10%
- Division organization: +3%
- Division attack: -3%
- xp: +15 (once)

### Combined Arms

`COLDWAR_KOR_combined_arms_training` · **35 days** · grid (55, 2) · owner: national

Develop coordinated maneuver without granting out-of-period equipment.

Prerequisites: (mobile_deterrence).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace defence:posture:
- Division attack: +7%
- Division organization: +5%
- Supply consumption: +7%
- xp: +15 (once)

### Military Logistics

`COLDWAR_KOR_defence_logistics` · **49 days** · grid (54, 3) · owner: national

Fund transport capacity and logistical staff.

Prerequisites: (counter_infiltration_units OR combined_arms_training).
Exclusive with: none.

- Treasury: -$2bn (once)
- Replace defence:logistics:
- Supply consumption: -3%
- Weekly personnel expenses: +3%
- State 606: +1 infrastructure (paid, once)

### Allied Procurement

`COLDWAR_KOR_allied_procurement` · **35 days** · grid (53, 4) · owner: national

Negotiate access to affordable allied systems while accepting dependence on suppliers.

Prerequisites: (defence_logistics).
Exclusive with: domestic_defence_industry.

- Replace defence:procurement:
- Weekly military equipment expenses: -6%
- Foreign influence defence: -6%
- Active only after accepted allied_procurement_contract
- offer: allied_procurement_contract

### Domestic Armaments

`COLDWAR_KOR_domestic_defence_industry` · **35 days** · grid (55, 4) · owner: national

Fund domestic armament production at the cost of capital and civilian opportunity.

Prerequisites: (defence_logistics).
Exclusive with: allied_procurement.

- Treasury: -$3bn (once)
- Replace defence:procurement:
- Military factory construction: +10%
- Military factory output: +3%
- Interest rate (percentage points before native clamps): +0.3 percentage points

### Licensed Maintenance

`COLDWAR_KOR_licensed_maintenance` · **35 days** · grid (53, 5) · owner: national

Build maintenance capability after a procurement agreement; no automatic foreign stockpile.

Prerequisites: (allied_procurement).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:procurement:
- Weekly military equipment expenses: -8%
- Military production efficiency cap: +3%
- Foreign influence defence: -7%
- condition: accepted allied_procurement_contract
- Requirement: accepted allied_procurement_contract

Bypass: {'condition': 'Final refusal or 60-day pending expiry of allied_procurement_contract; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_allied_procurement_contract_refused has_country_flag = COLDWAR_KOR_allied_procurement_contract_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Changwon Production

`COLDWAR_KOR_changwon_production` · **49 days** · grid (55, 5) · owner: national

Create a paid military-industrial production base using existing equipment technologies.

Prerequisites: (domestic_defence_industry).
Exclusive with: none.

- Treasury: -$3bn (once)
- Replace defence:procurement:
- Military factory construction: +12%
- Military factory output: +4%
- Interest rate (percentage points before native clamps): +0.4 percentage points
- State 605: +1 arms_factory (paid, once)

### Quality Standards

`COLDWAR_KOR_defence_quality` · **35 days** · grid (54, 6) · owner: national

Improve standards and inspections across the selected procurement model.

Prerequisites: (licensed_maintenance OR changwon_production).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:quality:
- Military production efficiency cap: +4%
- Weekly bureaucracy expenses: +3%

### The Reserve Army

`COLDWAR_KOR_reserve_army` · **35 days** · grid (53, 7) · owner: national

Maintain a broad trained reserve, diverting labor and training time from civilian life.

Prerequisites: (defence_quality).
Exclusive with: professional_core.

- Active programme: $0.00100bn/week (replacement slot)
- Replace defence:service:
- Recruitable population factor: +8%
- Army training time: -6%
- Building workforce requirement: +4%

### A Professional Core

`COLDWAR_KOR_professional_core` · **35 days** · grid (55, 7) · owner: national

Invest in a smaller professional core with higher personnel costs.

Prerequisites: (defence_quality).
Exclusive with: reserve_army.

- Active programme: $0.00100bn/week (replacement slot)
- Replace defence:service:
- Division organization: +6%
- Division recovery rate: +5%
- Weekly personnel expenses: +10%

### Civil Defence Training

`COLDWAR_KOR_civil_defence_training` · **35 days** · grid (53, 8) · owner: national

Expand readiness obligations without generating free military formations.

Prerequisites: (reserve_army).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:service:
- Recruitable population factor: +10%
- Army training time: -8%
- Building workforce requirement: +5%

### A Career NCO Corps

`COLDWAR_KOR_career_ncos` · **35 days** · grid (55, 8) · owner: national

Build experienced small-unit leadership through a funded career structure.

Prerequisites: (professional_core).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:service:
- Division organization: +8%
- Division recovery rate: +7%
- Weekly personnel expenses: +12%
- xp: +15 (once)

### The Joint Staff

`COLDWAR_KOR_joint_staff` · **35 days** · grid (54, 9) · owner: national

Coordinate service planning without giving the military a domestic political mandate.

Prerequisites: (civil_defence_training OR career_ncos).
Exclusive with: none.

- Replace defence:staff:
- Division organization: +3%
- Weekly bureaucracy expenses: +4%
- xp: +10 (once)

### Coastal Denial

`COLDWAR_KOR_coastal_defence` · **49 days** · grid (53, 10) · owner: national

Prioritize coastal warning and maritime readiness over air-force investment.

Prerequisites: (joint_staff).
Exclusive with: air_defence.

- Treasury: -$2bn (once)
- Replace defence:maritime:
- Naval organization: +8%
- Air mission efficiency: -3%
- State 608: +1 radar_station (paid, once)

### Air Defence Priority

`COLDWAR_KOR_air_defence` · **49 days** · grid (55, 10) · owner: national

Prioritize air-defense coverage while accepting slower maritime modernization.

Prerequisites: (joint_staff).
Exclusive with: coastal_defence.

- Treasury: -$2bn (once)
- Replace defence:maritime:
- Air mission efficiency: +6%
- Naval organization: -3%
- State 604: +1 anti_air_building (paid, once)

### Coastal Logistics

`COLDWAR_KOR_coastal_logistics` · **49 days** · grid (53, 11) · owner: national

Fund a coastal yard for fleet support; no modern warship or task force is spawned.

Prerequisites: (coastal_defence).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 605: +1 dockyard (paid, once)

### Joint Air Command

`COLDWAR_KOR_air_command` · **35 days** · grid (55, 11) · owner: national

Improve air coordination through a funded command structure.

Prerequisites: (air_defence).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:air:
- Air mission efficiency: +3%
- Weekly military equipment expenses: +4%

### Yulgok Readiness

`COLDWAR_KOR_yulgok_readiness_review` · **35 days** · grid (54, 12) · owner: national

Review the modernization programme and the existing force. No starting divisions or equipment are created.

Prerequisites: (coastal_logistics OR air_command).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:readiness_audit:
- Division organization: +2%
- Weekly personnel expenses: +3%
- xp: +15 (once)

### Air Cover Priority

`COLDWAR_KOR_air_cover_priority` · **35 days** · grid (52, 13) · owner: national

Prioritize coordinated air cover over spending on other service missions.

Prerequisites: (yulgok_readiness_review).
Exclusive with: escort_priority, counterbattery_priority.

- Treasury: -$2bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace defence:mission_priority:
- Air mission efficiency: +6%
- Weekly military equipment expenses: +6%

### Aircrew Training

`COLDWAR_KOR_aircrew_training` · **35 days** · grid (52, 14) · owner: national

Fund training and staff work for the chosen mission; technologies and equipment still follow the existing systems.

Prerequisites: (air_cover_priority).
Exclusive with: none.

- Treasury: -$1bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:mission_priority:
- Air mission efficiency: +9%
- Weekly military equipment expenses: +8%
- Weekly personnel expenses: +4%

### Escort Priority

`COLDWAR_KOR_escort_priority` · **35 days** · grid (54, 13) · owner: national

Prioritize escorts and maritime coordination with a continuing operating burden.

Prerequisites: (yulgok_readiness_review).
Exclusive with: air_cover_priority, counterbattery_priority.

- Treasury: -$2bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace defence:mission_priority:
- Naval organization: +8%
- Supply consumption: +4%
- Weekly military equipment expenses: +4%

### An Escort Staff

`COLDWAR_KOR_escort_staff` · **35 days** · grid (54, 14) · owner: national

Fund training and staff work for the chosen mission; technologies and equipment still follow the existing systems.

Prerequisites: (escort_priority).
Exclusive with: none.

- Treasury: -$1bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:mission_priority:
- Naval organization: +12%
- Supply consumption: +5%
- Weekly military equipment expenses: +6%

### Counter-Battery Fire

`COLDWAR_KOR_counterbattery_priority` · **35 days** · grid (56, 13) · owner: national

Prioritize land-fire coordination and survivability rather than a free artillery stockpile.

Prerequisites: (yulgok_readiness_review).
Exclusive with: air_cover_priority, escort_priority.

- Treasury: -$2bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace defence:mission_priority:
- Division defence: +5%
- Division attack: +3%
- Supply consumption: +5%

### Fire Direction

`COLDWAR_KOR_fire_direction` · **35 days** · grid (56, 14) · owner: national

Fund training and staff work for the chosen mission; technologies and equipment still follow the existing systems.

Prerequisites: (counterbattery_priority).
Exclusive with: none.

- Treasury: -$1bn (once)
- Active programme: $0.00200bn/week (replacement slot)
- Replace defence:mission_priority:
- Division defence: +7%
- Division attack: +4%
- Supply consumption: +7%

### Joint Readiness Audits

`COLDWAR_KOR_joint_readiness_audits` · **35 days** · grid (54, 15) · owner: national

Audit readiness and logistics across all services, using the actual force rather than spawning formations.

Prerequisites: (aircrew_training OR escort_staff OR fire_direction).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace defence:joint_audit:
- Supply consumption: -3%
- Weekly bureaucracy expenses: +4%
- xp: +15 (once)

## Foreign policy · alliances and markets

Entry condition: Independent KOR; 1970 scenario.

### A Diplomatic Review

`COLDWAR_KOR_diplomatic_review` · **21 days** · grid (63, 0) · owner: national

Review the alliance, Japanese cooperation and new market access from a divided peninsula.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:service:
- Trade opinion factor: +5%
- Weekly bureaucracy expenses: +3%

### The Alliance Bargain

`COLDWAR_KOR_alliance_bargain` · **35 days** · grid (62, 1) · owner: national

Seek American assurances after the troop drawdown. A focus cannot command US deployments.

Prerequisites: (diplomatic_review).
Exclusive with: strategic_autonomy.

- Replace foreign:alignment:
- Division defence on core territory: +5%
- Foreign influence defence: -5%
- offer: us_alliance_assurance

### Strategic Autonomy

`COLDWAR_KOR_strategic_autonomy` · **35 days** · grid (64, 1) · owner: national

Broaden diplomatic room while accepting narrower privileged access.

Prerequisites: (diplomatic_review).
Exclusive with: alliance_bargain.

- Treasury: -$1bn (once)
- Replace foreign:alignment:
- Foreign influence defence: +10%
- Trade opinion factor: -4%
- Replace starting problem: alliance

### Burden Sharing

`COLDWAR_KOR_burden_sharing` · **35 days** · grid (62, 2) · owner: national

Fund agreed local readiness in return for a credible alliance settlement.

Prerequisites: (alliance_bargain).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace foreign:alignment:
- Division organization: +4%
- Division defence on core territory: +5%
- Foreign influence defence: -7%
- condition: accepted us_alliance_assurance
- Requirement: accepted us_alliance_assurance

Bypass: {'condition': 'Final refusal or 60-day pending expiry of us_alliance_assurance; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_us_alliance_assurance_refused has_country_flag = COLDWAR_KOR_us_alliance_assurance_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Security Partners

`COLDWAR_KOR_diverse_partners` · **35 days** · grid (64, 2) · owner: national

Seek multiple limited partners without automatically changing treaties or factions.

Prerequisites: (strategic_autonomy).
Exclusive with: none.

- Replace foreign:alignment:
- Foreign influence defence: +12%
- Trade opinion factor: +2%
- Weekly bureaucracy expenses: +5%
- offer: security_partner_contacts

### The Vietnam Legacy

`COLDWAR_KOR_vietnam_legacy` · **35 days** · grid (63, 3) · owner: national

Negotiate an end to the existing commitment and veterans’ obligations. No units, experience or cash from an absent expedition.

Prerequisites: (burden_sharing OR diverse_partners).
Exclusive with: none.

- offer: vietnam_withdrawal_settlement
- condition: active Vietnam commitment
- note: bypass with no rewards if no commitment
- Requirement: active Vietnam commitment

Bypass: No active commitment: bypass, no settlement bonus; continue the foreign tree.

### Pragmatism with Japan

`COLDWAR_KOR_japan_pragmatism` · **35 days** · grid (62, 4) · owner: national

Seek capital and production cooperation while accepting domestic controversy over colonial claims.

Prerequisites: (vietnam_legacy).
Exclusive with: claims_first.

- Replace foreign:japan:
- Trade opinion factor: +8%
- Stability: -4%
- offer: japan_technology_finance

### Historical Claims

`COLDWAR_KOR_claims_first` · **35 days** · grid (64, 4) · owner: national

Prioritize public legitimacy and historical claims while accepting more difficult economic cooperation.

Prerequisites: (vietnam_legacy).
Exclusive with: japan_pragmatism.

- Replace foreign:japan:
- Stability: +6%
- Foreign influence defence: +5%
- Trade opinion factor: -6%
- offer: historical_claims_dialogue

### Technical Exchanges

`COLDWAR_KOR_joint_technical_training` · **35 days** · grid (62, 5) · owner: national

Fund training agreed with Japanese partners; no automatic transfer of research.

Prerequisites: (japan_pragmatism).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:japan:
- Trade opinion factor: +10%
- Stability: -5%
- Civilian industry productivity: +3%
- condition: accepted japan_technology_finance
- Requirement: accepted japan_technology_finance

Bypass: {'condition': 'Final refusal or 60-day pending expiry of japan_technology_finance; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_japan_technology_finance_refused has_country_flag = COLDWAR_KOR_japan_technology_finance_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Alternative Capital

`COLDWAR_KOR_alternative_capital` · **35 days** · grid (64, 5) · owner: national

Seek less concentrated capital sources with higher financing and diplomatic costs.

Prerequisites: (claims_first).
Exclusive with: none.

- Replace foreign:japan:
- Stability: +6%
- Foreign influence defence: +6%
- Interest rate (percentage points before native clamps): +0.2 percentage points
- Trade opinion factor: -3%
- offer: alternative_finance_contacts

### Overseas Workers

`COLDWAR_KOR_overseas_workers` · **35 days** · grid (63, 6) · owner: national

Extend the existing miners’ and nurses’ programme through negotiated contracts; remittances use the shared system.

Prerequisites: (joint_technical_training OR alternative_capital).
Exclusive with: none.

- Treasury: -$1bn (once)
- action: existing_guest_worker_contracts
- condition: existing overseas-employment system
- Requirement: existing overseas-employment system

### Northern Diplomacy

`COLDWAR_KOR_nordpolitik` · **35 days** · grid (62, 7) · owner: national

Seek reciprocal diplomatic openings with socialist states. Soviet recognition in 1990 is the historical precedent; earlier recognition or Chinese normalization before 1991 is alternate history.

Prerequisites: (overseas_workers).
Exclusive with: pacific_exports.

- Replace foreign:markets:
- Trade opinion factor: +8%
- Political power gain: -5%
- offer: nordpolitik_recognition
- Requirement: At peace with the proposed partner; the partner must agree to a diplomatic opening before recognition is ratified

### Pacific Exports

`COLDWAR_KOR_pacific_exports` · **35 days** · grid (64, 7) · owner: national

Deepen market access among existing Pacific partners at the cost of external dependence.

Prerequisites: (overseas_workers).
Exclusive with: nordpolitik.

- Replace foreign:markets:
- Trade opinion factor: +6%
- Foreign influence defence: -4%
- Civilian industry productivity: +4%
- offer: pacific_trade_contacts

### A Middle Power

`COLDWAR_KOR_middle_power` · **35 days** · grid (63, 8) · owner: national

Build a larger diplomatic service to sustain the selected overseas orientation.

Prerequisites: (nordpolitik OR pacific_exports).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:standing:
- Trade opinion factor: +5%
- Weekly bureaucracy expenses: +4%

### Commercial Missions

`COLDWAR_KOR_overseas_commercial_service` · **35 days** · grid (63, 9) · owner: national

Create a professional service for overseas contracts and export standards.

Prerequisites: (middle_power).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:commercial_service:
- Trade opinion factor: +4%
- Weekly bureaucracy expenses: +4%

### Middle Eastern Bids

`COLDWAR_KOR_middle_east_bids` · **35 days** · grid (62, 10) · owner: national

Bid for construction work through actual partner contracts. No remittance or foreign payment is granted on dispatch.

Prerequisites: (overseas_commercial_service).
Exclusive with: pacific_standards.

- Treasury: -$1bn (once)
- Replace foreign:commercial_orientation:
- Trade opinion factor: +5%
- Weekly bureaucracy expenses: +4%
- action: native_construction_contract_bids

### Pacific Standards

`COLDWAR_KOR_pacific_standards` · **35 days** · grid (64, 10) · owner: national

Prioritize technology-intensive Pacific markets while accepting dependence on external standards.

Prerequisites: (overseas_commercial_service).
Exclusive with: middle_east_bids.

- Treasury: -$1bn (once)
- Replace foreign:commercial_orientation:
- Research speed: +2%
- Foreign influence defence: -3%
- offer: pacific_trade_contacts

### Contract Labour Rights

`COLDWAR_KOR_contract_worker_protection` · **35 days** · grid (62, 11) · owner: national

Negotiate worker protection using the existing overseas-employment and remittance system.

Prerequisites: (middle_east_bids).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:commercial_orientation:
- Trade opinion factor: +7%
- Stability: +2%
- Weekly bureaucracy expenses: +6%
- action: existing_guest_worker_contracts

### Export Quality Rules

`COLDWAR_KOR_international_quality` · **35 days** · grid (64, 11) · owner: national

Improve the domestic ability to meet contracted quality standards without a free technology transfer.

Prerequisites: (pacific_standards).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:commercial_orientation:
- Research speed: +2%
- Weekly education expenses: +4%
- Foreign influence defence: -3%
- Civilian industry productivity: +3%

### Professional Missions

`COLDWAR_KOR_professional_trade_missions` · **35 days** · grid (63, 12) · owner: national

Maintain specialist missions rather than rely solely on personal diplomacy.

Prerequisites: (contract_worker_protection OR international_quality).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace foreign:missions:
- Trade opinion factor: +5%
- Weekly bureaucracy expenses: +5%

### Public Treaty Rules

`COLDWAR_KOR_public_treaty_process` · **35 days** · grid (63, 13) · owner: national

Publish treaty obligations and require the lawful approval procedure before major commitments.

Prerequisites: (professional_trade_missions).
Exclusive with: none.

- Replace foreign:treaty_rules:
- Foreign influence defence: +5%
- Trade opinion factor: +3%
- Political power gain: -4%
- Weekly bureaucracy expenses: +3%
- action: publish_treaty_obligations

## North Korea · rivalry, dialogue and settlement

Entry condition: Independent KOR; 1970 scenario.

### The Korean Question

`COLDWAR_KOR_korean_question` · **14 days** · grid (72, 0) · owner: national

A divided peninsula requires a policy toward Pyongyang. Diplomatic offers preserve both players’ control.

Prerequisites: Independent programme entry.
Exclusive with: none.

- pp_once: +50 (once)
- action: inter_korean_channels

### A Red Cross Channel

`COLDWAR_KOR_red_cross_channel` · **35 days** · grid (71, 1) · owner: national

Propose humanitarian liaison on separated families. The 1971–72 talks are the historical precedent; an earlier opening depends on Pyongyang’s agreement.

Prerequisites: (korean_question).
Exclusive with: armed_vigilance.

- offer: red_cross_channel

### Armed Vigilance

`COLDWAR_KOR_armed_vigilance` · **35 days** · grid (73, 1) · owner: national

Keep channels limited and fund a higher state of defensive readiness.

Prerequisites: (korean_question).
Exclusive with: red_cross_channel.

- Active programme: $0.00200bn/week (replacement slot)
- Replace korea:opening:
- Division defence on core territory: +6%
- Trade opinion factor: -3%

### Family Reunions

`COLDWAR_KOR_family_reunions` · **35 days** · grid (71, 2) · owner: national

Offer a funded programme of limited family visits, subject to agreement on both sides.

Prerequisites: (red_cross_channel).
Exclusive with: none.

- offer: family_reunions
- condition: accepted red_cross_channel
- Requirement: accepted red_cross_channel

Bypass: {'condition': 'Final refusal or 60-day pending expiry of red_cross_channel; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_red_cross_channel_refused has_country_flag = COLDWAR_KOR_red_cross_channel_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### An Incident Hotline

`COLDWAR_KOR_incident_hotline` · **35 days** · grid (73, 2) · owner: national

Offer an incident channel while maintaining a deterrent posture.

Prerequisites: (armed_vigilance).
Exclusive with: none.

- Active programme: $0.00200bn/week (replacement slot)
- Replace korea:opening:
- Division defence on core territory: +7%
- Trade opinion factor: -3%
- offer: military_hotline

### Peninsula Policy

`COLDWAR_KOR_review_korean_policy` · **35 days** · grid (72, 3) · owner: national

Coordinate diplomacy, defense and civilian oversight regardless of the first approach.

Prerequisites: (family_reunions OR incident_hotline).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace korea:coordination:
- Foreign influence defence: +4%
- Weekly bureaucracy expenses: +3%

### A Coexistence Proposal

`COLDWAR_KOR_peaceful_coexistence` · **35 days** · grid (71, 4) · owner: national

Offer nonaggression and reciprocal restraint. Neither side is forced to disarm or abandon allies.

Prerequisites: (review_korean_policy).
Exclusive with: competitive_legitimacy.

- offer: nonaggression_compact

### Korean Legitimacy

`COLDWAR_KOR_competitive_legitimacy` · **35 days** · grid (73, 4) · owner: national

Compete diplomatically while keeping military and humanitarian contacts available.

Prerequisites: (review_korean_policy).
Exclusive with: peaceful_coexistence.

- Treasury: -$1bn (once)
- Replace korea:strategy:
- Foreign influence defence: +6%
- Political power gain: +4%
- Trade opinion factor: -4%

### Verified Restraint

`COLDWAR_KOR_verified_restraint` · **35 days** · grid (71, 5) · owner: national

Negotiate reciprocal notification and verification with explicit funding and withdrawal terms.

Prerequisites: (peaceful_coexistence).
Exclusive with: none.

- offer: verified_restraint
- condition: accepted nonaggression_compact
- Requirement: accepted nonaggression_compact

Bypass: {'condition': 'Final refusal or 60-day pending expiry of nonaggression_compact; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_nonaggression_compact_refused has_country_flag = COLDWAR_KOR_nonaggression_compact_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Protect Defectors

`COLDWAR_KOR_defector_protection` · **35 days** · grid (73, 5) · owner: national

Fund protection and resettlement while accepting additional social responsibilities.

Prerequisites: (competitive_legitimacy).
Exclusive with: none.

- Active programme: $0.00100bn/week (replacement slot)
- Replace korea:strategy:
- Foreign influence defence: +7%
- Stability: +2%
- Weekly social expenses: +6%

### Working Contacts

`COLDWAR_KOR_reciprocal_contacts` · **35 days** · grid (72, 6) · owner: national

Offer narrow working contacts even when a larger political settlement has failed.

Prerequisites: (verified_restraint OR defector_protection).
Exclusive with: none.

- offer: working_contacts
- note: Alternative to a stalled nonaggression agreement

### Offer a Confederation

`COLDWAR_KOR_sovereign_confederation` · **70 days** · grid (71, 7) · owner: national

Propose a confederal forum with separate governments, armed forces and economies.

Prerequisites: (reciprocal_contacts).
Exclusive with: two_governments.

- offer: sovereign_confederation
- condition: accepted working_contacts OR nonaggression_compact
- Requirement: accepted working_contacts OR nonaggression_compact

### Parallel Recognition

`COLDWAR_KOR_two_governments` · **35 days** · grid (73, 7) · owner: national

Negotiate equal external representation and coexistence without dissolving either state.

Prerequisites: (reciprocal_contacts).
Exclusive with: sovereign_confederation.

- offer: parallel_recognition
- condition: accepted working_contacts OR nonaggression_compact
- Requirement: accepted working_contacts OR nonaggression_compact

### A Joint Secretariat

`COLDWAR_KOR_confederal_secretariat` · **35 days** · grid (71, 8) · owner: national

Offer a modest joint secretariat; cost and benefits begin only after both sides accept.

Prerequisites: (sovereign_confederation).
Exclusive with: none.

- offer: confederal_secretariat
- condition: accepted sovereign_confederation
- Requirement: accepted sovereign_confederation

Bypass: {'condition': 'Final refusal or 60-day pending expiry of sovereign_confederation; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_sovereign_confederation_refused has_country_flag = COLDWAR_KOR_sovereign_confederation_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### Inter-Korean Trade

`COLDWAR_KOR_limited_trade` · **35 days** · grid (73, 8) · owner: national

Offer a capped, funded trade arrangement with reciprocal obligations.

Prerequisites: (two_governments).
Exclusive with: none.

- offer: limited_trade
- condition: accepted parallel_recognition
- Requirement: accepted parallel_recognition

Bypass: {'condition': 'Final refusal or 60-day pending expiry of parallel_recognition; dispatch focus earned; not signed', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_parallel_recognition_refused has_country_flag = COLDWAR_KOR_parallel_recognition_expired }', 'effects': 'None. Accepted follow-up policy is forfeited; common continuation remains reachable. A later signed contract grants only its own contract effects.'}

### A Korean Settlement

`COLDWAR_KOR_korean_settlement` · **35 days** · grid (72, 9) · owner: national

Ratify the chosen settlement. Territorial integration, annexation and faction transfers require a separate explicit bilateral treaty.

Prerequisites: (confederal_secretariat OR limited_trade).
Exclusive with: none.

- action: conditional_peninsula_review

Completion alternatives: {"signed secretariat or signed limited trade": "Joint ratification decision; no forced annexation", "offer conclusively refused/expired": "Unilateral Peninsula Policy Review; +25 political power; no membership or treaty bonuses"}

### Reciprocal Obligations

`COLDWAR_KOR_korean_implementation_review` · **35 days** · grid (72, 10) · owner: national

Review which commitments were actually accepted. A failed settlement leaves a domestic liaison office, not a fictitious joint institution.

Prerequisites: (korean_settlement).
Exclusive with: none.

- Treasury: -$1bn (once)
- Replace korea:liaison_admin:
- Weekly bureaucracy expenses: +4%
- action: verify_korean_signatures

### Civilian Exchanges

`COLDWAR_KOR_civilian_exchange_priority` · **35 days** · grid (71, 11) · owner: national

Prioritize human contacts with an agreed exchange programme and exposure to external influence.

Prerequisites: (korean_implementation_review).
Exclusive with: verification_priority.

- Replace korea:contact_priority:
- Trade opinion factor: +5%
- Foreign influence defence: -3%
- Weekly bureaucracy expenses: +3%
- offer: cultural_exchanges

### Verification First

`COLDWAR_KOR_verification_priority` · **35 days** · grid (73, 11) · owner: national

Prioritize reciprocal notification and incident management; Pyongyang may refuse.

Prerequisites: (korean_implementation_review).
Exclusive with: civilian_exchange_priority.

- Replace korea:contact_priority:
- Division defence on core territory: +4%
- Political power gain: -3%
- offer: border_notifications

### Agreed Cultural Visits

`COLDWAR_KOR_cultural_visits` · **35 days** · grid (71, 12) · owner: national

Offer limited educational and cultural visits under a separately signed programme.

Prerequisites: (civilian_exchange_priority).
Exclusive with: none.

- offer: cultural_visits
- condition: accepted cultural_exchanges

Bypass: {'condition': 'Final refusal or expiry of cultural_exchanges', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_cultural_exchanges_refused has_country_flag = COLDWAR_KOR_cultural_exchanges_expired }', 'effects': 'No payment or agreement reward. Domestic liaison continuation remains available.'}

### Border Notice Rules

`COLDWAR_KOR_border_notice_protocol` · **35 days** · grid (73, 12) · owner: national

Offer reciprocal notification procedures without granting military access or control.

Prerequisites: (verification_priority).
Exclusive with: none.

- offer: border_notice_protocol
- condition: accepted border_notifications

Bypass: {'condition': 'Final refusal or expiry of border_notifications', 'native_pattern': 'OR = { has_country_flag = COLDWAR_KOR_border_notifications_refused has_country_flag = COLDWAR_KOR_border_notifications_expired }', 'effects': 'No payment or agreement reward. Domestic liaison continuation remains available.'}

### Peninsula Liaison

`COLDWAR_KOR_peninsula_liaison_office` · **35 days** · grid (72, 13) · owner: national

Fund the Southern liaison service. Partner participation still depends on signed agreements.

Prerequisites: (cultural_visits OR border_notice_protocol).
Exclusive with: none.

- Treasury: -$1bn (once)
- Active programme: $0.00100bn/week (replacement slot)
- Replace korea:liaison_admin:
- Trade opinion factor: +3%
- Weekly bureaucracy expenses: +5%

### A Korean Community

`COLDWAR_KOR_community_dialogue` · **35 days** · grid (72, 14) · owner: national

Offer a common-community dialogue grounded in the 1989 proposal. Earlier initiatives are alternate history; no merger, territorial transfer or 1991 treaty is automatic.

Prerequisites: (peninsula_liaison_office).
Exclusive with: none.

- offer: korean_community_dialogue

## Kim Jong-pil · civilian conservatism

Entry condition: ruling_party = 0 AND incumbent Kim Jong-pil; NDRP identity after reorganization.

### Kim Jong-pil

`COLDWAR_KOR_kjp_civilian_cabinet` · **14 days** · grid (54, 19) · owner: leader:Kim Jong-pil

A civilian conservative government combines administrative experience with the contested legacy of the 1961 order. His presidential office is alternate history, grounded in his actual conservative party and prime-ministerial career.

Prerequisites: Independent programme entry.
Exclusive with: none.

- Replace kjp:mandate:
- Political power gain: +6%
- Weekly bureaucracy expenses: -3%
- Stability: -2%
- condition: actual Kim Jong-pil government
- Requirement: Actual governing party/leader and legal settlement remain valid at completion
- Requirement: actual Kim Jong-pil government

### Conservative Coalition

`COLDWAR_KOR_kjp_coalition` · **35 days** · grid (53, 20) · owner: leader:Kim Jong-pil

Build a parliamentary conservative coalition without a return to presidential emergency rule.

Prerequisites: (kjp_civilian_cabinet).
Exclusive with: kjp_executive.

- Replace kjp:coalition:
- Stability: +6%
- Political power gain: -6%
- action: conservative_merger
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Executive Coordination

`COLDWAR_KOR_kjp_executive` · **35 days** · grid (55, 20) · owner: leader:Kim Jong-pil

Preserve executive coordination while accepting suspicions of the old governing networks.

Prerequisites: (kjp_civilian_cabinet).
Exclusive with: kjp_coalition.

- Replace kjp:coalition:
- Construction speed: +6%
- Political power gain: +6%
- Stability: -4%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Coalition Committees

`COLDWAR_KOR_kjp_coalition_committees` · **35 days** · grid (53, 21) · owner: leader:Kim Jong-pil

Share parliamentary authority and preserve a civilian political organization.

Prerequisites: (kjp_coalition).
Exclusive with: none.

- Replace kjp:coalition:
- Stability: +8%
- Political power gain: -8%
- Weekly bureaucracy expenses: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Professional Cabinet

`COLDWAR_KOR_kjp_professional_cabinet` · **35 days** · grid (55, 21) · owner: leader:Kim Jong-pil

Professional ministers coordinate development under a strong civilian executive.

Prerequisites: (kjp_executive).
Exclusive with: none.

- Replace kjp:coalition:
- Construction speed: +8%
- Political power gain: +6%
- Stability: -5%
- Weekly bureaucracy expenses: +3%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Provincial Credit

`COLDWAR_KOR_kjp_provincial_credit` · **49 days** · grid (54, 22) · owner: leader:Kim Jong-pil

Invest in Chungcheong without a permanent regional loyalty bonus.

Prerequisites: (kjp_coalition_committees OR kjp_professional_cabinet).
Exclusive with: none.

- Treasury: -$2bn (once)
- State 606: +1 industrial_complex (paid, once)
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Small-Enterprise Pact

`COLDWAR_KOR_kjp_small_enterprise` · **35 days** · grid (53, 23) · owner: leader:Kim Jong-pil

Broaden credit access beyond dominant industrial groups.

Prerequisites: (kjp_provincial_credit).
Exclusive with: kjp_large_industry.

- Treasury: -$1bn (once)
- Replace kjp:enterprise:
- Civilian factory construction: +8%
- Civilian industry productivity: +1%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Strategic Industry

`COLDWAR_KOR_kjp_large_industry` · **35 days** · grid (55, 23) · owner: leader:Kim Jong-pil

Preserve industrial scale through negotiated state guarantees.

Prerequisites: (kjp_provincial_credit).
Exclusive with: kjp_small_enterprise.

- Active programme: $0.00200bn/week (replacement slot)
- Replace kjp:enterprise:
- Interest rate (percentage points before native clamps): +0.3 percentage points
- Civilian industry productivity: +6%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Supplier Networks

`COLDWAR_KOR_kjp_supplier_networks` · **35 days** · grid (53, 24) · owner: leader:Kim Jong-pil

Give provincial suppliers access to procurement and enforceable contracts.

Prerequisites: (kjp_small_enterprise).
Exclusive with: none.

- Replace kjp:enterprise:
- Civilian factory construction: +10%
- Weekly bureaucracy expenses: +3%
- Civilian industry productivity: +2%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### An Export Compromise

`COLDWAR_KOR_kjp_export_compromise` · **35 days** · grid (55, 24) · owner: leader:Kim Jong-pil

Combine export targets and executive bargaining with larger financial exposure.

Prerequisites: (kjp_large_industry).
Exclusive with: none.

- Active programme: $0.00300bn/week (replacement slot)
- Replace kjp:enterprise:
- Interest rate (percentage points before native clamps): +0.4 percentage points
- Stability: -2%
- Civilian industry productivity: +8%
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### A Civilian Party

`COLDWAR_KOR_kjp_party_settlement` · **35 days** · grid (54, 25) · owner: leader:Kim Jong-pil

Consolidate an independent civilian conservative party; a 1990-style merger remains a separate political bargain.

Prerequisites: (kjp_supplier_networks OR kjp_export_compromise).
Exclusive with: none.

- Replace kjp:settlement:
- Stability: +5%
- Political power gain: -4%
- action: constitutional_party_guarantees
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Pragmatic Diplomacy

`COLDWAR_KOR_kjp_korean_policy` · **35 days** · grid (54, 26) · owner: leader:Kim Jong-pil

Offer practical working contacts while preserving separate Southern institutions.

Prerequisites: (kjp_party_settlement).
Exclusive with: none.

- Replace kjp:foreign:
- Trade opinion factor: +4%
- Political power gain: -3%
- offer: working_contacts
- Requirement: Actual governing party/leader and legal settlement remain valid at completion

### Coalition Brokerage

`COLDWAR_KOR_kjp_coalition_broker` · **35 days** · grid (53, 27) · owner: leader:Kim Jong-pil

Trade a distinct party identity for influence inside a negotiated governing coalition.

Prerequisites: (kjp_korean_policy).
Exclusive with: kjp_independent_party.

- Replace kjp:coalition_identity:
- Political power gain: +12%
- Stability: -3%
- Weekly bureaucracy expenses: +4%

### An Independent Party

`COLDWAR_KOR_kjp_independent_party` · **35 days** · grid (55, 27) · owner: leader:Kim Jong-pil

Preserve an independent conservative organization and accept reduced executive leverage.

Prerequisites: (kjp_korean_policy).
Exclusive with: kjp_coalition_broker.

- Treasury: -$1bn (once)
- Replace kjp:coalition_identity:
- Stability: +5%
- Civilian factory construction: +4%
- Political power gain: -6%

## Agreement option effects

Terms are offered by KOR; both players remain free to refuse. The following are proposed new content contracts built with existing MD primitives. Each has 60-day pending expiry, a 180-day failed-offer cooldown, two-party revalidation, a once-only signature, visible response effects and proposer notification. All recurring charges/income use native weekly rates.

### Red Cross Channel

`COLDWAR_KOR_red_cross_channel` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Exchange humanitarian liaison representatives. No passive stat reward.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Family Reunions

`COLDWAR_KOR_family_reunions` · recipient: **NKO** · term: 1095 days

Each Korea pays $1bn to establish visits and $0.001bn weekly for three years; each gains +2.5% stability. Separate from existing remittance schemes.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "humanitarian", "modifiers": {"stability_factor": 0.025}}]`.
- Recipient accepted effects: `{"treasury_change": -1, "weekly_expense_bn": 0.001, "policy": {"stability_factor": 0.025}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Military Hotline

`COLDWAR_KOR_military_hotline` · recipient: **NKO** · term: 1095 days

Both fund $0.0005bn weekly communication links. Core defence +2%, bureaucracy expenses +2%; no offensive coordination.

- KOR payment on acceptance: $0bn once; $0.00050bn/week.
- KOR accepted policy: `[{"slot": "hotline", "modifiers": {"army_core_defence_factor": 0.02, "bureaucracy_cost_multiplier_modifier": 0.02}}]`.
- Recipient accepted effects: `{"weekly_expense_bn": 0.0005, "policy": {"army_core_defence_factor": 0.02, "bureaucracy_cost_multiplier_modifier": 0.02}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Nonaggression Compact

`COLDWAR_KOR_nonaggression_compact` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Add a native bilateral nonaggression pact after acceptance; no forced military access, faction, disarmament or territory. Existing alliances remain subject to their own treaties.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Verified Restraint

`COLDWAR_KOR_verified_restraint` · recipient: **NKO** · term: 1095 days

Each side pays $1bn plus $0.001bn weekly for reciprocal verification; stability +3%, division attack -3%. Military commitments end on withdrawal or bilateral war.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "verification", "modifiers": {"stability_factor": 0.03, "army_attack_factor": -0.03}}]`.
- Recipient accepted effects: `{"treasury_change": -1, "weekly_expense_bn": 0.001, "policy": {"stability_factor": 0.03, "army_attack_factor": -0.03}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Working Contacts

`COLDWAR_KOR_working_contacts` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Maintain official working contacts; no free industrial or military effect.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Sovereign Confederation

`COLDWAR_KOR_sovereign_confederation` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Use the existing NKO confederation-channel model for a sovereign consultative framework. Separate governments, armies, economics and player control; no automatic faction, puppet or annexation.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{"add_ideas": "COLDWAR_KOR_confederal_member"}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

- KOR membership effect: `{"add_ideas": "COLDWAR_KOR_confederal_member"}`.

### Confederal Secretariat

`COLDWAR_KOR_confederal_secretariat` · recipient: **NKO** · term: 1095 days

Both pay $1bn and $0.002bn weekly for a consultative secretariat; trade opinion +4%, bureaucracy expenses +3%. No organizational focus until the actual membership spirit is present.

- KOR payment on acceptance: $1bn once; $0.00200bn/week.
- KOR accepted policy: `[{"slot": "secretariat", "modifiers": {"trade_opinion_factor": 0.04, "bureaucracy_cost_multiplier_modifier": 0.03}}]`.
- Recipient accepted effects: `{"treasury_change": -1, "weekly_expense_bn": 0.002, "policy": {"trade_opinion_factor": 0.04, "bureaucracy_cost_multiplier_modifier": 0.03}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Parallel Recognition

`COLDWAR_KOR_parallel_recognition` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Recognize parallel governments through mutual declarations. No free UN membership, diplomatic recognition from third parties or annexation.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Limited Trade

`COLDWAR_KOR_limited_trade` · recipient: **NKO** · term: 1095 days

KOR funds $1bn access and $0.002bn weekly purchases to NKO; both gain civilian industrial productivity +2.5%, influence defence -3%. Capped abstraction of civilian exchange, no free resources or arms.

- KOR payment on acceptance: $1bn once; $0.00200bn/week.
- KOR accepted policy: `[{"slot": "korean_trade", "modifiers": {"foreign_influence_defense_modifier": -0.03, "civilian_factories_productivity": 0.025}}]`.
- Recipient accepted effects: `{"treasury_change": 1, "policy": {"foreign_influence_defense_modifier": -0.03, "civilian_factories_productivity": 0.025}, "weekly_income_bn": 0.002}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Northern Security Compact

`COLDWAR_KOR_northern_security_compact` · recipient: **NKO** · term: 1095 days

Only for an actual RPR government. KOR pays NKO $1bn plus $0.001bn weekly for military liaison; limited readiness, dependence and external-access effects. No automatic allied formations.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "north_security", "modifiers": {"army_org_factor": 0.04, "foreign_influence_defense_modifier": -0.08, "trade_opinion_factor": -0.04}}]`.
- Recipient accepted effects: `{"treasury_change": 1, "weekly_income_bn": 0.001, "policy": {"army_org_factor": 0.02, "trade_opinion_factor": -0.02}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Independent Left Dialogue

`COLDWAR_KOR_independent_left_dialogue` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Open talks from an independent Southern socialist government; no union or surrender of sovereignty.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Technology Licence

`COLDWAR_KOR_technology_licence` · recipient: **One chosen consenting supplier: JAP or USA** · term: 1095 days

KOR pays the supplier $1bn plus $0.001bn weekly for industrial know-how. Civilian industrial productivity +3%, influence defence -3%; no technology completion or research-year bypass.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "licence", "modifiers": {"foreign_influence_defense_modifier": -0.03, "civilian_factories_productivity": 0.03}}]`.
- Recipient accepted effects: `{"treasury_change": 1, "weekly_income_bn": 0.001}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Allied Procurement Contract

`COLDWAR_KOR_allied_procurement_contract` · recipient: **USA** · term: 1095 days

KOR pays $2bn and $0.001bn weekly for access and maintenance; equipment expenses -4%, influence defence -4%. Equipment transfers require separately priced native equipment contracts.

- KOR payment on acceptance: $2bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "procurement_access", "modifiers": {"equipment_cost_multiplier_modifier": -0.04, "foreign_influence_defense_modifier": -0.04}}]`.
- Recipient accepted effects: `{"treasury_change": 2, "weekly_income_bn": 0.001}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Us Alliance Assurance

`COLDWAR_KOR_us_alliance_assurance` · recipient: **USA** · term: 1095 days

KOR funds $1bn plus $0.002bn weekly alliance liaison. Core defence +4%, organization +2%, influence defence -6%. No US unit deployment is ordered by the focus.

- KOR payment on acceptance: $1bn once; $0.00200bn/week.
- KOR accepted policy: `[{"slot": "assurance", "modifiers": {"army_core_defence_factor": 0.04, "army_org_factor": 0.02, "foreign_influence_defense_modifier": -0.06}}]`.
- Recipient accepted effects: `{"treasury_change": 1, "weekly_income_bn": 0.002}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Security Partner Contacts

`COLDWAR_KOR_security_partner_contacts` · recipient: **One chosen consenting partner: JAP or USA** · term: 1095 days

KOR pays $1bn for limited staff cooperation; organization +2.5%, bureaucracy expenses +2.5%.

- KOR payment on acceptance: $1bn once; $0.00000bn/week.
- KOR accepted policy: `[{"slot": "partner", "modifiers": {"army_org_factor": 0.025, "bureaucracy_cost_multiplier_modifier": 0.025}}]`.
- Recipient accepted effects: `{"treasury_change": 1}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Japan Technology Finance

`COLDWAR_KOR_japan_technology_finance` · recipient: **JAP** · term: 1095 days

KOR pays $2bn plus $0.001bn weekly to Japanese technical partners; civilian industrial productivity +4%, influence defence -4%. Claims are not settled by accepting technical cooperation.

- KOR payment on acceptance: $2bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "japan_contract", "modifiers": {"foreign_influence_defense_modifier": -0.04, "civilian_factories_productivity": 0.04}}]`.
- Recipient accepted effects: `{"treasury_change": 2, "weekly_income_bn": 0.001}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Historical Claims Dialogue

`COLDWAR_KOR_historical_claims_dialogue` · recipient: **JAP** · term: political framework; no perpetual passive stat grant

Open a historical-claims dialogue. No automated reparations, tribunal outcome or financial benefit.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Alternative Finance Contacts

`COLDWAR_KOR_alternative_finance_contacts` · recipient: **One chosen consenting partner: USA or GER** · term: 1095 days

KOR pays $1bn for financial access; interest-rate adjustment -0.25 points, influence defence -2.5%. No direct debt cancellation.

- KOR payment on acceptance: $1bn once; $0.00000bn/week.
- KOR accepted policy: `[{"slot": "capital_contacts", "modifiers": {"interest_rate_multiplier_modifier": -0.25, "foreign_influence_defense_modifier": -0.025}}]`.
- Recipient accepted effects: `{"treasury_change": 1}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Nordpolitik Recognition

`COLDWAR_KOR_nordpolitik_recognition` · recipient: **Separate contracts with SOV and CHI** · term: 1095 days

Each bilateral contract yields trade opinion +3% and bureaucracy expenses +2% to both sides. SOV and CHI offers use separate signatures and cannot duplicate a partner’s bonus.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[{"slot": "recognition", "modifiers": {"trade_opinion_factor": 0.03, "bureaucracy_cost_multiplier_modifier": 0.02}}]`.
- Recipient accepted effects: `{"policy": {"trade_opinion_factor": 0.03, "bureaucracy_cost_multiplier_modifier": 0.02}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Pacific Trade Contacts

`COLDWAR_KOR_pacific_trade_contacts` · recipient: **JAP** · term: 1095 days

KOR pays $1bn plus $0.001bn weekly for technical export access; civilian industrial productivity +2.5%, influence defence -2.5%.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "pacific_contract", "modifiers": {"foreign_influence_defense_modifier": -0.025, "civilian_factories_productivity": 0.025}}]`.
- Recipient accepted effects: `{"treasury_change": 1, "weekly_income_bn": 0.001}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Revolutionary Recognition

`COLDWAR_KOR_revolutionary_recognition` · recipient: **SOV** · term: 1095 days

A revolutionary government requests recognition; no free aid or automatic Soviet alliance.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[{"slot": "revolutionary_recognition", "modifiers": {"trade_opinion_factor": 0.04, "foreign_influence_defense_modifier": -0.04}}]`.
- Recipient accepted effects: `{"policy": {"trade_opinion_factor": 0.02}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Neutrality Guarantees

`COLDWAR_KOR_neutrality_guarantees` · recipient: **USA, NKO, SOV and CHI; all four must assent** · term: political framework; no perpetual passive stat grant

A negotiation framework for neutrality. No alliance withdrawal or guarantee changes until all signatories and KOR separately ratify final terms.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Vietnam Withdrawal Settlement

`COLDWAR_KOR_vietnam_withdrawal_settlement` · recipient: **SVN and USA; separate replies required** · term: 1095 days

Only if a real ongoing KOR Vietnam deployment/commitment is present. KOR pays $1bn veterans’ settlement; stability +3%, weekly social expenses +3%. The current empty 1970 OOB does not establish a deployment. Otherwise bypass with no payout.

- KOR payment on acceptance: $1bn once; $0.00000bn/week.
- KOR accepted policy: `[{"slot": "veterans", "modifiers": {"stability_factor": 0.03, "social_cost_multiplier_modifier": 0.03}}]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Cultural Exchanges

`COLDWAR_KOR_cultural_exchanges` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Agree a limited civilian-exchange framework. No automatic visits or passive stat bonus.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Cultural Visits

`COLDWAR_KOR_cultural_visits` · recipient: **NKO** · term: 1095 days

Each country pays $1bn plus $0.001bn weekly for agreed cultural and educational visits; trade opinion +4%, influence defence -2%.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "visits", "modifiers": {"trade_opinion_factor": 0.04, "foreign_influence_defense_modifier": -0.02}}]`.
- Recipient accepted effects: `{"treasury_change": -1, "weekly_expense_bn": 0.001, "policy": {"trade_opinion_factor": 0.04, "foreign_influence_defense_modifier": -0.02}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Border Notifications

`COLDWAR_KOR_border_notifications` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Agree a framework for military incident notifications. No automatic military access or disarmament.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Border Notice Protocol

`COLDWAR_KOR_border_notice_protocol` · recipient: **NKO** · term: 1095 days

Each country pays $1bn plus $0.001bn weekly for reciprocal notifications; core defence +2.5%, bureaucracy expenses +3%.

- KOR payment on acceptance: $1bn once; $0.00100bn/week.
- KOR accepted policy: `[{"slot": "notices", "modifiers": {"army_core_defence_factor": 0.025, "bureaucracy_cost_multiplier_modifier": 0.03}}]`.
- Recipient accepted effects: `{"treasury_change": -1, "weekly_expense_bn": 0.001, "policy": {"army_core_defence_factor": 0.025, "bureaucracy_cost_multiplier_modifier": 0.03}}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

### Korean Community Dialogue

`COLDWAR_KOR_korean_community_dialogue` · recipient: **NKO** · term: political framework; no perpetual passive stat grant

Negotiate a common-community agenda inspired by the1989 formula. Separate governments and armed forces remain; neither side is forced to unify or sign the1991 Basic Agreement.

- KOR payment on acceptance: $0bn once; $0.00000bn/week.
- KOR accepted policy: `[]`.
- Recipient accepted effects: `{}`.

No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.

## Event and decision timeline

### Labour Law and Enforcement

Jeon Tae-il’s protest exposed dangerous working conditions and the failure to enforce existing protections. A tragedy is not a beneficial policy action.

Trigger: Historical date and an actual unresolved workplace-rights crisis, or a separately named earlier equivalent

- **Enforce Existing Protections:** Create lawful inspection/mediation process; bureaucracy expenses +3%; no automatic universal insurance.
- **Retain Wage Discipline:** Retain the actual export/labor policy and its legitimacy costs; no reward from a death.

### The Presidential Contest

The 1971 Park–Kim Dae-jung contest follows the 1969 amendment.

Trigger: Native election/constitutional contest or a player-initiated early constitutional crisis

- **Respect the Competitive Mandate:** competitive election settlement; stability +3%; PP -50; election resolves through party system
- **Prepare an Executive Emergency:** constitutional crisis receipt; stability -5%; PP +50; permits Yushin proposal, does not enact it automatically

### YH and the Parliamentary Opposition

The YH workers’ sit-in and police raid connected workplace grievances to NDP politics; they are not the same event as the later mass labor surge.

Trigger: An actual export-firm labor dispute and opposition crisis; historical1979 reference

- **Accept Workplace Mediation:** Authorize mediation and preserve records; do not install an opposition government.
- **Clear the Political Occupation:** Record repression/rights consequences and unresolved grievances; no positive stability gift.

### The Busan–Masan Crisis

Regional mass protest followed the exclusion of Kim Young-sam and the escalating late-Yushin crisis.

Trigger: Actual Yushin/political exclusion crisis, or a separately framed alternate crisis

- **Open a Political Channel:** Authorize an early negotiated opening; no automatic successor.
- **Maintain Emergency Rule:** Retain emergency controls and their actual costs; preserve the crisis record.

### A Presidential Succession Crisis

Park’s assassination produced Choi Kyu-hah’s interim presidency, not an immediate automatic Chun government.

Trigger: Park dies/leaves office, or a separately resolved leadership crisis; historical branch dated 26 October 1979

- **Support the Interim Civilian Government:** install Choi through reconciled native office machinery; 180d interim spirit: PP -10%, stability -3%; open constitutional negotiations
- **Submit to an Officer Council:** open military contest decisions; no automatic coup victory; 90d contested-command spirit: organization -5%, stability -5%

### The December Officer Challenge

Chun’s seizure of military command preceded his presidential rule.

Trigger: Interim government and active Hanahoe challenge; historical 12 December precedent

- **Defend Civilian Command:** PP -75; 90d organization -5%; if legitimate command wins, competitive-election route; if defeated, officer-controlled transition
- **Concede Military Command:** party 22 transition proposal; stability -5%; retains contested-command burden until settlement

### The Nationwide Martial-Law Decision

The 17May extension, political arrests and Assembly closure preceded the 18–27May Gwangju events.

Trigger: A resolved officer-control crisis with an actual decision on renewed emergency rule

- **Continue Civilian Talks:** Keep the civilian negotiating window open.
- **Extend Nationwide Martial Law:** Set nationwide_martial_law; political activity is restricted and the legitimacy burden remains; no free civil-democratic rights.

### The Martial-Law Crisis

The 18–27May Gwangju uprising and suppression are separate from the 17May emergency measures and the earlier officer coup. Preserve case evidence and the lasting accountability claim.

Trigger: After a separately resolved17May nationwide martial-law expansion and actual violent suppression, historical18–27May1980; never the12December1979 coup itself

- **Negotiate Civilian Guarantees:** PP -75; 180d organization -3%; restore political participation and open direct-election settlement
- **Extend Nationwide Martial Law:** enable controlled Fifth Republic; persistent legitimacy scar: stability -8%, trade opinion -5%, police expenses +8%; no positive instant reward

### The Opposition Reorganizes

NKDP organization reconnects the Two Kims and constitutional opposition.

Trigger: Legal opposition recovers parliamentary weight; historical 1985 NKDP breakthrough

- **A Joint Reform Ticket:** native party 2 leadership contest; PP -50; maintains combined reform organization
- **Separate Democratic Organizations:** retain distinct YS/RDP and DJ/PDP identity receipts; split the existing reform vote through native party machinery, never create free popularity

### Torture, Disclosure and Accountability

Park Jong-cheol died under police torture; disclosure and the attempted cover-up became central to the 1987 crisis.

Trigger: A recorded state-abuse/disclosure crisis; use generic naming for alternate earlier cases

- **Protect the Investigation:** Preserve evidence and support an independent inquiry.
- **Suppress Disclosure:** Record continuing rights and credibility costs; do not delete the case on a later government change.

### Constitutional Defense or Revision

Chun’s 13April measure deferred constitutional revision and fueled the demand to end indirect selection.

Trigger: Actual military-led government facing a constitutional demand

- **Accept Revision Talks:** Authorize military_opening_authorized after a real government agreement.
- **Defend Indirect Selection:** Keep the existing rule, opposition campaign and costs; reopening talks later remains possible.

### The June Democracy Movement

Lee Han-yeol was injured on 9June and died on 5July. The June 10 rally, June 18 protest and June 26 march preceded the 29June declaration.

Trigger: Actual constitutional mobilization; earlier negotiated alternatives do not fabricate these dated casualties

- **Authorize a Negotiating Mandate:** Open the shared constitutional process under an accepted public mandate.
- **Refuse the Demand:** Keep the political crisis and its costs. No date automatically resolves it.

### The Direct-Election Settlement

Park Jong-cheol’s torture death and exposure, the 13April constitutional-defense measure, Lee Han-yeol’s 9June injury and the June 10–26 mobilization preceded Roh’s 29June concession. The concession opened negotiations; it did not itself ratify the constitution or predetermine the winner.

Trigger: Constitutional demand, protest escalation and a real government response; historical June 1987 precedent

- **Accept Direct Presidential Elections:** Authorize constitutional negotiations and the direct-election principle; PP -75. Actual ratification/election follows the shared transition. No automatic democracy or Roh appointment.
- **Defend Indirect Selection:** PP +25; stability -8%; police expenses +8%; civic unrest remains and Nordpolitik elected-leader branch unavailable

### The Great Workers’ Struggle

The post-June labor upsurge was a distinct organizing wave, especially in heavy industry; constitutional reform did not settle every workplace demand.

Trigger: An actual post-opening workplace-organizing wave; not erased by the1970 or1979 labor response

- **Recognize Lawful Bargaining:** Register the actual native labor faction if needed; preserve existing opinion and negotiate enforceable terms.
- **Restrict the New Unions:** Record the separate industrial and rights dispute; previous labor milestones remain historical receipts.

### The Constitutional Bargain

The eight-member ruling/opposition talks and Assembly process produced the agreed text submitted to voters in October.

Trigger: Real charter mandate, chosen model and actual party endorsements

- **Submit the Agreed Text:** Use the 30-day ratification event; no guaranteed approval.
- **Return to Negotiation:** Preserve the chosen model; renegotiate endorsements and safeguards without focus reset.

### Constitutional Review Becomes Operational

The court’s creation in the 1987 constitution and its 1988 operational beginning are separate institutional stages.

Trigger: Court legal basis enacted, appointments/implementation completed and constitutional order active; earlier operation is alternate history

- **Commence Judicial Review:** Run the already funded implementation event only with court_appointments_implemented and court_implementation_pending; activate the actual court reader once.
- **Delay Appointments:** Retain the legal mandate but do not grant an operational court or its modifier.

### The Conservative Coalition Talks

DJP + RDP + NDRP formed the DLP; Kim Dae-jung’s PDP remained outside.

Trigger: Actual Roh, YS and KJP party organizations have separately authorized a merger; historical January 1990 precedent

- **Ratify the Conservative Merger:** native coalition/identity update and existing support redistribution only; PP +75, stability -3%; independent DJ opposition preserved
- **Keep the Parties Independent:** no forced transfer of support; PP +25; separate programmes and elections continue

## Military-to-democratic transition rules

Research was completed before expansion. Constitutional approval, an election result and civilian command are separate milestones.

- **root:** COLDWAR_KOR_constitutional_question
- **focuses:** 36
- **entry_routes:** Electoral contest; legitimate caretaker succession; negotiated military withdrawal. Entries are not permanently mutually exclusive: a failed early window may be followed by later talks.
- **military_failure:** The command-challenge action sends a real resolution event. Successful civilian command sets negotiating_commitment. Failure sets military_reconsolidation, retains command burden and allows a later authorized military opening. It does not install Chun before a separate actual office transition.
- **ratification:** {"event": "COLDWAR_KOR_transition.30", "pending_days": 30, "reject_retry_days": 90, "vote_model": "Gameplay abstraction: charter supporters are a unique set of actual party/organization slots. Sum their current native party_pop_array shares divided by the sum of current legal participating shares. Passing requires strictly more than50%; no bonus popularity is created.", "accept": "Set constitutional_ratification_passed and exactly one selected constitutional model; call the actual politics/election configuration. No leader is installed by this vote.", "reject": "No constitutional programme or election-rule grant. Keep the chosen model; return to negotiation through a repeatable50PP redraft decision after90d. Do not reset focuses or replay rewards.", "resubmit_decision": "COLDWAR_KOR_reopen_charter_ballot", "model_rejection_rule": "Keep the previously chosen model1/2/3. Negotiations may change safeguards/endorsements within that model; resubmit by decision after90d. Changing the model requires a separate constitutional-reversal process, not free focus reset.", "eligible_slots": {"ordinary": [0, 1, 2, 3], "conditional": {"4": "Only after a legal revolutionary-party participation settlement", "5": "civic_legal_5", "19": "civic_legal_19", "22": "Only an actually formed legal DJP electoral vehicle; an Army institution alone is not a ballot party"}, "excluded": "KCIA7, EPB13 and non-party association slots are not independently counted as ballot parties. Native banned parties are excluded."}, "denominator": "Sum party_pop_array^s for every currently eligible, non-banned electoral party, whether endorsing or opposing. Endorsement membership is a subset, never the whole denominator by definition.", "supporter_membership": "Unique charter_supporter_s flags are set only by accepted, recorded party endorsement. Iterate each eligible slot once; sum its current native popularity only when that receipt is present.", "zero_denominator": "Support share remains0 and the vote is rejected/postponed with a data/eligibility diagnostic in the review log. Never divide by zero, fabricate an electorate or grant automatic passage.", "native_calculation": "set_temp_variable = { COLDWAR_KOR_charter_support = 0 }\nset_temp_variable = { COLDWAR_KOR_charter_electorate = 0 }\nif = {\n  limit = { check_variable = { party_banned_array^0 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^0 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_0 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^0 } }\n}\nif = {\n  limit = { check_variable = { party_banned_array^1 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^1 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_1 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^1 } }\n}\nif = {\n  limit = { check_variable = { party_banned_array^2 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^2 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_2 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^2 } }\n}\nif = {\n  limit = { check_variable = { party_banned_array^3 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^3 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_3 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^3 } }\n}\nif = {\n  limit = { has_country_flag = COLDWAR_KOR_electoral_party_4_legal check_variable = { party_banned_array^4 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^4 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_4 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^4 } }\n}\nif = {\n  limit = { has_country_flag = COLDWAR_KOR_civic_legal_5 check_variable = { party_banned_array^5 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^5 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_5 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^5 } }\n}\nif = {\n  limit = { has_country_flag = COLDWAR_KOR_civic_legal_19 check_variable = { party_banned_array^19 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^19 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_19 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^19 } }\n}\nif = {\n  limit = { has_country_flag = COLDWAR_KOR_electoral_party_22_legal check_variable = { party_banned_array^22 = 0 } }\n  add_to_temp_variable = { COLDWAR_KOR_charter_electorate = party_pop_array^22 }\n  if = { limit = { has_country_flag = COLDWAR_KOR_charter_supporter_22 } add_to_temp_variable = { COLDWAR_KOR_charter_support = party_pop_array^22 } }\n}\nset_variable = { COLDWAR_KOR_charter_support_share = 0 }\nif = { limit = { check_variable = { COLDWAR_KOR_charter_electorate > 0 } } set_variable = { COLDWAR_KOR_charter_support_share = { value = COLDWAR_KOR_charter_support divide = COLDWAR_KOR_charter_electorate clamp = { min = 0 max = 1 } } } }"}
- **election:** Only the actual native election/coalition result sets lawful_election_completed and installs the corresponding incumbent via the reconciled KOR router. Unity-ticket agreement redistributes existing candidacy/support only; it never ensures victory.
- **national_institutions:** Court, press, electoral administration, lawful unions, local-autonomy preparation and civilian appointment rights survive ordinary cabinet change. Their policy effects require the constitutional_order receipt where specified.
- **rollback:** {"decision": "COLDWAR_KOR_constitutional_rollback", "cost": "100PP; stability -10%; requires a resolved coup or a lawful, publicly ratified constitutional reversal", "effect": "Disable constitutional_order and safeguards, lawful union/press/command dependent effects; retain earned focus receipts. No institutional bonuses under emergency rule.", "restoration": "A public constitutional restoration vote and genuine lawful mandate can restore active earned institutions. No focus reset, cash, factories, experience or one-time PP replay."}
- **court_reader:** When judicial_review and constitutional_order are active, unlawful emergency/press-ban/security-decree actions are unavailable. A lawful emergency needs the defined Assembly approval and review event; constitutional repeal follows the explicit rollback route. Operational review additionally requires judicial_review_operational, not merely a completed founding focus.
- **civil_command_reader:** With civilian_appointments and constitutional_order, the military caretaker/coup entry cannot claim lawful appointment. Its initiator must resolve the actual extra-constitutional challenge and its costs; senior appointment actions require the lawful cabinet authority.
- **labor_provider:** If lawful_labour_bargaining is enacted, register labour_unions only if absent, initialize its native state once and call change_labour_unions_opinion with temp_opinion=10. Reconcile IP_idea_configuration so lawful recognition survives ordinary government changes. Never reset existing faction opinion or infer legality from the faction idea alone.
- **historical_dates:** Historical milestones remain1971/1972/1979–80/1985/1987/1988–90. Earlier negotiated settlements and parliamentary/consensus constitutions are clearly alternate history. Local elections1991/1995 and Hanahoe dissolution1993 are not historical pre1991 rewards.
- **event_history:** Separate1970 labor,1979 YH/Bu-Ma,1979 succession,12.12 command coup,17May emergency rule,18–27May Gwangju,1985 NKDP,1987 torture/4.13/June/6.29/eight-member negotiation,1987 labor surge and1988 court operation receipts. A reform never erases later chronology.

### Constitutional decisions and implementation costs

- **COLDWAR_KOR_reopen_constitutional_talks:** 75PP; no automatic appointment or popularity. Enables Negotiated Withdrawal after a failed caretaker/command window without resetting any completed focus.
- **COLDWAR_KOR_reopen_charter_ballot:** 50PP;90d after rejection; same chosen constitutional model. The decision itself reopens the ballot; the one-shot Submit the Charter focus remains completed. No new model, focus reward or building is granted.
- **COLDWAR_KOR_register_charter_endorsement:** No new monetary fee; the party representative must accept the recorded negotiated terms. The ballot helper checks this unique per-slot endorsement against current eligible native support. Power blocs are not automatically electoral parties.
- **COLDWAR_KOR_implement_constitutional_court:** 50PP and $1bn once;90d funded implementation. Appointments follow the enacted constitution and its nomination/confirmation rules. The event rechecks constitutional order. Interruption suspends operation without refund or repeat payment; restoration resumes the already funded process.

Command-resolution choice: 75PP and $1bn once;90d command reorganization: army organization -5%, political power gain -5%. No new president is installed.


## Research-led expansion

{
  "previous_focuses": 206,
  "focuses": 298,
  "added": 92,
  "transition_focuses": 36,
  "group_deltas": {
    "transition": 36,
    "drp": 3,
    "ndp": 3,
    "reform": 4,
    "army": 3,
    "usp": 2,
    "minjung": 3,
    "rpr": 2,
    "security": 2,
    "economy": 10,
    "defence": 8,
    "foreign": 7,
    "korea": 7,
    "kjp": 2
  },
  "research_first": [
    "research_democratic_transition_expansion.md",
    "mechanics_expansion_research.md",
    "layout_expansion_research.md"
  ],
  "historical_corrections": [
    "Nordpolitik and1990 merger no longer falsely exclude one another",
    "Local councils prepared, not historically elected before1991",
    "Hanahoe dismantling before1993 explicitly alternate",
    "Direct-election commitment no longer skips the actual constitutional process"
  ]
}

## Verification boundary

Source inspections and automated graph checks can establish native API patterns, defined modifier keys, coordinates, prerequisites and slot arithmetic. They cannot prove engine acceptance, exact hover tooltips, save behavior or runtime political transitions. No HOI4 game test is claimed. New Korean adapters, events, ideas, decisions and party migration are designs awaiting implementation approval.

Reference reports: `research_history.md`, `md_reference_layout.md`, `mechanics_feasibility.md`; final review status is recorded separately in `COLDWAR_KOR_review_resolution.md`.
