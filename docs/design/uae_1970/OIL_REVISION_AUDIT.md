# COLDWAR UAE — low-oil development revision audit

Date: 2026-10-19. **Concept only.** This audit does not authorize or perform installation. Only this design report was written.

Final emitted status: **98 focuses / 37 decisions; bounded oil revision review passed.** Four funded resource projects, the guarded low-oil start and both embedded previews match the final concept data. No unresolved oil-revision source blocker remains; gameplay and engine verification remain separate.

The requested revision replaces an inherited modern-scale oil start with a very small operating base and a deliberately expensive programme of actual resource expansion. The values below are gameplay proposals, not historical barrels/day or historical capital-expenditure estimates.

## Final recommended baseline and development schedule

Use **4 native base oil units** at the January 1970 start: **Abu Dhabi state 180 = 3; Dubai state 179 = 1**. The present state files contain 40 and 7 respectively, so this is a **43-unit / 91.49% reduction** from the inherited total of 47.

| Stage | Native permanent resource grant | Abu Dhabi base after stage | Dubai base after stage | National undisturbed base | Treasury cost, MD billions | Focus duration |
|---|---|---:|---:|---:|---:|---:|
| Starting operating fields | None | 3 | 1 | 4 | — | — |
| I — initial onshore expansion | +8 oil in state 180 | 11 | 1 | 12 | 0.75 | 70 days |
| II — major onshore investment | +10 oil in state 180 | 21 | 1 | 22 | 2.50 | 70 days |
| III — offshore systems | +12 oil in 180; +3 oil in 179 | 33 | 4 | 37 | 5.00 | 105 days |
| IV — late offshore expansion | +7 oil in 180; +3 oil in 179 | 40 | 7 | 47 | 8.00 | 140 days |

Totals: **+43 base oil**, **16.25 billion treasury cost**, 385 focus days across all four physical projects before other political prerequisites. The final undisturbed geographical allocation exactly restores the current inherited 40/7 raw baseline. The cumulative columns illustrate completing I, II, III, IV in that order; they are not compulsory milestone totals for every permitted order.

The emitted layout makes II and III compatible parallel projects after either ownership/services settlement. IV requires III; it does not require II. A player can complete I → III → IV and have a nominal base of 37, then complete II to reach 47. **All four paid projects** are required for the total 47.

“Base 47” means the initial four plus these fixed grants, before external losses and effective extraction modifiers. It is **not a cap on actual engine output**, a promise to sell 47 units, or a periodic restoration target.

The 0.686 billion historical starting GDP remains a calibration reference. The four invoice amounts equal about 109%, 364%, 729% and 1,166% of that reference GDP, respectively. This is a severe multiplayer development programme. It must be described as a proposal and checked against live cash flow before installation.

## Current source baseline and concept gap

- CW `history/states/180-Abu Dhabi.txt:4–8`: oil 40, aluminium 22, steel 5.
- CW `history/states/179-Dubai.txt:5–8`: oil 7, aluminium 19.
- Their January 1970 history blocks change population, ownership, buildings and productivity but currently do **not** reduce oil.
- The previous 97-focus catalogue had oil-contract, gas-power, export-margin and savings policies, but no physical `add_resource` oil grant. The emitted 98-focus revision replaces that gap with four paid physical projects. An oil export-income multiplier alone would not satisfy the requested production development.
- The replacement retains the equity-versus-service-partner choice while allowing both governments to fund the same physical extraction programme. Public ownership and foreign expertise change control, costs and revenue; they do not exclude half of the national drilling programme.
- II and III share an OR prerequisite group containing the two ownership/service alternatives. They are compatible parallel projects, and IV follows III. This preserves the actual proposed structure; no extra II-before-III requirement is introduced by this audit.

## Supported native effects

Installed HOI4 `documentation/effects_documentation.md:2056–2072` documents `add_resource` in STATE or COUNTRY scope as adding/removing resource production. Existing MD proves both signs:

- MD `common/national_focus/gulf.txt:55–87`: non-Saudi `GCC_expand_oil_extraction` spends 9.375 billion and adds 10 oil; Saudi branch spends 18.75 and adds 20.
- CW `common/on_actions/zzzzzz_imp_minis_on_actions.txt:223–226`: `add_resource = { type = oil amount = -2 }`.

A prospective fresh-scenario normalization can therefore remove **37** in Abu Dhabi and **6** in Dubai once, from the confirmed current inherited base. This is a fixed base correction, not subtraction of the country's effective produced/exported total.

Illustrative native resource leaves:

```text
180 = { add_resource = { type = oil amount = 8 } }
179 = { add_resource = { type = oil amount = 3 } }
```

The negative starting correction, its scenario/ownership gate, paid-stage flags and completion wrapper are **proposed COLDWAR_UAE integration**, not already installed effects.

Do not use `resource_produced@oil` to calculate how much to subtract down to four: that country value includes effective output and cannot safely identify the two states' unmodified base. Do not periodically set state oil to 3/1 or 40/7.

## Startup order: reduce resources before existing GDP calibration

The final choice is to apply the one-time low-oil baseline **before** the existing historical GDP profile computes its frozen offset.

Relevant call chain:

1. CW `common/scripted_effects/mdcw_communist_struggle_startup_effects.txt:114–124` refreshes state variables and invokes `IMP_1970_apply_starting_gdp_profile` for countries.
2. CW `common/scripted_effects/IMP_1970_gdp_scripted_effects.txt:1259–1268` gates the profile on the exact 1970 scenario and its one-time flag.
3. UAE target is 0.686 at line 1812.
4. Lines 1825–1834 refresh starting sectors, then set `imp_1970_gdp_base_adjustment = imp_1970_target_gdp - gdp_total` once and mark the profile applied.
5. CW `common/scripted_effects/00_money_system.txt:6153–6162` adds that stored adjustment to later calculated GDP, without refitting the target every tick.

The low-oil helper must therefore run before that country profile calculation and before its resource/GDP caches are finalized. The original historical snapshot remains 0.686 billion; the resource correction still lowers real oil output, fuel availability, exports and oil-derived treasury income. **No oil, treasury, debt or investment principal is granted to compensate.** Future physical expansions increase native resource GDP because the offset remains frozen.

The exact scenario trigger is safe for a January 1970 campaign: CW `common/scripted_triggers/IMP_cold_war_scenario_triggers.txt:1–4` checks `has_start_date` between 1969.12.31 and 1970.1.2. Use it with a persistent one-time baseline flag. Do not rerun the baseline on government change, independence, save load or release from occupation.

Why the rejected after-calibration ordering matters: native resource GDP is based on produced resources, then productivity and existing Imperia curves. Removing 43 units after the old frozen offset could push the displayed economy into its 0.1 billion floor and conceal intermediate growth until much of the old resource level returned. That would create an unintended GDP/debt trap. The before-calibration order avoids this without changing global GDP mechanics.

No UAE-specific startup routine was found that subsequently restores oil to 40/7. Political leader changes and world alignment setup do not add oil. The major later interference is native global depletion, described below.

## Funding and one-time delivery contract

Native money provider:

- CW `common/scripted_effects/00_budget_effects.txt:1482–1494`: `treasury_change` → `modify_treasury_effect` adds the signed treasury amount and calls `update_money_dirty_variable`.
- The helper **does not check affordability** and **does not finance the difference**.
- Native automatic borrowing reacts to negative treasury elsewhere; a guarded extraction project must prevent the treasury from becoming negative through its own transaction.

Required concept conditions for each paid stage:

1. Correct country/scenario identity and the focus's actual prerequisite graph: I precedes the ownership/service choice; II and III follow either choice; IV follows III. Full 47 additionally requires that II has been completed, but II is not a prerequisite for III or IV.
2. Its own one-time stage flag is absent.
3. UAE owns **and controls** every state receiving this stage's grant. Stage III/IV require both 179 and 180; do not charge for a two-state project while applying only one recipient.
4. Exact live treasury check: `check_variable = { var = treasury value = <fee> compare = greater_than_or_equals }`.
5. Resolve the selected equity/service contract if that particular programme promises partner participation.
6. In one guarded completion operation: debit the exact fee once, grant the stated oil once, record the completed-stage flag, refresh the country's economy.
7. If conditions fail, execute neither debit nor resource grant. A pending-funding route must be a named proposed decision/event; a tooltip is not funding.
8. Manual native borrowing, a separately agreed aid/loan transfer or retained oil receipts can provide funds before the player starts/completes the investment. No new bank or hidden automatic loan is required.

The state guard can use native `is_owned_by = UAE` and `is_controlled_by = UAE` in each state scope, or the supported native combined owned/control trigger with a verified country target. Do not allow a foreign state owner to receive oil as a side effect of a UAE investment without a separate agreement.

Physical gains remain national state resources after a government change. Party refresh restores only earned active programme modifiers; it must never repeat the oil grants or charge another invoice. Government turnover does not refund completed wells.

## Refresh: native budget recomputation, no treasury tick

After a successful resource grant, call one country-scoped `ingame_update_setup = yes`:

- CW `common/scripted_effects/00_money_system.txt:220–266` updates state variables/GDP first, resource sales and tax streams, currency multipliers, expenses and display.
- `update_money_dirty_variable` at lines 276–286 refreshes relevant player UI state.
- This recomputes budget streams; it does not itself pay an extra weekly treasury tick.
- `modify_treasury_effect` already marks the money UI dirty, but marking dirty alone is not equivalent to recalculating output/resource income.

Do not call the starting GDP profile again after a paid expansion. Do not reset global resource prices, the global oil model or all countries' historical GDP merely to update a UAE focus reward.

## Cost calibration and conditional payback

The native Gulf benchmark is **9.375 billion for +10 oil**, or 0.9375 billion per added base unit. The proposed programme's stage costs per base unit are 0.09375, 0.25, 0.33333 and 0.8 billion. Stage IV is near that native benchmark; early stages provide a costly but usable entry to development.

A high ratio to GDP does **not** prove a project is economically unaffordable because MD resource export cash and modeled GDP use different calculations.

Source formula:

- CW `common/scripted_effects/00_money_system.txt:49`: resource-sale conversion constant 0.00298.
- Lines 4505–4509: additive general/oil export multipliers.
- Line 4529: weekly oil receipts = `resource_exported@oil × global.oil_price × oil_export_multiplier × 0.00298`.
- Lines 4539+ clamp negative export income to zero.
- Lines 6714–6716 initialize the native resource-market oil price to 7.2; lines 6737–6807 recalculate by market supply/demand with a 1.36–38 clamp.
- Currency and other budget systems subsequently affect realized income/expenses.

At price 7.2 and export multiplier 1, one extra **effective exported unit** produces a formula contribution of **1.115712 billion/year** using 52 weekly ticks. At price 1.36, it produces 0.2107456 billion/year. These are static formula examples, not guaranteed income from one base unit.

For illustration only, suppose 20% of each base grant becomes additional effective exports, with no resource-tech/infra uplift and multiplier 1:

| Stage | Fee | Additional effective exports in illustration | Gross payback at price 7.2 | Gross payback at price 1.36 |
|---|---:|---:|---:|---:|
| I | 0.75 | 1.6 | 0.42 years | 2.22 years |
| II | 2.50 | 2.0 | 1.12 years | 5.93 years |
| III | 5.00 | 3.0 | 1.49 years | 7.91 years |
| IV | 8.00 | 2.0 | 3.59 years | 18.98 years |

These omit financing interest, project lead time, procurement, sanctions, trade law, actual extraction modifiers, workforce changes, oil-price effects, exchange rates, demand changes and later depletion. A 40% export conversion halves these gross payback times. An initial funding bottleneck remains possible even with a good long-run investment.

The right implementation check is a fresh campaign comparison of treasury, annualized net budget, produced/exported oil and expected stage cost under multiple price conditions. Do not replace this with a historical-dollar claim or the GDP percentage alone.

## Effective extraction, technologies and resources are separate

Paid `add_resource` quantities are the fixed development grants. Effective produced oil can exceed the undisturbed 47 total because native infrastructure and extraction technology remain active.

Evidence:

- CW `common/defines/MD_defines.lua:285` sets `INFRASTRUCTURE_RESOURCE_BONUS = 0.05`, overriding the vanilla value.
- CW `common/technologies/industry.txt:3031–3037` gives `excavation1` +0.075 `local_resources_oil_factor`, with further tiers at 3182, 3288, 3418, 3524 and 3662.
- CW `common/technologies/custom_tech.txt:493` also contains an oil extraction modifier.
- State/country modifiers, damage, ownership and native extraction systems influence the engine result.

Do not subtract or cap oil above 47: that would erase the player's legitimate research/infrastructure gains. Report separately:

1. Starting base 4.
2. Paid base additions +43.
3. Undisturbed completed-programme base 47.
4. Current effective production.
5. Current exports and oil receipts.

No barrels/day conversion has been established.

## Global GDP and independence

Resource production contributes to `total_resource_amount` at CW `00_money_system.txt:5071–5081`; the resource GDP component uses that value at 5217–5230; country GDP includes the component around 6045 and applies productivity/Imperia curves before the frozen baseline adjustment.

Reducing oil does not remove the other inherited resources: UAE also has 41 aluminium and 5 steel across these states. All resources feed the resource-sector GDP calculation. Do not call the initial oil reduction a 91.5% reduction in total national GDP.

An accepted independence settlement changes subject relations and leadership, not the geological resource ledger. The baseline/grant flags must survive it. Never restore 40/7 on federation formation, and never rerun the four grants merely because the UAE receives its federal cosmetic tag.

## Later native depletion prevents a guaranteed current total

CW `common/on_actions/zzzzzz_imp_minis_on_actions.txt:168–230` contains a live global resource-reduction routine:

- Every sixth monthly counter cycle, calculate worldwide exported minus imported oil.
- If surplus exceeds thresholds, run 6–50 random reduction attempts.
- Pick a random state with `oil > 6`.
- Remove 2 oil with native `add_resource`.

The block has no demonstrated 1970 or UAE exemption. At the proposed starting 3/1, neither UAE state qualifies; after investment Abu Dhabi can qualify.

Therefore the paid programme **adds 43 once**, but native global depletion, occupation or other resource changes may leave a current base below 47 later. State this in the approval concept. Do not silently restore lost resources or exempt the country through a global edit. Any proposed exemption or field-maintenance policy would be additional explicit design work beyond this bounded revision.

## Existing oil-price systems remain authoritative

There are two distinct native layers:

- The resource-market `global.oil_price` drives native export receipts and adjusts with world import/export balance.
- Imperia/Cold War's internal model price, OPEC level and embargo pressure feed export multipliers and consumer burdens.

CW `common/on_actions/zzzzzz_imp_oil_prices_on_actions.txt:6–52` initializes model price 75, the 1970 display conversion 0.024 and existing weekly/monthly callbacks. The displayed initial $1.80 is **not** the scalar to insert into the resource-sale formula.

CW `common/scripted_effects/mdcw_cold_war_effects.txt:1300+` maintains a calendar-based CPI series; `mdcw_cw_update_oil_level` at 1488–1548 updates producer-price levels monthly from the existing OPEC/market state. `imp_oil_prices_scripted_effects.txt:353–388` assembles displayed oil prices; the existing high/low modifiers and Cold War consequence reader affect revenue multipliers and consumer costs.

There is no justification for adding a separate UAE yearly guaranteed price schedule or promising that each project repays at a fixed 1973/1979 windfall. Keep existing OPEC decisions, the native restraint export penalty, embargoes, market prices and inflation.

Fixed focus fees of 0.75/2.50/5.00/8.00 are MD treasury amounts as designed. They do not automatically become historical real-dollar project quotes merely because the display uses dollars. Any future inflation indexing would need an explicit new pricing rule and frozen visible invoice; it should not be implied.

## Review boundary and required verification

This report confirms supported resource/money APIs and a coherent proposed quantity/cost schedule. It does not establish engine execution, exact starting cash, practical loan capacity, final effective resource numbers or multiplayer transaction atomicity.

Before installation: obtain concept approval; hook the baseline before the existing one-time calibration; inspect the new January 1970 start; verify base/produced/exported distinctions; complete each paid stage once; test inability to pay; occupied-state rejection; both equity/service routes; independence; party changes; save/load; ordinary extraction research; market-price downside; and native depletion. No loaded files were edited by this reviewer.

## Final emitted verification

Final JSON SHA-256: `fa3cd97ca1a914752a7a8f761b4635d671a935820c352d09dd69118255435c2b`.

Independent bounded checks of generator and emitted JSON confirmed:

- All four exact fees and durations match their proposed resource project records.
- Four distinct one-time delivery flags are checked before payment and set after resource delivery.
- Each paid body contains one treasury debit and one country economic refresh; all resource destinations have ownership and control checks.
- Recipient totals are Abu Dhabi 40 and Dubai 7 after all four projects, with total cost 16.25 billion.
- II and III are compatible, have the same OR ownership-policy predecessors and no mutual exclusion. IV requires III only; full 47 requires II as well.
- The starting wrapper checks original UAE identity, native `IMP_is_1970_scenario`, absence of `IMP_1970_gdp_profile_applied`, absence of its own start flag and ownership/control of both states before removing 6/37 units. This matches the metadata's before-calibration integration contract and prevents a normal already-calibrated save from receiving the destructive baseline again.
- All **87 non-oil focus records** match the stored preservation hashes for the audited fields.
- The structural validator reports zero errors, six passing remedy cases, four oil projects, start base 4, final undisturbed base 47 and cost 16.25.
- Embedded `uae-data` in both previews equals the current JSON after removing only embedded image assets.

Preview hashes at this final verification:

| Artifact | SHA-256 |
|---|---|
| `PREVIEW.html` | `662b44ebd0283b606ecb069bc8a3d13221cb45bc0e1bb6ba2b8db38c45a01980` |
| Inline `uae-1970-focus-concept.html` | `20641c75cc2aa44e999287e0311d62de3704faea016192675b1dde964e583b58` |

The parent also reports browser checks across 98 inspectors, 44 views, eight government selections and the four investment-cost details. Those are browser-preview observations, not HOI4 runtime results. This final section supersedes the previous 97-focus catalogue gap description as a statement of current delivery status.

