# IMPERIA CW — Cold War: emitted-script transaction and ownership boundary tests.
"""Execute the feature's emitted subset; unsupported model statements fail.

This model does not emulate HOI4 resistance evolution, GUI routing, AI or netcode.
It tests scope selection, atomic payments, flags and explicit scripted arithmetic.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
import json
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/spain_1970_v2'))
from script_ast import parse, first
D = Decimal


@dataclass(eq=False)
class Scope:
    id: str
    kind: str = 'country'
    vars: dict = field(default_factory=dict)
    flags: set = field(default_factory=set)
    equipment: dict = field(default_factory=lambda: {'infantry_weapons_type': D(250), 'cnc_equipment_type': D(25)})
    owner: object = None
    controller: object = None
    overlord: object = None
    cores: set = field(default_factory=set)
    modifiers: set = field(default_factory=set)
    targets: dict = field(default_factory=dict)
    occupied: str = 'SHA'
    resistance: D = D(8)
    compliance: D = D(20)
    has_resistance: bool = True
    agency: bool = True
    pp: D = D(15)
    networks: dict = field(default_factory=dict)
    ai: bool = False
    stability: D = D('.5')


class Model:
    def __init__(self):
        self.effects = dict((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_colonial_affairs.txt').read_text(encoding='utf-8')))
        self.triggers = dict((k,v) for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_colonial_affairs.txt').read_text(encoding='utf-8')))
        self.effects.update((k,v) for k,o,v in parse((ROOT/'common/scripted_effects/COLDWAR_colonial_contacts.txt').read_text(encoding='utf-8')))
        self.triggers.update((k,v) for k,o,v in parse((ROOT/'common/scripted_triggers/COLDWAR_colonial_contacts.txt').read_text(encoding='utf-8')))
        self.c = {tag:Scope(tag) for tag in ('SPR','SHA','MOR','ALG','USA','SOV','FRA','COM','ENG','BHR')}
        self.s = {str(i):Scope(str(i),'state') for i in (372,373,269,940,1214,423)}
        self.g = Scope('global','global')
        self.scenario = True
        self.scenario1985 = False
        self.date = '1970.1.1'
        self.random_branch = 0
        self.saved_targets = {}
        self.events = []
        for country in self.c.values():country.vars['treasury']=D('.05')
        for state in self.s.values():state.owner=state.controller=self.c['SPR'];state.cores={'SHA'}
        self.root=self.c['ALG']

    def scope(self,name,current,root,prev):
        name=name.strip('"')
        if name in ('THIS','ROOT','PREV'):return {'THIS':current,'ROOT':root,'PREV':prev}[name]
        if name in ('owner','controller','overlord'):return getattr(current,name)
        if name.startswith('event_target:'):return self.saved_targets.get(name.split(':',1)[1])
        if name.startswith('var:'):
            value=self.value(name[4:],current,root,prev)
            return self.s.get(str(int(value))) if isinstance(value,Decimal) else value
        return self.c.get(name,self.s.get(name))

    def variable(self,name,current,root,prev):
        if '.' in name:
            prefix,fieldname=name.rsplit('.',1)
            target=self.g if prefix=='global' else self.scope(prefix,current,root,prev)
            if target is None:raise ValueError('Unknown variable scope '+name)
            return target,fieldname
        return current,name

    def value(self,name,current,root,prev):
        if isinstance(name,(Decimal,Scope)):return name
        if name in ('THIS','ROOT','PREV'):return self.scope(name,current,root,prev)
        if name in self.c:return self.scope(name,current,root,prev)
        if name.endswith('.id'):return D(self.scope(name[:-3],current,root,prev).id)
        try:return D(name)
        except Exception:pass
        if name.endswith('.resistance'):return self.scope(name[:-11],current,root,prev).resistance
        if name.endswith('.compliance'):return self.scope(name[:-11],current,root,prev).compliance
        obj,key=self.variable(name,current,root,prev)
        return obj.vars.get(key,D(0))

    @staticmethod
    def compare(a,op,b):
        return {'=':lambda:a==b,'>':lambda:a>b,'<':lambda:a<b,'>=':lambda:a>=b,'<=':lambda:a<=b,'!=':lambda:a!=b}[op]()

    def condition(self,rows,current,root=None,prev=None):
        root=root or current
        def test(k,op,v):
            if k in self.triggers:return self.condition(self.triggers[k],current,root,prev)==(v=='yes')
            if k=='IMP_is_1970_scenario':return self.scenario==(v=='yes')
            if k=='IMP_is_1985_scenario':return self.scenario1985==(v=='yes')
            if k=='date':return self.compare(tuple(map(int,self.date.split('.'))),op,tuple(map(int,v.split('.'))))
            if k=='is_ai':return current.ai==(v=='yes')
            if k=='network_strength':
                target=first(v,'state')
                state=self.scope(target,current,root,prev) if str(target).startswith(('var:','PREV','ROOT','THIS')) else self.s.get(str(target))
                return state is not None and self.compare(current.networks.get(state.id,D(0)),next(o for a,o,b in v if a=='value'),D(first(v,'value')))
            if k in ('OR','AND','NOT'):
                values=(self.condition([row],current,root,prev) for row in v)
                return any(values) if k=='OR' else all(values) if k=='AND' else not any(values)
            if k=='always':return v=='yes'
            if k=='check_variable':
                if first(v,'var') is not None:
                    ops={'greater_than_or_equals':'>=','less_than_or_equals':'<=','equals':'=','greater_than':'>','less_than':'<'}
                    return self.compare(self.value(first(v,'var'),current,root,prev),ops.get(first(v,'compare','equals'),'='),self.value(first(v,'value'),current,root,prev))
                name,operation,value=v[0];return self.compare(self.value(name,current,root,prev),operation,self.value(value,current,root,prev))
            if k in ('has_country_flag','has_state_flag'):return v in current.flags
            if k=='has_variable':return v in current.vars
            if k=='political_power':return self.compare(current.pp,op,self.value(v,current,root,prev))
            if k=='resistance':return self.compare(current.resistance,op,self.value(v,current,root,prev))
            if k=='tag':return current is self.scope(v,current,root,prev)
            if k=='exists':return (current is not None)==(v=='yes')
            if k=='is_subject':return (current.overlord is not None)==(v=='yes')
            if k=='is_subject_of':return current.overlord is self.scope(v,current,root,prev)
            if k=='controls_state':return self.s[v].controller is current
            if k=='owns_state':return self.s[v].owner is current
            if k=='is_owned_by':return current.owner is self.scope(v,current,root,prev)
            if k=='is_controlled_by':return current.controller is self.scope(v,current,root,prev)
            if k=='has_resistance':return current.has_resistance==(v=='yes')
            if k=='occupied_country_tag':return current.occupied==v
            if k=='is_core_of':
                target=self.scope(v,current,root,prev)
                return (target.id if target is not None else v) in current.cores
            if k=='state':return current.id==v
            if k=='has_dynamic_modifier':return first(v,'modifier') in current.modifiers
            if k=='has_intelligence_agency':return current.agency==(v=='yes')
            if k=='is_neighbor_of':return False
            if k=='has_equipment':return all(self.compare(current.equipment.get(name,D(0)),operation,self.value(amount,current,root,prev)) for name,operation,amount in v)
            if k=='any_country':return any(self.condition(v,c,root,current) for c in self.c.values())
            if k in ('any_state','any_controlled_state'):return any((k=='any_state' or s.controller is current) and self.condition(v,s,root,current) for s in self.s.values())
            if k=='any_neighbor_state':return False
            target=self.scope(k,current,root,prev)
            if target is not None:return self.condition(v,target,root,current)
            raise ValueError('Unsupported condition '+k)
        return all(test(k,op,v) for k,op,v in rows)

    def run(self,name,current=None):
        current=current or self.root
        self.execute(self.effects[name],current,current,None)

    def populate_registry(self):
        self.registry=json.loads((ROOT/'tools/colonial_affairs/registry.json').read_text(encoding='utf-8'))['administrations']
        for row in self.registry:
            for tag in [row['power'],row.get('native_tag'),row.get('subject_tag')]+list(row.get('state_native_tags',{}).values()):
                if tag and tag not in self.c:self.c[tag]=Scope(tag)
            owner=self.c[row.get('subject_tag',row['power'])] if row.get('subject_only') else self.c[row['power']]
            if row.get('subject_only'):owner.overlord=self.c[row['power']]
            for state_id in row['states']:
                state=self.s.setdefault(str(state_id),Scope(str(state_id),'state'))
                state.owner=state.controller=owner
                state.cores={row['native_tag']} if row.get('native_tag') else set()
                state.has_resistance=row['profile'] in ('war','contested')
            anchor=self.s[str(row['states'][0])]
            anchor.vars['COLDWAR_COL_policy']=D(2 if row['profile']=='war' else 0)
            self.g.vars['COLDWAR_COL_power_'+row['id']]=self.c[row['power']]

    def execute(self,rows,current,root,prev):
        last_if=None
        for key,op,value in rows:
            if key in self.effects:
                self.execute(self.effects[key],current,root,prev);continue
            if key=='if':
                last_if=self.condition(first(value,'limit',[]),current,root,prev)
                if last_if:self.execute([(k,o,v) for k,o,v in value if k!='limit'],current,root,prev)
            elif key=='else':
                if last_if is False:self.execute(value,current,root,prev)
                last_if=None
            elif key in ('hidden_effect','effect_tooltip'):
                if key=='hidden_effect':self.execute(value,current,root,prev)
            elif key in ('set_variable','set_temp_variable','add_to_variable','add_to_temp_variable','subtract_from_variable','multiply_variable','multiply_temp_variable','divide_variable','divide_temp_variable'):
                name,operation,argument=value[0];target,fieldname=self.variable(name,current,root,prev);number=self.value(argument,current,root,prev)
                old=target.vars.get(fieldname,D(0))
                target.vars[fieldname]=number if key.startswith('set_') else old+number if key.startswith('add_') else old-number if key.startswith('subtract_') else old*number if key.startswith('multiply_') else old/number
            elif key=='clamp_variable':
                obj,name=self.variable(first(value,'var'),current,root,prev);obj.vars[name]=min(D(first(value,'max')),max(D(first(value,'min')),obj.vars.get(name,D(0))))
            elif key in ('set_country_flag','set_state_flag'):
                current.flags.add(first(value,'flag') if isinstance(value,list) else value)
            elif key in ('clr_country_flag','clr_state_flag'):current.flags.discard(value)
            elif key=='clear_variable':
                obj,name=self.variable(value,current,root,prev);obj.vars.pop(name,None)
            elif key=='set_resistance':current.resistance=self.value(value,current,root,prev)
            elif key=='random_list':
                entries=[v for k,o,v in value if k.isdigit()]
                self.execute(entries[min(self.random_branch,len(entries)-1)],current,root,prev)
            elif key=='save_event_target_as':self.saved_targets[value]=current
            elif key in ('country_event','news_event'):self.events.append((first(value,'id'),current.id,dict(self.saved_targets)))
            elif key=='every_country':
                limit=first(value,'limit',[]);body=[row for row in value if row[0]!='limit']
                for country in self.c.values():
                    if self.condition(limit,country,root,current):self.execute(body,country,root,current)
            elif key=='modify_treasury_effect':current.vars['treasury']+=current.vars['treasury_change']
            elif key=='add_political_power':current.pp+=self.value(value,current,root,prev)
            elif key=='add_stability':current.stability+=self.value(value,current,root,prev)
            elif key=='remove_ideas':pass
            elif key=='add_equipment_to_stockpile':current.equipment[first(value,'type')]+=self.value(first(value,'amount'),current,root,prev)
            elif key in ('add_dynamic_modifier','remove_dynamic_modifier'):
                modifier=first(value,'modifier');current.modifiers.add(modifier) if key.startswith('add_') else current.modifiers.discard(modifier)
            elif key=='remove_resistance_target':current.targets.pop(value,None)
            elif key=='add_resistance_target':current.targets[first(value,'id')]=self.value(first(value,'amount'),current,root,prev)
            elif key=='add_resistance':current.resistance+=self.value(value,current,root,prev)
            elif key=='add_compliance':current.compliance+=self.value(value,current,root,prev)
            elif key in ('add_opinion_modifier','reverse_add_opinion_modifier'):pass
            else:
                target=self.scope(key,current,root,prev)
                if target is None:raise ValueError('Unsupported effect '+key)
                self.execute(value,target,root,current)


class Transactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.template=Model()

    def setUp(self):
        import copy
        self.m=copy.deepcopy(self.template)
        self.m.g.vars['COLDWAR_COL_power_spr_western_sahara']=self.m.c['SPR']
        self.m.s['372'].vars['COLDWAR_COL_policy']=D(0)
        self.m.s['372'].flags.add('COLDWAR_COL_organised_movement')
        self.m.c['ALG'].vars['COLDWAR_COL_support_target']=D(372)
        self.m.c['ALG'].networks={'372':D(51),'373':D(51)}

    def allowed(self,package):return self.m.condition(self.m.triggers['COLDWAR_COL_can_spr_western_sahara_'+package],self.m.c['ALG'])

    def test_exact_funds_charge_once(self):
        self.assertTrue(self.allowed('funding'))
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],0)
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_support_bonus'],5)
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],0)

    def test_insufficient_funds_no_charge(self):
        self.m.c['ALG'].vars['treasury']=D('.04999')
        self.assertFalse(self.allowed('funding'))
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],D('.04999'))
        self.assertFalse(self.m.c['ALG'].flags)

    def test_exact_arms_stockpile_and_pp(self):
        for state in self.m.s.values():state.resistance=D(25)
        self.assertTrue(self.allowed('arms'))
        self.m.run('COLDWAR_COL_send_spr_western_sahara_arms')
        country=self.m.c['ALG']
        self.assertEqual(country.pp,0)
        self.assertEqual(country.equipment,{'infantry_weapons_type':0,'cnc_equipment_type':0})
        self.assertEqual(self.m.s['372'].resistance,30)
        self.m.run('COLDWAR_COL_send_spr_western_sahara_arms')
        self.assertEqual(self.m.s['372'].resistance,30)

    def test_low_stock_or_pp_has_no_side_effect(self):
        for key in ('infantry_weapons_type','cnc_equipment_type'):
            original=self.m.c['ALG'].equipment[key];self.m.c['ALG'].equipment[key]=original-1
            self.assertFalse(self.allowed('arms'));self.m.run('COLDWAR_COL_send_spr_western_sahara_arms')
            self.assertEqual(self.m.c['ALG'].pp,15)
            self.m.c['ALG'].equipment[key]=original
        self.m.c['ALG'].pp=D(14);self.assertFalse(self.allowed('arms'))

    def test_control_loss_independence_and_self_support(self):
        self.m.s['372'].owner=self.m.s['372'].controller=self.m.c['SHA']
        self.m.s['373'].owner=self.m.s['373'].controller=self.m.c['SHA']
        self.m.run('COLDWAR_COL_reconcile_spr_western_sahara',self.m.c['SPR'])
        self.assertFalse(self.allowed('funding'))
        self.m.s['372'].owner=self.m.s['372'].controller=self.m.c['SPR']
        self.m.run('COLDWAR_COL_reconcile_spr_western_sahara',self.m.c['SPR'])
        self.assertTrue(self.allowed('funding'))
        self.m.c['ALG'].overlord=self.m.c['SPR'];self.assertFalse(self.allowed('funding'))

    def test_multiple_sponsors_have_one_shared_cap(self):
        for tag in ('ALG','USA','SOV','MOR'):
            country=self.m.c[tag];country.flags.add('COLDWAR_COL_spr_western_sahara_funding_live')
        self.m.run('COLDWAR_COL_sum_support_spr_western_sahara')
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_support_bonus'],15)
        self.m.run('COLDWAR_COL_apply_spr_western_sahara')
        self.assertEqual(max(self.m.s['372'].targets.values()),15)

    def test_full_support_cap_blocks_new_payment_with_stale_preview(self):
        for tag in ('USA','SOV','MOR'):self.m.c[tag].flags.add('COLDWAR_COL_spr_western_sahara_funding_live')
        self.m.s['372'].vars['COLDWAR_COL_support_bonus']=D(0)
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],D('.05'))
        self.assertNotIn('COLDWAR_COL_spr_western_sahara_funding',self.m.c['ALG'].flags)

    def test_peaceful_political_support_does_not_create_war(self):
        self.m.s['372'].has_resistance=False;self.m.s['373'].has_resistance=False
        self.assertTrue(self.allowed('political'));self.assertFalse(self.allowed('arms'));self.assertFalse(self.allowed('funding'))
        self.m.run('COLDWAR_COL_send_spr_western_sahara_political')
        self.assertEqual(self.m.c['ALG'].pp,0)
        self.assertFalse(self.m.s['372'].has_resistance)
        self.assertIn('COLDWAR_COL_political_backing',self.m.s['372'].flags)

    def test_wrong_scenario_or_target_cannot_pay(self):
        self.m.scenario=False;self.assertFalse(self.allowed('funding'))
        self.m.scenario=True;self.m.c['ALG'].vars['COLDWAR_COL_support_target']=D(999)
        self.assertFalse(self.allowed('funding'))

    def test_current_weekly_cost_and_partial_independence(self):
        self.m.populate_registry()
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],D('.008'))
        self.m.s['372'].owner=self.m.s['372'].controller=self.m.c['SHA']
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],D('.004'))
        self.m.s['373'].owner=self.m.s['373'].controller=self.m.c['SHA']
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],0)

    def test_foreign_successor_assumes_colonial_cost(self):
        self.m.populate_registry()
        for state_id in ('372','373'):self.m.s[state_id].owner=self.m.s[state_id].controller=self.m.c['MOR']
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['SPR'])
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['MOR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],0)
        self.assertEqual(self.m.c['MOR'].vars['COLDWAR_COL_total_weekly_cost'],D('.008'))

    def test_protectorate_independence_ends_patron_cost(self):
        self.m.populate_registry()
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['ENG'])
        before=self.m.c['ENG'].vars['COLDWAR_COL_total_weekly_cost']
        self.m.c['BHR'].overlord=None
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['ENG'])
        self.assertEqual(before-self.m.c['ENG'].vars['COLDWAR_COL_total_weekly_cost'],D('.002'))

    def test_policy_budget_and_lock_use_actual_emitted_effect(self):
        self.m.populate_registry()
        self.m.c['SPR'].vars['COLDWAR_COL_selected']=D(30)
        self.m.run('COLDWAR_COL_set_spr_western_sahara_development',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],D('.024'))
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_policy_days'],180)
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_view_construction_penalty'],-2)
        self.m.run('COLDWAR_COL_set_spr_western_sahara_security',self.m.c['SPR'])
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_policy'],1)
        self.m.s['372'].vars['COLDWAR_COL_policy_days']=D(0)
        self.m.run('COLDWAR_COL_set_spr_western_sahara_security',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],D('.016'))
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_target'],D('.17'))

    def test_distinct_pacific_successors_are_not_new_colonisers(self):
        self.m.populate_registry()
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['USA'])
        for state_id,tag in [('819','PAU'),('820','MAR'),('821','MIC')]:
            self.m.s[state_id].owner=self.m.s[state_id].controller=self.m.c[tag]
        self.m.run('COLDWAR_COL_reconcile_usa_trust_pacific',self.m.c['USA'])
        self.assertIn('COLDWAR_COL_inactive',self.m.s['819'].flags)

    def test_independent_clicked_state_cannot_support_retained_sibling(self):
        self.m.s['372'].owner=self.m.s['372'].controller=self.m.c['SHA']
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],D('.05'))

    def test_unrest_stages_apply_actual_local_penalties(self):
        for resistance,construction,resources,garrison,supply in [(8,'-.15','-.05','0','0'),(20,'-.15','-.05','0','0'),(40,'-.15','-.15','.15','0'),(60,'-.15','-.15','.15','-.1')]:
            for s in ('372','373'):self.m.s[s].resistance=D(resistance)
            self.m.run('COLDWAR_COL_apply_spr_western_sahara')
            variables=self.m.s['372'].vars
            for key,expected in [('construction',construction),('resources',resources),('garrison',garrison),('supply',supply)]:
                self.assertEqual(variables['COLDWAR_COL_'+key],D(expected))

    def test_non_resistance_territories_do_not_get_war_stage_penalties(self):
        for s in ('372','373'):self.m.s[s].has_resistance=False;self.m.s[s].resistance=D(70)
        self.m.run('COLDWAR_COL_apply_spr_western_sahara')
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_garrison'],0)
        self.assertEqual(self.m.s['372'].vars['COLDWAR_COL_supply'],0)

    def pending_event(self,serial):
        state=self.m.s['372'];country=self.m.c['SPR']
        state.flags.add('COLDWAR_COL_issue_pending')
        state.vars.update(COLDWAR_COL_issue_serial=D(2),COLDWAR_COL_issue_days=D(60),COLDWAR_COL_issue_grant_cost=D('.05'),COLDWAR_COL_issue_pp_cost=D(15))
        country.flags.add('COLDWAR_COL_event_open')
        country.vars.update(COLDWAR_COL_event_anchor=D(372),COLDWAR_COL_event_serial=D(serial),COLDWAR_COL_issue_grant_cost=D('.05'),COLDWAR_COL_issue_pp_cost=D(15))
        return country,state

    def test_old_event_cannot_charge_or_resolve_a_new_petition(self):
        country,state=self.pending_event(1)
        self.m.run('COLDWAR_COL_respond_grant',country)
        self.assertEqual(country.vars['treasury'],D('.05'))
        self.assertIn('COLDWAR_COL_issue_pending',state.flags)
        self.assertNotIn('COLDWAR_COL_event_open',country.flags)

    def test_current_event_charges_once_and_keeps_quiet_benefit_real(self):
        country,state=self.pending_event(2)
        state.has_resistance=False
        self.m.run('COLDWAR_COL_respond_grant',country)
        self.assertEqual(country.vars['treasury'],0)
        self.assertNotIn('COLDWAR_COL_issue_pending',state.flags)
        self.assertIn('COLDWAR_COL_public_services_grant',state.modifiers)
        self.m.run('COLDWAR_COL_respond_grant',country)
        self.assertEqual(country.vars['treasury'],0)

    def test_repeated_startup_does_not_advance_existing_policy_or_petition(self):
        self.m.populate_registry()
        for country in self.m.c.values():country.flags.add('COLDWAR_COL_bootstrapped')
        state=self.m.s['372'];state.vars['COLDWAR_COL_policy_days']=D(180);state.vars['COLDWAR_COL_issue_days']=D(30)
        actions=parse((ROOT/'common/on_actions/COLDWAR_colonial_affairs.txt').read_text(encoding='utf-8'))
        startup=first(first(first(actions,'on_actions'),'on_startup'),'effect')
        self.m.execute(startup,self.m.c['SPR'],self.m.c['SPR'],None)
        self.assertEqual(state.vars['COLDWAR_COL_policy_days'],180)
        self.assertEqual(state.vars['COLDWAR_COL_issue_days'],30)

    def local_case(self, state='900', power='FRA'):
        self.m.c.setdefault('GER',Scope('GER'))
        region=self.m.s.setdefault(state,Scope(state,'state'))
        region.owner=self.m.c['USA'];region.controller=self.m.c[power]
        region.cores={'USA'};region.resistance=D(30);region.compliance=D(20)
        donor=self.m.c['ALG'];donor.vars['COLDWAR_COL_support_target']=D(state);donor.networks[state]=D(51)
        return donor,region

    def test_network_threshold_is_strict_and_regional(self):
        for strength,expected in [(0,False),(D('49.99'),False),(50,False),(D('50.01'),True)]:
            self.m.c['ALG'].networks['372']=D(str(strength))
            self.assertEqual(self.allowed('funding'),expected)
        self.m.c['ALG'].networks={'373':D(100)}
        self.assertFalse(self.allowed('funding'))
        self.m.run('COLDWAR_COL_send_spr_western_sahara_funding')
        self.assertEqual(self.m.c['ALG'].vars['treasury'],D('.05'))

    def test_lost_network_blocks_open_file_payment(self):
        donor,region=self.local_case()
        donor.flags.add('COLDWAR_COL_support_panel_open');donor.networks['900']=D(50)
        self.m.run('COLDWAR_COL_send_local_funding')
        self.assertEqual(donor.vars['treasury'],D('.05'))
        self.assertNotIn('COLDWAR_COL_local_funding_live',donor.flags)

    def test_occupation_funding_actual_charge_cap_and_expiry(self):
        donor,region=self.local_case()
        self.m.run('COLDWAR_COL_send_local_funding')
        self.assertEqual(donor.vars['treasury'],0)
        self.assertEqual(region.vars['COLDWAR_COL_local_aid'],5)
        self.assertEqual(region.targets['19709990'],5)
        self.m.run('COLDWAR_COL_send_local_funding')
        self.assertEqual(donor.vars['treasury'],0)
        donor.flags.discard('COLDWAR_COL_local_funding_live')
        self.m.run('COLDWAR_COL_refresh_local_aid',region)
        self.assertEqual(region.vars['COLDWAR_COL_local_aid'],0)
        self.assertNotIn('19709990',region.targets)

    def test_local_aid_does_not_pass_to_a_new_occupier(self):
        donor,region=self.local_case()
        self.m.run('COLDWAR_COL_send_local_funding')
        region.controller=self.m.c['SPR']
        self.m.run('COLDWAR_COL_refresh_local_aid',region)
        self.assertEqual(region.vars['COLDWAR_COL_local_aid'],0)

    def test_ended_occupation_cannot_revive_a_previous_delivery(self):
        donor,region=self.local_case()
        self.m.run('COLDWAR_COL_send_local_funding')
        region.has_resistance=False
        self.m.run('COLDWAR_COL_refresh_local_aid',region)
        self.assertNotIn('COLDWAR_COL_local_funding_live',donor.flags)
        self.assertIn('COLDWAR_COL_local_funding_cooldown',donor.flags)
        region.has_resistance=True
        self.m.run('COLDWAR_COL_refresh_local_aid',region)
        self.assertEqual(region.vars['COLDWAR_COL_local_aid'],0)

    def test_raf_is_not_present_on_january_start(self):
        donor,region=self.local_case('41','GER')
        self.m.c['GER'].flags.add('COLDWAR_GER_1970_initialized');self.m.c['GER'].vars['cwger_raf_gen']=D(1)
        region.owner=region.controller;region.cores={'GER'};region.has_resistance=False
        for date,expected in [('1970.1.1',False),('1970.5.13',False),('1970.5.14',True)]:
            self.m.date=date
            self.assertEqual(self.m.condition(self.m.triggers['COLDWAR_COL_group_raf'],region),expected)

    def raf_case(self):
        donor,region=self.local_case('41','GER');self.m.date='1970.6.1'
        country=self.m.c['GER'];country.flags.add('COLDWAR_GER_1970_initialized')
        country.vars.update(cwger_raf_gen=D(1),cwger_raf_cadre=D(12),cwger_raf_milieu=D(22),cwsec_plan_justice=D(74))
        for state in ('41','42','1080','1251'):
            s=self.m.s.setdefault(state,Scope(state,'state'));s.owner=s.controller=country;s.cores={'GER'};s.has_resistance=False;donor.networks[state]=D(51)
        ni=self.m.s.setdefault('17',Scope('17','state'));ni.owner=ni.controller=self.m.c['ENG']
        return donor,region,country

    def test_raf_assistance_feeds_existing_model_without_duplicate_case(self):
        donor,region,country=self.raf_case()
        self.m.run('COLDWAR_COL_send_local_arms')
        self.assertEqual(country.vars['cwger_raf_cadre'],13)
        self.assertEqual(country.vars['COLDWAR_COL_raf_aid'],5)
        self.m.run('COLDWAR_COL_contacts_monthly',country)
        self.assertEqual(country.vars['cwger_raf_cadre'],D('13.25'))
        self.assertEqual(country.vars['cwsec_plan_justice'],74)
        self.assertNotIn('COLDWAR_COL_domestic_security',region.modifiers)
        self.assertNotIn('COLDWAR_COL_cells',region.vars)
        self.assertFalse(self.m.events)
        self.m.run('COLDWAR_COL_domestic_budget',country)
        self.assertEqual(country.vars['COLDWAR_COL_domestic_weekly_cost'],0)

    def test_raf_global_cap_blocks_payment_in_another_region(self):
        donor,region,country=self.raf_case()
        for tag in ('USA','SOV','MOR'):
            sponsor=self.m.c[tag];sponsor.flags.add('COLDWAR_COL_local_funding_live')
            sponsor.vars.update(COLDWAR_COL_local_funding_state=D(41),COLDWAR_COL_local_funding_power=country)
        donor.vars['COLDWAR_COL_support_target']=D(42)
        self.m.run('COLDWAR_COL_send_local_funding')
        self.assertEqual(country.vars['COLDWAR_COL_raf_aid'],15)
        self.assertEqual(donor.vars['treasury'],D('.05'))
        self.assertNotIn('COLDWAR_COL_local_funding_live',donor.flags)

    def test_dissolved_raf_cannot_receive_further_support(self):
        donor,region,country=self.raf_case();country.flags.add('COLDWAR_GER_1970_raf_dissolved')
        self.m.run('COLDWAR_COL_send_local_arms')
        self.assertEqual(country.vars['cwger_raf_cadre'],12)
        self.assertEqual(donor.equipment['infantry_weapons_type'],250)

    def test_new_ira_uses_cells_without_forcing_occupation(self):
        donor,region=self.local_case('17','ENG')
        region.owner=region.controller;region.cores={'ENG'};region.has_resistance=False
        region.vars['COLDWAR_COL_cells']=D(35)
        self.m.run('COLDWAR_COL_send_local_arms')
        self.assertEqual(region.vars['COLDWAR_COL_cells'],38)
        self.assertEqual(region.vars['COLDWAR_COL_local_aid'],5)
        self.assertFalse(region.has_resistance)
        self.assertNotIn('19709990',region.targets)
        self.assertEqual(donor.equipment['infantry_weapons_type'],0)

    def test_domestic_monthly_policy_applies_only_once_by_controller(self):
        self.m.populate_registry();donor,region=self.local_case('17','ENG')
        region.owner=region.controller;region.cores={'ENG'};region.has_resistance=False
        region.vars.update(COLDWAR_COL_cells=D(35),COLDWAR_COL_case_policy=D(2))
        for s in ('41','42','1080','1251'):
            dummy=self.m.s.setdefault(s,Scope(s,'state'));dummy.owner=dummy.controller=self.m.c['GER']
        self.m.run('COLDWAR_COL_contacts_monthly',donor)
        self.assertEqual(region.vars['COLDWAR_COL_cells'],35)
        self.m.run('COLDWAR_COL_contacts_monthly',self.m.c['ENG'])
        self.assertEqual(region.vars['COLDWAR_COL_cells'],34)
        self.assertEqual(region.vars['COLDWAR_COL_domestic_construction'],D('-.084'))
        self.m.run('COLDWAR_COL_domestic_budget',self.m.c['ENG'])
        self.assertEqual(self.m.c['ENG'].vars['COLDWAR_COL_domestic_weekly_cost'],D('.02'))

    def test_disclosure_is_optional_and_captures_correct_sponsor_region(self):
        donor,region=self.local_case()
        self.m.random_branch=0;self.m.run('COLDWAR_COL_disclose_funding')
        self.assertFalse(self.m.events)
        self.m.random_branch=1;self.m.run('COLDWAR_COL_disclose_funding')
        event,power,targets=self.m.events[-1]
        self.assertEqual((event,power),('COLDWAR_colonial_contacts.1','FRA'))
        self.assertIs(targets['COLDWAR_COL_exposed_sponsor'],donor)
        self.assertIs(targets['COLDWAR_COL_exposed_region'],region)
        events=parse((ROOT/'events/COLDWAR_colonial_contacts.txt').read_text(encoding='utf-8'))
        response=next(v for k,o,v in events if k=='country_event' and first(v,'id')=='COLDWAR_colonial_contacts.1')
        self.m.execute(first(response,'immediate'),self.m.c['FRA'],self.m.c['FRA'],donor)
        self.assertEqual(donor.stability,D('.49'))
        self.assertEqual(self.m.events[-1][0],'COLDWAR_colonial_contacts.2')

    def test_new_case_policy_charges_once_and_keeps_mandate(self):
        donor,region=self.local_case('17','ENG');region.owner=region.controller;region.cores={'ENG'};region.has_resistance=False
        country=self.m.c['ENG'];country.pp=D(25);country.vars['COLDWAR_COL_case_target']=D(17)
        region.vars.update(COLDWAR_COL_cells=D(35),COLDWAR_COL_case_policy=D(0))
        self.m.run('COLDWAR_COL_adopt_case_1',country)
        self.assertEqual(country.pp,0)
        self.assertEqual(region.vars['COLDWAR_COL_case_policy'],1)
        self.assertEqual(region.vars['COLDWAR_COL_case_lock'],180)
        self.m.run('COLDWAR_COL_adopt_case_2',country)
        self.assertEqual(country.pp,0)
        self.assertEqual(region.vars['COLDWAR_COL_case_policy'],1)

    def test_domestic_startup_keeps_existing_lock_and_uses_current_country(self):
        donor,region=self.local_case('17','ENG');region.owner=region.controller;region.cores={'ENG'};region.has_resistance=False
        region.flags.add('COLDWAR_COL_ira_initialized');region.vars.update(COLDWAR_COL_cells=D(37),COLDWAR_COL_case_lock=D(180))
        for s in ('41','42','1080','1251'):
            dummy=self.m.s.setdefault(s,Scope(s,'state'));dummy.owner=dummy.controller=self.m.c['GER']
        actions=parse((ROOT/'common/on_actions/COLDWAR_colonial_contacts.txt').read_text(encoding='utf-8'))
        startup=first(first(first(actions,'on_actions'),'on_startup'),'effect')
        self.m.execute(startup,donor,donor,None)
        self.assertEqual(region.vars['COLDWAR_COL_cells'],37)
        self.assertEqual(region.vars['COLDWAR_COL_case_lock'],180)
        self.assertEqual(self.m.c['ENG'].vars['COLDWAR_COL_case_strength'],37)

    def test_monthly_dispatch_has_one_current_country_update(self):
        donor,region=self.local_case('17','ENG');region.owner=region.controller;region.cores={'ENG'};region.has_resistance=False
        region.vars.update(COLDWAR_COL_cells=D(35),COLDWAR_COL_case_policy=D(2))
        for s in ('41','42','1080','1251'):
            dummy=self.m.s.setdefault(s,Scope(s,'state'));dummy.owner=dummy.controller=self.m.c['GER']
        actions=parse((ROOT/'common/on_actions/COLDWAR_colonial_contacts.txt').read_text(encoding='utf-8'))
        monthly=first(first(first(actions,'on_actions'),'on_monthly'),'effect')
        self.assertNotIn('every_country',[k for k,o,v in monthly])
        self.m.execute(monthly,self.m.c['ENG'],self.m.c['ENG'],None)
        self.assertEqual(region.vars['COLDWAR_COL_cells'],34)

    def test_colonial_floor_respite_and_unrest_surcharge(self):
        self.m.populate_registry();region=self.m.s['372'];region.resistance=D(3)
        self.m.run('COLDWAR_COL_apply_spr_western_sahara')
        self.assertEqual(region.resistance,25)
        self.assertEqual(region.vars['COLDWAR_COL_target'],D('.28'))
        region.flags.add('COLDWAR_COL_detente');region.resistance=D(3)
        self.m.run('COLDWAR_COL_apply_spr_western_sahara')
        self.assertEqual(region.resistance,15)
        region.resistance=self.m.s['373'].resistance=D(65)
        self.m.c['SPR'].vars['COLDWAR_COL_selected']=D(0)
        self.m.run('COLDWAR_COL_recalculate_budget',self.m.c['SPR'])
        self.assertEqual(self.m.c['SPR'].vars['COLDWAR_COL_total_weekly_cost'],D('.012'))


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Transactions)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'passed':result.wasSuccessful(),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'engine_tested':False}
    (Path(__file__).parent/'runtime_tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
