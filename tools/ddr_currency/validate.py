# IMPERIA CW — Cold War: ddr currency — validate.
"""Read-only static and transition checks for the DDR currency integration.

This validates script structure and a small interpreter of the actual migration
block; it does not claim to run the HOI4 engine or inspect the in-game interface.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools/israel_1970'))
from script_format import read
sys.path.insert(0, str(ROOT / 'tools/currency_balance'))
from balance_manifest import reverse_if_recorded


def direct(block, key):
    return [value for name, op, value in block if name == key and op == '=']


def one(block, key):
    found = direct(block, key)
    assert len(found) == 1, (key, len(found))
    return found[0]


def walk(block):
    for key, op, value in block:
        yield key, op, value
        if isinstance(value, list):
            yield from walk(value)


def parse(name):
    return read((ROOT / name).read_text(encoding='utf-8-sig'))


def date(value):
    return tuple(map(int, value.split('.')))


def conditions(block, state, own_trigger):
    values = []
    for key, op, value in block:
        if key.startswith('#'):
            continue
        if key == 'NOT':
            result = not conditions(value, state, own_trigger)
        elif key == 'AND':
            result = conditions(value, state, own_trigger)
        elif key == 'OR':
            result = any(conditions([item], state, own_trigger) for item in value)
        elif key == 'tag':
            result = state['tag'] == value
        elif key == 'date':
            result = {'<': state['date'] < date(value),
                      '>': state['date'] > date(value),
                      '=': state['date'] == date(value)}[op]
        elif key == 'has_country_flag':
            result = value in state['flags']
        elif key == 'has_idea':
            result = value in state['ideas']
        elif key == 'uses_own_reserve_currency':
            result = conditions(own_trigger, state, own_trigger)
        else:
            raise AssertionError(f'Unsupported condition in evaluated branch: {key}')
        values.append(result)
    return all(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-missing-icon', action='store_true')
    args = parser.parse_args()
    checks = []

    def check(value, message):
        assert value, message
        checks.append(message)

    baseline = json.loads((HERE / 'integration_baseline.json').read_text())
    # Keep the original baseline and all existing currency bytes. Only the
    # user-approved modifier block inside our added DDR law has changed.
    original_modifier = '\t\t\tmodifier = { political_power_gain = 0.05 }'
    approved_modifier = ('\t\t\tmodifier = {\n'
                         '\t\t\t\tpolitical_power_gain = 0.05\n'
                         '\t\t\t\tstability_factor = 0.02\n'
                         '\t\t\t\tinterest_rate_multiplier_modifier = -0.5\n'
                         '\t\t\t\tcustom_modifier_tooltip = ddr_mark_interest_scope_tt\n'
                         '\t\t\t}')
    old_laws = None
    for name, expected in baseline.items():
        current = reverse_if_recorded(name, (ROOT / name).read_bytes())
        # Later authorized currency-label/art work has a separate reverse-byte
        # manifest. Preserve the DDR audit's original baseline rather than
        # replacing it with hashes that silently accept unrelated changes.
        period_manifest = ROOT / 'tools/historical_currencies/changes.json'
        if period_manifest.exists():
            period_changes = json.loads(period_manifest.read_text())['files']
            if name in period_changes:
                record = period_changes[name]
                check(hashlib.sha256(current).hexdigest() == record['after_sha256'],
                      f'Authorized historical-currency changes match: {name}')
                for edit in reversed(record['edits']):
                    at, after = edit['offset_after'], edit['after'].encode()
                    check(current[at:at+len(after)] == after, 'Historical-currency edit preimage matches')
                    current = current[:at]+edit['before'].encode()+current[at+len(after):]
                check(hashlib.sha256(current).hexdigest() == record['before_sha256'],
                      'Historical-currency changes reverse exactly before the DDR audit')
        insertion_text = expected['insertion']
        if name.startswith('common/ideas/'):
            check(insertion_text.count(original_modifier) == 1,
                  'Original DDR modifier baseline is intact')
            insertion_text = insertion_text.replace(original_modifier, approved_modifier, 1)
        insertion = insertion_text.encode()
        check(current.count(insertion) == 1, f'Exactly one scoped insertion: {name}')
        restored = current.replace(insertion, b'', 1)
        check(hashlib.sha256(restored).hexdigest() == expected['sha256'],
              f'Every pre-existing byte preserved: {name}')
        if name.startswith('common/ideas/'):
            old_laws = one(one(read(restored.decode()), 'ideas'), 'reserve_currency')

    laws = one(one(parse('common/ideas/AA_law_expanded_economics.txt'), 'ideas'),
               'reserve_currency')
    mark = one(laws, 'ddr_mark')
    old_keys = [key for key, op, value in old_laws if isinstance(value, list)]
    new_keys = [key for key, op, value in laws if isinstance(value, list)]
    check(new_keys == old_keys + ['ddr_mark'], 'All existing currency keys and ordering preserved')
    check(one(mark, 'picture') == 'ddr_mark', 'Law uses the new DDR coin sprite')
    modifier = one(mark, 'modifier')
    check(dict((key, value) for key, op, value in modifier) == {
        'political_power_gain': '0.05', 'stability_factor': '0.02',
        'interest_rate_multiplier_modifier': '-0.5',
        'receiving_investment_cost_modifier': '0.10'},
        'Ostmark has the approved benefits and inbound-investment drawback')
    check('custom_modifier_tooltip' not in dict((key,value) for key,op,value in modifier),
          'Ostmark interest benefit is displayed once without a duplicate explanatory line')
    check(one(one(one(laws, 'no_foreign_reserve'), 'modifier'), 'political_power_gain') ==
          one(modifier, 'political_power_gain'), 'Existing domestic political-power bonus retained')
    interest_definition = one(parse('common/modifier_definitions/money_modifier_definitions.txt'),
                              'interest_rate_multiplier_modifier')
    check(one(interest_definition, 'value_type') == 'number', 'Interest modifier is a numeric rate adjustment')
    interest = one(parse('common/scripted_effects/00_money_system.txt'), 'calculate_interest_rate')
    addition = ('add', '=', 'modifier@interest_rate_multiplier_modifier')
    check(addition in list(walk(interest)), 'Native money calculation consumes the interest modifier additively')
    pre_clamp = next(value for key, op, value in walk(interest) if key == 'pre_clamp_interest_rate')
    check(addition in pre_clamp, 'Interest modifier contributes before the native clamp')
    rate = next(value for key, op, value in walk(interest)
                if key == 'interest_rate' and isinstance(value, list)
                and ('value', '=', 'pre_clamp_interest_rate') in value)
    bounds = one(rate, 'clamp')
    lower, upper = float(one(bounds, 'min')), float(one(bounds, 'max'))
    reduction = float(one(modifier, 'interest_rate_multiplier_modifier'))
    check((lower, upper) == (0.8, 50), 'Native minimum and maximum interest rates preserved')
    check(max(lower, min(upper, 5+reduction)) == 4.5 and
          max(lower, min(upper, 1+reduction)) == .8,
          'Half-percentage-point discount changes 5% to 4.5% and respects the 0.8% floor')
    check(('set_variable', '=', [('no_foreign_reserve', '=', '1')]) in list(walk(one(mark, 'on_add'))),
          'Adoption uses domestic debt denomination')
    check(('set_variable', '=', [('no_foreign_reserve', '=', '0')]) in list(walk(one(mark, 'on_remove'))),
          'Later foreign-currency changes restore foreign debt denomination')
    check(not any(key in ('add_to_variable', 'subtract_from_variable')
                  for key, op, value in walk(mark)),
          'DDR mark creates no international reserve adoption or issuer bonuses')

    startup = one(parse('common/scripted_effects/00_currency_effects.txt'), 'currency_startup')
    check(one(startup, 'mdcw_initialize_ddr_currency') == 'yes', 'Fresh campaigns initialize the DDR currency')
    migration = one(parse('common/scripted_effects/mdcw_ddr_currency_effects.txt'),
                    'mdcw_initialize_ddr_currency')
    branch = one(migration, 'if')
    limit = one(branch, 'limit')
    flag = one(branch, 'set_country_flag')
    own = one(parse('common/scripted_triggers/00_economic_triggers.txt'),
              'uses_own_reserve_currency')
    weekly = one(one(one(parse('common/on_actions/99_mdcw_ddr_currency_on_actions.txt'),
                         'on_actions'), 'on_weekly'), 'effect')
    check(any(key == 'mdcw_initialize_ddr_currency' and value == 'yes'
              for key, op, value in walk(weekly)), 'Existing-save migration is reachable from the weekly pulse')

    def state(tag, when):
        return {'tag': tag, 'date': date(when), 'flags': set(),
                'ideas': {'russia_rouble'}, 'variables': {'reserve_roi_bonus': .02,
                                                         'reserve_trade_bonus': .05}}

    def apply(state):
        if not conditions(limit, state, own):
            return False
        for key, op, value in branch:
            if key == 'add_ideas':
                state['ideas'].difference_update(new_keys)
                state['ideas'].add(value)
            elif key == 'set_variable':
                for var, var_op, amount in value:
                    state['variables'][var] = float(amount)
            elif key == 'calculate_reserve_roi_bonus':
                # The existing generic effect has no ddr_mark holder branch.
                check(not any(k == 'has_idea' and v == 'ddr_mark' for k, o, v in walk(
                    one(parse('common/scripted_effects/00_currency_effects.txt'), 'calculate_reserve_roi_bonus'))),
                    'Existing generic calculation clears domestic reserve returns')
                state['variables'].update(reserve_roi_bonus=0, reserve_trade_bonus=0)
            elif key == 'set_country_flag':
                state['flags'].add(value)
        return True

    for when, enabled in [('1967.12.31', False), ('1968.1.1', True), ('1970.1.1', True),
                          ('1985.1.1', True), ('1990.6.30', True), ('1990.7.1', False)]:
        sample = state('DDR', when)
        check(apply(sample) == enabled, f'Historical initialization boundary: {when}')
        if enabled:
            check(sample['ideas'] == {'ddr_mark'} and flag in sample['flags'] and
                  sample['variables'] == {'no_foreign_reserve': 1., 'reserve_roi_bonus': 0,
                                          'reserve_trade_bonus': 0},
                  f'Initial reserve law is replaced cleanly: {when}')
            check(conditions(own, sample, own), f'DDR mark is recognized as its own domestic currency: {when}')
            sample['ideas'] = {'us_dollar'}
            check(not apply(sample) and sample['ideas'] == {'us_dollar'},
                  f'Later player currency choices are preserved: {when}')
    check(not apply(state('GER', '1970.1.1')), 'West German currency remains untouched')

    sample = state('DDR', '1970.1.1')
    apply(sample)
    for currency in ['russia_rouble', 'us_dollar', 'deutsche_mark', 'no_foreign_reserve']:
        ai = one(one(laws, currency), 'ai_will_do')
        vetoes = [item for item in direct(ai, 'modifier') if ('factor', '=', '0') in item
                  and ('uses_own_reserve_currency', '=', 'yes') in item]
        check(any(conditions([item for item in veto if item[0] != 'factor'], sample, own)
                  for veto in vetoes), f'AI cannot replace DDR currency with {currency}')
    faction_hook = one(one(one(parse('common/on_actions/MD_on_actions.txt'),
                              'on_actions'), 'on_join_faction'), 'effect')
    check(any(key == 'NOT' and ('uses_own_reserve_currency', '=', 'yes') in value
              for key, op, value in walk(faction_hook) if isinstance(value, list)),
          'AI faction auto-switch respects the own-currency guard')

    sprite = one(one(parse('interface/mdcw_ddr_currency.gfx'), 'spriteTypes'), 'spriteType')
    check(one(sprite, 'name') == '"GFX_idea_ddr_mark"', 'Unique named currency sprite')
    texture = one(sprite, 'texturefile').strip('"')
    for lang in ['english', 'german']:
        payload = (ROOT / f'localisation/{lang}/mdcw_ddr_currency_l_{lang}.yml').read_bytes()
        check(payload.startswith(b'\xef\xbb\xbf'), f'{lang} localisation has a UTF-8 BOM')
        content = payload.decode('utf-8-sig')
        check(' ddr_mark: ' in content and ' ddr_mark_desc: ' in content and 'M)' in content,
              f'{lang} name and historical currency description resolve')
        check(' ddr_mark_interest_scope_tt: ' not in content and
              ' ddr_mark: "Mark der DDR (Ostmark)"' in content,
              f'{lang} Ostmark name resolves and repeated interest text is removed')

    icon = ROOT / texture
    if icon.exists():
        raw = icon.read_bytes()
        check(raw[:4] == b'DDS ' and struct.unpack_from('<II', raw, 12) == (64, 72),
              'Currency DDS matches the 72 by 64 UI canvas')
        check(struct.unpack_from('<I', raw, 88)[0] == 32 and
              struct.unpack_from('<4I', raw, 92) == (0xff0000, 0xff00, 0xff, 0xff000000),
              'Currency DDS uses an alpha-preserving BGRA pixel format')
        with Image.open(icon) as source:
            alpha = source.convert('RGBA').getchannel('A')
            check(alpha.getbbox() is not None and alpha.getextrema() == (0, 255),
                  'Currency coin has opaque artwork and transparent surroundings')
            check(all(alpha.getpixel((x, y)) == 0 for x in range(72) for y in [0, 63]) and
                  all(alpha.getpixel((x, y)) == 0 for y in range(64) for x in [0, 71]),
                  'All four outer edges are fully transparent')
    else:
        check(args.allow_missing_icon, 'Final currency icon exists')
    report = {'status': 'PASS', 'checks': checks, 'icon_verified': icon.exists(),
              'scope': 'Static scripts, migration transitions and DDS alpha; no in-game test.'}
    (HERE / 'validation_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"PASS: {len(checks)} checks; icon verified: {icon.exists()}")


if __name__ == '__main__':
    main()
