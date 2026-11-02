# IMPERIA COLD WAR — Source-driven domestic transaction regression checks.
"""Run returned native effect bodies in a bounded fiscal/lifecycle interpreter.

This validates the emitted transactions, not native HOI4 rendering or ticks.
The actual bilateral pool and early-repayment bodies are included. Native
Treasury/debt consumers are represented by their inspected variable changes.
"""
from collections import defaultdict
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import re
import unittest

from runtime_bilateral import build as bilateral_build, extend_data as bilateral_extend
from runtime_domestic import build, extend_data
from runtime_layout import arrange, audit


def parse(text):
    tokens = [m[0] for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|>=|<=|!=|[{}=<>]|[^\s{}=<>!#"]+', text) if not m[0].startswith('#')]
    cursor = 0
    def block(nested=False):
        nonlocal cursor
        rows = []
        while cursor < len(tokens):
            key = tokens[cursor]; cursor += 1
            if key == '}':
                assert nested
                return rows
            op = tokens[cursor]; cursor += 1
            assert op in ('=', '>', '<', '>=', '<=', '!=')
            value = tokens[cursor]; cursor += 1
            if value == '{': value = block(True)
            rows.append((key.strip('"'), op, value.strip('"') if isinstance(value, str) else value))
        assert not nested
        return rows
    return block()


def one(rows, key, default=None):
    return next((v for k, o, v in rows if k == key), default)


class Runtime:
    def __init__(self, domestic, bilateral):
        self.vars = defaultdict(lambda: defaultdict(Decimal))
        self.temp = defaultdict(dict)
        self.flags = defaultdict(dict)
        self.modifiers = defaultdict(set)
        self.technologies = defaultdict(set)
        self.completed = set()
        self.party = set()
        self.war = False
        self.states = {str(s): {'owner': 'ISR', 'controller': 'ISR', 'slots': 5, 'factories': 1} for s in (204,205,206)}
        self.effects, self.triggers = {}, {}
        self.resets, self.xp = [], 0
        self.overrides = {}
        for bundle in (domestic, bilateral):
            for path, source in bundle['files'].items():
                if '/scripted_effects/' in path: self.effects.update({k:v for k,o,v in parse(source)})
                if '/scripted_triggers/' in path: self.triggers.update({k:v for k,o,v in parse(source)})
        self.vars['ISR'].update(gdp_total=Decimal('10'), treasury=Decimal('5'), debt=Decimal('1'),
                                political_power=Decimal('100'), stability=Decimal('.5'))
        self.party.update(g['runtime_party_trigger'] for g in DATA['groups'] if g.get('runtime_party_trigger'))
        for name in self.triggers:
            if name.endswith('_pair_clear'): self.overrides[name] = True
        self.run('ISR2_domestic_init')

    def value(self, raw, ctx='ISR'):
        if isinstance(raw, list):
            result = self.value(one(raw, 'value', '0'), ctx)
            for key, op, val in raw:
                if key == 'multiply': result *= self.value(val, ctx)
                if key == 'divide': result /= self.value(val, ctx)
                if key == 'add': result += self.value(val, ctx)
                if key == 'subtract': result -= self.value(val, ctx)
            return result
        try: return Decimal(raw)
        except Exception: pass
        if '.' in raw:
            tag, name = raw.split('.', 1)
            if tag in ('ISR','SOV','USA','GER','ROM'): return self.value(name, tag)
        return self.temp[ctx].get(raw, self.vars[ctx][raw])

    def test(self, rows, ctx='ISR', mode='AND'):
        vals = []
        for key, op, val in rows:
            if key in ('AND', 'hidden_trigger', 'limit'): result = self.test(val, ctx)
            elif key == 'OR': result = self.test(val, ctx, 'OR')
            elif key == 'NOT': result = not self.test(val, ctx)
            elif key == 'custom_trigger_tooltip': result = self.test([r for r in val if r[0]!='tooltip'], ctx)
            elif key == 'check_variable':
                if one(val,'var') is not None:
                    x=self.value(one(val,'var'),ctx);y=self.value(one(val,'value'),ctx);cmp=one(val,'compare')
                    result = x<=y if cmp=='less_than_or_equals' else x>=y
                else:
                    var, cmp, rhs = val[0];x=self.value(var,ctx);y=self.value(rhs,ctx)
                    result = {'=':x==y,'>':x>y,'<':x<y,'>=':x>=y,'<=':x<=y,'!=':x!=y}[cmp]
            elif key == 'has_country_flag': result = val in self.flags[ctx]
            elif key == 'has_completed_focus': result = val in self.completed
            elif key == 'has_dynamic_modifier': result = one(val,'modifier') in self.modifiers[ctx]
            elif key == 'has_war': result = self.war == (val=='yes')
            elif key in ('has_political_power','has_stability'):
                actual={'has_political_power':'political_power','has_stability':'stability'}[key]
                x=self.vars[ctx][actual];y=self.value(val,ctx);result={'<':x<y,'>':x>y,'=':x==y}[op]
            elif key in ('owns_state','controls_state','has_full_control_of_state'):
                result = self.states[val]['owner' if key=='owns_state' else 'controller']==ctx
            elif key in ('is_owned_by','is_controlled_by'): result=self.states[ctx]['owner' if key=='is_owned_by' else 'controller']==val
            elif key == 'free_building_slots': result=self.states[ctx]['factories']<50
            elif key == 'can_staff_an_industrial_complex': result=True
            elif key == 'ISR2_is_scenario': result=ctx=='ISR'
            elif key in self.overrides: result=self.overrides[key]
            elif key in self.party: result=True
            elif key in self.triggers: result=self.test(self.triggers[key],ctx)
            elif isinstance(val,list) and key in ('ISR','SOV','USA','GER','ROM','204','205','206'): result=self.test(val,key)
            else: raise AssertionError(('Unmodelled trigger',ctx,key,op,val))
            vals.append(result)
        return any(vals) if mode=='OR' else all(vals)

    def run(self, name, ctx='ISR'):
        self.execute(self.effects[name],ctx)

    def execute(self, rows, ctx='ISR'):
        prior = False
        for key, op, val in rows:
            if key=='if':
                prior=self.test(one(val,'limit',[]),ctx)
                if prior:self.execute([r for r in val if r[0]!='limit'],ctx)
            elif key=='else':
                if not prior:self.execute(val,ctx)
            elif key in ('set_variable','set_temp_variable','add_to_variable','subtract_from_variable','multiply_variable','divide_variable'):
                var,_,raw=val[0];amount=self.value(raw,ctx)
                if key=='set_temp_variable':self.temp[ctx][var]=amount
                elif key=='set_variable':self.vars[ctx][var]=amount
                elif key=='add_to_variable':self.vars[ctx][var]+=amount
                elif key=='subtract_from_variable':self.vars[ctx][var]-=amount
                elif key=='multiply_variable':self.vars[ctx][var]*=amount
                else:self.vars[ctx][var]/=amount
            elif key=='clamp_variable':
                name=one(val,'var');self.vars[ctx][name]=max(self.value(one(val,'min','-999999'),ctx),min(self.value(one(val,'max','999999'),ctx),self.vars[ctx][name]))
            elif key=='multiply_temp_variable':
                name,op,raw=val[0];self.temp[ctx][name]=self.value(name,ctx)*self.value(raw,ctx)
            elif key=='set_country_flag':
                if isinstance(val,list):
                    # Native dictionary form defaults to value 0. Such a flag
                    # does not satisfy has_country_flag, even with days set.
                    flag=one(val,'flag')
                    if self.value(one(val,'value','0'),ctx)>0:
                        days=one(val,'days')
                        self.flags[ctx][flag]=int(days) if days is not None else None
                    else:self.flags[ctx].pop(flag,None)
                else:self.flags[ctx][val]=None
            elif key=='clr_country_flag':self.flags[ctx].pop(val,None)
            elif key=='add_dynamic_modifier':self.modifiers[ctx].add(one(val,'modifier'))
            elif key=='remove_dynamic_modifier':self.modifiers[ctx].discard(one(val,'modifier'))
            elif key=='set_technology':self.technologies[ctx].update(k for k,o,v in val)
            elif key=='add_extra_state_shared_building_slots':self.states[ctx]['slots']+=int(val)
            elif key=='add_building_construction':self.states[ctx]['factories']+=int(one(val,'level'))
            elif key=='army_experience':self.xp+=int(val)
            elif key=='add_political_power':self.vars[ctx]['political_power']+=Decimal(val)
            elif key=='add_stability':self.vars[ctx]['stability']+=Decimal(val)
            elif key=='uncomplete_national_focus':
                assert one(val,'uncomplete_children')=='no' and one(val,'refund_political_power')=='no'
                focus=one(val,'focus');self.completed.discard(focus);self.resets.append(focus)
            elif key=='modify_treasury_effect':self.vars[ctx]['treasury']+=self.temp[ctx].get('treasury_change',0)
            elif key=='modify_debt_effect':self.vars[ctx]['debt']=max(Decimal(0),self.vars[ctx]['debt']+self.temp[ctx].get('debt_change',0))
            elif key in ('custom_effect_tooltip','update_money_dirty_variable','effect_tooltip'):pass
            elif key in self.effects:self.run(key,ctx)
            elif isinstance(val,list) and key in ('ISR','SOV','USA','GER','ROM','204','205','206'):self.execute(val,key)
            else:raise AssertionError(('Unmodelled effect',ctx,key,op,val))

    def days(self, count):
        for _ in range(count):
            for ctx in list(self.flags):
                for flag, days in list(self.flags[ctx].items()):
                    if days is not None:
                        if days<=1:self.flags[ctx].pop(flag)
                        else:self.flags[ctx][flag]-=1
            self.run('ISR2_domestic_daily')


DATA=extend_data(bilateral_extend(json.loads((Path(__file__).parent/'design.json').read_text(encoding='utf-8'))))
DOMESTIC=build(DATA)
BILATERAL=bilateral_build(DATA)


class DomesticTransactions(unittest.TestCase):
    def setUp(self):self.r=Runtime(DOMESTIC,BILATERAL)
    def vars(self):return self.r.vars['ISR']
    def complete(self,slug):self.r.run('ISR2_domestic_complete_'+slug)
    def quote(self,cost,kind=1,proc=0):
        self.vars().update(ISR2_project_cost=Decimal(str(cost)),ISR2_project_class=Decimal(kind),ISR2_project_quote=Decimal(10),ISR2_project_procurement=Decimal(proc))
        self.r.run('ISR2_project_support_quote')
    def fund(self,amount):
        self.r.flags['ISR']['ISR2_b_financing_usa_signed']=None
        self.vars()['ISR2_b_financing_usa_days']=Decimal(300)
        self.vars()['ISR2_b_financing_usa_unallocated']=Decimal(str(amount))
        self.r.run('ISR2_private_recalculate')
    def test_input_immutable_and_native217(self):
        before=deepcopy(DATA);build(DATA);self.assertEqual(DATA,before)
        result=arrange(DATA);self.assertEqual(audit(result)['nodes'],217);self.assertEqual(audit(result)['edges'],245)
        for path,source in DOMESTIC['files'].items():self.assertTrue(source.startswith('# IMPERIA COLD WAR'));parse(source)
    def test_native_resource_trigger_keywords_match_current_md_providers(self):
        code=DOMESTIC['files']['common/scripted_triggers/ISR2_domestic_triggers.txt']
        self.assertIn('has_political_power < 30',code);self.assertIn('has_stability < 0.03',code)
        self.assertNotRegex(code,r'\b(?:political_power|stability)\s*[<>=]')
        root=Path(__file__).resolve().parents[2]
        self.assertRegex((root/'common/scripted_triggers/99_BOS_scripted_triggers.txt').read_text(encoding='utf-8-sig'),r'\bhas_political_power\s*>')
        self.assertRegex((root/'common/national_focus/05_israel.txt').read_text(encoding='utf-8-sig'),r'\bhas_stability\s*>')
    def test_timed_dictionary_flag_without_explicit_value_is_inactive(self):
        self.r.execute(parse('set_country_flag = { flag = ISR2_fixture_missing_value days = 70 }'))
        self.assertFalse(self.r.test(parse('has_country_flag = ISR2_fixture_missing_value')))
        self.r.execute(parse('set_country_flag = { flag = ISR2_fixture_active value = 1 days = 2 }'))
        self.assertTrue(self.r.test(parse('has_country_flag = ISR2_fixture_active')))
        self.r.days(1);self.assertTrue(self.r.test(parse('has_country_flag = ISR2_fixture_active')))
        self.r.days(1);self.assertFalse(self.r.test(parse('has_country_flag = ISR2_fixture_active')))
    def test_all_six_domestic_timed_flags_have_explicit_native_value(self):
        found={}
        def inspect(rows):
            for key,op,val in rows:
                if key=='set_country_flag' and isinstance(val,list) and one(val,'days') is not None:
                    self.assertEqual(one(val,'value'),'1',one(val,'flag'))
                    found[one(val,'flag')]=int(one(val,'days'))
                elif isinstance(val,list):inspect(val)
        for path,source in DOMESTIC['files'].items():
            if '/scripted_effects/' in path:inspect(parse(source))
        self.assertEqual(found,{
            'ISR2_domestic_security_emergency':70,
            'ISR2_domestic_cooldown_development_repayment':182,
            'ISR2_domestic_cooldown_reserve_exercise':182,
            'ISR2_domestic_cooldown_security_emergency':180,
            'ISR2_domestic_cooldown_reserve_callup':70,
            'ISR2_domestic_cooldown_reserve_release':70})
    def test_negative_money_previews_use_scalar_temp_assignment_then_negation(self):
        checked=0
        def inspect(rows):
            nonlocal checked
            for key,op,val in rows:
                if key=='set_temp_variable':
                    self.assertTrue(all(not isinstance(v,list) for k,o,v in val));checked+=1
                elif isinstance(val,list):inspect(val)
        for a in DOMESTIC['actions'].values():inspect(parse(a['preview']))
        self.assertGreater(checked,5)
        self.assertIn('multiply_temp_variable = { treasury_change = -1 }',DOMESTIC['actions']['ISR2_sapir_book']['preview'])
        self.assertIn('multiply_temp_variable = { debt_change = -1 }',DOMESTIC['actions']['ISR2_development_repayment']['preview'])
    def test_grant_only_housing_actual_cost_no_cash(self):
        self.complete('absorption_appeal');self.assertEqual(self.vars()['treasury'],5)
        self.quote('.1',2);self.assertEqual(self.vars()['ISR2_project_net_cost'],Decimal('.1'))
        self.quote('.1');balance=self.vars()['ISR2_domestic_absorption_balance'];self.r.run('ISR2_project_support_quote')
        self.assertEqual(self.vars()['ISR2_domestic_absorption_balance'],balance)
        self.r.run('ISR2_project_support_commit');self.assertEqual(self.vars()['ISR2_domestic_absorption_balance'],Decimal('.3'))
        self.assertEqual(self.vars()['treasury'],5)
        self.complete('absorption_appeal');self.assertEqual(self.vars()['ISR2_domestic_absorption_balance'],Decimal('.3'))
    def test_real_match_pool_two_capped_projects(self):
        self.complete('national_bargain');self.assertEqual(self.vars()['treasury'],5)
        self.assertNotIn('ISR2_domestic_done_national_bargain',self.r.flags['ISR'])
        self.fund('.05');self.complete('national_bargain')
        self.assertEqual(self.vars()['treasury'],Decimal('4.95'));self.assertEqual(self.vars()['ISR2_b_financing_usa_unallocated'],0)
        for _ in range(2):
            self.quote('.08');self.assertEqual(self.vars()['ISR2_project_net_cost'],Decimal('.03'));self.r.run('ISR2_project_support_commit')
        self.quote('.08');self.assertEqual(self.vars()['ISR2_project_net_cost'],Decimal('.08'))
        self.assertEqual(self.vars()['ISR2_domestic_civilian_projects'],0)
    def test_small_project_consumes_only_real_support(self):
        self.fund('.05');self.complete('gahal_settlement_match');self.quote('.01',2);self.r.run('ISR2_project_support_commit')
        self.assertEqual(self.vars()['ISR2_domestic_settlement_balance'],Decimal('.09'))
        self.assertEqual(self.vars()['ISR2_domestic_settlement_projects'],1)
        self.assertEqual(self.vars()['ISR2_project_net_cost'],0)
    def test_match_cannot_fund_both_exclusive_envelopes(self):
        self.fund('.1');self.complete('national_bargain');self.complete('gahal_settlement_match')
        self.assertEqual(self.vars()['treasury'],Decimal('4.95'));self.assertEqual(self.vars()['ISR2_domestic_settlement_balance'],0)
        self.assertEqual(self.vars()['ISR2_b_financing_usa_unallocated'],Decimal('.05'))
    def test_tender_rechecks_owner_capacity_funding_and_replay(self):
        self.fund('.15');self.r.states['205']['controller']='EGY';self.r.completed.add('ISR2_sapir_book')
        self.complete('sapir_book');self.assertEqual(self.vars()['treasury'],5);self.assertNotIn('ISR2_sapir_book',self.r.completed)
        self.r.states['205']['controller']='ISR';self.r.states['205']['factories']=50;self.complete('sapir_book');self.assertEqual(self.vars()['treasury'],5)
        self.r.states['205']['factories']=1;self.complete('sapir_book');self.complete('sapir_book')
        self.assertEqual(self.vars()['treasury'],Decimal('4.925'));self.assertEqual(self.r.states['205']['factories'],2);self.assertEqual(self.r.states['205']['slots'],6)
        self.complete('sapir_negev');self.assertEqual(self.vars()['ISR2_b_financing_usa_unallocated'],0)
    def test_completed_receipt_replay_preserves_badge_and_assets(self):
        self.fund('.075');self.complete('sapir_book');self.r.completed.add('ISR2_sapir_book')
        before=deepcopy(self.r.states);cash=self.vars()['treasury'];self.complete('sapir_book')
        self.assertIn('ISR2_sapir_book',self.r.completed);self.assertEqual(before,self.r.states);self.assertEqual(cash,self.vars()['treasury'])
    def test_refresh_and_reinitialization_never_advance_calendar_or_replay_cash(self):
        self.r.war=True;self.complete('reserve_callup');self.complete('absorption_appeal')
        days=self.vars()['ISR2_domestic_callup_days'];cash=self.vars()['treasury'];balance=self.vars()['ISR2_domestic_absorption_balance']
        for _ in range(6):self.r.run('ISR2_domestic_refresh');self.r.run('ISR2_domestic_init')
        self.assertEqual(days,self.vars()['ISR2_domestic_callup_days']);self.assertEqual(cash,self.vars()['treasury'])
        self.assertEqual(balance,self.vars()['ISR2_domestic_absorption_balance'])
    def test_anonymous_repayment_and_named_credit_are_not_duplicated(self):
        self.vars()['debt']=Decimal('.3');self.vars()['ISR2_bilateral_loan_outstanding']=Decimal('.15')
        self.vars()['ISR2_b_eastern_credit_interest_remaining']=Decimal('.01');self.vars()['ISR2_b_eastern_credit_weeks_remaining']=Decimal(100)
        self.r.run('ISR2_domestic_refresh_prices');self.complete('development_repayment')
        self.assertEqual(self.vars()['treasury'],Decimal('4.8'));self.assertEqual(self.vars()['debt'],Decimal('.1'))
        self.assertEqual(self.r.vars['SOV']['treasury'],Decimal('.05'));self.assertEqual(self.vars()['ISR2_bilateral_loan_outstanding'],Decimal('.1'))
        self.complete('development_repayment');self.assertEqual(self.vars()['treasury'],Decimal('4.8'))
    def test_suspended_named_claim_cannot_be_retired_anonymously(self):
        self.vars()['debt']=Decimal('.2');self.vars()['ISR2_bilateral_loan_outstanding']=Decimal('.2')
        self.r.overrides['ISR2_b_eastern_credit_pair_clear']=False;self.r.run('ISR2_domestic_refresh_prices');self.complete('development_repayment')
        self.assertEqual(self.vars()['debt'],Decimal('.2'));self.assertEqual(self.vars()['treasury'],5)
    def test_procurement_single_use_only_uncompleted_project(self):
        self.r.completed.add('ISR2_tal_tank');self.complete('labor_procurement_ceiling')
        self.assertNotIn('ISR2_domestic_tank_coupon',self.r.flags['ISR'])
        self.quote('.18',0,2);self.assertEqual(self.vars()['ISR2_project_net_cost'],Decimal('.13'));self.r.run('ISR2_project_support_commit')
        self.quote('.18',0,2);self.assertEqual(self.vars()['ISR2_project_net_cost'],Decimal('.18'))
        self.r.run('ISR2_domestic_init');self.assertNotIn('ISR2_domestic_aircraft_coupon',self.r.flags['ISR'])
    def test_reserve_exercise_calendar_and_full_repeated_cost(self):
        self.complete('bounded_callup');self.complete('reserve_exercise')
        self.assertEqual(self.vars()['ISR2_domestic_exercise_days'],28);self.assertEqual(self.r.xp,20)
        self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_reserve_exercise'),182)
        self.r.days(28);self.assertNotIn('ISR2_domestic_exercise',self.r.modifiers['ISR'])
        prior=self.vars()['treasury'];self.complete('reserve_exercise')
        self.assertEqual(self.vars()['treasury'],prior);self.assertEqual(self.r.xp,20)
        self.r.days(153);self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_reserve_exercise'),1)
        self.complete('reserve_exercise');self.assertEqual(self.r.xp,20);self.assertEqual(self.vars()['treasury'],prior)
        self.r.days(1);self.assertNotIn('ISR2_domestic_cooldown_reserve_exercise',self.r.flags['ISR'])
        self.complete('reserve_exercise')
        self.assertEqual(self.r.xp,40);self.assertEqual(self.vars()['treasury'],prior-Decimal('.02'))
    def test_calendar_shortens_existing_exercise_by_seven_days(self):
        self.complete('reserve_exercise');self.r.days(10);self.complete('bounded_callup')
        self.assertEqual(self.vars()['ISR2_domestic_exercise_days'],18)
        self.r.days(18);self.assertNotIn('ISR2_domestic_exercise',self.r.modifiers['ISR'])
    def test_real_cabinet_gate_cost_expiry_and_cooldown(self):
        self.complete('reserve_callup');self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0)
        self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],70);self.assertEqual(self.vars()['stability'],Decimal('.47'))
        self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_security_emergency'),70)
        self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_security_emergency'),180)
        self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],70)
        self.complete('reserve_callup');self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],Decimal('.004'))
        self.r.days(69);self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_security_emergency'),1)
        self.assertEqual(self.vars()['ISR2_domestic_callup_days'],1)
        self.r.days(1);self.assertNotIn('ISR2_domestic_security_emergency',self.r.flags['ISR'])
        self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],0);self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0)
        self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],70)
        self.r.days(109);self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_security_emergency'),1)
        self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],70)
        self.r.days(1);self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],40)
    def test_callup_cooldown_survives_early_release_until_day70(self):
        self.r.war=True;self.complete('reserve_callup')
        self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_reserve_callup'),70)
        self.r.days(1);self.complete('reserve_release')
        self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0)
        self.complete('reserve_callup');self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0)
        self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],0)
        self.r.days(68);self.assertEqual(self.r.flags['ISR'].get('ISR2_domestic_cooldown_reserve_callup'),1)
        self.complete('reserve_callup');self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0)
        self.r.days(1);self.complete('reserve_callup')
        self.assertEqual(self.vars()['ISR2_domestic_callup_days'],70)
        self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],Decimal('.004'))
    def test_cabinet_insufficient_political_power_does_not_pay_partial_cost(self):
        self.vars()['political_power']=Decimal('29.5');self.complete('security_emergency')
        self.assertEqual(self.vars()['political_power'],Decimal('29.5'));self.assertEqual(self.vars()['stability'],Decimal('.5'))
        self.assertNotIn('ISR2_domestic_security_emergency',self.r.flags['ISR'])
        self.vars()['political_power']=Decimal(30);self.vars()['stability']=Decimal('.03')
        self.complete('security_emergency');self.assertEqual(self.vars()['political_power'],0);self.assertEqual(self.vars()['stability'],0)
        self.assertIn('ISR2_domestic_security_emergency',self.r.flags['ISR'])
    def test_release_and_war_end_remove_all_effects_and_cost(self):
        self.r.war=True;self.complete('reserve_exercise');self.complete('reserve_callup')
        self.assertEqual(self.vars()['ISR2_domestic_exercise_days'],0);self.assertIn('ISR2_domestic_callup',self.r.modifiers['ISR'])
        self.complete('reserve_release');self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],0);self.assertNotIn('ISR2_domestic_callup',self.r.modifiers['ISR'])
        self.r.days(70);self.complete('reserve_callup');self.r.war=False;self.r.days(1)
        self.assertEqual(self.vars()['ISR2_domestic_callup_days'],0);self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],0)
    def test_homefront_real_tech_slot_and_idempotent_stream(self):
        self.complete('home_front');self.assertEqual(self.vars()['treasury'],Decimal('4.92'))
        self.assertEqual(self.r.states['204']['slots'],6);self.assertIn('ISR2_homefront_medical_protocol',self.r.technologies['ISR'])
        for _ in range(4):self.r.run('ISR2_domestic_refresh')
        self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],Decimal('.001'))
        self.r.states['204']['controller']='EGY';self.r.run('ISR2_domestic_refresh');self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],0)
        self.r.states['204']['controller']='ISR';self.r.run('ISR2_domestic_refresh');self.assertEqual(self.r.states['204']['slots'],6)
        self.assertEqual(self.vars()['ISR2_domestic_weekly_expense'],Decimal('.001'))


if __name__=='__main__':unittest.main(verbosity=2)
