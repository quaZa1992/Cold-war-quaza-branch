# South Korea — native MD implementation recipes

**Approval-stage specifications. No COLDWAR_KOR runtime helper is claimed to exist yet.**

Civilian development uses civilian_factories_productivity, consumed in 00_money_system.txt:469 and6027 for civilian tax/GDP calculations. It is not a flat equal percentage increase in national GDP. Military factory output and production efficiency cap are retained only in the actual defence programme.

## Existing primitives and source evidence

- **change_ruling_party_effect:** common/scripted_effects/00_MD_politicsview_scripted_effects.txt:1980-2085; inputs rul_party_temp, disable_elections; optional col_one..col_five and change_leader_temp
- **money:** common/scripted_effects/00_budget_effects.txt:1484-1498; modify_treasury_effect requires treasury_change in billions
- **diplomatic_relation:** HOI4 documentation/effects_documentation.md:3564; MD common/national_focus/05_russia.txt:18890-18893 uses non_aggression_pact
- **construction:** HOI4 documentation/effects_documentation.md:839; native KOR paid projects; state scope plus current slots/ownership checked twice
- **dynamic:** HOI4 documentation/effects_documentation.md:4372; target generic/VIE/SOV ownership patterns

## Native political change contract

```hoi4
# Existing MD API; target and election settings supplied by the resolved political result.
set_temp_variable = { rul_party_temp = TARGET_SLOT }
set_temp_variable = { disable_elections = ELECTIONS_DISABLED }
change_ruling_party_effect = yes
# This existing helper calls set_leader; the NEW COLDWAR_KOR_1970_set_leader
# early dispatcher must therefore exist before integration. Never call the
# unmodified modern KOR pool and hope it chooses the proposed 1970 incumbent.
```

Existing common/scripted_effects/KOR_political_leaders.txt installs Kim Jong-pil under ruling_party=14. The proposed 1970 router must route him through actual DRP/NDRP slot0 and preserve NACF slot14; do not copy the modern slot14 office gate.

## New Korean providers to implement

- `COLDWAR_KOR_1970_set_leader`: New early country dispatcher inside set_leader. Respects actual selection, never rerolls Park at initialization. Pools: Park/KJP0, NDP1, both reform Kims2 with separate incumbent, Kim Chul3, RPR4, civic5, security7, independent left19, Chun/Roh22. Choi interim office gets its actual caretaker state before an election; it does not pretend to be a normal party victory.
- `COLDWAR_KOR_refresh_programmes`: New idempotent recomputation: reset sums, select latest earned policy per qualified slot, include only current actual owner and constitutional settlement, include signed active contract modifiers, update dynamic modifier once. No treasury, buildings, XP or PP writes. Explicitly remove inactive party/leader dynamic modifiers, retain earned variables and re-add only the returning active owner’s modifier. Enable guards are a second safeguard; the hook must detect exact-party changes within the same broad outlook.
- `COLDWAR_KOR_calculate_weekly_cost`: New single aggregation of active expense_commitment slots and accepted contract charges. Native calculate_additional_expense_rate calls this and adds its result to additional_expenses_rate; accepted recipient income uses a matching additional_income_rate reader. Never subtract cash directly on a monthly or GUI refresh.
- `COLDWAR_KOR_sync_politics`: New KOR hook from native exact-party change helper, KOR office dispatcher and on-load/monthly failsafe; calls refresh, does not set party or office itself. Also run the declared transition_maintenance_recipe to resume already funded court commissioning after constitutional restoration; never charge or appoint a ruler there.
- `COLDWAR_KOR_offer_dispatch`: New bounded offer sender with per-pair pending lock,60d deadline, sender office/country snapshot and no payment. Recipient options show each exact payer and benefit.
- `COLDWAR_KOR_offer_accept`: New revalidated transaction; charge and grant once, mark signed membership or relation and ledger receipt, clear pending, notify proposer. Existing NKO-side offers map to the same ledger.
- `COLDWAR_KOR_offer_refuse`: New final refusal/expiry receipt with no charge or agreement modifier; clear pending and start180d renegotiation cooldown; treaty-only follow-ups bypass without reward.

## Exceptional and civilian accession routes

### COLDWAR_KOR_legalize_civic_parties

Competitive civilian constitution OR a negotiated civilian opening; no nationwide martial law; existing lawful governing player authorizes legalization

Cost: 50 political power; 90d political adjustment: political power gain -5%

Record legal participation for student civic slot5 and independent left slot19. No automatic popularity or appointment. Actual native election/coalition result must put the party in office before its programme opens.

### COLDWAR_KOR_ratify_revolutionary_transition

A native resolved regime transition has actually selected slot4; or a legalized slot4 party wins through the existing political system. An underground network or Northern offer alone is insufficient.

Cost: 90d transition burden: stability -8%, factory output -5%; no industrial or diplomatic gift

Set revolutionary-settlement receipt, use native change_ruling_party_effect with target4 only after the actual transition; dispatch a historical Southern revolutionary cabinet from the new 1970 pool. Northern material support still requires a signed contract.

### COLDWAR_KOR_ratify_security_directorate

Unresolved presidential succession crisis; stability below30%; current government explicitly accepts a security caretaker; no existing civilian settlement ratification

Cost: 100 political power; stability -5%; 180d caretaker burden: trade opinion -5%, police expenses +5%

Set security-directorate receipt. Use native change_ruling_party_effect target7, elections disabled, existing actual support unchanged; create/select the new KCIA caretaker pool in the 1970 router. Party-array slot7 now actually governs. This is labelled alternate history and cannot trigger from coalition backing alone.

### COLDWAR_KOR_native_party_accession

Real native political result for slots0,1,2,3 or22

Cost: Native politics costs; no duplicate accession fee

Use current change_ruling_party_effect inputs; update actual incumbent and exact-party programmes. Preserve completed national development and party vote totals.

## Native examples

### nonaggression_accept

```hoi4
diplomatic_relation = { country = NKO relation = non_aggression_pact active = yes }
```

### national_policy_dynamic

```hoi4
COLDWAR_KOR_national_programme = { enable = { original_tag = KOR IMP_is_1970_scenario = yes } civilian_factories_productivity = COLDWAR_KOR_active_civ_productivity stability_factor = COLDWAR_KOR_active_stab }
```

### park_programme_dynamic

```hoi4
COLDWAR_KOR_park_programme = { enable = { original_tag = KOR check_variable = { ruling_party = 0 } has_country_leader = { name = "Park Chung Hee" ruling_only = yes } } political_power_factor = COLDWAR_KOR_park_pp stability_factor = COLDWAR_KOR_park_stab }
```

### modifier_refresh

```hoi4
add_dynamic_modifier = { modifier = COLDWAR_KOR_park_programme }
force_update_dynamic_modifier = yes
```

### weekly_reader_addition

```hoi4
COLDWAR_KOR_calculate_weekly_cost = yes
add_to_variable = { additional_expenses_rate = COLDWAR_KOR_weekly_cost }
```

## NKO agreement compatibility

- **existing_sources:** ['common/scripted_effects/COLDWAR_NKO_1970_foreign.txt:831-909', 'common/decisions/COLDWAR_NKO_1970_foreign.txt:238-248', 'common/dynamic_modifiers/COLDWAR_NKO_1970_foreign.txt:80-98']
- **existing_acceptance:** COLDWAR_NKO_korean_channel_confederation_offer_accepted must be present in both countries, not merely the offer-earned flag.
- **old_to_new:** Grandfather genuinely signed existing channels/frameworks into the shared ledger and add the zero-stat membership receipt. Preserve their already accepted native payments, modifiers and upkeep; no recharge, free refund or duplicated KOR bonus.
- **new_to_old:** NKO send/eligibility checks read shared pending/signature/membership OR genuine legacy acceptance. Do not manufacture the old acceptance flag on a new deal, because it can activate legacy reward consumers without their negotiated payment.
- **new_project:** A new secretariat or civilian-trade project requires a separate accepted numeric contract; it is additional scope, not a second award for the existing framework.
- **scope:** These are proposed narrowly scoped integration changes; no existing NKO agreement is altered during this concept phase.

## Legal accountability follow-up

{
  "id": "COLDWAR_KOR_review_repression_cases",
  "availability": "Competitive civilian settlement, independent court or oversight, no nationwide martial law",
  "cost": "75 political power and $1bn once",
  "effect": "Adjudicate cases and compensate victims. Reduce national martial-law legitimacy scar from stability -8%, trade opinion -5%, police expenses +8% to stability -3%, bureaucracy expenses +4%; no historical memory erasure.",
  "historicity": "Earlier independent accountability is alternate history; the1995\u201396 trials are not claimed to occur before1990."
}

## Shared transition providers, decisions and events

### Transition Receipt Providers

```json
{
  "COLDWAR_KOR_electoral_opening": {
    "provider": "COLDWAR_KOR_transition_1971 / Respect the Competitive Mandate",
    "guard": "A genuine1971 electoral contest or a separately authorized earlier constitutional contest, not mere party popularity",
    "effect": "set_country_flag = COLDWAR_KOR_electoral_opening"
  },
  "COLDWAR_KOR_caretaker_installed": {
    "provider": "COLDWAR_KOR_install_interim_choi",
    "guard": "Park has actually left office; civilian succession chosen; native office transition has installed Choi Kyu-hah",
    "native_effect": "set_temp_variable = { rul_party_temp = 0 }\nset_temp_variable = { disable_elections = 1 }\nset_country_flag = COLDWAR_KOR_select_interim_choi\nchange_ruling_party_effect = yes\nif = { limit = { has_country_leader = { name = \"Choi Kyu-hah\" ruling_only = yes } } set_country_flag = COLDWAR_KOR_caretaker_installed }",
    "router_note": "NEW1970 dispatcher consumes select_interim_choi before modern pools;0 is the existing governing parliamentary vehicle, not a claim Choi personally joined the DRP. Preserve party votes."
  },
  "COLDWAR_KOR_military_opening_authorized": {
    "provider": "COLDWAR_KOR_reopen_constitutional_talks / accepted1987 concession",
    "guard": "Actual military-led government accepts a negotiated opening after organized opposition pressure or a resolved command crisis",
    "effect": "set_country_flag = COLDWAR_KOR_military_opening_authorized"
  },
  "COLDWAR_KOR_negotiating_commitment": {
    "provider": "Bind the Incumbent OR Retirement Guarantees OR a successful command-challenge resolution",
    "effect": "set_country_flag = COLDWAR_KOR_negotiating_commitment"
  },
  "COLDWAR_KOR_lawful_election_completed": {
    "provider": "COLDWAR_KOR_on_native_election_resolved",
    "guard": "Native election/coalition result actually resolved under the ratified constitution and installed the resulting incumbent",
    "effect": "set_country_flag = COLDWAR_KOR_lawful_election_completed",
    "prohibition": "No focus, declaration, party popularity or coalition membership may set this receipt on its own."
  },
  "COLDWAR_KOR_conservative_merger_ratified": {
    "provider": "COLDWAR_KOR_transition_1990 / Ratify the Conservative Merger",
    "guard": "Actual participating DJP/RDP/NDRP organizations have authorized the bargain; earlier equivalents are alternate history. Kim Dae-jung’s organization is not included automatically.",
    "effect": "set_country_flag = COLDWAR_KOR_conservative_merger_ratified",
    "cleanup": "Clear on actual coalition dissolution. The earned programme can resume only with an actual re-ratified agreement; party change alone never manufactures one."
  },
  "COLDWAR_KOR_opposition_constitutional_demand": {
    "provider": "Actual1985 constitutional campaign or verified legal-opposition demand response",
    "guard": "Legal opposition party exists and has explicitly accepted the constitutional-demand campaign; no date-only automatic demand",
    "effect": "set_country_flag = COLDWAR_KOR_opposition_constitutional_demand"
  },
  "COLDWAR_KOR_court_appointments_implemented": {
    "provider": "COLDWAR_KOR_implement_constitutional_court",
    "guard": "Enacted court mandate, actual nomination/confirmation settlement and paid implementation",
    "effect": "See the once-only decision; focus completion alone never grants this receipt"
  }
}
```

### Transition Decisions

```json
[
  {
    "id": "COLDWAR_KOR_reopen_constitutional_talks",
    "repeatable": true,
    "available": "original_tag = KOR\nIMP_is_1970_scenario = yes\ncheck_variable = { ruling_party = 22 }\nhas_country_flag = COLDWAR_KOR_military_reconsolidation\nhas_country_flag = COLDWAR_KOR_opposition_constitutional_demand\nNOT = { has_country_flag = COLDWAR_KOR_constitutional_order }\nNOT = { has_country_flag = COLDWAR_KOR_military_opening_authorized }\nNOT = { has_country_flag = COLDWAR_KOR_transition_open }\nNOT = { has_country_flag = COLDWAR_KOR_talks_authorized }\nNOT = { has_country_flag = COLDWAR_KOR_talks_retry_cooldown }",
    "additional_guard": "The actual military-led government chooses this authorization. A legal opposition demand must be registered by the1985 constitutional campaign or equivalent verified opposition response.",
    "cost": "75PP; no automatic appointment or popularity",
    "effect": "add_political_power = -75\nset_country_flag = COLDWAR_KOR_military_opening_authorized\nclr_country_flag = COLDWAR_KOR_military_reconsolidation\nset_country_flag = { flag = COLDWAR_KOR_talks_retry_cooldown days = 90 }",
    "reader": "Enables Negotiated Withdrawal after a failed caretaker/command window without resetting any completed focus."
  },
  {
    "id": "COLDWAR_KOR_reopen_charter_ballot",
    "repeatable": true,
    "available": "original_tag = KOR\nIMP_is_1970_scenario = yes\nhas_country_flag = COLDWAR_KOR_charter_rejected\nhas_country_flag = COLDWAR_KOR_talks_authorized\nhas_country_flag = COLDWAR_KOR_charter_mandate\nNOT = { has_country_flag = COLDWAR_KOR_constitutional_order }\nNOT = { has_country_flag = COLDWAR_KOR_ballot_pending }\nNOT = { has_country_flag = COLDWAR_KOR_charter_retry_cooldown }\ncheck_variable = { COLDWAR_KOR_charter_model > 0 }",
    "cost": "50PP;90d after rejection; same chosen constitutional model",
    "effect": "add_political_power = -50\nclr_country_flag = COLDWAR_KOR_charter_rejected\nset_country_flag = COLDWAR_KOR_ballot_pending\ncountry_event = { id = COLDWAR_KOR_transition.30 days = 30 }",
    "reader": "The decision itself reopens the ballot; the one-shot Submit the Charter focus remains completed. No new model, focus reward or building is granted."
  },
  {
    "id": "COLDWAR_KOR_register_charter_endorsement",
    "repeatable": true,
    "available": "has_country_flag = COLDWAR_KOR_talks_authorized\nNOT = { has_country_flag = COLDWAR_KOR_ballot_pending }",
    "cost": "No new monetary fee; the party representative must accept the recorded negotiated terms",
    "effect": "For one actual eligible party slot s, set COLDWAR_KOR_charter_supporter_s only after that party’s endorsement response. No free support; a withdrawal clears the same receipt.",
    "reader": "The ballot helper checks this unique per-slot endorsement against current eligible native support. Power blocs are not automatically electoral parties."
  },
  {
    "id": "COLDWAR_KOR_implement_constitutional_court",
    "repeatable": false,
    "available": "original_tag = KOR\nIMP_is_1970_scenario = yes\nhas_country_flag = COLDWAR_KOR_constitutional_order\nhas_country_flag = COLDWAR_KOR_judicial_review\nNOT = { has_country_flag = COLDWAR_KOR_court_appointments_implemented }\nNOT = { has_country_flag = COLDWAR_KOR_court_implementation_pending }\nNOT = { has_country_flag = COLDWAR_KOR_judicial_review_operational }",
    "cost": "50PP and $1bn once;90d funded implementation",
    "effect": "add_political_power = -50\nset_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nset_country_flag = COLDWAR_KOR_court_implementation_pending\nset_country_flag = COLDWAR_KOR_court_appointments_implemented\nset_country_flag = { flag = COLDWAR_KOR_court_commissioning_delay days = 90 }\ncountry_event = { id = COLDWAR_KOR_transition.88 days = 90 }",
    "reader": "Appointments follow the enacted constitution and its nomination/confirmation rules. The event rechecks constitutional order. Interruption suspends operation without refund or repeat payment; restoration resumes the already funded process."
  }
]
```

### Proposed Transition Events

```json
{
  "COLDWAR_KOR_transition.12": {
    "trigger": "has_country_flag = COLDWAR_KOR_command_settlement_pending",
    "success": "Set negotiating_commitment; clear command_settlement_pending; legitimate civilian command continues.",
    "failure": "Set military_reconsolidation and90d talks_retry_cooldown; clear command_settlement_pending, negotiating_commitment and caretaker_installed; record command burden. A separate actual office event installs a military president; reopening requires the actual military-led government and registered opposition demand.",
    "success_option_guard": "has_country_flag = COLDWAR_KOR_caretaker_installed\nNOT = { has_country_flag = COLDWAR_KOR_nationwide_martial_law }",
    "success_native": "add_political_power = -75\nset_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes\nadd_timed_idea = { idea = COLDWAR_KOR_command_reorganization days = 90 }\nset_country_flag = COLDWAR_KOR_negotiating_commitment\nclr_country_flag = COLDWAR_KOR_command_settlement_pending",
    "failure_native": "add_political_power = -25\nset_country_flag = COLDWAR_KOR_military_reconsolidation\nset_country_flag = { flag = COLDWAR_KOR_talks_retry_cooldown days = 90 }\nclr_country_flag = COLDWAR_KOR_command_settlement_pending\nclr_country_flag = COLDWAR_KOR_negotiating_commitment\nclr_country_flag = COLDWAR_KOR_caretaker_installed\nclr_country_flag = COLDWAR_KOR_transition_open\nclr_country_flag = COLDWAR_KOR_military_opening_authorized",
    "success_cost": "75PP and $1bn once;90d command reorganization: army organization -5%, political power gain -5%. No new president is installed.",
    "resolution_mode": "Player-facing internal command-resolution event. Reorganize and Uphold Civil Command purchases a costly alternate outcome under the actual caretaker; Yield the Command records failure. These options resolve the challenge itself. No hidden dice, external success receipt or invented command meter is assumed."
  },
  "COLDWAR_KOR_transition.30": {
    "trigger": "has_country_flag = COLDWAR_KOR_ballot_pending\nhas_country_flag = COLDWAR_KOR_charter_mandate\ncheck_variable = { COLDWAR_KOR_charter_model > 0 }\ncheck_variable = { COLDWAR_KOR_charter_model < 4 }",
    "immediate": "Run NEW COLDWAR_KOR_calculate_charter_vote using the exact native calculation in ratification.native_calculation.",
    "pass_guard": "check_variable = { COLDWAR_KOR_charter_support_share > 0.5 }",
    "pass": "Set constitutional_ratification_passed and the selected model’s constitution receipt; clear pending/rejected. No incumbent appointment. Election-board implementation remains required.",
    "reject": "Clear ballot_pending; set charter_rejected and a90d charter_retry_cooldown; retain chosen model. No constitutional modifiers or election grant. Resubmit only through reopen_charter_ballot.",
    "pass_native": "set_country_flag = COLDWAR_KOR_constitutional_ratification_passed\nclr_country_flag = COLDWAR_KOR_ballot_pending\nclr_country_flag = COLDWAR_KOR_charter_rejected\nif = { limit = { check_variable = { COLDWAR_KOR_charter_model = 1 } } set_country_flag = COLDWAR_KOR_constitution_presidential }\nif = { limit = { check_variable = { COLDWAR_KOR_charter_model = 2 } } set_country_flag = COLDWAR_KOR_constitution_parliamentary }\nif = { limit = { check_variable = { COLDWAR_KOR_charter_model = 3 } } set_country_flag = COLDWAR_KOR_constitution_consensus }",
    "reject_native": "clr_country_flag = COLDWAR_KOR_ballot_pending\nset_country_flag = COLDWAR_KOR_charter_rejected\nset_country_flag = { flag = COLDWAR_KOR_charter_retry_cooldown days = 90 }",
    "implementation": "After the immediate calculation, execute one guarded pass/reject branch once. This is an adjudicated support model, not a player option that can choose passage against the result."
  },
  "COLDWAR_KOR_transition.88": {
    "trigger": "has_country_flag = COLDWAR_KOR_judicial_review\nhas_country_flag = COLDWAR_KOR_constitutional_order\nhas_country_flag = COLDWAR_KOR_court_appointments_implemented\nhas_country_flag = COLDWAR_KOR_court_implementation_pending\nNOT = { has_country_flag = COLDWAR_KOR_court_commissioning_delay }",
    "effect": "set_country_flag = COLDWAR_KOR_judicial_review_operational\nclr_country_flag = COLDWAR_KOR_court_implementation_pending",
    "historicity": "The constitutional creation in1987 and operational court in1988 are distinct. An earlier alternative still needs appointments/implementation; no automatic court operational at draft approval."
  }
}
```

### Transition Maintenance Recipe

```json
"if = { limit = { has_country_flag = COLDWAR_KOR_constitutional_order has_country_flag = COLDWAR_KOR_judicial_review has_country_flag = COLDWAR_KOR_court_appointments_implemented has_country_flag = COLDWAR_KOR_court_implementation_pending NOT = { has_country_flag = COLDWAR_KOR_court_commissioning_delay } } country_event = { id = COLDWAR_KOR_transition.88 days = 1 } }"
```

### Transition Maintenance Note

```json
"Run from the monthly KOR synchronization and constitutional restoration hook. This resumes an already funded, matured court commissioning after emergency interruption; the cleared pending receipt prevents repeated operation or payment."
```


## Per-focus native guards and leaves

These country-scope bodies supplement exact grouped prerequisites and reciprocal exclusions in the JSON. Leaf variable assignments require the declared latest-slot selector and mapped dynamic modifiers. Additional semantic requirements remain explicit; this is not ready-to-install generated game code.

### COLDWAR_KOR_developmental_state

```hoi4
COLDWAR_KOR_can_developmental_state = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = 50
set_variable = { COLDWAR_KOR_developmental_state_mandate_production_speed_buildings_factor = 0.04 }
set_variable = { COLDWAR_KOR_developmental_state_mandate_stability_factor = -0.03 }
```

### COLDWAR_KOR_yushin

```hoi4
COLDWAR_KOR_can_yushin = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
has_country_flag = COLDWAR_KOR_constitutional_crisis
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_yushin_constitution_political_power_factor = 0.18 }
set_variable = { COLDWAR_KOR_yushin_constitution_stability_factor = -0.08 }
set_variable = { COLDWAR_KOR_yushin_constitution_trade_opinion_factor = -0.05 }
```

### COLDWAR_KOR_constitutional_drp

```hoi4
COLDWAR_KOR_can_constitutional_drp = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_constitutional_drp_constitution_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_constitutional_drp_constitution_political_power_factor = -0.08 }
```

### COLDWAR_KOR_emergency_decrees

```hoi4
COLDWAR_KOR_can_emergency_decrees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
has_country_flag = COLDWAR_KOR_constitution_yushin
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_emergency_decrees_constitution_political_power_factor = 0.23 }
set_variable = { COLDWAR_KOR_emergency_decrees_constitution_stability_factor = -0.1 }
set_variable = { COLDWAR_KOR_emergency_decrees_constitution_police_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_emergency_decrees_constitution_trade_opinion_factor = -0.05 }
```

### COLDWAR_KOR_assembly_bargain

```hoi4
COLDWAR_KOR_can_assembly_bargain = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_assembly_bargain_constitution_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_assembly_bargain_constitution_political_power_factor = -0.1 }
set_variable = { COLDWAR_KOR_assembly_bargain_constitution_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_presidential_administration

```hoi4
COLDWAR_KOR_can_presidential_administration = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_presidential_administration_cabinet_production_speed_buildings_factor = 0.04 }
set_variable = { COLDWAR_KOR_presidential_administration_cabinet_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_chaebol_compact

```hoi4
COLDWAR_KOR_can_chaebol_compact = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_chaebol_compact_credit_interest_rate_multiplier_modifier = 0.35 }
set_variable = { COLDWAR_KOR_chaebol_compact_credit_civilian_factories_productivity = 0.06 }
```

### COLDWAR_KOR_competitive_credit

```hoi4
COLDWAR_KOR_can_competitive_credit = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_competitive_credit_credit_production_speed_industrial_complex_factor = 0.08 }
set_variable = { COLDWAR_KOR_competitive_credit_credit_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_competitive_credit_credit_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_export_targets

```hoi4
COLDWAR_KOR_can_export_targets = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_export_targets_credit_interest_rate_multiplier_modifier = 0.45 }
set_variable = { COLDWAR_KOR_export_targets_credit_stability_factor = -0.03 }
set_variable = { COLDWAR_KOR_export_targets_credit_civilian_factories_productivity = 0.12 }
```

### COLDWAR_KOR_subcontractor_guarantees

```hoi4
COLDWAR_KOR_can_subcontractor_guarantees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_subcontractor_guarantees_credit_production_speed_industrial_complex_factor = 0.1 }
set_variable = { COLDWAR_KOR_subcontractor_guarantees_credit_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_subcontractor_guarantees_credit_bureaucracy_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_subcontractor_guarantees_credit_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_planning_board

```hoi4
COLDWAR_KOR_can_planning_board = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_planning_board_planning_production_speed_buildings_factor = 0.03 }
set_variable = { COLDWAR_KOR_planning_board_planning_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_mobilized_villages

```hoi4
COLDWAR_KOR_can_mobilized_villages = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_mobilized_villages_rural_agricolture_productivity_modifier = 0.08 }
set_variable = { COLDWAR_KOR_mobilized_villages_rural_political_power_factor = 0.04 }
set_variable = { COLDWAR_KOR_mobilized_villages_rural_stability_factor = -0.02 }
```

### COLDWAR_KOR_rural_cooperatives

```hoi4
COLDWAR_KOR_can_rural_cooperatives = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_rural_cooperatives_rural_agricolture_productivity_modifier = 0.07 }
set_variable = { COLDWAR_KOR_rural_cooperatives_rural_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_rural_cooperatives_rural_political_power_factor = -0.04 }
```

### COLDWAR_KOR_performance_grants

```hoi4
COLDWAR_KOR_can_performance_grants = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_performance_grants_rural_agricolture_productivity_modifier = 0.12 }
set_variable = { COLDWAR_KOR_performance_grants_rural_political_power_factor = 0.04 }
set_variable = { COLDWAR_KOR_performance_grants_rural_stability_factor = -0.03 }
```

### COLDWAR_KOR_village_accounts

```hoi4
COLDWAR_KOR_can_village_accounts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_village_accounts_rural_agricolture_productivity_modifier = 0.09 }
set_variable = { COLDWAR_KOR_village_accounts_rural_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_village_accounts_rural_political_power_factor = -0.05 }
set_variable = { COLDWAR_KOR_village_accounts_rural_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_balanced_provinces

```hoi4
COLDWAR_KOR_can_balanced_provinces = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
607 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
607 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
```

### COLDWAR_KOR_dynastic_presidency

```hoi4
COLDWAR_KOR_can_dynastic_presidency = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
has_country_flag = COLDWAR_KOR_constitution_yushin
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_dynastic_presidency_succession_political_power_factor = 0.12 }
set_variable = { COLDWAR_KOR_dynastic_presidency_succession_stability_factor = -0.05 }
```

### COLDWAR_KOR_civilian_handover

```hoi4
COLDWAR_KOR_can_civilian_handover = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_handover_succession_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_civilian_handover_succession_political_power_factor = -0.08 }
```

### COLDWAR_KOR_parliamentary_government

```hoi4
COLDWAR_KOR_can_parliamentary_government = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_parliamentary_government_mandate_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_parliamentary_government_mandate_political_power_factor = -0.05 }
```

### COLDWAR_KOR_parliamentary_republic

```hoi4
COLDWAR_KOR_can_parliamentary_republic = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_parliamentary_republic_constitution_stability_factor = 0.07 }
set_variable = { COLDWAR_KOR_parliamentary_republic_constitution_political_power_factor = -0.1 }
```

### COLDWAR_KOR_checked_presidency

```hoi4
COLDWAR_KOR_can_checked_presidency = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_checked_presidency_constitution_political_power_factor = 0.06 }
set_variable = { COLDWAR_KOR_checked_presidency_constitution_stability_factor = 0.02 }
```

### COLDWAR_KOR_coalition_committees

```hoi4
COLDWAR_KOR_can_coalition_committees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_coalition_committees_constitution_stability_factor = 0.09 }
set_variable = { COLDWAR_KOR_coalition_committees_constitution_political_power_factor = -0.12 }
set_variable = { COLDWAR_KOR_coalition_committees_constitution_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_constitutional_court

```hoi4
COLDWAR_KOR_can_constitutional_court = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_constitutional_court_constitution_political_power_factor = 0.04 }
set_variable = { COLDWAR_KOR_constitutional_court_constitution_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_constitutional_court_constitution_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_civil_service_review

```hoi4
COLDWAR_KOR_can_civil_service_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_civil_service_review_service_bureaucracy_cost_multiplier_modifier = -0.04 }
set_variable = { COLDWAR_KOR_civil_service_review_service_political_power_factor = -0.03 }
```

### COLDWAR_KOR_market_conservatives

```hoi4
COLDWAR_KOR_can_market_conservatives = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_market_conservatives_enterprise_interest_rate_multiplier_modifier = -0.35 }
set_variable = { COLDWAR_KOR_market_conservatives_enterprise_production_speed_industrial_complex_factor = 0.06 }
set_variable = { COLDWAR_KOR_market_conservatives_enterprise_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_social_conservatives

```hoi4
COLDWAR_KOR_can_social_conservatives = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_social_conservatives_enterprise_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_social_conservatives_enterprise_social_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_social_conservatives_enterprise_civilian_factories_productivity = 0.03 }
```

### COLDWAR_KOR_open_tenders

```hoi4
COLDWAR_KOR_can_open_tenders = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_open_tenders_enterprise_interest_rate_multiplier_modifier = -0.4 }
set_variable = { COLDWAR_KOR_open_tenders_enterprise_production_speed_industrial_complex_factor = 0.09 }
set_variable = { COLDWAR_KOR_open_tenders_enterprise_bureaucracy_cost_multiplier_modifier = 0.03 }
set_variable = { COLDWAR_KOR_open_tenders_enterprise_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_pension_contributions

```hoi4
COLDWAR_KOR_can_pension_contributions = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_pension_contributions_enterprise_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_pension_contributions_enterprise_social_cost_multiplier_modifier = 0.1 }
set_variable = { COLDWAR_KOR_pension_contributions_enterprise_consumer_goods_factor = 0.01 }
set_variable = { COLDWAR_KOR_pension_contributions_enterprise_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_regional_compromise

```hoi4
COLDWAR_KOR_can_regional_compromise = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
607 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
607 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
```

### COLDWAR_KOR_civilian_security

```hoi4
COLDWAR_KOR_can_civilian_security = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_security_security_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_civilian_security_security_intel_network_gain_factor = -0.04 }
```

### COLDWAR_KOR_security_compromise

```hoi4
COLDWAR_KOR_can_security_compromise = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_compromise_security_intel_network_gain_factor = 0.08 }
set_variable = { COLDWAR_KOR_security_compromise_security_stability_factor = -0.04 }
set_variable = { COLDWAR_KOR_security_compromise_security_police_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_democratic_conservatism

```hoi4
COLDWAR_KOR_can_democratic_conservatism = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_democratic_conservatism_settlement_trade_opinion_factor = 0.08 }
set_variable = { COLDWAR_KOR_democratic_conservatism_settlement_political_power_factor = -0.04 }
```

### COLDWAR_KOR_reform_mandate

```hoi4
COLDWAR_KOR_can_reform_mandate = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_reform_mandate_mandate_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_reform_mandate_mandate_political_power_factor = -0.05 }
```

### COLDWAR_KOR_ys_civilian_authority

```hoi4
COLDWAR_KOR_can_ys_civilian_authority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_ys_civilian_authority_ys_base_political_power_factor = 0.06 }
set_variable = { COLDWAR_KOR_ys_civilian_authority_ys_base_army_org_factor = -0.03 }
```

### COLDWAR_KOR_dj_people_economy

```hoi4
COLDWAR_KOR_can_dj_people_economy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_dj_people_economy_dj_base_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_dj_people_economy_dj_base_social_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_financial_disclosure

```hoi4
COLDWAR_KOR_can_financial_disclosure = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_financial_disclosure_ys_finance_interest_rate_multiplier_modifier = -0.4 }
set_variable = { COLDWAR_KOR_financial_disclosure_ys_finance_political_power_factor = -0.05 }
```

### COLDWAR_KOR_negotiated_cleanup

```hoi4
COLDWAR_KOR_can_negotiated_cleanup = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_negotiated_cleanup_ys_finance_production_speed_buildings_factor = 0.06 }
set_variable = { COLDWAR_KOR_negotiated_cleanup_ys_finance_interest_rate_multiplier_modifier = 0.2 }
```

### COLDWAR_KOR_real_name_accounts

```hoi4
COLDWAR_KOR_can_real_name_accounts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_real_name_accounts_ys_finance_interest_rate_multiplier_modifier = -0.55 }
set_variable = { COLDWAR_KOR_real_name_accounts_ys_finance_political_power_factor = -0.07 }
set_variable = { COLDWAR_KOR_real_name_accounts_ys_finance_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_corporate_transition

```hoi4
COLDWAR_KOR_can_corporate_transition = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_corporate_transition_ys_finance_production_speed_buildings_factor = 0.08 }
set_variable = { COLDWAR_KOR_corporate_transition_ys_finance_interest_rate_multiplier_modifier = 0.25 }
set_variable = { COLDWAR_KOR_corporate_transition_ys_finance_stability_factor = -0.02 }
```

### COLDWAR_KOR_ys_civil_coalition

```hoi4
COLDWAR_KOR_can_ys_civil_coalition = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_ys_civil_coalition_ys_coalition_trade_opinion_factor = 0.06 }
set_variable = { COLDWAR_KOR_ys_civil_coalition_ys_coalition_political_power_factor = -0.03 }
```

### COLDWAR_KOR_ys_consolidation

```hoi4
COLDWAR_KOR_can_ys_consolidation = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_ys_consolidation_ys_consolidation_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_ys_consolidation_ys_consolidation_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_broad_welfare

```hoi4
COLDWAR_KOR_can_broad_welfare = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_broad_welfare_dj_welfare_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_broad_welfare_dj_welfare_social_cost_multiplier_modifier = 0.15 }
```

### COLDWAR_KOR_targeted_welfare

```hoi4
COLDWAR_KOR_can_targeted_welfare = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_targeted_welfare_dj_welfare_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_targeted_welfare_dj_welfare_bureaucracy_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_targeted_welfare_dj_welfare_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_national_health_cover

```hoi4
COLDWAR_KOR_can_national_health_cover = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_national_health_cover_dj_welfare_stability_factor = 0.1 }
set_variable = { COLDWAR_KOR_national_health_cover_dj_welfare_social_cost_multiplier_modifier = 0.15 }
set_variable = { COLDWAR_KOR_national_health_cover_dj_welfare_health_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_regional_equalization

```hoi4
COLDWAR_KOR_can_regional_equalization = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_regional_equalization_dj_welfare_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_regional_equalization_dj_welfare_bureaucracy_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_regional_equalization_dj_welfare_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_dj_civil_coalition

```hoi4
COLDWAR_KOR_can_dj_civil_coalition = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_dj_civil_coalition_dj_coalition_trade_opinion_factor = 0.06 }
set_variable = { COLDWAR_KOR_dj_civil_coalition_dj_coalition_political_power_factor = -0.03 }
```

### COLDWAR_KOR_dj_consolidation

```hoi4
COLDWAR_KOR_can_dj_consolidation = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_dj_consolidation_dj_consolidation_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_dj_consolidation_dj_consolidation_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_sixth_republic

```hoi4
COLDWAR_KOR_can_sixth_republic = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_sixth_republic_republic_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_sixth_republic_republic_political_power_factor = -0.04 }
```

### COLDWAR_KOR_democratic_alliance

```hoi4
COLDWAR_KOR_can_democratic_alliance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_democratic_alliance_foreign_trade_opinion_factor = 0.1 }
set_variable = { COLDWAR_KOR_democratic_alliance_foreign_foreign_influence_defense_modifier = -0.05 }
```

### COLDWAR_KOR_reform_nordpolitik

```hoi4
COLDWAR_KOR_can_reform_nordpolitik = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_reform_nordpolitik_foreign_trade_opinion_factor = 0.06 }
set_variable = { COLDWAR_KOR_reform_nordpolitik_foreign_foreign_influence_defense_modifier = 0.06 }
set_variable = { COLDWAR_KOR_reform_nordpolitik_foreign_political_power_factor = -0.06 }
```

### COLDWAR_KOR_military_cabinet

```hoi4
COLDWAR_KOR_can_military_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
army_experience = 15
set_variable = { COLDWAR_KOR_military_cabinet_mandate_army_org_factor = 0.05 }
set_variable = { COLDWAR_KOR_military_cabinet_mandate_stability_factor = -0.05 }
```

### COLDWAR_KOR_fifth_republic

```hoi4
COLDWAR_KOR_can_fifth_republic = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
has_country_leader = { name = "Chun Doo-hwan" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_fifth_republic_constitution_political_power_factor = 0.15 }
set_variable = { COLDWAR_KOR_fifth_republic_constitution_stability_factor = -0.07 }
set_variable = { COLDWAR_KOR_fifth_republic_constitution_police_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_managed_liberalization

```hoi4
COLDWAR_KOR_can_managed_liberalization = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_managed_liberalization_constitution_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_managed_liberalization_constitution_political_power_factor = -0.07 }
```

### COLDWAR_KOR_press_consolidation

```hoi4
COLDWAR_KOR_can_press_consolidation = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
has_country_leader = { name = "Chun Doo-hwan" ruling_only = yes }
has_country_flag = COLDWAR_KOR_constitution_controlled_fifth
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_press_consolidation_constitution_political_power_factor = 0.19 }
set_variable = { COLDWAR_KOR_press_consolidation_constitution_stability_factor = -0.09 }
set_variable = { COLDWAR_KOR_press_consolidation_constitution_police_cost_multiplier_modifier = 0.1 }
set_variable = { COLDWAR_KOR_press_consolidation_constitution_trade_opinion_factor = -0.04 }
```

### COLDWAR_KOR_june_declaration

```hoi4
COLDWAR_KOR_can_june_declaration = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_june_declaration_constitution_stability_factor = 0.1 }
set_variable = { COLDWAR_KOR_june_declaration_constitution_political_power_factor = -0.1 }
```

### COLDWAR_KOR_professional_officers

```hoi4
COLDWAR_KOR_can_professional_officers = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_professional_officers_officers_army_org_factor = 0.04 }
set_variable = { COLDWAR_KOR_professional_officers_officers_personnel_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_stabilization_first

```hoi4
COLDWAR_KOR_can_stabilization_first = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_stabilization_first_stabilize_interest_rate_multiplier_modifier = -0.6 }
set_variable = { COLDWAR_KOR_stabilization_first_stabilize_stability_factor = -0.02 }
set_variable = { COLDWAR_KOR_stabilization_first_stabilize_civilian_factories_productivity = -0.04 }
```

### COLDWAR_KOR_industrial_continuity

```hoi4
COLDWAR_KOR_can_industrial_continuity = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_industrial_continuity_stabilize_interest_rate_multiplier_modifier = 0.45 }
set_variable = { COLDWAR_KOR_industrial_continuity_stabilize_civilian_factories_productivity = 0.07 }
```

### COLDWAR_KOR_industrial_rationalization

```hoi4
COLDWAR_KOR_can_industrial_rationalization = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_industrial_rationalization_stabilize_interest_rate_multiplier_modifier = -0.7 }
set_variable = { COLDWAR_KOR_industrial_rationalization_stabilize_civilian_factories_productivity = 0.03 }
```

### COLDWAR_KOR_export_recovery

```hoi4
COLDWAR_KOR_can_export_recovery = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_export_recovery_stabilize_interest_rate_multiplier_modifier = 0.5 }
set_variable = { COLDWAR_KOR_export_recovery_stabilize_stability_factor = -0.03 }
set_variable = { COLDWAR_KOR_export_recovery_stabilize_civilian_factories_productivity = 0.1 }
```

### COLDWAR_KOR_civil_administration

```hoi4
COLDWAR_KOR_can_civil_administration = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_civil_administration_administration_bureaucracy_cost_multiplier_modifier = -0.04 }
set_variable = { COLDWAR_KOR_civil_administration_administration_political_power_factor = -0.03 }
```

### COLDWAR_KOR_hanahoe_compact

```hoi4
COLDWAR_KOR_can_hanahoe_compact = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_hanahoe_compact_command_army_org_factor = 0.06 }
set_variable = { COLDWAR_KOR_hanahoe_compact_command_political_power_factor = 0.04 }
set_variable = { COLDWAR_KOR_hanahoe_compact_command_stability_factor = -0.05 }
```

### COLDWAR_KOR_retire_political_officers

```hoi4
COLDWAR_KOR_can_retire_political_officers = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_retire_political_officers_command_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_retire_political_officers_command_army_org_factor = -0.03 }
```

### COLDWAR_KOR_security_continuity

```hoi4
COLDWAR_KOR_can_security_continuity = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_continuity_command_army_org_factor = 0.08 }
set_variable = { COLDWAR_KOR_security_continuity_command_intel_network_gain_factor = 0.06 }
set_variable = { COLDWAR_KOR_security_continuity_command_stability_factor = -0.07 }
set_variable = { COLDWAR_KOR_security_continuity_command_police_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_civilian_promotions

```hoi4
COLDWAR_KOR_can_civilian_promotions = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_promotions_command_stability_factor = 0.09 }
set_variable = { COLDWAR_KOR_civilian_promotions_command_army_org_factor = -0.02 }
set_variable = { COLDWAR_KOR_civilian_promotions_command_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_olympic_republic

```hoi4
COLDWAR_KOR_can_olympic_republic = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_olympic_republic_opening_trade_opinion_factor = 0.08 }
set_variable = { COLDWAR_KOR_olympic_republic_opening_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_roh_nordpolitik

```hoi4
COLDWAR_KOR_can_roh_nordpolitik = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
has_country_leader = { name = "Roh Tae-woo" ruling_only = yes }
has_elections = yes
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_roh_nordpolitik_nordpolitik_trade_opinion_factor = 0.1 }
set_variable = { COLDWAR_KOR_roh_nordpolitik_nordpolitik_political_power_factor = -0.06 }
```

### COLDWAR_KOR_conservative_merger

```hoi4
COLDWAR_KOR_can_conservative_merger = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_conservative_merger_coalition_political_power_factor = 0.12 }
set_variable = { COLDWAR_KOR_conservative_merger_coalition_stability_factor = -0.04 }
```

### COLDWAR_KOR_social_democratic_cabinet

```hoi4
COLDWAR_KOR_can_social_democratic_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_social_democratic_cabinet_mandate_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_social_democratic_cabinet_mandate_social_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_universal_insurance

```hoi4
COLDWAR_KOR_can_universal_insurance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_universal_insurance_welfare_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_universal_insurance_welfare_social_cost_multiplier_modifier = 0.16 }
```

### COLDWAR_KOR_contributory_welfare

```hoi4
COLDWAR_KOR_can_contributory_welfare = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_contributory_welfare_welfare_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_contributory_welfare_welfare_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_contributory_welfare_welfare_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_rural_health

```hoi4
COLDWAR_KOR_can_rural_health = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_rural_health_welfare_stability_factor = 0.1 }
set_variable = { COLDWAR_KOR_rural_health_welfare_social_cost_multiplier_modifier = 0.16 }
set_variable = { COLDWAR_KOR_rural_health_welfare_health_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_portable_benefits

```hoi4
COLDWAR_KOR_can_portable_benefits = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_portable_benefits_welfare_stability_factor = 0.07 }
set_variable = { COLDWAR_KOR_portable_benefits_welfare_bureaucracy_cost_multiplier_modifier = 0.07 }
set_variable = { COLDWAR_KOR_portable_benefits_welfare_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_independent_unions

```hoi4
COLDWAR_KOR_can_independent_unions = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_independent_unions_labour_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_independent_unions_labour_civilian_factories_productivity = -0.03 }
```

### COLDWAR_KOR_public_credit

```hoi4
COLDWAR_KOR_can_public_credit = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_public_credit_ownership_production_speed_industrial_complex_factor = 0.08 }
set_variable = { COLDWAR_KOR_public_credit_ownership_interest_rate_multiplier_modifier = 0.25 }
set_variable = { COLDWAR_KOR_public_credit_ownership_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_social_market_industry

```hoi4
COLDWAR_KOR_can_social_market_industry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_social_market_industry_ownership_social_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_social_market_industry_ownership_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_cooperative_industry

```hoi4
COLDWAR_KOR_can_cooperative_industry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_cooperative_industry_ownership_production_speed_industrial_complex_factor = 0.1 }
set_variable = { COLDWAR_KOR_cooperative_industry_ownership_interest_rate_multiplier_modifier = 0.3 }
set_variable = { COLDWAR_KOR_cooperative_industry_ownership_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_cooperative_industry_ownership_civilian_factories_productivity = 0.03 }
```

### COLDWAR_KOR_works_councils

```hoi4
COLDWAR_KOR_can_works_councils = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_works_councils_ownership_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_works_councils_ownership_social_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_works_councils_ownership_civilian_factories_productivity = 0.06 }
```

### COLDWAR_KOR_balanced_development

```hoi4
COLDWAR_KOR_can_balanced_development = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
607 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
607 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
```

### COLDWAR_KOR_socialist_alliance

```hoi4
COLDWAR_KOR_can_socialist_alliance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_socialist_alliance_external_foreign_influence_defense_modifier = 0.1 }
set_variable = { COLDWAR_KOR_socialist_alliance_external_trade_opinion_factor = -0.04 }
```

### COLDWAR_KOR_neutral_peace

```hoi4
COLDWAR_KOR_can_neutral_peace = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_neutral_peace_external_foreign_influence_defense_modifier = 0.06 }
set_variable = { COLDWAR_KOR_neutral_peace_external_army_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_neutral_peace_external_personnel_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_labour_republic

```hoi4
COLDWAR_KOR_can_labour_republic = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_labour_republic_settlement_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_labour_republic_settlement_political_power_factor = -0.05 }
```

### COLDWAR_KOR_student_cabinet

```hoi4
COLDWAR_KOR_can_student_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_student_cabinet_student_base_research_speed_factor = 0.03 }
set_variable = { COLDWAR_KOR_student_cabinet_student_base_political_power_factor = -0.07 }
```

### COLDWAR_KOR_campus_pluralism

```hoi4
COLDWAR_KOR_can_campus_pluralism = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_campus_pluralism_student_education_research_speed_factor = 0.05 }
set_variable = { COLDWAR_KOR_campus_pluralism_student_education_education_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_national_service_schools

```hoi4
COLDWAR_KOR_can_national_service_schools = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_national_service_schools_student_education_training_time_army_factor = -0.08 }
set_variable = { COLDWAR_KOR_national_service_schools_student_education_conscription_factor = 0.04 }
set_variable = { COLDWAR_KOR_national_service_schools_student_education_education_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_national_service_schools_student_education_political_power_factor = -0.05 }
```

### COLDWAR_KOR_technical_scholarships

```hoi4
COLDWAR_KOR_can_technical_scholarships = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_technical_scholarships_student_education_research_speed_factor = 0.07 }
set_variable = { COLDWAR_KOR_technical_scholarships_student_education_education_cost_multiplier_modifier = 0.1 }
```

### COLDWAR_KOR_community_service

```hoi4
COLDWAR_KOR_can_community_service = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_community_service_student_education_training_time_army_factor = -0.1 }
set_variable = { COLDWAR_KOR_community_service_student_education_conscription_factor = 0.06 }
set_variable = { COLDWAR_KOR_community_service_student_education_education_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_community_service_student_education_political_power_factor = -0.05 }
```

### COLDWAR_KOR_civic_charter

```hoi4
COLDWAR_KOR_can_civic_charter = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civic_charter_student_charter_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_civic_charter_student_charter_political_power_factor = -0.05 }
```

### COLDWAR_KOR_student_cabinet_public_accounts

```hoi4
COLDWAR_KOR_can_student_cabinet_public_accounts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_student_cabinet_public_accounts_student_cabinet_accounts_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_student_cabinet_public_accounts_student_cabinet_accounts_political_power_factor = -0.03 }
```

### COLDWAR_KOR_independent_left

```hoi4
COLDWAR_KOR_can_independent_left = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_independent_left_left_base_foreign_influence_defense_modifier = 0.08 }
set_variable = { COLDWAR_KOR_independent_left_left_base_trade_opinion_factor = -0.05 }
```

### COLDWAR_KOR_worker_management

```hoi4
COLDWAR_KOR_can_worker_management = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_worker_management_left_ownership_political_power_factor = -0.08 }
set_variable = { COLDWAR_KOR_worker_management_left_ownership_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_worker_management_left_ownership_civilian_factories_productivity = 0.07 }
```

### COLDWAR_KOR_strategic_public_sector

```hoi4
COLDWAR_KOR_can_strategic_public_sector = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_strategic_public_sector_left_ownership_interest_rate_multiplier_modifier = 0.3 }
set_variable = { COLDWAR_KOR_strategic_public_sector_left_ownership_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_strategic_public_sector_left_ownership_civilian_factories_productivity = 0.06 }
```

### COLDWAR_KOR_industrial_councils

```hoi4
COLDWAR_KOR_can_industrial_councils = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_industrial_councils_left_ownership_political_power_factor = -0.1 }
set_variable = { COLDWAR_KOR_industrial_councils_left_ownership_bureaucracy_cost_multiplier_modifier = 0.07 }
set_variable = { COLDWAR_KOR_industrial_councils_left_ownership_civilian_factories_productivity = 0.1 }
```

### COLDWAR_KOR_public_holding_fund

```hoi4
COLDWAR_KOR_can_public_holding_fund = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_public_holding_fund_left_ownership_interest_rate_multiplier_modifier = 0.4 }
set_variable = { COLDWAR_KOR_public_holding_fund_left_ownership_bureaucracy_cost_multiplier_modifier = 0.07 }
set_variable = { COLDWAR_KOR_public_holding_fund_left_ownership_civilian_factories_productivity = 0.09 }
```

### COLDWAR_KOR_southern_socialism

```hoi4
COLDWAR_KOR_can_southern_socialism = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_southern_socialism_left_charter_foreign_influence_defense_modifier = 0.08 }
set_variable = { COLDWAR_KOR_southern_socialism_left_charter_army_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_southern_socialism_left_charter_trade_opinion_factor = -0.04 }
```

### COLDWAR_KOR_independent_left_public_accounts

```hoi4
COLDWAR_KOR_can_independent_left_public_accounts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_independent_left_public_accounts_independent_left_accounts_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_independent_left_public_accounts_independent_left_accounts_political_power_factor = -0.03 }
```

### COLDWAR_KOR_revolutionary_cabinet

```hoi4
COLDWAR_KOR_can_revolutionary_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_revolutionary_cabinet_mandate_stability_factor = -0.08 }
set_variable = { COLDWAR_KOR_revolutionary_cabinet_mandate_trade_opinion_factor = -0.08 }
set_variable = { COLDWAR_KOR_revolutionary_cabinet_mandate_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_southern_front

```hoi4
COLDWAR_KOR_can_southern_front = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_southern_front_front_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_southern_front_front_political_power_factor = -0.08 }
set_variable = { COLDWAR_KOR_southern_front_front_foreign_influence_defense_modifier = 0.06 }
```

### COLDWAR_KOR_vanguard_party

```hoi4
COLDWAR_KOR_can_vanguard_party = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_vanguard_party_front_political_power_factor = 0.18 }
set_variable = { COLDWAR_KOR_vanguard_party_front_stability_factor = -0.07 }
set_variable = { COLDWAR_KOR_vanguard_party_front_police_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_pluralist_socialism

```hoi4
COLDWAR_KOR_can_pluralist_socialism = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_pluralist_socialism_front_stability_factor = 0.09 }
set_variable = { COLDWAR_KOR_pluralist_socialism_front_political_power_factor = -0.1 }
set_variable = { COLDWAR_KOR_pluralist_socialism_front_foreign_influence_defense_modifier = 0.06 }
```

### COLDWAR_KOR_party_cadres

```hoi4
COLDWAR_KOR_can_party_cadres = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_party_cadres_front_political_power_factor = 0.2 }
set_variable = { COLDWAR_KOR_party_cadres_front_stability_factor = -0.09 }
set_variable = { COLDWAR_KOR_party_cadres_front_police_cost_multiplier_modifier = 0.1 }
set_variable = { COLDWAR_KOR_party_cadres_front_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_revolutionary_reconstruction

```hoi4
COLDWAR_KOR_can_revolutionary_reconstruction = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_revolutionary_reconstruction_rebuild_interest_rate_multiplier_modifier = 0.35 }
```

### COLDWAR_KOR_confederal_revolution

```hoi4
COLDWAR_KOR_can_confederal_revolution = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_confederal_revolution_korea_foreign_influence_defense_modifier = 0.08 }
set_variable = { COLDWAR_KOR_confederal_revolution_korea_political_power_factor = -0.06 }
```

### COLDWAR_KOR_northern_alignment

```hoi4
COLDWAR_KOR_can_northern_alignment = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_northern_alignment_korea_army_org_factor = 0.06 }
set_variable = { COLDWAR_KOR_northern_alignment_korea_trade_opinion_factor = -0.1 }
set_variable = { COLDWAR_KOR_northern_alignment_korea_foreign_influence_defense_modifier = -0.08 }
```

### COLDWAR_KOR_southern_guarantees

```hoi4
COLDWAR_KOR_can_southern_guarantees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
has_country_flag = COLDWAR_KOR_sovereign_confederation_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_southern_guarantees_korea_foreign_influence_defense_modifier = 0.1 }
set_variable = { COLDWAR_KOR_southern_guarantees_korea_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_southern_guarantees_korea_political_power_factor = -0.08 }
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_confederal_revolution has_completed_focus = COLDWAR_KOR_sovereign_confederation }
NOT = { has_country_flag = COLDWAR_KOR_sovereign_confederation_signed }
OR = { has_country_flag = COLDWAR_KOR_sovereign_confederation_refused has_country_flag = COLDWAR_KOR_sovereign_confederation_expired }
}
```

### COLDWAR_KOR_joint_planning

```hoi4
COLDWAR_KOR_can_joint_planning = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
has_country_flag = COLDWAR_KOR_northern_security_compact_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_joint_planning_korea_trade_opinion_factor = -0.1 }
set_variable = { COLDWAR_KOR_joint_planning_korea_foreign_influence_defense_modifier = -0.1 }
set_variable = { COLDWAR_KOR_joint_planning_korea_civilian_factories_productivity = 0.08 }
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_northern_alignment }
NOT = { has_country_flag = COLDWAR_KOR_northern_security_compact_signed }
OR = { has_country_flag = COLDWAR_KOR_northern_security_compact_refused has_country_flag = COLDWAR_KOR_northern_security_compact_expired }
}
```

### COLDWAR_KOR_southern_settlement

```hoi4
COLDWAR_KOR_can_southern_settlement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_southern_settlement_settlement_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_southern_settlement_settlement_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_revolutionary_diplomacy

```hoi4
COLDWAR_KOR_can_revolutionary_diplomacy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_security_cabinet

```hoi4
COLDWAR_KOR_can_security_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_cabinet_mandate_intel_network_gain_factor = 0.08 }
set_variable = { COLDWAR_KOR_security_cabinet_mandate_stability_factor = -0.08 }
set_variable = { COLDWAR_KOR_security_cabinet_mandate_police_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_internal_directorate

```hoi4
COLDWAR_KOR_can_internal_directorate = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_internal_directorate_service_intel_network_gain_factor = 0.1 }
set_variable = { COLDWAR_KOR_internal_directorate_service_political_power_factor = 0.08 }
set_variable = { COLDWAR_KOR_internal_directorate_service_stability_factor = -0.08 }
set_variable = { COLDWAR_KOR_internal_directorate_service_police_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_external_service

```hoi4
COLDWAR_KOR_can_external_service = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_external_service_service_intel_network_gain_factor = 0.08 }
set_variable = { COLDWAR_KOR_external_service_service_encryption_factor = 0.05 }
set_variable = { COLDWAR_KOR_external_service_service_bureaucracy_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_national_files

```hoi4
COLDWAR_KOR_can_national_files = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_national_files_service_intel_network_gain_factor = 0.14 }
set_variable = { COLDWAR_KOR_national_files_service_political_power_factor = 0.1 }
set_variable = { COLDWAR_KOR_national_files_service_stability_factor = -0.1 }
set_variable = { COLDWAR_KOR_national_files_service_police_cost_multiplier_modifier = 0.1 }
```

### COLDWAR_KOR_warranted_operations

```hoi4
COLDWAR_KOR_can_warranted_operations = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_warranted_operations_service_intel_network_gain_factor = 0.1 }
set_variable = { COLDWAR_KOR_warranted_operations_service_encryption_factor = 0.08 }
set_variable = { COLDWAR_KOR_warranted_operations_service_bureaucracy_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_warranted_operations_service_political_power_factor = -0.04 }
```

### COLDWAR_KOR_counter_infiltration

```hoi4
COLDWAR_KOR_can_counter_infiltration = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_counter_infiltration_border_army_core_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_counter_infiltration_border_police_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_security_technocrats

```hoi4
COLDWAR_KOR_can_security_technocrats = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_technocrats_governance_production_speed_buildings_factor = 0.07 }
set_variable = { COLDWAR_KOR_security_technocrats_governance_stability_factor = -0.04 }
set_variable = { COLDWAR_KOR_security_technocrats_governance_interest_rate_multiplier_modifier = 0.2 }
```

### COLDWAR_KOR_civilian_exit

```hoi4
COLDWAR_KOR_can_civilian_exit = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_exit_governance_stability_factor = 0.07 }
set_variable = { COLDWAR_KOR_civilian_exit_governance_political_power_factor = -0.1 }
```

### COLDWAR_KOR_protected_planning

```hoi4
COLDWAR_KOR_can_protected_planning = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_protected_planning_governance_production_speed_buildings_factor = 0.1 }
set_variable = { COLDWAR_KOR_protected_planning_governance_stability_factor = -0.06 }
set_variable = { COLDWAR_KOR_protected_planning_governance_interest_rate_multiplier_modifier = 0.3 }
```

### COLDWAR_KOR_disclose_archives

```hoi4
COLDWAR_KOR_can_disclose_archives = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_disclose_archives_governance_stability_factor = 0.1 }
set_variable = { COLDWAR_KOR_disclose_archives_governance_political_power_factor = -0.12 }
set_variable = { COLDWAR_KOR_disclose_archives_governance_intel_network_gain_factor = -0.03 }
```

### COLDWAR_KOR_security_settlement

```hoi4
COLDWAR_KOR_can_security_settlement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_security_settlement_settlement_army_core_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_security_settlement_settlement_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_security_handover

```hoi4
COLDWAR_KOR_can_security_handover = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = 75
add_stability = -0.03
```

### COLDWAR_KOR_third_plan

```hoi4
COLDWAR_KOR_can_third_plan = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_third_plan_planning_production_speed_buildings_factor = 0.04 }
set_variable = { COLDWAR_KOR_third_plan_planning_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_heavy_chemical_drive

```hoi4
COLDWAR_KOR_can_heavy_chemical_drive = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_heavy_chemical_drive_industrial_model_interest_rate_multiplier_modifier = 0.4 }
set_variable = { COLDWAR_KOR_heavy_chemical_drive_industrial_model_civilian_factories_productivity = 0.09 }
```

### COLDWAR_KOR_light_export_model

```hoi4
COLDWAR_KOR_can_light_export_model = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_light_export_model_industrial_model_production_speed_industrial_complex_factor = 0.09 }
set_variable = { COLDWAR_KOR_light_export_model_industrial_model_buildings_worker_requirement_modifier = 0.03 }
set_variable = { COLDWAR_KOR_light_export_model_industrial_model_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_pohang_foundry

```hoi4
COLDWAR_KOR_can_pohang_foundry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
605 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
605 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_pohang_foundry_industrial_model_interest_rate_multiplier_modifier = 0.5 }
set_variable = { COLDWAR_KOR_pohang_foundry_industrial_model_civilian_factories_productivity = 0.12 }
```

### COLDWAR_KOR_provincial_export_zones

```hoi4
COLDWAR_KOR_can_provincial_export_zones = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_provincial_export_zones_industrial_model_production_speed_industrial_complex_factor = 0.11 }
set_variable = { COLDWAR_KOR_provincial_export_zones_industrial_model_buildings_worker_requirement_modifier = 0.04 }
set_variable = { COLDWAR_KOR_provincial_export_zones_industrial_model_civilian_factories_productivity = -0.02 }
```

### COLDWAR_KOR_freight_corridors

```hoi4
COLDWAR_KOR_can_freight_corridors = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
604 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
605 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
604 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
605 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
```

### COLDWAR_KOR_assembly_contracts

```hoi4
COLDWAR_KOR_can_assembly_contracts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_assembly_contracts_technology_foreign_influence_defense_modifier = -0.05 }
set_variable = { COLDWAR_KOR_assembly_contracts_technology_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_domestic_engineering

```hoi4
COLDWAR_KOR_can_domestic_engineering = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_domestic_engineering_technology_research_speed_factor = 0.04 }
set_variable = { COLDWAR_KOR_domestic_engineering_technology_education_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_technical_colleges

```hoi4
COLDWAR_KOR_can_technical_colleges = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_technical_colleges_technology_research_speed_factor = 0.02 }
set_variable = { COLDWAR_KOR_technical_colleges_technology_education_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_technical_colleges_technology_foreign_influence_defense_modifier = -0.05 }
set_variable = { COLDWAR_KOR_technical_colleges_technology_civilian_factories_productivity = 0.07 }
```

### COLDWAR_KOR_industrial_laboratories

```hoi4
COLDWAR_KOR_can_industrial_laboratories = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_industrial_laboratories_technology_research_speed_factor = 0.06 }
set_variable = { COLDWAR_KOR_industrial_laboratories_technology_education_cost_multiplier_modifier = 0.1 }
```

### COLDWAR_KOR_industrial_skills

```hoi4
COLDWAR_KOR_can_industrial_skills = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_industrial_skills_skills_buildings_worker_requirement_modifier = -0.03 }
set_variable = { COLDWAR_KOR_industrial_skills_skills_education_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_labor_discipline

```hoi4
COLDWAR_KOR_can_labor_discipline = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_labor_discipline_labour_stability_factor = -0.06 }
set_variable = { COLDWAR_KOR_labor_discipline_labour_civilian_factories_productivity = 0.07 }
```

### COLDWAR_KOR_labor_compact

```hoi4
COLDWAR_KOR_can_labor_compact = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_labor_compact_labour_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_labor_compact_labour_civilian_factories_productivity = 0.01 }
```

### COLDWAR_KOR_controlled_arbitration

```hoi4
COLDWAR_KOR_can_controlled_arbitration = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_controlled_arbitration_labour_stability_factor = -0.07 }
set_variable = { COLDWAR_KOR_controlled_arbitration_labour_police_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_controlled_arbitration_labour_civilian_factories_productivity = 0.09 }
```

### COLDWAR_KOR_safety_inspectorate

```hoi4
COLDWAR_KOR_can_safety_inspectorate = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_safety_inspectorate_labour_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_safety_inspectorate_labour_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_safety_inspectorate_labour_civilian_factories_productivity = 0.02 }
```

### COLDWAR_KOR_urban_services

```hoi4
COLDWAR_KOR_can_urban_services = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_urban_services_urban_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_urban_services_urban_consumer_goods_factor = 0.01 }
```

### COLDWAR_KOR_export_credit_guarantees

```hoi4
COLDWAR_KOR_can_export_credit_guarantees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_export_credit_guarantees_finance_interest_rate_multiplier_modifier = 0.4 }
set_variable = { COLDWAR_KOR_export_credit_guarantees_finance_civilian_factories_productivity = 0.06 }
```

### COLDWAR_KOR_banking_discipline

```hoi4
COLDWAR_KOR_can_banking_discipline = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_banking_discipline_finance_interest_rate_multiplier_modifier = -0.5 }
set_variable = { COLDWAR_KOR_banking_discipline_finance_civilian_factories_productivity = -0.03 }
```

### COLDWAR_KOR_strategic_refinancing

```hoi4
COLDWAR_KOR_can_strategic_refinancing = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_strategic_refinancing_finance_interest_rate_multiplier_modifier = 0.5 }
set_variable = { COLDWAR_KOR_strategic_refinancing_finance_civilian_factories_productivity = 0.08 }
```

### COLDWAR_KOR_orderly_restructuring

```hoi4
COLDWAR_KOR_can_orderly_restructuring = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_orderly_restructuring_finance_interest_rate_multiplier_modifier = -0.6 }
set_variable = { COLDWAR_KOR_orderly_restructuring_finance_civilian_factories_productivity = 0.02 }
```

### COLDWAR_KOR_energy_planning

```hoi4
COLDWAR_KOR_can_energy_planning = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
```

### COLDWAR_KOR_civil_nuclear

```hoi4
COLDWAR_KOR_can_civil_nuclear = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
COLDWAR_nuc_economy_allows = yes
has_tech = reactor1
country_can_build_nuclear_reactors = yes
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
```

### COLDWAR_KOR_thermal_diversification

```hoi4
COLDWAR_KOR_can_thermal_diversification = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_thermal_diversification_energy_interest_rate_multiplier_modifier = 0.2 }
set_variable = { COLDWAR_KOR_thermal_diversification_energy_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_advanced_export_economy

```hoi4
COLDWAR_KOR_can_advanced_export_economy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_advanced_export_economy_maturity_buildings_worker_requirement_modifier = -0.03 }
set_variable = { COLDWAR_KOR_advanced_export_economy_maturity_education_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_advanced_export_economy_maturity_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_defence_review

```hoi4
COLDWAR_KOR_can_defence_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
army_experience = 25
set_variable = { COLDWAR_KOR_defence_review_readiness_army_core_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_defence_review_readiness_personnel_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_dmz_deterrence

```hoi4
COLDWAR_KOR_can_dmz_deterrence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_dmz_deterrence_posture_army_core_defence_factor = 0.08 }
set_variable = { COLDWAR_KOR_dmz_deterrence_posture_army_attack_factor = -0.03 }
```

### COLDWAR_KOR_mobile_deterrence

```hoi4
COLDWAR_KOR_can_mobile_deterrence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_mobile_deterrence_posture_army_attack_factor = 0.05 }
set_variable = { COLDWAR_KOR_mobile_deterrence_posture_army_org_factor = 0.04 }
set_variable = { COLDWAR_KOR_mobile_deterrence_posture_supply_consumption_factor = 0.05 }
```

### COLDWAR_KOR_counter_infiltration_units

```hoi4
COLDWAR_KOR_can_counter_infiltration_units = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
army_experience = 15
set_variable = { COLDWAR_KOR_counter_infiltration_units_posture_army_core_defence_factor = 0.1 }
set_variable = { COLDWAR_KOR_counter_infiltration_units_posture_army_org_factor = 0.03 }
set_variable = { COLDWAR_KOR_counter_infiltration_units_posture_army_attack_factor = -0.03 }
```

### COLDWAR_KOR_combined_arms_training

```hoi4
COLDWAR_KOR_can_combined_arms_training = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
army_experience = 15
set_variable = { COLDWAR_KOR_combined_arms_training_posture_army_attack_factor = 0.07 }
set_variable = { COLDWAR_KOR_combined_arms_training_posture_army_org_factor = 0.05 }
set_variable = { COLDWAR_KOR_combined_arms_training_posture_supply_consumption_factor = 0.07 }
```

### COLDWAR_KOR_defence_logistics

```hoi4
COLDWAR_KOR_can_defence_logistics = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_defence_logistics_logistics_supply_consumption_factor = -0.03 }
set_variable = { COLDWAR_KOR_defence_logistics_logistics_personnel_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_allied_procurement

```hoi4
COLDWAR_KOR_can_allied_procurement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_allied_procurement_procurement_equipment_cost_multiplier_modifier = -0.06 }
set_variable = { COLDWAR_KOR_allied_procurement_procurement_foreign_influence_defense_modifier = -0.06 }
```

### COLDWAR_KOR_domestic_defence_industry

```hoi4
COLDWAR_KOR_can_domestic_defence_industry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_domestic_defence_industry_procurement_production_speed_arms_factory_factor = 0.1 }
set_variable = { COLDWAR_KOR_domestic_defence_industry_procurement_industrial_capacity_factory = 0.03 }
set_variable = { COLDWAR_KOR_domestic_defence_industry_procurement_interest_rate_multiplier_modifier = 0.3 }
```

### COLDWAR_KOR_licensed_maintenance

```hoi4
COLDWAR_KOR_can_licensed_maintenance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_allied_procurement_contract_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_licensed_maintenance_procurement_equipment_cost_multiplier_modifier = -0.08 }
set_variable = { COLDWAR_KOR_licensed_maintenance_procurement_production_factory_max_efficiency_factor = 0.03 }
set_variable = { COLDWAR_KOR_licensed_maintenance_procurement_foreign_influence_defense_modifier = -0.07 }
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_allied_procurement }
NOT = { has_country_flag = COLDWAR_KOR_allied_procurement_contract_signed }
OR = { has_country_flag = COLDWAR_KOR_allied_procurement_contract_refused has_country_flag = COLDWAR_KOR_allied_procurement_contract_expired }
}
```

### COLDWAR_KOR_changwon_production

```hoi4
COLDWAR_KOR_can_changwon_production = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
605 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = arms_factory size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
605 = { add_building_construction = { type = arms_factory level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_changwon_production_procurement_production_speed_arms_factory_factor = 0.12 }
set_variable = { COLDWAR_KOR_changwon_production_procurement_industrial_capacity_factory = 0.04 }
set_variable = { COLDWAR_KOR_changwon_production_procurement_interest_rate_multiplier_modifier = 0.4 }
```

### COLDWAR_KOR_defence_quality

```hoi4
COLDWAR_KOR_can_defence_quality = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_defence_quality_quality_production_factory_max_efficiency_factor = 0.04 }
set_variable = { COLDWAR_KOR_defence_quality_quality_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_reserve_army

```hoi4
COLDWAR_KOR_can_reserve_army = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_reserve_army_service_conscription_factor = 0.08 }
set_variable = { COLDWAR_KOR_reserve_army_service_training_time_army_factor = -0.06 }
set_variable = { COLDWAR_KOR_reserve_army_service_buildings_worker_requirement_modifier = 0.04 }
```

### COLDWAR_KOR_professional_core

```hoi4
COLDWAR_KOR_can_professional_core = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_professional_core_service_army_org_factor = 0.06 }
set_variable = { COLDWAR_KOR_professional_core_service_army_morale_factor = 0.05 }
set_variable = { COLDWAR_KOR_professional_core_service_personnel_cost_multiplier_modifier = 0.1 }
```

### COLDWAR_KOR_civil_defence_training

```hoi4
COLDWAR_KOR_can_civil_defence_training = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civil_defence_training_service_conscription_factor = 0.1 }
set_variable = { COLDWAR_KOR_civil_defence_training_service_training_time_army_factor = -0.08 }
set_variable = { COLDWAR_KOR_civil_defence_training_service_buildings_worker_requirement_modifier = 0.05 }
```

### COLDWAR_KOR_career_ncos

```hoi4
COLDWAR_KOR_can_career_ncos = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
army_experience = 15
set_variable = { COLDWAR_KOR_career_ncos_service_army_org_factor = 0.08 }
set_variable = { COLDWAR_KOR_career_ncos_service_army_morale_factor = 0.07 }
set_variable = { COLDWAR_KOR_career_ncos_service_personnel_cost_multiplier_modifier = 0.12 }
```

### COLDWAR_KOR_joint_staff

```hoi4
COLDWAR_KOR_can_joint_staff = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
army_experience = 10
set_variable = { COLDWAR_KOR_joint_staff_staff_army_org_factor = 0.03 }
set_variable = { COLDWAR_KOR_joint_staff_staff_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_coastal_defence

```hoi4
COLDWAR_KOR_can_coastal_defence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
608 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = radar_station size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
608 = { add_building_construction = { type = radar_station level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_coastal_defence_maritime_navy_org_factor = 0.08 }
set_variable = { COLDWAR_KOR_coastal_defence_maritime_air_mission_efficiency = -0.03 }
```

### COLDWAR_KOR_air_defence

```hoi4
COLDWAR_KOR_can_air_defence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
604 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = anti_air_building size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
604 = { add_building_construction = { type = anti_air_building level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_air_defence_maritime_air_mission_efficiency = 0.06 }
set_variable = { COLDWAR_KOR_air_defence_maritime_navy_org_factor = -0.03 }
```

### COLDWAR_KOR_coastal_logistics

```hoi4
COLDWAR_KOR_can_coastal_logistics = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
605 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = dockyard size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
605 = { add_building_construction = { type = dockyard level = 1 instant_build = yes } }
```

### COLDWAR_KOR_air_command

```hoi4
COLDWAR_KOR_can_air_command = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_air_command_air_air_mission_efficiency = 0.03 }
set_variable = { COLDWAR_KOR_air_command_air_equipment_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_diplomatic_review

```hoi4
COLDWAR_KOR_can_diplomatic_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_diplomatic_review_service_trade_opinion_factor = 0.05 }
set_variable = { COLDWAR_KOR_diplomatic_review_service_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_alliance_bargain

```hoi4
COLDWAR_KOR_can_alliance_bargain = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_alliance_bargain_alignment_army_core_defence_factor = 0.05 }
set_variable = { COLDWAR_KOR_alliance_bargain_alignment_foreign_influence_defense_modifier = -0.05 }
```

### COLDWAR_KOR_strategic_autonomy

```hoi4
COLDWAR_KOR_can_strategic_autonomy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_strategic_autonomy_alignment_foreign_influence_defense_modifier = 0.1 }
set_variable = { COLDWAR_KOR_strategic_autonomy_alignment_trade_opinion_factor = -0.04 }
```

### COLDWAR_KOR_burden_sharing

```hoi4
COLDWAR_KOR_can_burden_sharing = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_us_alliance_assurance_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_burden_sharing_alignment_army_org_factor = 0.04 }
set_variable = { COLDWAR_KOR_burden_sharing_alignment_army_core_defence_factor = 0.05 }
set_variable = { COLDWAR_KOR_burden_sharing_alignment_foreign_influence_defense_modifier = -0.07 }
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_alliance_bargain }
NOT = { has_country_flag = COLDWAR_KOR_us_alliance_assurance_signed }
OR = { has_country_flag = COLDWAR_KOR_us_alliance_assurance_refused has_country_flag = COLDWAR_KOR_us_alliance_assurance_expired }
}
```

### COLDWAR_KOR_diverse_partners

```hoi4
COLDWAR_KOR_can_diverse_partners = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_diverse_partners_alignment_foreign_influence_defense_modifier = 0.12 }
set_variable = { COLDWAR_KOR_diverse_partners_alignment_trade_opinion_factor = 0.02 }
set_variable = { COLDWAR_KOR_diverse_partners_alignment_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_vietnam_legacy

```hoi4
COLDWAR_KOR_can_vietnam_legacy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_japan_pragmatism

```hoi4
COLDWAR_KOR_can_japan_pragmatism = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_japan_pragmatism_japan_trade_opinion_factor = 0.08 }
set_variable = { COLDWAR_KOR_japan_pragmatism_japan_stability_factor = -0.04 }
```

### COLDWAR_KOR_claims_first

```hoi4
COLDWAR_KOR_can_claims_first = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_claims_first_japan_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_claims_first_japan_foreign_influence_defense_modifier = 0.05 }
set_variable = { COLDWAR_KOR_claims_first_japan_trade_opinion_factor = -0.06 }
```

### COLDWAR_KOR_joint_technical_training

```hoi4
COLDWAR_KOR_can_joint_technical_training = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_japan_technology_finance_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_joint_technical_training_japan_trade_opinion_factor = 0.1 }
set_variable = { COLDWAR_KOR_joint_technical_training_japan_stability_factor = -0.05 }
set_variable = { COLDWAR_KOR_joint_technical_training_japan_civilian_factories_productivity = 0.03 }
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_japan_pragmatism }
NOT = { has_country_flag = COLDWAR_KOR_japan_technology_finance_signed }
OR = { has_country_flag = COLDWAR_KOR_japan_technology_finance_refused has_country_flag = COLDWAR_KOR_japan_technology_finance_expired }
}
```

### COLDWAR_KOR_alternative_capital

```hoi4
COLDWAR_KOR_can_alternative_capital = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_alternative_capital_japan_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_alternative_capital_japan_foreign_influence_defense_modifier = 0.06 }
set_variable = { COLDWAR_KOR_alternative_capital_japan_interest_rate_multiplier_modifier = 0.2 }
set_variable = { COLDWAR_KOR_alternative_capital_japan_trade_opinion_factor = -0.03 }
```

### COLDWAR_KOR_overseas_workers

```hoi4
COLDWAR_KOR_can_overseas_workers = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
```

### COLDWAR_KOR_nordpolitik

```hoi4
COLDWAR_KOR_can_nordpolitik = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_nordpolitik_markets_trade_opinion_factor = 0.08 }
set_variable = { COLDWAR_KOR_nordpolitik_markets_political_power_factor = -0.05 }
```

### COLDWAR_KOR_pacific_exports

```hoi4
COLDWAR_KOR_can_pacific_exports = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_pacific_exports_markets_trade_opinion_factor = 0.06 }
set_variable = { COLDWAR_KOR_pacific_exports_markets_foreign_influence_defense_modifier = -0.04 }
set_variable = { COLDWAR_KOR_pacific_exports_markets_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_middle_power

```hoi4
COLDWAR_KOR_can_middle_power = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_middle_power_standing_trade_opinion_factor = 0.05 }
set_variable = { COLDWAR_KOR_middle_power_standing_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_korean_question

```hoi4
COLDWAR_KOR_can_korean_question = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = 50
```

### COLDWAR_KOR_red_cross_channel

```hoi4
COLDWAR_KOR_can_red_cross_channel = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_armed_vigilance

```hoi4
COLDWAR_KOR_can_armed_vigilance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_armed_vigilance_opening_army_core_defence_factor = 0.06 }
set_variable = { COLDWAR_KOR_armed_vigilance_opening_trade_opinion_factor = -0.03 }
```

### COLDWAR_KOR_family_reunions

```hoi4
COLDWAR_KOR_can_family_reunions = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_red_cross_channel_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_red_cross_channel }
NOT = { has_country_flag = COLDWAR_KOR_red_cross_channel_signed }
OR = { has_country_flag = COLDWAR_KOR_red_cross_channel_refused has_country_flag = COLDWAR_KOR_red_cross_channel_expired }
}
```

### COLDWAR_KOR_incident_hotline

```hoi4
COLDWAR_KOR_can_incident_hotline = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_incident_hotline_opening_army_core_defence_factor = 0.07 }
set_variable = { COLDWAR_KOR_incident_hotline_opening_trade_opinion_factor = -0.03 }
```

### COLDWAR_KOR_review_korean_policy

```hoi4
COLDWAR_KOR_can_review_korean_policy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_review_korean_policy_coordination_foreign_influence_defense_modifier = 0.04 }
set_variable = { COLDWAR_KOR_review_korean_policy_coordination_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_peaceful_coexistence

```hoi4
COLDWAR_KOR_can_peaceful_coexistence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_competitive_legitimacy

```hoi4
COLDWAR_KOR_can_competitive_legitimacy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_competitive_legitimacy_strategy_foreign_influence_defense_modifier = 0.06 }
set_variable = { COLDWAR_KOR_competitive_legitimacy_strategy_political_power_factor = 0.04 }
set_variable = { COLDWAR_KOR_competitive_legitimacy_strategy_trade_opinion_factor = -0.04 }
```

### COLDWAR_KOR_verified_restraint

```hoi4
COLDWAR_KOR_can_verified_restraint = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_nonaggression_compact_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_peaceful_coexistence }
NOT = { has_country_flag = COLDWAR_KOR_nonaggression_compact_signed }
OR = { has_country_flag = COLDWAR_KOR_nonaggression_compact_refused has_country_flag = COLDWAR_KOR_nonaggression_compact_expired }
}
```

### COLDWAR_KOR_defector_protection

```hoi4
COLDWAR_KOR_can_defector_protection = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_defector_protection_strategy_foreign_influence_defense_modifier = 0.07 }
set_variable = { COLDWAR_KOR_defector_protection_strategy_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_defector_protection_strategy_social_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_reciprocal_contacts

```hoi4
COLDWAR_KOR_can_reciprocal_contacts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_sovereign_confederation

```hoi4
COLDWAR_KOR_can_sovereign_confederation = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
OR = { has_country_flag = COLDWAR_KOR_working_contacts_signed has_country_flag = COLDWAR_KOR_nonaggression_compact_signed }
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_two_governments

```hoi4
COLDWAR_KOR_can_two_governments = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
OR = { has_country_flag = COLDWAR_KOR_working_contacts_signed has_country_flag = COLDWAR_KOR_nonaggression_compact_signed }
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_confederal_secretariat

```hoi4
COLDWAR_KOR_can_confederal_secretariat = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_sovereign_confederation_signed
has_idea = COLDWAR_KOR_confederal_member
NKO = { has_idea = COLDWAR_KOR_confederal_member }
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_confederal_revolution has_completed_focus = COLDWAR_KOR_sovereign_confederation }
NOT = { has_country_flag = COLDWAR_KOR_sovereign_confederation_signed }
OR = { has_country_flag = COLDWAR_KOR_sovereign_confederation_refused has_country_flag = COLDWAR_KOR_sovereign_confederation_expired }
}
```

### COLDWAR_KOR_limited_trade

```hoi4
COLDWAR_KOR_can_limited_trade = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_parallel_recognition_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_two_governments }
NOT = { has_country_flag = COLDWAR_KOR_parallel_recognition_signed }
OR = { has_country_flag = COLDWAR_KOR_parallel_recognition_refused has_country_flag = COLDWAR_KOR_parallel_recognition_expired }
}
```

### COLDWAR_KOR_korean_settlement

```hoi4
COLDWAR_KOR_can_korean_settlement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_kjp_civilian_cabinet

```hoi4
COLDWAR_KOR_can_kjp_civilian_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_civilian_cabinet_mandate_political_power_factor = 0.06 }
set_variable = { COLDWAR_KOR_kjp_civilian_cabinet_mandate_bureaucracy_cost_multiplier_modifier = -0.03 }
set_variable = { COLDWAR_KOR_kjp_civilian_cabinet_mandate_stability_factor = -0.02 }
```

### COLDWAR_KOR_kjp_coalition

```hoi4
COLDWAR_KOR_can_kjp_coalition = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_coalition_coalition_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_kjp_coalition_coalition_political_power_factor = -0.06 }
```

### COLDWAR_KOR_kjp_executive

```hoi4
COLDWAR_KOR_can_kjp_executive = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_executive_coalition_production_speed_buildings_factor = 0.06 }
set_variable = { COLDWAR_KOR_kjp_executive_coalition_political_power_factor = 0.06 }
set_variable = { COLDWAR_KOR_kjp_executive_coalition_stability_factor = -0.04 }
```

### COLDWAR_KOR_kjp_coalition_committees

```hoi4
COLDWAR_KOR_can_kjp_coalition_committees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_coalition_committees_coalition_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_kjp_coalition_committees_coalition_political_power_factor = -0.08 }
set_variable = { COLDWAR_KOR_kjp_coalition_committees_coalition_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_kjp_professional_cabinet

```hoi4
COLDWAR_KOR_can_kjp_professional_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_professional_cabinet_coalition_production_speed_buildings_factor = 0.08 }
set_variable = { COLDWAR_KOR_kjp_professional_cabinet_coalition_political_power_factor = 0.06 }
set_variable = { COLDWAR_KOR_kjp_professional_cabinet_coalition_stability_factor = -0.05 }
set_variable = { COLDWAR_KOR_kjp_professional_cabinet_coalition_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_kjp_provincial_credit

```hoi4
COLDWAR_KOR_can_kjp_provincial_credit = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
```

### COLDWAR_KOR_kjp_small_enterprise

```hoi4
COLDWAR_KOR_can_kjp_small_enterprise = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_kjp_small_enterprise_enterprise_production_speed_industrial_complex_factor = 0.08 }
set_variable = { COLDWAR_KOR_kjp_small_enterprise_enterprise_civilian_factories_productivity = 0.01 }
```

### COLDWAR_KOR_kjp_large_industry

```hoi4
COLDWAR_KOR_can_kjp_large_industry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_large_industry_enterprise_interest_rate_multiplier_modifier = 0.3 }
set_variable = { COLDWAR_KOR_kjp_large_industry_enterprise_civilian_factories_productivity = 0.06 }
```

### COLDWAR_KOR_kjp_supplier_networks

```hoi4
COLDWAR_KOR_can_kjp_supplier_networks = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_supplier_networks_enterprise_production_speed_industrial_complex_factor = 0.1 }
set_variable = { COLDWAR_KOR_kjp_supplier_networks_enterprise_bureaucracy_cost_multiplier_modifier = 0.03 }
set_variable = { COLDWAR_KOR_kjp_supplier_networks_enterprise_civilian_factories_productivity = 0.02 }
```

### COLDWAR_KOR_kjp_export_compromise

```hoi4
COLDWAR_KOR_can_kjp_export_compromise = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_export_compromise_enterprise_interest_rate_multiplier_modifier = 0.4 }
set_variable = { COLDWAR_KOR_kjp_export_compromise_enterprise_stability_factor = -0.02 }
set_variable = { COLDWAR_KOR_kjp_export_compromise_enterprise_civilian_factories_productivity = 0.08 }
```

### COLDWAR_KOR_kjp_party_settlement

```hoi4
COLDWAR_KOR_can_kjp_party_settlement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_party_settlement_settlement_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_kjp_party_settlement_settlement_political_power_factor = -0.04 }
```

### COLDWAR_KOR_kjp_korean_policy

```hoi4
COLDWAR_KOR_can_kjp_korean_policy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_korean_policy_foreign_trade_opinion_factor = 0.04 }
set_variable = { COLDWAR_KOR_kjp_korean_policy_foreign_political_power_factor = -0.03 }
```

### COLDWAR_KOR_drp_budget_charter

```hoi4
COLDWAR_KOR_can_drp_budget_charter = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_drp_budget_charter_oversight_production_speed_buildings_factor = 0.04 }
set_variable = { COLDWAR_KOR_drp_budget_charter_oversight_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_drp_technocrats

```hoi4
COLDWAR_KOR_can_drp_technocrats = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_drp_technocrats_administrative_base_research_speed_factor = 0.04 }
set_variable = { COLDWAR_KOR_drp_technocrats_administrative_base_education_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_drp_technocrats_administrative_base_political_power_factor = -0.04 }
```

### COLDWAR_KOR_drp_provincial_brokers

```hoi4
COLDWAR_KOR_can_drp_provincial_brokers = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Park Chung Hee" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_drp_provincial_brokers_administrative_base_agricolture_productivity_modifier = 0.08 }
set_variable = { COLDWAR_KOR_drp_provincial_brokers_administrative_base_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_drp_provincial_brokers_administrative_base_bureaucracy_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_ndp_tax_transparency

```hoi4
COLDWAR_KOR_can_ndp_tax_transparency = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_ndp_tax_transparency_revenue_interest_rate_multiplier_modifier = -0.25 }
set_variable = { COLDWAR_KOR_ndp_tax_transparency_revenue_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_ndp_tax_transparency_revenue_political_power_factor = -0.04 }
```

### COLDWAR_KOR_ndp_tax_compromise

```hoi4
COLDWAR_KOR_can_ndp_tax_compromise = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_ndp_tax_compromise_revenue_production_speed_industrial_complex_factor = 0.06 }
set_variable = { COLDWAR_KOR_ndp_tax_compromise_revenue_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_ndp_tax_compromise_revenue_interest_rate_multiplier_modifier = 0.15 }
```

### COLDWAR_KOR_ndp_municipal_services

```hoi4
COLDWAR_KOR_can_ndp_municipal_services = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 1 }
607 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = infrastructure size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
607 = { add_building_construction = { type = infrastructure level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_ndp_municipal_services_local_admin_agricolture_productivity_modifier = 0.04 }
set_variable = { COLDWAR_KOR_ndp_municipal_services_local_admin_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_reform_party_accounts

```hoi4
COLDWAR_KOR_can_reform_party_accounts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_reform_party_accounts_party_finance_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_reform_party_accounts_party_finance_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_reform_party_accounts_party_finance_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_ys_civilian_contracts

```hoi4
COLDWAR_KOR_can_ys_civilian_contracts = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
has_country_leader = { name = "Kim Young-sam" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_ys_civilian_contracts_ys_contracts_production_speed_industrial_complex_factor = 0.06 }
set_variable = { COLDWAR_KOR_ys_civilian_contracts_ys_contracts_bureaucracy_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_ys_civilian_contracts_ys_contracts_political_power_factor = -0.03 }
```

### COLDWAR_KOR_dj_social_dialogue

```hoi4
COLDWAR_KOR_can_dj_social_dialogue = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
has_country_leader = { name = "Kim Dae-jung" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_dj_social_dialogue_dj_dialogue_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_dj_social_dialogue_dj_dialogue_social_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_dj_social_dialogue_dj_dialogue_civilian_factories_productivity = 0.03 }
```

### COLDWAR_KOR_reform_lawful_succession

```hoi4
COLDWAR_KOR_can_reform_lawful_succession = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 2 }
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_reform_lawful_succession_succession_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_reform_lawful_succession_succession_political_power_factor = -0.04 }
```

### COLDWAR_KOR_army_constitutional_service

```hoi4
COLDWAR_KOR_can_army_constitutional_service = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_army_constitutional_service_service_law_army_org_factor = 0.03 }
set_variable = { COLDWAR_KOR_army_constitutional_service_service_law_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_army_constitutional_service_service_law_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_army_civilian_ministry

```hoi4
COLDWAR_KOR_can_army_civilian_ministry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_army_civilian_ministry_command_settlement_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_army_civilian_ministry_command_settlement_army_org_factor = -0.02 }
set_variable = { COLDWAR_KOR_army_civilian_ministry_command_settlement_personnel_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_army_advisory_council

```hoi4
COLDWAR_KOR_can_army_advisory_council = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 22 }
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_army_advisory_council_command_settlement_army_org_factor = 0.06 }
set_variable = { COLDWAR_KOR_army_advisory_council_command_settlement_stability_factor = -0.03 }
set_variable = { COLDWAR_KOR_army_advisory_council_command_settlement_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_usp_national_wage_floor

```hoi4
COLDWAR_KOR_can_usp_national_wage_floor = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_usp_national_wage_floor_wage_settlement_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_usp_national_wage_floor_wage_settlement_social_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_usp_national_wage_floor_wage_settlement_civilian_factories_productivity = -0.03 }
```

### COLDWAR_KOR_usp_sectoral_bargaining

```hoi4
COLDWAR_KOR_can_usp_sectoral_bargaining = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 3 }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_usp_sectoral_bargaining_wage_settlement_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_usp_sectoral_bargaining_wage_settlement_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_usp_sectoral_bargaining_wage_settlement_civilian_factories_productivity = 0.04 }
```

### COLDWAR_KOR_student_workplace_alliance

```hoi4
COLDWAR_KOR_can_student_workplace_alliance = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 5 }
has_country_flag = COLDWAR_KOR_civic_legal_5
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_student_workplace_alliance_civic_training_research_speed_factor = 0.03 }
set_variable = { COLDWAR_KOR_student_workplace_alliance_civic_training_education_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_student_workplace_alliance_civic_training_political_power_factor = -0.04 }
```

### COLDWAR_KOR_left_public_procurement

```hoi4
COLDWAR_KOR_can_left_public_procurement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 19 }
has_country_flag = COLDWAR_KOR_civic_legal_19
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_left_public_procurement_left_procurement_bureaucracy_cost_multiplier_modifier = 0.05 }
set_variable = { COLDWAR_KOR_left_public_procurement_left_procurement_interest_rate_multiplier_modifier = 0.15 }
set_variable = { COLDWAR_KOR_left_public_procurement_left_procurement_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_civic_association_law

```hoi4
COLDWAR_KOR_can_civic_association_law = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
OR = { check_variable = { ruling_party = 5 } check_variable = { ruling_party = 19 } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civic_association_law_associations_research_speed_factor = 0.02 }
set_variable = { COLDWAR_KOR_civic_association_law_associations_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_civic_association_law_associations_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_rpr_worker_elections

```hoi4
COLDWAR_KOR_can_rpr_worker_elections = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_rpr_worker_elections_workplace_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_rpr_worker_elections_workplace_political_power_factor = -0.05 }
set_variable = { COLDWAR_KOR_rpr_worker_elections_workplace_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_rpr_production_cadres

```hoi4
COLDWAR_KOR_can_rpr_production_cadres = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 4 }
has_country_flag = COLDWAR_KOR_revolutionary_settlement
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_rpr_production_cadres_workplace_stability_factor = -0.04 }
set_variable = { COLDWAR_KOR_rpr_production_cadres_workplace_interest_rate_multiplier_modifier = 0.2 }
set_variable = { COLDWAR_KOR_rpr_production_cadres_workplace_civilian_factories_productivity = 0.08 }
```

### COLDWAR_KOR_security_due_process

```hoi4
COLDWAR_KOR_can_security_due_process = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_due_process_legal_settlement_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_security_due_process_legal_settlement_research_speed_factor = 0.02 }
set_variable = { COLDWAR_KOR_security_due_process_legal_settlement_intel_network_gain_factor = -0.04 }
set_variable = { COLDWAR_KOR_security_due_process_legal_settlement_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_security_protected_archives

```hoi4
COLDWAR_KOR_can_security_protected_archives = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 7 }
has_country_flag = COLDWAR_KOR_security_directorate_ratified
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_security_protected_archives_legal_settlement_intel_network_gain_factor = 0.1 }
set_variable = { COLDWAR_KOR_security_protected_archives_legal_settlement_stability_factor = -0.05 }
set_variable = { COLDWAR_KOR_security_protected_archives_legal_settlement_police_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_kjp_coalition_broker

```hoi4
COLDWAR_KOR_can_kjp_coalition_broker = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_kjp_coalition_broker_coalition_identity_political_power_factor = 0.12 }
set_variable = { COLDWAR_KOR_kjp_coalition_broker_coalition_identity_stability_factor = -0.03 }
set_variable = { COLDWAR_KOR_kjp_coalition_broker_coalition_identity_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_kjp_independent_party

```hoi4
COLDWAR_KOR_can_kjp_independent_party = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
check_variable = { ruling_party = 0 }
has_country_leader = { name = "Kim Jong-pil" ruling_only = yes }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_kjp_independent_party_coalition_identity_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_kjp_independent_party_coalition_identity_production_speed_industrial_complex_factor = 0.04 }
set_variable = { COLDWAR_KOR_kjp_independent_party_coalition_identity_political_power_factor = -0.06 }
```

### COLDWAR_KOR_sector_investment_review

```hoi4
COLDWAR_KOR_can_sector_investment_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
```

### COLDWAR_KOR_electronics_priority

```hoi4
COLDWAR_KOR_can_electronics_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_electronics_priority_sector_research_speed_factor = 0.03 }
set_variable = { COLDWAR_KOR_electronics_priority_sector_education_cost_multiplier_modifier = 0.07 }
set_variable = { COLDWAR_KOR_electronics_priority_sector_buildings_worker_requirement_modifier = 0.03 }
set_variable = { COLDWAR_KOR_electronics_priority_sector_civilian_factories_productivity = 0.05 }
```

### COLDWAR_KOR_electronics_capability

```hoi4
COLDWAR_KOR_can_electronics_capability = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_electronics_capability_sector_research_speed_factor = 0.04 }
set_variable = { COLDWAR_KOR_electronics_capability_sector_education_cost_multiplier_modifier = 0.1 }
set_variable = { COLDWAR_KOR_electronics_capability_sector_buildings_worker_requirement_modifier = 0.03 }
set_variable = { COLDWAR_KOR_electronics_capability_sector_civilian_factories_productivity = 0.08 }
```

### COLDWAR_KOR_machinery_priority

```hoi4
COLDWAR_KOR_can_machinery_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_machinery_priority_sector_production_speed_buildings_factor = 0.03 }
set_variable = { COLDWAR_KOR_machinery_priority_sector_interest_rate_multiplier_modifier = 0.25 }
set_variable = { COLDWAR_KOR_machinery_priority_sector_buildings_worker_requirement_modifier = 0.03 }
set_variable = { COLDWAR_KOR_machinery_priority_sector_civilian_factories_productivity = 0.07 }
```

### COLDWAR_KOR_supplier_engineering

```hoi4
COLDWAR_KOR_can_supplier_engineering = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
606 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = industrial_complex size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
606 = { add_building_construction = { type = industrial_complex level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_supplier_engineering_sector_production_speed_buildings_factor = 0.04 }
set_variable = { COLDWAR_KOR_supplier_engineering_sector_interest_rate_multiplier_modifier = 0.35 }
set_variable = { COLDWAR_KOR_supplier_engineering_sector_buildings_worker_requirement_modifier = 0.04 }
set_variable = { COLDWAR_KOR_supplier_engineering_sector_civilian_factories_productivity = 0.1 }
```

### COLDWAR_KOR_shipbuilding_priority

```hoi4
COLDWAR_KOR_can_shipbuilding_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -3 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_shipbuilding_priority_sector_buildings_worker_requirement_modifier = 0.04 }
set_variable = { COLDWAR_KOR_shipbuilding_priority_sector_interest_rate_multiplier_modifier = 0.2 }
set_variable = { COLDWAR_KOR_shipbuilding_priority_sector_civilian_factories_productivity = 0.03 }
set_variable = { COLDWAR_KOR_shipbuilding_priority_sector_dockyard_productivity = 0.12 }
```

### COLDWAR_KOR_commercial_shipyards

```hoi4
COLDWAR_KOR_can_commercial_shipyards = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
605 = { is_owned_by = ROOT is_controlled_by = ROOT free_building_slots = { building = dockyard size > 0 include_locked = no } }
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
605 = { add_building_construction = { type = dockyard level = 1 instant_build = yes } }
set_variable = { COLDWAR_KOR_commercial_shipyards_sector_buildings_worker_requirement_modifier = 0.04 }
set_variable = { COLDWAR_KOR_commercial_shipyards_sector_interest_rate_multiplier_modifier = 0.3 }
set_variable = { COLDWAR_KOR_commercial_shipyards_sector_civilian_factories_productivity = 0.05 }
set_variable = { COLDWAR_KOR_commercial_shipyards_sector_dockyard_productivity = 0.18 }
```

### COLDWAR_KOR_industrial_quality_service

```hoi4
COLDWAR_KOR_can_industrial_quality_service = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_industrial_quality_service_standards_buildings_worker_requirement_modifier = -0.02 }
set_variable = { COLDWAR_KOR_industrial_quality_service_standards_education_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_industrial_quality_service_standards_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_urban_insurance_network

```hoi4
COLDWAR_KOR_can_urban_insurance_network = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_urban_insurance_network_social_network_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_urban_insurance_network_social_network_health_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_urban_insurance_network_social_network_social_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_urban_insurance_network_social_network_buildings_worker_requirement_modifier = -0.02 }
```

### COLDWAR_KOR_rural_insurance_network

```hoi4
COLDWAR_KOR_can_rural_insurance_network = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_rural_insurance_network_social_network_agricolture_productivity_modifier = 0.07 }
set_variable = { COLDWAR_KOR_rural_insurance_network_social_network_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_rural_insurance_network_social_network_health_cost_multiplier_modifier = 0.06 }
set_variable = { COLDWAR_KOR_rural_insurance_network_social_network_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_yulgok_readiness_review

```hoi4
COLDWAR_KOR_can_yulgok_readiness_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
army_experience = 15
set_variable = { COLDWAR_KOR_yulgok_readiness_review_readiness_audit_army_org_factor = 0.02 }
set_variable = { COLDWAR_KOR_yulgok_readiness_review_readiness_audit_personnel_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_air_cover_priority

```hoi4
COLDWAR_KOR_can_air_cover_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_air_cover_priority_mission_priority_air_mission_efficiency = 0.06 }
set_variable = { COLDWAR_KOR_air_cover_priority_mission_priority_equipment_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_aircrew_training

```hoi4
COLDWAR_KOR_can_aircrew_training = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_aircrew_training_mission_priority_air_mission_efficiency = 0.09 }
set_variable = { COLDWAR_KOR_aircrew_training_mission_priority_equipment_cost_multiplier_modifier = 0.08 }
set_variable = { COLDWAR_KOR_aircrew_training_mission_priority_personnel_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_escort_priority

```hoi4
COLDWAR_KOR_can_escort_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_escort_priority_mission_priority_navy_org_factor = 0.08 }
set_variable = { COLDWAR_KOR_escort_priority_mission_priority_supply_consumption_factor = 0.04 }
set_variable = { COLDWAR_KOR_escort_priority_mission_priority_equipment_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_escort_staff

```hoi4
COLDWAR_KOR_can_escort_staff = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_escort_staff_mission_priority_navy_org_factor = 0.12 }
set_variable = { COLDWAR_KOR_escort_staff_mission_priority_supply_consumption_factor = 0.05 }
set_variable = { COLDWAR_KOR_escort_staff_mission_priority_equipment_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_counterbattery_priority

```hoi4
COLDWAR_KOR_can_counterbattery_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_counterbattery_priority_mission_priority_army_defence_factor = 0.05 }
set_variable = { COLDWAR_KOR_counterbattery_priority_mission_priority_army_attack_factor = 0.03 }
set_variable = { COLDWAR_KOR_counterbattery_priority_mission_priority_supply_consumption_factor = 0.05 }
```

### COLDWAR_KOR_fire_direction

```hoi4
COLDWAR_KOR_can_fire_direction = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_fire_direction_mission_priority_army_defence_factor = 0.07 }
set_variable = { COLDWAR_KOR_fire_direction_mission_priority_army_attack_factor = 0.04 }
set_variable = { COLDWAR_KOR_fire_direction_mission_priority_supply_consumption_factor = 0.07 }
```

### COLDWAR_KOR_joint_readiness_audits

```hoi4
COLDWAR_KOR_can_joint_readiness_audits = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
army_experience = 15
set_variable = { COLDWAR_KOR_joint_readiness_audits_joint_audit_supply_consumption_factor = -0.03 }
set_variable = { COLDWAR_KOR_joint_readiness_audits_joint_audit_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_overseas_commercial_service

```hoi4
COLDWAR_KOR_can_overseas_commercial_service = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_overseas_commercial_service_commercial_service_trade_opinion_factor = 0.04 }
set_variable = { COLDWAR_KOR_overseas_commercial_service_commercial_service_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_middle_east_bids

```hoi4
COLDWAR_KOR_can_middle_east_bids = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_middle_east_bids_commercial_orientation_trade_opinion_factor = 0.05 }
set_variable = { COLDWAR_KOR_middle_east_bids_commercial_orientation_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_pacific_standards

```hoi4
COLDWAR_KOR_can_pacific_standards = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_pacific_standards_commercial_orientation_research_speed_factor = 0.02 }
set_variable = { COLDWAR_KOR_pacific_standards_commercial_orientation_foreign_influence_defense_modifier = -0.03 }
```

### COLDWAR_KOR_contract_worker_protection

```hoi4
COLDWAR_KOR_can_contract_worker_protection = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_contract_worker_protection_commercial_orientation_trade_opinion_factor = 0.07 }
set_variable = { COLDWAR_KOR_contract_worker_protection_commercial_orientation_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_contract_worker_protection_commercial_orientation_bureaucracy_cost_multiplier_modifier = 0.06 }
```

### COLDWAR_KOR_international_quality

```hoi4
COLDWAR_KOR_can_international_quality = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_international_quality_commercial_orientation_research_speed_factor = 0.02 }
set_variable = { COLDWAR_KOR_international_quality_commercial_orientation_education_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_international_quality_commercial_orientation_foreign_influence_defense_modifier = -0.03 }
set_variable = { COLDWAR_KOR_international_quality_commercial_orientation_civilian_factories_productivity = 0.03 }
```

### COLDWAR_KOR_professional_trade_missions

```hoi4
COLDWAR_KOR_can_professional_trade_missions = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_professional_trade_missions_missions_trade_opinion_factor = 0.05 }
set_variable = { COLDWAR_KOR_professional_trade_missions_missions_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_public_treaty_process

```hoi4
COLDWAR_KOR_can_public_treaty_process = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_public_treaty_process_treaty_rules_foreign_influence_defense_modifier = 0.05 }
set_variable = { COLDWAR_KOR_public_treaty_process_treaty_rules_trade_opinion_factor = 0.03 }
set_variable = { COLDWAR_KOR_public_treaty_process_treaty_rules_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_public_treaty_process_treaty_rules_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_korean_implementation_review

```hoi4
COLDWAR_KOR_can_korean_implementation_review = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_korean_implementation_review_liaison_admin_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_civilian_exchange_priority

```hoi4
COLDWAR_KOR_can_civilian_exchange_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_exchange_priority_contact_priority_trade_opinion_factor = 0.05 }
set_variable = { COLDWAR_KOR_civilian_exchange_priority_contact_priority_foreign_influence_defense_modifier = -0.03 }
set_variable = { COLDWAR_KOR_civilian_exchange_priority_contact_priority_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_verification_priority

```hoi4
COLDWAR_KOR_can_verification_priority = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_verification_priority_contact_priority_army_core_defence_factor = 0.04 }
set_variable = { COLDWAR_KOR_verification_priority_contact_priority_political_power_factor = -0.03 }
```

### COLDWAR_KOR_cultural_visits

```hoi4
COLDWAR_KOR_can_cultural_visits = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_cultural_exchanges_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_civilian_exchange_priority }
NOT = { has_country_flag = COLDWAR_KOR_cultural_exchanges_signed }
OR = { has_country_flag = COLDWAR_KOR_cultural_exchanges_refused has_country_flag = COLDWAR_KOR_cultural_exchanges_expired }
}
```

### COLDWAR_KOR_border_notice_protocol

```hoi4
COLDWAR_KOR_can_border_notice_protocol = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_border_notifications_signed
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

Native focus-level bypass (no reward):

```hoi4
bypass = {
original_tag = KOR
IMP_is_1970_scenario = yes
OR = { has_completed_focus = COLDWAR_KOR_verification_priority }
NOT = { has_country_flag = COLDWAR_KOR_border_notifications_signed }
OR = { has_country_flag = COLDWAR_KOR_border_notifications_refused has_country_flag = COLDWAR_KOR_border_notifications_expired }
}
```

### COLDWAR_KOR_peninsula_liaison_office

```hoi4
COLDWAR_KOR_can_peninsula_liaison_office = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_peninsula_liaison_office_liaison_admin_trade_opinion_factor = 0.03 }
set_variable = { COLDWAR_KOR_peninsula_liaison_office_liaison_admin_bureaucracy_cost_multiplier_modifier = 0.05 }
```

### COLDWAR_KOR_community_dialogue

```hoi4
COLDWAR_KOR_can_community_dialogue = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
OR = { has_country_flag = COLDWAR_KOR_working_contacts_signed has_country_flag = COLDWAR_KOR_sovereign_confederation_signed }
}
# One-time completion leaves; new programme/offer handlers remain separate.
# No unilateral leaf reward; see the accepted contract or action definition.
```

### COLDWAR_KOR_constitutional_question

```hoi4
COLDWAR_KOR_can_constitutional_question = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = -50
set_variable = { COLDWAR_KOR_constitutional_question_constitutional_audit_political_power_factor = 0.03 }
set_variable = { COLDWAR_KOR_constitutional_question_constitutional_audit_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_electoral_opening

```hoi4
COLDWAR_KOR_can_electoral_opening = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_electoral_opening
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_electoral_opening_transition_phase_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_electoral_opening_transition_phase_stability_factor = -0.02 }
set_country_flag = COLDWAR_KOR_transition_open
```

### COLDWAR_KOR_interim_cabinet

```hoi4
COLDWAR_KOR_can_interim_cabinet = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_caretaker_installed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_interim_cabinet_transition_phase_political_power_factor = -0.06 }
set_variable = { COLDWAR_KOR_interim_cabinet_transition_phase_army_org_factor = -0.02 }
set_country_flag = COLDWAR_KOR_transition_open
```

### COLDWAR_KOR_negotiated_withdrawal

```hoi4
COLDWAR_KOR_can_negotiated_withdrawal = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_military_opening_authorized
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_negotiated_withdrawal_transition_phase_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_negotiated_withdrawal_transition_phase_personnel_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_transition_open
```

### COLDWAR_KOR_bind_incumbent

```hoi4
COLDWAR_KOR_can_bind_incumbent = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_bind_incumbent_transition_phase_political_power_factor = -0.05 }
set_variable = { COLDWAR_KOR_bind_incumbent_transition_phase_bureaucracy_cost_multiplier_modifier = 0.03 }
set_country_flag = COLDWAR_KOR_negotiating_commitment
```

### COLDWAR_KOR_defend_civil_command

```hoi4
COLDWAR_KOR_can_defend_civil_command = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_defend_civil_command_transition_phase_army_org_factor = -0.03 }
set_variable = { COLDWAR_KOR_defend_civil_command_transition_phase_political_power_factor = -0.04 }
set_country_flag = COLDWAR_KOR_command_settlement_pending
country_event = { id = COLDWAR_KOR_transition.12 days = 1 }
```

### COLDWAR_KOR_retirement_guarantees

```hoi4
COLDWAR_KOR_can_retirement_guarantees = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_retirement_guarantees_retirement_promise_army_org_factor = 0.02 }
set_variable = { COLDWAR_KOR_retirement_guarantees_retirement_promise_personnel_cost_multiplier_modifier = 0.08 }
set_country_flag = COLDWAR_KOR_negotiating_commitment
```

### COLDWAR_KOR_authorize_talks

```hoi4
COLDWAR_KOR_can_authorize_talks = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_negotiating_commitment
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_authorize_talks_transition_phase_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_authorize_talks_transition_phase_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_talks_authorized
```

### COLDWAR_KOR_open_civic_space

```hoi4
COLDWAR_KOR_can_open_civic_space = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_country_flag = COLDWAR_KOR_civic_space_open
set_country_flag = COLDWAR_KOR_civic_legal_5
set_country_flag = COLDWAR_KOR_civic_legal_19
```

### COLDWAR_KOR_broad_democratic_coalition

```hoi4
COLDWAR_KOR_can_broad_democratic_coalition = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_broad_democratic_coalition_coalition_forum_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_broad_democratic_coalition_coalition_forum_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_open_security_records

```hoi4
COLDWAR_KOR_can_open_security_records = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_open_security_records_records_intel_network_gain_factor = -0.02 }
set_variable = { COLDWAR_KOR_open_security_records_records_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_unity_ticket

```hoi4
COLDWAR_KOR_can_unity_ticket = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_unity_ticket_campaign_settlement_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_unity_ticket_campaign_settlement_political_power_factor = -0.05 }
set_country_flag = COLDWAR_KOR_unified_ticket
```

### COLDWAR_KOR_independent_tickets

```hoi4
COLDWAR_KOR_can_independent_tickets = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_independent_tickets_campaign_settlement_political_power_factor = 0.08 }
set_variable = { COLDWAR_KOR_independent_tickets_campaign_settlement_stability_factor = -0.02 }
set_country_flag = COLDWAR_KOR_separate_tickets
```

### COLDWAR_KOR_independent_inquiry

```hoi4
COLDWAR_KOR_can_independent_inquiry = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_independent_inquiry_accountability_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_independent_inquiry_accountability_bureaucracy_cost_multiplier_modifier = 0.07 }
set_variable = { COLDWAR_KOR_independent_inquiry_accountability_intel_network_gain_factor = -0.03 }
```

### COLDWAR_KOR_conditional_amnesty

```hoi4
COLDWAR_KOR_can_conditional_amnesty = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_conditional_amnesty_accountability_army_org_factor = 0.03 }
set_variable = { COLDWAR_KOR_conditional_amnesty_accountability_stability_factor = -0.02 }
set_variable = { COLDWAR_KOR_conditional_amnesty_accountability_trade_opinion_factor = -0.02 }
set_variable = { COLDWAR_KOR_conditional_amnesty_accountability_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_negotiating_mandate

```hoi4
COLDWAR_KOR_can_negotiating_mandate = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_country_flag = COLDWAR_KOR_charter_mandate
```

### COLDWAR_KOR_presidential_democracy

```hoi4
COLDWAR_KOR_can_presidential_democracy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_presidential_democracy_constitution_political_power_factor = 0.08 }
set_variable = { COLDWAR_KOR_presidential_democracy_constitution_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_presidential_democracy_constitution_bureaucracy_cost_multiplier_modifier = 0.03 }
set_country_flag = COLDWAR_KOR_draft_presidential
set_variable = { COLDWAR_KOR_charter_model = 1 }
```

### COLDWAR_KOR_one_term_presidency

```hoi4
COLDWAR_KOR_can_one_term_presidency = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_one_term_presidency_constitution_political_power_factor = 0.1 }
set_variable = { COLDWAR_KOR_one_term_presidency_constitution_stability_factor = 0.04 }
set_variable = { COLDWAR_KOR_one_term_presidency_constitution_bureaucracy_cost_multiplier_modifier = 0.03 }
```

### COLDWAR_KOR_parliamentary_democracy

```hoi4
COLDWAR_KOR_can_parliamentary_democracy = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_parliamentary_democracy_constitution_political_power_factor = -0.08 }
set_variable = { COLDWAR_KOR_parliamentary_democracy_constitution_stability_factor = 0.07 }
set_variable = { COLDWAR_KOR_parliamentary_democracy_constitution_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_draft_parliamentary
set_variable = { COLDWAR_KOR_charter_model = 2 }
```

### COLDWAR_KOR_cabinet_responsibility

```hoi4
COLDWAR_KOR_can_cabinet_responsibility = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_cabinet_responsibility_constitution_political_power_factor = -0.1 }
set_variable = { COLDWAR_KOR_cabinet_responsibility_constitution_stability_factor = 0.08 }
set_variable = { COLDWAR_KOR_cabinet_responsibility_constitution_bureaucracy_cost_multiplier_modifier = 0.04 }
```

### COLDWAR_KOR_consensus_presidency

```hoi4
COLDWAR_KOR_can_consensus_presidency = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_consensus_presidency_constitution_political_power_factor = 0.02 }
set_variable = { COLDWAR_KOR_consensus_presidency_constitution_stability_factor = 0.05 }
set_variable = { COLDWAR_KOR_consensus_presidency_constitution_bureaucracy_cost_multiplier_modifier = 0.08 }
set_country_flag = COLDWAR_KOR_draft_consensus
set_variable = { COLDWAR_KOR_charter_model = 3 }
```

### COLDWAR_KOR_coalition_veto_rules

```hoi4
COLDWAR_KOR_can_coalition_veto_rules = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_coalition_veto_rules_constitution_political_power_factor = 0.03 }
set_variable = { COLDWAR_KOR_coalition_veto_rules_constitution_stability_factor = 0.06 }
set_variable = { COLDWAR_KOR_coalition_veto_rules_constitution_bureaucracy_cost_multiplier_modifier = 0.08 }
```

### COLDWAR_KOR_constitution_referendum

```hoi4
COLDWAR_KOR_can_constitution_referendum = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
NOT = { has_country_flag = COLDWAR_KOR_ballot_pending }
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = -75
set_country_flag = COLDWAR_KOR_ballot_pending
country_event = { id = COLDWAR_KOR_transition.30 days = 30 }
```

### COLDWAR_KOR_impartial_election_board

```hoi4
COLDWAR_KOR_can_impartial_election_board = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_ratification_passed
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_impartial_election_board_election_administration_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_impartial_election_board_election_administration_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_impartial_election_board_election_administration_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_constitutional_order
clr_country_flag = COLDWAR_KOR_constitution_yushin
clr_country_flag = COLDWAR_KOR_constitution_controlled_fifth
clr_country_flag = COLDWAR_KOR_nationwide_martial_law
```

### COLDWAR_KOR_uncensored_press

```hoi4
COLDWAR_KOR_can_uncensored_press = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_uncensored_press_press_rights_research_speed_factor = 0.03 }
set_variable = { COLDWAR_KOR_uncensored_press_press_rights_trade_opinion_factor = 0.04 }
set_variable = { COLDWAR_KOR_uncensored_press_press_rights_political_power_factor = -0.04 }
set_country_flag = COLDWAR_KOR_press_protected
```

### COLDWAR_KOR_accountable_intelligence

```hoi4
COLDWAR_KOR_can_accountable_intelligence = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_accountable_intelligence_intelligence_law_encryption_factor = 0.04 }
set_variable = { COLDWAR_KOR_accountable_intelligence_intelligence_law_intel_network_gain_factor = -0.04 }
set_variable = { COLDWAR_KOR_accountable_intelligence_intelligence_law_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_security_warrants
```

### COLDWAR_KOR_independent_constitutional_court

```hoi4
COLDWAR_KOR_can_independent_constitutional_court = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_independent_constitutional_court_court_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_independent_constitutional_court_court_political_power_factor = -0.04 }
set_variable = { COLDWAR_KOR_independent_constitutional_court_court_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_judicial_review
```

### COLDWAR_KOR_civilian_appointments

```hoi4
COLDWAR_KOR_can_civilian_appointments = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_civilian_appointments_appointment_law_army_org_factor = -0.02 }
set_variable = { COLDWAR_KOR_civilian_appointments_appointment_law_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_civilian_appointments_appointment_law_personnel_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_civilian_appointments
```

### COLDWAR_KOR_retire_political_networks

```hoi4
COLDWAR_KOR_can_retire_political_networks = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -2 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_retire_political_networks_officer_settlement_army_org_factor = 0.05 }
set_variable = { COLDWAR_KOR_retire_political_networks_officer_settlement_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_retire_political_networks_officer_settlement_personnel_cost_multiplier_modifier = 0.08 }
set_country_flag = COLDWAR_KOR_officer_networks_retired
add_timed_idea = { idea = COLDWAR_KOR_officer_retirement_disruption days = 180 }
```

### COLDWAR_KOR_staged_officer_retirement

```hoi4
COLDWAR_KOR_can_staged_officer_retirement = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_staged_officer_retirement_officer_settlement_army_org_factor = 0.06 }
set_variable = { COLDWAR_KOR_staged_officer_retirement_officer_settlement_stability_factor = 0.01 }
set_variable = { COLDWAR_KOR_staged_officer_retirement_officer_settlement_personnel_cost_multiplier_modifier = 0.12 }
set_country_flag = COLDWAR_KOR_officer_retirement_schedule
```

### COLDWAR_KOR_parliamentary_audits

```hoi4
COLDWAR_KOR_can_parliamentary_audits = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_parliamentary_audits_budget_oversight_interest_rate_multiplier_modifier = -0.2 }
set_variable = { COLDWAR_KOR_parliamentary_audits_budget_oversight_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_parliamentary_audits_budget_oversight_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_assembly_audit_rights
```

### COLDWAR_KOR_restore_labour_bargaining

```hoi4
COLDWAR_KOR_can_restore_labour_bargaining = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_restore_labour_bargaining_labour_law_stability_factor = 0.03 }
set_variable = { COLDWAR_KOR_restore_labour_bargaining_labour_law_social_cost_multiplier_modifier = 0.04 }
set_variable = { COLDWAR_KOR_restore_labour_bargaining_labour_law_civilian_factories_productivity = -0.02 }
set_country_flag = COLDWAR_KOR_lawful_labour_bargaining
```

### COLDWAR_KOR_prepare_local_councils

```hoi4
COLDWAR_KOR_can_prepare_local_councils = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_temp_variable = { treasury_change = -1 }
modify_treasury_effect = yes
set_variable = { COLDWAR_KOR_prepare_local_councils_local_government_agricolture_productivity_modifier = 0.03 }
set_variable = { COLDWAR_KOR_prepare_local_councils_local_government_stability_factor = 0.02 }
set_variable = { COLDWAR_KOR_prepare_local_councils_local_government_bureaucracy_cost_multiplier_modifier = 0.04 }
set_country_flag = COLDWAR_KOR_local_autonomy_prepared
```

### COLDWAR_KOR_constitutional_security

```hoi4
COLDWAR_KOR_can_constitutional_security = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_constitutional_security_transition_phase_political_power_factor = 0.0 }
set_variable = { COLDWAR_KOR_constitutional_security_transition_phase_bureaucracy_cost_multiplier_modifier = 0.0 }
set_country_flag = COLDWAR_KOR_civilian_control
clr_country_flag = COLDWAR_KOR_transition_open
```

### COLDWAR_KOR_orderly_handover

```hoi4
COLDWAR_KOR_can_orderly_handover = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_lawful_election_completed
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
add_political_power = 75
set_country_flag = COLDWAR_KOR_lawful_handover
```

### COLDWAR_KOR_defend_new_order

```hoi4
COLDWAR_KOR_can_defend_new_order = {
original_tag = KOR
IMP_is_1970_scenario = yes
is_subject = no
has_country_flag = COLDWAR_KOR_constitutional_order
}
# One-time completion leaves; new programme/offer handlers remain separate.
set_variable = { COLDWAR_KOR_defend_new_order_democratic_safeguards_political_power_factor = -0.03 }
set_variable = { COLDWAR_KOR_defend_new_order_democratic_safeguards_police_cost_multiplier_modifier = 0.03 }
set_variable = { COLDWAR_KOR_defend_new_order_democratic_safeguards_drift_defence_factor = 0.08 }
set_country_flag = COLDWAR_KOR_democratic_safeguards
```
