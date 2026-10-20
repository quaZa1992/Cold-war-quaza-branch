# Syria screenshot and crash investigation, 19 October 2026

Read-only investigation of the captured game run and current generated sources. No game scripts or generators were changed by this review. Source line numbers below describe the pre-repair snapshot and may move during the implementation.

## What the crash evidence proves

- Captured directory: `Documents/Paradox Interactive/Hearts of Iron IV/crashes/hoi4_20261019_100834`.
- `exception.txt`: HOI4 Operation Postern `v1.19.3.0.c01a`, crash time **2026-10-19 10:08:35**, `C0000005 (EXCEPTION_ACCESS_VIOLATION)` at instruction `0x00007FF7FB1B45C6`.
- The minidump's exception stream independently records two exception parameters: access operation **0 (read)**, fault memory address **0x68**. This establishes a near-null pointer read in the game engine. It does not identify a particular script as its cause.
- `meta.yml`: only listed mod is **MD Cold War**, `IsOldSave: false`, release Windows 64-bit build. The crash folder date is local Berlin time (`+0200`).
- The stack has only generic exported names such as `PHYSFS_swapULE64` with very large offsets. These are not reliable function names for diagnosing the failing subsystem. There are no usable debug symbols/source frames in the captured stack.
- Live `game.log` ends at **10:08:34 / 1970.06.13.04**, with Chad's debt-default decision. The latest Syrian focus log was **10:08:27 / 1970.06.03.01**, `COLDWAR_SYR_opening_settlement`. The last logged command is not proof of crash causality.
- The most recent runtime entries in `error.log` are Algeria's undefined poacher variables and zero-weight `random_list`, last repeated at **10:08:25 / 1970.06.01.01**. These identify separate defects; no source evidence connects them to this access violation.

**Conclusion:** a game-engine near-null read is confirmed. The available stack/logs do not establish the exact gameplay/script trigger. A claim that a specific Syrian event definitively caused this crash would exceed the evidence. Repair the confirmed defects below and obtain a fresh run/log before claiming the crash is resolved.

## Confirmed Syrian parser defect in this same run

The crash-captured `logs/error.log` lines **464–465** and **578–579** report the same error at **09:57:56** and **09:58:02**:

```
Malformed token: _bare, near line: 23
Malformed token: =, near line: 23
common/scripted_effects/COLDWAR_SYR_foreign_effects.txt near line: 25
```

The loaded source line **23** contains:

```
generator = { _bare = 587 }
```

This is invalid syntax for a war-goal state list. The authored `tools/syria_1970/foreign.py` uses the valid bare list `generator = { 587 }`. The later presentation rewrite corrupts it: `validate_content.py:55` represents a bare list token as the internal AST tuple `('_bare', '=', '587')`, and `decision_presentation.py:60` serializes that tuple as a normal assignment. Preserve bare tokens when serializing and reject internal sentinel names in loaded output. The crash is not proven to originate from this parser error, but this is an actual engine-rejected Syrian defect and must be fixed.

## Screenshot 1: negative prerequisite localization

`common/decisions/COLDWAR_SYR_politics_decisions.txt:87–93` places a custom tooltip inside `NOT`:

```
NOT = {
    custom_trigger_tooltip = {
        tooltip = COLDWAR_SYR_requirement_088259282155e6a3
        has_country_flag = COLDWAR_SYR_dual_command_resolved
    }
}
```

The base localization exists at `localisation/english/COLDWAR_SYR_decision_requirements_l_english.yml:11`; its negative variant does not. The screenshot displays the engine-requested `_NOT` key. Native MD localization uses explicit negative keys, for example `MD_country_politics_view_l_english.yml:158`, `party_is_in_power_or_coalition_TT_NOT`. Check custom requirement labels in both positive and negative presentation contexts, including nested conditions; key existence in the positive context alone is insufficient.

## Screenshot 4: identical leadership tooltips

`tools/syria_1970/politics.py:317` makes `COLDWAR_SYR_1970_set_leader` unconditionally clear flags, execute `kill_country_leader`, synchronize outlook, then create a leader. The emitted setter begins at `common/scripted_effects/COLDWAR_SYR_politics_effects.txt:133`.

Both options in event `COLDWAR_SYR_POL.3` call that setter while `baath_head = 0`. They change the authority variable, but both then kill and recreate Nureddin al-Atassi. The screenshot's “Atassi dies / Atassi becomes leader” tooltip therefore follows the actual source. Atassi-versus-Jadid authority is meant to differ from the formal presidency; it should not rebuild an unchanged president. Keep any required synchronization and bookkeeping hidden, avoid repeated leader creation when office has not changed, and expose the actual distinct policy consequences of the choice. Audit every event option through helper expansion rather than comparing only labels.

No immediate setter recursion was established by tracing the current dispatcher, `update_set_politics`, programme refresh, and weekly hooks. Repeated leader recreation remains a confirmed gameplay/presentation defect, not an established explanation for the access violation.

## Screenshot 5: event body and fourth option share a localization key

`politics.py:140` assigns the event description to `.d`; `politics.py:143` assigns lettered option names `.a`, `.b`, `.c`, `.d`, etc. Thus option four collides with the description. English UI overrides can make either the event body become a short option or the fourth button become the entire description.

The six affected emitted domestic events are **POL.1, POL.6, POL.20, POL.23, POL.24, POL.27**. Example source anchors:

- `events/COLDWAR_SYR_politics_events.txt:514`: description `COLDWAR_SYR_POL.20.d`.
- Same file **574**: fourth option also named `COLDWAR_SYR_POL.20.d`.
- `localisation/english/COLDWAR_SYR_politics_l_english.yml:25`: that key contains the long campaign narrative shown on the oversized button in screenshot 5.

The foreign event emitter uses the same `.d` description convention. An independent parse of all **69** country/news events in the emitted `COLDWAR_SYR*.txt` files found two further collisions: **COLDWAR_SYR_FOREIGN.7** and **COLDWAR_SYR_FOREIGN.20**, for **eight** total collisions across the new content. Use a description suffix that cannot collide with lettered options, update corresponding overrides, and assert description/title/option key disjointness in all emitted events. The missing campaign effect in screenshot 5 is consistent with the player hovering the **cancel** option whose label was overwritten by the body text; cancellation genuinely grants no party support. Do not invent a reward for cancellation to mask the collision.

## Separate non-Syrian errors in the captured run

The same startup log also contains Israeli trigger names rejected by this engine, China focus effect tokens, Greek scalar dynamic-modifier removal, Cyprus `YUG` scopes, Northern Cyprus/Turkish runtime `recruit_character` warnings, and several scripted GUI `context_type` tokens. These are useful separate audits but are not confirmed causes of this crash and should not be silently bundled into a Syria repair.

## Validation requirements after repair

1. Assert emitted Clausewitz bare lists round-trip without `_bare` sentinels.
2. Assert unique event body/title/option localization keys, plus resolved positive and negative custom trigger labels.
3. Compare actual helper-expanded option effects; hide bookkeeping and do not kill/recreate an unchanged head of state.
4. Restart HOI4 fully and inspect fresh `error.log`, event UI, campaign/cancel effects, and progression past June 1970. Static checks alone cannot establish that this access violation is gone.
