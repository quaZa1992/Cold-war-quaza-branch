# IMPERIA CW — Cold War: uae 1970 — test revision.
"""Check the user's independence/proclamation correction in installed scripts."""
import hashlib
import json
import re
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, values, walk
from revision import current_design
from focus_only import RETAINED_DECISIONS, FOCUS_ACTIONS, NEW_FOCUS_KEYS
from test_focus_runtime import World, T, E, P


def run():
    cases = []
    original = json.loads((HERE / 'approved_design.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((HERE / 'approved_design.json').read_bytes()).hexdigest() == '23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272'
    revised = current_design()
    old = {n['id']: n for n in original['nodes']}
    new = {n['id']: n for n in revised['nodes']}
    allowed = {P + k for k in ['council', 'treaty_coast', 'sovereign_union', 'rak_accession', 'federal_council', 'dirham',
                             'industrial_port', 'aviation_hub', 'schools_clinics', 'water_network', 'citizen_housing', 'worker_towns', 'efficient_services', 'trading_coast', 'port_planning',
                             'oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase']}
    allowed.update(n['id'] for n in revised['nodes'] if n.get('streamlined'))
    assert set(new) - set(old) == {P + k for k in ['proclaim_federation', 'jebel_ali_smelter', 'steel_rolling_mills', *NEW_FOCUS_KEYS]} and not set(old) - set(new)
    # Funding eligibility was removed globally by the user's later revision;
    # all unrelated fields remain covered by the immutable approval comparison.
    for key, before in old.items():
        if key in allowed:
            continue
        after = new[key]
        normalized = json.loads(json.dumps(before))
        # Later explicit user revision: all national focuses take70 days.
        normalized.update(days=70, cost=10.0)
        for field in ('available', 'effect_body'):
            normalized[field] = re.sub(r'check_variable\s*=\s*\{[^{}]*\btreasury\b[^{}]*\}', '', normalized[field]).strip()
        for contract in normalized.get('requirement_contracts', []):
            contract['proposed_code'] = re.sub(r'check_variable\s*=\s*\{[^{}]*\btreasury\b[^{}]*\}', '', contract['proposed_code']).strip()
        # Latest explicit revision retires domestic decision delivery, preserving
        # original actual rewards, costs and coordinates on these other nodes.
        normalized['reward_summary'] = [line for line in normalized.get('reward_summary', [])
            if not any(word in line.lower() for word in
                ('unlock', 'decision', 'respond to an invasion', 'crisis popup'))]
        if key.removeprefix(P) in FOCUS_ACTIONS:
            normalized['focus_actions'] = FOCUS_ACTIONS[key.removeprefix(P)]
        assert after == normalized, key
    expected_decisions = json.loads(json.dumps([d for d in original['decisions']
        if d['id'].removeprefix(P+'decision_') in RETAINED_DECISIONS]))
    for d in expected_decisions:
        if d['id'] in {P+'decision_reserve_withdraw', P+'decision_british_withdrawal_policy'}:
            d['pp'] = 0
    assert revised['decisions'] == expected_decisions
    assert all(new[k]['treasury_cost_billion'] == n['treasury_cost_billion'] for k, n in old.items() if k not in allowed)
    cases.append('Immutable approval preserved; unrelated rewards and costs retained with only explicit duration/funding/unlock metadata normalization; only three oil/reserve decisions remain')

    w = World(); w.variables['treasury'] = 0
    assert w.test(T[P + 'can_apply_treaty_coast'])
    assert not w.test(T[P + 'can_apply_council'])
    w.call('apply_council')
    assert not w.has_flag(P + 'done_council')
    w.call('apply_treaty_coast')
    assert w.has_flag(P + 'done_treaty_coast') and w.variables['treasury'] == 0
    assert w.variables[P + 'british_bureaucracy_cost_multiplier_modifier'] == -.05
    assert w.test(T[P + 'can_apply_renew_protection']) and w.test(T[P + 'can_apply_petition_independence'])
    cases.append('Zero-treasury British subject can take Protected Coast and reach both policy choices; transition grants nothing')

    w = World(); w.subject = 'USA'
    assert not w.test(T[P + 'can_apply_treaty_coast']) and not w.test(T[P + 'can_apply_council'])
    w.subject = None
    assert w.test(T[P + 'can_apply_council']) and not w.test(T[P + 'can_apply_treaty_coast'])
    w.call('apply_council')
    assert w.has_flag(P + 'done_council')
    w.subject = 'ENG'
    assert not w.test(T[P + 'can_apply_council'])
    cases.append('Transition requires full independence, including after re-subjection; British entry requires the actual UK overlord')

    tree = first(parse((ROOT / 'common/national_focus/COLDWAR_UAE_1970_focus.txt').read_text()), 'focus_tree')
    focuses = {first(f, 'id'): f for f in values(tree, 'focus')}
    assert len(focuses)==114
    assert all(n['days']==70 and n['cost']==10 for n in revised['nodes'])
    assert all(float(first(f,'cost'))==10 for f in focuses.values())
    cases.append('All114 UAE national focuses have nominal70-day duration in current design and installed cost10; other fields retain their separate approved revisions')
    for k in ['rak_accession', 'federal_council']:
        assert [values(r, 'focus') for r in values(focuses[P + k], 'prerequisite')] == [[P + 'proclaim_federation']]
    assert [values(r, 'focus') for r in values(focuses[P + 'proclaim_federation'], 'prerequisite')] == [[P + 'sovereign_union']]
    assert not any(k == P + 'form_federation' for k, _, _ in walk(E[P + 'apply_sovereign_union']))
    assert any(k == P + 'form_federation' for k, _, _ in walk(E[P + 'apply_proclaim_federation']))
    politics = dict((k, v) for k, _, v in parse((ROOT / 'common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt').read_text()))
    guard = first(first(politics[P + 'form_federation'], 'if'), 'limit')
    assert ('is_subject', '=', 'no') in guard
    for k in ['done_sovereign_union', 'done_proclaim_federation', 'founders_consented']:
        assert ('has_country_flag', '=', P + k) in guard
    callers = [(name, k) for name, body in E.items() for k, _, _ in walk(body) if k == P + 'form_federation']
    assert callers == [(P + 'apply_proclaim_federation', P + 'form_federation')]
    cases.append('Only the new proclamation focus forms/names the federation, after independence and the founding settlement')

    w = World(); w.flags[P + 'done_sovereign_union'] = None; w.flags[P + 'founders_consented'] = None
    assert not w.test(T[P + 'can_apply_proclaim_federation'])
    w.subject = None
    assert w.test(T[P + 'can_apply_proclaim_federation'])
    w.flags[P + 'done_dual_veto'] = None
    assert not w.test(T[P + 'can_apply_rak_accession'])
    w.flags[P + 'done_proclaim_federation'] = None
    assert w.test(T[P + 'can_apply_rak_accession'])
    cases.append('Independence cannot skip proclamation or unlock its follow-ups through the old withdrawal join')

    # Exercise the installed identity provider separately from the focus-only
    # numerical harness: history/cosmetic dispatch is a native API boundary.
    import importlib.util
    spec = importlib.util.spec_from_file_location('coldwar_uae_revision_politics_runtime', HERE/'test_politics.py')
    political_runtime = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(political_runtime)
    previous_effects = political_runtime.E
    political_runtime.E = politics
    try:
        c = political_runtime.Country()
        c.flags.update({P+'done_sovereign_union', P+'done_proclaim_federation', P+'founders_consented'})
        c.call('form_federation')
        assert c.cosmetic == 'UAE_TRUCIAL_1970' and c.leader == 'Trucial States Council'
        c.subject = None
        c.call('form_federation')
        assert c.cosmetic is None and c.leader == 'Zayed bin Sultan Al Nahyan'
        assert c.leader_ideology == 'Western_Autocracy' and 'western_Western_Autocracy' in c.traits
        assert c.variables[P+'president'] == 0 and c.portrait.endswith('zayed_bin_sultan_al_nahyan.dds')
        state = (c.cosmetic, c.leader, c.portrait, c.installs)
        c.call('form_federation')
        assert state == (c.cosmetic, c.leader, c.portrait, c.installs)
    finally:
        political_runtime.E = previous_effects
    names = (ROOT/'localisation/english/countries_l_english.yml').read_text(encoding='utf-8-sig')
    assert re.search(r'UAE_democratic:\s*(?:0\s*)?"United Arab Emirates"', names)
    for size in ('', 'medium/', 'small/'):
        assert (ROOT/('gfx/flags/'+size+'UAE_TRUCIAL_1970_democratic.tga')).exists()
        # Dropping the cosmetic resolves the actual native UAE flag namespace.
        assert any((base/('gfx/flags/'+size+'UAE_democratic.tga')).exists() or
                   (base/('gfx/flags/'+size+'UAE.tga')).exists() for base in
                   [ROOT, Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')])
    from PIL import Image
    # Check image content independently of the SVG renderer: the old incorrect
    # modern-UAE patterns used these same filenames and would pass path tests.
    for size, expected in [('', (82, 52)), ('medium/', (41, 26)), ('small/', (10, 7))]:
        for outlook in ('', '_democratic', '_communism', '_fascism', '_neutrality', '_nationalist'):
            with Image.open(ROOT/('gfx/flags/'+size+'UAE_TRUCIAL_1970'+outlook+'.tga')) as image:
                image = image.convert('RGB')
                assert image.size == expected
                for fraction in (.1, .9):
                    red = image.getpixel((1, int((image.height-1)*fraction)))
                    assert red[0] > 150 and red[1] < 100 and red[2] < 100
                white = image.getpixel((1, image.height//2))
                assert min(white) > 200
                assert any(g > r+5 and g > b+5 for r, g, b in
                           (image.getpixel((x, y)) for y in range(image.height) for x in range(image.width)))
    cases.append('Installed proclamation preserves the protected Council, then once independent selects historical Zayed/Western autocracy/portrait and drops the Trucial name-and-flag namespace; repeats do not recreate the president')

    assert 'convene_constitution' not in new[P+'federal_council'].get('focus_only_effect_body', '')
    competition = new[P+'constitutional_competition']
    assert competition['prerequisites'] == [[P+'federal_council']]
    assert P+'convene_constitution' in competition['focus_only_effect_body']
    convention_calls = [name for name, body in E.items()
                       if name.startswith(P+'apply_') and
                       any(k == P+'convene_constitution' for k, _, _ in walk(body))]
    assert convention_calls == [P+'apply_constitutional_competition']
    cases.append('Historical consultative National Council recognises associations without forcing elections; only optional Constitutional Competition opens elected party government')

    def no_funds_predicate(body, seen=frozenset()):
        for key, _, value in walk(body):
            if key == 'check_variable':
                variable = first(value, 'var', value[0][0])
                assert variable != 'treasury', ('Focus treasury veto remains', value)
            if key == 'custom_trigger_tooltip':
                assert not str(first(value, 'tooltip', '')).endswith('_funds_tt')
            if key in T and key not in seen:
                no_funds_predicate(T[key], seen | {key})
    for n in revised['nodes']:
        no_funds_predicate(first(focuses[n['id']], 'available', []))
        body = T[P + 'can_apply_' + n['id'].removeprefix(P)]
        no_funds_predicate(body)
        # Inspect actual focus eligibility, not downstream recipient-controlled
        # response handlers whose own transaction invoices legitimately differ.
        application = E[P + 'apply_' + n['id'].removeprefix(P)]
        no_funds_predicate(first(first(application, 'if'), 'limit', []))
    cases.append('All114 focus eligibility and actual application guards have no direct or transitive treasury veto or funds-tooltip label; separate foreign-consent transactions remain outside this predicate audit')
    report = {'passed': len(cases), 'cases': cases, 'errors': [], 'engine_tested': False}
    (HERE / 'revision_validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
