# IMPERIA CW — Cold War: Guest Worker Administration
"""Execute the emitted Ministry UI, including its country-reference adapter.

Native DDS rendering and HOI4 multiplayer scheduling are explicit boundaries.
The every_country addition models only that documented iterator, not new rules.
"""
from copy import deepcopy
import json
from pathlib import Path
import unittest
import validate as V
import validate_diaspora as T


class Machine(V.ScriptMachine):
    country_scans=0
    def execute(self,body):
        if not any(k=='every_country' for k,_,v in body):return super().execute(body)
        assert not any(k in ('else','else_if') for k,_,v in body)
        for key,op,value in body:
            if key!='every_country':super().execute([(key,op,value)]);continue
            self.country_scans+=1
            for country in list(self.countries.values()):
                if self.in_scope(country,lambda:self.test(V.first(value,'limit',[]))):
                    self.in_scope(country,lambda:self.execute([n for n in value if n[0]!='limit']))


DATA=T.load()
SCRIPT=V.first(V.first(V.read_script('common/scripted_guis/mdcw_diaspora_gui.txt'),'scripted_gui',[]),'mdcw_gw_dashboard',[])
CLICKS=dict((k,v) for k,_,v in V.first(SCRIPT,'effects',[]))
GUARDS=dict((k,v) for k,_,v in V.first(SCRIPT,'triggers',[]))


def fixture():
    m=Machine(*DATA)
    m.root.variables['gw_ui_partner']=V.D(2)
    m.root.variables['mdcw_gw_net_emigration_k']=V.D(0)
    m.root.ideas.discard('mdcw_ni_overseas_employment_programme')
    m.origin.ideas.discard('mdcw_ni_guest_worker_recruitment_programme')
    return m


class Ministry(unittest.TestCase):
    def click(self,m,key):m.execute(CLICKS[key+'_click'])

    # IMPERIA CW — Cold War: Model the UI's dirty-key cache, not only runtime guards.
    def test_pending_request_refreshes_all_sizes_and_cannot_be_bypassed_by_partner(self):
        for size,pp in ((25000,75),(50000,125),(100000,200)):
            with self.subTest(size=size):
                m=fixture();m.root.variables['gw_ui_tab']=V.D(2)
                m.origin.states.append(V.State(owner='B',controller='B'))
                other=V.Country('C');other.ideas.add('mdcw_ni_overseas_employment_programme')
                other.states=[V.State(owner='C',controller='C'),V.State(owner='C',controller='C')]
                m.countries['C']=other
                cached_key=None;cached=None
                def visible_controls():
                    nonlocal cached_key,cached
                    if cached is None or cached_key!=m.get('gw_ui_dirty'):
                        cached_key=m.get('gw_ui_dirty')
                        cached={tier:(m.test(GUARDS[f'gw_recruit_{tier}_visible']),
                                      m.test(GUARDS[f'gw_recruit_{tier}_unavailable_visible']))
                                for tier in (25000,50000,100000)}
                    return cached
                self.assertTrue(all(v==(True,False) for v in visible_controls().values()))
                receiver_dirty=m.get('gw_ui_dirty');sender_dirty=m.origin.variables.get('gw_ui_dirty',0)
                self.click(m,'gw_recruit_'+str(size))
                self.assertGreater(m.get('gw_ui_dirty'),receiver_dirty)
                self.assertGreater(m.origin.variables['gw_ui_dirty'],sender_dirty)
                self.assertTrue(all(v==(False,True) for v in visible_controls().values()))
                before=T.resources(m);queued=len(m.queue)
                for partner in (2,3):
                    m.root.variables['gw_ui_partner']=V.D(partner)
                    for tier in (25000,50000,100000):
                        self.assertFalse(m.test(GUARDS[f'gw_recruit_{tier}_click_enabled']))
                        self.assertFalse(m.test(GUARDS[f'gw_recruit_{tier}_unavailable_click_enabled']))
                        self.assertNotIn(f'gw_recruit_{tier}_unavailable_click',CLICKS)
                        for _ in range(10):self.click(m,'gw_recruit_'+str(tier))
                self.assertEqual(T.resources(m),before);self.assertEqual(len(m.queue),queued)
                self.assertEqual(m.root.political_power,1000-pp)
                m.root.variables['gw_ui_partner']=V.D(2);m.advance_days(1)
                offer=next(e for e in m.open_events if e[1] in ('mdcw_guest_workers.1','mdcw_guest_workers.2','mdcw_guest_workers.3'))
                pending_dirty=m.get('gw_ui_dirty');sender_dirty=m.origin.variables['gw_ui_dirty']
                m.choose(offer,1)
                self.assertGreater(m.get('gw_ui_dirty'),pending_dirty)
                self.assertGreater(m.origin.variables['gw_ui_dirty'],sender_dirty)
                self.assertTrue(all(v==(True,False) for v in visible_controls().values()))
                self.assertEqual(m.root.political_power,1000)
                self.assertNotIn('mdcw_gw_receiving_cooldown',m.root.flags)
                self.assertEqual(m.country_scans,0)

    def test_unanswered_request_refreshes_controls_and_refunds_only_once(self):
        m=fixture();self.click(m,'gw_recruit_25000');pending_dirty=m.get('gw_ui_dirty')
        m.advance_days(17)
        self.assertGreater(m.get('gw_ui_dirty'),pending_dirty)
        self.assertNotIn('mdcw_gw_request_pending',m.root.flags)
        self.assertEqual(m.root.political_power,1000)
        # The still-open old offer remains quarantined on its sender; another
        # valid country can nevertheless be approached by the former recipient.
        other=V.Country('C');other.ideas.add('mdcw_ni_overseas_employment_programme')
        other.states=[V.State(owner='C',controller='C')]
        m.countries['C']=other;m.root.variables['gw_ui_partner']=V.D(3)
        self.assertTrue(m.test(GUARDS['gw_recruit_25000_click_enabled']))
        m.call('mdcw_gw_refund_request');self.assertEqual(m.root.political_power,1000)

    def test_late_reply_refreshes_sender_window_lock_without_replaying_transfer(self):
        m=fixture();self.click(m,'gw_recruit_25000');m.advance_days(17)
        offer=next(e for e in m.open_events if e[1]=='mdcw_guest_workers.1')
        self.assertIn('mdcw_gw_offer_window_open',m.origin.flags)
        before=T.resources(m);dirty=m.origin.variables['gw_ui_dirty']
        m.choose(offer,0)
        self.assertNotIn('mdcw_gw_offer_window_open',m.origin.flags)
        self.assertGreater(m.origin.variables['gw_ui_dirty'],dirty)
        self.assertEqual(T.resources(m),before)

    def test_tabs_and_selection_do_not_spend_resources(self):
        m=fixture();before=T.resources(m)
        for tab in ('overview','communities','recruitment'):
            self.click(m,'gw_tab_'+tab)
        self.assertEqual(T.resources(m),before)
        self.assertEqual(m.country_scans,1)
        self.assertEqual(m.array_values('gw_ui_candidates'),[V.D(2)])
        self.assertEqual(m.get('gw_ui_tab'),2)

    def test_candidate_paging_is_uncapped_and_does_not_scan_on_page(self):
        m=fixture()
        for i in range(3,15):
            c=V.Country(str(i));c.ideas.add('mdcw_ni_overseas_employment_programme');m.countries[c.tag]=c
        self.click(m,'gw_tab_recruitment');seen=[]
        for page in range(4):
            seen += [int(m.get('gw_ui_partner_'+str(row))) for row in range(1,5) if m.get('gw_ui_partner_'+str(row))>-1]
            if page<3:self.click(m,'gw_partner_next')
        self.assertEqual(len(seen),13);self.assertEqual(len(set(seen)),13)
        self.assertEqual(m.country_scans,1)
        for _ in range(20):m.call('mdcw_gw_ministry_counters')
        self.assertEqual(m.country_scans,1)

    def test_refreshed_partner_list_clears_a_removed_partner(self):
        m=fixture();self.click(m,'gw_tab_recruitment')
        self.assertEqual(m.get('gw_ui_partner'),2)
        m.origin.ideas.clear();self.click(m,'gw_partner_refresh')
        self.assertEqual(m.get('gw_ui_partner'),-1)
        self.assertFalse(m.call('mdcw_gw_ui_can_recruit_25000',trigger=True))

    # IMPERIA CW — Cold War: MP caching never replaces live transaction guards.
    def test_partner_register_reuse_expiry_and_refresh_spam_guard(self):
        m=fixture();before=T.resources(m)
        for _ in range(20):self.click(m,'gw_tab_recruitment')
        self.assertEqual(m.country_scans,1)
        self.click(m,'gw_partner_refresh');self.assertEqual(m.country_scans,2)
        for _ in range(20):self.click(m,'gw_partner_refresh')
        self.assertEqual(m.country_scans,2)
        self.assertFalse(m.test(GUARDS['gw_partner_refresh_click_enabled']))
        m.elapse(V.D(1));self.assertTrue(m.test(GUARDS['gw_partner_refresh_click_enabled']))
        self.click(m,'gw_partner_refresh');self.assertEqual(m.country_scans,3)
        m.elapse(V.D(7));self.click(m,'gw_tab_recruitment');self.assertEqual(m.country_scans,4)
        self.assertEqual(T.resources(m),before)

    def test_cached_partner_with_lost_population_still_cannot_send_workers(self):
        m=fixture();self.click(m,'gw_tab_recruitment')
        m.origin.states[0].population=V.D(1000)
        before=T.resources(m);self.click(m,'gw_recruit_25000')
        self.assertEqual(T.resources(m),before);self.assertFalse(m.queue)

    def test_origin_lookup_cache_revalidates_rebuilt_and_extended_ledgers(self):
        m=fixture()
        for origin in (2,3):m.execute([('add_to_array','=',[('gw_origins','=',str(origin))])])
        m.root.temporary['gw_lookup_origin']=V.D(2);m.call('mdcw_gw_find_origin')
        self.assertEqual(m.get('gw_index'),0)
        # Same length and an in-bounds cached index, but a different country at it.
        m.execute([('clear_array','=','gw_origins')])
        for origin in (3,2):m.execute([('add_to_array','=',[('gw_origins','=',str(origin))])])
        m.call('mdcw_gw_find_origin');self.assertEqual(m.get('gw_index'),1)
        m.root.temporary['gw_lookup_origin']=V.D(99);m.call('mdcw_gw_find_origin')
        self.assertEqual(m.get('gw_index'),-1)
        m.execute([('add_to_array','=',[('gw_origins','=','99')])])
        m.call('mdcw_gw_find_origin');self.assertEqual(m.get('gw_index'),2)
        m.execute([('clear_array','=','gw_origins')]);m.call('mdcw_gw_find_origin')
        self.assertEqual(m.get('gw_index'),-1)

    def test_inactive_budget_does_not_prepare_hidden_gui_but_active_data_stays_current(self):
        m=fixture();m.root.ideas.clear();m.root.variables['gw_ui_dirty']=V.D(10)
        m.call('mdcw_gw_update_cost_receipt')
        self.assertEqual(m.get('gw_ui_dirty'),10)
        self.assertNotIn('gw_ui_population',m.root.variables)
        m.root.variables['mdcw_gw_guest_workers_k']=V.D(100)
        m.call('mdcw_gw_update_cost_receipt')
        self.assertEqual(m.get('gw_ui_dirty'),11);self.assertEqual(m.get('gw_ui_population'),100000)
        m.root.variables.update(mdcw_gw_guest_workers_k=V.D(0),mdcw_gw_remittance_pool_m=V.D(100))
        m.call('mdcw_gw_update_cost_receipt')
        self.assertEqual(m.get('gw_ui_dirty'),12)

    def test_all_sizes_pay_native_fee_and_reach_selected_sender(self):
        for size,pp,tier in ((25000,75,1),(50000,125,2),(100000,200,3)):
            with self.subTest(size=size):
                m=fixture()
                m.origin.states.append(V.State(owner='B',controller='B'))
                # An unrelated FROM must never redirect the GUI transaction.
                wrong=V.Country('C');m.countries['C']=wrong;m.origin=wrong
                treasury=m.get('treasury');pop=sum(s.population for c in m.countries.values() for s in c.states)
                self.click(m,'gw_recruit_'+str(size))
                self.assertEqual(m.root.political_power,1000-pp)
                self.assertIn('mdcw_gw_request_pending',m.root.flags)
                self.assertIn('mdcw_gw_offer_pending',m.countries['B'].flags)
                self.assertNotIn('mdcw_gw_offer_pending',wrong.flags)
                self.assertEqual(m.get('treasury'),treasury)
                self.assertEqual(sum(s.population for c in m.countries.values() for s in c.states),pop)
                self.click(m,'gw_recruit_'+str(size));self.assertEqual(m.root.political_power,1000-pp)
                m.advance_days(1)
                offer=next(e for e in m.open_events if e[1]=='mdcw_guest_workers.'+str(tier))
                self.assertIs(offer[2],m.countries['B']);self.assertIs(offer[3],m.root)
                m.choose(offer,1)  # native refusal returns the full paid request fee
                self.assertEqual(m.root.political_power,1000)

    def test_acceptance_transfers_population_and_arrival_starts_receiver_cooldown(self):
        for size,price,tier in ((25000,10,1),(50000,15,2),(100000,25,3)):
            with self.subTest(size=size):
                m=fixture();receiver=m.root;sender=m.origin
                sender.states.append(V.State(owner='B',controller='B'))
                before_receiver=receiver.states[0].population;source_before=[s.population for s in sender.states]
                self.click(m,'gw_recruit_'+str(size));m.advance_days(1)
                event=next(e for e in m.open_events if e[1]=='mdcw_guest_workers.'+str(tier));m.choose(event,0)
                self.assertEqual(receiver.states[0].population,before_receiver+size)
                self.assertEqual(sum(s.population for s in sender.states),sum(source_before)-size)
                if size==100000:self.assertEqual([a-s.population for a,s in zip(source_before,sender.states)],[50000,50000])
                self.assertEqual(receiver.variables['treasury'],100-price);self.assertEqual(sender.variables['treasury'],100+price)
                self.assertIn('mdcw_gw_receiving_cooldown',receiver.flags)
                self.assertNotIn('mdcw_gw_receiving_cooldown',sender.flags)
                m.advance_days(V.D(1)/24)
                self.assertTrue(any(e[1]=='mdcw_guest_workers.30' and e[2] is receiver for e in m.open_events))
                for agreement_size in (25000,50000,100000):
                    self.assertFalse(m.test(GUARDS[f'gw_recruit_{agreement_size}_click_enabled']))
                m.advance_days(59)
                self.assertFalse(m.test(GUARDS['gw_recruit_25000_click_enabled']))
                m.advance_days(1)
                self.assertTrue(m.test(GUARDS['gw_recruit_25000_click_enabled']))

    def test_invalidated_requests_cannot_create_pp_or_free_requests(self):
        changes=[lambda m:m.root.flags.update(mdcw_gw_receiving_cooldown=V.D(60)),
                 lambda m:m.root.variables.update(treasury=V.D(9)),
                 lambda m:setattr(m.root,'political_power',V.D('74.999')),
                 lambda m:m.root.variables.update(gw_ui_partner=V.D(-1)),
                 lambda m:m.origin.variables.update(gdp_per_capita=V.D(20)),
                 lambda m:m.origin.ideas.clear(),lambda m:m.root.flags.update(gw_dialog_window=V.D(0)),
                 lambda m:m.origin.flags.update(mdcw_gw_offer_pending=V.D(0))]
        for change in changes:
            m=fixture();change(m);before=T.resources(m)
            self.click(m,'gw_recruit_25000')
            self.assertEqual(T.resources(m),before);self.assertEqual(m.queue,[])

    def test_coverage_and_counter_frames_are_bounded_without_large_fixed_point_overflow(self):
        m=T.fixture(DATA,500)
        m.root.variables.update({'gw_registered^0':V.D(300),'gw_housed^0':V.D(200),'gw_protected^0':V.D(500)})
        m.call('mdcw_gw_select_origin')
        self.assertEqual(m.get('gw_ui_registered_frame'),7);self.assertEqual(m.get('gw_ui_housed_frame'),5)
        self.assertEqual(m.get('gw_ui_protected_frame'),11)
        self.assertEqual(m.get('gw_ui_selected_people'),500000)
        m.root.variables['mdcw_gw_guest_workers_k']=V.D(50000);m.call('mdcw_gw_ministry_counters')
        self.assertEqual(m.get('gw_ui_population_m'),50)
        self.assertEqual(m.get('gw_ui_population'),2000000) # safe hidden fallback; visible unit is millions

    def test_fully_covered_programme_is_disabled(self):
        m=T.fixture(DATA,100);m.root.variables['gw_registered^0']=V.D(100);m.call('mdcw_gw_select_origin')
        self.assertFalse(m.test(GUARDS['gw_register_click_enabled']))
        before=T.resources(m);self.click(m,'gw_register');self.assertEqual(T.resources(m),before)

    def test_overseas_view_reads_the_correct_hosts_without_spending(self):
        m=fixture();m.root.variables.update(gw_abroad_k=V.D(100),gw_ui_host=V.D(2))
        m.execute([('add_to_array','=',[('gw_hosts','=','2')])])
        host=m.origin;host.variables.update({'gw_origins^num':V.D(1),'gw_origins^0':V.D(1),'gw_stock^0':V.D(100),
                                          'gw_registered^0':V.D(20),'gw_housed^0':V.D(50),'gw_protected^0':V.D(80),
                                          'population_total':V.D(100)})
        before=T.resources(m);self.click(m,'gw_abroad_mode')
        self.assertEqual(T.resources(m),before)
        self.assertEqual(m.get('gw_host1_k'),100);self.assertEqual(m.get('gw_ui_host_stock_k'),100)
        self.assertEqual(m.get('gw_ui_protected_ratio'),V.D('.8'))
        self.assertEqual(m.country_scans,0)

    def test_consular_dialog_freezes_host_and_charges_once(self):
        m=fixture();m.root.variables.update(gw_ui_host=V.D(2))
        host=m.origin;host.variables.update({'gw_origins^num':V.D(1),'gw_origins^0':V.D(1),'gw_stock^0':V.D(100),'population_total':V.D(100)})
        self.click(m,'gw_outreach');m.root.variables['gw_ui_host']=V.D(1);m.advance_days(0)
        e=next(e for e in m.open_events if e[1]=='mdcw_diaspora.86');m.choose(e,0)
        self.assertEqual(m.root.political_power,925);self.assertEqual(m.get('treasury'),V.D('99.5'))
        self.assertEqual(host.variables['gw_outreach^0'],1)
        m.call('mdcw_gw_ministry_confirm_outreach');self.assertEqual(m.root.political_power,925)
        m.advance_days(180);self.assertEqual(host.variables['gw_outreach^0'],0)

    def test_expired_consular_dialog_does_not_charge(self):
        m=fixture();m.root.variables.update(gw_ui_host=V.D(2))
        m.origin.variables.update({'gw_origins^num':V.D(1),'gw_origins^0':V.D(1),'gw_stock^0':V.D(100),'population_total':V.D(100)})
        self.click(m,'gw_outreach');m.advance_days(14);before=T.resources(m)
        m.call('mdcw_gw_ministry_confirm_outreach');self.assertEqual(T.resources(m),before)

    def test_consular_exact_funding_and_invalidated_community(self):
        for invalid in (False,True):
            m=fixture();m.root.variables.update(gw_ui_host=V.D(2),treasury=V.D('.5'));m.root.political_power=V.D(75)
            m.origin.variables.update({'gw_origins^num':V.D(1),'gw_origins^0':V.D(1),'gw_stock^0':V.D(100),'population_total':V.D(100)})
            self.click(m,'gw_outreach');m.advance_days(0)
            if invalid:m.origin.variables['gw_stock^0']=V.D(0)
            before=T.resources(m);m.call('mdcw_gw_ministry_confirm_outreach')
            if invalid:self.assertEqual(T.resources(m),before)
            else:self.assertEqual(m.get('treasury'),0);self.assertEqual(m.root.political_power,0)

    def test_tier_tooltips_explain_the_actual_blocker(self):
        definitions={V.first(v,'name'):v for k,_,v in V.read_script('common/scripted_localisation/mdcw_diaspora_dashboard_localisation.txt')}
        def chosen(m,name):
            return next(V.first(t,'localization_key') for t in V.values(definitions[name],'text') if m.test(V.first(t,'trigger',[])))
        m=fixture();m.root.political_power=V.D(150)
        self.assertEqual(chosen(m,'mdcw_gw_ministry_readiness_100000'),'gw_tier_pp_100000')
        m.root.political_power=V.D(1000)
        self.assertEqual(chosen(m,'mdcw_gw_ministry_readiness_100000'),'gw_tier_population_100000')
        m.origin.variables['gdp_per_capita']=V.D(10)
        self.assertEqual(chosen(m,'mdcw_gw_ministry_readiness_25000'),'gw_ministry_reason_10')

    def test_close_requires_exact_full_fee_and_zero_residents(self):
        m=fixture();m.root.political_power=V.D('149.999')
        self.assertFalse(m.call('mdcw_gw_can_close_programme',trigger=True))
        m.root.political_power=V.D(150);self.assertTrue(m.call('mdcw_gw_can_close_programme',trigger=True))
        m.root.variables['mdcw_gw_guest_workers_k']=V.D('.001')
        self.assertFalse(m.call('mdcw_gw_can_close_programme',trigger=True))

    def test_tab_and_mode_visibility_separate_actions(self):
        m=fixture();m.root.variables.update(gw_ui_tab=V.D(1),gw_selected_stock_k=V.D(100),gw_ui_host_stock_k=V.D(100))
        self.assertTrue(m.test(GUARDS['gw_register_visible']))
        self.assertFalse(m.test(GUARDS['gw_outreach_visible']))
        m.root.flags['gw_ui_show_abroad']=V.D(0)
        self.assertFalse(m.test(GUARDS['gw_register_visible']))
        self.assertTrue(m.test(GUARDS['gw_outreach_visible']))
        m.root.variables['gw_ui_tab']=V.D(2)
        self.assertFalse(m.test(GUARDS['gw_outreach_visible']))
        self.assertTrue(m.test(GUARDS['gw_recruit_25000_visible']))

    def test_global_scan_is_confined_to_explicit_partner_list_action(self):
        effects=DATA[0]
        scans=[name for name,body in effects.items() if any(k in ('every_country','every_other_country') for k,_,v in V.walk(body))]
        self.assertEqual(scans,['mdcw_gw_ministry_list_partners'])
        for name in ('mdcw_gw_ministry_counters','mdcw_gw_calculate_diaspora_costs'):
            self.assertFalse(any(k in ('every_country','for_each_loop','any_country','any_owned_state') for k,_,v in V.walk(effects[name])))


if __name__=='__main__':unittest.main(verbosity=2)
