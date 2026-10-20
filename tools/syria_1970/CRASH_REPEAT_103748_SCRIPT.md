# Repeat crash 10:37:48: Syrian script audit

Read-only review of crash `hoi4_20261019_103748`, compared with
`hoi4_20261019_100834`. The audit changed no loaded game files or generators.
It applies the installed `mdcw-modifier-audit` skill and distinguishes source
evidence from engine causality.

## Captured evidence

- Both `exception.txt` files identify HOI4 `v1.19.3.0.c01a` and
  `C0000005` at instruction `0x00007FF7FB1B45C6`.
- The new stack shares its first seven application frames and nearly all its
  remaining frame offsets with the earlier crash. The new stack has one extra
  repeated pair of frames (`+3434569`, `+18472713`). Generic exported names do
  not identify the subsystem reliably without disassembly or symbols.
- The new captured `error.log` contains 718 lines, versus 719 in the earlier
  capture. Removing wall-clock and game-date prefixes yields four removed
  distinct patterns and one added pattern. The only added pattern is the
  database diagnostic's aggregate `93 errors` count. It is not a new script
  defect.
- The earlier malformed `_bare`/`=` war-goal-state-list errors are absent from
  the new log. A case-insensitive search for `COLDWAR_SYR`, `Syria` or `SYR`
  returns no line in the new captured error log. This establishes that the
  known Syrian parser defect was removed; it does not establish that all
  Syrian runtime behavior is safe.
- The live `logs/game.log`, last written at the crash time, ends at
  **1970.06.01.02**, when Syria abstains from a UN General Assembly vote of
  type 6. The prior review recorded the older game log ending at
  **1970.06.13.04**. Therefore the crashes are not tied to the same game date
  or simply the same last logged decision.

## Syrian path reached in this run

The matching live game log records:

| Game date | Completed focus |
| --- | --- |
| 1970.01.21.01 | `COLDWAR_SYR_opening_entry` |
| 1970.02.25.01 | `COLDWAR_SYR_opening_military` |
| 1970.03.18.01 | `COLDWAR_SYR_opening_corrective` |
| 1970.04.22.01 | `COLDWAR_SYR_opening_settlement` |
| 1970.05.13.01 | `COLDWAR_SYR_outlooks_western` |

Those five helpers grant variables/flags, attach earned dynamic modifiers,
clear the divided-command penalty at settlement and expose the relevant
decisions. They do not execute an Israel war goal, foreign contract, building
scope or later Cold War succession event. The limited-war goal helper is
therefore not a demonstrated active trigger of this crash.

## Initialization, weekly and leadership trace

Current source anchors:

- `common/on_actions/COLDWAR_SYR_1970_on_actions.txt:2`: startup enters the
  existing `SYR` country scope after checking `country_exists = SYR`;
  `on_weekly` invokes a helper whose first operation checks Syrian country
  identity and the 1970 scenario; government changes only refresh programmes.
- `common/scripted_effects/COLDWAR_SYR_programme_effects.txt:3658`:
  initialization has a once-only flag, invokes politics/foreign initialization,
  runs a once-only entry-reward migration, conditionally loads the intended
  tree and refreshes programmes. Weekly flow is at line 3680.
- `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:153`: the leader
  dispatcher synchronizes MD politics, sets programme-ownership flags, and
  only retires/creates a head of state when `has_country_leader` does not
  match the requested name. Atassi/Jadid mandate-only event `POL.3` calls
  `COLDWAR_SYR_sync_baath_mandate`, which creates/retires no character.
- `common/scripted_effects/00_leader_setup_scripted_effects.txt:9`: the native
  dispatcher intercepts Syria before its modern generic kill/create branch.
  `update_set_politics` at line 73 changes the actual outlook and party name;
  it does not call back into `set_leader`.
- `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:579`: weekly
  politics checks cabinet contracts; the death/incapacity branches are gated
  after 1982/1983, and the unrest branch by 1980 or a specific discriminatory
  settlement. The crop-crisis event requires the agriculture entry focus,
  absent from the five logged focuses above.
- `common/scripted_effects/COLDWAR_SYR_foreign_effects.txt:58`: weekly
  foreign flow recalculates three GDP-based amounts and checks already-active
  country contracts. Later Iranian supply and hard-currency crisis branches
  are date-gated. No new foreign programme is logged as implemented here.
- `common/scripted_effects/COLDWAR_SYR_programme_effects.txt:347`: refresh
  only attaches/removes native dynamic modifiers according to their earned
  flags and ownership gates, fills missing numeric variables and recalculates
  starting-spirit values. Its add/remove operations do not create a direct
  scripted-effect recursion.

No immediate cycle was found among initialization, migration, the leader
dispatcher, native `update_set_politics`, programme refresh and weekly hooks.
The global native politics GUI contains no Syrian scripted-GUI blocks or
Syrian event-target dereferences. Syria's added party-name localization
branches use country identity/scenario checks and plain localization keys.

## Native politics-tooltip candidate identified after dump inspection

The parent investigation subsequently reported that both minidumps retain the
native tooltip text **`Politics will change:`**, corresponding to
`EFFECT_SET_POLITICS`. This materially narrows the source audit. It is stronger
evidence than the final UN vote or Algeria error-log entry.

An AST scan of all `set_politics` blocks in loaded common decisions, scripted
effects, scripted GUIs, national focuses and events finds exactly **three**
blocks lacking `ruling_party`:

1. `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:78`,
   `COLDWAR_SYR_accept_national_pact`:
   `set_politics = { elections_allowed = yes election_frequency = 48 }`.
2. `SPR_1970_hold_first_free_elections` in
   `common/scripted_effects/SPR_1970_scripted_effects.txt`: elections enabled,
   frequency 48 and last election 1977.6.15.
3. `SPR_1970_install_felipe_gonzalez_government` in the same Spanish file:
   elections enabled, frequency 48 and last election 1982.10.28.

The Spanish calls come from hidden immediate events for their later historical
transitions, whereas Syria's pact is reachable immediately from the player's
decision list. The Syrian helper is reached from event `POL.4` option A
(`events/COLDWAR_SYR_politics_events.txt:242`) and `POL.34` option A (line 1572).
Both real invocations are under `hidden_effect`; the authored material
`effect_tooltip` blocks do not call the helper. No other Syrian focus preview,
decision or event emits a direct `set_politics` block. A hidden wrapper alone
therefore must not be treated as proof that the native tooltip code can never
visit or prepare that effect.

There is an exact native MD counterpart for changing election settings while
retaining the outlook: `ruling_party = ROOT`. In the main MD reference,
`common/scripted_effects/00_MD_politicsview_scripted_effects.txt` uses it in
`set_elections_with_frequency` at line 2175, and in
`enable_elections_with_no_leader_change` at line 2339. The local native helper
has the same pattern. Supplying that supported current-country argument in
the Syrian pact preserves its intended governing outlook while avoiding an
omitted ideology pointer during native politics description. Source of the
Syrian omission: `tools/syria_1970/politics.py:412`.

This is the specific targeted repair candidate supported jointly by the native
tooltip evidence and the source scan. Binary inspection must establish the
faulting object/type before stating exact causality; a fresh run still needs
to verify the corrected hover/event interaction.

## Continuing unrelated engine diagnostics

The new run logs no unknown Syrian effect/trigger or Syrian invalid scope.
Current war-goal syntax is `generator = { 587 }`; dynamic-modifier removal is
the block form `remove_dynamic_modifier = { modifier = ID }`. Neither earlier
argument-form defect is present in this capture. A parser-clean load does not
exclude the omitted `ruling_party` argument in the native tooltip candidate
above.

The log still confirms three **global startup scope defects**, unrelated to a
specific Syrian call:

1. `common/on_actions/00_on_actions.txt:1991` invokes
   `mdcw1970_initialize_personnel` with provided scope `None`.
2. That path evaluates the `IMP_is_1970_scenario` country trigger with
   provided scope `None`.
3. `common/on_actions/zz_IMP_cold_war_military_industrial_complex_on_actions.txt:13`
   invokes `IMP_cold_war_initialize_military_industrial_complex` with provided
   scope `None`.

The engine explicitly accepts the identifiers but rejects their invocation
scope. These are valid repair candidates; the log does not connect them to
the later near-null read. Other continuing errors include Greek decision
`allowed` use of `exists`, Israeli unsupported trigger names, Cyprus `YUG`
scopes, Algeria's uninitialized poacher chances, and trait AI commands. Their
continued presence is not proof that the final log entry caused the crash.

## Conclusion

The prior malformed Syrian war-goal-state-list error is demonstrably absent,
yet the same engine fault recurs on a different date. No new Syrian parser
failure or immediate helper recursion is established by this review. The
native politics-tooltip clue narrows the targeted repair to the election-only
`set_politics` call lacking the native MD `ruling_party = ROOT` argument.
Calling the crash fixed based solely on another static PASS would be
unwarranted. A fresh game run past the failure is still required after any
targeted runtime repair.
