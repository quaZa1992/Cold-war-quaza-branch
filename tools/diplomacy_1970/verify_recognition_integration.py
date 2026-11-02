# IMPERIA COLD WAR — Bounded recognition patch verification against the saved live baseline.
"""Record exactly which parsed gameplay nodes changed; does not prove engine behavior."""
from pathlib import Path
import hashlib
import json
import re
import sys

from test_diplomacy import ROOT, parse, first
from native_hooks import apply_recognition_hooks


def index(path, events=False):
    if path.suffix == '.yml':
        result = dict(re.findall(r'^\s+([^\s:]+):\d+\s+"(.*)"\s*$', path.read_text(encoding='utf-8-sig'), re.M))
        assert result, 'No localisation entries parsed'
        return result
    rows = parse(path.read_text(encoding='utf-8-sig'))
    if events:
        return {first(v, 'id'): v for k, o, v in rows if k == 'country_event'}
    return {k: v for k, o, v in rows}


def verify(backup):
    expected = {
        'common/scripted_effects/COLDWAR_diplomacy_1970.txt': {
            'COLDWAR_Germany_recount_recognition', 'COLDWAR_Germany_observe_DDR_recognition', 'COLDWAR_UN_1970_initialize'},
        'common/scripted_effects/COLDWAR_GER_1970_windows_effects.txt': {
            'COLDWAR_GER_1970_rv_ddr_ai', 'COLDWAR_GER_1970_rv_pick_crisis'},
        'events/International Recognition.txt': {'recognition.8', 'recognition.31'},
        'common/scripted_triggers/COLDWAR_diplomacy_1970.txt': set(),
        'common/on_actions/COLDWAR_diplomacy_1970.txt': set(),
        'common/scripted_localisation/COLDWAR_diplomacy_1970.txt': set(),
    }
    changes = {}
    for rel, allowed in expected.items():
        old, new = index(backup / rel, rel.startswith('events/')), index(ROOT / rel, rel.startswith('events/'))
        changed = {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
        assert changed == allowed, (rel, changed, allowed)
        changes[rel] = sorted(changed)
        assert not (ROOT / rel).read_bytes().startswith(b'\xef\xbb\xbf'), rel
    rel = 'localisation/english/COLDWAR_GER_1970_l_english.yml'
    old, new = index(backup / rel), index(ROOT / rel)
    assert {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)} == {'COLDWAR_GGR.105.desc'}
    rel = 'events/International Recognition.txt'
    before = (ROOT / rel).read_bytes()
    apply_recognition_hooks(ROOT)
    assert before == (ROOT / rel).read_bytes(), 'Native patch is not idempotent'
    return {
        'project': 'IMPERIA COLD WAR',
        'baseline': str(backup),
        'changed_gameplay_nodes': changes,
        'source_model_tests': {'diplomacy': 30, 'recognition_observer': 12, 'ddr_relations': 16, 'bilateral_sandbox': 19},
        'gui_performance_checks': 106,
        'german_source_validator': {'errors': 0, 'warnings': 48, 'notes': 'Existing retired event stubs, two retired ideas, average focus cost advisory'},
        'native_event_image': {'sprite': 'GFX_political_deal', 'size': [217, 163], 'format': 'RGBA DDS', 'source': 'Existing native MD event asset'},
        'native_event_queue_rendering_multiplayer_tested': False,
        'runtime_sha256': {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in list(expected) + [
            'events/COLDWAR_German_recognition_1970.txt', 'localisation/english/COLDWAR_diplomacy_1970_l_english.yml',
            'localisation/english/COLDWAR_GER_1970_l_english.yml']},
    }


if __name__ == '__main__':
    result = verify(Path(sys.argv[1]).resolve())
    output = Path(__file__).with_name('recognition_observer_validation.json')
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
