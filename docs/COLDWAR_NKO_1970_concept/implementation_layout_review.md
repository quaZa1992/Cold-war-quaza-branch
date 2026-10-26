# NKO 1970 implementation integration review

Read-only discovery for the approved 189-focus design. No loaded files were changed. The most relevant local integration precedent is the Syria 1970 party-programme lifecycle, combined with the existing NKO-tagged weekly action and MD’s central party-change effect.

## Starting state and focus-tree setup

`history/countries/NKO - North Korea.txt:5–42` defines the January 1970 setup. It assigns the MD ruling-party array variable `ruling_party = 4` (WPK) at line 30, creates Kim Il Sung as leader, and loads `mdcw_1970_generic_focus` at line 42. This is separate from the engine ideology group set to `communism` at line 13. Gate party programmes against the MD array value, not just the engine ideology.

Syria demonstrates an idempotent startup initializer that can load a country-specific tree if missing: `common/on_actions/COLDWAR_SYR_1970_on_actions.txt:4–9` scopes from startup to `SYR`, then calls `COLDWAR_SYR_initialize`; `common/scripted_effects/COLDWAR_SYR_programme_effects.txt:3892–3914` checks the 1970 tag and scenario, runs one-time setup behind `COLDWAR_SYR_initialized`, loads the tree only if absent, and calls programme reconciliation on every initializer invocation. For NKO, use the same separation: one-time setup behind an initialization receipt, tree loading guarded by `has_focus_tree`, and a refresh call outside the one-time block. Keep unrelated one-time rewards out of a repeatable initializer.

## Hooks and scopes

| Hook / call site | Observed scope and source | Recommended NKO use |
|---|---|---|
| `on_startup` | General startup action. Syria explicitly checks `country_exists = SYR`, then scopes into `SYR` (`COLDWAR_SYR_1970_on_actions.txt:4–9`). The project scenario startup action is global and addresses `USA` explicitly (`00_IMP_cold_war_scenario_on_actions.txt:3–14`). | Check `country_exists = NKO`, then scope to `NKO` to initialize the 1970 tree and reconcile earned programmes. Guard the initializer by NKO original tag and `IMP_is_1970_scenario = yes`. |
| `on_weekly_NKO` | Tag-specific weekly hook listed by the local hook catalogue as `on_weekly_TAG`; already used in NKO’s existing actions (`common/on_actions/_documentation.md:5–11`, `common/on_actions/99_NKO_on_actions.txt:4–22`). Its body is in NKO scope, as shown by the unqualified `has_completed_focus`, flags, and NKO effects. | Add a scenario-guarded weekly initialization/reconciliation branch to the existing tag hook. This supplies a low-frequency recovery path after startup/load and catches states changed outside the focus/UI callbacks. Do not move this lightweight state check to a daily or hourly loop. |
| `on_government_change` | Listed as a politics hook (`_documentation.md:16–21`). Syria calls its refresh directly in the action body (`COLDWAR_SYR_1970_on_actions.txt:15–17`), and the global MD hook performs country-scope updates (`00_on_actions.txt:2005+`). | Use an NKO/scenario-guarded refresh for actual engine-government changes, but do not rely on it for MD subparty-slot changes. |
| `on_ruling_party_change` | Listed in the same politics catalogue; Greece uses it as a country-scoped refresh callback (`COLDWAR_GRE_1970_tree_on_actions.txt:22–32`). | It can cover actual engine ruling-party changes as a second idempotent callback. It does not replace a direct call after an MD array-index change. |
| Direct MD party-change callback | The central `change_ruling_party_effect` in `common/scripted_effects/00_MD_politicsview_scripted_effects.txt` sets the MD `ruling_party` variable at line 1996, then calls `set_politics` and updates the leader/coalition. At lines 2051–2058 it explicitly notes that subideology swaps keep the same ideology group, so `on_government_change` cannot carry them; the Syria refresh is called directly from this helper. | Add a narrowly guarded NKO 1970 refresh beside that established callback, after the new party/leader state is written. This is the key path for same-ideology changes among the NKO party slots. Also call refresh from any NKO-specific event that changes party/leader programme state without using this helper. |

The local `_documentation.md` lists startup, daily/weekly/monthly, government-change and ruling-party-change hooks, but no `on_load` or `on_game_load` action. No dedicated load hook was found in active `common/on_actions` definitions. Treat startup and the NKO weekly reconcile as the available initialization/backstop pair; verify actual save-load timing in HOI4 before claiming a load callback.

The current NKO weekly action already handles 2000s arms-export persistence and patrols (`99_NKO_on_actions.txt:6–19`), so keep the new branch independent and guarded with `original_tag = NKO`, `exists = yes`, and the 1970 scenario trigger. The separate `on_monthly_NKO` content is date-gated to post-1999 (`:24–43`); it is not the right cadence for 1970 party-programme reattachment.

## Dynamic modifier lifecycle without replaying rewards

Syria’s `COLDWAR_SYR_refresh_programmes` (`common/scripted_effects/COLDWAR_SYR_programme_effects.txt:383–418`) is the relevant model. For each eligible programme, it checks a durable `*_programme_earned` flag plus the active party/leader condition. If eligible and the dynamic modifier is missing, it calls `add_dynamic_modifier = { modifier = ... }`; if ineligible and present, it removes it with the structured `remove_dynamic_modifier = { modifier = ... }` form. The refresh body contains reconciliation only; it does not reconstruct focus construction, cash, research grants, or other one-time outcomes.

The focus-reward example shows the state boundary clearly: `common/scripted_effects/COLDWAR_SYR_focus_rewards.txt:5–23` has a separate once-only `*_implemented` receipt, records `*_programme_earned`, updates the variable-backed modifier values, and refreshes the modifier. Subsequent refreshes can remove it when a different programme governs and add it again if that programme returns, while the earned receipt and variable values persist. This reattachment model avoids replaying a focus reward.

For NKO, keep three pieces separate:

1. **Permanent focus receipt:** set once when the focus genuinely completes. Do not clear it on party change.
2. **Earned variable-backed values:** preserve them when a programme becomes inactive. The dynamic modifier definition reads these values; the refresh must not zero or rebuild the award during a party transition.
3. **Currently active programme modifier:** reconcile from the durable receipt plus the actual current MD party slot and any leader/institution guard. Add it only when absent and eligible; remove it when present but no longer eligible. A weekly tick or save-load backstop can repair a missed callback without granting the focus again.

Party programmes may share the engine ideology while using different MD indices. The direct callback after `change_ruling_party_effect` is therefore essential. For conditional leader programmes, run the same refresh after the leader/office flag changes, even if the party slot stays the same. Keep continuous modifiers distinct from permanent national rewards so a return to a prior party reactivates only its earned programme, not construction or a treasury payment.

## Verification boundary

These hooks and patterns are present in the current repository and establish an integration route; they do not prove engine execution order, save-load behavior, dynamic-modifier reattachment timing, or multiplayer callback behavior. Validate the emitted NKO hook scopes and run a game test covering start as slot 4, switch to another slot within the same ideology, switch to another ideology, save/reload, and return to a previously earned slot. Check that only the matching modifier changes and that no focus reward is replayed.
