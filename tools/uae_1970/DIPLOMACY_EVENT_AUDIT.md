# UAE diplomacy and event audit

Read-only audit of the currently emitted UAE agreement events, decisions and
providers,2026-10-19. No game code was changed by this review. Findings below
describe the inspected pre-fix revision; later fixes need separate regression
evidence. Native HOI4 UI and multiplayer delivery were not tested.

## Confirmed defects

### D1: an old procurement quotation can cancel a newer round

Priority:P2. Canonical source `tools/uae_1970/diplomacy.py:610` creates the
buyer's decline option as an unconditional call to
`COLDWAR_UAE_close_procurement_offer`. The helper clears the sender's current
pending/awaiting flags and starts a180-day cooldown without identifying which
quotation was declined. Unlike the neighbouring British and Iranian
counterproposal declines, this option does not check its immutable event round.
The first emitted instance is `events/COLDWAR_UAE_1970_contracts.txt:199893`,
event `.90001`, option1. All128 buyer quotations have the same omission.

Executed reproduction using the existing generated-AST harness:

```python
import sys
sys.path.insert(0, 'tools/uae_1970')
import test_diplomacy as d
w = d.World()
w.earn('air_coastal_shield')
w.targets['COLDWAR_UAE_contract_recipient'] = 'FRA'
w.call('send_procurement_offer')
w.choose()                         # seller quotes round1
old_quote = w.events[-1]           # .90001, UAE
w.day = 61
w.call('british_tick')             # expire and close round1
w.day = 242
w.call('send_procurement_offer')   # round2, seller event .11002
assert w.has('UAE', d.P + 'offer_pending_procurement')
w.choose(*old_quote, option=1)     # decline old buyer popup
assert not w.has('UAE', d.P + 'offer_pending_procurement')
assert not w.has('UAE', d.P + 'offer_awaiting_procurement')
assert w.has('UAE', d.P + 'offer_cooldown_procurement')
```

Observed: round2 pending/awaiting changed from true to false; its new cooldown
became true. No money transfer was required. The existing19-case test passes
because it tests stale acceptance and duplicate purchase, not stale buyer
decline. Recommended fix: bind closure to the matching current round and
pending quotation, and make an expired old popup harmless. Do not replace
immutable round identity with a mutable shared event target.

### D2: the old UAE charter bypasses the new common GCC admission rules

Priority:P2. Both `COLDWAR_UAE_decision_gcc` and the new common
`COLDWAR_GCC_charter_decision` are installed. The old decision still dispatches
`COLDWAR_UAE_send_gcc_offer`. Its acceptance guard at
`tools/uae_1970/diplomacy.py:513` checks payment and existing membership but
does not check recipient sovereignty or `recently_expelled_from_gcc`.
Compare `common/scripted_triggers/COLDWAR_GCC_1970.txt:15` and the common
sender/recipient guards in `tools/gcc_1970/compile.py:183`.

Loaded anchors: old decision
`common/decisions/COLDWAR_UAE_1970_decisions.txt:2255`, old sender trigger
`common/scripted_triggers/COLDWAR_UAE_1970_diplomacy.txt:177`, first old
acceptance event `events/COLDWAR_UAE_1970_contracts.txt:233348` (`.14001`).

Executed old/new comparison:

```python
# Import UAE test_diplomacy as old and load GCC test_integration as new.
class ProtectedWorld(old.World):
    def cond(self, key, op, value, country, root, prev, state):
        if key == 'is_subject' and country == 'QAT':
            return value == 'yes'
        return super().cond(key, op, value, country, root, prev, state)

w = ProtectedWorld()
w.subject = None                   # independent UAE
w.earn('gulf_cooperation')
w.targets['COLDWAR_UAE_contract_recipient'] = 'QAT'
w.call('send_gcc_offer')
event = w.events[-1]               # .14001, QAT
# QAT is protected; the old actual option trigger nevertheless returns true.
w.choose(*event)
assert 'idea_gcc_member_state' in w.c['QAT']['ideas']
assert 'idea_gcc_member_state' in w.c['UAE']['ideas']

v = new.World()
v.c['QAT']['subject'] = True
assert v.send('UAE', 'QAT') == []   # common path rejects protected target
v = new.World()
event, = v.send('UAE', 'QAT')       # target independent when sent
v.c['QAT']['subject'] = True
option = new.values(new.EVENTS[event[0]], 'option')[0]
assert not v.test(new.first(option, 'trigger'), 'QAT')
assert 'idea_gcc_member_state' not in v.c['QAT']['ideas']
```

Observed: the old path accepts protected Qatar; the new path rejects it both
at dispatch and if protection begins before acceptance. Recently expelled
recipients have the analogous missing guard in the old source. The common
path and legacy path also expose separate rounds and two similarly named
decisions. Recommended fix: retain compatibility but route/hide the obsolete
UI path and guard old pending popups consistently. Hiding the old decision
alone does not invalidate an already open old acceptance popup.

### D4: delegated-powers acceptance has no enacted constitutional effect

Priority:P2. `diplomacy.py:332` / event `.113001` accepts delegated powers
after the50PP decision. It sets `delegated_powers_accepted`, sets
`executive_delegated`, adds a modifier-free status idea and refreshes
programmes. Searching all loaded `common` and `events` files finds no policy,
focus-availability or office consumer for these flags:

- `delegated_powers_accepted` occurs only in this event family and the
  decision's repeat guard.
- `executive_delegated` occurs only in this event family and the status idea's
  cancellation condition.

Executed reproduction: `World(); earn('presidential_union');
click('delegation'); choose()` accepts event `.113001`. The acceptance flag
and cosmetic status idea appear, but dynamic modifiers remain empty, Army
experience remains0 and treasury remains10. Static consumer tracing confirms
there is no delegated-power availability benefit outside this harness either.
Thus this is a missing implementation of the approved decision summary,
"Acceptance activates the constitutional change", rather than a hidden
working effect. Implement a real negotiated authority change or accurately
redesign the decision as a roleplay status; do not merely add a numerical
tooltip that claims an effect absent from execution.

## Presentation findings

### D3: important internal bargains lack focused outcome previews

Priority:P2 presentation, not proof that gameplay effects are absent.

- Founders' Settlement: `diplomacy.py:312`, event `.110001`. Options0/1 only
  set/clear settlement flags and reconcile programmes. There is no explicit
  native unlock preview identifying the mutually exclusive focus enabled:
  Emirate Guarantees versus A Stronger Mandate. These are future branch
  permissions, not immediate numerical gifts.
- Federal Dispute and Crown and Property: `diplomacy.py:322`, events `.111001`
  and `.112001`. The invoice executes, while the remedy is only communicated
  through a flag and the broad programme refresh. A concise marginal native
  spirit preview should accompany the payment.
- Delegation of Federal Powers: seeD4. No direct modifier or future policy
  permission exists in the inspected loaded code, so presentation alone
  cannot fix this acceptance.
- Cabinet Bargain: `diplomacy.py:342`, event `.114001`. Its provider changes
  the actual cabinet and adds its bureaucracy burden. Preview the actual
  office outcome and marginal spirit changes rather than the entire country.

These event actions call `COLDWAR_UAE_refresh_programmes` directly. That
provider (`common/scripted_effects/COLDWAR_UAE_1970_programmes.txt:2`) contains
the full dynamic-modifier reconciliation, without an event-side hidden effect.
Consequently source alone cannot establish a clean marginal tooltip; broad
replacement effects may be exposed. Live hover rendering is unverified. The
appropriate correction is the existing focus presentation pattern: explicit
nonexecuting native outcome previews, hidden authoritative execution, and
only necessary text for genuine branch/institution permissions.

Some diplomacy agreements intentionally record roleplay status only. Islands
arbitration and the Saudi border accord add named status spirits/flags but no
territory, oil transfer, automatic war or cash. That is their current actual
effect, not evidence of a broken transfer. If stronger game incentives are
wanted, their values require a deliberate design change.

## Checks that passed

- `python tools/uae_1970/test_diplomacy.py`:19 focused cases passed.
-4,480 declared UAE contract events,4,480 distinct actual nested event calls;
  no unresolved call and no unreferenced event ID in this owned output set.
- The4,480 events are35 dialogue/transaction templates with128 never-reused
  rounds each:20 bilateral families,12 domestic meeting families and3 buyer/
  counterproposal confirmation families. They are not4,480 different stories.
- Existing checks execute automatic British release, treaty-version races,
  shared policy locks, exact/insufficient funds, recipient-owned grants,
  duplicate-proof transfers, interrupted courses, reserve conservation, port
  control/capacity, own-GDP GCC fees, native OPEC delegation, domestic authority
  loss, Kuwait access and both British/Iranian counterproposal confirmations.

Scope: owned UAE diplomacy/decision/event code and the interacting common GCC
admission guards. This is not an exhaustive engine or other-country event
audit. No claim is made that every remaining source or live-game bug is absent.
