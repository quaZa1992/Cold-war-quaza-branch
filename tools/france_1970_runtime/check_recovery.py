# IMPERIA COLD WAR — Emitted recovery migration state checks.
"""Execute the authored migration's restricted AST; this is not an engine test."""
from pathlib import Path
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field

SCRIPT = ROOT / 'common/scripted_effects/COLDWAR_FRA2_1970_effects.txt'
P = 'COLDWAR_FRA2_'


class State:
    def __init__(self, ideas, flags, scenario=True):
        self.ideas, self.flags, self.scenario = set(ideas), set(flags), scenario

    def condition(self, row):
        key, value = row.key, row.value
        if key in ('limit', 'AND'):
            return all(self.condition(c) for c in row.children())
        if key == 'OR':
            return any(self.condition(c) for c in row.children())
        if key == 'NOT':
            return not all(self.condition(c) for c in row.children())
        if key == 'has_idea':
            return value in self.ideas
        if key == 'has_country_flag':
            return value in self.flags
        if key == P + 'is_1970':
            return self.scenario
        raise AssertionError('Unsupported trigger: ' + key)

    def execute(self, rows):
        last_if = None
        for row in rows:
            key = row.key
            if key == 'if':
                limit = next(c for c in row.children() if c.key == 'limit')
                last_if = self.condition(limit)
                if last_if:
                    self.execute([c for c in row.children() if c.key != 'limit'])
            elif key == 'else':
                assert last_if is not None
                if not last_if:
                    self.execute(row.children())
                last_if = None
            elif key == 'swap_ideas':
                self.ideas.discard(field(row.children(), 'remove_idea'))
                self.ideas.add(field(row.children(), 'add_idea'))
            elif key == 'add_ideas':
                assert isinstance(row.value, str)
                self.ideas.add(row.value)
            elif key == 'remove_ideas':
                self.ideas.discard(row.value)
            elif key == 'set_country_flag':
                assert isinstance(row.value, str)
                self.flags.add(row.value)
            else:
                # Fees, variables, construction and research are forbidden in
                # this migration. Do not silently stub an unexpected statement.
                raise AssertionError('Unsupported or finite effect: ' + key)


def main():
    raw = SCRIPT.read_bytes()
    provider = next(n for n in nodes(raw.decode('utf-8')) if n.key == P + 'migrate_starting_spirit_revision')
    cases = []
    for political, education, oil, mode in itertools.product(
            ('none', 'executive', 'parliament', 'civic'),
            ('none', 'technical_colleges', 'mass_universities'),
            ('none', 'nuclear_scale', 'diverse_energy', 'oil_resilience'),
            ('legacy', 'current')):
        flags, initial, expected = set(), set(), set()
        if political == 'none':
            initial.add(P + 'presidency'); expected.add(P + 'presidency')
        elif political == 'civic':
            flags.update({P + 'earned_parliament', P + 'earned_civic_settlement'})
        else:
            flags.add(P + 'earned_' + political)
            expected.add(P + 'institutional_balance_residual')
            if mode == 'current': initial.add(P + 'institutional_balance_residual')
        if education == 'none':
            initial.add(P + 'education'); expected.add(P + 'education')
        else:
            flags.add(P + 'earned_' + education)
            expected.add(P + 'higher_education_pressures')
            if mode == 'current': initial.add(P + 'higher_education_pressures')
        if oil == 'none':
            initial.add(P + 'oil'); expected.add(P + 'oil')
        elif oil == 'oil_resilience':
            flags.update({P + 'earned_diverse_energy', P + 'earned_oil_resilience'})
            expected.add(P + 'oil_dependence_residual')
            if mode == 'current': initial.add(P + 'oil_dependence_residual')
        else:
            flags.add(P + 'earned_' + oil)
            expected.add(P + 'oil_dependence_intermediate')
            initial.add(P + ('oil' if mode == 'legacy' else 'oil_dependence_intermediate'))
        state = State(initial, flags)
        state.execute(provider.children())
        assert state.ideas == expected, (political, education, oil, mode, state.ideas, expected)
        first = (state.ideas.copy(), state.flags.copy())
        state.execute(provider.children())
        assert (state.ideas, state.flags) == first, 'Replay changed migration state'
        cases.append({'political':political,'education':education,'oil':oil,'mode':mode,'passed':True})
    blocked = State({P + 'presidency'}, {P + 'earned_executive'}, scenario=False)
    blocked.execute(provider.children())
    assert blocked.ideas == {P + 'presidency'} and blocked.flags == {P + 'earned_executive'}
    report = {'project':'IMPERIA COLD WAR','scope':'Restricted AST execution of emitted migration; not native UI/engine/save loading',
              'script_sha256':hashlib.sha256(raw).hexdigest(),'state_cases':len(cases),'replay_checks':len(cases),
              'scenario_guard_passed':True,'finite_effects_permitted':False,'cases':cases,'passed':True}
    (HERE / 'RECOVERY_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))


if __name__ == '__main__':
    main()
