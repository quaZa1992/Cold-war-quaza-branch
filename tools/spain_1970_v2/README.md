# IMPERIA CW — Cold War: Spain 1970–1990s

The owner approved the interactive 231-focus concept on 21 October 2026 and then authorised implementation. `approved_design.json` is immutable; SHA-256: `2b1868c55a00539b99c6236483f36c2a03870ab03211f4cc8bc4b5ac3efc5ff3`.

## Build and ownership

Run from the mod root:

```powershell
python tools/spain_1970_v2/compile.py
python tools/spain_1970_v2/validate.py
python tools/spain_1970_v2/test_core.py
python tools/spain_1970_v2/politics_test.py
python tools/spain_1970_v2/test_agreements.py
python tools/spain_1970_v2/review_emitted.py
```

`compile.py --stage <directory>` creates an isolated output mirror. Its scoped providers read the existing shared native contracts; the agreements provider also maintains its marked, Spain-only NATO event guards. Do not run a broad country or party generator to rebuild this tree.

The compiler owns the focus tree, core transactions, seven initial spirit families, their eight recovery stages, accession receipt, thirteen aggregate programmes and their English localisation/art declarations. `politics.py` owns the authoritative succession, native leader/party integration and constitutional process. `agreements.py` owns funded decisions, crises, investment and recipient-controlled diplomacy. Provider modules return exact output mappings; `manifest.json` records their hashes. Source scripts/GFX are UTF-8 without BOM; localisation alone uses a single UTF-8 BOM.

`integrate.py` maintains narrow historical-party display and bookmark hooks and retires only the snapshotted, wholly custom former Spain providers. It preserves the colour files, historical roster/party registry, native `99_SPR*` files and later MD history. Its registry branches are explicitly retained by the existing shared party-registry generator. Old `tools/spain_1970/{compile,rebuild}.py` entry points redirect to this compiler. The rejected design/provider snapshot is archived outside the loaded mod; `retired_snapshot.json` and `retirement.json` record its removal.

## Runtime contracts

- The tree applies to the real SPR tag in the persistent 1970 campaign. The native generic-tree exemption and dated history loader remain in place. No alternate starting units, equipment, research or map ownership is granted.
- Programme rewards follow the actual MD subparty. UCD and AP/PP share slot 1 but use the native cabinet's recorded mandate. Earned modifiers rest on departure and return with that mandate; cash, buildings, XP and research never replay.
- Permanent institutional gains, current constitutional terms, Carlist cabinet agreements, Franco-only authority and NATO/EC obligations have separate activation conditions. Legal labour packages replace rather than stack. The programme reconciler changes modifiers only.
- Franco starts active, with declining governing capacity. Preparation improves the handover rather than health. The later illness and bounded 1975 departure replace the old observer; ordinary refresh cannot retire him, native retirement can, and expiry gaps cannot resurrect him. The historical native leader system remains authoritative.
- The approved focus funding contract checks live affordability, state ownership/control and per-building headroom at completion. Shared-slot grants precede instant construction. A completed but never delivered transaction retries without an extra fee when eligible; its once-only receipt prevents repeated rewards. Hidden predecessor receipts preserve graph logic without extra tooltip clutter.
- Education invokes the actual native law helper only below its maximum, excluding its endpoint PP fallback. Research/doctrine rewards use real named categories and limited uses.
- Treaty rewards show prospective native numeric effects even before acceptance. Payments and benefits require the actual accepting government, live funds, eligibility and pending state. Silence/refusal pays nothing. Identical renewed offers may answer the current identical pending terms; immutable event-local nonces are not claimed.
- Uranium remains a surveyed opportunity with no automatic mine or raw production. Energy construction is the existing funded MD investment system. All recurring budget multipliers feed native weekly costs; one-off money is in native treasury billions.

## Implementation adaptations

The concept audit had missed the existing Cold War mode of MD's EC system. Implementation uses its actual candidate/admission route and member assent instead of a parallel organisation. The Spanish accession receipt follows real `EU_member` status, consent and legal adjustment. Member-only rewards require both that receipt and current native membership in availability, execution and ongoing activation. NATO uses its native leader/applicant consent chain with narrow SPR-only stale-acceptance guards.

The territorial entry's approved `root` field was null because it already depended on the common trunk. The compiler uses its existing zero-offset focus as the relative anchor; every approved position, prerequisite group, icon, title and description remains identical. Sahara offers are diplomatic protocols and reviewed cooperation, with no forced foreign transfer or starting-map change.

## Verification and limits

`review_emitted_report.json` independently reconstructs all installed focus coordinates and grouped prerequisites and compares rewards/localisation to approval. All 231 match. The native preview's geometry, bitmap-title widths and artwork remain representative because those fields were preserved; idea art was additionally inspected from the actual `gfx/interface/ideas/` textures.

`core_tests.json` covers 35 asset transactions, exact/low funds, control/headroom failures, once-only delivery, government departure/return, mandate isolation, legal replacement, membership loss (including stale EC receipt), education maximum and deferred delivery. `politics_tests.json` covers 17 political lifecycle classes, including expiry/retirement, delayed events, rejected reform and actual election/coalition completion. `agreements_tests.json` covers 33 transaction boundary cases. The test interpreters read emitted scripts, fail on unsupported authored commands and document their native-model boundaries.

Independent reviews are recorded in `politics_independent_review.*`, `core_tests.json`, `review_*`, `politics_reference.json` and `agreements_native_contracts.md`. `validation.json` checks loaded provider closure, duplicate aliases, encoding, fixed-point precision and retired files. A second build checks byte stability; it does not substitute for runtime idempotence fixtures.

No HOI4 engine session was run. Native hovers, event scope/UI behaviour, saving/reloading and multiplayer synchronisation remain engine checks. This is a replacement tree intended for a fresh January 1970 campaign; no migration of rejected-tree focus progress is claimed.
