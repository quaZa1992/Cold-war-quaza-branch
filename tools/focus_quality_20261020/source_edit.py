# IMPERIA CW — Cold War: focus quality 20261020 — source edit.
"""Small source-preserving helpers for the approved October focus quality pass."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def end_block(text, start):
    depth = 0
    quoted = comment = escaped = False
    for i in range(start, len(text)):
        c = text[i]
        if comment:
            if c == '\n':
                comment = False
            continue
        if quoted:
            if c == '"' and not escaped:
                quoted = False
            escaped = c == '\\' and not escaped
            continue
        if c == '#':
            comment = True
        elif c == '"':
            quoted = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError('Unclosed script block')


def focus_span(text, fid):
    for m in re.finditer(r'^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{', text, re.M):
        opening = text.index('{', m.start())
        end = end_block(text, opening)
        if re.search(r'\bid\s*=\s*' + re.escape(fid) + r'(?=\s|\})', text[opening:end]):
            return m.start(), end
    raise KeyError(fid)


def replace_reward(text, fid, reward):
    a, b = focus_span(text, fid)
    body = text[a:b]
    m = re.search(r'\bcompletion_reward\s*=\s*\{', body)
    opening = body.index('{', m.start())
    end = end_block(body, opening)
    replacement = 'completion_reward = {\n' + '\n'.join('\t\t\t' + x if x else '' for x in reward.splitlines()) + '\n\t\t}'
    return text[:a] + body[:m.start()] + replacement + body[end:] + text[b:]


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = 'utf-8-sig' if path.suffix == '.yml' else 'utf-8'
    payload = text.encode(encoding)
    if not path.exists() or path.read_bytes() != payload:
        path.write_bytes(payload)


def loc_update(text, entries):
    for key, value in entries.items():
        line = ' ' + key + ':0 "' + value.replace('"', "'").replace('\n', '\\n') + '"'
        pattern = r'^\s*' + re.escape(key) + r':\d*\s*".*"\s*$'
        if re.search(pattern, text, re.M):
            text = re.sub(pattern, lambda _: line, text, count=1, flags=re.M)
        else:
            text = text.rstrip() + '\n' + line + '\n'
    return text
