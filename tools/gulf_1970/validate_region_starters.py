# IMPERIA CW — Cold War: gulf 1970 — validate region starters.
"""Check actual regional history snapshots, portrait bindings and MD slots."""
from pathlib import Path
import hashlib
import json
import re
import sys

from PIL import Image

from repair_region_starters import ROOT, TAGS, parse, first, values, walk


def main():
    path = ROOT / 'docs/regional_starting_rulers_1970_20261019.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        assert condition, message

    def read(relative):
        return parse((ROOT / relative).read_text(encoding='utf-8-sig'))

    ideologies = first(read('common/ideologies/00_ideologies.txt'), 'ideologies')
    groups = {ideology: group for group, op, definition in ideologies
              if isinstance(definition, list) for ideology, op, definition in first(definition, 'types', [])}
    check({row['tag'] for row in report['countries']} == set(TAGS), 'Regional coverage mismatch')
    backup_root = Path(report['backup_root'])
    gulf = json.loads((ROOT / 'docs/gulf_start_1970_portraits_20261019.json').read_text(encoding='utf-8'))['items']
    gulf_by_token = {row['token']: row for row in gulf}
    revised_roles = {tag: ('Western_Autocracy', 0) for tag in ('BHR', 'JOR', 'KUW', 'UAE', 'PER')}
    for row in report['countries']:
        tag = row['tag']
        expected_ideology, expected_slot = revised_roles.get(tag, (row['ideology'], row['party_index']))
        raw = (ROOT / row['history']).read_bytes()
        history = parse(raw.decode('utf-8-sig'))
        starters = values(history, '1970.1.1')
        direct = [(node, leader) for node in starters for leader in values(node, 'create_country_leader')]
        for node in starters:
            promotion = first(node, 'promote_character')
            if promotion is None:
                continue
            token = first(promotion, 'character')
            check(first(node, 'recruit_character') == token, (tag, 'promoted but not recruited'))
            character = gulf_by_token[token]
            direct.append((node, [('name', '=', json.dumps(character['name'], ensure_ascii=False)),
                                  ('picture', '=', json.dumps(character['portrait'])),
                                  ('ideology', '=', first(promotion, 'ideology'))]))
        check(len(direct) == 1, (tag, 'missing/competing direct starting ruler'))
        node, leader = direct[0]
        check(first(leader, 'name').strip('"') == row['name'], (tag, 'wrong starting identity'))
        check(first(leader, 'ideology') == expected_ideology, (tag, 'wrong starting ideology'))
        all_created = [value for starter in starters for key, op, value in walk(starter) if key == 'create_country_leader']
        check(len(all_created) + sum(first(node, 'promote_character') is not None for node in starters) == 1,
              (tag, 'duplicate conditional starting ruler'))
        politics = first(node, 'set_politics')
        check(politics is not None, (tag, 'outlook still hidden in conditional initialization'))
        check(first(politics, 'ruling_party') == groups[expected_ideology], (tag, 'ruler is in an inactive outlook'))
        check(any(first(variable, 'ruling_party') == str(expected_slot) for variable in values(node, 'set_variable')),
              (tag, 'MD party slot missing or mismatched'))
        portrait = first(leader, 'picture').strip('"')
        check(portrait == row['portrait'] and (ROOT / portrait).is_file(), (tag, 'missing/wrong portrait file'))
        with Image.open(ROOT / portrait) as image:
            image.load()
            check(image.size == (156, 210), (tag, 'unexpected portrait dimensions', image.size))
            check(len(image.convert('RGB').getcolors(100000) or []) > 100, (tag, 'empty/flat portrait'))
        boundary = re.search(rb'(?m)^2000\.1\.1[ \t]*=', raw)
        later = raw[boundary.start():] if boundary else b''
        check(hashlib.sha256(later).hexdigest() == row['later_history_sha256'], (tag, 'later bookmark bytes changed'))
        old_path = backup_root / row['history']
        if old_path.exists():
            old = old_path.read_bytes()
            boundary_old = re.search(rb'(?m)^2000\.1\.1[ \t]*=', old)
            check((old[boundary_old.start():] if boundary_old else b'') == later, (tag, 'later history differs from backup'))
            old_tree = parse(old.decode('utf-8-sig'))
            # The repair must leave country content and authored regional
            # initializers in place, including existing guest-worker ideas.
            critical = {'load_focus_tree', 'add_ideas', 'set_cosmetic_tag', 'set_oob', 'set_naval_oob', 'set_air_oob',
                        'ISR70_initialize', 'COLDWAR_EGY_initialize_1970', 'COLDWAR_IRQ_seed_starting_spirits'}
            # Direct identity repair moves the same cosmetic before politics.
            # Preserve other mechanics in order and cosmetic values separately.
            previous = [(k, op, v) for k, op, v in walk(old_tree) if k in critical and k != 'set_cosmetic_tag']
            current = [(k, op, v) for k, op, v in walk(history) if k in critical and k != 'set_cosmetic_tag']
            if tag != 'UAE':
                check(previous == current, (tag, 'regional content changed during ruler repair'))
                check(values(list(walk(old_tree)), 'set_cosmetic_tag') == values(list(walk(history)), 'set_cosmetic_tag'),
                      (tag, 'historical cosmetics changed during ruler repair'))
        setter = ROOT / 'common/scripted_effects' / (tag + '_political_leaders.txt')
        if setter.exists():
            tree = parse(setter.read_text(encoding='utf-8-sig'))
            check(first(tree, 'set_leader_' + tag) is not None, (tag, 'native selector not at top level'))
            check('# MDCW HISTORICAL NATIVE POOL END ' + tag + '}' not in setter.read_text(encoding='utf-8-sig'),
                  (tag, 'commented-out selector closing brace'))
    # A potential tag must not acquire territory just to get a ruler entry.
    ncy = next(row for row in report['countries'] if row['tag'] == 'NCY')
    snapshot = values(read(ncy['history']), '1970.1.1')
    check(not any(key in {'release', 'release_puppet', 'transfer_state', 'set_state_owner'}
                  for node in snapshot for key, op, value in walk(node)), 'Potential NCY was spawned')
    # The direct preview slot must not block its existing full political seed.
    initialization = first(read('common/scripted_effects/COLDWAR_NCY_1970_effects.txt'), 'COLDWAR_NCY_1970_initialize')
    root_if = first(initialization, 'if')
    seeding = next(node for node in values(root_if, 'if') if first(node, 'IMP_1970_profile_democratic_conservative') == 'yes')
    alternatives = first(first(seeding, 'limit'), 'OR')
    check(alternatives is not None and len(values(alternatives, 'NOT')) == 2,
          'NCY direct preview slot blocks political initialization')
    check(any(first(node, 'has_variable') == 'ruling_party' for node in values(alternatives, 'NOT'))
          and any(first(node, 'has_country_flag') == 'IMP_1970_historical_politics' for node in values(alternatives, 'NOT')),
          'NCY seed guard is not tied to real preset initialization')
    for has_slot, seeded, expected in [(False, False, True), (True, False, True), (True, True, False), (False, True, True)]:
        check((not has_slot or not seeded) == expected, ('NCY seed state', has_slot, seeded))
    generator = (ROOT / 'tools/cyprus_1970/north.py').read_text(encoding='utf-8')
    check('OR = { NOT = { has_variable = ruling_party } NOT = { has_country_flag = IMP_1970_historical_politics } }' in generator,
          'NCY generator loses the seed repair')
    # The authored UAE provider precedes the legacy historical pool. Its Council
    # lasts until actual federation; native retirement selects its presidency.
    uae = next(row for row in report['countries'] if row['tag'] == 'UAE')
    uae_start = first(read(uae['history']), '1970.1.1')
    council = first(uae_start, 'create_country_leader')
    check(first(council, 'name') == '"Trucial States Council"' and first(council, 'expire') is None,
          'UAE Council must not expire automatically in1971')
    check(first(uae_start, 'promote_character') is None and first(uae_start, 'recruit_character') is None,
          'UAE uses an obsolete recruited/promoted Council instead of its canonical provider')
    check(any(k == 'load_focus_tree' and v == 'COLDWAR_UAE_1970_focus' for k, _, v in walk(uae_start)),
          'UAE lost its authored focus tree')
    effects = read('common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt')
    provider = first(effects, 'COLDWAR_UAE_set_monarchist_leader')
    created = [v for k, _, v in walk(provider) if k == 'create_country_leader']
    check({first(v, 'ideology') for v in created} == {'Western_Autocracy', 'Monarchist'}
          and all(first(v, 'expire') is None for v in created), 'UAE exact native subtypes or durable office providers changed')
    check({first(v, 'name').strip('"') for v in created} >= {'Trucial States Council', 'Zayed bin Sultan Al Nahyan', 'Rashid bin Saeed Al Maktoum'},
          'UAE historical presidency choices disappeared')
    succession = first(effects, 'COLDWAR_UAE_set_leader')
    check(any(k == 'COLDWAR_UAE_set_monarchist_leader' for k, _, _ in walk(succession)),
          'UAE leader dispatch no longer reaches its authored presidency provider')
    dispatcher = (ROOT / 'common/scripted_effects/00_leader_setup_scripted_effects.txt').read_text(encoding='utf-8-sig')
    check(dispatcher.index('COLDWAR_UAE_set_leader = yes') < dispatcher.index('kill_country_leader = yes'),
          'Native dispatcher removes the UAE provider before its authored route')
    report['validation'] = {'passed': True, 'checks': checks, 'native_game_runtime_tested': False,
                            'countries': len(TAGS), 'new_direct_snapshots': sum(row['new_direct_snapshot'] for row in report['countries']),
                            'repaired_selectors': len(report['repaired_setters']),
                            'native_outlook_revisions': {tag: {'ideology': value[0], 'party_index': value[1]}
                                                         for tag, value in revised_roles.items()}}
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report['validation']))


if __name__ == '__main__':
    main()
