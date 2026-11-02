IMPERIA COLD WAR

# France 1970 core party revision

## Input and scope

The core generator now accepts the frozen party proposal at `tools/france_1970_party_revision/proposal.json` with SHA-256 `5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419`. It retains every existing focus key and adds the four proposal focuses. The generator returns source text in memory; this task did not write emitted or loaded game files.

## Runtime changes

- All nine party branches remain visible. Focus availability and completion use the existing exact MD party-in-power predicates. Earned party modifiers are attached and removed by programme synchronization; finite focus rewards remain behind the existing earned receipts.
- Reciprocal offers keep their focus-specific diplomacy helpers and do not receive a second domestic focus reward. Their search tags use the native foreign-policy filter plus one leading substantive filter selected from the offer payload.
- The two new domestic decisions use their authored runtime guards for both visibility and completion. They charge the stated own-country GDP share once, preflight the state and native building cap before payment, grant one shared slot, construct, then award the limited industry research bonus. The decision completion receipt blocks replay.
- Native player effects continue to use MD syntax for GDP treasury changes, faction opinion, experience, doctrine reductions and finite research bonuses, including `CAT_energy`. No custom effect kinds were added.
- AI focus selection skips immediate treasury spending and recipient offers with setup fees during the native `bankruptcy_incoming_collapse` mission. Diplomacy acceptance decisions already have zero AI weight, so the AI cannot automatically accept and pay those bilateral setup fees.

## Save compatibility

All 152 prior focus keys are retained; four new focus keys were added. No old completion receipt is cleared. A one-time, France 1970 guarded migration rebuilds only focus programme modifier variables from current non-offer modifier effects whose `COLDWAR_FRA2_earned_<focus>` receipt exists. It clears stale pool variables from the previous approved snapshot first, so converted offer focuses such as Soviet Partnership no longer retain their old unilateral local modifier. It excludes every offer focus and does not replay treasury fees, buildings, research, doctrine, experience, opinion changes or starting spirit removals. The retired `pcf_parent_soviet_science_programme` definition remains zero-backed for old save loading and is removed once during the migration. The migration marker makes it idempotent.

## Verification

An in-memory `build_core()` smoke build against the frozen proposal returned eight source files and 115 English localisation entries. It confirmed 156 focuses, 35 recipient offers, foreign-policy tags and bankruptcy AI guards on all offer focuses, and guarded implementations for both new decisions, including resolved `assets_ready` scripted-trigger providers for both. The migration output contains only programme variable resets, receipt-gated modifier rebuilds and retired-modifier cleanup. GDP payments use a temporary `treasury_change` calculation in the same form as MD treasury effects, avoiding stale persistent values from earlier offer previews. Generated script strings were checked for UTF-8 without BOM and the project marker. Native references checked include `common/national_focus/00_generic.txt` for the bankruptcy AI guard and temp-variable opinion providers, `common/national_focus/03_china_north_korea_joint.txt` for foreign-policy search filters, `common/national_focus/COLDWAR_DDR_1970_focus.txt` for `CAT_energy`, and the existing France runtime providers for treasury, building-cap, doctrine and party-pool conventions. These are source checks only; no HOI4 runtime claim is made here. The root-owned compiler and validation pass remain separate.
