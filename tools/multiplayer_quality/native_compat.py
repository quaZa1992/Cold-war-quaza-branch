# IMPERIA COLD WAR — Native decision and dynamic-modifier schemas.
"""Preserve source comments and move live decision gates out of static allowed."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import TOKEN, parse, walk
from multiplayer_quality.repair_native_syntax import repair as repair_triggers

MARKER = '# IMPERIA COLD WAR — Native decision and modifier cleanup integration.\n'


def startup_country_once(body, feature):
    """Dispatch a world setup once from an extant country on every startup.

    on_startup has no country scope. The transient global flag selects the
    first country without an RNG draw and is cleared before and after the loop.
    """
    assert re.fullmatch(r'[a-z_]+', feature)
    flag = 'ICW_startup_dispatch_' + feature
    return (f'clr_global_flag = {flag}\nevery_country = {{\n'
            f' limit = {{ NOT = {{ has_global_flag = {flag} }} }}\n'
            f' set_global_flag = {flag}\n' + body.strip() +
            f'\n}}\nclr_global_flag = {flag}\n')


def blocks(source):
    tokens = [m for m in TOKEN.finditer(source) if not m[0].startswith('#')]
    stack, result = [], []
    for index, token in enumerate(tokens):
        if token[0] == '{':
            key = tokens[index - 2][0] if index > 1 and tokens[index - 1][0] == '=' else None
            node = {'key': key, 'open': token.start(), 'parent': stack[-1] if stack else None}
            stack.append(node)
        elif token[0] == '}':
            if not stack:
                raise ValueError('Unexpected closing brace')
            node = stack.pop()
            node['end'] = token.end()
            result.append(node)
    if stack:
        raise ValueError('Unclosed script block')
    return result


def decision_gates(source):
    nodes = blocks(source)
    edits = []
    static_keys = {'always', 'tag', 'original_tag', 'is_dynamic_country', 'has_dlc', 'has_game_rule', 'AND', 'OR', 'NOT'}
    for node in nodes:
        if node['key'] != 'allowed' or node['parent'] is None:
            continue
        body = source[node['open'] + 1:node['end'] - 1]
        rows = parse(body)
        if all(key in static_keys for key, _, _ in walk(rows)):
            continue
        # Keep cheap static country routing in allowed; preserve the COMPLETE
        # old condition in visible, including OR/NOT nesting and script calls.
        static = [(k, op, v) for k, op, v in rows if k in {'original_tag', 'tag'} and isinstance(v, str)]
        retained = ' '.join(f'{k} {op} {v}' for k, op, v in static) or 'always = yes'
        edits.append((node['open'] + 1, node['end'] - 1, ' ' + retained + ' '))
        visible = next((n for n in nodes if n['key'] == 'visible' and n['parent'] is node['parent']), None)
        if visible:
            edits.append((visible['open'] + 1, visible['open'] + 1, '\n' + body.strip() + '\n'))
        else:
            edits.append((node['end'], node['end'], '\nvisible = {\n' + body.strip() + '\n}'))
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source


def modifier_removals(source):
    # remove_dynamic_modifier accepts a modifier block, not an idea-style scalar.
    return re.sub(r'\bremove_dynamic_modifier\s*=\s*([A-Za-z_]\w*)',
                  r'remove_dynamic_modifier = { modifier = \1 }', source)


def normalize(source, relative):
    original = source
    if relative.startswith(('common/', 'events/')) and relative.endswith('.txt'):
        source = repair_triggers(source)
    if relative.startswith('common/decisions/'):
        source = decision_gates(source)
    if relative.startswith(('common/', 'events/')) and relative.endswith('.txt'):
        source = modifier_removals(source)
    if source.startswith('# IMPERIA CW — Cold War:'):
        source = source.replace('# IMPERIA CW — Cold War:', '# IMPERIA COLD WAR —', 1)
    if relative.endswith('.yml') and source.startswith('l_english:'):
        source = source.replace('# IMPERIA CW — Cold War:', '# IMPERIA COLD WAR —', 1)
    if source != original and not source.startswith('# IMPERIA COLD WAR —'):
        source = MARKER + source
    return source


def main():
    decisions = ['COLDWAR_GRE_1970_tree_decisions', '00_political_decisions', 'COLDWAR_GCC_1970',
                 'COLDWAR_GRE_1970_regional_decisions', 'COLDWAR_NCY_1970_decisions',
                 'COLDWAR_SOV_1970_decisions', 'COLDWAR_SYR_foreign_decisions',
                 'COLDWAR_TUR_1970_regional_decisions', 'COLDWAR_UAE_1970_decisions', 'CYP_decisions']
    paths = [ROOT / 'common/decisions' / (name + '.txt') for name in decisions]
    paths += [ROOT / 'common/scripted_effects' / (name + '.txt')
              for name in ['ISR70_policy_effects', 'COLDWAR_GRE_1970_tree_effects']]
    changed = []
    for path in paths:
        source = path.read_text(encoding='utf-8-sig')
        revised = normalize(source, path.relative_to(ROOT).as_posix())
        if revised != source:
            if not revised.startswith('# IMPERIA COLD WAR —'):
                revised = MARKER + revised
            path.write_text(revised, encoding='utf-8', newline='\n')
            changed.append(path.relative_to(ROOT).as_posix())
    print('Repaired native schemas:', len(changed), 'files', flush=True)


if __name__ == '__main__':
    main()
