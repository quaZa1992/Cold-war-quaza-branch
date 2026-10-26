# IMPERIA CW — Cold War: iraq 1970 — test reward overhaul.
"""Execute v3 source transactions and compare faithful prospective rewards.

The strict AST harness records native construction/research/literacy boundaries.
It does not emulate combat, research consumption, UI rendering or multiplayer.
"""
from copy import deepcopy
import unittest

import compile as compiler
import reward_overhaul as overhaul
import audit_migration
from audit_design import load_design
from common import P, ROOT, GROUP_SLOTS, parse, first, values, walk
from test_audit_transactions import AuditWorld, fresh_outputs


class DirectRewardsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=fresh_outputs();cls.design=cls.out.design
        cls.old={n['key']:n for n in load_design(False)['nodes']}
        cls.nodes={n['key']:n for n in cls.design['nodes']}

    def world(self,key):
        w=AuditWorld(self.out);c=w.c['IRQ'];n=w.nodes[key]
        c.var['ruling_party']=GROUP_SLOTS.get(n['group'],[21])[0]
        if n['group']=='saddam':c.leader='Saddam Hussein'
        if n['group']=='aziz':c.leader='Aziz Muhammad'
        if n['group']=='puk':c.flags[P+'puk_formed']=None
        if n['group']=='sciri':c.flags[P+'sciri_formed']=None
        w.parents(key)
        for ancestor in min(compiler.routes(n['id']),key=lambda path:(len(path),sorted(path))):
            c.flags[compiler.selection(ancestor)]=None
        return w,c,n

    def migrate(self,w):
        w.call_irq('migrate_audit_revision');w.call_irq('migrate_direct_rewards_v3')

    def legacy_v2(self,w,key):
        c=w.c['IRQ'];n=self.old[key]
        c.flags[audit_migration.VERSION]=None;c.flags[audit_migration.QUOTE_VERSION]=None
        c.flags[n['id']+'_implemented']=None;c.flags[n['id']+'_package_earned']=None
        for component in n.get('audit_delivery_components',[]):c.flags[component['receipt']]=None
        return c

    def test_all_active_nodes_have_direct_effect_and_unchanged_graph(self):
        active=[n for n in self.design['nodes'] if not n.get('audit_retired')]
        self.assertEqual(len(active),410)
        for n in active:
            self.assertTrue(n.get('overhaul_changed'),n['key'])
            self.assertTrue(n['modifiers'] or n['overhaul_components'] or n['replaces'],n['key'])
            old=self.old[n['key']]
            for field in ('id','group','xy','anchor','offset','prerequisites','mutually_exclusive','requires','active_requires'):
                self.assertEqual(n.get(field),old.get(field),(n['key'],field))
        self.assertEqual(self.design['starting_spirits'],load_design(False)['starting_spirits'])
        self.assertEqual(self.design['iran_war_ideas'],load_design(False)['iran_war_ideas'])

    def test_every_asset_rejects_foreign_control_or_no_capacity_before_payment(self):
        count=0
        for n in self.nodes.values():
            for component in n.get('overhaul_components',[]):
                if component['kind']!='building':continue
                for failure in ('owner','controller','capacity'):
                    w,c,_=self.world(n['key']);self.migrate(w)
                    sid=str(component['state'])
                    if failure=='capacity':w.capacity[sid]=0
                    else:setattr(w.s[sid],failure,'PER')
                    cash=c.var['treasury'];w.call_irq('apply_'+n['key'])
                    self.assertAlmostEqual(c.var['treasury'],cash,(n['key'],failure))
                    self.assertFalse(w.assets,(n['key'],failure))
                count+=1
        self.assertGreaterEqual(count,36)

    def test_new_power_plant_is_direct_paid_once_and_survives_party_change(self):
        key=next(n['key'] for n in self.nodes.values() if n.get('building') and n['building'][1]=='fossil_powerplant')
        w,c,n=self.world(key);self.migrate(w);start=c.var['treasury']
        w.call_irq('apply_'+key);self.assertEqual(len(w.assets),1)
        self.assertAlmostEqual(c.var['treasury'],start-10*n['budget_gdp_share'])
        w.call_irq('apply_'+key);w.call_irq('reconcile_programmes')
        c.var['ruling_party']=4;w.call_irq('reconcile_programmes')
        self.assertEqual(len(w.assets),1)
        self.assertAlmostEqual(c.var['treasury'],start-10*n['budget_gdp_share'])

    def test_fresh_research_and_xp_not_replayed_by_resync(self):
        w,c,n=self.world('bakr_technical_mission');self.migrate(w)
        w.call_irq('apply_bakr_technical_mission')
        self.assertEqual([(x['category'],float(x['bonus'])) for x in w.research],[('CAT_construction',.3),('CAT_industry',.25)])
        for _ in range(3):w.call_irq('apply_bakr_technical_mission');w.call_irq('reconcile_programmes')
        self.assertEqual(len(w.research),2)
        w,c,n=self.world('defence_air_maintenance');self.migrate(w)
        for _ in range(3):w.call_irq('apply_defence_air_maintenance')
        self.assertEqual(c.var['air_xp'],15);self.assertEqual(len(w.research),1)

    def test_existing_v2_research_uses_credited_even_if_bonus_changes(self):
        w,c,n=self.world('industry_machine_tools');self.legacy_v2(w,n['key'])
        self.migrate(w);w.call_irq('refresh_direct_reward_quotes_v3')
        self.assertTrue(w.flag(c,overhaul.current(n)))
        self.assertFalse(w.flag(c,overhaul.pending(n)))
        w.call_irq('upgrade_reward_v3_'+n['key']);w.call_irq('reconcile_programmes')
        self.assertFalse(w.research);self.assertFalse(w.assets)
        self.assertAlmostEqual(c.var['treasury'],10)

    def test_old_policy_kept_until_funded_expansion_and_frozen_surcharge(self):
        w,c,n=self.world('oil_baiji');self.legacy_v2(w,n['key']);self.migrate(w)
        w.call_irq('refresh_direct_reward_quotes_v3');price=10*n['overhaul_price_increment']
        self.assertAlmostEqual(c.var[overhaul.uid(n)+'_invoice'],price)
        c.var['treasury']=price-.001;w.call_irq('upgrade_reward_v3_oil_baiji')
        self.assertFalse(w.assets);self.assertTrue(w.flag(c,overhaul.pending(n)))
        w.call_irq('reconcile_programmes')
        for key,value in n['overhaul_previous_modifiers'].items():
            self.assertAlmostEqual(c.var[P+n['group']+'_'+key],value)
        c.var.update(treasury=price,gdp_total=1000)
        for _ in range(3):w.call_irq('upgrade_reward_v3_oil_baiji')
        self.assertEqual(w.assets,[('167','fuel_silo',1)]);self.assertAlmostEqual(c.var['treasury'],0)
        self.assertTrue(w.flag(c,overhaul.current(n)))

    def test_ordinary_pending_quote_preserves_original_gdp_and_no_receipt_fabrication(self):
        w,c,n=self.world('oil_baiji');c.flags[audit_migration.VERSION]=None;c.flags[audit_migration.QUOTE_VERSION]=None
        c.flags[n['id']+'_quoted']=None;c.flags[n['id']+'_pending']=None
        c.var[n['id']+'_invoice']=10*self.old[n['key']]['budget_gdp_share'];c.var['gdp_total']=100
        self.migrate(w);self.migrate(w)
        self.assertAlmostEqual(c.var[n['id']+'_invoice'],10*n['budget_gdp_share'])
        self.assertFalse(w.flag(c,overhaul.old_holder(n)));self.assertFalse(w.assets)
        w.call_irq('apply_'+n['key']);self.assertEqual(w.assets,[('167','fuel_silo',1)])

    def test_delivered_merged_child_credited_before_parent_ordinary_delivery(self):
        w,c,n=self.world('industry_heavy');w.legacy('industry_steel')
        self.migrate(w)
        building=next(x for x in n['overhaul_components'] if x['kind']=='building')
        self.assertTrue(w.flag(c,building['receipt']))
        self.assertFalse(w.flag(c,overhaul.pending(n)))
        w.call_irq('apply_industry_heavy');self.assertFalse(w.assets)
        self.assertEqual(len(w.research),1)

    def test_old_v2_unfinished_upgrade_blocks_v3_expansion(self):
        w,c,n=self.world('industry_heavy');w.legacy('industry_heavy')
        self.migrate(w);self.assertTrue(w.flag(c,n['id']+'_audit_upgrade_pending'))
        w.call_irq('upgrade_reward_v3_industry_heavy');self.assertFalse(w.assets)
        w.call_irq('upgrade_industry_heavy');self.assertEqual(len(w.assets),1)
        w.call_irq('refresh_direct_reward_quotes_v3');w.call_irq('upgrade_reward_v3_industry_heavy')
        self.assertEqual(len(w.assets),1);self.assertEqual(len(w.research),1)
        self.assertTrue(w.flag(c,overhaul.current(n)))

    def test_current_party_programme_removed_and_restored_without_assets(self):
        w,c,n=self.world('bakr_technical_mission');self.migrate(w)
        w.call_irq('apply_bakr_technical_mission')
        var=P+'bakr_education_cost_multiplier_modifier'
        self.assertAlmostEqual(c.var[var],-.03)
        c.leader='Saddam Hussein';w.call_irq('reconcile_programmes');self.assertEqual(c.var[var],0)
        c.leader='Ahmed Hassan al-Bakr';w.call_irq('reconcile_programmes');self.assertAlmostEqual(c.var[var],-.03)
        self.assertEqual(len(w.research),2)

    def test_courts_apply_real_corruption_law_step_only_once(self):
        w,c,n=self.world('civic_commercial_courts');c.ideas['corruption_level_07']=None
        self.migrate(w)
        w.call_irq('apply_civic_commercial_courts')
        self.assertNotIn('corruption_level_07',c.ideas);self.assertIn('corruption_level_06',c.ideas)
        c.var['ruling_party']=21;w.call_irq('reconcile_programmes')
        c.var['ruling_party']=2;w.call_irq('reconcile_programmes');w.call_irq('apply_civic_commercial_courts')
        self.assertIn('corruption_level_06',c.ideas);self.assertNotIn('corruption_level_05',c.ideas)

    def test_front_preview_numbers_present_while_contract_false(self):
        for key in ('national_front','baath_monopoly'):
            n=self.nodes[key];preview=compiler.presentation.reward_preview(n,n['group'],compiler.PROGRAMME_CONTRACT_GATES[n['id']])
            operands=[r for body in values(parse(preview),'effect_tooltip') for r in body]
            self.assertEqual(len([k for k,o,v in operands if k=='add_to_variable']),len(n['modifiers']))
            self.assertFalse(any(k=='if' for k,o,v in operands))

    def test_nationalisation_preserves_90_day_cost_without_replaying_old_transition(self):
        n=self.nodes['oil_nationalize'];payload=overhaul.delivery(n,preview=True)
        self.assertIn('days = 90',payload);self.assertIn('COLDWAR_IRQ_ipc_marketing_transition',payload)
        w,c,n=self.world('oil_nationalize');self.legacy_v2(w,n['key']);self.migrate(w)
        self.assertFalse(w.flag(c,overhaul.pending(n)))
        self.assertTrue(all(w.flag(c,x['receipt']) for x in n['overhaul_components']))


if __name__=='__main__':unittest.main(verbosity=2)
