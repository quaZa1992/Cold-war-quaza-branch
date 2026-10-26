# IMPERIA CW — Cold War: modern news 1970 — test buran.
"""Source regression: old mission and queued outcomes cannot act in 1970."""
import json
from pathlib import Path
import subprocess
import sys
from buran import ROOT, EVENT_IDS, DECISIONS, install, patch_events, patch_decisions
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first

GATE = ('NOT', '=', [('IMP_is_1970_scenario', '=', 'yes')])


def modern_projection(rows):
    out = []
    for key, op, value in rows:
        if (key, op, value) == GATE: continue
        if key == 'cancel_trigger' and value == [('IMP_is_1970_scenario', '=', 'yes')]: continue
        if key == 'trigger' and value == [GATE]: continue
        if key == 'visible' and value == [GATE]: continue
        if key == 'if' and isinstance(value, list) and value[0] == ('limit', '=', [GATE]):
            out.extend(modern_projection(value[1:])); continue
        out.append((key, op, modern_projection(value) if isinstance(value, list) else value))
    return out


def run():
    checks = 0
    files = [('events/Russia.txt', patch_events), ('common/decisions/Russia.txt', patch_decisions)]
    for rel, patch in files:
        # Both native files were clean before this narrowly scoped adapter.
        old_text = subprocess.check_output(['git', 'show', 'HEAD:'+rel], cwd=ROOT).decode('utf-8-sig')
        text = (ROOT / rel).read_text(encoding='utf-8-sig')
        assert patch(text) == text
        assert modern_projection(parse(text)) == parse(old_text), rel
        checks += 2
    events = parse((ROOT/'events/Russia.txt').read_text(encoding='utf-8-sig'))
    for ident in EVENT_IDS:
        [event] = [value for key, _, value in events if key in ('country_event','news_event') and first(value,'id') == ident]
        assert first(event, 'trigger') == [GATE], ident
        for key, _, option in event:
            if key != 'option': continue
            effects = [row for row in option if row[0] != 'name']
            assert not effects or (len(effects) == 1 and effects[0][0] == 'if' and first(effects[0][2], 'limit') == [GATE]), ident
        checks += 2
    category = first(parse((ROOT/'common/decisions/Russia.txt').read_text(encoding='utf-8-sig')), 'SOV_economy_category')
    for name in DECISIONS:
        decision = first(category, name)
        assert first(decision,'visible')[0] == GATE
        assert first(decision,'available')[0] == GATE
        for key in ('remove_effect','complete_effect','timeout_effect'):
            effect = first(decision,key)
            if effect is not None:
                assert len(effect) == 1 and effect[0][0] == 'if'
                assert first(effect[0][2], 'limit') == [GATE]
                # A 1970 active legacy course/mission executes no original effects.
                assert effect[0][2][0] == ('limit','=',[GATE])
                checks += 1
        checks += 2
    mission = first(category, 'SOV_buran_hangar')
    assert first(mission,'activation')[0] == GATE
    assert first(mission,'cancel_trigger') == [('IMP_is_1970_scenario','=','yes')]
    assert first(mission,'cancel_effect') is None  # cancellation grants/charges nothing
    assert install() == []
    checks += 4
    report = dict(passed=True, checks=checks, events=len(EVENT_IDS), decisions=len(DECISIONS),
                  modern_ast_unchanged=True, engine_tested=False)
    (Path(__file__).parent/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__': run()
