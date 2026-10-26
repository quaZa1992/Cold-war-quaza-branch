> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# Original Millennium Dawn EU compatibility review

Reference: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`. The reference installation is read-only throughout this task. This review uses its actual GUI, scripted GUI, decisions, triggers, effects and on-actions rather than assuming how the original system works.

## What the original interface actually provides

The native launcher is `open_the_eu_scripted_gui`, bound to `EU_open_the_eu_scripted_gui_window`. Its click toggles the player's `new_EU_open` flag and increments `global.EU_dirty_update_var`. The native main window is `EU_main_background_window`; the five navigation buttons are **Offices**, **Europeanism**, **Parliament**, **Council** and **Fiscal**. See original `common/scripted_guis/01_european_union_guis.txt:4` and `interface/eu.gui:70`.

The Council page is an actionable catalogue, not just a current-vote display. Its available proposals, passed measures, members, supporters and rejecters are all visible. The available-proposal binding is:

```
global.EU_council_votes
  -> dynamic_lists.list_of_available_council_votes
  -> eu_council_available_reforms_list
  -> eu_council_available_reforms_button_click
```

The click assigns the current agenda, starts national vote missions, sends events to human members and updates the dirty variable. Original references: `common/scripted_guis/01_european_union_guis.txt:4382`, `:4473`, `:4481` and `:4553`; the window and scroll/grid layout are in `interface/eu.gui:2022`.

The original globally registers dynamic-list window types and attaches their scripted GUIs using `parent_scripted_gui = european_union_gui` and `window_name = ...`. A type does not need to be physically nested inside the main GUI declaration. `european_info_dynamic_lists` / `state_of_the_european_union_container` provide a particularly small reference at original scripted GUI `:4157` and interface `:1931`. The same pattern is used by the Parliament secondary display at scripted GUI `:5187` and interface `:1714`.

## Compatibility mapping

| Native feature or contract | Native implementation | Cold War requirement and integration rule |
|---|---|---|
| Shared membership identity | `EU_member` idea; `global.EU_member`; `EU_resync_member_array` | Keep the canonical idea and array. The six founders are FRA, GER, ITA, BEL, HOL and LUX. Recompute institutional totals when actual membership changes. |
| Shared launcher and refresh | `new_EU_open`; `global.EU_dirty_update_var`; original scripted GUI `:4` | Keep one launcher, one player's open/closed state and native dirty invalidation. Initialize the player's selected page explicitly on opening. |
| Available Council measures | `global.EU_council_votes`; original scripted GUI `:4481` | Present the Cold War treaty, policy, budget and accession catalogue directly in the community interface. Retaining Decisions as an alternative entry point is useful; hiding the only proposal controls in Decisions is not equivalent to native MD. |
| Passed-law catalogue | `global.EU_passed_votes`; original scripted GUI `:4553` | Show `global.CWEC_enacted_dockets`, with the same readable titles and substantive tooltips as proposals. A successful vote must visibly move policy into the enacted record. |
| Council procedure | Original voting effects and decision mission `EU_voting_mission_focus_EUXXX_QMV_result` | Use the human-only frozen CWEC electorate. Native AI weight calculation, opinion lobbying and influence-for-votes buttons must not be re-enabled. |
| Parliament information | `election_EU_Parliament` at original effects `:1582`; country delegations at `:1677` | Display all seats, active player seats, the current parliamentary powers, and delegation status. Historical appointment/direct-election reforms must remain separate from AI party popularity. |
| Institutions and offices | Original main GUI office controls; proposal eligibility at original scripted GUI `:4257` | The rotating Council presidency is present in CWEC. Native offices affect authority and costs, so Commission and Parliament offices cannot be described as ported merely because an institution summary is shown. Any future office appointment requires a human-only ballot and a historically appropriate competency. |
| Europeanism and campaigns | Original effects `EU_update_vars:29`, `europeanism_change:119`; native Europeanism UI | Europeanism/influence campaigning is distinct from a human ballot. Original AI influence and ideology drift must not silently determine political outcomes. Any retained integration support must be a visible political/economic variable, not an inverse ideology modifier. |
| Budget and MFF | Original effects `update_EU_budget_call_rate:1312`, `distribute_EU_budget:1395`; original decision drafts `:435`, `:463`, `:541`, `:569` | Publish the selected allocation, contributions, funded cash and national net accounts. Adopt changes by human vote. Use CWEC funded transfers through MD's weekly finance calculation; never run both native subsidy generation and CWEC cash settlement. |
| National finance integration | Original money effects EU additional income and contribution expense; weekly treasury accrual in `MD_on_actions` | Retain native national income/expense reporting and single weekly treasury application. Cash from an actual national payment funds a later common disbursement; preview/recalculation must never create cash. |
| Single-market investment | Original `invest_in_EU_single_market_infra:217` | A community project needs an accessible request action, an explicit recipient/state, common commitment, national match, duration and completion result. No invisible grant-only substitute for project construction. |
| Monetary interventions | Original `execute_OMT:241`, `remove_OMT:273`, `joining_the_euro:1829` | OMT/euro/ECB are not 1970 starting institutions. Keep EIB capital/loans separate from common grants; later monetary integration needs an explicit adopted path. Do not automatically enter the euro on admission. |
| Admission and withdrawal | Original `EU_apply_for_membership:1635`; Article 50/withdrawal decisions from `:777` | Application, member approval and accession must remain visible. A sovereign 1970 withdrawal must not be labelled as a pre-existing Lisbon Article 50 procedure. Admission must not silently rewrite NATO or transfer territory. |
| Modern integration/endgame | Original startup proposal IDs at effects `:699`–`:751`; original USoE/POTEF systems | GDPR, Dublin II, Lisbon, modern military organisations and annexation endgames are not restored simply to fill a catalogue. Historical/alternative Cold War equivalents must use explicit prerequisites and human decisions. |

## Diagnosis of the empty replacement

The existing game log proves that the model was populated in the observed session:

```
[1970.01.01.12] CWEC initialized: members=6 seats=142 humans=1 GDP=2216.15916
```

The previous replacement provided five views: Members, Institutions, Common Treasury, Current Ballot and Flow History. It provided **no proposal catalogue and no enacted-law catalogue**. All 51 political options existed only as Decisions. This is a missing interface feature even when the finance and voting scripts are otherwise valid.

Every replacement page was also gated by `check_variable = { CWEC_view = n }`, but neither the native launcher nor `CWEC_initialize` assigned that local variable. Runtime-free tests defaulted missing variables to zero. The repair must set a deliberate opening page and use explicit country page flags, matching the native navigation pattern. A static test's default-value assumption is not evidence of successful engine rendering.

## Review gates for the repaired interface

1. The native launcher opens a populated Members page immediately, without a prior tab click, for both a fresh start and an already running save.
2. Exactly one content view is visible. Navigation is a local country state and never a shared global page index.
3. Every `window_name` and every `entry_container` resolves to a globally registered `containerWindowType`; every dynamic-list key resolves to a gridbox under that window.
4. Numeric catalogue rows stay in player context. Their `v` is the docket ID; availability/cost checks use the human proposer, not a country interpreted from the ID.
5. Country rows use `change_scope = yes` with `global.EU_member`, `global.CWEC_ledger_members` or the frozen electorate. Numeric history/catalogue rows must not use country scope switching.
6. All historical/alternative proposals remain inspectable in the catalogue, including locked entries with reasons and implemented entries with status. Only a valid human proposer can pay the political-power cost and open proceedings.
7. The enacted list uses `global.CWEC_enacted_dockets`. Programme flags, treasury allocations and actual funded results remain separately inspectable.
8. Finance/project buttons invoke exactly the same guarded effects and payments as their Decisions counterparts. The UI must not create a second finance implementation.
9. Old modern GUI children, AI GUI evaluation and modern result handlers remain excluded while `CWEC_active` is set.
10. The in-game view, text wrapping, dynamic rows and click outcomes must be checked in HOI4. Static binding and voting tests cannot certify visual layout or multiplayer synchronisation.

The final repaired interface is reviewed against these gates during the active task. Items that require an actual running game must remain labelled unverified until observed.

## Review of the replacement bindings

The revised `CWEC_gui.txt` now follows the original contracts: seven globally registered content windows share `CWEC_main_gui`, the native dirty variable, and a local `CWEC_page_*` country flag. Country delegation, member, ledger and ballot rows use country scope switching. The proposal catalogue, enacted-docket record and weekly history retain numeric `v`/`i` values in player context.

The Treaties page contains both `global.CWEC_proposal_catalogue` and `global.CWEC_enacted_dockets`, restoring the original available/passed split. The new submission adapter preserves the selected ID before recalculation, checks a live second human member, verifies the same substantive prerequisites as the Decisions and charges 35/50 political power only after proceedings actually open. It never calls the modern AI or annexation handlers.

The seven navigation buttons now use the existing native `GFX_sort_button_83x29` without reducing the text scale. The Projects page has direct programme, construction, EIB, contribution, implementation, Schengen, withdrawal and accession controls. Each control is owned by that page's scripted GUI. The original long Decision titles were flagged during review for replacement with short GUI-specific labels; full descriptions remain in tooltips.

The initial-page path has now also been reviewed. The existing native launcher calls the safe state repair, explicitly selects the Members flag when opening, and then invalidates the native dirty variable. All seven navigation helpers clear the other page flags before selecting one. Startup and repair populate the catalogue. Institution recalculation derives an assessment preview without moving any cash or changing the prepared weekly payment orders.

The fourteen national GUI actions have guarded APIs derived from the actual Decisions' visible/available/complete clauses and political-power costs. The withdrawal action and Decision share a 180-day scheduled notice. Both its hidden event and legacy Decision completion guard membership, so simultaneous completion cannot remove membership twice. No native modern voting/result handler is re-enabled.

Review verdict: the revised code restores the original **membership/delegation information**, **available and enacted proposal catalogues**, **actionable human Council/assembly proceedings**, **budget information**, **national programme actions**, **accession/withdrawal access**, and **native finance integration**, while adding a funded payment ledger and EIB accounting. The binding, scope, explicit-default and action-guard contracts pass code review. The UI regression harness also passes 56 actual-script visibility states and checks all seven pages, fourteen actions, list ownership and geometry.

This is **not** a claim that every modern MD feature was ported. Modern office election/authority mechanics, Europeanism/influence campaigns, AI party-popularity parliamentary simulation, the full euro/ECB/OMT path, Frontex/EuroArmy/EuroNavy and the original annexation/federalisation endgames are not silently restored. The implemented Cold War treaty and cooperation options are the selectable scope; future ports need explicit historical adaptation and human political authority.

These are code-level binding and scope findings. Actual runtime rendering, save/load and multiplayer synchronisation remain separate verification gates; no successful in-game rendering is implied by this review.

## Keeping the original reference reviewable

`original_md_reference_manifest.json` records SHA-256, size and line count for 21 reviewed original files: the EU GUI and graphics, scripted GUI, effects, triggers, Decisions/categories, events and English localisation, plus membership ideas, startup/on-actions and native money calculations. No reference installation file was modified.

Before a future EU change, run:

```
python tools/europe_1970/check_original_md_reference.py
```

The check reports changed or missing original files. The recorded baseline currently matches all 21 files. After a Workshop update, review changed originals against this document before explicitly updating the baseline with `--refresh`. The tool is a repeatable comparison, not a background monitor or an automation.
