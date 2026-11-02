# IMPERIA COLD WAR — Economic reform previews, sale settlement and political support.
import copy
import json
import re
import unittest

import validate as V

LOC=dict(re.findall(r'^ (\w+): "(.*)"$',(V.ROOT/'localisation/english/ICW_economic_organisation_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
FUNCTIONS={V.first(body,'name'):body for key,op,body in V.ASTS['common/scripted_localisation/ICW_economic_organisation.txt'] if key=='defined_text'}


def country(position=20, gdp=100):
    c=V.Country();c.variables.update(gdp_total=gdp,treasury=10)
    c.call('icw_econ_initialize')
    c.variables.update(icw_econ_position=position,icw_econ_market_high_water=position)
    c.call('icw_econ_refresh_tier')
    return c


def localised(function,c):
    matches=[V.first(choice,'localization_key') for choice in V.vals(FUNCTIONS[function],'text')
             if c.test(V.first(choice,'trigger',[]))]
    return matches


def finish(c):
    for _ in range(90):c.call('icw_econ_daily')


def ready(c):
    for _ in range(90):c.call('icw_econ_daily')


class ReformTests(unittest.TestCase):
    def test_every_position_and_reform_has_exact_target_and_delta(self):
        positions=list(range(-100,101))+[-70.001,-40.001,-15.001,14.999,39.999,69.999]
        for position in positions:
            c=country(position)
            current=next(t for t in V.TIERS if t[2]<=position<t[3])
            for index,(slug,name,delta,cost,description) in enumerate(V.REFORMS,1):
                c.variables['icw_econ_selected_reform']=index
                future=max(-100,min(100,position+delta))
                target=next(t for t in V.TIERS if t[2]<=future<t[3])
                # Target-name selectors intentionally choose first matching range.
                self.assertEqual(localised('icw_econ_target_name_'+slug,c)[0],'icw_econ_'+target[0])
                self.assertEqual(localised('icw_econ_delta_'+slug,c),['icw_econ_delta_'+current[0]+'_'+target[0]])
                self.assertAlmostEqual(c.number('icw_econ_target_'+slug),future)
                self.assertEqual(len(localised('icw_econ_selected_changes',c)),1)

    def test_tooltips_have_no_literal_key_substitution(self):
        for slug,*_ in V.REFORMS:
            text=LOC['icw_econ_decision_'+slug+'_desc']
            self.assertNotRegex(text,r'\$icw_econ_')
            self.assertIn('[icw_econ_target_name_'+slug+']',text)
            self.assertIn('[icw_econ_delta_'+slug+']',text)
        for value in LOC.values():
            for function in re.findall(r'\[(icw_econ_\w+)\]',value):
                self.assertIn(function,FUNCTIONS)
        self.assertEqual(LOC['icw_econ_delta_regulated_regulated'],LOC['icw_econ_no_modifier_change'])

    def test_sale_pays_once_on_completion_at_starting_quote(self):
        c=country();c.call('icw_econ_start_privatisation')
        self.assertAlmostEqual(c.number('icw_econ_pending_sale'),.5)
        self.assertEqual(c.number('treasury'),10)
        c.variables['gdp_total']=200
        for _ in range(89):c.call('icw_econ_daily')
        self.assertEqual(c.number('treasury'),10)
        finish_state=copy.deepcopy(c.__dict__)
        resumed=V.Country();resumed.__dict__=finish_state
        resumed.call('icw_econ_initialize');resumed.call('icw_econ_daily')
        self.assertEqual(resumed.number('treasury'),10.5)
        self.assertEqual(resumed.number('icw_econ_market_high_water'),30)
        resumed.call('icw_econ_complete_reform')
        self.assertEqual(resumed.number('treasury'),10.5)
        self.assertEqual(resumed.number('icw_econ_pending_sale'),0)

    def test_nationalise_and_resell_does_not_generate_money(self):
        c=country();c.call('icw_econ_start_privatisation');finish(c);ready(c)
        c.call('icw_econ_start_ownership');finish(c);ready(c)
        self.assertEqual(c.number('icw_econ_position'),20)
        c.call('icw_econ_start_privatisation')
        self.assertEqual(c.number('icw_econ_pending_sale'),0)
        finish(c);ready(c)
        self.assertEqual(c.number('treasury'),10.5)
        c.call('icw_econ_start_privatisation');finish(c)
        self.assertEqual(c.number('treasury'),11)

    def test_partial_new_range_and_already_reformed_range(self):
        for previous_peak,expected in [(35,.25),(40,0),(55,0)]:
            c=country(30);c.variables['icw_econ_market_high_water']=previous_peak
            c.call('icw_econ_start_privatisation')
            self.assertAlmostEqual(c.number('icw_econ_pending_sale'),expected)
            finish(c)
            self.assertAlmostEqual(c.number('treasury'),10+expected)
            self.assertEqual(c.number('icw_econ_market_high_water'),max(previous_peak,40))
        for position,expected in [(95,.25),(100,0)]:
            c=country(position)
            self.assertEqual(c.number('icw_econ_sale_quote'),expected)

    def test_preview_does_not_claim_sale_or_charge_money(self):
        c=country();before=copy.deepcopy(c.__dict__)
        c.run([('effect_tooltip','=',[('icw_econ_preview_privatisation','=','yes')])])
        self.assertEqual(c.__dict__,before)
        c.variables['gdp_total']=300;c.call('icw_econ_update_preview')
        self.assertEqual(c.number('treasury'),10)
        self.assertEqual(c.number('icw_econ_market_high_water'),20)
        self.assertEqual(c.number('icw_econ_sale_quote'),1.5)

    def test_rejected_and_concurrent_starts_do_not_change_snapshot(self):
        c=country();c.variables['political_power']=49
        before=copy.deepcopy(c.__dict__);c.call('icw_econ_start_privatisation')
        self.assertEqual(c.__dict__,before)
        c.variables['political_power']=1000;c.call('icw_econ_start_privatisation')
        before=copy.deepcopy(c.__dict__)
        for slug,*_ in V.REFORMS:c.call('icw_econ_start_'+slug)
        self.assertEqual(c.__dict__,before)

    def test_other_market_reforms_do_not_pay_or_reopen_old_sales(self):
        c=country(20);c.call('icw_econ_start_autonomy');finish(c)
        self.assertEqual(c.number('treasury'),10)
        self.assertEqual(c.number('icw_econ_market_high_water'),25)
        c.variables['icw_econ_position']=20;c.call('icw_econ_refresh_tier');ready(c)
        c.call('icw_econ_start_privatisation');finish(c)
        self.assertEqual(c.number('treasury'),10.25)

    def test_existing_save_migration_does_not_reset_live_reform(self):
        c=country(35);c.flags.discard('icw_econ_sale_initialized')
        c.flags.add('icw_econ_reform_active')
        c.variables.update(icw_econ_pending_position=45,icw_econ_days_remaining=40,icw_econ_cooldown_days=130)
        c.call('icw_econ_initialize')
        self.assertEqual(c.number('icw_econ_market_high_water'),35)
        self.assertEqual(c.number('icw_econ_days_remaining'),40)
        self.assertEqual(c.number('icw_econ_pending_position'),45)
        self.assertEqual(c.number('treasury'),10)

    def test_subject_approval_and_cash_belong_to_applicant(self):
        s,p=country(),country();s.tag='SUB';p.tag='PAR';world={'SUB':s,'PAR':p};events=[]
        for c in (s,p):c.context.update(world=world,events=events)
        s.context['parent']='PAR';s.call('icw_econ_start_privatisation')
        self.assertEqual(s.number('treasury'),10)
        self.assertEqual(s.number('icw_econ_pending_sale'),0)
        p.context['targets']=events[0]['targets']
        p.run([('event_target:icw_econ_applicant','=',[('icw_econ_approve_privatisation','=','yes')])])
        self.assertEqual(s.number('political_power'),950)
        self.assertEqual(p.number('political_power'),1000)
        finish(s)
        self.assertEqual(s.number('treasury'),10.5)
        self.assertEqual(p.number('treasury'),10)

    def test_outer_tiers_add_native_daily_support_only(self):
        expected={'command':('communism_drift',.02),'planning':('communism_drift',.01),
                  'liberal':('democratic_drift',.01),'laissez':('democratic_drift',.02)}
        for slug,idea in V.IDEAS.items():
            stage=slug.removeprefix('icw_econ_');mods=V.first(idea,'modifier')
            for key in ('democratic_drift','communism_drift'):
                value=float(V.first(mods,key,0))
                self.assertEqual(value,expected[stage][1] if stage in expected and expected[stage][0]==key else 0)
        self.assertIn('Daily Western Support: §G+0.01§!',LOC['icw_econ_effects_liberal'])
        self.assertIn('Daily Emerging Support: §G+0.02§!',LOC['icw_econ_effects_command'])


if __name__=='__main__':unittest.main()
