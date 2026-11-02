IMPERIA COLD WAR: France 1970 foreign-policy mechanics reference

# Scope

Read-only mechanics review for a proposed France 1970 foreign-policy expansion. This documents source-supported effects and consumers in the loaded MD mod, not game-tested behavior. It does not add or change runtime code. Reference entries in `MECHANICS.json` include source paths and approximate line anchors.

# What the native systems actually do

## Bilateral access and military commitments

MD uses `give_military_access = TAG` in country scope. Its direction is explicit: that country grants access to the named tag. To suspend/revoke it, the donor code uses the recipient's `diplomatic_relation = { country = ROOT relation = military_access active = no }`. Docking rights use the same relation effect with `relation = docking_rights active = yes/no`. The UK-Egypt event `britain_md.31` has both an acceptance preview and a recipient event: Egypt grants British military access and docking rights, while the UK pays a GDP-based transfer and increases influence. This is a strong native model for a concrete access-for-funding offer.

`give_guarantee = TAG` is also present in native focus effects, including Afghanistan's protection path. A guarantee is a real military commitment that may pull France into a war. Use it only where that is the intended treaty term, with a named recipient's acceptance. Do not present it as a general friendship bonus. A signed treaty should store its own receipt; access and docking relations should be applied or suspended idempotently from that receipt and a clearly stated peace/eligibility guard.

## Aid and matched transfers

The native UK-Egypt agreement is the clearest transfer precedent. On acceptance, the UK scopes a treasury debit from its own GDP; Egypt receives the same amount, computed as `ENG.gdp_total * 0.02`. The effects are previewed under `custom_effect_tooltip = TT_IF_THEY_ACCEPT` before the recipient accepts. In current code, this is an upfront transfer, not a recurring stream.

For an ongoing French-funded programme, the loaded economy already aggregates `additional_income_rate` and `additional_expenses_rate` every weekly update. The runtime's France agreement pipeline and the USA agreement pipeline are examples of signed, computed weekly charges feeding that aggregator. A balanced bilateral transfer can debit the payer's additional expense stream and credit the recipient's additional income stream by the same nominal weekly amount, both under one durable signed-agreement receipt and the same activation guard. Calculate a GDP-based annual promise once from the payer's current GDP, divide by 52, and use that same value on each side. If each side recalculates its own GDP share, the amount paid and received will not match. Preview the payer and recipient rows separately with exact numeric values and retain the actual effects in the preview.

The two aggregation APIs add values to their respective country ledgers; the existing engine does not automatically link them into one transaction. The bilateral helper must do that pairing, prevent a one-sided stream when one country is absent or a treaty is suspended, and avoid replaying the setup debit when activity resumes. The money source's `apply_currency_multipliers` changes `resource_sale_rate` and its resource breakdown, not `additional_income_rate`; additional-expense inflation is applied earlier in the expense aggregator. Therefore an integration appended after the common expense multiplier can debit and credit the same nominal weekly amount without the resource-sale currency scaler changing it. Verify any new hook's exact insertion point and keep only the signed agreement streams in this pair; unrelated national modifiers can still change each country's overall income/expenses.

## Trade, export receipts, and commodity offtake

`set_improved_trade_agreement` is not a shipment or purchase contract. It applies mutual trade opinions, increments each side's signed-agreement count, and sets pair flags. I found no quantity, buyer, price, import-priority, or committed-delivery fields in that helper.

`resource_export_multiplier_modifier` is consumed by the resource-sale calculator as a multiplier on a country's actual exported resource quantities at global market prices. Type-specific modifiers such as `oil_export_multiplier_modifier` apply to that country's oil export sales. These affect realized sale receipts, not resource volume, a named buyer's imports, a bilateral price, or delivery to France. They are appropriate for a broadly named export-market settlement or exporter earnings programme, with wording that stays at that level. They are not a verified implementation of “France receives X oil/uranium from partner Y.”

The native `give_resource_rights` system lets a partner grant another country rights over a particular state, optionally restricted by resource. In the resource GUI this is an accepted request for rights; separate cancellation/revocation events exist. In the investment system, an investment project can build a uranium mine, update mine slots, and recalculate the mine output. These tools support a real investment/concession proposal if the state and resource are valid, but rights alone do not promise extraction, a fixed quantity, shipment to France, or market priority. Uranium must remain mine-based: the resource code explicitly says supply begins at zero, surveyed deposits do not grant history production, and only working built mines add uranium.

The resource definitions give a useful comparison for proposed African deals: NGR Zinder (state 329) has a documented deposit of 439.4 kt, three mine levels and 12 units per level; Gabon Highlands (1004) has 5.8 kt, one level and 3 units per level. The 1970 state histories do not start these uranium mines. The established investment UI and its capacity, rights, deposit, construction-cost and ownership checks should remain the route to production. A France-Niger package could offer a funded development grant, recipient-approved uranium resource rights, and a later investment decision or project. It must not instantly add a mine or guarantee French fuel. Gabon can be an exploration/technical-assistance option, but its coded deposit capacity is much smaller.

Iraq's state 171 Basrah begins with 39 oil; state 165 Kirkuk begins with 4. A source-backed oil offer can be framed as a development or export-revenue agreement, or as a cash transfer attached to access/industrial support. Do not call it an oil offtake unless a custom bilateral quantity-and-delivery consumer is built and tested. Any partner export modifier changes its market sale receipts; it does not reserve Iraqi oil for France.

## Technology and production arrangements

Finite `add_tech_bonus` and `add_doctrine_cost_reduction` are supported in the existing France and USA agreement generators. Use the real research category tags and finite uses. They are clean bilateral benefits when both parties receive distinct, named one-use research or doctrine support. A tech bonus is not tech sharing and does not transfer a technology already researched by the other country.

The native tech-sharing effect adds a country to a named, global technology-sharing group. The UK AUKUS focus/event adds the UK, USA and Australia to a group whose definition shares submarine-related categories at a 5% per-country bonus. That is group-wide sharing, not a bilateral French licence; adding France and a partner to an existing large group can disclose technology to third parties. A dedicated pair group would require a new group definition, explicit membership and exit/suspension lifecycle. Prefer finite named bonuses if a narrow bilateral research benefit is intended.

The modifier `license_production_speed` is consumed by licensed production lines, and MD uses it in several national programme modifiers. In the source search for this review I found no generic scripted effect that creates, transfers or accepts a production license. Therefore a focus can reward faster production on licenses the country already has, but should not promise the partner has issued a license unless the actual licensed-equipment action is separately handled and verified in game. A native tech-sharing group is not a production license.

## Equipment, infrastructure, and assets

`add_equipment_to_stockpile` supports adding to a country's stockpile and loaded effects also use negative amounts to remove stock. There are examples of explicit `has_equipment = { type < amount }` checks before a decision spends equipment. A one-off arms package is feasible as a recipient-approved, atomic transfer: verify the donor's stockpile first, remove exactly that amount from donor, add it to recipient, retain a producer tag, and preview both the debit and credit. Choose equipment that exists in the 1970 tree and cap quantities modestly. This is a real shipment; a permanent factory modifier is not.

Recipient-state industrial projects are also feasible. The French bilateral core already knows how to preview and grant buildings and shared slots. Every level, including infrastructure, needs its additional state shared slot in the same one-time transaction before construction, and the actual target state must pass ownership, control, full-control and physical building-cap checks. Do not use a generic market agreement as a proxy for investment in a named partner state.

# Candidate contract shapes for design

These are mechanics-first patterns, not approved numerical offers.

| Counterpart and purpose | Recipient's concrete benefit | France's concrete benefit | Source-backed mechanism and boundary |
| --- | --- | --- | --- |
| Niger uranium development | French-funded development transfer; optional local infrastructure after consent; a durable French uranium resource-rights receipt | Right to use the existing uranium investment interface in Zinder; optionally a finite nuclear-reactor research bonus | Rights and mine investment are supported; the 439.4 kt deposit has 3 levels at 12 units/level. No instant mine, output, fixed offtake, or exclusive shipment. Check deposit and mining system at execution. |
| Gabon exploration cooperation | Small grant or technical training support; local industrial/port asset with slots | A finite nuclear/energy research bonus and prospecting rights if legal under resource UI | State 1004 is coded at 5.8 kt uranium, one level at 3 per level. It is materially weaker than Niger for a production promise; frame as exploration/technical cooperation. |
| Iraq oil-field services | Recipient receives French-funded one-off equipment/infrastructure or equal-value weekly support; its market receipts may improve if export factors are used | Reciprocal military/docking access or a small finite energy/electronics research benefit | Native access/docking and matched treasury transfer are proven. Iraq's Basrah/Kirkuk oil exists; oil export-factor changes market receipts but cannot reserve France's imports. Avoid “X barrels for France.” |
| Libya refinery / port protocol | One-time construction or arms transfer and a matched operating payment from France | Limited access/docking rights or a narrow research benefit | Uses native construction, stockpile, treasury, and access effects. If changing Libyan oil export earnings, keep the language at exporter revenue; no buyer link. |
| Saudi or Algerian export modernization | French-funded port, storage/industrial works or training; possible improved export earnings | Finite doctrine/research bonus or negotiated access, if specifically accepted | Native buildings, research and market-sale modifiers are usable. No built-in importer-specific resource pricing/convoy discount was verified. |

To keep choices distinct, separate four reward families: (1) hard access/port rights with a real strategic liability, (2) industrial or mining concessions with partner-controlled assets and capped capacity, (3) finite research/doctrine or actual stockpile transfers, and (4) transparent equal-value cash support. Avoid making every agreement the same industrial productivity idea with a different flag.

# Unsupported or unverified promises to keep out of the design

- Guaranteed commodity quantities, named bilateral buyers, import priority, fixed oil/uranium prices or guaranteed reactor fuel from a treaty: no such native bilateral trade consumer was verified.
- A free-trade, convoy-cost or logistics discount for one named partner: the convoy modifier found in the native market system is global/economic, not verified as bilateral.
- A production license issued solely by `license_production_speed`: that modifier accelerates qualifying licensed lines; it is not the license action.
- Automatically started uranium production or mines without actual survey/deposit, mining-slot, rights, cost, state-control and construction checks.
- Unilateral “military cooperation” prose standing in for access, docking, guarantee, finite research or a real shipment.

No new runtime effects were added or tested in HOI4 as part of this reference.
