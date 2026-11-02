IMPERIA COLD WAR
# Universal SSR implementation result

The approved tree is installed for all fourteen 1970 Union republics. Every republic has all nine mutually exclusive specialisations; the naval programme requires an owned, controlled core coast. Country examples in focus descriptions are historical precedents, not selection restrictions. All new game localisation is English.

The shared SSR requirement is actual Union-republic status, without a communist-party or Soviet-outlook requirement. Independence automatically selects the earned national legacy on the next daily check, removes the full Union counterpart and activates country-specific transition liabilities. Accepted re-entry restores the full specialisation. A second exit preserves earlier preparation and repairs. Independent political programmes remain visible and their benefits follow the exact native MD ruling-party slot.

Full specialisation benefits retain 20% of their beneficial components after independence, 75% of their adverse components and 50% of the weekly GDP allocation. Durable construction, research and experience are not granted again by status reconciliation. Weapon programmes retain their production bonuses and use the approved native equipment-specific production-cost reductions.

| Agricultural route | District labour requirement | Subsistence labour requirement | Independent district / subsistence legacy |
| --- | ---: | ---: | ---: |
| Mechanised | -25% | -20% | -5% / -4% |
| Diversified | -15% | -15% | -3% / -3% |

These are sector labour requirements. Total workforce is unchanged; native employment demand, floors and agricultural GDP calculations still apply.

Seven recipient-approved diplomatic programmes use paired standing spirits, current-GDP setup fees and dedicated weekly MD expenses. Daily validity checks suspend and restore both countries under bilateral restrictions without repeating fees. Last-agreement termination removes the recipient spirit before retiring its activity flag. The three sovereign market courses have once-only 730-day windows and a separate persistent restructuring burden. Six finite sector settlements offer sales, worker buyouts, public retooling or one-factory liquidation.

## Verification

- 1,242 installed focus definitions, fourteen country views of 262 to 312 focuses, 69 political programmes and 42 integration outputs.
- 51 Python source/model regression tests passed. Static graph, reference, condition, encoding and integration checks report no errors or warnings.
- Repeated compilation produced identical outputs. The final native run used a private snapshot; all source and snapshot hashes remained unchanged.
- 36 native checks passed across four simulated days. They cover full/legacy replacement, real independence and re-entry, exact-party changes, actual agricultural modifiers, legacy repairs, real recipient acceptance, daily financial-sanction suspension/restoration, economic-sanction suspension/restoration, zero suspended expenses, last-agreement termination, course timers and exactly one civilian factory removed once.
- Two native embargo-only checks were skipped because By Blood Alone was not active in the isolated process. Their raw verdicts and capability reason remain in ENGINE_REPORT.json. Manual tooltip/layout inspection, save/reload and live multiplayer were not tested.

The detailed evidence is in IMPLEMENTATION_RESULT.json and its linked reports. The approved source snapshot remains unchanged; the subsequent agricultural amendment has its own recorded hash. Attempt 4 was rejected because an older diplomacy output replaced three files during that run. Its complete diagnostic artefact remains available under the ignored private runtime directory; it is not counted as successful validation.
