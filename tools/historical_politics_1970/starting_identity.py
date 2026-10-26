# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Bounded 1970 history identity repair; never regenerate regional mechanics.

Only existing authored incumbents and political profiles are promoted to native
dated history. Later bookmarks and unrelated history commands remain intact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, emit, first, values, walk
from script_ast import TOKEN

IDEOLOGIES = ['Western_Autocracy', 'conservatism', 'liberalism', 'socialism',
    'communist_state', 'anarchist_communism', 'Conservative', 'Autocracy',
    'Mod_Vilayat_e_Faqih', 'Vilayat_e_Faqih', 'Kingdom', 'Caliphate',
    'Neutral_Muslim_Brotherhood', 'Neutral_Autocracy', 'Neutral_conservatism',
    'oligarchism', 'Neutral_Libertarian', 'Neutral_green', 'neutral_Social',
    'Neutral_Communism', 'Nat_Populism', 'Nat_Fascism', 'Nat_Autocracy', 'Monarchist']
SNAPSHOT_BEGIN = '# COLDWAR HISTORICAL1970 NATIVE IDENTITY BEGIN'
SNAPSHOT_END = '# COLDWAR HISTORICAL1970 NATIVE IDENTITY END'
MODERN_BEGIN = '# COLDWAR HISTORICAL1970 MODERN IDENTITY COMPATIBILITY BEGIN'
MODERN_END = '# COLDWAR HISTORICAL1970 MODERN IDENTITY COMPATIBILITY END'
MODERN_DEFAULT_RESTORES = {'DDR': 'DDR_DDR', 'SAM': 'SAM_WESTERN_SAMOA_1970',
                           'SVN': 'SVN_REPUBLIC_1970', 'SYE': 'SYE_SOUTH_YEMEN_1970'}

GULF_BEGIN = '# COLDWAR HISTORICAL1970 PRESERVE COSMETICS BEGIN'
GULF_END = '# COLDWAR HISTORICAL1970 PRESERVE COSMETICS END'
TREATY_BEGIN = '# COLDWAR HISTORICAL1970 INITIAL TREATIES BEGIN'
TREATY_END = '# COLDWAR HISTORICAL1970 INITIAL TREATIES END'


def replace_marker(source, begin, end, body, anchor=None):
    replacement = begin + '\n# IMPERIA CW — Cold War: Historical identity and initial treaty integration.\n' + body.rstrip() + '\n' + end
    pattern = re.escape(begin) + r'.*?' + re.escape(end)
    if begin in source:
        assert source.count(begin) == source.count(end) == 1
        return re.sub(pattern, lambda _: replacement, source, flags=re.S)
    assert anchor and source.count(anchor) == 1, (begin, anchor)
    return source.replace(anchor, replacement + '\n' + anchor)


def callback_outputs():
    """Protect authored Gulf names and only the initial UK treaty setup."""
    path = 'common/on_actions/00_on_actions.txt'
    source = (ROOT / path).read_text(encoding='utf-8-sig')
    # on_government_change runs before MD writes the new subparty variable.
    # Engine outlook + exact authored cosmetic therefore identify this guard.
    body = '''\t\t\t\t\tNOT = {
\t\t\t\t\t\tAND = {
\t\t\t\t\t\t\tIMP_is_1970_scenario = yes
\t\t\t\t\t\t\tOR = {
\t\t\t\t\t\t\t\tAND = { original_tag = SAU has_cosmetic_tag = SAU_KSA_1985 has_government = fascism }
\t\t\t\t\t\t\t\tAND = { original_tag = OMA has_cosmetic_tag = OMA_MUSCAT_1970 has_government = nationalist }
\t\t\t\t\t\t\t\tAND = { original_tag = JOR has_cosmetic_tag = JOR_AUTH has_government = democratic }
\t\t\t\t\t\t\t}
\t\t\t\t\t\t}
\t\t\t\t\t}'''
    source = replace_marker(source, GULF_BEGIN, GULF_END, body,
                            '# COLDWAR UAE PRESERVE TRUCIAL NAME BEGIN')
    yield path, source
    path = 'common/scripted_effects/IMP_1970_world_politics_effects.txt'
    source = (ROOT / path).read_text(encoding='utf-8-sig')
    if TREATY_BEGIN not in source:
        opening = '\tENG = {\n\t\tset_autonomy = { target = BHR autonomy_state = autonomy_puppet_state }'
        assert source.count(opening) == 1
        source = source.replace(opening, '\tENG = {\n' + TREATY_BEGIN + '\n# IMPERIA CW — Cold War: Initial British treaty arrangements.\n'
                                '\t\tset_global_flag = COLDWAR_1970_initial_treaty_setup\n' + TREATY_END + '\n'
                                '\t\tset_autonomy = { target = BHR autonomy_state = autonomy_puppet_state }')
        closing = '\t\tset_autonomy = { target = TON autonomy_state = autonomy_puppet_state }\n'
        assert source.count(closing) == 1
        source = source.replace(closing, closing +
                                '\t\tclr_global_flag = COLDWAR_1970_initial_treaty_setup\n')
    assert source.count('set_global_flag = COLDWAR_1970_initial_treaty_setup') == 1
    assert source.count('clr_global_flag = COLDWAR_1970_initial_treaty_setup') == 1
    yield path, source


def write_outputs(outputs):
    changed = []
    for name, text in outputs:
        path = ROOT / name
        before = path.read_text(encoding='utf-8-sig')
        if before != text:
            path.write_text(text, encoding='utf-8-sig', newline='\n')
            changed.append(name)
    return changed


def nodes(source):
    """Parse with source positions so unrelated history text stays untouched."""
    tokens = [m for m in TOKEN.finditer(source) if not m[0].startswith('#')]
    cursor = 0
    def read(nested=False):
        nonlocal cursor
        result = []
        while cursor < len(tokens):
            token = tokens[cursor]; cursor += 1
            if token[0] == '}':
                assert nested
                return result, token.end()
            key = token[0]
            if cursor >= len(tokens) or tokens[cursor][0] not in ('=', '<', '>', '>=', '<=', '!='):
                result.append({'key': '_bare', 'start': token.start(), 'end': token.end(), 'value': key, 'children': []})
                continue
            op = tokens[cursor][0]; cursor += 1
            value = tokens[cursor]; cursor += 1
            children = []
            if value[0] == '{':
                children, end = read(True)
                parsed_value = parse(source[value.end():end - 1])
            else:
                end = value.end(); parsed_value = value[0]
            result.append({'key': key, 'op': op, 'start': token.start(), 'end': end,
                           'opening': value.end() if children or value[0] == '{' else None,
                           'value': parsed_value, 'children': children})
        assert not nested
        return result, len(source)
    return read()[0]


def identity_nodes(children):
    for node in children:
        key, value = node['key'], node['value']
        if (key.startswith('IMP_1970_profile_') or key in {
                'set_popularities', 'set_politics', 'set_cosmetic_tag',
                'create_country_leader', 'recruit_character', 'promote_character'}
            or key == 'set_variable' and isinstance(value, list)
                and any(k == 'ruling_party' or k.startswith('party_pop_array^') for k, _, _ in value)):
            yield node
        elif key in {'if', 'else_if', 'else', 'hidden_effect'}:
            yield from identity_nodes(node['children'])


def profile_seed(profile):
    """Expand the existing MD inputs, excluding runtime recalculation helpers."""
    return [(key, op, value) for key, op, value in profile
            if key in {'set_popularities', 'set_politics', 'add_to_array'}
            or key == 'set_variable' and isinstance(value, list)
                and any(k == 'ruling_party' or k.startswith('party_pop_array^') for k, _, _ in value)]


def native_seed_prefix():
    # Native start_politics_input leaves; no GUI/leader callback or helper gate.
    return parse('''clear_array = party_pop_array
clear_array = party_pop_elect_array
clear_array = pos_array
clear_variable = ruling_party
clear_array = gov_coalition_array
resize_array = { array = party_pop_array size = 24 }
resize_array = { array = party_pop_elect_array size = 24 value = -1 }
resize_array = { array = pos_array size = 24 }
resize_array = { array = party_banned_array size = 24 value = 0 }''')


def leb_array_input(row):
    key, _, value = row
    return (key == 'clear_array' and value in {'party_pop_array', 'party_pop_elect_array', 'pos_array', 'gov_coalition_array'}
            or key == 'clear_variable' and value == 'ruling_party'
            or key == 'resize_array' and first(value, 'array') in {'party_pop_array', 'party_pop_elect_array', 'pos_array', 'party_banned_array'}
            or key == 'set_variable' and isinstance(value, list) and any(k.startswith('party_pop_array^') for k, _, _ in value)
            or key == 'add_to_array' and isinstance(value, list) and first(value, 'gov_coalition_array') is not None)


def normalise_native_seed(seed, tag=None):
    """Preview identity stays direct; campaign-only flags stay scenario-scoped."""
    seed = [('if', '=', [('limit', '=', [('IMP_is_1970_scenario', '=', 'yes')]),
                         ('set_country_flag', '=', value)])
            if key == 'set_country_flag' and value == 'IMP_1970_historical_politics'
            else (key, op, value) for key, op, value in seed]
    recruits = [row for row in seed if row[0] == 'recruit_character']
    if recruits:
        seed = [row for row in seed if row[0] != 'recruit_character']
        position = next(i for i, row in enumerate(seed) if row[0] == 'set_politics')
        seed[position:position] = recruits
    if tag == 'LEB':
        # Lebanon's native2000 history has no political array seed. Preserve
        # that existing fallback while keeping its preexisting raw incumbent,
        # broad politics and ruling subtype available in country selection.
        array_input = [row for row in seed if leb_array_input(row)]
        if array_input:
            first_position = next(i for i, row in enumerate(seed) if leb_array_input(row))
            seed = [row for row in seed if not leb_array_input(row)]
            guarded = ('if', '=', [('limit', '=', [('IMP_is_1970_scenario', '=', 'yes')])] + array_input)
            seed.insert(first_position, guarded)
    if tag == 'QAT':
        from qatar_identity import align_seed
        seed = align_seed(seed)
    return seed


def modern_identity_compatibility(source, tag):
    cosmetic = MODERN_DEFAULT_RESTORES.get(tag)
    if not cosmetic or MODERN_BEGIN in source:
        return source
    assert any(k == 'set_cosmetic_tag' and v == cosmetic
               for block in values(parse(source), '1970.1.1') for k, _, v in block), (tag, 'unexpected historical cosmetic')
    # This is a pre-modern-bookmark setup boundary, not a historical rename
    # event. Dated history does not execute as an on-action in a running game.
    return source.rstrip() + '\n\n' + MODERN_BEGIN + '\n# IMPERIA CW — Cold War: Later-bookmark national identity compatibility.\n' + '''# Preserve the native modern default when past dated history is replayed.
# Setup compatibility boundary only; not a claimed historical renaming date.
1999.12.31 = {
\tif = {
\t\tlimit = {
\t\t\tNOT = { IMP_is_1970_scenario = yes }
\t\t\thas_cosmetic_tag = ''' + cosmetic + '''
\t\t}
\t\tdrop_cosmetic_tag = yes
\t}
}
''' + MODERN_END + '\n\n'


def history_output(path, profile_tree):
    raw = path.read_bytes()
    boundary = re.search(rb'(?m)^2000\.1\.1[ \t]*=', raw)
    prefix_bytes, tail = (raw[:boundary.start()], raw[boundary.start():]) if boundary else (raw, b'')
    source = prefix_bytes.decode('utf-8-sig').replace('\r\n', '\n')
    date_nodes = [n for n in nodes(source) if n['key'] == '1970.1.1']
    original_nodes = [n for date_node in date_nodes for n in identity_nodes(date_node['children'])]
    leaders = [n for n in original_nodes if n['key'] in {'create_country_leader', 'promote_character'}]
    if not leaders:
        return None, {'tag': path.name[:3], 'status': 'dormant_no_authored_1970_identity',
                      'history': path.relative_to(ROOT).as_posix()}
    assert len(leaders) == 1, (path, 'competing authored incumbents')
    # Already installed output remains an input source, but reconstructing it
    # cannot remove its raw array initialization or duplicate the marker.
    if SNAPSHOT_BEGIN in source:
        begin = source.index(SNAPSHOT_BEGIN) + len(SNAPSHOT_BEGIN)
        end = source.index(SNAPSHOT_END)
        old_seed = parse(source[begin:end])
        new_seed = normalise_native_seed(old_seed, path.name[:3])
        if new_seed != old_seed:
            source = source[:begin] + '\n' + emit(new_seed, 1) + '\n\t' + source[end:]
        source = modern_identity_compatibility(source, path.name[:3])
        output = b'\xef\xbb\xbf' + source.encode('utf-8') + tail
        return output, {'tag': path.name[:3], 'status': 'already_native_snapshot',
                     'history': path.relative_to(ROOT).as_posix(), 'later_sha256': hashlib.sha256(tail).hexdigest(),
                     'after_sha256': hashlib.sha256(output).hexdigest(),
                     'array_initialization_mode': 'scenario_guarded_existing_modern_fallback' if path.name.startswith('LEB') else 'native_direct'}
    profiles = [n['key'] for n in original_nodes if n['key'].startswith('IMP_1970_profile_')]
    assert len(profiles) <= 1, (path, profiles)
    if profiles:
        provider = 'common/scripted_effects/IMP_1970_world_politics_effects.txt#' + profiles[0]
        seed = profile_seed(first(profile_tree, profiles[0]))
    elif path.name.startswith('ISR'):
        provider = 'common/scripted_effects/ISR70_effects.txt#ISR70_apply_starting_politics'
        seed = profile_seed(first(parse((ROOT / 'common/scripted_effects/ISR70_effects.txt').read_text(encoding='utf-8-sig')), 'ISR70_apply_starting_politics'))
    else:
        assert path.name.startswith('NCY'), ('missing authored profile', path)
        provider = 'common/scripted_effects/IMP_1970_world_politics_effects.txt#IMP_1970_profile_democratic_conservative'
        seed = profile_seed(first(profile_tree, 'IMP_1970_profile_democratic_conservative'))
    # Existing direct election dates, ruling subtype and broad popularity win.
    for key in ('set_popularities', 'set_politics'):
        override = [n['value'] for n in original_nodes if n['key'] == key]
        if override:
            seed = [(k, op, override[-1] if k == key else v) for k, op, v in seed]
    variable_overrides = {k: (k, op, v) for n in original_nodes if n['key'] == 'set_variable'
                          for k, op, v in n['value']}
    seed = [(k, op, [variable_overrides.get(kk, (kk, oo, vv)) for kk, oo, vv in v])
            if k == 'set_variable' else (k, op, v) for k, op, v in seed]
    ideology = first(leaders[0]['value'], 'ideology')
    index = IDEOLOGIES.index(ideology)
    ruling = next(first(v, 'ruling_party') for k, _, v in seed if k == 'set_variable' and first(v, 'ruling_party') is not None)
    assert int(ruling) == index, (path, 'authored profile and incumbent disagree', ruling, ideology)
    recruit_rows = [(n['key'], '=', n['value']) for n in original_nodes if n['key'] == 'recruit_character']
    leader_rows = [(n['key'], '=', n['value']) for n in original_nodes
                   if n['key'] in {'create_country_leader', 'promote_character'}]
    cosmetic_rows = [(n['key'], '=', n['value']) for n in original_nodes if n['key'] == 'set_cosmetic_tag']
    assert len(cosmetic_rows) <= 1, (path, cosmetic_rows)
    politics_rows = [(k, o, v) for k, o, v in seed if k in {'set_popularities', 'set_politics'}]
    array_rows = [(k, o, v) for k, o, v in seed if k not in {'set_popularities', 'set_politics'}]
    historical_flag = ('if', '=', [('limit', '=', [('IMP_is_1970_scenario', '=', 'yes')]),
                                   ('set_country_flag', '=', 'IMP_1970_historical_politics')])
    snapshot = [historical_flag] + cosmetic_rows + recruit_rows + politics_rows + native_seed_prefix() + array_rows + leader_rows
    snapshot = normalise_native_seed(snapshot, path.name[:3])
    # Remove exactly the source identity statements, leaving all mechanics,
    # comments, technology, OOB and helper calls in their original locations.
    for node in sorted(original_nodes, key=lambda n: n['start'], reverse=True):
        source = source[:node['start']] + source[node['end']:]
    first_date = next(n for n in nodes(source) if n['key'] == '1970.1.1')
    fragment = '\n\t' + SNAPSHOT_BEGIN + '\n\t# IMPERIA CW — Cold War: Historical 1970 national identity.\n' + emit(snapshot, 1) + '\n\t' + SNAPSHOT_END + '\n'
    source = source[:first_date['opening']] + fragment + source[first_date['opening']:]
    # Remove only newly empty lines; never rewrite the native later bookmark.
    source = re.sub(r'(?m)^[ \t]+\n', '\n', source)
    source = modern_identity_compatibility(source, path.name[:3])
    result = b'\xef\xbb\xbf' + source.encode('utf-8') + tail
    return result, {'tag': path.name[:3], 'status': 'native_snapshot', 'profile_provider': provider,
                    'history': path.relative_to(ROOT).as_posix(), 'party_index': index,
                    'ideology': ideology, 'leader': first(leaders[0]['value'], 'name') or first(leaders[0]['value'], 'character'),
                    'cosmetic': cosmetic_rows[0][2] if cosmetic_rows else None,
                    'later_sha256': hashlib.sha256(tail).hexdigest(),
                    'before_sha256': hashlib.sha256(raw).hexdigest(), 'after_sha256': hashlib.sha256(result).hexdigest(),
                    'array_initialization_mode': 'scenario_guarded_existing_modern_fallback' if path.name.startswith('LEB') else 'native_direct'}


def history_outputs(install=False):
    profile_tree = parse((ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig'))
    rows, changed, outputs = [], [], []
    report_path = ROOT / 'docs/audits/1970_starting_identity.json'
    old_report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
    old_rows = {row['tag']: row for row in old_report.get('countries', [])}
    for path in sorted((ROOT / 'history/countries').glob('*.txt')):
        if path.name.startswith('UAE - '):
            rows.append({'tag': 'UAE', 'status': 'delegated_uae_canonical_generator'})
            continue
        output, row = history_output(path, profile_tree)
        if row['status'] == 'already_native_snapshot' and row['tag'] in old_rows:
            row = {**old_rows[row['tag']], **row, 'status': 'native_snapshot'}
        rows.append(row)
        if output is not None and output != path.read_bytes():
            changed.append(path.relative_to(ROOT).as_posix())
            outputs.append((path, output))
    cumulative = sorted({row['history'] for row in rows if row.get('before_sha256') and row.get('before_sha256') != row.get('after_sha256')})
    report = {'scope': '1970 native country history identities; UAE delegated',
              'native_game_runtime_tested': False, 'files_audited': len(rows), 'changed': cumulative,
              'changed_this_run': changed,
              'countries': rows}
    if install:
        for path, output in outputs:
            path.write_bytes(output)
        dest = ROOT / 'docs/audits/1970_starting_identity.json'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--callbacks', action='store_true')
    cli.add_argument('--history', action='store_true')
    cli.add_argument('--install', action='store_true')
    args = cli.parse_args()
    if args.callbacks:
        print(json.dumps({'changed': write_outputs(callback_outputs())}))
    if args.history:
        result = history_outputs(args.install)
        print(json.dumps({'files_audited': result['files_audited'], 'changes': len(result['changed_this_run']),
                          'statuses': {s: sum(r['status'] == s for r in result['countries']) for s in sorted({r['status'] for r in result['countries']})}}))
