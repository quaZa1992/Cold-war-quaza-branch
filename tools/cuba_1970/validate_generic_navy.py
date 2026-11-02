# IMPERIA COLD WAR — Independent donor parity and integration checks for Cuba's navy.
"""Compare loaded output to frozen original MD ASTs, with explicit adaptation limits."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/vietnam_1970'))
from script_ast import parse, first, values, walk


def main():
    source = json.loads((HERE/'GENERIC_NAVY_SOURCE.json').read_text(encoding='utf8'))
    donor = {record['id']: parse(record['script']) for record in source['focuses']}
    reverse = {key.replace('GENERIC_', 'COLDWAR_CUB_GEN_', 1): key for key in donor}
    raw = (ROOT/'common/national_focus/COLDWAR_CUB_1970_focus.txt').read_bytes()
    tree = first(parse(raw.decode('utf8')), 'focus_tree')
    all_nodes = values(tree, 'focus')
    by = {first(n, 'id'): n for n in all_nodes}
    errors, checks = [], 0

    def check(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            errors.append(message)

    def undo(rows):
        result = []
        for key, operator, value in rows:
            if isinstance(value, list):
                value = undo(value)
            elif value in reverse:
                value = reverse[value]
            elif key == 'log':
                for new, old in sorted(reverse.items(), key=lambda row: -len(row[0])):
                    value = value.replace(new, old)
            if key == 'COLDWAR_CUB_GEN_one_random_composite_plant':
                key = 'one_random_composite_plant'
            result.append((key, operator, value))
        return result

    check(len(source['naval_ids']) == 20 and len(donor) == 26, 'The full twenty-focus naval branch and six feeders are required')
    check(len(all_nodes) == len(by) == 146, 'Expected 146 unique loaded focuses')
    check(set(reverse) <= by.keys(), 'Imported focus missing from the loaded tree')
    root_ids = {'GENERIC_naval_reform', 'GENERIC_light_industry_investments', 'GENERIC_air_force_reform'}
    for new_id, old_id in reverse.items():
        if new_id not in by:
            continue
        actual = undo(by[new_id])
        expected = donor[old_id]
        if old_id in root_ids:
            actual = [r for r in actual if r[0] not in ('x', 'y')]
            expected = [r for r in expected if r[0] not in ('x', 'y')]
        if old_id == 'GENERIC_naval_bases':
            state = first(first(actual, 'completion_reward'), 'random_owned_controlled_state')
            position = next(i for i, row in enumerate(state) if row[0] == 'construct_building_in_random_province')
            check(state[position-1] == ('add_extra_state_shared_building_slots', '=', '1'), 'Naval base must gain its slot in the same state before construction')
            state.pop(position-1)
        if old_id == 'GENERIC_light_industry_investments':
            state = first(first(actual, 'completion_reward'), 'capital_scope')
            check(first(state, 'add_extra_state_shared_building_slots') == '2', 'Light industry must grant two slots for two building levels')
            state[:] = [(k, op, '1' if k == 'add_extra_state_shared_building_slots' else v) for k, op, v in state]
        check(actual == expected, 'Unapproved donor mechanic, cost, geometry or prerequisite change: '+new_id)

    # Complete dependency closure, declaration-first anchors, and all card rows.
    coordinates, seen = {}, set()
    def resolve(key, active=()):
        if key in coordinates:
            return coordinates[key]
        check(key not in active, 'Cyclic relative anchor: '+key)
        node = by[key]
        x, y = int(first(node, 'x')), int(first(node, 'y'))
        anchor = first(node, 'relative_position_id')
        if anchor:
            ax, ay = resolve(anchor, active+(key,))
            x, y = x+ax, y+ay
        coordinates[key] = (x, y)
        return x, y
    for node in all_nodes:
        key = first(node, 'id')
        anchor = first(node, 'relative_position_id')
        check(not anchor or anchor in seen, 'Relative anchor declared too late: '+key)
        seen.add(key)
        for group in values(node, 'prerequisite') + values(node, 'mutually_exclusive'):
            for other in values(group, 'focus'):
                check(other in by, 'Dangling focus link: '+key+' -> '+other)
        check(first(node, 'allow_branch') is None, 'An imported party branch was hidden')
        resolve(key)
    check(len(set(coordinates.values())) == 146, 'Overlapping focus coordinates')
    for key, node in by.items():
        for group in values(node, 'prerequisite'):
            for parent in values(group, 'focus'):
                check(coordinates[parent][1] < coordinates[key][1], 'Prerequisite must be above its continuation: '+parent+' -> '+key)
    ordered = list(coordinates.items())
    for i, (key, (x, y)) in enumerate(ordered):
        for other, (ox, oy) in ordered[i+1:]:
            if y == oy:
                check(abs(x-ox)*96 >= 165, 'Overlapping native focus cards: '+key+' / '+other)

    helpers_raw = (ROOT/'common/scripted_effects/COLDWAR_CUB_1970_generic_navy.txt').read_bytes()
    helper = first(parse(helpers_raw.decode('utf8')), 'COLDWAR_CUB_GEN_one_random_composite_plant')
    state = first(helper, 'every_controlled_state')
    slot_index = next(i for i, row in enumerate(state) if row[0] == 'add_extra_state_shared_building_slots')
    build_index = next(i for i, row in enumerate(state) if row[0] == 'add_building_construction')
    check(slot_index < build_index, 'Composite plant slot must precede construction')
    original = parse(source['composite_helper'])
    check(sorted(first(original, 'every_controlled_state'), key=str) == sorted(state, key=str), 'Composite state effects differ from native donor')
    check([r for r in helper if r[0] != 'every_controlled_state'] == [r for r in original if r[0] != 'every_controlled_state'], 'Composite payment or guards differ from native donor')

    loc_raw = (ROOT/'localisation/english/COLDWAR_CUB_1970_l_english.yml').read_bytes()
    check(loc_raw.startswith(b'\xef\xbb\xbf'), 'Localisation requires UTF-8 BOM')
    text = loc_raw.decode('utf-8-sig')
    for new_id, old_id in reverse.items():
        for suffix in ('', '_desc'):
            match = re.search(r'(?m)^ '+re.escape(new_id+suffix)+r':0 "(.*)"$', text)
            check(match is not None, 'Missing English donor localisation: '+new_id+suffix)
            if match:
                actual = json.loads('"'+match[1]+'"')
                expected = source['localisation'][old_id+suffix]
                expected = expected.replace(' \u2014 ', '. ').replace(' \u2013 ', ': ').replace('\u2014', ':').replace('\u2013', '-')
                check(actual == expected, 'Changed English donor localisation: '+new_id+suffix)
    check(not raw.startswith(b'\xef\xbb\xbf') and not helpers_raw.startswith(b'\xef\xbb\xbf'), 'Script BOM is invalid')
    report = dict(project='IMPERIA COLD WAR', status='fail' if errors else 'pass', checks=checks, errors=errors,
                  base_cuba_focuses=120, naval_focuses=20, required_feeders=6, total_focuses=146,
                  source_sha256=source['source_sha256'], output_sha256=hashlib.sha256(raw).hexdigest(),
                  allowed_adaptations=['Unique Cuba IDs and English localisation keys', 'Three section-root positions', 'One slot per building level, before construction'],
                  native_game_tested=False)
    (HERE/'GENERIC_NAVY_VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
