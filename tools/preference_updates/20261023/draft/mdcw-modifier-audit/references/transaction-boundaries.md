# IMPERIA COLD WAR: stateful transaction and scenario audit lessons

Recheck providers in the current checkout. The original Vietnam lessons were exercised in focused script interpreters and source audits. The later Cuba examples also have bounded native transaction/event-arrival evidence; consult their current reports before claiming live coverage. The examples below are relative to TARGET_ROOT and optional when reviewing another project.

## Focus application and government return

Trace availability -> live application guard -> charge/reward -> success marker -> retry/cleanup. Establish the requested funding contract first: a Treasury cost is not inherently an affordability prerequisite. For newly authored Enes national focuses, use native cost deductions without introducing a hard Treasury gate by default; preserve an existing explicitly approved funding contract unless the user changes it. The UAE correction removed all focus funding gates, including hidden application/retry vetoes, while keeping full once-only native deductions. Decision/foreign-recipient affordability was not removed. Check negative-balance behavior in the live native cost/debt providers; the inspected `modify_treasury_effect` allows a negative balance, and the existing weekly debt system later services a shortfall. Do not invent automatic loans in the focus or claim that no borrowing occurs. Where affordability is required, exact equality with the required treasury amount should behave according to the approved contract; avoid arbitrary epsilon checks. Use the engine's actual comparison form, such as `check_variable` with `compare = greater_than_or_equals`, rather than assuming a general-purpose parser's operators are valid HOI4 syntax.

Review one-time initialization independently from one-time rewards. Programme synchronization should only maintain the appropriate active modifier set, retaining earned backing values when intended. Search for cash, construction, experience and other grants accidentally reachable from refresh. Test party/leader departure and return, repeated initialization, repeat callbacks and recovery-stage replacement.

When an earned provider is required, check the actual paired provider/government condition. When a focus can complete before implementation, distinguish its badge from its applied-reward flag and review downstream access. Retry is a design-specific recovery mechanism, not a reason to add fees or new policy systems.

## Recipient-owned agreements

Check sender identity and scope, recipient identity, current pending state, expiry, live eligibility, family limits and recipient existence again at acceptance; recheck payer funds where the approved contract requires affordability. `original_tag` can also match dynamic civil-war descendants; a response hardcoded to a fixed tag requires compatible sender gating or stored sender identity.

Prove who pays, who receives the outcome, and when the one-time marker is set. Refusal, silence, lost eligibility or failed funding must follow the stated contract. Clear pending/awaiting state deliberately and send truthful feedback. Delayed or duplicate events must not create a second debit/reward. If old and renewed offers can coexist, determine whether a response is tied to a distinct proposal or can validly accept the current identical proposal; do not claim stronger stale-offer isolation than the code provides.

Temporary offers/programmes must not be described as physical foreign aid unless a real native transfer/project occurs. Verify family exclusion at application, not just the button. Scope the recipient's consent to the outcome actually requested.

### Standing Cuban bilateral agreements

The approved Cuban model places concrete offers in separate national focuses and responses with the recipient RP country. Compare the real `country_event` destination, pending/offer state and actual arrival, not just the pending flag. Popup and decision responses must execute the same consent-guarded transaction. Show both countries' complete numeric prospective outcomes directly in focus/event/decision Effects, regardless of acceptance or current eligibility. Custom explanatory prose does not replace native effects.

For these standing agreements, both countries must exist and their paired spirits last indefinitely while at peace and free of mutual embargoes and all four Imperia sanction classes. Check each direction and mirrored incoming/outgoing storage. Both spirits suspend and resume together without replaying fees or assets. Check parent cancellation, country disappearance, asymmetric receipts and termination during suspension. A clickable cancellation that no-ops when a counterpart disappears is a defect. Third-country sanctions alone do not cancel the bilateral pact.

Dependent or member-only content, including a member-only entry focus, needs the actual active parent/membership spirit in availability, completion and recipient acceptance. Founding/admission stays reachable first. Preserve paid/grant receipts during suspension; resuming a parent must not replay child projects. Research source label, country, category, amount and uses must match across preview and the actual acceptance helper, with one localization key per label.

## Queued construction and startup feasibility

Distinguish `instant_build = no` construction, finished-building grants, offsite capacity, timed native investment and a policy modifier. A small planning contribution is not the full building price. Check current owner/control and building capacity before payment and again on a later retry. Read the building's actual `level_cap.shares_slots` definition; Vietnam uses `include_locked = no` for shared slots and omits it for non-shared buildings. Do not apply that field indiscriminately.

Enes explicitly requires one extra shared state building slot for every granted building level, before construction in the same state and same one-time guard. This includes infrastructure and province land/coastal forts even though forts do not consume shared slots. Do not remove these grants as supposedly redundant. Capacity is a separate native province/state check: verify owner/control, exact province, current cap and all granted levels. The inspected MD fort cap was 7, not a universal engine value. Native `any_province_building_level` requires `<` or `>` comparisons rather than an assumed `=`.

Recurring monetary costs use weekly MD units and budget literals have at most five fractional digits. Keep real gameplay requirements visible while hiding scenario/country/date routing and duplicate predecessor receipts. New player text contains no en/em dashes; native signed numeric formatting must display correctly.

A country with zero starting civilians needs a traceable source of construction capacity; the queue does not produce it. In the inspected project, native Economy -> Leasing offers paid offsite civilians, and recipient-approved foreign investment uses a separate timed project. Imperia Transfer Funds can finance agreed expenses. Trace recurring expenses, co-payments, influence and completion readers. Current active price arrays take precedence over stale comments. These are possible campaign routes, not guaranteed AI behavior or permission to add free factories.

## Observe a transition, not merely a state

A 'patron government fell' observer needs an accepted relationship and a recorded baseline: an already noncommunist patron is not evidence of a later communist collapse. Review disappearance, agreement expiry and actual government change as distinct causes. Stamp handled transitions to prevent recurring surprise penalties where a one-off shock was intended.

Check historical event windows against a fresh start, a tick at each boundary and a first tick after the window. Decide explicitly whether late saves receive retrospective events. War-pressure effects should follow actual war and peace, not a chapter title or scheduled declaration. Do not infer that a future crisis belongs among January 1970 starting spirits.

## Reproducible evidence and its limits

Useful scenarios include insufficient/exact funds; repeat application; loss of state control or slots; unimplemented prerequisites; provider/government mismatches; family conflicts; wrong recipient; refused/expired/duplicate acceptance; party return; leader-expiry gaps; delayed succession; and a patron noncommunist at acceptance. Select cases for the actual contract, not a fixed test quota.

A focused AST interpreter should fail on unsupported authored statements and disclose omitted native behavior. Assert integration ordering against real dispatchers when the model depends on it. Parsing all keys or reporting many checks does not prove engine loading, UI, economic formulas, queue timing, multiplayer synchronization or save migration.

Evidence: `tools/vietnam_1970/MECHANICS_REVIEW.md`, `test_transactions.py`, `test_politics.py`, `validation.json`; the real economic providers are under `common/scripted_guis/00_MD_economyview_scripted_guis.txt`, `common/scripted_effects/00_money_system.txt`, `99_investment_scripted_effects.txt`, and the current Imperia transfer-action file. Rediscover paths/values rather than copying snapshot line numbers.
