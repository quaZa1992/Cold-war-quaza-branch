# IMPERIA CW — Cold War: iraq 1970 — test usa review regressions.
"""Counterexample regressions for post-install US review findings 1 and 2.

Runs emitted AST in memory, including the actual native MD treasury effect.
Only its money-dirty UI refresh is stubbed. PP payment, native diplomacy,
air missions, save loading and event-display ordering remain engine boundaries.
"""
from pathlib import Path
import hashlib
import json
import math

from test_audit_usa import PolicyWorld, ROOT, local
from usa_module import generate, P
from script_ast import parse, first, values


def world(out):
    w = PolicyWorld(out)
    native = parse((ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8-sig'))
    w.effects['modify_treasury_effect'] = first(native, 'modify_treasury_effect')
    # Display/cache invalidation has no budget authority and is outside this AST harness.
    w.effects['update_money_dirty_variable'] = []
    return w


def option_open(w, number, tag, option=0):
    event = w.events[P+'events.'+str(number)]
    w.run(first(event, 'immediate') or [], w.c[tag])
    return w.tests(first(values(event, 'option')[option], 'trigger') or [], w.c[tag])


def main():
    loaded = ROOT/'common/national_focus/USA_1970.txt'
    original_hash = hashlib.sha256(loaded.read_bytes()).hexdigest()
    out = generate(ROOT)
    category = first(parse(out['common/decisions/categories/COLDWAR_USA_gulf_categories.txt']), P+'category')
    decs = first(parse(out['common/decisions/COLDWAR_USA_gulf_decisions.txt']), P+'category')
    checks = []

    def decide(w, key, tag='USA'):
        d = first(decs, P+key)
        c = w.c[tag]
        assert w.tests(first(category, 'allowed'), c)
        assert w.tests(first(category, 'visible'), c)
        assert w.tests(first(d, 'visible'), c)
        assert w.tests(first(d, 'available'), c)
        w.run(first(d, 'complete_effect'), c)
        return d

    def autonomy(cash=10, gdp=10, skip=False):
        w = world(out)
        local(w)
        w.c['USA'].flags['_completed'] = {P+'baghdad_accord'}
        w.c['IRQ'].var.update(treasury=cash, gdp_total=gdp)
        if skip:
            w.c['IRQ'].flags['MD_skip_treasury_cost'] = None
        d = decide(w, 'accord')
        assert float(first(d, 'cost')) == 25  # Native engine PP charge, not simulated here.
        return w

    for cash,gdp,skip,label in [(.1,10,False,'insufficient treasury'),(10,0,False,'zero GDP'),(10,10,True,'MD treasury skip')]:
        w = autonomy(cash,gdp,skip)
        assert not option_open(w,30,'IRQ')
        # A stale callback or queued old event cannot bypass the visible guard.
        w.accept(30,'IRQ')
        assert not w.flag(w.c['IRQ'],P+'accord_pending')
        assert w.c['IRQ'].var['treasury'] == cash
        assert not w.flag(w.c['IRQ'],P+'accord_paid') and not w.c['KUR'].subject
        checks.append('native legal decision reaches Baghdad event but rejects first payment with '+label)

    w = autonomy(.2)
    assert option_open(w,30,'IRQ')
    assert w.c['IRQ'].var[P+'accord_invoice'] == .2
    w.accept(30,'IRQ')
    assert option_open(w,31,'KUR')
    w.accept(31)
    assert math.isclose(w.c['IRQ'].var['treasury'],0,abs_tol=1e-12)
    assert w.flag(w.c['IRQ'],P+'accord_paid') and w.c['KUR'].subject == 'IRQ'
    for _ in range(3):
        w.accept(31)
    assert math.isclose(w.c['IRQ'].var['treasury'],0,abs_tol=1e-12)
    checks.append('exact affordability pays actual native 2% GDP once and establishes consented self-government')

    for cash,gdp,skip,label in [(.1,10,False,'treasury loss'),(.2,0,False,'GDP loss'),(.2,10,True,'skip enabled after offer')]:
        w = autonomy(.2)
        assert option_open(w,30,'IRQ')
        w.accept(30,'IRQ')
        w.c['IRQ'].var.update(treasury=cash,gdp_total=gdp)
        if skip:
            w.c['IRQ'].flags['MD_skip_treasury_cost'] = None
        assert not option_open(w,31,'KUR')
        w.accept(31)
        assert w.c['IRQ'].var['treasury'] == cash
        assert not w.flag(w.c['IRQ'],P+'accord_paid')
        assert not w.flag(w.c['KUR'],P+'accord_consent') and not w.c['KUR'].subject
        assert w.flag(w.c['KUR'],P+'accord_offer')
        checks.append('ratification rechecks '+label+' before any cash, paid receipt, consent or autonomy mutation')

    for invoice in (0,-.2):
        w=autonomy(.2)
        assert option_open(w,30,'IRQ')
        w.accept(30,'IRQ')
        w.c['IRQ'].var[P+'accord_invoice']=invoice
        assert not option_open(w,31,'KUR')
        w.accept(31)
        assert w.c['IRQ'].var['treasury']==.2
        assert not w.flag(w.c['IRQ'],P+'accord_paid') and not w.c['KUR'].subject
    checks.append('zero/negative stale invoice cannot ratify even with positive GDP and sufficient treasury')

    w = autonomy(.2)
    assert option_open(w,30,'IRQ')
    w.c['IRQ'].var['gdp_total'] = 100
    assert option_open(w,30,'IRQ')
    w.accept(30,'IRQ')
    assert option_open(w,31,'KUR')
    w.accept(31)
    assert w.c['IRQ'].var[P+'accord_invoice'] == .2
    assert math.isclose(w.c['IRQ'].var['treasury'],0,abs_tol=1e-12)
    # A paid receipt is a genuine exception, even if today's price basis/funds
    # are invalid. It restores no money and never quotes or charges again.
    w.c['IRQ'].var.update(gdp_total=0,treasury=0)
    w.c['IRQ'].flags['MD_skip_treasury_cost'] = None
    assert option_open(w,30,'IRQ')
    w.accept(30,'IRQ')
    assert option_open(w,31,'KUR')
    w.accept(31)
    assert w.c['IRQ'].var[P+'accord_invoice'] == .2 and w.c['IRQ'].var['treasury'] == 0
    assert w.c['KUR'].subject == 'IRQ'
    checks.append('positive quote remains frozen across GDP growth/reopen; paid exception remains free without creating new receipts')

    def external():
        w = world(out)
        local(w)
        w.c['USA'].flags['_completed'] = {P+'self_rule',P+'safe_haven'}
        w.c['TUR'].flags[P+'fresh_north_consent'] = None
        assert not w.tests(w.triggers[P+'humanitarian_crisis'],w.c['USA'])
        d = decide(w,'external_policy')
        assert float(first(d,'cost')) == 25
        assert option_open(w,52,'KUR')
        w.accept(52)
        assert w.c['USA'].var[P+'current_settlement_policy'] == 2
        assert w.c['USA'].var[P+'protection_days'] == 90
        assert w.idea(w.c['USA'],P+'northern_air_readiness')
        assert w.idea(w.c['KUR'],P+'external_guarantee')
        # This is an additional recipient choice; protection acceptance does
        # not silently accept a separate air liaison offer on its behalf.
        assert option_open(w,20,'KUR')
        w.accept(20)
        assert w.idea(w.c['KUR'],'COLDWAR_KUR_coalition_air_cover')
        return w

    w = external()
    cash = w.c['USA'].var['treasury']
    for day in range(1,90):
        w.tick()
        assert w.c['USA'].var[P+'protection_days'] == 90-day
        assert w.idea(w.c['USA'],P+'northern_air_readiness')
        assert w.idea(w.c['KUR'],P+'external_guarantee')
        assert not w.tests(w.triggers[P+'humanitarian_crisis'],w.c['USA'])
    w.tick()
    assert w.c['USA'].var[P+'protection_days'] == 0
    assert not w.idea(w.c['USA'],P+'northern_air_readiness')
    assert not w.idea(w.c['KUR'],P+'external_guarantee')
    assert not w.idea(w.c['KUR'],'COLDWAR_KUR_coalition_air_cover')
    assert math.isclose(cash-w.c['USA'].var['treasury'],90*.05/7,abs_tol=1e-10)
    expired_cash = w.c['USA'].var['treasury']
    w.accept(52);w.tick()
    assert w.c['USA'].var[P+'protection_days'] == 0 and w.c['USA'].var['treasury'] == expired_cash
    assert not w.flag(w.c['TUR'],P+'fresh_north_consent')
    checks.append('peaceful unresolved north: legal request, separate consent, real air activation, 90 daily payments and expiry all work without acute crisis')

    invalidities = {
        'withdrawn local consent':lambda w:w.c['KUR'].flags.pop(P+'protection_consent'),
        'lost military access':lambda w:w.c['USA'].access.clear(),
        'host withdraws agreement':lambda w:w.c['TUR'].flags.pop(P+'host_north'),
        'no actual deployed aircraft':lambda w:w.c['USA'].var.update(deployed_air=0),
        'insufficient recurring funds':lambda w:w.c['USA'].var.update(treasury=.001),
        'US treasury skip':lambda w:w.c['USA'].flags.update(MD_skip_treasury_cost=None),
        'local war against USA':lambda w:w.c['KUR'].wars.add('USA'),
        'no controlled local stronghold':lambda w:setattr(w.s['164'],'controller','IRQ'),
    }
    for label,invalidate in invalidities.items():
        w=external();invalidate(w);cash=w.c['USA'].var['treasury'];w.tick()
        assert w.c['USA'].var[P+'protection_days'] == 0, label
        assert not w.idea(w.c['USA'],P+'northern_air_readiness'),label
        assert not w.idea(w.c['KUR'],P+'external_guarantee'),label
        assert not w.idea(w.c['KUR'],'COLDWAR_KUR_coalition_air_cover'),label
        assert w.c['USA'].var['treasury'] == cash,label
    checks.append('live external invalidities terminate term, owned air/liaison and guarantee on same tick without charging: '+', '.join(invalidities))

    # The old Safe Haven cannot secretly renew the new policy without a fresh
    # externally ratified host/recipient commitment.
    w=external();w.c['IRQ'].flags[P+'northern_emergency']=None
    w.c['USA'].var.update({P+'relief_days':90,P+'protection_days':0})
    haven=first(decs,P+'protection')
    assert not w.tests(first(haven,'available'),w.c['USA'])
    w.run(first(haven,'complete_effect'),w.c['USA'])
    assert w.c['USA'].var[P+'protection_days'] == 0
    assert not w.tests(w.triggers[P+'can_request_external_policy'],w.c['USA'])
    checks.append('legacy Safe Haven renewal cannot bypass expired external-contract fresh host consent')

    # Conversely the pre-existing standalone programme keeps its own crisis
    # and relief requirements and its earned readiness after basing loss.
    w=world(out);local(w);w.c['USA'].flags['_completed']={P+'safe_haven'}
    w.c['USA'].var[P+'relief_days']=90
    assert not w.tests(first(haven,'available'),w.c['USA'])
    w.c['IRQ'].flags[P+'northern_emergency']=None
    decide(w,'protection');w.call(P+'start_air');cash=w.c['USA'].var['treasury'];w.tick()
    assert w.c['USA'].var[P+'protection_days'] == 89
    assert math.isclose(cash-w.c['USA'].var['treasury'],(.025+.05)/7,abs_tol=1e-10)
    w.c['USA'].access.clear();w.tick()
    assert w.c['USA'].var[P+'protection_days'] == 0
    assert w.idea(w.c['USA'],P+'northern_air_readiness')
    checks.append('original Safe Haven still needs crisis, relief and funding; standalone earned air readiness survives access loss')

    old_ids={P+'events.'+str(n) for n in [10,11,12,13,20,21,22,23,24,25,30,31,40,41,42,43,44,45,46,47,50,52,54]}
    assert old_ids <= set(w.events)
    installed_events=parse((ROOT/'events/COLDWAR_USA_gulf_events.txt').read_text(encoding='utf-8-sig'))
    assert set(w.events)=={first(e,'id') for e in values(installed_events,'country_event')}
    checks.append('all installed event IDs remain registered exactly; new initialisation does not shift event/save identity')
    assert original_hash == hashlib.sha256(loaded.read_bytes()).hexdigest()
    report={'scope':'Pure emitted-AST regression checks with real native treasury-effect body; no compile/install or engine UI simulation','passed':len(checks),'checks':checks,'loaded_usa_file_unchanged_sha256':original_hash}
    target=ROOT/'docs/design/iraq_1970/audit_2026_10_19/US_REVIEW_REGRESSION_TESTS.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
