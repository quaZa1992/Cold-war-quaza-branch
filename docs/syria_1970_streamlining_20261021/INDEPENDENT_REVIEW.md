# Independent Syria streamlining review

Scope: `tools/syria_1970/streamlining.py`, `streamlining_build.py`, applicable compiler helpers, and actual isolated output returned by `streamlining_build.generate()`. Review is against the archived loaded country code in `before.zip`, not an older fork's integration baseline. No gameplay code was edited by this reviewer.

## Verified source properties

- All **420** native focus positions, relative anchors, grouped prerequisites, exclusions and focus durations match the archived loaded focus tree exactly.
- Every generated `COLDWAR_SYR_*` event reference resolves in the current generated event registry.
- Automatic proposal helpers retain their original live sender/target/pending-state guards. Their original paid-decision failure/refund branch is excluded, preventing free focus requests from generating political power refunds.
- Actual lender/recipient event options retain recipient-controlled responses and guarded payment/debt effects. No automatic government replacement, territory transfer or war declaration was introduced by proposal dispatch.
- Normal focus rewards retain the original once-only implementation signature and full native treasury deduction without a positive-treasury eligibility veto.
- Modifier updates are signed old-to-new deltas into accumulated programme variables. Existing backing variables are preserved, and missing new variables are initialized separately. Recovery does not call a focus implementation to replay construction or cash.
- Party, office-holder and coalition programme attachment remains controlled by the existing group guards. Returning authority reattaches stored values rather than rerunning material focus awards.
- The isolated builder avoids shared politics/history patching, modern-tree retirement and whole-mod encoding normalization. It writes country files only after source-hash preflight.

## Findings reported during implementation

1. **Old saves stranded at the opening settlement.** Initially migration omitted officer backing and the command/corrective agreement flags, while their former decisions were removed. An already-completed opening route without its old accepted event could never reach the settlement. Root has changed recovery to restore these agreement/backing outcomes without installing a head of state. Preserve the actual current mandate and do not reset greater officer backing.

2. **Unanswered one-off proposals blocked the shared retry channel.** The automatic helper initially copied `<decision>_completed` at dispatch, plus its `NOT completed` guard. This consumed friendship, pipeline, Lebanese, Iranian and several other offers merely on sending, even after refusal or expiry. Proposal completion must instead depend on actual pending/accepted/current-agreement state; one-time project delivery guards still belong at delivery.

3. **Preparation bonuses can trigger premature campaign cleanup.** Reserve and depot focuses now grant temporary operation ideas before the appropriation focus establishes `operational_mandate`. The existing weekly cleanup treats those ideas as an active campaign and clears both them and `operations_funded` when there is no mandate. That erases the paid budget and can strand the appropriation focus. Preparation activation, mandate timing and cleanup must be aligned before install.

4. **Legacy Front implementation needs a surviving provider.** New completion of `baath_02` calls `enact_front`, but the first migration only applied its modifier delta. Removing the old `front_offer` menu then left an old, previously unratified Front without its promised domestic legalization/cooperation provider. Use a current-Baath guarded compatibility enactment or a reachable surviving domestic agreement path.

5. **Two transfer decisions need explicit reward accounting.** Removing subsidy review must consciously map the targeted-relief/restraint outcomes into `fiscal_13/14`, rather than silently discarding them. The formerly free `opening_military` now grants two backing stages whereas the old officer bargain paid for each stage; the new compact's financing must be a deliberate recorded balance choice, not justified by a nonexistent existing focus appropriation.

6. **The installed-tree renderer initially still indexed deleted decisions.** `render_preview.py` iterated all original manifest decision IDs, then indexed actual installed definitions. Filter to actual definitions, adding shared campaign/coalition/retry entries, so the faithful preview remains usable after removing old menus.

7. **Weekly pipeline transition should credit a still-paid old interval.** A save can still hold `pipeline_payment_month` from a paid 30-day interval. Honor that timed legacy flag until expiry before starting new weekly charges; all new contract terms and actual transfers remain weekly.

## Deliberate limits

This is bounded source and emitted-output review. It does not establish HOI4 loading, exact native tooltip rendering, native economic tick behavior, save/reload or live multiplayer synchronization. New doctrine instruction in the reward overlay is a new-completion one-time reward; if existing completed focuses are intentionally not awarded that new supplement, disclose that compatibility policy.

The reward overlay revises 22 named focuses. It is not a claim that all 420 reward bundles or all pre-existing bureaucracy costs were rebalanced.

## Final emitted-output recheck

All findings above have been addressed in the current source and independently regenerated output:

- Implemented old opening routes receive their missing compact/backing/transition flags without installing a president. Recovery does not lower officer backing already above two.
- Proposal dispatch no longer consumes the old sender-completion receipt, and its former completion guard no longer blocks refused/expired proposals. Real pending and recipient/contract delivery guards remain.
- Reserve, forward-depot and medical preparation are standing focus programme modifiers with their own continuing burdens. They no longer create pre-mandate temporary operation ideas that would trigger premature cleanup. Their matching old timed ideas are explicitly removed during signed conversion, preventing transitional double stacking.
- One live operational-cabinet decision authorizes a genuinely valid campaign, credits an existing appropriation and charges 0.75% GDP only when renewing expired funding. Its meaningful campaign requirement has a player-facing caption.
- Existing Baath Front programmes receive a current-Baath guarded cooperation enactment. This admits eligible partners through the native domestic coalition and preserves the incumbent.
- The existing officer bargain is now the military opening focus's explicit $2 billion native charge. The two subsidy focuses directly grant their respective former temporary packages.
- Manifest decision metadata indexes actual retained definitions, including new shared entries, so the unchanged renderer no longer looks up deleted decisions.
- The weekly pipeline payer honors an unexpired old `pipeline_payment_month` interval before beginning new weekly payments. Both sides transfer the same $0.00093 billion.

Independent assertions on the final emitted snapshot passed for all 420 positions/anchors/prerequisite groups/exclusions/durations, all own event references, actual decision metadata, three old timed-package replacements, the old paid pipeline interval, absence of treasury/building/training/leader/foreign-event replay in migration, and removal of sender-completion guards from all automatic proposals.

Final inventory: **29 regular decision definitions including two counterparty withdrawal controls; 44 event definitions, of which 16 are hidden cleanup/crisis callbacks; 25 focus modifier dictionaries changed**. The 22-entry reward overlay plus three standing Golan service packages explain that last count. No unresolved material issue remains within this bounded source recheck. HOI4 engine, exact UI and live multiplayer tests remain outside this evidence.
