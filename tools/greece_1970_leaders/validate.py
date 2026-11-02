# IMPERIA COLD WAR — Greek undated candidate selection validation.
"""Bounded static and interpreted-script checks. This is not the HOI4 engine."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import importlib.util
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
from multiplayer_quality.audit import parse
from greece_1970_leaders.build import P, PARTY_TRIGGERS, DEFAULTS


def first(tree, key, default=None):
    return next((v for k, op, v in tree if k == key), default)


def walk(tree):
    for key, op, value in tree:
        yield key, op, value
        if isinstance(value, list):
            yield from walk(value)


def unquote(s):
    return s.strip('"')


class Model:
    def __init__(self, effects, party=22, when=(1970, 1, 1), tag='GRE', scenario=True, human=True):
        self.effects = effects
        self.party = party
        self.when, self.tag, self.scenario, self.human = when, tag, scenario, human
        self.variables = {'ruling_party': party}
        self.flags, self.characters = set(), set()
        self.leader = ''
        self.creations, self.retirements, self.callbacks = 0, 0, 0

    def number(self, v):
        if v in self.variables:
            return self.variables[v]
        try:
            return float(v)
        except ValueError:
            return 0

    def condition(self, tree):
        def item(key, op, value):
            if key == 'OR':
                return any(item(*row) for row in value)
            if key in ('AND', 'hidden_trigger'):
                return self.condition(value)
            if key == 'NOT':
                return not self.condition(value)
            if key == 'original_tag':
                return value == self.tag
            if key == 'exists':
                return value == 'yes'
            if key == 'IMP_is_1970_scenario':
                return self.scenario == (value == 'yes')
            if key == 'is_ai':
                return (not self.human) == (value == 'yes')
            if key in PARTY_TRIGGERS.values():
                return PARTY_TRIGGERS.get(self.party) == key and value == 'yes'
            if key == 'has_country_flag':
                return value in self.flags
            if key == 'has_character':
                return value in self.characters
            if key == 'has_country_leader':
                return unquote(first(value, 'name')) == self.leader
            if key == 'check_variable':
                return all(self.number(k) == self.number(v) for k, op, v in value)
            if key == 'date':
                other = tuple(map(int, value.split('.')))
                return self.when > other if op == '>' else self.when < other
            raise AssertionError('Uninterpreted trigger: ' + key)
        return all(item(*row) for row in tree)

    def run(self, tree, depth=0):
        assert depth < 24
        chain = False
        for key, op, value in tree:
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    chain = False
                if not chain and (key == 'else' or self.condition(first(value, 'limit', []))):
                    self.run([r for r in value if r[0] != 'limit'], depth + 1)
                    chain = True
            elif key in self.effects:
                self.run(self.effects[key], depth + 1)
            elif key == 'set_country_flag':
                self.flags.add(value)
            elif key == 'clr_country_flag':
                self.flags.discard(value)
            elif key == 'set_variable':
                for k, op, v in value:
                    self.variables[k] = self.number(v)
            elif key == 'create_country_leader':
                self.leader = unquote(first(value, 'name'))
                self.creations += 1
            elif key == 'retire_country_leader':
                self.leader = ''
                self.retirements += 1
            elif key == 'recruit_character':
                self.characters.add(value)
            elif key == 'retire_character':
                self.characters.discard(value)
            elif key in ('update_set_politics', 'set_correct_ideology_trait'):
                pass  # Native MD execution boundary, not simulated.
            elif key == P + 'reconcile_programmes_effect':
                self.callbacks += 1  # Existing programme owner is deliberately not reimplemented.
            else:
                raise AssertionError('Uninterpreted effect: ' + key)

    def effect(self, key):
        self.run(self.effects[key])


def main():
    build = json.loads((HERE / 'build_report.json').read_text(encoding='utf-8'))
    roster = json.loads((HERE / 'runtime_roster.json').read_text(encoding='utf-8'))['roster']
    asts, hashes = {}, {}
    for rel in build['files']:
        path = ROOT / rel
        raw = path.read_bytes()
        hashes[rel] = hashlib.sha256(raw).hexdigest()
        if path.suffix in ('.txt', '.gfx'):
            assert not raw.startswith(b'\xef\xbb\xbf'), rel
            assert raw.decode('utf-8').startswith('# IMPERIA COLD WAR'), rel
            asts[rel] = parse(raw.decode('utf-8'))
        if path.suffix == '.yml':
            assert raw.startswith(b'\xef\xbb\xbf'), rel
            assert raw.decode('utf-8-sig').splitlines()[1].startswith('# IMPERIA COLD WAR'), rel
    chars = dict((k, v) for k, op, v in first(asts['common/characters/COLDWAR_GRE_1970_regional_characters.txt'], 'characters'))
    effects = dict((k, v) for k, op, v in asts['common/scripted_effects/COLDWAR_GRE_1970_regional_effects.txt'])
    assert len(chars) == len(roster) == 36
    definitions = (ROOT / 'common/scripted_triggers/01_political_triggers.txt').read_text(encoding='utf-8')
    assert all(name + ' = {' in definitions for name in PARTY_TRIGGERS.values())
    for row in roster:
        assert row['id'] in chars
        for field, size in (('portrait', (156, 210)), ('small', (38, 51))):
            with Image.open(ROOT / row[field]) as im:
                assert im.size == size, (row['key'], field, im.size)
        if row['kind'] == 'political':
            assert not any(k == 'date' for k, op, v in walk(chars[row['id']])), row['key']
    decisions = asts['common/decisions/COLDWAR_GRE_1970_leadership_decisions.txt']
    choices = [(int(category.rsplit('_', 1)[1]), key, value) for category, op, body in decisions for key, op, value in body]
    assert len(choices) == 31
    sprites = {unquote(first(v, 'name')): unquote(first(v, 'texturefile'))
               for k, op, v in first(asts['interface/COLDWAR_GRE_1970_leadership.gfx'], 'spriteTypes') if k == 'spriteType'}
    loc_keys = set()
    for path in (ROOT / 'localisation/english').glob('COLDWAR_GRE_1970_leadership*.yml'):
        loc_keys.update(re.findall(r'^\s+(\S+):0 ', path.read_text(encoding='utf-8-sig'), re.M))
    assert set(chars) <= loc_keys
    for slot, key, choice in choices:
        assert key in loc_keys and key + '_desc' in loc_keys
        assert first(choice, 'icon') in sprites
        with Image.open(ROOT / sprites[first(choice, 'icon')]) as icon:
            assert icon.size == (33, 30)
    old_focus = asts['common/national_focus/COLDWAR_GRE_1970_focus.txt']
    for key, op, body in first(old_focus, 'focus_tree'):
        if key == 'focus':
            ident = first(body, 'id')
            section = next((name for name in ('nd', 'centre', 'pasok', 'kke') if ident.startswith(P + name + '_')), None)
            if section:
                required = PARTY_TRIGGERS[{'nd': 1, 'centre': 2, 'pasok': 3, 'kke': 4}[section]]
                available = first(body, 'available', [])
                assert (required, '=', 'yes') in list(walk(available)), ident
                assert not any(k == 'has_country_leader' for k, op, v in walk(available)), ident
    personal = (ROOT / 'common/national_focus/COLDWAR_GRE_1970_focus.txt').read_text(encoding='utf-8')
    assert 'name = "Georgios Papadopoulos"' in personal and 'name = "Dimitrios Ioannidis"' in personal
    cases = []
    for when in ((1970, 1, 1), (1980, 1, 1), (1990, 1, 1), (1999, 12, 31)):
        for slot, key, choice in choices:
            assert first(choice, 'cost') == '0'
            assert first(choice, 'fire_only_once') == 'no'
            assert not any(k in ('date', 'has_completed_focus') for k, op, v in walk(choice))
            m = Model(effects, party=slot, when=when)
            m.effect(P + 'initialize')
            execution = first(choice, 'complete_effect')
            current = m.leader
            if m.condition(first(choice, 'available')):
                m.run(execution)
            name = unquote(next(v for k, op, v in walk(first(choice, 'available')) if k == 'name'))
            assert m.leader == name, (key, m.leader, name)
            assert m.party == slot and m.variables['ruling_party'] == slot
            before = m.creations
            m.run(execution)
            assert m.creations == before, ('repeat', key)
            m.effect(P + 'initialize')
            assert m.leader == name and m.creations == before, ('monthly reset', key)
            for label, kwargs in (('wrong_country', {'tag': 'TUR'}), ('other_bookmark', {'scenario': False}),
                                  ('AI', {'human': False}), ('wrong_party', {'party': (slot + 1) % 24})):
                other = Model(effects, **kwargs)
                other.leader = 'Incumbent'
                other.run(execution)
                assert other.leader == 'Incumbent' and other.creations == 0, (key, label)
            cases.append({'choice': key, 'date': '.'.join(map(str, when)), 'selected': name, 'duplicate': 'no-op'})
    # Separate party memories, including a person present in two party lists.
    m = Model(effects, party=1)
    m.effect(P + 'initialize')
    m.effect(P + 'choose_1_mitsotakis_effect')
    m.party = m.variables['ruling_party'] = 2
    m.effect(P + 'set_leader')
    m.effect(P + 'choose_2_mavros_effect')
    m.party = m.variables['ruling_party'] = 3
    m.effect(P + 'set_leader')
    m.effect(P + 'choose_3_simitis_effect')
    m.party = m.variables['ruling_party'] = 1
    m.effect(P + 'set_leader')
    assert m.leader == 'Konstantinos Mitsotakis'
    # A legacy focus selection can deliberately replace the remembered candidate.
    m.flags.add(P + 'selected_karamanlis')
    m.effect(P + 'set_leader')
    assert m.leader == 'Konstantinos Karamanlis'
    modern = Model(effects, scenario=False)
    modern.leader = 'Modern incumbent'
    modern.effect(P + 'initialize')
    assert modern.leader == 'Modern incumbent' and not modern.characters
    hooks = (ROOT / 'common/on_actions/COLDWAR_GRE_1970_regional_on_actions.txt').read_text(encoding='utf-8')
    assert 'on_daily' not in hooks and 'on_weekly' not in hooks and 'on_monthly' in hooks
    assert 'every_country' not in str(effects) and 'every_state' not in str(effects)
    assert all(k not in ('add_political_power', 'add_manpower', 'add_equipment_to_stockpile', 'kill_country_leader')
               for key, tree in effects.items() for k, op, v in walk(tree))
    # Rebuild in place is bounded to the explicit owned outputs and must be byte-stable.
    process = subprocess.run([sys.executable, str(HERE / 'build.py')], capture_output=True, text=True)
    assert process.returncode == 0, process.stderr
    assert all(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == digest for rel, digest in hashes.items()), 'Non-idempotent regeneration'
    report = {'project': 'IMPERIA COLD WAR', 'status': 'pass', 'characters': len(chars),
        'unique_political_candidates': len({r['key'] for r in roster if r['slots']}),
        'party_candidate_choices': len(choices), 'calendar_choice_cases': len(cases), 'cases': cases,
        'guards': ['wrong country', 'other bookmark', 'AI selection', 'wrong party', 'duplicate click'],
        'party_memory': 'pass, including overlapping party eligibility', 'legacy_focus_selection': 'pass',
        'party_focus_access': 'Conservative, Centre, socialist and left availability uses the native party trigger; personal junta and royal gates retained.',
        'portrait_and_icon_references': 'pass',
        'byte_stable_regeneration': True, 'monthly_only': True, 'output_hashes': hashes,
        'limits': 'Static parsing and interpreted custom script only. Native portrait rendering, MD trait application, programme callback behavior, multiplayer and save/rehost remain unobserved.'}
    (HERE / 'VALIDATION.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('cases', 'output_hashes')}))


if __name__ == '__main__':
    main()
