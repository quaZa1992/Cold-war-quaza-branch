IMPERIA COLD WAR

# Final mechanics review

Read-only review of `concept.json`, `CONCEPT.md`, and `preview.html` on 29 October 2026.

## Result

No concrete mechanics defects remain in the reviewed concept contracts.

- The JSON parses and contains 100 focuses. Party paths use the listed native Greek party triggers, keep party identity requirements explicit, and identify leader-specific programmes.
- The implementation contract now assigns dynamic programme modifiers and weekly streams to the governing party and, where applicable, the actual leader. Departure disables those streams; return rebuilds earned effects without replaying one-time assets or costs.
- Network preparation has a separate +10 receipt, 180-day expiry and cleanup on withdrawal, cancellation or coup resolution. Existing withdrawal remains -20 and removes the extra -10 only when its receipt is active.
- EEC association and accession use the live `EU_member` snapshot, exclude Greece as a sender, and price the weekly Greek expense as `0.00001 * Greek GDP * approved recipient count`. Six members are clearly labelled as the dated preview. The preview template shows both sides and their numeric effects; accession separately requires a native helper to enumerate current `EU_passed_votes` effects and revalidate changed terms.
- Cyprus settlement validity enumerates all six country pairs and requires peace plus native embargo and mirrored sanction checks in both directions. Community assent receipts remain distinct from Turkish government consent.
- The concept records removal of the erroneous inherited Greek membership through native cleanup, then clears only the artificial former-member and cooldown flags. Native membership is added on accession through `EU_member` itself.

The live native-law preview and proposed event/helper wiring are implementation requirements, not installed runtime behavior. Their absence from this design-only artifact is not a remaining concept defect.

## New direct-entry package

**Resolved in the latest concept build.** `gre_escalate` now describes a structured post-helper transaction with four conditions, separate issued/active receipts, once-only issuance, and the +0.005% weekly charge inside that transaction. The implementation contract now requires checking war state and funds before the attempt, then refunding the captured PP/GDP cost and reverting only this attempt's NATO changes if native entry fails. NATO restoration remains independently tied to both peace pairs. The exact army, navy, planning, amphibious, invasion-preparation and office-yield keys match the current crisis idea modifier set (`MECHANICS_REFERENCE.md`, native idea/effect citations in its “Native key boundary” and war API sections). This is an explicit implementation contract; it is not yet installed runtime behavior.

## Representative content and alternatives

The sampled descriptions use Greek institutions and economic conditions directly, and keep implementation details in the contract instead of the player-facing description. The policy rewards form meaningful choices: Republic trades 3% stability for political power and influence defence, while the parliamentary Crown trades political power for stability and naval organization (`CONCEPT.md`, “A Parliamentary Republic” / “A Crown Bound by Parliament”); industrial credit trades office yield for factory output and a factory, while visitor credit trades civilian construction for office yield and an office (`CONCEPT.md`, “Credit for Industry” / “Credit for the Visitor Economy”). The Greek Cyprus treaty and intervention choices likewise distinguish accepted constitutional influence from a costly, contingent coup route.

These match the inspected MD presentation examples: Israel's `ISR2_broad_coalition` versus `ISR2_working_majority` varies stability against political power with a distinct institutional choice (`common/national_focus/ISR70_focus.txt:149-200`); Russia's `COLDWAR_SOV_renew_the_cadres` versus `COLDWAR_SOV_respect_for_seniority` offers contrasting cadre renewal and seniority packages, including real political-balance and stability costs (`common/national_focus/COLDWAR_SOV_1970_focus.txt:280-364`). No concrete content or reward-bundle defect was found in the sampled Greek alternatives.
