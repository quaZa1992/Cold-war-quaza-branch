# IMPERIA COLD WAR — execute the actual intelligence effects at their scope boundaries.
from dataclasses import dataclass, field
from decimal import Decimal as D
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first


@dataclass(eq=False)
class Scope:
    tag: str
    id: int
    kind: str = 'country'
    vars: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)
    ideas: set = field(default_factory=set)
    techs: set = field(default_factory=set)
    projects: set = field(default_factory=set)
    completed: set = field(default_factory=set)
    upgrades: set = field(default_factory=set)
    networks: dict = field(default_factory=dict)
    neighbors: list = field(default_factory=list)
    agency: bool = False
    defense: D = D(0)
    owner: object = None
    controller: object = None
    level: int = 0
    queued: bool = False


class Model:
    def __init__(self):
        self.effects = dict((k, v) for k, _, v in parse((ROOT / 'common/scripted_effects/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')))
        self.triggers = dict((k, v) for k, _, v in parse((ROOT / 'common/scripted_triggers/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')))
        self.c = {t: Scope(t, i + 1) for i, t in enumerate(('PER', 'USA', 'SOV', 'ENG', 'FRA', 'CHI', 'TUR', 'JAP', 'BRA'))}
        self.g = Scope('global', 0, 'global')
        self.s = [Scope(str(i), i, 'state', owner=self.c['PER'], controller=self.c['PER']) for i in (100, 101)]
        self.day = 0
        self.rolls = []
        self.roll_count = 0
        self.events = []
        self.visits = 0
        self.from_scope = None

    def scope(self, name, cur, root, prev):
        if name == 'FROM':
            return self.from_scope
        if name in ('THIS', 'ROOT', 'PREV', 'OWNER', 'CONTROLLER'):
            return {'THIS': cur, 'ROOT': root, 'PREV': prev, 'OWNER': cur.owner, 'CONTROLLER': cur.controller}[name]
        return self.c.get(name)

    def key(self, key, cur, root, prev):
        if '@' in key:
            name, target = key.rsplit('@', 1)
            obj = self.scope(target, cur, root, prev)
            return name + '@' + (obj.tag if obj is not None else target)
        return key

    def variable(self, key, cur, root, prev):
        if key.startswith('global.'):
            return self.g, key[7:]
        if '.' in key:
            prefix, fieldname = key.split('.', 1)
            return self.scope(prefix, cur, root, prev), self.key(fieldname, cur, root, prev)
        return cur, self.key(key, cur, root, prev)

    def value(self, key, cur, root, prev):
        try:
            return D(key)
        except Exception:
            pass
        if key.endswith('.id'):
            return D(self.scope(key[:-3], cur, root, prev).id)
        if key == 'building_level@enrichment_facility':
            return D(cur.level)
        if key == 'modifier@intelligence_agency_defense':
            return cur.defense
        obj, key = self.variable(key, cur, root, prev)
        return obj.vars.get(key, D(0))

    @staticmethod
    def compare(a, op, b):
        return {'=': lambda: a == b, '>': lambda: a > b, '<': lambda: a < b, '>=': lambda: a >= b, '<=': lambda: a <= b}[op]()

    def condition(self, rows, cur, root, prev=None):
        def test(k, op, v):
            if k in self.triggers:
                return self.condition(self.triggers[k], cur, root, prev) == (v == 'yes')
            if k in ('OR', 'AND', 'NOT'):
                values = [test(*r) for r in v]
                return any(values) if k == 'OR' else all(values) if k == 'AND' else not any(values)
            if k == 'check_variable':
                a, cmp, b = v[0]
                return self.compare(self.value(a, cur, root, prev), cmp, self.value(b, cur, root, prev))
            if k == 'has_country_flag' or k == 'has_state_flag':
                key = self.key(v, cur, root, prev)
                return key in cur.flags and cur.flags[key] > self.day
            if k == 'has_global_flag':
                return v in self.g.flags and self.g.flags[v] > self.day
            if k in ('has_idea', 'has_tech'):
                return v in (cur.ideas if k == 'has_idea' else cur.techs)
            if k == 'exists':
                return v == 'yes'
            if k in ('tag', 'original_tag'):
                return cur is self.scope(v, cur, root, prev)
            if k == 'is_neighbor_of':
                return self.scope(v, cur, root, prev) in cur.neighbors
            if k == 'has_intelligence_agency':
                return cur.agency == (v == 'yes')
            if k == 'network_strength':
                target = self.scope(first(v, 'target'), cur, root, prev)
                cmp = next(o for a, o, b in v if a == 'value')
                return self.compare(cur.networks.get(target.tag, D(0)), cmp, D(first(v, 'value')))
            if k == 'is_special_project_being_researched':
                return v in cur.projects
            if k == 'is_special_project_completed':
                return v in cur.completed
            if k == 'has_done_agency_upgrade':
                return v in cur.upgrades
            if k == 'is_controlled_by':
                return cur.controller is self.scope(v, cur, root, prev)
            if k == 'enrichment_facility':
                count = cur.level if cur.kind == 'state' else sum(s.level for s in self.s if s.owner is cur)
                return self.compare(D(count), op, D(v))
            if k == 'free_building_slots':
                cmp = next(o for a, o, b in v if a == 'size')
                return self.compare(D(1 - cur.level), cmp, D(first(v, 'size')))
            if k == 'can_construct_building':
                return not cur.queued and cur.level == 0
            if k == 'is_in_array':
                array = first(v, 'array')
                if array is None:
                    array, _, value = v[0]
                else:
                    value = first(v, 'value')
                obj, name = self.variable(array, cur, root, prev)
                return self.value(value, cur, root, prev) in obj.vars.get(name, [])
            obj = self.scope(k, cur, root, prev)
            if obj is not None:
                return self.condition(v, obj, root, cur)
            raise AssertionError('Unsupported trigger ' + k)
        return all(test(*r) for r in rows)

    def execute(self, rows, cur, root, prev=None):
        chain = False
        for k, op, v in rows:
            if k in ('if', 'else_if', 'else'):
                if k == 'if':
                    chain = False
                if not chain and (k == 'else' or self.condition(first(v, 'limit', []), cur, root, prev)):
                    chain = True
                    self.execute([r for r in v if r[0] != 'limit'], cur, root, prev)
            elif k in self.effects:
                self.execute(self.effects[k], cur, root, prev)
            elif k in ('set_variable', 'set_temp_variable', 'add_to_variable', 'multiply_temp_variable', 'divide_temp_variable'):
                name, _, val = v[0]
                obj, name = self.variable(name, cur, root, prev)
                val = self.value(val, cur, root, prev)
                if k.startswith('set_'):
                    obj.vars[name] = val
                elif k.startswith('add_'):
                    obj.vars[name] = obj.vars.get(name, D(0)) + val
                elif k.startswith('multiply_'):
                    obj.vars[name] *= val
                else:
                    obj.vars[name] /= val
            elif k in ('set_country_flag', 'set_state_flag', 'set_global_flag'):
                obj = self.g if k == 'set_global_flag' else cur
                name = first(v, 'flag') if isinstance(v, list) else v
                duration = D(first(v, 'days', 999999)) if isinstance(v, list) else D(999999)
                obj.flags[self.key(name, cur, root, prev)] = self.day + duration
            elif k in ('clr_country_flag', 'clr_state_flag'):
                cur.flags.pop(self.key(v, cur, root, prev), None)
            elif k == 'set_temp_variable_to_random':
                self.roll_count += 1
                cur.vars[first(v, 'var')] = D(self.rolls.pop(0) if self.rolls else 9999)
            elif k == 'country_event':
                self.events.append((cur.tag, root.tag, first(v, 'id')))
            elif k in ('every_owned_state', 'every_country', 'every_neighbor_country', 'for_each_scope_loop'):
                if k == 'every_owned_state':
                    candidates = [s for s in self.s if s.owner is cur]
                elif k == 'every_country':
                    candidates = list(self.c.values())
                elif k == 'every_neighbor_country':
                    candidates = cur.neighbors
                else:
                    obj, name = self.variable(first(v, 'array'), cur, root, prev)
                    candidates = [c for idx in obj.vars.get(name, []) for c in self.c.values() if c.id == idx]
                for obj in candidates:
                    self.visits += 1
                    if self.condition(first(v, 'limit', []), obj, root, cur):
                        self.execute([r for r in v if r[0] not in ('limit', 'array')], obj, root, cur)
            elif k == 'clear_array':
                obj, name = self.variable(v, cur, root, prev)
                obj.vars[name] = []
            elif k == 'add_to_array':
                name, _, value = v[0]
                obj, name = self.variable(name, cur, root, prev)
                obj.vars.setdefault(name, []).append(self.value(value, cur, root, prev))
            else:
                obj = self.scope(k, cur, root, prev)
                if obj is None:
                    raise AssertionError('Unsupported effect ' + k)
                self.execute(v, obj, root, cur)

    def run(self, name, observer='PER', programme=None):
        cur = self.c[observer]
        self.execute(self.effects[name], cur, self.c[programme] if programme else cur)


class IntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.m = Model()
        self.p = self.m.c['PER']
        self.p.techs.add('nuclear_technology')
        self.m.run('COLDWAR_NI_initialize_country')
        self.m.run('COLDWAR_NI_calculate_defense')

    def observe(self, who='ENG', roll=0):
        self.m.rolls = [roll]
        self.m.run('COLDWAR_NI_observe_programme', who, 'PER')

    def test_exact_category_rates_and_network_boundaries(self):
        c = self.m.c['TUR']
        c.neighbors = [self.p]
        self.m.run('COLDWAR_NI_observer_rates', 'TUR', 'PER')
        self.assertEqual((c.vars['COLDWAR_NI_enrichment_chance'], c.vars['COLDWAR_NI_weapons_chance']), (15, 10))
        c.agency = True
        for network, rates in [(D('49.99'), (15, 10)), (50, (30, 25)), (D('69.99'), (30, 25)), (70, (40, 40)), (90, (55, 55)), (100, (55, 55))]:
            c.networks['PER'] = D(network)
            self.m.run('COLDWAR_NI_observer_rates', 'TUR', 'PER')
            self.assertEqual((c.vars['COLDWAR_NI_enrichment_chance'], c.vars['COLDWAR_NI_weapons_chance']), rates)

    def test_great_power_rank_and_overlap_never_add(self):
        c = self.m.c['JAP']
        c.ideas.add('great_power')
        c.neighbors = [self.p]
        self.m.run('COLDWAR_NI_observer_rates', 'JAP', 'PER')
        self.assertEqual(c.vars['COLDWAR_NI_enrichment_chance'], 25)
        self.assertEqual(c.vars['COLDWAR_NI_weapons_chance'], 20)
        self.m.run('COLDWAR_NI_observer_rates', 'BRA', 'PER')
        self.assertEqual(self.m.c['BRA'].vars['COLDWAR_NI_enrichment_chance'], 0)

    def test_defense_reductions_use_target_not_observer(self):
        self.m.c['ENG'].defense = D(99)
        for defense, expected in [(0, ('25', '20')), (D('1.249'), ('25', '20')), (D('1.25'), ('21.25', '16')), (D('2.5'), ('18.75', '12')), (99, ('18.75', '12'))]:
            self.p.defense = D(defense)
            self.m.run('COLDWAR_NI_calculate_defense')
            self.m.run('COLDWAR_NI_observer_rates', 'ENG', 'PER')
            c = self.m.c['ENG']
            self.assertEqual((c.vars['COLDWAR_NI_enrichment_chance'], c.vars['COLDWAR_NI_weapons_chance']), tuple(map(D, expected)))

    def test_two_successes_are_private_and_cannot_share_a_month(self):
        self.m.run('COLDWAR_NI_mark_enrichment_expansion')
        self.observe()
        self.observe()
        self.assertEqual(self.m.roll_count, 1)
        self.assertEqual(self.m.events, [('ENG', 'PER', 'COLDWAR_NI.1')])
        self.assertFalse(self.m.c['SOV'].vars)
        self.m.day += 31
        self.observe()
        self.assertEqual(self.m.events[-1], ('ENG', 'PER', 'COLDWAR_NI.2'))
        self.m.day += 31
        self.observe()
        self.assertEqual(self.m.roll_count, 2)

    def test_completed_passive_defense_is_supported_without_queued_cache(self):
        self.p.vars['agency_upgrades_completed_and_queued^3'] = D(4)
        self.m.run('COLDWAR_NI_calculate_defense')
        self.assertEqual(self.p.vars['COLDWAR_NI_weapons_defense_factor'], 1)
        self.p.vars['COLDWAR_NI_passive_defense_level'] = D(2)
        self.m.run('COLDWAR_NI_calculate_defense')
        self.assertEqual(self.p.vars['COLDWAR_NI_weapons_defense_factor'], D('.8'))
        self.p.upgrades.add('upgrade_passive_defense')
        self.m.run('COLDWAR_NI_calculate_defense')
        self.assertEqual(self.p.vars['COLDWAR_NI_weapons_defense_factor'], D('.6'))

    def test_new_expansion_reopens_dossier_but_keeps_known_capability(self):
        self.m.run('COLDWAR_NI_mark_enrichment_expansion')
        self.observe(); self.m.day += 31; self.observe()
        self.m.run('COLDWAR_NI_mark_enrichment_expansion')
        self.m.day += 31; self.observe()
        self.assertEqual(self.m.events[-1][-1], 'COLDWAR_NI.1')
        self.assertIn('COLDWAR_NI_enrichment_known@PER', self.m.c['ENG'].flags)

    def test_active_weapons_take_one_roll_and_do_not_confirm_arsenal(self):
        self.p.projects.add('sp:sp_nuclear_bomb')
        self.m.run('COLDWAR_NI_mark_enrichment_expansion')
        self.observe(); self.m.day += 31; self.observe()
        self.assertEqual([e[-1] for e in self.m.events], ['COLDWAR_NI.3', 'COLDWAR_NI.4'])
        self.assertEqual(self.m.roll_count, 2)
        self.assertIn('COLDWAR_NI_weapons_confirmed@PER', self.m.c['ENG'].flags)

    def test_probability_boundary_is_exact_and_failed_roll_does_not_notify(self):
        self.p.projects.add('sp:sp_nuclear_bomb')
        self.observe(roll=2000)
        self.assertFalse(self.m.events)
        self.m.day += 31
        self.observe(roll=1999)
        self.assertEqual(self.m.events[-1][-1], 'COLDWAR_NI.3')

    def test_cancelled_and_completed_work_stays_discoverable(self):
        self.m.run('COLDWAR_NI_record_weapons_work')
        self.observe(roll=999)  # 20% * 0.5 = 10% during the twelve-month trace.
        self.assertEqual(self.m.events[-1][-1], 'COLDWAR_NI.3')
        self.m.day = 400
        self.observe(roll=499)  # Residual archived work: 20% * 0.25 = 5%.
        self.assertEqual(self.m.events[-1][-1], 'COLDWAR_NI.4')

    def test_existing_enrichment_runs_at_quarter_rate(self):
        self.p.vars['COLDWAR_NI_facilities'] = D(1)
        self.observe(roll=625)
        self.assertFalse(self.m.events)
        self.m.day += 31
        self.observe(roll=624)
        self.assertEqual(self.m.events[-1][-1], 'COLDWAR_NI.1')

    def test_queue_completion_repair_and_transfer_receipts(self):
        state = self.m.s[0]
        state.queued = True
        self.m.run('COLDWAR_NI_update_enrichment')
        self.assertEqual(self.p.vars['COLDWAR_NI_enrichment_revision'], 1)
        self.assertIn('COLDWAR_NI_expansion_active', self.p.flags)
        self.m.run('COLDWAR_NI_update_enrichment')
        self.assertEqual(self.p.vars['COLDWAR_NI_enrichment_revision'], 1)
        state.queued = False; state.level = 1
        self.m.run('COLDWAR_NI_update_enrichment')
        self.assertEqual(self.p.vars['COLDWAR_NI_enrichment_revision'], 1)
        self.m.run('COLDWAR_NI_update_enrichment')  # Raw levels also stay unchanged on repair.
        self.assertEqual(self.p.vars['COLDWAR_NI_enrichment_revision'], 1)
        state.owner = state.controller = self.m.c['TUR']
        self.m.run('COLDWAR_NI_update_enrichment', 'TUR')
        self.assertNotIn('COLDWAR_NI_enrichment_revision', self.m.c['TUR'].vars)

    def test_initial_history_is_not_a_new_expansion(self):
        m = Model(); m.s[0].level = 1; m.c['PER'].techs.add('nuclear_technology')
        m.run('COLDWAR_NI_initialize_country'); m.run('COLDWAR_NI_update_enrichment')
        self.assertEqual(m.c['PER'].vars['COLDWAR_NI_facilities'], 1)
        self.assertNotIn('COLDWAR_NI_enrichment_revision', m.c['PER'].vars)

    def test_unrelated_agency_without_high_network_cannot_receive_reports(self):
        self.m.c['BRA'].agency = True
        self.m.c['BRA'].networks['PER'] = D('49.99')
        self.p.projects.add('sp:sp_nuclear_bomb')
        self.observe('BRA')
        self.assertEqual(self.m.roll_count, 0)
        self.assertFalse(self.m.events)

    def test_known_public_arsenal_does_not_generate_repeated_weapons_reports(self):
        self.p.ideas.add('nuclear_power_off')
        self.p.projects.add('sp:sp_nuclear_warhead_program')
        self.observe()
        self.assertEqual(self.m.roll_count, 0)

    def test_raid_requires_this_observers_own_enrichment_knowledge(self):
        self.m.from_scope = self.p
        self.m.run('COLDWAR_NI_enrichment_success', 'ENG', 'PER')
        trigger = self.m.triggers['COLDWAR_NI_enrichment_target_known']
        self.assertFalse(self.m.condition(trigger, self.m.c['ENG'], self.m.c['ENG']))
        self.m.run('COLDWAR_NI_enrichment_success', 'ENG', 'PER')
        self.assertTrue(self.m.condition(trigger, self.m.c['ENG'], self.m.c['ENG']))
        self.assertFalse(self.m.condition(trigger, self.m.c['SOV'], self.m.c['SOV']))

    def test_upgrade_hooks_only_count_completed_passive_branch(self):
        rows = parse((ROOT / 'common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt').read_text(encoding='utf-8'))
        branch = first(first(rows, 'branch_defense'), 'upgrade_passive_defense')
        levels = [v for k, _, v in branch if k == 'level']
        self.assertEqual(len(levels), 4)
        for index, level in enumerate(levels, 1):
            body = first(level, 'complete_effect')
            assignments = [v for k, _, v in body if k == 'set_variable' and v[0][0] == 'COLDWAR_NI_passive_defense_level']
            self.assertEqual(assignments[0][0][2], str(index))
        counterterror = first(first(rows, 'branch_defense'), 'upgrade_counter_terror_operations')
        self.assertNotIn('COLDWAR_NI_passive_defense_level', str(counterterror))

    def test_monthly_cache_and_neighbour_overlap_have_one_roll(self):
        hooks = first(parse((ROOT / 'common/on_actions/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')), 'on_actions')
        monthly = first(first(hooks, 'on_monthly'), 'effect')
        self.p.projects.add('sp:sp_nuclear_bomb')
        self.p.neighbors = [self.m.c['ENG'], self.m.c['TUR']]
        self.m.c['ENG'].neighbors = [self.p]
        self.m.c['TUR'].neighbors = [self.p]
        self.m.execute(monthly, self.p, self.p)
        self.assertEqual(self.m.roll_count, 6)  # Five named powers and one other neighbour.
        self.assertEqual(len(self.m.g.vars['COLDWAR_NI_observers']), 5)
        before = self.m.visits
        self.m.execute(monthly, self.m.c['BRA'], self.m.c['BRA'])
        self.assertEqual(self.m.visits, before)  # Cache reused; irrelevant country does no work.

    def test_encoding_event_bindings_and_no_daily_world_work(self):
        for rel in ('common/scripted_effects/COLDWAR_nuclear_intelligence.txt', 'common/scripted_triggers/COLDWAR_nuclear_intelligence.txt', 'common/on_actions/COLDWAR_nuclear_intelligence.txt', 'events/COLDWAR_nuclear_intelligence.txt', 'interface/COLDWAR_nuclear_intelligence.gfx'):
            raw = (ROOT / rel).read_bytes()
            self.assertFalse(raw.startswith(b'\xef\xbb\xbf'))
            parse(raw.decode('utf-8'))
        loc = (ROOT / 'localisation/english/COLDWAR_nuclear_intelligence_l_english.yml').read_bytes()
        self.assertTrue(loc.startswith(b'\xef\xbb\xbf'))
        text = loc.decode('utf-8-sig')
        for i in range(1, 5):
            for suffix in ('t', 'd', 'a'):
                self.assertEqual(len(re.findall(r'^ COLDWAR_NI\.' + str(i) + r'\.' + suffix + ':', text, re.M)), 1)
        hooks = (ROOT / 'common/on_actions/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')
        self.assertNotRegex(hooks, r'on_(daily|weekly)\s*=')
        effects = (ROOT / 'common/scripted_effects/COLDWAR_nuclear_intelligence.txt').read_text(encoding='utf-8')
        self.assertNotIn('every_state =', effects)
        self.assertNotIn('news_event =', effects)


if __name__ == '__main__':
    unittest.main(verbosity=2)
