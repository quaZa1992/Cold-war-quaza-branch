# IMPERIA CW — Cold War: Historical parties, leaders and national identities.
"""Focused loaded-history, native-provider and bounded regeneration checks."""
import hashlib
import json
import re
import sys
from pathlib import Path

import qatar_identity as q
from starting_identity import parse, first, values, nodes, SNAPSHOT_BEGIN, SNAPSHOT_END
sys.path.insert(0, str(q.HERE))
from dispatch import _restore_setter
from apply_monarchy_alignment import output_bytes
from monarchy_alignment import apply_country

checks = 0


def check(value, message):
    global checks
    checks += 1
    assert value, message


def main():
    planned = q.build()
    for name, value in planned.items():
        check((q.ROOT / name).read_bytes() == output_bytes(q.ROOT / name, value), name + ' is not reproducible')
    history = (q.ROOT / 'history/countries/QAT - Qatar.txt').read_text(encoding='utf-8-sig')
    seed = parse(history.split(SNAPSHOT_BEGIN)[1].split(SNAPSHOT_END)[0])
    check(first(first(seed, 'set_politics'), 'ruling_party') == 'democratic', 'Menu outlook differs from Western government')
    check(first(seed, 'recruit_character') == 'QAT_MDCW_1970_incumbent', 'No actual dated character recruitment')
    check(first(first(seed, 'promote_character'), 'ideology') == 'Western_Autocracy', 'Promotion targets wrong outlook')
    check(any(first(v, 'ruling_party') == '0' for v in values(seed, 'set_variable')), 'Wrong native party index')
    check(any(first(v, 'party_pop_array^0') == '0.74' for v in values(seed, 'set_variable')), 'Dynastic support was lost')
    check('startup_politics' not in history.split('2000.1.1')[0], 'Identity deferred to startup')
    check(sum(float(v) for _, _, v in first(seed, 'set_popularities')) == 100, 'Invalid broad popularity sum')
    character = first(first(parse((q.ROOT / 'common/characters/mdcw_gulf_1970.txt').read_text(encoding='utf-8-sig')), 'characters'), 'QAT_MDCW_1970_incumbent')
    role = first(character, 'country_leader')
    check(first(character, 'name') == '"Ahmad bin Ali Al Thani"', 'Wrong historical ruler/name')
    check(first(role, 'ideology') == 'Western_Autocracy', 'Visible portrait has no active civilian leader role for the government')
    check(first(role, 'expire') == '"1972.2.22"', 'Existing1972 boundary was changed')
    sprite = first(first(first(character, 'portraits'), 'civilian'), 'large')
    check(sprite == 'GFX_MDCW_GULF_1970_QAT', 'Approved portrait binding lost')
    setter = (q.ROOT / 'common/scripted_effects/QAT_political_leaders.txt').read_text(encoding='utf-8-sig')
    historical = first(first(parse(setter), 'set_leader_QAT'), 'if')
    check(first(first(historical, 'limit'), 'IMP_is_1970_scenario') == 'yes', 'Historical setter affects modern bookmarks')
    check(first(first(first(historical, 'limit'), 'check_variable'), 'ruling_party') == '0', 'Historical setter missing Western0 provider')
    check(first(historical, 'MDCW_HP_native_pool_QAT_0') == 'yes', 'Missing actual native provider call')
    poolpath = q.ROOT / 'common/scripted_effects/mdcw_historical_native_pools.txt'
    pool = first(parse(poolpath.read_text(encoding='utf-8-sig')), 'MDCW_HP_native_pool_QAT_0')
    check(pool is not None, 'Referenced native provider undefined')
    for branch in values(pool, 'if') + values(pool, 'else_if') + values(pool, 'else'):
        leader = first(branch, 'create_country_leader')
        check(bool(first(leader, 'name')), 'Native set_leader would kill current ruler without a named replacement')
        check(first(leader, 'ideology') == 'Western_Autocracy', 'Native set_leader replacement is inactive for Western government')
        picture = first(leader, 'picture').strip('"')
        check((q.ROOT / picture).is_file(), 'Native replacement portrait missing')
    # The native modern fallback is unchanged, including its10/13 handling.
    md = Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
    original = (md / 'common/scripted_effects/QAT_political_leaders.txt').read_text(encoding='utf-8-sig')
    check(parse(_restore_setter(setter, 'QAT')) == parse(original), 'Native modern QAT selector changed')
    nativehistory = (md / 'history/countries/QAT - Qatar.txt').read_bytes()
    installed = (q.ROOT / 'history/countries/QAT - Qatar.txt').read_bytes()
    # Earlier accepted mod work may alter modern history; our repair itself
    # never touches the tail, proven by the output build preserving it.
    check(installed.split(b'2000.1.1', 1)[1] == output_bytes(q.ROOT / 'history/countries/QAT - Qatar.txt', planned['history/countries/QAT - Qatar.txt']).split(b'2000.1.1', 1)[1], 'Repair changes modern history tail')
    world = json.loads((q.HERE / 'data/world.json').read_text(encoding='utf-8'))
    qat = next(c for c in world['countries'] if c['tag'] == 'QAT')
    check(apply_country(qat) == qat, 'Canonical catalogue mapping is not stable')
    check(next(p for p in qat['parties'] if p['name'] == 'House of Al Thani')['index'] == 0, 'Canonical party mismatches native role')
    for country in world['countries']:
        if country['tag'] != 'QAT':
            check(q.align_country(country) == country, 'Qatar adapter changes another catalogue country')
    report = {'status': 'pass', 'checks': checks, 'native_engine_tested': False,
              'identity': {'name': 'Ahmad bin Ali Al Thani', 'outlook': 'democratic',
                           'party': 0, 'ideology': 'Western_Autocracy', 'existing_expiry': '1972.2.22'},
              'sources': q.SOURCES, 'files': {name: hashlib.sha256((q.ROOT / name).read_bytes()).hexdigest() for name in planned}}
    (q.HERE / 'QATAR_IDENTITY_VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, indent=2))


if __name__ == '__main__':
    main()

