IMPERIA COLD WAR — Economic organisation balance concept, 23 October 2026

Status: design record. The core compact bar, seven policy tiers and repeatable institutional reforms have been implemented; see [IMPLEMENTATION.md](IMPLEMENTATION.md) for the active values, integration and validation. The additional funded decision families below remain proposals. Globalisation and market sensitivity are consequences of the economic policy tiers themselves. The percentages originated as balancing samples, not historical estimates.

The compact native-style policy bar remains the primary control. Repeatable reform decisions move its country-specific value. The country's original native balance of power remains independent.

## Economic policy contributions

The policy affects allocation, investment coordination and exposure. At the user's explicit clarification, the full original compact-concept effect package has been restored alongside the later additions. This includes workforce participation on the command and central-planning tiers, direct relative productivity growth, administration costs and the highest market tier's annual investment-return contribution. Existing Globalisation readers still operate additively. The earlier recommendation to omit direct growth and ROI contributions is superseded by that instruction. Scientific research and welfare policy remain separate institutions.

Globalisation equilibrium is a contribution to the existing sum of equilibrium modifiers, before the existing 0–100 clamp. It does not replace trade policy or assign the current globalisation level instantly. A planned economy can remain internationally integrated when its other policies support that integration. Globalisation continues to adjust weekly.

Market exposure is an additive contribution to the existing mdcw_cw_market_exposure modifier. It scales favourable world-market conditions as well as unfavourable conditions. It is not the probability of a recession occurring.

| Tier | Globalisation equilibrium contribution | World market exposure contribution | Office productivity contribution |
| --- | ---: | ---: | ---: |
| Command Economy | -15 points | -25% | -10% |
| Central Planning | -10 points | -15% | -7% |
| State-Led Development | -5 points | -5% | -3% |
| Mixed Economy | 0 | 0 | 0 |
| Regulated Market Economy | +5 points | +5% | +3% |
| Liberal Market Economy | +10 points | +15% | +7% |
| Laissez-Faire Economy | +15 points | +25% | +10% |

Example with current globalisation held at 62 and no other exposure modifiers: the existing base exposure is 1.24. Command Economy's -25% contribution produces 0.93 transmission; Laissez-Faire Economy's +25% produces 1.55. The existing 0–2.5 final clamp still applies. Other national exposure contributions must be included additively in the same modifier sum.

## Construction and production roles

The following figures illustrate the outer tiers; intermediate tiers should scale down rather than copy the complete extreme package.

| Mechanic | Strong planning | Strong market coordination |
| --- | --- | --- |
| Civilian factory construction | Approximately +10% | Baseline; private capital access provides a different advantage |
| Infrastructure construction | Approximately +15% | Baseline; targeted public programmes remain available |
| Office construction | Approximately -15% | Approximately +15% |
| Office productivity | Approximately -10% | Approximately +10% |
| Production efficiency cap | Approximately +5 to +8 percentage points | Baseline |
| Production efficiency growth | Approximately -15 to -20% | Baseline or a small adaptation bonus, subject to whole-system testing |
| Incoming investment cost and duration | Approximately +10 to +15% | Approximately -10 to -15% |
| Paid domestic investment projects | Lower coordination cost / targeted programme access | Approximately +10 to +15% money cost |

These are gameplay abstractions, not universal claims that a given economic institution always builds more quickly. In particular, the advantage of coordination is best represented in explicitly funded priority programmes, and the market advantage should depend on capital access and functioning institutions. No general construction bonus should make every building type equally strong on the same side.

Office productivity is separate from office construction speed. The existing offices_productivity modifier is read by common/scripted_effects/00_money_system.txt in office_tax and gdp_from_offices. The office tax reader multiplies by 1 + offices_productivity; the GDP reader uses a base factor plus a productivity coefficient. A +10% office productivity contribution therefore must not be advertised as +10% national GDP. Both readers also account for office workforce fulfilment. This is the appropriate existing mechanic for the proposed sector productivity difference, rather than applying office_park_income_tax_modifier alone.

The user requested a modest office productivity disadvantage for planning and the reverse advantage for market coordination. The seven-step -10/-7/-3/0/+3/+7/+10 schedule is a provisional response to that design request. Its rationale is sectoral priority and enterprise incentives, within the historical limits recorded below; it is not a universal historical efficiency estimate. It must be calibrated together with office construction, globalisation and existing world-market office income effects before implementation.

Existing local content uses the relevant production-efficiency and building-construction modifier families, and the money/investment readers expose the investment modifiers. Exact building keys, reader direction, stacking, preview behaviour and meaningful marginal effects must be verified before runtime integration. Source presence alone does not prove that proposed signs and values behave correctly in-game.

## Additional decision families

1. Industrial priorities: choose one funded infrastructure, energy or heavy-industry programme at a time. Gain concentrated construction advantages, with weekly treasury payments and delayed capacity rather than an immediate permanent free national bonus. Development plans should also be accessible to suitable non-communist developmental governments.
2. Enterprise modernisation: fund machinery, worker training and production-line changes. Faster adaptation and improved productivity compete with the planning route's cheap standardised mass production. Avoid counting the same productivity gain in both globalisation and the programme without checking total impact.
3. Labour participation: the restored original core spirits contribute +5% Available Workforce for Command Economy and +3% for Central Planning through MD's existing participation modifier. Additional funded childcare, vocational training and rural-to-industrial recruitment decisions remain future options. These effects do not create population or universally reduce workers per building.
4. Industrial zones: paid development in selected eligible states can provide shared building slots and construction. Every granted building level receives a shared slot first in the same state and in the same one-time transaction. Changing policy direction must not allow repeated slot collection.
5. Strategic reserves and resource development: improve resilience through paid stockpiles or development projects where supported by existing resource systems. Deposits, energy, labour and maintenance constrain the benefit. Uranium surveys remain separate from mine construction and raw production.
6. Reform adjustment: rapid changes can temporarily interrupt production or employment. The magnitude should depend on the scale and speed of reform. Long-lived structural penalties should not substitute for distinct economic choices.

Aim for roughly five to seven readable core modifier lines per tier. Put specialised options into a small number of decision families rather than adding every possible modifier to each tier. Use English institutional names and native signed numeric effect previews in any later implementation.

## Historical precedents and limits

- IMF, Reforming the Soviet Economy (1991): extensive accumulation of labour, capital and raw materials supported earlier growth, but participation limits and declining efficiency constrained the model by the 1970s. This supports mobilisation and standardisation benefits, with diminishing returns and adaptation costs. https://www.elibrary.imf.org/abstract/journals/022/0028/002/article-A006-en.xml
- World Bank, Korean industrial-sector assessment: directed credit and human/physical infrastructure supported industrialisation, while heavy-industry promotion also produced debt, excess capacity and credit crowding-out for smaller firms. This supports funded sector priorities and genuine financial opportunity costs; it also demonstrates that planning instruments are not exclusive to communist governments. https://documents1.worldbank.org/curated/en/580261468045001809/pdf/multi-page.pdf
- World Bank, Credit Policies and the Industrialization of Korea: the heavy and chemical industry drive combined targeted credit, protection and government-directed decisions. It created substantial industrial capabilities alongside inefficient scale choices, capital intensity and delayed liberalisation. https://documents.worldbank.org/curated/en/756811468272061144/pdf/multi-page.pdf
- IMF, Why Is China Growing So Fast?: stronger enterprise incentives and gradual opening accompanied productivity gains. This supports market access and adaptation as long-term strengths without equating every reform with complete privatisation. https://www.imf.org/external/pubs/ft/issues8/index.htm
- IMF, Economic Reform in Hungary Since 1968: market-based decentralisation operated within socialist ownership and political institutions. The bar should represent actual policy, not an automatic outlook or party-popularity assignment. https://www.elibrary.imf.org/display/book/9781557752161/Ch02.xml

These sources establish precedents and trade-offs, not the proposed modifier percentages. Third-party materials remain with their original authors and institutions; no images or article text are copied into this proposal. Separate redistribution permission for source material is not established by this record.
