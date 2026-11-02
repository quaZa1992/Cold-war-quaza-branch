IMPERIA COLD WAR — German two-player sandbox

The German dossier now treats Bonn and East Berlin as independent governments. Neither country's calendar appoints a leader, opens the border, changes the other's government or orders its annexation. Elections, national policies, economic pressure and the consequences of chosen actions remain active.

## Consent and ownership

GER owns the shared climate, crisis, treaty, initiative and Unity state. Each player owns their interface state and political-power expenditure. DDR's domestic pressures and native political course remain DDR-owned.

Either government can initiate any of the nine treaties when its substantive prerequisites are met. Preparation costs the initiator 25 PP and 2 initiative. Negotiation reaching 100 does not apply the treaty. Bonn must sign; a human DDR receiving Bonn's proposal must also accept. An explicit DDR proposal carries DDR's willingness, with Bonn free to refuse. Pending proposals remain locked, can be deferred and can be reopened through Review Proposal. Effects recheck current eligibility and apply once.

Bonn can explicitly decline a ready proposal before signing. Declining frees the negotiation slot without refunding preparation, applying the treaty or adding a new penalty. Once Bonn has signed and sent the offer to DDR, the recipient resolves that pending offer. At the user's request, ordinary treaty eligibility, including the Basic Treaty, retains its existing behavior without adding a Bundestag-majority gate.

Human crisis rounds require instructions from both governments. The monthly clock waits for missing instructions. Resolution rechecks affordability before spending initiative; an invalid instruction pauses the round rather than substituting an AI answer. Current orders remain confidential until resolution. Missing Unity chapter positions also pause their round.

Unity needs five agreed chapters, all four existing powers' consent and both parliamentary ratifications. Old fast-track events cannot bypass these receipts. A confederation records cooperation between two playable states; it neither puppets DDR nor changes its faction or government, and does not prevent later Unity talks.

War requires an explicit valid order. A countdown or false alarm cannot automatically order war. A human Soviet Union is not automatically brought into the conflict. Bonn's armistice offer goes to DDR for a decision. A military settlement still requires an actual declared war and verified capitulation; if the engine has already removed DDR, the bilateral war record is simply closed without another territorial transfer or duplicate victory reward.

## Historical rails retired

- The April 1971 Honecker appointment and old GER-owned DDR leader/Wende proxies.
- The scripted crackdown-to-Wall-opening chain, Krenz/collapse sequence and one-sided Unity settlement.
- Dated Bonn political replacements and calendar-only coalition changes in the old scheduler.
- Automatic native DDR calendar mortality for human players. Paid Central Committee choices and voluntary retirement remain player-controlled; AI mortality remains available.

Legacy queued historical event IDs are hidden no-effect compatibility stubs. Two old collapse spirits are disabled, have no modifiers and are removed by startup cleanup. Startup also clears obsolete proxy variables and flags. It does not rewind either country's actual government. Border-dependent focuses and refugee systems read the native DDR border policy rather than the removed Wall/Wende outcome flags. Historical policy references remain in [DDR_RELATIONS_HISTORY.md](DDR_RELATIONS_HISTORY.md).

A separate versioned startup repair handles negotiations from before the recipient-consent system, even if the initial sandbox migration already ran. Those old negotiations were initiated by Bonn: the repair restores that sender, preserves progress and paid costs, and makes completed preparation reviewable. It grants no DDR signature or treaty effect and leaves current DDR-origin and already-signed offers alone. Unanswered armistice requests are cleared after peace, at a valid new-war start, by the existing no-war observer, and when a stale response is closed. No new recurring callback is added.

## Integration and validation

`compile_sandbox.py` compares canonical nodes, preserves unrelated live content and rejects unexpected divergence. Follow-up updates require an exact installed file hash. It writes complete temporary files before replacing native files. The broad national compiler was not run over the live mod.

Validation on 23 October 2026:

- 19 emitted-script sandbox contracts, 9 historical/policy regressions and 16 DDR dossier tests pass. The eight new contracts cover refusal, legacy negotiation recovery, preserved current offers, stale armistice state and the deliberately retained no-majority-gate behavior.
- 12 existing German security-contract tests and 5 trust-retirement tests pass.
- 106 GUI/performance checks pass, including no full presentation arithmetic for closed or AI windows.
- German content validation: 0 errors. The 31 warnings concern unscheduled retained/compatibility events and the existing average-focus-cost warning.
- Five DDR tab previews and the BRD treaty tab show no reported text overflow; nine DDR treaty rows and the footer were visually reviewed.
- Script/English localisation encoding, installed hashes and native variable-check structure pass. 1,684 pre-existing nodes outside the intended canonical changes remain identical to the task-start snapshot.
- Re-running the bounded installer reports 0 files and 0 changed nodes.

There is still one GER-owned monthly bilateral simulation. The DDR view adds no second simulation or border scan; presentation stays gated by the open human window. These are source and script-model checks, not an HOI4 multiplayer or FPS benchmark. Native event timeout behavior, UI scaling, save/reload and synchronization still need a game session. Restart HOI4 to load the changed GUI and script definitions.
