# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | load the current generic focus file: header, sections, focus blocks (fields kept as raw text)."""
import re
from gen_common import read, block_end, F_FOCUS, P

SECTION_RE = re.compile(r'^\t### (.+?) ###[ \t]*$', re.M)


def parse_fields(block):
    """block = text of one 'focus = { ... }'. Returns [(key, raw)] in file order (raw = '{...}' or scalar)."""
    inner_start = block.index('{') + 1
    inner = block[inner_start:block.rindex('}')]
    out = []
    i = 0
    n = len(inner)
    key_re = re.compile(r'\s*([A-Za-z_][\w.@:^]*)\s*=\s*')
    while i < n:
        # skip whitespace and comments
        m = re.compile(r'(\s+|#[^\n]*)').match(inner, i)
        if m and m.end() > i:
            i = m.end()
            continue
        m = key_re.match(inner, i)
        if not m:
            raise ValueError('cannot parse focus field near: ' + inner[i:i + 60])
        key = m.group(1)
        j = m.end()
        if inner[j] == '{':
            e = block_end(inner, j)
            out.append((key, inner[j:e + 1]))
            i = e + 1
        else:
            m2 = re.compile(r'("[^"]*"|[^\s#}]+)').match(inner, j)
            out.append((key, m2.group(1)))
            i = m2.end()
    return out


def load_focus_file(mod_root):
    s, bom = read(f'{mod_root}/{F_FOCUS}')
    first = SECTION_RE.search(s)
    header = s[:first.start()]
    secs = list(SECTION_RE.finditer(s))
    sections = []
    for k, m in enumerate(secs):
        end = secs[k + 1].start() if k + 1 < len(secs) else s.rindex('}')
        text = s[m.end():end]
        foci = []
        j = 0
        while True:
            q = text.find('\tfocus = {', j)
            if q < 0:
                rest = text[j:]
                break
            pre = text[j:q]
            if pre.strip() and not all(l.strip().startswith('#') for l in pre.strip().split('\n')):
                raise ValueError(f'unexpected content in section {m.group(1)}: {pre.strip()[:80]}')
            e = block_end(text, q)
            raw = text[q:e + 1]
            fields = parse_fields(raw)
            fid = dict(fields)['id']
            foci.append(dict(id=fid, fields=fields, raw=raw))
            j = e + 1
        if rest.strip() and not all(l.strip().startswith('#') for l in rest.strip().split('\n')):
            raise ValueError(f'unexpected trailing content in section {m.group(1)}')
        sections.append((m.group(1), foci))
    tail = s[s.rindex('}'):]
    assert tail.strip() == '}', 'file must end with the closing brace of focus_tree'
    return dict(header=header, sections=sections, bom=bom, text=s)


def abs_positions(foci_by_id, extra=None):
    """absolute (x, y) of every focus; foci_by_id: id -> dict with x, y, rel"""
    cache = {}
    def ab(fid, depth=0):
        if fid in cache:
            return cache[fid]
        f = foci_by_id.get(fid) or (extra or {}).get(fid)
        if f is None:
            raise KeyError(fid)
        if depth > 50:
            raise ValueError('relative_position_id cycle at ' + fid)
        if f.get('rel'):
            px, py = ab(f['rel'], depth + 1)
            r = (px + f['x'], py + f['y'])
        else:
            r = (f['x'], f['y'])
        cache[fid] = r
        return r
    return {fid: ab(fid) for fid in foci_by_id}


def simple(fields):
    d = {}
    for k, v in fields:
        if k in ('prerequisite',):
            d.setdefault(k, []).append(v)
        else:
            d[k] = v
    return d


def shared_footprint(mod_root, path, base_offset=(0, 0)):
    """absolute cells of a shared/joint focus file attached to the generic tree"""
    s, _ = read(f'{mod_root}/{path}')
    F = {}
    for b in re.split(r'\n(?:shared_focus|joint_focus) = \{', s)[1:]:
        fid = re.search(r'\bid = (\S+)', b).group(1)
        x = int(re.search(r'\n\tx = (-?\d+)', b).group(1))
        y = int(re.search(r'\n\ty = (-?\d+)', b).group(1))
        rel = re.search(r'\n\trelative_position_id = (\S+)', b)
        F[fid] = dict(x=x, y=y, rel=rel.group(1) if rel else None)
    pos = abs_positions(F)
    return {k: (x + base_offset[0], y + base_offset[1]) if not F[k]['rel'] else
            (x + base_offset[0], y + base_offset[1]) for k, (x, y) in pos.items()}
