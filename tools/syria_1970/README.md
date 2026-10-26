# COLDWAR_SYR: Syria, January 1970–1990

## Current focus-owned rewards revision — 21 October 2026

The current user-authorized streamlining replaces most domestic confirmation
menus with direct focus outcomes. There are now 27 Syrian decisions, two foreign
withdrawal controls, 28 visible events and 16 hidden expiry/crisis callbacks.
All 420 focus positions, prerequisite groups, exclusions and durations are
preserved; 25 modifier bundles are deliberately revised. The counts and earlier
contracts below describe the prior imported revision where superseded.

`streamlining_build.py` generates into an isolated temporary country tree and
installs only Syria-owned outputs. `build_content.py` now delegates to that
installer; it does not rerun shared integration or modern-content retirement.
`streamlining.py` owns the conversion, saved-variable deltas and preserved consent
boundaries. `streamlining_rewards.json` declares 22 of the revised reward bundles;
three standing Golan services replace the former short-lived preparation clicks.

Current verification: `test_streamlining.py --installed`, `validate_content.py`,
`validate_tooltips.py`, and `verify_streamlined_preview.cjs <absolute-html-path>`.
See [the revision report](../../docs/syria_1970_streamlining_20261021/CHANGES.md)
for exact changes and testing limits. Older snapshot-specific tests remain
provenance and are not evidence for this revision's deleted event/decision IDs.

## IMPERIA CW selective import

Imported from quaZa's `quaza/projektdateien-2026-10-20` branch at
`e45483ffc603835c8f44db1e2f9975cbc13fba85` on 21 October 2026.
This integration retains native MD providers and later-start content, with
1970-specific dispatch and scenario guards. The normal compiler therefore does
not run the upstream `retire_modern` deletion migrations. The seven extracted
legacy-provider files are archived under `imported_shared_legacy/` instead of
being loaded a second time alongside their original native definitions.

The retirement reports and `validate_retirement.py` below describe the upstream
retirement mode. They are retained as provenance, not as evidence for this
coexistence integration. Current import checks are recorded under
`docs/quaza_country_import_20261021/`.

Country-only output writers preserve the `IMPERIA CW — Cold War` headers.
No whole-mod generator is required merely to install these imported files.

The approved 420-focus design is implemented in the loaded mod. Its 38 sections
retain the approved coordinates, prerequisite groups, exclusive choices and native
MD art. All new localization is English. The original approved input is
`design_source.json`; `manifest.json` records the installed amendments.

Later user instructions amend the original concept:

- Paid focus treasury costs are **$2.000–$7.000 billion**, according to project
  size. Free focuses remain free. Decision costs and percentage-of-GDP operational
  appropriations retain their separate schedules. Focus duration and political
  power prices were not multiplied.
- Focus affordability requirements are removed. Native MD treasury expenditure
  may become negative and the existing budget system finances the deficit as debt.
  The focus still pays its full cost once. Donor/contract/decision funding guards
  retain their separate meaning and are not removed by this focus-only change.
- All 29 entries formerly rewarding only continuation or decisions now also grant
  a thematic domestic modifier with a real continuing expense or disadvantage.
  `runtime_policy.json` and `additional_entry_rewards.json` record the amendments.
- The dedicated modern Syrian programme has been retired. Original files are
  recoverable under `retired_modern/`, which HOI4 does not load.

## Installed content

- 420 focuses, 38 sections, 110 reused focus icons and 467 prerequisite edges.
- 56 approved decisions plus 11 concrete formation, leadership and retry
  decisions; two additional controls let Lebanon and Iraq end their agreements.
- 66 new country events. Three older shared events remain only because foreign
  content calls them; they are not Syrian 2000 succession events.
- 38 earned programme modifiers and seven staged starting-problem modifiers.
  The 784 original programme-stat grants retain their values; 58 new grants give
  the 29 amended entries benefits and corresponding burdens, for 842 total.
- Separate timed operational packages, domestic burdens and consent-based
  diplomatic contracts. Native MD and Imperia readers consume their real effects.

The opening preserves Nureddin al-Atassi as formal president. Salah Jadid's
programme represents dominant party authority, not a false presidential title.
The officer bargain and cabinet settlement determine whether the Corrective
Movement can succeed; there is no automatic November coup. Ahmad al-Khatib's
transitional stewardship, an institutional civilian council and actual Hafez
accession are distinct outcomes. Rifaat requires the later incapacity and rival
guard crisis. The later council does not resurrect al-Khatib.

Party and leader programmes cover the Syrian Ba'ath; Communist and independent
left alternatives; Arab Socialist Union; conservative and civic constitutional
parties; SSNP; Iraqi-aligned Ba'ath; Muslim Brotherhood; and a provisional military
council. Darwish and Badr represent negotiated Kurdish coalition programmes rather
than being installed as national presidents. Later party splits have real
formation decisions and dates. No modern HTS, ISIS, FSA or Assad-family 2000
succession path is introduced into this tree.

The optional outlook campaigning branches select actual legal MD subparties.
They are not prerequisite ceremonies for an already-governing party. Political
legality, elections and cabinet coalitions use MD's existing arrays and helpers.
The initial subparty percentages are scenario balance estimates, not historical
polling figures. Unsupported slots start banned; alternative legal government
requires an accepted political pact and the existing political system.

## Programme lifecycle and implementation

Every focus now has an unconditional native `effect_tooltip` for its material
rewards, separate from the hidden guarded payout. Locked party paths retain their
intended reward preview. Every formerly empty entry has a material reward;
branch-opening placeholder text has been removed. Outlook entries show their
real decision unlocks alongside their new institutional benefits and costs.
Neither display-only effects nor returning governments replay one-time grants.

Each material focus calls its own guarded `_implement` effect. An
`<focus>_implemented` signature prevents repeated cash, construction, taxes,
events and programme grants. If authority or building access changes at
completion, the signed programme remains pending. Its normally hidden resumption
decision rechecks the original conditions and executes the same once-only helper.
It cannot spend money or give a factory twice. Follow-up decisions require actual
implementation, not merely a completed but unimplemented focus.

National development persists. Party programmes require the exact ruling
subparty; leadership programmes require both that party and the office-holder
flag. They detach when authority changes while their earned variables are kept.
Returning authority restores those variables without replaying one-time rewards.
Coalition rights programmes additionally require a valid current cabinet compact.
Leader installation and same-outlook party changes refresh these attachments;
weekly refresh is a backup. No budget week is settled during programme refresh.

The seven starting problems are Divided Ba'ath Command; Permanent Emergency;
Defeat of 1967; Uneven Development and Skilled-Labour Shortages; State-Sector
Strain; Rainfall-Sensitive Agriculture; and the Citizenship Census. Reforms remove
specific components. Independent education/construction and two administrative
stages commute and do not erase unfinished reforms. Command unity requires both
a genuine agreement and its implementation, or an actual civilian constitutional
transition. Ending emergency powers also removes their stability benefit.

Tabqa uses state **994** and native `renewable_energy_infra`; it requires funded
resettlement. Water-management improvement requires three paid trials. Latakia
naval-base work uses province **1088** and checks the native level cap. Construction
rechecks control and capacity, refreshes state/GDP caches and recalculates energy
only when that system is initialized. It does not grant invented GDP tiers.

## Limited war and foreign consent

`COLDWAR_SYR_levant_02` creates a real 365-day goal against Israel at peace while
Israel controls the Golan. If Israel owns state 587 it uses `take_state_focus`.
If Israel only occupies Syrian-owned Golan, the supported engine fallback is
`annex_everything`; the broader peace-conference scope is explicitly disclosed.
No focus automatically declares war or forces coalition peace.

The actual 1970 setup already places Syria in the War of Attrition. In that
case the route opens operational preparation and a funded post-armistice goal
decision. Appropriation, cabinet authorization, the paid operational window and
doctrine choice are separate steps. Timed benefits and their personnel, supply,
medical or administration burdens expire together. Demobilization retains real
loan debt and earned professional learning.

Soviet training uses native Cold War programme 6, size 1, with donor consent,
capacity and 25 PP. Syria pays hosting only after a new programme starts. Loans
transfer real lender cash and create equal Syrian debt. Project grants are
reserved for one eligible project or returned. Pipeline payments leave the actual
Iraqi treasury. Invitations and international agreements have recipient responses,
execution-time revalidation and expiry. Security operations can invite a voluntary
US sanctions response through the actual Imperia system. See
`FOREIGN_IMPLEMENTATION.md` for source paths, scopes and contract details.

## Modern content retirement

`retire_modern.py` performs bounded, idempotent migrations with recovery copies.
The retirement reports list 41 removed files, removal of post-2000 country
history and the old Syrian AI selections, and all changed foreign references.
Foreign reads of deleted focuses are false; foreign diplomatic settlements no
longer award nonexistent Syrian focuses. Their actual negotiated outcomes remain.

Twenty-seven genuinely shared definitions, 71 English text keys and two Gulf-used
unit templates remain because other countries consume them. Their original IDs
are compatibility contracts, not active modern Syrian programmes. Art, the country
tag and reusable MD military/economic infrastructure remain available.

The historical council uses the existing Syrian national flag formatted as a
collective emblem. Verified existing portraits are reused where available;
unavailable historical individual portraits use a generic Middle Eastern portrait.
This does not claim a full new set of historical portrait artwork.

## Build and verification

Run from the mod root with the configured Python runtime:

```powershell
python tools/syria_1970/build_content.py
python tools/syria_1970/validate_content.py --report tools/syria_1970/validation.json
python tools/syria_1970/validate_tooltips.py --report tools/syria_1970/tooltip_validation.json
python tools/syria_1970/validate_decision_localisation.py
python tools/syria_1970/validate_event_choices.py
python tools/syria_1970/validate_runtime_repairs.py
python tools/syria_1970/validate_retirement.py
python tools/syria_1970/test_lifecycle.py
python tools/syria_1970/test_foreign.py
```

The independent parser compares installed IDs, resolved anchors, prerequisite
groups, exclusions, durations, costs and all 842 modifier grants with the approved
input and explicit user amendments. It checks native sprite/text/helper/flag references.
The retirement audit checks the backed-up providers against live incoming calls.
Fifteen scenario-model tests exercise government departure/return, staged
reforms, borrowing, changed control/funding, once-only construction, real war-goal selection,
GDP funding and operational cleanup. These models are not an HOI4 engine.

`render_preview.py <absolute-output.html>` independently resolves installed focus
positions and reads actual reward and decision scripts. It embeds native MD art
and HOI16 bitmap labels. `verify_preview.cjs <preview-directory>` checks all 38
sections at 320/736/1024 pixels, including actual cost and war-goal inspection.
The 114 browser views have no script errors, missing images, clipping or overflow.
The approved card/connector geometry has no detected card collisions.

## Repair based on the player's screenshots and engine log

The player's actual log exposed errors missed by the earlier source checks:
scalar dynamic-modifier removal and BOM-prefixed shared political scripts.
Removal now uses the native `{ modifier = ID }` block. Changed non-localization
scripts are plain UTF-8; English localization retains its required BOM. Scoped
recovery copies and the repaired-file list are in `encoding_backups/` and
`encoding_repairs.json`. The generator preserves this encoding on subsequent runs.

Scenario/tag checks remain executable inside `hidden_trigger`; meaningful party,
leader, coalition and funding conditions use explicit English labels. The
technical initial-start-date lines and deferred-programme paragraph have been
removed from the focus reward display. All 420 narrative descriptions were
rewritten individually in `english_politics.json` and `english_national.json`.

`validate_tooltips.py` checks all 420 independent display/execution boundaries,
842 modifier pairs, 29 material entry rewards and the exact approved
outlook IDs, positions and unlocks. It also checks argument shapes and raw script
encoding. The model interpreter excludes display-only effects from execution.
The repair does not change approved geometry or substitute invented bonuses.
Completed, implemented entries in existing saves receive their newly authorized
modifier package once through the dated migration. Each new completion records
the same signature; refreshing or loading cannot duplicate the package, replay
construction, debit cash again or reissue events. Missing programme variables are
initialized without overwriting existing earned values.

The subsequent five-screenshot repair adds the implicit `_NOT` localization
variants required by native trigger presentation. Inverse text negates the actual
whole condition; absence of a pending offer does not falsely claim an answer.
All new event option keys use `.option_a` etc., disjoint from `.t` and `.d`.
All domestic and foreign choices explain their distinct actual outcomes, including
explicit no-change/cancel outcomes. Native numerical material effects retain
their own previews, while guarded bookkeeping remains hidden.

Mandate choices now switch Atassi/Jadid programme authority without changing
Atassi's actual presidency. The leader setter preserves the incumbent when the
same person is selected; a real transfer uses native retirement instead of death.
Campaign/coalition decisions require at least one eligible legal party. Distinct
Kurdish representation choices cannot accumulate a joint compact accidentally.

The latest captured crash is reviewed in `CRASH_REVIEW_20261019.md`. It confirms
an engine access violation reading address 0x68; the stack does not identify its
script trigger. The same run rejected a malformed war-goal list produced by our
AST writer. Bare list serialization is repaired, raw `_bare`/`_list` assignments
are rejected, and output round trips are checked. These source repairs do not
establish that the access violation has been reproduced or resolved in HOI4.

Decision prerequisites are also presented independently of internal state names.
`decision_presentation.py` covers all 69 gameplay decisions and 420 conditional
resumption decisions. Native `custom_trigger_tooltip` wrappers explain programme
implementation, government, leadership, crisis status, negotiations, funding and
stage limits; scenario identity and initialization checks remain hidden but
executable. The same treatment covers conditions in completion/expiry tooltips.
Four discrete progress counters have explicit English effect captions, while
clamps and cache refreshes are hidden. Visibility filters remain internal.

The compiler compares the complete decision AST before and after removing only
presentation metadata and wrappers. Per-file gameplay digests are recorded in
`decision_presentation_build.json`. The independent decision-localization audit
checks emitted names, descriptions, condition labels, substitution references,
the player's screenshot regression and those semantic digests. This is source
verification; a fresh in-game hover remains necessary to confirm engine rendering.

The five skill amendments are staged, reviewed and installed through
`skill_updates/`, preserving original metadata and previous-file hashes. They
record the concrete parser, presentation, screenshot and English-writing lessons.
The official skill quick validator could not run without PyYAML; a separate
metadata-preservation, scaffold and local-reference check passed.

**Fresh engine test still required after a full HOI4 restart:** startup/loading,
exact engine tooltips and connectors,
save/reload, native economic ticks, AI progression and live multiplayer responses.
Static/source and browser results do not establish those runtime outcomes.
The recorded player log predates the repair; it is evidence of the original
defects, not confirmation that the corrected files have loaded in a fresh game.

Historical correction reference: [Munzinger, Ahmed Khatib](https://www.munzinger.de/register/portrait/biographien/Ahmed%2BKhatib/00/12824)
records his death in 1982. Where only the death year is established, prolonged
alternate stewardship becomes collective from the first day after that year.
The original concept research cites the
[Library of Congress country study](https://tile.loc.gov/storage-services/master/frd/frdcstdy/sy/syriacountrystud00coll_0/syriacountrystud00coll_0.pdf)
for the 1970 transition and Syrian institutions.
