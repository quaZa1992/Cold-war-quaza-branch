# IMPERIA COLD WAR — Bind ideological defence to the current native consumer.
"""Repair the retired modifier alias without editing approved design records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = 'mdcw_cw_ideological_defence'
NEW = 'drift_defence_factor'
MARKER = '# IMPERIA COLD WAR — Native ideological defence integration.\n'


def main():
    paths = [p for p in (ROOT / 'common').rglob('*.txt')
             if OLD in p.read_text(encoding='utf-8-sig') and 'synchronized_dynamic_tokens' not in p.parts
             and p.name != 'ICW_native_compatibility.txt']
    paths += [ROOT / 'tools/west_germany_1970' / name for name in ['tree.py', 'ideas.py', 'systems.py']]
    paths.append(ROOT / 'Claude outputs/COLDWAR_DDR_generator/dg_misc.py')
    changed = []
    for path in paths:
        source = path.read_text(encoding='utf-8-sig')
        revised = source.replace(OLD, NEW)
        if revised == source:
            continue
        if not revised.startswith('# IMPERIA COLD WAR —'):
            revised = MARKER + revised
        path.write_text(revised, encoding='utf-8', newline='\n')
        changed.append(path.relative_to(ROOT).as_posix())
    out = ROOT / 'docs/audits/multiplayer_quality_20261023/modifier_alias_repairs.json'
    out.write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'files': changed,
                              'reader': 'mdcw_cw_apply_pps reads modifier@drift_defence_factor',
                              'approved_design_records_modified': False}, indent=2) + '\n', encoding='utf-8')
    print('Updated', len(changed), 'runtime and generator files', flush=True)


if __name__ == '__main__':
    main()
