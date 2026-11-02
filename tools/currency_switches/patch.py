# IMPERIA COLD WAR — Bounded, reversible currency-law integration.
"""Locate script statements without reformatting unrelated source bytes."""
from dataclasses import dataclass
import re

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\r\n]*|>=|<=|!=|[{}=<>]|[^\s{}=<>!#"]+')


@dataclass
class Node:
    key: str
    value: object
    start: int
    end: int
    opening: int = 0
    closing: int = 0

    def child(self, key):
        return next((n for n in self.value if n.key == key), None)


def parse(text):
    tokens = [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(text) if not m.group().startswith('#')]
    index = 0

    def block(nested=False):
        nonlocal index
        result = []
        while index < len(tokens):
            key, start, end = tokens[index]
            index += 1
            if key == '}':
                if not nested:
                    raise ValueError('Unexpected closing brace')
                return result, start, end
            if index < len(tokens) and tokens[index][0] in ('=', '>', '<', '>=', '<=', '!='):
                index += 1
                value, _, end = tokens[index]
                index += 1
                if value == '{':
                    opening = end
                    children, closing, end = block(True)
                    result.append(Node(key, children, start, end, opening, closing))
                else:
                    result.append(Node(key, value, start, end))
            else:
                result.append(Node('_bare', key, start, end))
        if nested:
            raise ValueError('Unclosed script block')
        return result, len(text), len(text)

    return block()[0]


def walk(nodes, parents=()):
    for node in nodes:
        yield node, parents
        if isinstance(node.value, list):
            yield from walk(node.value, parents + (node,))


def reverse_edits(data, record):
    import hashlib
    assert hashlib.sha256(data).hexdigest() == record['after_sha256'], 'Currency-switch integration differs from recorded output'
    for edit in reversed(record['edits']):
        offset = edit['offset_after']
        added = edit['text'].encode('utf-8')
        assert data[offset:offset + len(added)] == added, 'Currency-switch insertion differs'
        data = data[:offset] + data[offset + len(added):]
    assert hashlib.sha256(data).hexdigest() == record['before_sha256'], 'Currency-switch preimage differs'
    return data
