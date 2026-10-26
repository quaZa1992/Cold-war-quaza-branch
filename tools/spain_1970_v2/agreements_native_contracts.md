<!-- IMPERIA CW — Cold War: Spain V2 agreement provider and consumer evidence. -->
# Spain V2 agreements: native contracts

The immutable approved design is `approved_design.json`. `agreements.py` owns its
isolated `COLDWAR_SPR_v2_agreements` outputs and a narrow, idempotent patch of
`events/NATO_system.txt`. The root compiler calls every decision effect helper
once after its paid focus transaction succeeds. Politics calls
`COLDWAR_SPR_initialize_agreements` at initialization and
`COLDWAR_SPR_refresh_agreements` from its daily observer.

## Economic and procurement providers

* Treasury changes use `modify_treasury_effect` in `00_money_system.txt`.
  Every decision/recipient affordability comparison includes exact equality.
* Paid domestic energy decisions select an owned and controlled Spanish state,
  calculate price and duration with the current native `update_gui`, confirm the
  offer, and call `start_project_two`. Its native project decisions complete the
  building; no focus grants a reactor, fossil plant or mine. The current price
  array is 13=nuclear 14.40, 12=fossil 5.20, 15=uranium mine 6.00 billion per
  level before actual receiving/investing modifiers. `99_investment_scripted_effects`
  provides pricing, 15-slot allocation, timing, completion, cancellation and
  capital accounting. Completion removes the spent project principal; it does not
  refund the completed building price. Existing MD project rewards are preserved.
* `reactor1`, `country_can_build_nuclear_reactors`, ownership, control, slots,
  active project, bankruptcy and project-cap checks are retained. Fuel and staff
  requirements remain in `!_energy_effects.txt` and the native building system.
  The operating-generation focus gate requires positive consumed native
  `nuclear_energy_generation` and an owned, controlled reactor.
* Salamanca/90 is already the 1970 native surveyed district in
  `COLDWAR_quaza_imp_uranium_effects.txt`: two potential mine levels, four uranium
  per completed level. Survey repeats the deposit metadata only. Startup is not
  granted a mine or any raw uranium; the normal mine-production consumer runs
  after actual paid completion.
* Reserve-law adoption reads the actual next law's `available` block in
  `AA_law_military_ideas.txt`, charges its current 150 PP and calls
  `increase_conscription_effect`. It remains optional, once only and subject to
  conscription blocks and the all-volunteer doctrine.
* Equipment licensing uses the real diplomacy licence-production request. The
  exporter chooses equipment and accepts it; no invented generic licence or
  equipment is issued. The focus retains its separately compiled native licence
  production modifier. No duplicate licence menu or no-op decision is added.

## Consent and exact terms

Offers are recipient-owned events with 90-day pending flags, live sender/recipient
identity and eligibility, accepted receipts and execute-time guards. Silence and
refusal charge nothing. Duplicate acceptance cannot replay a transaction. A new
identical proposal can validly replace an expired one; responses do not carry a
separate cryptographic proposal generation identifier.

* US facilities: United States pays 1.50 billion; Spain receives 1.50; US military
  access lasts 720 days. Restricted facilities have the same temporary-access
  contract without that payment. Only access created by this agreement is removed;
  pre-existing access and subsequent NATO access are preserved.
* Exercises: each side pays 0.30 billion and receives 20 Army / 10 Air XP, once for
  the exercise family.
* Mediterranean and Maghreb projects: each side pays 0.50 billion; each receives
  office productivity +5% for 720 days. Accepted partners pay separately; the
  shared productivity idea does not stack multiple +5% bonuses on Spain.
* Ibero-American bond: Spain pays 2.00, borrower receives 2.00; Spain's real
  `given_bonds@borrower` increases by 2.00. Both native bond totals are recomputed
  with `calculate_new_bonds_held/owed`. Native `imp_bond_buyback` and bond sale
  read the same ledger. This is a face-value bilateral obligation, not an added
  ordinary MD public-debt charge or an invented interest stream.
* Trade talks establish a bilateral accepted negotiating channel; no unapproved
  free trade law, compulsory foreign construction, subsidy or modifier is added.
* Sahara conference/transition/presence agreements are reachable with either the
  Spanish or another participant's current administration. Every existing
  MOR/MAU/ALG/SHA participant must assent. Final transition protocol creates native
  non-aggression agreements with Spain, not a territorial transfer. Interim
  administration has a 720-day review receipt and reopening decision. No owned
  state, core, unit or foreign asset is transferred by these protocols. This is
  the conservative implementation authorized by the root after reviewing current
  map uncertainty.

## EC and NATO integration adaptation

The approved concept assumed there was no usable existing EC integration. Source
inspection found an active 1970 EC mode of MD's native EU system:
`COLDWAR_EC_1970_effects`, the startup adapter in `99_eu_scripted_effects`,
`Organizations.txt:EU_member` and `EU_voting_decisions:EU_apply_for_membership`.
The root explicitly approved reuse of that actual system instead of a parallel
organization. Spain's 70-day legal adjustment and every current real member's
assent provide native candidate status. Actual admission still uses the native
decision's 50 PP, Europeanism, peace, breach and influence requirements. Only a
genuine `EU_member` plus the completed Spanish consent/legal stage provides the
approved `COLDWAR_SPR_eec_membership` receipt, which is removed on departure. No
modern global activation or global founding-member setup is run by this module.

NATO uses `NATO_join_via_event` -> member/faction leader's `NATO.14` -> Spanish
`NATO.9` -> native `NATO_join`. The shared .14/.9 options were narrowly patched,
with root authorization, only for Spain in the 1970 scenario. Visibility and
execute-time guards require democracy, elections, actual eligibility, unexpired
pending status, a still-valid member/faction leader and peace; the final Spanish
acceptance also requires the same recorded sponsor. Leader response and final
admission cannot replay. Other countries and later starts retain their original
native behavior.

## Crisis lifecycle

No crisis idea is installed at initialization. Daily observers apply the 1973
oil shock (-10% civilian, -5% offices, 180 days) once in its window; the later 1979
supply shock uses 90 days if the paid contingency focus is applied and a controlled
owned reserve facility remains. The 1981 reconversion shock (-10% civilian,
+10% social expense, 365 days) is -5% civilian if the paid Reconversion Fund has
already applied. The original 1973 shock is never retroactively removed. Late
saves beyond each event window do not receive retrospective shocks. No recurring
monetary literals are introduced by this module.

`agreements_previews.json` supplies prospective native cost/reward snippets to the
root's non-executing focus preview. Event acceptance exposes native money, XP and
timed-idea effects in addition to concise numeric treaty terms.

Static parsing and rebuild checks establish source consistency only. HOI4 must
still verify target-decision UI, native own-country investment scheduling,
tooltips, live event scope, save/reload and multiplayer responses.
