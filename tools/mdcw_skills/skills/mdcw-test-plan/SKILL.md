---
name: mdcw-test-plan
description: Build a concrete 1970 playthrough and multiplayer rehearsal plan for specified IMPERIA COLD WAR changes. Use when test steps or a validation plan are requested; the plan itself is not evidence that checks passed.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Playthrough and multiplayer test plans

Read `AGENTS.md`. Resolve the requested mechanics, current diff or commits, real native country tags and 1 January 1970 setup. A named mechanic remains testable on `main` even without commits ahead of `origin/main`. Include only relevant systems and do not invent issue numbers.

Group tests by scenario and participating countries. Give each check an initial state, concrete action, exact observable expected result and evidence to capture. Use checklist items for steps still to run. Keep proposed, executed, passed, failed and unverified states separate.

Cover startup and actual reachability before using console shortcuts. Forced focus completion or injected flags can test an effect but cannot prove its normal prerequisite path. For costs, record starting and resulting treasury, debt, weekly stream, assets and spirit values rather than merely checking that a popup appears.

For multiplayer mechanics include identical build/checksum, two independent human countries, co-op if relevant, simultaneous actions, duplicate clicks, recipient acceptance/refusal, insufficient funds, target changes, sanctions/war, cancellation, save/reload and rehost. Exercise at least the relevant weekly pulses and January/February boundary when testing recurring systems. Never use `tag` switching or destructive console injection in a live RP session; keep setup commands in an isolated test save.

For bilateral programmes verify pending offers, exact event delivery, previews before acceptance, actual paired effects, replay protection, suspension, restoration and no repeated setup rewards. For GUI minigames verify invalid buttons cannot mutate state and closed views do not trigger expensive display refreshes.

Separate source checks, Python model checks, native single-client checks and genuine network tests. Use available native tools when the task authorizes running them; do not inherit upstream's assumption that the agent can never launch the game. Do not attach a plan to a PR or contact testers unless that action was requested or already authorized.

Source and adaptation: [references/source.md](references/source.md).
