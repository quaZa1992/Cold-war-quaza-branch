IMPERIA COLD WAR: Independent USA implementation support

24 October 2026. This is a source audit and migration recommendation record. It does not itself change loaded gameplay. The baseline is the immutable 229-focus `current_inventory.json`, corresponding to tree SHA256 `479D4979B1B7574AC8F58E2943505DDC432DE1E563429C837E276D0E585C8DA8`. New implementation files may subsequently differ.

## Machine-readable records

- `building_slot_repairs.json`: all 48 baseline focuses with missing slots, exact raw focus and construction/container spans, existing fees, state/type groups, ownership/control checks and native capacity providers. The three slot-bearing focuses are recorded separately because they still need transaction review.
- `implementation_support_elections.json`: all 113 later-election nodes, exact party triggers, receipt/flag preservation, signed helper-to-consumed-variable mappings and proposed conservative lifetime classification.
- `implementation_support_diplomacy.json`: original acceptance and renegotiation event bodies, flags, signed helper deltas, payment helpers and consolidation rules.
- `tools/usa_1970_expansion/source_audit.py`: writes only these audit records. It never edits loaded game scripts. Its source spans are Unicode code-point offsets relative to each stored raw focus, not offsets into a moving live file.

## Building repairs

The complete baseline contains 51 focuses with 135 construction commands. Forty-eight focuses lack all matching slot grants, affecting 127 commands. N2, N3 and N6 contain slots for their eight commands, but slots alone do not prove ownership, control or capacity safety.

All 135 are fixed-state grants of one building level. There are no provincial, land-fort or coastal-fort grants in this tree. Twenty-three distinct target states are involved; all have USA ownership and controller in their inspected 1970 history. That does not prove runtime ownership after wars, cessions or civil wars.

State 775 in NIX_E2 receives a factory and infrastructure. State 769 in the 1976 Democratic urban-development focus receives a factory and infrastructure through separate blocks. State 811 in the 1984 Republican high-technology focus receives an office and an arms factory. Group every same-state asset when checking capacity, and keep the entire package with its setup payment under one transaction receipt. Do not grant one subset and charge for the whole package.

`common/buildings/00_buildings.txt` defines separate native maxima: civilian factories and offices 50; arms factories 35; dockyards 20; infrastructure 6; agriculture districts 10; fossil powerplants, nuclear reactors and renewable infrastructure 20; fuel silos 5; reinforced electrical grid 1 with `infrastructure_keystone` grouping. `common/defines/MD_defines.lua:284` caps shared slots at 80. Matching extra slots do not override these caps or grouping restrictions.

The supplied `free_building_slots` triggers conservatively require current capacity before adding the extra slot. This is safe against disappearing grants but can reject a full shared-slot state even where an extra slot could have created room. Do not claim a model of post-grant capacity without testing the native engine. Ownership/control and capacity remain independent requirements.

The instant construction commands and reviewed USA bridge helpers do not call an implicit Treasury payment helper. The focus already sets its own `treasury_change` before `modify_treasury_effect`. The latter, at `common/scripted_effects/00_budget_effects.txt:1487`, only adds the supplied amount and refreshes the money dirty flag, unless `MD_skip_treasury_cost` is set. Do not add a second fee from the pricing comments at the top of the buildings file.

Preserve the approved native domestic deficit pattern. The national-tree project contract explicitly says newly authored focuses use native deductions without a Treasury prerequisite by default. This audit does not authorize adding affordability gates to those focuses. Preserve any separately approved bilateral funding contract.

## Election programme gates and lifetime classification

The 113 nodes are 14 zero-cost election receipts, 92 partisan programme focuses and seven common national acts. Apply live party execution gates to the 92 partisan programme focuses. Keep the 14 historical results and seven shared institutions persistent.

The exact native triggers are:

- Republicans: `western_conservatism_are_in_power`, ruling-party slot 1, `common/scripted_triggers/01_political_triggers.txt:176`.
- Democrats: `western_liberals_are_in_power`, slot 2, `:183`.

The singular `conservatism` spelling is authoritative. Broad democratic outlook, coalition membership or party popularity is insufficient. The country starts with Republican slot 1; a Democrat can be present in the coalition without governing.

The audit proposes the following conservative split among the 92 partisan nodes:

- 41 enduring statutes, official institutions, lasting reorganisations, completed industrial conversions or resolved financial interventions: preserve their helper bundle.
- 44 ongoing appropriations, discretionary economic stances, diplomatic postures or strategic programmes: make the signed helper bundle follow the actual governing party.
- Seven ambiguous mixed bundles: preserve pending an explicit split, rather than invent a blanket reversal.

These are implementation classifications based on the actual names and reward scope. They are not claims that every historical programme legally ended when the opposing party took office. The seven flagged nodes are State Export Development Grants; Economic Stimulus Appropriations Act of 1977; Kemp-Roth Growth Program; Modernize the Social Contract; Enforce Budget Rules; Return Power to the States; and Globalization Adjustment and Digital Classrooms.

All 113 records include their exact helper deltas and persistence recommendation. No helper amount was left unmapped. One-time buildings, slots, PP, stability, XP, paid money, party popularity, Congress and faction changes remain earned. Native law swaps, the Department of Energy and formal institutions must not be replayed or erased on a later party change.

Four key baseline receipt flags are shared with other mechanics. `USA_1970_congressional_vietnam_review` unlocks Vietnam decisions alongside `USA_1970_executive_vietnam_strategy`; the latter can also come from the Nixon programme. `USA_1970_covert_oversight` can come from the 1984 Democratic programme or D3 and is consumed by intelligence decisions. Do not clear those flags simply because one party loses office. A shared receipt is not an attributable numerical contribution.

For active numerical bundles, retain a ledger of the previously applied contribution per consumed USA variable. Recalculate the desired contribution from completed eligible programmes, adjust only the difference, and store the result. Do not overwrite the whole native variable, which also includes the difficult start, other focuses, decisions and diplomacy. Initialize an old-save ledger from completed active programmes whose old deltas are already embedded; then reconcile, rather than adding them again.

Do not reverse random or clamped systems by applying their opposite helper. Congress mutations use random factors and clamps, economic regulation is clamped, and Wall Street helpers also mutate strength. Such an operation cannot reconstruct the original state.

## Immediate and fallback hooks

The authoritative generic dispatcher is `set_leader` in `common/scripted_effects/00_leader_setup_scripted_effects.txt:9`. In its normal path it updates the political outlook and calls `set_leader_[TAG]` using the original tag. USA's specific dispatcher is `set_leader_USA` in `common/scripted_effects/USA_political_leaders.txt:1`.

The narrow immediate hook belongs at the end of the complete `set_leader_USA` function, outside its special-successor if/else chain, guarded by the actual USA/1970/initialisation conditions. Hooking only `USA_1970_set_scenario_leader` misses the special-successor paths and governments outside the two major parties. Add an idempotent fallback to the already existing `on_weekly_USA` effect in `common/on_actions/mdcw_1970_USA_on_actions.txt`, preserving its Vietnam-overextension maintenance.

Neither hook should call a focus completion reward or setup effect. Sync only current modifiers and declared weekly streams.

## Legacy diplomacy consolidation

Old sending focuses already obtain real consent. Their accepted flags prove the old terms, not acceptance of a new paid programme.

| Old source | Existing recipients and receipts |
|---|---|
| F4 Atlantic | ENG, FRA, GER, CAN: `USA_1970_atlantic_bargain_partner`; USA aggregate `USA_1970_atlantic_bargain_applied` after two registrations |
| F5 triangular | SOV, CHI: `USA_1970_theater_trade_partner` |
| F7 Israel | ISR: `USA_1970_israel_security_partner`; USA `USA_1970_israel_package_completed` |
| F8 mediation | ISR, EGY, JOR: `USA_1970_broker_partner`; USA `USA_1970_broker_partner_found` |
| F9 Arab trade | SAU, EGY, KUW: `USA_1970_arab_compact_partner`; USA `USA_1970_arab_compact_applied` |
| D6 maritime | ENG, JAP, PHI: `USA_1970_maritime_basing_partner`; USA `USA_1970_basing_access` |
| E9 commercial, plus later globalisation sender | CAN, MEX, later CHI: `USA_1970_commercial_partner`; USA `USA_1970_commercial_package_applied` |

Do not map one partner's receipt to every recipient of a multilateral or aggregate offer. Do not infer acceptance from completion of the sending focus. Pending, refused, unavailable and accepted remain separate states.

Existing payment traps:

- `enbo_usa_send_monetary_package_to_israel_effect`, `mdcw_1970_aipac_consumed_helpers.txt:32`, already debits USA 5 and credits Israel 5, plus faction/influence effects. Calling it alongside the approved new setup charge would double-charge the player.
- `USA_1970_register_arab_compact_acceptance`, `USA_1970_scripted_effects.txt:384`, debits USA 15 behind a once-only aggregate receipt.
- `USA_1970.101.a` charges USA 5 for renegotiated Atlantic terms.
- `USA_1970.141.a` charges USA 10 for renegotiated basing.

Retiring senders is insufficient if their already queued acceptance or renegotiation events can still execute. Guard or redirect those old option bodies consistently. Retain actual old payments, PP/XP, trade/access and historical receipts; do not execute them from treaty restoration. Do not remove access or old native trade arrangements merely because a new training programme temporarily suspends.

Nixon China/SALT channels, Beijing/Moscow summits, Okinawa consultation and ARVN assistance have their own offered/accepted/rejected/partner receipts. They grant old PP, stability, XP and USA policy deltas. New commercial, scientific or advisory programmes need new consent to their new terms, while their historical channels remain intact. Never replay a summit or old assistance acknowledgement to install a new paired spirit. The baseline Okinawa event in fact grants consultation/opinion/policy changes; its title alone is not proof of a territorial-transfer effect.

F10 and later policy decisions consume the old aggregate acceptance flags. Either preserve their safe historical meaning or migrate the readers to specific new active receipts. Removing old dispatchers while leaving those requirements untouched can strand existing content.

## Validation boundary

This support audit establishes source spans, exact trigger names, declared fees, helper consumers and migration design constraints. It does not establish live focus completion, event execution, tooltip rendering, native capacity behaviour, save migration or multiplayer stability. Independent emitted-code and in-engine checks remain separate evidence.
