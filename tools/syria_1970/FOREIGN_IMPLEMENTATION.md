# Syria 1970: foreign contracts and limited war

`foreign.install(root, data)` emits only the files named `COLDWAR_SYR_foreign*`.
It replaces the structured one-time reward for `COLDWAR_SYR_levant_02` with the
real war-goal adapter. The main compiler owns focus costs and programme rewards.

The module implements all 28 foreign/operational decisions in the approved
catalogue, plus Lebanese invitation revocation and Iraqi pipeline suspension.
The stable `COLDWAR_SYR_WAR.1`–`.14` event IDs are preserved. Additional
`COLDWAR_SYR_FOREIGN` events provide actual recipient responses and bounded
offer expiry. All loaded localization is English.

## Runtime hooks

- `COLDWAR_SYR_foreign_init`: initialize current-GDP operational price caches.
- `COLDWAR_SYR_foreign_weekly`: refresh prices, clean invalid operations, execute
  actual Iraqi transit payments, and detect a bounded post-1980 liquidity/debt
  crisis. The main country on-actions call these hooks only in the 1970 scenario.
- `COLDWAR_SYR_request_sanctions_review`: domestic security operations can invite
  a US response. The US chooses whether to spend the normal 35 PP on native
  Imperia diplomatic sanctions. The default response declines sanctions.

## Native interfaces and units

- `common/scripted_effects/00_budget_effects.txt`: `modify_treasury_effect` and
  `modify_debt_effect` receive billions of dollars. Neither helper establishes
  affordability; the Syrian adapters check it again at execution.
- `common/wargoals/00_invasion.txt`: `take_state_focus` and `annex_everything`
  are existing types. If Israel owns Golan state 587, the goal targets that
  state. If Israel only occupies Syrian-owned Golan, the engine fallback is a
  broader conquest goal. Its scope is disclosed in the tooltip. Both last
  365 days, and neither automatically declares war.
- `common/scripted_effects/00_scripted_effects.txt`:
  `add_threat_from_wargoal_effect` uses category 0 for the state goal and 2 for
  conquest. Cold War war-relation shocks remain owned by existing on-actions.
- `common/scripted_effects/mdcw_cold_war_effects.txt`:
  `mdcw_cw_start_pending_program` starts Soviet programme 6, size 1, with the
  native capacity, duration, training and recurring-cost consumers. Soviet
  donor scope enters from Syrian recipient scope, making PREV the recipient.
  The donor spends 25 PP; Syria pays hosting only after a new programme starts.
- `common/scripted_effects/IMP_sanctions_support_effects.txt` and
  `common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt`:
  sanction arrays, native opinion penalty and the Cold War sanctions hook are
  reused. There is no substitute sanctions spirit.
- `common/scripted_effects/00_money_system.txt`: existing military, medical,
  bureaucracy, social and interest readers consume the timed idea modifiers.
  Interest premiums are percentage points, not multiplicative percentages.
- `update_state_variables` refreshes actual project buildings and GDP. Energy
  recalculation is guarded by `energy_state_bases_initialized`.

Operational appropriations use 0.75%, 0.50% or 0.25% of current GDP as specified
in the catalogue. At the historical $2.140 billion GDP, the main appropriation
is $0.01605 billion. Decision costs were not raised by the later user instruction
to price paid focuses at $2–7 billion.

## Consent and lifecycle

Every foreign proposal records its own pending flag and expires after 90 days.
Popup options repeat the full matching-offer and funding checks when executed.
The first/default option is safe refusal or cancellation where a financial or
operational commitment would otherwise occur. Failed preparations refund PP and
remain retryable; successful once-only decisions record an explicit completion
flag instead of permanently consuming a failed engine decision.

The development loan transfers $0.20 billion from the Soviet treasury and adds
equal Syrian cash and debt. A civil-project donor pays $0.20 billion into a
reserved, once-only project contract; Syria builds one eligible workshop or
road improvement, or returns the reserve. The grant is not also spendable cash.
Iraq pays actual monthly transit fees while its contract operates and funds are
available. The Lebanese invitation and paid deployment are separate stages.

Disengagement and Golan offers establish negotiating willingness only. They
never transfer land or execute white peace. Actual governments and coalition
war leaders retain the normal diplomatic settlement process. The standard
Egyptian staff-cooperation decision also works without an offensive mandate;
its paid temporary planning package cannot stack with the limited-war package
or the existing Egyptian October coalition idea.

Operational cleanup removes temporary advantages and their spending burdens
together. It preserves unused appropriations awaiting cabinet authorization,
durable focus learning, actual public debt and emergency-credit interest terms.

## Verification

Run `python tools/syria_1970/test_foreign.py` after compilation. Seven scenarios
execute the emitted goal, GDP-funding and cleanup scripts through a small
documented-interface model. They cover ownership-sensitive goals, ongoing war,
alliance/recovery invalidation, exact-balance funding, money spent during
preparations, one-time grants, retry, unused appropriations and debt preservation.
The main independent content validator also checks emitted IDs and references.

These are source/scenario checks. HOI4 popup scopes, actual native assistance,
save/reload, multiplayer responses and economic ticks still require engine tests.
