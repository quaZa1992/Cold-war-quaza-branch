# IMPERIA COLD WAR — Independent validation of direct 1970 currency-history profiles.
"""Read-only audit. Default checks planned text; --actual requires live insertions."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first, walk
from history_patch import BEGIN, END, date_blocks, patched, strip_profile


def load(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def native_currencies():
    result = {}
    for path in sorted((ROOT / 'common/ideas').glob('*.txt')):
        rows = parse(path.read_text(encoding='utf-8-sig'))
        for key, _, rows in rows:
            if key != 'ideas' or not isinstance(rows, list):
                continue
            for category, _, ideas in rows:
                if category != 'reserve_currency' or not isinstance(ideas, list):
                    continue
                for name, _, body in ideas:
                    if isinstance(body, list):
                        assert name not in result, ('Duplicate currency definition', name)
                        result[name] = (path, body)
    return result


def assigned_value(rows, name):
    values = []
    for key, _, value in walk(rows):
        if key != 'set_variable' or not isinstance(value, list):
            continue
        direct = first(value, name)
        if direct is not None:
            values.append(direct)
        elif first(value, 'var') == name:
            values.append(first(value, 'value'))
    return values


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--actual', action='store_true')
    args = ap.parse_args()
    inventory, profiles_doc, research = load('inventory.json'), load('profiles.json'), load('currency.json')
    profiles = profiles_doc['profiles']
    pending = {'ADS', 'ALN', 'C01', 'ZOM'}
    alltags = {c['tag'] for c in inventory['countries']}
    assert set(profiles) == alltags - pending
    assert set(profiles_doc['pending_unchanged_tags']) == pending
    native = native_currencies()
    prohibited = {'euro', 'bitcoin', 'brazilian_real', 'chinese_yuan_2', 'chinese_yuan_3'}
    rules = {'french_franc': {'FRA'}, 'italian_lira': {'ITA'}, 'ddr_mark': {'DDR'}, 'swiss_frank': {'SWI', 'LIC'}}
    counts = Counter()
    snapshots = 0
    after_other_snapshot = []
    for original in inventory['countries']:
        tag = original['tag']
        path = ROOT / original['path']
        raw = path.read_bytes()
        assert not raw.startswith(b'\xef\xbb\xbf'), ('Script BOM', tag)
        text = raw.decode('utf-8')
        if tag in pending:
            assert digest(raw) == original['sha256'], ('Pending history changed', tag)
            assert BEGIN not in text
            assert research['records'][tag]['reserve_currency'] is None
            continue
        profile = profiles[tag]
        currency = profile['currency']
        source = research['records'][tag]
        assert (currency, profile['no_foreign_reserve']) == (source['reserve_currency'], source['no_foreign_reserve']), tag
        assert currency in native and currency not in prohibited, (tag, currency)
        assert currency not in rules or tag in rules[currency], (tag, currency)
        on_add = first(native[currency][1], 'on_add', [])
        native_values = assigned_value(on_add, 'no_foreign_reserve')
        assert native_values == [str(profile['no_foreign_reserve'])], (tag, currency, native_values)
        assert source['currency_strength_action'] == 'retain_existing_else_native_startup_default', tag
        baseline = strip_profile(text)
        assert digest(baseline.encode('utf-8')) == original['sha256'], ('Original bytes not preserved', tag)
        proposed = text if args.actual else patched(text, profile)
        spans = date_blocks(proposed)
        assert len(spans) == original['snapshot_count'], ('Snapshot count', tag)
        assert proposed.count(BEGIN) == len(spans), ('Missing or duplicate profile', tag)
        assert proposed.count(END) == len(spans), ('Unclosed profile', tag)
        for _, start, close, _ in spans:
            body = proposed[start:close]
            begin, end = body.rfind(BEGIN), body.rfind(END)
            assert 0 <= begin < end, ('Profile outside 1970', tag)
            assert not body[end + len(END):].strip(), ('Profile is not final statement', tag)
            block = body[begin:end + len(END)]
            commands = parse(block)
            assert len(commands) == 1 and commands[0][0] == 'if', tag
            effect = commands[0][2]
            assert first(effect, 'limit') == [('IMP_is_1970_scenario', '=', 'yes')], ('Scenario guard', tag)
            # IMPERIA COLD WAR — Accept native scalar and list idea grants within guarded additions.
            chosen = []
            for command, _, grant in walk(effect):
                if command != 'add_ideas':
                    continue
                ideas = [v for k, _, v in grant if k == '_bare'] if isinstance(grant, list) else [grant]
                chosen.extend(idea for idea in ideas if idea in native)
            assert chosen == [currency], ('Wrong currency grant', tag, chosen)
            if first(effect, 'add_ideas') is None:
                currency_grants = [body for command, _, body in walk(effect)
                                   if command == 'if' and isinstance(body, list)
                                   and first(body, 'add_ideas') == currency]
                assert len(currency_grants) == 1, ('Ambiguous guarded currency grant', tag)
                expected_guard = [('NOT', '=', [('has_idea', '=', currency)])]
                assert first(currency_grants[0], 'limit') == expected_guard, ('Currency replay guard', tag)
            assert assigned_value(effect, 'no_foreign_reserve') == [str(profile['no_foreign_reserve'])], tag
            assert assigned_value(effect, 'currency_strength') == [], ('Invented strength', tag)
            assert assigned_value(effect, 'currency_strength_base') == [], ('Invented strength base', tag)
            forbidden_commands = {'every_country', 'every_state', 'random', 'random_list', 'on_daily', 'on_monthly', 'ingame_update_setup', 'calculate_currency_strength', 'country_event'}
            assert not ({k for k, _, _ in walk(effect)} & forbidden_commands), ('Added runtime activity', tag)
            snapshots += 1
        # Informational: old later snapshots are untouched and may independently
        # change currencies for other bookmarks. The start-date guard scopes us.
        for key, _, val in parse(baseline):
            if re.fullmatch(r'\d+\.\d+\.\d+', key) and (1970, 1, 1) < tuple(map(int, key.split('.'))) <= (2000, 1, 1):
                if any(k == 'add_ideas' for k, _, _ in walk(val)):
                    after_other_snapshot.append(tag)
                    break
        counts[currency] += 1
    trigger_file = ROOT / 'common/scripted_triggers/IMP_cold_war_scenario_triggers.txt'
    guard = first(parse(trigger_file.read_text(encoding='utf-8-sig')), 'IMP_is_1970_scenario')
    assert guard == [('has_start_date', '>', '1969.12.31'), ('has_start_date', '<', '1970.1.2')], 'Unexpected scenario guard semantics'
    startup = first(parse((ROOT / 'common/scripted_effects/00_currency_effects.txt').read_text(encoding='utf-8-sig')), 'currency_startup')
    adds = [v for k, _, v in walk(startup) if k == 'add_ideas']
    assert adds == ['deutsche_mark'], ('Native startup currency changes need review', adds)
    assert assigned_value(startup, 'currency_strength') == ['1.0'], 'Native missing-strength default changed'
    # IMPERIA COLD WAR — Persist the independently checked currency report with the provenance record.
    report = {'project': 'IMPERIA COLD WAR', 'mode': 'actual' if args.actual else 'planned',
                      'profiles_validated': len(profiles), 'marked_snapshots_validated': snapshots,
                      'pending_unchanged': sorted(pending), 'currency_counts': dict(counts),
                      'native_on_add_flags_match': True, 'existing_bytes_preserved': True,
                      'new_strength_assignments': 0, 'new_recurring_activity': 0,
                      'later_snapshots_preserved': len(after_other_snapshot)}
    (HERE / 'currency_validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
