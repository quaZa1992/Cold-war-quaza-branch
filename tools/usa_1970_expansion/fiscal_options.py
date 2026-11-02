# IMPERIA COLD WAR — USA 1970 bounded fiscal-policy comparison.
"""Produce a conditional, source-based comparison, never install gameplay.

The retained engine budget is before final sanctions calculation. The explicit
post-blowback case assumes the known native USA corporate-income baseline +2%.
No live save or complete engine economy is simulated by this small model.
"""
from __future__ import annotations
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from economy import consumer_goods
from focus_prerequisite_ui import nodes

BASE = dict(gdp=D('3941.76292'), population_m=D('208.19219'), gdpc=D('18.93328'),
            income=D('69.25320'), corporate=D('49.76320'), household=D('14.13042'),
            expense=D('54.85895'), defence=D('9.52178'), bureaucracy=D('5.46262'),
            education=D('4.70827'), health=D('7.46301'), welfare=D('12.79760'))
OPTIONS = [
    dict(id='investment_and_retrenchment', corporate=D(20), household=D(31), defence=3,
         bureaucracy=2, health=2, welfare=2, healthcare='fully_privatized_healthcare'),
    dict(id='funded_strategic_commitment', corporate=D(23), household=D(31), defence=4,
         bureaucracy=2, health=2, welfare=2, healthcare='fully_privatized_healthcare'),
]


def ideas():
    result = {}
    wanted = {'bureau_02', 'bureau_03', 'health_02', 'health_03', 'social_02', 'social_03',
              'defence_03', 'defence_04', 'defence_05', 'fully_privatized_healthcare'}
    def visit(rows):
        for n in rows:
            if n.key in wanted:
                mod = next((x for x in n.children() if x.key == 'modifier'), None)
                result[n.key] = {x.key: D(x.value) for x in mod.children()} if mod else {}
            visit(n.children())
    for name in ('AA_law_budget.txt', 'AA_law_military_ideas.txt', 'AA_law_expanded_economics.txt'):
        visit(nodes((ROOT / 'common/ideas' / name).read_text(encoding='utf-8-sig')))
    return result


def forecast(option, legacy_rate=48, pre_bb_corporate_modifier=D('.02')):
    b = BASE
    rate = option['corporate'] * D(legacy_rate) / 48
    common = 1 + b['gdpc'] * D('.006')
    security = b['population_m'] * 10 * D('.00098') * common * D('1.29') * D('1.6')
    residual = b['expense'] - sum(b[k] for k in ('defence', 'bureaucracy', 'education', 'health', 'welfare')) - security
    # Native daily industry component is multiplied by seven at the weekly reader.
    defence_industry = 80 * D('.03') / (b['gdpc'] * D('-.046') + D('4.286')) * 7
    defence_remainder = b['defence'] - defence_industry
    target = option['defence']
    defence_ladder = {3: D('.015'), 4: D('.023'), 5: D('.03')}
    defence = defence_industry * defence_ladder[target] / D('.03')
    defence += defence_remainder * (D('.25') * target + D('.75')) / 2
    health = b['health'] * D('.83') / D('1.18') * D('.5')
    welfare = b['welfare'] * D('2.5') / 4
    bureaucracy = b['bureaucracy'] * D('1.6') / D('2.2')
    expense = residual + security + b['education'] + bureaucracy + health + welfare + defence
    blowback = D('.355') / D('.6') * D('-.35')
    factor = (1 + pre_bb_corporate_modifier + blowback) / (1 + pre_bb_corporate_modifier)
    corp = b['corporate'] * rate / 48 * factor
    household = b['household'] * option['household'] / 24
    # Deliberately pessimistic health-sector allowance: discard the entire
    # upper-bound $2 pre-BB/week at rate48, not just the actual privatisation/law loss.
    health_income_reserve = 2 * rate / 48 * factor
    other = b['income'] - b['corporate'] - b['household']
    income = other + corp + household - health_income_reserve
    multiplier = D('1.62') / D('.99')  # health02 loses health03's -1% demand factor.
    cg = consumer_goods(rate, multiplier)
    balance = income - expense
    return dict(corporate_rate=rate, household_rate=option['household'],
                weekly_income_lower_estimate=income, weekly_expense_estimate=expense,
                weekly_balance_lower_estimate=balance,
                annual_deficit_gdp_share=max(0, -balance * 52 / b['gdp']),
                consumer_goods=cg, health_tax_uncertainty_reserve=health_income_reserve,
                expense_breakdown=dict(defence=defence, bureaucracy=bureaucracy,
                                       education=b['education'], health=health, welfare=welfare,
                                       security=security, unchanged_residual=residual))


def generate():
    native = ideas()
    results = []
    for option in OPTIONS:
        swaps = [('bureau_03', 'bureau_02'), ('health_03', 'health_02'),
                 ('social_03', 'social_02'), ('defence_05', f'defence_0{option["defence"]}')]
        deltas = {}
        for old, new in swaps:
            keys = native[old].keys() | native[new].keys()
            deltas[old + ' -> ' + new] = {k: native[new].get(k, D(0)) - native[old].get(k, D(0)) for k in sorted(keys)}
        results.append(dict(policy=option, native_law_deltas=deltas,
                            healthcare_class_effects=native['fully_privatized_healthcare'],
                            new_default=forecast(option), observed_42_relative=forecast(option, 42)))
    files = ['common/scripted_effects/00_money_system.txt', 'common/scripted_effects/USA_1970_scripted_effects.txt',
             'common/scripted_effects/mdcw_communist_struggle_startup_effects.txt',
             'common/scripted_effects/imp_sanctions_effects.txt', 'common/ideas/AA_law_budget.txt',
             'common/ideas/AA_law_military_ideas.txt', 'common/ideas/AA_law_expanded_economics.txt']
    report = dict(project='IMPERIA COLD WAR', status='Unselected conditional alternatives. User explicitly chose retaining all existing services and accepting the deficit; no runtime policy package installed.',
                  native_observation='Earlier pre-final-sanctions startup budget, not a post-fix game test.',
                  base=BASE, corporate_blowback_delta=D('.355') / D('.6') * D('-.35'), options=results,
                  assumptions=['Known pre-BB corporate-income modifier +.02. Actual other modifiers must be checked in the live save.',
                               'No full GDP/workforce/future growth/interest recalculation. Military remainder treated as personnel; fixed equipment cost is zero in the intentionally empty OOB start.',
                               'Hospital/workforce and military-productivity changes can alter later GDP and revenue. Entire rate48 health revenue upper bound2/week is discarded as a pessimistic allowance.',
                               'Other sanctions channels, later currency/market changes and actual live-save spending remain outside this conditional forecast.',
                               'Lower clinic and pension laws are political retrenchment choices, not proven historically correct default laws.'],
                  hashes={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files})
    path = ROOT / 'docs/design/usa_1970_expansion_20261024/USA_FISCAL_OPTIONS_20261024.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    report = generate()
    print(json.dumps(dict(project=report['project'], status=report['status'],
                          options=[dict(id=r['policy']['id'], new=r['new_default'],
                                        observed_42_relative=r['observed_42_relative']) for r in report['options']]),
                     indent=2, default=str))
