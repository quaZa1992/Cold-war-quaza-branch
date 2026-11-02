# IMPERIA COLD WAR — Canonical USA Gulf subtree integration.
"""Use the owning Gulf generator without running the full Iraqi compiler.

The immutable approval/source snapshots are retained. Only the existing fifteen
Gulf focus IDs are replaced; all other focus blocks keep their current content.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import nodes, field

PREFIX = 'COLDWAR_USA_gulf_'


@lru_cache(maxsize=1)
def outputs():
    folder = ROOT / 'tools/iraq_1970'
    if str(folder) not in sys.path:
        sys.path.append(str(folder))
    spec = importlib.util.spec_from_file_location('usa_owned_gulf_source', folder / 'usa_module.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate(ROOT)


def emit(write, pretty):
    changed = []
    for path, text in outputs().items():
        # The unchanged autonomy definition remains owned by the Iraqi compiler.
        if path.startswith('common/autonomous_states/'):
            continue
        if path.endswith('.txt'):
            text = pretty(text)
        if write(path, text.lstrip('\ufeff'), path.endswith('.yml')):
            changed.append(path)
    return changed


def patch_tree(text):
    tree = next(n for n in nodes(text) if n.key == 'focus_tree')
    current = {field(n.children(), 'id'): n for n in tree.children()
               if n.key == 'focus' and str(field(n.children(), 'id')).startswith(PREFIX)}
    source = outputs()['tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt']
    desired = {field(n.children(), 'id'): n for n in nodes(source) if n.key == 'focus'}
    assert len(current) == 15 and current.keys() == desired.keys(), 'Preserve all existing Gulf focus IDs'
    anchor = PREFIX + 'desert_storm'
    dx = int(field(current[anchor].children(), 'x')) - int(field(desired[anchor].children(), 'x'))
    dy = int(field(current[anchor].children(), 'y')) - int(field(desired[anchor].children(), 'y'))
    edits = []
    for key, new in desired.items():
        raw = source[new.start:new.end]
        for axis, offset in (('x', dx), ('y', dy)):
            old = field(new.children(), axis)
            raw, count = re.subn(r'(?m)^(\s*' + axis + r'\s*=\s*)-?\d+\s*$',
                                lambda m: m[1] + str(int(old) + offset), raw, count=1)
            assert count == 1, (key, axis)
        edits.append((current[key].start, current[key].end, raw))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text
