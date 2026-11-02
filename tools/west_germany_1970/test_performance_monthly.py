# IMPERIA CW — Cold War: Differential checks for monthly performance changes.
"""Compare emitted effects with a supplied, pre-change effects snapshot.

    python tools/west_germany_1970/test_performance_monthly.py <baseline-effects-file>

Runs the actual old/new script AST through the established native-script harness.
These checks establish script equivalence for the exercised states, not HOI4 FPS.
"""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

import systems

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "cwger_monthly_native_harness", ROOT / "tools/guest_workers/validate.py")
V = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)


class MonthlyMachine(V.ScriptMachine):
    """Add native date comparisons and array sizing used by these effects."""

    def __init__(self):
        super().__init__({}, {})
        self.countries = {"GER": V.Country("GER")}
        self.current = self.root = self.previous = self.countries["GER"]
        self.current_date = (1970, 1, 1)
        self.array_resizes = 0

    def test(self, body):
        results = []
        for key, op, value in body:
            if key == "date":
                results.append(self.compare(
                    self.current_date, op, tuple(map(int, value.split(".")))))
            else:
                results.append(super().test([(key, op, value)]))
        return all(results)

    def execute(self, body):
        # Process ordinary runs together: splitting if/else chains would change
        # their semantics in the existing harness.
        ordinary = []
        for node in body:
            key, _, value = node
            if key != "resize_array":
                ordinary.append(node)
                continue
            if ordinary:
                super().execute(ordinary)
                ordinary = []
            self.array_resizes += 1
            name = V.first(value, "array")
            scope, name = self.resolve_variable(name)
            size = int(self.expression(V.first(value, "size")))
            before = int(scope.variables.get(name + "^num", V.D(0)))
            for index in range(size, before):
                scope.variables.pop(f"{name}^{index}", None)
            for index in range(size):
                scope.variables.setdefault(f"{name}^{index}", V.D(0))
            scope.variables[name + "^num"] = V.D(size)
        if ordinary:
            super().execute(ordinary)


def outcome(machine):
    return deepcopy((
        machine.root.variables,
        machine.root.flags,
        [(item[0], item[1], item[2].tag) for item in machine.queue],
    ))


def run_checks(baseline):
    before = {key: value for key, _, value in V.parse(
        baseline.read_text(encoding="utf-8-sig"))}
    after = {key: value for key, _, value in V.parse(
        systems.monthly_effects() + systems.election_cache_effect())}
    checks = 0
    # Include both sides of succession dates, the restricted Engholm interval,
    # and late saves where several ordered transitions occur in one tick.
    dates = [
        (1970, 1, 1), (1973, 6, 12), (1973, 6, 13),
        (1982, 12, 1), (1982, 12, 2), (1986, 8, 25), (1986, 8, 26),
        (1990, 3, 19), (1990, 3, 20), (1991, 5, 29), (1991, 5, 30),
        (1992, 5, 18), (1992, 5, 19), (1993, 6, 25), (1993, 6, 26),
        (1995, 11, 1), (1995, 11, 16), (1995, 11, 17),
        (1998, 3, 2), (1998, 3, 3), (2000, 1, 1),
    ]
    key = systems.P + "_leadership_tick"
    for party in range(24):
        for chair in range(1, 9):
            for mannheim in (False, True):
                for date in dates:
                    outcomes = []
                    for body in (before[key], after[key]):
                        machine = MonthlyMachine()
                        machine.current_date = date
                        machine.root.variables.update(
                            ruling_party=V.D(party), cwger_spd_leader=V.D(chair),
                            cwger_cdu_leader=V.D(1), cwger_fdp_leader=V.D(1))
                        if mannheim:
                            machine.root.flags[systems.P + "_lafontaine_mannheim"] = V.D(0)
                        machine.execute(body)
                        outcomes.append(outcome(machine))
                    assert outcomes[0] == outcomes[1], (party, chair, mannheim, date)
                    checks += 1
    leadership_checks = checks

    key = systems.P + "_cache_election_shares"
    for party in range(24):
        for initial_size in (None, 0, 12, 24, 30):
            for fallback in (False, True):
                machines = [MonthlyMachine(), MonthlyMachine()]
                for machine in machines:
                    machine.root.variables["ruling_party"] = V.D(party)
                    if initial_size is not None:
                        machine.root.variables["cwger_parliament_shares^num"] = V.D(initial_size)
                        for index in range(initial_size):
                            machine.root.variables[f"cwger_parliament_shares^{index}"] = V.D(".99")
                for refresh in range(2):
                    # Change both possible sources between calls so caching
                    # cannot accidentally freeze an election result or polls.
                    for machine, body in zip(machines, (before[key], after[key])):
                        for index in range(24):
                            machine.root.variables[f"party_pop_elect_array^{index}"] = V.D(index + refresh + 1) / 1000
                            machine.root.variables[f"party_pop_array^{index}"] = V.D(24 - index + refresh) / 1000
                        if fallback:
                            machine.root.variables[f"party_pop_elect_array^{party}"] = V.D(-1)
                        machine.execute(body)
                    assert outcome(machines[0]) == outcome(machines[1]), (party, initial_size, fallback, refresh)
                    checks += 1
                assert machines[0].array_resizes == 2
                assert machines[1].array_resizes == (0 if initial_size == 24 else 1)
                checks += 1
    return {
        "checks": checks,
        "leadership_differential_cases": leadership_checks,
        "cache_checks": checks - leadership_checks,
        "errors": [],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path, help="Pre-change scripted effects snapshot")
    args = parser.parse_args()
    print(json.dumps(run_checks(args.baseline), indent=2))
