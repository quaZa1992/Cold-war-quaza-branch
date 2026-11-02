# IMPERIA COLD WAR — Emitted Israel V2 bilateral transaction model checks.
"""Execute the generated Clausewitz subset, not a second contract implementation.

These checks establish script structure and accounting in a deterministic model.
They do not establish native engine event delivery, UI rendering or MP stability.
"""
import copy
import json
from pathlib import Path
import re
import unittest
from decimal import Decimal

import runtime_bilateral as generator

ROOT = Path(__file__).resolve().parents[2]


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|>=|<=|!=|[{}=<>]|[^\s{}=<>]+', re.sub(r'#[^\n]*', '', text))
    cursor = 0

    def block(closing=False):
        nonlocal cursor
        result = []
        while cursor < len(tokens):
            if tokens[cursor] == '}':
                if not closing:
                    raise AssertionError('Unexpected closing brace')
                cursor += 1
                return result
            key, op = tokens[cursor:cursor+2]
            if op not in ('=', '>', '<', '>=', '<=', '!='):
                raise AssertionError((key, op))
            cursor += 2
            if tokens[cursor] == '{':
                cursor += 1
                value = block(True)
            else:
                value = tokens[cursor]
                cursor += 1
            result.append((key, op, value))
        if closing:
            raise AssertionError('Unclosed block')
        return result
    return block()


def field(body, name, default=None):
    return next((v for k, _, v in body if k == name), default)


def native_block(text, name):
    start = re.search(r'^'+re.escape(name)+r'\s*=\s*\{',text,re.M).start()
    depth=0
    for i in range(text.index('{',start),len(text)):
        if text[i]=='{': depth+=1
        elif text[i]=='}':
            depth-=1
            if not depth: return parse(text[start:i+1])[0][2]
    raise AssertionError('Unclosed native helper '+name)


class Model:
    """Strict executor of the emitted effects and their actual native helpers."""
    def __init__(self, output):
        self.effects = dict((k, v) for k, _, v in parse(output['files']['common/scripted_effects/ISR2_bilateral_effects.txt']))
        self.triggers = dict((k, v) for k, _, v in parse(output['files']['common/scripted_triggers/ISR2_bilateral_triggers.txt']))
        native = (ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8')
        for key in ('modify_treasury_effect', 'modify_debt_effect', 'modify_international_investment_effect'):
            self.effects[key] = native_block(native,key)
        self.tags = ('ISR',) + generator.PARTNERS
        self.vars = {t:dict(treasury=Decimal('100'), debt=Decimal('10'), gdp_total=Decimal('10'), int_investments=Decimal('0')) for t in self.tags}
        self.temp = {t:{} for t in self.tags}
        self.flags = {t:{} for t in self.tags}
        self.ideas = {t:set() for t in self.tags}
        self.arrays = {t:{} for t in self.tags}
        self.equipment = {t:2000 for t in self.tags}
        self.alive = set(self.tags)
        self.original_tags={tag:tag for tag in self.tags}
        self.wars, self.embargoes = set(), set()
        self.events, self.reopened, self.techs = [], [], []
        self.day, self.depth = 0, 0
        self.parties, self.disabled_parties = set(),set()
        for group in json.loads((ROOT/'tools/israel_v2/design.json').read_text(encoding='utf-8'))['groups']:
            if group.get('runtime_party_trigger'):
                self.parties.add(group['runtime_party_trigger'])

    def number(self, value, tag):
        if isinstance(value, list):
            result = self.number(field(value, 'value', '0'), tag)
            for key, _, v in value:
                if key == 'value':
                    continue
                if key == 'clamp':
                    result = max(self.number(field(v,'min'),tag), min(result,self.number(field(v,'max'),tag)))
                elif key == 'multiply': result *= self.number(v,tag)
                elif key == 'divide': result /= self.number(v,tag)
                elif key == 'add': result += self.number(v,tag)
                elif key == 'subtract': result -= self.number(v,tag)
                else: raise AssertionError(('math',key))
            return result
        try:
            return Decimal(value)
        except Exception:
            if value.startswith('modifier@'): return Decimal('0')
            if value == 'global.roi_rate_cap': return Decimal('.25')
            if '.' in value and value.split('.')[0] in self.tags:
                country, name = value.split('.',1)
                return self.temp[country].get(name,self.vars[country].get(name,Decimal(0)))
            return self.temp[tag].get(value,self.vars[tag].get(value,Decimal(0)))

    def test(self, body, tag='ISR', any_of=False):
        results = []
        for k, op, v in body:
            if k == 'AND': result = self.test(v,tag)
            elif k == 'OR': result = self.test(v,tag,True)
            elif k == 'NOT': result = not self.test(v,tag)
            elif k == 'always': result = v == 'yes'
            elif k == 'ISR2_is_scenario': result = tag == 'ISR' and self.original_tags.get(tag)== 'ISR' and 'ISR' in self.alive
            elif k == 'IMP_is_1970_scenario': result = True
            elif k in self.parties: result = k not in self.disabled_parties
            elif k in self.triggers: result = self.test(self.triggers[k],tag)
            elif k in self.tags: result = k in self.alive and self.test(v,k)
            elif k == 'country_exists': result = v in self.alive
            elif k == 'tag': result = tag == v
            elif k == 'has_country_flag': result = v in self.flags[tag]
            elif k == 'has_variable': result = v in self.vars[tag] or v in self.temp[tag]
            elif k == 'has_idea': result = v in self.ideas[tag]
            elif k == 'custom_trigger_tooltip': result = self.test([x for x in v if x[0]!='tooltip'],tag)
            elif k in ('has_active_mission','is_debug','has_dynamic_modifier'): result = False
            elif k == 'is_ai': result = True
            elif k == 'has_war_with': result = (tag,v) in self.wars or (v,tag) in self.wars
            elif k == 'is_embargoing': result = (tag,v) in self.embargoes
            elif k == 'is_in_array': result = field(v,'value') in self.arrays[tag].get(field(v,'array'),set())
            elif k == 'has_equipment':
                _, compare, quantity = v[0]
                result = self.compare(self.equipment[tag],compare,self.number(quantity,tag))
            elif k == 'check_variable':
                if field(v,'var') is not None:
                    name, quantity = field(v,'var'),field(v,'value')
                    compare={'greater_than_or_equals':'>=','less_than_or_equals':'<='}[field(v,'compare')]
                else: name, compare, quantity = v[0]
                result = self.compare(self.number(name,tag),compare,self.number(quantity,tag))
            else: raise AssertionError(('trigger',k))
            results.append(result)
        return any(results) if any_of else all(results)

    @staticmethod
    def compare(left, op, right):
        return {'=':left==right,'!=':left!=right,'>':left>right,'<':left<right,'>=':left>=right,'<=':left<=right}[op]

    def call(self, name, tag='ISR'):
        self.depth += 1
        if self.depth > 40: raise AssertionError('Recursive scripted effect')
        self.run(self.effects[name],tag)
        self.depth -= 1

    def run(self, body, tag='ISR'):
        previous_if = None
        for k, _, v in body:
            if k == 'if':
                previous_if = self.test(field(v,'limit'),tag)
                if previous_if: self.run([x for x in v if x[0]!='limit'],tag)
            elif k == 'else':
                if previous_if is False: self.run(v,tag)
                previous_if = None
            elif k == 'else_if':
                if previous_if is False:
                    previous_if = self.test(field(v,'limit'),tag)
                    if previous_if: self.run([x for x in v if x[0]!='limit'],tag)
            elif k in self.tags:
                if k in self.alive: self.run(v,k)
            elif k in self.effects: self.call(k,tag)
            elif k in ('hidden_effect',): self.run(v,tag)
            elif k in ('effect_tooltip','custom_effect_tooltip','update_money_dirty_variable','ingame_update_setup','log'): pass
            elif k in ('set_variable','set_temp_variable','add_to_variable','subtract_from_variable'):
                name, _, value = v[0]
                if name == 'var': name, value = field(v,'var'),field(v,'value')
                amount = self.number(value,tag)
                destination = self.temp[tag] if k == 'set_temp_variable' else self.vars[tag]
                if k == 'add_to_variable': amount = self.number(name,tag)+amount
                if k == 'subtract_from_variable': amount = self.number(name,tag)-amount
                destination[name] = amount
            elif k in ('clamp_variable','clamp_temp_variable'):
                name = field(v,'var')
                destination=self.temp[tag] if k=='clamp_temp_variable' else self.vars[tag]
                destination[name] = max(self.number(field(v,'min','-1000000'),tag), min(self.number(name,tag),self.number(field(v,'max','1000000'),tag)))
            elif k in ('subtract_from_temp_variable','add_to_temp_variable','multiply_temp_variable','multiply_variable'):
                name,_,value=v[0];amount=self.number(value,tag)
                old=self.number(name,tag)
                destination=self.temp[tag] if 'temp' in k else self.vars[tag]
                destination[name]=old-amount if k.startswith('subtract') else old+amount if k.startswith('add') else old*amount
            elif k == 'clear_variable': self.vars[tag].pop(v,None)
            elif k == 'set_country_flag':
                if isinstance(v,list):
                    name=field(v,'flag')
                    if self.number(field(v,'value','0'),tag)==0:self.flags[tag].pop(name,None)
                    else:self.flags[tag][name]=self.day+int(field(v,'days','999999'))
                else: self.flags[tag][v] = None
            elif k == 'clr_country_flag': self.flags[tag].pop(v,None)
            elif k == 'add_ideas': self.ideas[tag].add(v)
            elif k == 'remove_ideas': self.ideas[tag].discard(v)
            elif k == 'country_event': self.events.append((tag,field(v,'id')))
            elif k == 'uncomplete_national_focus': self.reopened.append((tag,field(v,'focus')))
            elif k == 'send_equipment':
                amount, target = int(field(v,'amount')),field(v,'target')
                assert self.equipment[tag]>=amount
                self.equipment[tag]-=amount; self.equipment[target]+=amount
            elif k in ('army_experience','air_experience'):
                self.vars[tag][k] = self.vars[tag].get(k,Decimal(0))+self.number(v,tag)
            elif k == 'add_tech_bonus': self.techs.append((tag,field(v,'category')))
            elif k == 'add_opinion_modifier': pass
            else: raise AssertionError(('effect',k))

    def advance(self, days=1):
        for _ in range(days):
            self.day += 1
            for tag in self.tags:
                self.temp[tag].clear()
                self.flags[tag] = {k:v for k,v in self.flags[tag].items() if v is None or v>self.day}
            self.call('ISR2_bilateral_daily')

    def accept(self, slug):
        self.call('ISR2_b_'+slug+'_offer')
        self.call('ISR2_b_'+slug+'_accept')


class BilateralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads((ROOT/'tools/israel_v2/design.json').read_text(encoding='utf-8'))
        cls.data = generator.extend_data(cls.original)
        cls.output = generator.build(cls.data)

    def model(self):
        result=Model(self.output);result.call('ISR2_bilateral_init');return result

    def test_emitter_is_pure_and_deterministic(self):
        snapshot=copy.deepcopy(self.original)
        data=generator.extend_data(self.original);before=copy.deepcopy(data)
        self.assertEqual(generator.build(data),self.output)
        self.assertEqual(data,before);self.assertEqual(self.original,snapshot)
        self.assertEqual(generator.extend_data(data),data)
        self.assertEqual(len(self.output['actions']),18)

    def test_native_files_parse_markers_precision_and_no_decisions(self):
        for path,text in self.output['files'].items():
            self.assertTrue(text.startswith('# IMPERIA COLD WAR — '),path)
            self.assertFalse(text.startswith('\ufeff'),path)
            self.assertNotIn('decisions/',path)
            self.assertFalse(re.search(r'(?<![\w.])\d*\.\d{6,}(?![\w.])',text),path)
            parse(text)
        events=parse(self.output['files']['events/ISR2_bilateral_events.txt'])
        self.assertEqual(len([x for x in events if x[0]=='country_event']),18)

    def test_all_offers_are_pure_until_actual_acceptance(self):
        for node in [n for n in self.data['nodes'] if n.get('offer_target')]:
            m=self.model();m.vars['ISR']['ISR2_territories_pressure_208']=Decimal(2)
            before=copy.deepcopy((m.vars,m.ideas,m.equipment,m.techs))
            slug=node['id'][5:];p='ISR2_b_'+slug
            m.call(p+'_preview');self.assertEqual((m.vars,m.ideas,m.equipment,m.techs),before)
            m.call(p+'_offer')
            for tag in m.tags:
                for key in ('treasury','debt','int_investments'):
                    self.assertEqual(m.vars[tag][key],before[0][tag][key],node['id'])
            self.assertEqual(m.events,[(node['offer_target']['tag'],'ISR2_bilateral.'+str([x['id'] for x in self.data['nodes'] if x.get('offer_target')].index(node['id'])+1))])
            m.call(p+'_accept');after=copy.deepcopy((m.vars,m.ideas,m.equipment,m.techs))
            m.call(p+'_accept');self.assertEqual((m.vars,m.ideas,m.equipment,m.techs),after)

    def test_changed_funds_refusal_and_pending_timeout_do_not_charge(self):
        m=self.model();m.call('ISR2_b_financing_usa_offer');m.vars['USA']['treasury']=Decimal('.01')
        m.call('ISR2_b_financing_usa_accept')
        self.assertEqual(m.vars['USA']['treasury'],Decimal('.01'))
        self.assertNotIn('ISR2_b_financing_usa_signed',m.flags['ISR'])
        m.call('ISR2_b_irrigation_exports_offer');m.call('ISR2_b_irrigation_exports_decline')
        self.assertEqual(m.vars['ISR']['treasury'],Decimal(100))
        m.call('ISR2_b_mashav_offer');m.advance(30)
        self.assertNotIn('ISR2_b_mashav_pending',m.flags['ISR'])
        self.assertEqual(m.vars['ISR']['treasury'],Decimal(100))

    def test_real_governing_party_rechecked_on_offer_and_on_acceptance(self):
        m=self.model();m.disabled_parties.add('emerging_communist_state_are_in_power')
        m.call('ISR2_b_eastern_credit_offer');self.assertEqual(m.events,[])
        m.disabled_parties.clear();m.call('ISR2_b_eastern_credit_offer')
        m.disabled_parties.add('emerging_communist_state_are_in_power')
        m.call('ISR2_b_eastern_credit_accept')
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],0)
        self.assertEqual(m.vars['SOV']['treasury'],100)

    def test_prospective_previews_keep_offer_snapshots_separate(self):
        text=self.output['files']['common/scripted_effects/ISR2_bilateral_effects.txt']
        for node in [n for n in self.data['nodes'] if n.get('offer_target')]:
            p='ISR2_b_'+node['id'][5:]
            preview=native_block(text,p+'_preview')
            tooltip=field(preview,'effect_tooltip')
            self.assertIsNotNone(field(tooltip,'ISR'))
            self.assertIsNotNone(field(tooltip,node['offer_target']['tag']))
            actual=next(v for k,_,v in parse(text) if k==p+'_preview')
            def traverse(block):
                for key,_,value in block:
                    self.assertNotEqual(key,'set_variable',p)
                    if isinstance(value,list): traverse(value)
            traverse(actual)
            for variable in ('gdp','partner_gdp','setup_isr','setup_partner','weekly_isr','weekly_partner'):
                self.assertIn(f'{p}_pv_{variable} = {p}_{variable}',text)

    def test_invoice_margin_expiry_and_reconcile_idempotence(self):
        m=self.model();m.accept('irrigation_exports')
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('100.004'))
        self.assertEqual(m.vars['ETH']['treasury'],Decimal('99.994'))
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],Decimal('.00002'))
        before=copy.deepcopy(m.vars)
        m.call('ISR2_bilateral_reconcile');m.call('ISR2_bilateral_reconcile')
        self.assertEqual(m.vars,before)
        m.advance(728)
        self.assertNotIn('ISR2_b_irrigation_exports_partner_idea',m.ideas['ETH'])
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],0)
        self.assertEqual(Decimal('.006')-Decimal('.002')-104*Decimal('.00002'),Decimal('.00192'))

    def test_every_mirrored_sanction_suspends_then_restores_without_setup(self):
        for who,other in [('ISR','ETH'),('ETH','ISR')]:
            for array in generator.SANCTIONS:
                m=self.model();m.accept('irrigation_exports');paid=copy.deepcopy(m.vars)
                m.arrays[who][array]={other};m.call('ISR2_bilateral_reconcile')
                self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],0)
                self.assertNotIn('ISR2_b_irrigation_exports_partner_idea',m.ideas['ETH'])
                m.arrays[who][array]=set();m.call('ISR2_bilateral_reconcile')
                self.assertEqual(m.vars,paid)
        m=self.model();m.accept('irrigation_exports')
        for flag in ('disabled_economic_system',):
            m.flags['ETH'][flag]=None;m.call('ISR2_bilateral_reconcile')
            self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],0)

    def test_real_equipment_and_one_order_shared_across_all_offers(self):
        m=self.model();m.equipment['ISR']=0;m.call('ISR2_b_arms_exports_offer')
        m.call('ISR2_b_arms_congo_offer');self.assertEqual(len(m.events),1)
        m.call('ISR2_b_arms_exports_accept')
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('100.006'))
        self.assertNotIn('army_experience',m.vars['ISR'])
        m.advance(1);self.assertEqual(m.equipment['UGA'],2000)
        m.equipment['ISR']=1000;m.advance(1)
        self.assertEqual((m.equipment['ISR'],m.equipment['UGA']),(0,3000))
        self.assertEqual(m.vars['ISR']['army_experience'],5)
        m.call('ISR2_b_arms_exports_end');self.assertEqual(m.vars['UGA']['treasury'],Decimal('99.99'))
        m.advance(364);m.accept('arms_exports');m.advance(182)
        self.assertEqual(m.vars['UGA']['treasury'],Decimal('99.99'))
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('100.002'))

    def test_project_capital_real_funding_fifo_no_second_debit_and_unused_return(self):
        m=self.model();m.accept('financing_usa');m.advance(10);m.accept('financing_ger')
        self.assertEqual(m.vars['ISR']['treasury'],100)
        self.assertEqual(m.vars['USA']['treasury'],Decimal('99.8'))
        self.assertEqual(m.vars['USA']['int_investments'],Decimal('.2'))
        m.vars['ISR']['ISR2_private_required']=Decimal('.25');m.call('ISR2_private_commit')
        self.assertEqual(m.vars['ISR']['ISR2_private_paid'],Decimal('.25'))
        self.assertEqual(m.vars['ISR']['ISR2_private_paid_USA'],Decimal('.2'))
        self.assertEqual(m.vars['ISR']['ISR2_private_paid_GER'],Decimal('.05'))
        self.assertEqual(m.vars['ISR']['ISR2_private_paid_ROM'],0)
        self.assertEqual(m.vars['ISR']['ISR2_b_financing_usa_unallocated'],0)
        self.assertEqual(m.vars['ISR']['ISR2_b_financing_ger_unallocated'],Decimal('.15'))
        self.assertEqual(m.vars['USA']['treasury'],Decimal('99.8'))
        m.vars['ISR']['ISR2_private_required']=Decimal('.16');m.call('ISR2_private_commit')
        self.assertEqual(m.vars['ISR']['ISR2_private_paid'],0)
        self.assertTrue(all(m.vars['ISR']['ISR2_private_paid_'+t]==0 for t in generator.FINANCIERS))
        self.assertEqual(m.vars['ISR']['ISR2_b_financing_ger_unallocated'],Decimal('.15'))
        m.advance(364)
        self.assertEqual(m.vars['GER']['treasury'],Decimal('99.95'))
        self.assertEqual(m.vars['GER']['int_investments'],Decimal('.05'))
        self.assertEqual(m.vars['USA']['int_investments'],Decimal('.2'))
        self.assertEqual(m.vars['ISR']['ISR2_private_available'],0)
        before=copy.deepcopy(m.vars);m.call('ISR2_b_financing_ger_end');m.call('ISR2_b_financing_ger_return_unused')
        self.assertEqual(m.vars,before)

    def test_inactive_capital_cannot_be_spent_and_dead_country_return_is_preserved(self):
        m=self.model();m.accept('financing_rom');m.wars.add(('ISR','ROM'))
        m.vars['ISR']['ISR2_private_required']=Decimal('.1');m.call('ISR2_private_commit')
        self.assertEqual(m.vars['ISR']['ISR2_private_paid'],0)
        m.alive.remove('ROM');m.advance(364)
        self.assertEqual(m.vars['ISR']['ISR2_b_financing_rom_unallocated'],Decimal('.2'))
        self.assertIn('ISR2_b_financing_rom_refund_due',m.flags['ISR'])
        m.alive.add('ROM');m.advance(1)
        self.assertEqual(m.vars['ROM']['treasury'],100)
        self.assertEqual(m.vars['ROM']['int_investments'],0)

    def test_loan_exact_104_atomic_settlements_and_no_duplicate_budget_stream(self):
        m=self.model();m.accept('eastern_credit')
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('100.4'))
        self.assertEqual(m.vars['ISR']['debt'],Decimal('10.4'))
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],0)
        m.advance(728)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],0)
        self.assertAlmostEqual(m.vars['ISR']['debt'],Decimal(10),places=5)
        self.assertAlmostEqual(m.vars['ISR']['treasury'],Decimal('99.968'))
        self.assertAlmostEqual(m.vars['SOV']['treasury'],Decimal('100.032'))

    def test_loan_war_and_funds_failure_keep_principal_then_early_repayment(self):
        m=self.model();m.accept('eastern_credit');m.wars.add(('ISR','SOV'));m.advance(30)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],Decimal('.4'))
        m.wars.clear();m.vars['ISR']['treasury']=Decimal('0');m.advance(7)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],Decimal('.4'))
        m.vars['ISR']['treasury']=Decimal(1);m.vars['ISR']['ISR2_bilateral_early_repayment']=Decimal('.2');m.call('ISR2_bilateral_loan_early_repay')
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],Decimal('.2'))
        self.assertEqual(m.vars['ISR']['ISR2_b_eastern_credit_interest_remaining'],Decimal('.016'))
        m.advance(728)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],0)
        self.assertAlmostEqual(m.vars['ISR']['debt'],Decimal(10),places=5)

    def test_pal_relief_needs_actual_pressure_and_municipal_family_replaces(self):
        m=self.model();m.call('ISR2_b_negotiated_terms_offer');self.assertEqual(m.events,[])
        m.vars['ISR']['ISR2_territories_pressure_208']=Decimal(1);m.vars['ISR']['ISR2_territories_pressure_209']=Decimal(2)
        m.accept('negotiated_terms')
        self.assertEqual(m.vars['ISR']['ISR2_pal_service_relief_state'],209)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_weekly_expense'],Decimal('.002'))
        self.assertEqual(m.vars['PAL']['ISR2_bilateral_weekly_income'],Decimal('.002'))
        m.accept('gahal_local_autonomy');m.accept('haolam_joint_services')
        self.assertNotIn('ISR2_b_gahal_local_autonomy_isr_idea',m.ideas['ISR'])
        self.assertIn('ISR2_b_haolam_joint_services_isr_idea',m.ideas['ISR'])

    def test_daily_is_idempotent_within_same_day_and_mashav_lesson_once(self):
        m=self.model();m.accept('mashav');m.accept('mashav_ethiopia')
        self.assertEqual(m.techs.count(('ISR','CAT_agriculture')),1)
        m.advance(1);before=copy.deepcopy(m.vars);m.call('ISR2_bilateral_daily');self.assertEqual(m.vars,before)

    def test_claim_credits_actual_investors_and_retires_only_affected_principal_once(self):
        m=self.model();m.accept('financing_usa');m.accept('financing_ger')
        m.vars['ISR']['ISR2_private_required']=Decimal('.25');m.call('ISR2_private_commit')
        m.vars['ISR'].update(ISR2_private_claim_id=Decimal(1),ISR2_private_claim_amount=Decimal('.4'))
        for tag in generator.FINANCIERS:
            m.vars['ISR']['ISR2_private_claim_share_'+tag]=m.vars['ISR']['ISR2_private_paid_'+tag]
        treasury=m.vars['ISR']['treasury'];m.call('ISR2_private_claim_credit')
        self.assertEqual(m.vars['USA']['treasury'],Decimal('100.12'))
        self.assertEqual(m.vars['GER']['treasury'],Decimal('99.88'))
        self.assertEqual(m.vars['USA']['int_investments'],0)
        self.assertEqual(m.vars['GER']['int_investments'],Decimal('.15'))
        self.assertEqual(m.vars['ISR']['treasury'],treasury)
        before=copy.deepcopy(m.vars);m.call('ISR2_private_claim_credit')
        before['ISR']['ISR2_private_claim_registered_amount']=Decimal(0)
        self.assertEqual(m.vars,before)

    def test_dead_claim_recipient_retains_both_cash_and_retirement_obligation(self):
        m=self.model();m.accept('financing_rom')
        m.vars['ISR']['ISR2_private_required']=Decimal('.1');m.call('ISR2_private_commit')
        m.alive.remove('ROM');m.vars['ISR'].update(ISR2_private_claim_id=Decimal(3),ISR2_private_claim_amount=Decimal('.16'),ISR2_private_claim_share_ROM=Decimal('.1'))
        m.call('ISR2_private_claim_credit')
        self.assertEqual(m.vars['ISR']['ISR2_private_claim_due_ROM'],Decimal('.16'))
        self.assertEqual(m.vars['ISR']['ISR2_private_retire_due_ROM'],Decimal('.1'))
        self.assertEqual(m.vars['ROM']['int_investments'],Decimal('.2'))
        m.alive.add('ROM');m.advance(1)
        self.assertEqual(m.vars['ROM']['treasury'],Decimal('99.96'))
        self.assertEqual(m.vars['ROM']['int_investments'],Decimal('.1'))
        before=copy.deepcopy(m.vars);m.call('ISR2_private_claim_settle');self.assertEqual(m.vars,before)

    def test_last_claim_recipient_receives_exact_rounding_remainder(self):
        m=self.model();m.vars['ISR'].update(ISR2_private_claim_id=Decimal(2),ISR2_private_claim_amount=Decimal('.00013'))
        for tag,amount in zip(generator.FINANCIERS,('.00001','.00002','.00004')):
            m.vars['ISR']['ISR2_private_claim_share_'+tag]=Decimal(amount)
        m.call('ISR2_private_claim_credit')
        self.assertEqual(m.vars['ISR']['ISR2_private_claim_remainder'],0)
        self.assertAlmostEqual(sum(m.vars[tag]['treasury']-100 for tag in generator.FINANCIERS),Decimal('.00013'),places=5)

    def test_refresh_never_advances_time_or_loan_settlement(self):
        m=self.model();m.accept('eastern_credit');m.call('ISR2_b_mashav_offer');m.advance(6)
        before=copy.deepcopy(m.vars)
        for _ in range(20): m.call(self.output['refresh'].split(' = ')[0])
        self.assertEqual(m.vars,before)

    def test_timed_flag_zero_default_and_explicit_cooldown_expiry(self):
        m=self.model()
        m.run(parse('set_country_flag = { flag = missing_value days = 14 }'))
        self.assertNotIn('missing_value',m.flags['ISR'])
        m.run(parse('set_country_flag = { flag = explicit_value value = 1 days = 14 }'))
        m.advance(13)
        self.assertIn('explicit_value',m.flags['ISR'])
        m.advance(1)
        self.assertNotIn('explicit_value',m.flags['ISR'])

    def test_native_cost_skip_never_mints_investments_or_loses_a_return_claim(self):
        m=self.model();m.flags['USA']['MD_skip_treasury_cost']=None
        m.call('ISR2_b_financing_usa_offer');self.assertEqual(m.events,[])
        m.flags['USA'].clear();m.call('ISR2_b_financing_usa_offer')
        m.flags['USA']['MD_skip_treasury_cost']=None;m.call('ISR2_b_financing_usa_accept')
        self.assertEqual(m.vars['USA']['int_investments'],0)
        m.flags['USA'].clear();m.advance(14);m.accept('financing_usa')
        m.flags['USA']['MD_skip_treasury_cost']=None;m.advance(364)
        self.assertEqual(m.vars['ISR']['ISR2_b_financing_usa_unallocated'],Decimal('.2'))
        self.assertEqual(m.vars['USA']['treasury'],Decimal('99.8'))
        m.flags['USA'].clear();m.advance(1)
        self.assertEqual(m.vars['USA']['treasury'],100)
        self.assertEqual(m.vars['USA']['int_investments'],0)

    def test_undelivered_invoice_return_survives_recipient_absence(self):
        m=self.model();m.equipment['ISR']=0;m.accept('arms_exports');m.alive.remove('UGA');m.advance(182)
        self.assertIn('ISR2_b_arms_exports_invoice_refund_due',m.flags['ISR'])
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('100.006'))
        m.alive.add('UGA');m.advance(1)
        self.assertEqual(m.vars['ISR']['treasury'],Decimal('99.996'))
        self.assertEqual(m.vars['UGA']['treasury'],100)
        before=copy.deepcopy(m.vars);m.call('ISR2_b_arms_exports_return_invoice');self.assertEqual(m.vars,before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
