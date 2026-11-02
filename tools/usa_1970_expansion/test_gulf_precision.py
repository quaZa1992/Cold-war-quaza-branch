# IMPERIA COLD WAR — Gulf native-proration and preservation checks.
"""Exercise generated Gulf AST without rewriting old reports or game outputs.

Both preserved suites now assert five-place values from the archived native
probe. Use that same model for their reruns; this is not a new HOI4 launch.
"""
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_DOWN
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/iraq_1970'))
from usa_module import generate, P, daily_cost, relief_start_cost, WEEKLY_RATES
import test_usa_module as original_suite
import test_usa_review_regressions as review_suite
from test_audit_usa import PolicyWorld, local
from script_ast import parse, first, values


class ProratedWorld(PolicyWorld):
    fixed = False

    def __init__(self, outputs):
        super().__init__(outputs)
        # Model the new parent's USA initialisation hook before opening controls.
        self.call(P + 'recalculate_prorated_costs')

    def run(self, rows, c, root=None, prev=None, source=None):
        buffered = []
        for k, op, v in rows:
            if k in ('divide_variable', 'divide_temp_variable'):
                if buffered:
                    super().run(buffered, c, root, prev, source)
                    buffered = []
                name, _, value = v[0]
                dividend = Decimal(str(c.var.get(name, 0)))
                divisor = Decimal(str(self.num(value, c)))
                amount = dividend / divisor
                if self.fixed:
                    amount = amount.quantize(Decimal('0.00001'), rounding=ROUND_DOWN)
                c.var[name] = float(amount)
            else:
                buffered.append((k, op, v))
        if buffered:
            return super().run(buffered, c, root, prev, source)


class FiveDecimalWorld(ProratedWorld):
    fixed = True


def run_old_suite(module, model_name, model=FiveDecimalWorld):
    captured = {}
    def capture(path, text, *args, **kwargs):
        captured[str(path)] = text
        return len(text)
    stream = io.StringIO()
    with patch.object(module, model_name, model), patch.object(Path, 'write_text', capture), redirect_stdout(stream):
        module.main()
    assert len(captured) == 1, captured
    report = json.loads(next(iter(captured.values())))
    return report


def main():
    before = hashlib.sha256((ROOT / 'common/national_focus/USA_1970.txt').read_bytes()).hexdigest()
    outputs = generate(ROOT)
    assert outputs == generate(ROOT)
    for path, source in outputs.items():
        if path.endswith('.txt'):
            parse(source)
        assert not re.search(r'(?<![A-Za-z0-9_])[-+]?\d*\.\d{6,}', source), path

    # Existing suites contain useful transaction, consent and timer tests. Their
    # output writes are captured in memory; their obsolete whole-tree fixture is
    # never used. Only documented native divide operations are added to the model.
    old = run_old_suite(original_suite, 'World', FiveDecimalWorld)
    revised = run_old_suite(review_suite, 'PolicyWorld')
    checks = ['Original Gulf transaction suite: ' + str(old['passed']) + ' checks',
              'Existing native-treasury review suite: ' + str(revised['passed']) + ' checks',
              'All generated scripts parse; no numeric literal exceeds five fractional digits']

    quantised = {}
    for rate in WEEKLY_RATES:
        w = FiveDecimalWorld(outputs)
        cost = w.c['USA'].var[daily_cost(str(rate))]
        assert cost > 0
        assert math.isclose(w.c['USA'].var[relief_start_cost(str(rate))], .5 + cost, abs_tol=1e-12)
        quantised[str(rate)] = {'model_daily_cost': cost, 'model_seven_day_sum': float(Decimal(str(cost))*7),
                              'model_weekly_difference': str(Decimal(str(cost))*7-rate)}
    checks.append('All three computed prices and initial-relief floors remain positive and internally consistent')

    w = FiveDecimalWorld(outputs)
    local(w)
    w.c['KUR'].flags[P + 'support_offer'] = None
    daily = w.c['USA'].var[daily_cost('0.05')]
    w.c['USA'].var['treasury'] = daily - .00001
    w.accept(22)
    assert not w.flag(w.c['USA'], P + 'support_kur') and w.c['USA'].var.get(P+'support_days',0) == 0
    w.c['USA'].var['treasury'] = daily
    w.accept(22)
    assert w.flag(w.c['USA'], P + 'support_kur')
    donor, recipient = w.c['USA'].var['treasury'], w.c['KUR'].var['treasury']
    w.tick()
    assert math.isclose(donor-w.c['USA'].var['treasury'], daily, abs_tol=1e-12)
    assert math.isclose(w.c['KUR'].var['treasury']-recipient, daily, abs_tol=1e-12)
    assert w.c['USA'].var['treasury'] >= -1e-12
    checks.append('Five-decimal model: below-boundary rejection, exact affordability and matched donor/recipient daily transfer')

    w = FiveDecimalWorld(outputs)
    for rate in WEEKLY_RATES:
        w.c['USA'].var.pop(daily_cost(str(rate)), None)
    w.c['KUR'].flags[P+'support_offer'] = None
    local(w)
    w.accept(22)
    assert w.c['USA'].var.get(P+'support_days',0) == 0
    checks.append('Uninitialised daily-price controls fail closed instead of accepting a zero-cost contract')

    w = FiveDecimalWorld(outputs)
    w.call(P+'initial_underground')
    initial = w.c['USA'].var['treasury']
    for _ in range(90):
        w.tick()
    expected = 90*w.c['USA'].var[daily_cost('0.05')]
    assert math.isclose(initial-w.c['USA'].var['treasury'], expected, abs_tol=1e-10)
    assert w.c['USA'].var[P+'support_days'] == 0
    expired = w.c['USA'].var['treasury']
    w.tick()
    assert w.c['USA'].var['treasury'] == expired
    checks.append('Five-decimal model: ninety charged days, unchanged timer cadence and no payment after expiry')

    assert before == hashlib.sha256((ROOT/'common/national_focus/USA_1970.txt').read_bytes()).hexdigest()
    checks.append('Loaded 301-focus USA tree remains byte-identical throughout all checks')
    report = {'project':'IMPERIA COLD WAR', 'status':'Source and bounded-AST checks passed; five-place values calibrated to archived native probe; no new engine run',
              'checks':checks, 'original_preservation_checks':old['passed'], 'review_preservation_checks':revised['passed'],
              'five_decimal_truncation_model':quantised, 'native_engine_tested':False,
              'loaded_usa_sha256':before,
              'catalogue_sha256':hashlib.sha256((ROOT/'docs/design/iraq_1970/usa_gulf/COLDWAR_USA_GULF_CONCEPT.json').read_bytes()).hexdigest()}
    destination=ROOT/'docs/design/usa_1970_expansion_20261024/implementation_support_gulf_precision.json'
    destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
