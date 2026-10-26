# Syria runtime UI review — 19 October 2026

Read-only source review of the five reported screenshots. Findings below describe
the pre-repair generator and loaded sources, not a fresh HOI4 runtime test.

## 1. Inverted decision requirement loses localization

`decision_presentation.py` wraps primitive flags in `custom_trigger_tooltip`,
including predicates nested inside `NOT`, but initially writes only the positive
localization key. The reported `COLDWAR_SYR_requirement_088259282155e6a3_NOT`
corresponds to the inverse of the command-settlement flag.

The installed game's `documentation/triggers_documentation.md:2431` describes
`custom_override_tooltip` as an AND wrapper. It supports `tooltip` and
`not_tooltip`; without an explicit negative tooltip the engine uses the root
localization key with `_NOT` appended. `custom_trigger_tooltip` is its compatible
alias (`:2482`). The current MD localization already contains explicit negative
variants, for example `party_is_in_power_or_coalition_TT_NOT` and
`election_threshold_max_NOT`.

Repair must provide truthful inverse text, and independently audit wrappers in
inverted contexts. Checking that the positive key exists does not establish
negative-context coverage. If `not_tooltip` is added explicitly, source semantic
comparisons must treat it as presentation metadata rather than a gameplay trigger.

## 2. Treasury requirement blocks native debt financing

`common/scripted_effects/00_budget_effects.txt:1487` defines
`modify_treasury_effect`: it adds `treasury_change` directly to `treasury` and
marks the money UI dirty. It does not require a positive balance or charge public
debt itself.

`common/scripted_effects/00_economic_system_utilities.txt:29` defines
`automated_debt_taker`, which converts a negative treasury to native borrowing.
The requested advance includes a buffer (1.25 times the shortfall plus one percent
of GDP); the debt includes the current one-percent origination fee. Native weekly
money processing invokes it after treasury accrual in
`common/on_actions/MD_on_actions.txt:168`.

Therefore removing Syrian focus affordability gates while preserving each
negative treasury charge allows the mod's existing budget/debt mechanism to
operate. The same gate must be removed from the visible requirement, execution
guard and deferred resumption decision. A second direct debt charge would double
finance the shortfall. Government, site ownership, physical capacity and genuine
political mandate checks are separate requirements and should remain.

## 3. Focuses that only unlock continuation or decisions

Eight focuses initially contain only a generated `policy_choices_tt` statement:

| Focus suffix | Subject | Suggested small national programme benefit | Suggested cost |
| --- | --- | --- | --- |
| industry_entry | Industrial survey | Civilian factory construction +2% | Bureaucracy spending +1% |
| infrastructure_entry | Infrastructure survey | Infrastructure construction +3% | Bureaucracy spending +1% |
| army_entry | Lessons of 1967 | Army organization +2% | Supply use +1% |
| air_entry | Air readiness audit | Air accidents −3% | Air personnel spending +2% |
| navy_entry | Coastal mission | Positioning +3% | Navy fuel use +2% |
| great_powers_entry | Dependencies review | Receiving investment cost −3% | Bureaucracy spending +1% |
| arab_world_entry | Regional diplomatic review | Stability +1% | Bureaucracy spending +1% |
| levant_entry | Unfinished conflict | Army defence +2% | Supply use +1% |

These are balance proposals, not historical measurements. Every modifier key is
already used by the corresponding emitted `COLDWAR_SYR_*_programme` modifier in
`common/dynamic_modifiers/COLDWAR_SYR_programmes.txt:366–530`; each can therefore
use the established earned-programme variable and refresh pipeline. The approved
focus geometry need not change. The visible “opens following policy choices”
message should be removed once an actual reward exists.

A broader inventory finds 29 focuses with no immediate modifiers, material
one-time effects, additional political outcome or starting-spirit reform. In
addition to the eight roots, these initially grant only decision access:

- `opening_entry`, `opening_corrective`;
- all eight `outlooks_*` focuses;
- `agriculture_entry`, `citizenship_entry`;
- `great_powers_10`, `great_powers_13`;
- `arab_world_06`, `arab_world_07`, `arab_world_09`, `arab_world_10`, `arab_world_13`;
- `levant_10`, `levant_13`.

The user asks for an audit of each such focus. Diplomatic preparation can reward
Syrian administrative capacity without granting a foreign agreement, investment,
mission or territory before the recipient actually consents.

## 4. Mandate choices recreate the same head of state

The initial `COLDWAR_SYR_1970_set_leader` helper unconditionally invokes
`kill_country_leader` followed by leader creation. The Atassi/Jadid mandate event
calls it for both choices even though both correctly retain Atassi's formal
presidency. Hence both options show “Atassi dies / Atassi becomes leader”.

The installed game's `documentation/effects_documentation.md:4707` confirms that
`kill_country_leader` actually removes the incumbent. Hiding that tooltip alone
does not fix the unwanted action. A mandate-only choice should update mandate
flags and programme attachments without replacing the person. Actual accession
must remain a separate guarded office change. Choice rewards should describe and
implement different policy consequences rather than repeat a generic leader
installation effect.

## 5. Event description becomes a giant option label

Both the original politics and foreign event emitters assign the event description
to `<event>.d`, then name the fourth option `<event>.d` as well (`chr(97 + index)`).
Those identifiers collide in the same localization dictionary. A later English
description override can then turn the fourth option into the full event body,
exactly matching the campaign screenshot.

Use an unambiguous option namespace such as `<event>.option_a` and keep it separate
from `.t` / `.d`. Audit every event, not only the pictured campaign. Reject
duplicate localization assignments during generation rather than relying only on
duplicate lines in final YAML: dictionary overwrites erase that evidence.

The 1970 start also bans all constitutional campaign parties. Their option
triggers hide the three actual choices and leave only the fourth cancel option.
After repairing the collision, the paid decision still needs an eligible legal
party check (and coalitions need legal/support/membership checks) to avoid charging
political power for an event with no substantive option.

## Runtime limitations

These defects are established by the user's actual screenshots, the current
generator, loaded files and installed engine documentation. This review does not
attribute the crash: the independent crash investigator must compare fresh crash
exception metadata, logs and last executed effects. A localization collision can
explain the malformed event without proving it caused a process crash.

## Independent review after the first runtime-repair build

Source checks on emitted files established:

- All 420 focus availability and implementation blocks lack a treasury-balance
  gate. Their 420 deferred resumption decisions lack one as well.
- All 332 paid focus implementation helpers retain exactly one native treasury
  charge and a `NOT <focus>_implemented` once-only guard.
- The 29 agreed entry/unlock reward amendments are present with the specified
  benefits and costs. The new outlook programme has native dynamic-modifier
  providers. Every focus retains its approved anchor, offset, prerequisite groups
  and exclusions.
- All 229 country-owned custom requirement labels have both positive and implicit
  `_NOT` localization, including the screenshot's `088259282155e6a3` requirement.
  All country-owned `$key$` substitutions resolve.
- Twelve country-owned focus/decision/effect/event files retain their complete
  parsed structure after parse/serialize/parse. The Golan goal is emitted as
  `generator = { 587 }`, preserving its bare state-ID list.
- The 40 new foreign/war events and one retained compatibility event have 73
  options in total. No option reuses an event-description key. No pair within an
  event has a literally identical executed-effect structure.

The first repair build still needed English semantic refinements. Mechanical key
coverage alone did not catch these:

- Negating only “has been funded” inside “funded and remains valid” changes an
  entire conjunction incorrectly. Composite requirements need a whole-condition
  inverse or an explicit equivalent.
- A false pending-offer flag does not prove a government “has already answered”;
  there may never have been an offer or it may have expired. Describe the absence
  of an outstanding response instead.
- “A donor must be selected before the civil-project proposal cannot be sent” is
  not the inverse of donor selection being pending. Use an explicit label for the
  actual selection state.
- Several plural group names need agreement corrections (“Communists does not
  lead”, “Armed Forces does not lead”).
- Foreign/war choices whose sole effect is a route or mandate flag need an
  explicit visible outcome. Different flag names prove different execution but
  do not themselves give a player a useful tooltip.

These findings were returned to the implementation agent before final validation.
