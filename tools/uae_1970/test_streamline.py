# IMPERIA CW — Cold War: uae 1970 — test streamline.
"""Independent installed-AST checks for direct domestic focus settlements.

Native economy, portraits and office synchronization are explicit boundaries;
authored focus guards, once receipts, modifier arithmetic and political receipt
guards are executed from installed files. No generator is run by this test.
"""
import copy
import json
import math
from pathlib import Path
import re

import test_focus_runtime as runtime
from test_focus_runtime import World as BaseWorld, T, E, P, D
from test_presentation import Preview
from script_ast import parse, first, values, walk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NS = 'COLDWAR_UAE_1970_contracts'


def read(path): return parse((ROOT / path).read_text(encoding='utf-8-sig'))


POLITICS = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt'))
for key in ('accept_cabinet_bargain', 'form_federation'):
    E[P + key] = POLITICS[P + key]
TREE = first(read('common/national_focus/COLDWAR_UAE_1970_focus.txt'), 'focus_tree')
F = {first(node, 'id'): node for node in values(TREE, 'focus')}
BY = {n['id'].removeprefix(P): n for n in D['nodes']}


class World(BaseWorld):
    def __init__(self):
        super().__init__()
        self.boundaries = []
        self.cosmetic = 'UAE_TRUCIAL_1970'

    def execute(self, rows, state=None):
        remaining = []
        for key, op, value in rows:
            if key in {P+'sync_offices', P+'politics_sync'}:
                self.boundaries.append(key)
            elif key == 'drop_cosmetic_tag':
                self.cosmetic = None
            else:
                remaining.append((key, op, value))
        super().execute(remaining, state)


class CurrentPreview(Preview):
    """Render numeric rows in a representative 1972 office context."""
    def condition(self, key, op, value, state):
        if key == 'date':
            today = (1972, 1, 1)
            target = tuple(map(int, value.split('.')))
            return {'<': today < target, '>': today > target, '=': today == target}[op]
        return super().condition(key, op, value, state)

    def execute(self, rows, state=None):
        super().execute([row for row in rows if row[0] not in {'add_ideas', 'remove_ideas'}], state)


def near(actual, expected): assert math.isclose(actual, expected, abs_tol=1e-9), (actual, expected)


def assets(w):
    return copy.deepcopy((w.variables['treasury'], w.states, w.queue, w.xp))


def parents(w, key):
    for group in BY[key]['prerequisites']:
        w.flags[P+'done_'+group[0].removeprefix(P)] = None


def finish(w, key):
    assert w.test(T[P+'can_apply_'+key]), key
    w.call('apply_'+key)
    assert w.has_flag(P+'done_'+key), key


def run():
    cases = []
    for choice, opposite, receipt in [('dual_veto', 'federal_ministries', 'guarantees_agreed'),
                                       ('federal_ministries', 'dual_veto', 'mandate_agreed')]:
        w = World(); w.subject = None; w.variables['treasury'] = -1
        assert w.cosmetic == 'UAE_TRUCIAL_1970'
        for key in ('council', 'development_fund', 'seven_emirates', 'charter'):
            finish(w, key)
        assert w.has_flag(P+'founders_consented')
        assert w.test(T[P+'can_apply_dual_veto']) and w.test(T[P+'can_apply_federal_ministries'])
        finish(w, choice)
        assert w.has_flag(P+receipt) and not w.test(T[P+'can_apply_'+opposite])
        before = assets(w); w.call('apply_'+opposite)
        assert before == assets(w) and not w.has_flag(P+'done_'+opposite)
        finish(w, 'sovereign_union')
        assert w.cosmetic == 'UAE_TRUCIAL_1970' and not w.has_flag(P+'federation_formed')
        finish(w, 'proclaim_federation')
        assert w.cosmetic is None and w.has_flag(P+'federation_formed') and w.has_flag(P+'federation_established')
        before = assets(w)
        for key in ('charter', choice, 'sovereign_union', 'proclaim_federation'):
            w.call('apply_'+key)
        assert before == assets(w)
    cases.append('Both direct constitutional choices reach proclamation without meetings, remain exclusive, and change Trucial identity only through proclamation with no duplicate charge')

    w = World(); w.variables['treasury'] = -1
    finish(w, 'treaty_coast'); before = assets(w)
    finish(w, 'petition_independence')
    assert w.subject == 'ENG' and before == assets(w)
    near(w.variables[P+'british_offices_productivity'], .05)
    near(w.variables[P+'fragmented_authority_bureaucracy_cost_multiplier_modifier'], .17)
    before = assets(w); w.call('apply_petition_independence')
    w.subject = None; w.call('refresh_programmes')
    near(w.variables[P+'fragmented_authority_bureaucracy_cost_multiplier_modifier'], .17)
    assert before == assets(w)
    assert not any(k == 'country_event' or 'send_early_handover' in k for k, _, _ in walk(E[P+'apply_petition_independence']))
    cases.append('Prepare the Handover grants real office productivity and permanent civil-service relief once, creates no independence request, charges no handover fee and survives withdrawal')

    w = World(); w.subject = None; w.variables['treasury'] = -1
    finish(w, 'council'); before_cash = w.variables['treasury']
    before_bureaucracy = w.variables[P+'union_bureaucracy_cost_multiplier_modifier']
    finish(w, 'development_fund')
    near(w.variables['treasury'], before_cash - .01)
    near(w.variables[P+'unequal_development_stability_factor'], -.03)
    near(w.variables[P+'union_bureaucracy_cost_multiplier_modifier'] - before_bureaucracy, .03)
    before = assets(w); w.call('apply_development_fund'); w.call('refresh_programmes')
    assert before == assets(w)
    cases.append('Development Fund pays its native focus cost once from a negative balance and applies +3pp stability relief with +3% ongoing administration cost')

    for key in ('rulers_compact', 'presidential_union'):
        for context in ('protected', 'independent_unproclaimed', 'formed'):
            w = World(); parents(w, key)
            if context != 'protected': w.subject = None
            if context == 'formed':
                w.flags[P+'federation_formed'] = None; w.flags[P+'federation_established'] = None
            before = assets(w)
            if context != 'formed':
                assert not w.test(T[P+'can_apply_'+key]), (key, context)
                w.call('apply_'+key)
                assert not w.has_flag(P+'done_'+key) and before == assets(w)
            else:
                w.flags[P+'constitutional_crisis'] = None
                finish(w, key)
                if key == 'rulers_compact':
                    assert w.has_flag(P+'cabinet_settled') and not w.has_flag(P+'constitutional_crisis')
                    assert P+'sync_offices' in w.boundaries
                    near(w.variables[P+'fragmented_authority_bureaucracy_cost_multiplier_modifier'], .17)
                else:
                    assert w.has_flag(P+'delegated_powers_accepted') and w.has_flag(P+'executive_delegated')
                snapshot = assets(w), copy.deepcopy(w.variables), list(w.boundaries)
                w.call('apply_'+key)
                assert snapshot == (assets(w), w.variables, w.boundaries)
    cases.append('Cabinet and presidential delegation reject protected/unproclaimed contexts; formed-state direct settlements apply their real helper/receipts and relief exactly once')

    w = World(); w.subject = None; parents(w, 'citizen_republic')
    w.governments = {'western_liberals_are_in_power'}
    finish(w, 'citizen_republic')
    near(w.variables[P+'constitutional_offices_productivity'], .05)
    before = assets(w); w.governments = {'western_autocrats_are_in_power'}; w.call('refresh_programmes')
    near(w.variables[P+'constitutional_offices_productivity'], 0)
    w.governments = {'western_liberals_are_in_power'}; w.call('refresh_programmes')
    near(w.variables[P+'constitutional_offices_productivity'], .05)
    assert before == assets(w)
    w = World(); w.subject = None; finish(w, 'gulf_diplomacy')
    near(w.variables[P+'diplomacy_political_power_factor'], .05)
    near(w.variables[P+'diplomacy_improve_relations_maintain_cost_factor'], -.20)
    near(w.variables[P+'diplomacy_bureaucracy_cost_multiplier_modifier'], .03)
    cases.append('Republic office productivity follows its actual party programme without replay, while Gulf Diplomacy delivers native PP/relations/administration modifiers directly')

    # Numeric rows must be emitted in the nonexecuting native reward preview,
    # not just narrated in descriptions. Exercise the changing inherited relief.
    for key, modifier, expected in [('petition_independence', 'bureaucracy_cost_multiplier_modifier', -.03),
                                     ('development_fund', 'stability_factor', .03),
                                     ('rulers_compact', 'bureaucracy_cost_multiplier_modifier', -.03)]:
        preview = CurrentPreview(); preview.subject = None
        if key == 'rulers_compact':
            preview.flags.update({P+'federation_formed': None, P+'federation_established': None})
        rows = first(first(F[P+key], 'completion_reward'), 'effect_tooltip')
        preview.execute(rows)
        assert any(name == modifier+'_tt' and math.isclose(value, expected, abs_tol=1e-9) for name, value in preview.lines), (key, preview.lines)
    cases.append('Installed native focus previews show the exact +3pp stability / -3pp inherited-administration changes as numeric modifier rows')

    # All removed ID slots are tested explicitly; retained family identities
    # must not shift when catalogue entries are removed.
    events_path = ROOT/'events/COLDWAR_UAE_1970_contracts.txt'
    event_text = events_path.read_text(encoding='utf-8-sig')
    event_ids = set(re.findall(r'(?m)^\s*id = '+NS+r'\.(\d+)\s*$', event_text))
    retired_bases = [2000, 12000, 13000, 14000, 16000, 17000, 18000,
                     110000, 111000, 112000, 113000, 114000, 115000, 116000,
                     117000, 118000, 119000, 120000, 121000, 80000]
    removed = {str(base+round_) for base in retired_bases for round_ in range(1, 129)}
    assert not event_ids & removed
    assert len(event_ids) == 1920, len(event_ids)
    authored = [events_path] + list((ROOT/'common').rglob('*COLDWAR_UAE_1970*.txt'))
    references = {ident for path in authored for ident in re.findall(NS+r'\.(\d+)', path.read_text(encoding='utf-8-sig'))}
    assert references <= event_ids, sorted(references-event_ids)
    for base in (1000, 3000, 15000, 19000, 20000, 70000, 90000):
        assert {str(base+round_) for round_ in range(1,129)} <= event_ids, base
    cases.append('All2560 redundant event slots are absent;1920 real foreign-consent delivery IDs resolve, including focus-led Kuwait agreements and British/procurement confirmations')

    diplomatic = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_diplomacy.txt'))
    retired = ('early_handover', 'uk_protection', 'uk_release', 'dated_release', 'island_offer', 'jeddah', 'gcc')
    for key in retired:
        assert P+'send_'+key+'_offer' not in diplomatic
    # Legacy pending state is cleared without executing an obsolete meeting.
    assert (P+'british_tick', '=', 'yes') in diplomatic[P+'diplomacy_tick']
    tick = diplomatic[P+'british_tick']
    for key in ('founders','mediate','court_settlement','delegation','cabinet_bargain','withdrawal','british_amendment','british_withdrawal_policy','reserve_withdraw','sharjah','oil_downturn','kuwait'):
        assert any(k == 'clr_country_flag' and v == P+'meeting_pending_'+key for k, _, v in walk(tick)), key
    for key in ('charter', 'dual_veto', 'federal_ministries', 'petition_independence', 'rulers_compact', 'presidential_union'):
        assert not any(k == 'country_event' for k, _, _ in walk(E[P+'apply_'+key])), key
    import test_diplomacy as diplomacy_runtime
    diplomacy_runtime.E.update(diplomatic)
    dw = diplomacy_runtime.World()
    for key in ('founders','mediate','court_settlement','delegation','cabinet_bargain','withdrawal','british_amendment','reserve_withdraw'):
        dw.c['UAE']['flags'][P+'meeting_pending_'+key] = None
    dw.c['ENG']['flags'][P+'meeting_pending_british_withdrawal_policy'] = None
    dw.c['UAE']['flags'][P+'withdrawal_schedule_active'] = None
    dw.c['UAE']['flags'][P+'historical_withdrawal_schedule'] = None
    def bilateral_assets():
        return copy.deepcopy(([(tag, c['v']['treasury'], c['stock'], c['xp']) for tag, c in dw.c.items()], dw.subject, dw.queue))
    before = bilateral_assets()
    dw.call('diplomacy_tick'); dw.call('diplomacy_tick')
    assert bilateral_assets() == before and not dw.events
    assert dw.has('UAE', P+'withdrawal_schedule_active') and dw.has('UAE', P+'historical_withdrawal_schedule')
    for tag, country in dw.c.items():
        assert not any(flag.startswith(P+'meeting_pending_') and dw.has(tag, flag) for flag in country['flags'])
    cases.append('Retired offer senders are not callable and obsolete pending meetings are cleared without dispatch, payment or lost signed treaty state')

    report = {'passed': len(cases), 'cases': cases, 'errors': [], 'engine_tested': False,
              'boundaries': 'Installed authored AST executed. Native economic recalculation, portrait/office synchronization, HOI4 event rendering and MP transport are outside this suite.'}
    (HERE/'streamline_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__': run()
