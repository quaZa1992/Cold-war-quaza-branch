# IMPERIA CW — Cold War: Japan script grammar and focus nesting checks.
"""Check Clausewitz token/assignment shapes, including the rejected >= syntax.

This is a bounded syntax check, not the HOI4 parser. The comparison regression
comes from error.log at COLDWAR_JAP_1970_focus.txt:433, 27 October 2026.
"""
from dataclasses import dataclass
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEXER = re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|[{}=<>]|[^\s{}=<>#"]+')

@dataclass
class Entry:
    key: str
    operator: str | None
    value: str | list['Entry'] | None
    line: int

def parse(text):
    tokens = []
    cursor = 0
    for match in LEXER.finditer(text):
        if match.start() != cursor:
            raise ValueError(f'Unrecognized text at line {text.count(chr(10), 0, cursor) + 1}')
        cursor = match.end()
        word = match.group()
        if not word.isspace() and not word.startswith('#'):
            tokens.append((word, text.count('\n', 0, match.start()) + 1))
    if cursor != len(text):
        raise ValueError('Unrecognized trailing text')
    index = 0
    def entries(nested=False):
        nonlocal index
        result = []
        while index < len(tokens):
            key, line = tokens[index]
            if key == '}':
                if not nested:
                    raise ValueError(f'Unexpected closing brace at line {line}')
                index += 1
                return result
            if key in ('{', '=', '<', '>'):
                raise ValueError(f'Expected key or list value at line {line}, found {key!r}')
            index += 1
            if index == len(tokens) or tokens[index][0] not in ('=', '<', '>'):
                result.append(Entry(key, None, None, line))
                continue
            operator = tokens[index][0]
            index += 1
            if index == len(tokens):
                raise ValueError(f'Missing assignment value at line {line}')
            value, value_line = tokens[index]
            if value == '{':
                index += 1
                value = entries(True)
            elif value in ('=', '<', '>', '}'):
                raise ValueError(f'Invalid comparison/assignment at line {value_line}: {key} {operator} {value}')
            else:
                index += 1
            result.append(Entry(key, operator, value, line))
        if nested:
            raise ValueError('Unclosed block')
        return result
    return entries()

def check_variable_blocks(entries, errors, path):
    for node in entries:
        if not isinstance(node.value, list):
            continue
        if node.key == 'check_variable':
            body = node.value
            if any(x.operator is None for x in body):
                errors.append(f'{path}:{node.line}: bare token in check_variable')
            explicit = {x.key: x.value for x in body}
            if 'compare' in explicit and explicit['compare'] not in {
                'less_than', 'less_than_or_equals', 'greater_than', 'greater_than_or_equals', 'equals', 'not_equals'
            }:
                errors.append(f'{path}:{node.line}: unsupported check_variable comparison')
        check_variable_blocks(node.value, errors, path)

def main():
    errors = []
    # A balanced-brace counter accepts this broken input; the grammar must reject it.
    try:
        parse('available = { check_variable = { support >= 67 } }')
    except ValueError:
        pass
    else:
        raise AssertionError('Comparison regression was not rejected')
    parse('available = { check_variable = { var = support value = 67 compare = greater_than_or_equals } }')
    files = list((ROOT / 'common').rglob('COLDWAR_JAP*.txt')) + list((ROOT / 'events').glob('COLDWAR_JAP*.txt'))
    files += [ROOT / 'history/countries/JAP - Japan.txt', ROOT / 'common/scripted_effects/mdcw_1970_focus_tree_effects.txt']
    for path in files:
        try:
            tree = parse(path.read_text(encoding='utf-8'))
            check_variable_blocks(tree, errors, path.relative_to(ROOT))
            if path.parent.name == 'events':
                for node in tree:
                    if node.key not in ('add_namespace', 'country_event', 'news_event'):
                        errors.append(f'{path.name}:{node.line}: unexpected top-level event statement {node.key}')
                    if node.key not in ('country_event','news_event') or not isinstance(node.value,list):
                        continue
                    fields={entry.key:entry.value for entry in node.value}
                    ident=fields.get('id','<missing id>')
                    options=[entry for entry in node.value if entry.key=='option']
                    if fields.get('hidden')!='yes' and not options:
                        errors.append(f'{path.name}:{node.line}: visible event {ident} has no direct option')
                    if (path.name in ('COLDWAR_JAP70_bilateral_events.txt','COLDWAR_JAP70_multilateral_invitation_events.txt')
                            and fields.get('hidden')!='yes' and len(options)!=2):
                        errors.append(f'{path.name}:{node.line}: recipient event {ident} needs two direct response options, found {len(options)}')
            if path.name == 'COLDWAR_JAP_1970_focus.txt':
                if len(tree) != 1 or tree[0].key != 'focus_tree' or not isinstance(tree[0].value, list):
                    raise ValueError('Expected one top-level focus_tree block')
                focuses = [n for n in tree[0].value if n.key == 'focus']
                if len(focuses) != 425:
                    raise ValueError(f'Expected 425 direct focus children, found {len(focuses)}')
                for focus in focuses:
                    if not isinstance(focus.value, list):
                        raise ValueError(f'Malformed focus block at line {focus.line}')
                    keys = [n.key for n in focus.value]
                    for required in ('id', 'available', 'completion_reward', 'ai_will_do'):
                        if keys.count(required) != 1:
                            raise ValueError(f'Focus at line {focus.line}: expected one direct {required}')
        except ValueError as error:
            errors.append(f'{path.relative_to(ROOT)}: {error}')
    print(f'Grammar checked {len(files)} installed scripts; {len(errors)} findings')
    for error in errors:
        print('ERROR:', error)
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
