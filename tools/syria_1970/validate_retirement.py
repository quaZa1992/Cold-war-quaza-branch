"""Check the installed retirement against backed-up providers and live callers."""
from pathlib import Path
import json
import re
from retire_modern import FILES, HISTORY, definitions, tokens

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def audit():
    registry = {}
    for relative in FILES:
        backup = HERE/'retired_modern'/relative
        if backup.is_file():
            registry.update(definitions(relative, backup.read_text(encoding='utf-8-sig')))
    reports = [json.loads((HERE/name).read_text(encoding='utf-8')) for name in ('retirement_report.json', 'retirement_auxiliary_report.json')]
    errors, live, providers = [], {}, set()
    old_focuses = set(definitions('common/national_focus/05_syria.txt', (HERE/'retired_modern/common/national_focus/05_syria.txt').read_text(encoding='utf-8-sig')))
    for folder in ('common', 'events', 'history'):
        for path in (ROOT/folder).rglob('*.txt'):
            source = path.read_text(encoding='utf-8-sig')
            executable = re.sub(r'#[^\n]*', '', source)
            live[path.relative_to(ROOT).as_posix()] = executable
            providers.update(re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*\{', executable))
            providers.update(re.findall(r'\bid\s*=\s*([A-Za-z_]\w*\.\d+)\b', executable))
    for report in reports:
        for relative in report['retired_files']:
            if (ROOT/relative).exists():
                errors.append('Retired file still loaded: '+relative)
            if not (HERE/'retired_modern'/relative).is_file():
                errors.append('Recovery copy absent: '+relative)
    incoming = {}
    for relative, source in live.items():
        old_refs = tokens(source) & registry.keys()
        # Public trigger stubs deliberately remain false. Foreign/shared
        # definitions are real providers, never invisible focus placeholders.
        for ident in old_refs:
            kind = registry[ident][0]
            if ident in old_focuses:
                if re.search(r'\b(?:has_completed_focus|complete_national_focus|uncomplete_national_focus|focus)\s*=\s*'+re.escape(ident)+r'\b', source):
                    errors.append(f'Dangling modern focus {ident}: {relative}')
            elif kind in ('scripted_effects', 'scripted_triggers', 'idea', 'dynamic_modifiers', 'templates', 'event', 'opinion', 'character') and ident not in providers:
                errors.append(f'Missing retained {kind} provider {ident}: {relative}')
        if old_refs:
            incoming[relative] = sorted(old_refs)
        if re.search(r'\bSyria_2000\b|\bSyriaFocus\.(?:39|40|41|42)\b', source):
            errors.append('Retired modern tree/succession reference: '+relative)
    history = (ROOT/HISTORY).read_text(encoding='utf-8-sig')
    if re.search(r'(?m)^\s*20\d\d\.\d+\.\d+\s*=\s*\{', history):
        errors.append('Modern Syrian country-history block remains')
    if 'load_focus_tree = COLDWAR_SYR_1970_focus' not in history:
        errors.append('New Syrian focus tree absent from 1970 history')
    for relative in reports[0]['retired_foreign_focus_conditions']:
        current = live[relative]
        if 'SYR_ai_behavior' in current and relative.endswith(('00_game_rules.txt', '999_game_rules_on_actions.txt')):
            errors.append('Old Syrian AI selection still available: '+relative)
    english = ROOT/'localisation/english/COLDWAR_SYR_shared_legacy_l_english.yml'
    text_keys = set(re.findall(r'^\s+([\w.]+):', english.read_text(encoding='utf-8-sig'), re.M))
    missing = set(reports[1]['retained_english_keys'])-text_keys
    if missing:
        errors.append('Missing shared English text: '+str(sorted(missing)))
    return {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
            'retired_files': sum(len(r['retired_files']) for r in reports),
            'retained_shared_definitions': len(reports[0]['retained_shared_definitions']),
            'retained_english_keys': len(text_keys), 'live_files_checked': len(live),
            'engine_tested': False}


if __name__ == '__main__':
    result = audit()
    (HERE/'retirement_validation.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['errors']))
