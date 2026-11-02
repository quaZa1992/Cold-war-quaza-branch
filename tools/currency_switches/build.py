# IMPERIA COLD WAR — Integrate uncapped reserve-currency realignment costs.
"""Only recorded insertions into existing laws and scripted conversion sites."""
from pathlib import Path
import hashlib
import json
import os
import re
import sys
from patch import parse, walk, reverse_edits

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = HERE / 'changes.json'
MARKER = '# IMPERIA COLD WAR — Reserve-currency realignment'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main(apply=False):
    previous = json.loads(MANIFEST.read_text(encoding='utf-8'))['files'] if MANIFEST.exists() else {}
    pending = {}

    def source(path):
        name = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        if name in previous:
            raw = reverse_edits(raw, previous[name])
        return raw, raw.decode('utf-8')

    def add(path, raw, inserts):
        if not inserts:
            return
        edits, offset, out = [], 0, raw
        for position, text in sorted(inserts, key=lambda item: item[0]):
            byte_position = len(raw.decode('utf-8')[:position].encode('utf-8'))
            edits.append({'offset_after': byte_position + offset, 'text': text})
            out = out[:byte_position + offset] + text.encode('utf-8') + out[byte_position + offset:]
            offset += len(text.encode('utf-8'))
        pending[path.relative_to(ROOT).as_posix()] = (out, {'before_sha256': sha(raw), 'after_sha256': sha(out), 'edits': edits})

    laws = {}
    for path in (ROOT / 'common/ideas').glob('*.txt'):
        raw, text = source(path)
        if not re.search(r'\breserve_currency\s*=\s*\{', text):
            continue
        nodes = parse(text)
        ideas = next(node for node in nodes if node.key == 'ideas')
        category = ideas.child('reserve_currency')
        inserts = []
        nl = '\r\n' if '\r\n' in text else '\n'
        for law in category.value:
            if not isinstance(law.value, list):
                continue
            laws[law.key] = path.relative_to(ROOT).as_posix()
            for hook, statement in [
                ('available', 'ICW_reserve_currency_affordable = yes'),
                ('modifier', 'custom_modifier_tooltip = ICW_reserve_currency_realignment_tt'),
                ('on_add', 'hidden_effect = { ICW_charge_reserve_realignment = yes }'),
            ]:
                block = law.child(hook)
                assert block is not None, (law.key, hook)
                if hook == 'on_add' and block.child('hidden_effect'):
                    block = block.child('hidden_effect')
                    statement = 'ICW_charge_reserve_realignment = yes'
                inserts.append((block.opening, hook_insertion(text, block, statement, hook)))
            if law.key == 'us_dollar':
                block = law.child('on_remove')
                block = block.child('hidden_effect') or block
                inserts.append((block.opening, hook_insertion(text, block, 'ICW_report_dollar_departure = yes', 'presidential departure report')))
        # The euro's native fallback is a conversion inside a law callback.
        inserts += scripted_insertions(text, nodes, set(laws), path)
        add(path, raw, inserts)

    assert len(laws) == 18, laws
    currency_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, laws)) + r')\b')
    for directory in ('common', 'events'):
        for path in (ROOT / directory).rglob('*.txt'):
            if 'ideas' in path.parts or path.name == 'ICW_reserve_currency_realignment.txt':
                continue
            raw, text = source(path)
            if not currency_pattern.search(text):
                continue
            try:
                nodes = parse(text)
            except ValueError:
                # Unrelated native data tables can use syntax outside this patcher's subset.
                assert not re.search(r'\b(?:add_ideas|remove_ideas|swap_ideas)\s*=.*(?:' + '|'.join(map(re.escape, laws)) + r')\b', text)
                continue
            add(path, raw, scripted_insertions(text, nodes, set(laws), path))

    records = {name: record for name, (out, record) in sorted(pending.items())}
    assert not set(previous) - set(records), 'A previously recorded insertion is missing'
    if apply:
        for name, (out, record) in pending.items():
            path = ROOT / name
            current = path.read_bytes()
            allowed = {record['before_sha256'], record['after_sha256']}
            if name in previous:
                allowed.add(previous[name]['after_sha256'])
            assert sha(current) in allowed, name
            if current != out:
                # Stage the complete UTF-8 payload before replacing a shared script.
                staged = path.with_name(path.name + '.ICW_reserve.tmp')
                staged.write_bytes(out)
                os.replace(staged, path)
        MANIFEST.write_text(json.dumps({'project': 'IMPERIA COLD WAR', 'files': records, 'laws': laws}, indent=2) + '\n', encoding='utf-8')
    up_to_date = all((ROOT / name).read_bytes() == out for name, (out, record) in pending.items())
    print(json.dumps({'project': 'IMPERIA COLD WAR', 'applied': apply, 'up_to_date': up_to_date, 'laws': len(laws), 'existing_files': len(records), 'insertions': sum(len(r['edits']) for r in records.values())}))


def hook_insertion(text, block, statement, purpose):
    nl = '\r\n' if '\r\n' in text else '\n'
    start = text.rfind('\n', 0, block.start) + 1
    indent = re.match(r'[\t ]*', text[start:]).group() + '\t'
    tail = '' if text[block.opening:].startswith(nl) else nl + indent
    return nl + indent + MARKER + ': ' + purpose + '.' + nl + indent + statement + tail


def scripted_insertions(text, nodes, laws, path):
    result, seen = [], set()
    nl = '\r\n' if '\r\n' in text else '\n'
    for node, parents in walk(nodes):
        if node.key not in ('add_ideas', 'remove_ideas', 'add_idea', 'remove_idea'):
            continue
        values = [node.value] if isinstance(node.value, str) else [n.value for n in node.value if n.key == '_bare']
        if not set(values) & laws:
            continue
        if any(n.key == 'effect_tooltip' for n in parents):
            continue
        operation = parents[-1] if parents and parents[-1].key == 'swap_ideas' else node
        if operation.start in seen:
            continue
        seen.add(operation.start)
        line_start = text.rfind('\n', 0, operation.start) + 1
        indent = re.match(r'[\t ]*', text[line_start:]).group()
        silent = any(n.key in ('currency_startup', 'mdcw_initialize_ddr_currency', 'on_startup_euu_action') for n in parents)
        gap_start = operation.start
        while gap_start > line_start and text[gap_start - 1] in ' \t':
            gap_start -= 1
        leading = '' if gap_start == line_start else nl
        before = leading + indent + MARKER + ': authored conversion. BEGIN' + nl + indent
        before += 'add_to_variable = { ICW_reserve_scripted_depth = 1 }' + nl + indent
        if silent:
            before += 'add_to_variable = { ICW_reserve_initializing_depth = 1 }' + nl + indent
        after = nl + indent
        if silent:
            after += 'subtract_from_variable = { ICW_reserve_initializing_depth = 1 }' + nl + indent
            after += 'if = { limit = { NOT = { check_variable = { ICW_reserve_initializing_depth > 0 } } } clear_variable = ICW_reserve_initializing_depth }' + nl + indent
        after += 'subtract_from_variable = { ICW_reserve_scripted_depth = 1 }' + nl + indent
        after += 'if = { limit = { NOT = { check_variable = { ICW_reserve_scripted_depth > 0 } } } clear_variable = ICW_reserve_scripted_depth }' + nl + indent
        after += MARKER + ': authored conversion. END' + nl + indent
        before = before.removesuffix(indent) if indent else before
        after = after.removesuffix(indent) if indent else after
        result += [(gap_start, before), (operation.end, after)]
    return result


if __name__ == '__main__':
    main('--apply' in sys.argv)
