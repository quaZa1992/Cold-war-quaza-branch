# IMPERIA COLD WAR — Read-only parity check for retained Soviet annual-order adapters.
"""Import the content donor, never cw_build or its broad filesystem writer."""
import ast
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DONOR = ROOT / 'Claude outputs/COLDWAR_SOV_generator'
sys.path[:0] = [str(DONOR), str(ROOT / 'tools/vietnam_1970')]
from script_ast import parse


def flatten(rows):
    result = []
    for key, operator, value in rows:
        if isinstance(value, list):
            value = flatten(value)
        if key == 'hidden_effect':
            result.extend(value)
        else:
            result.append((key, operator, value))
    return result


def main():
    donor = importlib.import_module('cw_union')
    # Extract only the variable-tooltip filter. Importing cw_build would invoke
    # its unrelated output-directory setup and is intentionally prohibited here.
    source = ast.parse((DONOR / 'cw_build.py').read_text(encoding='utf-8'))
    nodes = [node for node in source.body if
             isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'VAR_OP' for t in node.targets)
             or isinstance(node, ast.FunctionDef) and node.name == 'hide_var_ops']
    assert len(nodes) == 2
    namespace = {'re': re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<retained-tooltip-filter>', 'exec'), namespace)
    checks = {}
    for relative in (
        'common/national_focus/COLDWAR_UNI_1970_union_joint.txt',
        'common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt',
        'events/COLDWAR_UNI_1970_events.txt',
        'common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt',
        'common/decisions/categories/COLDWAR_UNI_1970_decision_categories.txt',
    ):
        generated = namespace['hide_var_ops'](donor.FILES[relative])
        actual = (ROOT / relative).read_bytes()
        checks[relative] = {
            'runtime_semantics_match': flatten(parse(generated)) == flatten(parse(actual.decode('utf-8'))),
            'source_sha256': hashlib.sha256(actual).hexdigest(),
        }
    report = {
        'project': 'IMPERIA COLD WAR', 'checks': checks,
        'scope': 'Read-only retained donor import and its variable-tooltip filter. Hidden bookkeeping wrappers flattened for semantic comparison. No broad Soviet generator executed.',
    }
    report['success'] = all(row['runtime_semantics_match'] for row in checks.values())
    (HERE / 'GENERATOR_PARITY.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    return not report['success']


if __name__ == '__main__':
    raise SystemExit(main())
