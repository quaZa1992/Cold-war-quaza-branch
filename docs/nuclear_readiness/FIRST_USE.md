# Nuclear first use during a diplomatic confrontation

The 1970 multiplayer scenario can now reach nuclear hostilities without a preceding declaration of conventional war. An existing confrontation, national employment policy and an explicit military order remain necessary.

## Historical basis and gameplay interpretation

The [Kennedy–Khrushchev letter of 22 October 1962](https://history.state.gov/historicaldocuments/frus1961-63v11/d44) makes the communicating government's position explicit while stressing the danger of misreading its determination. The [NSC minutes of the same day](https://microsites.jfklibrary.org/cmc/oct22/doc1.html) distinguish a coercive measure from an immediate strike and record the concern that a surprise attack could precipitate a wider nuclear war. These precedents support a publicly identified counterpart, a period for negotiations and a distinct decision to execute an operation. They do not establish that an actual nuclear attack occurred or that a 72-hour nuclear ultimatum was used historically.

The 72-hour ultimatum, seven-day release window, political costs, penalties and cooling-off periods are multiplayer balance choices. Restored archival photographs illustrate the themes; they do not identify the countries involved in a particular campaign.

## Procedure

1. A human government issues the existing nuclear warning and establishes a reciprocal confrontation.
2. At completed Maximum Readiness, an independent government with actual nuclear missile holdings, offensive nuclear policy and a first-use doctrine may issue **Issue Nuclear Ultimatum** for 100 political power. The counterpart must also be independent; the countries must be at peace, outside the same faction and without a non-aggression pact.
3. A 72-hour public ultimatum begins. The named counterpart is notified, and other human governments receive a public report. Eligible native nuclear raids may be prepared during this period, but launch authority remains withheld.
4. On expiry, seven days of release authority become available against that exact country. A separate native raid order is required. Tactical-only first-use doctrine continues to prohibit state and strategic first use.
5. **Withdraw Nuclear Ultimatum** revokes further peacetime launches without changing readiness, refunding political power or removing tension. The government cannot issue another ultimatum for 90 days, including against a different counterpart.

Both governments may issue their own ultimatum. Their countdowns and release windows are independent, while the confrontation identity and counterpart remain shared. The command panel shows the current escalation status and provides separate own/foreign countdowns in its hover description.

## De-escalation and invalidation

An accepted direct communications offer now permits an immediate mutual stand-down proposal; the offer cooldown no longer obstructs this next negotiated step. Unanswered or rejected offers retain the existing cooldown. Accepted mutual stand-down clears both release procedures before lowering readiness and applying the existing commitments.

Lower readiness, loss of weapons, changed employment policy, capitulation, subjection, a new alliance or non-aggression pact, counterpart changes, a different confrontation serial and either country's nuclear-use revision invalidate the procedure. Withdrawal, confrontation expiry and orphan cleanup also clear release authority. Launch checks independently recheck validity, so a prepared raid does not retain a stale permission until the next callback.

The countdown uses a single hidden country-event chain for each active issuing government. It is saved with the campaign and stops on revocation. Its native delay includes the scheduling hour: `hours = 2` advances the counter once per elapsed game hour in the tested engine. The 90-day ultimatum cooldown prevents a cancelled procedure's remaining callback from attaching to a new ultimatum. No global hourly scan and no random timer are used.

Revocation blocks further launches. An operation already underway remains committed and can still open hostilities when it resolves.

## War opening and consequences

Every outcome of all three native nuclear raids calls the peacetime operation handler before its existing actor effects. Successful-hit attribution also calls the same handler defensively. Its war-state guard makes the operation idempotent, so outcome ordering cannot duplicate the declaration or penalties.

The first resolved nuclear operation against a country at peace with the actor opens war, including an intercepted or unsuccessful attack. The attacker is recorded as the aggressor. The victim receives attacker-specific retaliation eligibility and emergency readiness preparation; no retaliatory weapon is launched automatically. Existing pending diplomatic offers fail their nuclear-use revision check. Existing casualties, fallout, equipment consumption, interception and strike-specific costs remain in the native outcome blocks.

Additional first-use consequences are +20 Cold War tension, +10 world tension, −5 percentage points of stability and a −100 opinion modifier toward the attacker from foreign governments for 365 days. These are additional to the native strike effects. War opening creates no scripted calls to allies; normal faction, guarantee and scenario rules still apply.

Each ultimatum adds +5 Cold War tension and +2 world tension. Its actual contribution after clamping is added to both governments' confrontation record. A mutual stand-down removes only this accumulated contribution, up to 18 points with a warning, a counter-alert and both ultimatums. Actual-use tension is excluded from that refundable contribution. Unilateral withdrawal retains the existing maximum two-point reduction.

## Verification

The 41 source-level scenario and integration tests cover the 72-hour boundary, seven-day expiry, country-agnostic access, target and serial binding, doctrine restrictions, revocation, cooling-off periods, political changes, weapon losses, simultaneous ultimatums, immediate negotiated stand-down, capped tension, war opening, attacker-specific retaliation, invalidated offers and one-time consequences. The native test record is stored separately in `tools/nuclear_readiness/engine_report.json`.

The final HOI4 1.19.3 campaign passed all 16 native checkpoints with no readiness/escalation-module errors, including the restored country-name promotions in event text. The native fixture verifies the real event callback before advancing the remaining boundary steps through the same native timer helper. It invokes the raid outcome handler directly rather than conducting a live combat launch. Neither that fixture nor the source interpreter constitutes a two-client multiplayer or network/OOS test.
