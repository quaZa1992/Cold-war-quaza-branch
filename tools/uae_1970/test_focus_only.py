# IMPERIA CW — Cold War: uae 1970 — test focus only.
"""Independent installed-AST checks for the UAE focus-only policy revision.

The existing interpreters execute authored guards/transactions. Native economy,
portrait installation, UI rendering and multiplayer transport remain boundaries.
"""
from pathlib import Path
import copy
import importlib.util
import json
import math
import re

import test_diplomacy as contracts
import test_focus_runtime as runtime
from script_ast import parse, first, values, walk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P = 'COLDWAR_UAE_'
spec = importlib.util.spec_from_file_location('uae_focus_only_politics_fixture', HERE/'test_politics.py')
political = importlib.util.module_from_spec(spec)
spec.loader.exec_module(political)
Country = political.Country


def read(path): return parse((ROOT/path).read_text(encoding='utf-8-sig'))


TREE = first(read('common/national_focus/COLDWAR_UAE_1970_focus.txt'), 'focus_tree')
F = {first(n, 'id'): n for n in values(TREE, 'focus')}
FOCUS_E = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt'))
FOCUS_T = dict((k, v) for k, _, v in read('common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt'))
POLITICS_E = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt'))
contracts.E.update(dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_UAE_1970_diplomacy.txt')))
contracts.T.update(dict((k, v) for k, _, v in read('common/scripted_triggers/COLDWAR_UAE_1970_diplomacy.txt')))
contracts.E.update(FOCUS_E)
contracts.T.update(FOCUS_T)
contracts.EVENTS = {first(n, 'id'): n for k, _, n in read('events/COLDWAR_UAE_1970_contracts.txt') if k == 'country_event'}
for key in ('organise_association', 'convene_constitution'):
    contracts.E[P+key] = POLITICS_E[P+key]
political.E.update(POLITICS_E)


class World(contracts.World):
    def __init__(self):
        super().__init__()
        self.elections = False
        self.scenario = True

    def cond(self, k, op, v, c, root, prev, state):
        if k == P+'1970_campaign': return (c == 'UAE' and self.scenario) == (v == 'yes')
        if k == 'custom_trigger_tooltip':
            return self.test([r for r in v if r[0] != 'tooltip'], c, root, prev, state)
        if k == 'emerging_autocracy_are_in_power':
            return (self.c[c]['v'].get('ruling_party', 0) == 7) == (v == 'yes')
        return super().cond(k, op, v, c, root, prev, state)

    def execute(self, rows, current='UAE', root=None, prev=None, state=None):
        remaining = []
        for k, op, v in rows:
            if k == 'set_politics':
                self.elections = first(v, 'elections_allowed') == 'yes'
            elif k == 'update_dirty_politicsview_expanded':
                pass  # Native UI redraw, no invented policy execution.
            else: remaining.append((k, op, v))
        super().execute(remaining, current, root, prev, state)

    def finish(self, key):
        assert self.test(FOCUS_T[P+'can_apply_'+key]), key
        self.call('apply_'+key)
        assert self.has('UAE', P+'done_'+key), key


def parents(w, key):
    for group in values(F[P+key], 'prerequisite'):
        w.c['UAE']['flags'][P+'done_'+values(group, 'focus')[0].removeprefix(P)] = None


def assets(w):
    return copy.deepcopy(([(tag, c['v']['treasury'], c['stock'], c['xp']) for tag, c in w.c.items()],
                          w.states, w.queue, w.access, w.subject))


def near(a, b): assert math.isclose(a, b, abs_tol=1e-9), (a, b)


def run():
    cases = []
    assert len(F) == 114
    remaining, reached = set(F), set()
    for ident, node in F.items():
        for group in values(node, 'prerequisite') + values(node, 'mutually_exclusive'):
            assert set(values(group, 'focus')) <= F.keys(), ident
        for exclusion in [x for g in values(node, 'mutually_exclusive') for x in values(g, 'focus')]:
            assert ident in [x for g in values(F[exclusion], 'mutually_exclusive') for x in values(g, 'focus')], ident
        assert float(first(node, 'cost')) == 10
    while remaining:
        new = {ident for ident in remaining if all(any(p in reached for p in values(group, 'focus'))
               for group in values(F[ident], 'prerequisite'))}
        assert new, ('Unreachable/cyclic prerequisite graph', sorted(remaining))
        reached |= new; remaining -= new
    category = first(read('common/decisions/COLDWAR_UAE_1970_decisions.txt'), P+'1970_decisions_category')
    expected = {P+'decision_'+key for key in ('oil_restraint','reserve_deposit','reserve_withdraw')}
    assert {k for k, _, _ in category} == expected
    for focus in F.values():
        assert {v for k, _, v in walk(first(focus, 'completion_reward')) if k == 'unlock_decision_tooltip'} <= expected
    cases.append('All114 nominal70-day focuses have a complete, acyclic prerequisite graph and symmetric exclusions; only OPEC restraint and reserve deposit/withdrawal remain as authored UAE decisions')

    resources = first(read('common/decisions/categories/00_resources_expansion.txt'), 'resources_expansion_category')
    visibility = first(resources, 'visible')
    assert visibility == [('NOT','=',[(P+'1970_campaign','=','yes')])]
    w = World()
    assert not w.test(visibility, 'UAE')
    w.scenario = False
    assert w.test(visibility, 'UAE')
    w.scenario = True
    assert w.test(visibility, 'ENG')
    cases.append('Native resource-expansion category is hidden only for 1970 UAE; later UAE and other countries retain the original resource decisions')

    w = World(); w.subject = None
    w.c['UAE']['flags'].update({P+'federation_formed':None, P+'federation_established':None})
    parents(w, 'federal_council'); w.finish('federal_council')
    assert w.has('UAE', P+'islah_organised') and not w.elections
    assert not w.has('UAE', P+'constitutional_convention')
    assert w.c['UAE']['v']['party_banned_array^12'] == 0
    w.finish('constitutional_competition')
    assert w.elections and w.has('UAE', P+'constitutional_convention')
    before = assets(w); w.call('apply_constitutional_competition')
    assert assets(w) == before
    # The actual optional election helper, not the historical council focus,
    # owns elections and the wider party legalization.
    assert not any(k == P+'convene_constitution' for k, _, _ in walk(FOCUS_E[P+'apply_federal_council']))
    assert any(k == P+'convene_constitution' for k, _, _ in walk(FOCUS_E[P+'apply_constitutional_competition']))
    cases.append('Historical federal council only recognizes the association; the separate optional constitutional focus enables elections and legal party competition once')

    # Existing domestic investment delivers its permanent programme, without
    # replaying any removed course's temporary bonus or secondary invoice.
    for key in ('municipal_compact','public_industry','labour_code','technical_cadres',
                'charitable_network','port_planning','aviation_hub','industrial_port',
                'citizen_housing','worker_towns','technical_institutes','sustainable_force','land_deterrent'):
        body = FOCUS_E[P+'apply_'+key]
        assert not any(k == 'add_dynamic_modifier' for k, _, _ in walk(body)), key
        assert not any(k == 'country_event' for k, _, _ in walk(body)), key
        assert not any(k.startswith(P+'decision_') or k.startswith(P+'send_') for k, _, _ in walk(body)), key
    cases.append('Domestic programme focuses contain no former course popup, extra timed carrier or removed decision callback; existing permanent programme remains the reward source')

    w = World(); w.subject = None; w.c['UAE']['groups'] = {'arab'}
    w.c['UAE']['v']['ruling_party'] = 7
    parents(w, 'arab_solidarity')
    before_cash = w.c['UAE']['v']['treasury']
    w.finish('arab_solidarity')
    event = w.events[-1]
    assert event[1] == 'EGY' and w.c['UAE']['v'].get(P+'offer_round_arab_exchange') == 1
    focus_cost = next(n['treasury_cost_billion'] for n in runtime.D['nodes'] if n['id'] == P+'arab_solidarity')
    near(w.c['UAE']['v']['treasury'], before_cash - focus_cost)
    before = assets(w), len(w.events)
    w.call('apply_arab_solidarity'); w.call('focus_arab_exchange'); w.call('retry_focus_offers')
    assert before == (assets(w), len(w.events))
    w.choose(*event)
    near(w.c['UAE']['v']['treasury'], before_cash - focus_cost - .686*.02)
    assert w.states[179]['productivity'] == 110
    before = assets(w)
    # Re-executing the actual accepted option cannot replay a settled round.
    option = values(contracts.EVENTS[event[0]], 'option')[0]
    w.execute([r for r in option if r[0] not in {'name','trigger','ai_chance'}], event[1])
    assert before == assets(w)
    cases.append('Actual foreign-focus dispatch chooses Egypt, charges the separate focus investment once, waits for true acceptance, then pays the frozen invoice and grants productivity once')

    kuwait = ('kuwait_support','kuwait_transit','kuwait_deployment')
    for key in kuwait:
        assert not values(F[P+key], 'mutually_exclusive'), key
        w = World(); w.subject = None
        w.c['UAE']['flags'].update({P+'federation_formed':None, P+'federation_established':None})
        parents(w, key)
        assert not w.test(FOCUS_T[P+'can_apply_'+key]), key
        w.c['KUW']['wars'].add('IRQ')
        assert w.test(FOCUS_T[P+'can_apply_'+key]), key
        # Neither a generic Gulf diplomacy receipt nor the other two optional
        # commitments may authorize this focus's agreement.
        assert ('has_country_flag','=',P+'done_'+key) in list(walk(contracts.T[P+'can_offer_'+key])), key
        assert not w.test(contracts.T[P+'can_offer_'+key]), key
        before = assets(w); w.call('focus_'+key)
        assert not w.events and before == assets(w), key
        w.finish(key); event = w.events[-1]
        assert event[1] == 'KUW'
        assert w.subject is None and not w.c['UAE']['wars'] and not w.access
        before = assets(w), len(w.events)
        w.call('apply_'+key); w.call('focus_'+key); w.call('retry_focus_offers')
        assert before == (assets(w), len(w.events)), key
        w.choose(*event)
        if key == 'kuwait_support':
            near(w.c['UAE']['v']['treasury'], 10-.686*.03)
            near(w.c['KUW']['v']['treasury'], 10+.686*.03)
        elif key == 'kuwait_transit': assert ('UAE','KUW') in w.access
        else: assert ('KUW','UAE') in w.access
        assert not w.c['UAE']['wars']
    cases.append('Three complementary Kuwait focuses require a real Kuwaiti war and their own focus receipts, dispatch once, retain recipient consent, grant only the selected aid/access and never enter war automatically')

    c = Country(); c.subject = None
    c.flags.add(P+'done_sovereign_union'); c.flags.add(P+'founders_consented')
    c.call('form_federation')
    assert c.cosmetic == 'UAE_TRUCIAL_1970' and c.leader == 'Trucial States Council'
    c.flags.add(P+'done_proclaim_federation'); c.call('form_federation')
    assert c.cosmetic is None and c.leader == 'Zayed bin Sultan Al Nahyan'
    assert c.leader_ideology == 'Western_Autocracy'
    for size in ('','medium','small'):
        from PIL import Image
        image = Image.open(ROOT/'gfx/flags'/size/'UAE_TRUCIAL_1970_democratic.tga').convert('RGB')
        modern = Image.open(ROOT/'gfx/flags'/size/'UAE_democratic.tga').convert('RGB')
        assert image.tobytes() != modern.tobytes(), size
        # The historical cosmetic must not retain the modern green stripe.
        assert not any(g > 70 and g > r*1.25 and g > b*1.25 for r,g,b in image.get_flattened_data()), size
    cases.append('Only proclamation creates the Zayed presidency and removes Trucial identity; historical flag assets differ from modern UAE flags at allthree resolutions')

    # GCC founding/admission remains before its member-only entry. Current
    # members can complete the UAE diplomatic programme without a new petition.
    gulf = FOCUS_T[P+'can_apply_gulf_cooperation']
    rows = list(walk(gulf))
    assert ('has_idea','=','idea_gcc_member_state') in rows
    assert ('COLDWAR_GCC_UAE_can_petition','=','yes') in rows
    assert any(k == 'COLDWAR_GCC_UAE_petition' for k, _, _ in walk(FOCUS_E[P+'apply_gulf_cooperation']))
    shared_root = first(read('common/national_focus/COLDWAR_GCC_1970_shared.txt'), 'shared_focus')
    assert ('has_idea','=','idea_gcc_member_state') in list(walk(first(shared_root,'available')))
    decision = first(first(read('common/decisions/COLDWAR_GCC_1970.txt'), 'COLDWAR_GCC_decisions'), 'COLDWAR_GCC_charter_decision')
    assert ('NOT','=',[('tag','=','UAE')]) in first(decision,'visible')
    cases.append('GCC admission is focus-led for UAE; the shared GCC root still requires actual membership and existing members retain the UAE cooperation programme')

    events_path = ROOT/'events/COLDWAR_UAE_1970_contracts.txt'
    namespace = 'COLDWAR_UAE_1970_contracts'
    ids = set(re.findall(r'^\s*id = '+namespace+r'\.(\d+)\s*$', events_path.read_text(encoding='utf-8-sig'), re.M))
    assert len(ids) == 1920, len(ids)
    paths = [events_path] + list((ROOT/'common').rglob('*COLDWAR_UAE_1970*.txt'))
    referenced = {ident for path in paths for ident in re.findall(namespace+r'\.(\d+)', path.read_text(encoding='utf-8-sig'))}
    assert referenced <= ids, sorted(referenced-ids)
    for base in (115000, 117000, 121000):
        assert not ids & {str(base+round_) for round_ in range(1,129)}
    cases.append('All1920 retained UAE recipient/confirmation delivery IDs resolve; the former Sharjah, oil-downturn and Kuwait policy menus have no event IDs or live orphan calls')

    report = {'passed':len(cases),'cases':cases,'errors':[], 'engine_tested':False,
              'boundaries':'Installed authored focus and recipient-event AST; native engine economy, portraits, UI and multiplayer are explicit unobserved boundaries.'}
    (HERE/'focus_only_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__': run()
