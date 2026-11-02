# IMPERIA COLD WAR — PMC access, queued recruitment and native-cost regression tests.
"""Bounded source execution. Does not emulate HOI4 timers, UI rendering or netcode."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/colonial_affairs'))
from test_runtime import Model, Scope, D, parse, first
from patch import validate_reverse


def load(rel):
    return parse((ROOT/rel).read_text(encoding='utf-8-sig'))


class PMCModel(Model):
    def __init__(self):
        self.c = {tag:Scope(tag) for tag in ('GC','USA','SOV','ENG','FRA')}
        self.g = Scope('global','global')
        self.s = {'1':Scope('1','state')}
        self.root = self.c['FRA']
        self.start = '1970.1.1'
        self.date = '1970.1.1'
        self.saved_targets = {}
        self.events = []
        self.effects = dict((k,v) for k,o,v in load('common/scripted_effects/ICW_pmc_access.txt'))
        self.effects.update((k,v) for k,o,v in load('common/scripted_effects/02_pmc_scripted_effects.txt'))
        native = load('common/scripted_effects/01_international_systems_effects.txt')
        self.effects['international_systems_force_update'] = first(native,'international_systems_force_update')
        self.effects['international_systems_update'] = first(native,'international_systems_update')
        self.triggers = dict((k,v) for k,o,v in load('common/scripted_triggers/ICW_pmc_access.txt'))
        self.decisions = dict((k,v) for cat,o,rows in load('common/decisions/01_pmc_decisions.txt') for k,o,v in rows)
        for c in self.c.values():
            c.vars['treasury'] = D(100)
            c.missions = set()
            c.units = []
        self.c['GC'].ideas.add('imp_gc_nation')
        self.s['1'].owner = self.s['1'].controller = self.c['FRA']
        for k,o,v in self.effects['pmc_variables_setup']:
            if k=='add_to_array':
                self.g.vars[first(v,'array').removeprefix('global.')+'^'+first(v,'index')] = D(first(v,'value'))

    def condition(self,rows,current,root=None,prev=None):
        root = root or current
        for k,o,v in rows:
            if k=='has_start_date':
                ok = self.compare(tuple(map(int,self.start.split('.'))),o,tuple(map(int,v.split('.'))))
            elif k=='has_decision':
                ok = v in current.missions
            elif k=='has_full_control_of_state':
                ok = self.s['1'].owner is current and self.s['1'].controller is current
            else:
                ok = super().condition([(k,o,v)],current,root,prev)
            if not ok:return False
        return True

    def execute(self,rows,current,root,prev):
        last_if = None
        for k,o,v in rows:
            if k=='if':
                last_if = self.condition(first(v,'limit',[]),current,root,prev)
                if last_if:self.execute([r for r in v if r[0]!='limit'],current,root,prev)
            elif k=='else_if':
                if last_if is False:
                    last_if = self.condition(first(v,'limit',[]),current,root,prev)
                    if last_if:self.execute([r for r in v if r[0]!='limit'],current,root,prev)
            elif k=='else':
                if last_if is False:self.execute(v,current,root,prev)
                last_if = None
            elif k in ('set_global_flag','clr_global_flag'):
                self.g.flags.add(v) if k=='set_global_flag' else self.g.flags.discard(v)
            elif k in ('remove_mission','remove_decision'):
                current.missions.discard(v)
                # Exercise both cleanup callbacks to detect double-refund exposure.
                for key in ('cancel_effect','remove_effect'):
                    self.execute(first(self.decisions[v],key,[]),current,root,prev)
            elif k=='division_template':
                pass  # Template contents are checked by exact source reversal, not simulated.
            elif k=='random_owned_controlled_state':
                self.s['1'].owner = self.s['1'].controller = current
                self.execute([r for r in v if r[0] not in ('limit','prioritize')],self.s['1'],root,current)
            elif k=='create_unit':
                owner = self.scope(first(v,'owner'),current,root,prev)
                owner.units.append(re.search(r'division_template = \\"(.*?)\\"',first(v,'division')).group(1))
            elif k=='delete_unit_template_and_units':
                name = first(v,'division_template').strip('"')
                current.units[:] = [u for u in current.units if u!=name]
            elif k in ('country_event','news_event') and isinstance(v,str):
                self.events.append((v,current.id))
            else:
                super().execute([(k,o,v)],current,root,prev)


class Access(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = PMCModel()
        cls.record = json.loads((Path(__file__).with_name('changes.json')).read_text(encoding='utf-8'))
        cls.gui = first(load('common/scripted_guis/00_missiles_scripted_guis.txt'),'scripted_gui')

    def setUp(self):self.m = copy.deepcopy(self.template)

    def active(self):return self.m.condition([('ICW_pmc_system_active','=','yes')],self.m.root)

    def test_default_is_bound_to_the_2000_start_not_the_current_year(self):
        for start in ('1969.1.1','1970.1.1','1985.1.1','1999.1.1','2000.1.1','2001.1.1','2017.1.1'):
            with self.subTest(start=start):
                self.m.start = start
                self.m.date = '2030.1.1'
                self.assertEqual(self.active(),start=='2000.1.1')

    def test_gc_can_repeat_open_close_and_reopen_in_both_starts(self):
        for start in ('1970.1.1','2000.1.1'):
            self.m.start = start
            for _ in range(2):
                if self.active():self.m.run('ICW_pmc_gc_close',self.m.c['GC'])
                self.assertFalse(self.active())
                self.m.run('ICW_pmc_gc_open',self.m.c['GC'])
                self.assertTrue(self.active())
        restored = copy.deepcopy(self.m)
        self.assertTrue(restored.condition([('ICW_pmc_system_active','=','yes')],restored.root))

    def test_regular_players_and_ai_cannot_override_even_by_calling_the_effect(self):
        controls = first(load('common/decisions/ICW_pmc_access.txt'),'imp_gc_tools_decisions')
        for k,o,v in controls:
            self.assertEqual(first(v,'cost'),'0')
            self.assertEqual(first(first(v,'ai_will_do'),'factor'),'0')
            self.assertFalse(self.m.condition(first(v,'visible'),self.m.c['FRA']))
        self.assertTrue(self.m.condition(first(first(controls,'ICW_pmc_gc_open'),'visible'),self.m.c['GC']))
        self.assertFalse(self.m.condition(first(first(controls,'ICW_pmc_gc_close'),'visible'),self.m.c['GC']))
        for actor in (self.m.c['FRA'],self.m.c['GC']):
            actor.ai = actor.id=='GC'
            before = copy.deepcopy(self.m.g.vars)
            self.m.run('ICW_pmc_gc_open',actor)
            self.assertFalse(self.active())
            self.assertEqual(self.m.g.vars,before)
        self.m.start = '2000.1.1'
        self.m.run('ICW_pmc_gc_close',self.m.c['FRA'])
        self.assertTrue(self.active())

    def test_all_native_spawn_effects_are_inert_while_closed(self):
        actor = self.m.root
        for name in (k for k in self.m.effects if k.startswith('spawn_')):
            with self.subTest(effect=name):
                before = copy.deepcopy(actor.vars)
                self.m.run(name,actor)
                self.assertEqual(actor.vars,before)
                self.assertFalse(actor.units)

    def test_all_native_spawn_effects_still_deliver_after_gc_authorization(self):
        self.m.run('ICW_pmc_gc_open',self.m.c['GC'])
        actor = self.m.root
        for name in (k for k in self.m.effects if k.startswith('spawn_')):
            with self.subTest(effect=name):
                count = len(actor.units)
                self.m.run(name,actor)
                self.assertEqual(len(actor.units),count+1)

    def test_closed_gui_callbacks_are_inert_and_all_panels_are_hidden(self):
        actor = self.m.root
        callbacks = [('MD_missiles_gui','pmc_gui_ledger_button'),
                     ('international_pmc_units_dynamic_lists','name_of_pmc_units_button'),
                     ('international_pmc_companies_dynamic_lists','name_of_pmc_companies_button')]
        for name,control in callbacks:
            gui = first(self.gui,name)
            self.assertFalse(self.m.condition(first(first(gui,'triggers'),control+'_click_enabled'),actor))
            self.m.execute(first(first(gui,'effects'),control+'_click'),actor,actor,None)
        self.assertEqual(actor.vars,{'treasury':D(100)})
        for name in ('MD_PMC_system_gui','international_pmc_units_dynamic_lists','international_pmc_companies_dynamic_lists'):
            self.assertFalse(self.m.condition(first(first(self.gui,name),'visible'),actor))
        triggers = first(first(self.gui,'MD_missiles_gui'),'triggers')
        for key in ('pmc_gui_ledger_button_visible','icon_pmc_gui_ledger_visible'):
            self.assertFalse(self.m.condition(first(triggers,key),actor))
            self.m.start = '2000.1.1'
            self.assertTrue(self.m.condition(first(triggers,key),actor))
            self.m.start = '1970.1.1'

    def test_stale_major_timeouts_cannot_charge_reserve_capacity_or_deliver(self):
        actor = self.m.root
        for name in self.record['major_recruitment_missions']:
            with self.subTest(mission=name):
                before = copy.deepcopy(actor.vars)
                global_before = copy.deepcopy(self.m.g.vars)
                self.m.execute(first(self.m.decisions[name],'timeout_effect'),actor,actor,None)
                self.assertEqual(actor.vars,before)
                self.assertEqual(self.m.g.vars,global_before)
                self.assertFalse(actor.units)

    def test_gc_close_cancels_all_major_orders_and_clears_hiring_flags(self):
        self.m.run('ICW_pmc_gc_open',self.m.c['GC'])
        for actor in self.m.c.values():
            actor.missions.update(self.record['major_recruitment_missions'])
            actor.flags.update(('inf_hire','mot_inf_hire','mech_inf_hire','hvy_inf_hire','spec_inf_hire','tank_hire','sf_hire'))
            actor.vars['var_open_MD_PMC_gui'] = D(2)
        self.m.run('ICW_pmc_gc_close',self.m.c['GC'])
        for actor in self.m.c.values():
            self.assertFalse(actor.missions)
            self.assertFalse(actor.flags)
            self.assertNotIn('var_open_MD_PMC_gui',actor.vars)
            self.assertEqual(actor.vars['treasury'],100)
        self.m.run('ICW_pmc_gc_open',self.m.c['GC'])
        self.assertTrue(self.active())
        self.assertFalse(any(c.missions for c in self.m.c.values()))

    def test_native_blackwater_price_weekly_charge_and_discount_are_preserved(self):
        self.m.start = '2000.1.1'
        for tag,cost,weekly in (('FRA','3','.1'),('USA','2.4','.08')):
            actor = self.m.c[tag]
            self.m.execute(first(self.m.decisions['get_blackwater_light_infantry'],'timeout_effect'),actor,actor,None)
            self.assertEqual(actor.vars['treasury'],100-D(cost))
            self.assertEqual(actor.vars['pmc_expenses'],D(weekly))
            self.assertEqual(actor.vars['pmc_bought'],1)
            self.assertEqual(len(actor.units),1)

    def test_pending_local_order_refund_preserves_delivered_units_and_is_once_only(self):
        self.m.start = '2000.1.1'
        for index,name in enumerate(self.record['local_recruitment_decisions']):
            with self.subTest(decision=name):
                m = copy.deepcopy(self.m);actor = m.root;body = m.decisions[name]
                m.execute(first(body,'complete_effect'),actor,actor,None)
                m.execute(first(body,'remove_effect'),actor,actor,None)
                paid = actor.vars['treasury'];weekly = actor.vars['pmc_expenses']
                m.execute(first(body,'complete_effect'),actor,actor,None)
                actor.missions.add(name)
                m.run('ICW_pmc_gc_close',m.c['GC'])
                self.assertEqual(actor.vars['treasury'],paid)
                self.assertEqual(actor.vars['pmc_expenses'],weekly)
                self.assertEqual(actor.vars['pmc_bought'],1)
                self.assertEqual(len(actor.units),1)
                self.assertFalse(actor.missions)
                m.execute(first(body,'remove_effect'),actor,actor,None)
                m.execute(first(body,'cancel_effect'),actor,actor,None)
                self.assertEqual(actor.vars['treasury'],paid)
                self.assertEqual(len(actor.units),1)
                m.run('ICW_pmc_gc_open',m.c['GC'])
                m.execute(first(body,'complete_effect'),actor,actor,None)
                actor.missions.add(name)
                m.run('ICW_pmc_gc_close',m.c['GC'])
                self.assertEqual(actor.vars['treasury'],paid)
                self.assertEqual(actor.vars['pmc_expenses'],weekly)

    def test_startup_applies_closed_state_without_resetting_override(self):
        startup = first(first(first(load('common/on_actions/ICW_pmc_access.txt'),'on_actions'),'on_startup'),'effect')
        actor = self.m.root;actor.missions.add('get_blackwater_light_infantry')
        self.m.execute(startup,actor,actor,None)
        self.assertFalse(actor.missions)
        self.m.run('ICW_pmc_gc_open',self.m.c['GC'])
        actor.missions.add('get_blackwater_light_infantry')
        self.m.execute(startup,actor,actor,None)
        self.assertTrue(self.active())
        self.assertTrue(actor.missions)

    def test_close_preserves_delivered_units_and_voluntary_dismissal_ends_costs(self):
        self.m.start = '2000.1.1';actor = self.m.root
        self.m.execute(first(self.m.decisions['get_blackwater_light_infantry'],'timeout_effect'),actor,actor,None)
        self.m.run('ICW_pmc_gc_close',self.m.c['GC'])
        self.assertEqual(len(actor.units),1)
        self.assertEqual(actor.vars['pmc_expenses'],D('.1'))
        body = first(first(load('common/decisions/ICW_pmc_access.txt'),'pmc_category'),'ICW_pmc_dismiss_existing_units')
        self.assertTrue(self.m.condition(first(body,'visible'),actor))
        self.m.execute(first(body,'complete_effect'),actor,actor,None)
        self.assertFalse(actor.units)
        self.assertEqual(actor.vars['pmc_expenses'],0)
        self.assertEqual(actor.vars['pmc_bought'],0)

    def test_native_sources_are_exactly_recoverable_and_encodings_are_correct(self):
        validate_reverse(self.record)
        files = list(self.record['native_sha256_before'])
        files += ['common/'+folder+'/ICW_pmc_access.txt' for folder in ('scripted_effects','scripted_triggers','decisions','on_actions')]
        for rel in files:
            data = (ROOT/rel).read_bytes()
            self.assertFalse(data.startswith(b'\xef\xbb\xbf'),rel)
            self.assertTrue(data.decode('utf-8').startswith('# IMPERIA COLD WAR — '),rel)
            parse(data.decode('utf-8'))
        data = (ROOT/'localisation/english/ICW_pmc_access_l_english.yml').read_bytes()
        self.assertTrue(data.startswith(b'\xef\xbb\xbf'))
        on_actions = load('common/on_actions/ICW_pmc_access.txt')
        self.assertEqual([k for k,o,v in first(on_actions,'on_actions')],['on_startup'])


if __name__=='__main__':unittest.main(verbosity=2)
