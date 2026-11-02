# IMPERIA COLD WAR — Native German programme payment and lifecycle checks.
"""Private country-scoped fixture uses exact emitted completion bodies.

The private histories withhold reactor/chip research to test real missing-tech
states. No user history, playset, save, or live multiplayer session is changed.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'docs/german_reward_revision_20261027'
GAME = Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
PROFILE = Path('E:/HOI4_Mod_Tools/mdcoldwar/runtime/german_reward_revision_20261027/native') / time.strftime('%Y%m%d_%H%M%S')
MARK = '# IMPERIA COLD WAR — Private German programme test fixture.\n'
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk, emit
from programme_assets import coalesce, building_limits, technology_limits

CHECKS = []
CASES = [
    ('GER', 'social_market', .002, None, ''),
    ('GER', 'nuclear_buildout', .005, 'reactor1', ''),
    ('DDR', 'energy_brown_coal_from_lusatia', .0135, None, ''),
    ('DDR', 'mit_the_microelectronics_resolution', .0222, 'microchip_production_3',
     'set_variable = { ruling_party = 4 } set_country_flag = COLDWAR_DDR_first_sec_mit'),
]


def check(name, condition):
    CHECKS.append(name)
    return f'if = {{ limit = {{ {condition} }} log = "COLDWAR_GR_PROBE PASS {name}" }} else = {{ log = "COLDWAR_GR_PROBE FAIL {name}" }}\n'


def near(variable, expected):
    return f'check_variable = {{ {variable} > {expected-.0001:.5f} }} check_variable = {{ {variable} < {expected+.0001:.5f} }}'


def trees():
    return {tag: {first(node, 'id'): node for node in values(first(parse(
        (ROOT / f'common/national_focus/COLDWAR_{tag}_1970_focus.txt').read_text(encoding='utf-8')), 'focus_tree'), 'focus')}
        for tag in ('GER', 'DDR')}


def fixture():
    nodes = trees()
    events = [MARK, 'add_namespace = COLDWAR_GR_PROBE']
    helpers = [MARK]
    triggers = [MARK]
    records = []
    by_country = {'GER': '', 'DDR': ''}
    for index, (tag, key, fraction, technology, prepare) in enumerate(CASES, 1):
        identifier = ('COLDWAR_GER_1970_' if tag == 'GER' else 'COLDWAR_DDR_') + key
        node = nodes[tag][identifier]
        reward = first(node, 'completion_reward')
        preview = first(reward, 'effect_tooltip', [])
        # Prospective native building entries are explicit in each selected focus.
        assets = []
        for state, operator, body in walk(preview):
            if state.isdigit() and isinstance(body, list):
                assets.extend((int(state), first(grant, 'type'), int(first(grant, 'level')))
                              for grant in values(body, 'add_building_construction'))
        assets = coalesce(assets)
        assert assets, identifier
        receipt = (identifier + '_reward_receipt' if tag == 'GER'
                   else 'COLDWAR_DDR_R_20261027_' + key)
        call, can = f'COLDWAR_GR_fixture_run_{index}', f'COLDWAR_GR_fixture_can_{index}'
        # This wrapper contains the exact loaded completion code, including its
        # real hidden transaction and any integrated physical-grant wrapper.
        helpers.append(call + ' = {\n' + emit(reward) + '\n}')
        triggers.append(can + ' = {\n' + emit(first(node, 'available', [])) + '\n}')
        code = prepare + '\nset_variable = { gdp_total = 100 }\nset_variable = { treasury = 0 }\n'
        for state, building, level in assets:
            code += f'{state} = {{ add_extra_state_shared_building_slots = 80 set_building_level = {{ type = {building} level = 0 }} }}\n'

        def snapshot():
            return '\n'.join(f'{state} = {{ set_variable = {{ COLDWAR_GR_before_{index}_{building} = building_level@{building} }} }}'
                             for state, building, level in assets) + '\n'

        def unchanged():
            return ' '.join(f'{state} = {{ check_variable = {{ building_level@{building} = COLDWAR_GR_before_{index}_{building} }} }}'
                            for state, building, level in assets)

        untouched = f'NOT = {{ has_country_flag = {receipt} }} ' + near('treasury', 0)
        if technology:
            code += snapshot()
            code += check(key + '_missing_tech_is_real', 'NOT = { has_tech = ' + technology + ' }')
            code += check(key + '_missing_tech_blocks', 'NOT = { ' + can + ' = yes }')
            code += call + ' = yes\n'
            code += check(key + '_missing_tech_no_partial_payment', untouched + ' ' + unchanged())
            if 'microchip' in technology:
                code += 'set_technology = { microchip_production_1 = 1 }\n'
                code += check(key + '_tier_one_insufficient_for_two', 'NOT = { ' + can + ' = yes }')
                code += 'set_technology = { microchip_production_2 = 1 microchip_production_3 = 1 }\n'
            else:
                code += f'set_technology = {{ {technology} = 1 }}\n'
        code += snapshot() + 'set_variable = { gdp_total = 0 }\n'
        code += check(key + '_zero_gdp_blocks', 'NOT = { ' + can + ' = yes }')
        code += call + ' = yes\n'
        code += check(key + '_zero_gdp_no_partial_payment', untouched + ' ' + unchanged())
        code += 'set_variable = { gdp_total = 100 }\n'
        state, building, level = assets[0]
        maximum = building_limits()[building]
        if technology and building in technology_limits():
            maximum = min(maximum, max(cap for tech, cap in technology_limits()[building]))
        code += f'{state} = {{ set_building_level = {{ type = {building} level = {maximum-level+1} }} }}\n' + snapshot()
        code += check(key + '_whole_amount_capacity_blocks', 'NOT = { ' + can + ' = yes }')
        code += call + ' = yes\n'
        code += check(key + '_blocked_capacity_no_partial_payment', untouched + ' ' + unchanged())
        code += f'{state} = {{ set_building_level = {{ type = {building} level = 0 }} }}\n'
        code += check(key + '_eligible', can + ' = yes')
        code += call + ' = yes\n'
        paid = f'has_country_flag = {receipt} ' + near('treasury', -fraction*100)
        paid += ' ' + ' '.join(f'{state} = {{ check_variable = {{ building_level@{building} = {level} }} }}'
                               for state, building, level in assets)
        code += check(key + '_actual_assets_and_gdp_charge', paid)
        code += call + ' = yes\n' + check(key + '_replay_does_not_repay_or_rebuild', paid)
        by_country[tag] += code
        records.append({'focus': identifier, 'receipt': receipt, 'assets': assets, 'expected_gdp_fraction': fraction,
                        'method': 'Exact loaded completion_reward executed in a private country-scoped wrapper.'})
    for index, tag in enumerate(('GER', 'DDR'), 1):
        code = check(tag + '_authored_tree', f'has_focus_tree = COLDWAR_{tag}_1970_focus') + by_country[tag]
        code += f'log = "COLDWAR_GR_PROBE DONE_{tag}"\n'
        events.append(f'country_event = {{ id = COLDWAR_GR_PROBE.{index} hidden = yes is_triggered_only = yes immediate = {{\n{code}\n}} }}')
    return '\n'.join(events), '\n'.join(helpers), '\n'.join(triggers), records


def write(relative, text):
    path = PROFILE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    hashes = json.loads((REPORT / 'SOURCE_CHECKS.json').read_text(encoding='utf-8'))['runtime_sha256']
    for relative, digest in hashes.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    write('mod/base.mod', MARK + (ROOT / 'descriptor.mod').read_text(encoding='utf-8-sig') + '\npath="' + ROOT.as_posix() + '"\n')
    addon = MARK + 'name="German programme native fixture"\ndependencies={ "MD Cold War" }\npath="' + (PROFILE / 'fixture').as_posix() + '"\n'
    write('mod/probe.mod', addon)
    write('fixture/descriptor.mod', addon)
    # Freeze only the small German script inventory and its shared grant
    # dependencies. Concurrent work in other chats cannot alter these inputs
    # halfway through the native run. No artwork junctions are copied.
    for relative in hashes:
        target = PROFILE / 'fixture' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / relative).read_bytes())
    write('dlc_load.json', json.dumps({'enabled_mods': ['mod/base.mod', 'mod/probe.mod'], 'disabled_dlcs': []}))
    write('settings.txt', MARK + 'language="l_english"\ngraphics={size={x=1280 y=900} fullScreen=no borderless=no}\nmaster_volume=0\n')
    dispatch = ' '.join(f'{tag} = {{ country_event = {{ id = COLDWAR_GR_PROBE.{index} hours = 1 }} }}' for index, tag in enumerate(('GER', 'DDR'), 1))
    write('fixture/common/on_actions/zz_COLDWAR_GR_probe.txt', MARK + 'on_actions = { on_startup = { effect = { ' + dispatch + ' } } }')
    for tag in ('GER', 'DDR'):
        path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        history = re.sub(r'(?m)^\s*(?:reactor1|microchip_production_[123])\s*=\s*1[^\n]*\n', '', path.read_text(encoding='utf-8'))
        write('fixture/history/countries/' + path.name, MARK + history)
    events, helpers, triggers, records = fixture()
    for text in (events, helpers, triggers):
        parse(text)
    write('fixture/events/COLDWAR_GR_probe.txt', events)
    write('fixture/common/scripted_effects/COLDWAR_GR_probe.txt', helpers)
    write('fixture/common/scripted_triggers/COLDWAR_GR_probe.txt', triggers)
    for name in ('game.log', 'error.log'):
        write('logs/' + name, '')
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    started = time.monotonic()
    process = subprocess.Popen([str(GAME / 'hoi4.exe'), '-debug', '-noasserts', '-assertsdialog=no', '-userdir=' + str(PROFILE), '-start_tag=GER', '-start_speed=5'], cwd=GAME, startupinfo=startup)
    print(json.dumps({'pid': process.pid, 'profile': str(PROFILE), 'assertions': len(CHECKS)}), flush=True)
    try:
        while process.poll() is None and time.monotonic()-started < 700:
            time.sleep(1)
            game = (PROFILE / 'logs/game.log').read_text(encoding='utf-8-sig', errors='replace')
            if all('COLDWAR_GR_PROBE DONE_' + tag in game for tag in ('GER', 'DDR')):
                break
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    game = (PROFILE / 'logs/game.log').read_text(encoding='utf-8-sig', errors='replace')
    errors = (PROFILE / 'logs/error.log').read_text(encoding='utf-8-sig', errors='replace')
    relevant = [entry.strip() for entry in re.split(r'(?=\[\d{2}:\d{2}:\d{2}\]\[)', errors)
                if any(name in entry for name in ('COLDWAR_GER', 'COLDWAR_DDR', 'COLDWAR_GR_', 'COLDWAR_GRANT')) and 'Reloading Events:' not in entry]
    passed = [name for name in CHECKS if 'COLDWAR_GR_PROBE PASS ' + name in game]
    failed = [name for name in CHECKS if 'COLDWAR_GR_PROBE FAIL ' + name in game]
    unrun = [name for name in CHECKS if name not in passed + failed]
    changed = [relative for relative, digest in hashes.items() if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != digest]
    result = {'project': 'IMPERIA COLD WAR', 'profile': str(PROFILE), 'passed': passed, 'failed': failed,
              'unrun': unrun, 'relevant_errors': relevant, 'source_sha256': hashes, 'changed_during_run': changed,
              'cases': records, 'elapsed_seconds': round(time.monotonic()-started, 1),
              'process_exit_code': process.returncode,
              'crashes': [path.name for path in (PROFILE / 'crashes').glob('*') if path.is_dir()],
              'scope': 'Targeted single-client fixture. Exact emitted focus completion code, private initial withheld chip/reactor tech, temporary state slots/levels and party/leader receipts. Not a full focus playthrough, hover, campaign balance, save/rehost or multiplayer/OOS test.'}
    result['success'] = not failed and not unrun and not relevant and not changed and not result['crashes']
    (REPORT / 'ENGINE_REPORT.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'success': result['success'], 'passed': len(passed), 'failed': failed, 'unrun': unrun,
                      'relevant_errors': relevant[:8], 'changed': changed}), flush=True)


if __name__ == '__main__':
    main()
