# IMPERIA CW — Cold War: independently read the emitted Japan focus presentation.
"""Resolve the actual script, including relative anchors, for audits and images."""
from functools import lru_cache
from check_script_grammar import parse


def field(entries, key, default=None):
    return next((e.value for e in entries if e.key == key), default)


def read_focuses(text):
    tree = parse(text)
    if len(tree) != 1 or tree[0].key != 'focus_tree':
        raise ValueError('Expected one focus_tree')
    result = {}
    for item in tree[0].value:
        if item.key != 'focus':
            continue
        body = item.value
        ident = field(body, 'id')
        if ident in result:
            raise ValueError('Duplicate focus ' + ident)
        result[ident] = {
            'id': ident, 'icon': field(body, 'icon'),
            'x': int(field(body, 'x')), 'y': int(field(body, 'y')),
            'anchor': field(body, 'relative_position_id'),
            'parents': [[e.value for e in n.value if e.key == 'focus'] for n in body if n.key == 'prerequisite'],
            'exclusive': field(body, 'mutually_exclusive', []), 'entries': body,
        }
        result[ident]['exclusive'] = [e.value for e in result[ident]['exclusive'] if e.key == 'focus']

    visiting = set()
    @lru_cache(None)
    def resolve(ident):
        if ident not in result or ident in visiting:
            raise ValueError('Missing or cyclic anchor ' + ident)
        visiting.add(ident)
        node = result[ident]
        ax, ay = resolve(node['anchor']) if node['anchor'] else (0, 0)
        visiting.remove(ident)
        return ax + node['x'], ay + node['y']
    for ident, node in result.items():
        node['globalX'], node['globalY'] = resolve(ident)
    return result


def semantic(entries, omit=()):
    return [(e.key, e.operator, semantic(e.value) if isinstance(e.value, list) else e.value)
            for e in entries if e.key not in omit]
