# IMPERIA COLD WAR — Actual emitted MD missile, ceiling, historical and custom-paper tests
"""Source/AST tests. Does not start HOI4 or establish multiplayer synchronization."""
import copy
import json
import re
import unittest
from test_programmes import ProgrammeModel
from test_treaties import ROOT,HERE
from behavior_tests import parser


class MissileProtocols(unittest.TestCase):
    def model(self,n=12):
        m=ProgrammeModel()
        m.call(f'icwt_edit_{n}')
        return m

    def sign(self,m,n=12):
        m.call(f'icwt_send_{n}');m.call(f'icwt_review_{n}','SOV');m.call(f'icwt_sign_{n}','SOV')
        self.assertIn(f'icwt_spirit_{n}',m.ideas['USA'])
        self.assertIn(f'icwt_spirit_{n}',m.ideas['SOV'])

    def test_nuclear_selection_retires_actual_nuclear_capable_models_only(self):
        m=self.model();m.v['USA'].update(icwt_edit_scope=5,icwt_edit_reduction=25,icwt_edit_reserve_limit=1)
        for t in ('USA','SOV'):m.stocks[t].update(nuclear_missile_equipment_1=20,nuclear_ballistic_missile_equipment_5=10,ballistic_missile_equipment_1=30,guided_missile_equipment_6=40)
        self.sign(m)
        for t in ('USA','SOV'):
            self.assertEqual(m.stocks[t]['nuclear_missile_equipment_1'],15)
            self.assertEqual(m.stocks[t]['nuclear_ballistic_missile_equipment_5'],7)
            self.assertEqual(m.stocks[t]['ballistic_missile_equipment_1'],30)
            self.assertEqual(m.stocks[t]['guided_missile_equipment_6'],40)
            self.assertEqual(m.v[t]['icwt_cap_12'],22)

    def test_all_models_including_later_generations_are_real_and_synchronized(self):
        equipment={}
        for name in ('MD_nuclear_missiles.txt','MD_ballistic_missiles.txt','MD_guided_missiles.txt'):
            source=(ROOT/'common/units/equipment'/name).read_text(encoding='utf-8')
            for k,o,body in parser.parse(source):
                if k=='equipments':equipment.update({k:dict((k,v) for k,o,v in b) for k,o,b in body})
        tokens=[s for s in (ROOT/'common/synchronized_dynamic_tokens/ICW_superpower_treaties.txt').read_text().splitlines() if s and not s.startswith('#')]
        self.assertEqual(len(tokens),23)
        self.assertEqual(set(tokens),{e for e in equipment if re.fullmatch(r'(?:nuclear_missile|nuclear_ballistic_missile|ballistic_missile|guided_missile)_equipment_\d+',e)})
        for token in tokens:self.assertIn(token,equipment)
        for token in tokens:
            if token.startswith(('nuclear_missile_equipment_','nuclear_ballistic_missile_equipment_')):
                base=equipment[equipment[token]['archetype']]
                self.assertIn('drop_nuke',str(base['allow_mission_type']))
            else:
                self.assertNotIn('drop_nuke',str(equipment[equipment[token]['archetype']]['allow_mission_type']))
        inf_from_native={e for e in tokens if not e.startswith('nuclear_missile_equipment_') and 500<=int(equipment[e]['air_range'])<=5500}
        verify=self.model(4)
        for t in ('USA','SOV'):verify.stocks[t].update({e:1 for e in tokens})
        self.sign(verify,4)
        self.assertEqual({e for e in tokens if verify.stocks['USA'][e]==0},inf_from_native)
        m=self.model();m.v['USA'].update(icwt_edit_scope=4,icwt_edit_reduction=100)
        for t in ('USA','SOV'):
            m.stocks[t].update({e:3 for e in tokens});m.stocks[t]['sam_missile_equipment_1']=9
        self.sign(m)
        for t in ('USA','SOV'):
            self.assertTrue(all(m.stocks[t][e]==0 for e in tokens));self.assertEqual(m.stocks[t]['sam_missile_equipment_1'],9)

    def test_inf_template_uses_actual_loaded_range_not_just_nuclear_labels(self):
        m=self.model(4)
        for t in ('USA','SOV'):m.stocks[t].update(nuclear_missile_equipment_1=5,ballistic_missile_equipment_3=5,ballistic_missile_equipment_4=5,nuclear_ballistic_missile_equipment_2=5,nuclear_ballistic_missile_equipment_3=5,guided_missile_equipment_6=5)
        self.sign(m,4)
        for t in ('USA','SOV'):
            for e in ('ballistic_missile_equipment_3','nuclear_ballistic_missile_equipment_2','guided_missile_equipment_6'):self.assertEqual(m.stocks[t][e],0)
            for e in ('nuclear_missile_equipment_1','ballistic_missile_equipment_4','nuclear_ballistic_missile_equipment_3'):self.assertEqual(m.stocks[t][e],5)
            self.assertEqual(m.v[t]['icwt_cap_4'],0)

    def test_salt_freezes_reserves_and_does_not_destroy_them_on_open_or_send(self):
        m=self.model(1)
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=20
        before=copy.deepcopy((m.stocks,m.ideas))
        m.call('icwt_edit_1');m.call('icwt_send_1')
        self.assertEqual(before,(m.stocks,m.ideas))
        m.call('icwt_review_1','SOV');m.call('icwt_sign_1','SOV')
        for t in ('USA','SOV'):
            self.assertEqual(m.stocks[t]['nuclear_missile_equipment_1'],20);self.assertEqual(m.v[t]['icwt_cap_1'],20)
        self.assertEqual(m.v['global']['icwt_1_duration'],1825)

    def test_excess_pauses_real_programme_and_funding_and_can_be_dismantled_once(self):
        m=self.model(1);m.flags['USA'].add('icwt_programme_3_unlocked');m.v['USA'].update(icwt_edit_programme=3,icwt_edit_trade=2,icwt_edit_investment=1)
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=20
        self.sign(m,1);cash=copy.deepcopy(m.v['USA']['treasury'])
        m.stocks['SOV']['nuclear_missile_equipment_1']=21;m.call('icwt_weekly');m.call('icwt_programme_fiscal')
        self.assertIn('icwt_limit_broken_1',m.flags['SOV']);self.assertEqual(m.stocks['SOV']['nuclear_missile_equipment_1'],21)
        self.assertEqual(m.v['USA']['icwt_weekly_expense'],0);self.assertNotIn('icwt_programme_3_usa',m.ideas['USA'])
        self.assertEqual(m.v['USA']['icwt_investment@SOV'],0)
        m.call('icwt_restore_1','SOV');m.call('icwt_restore_1','SOV');m.call('icwt_programme_fiscal')
        self.assertEqual(m.stocks['SOV']['nuclear_missile_equipment_1'],20)
        self.assertIn('icwt_programme_3_usa',m.ideas['USA']);self.assertEqual(m.v['USA']['treasury'],cash)
        self.assertAlmostEqual(m.v['USA']['icwt_weekly_expense'],.0002)

    def test_modernisation_inside_aggregate_ceiling_is_allowed(self):
        m=self.model(1)
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=20
        self.sign(m,1);m.stocks['USA'].update(nuclear_missile_equipment_1=10,nuclear_missile_equipment_6=10,guided_missile_equipment_1=999)
        m.call('icwt_weekly');self.assertNotIn('icwt_limit_broken_1',m.flags['USA'])

    def test_pre_signature_stock_growth_aborts_every_party_transaction(self):
        m=self.model(1);m.flags['USA'].add('icwt_programme_3_unlocked');m.v['USA']['icwt_edit_programme']=3
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=20
        m.call('icwt_send_1');m.call('icwt_review_1','SOV');m.stocks['USA']['nuclear_missile_equipment_1']=21
        before=copy.deepcopy((m.stocks,m.ideas,m.v['USA']['treasury'],m.v['SOV']['treasury']))
        m.call('icwt_sign_1','SOV')
        self.assertEqual(before,(m.stocks,m.ideas,m.v['USA']['treasury'],m.v['SOV']['treasury']));self.assertEqual(m.v['global']['icwt_pending'],1)

    def test_legacy_coverage_does_not_silently_expand_to_new_equipment(self):
        m=self.model();m.v['USA'].update(icwt_edit_scope=2,icwt_edit_reduction=100,icwt_edit_missile_version=0,icwt_edit_reserve_limit=0)
        for t in ('USA','SOV'):m.stocks[t].update(nuclear_ballistic_missile_equipment_3=4,nuclear_ballistic_missile_equipment_5=4,ballistic_missile_equipment_4=4)
        self.sign(m)
        for t in ('USA','SOV'):
            self.assertEqual(m.stocks[t]['nuclear_ballistic_missile_equipment_3'],0)
            self.assertEqual(m.stocks[t]['nuclear_ballistic_missile_equipment_5'],4);self.assertEqual(m.stocks[t]['ballistic_missile_equipment_4'],4)

    def test_legacy_production_spirits_are_removed_without_imposing_new_missile_terms(self):
        m=self.model();m.a['global']['icwt_roster']=[1,2];m.a['global']['icwt_1_members']=[1,2]
        m.v['global'].update(icwt_1_revision=1,icwt_1_restraint=50)
        for t in ('USA','SOV'):
            m.flags[t].add('icwt_member_1');m.ideas[t].update({'icwt_spirit_1','icwt_restraint_50'});m.stocks[t]['nuclear_missile_equipment_1']=25
        before=copy.deepcopy(m.stocks);m.call('icwt_refresh')
        self.assertEqual(m.stocks,before)
        for t in ('USA','SOV'):
            self.assertNotIn('icwt_restraint_50',m.ideas[t]);self.assertIn('icwt_spirit_1',m.ideas[t]);self.assertNotIn('icwt_limit_broken_1',m.flags[t])
        ideas=(ROOT/'common/ideas/ICW_superpower_treaties.txt').read_text()
        self.assertNotIn('nuclear_production_factor',ideas);self.assertNotIn('thermonuclear_production_factor',ideas)

    def test_custom_paper_is_independent_and_has_real_consent_and_expiry(self):
        m=self.model();m.v['USA'].update(icwt_edit_scope=5,icwt_edit_reduction=10,icwt_edit_reserve_limit=1,icwt_edit_duration=180,icwt_edit_trade=2)
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=100
        self.sign(m);self.assertEqual(m.stocks['USA']['nuclear_missile_equipment_1'],90)
        self.assertFalse(any('icwt_spirit_'+str(n) in m.ideas['USA'] for n in range(1,12)))
        m.v['global']['num_days']+=180;m.call('icwt_weekly')
        self.assertNotIn('icwt_spirit_12',m.ideas['USA']);self.assertEqual(m.stocks['USA']['nuclear_missile_equipment_1'],90)

    def test_opening_a_custom_paper_cannot_overwrite_a_pending_proposal(self):
        m=self.model(1);m.call('icwt_send_1');before=copy.deepcopy((m.v['global'],m.stocks,m.ideas))
        m.call('icwt_open_custom');self.assertEqual(before,(m.v['global'],m.stocks,m.ideas))

    def test_late_invitee_must_review_its_own_current_ceiling(self):
        m=self.model(1);m.a['USA']['icwt_edit_invites']=[6]
        for t in ('USA','SOV','FRA'):m.stocks[t]['nuclear_missile_equipment_1']=10
        self.sign(m,1);m.call('icwt_review_1','FRA')
        m.stocks['FRA']['nuclear_missile_equipment_1']=11;m.call('icwt_accept_invite_1','FRA')
        self.assertNotIn('icwt_spirit_1',m.ideas['FRA'])
        m.call('icwt_review_1','FRA');m.call('icwt_accept_invite_1','FRA')
        self.assertIn('icwt_spirit_1',m.ideas['FRA']);self.assertEqual(m.v['FRA']['icwt_cap_1'],11)

    def test_old_unsigned_production_paper_requires_fresh_missile_terms(self):
        m=self.model(1)
        for t in ('USA','SOV'):m.stocks[t]['nuclear_missile_equipment_1']=20
        m.call('icwt_send_1');old=m.v['global']['icwt_p_revision']
        m.v['global'].update(icwt_p_restraint=25,icwt_p_reserve_limit=0,icwt_p_missile_version=0)
        m.call('icwt_review_1','SOV');m.call('icwt_sign_1','SOV')
        self.assertNotIn('icwt_spirit_1',m.ideas['SOV'])
        self.assertEqual(m.stocks['USA']['nuclear_missile_equipment_1'],20)
        m.call('icwt_counteroffer','SOV')
        self.assertEqual(m.v['SOV'].get('icwt_edit_restraint',0),0)
        self.assertEqual(m.v['SOV']['icwt_edit_missile_version'],1)
        m.v['SOV'].update(icwt_edit_reduction=25,icwt_edit_reserve_limit=1)
        m.call('icwt_send_1','SOV');self.assertNotEqual(m.v['global']['icwt_p_revision'],old)
        m.call('icwt_sign_1','USA');self.assertNotIn('icwt_spirit_1',m.ideas['USA'])
        m.call('icwt_review_1','USA');m.call('icwt_sign_1','USA')
        self.assertEqual(m.stocks['USA']['nuclear_missile_equipment_1'],15)
        self.assertEqual(m.v['USA']['icwt_cap_1'],15)

    def test_start_fifteen_year_term_and_four_row_register(self):
        m=self.model(5);self.sign(m,5)
        self.assertEqual(m.v['global']['icwt_5_end'],100+5475)
        def descendants(rows):
            for k,o,b in rows:
                yield k,o,b
                if isinstance(b,list):yield from descendants(b)
        scheduled=[dict((k,b) for k,o,b in v) for k,o,v in descendants(m.effects['icwt_sign_5']) if k=='country_event']
        self.assertIn({'id':'icwt.605','days':'5475'},scheduled)
        m.v['global']['num_days']=100+5474;m.call('icwt_weekly')
        self.assertIn('icwt_spirit_5',m.ideas['USA'])
        m.v['global']['num_days']+=1;m.call('icwt_weekly')
        self.assertNotIn('icwt_spirit_5',m.ideas['USA'])
        for n in range(1,13):m.v['USA'][f'icwt_receipt_{n}']=1
        m.v['USA'].update(icwt_register_offset=8,icwt_template=12);m.call('icwt_display')
        self.assertEqual(m.a['USA']['icwt_rows'],[9,10,11,12])
        self.assertEqual(m.v['USA']['icwt_register_next'],12)

    def test_standing_custom_paper_can_invite_through_actual_country_picker(self):
        m=self.model();self.sign(m)
        m.v['USA'].update(icwt_pick_role=4,icwt_picking_template=12);m.flags['USA'].add('icsd_picking')
        scripted=parser.parse((ROOT/'common/scripted_guis/ICW_superpower_dossier.txt').read_text())[0][2]
        picker=dict((k,b) for k,o,b in next(b for k,o,b in scripted if k=='icsd_picker'))
        click=next(b for k,o,b in picker['effects'] if k=='icsd_pick_use_click')
        m.run(click,('FRA','FRA','USA'))
        self.assertIn(6,m.a['global']['icwt_12_invites'])
        self.assertNotIn('icwt_spirit_12',m.ideas['FRA'])
        m.call('icwt_review_12','FRA');m.call('icwt_accept_invite_12','FRA')
        self.assertIn('icwt_spirit_12',m.ideas['FRA'])

    def test_editor_fields_and_historical_custom_buttons_have_complete_help(self):
        strings={k:v for k,v in re.findall(r'^\s*(\w+):\d*\s+"(.*)"\s*$',(ROOT/'localisation/english/ICW_superpower_dossier_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}
        gui=(ROOT/'interface/ICW_superpower_dossier.gui').read_text();behaviour=(ROOT/'common/scripted_guis/ICW_superpower_dossier.txt').read_text()
        for f in ('scope','reduction','reserve_limit','sanctions','trade','investment','duration','regional','programme','usa_target','sov_target','invites'):
            self.assertGreater(len(strings['icwt_help_'+f].split()),25)
        for n in range(1,13):self.assertIn('icwt_history_'+str(n),strings)
        self.assertIn('icwt_custom_draft',gui);self.assertIn('icwt_open_custom = yes',behaviour)
        self.assertEqual(strings['icwt_create'],'Historical proposal');self.assertEqual(strings['icwt_regional'],'Other')
        self.assertNotIn('icwt_value_restraint',gui)
        self.assertNotIn('Bomb production',strings['icwt_terms_summary'])


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MissileProtocols))
    report={'project':'IMPERIA COLD WAR','status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'scope':'Actual emitted treaty AST and loaded MD equipment definitions; no engine or live MP execution'}
    (HERE/'missile-protocol-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
