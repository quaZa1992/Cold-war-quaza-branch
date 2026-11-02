# IMPERIA COLD WAR — France native cost-row and transaction preservation checks.
"""Check generated previews without executing any treasury or reward effect."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes

SCRIPT = ROOT / 'common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt'
LOC = ROOT / 'localisation/english/COLDWAR_FRA2_1970_l_english.yml'
BASELINE = HERE / 'COST_DISPLAY_BASELINE.json'
PREFIX = 'COLDWAR_FRA2_offer_preview_'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def nonpreview_hashes(text):
    return {n.key: digest(text[n.start:n.end]) for n in nodes(text)
            if not n.key.startswith(PREFIX)}


def main():
    text = SCRIPT.read_text(encoding='utf-8')
    if sys.argv[1:] == ['--capture-before']:
        assert not BASELINE.exists(), 'Do not replace the transaction baseline.'
        assert 'Setup expenditure:' in LOC.read_text(encoding='utf-8-sig')
        record = {'project': 'IMPERIA COLD WAR',
                  'scope': 'Pre-repair hashes of every non-preview diplomacy provider. Not an approval snapshot.',
                  'providers': nonpreview_hashes(text)}
        BASELINE.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
        print('Captured', len(record['providers']), 'unchanged transaction/lifecycle providers')
        return
    assert not sys.argv[1:], 'Only --capture-before or no arguments is supported.'
    issues = []
    def require(ok, message):
        if not ok:
            issues.append(message)
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    # The later approved foreign-policy extension adds countries to these
    # aggregates. The original 35 offer/accept/decline/reissue bodies and the
    # initialization provider must still preserve their exact transactions.
    expanded_aggregates = {'COLDWAR_FRA2_add_weekly_expenses', 'COLDWAR_FRA2_sync_treaties',
                          'COLDWAR_FRA2_cleanup_orphaned_recipient_ideas'}
    current_providers = nonpreview_hashes(text)
    design = json.loads((HERE / 'runtime_design.json').read_text(encoding='utf-8'))
    # Later explicit balance requests may alter finite reward amount/indexes in
    # named accept transactions. Prove their before AND after source, rather
    # than permitting a blanket exception to the frozen cost-row baseline.
    from diplomacy import build_diplomacy
    from deal_balance_revision import apply_deal_balance_revision
    snapshot = json.loads((HERE / 'approved_foreign_policy.json').read_text(encoding='utf-8'))
    old_source = build_diplomacy(snapshot)['files']['common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt']
    new_source = build_diplomacy(apply_deal_balance_revision(snapshot))['files']['common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt']
    old_hashes, new_hashes = nonpreview_hashes(old_source), nonpreview_hashes(new_source)
    revised = {}
    for key, before in baseline['providers'].items():
        if key in expanded_aggregates or current_providers.get(key) == before:
            continue
        require(old_hashes.get(key) == before, 'Pre-rebalance transaction does not match frozen baseline: ' + key)
        require(old_hashes.get(key) != new_hashes.get(key), 'Transaction changed outside the authorized balance revision: ' + key)
        require(current_providers.get(key) == new_hashes.get(key), 'Rebalanced transaction differs from canonical terms: ' + key)
        revised[key] = current_providers.get(key)
    preserved = {key:value for key,value in baseline['providers'].items() if key not in expanded_aggregates and key not in revised}
    require(all(current_providers.get(key) == value for key,value in preserved.items()),
            'An existing agreement transaction provider changed')
    definitions = {n.key: n for n in nodes(text)}
    loc = {}
    for line in LOC.read_text(encoding='utf-8-sig').splitlines():
        if match := re.match(r' (\S+):0 (".*")$', line):
            loc[match[1]] = json.loads(match[2])
    checked = 0
    for focus in design['nodes']:
        if 'offer' not in focus:
            continue
        key, offer = focus['key'], focus['offer']
        preview = definitions[PREFIX + key]
        for side, tag in (('france', 'FRA'), ('recipient', offer['partner'])):
            scope = next(n for n in preview.children() if n.key == tag)
            script = text[scope.start:scope.end]
            terms = offer[side]['effects']
            setup = next(e for e in terms if e['kind'] == 'treasury_gdp')
            weekly = next(e for e in terms if e['kind'] == 'weekly_gdp_expense')
            frac = Decimal(str(weekly['gdp_fraction']))
            fee = abs(Decimal(str(setup['gdp_fraction'])))
            v = f'COLDWAR_FRA2_{key}_quote_weekly_{side}'
            require(f'value = gdp_total multiply = {frac.normalize():f} divide = 52' in script, f'Own-GDP weekly quote: {key}/{side}')
            require(f'value = {v} multiply = 1000' in script, f'Display-only million conversion: {key}/{side}')
            require(f'value = gdp_total multiply = {-fee.normalize():f}' in script, f'Native GDP setup fee: {key}/{side}')
            require(script.count('modify_treasury_effect = yes') == 1, f'One native setup row: {key}/{side}')
            label = f'COLDWAR_FRA2_offer_{key}_{side}_weekly_share'
            value = loc.get(label, '')
            require(f'[?{v}_millions|R2]' in value and 'Million/week' in value, f'Native red numeric weekly cost: {key}/{side}')
            require(value.endswith('\n'), f'Separate weekly cost and next effect: {key}/{side}')
            require('setup_share' not in script, f'Duplicated setup explanation: {key}/{side}')
            checked += 1
    for value in loc.values():
        require(not any(s in value for s in ('Setup expenditure:', 'Weekly programme expenditure:', 'annual GDP / 52', 'bn/week')), 'Retired fiscal prose remains in emitted English')
    # Provider definitions are inert. All executable call sites must be inside
    # native effect_tooltip, including focus and recipient decision inspectors.
    call_sites = 0
    def inspect_calls(rows, tooltip=False):
        nonlocal call_sites
        for n in rows:
            inside = tooltip or n.key == 'effect_tooltip'
            if n.key.startswith(PREFIX) and n.value == 'yes':
                call_sites += 1
                require(inside, f'Prospective reward executes outside effect_tooltip: {n.key}')
            inspect_calls(n.children(), inside)
    for rel in ('common/national_focus/COLDWAR_FRA2_1970_focus.txt', 'common/decisions/COLDWAR_FRA2_diplomacy_decisions.txt'):
        inspect_calls(nodes((ROOT / rel).read_text(encoding='utf-8')))
    expected = 2 * sum('offer' in n for n in design['nodes'])
    require(checked == expected, 'Both participants of every agreement must show costs')
    report = {'project': 'IMPERIA COLD WAR', 'scope': 'Emitted source and numeric-display contract, not native rendering',
              'country_cost_previews': checked, 'tooltip_call_sites': call_sites,
              'unchanged_existing_providers': len(preserved),
              'authorized_balance_transactions_verified_before_and_after': sorted(revised),
              'approved_aggregate_extensions': sorted(expanded_aggregates),
              'precision': '0.01 million equals 0.00001 billion; payments and weekly streams unchanged',
              'issues': issues, 'passed': not issues}
    (HERE / 'COST_DISPLAY_CHECKS.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    assert not issues


if __name__ == '__main__':
    main()
