# Global-chain review: repeated crash 2026-10-19 10:37:48

Read-only source investigation of the supplied `hoi4_20261019_103748` crash, compared with the earlier `hoi4_20261019_100834` crash. This review makes no claim of a successful in-engine reproduction or a proven fix.

## Evidence and timing

- Both `exception.txt` files report HOI4 `1.19.3.0.c01a`, access violation `C0000005`, address `0x00007FF7FB1B45C6`. Their first eight displayed stack frames match. The newer stack includes one extra nested `PHYSFS_swapULE64 (+ 18472713)` / `(+ 3434569)` pair before rejoining the old sequence. These exported labels do not identify the actual game subsystem; they must not be interpreted as proof of a filesystem fault.
- The latest live `logs/game.log`, which corresponds to this crash, ends at **10:37:48 / 1970.06.01.02**: Syria abstained from GA vote type 6. The preceding entries are numerous countries' monthly economic and African Union event choices at 01:00.
- The earlier report, captured before the live log was overwritten (`CRASH_REVIEW_20261019.md:12`), records **10:08:34 / 1970.06.13.04**, Chad's `bankruptcy_default_on_debts`. Consequently Chad's decision is **not a common immediately preceding logged command**. The latest crash occurred twelve game days earlier.
- `meta.yml` names only **MD Cold War**, and records `IsOldSave: false`. There is no evidence here of a second active mod or an old-save migration as the explanation.

## Last logged global call

`events/UN_Voting_Events.txt:621–631` (GA abstention option) conditionally appends `THIS` to `global.general_assembly_vote_abstain`, logs the vote, and calls `international_systems_update`.

`common/scripted_effects/01_international_systems_effects.txt:331` only calls `international_systems_force_update` if a vote is live or the country is player-controlled. That helper, immediately above it, increments or resets the numerical global GUI dirty counter `global.international_systems_updated`.

This path does not change a country leader, create or dissolve a faction, enter an event-target scope, remove a state, or modify an army. Source inspection therefore supplies **no concrete null country/character/state operation in the last logged option**. A queued operation, another system at the same hour, or a player interaction may still be responsible. Last log entry alone does not establish causality.

## Confirmed separate 1970 defect: Algerian monthly weights

`common/on_actions/99_ALG_on_actions.txt:133–144` runs a poaching `random_list` every month with weights `chance_to_kill_poachers` and `chance_to_not_kill_poachers`.

Those variables are initialized at `history/countries/ALG - Algeria.txt:288–291`, inside the **2000.1.1** history block beginning at line 26. The 1970 block at lines 5–24 does not initialize them. The current crash error log accordingly reports two undefined weights and “all entries in random_list have 0 chance” on February 1, March 1, April 1, May 1, and June 1. The engine explicitly reports that no random-list effect is executed.

Minimal repair proposal: execute this random list only when both weight variables are initialized and their total is positive. That preserves the existing modern-start values and avoids inventing a new 1970 balance. Alternatively initialize the subsystem from its native provider if it is meant to be active in 1970; `ALG_update_anti_poaching` in `common/scripted_effects/99_ALG_scripted_effects.txt:189` derives weights from police laws, but lacks a fallback if none of its specific police ideas is present.

This is a reproducible script error and a reasonable narrow repair. **It is not an established crash cause**: the same failure was logged repeatedly in months from which the simulation recovered, and the previous crash occurred June 13, rather than at that month's poaching pulse.

## Debt-default and weekly economy trace

- `common/decisions/bankruptcy_decisions.txt:926` defines the prior last-logged decision. Its first-AI-rescue branch (`:943`) only reduces debt, sets a two-year rescue flag, and adds a one-year idea. The other branch records default accounting, calls the native `depression` helper, starts a mission, and may release subjects.
- `depression` (`common/scripted_effects/00_budget_effects.txt:1149`) swaps the existing economic-cycle idea under the native cost-suppression flag; it contains no character, event-target, faction, or state deletion.
- Subject-release loops at `bankruptcy_decisions.txt:914–915` and `:974–975` iterate native `subjects` while calling `end_puppet`. A snapshot loop or `every_subject_country` would avoid collection mutation during iteration. This is a **potential defensive improvement**, not evidence of this crash: no supplied save establishes that Chad had subjects, and the latest crash has no nearby debt-default log.
- Weekly country economy updates start at `common/on_actions/MD_on_actions.txt:4`; `ingame_update_setup` is called at `:37`, followed later by treasury accrual, AI repayment and automatic borrowing (`:137–168`). `ingame_update_setup` (`common/scripted_effects/00_money_system.txt:220`) recomputes national/state values and the expense/income aggregates. Its capital repair is guarded by owned-state existence. `automated_debt_taker` (`00_economic_system_utilities.txt:29`) and `ai_repay_debt` (`:47`) perform guarded numeric accounting; no definite invalid country or character dereference was identified in these inspected entry paths.

## Recommended next diagnostic step

Use the minidump's actual effect-command/stack data to identify the native effect being executed, or add narrowly scoped before/after diagnostic logs to the suspected effect chain once that chain is identified. Avoid presenting an Algerian error cleanup, a broad economic rewrite, or disabling Syria as a proven resolution to this repeated address. The same address is a useful signature, but without symbols or effect-context evidence it does not select a unique source command.

No loaded mod files were changed by this review.
