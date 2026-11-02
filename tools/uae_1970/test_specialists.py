# IMPERIA COLD WAR — Research-only scarcity, save refresh and emitted-preview regressions.
"""Exercise installed script AST; this does not emulate the native UI or MP."""
from copy import deepcopy
import hashlib
from itertools import product
import json
import math
from pathlib import Path

import flavour  # Resolve this country's narrative before sibling parser paths.
from revision import current_design
from test_focus_runtime import World, P, parse, first
from test_presentation import Preview

ROOT = Path(__file__).resolve().parents[2]
SID = P + 'scarce_specialists'


def run():
    checks = 0
    def check(condition, message):
        nonlocal checks
        checks += 1
        assert condition, message

    design = current_design()
    definitions = dict((k, v) for k, _, v in parse((ROOT / 'common/dynamic_modifiers/COLDWAR_UAE_1970_programmes.txt').read_text(encoding='utf-8')))
    tree = first(parse((ROOT / 'common/national_focus/COLDWAR_UAE_1970_focus.txt').read_text(encoding='utf-8')), 'focus_tree')
    focuses = {first(v, 'id'): v for k, _, v in tree if k == 'focus'}
    modifiers = {s['id']: s['modifiers'] for s in design['starting_spirits']}
    check(modifiers[SID] == {'research_speed_factor': -0.15}, 'Scarcity must be research-only at -15%')
    check(first(definitions[SID], 'total_workforce_modifier') is None, 'Installed scarcity still consumes workforce')
    check(all(n['modifiers'].get('total_workforce_modifier', 0) >= 0 for n in design['nodes']), 'A focus still penalizes workforce')

    def active_total(world, modifier):
        return sum(world.num(first(definitions[s], modifier, '0')) for s in world.dynamic if s in definitions)

    keys = ['technical_cadres', 'national_training', 'foreign_specialists', 'technical_institutes']
    for earned in product((False, True), repeat=4):
        world = World()
        world.flags = {P+'done_'+key: None for key, done in zip(keys, earned) if done}
        # Old-save values must not remain active through the new definitions.
        world.variables[SID+'_total_workforce_modifier'] = -0.08
        world.variables[P+'constitutional_total_workforce_modifier'] = -0.03
        world.variables[SID+'_research_speed_factor'] = -0.10
        world.dynamic.add(SID)
        world.call('refresh_programmes')
        expected = min(0, -0.15 + sum(0.05 for done in earned[:3] if done) + (0.15 if earned[3] else 0))
        check(math.isclose(world.num(SID+'_research_speed_factor'), expected, abs_tol=1e-9), ('Wrong research relief', earned))
        check((SID in world.dynamic) == (expected < -1e-9), ('Scarcity removal mismatch', earned))
        check(active_total(world, 'total_workforce_modifier') >= 0.10-1e-9, ('Old workforce penalty remains active', earned))
        before = deepcopy(world.variables)
        world.call('refresh_programmes')
        check(world.variables == before, ('Repeated refresh compounded values', earned))

    for focus in ['national_training', 'foreign_specialists', 'technical_institutes']:
        for receipts in [set(), {'technical_cadres'}, {'technical_cadres', 'national_training'}, {'technical_institutes'}]:
            # Compare a still-unearned focus, as in normal prospective hovers.
            receipts = receipts - {focus}
            before = Preview()
            before.flags = {P+'done_'+key: None for key in receipts}
            before.call('refresh_programmes')
            after = deepcopy(before)
            after.flags[P+'done_'+focus] = None
            after.call('refresh_programmes')
            preview = deepcopy(before)
            preview.lines = []
            preview.execute(first(first(focuses[P+focus], 'completion_reward'), 'effect_tooltip'))
            shown_research = sum(v for k, v in preview.lines if k == 'research_speed_factor_tt')
            actual_research = active_total(after, 'research_speed_factor') - active_total(before, 'research_speed_factor')
            check(math.isclose(shown_research, actual_research, abs_tol=1e-9), ('Loaded focus hover differs from executed research', focus, receipts, shown_research, actual_research))
            if focus == 'foreign_specialists':
                check(not any(k == 'total_workforce_modifier_tt' and v < 0 for k, v in preview.lines), 'Specialist preview shows a workforce loss')

    for focus, government, programme in [
        ('citizen_ballot', 'western_liberals_are_in_power', 'constitutional'),
        ('citizen_dividend', 'emerging_communist_state_are_in_power', 'left'),
    ]:
        world = World()
        world.governments = {government}
        world.flags[P+'done_'+focus] = None
        world.call('refresh_programmes')
        check(math.isclose(world.num(P+programme+'_research_speed_factor'), -0.03, abs_tol=1e-9), ('Research trade-off missing', focus))
        check(active_total(world, 'total_workforce_modifier') >= 0.10-1e-9, ('Policy still reduces workforce', focus))

    approval = json.loads((ROOT / 'tools/uae_1970/approval.json').read_text(encoding='utf-8'))
    check(hashlib.sha256((ROOT / 'tools/uae_1970/approved_design.json').read_bytes()).hexdigest() == approval['sha256'], 'Immutable approval changed')
    report = {'project': 'IMPERIA COLD WAR', 'passed': True, 'checks': checks,
              'receipt_combinations': 16, 'loaded_preview_contexts': 12,
              'limits': 'Installed AST and bounded model only; native tooltip, economy refresh and multiplayer not observed.'}
    output = ROOT / 'docs/audits/workforce_research_revision_20261025/specialists_validation.json'
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    run()
