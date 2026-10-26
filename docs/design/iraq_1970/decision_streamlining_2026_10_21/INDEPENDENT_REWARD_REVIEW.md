# Independent reward and presentation review

Reviewed 2026-10-21 before installation. This is a source review of the initial streamlining implementation, not an HOI4 engine test. Findings were sent to the implementing agent for correction; they must be rechecked against the final emitted snapshot.

## Required corrections identified

1. `front_guarantees` is absent from the legacy-upgrade candidates because it has no hook. Its additional 1% GDP appropriation is therefore not charged to a completed v3 save, although the new permanent productivity and social-cost modifiers activate.
2. Existing v3 saves already possess `reward_v3_current`. The programme compiler therefore activates streamlining's revised permanent modifiers before the separate streamlining appropriation has been funded. A separate entitlement must control old/new permanent packages.
3. A v2 save's existing v3 migration calculates the price increase using the newly overlaid total, including streamlining additions. The later streamlining upgrade charges its own increase over the captured v3 share again. The two migration paths need explicit credit or separated pricing.
4. The single-target automatic-offer transform drops the selected option's trigger. Those triggers contain country existence, peace, pending-offer and accepted-offer checks that the outer decision helper does not duplicate. Keep the original option trigger around the inlined action.
5. The normal pending-delivery preview omits the streamlining hook preview. The new streamlining upgrade mixes an explicit hook preview with an unhidden executing helper, rather than using the existing preview-plus-hidden-execution grammar. Costs, remaining material components and reforms should use one consistent preview.
6. Amnesty, legalization, Front and transition hooks add `COLDWAR_IRQ_civil_rights_cost`, but their descriptive preview does not expose the idea's +3% bureaucracy cost and -4% drift defence. Show its native idea effect beside the political description.
7. New upgrade descriptions refer to recorded annual GDP, while `invoice(q, delta)` freezes live GDP at the first streamlining quote. Use the recorded historical basis where intended or describe the actual basis accurately.

## Editorial corrections identified

The initial retained event set still exposes generic implementation prose. International acceptance options say “deliver the guarded transaction”; their descriptions discuss invoices, native debt, replay and recipient-owned rechecks. Rewrite these as short proposals specific to the actual agreement, retaining numeric costs and rewards in native option effects.

Other retained examples include leadership events `.193` and `.213` referring to the native leader provider and programme reconciliation, election event `.165` discussing MD party arrays, and outlook-organizing events `.542`, `.548`, `.553` and `.558` discussing native inputs and normalization. These need concise political descriptions.

## Verified elements

- The 13 authored streamlining overrides preserve their existing army experience, research grants and focus durations. Three pre-existing research grants remain single grants. Only `foreign_kuwait` adds a structured offices building.
- New-focus completion calls the local or negotiation hook after successful implementation. The hook's own receipt prevents repeat command-power, readiness and negotiation dispatch through reconciliation.
- Amnesty retains living-candidate and date checks; Front formation uses the actual governing-party coalition array. No candidate resurrection was found in the reviewed payloads.
- Basra offices use the existing structured building, ownership, control, capacity and component-receipt pipeline.
- The new institutional focus descriptions use English political and economic language. Normal MD references support their reward shapes: Iraqi officer experience/command power, Iraqi office construction, Iranian labour institutions and Soviet staff training.

Final emitted-output verification and an engine hover/save/reload test remain outstanding at this review stage.

## Corrected-source recheck

The corrected source now includes every revised focus in the separate upgrade list, preserves the captured pre-streamlining modifiers until its own receipt, separates the original v2-to-v3 price increase from the new appropriation, wraps inlined sender actions in their original option trigger, exposes the political-guarantee idea, includes hook previews in ordinary pending deliveries, and hides executing legacy upgrade helpers. The additional review finding that legacy previews showed already-delivered experience and instruction has also been corrected by using the receipt-sensitive delivery preview.

The amnesty credit now considers Dukhayl release, Rikabi rehabilitation and protected Dawa cadres. The old prisoner-review implementation did not preserve a unique durable payment receipt, so exact historical payment cannot be reconstructed. Crediting the already-delivered protection outcomes avoids charging again for a completed outcome, with the acknowledged possibility of forgiving a small historical fee where a different political path had produced protection.

One migration timing issue remains in the source reviewed at this point: an old v2 save can receive the newly added Basra offices component through its ordinary v3 upgrade before paying the separate streamlining appropriation. Its v2-to-v3 bill is 1% GDP, while the separate streamlining bill is another 2% GDP; the office is already part of the v3 payload. Its component receipt prevents duplication, but the new asset needs to be deferred until the associated additional funding is committed, or the appropriations must be settled atomically with explicit credit.

The retained-event editorial rewrite has been completed in `decisions_module.py`; pure in-memory generation passes. No engine behaviour is asserted by this recheck.

## Final source verification

The remaining Basra office timing issue is corrected. `reward_overhaul.delivery(..., defer_streamlined=True)` is used for the old v3 upgrade's actual delivery and native preview. Both omit the newly authored office and its component receipt. Normal new-focus delivery and the separately funded streamlining supplement use ordinary delivery, which retains the office and its one-time receipt.

Read-only assertions confirmed that all 426 captured original GDP shares exactly match the actual reward code in `before.zip`, whose SHA-256 also matches the baseline's recorded hash. All 426 captured modifier dictionaries exactly match `current_design.json` before installation. The historical shares and modifier fallback therefore describe the same pre-streamlining design snapshot rather than an inferred catalogue price.

Direct payload assertions also confirmed that the deferred old-upgrade actual and preview contain neither the offices construction nor its receipt, while ordinary actual and prospective delivery retain construction. The previously reported source defects are resolved in the final source reviewed here. No additional material mechanics regression was identified within this bounded recheck. Installation and HOI4 engine testing were not performed by this reviewer.
