---
name: mdcw-events-decisions
description: Implement or repair IMPERIA COLD WAR events, decisions and recipient-approved agreements for 1970 multiplayer RP. Use for event routing, pending offers, transaction guards and native numeric option effects.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Events, decisions and agreement execution

Read `AGENTS.md` and [references/transactions.md](references/transactions.md). Locate the mechanic's real entry point, native country identities, decision category, event namespace, canonical emitter and existing persistent state. Preserve approved IDs and receipts unless a migration is part of the task.

Use actual native `add_namespace`, unique event IDs and a supported event/decision schema. Trace the sender and recipient through each call: `FROM` and `PREV` do not automatically mean the intended counterpart when a focus, on_action or scope loop fires an event. Preserve named targets only for their real lifetime, and guard dead countries or missing stored targets before entering them.

For agreements, keep the offered terms, pending transaction, recipient choice and execution separate. Cuban offers originate in distinct national focuses; the named RP recipient gets the real acceptance/refusal decision. Do not relocate them to a Cuban offer menu. AI behavior must respect human authority and current GC/RP policy.

Recheck eligibility, current or committed price, funds, capacity, parent/membership and replay state inside the executing transaction. Apply setup fees and one-time assets once. Any building levels need their extra shared slots in the same state and guarded transaction, with separate owner/control/capacity checks. Refusal and failed execution must leave coherent pending and payment state.

Approved standing Cuban agreements have no expiry: suspend/restore both spirits according to existence, bilateral peace, native embargo and all four mirrored sanction classes in both directions. Retain actual active parent membership; restoration repeats neither setup charges nor assets.

Show complete native numeric option effects and prospective bilateral focus effects. Descriptions remain short political context. Use actual native country-event framing, English localisation, file markers and proper encoding. Test target routing, duplicate acceptance, refusal, funds changes, suspension/restoration and rehost-sensitive state, while distinguishing model tests from observed native delivery.

Source and adaptation: [references/source.md](references/source.md).
