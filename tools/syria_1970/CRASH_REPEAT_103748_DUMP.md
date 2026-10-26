# Repeated crash dump comparison, 19 October 2026

Read-only examination of `hoi4_20261019_103748`, compared with `hoi4_20261019_100834`. No game was launched and no loaded script was changed by this investigation. Times below use the Berlin timestamps recorded by the game.

## Confirmed repeated signature

Both `exception.txt` files and independently decoded minidump exception streams record the same failure:

| Evidence | First run | Repeated run |
| --- | --- | --- |
| Engine | Operation Postern v1.19.3.0.c01a | Same build |
| Crash time | 10:08:35 | 10:37:49 |
| Exception | `C0000005`, read access violation | Same |
| Instruction | `hoi4.exe+0x11a45c6` | Same |
| Read address | `0x68` | Same |
| RCX / RAX | `0` / `0` | Same |
| Instruction bytes | `80 79 68 00` | Same |
| Decoded instruction | `cmp byte ptr [rcx+0x68], 0` | Same |
| First eight reported stack frames | Identical exported-name offsets | Identical |

This is the same null-pointer failure, not merely another crash with the same generic exception code. The repeated run includes two additional pairs of nested frames farther down the stack. Their presence alone does not prove script recursion or identify the originating helper.

The executable's loaded base was `0x7ff7fa010000` in both dumps. Module-relative offsets above avoid relying on that incidental process address. The generic `PHYSFS_swapULE64` names printed by the crash reporter are distant exported-symbol labels and do not identify the actual failing subsystem.

## New diagnostic evidence: politics effect presentation

The dump contains two especially useful object/string observations in **both** crashes:

- `RSI` points to the live string **`Politics will change:\n`**. The installed game's `localisation/english/effects_l_english.yml:195` identifies this exact text as **`EFFECT_SET_POLITICS`**.
- `RBX` points to an object with vtable `hoi4.exe+0x293c900`. Decoding the MSVC RTTI CompleteObjectLocator and TypeDescriptor from the installed executable identifies it as **`.?AV?$TNullObject@VCIdeologyGroup@@V1@@@`**, a null `CIdeologyGroup` object.
- `R12` points to an object with vtable `hoi4.exe+0x271b710`. Its RTTI is **`.?AVCScriptedEffectTemplate@@`**.
- The immediate caller at `hoi4.exe+0x3a0b61` calls the function beginning at `hoi4.exe+0x11a45c0`; the return address is `+0x3a0b66`. This matches the captured stack and fault instruction.

These observations materially narrow the failure to a native politics-effect description/ideology lookup reached through a scripted effect template. They provide substantially stronger evidence than the last gameplay log line. They do **not** preserve a scripted helper name or the UI element being hovered, so they do not independently prove which `set_politics` block was expanded.

Before repair, a concrete suspect in the current Syria source is:

```
COLDWAR_SYR_accept_national_pact = {
    ...
    set_politics = { elections_allowed = yes election_frequency = 48 }
    ...
}
```

The declaration omits `ruling_party`. The current emitted source places it in `common/scripted_effects/COLDWAR_SYR_politics_effects.txt` around line 78. Treat line anchors as a pre-repair snapshot because generation may move them. The helper has event and deferred-programme callers; the exact crash route must be traced through all exposed reward descriptions, including branches the player cannot presently execute. Native MD's `set_elections_with_frequency` helper in `00_MD_politicsview_scripted_effects.txt` around lines 2168–2178 supplies `ruling_party = ROOT` while preserving the current government. A repair should follow a verified native form rather than mapping MD party-array index `7` into an engine ideology token.

The safe isolation target is therefore an exposed politics helper with an absent/invalid engine ideology, not a wholesale disablement of Syrian content or UN events. Check both the actual effect and its tooltip expansion. Merely hiding a broken native effect would not establish correct execution.

## Timeline and limits of the logs

The crash package contains `error.log`, `system.log` and `code_revisions.log`; it does **not** contain `game.log`. The live `Documents/Paradox Interactive/Hearts of Iron IV/logs/game.log` has a matching final timestamp of **10:37:48**, so it is usable for this run while that file remains unchanged.

Relevant Syrian progression in that live log:

| Wall time | In-game time | Recorded action |
| --- | --- | --- |
| 10:35:05 | 1970.01.21.01 | `COLDWAR_SYR_opening_entry` |
| 10:35:47 | 1970.02.25.01 | `COLDWAR_SYR_opening_military` |
| 10:36:32 | 1970.03.18.01 | `COLDWAR_SYR_opening_corrective` |
| 10:36:55 | 1970.04.22.01 | `COLDWAR_SYR_opening_settlement` |
| 10:37:34 | 1970.05.13.01 | `COLDWAR_SYR_outlooks_western` |
| 10:37:48 | 1970.06.01.02 | Syria abstains from General Assembly vote type 6 |

The first crash's prior investigation recorded the last live log action at **1970.06.13.04**, Chad's debt-default decision. That older live `game.log` is now overwritten; its observation is retained in `CRASH_REVIEW_20261019.md`. The differing dates and final country actions argue against asserting one fixed monthly tick or the last UN vote as the cause. Tooltips can be evaluated while simulation advances and need not produce their own gameplay log entry.

The repeated captured `error.log` contains **no `COLDWAR_SYR` or `_bare` entries**. The previously repaired malformed war-goal list is therefore absent from this run's parser errors, yet the identical crash returned. Its repair was necessary but did not eliminate this failure. The newest error entries remain Algeria's undefined poacher variables and zero-total random list at June 1; they do not identify the politics null-object failure.

The two metadata files have different content checksums (`fe79ccb60c496f4548e98773b1cd019a` versus `dffe6e21a757795891396d9077368da6`), matching an intervening content change. Both identify only **MD Cold War** as the active mod and `IsOldSave: false`.

## Concrete repair and verification target

1. Enumerate every reachable `set_politics` block behind Syria's focuses, decisions, event options and deferred programmes. Ensure engine ideology/country references resolve; MD party-array values and engine ideology identifiers are different APIs.
2. Repair the confirmed incomplete declaration through the canonical generator. Preserve election frequency, existing governing outlook and native party/election bookkeeping.
3. Keep pure visible consequences separate from internal leader/party refresh calls. Check helper-expanded display paths even when a trigger would currently fail; the engine must still be able to describe the option.
4. Add a source regression for absent/invalid politics references in generated Syria scripts and any added repair helper. Do not substitute a Python model test for an engine test.
5. Restart the game, open/hover the same Syrian decisions and event options, then advance beyond both June 1 and June 13. A fresh dump, if any, can be compared against the exact instruction, access address and RTTI signature above. Only that new run can establish that the runtime failure is gone.

Reproduction support: `inspect_repeat_dump.py` reads both supplied dumps, parses the minidump streams, registers, raw captured memory and the installed executable's PE sections, and resolves the two RTTI objects. `repeat_dump_details.json` is its retained diagnostic output. PE fallback data is read from the installed executable; heap contents and exception registers come from each respective dump. No debugger symbols or downloads were used.
