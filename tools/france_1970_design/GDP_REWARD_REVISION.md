IMPERIA COLD WAR

# France concept: GDP funding, building slots and differentiated rewards

Current revision: **FRA2 concept 1.2**. Design and preview only; no replacement focus tree or fiscal stream is installed. This revision supersedes the fixed prices and reward totals in the earlier 1.0/1.1 design and review notes.

All 152 focus IDs, positions, grouped prerequisites and exclusions are retained. Rewards are revised in 52 focuses and six bilateral offers. Additional technology and operating requirements are visible where the new assets need them.

## Every payment uses the payer's GDP

- One-time focus, decision and acceptance charges are percentages of the payer's **own current `gdp_total`**, calculated when payment actually occurs. There is no fixed-dollar fallback or new Treasury-balance gate.
- Bilateral terms use two separate country scopes. For example, the Airbus setup is **0.5% of France's GDP** and **0.5% of Germany's GDP**; it is not the same invoice charged to both countries.
- Standing programme budgets are annual GDP shares converted into a weekly MD expense: **own current GDP x annual share / 52**. The weekly contribution is recalculated and becomes zero when the programme is suspended.
- The preview displays the exact percentage and weekly division. It does not invent a live campaign GDP or a fixed cash estimate. In the eventual game implementation, native money formatters must additionally show the calculated amount from the live country scope.
- Native script share literals are exact and have at most five fractional digits. Division by integer 52 takes place at runtime rather than embedding a long weekly decimal. The helper rejects silently rounded or zero share literals.

Examples: Rhine exercises cost France 0.08% of its GDP and Germany 0.08% of its GDP once. French weekly funding is `(0.03% of French GDP) / 52`; German weekly funding is `(0.02% of German GDP) / 52`. These intentionally asymmetric shares replace the old fixed amounts. Native spending multipliers remain percentages of their existing weekly bills; they are distinct from a Treasury payment.

`gdp_total` is MD's internal annual GDP base. The 1970 historical-dollar display conversion is not a second cost multiplier. Source providers and comparisons with native France/UK/Iraq focus costs are in `GDP_COST_REFERENCE.md`. All proposed price bands are game balance, not reconstructed historical budgets.

## Every building level includes a slot

All **43 asset rows** grant one extra shared slot per building level in the same state, before construction and inside the same once-only transaction. This includes infrastructure, network infrastructure and provincial naval bases even where native construction does not consume a shared slot. Slots and buildings are separate consecutive rows in the inspector.

Execution must separately recheck ownership, full control, province control where relevant, native building/technology capacity and slot feasibility before charging either signatory. No fixed native building charge is added to the GDP payment. Restoring a party programme or agreement never grants the slot or asset again.

Verified coastal targets include Normandie port province 6449, Marseille 11834 in Provence, and Lorient 6536 in Bretagne. New foreign assets are confined to recipient-approved offers: Hamburg 1080 and Baden-Wurttemberg 42 remain German-side rewards. The German player retains the actual acceptance/refusal decision.

## More specific policy outcomes

| Choice or programme | Revised distinction |
|---|---|
| Chaban or industrial presidency | Technical training and a stronger labour relationship versus a funded factory and concentrated industrial efficiency. |
| Participation or management autonomy | Native labour-union and industrial-conglomerate opinion moves create actual constituency gains and losses, alongside productivity and tax consequences. |
| Private enterprise or public credit | Professional-services offices and office productivity versus industrial research, credit guarantees and a larger public administration. |
| Technical colleges or mass universities | Targeted industrial/electronics research and efficiency growth versus broader academic research and a higher permanent education bill. No unmanaged extra research slot is granted. |
| Regional development or champions | A northern plant and Provence port upgrade versus concentrated production capacity and national productivity. |
| TGV or motorways | SNCF engineering research and a Lyon infrastructure upgrade versus two regional road-infrastructure upgrades with higher energy use. No 1990 rail-terminal technology is handed out in 1970. |
| PTT/CNET networks | Network-infrastructure buildings in Paris and Rhone-Alpes plus electronics research, with the actual `internet_1` technology requirement. |
| Public combines or municipal socialism | Paid civilian/military plants and planning costs versus local infrastructure, labour support and social provision. |
| PSU self-management or sector bargaining | A funded worker-managed industrial pilot versus union support, bargaining outcomes and continuing social spending. |
| Export farms or family-farm services | A paid agricultural district in either route, with different productivity, farmer opinion and social-budget consequences. |
| Deterrent and conventional forces | Narrow research, finite doctrine reductions, training XP and actual upkeep bills replace part of the broad permanent combat stacking. |
| Gaullist land or sea priority | An arms factory with a slot versus a dockyard with a slot; their sector productivity and personnel/equipment costs differ. |
| NATO fleet support and escorts | Actual port upgrades with slots, naval research, supply and safety effects rather than an abstract percentage alone. |
| Airbus or Concorde | Civilian production sites in Toulouse and Hamburg versus a more research-intensive programme with higher annual GDP funding. |
| Symphonie or launcher development | Consented network/ground-system investment and research versus the alternate launch programme. Symphonie's native network grants require both countries' relevant technology. |

Faction opinion uses the existing MD helpers and `temp_opinion`, including their native caps and regime handling. No separate CGT faction or fictional university building is invented. No negative workforce-size modifier, free completed technology, ship or advanced stockpile is added. Historical precedents are recorded in `REWARD_PRECEDENTS.md`.

## Consent, persistence and checks

All 19 offers specify recipient consent, acceptance-time rechecks, separate GDP payments, asset feasibility and once-only paired delivery. Peace, native embargo, all four mirrored sanction classes, actual parent agreements and NATO membership where relevant continue to govern activation. Signed agreements survive government changes. Party modifiers still require the exact native ruling party, and all branches remain inspectable.

`GDP_REWARD_REVIEW.md` verifies the fiscal schema and native reward providers. `GDP_ASSET_REVIEW.md` checks asset capacities and representative rendered offers. `GDP_REWARD_CHECKS.json` records independent design-contract checks and graph preservation. `BROWSER_QA.json` checks 152 inspectors, all 19 bilateral term sets, nine governments and 42 section/width views.

These are source and external-preview checks. Native executable transactions, money-stream integration, hovers, save/reload and multiplayer timing remain part of the implementation after approval.
