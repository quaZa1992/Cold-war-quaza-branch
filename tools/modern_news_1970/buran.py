# IMPERIA CW — Cold War: modern news 1970 — buran.
"""Bounded adapter for MD's post-Soviet Buran preservation storyline.

Run this installer after refreshing the two native MD files. It deliberately
does not alter the separate Cold War Soviet space programme or political news.
"""
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parents[2]
EVENT_IDS = ('russia.200', 'russia.300', 'russia.301', 'russia.302',
             'russia.3022', 'russia.303', 'russia.3033', 'russia.304', 'russia.3044')
DECISIONS = ('SOV_buran_hangar', 'SOV_begin_funding', 'SOV_dissassemble_the_shuttle',
             'SOV_build_hangar', 'SOV_make_repairs_at_temp_hangar', 'SOV_announce_full_restoration')
GUARD = 'NOT = { IMP_is_1970_scenario = yes }'
MARKER = '# COLDWAR | Post-Soviet Buran preservation is unavailable in the 1970 campaign.'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]')


def end_brace(text, opening):
    depth = 1
    for token in TOKEN.finditer(text, opening + 1):
        if token[0] == '{': depth += 1
        elif token[0] == '}':
            depth -= 1
            if not depth: return token.start()
    raise ValueError('Unclosed script block')


def blocks(text, key):
    """Top-level child block spans, excluding strings and comments."""
    depth = 0
    out = []
    cursor = 0
    for token in TOKEN.finditer(text):
        if token[0] == '{':
            if depth == 0:
                match = re.search(r'\b' + re.escape(key) + r'\s*=\s*$', text[cursor:token.start()])
                if match: out.append((token.start(), end_brace(text, token.start())))
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0: cursor = token.end()
    return out


def add_condition(body, key, guard=GUARD):
    found = blocks(body, key)
    if not found:
        indent = re.search(r'(?m)^(\s*?)\S', body)[1].replace('\n', '')
        return body.rstrip() + '\n' + indent + key + ' = { ' + guard + ' }\n' + indent[:-1]
    assert len(found) == 1, key
    start, end = found[0]
    line = body[body.rfind('\n', 0, start)+1:start]
    indent = re.match(r'[\t ]*', line)[0] + '\t'
    return body[:start+1] + '\n' + indent + guard + body[start+1:]


def wrap_effects(body, key):
    for start, end in reversed(blocks(body, key)):
        line = body[body.rfind('\n', 0, start)+1:start]
        key_indent = re.match(r'[\t ]*', line)[0]
        indent = key_indent + '\t'
        old = body[start+1:end]
        if key == 'option':
            # These nine native events have only a name and effects in options.
            name = re.match(r'(\s*name\s*=\s*\S+)(.*)', old, re.S)
            assert name, key
            prefix, old = name.groups()
            prefix = '\n' + indent + prefix.strip()
            if not old.strip(): continue
        else: prefix = ''
        payload = textwrap.dedent(old).strip()
        payload = '\n'.join(indent + '\t' + line if line.strip() else '' for line in payload.splitlines())
        wrapped = prefix + '\n' + indent + 'if = {\n' + indent + '\tlimit = { ' + GUARD + ' }\n' + payload + '\n' + indent + '}\n' + key_indent
        body = body[:start+1] + wrapped + body[end:]
    return body


def patch_events(text):
    for start, end in sorted(blocks(text, 'country_event') + blocks(text, 'news_event'), reverse=True):
        body = text[start+1:end]
        ident = re.search(r'\bid\s*=\s*(\S+)', body)
        if not ident or ident[1] not in EVENT_IDS or MARKER in body: continue
        body = '\n\t' + MARKER + body
        body = add_condition(body, 'trigger')
        body = wrap_effects(body, 'option')
        text = text[:start+1] + body + text[end:]
    return text


def patch_decisions(text):
    # Decisions are one level below their category.
    for cat_start, cat_end in reversed(blocks(text, 'SOV_economy_category')):
        category = text[cat_start+1:cat_end]
        for name in DECISIONS:
            [(start, end)] = blocks(category, name)
            body = category[start+1:end]
            if MARKER in body: continue
            body = '\n\t\t' + MARKER + body
            for key in ('visible', 'available'):
                body = add_condition(body, key)
            if name == 'SOV_buran_hangar':
                body = add_condition(body, 'activation')
                body = add_condition(body, 'cancel_trigger', 'IMP_is_1970_scenario = yes')
            for key in ('complete_effect', 'remove_effect', 'timeout_effect'):
                body = wrap_effects(body, key)
            category = category[:start+1] + body + category[end:]
        text = text[:cat_start+1] + category + text[cat_end:]
    return text


def install(root=ROOT):
    changed = []
    for rel, patch in [('events/Russia.txt', patch_events), ('common/decisions/Russia.txt', patch_decisions)]:
        path = Path(root) / rel
        original = path.read_bytes()
        bom = b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b''
        text = original.decode('utf-8-sig')
        newline = '\r\n' if '\r\n' in text else '\n'
        result = patch(text.replace('\r\n', '\n')).replace('\n', newline)
        payload = bom + result.encode('utf-8')
        if payload != original:
            path.write_bytes(payload)
            changed.append(rel)
    return changed


if __name__ == '__main__':
    print(install())
