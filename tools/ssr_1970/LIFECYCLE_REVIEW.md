IMPERIA COLD WAR

# Lifecycle review

Read-only review of `tools/ssr_1970/lifecycle.py` and the current emitted lifecycle effects, ideas, triggers, and on-actions. No generators or game runtime were run. No lifecycle implementation files were changed.

## Findings

No concrete lifecycle defect was confirmed in the requested paths.

## Verified behavior

- The emitted tree uses 1,242 focus nodes. The lifecycle grouping code skips replacement and specialization nodes, then recalculates receipt-backed dynamic modifiers by current status, country scope, and current party trigger. Party changes call reconciliation through `on_ruling_party_change`; a daily ruling-party slot comparison provides a fallback. I found no party group mixing different tags or outlook gates.
- SSR and independent status are derived from the persistent scenario identity or accepted-admission receipt, subject status, and the recorded-transition guard. Daily checks reconcile SSR, independence, subject, and capitulation changes. The transition receipt is written once and retained for re-entry.
- Each of the nine specialization roles currently has 18 enumerated receipt sets: 17 mandate-bearing reachable combinations plus the empty set. For each set, full and legacy ideas are emitted. Reconciliation applies the full idea only while the republic is an SSR, applies the corresponding legacy idea while independent, removes all same-role variants before replacement, and removes them when neither status applies. Each specialization focus reward calls reconciliation after setting its receipt.
- The country starting-effect callbacks remove their prior reform ideas before selecting a replacement. Separate static starting/reform ideas are not included in receipt-based dynamic groups, avoiding duplicate application from those paths.
- Preparation snapshots are taken during the first transition capture and read from snapshot flags thereafter. Repair calculations use the three configured receipt groups per liability, count alternative receipts within a group once, and apply the negotiated-transition factor separately. Emitted repair previews use the same calculation for pre-transition and recorded-transition states.
- Status, party, preparation, and repair changes reach lifecycle reconciliation through the emitted callbacks. Lifecycle hooks also call market and diplomacy reconciliation; the country daily hooks target the matching republic.

## Limits

This review checked the generated script and source logic statically. It does not establish that the game engine parses every emitted effect or that a multiplayer session exercises every transition path correctly.

