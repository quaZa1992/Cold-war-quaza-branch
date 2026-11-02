# IMPERIA COLD WAR — Bounded installation of approved German multiplayer balance changes.
"""Render canon in memory; replace only nodes changed since the preserved source baseline."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import compile as generator
from compile_sandbox import entries, native_span
from compile_security import parse

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARK = '# IMPERIA COLD WAR — German multiplayer balance integration\n'
BASE = HERE / 'balance_audit/before_generated.json'
REPORT = HERE / 'balance_audit/integration.json'


def normalize(rows):
    """Accept earlier redundant hidden-effect wrapping, never meaningful runtime divergence."""
    out = []
    for k, o, v in rows:
        if k == 'hidden_effect':
            out.extend(normalize(v))
        else:
            out.append((k, o, normalize(v) if isinstance(v, list) else v))
    return out


def header(text, bom):
    if bom:
        lines = text.splitlines()
        if len(lines) < 2 or not lines[1].startswith('# IMPERIA COLD WAR'):
            text = text.replace('l_english:\n', 'l_english:\n' + MARK, 1)
    elif not text.startswith('# IMPERIA COLD WAR'):
        text = MARK + text
    return text


def plan():
    before = json.loads(BASE.read_text(encoding='utf-8'))['files']
    previous = json.loads(REPORT.read_text(encoding='utf-8')).get('installed_sha256', {}) if REPORT.exists() else {}
    captured = {}
    def capture(root, rel, text, bom=False):
        captured[rel] = dict(text=text, bom=bom)
        return rel
    generator.write = capture
    generator.build(str(ROOT), scripts_only=True)
    writes, changes, conflicts = {}, {}, []
    for rel, record in captured.items():
        new, bom = record['text'], record['bom']
        path = ROOT / rel
        installed = path.exists() and previous.get(rel) == hashlib.sha256(path.read_bytes()).hexdigest()
        if rel not in before:
            assert 'COLDWAR_GER_1970_balance_diplomacy' in rel, ('Unexpected new output', rel)
            if path.exists() and path.read_text(encoding='utf-8-sig') == header(new, bom):
                continue
            if path.exists() and not installed:
                conflicts.append([rel, 'Dedicated file changed outside this installation']); continue
            writes[rel] = (header(new, bom), bom)
            changes[rel] = ['new dedicated provider']
            continue
        old_source = before[rel]['text']
        if old_source == new:
            continue
        live = path.read_text(encoding='utf-8-sig')
        result, touched = live, []
        if bom:
            pattern = r'(?m)^ ([^:\s]+):\d*\s+(".*")$'
            a, b, current = (dict(re.findall(pattern, text)) for text in (old_source, new, live))
            for key in sorted(a.keys() | b.keys()):
                if a.get(key) == b.get(key) or current.get(key) == b.get(key):
                    continue
                if current.get(key) != a.get(key) and key in current and not installed:
                    conflicts.append([rel, key]); continue
                line = r'(?m)^ ' + re.escape(key) + r':\d*\s+".*"\n?'
                replacement = f' {key}:0 {b[key]}\n' if key in b else ''
                if key in current: result = re.sub(line, lambda _: replacement, result)
                else: result += replacement
                touched.append(key)
        else:
            a, b, current = (entries(text, rel) for text in (old_source, new, live))
            for key in sorted(a.keys() | b.keys()):
                pre, post, actual = a.get(key), b.get(key), current.get(key)
                if (pre or {}).get('node') == (post or {}).get('node'):
                    continue
                if (actual or {}).get('node') == (post or {}).get('node'):
                    continue
                if actual and normalize(actual['node']) != normalize((pre or {}).get('node', [])) and not installed:
                    conflicts.append([rel, list(key)]); continue
                replacement = MARK + native_span(new, post)[2] if post else ''
                if actual:
                    start, end, _ = native_span(result, actual)
                    result = result[:start] + replacement + result[end:]
                elif post:
                    if post['wrapper']:
                        from compile_security import spans
                        end = spans(result, post['wrapper'])[0][1] - 1
                        result = result[:end] + '\n' + replacement + '\n' + result[end:]
                    else: result += '\n' + replacement + '\n'
                touched.append(list(key))
            parse(result)
            if rel.endswith('COLDWAR_GER_1970_windows_effects.txt'):
                result = result.replace('a round is resolved every six months', 'a round is resolved every two months')
                result = result.replace('One round of a crisis (every six months)', 'One round of a crisis (every two months)')
        if result != live:
            writes[rel] = (header(result, bom), bom)
        if touched: changes[rel] = touched
    return writes, changes, conflicts


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument('--dry-run', action='store_true')
    args = cli.parse_args()
    writes, changes, conflicts = plan()
    report = dict(project='IMPERIA COLD WAR', dry_run=args.dry_run, conflicts=conflicts, changes=changes)
    if conflicts:
        print(json.dumps(report, indent=2)); raise SystemExit('Preserve divergent live nodes; inspect before installing.')
    if not args.dry_run:
        for rel, (text, bom) in writes.items():
            path = ROOT / rel; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8-sig' if bom else 'utf-8', newline='\n')
        report['installed_sha256'] = {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in writes}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    destination = REPORT.with_name('plan.json') if args.dry_run else REPORT
    if not args.dry_run:
        previous = json.loads(REPORT.read_text(encoding='utf-8')).get('installed_sha256', {}) if REPORT.exists() else {}
        report['installed_sha256'] = {**previous, **report['installed_sha256']}
    destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR', dry_run=args.dry_run, changed_files=len(changes), changed_nodes=sum(map(len, changes.values())), conflicts=conflicts), indent=2))


if __name__ == '__main__': main()
