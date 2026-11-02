# IMPERIA CW — Cold War: Differential execution of optimized border division counting.
"""Compare emitted border arithmetic against an earlier windows-effects snapshot.

    python tools/west_germany_1970/test_performance_border.py <old_windows_effects.txt>

Executes both actual Clausewitz ASTs in the established strict harness. The
native divisions_in_state trigger is supplied with fixture division counts;
this measures query counts, not HOI4 execution time or rendering performance.
"""
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import random
import sys

import rivalry

ROOT = Path(__file__).resolve().parents[2]
spec = spec_from_file_location('cwger_border_harness', ROOT / 'tools/guest_workers/validate.py')
V = module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)


class BorderMachine(V.ScriptMachine):
    def __init__(self, effects, divisions, ddr_exists=True):
        super().__init__(effects, {})
        self.countries = {tag: V.Country(tag) for tag in ('GER', 'DDR')}
        self.countries['DDR'].exists = ddr_exists
        self.current = self.root = self.countries['GER']
        self.previous = self.current
        self.origin = self.countries['DDR']
        self.divisions = divisions
        self.queries = 0

    def test(self, body):
        results = []
        for key, op, value in body:
            if key == 'country_exists':
                results.append(self.countries[value].exists)
            elif key == 'divisions_in_state':
                self.queries += 1
                state = int(V.first(value, 'state'))
                _key, comparison, threshold = next(node for node in value if node[0] == 'size')
                results.append(self.compare(self.divisions.get((self.current.tag, state), 0),
                                            comparison, int(threshold)))
            else:
                results.append(super().test([(key, op, value)]))
        return all(results)


def main():
    baseline = Path(sys.argv[1])
    old = dict((key, body) for key, _op, body in V.parse(baseline.read_text(encoding='utf-8-sig')))
    new = dict((key, body) for key, _op, body in V.parse(rivalry.border_watch()))
    name = rivalry.R + '_border_count'
    states = [('GER', state) for state in rivalry.BORDER_BRD] + [('DDR', state) for state in rivalry.BORDER_DDR]
    cases = [{}]
    cases.extend({state: count} for state in states for count in range(65))
    cases.extend(dict.fromkeys(states, count) for count in range(65))
    rng = random.Random(1970)
    cases.extend({state: rng.randrange(65) for state in states} for _ in range(500))
    maximum = 0
    for divisions in cases:
        before, after = BorderMachine(old, divisions), BorderMachine(new, divisions)
        before.call(name)
        after.call(name)
        assert before.root.variables == after.root.variables, ('Border arithmetic changed', divisions)
        assert before.queries == len(states) * len(rivalry.BORDER_STEPS)
        assert after.queries <= len(states) * 5, ('Unbounded division queries', divisions)
        assert after.countries['DDR'].variables == before.countries['DDR'].variables
        maximum = max(maximum, after.queries)
    empty = BorderMachine(new, {})
    empty.call(name)
    assert empty.queries == len(states)
    for divisions in ({}, dict.fromkeys(states, 30)):
        before, after = BorderMachine(old, divisions, False), BorderMachine(new, divisions, False)
        for machine in (before, after):
            machine.root.variables.update(cwgg_aufm_brd=3, cwgg_aufm_ddr=3,
                                          cwgg_aufm_brd_div=180, cwgg_aufm_ddr_div=180)
            machine.call(name)
            assert machine.queries == 0
        assert before.root.variables == after.root.variables
    print(json.dumps({'differential_cases': len(cases) + 2,
                      'old_queries_per_count': len(states) * len(rivalry.BORDER_STEPS),
                      'new_maximum_queries': maximum, 'new_empty_queries': empty.queries,
                      'errors': []}, indent=2))


if __name__ == '__main__':
    main()
