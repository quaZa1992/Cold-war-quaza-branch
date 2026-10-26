# IMPERIA CW — Cold War: one source for GDP research thresholds and displayed prices.
"""Apply the GDP balance before native slot initialization and on campaign load.

No country slot counters or ongoing research are reset when loading a save.
GDP-per-capita requirements and their existing presentation remain unchanged.
Run with --check to compare the dedicated output and bounded shared patches.
"""
from decimal import Decimal
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EFFECT = 'COLDWAR_configure_research_slot_thresholds'
MARKER = '# IMPERIA CW — Cold War: GDP research thresholds follow the displayed currency scale.'
EFFECT_PATH = 'common/scripted_effects/COLDWAR_research_slot_thresholds.txt'
HOOK_PATH = 'common/on_actions/COLDWAR_research_slot_thresholds.txt'
STARTUP_PATH = 'common/scripted_effects/00_startup_effects.txt'
LOC_PATH = 'localisation/english/research_slots_l_english.yml'


def number(value):
    return format(Decimal(str(value)).normalize(), 'f')


def render():
    data = json.loads((HERE / 'balance.json').read_text(encoding='utf-8'))
    scale = Decimal(data['price_level_1970_to_2000'])
    tracks = [('gdp_slot', 'cw_research_gdp_display', data['gdp_billions_1970'])]
    assert [len(row[2]) for row in tracks] == [9]
    for _, _, values in tracks:
        assert values[0] == 0 and all(a < b for a, b in zip(values, values[1:]))
    era = (ROOT / 'common/scripted_effects/mdcw_era_reference_effects.txt').read_text(encoding='utf-8-sig')
    actual = re.search(r'@mdcw_price_level_1970_to_2000\s*=\s*([\d.]+)', era)
    assert actual and Decimal(actual[1]) == scale, 'Research and economy price scales differ'

    lines = [MARKER, f'{EFFECT} = {{', '\tif = {',
             '\t\tlimit = { IMP_is_1970_scenario = yes }']
    for runtime, display, values in tracks:
        for index, value in enumerate(values, 1):
            lines += [f'\t\tset_variable = {{ GLOBAL.{runtime}^{index} = {number(Decimal(str(value)) * scale)} }}',
                      f'\t\tset_variable = {{ GLOBAL.{display}^{index} = {number(value)} }}']
    lines += ['\t}', '\telse = {']
    for runtime, display, values in tracks:
        for index in range(1, len(values) + 1):
            lines.append(f'\t\tset_variable = {{ GLOBAL.{display}^{index} = GLOBAL.{runtime}^{index} }}')
    lines += ['\t}', '\tadd_to_variable = { global.research_screen_ui = 1 }', '}', '']
    outputs = {EFFECT_PATH: '\n'.join(lines)}
    outputs[HOOK_PATH] = ('# IMPERIA CW — Cold War: existing development thresholds and revised GDP progression.\n'
                          'on_actions = {\n\ton_startup = {\n\t\teffect = {\n'
                          '\t\t\tset_variable = { GLOBAL.gdp_c_slot^2 = 10.000 }\n'
                          '\t\t\tset_variable = { GLOBAL.gdp_c_slot^3 = 30.000 }\n'
                          '\t\t\tset_variable = { GLOBAL.gdp_c_slot^4 = 40.000 }\n'
                          f'\t\t\t{EFFECT} = yes\n\t\t}}\n\t}}\n}}\n')

    startup = (ROOT / STARTUP_PATH).read_text(encoding='utf-8-sig')
    anchor = '\tset_variable = { GLOBAL.gdp_c_slot^6 = 200.000 }'
    insertion = '\n\n\t' + MARKER + '\n\t' + EFFECT + ' = yes'
    if f'\t{EFFECT} = yes' not in startup:
        assert startup.count(anchor) == 1, 'Native threshold anchor changed'
        startup = startup.replace(anchor, anchor + insertion, 1)
    outputs[STARTUP_PATH] = startup

    loc = (ROOT / LOC_PATH).read_text(encoding='utf-8-sig')
    loc = loc.replace('GLOBAL.gdp_slot^', 'GLOBAL.cw_research_gdp_display^')
    loc = loc.replace('[?gdp_total|Y]', '[?mdcw_gdp_display|Y]')
    for anchor in (' # GUI', ' # GDP Industry Size',
                   ' gdp_gain_slot: ', ' gdp_lose_slot: '):
        offset = loc.index(anchor)
        if not loc[:offset].endswith(' ' + MARKER + '\n'):
            loc = loc[:offset] + ' ' + MARKER + '\n' + loc[offset:]
    outputs[LOC_PATH] = loc
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for relative, text in render().items():
        encoded = text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
        path = ROOT / relative
        if args.check:
            assert path.read_bytes() == encoded, 'Output differs: ' + relative
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(encoded)
    print('1970 GDP research ladder and displayed prices synchronized; development thresholds preserved.')
