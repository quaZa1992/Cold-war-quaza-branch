# Runtime presentation and parser acceptance

Use this reference when focus rewards disappear from unavailable paths or a player's screenshot/log contradicts a static report. The Syria 1970 repair is evidence for these checks, not a requirement to copy its whole architecture.

## Display rewards independently from their guarded execution

A focus tooltip evaluates conditional reward branches in the current country state. Wrapping every material reward inside an `if` for party, funds or completion can leave an unavailable focus showing only a fallback paragraph. Test the hover before prerequisites, under a different government, without funds, when available and after completion.

Where current MD and engine documentation support it, use an unconditional native `effect_tooltip` containing the truthful material preview and a separate `hidden_effect` containing the guarded, once-only payout. Native Germany focus examples use `effect_tooltip` with real building/temp-variable/helper bodies. Recheck that example in the active MD version. Preserve conditional wording for genuinely conditional outcomes; do not promise every mutually exclusive event option.

Validate display and execution as separate paths. A display-only block is not a second factory, treasury charge or modifier grant. Trace its helpers and compare amounts, scopes, costs, buildings, decision unlocks and events with the actual payout. Keep lifecycle flags, cache refreshes, logging and deferred-programme bookkeeping out of the material preview. A deferred implementation message must not replace the focus's real rewards. Structural entries should truthfully describe their downstream choices or decision unlocks rather than inventing bonuses.

## Show political requirements, hide technical plumbing

Keep scenario identity, original-tag and initialization predicates executable but hidden through the native trigger presentation mechanism supported by that context, such as `hidden_trigger`. Localize meaningful party, leader, coalition, funding, formation and reform requirements. Do not expose raw flags or generic 'game initially started' lines to explain a national policy. Hidden technical checks must remain in the execution gate; removing their display does not authorize removing the condition.

## Accept the engine's evidence

Check actual argument syntax and encoding in addition to vocabulary. In the Syrian log, scalar dynamic-modifier removal was rejected; the supported form was `remove_dynamic_modifier = { modifier = ID }`. Changed non-localization scripts also contained leading UTF-8 BOM bytes that the game rejected, preventing shared native party helpers from registering. Inspect raw bytes; a BOM-stripping text reader can conceal the defect. Keep localization's encoding convention separate and repair only files within the authorized change. Fix the generator so rebuilding cannot reintroduce the error.

An actual screenshot or engine parser error overrides earlier claims based on static checks. Retain that evidence, identify the primary error before following downstream unknown-helper messages, and rerun the relevant validator after the repair. Restart the game fully and inspect a fresh log when possible; explicitly report when fresh engine verification has not occurred.

## Write descriptions for players

Use specific historical institutions, policy choices and practical burdens in English descriptions. Keep the native numerical reward tooltip separate from narrative. Avoid repeated 'benefits and costs apply' boilerplate, raw script names, array indexes and generator explanations. Cross-check each narrative against the implemented outcome and the actual historical actor; do not improve prose by inventing a new mechanic.

## Local repair anchors to reconfirm

- `tools/syria_1970/validate_tooltips.py`: independently compares 420 emitted reward previews and guarded helpers, checks raw encoding and modifier-removal syntax, and verifies the eight outlook entries against approved source. Its country-specific counts are not universal requirements.
- `tools/syria_1970/presentation.py`: separates meaningful eligibility labels from hidden scenario identity.
- `tools/syria_1970/script_encoding.py`: bounded repair of changed files, not a repository-wide recoding recipe.
- Current MD `common/national_focus/05_germany.txt` and installed `effects_documentation.md`: native presentation and effect argument forms. Source paths/line numbers vary with version.

## Further engine evidence: decisions, events and generated lists

The next Syrian game run exposed these concrete cases. Reconfirm the native API in the installed version rather than treating static key coverage as an engine test.

- Native `custom_trigger_tooltip`/`custom_override_tooltip` implicitly requests `tooltip_key_NOT` in a negated context; the documented explicit alternative is `not_tooltip`. Check both forms, including nested NOT/OR. A positive key alone does not localize its inverse. Write a truthful inverse of the whole predicate: absence of a pending offer includes never-sent and expired offers and does not prove that a government answered. Negating only one clause of a funded-and-valid condition misstates its logic.
- Event title, description and option localization namespaces must be disjoint. Using `.d` for the description and the fourth lettered option overwrote one with the other. A safe convention is `.t`, `.d`, `.option_a` etc. Compare emitted keys, not just dictionary counts, and check every option against its own actual outcome. Cancellation should clearly say that nothing changes; it does not need a fabricated reward.
- Mandate/party-authority choices need not change the formal head of state. Do not call a destructive leader setter just to refresh policy flags. Preserve an unchanged incumbent; use a supported retirement/transfer API only for an actual replacement. Hiding a kill-and-recreate sequence fixes neither its historical meaning nor execution. Expose distinct party/leader programme ownership when that is the real choice.
- Clausewitz bare lists are data, not key assignments. The Syrian writer corrupted `generator = { 587 }` into `generator = { _bare = 587 }`. Parser sentinel names must never reach loaded script. Check raw output for `_bare`/`_list` assignments as well as round trips: a permissive AST can represent the sentinel assignment and a bare token identically, so round-trip equality alone can miss this defect. Validate argument shapes against the native effect documentation and actual engine errors.
- Follow the native budget path before adding affordability gates or custom debt. In this project, `modify_treasury_effect` permits a negative treasury and the existing budget tick runs `automated_debt_taker`. The user explicitly removed positive-cash gates from Syrian focuses while retaining their once-only expenditure. Do not charge the same shortfall directly as debt again. This focus-specific instruction does not remove a donor's or a bilateral contract's separate funding requirement.
- The user subsequently required material benefits for all Syrian entries previously rewarding only branch continuation or decision access. Record these authorized amendments separately from the original spatial design; give each an actual supported reward and plausible burden. Preserve earned rewards and geometry. This does not authorize arbitrary buffs to other countries or a tooltip pretending to grant a modifier.

A recorded engine access violation with an unsymbolized stack does not identify a script cause. Distinguish confirmed parser/UI/gameplay defects from an unproven crash hypothesis, retain the captured run, and require a fresh run before claiming the crash is resolved.
