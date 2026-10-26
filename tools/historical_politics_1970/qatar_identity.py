# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Bounded Qatari 1970 identity repair; no startup government replacement.

The protected ruling house uses MD Western_Autocracy0 for this scenario.
Modern native selectors remain their original fallback, including Kingdom10.
"""
from copy import deepcopy
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = [
    'https://www.diwan.gov.qa/about-qatar/qatars-rulers/sheikh-ahmad-bin-ali-al-thani?sc_lang=en',
    'https://www.diwan.gov.qa/en/about-qatar/qatars-rulers/sheikh-khalifa-bin-hamad-al-thani',
]


def align_country(original):
    country = deepcopy(original)
    if country['tag'] != 'QAT':
        return country
    for party in country['parties']:
        if party['name'] == 'House of Al Thani':
            assert party['index'] in (0, 10)
            party['index'] = 0
    for person in country['leaders']:
        if person['party_index'] == 10:
            person['party_index'] = 0
        if person['party_index'] == 0:
            person['alignment_note'] = '1970 British-protected ruling house represented by native MD Western_Autocracy0; not a change to modern Qatar.'
        if person['id'] in {'ahmad_bin_ali_al_thani', 'hamad_bin_khalifa_al_thani'}:
            person['traits'] = list(dict.fromkeys(person.get('traits', []) + ['king']))
    return country


def align_seed(seed):
    """Relocate the existing royal support, retaining total support and dates."""
    from starting_identity import first, values
    ruling = next((first(v, 'ruling_party') for v in values(seed, 'set_variable')
                   if first(v, 'ruling_party') is not None), None)
    if ruling not in ('0', '10'):
        return seed
    result = []
    for key, op, value in seed:
        if ruling == '10':
            if key == 'set_variable':
                value = [(('party_pop_array^0' if k == 'party_pop_array^10' else
                           'party_pop_array^10' if k == 'party_pop_array^0' else k), oo,
                          '0' if k == 'ruling_party' else v) for k, oo, v in value]
            elif key == 'set_popularities':
                # Move the existing72 broad-outlook points to Western;
                # broad outlooks remain nonnegative and sum to100.
                value = [(k, oo, '76' if k == 'democratic' else '0' if k == 'fascism' else v)
                         for k, oo, v in value]
            elif key == 'set_politics':
                value = [(k, oo, 'democratic' if k == 'ruling_party' else v) for k, oo, v in value]
        if key in {'create_country_leader', 'promote_character'}:
            value = [(k, oo, 'Western_Autocracy' if k == 'ideology' else v) for k, oo, v in value]
        result.append((key, op, value))
    return result


def build():
    from starting_identity import nodes, parse, first, emit, SNAPSHOT_BEGIN, SNAPSHOT_END
    # starting_identity exposes the shared AST by adding Vietnam's tools path;
    # select this directory's Builder explicitly before importing adapters.
    import sys
    sys.path.insert(0, str(HERE))
    from apply_monarchy_alignment import set_field
    from dispatch import _pool_text, _wrap_native_setter, _validated_people, POOL_FILE, POOL_TRIGGER_FILE, SYNC_EFFECT
    from monarchy_runtime import _blocks, _splice, _script_block
    from build import Builder

    output = {}
    worldpath = HERE / 'data/world.json'
    world = json.loads(worldpath.read_text(encoding='utf-8-sig'))
    world['countries'] = [align_country(c) if c['tag'] == 'QAT' else c for c in world['countries']]
    country = next(c for c in world['countries'] if c['tag'] == 'QAT')
    output[worldpath.relative_to(ROOT).as_posix()] = json.dumps(world, ensure_ascii=False, indent=2) + '\n'

    history = 'history/countries/QAT - Qatar.txt'
    text = (ROOT / history).read_text(encoding='utf-8-sig')
    begin = text.index(SNAPSHOT_BEGIN) + len(SNAPSHOT_BEGIN)
    end = text.index(SNAPSHOT_END)
    text = text[:begin] + '\n\t# IMPERIA CW — Cold War: Historical Qatari national identity.\n' + emit(align_seed(parse(text[begin:end])), 1) + '\n\t' + text[end:]
    output[history] = text

    path = 'common/characters/mdcw_gulf_1970.txt'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    character = next(n for n in nodes(text)[0]['children'] if n['key'] == 'QAT_MDCW_1970_incumbent')
    role = next(n for n in character['children'] if n['key'] == 'country_leader')
    value = set_field(role['value'], 'ideology', 'Western_Autocracy')
    value = set_field(value, 'traits', [('_bare', '=', 'king'), ('_bare', '=', 'western_Western_Autocracy')])
    output[path] = text[:role['start']] + 'country_leader = {\n' + emit(value, 3) + '\n\t\t}' + text[role['end']:]

    # Reuse approved native pools; splice QAT only into both the pool and its
    # counter sync. No other country's generated branch is emitted here.
    builder = Builder({'QAT': country})
    builder.leaders()
    people = _validated_people(ROOT, {'QAT': country}, builder.ready)
    grouped = {('QAT', 0): [p for p in people if p['party_index'] == 0]}
    generated, trigger = _pool_text(ROOT, grouped)
    path = POOL_FILE
    old = (ROOT / path).read_text(encoding='utf-8-sig')
    pattern = r'^MDCW_HP_native_pool_QAT_\d+\s*=\s*\{'
    old = _splice(old, _blocks(old, pattern), ''.join(r[2] for r in _blocks(generated, pattern)))
    sync = _script_block(old, SYNC_EFFECT)
    pattern = r'^\tif = \{\n\t\tlimit = \{ original_tag = QAT check_variable = \{ ruling_party = \d+ \} \}'
    new_sync = _splice(sync, _blocks(sync, pattern), ''.join(r[2] for r in _blocks(_script_block(generated, SYNC_EFFECT), pattern)))
    output[path] = old.replace(sync, new_sync, 1)
    path = POOL_TRIGGER_FILE
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    output[path] = re.sub(r'original_tag = QAT check_variable = \{ ruling_party = (?:0|10) \}',
                          'original_tag = QAT check_variable = { ruling_party = 0 }', text)
    output['common/scripted_effects/QAT_political_leaders.txt'] = _wrap_native_setter(ROOT, 'QAT', {0: grouped[('QAT', 0)]})

    # Keep the dormant global provider consistent without running it at startup.
    path = 'common/scripted_effects/IMP_1970_world_politics_effects.txt'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    effect = next(n for n in nodes(text) if n['key'] == 'IMP_1970_apply_world_politics')
    branch = next(n for n in effect['children'] if n['key'] in {'if', 'else_if'} and
                  first(first(n['value'], 'limit', []), 'original_tag') == 'QAT')
    body = text[branch['start']:branch['end']].replace('IMP_1970_profile_salafist_kingdom = yes', 'COLDWAR_QAT_profile_western_dynasty = yes')
    body = body.replace('ideology = Kingdom', 'ideology = Western_Autocracy')
    output[path] = text[:branch['start']] + body + text[branch['end']:]
    profile = first(parse(text), 'IMP_1970_profile_salafist_kingdom')
    output['common/scripted_effects/COLDWAR_QAT_1970_identity.txt'] = (
        '# Canonical owner: tools/historical_politics_1970/qatar_identity.py\n'
        'COLDWAR_QAT_profile_western_dynasty = {\n' + emit(align_seed(profile), 1) + '\n}\n')

    # Party UI branches are bounded to QAT; the native modern setter and all
    # neighbouring countries remain unchanged.
    path = 'tools/historical_politics_1970/data_party_names_americas_middleeast.json'
    names = json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
    names['countries']['QAT']['labels'][0] = 'Diwan Al Thani'
    names['countries']['QAT']['labels'][23] = 'Sovereigntist royalist current'
    output[path] = json.dumps(names, ensure_ascii=False, indent=2) + '\n'
    from unittest.mock import patch
    from party_presentation import load_names
    planned = load_names()
    planned['QAT'] = names['countries']['QAT']
    with patch('party_presentation.load_names', return_value=planned):
        builder.parties()
    path = 'common/scripted_localisation/mdcw_historical_parties.txt'
    old = (ROOT / path).read_text(encoding='utf-8-sig')
    new = builder.outputs[path]
    newdefs = {first(n['value'], 'name'): n for n in nodes(new) if n['key'] == 'defined_text'}
    replacements = []
    for definition in nodes(old):
        if definition['key'] != 'defined_text':
            continue
        name = first(definition['value'], 'name')
        if name not in newdefs:
            continue
        qrows = [n for n in definition['children'] if n['key'] == 'text' and first(first(n['value'], 'trigger', []), 'original_tag') == 'QAT']
        if not qrows:
            continue
        nrows = [n for n in newdefs[name]['children'] if n['key'] == 'text' and first(first(n['value'], 'trigger', []), 'original_tag') == 'QAT']
        insertion = '\t' + '\n\t'.join(new[n['start']:n['end']] for n in nrows) + '\n'
        for index, row in enumerate(qrows):
            begin = old.rfind('\n', 0, row['start']) + 1
            end = old.find('\n', row['end'])
            end = len(old) if end < 0 else end + 1
            assert not old[begin:row['start']].strip()
            assert not old[row['end']:end].strip()
            if index == len(qrows) - 1:
                # Own only trailing whitespace of this QAT group. Previous
                # narrower replacements left whitespace-only deleted rows.
                while (blank := re.match(r'[\t ]*\n', old[end:])):
                    end += blank.end()
            replacements.append((begin, end, insertion if index == 0 else ''))
    for begin, end, value in sorted(replacements, reverse=True):
        old = old[:begin] + value + old[end:]
    output[path] = old
    from build import loc_quote
    path = 'localisation/english/mdcw_historical_politics_1970_l_english.yml'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    for key, value in builder.loc.items():
        if not key.startswith('MDCW_HP_QAT_'):
            continue
        line = ' ' + key + ':0 ' + loc_quote(value)
        pattern = r'(?m)^ ' + re.escape(key) + r':0[^\n]*'
        if re.search(pattern, text):
            text = re.sub(pattern, lambda _: line, text)
        else:
            text += line + '\n'
    output[path] = text
    import hashlib
    from apply_monarchy_alignment import output_bytes
    history_hash = hashlib.sha256(output_bytes(ROOT / history, output[history])).hexdigest()
    for path in ('tools/historical_politics_1970/party_inventory.json',
                 'docs/audits/1970_starting_identity.json',
                 'docs/regional_starting_rulers_1970_20261019.json',
                 'docs/gulf_start_1970_portraits_20261019.json'):
        raw = (ROOT / path).read_text(encoding='utf-8-sig')
        report = json.loads(raw)
        for row in report.get('countries', report.get('items', [])):
            if row['tag'] != 'QAT':
                continue
            for key, value in [('ruling_party_index', 0), ('index_label', 'Western_Autocracy'),
                               ('party_index', 0), ('ideology', 'Western_Autocracy')]:
                if key in row:
                    row[key] = value
            if 'after_sha256' in row:
                row['after_sha256'] = history_hash
            row['qatar_identity_owner'] = 'tools/historical_politics_1970/qatar_identity.py'
        output[path] = json.dumps(report, ensure_ascii=False, indent=2) + ('\n' if raw.endswith('\n') else '')
    return output


def install():
    from apply_monarchy_alignment import output_bytes
    changed = []
    for name, value in build().items():
        path = ROOT / name
        raw = output_bytes(path, value)
        if not path.exists() or path.read_bytes() != raw:
            path.write_bytes(raw)
            changed.append(name)
    return changed


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--install', action='store_true')
    args = cli.parse_args()
    print(json.dumps({'changed': install()} if args.install else {'planned': list(build())}))
