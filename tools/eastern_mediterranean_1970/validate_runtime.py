"""Structural and integration checks for the generated regional roster."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def behavioral_checks(asts, compiler, roster):
    """Interpret the small emitted condition/effect subset, not the HOI4 engine."""
    functions = {}
    for path, tree in asts.items():
        if 'regional_effects' in path.name:
            functions.update({k: v for k, op, v in tree})
    cases = 0
    def environment(tag, when=(1970, 1, 1), scenario=True, party=1):
        return dict(tag=tag, date=when, scenario=scenario, human=True,
            variables={'ruling_party': party}, flags=set(), characters=set(), leaders=[])
    def numeric(value, env):
        if value in env['variables']:
            return env['variables'][value]
        try:
            return float(value)
        except ValueError:
            return 0
    def condition(tree, env):
        def item(key, op, value):
            if key == 'OR':return any(item(*v) for v in value)
            if key == 'AND':return condition(value, env)
            if key == 'NOT':return not condition(value, env)
            if key == 'original_tag':return value == env['tag']
            if key == 'exists':return value == 'yes'
            if key == 'IMP_is_1970_scenario':return env['scenario'] == (value == 'yes')
            if key == 'is_ai':return (not env['human']) == (value == 'yes')
            if key == 'has_country_flag':return value in env['flags']
            if key == 'has_character':return value in env['characters']
            if key == 'check_variable':
                return all(numeric(k, env) == numeric(v, env) for k, op, v in value)
            if key == 'date':
                other = tuple(map(int, value.split('.')))
                return env['date'] > other if op == '>' else env['date'] < other if op == '<' else env['date'] == other
            raise AssertionError('Uninterpreted emitted trigger ' + key)
        return all(item(*v) for v in tree)
    def execute(tree, env, depth=0):
        assert depth < 20, 'Recursive effect loop'
        chain = False
        for key, op, value in tree:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':chain = False
                limit = next((v for k, op, v in value if k == 'limit'), [])
                if not chain and (key == 'else' or condition(limit, env)):
                    execute([(k, op, v) for k, op, v in value if k != 'limit'], env, depth + 1)
                    chain = True
            elif key in functions:
                execute(functions[key], env, depth + 1)
            elif key == 'set_country_flag':env['flags'].add(value)
            elif key == 'clr_country_flag':env['flags'].discard(value)
            elif key == 'recruit_character':env['characters'].add(value)
            elif key == 'retire_character':env['characters'].discard(value)
            elif key == 'set_variable':
                for k, op, v in value:env['variables'][k] = numeric(v, env)
            elif key == 'create_country_leader':env['leaders'].append(dict((k, v) for k, op, v in value))
            elif key == 'update_set_politics':pass
            else:raise AssertionError('Uninterpreted emitted effect ' + key)
    # The dispatcher must map each native MD index to exactly its own ideology.
    for tag in ('GRE', 'TUR'):
        for index, ideology in enumerate(compiler.IDEOLOGIES):
            env = environment(tag, party=index)
            execute(functions[f'COLDWAR_{tag}_1970_set_leader'], env)
            assert len(env['leaders']) == 1 and env['leaders'][-1]['ideology'] == ideology, (tag, index)
            cases += 1
        # Neither startup nor a direct call may touch a2000-start campaign.
        env = environment(tag, (2000, 1, 1), scenario=False)
        native = next(v for v in functions[f'COLDWAR_{tag}_1970_retire_modern_roster'][0][2] if v[0] == 'if')
        native_id = next(v for k, op, v in native[2] if k == 'retire_character')
        env['characters'].add(native_id)
        execute(functions[f'COLDWAR_{tag}_1970_daily_tick'], env)
        execute(functions[f'COLDWAR_{tag}_1970_set_leader'], env)
        assert env['characters'] == {native_id} and not env['leaders'], tag
        env['scenario'] = True
        env['date'] = (1970, 1, 1)
        execute(functions[f'COLDWAR_{tag}_1970_daily_tick'], env)
        assert native_id not in env['characters'], tag
        # Merely advancing the calendar does not redispatch the incumbent.
        count = len(env['leaders'])
        env['date'] = (1974, 12, 1)
        execute(functions[f'COLDWAR_{tag}_1970_daily_tick'], env)
        assert len(env['leaders']) == count, tag
        cases += 3
    ready = {(r['tag'], r['key']) for r in roster}
    if {('TUR', 'ismet_inonu'), ('TUR', 'bulent_ecevit')} <= ready:
        env = environment('TUR', party=3)
        env['flags'].add('COLDWAR_TUR_1970_selected_ismet_inonu')
        execute(functions['COLDWAR_TUR_1970_daily_tick'], env)
        original = env['leaders'][-1]
        env['date'] = (1973, 12, 26)
        execute(functions['COLDWAR_TUR_1970_daily_tick'], env)
        assert env['leaders'][-1] == original and len(env['leaders']) == 1
        execute(functions['COLDWAR_TUR_1970_set_leader'], env)
        assert env['leaders'][-1]['name'] != original['name'], 'Expired selected politician reapplied'
        cases += 2
    if ('CYP', 'georgitsis') in ready:
        fx = functions['COLDWAR_EASTMED_CYP_1970_refresh_roster']
        env = environment('CYP', (1974, 7, 15))
        execute(fx, env)
        assert 'COLDWAR_CYP_1970_georgitsis' not in env['characters']
        env['flags'].add('COLDWAR_CYP_1970_coup_regime_active')
        execute(fx, env)
        assert 'COLDWAR_CYP_1970_georgitsis' in env['characters']
        env['flags'].discard('COLDWAR_CYP_1970_coup_regime_active')
        execute(fx, env)
        assert 'COLDWAR_CYP_1970_georgitsis' not in env['characters']
        cases += 3
    return cases


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = load(ROOT / 'tools/cyprus_1970/validate.py', 'cyprus_parser')
    compiler = load(HERE / 'compile.py', 'regional_compiler')
    report = json.loads((HERE / 'runtime_build.json').read_text(encoding='utf-8'))
    roster = json.loads((HERE / 'runtime_roster.json').read_text(encoding='utf-8'))
    paths = [ROOT / rel for rel in report['files']]
    asts = {}
    for path in paths:
        assert path.is_file(), path
        if path.suffix in ('.txt', '.gfx'):
            asts[path] = parser.parse(path.read_text(encoding='utf-8-sig'))
    all_chars = {}
    for path, tree in asts.items():
        if path.parent.name == 'characters':
            for ident, op, value in parser.first(tree, 'characters', []):
                assert ident not in all_chars, ident
                all_chars[ident] = value
    assert len(all_chars) == len(roster), (len(all_chars), len(roster))
    for row in roster:
        tree = all_chars[row['id']]
        assert (ROOT / row['portrait']).is_file(), row['id']
        assert (ROOT / row['small']).is_file(), row['id']
        assert row['portrait'] not in report['institutional_generic'].values(), row['id']
        advisor = parser.first(tree, 'advisor', [])
        assert 'IMP_is_1970_scenario' in str(parser.first(advisor, 'allowed')), row['id']
        assert 'IMP_is_1970_scenario' in str(parser.first(advisor, 'available')), row['id']
        assert ('exists', '=', 'yes') in list(parser.walk(parser.first(advisor, 'available', [])))
        assert ('date', '>', compiler.previous_day(row['chief_start'])) in list(parser.walk(parser.first(advisor, 'available', [])))
        if row['kind'] in ('political', 'air', 'navy'):
            assert not parser.vals(tree, 'corps_commander'), row['id']
        if row['kind'] == 'navy':
            assert parser.vals(tree, 'navy_leader'), row['id']
    owned = {p: tree for p, tree in asts.items() if 'regional_' in p.name or p.name == 'COLDWAR_EASTMED_1970_traits.txt'}
    forbidden = {'create_wargoal', 'declare_war_on', 'set_politics', 'country_event',
        'kill_country_leader', 'annex_country', 'transfer_state', 'set_popularities'}
    for path, tree in owned.items():
        assert not (forbidden & {k for k, op, v in parser.walk(tree)}), path
        for k, op, value in parser.walk(tree):
            if k == 'create_country_leader':
                assert parser.first(value, 'expire') == '"2000.1.1"', path
    # Every native retirement must be nested in its own has_character guard.
    def check_retire(tree, guards=()):
        for k, op, value in tree:
            if k == 'retire_character':
                assert any(('has_character', '=', value) in list(parser.walk(g)) for g in guards), value
            if isinstance(value, list):
                check_retire(value, guards + tuple(parser.vals(value, 'limit')))
    for path, tree in owned.items():
        check_retire(tree)
    for tag in ('TUR', 'GRE'):
        fx = asts[ROOT / f'common/scripted_effects/COLDWAR_{tag}_1970_regional_effects.txt']
        leader = parser.first(fx, f'COLDWAR_{tag}_1970_set_leader')
        assert leader is not None
        parties = {v for k, op, v in parser.walk(leader) if k == 'ruling_party'}
        assert parties == set(map(str, range(24))), (tag, parties)
        for key, op, body in parser.walk(leader):
            if key in ('if', 'else_if'):
                limit = parser.first(body, 'limit', [])
                selected = [v for k, op, v in parser.walk(limit) if k == 'has_country_flag' and '_selected_' in v]
                if selected:
                    assert any(k == 'date' for k, op, v in parser.walk(limit)), selected
    cypfx = asts[ROOT / 'common/scripted_effects/COLDWAR_CYP_1970_regional_effects.txt']
    refresh = parser.first(cypfx, 'COLDWAR_EASTMED_CYP_1970_refresh_roster', [])
    for k, op, body in parser.walk(refresh):
        if k == 'if' and ('recruit_character', '=', 'COLDWAR_CYP_1970_georgitsis') in body:
            assert ('has_country_flag', '=', 'COLDWAR_CYP_1970_coup_regime_active') in list(parser.walk(parser.first(body, 'limit', [])))
    dispatch = (ROOT / 'common/scripted_effects/00_leader_setup_scripted_effects.txt').read_text(encoding='utf-8')
    first_kill = dispatch.index('kill_country_leader = yes')
    for tag in ('GRE', 'TUR'):
        assert dispatch.index(f'COLDWAR_{tag}_1970_set_leader = yes') < first_kill
        assert dispatch.count(f'COLDWAR_{tag}_1970_set_leader = yes') == 1
    local_path = ROOT / 'localisation/english/COLDWAR_EASTMED_1970_l_english.yml'
    raw = local_path.read_bytes()
    assert raw.startswith(b'\xef\xbb\xbf')
    keys = re.findall(r'^ (\S+):0 ', raw.decode('utf-8-sig'), re.M)
    assert len(keys) == len(set(keys))
    assert set(all_chars) <= set(keys)
    behavior_cases = behavioral_checks(asts, compiler, roster)
    # Rerun in place only after checking syntax. No new assets or input mutation
    # occurs in this test: deterministic compilation must preserve every byte.
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    compiler.Compiler(ROOT).generate()
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before == after, [str(p) for p in before if before[p] != after[p]]
    print(json.dumps({'result': 'PASS', 'characters': len(all_chars), 'political_slots': 48,
        'parsed_files': len(asts), 'localisation_keys': len(keys), 'behavior_cases': behavior_cases, 'idempotent': True,
        'in_game_engine_test': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
