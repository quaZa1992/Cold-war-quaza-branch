"""Stage one reviewed runtime reference, then install only with explicit access."""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
TARGET = Path('C:/Users/sonyz/.codex/skills/mdcw-national-trees/references/runtime-presentation.md')
STAGE = HERE/'skill_updates_runtime'
LESSONS = '''
## Further engine evidence: decisions, events and generated lists

The next Syrian game run exposed these concrete cases. Reconfirm the native API in the installed version rather than treating static key coverage as an engine test.

- Native `custom_trigger_tooltip`/`custom_override_tooltip` implicitly requests `tooltip_key_NOT` in a negated context; the documented explicit alternative is `not_tooltip`. Check both forms, including nested NOT/OR. A positive key alone does not localize its inverse. Write a truthful inverse of the whole predicate: absence of a pending offer includes never-sent and expired offers and does not prove that a government answered. Negating only one clause of a funded-and-valid condition misstates its logic.
- Event title, description and option localization namespaces must be disjoint. Using `.d` for the description and the fourth lettered option overwrote one with the other. A safe convention is `.t`, `.d`, `.option_a` etc. Compare emitted keys, not just dictionary counts, and check every option against its own actual outcome. Cancellation should clearly say that nothing changes; it does not need a fabricated reward.
- Mandate/party-authority choices need not change the formal head of state. Do not call a destructive leader setter just to refresh policy flags. Preserve an unchanged incumbent; use a supported retirement/transfer API only for an actual replacement. Hiding a kill-and-recreate sequence fixes neither its historical meaning nor execution. Expose distinct party/leader programme ownership when that is the real choice.
- Clausewitz bare lists are data, not key assignments. The Syrian writer corrupted `generator = { 587 }` into `generator = { _bare = 587 }`. Parser sentinel names must never reach loaded script. Check raw output for `_bare`/`_list` assignments as well as round trips: a permissive AST can represent the sentinel assignment and a bare token identically, so round-trip equality alone can miss this defect. Validate argument shapes against the native effect documentation and actual engine errors.
- Follow the native budget path before adding affordability gates or custom debt. In this project, `modify_treasury_effect` permits a negative treasury and the existing budget tick runs `automated_debt_taker`. The user explicitly removed positive-cash gates from Syrian focuses while retaining their once-only expenditure. Do not charge the same shortfall directly as debt again. This focus-specific instruction does not remove a donor's or a bilateral contract's separate funding requirement.
- The user subsequently required material benefits for all Syrian entries previously rewarding only branch continuation or decision access. Record these authorized amendments separately from the original spatial design; give each an actual supported reward and plausible burden. Preserve earned rewards and geometry. This does not authorize arbitrary buffs to other countries or a tooltip pretending to grant a modifier.

A recorded engine access violation with an unsymbolized stack does not identify a script cause. Distinguish confirmed parser/UI/gameplay defects from an unproven crash hypothesis, retain the captured run, and require a fresh run before claiming the crash is resolved.
'''

POLITICS_LESSONS = '''
## Politics effects and repeated native crashes

- Supply a valid engine ideology to `set_politics`, even when changing only election settings. MD's numerical `ruling_party` variable is a subparty-array index, not the engine's ideology argument. Native MD's `set_elections_with_frequency` and `enable_elections_with_no_leader_change` use `ruling_party = ROOT` with a surrounding `no_leader_change` flag. Reuse that pattern when ROOT is the intended governing country; verify callers' scopes and retain the required frequency. Do not replace the current outlook with a hard-coded ideology just to enable elections.
- Validate the body of a helper even if every known caller uses `hidden_effect`. Concealing internal politics bookkeeping does not repair a missing native argument. Check generated definitions and shared providers, not only the visible option's direct effect list. Include regressions that reject an omitted ideology, a numerical party index and a subideology in the engine-group field.
- A last `game.log` entry does not identify a crash cause. Repeated Syrian dumps showed the same native fault, the localized `Politics will change` string and a null `CIdeologyGroup` object, narrowing the investigation to politics-effect presentation. Saved source metadata may strengthen attribution only after calibration against several independently identified objects. Keep uncaptured strings and runtime uncertainty explicit; repairing the matching malformed effect still requires a fresh HOI4 run before declaring the crash resolved.
'''

BORROWING_LESSONS = '''
## State expenditure and borrowing: all countries

The user's rule applies to every country when authoring or changing content: own state expenditure in focuses, decisions and their linked event options must not require a positive treasury or a minimum cash balance. Keep the actual payment through native `modify_treasury_effect`; it may leave treasury negative. The existing MD budget tick converts the deficit into debt through `automated_debt_taker`, including its native fees. Do not add the same shortfall to debt again or turn the removed gate into a free reward.

Trace the whole transaction. Remove an affordability check from availability and from later completion/acceptance guards where both belong to the country's own payment. Handle shorthand `check_variable = { treasury > ... }` and verbose `check_variable = { var = treasury value = ... compare = greater_than_or_equals }`. Retain meaningful political, ownership, consent, once-only and timing conditions, and validate a GDP-based charge so zero or invalid GDP cannot grant free benefits. Player-facing text must describe the charge truthfully without claiming that cash on hand is required.

Do not erase every treasury comparison: low-balance crisis triggers, debt repayment, reserved project money and contractual counterparty settlement serve other mechanics. Trace payer, recipient and funding source before changing those conditions. A rule for future country work is not authorization to rewrite every existing tree or another country's contracts in the current task.

Verify representative transactions from zero and negative balances: eligibility, the real deduction, later resolution and repeat protection. Preserve the cost amount and payment timing unless the user requests changing them. Static checks establish these source contracts; they do not replace a live budget-tick test.
'''

if '--politics' in sys.argv:
    STAGE = HERE/'skill_updates_politics'
    LESSONS = POLITICS_LESSONS
if '--decision-borrowing' in sys.argv:
    STAGE = HERE/'skill_updates_decision_borrowing'
    LESSONS = BORROWING_LESSONS

if '--install' not in sys.argv:
    raw = TARGET.read_bytes()
    text = raw.decode('utf-8-sig')
    heading = next(line for line in LESSONS.splitlines() if line.startswith('## '))
    assert heading not in text
    if '--decision-borrowing' in sys.argv:
        previous_rule = next(line for line in text.splitlines() if line.startswith('- Follow the native budget path before adding affordability gates or custom debt.'))
        text = text.replace(previous_rule, '- Follow the native budget path before adding affordability gates or custom debt. The user extended the earlier Syrian focus rule to own spending in decisions and linked event options, for every country prospectively. See "State expenditure and borrowing: all countries" below for the current rule and transaction boundaries.', 1)
    STAGE.mkdir(parents=True, exist_ok=True)
    (STAGE/'runtime-presentation.md').write_text(text.rstrip()+'\n'+LESSONS, encoding='utf-8', newline='\n')
    (STAGE/'previous.md').write_bytes(raw)
    (STAGE/'manifest.json').write_text(json.dumps({'target': str(TARGET), 'previous_sha256': hashlib.sha256(raw).hexdigest()}, indent=2), encoding='utf-8')
    print('Staged one reference; original metadata, policy and other skills unchanged.')
else:
    manifest = json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
    staged = (STAGE/'runtime-presentation.md').read_bytes()
    current = TARGET.read_bytes()
    assert str(TARGET) == manifest['target']
    assert current == staged or hashlib.sha256(current).hexdigest() == manifest['previous_sha256']
    TARGET.write_bytes(staged)
    assert TARGET.read_bytes() == staged
    print('Installed and byte-verified the single reviewed runtime reference.')
