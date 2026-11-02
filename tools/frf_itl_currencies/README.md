# IMPERIA COLD WAR — French Franc, Italian Lira and reserve-currency review

This revision adds the two requested national currencies within the existing monetary-law category. The user explicitly chose to add them first and discuss the broader redesign afterwards. National currency, reserve allocation and debt denomination have not been split into separate systems.

## Implemented scope

| Item | Behaviour |
|---|---|
| French Franc | A national currency option for France. |
| Italian Lira | A national currency option for Italy. |
| Starting campaigns | France and Italy receive their respective law in the 1970 and 1985 country-history snapshots. |
| Existing saves | No startup or periodic migration overwrites an existing monetary choice. The new option can be selected manually. |
| Euro | Actual eurozone participation blocks adoption of the national law; `joining_the_euro` converts either law to the euro. Reaching 1999 alone does not force an alternative-history campaign to abandon its currency. |
| Base price | 50 political power, following the generic domestic-reserve law. National law-cost modifiers still apply. |
| Benefits and costs | Both inherit the generic domestic option's +0.05 political power/day and +5% receiving-investment project cost. These are existing gameplay abstractions, not historical economic measurements. |
| Reserve status | Neither addition creates an international issuer flag, adopter network, seigniorage income or fabricated reserve-return bonus. |
| Presentation | English institutional descriptions and two dedicated transparent 72×64 BGRA icons. |

All previous currency laws and their modifiers remain unchanged. The `uses_own_reserve_currency` helper recognises the two national laws, preserving the existing AI protection against an automatic faction-join switch away from a government's own currency. The addition uses the existing domestic-debt treatment, including its limitations described below.

## What the current code models

`reserve_currency` is a single law slot. It selects one currency basis, rather than tracking a central bank's mixed portfolio of dollars, gold, sterling and other reserve assets. Domestic currency identities have also been placed in that slot, which is why its name and economic meaning no longer line up cleanly.

Each country has an independent `currency_strength`. Its monthly calculation responds to inflation, debt risk, monetary policy, stability, economic conditions, war and sanctions. Selecting dollars does not replace this national strength variable with the American value.

The selected reserve option can add investment-return and trade-opinion benefits calculated from issuer strength and the number of adopting countries. The investment component is clamped between −0.03 and +0.03; trade opinion ranges from +0.025 to +0.10. This is an abstract network benefit, not an actual reserve-portfolio valuation.

Issuers can receive a base monetary income of **0.0225 in-game billion per week per adopting country**, before applicable modifiers. Adopters are counted as countries, not weighted by their reserve amounts or economic size. The mechanism does not represent each holder transferring that sum to the issuer.

Debt is the most consequential simplification. `calculate_debt_fx_factor` uses `1 / currency_strength`, capped at 2, while `no_foreign_reserve = 0`; the factor is 1 for the domestic option. The law's adoption hook changes that variable immediately. A country at strength 0.8 can therefore move from a 1.25 debt-service factor to 1 by selecting a domestic law, even though existing foreign-currency contracts have not been separately refinanced. This is an existing structural weakness, also inherited by the two additions; it is not a realistic model of the denomination of outstanding debt.

Reserve-law changes generally cost only 50 or 75 base political power. There is no separate stock of dollar claims, old dollar debt, reserve diversification progress or settlement-network conversion. The existing AI can also change reserve laws automatically on some faction joins and leaves. Political alignment is consequently more mechanically decisive than the underlying financial contracts.

Relevant providers: `common/ideas/AA_law_expanded_economics.txt`, `common/scripted_effects/00_currency_effects.txt`, `calculate_debt_fx_factor` in `common/scripted_effects/00_money_system.txt`, reserve counters in `00_economic_system_utilities.txt`, and the faction callbacks in `common/on_actions/MD_on_actions.txt`.

## Historical interpretation

The dollar's international role must be distinguished from a country's domestic money. Under Bretton Woods, participating national currencies were related to the dollar through adjustable fixed parities, while official dollar-gold convertibility underpinned the arrangement. The United States ended that convertibility in August 1971; this did not mean that other countries ceased having their own currencies. See [Federal Reserve History](https://www.federalreservehistory.org/essays/gold-convertibility-ends) and the [US Office of the Historian](https://history.state.gov/milestones/1969-1976/nixon-shock).

The French franc also had a reserve and regional monetary role. The franc area's African currencies remained distinct monies linked through monetary agreements; they should not be represented as every member simply adopting French banknotes. See [Banque de France's monetary-cooperation history](https://www.banque-france.fr/fr/banque-de-france/partenariats-afrique-france). The addition is deliberately a French national option, not a complete franc-area simulation.

The lira was Italy's national currency, with the Banca d'Italia balancing credit, investment and external stability. The breakdown of Bretton Woods, inflation and exchange controls form part of that historical context. See [Banca d'Italia, from the 1950s to Maastricht](https://www.bancaditalia.it/chi-siamo/storia/anni-cinquanta/index.html). The generic inherited modifiers are not estimates of the effect of choosing the lira.

The [IMF's reserve-currency study](https://www.imf.org/-/media/files/publications/dp/2020/english/rceimsea.pdf) identifies strong inertia and network effects, alongside financial links and currency credibility. It also includes historical French-franc reserves and describes the continuing sterling area around 1970. Dollar dominance therefore supports a strong default and substantial switching friction, not a claim that all reserves everywhere were dollars or that national currencies were absent.

## Recommended next design, not implemented

1. Keep national currency separate from reserve and settlement alignment. France can use francs at home and maintain a dollar-heavy external position; the same applies to Italy and the lira.
2. Keep existing foreign-currency debt outstanding after a reserve-policy change. Alter new borrowing and refinancing gradually, rather than erasing the exchange exposure of old loans.
3. Represent diversification as a funded transition with a stated duration, reserve requirements and credible alternative payment access. A multiyear transition is a gameplay proposal, not a directly measured historical coefficient.
4. Give dollar settlement practical advantages through liquidity, access to borrowing and accepted trade finance. Require actual alternative institutions or agreements to replace those services. The dollar should be attractive because of these links, while preserving a costly route out.
5. Weight issuer advantages by meaningful reserve demand or economic exposure instead of treating every adopting country equally. Distinguish the sterling and franc areas and Comecon clearing from a universal reserve-currency menu.

A permanently compulsory dollar law would remove useful RP choices. A cheap instantaneous switch would fail to represent existing obligations. Persistent contracts and gradual reserve reallocation provide a more defensible middle course.

## Verification and source records

`python tools/frf_itl_currencies/validate.py` performs 70 checks of ownership, availability, lifecycle, actual euro conversion, 1970/1985 defaults, source preservation, English labels and native icon packaging. `changes.json` reverses only the four bounded existing-file insertions, without changing earlier baselines. `build_icons.py` packages the retained generated masters. [generation.json](generation.json) contains the full built-in Imagegen prompts.

The three older currency validation suites currently fail on a pre-existing main-law manifest mismatch: their recorded `AA_law_expanded_economics.txt` digest is `6888493f03f5f964c747b1ed2071d8c915125443d9bb70f4202223bc657eed3c`, while the untouched main-law file has digest `2accac6e9292b89d113d35147bb0e78358d8add834b1717cc93ab8e1009ec718`. Their original baselines have not been replaced to conceal the mismatch. The new extension's tests pass independently. No native-game, save/reload or multiplayer test has been performed.
