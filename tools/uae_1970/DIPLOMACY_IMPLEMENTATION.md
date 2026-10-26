# UAE 1970 decisions and agreements: implementation interface

Implementation authorized by the user's approval to code the approved concept. `diplomacy.py` reads the immutable design passed by the root compiler and returns eight uniquely owned output paths; it never writes loaded files itself. `test_diplomacy.py` builds the current module in memory and executes a deliberately bounded subset of the emitted native AST.

## Integration points

- Call `COLDWAR_UAE_init_british` in UAE scope after the new-1970 scenario has created the actual ENG subject relation. Repeated calls do not recreate an accepted replacement or a fulfilled schedule. The root compiler also owns a narrow post-alignment integration hook.
- Call `COLDWAR_UAE_british_tick` / its alias `COLDWAR_UAE_diplomacy_tick` in UAE scope on daily/load reconciliation. It delivers the current schedule, cleans expired or obsolete offers, maintains both treaty displays, observes actual oil-price movement and opens the defined historical crisis windows.
- `COLDWAR_UAE_sync_treaty_spirits` reads actual relation and current treaty state. Starting, dated-withdrawal and renewed-protection UAE ideas each carry the same `political_power_factor = -0.10`; exactly one is present while the corresponding British subject arrangement is active. Fulfillment and friendship carry no such penalty. The root compiler must not add another Treaty Dependence carrier.
- Focus completion may call `COLDWAR_UAE_send_protection_offer`, `COLDWAR_UAE_send_early_handover_offer` and `COLDWAR_UAE_send_friendship_offer` only after setting its successful `COLDWAR_UAE_done_<suffix>` marker. Failed/unpaid focus completion must not dispatch an offer.
- Other generated dispatchers have the same `COLDWAR_UAE_send_<family>_offer` convention. Families whose descriptive name already ends in `_offer` retain that suffix (for example `COLDWAR_UAE_send_exchange_offer_offer`). The decisions invoke their actual generated provider.
- Root provides `COLDWAR_UAE_<political group>_government` and `COLDWAR_UAE_refresh_programmes`.
- Politics provides `COLDWAR_UAE_convene_constitution`, `COLDWAR_UAE_organise_association` and `COLDWAR_UAE_accept_cabinet_bargain`. Politics owns `COLDWAR_UAE_cabinet_active` and its office/succession lifecycle; this module owns the +3% bureaucracy burden enabled only by that flag and monarchy government.
- Root consumes once-earned remedy flags: `COLDWAR_UAE_mediate_settled`, `COLDWAR_UAE_court_settled`, `COLDWAR_UAE_charity_registered` and `COLDWAR_UAE_cabinet_settled`. The first three come from guarded paid settlements/courses; the cabinet helper owns actual negotiated appointment.

## Authoritative British state

Both countries start with the announced-withdrawal spirit. The canonical fixed ENG–UAE relation and its monotonic `COLDWAR_UAE_treaty_nonce` identify the current record. Its origin is the 1968 policy; its announced horizon is the end of 1971. The visible exact **historical scenario handover: 1 December 1971** is not represented as a precise treaty already signed in January 1970.

The default due handler requires actual British subject status and the current schedule. It requires no focus, Emirati request or fresh UK approval. It executes only `ENG = { end_puppet = UAE }`, confirms actual independence, consumes the schedule and updates both treaty displays. It does not pay money, spawn forces, form the federation, alter oil, reset GDP, or replay national gains. Another overlord invalidates the British record rather than being released by it.

Accepted renewal clears the old release schedule. Unsigned/refused/expired proposals never pause it. An accepted relative transition uses an offer-frozen date; 360 days follows MD's existing `global.date + 8.64` convention. Dates/review dates are mirrored to ENG and read through native `GetDateStringNoHourLong`. Native timed-idea expiry does not perform release.

Every British policy offer captures the current treaty nonce and checks it again at acceptance. A current policy negotiation is shared across both initiators and all policy families, so the UK and UAE cannot open overlapping policy offers. Co-financing is a separate financial offer and still checks the treaty version. A signed replacement makes older-context popups stale even before periodic cleanup. A deadline already due cannot be postponed by an old response.

## All 40 decisions

Every approved decision has an executable provider and finished English description. Payment courses freeze their price when started and apply their payment/reward together only on successful completion. Current government, once/cooldown flags and project eligibility are checked again. Cancellation or an unpaid completion grants no effect. Non-executing native completion previews show the actual programme, duration, treasury debit, experience, productivity or queued port construction.

The required founders' settlement has nonzero AI willingness. Its two charter choices retain their acceptance weights and one consumed meeting cannot switch their exclusive flags afterward. Other diplomatic/manual political decisions remain player-controlled. British response weights favour the historical timetable: practical handover rather than immediate release, and refusal of an unsolicited retained-protection departure from that timetable. Human options are unchanged.

Recurring local meetings also use pending windows and round-specific event IDs. They cannot spend a later price quote, resolve the same local crisis twice, withdraw already removed reserve principal or enact a settlement after a party/authority change. Internal ruler choices are decisions of the UAE player; the module does not simulate a separate foreign player for each emirate.

Recipient country events check sender, partner, exact round, pending/expiry state, current earned provider/government and actual funds/stock where applicable. Refusal does not charge the treasury. Bahrain/Qatar choose their own representation or association; there is no unilateral annexation. Both full charter acceptances are needed for the root's conditional broad-settlement investment capacity. Association remains distinct. Charter preparation invoices use the symmetric 2% offer-GDP amount.

Counteroffers are not imposed terms. Iran's narrower Abu Musa proposal requires its own current UAE confirmation and leaves the Tunbs dispute unresolved. The British independent-friendship counterproposal requires UAE confirmation before immediate release and friendship acceptance; declining preserves the prior schedule. All such confirmations are round-bound and once-only.

## Numeric native integrations

| Integration | Executed native form / values |
|---|---|
| Historical fixed GDP invoices | Root-frozen `COLDWAR_UAE_start_gdp = 0.686`; 1%=0.00686bn, 2%=0.01372bn, 3%=0.02058bn, 5%=0.03430bn |
| Offer-GDP invoices | `gdp_total` in country scope, frozen at offer/start; equity 10%, technical/training/Arab exchange 2%, airline 5%, Kuwait financial support 3%, civil protection 1% |
| Money | Signed `treasury_change` through native `modify_treasury_effect`; sufficient funds checked with `compare = greater_than_or_equals`; no automatic borrowing |
| Productivity | `temp_productivity_change = 10`, `flat_productivity_change_effect = yes`; +10 points per controlled state, not +10% |
| Procurement | Seller quotes **1,000 `infantry_weapons_1` (1965) for $0.25bn**; buyer separately confirms; live seller stock and buyer funds checked; native `send_equipment` subtracts existing seller stock and transfers it. Numeric package follows existing `COLDWAR_USA_gulf_events.21`, not a new equipment type |
| British co-finance | UK −0.25bn / UAE +0.25bn, once per programme, actual accepted compact and successful Enduring Compact provider required |
| Reserves | Deposit exactly 5% frozen start GDP; withdraw all principal or one 0.03430bn standard deposit when covered; debit the ledger and credit treasury in the same transaction; no synthetic return |
| GCC | Each accepting participant pays 2% of its own frozen offer GDP; UAE entry charged only if not yet a member; native `idea_gcc_member_state` maintains the existing global member array and its existing modifiers; no automatic faction |
| OPEC | `mdcw_cw_start_opec_vote` with vote type3; use native membership/vote/cooldown guards; existing supply-restraint flag and penalties remain native, not duplicated |
| Downturn availability | Observe native `global.mdcw_cw_oil_ratio`; a fall below 80% of the recorded annual benchmark opens the response. This is a new local availability observer, not an existing native slump trigger or a replacement world price model |
| Port | State179, verified coastal province3725; current UAE ownership/control and native province-specific free capacity required; queue one ordinary naval-base level, +15% port construction speed365d. State180/province3689's existing level10 is not used |
| Kuwait access | Actual bilateral `give_military_access` in the appropriate direction. Existing units remain player-controlled; no spawned army or automatic declaration/entry into war |

API source anchors are recorded in the design audits. Current providers include `00_money_system.txt` (GDP/treasury), `00_economic_system_utilities.txt:2–9` (flat productivity), `mdcw_cold_war_effects.txt:1468–1479,1781–1865` (effective oil ratio/OPEC), `common/ideas/Factions.txt:114–143` (GCC), `events/COLDWAR_USA_gulf_events.txt:462–484` (native stock transfer), and `map/definition.csv:3726` plus state179 history (coastal Dubai3725). Installed trigger documentation specifies province-aware `free_building_slots` at2901–2913.

## Popup identity and limits

Each offer/meeting family has 128 non-reused event rounds. A popup's event ID therefore carries immutable round identity; a mutable country variable alone is not claimed to snapshot an event instance. Exhaustion disables further proposals instead of recycling a stale event ID. The bound is deliberately generous for the intended campaign, but is finite and is not an assertion of unlimited negotiations. There are 4,480 generated events, including seller/buyer and counterproposal confirmations.

## Verification

`python tools/uae_1970/test_diplomacy.py` passed **19** focused emitted-AST cases, with zero errors. The cases cover automatic independence, idempotence, same-family and cross-family stale responses, shared policy locks, due-date races, exact/insufficient funds, duplicate grant rejection, recipient-approved productivity, stock-backed two-step procurement, interrupted courses, reserve conservation, guarded port queues, own-GDP GCC fees, native price observation/OPEC delegation, domestic authority changes, Kuwait access, both counteroffer flows, and AI founders' reachability.

This establishes generator/source behavior for the exercised AST subset. It does not establish HOI4 loading, native tooltips, all economic formulas, save migration or multiplayer delivery. Native economy/UI and other-module political helpers are explicit boundaries of this harness; the root's separate validators and politics/focus tests cover their own source contracts. A live HOI4 test remains required before claiming engine verification.
