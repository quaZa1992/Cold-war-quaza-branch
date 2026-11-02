---
name: mdcw-scripted-gui
description: Build or repair native MD scripted GUIs for IMPERIA COLD WAR mechanics and minigames, including scopes, list entries, invalidation, click safety and donor geometry. Use for in-game GUI work rather than web previews or national-focus coordinates.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Native mechanic interfaces

Read `AGENTS.md` and [references/gui-contract.md](references/gui-contract.md). Trace the full live donor window, scripted GUI, localisation, GFX, data provider, execution effect and owning generator. Inspect neighbours, child names, entry widths, slot limits, positions and conditional variants; isolated keyword-matched hunks do not prove a complete port.

Resolve actual context scope and parent attachment. For dynamic lists distinguish numeric indices, type IDs and country/state scopes; verify the first and last row and the empty-list case. Use current MD templates and engine documentation rather than assuming every property from modern upstream exists here.

Match enabled/visible state to real requirements, then recheck authoritative eligibility inside the gameplay effect. A disabled button, hidden window or GUI-local selection is not a transaction guard. Keep display-only calculation and preview state separate from persistent gameplay receipts, money and rewards.

Invalidate views when their actual data changes. Avoid clock-bound dirty variables and full country/state scans in frequently evaluated properties. Gate costly display refreshes on the relevant open human view without suppressing updates that originate from an AI or another country. Measure operation counts with explicit context; they are not FPS or native timing.

Preserve native typography, chroming, icon classes and complete frames. Country-event pictures require the live MD donor frame, its photo viewport and neighbouring option geometry, not merely a registered news sprite. Existing measured dimensions are a reference to recheck, not a permanent engine constant. Preserve frame and alpha pixels and record image provenance.

Check close/reopen, selection changes, empty/full lists, co-op, concurrent actions, stale entries and save/reload. Verify any required AI access using supported current mechanisms rather than a blanket claim about GUI capability. Label composed previews and distinguish them from live game evidence. Do not change global fonts or unrelated windows to hide local layout problems.

Source and adaptation: [references/source.md](references/source.md).
