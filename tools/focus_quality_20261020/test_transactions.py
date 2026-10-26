# IMPERIA CW — Cold War: focus quality 20261020 — test transactions.
"""Execute real emitted transaction ASTs against bounded test country states."""
import importlib.util
import sys
import unittest
from source_edit import ROOT
from script_model import Model, State, D, parse, walk, first

sys.path.insert(0,str(ROOT/'Claude outputs/COLDWAR_GEN_generator'))
from gen_quality import OFFICE_PROJECTS, prefix

P='COLDWAR_DDR_Q_'


class Transactions(unittest.TestCase):
    def test_repayment_cash_equals_principal_and_once(self):
        m=Model();d=m.countries['DDR']
        m.call(P+'open_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(7),D(47)))
        self.assertEqual(d.ideas[P+'creditworthiness'],730)
        self.assertEqual(d.vars['COLDWAR_DDR_planned_economy_imp_sanction_resistance'],D('.08'))
        m.call(P+'open_repayment');m.call(P+'finish_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(7),D(47)))

    def test_repayment_caps_at_remaining_debt(self):
        m=Model();d=m.countries['DDR'];d.vars['debt']=D('1.2')
        m.call(P+'open_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D('8.8'),D(0)))

    def test_repayment_does_not_borrow_or_grant_unfunded_rewards(self):
        m=Model();d=m.countries['DDR'];d.vars['treasury']=D(2)
        m.call(P+'open_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(2),D(50)))
        self.assertNotIn(P+'creditworthiness',d.ideas)
        self.assertIn(P+'repayment_open',d.flags)
        d.vars['treasury']=D(3);m.call(P+'finish_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(0),D(47)))

    def test_confirmation_preserves_quote_if_gdp_changes(self):
        m=Model();d=m.countries['DDR'];d.flags.add(P+'repayment_open')
        m.call(P+'prepare_repayment');d.vars['gdp_total']=D(200)
        m.call(P+'finish_repayment')
        self.assertEqual(d.vars['debt'],D(47))

    def test_confirmation_rejects_outdated_quote_if_principal_falls(self):
        m=Model();d=m.countries['DDR'];d.flags.add(P+'repayment_open')
        m.call(P+'prepare_repayment');d.vars['debt']=D(1)
        m.call(P+'finish_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(10),D(1)))
        m.call(P+'prepare_repayment');m.call(P+'finish_repayment')
        self.assertEqual((d.vars['treasury'],d.vars['debt']),(D(9),D(0)))

    def test_no_debt_no_payment_or_bonus(self):
        for debt in [0,-1]:
            m=Model();d=m.countries['DDR'];d.vars['debt']=D(debt)
            m.call(P+'open_repayment')
            self.assertEqual(d.vars['treasury'],D(10));self.assertFalse(d.ideas)

    def import_setup(self, stock=90):
        m=Model();m.countries['SOV'].stock=D(stock);m.call(P+'start_import')
        return m

    def test_import_moves_real_stock_and_entire_price_once(self):
        m=self.import_setup();d=m.countries['DDR'];s=m.countries['SOV']
        self.assertEqual(d.xp,D(25));m.call(P+'start_import');self.assertEqual(d.xp,D(25))
        m.call(P+'accept_import','SOV')
        self.assertEqual((s.stock,d.stock),(D(0),D(90)))
        self.assertEqual((s.vars['treasury'],d.vars['treasury']),(D(11),D(9)))
        m.call(P+'accept_import','SOV')
        self.assertEqual((s.stock,d.stock),(D(0),D(90)))
        self.assertEqual(d.vars['treasury'],D(9))

    def test_import_revalidates_stock_cash_pending_and_war(self):
        for failure in ['stock','cash','pending','war','done']:
            m=self.import_setup();d=m.countries['DDR'];s=m.countries['SOV']
            if failure=='stock':s.stock=D(89)
            if failure=='cash':d.vars['treasury']=D('.99')
            if failure=='pending':d.flags.discard(P+'trade_pending')
            if failure=='war':s.wars.add('DDR')
            if failure=='done':d.flags.add(P+'import_done')
            before=(s.stock,d.stock,s.vars['treasury'],d.vars['treasury'])
            m.call(P+'accept_import','SOV')
            self.assertEqual(before,(s.stock,d.stock,s.vars['treasury'],d.vars['treasury']),failure)

    def test_request_guard_and_frozen_price(self):
        m=self.import_setup();d=m.countries['DDR'];self.assertEqual(len(m.events),1)
        d.vars['gdp_total']=D(300);m.call(P+'request_import');self.assertEqual(len(m.events),1)
        self.assertEqual(d.vars[P+'import_price'],D(1))

    def licence_setup(self):
        m=Model();s=m.countries['SOV'];s.techs={'mbt_tech'};s.designs={'medium_tank_chassis_0'}
        m.call(P+'start_licence');return m

    def test_licence_design_factories_and_funds_once(self):
        m=self.licence_setup();d=m.countries['DDR'];s=m.countries['SOV']
        m.call(P+'accept_licence','SOV')
        self.assertIn('SOV',d.licenses);self.assertEqual(m.states[0].arms_factory,2)
        self.assertEqual((d.vars['treasury'],s.vars['treasury']),(D('8.4'),D('11.6')))
        self.assertEqual(d.vars['COLDWAR_DDR_planned_economy_military_factories_productivity'],D('.03'))
        m.call(P+'accept_licence','SOV');self.assertEqual(m.states[0].arms_factory,2)
        self.assertEqual(d.vars['treasury'],D('8.4'))

    def test_licence_falls_back_to_existing_older_design(self):
        m=self.licence_setup();m.date='1976.1.1';m.countries['SOV'].techs.add('mbt_tech_1')
        m.call(P+'accept_licence','SOV')
        self.assertIn('SOV',m.countries['DDR'].licenses)
        self.assertEqual(m.states[0].arms_factory,2)

    def test_licence_never_unlocks_future_tank_or_free_design(self):
        m=self.licence_setup();s=m.countries['SOV'];s.designs={'medium_tank_chassis_1'};s.techs={'mbt_tech_1'}
        m.call(P+'accept_licence','SOV')
        self.assertFalse(m.countries['DDR'].licenses)
        self.assertEqual(m.countries['DDR'].vars['treasury'],D(10));self.assertEqual(m.states[0].arms_factory,0)

    def test_existing_licence_allows_assembly_project(self):
        m=self.licence_setup();d=m.countries['DDR'];d.licenses.add('SOV');m.countries['SOV'].techs.clear()
        m.call(P+'accept_licence','SOV')
        self.assertEqual(m.states[0].arms_factory,2);self.assertEqual(d.vars['treasury'],D('8.4'))

    def test_licence_no_variant_no_money_or_factory(self):
        m=self.licence_setup();m.countries['SOV'].designs.clear()
        m.call(P+'accept_licence','SOV')
        self.assertEqual(m.countries['DDR'].vars['treasury'],D(10));self.assertEqual(m.states[0].arms_factory,0)
        self.assertNotIn(P+'licence_done',m.countries['DDR'].flags)

    def test_licence_revalidates_money_and_capacity(self):
        for failure in ['cash','slots','control','pending']:
            m=self.licence_setup();d=m.countries['DDR']
            if failure=='cash':d.vars['treasury']=D('1.59')
            if failure=='slots':m.states[0].slots=1
            if failure=='control':m.states[0].controller='SOV'
            if failure=='pending':d.flags.discard(P+'trade_pending')
            before=d.vars['treasury'];m.call(P+'accept_licence','SOV')
            self.assertEqual(d.vars['treasury'],before);self.assertFalse(d.licenses)
            self.assertEqual(m.states[0].arms_factory,0)

    def office_setup(self, fid='GEN_1970_wa_free_export_zones'):
        m=Model();party=OFFICE_PROJECTS[fid][1]
        if party:m.countries['DDR'].parties.add(party)
        return m,prefix(fid)

    def test_two_offices_in_one_state_exact_price(self):
        m,p=self.office_setup();m.states[0].slots=1
        m.call(p+'_open')
        self.assertEqual((m.states[0].offices,m.states[0].fossil_powerplant),(2,2))
        self.assertEqual(m.countries['DDR'].vars['treasury'],D('7.3'))
        m.call(p+'_open');m.call(p+'_finish')
        self.assertEqual(m.states[0].offices,2);self.assertEqual(m.countries['DDR'].vars['treasury'],D('7.3'))

    def test_partial_office_invoice_and_later_frozen_price(self):
        m,p=self.office_setup();d=m.countries['DDR'];d.vars['treasury']=D('1.5')
        m.call(p+'_open');self.assertEqual(m.states[0].offices,1);self.assertEqual(d.vars['treasury'],D('.15'))
        d.vars['treasury']=D(2);d.vars['gdp_total']=D(200);m.call(p+'_finish')
        self.assertEqual(m.states[0].offices,2);self.assertEqual(d.vars['treasury'],D('.65'))

    def test_power_capacity_blocks_only_unbuilt_phase(self):
        m,p=self.office_setup();m.states[0].fossil_powerplant=19;m.call(p+'_open')
        self.assertEqual(m.states[0].offices,1);self.assertEqual(m.countries['DDR'].vars['treasury'],D('8.65'))
        m.states[0].fossil_powerplant=18;m.call(p+'_finish');self.assertEqual(m.states[0].offices,2)

    def test_office_gates_preserve_money_and_partial_receipts(self):
        for failure in ['ownership','control','slots','government']:
            m,p=self.office_setup();d=m.countries['DDR']
            if failure=='ownership':m.states[0].owner='SOV'
            if failure=='control':m.states[0].controller='SOV'
            if failure=='slots':m.states[0].slots=0
            if failure=='government':d.parties.clear()
            m.call(p+'_open');self.assertEqual(d.vars['treasury'],D(10));self.assertEqual(m.states[0].offices,0)
            self.assertIn(p+'_pending',d.flags)

    def test_all_office_prices_and_base_fixed_fee(self):
        for fid,(share,_) in OFFICE_PROJECTS.items():
            m,p=self.office_setup(fid);d=m.countries['DDR'];d.vars['treasury']=D(100)
            m.call(p+'_open')
            expected=D(24) if share is None else D(str(share))*100
            self.assertEqual(d.vars['treasury'],D(100)-expected,fid)
            self.assertEqual(m.states[0].offices,2,fid)

    def test_native_skip_flag_cannot_create_unpaid_assets_or_debt_relief(self):
        m=Model();d=m.countries['DDR'];d.flags.add('MD_skip_treasury_cost')
        m.call(P+'open_repayment');self.assertEqual(d.vars['debt'],D(50));self.assertFalse(d.ideas)
        m,p=self.office_setup();m.countries['DDR'].flags.add('MD_skip_treasury_cost');m.call(p+'_open')
        self.assertEqual(m.states[0].offices,0);self.assertEqual(m.countries['DDR'].vars['treasury'],D(10))
        for tag in ['DDR','SOV']:
            m=self.import_setup();m.countries[tag].flags.add('MD_skip_treasury_cost');m.call(P+'accept_import','SOV')
            self.assertEqual(m.countries['DDR'].stock,D(0));self.assertEqual(m.countries['SOV'].stock,D(90))
            m=self.licence_setup();m.countries[tag].flags.add('MD_skip_treasury_cost');m.call(P+'accept_licence','SOV')
            self.assertEqual(m.states[0].arms_factory,0);self.assertFalse(m.countries['DDR'].licenses)

    def test_office_zero_gdp_can_recover_without_free_or_duplicate_assets(self):
        m,p=self.office_setup();d=m.countries['DDR'];d.vars['gdp_total']=D(0)
        m.call(p+'_open');self.assertEqual(m.states[0].offices,0);self.assertIn(p+'_pending',d.flags)
        d.vars['gdp_total']=D(100)
        self.assertTrue(m.condition(m.triggers[p+'_can_quote'],d))
        m.call(p+'_finish');self.assertEqual(m.states[0].offices,2);self.assertEqual(d.vars['treasury'],D('7.3'))
        m.call(p+'_finish');self.assertEqual(m.states[0].offices,2)

    def test_emitted_sources_have_correct_encodings_and_no_periodic_callback(self):
        paths=[p for base in ['common','events','localisation/english'] for p in (ROOT/base).rglob('*quality*') if p.is_file() and p.suffix in ['.txt','.yml'] and ('DDR_1970_quality' in p.name or 'GEN_1970_quality' in p.name)]
        self.assertEqual(len(paths),12)
        for p in paths:
            self.assertEqual(p.read_bytes().startswith(b'\xef\xbb\xbf'),p.suffix=='.yml',str(p))
            if p.suffix=='.txt':parse(p.read_text(encoding='utf-8'))
        for stem in ['COLDWAR_DDR_Q','COLDWAR_GEN_Q']:
            for p in (ROOT/'common/on_actions').glob('*.txt'):
                self.assertNotIn(stem,p.read_text(encoding='utf-8-sig'))


if __name__=='__main__':unittest.main(verbosity=2)
