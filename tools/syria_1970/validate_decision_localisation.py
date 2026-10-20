"""Independent audit of Syrian decision requirements and effect presentation.

Reads emitted scripts/localization and independently recomputes the recorded
pre-presentation gameplay digest. Never imports or runs the presentation writer.
Visibility predicates are internal filtering; available/limit predicates are
player-facing unless enclosed by a native presentation wrapper.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from validate_content import parse, first, vals, walk

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'COLDWAR_SYR_'
PROGRESS = {PREFIX + x for x in ('officer_backing', 'citizenship_stages', 'enterprise_audits', 'irrigation_trials')}
TECHNICAL_KEYS = {'original_tag', 'IMP_is_1970_scenario', 'has_start_date', 'check_variable', 'has_variable'}
WRAPPERS = {'custom_trigger_tooltip', 'custom_override_tooltip', 'hidden_trigger'}


def gameplay_nodes(body):
    """Independently erase UI-only annotations while retaining statement order."""
    nodes = []
    for key, op, value in body:
        if key == 'tooltip':
            continue
        if key in ('custom_trigger_tooltip', 'hidden_trigger', 'hidden_effect') and isinstance(value, list):
            nodes.extend(gameplay_nodes(value))
        else:
            nodes.append((key, op, gameplay_nodes(value) if isinstance(value, list) else value))
    return nodes


def audit(root=ROOT):
    root = Path(root)
    errors = []
    checks = Counter()
    hashes = {}

    def check(condition, message):
        if not condition:
            errors.append(message)

    # Native substitutions may refer to existing MD labels. Country-owned values
    # are parsed strictly; unrelated pre-existing localization is indexed only.
    loc, native_keys = {}, set()
    for path in (root / 'localisation/english').rglob('*.yml'):
        text = path.read_text(encoding='utf-8-sig')
        native_keys.update(re.findall(r'^\s*(\S+):(?:\d+)?\s', text, re.M))
        if not path.name.startswith(PREFIX):
            continue
        raw = path.read_bytes()
        check(raw.startswith(b'\xef\xbb\xbf'), 'English localization needs BOM: ' + path.name)
        check(text.startswith('l_english:'), 'English header missing: ' + path.name)
        hashes[path.relative_to(root).as_posix()] = hashlib.sha256(raw).hexdigest()
        for key, encoded in re.findall(r'^\s+(\S+):(?:\d+)?\s+([^\n]+)$', text, re.M):
            if key.startswith('#'):
                continue
            try:
                value = json.loads(encoded)
            except json.JSONDecodeError:
                errors.append('Malformed quoted English value: ' + key)
                continue
            check(isinstance(value, str), 'Localization must be a string, not an array/object: ' + key)
            if not isinstance(value, str):
                continue
            check(key not in loc, 'Duplicate country localization key: ' + key)
            loc[key] = value
    keys = set(loc) | native_keys

    def validate_text(key):
        check(key in keys, 'Missing English decision/requirement text: ' + str(key))
        if key not in loc:
            return
        text = loc[key]
        check(bool(text.strip()), 'Empty English text: ' + key)
        for ref in re.findall(r'\$([A-Za-z_]\w*(?:\.\w+)*)(?:\|[^$]*)?\$', text):
            check(ref in keys or ref in ('RIGHT', 'LEFT', 'MODIFIER', 'COUNTRY'),
                  'Unresolved localization substitution: ' + key + '/' + ref)
        plain = re.sub(r'\$[^$]+\$|\[\?[^]]+\]', '', text)
        check(not re.search(r'\b(?:COLDWAR_SYR_\w+|has_country_flag|check_variable|party_index|namespace|scripted_effect)\b', plain),
              'Internal script identifier in visible English: ' + key)
        check(not re.search(r'\b(?:Voraussetzung|Entscheidungen|Regierung|Forschung|Wirtschaft)\b', plain),
              'German prose in English decision localization: ' + key)

    helper_bodies = {}
    for directory in ('common/scripted_effects', 'common/scripted_triggers'):
        for path in (root / directory).glob('COLDWAR_SYR*.txt'):
            for key, _, value in parse(path.read_text(encoding='utf-8-sig')):
                if isinstance(value, list):
                    helper_bodies[key] = value

    def trigger(body, owner, path='available', covered=False):
        for key, _, value in body:
            if key in WRAPPERS:
                if key in ('custom_trigger_tooltip', 'custom_override_tooltip'):
                    label = first(value, 'tooltip')
                    check(isinstance(label, str), 'Requirement wrapper has no tooltip key: ' + owner)
                    if isinstance(label, str):
                        validate_text(label)
                        if label.startswith(PREFIX):
                            validate_text(label+'_NOT')
                        checks['localized_requirement_references'] += 1
                trigger(value, owner, path, True)
                continue
            custom_flag = key == 'has_country_flag' and isinstance(value, str) and value.startswith(('COLDWAR_SYR_', 'mdcw_'))
            helper = key.startswith(('COLDWAR_SYR_', 'IMP_', 'mdcw_')) and value in ('yes', 'no')
            if not covered and (key in TECHNICAL_KEYS or custom_flag or helper):
                errors.append('Raw internal predicate outside presentation wrapper: ' + owner + '/' + path + '/' + key)
            if isinstance(value, list):
                trigger(value, owner, path, covered)

    def effect(body, owner, path, covered=False, chain=frozenset()):
        for key, _, value in body:
            if key == 'hidden_effect':
                continue
            if key == 'limit':
                trigger(value, owner, path + '/limit')
                continue
            if key in ('custom_effect_tooltip', 'tooltip', 'localization_key') and isinstance(value, str):
                if value.startswith(PREFIX):
                    validate_text(value)
            if key == 'add_to_variable' and isinstance(value, list):
                variables = [k for k, _, _ in value if k.startswith(PREFIX)]
                if variables:
                    label = first(value, 'tooltip')
                    check(isinstance(label, str), 'Uncaptioned custom variable change: ' + owner + '/' + ','.join(variables))
                    if isinstance(label, str):
                        validate_text(label)
                    for variable in variables:
                        if variable in PROGRESS:
                            check(first(value, variable) == '1', 'Progress caption expects a different actual increment: ' + owner + '/' + variable)
                            checks['captioned_progress_changes'] += 1
            if key in ('clamp_variable', 'COLDWAR_SYR_update_operation_costs', 'COLDWAR_SYR_refresh_programmes', 'update_money_dirty_variable'):
                errors.append('Visible internal cache/clamp/lifecycle effect: ' + owner + '/' + key)
            if key in helper_bodies and value == 'yes' and key not in chain:
                effect(helper_bodies[key], owner, path + '/' + key, covered, chain | {key})
            if isinstance(value, list):
                effect(value, owner, path, covered, chain)

    report_path = root / 'tools/syria_1970/decision_presentation_build.json'
    report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
    expected_hashes = report.get('gameplay_sha256', {})
    helper_path = root/'common/scripted_effects/COLDWAR_SYR_foreign_effects.txt'
    helper_rel = helper_path.relative_to(root).as_posix()
    helper_digest = hashlib.sha256(json.dumps(gameplay_nodes(parse(helper_path.read_text(encoding='utf-8-sig'))), separators=(',', ':')).encode()).hexdigest()
    check(expected_hashes.get(helper_rel) == helper_digest, 'Foreign helper gameplay semantic digest changed')
    decisions = {}
    files = {}
    for path in sorted((root / 'common/decisions').glob('COLDWAR_SYR*.txt')):
        raw = path.read_bytes()
        rel = path.relative_to(root).as_posix()
        hashes[rel] = hashlib.sha256(raw).hexdigest()
        check(b'\xef\xbb\xbf' not in raw, 'Non-localization script contains rejected BOM: ' + rel)
        ast = parse(raw.decode('utf-8-sig'))
        check(not re.search(rb'\b_(?:bare|list)\s*=', raw), 'AST sentinel leaked into decision script: '+rel)
        normalized = gameplay_nodes(ast)
        digest = hashlib.sha256(json.dumps(normalized, separators=(',', ':')).encode()).hexdigest()
        check(rel in expected_hashes and digest == expected_hashes[rel], 'Gameplay semantic digest differs from recorded pre-presentation source: ' + rel)
        files[rel] = {'pre_presentation_gameplay_sha256': expected_hashes.get(rel), 'emitted_gameplay_sha256': digest}
        for category, _, entries in ast:
            if not isinstance(entries, list):
                continue
            for ident, _, body in entries:
                if not isinstance(body, list) or not ident.startswith(PREFIX):
                    continue
                check(ident not in decisions, 'Duplicate decision ID: ' + ident)
                decisions[ident] = body
                validate_text(ident)
                validate_text(ident + '_desc')
                for field in ('available', 'target_trigger', 'cancel_trigger', 'remove_trigger'):
                    for value in vals(body, field):
                        trigger(value, ident, field)
                # Visible/allowed predicates are filtering, intentionally retained.
                for field in ('complete_effect', 'remove_effect', 'cancel_effect', 'timeout_effect'):
                    for value in vals(body, field):
                        effect(value, ident, field)
    gameplay = {k: v for k, v in decisions.items() if not k.endswith('_resume')}
    deferred = {k: v for k, v in decisions.items() if k.endswith('_resume')}
    check(len(decisions) == 489 and len(gameplay) == 69 and len(deferred) == 420,
          'Expected69 gameplay decisions and420 deferred programmes')

    # Regression for the exact photographed officer-bargain tooltip. Check the
    # real flag predicates and readable text; do not merely require key counts.
    officer = decisions.get(PREFIX + 'decision_officer_bargain', [])
    available = first(officer, 'available', [])
    for flag in (PREFIX + 'opening_entry_implemented', PREFIX + 'dual_command_resolved'):
        wrappers = [v for k, _, v in walk(available) if k == 'custom_trigger_tooltip' and
                    isinstance(v, list) and ('has_country_flag', '=', flag) in v]
        check(len(wrappers) == 1, 'Screenshot flag requirement not independently localized: ' + flag)
        for wrapper in wrappers:
            label = first(wrapper, 'tooltip')
            text = loc.get(label, '')
            if flag.endswith('opening_entry_implemented'):
                check('$COLDWAR_SYR_opening_entry$' in text, 'Opening requirement does not reference the actual focus title')
            else:
                check('command settlement' in text.lower(), 'Command-settlement condition lost its historical meaning')
    unresolved = next((v for k, _, v in available if k == 'NOT' and any(
        key == 'has_country_flag' and value == PREFIX + 'dual_command_resolved' for key, _, value in walk(v))), None)
    check(unresolved is not None, 'Presentation accidentally removed/reversed the unsettled-command condition')
    for key in (PREFIX + x + '_change_tt' for x in ('officer_backing', 'citizenship_stages', 'enterprise_audits', 'irrigation_trials')):
        validate_text(key)
        check('+1' in loc.get(key, '') or '$RIGHT' in loc.get(key, ''), 'Progress caption does not expose its actual positive increment: ' + key)
    return {
        'status': 'FAIL' if errors else 'PASS', 'errors': list(dict.fromkeys(errors)),
        'decisions': len(decisions), 'gameplay_decisions': len(gameplay), 'deferred_programmes': len(deferred),
        'presentation_checks': dict(checks), 'semantic_parity_files': files, 'file_hashes': hashes,
        'screenshot_regression_checked': True, 'engine_hover_retested': False,
        'limitations': 'Independent emitted-source/localization and recorded pre-presentation semantic-digest checks. Visibility predicates remain internal filtering. Fresh actual HOI4 decision hovers are not established by this report.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'file_hashes'}, ensure_ascii=True, indent=2))
    raise SystemExit(bool(result['errors']))


if __name__ == '__main__':
    main()
