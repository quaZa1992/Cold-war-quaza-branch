# UAE political event audit

Read-only review of the installed politics providers and domestic political events, 19 October 2026. No game-code changes.

## Confirmed finding

**P2 — Cabinet acceptance can remain selectable after its actual authority condition expires.**

`tools/uae_1970/diplomacy.py:343` builds the cabinet acceptance option with no `COLDWAR_UAE_constitutional_crisis` condition, but the nested execution guard requires that flag. `domestic_event` at lines 292–304 constructs its round authority without `domestic_extra` (which includes the crisis condition at line 346). If a player opens the cabinet dialogue and then completes the mediation settlement before choosing, mediation clears the crisis. The cabinet acceptance option still passes its displayed trigger, consumes the pending meeting flag, and executes no cabinet settlement. The expired-dialogue fallback also remains unavailable because the broader meeting authority remains valid.

Recommended correction: include crisis state in the cabinet round authority, so stale offers show the existing concluded-meeting option; at minimum align the acceptance option trigger with the execution guard. Add a regression opening cabinet, resolving mediation, then trying the old cabinet popup.

## Design consistency question

Cabinet acceptance leaves `COLDWAR_UAE_constitutional_crisis` set (`diplomacy.py:343`, `politics.py:285–290`), while mediation explicitly clears it (`diplomacy.py:323–325`). Consequently the mediation settlement remains available after a successful cabinet bargain. If the bargain is meant to resolve the same federal dispute, clear the crisis atomically and test both mutually outstanding dialogues. If it is deliberately a distinct administrative settlement, explain that distinction in lore rather than claiming a resolved constitutional crisis. This is a design interpretation, not a confirmed engine failure.

## Reviewed behaviour with no defect found

- History supplies the Council identity, native Western autocracy and Trucial cosmetic directly.
- Federation requires independent status, earned union/proclamation and founders' consent; date expiry cannot create it.
- Founders' two accepted choices write distinct flags consumed by mutually exclusive guarantees/mandate focus availability. They are not equivalent no-op options.
- Political programmes follow exact native party slots. Government loss does not forcibly restore the historical party.
- Constitutional convention changes native election/ban data without forcing a preferred winner or 100% support.
- Monarchy office restoration retains presidency; cabinet office is separate. Death/succession dates prevent perpetual Rashid resurrection.
- Local meetings use immutable round IDs, current-party checks and pending flags, preventing old accepted choices from replaying transactions or replacing newer settlements.
- Reserve release consumes recorded principal; negotiation rejection options intentionally do not pay/grant benefits.
- Supported party names and English localisation providers resolve through the native registry.

## Validation run

`python tools/uae_1970/test_politics.py`: 18 groups passed.

`python tools/uae_1970/test_diplomacy.py`: 19 cases passed; 4,480 emitted event instances.

These are generated-AST/source checks. They do not establish native UI presentation, actual multiplayer popup delivery, or engine load/save correctness. The stale cabinet interleaving above is absent from the passing cases.
