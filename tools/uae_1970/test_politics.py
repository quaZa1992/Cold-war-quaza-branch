# IMPERIA CW — Cold War: uae 1970 — test politics.
"""Execute emitted political AST at native API boundaries, without HOI4.

The native economic calibration/UI are outside this model. Their source-order
contracts are checked separately. Unsupported authored statements fail loudly.
"""
import copy
import json
from pathlib import Path
import re
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/vietnam_1970'))
from script_ast import parse, first, walk
import politics

from revision import current_design
DATA = current_design()
OUTPUTS = politics.build(DATA)
E = dict((k, v) for k, _, v in parse(OUTPUTS['common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt']))
T = dict((k, v) for k, _, v in parse(OUTPUTS['common/scripted_triggers/COLDWAR_UAE_1970_politics_triggers.txt']))
P = 'COLDWAR_UAE_'


class Country:
    def __init__(self, date='1970.1.1', tag='UAE', scenario=True, dynamic=False):
        self.date, self.tag, self.scenario, self.dynamic = date, tag, scenario, dynamic
        self.variables = {'ruling_party': 0, 'treasury': 0.2}
        self.flags, self.ideas, self.global_flags = set(), set(), set()
        self.leader, self.subject = 'Trucial States Council', 'ENG'
        self.resources = {179: 7, 180: 40}
        self.states = {179: ('UAE', 'UAE'), 180: ('UAE', 'UAE')}
        self.refreshes = self.kills = self.installs = 0
        self.elections = False
        self.outlook, self.cosmetic = 'democratic', 'UAE_TRUCIAL_1970'
        self.portrait = None
        self.leader_ideology = 'Western_Autocracy'
        self.traits = {'western_Western_Autocracy'}
        self.popularities = {}
        self.trace = []

    def number(self, value):
        try: return float(value)
        except (ValueError, TypeError): return self.variables.get(value, 0)

    def test(self, rows):
        return all(self.condition(k, o, v) for k, o, v in rows)

    def condition(self, key, op, value):
        if key in {'AND', 'limit'}: return self.test(value)
        if key == 'OR': return any(self.condition(k, o, v) for k, o, v in value)
        if key == 'NOT': return not self.test(value)
        if key in T: return self.test(T[key]) == (value == 'yes')
        if key == 'original_tag': return self.tag == value
        if key == 'IMP_is_1970_scenario': return self.scenario == (value == 'yes')
        if key == 'is_dynamic_country': return self.dynamic == (value == 'yes')
        if key == 'has_country_flag': return value in self.flags
        if key == 'has_global_flag': return value in self.global_flags
        if key == 'has_country_leader_with_trait': return value in self.traits
        if key == 'has_government': return self.outlook == value
        if key == 'has_variable': return value in self.variables
        if key == 'has_idea': return value in self.ideas
        if key == 'is_subject': return bool(self.subject) == (value == 'yes')
        if key == 'is_subject_of': return self.subject == value
        if key == 'var:overlord_to_match': return self.variables.get('overlord_to_match') == first(value, 'tag')
        if key == 'has_cosmetic_tag': return self.cosmetic == value
        if key == 'salafist_caliphate_are_in_power': return (self.variables.get('ruling_party') == 11) == (value == 'yes')
        if key in {'owns_state', 'controls_state'}: return self.states[int(value)][0 if key == 'owns_state' else 1] == self.tag
        if key == 'has_country_leader': return self.leader == first(value, 'name').strip('"')
        if key == 'date':
            a, b = tuple(map(int, self.date.split('.'))), tuple(map(int, value.split('.')))
            return {'>': a > b, '<': a < b, '=': a == b}[op]
        if key == 'check_variable':
            k, o, v = value[0]
            a, b = self.number(k), self.number(v)
            return {'>': a > b, '<': a < b, '=': a == b}[o]
        raise AssertionError('Unmodelled trigger ' + key)

    def execute(self, rows, state=None):
        branch = False
        for k, o, v in rows:
            if k == 'if':
                branch = self.test(first(v, 'limit', []))
                if branch: self.execute([r for r in v if r[0] != 'limit'], state)
                continue
            if k == 'else_if':
                if not branch:
                    branch = self.test(first(v, 'limit', []))
                    if branch: self.execute([r for r in v if r[0] != 'limit'], state)
                continue
            if k == 'else':
                if not branch: self.execute(v, state)
                branch = False
                continue
            branch = False
            if k in E: self.execute(E[k], state)
            elif k.isdigit(): self.execute(v, int(k))
            elif k in {'set_variable', 'set_temp_variable'}:
                for var, _, operand in v: self.variables[var] = self.number(operand)
            elif k == 'set_country_flag': self.flags.add(v)
            elif k == 'clr_country_flag': self.flags.discard(v)
            elif k == 'add_resource': self.resources[state] += int(first(v, 'amount'))
            elif k == 'kill_country_leader': self.leader = None; self.kills += 1
            elif k == 'create_country_leader':
                self.leader = first(v, 'name').strip('"'); self.installs += 1
                self.portrait = first(v, 'picture', '').strip('"')
                self.leader_ideology = first(v, 'ideology')
                self.traits = {value for _, _, value in first(v, 'traits', [])}
            elif k == 'add_ideas':
                if v == P + 'dirham_currency':
                    self.ideas.difference_update({'british_pound', 'us_dollar', 'no_foreign_reserve'})
                self.ideas.add(v)
            elif k == 'remove_ideas': self.ideas.discard(v)
            elif k == 'set_politics':
                self.elections = first(v, 'elections_allowed') == 'yes'
                self.outlook = first(v, 'ruling_party', self.outlook)
            elif k == 'set_popularities': self.popularities = {key: float(amount) for key, _, amount in v}
            elif k == 'start_politics_input':
                # Native boundary: input clears existing politics, it creates no leader.
                self.variables = {key: value for key, value in self.variables.items()
                                  if not key.startswith(('party_pop_array^', 'party_pop_elect_array^', 'pos_array^', 'party_banned_array^')) and key != 'ruling_party'}
            elif k == 'set_cosmetic_tag': self.cosmetic = v
            elif k == 'drop_cosmetic_tag': self.cosmetic = None
            elif k == 'set_party_name': self.trace.append(k)
            elif k == 'COLDWAR_UAE_refresh_programmes': self.refreshes += 1
            elif k in {'update_set_politics', 'set_correct_ideology_trait', 'startup_politics',
                       'update_dirty_politicsview_expanded', 'calculate_reserve_roi_bonus', 'refresh_currency_inflation_effects',
                       'COLDWAR_UAE_startup_industry'}:
                # The industrial baseline has its own emitted-AST regression
                # suite, test_start_economy.py; this harness covers politics/oil.
                self.trace.append(k)  # Verified native boundaries, no model of global UI/economy.
            else: raise AssertionError('Unmodelled effect ' + k)

    def call(self, name): self.execute(E[P + name])


def run():
    checks = []
    def passed(text): checks.append(text)
    history = OUTPUTS['history/countries/UAE - United Arab Emirates.txt']
    snapshot = first(parse(history), '1970.1.1')
    direct_history = [row for row in snapshot if row[0] != 'if']
    # Country selection must have the historical identity even when scenario
    # predicates are unavailable; no startup effect is needed to install it.
    c = Country(scenario=False); c.variables = {}; c.leader = None; c.cosmetic = None
    c.execute(direct_history)
    assert c.leader == 'Trucial States Council' and c.leader_ideology == 'Western_Autocracy'
    assert c.portrait == 'gfx/leaders/UAE/UAE_Coldwar_Trucial_States_Council.dds'
    assert c.outlook == 'democratic' and c.variables['ruling_party'] == 0
    assert c.variables['party_pop_array^0'] == .54 and c.variables['party_pop_array^23'] == .05 and c.cosmetic == 'UAE_TRUCIAL_1970'
    assert c.traits == {'western_Western_Autocracy'} and c.popularities == dict(democratic=61, communism=4, fascism=2, neutrality=22, nationalist=11)
    assert abs(sum(value for key, value in c.variables.items() if key.startswith('party_pop_array^')) - 1) < 1e-9
    assert 'IMP_1970_profile_monarchist' not in str(snapshot) and 'startup_politics' not in str(snapshot)
    passed('History alone installs Council, portrait, native Western_Autocracy slot0 and trait, balanced preserved support, and Trucial name without startup/scenario-preview predicates')

    c = Country(); c.call('apply_starting_politics')
    assert c.variables['ruling_party'] == 0 and c.variables['party_pop_array^0'] == .54 and c.variables['party_pop_array^23'] == .05
    assert c.outlook == 'democratic' and c.popularities['democratic'] == 61 and 'startup_politics' in c.trace
    c = Country(scenario=False); c.variables['ruling_party'] = 18; c.call('apply_starting_politics'); assert c.variables['ruling_party'] == 18
    passed('UAE-only world startup uses the same corrected historical Western profile; later starts are excluded')

    native = parse(OUTPUTS['common/scripted_effects/00_MD_politicsview_scripted_effects.txt'])
    matcher = first(native, 'effect_puppet_match_ruling_party_to_overlord')
    match_limit = first(first(matcher, 'if'), 'limit')
    c = Country(); c.variables['overlord_to_match'] = 'ENG'
    assert not c.test(match_limit)
    for date, treaty in [('1971.1.1', 'withdrawal_schedule_active'), ('1975.1.1', 'protection_accepted')]:
        c.date = date; c.flags = {P + treaty}; c.variables['ruling_party'] = 1
        assert not c.test(match_limit) and c.variables['ruling_party'] == 1
    c.variables['overlord_to_match'] = 'FRA'; assert c.test(match_limit)
    c.variables['overlord_to_match'] = 'ENG'; c.subject = 'FRA'; assert c.test(match_limit)
    c.subject = 'ENG'; c.flags.add(P+'federation_formed'); assert c.test(match_limit)
    c.flags.clear(); assert c.test(match_limit)  # Later non-treaty puppeting.
    for params in [dict(tag='BHR'), dict(scenario=False), dict(dynamic=True)]:
        c = Country(**params); c.variables['overlord_to_match'] = 'ENG'; assert c.test(match_limit)
    passed('Native puppet matcher preserves domestic parties only under UAE1970 British treaty protection; other subjects, overlords, starts and later non-treaty puppeting remain native')

    for tag in ['BHR','QAT','BRU','TON']:
        c = Country(tag=tag); c.global_flags.add('COLDWAR_1970_initial_treaty_setup'); c.variables['overlord_to_match'] = 'ENG'
        assert not c.test(match_limit)
        c.global_flags.clear(); assert c.test(match_limit)
        c.global_flags.add('COLDWAR_1970_initial_treaty_setup'); c.subject = 'USA'; assert c.test(match_limit)
        c.subject = 'ENG'; c.variables['overlord_to_match'] = 'USA'; assert c.test(match_limit)
        c.variables['overlord_to_match'] = 'ENG'; c.dynamic = True; assert c.test(match_limit)
        c.dynamic = False; c.scenario = False; assert c.test(match_limit)
    c = Country(tag='OMA'); c.global_flags.add('COLDWAR_1970_initial_treaty_setup'); c.variables['overlord_to_match'] = 'ENG'; assert c.test(match_limit)
    passed('Initial British treaty exemption is limited to BHR/QAT/BRU/TON under the active setup flag, actual/intended ENG overlord, original static tags and 1970 scenario; later puppeting stays native')

    actions = first(parse(OUTPUTS['common/on_actions/00_on_actions.txt']), 'on_actions')
    government = first(first(actions, 'on_government_change'), 'effect')
    gulf = next(body for key, _, body in walk(government) if key == 'if' and
                first(body, 'drop_cosmetic_tag') == 'yes' and
                ('original_tag', '=', 'UAE') in list(walk(first(body, 'limit', []))))
    c = Country(); assert not c.test(first(gulf, 'limit'))
    c.flags.add(P+'federation_formed'); assert c.test(first(gulf, 'limit'))
    c = Country(scenario=False); assert c.test(first(gulf, 'limit'))
    c = Country(tag='SAU'); assert c.test(first(gulf, 'limit'))
    c = Country(); c.subject = None
    c.call('form_federation')
    assert c.cosmetic == 'UAE_TRUCIAL_1970' and c.leader == 'Trucial States Council'
    c.flags.update({P+'done_sovereign_union', P+'done_proclaim_federation', P+'founders_consented'})
    c.call('form_federation')
    assert c.cosmetic is None and c.leader == 'Zayed bin Sultan Al Nahyan'
    passed('Native government-change callback preserves Trucial identity until actual formation; formation drops it, other Gulf countries/later starts retain normal behaviour')

    c = Country(); c.call('startup_pre_economy'); assert c.resources == {179: 1, 180: 3}
    c.call('startup_pre_economy'); assert c.resources == {179: 1, 180: 3}
    c.resources[180] += 8; c.date = '1975.1.1'; c.call('startup_pre_economy'); assert c.resources[180] == 11
    passed('Fresh startup reduces 47 to 4 raw oil exactly once; later expansion/load is preserved')
    for params in [dict(scenario=False), dict(tag='OMA'), dict(dynamic=True), dict(date='1985.1.1')]:
        c = Country(**params); c.call('startup_pre_economy'); assert c.resources == {179: 7, 180: 40}
    c = Country(); c.flags.add('IMP_1970_gdp_profile_applied'); c.call('startup_pre_economy'); assert c.resources == {179:7,180:40}
    passed('Other countries, later starts, dynamic tags and calibrated existing saves never receive raw-resource resets')
    c = Country(); c.date = '1972.1.1'; c.call('politics_init'); c.call('politics_tick')
    assert c.leader == 'Trucial States Council' and not any('president' in f for f in c.flags)
    c.flags.update({P+'done_sovereign_union', P+'done_proclaim_federation', P+'founders_consented'})
    c.call('form_federation'); assert P + 'federation_formed' not in c.flags
    passed('1971 date expiry cannot create a president; a still-protected Council cannot form sovereign federation')
    c.flags.remove(P+'done_proclaim_federation')
    c.subject = None; c.call('form_federation')
    assert c.cosmetic == 'UAE_TRUCIAL_1970' and c.leader == 'Trucial States Council'
    c.flags.update({P+'done_sovereign_union', P+'done_proclaim_federation', P+'founders_consented'})
    c.call('form_federation')
    assert c.leader == 'Zayed bin Sultan Al Nahyan' and {P+'federation_formed',P+'federation_established',P+'zayed_president'} <= c.flags
    assert P+'prime_minister_maktoum' in c.ideas and P+'prime_minister_rashid' not in c.ideas
    assert c.leader_ideology == 'Western_Autocracy' and c.traits == {'king','western_Western_Autocracy'}
    c.call('accept_cabinet_bargain'); assert c.leader == 'Zayed bin Sultan Al Nahyan' and P+'prime_minister_rashid' in c.ideas and P+'cabinet_active' in c.flags
    passed('Actual formation creates Zayed presidency; the cabinet bargain installs Rashid in a separate premiership')
    c.variables['MDCW_HP_native_retirement'] = 1; c.call('set_leader'); c.variables['MDCW_HP_native_retirement'] = 0
    assert c.leader == 'Rashid bin Saeed Al Maktoum' and P+'rashid_president' in c.flags and P+'prime_minister_rashid' not in c.ideas and P+'cabinet_active' not in c.flags
    for slot, expected in politics.LEADERS.items():
        c.variables['ruling_party'] = slot; c.call('set_leader'); assert c.leader == expected
    c.variables['ruling_party'] = 23; c.call('set_leader'); assert c.leader == 'Rashid bin Saeed Al Maktoum'
    assert c.leader_ideology == 'Monarchist' and c.traits == {'king','nationalist_Monarchist'}
    c.variables['ruling_party'] = 0; c.call('politics_tick')
    assert c.leader == 'Rashid bin Saeed Al Maktoum' and c.leader_ideology == 'Western_Autocracy'
    assert c.traits == {'king','western_Western_Autocracy'}
    c.variables['ruling_party'] = 23; c.call('politics_tick')
    assert c.leader_ideology == 'Monarchist' and c.traits == {'king','nationalist_Monarchist'}
    c2 = copy.deepcopy(c); installs = c2.installs; c2.call('politics_init'); c2.call('politics_tick')
    assert c2.leader == c.leader and c2.installs == installs
    passed('Native retirement selects eligible alternate president; all approved subparties receive era-appropriate collective providers; return/reload preserves presidency')
    passed('Western and nationalist dynastic governments share earned institutions and historical officeholders but preserve distinct native ideologies and traits even when the officeholder name is unchanged')
    for date, expected in [('1990.10.7','Zayed bin Sultan Al Nahyan'),('2004.11.2','Khalifa bin Zayed Al Nahyan'),('2022.5.13','Mohammed bin Zayed Al Nahyan')]:
        c.date = date; c.call('politics_tick'); assert c.leader == expected
    passed('Historical death dates prevent resurrection in long-running 1970 campaigns')
    c = Country(); c.variables['ruling_party'] = 12
    assert not c.test(T[P+'islah_government'])
    c.call('organise_association'); assert c.test(T[P+'islah_government'])
    c.variables['ruling_party'] = 23; assert not c.test(T[P+'islah_government'])
    oldslot = c.variables['ruling_party']; c.call('convene_constitution')
    assert c.elections and c.variables['ruling_party'] == oldslot and all(c.variables['party_banned_array^'+str(s)] == 0 for s in [0,1,2,4,7,18,22,23])
    passed('Recognition gates Islah; convention uses native election/ban arrays without forcing governing party or 100% popularity')
    c = Country(); c.ideas.add('british_pound'); c.call('establish_dirham')
    assert P+'dirham_currency' in c.ideas and 'british_pound' not in c.ideas and c.variables['no_foreign_reserve'] == 1
    c.ideas.remove(P+'dirham_currency'); c.ideas.add('us_dollar'); c.call('establish_dirham'); assert c.ideas == {'us_dollar'}
    passed('Dirham adoption replaces the native currency law once; reload cannot undo later currency choices')
    startup = OUTPUTS['common/on_actions/00_on_actions.txt']
    assert startup.index('COLDWAR_UAE_startup_pre_economy = yes') < startup.index('startup_politics = yes') < startup.index('IMP_communist_struggle_startup_after_native_money = yes')
    dispatcher = OUTPUTS['common/scripted_effects/00_leader_setup_scripted_effects.txt']
    assert dispatcher.index('COLDWAR_UAE_set_leader = yes') < dispatcher.index('kill_country_leader = yes')
    relationships = OUTPUTS['common/scripted_effects/IMP_1970_world_politics_effects.txt']
    assert relationships.index('set_autonomy = { target = UAE autonomy_state = autonomy_puppet_state }') < relationships.index('UAE = { COLDWAR_UAE_init_british = yes }') < relationships.index('set_autonomy = { target = BRU')
    world_uae = next(body for key, _, body in walk(parse(relationships)) if key == 'else_if' and first(body, 'limit') == [('original_tag','=','UAE')])
    world_council = first(world_uae, 'create_country_leader')
    assert first(world_council, 'expire') is None and first(world_council, 'ideology') == 'Western_Autocracy'
    assert first(world_uae, 'COLDWAR_UAE_apply_starting_politics') == 'yes' and first(world_uae, 'IMP_1970_profile_monarchist') is None
    assert first(E[P+'startup_pre_economy'][0][2], 'COLDWAR_UAE_refresh_programmes') == 'yes'
    for rel, expected in [('history/states/179-Dubai.txt',7), ('history/states/180-Abu Dhabi.txt',40)]:
        assert first(first(parse((ROOT/rel).read_text(encoding='utf-8-sig')), 'state'), 'resources') is not None
        assert int(first(first(first(parse((ROOT/rel).read_text(encoding='utf-8-sig')), 'state'), 'resources'), 'oil')) == expected
    history = OUTPUTS['history/countries/UAE - United Arab Emirates.txt']
    assert 'expire' not in history.split('2000.1.1 = {')[0] and 'UAE_MDCW_1970_incumbent' not in history
    original_tail = (ROOT/'history/countries/UAE - United Arab Emirates.txt').read_text(encoding='utf-8-sig').replace('\r\n','\n').split('2000.1.1 = {',1)[1]
    assert history.split('2000.1.1 = {',1)[1] == original_tail
    for slot, token in politics.SLOTS.items():
        registry = OUTPUTS['common/scripted_localisation/mdcw_historical_parties.txt']
        for tail in ['', '_desc', '_icon']:
            section = registry.split('\tname = MDCW_HP_' + token + tail + '\n',1)[1].split('defined_text = {',1)[0]
            assert section.index('COLDWAR_UAE_party_' + str(slot) + tail) < section.index('MDCW_HP_generic_')
    party_localisation = OUTPUTS['localisation/english/COLDWAR_UAE_1970_politics_l_english.yml']
    for slot, inline in politics.native_party_text_icons().items():
        assert f'COLDWAR_UAE_party_{slot}_icon:0 "{inline}"' in party_localisation
    assert '£generic_Communist_State_small' in party_localisation and '£generic_communist_state_small' not in party_localisation
    passed('Source contracts: pre-GDP bootstrap, pre-kill routing, Council no-expiry, all later history unchanged, registry priority before fallbacks')
    passed('All nine party inline icons resolve through exact native MD_texticons registrations and existing DDS files, including case-sensitive Communist_State')
    for path, text in OUTPUTS.items():
        if path.endswith('.txt'): parse(text)
    passed('Every owned or narrowly patched Clausewitz output parses')
    # Compile a disposable tree twice to prove whole-file patches and the
    # before-hash manifest remain stable after actual installation.
    old_root, old_here = politics.ROOT, politics.HERE
    try:
        # The resolved, explicitly named workspace directory bounds cleanup.
        assert HERE.resolve().is_relative_to(ROOT.resolve())
        with tempfile.TemporaryDirectory(prefix='politics_test_', dir=HERE.resolve()) as tmp:
            politics.ROOT = Path(tmp); politics.HERE = Path(tmp)/'tools/uae_1970'
            politics.HERE.mkdir(parents=True)
            native_texticons = old_root / 'interface/MD_texticons.gfx'
            needed_sprites = set(politics.PARTY_TEXT_ICONS.values())
            native_icons = dict(re.findall(r'name\s*=\s*"([^"]+)"[^}]*?texturefile\s*=\s*"([^"]+)"', native_texticons.read_text(encoding='utf-8-sig'), re.I))
            for path in ['interface/MD_texticons.gfx'] + [native_icons[sprite] for sprite in needed_sprites]:
                target = politics.ROOT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes((old_root/path).read_bytes())
            for path in OUTPUTS:
                source = old_root/path
                if source.exists() and path != 'tools/uae_1970/politics_shared_integrations.json':
                    target = politics.ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
            first_build = politics.build(DATA)
            for path, text in first_build.items():
                target = politics.ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf8')
            second_build = politics.build(DATA)
            assert first_build == second_build, [p for p in first_build if first_build[p] != second_build[p]]
    finally: politics.ROOT, politics.HERE = old_root, old_here
    passed('Installed shared patches and before/after hash manifest are byte-stable on rebuild')
    print(json.dumps({'politics_ast_checks':len(checks),'checks':checks,'limit':'Native APIs and actual HOI4 UI/economy/multiplayer behaviour require engine testing.'},indent=2))


if __name__ == '__main__': run()
