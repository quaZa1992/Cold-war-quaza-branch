IMPERIA COLD WAR: Israel occupation-system concept

29 October 2026. Proposal only. This document adds no runtime mechanic, Decisions, events, population transfers or cores. It follows the user's new request for a simple occupation Decision system; that request supersedes the earlier focus-only restriction for this system. The installed 217-focus tree remains the current runtime baseline. Proposed amounts below are untested game-balance values, not measured historical budgets or casualties.

Revision 2 follows the user's higher-cost and temporary-relief correction: quadruple the first draft's base administration rates, introduce much larger native police-cost modifiers, and replace accumulated permanent reductions with fixed-term relief. Programme expiry restores the full underlying pressure and removes the programme's police discount or surcharge. Renewal extends a paid deadline without stacking the effect.

Revision 3 adds the requested settlement returns, funded local military roles, recurring raids and distinct civilian consequences. All following new amounts and outcome weights remain proposed balance, not approved runtime values or historical casualty estimates. The map preview predates these additional action rows; the concept below is the newer design record. No occupation runtime has been implemented.

Revision 4 adds [the local-event and world-news concept](NEWS_EVENT_CONCEPT.md): nine conditional world-news families, eight local report/response templates, publication limits, original English drafts and colourized archival picture examples. The user subsequently requested an actual shared graphic for all in-game world news and corrected the settler-picture motif. The original World Dispatch native background and a registered full-colour mid-1970s settler illustration are now installed, as recorded in [the artwork notice](../../tools/world_news_skin/NOTICE.md). The occupation rules, Decisions, incidents and new event delivery remain design-only; this artwork installation does not implement them.

Presentation correction: use the ordinary native Decision menu with minimal design. There is no separate occupation window, dashboard, custom meters or separate effect inspector. The user's subsequent map request permits one small embedded map in the category header, following MD's existing decision-category map pattern. The previous custom-screen concept remains superseded. Use short native category descriptions, ordinary Decision rows, native active-duration displays and numerical tooltips. The external minimal preview only expands an effect description for inspection; that is a preview convenience, not a proposed custom in-game control.

### Small embedded occupation map

Keep the map inside the existing Decision menu above the normal local actions. At the opening it covers West Bank, Gaza, Sinai and Golan with geographic state shapes. Gold identifies an Israeli-controlled non-core, subdued grey identifies a territory outside Israeli control, and a small red incident marker identifies current unrest or an active incident without changing the ownership colour. Israeli cores use a separate neutral background. Highlight follows actual controller and core status, not the legal owner alone. A selected area receives a light outline.

Selecting an area is display-only and exposes its ordinary Decisions and short numerical status. It cannot approve settlement, charge money, change government or grant a core. Losing control removes that area's occupation highlight immediately; recapture restores the appropriate status without duplicating assets or arrivals. Other newly occupied states retain ordinary state-targeted Decisions and native world-map targeting; the four-area header does not exempt them from the system.

Verified local MD precedents: `common/decisions/categories/israel_categories.txt` attaches `israel_screen_gui` to a normal Decision category. Its complete first window in `interface/MD_israel_gui.gui` is 500 x 435 and contains Israel, Gaza and West Bank map buttons plus adjacent description/cancel elements. `common/scripted_guis/99_ISR_scripted_guis.txt` uses decision-category context and selection-only callbacks. Those are presentation precedents, not a ready four-area occupation map: Sinai/Golan artwork and the final smaller header geometry still need authoring and verification. The existing unrelated modern systems must not be activated for the 1970 scenario.

The same category file also uses native `on_map_area` state lists for Israel's boycott categories; Bosnia's categories demonstrate country `ROOT` and target-state `FROM` checks. Retain native world-map highlighting where useful. The exact embedded-map implementation must use its own read-only state/controller/core display conditions and refresh when those data change. Four opening regions need only bounded display checks; do not add global daily scans, calendar-bound dirty counters or a second gameplay evaluator for the map. An external map-bearing preview has now been authored as israel-occupation-map.html. It derives the four regions and contextual geography directly from the existing projected province bitmap and state province lists, with individual source hashes and no guessed geographic outlines. Twelve browser checks verified region selection and visibility at three widths; the map and normal Decision rows were visually inspected. This is a concept preview only: no new map runtime or native GUI has been installed.

## Small player-facing model

Use ordinary collapsible native categories for `Military Administration: West Bank`, `Military Administration: Gaza`, `Military Administration: Sinai` and `Military Administration: Golan`. Other states controlled by the actual Israeli actor which are not its cores use ordinary state-targeted Decisions in an additional native category. Legal annexation alone does not end the programme. Existing Israeli cores are excluded. Newly occupied non-core states use the same framework.

Each category shows `Resistance Activity`, 0 to 100, and `Consolidation`, 0 to 100, as short text in its normal description. Show the weekly cash cost and police surcharge there; put resident counts, exact active terms and core obstacles in native descriptions and tooltips where relevant. There are no custom progress bars. Resistance Activity is the single custom incident index, including in annexed states where the native occupation interface may not express the whole situation. Native resistance/compliance remain underlying game systems, not a second custom resistance minigame.

Example inspection, labelled as proposed UI data rather than a live state:

| Field | Illustrative West Bank value |
|---|---|
| Resistance Activity | 30 / 100 with the 13-week security programme; underlying pressure 60 |
| Consolidation | 4.0 / 100 |
| Funded settler residents | 1,500 |
| Base administration cost | 0.080% of Israeli annual GDP per week |
| Occupation Police Cost Modifier | +45 percentage points before optional programmes |
| Security programme | 13 weeks remaining: -30 temporary activity |
| Core obstacles | Consolidation below 100; 0 / 60 qualifying calm months; Israeli ownership absent |

Consolidation is an abstract game-integration measure. It does not assert international recognition, resident consent or legal validity. A settler population ratio never independently grants a core. Preserve other countries' cores, existing claims and RP diplomacy.

## Opening and financial burden

| State | Underlying activity | Base weekly expense | Occupation Police Cost Modifier |
|---|---:|---:|---:|
| West Bank, 208 | 60 | 0.080% of Israeli annual GDP | +45 percentage points |
| Gaza, 209 | 75 | 0.100% | +60 percentage points |
| Sinai, 213 | 35 | 0.060% | +30 percentage points |
| Golan, 587 | 40 | 0.040% | +25 percentage points |

These four base streams sum to 0.280% of annual GDP per week, or 14.56% over 52 weeks, before police surcharges, optional programmes, actual settlement upkeep and existing native garrison costs. Their native police modifiers add to +160 percentage points. This is an addition to the native police-cost multiplier, not a percentage of GDP. In an isolated example with no other modifiers it makes the police multiplier 2.60. Initial Consolidation is zero. Record that the occupation began in 1967 for historical continuity, but do not invent twenty years of completed integration or award instant progress. Audited opening settler counts require a separate historical data pass before implementation; the illustrative UI's 1,500 is not an asserted January 1970 census.

For other states, use simple population-size bands: below 100,000 residents, 0.020%; 100,000 to 499,999, 0.040%; 500,000 to 1,999,999, 0.080%; at least 2,000,000, 0.120% of annual GDP per week. Corresponding proposed native police additions are +20, +30, +45 and +60 percentage points. The four historical presets additionally represent different security and logistical burdens. These are proposed tuning bands. Apply the system to all eligible occupied states, rather than a fixed four-state exemption or an eight-state cap.

Replace the current custom administration/personnel country-budget surcharges with the explicit base stream; do not charge both representations of the same administration obligation. Replace the existing +17-point combined occupation police modifier with the new +160-point total, rather than stacking both generations. Keep distinct native garrison/supply burdens. Replace an old settlement's weekly site charge when importing it into the new site ledger, rather than adding a second upkeep charge. Existing accepted foreign project capital remains restricted to its actual funded project and never finances recurring administration automatically.

Use actual MD weekly money consumers once. Base occupation obligations and existing site upkeep continue while the state is held, including during a fiscal deficit. Optional new approvals require the real setup funds. Ending an optional programme removes its benefit and its own optional expense, not the underlying occupation or occupied settlement obligations.

## Eight regular actions

| Decision | Proposed terms | Meaningful result |
|---|---|---|
| `Fund a Security Programme` | 13 weeks; +0.020% of annual GDP in weekly expenses; Police Cost Modifier +25 points | Activity -30 and incident probability multiplied by 0.60 during the term only. Both effects and the police surcharge expire. |
| `Fund Civil Services` | 26 weeks; +0.015% of annual GDP in weekly expenses | Activity -20 and Police Cost Modifier -10 points during the term only; allows slow Consolidation under the actual conditions. Both reductions expire. |
| `Fund Local Defence` | 26 weeks; 0.10% GDP setup; 100 actual infantry equipment; +0.005% GDP in weekly expenses; Police Cost Modifier +10 points | Requires an actual inhabited funded site. State Local Supplies for the controller +1; Damage to Garrisons -15%; the local raid's favourable-outcome probability +10 percentage points. These benefits expire and cannot stack with another instance of the same programme. |
| `Conduct a Security Raid` | 14 days; 0.10% GDP setup; 25 political power; extra Police Cost Modifier +10 points during the operation; 13-week per-state cooldown | Requires full local control, an actual recorded resistance network and a funded security programme. The resulting disruption is temporary, with explicit own-personnel and civilian-harm risks. No automatic border change, war or core progress. |
| `Approve a Settlement Project` | 0.50% of annual GDP setup; 26 weeks; one approval per state per 52 weeks | Transfer a verified cohort of up to 500 actual residents; arrival agitation +10 for 26 weeks; resident-linked pressure +3 while the new cohort remains; +0.002% GDP weekly upkeep per completed cohort. No instant core progress. |
| `Freeze New Settlement Approvals` | 13 weeks; 25 political power per term | No new settlement contracts or new arrivals; Activity -15 during the term. Both restrictions and relief expire unless renewed. Existing residents and their security expenses remain. |
| `Evacuate a Settlement Cohort` | 0.25% of annual GDP; 25 political power | Return the actual surviving cohort; -10 community relief for 13 weeks only. Removing that real cohort also removes its actual upkeep and its own resident-linked pressure. No permanent general reduction. |
| `Review Constitutional Status` | Actual Israeli state ownership and full control; all hard conditions below; 2% of annual GDP | Deliberate final core decision including the binding civilian-status commitment. Preserve foreign cores and claims. No automatic border transfer, peace treaty, recognition, war or government change. |

Underlying pressure persists separately from the effective Activity shown in the native category description. Effective Activity is underlying pressure plus active shocks and resident-linked pressure, minus currently funded relief, clamped to 0-100. A Decision never permanently subtracts its relief from underlying pressure. Expiry removes the relief in full at that time. Civil-service expiry also removes its police discount; security expiry removes its temporary extra deployment and probability reduction. Renewals open in the final four weeks, extend the existing deadline and pay another actual term without stacking strength. This allows continuous expensive management but no permanent solution bought once.

West Bank example: underlying activity 60, security relief -30 and effective activity 30. At week 13, protection expires and activity returns to 60 under otherwise unchanged conditions. Gaza example: security, services and a temporary freeze together can bring 75 down to 10; each expiry exposes that programme's portion of the underlying pressure again. Real migration, money spent, personnel losses and earned Consolidation remain actual outcomes. Their associated temporary relief does not become permanent.

Settlement contracts must be completed only with full state/province control, a usable connection, actual funding and a valid origin population. One cohort is one recorded transaction. A focus-funded contract replaces the matching setup invoice; it is not an additional invoice or an additional free cohort. Actual building levels, where included in a contract, receive matching extra shared slots before construction inside that same transaction.

The 0.50% proposal prices a basic resident cohort, not an agricultural/fortification bundle. A regional focus contract retains its actual larger bundle invoice and accepted public/partner shares; it replaces the basic invoice once. The existing real partner pool can cover only the contract's specified eligible contribution. It cannot be quoted as new money or pay the same price reduction twice.

### Productive settlement choices

The existing `Approve a Settlement Project` entry can open one ordinary Israeli project-selection event. The chosen option, not merely opening the event, commits its actual price. A native event avoids adding a separate regular Decision for every settlement type. All projects retain the 26-week completion period, up to 500 conserved incoming residents, annual local approval limit, ordinary control/capacity checks and recurring site obligations.

| Standalone project | Proposed complete setup price | Concrete assets at successful completion | Distinct trade-off |
|---|---:|---|---|
| `Residential Community` | 0.50% of annual GDP | The actual resident cohort; no free industrial building | Cheapest demographic commitment, with upkeep, arrival agitation and resident-linked pressure. |
| `Agricultural Cooperative` | 1.00% | One agricultural district and one extra shared slot | Productive land and settlement administration require continuing protection; land-use disputes can feed unrest. |
| `Nahal Outpost` | 1.50% | One agricultural district, one land-fort level and two extra shared slots | A real fortified agricultural site, with additional security commitments and exposure during hostilities. |
| `Workshop and Service Community` | 2.00% | One office level, one infrastructure level and two extra shared slots | Economic and transport assets, with a larger public invoice and a more valuable sabotage target. |

These standalone packages do not rewrite an already paid focus contract's original assets or invoice. An imported national/party project keeps its actual bundle and original accepted investor shares. Every building level receives its extra shared slot before construction, including forts and infrastructure. Actual province control, ownership, native limits and staffing remain separate checks. A focus and local approval cannot pay twice or grant two cohorts/building bundles for one project.

Additional operating returns can be attached to funded Civil Services at actual completed productive sites: Agricultural Productivity +2% for an agricultural site, or Office Productivity +2% for a workshop/service site, only while its paid 26-week programme remains active and Israel controls the site. Cap these new operating-contract contributions at +4% per sector across their own compatible providers. Do not silently cap or replace unrelated previously approved country programmes. A building is a durable asset; a paid operating, security or productivity modifier has its stated finite term. Real tax and output consumers carry the return, rather than creating an unfinanced private-income account.

### Local military role

The military return belongs to an actual outpost and an active funded defence programme. It does not classify all settlers as soldiers or create free field divisions. Local Supplies +1 is a flat native state supply amount, not an invented +100% or +1% national modifier. Damage to Garrisons -15% is the native state modifier; for example it offsets part of a positive occupation damage penalty rather than making attacks impossible. The custom +10-point raid advantage is consumed only by that state's raid-outcome calculation.

The programme consumes actual equipment on each funded term. Its weekly expense and police deployment remain visible. At most one funded Local Defence contribution applies per state, regardless of its number of cohorts or fort levels. On expiry, state supply, garrison protection and the raid advantage return to their unmodified values. A persistent land fort remains physical construction. The need to protect actual residents remains after the optional programme ends. Armed local groups and unresolved attacks can increase the weight of a later settler-violence event; funded oversight and civil services can temporarily limit that escalation. These are proposed event relationships, not a claim that every Nahal member or civilian settler behaved identically.

### Recurring security raids

Keep one regular raid entry, with one operation per state at a time and a 13-week cooldown. A raid is an abstract local game operation, not a tactical planning interface. Recheck actual control and programme eligibility when committing it and before resolving it. A genuine loss of the target stops invalid execution and preserves the exact unspent/committed accounting. Annexation or recapture never resets the raid cooldown or grants its outcome again.

Illustrative resolution weights before the funded local-defence advantage:

| Outcome | Proposed weight | Numerical result |
|---|---:|---|
| Network disrupted | 60% | Activity relief -20 for 8 weeks. |
| Limited result | 25% | Activity relief -5 for 4 weeks; Israeli military manpower -10. |
| Operation escalates | 15% | Israeli military manpower -50; Activity shock +10 for 13 weeks. |

An active Local Defence programme shifts ten percentage points from Limited Result to Network Disrupted: 70/15/15. It does not eliminate the escalation branch. Repeat raids refresh/replace their own disruption family rather than stacking it indefinitely. There is no repeated army-experience, equipment or core-progress reward for performing raids.

Check civilian harm separately from those military outcomes, including after an otherwise successful operation. An initial proposal is a 10% civilian-harm chance, rising to 25% during an unresolved severe local escalation. A triggered severe incident might cause 1-5 local civilian deaths, Activity +15 for 26 weeks, Consolidation -3 and a reset of the severe-incident calm clock. Those amounts are deliberately provisional. Wounded civilians remain people in the population stock and generate temporary treatment/disruption costs; they must not be subtracted as dead. Calibrate actual severity and attribution in rehearsal rather than claiming that a percentage is historical.

The incident event can offer an actual funded investigation/relief response, proposed at 0.05% GDP and 25 political power, with -10 temporary Activity relief for 13 weeks and arrivals restrictions where relevant. Ignoring the incident avoids that new invoice but leaves the escalation unresolved. A response does not restore fatalities or automatically reverse the recorded Consolidation loss. Existing normal country-event presentation is sufficient; no new GUI is needed.

### Civilians, military losses and retaliation

Track Israeli military personnel losses, Israeli civilian/settler fatalities, local civilian fatalities and wounded people separately. A resistance attack can harm soldiers, settlers or local residents, depending on the event. Settler violence can harm local residents, damage property and interrupt services. Israeli operations can also cause local civilian harm. Attribute the event's actor and victims explicitly; do not turn every local resident into a combatant or force equal casualty totals between groups.

Civilian fatalities debit the appropriate actual population and, for settlers, the actual surviving cohort. They are not also charged as military reserve losses. Native state-population/reserve side effects still require the already stated prototype and conservation checks. All losses, expenses and event receipts commit once before player response. Unanswered events, reloads, state-control changes or a cabinet change cannot erase casualties or reroll an unfavourable result.

The long-term loop is productive settlement investment, real local military/logistical capacity, additional protection obligations and agitation, temporary funded stabilisation or raids, possible attacks/civilian harm and renewed administration. Paid programmes can be renewed every 13/26 weeks; settlement approvals recur subject to the annual limit; raids recur after their cooldown. Physical building tiers remain bounded by actual local capacity. After an asset limit is reached, maintenance, protection, services and raids remain recurring choices; renewal grants no new building or shared slot. There is no automatic final victory event while a non-core occupation persists.

HOI4 has no native ethnic-population simulation. Maintain a separate settler-resident ledger and conserve actual source/destination population; do not label the entire destination population Israeli or spawn population/manpower. Country-scope `add_manpower` is a military reserve effect; state-scope `add_manpower` is already used for population changes in this mod. The observed reserve side effects, especially when controller and legal owner differ, require a native prototype before committing the transfer adapter. Reuse the inspected population-observation/conservation pattern, not an untested copy of a helper which requires both states to be owned. If that native accounting cannot remain correct, revise the adapter explicitly before implementation rather than presenting a counter-only increase as a real population move.

## Resistance and incidents

One aggregate underground per state is sufficient. Suggested labels are `Quiet Networks`, `Organising Underground`, `Active Underground` and `Escalating Conflict`. West Bank and Gaza can reference contemporary Fatah/PFLP networks in appropriate descriptions. Other territories use local contextual wording; no invented common Arab organisation, new rebel country tag, spawned division or scripted war is required.

Once per quarter, an eligible state outside its 26-week post-incident cooldown receives one incident roll:

| Resistance Activity | Proposed probability per eligible quarter |
|---|---:|
| 0 to 24 | 5% |
| 25 to 49 | 20% |
| 50 to 74 | 40% |
| 75 to 100 | 65% |

Show the actual modified probability before the player spends. Fixed-term incident shocks also have explicit expiries; completed losses, spent cash and actual population changes remain durable. Settler-related incidents are eligible only with actual residents. Their weight increases with expansion and an unresolved previous incident; they are not a guaranteed event on a fixed date. In the implementation tuning pass, give a majority of eligible personnel-loss results the small 10/25 tier, keep 50 uncommon and 100 exceptional. Final severity weights require rehearsal rather than an invented claim of historical calibration.

Four incident families cover the requested experience:

1. `An Attack on an IDF Patrol`: actual military manpower loss, with small 10/25 outcomes and uncommon 50 or exceptional 100 outcomes; small fixed repair/emergency invoices where relevant. The larger numbers represent a severe game personnel-loss episode, not a claim that an ordinary 1970 grenade incident killed a hundred soldiers.
2. `Sabotage Disrupts Civil Administration`: a bounded temporary supply/output disruption or an actual repair charge, proposed at 0.10% of annual GDP. Show its duration and numerical effects.
3. `An Attack on a Settlement`: site disruption, a 13-week halt to new arrivals, proposed 0.10%-GDP repairs and Consolidation -1. Civilian casualties, if represented, must use the actual surviving cohort and native population accounting; they are not charged again as military manpower.
4. `Settler Violence against Local Residents`: Resistance Activity +15, Consolidation -3 and restart the severe-incident calm clock. A funded investigation costs 0.10% of annual GDP, imposes the arrivals freeze and limits the unresolved escalation. Ignoring the incident preserves the higher recurrence weight. Violence never grants population, land, free assets or core progress.

Casualty/damage effects occur once when the incident is committed. Leaving an event unanswered cannot postpone them. Event options contain actual numeric effects, not prose substitutes. A quarterly country report can combine occurred incidents into one notification. Store only bounded recent records, not an ever-growing archive. Palestinian civilian residents, Israeli settlers and Israeli military personnel remain distinct affected populations in descriptions and accounting.

## An extremely difficult core

Consolidation gains only during paid, stable administration. At war, with uncontrolled territory, with high activity or without funded services, positive progress stops.

- Base gain: +0.20 per qualifying month with Civil Services funded, Resistance Activity at most 25, full control and no Israeli war.
- Established settlement presence: at least 1,500 audited actual residents adds +0.10 per qualifying month. It gives no instant progress and cannot stack with cohort spam.
- The relevant completed civilian-administration focus adds +0.10 per qualifying month only while the required paid programme is active, subject to the same actual conditions. It grants no permanent resistance or police-cost reduction.
- Hard positive ceiling: +0.40 per month across all policies, parties, focuses and Decisions. No focus grants a core or bypasses the clock.
- Activity at least 75 causes -0.20 per month. Serious incidents apply their stated direct setbacks.

Starting at zero, even uninterrupted maximum progress requires 250 qualifying months, or 20 years and 10 months. Actual unrest, wars, expansion, missed funding and setbacks make a longer campaign likely. The display should show the current monthly change, exact missing conditions and a theoretical minimum time, never a promised completion date or a fictitious probability of legitimacy.

The final Decision additionally requires actual Israeli ownership and full control, at least twenty years of recorded continuous control, Resistance Activity at most 10, sixty consecutive qualifying calm months without a severe incident and peace. Executing it also enacts the binding civilian-status commitment covering all permanent residents. This commitment is a consequence of the final Decision, not an unavailable seventh prerequisite with no provider. The core changes Israel's native game treatment only. It removes no other country's core, enforces no recognition and creates no diplomatic treaty. The existing 0.015%-GDP weekly Civil Services payment becomes an ongoing civilian obligation, replacing its temporary programme charge rather than stacking another charge. Record that obligation in the expense ledger after the state leaves the occupation list. Do not delete accepted investor liabilities or population receipts.

Loss of control stops local benefits and spending attributable to actual administration immediately. Preserve the resident/contract/claim history; do not duplicate arrivals or refund completed assets on recapture. Interrupt the continuous-control clock and reduce Consolidation by a proposed 25 points once per genuine loss, guarded against repeated refresh and one-day controller churn. Exact anti-churn timing is an implementation test, not a hidden player burden. Annexation, a new cabinet or a save reload never resets opposition to zero.

## Adapting the installed focus tree

Keep its compact arrangement and visible party branches. Focuses set national policies, institutional capacity, funding contracts and bounded terms; the new Decisions operate the repeated local choices.

| Existing focus or group | Proposed integration |
|---|---|
| `ISR2_occupation_accounts`, Military Administration | Strengthen a paid active administration programme. Any 5% base-bill efficiency discount lasts only for that funded programme's term. Cap combined conditional discounts at 20%; site upkeep remains separate. The system itself exists from day one. |
| Civil administration and `ISR2_labor_functional_rule` | Enable the +0.10 conditional Consolidation term and service efficiency, with actual continuing funding. |
| Regional settlement works, `ISR2_labor_valley`, Gahal entitlements and Mafdal cooperatives | Their actual paid project becomes a recorded settlement/construction contract. Later local approval consumes the same entitlement once. Preserve accepted co-financing and prevent duplicate buildings, invoices and arrivals. |
| `ISR2_mafdal_land_committee` and planning appeals | Improve contract oversight, arrivals controls or investigation expense. They cannot erase existing site obligations or provide a core shortcut. |
| `ISR2_labor_yanai` | Preserve real partner-funded guarantee reserves and insured claims when a funded site is lost or evacuated. |
| Restraint/municipal programmes | Provide only fixed-term relief through paid services, 13-week freezes or enforceable investigation. Programme expiry removes its discounts and relief. |
| Uncontrolled foreign footholds | Retain their separate host/Palestinian burdens and bounded Israeli benefits. They accumulate no controlled-territory Consolidation or core clock. |

Keep the approved maximum +15% workforce route unchanged. This occupation concept adds neither another workforce-size reward nor a negative workforce-size modifier. Actual migration and military personnel losses are explicit transactions, not a hidden workforce multiplier.

Settlement approval remains unilateral in this system. Neither Palestine nor a host receives an establishment veto. Existing Palestinian pressure applies when Palestine exists and the area is its core, with its established area/total caps. Peace offers and partner financing continue to require actual consent where the player is committing another state's policy or money. No opponent player is required to click an option for Israel's budget, incidents or progress to function.

## Performance and multiplayer design

Only the actual Israeli 1970 actor runs the monthly occupation update. Maintain its active state list on initialization and real state-control changes; use a bounded Israeli controlled-state reconciliation to recover missed changes. Recompute an affected state's cached expense immediately after a genuine transaction/control change. The native weekly budget reads one cached aggregate, without rolling incidents or advancing time.

At the four-state opening, the schedule implies approximately 48 regular state updates and at most 16 pre-cooldown incident eligibility checks in a year, plus actual player/control-change transactions. These are design-level cadence counts, not measured script operations, milliseconds, FPS or a multiplayer stability result. Existing other Israel mechanics have their own cadence; do not silently leave a second daily occupation evaluator active after this replacement.

All gameplay randomness uses the synchronized native simulation, independent of hover, an open Decision panel or wall-clock time. Persistent period receipts prevent a reload/rehost or repeated refresh from rolling a new outcome. Invalidated pending construction checks actual control, owner, capacity, real funding and remaining residents before moving anything. Optional programme AI should be conservative and budget-aware, and never choose an automatic core or force a human country's diplomacy.

Before implementation is accepted, native checks must cover held-but-foreign-owned and annexed non-cores, existing cores, source/destination population conservation and reserve side effects, casualties and civilian distinctions, a controller change during a pending project, recapture, genuine partial-state capacity, save/reload period receipts, simultaneous participant actions, stopped funding, all claimed budget streams exactly once and the hard core-growth ceiling. A multiplayer rehearsal remains separate from those single-client checks.

## Historical precedents and limits

- JTA's 8 May 1969 account describes Nahal Argaman as an outpost staffed by people serving in the Israeli armed forces, with vegetable cultivation as its proposed economic basis. This directly supports the military/agricultural project distinction, without establishing any proposed modifier value: [Nahal Argaman contemporary report](https://www.jta.org/archive/third-israeli-outpost-on-west-bank-is-inaugurated-named-for-2-dead-officers).
- A JTA report of 17 November 1969 records military and civilian casualties, attacks affecting local Arab residents, and subsequent security measures in Gaza and Ramallah. Treat its individual attributions as contemporary reporting, not independent proof of every official assertion. It supports separate event actors/victim groups and a recurring incident/security-response cycle: [contemporary incident report](https://www.jta.org/archive/fighting-grenade-incidents-cause-21-israeli-casualties-over-weekend).
- A contemporaneous JTA report of 6 January 1970 records a Gaza confrontation involving Israeli soldiers and PFLP members. It supports an already active underground at the scenario start, not the proposed numerical casualty distribution: [original wire report](https://www.jta.org/archive/israeli-soldiers-and-arab-guerrillas-killed-and-wounded-in-encounter).
- JTA's 27 April 1970 report describes the cabinet dispute over permanent housing for 250 families near Hebron. This supports paid political approvals, staged civilian establishment and domestic disagreement: [Hebron cabinet dispute](https://www.jta.org/archive/new-split-emerges-in-cabinet-over-issue-of-permanent-jewish-settlement-in-hebron).
- JTA's 24 June 1969 report records military authorities turning back an attempted settlement at Nablus. This supports meaningful approval/freeze/enforcement policy before later settlement movements existed: [Nablus approval dispute](https://www.jta.org/archive/troops-turn-back-israelis-who-want-to-establish-settlement-in-nablus).
- The US National Security Council record of 1 February 1969 discusses the contemporary fedayeen movements, retaliation, the Allon proposal and a divided Israeli cabinet. It is a contemporary US diplomatic assessment, not neutral proof of every participant's assertion: [FRUS, document 4](https://history.state.gov/historicaldocuments/frus1969-76v23/d4).
- The 1983 UN seminar report discusses increasing reports of settler violence from 1979/1980. This is a later source, not a justification for copying the same mature pattern into January 1970. It supports a later/dynamically escalating event pool, with attribution to the reported statements: [UN seminar report](https://www.un.org/unispal/document/auto-insert-194986/).

Accordingly, armed underground incidents, military government, Nahal/institutional projects and competing settlement policies fit the early scenario. Later organisations and contemporary mass-settlement levels must not appear automatically at the start. The eventual native core is explicitly alternate-history game design. All proposed budget rates, event chances, cohorts and growth values are balance proposals requiring testing.

Revision 3 API evidence: the installed engine's `documentation/modifiers_documentation.md` lists `local_supplies_for_controller` as a state/war-production numeric modifier and `resistance_damage_to_garrison` as country/state. Its native English formatter renders garrison damage as a percentage. Existing MD state examples appear in `common/dynamic_modifiers/99_BLR_dynamic_modifiers.txt` and the current Israel territorial definitions. The controller supply proposal is +1 flat local supply, not +10% national supply. Do not infer a valid local defence or attack modifier from an invented key or an army-only modifier merely attached to a state. The new raid probability advantage is a proposed custom input to its own future outcome calculation, not an existing engine combat stat. Native income readers for `agricolture_productivity_modifier` and `offices_productivity` were inspected in `common/scripted_effects/00_money_system.txt`; both affect actual native sector income calculations. Those source checks do not prove the proposed new activation, lifecycle or ownership adapter in the engine.

Provenance: original concept prepared with Codex for IMPERIA COLD WAR from the user's specification, the installed Israel V2 baseline and the linked primary/period records. Source institutions and JTA retain their original text rights; no source text or third-party artwork is reproduced. This document claims no ownership of inherited MD code or assets. No runtime or performance test of the proposed occupation system has been run. The native police formula was inspected in common/scripted_effects/00_money_system.txt: the modifier adds to the national police multiplier before its per-capita base and spending ladder. The currency illustration uses an unmodified police-cost base, not a percentage of GDP or the complete current police bill.
