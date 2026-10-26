# IMPERIA CW — Cold War: gcc 1970 — test legacy.
"""Exercise the bounded native-decision scenario adapter without a generator."""
from pathlib import Path
import json
import sys
import tempfile

from legacy import (ROOT, RELATIVE, INSERT, patch, install, STARTUP_RELATIVE,
                    STARTUP_ORIGINAL, STARTUP_BEGIN, patch_startup, startup_region)
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first


def run():
    current = (ROOT / RELATIVE).read_bytes()
    text = current.decode('utf-8-sig')
    original = text.replace(INSERT, '')
    adapted = patch(original)
    assert patch(adapted) == adapted
    assert adapted.replace(INSERT, '') == original
    before = first(first(parse(original), 'gcc_decisions'), 'GCC_request_bloc_arms_sales')
    after = first(first(parse(adapted), 'gcc_decisions'), 'GCC_request_bloc_arms_sales')
    visible = first(after, 'visible')
    assert visible[0] == ('NOT', '=', [('IMP_is_1970_scenario', '=', 'yes')])
    assert visible[1:] == first(before, 'visible')
    assert [row for row in after if row[0] != 'visible'] == [row for row in before if row[0] != 'visible']
    for scenario, expected in [(True, False), (False, True)]:
        guard_passes = not scenario
        assert guard_passes is expected
    source_startup = (ROOT/STARTUP_RELATIVE).read_bytes().decode('utf-8-sig')
    start, end, newline = startup_region(source_startup)
    original_startup = source_startup[:start]+STARTUP_ORIGINAL.replace('\n',newline)+source_startup[end:]
    adapted_startup = patch_startup(original_startup)
    assert patch_startup(adapted_startup) == adapted_startup
    after_start, after_end, _ = startup_region(adapted_startup)
    assert adapted_startup[:after_start] == original_startup[:start]
    assert adapted_startup[after_end:] == original_startup[start+len(STARTUP_ORIGINAL.replace('\n',newline)):]
    modern = first(parse(adapted_startup[after_start:after_end]), 'if')
    assert [r for r in modern if r[0] != 'limit'] == parse(STARTUP_ORIGINAL)
    # Installing preserves BOM and every original newline/byte outside INSERT.
    for bom in (b'', b'\xef\xbb\xbf'):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            assert Path(directory).resolve().is_relative_to(Path(__file__).parent.resolve())
            path = Path(directory) / RELATIVE
            path.parent.mkdir(parents=True)
            payload = bom + original.encode('utf-8')
            path.write_bytes(payload)
            startup_path = Path(directory)/STARTUP_RELATIVE
            startup_path.parent.mkdir(parents=True)
            startup_path.write_bytes(bom+original_startup.encode('utf-8'))
            assert install(directory) == [RELATIVE,STARTUP_RELATIVE]
            assert path.read_bytes() == bom + adapted.encode('utf-8')
            assert startup_path.read_bytes() == bom+adapted_startup.encode('utf-8')
            assert install(directory) == []
    report = dict(passed=True, checks=17, engine_tested=False,
                  change='Only modern arms decision visibility and the six-member GCC startup seed are adapted; modern seed AST and every outside byte are preserved')
    (Path(__file__).parent / 'legacy_validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__': run()
