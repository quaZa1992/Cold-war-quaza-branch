IMPERIA COLD WAR

# Kuwait-war access, northern counterplay and Basrah correction

Implemented on 25 October 2026 following the user's request to repair the map label and make the existing USA Gulf branch respond to a real Iraq-Kuwait war. The immutable original Gulf catalogue and original USA approval remain unchanged. The existing fifteen Gulf focus IDs are retained; fourteen are visible. The obsolete contact receipt is intentionally hidden again. This revision supersedes earlier Gulf runtime hashes without changing the other 266 USA focus blocks.

## Historical scope

The [primary-source research record](PLAYER_REVISION_RESEARCH_20261025.md) distinguishes the documented US covert aid programme of 1972-75, routed through Iran, from the political appeal, local uprisings and subsequent humanitarian intervention of 1991. Washington did not historically guarantee or arm a successful Kurdish overthrow in March 1991. The limited-war branch has the higher AI weight. The armed branch is an optional RP escalation using the earlier documented method, available through actual crisis conditions rather than a fixed 1991 date. Its description does not assume that 1972 has already occurred in an early campaign.

Garrison quantities, resistance changes, timers and money values below are authored game balance. They are not claims about an exact historical Iraqi appropriation or troop order. Resolution 688 is not represented as an automatic grant of Kurdish independence or an explicit UN no-fly-zone authorization.

## US access and commitments

- A live Iraq-Kuwait war directly opens the crisis conditions, including ordinary declarations and a war already present in a loaded save. The special historical aggression receipt remains compatible but is no longer mandatory. Iraqi ownership/control of either Kuwaiti state or subjection of Kuwait also keeps the crisis open. Full restoration of independent Kuwait closes the offensive crisis.
- Desert Storm is bypassed when the USA is already fighting Iraq. Open Northern Channels accepts Desert Shield, Desert Storm or Coalition Mandate as alternative predecessors. Its availability also accepts the live Kuwait crisis while the USA remains at peace. Humanitarian relief and northern access retain independent entry points.
- Observed liberation following Iraqi occupation or US belligerency supplies a once-recorded 180-day postwar opening. Merely opening and diplomatically settling an unoccupied war does not fabricate an Iraqi military defeat. The observer does not refresh the term every day.
- Iran now receives a real northern-access offer, event 14. A first accepted northern-access agreement costs the USA 0.50 billion, without a cash gift to the host. An accepted Iranian route provides the historical covert-supply precedent; a separately consenting Turkish border route is an RP alternative. Distant French, British or Saudi basing rights alone cannot supply the underground. Hosts can refuse or withdraw access.
- All first host invoices now require the complete affordability test at recipient acceptance. The old OR grouping incorrectly allowed a non-skipped treasury check to substitute for money. Both the request and final transaction now group the conditions correctly. Previously paid host receipts avoid a second setup fee.
- Underground preparation still costs the USA 0.25 billion and 1,000 real infantry weapons. It creates one finite cache, seeds at most two eligible Iraqi-held northern states and uses the common 90-day support programme at 0.05 billion per week. Expansions require a separate 0.10 billion payment and thirty funded days. Payments retain the existing native daily proration from short weekly literals.

## An uprising with Iraqi counterplay

The observer requires at least two organised, eligible Iraqi-held states at 80% native resistance, a real wartime/postwar opening and a committed arms cache. Thirty qualifying days precede a public 45-day warning. Losing those conditions pauses the warning and clears it after fifteen days below the conditions. An implemented and respected autonomy settlement ends the grievance. Withdrawing American funding does not erase weapons already committed locally.

The executing uprising helper rechecks the actual eligible hot states. Transfers remain bounded to prepared northern strongholds. Iraqi cores and claims remain. The existing native core-group revolt guard still prevents the generic resistance event from racing the bespoke warning. Actual resistance growth, native daily ordering, combat strength and campaign pacing remain engine-rehearsal questions; the bounded models explicitly do not simulate those systems.

| Iraqi decision | Setup invoice | Actual divisions in each state | Continuous local preparation | Resistance reduction per state and operation | Local target contribution | National costs for the 90-day term |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Emergency Security Appropriation | 2% of current annual GDP | 2 | 30 days | -15 points once | -20 points while effective | Army personnel cost +35%; equipment cost +20% |
| Major Northern Operation | 4% of current annual GDP | 3 | 30 days | -25 points once | -35 points while effective | Army personnel cost +60%; equipment cost +35% |

Iraq can fund these operations preventatively during its Kuwait war, before American seeding. The setup invoice is recomputed and guarded on execution. Both decisions share a 90-day cooldown. Ending an operation does not refund the invoice or clear the cooldown.

Readiness belongs to each actual state. Paying while two divisions stand in one state cannot suppress every northern state. Moving those divisions away resets that state's preparation and removes its target reduction on the next observer. Returning troops require another thirty continuous days, and the same paid operation cannot repeat its immediate resistance reduction. A national idea by itself no longer blocks American mobilisation pulses.

An Iraqi response begun in the first fifteen days of the public warning can finish its thirty-day preparation before the full warning elapses. The player can also deploy and fund earlier. A respected political settlement remains another route, rather than an unavoidable release or a required crackdown.

## Multiplayer and old-save behavior

If a Kurdish country appears through another system after the USA commits its underground cache, the script cannot force that existing peaceful player into Iraq's war. An existing independent actor must explicitly coordinate the rising or already be fighting Iraq. The final country handler also requires an actually owned and controlled rebel stronghold. A bounded newly created rebel actor can receive both prepared states, using a temporary creation receipt, without treating the second state as an unapproved gift. Cache delivery still requires its own acceptance.

Existing paid Iraqi operations migrate conservatively: old payments and term/cooldown remain, and previously delivered reductions are marked so they cannot replay. Unknown local deployment history is not invented. Undelivered operations acquire the new local preparation requirements. The old generic USA focus-wrapper entitlements for these fifteen nodes are retired, while earned cash, assets and focus completion are not refunded or repeated.

The USA coordinator now imports the Gulf owner's current fifteen focus blocks directly. This fixes the integration error that stripped the intentionally hidden contact card's `allow_branch`. It also avoids trapping the new Gulf conditions inside obsolete generic wrappers. There are 184 remaining generic legacy wrappers, rather than the previous 199; the Gulf's own executing guards now own those fifteen programmes.

Fully restart HOI4 and reload to load the changed tree/localisation. Existing campaigns receive the daily observation and migration. The date-free USA programmes and the previously selected keep-services/accept-deficit tax calibration remain in place.

## Presentation and map label

Twelve active Gulf focuses now show nonexecuting native numeric previews. The nine bilateral roots show both sides' prospective terms before acceptance, including named ideas and signed modifiers, equipment, setup fees, weekly costs and fixed terms. Host fees are expenditure, not a fictional payment to the host. Direct arms and the underground cache have separate previews; later cache acceptance does not add another cash grant or donor deduction. Each local reconstruction option shows its own 0.20 billion fee, one slot and one infrastructure level.

The real local reconstruction transaction now grants its extra shared slot before construction, inside the same one-time guard. Ownership, control and native infrastructure capacity remain separate requirements.

`VICTORY_POINTS_14402` now reads **Al-Basrah**. The previous dotted character was absent from both relevant native map fonts. The replacement fits the actual victory-point field, retains the localisation BOM and has exactly one English provider; all other 4,844 values were preserved. [City-label evidence](../../usa_1970_expansion_20261024/implementation_support_basrah_label_fix_20261025.json).

## Verification and evidence limits

The current installed validation passes 4,146 assertions over 46 runtime files, including exact semantic comparison with all eleven owned Gulf runtime/staged outputs. Dedicated bounded cases cover 18 access/agency scenarios, 15 local-counterplay scenarios and 14 prospective-preview checks. The preserved Gulf transaction and native-treasury suites pass 20 and 14 cases. The previous USA domestic, calendar, economy, early-cooperation and integrated suites also pass; the advanced-agreement generator retains its 36 model cases.

[Independent review](PLAYER_REVISION_REVIEW_20261025.md) records the historical and layout inspection, counterexamples and confirmed fixes. The [current Gulf view](../../usa_1970_expansion_20261024/installed/USA_GULF.png) reconstructs installed native artwork, labels and connectors. It is a source composite, not a game screenshot. Actual connector routing is an engine observation. The older native run's 92 passing checks predate these changes and do not establish current uprising, save-loading or multiplayer behavior. No current native or network rehearsal is claimed.

Canonical reproduction uses `python tools/usa_1970_expansion/compile.py`, followed by its scoped validator and the three `test_gulf_*.py` files in `tools/iraq_1970`. This bounded route does not run the full Iraqi compiler over unrelated country work. `tools/usa_1970_expansion/gulf_revision.py` owns the host integration; `usa_module.py`, `gulf_counterplay.py` and `gulf_previews.py` own the feature.

## Provenance

New integrations, balance rules, tests and English prose are project work. Existing Millennium Dawn scripts, native country-event frame, registered focus/spirit art and map fonts retain their upstream authorship. No binary game asset or font was modified. Individual artwork credits and separate redistribution permissions remain unknown where the checkout does not identify them. The installed preview notice records the asset-composition transformation. Historical documents remain with their cited institutional publishers; a project marker does not establish ownership of third-party material.
