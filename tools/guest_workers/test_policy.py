# IMPERIA CW — Cold War: Execute real policy/return ASTs, including native UI and consent callbacks.
from copy import deepcopy
import unittest
import validate as V
import validate_diaspora as T
from test_ministry import Machine, CLICKS, GUARDS, fixture as recruitment_fixture
D=V.D
DATA=T.load()

def fixture(stock=100):
    m=Machine(*DATA);s=m.root;h=m.origin
    s.ideas={'mdcw_ni_overseas_employment_programme'}
    h.ideas={'mdcw_ni_guest_worker_recruitment_programme'}
    s.variables.update(gw_ui_host=D(2),gw_abroad_k=D(stock),mdcw_gw_net_emigration_k=D(stock),mdcw_gw_remittance_pool_m=D(400))
    h.variables.update(mdcw_gw_guest_workers_k=D(stock),mdcw_gw_net_emigration_k=-D(stock),gdp_per_capita=D(5))
    s.variables['gdp_per_capita']=D(2)
    m.execute([('add_to_array','=',[('gw_hosts','=','2')])])
    def seed():
        m.call('mdcw_gw_ledger_initialize')
        h.temporary['gw_lookup_origin']=D(1);m.call('mdcw_gw_ensure_origin')
        h.variables.update({'gw_stock^0':D(stock),'gw_unrecorded_k':D(0)})
        m.call('mdcw_gw_recount_ledger')
    m.event_context((m.now,'',h,s,{}),seed)
    m.call('mdcw_dp_prepare_selected')
    return m

def host_call(m,name):
    return m.event_context((m.now,'',m.countries['B'],m.countries['A'],{}),lambda:m.call(name))

def resources(m):return T.resources(m)

class Policies(unittest.TestCase):
    def offer(self,m,kind):
        m.call('mdcw_dp_request_'+kind);m.advance_days(1)
        return next(e for e in m.open_events if e[1]=='mdcw_dp.'+('1' if kind=='trade' else '2'))

    # IMPERIA CW — Cold War: War pressure is exclusive, quarterly and population-conserving.
    def test_war_pressure_distinguishes_all_four_country_states(self):
        for home_war,host_war,expected in ((False,False,8),(False,True,32),(True,False,2),(True,True,8)):
            m=fixture();m.origin.variables['gdp_per_capita']=D('2.2')
            m.root.peace=not home_war;m.origin.peace=not host_war
            m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1))
            host_call(m,'mdcw_dp_return_rate')
            self.assertEqual(m.origin.temporary['gw_rate'],expected,(home_war,host_war))

    def test_host_only_war_can_exceed_fifteen_and_reach_sixty_percent(self):
        m=fixture();m.origin.variables['gdp_per_capita']=D(1)
        m.root.stability=D('.9');m.origin.stability=D('.8');m.origin.peace=False
        m.root.flags['gw_dp_homecoming']=D(0);m.root.variables['gw_dp_homecoming_covered']=D(100)
        m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1))
        host_call(m,'mdcw_dp_return_rate');self.assertEqual(m.origin.temporary['gw_rate'],60)
        m.root.peace=False
        host_call(m,'mdcw_dp_return_rate');self.assertEqual(m.origin.temporary['gw_rate'],15)
        m.origin.peace=True
        host_call(m,'mdcw_dp_return_rate');self.assertEqual(m.origin.temporary['gw_rate'],4)

    def test_wartime_annual_returns_move_real_population_and_income_proportionally(self):
        m=fixture();m.origin.variables['gdp_per_capita']=D('2.2');m.origin.peace=False
        before=sum(st.population for c in m.countries.values() for st in c.states)
        m.advance_days(365)
        self.assertEqual(m.origin.variables['gw_return_last^0'],32)
        self.assertEqual(m.origin.states[0].population,968000)
        self.assertEqual(m.root.states[0].population,1032000)
        self.assertEqual(m.root.variables['mdcw_gw_remittance_pool_m'],272)
        self.assertEqual(sum(st.population for c in m.countries.values() for st in c.states),before)
        self.assertEqual(m.country_scans,0)

    def test_war_changes_are_sampled_without_retroactive_full_year_multiplier(self):
        m=fixture();m.origin.variables['gdp_per_capita']=D('2.2')
        m.advance_days(273);m.origin.peace=False;m.advance_days(92)
        self.assertEqual(m.origin.variables['gw_return_last^0'],14) # (8+8+8+32)/4

    def test_ai_cannot_import_any_tier_but_human_can_recruit_from_ai(self):
        for size in (25000,50000,100000):
            m=recruitment_fixture();m.origin.states.append(V.State(owner='B',controller='B'))
            m.root.is_ai=True;before=resources(m);queued=len(m.queue)
            self.assertFalse(m.test([(f'mdcw_gw_request_available_{size}','=','yes')]))
            self.assertFalse(m.test([(f'mdcw_gw_ui_can_recruit_{size}','=','yes')]))
            m.execute(CLICKS[f'gw_recruit_{size}_click'])
            self.assertEqual(resources(m),before);self.assertEqual(len(m.queue),queued)
            m.root.is_ai=False;m.origin.is_ai=True
            m.execute(CLICKS[f'gw_recruit_{size}_click']);m.advance_days(1)
            e=next(e for e in m.open_events if e[1].startswith('mdcw_guest_workers.') and int(e[1].split('.')[-1]) in (1,2,3))
            m.choose(e,'accept')
            self.assertEqual(m.root.states[0].population,1000000+size)
            self.assertEqual(m.origin.variables['treasury'],D(100)+{25000:10,50000:15,100000:25}[size])

    def test_ai_cannot_start_special_programmes_but_can_answer_human_trade_and_skill(self):
        for effect in ('mdcw_dp_request_trade','mdcw_dp_request_skill','mdcw_dp_open_remittance','mdcw_dp_open_retention','mdcw_dp_open_homecoming'):
            m=fixture();m.root.is_ai=True;before=resources(m);queued=len(m.queue)
            m.call(effect);self.assertEqual(resources(m),before,effect)
            self.assertEqual(len(m.queue),queued,effect)
        for kind in ('trade','skill'):
            m=fixture();m.origin.is_ai=True;e=self.offer(m,kind)
            self.assertTrue(m.event_context(e,lambda:m.test([('mdcw_dp_offer_pending','=','yes')])))
            m.choose(e,0);self.assertIn('gw_dp_active_1',m.root.flags)
        m=fixture();m.root.is_ai=True
        self.assertFalse(m.in_scope(m.origin,lambda:m.test([('mdcw_gw_outreach_target_valid','=','yes')])))
        m.origin.is_ai=True
        self.assertFalse(m.in_scope(m.origin,lambda:m.test([('mdcw_gw_management_unlocked','=','yes')])))

    def test_ai_sender_spirit_uses_population_or_unemployment_only_for_acquisition(self):
        ideas=V.first(V.read_script('common/ideas/mdcw_guest_workers_ideas.txt'),'ideas',[])
        group=V.first(ideas,'imp_national_ideas_2',[])
        sender=V.first(group,'mdcw_ni_overseas_employment_programme',[])
        receiver=V.first(group,'mdcw_ni_guest_worker_recruitment_programme',[])
        for pop,unemployment,expected in ((99,'0.0999',False),(100,0,True),(10,'0.10',True),(10,'0.0999',False)):
            m=fixture();m.root.is_ai=True
            m.root.variables.update(population_total=D(pop),total_unemployed_percentage_display=D(unemployment))
            self.assertEqual(m.test(V.first(sender,'available',[])),expected)
            self.assertFalse(m.test(V.first(receiver,'available',[])))
            m.root.is_ai=False
            self.assertTrue(m.test(V.first(sender,'available',[])))
            self.assertTrue(m.test(V.first(receiver,'available',[])))
        m=fixture();m.root.is_ai=True;m.root.variables['population_total']=D(1)
        self.assertTrue(m.test([('mdcw_gw_is_sending_country','=','yes')])) # Historical giver remains available.

    def test_pending_human_request_cannot_complete_after_applicant_becomes_ai(self):
        m=recruitment_fixture();before=resources(m)
        m.execute(CLICKS['gw_recruit_25000_click']);m.advance_days(1)
        e=next(e for e in m.open_events if e[1]=='mdcw_guest_workers.1')
        m.root.is_ai=True;m.choose(e,'accept')
        self.assertEqual(resources(m),before)
        m=fixture();before=resources(m);e=self.offer(m,'trade')
        m.root.is_ai=True;m.choose(e,0)
        self.assertEqual(resources(m),before)
        self.assertNotIn('gw_dp_active_1',m.root.flags)

    def test_stability_uses_five_point_steps_and_two_point_cap(self):
        for difference,expected in [('0.0499',8),('0.05',9),('0.10',10),('0.3',10),('-.0499',8),('-.05',7),('-.10',6),('-.3',6)]:
            m=fixture();m.origin.variables['gdp_per_capita']=D('2.2')
            m.origin.stability=D('.6');m.root.stability=D('.6')+D(difference)
            m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1))
            host_call(m,'mdcw_dp_return_rate')
            self.assertEqual(m.origin.temporary['gw_rate'],D(expected),difference)

    def test_gdp_steps_retention_coverage_recall_and_caps(self):
        for ratio,rate in [('3',1),('2',2),('1.5',4),('1.25',6),('1',8),('.9',10)]:
            m=fixture();m.origin.variables['gdp_per_capita']=D(ratio)*2
            m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1));host_call(m,'mdcw_dp_return_rate')
            self.assertEqual(m.origin.temporary['gw_rate'],rate)
        m=fixture();m.origin.variables['gdp_per_capita']=D('2.2');m.origin.stability=D('.6');m.root.stability=D('.7')
        m.origin.flags['gw_dp_retention']=D(0)
        for field in ('housed','protected','registered'):m.origin.variables[f'gw_{field}^0']=D(100)
        m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1));host_call(m,'mdcw_dp_return_rate')
        self.assertEqual(m.origin.temporary['gw_rate'],D(4))
        m.root.flags['gw_dp_homecoming']=D(0);m.root.variables['gw_dp_homecoming_covered']=D(100);host_call(m,'mdcw_dp_return_rate')
        self.assertEqual(m.origin.temporary['gw_rate'],D('5.6'))
        m.origin.variables['gdp_per_capita']=D(20);m.origin.stability=D(1);m.root.stability=D('.5');m.root.flags.clear()
        host_call(m,'mdcw_dp_return_rate');self.assertEqual(m.origin.temporary['gw_rate'],D('.5'))

    def test_four_samples_and_exact_365_day_population_return(self):
        m=fixture();s=m.root;h=m.origin;pop=sum(x.population for c in m.countries.values() for x in c.states)
        m.advance_days(364)
        self.assertEqual(h.states[0].population,1000000)
        self.assertEqual(h.variables['gw_migration_quarter'],3)
        m.advance_days(1)
        self.assertEqual(h.states[0].population,998000);self.assertEqual(s.states[0].population,1002000)
        self.assertEqual(h.variables['gw_stock^0'],98);self.assertEqual(s.variables['gw_abroad_k'],98)
        self.assertEqual(s.variables['mdcw_gw_remittance_pool_m'],392)
        self.assertEqual(h.variables['gw_return_last^0'],2)
        self.assertEqual(sum(x.population for c in m.countries.values() for x in c.states),pop)
        self.assertEqual(s.stability,D('.8'));self.assertEqual(h.stability,D('.8'))
        m.advance_days(365);self.assertEqual(h.variables['gw_stock^0'],D('96.04'))

    def test_arrivals_during_year_do_not_increase_eligible_return_stock(self):
        m=fixture();m.advance_days(300)
        m.origin.variables['gw_stock^0']+=D(100)
        m.advance_days(65)
        self.assertEqual(m.origin.variables['gw_return_last^0'],2)
        self.assertEqual(m.origin.variables['gw_return_basis^0'],198)

    def test_trade_acceptance_pays_host_and_applies_real_modifier_once(self):
        m=fixture();e=self.offer(m,'trade')
        self.assertEqual(m.root.political_power,950)
        self.assertIn('gw_dp_offer',m.origin.flags);self.assertIn('gw_dp_request',m.root.flags)
        before=resources(m);m.call('mdcw_dp_request_trade');self.assertEqual(resources(m),before)
        m.choose(e,0)
        self.assertEqual(m.root.variables['treasury'],99);self.assertEqual(m.origin.variables['treasury'],101)
        self.assertEqual(m.root.variables['gw_dp_trade_factor'],D('-.03'))
        self.assertIn('mdcw_dp_programmes',m.root.dynamic_modifiers)
        before=resources(m);m.choose(e,0);self.assertEqual(resources(m),before)
        self.assertEqual(m.root.variables['gw_dp_active_count'],1)
        self.assertIn('gw_dp_cooldown@A',m.origin.flags)

    def test_refusal_expiry_and_late_acceptance_never_charge_or_transfer(self):
        for reject in (True,False):
            m=fixture();before=resources(m);e=self.offer(m,'trade')
            if reject:m.choose(e,1)
            else:
                m.advance_days(16);self.assertEqual(resources(m),before)
                m.choose(e,0)
            self.assertEqual(resources(m),before)
            self.assertNotIn('gw_dp_request',m.root.flags)
            self.assertNotIn('gw_dp_offer',m.origin.flags)

    def test_invalidated_cash_or_community_refunds_request(self):
        for change in ('cash','stock'):
            m=fixture();e=self.offer(m,'trade')
            if change=='cash':m.root.variables['treasury']=D('.999')
            else:m.origin.variables['gw_stock^0']=D(10)
            before=resources(m);m.choose(e,0)
            self.assertEqual(m.root.political_power,1000)
            self.assertEqual(m.root.variables['treasury'],before[0][1])
            self.assertNotIn('gw_dp_active_1',m.root.flags)

    def test_skilled_return_counts_natural_returns_and_settles_once(self):
        m=fixture();s=m.root;h=m.origin;e=self.offer(m,'skill');m.choose(e,0)
        self.assertEqual(s.variables['treasury'],100);self.assertEqual(s.variables['gw_dp_cohort_1'],10)
        m.advance_days(364) # day365: ordinary annual migration
        self.assertEqual(s.variables['gw_dp_returned_1'],2)
        m.advance_days(1) # day366: programme completion
        self.assertEqual(h.variables['gw_stock^0'],90)
        self.assertEqual(s.states[0].population,1010000);self.assertEqual(h.states[0].population,990000)
        self.assertEqual(s.variables['treasury'],99);self.assertEqual(h.variables['treasury'],D('100.5'))
        self.assertEqual(s.variables['gw_dp_research_factor'],D('.02'))
        self.assertEqual(s.variables['gw_dp_receipt_credited'],2);self.assertEqual(s.variables['gw_dp_receipt_new'],8)
        self.assertEqual(s.variables['mdcw_gw_remittance_pool_m'],360)
        before=resources(m)
        m.event_context((m.now,'mdcw_dp.61',h,s,dict(m.targets)),lambda:m.execute(V.first(m.events['mdcw_dp.61'],'immediate',[])) if m.test(V.first(m.events['mdcw_dp.61'],'trigger',[])) else None)
        self.assertEqual(resources(m),before)
        m.advance_days(D(1)/24)
        self.assertTrue(any(e[1]=='mdcw_dp.12' and e[2] is s for e in m.open_events))
        receipt=next(e for e in m.open_events if e[1]=='mdcw_dp.12')
        before=resources(m);m.choose(receipt,0);self.assertEqual(resources(m),before)

    def test_remittance_campaign_shared_three_billion_cap_import_guard_and_expiry(self):
        m=fixture();m.call('mdcw_dp_open_remittance');m.advance_days(0)
        e=next(e for e in m.open_events if e[1]=='mdcw_dp.20');m.choose(e,0)
        self.assertEqual(m.root.variables['treasury'],D('99.5'))
        self.assertEqual(m.root.variables['gw_dp_bonus_m'],100)
        m.root.variables['mdcw_gw_remittance_pool_m']=D(2950)
        m.root.variables['additional_income_rate']=D(0);m.call('mdcw_gw_add_remittance_income')
        self.assertEqual(m.root.variables['additional_income_rate'],3)
        self.assertEqual(m.root.variables['gw_dp_bonus_m'],50)
        m.call('mdcw_gw_apply_immigration_25000');m.call('mdcw_dp_income_preview')
        self.assertEqual(m.root.variables['gw_dp_bonus_m'],75)
        m.advance_days(180)
        self.assertEqual(m.root.variables['gw_dp_remit_stock_k'],0)
        self.assertIn('gw_dp_cooldown@A',m.origin.flags)

    def test_private_dialog_expiry_and_frozen_host_prevent_redirected_funding(self):
        m=fixture();m.call('mdcw_dp_open_remittance');m.advance_days(0)
        m.root.variables['gw_ui_host']=D(1)
        e=next(e for e in m.open_events if e[1]=='mdcw_dp.20');m.choose(e,0)
        self.assertEqual(m.root.variables['gw_dp_host_1'],2)
        m=fixture();m.call('mdcw_dp_open_remittance');m.advance_days(14)
        before=resources(m);m.call('mdcw_dp_confirm_remittance');self.assertEqual(resources(m),before)

    def test_national_policies_costs_and_expiry(self):
        m=fixture();m.call('mdcw_dp_open_homecoming');m.advance_days(0)
        e=next(e for e in m.open_events if e[1]=='mdcw_dp.22');m.choose(e,0)
        self.assertEqual(m.root.variables['treasury'],D('99.5'))
        self.assertIn('gw_dp_homecoming',m.root.flags)
        host_call(m,'mdcw_dp_open_retention');m.advance_days(0)
        e=next(e for e in m.open_events if e[1]=='mdcw_dp.21');m.choose(e,0)
        self.assertIn('gw_dp_retention',m.origin.flags)
        self.assertEqual(m.origin.variables['gw_dp_retention_weekly'],D('.025'))
        m.advance_days(365)
        self.assertNotIn('gw_dp_homecoming',m.root.flags);self.assertNotIn('gw_dp_retention',m.origin.flags)

    def test_invalid_state_or_dead_origin_preserves_population_and_stock(self):
        for invalid in ('home','source','dead'):
            m=fixture()
            if invalid=='home':m.root.states[0].controller='B'
            if invalid=='source':m.origin.states[0].controller='A'
            if invalid=='dead':m.root.exists=False
            before=resources(m);m.advance_days(365)
            self.assertEqual(resources(m),before)

    def test_policy_pending_turns_recruitment_and_other_policy_buttons_grey(self):
        m=fixture();m.call('mdcw_dp_request_trade')
        for size in (25000,50000,100000):
            self.assertFalse(m.test(GUARDS[f'gw_recruit_{size}_click_enabled']))
        m.root.variables['gw_ui_tab']=D(3)
        for key in ('trade','skill','remittance','homecoming','retention'):
            self.assertTrue(m.test(GUARDS[f'gw_dp_{key}_unavailable_visible']))
        self.assertEqual(m.country_scans,0)

    def test_two_programme_places_and_trade_expiry(self):
        m=fixture();e=self.offer(m,'trade');m.choose(e,0)
        c=V.Country('C');c.states=[V.State(owner='C',controller='C')]
        c.variables.update({'gw_origins^num':D(1),'gw_origins^0':D(1),'gw_stock^0':D(100)})
        m.countries['C']=c;m.root.variables['gw_ui_host']=D(3)
        e=self.offer(m,'trade');m.choose(e,0)
        self.assertEqual(m.root.variables['gw_dp_active_count'],2)
        self.assertEqual(m.root.variables['gw_dp_trade_factor'],D('-.06'))
        m.call('mdcw_dp_prepare_selected');self.assertFalse(m.call('mdcw_dp_can_trade',trigger=True))
        m.advance_days(364) # first contract ends on day366, second on day367
        self.assertEqual(m.root.variables['gw_dp_trade_factor'],D('-.03'))
        m.advance_days(1)
        self.assertEqual(m.root.variables['gw_dp_trade_factor'],0)

    def test_partial_funded_skill_return_scales_payment_and_research(self):
        m=fixture();e=self.offer(m,'skill');m.choose(e,0)
        m.root.variables['treasury']=D('.8')
        m.advance_days(365)
        self.assertEqual(m.origin.variables['gw_stock^0'],92)
        self.assertEqual(m.root.variables['treasury'],0)
        self.assertEqual(m.origin.variables['treasury'],D('100.4'))
        self.assertEqual(m.root.variables['gw_dp_research_factor'],D('.016'))
        self.assertEqual(m.root.variables['gw_dp_receipt_funded'],8)

    def test_two_source_states_odd_headcounts_and_reserve_compensation(self):
        m=fixture(1);h=m.origin;s=m.root
        h.states=[V.State(population=D(7),owner='B',controller='B'),V.State(population=D(7),owner='B',controller='B')]
        def hook(machine,state,delta):
            if delta<0:h.military_manpower+=D(123)
        m.state_population_hook=hook;reserve=h.military_manpower
        h.variables.update(gw_move_origin=D(1),gw_move_index=D(0),gw_move_k=D('.011'),gw_move_mode=D(1))
        host_call(m,'mdcw_dp_move_population')
        self.assertEqual(sum(st.population for st in h.states),3)
        self.assertEqual(s.states[0].population,1000011)
        self.assertEqual(h.variables['gw_stock^0'],D('.989'))
        self.assertEqual(h.military_manpower,reserve)

    def test_large_returns_use_safe_chunks_without_population_or_income_loss(self):
        m=fixture(20000);h=m.origin;s=m.root
        h.states[0].population=D(30000000)
        h.variables.update(gw_move_origin=D(1),gw_move_index=D(0),gw_move_k=D(2500),gw_move_mode=D(1))
        host_call(m,'mdcw_dp_move_population')
        self.assertEqual(h.variables['gw_move_chunks'],3)
        self.assertEqual(h.variables['gw_move_actual_k'],2500)
        self.assertEqual(h.states[0].population,27500000)
        self.assertEqual(s.states[0].population,3500000)
        self.assertEqual(h.variables['gw_stock^0'],17500)
        self.assertEqual(s.variables['mdcw_gw_remittance_pool_m'],350)

    def test_annexation_cancels_old_host_contract_and_resets_migration_arrays(self):
        m=fixture();e=self.offer(m,'trade');m.choose(e,0)
        c=V.Country('C');c.states=[V.State(owner='C',controller='C')];m.countries['C']=c
        m.event_context((m.now,'',c,m.origin,{}),lambda:m.call('mdcw_gw_absorb_annexed_ledger'))
        self.assertNotIn('gw_dp_active_1',m.root.flags)
        self.assertEqual(m.root.variables['gw_dp_trade_factor'],0)
        self.assertEqual(c.variables['gw_stock^0'],100)
        self.assertEqual(m.origin.variables.get('gw_return_basis^num',0),0)
        m.root.variables['gw_ui_host']=D(3)
        e=self.offer(m,'trade');m.choose(e,0)
        self.assertIn('gw_dp_active_1',m.root.flags)

    def test_income_refresh_has_no_foreign_or_population_iterators(self):
        effects=DATA[0]
        body=effects['mdcw_dp_income_preview']
        self.assertFalse(any(k in ('for_each_loop','every_country','random_owned_state','any_owned_state') for k,o,v in V.walk(body)))
        m=fixture();before=resources(m)
        for _ in range(50):m.call('mdcw_dp_income_preview')
        self.assertEqual(resources(m),before);self.assertEqual(m.country_scans,0)

    def test_recruitment_preview_accounts_for_campaign_displacement_at_cap(self):
        m=fixture();m.root.variables.update(mdcw_gw_remittance_pool_m=D(2950),gw_dp_remit_stock_k=D(100))
        m.root.temporary.update(mdcw_gw_offer_remittance_m=D(50),gw_dp_offer_people_k=D(25))
        before=resources(m);m.call('mdcw_dp_preview_export_income')
        self.assertEqual(m.root.temporary['mdcw_gw_offer_remittance_m'],0)
        self.assertEqual(resources(m),before)

    def test_skill_completion_before_annual_settlement_does_not_return_twice(self):
        m=fixture()
        m.queue=[(e[0]+D(2),*e[1:]) if e[1]=='mdcw_diaspora.60' else e for e in m.queue]
        e=self.offer(m,'skill');m.choose(e,0)
        m.advance_days(365)
        self.assertEqual(m.origin.variables['gw_stock^0'],90)
        self.assertEqual(m.root.variables['gw_dp_receipt_new'],10)
        m.advance_days(1)
        self.assertEqual(m.origin.variables['gw_stock^0'],90)
        self.assertEqual(m.root.states[0].population,1010000)

    def test_homecoming_coverage_cannot_grow_through_new_emigration(self):
        m=fixture();m.call('mdcw_dp_open_homecoming');m.advance_days(0)
        e=next(e for e in m.open_events if e[1]=='mdcw_dp.22');m.choose(e,0)
        m.root.variables['gw_abroad_k']=D(200)
        m.origin.temporary.update(gw_mi=D(0),gw_mo=D(1))
        host_call(m,'mdcw_dp_return_rate')
        self.assertEqual(m.origin.temporary['gw_rate'],4) # base2 + half-funded4pp

if __name__=='__main__':unittest.main(verbosity=2)
