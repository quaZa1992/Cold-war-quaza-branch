# Iraq runtime activation audit

Audited 18 October 2026 after the reported in-game absence of starting spirits
and focus modifiers. This is a source/native-provider audit, not an observed
successful game session.

## Confirmed activation and presentation gaps

The original `history/countries/IRQ - Iraq.txt` 1970 block loaded the authored
tree and political profile but did not seed its seven starting challenge cards
or call `COLDWAR_IRQ_initialize`. Their attachment existed only in
`common/on_actions/COLDWAR_IRQ_1970_on_actions.txt` through new-game
`on_startup`, plus the country-scoped daily fallback. Country-selection preview
therefore had no direct historical attachment route. This proves a preview
omission; it does not prove the same callback failed after Play.

All original starting challenges except literacy used variable-backed dynamic
modifiers. Their enable conditions depended on `COLDWAR_IRQ_campaign_active`,
which includes `exists` and the selected game's `has_start_date`. Source does
not establish that those are finalized in every pre-Play preview context, or
that the preview lists dynamic modifiers alongside ordinary ideas. Ordinary
staged ideas seeded directly in the dated history remove those dependencies
for the seven starting cards without changing their approved values.

The generic focus-eligibility sentence was authored localization, rather than
a missing localization key. A single `custom_trigger_tooltip` hid its real
conditions under `hidden_trigger`. Seeing that sentence alone does not prove
that programme delivery or the scenario condition executed.

## Native API checks

* `on_startup` and `on_daily` are present in native MD's
  `common/on_actions/00_on_actions.txt` at the audited lines 1714 and 86.
  Native daily code invokes country-only helpers and `is_ai` directly, matching
  the Iraqi daily country scope. Startup explicitly enters `IRQ`; the Soviet
  provider documents the same need to enter a country from the global callback.
* Local engine `documentation/triggers_documentation.md` explicitly supports
  `exists = yes` in a country scope, `is_dynamic_country`, `hidden_trigger`,
  and `has_start_date`. No unsupported trigger was found in the original
  campaign gate.
* Local engine `documentation/effects_documentation.md` documents
  `custom_effect_tooltip` and `add_dynamic_modifier`. The installed main MD
  `history/countries/IRQ - Iraq.txt` seeds ordinary ideas directly around line
  358 and an Iraqi dynamic modifier around line 400. History-level effects are
  native; actual new-card rendering still requires an engine check.
* MD's `common/on_actions/MD_on_actions.txt` explicitly documents that startup
  does not refire for saves already in progress. No `on_load` callback was
  established from the local native documentation. Existing-save recovery must
  use a real callback such as the first daily tick, without promising immediate
  changes while a loaded save remains paused.

## Recommended implementation contract

Root owns the static stage conversion and native history integration. Keep the
same seven historical challenges and approved modifier amounts. Remove all six
legacy starting dynamic modifiers before attaching each current static stage;
disable their retained definitions for old saved IDs. Use one current static
stage per burden. Keep the 23 earned government programmes dynamic, including
their current-party/leader/contract conditions. Literacy remains in native
education; its challenge marker must not duplicate education's modifiers.

Seed the initial stages directly from the existing IRQ 1970 history block, with
the existing later-start exclusion. Startup/daily reconciliation then advances
or removes stages from actual delivered reforms and current agreements. Do not
reset literacy, treasury, debt, resources or completed investments on reload.

`startup_patch.py` supplies the isolated metadata recovery effect
`COLDWAR_IRQ_repair_completed_focus_metadata`, to run inside the genuine
1970-country startup/daily route before programme reconciliation. It restores
programme/unlock metadata only from an existing successful `_implemented`
receipt. A native-completed but undelivered focus becomes pending; it is not
given free programme benefits or physical rewards. Existing positive invoices
are retained, no historical GDP quote is fabricated, and paid later policy
selections are preserved. The recovery never calls a focus `apply` helper or
replays treasury, debt, building, resource, literacy or technology effects.

## Why earlier tests passed

`test_usa_module.py` replaces the real campaign gate with a tag-only model at
the audited line 84. `test_core.py` models dynamic attachment as Python set
insertion around line 60 and stubs native refresh around line 62. Those tests
establish authored transaction and cache behavior under assumed activation;
they do not load dated country history, execute the engine's callback scheduler
or render a national-spirit list. Their passing result cannot establish preview,
startup, dynamic-modifier display or save-loading behavior.

The new bounded metadata recovery AST suite passes ten scenarios: actual
receipt recovery, repeat idempotence, preserved pending/frozen invoices, no
fabricated invoice, review-package distinction, unique policy reconstruction,
preserved revised policy, ambiguous excluded-completion handling, actor gate,
and absence of physical/financial replay.

## Remaining engine checks

Subsequent native-engine evidence: `ENGINE_RUNTIME_REPORT.json` now records a
successful actual January1970 startup with the final manifest
`64140bdb6bd66e6ddd4c6927f1eb2da96d6aff3d52092549f5abafcde8382594`
unchanged. All seven ordinary starting cards were present. Completing
`COLDWAR_IRQ_regional_command` awarded its implemented/earned receipts,
the Baath programme and the approved0.04 political-power value. The real MD
party-change effect removed that programme and July State on departure;
return restored the programme at0.04 after repeated reconciliation. Five
native checkpoints passed; no Iraq/USA module error lines were recorded.
The test addon existed only in the isolated test profile. This verifies
representative activation and cleanup, not UI hover or a full playthrough.

Verify seven cards before Play; verify their exact amounts after a fresh 1970
start; complete one free and one funded focus and inspect the resulting native
programme and account changes; switch the exact subparty and restore it; load
an existing 1970 save and advance one day to verify metadata recovery without
duplicate assets. Confirm later starts receive none of the 1970 seed. Current
22:33 error-log searches found no `COLDWAR_IRQ` parser error, which is useful
negative evidence but does not establish runtime success.
