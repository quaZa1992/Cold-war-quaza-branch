# IMPERIA COLD WAR — Sourced uranium districts and requested Karelia/Mali mining capacity.
"""Rebuild deposit access from the source register, never resources or mines."""
import json, re
from port import ROOT, AUDIT, read, write
from adapt import block


def render_deposits(entries, effect, capacities, seen, *, geographic_exception=False):
    state_files = {int(re.match(r'\d+', p.name)[0]): p
                   for p in (ROOT / 'history/states').glob('*.txt')}
    lines = [effect + ' = {']
    for entry in sorted(entries, key=lambda item: item['state_id']):
        state = entry['state_id']
        assert state in state_files and state not in seen, state
        seen.add(state)
        if geographic_exception:
            assert entry['scenario_access'] == 'user_requested_geographic_exception', entry
            assert entry['note'] and entry['discovery_history'], entry
            assert (entry['slots'], entry['output_per_level']) == {
                'LOW': (1, 3), 'HIGH': (3, 9)
            }[entry['requested_tier']], entry
            chronology = 'requested ' + entry['requested_tier'] + ' capacity; historical dates in source register'
        else:
            assert 0 < entry['known_by_year'] <= 1969, entry
            chronology = f'known by {entry["known_by_year"]}'
        assert entry['sources'] and all(url.startswith('https://') for url in entry['sources']), entry
        slots, output = entry['slots'], entry['output_per_level']
        assert slots in [1, 2, 3] and output in [3, 4, 6, 9, 12], entry
        districts = entry['districts']
        if isinstance(districts, list): districts = '; '.join(districts)
        assert '\n' not in districts, entry
        lines.extend([
            f'\t# {state_files[state].stem}: {districts}; {chronology}.',
            f'\t{state} = {{ imp_uranium_add_deposit = yes '
            f'set_variable = {{ imp_uranium_mine_slots = {slots} }} '
            f'set_variable = {{ imp_uranium_per_level = {output} }} }}',
        ])
        capacities[str(state)] = {'mine_slots': slots, 'output_per_level': output}
    lines.append('}')
    return '\n'.join(lines)


def main():
    register = json.loads(read(AUDIT / 'uranium_1970_research.json'))
    entries = register['deposits']
    additions = register.get('rp_geographic_additions', [])
    capacities, seen = {}, set()
    dated_effect = 'COLDWAR_uranium_setup_1970_deposits'
    additional_effect = 'COLDWAR_uranium_setup_karelia_mali_deposits'
    dated = render_deposits(entries, dated_effect, capacities, seen)
    additional = render_deposits(additions, additional_effect, capacities, seen,
                                 geographic_exception=True)
    rel = 'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt'
    original = read(ROOT / rel)
    node = block(original, dated_effect)
    updated = original[:node['start']] + dated + original[node['end']:]
    if re.search(r'\b' + additional_effect + r'\s*=', updated):
        node = block(updated, additional_effect)
        updated = updated[:node['start']] + additional + updated[node['end']:]
    else:
        node = block(updated, dated_effect)
        marker = '# IMPERIA COLD WAR — Requested Karelia LOW and Mali HIGH deposit access; paid development only.'
        updated = updated[:node['end']] + '\n\n' + marker + '\n' + additional + updated[node['end']:]
    updated = '# IMPERIA COLD WAR — Uranium supply chain and sourced Karelia/Mali deposit access.\n' + updated.split('\n', 1)[1]
    if updated != original:
        before = AUDIT / 'geology_before' / rel
        if not before.exists(): write(before, original)
        write(ROOT / rel, updated)
    balance = json.loads(read(AUDIT / 'coldwar_balance.json'))
    balance = {'project': 'IMPERIA COLD WAR', **balance}
    balance.update(starting_resources={}, deposits=capacities,
                   knowledge_cutoff='1970-01-01', source_register='uranium_1970_research.json',
                   rp_geographic_additions=[entry['state_id'] for entry in additions],
                   method=f'Zero initial raw uranium and no built mines. {len(entries)} districts known before 1970 plus {len(additions)} explicitly requested geographic additions permit paid development. The latter do not claim pre-1970 discovery. Mine slots and output are gameplay capacity, not historical reserve tonnages.')
    write(AUDIT / 'coldwar_balance.json', json.dumps(balance, indent=2, ensure_ascii=False) + '\n')
    print(f'Built {len(entries)} dated districts and {len(additions)} requested geographic additions; no resources or buildings granted.')


if __name__ == '__main__': main()
