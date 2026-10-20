"""Independent regression audit for Syrian domestic event choices.

Checks emitted labels, visible outcomes, distinct executed choices, the
Atassi/Jadid mandate split and the legal campaign/coalition decision gates.
This is a source contract check, not a claim of a fresh HOI4 engine test.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
import re

from validate_content import parse, first, vals, walk, plain

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'COLDWAR_SYR_'
EVENT_FILE = 'events/COLDWAR_SYR_politics_events.txt'
EFFECT_FILE = 'common/scripted_effects/COLDWAR_SYR_politics_effects.txt'
DECISION_FILE = 'common/decisions/COLDWAR_SYR_politics_decisions.txt'
OUTLOOKS = {'western': [1, 2, 3], 'emerging': [4, 7],
            'nonaligned': [12, 13], 'nationalist': [20, 21, 22]}
MATERIAL = {'add_stability', 'add_war_support', 'add_ideas', 'remove_ideas',
            'add_timed_idea', 'modify_treasury_effect'}


def execution(body):
    """Exclude native display-only effects while retaining actual political state."""
    result = []
    for key, op, value in body:
        if key in ('effect_tooltip', 'custom_effect_tooltip', 'ai_chance',
                   'trigger', 'name', 'tooltip', 'localization_key'):
            continue
        if isinstance(value, list):
            value = execution(value) if key != 'limit' else value
        result.append((key, op, value))
    return result


def material(body):
    result = collections.Counter()
    for key, op, value in walk(body):
        if key in MATERIAL or (key == 'set_temp_variable' and isinstance(value, list)
                               and value and value[0][0] == 'treasury_change'):
            result[json.dumps((key, op, value), separators=(',', ':'))] += 1
    return result


def audit(root=ROOT):
    root = Path(root)
    errors, hashes, loc, duplicate_loc = [], {}, {}, []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def source(relative):
        path = root/relative
        raw = path.read_bytes()
        hashes[relative] = hashlib.sha256(raw).hexdigest()
        return parse(raw.decode('utf-8-sig'))

    for path in sorted((root/'localisation/english').glob('COLDWAR_SYR*.yml')):
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            match = re.match(r'\s*([^#\s:]+):\d*\s+"(.*)"\s*$', line)
            if match:
                key, value = match.groups()
                if key in loc:
                    duplicate_loc.append(key)
                loc[key] = value
    check(not duplicate_loc, 'Duplicate Syrian English keys: '+str(duplicate_loc[:12]))

    events = {first(value, 'id'): value for value in vals(source(EVENT_FILE), 'country_event')}
    effects = {key: value for key, _, value in source(EFFECT_FILE)}
    decision_ast = source(DECISION_FILE)
    decisions = {key: value for _, _, category in decision_ast for key, _, value in category
                 if isinstance(value, list)}
    option_count, material_count, distinct_count = 0, 0, 0
    for ident, event in events.items():
        title, desc = first(event, 'title'), first(event, 'desc')
        check(title in loc and desc in loc, 'Missing event title/description: '+ident)
        options = vals(event, 'option')
        labels, outcomes, signatures = [], [], []
        for index, option in enumerate(options):
            option_count += 1
            key = first(option, 'name')
            expected = ident+'.option_'+chr(97+index)
            check(key == expected, 'Unsafe/unstable option key: '+str(key))
            check(key not in (title, desc), 'Option collides with event title/description: '+str(key))
            label = loc.get(key, '')
            labels.append(label)
            check(bool(label) and len(label) < 140, 'Missing/overlong option label: '+str(key))
            check(label != loc.get(desc), 'Event description used as option label: '+str(key))
            tip = first(option, 'custom_effect_tooltip')
            check(tip == key+'_outcome_tt' and bool(loc.get(tip)), 'Missing unconditional outcome: '+str(key))
            text = loc.get(tip, '')
            outcomes.append(text)
            check(not re.search(r'COLDWAR_SYR_|party_index|ruling_party|_array', text),
                  'Internal script names in outcome: '+str(key))
            actual = execution(option)
            signatures.append(json.dumps(actual, separators=(',', ':')))
            check(all(k in ('name', 'ai_chance', 'trigger', 'custom_effect_tooltip',
                            'effect_tooltip', 'hidden_effect') for k, _, _ in option),
                  'Exposed execution/bookkeeping in option: '+str(key))
            if actual:
                check(len(vals(option, 'hidden_effect')) == 1,
                      'Actual choice is not guarded/hidden once: '+str(key))
                check(len(vals(first(option, 'hidden_effect'), 'if')) == 1,
                      'Choice lost its final office/legality recheck: '+str(key))
            shown = []
            for block in vals(option, 'effect_tooltip'):
                shown.extend(block)
            check(material(shown) == material(actual), 'Native material preview mismatch: '+str(key))
            material_count += sum(material(actual).values())
        check(len(set(labels)) == len(labels), 'Duplicate choice labels: '+ident)
        check(len(set(outcomes)) == len(outcomes), 'Indistinguishable visible outcomes: '+ident)
        check(len(set(signatures)) == len(signatures), 'Duplicate executed choices: '+ident)
        distinct_count += len(set(signatures))

    # The screenshot showed Atassi dying and being recreated for either policy
    # mandate. These choices must be different without touching a real person.
    mandate = events.get(PREFIX+'POL.3', [])
    options = vals(mandate, 'option')
    for index in range(min(2, len(options))):
        body = execution(options[index])
        check(any(k == 'set_variable' and first(v, PREFIX+'baath_mandate') == str(index)
                  for k, _, v in walk(body) if isinstance(v, list)),
              'Mandate choice lacks its distinct actual mandate: '+str(index))
        check(any(k == PREFIX+'sync_baath_mandate' and v == 'yes' for k, _, v in walk(body)),
              'Mandate choice does not synchronize programme ownership: '+str(index))
        check(not any(k in ('kill_country_leader', 'retire_country_leader', 'create_country_leader',
                            PREFIX+'1970_set_leader') for k, _, _ in walk(body)),
              'Mandate-only choice still changes the president: '+str(index))
    sync = effects.get(PREFIX+'sync_baath_mandate', [])
    check(not any(k in ('kill_country_leader', 'retire_country_leader', 'create_country_leader')
                  for k, _, _ in walk(sync)), 'Mandate synchronization replaces a person')
    for flag in ('atassi', 'jadid'):
        check(('clr_country_flag', '=', PREFIX+'leader_'+flag) in sync,
              'Mandate synchronization does not clear the old programme: '+flag)
    check(any(k == PREFIX+'refresh_programmes' and v == 'yes' for k, _, v in walk(sync)),
          'Mandate synchronization does not refresh actual programmes')

    setter = effects.get(PREFIX+'1970_set_leader', [])
    check(not any(k == 'kill_country_leader' for k, _, _ in walk(setter)),
          'Political leader selection still kills a living predecessor')
    replacements = [value for key, _, value in walk(setter)
                    if key == 'if' and isinstance(value, list) and vals(value, 'create_country_leader')]
    for replacement in replacements:
        created = vals(replacement, 'create_country_leader')
        limit = first(replacement, 'limit', [])
        existing = [v for k, _, v in walk(limit) if k == 'has_country_leader']
        check(len(existing) == 1 and first(existing[0], 'name') == first(created[0], 'name'),
              'Leader replacement does not guard the same incumbent')
        check(any(k == 'NOT' for k, _, _ in limit), 'Incumbent guard is not negated')
        check(('retire_country_leader', '=', 'yes') in replacement,
              'Genuine leadership transfer lacks native retirement')
    check(bool(replacements), 'No guarded leader installation branches found')

    for index, (outlook, slots) in enumerate(OUTLOOKS.items()):
        for kind, number in (('campaign', 20+index), ('coalition', 24+index)):
            ident = PREFIX+'decision_'+kind+'_'+outlook
            available = first(decisions.get(ident, []), 'available', [])
            raw = json.dumps(available)
            for slot in slots:
                check('party_banned_array^'+str(slot) in raw,
                      'Paid political decision allows a cancel-only menu: '+ident)
                if kind == 'coalition':
                    check('party_pop_array^'+str(slot) in raw and 'gov_coalition_array' in raw,
                          'Coalition decision lacks support/membership guard: '+ident)
            choices = vals(events.get(PREFIX+'POL.'+str(number), []), 'option')
            check(len(choices) == len(slots)+1, 'Political menu lost a party or cancellation: '+ident)
            for option, slot in zip(choices, slots):
                actual = json.dumps(execution(option))
                expected = 'party_index' if kind == 'campaign' else 'add_col_one'
                check(any(k == 'set_temp_variable' and first(v, expected) == str(slot)
                          for k, _, v in walk(execution(option)) if isinstance(v, list)),
                      'Political choice affects the wrong party: '+first(option, 'name'))

    return {'passed': not errors, 'errors': errors, 'events': len(events),
            'options': option_count, 'distinct_executed_choices': distinct_count,
            'native_material_effects_compared': material_count,
            'guarded_leader_installations': len(replacements), 'source_sha256': hashes,
            'engine_tested': False,
            'limitations': 'Checks loaded-source contracts and actual effect differences; does not prove engine rendering, timing, character revival semantics or multiplayer behavior.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = audit(args.root)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
