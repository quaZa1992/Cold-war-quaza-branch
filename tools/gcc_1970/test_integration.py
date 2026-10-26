# IMPERIA CW — Cold War: gcc 1970 — test integration.
"""Independent emitted-AST integration cases; this is not an HOI4 engine test.

Native treasury, idea, technology-sharing and XP commands are explicit simulation
boundaries. Authored guards/scopes/once receipts are executed from installed AST.
"""
from pathlib import Path
import copy
import json
import math
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk

P = 'COLDWAR_GCC_'
TAGS = ('SAU', 'KUW', 'BHR', 'QAT', 'OMA', 'UAE')


def read(path):
    return parse((ROOT / path).read_text(encoding='utf-8-sig'))


E = dict((k, v) for k, _, v in read('common/scripted_effects/COLDWAR_GCC_1970.txt'))
T = dict((k, v) for k, _, v in read('common/scripted_triggers/COLDWAR_GCC_1970.txt'))
T['gcc_unity_greater_20'] = first(read('common/scripted_triggers/99_GCC_scripted_triggers.txt'), 'gcc_unity_greater_20')
F = {first(v, 'id'): v for _, _, v in read('common/national_focus/COLDWAR_GCC_1970_shared.txt')}
EVENTS = {first(v, 'id'): v for k, _, v in read('events/COLDWAR_GCC_1970.txt') if k == 'country_event'}


class World:
    def __init__(self):
        self.day = 0
        self.global_v = {}
        self.global_flags = set()
        self.targets = {}
        self.arrays = {}
        self.events = []
        self.scenario = True
        self.c = {tag: dict(v={'gdp_total': 1 + i, 'treasury': 10}, flags={},
                           ideas=set(), dynamic=set(), tech=set(), subject=False,
                           jihadist=False, wars=set(), xp={}, pp=0)
                  for i, tag in enumerate(TAGS)}
        self.c['UAE']['flags']['COLDWAR_UAE_federation_established'] = None

    def has(self, tag, flag):
        expiry = self.c[tag]['flags'].get(flag, -1)
        return expiry is None or expiry > self.day

    def scope(self, key, c, root, prev):
        if key == 'ROOT': return root
        if key == 'THIS': return c
        if key == 'PREV': return prev
        if key.startswith('event_target:'): return self.targets.get(key.split(':', 1)[1])
        return key if key in self.c else None

    def num(self, value, c, root, prev):
        try: return float(value)
        except (ValueError, TypeError): pass
        if value.startswith('global.'): return self.global_v.get(value[7:], 0)
        if '.' in value:
            scope, key = value.split('.', 1)
            tag = self.scope(scope, c, root, prev)
            return TAGS.index(tag) + 1 if key == 'id' else self.c[tag]['v'].get(key, 0)
        return self.c[c]['v'].get(value, 0)

    def test(self, rows, c, root=None, prev=None):
        return all(self.cond(k, op, v, c, root or c, prev) for k, op, v in rows)

    def cond(self, k, op, v, c, root, prev):
        if k in {'AND', 'limit', 'hidden_trigger'}: return self.test(v, c, root, prev)
        if k == 'OR': return any(self.cond(a, o, x, c, root, prev) for a, o, x in v)
        if k == 'NOT': return not self.test(v, c, root, prev)
        if k == 'custom_trigger_tooltip': return self.test([r for r in v if r[0] != 'tooltip'], c, root, prev)
        if k in T: return self.test(T[k], c, root, prev) == (v == 'yes')
        scoped = self.scope(k, c, root, prev)
        if scoped: return self.test(v, scoped, root, c)
        if k in {'any_country', 'any_other_country'}:
            return any(self.test(v, tag, root, c) for tag in TAGS if k == 'any_country' or tag != c)
        if k == 'tag': return c == self.scope(v, c, root, prev)
        if k in {'exists', 'always'}: return v == 'yes'
        if k == 'IMP_is_1970_scenario': return self.scenario == (v == 'yes')
        if k == 'country_exists': return v in self.c
        if k == 'is_subject': return self.c[c]['subject'] == (v == 'yes')
        if k == 'no_jihadist_government': return (not self.c[c]['jihadist']) == (v == 'yes')
        if k == 'has_country_flag': return self.has(c, v)
        if k == 'has_global_flag': return v in self.global_flags
        if k == 'has_idea': return v in self.c[c]['ideas']
        if k == 'has_dynamic_modifier': return first(v, 'modifier') in self.c[c]['dynamic']
        if k == 'has_war_with': return self.scope(v, c, root, prev) in self.c[c]['wars']
        if k == 'has_war': return bool(self.c[c]['wars']) == (v == 'yes')
        if k == 'is_in_array':
            array, _, entry = v[0]
            return self.scope(entry, c, root, prev) in self.arrays.get(array, [])
        if k == 'check_variable':
            if first(v, 'var'):
                a, b, cmp = first(v, 'var'), first(v, 'value'), first(v, 'compare', 'equals')
            else: a, cmp, b = v[0]
            a, b = self.num(a, c, root, prev), self.num(b, c, root, prev)
            return {'equals': a == b, '=': a == b, 'less_than': a < b,
                    'greater_than_or_equals': a >= b, '>': a > b}[cmp]
        raise AssertionError('Unmodelled authored condition: ' + k)

    def execute(self, rows, c, root=None, prev=None):
        root = root or c
        branch = False
        for k, op, v in rows:
            if k == 'if':
                branch = self.test(first(v, 'limit', []), c, root, prev)
                if branch: self.execute([r for r in v if r[0] != 'limit'], c, root, prev)
                continue
            if k == 'else':
                if not branch: self.execute(v, c, root, prev)
                branch = False
                continue
            if k == 'hidden_effect': self.execute(v, c, root, prev); continue
            if k in E: self.execute(E[k], c, root, prev); continue
            scoped = self.scope(k, c, root, prev)
            if scoped: self.execute(v, scoped, root, c); continue
            if k == 'for_each_scope_loop':
                for tag in list(self.arrays.get(first(v, 'array'), [])):
                    self.execute([row for row in v if row[0] not in {'array','tooltip'}], tag, root, c)
                continue
            country = self.c[c]
            if k in {'set_variable', 'set_temp_variable', 'add_to_variable', 'multiply_variable', 'multiply_temp_variable'}:
                name, _, value = v[0]
                number = self.num(value, c, root, prev)
                dest = self.global_v if name.startswith('global.') else country['v']
                name = name.removeprefix('global.')
                if k in {'set_variable', 'set_temp_variable'}: dest[name] = number
                elif k == 'add_to_variable': dest[name] = dest.get(name, 0) + number
                else: dest[name] = dest.get(name, 0) * number
            elif k == 'set_country_flag':
                name = first(v, 'flag') if isinstance(v, list) else v
                country['flags'][name] = self.day + int(first(v, 'days')) if isinstance(v, list) else None
            elif k == 'clr_country_flag': country['flags'].pop(v, None)
            elif k == 'set_global_flag': self.global_flags.add(v)
            elif k == 'save_event_target_as': self.targets[v] = c
            elif k == 'country_event': self.events.append((first(v, 'id') if isinstance(v,list) else v, c))
            elif k in {'add_to_array','remove_from_array'}:
                array, _, entry = v[0]
                tag = self.scope(entry, c, root, prev)
                members = self.arrays.setdefault(array, [])
                if k == 'add_to_array': members.append(tag)
                elif tag in members: members.remove(tag)
            elif k == 'modify_treasury_effect': country['v']['treasury'] += country['v']['treasury_change']
            elif k == 'modify_gcc_unity': self.global_v['gcc_unity'] = min(100, max(0, self.global_v.get('gcc_unity', 0) + country['v']['temp_modify_gcc_unity']))
            elif k == 'add_ideas': country['ideas'].add(v)
            elif k == 'add_dynamic_modifier': country['dynamic'].add(first(v, 'modifier'))
            elif k == 'remove_dynamic_modifier': country['dynamic'].discard(first(v, 'modifier'))
            elif k == 'add_to_tech_sharing_group': country['tech'].add(v)
            elif k == 'remove_from_tech_sharing_group': country['tech'].discard(v)
            elif k in {'army_experience', 'navy_experience', 'air_experience'}: country['xp'][k] = country['xp'].get(k, 0) + float(v)
            elif k == 'add_political_power': country['pp'] += float(v)
            elif k in {'effect_tooltip', 'custom_effect_tooltip', 'force_update_dynamic_modifier', 'log'}: pass
            else: raise AssertionError('Unmodelled authored effect: ' + k)

    def call(self, key, tag): self.execute(E[P + key], tag)

    def send(self, tag, recipient):
        self.targets[P + 'recipient'] = recipient
        before = len(self.events)
        self.call('send_offer', tag)
        return self.events[before:]  # The receiver's unique round event.

    def choose(self, event, option=0):
        ident, tag = event
        opt = values(EVENTS[ident], 'option')[option]
        assert self.test(first(opt, 'trigger', []), tag), (ident, tag, option)
        self.execute([r for r in opt if r[0] not in {'name', 'trigger', 'ai_chance'}], tag)

    def account(self):
        return [(tag, self.c[tag]['v']['treasury'], copy.deepcopy(self.c[tag]['xp']), self.c[tag]['pp']) for tag in TAGS]


def near(a, b): assert math.isclose(a, b, abs_tol=1e-9), (a, b)


def run():
    cases = []
    # Read the installed availability, not a separately constructed UI model.
    # Only actual membership/sovereignty are visible. Internal scenario, host
    # and predecessor receipts remain executed inside hidden_trigger.
    for ident,focus in F.items():
        available=first(focus,'available')
        assert available==[
            ('hidden_trigger','=',[(P+'can_apply_'+ident.removeprefix(P),'=','yes')]),
            ('has_idea','=','idea_gcc_member_state'),('is_subject','=','no')],ident
        assert first(focus,'cancel_if_invalid')=='yes'
        assert first(focus,'continue_if_invalid')=='no'
    cases.append('All14 installed focus tooltips hide internal country/scenario/receipt checks and show actual membership and sovereignty')

    for tag in TAGS:
        for ident,focus in F.items():
            for invalid in ('nonmember','membership_lost','subject','wrong_scenario','missing_parent'):
                parents=values(focus,'prerequisite')
                if invalid=='missing_parent' and not parents:continue
                w=World()
                for other in F:
                    if other!=ident:w.c[tag]['flags'][P+'done_'+other.removeprefix(P)]=None
                if invalid!='nonmember':w.c[tag]['ideas'].add('idea_gcc_member_state')
                if invalid=='membership_lost':
                    assert w.test(first(focus,'available'),tag)
                    w.c[tag]['ideas'].clear()
                if invalid=='subject':w.c[tag]['subject']=True
                if invalid=='wrong_scenario':w.scenario=False
                if invalid=='missing_parent':
                    for parent in values(parents[0],'focus'):
                        w.c[tag]['flags'].pop(P+'done_'+parent.removeprefix(P),None)
                assert not w.test(first(focus,'available'),tag),(tag,ident,invalid)
                before=w.account();w.call('apply_'+ident.removeprefix(P),tag)
                assert w.account()==before,(tag,ident,invalid)
                assert not w.has(tag,P+'done_'+ident.removeprefix(P))
    cases.append('All six hosts/all14 focuses reject nonmembers, lost membership, subjects, wrong scenario and missing delivered parents before rewards or payment')

    # Every founder can adopt the whole actual emitted tree. Effects stay local.
    for tag in TAGS:
        w = World(); w.c[tag]['ideas'].add('idea_gcc_member_state')
        w.c[tag]['v']['treasury'] = -1
        neighbours = [(t, copy.deepcopy(w.c[t])) for t in TAGS if t != tag]
        for ident, focus in F.items():
            assert w.test(first(focus, 'available'), tag), (tag, ident)
            w.execute(first(focus, 'completion_reward'), tag)
        paid = sum(n['share'] for n in json.loads((HERE / 'manifest.json').read_text())['nodes'])
        near(w.c[tag]['v']['treasury'], -1 - w.c[tag]['v']['gdp_total'] * paid)
        assert P + 'technical_exchange' in w.c[tag]['tech']
        assert neighbours == [(t, w.c[t]) for t in TAGS if t != tag]
        before = w.account()
        for ident in F: w.call('apply_' + ident.removeprefix(P), tag)
        for _ in range(3): w.call('tick', tag)
        assert before == w.account()
        w.c[tag]['ideas'].clear(); w.call('tick', tag)
        assert not w.c[tag]['dynamic'] and not w.c[tag]['tech']
        assert all(value == 0 for key, value in w.c[tag]['v'].items() if key.startswith(P) and key not in {P+'entry_price'})
        w.c[tag]['ideas'].add('idea_gcc_member_state'); w.call('tick', tag)
        near(w.c[tag]['v'][P+'offices_productivity'], .13)
        assert P + 'technical_exchange' in w.c[tag]['tech'] and before == w.account()
    cases.append('All six full branches: negative balances permitted, exact once GDP costs, own rewards only, suspension and restoration without replay')

    w = World(); w.c['UAE']['subject'] = True
    assert not w.test(T[P+'can_apply_council'], 'UAE')
    w.c['UAE']['subject'] = False; w.c['UAE']['flags'].clear()
    assert not w.test(T[P+'can_apply_council'], 'UAE')
    w.c['SAU']['jihadist'] = True
    assert not w.test(T[P+'can_apply_council'], 'SAU')
    cases.append('Protected UAE, unproclaimed UAE and incompatible government cannot enter')

    for origin in TAGS:
        recipient = next(t for t in TAGS if t != origin)
        w = World()
        decision=first(read('common/decisions/COLDWAR_GCC_1970.txt'),P+'decisions')
        decision=first(decision,P+'charter_decision')
        category=first(read('common/decisions/categories/COLDWAR_GCC_1970.txt'),P+'decisions')
        assert w.test(first(category,'visible'),origin)
        assert w.test(first(decision,'visible'),origin) == (origin != 'UAE')
        assert w.test(first(decision,'available'),origin)
        assert not w.test(first(F[P+'council'],'available'),origin)
        event, = w.send(origin, recipient)
        sender_gdp = w.c[origin]['v']['gdp_total']; recipient_gdp = w.c[recipient]['v']['gdp_total']
        w.c[origin]['v']['gdp_total'] *= 10; w.c[recipient]['v']['gdp_total'] *= 10
        w.choose(event)
        near(w.c[origin]['v']['treasury'], 10 - sender_gdp * .02)
        near(w.c[recipient]['v']['treasury'], 10 - recipient_gdp * .02)
        assert all('idea_gcc_member_state' in w.c[t]['ideas'] for t in (origin, recipient))
        assert w.test(first(F[P+'council'],'available'),origin)
        assert not w.has(origin,P+'done_council') and w.c[origin]['pp']==0
        assert w.global_v['gcc_unity'] == 5
        assert sum(w.has(t, 'gcc_dominant_member') for t in TAGS) == 1
        assert not w.has(origin, P+'offer_awaiting')
        # Double dispatch must not make the real guarded effects run twice.
        before = w.account()
        opt = values(EVENTS[event[0]], 'option')[0]
        w.execute([r for r in opt if r[0] not in {'name', 'trigger', 'ai_chance'}], recipient)
        assert before == w.account()
    cases.append('All six charter origins before the member-only focus: frozen bilateral entry cost, consent, exactly two memberships, unity and leader initialization, duplicate acceptance safe')

    w = World(); event, = w.send('SAU', 'QAT')
    before = w.account(); w.choose(event, 1)
    assert before == w.account() and all(not w.c[t]['ideas'] for t in TAGS)
    event, = w.send('SAU', 'QAT'); w.c['QAT']['v']['treasury'] = 0
    assert not w.test(first(values(EVENTS[event[0]], 'option')[0], 'trigger'), 'QAT')
    w.c['QAT']['v']['treasury'] = 10; w.day = 61; w.call('tick', 'SAU')
    assert not w.test(first(values(EVENTS[event[0]], 'option')[0], 'trigger'), 'QAT')
    newer, = w.send('SAU', 'QAT')
    assert newer[0] != event[0]
    assert not w.test(first(values(EVENTS[event[0]], 'option')[0], 'trigger'), 'QAT')
    w.choose(newer)
    cases.append('Refusal, insufficient agreement funds, expiry and stale same-recipient rounds cannot grant or charge')

    w = World()
    old, = w.send('SAU', 'QAT'); newer, = w.send('KUW', 'QAT')
    w.choose(newer)
    # Qatar is now an existing member and may separately admit the other
    # petitioner. Its existing membership never incurs a second entry charge.
    assert w.test(first(values(EVENTS[old[0]], 'option')[0], 'trigger'), 'QAT')
    assert not w.c['SAU']['ideas']
    w.choose(old, 1)
    assert 'idea_gcc_member_state' in w.c['QAT']['ideas']
    cases.append('Concurrent different-origin invitations cannot double-charge a recipient or grant a nonaccepted founder membership')

    for existing in (False, True):
        for accept in (False, True):
            w = World()
            if existing:
                w.c['SAU']['ideas'].add('idea_gcc_member_state')
                w.c['SAU']['v']['treasury'] = -1
            assert w.test(T[P+'UAE_can_petition'], 'UAE')
            assert not w.test(first(F[P+'council'], 'available'), 'UAE')
            before = w.account()
            w.call('UAE_petition', 'UAE')
            event = w.events[-1]
            assert event == ('COLDWAR_GCC_1970.6001', 'SAU')
            assert not w.test(T[P+'UAE_can_petition'], 'UAE')
            assert w.account() == before
            w.choose(event, 0 if accept else 1)
            if accept:
                near(w.c['UAE']['v']['treasury'], 10 - 6*.02)
                near(w.c['SAU']['v']['treasury'], -1 if existing else 10 - .02)
                assert 'idea_gcc_member_state' in w.c['UAE']['ideas']
                assert w.test(first(F[P+'council'], 'available'), 'UAE')
                assert not w.test(T[P+'UAE_can_petition'], 'UAE')
                assert w.send('UAE', 'SAU') == []
            else:
                assert w.account() == before
                assert 'idea_gcc_member_state' not in w.c['UAE']['ideas']
                assert w.test(T[P+'UAE_can_petition'], 'UAE')
    for invalid in ('subject', 'unproclaimed', 'war', 'expelled', 'already_member'):
        w = World()
        if invalid == 'subject': w.c['SAU']['subject'] = True
        elif invalid == 'unproclaimed': w.c['UAE']['flags'].clear()
        elif invalid == 'war': w.c['SAU']['wars'].add('UAE')
        elif invalid == 'expelled': w.c['SAU']['flags']['recently_expelled_from_gcc'] = None
        else: w.c['UAE']['ideas'].add('idea_gcc_member_state')
        assert not w.test(T[P+'UAE_can_petition'], 'UAE'), invalid
        before = w.account(); w.call('UAE_petition', 'UAE')
        assert not w.events and before == w.account()
    assert (P+'UAE_petition_preview') in E
    petition_preview = first(E[P+'UAE_petition_preview'], 'if')
    assert first(petition_preview, 'custom_effect_tooltip') == 'TT_IF_THEY_ACCEPT'
    for existing in (False, True):
        w = World()
        if existing: w.c['SAU']['ideas'].add('idea_gcc_member_state')
        assert w.test(first(petition_preview, 'limit'), 'UAE')
        w.execute(first(petition_preview, 'effect_tooltip'), 'UAE')
        near(w.c['UAE']['v']['treasury'], 10 - 6*.02)
        near(w.c['SAU']['v']['treasury'], 10 if existing else 10 - .02)
    w = World(); w.c['UAE']['ideas'].add('idea_gcc_member_state')
    assert not w.test(first(petition_preview, 'limit'), 'UAE')
    cases.append('Focus-safe UAE-to-Saudi charter/admission requires real Saudi consent, charges only new members, rejects invalid/both-member contexts and previews native conditional entry costs; common UAE decision hidden')

    w = World()
    for tag in ('SAU', 'KUW', 'QAT'): w.c[tag]['ideas'].add('idea_gcc_member_state')
    w.call('refresh', 'SAU')
    assert w.has('SAU', 'gcc_dominant_member')
    w.global_v['gcc_unity'] = 47
    before = w.account()
    w.c['SAU']['ideas'].clear(); w.call('refresh', 'SAU')
    assert not w.has('SAU', 'gcc_dominant_member')
    w.call('refresh', 'KUW'); w.call('refresh', 'QAT')
    assert w.has('KUW', 'gcc_dominant_member') and not w.has('QAT', 'gcc_dominant_member')
    assert w.global_v['gcc_unity'] == 47 and before == w.account()
    w.c['SAU']['ideas'].add('idea_gcc_member_state'); w.call('refresh', 'SAU')
    assert not w.has('SAU', 'gcc_dominant_member') and w.has('KUW', 'gcc_dominant_member')
    cases.append('Dominant departure transfers to a remaining actual member without resetting unity, paying assets or overriding the valid successor on return')

    from legacy import STARTUP_RELATIVE, startup_region
    text = (ROOT/STARTUP_RELATIVE).read_text(encoding='utf-8-sig')
    begin, end, _ = startup_region(text)
    seed = parse(text[begin:end])
    array = 'global.gcc_member_state'
    for scenario, members in ((True, ()), (False, ()), (True, ('SAU','UAE'))):
        w = World(); w.scenario = scenario
        for tag in members: w.c[tag]['ideas'].add('idea_gcc_member_state')
        w.arrays['global.unrelated_organisation'] = ['UNCHANGED']
        before = w.account()
        w.execute(seed, 'SAU')
        expected = set(members) if scenario else set(TAGS)
        assert set(w.arrays.get(array, [])) == expected, (scenario, members, w.arrays)
        assert len(w.arrays.get(array, [])) == len(expected)
        assert before == w.account() and w.arrays['global.unrelated_organisation'] == ['UNCHANGED']
        if not scenario:
            snapshot = copy.deepcopy(w.arrays)
            for tag in TAGS: w.call('refresh', tag)
            assert w.arrays == snapshot and before == w.account()
    # Old saves can retain the original six unsigned entries. Reconcile each
    # founder without destroying an independently admitted non-founder.
    w = World(); w.arrays[array] = list(TAGS) + ['EGY']
    w.c['EGY'] = copy.deepcopy(w.c['SAU'])
    for tag in ('SAU','UAE','EGY'): w.c[tag]['ideas'].add('idea_gcc_member_state')
    before = w.account()
    for _ in range(2):
        for tag in TAGS: w.call('refresh', tag)
    assert set(w.arrays[array]) == {'SAU','UAE','EGY'} and len(w.arrays[array]) == 3
    assert before == w.account()
    # Trace the actual native on_add/on_remove array API too: history seeding
    # and reconciler idempotence do not rely on a made-up membership container.
    ideas = first(first(read('common/ideas/Factions.txt'), 'ideas'), 'country')
    native_member = first(ideas, 'idea_gcc_member_state')
    w.execute(first(native_member, 'on_add'), 'UAE')
    assert w.arrays[array].count('UAE') == 1
    w.c['UAE']['ideas'].clear(); w.execute(first(native_member, 'on_remove'), 'UAE')
    w.call('refresh', 'UAE')
    assert 'UAE' not in w.arrays[array] and 'EGY' in w.arrays[array]
    w.c['UAE']['ideas'].add('idea_gcc_member_state'); w.call('refresh', 'UAE')
    assert w.arrays[array].count('UAE') == 1
    # The actual ROOT-scoped native puppet/free hooks refresh the same array.
    hooks = first(read('common/on_actions/COLDWAR_GCC_1970.txt'), 'on_actions')
    for puppet_hook in ('on_puppet','on_release_as_puppet'):
        w.c['UAE']['subject'] = True
        w.execute(first(first(hooks, puppet_hook), 'effect'), 'UAE')
        assert 'UAE' not in w.arrays[array]
        w.c['UAE']['subject'] = False
        w.execute(first(first(hooks, 'on_subject_free'), 'effect'), 'UAE')
        assert w.arrays[array].count('UAE') == 1
    w.execute(first(first(hooks, 'on_release_as_free'), 'effect'), 'UAE')
    assert w.arrays[array].count('UAE') == 1 and before == w.account()
    # Execute the original native exercise offer. Only actual retained members
    # receive gcc.26; the four unsigned founder countries receive no invitation.
    native_decisions = first(read('common/decisions/Gulf.txt'), 'gcc_decisions')
    offer = first(native_decisions, 'GCC_offer_joint_exercises_specific')
    w.global_v['gcc_unity'] = 30
    assert w.test(first(offer, 'available'), 'SAU')
    w.events.clear(); w.execute(first(offer, 'complete_effect'), 'SAU')
    assert set(w.events) == {('gcc.26','UAE'),('gcc.26','EGY')}, w.events
    cases.append('Actual native startup array is empty for unsigned1970 founders and unchanged for modern starts; stale entries, departure, puppet/free hooks and native idea callbacks reconcile without duplicates, assets or deleting other members; native exercise offers reach only real members')

    forbidden = {'annex_country', 'puppet', 'create_faction', 'create_faction_from_template', 'add_to_faction', 'give_guarantee', 'add_core_of'}
    assert not [(k, v) for node in list(E.values()) + list(F.values()) + list(EVENTS.values()) for k, _, v in walk(node) if k in forbidden]
    assert len(F) == 14
    report = {'cases': cases, 'passed': True, 'engine_tested': False,
              'boundaries': 'Native engine commands simulated explicitly; authored installed AST conditions, scopes and once-only transactions executed.'}
    (HERE / 'integration_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__': run()
