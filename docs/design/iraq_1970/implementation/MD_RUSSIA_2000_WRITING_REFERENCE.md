# Main MD Russia 2000: writing and reward presentation reference

Inspected 18 October 2026. This reference concerns the installed **main Millennium Dawn Russia tree**, `common/national_focus/05_russia.txt`, and its English localisation. It is not the project's custom Soviet Union 1970 tree. Recheck line numbers against the installed version before using them in later work.

Reference root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/`.

## Failure learned from the Iraq screenshot

The Iraq focus **Consumer Industry** described itself as “Pay for a Nineveh civilian factory.” Its effect panel then explained GDP quotation, blocked delivery and a project queue. This mixed an authoring instruction and implementation details into the country's political narrative. Valid calculations and a native building tooltip did not make that presentation conform to the requested MD reference.

Treat main MD Russia 2000 as the required writing and reward-presentation reference for national focus work. Descriptions explain the country's situation, the proposed policy and its purpose. Native effect tooltips show the actual numbers and named outcomes. Preserve approved mechanics and balance while correcting presentation; a writing request does not authorize removing financing or changing rewards.

## Verified source examples

| Concern | Main MD source and line | Actual pattern |
|---|---|---|
| Purposeful financial narrative | `localisation/english/MD_focus_SOV_l_english.yml:33`, `SOV_stabilisation_fund_desc` | Explains a reserve against crisis, continuity of public services and domestic/international position; it does not tell the player to pay a bill. |
| Political narrative | Same file `:43`, `SOV_putinism_desc` | Explains the governing institutions and their political character. |
| Industrial narrative | Same file `:3745`, `SOV_economic_slavneft_desc` | Names Rosneft, Gazprom and the intended acquisition of Slavneft assets. |
| Reform narrative | Same file `:3927`, `SOV_economic_sber_reorg_desc` | Describes modernising Sberbank's operations and services. |
| Native cost and decision | `common/national_focus/05_russia.txt:297–304`, `SOV_stabilisation_fund` | `unlock_decision_tooltip`, `add_ideas`, a negative `treasury_change`, then `modify_treasury_effect`. |
| Native regional building and cost | Same file `:34232–34251`, `SOV_economic_slavneft` | State-scoped `add_building_construction`, native resource effects, company effects, and a numeric treasury deduction. |
| Native programme deltas | Same file `:410–413`, `SOV_putinism` | `modifies_dynamic_modifier_tt` names the programme; `add_to_variable` supplies exact changes with native `<modifier>_tt` formatters. |
| Decision plus programme | Same file `:34527–34533`, `SOV_economic_sber_reorg` | `unlock_decision_tooltip` followed by named programme changes. |
| Native spirit replacement | Same file `:628–635`, `SOV_oligarchic_republic` | A current-idea check and `swap_ideas` name the removed and replacement ideas. |
| Treasury provider | `common/scripted_effects/00_budget_effects.txt:1482–1493` | `modify_treasury_effect` consumes `treasury_change`, supplies its tooltip, changes treasury and marks the economy dirty; it respects `MD_skip_treasury_cost`. |
| Treasury text | `localisation/english/MD_tooltips_l_english.yml:90` | `modify_treasury_effect_tt` displays country flag/adjective, Treasury, and signed dollar amount in billions. |
| Programme heading | `localisation/english/MD_dm_modifiers_l_english.yml:3` | `modifies_dynamic_modifier_tt` supplies the native heading naming `$MODIFIER$`. |

These are examples of presentation grammar, not permission to copy Russian state IDs, company mechanisms, amounts or political history into Iraq. Some native descriptions are very short; sentence count alone is not a quality criterion.

### Supplementary native API evidence: non-executing numeric previews

Russia's ordinary rewards execute their variable setup and payment directly. Iraq retains hidden, guarded transactions, so its matching preview must show the same value without charging it. The installed MD already calculates variable amounts inside `effect_tooltip`:

- `common/national_focus/05_united_kingdom.txt:20914–20917`: sets `treasury_change = gdp_total`, multiplies it by `-0.05`, and invokes `modify_treasury_effect` inside `effect_tooltip`.
- `common/decisions/05_afghanistan.txt:861–865` and `:953–957`: the same pattern for GDP-based investment returns of `0.06` and `0.08`.
- `common/decisions/Iraq.txt:2529–2531`: a fixed `treasury_change = 75.00` and the treasury provider inside `effect_tooltip`.

Use this native calculation pattern for the Iraqi preview: if a quote exists, display its negative stored amount; otherwise calculate the negative current GDP share. Keep all preview setup and the provider inside the non-executing block, and retain the actual payment solely in the guarded transaction. The treasury provider itself respects `MD_skip_treasury_cost`. Native source precedent supports this construction; observing the rendered dollar value still requires an in-game hover check.

All 75 distinct decision IDs referenced by the approved Iraqi focus catalogue were found as exact definitions in the loaded decision files during this review, so they are suitable targets for native `unlock_decision_tooltip`. This reference check is separate from validating each decision's availability or effects.

## Reusable authoring rules

1. **Narrative descriptions:** name the relevant institution, sector, locality or constituency. Explain the problem and the chosen response in natural English, usually one to three sentences. Include a meaningful political or economic tension when relevant. Avoid generic promises of greatness, repeated title paraphrases, player instructions and lists of modifiers.
2. **No implementation prose in focus flavour:** reject phrases such as “Pay for a factory”, “quoted once”, “implemented prerequisite rewards”, “package earned”, “frozen invoice”, and debugging explanations of delivery or variable bookkeeping. Explain a delayed project's actionable status in its decision UI when necessary, without flooding every focus with system documentation.
3. **Numeric economic effects:** show the actual signed treasury/debt amount using the native MD formatter/provider. A GDP-funded cost must display the correct current estimate or already fixed quote. Do not conceal a cost in order to shorten the text, and do not execute a real payment merely to build a preview.
4. **Programme changes:** retain the native named modifier heading and one native signed numeric row per modifier. Do not duplicate those values as a prose reward paragraph. Preserve special caps and eligibility where they change what the player receives; place common rules in the programme explanation rather than repeating implementation commentary everywhere.
5. **Decisions and spirits:** use `unlock_decision_tooltip`, `add_ideas`, `remove_ideas` or `swap_ideas` where applicable. Hidden transaction helpers still require equivalent native previews. Do not replace named outcomes with “unlocks content” or a catalogue's internal design note.
6. **Buildings and instant rewards:** show native state-scoped building, resource, experience, research, claim and war-goal effects. Displaying a tooltip is not proof that a hidden transaction executes; verify the actual provider separately.
7. **Agreement options:** show concrete numeric native costs and rewards on the options. Keep the event's description to the political proposal and stakes.
8. **Scope and truthfulness:** preserve one-time charges, affordability checks, receipts, government-bound activation and save recovery when correcting text. Do not promise an immediate grant if the retained mechanics can defer it; provide a short, truthful pending-state notice in the appropriate UI.
9. **Review both surfaces:** compare a political, industrial, military and diplomatic focus's description **and** effects against the current main MD Russia source. Inspect at least one representative rendered in-game tooltip when available. Static tests, preview HTML and source comparison are distinct from observing the game UI.

## Concrete Iraq examples

The following are original illustrative wording, not new balance proposals:

- **Consumer Industry:** “Baghdad's development plans must reach the northern provinces. Expanding consumer production around Mosul will supply domestic markets and provide industrial employment beyond the capital.” The effect panel should show the native Nineveh civilian-industry grant and its exact treasury cost.
- **Chain of Command:** “Party officials and competing security services have blurred responsibility within the armed forces. A single chain of command will give professional officers clearer authority, at the cost of some of the leadership's direct control.” The effects should show the actual patronage spirit change and the separate programme organisation delta, preserving the existing component arithmetic.

These examples may be adopted only if they describe the corresponding implemented policy accurately. They are not historical claims requiring the game to invent a new factory, military reform or cost.

## Presentation-only corrections identified in the Iraq generator

At inspection, `tools/iraq_1970/compile.py:123` generated the long GDP/invoice/queue text shown in the screenshot. Replace that presentation with an accurate native numeric treasury preview while preserving the existing `invoice()`/`pay_var()` transaction and deferred delivery rules.

At `:132`, custom “Unlocks decision” prose duplicated the native `unlock_decision_tooltip` capability. Prefer the native form for real decision IDs.

At `:134`, catalogue `replaces` strings were exposed directly even though `presentation.situation_preview()` already supplies actual conditional idea swaps/removals. Keep design and arithmetic notes out of the player-facing reward list; preserve any genuine extra effect that is not otherwise represented.

At `:137`, the raw approved catalogue description was copied verbatim. Approved effect values do not make an authoring note suitable flavour text. Maintain a reviewed description override layer, or improve the canonical description only when that source is permitted to change; do not alter the approved geometry or reward payload to fix writing.

`presentation.reward_preview()` already follows the Russia programme-heading and native modifier formatter pattern. Retain it while removing surrounding technical prose. A numeric preview must remain non-executing and must agree with the actual hidden grant.

## Before considering a writing fix complete

- Verify that every focus retains its approved numeric reward, financing, prerequisites, exclusions and coordinates.
- Search emitted English localisation for authoring instructions, obsolete invoice essays, raw design notes, duplicate reward prose and unresolved identifiers.
- Verify displayed treasury units/sign/quoted-vs-estimated amount, named programme changes, decision unlocks and idea swaps.
- Ensure the generator regenerates the correction rather than restoring the old wording.
- State separately what was source-reviewed, statically validated and actually inspected in HOI4.
