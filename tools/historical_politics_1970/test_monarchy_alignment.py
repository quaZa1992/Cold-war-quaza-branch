# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Check direct history, numeric conservation and native political UI leaves."""
from __future__ import annotations
import json
import re

from apply_monarchy_alignment import ROOT, build, align_seed, profile_body, output_bytes
from monarchy_alignment import corrections, apply_world
from starting_identity import parse, first, values, walk


def main():
    checks = 0
    def check(condition, message):
        nonlocal checks
        checks += 1
        assert condition, message
    patches = corrections()
    check(set(patches) == {'BHR', 'JOR', 'KUW', 'PER'}, 'Correction scope drift')
    world = json.loads((ROOT / 'tools/historical_politics_1970/data/world.json').read_text(encoding='utf-8-sig'))
    countries = {c['tag']: c for c in world['countries']}
    check(apply_world(world) == world, 'Canonical catalogue overlay not idempotent')
    profiles = parse((ROOT / 'common/scripted_effects/IMP_1970_world_politics_effects.txt').read_text(encoding='utf-8-sig'))
    old_profile = first(profiles, 'IMP_1970_profile_monarchist')
    old_support = {k: float(v) for row in values(old_profile, 'set_variable') for k, _, v in row if k.startswith('party_pop_array^')}
    old_broad = {k: float(v) for k, _, v in first(old_profile, 'set_popularities')}
    loc = dict(re.findall(r'(?m)^ ([^\s:]+):0 "(.*)"$',
               (ROOT / 'localisation/english/mdcw_historical_politics_1970_l_english.yml').read_text(encoding='utf-8-sig')))
    registry = parse((ROOT / 'common/scripted_localisation/mdcw_historical_parties.txt').read_text(encoding='utf-8-sig'))
    world_effect = first(profiles, 'IMP_1970_apply_world_politics')
    for tag, patch in patches.items():
        history_path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        snapshot = first(parse(history_path.read_text(encoding='utf-8-sig')), '1970.1.1')
        check(first(first(snapshot, 'set_politics'), 'ruling_party') == 'democratic', (tag, 'wrong starting outlook'))
        support = {k: float(v) for row in values(snapshot, 'set_variable') for k, _, v in row if k.startswith('party_pop_array^')}
        check(support['party_pop_array^0'] == old_support['party_pop_array^23'] and
              support['party_pop_array^23'] == old_support['party_pop_array^0'], (tag, 'dynastic support not conserved'))
        check(all(v == support[k] for k, v in old_support.items() if k not in {'party_pop_array^0', 'party_pop_array^23'}),
              (tag, 'unrelated party support changed'))
        check(abs(sum(support.values()) - sum(old_support.values())) < 1e-9, (tag, 'support created or destroyed'))
        broad = {k: float(v) for k, _, v in first(snapshot, 'set_popularities')}
        check(sum(broad.values()) == sum(old_broad.values()) == 100, (tag, 'broad outlook totals changed'))
        check(all(broad[k] == old_broad[k] for k in ('communism', 'fascism', 'neutrality')), (tag, 'unrelated outlook changed'))
        check(broad['democratic'] == 61 and broad['nationalist'] == 11, (tag, 'broad shift differs from subtype shift'))
        leader = first(snapshot, 'create_country_leader') or first(snapshot, 'promote_character')
        check(first(leader, 'ideology') == 'Western_Autocracy', (tag, 'inactive dynastic leader type'))
        if tag in {'BHR', 'KUW'}:
            token = first(snapshot, 'recruit_character')
            keys = [k for k, _, _ in snapshot]
            check(keys.index('recruit_character') < keys.index('set_politics') < keys.index('promote_character'),
                  (tag, 'character attachment occurs too late'))
            characters = first(parse((ROOT / 'common/characters/mdcw_gulf_1970.txt').read_text(encoding='utf-8-sig')), 'characters')
            role = first(first(characters, token), 'country_leader')
            check(first(role, 'ideology') == 'Western_Autocracy', (tag, 'defined character role mismatched'))
            check({v for _, _, v in first(role, 'traits')} == {'king', 'western_Western_Autocracy'}, (tag, 'native royal traits absent'))
        else:
            check({v for _, _, v in first(leader, 'traits')} == {'king', 'western_Western_Autocracy'}, (tag, 'native royal traits absent'))
        if tag == 'PER':
            check(first(leader, 'expire') == '"1979.2.11"', 'Shah history expiry altered')
            check(patch['evidence_kind'] == 'historical_1970_adaptation_to_native_MD_family' and
                  'https://history.state.gov/historicaldocuments/frus1969-76ve04/d2' in patch['historical_sources'],
                  'Shah adaptation confused with native2000 template')
            check(next(p for p in countries[tag]['leaders'] if p['id'] == 'ruhollah_khomeini')['party_index'] == 9,
                  'Iranian revolutionary alternative altered')
        for name in patch['parties']:
            row = next(p for p in countries[tag]['parties'] if p['name'] == name)
            check(row['index'] == 0, (tag, name, 'catalogue party still23'))
        for ident in patch['leaders']:
            row = next(p for p in countries[tag]['leaders'] if p['id'] == ident)
            check(row['party_index'] == 0, (tag, ident, 'catalogue leader still23'))
            if ident in patch['sovereigns']:
                check('king' in row['traits'], (tag, ident, 'catalogue king trait missing'))
        branch = next(v for k, _, v in world_effect if k in {'if', 'else_if'} and first(first(v, 'limit', []), 'original_tag') == tag)
        check(first(branch, 'COLDWAR_1970_profile_western_dynasty') == 'yes', (tag, 'world provider not aligned'))
        check(first(first(branch, 'create_country_leader'), 'ideology') == 'Western_Autocracy', (tag, 'world leader not aligned'))
        # Evaluate the selected country's current registry branches, preserving
        # date-gated party names and using its native Western family icon.
        for year in (1970, 1990, 1999):
            for family, index in [('Western_Autocracy', 0), ('Monarchist', 23)]:
                definition = next(v for k, _, v in registry if k == 'defined_text' and first(v, 'name') == 'MDCW_HP_' + family)
                chosen = None
                for text in values(definition, 'text'):
                    condition = first(text, 'trigger', [])
                    if first(condition, 'original_tag') != tag:
                        continue
                    allowed = True
                    for key, op, value in condition:
                        if key == 'date':
                            boundary = tuple(map(int, value.split('.')))
                            allowed &= (year, 1, 1) > boundary if op == '>' else (year, 1, 1) < boundary
                    if allowed:
                        chosen = first(text, 'localization_key'); break
                check(chosen in loc, (tag, year, family, 'missing current party display'))
                check('$MDCW_HP_family_' + str(index) + '_desc$' in loc[chosen + '_desc'],
                      (tag, family, 'party description has wrong native outlook'))
                if index == 0:
                    check('generic_Monarchist' not in loc[chosen], (tag, 'Western ruling party still uses Nationalist star'))
    # Native differing monarchies retain their existing assignments.
    for tag, index in [('SAU', 10), ('QAT', 0), ('OMA', 23), ('BRU', 23), ('MOR', 23)]:
        path = next((ROOT / 'history/countries').glob(tag + ' - *.txt'))
        seed = first(parse(path.read_text(encoding='utf-8-sig')), '1970.1.1')
        ruling = next(first(v, 'ruling_party') for v in values(seed, 'set_variable') if first(v, 'ruling_party') is not None)
        check(int(ruling) == index, (tag, 'unapproved monarchy remap'))
    # All planned outputs exactly reproduce installed artifacts.
    for name, value in build().items():
        path = ROOT / name
        expected = output_bytes(path, value)
        check(path.read_bytes() == expected, (name, 'bounded generation not idempotent'))
    check(not any(k in {'on_startup', 'on_daily', 'on_government_change'} for k, _, _ in parse(
          (ROOT / 'common/scripted_effects/COLDWAR_1970_western_dynasties.txt').read_text(encoding='utf-8-sig'))),
          'Added runtime government restoration')
    print(json.dumps({'ok': True, 'checks': checks, 'aligned_tags': sorted(patches),
                      'engine_tested': False, 'shah_evidence': patches['PER']['historical_sources']}))


if __name__ == '__main__':
    main()
