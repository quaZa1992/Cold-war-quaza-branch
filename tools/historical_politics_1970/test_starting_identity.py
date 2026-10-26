# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Source/AST regressions for native 1970 history snapshots and callbacks."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from unittest.mock import patch

from starting_identity import (ROOT, SNAPSHOT_BEGIN, SNAPSHOT_END, IDEOLOGIES,
    callback_outputs, history_output, identity_nodes, nodes, parse, first, values, walk,
    MODERN_DEFAULT_RESTORES, MODERN_BEGIN)


def without_identity(source):
    if SNAPSHOT_BEGIN in source:
        source = re.sub(re.escape(SNAPSHOT_BEGIN) + '.*?' + re.escape(SNAPSHOT_END), '', source, flags=re.S)
    removals = [node for date in nodes(source) if date['key'] == '1970.1.1'
                for node in identity_nodes(date['children'])]
    for node in sorted(removals, key=lambda n: n['start'], reverse=True):
        source = source[:node['start']] + source[node['end']:]
    return parse(source)


def later(raw):
    match = re.search(rb'(?m)^2000\.1\.1[ \t]*=', raw)
    return raw[match.start():] if match else b''


def main():
    checks = 0
    def check(ok, message):
        nonlocal checks
        checks += 1
        assert ok, message
    profiles = parse((ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig'))
    ideology_groups = first(parse((ROOT / 'common/ideologies/00_ideologies.txt').read_text(encoding='utf-8-sig')), 'ideologies')
    groups = {ideology: group for group, _, body in ideology_groups
              if isinstance(body, list) for ideology, _, _ in first(body, 'types', [])}
    active = set()
    for path in (ROOT / 'history/states').glob('*.txt'):
        history = first(first(parse(path.read_text(encoding='utf-8-sig')), 'state'), 'history', [])
        owner = first(history, 'owner')
        for key, _, value in history:
            if isinstance(value, list) and re.fullmatch(r'\d+\.\d+\.\d+', key) and tuple(map(int, key.split('.'))) <= (1970, 1, 1):
                owner = first(value, 'owner', owner)
        if owner:
            active.add(owner)
    report_path = ROOT / 'docs/audits/1970_starting_identity.json'
    report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else None
    report_rows = {r['tag']: r for r in report['countries']} if report else {}
    covered, dormant, direct_before, missing_before = set(), set(), 0, 0
    for path in sorted((ROOT / 'history/countries').glob('*.txt')):
        tag = path.name[:3]
        if tag == 'UAE':
            continue
        before = path.read_bytes()
        output, row = history_output(path, profiles)
        if output is None:
            dormant.add(tag)
            check(tag not in active, (tag, 'active country lacks existing authored incumbent'))
            continue
        covered.add(tag)
        after = parse(output.decode('utf-8-sig'))
        starts = values(after, '1970.1.1')
        seed = next(block for block in starts if first(block, 'set_popularities') is not None)
        incumbents = [(k, v) for block in starts for k, _, v in block if k in {'create_country_leader', 'promote_character'}]
        check(len(incumbents) == 1, (tag, 'direct incumbent missing or duplicated'))
        check(sum(k in {'create_country_leader', 'promote_character'} for block in starts for k, _, _ in walk(block)) == 1,
              (tag, 'conditional competing incumbent'))
        ideology = first(incumbents[0][1], 'ideology')
        index = IDEOLOGIES.index(ideology)
        ruling = next(first(v, 'ruling_party') for v in values(seed, 'set_variable') if first(v, 'ruling_party') is not None)
        check(int(ruling) == index, (tag, 'wrong MD ruling subtype'))
        check(first(first(seed, 'set_politics'), 'ruling_party') == groups[ideology], (tag, 'inactive incumbent outlook'))
        array_seed = seed
        if tag == 'LEB':
            guard = next(v for v in values(seed, 'if') if any(k == 'resize_array' for k, _, _ in v))
            check(first(first(guard, 'limit'), 'IMP_is_1970_scenario') == 'yes', 'LEB array seed lacks1970guard')
            array_seed = guard
        check(any(first(v, 'array') == 'party_pop_array' and first(v, 'size') == '24' for v in values(array_seed, 'resize_array')),
              (tag, 'missing native party array'))
        support = {k: v for entry in values(array_seed, 'set_variable') for k, _, v in entry if k.startswith('party_pop_array^')}
        check(float(support.get('party_pop_array^' + str(index), '0')) > 0, (tag, 'ruling party has no seed support'))
        check(not any(k.startswith('IMP_1970_profile_') for block in starts for k, _, _ in walk(block)),
              (tag, 'identity still requires helper execution'))
        check(later(before) == later(output), (tag, 'native later history bytes altered'))
        check(without_identity(before.decode('utf-8-sig')) == without_identity(output.decode('utf-8-sig')),
              (tag, 'unrelated history effects changed'))
        check(output.decode('utf-8-sig').count(SNAPSHOT_BEGIN) == 1, (tag, 'snapshot marker count'))
        check(first(seed, 'set_country_flag') != 'IMP_1970_historical_politics', (tag, 'historical flag leaks into later bookmarks'))
        guards = [body for body in values(seed, 'if') if first(body, 'set_country_flag') == 'IMP_1970_historical_politics']
        check(len(guards) == 1 and first(first(guards[0], 'limit'), 'IMP_is_1970_scenario') == 'yes',
              (tag, 'historical flag lacks exact scenario guard'))
        for scenario in (False, True):
            flags, leaders_seen = set(), []
            def execute(rows):
                for key, _, value in rows:
                    if key == 'set_country_flag':
                        flags.add(value)
                    elif key in {'create_country_leader', 'promote_character'}:
                        leaders_seen.append(value)
                    elif key == 'if':
                        condition = first(value, 'limit', [])
                        if first(condition, 'IMP_is_1970_scenario') == 'yes' and scenario:
                            execute([(k, o, v) for k, o, v in value if k != 'limit'])
            execute(seed)
            check(('IMP_1970_historical_politics' in flags) == scenario and len(leaders_seen) == 1,
                  (tag, scenario, 'preview leader depends on flag or flag leaks'))
        # Every actual referenced portrait/character must already exist.
        if incumbents[0][0] == 'create_country_leader':
            picture = first(incumbents[0][1], 'picture').strip('"')
            check((ROOT / picture).is_file(), (tag, 'missing authored portrait', picture))
        else:
            token = first(incumbents[0][1], 'character')
            check(first(seed, 'recruit_character') == token, (tag, 'unrecruited historical character'))
        if report and tag in report_rows and 'after_sha256' in report_rows[tag]:
            check(hashlib.sha256(before).hexdigest() == report_rows[tag]['after_sha256'], (tag, 'installed snapshot drift'))
            check(hashlib.sha256(later(before)).hexdigest() == report_rows[tag]['later_sha256'], (tag, 'later bookmark drift'))
    check(active - {'UAE'} <= covered, 'active country coverage incomplete')
    check(len(active) == 163 and len(covered) == 163 and len(dormant) == 233, 'country coverage changed; review inventory')
    # Exercise a fresh, unmarked authored input instead of only the installed
    # marker path. Gulf promotion requires recruitment before set_politics.
    fresh = b'''capital = 423\n1970.1.1 = {
if = { limit = { date < 1985.1.1 } IMP_1970_profile_monarchist = yes }
recruit_character = BHR_MDCW_1970_incumbent
set_politics = { ruling_party = nationalist elections_allowed = no }
set_variable = { ruling_party = 23 }
promote_character = { character = BHR_MDCW_1970_incumbent ideology = Monarchist }
}\n2000.1.1 = { set_country_flag = modern_tail_sentinel }\n'''
    path = next((ROOT / 'history/countries').glob('BHR - *.txt'))
    with patch.object(Path, 'read_bytes', return_value=fresh):
        transformed, _ = history_output(path, profiles)
    seed = first(parse(transformed.decode('utf-8-sig')), '1970.1.1')
    keys = [key for key, _, _ in seed]
    check(keys.index('recruit_character') < keys.index('set_politics') < keys.index('promote_character'),
          'Fresh Gulf transformation regressed native recruitment order')
    check(first(seed, 'set_country_flag') is None and
          first(first(first(seed, 'if'), 'limit'), 'IMP_is_1970_scenario') == 'yes',
          'Fresh snapshot leaks runtime historical flag')
    check(later(fresh) == later(transformed), 'Fresh transformation changed modern sentinel')
    # Only four promoted cosmetics lack a native modern restore. The setup
    # boundary is future-dated in a1970 start and cannot overwrite a different
    # cosmetic or execute as a runtime on-action in that campaign.
    for tag, cosmetic in MODERN_DEFAULT_RESTORES.items():
        path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        text = path.read_text(encoding='utf-8-sig')
        tree = parse(text)
        compat = first(tree, '1999.12.31')
        check(text.count(MODERN_BEGIN) == 1 and compat is not None, (tag, 'modern identity compatibility absent/duplicated'))
        action = first(compat, 'if')
        condition = first(action, 'limit')
        check(first(first(condition, 'NOT'), 'IMP_is_1970_scenario') == 'yes' and
              first(condition, 'has_cosmetic_tag') == cosmetic and first(action, 'drop_cosmetic_tag') == 'yes',
              (tag, 'modern identity compatibility scope widened'))
        for scenario, start_date, initial in [(True, (1970, 1, 1), cosmetic),
                                              (False, (2000, 1, 1), cosmetic),
                                              (False, (2000, 1, 1), 'unrelated_manual_cosmetic'),
                                              (True, (2000, 1, 1), cosmetic)]:
            current = initial
            if start_date >= (1999, 12, 31) and not scenario and current == cosmetic:
                current = None
            expected = None if not scenario and initial == cosmetic else initial
            check(current == expected, (tag, scenario, start_date, 'modern name or1970 identity changed'))
        # Exercise fresh source as well as migrated installed markers.
        raw = (f'capital = 1\n1970.1.1 = {{ if = {{ limit = {{ date < 1985.1.1 }} '
               f'IMP_1970_profile_communist_state = yes set_cosmetic_tag = {cosmetic} '
               'create_country_leader = { name = "Existing incumbent" picture = "existing.dds" ideology = communist_state } } }\n'
               '2000.1.1 = { set_country_flag = modern_tail_sentinel }\n').encode('utf-8')
        with patch.object(Path, 'read_bytes', return_value=raw):
            fresh_result, _ = history_output(path, profiles)
        check(fresh_result.decode('utf-8-sig').count(MODERN_BEGIN) == 1 and later(raw) == later(fresh_result),
              (tag, 'fresh source lost modern compatibility or native tail'))
    # Canonical callback builder must reproduce its own installed markers.
    for name, value in callback_outputs():
        check(parse(value) == parse((ROOT / name).read_text(encoding='utf-8-sig')), (name, 'callback patch not idempotent'))
    world = (ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig')
    begin = world.index('set_global_flag = COLDWAR_1970_initial_treaty_setup')
    end = world.index('clr_global_flag = COLDWAR_1970_initial_treaty_setup')
    for tag in ('BHR', 'QAT', 'UAE', 'BRU', 'TON'):
        check(begin < world.index('set_autonomy = { target = ' + tag, begin) < end, (tag, 'initial subject outside bounded flag'))
    print(json.dumps({'ok': True, 'checks': checks, 'country_files': 397, 'active_1970_tags': len(active),
                      'direct_identities_owned': len(covered), 'uae_delegated': 1,
                      'dormant_placeholders_untouched': len(dormant), 'native_game_runtime_tested': False}))


if __name__ == '__main__':
    main()
