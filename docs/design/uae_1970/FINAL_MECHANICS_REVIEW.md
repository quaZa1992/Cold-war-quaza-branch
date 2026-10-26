# COLDWAR UAE — independent final mechanics review

Reviewed 2026-10-19: `build_concept.py` and emitted `COLDWAR_UAE_1970_CONCEPT.json` (96 focuses, 32 decisions, 11 sections, 22 mutually exclusive pairs). This review examines the concept source and preview data, not loaded HOI4 content.

## Current review status

The catalogue contains **97 focuses and 37 decisions**. The six initial findings and the final reform-family issue have been corrected in the generator and final artifacts. No unresolved mechanics blocker remains in the reviewed concept source. These are design records and verified native leaf APIs, not a gameplay implementation guarantee. Final artifact synchronization is verified below.

## Result at first review

The numerical catalogue is broadly grounded in actual MD APIs. The current plan uses sensible subject matter and substantial outcomes, distinguishes queued construction from completed factories, preserves recipient consent, and separates ordinary political programmes from permanent national capital. It is suitable for an approval preview **after the consistency fixes below**.

The remaining source limitations are explicit: all COLDWAR UAE helpers, flags, stage replacements and decision bodies are new design work. None is installed or engine tested.

## Required corrections

### 1. Country spirit uses a state modifier

`COLDWAR_UAE_expatriate_workforce` places `recruitable_population_factor = -0.20` in a country spirit. Installed HOI4 `documentation/modifiers_documentation.md:4552–4555` identifies this key as a **state** modifier. MD occurrences in Balance of Power are not proof of valid country-idea scope.

Use the supported native country `conscription_factor = -0.20` for a 20% recruitable-population multiplier, or `conscription` for a flat population-share deduction with an intentionally recalibrated value. Installed documentation at 2272–2281 distinguishes these country keys. Native MD `common/ideas/arab_spirits.txt:254–264` uses `conscription` in the expatriate country idea.

This is a real scope issue; it should be fixed before declaring the whole proposed palette verified.

### 2. Structural remedies are missing from structured concept data

At first review, **all 96 nodes have `starting_changes = []`**. Many reward summaries promise explicit starting-spirit replacements, yet their technical effect outlines and machine-readable plan contain only newly earned positive contributions.

Affected areas include Treaty Dependence, Fragmented Authority, Unequal Development, Scarce Specialists, Water and Power Constraints and Narrow Revenue Base. Examples: `federal_ministries`, `dual_veto`, `technical_institutes`, `water_network`, `commercial_courts`, `beyond_oil`, `oil_shock_plan`, `rak_accession`, `union_command`.

The generator already has a `changes` parameter; populate it or add structured stage/floor records. Record target spirit/component, target/floor, prerequisite stage and permanence. Do not implement a promise by granting a permanent positive counterbonus while leaving the original starting malus unaltered.

Particularly ensure that `technical_cadres` plus national training does not double-remove a −10% research penalty, and that completing a defence remedy before a constitutional remedy cannot later reintroduce an older army-organization penalty.

### 3. Conditional contract benefits contradict node conditions

`state_participation` advertises acceptance-only +15% oil export revenue. Global programme rules repeat this requirement. Its own `active_condition` is `always = yes`, its modifiers contain unconditional +0.15, and its effect outline immediately earns that value.

Separate setup expense and administrative burden from the conditional contract contribution. Give the latter an explicit acceptance/buyout condition in the same node and inspector. A parent rule at the bottom of the catalogue is not a substitute for truthful local conditions.

Likewise, `federal_ministries` promises an accepted rulers' compact but has no local availability condition or requirement contract. Define whether the focus initiates an offer and waits, or requires a previously accepted compact; apply reform/benefits only at the stated stage.

### 4. Formation lacks a designed consent provider

`sovereign_union` requires `COLDWAR_UAE_founders_consented`, but no existing decision summary names an action that sets it. `charter` refers to a settlement and an emirate ledger, without defining the acceptance operation. The monarchy's later mediation decision unlocks only after federal formation, so it cannot supply this prerequisite without a circular route.

Add a named charter settlement/ledger event or decision contract, available before formation, that resolves the participating rulers' consent and selected constitutional bargain. Keep this independent of the later 1976–79 mediation. Explicitly connect British withdrawal acceptance, founder consent and post-formation leadership.

No loaded implementation is required at concept phase, but the source of each promised gate needs an actual design provider.

### 5. Empty diplomatic focuses lack linked offer decisions

`security_contracts` (Training Agreements) and `technical_exchange` (Across the Blocs) have empty technical bodies and advertise accepted contract rewards. Programme rules say these focuses unlock decisions rather than grant immediately. None of the 32 decision records currently unlocks from either focus.

Add their concrete recipient-controlled offer records or explicitly link them to an appropriate existing record, including payer, recipient, frozen price, cooldown, acceptance/refusal and exact rewards. The domestic `decision_training` unlocked by `sustainable_force` is not a replacement for foreign training consent.

### 6. Islah association flag needs explicit independent access

The Islah group requires both the ruling Muslim Brotherhood subparty and `COLDWAR_UAE_islah_organised`. `decision_association_law` has `unlock = null`, but its summary does not explicitly set that flag or state that its availability is independent of the group flag it must establish.

Record its pre-government visibility/availability and flag grant. Historical 1974 context and an agreed earlier legalization are sensible; a decision hidden by the condition it must create is not.

## Passed source checks and appropriate choices

- Country/tag and map: UAE, state 179 Dubai, state 180 Abu Dhabi. No guessed foreign state transfers.
- Political root gates use actual MD subparty triggers, not outlook-only tests.
- Arab civilian vs officer policy and communist vs non-aligned social alternatives have explicit additional exact-party gates.
- Government programme variables are intended to persist and reactivate; factories, productivity-point grants, cash and XP are intended to run once.
- Money labels correctly use MD billions; interest discounts use annual percentage points rather than percentages.
- Flat productivity grants are points; `productivity_growth_modifier` is labelled growth input rather than +X% growth.
- `offices_productivity` has real office tax/GDP consumers; `total_workforce_modifier` is not described as granting manpower.
- Registered Imperia investment-capacity, sanctions and oil-price systems are used. No second OPEC model or duplicate restraint income debit is proposed.
- Construction fees are explicitly preparation costs. Factories, offices and fossil plants are **queued** and still consume normal native construction, staffing and energy.
- The inherited level-10 Abu Dhabi port is acknowledged; any further port construction is conditioned on verified coastal capacity.
- There are no modern aircraft, free divisions or automatic bilateral annexations in the numerical leaf bodies.
- Starting spirits contain real constraints and planned treatment instead of only beneficial national identity spirits.
- Save/load and party change must resynchronize active programmes without replaying one-time leaves.
- The graph's joins use one OR prerequisite group for mutually exclusive alternatives in the inspected diamonds.
- Positive stability caps are stated as programme contribution caps; negatives remain visible.

## Balance observations, not blocking defects

The 0.01–0.04 billion setup fees equal roughly 1.46–5.83% of the authored initial 0.686bn GDP. Requiring ordinary construction after this fee prevents a small payment from buying an instantly completed native factory. Final affordability still needs a fresh scenario budget because wages, electricity, subject status and world initialization change actual cash flow.

The free-zone +1 inward investment slot is substantial (native base is three at this GDP band) and has an explicit bureaucracy burden. Industrial and service paths improve different sectors rather than presenting cosmetic alternatives.

Cumulative modifier accounting is needed at implementation: several shared construction, office, workforce and administrative contributions accumulate in addition to the active political programme. The concept explicitly proposes uncapped economic/military accumulation; do not silently add a new cap after approval. Present route totals during balance review before changing them.

Recurring productivity courses require their stated cooldowns and one grant per paid course. Track the paid course identity and pending completion so changing government or reloading cannot trigger a second award.

## Narrative and presentation comparison

Representative descriptions such as The Development Fund, Retain the Partners, Technical Institutes and A Sustainable Force explain local institutions and policy tensions in readable English. Their one- or two-sentence style is suitable for a concept and is more country-specific than generic reward prose. Reward bundles resemble MD's named programmes with visible cost, a real system benefit and a counterweight.

The concept contains implementation caveats in reward lists (for example references to an impossible port, no free modern aircraft, no duplicate money and no unilateral effects). These are useful audit notes for approval, but should be kept in design/technical details when final player-facing localization is authored. Native MD completion text should show the actual named numeric result and conditions; it should not be a developer checklist.

No source audit can establish exact in-game hover rendering, dynamic-modifier enable behavior after a save, construction queue behavior at capacity, or multiplayer event scope. Those remain implementation/runtime checks.

## Recheck status

### Regenerated catalogue closure review

The 97-focus / 37-decision JSON was re-read after regeneration. The following first-review issues are closed at the concept-data level:

| Finding | Closure evidence |
|---|---|
| Wrong scope for expatriate recruiting key | Spirit now uses supported country `conscription_factor = -0.20`. |
| Missing structural remedies | Sixteen focus nodes now contain explicit `starting_changes` / `spirit_changes`, including owner, component and evaluation contract. |
| Unconditional oil contract bonus | `state_participation.active_condition` now requires `COLDWAR_UAE_oil_participation_accepted`, and its own reward list labels the contract condition. |
| Unprovided founders' consent | Founders’ Settlement unlocks from the draft charter and sets consent plus a mutually exclusive chosen charter term; matching institutional focuses check the chosen term. |
| Missing foreign contract decisions | Training and technical exchange offer records now unlock from their respective focuses, with numerical terms and recipient acceptance. |
| Islah flag self-lock | Association recognition explicitly has independent availability and sets `COLDWAR_UAE_islah_organised` without installing that government. |
| Dirham integration claim | New currency focus calls its domestic identity/board bridge proposed and does not grant reserve-issuer status or a fictional exchange-rate bonus. |
| Completion-order-dependent reforms | Contract now recomputes from immutable original components and once-earned credits, with strongest relief inside a stage family and zero clamping. Army integration is explicitly one family. |

Final family adjustment is corrected in the generator: `seven_emirates` administrative relief and `federal_ministries` target +5% now use `administration_integration`, so the strongest stage gives the stated +5% remaining bureaucracy burden. The six-case remedy validator includes this combination, both construction orders, both army-integration orders and completed civilian-revenue reforms; it reports no errors.

Final bounded artifact verification after the 14:14 regeneration: both administrative remedies contain `administration_integration`; all six remedy cases pass. The embedded `uae-data` in both `PREVIEW.html` and the inline visualization equals the final concept JSON after removing only the embedded image-assets field.

| Artifact | SHA-256 at final verification |
|---|---|
| `COLDWAR_UAE_1970_CONCEPT.json` | `da4df00e465b2d88f048869948fa2ac1eaeb62aed66b92a6715a73faece3da52` |
| `PREVIEW.html` | `831f64fb7e1ae6811d101764bb94cf37f46f11219b97bc23738874d80f1bfe23` |
| Inline `uae-1970-focus-concept.html` | `4e69161025a0de037c97f4a14a00fcfe1b96a794e65c65148dbb04cb9d16d33b` |

### Optional savings-policy calibration

The savings path's interest discount has no cash-flow effect when debt is zero, while a pure cash reserve ledger earns no return beyond treasury. A verified native improvement is `return_on_investment_modifier`: CW `common/modifier_definitions/money_modifier_definitions.txt:198` registers the country key; `common/ideas/generic_ideas.txt:297` uses +0.01; `common/scripted_effects/00_money_system.txt:4484–4487` adds it to the base annual ROI of 0.04, clamps to the configured ceiling, then computes weekly income on actual native investment principal (plus 25% of held bonds).

Thus +0.005 or +0.01 means +0.5 or +1 **annual percentage point**, not a relative percentage increase and not free cash. It would make an investment institution useful while retaining its construction penalty. It must affect a separately funded native portfolio; the uninvested cash ledger still earns zero. The existing `modify_international_investment_effect` at `00_budget_effects.txt:1527–1535` changes native principal, but cash transfers and withdrawal accounting must remain paired. This is an optional balance improvement, not an unresolved source defect or permission to duplicate principal.

All decision focus-unlock references resolve in the re-read JSON. The structural validator reports no errors. No loaded mod files were changed by this reviewer.



## Final delivery synchronization by root

The sole final balance addition after the independent snapshot is `return_on_investment_modifier = 0.005` on Save the Windfall, using the provider/consumer traced in the mechanics review. Its inspector shows +0.5 annual percentage points on funded native investments; the uninvested cash reserve ledger earns zero. `FINAL_SAVINGS_VALIDATION.json` records the targeted mouse-click check. Geometry, titles, icons and dependencies are unchanged. Both preview models match the final JSON exactly (`FINAL_BUNDLE_VALIDATION.json`); six remedy cases and the existing 97-inspector/44-view browser checks pass. No HOI4 engine test has been performed.

Final delivery hashes:

- `COLDWAR_UAE_1970_CONCEPT.json`: `9bb4c67945aeb4aa1dedb7b962992dac4ee022797e8ce8b4ca8cc2e46ffdfb13`
- `PREVIEW.html`: `c42059930d47fc6c422654e08f0a5e939e25007159321be79c5d1619cf6ad98b`
- `uae-1970-focus-concept.html`: `8efd8589ab4fa9ec5103ba18d580191ab4f3392dd8db0117dddc6fe57e0f9628`
