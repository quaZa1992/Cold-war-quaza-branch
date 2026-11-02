# IMPERIA COLD WAR: Israel legacy callback isolation

`runtime_legacy.build()` freshly reads the existing event, project-start and occupation sources and returns five texts to the root compiler. It performs no game-file writes. The original project markers, generator attribution and surrounding source remain present. The root writer must preserve the returned UTF-8 text without newline translation.

The patch protects 76 retired Israel events at registration, option availability and the actual executable bodies. This includes 72 option bodies and 43 immediate callbacks. Trigger rejection is therefore not the only protection: already opened or forced old callbacks cannot execute their old rewards, payments, population transfers, diplomatic actions or political changes once actual ISR has `ISR2_enabled`.

The permanent global marker `ISR2_legacy_replaced`, set by the root initialization, is the primary retirement record. Annexation or loss of the old country flag cannot reactivate foreign-country callbacks. The actual-ISR flag remains a compatibility fallback for earlier private test builds. Existing actor-only patches are upgraded without adding repeated guard layers. Refunds remain strictly scoped to the actual enabled ISR country.

The 33 visible retired events gain one effect-free closing option, available only after the replacement module is enabled. Original options are then unavailable. No new policy menu or gameplay decision is introduced.

Egypt's independent `ISR70P.1160` canal-reopening event is exempt. Its entire event block, including existing triggers and its own completion/refund behavior, remains byte-for-byte identical. No Egyptian funding variable is part of the Israeli refund inventory.

Four old occupation-local dynamic modifiers remain loaded compatibility providers. Their known invalid root-level state predicates are now inside absolute state wrappers for 208, 209, 213 and 587. The owning `state_gate` expression in `tools/israel_1970/occupation_profiles.py` receives the same fix. All modifier values, other definitions and remaining template code are unchanged.

The refund provider derives 40 known `paid`/`active`/`done` reservation records from the actual callbacks and verifies their corresponding paid start transactions. It refunds only a positive stored amount belonging to an active, unfinished ISR project. It never recalculates a price from current GDP. Completed projects, zero or negative balances, and balances without the corroborating active receipt are not refunded or erased. Finished assets are neither removed nor reissued.

The claim is cleared before native payment, preventing replay through a fiscal refresh. While `MD_skip_treasury_cost` is active, the provider performs no mutation, retaining the amount and active receipt for a later actual payment. New campaigns without old reservations receive nothing. The helper is actual-ISR-only and can be called from initialization and refresh without advancing time.

This is reservation accounting and callback retirement, not a focus-progress or general legacy-save migration. Uncorroborated stale balances are retained for inspection rather than converted into speculative refunds.

## Verification

`python tools/israel_v2/test_runtime_legacy.py` passed ten tests. They parse the emitted native AST and bypass registration and option triggers to force every retired executable body in five country scopes. No old effect executes. Additional checks cover all 40 exact stored refunds, replay, finished/unpaid/orphan cases, treasury-skip deferral, other-country exclusion, the effect-free closing option, the unchanged Egyptian exception and freshly read patch idempotence. Global retirement is tested after Israeli annexation and actor-flag removal. Occupation tests verify explicit state scope, unchanged modifier values and unchanged template AST outside `state_gate`. Payment tests use the currently loaded native `modify_treasury_effect` definition. The canal world's independent implementation is a fixture in the bounded callback model; its full unchanged event block is also compared directly.

These are source and model results, not observed HOI4 event arrival, save loading or multiplayer evidence. The root integration remains responsible for file output and native verification.

Provenance: original patch and tests by Codex for IMPERIA COLD WAR. Existing event bodies and project declarations come from the repository's prior Israel compiler. Current MD budget effects supply the native monetary provider. Existing credits and licences remain applicable; individual original author or separate permission information is unknown where inherited records do not identify it. No third-party art is changed.
