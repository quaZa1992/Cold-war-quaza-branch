IMPERIA COLD WAR

# France 1970 political tree implementation

The approved revision 4 is installed as `COLDWAR_FRA_1970_focus`: 234 focuses, twelve exact-party programmes plus shared republican institutions, 79 exclusive pairs, 48 armaments-industry focuses, 24 dedicated research-priority focuses and 24 voluntary bilateral offers. The 996 compatible route totals are preserved. Party programmes include their approved political, economic, armed-forces and foreign-policy branches.

`approved_design.json` is an immutable copy of the approved concept. SHA-256: `f90e6193464ffce880d3a6ba049568f779ccb0ab8111acb252c34118cdbdc780`. Its existing schema is preserved; this companion record identifies the project. No new branch, historical leader replacement, free equipment, forced alliance or automatic foreign-country reward was added.

The subsequent user-authorized compact lifecycle is recorded in `offer_policy.json`: existing agreement spirits have no fixed expiry, survive government changes and end on bilateral war or bilateral Imperia sanctions. It supersedes the annual/government-bound lifecycle in the frozen design and earlier offer review. Approved modifier values, setup costs and the eight finite research exchanges remain intact.

The whole-tree completeness audit is in `FULL_TREE_COVERAGE.md`: 34 political, 80 economic, 96 military and 24 foreign-policy focuses, covering every previewed focus in all twelve parties and the common institutions. The current effect presentation follows the user's explicit correction: native costs, signed modifier deltas, research/experience, spirit changes and decision unlocks only. Explanatory effect paragraphs about ownership, consent or internal handling have been removed. The durable rule is recorded in the root `AGENTS.md`.

Foreign focuses show their actual unlocked decision using `unlock_decision_tooltip`. Decisions show native prospective terms with MD's standard conditional heading. Recipient acceptance options show native numeric effects; real guarded acceptance and its internal receipts run separately in `hidden_effect`. Non-executing previews are compared against the actual charged/granted effects for both countries. `BARE_EFFECTS_REVIEW.md` records an independent review against native France MD examples. This supersedes older reports describing prose agreement summaries.

## Runtime behavior

- The France history and legacy fallback select the authored tree in a campaign whose start date is 1 January 1970. The predicate uses the campaign start date, so the tree remains active after 1985. Other start dates retain their existing routing. Pompidou and the existing party/leader system are retained.
- Shared institutions endure. Every party branch remains visible and inspectable, including parties outside government. Availability, guarded completion and programme activation use exact native `ruling_party` indices. Slot 20 has separate CID and FN ledgers, divided at 5 October 1972. Party-dependent `allow_branch` gates have been removed following the user's correction. A one-time layout refresh clears the former hiding state without reloading the tree or resetting focus receipts. Thirteen shortcuts support navigation across the approved positions.
- Programme dynamic modifiers have government `enable` gates. Refresh also removes inactive programmes and reconstructs the current government's totals from permanent earned receipts. Exact-subparty callbacks, government on-actions and a daily France fallback run refresh. A return to office restores policies without repeating PP charges, experience, stability grants or research bonuses.
- Three starting spirits are granted once: Presidential Republic, Unsettled Social Compromise and Uneven Modernisation. Approved reforms conditionally replace or remove the two historical difficulties. Removed spirits are not re-created on daily initialization.
- Narrow research rewards use the actual MD technology IDs for the active DLC configuration. Required design projects and unresearched-target guards apply to availability and execution. Awards give one 50% use on one listed eligible target, without completing the technology or its design project.
- Offers require recipient-owned acceptance. The 16 compact spirits last indefinitely; eight exchanges grant finite research. Costs are rechecked for both countries before acceptance. No charge or treaty reward occurs when merely completing the focus or sending a proposal. France can maintain one compact. Accepted compacts survive government changes. Either signatory may withdraw; bilateral war, any bilateral Imperia diplomatic/financial/economic/military sanction, loss of sovereignty, missing signatories or a missing matching spirit terminates both halves. War/sanctions against third countries do not end the compact. Ending a war or lifting sanctions does not automatically restore an agreement: a new proposal and consent are required. Research receipts persist across government changes and cleanup. Quoted proposals still expire after 90 days and reject changed government snapshots before acceptance.
- Compact maintenance scopes directly to the saved counterpart, runs from the existing daily France update and government callbacks, and never scans world countries. Eight local sanctions-array memberships cover both directions of all four supported sanctions types. This establishes bounded source work, not an observed FPS or multiplayer timing benchmark. Termination is guaranteed only by the source contract at the next maintenance tick; engine timing remains untested. A one-time refresh converts an existing accepted annual idea into an untimed idea on both sides without reapplying setup charges or research rewards. Native cancellation guards prevent orphan spirits from remaining valid after their recorded relationship is gone.
- Monetary setup charges use MD treasury effects. Recurring modifier costs apply to MD's weekly expenditure bases. Land-equipment upkeep is not procurement price or aircraft/naval upkeep.

## Files and reproducibility

Core runtime files use `COLDWAR_FRA_1970*` in national focuses, ideas, dynamic modifiers, scripted effects/triggers, on-actions, interface and English localisation. Offers have separate decision, category, event, treaty-idea and scripted-effect files. `INTEGRATION_HOOKS.md` identifies the three narrowly edited shared/history files.

Run, in order, from the mod root:

```text
python tools/france_1970/build_offers.py
python tools/france_1970/compile.py
python tools/france_1970/validate.py
python tools/france_1970/test_programmes.py
python tools/france_1970/test_offers.py
```

`VALIDATION.json` records emitted-source consistency, graph coordinates, AND/OR prerequisites, reciprocal exclusions, research references, sprite/idea references, exact modifier contributions, route sums and encodings. `PROGRAMME_TESTS.json` records execution of the emitted AST in a bounded source model: all focuses in two DLC configurations, repeated completion, wrong governments, excluded alternatives, exhausted research, missing design projects, all 996 routes through government loss/return, one-time spirit initialization and CID/FN identity separation. These are source checks, not an HOI4 engine simulation.

`OFFER_TESTS.json` records focused emitted-AST lifecycle tests for all 16 compacts: indefinite persistence, government changes, sanctions in both directions, bilateral war, unrelated third-country sanctions, withdrawal identity, missing counterparts, annual-idea migration, pending expiry and durable finite research receipts. It also exercises exact affordability for fractional Political Power balances. These model tests do not measure game performance.

The existing interactive inspector has been synchronized with all installed focus IDs and current agreement lifecycles. `sync_preview.py` updates its embedded data without invoking archived concept generators. `check_preview.cjs` exercises all 234 focus selections, all 13 groups, all 288 prerequisite links, effect-only content and responsive widths; `PREVIEW_TESTS.json` records the results. `PREVIEW_SYNC.json` records the inspected file hash. This is a source reconstruction rather than a native HOI4 screenshot.

Independent reviews are in `CORE_REVIEW.md`, `OFFERS_REVIEW.md`, `PERMANENT_COMPACTS_REVIEW.md` and `ICON_REVIEW.md`. The permanent-compacts review supersedes the original annual/government-bound contract in `OFFERS_REVIEW.md`. Historical and mechanic evidence is retained in `HISTORICAL_PRECEDENTS.md`, `HISTORY_SOURCES.json`, `MECHANICS_EVIDENCE.md`, `RESEARCH_EVIDENCE.md`, `RESEARCH_SOURCES.json` and `MODIFIER_PROVIDERS.json`. Design-stage reports describe the earlier concept and must not be read as runtime certificates.

## Verification limits

No running HOI4 load, native hover, save/reload or multiplayer timing test was performed. Use a new 1970 campaign to inspect the history-selected tree. Save migration from an already-running campaign is not implemented as a separate feature. Native branch refresh/scroll behavior and simultaneous multiplayer event handling remain engine checks. Government callbacks plus party snapshots do not establish detection of every same-party character replacement. All selected focus masks and texture files resolve; the stock game's shine overlay follows the existing MD path but is unavailable for direct inspection in this checkout.

## Provenance

The gameplay source is the user's approved France concept, generated during this project. Historical precedents retain their original source links and distinguish documented policy from proposed alternate-history programmes. Engine/API conventions are adapted from installed Millennium Dawn, including France/Russia examples and the existing Cold War national-tree implementation patterns. Existing shared-file upstream credits remain intact.

The 35 selected focus textures are reused from this checkout's `gfx/interface/goals/coldwar` and `coldwar/fracoop` directories; 37 aliases and their native shine pairs are registered without editing artwork. Starting/programme spirits use existing small MD idea textures. Original individual artwork authors and redistribution licences are unknown in the available checkout; the project marker establishes neither ownership nor a new licence. See `ICON_REVIEW.md` and `IMPERIA_COLD_WAR_NOTICE.md`.
