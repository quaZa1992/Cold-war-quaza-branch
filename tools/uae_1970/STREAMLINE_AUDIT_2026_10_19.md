# Independent direct-focus settlement review — 19 October 2026

Reviewed the current installed UAE files after the user-authorized removal of
redundant domestic/invoice events. This audit changed only the independent test
and its report, not the generator or game implementation.

## Finding resolved during review

The first emitted `rulers_compact` focus could finish before proclamation, while
its called `accept_cabinet_bargain` helper required a formed federation. That
would stamp completion without settling the cabinet and prevent a later retry.
The root implementation added actual federation requirements to both the
compact and presidential-delegation guards. The final installed guards at
`common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt:155` and `:179`
now reject protected and independent-but-unproclaimed countries. The new test
executes both rejected cases and the valid formed-state delivery.

## Final source and transaction evidence

- Both exclusive constitutional routes now proceed through direct charter
  ratification, the chosen distribution of authority, sovereign settlement and
  proclamation. `COLDWAR_UAE_apply_charter` at
  `common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt:92` records the
  founding framework without an invoice event. The opposite focus cannot pay or
  apply after the first choice is delivered.
- The actual formation helper at
  `common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt:337` still
  requires independence, the two completed focuses and the founding framework.
  The Trucial identity persists through the sovereign-settlement focus and is
  removed only by the proclamation delivery.
- Prepare the Handover at
  `common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt:2308` grants its
  real office programme and permanently reduces inherited administration cost
  from +20% to +17%. Completing it neither requests independence nor charges a
  release fee. The earned three-point relief survives withdrawal.
- Development Fund at `COLDWAR_UAE_1970_focus_effects.txt:22` pays $0.01bn once,
  including when the treasury is negative, reduces unequal-development
  stability loss from -6% to -3%, and adds its own +3% bureaucracy contribution.
  The existing opening-focus bureaucracy contribution remains distinct.
- The cabinet focus at `COLDWAR_UAE_1970_focus_effects.txt:333` invokes the real
  helper at `COLDWAR_UAE_1970_politics_effects.txt:377`, records settlement,
  clears the crisis and requests office synchronization. The inherited
  administration relief is visible numerically and applies once.
- Republican office productivity suspends and restores with its actual party
  programme, without repeating cash or assets. Gulf Diplomacy delivers +5%
  political-power gain, -20% relations maintenance and +3% bureaucracy through
  the native dynamic modifier system.
- Removed offers have no callable sender and no generated event IDs. All 2,048
  retired delivery slots are absent. All 2,432 retained UAE contract event IDs
  resolve within the audited UAE files. The genuine British counterproposal and
  procurement confirmations remain, as do the three crisis families.
- Obsolete pending meeting flags are cleared through the actual diplomatic
  tick. Executing it twice with legacy pending state produces no event, cash,
  stockpile, XP or subject change and preserves the historical withdrawal
  schedule.

## Verification and limits

`python tools/uae_1970/test_streamline.py` passes eight independent installed-AST
groups. Results are recorded in `streamline_validation.json`. The tests execute
the actual authored guards, receipts, costs, dynamic-modifier arithmetic and
political helper guards rather than accepting descriptions as evidence.

Portrait installation and native office synchronization are explicit test
boundaries; their broader political tests remain separate. Exact HOI4 hovers,
loading, event rendering and multiplayer transport were not observed. No
remaining source blocker was found in the reviewed direct-focus integration.

## Final GCC notification cleanup

The two GCC origin-only acceptance/refusal notifications were subsequently
removed with their follow-up calls. The recipient's real admission event and
all signed membership/entry-payment effects remain. A final installed-source
scan finds no call to the retired `.1` or `.2` IDs, and every remaining GCC event
reference resolves. All eight GCC integration groups still pass, including all
six senders, refusal without charge, duplicate acceptance, concurrent invitations
and frozen bilateral entry payments.

Final authored inventory: **192 GCC admission instances + 2,432 UAE contract
instances = 2,624 delivery IDs**, representing **20 narrative/event types**.
The omitted notifications carried no assets or contractual authority; removing
them does not remove consent, membership, costs or programme rewards.
