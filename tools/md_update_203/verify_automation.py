# IMPERIA COLD WAR — MD 2.0.3 automation wiring and feature-preservation verification.
"""Read current loaded sources; write only a new audit evidence report.

This checks wiring and source preservation. It does not simulate native GUI
clicks, certify every programme, or substitute for a multiplayer rehearsal.
"""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import re
import sys

from audit import ROOT, OUT, UP, PROJECT, emit, scan

sys.path.insert(0, str(ROOT/'Claude outputs/COLDWAR_SOV_generator/tools'))
import pdx


def walk(nodes):
    for node in nodes:
        yield node
        if isinstance(node[2], list):
            yield from walk(node[2])


def unquote(value):
    return value.strip('"') if isinstance(value, str) else value


def tokens(text):
    return [token for token, line in pdx.tokenize(text)[0]]


def main():
    checks = []
    failures = []

    def check(condition, name):
        (checks if condition else failures).append(name)

    with gzip.open(OUT/'all_files.jsonl.gz', 'rt', encoding='utf-8') as stream:
        inventory = [json.loads(line) for line in stream]
    original = {r['cold_war']['path']: r['cold_war'] for r in inventory if r['cold_war']}
    expected_source = {r['new_md']['path'].casefold(): r['new_md'] for r in inventory if r['new_md']}
    current_source, exclusions = scan(UP)
    source_metadata_changes = sorted(set(expected_source) ^ set(current_source))
    source_metadata_changes += [current_source[k]['path'] for k in set(expected_source) & set(current_source)
        if any(expected_source[k][field] != current_source[k][field] for field in ('bytes', 'mtime_ns'))]
    check(not source_metadata_changes, 'Supplied MD inventory has no path, size or modification-time change since the complete hash pass')

    paths = [
        'interface/MD_automation_settings.gui',
        'interface/countryintelligenceagencyview.gui',
        'common/scripted_guis/01_automation_settings_scripted_gui.txt',
        'common/scripted_localisation/00_automation_settings_scripted_localisation.txt',
        'localisation/english/MD_automation_settings_l_english.yml',
        'common/scripted_effects/00_economy_automation_effects.txt',
        'common/scripted_effects/00_internal_investment_automation_effects.txt',
        'common/scripted_effects/00_space_automation_effects.txt',
        'common/scripted_effects/00_influence_scripted_effects.txt',
        'common/on_actions/00_on_actions.txt',
        'common/on_actions/MD_on_actions.txt',
        'common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt',
        'common/scripted_guis/COLDWAR_SSR_intelligence.txt',
        'common/scripted_triggers/COLDWAR_SSR_intelligence.txt',
        'common/scripted_effects/00_lar_effects.txt',
        'interface/COLDWAR_SSR_intelligence.gui',
        'common/scripted_effects/00_money_system.txt',
        'common/synchronized_dynamic_tokens/MD_tokens.txt',
        'interface/countrytechtreeview.gui',
        'interface/countrytradeview.gui',
        'interface/MD_countrymissilesview.gui',
    ]
    parsed, sources, preserved = {}, {}, []
    for rel in paths:
        path = ROOT/rel
        check(path.is_file(), rel+': loaded file exists')
        if not path.is_file():
            continue
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        check(rel in original and digest == original[rel]['sha256'], rel+': unchanged bytes since the pre-update Cold War inventory')
        sources[rel] = raw.decode('utf-8-sig')
        preserved.append(dict(path=rel, sha256=digest))
        if path.suffix != '.yml':
            check(not raw.startswith(b'\xef\xbb\xbf'), rel+': UTF-8 without BOM')
            depth = 0
            balanced = True
            for token in tokens(sources[rel]):
                if token == '{': depth += 1
                elif token == '}': depth -= 1
                if depth < 0: balanced = False
            check(balanced and depth == 0, rel+': balanced native script blocks')
            parsed[rel] = pdx.parse(sources[rel])[0]

    donor_equal = []
    for rel in paths[:5]:
        current, donor = (ROOT/rel).read_text(encoding='utf-8-sig'), (UP/rel).read_text(encoding='utf-8-sig')
        equal = tokens(current) == tokens(donor)
        check(equal, rel+': complete executable token stream matches supplied MD 2.0.3')
        donor_equal.append(rel)

    gui = parsed['interface/MD_automation_settings.gui']
    windows = {unquote(pdx.get(value, 'name')): value for key, op, value, line in walk(gui)
        if isinstance(value, list) and key == 'containerWindowType'}
    sg = pdx.get(parsed['common/scripted_guis/01_automation_settings_scripted_gui.txt'], 'scripted_gui')
    callbacks = []
    for name, op, body, line in sg:
        window_name = unquote(pdx.get(body, 'window_name'))
        check(window_name in windows, name+': complete native parent window resolves')
        if window_name not in windows: continue
        widgets = {unquote(pdx.get(value, 'name')) for key, op, value, ln in walk(windows[window_name]) if isinstance(value, list)}
        for callback, op, effect, ln in pdx.get(body, 'effects', []):
            widget = re.sub(r'_(?:control_|shift_|right_)?click$', '', callback)
            check(widget in widgets, name+': '+callback+' resolves to its own native widget')
            callbacks.append(dict(panel=name, callback=callback, line=ln))

    # Resolve dynamic checkbox images to the registered scripted-localisation names.
    loc = parsed['common/scripted_localisation/00_automation_settings_scripted_localisation.txt']
    names = {pdx.get(value, 'name') for key, op, value, ln in loc if key == 'defined_text'}
    # The energy checkbox intentionally lives in MD's shared money localisation.
    money_loc = pdx.parse((ROOT/'common/scripted_localisation/01_money_scripted_localisation.txt').read_text(encoding='utf-8-sig'))[0]
    names.update(pdx.get(value, 'name') for key, op, value, ln in money_loc if key == 'defined_text')
    dynamic_images = re.findall(r'image\s*=\s*"\[([A-Za-z_0-9]+)\]"', sources['common/scripted_guis/01_automation_settings_scripted_gui.txt'])
    for name in dynamic_images:
        check(name in names, name+': dynamic checkbox image provider resolves')

    hooks = parsed['common/on_actions/00_on_actions.txt'] + parsed['common/on_actions/MD_on_actions.txt']
    hook_calls = collections.defaultdict(list)
    for key, op, entries, ln in hooks:
        if key != 'on_actions': continue
        for hook, op, effect, ln in entries:
            for call, op, value, line in walk(effect):
                if isinstance(value, str) and value == 'yes': hook_calls[call].append(hook)
    required_hooks = {
        'automation_influence_daily': 'on_daily',
        'automation_internal_investments_daily': 'on_daily',
        'automation_internal_investments_weekly': 'on_weekly',
        'automation_economy_weekly': 'on_weekly',
        'space_automation_weekly': 'on_weekly',
        'space_automation_monthly': 'on_monthly',
    }
    for name, hook in required_hooks.items():
        check(hook in hook_calls[name], name+': reachable from '+hook)

    definitions = collections.defaultdict(list)
    for path in (ROOT/'common/scripted_effects').glob('*.txt'):
        for name in re.findall(r'(?m)^([A-Za-z_][A-Za-z_0-9]*)\s*=\s*\{', path.read_text(encoding='utf-8-sig')):
            definitions[name].append(path.relative_to(ROOT).as_posix())
    for name in required_hooks:
        check(len(definitions[name]) == 1, name+': unique active scripted-effect provider')

    agency = sources['interface/countryintelligenceagencyview.gui']
    check(all('"'+name+'"' in agency for name in ('queue_badge', 'queue_badge_text', 'cancel_upgrade', 'upgrade_button')), 'Native agency queue badge, cancellation and upgrade widgets are present')
    upgrades = parsed['common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt']
    completed = []
    for key, op, value, line in walk(upgrades):
        if key == 'complete_effect' and isinstance(value, list):
            for k, o, v, ln in walk(value):
                if k == 'COLDWAR_NI_passive_defense_level': completed.append(v)
    check(completed == ['1', '2', '3', '4'], 'All four completed passive-defence levels retain nuclear-intelligence receipts')
    check('parent_window_name = "countryintelligenceagencyview"' in sources['common/scripted_guis/COLDWAR_SSR_intelligence.txt'], 'SSR creation blocker remains attached to the native agency window')
    check('COLDWAR_can_create_intelligence_agency = yes' in sources['common/scripted_effects/00_lar_effects.txt'], 'Generic agency rewards retain the SSR permission guard')
    check('mdcw_own_soi_duration = 360' in sources['common/scripted_effects/00_internal_investment_automation_effects.txt'], 'Internal investment automation retains custom Cold War investment terms')

    report = dict(project=PROJECT, status='PASS' if not failures else 'FAIL',
        evidence_level='Current source structure, upstream parity, callbacks and recurring-hook wiring only',
        source_files_seen=len(current_source), source_metadata_changes=source_metadata_changes,
        current_source_hashes=preserved, full_donor_parity=donor_equal,
        callback_count=len(callbacks), callbacks=callbacks, dynamic_image_count=len(dynamic_images),
        recurring_hooks={name: hook_calls[name] for name in required_hooks},
        checks=checks, failures=failures,
        limitations=['No native automation-button interaction or end-to-end automation execution is asserted.',
            'Preserved sources do not prove all historical features were defect-free before the update.',
            'No multi-client, save/rehost or simultaneous-action verification.'])
    emit(OUT/'automation_verification.json', report)
    print(json.dumps({key: report[key] for key in ('status', 'source_files_seen', 'source_metadata_changes', 'callback_count', 'dynamic_image_count', 'failures')}, indent=2))
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
