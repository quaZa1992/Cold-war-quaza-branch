# IMPERIA COLD WAR

## Japan party capital packages: independent source review

Review date: 2026-10-27

### Scope and method

This review traces the six new party capital packages from the effective reward revision into the installed focus definitions, their native effect previews, their scripted reward helpers, and party modifier activation. It checks the package-specific state guards, building ceilings, slot grants, GDP-share charge formulas, one-time receipts, and limited-use technology rewards. The review is based on emitted source inspection. It does not report a native tooltip or game transaction test; the root agent's separate frozen runtime probe is outside this review.

The reward definitions were read from `tools/japan_1970/reward_revision_20261027.json` and checked against `common/national_focus/COLDWAR_JAP_1970_focus.txt`, `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt`, and `common/dynamic_modifiers/COLDWAR_JAP_1970_party_modifiers.txt`.

### Package audit

The cost column gives the one-time Treasury debit as fixed billions plus a share of current GDP. At GDP 100B, the last column gives the expected numeric debit. State IDs and asset levels are the emitted native construction rewards. Each construction level receives the same number of extra shared state slots before construction.

| Focus | Required party slot | Treasury cost | Capital assets and added slots | Other reward | GDP 100B |
|---|---:|---:|---|---|---:|
| `COLDWAR_JAP_1970_ldp_deep_fork1_a_follow` | LDP, 1 | $2B + 0.75% GDP | State 615, industrial complex +1, +1 slot | CAT_industry research bonus, 50%, 1 use; active LDP: civilian factory productivity +3%, research speed +4% | $2.75B |
| `COLDWAR_JAP_1970_ldp_deep_fork1_b_follow` | LDP, 1 | 1% GDP | State 612, offices +2, +2 slots | Active LDP: offices productivity +4%, bureaucracy cost multiplier +3% | $1B |
| `COLDWAR_JAP_1970_dsp_programme` | DSP, 2 | $2B + 1% GDP | State 614, industrial complex +1, +1 slot | CAT_industry research bonus, 50%, 1 use; active DSP: civilian factory productivity -2%, stability +2% | $3B |
| `COLDWAR_JAP_1970_jsp_programme` | JSP, 3 | 1% GDP | State 612 industrial complex +1 and state 616 offices +1, each +1 slot | Active JSP: foreign influence defence +3%, research speed -2%, stability +3% | $1B |
| `COLDWAR_JAP_1970_jcp_industry` | JCP, 4 | $1B + 1% GDP | State 611 industrial complex +1 and state 612 offices +1, each +1 slot | Active JCP: navy XP gain -2%, research speed +3% | $2B |
| `COLDWAR_JAP_1970_komeito_programme` | Komeito/KMT, 14 | $3B + 1% GDP | State 612 offices +1 and state 616 industrial complex +1, each +1 slot | Active Komeito: migration rate +2%, stability +3% | $4B |

### Guard, transaction, capacity, and preview findings

All six helpers apply inside a single `if` guard with the expected original-tag and scenario checks, a defined `ruling_party` value equal to the party's native slot, an unused package receipt, and `gdp_total > 0`. Every named asset state is separately checked for Japanese ownership, Japanese control, and the relevant building level ceiling. The helpers do not impose a treasury affordability check. The GDP and fixed debits, party-variable increments, construction, technology bonus when present, and receipt are all inside the same guarded transaction. The receipt is written after the package effects. A failed party, GDP, ownership/control, or capacity guard therefore skips the full package rather than charging while withholding its assets.

The two-level Kansai offices package uses `building_level@offices < 49`, which is the correct precondition for adding two levels under the native state maximum of 50. At 48, the two-level transaction fits exactly; at 49, the guard rejects the complete package. Each other one-level package requires the relevant building level to be below 50. Multiple-asset packages guard each distinct state and building type independently. These packages do not depend on existing free shared slots: each asset level is preceded by an equal `add_extra_state_shared_building_slots` grant in that asset's state scope. No package here combines different building types against a shared type-specific cap.

Each of the six focus completion blocks contains an unconditional `effect_tooltip` preview for its actual signed variable changes, fixed and GDP charges, all assets and added slots, and any CAT_industry bonus. The scripted helper is called separately inside `hidden_effect`, keeping the transaction guard out of the player-facing preview while retaining it for execution. The GDP validity check is hidden in focus availability, and the real party and state/capacity requirements use native requirements. The previews therefore remain inspectable for a player who does not currently satisfy the party or other availability conditions. This is a source inspection finding, not a live UI observation.

### Party activation and replay

The corresponding dynamic modifiers check `original_tag = JAP`, the 1970 scenario trigger, and the exact `ruling_party` slot. Their party-specific numeric variables persist across changes of government, while the dynamic modifier applies only when its party is ruling. Thus the party package's ongoing bonuses and drawbacks deactivate with a government change and reactivate if that party returns. The one-time capital and technology rewards are protected by `COLDWAR_JAP_1970_party_reward_done_<package>` receipts in addition to being reachable through one-time completed focuses; returning to office does not grant the package again. Existing party initialization is itself guarded by its initialized flag.

The party slots align with the existing native MD triggers: LDP slot 1 (`western_conservatism_are_in_power`), DSP slot 2 (`western_liberals_are_in_power`), JSP slot 3 (`western_social_democrats_are_in_power`), JCP slot 4 (`emerging_communist_state_are_in_power`), and Komeito slot 14 (`neutrality_neutral_conservatism_are_in_power`). The new research bonuses use the native `CAT_industry` category and each has one use at 50%.

### Compatible route cost envelope

At a GDP value of 100B, summing one complete party route's one-time base programmes and allowed mutually exclusive fork choices gives the following package-family totals. These totals cover the party reward helpers only; they exclude other national economy, foreign policy, and unrelated focus costs. The mutually exclusive LDP fork 1 A and B follow-ups cannot be combined, so both valid outcomes are shown.

| Party route | Fixed cost | GDP share | Total at GDP 100B |
|---|---:|---:|---:|
| LDP with fork 1A follow-up | $21B | 0.75% | $21.75B |
| LDP with fork 1B follow-up | $19B | 1.00% | $20B |
| DSP | $21B | 1.00% | $22B |
| JSP | $18B | 1.00% | $19B |
| JCP | $15B | 1.00% | $16B |
| Komeito | $19.5B | 1.00% | $20.5B |

These are large, finite capital programmes, not recurring bills. The cost previews use the same `gdp_total` formula as execution. This review confirmed the formulas and sums in emitted source; it did not observe the Treasury value in the native interface.

### Source anchors

- LDP A follow-up focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:8309`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:305`.
- LDP B follow-up focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:8347`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:337`.
- DSP programme focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:8735`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:624`.
- JSP programme focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:9304`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:1040`.
- JCP industry focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:9799`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:1402`.
- Komeito programme focus and preview: `common/national_focus/COLDWAR_JAP_1970_focus.txt:10439`; helper: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:1873`.
- Party dynamic modifier eligibility: `common/dynamic_modifiers/COLDWAR_JAP_1970_party_modifiers.txt:1-126`.
- One-time modifier initialization: `common/scripted_effects/COLDWAR_JAP_1970_party_effects.txt:3-18`.
- Native industrial complex and offices caps: `common/buildings/00_buildings.txt:43-53` and `common/buildings/00_buildings.txt:255-265`.
- Native party trigger definitions: `common/scripted_triggers/01_political_triggers.txt:176-197` and `common/scripted_triggers/01_political_triggers.txt:267-273`.
- Native `CAT_industry` category: `common/technology_tags/00_technology.txt:184`.

### Review result

No source-level defect was found in these six emitted package transactions. The party, GDP, receipt, state ownership/control, capacity, slot-grant, and one-time research flows align between focus previews and reward helpers. Native UI readability, actual parser execution, and real transaction results remain for the separate root runtime/native probe.

## Final native evidence

The final single-client native probe confirms the actual LDP industrial capital transaction and its 2.75B debit at fixture GDP=100, then checks party departure and return. The policy modifier deactivates and restores without another charge or asset grant. Immediate modifier refresh after programme variables change is now part of the canonical party writer. This extends the source review; it does not establish all party routes through a full playthrough or multiplayer synchronization.
