# IMPERIA CW — Cold War: build surveyed uranium districts from the dated source register.
"""Rebuild only the January 1970 deposit profile, never state resources or mines."""
import json, re
from port import ROOT, AUDIT, read, write
from adapt import block


def main():
    register = json.loads(read(AUDIT / 'uranium_1970_research.json'))
    entries = register['deposits']
    state_files = {int(re.match(r'\d+', p.name)[0]): p
                   for p in (ROOT / 'history/states').glob('*.txt')}
    seen = set()
    lines = ['COLDWAR_uranium_setup_1970_deposits = {']
    capacities = {}
    for entry in sorted(entries, key=lambda item: item['state_id']):
        state = entry['state_id']
        assert state in state_files and state not in seen, state
        seen.add(state)
        assert 0 < entry['known_by_year'] <= 1969, entry
        assert entry['sources'] and all(url.startswith('https://') for url in entry['sources']), entry
        slots, output = entry['slots'], entry['output_per_level']
        assert slots in [1, 2, 3] and output in [3, 4, 6, 9, 12], entry
        districts = entry['districts']
        if isinstance(districts, list): districts = '; '.join(districts)
        assert '\n' not in districts, entry
        lines.extend([
            f'\t# {state_files[state].stem}: {districts}; known by {entry["known_by_year"]}.',
            f'\t{state} = {{ imp_uranium_add_deposit = yes '
            f'set_variable = {{ imp_uranium_mine_slots = {slots} }} '
            f'set_variable = {{ imp_uranium_per_level = {output} }} }}',
        ])
        capacities[str(state)] = {'mine_slots': slots, 'output_per_level': output}
    lines.append('}')
    rel = 'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt'
    original = read(ROOT / rel)
    node = block(original, 'COLDWAR_uranium_setup_1970_deposits')
    updated = original[:node['start']] + '\n'.join(lines) + original[node['end']:]
    if updated != original:
        before = AUDIT / 'geology_before' / rel
        if not before.exists(): write(before, original)
        write(ROOT / rel, updated)
    balance = json.loads(read(AUDIT / 'coldwar_balance.json'))
    balance.update(starting_resources={}, deposits=capacities,
                   knowledge_cutoff='1970-01-01', source_register='uranium_1970_research.json',
                   method=f'Zero initial raw uranium and no built mines. {len(entries)} districts known before 1970 permit paid development. Mine slots and output are gameplay capacity, not historical reserve tonnages.')
    write(AUDIT / 'coldwar_balance.json', json.dumps(balance, indent=2, ensure_ascii=False) + '\n')
    print(f'Built {len(entries)} sourced January 1970 districts; no resources or buildings granted.')


if __name__ == '__main__': main()
