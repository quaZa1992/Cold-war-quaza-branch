# Colonial Affairs runtime

<!-- IMPERIA CW — Cold War: unified security-register navigation. -->

The native entry point is **Decisions → Security Affairs**. `COLDWAR_COL_section` stores the selected tab: 0 Territories, 1 Internal Files, 2 Foreign Files. With no saved selection, an active administrator defaults to Territories; Britain/Germany without a selected administration default to Internal Files; other countries default to Foreign Files. The three predicates are mutually exclusive. The category is available to human players in the existing 1970/1985 scenario envelope even when no organisation is accessible.

The British internal file uses the current IRA target and policy providers. The German file uses `COLDWAR_COL_own_raf`, which preserves the organisation's existing date, ownership, initialization and dissolution gates. Its countermeasure button additionally requires `cwsec_initialized` and the native German cabinet visibility predicate, then opens `cwsec_open`, selects `cwsec_tab = 1` and calls `COLDWAR_GER_1970_sec_gui_refresh`. It does not replace German policing or recalculate a parallel RAF budget. Germany before 14 May 1970 sees an observation notice.

Foreign organisation names, emblems, strength and support buttons additionally require `COLDWAR_COL_contact_target_available`. The browser selects the smallest eligible state ID above the current target and wraps to the smallest eligible ID. Every candidate passes the complete per-state foreign-contact gate before selection. If access is lost, the organisation content is hidden and the requirements sheet is shown; the main register remains accessible. Existing organisation registration and aid effects are unchanged.

The historical inclusion and grouping decisions are recorded in [HISTORY.md](HISTORY.md) and [registry.json](registry.json). Weekly budget values are gameplay calibration, not quotations of historical government expenditure. The runtime preserves existing ownership, control, cores, governments and constitutional arrangements.

`runtime.py.build(root, registry)` returns the canonical generated scripts and English localisation. Run `compile.py` to write them, merge UI localisation and maintain the manifest. Script files use UTF-8 without BOM; localisation uses UTF-8 with BOM. `validate.py` checks installed sources. `test_runtime.py` exercises a bounded model of emitted script AST; neither establishes native engine behaviour or visual correctness.

## Eligibility and sovereignty

Colonial administrations use the persistent `IMP_is_1970_scenario` start-date check. Regional contacts/domestic cases support the 1970 and 1985 bookmarks, never the MD 2000 bookmark.

Each administration is one historical registry group. Its first state is a persistent data record, which does not need to remain under the administrator's sovereignty. Reconciliation examines the controlled member states and records the live foreign administrator in `global.COLDWAR_COL_power_<id>` and the anchor state's `COLDWAR_COL_power`. A locally owned subject territory uses its actual overlord. A native successor which is independent is excluded. A territory outside the live administrator's ownership or actual subject relationship receives no colonial modifier or expense.

Partial independence is supported: releasing the anchor does not remove the administration of another retained state. The weekly budget is prorated by the number of eligible controlled member states. This is a simple member-count allocation, not a population or GDP allocation.

One historical administration split simultaneously between several unrelated foreign powers is a known limitation. The first eligible registry member determines the administrator; members held by another power are excluded from that administration's budget and modifiers. The runtime does not merge or transfer their territory to resolve the split. Protected-state rows marked `subject_only` require the actual locally owned subject relationship. If the protected state is annexed outright, that protected relationship no longer qualifies.

## Policies and expenditure

The four policies can be revised once every 180 active administration days. Their modifiers affect only live controlled member states. Weekly expenditure persists between petitions.

| Policy | Weekly base multiplier | Local construction | Local resources | Native occupation effects |
| --- | ---: | ---: | ---: | --- |
| Civil Administration | 1x | -5% | -5% | Resistance target +8 points; resistance growth +0.02; compliance growth +0.005 |
| Development Programme | 3x | +8% | +3% | Resistance target +3 points; resistance growth -0.01; compliance growth +0.015 |
| Security Administration | 2x | -15% | -10% | Resistance target -3 points; resistance growth -0.01; compliance growth -0.02 |
| Constitutional Self-Government | 1.5x | -5% | -18% | Resistance target -6 points; compliance growth +0.02 |

Armed-conflict profiles initially use Security Administration; other profiles initially use Civil Administration. Self-government is a domestic administrative programme: it does not grant cores, factories, autonomy or independence automatically.

The registry base budgets are multiplied by two at emission, before policy and retained-member factors. Every weekly calculation reads **all eligible members' current native resistance**, independently of the selected UI file. At mean resistance 40 it adds 25% to expenditure; at 60 it adds 50%. There is no compound accumulation because each calculation starts from the base.

War profiles add 30 native resistance-target points and retain a 35% actual resistance floor. Contested profiles add 20 target points and retain a 25% floor. These apply only where native occupation resistance already exists; quiet/associated territories are not force-converted into fictional wars. Policies cannot permanently remove this colonial pressure. A paid petition settlement has a 15% chance to set a 90-day detente: floor 15%, target pressure reduced by 10 points. An independent successor loses the colonial administration and its floor entirely.

The native state dynamic modifier uses `resistance_target` as a ratio (`−0.03` for three target points). `add_resistance_target` uses point amounts (`5` for five points). Construction uses `state_production_speed_buildings_factor`; resource extraction uses `state_resources_factor`.

Existing native resistance adds cumulative stages on top of the selected policy. At 20% resistance, construction loses a further 10%; at 40%, local resources lose 10% and required garrisons rise 15%; at 60%, local supplies fall 10%. The modifier reads state variables `COLDWAR_COL_garrison` through native `required_garrison_factor` and `COLDWAR_COL_supply` through native `local_supplies`. Every application resets these variables before applying the current bands, so reductions in resistance remove the corresponding penalties. A quiet state without native resistance receives no stage penalties. Native full-uprising behaviour is retained; the stages create no custom war or insurgency meter.

The compiler integrates `COLDWAR_COL_recalculate_budget` into native `calculate_additional_expense_rate` in `00_money_system.txt`. The result, `COLDWAR_COL_total_weekly_cost`, is added once to `additional_expenses_rate`, the actual native weekly expense accumulator. There is no daily treasury subtraction of the weekly amount. Budget reconciliation does not call GUI or economy-update hooks recursively. Numeric budget literals are emitted with at most five fractional places.

## Petitions

Each administering country receives at most one pending concern. Reviews occur every 180 days, with a 60-day response window. A transferred pending concern counts toward the new administrator's one-concern limit. Petitions are administrative and political; they do not automatically manufacture a liberation war.

| Response | Payment | Effect on eligible states |
| --- | --- | --- |
| Public-services grant | $0.05 billion once | Construction +5% for 90 days; +5 compliance where native occupation applies |
| Public consultation | 15 political power | Local resources +3% for 90 days; −3 resistance where native occupation applies |
| Retain existing arrangements | None | Construction −5% and local resources −5% for 90 days |

An unanswered petition applies the same temporary penalty as retaining existing arrangements. Political backing raises the next petition's grant cost to $0.075 billion or its consultation cost to 25 political power. The payment and effects are guarded again when the event option executes. A native event pins its anchor, serial number and displayed costs. Only one petition event can be open per country. Every response checks that the pinned generation is still pending and clears the open-window receipt even if it is stale. An old event cannot charge for or resolve a later petition.

## External assistance and regional intelligence

The selected state ID is country-owned `COLDWAR_COL_support_target`. Both state-view visibility and the decision-category file require a native agency and **network_strength > 50 in that exact state**. The country-wide network strength and a network in a neighbouring state do not substitute. Every executable aid effect rechecks the same regional condition, ownership, cooldown, affordability and aid cap. Network loss closes the state popup and hides the file, without refunding already delivered aid.

Colonial political backing costs 15 PP and strengthens the next petition; funding costs $0.05bn and gives +5 native resistance target for 180 days; arms cost 15 PP, 250 infantry weapons and 25 command/control equipment and give +5 current resistance plus +5 target for 180 days. Colonial packages retain their per-sponsor/per-administration cooldowns and shared 15-point cap. Native resistance must actually exist for armed effects. Peaceful political organisations cannot be turned into a war through this panel.

Outside registered colonial administrations, any actual non-core occupation with native resistance can expose a local resistance contact. Political backing costs 15 PP and lowers compliance by 3; money/arms use the same prices and native target effects. Each sponsor can maintain one funding delivery and one arms delivery across these local contacts for 180 days. This deliberately simple capacity is separate from the per-administration colonial cooldowns. A state has one shared +15 target cap. The original occupier is recorded: a new occupier does not inherit previous supplies. Native resistance target entries are refreshed for two days and removed when aid expires or the occupation ends.

A successful delivery rolls disclosure: political 10%, funds 25%, arms 40%. Success without disclosure has no automatic public opinion penalty. A disclosure gives the sponsor −1% stability, applies −25 relations for 180 days from the responsible government, sends that government a country event, and broadcasts a major news event. The notified government gains 15 PP when protesting. Event-local sponsor and region targets travel through the news chain; no shared global news identity can be overwritten by another sponsor. Exact engine rendering and concurrency remain untested.

## New IRA and RAF regional cases

The previous IRA seven sliders, two interfaces, counterdecision category, static/dynamic conflict modifiers, incident module and direct Libyan decision duplicates are retired. Original sources are archived outside loaded folders. Remaining British political focus graphs consume regional organisation strength through bounded adapters. The two obsolete Libyan IRA delivery focuses are removed; neither has a remaining dependent focus. Actual support is now commissioned through the shared regional file and its network gate. Inert old identifiers exist solely for save cleanup; they contain no retired effects.

The IRA is active in state 17 under British ownership/control in the 1970 and 1985 bookmarks. Regional strength starts at 35. This strength index is authored gameplay calibration, not an estimate of popular support. It uses the shared aid, visibility, disclosure and emblem system. It never force-enables native occupation resistance in core territory.

The RAF is an adapter to the **existing German module**, not a new strength simulation. Regional files open after 13 May 1970 in states 41, 42, 1080 and 1251 only while `COLDWAR_GER_1970_initialized` is set, `cwger_raf_gen < 4`, and the RAF is not dissolved. Its native source/readers are `COLDWAR_GER_1970_terror_tick` in `common/scripted_effects/COLDWAR_GER_1970_effects.txt` and `COLDWAR_GER_1970_sec_tick` in `COLDWAR_GER_1970_windows_effects.txt`: cadre strength and milieu feed recruitment, manhunts, generations and attack-planning speed. Foreign political aid adds 2 milieu; arms add 1 cadre. Funding/arms add 5 ongoing aid for 180 days. **All four regional files share one 15-point RAF aid cap**. Each monthly aid point adds 0.05 cadres to the existing native `cwger_raf_cadre`, capped at its native 120 limit. Network, stockpile, treasury, cooldown and disclosure rules apply as for other files. Dissolution blocks further payments. The adapter never calls the full German monthly tick, adds shared IRA incidents or charges a second regional police budget. Existing German countermeasures and attack plans retain their own values. RAF case visibility in 1985 requires that module actually to exist; the adapter does not fabricate its state.

The following new regional policy table applies to the IRA:

| Regional policy | Weekly budget | Monthly strength change | Other effects |
| --- | --- | --- | --- |
| Routine policing | $0.005bn | +1 | No additional restriction modifier |
| Community liaison | $0.012bn | −0.5 | Slow, costly de-escalation |
| Intensive investigation | $0.020bn | −1 | Additional construction −5% and local manpower −2% |

Changing policy costs 25 PP and locks that regional mandate for 180 days. Choosing the existing policy is blocked. Foreign active aid adds 0.1 monthly strength per aid point; political support adds 5 strength once, arms add 3 once. Funding/arms add +5 ongoing aid for 180 days, capped at 15. IRA strength has a 25 minimum and a 90 maximum. Regional construction penalty is strength × −0.1%, resources/workforce strength × −0.05%. Above 44 strength there is a 15% monthly incident chance, at most one incident per country every 90 days; an incident costs 0.5% stability and 10 PP. A negotiated British settlement flag from the retained national political route deactivates the IRA case.

`on_monthly` is already a per-country native hook, as demonstrated by main MD's `MD_on_actions.txt`. The shared monthly callback therefore updates its current country directly, without another `every_country` multiplication. Startup initialization preserves existing strength and policy locks. Cross-state startup copies use the immediate country scope rather than assuming a global ROOT is that country.

## Native resistance and cleanup

Quiet and associated territories do not have native resistance force-enabled. Only documented armed-conflict profiles can seed it, and only where the registered native tag already has a core. No new cores are created. Existing native resistance is not indiscriminately reset.

When this mechanic creates a forced override it stores both an ownership flag and the exact original occupier in `COLDWAR_COL_forced_power`. A sovereignty change clears that exact override, rather than disabling an unrelated override belonging to the new occupier. The persistent seeding receipt prevents initial-resistance rewards from replaying after reconquest.

All administrative and temporary petition modifier providers require `COLDWAR_COL_active_state`; daily cleanup removes their entries and custom resistance-target entries from ineligible states. `COLDWAR_COL_registered` identifies the states covered by the shared system. The Sahara migration removes the old `COLDWAR_SAHARA_political_mobilisation` modifier to prevent it stacking with the new administration.

## UI contract

### Domestic measures

`measures.py` owns `COLDWAR_colonial_measures.txt` effect/trigger adapters and appends contact outcome events 4–7. `COLDWAR_COL_measures_open` toggles the organisation's measures sheet; `COLDWAR_COL_measure_page` selects one of its two pages. All German measure wrappers call the native `_sec_can_*` and `_sec_act_*` providers, retaining their unlocks and cooldowns. `raf_programmes.json` is the common catalogue; `tools/west_germany_1970/security_contract.py` owns their actual actions, lifecycle, monthly programme effects and budget calculation.

Northern Ireland lazily initializes `COLDWAR_COL_tension = 55`, without resetting existing organisation strength or policies. The monthly hook applies the existing base police drift, plus active programme changes, foreign aid and tension. Tension above 69 adds +0.5 strength/month; below 36 adds −0.5. Tension stays within 20–95. Organisation remains within the existing 25–90 bounds. If organisation exceeds 44 and the incident cooldown has expired, monthly incident probability is 15%, 25% at high tension, or 2% during a ceasefire. The original incident effects and 90-day cooldown remain.

| British measure | Upfront PP / bn | Weekly bn | Term / cooldown | Consequences |
|---|---:|---:|---|---|
| Casework | 20 / 0.025 | 0.003 | 180 / 180 days | Agency required; strength −2, then −0.5/month. |
| Employment/complaints | 30 / 0.040 | 0.004 | 180 / 365 days | Tension −8, then −1/month; incompatible with internment. |
| Internment | 45 / 0.020 | 0.006 | 90 / 365 days | Strength must exceed 44; −8 strength, +15 tension, −1% stability; +1.5 recruitment/month and −3% local manpower while active. Blocks ceasefire/reform/roundtable combinations. |
| Detention review | 15 / 0 | 0 | Immediate | Ends internment's cost/restriction/recruitment penalty; strength +3, tension −8. Preserves cooldown. |
| Confidential contacts | 25 / 0.015 | 0.002 on success | 90 / 180 days | Tension below 71, no internment; 60% ceasefire and tension −5; 40% failure, tension +5 and −0.5% stability. Ceasefire gives −0.5 strength/month and 2% incident probability. |
| Constitutional roundtable | 60 / 0.080 | 0.006 | 180 / 365 days | Active ceasefire, tension below 46, reconciled aid below 6, no internment. Tension −10, then −1/month; strength −0.5/month; −1.5% stability. At day 60, 30% chance of obstruction ending talks and ceasefire, +10 tension and +3 strength. No automatic settlement. |

Each German programme requires the actual active RAF case and native security cabinet. Coordination additionally needs BKA level 1 and cadres: 25 PP, 0.035bn upfront and 0.003bn/week for 180 days; +8 trace initially and +1/month for each wanted person still at large, capped at 100, without automatic arrest. Judicial review costs 35 PP, 0.025bn upfront and 0.002bn/week for 180 days: rule of law +3, security −2, milieu −3 initially and −0.25/month. Medical review requires prisoners, hunger pressure above 9 and security above 1: 35 PP, 0.030bn upfront and 0.003bn/week for 90 days; hunger pressure −10, milieu −2, rule of law +2, security −2. It does not replace the selected prison regime. Judicial/medical review have 180-day cooldowns.

<!-- IMPERIA CW — Cold War: one RAF runtime and focus unlock contract. -->
Programme focus requirements are respectively **BKA Expansion**, **Data Protection** and **The Stammheim Trial**. Existing completed focuses recover their unlock receipts without replaying rewards. Legacy live/cooldown programme flag names remain valid; an already paid term can finish, but future activation requires its focus. The native cabinet's fourth tab and the shared file use exactly the same actions. Relevant focus rewards refresh the native case immediately. The existing reconciliation focus retains its OR prerequisites.

Before an IRA measure is paid, local aid is reconciled and ownership is rechecked. All paid actions recheck political power, treasury, programme cooldown and institutional prerequisites at effect time. A blocked action does not pay. Active programme flags drive weekly costs; expiry or loss of the case ends the cost. Cancellation/loss preserves cooldown flags. The existing national expense hook calls `COLDWAR_COL_domestic_budget`, which adds these costs once. The dossier's regional cost includes active British programmes; costs never depend on which UI page is open.

The existing once-per-country monthly contact hook owns British measure effects. The native German monthly dispatcher alone invokes `COLDWAR_GER_1970_security_external_monthly`, before native recruitment and manhunts; common contacts never tick RAF aid or programmes. Recomputing derived threat, displayed costs or GUI geometry cannot replay monthly effects. The delayed roundtable event checks that the original Northern Ireland case and roundtable remain active. Its 365-day cooldown prevents a second roundtable from taking over an old 60-day callback. Receipt events describe outcomes after activation; they do not offer a second charge or an agreement acceptance option. See [MEASURES_HISTORY.md](MEASURES_HISTORY.md) for historical evidence versus authored game values and [SECURITY_CONTRACT.md](../west_germany_1970/SECURITY_CONTRACT.md) for German lifecycle, custody and stale-action checks.

Country selection uses `COLDWAR_COL_selected` (one-based registry index) and `COLDWAR_COL_selected_anchor` (saved state ID). Navigation and policy effects run in country scope. `COLDWAR_COL_refresh_view` copies resistance, compliance, cost, policy, pending concern, days remaining, state count and current construction/resource percentages into country-owned `COLDWAR_COL_view_*` fields. Construction and resource percentages average each eligible state's actual administration variables after policy and resistance-stage effects; they are not fixed policy-label values. Temporary petition grants or penalties remain separate native modifiers. Resistance and compliance are read from the native `THIS.resistance` and `THIS.compliance` values and averaged over eligible member states. They are not a second custom insurgency simulation.

The selected anchor exposes `COLDWAR_COL_policy0` through `policy3`, `weekly_cost`, `resistance`, `compliance`, `issue_days`, the `COLDWAR_COL_issue_pending` flag and its current country target. The support panel uses `COLDWAR_COL_support_index`, `support_bonus` and `support_resistance`, with eligibility checked by `COLDWAR_COL_can_support_political`, `funding` and `arms`.

Native engine load, state-context scopes, dynamic country-variable resolution, tooltips, save/reload behaviour and multiplayer UI interactions still require an in-game test. The emitted source and bounded AST harness cannot establish those behaviours.
