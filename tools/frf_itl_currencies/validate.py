# IMPERIA COLD WAR — Validate French/Italian law availability, lifecycle, history and euro conversion.
"""Exercise emitted source and preserve earlier edits; no HOI4 engine is emulated."""
from pathlib import Path
import hashlib
import json
import re
import struct
import sys
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first, walk
from extension_manifest import reverse_extension, reverse_realignment_extension


def source(name):
    # IMPERIA COLD WAR — Audit this earlier extension beneath recorded paid-switch additions.
    data = reverse_realignment_extension(name, (ROOT / name).read_bytes())
    return parse(data.decode('utf-8-sig'))


def enabled(rows, state):
    def condition(key, op, value):
        if key == 'OR':
            return any(enabled([row], state) for row in value)
        if key in ('AND', 'limit'):
            return enabled(value, state)
        if key == 'NOT':
            return not enabled(value, state)
        if key == 'tag':
            return state['tag'] == value
        if key == 'has_idea':
            return value in state['ideas']
        if key == 'has_country_flag':
            return value in state['flags']
        if key == 'COLDWAR_UAE_1970_campaign':
            return False
        raise AssertionError(('Unsupported condition', key))
    return all(condition(*row) for row in rows)


def main():
    checks = []
    def check(value, message):
        assert value, message
        checks.append(message)
    changes = json.loads((HERE / 'changes.json').read_text(encoding='utf-8'))
    for name, record in changes['files'].items():
        before = reverse_extension(name, (ROOT / name).read_bytes())
        check(hashlib.sha256(before).hexdigest() == record['before_sha256'], 'Exact insertion reversal: ' + name)
        check(all(not edit['before'] for edit in record['edits']), 'Existing bytes were not replaced: ' + name)
    own = first(source('common/scripted_triggers/00_economic_triggers.txt'), 'uses_own_reserve_currency')
    laws = first(first(source('common/ideas/COLDWAR_FRF_ITL_currencies.txt'), 'ideas'), 'reserve_currency')
    euro = first(source('common/scripted_effects/99_eu_scripted_effects.txt'), 'joining_the_euro')
    core = first(source('common/scripted_effects/00_currency_effects.txt'), 'calculate_reserve_roi_bonus')
    issuer = first(source('common/scripted_triggers/00_economic_triggers.txt'), 'is_reserve_currency_issuer')
    for currency, tag in [('french_franc', 'FRA'), ('italian_lira', 'ITA')]:
        law = first(laws, currency)
        state = {'tag': tag, 'ideas': {currency}, 'flags': set()}
        check(enabled(first(law, 'visible'), state) and enabled(first(law, 'available'), state), currency + ': domestic availability')
        check(enabled(own, state), currency + ': recognised as own currency')
        check(not enabled(issuer, state), currency + ': no fabricated reserve issuer status')
        for foreign_tag in ('USA', 'GER', 'DDR', 'FRA' if tag == 'ITA' else 'ITA'):
            other = dict(state, tag=foreign_tag)
            check(not enabled(first(law, 'available'), other), currency + ': foreign government excluded: ' + foreign_tag)
        state['flags'].add('EU_joined_the_eurozone')
        check(not enabled(first(law, 'available'), state), currency + ': blocked after actual euro adoption')
        check(first(law, 'cost') == '50', currency + ': base adoption price')
        check(first(first(law, 'modifier'), 'political_power_gain') == '0.05'
              and first(first(law, 'modifier'), 'receiving_investment_cost_modifier') == '0.05', currency + ': generic domestic-law balance')
        for hook, expected in [('on_add', '1'), ('on_remove', '0')]:
            body = first(first(law, hook), 'hidden_effect')
            check(first(first(body, 'set_variable'), 'no_foreign_reserve') == expected, currency + ': domestic flag lifecycle: ' + hook)
            check(first(body, 'calculate_reserve_roi_bonus') == 'yes', currency + ': derived reserve effects refreshed: ' + hook)
            check(not any(key in ('add_to_variable', 'set_country_flag') for key, op, value in walk(body)), currency + ': no reserve network receipt: ' + hook)
        check(not any(key == 'has_idea' and value == currency for key, op, value in walk(core)), currency + ': no international network return invented')
        branches = [node for key, op, node in euro if key == 'if' and first(node, 'limit') == [('has_idea', '=', currency)]]
        check(len(branches) == 1, currency + ': exactly one euro conversion')
        check(first(branches[0], 'swap_ideas') == [('remove_idea', '=', currency), ('add_idea', '=', 'euro')], currency + ': actual adoption replaces the national currency')
        state = {'tag': tag, 'ideas': {currency}, 'flags': set()}
        for key, op, node in euro:
            if key == 'set_country_flag':
                state['flags'].add(node)
            elif key == 'if' and enabled(first(node, 'limit'), state):
                swap = first(node, 'swap_ideas')
                state['ideas'].discard(first(swap, 'remove_idea'))
                state['ideas'].add(first(swap, 'add_idea'))
        check(state['ideas'] == {'euro'}, currency + ': euro conversion has no leftover domestic law')
        history = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        parsed = parse(history.read_text(encoding='utf-8-sig'))
        for when in ('1970.1.1', '1985.1.1'):
            dated = first(parsed, when)
            check(dated.count(('add_ideas', '=', currency)) == 1, currency + ': default in ' + when)
            check(('set_variable', '=', [('no_foreign_reserve', '=', '1')]) in dated, currency + ': history initializes monetary variables in ' + when)
    assets = json.loads((HERE / 'asset_manifest.json').read_text(encoding='utf-8'))['assets']
    for name, record in assets.items():
        data = (ROOT / record['texture']).read_bytes()
        check(hashlib.sha256(data).hexdigest() == record['texture_sha256'], name + ': texture hash')
        check(hashlib.sha256((ROOT / record['source']).read_bytes()).hexdigest() == record['source_sha256'], name + ': original generated master retained')
        check(struct.unpack_from('<4I', data, 92) == (0xff0000, 0xff00, 0xff, 0xff000000), name + ': native BGRA storage')
        im = Image.open(ROOT / record['texture']).convert('RGBA')
        check(im.size == (72, 64) and im.getchannel('A').getextrema() == (0, 255), name + ': transparent native footprint')
        check(all(im.getpixel(point)[3] == 0 for point in [(0, 0), (71, 0), (0, 63), (71, 63)]), name + ': clear outer corners')
    for path in [ROOT / 'common/ideas/COLDWAR_FRF_ITL_currencies.txt', ROOT / 'interface/COLDWAR_FRF_ITL_currencies.gfx']:
        check(not path.read_bytes().startswith(b'\xef\xbb\xbf'), 'Script/GFX without BOM: ' + path.name)
    loc = ROOT / 'localisation/english/COLDWAR_FRF_ITL_currencies_l_english.yml'
    check(loc.read_bytes().startswith(b'\xef\xbb\xbf'), 'English localisation with BOM')
    labels = dict(re.findall(r'^ (\w+): "(.*)"$', loc.read_text(encoding='utf-8-sig'), re.M))
    check(labels['french_franc'] == 'French Franc' and labels['italian_lira'] == 'Italian Lira', 'English monetary identities')
    (HERE / 'validation.json').write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'passed': True,
        'checks': checks, 'engine_tested': False}, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(checks)} currency-law, lifecycle, history, asset and preservation checks.')


if __name__ == '__main__':
    main()
