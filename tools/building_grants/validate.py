# IMPERIA COLD WAR — Scoped building-grant provider and integration verification.
"""Read-only validation with one compact diagnostic report, without generation."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from building_grants import grants as G
from building_grants.remaining import repair_syria_output, SYR_PATHS
from focus_prerequisite_ui import nodes


def main():
    errors = []
    records = []
    expected = G.runtime_outputs()
    definitions = set()
    references = set()
    tooltips = set()
    localisation = set(re.findall(r'^\s+(\w+):\d*\s', expected[
        'localisation/english/COLDWAR_GRANT_capacity_l_english.yml'], re.M))
    for relative, text in expected.items():
        path = G.ROOT/relative
        payload = text.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
        actual = path.read_bytes()
        if actual != payload:
            errors.append('Canonical provider differs: '+relative)
        if not relative.endswith('.yml'):
            definitions.update(n.key for n in nodes(text) if n.key.startswith(G.PREFIX))
        records.append(dict(path=relative, sha256=hashlib.sha256(actual).hexdigest()))

    for directory in ('common/national_focus', 'common/scripted_effects',
                      'common/scripted_triggers', 'common/decisions',
                      'common/on_actions', 'events'):
        for path in (G.ROOT/directory).glob('*.txt'):
            payload = path.read_bytes()
            text = payload.decode('utf-8-sig')
            if G.PREFIX not in text:
                continue
            relative = path.relative_to(G.ROOT).as_posix()
            if payload.startswith(b'\xef\xbb\xbf'):
                errors.append('Script BOM: '+relative)
            if not text.startswith('# IMPERIA COLD WAR —'):
                errors.append('Missing file-start project marker: '+relative)
            try:
                nodes(text)
            except Exception as exc:
                errors.append('Script structure: '+relative+': '+str(exc))
            references.update(re.findall(r'\b(COLDWAR_GRANT_\w+)\s*=\s*yes\b', text))
            tooltips.update(re.findall(r'\btooltip\s*=\s*(COLDWAR_GRANT_\w+)', text))

    errors.extend('Missing provider: '+key for key in sorted(references-definitions))
    errors.extend('Missing English tooltip: '+key for key in sorted(tooltips-localisation))
    for tag, spec in G.scope().items():
        text = (G.ROOT/spec['tree']).read_text(encoding='utf-8-sig')
        if G.repair_focus_tree(tag, text) != text:
            errors.append('National adapter is not retained: '+tag)
    for relative in sorted(SYR_PATHS):
        text = (G.ROOT/relative).read_text(encoding='utf-8-sig')
        if repair_syria_output(relative, text) != text:
            errors.append('Syrian adapter is not retained: '+relative)
    from building_grants.apply_reviewed_queue import outputs as reviewed_awards
    before, prospective = reviewed_awards()
    for relative, text in prospective.items():
        if before.get(relative) != text:
            errors.append('Reviewed completion award is not retained: '+relative)
    if (G.ROOT/'common/technologies/COLDWAR_QUEUE_construction.txt').exists():
        errors.append('Rejected construction-permission prototype is installed')
    inventory=json.loads((G.ROOT/'docs/design/building_capacity_audit_20261027/INVENTORY.json').read_text(encoding='utf-8'))
    upstream={path:sha for path,sha in inventory['source_hashes'].items()
              if path.startswith('common/technologies/') or path in
              ('common/scripted_effects/00_scripted_effects.txt','common/scripted_triggers/00_scripted_triggers.txt')}
    for relative, expected_hash in upstream.items():
        if hashlib.sha256((G.ROOT/relative).read_bytes()).hexdigest()!=expected_hash:
            errors.append('Audited upstream provider changed: '+relative)
    for name in ('grants.py', 'remaining.py', 'native_queue_probe.py', 'validate.py',
                 'apply_reviewed_queue.py', 'queue_permissions.py', 'test_reviewed_queue.py'):
        path = Path(__file__).resolve().parent/name
        text = path.read_text(encoding='utf-8')
        ast.parse(text, filename=str(path))
        if not text.startswith('# IMPERIA COLD WAR —'):
            errors.append('Missing tool marker: '+name)

    result = dict(project='IMPERIA COLD WAR', passed=not errors,
                  native_engine_test=False, multiplayer_test=False,
                  providers=records, resolved_references=len(references),
                  resolved_tooltips=len(tooltips), unchanged_upstream_providers=len(upstream),
                  reviewed_completion_awards=5, errors=errors,
                  scope='Current scoped providers, source structure, encoding, English tooltip closure and retained canonical adapters. No country build or game launch.')
    target = G.ROOT/'docs/design/building_capacity_audit_20261027/PROVIDER_VERIFICATION.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
