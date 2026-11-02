# IMPERIA COLD WAR — Bounded Iraqi and Cuban instant-gift capacity integration.
"""Keep country receipts, money and consent unchanged around physical queries.

Country compilers call the pure wrappers. The installer transforms only the
seven reviewed live files and never runs a broad country compiler or writes an
approval snapshot. Central query rewriting and English labels remain owned by
building_grants.grants.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
QUERY = re.compile(r'\bfree_building_slots\s*=\s*\{[^{}]*\}')
MARK = '# IMPERIA COLD WAR — Physical capacity for retained Iraqi and Cuban gift transactions.\n'
FILES = {
    'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt': frozenset(('infrastructure', 'fuel_silo')),
    'common/scripted_effects/COLDWAR_IRQ_1970_direct_rewards_v3.txt': frozenset(('infrastructure', 'fuel_silo')),
    'common/scripted_effects/COLDWAR_IRQ_1970_audit_migration.txt': frozenset(('infrastructure', 'fuel_silo')),
    'common/decisions/COLDWAR_IRQ_1970_pending.txt': frozenset(('infrastructure', 'fuel_silo')),
    'common/scripted_triggers/COLDWAR_CUB_1970_triggers.txt': frozenset(('fuel_silo',)),
    'common/scripted_effects/COLDWAR_CUB_1970_diplomacy.txt': frozenset(('radar_station',)),
    'common/decisions/COLDWAR_CUB_1970_diplomacy.txt': frozenset(('radar_station',)),
}
SLOT_FILES = tuple(p for p in FILES if 'COLDWAR_IRQ' in p) + ('common/national_focus/COLDWAR_IRQ_1970_focus.txt',)


def rewrite_selected(text: str, buildings: frozenset[str], transform=None, changes=None) -> str:
    """Replace only requested non-provincial queries, without reformatting text."""
    length_change = 0
    def replace(match):
        nonlocal length_change
        raw = match.group()
        kind = re.search(r'\bbuilding\s*=\s*(\w+)', raw)
        if not kind or kind[1] not in buildings or re.search(r'\bprovince\s*=', raw):
            return raw
        action = transform
        if action is None:
            # Late import keeps the adapter import side-effect-free and permits
            # source inspection without executing a central compiler.
            from building_grants.grants import rewrite_queries
            action = rewrite_queries
        replacement = action(raw)
        assert isinstance(replacement, str), 'Central query API must return text'
        assert replacement != raw, ('Central API did not replace reviewed query', raw)
        if changes is not None:
            changes.append({'building': kind[1], 'before': raw, 'after': replacement,
                            'line': text[:match.start()].count('\n') + 1,
                            'new_start': match.start() + length_change,
                            'new_end': match.start() + length_change + len(replacement)})
        length_change += len(replacement) - len(raw)
        return replacement
    return QUERY.sub(replace, text)


def irq_queries(text: str) -> str:
    return rewrite_selected(text, frozenset(('infrastructure', 'fuel_silo')))


def cub_silo_queries(text: str) -> str:
    return rewrite_selected(text, frozenset(('fuel_silo',)))


def cub_radar_queries(text: str) -> str:
    return rewrite_selected(text, frozenset(('radar_station',)))


def irq_slots(text: str, changes=None) -> str:
    """Mirror each delivered infrastructure/silo level in its own state scope.

    The final emitted level already is the outstanding remainder after credit.
    No migration hook or completed-country receipt is added or changed.
    """
    from focus_prerequisite_ui import nodes, field
    edits = []
    def visit(siblings, parent=None):
        for index, node in enumerate(siblings):
            if node.key == 'add_building_construction':
                kind = field(node.children(), 'type')
                instant = field(node.children(), 'instant_build')
                if kind in ('infrastructure', 'fuel_silo') and instant == 'yes':
                    quantity = int(field(node.children(), 'level'))
                    if quantity <= 0:
                        continue
                    assert parent is not None and parent.key.isdigit(), ('Unreviewed grant scope', parent, kind)
                    previous = siblings[index - 1] if index else None
                    if previous is not None and previous.key == 'add_extra_state_shared_building_slots':
                        assert int(previous.value) >= quantity, ('Insufficient existing paired slots', kind)
                        continue
                    line_start = text.rfind('\n', 0, node.start) + 1
                    indentation = text[line_start:node.start]
                    addition = f'add_extra_state_shared_building_slots = {quantity}'
                    addition += ' ' if indentation.strip() else '\n' + indentation
                    edits.append((node.start, addition, parent.key, kind, quantity))
            visit(node.children(), node)
    visit(nodes(text))
    for start, addition, state, kind, quantity in sorted(edits, reverse=True):
        if changes is not None:
            changes.append({'source_start': start, 'addition': addition, 'state': int(state),
                            'building': kind, 'quantity': quantity,
                            'line': text[:start].count('\n') + 1})
        text = text[:start] + addition + text[start:]
    return text


def proof(before: str, after: str, changes: list[dict]) -> None:
    """Reversing only recorded replacements must reproduce every original byte."""
    reverse = after
    for entry in reversed(changes):
        # Reverse exact transformed spans, preserving unrelated identical
        # predicates and their positions elsewhere in the source.
        start, end = entry['new_start'], entry['new_end']
        assert reverse[start:end] == entry['after']
        reverse = reverse[:start] + entry['before'] + reverse[end:]
    assert reverse == before, 'Unrelated text changed'
    from vietnam_1970.script_ast import parse, walk, first
    old_tree, new_tree = parse(before), parse(after)
    assert old_tree and new_tree
    # Money, party and once-only receipt statements are not query payloads.
    retained = ('set_country_flag', 'clr_country_flag', 'has_country_flag',
                'modify_treasury_effect', 'country_event', 'tag', 'ruling_party',
                'treasury_change', 'add_building_construction',
                'add_extra_state_shared_building_slots', 'is_owned_and_controlled_by',
                'owns_state', 'controls_state', 'has_war_with')
    def statements(tree):
        return [(k, op, value) for k, op, value in walk(tree) if k in retained]
    assert statements(old_tree) == statements(new_tree), 'Transaction statements changed'
    for entry in changes:
        fields = [(k, op, v) for k, op, v in walk(parse(entry['after']))]
        checks = [v for k, _, v in fields if k == 'check_variable']
        assert checks, entry
        assert any(first(v, 'var') == 'building_level@' + entry['building'] for v in checks), entry


def install(dry_run=False):
    results = []; pending = []
    for rel, kinds in FILES.items():
        path = ROOT / rel; raw = path.read_bytes()
        assert not raw.startswith(b'\xef\xbb\xbf'), rel
        before = raw.decode('utf-8'); changes = []
        after = rewrite_selected(before, kinds, changes=changes)
        proof(before, after, changes)
        assert rewrite_selected(after, kinds) == after, 'Not idempotent: ' + rel
        if not after.startswith('# IMPERIA COLD WAR — '):
            after = MARK + after
        result = after.encode('utf-8')
        results.append({'path': rel, 'before_sha256': hashlib.sha256(raw).hexdigest(),
                        'after_sha256': hashlib.sha256(result).hexdigest(),
                        'replacement_count': len(changes), 'changes': changes,
                        'inverse_bytes_proof': True, 'transaction_ast_proof': True})
        pending.append((path, raw, result))
    for path, raw, _ in pending:
        assert path.read_bytes() == raw, 'Concurrent modification: ' + str(path)
    if not dry_run:
        for path, raw, result in pending:
            assert path.read_bytes() == raw, 'Concurrent modification: ' + str(path)
            if raw != result:
                temporary = path.with_name(path.name + '.capacity.tmp')
                temporary.write_bytes(result); temporary.replace(path)
    report = {'project': 'IMPERIA COLD WAR', 'created_utc': datetime.now(timezone.utc).isoformat(),
              'scope': '20 Iraqi focus gifts and Cuban Havana silo/Soviet radar agreement; seven bounded live providers.',
              'dry_run': dry_run, 'replacements': sum(r['replacement_count'] for r in results),
              'files': results, 'checks': ['Every byte outside selected query payloads retained before optional first project comment',
                  'Money, ownership, party, receipt, construction, slot and event AST statements retained',
                  'Central physical building-level predicate present', 'Idempotent transformation',
                  'No broad compiler or approval-snapshot write', 'UTF-8 scripts without BOM'],
              'limits': 'Source/AST proof only; no engine launch or live multiplayer test.'}
    if not dry_run:
        out = ROOT / 'docs/design/usa_capacity_20261027/IRQ_CUB_IMPLEMENTATION.json'
        out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


def install_slots(dry_run=False):
    from vietnam_1970.script_ast import parse, walk
    results = []; pending = []
    for rel in SLOT_FILES:
        path = ROOT / rel; raw = path.read_bytes(); before = raw.decode('utf-8')
        changes = []; after = irq_slots(before, changes)
        self_check = after
        # The recorded source positions preceded lower-position insertions;
        # remove final insertions from left to right using the accumulated shift.
        for entry in sorted(changes, key=lambda c: c['source_start']):
            start = entry['source_start']
            assert self_check[start:start + len(entry['addition'])] == entry['addition']
            self_check = self_check[:start] + self_check[start + len(entry['addition']):]
        assert self_check == before, rel
        # Nested parent values contain the new statements, so compare the exact
        # reversed AST rather than stripping all pre-existing slot grants.
        assert parse(self_check) == parse(before) and parse(after), rel
        assert irq_slots(after) == after, rel
        assert not raw.startswith(b'\xef\xbb\xbf') and after.startswith('# IMPERIA COLD WAR — ')
        result = after.encode('utf-8')
        results.append({'path': rel, 'before_sha256': hashlib.sha256(raw).hexdigest(),
                        'after_sha256': hashlib.sha256(result).hexdigest(),
                        'inserted_slot_commands': len(changes), 'changes': changes,
                        'inverse_bytes_and_ast_proof': True})
        pending.append((path, raw, result))
    for path, raw, _ in pending:
        assert path.read_bytes() == raw, 'Concurrent modification: ' + str(path)
    if not dry_run:
        for path, raw, result in pending:
            assert path.read_bytes() == raw, 'Concurrent modification: ' + str(path)
            if raw != result:
                temporary = path.with_name(path.name + '.capacity.tmp')
                temporary.write_bytes(result); temporary.replace(path)
    report = {'project': 'IMPERIA COLD WAR', 'dry_run': dry_run,
              'slot_commands_added': sum(r['inserted_slot_commands'] for r in results),
              'files': results,
              'replay': 'No country migration or receipt reset. Existing delivered/credited components execute no new building or slot grant.',
              'source_proof': 'Only one adjacent same-state slot command per actually emitted remaining instant building level added; all original statements and guards unchanged.'}
    if not dry_run:
        out = ROOT / 'docs/design/usa_capacity_20261027/IRQ_CUB_IMPLEMENTATION.json'
        combined = json.loads(out.read_text(encoding='utf-8'))
        combined['slot_layer'] = report
        combined['final_source_hashes'] = {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
                                           for rel in set(FILES) | set(SLOT_FILES)}
        out.write_text(json.dumps(combined, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--dry-run', action='store_true'); parser.add_argument('--slots', action='store_true')
    args = parser.parse_args(); result = install_slots(args.dry_run) if args.slots else install(args.dry_run)
    print(json.dumps({'dry_run': result['dry_run'], 'replacements': result.get('replacements', 0),
                      'slot_commands_added': result.get('slot_commands_added', 0), 'files': len(result['files'])}))
