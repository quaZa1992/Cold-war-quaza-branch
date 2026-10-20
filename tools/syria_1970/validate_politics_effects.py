"""Bounded source regression for Syrian native ``set_politics`` effects.

MD's numeric ``ruling_party`` variable stores a party slot; the engine effect
instead requires an ideology group or a proven country scope. These are separate
interfaces. This audit does not execute HOI4 or establish the cause of a crash.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from validate_content import first, parse, plain, vals, walk

ROOT = Path(__file__).resolve().parents[2]
POLITICS = 'common/scripted_effects/COLDWAR_SYR_politics_effects.txt'
EVENTS = 'events/COLDWAR_SYR_politics_events.txt'
PACT = 'COLDWAR_SYR_accept_national_pact'
# These helpers are called directly by the Syrian country effects. Their native
# set_politics bodies are inspected, not the unrelated countries in set_leader.
SHARED_HELPERS = {
    'startup_politics': 'common/scripted_effects/00_MD_politicsview_scripted_effects.txt',
    'update_set_politics': 'common/scripted_effects/00_leader_setup_scripted_effects.txt',
}
COUNTRY_ENTRIES = {'COLDWAR_SYR_initial_profile', PACT, *SHARED_HELPERS}
COUNTRY_SCOPES = {'ROOT', 'THIS', 'FROM', 'PREV', 'FROM.FROM', 'PREV.PREV'}
NEUTRAL_BLOCKS = {'if', 'else_if', 'else', 'hidden_effect', 'effect_tooltip',
                  'random', 'random_list', 'while', 'for_loop_effect', 'for_each_loop'}


def politics_errors(body, groups, *, country_effect_scope, known_country_scopes=()):
    """Check one native effect; scope references require caller-supplied proof.

    No guessing from upper-case spelling: e.g. FROM is not implicitly a country.
    A valid ROOT reference is distinct from the MD party-slot variable.
    """
    errors = []
    if not country_effect_scope:
        errors.append('set_politics is not in a proven country effect scope')
    if not isinstance(body, list):
        return errors + ['set_politics requires an argument block']
    parties = vals(body, 'ruling_party')
    if len(parties) != 1:
        return errors + ['set_politics requires exactly one ruling_party']
    party = plain(parties[0])
    if not isinstance(party, str):
        errors.append('ruling_party must be an ideology group or country scope')
    elif party not in groups and party not in known_country_scopes:
        if party in COUNTRY_SCOPES:
            errors.append('unproven country scope for ruling_party: ' + party)
        else:
            errors.append('not a native ideology group or proven country scope: ' + party)
    return errors


def sites(body, ancestry=()):
    """Retain ancestry so a state or unrecognized scope is not silently accepted."""
    for key, _, value in body:
        if key == 'set_politics':
            yield ancestry, value
        elif isinstance(value, list) and key not in ('limit', 'trigger'):
            yield from sites(value, ancestry + (key,))


def country_context(ancestry):
    # Current Syrian sites and shared country-helper sites use these wrappers.
    # Future state/character/unknown scope additions must be reviewed explicitly.
    return all(key in NEUTRAL_BLOCKS for key in ancestry)


def pact_errors(body):
    """Protect the election reform without replacing an incumbent or MD slot."""
    errors = []
    if not isinstance(body, list):
        return ['Missing national-pact helper']
    calls = [(i, value) for i, (key, _, value) in enumerate(body) if key == 'set_politics']
    if len(calls) != 1:
        return ['Pact must contain one direct native set_politics call']
    index, politics = calls[0]
    if not isinstance(politics, list):
        return ['Pact set_politics must be a block']
    expected = {'ruling_party': 'ROOT', 'elections_allowed': 'yes', 'election_frequency': '48'}
    for key, value in expected.items():
        if vals(politics, key) != [value]:
            errors.append('Pact must retain ' + key + ' = ' + value)
    before, after = body[:index], body[index+1:]
    if vals(before, 'set_country_flag') != ['COLDWAR_SYR_national_pact', 'no_leader_change']:
        errors.append('Pact must set the native no_leader_change guard before set_politics')
    if vals(after, 'clr_country_flag') != ['no_leader_change']:
        errors.append('Pact must clear the native no_leader_change guard after set_politics')
    if sum(key == 'set_politics' for key, _, _ in walk(body)) != 1:
        errors.append('Pact contains an extra nested set_politics call')
    if not any(first(value, 'disable_elections') == '0' for value in vals(body, 'set_variable')):
        errors.append('Pact must enable elections in the MD election system')
    for key, _, value in walk(body):
        if key in ('kill_country_leader', 'retire_country_leader', 'create_country_leader'):
            errors.append('Election reform must not replace a leader: ' + key)
        if key == 'set_variable' and isinstance(value, list) and vals(value, 'ruling_party'):
            errors.append('Election reform must preserve the current MD party slot')
    return errors


def audit(root=ROOT):
    root = Path(root)
    errors, checks, hashes = [], Counter(), {}

    def source(relative):
        path = root / relative
        raw = path.read_bytes()
        hashes[relative] = hashlib.sha256(raw).hexdigest()
        return parse(raw.decode('utf-8-sig'))

    groups = set()
    subideologies = set()
    for path in sorted((root/'common/ideologies').glob('*.txt')):
        for block in vals(source(path.relative_to(root).as_posix()), 'ideologies'):
            for group, _, body in block:
                if isinstance(body, list):
                    groups.add(group)
                    for types in vals(body, 'types'):
                        subideologies.update(key for key, _, _ in types)
    if not groups:
        errors.append('Native ideology-group provider is empty or unavailable')

    scripts = {}
    for directory in ('common', 'events', 'history'):
        for path in sorted((root/directory).rglob('COLDWAR_SYR*.txt')):
            relative = path.relative_to(root).as_posix()
            if any(part.lower() in ('backup', 'backups', 'staging') for part in path.relative_to(root).parts[:-1]):
                continue
            scripts[relative] = source(relative)
            checks['loaded_syrian_script_files'] += 1

    direct_shared = set()
    for relative, ast in scripts.items():
        direct_shared.update(key for key, _, _ in walk(ast) if key in SHARED_HELPERS)
        for owner, _, body in ast:
            if not isinstance(body, list):
                continue
            for ancestry, politics in sites(body):
                known_country = relative.startswith('common/scripted_effects/') and owner in COUNTRY_ENTRIES
                context = known_country and country_context(ancestry)
                issues = politics_errors(politics, groups, country_effect_scope=context,
                                         known_country_scopes={'ROOT'} if known_country else set())
                errors.extend(relative + ':' + owner + ': ' + issue for issue in issues)
                checks['syrian_set_politics_sites'] += 1

    for helper in sorted(direct_shared):
        relative = SHARED_HELPERS[helper]
        definitions = vals(source(relative), helper)
        if len(definitions) != 1:
            errors.append('Expected one shared helper definition: ' + helper)
            continue
        for ancestry, politics in sites(definitions[0]):
            issues = politics_errors(politics, groups, country_effect_scope=country_context(ancestry),
                                     known_country_scopes={'ROOT'})
            errors.extend(relative + ':' + helper + ': ' + issue for issue in issues)
            checks['direct_shared_helper_set_politics_sites'] += 1
        checks['direct_shared_country_helpers_reviewed'] += 1

    politics_ast = scripts.get(POLITICS, [])
    pact = first(politics_ast, PACT)
    errors.extend(PACT + ': ' + issue for issue in pact_errors(pact))
    checks['pact_preserves_current_outlook_and_party_slot'] = not pact_errors(pact)
    events = {first(body, 'id'): body for body in vals(scripts.get(EVENTS, []), 'country_event')}
    callers = []
    for ident, event in events.items():
        for option in vals(event, 'option'):
            name = first(option, 'name')
            calls = sum(key == PACT for key, _, _ in walk(option))
            if not calls:
                continue
            callers.append(name)
            executed = sum(key == PACT for block in vals(option, 'hidden_effect') for key, _, _ in walk(block))
            preview = sum(key == PACT for block in vals(option, 'effect_tooltip') for key, _, _ in walk(block))
            if calls != 1 or executed != 1 or preview:
                errors.append('Pact must execute once, outside its preview: ' + str(name))
            expected_idea = {'COLDWAR_SYR_POL.4.option_a': 'COLDWAR_SYR_politics_transition_burden',
                             'COLDWAR_SYR_POL.34.option_a': 'COLDWAR_SYR_politics_command_disruption'}.get(name)
            if not expected_idea:
                errors.append('Unreviewed pact option caller: ' + str(name))
            elif not any(first(value, 'idea') == expected_idea and first(value, 'days') == '180'
                         for block in vals(option, 'hidden_effect') for key, _, value in walk(block)
                         if key == 'add_timed_idea' and isinstance(value, list)):
                errors.append('Pact option lost its 180-day transition burden: ' + str(name))
            if ident == 'COLDWAR_SYR_POL.34' and not any(
                    key == 'set_country_flag' and value == 'COLDWAR_SYR_military_transfer_agreed'
                    for block in vals(option, 'hidden_effect') for key, _, value in walk(block)):
                errors.append('Military pact option lost its negotiated-transfer result')
    if sorted(callers) != ['COLDWAR_SYR_POL.34.option_a', 'COLDWAR_SYR_POL.4.option_a']:
        errors.append('Expected the two reviewed national-pact event options')
    checks['reviewed_pact_event_options'] = len(callers)
    return {'ok': not errors, 'checks': dict(checks), 'errors': errors,
            'native_ideology_groups': sorted(groups), 'subideologies_are_not_group_keys': sorted(subideologies - groups),
            'shared_helpers_reviewed': sorted(direct_shared), 'source_sha256': hashes,
            'engine_tested': False,
            'scope': 'Loaded COLDWAR_SYR*.txt under common/events/history; native ideology providers; '
                     'the bodies of directly called startup_politics/update_set_politics. '
                     'No claim of all-mod transitive helper coverage, engine rendering or crash reproduction.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'source_sha256'}, indent=2))
    raise SystemExit(0 if result['ok'] else 1)
