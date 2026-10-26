# South Korea Expansion: Aggregate Reward Review

## Method and scope

Reviewed the current 298-focus JSON as a design catalogue. The figures below are **raw proposed modifier coefficients**, not guaranteed percentage changes to national output. For each profile I selected one mature, internally compatible policy route through national economy, defence, foreign affairs and Korea, then one current-government programme. Within each owner-qualified policy slot, I counted only the latest selected focus. Party/leader programmes for inactive leaders, the emergency constitution outside the Park profile, transition stages replaced by the final constitutional policy, mutually exclusive alternatives, one-time PP/building rewards, and external agreement rewards were excluded.

The common national route is a high-investment/export portfolio: Pohang/HCI, domestic engineering and laboratories, workplace safeguards, refinancing, thermal diversification, commercial shipyards, rural insurance; a combined-arms/career-NCO/domestic-armaments defence package; alliance burden-sharing, Japan technical exchange, Pacific exports and commercial labour contracts; and a defensive inter-Korean posture. The democratic profiles then add the historical presidential constitution and its institutional safeguards. The Park profile uses the Yushin/emergency-decree route. This is a useful mature-stack check, not an exhaustive maximum search or a claim that every path is equally easy to complete.

## Compatible mature-profile totals

Each row is the sum of selected persistent policy slots. The first two columns are especially important for checking buildup and ongoing budget pressure.

| Governing profile | Civilian factories productivity | Interest-rate modifier | Stability | Bureaucracy-cost modifier | Political power | Social-cost modifier | Recurring commitments per week |
|---|---:|---:|---:|---:|---:|---:|---:|
| Park / DRP, Yushin with emergency decrees | +0.54 | +2.35 | +0.01 | +0.75 | +0.26 | +0.06 | $0.027bn |
| Roh / DJP, constitutional order and ratified conservative coalition | +0.50 | +2.20 | +0.49 | +0.99 | -0.14 | +0.10 | $0.025bn |
| Kim Young-sam / RDP, alternate elected government | +0.40 | +0.95 | +0.50 | +1.08 | -0.34 | +0.10 | $0.021bn |
| Kim Dae-jung / PDP, alternate elected government | +0.43 | +1.50 | +0.70 | +1.00 | -0.24 | +0.39 | $0.027bn |
| Unification Socialist Party, lawful alternate coalition | +0.44 | +2.00 | +0.58 | +1.03 | -0.09 | +0.31 | $0.026bn |

For comparison, the shared national package **before any actual government programme or transition branch** contributes approximately +0.42 civilian-factories productivity, +1.90 interest-rate modifier, +0.13 stability, +0.54 bureaucracy-cost modifier, -0.04 political power, +0.06 social-cost modifier and $0.017bn/week in recurring commitments. It also supplies +0.16 army core defence, +0.18 army organization, +0.11 army attack, +0.07 army defence, +0.07 army morale, +0.08 supply consumption, +0.45 trade opinion, +0.05 foreign-influence defence, +0.18 dockyard productivity and +0.07 agricultural productivity.

The policy totals omit active starting-idea residuals. If the energy problem has only been reduced to its intermediate stage, add +0.10 interest-rate modifier and -0.02 civilian-factories productivity to each profile. If no US assurance has been accepted, retain the starting alliance overlay (+0.05 army core defence and -0.10 foreign-influence defence). Park also retains the political-command spirit until lawful civilian control (+0.04 army organization, +0.03 political power, -0.04 stability and +0.04 personnel-cost modifier). The other four profiles assume constitutional civilian control has removed that spirit. Starting finance, rural, labour and social-insurance problems are assumed resolved by the selected mature route.

All figures use latest-slot replacement. For example, the table counts `Pohang Steelworks`, not both it and its `Heavy Industry Drive` predecessor; `Commercial Shipyards`, not its earlier shipbuilding priority; and `Emergency Decrees`, not both that reward and Yushin’s earlier `drp:constitution` value. The democratic transition total likewise counts the final `One-Term Presidency` constitution, not the earlier transition-phase policies that it replaces.

## Concrete tuning findings

### 1. Roh's compatible programmes: clarified and corrected

**Parent correction, 25 October 2026:** the earlier review overstated a guaranteed collision. The intended replacement key includes ownership: Nordpolitik belongs to the actual Roh incumbent, while the merger belongs to the Army/DJP party programme. A correct owner-qualified selector can retain both. The current design resolves every authored generic `party` owner into an explicit registry owner (here `party:22`), and gives these programmes explicit `army:nordpolitik` and `army:coalition` names. This removes both sources of ambiguity before implementation.

The two outcomes are materially different: Nordpolitik grants trade opinion +10% and political-power gain -6%; the merger grants political-power gain +12% and stability -4% only while an actual participating-party coalition is ratified. The corrected Roh example includes both, adding Nordpolitik's -0.06 PP coefficient and +0.10 trade coefficient to the earlier merger-only example. If the coalition is not ratified, its +0.12 PP and -0.04 stability are absent; Nordpolitik remains independently available to the actual elected Roh government. This is a corrected example portfolio, not a mandatory set of player choices.

### 2. The cross-sector mature stack is very cost-heavy

Across the shared national route alone, the proposed modifiers total +1.90 to interest-rate calculations and +0.54 to bureaucracy costs. With the Park high-investment programme, the totals rise to +2.35 and +0.75; the constitutional profiles range from +0.95 to +2.20 interest and +0.99 to +1.08 bureaucracy. These are coefficients, not percentage claims, but they are large accumulated modifiers across separate economy, military procurement, foreign-service and transition slots. The economic profile does offset them with +0.40–0.54 civilian-factories productivity before starting-energy residuals, and the strategic policy intentionally carries debt/administrative risk. Still, verify these cost-side stacks against their actual consumers before accepting the mature reward scale; otherwise high-cost penalties can dominate the intended policy trade-offs.

The same issue appears in output bonuses. The common route supplies +0.18 dockyard productivity, +0.12 arms-factory production speed and +0.18 army-industry build speed across different slots. The mature Park total reaches +0.54 civilian-factories productivity before its starting-energy penalty. This may be appropriate after a very deep tree, but should be checked against KOR’s base scale and not judged focus-by-focus.

The actual consumers establish the units. `common/scripted_effects/00_money_system.txt:2577` adds `interest_rate_multiplier_modifier` to the pre-clamp interest calculation: +2.35 means2.35 percentage points, not235%. At3333, the bureaucracy reader multiplies only that spending category by `1 + modifier`; the example +0.75 to +1.08 coefficients mean75–108% higher bureaucracy-category spending, not an equivalent increase to the entire government budget. Civilian-industry productivity affects its civilian tax/GDP component rather than flat national GDP or arms production. No hidden cap or general solvency is assumed. Budget scaling, employment, department laws, base debt and existing modifiers still require an engine balance test.

### 3. Recurring cost totals are meaningful when combined

The common package reserves $0.017bn/week. The completed profiles reach $0.021–0.027bn/week, or $1.09–1.40bn per year at a constant rate, before one-time focus costs or any accepted partner contract. This is the arithmetic sum of current terminal expense commitments, not an estimated historical budget. It is substantial enough that the ongoing programme tooltip and treasury affordability should be reviewed as a combined national portfolio; the user-visible burden should not be obscured by each individual $0.001–0.004bn/week line appearing small.

### 4. Leader and party alternatives are being counted correctly here, but selector semantics must match

The Kim profiles count YS- or DJ-owned policy slots only for that actual incumbent. They do not add the other Kim’s leader-specific programme. They are alternate elected-government profiles in the 1970–90 scenario, not claims that either leader historically held the presidency during this period. The USP profile assumes a lawful post-opening electoral/coalition transition and excludes the minjung or underground-left government programmes. The Park profile counts the actual Park/Yushin branch only; it does not stack the constitutional-restraint alternative.

When implementing these totals, verify that the “latest earned policy” selector is truly keyed by the relevant owner-qualified slot and refreshes after an office/party change. The JSON records and arithmetic alone do not establish runtime stacking, active-condition behavior, or the percentage semantics of any modifier.

## Diplomatic consent excluded from the totals

The calculations include only domestic policy records on the selected focuses. They do not count a successful US assurance, North Korean agreement, joint office, cultural exchange, verification mechanism, trade agreement, or partner-provided benefit unless its contract is accepted and its acceptance-specific reward is active. The peninsula figure includes the unilaterally chosen defensive policy through `defector_protection`; it does not include later liaison/contact terms whose availability or reward depends on counterpart participation.

## Recommendation

Retain the broad policy diversity and the clarified separate Roh slots. The source readers and cumulative cost semantics are now recorded; the high-end interest, bureaucracy and $0.021–0.027bn weekly commitments remain visible proposals for multiplayer testing after implementation. Do not count every intermediate focus reward as additive: several are progression levels in the same owner-qualified slot and only their latest value belongs in a mature profile.
