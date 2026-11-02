IMPERIA COLD WAR

# Chile, January 1970 to 1990: approval concept

184 focuses, 11 political programmes, 52 reciprocal exclusion pairs, 7 starting spirits, 14 events, eight bilateral offers and one five-country Andean protocol.

This is the complete proposed design, not installed game content. All new game text is English. IDs begin COLDWAR_CHL_. All numerical effects and prices are balance proposals, not historical dollar amounts. Approve or amend the concept before implementation.

## Structure and political scope

The design uses the installed MD 2.0.4 France/Russia grammar: relative section anchors, local policy forks and OR joins, 96 by130 grid units, 165 by128 item containers and short single-line English titles. Over91% of descending donor links advance one row; ordinary Chile levels now do the same. The complete proposal spans x4..160,y0..17. The two banks are at y0 and9. There are no party-dependent branch visibility rules.

| Section | Root x,y | Focuses | Ruling subparty |
|---|---:|---:|---:|
| The Republic and its Institutions | 8,0 | 12 | Shared |
| Copper, Credit and National Development | 26,0 | 20 | Shared |
| The Armed Forces of a Pacific Republic | 48,0 | 15 | Shared |
| Christian Democratic Reform | 74,0 | 13 | 1 |
| National Party and Civilian Conservatism | 90,0 | 13 | 2 |
| Radical Republicanism | 106,0 | 11 | 3 |
| The Socialist Party and the Chilean Road | 122,0 | 13 | 18 |
| Communist Organization and Popular Unity | 138,0 | 11 | 4 |
| MAPU and Agrarian Socialism | 154,0 | 11 | 19 |
| Radical Democracy | 74,9 | 8 | 14 |
| PADENA and Provincial Populism | 90,9 | 7 | 20 |
| Gremialist Institutional Conservatism | 106,9 | 9 | 0 |
| MIR and the Revolutionary Left | 122,9 | 9 | 5 |
| The Military Government and Pinochet | 142,9 | 20 | 22 |
| Agreements across the Pacific and the Andes | 48,9 | 12 | Shared |

Initial game camera: Constitutional Mandate. Topic shortcuts: Republic, Development, Armed Forces, Foreign Agreements and the political programme roots. Continuous-focus panel: proposed lower-left pocket at768,1170px. The preview provides a full-tree atlas and native-scale branch navigation. Global shared organisation trees are not transplanted wholesale. Exact game font, connector routing, camera and continuous-panel bounds require HOI4 after approval.

PDC, PN, PR, PS, PCCh and MAPU have distinct programmes. DR and PADENA retain smaller minority programmes. MIR and Gremialismo are real movements with expressly counterfactual governing alternatives. No focus manufactures office for a minor party or movement. Military rule is an institutional rupture, with a constitutionalist early-exit alternative and a separate actual-Pinochet programme. No Muslim or monarchist filler branches are included.

PR has11 focuses, DR8 and PADENA7. Historical review suggested a10-12 combined cap, but that cap is a reviewer balance suggestion, not a user requirement: this proposal deliberately preserves separate inspectable programmes for the real parties. DR/PADENA each grant at most one paid regional building; they have less depth and scale than the dominant parties.

## Starting spirits

### A Republic under Strain

Organized mass parties compete within the 1925 constitutional order, but no bloc can easily secure consent for its programme.

- Political Power Gain: -12%; Stability: -6%; Foreign Influence Defense: +5%

### Copper and the External Account

Copper underpins export earnings. Concentrated markets and dependence on imported machinery leave public finances exposed.

- Resource Export Revenue: +6%; Trade Opinion: -8%; Interest Rate: +0.5 pp

### Unfinished Agrarian Reform

Redistribution and rural unionization have opened the countryside to change. Credit, technical assistance and disputed titles lag behind.

- Agriculture Productivity: -12%; Stability: -4%

### Inflationary Expectations

Persistent price pressure raises the cost of credit and undermines confidence in long public investment programmes.

- Interest Rate: +1 pp; Construction Speed: -6%

### Uneven Technical Education

Chile possesses capable universities and engineers, but specialist training does not yet meet the needs of a diversified economy.

- Research Speed: -7%

### A Long and Uneven Republic

Mines, farms, ports and isolated southern communities depend on transport corridors vulnerable to disruption.

- Supply Consumption: +8%; Infrastructure Construction Speed: -10%

### Cartagena Agreement Participant

Chile is a signatory of the 1969 Cartagena Agreement. Participation requires negotiated regional industrial and trade rules.

- Trade Opinion: +3%; Bureaucracy Expenditure: +2%

## Policy trade-offs

- Copper: negotiated ownership buys supplier access and export gains at a higher setup price; full nationalization gives the strongest export-income proxy with research/trade burdens and compensation choices; regulated concessions favor construction and investment with reduced resistance to foreign influence.
- Rural development: cooperatives offer a social and machinery programme; family holdings favor greater agricultural productivity with a lower tax yield. Both remedy the actual starting agrarian penalty.
- Stabilization: a negotiated wage-price compact protects social cohesion but concedes tax and political capacity; monetary restraint improves interest terms while reducing construction and stability.
- Pinochet: Chicago adjustment favors construction, credit and trade with sharp social costs; strategic state capitalism favors output and production capacity with administrative and commercial burdens. Each has further pension/social-floor or public-copper/mixed-enterprise choices. Later rule divides into managed constitutionalism, security-state continuity or an enforceable continuation plebiscite.
- Constitutional military exit is genuinely separate from personal Pinochet rule. Authoritarian coercion carries Repression, Exile and Broken Institutions, not a hidden free stability gain. Truth and reparations end active repression while preserving The Legacy of Repression.

## Runtime design contract

- **starting_leader:** Eduardo Frei Montalva, PDC slot1, January1970. Preserve starting technology and deferred OOB choices.
- **routing_fix:** Correct Chile native leader routing: slot18 Socialist Allende; slot3 Radical Baltra; slot1 period-appropriate PDC Tomic/Aylwin after Frei Montalva. Current Allende-slot3 and Frei Ruiz-Tagle early pool are incompatible with the 1970 registry.
- **party_checks:** Use existing exact *_in_power scripted triggers for each numeric subparty. No party-dependent allow_branch; branches remain visible. Military slot22 is not itself proof that Pinochet rules.
- **sync:** Party programmes retain earned variables but their dynamic modifier and weekly expenses apply only while that party actually rules. Recheck on party/leader change, daily fallback and load. Construction, research bonuses and setup payments have independent once-only receipts.
- **finance:** One-time costs use set_temp_variable treasury_change then modify_treasury_effect in the execution guard. Native borrowing remains permitted for own authorized spending. New Chile weekly totals must be integrated into calculate_additional_expenses_rate; not an already-installed Chile API.
- **copper:** Copper is an export-income proxy using resource_export_multiplier_modifier. No local_resources_copper_factor, no extra raw tungsten mislabeled copper, no invented copper building.
- **buildings:** Same-state add_extra_state_shared_building_slots, then add_building_construction instant_build=yes. Completion rechecks actual ownership/control, building native cap, province validity for province buildings and total slot capacity. If any destination is invalid, no charge, no receipt, no completion payout.
- **andean:** Chile is historically a 1969 Cartagena signatory. Seed actual treaty membership at the historical start; future accession requires ratification. Every member-only entry and continuation requires the actual membership spirit in availability and reward guards. The industrial protocol additionally requires all four recipient governments to ratify. No modern Mercosur/EU membership reward.
- **events:** This concept specifies native country-event records, recipient decisions, reply notifications and guarded options. Country-event art is not yet composed. Reinspect current donor frame and full option window before adding event assets.
- **approval:** No runtime tree, localisation, event, history, interface, idea or monetary-system file is emitted or installed by this review generator.

All Pinochet continuation focuses require his actual leadership in both availability and guarded rewards. Party and leader programmes suspend on loss of office, retaining earned receipts for a return. National assets and paid research bonuses are one-time outcomes. Party reactivation never builds another factory or charges setup again. The national financial restructuring remedy lasts365 days and its liability is retained across government changes.

Native party requirements reuse the exact existing *_are_in_power triggers, whose tooltip scripted localisation is already routed through the 1970 registry (for example conservatism_L -> MDCW_HP_conservatism -> MDCW_HP_CHL_1_0). Do not replace these with modern Chilean party names or a custom generic governing-current label. Current leader-pool mappings are a separate confirmed defect: PS/Allende belongs to18, PR/Baltra to3, and PDC succession needs Tomic/Aylwin rather than early Frei Ruiz-Tagle.

**Copper limitation:** the engine has no copper resource. Resource Export Revenue is the existing all-resource weekly export-revenue multiplier, affecting supported native resource exports; it does not create copper tonnage or income from a nonexistent copper export base. Copper institutions are represented through export, tax, engineering, credit and public/private industrial-policy effects. No new unconsumed copper modifier is proposed.

**Construction contract:** each level adds exactly one shared slot in the same selected Chilean state before instant construction. Ownership, control, native type/level caps, total slot maximum and coastline/province validity are separate guards. The slot and building sit inside one transaction receipt. These checks and the monetary debit must be revalidated together. Native maintenance, workforce and power costs still apply.

**Finance:** all cash amounts are billions. Ordinary project prices follow the current project convention of1-10billion; own spending uses native borrowing. Weekly literals are already weekly and have at most five fractional places. Rates in this design are balance values, not copied historical budgets. Starting1970 treasury is not established by the later2000 value of22. Simultaneous programme debt/interest affordability remains a required balance test, including19billion setup and0.012billion weekly for all foreign protocols.

## Election and succession contract

{
  "status": "New Chile integration using the existing MD election/party array; not an existing working Chile election event.",
  "calendar": {
    "campaign": "1970-01-01 to 1970-09-03",
    "popular_vote": "1970-09-04",
    "congress_if_needed": "1970-10-24",
    "inauguration": "1970-11-03"
  },
  "native_calendar_correction": "Current Chile1970 history uses generic last_election1968 and48months. Replace that presidential schedule in the future1970 integration with the historical1964 ballot baseline and72-month term, then record the actual1970 ballot. Restore48months for the1990 transitional presidency. Do not emit an extra1972 presidential election from the old generic schedule.",
  "campaign_receipt": "The campaign event fires once; each option calls native party support adjustment for only its stated slot. It never installs the candidate.",
  "count": "At the ballot, normalize eligible civilian party_pop_array support after native campaign/election changes. Save final candidate shares for Tomic1, Alessandri2 and Allende18, plus registered coalition endorsements. Do not count the same coalition share twice.",
  "result_record": {
    "COLDWAR_CHL_election_winner_slot": "Native ballot winner slot: 1, 2 or 18.",
    "COLDWAR_CHL_election_runner_up_slot": "Runner-up slot for congressional runoff.",
    "COLDWAR_CHL_election_confirmed_slot": "Only the candidate constitutionally confirmed by majority or Congress.",
    "COLDWAR_CHL_election_ratified": "Set only after lawful confirmation; consumed once at inauguration."
  },
  "congress": "If no absolute majority, congress event receives saved top two eligible candidates. Ratify plurality confirms stored winner. Alternative majority considers only stored runner-up and requires a real negotiated parliamentary coalition; if absent, the option fails visibly and no president is installed.",
  "inauguration": "Consume confirmed_slot once on 1970-11-03, set native ruling subparty/coalition via existing MD government setter and install period-correct Tomic, Alessandri or Allende. Correct current slot3 Allende routing first. Campaign choices never guarantee victory.",
  "later": "Subsequent ordinary elections use the corrected period-appropriate native pools. Minority PR/PCCh/MAPU/DR/PADENA governments require an actual later election or coalition transition, not a focus reward."
}

The historical calendar must run independently of whether the opening focus is taken. Its completion may show the campaign event only while the campaign remains open and its one-time receipt is unset. A late completion never reopens1970 or replaces a sitting president. All internal date/scenario/receipt checks stay hidden in game tooltips.

## Historical and alternate-history boundaries

- MIR: Extra-parliamentary movement in actual history. A governing MIR programme is explicitly counterfactual, requires actual rule, and grants no automatic revolution.
- Gremialismo: University movement founded1967; regime influence after1973, UDI movement1983, legal party1988-89. A 1970 governing Gremialist party is counterfactual. Do not reuse the name as a synonym for PN.
- civilian_right: PN1970 programme may continue if civilian rule survives. After the historical dictatorship, RN/UDI successor formations require an explicit period-correct transition; a restored PN is counterfactual.
- policy_dates: Mapuche law1972, Chicago stabilization1975, pension reform1980-81, Cartagena withdrawal1976 and plebiscite1988 are source precedents. Earlier equivalent policies require the stated institutional and political conditions and are alternate history, not a claim those laws existed at the start.

Historic dates establish the precedent. Except the actual1970 constitutional ballot and historical1976 membership review, earlier equivalent policy choices can represent explicit alternate history under the required institutions; they do not pretend later statutes existed inJanuary1970. The credible continuation plebiscite is distinct from the contested1980 constitutional vote. A different negotiated timetable is alternate history.

## Reciprocal agreement terms

Every offer originates in a separate Chilean national focus. The named RP recipient receives real Accept and Decline decisions. No spirit, fee, research or building is granted on proposal. Native focus tooltips must show these complete If they accept terms while locked, pending or suspended, using display-only effect blocks. All standing agreements have no expiry. Pending offers expire after90 days without payment, and can be resubmitted after180 days if unratified. Accepted records cannot be purchased twice.

Suspension checks both directions: existence, war with the partner, native embargo and all four Imperia sanction classes (diplomatic,financial,economic,military). Both spirits and their weekly flows suspend/restore together. The five-country protocol checks every participant pair and all memberships. No setup payment, research bonus or asset repeats on restoration. Recipient government changes do not nullify an already ratified treaty.

### Copper Compensation and Engineering

Offer a compensation settlement and technical partnership for the copper industry.

Frei negotiated copper ownership; exact reciprocal contract is alternate-history RP terms.

**Chile**

- Setup: $4.000billion. Weekly: $0.00200billion.
- Add Copper Compensation and Engineering: Chile: Production Efficiency Cap: +6%; Resource Export Revenue: +7%; Foreign Influence Defense: -4%
- 1 x 25% research bonus: CAT_industry.

**United States**

- Setup: $1.000billion. Weekly: $0.00100billion.
- Add Copper Compensation and Engineering: United States: Corporate Tax Revenue: +1.5%; Trade Opinion: +2%; Bureaucracy Expenditure: +1%

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Soviet Machinery and Technical Credit

Propose machinery deliveries and technical training backed by reciprocal commitments.

Allende visited Moscow in 1972; Soviet supplier credit existed, exact project and price are proposed.

**Chile**

- Setup: $2.000billion. Weekly: $0.00300billion.
- Add Soviet Machinery and Technical Credit: Chile: Factory Output: +6%; Production Efficiency Cap: +5%; Foreign Influence Defense: -4%
- State468: +1shared slots, then +1 industrial_complex.

**Soviet Union**

- Setup: $3.000billion. Weekly: $0.00100billion.
- Add Soviet Machinery and Technical Credit: Soviet Union: Resource Export Revenue: +2%; Foreign Influence: +3%; Bureaucracy Expenditure: +1%

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Pacific Copper Supply and Port Equipment

Offer long-term copper sales in exchange for port equipment and industrial cooperation.

Japan was a diversification partner; this named contract is plausible alternate history.

**Chile**

- Setup: $3.000billion. Weekly: $0.00150billion.
- Add Pacific Copper Supply and Port Equipment: Chile: Resource Export Revenue: +8%; Trade Opinion: +4%; Corporate Tax Revenue: -2%
- State949: +1shared slots, then +1 infrastructure.

**Japan**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Pacific Copper Supply and Port Equipment: Japan: Factory Output: +2%; Trade Opinion: +3%; Bureaucracy Expenditure: +1%

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Chilean-Cuban Public Health Exchange

Offer a reciprocal programme of medical training, public health and clinical exchange.

Castro visited Chile in 1971; this specific exchange and reciprocal costs are proposed.

**Chile**

- Setup: $1.000billion. Weekly: $0.00100billion.
- Add Chilean-Cuban Public Health Exchange: Chile: Research Speed: +2%; Health Expenditure: +3%; Trade Opinion: -2%

**Cuba**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Chilean-Cuban Public Health Exchange: Cuba: Research Speed: +1%; Foreign Influence: +3%; Health Expenditure: +3%

Requirements: Diplomatic relations with Cuba. Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Beagle Peace and Maritime Cooperation

Offer a mutually ratified settlement, maritime confidence measures and border cooperation.

1979 papal mediation and the 1984 Treaty of Peace and Friendship; exact economic terms are proposed.

**Chile**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Beagle Peace and Maritime Cooperation: Chile: Stability: +3%; Supply Consumption: -4%; Trade Opinion: +4%; Bureaucracy Expenditure: +2%

**Argentina**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Beagle Peace and Maritime Cooperation: Argentina: Stability: +3%; Supply Consumption: -4%; Trade Opinion: +4%; Bureaucracy Expenditure: +2%

Requirements: Both governments accept the negotiated maritime settlement. Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Peruvian-Chilean Maritime Confidence Measures

Offer incident prevention, port contacts and transparent notification of exercises.

Regional tensions and Andean cooperation are historical; this bilateral protocol is alternate history.

**Chile**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Peruvian-Chilean Maritime Confidence Measures: Chile: Supply Consumption: -3%; Trade Opinion: +5%; Bureaucracy Expenditure: +2%

**Peru**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Peruvian-Chilean Maritime Confidence Measures: Peru: Supply Consumption: -3%; Trade Opinion: +5%; Bureaucracy Expenditure: +2%

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Bolivian-Chilean Transit Facilities

Offer improved bonded transit and commercial handling through Chilean ports.

1904 transit treaty and later negotiations are historical; no sovereignty transfer or corridor is assumed.

**Chile**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Bolivian-Chilean Transit Facilities: Chile: Resource Export Revenue: +4%; Trade Opinion: +4%; Bureaucracy Expenditure: +3%
- State950: +1shared slots, then +1 infrastructure.

**Bolivia**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Bolivian-Chilean Transit Facilities: Bolivia: Trade Opinion: +6%; Supply Consumption: -4%; Bureaucracy Expenditure: +2%

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### French-Chilean Technical Cooperation

Offer university, engineering and industrial technical cooperation.

European diversification is documented; this specific bilateral programme is alternate history.

**Chile**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add French-Chilean Technical Cooperation: Chile: Research Speed: +2.5%; Production Efficiency Cap: +4%; Education Expenditure: +3%
- 1 x 25% research bonus: CAT_industry.

**France**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add French-Chilean Technical Cooperation: France: Resource Export Revenue: +1.5%; Trade Opinion: +3%; Education Expenditure: +2%
- 1 x 15% research bonus: CAT_industry.

Requirements: Both countries exist. Both countries have ratified the agreement. The two countries are at peace with one another. Neither country imposes a native embargo or diplomatic, financial, economic or military Imperia sanctions on the other.

### Andean Industrial Protocol

A jointly ratified industrial and technical cooperation protocol among participating Cartagena states.

1969 Cartagena Agreement; exact project, costs and national rewards are RP proposals.

**Chile**

- Setup: $2.000billion. Weekly: $0.00100billion.
- Add Andean Industrial Protocol: Chile: Production Efficiency Cap: +4%; Trade Opinion: +3%; Bureaucracy Expenditure: +2%

**Bolivia**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Andean Industrial Protocol: Bolivia: Production Efficiency Cap: +2.5%; Trade Opinion: +3%; Bureaucracy Expenditure: +2%

**Colombia**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Andean Industrial Protocol: Colombia: Production Efficiency Cap: +2.5%; Trade Opinion: +3%; Bureaucracy Expenditure: +2%

**Ecuador**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Andean Industrial Protocol: Ecuador: Production Efficiency Cap: +2.5%; Trade Opinion: +3%; Bureaucracy Expenditure: +2%

**Peru**

- Setup: $1.000billion. Weekly: $0.00050billion.
- Add Andean Industrial Protocol: Peru: Production Efficiency Cap: +2.5%; Trade Opinion: +3%; Bureaucracy Expenditure: +2%

Requirements: Active Cartagena Agreement Participant spirit in every participant. All five countries exist and ratify independently. Every pair remains at peace and free of directed embargoes and all four Imperia sanction classes. All participants retain actual Cartagena membership.

## Conditional liabilities and national remedies

### Repression, Exile and Broken Institutions

Arbitrary detention, torture, disappearances and exile damage Chilean society and public institutions.

- Stability: -12%; Research Speed: -5%; Trade Opinion: -10%; Police Expenditure: +8%

Actual repression event or security-state decree; never applied at the January 1970 start.
Civilian restoration, independent investigation and funded reparations; repeal does not undo one-time human losses.

### Banking and External Debt Crisis

External indebtedness and fragile banks transmit a financial shock through the economy.

- Construction Speed: -12%; Factory Output: -8%; Interest Rate: +1.5 pp; Stability: -6%

Credit-risk crisis event after fragile financial policy and an external shock, not every government automatically in 1982.
Chosen intervention or creditor-loss programme replaces this crisis with a 365-day restructuring burden.

### Financial Restructuring

Credit is recovering, but the costs of bank restructuring continue.

- Construction Speed: -4%; Interest Rate: +0.5 pp; Stability: -2%

Replacement for an active banking crisis when the selected rescue completes.
365 days; no repeat crisis replacement payout.

### An Unfinished Reckoning

Reparations have begun, but negotiated limits leave accountability incomplete.

- Stability: -4%; Trade Opinion: -3%; Police Expenditure: +3%

Truth commission negotiated-limits option.
Later judicial settlement requires a separately funded decision; no repeat reparations payment.

### The Legacy of Repression

Civilian rights have been restored. Families, exiles and damaged institutions still bear lasting losses.

- Stability: -2%; Research Speed: -1%; Health Expenditure: +2%

Any documented repression period leaves this legacy after active repression ends.
No focus erases the human losses. Reparations remain a funded national obligation.

### Conduct Banking Stress Tests

Requirements: External Debt Review or Prudential Bank Rules completed. No active banking crisis.
Cost: $1.000billion; weekly $0.00000billion.
Bureaucracy Expenditure: +2%; Interest Rate: -0.25 pp
Create the funded stress-test programme for365 days; prevent a first fragile-bank event only while this programme is active. Does not cancel a crisis already active.

### Authorize Emergency Bank Restructuring

Requirements: Civilian government. Banking and External Debt Crisis is active.
Cost: $6.000billion; weekly $0.00300billion.
Construction Speed: +8%; Interest Rate: +0.5 pp; Tax Revenue: -3%
Replace active Banking and External Debt Crisis with Financial Restructuring for365 days. One restructuring receipt. These national crisis remedies remain reachable after a party change, including loss of military rule. No focus completion or building payout is replayed.

### Restructure Banks through Creditor Losses

Requirements: Civilian government. Banking and External Debt Crisis is active.
Cost: $2.000billion; weekly $0.00000billion.
Interest Rate: -0.5 pp; Construction Speed: -6%; Stability: -5%
Replace active Banking and External Debt Crisis with Financial Restructuring for365 days. Mutually exclusive with the funded public intervention for this crisis episode.

### Complete the Judicial Settlement

Requirements: Civilian government. An Unfinished Reckoning is active.
Cost: $2.000billion; weekly $0.00000billion.
None
Remove An Unfinished Reckoning. Preserve The Legacy of Repression and existing national reparations. No repeat reparations setup fee, no second weekly reparations obligation.

## Events

### The Presidential Succession of 1970

Chile faces a contested succession. The presidency requires a constitutional result and recognition by Congress.

Design trigger: Campaign opens in the historical 1970 election calendar; September vote and October congressional ratification read the actual election result.

- **Support Radomiro Tomic**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: +2%.
  party_support: {'party': 1, 'amount': 0.03}
  candidate: Radomiro Tomic
- **Support Salvador Allende**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: +2%.
  party_support: {'party': 18, 'amount': 0.03}
  candidate: Salvador Allende
- **Support Jorge Alessandri**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: +2%.
  party_support: {'party': 2, 'amount': 0.03}
  candidate: Jorge Alessandri

### Congress and the Electoral Plurality

Congress must confirm a lawful president. Constitutional guarantees may secure the decisive votes.

Design trigger: No candidate wins an absolute majority in the 1970 election.

- **Ratify the lawful plurality with guarantees**: setup $0.000billion; weekly $0.00000billion. Stability: +4%; Political Power Gain: -4%.
  result: Install the actual confirmed candidate through the corrected native leader system.
- **Seek an alternative constitutional majority**: setup $0.000billion; weekly $0.00000billion. Stability: -4%; Political Power Gain: +4%.
  result: Congress considers only constitutionally eligible candidates; failure opens a constitutional crisis, not an automatic coup.

### Compensation after Nationalization

Public ownership is settled. The government must decide how to resolve compensation claims.

Design trigger: Full Copper Nationalization completes.

- **Negotiate a compensation settlement**: setup $3.000billion; weekly $0.00000billion. Trade Opinion: +6%; Interest Rate: -0.25 pp.
- **Contest the claims through sovereign law**: setup $0.000billion; weekly $0.00000billion. Foreign Influence Defense: +6%; Trade Opinion: -8%; Interest Rate: +0.5 pp.

### A National Transport Stoppage

A transport stoppage disrupts supply. Workers, firms and the government demand a response.

Design trigger: A conditional logistics crisis under high political confrontation; historical reference October 1972.

- **Negotiate a funded transport compact**: setup $1.000billion; weekly $0.00000billion. Stability: +3%; Corporate Tax Revenue: -2% (180days).
- **Organize emergency public distribution**: setup $2.000billion; weekly $0.00100billion. Supply Consumption: -4%; Bureaucracy Expenditure: +6% (180days).
- **Confront the stoppage through emergency powers**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: +8%; Stability: -7%; Police Expenditure: +6% (180days).

### The Constitutional Crisis

Civilian and military authorities face a choice between negotiated guarantees and a violent rupture.

Design trigger: High confrontation, failed civilian settlement and a real military intervention condition. Historical reference 1973.

- **Conclude an enforceable constitutional accord**: setup $1.000billion; weekly $0.00000billion. Stability: +5%; Political Power Gain: -8%.
  result: Retain civilian succession if parliamentary and military participants accept.
- **Permit the service chiefs to seize government**: setup $0.000billion; weekly $0.00000billion. Stability: -10%; Research Speed: -3%.
  add_spirit: COLDWAR_CHL_repression
  result: Actual military transfer activates the military branch. Pinochet is not automatically commander in January 1970; the later junta leadership event selects the actual leader.

### The Presidency of the Junta

The historical junta was chaired by Pinochet from September 1973. Formal executive concentration followed in June and December 1974. An earlier collective constitutionalist government is an alternate outcome.

Design trigger: A military government actually exists after a coup. Historical Pinochet command is a later outcome.

- **Retain collective military authority**: setup $0.000billion; weekly $0.00000billion. Division Organization: +3%; Political Power Gain: -4%.
  result: Preserve the actual constitutionalist or collective leader; early exit remains possible.
- **Concentrate the presidency under Pinochet**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: +10%; Stability: -6%.
  result: Install Augusto Pinochet through the corrected slot22 leader route. Requires his actual availability and officer backing; does not create him in January1970.

### Emergency Security Decrees

The security apparatus seeks wider powers of detention and political suppression.

Design trigger: An actual coercive security decree or the National Security State focus.

- **Authorize the coercive decrees**: setup $0.000billion; weekly $0.00000billion. None.
  add_spirit: COLDWAR_CHL_repression
  result: Add Repression, Exile and Broken Institutions.
- **Require civilian legal safeguards**: setup $0.000billion; weekly $0.00000billion. Political Power Gain: -8%; Police Expenditure: +3%.
  result: Reject exceptional coercive powers and preserve judicial review.

### The Social Cost of Adjustment

The pace of economic adjustment has become a dispute within the government and society.

Design trigger: The Chicago Programme completes.

- **Maintain the rapid programme**: setup $0.000billion; weekly $0.00000billion. Construction Speed: +4%; Stability: -6%; Social Expenditure: -3% (365days).
- **Fund a staged adjustment**: setup $2.000billion; weekly $0.00200billion. Stability: +4%; Social Expenditure: +5% (365days).

### External Credit and the Banks

Foreign financing tightens and weak balance sheets threaten lending and production.

Design trigger: A fragile domestic banking system meets an external credit shock. The event is evaluated independently of focus completion. 1982-83 supplies the historical precedent.

- **Declare the crisis and prepare restructuring**: setup $0.000billion; weekly $0.00000billion. None.
  add_spirit: COLDWAR_CHL_bank_crisis
  result: Unlock Public Bank Intervention and Impose Creditor Losses.
- **Enforce supervision before failures spread**: setup $2.000billion; weekly $0.00000billion. Corporate Tax Revenue: -4%; Bureaucracy Expenditure: +4%; Interest Rate: -0.25 pp.
  require: Prudential Bank Supervision already completed.
  result: Prevention is available only before systemic bank failure; it cannot erase an active crisis.

### An Early Civilian Transfer

Military and civilian negotiators agree the terms of a return to competitive government.

Design trigger: Guarantee a Civilian Ballot completes under constitutionalist military leadership.

- **Schedule and enforce the civilian election**: setup $1.000billion; weekly $0.00000billion. Stability: +5%; Military Personnel Expenditure: +3%.
  result: Restore native elections. Government follows the actual result; military programme deactivates on handover.
- **Delay until the guarantees are ratified**: setup $0.000billion; weekly $0.00000billion. Stability: -3%; Political Power Gain: +3% (180days).
  result: A new ratification deadline is set; no permanent military bonus.

### The Continuation Plebiscite

The electorate decides whether military rule may continue under the proposed constitutional terms.

Design trigger: An Enforceable Plebiscite completes and the agreed vote is conducted; 1988 is the historical precedent.

- **Respect a No majority**: setup $0.000billion; weekly $0.00000billion. Stability: +5%; Political Power Gain: -5%.
  require: No won the actual vote.
  result: Unlock negotiated handover and competitive civilian elections.
- **Respect a Yes majority**: setup $0.000billion; weekly $0.00000billion. Stability: +2%; Political Power Gain: +3%.
  require: Yes won the actual vote.
  result: A counterfactual continuation retains authoritarian liabilities and the need for future constitutional consent.

### The Civilian Inauguration

A civilian president takes office under a negotiated constitutional settlement.

Design trigger: Negotiated handover and actual civilian election result. Historical reference March 1990.

- **Transfer the presidency to the elected coalition**: setup $0.000billion; weekly $0.00000billion. Stability: +5%.
  result: Install the actual winning civilian candidate, including Aylwin for an appropriate PDC coalition. Suspend the military programme without replaying assets.

### Truth, Justice and Reparations

The commission presents its findings. Civilian authorities must choose how to fund remedies and pursue accountability.

Design trigger: A National Truth Commission completes after a documented repression period.

- **Fund reparations and independent prosecutions**: setup $3.000billion; weekly $0.00100billion. Stability: +4%; Police Expenditure: +4%.
  add_spirit: COLDWAR_CHL_lasting_legacy
  remove_spirit: COLDWAR_CHL_repression
  weekly_lifetime: Standing national reparations, survives party changes; budgeted weekly, no expiry.
- **Fund reparations under negotiated limits**: setup $2.000billion; weekly $0.00100billion. Stability: +2%; Military Personnel Expenditure: +4%.
  add_spirit: COLDWAR_CHL_lasting_legacy
  replace_spirit: {'old': 'COLDWAR_CHL_repression', 'new': 'COLDWAR_CHL_limited_accountability'}
  weekly_lifetime: Standing national reparations, survives party changes; budgeted weekly, no expiry.

### Chile and the Cartagena Commitments

The government must decide whether regional industrial rules remain compatible with its national programme.

Design trigger: 1976 membership review, or completion of a Chilean trade-policy review under a different historical timetable.

- **Remain within the ratified framework**: setup $0.000billion; weekly $0.00000billion. Production Efficiency Cap: +2%; Trade Opinion: -2%.
  result: Retain actual membership and the agreed obligations. Continued membership after 1976 is a counterfactual policy choice.
- **Withdraw under the treaty procedure**: setup $0.000billion; weekly $0.00000billion. Construction Speed: +3%; Trade Opinion: +2%.
  remove_spirit: COLDWAR_CHL_cartagena_member
  result: Suspend every dependent member programme and the five-country industrial protocol. One-time assets remain; no fees or construction repeat.

## Exact focus catalogue

### The Republic and its Institutions

#### Constitutional Mandate

`COLDWAR_CHL_constitutional_mandate`. Absolute(8,0), anchor`none`, local(8,0), cost2 = 14days. Lifetime: national.

Fund Congress and the electoral administration to uphold a contested presidential succession.

- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +6%; Bureaucracy Expenditure: +2%
- event: election

#### The Schneider Doctrine

`COLDWAR_CHL_schneider_doctrine`. Absolute(4,1), anchor`COLDWAR_CHL_constitutional_mandate`, local(-4,1), cost5 = 35days. Lifetime: national.

Affirm military subordination to the lawful civilian government and address professional grievances.

Requires: (Constitutional Mandate).
- Setup: $0.000billion; weekly: $0.00000billion.
- Foreign Influence Defense: +8%; Military Personnel Expenditure: +3%

#### Congressional Guarantees

`COLDWAR_CHL_congressional_guarantees`. Absolute(8,1), anchor`COLDWAR_CHL_constitutional_mandate`, local(0,1), cost5 = 35days. Lifetime: national.

Bind the executive to negotiated guarantees for Congress, courts and political organization.

Requires: (Constitutional Mandate).
- Setup: $0.000billion; weekly: $0.00000billion.
- Stability: +5%; Political Power Gain: -4%

#### Electoral Independence

`COLDWAR_CHL_electoral_rolls`. Absolute(12,1), anchor`COLDWAR_CHL_constitutional_mandate`, local(4,1), cost5 = 35days. Lifetime: national.

Protect registration and scrutiny from intervention by whichever party governs.

Requires: (Constitutional Mandate).
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +3%; Bureaucracy Expenditure: +3%

#### A Cross-Party Accord

`COLDWAR_CHL_cross_party_accord`. Absolute(6,2), anchor`COLDWAR_CHL_constitutional_mandate`, local(-2,2), cost5 = 35days. Lifetime: national.

Negotiate a common constitutional floor without requiring agreement on ownership or social policy.

Requires: (The Schneider Doctrine) AND (Congressional Guarantees).
Excludes: Presidential Initiative.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +8%; Stability: +3%
- Remove A Republic under Strain.

#### Presidential Initiative

`COLDWAR_CHL_presidential_initiative`. Absolute(10,2), anchor`COLDWAR_CHL_constitutional_mandate`, local(2,2), cost5 = 35days. Lifetime: national.

Secure a wider executive legislative mandate, accepting stronger opposition to concentrated authority.

Requires: (Congressional Guarantees) AND (Electoral Independence).
Excludes: A Cross-Party Accord.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +14%; Stability: -3%

#### Professional Civil Service

`COLDWAR_CHL_civil_service`. Absolute(8,3), anchor`COLDWAR_CHL_constitutional_mandate`, local(0,3), cost5 = 35days. Lifetime: national.

Replace patronage appointments with professional examinations and protected technical careers.

Requires: (A Cross-Party Accord OR Presidential Initiative).
- Setup: $2.000billion; weekly: $0.00000billion.
- Bureaucracy Expenditure: -6%; Research Speed: +2%

#### Neighbourhood Services

`COLDWAR_CHL_housing_services`. Absolute(4,4), anchor`COLDWAR_CHL_constitutional_mandate`, local(-4,4), cost5 = 35days. Lifetime: national.

Extend water, clinics and public services through municipal and neighbourhood institutions.

Requires: (Professional Civil Service).
- Setup: $2.000billion; weekly: $0.00000billion.
- Stability: +5%; Social Expenditure: +5%

#### Mapuche Land Rights

`COLDWAR_CHL_mapuche_titles`. Absolute(8,4), anchor`COLDWAR_CHL_constitutional_mandate`, local(0,4), cost5 = 35days. Lifetime: national.

Prepare recognition of indigenous community claims and fund legal settlement of disputed titles. The 1972 indigenous law supplies the historical legislative precedent.

Requires: (Professional Civil Service).
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +4%; Agriculture Productivity: -2%; Bureaucracy Expenditure: +3%

#### Independent Courts

`COLDWAR_CHL_judicial_review`. Absolute(12,4), anchor`COLDWAR_CHL_constitutional_mandate`, local(4,4), cost5 = 35days. Lifetime: national.

Give courts the resources to enforce lawful procedure against both executive and private abuses.

Requires: (Professional Civil Service).
- Setup: $1.000billion; weekly: $0.00000billion.
- Foreign Influence Defense: +6%; Political Power Gain: -3%

#### A Truth Commission

`COLDWAR_CHL_commission_truth`. Absolute(6,5), anchor`COLDWAR_CHL_constitutional_mandate`, local(-2,5), cost5 = 35days. Lifetime: national.

Document disappearances and repression and provide remedies for victims as civilian institutions recover.

Requires: (Neighbourhood Services) AND (Mapuche Land Rights).
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Police Expenditure: +3%
- event: truth

#### A Civilian Compact

`COLDWAR_CHL_civilian_compact`. Absolute(10,5), anchor`COLDWAR_CHL_constitutional_mandate`, local(2,5), cost5 = 35days. Lifetime: national.

Secure reciprocal commitments to civilian succession and peaceful opposition.

Requires: (Independent Courts) AND (Mapuche Land Rights).
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +6%; Stability: +3%

### Copper, Credit and National Development

#### CORFO Investment Plan

`COLDWAR_CHL_corfo_plan`. Absolute(26,0), anchor`none`, local(26,0), cost3 = 21days. Lifetime: national.

Audit public enterprises and direct scarce investment toward export capacity, food and transport.

- Setup: $0.000billion; weekly: $0.00000billion.
- Construction Speed: +4%; Bureaucracy Expenditure: +2%

#### A Copper Settlement

`COLDWAR_CHL_negotiated_copper`. Absolute(22,1), anchor`COLDWAR_CHL_corfo_plan`, local(-4,1), cost5 = 35days. Lifetime: national.

Settle compensation and retain supplier cooperation while consolidating Chilean public participation.

Requires: (CORFO Investment Plan).
Excludes: Nationalize Copper, Regulated Concessions.
- Setup: $4.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +10%; Trade Opinion: +6%; Corporate Tax Revenue: -2%

#### Nationalize Copper

`COLDWAR_CHL_national_copper`. Absolute(26,1), anchor`COLDWAR_CHL_corfo_plan`, local(0,1), cost5 = 35days. Lifetime: national.

Bring large-scale copper into public ownership while accepting management and compensation disputes.

Requires: (CORFO Investment Plan).
Excludes: A Copper Settlement, Regulated Concessions.
- Setup: $2.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +16%; Research Speed: -3%; Trade Opinion: -8%
- event: copper

#### Regulated Concessions

`COLDWAR_CHL_concession_copper`. Absolute(30,1), anchor`COLDWAR_CHL_corfo_plan`, local(4,1), cost5 = 35days. Lifetime: national.

Attract private capital under royalty and reinvestment rules, trading some autonomy for new investment.

Requires: (CORFO Investment Plan).
Excludes: A Copper Settlement, Nationalize Copper.
- Setup: $1.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +8%; Construction Speed: +6%; Foreign Influence Defense: -6%

#### Train Mine Engineers

`COLDWAR_CHL_mine_engineers`. Absolute(26,2), anchor`COLDWAR_CHL_corfo_plan`, local(0,2), cost5 = 35days. Lifetime: national.

Expand mining engineering, maintenance and technical training so ownership reform can sustain production.

Requires: (A Copper Settlement OR Nationalize Copper OR Regulated Concessions).
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +3%; Education Expenditure: +4%
- Remove Uneven Technical Education.
- 1 x 25% research bonus: CAT_industry.

#### Copper Stabilization Fund

`COLDWAR_CHL_copper_stabilization`. Absolute(24,3), anchor`COLDWAR_CHL_corfo_plan`, local(-2,3), cost5 = 35days. Lifetime: national.

Reserve part of export receipts against downturns instead of committing every windfall to current spending.

Requires: (Train Mine Engineers).
Excludes: Reinvest Export Earnings.
- Setup: $3.000billion; weekly: $0.00000billion.
- Resource Export Revenue: -4%; Interest Rate: -0.75 pp; Stability: +2%

#### Reinvest Export Earnings

`COLDWAR_CHL_export_reinvestment`. Absolute(28,3), anchor`COLDWAR_CHL_corfo_plan`, local(2,3), cost5 = 35days. Lifetime: national.

Commit more export receipts immediately to production, accepting greater exposure to the next downturn.

Requires: (Train Mine Engineers).
Excludes: Copper Stabilization Fund.
- Setup: $3.000billion; weekly: $0.00000billion.
- Construction Speed: +8%; Interest Rate: +0.5 pp
- State472: +1 shared slots, then +1 industrial_complex.

#### Agricultural Extension

`COLDWAR_CHL_rural_extension`. Absolute(18,1), anchor`COLDWAR_CHL_corfo_plan`, local(-8,1), cost5 = 35days. Lifetime: national.

Send agronomists, credit officers and irrigation technicians to the reformed countryside.

Requires: (CORFO Investment Plan).
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +6%; Education Expenditure: +2%

#### Secure Cooperative Titles

`COLDWAR_CHL_cooperative_titles`. Absolute(18,3), anchor`COLDWAR_CHL_corfo_plan`, local(-8,3), cost5 = 35days. Lifetime: national.

Secure cooperative holdings and provide common machinery and working capital.

Requires: (Agricultural Extension).
Excludes: Secure Family Holdings.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +7%; Social Expenditure: +3%; Stability: +4%
- Remove Unfinished Agrarian Reform.

#### Secure Family Holdings

`COLDWAR_CHL_family_farms`. Absolute(22,3), anchor`COLDWAR_CHL_corfo_plan`, local(-4,3), cost5 = 35days. Lifetime: national.

Give individual farmers secure holdings, with extension services and enforceable credit obligations.

Requires: (Agricultural Extension).
Excludes: Secure Cooperative Titles.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +10%; Tax Revenue: -2%
- Remove Unfinished Agrarian Reform.

#### Rural Storage Networks

`COLDWAR_CHL_cold_chain`. Absolute(20,4), anchor`COLDWAR_CHL_corfo_plan`, local(-6,4), cost5 = 35days. Lifetime: national.

Reduce losses between farms, cities and export ports.

Requires: (Secure Cooperative Titles OR Secure Family Holdings).
- Setup: $3.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +5%; Supply Consumption: -3%
- State463: +1 shared slots, then +1 agriculture_district.

#### A Wage and Price Pact

`COLDWAR_CHL_price_compact`. Absolute(32,1), anchor`COLDWAR_CHL_corfo_plan`, local(6,1), cost5 = 35days. Lifetime: national.

Negotiate a stabilization pact among employers, unions and the government.

Requires: (CORFO Investment Plan).
Excludes: Monetary Restraint.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +4%; Corporate Tax Revenue: -3%; Political Power Gain: -3%
- Remove Inflationary Expectations.

#### Monetary Restraint

`COLDWAR_CHL_monetary_restraint`. Absolute(36,1), anchor`COLDWAR_CHL_corfo_plan`, local(10,1), cost5 = 35days. Lifetime: national.

Constrain monetary financing and public demand to restore credit confidence.

Requires: (CORFO Investment Plan).
Excludes: A Wage and Price Pact.
- Setup: $1.000billion; weekly: $0.00000billion.
- Interest Rate: -0.75 pp; Construction Speed: -3%; Stability: -3%
- Remove Inflationary Expectations.

#### Prudential Bank Rules

`COLDWAR_CHL_prudential_banks`. Absolute(32,3), anchor`COLDWAR_CHL_corfo_plan`, local(6,3), cost5 = 35days. Lifetime: national.

Limit connected lending and foreign-currency exposure before a credit boom becomes a public liability.

Requires: (A Wage and Price Pact OR Monetary Restraint).
- Setup: $1.000billion; weekly: $0.00000billion.
- Interest Rate: -0.25 pp; Corporate Tax Revenue: -2%; Bureaucracy Expenditure: +2%

#### The Central Corridor

`COLDWAR_CHL_central_corridor`. Absolute(26,4), anchor`COLDWAR_CHL_corfo_plan`, local(0,4), cost5 = 35days. Lifetime: national.

Improve the central rail and road corridor linking production to ports.

Requires: (Copper Stabilization Fund OR Reinvest Export Earnings).
- Setup: $3.000billion; weekly: $0.00000billion.
- Infrastructure Construction Speed: +8%; Supply Consumption: -3%
- Remove A Long and Uneven Republic.
- State468: +1 shared slots, then +1 infrastructure.

#### Huachipato Suppliers

`COLDWAR_CHL_huachipato`. Absolute(24,5), anchor`COLDWAR_CHL_corfo_plan`, local(-2,5), cost5 = 35days. Lifetime: national.

Develop steelworking suppliers around existing industrial centers.

Requires: (The Central Corridor).
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +5%; Production Efficiency Cap: +4%
- State463: +1 shared slots, then +1 industrial_complex.

#### ENDESA Grid Investment

`COLDWAR_CHL_endesas_grid`. Absolute(28,5), anchor`COLDWAR_CHL_corfo_plan`, local(2,5), cost5 = 35days. Lifetime: national.

Expand electricity supply for urban and industrial development.

Requires: (The Central Corridor).
- Setup: $3.000billion; weekly: $0.00200billion.
- Construction Speed: +4%; Infrastructure Construction Speed: +4%
- State468: +1 shared slots, then +1 fossil_powerplant.

#### Pacific Export Terminals

`COLDWAR_CHL_pacific_ports`. Absolute(32,4), anchor`COLDWAR_CHL_corfo_plan`, local(6,4), cost5 = 35days. Lifetime: national.

Improve port handling and shipping reliability for a wider range of exports.

Requires: (Prudential Bank Rules).
- Setup: $3.000billion; weekly: $0.00100billion.
- Resource Export Revenue: +6%; Trade Opinion: +3%
- State949: +1 shared slots, then +1 infrastructure.

#### Forestry and Fruit Exports

`COLDWAR_CHL_forestry_exports`. Absolute(30,5), anchor`COLDWAR_CHL_corfo_plan`, local(4,5), cost5 = 35days. Lifetime: national.

Diversify exports with tax-supported incentives, inspection and rural infrastructure.

Requires: (Pacific Export Terminals).
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +6%; Resource Export Revenue: +3%; Tax Revenue: -2%
- State463: +1 shared slots, then +1 agriculture_district.

#### Technical Universities

`COLDWAR_CHL_technical_universities`. Absolute(26,6), anchor`COLDWAR_CHL_corfo_plan`, local(0,6), cost5 = 35days. Lifetime: national.

Connect regional technical institutes, public universities and industrial apprenticeships.

Requires: (Huachipato Suppliers) AND (ENDESA Grid Investment).
- Setup: $3.000billion; weekly: $0.00000billion.
- Research Speed: +3%; Education Expenditure: +4%
- 1 x 30% research bonus: CAT_computing.

### The Armed Forces of a Pacific Republic

#### Service Readiness Review

`COLDWAR_CHL_professional_review`. Absolute(48,0), anchor`none`, local(48,0), cost3 = 21days. Lifetime: national.

Assess readiness across the three services without predetermining their political role.

- Setup: $0.000billion; weekly: $0.00000billion.
- Division Organization: +3%; Military Personnel Expenditure: +3%

#### Andean Territorial Defense

`COLDWAR_CHL_andean_defence`. Absolute(44,1), anchor`COLDWAR_CHL_professional_review`, local(-4,1), cost5 = 35days. Lifetime: national.

Prioritize prepared mountain positions and reliable local supply over rapid offensive movement.

Requires: (Service Readiness Review).
Excludes: A Mobile Reserve.
- Setup: $2.000billion; weekly: $0.00000billion.
- Division Defense on Core Territory: +10%; Supply Consumption: -6%; Division Speed: -3%

#### A Mobile Reserve

`COLDWAR_CHL_mobile_reserve`. Absolute(48,1), anchor`COLDWAR_CHL_professional_review`, local(0,1), cost5 = 35days. Lifetime: national.

Build a mobile reserve able to reinforce distant fronts, accepting a larger logistical burden.

Requires: (Service Readiness Review).
Excludes: Andean Territorial Defense.
- Setup: $3.000billion; weekly: $0.00000billion.
- Division Speed: +8%; Division Recovery Rate: +6%; Supply Consumption: +6%

#### Professional Cadres

`COLDWAR_CHL_professional_cadres`. Absolute(44,2), anchor`COLDWAR_CHL_professional_review`, local(-4,2), cost5 = 35days. Lifetime: national.

Retain experienced noncommissioned officers and lengthen unit training.

Requires: (Andean Territorial Defense OR A Mobile Reserve).
Excludes: A Trained Reserve.
- Setup: $2.000billion; weekly: $0.00000billion.
- Division Organization: +6%; Division Training Time: +8%; Military Personnel Expenditure: +5%

#### A Trained Reserve

`COLDWAR_CHL_reserve_training`. Absolute(48,2), anchor`COLDWAR_CHL_professional_review`, local(0,2), cost5 = 35days. Lifetime: national.

Favor a broad reserve able to replenish formations over a smaller professional establishment.

Requires: (Andean Territorial Defense OR A Mobile Reserve).
Excludes: Professional Cadres.
- Setup: $1.000billion; weekly: $0.00000billion.
- Division Recovery Rate: +7%; Division Organization: -2%; Military Personnel Expenditure: +3%

#### FAMAE Workshops

`COLDWAR_CHL_famae`. Absolute(46,3), anchor`COLDWAR_CHL_professional_review`, local(-2,3), cost5 = 35days. Lifetime: national.

Expand repair, ammunition and maintenance capacity around FAMAE.

Requires: (Professional Cadres OR A Trained Reserve).
- Setup: $3.000billion; weekly: $0.00000billion.
- Production Efficiency Growth: +6%; Military Factory Construction Speed: +5%
- State468: +1 shared slots, then +1 arms_factory.

#### Standardized Ammunition

`COLDWAR_CHL_standard_ammunition`. Absolute(46,4), anchor`COLDWAR_CHL_professional_review`, local(-2,4), cost5 = 35days. Lifetime: national.

Concentrate production on fewer ammunition standards and more consistent artillery supply.

Requires: (FAMAE Workshops).
- Setup: $1.000billion; weekly: $0.00000billion.
- Artillery Attack: +6%; Production Efficiency Cap: +4%; Production Efficiency Growth: -3%

#### Coastal Denial Doctrine

`COLDWAR_CHL_coastal_denial`. Absolute(52,1), anchor`COLDWAR_CHL_professional_review`, local(4,1), cost5 = 35days. Lifetime: national.

Protect ports and sea approaches through a concentrated coastal defense posture.

Requires: (Service Readiness Review).
Excludes: Ocean Escort Doctrine.
- Setup: $2.000billion; weekly: $0.00000billion.
- Naval Organization: +8%; Dockyard Output: +4%; Air Mission Efficiency: -2%

#### Ocean Escort Doctrine

`COLDWAR_CHL_ocean_escort`. Absolute(56,1), anchor`COLDWAR_CHL_professional_review`, local(8,1), cost5 = 35days. Lifetime: national.

Invest in sustained escort operations to protect a long maritime trading network.

Requires: (Service Readiness Review).
Excludes: Coastal Denial Doctrine.
- Setup: $3.000billion; weekly: $0.00000billion.
- Naval Organization: +5%; Trade Opinion: +5%; Military Personnel Expenditure: +4%

#### ASMAR Dockyards

`COLDWAR_CHL_asmar`. Absolute(54,2), anchor`COLDWAR_CHL_professional_review`, local(6,2), cost5 = 35days. Lifetime: national.

Expand naval construction and refit capacity at Talcahuano.

Requires: (Coastal Denial Doctrine OR Ocean Escort Doctrine).
- Setup: $3.000billion; weekly: $0.00150billion.
- Dockyard Output: +5%
- State463: +1 shared slots, then +1 dockyard.

#### Naval Training Missions

`COLDWAR_CHL_naval_training`. Absolute(54,3), anchor`COLDWAR_CHL_professional_review`, local(6,3), cost5 = 35days. Lifetime: national.

Improve damage control, engineering and combined fleet exercises.

Requires: (ASMAR Dockyards).
- Setup: $1.000billion; weekly: $0.00000billion.
- Naval Organization: +4%; Military Personnel Expenditure: +2%
- 1 x 25% research bonus: CAT_surface_ships.

#### Airspace Interception

`COLDWAR_CHL_air_interception`. Absolute(42,5), anchor`COLDWAR_CHL_professional_review`, local(-6,5), cost5 = 35days. Lifetime: national.

Improve radar coverage and the readiness of interceptor squadrons.

Requires: (Standardized Ammunition).
Excludes: Tactical Air Cooperation.
- Setup: $2.000billion; weekly: $0.00100billion.
- Interception Detection: +12%; Air Mission Efficiency: +4%
- State472: +1 shared slots, then +1 radar_station.

#### Tactical Air Cooperation

`COLDWAR_CHL_tactical_air`. Absolute(46,5), anchor`COLDWAR_CHL_professional_review`, local(-2,5), cost5 = 35days. Lifetime: national.

Train air crews and ground formations to coordinate reconnaissance and tactical support.

Requires: (Standardized Ammunition).
Excludes: Airspace Interception.
- Setup: $2.000billion; weekly: $0.00000billion.
- Air Mission Efficiency: +8%; Supply Consumption: +3%
- 1 x 25% research bonus: CAT_aircraft.

#### ENAER Foundations

`COLDWAR_CHL_enaer`. Absolute(44,6), anchor`COLDWAR_CHL_professional_review`, local(-4,6), cost5 = 35days. Lifetime: national.

Develop the engineering and maintenance base for a national aeronautical industry.

Requires: (Airspace Interception OR Tactical Air Cooperation).
- Setup: $3.000billion; weekly: $0.00000billion.
- Military Factory Construction Speed: +5%; Research Speed: +1.5%
- 1 x 25% research bonus: CAT_aircraft.

#### A Joint Professional Staff

`COLDWAR_CHL_joint_staff`. Absolute(50,5), anchor`COLDWAR_CHL_professional_review`, local(2,5), cost5 = 35days. Lifetime: national.

Standardize operational planning while keeping service commands accountable to the lawful government.

Requires: (Standardized Ammunition) AND (Naval Training Missions).
- Setup: $1.000billion; weekly: $0.00000billion.
- Division Organization: +4%; Naval Organization: +3%; Bureaucracy Expenditure: +2%

### Christian Democratic Reform

#### Community Development

`COLDWAR_CHL_pdc_social`. Absolute(74,0), anchor`none`, local(74,0), cost5 = 35days. Lifetime: party.

Fund neighbourhood organizations, housing services and local social provision.

Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +4%; Social Expenditure: +3%

#### Consolidate Frei's Reforms

`COLDWAR_CHL_pdc_frei`. Absolute(70,1), anchor`COLDWAR_CHL_pdc_social`, local(-4,1), cost5 = 35days. Lifetime: party.

Consolidate legal land reform and a negotiated mixed economy.

Requires: (Community Development).
Excludes: Tomic's Convergence.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +6%; Stability: +2%; Corporate Tax Revenue: -3%

#### Tomic's Convergence

`COLDWAR_CHL_pdc_tomic`. Absolute(78,1), anchor`COLDWAR_CHL_pdc_social`, local(4,1), cost5 = 35days. Lifetime: party.

Seek a wider reform alliance with the democratic left, accepting business and centrist resistance.

Requires: (Community Development).
Excludes: Consolidate Frei's Reforms.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +9%; Political Power Gain: +6%; Trade Opinion: -4%

#### The Education Reform

`COLDWAR_CHL_pdc_school`. Absolute(70,2), anchor`COLDWAR_CHL_pdc_social`, local(-4,2), cost5 = 35days. Lifetime: party.

Extend secondary and technical education beyond the established urban schools.

Requires: (Consolidate Frei's Reforms).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +3.5%; Education Expenditure: +5%

#### Peasant Cooperatives

`COLDWAR_CHL_pdc_coops`. Absolute(78,2), anchor`COLDWAR_CHL_pdc_social`, local(4,2), cost5 = 35days. Lifetime: party.

Back cooperatives with machinery, credit and trained rural organizers.

Requires: (Tomic's Convergence).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +7%; Social Expenditure: +4%

#### An Independent Center

`COLDWAR_CHL_pdc_centre`. Absolute(68,3), anchor`COLDWAR_CHL_pdc_social`, local(-6,3), cost5 = 35days. Lifetime: party.

Preserve an independent center able to negotiate with either parliamentary bloc.

Requires: (The Education Reform).
Excludes: A Social Partnership.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Foreign Influence Defense: +8%; Political Power Gain: +8%; Stability: -2%

#### A Social Partnership

`COLDWAR_CHL_pdc_business`. Absolute(72,3), anchor`COLDWAR_CHL_pdc_social`, local(-2,3), cost5 = 35days. Lifetime: party.

Trade predictable investment rules for employer support of social provision.

Requires: (The Education Reform).
Excludes: An Independent Center.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +6%; Stability: +3%; Social Expenditure: +3%

#### Christian Trade Unionism

`COLDWAR_CHL_pdc_unions`. Absolute(76,3), anchor`COLDWAR_CHL_pdc_social`, local(2,3), cost5 = 35days. Lifetime: party.

Strengthen autonomous Christian unions within an organized labor movement.

Requires: (Peasant Cooperatives).
Excludes: A Reform Coalition.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +5%; Factory Output: +4%; Corporate Tax Revenue: -3%

#### A Reform Coalition

`COLDWAR_CHL_pdc_left`. Absolute(80,3), anchor`COLDWAR_CHL_pdc_social`, local(6,3), cost5 = 35days. Lifetime: party.

Share policy authority with the democratic left rather than governing through a narrow party machine.

Requires: (Peasant Cooperatives).
Excludes: Christian Trade Unionism.
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +12%; Stability: +3%; Bureaucracy Expenditure: +4%

#### Neighbourhood Services

`COLDWAR_CHL_pdc_housing`. Absolute(74,4), anchor`COLDWAR_CHL_pdc_social`, local(0,4), cost5 = 35days. Lifetime: party.

Link housing settlements to clinics and public services.

Requires: (An Independent Center OR A Social Partnership OR Christian Trade Unionism OR A Reform Coalition).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Stability: +4%; Health Expenditure: +4%

#### Community Enterprises

`COLDWAR_CHL_pdc_enterprise`. Absolute(72,5), anchor`COLDWAR_CHL_pdc_social`, local(-2,5), cost5 = 35days. Lifetime: party.

Finance worker and community enterprises within a plural economy.

Requires: (Neighbourhood Services).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +6%; Production Efficiency Growth: +4%; Bureaucracy Expenditure: +3%
- State468: +1 shared slots, then +1 industrial_complex.

#### Civic Reconciliation

`COLDWAR_CHL_pdc_church`. Absolute(76,5), anchor`COLDWAR_CHL_pdc_social`, local(2,5), cost5 = 35days. Lifetime: party.

Support independent civic mediation across polarized communities.

Requires: (Neighbourhood Services).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +5%; Political Power Gain: -3%

#### A Civilian Coalition

`COLDWAR_CHL_pdc_aylwin`. Absolute(74,6), anchor`COLDWAR_CHL_pdc_social`, local(0,6), cost5 = 35days. Lifetime: party.

Build a governing coalition committed to peaceful succession and enforceable civil rights.

Requires: (Community Enterprises) AND (Civic Reconciliation).
Native availability and reward guard: `western_conservatism_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Stability: +5%; Foreign Influence Defense: +5%; Social Expenditure: +2%

### National Party and Civilian Conservatism

#### Investment Guarantees

`COLDWAR_CHL_pn_investment`. Absolute(90,0), anchor`none`, local(90,0), cost5 = 35days. Lifetime: party.

Give private investment predictable rules while retaining parliamentary government.

Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Construction Speed: +6%; Corporate Tax Revenue: +3%; Stability: -2%

#### Alessandri's Republic

`COLDWAR_CHL_pn_alessandri`. Absolute(86,1), anchor`COLDWAR_CHL_pn_investment`, local(-4,1), cost5 = 35days. Lifetime: party.

Restrain spending and restore private credit through a civilian fiscal programme.

Requires: (Investment Guarantees).
Excludes: Jarpa's Development Plan.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Interest Rate: -0.75 pp; Bureaucracy Expenditure: -5%; Social Expenditure: -3%; Stability: -3%

#### Jarpa's Development Plan

`COLDWAR_CHL_pn_jarpa`. Absolute(94,1), anchor`COLDWAR_CHL_pn_investment`, local(4,1), cost5 = 35days. Lifetime: party.

Favor domestic producers and provincial industry over a rapid opening of imports.

Requires: (Investment Guarantees).
Excludes: Alessandri's Republic.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Production Efficiency Cap: +4%; Trade Opinion: -6%

#### Compensation Courts

`COLDWAR_CHL_pn_compensation`. Absolute(86,2), anchor`COLDWAR_CHL_pn_investment`, local(-4,2), cost5 = 35days. Lifetime: party.

Resolve expropriation claims through compensation and ordinary courts.

Requires: (Alessandri's Republic).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +6%; Stability: +2%; Bureaucracy Expenditure: +3%

#### National Supply Contracts

`COLDWAR_CHL_pn_suppliers`. Absolute(94,2), anchor`COLDWAR_CHL_pn_investment`, local(4,2), cost5 = 35days. Lifetime: party.

Reserve development contracts for qualified domestic suppliers.

Requires: (Jarpa's Development Plan).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Production Efficiency Growth: +6%; Civilian Factory Construction Speed: +5%; Bureaucracy Expenditure: +2%
- State468: +1 shared slots, then +1 industrial_complex.

#### Competitive Enterprise

`COLDWAR_CHL_pn_liberal`. Absolute(84,3), anchor`COLDWAR_CHL_pn_investment`, local(-6,3), cost5 = 35days. Lifetime: party.

Favor competition and lower entry barriers while accepting lower immediate tax yield.

Requires: (Compensation Courts).
Excludes: Conservative Social Policy.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Construction Speed: +8%; Tax Revenue: -3%; Trade Opinion: +4%

#### Conservative Social Policy

`COLDWAR_CHL_pn_social`. Absolute(88,3), anchor`COLDWAR_CHL_pn_investment`, local(-2,3), cost5 = 35days. Lifetime: party.

Protect pensions and family assistance to broaden the conservative mandate.

Requires: (Compensation Courts).
Excludes: Competitive Enterprise.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +6%; Social Expenditure: +6%

#### Commercial Agriculture

`COLDWAR_CHL_pn_agrarian`. Absolute(92,3), anchor`COLDWAR_CHL_pn_investment`, local(2,3), cost5 = 35days. Lifetime: party.

Prioritize commercially viable farming and private investment over further redistribution.

Requires: (National Supply Contracts).
Excludes: Provincial Industrial Credit.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +12%; Corporate Tax Revenue: +3%; Stability: -4%

#### Provincial Industrial Credit

`COLDWAR_CHL_pn_provincial`. Absolute(96,3), anchor`COLDWAR_CHL_pn_investment`, local(6,3), cost5 = 35days. Lifetime: party.

Direct credit to provincial manufacturers even where private finance is reluctant.

Requires: (National Supply Contracts).
Excludes: Commercial Agriculture.
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Interest Rate: +0.25 pp

#### A Constitutional Right

`COLDWAR_CHL_pn_compact`. Absolute(90,4), anchor`COLDWAR_CHL_pn_investment`, local(0,4), cost5 = 35days. Lifetime: party.

Bind the civilian right to elections and reject an autonomous military political mandate.

Requires: (Competitive Enterprise OR Conservative Social Policy OR Commercial Agriculture OR Provincial Industrial Credit).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +8%; Foreign Influence Defense: +6%

#### Diversify Exports

`COLDWAR_CHL_pn_portfolio`. Absolute(88,5), anchor`COLDWAR_CHL_pn_investment`, local(-2,5), cost5 = 35days. Lifetime: party.

Develop agricultural and manufacturing exports alongside copper.

Requires: (A Constitutional Right).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +6%; Agriculture Productivity: +4%; Bureaucracy Expenditure: +2%

#### Accountable Public Order

`COLDWAR_CHL_pn_policing`. Absolute(92,5), anchor`COLDWAR_CHL_pn_investment`, local(2,5), cost5 = 35days. Lifetime: party.

Improve police readiness under civilian legal supervision.

Requires: (A Constitutional Right).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +4%; Police Expenditure: +4%

#### A Conservative Mandate

`COLDWAR_CHL_pn_republic`. Absolute(90,6), anchor`COLDWAR_CHL_pn_investment`, local(0,6), cost5 = 35days. Lifetime: party.

Consolidate a conservative programme that can survive the next competitive election.

Requires: (Diversify Exports) AND (Accountable Public Order).
Native availability and reward guard: `western_liberals_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Stability: +4%; Corporate Tax Revenue: +4%; Social Expenditure: +2%

### Radical Republicanism

#### The Teachers' Republic

`COLDWAR_CHL_pr_teachers`. Absolute(106,0), anchor`none`, local(106,0), cost5 = 35days. Lifetime: party.

Rebuild the Radical tradition of public education and secular civic service.

Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +2.5%; Education Expenditure: +4%

#### Baltra's Development Plan

`COLDWAR_CHL_pr_baltra`. Absolute(102,1), anchor`COLDWAR_CHL_pr_teachers`, local(-4,1), cost5 = 35days. Lifetime: party.

Use planning and public investment to integrate a plural left governing coalition.

Requires: (The Teachers' Republic).
Excludes: A Republican Center-Left.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +6%; Civilian Factory Construction Speed: +5%; Bureaucracy Expenditure: +4%

#### A Republican Center-Left

`COLDWAR_CHL_pr_bridge`. Absolute(110,1), anchor`COLDWAR_CHL_pr_teachers`, local(4,1), cost5 = 35days. Lifetime: party.

Seek a constitutional center-left coalition with clear limits on unilateral executive action.

Requires: (The Teachers' Republic).
Excludes: Baltra's Development Plan.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +12%; Stability: +4%; Corporate Tax Revenue: -2%

#### CORFO Regional Projects

`COLDWAR_CHL_pr_corfo`. Absolute(102,2), anchor`COLDWAR_CHL_pr_teachers`, local(-4,2), cost5 = 35days. Lifetime: party.

Expand selected regional industrial projects through the development corporation.

Requires: (Baltra's Development Plan).
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Production Efficiency Cap: +5%; Construction Speed: +4%
- State463: +1 shared slots, then +1 industrial_complex.

#### Provincial Civil Service

`COLDWAR_CHL_pr_provinces`. Absolute(110,2), anchor`COLDWAR_CHL_pr_teachers`, local(4,2), cost5 = 35days. Lifetime: party.

Strengthen professional administration beyond Santiago.

Requires: (A Republican Center-Left).
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Bureaucracy Expenditure: -6%; Stability: +3%

#### Secular Public Schools

`COLDWAR_CHL_pr_secular`. Absolute(100,3), anchor`COLDWAR_CHL_pr_teachers`, local(-6,3), cost5 = 35days. Lifetime: party.

Direct scarce education funds toward a common secular public system.

Requires: (CORFO Regional Projects).
Excludes: Plural Education Pacts.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +4%; Education Expenditure: +5%; Stability: -2%

#### Plural Education Pacts

`COLDWAR_CHL_pr_plural`. Absolute(104,3), anchor`COLDWAR_CHL_pr_teachers`, local(-2,3), cost5 = 35days. Lifetime: party.

Fund public education alongside agreed provision by independent institutions.

Requires: (CORFO Regional Projects).
Excludes: Secular Public Schools.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +2.5%; Stability: +4%; Education Expenditure: +6%

#### An Independent Plan

`COLDWAR_CHL_pr_planning`. Absolute(108,3), anchor`COLDWAR_CHL_pr_teachers`, local(2,3), cost5 = 35days. Lifetime: party.

Insulate investment planning from immediate party patronage.

Requires: (Provincial Civil Service).
Excludes: Budgetary Oversight.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Construction Speed: +8%; Bureaucracy Expenditure: +4%; Political Power Gain: -3%

#### Budgetary Oversight

`COLDWAR_CHL_pr_parliament`. Absolute(112,3), anchor`COLDWAR_CHL_pr_teachers`, local(6,3), cost5 = 35days. Lifetime: party.

Give parliamentary committees real leverage over expenditure and borrowing.

Requires: (Provincial Civil Service).
Excludes: An Independent Plan.
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Interest Rate: -0.5 pp; Tax Revenue: +4%; Political Power Gain: -4%

#### Provincial Hospitals

`COLDWAR_CHL_pr_health`. Absolute(106,4), anchor`COLDWAR_CHL_pr_teachers`, local(0,4), cost5 = 35days. Lifetime: party.

Improve access to health care in the provincial republic.

Requires: (Secular Public Schools OR Plural Education Pacts OR An Independent Plan OR Budgetary Oversight).
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Stability: +5%; Health Expenditure: +6%

#### Pluralist Development

`COLDWAR_CHL_pr_pluralist`. Absolute(106,5), anchor`COLDWAR_CHL_pr_teachers`, local(0,5), cost5 = 35days. Lifetime: party.

Keep the development state accountable to a competitive parliamentary coalition.

Requires: (Provincial Hospitals).
Native availability and reward guard: `western_social_democrats_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Factory Output: +4%; Political Power Gain: +5%; Bureaucracy Expenditure: +2%

### The Socialist Party and the Chilean Road

#### The Nutrition Programme

`COLDWAR_CHL_ps_milk`. Absolute(122,0), anchor`none`, local(122,0), cost5 = 35days. Lifetime: party.

Provide milk and basic nutrition through schools and public health services.

Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00200billion.
- Stability: +5%; Health Expenditure: +4%; Social Expenditure: +3%

#### Allende's Legal Road

`COLDWAR_CHL_ps_allende`. Absolute(118,1), anchor`COLDWAR_CHL_ps_milk`, local(-4,1), cost5 = 35days. Lifetime: party.

Seek a durable socialist mandate through constitutional guarantees and broad electoral support.

Requires: (The Nutrition Programme).
Excludes: The Industrial Cordons.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +5%; Political Power Gain: +8%; Bureaucracy Expenditure: +2%

#### The Industrial Cordons

`COLDWAR_CHL_ps_cordones`. Absolute(126,1), anchor`COLDWAR_CHL_ps_milk`, local(4,1), cost5 = 35days. Lifetime: party.

Empower industrial coordination committees, accepting a sharper confrontation over authority.

Requires: (The Nutrition Programme).
Excludes: Allende's Legal Road.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Factory Output: +10%; Division Organization: -3%; Stability: -4%

#### A Social Property Pact

`COLDWAR_CHL_ps_mixed`. Absolute(118,2), anchor`COLDWAR_CHL_ps_milk`, local(-4,2), cost5 = 35days. Lifetime: party.

Negotiate the boundaries of public, mixed and private enterprise to keep production and credit flowing.

Requires: (Allende's Legal Road).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +4%; Factory Output: +4%; Resource Export Revenue: -2%

#### Workers' Councils

`COLDWAR_CHL_ps_control`. Absolute(126,2), anchor`COLDWAR_CHL_ps_milk`, local(4,2), cost5 = 35days. Lifetime: party.

Make worker councils responsible for management and production targets.

Requires: (The Industrial Cordons).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Production Efficiency Growth: +5%; Bureaucracy Expenditure: +5%

#### Project Cybersyn

`COLDWAR_CHL_ps_cybersyn`. Absolute(116,3), anchor`COLDWAR_CHL_ps_milk`, local(-6,3), cost5 = 35days. Lifetime: party.

Use telex networks and industrial reporting to coordinate public enterprises.

Requires: (A Social Property Pact).
Excludes: Regional Economic Boards.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Research Speed: +2.5%; Production Efficiency Cap: +6%; Education Expenditure: +4%
- 1 x 35% research bonus: CAT_computing.

#### Regional Economic Boards

`COLDWAR_CHL_ps_decentral`. Absolute(120,3), anchor`COLDWAR_CHL_ps_milk`, local(-2,3), cost5 = 35days. Lifetime: party.

Delegate development priorities to regional councils instead of concentrating every decision in Santiago.

Requires: (A Social Property Pact).
Excludes: Project Cybersyn.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Construction Speed: +7%; Stability: +3%; Bureaucracy Expenditure: +4%

#### A Bargain with the CUT

`COLDWAR_CHL_ps_bargain`. Absolute(124,3), anchor`COLDWAR_CHL_ps_milk`, local(2,3), cost5 = 35days. Lifetime: party.

Trade enforceable social guarantees for agreed production and wage targets.

Requires: (Workers' Councils).
Excludes: Popular Mobilization.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Factory Output: +5%; Stability: +4%; Social Expenditure: +5%

#### Popular Mobilization

`COLDWAR_CHL_ps_mobilization`. Absolute(128,3), anchor`COLDWAR_CHL_ps_milk`, local(6,3), cost5 = 35days. Lifetime: party.

Rely on mass organizations to sustain the government through confrontation.

Requires: (Workers' Councils).
Excludes: A Bargain with the CUT.
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +15%; Foreign Influence Defense: +8%; Stability: -6%; Trade Opinion: -4%

#### Public Housing Works

`COLDWAR_CHL_ps_housing`. Absolute(122,4), anchor`COLDWAR_CHL_ps_milk`, local(0,4), cost5 = 35days. Lifetime: party.

Link public construction and industrial supply to a national housing effort.

Requires: (Project Cybersyn OR Regional Economic Boards OR A Bargain with the CUT OR Popular Mobilization).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Stability: +4%; Civilian Factory Construction Speed: +6%; Social Expenditure: +4%
- State468: +1 shared slots, then +1 industrial_complex.

#### Distribution Boards

`COLDWAR_CHL_ps_supply`. Absolute(120,5), anchor`COLDWAR_CHL_ps_milk`, local(-2,5), cost5 = 35days. Lifetime: party.

Make neighborhood distribution accountable and link it to food supply.

Requires: (Public Housing Works).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Supply Consumption: -5%; Agriculture Productivity: +5%; Bureaucracy Expenditure: +4%

#### Democratic Coexistence

`COLDWAR_CHL_ps_coexistence`. Absolute(124,5), anchor`COLDWAR_CHL_ps_milk`, local(2,5), cost5 = 35days. Lifetime: party.

Accept reciprocal constitutional limits in exchange for recognition of the social programme.

Requires: (Public Housing Works).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +7%; Political Power Gain: -4%; Trade Opinion: +4%

#### The Chilean Road

`COLDWAR_CHL_ps_chilean_road`. Absolute(122,6), anchor`COLDWAR_CHL_ps_milk`, local(0,6), cost5 = 35days. Lifetime: party.

Preserve social gains through a viable, plural and politically accountable economy.

Requires: (Distribution Boards) AND (Democratic Coexistence).
Native availability and reward guard: `neutrality_neutral_social_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Factory Output: +4%; Stability: +4%; Social Expenditure: +2%

### Communist Organization and Popular Unity

#### Organized Labour

`COLDWAR_CHL_pcch_unions`. Absolute(138,0), anchor`none`, local(138,0), cost5 = 35days. Lifetime: party.

Build a disciplined production agreement with organized labor and the broader left.

Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Factory Output: +4%; Stability: +3%; Social Expenditure: +3%

#### A Broad Popular Front

`COLDWAR_CHL_pcch_front`. Absolute(134,1), anchor`COLDWAR_CHL_pcch_unions`, local(-4,1), cost5 = 35days. Lifetime: party.

Keep Popular Unity open to non-Marxist partners and defend electoral organization.

Requires: (Organized Labour).
Excludes: Industrial Party Cadres.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +10%; Stability: +5%; Bureaucracy Expenditure: +2%

#### Industrial Party Cadres

`COLDWAR_CHL_pcch_cadres`. Absolute(142,1), anchor`COLDWAR_CHL_pcch_unions`, local(4,1), cost5 = 35days. Lifetime: party.

Concentrate trained organizers in mines, factories and public enterprises.

Requires: (Organized Labour).
Excludes: A Broad Popular Front.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Production Efficiency Cap: +8%; Production Efficiency Growth: +4%; Political Power Gain: -3%

#### Soviet Technical Training

`COLDWAR_CHL_pcch_soviet`. Absolute(134,2), anchor`COLDWAR_CHL_pcch_unions`, local(-4,2), cost5 = 35days. Lifetime: party.

Adapt supplier standards and technical training to Soviet cooperation.

Requires: (A Broad Popular Front).
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +2.5%; Production Efficiency Cap: +4%; Foreign Influence Defense: -4%

#### Domestic Machinery

`COLDWAR_CHL_pcch_domestic`. Absolute(142,2), anchor`COLDWAR_CHL_pcch_unions`, local(4,2), cost5 = 35days. Lifetime: party.

Build domestic repair and machinery networks instead of relying on a single foreign supplier.

Requires: (Industrial Party Cadres).
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +6%; Production Efficiency Growth: +4%; Trade Opinion: -3%
- State468: +1 shared slots, then +1 industrial_complex.

#### Production before Growth

`COLDWAR_CHL_pcch_cautious`. Absolute(132,3), anchor`COLDWAR_CHL_pcch_unions`, local(-6,3), cost5 = 35days. Lifetime: party.

Prioritize operating existing public enterprises before widening the social property area.

Requires: (Soviet Technical Training).
Excludes: Public Sector Unity.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Trade Opinion: +3%; Political Power Gain: -3%

#### Public Sector Unity

`COLDWAR_CHL_pcch_public`. Absolute(136,3), anchor`COLDWAR_CHL_pcch_unions`, local(-2,3), cost5 = 35days. Lifetime: party.

Concentrate investment and management within a larger public-enterprise system.

Requires: (Soviet Technical Training).
Excludes: Production before Growth.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +7%; Production Efficiency Cap: +6%; Bureaucracy Expenditure: +5%

#### Union Autonomy

`COLDWAR_CHL_pcch_local`. Absolute(140,3), anchor`COLDWAR_CHL_pcch_unions`, local(2,3), cost5 = 35days. Lifetime: party.

Preserve bargaining autonomy for organized workers within a left government.

Requires: (Domestic Machinery).
Excludes: Production Agreements.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Factory Output: +2%; Social Expenditure: +4%

#### Production Agreements

`COLDWAR_CHL_pcch_plan`. Absolute(144,3), anchor`COLDWAR_CHL_pcch_unions`, local(6,3), cost5 = 35days. Lifetime: party.

Enforce production obligations across public enterprises and organized labor.

Requires: (Domestic Machinery).
Excludes: Union Autonomy.
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Factory Output: +9%; Production Efficiency Growth: +3%; Stability: -4%

#### Workers' Technical Schools

`COLDWAR_CHL_pcch_literacy`. Absolute(138,4), anchor`COLDWAR_CHL_pcch_unions`, local(0,4), cost5 = 35days. Lifetime: party.

Make technical education accessible to industrial workers and their families.

Requires: (Production before Growth OR Public Sector Unity OR Union Autonomy OR Production Agreements).
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Research Speed: +3.5%; Education Expenditure: +5%

#### A Plural Popular Unity

`COLDWAR_CHL_pcch_pluralism`. Absolute(138,5), anchor`COLDWAR_CHL_pcch_unions`, local(0,5), cost5 = 35days. Lifetime: party.

Retain a coalition of distinct parties rather than equating socialist development with one-party rule.

Requires: (Workers' Technical Schools).
Native availability and reward guard: `emerging_communist_state_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +5%; Stability: +5%; Bureaucracy Expenditure: +2%

### MAPU and Agrarian Socialism

#### Rural Reform Service

`COLDWAR_CHL_mapu_extension`. Absolute(154,0), anchor`none`, local(154,0), cost5 = 35days. Lifetime: party.

Deploy agrarian reform technicians and young professionals alongside peasant organizations.

Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +6%; Education Expenditure: +2%

#### Chonchol's Administration

`COLDWAR_CHL_mapu_technicians`. Absolute(150,1), anchor`COLDWAR_CHL_mapu_extension`, local(-4,1), cost5 = 35days. Lifetime: party.

Make technical support, credit and accountable administration the core of agrarian change.

Requires: (Rural Reform Service).
Excludes: Popular Agrarian Power.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +10%; Bureaucracy Expenditure: +4%

#### Popular Agrarian Power

`COLDWAR_CHL_mapu_popular`. Absolute(158,1), anchor`COLDWAR_CHL_mapu_extension`, local(4,1), cost5 = 35days. Lifetime: party.

Give organized peasants greater authority over the pace and institutions of reform.

Requires: (Rural Reform Service).
Excludes: Chonchol's Administration.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +12%; Agriculture Productivity: +6%; Stability: -4%

#### Cooperative Machinery

`COLDWAR_CHL_mapu_technical`. Absolute(150,2), anchor`COLDWAR_CHL_mapu_extension`, local(-4,2), cost5 = 35days. Lifetime: party.

Finance common machinery and trained maintenance teams.

Requires: (Chonchol's Administration).
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Agriculture Productivity: +7%; Production Efficiency Cap: +3%
- State463: +1 shared slots, then +1 agriculture_district.

#### Land Councils and Titles

`COLDWAR_CHL_mapu_land`. Absolute(158,2), anchor`COLDWAR_CHL_mapu_extension`, local(4,2), cost5 = 35days. Lifetime: party.

Make peasant councils responsible for durable titles and conflict resolution.

Requires: (Popular Agrarian Power).
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +3%; Agriculture Productivity: +5%; Bureaucracy Expenditure: +3%

#### Christian Social Reform

`COLDWAR_CHL_mapu_christian`. Absolute(148,3), anchor`COLDWAR_CHL_mapu_extension`, local(-6,3), cost5 = 35days. Lifetime: party.

Retain a bridge to Catholic social institutions and the reformist Christian left.

Requires: (Cooperative Machinery).
Excludes: Independent Marxism.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Health Expenditure: +4%

#### Independent Marxism

`COLDWAR_CHL_mapu_marxist`. Absolute(152,3), anchor`COLDWAR_CHL_mapu_extension`, local(-2,3), cost5 = 35days. Lifetime: party.

Define an independent Marxist programme beyond Christian Democracy or Soviet tutelage.

Requires: (Cooperative Machinery).
Excludes: Christian Social Reform.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Foreign Influence Defense: +5%; Trade Opinion: -4%

#### Cooperative Autonomy

`COLDWAR_CHL_mapu_local`. Absolute(156,3), anchor`COLDWAR_CHL_mapu_extension`, local(2,3), cost5 = 35days. Lifetime: party.

Allow local cooperatives discretion over output and retained earnings.

Requires: (Land Councils and Titles).
Excludes: Food Delivery Contracts.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +8%; Stability: +3%; Tax Revenue: -2%

#### Food Delivery Contracts

`COLDWAR_CHL_mapu_delivery`. Absolute(160,3), anchor`COLDWAR_CHL_mapu_extension`, local(6,3), cost5 = 35days. Lifetime: party.

Bind cooperatives to food delivery contracts while improving transport and storage.

Requires: (Land Councils and Titles).
Excludes: Cooperative Autonomy.
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +5%; Supply Consumption: -5%; Bureaucracy Expenditure: +4%

#### Rural Schools and Clinics

`COLDWAR_CHL_mapu_service`. Absolute(154,4), anchor`COLDWAR_CHL_mapu_extension`, local(0,4), cost5 = 35days. Lifetime: party.

Bring health care and technical schooling into the reformed countryside.

Requires: (Christian Social Reform OR Independent Marxism OR Cooperative Autonomy OR Food Delivery Contracts).
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Research Speed: +2%; Health Expenditure: +4%; Education Expenditure: +3%

#### An Agrarian Settlement

`COLDWAR_CHL_mapu_reform`. Absolute(154,5), anchor`COLDWAR_CHL_mapu_extension`, local(0,5), cost5 = 35days. Lifetime: party.

Build a durable settlement around productive land, secure rights and rural institutions.

Requires: (Rural Schools and Clinics).
Native availability and reward guard: `neutrality_neutral_communism_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +5%; Stability: +4%; Social Expenditure: +2%

### Radical Democracy

#### Secular Republicanism

`COLDWAR_CHL_dr_republic`. Absolute(74,9), anchor`none`, local(74,9), cost5 = 35days. Lifetime: party.

Offer a secular, anti-communist parliamentary alternative rooted in the provincial middle classes.

Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +8%; Stability: +3%

#### An Independent Bloc

`COLDWAR_CHL_dr_independent`. Absolute(71,10), anchor`COLDWAR_CHL_dr_republic`, local(-3,1), cost5 = 35days. Lifetime: party.

Defend an independent center rather than merging with the National Party.

Requires: (Secular Republicanism).
Excludes: A Civilian Right Accord.
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +10%; Foreign Influence Defense: +6%; Stability: -2%

#### A Civilian Right Accord

`COLDWAR_CHL_dr_alliance`. Absolute(77,10), anchor`COLDWAR_CHL_dr_republic`, local(3,1), cost5 = 35days. Lifetime: party.

Negotiate a civilian coalition with the electoral right.

Requires: (Secular Republicanism).
Excludes: An Independent Bloc.
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +5%; Stability: +4%; Bureaucracy Expenditure: +2%

#### Schools and Examinations

`COLDWAR_CHL_dr_schools`. Absolute(74,11), anchor`COLDWAR_CHL_dr_republic`, local(0,2), cost5 = 35days. Lifetime: party.

Defend secular schools and professional entry to public service.

Requires: (An Independent Bloc OR A Civilian Right Accord).
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +2.5%; Bureaucracy Expenditure: -3%; Education Expenditure: +4%

#### Credit for Small Proprietors

`COLDWAR_CHL_dr_small_business`. Absolute(71,12), anchor`COLDWAR_CHL_dr_republic`, local(-3,3), cost5 = 35days. Lifetime: party.

Finance small commercial and productive firms without wholesale privatization.

Requires: (Schools and Examinations).
Excludes: A Reformed Mixed Sector.
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +6%; Construction Speed: +3%; Tax Revenue: -2%

#### A Reformed Mixed Sector

`COLDWAR_CHL_dr_public`. Absolute(77,12), anchor`COLDWAR_CHL_dr_republic`, local(3,3), cost5 = 35days. Lifetime: party.

Keep a mixed economy under stricter public accounting.

Requires: (Schools and Examinations).
Excludes: Credit for Small Proprietors.
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Factory Output: +5%; Civilian Factory Construction Speed: +5%; Bureaucracy Expenditure: +3%
- State463: +1 shared slots, then +1 industrial_complex.

#### Provincial Services

`COLDWAR_CHL_dr_provincial`. Absolute(74,13), anchor`COLDWAR_CHL_dr_republic`, local(0,4), cost5 = 35days. Lifetime: party.

Give provincial municipalities a funded service programme.

Requires: (Credit for Small Proprietors OR A Reformed Mixed Sector).
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +5%; Social Expenditure: +4%

#### Republican Succession

`COLDWAR_CHL_dr_constitution`. Absolute(74,14), anchor`COLDWAR_CHL_dr_republic`, local(0,5), cost5 = 35days. Lifetime: party.

Preserve the parliamentary republic and competitive civilian succession.

Requires: (Provincial Services).
Native availability and reward guard: `neutrality_neutral_conservatism_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Stability: +4%; Political Power Gain: +5%; Bureaucracy Expenditure: +1%

### PADENA and Provincial Populism

#### The Forgotten Provinces

`COLDWAR_CHL_padena_provinces`. Absolute(90,9), anchor`none`, local(90,9), cost5 = 35days. Lifetime: party.

Address small farmers, pensioners and employees outside the metropolitan party networks.

Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +4%; Social Expenditure: +3%

#### Small-Farmer Credit

`COLDWAR_CHL_padena_coops`. Absolute(87,10), anchor`COLDWAR_CHL_padena_provinces`, local(-3,1), cost5 = 35days. Lifetime: party.

Protect small farmers with public credit and common purchasing.

Requires: (The Forgotten Provinces).
Excludes: Provincial Enterprise.
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Agriculture Productivity: +10%; Interest Rate: +0.25 pp

#### Provincial Enterprise

`COLDWAR_CHL_padena_enterprise`. Absolute(93,10), anchor`COLDWAR_CHL_padena_provinces`, local(3,1), cost5 = 35days. Lifetime: party.

Back small provincial manufacturers and transport firms.

Requires: (The Forgotten Provinces).
Excludes: Small-Farmer Credit.
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Civilian Factory Construction Speed: +7%; Corporate Tax Revenue: +4%; Bureaucracy Expenditure: +3%
- State463: +1 shared slots, then +1 industrial_complex.

#### Honest Public Contracts

`COLDWAR_CHL_padena_integrity`. Absolute(90,11), anchor`COLDWAR_CHL_padena_provinces`, local(0,2), cost5 = 35days. Lifetime: party.

Audit local contracts and patronage rather than promise an unexplained end to corruption.

Requires: (Small-Farmer Credit OR Provincial Enterprise).
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Bureaucracy Expenditure: -4%; Political Power Gain: +5%

#### Protect Pensioner Incomes

`COLDWAR_CHL_padena_pensions`. Absolute(87,12), anchor`COLDWAR_CHL_padena_provinces`, local(-3,3), cost5 = 35days. Lifetime: party.

Fund pension protection as a visible social commitment.

Requires: (Honest Public Contracts).
Excludes: Provincial Roads.
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +7%; Social Expenditure: +7%

#### Provincial Roads

`COLDWAR_CHL_padena_roads`. Absolute(93,12), anchor`COLDWAR_CHL_padena_provinces`, local(3,3), cost5 = 35days. Lifetime: party.

Direct the available budget toward transport links and market access.

Requires: (Honest Public Contracts).
Excludes: Protect Pensioner Incomes.
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Infrastructure Construction Speed: +12%; Social Expenditure: -2%
- State463: +1 shared slots, then +1 infrastructure.

#### A Provincial Coalition

`COLDWAR_CHL_padena_bargain`. Absolute(90,13), anchor`COLDWAR_CHL_padena_provinces`, local(0,4), cost5 = 35days. Lifetime: party.

Turn provincial representation into a negotiated civilian governing coalition.

Requires: (Protect Pensioner Incomes OR Provincial Roads).
Native availability and reward guard: `nationalist_right_wing_populists_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +10%; Stability: +3%; Bureaucracy Expenditure: +2%

### Gremialist Institutional Conservatism

#### Professional Associations

`COLDWAR_CHL_gremial_guilds`. Absolute(106,9), anchor`none`, local(106,9), cost5 = 35days. Lifetime: party.

Bring professional and university associations into a conservative institutional programme.

Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Production Efficiency Cap: +4%; Political Power Gain: +6%; Stability: -2%

#### The Subsidiary State

`COLDWAR_CHL_gremial_subsidiary`. Absolute(102,10), anchor`COLDWAR_CHL_gremial_guilds`, local(-4,1), cost5 = 35days. Lifetime: party.

Delegate provision to private and civic institutions while limiting direct state management.

Requires: (Professional Associations).
Excludes: A Corporatist Compact.
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Construction Speed: +8%; Bureaucracy Expenditure: -5%; Tax Revenue: -3%

#### A Corporatist Compact

`COLDWAR_CHL_gremial_corporate`. Absolute(110,10), anchor`COLDWAR_CHL_gremial_guilds`, local(4,1), cost5 = 35days. Lifetime: party.

Organize negotiated representation through professional and employer bodies.

Requires: (Professional Associations).
Excludes: The Subsidiary State.
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Factory Output: +7%; Stability: +3%; Political Power Gain: -4%

#### Independent Schools

`COLDWAR_CHL_gremial_schools`. Absolute(102,11), anchor`COLDWAR_CHL_gremial_guilds`, local(-4,2), cost5 = 35days. Lifetime: party.

Shift provision toward independent institutions while accepting unequal access.

Requires: (The Subsidiary State).
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Research Speed: +3%; Education Expenditure: -3%; Stability: -3%

#### Civic Social Provision

`COLDWAR_CHL_gremial_social`. Absolute(110,11), anchor`COLDWAR_CHL_gremial_guilds`, local(4,2), cost5 = 35days. Lifetime: party.

Finance civic organizations to provide family and neighborhood services.

Requires: (A Corporatist Compact).
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Stability: +5%; Social Expenditure: +5%

#### Protected Institutions

`COLDWAR_CHL_gremial_tutelage`. Absolute(102,12), anchor`COLDWAR_CHL_gremial_guilds`, local(-4,3), cost5 = 35days. Lifetime: party.

Entrench institutional vetoes against elected opponents, accepting a continuing legitimacy conflict.

Requires: (Independent Schools).
Excludes: An Electoral Right, Functional Representation.
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Foreign Influence Defense: +10%; Political Power Gain: +10%; Stability: -6%; Trade Opinion: -4%

#### An Electoral Right

`COLDWAR_CHL_gremial_electoral`. Absolute(106,12), anchor`COLDWAR_CHL_gremial_guilds`, local(0,3), cost5 = 35days. Lifetime: party.

Transform the movement into an accountable electoral organization.

Requires: (Independent Schools OR Civic Social Provision).
Excludes: Protected Institutions, Functional Representation.
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Corporate Tax Revenue: +4%; Political Power Gain: -3%

#### Functional Representation

`COLDWAR_CHL_gremial_guildrule`. Absolute(110,12), anchor`COLDWAR_CHL_gremial_guilds`, local(4,3), cost5 = 35days. Lifetime: party.

Prioritize organized professional representation over open partisan competition.

Requires: (Civic Social Provision).
Excludes: Protected Institutions, An Electoral Right.
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Production Efficiency Cap: +7%; Bureaucracy Expenditure: -4%; Stability: -5%

#### Conservative Continuity

`COLDWAR_CHL_gremial_continuity`. Absolute(106,13), anchor`COLDWAR_CHL_gremial_guilds`, local(0,4), cost5 = 35days. Lifetime: party.

Consolidate the selected institutional settlement without erasing its constitutional liabilities.

Requires: (Protected Institutions OR An Electoral Right OR Functional Representation).
Native availability and reward guard: `western_autocrats_are_in_power = yes`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Construction Speed: +4%; Foreign Influence Defense: +4%; Social Expenditure: +2%

### MIR and the Revolutionary Left

#### Settlement Organization

`COLDWAR_CHL_mir_organize`. Absolute(122,9), anchor`none`, local(122,9), cost5 = 35days. Lifetime: party.

Organize marginalized urban and rural communities around a revolutionary programme.

Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +10%; Stability: -3%; Social Expenditure: +2%

#### An Independent Left

`COLDWAR_CHL_mir_civil`. Absolute(118,10), anchor`COLDWAR_CHL_mir_organize`, local(-4,1), cost5 = 35days. Lifetime: party.

Seek a legal mass organization independent of both traditional parliamentary parties and foreign tutelage.

Requires: (Settlement Organization).
Excludes: Revolutionary Vanguard.
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Stability: +4%; Factory Output: +4%; Bureaucracy Expenditure: +3%

#### Revolutionary Vanguard

`COLDWAR_CHL_mir_vanguard`. Absolute(126,10), anchor`COLDWAR_CHL_mir_organize`, local(4,1), cost5 = 35days. Lifetime: party.

Build a disciplined revolutionary governing structure amid continuing domestic confrontation.

Requires: (Settlement Organization).
Excludes: An Independent Left.
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Division Organization: +6%; Foreign Influence Defense: +8%; Stability: -8%; Trade Opinion: -8%

#### Settlement Autonomy

`COLDWAR_CHL_mir_selfmanagement`. Absolute(118,11), anchor`COLDWAR_CHL_mir_organize`, local(-4,2), cost5 = 35days. Lifetime: party.

Give elected settlement committees responsibility for local public works.

Requires: (An Independent Left).
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Stability: +5%; Construction Speed: +5%; Tax Revenue: -3%

#### Defense Committees

`COLDWAR_CHL_mir_territorial`. Absolute(126,11), anchor`COLDWAR_CHL_mir_organize`, local(4,2), cost5 = 35days. Lifetime: party.

Organize territorial defense through the state while imposing larger security and supply burdens.

Requires: (Revolutionary Vanguard).
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Division Defense on Core Territory: +8%; Supply Consumption: +4%; Police Expenditure: +5%

#### A Plural Popular Congress

`COLDWAR_CHL_mir_agreement`. Absolute(118,12), anchor`COLDWAR_CHL_mir_organize`, local(-4,3), cost5 = 35days. Lifetime: party.

Accept a plural political settlement with organized left parties and independent communities.

Requires: (Settlement Autonomy).
Excludes: Revolutionary Command, Revolutionary Autonomy.
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Political Power Gain: +8%; Stability: +5%; Bureaucracy Expenditure: +3%

#### Revolutionary Command

`COLDWAR_CHL_mir_command`. Absolute(122,12), anchor`COLDWAR_CHL_mir_organize`, local(0,3), cost5 = 35days. Lifetime: party.

Concentrate production and security authority in the revolutionary state.

Requires: (Settlement Autonomy OR Defense Committees).
Excludes: A Plural Popular Congress, Revolutionary Autonomy.
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Factory Output: +8%; Division Organization: +3%; Stability: -5%

#### Revolutionary Autonomy

`COLDWAR_CHL_mir_nonalign`. Absolute(126,12), anchor`COLDWAR_CHL_mir_organize`, local(4,3), cost5 = 35days. Lifetime: party.

Reject external political tutelage while bearing a narrower diplomatic and commercial base.

Requires: (Defense Committees).
Excludes: A Plural Popular Congress, Revolutionary Command.
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Foreign Influence Defense: +10%; Resource Export Revenue: -5%; Trade Opinion: -4%

#### Community Services

`COLDWAR_CHL_mir_clinics`. Absolute(122,13), anchor`COLDWAR_CHL_mir_organize`, local(0,4), cost5 = 35days. Lifetime: party.

Consolidate material social provision within the selected revolutionary settlement.

Requires: (A Plural Popular Congress OR Revolutionary Command OR Revolutionary Autonomy).
Native availability and reward guard: `emerging_anarchist_communism_are_in_power = yes`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Research Speed: +2.5%; Health Expenditure: +5%; Education Expenditure: +4%

### The Military Government and Pinochet

#### The Service Chiefs

`COLDWAR_CHL_military_staff`. Absolute(142,9), anchor`none`, local(142,9), cost5 = 35days. Lifetime: party.

Establish the joint administration after a real military transfer of power.

Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_flag = COLDWAR_CHL_military_government`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Division Organization: +4%; Bureaucracy Expenditure: +4%; Stability: -4%

#### A Constitutional Exit

`COLDWAR_CHL_military_constitution`. Absolute(136,10), anchor`COLDWAR_CHL_military_staff`, local(-6,1), cost5 = 35days. Lifetime: party.

Set enforceable limits on military rule and open negotiations for an early civilian transfer.

Requires: (The Service Chiefs).
Excludes: Pinochet's Command.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_flag = COLDWAR_CHL_constitutional_military_council`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +7%; Political Power Gain: -6%; Military Personnel Expenditure: +4%

#### Pinochet's Command

`COLDWAR_CHL_pinochet_command`. Absolute(144,10), anchor`COLDWAR_CHL_military_staff`, local(2,1), cost5 = 35days. Lifetime: leader.

Concentrate the junta presidency in Augusto Pinochet and bear the institutional consequences.

Requires: (The Service Chiefs).
Excludes: A Constitutional Exit.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +15%; Division Organization: +5%; Stability: -6%; Research Speed: -2.5%

#### Guarantee a Civilian Ballot

`COLDWAR_CHL_military_ballot`. Absolute(136,11), anchor`COLDWAR_CHL_military_staff`, local(-6,2), cost5 = 35days. Lifetime: party.

Restore civilian electoral organization under agreed military withdrawal terms. The national election proceeds even if military leaders subsequently lose office.

Requires: (A Constitutional Exit).
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Political Power Gain: -4%; Bureaucracy Expenditure: +3%
- event: early_exit

#### The Chicago Programme

`COLDWAR_CHL_pinochet_chicago`. Absolute(140,11), anchor`COLDWAR_CHL_military_staff`, local(-2,2), cost5 = 35days. Lifetime: leader.

Apply rapid trade, price and market reforms while bearing severe adjustment and social conflict.

Requires: (Pinochet's Command).
Excludes: Strategic State Capitalism.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Construction Speed: +10%; Interest Rate: -0.75 pp; Stability: -8%; Trade Opinion: +5%
- event: adjustment

#### Strategic State Capitalism

`COLDWAR_CHL_pinochet_state`. Absolute(148,11), anchor`COLDWAR_CHL_military_staff`, local(6,2), cost5 = 35days. Lifetime: leader.

Retain strategic public firms and selective protection rather than adopt a comprehensive market opening.

Requires: (Pinochet's Command).
Excludes: The Chicago Programme.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $4.000billion; weekly: $0.00000billion.
- Factory Output: +8%; Production Efficiency Cap: +6%; Bureaucracy Expenditure: +5%; Trade Opinion: -3%
- State468: +1 shared slots, then +1 industrial_complex.

#### Pension Capitalization

`COLDWAR_CHL_pinochet_pensions`. Absolute(138,12), anchor`COLDWAR_CHL_military_staff`, local(-4,3), cost5 = 35days. Lifetime: leader.

Redirect pension contributions toward private capitalization with a difficult transition burden.

Requires: (The Chicago Programme).
Excludes: A Funded Social Floor.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Corporate Tax Revenue: +7%; Social Expenditure: -5%; Stability: -4%

#### A Funded Social Floor

`COLDWAR_CHL_pinochet_floor`. Absolute(142,12), anchor`COLDWAR_CHL_military_staff`, local(0,3), cost5 = 35days. Lifetime: leader.

Retain social protection while pursuing the market programme.

Requires: (The Chicago Programme).
Excludes: Pension Capitalization.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $2.000billion; weekly: $0.00200billion.
- Stability: +7%; Social Expenditure: +7%; Corporate Tax Revenue: -2%

#### Retain Public Copper

`COLDWAR_CHL_pinochet_codelco`. Absolute(146,12), anchor`COLDWAR_CHL_military_staff`, local(4,3), cost5 = 35days. Lifetime: leader.

Retain copper revenues under public ownership and sustain military fiscal claims.

Requires: (Strategic State Capitalism).
Excludes: Mixed Strategic Firms.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +10%; Military Personnel Expenditure: +4%

#### Mixed Strategic Firms

`COLDWAR_CHL_pinochet_private`. Absolute(150,12), anchor`COLDWAR_CHL_military_staff`, local(8,3), cost5 = 35days. Lifetime: leader.

Invite private partners into strategic enterprises while retaining state leverage.

Requires: (Strategic State Capitalism).
Excludes: Retain Public Copper.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Construction Speed: +7%; Production Efficiency Cap: +4%; Foreign Influence Defense: -5%

#### External Debt Review

`COLDWAR_CHL_pinochet_crisis`. Absolute(144,13), anchor`COLDWAR_CHL_military_staff`, local(2,4), cost5 = 35days. Lifetime: leader.

Review banks and external exposure before deciding how to distribute the costs of a credit crisis.

Requires: (Pension Capitalization OR A Funded Social Floor OR Retain Public Copper OR Mixed Strategic Firms).
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Interest Rate: -0.25 pp; Bureaucracy Expenditure: +3%
- decision: Conduct banking stress tests

#### Public Bank Intervention

`COLDWAR_CHL_pinochet_rescue`. Absolute(142,14), anchor`COLDWAR_CHL_military_staff`, local(0,5), cost5 = 35days. Lifetime: national:365 days.

Stabilize lending through public intervention and assume a substantial fiscal burden.

Requires: (External Debt Review).
Excludes: Impose Creditor Losses, Prudential Reform.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }; has_idea = COLDWAR_CHL_bank_crisis`.
- Setup: $6.000billion; weekly: $0.00300billion.
- Construction Speed: +8%; Interest Rate: +0.5 pp; Tax Revenue: -3%
- {'old': 'COLDWAR_CHL_bank_crisis', 'new': 'COLDWAR_CHL_restructuring', 'duration': 365}

#### Impose Creditor Losses

`COLDWAR_CHL_pinochet_losses`. Absolute(146,14), anchor`COLDWAR_CHL_military_staff`, local(4,5), cost5 = 35days. Lifetime: national:365 days.

Limit public rescue costs by imposing losses and accepting a sharper immediate contraction.

Requires: (External Debt Review).
Excludes: Public Bank Intervention, Prudential Reform.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }; has_idea = COLDWAR_CHL_bank_crisis`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Interest Rate: -0.5 pp; Construction Speed: -6%; Stability: -5%
- {'old': 'COLDWAR_CHL_bank_crisis', 'new': 'COLDWAR_CHL_restructuring', 'duration': 365}

#### Prudential Reform

`COLDWAR_CHL_pinochet_supervision`. Absolute(150,14), anchor`COLDWAR_CHL_military_staff`, local(8,5), cost5 = 35days. Lifetime: leader.

Reduce connected lending and currency exposure while restricting the credit boom.

Requires: (External Debt Review).
Excludes: Public Bank Intervention, Impose Creditor Losses.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $2.000billion; weekly: $0.00000billion.
- Interest Rate: -0.25 pp; Corporate Tax Revenue: -3%; Bureaucracy Expenditure: +3%

#### Pragmatic Export Policy

`COLDWAR_CHL_pinochet_pragmatic`. Absolute(144,15), anchor`COLDWAR_CHL_military_staff`, local(2,6), cost5 = 35days. Lifetime: leader.

Support export recovery and targeted intervention without erasing the costs of the previous programme.

Requires: (Public Bank Intervention OR Impose Creditor Losses OR Prudential Reform).
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $3.000billion; weekly: $0.00000billion.
- Resource Export Revenue: +7%; Agriculture Productivity: +5%; Social Expenditure: +3%

#### Technocratic Continuity

`COLDWAR_CHL_pinochet_technocrat`. Absolute(140,16), anchor`COLDWAR_CHL_military_staff`, local(-2,7), cost5 = 35days. Lifetime: leader.

Entrench a managed constitutional succession and restricted political competition.

Requires: (Pragmatic Export Policy).
Excludes: The Security State, An Enforceable Plebiscite.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Construction Speed: +6%; Political Power Gain: +8%; Stability: -4%

#### The Security State

`COLDWAR_CHL_pinochet_security`. Absolute(144,16), anchor`COLDWAR_CHL_military_staff`, local(2,7), cost5 = 35days. Lifetime: leader.

Prioritize military organization and resilient domestic supply under permanent security rule, bearing the costs of repression, isolation and lost expertise.

Requires: (Pragmatic Export Policy).
Excludes: Technocratic Continuity, An Enforceable Plebiscite.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $2.000billion; weekly: $0.00200billion.
- Foreign Influence Defense: +20%; Division Organization: +8%; Stability: -10%; Research Speed: -4%; Trade Opinion: -8%; Police Expenditure: +10%; Sanction Resistance: +12%

#### An Enforceable Plebiscite

`COLDWAR_CHL_pinochet_plebiscite`. Absolute(148,16), anchor`COLDWAR_CHL_military_staff`, local(6,7), cost5 = 35days. Lifetime: leader.

Permit credible registration, campaigning and scrutiny under an agreed transfer procedure.

Requires: (Pragmatic Export Policy).
Excludes: Technocratic Continuity, The Security State.
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +8%; Political Power Gain: -8%; Bureaucracy Expenditure: +3%
- event: plebiscite

#### A Civilian Handover

`COLDWAR_CHL_pinochet_handover`. Absolute(148,17), anchor`COLDWAR_CHL_military_staff`, local(6,8), cost5 = 35days. Lifetime: leader.

Implement the civilian electoral result and negotiated constitutional guarantees.

Requires: (An Enforceable Plebiscite).
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }; has_country_flag = COLDWAR_CHL_plebiscite_no_won`.
- Setup: $1.000billion; weekly: $0.00000billion.
- Stability: +6%; Military Personnel Expenditure: +3%
- event: handover

#### Military Continuation

`COLDWAR_CHL_pinochet_continuity`. Absolute(142,17), anchor`COLDWAR_CHL_military_staff`, local(0,8), cost5 = 35days. Lifetime: leader.

Maintain military rule under the selected institutional settlement and its unresolved legitimacy conflict.

Requires: (Technocratic Continuity OR The Security State).
Native availability and reward guard: `nationalist_military_junta_are_in_power = yes; has_country_leader = { name = "Augusto Pinochet" ruling_only = yes }`.
- Setup: $0.000billion; weekly: $0.00000billion.
- Political Power Gain: +6%; Stability: -4%; Police Expenditure: +4%

### Agreements across the Pacific and the Andes

#### The Diplomatic Service

`COLDWAR_CHL_diplomatic_service`. Absolute(48,9), anchor`none`, local(48,9), cost3 = 21days. Lifetime: national.

Give Chile the capacity to negotiate with its neighbors and competing Cold War partners.

- Setup: $1.000billion; weekly: $0.00000billion.
- Trade Opinion: +4%; Bureaucracy Expenditure: +2%

#### US Copper Protocol

`COLDWAR_CHL_usa_mines`. Absolute(42,10), anchor`COLDWAR_CHL_diplomatic_service`, local(-6,1), cost5 = 35days. Lifetime: national.

Offer a compensation settlement and technical partnership for the copper industry.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_usa_mines

#### Soviet Machinery Credit

`COLDWAR_CHL_soviet_machinery`. Absolute(46,10), anchor`COLDWAR_CHL_diplomatic_service`, local(-2,1), cost5 = 35days. Lifetime: national.

Propose machinery deliveries and technical training backed by reciprocal commitments.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_soviet_machinery

#### Pacific Copper Contract

`COLDWAR_CHL_japan_copper`. Absolute(50,10), anchor`COLDWAR_CHL_diplomatic_service`, local(2,1), cost5 = 35days. Lifetime: national.

Offer long-term copper sales in exchange for port equipment and industrial cooperation.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_japan_copper

#### Cuban Health Exchange

`COLDWAR_CHL_cuba_clinics`. Absolute(54,10), anchor`COLDWAR_CHL_diplomatic_service`, local(6,1), cost5 = 35days. Lifetime: national.

Offer a reciprocal programme of medical training, public health and clinical exchange.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_cuba_clinics

#### Beagle Peace Treaty

`COLDWAR_CHL_argentina_beagle`. Absolute(42,12), anchor`COLDWAR_CHL_diplomatic_service`, local(-6,3), cost5 = 35days. Lifetime: national.

Offer a mutually ratified settlement, maritime confidence measures and border cooperation.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_argentina_beagle

#### Pacific Maritime Protocol

`COLDWAR_CHL_peru_maritime`. Absolute(46,12), anchor`COLDWAR_CHL_diplomatic_service`, local(-2,3), cost5 = 35days. Lifetime: national.

Offer incident prevention, port contacts and transparent notification of exercises.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_peru_maritime

#### Bolivian Transit Protocol

`COLDWAR_CHL_bolivia_transit`. Absolute(50,12), anchor`COLDWAR_CHL_diplomatic_service`, local(2,3), cost5 = 35days. Lifetime: national.

Offer improved bonded transit and commercial handling through Chilean ports.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_bolivia_transit

#### French Technical Accord

`COLDWAR_CHL_france_technical`. Absolute(54,12), anchor`COLDWAR_CHL_diplomatic_service`, local(6,3), cost5 = 35days. Lifetime: national.

Offer university, engineering and industrial technical cooperation.

Requires: (The Diplomatic Service).
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_france_technical

#### The Andean Protocol

`COLDWAR_CHL_andean_admission`. Absolute(48,11), anchor`COLDWAR_CHL_diplomatic_service`, local(0,2), cost5 = 35days. Lifetime: national.

Propose a jointly ratified industrial protocol to Bolivia, Colombia, Ecuador and Peru within the Cartagena institutions.

Requires: (The Diplomatic Service).
Native availability and reward guard: `; has_idea = COLDWAR_CHL_cartagena_member`.
- Setup: $0.000billion; weekly: $0.00000billion.
- None
- agreement: COLDWAR_CHL_andean_protocol

#### Andean Specialization

`COLDWAR_CHL_andean_industry`. Absolute(46,15), anchor`COLDWAR_CHL_diplomatic_service`, local(-2,6), cost5 = 35days. Lifetime: membership.

Coordinate industrial specialization with the Andean partners under the actual membership agreement.

Requires: (The Andean Protocol).
Excludes: Andean Technical Mobility.
Native availability and reward guard: `; has_idea = COLDWAR_CHL_cartagena_member; has_idea = COLDWAR_CHL_andean_protocol_chile`.
- Setup: $3.000billion; weekly: $0.00100billion.
- Production Efficiency Cap: +6%; Factory Output: +4%; Trade Opinion: -3%
- State468: +1 shared slots, then +1 industrial_complex.

#### Andean Technical Mobility

`COLDWAR_CHL_andean_autonomy`. Absolute(50,15), anchor`COLDWAR_CHL_diplomatic_service`, local(2,6), cost5 = 35days. Lifetime: membership.

Prioritize mobile technical teams and training over domestic industrial specialization.

Requires: (The Andean Protocol).
Excludes: Andean Specialization.
Native availability and reward guard: `; has_idea = COLDWAR_CHL_cartagena_member; has_idea = COLDWAR_CHL_andean_protocol_chile`.
- Setup: $2.000billion; weekly: $0.00100billion.
- Trade Opinion: +6%; Research Speed: +2.5%; Education Expenditure: +4%
- 1 x 25% research bonus: CAT_industry.

## Verification and provenance

Read MD_REFERENCE.md, HISTORICAL_RESEARCH.md and MECHANICS_AUDIT.md for source paths, direct historical URLs, native provider/consumer traces and units. DESIGN_REVIEW.md, HISTORY_DESIGN_REVIEW.md and LAYOUT_REVIEW.md are independent first-pass reviews; REVIEW_RESOLUTIONS.md records their final disposition.
MODEL_QA.json checks IDs, anchors, card bounds, reciprocal exclusions and compatible prerequisite histories. BROWSER_QA.json checks all184 inspectors, all event options, twelve government variants and complete prospective agreement sides. These are concept/model/browser checks, not HOI4 or multiplayer engine tests.

No runtime content is installed. Event pictures are not fabricated native screenshots; country-event frame composition remains after approval and requires current donor-window inspection. PREVIEW_PROVENANCE.json records embedded native art and screenshot provenance. Original individual artists and separate redistribution permission are unknown. Existing upstream rights remain separate. No new ownership is claimed by project markers.
