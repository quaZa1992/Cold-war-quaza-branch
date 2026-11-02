# IMPERIA COLD WAR — Guard-preserving coastal predecessor building slots.
"""Apply only the two reviewed predecessor corrections and record AST proof.

This does not import or run a country compiler. Existing delivery receipts and
old-save credits continue to govern both the building and its additional slot.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse

MARK = '# IMPERIA COLD WAR — Coastal predecessor building-slot correction.'
SLOT = 'add_extra_state_shared_building_slots = 1'
IRQ_BUILD = 'add_building_construction = { type = dockyard level = 1 instant_build = yes }'
UAE_BUILD = 'add_building_construction = { type = naval_base province = 3725 level = 1 instant_build = no }'


def bounded_block(text: str, name: str, focus: bool = False) -> tuple[int, int]:
    if focus:
        marker = re.search(r'(?m)^\s*id = ' + re.escape(name) + r'\s*$', text)
        assert marker, name
        start = text.rfind('\n\tfocus = {', 0, marker.start()) + 1
        assert start > 0, name
    else:
        marker = re.search(r'(?m)^\s*' + re.escape(name) + r' = \{', text)
        assert marker, name
        start = marker.start()
    opening = text.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return start, end


def marked(text: str) -> str:
    return text if text.startswith('# IMPERIA COLD WAR — ') else MARK + '\n' + text


def strip_added_slots(rows):
    cleaned = []
    for key, op, value in rows:
        if key == 'add_extra_state_shared_building_slots' and str(value) == '1':
            continue
        cleaned.append((key, op, strip_added_slots(value) if isinstance(value, list) else value))
    return cleaned


def build() -> dict:
    # The inserted command is attached to each exact construction statement in
    # its original state scope, never outside its existing delivery transaction.
    runtime = {
        'common/national_focus/COLDWAR_IRQ_1970_focus.txt': [('COLDWAR_IRQ_defence_coastal', True, IRQ_BUILD)],
        'common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt': [('COLDWAR_IRQ_apply_defence_coastal', False, IRQ_BUILD)],
        'common/scripted_effects/COLDWAR_IRQ_1970_direct_rewards_v3.txt': [('COLDWAR_IRQ_upgrade_reward_v3_defence_coastal', False, IRQ_BUILD)],
        'common/decisions/COLDWAR_IRQ_1970_pending.txt': [('COLDWAR_IRQ_defence_coastal_delivery', False, IRQ_BUILD), ('COLDWAR_IRQ_defence_coastal_reward_v3_upgrade_delivery', False, IRQ_BUILD)],
        'common/national_focus/COLDWAR_UAE_1970_focus.txt': [('COLDWAR_UAE_port_planning', True, UAE_BUILD)],
        'common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt': [('COLDWAR_UAE_apply_port_planning', False, UAE_BUILD)],
    }
    out = {}
    records = []
    for rel, targets in runtime.items():
        path = ROOT / rel
        before_bytes = path.read_bytes()
        assert not before_bytes.startswith(b'\xef\xbb\xbf'), rel
        before = before_bytes.decode('utf-8')
        text = before
        inserted = 0
        locations = []
        for name, focus, construction in targets:
            start, end = bounded_block(text, name, focus)
            part = text[start:end]
            assert part.count(construction) == 1, (rel, name)
            match = re.search(r'(?m)^([ \t]*)' + re.escape(construction) + r'(\r?)$', part)
            assert match, (rel, name)
            prefix = part[:match.start()].rstrip()
            if not prefix.endswith(SLOT):
                part = part[:match.start()] + match[1] + SLOT + match[2] + '\n' + part[match.start():]
                inserted += 1
            text = text[:start] + part + text[end:]
            locations.append(name)
        text = marked(text)
        old_ast, new_ast = parse(before), parse(text)
        assert strip_added_slots(old_ast) == strip_added_slots(new_ast), rel
        # A stricter byte proof removes only lines newly added inside the named
        # blocks and an optional first comment. It preserves all other content.
        check = text
        for name, focus, construction in targets:
            start, end = bounded_block(check, name, focus)
            part = check[start:end]
            part = re.sub(r'(?m)^[ \t]*' + re.escape(SLOT) + r'\r?\n(?=[ \t]*' + re.escape(construction) + ')', '', part)
            check = check[:start] + part + check[end:]
        if check.startswith(MARK + '\n') and not before.startswith(MARK + '\n'):
            check = check[len(MARK) + 1:]
        original_without_target_slots = before
        for name, focus, construction in targets:
            start, end = bounded_block(original_without_target_slots, name, focus)
            part = original_without_target_slots[start:end]
            part = re.sub(r'(?m)^[ \t]*' + re.escape(SLOT) + r'\r?\n(?=[ \t]*' + re.escape(construction) + ')', '', part)
            original_without_target_slots = original_without_target_slots[:start] + part + original_without_target_slots[end:]
        assert check == original_without_target_slots, rel
        out[rel] = (before_bytes, text.encode('utf-8'))
        records.append({'path': rel, 'node_blocks': locations, 'inserted_slots': inserted,
                        'before_sha256': hashlib.sha256(before_bytes).hexdigest(),
                        'after_sha256': hashlib.sha256(out[rel][1]).hexdigest(),
                        'proof': 'All other bytes and all original AST statements retained; slot immediately before construction in the same state and guards.'})

    canonical = {
        'tools/iraq_1970/reward_overhaul.py': (
            '    if kind==\'building\':return f\'{c["state"]} = {{ add_building_construction = {{ type = {c["building_type"]} level = {int(amount)} instant_build = yes }} }}\'',
            '    if kind==\'building\':\n'
            '        slots = f\'add_extra_state_shared_building_slots = {int(amount)} \' if c.get(\'receipt\') == P+\'reward_v3_defence_coastal_0\' else \'\'\n'
            '        return f\'{c["state"]} = {{ {slots}add_building_construction = {{ type = {c["building_type"]} level = {int(amount)} instant_build = yes }} }}\''),
        'tools/uae_1970/compile.py': (
            "block('179', '" + UAE_BUILD + "')",
            "block('179', '" + SLOT + "\\n" + UAE_BUILD + "')"),
        'tools/uae_1970/diplomacy.py': (
            'if key == "port_project": preview += "\\n179 = { ' + UAE_BUILD + ' }"',
            'if key == "port_project": preview += "\\n179 = { ' + SLOT + ' ' + UAE_BUILD + ' }"'),
    }
    for rel, (old, new) in canonical.items():
        path = ROOT / rel
        before_bytes = path.read_bytes()
        assert not before_bytes.startswith(b'\xef\xbb\xbf'), rel
        before = before_bytes.decode('utf-8')
        assert before.count(old) + before.count(new) == 1, rel
        text = marked(before.replace(old, new))
        compile(text, str(path), 'exec')
        out[rel] = (before_bytes, text.encode('utf-8'))
        records.append({'path': rel, 'before_sha256': hashlib.sha256(before_bytes).hexdigest(),
                        'after_sha256': hashlib.sha256(out[rel][1]).hexdigest(),
                        'proof': 'One bounded template replacement plus first project marker where previously absent; no compiler executed.'})

    for rel, (old, new) in out.items():
        assert (ROOT / rel).read_bytes() == old, 'Concurrent file modification: ' + rel
    for rel, (_, new) in out.items():
        (ROOT / rel).write_bytes(new)
    return {'project': 'IMPERIA COLD WAR', 'date': '2026-10-25',
            'scope': ['COLDWAR_IRQ_defence_coastal', 'COLDWAR_UAE_port_planning'],
            'runtime_added_slots': sum(r.get('inserted_slots', 0) for r in records),
            'checks': ['Unchanged runtime AST after removing slot statements',
                       'Unchanged original runtime bytes after bounded reversal',
                       'Seven exact state-scoped one-level construction sites',
                       'Python template syntax', 'No BOM in scripts', 'No country compiler run'],
            'files': records,
            'limits': 'No native gameplay test. Existing completed deliveries retain receipts and receive no retroactive slot or asset.'}


if __name__ == '__main__':
    result = build()
    report = ROOT / 'docs/design/naval_adaptation_1970_20261025/PREDECESSOR_SLOT_PROOF.json'
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'runtime_added_slots': result['runtime_added_slots'], 'files': len(result['files']), 'report': str(report)}))
