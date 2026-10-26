# COLDWAR_USA: resistance without an existing Kurdish country

Bounded source research, 18 October 2026. Concept only; no authoring preview or loaded mod files changed. This note supersedes any assumption that native resistance is impossible in Iraqi core states.

## Native core resistance is supported

The installed game's primary generated documentation explicitly says `force_enable_resistance` works even on a core or when the normal resistance check fails: `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/effects_documentation.html:3826–3836`. It is a state effect. `start_resistance` is documented at6967–6975 and is expressly paired with force-enable for otherwise ineligible cores. Neither activation requires an already existing Kurdish country.

Main MD directly demonstrates this exception. Relative to `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`:

- `events/protests.txt:30–43` chooses an owned, controlled core, force-enables resistance against the owning country, starts it and sets resistance50. The spread event repeats this with60 at75–87.
- `events/Ghana.txt:31–36` and64–68 enable resistance, start it and set an initial value without first creating a separatist country.

For a USA-originated intervention, specify IRQ as the occupier. Copying `force_enable_resistance = ROOT` from an Iraqi event into USA scope would point at USA instead. Always recheck the individual state's current IRQ ownership/control, eligible local grievance and absence of a respected settlement before affecting it. Iraqi cores need not be removed.

## Binding a resistance identity

The `occupied` field of force-enable is a filter, not an assignment. `occupied_country_tag` is a read-only comparison trigger in `triggers_documentation.html:5797–5802`; no separate `set_resistance_country_tag` effect was found in the installed effect documentation.

The supported binding candidate is `start_resistance = COUNTRY`. Vanilla `common/operations/LaR_FRA_operations.txt:46–69` pairs force-enable filters for ENG/SCO, ENG/WLS and ENG/NIR with `start_resistance = SCO`, WLS and NIR. Vanilla `common/scripted_effects/POL_scripted_effects.txt:53–62` explicitly uses `start_resistance = POL` to swap Danzig's resistance identity to Poland. This is stronger evidence than assuming that a force-enable filter alone sets identity.

An IRQ/KUR or IRQ/PUK pairing therefore has a native foundation, but each location needs the appropriate core tag and an eventual runtime check of `occupied_country_tag`. Workspace states164/633/630 have KUR cores;1078 has a PUK core in its1970 block. Starting resistance with `yes` or an inferred self-country identity must not be advertised as a guaranteed KUR/PUK uprising.

## Strength, target and escalation are different mechanics

Primary effects documentation supports state `set_resistance` (6598–6603), `add_resistance` (1839–1844), and `add_resistance_target` (1846–1858). Values are resistance points on the0–100 scale. The target effect supports a removable ID, occupier/occupied filters, duration and tooltip.

`add_resistance_target = { amount = 80 }` adds80points to the existing target; it does not set the final target to80. A proposal should specify a bounded additional contribution, or explicitly design a new reconciliation formula which includes Iraqi countermeasures. Automatically forcing the final target back to80 would defeat counterplay. Repeatedly setting current resistance back to60 would similarly erase paid Iraqi reductions. Initial strength should be once-only; subsequent support, decay and countermeasures need explicit bounded rules.

The state target is not a hard maximum. No native per-state resistance cap or per-state generic-uprising-disable effect was found. Setting a desired target80 does not prove that other systems cannot push resistance above90.

Main MD's thresholds have substantial real consequences in `common/resistance_compliance_modifiers/resistance_modifiers.txt`:

- 25: garrison penetration bonus (54–62).
- 50: increased damage to garrisons (64–72).
- 75: controller movement and supply−50%, attrition modifier0.30, disabled strategic redeployment (75–85).
- 90: a **core-group** threshold starts a country/revolt handler (89–146). The handler transfers controlled states sharing `occupied_country_tag` (255–277), creates2–6 fully equipped resistance units per eligible state (286–299), and declares war if necessary (332–335).

Thus100% is not merely a dramatic unrest label, and the90 handler is not inherently confined to the intended northern map. Its group may include other states. A dedicated northern uprising mission around80 needs explicitly authored coordination with that handler, or proven isolation of the resistance group and accepted native consequences. A daily clamp alone cannot prove safe ordering against threshold callbacks. The handler's own documentation allows an `enabled` condition, but introducing a scoped coordination guard is new integration requiring review, not an existing COLDWAR API.

## Iraqi counterplay and financial costs

Native state `add_resistance = -N` and timed negative target contributions provide real counter-effects. Occupation-law effects are documented at `effects_documentation.html:6416–6443`: state overrides must be invoked with the occupying country as the previous scope. Actual law availability and garrison assignment must be checked. Workspace `common/occupation_laws/occupation_laws.txt:63–95` shows missing-garrison consequences and the default no-garrison law; that default has no compliance gain and no required garrison. Force-enabling a core is not proof that the player has supplied a working garrison.

Do not copy `set_garrison_strength = 1` as a paid force-creation mechanism: documentation6106–6111 describes setting initial garrison strength, not deducting a verified manpower/equipment invoice.

For a funded counterinsurgency programme, both financial keys are registered in workspace `common/modifier_definitions/money_modifier_definitions.txt:23–49`:

- `army_personnel_cost_multiplier_modifier` affects the country's native army-personnel component.
- `equipment_cost_multiplier_modifier` affects the country's native operative equipment component, including stockpile/deployed equipment.

Consumers are `common/scripted_effects/00_money_system.txt:3182–3197`; these are additive inputs inside their respective `(1 + modifier)` multipliers. Other general-personnel, GDP, inflation, mobilization and wartime factors remain in the calculation. Native land-personnel wartime scaling is1.20 at3216–3219. Adding a counterinsurgency+30% to an existing+100% army-personnel modifier changes that component from2.0 to2.3 times its unmodified base, not an extra30% of total defence spending. These country modifiers are not a separate geographically exact Kurdish-garrison bill.

A quoted treasury invoice can accompany temporary personnel/equipment surcharges for the same operation. Describe the fixed operation expenditure and ongoing national military overhead separately; do not charge the same item twice. Programme funding, expiry and repeat limits are new transaction logic. High costs can cause a deficit, but do not guarantee debt independently of taxation, exports, reserves and forces. Native weekly borrowing only follows negative treasury (`00_economic_system_utilities.txt:29–42`).

## Aid when no recipient country exists

Do not send equipment or treasury to an absent KUR/PUK and call that actual delivery. An initial cash-only clandestine operation is viable without a recipient-country grant. Removing real donor equipment for a committed clandestine cache is also supported: primary `effects_documentation.html:1171–1181` explicitly allows negative `add_equipment_to_stockpile` values; native MD `common/decisions/05_GRE_decisions.txt:578–580,600–604` checks stock and removes100 `infantry_weapons_1` items. Recheck the same equipment selection at delivery. Omit a producer restriction unless a matching stock check is actually available; an all-producer stock count does not establish sufficient USA-produced items.

A later cache delivery to a newly existing actor needs a new bounded ledger, with permanent transaction IDs, no second donor deduction and no repeated equipment creation. That storage/delivery contract is not already an MD helper.

## Cleanup and confidence boundary

Use an ID for the intervention's own target contribution and remove only that ID (`effects_documentation.html:5390–5396`). Force-enable overrides are keyed by occupier/occupied, not by an arbitrary COLDWAR provider. Record whether this crisis created the forced resistance, respect overlapping native protests, and avoid cancelling another provider's unrest or ordinary foreign occupation. Main MD `05_china.txt:26702–26704` demonstrates clearing a force-enable override and cancelling resistance after integration; `clear = yes` removes an override, rather than establishing a permanent immunity.

Native core resistance and financial primitives are source-confirmed. Exact resistance identity, garrison UI/assignment, shared-provider cleanup, threshold ordering, a bounded Kurdish uprising and save/load behavior remain runtime/integration work. Newly authored political organization pressure may supplement the system, but must not be presented as native resistance when the engine resistance meter is not actually enabled.
