# Lessons from the North Vietnam implementation

This is a source-level case study, not an engine-tested template. Inspect current files before reuse. Paths are relative to TARGET_ROOT; absent project examples are optional evidence, not dependencies supplied by this skill. Vietnam's 239 focuses, 48 decisions, six starting spirit families, dates and numerical rewards are country-specific.

## Preserve the approval baseline and source ownership

Keep a machine-readable approved design snapshot and its hash when translating an approved concept. Compare installed focus IDs, resolved positions, grouped prerequisites, exclusions, titles, costs and raw reward payloads against that baseline. Keep final narrative prose and runtime implementation separate when the approved snapshot must remain immutable. Old concept-only metadata does not establish that implementation is absent; inspect loaded files.

A manifest should distinguish generated outputs, narrow shared-file integrations, hand-authored providers and art/provenance. A compiler must not overwrite manual political providers or regenerate unrelated countries. After meaningful compiler changes, a second build can check byte stability and preservation of manually maintained files. This proves reproducibility, not in-game reward idempotence; verify both separately.

Example: `tools/vietnam_1970/approved_design.json`, `compile.py`, `flavour.py`, `manifest.json`, `rebuild_check.json` and `README.md`.

## Integrate the tree and the authoritative political system

A country-history `load_focus_tree` is only one entry point. Inspect startup/fallback dispatchers so an old generic-tree call cannot replace the new tree or reset its progress. Use the actual persistent scenario predicate: current calendar year alone must not switch off a 1970 campaign's programmes in the 1980s. Preserve later starts and define behavior for dynamic/civil-war countries explicitly.

An MD subparty can change without changing the broad outlook. Wire programme synchronization into the actual native subparty callback and leader installation path; broad government hooks alone may miss it. Use the existing party/retirement/provider system rather than a second leadership menu.

Leadership succession must tolerate the outgoing leader disappearing before the next appointment. Synchronize recognized current incumbency, retain persistent memory when expiry leaves no recognized leader, and evaluate the latest due successor first on delayed catch-up. Do not resurrect a deceased predecessor or install and remove several intermediate leaders on one late tick. Respect actual player choices and distinguish explicit retirement from party return or routine refresh. If the native dispatcher removes the old leader before the country provider runs, record incumbency before that removal. Test `do_not_retire`, death gaps, delayed ticks and return to power.

Example: `common/scripted_effects/COLDWAR_VIE_1970_politics.txt`, the narrow `VIE_political_leaders.txt` delegation, and `tools/vietnam_1970/POLITICS.md` / `test_politics.py`. Vietnam's succession dates and remembered ordinal are examples, not universal roster rules.

## Separate earned state, active authority and transactions

Classify each benefit as durable national development, an earned party programme, an exact leader's programme, a temporary funded action or a one-time transaction. For retained programmes, remove/deactivate the live modifier on departure while keeping earned values. Synchronization may restore the modifier; it must not execute the original reward again. Recovery stages should replace earlier stages monotonically rather than stack or regress.

Where the approved contract requires affordability, check the live funds/authority/territory/capacity again inside the application helper, not only focus availability. Apply the cost and reward once, then stamp success. If implementation fails after completion, an authorized deferred retry can call the same helper; do not silently charge for failure or add a new refund economy. For this design, implemented-parent flags prevent an unpaid completed badge from unlocking downstream rewards. Such additional eligibility guards must be documented and checked against the approved contract rather than automatically added to every tree.

For shared decisions, preserve pairs: `(earned provider A AND A's current authority) OR (earned provider B AND B's current authority)`. A shared unlock flag combined with an unrelated active government can grant unearned access. A one-per-family limit belongs in execution as well as availability. A cancelled paid timed action does not automatically become a free entitlement on government return.

Example: `COLDWAR_VIE_1970_effects.txt`, `COLDWAR_VIE_1970_triggers.txt` and `tools/vietnam_1970/test_transactions.py`. Use `$mdcw-modifier-audit` for detailed transactional checks.

## Historical identities and realistic constraints

Distinguish real historical allied parties from proposed independent governing transformations. A former administrator's alternative party-chief mandate is not a historical incumbency. For proposed collective governments, use institutional identity rather than assigning a real person an invented coup. Verify actual party-name/localization consumers: adding names without registry routing may leave modern names visible. Preserve other countries and later-start fallbacks.

Trace a viable route through a difficult starting economy. A queued factory is not construction capacity. Existing paid leasing, recipient-approved native investment or agreed transfers may provide a route; inspect their actual costs and restrictions. Do not grant unsolicited start industry, GDP, armies or equipment to make a focus tree easier. Keep the historical constraint and explain the playable native route.

Use identified historical portraits with source/processing provenance. Distinguish an unmodified photograph, normalized image and identity-preserving derived portrait. Reuse existing correct people and use institutional emblems where no individual is intended; valid sprite paths alone do not establish identity.
