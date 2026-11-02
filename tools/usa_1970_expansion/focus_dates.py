# IMPERIA COLD WAR — USA programme availability without arbitrary calendar locks.
"""Pure, bounded compiler hooks. Importing this module writes no files.

Historical election-result cards retain their real dated automatic bypasses.
Paid programmes instead use the actual ruling party and their policy chain.
Leader selection, scheduled events, agreement terms and timed flags are outside
this transformation. Immutable source/proposal snapshots are never modified.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Mapping

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from focus_prerequisite_ui import Node, field, nodes

YEARS = (1972, 1976, 1980, 1984, 1988, 1992, 1996)
ELECTION_RECEIPTS = frozenset(
    f'USA_1970_{year}_{party}_victory'
    for year in YEARS for party in ('democratic', 'republican')
)
READY_PREFIXES = ('COLDWAR_USA_legacy_ready_', 'COLDWAR_USA_dom_ready_')
TRIGGER_PATHS = frozenset({
    'common/scripted_triggers/COLDWAR_USA_1970_expansion.txt',
    'common/scripted_triggers/COLDWAR_USA_1970_programmes.txt',
})
TREE_PATH = 'common/national_focus/USA_1970.txt'
LOCALE_PATH = 'localisation/english/USA_1970_focus_l_english.yml'
ENGLISH_OVERRIDES = {
    'USA_1970_nixon_first_term_tt': 'Nixon is President.',
    'USA_1970_nixon_shortcut': 'Nixon Administration',
}


def walk(rows):
    for node in rows:
        yield node
        yield from walk(node.children())


def _shape(rows):
    return [(n.key, n.op, _shape(n.children()) if isinstance(n.value, list)
             else n.value) for n in rows]


def _render(node):
    if node.key == '_bare':
        return str(node.value)
    value = ('{ ' + ' '.join(_render(n) for n in node.children()) + ' }'
             if isinstance(node.value, list) else str(node.value))
    return node.key + ' ' + node.op + ' ' + value


def _apply_edits(text, edits):
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def party_gate(focus_id):
    """Use the native exact MD subparty triggers, never a broad outlook."""
    match = re.fullmatch(r'USA_1970_(?:1972|1976|1980|1984|1988|1992|1996)_(dem|rep)_.+', focus_id)
    if not match:
        match = re.fullmatch(r'USA_X_(dem|rep)(?:72|80)_.+', focus_id)
    if not match:
        return None
    return ('western_liberals_are_in_power' if match[1] == 'dem'
            else 'western_conservatism_are_in_power')


def strip_condition_dates(body, *, detach_election_receipts=False):
    """Remove date predicates while retaining every non-calendar predicate.

    This is pruning, not replacing a date with always=yes. In particular,
    OR={publication flag, date fallback} retains the actual publication flag.
    Empty grouping/tooltip wrappers are removed rather than leaving an empty
    OR/NOT that the engine could interpret differently. Negative receipt tests
    are deliberately not rewritten because they may express a real exclusion.
    """
    before = nodes(body)

    def prune(node, negated=False):
        if node.key == 'date':
            return None
        if (detach_election_receipts and node.key == 'has_completed_focus'
                and node.value in ELECTION_RECEIPTS and not negated):
            return None
        if not isinstance(node.value, list):
            return node
        children = [child for child in
                    (prune(n, negated or node.key == 'NOT') for n in node.children())
                    if child is not None]
        # Tooltip metadata must not keep a wrapper alive after its sole
        # gameplay condition has gone. Other grouping blocks have no metadata.
        predicates = [n for n in children if n.key != 'tooltip']
        if not predicates and node.children():
            return None
        return Node(node.key, node.op, children, node.start, node.end)

    after = [n for n in (prune(node) for node in before) if n is not None]
    if _shape(before) == _shape(after):
        return body
    return '\n'.join(_render(node) for node in after)


def patch_focus_tree(text):
    """Patch only paid-focus availability and election-receipt parent links.

    All 14 receipt cards, including their bypass windows and opposite-result
    tests, remain byte-identical. Every ordinary policy-to-policy AND/OR link,
    cost, coordinate, exclusion, completion effect and real state gate remains.
    """
    tree = next(n for n in nodes(text) if n.key == 'focus_tree')
    assert field(tree.children(), 'id') == 'USA_1970_focus'
    edits = []
    for focus in tree.children():
        if focus.key != 'focus':
            continue
        fid = field(focus.children(), 'id')
        if fid in ELECTION_RECEIPTS:
            continue
        if float(field(focus.children(), 'cost', 0)) == 0:
            # A future zero-cost automatic focus needs an explicit review.
            assert not any(n.key == 'date' for n in walk(focus.children())), fid
            continue
        available = next((n for n in focus.children() if n.key == 'available'), None)
        gate = party_gate(fid)
        detached = False
        for prerequisite in [n for n in focus.children() if n.key == 'prerequisite']:
            refs = [n.value for n in prerequisite.children() if n.key == 'focus']
            if not any(p in ELECTION_RECEIPTS for p in refs):
                continue
            # No current group mixes an election receipt and an ordinary
            # policy. Refuse to silently alter such a future OR dependency.
            assert refs and all(p in ELECTION_RECEIPTS for p in refs), (fid, refs)
            assert gate, ('Receipt-independent programme needs exact party', fid)
            edits.append((prerequisite.start, prerequisite.end, ''))
            detached = True
        if available:
            original = text[available.start:available.end]
            rewritten = strip_condition_dates(original)
            # A sole date becomes an unrestricted ordinary available block.
            if not rewritten:
                rewritten = 'available = { always = yes }'
            if detached and not any(n.key == gate for n in walk(nodes(rewritten))):
                wrapper = nodes(rewritten)[0]
                rewritten = rewritten[:wrapper.end - 1] + ' ' + gate + ' = yes }'
            if rewritten != original:
                edits.append((available.start, available.end, rewritten))
        elif detached:
            edits.append((focus.end - 1, focus.end - 1,
                          '\n\t\tavailable = { ' + gate + ' = yes }\n\t'))
    return _apply_edits(text, edits)


def patch_trigger_bodies(triggers: Mapping[str, str]):
    """Canonical legacy trigger dictionary hook before emission."""
    return {name: strip_condition_dates(body, detach_election_receipts=True)
            if name.startswith(READY_PREFIXES) else body
            for name, body in triggers.items()}


def patch_ready_triggers(text):
    """Patch real execution/retry predicates, not their tooltip alone."""
    edits = []
    for trigger in nodes(text):
        if not trigger.key.startswith(READY_PREFIXES):
            continue
        original = text[trigger.start:trigger.end]
        rewritten = strip_condition_dates(original, detach_election_receipts=True)
        if rewritten != original:
            edits.append((trigger.start, trigger.end, rewritten))
    return _apply_edits(text, edits)


def patch_english_localisation(text):
    """Return corrected requirement/shortcut wording; no names or Act dates."""
    for key, value in ENGLISH_OVERRIDES.items():
        pattern = r'(?m)^\s*' + re.escape(key) + r':\d*\s*".*"[\t ]*$'
        assert re.search(pattern, text), ('Missing date-text override', key)
        text = re.sub(pattern, lambda _: ' ' + key + ':0 ' + json.dumps(value), text, count=1)
    return text


def patch_outputs(outputs: Mapping[str, str]):
    """In-memory coordinator hook. The coordinator retains all write ownership."""
    result = dict(outputs)
    for path, text in outputs.items():
        normalized = str(path).replace('\\', '/')
        if normalized == TREE_PATH:
            result[path] = patch_focus_tree(text)
        elif normalized in TRIGGER_PATHS:
            result[path] = patch_ready_triggers(text)
        elif normalized == LOCALE_PATH:
            result[path] = patch_english_localisation(text)
    return result
