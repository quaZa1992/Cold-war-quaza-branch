# IMPERIA COLD WAR — Repair historical leader wrapper delimiters.
"""Restore only closing braces swallowed by the historical pool END comment."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse

MARKER = '# IMPERIA COLD WAR — Historical national leader selection integration.\n'
PATTERN = re.compile(r'(?m)^(# MDCW HISTORICAL NATIVE POOL END [A-Z0-9]{3})(\})([ \t]*)$')


def main():
    repairs = []
    for path in sorted((ROOT / 'common/scripted_effects').glob('*_political_leaders.txt')):
        text = path.read_text(encoding='utf-8-sig')
        repaired, count = PATTERN.subn(r'\1\n\2\3', text)
        if not count:
            continue
        # No generated branch, appointment, fallback, or existing closing brace changes.
        assert count == 1, path
        parse(repaired)
        repaired = MARKER + repaired
        repaired = re.sub(r'(?m)^(# MDCW HISTORICAL NATIVE POOL [A-Z0-9]{3} BEGIN)$',
                          r'\1\n# IMPERIA COLD WAR — Historical national leader selection.', repaired)
        path.write_text(repaired, encoding='utf-8', newline='\n')
        repairs.append(path.relative_to(ROOT).as_posix())
    report = {'project': 'IMPERIA COLD WAR', 'repaired_count': len(repairs), 'files': repairs}
    out = ROOT / 'docs/audits/multiplayer_quality_20261023/leader_delimiter_repairs.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Repaired and parsed', len(repairs), 'leader setters', flush=True)


if __name__ == '__main__':
    main()
