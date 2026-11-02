# IMPERIA COLD WAR — Native trigger compatibility repair.
"""Correct trigger names confirmed by the installed 1.19 engine documentation."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
MARKER = '# IMPERIA COLD WAR — Native trigger compatibility integration.\n'
INVALID_STATS = re.compile(r'(?<![\w@.])(?P<stat>political_power|stability)(?=\s*[<>])')
COMPARE = re.compile(r'check_variable\s*=\s*(\{\{?)\s*([^\s{}]+)\s*(>=|<=|!=)\s*([^\s{}]+)\s*(\}\}?)')


def repair(source):
    # Native dynamic variables named stability/political_power remain valid in
    # check_variable. Do not turn these variable operands into trigger names.
    protected = [m.span() for m in re.finditer(r'check_variable\s*=\s*\{\{?[^{}]*\}\}?', source)]
    def stat(match):
        if any(start <= match.start() < end for start, end in protected):
            return match.group(0)
        line_start = source.rfind('\n', 0, match.start()) + 1
        if '#' in source[line_start:match.start()]:
            return match.group(0)
        return 'has_' + match['stat']
    source = INVALID_STATS.sub(stat, source)
    def explicit(match):
        opening, variable, operator, value, closing = match.groups()
        comparison = {'>=': 'greater_than_or_equals', '<=': 'less_than_or_equals', '!=': 'not_equals'}[operator]
        return f'check_variable = {opening} var = {variable} value = {value} compare = {comparison} {closing}'
    return COMPARE.sub(explicit, source)


def main():
    apply = '--apply' in sys.argv
    paths = [p for directory in ['common', 'events'] for p in (ROOT / directory).rglob('*.txt')]
    excluded = {'archive_v4', 'proposal_v5', 'audit_snapshots', 'before', '.vendor', '__pycache__',
                'draft', 'foreign_concept', 'skill_updates'}
    for directory in ['tools', 'Claude outputs']:
        for path in (ROOT / directory).rglob('*.py'):
            parts = path.relative_to(ROOT).parts
            if any(part in excluded or part.startswith('runtime') or part.endswith('_concept') for part in parts):
                continue
            if path.name.startswith(('test_', 'qa_')) or 'multiplayer_quality' in parts:
                continue
            paths.append(path)
    changes = []
    for path in paths:
        source = path.read_text(encoding='utf-8-sig')
        revised = repair(source)
        if revised == source:
            continue
        if not revised.startswith('# IMPERIA COLD WAR —'):
            revised = MARKER + revised
        changes.append(path.relative_to(ROOT).as_posix())
        if apply:
            path.write_text(revised, encoding='utf-8', newline='\n')
    report = {'project': 'IMPERIA COLD WAR', 'applied': apply, 'files': changes}
    if apply:
        out = ROOT / 'docs/audits/multiplayer_quality_20261023/native_syntax_repairs.json'
        out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
