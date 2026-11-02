# IMPERIA COLD WAR — Native money patch and protected-loan cashflow checks.
"""Execute emitted native AST providers; this is not a live HOI4 test."""
import json
from decimal import Decimal
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import runtime_money as money
import runtime_bilateral as bilateral
from test_runtime_bilateral import Model,parse,native_block,field


def section(text,name):
    pattern=re.escape(money.PREFIX+'['+name+'] BEGIN\n')+r'(.*?)'+re.escape(money.PREFIX+'['+name+'] END')
    return re.search(pattern,text,re.S)[1]


class MoneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output=money.integrate()
        data=bilateral.extend_data(json.loads((money.ROOT/'tools/israel_v2/design.json').read_text(encoding='utf-8')))
        cls.bilateral=bilateral.build(data)

    def model(self):
        m=Model(self.bilateral)
        files=self.output['files']
        utility=files[money.PATHS[2]]
        for name in ('ai_repay_debt','repay_manual_debt_effect','ISR2_money_quote_unprotected_debt','ISR2_money_clamp_repayment','ISR2_money_preserve_principal'):
            m.effects[name]=native_block(utility,name)
        m.effects['modify_debt_effect']=native_block(files[money.PATHS[1]],'modify_debt_effect')
        m.triggers['ISR2_money_has_protected_loan']=native_block(files['common/scripted_triggers/ISR2_money_triggers.txt'],'ISR2_money_has_protected_loan')
        m.effects['calculate_interest_rate']=[]  # External macro is tested via its actual consumer below.
        m.effects['ISR2_refresh']=[]
        m.call('ISR2_bilateral_init')
        return m

    def test_exact_reversible_patches_and_repeated_build(self):
        installed=self.output['files']
        for path in money.PATHS:
            current=(money.ROOT/path).read_text(encoding='utf-8-sig')
            self.assertEqual(money.clean(installed[path]),money.clean(current),path)
            self.assertTrue(installed[path].startswith(money.HEADER))
            self.assertFalse(installed[path].startswith('\ufeff'))
        old=Path.read_text
        def read(path,*args,**kwargs):
            try: relative=path.relative_to(money.ROOT).as_posix()
            except ValueError: return old(path,*args,**kwargs)
            return installed[relative] if relative in money.PATHS else old(path,*args,**kwargs)
        with patch.object(Path,'read_text',read):
            rebuilt=money.integrate()
        self.assertEqual(rebuilt['files'],installed)

    def test_four_streams_once_zero_reset_and_missing_variables(self):
        for kind in ('income','expense'):
            m=self.model()
            for i,component in enumerate(('core','domestic','territories','bilateral'),1):
                m.vars['ISR']['ISR2_'+component+'_weekly_'+kind]=Decimal(i)/100
            target='additional_income_rate' if kind=='income' else 'additional_expenses_rate'
            code=parse(section(self.output['files'][money.PATHS[0]],kind+' streams'))
            for _ in range(3):
                m.vars['ISR'][target]=Decimal('.7');m.run(code)
                self.assertEqual(m.vars['ISR'][target],Decimal('.8'))
                self.assertEqual(m.vars['ISR']['ISR2_money_weekly_'+kind],Decimal('.1'))
            # A fixed foreign partner has no unrelated Israeli output variables.
            for component in ('core','domestic','territories'):
                m.vars['GER'].pop('ISR2_'+component+'_weekly_'+kind,None)
            m.vars['GER']['ISR2_bilateral_weekly_'+kind]=Decimal('.03')
            m.vars['GER'][target]=Decimal('.4');m.run(code,'GER')
            self.assertEqual(m.vars['GER'][target],Decimal('.43'))
        expenses=self.output['files'][money.PATHS[0]]
        self.assertLess(expenses.index('multiply_variable = { additional_expenses_rate = additional_expenses_inflation }'),expenses.index(money.PREFIX+'[expense streams] BEGIN'))

    def test_interest_exclusion_consumes_actual_native_formula_with_fx(self):
        m=self.model();m.vars['ISR'].update(debt=Decimal(10),interest_rate=Decimal(5),debt_fx_factor=Decimal('1.7'),ISR2_bilateral_loan_outstanding=Decimal(4))
        block=native_block(self.output['files'][money.PATHS[0]],'calculate_interest_rate')
        def find(rows):
            for key,_,value in rows:
                if key=='set_variable' and isinstance(value,list) and value[0][0]=='debt_rate' and isinstance(value[0][2],list): return [(key,'=',value)]
                if isinstance(value,list):
                    found=find(value)
                    if found:return found
        consumer=find(block);self.assertIsNotNone(consumer)
        m.run(consumer)
        self.assertEqual(m.vars['ISR']['debt_rate'],Decimal('.01615'))
        hook=parse(section(self.output['files'][money.PATHS[0]],'exclude contracted interest'))
        m.run(hook);self.assertEqual(m.vars['ISR']['debt_rate'],Decimal('.00969'))
        m.vars['ISR']['debt_rate']=Decimal('.00001');m.run(hook)
        self.assertEqual(m.vars['ISR']['debt_rate'],0)

    def test_manual_repayment_clamped_before_cash_and_native_non_israel_preserved(self):
        for tag,outstanding,expected in [('ISR','4','4'),('GER','0','0')]:
            m=self.model();m.vars[tag].update(debt=Decimal(10),treasury=Decimal(100),ISR2_bilateral_loan_outstanding=Decimal(outstanding),repay_debt_max=Decimal(1))
            m.call('repay_manual_debt_effect',tag)
            self.assertEqual(m.vars[tag]['debt'],Decimal(expected))
            self.assertEqual(m.vars[tag]['treasury'],Decimal(90)+Decimal(expected))

    def test_AI_full_treasury_still_preserves_principal_and_pays_ordinary_remainder(self):
        for debt,outstanding in [('10','4'),('.40001','.4'),('4','4'),('.00041','.0004')]:
            m=self.model();m.vars['ISR'].update(debt=Decimal(debt),treasury=Decimal(100),treasury_rate=Decimal(1),display_expense=Decimal('.1'),ISR2_bilateral_loan_outstanding=Decimal(outstanding))
            m.call('ai_repay_debt')
            self.assertEqual(m.vars['ISR']['debt'],Decimal(outstanding))
            self.assertEqual(m.vars['ISR']['treasury'],100-Decimal(debt)+Decimal(outstanding))
        m=self.model();m.vars['GER'].update(debt=Decimal(10),treasury=Decimal(100),treasury_rate=Decimal(1))
        m.call('ai_repay_debt','GER');self.assertEqual(m.vars['GER']['debt'],0);self.assertEqual(m.vars['GER']['treasury'],90)

    def test_generic_writeoff_has_no_cash_refund_and_named_loan_can_reduce_principal(self):
        m=self.model();m.vars['ISR'].update(debt=Decimal(10),ISR2_bilateral_loan_outstanding=Decimal(4))
        m.temp['ISR']['debt_change']=Decimal(-100);m.call('modify_debt_effect')
        self.assertEqual(m.vars['ISR']['debt'],4);self.assertEqual(m.vars['ISR']['treasury'],100)
        m.vars['ISR']['ISR2_bilateral_principal_reduction']=Decimal(1);m.call('ISR2_bilateral_apply_principal_reduction')
        self.assertEqual(m.vars['ISR']['debt'],3)
        self.assertNotIn('ISR2_bilateral_authorized_principal',m.flags['ISR'])

    def test_actual_loan_104_settlements_survive_the_writeoff_guard(self):
        m=self.model();m.accept('eastern_credit');m.advance(728)
        self.assertEqual(m.vars['ISR']['ISR2_bilateral_loan_outstanding'],0)
        self.assertAlmostEqual(m.vars['ISR']['debt'],Decimal(10),places=5)
        self.assertAlmostEqual(m.vars['ISR']['treasury'],Decimal('99.968'),places=5)
        self.assertAlmostEqual(m.vars['SOV']['treasury'],Decimal('100.032'),places=5)

    def test_human_automatic_cash_consumer_is_clamped_before_both_subtractions(self):
        text=self.output['files'][money.PATHS[3]]
        m=self.model();m.vars['ISR'].update(debt=Decimal(5),ISR2_bilateral_loan_outstanding=Decimal(4),treasury_rate=Decimal(20))
        m.temp['ISR'].update(treasury_rate_gain=Decimal(20),treasury_rate_debt_payment=Decimal(5))
        m.run(parse(section(text,'automatic weekly payment clamp')))
        self.assertEqual(m.temp['ISR']['treasury_rate_debt_payment'],1)
        m.run(parse('subtract_from_variable = { debt = treasury_rate_debt_payment } subtract_from_temp_variable = { treasury_rate_gain = treasury_rate_debt_payment }'))
        self.assertEqual(m.vars['ISR']['debt'],4);self.assertEqual(m.temp['ISR']['treasury_rate_gain'],19)
        self.assertLess(text.index('[automatic weekly payment clamp] BEGIN'),text.index('subtract_from_variable = { debt = treasury_rate_debt_payment }'))

    def test_only_comparators_supported_by_native_script_parser(self):
        for text in self.bilateral['files'].values():
            self.assertNotIn('>=',text);self.assertNotIn('<=',text)
        for action in self.bilateral['actions'].values():
            self.assertTrue(action['visible_available'])
            self.assertNotIn('always = yes',action['visible_available'])

    def test_civilwar_clone_cannot_charge_copied_streams_or_inherit_actor_authority(self):
        m=self.model();m.tags=m.tags+('D01',)
        for mapping in (m.vars,m.temp,m.flags,m.ideas,m.arrays,m.equipment):
            original=mapping['ISR']
            mapping['D01']=original.copy() if hasattr(original,'copy') else original
        m.alive.add('D01');m.original_tags['D01']='ISR'
        for tag in ('ISR','GER','D01'):
            for kind in ('income','expense'):
                for component in ('core','domestic','territories','bilateral'):
                    m.vars[tag]['ISR2_'+component+'_weekly_'+kind]=Decimal('.1')
                target='additional_income_rate' if kind=='income' else 'additional_expenses_rate'
                m.vars[tag][target]=Decimal('.5')
                m.run(parse(section(self.output['files'][money.PATHS[0]],kind+' streams')),tag)
                self.assertEqual(m.vars[tag][target],{'ISR':Decimal('.9'),'GER':Decimal('.6'),'D01':Decimal('.5')}[tag])


if __name__=='__main__':
    unittest.main(verbosity=2)
