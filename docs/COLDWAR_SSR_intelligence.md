<!-- IMPERIA COLD WAR: SSR agency creation restriction, scope, compatibility and source attribution. -->
# SSR intelligence agencies

Union republics with `autonomy_soviet_republic_1985` cannot start a separate agency
through the standard agency interface or AI agency-building logic. The restriction
follows current autonomy status, rather than nationality: an independent Ukraine,
for example, becomes eligible immediately. The USSR and other autonomy types are
unaffected. No autonomous republic list is polled, and no periodic hook is added.

The player control uses the current MD agency creation button's sprite and exact
position (25, 56 in the agency view). A disabled upper button explains Union KGB
authority; an inert lower button absorbs clicks rather than passing them to the
native control. This is an interface restriction, not an invented engine rule.
The AI strategy sets its agency factory budget to -10,000 while creation is
restricted; it aborts when the country becomes eligible.

The general random-agency reward and faction spymaster reward check the same
eligibility predicate, preventing those scripted rewards from bypassing the UI.
The 14 republic histories contain no agency grant active at the 1970 start. Their
modern Ukraine/Belarus agency setup belongs to the 2000 date blocks.

Already-established agencies and construction already underway in old saves are
retained. Direct console commands,
external scripts and future country-specific grants can bypass the interface;
future SSR agency grants must check `COLDWAR_can_create_intelligence_agency`.
This gameplay restriction centralises independent foreign intelligence in the
Union agency; it does not model republican security offices as separate services.

Technique credit: [Yard1, Intelligence Agency Blocker](https://github.com/Yard1/HoI4-Intelligence-Agency-Blocker).
The two-layer UI blocker and AI factory-budget technique are adapted from that
resource, with credit retained in code and the repository README. The SSR predicate,
MD reward guards, current-view alignment checks and integration tests are project
additions. Carry the Yard1 credit into the published download description as well.

Verification: `python tools/ssr_intelligence/test_restriction.py` checks all 14
SSR identities, status changes, native button alignment, AI activation and release,
reward guards, preservation of original random rewards, history dates and encoding.
These are static/script-fixture checks; native mouse input, agency creation and
multiplayer synchronisation still require an in-game test.
