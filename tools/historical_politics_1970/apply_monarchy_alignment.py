# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Install only keyed native dynasty corrections and their party presentation.

No date-driven government restoration is added. Runtime leader pools are owned
by monarchy_runtime.py; this file owns the corresponding data/history/UI leaves.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import os
import tempfile
from pathlib import Path

from starting_identity import (ROOT, SNAPSHOT_BEGIN, SNAPSHOT_END, nodes, parse,
                               emit, first, values, walk, callback_outputs,
                               normalise_native_seed, modern_identity_compatibility)
from monarchy_alignment import corrections, apply_world

HERE = Path(__file__).resolve().parent


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def set_field(rows, key, value):
    assert sum(k == key for k, _, _ in rows) <= 1, key
    if any(k == key for k, _, _ in rows):
        return [(k, op, value if k == key else v) for k, op, v in rows]
    return rows + [(key, '=', value)]


def align_seed(seed, tag):
    """Move only existing dynastic support; no popularity or cash is added."""
    # Dated1970 history is also replayed when selecting a later bookmark.
    # The native preview identity stays direct, while this runtime-only flag
    # must never leak into2000 through the earlier dated snapshot.
    seed = normalise_native_seed(seed, tag)
    patch = corrections().get(tag)
    if patch:
        ruling = next(first(v, 'ruling_party') for v in values(seed, 'set_variable') if first(v, 'ruling_party') is not None)
        assert ruling in ('0', '23'), (tag, ruling)
        if ruling == '23':
            support = {k: float(v) for row in values(seed, 'set_variable') for k, _, v in row if k.startswith('party_pop_array^')}
            delta = (support['party_pop_array^23'] - support['party_pop_array^0']) * 100
            changed = []
            for key, op, value in seed:
                if key == 'set_variable':
                    value = [(('party_pop_array^23' if k == 'party_pop_array^0' else
                               'party_pop_array^0' if k == 'party_pop_array^23' else k), oo,
                              '0' if k == 'ruling_party' else v) for k, oo, v in value]
                elif key == 'set_popularities':
                    old = {k: float(v) for k, _, v in value}
                    old['democratic'] += delta
                    old['nationalist'] -= delta
                    value = [(k, oo, f'{old[k]:g}') for k, oo, _ in value]
                elif key == 'set_politics':
                    value = set_field(value, 'ruling_party', 'democratic')
                changed.append((key, op, value))
            seed = changed
        changed = []
        for key, op, value in seed:
            if key in {'create_country_leader', 'promote_character'}:
                value = set_field(value, 'ideology', 'Western_Autocracy')
                if key == 'create_country_leader':
                    value = set_field(value, 'traits', [('_bare', '=', 'king'), ('_bare', '=', 'western_Western_Autocracy')])
            changed.append((key, op, value))
        seed = changed
    # Gulf characters must already be recruited when their outlook is selected.
    return seed


def history_outputs():
    for path in sorted((ROOT / 'history/countries').glob('*.txt')):
        if path.name.startswith('UAE - '):
            continue
        raw = path.read_bytes()
        # Preserve every byte from the native2000bookmark onwards.
        boundary = re.search(rb'(?m)^2000\.1\.1[ \t]*=', raw)
        prefix, tail = (raw[:boundary.start()], raw[boundary.start():]) if boundary else (raw, b'')
        source = prefix.decode('utf-8-sig')
        if SNAPSHOT_BEGIN not in source:
            continue
        begin = source.index(SNAPSHOT_BEGIN) + len(SNAPSHOT_BEGIN)
        end = source.index(SNAPSHOT_END)
        old = parse(source[begin:end])
        new = align_seed(old, path.name[:3])
        if new != old:
            source = source[:begin] + '\n' + emit(new, 1) + '\n\t' + source[end:]
        source = modern_identity_compatibility(source, path.name[:3])
        if source != prefix.decode('utf-8-sig'):
            yield path.relative_to(ROOT).as_posix(), b'\xef\xbb\xbf' + source.encode('utf-8') + tail


def profile_body():
    tree = parse((ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig'))
    body = first(tree, 'IMP_1970_profile_monarchist')
    # Same authored monarchist distribution, explicitly relocated in MD's
    # Western dynastic family. The general monarchist provider stays intact.
    from starting_identity import native_seed_prefix, profile_seed
    seed = [('set_country_flag', '=', 'IMP_1970_historical_politics')] + native_seed_prefix() + profile_seed(body)
    return align_seed(seed, 'BHR') + [('startup_politics', '=', 'yes')]


def world_output():
    path = 'common/scripted_effects/IMP_1970_world_politics_effects.txt'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    effect = next(n for n in nodes(text) if n['key'] == 'IMP_1970_apply_world_politics')
    changes = []
    for node in effect['children']:
        if node['key'] not in {'if', 'else_if'}:
            continue
        tag = first(first(node['value'], 'limit', []), 'original_tag')
        if tag not in corrections():
            continue
        body = text[node['start']:node['end']]
        assert ('IMP_1970_profile_monarchist = yes' in body or
                'COLDWAR_1970_profile_western_dynasty = yes' in body), tag
        body = body.replace('IMP_1970_profile_monarchist = yes', 'COLDWAR_1970_profile_western_dynasty = yes')
        body = body.replace('ideology = Monarchist', 'ideology = Western_Autocracy')
        leader = next(n for n in nodes(body)[0]['children'] if n['key'] == 'create_country_leader')
        traits = [('_bare', '=', 'king'), ('_bare', '=', 'western_Western_Autocracy')]
        value = set_field(leader['value'], 'traits', traits)
        body = body[:leader['start']] + 'create_country_leader = {\n' + emit(value, 3) + '\n\t\t}' + body[leader['end']:]
        changes.append((node['start'], node['end'], body))
    assert len(changes) == len(corrections())
    for begin, end, body in sorted(changes, reverse=True):
        text = text[:begin] + body + text[end:]
    return path, text


def party_outputs(world):
    """Use the canonical formatter only for the selected country branches."""
    from build import IDEOLOGIES, party_periods, context, window, block, loc_quote
    from party_presentation import PartyPresentation
    countries = {c['tag']: c for c in world['countries'] if c['tag'] in corrections()}
    icons = dict(re.findall(r'generic\.([^\s:]+)_icon:\s*"([^"]*)"',
                 (ROOT / 'localisation/english/0_political_system_l_english.yml').read_text(encoding='utf-8-sig')))
    manifest = json.loads((HERE / 'party_icon_manifest.json').read_text(encoding='utf-8'))
    presentation = PartyPresentation(countries, manifest, icons)
    newloc, branches = {}, {}
    for index in (0, 23):
        ideology = IDEOLOGIES[index]
        for tag, country in countries.items():
            parties = presentation.parties(tag, country['parties'])
            choices = party_periods(parties, index) + [p for p in parties if p['index'] == index and p.get('extra_trigger')]
            rows = []
            for number, party in reversed(list(enumerate(choices))):
                key = f'MDCW_HP_{tag}_party_{index}_{number}'
                label, icon = presentation.render(tag, ideology, party)
                newloc[key] = label
                newloc[key + '_desc'] = presentation.description(index, party.get('description', ''))
                newloc[key + '_icon'] = icon
                tests = context(tag) + '\n' + window(party.get('from', '1970.1.1'), party.get('until'))
                if party.get('extra_trigger'):
                    tests += '\n' + party['extra_trigger']
                rows.append((tests, key))
            key = f'MDCW_HP_{tag}_current_{index}'
            newloc[key] = icons[ideology] + ' ' + presentation.names[tag]['labels'][index]
            newloc[key + '_desc'] = presentation.description(index) + '\n\nAn alternative political current; this name does not imply that a separate registered party existed in 1970.'
            newloc[key + '_icon'] = icons[ideology]
            rows.append((context(tag), key))
            for suffix in ('', '_desc', '_icon'):
                branches[(f'MDCW_HP_{ideology}{suffix}', tag)] = '\n'.join(
                    '\t' + block('text', block('trigger', tests) + '\nlocalization_key = ' + name + suffix).replace('\n', '\n\t')
                    for tests, name in rows)
    path = 'common/scripted_localisation/mdcw_historical_parties.txt'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    changes = []
    for definition in nodes(text):
        if definition['key'] != 'defined_text':
            continue
        name = first(definition['value'], 'name')
        inserted = set()
        for node in definition['children']:
            if node['key'] != 'text':
                continue
            tag = first(first(node['value'], 'trigger', []), 'original_tag')
            if (name, tag) not in branches:
                continue
            replacement = branches[(name, tag)] + '\n' if tag not in inserted else ''
            inserted.add(tag)
            line_begin = text.rfind('\n', 0, node['start']) + 1
            line_end = text.find('\n', node['end'])
            line_end = len(text) if line_end < 0 else line_end + 1
            assert not text[line_begin:node['start']].strip()
            assert not text[node['end']:line_end].strip()
            changes.append((line_begin, line_end, replacement))
    assert len({(name, tag) for name, tag in branches}) == len(corrections()) * 6
    for begin, end, replacement in sorted(changes, reverse=True):
        text = text[:begin] + replacement + text[end:]
    # Removed old text branches leave whitespace-only lines. Canonicalize only
    # that whitespace so repeated bounded generation cannot accumulate gaps.
    text = re.sub(r'(?m)^[\t ]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    yield path, text
    path = 'localisation/english/mdcw_historical_politics_1970_l_english.yml'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    tags = '|'.join(sorted(corrections()))
    pattern = r'(?m)^ MDCW_HP_(?:' + tags + r')_(?:party_(?:0|23)_\d+|current_(?:0|23))(?:_desc|_icon)?:0[^\n]*\n'
    matches = list(re.finditer(pattern, text))
    assert matches
    insertion = ''.join(' ' + key + ':0 ' + loc_quote(value) + '\n' for key, value in newloc.items())
    first_position = matches[0].start()
    for match in reversed(matches):
        text = text[:match.start()] + text[match.end():]
    text = text[:first_position] + insertion + text[first_position:]
    yield path, text


def build():
    outputs = {}
    worldpath = HERE / 'data/world.json'
    world = apply_world(json.loads(worldpath.read_text(encoding='utf-8-sig')))
    outputs[worldpath.relative_to(ROOT).as_posix()] = dump(world)
    namespath = HERE / 'data_party_names_americas_middleeast.json'
    names = json.loads(namespath.read_text(encoding='utf-8-sig'))
    for tag, patch in corrections().items():
        names['countries'][tag]['labels'][0] = patch['fallback_0']
        names['countries'][tag]['labels'][23] = patch['fallback_23']
    outputs[namespath.relative_to(ROOT).as_posix()] = dump(names)
    # party_outputs reads canonical labels; use the planned labels directly.
    from unittest.mock import patch
    from party_presentation import load_names
    planned_names = load_names()
    for tag, value in names['countries'].items():
        if tag in corrections():
            planned_names[tag] = value
    with patch('party_presentation.load_names', return_value=planned_names):
        outputs.update(party_outputs(world))
    outputs.update(history_outputs())
    outputs.update([world_output()])
    outputs['common/scripted_effects/COLDWAR_1970_western_dynasties.txt'] = (
        '# Keyed native MD Western-autocratic dynasties; starting_identity/monarchy_alignment tools own this provider.\n' +
        'COLDWAR_1970_profile_western_dynasty = {\n' + emit(profile_body(), 1) + '\n}\n')
    path = 'common/characters/mdcw_gulf_1970.txt'
    text = (ROOT / path).read_text(encoding='utf-8-sig')
    changes = []
    characters = next(n for n in nodes(text) if n['key'] == 'characters')
    for character in characters['children']:
        if character['key'] not in {'BHR_MDCW_1970_incumbent', 'KUW_MDCW_1970_incumbent'}:
            continue
        role = next(n for n in character['children'] if n['key'] == 'country_leader')
        value = set_field(role['value'], 'ideology', 'Western_Autocracy')
        value = set_field(value, 'traits', [('_bare', '=', 'king'), ('_bare', '=', 'western_Western_Autocracy')])
        changes.append((role['start'], role['end'], 'country_leader = {\n' + emit(value, 3) + '\n\t\t}'))
    for begin, end, body in sorted(changes, reverse=True):
        text = text[:begin] + body + text[end:]
    outputs[path] = text
    path = 'docs/gulf_start_1970_portraits_20261019.json'
    roster = json.loads((ROOT / path).read_text(encoding='utf-8'))
    for row in roster['items']:
        if row['tag'] in {'BHR', 'KUW'}:
            row['ideology'] = 'Western_Autocracy'
            row['native_md_alignment'] = corrections()[row['tag']]['native_reference']
    outputs[path] = dump(roster)
    path = 'tools/historical_politics_1970/party_inventory.json'
    inventory = json.loads((ROOT / path).read_text(encoding='utf-8'))
    for row in inventory['countries']:
        if row['tag'] in corrections():
            row.update(ruling_party_index=0, index_label='Western_Autocracy',
                       native_md_alignment=corrections()[row['tag']]['native_reference'])
    outputs[path] = dump(inventory)
    # Keep original audit baselines, update only the verified final signatures.
    for path in ('docs/audits/1970_starting_identity.json', 'docs/regional_starting_rulers_1970_20261019.json'):
        previous_text = (ROOT / path).read_text(encoding='utf-8')
        report = json.loads(previous_text)
        for row in report['countries']:
            history = row.get('history')
            if history and history in outputs:
                raw = outputs[history]
                row['after_sha256'] = hashlib.sha256(raw).hexdigest()
            if row['tag'] in corrections():
                row.update(ideology='Western_Autocracy', party_index=0,
                           native_md_alignment=corrections()[row['tag']]['native_reference'])
        outputs[path] = dump(report).rstrip('\n') + ('\n' if previous_text.endswith('\n') else '')
    # Replace only our own scoped JOR cosmetic guard, preserving the UAE marker.
    path = 'common/on_actions/00_on_actions.txt'
    source = (ROOT / path).read_text(encoding='utf-8-sig')
    source = source.replace('original_tag = JOR has_cosmetic_tag = JOR_AUTH has_government = nationalist',
                            'original_tag = JOR has_cosmetic_tag = JOR_AUTH has_government = democratic')
    outputs[path] = source
    return outputs


def install():
    changed = []
    for name, value in build().items():
        path = ROOT / name
        raw = output_bytes(path, value)
        if not path.exists() or path.read_bytes() != raw:
            path.parent.mkdir(parents=True, exist_ok=True)
            # Replace a complete staged file rather than truncating a loaded
            # history file while the launcher/game may be reading it.
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.coldwar_identity_', suffix='.tmp', delete=False) as staged:
                staged.write(raw)
                temporary = staged.name
            os.replace(temporary, path)
            changed.append(name)
    return changed


def output_bytes(path, value):
    if isinstance(value, bytes):
        return value
    # HOI localisation requires BOM. Script text can use either native style;
    # preserve an existing caller/compiler's choice rather than churn bytes.
    existing = path.read_bytes() if path.exists() else b''
    bom = path.suffix == '.yml' or (path.suffix == '.txt' and existing.startswith(b'\xef\xbb\xbf'))
    if b'\r\n' in existing and b'\n' not in existing.replace(b'\r\n', b''):
        value = value.replace('\r\n', '\n').replace('\n', '\r\n')
    return value.encode('utf-8-sig' if bom else 'utf-8')


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--install', action='store_true')
    args = cli.parse_args()
    if args.install:
        print(json.dumps({'changed': install()}))
    else:
        print(json.dumps({'planned_outputs': list(build())}))
