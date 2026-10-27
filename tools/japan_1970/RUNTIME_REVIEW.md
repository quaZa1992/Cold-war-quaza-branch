# Japan execution audit — 27 October 2026

The reported focus is `COLDWAR_JAP_1970_korea_claims_commission`
(Seoul Claims Talks). Its actual completion calls the guarded bilateral offer
helper, which marks KOR pending and fires `COLDWAR_JAP70_BILATERAL.7117`.
The responding country controls acceptance. Completing the focus does not
itself pay for an accepted agreement.

## Evidence and correction

The user's test had AI-controlled South Korea and advancing time. The existing
binary autosave contains the prior Seoul Relations offer receipt and recipient
resolved flag. This is evidence of dispatch and a response, not evidence of
which option the AI chose. No full binary-save interpretation was assumed.

Sender-side acceptance/refusal reports were absent. Added reports for all 39
offer focuses and the four completed-site transactions. Each report identifies
its responding country through native event FROM scope; numeric terms are
explicitly described as already applied. Acknowledging a report grants no
money, buildings, modifiers or research.

Recipient accept/refuse transactions now repeat their pending/unresolved
checks inside actual execution. Acceptance also requires Japan to exist.
This protects against stale or duplicate response events. Existing payment
amounts, beneficiaries, durations, consent and construction rules are preserved.
Dispatch receipts on the 20 single-recipient helpers are recorded only inside
the valid-recipient dispatch branch.

A one-time daily Japan migration restores completed direct offers only where
the current recipient exists and has neither a pending nor resolved response.
It covers 22 recipient routes (20 single-recipient offers plus the two Korean
reconciliation recipients), sends no proposal for an unfinished focus, and
executes no payment or agreement reward. Existing pending/answered offers are
preserved. Broader invitation eligibility is not automatically expanded.

## Whole-tree source coverage

| Content | Source review |
|---|---|
| 212 national/economic focuses | 88 one-time treasury charges; 37 state building grants across 33 focuses; three one-use research bonuses; 41 modifier keys traced to native MD definitions/usage, including energy consumers and the money system |
| 120 party focuses | Authoritative ruling-party slots 1/2/3/4/14, once-only reward flags, persistent earned variables, conditional programme activation, and starting initialization |
| 13 Article Nine focuses | Support initialization/campaigns, reachable 67-support threshold, repeated final guards, retained/replaced starting spirit, USA/SOV event scopes |
| 80 foreign focuses | 41 domestic programmes plus 39 offers, target eligibility, consent, costs, effects, opinion/idea durations, four recipient-selected construction projects and cumulative bonus expiry |

There are 40 recipient response events because Korean reconciliation sends
separate North and South Korean proposals. The independent review counted
80 direct accept/refuse options, 82 notice calls/providers, and 82 report
events. Each recipient event has exactly two direct options. Four project
completion notices remain in recipient country scope outside state/JAP scopes.

## Actual engine probe

`engine_runtime_probe.py` uses a separate user directory, the full mod
descriptor (including replace paths), a temporary addon and diagnostic logs.
The final machine-readable evidence is `ENGINE_VERIFIED_REPORT.json`.

The native game completed Seoul Claims Talks, delivered its recipient event
to KOR, executed the AI acceptance, and delivered Japan's reply with KOR as
FROM. It also exercised a real Hokkaido factory grant, negative-treasury
payment, repeat-payment protection, an LDP policy variable, and opening the
constitutional campaign. A separate fixture checks restoration of a completed
offer whose old dispatch receipt exists without recipient pending/resolved
state, and verifies that restoration itself has no payment.

Earlier diagnostic attempts are not successful campaign tests: two attempts
did not select their separate user directory; another lacked the base mod's
replace paths; an intermediate event snapshot had an option-nesting defect.
The final source and validator correct those problems. Temporary probe assets
are outside loaded mod directories and are never added to the user's playset.

## Limits

Source review covers all 425 focuses. The native probe covers representative
execution, not every possible 1970–1990 campaign, all 425 completed routes,
every party transition, long-duration expiry, or a live multiplayer session.
The native UI's hover presentation was not exercised in this audit.
