# IMPERIA CW — Cold War: emitted focus/decision contract regressions.
"""Exercise fresh scoped compiler output without installing game files.

The strict existing AST interpreter records native politics, research and
construction boundaries. These tests do not establish HOI4 loading, tooltip
rendering, elections, economy simulation or multiplayer synchronisation.
"""
from copy import deepcopy
from datetime import date
import re
import unittest
import zipfile

import apply_streamlining
import audit_migration
import compile as compiler
import decision_streamlining as streamline
import reward_overhaul
from common import ROOT, P, GROUP_SLOTS, parse, first, values, walk
from test_audit_transactions import AuditWorld, GeneratedOutputs


GENERAL_EFFECTS = 'common/scripted_effects/COLDWAR_IRQ_1970_decision_effects.txt'
GENERAL_EVENTS = 'events/COLDWAR_IRQ_1970_decisions.txt'
DECISIONS = 'common/decisions/COLDWAR_IRQ_1970_decisions.txt'
FOCUSES = 'common/national_focus/COLDWAR_IRQ_1970_focus.txt'


class StreamlinedWorld(AuditWorld):
    """Load emitted providers; never leave pruned legacy helpers as fallbacks."""
    def __init__(self, outputs):
        super().__init__(outputs)
        for name, _, _ in parse(self.out[GENERAL_EFFECTS]):
            self.effects.pop(name, None)
        for path, text in outputs.items():
            if path.startswith('common/scripted_effects/'):
                self.effects.update({k: v for k, _, v in parse(text)})
            elif path.startswith('events/'):
                if path == GENERAL_EVENTS:
                    self.events = {k: v for k, v in self.events.items()
                                   if not k.startswith('COLDWAR_IRQ_decision_events.')}
                self.events.update({first(v, 'id'): v
                                    for v in values(parse(text), 'country_event')})
        self.loc = {}
        for path, text in outputs.items():
            if path.endswith('.yml'):
                self.loc.update(re.findall(r'^\s*([^\s:]+):\d* "(.*)"$', text, re.M))
        self.native_politics = []

    def run(self, rows, c, root=None, prev=None, source=None):
        # These are explicit native API boundaries; all authored guards/effects
        # around them continue through the strict existing interpreter.
        filtered = []
        for k, o, v in rows:
            if k == 'add_command_power':
                c.var['command_power'] = c.var.get('command_power', 0) + self.num(v, c)
            elif k == 'set_politics':
                self.native_politics.append((c.key, deepcopy(v)))
            else:
                filtered.append((k, o, v))
        super().run(filtered, c, root, prev, source)


class DecisionStreamliningTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        outputs, design, cls.report = apply_streamlining.generate()
        cls.out = GeneratedOutputs(outputs)
        cls.out.design = design
        cls.design = design
        cls.nodes = {n['key']: n for n in design['nodes']}
        cls.decs = dict((k, v) for k, _, v in first(parse(outputs[DECISIONS]), P+'1970_decisions'))
        cls.events = {first(v, 'id'): v for v in values(parse(outputs[GENERAL_EVENTS]), 'country_event')}
        cls.effects = {}
        for path, text in outputs.items():
            if path.startswith('common/scripted_effects/'):
                cls.effects.update({k: v for k, _, v in parse(text)})
        cls.prototype = StreamlinedWorld(cls.out)

    def world(self, key=None, fresh=True):
        w = deepcopy(self.prototype)
        c = w.c['IRQ']
        if fresh:
            for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION,
                           reward_overhaul.VERSION, streamline.VERSION):
                c.flags[marker] = None
        if key:
            n = self.nodes[key]
            c.var['ruling_party'] = GROUP_SLOTS.get(n['group'], [21])[0]
            if n['group'] == 'saddam': c.leader = 'Saddam Hussein'
            if n['group'] == 'aziz': c.leader = 'Aziz Muhammad'
            if n['group'] == 'puk': c.flags[P+'puk_formed'] = None
            if n['group'] == 'sciri': c.flags[P+'sciri_formed'] = None
            w.parents(key)
            for ancestor in min(compiler.routes(n['id']), key=lambda p: (len(p), sorted(p))):
                c.flags[compiler.selection(ancestor)] = None
        return w, c

    def accept(self, w, eid, country, option=0):
        w.show(eid, country)
        body = values(w.events[eid], 'option')[option]
        # Deliberately bypass option visibility to prove execution guards.
        w.run([r for r in body if r[0] not in ('name', 'trigger', 'ai_chance')], w.c[country])

    def test_counts_and_geometry_match_backed_up_tree(self):
        self.assertEqual(len(self.decs), 25)
        self.assertEqual(len(self.design['nodes']), 426)
        with zipfile.ZipFile(apply_streamlining.REPORT/'before.zip') as z:
            old = z.read(FOCUSES).decode('utf-8-sig')
        def geometry(text):
            tree = first(parse(text), 'focus_tree')
            return {first(f, 'id'): [(k, o, v) for k, o, v in f if k in
                    ('x', 'y', 'relative_position_id', 'prerequisite', 'mutually_exclusive')]
                    for f in values(tree, 'focus')}
        self.assertEqual(len(geometry(old)), 426)
        self.assertEqual(geometry(self.out[FOCUSES]), geometry(old))

    def test_pruned_runtime_references_resolve(self):
        with zipfile.ZipFile(apply_streamlining.REPORT/'before.zip') as z:
            old_helpers = {k for k, _, _ in parse(z.read(GENERAL_EFFECTS).decode('utf-8-sig'))}
        for path, text in self.out.items():
            if not path.endswith(('.txt', '.gui')): continue
            for k, _, v in walk(parse(text)):
                if k == 'country_event' and isinstance(v, list):
                    eid = first(v, 'id', '')
                    if eid.startswith('COLDWAR_IRQ_decision_events.'):
                        self.assertIn(eid, self.events, (path, eid))
                if k in old_helpers and v == 'yes':
                    self.assertIn(k, self.effects, (path, k))
        self.assertNotIn('COLDWAR_IRQ_decision_events.223', self.events)
        self.assertNotIn(P+'do_constitutional_revision', self.effects)

    def test_gulf_preserved_and_us_only_loses_two_duplicate_menus(self):
        with zipfile.ZipFile(apply_streamlining.REPORT/'before.zip') as z:
            gulf = z.read('common/decisions/COLDWAR_IRQ_gulf_decisions.txt').decode('utf-8-sig')
            usa = z.read('common/decisions/COLDWAR_USA_gulf_decisions.txt').decode('utf-8-sig')
        def ids(text):
            return {k for _, _, body in parse(text) if isinstance(body, list)
                    for k, _, v in body if isinstance(v, list)}
        self.assertEqual(len(ids(gulf)), 12)
        if 'common/decisions/COLDWAR_IRQ_gulf_decisions.txt' in self.out:
            self.assertEqual(parse(self.out['common/decisions/COLDWAR_IRQ_gulf_decisions.txt']), parse(gulf))
        removed = ids(usa)-ids(self.out['common/decisions/COLDWAR_USA_gulf_decisions.txt'])
        self.assertEqual(removed, {'COLDWAR_USA_gulf_respond', 'COLDWAR_USA_gulf_uprising_aftermath'})

    def test_unaffordable_focus_cannot_commit_domestic_charter(self):
        w, c = self.world('national_front')
        c.var['treasury'] = 0
        w.call_irq('apply_national_front')
        self.assertFalse(w.flag(c, P+'front_accepted'))
        self.assertFalse(w.flag(c, P+'focus_owned_national_front_delivered'))
        self.assertNotIn(4, w.arrays['IRQ'].get('gov_coalition_array', set()))
        self.assertAlmostEqual(c.var['treasury'], 0)

    def test_exact_funds_charter_and_normal_hook_cannot_replay(self):
        w, c = self.world('national_front')
        price = 10*self.nodes['national_front']['budget_gdp_share']
        c.var['treasury'] = price
        w.call_irq('apply_national_front')
        self.assertAlmostEqual(c.var['treasury'], 0)
        self.assertTrue(w.flag(c, P+'front_accepted'))
        self.assertTrue(w.flag(c, P+'legalization_accepted'))
        self.assertIn(4, w.arrays['IRQ']['gov_coalition_array'])
        self.assertTrue(w.idea(c, P+'civil_rights_cost'))
        for _ in range(3):
            w.call_irq('apply_national_front')
            w.call_irq('focus_owned_national_front')
            w.call_irq('reconcile_programmes')
        self.assertAlmostEqual(c.var['treasury'], 0)
        self.assertEqual(w.arrays['IRQ']['gov_coalition_array'], {4})

    def test_normal_one_time_command_power_and_readiness(self):
        w, c = self.world('baath_monopoly')
        w.call_irq('apply_baath_monopoly')
        self.assertEqual(c.var['command_power'], 25)
        cash = c.var['treasury']
        for _ in range(3):
            w.call_irq('apply_baath_monopoly'); w.call_irq('reconcile_programmes')
        self.assertEqual(c.var['command_power'], 25)
        self.assertEqual(c.var['treasury'], cash)
        w, c = self.world('defence_readiness')
        w.call_irq('apply_defence_readiness')
        self.assertTrue(w.idea(c, P+'readiness_cycle'))
        expiry = c.ideas[P+'readiness_cycle']
        w.day = 30
        w.call_irq('focus_owned_defence_readiness'); w.call_irq('reconcile_programmes')
        self.assertEqual(c.ideas[P+'readiness_cycle'], expiry)
        w.day = 90
        self.assertFalse(w.idea(c, P+'readiness_cycle'))

    def test_amnesty_does_not_resurrect_recorded_dead(self):
        w, c = self.world('review_detentions')
        c.flags[P+'rikabi_dead'] = c.flags[P+'dukhayl_dead'] = None
        w.call_irq('apply_review_detentions')
        self.assertTrue(w.flag(c, P+'legalization_accepted'))
        for flag in ('rikabi_rehabilitated', 'dukhayl_released', 'dawa_cadres_protected'):
            self.assertFalse(w.flag(c, P+flag), flag)
        self.assertTrue(w.flag(c, P+'rikabi_dead'))
        self.assertTrue(w.flag(c, P+'dukhayl_dead'))

    def test_amnesty_case_deadlines_and_single_package(self):
        for when, expected in [(date(1970, 1, 1), {'rikabi_rehabilitated', 'dukhayl_released', 'dawa_cadres_protected'}),
                               (date(1972, 1, 1), {'dukhayl_released'}),
                               (date(1974, 1, 1), set())]:
            with self.subTest(date=when):
                w, c = self.world('review_detentions'); w.date = when
                w.call_irq('apply_review_detentions')
                for flag in ('rikabi_rehabilitated', 'dukhayl_released', 'dawa_cadres_protected'):
                    self.assertEqual(w.flag(c, P+flag), flag in expected)
                self.assertAlmostEqual(c.var['treasury'], 10-10*self.nodes['review_detentions']['budget_gdp_share'])

    def test_single_recipient_focus_freezes_quote_without_imposing_agreement(self):
        w, c = self.world('bakr_unity')
        w.call_irq('apply_bakr_unity')
        self.assertEqual(w.event_queue, [('SYR', 'COLDWAR_IRQ_decision_events.226')])
        invoice = P+'D_bakr_syria_offer_SYR_invoice'
        self.assertAlmostEqual(c.var[invoice], .1)
        self.assertFalse(w.flag(c, P+'syria_charter_accepted'))
        cash = c.var['treasury']; c.var['gdp_total'] = 100
        self.accept(w, 'COLDWAR_IRQ_decision_events.226', 'SYR')
        self.assertAlmostEqual(c.var['treasury'], cash-.1)
        self.assertTrue(w.flag(c, P+'syria_charter_accepted'))
        self.accept(w, 'COLDWAR_IRQ_decision_events.226', 'SYR')
        self.assertAlmostEqual(c.var['treasury'], cash-.1)

    def test_single_recipient_sender_rechecks_existence_and_existing_offer(self):
        w, c = self.world('bakr_unity'); w.c['SYR'].exists = False
        w.call_irq('apply_bakr_unity')
        self.assertFalse(w.event_queue)
        self.assertFalse(w.flag(c, P+'offer_bakr_syria_offer_SYR'))
        w.c['SYR'].exists = True
        w.call_irq('do_bakr_syria_offer')
        self.assertEqual(len(w.event_queue), 1)
        w.call_irq('do_bakr_syria_offer')
        self.assertEqual(len(w.event_queue), 1)

    def test_refused_or_expired_offer_can_retry_but_stale_acceptance_cannot_pay(self):
        for failure in ('expired', 'party', 'funds'):
            with self.subTest(failure=failure):
                w, c = self.world('bakr_unity'); w.call_irq('apply_bakr_unity')
                cash = c.var['treasury']
                if failure == 'expired': w.day = 61
                if failure == 'party': c.var['ruling_party'] = 22
                if failure == 'funds': c.var['treasury'] = 0; cash = 0
                self.accept(w, 'COLDWAR_IRQ_decision_events.226', 'SYR')
                self.assertAlmostEqual(c.var['treasury'], cash)
                self.assertFalse(w.flag(c, P+'syria_charter_accepted'))
        w, c = self.world('bakr_unity'); w.call_irq('apply_bakr_unity'); w.day = 61
        retry = self.decs[streamline.RETRY_ID]
        self.assertTrue(w.tests(first(retry, 'available'), c))
        menu = self.events[streamline.RETRY_EVENT]
        option = next(o for o in values(menu, 'option') if first(o, 'name') == P+'focus_owned_retry_bakr_syria_offer')
        self.assertTrue(w.tests(first(option, 'trigger'), c))
        w.event_queue.clear()
        w.run([r for r in option if r[0] not in ('name', 'trigger')], c)
        self.assertEqual(w.event_queue, [('SYR', 'COLDWAR_IRQ_decision_events.226')])
        w, c = self.world('bakr_unity'); w.call_irq('apply_bakr_unity')
        cash = c.var['treasury']
        self.accept(w, 'COLDWAR_IRQ_decision_events.226', 'SYR', option=1)
        self.assertAlmostEqual(c.var['treasury'], cash)
        self.assertFalse(w.flag(c, P+'syria_charter_accepted'))
        w.event_queue.clear(); w.call_irq('do_bakr_syria_offer')
        self.assertEqual(w.event_queue, [('SYR', 'COLDWAR_IRQ_decision_events.226')])

    def test_automatic_credit_selection_preserves_real_lender_consent_and_cash(self):
        w, c = self.world('civic_credit_terms')
        c.var.update(debt=1, COLDWAR_IRQ_gulf_debt_snapshot=1,
                     COLDWAR_IRQ_gulf_other_debt=0, COLDWAR_IRQ_gulf_principal_KUW=1)
        c.flags[P+'gulf_initialized'] = None
        w.call_irq('apply_civic_credit_terms')
        cash = c.var['treasury']
        self.assertEqual(w.event_queue, [('IRQ', 'COLDWAR_IRQ_decision_events.275')])
        shown = w.show('COLDWAR_IRQ_decision_events.275', 'IRQ')
        w.choose(shown, 'SOV')
        self.assertAlmostEqual(c.var['debt'], 1)
        self.assertAlmostEqual(c.var['treasury'], cash)
        self.assertAlmostEqual(w.c['SOV'].var['treasury'], 10)
        self.accept(w, 'COLDWAR_IRQ_decision_events.272', 'SOV')
        self.assertAlmostEqual(c.var['debt'], 1.5)
        self.assertAlmostEqual(c.var['treasury'], cash+.5)
        self.assertAlmostEqual(w.c['SOV'].var['treasury'], 9.5)
        self.accept(w, 'COLDWAR_IRQ_decision_events.272', 'SOV')
        self.assertAlmostEqual(c.var['debt'], 1.5)
        self.assertAlmostEqual(c.var['treasury'], cash+.5)
        self.assertAlmostEqual(w.c['SOV'].var['treasury'], 9.5)

    def test_refresh_never_replays_foreign_offer_or_material_reward(self):
        w, c = self.world('bakr_unity'); w.call_irq('apply_bakr_unity')
        before = (c.var['treasury'], deepcopy(w.assets), deepcopy(w.research), list(w.event_queue))
        for _ in range(3): w.call_irq('reconcile_programmes')
        self.assertEqual((c.var['treasury'], w.assets, w.research, w.event_queue), before)

    def test_legacy_refresh_only_records_upgrade_without_delivering_or_charging(self):
        w, c = self.world('national_front', fresh=False)
        c.flags[P+'national_front_implemented'] = c.flags[P+'national_front_reward_v3_current'] = None
        for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION, reward_overhaul.VERSION):
            c.flags[marker] = None
        w.call_irq('migrate_focus_owned_reforms')
        self.assertAlmostEqual(c.var['treasury'], 10)
        self.assertFalse(w.flag(c, P+'front_accepted'))
        self.assertFalse(w.assets); self.assertFalse(w.research)
        pending = P+'focus_owned_national_front_pending'
        self.assertTrue(w.flag(c, pending))
        c.var['treasury'] = 0; w.call_irq('upgrade_focus_owned_national_front')
        self.assertFalse(w.flag(c, P+'front_accepted'))
        c.var['treasury'] = .1; w.call_irq('upgrade_focus_owned_national_front')
        self.assertTrue(w.flag(c, P+'front_accepted'))
        self.assertAlmostEqual(c.var['treasury'], 0)
        w.call_irq('upgrade_focus_owned_national_front'); w.call_irq('migrate_focus_owned_reforms')
        self.assertAlmostEqual(c.var['treasury'], 0)

    def test_legacy_paid_front_is_not_charged_twice(self):
        w, c = self.world('national_front', fresh=False)
        for flag in ('national_front_implemented', 'national_front_reward_v3_current', 'front_accepted', 'legalization_accepted'):
            c.flags[P+flag] = None
        w.arrays['IRQ']['gov_coalition_array'] = {4}
        w.call_irq('migrate_focus_owned_reforms')
        w.call_irq('upgrade_focus_owned_national_front')
        self.assertAlmostEqual(c.var['treasury'], 10)
        self.assertEqual(w.arrays['IRQ']['gov_coalition_array'], {4})

    def test_legacy_labour_charter_modifiers_wait_for_paid_revision(self):
        w, c = self.world('front_guarantees', fresh=False)
        n = self.nodes['front_guarantees']
        for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION, reward_overhaul.VERSION):
            c.flags[marker] = None
        for suffix in ('_implemented', '_package_earned', '_reward_v3_current'):
            c.flags[n['id']+suffix] = None
        c.flags[P+'front_accepted'] = c.flags[P+'legalization_accepted'] = None
        w.arrays['IRQ']['gov_coalition_array'] = {4}
        w.call_irq('reconcile_programmes')
        self.assertAlmostEqual(c.var[P+'baath_civilian_factories_productivity'], 0)
        self.assertAlmostEqual(c.var[P+'baath_social_cost_multiplier_modifier'], 0)
        self.assertFalse(w.flag(c, streamline.receipt(n)))
        price = 10*(n['budget_gdp_share']-apply_streamlining.original_shares()[n['key']])
        self.assertGreater(price, 0)
        c.var['treasury'] = price-.001
        w.call_irq('upgrade_focus_owned_front_guarantees'); w.call_irq('reconcile_programmes')
        self.assertFalse(w.flag(c, streamline.receipt(n)))
        self.assertAlmostEqual(c.var[P+'baath_civilian_factories_productivity'], 0)
        c.var['treasury'] = price
        w.call_irq('upgrade_focus_owned_front_guarantees'); w.call_irq('reconcile_programmes')
        self.assertTrue(w.flag(c, streamline.receipt(n)))
        self.assertAlmostEqual(c.var['treasury'], 0)
        self.assertAlmostEqual(c.var[P+'baath_civilian_factories_productivity'], .05)
        self.assertAlmostEqual(c.var[P+'baath_social_cost_multiplier_modifier'], .02)

    def test_legacy_readiness_supplement_never_repeats_earned_experience(self):
        w, c = self.world('defence_readiness', fresh=False)
        n = self.nodes['defence_readiness']
        for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION, reward_overhaul.VERSION):
            c.flags[marker] = None
        for suffix in ('_implemented', '_package_earned', '_reward_v3_current'):
            c.flags[n['id']+suffix] = None
        for component in n['overhaul_components']:
            c.flags[component['receipt']] = None
        c.var['army_xp'] = 35
        w.call_irq('migrate_focus_owned_reforms')
        price = c.var[P+'focus_owned_defence_readiness_upgrade_invoice']
        self.assertGreater(price, 0)
        c.var['treasury'] = price-.001; w.call_irq('upgrade_focus_owned_defence_readiness')
        self.assertFalse(w.idea(c, P+'readiness_cycle'))
        self.assertEqual(c.var['army_xp'], 35)
        c.var['treasury'] = price; w.call_irq('upgrade_focus_owned_defence_readiness')
        self.assertAlmostEqual(c.var['treasury'], 0)
        self.assertEqual(c.var['army_xp'], 35)
        self.assertTrue(w.idea(c, P+'readiness_cycle'))
        expiry = c.ideas[P+'readiness_cycle']; w.day = 30
        w.call_irq('upgrade_focus_owned_defence_readiness'); w.call_irq('reconcile_programmes')
        self.assertEqual(c.ideas[P+'readiness_cycle'], expiry)
        self.assertEqual(c.var['army_xp'], 35)

    def test_old_v2_kuwait_revision_defers_new_office_until_own_appropriation(self):
        w, c = self.world('foreign_kuwait', fresh=False)
        n = self.nodes['foreign_kuwait']
        for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION): c.flags[marker] = None
        c.flags[n['id']+'_implemented'] = c.flags[n['id']+'_package_earned'] = None
        w.call_irq('migrate_direct_rewards_v3')
        w.call_irq('upgrade_reward_v3_foreign_kuwait')
        self.assertFalse(w.assets)
        self.assertTrue(w.flag(c, n['id']+'_reward_v3_current'))
        self.assertFalse(w.flag(c, streamline.receipt(n)))
        price = c.var[P+'focus_owned_foreign_kuwait_upgrade_invoice']
        self.assertAlmostEqual(price, .2)
        c.var['treasury'] = price-.001; w.call_irq('upgrade_focus_owned_foreign_kuwait')
        self.assertFalse(w.assets)
        c.var['treasury'] = price; w.call_irq('upgrade_focus_owned_foreign_kuwait')
        self.assertEqual(w.assets, [('171', 'offices', 1)])
        self.assertAlmostEqual(c.var['treasury'], 0)
        w.call_irq('upgrade_focus_owned_foreign_kuwait'); w.call_irq('upgrade_reward_v3_foreign_kuwait')
        self.assertEqual(w.assets, [('171', 'offices', 1)])
        self.assertAlmostEqual(c.var['treasury'], 0)

    def test_pending_v3_and_v2_focus_quotes_keep_historic_gdp_and_reprice_once(self):
        n = self.nodes['national_front']
        for revision in ('v3', 'v2'):
            with self.subTest(revision=revision):
                w, c = self.world('national_front', fresh=False)
                for marker in (audit_migration.VERSION, audit_migration.QUOTE_VERSION): c.flags[marker] = None
                if revision == 'v3': c.flags[reward_overhaul.VERSION] = None
                share = (apply_streamlining.original_shares()[n['key']] if revision == 'v3'
                         else n['overhaul_previous_share'])
                self.assertGreater(share, 0)
                c.flags[n['id']+'_quoted'] = c.flags[n['id']+'_pending'] = None
                c.var[n['id']+'_invoice'] = 10*share
                c.var.update(gdp_total=100, treasury=0)
                for _ in range(2):
                    w.call_irq('apply_national_front')
                    self.assertAlmostEqual(c.var[n['id']+'_invoice'], 10*n['budget_gdp_share'])
                    self.assertAlmostEqual(c.var['treasury'], 0)
                    self.assertFalse(w.flag(c, P+'front_accepted'))

    def test_focus_previews_expose_permanent_guarantee_cost(self):
        focuses = {first(f, 'id'): f for f in values(first(parse(self.out[FOCUSES]), 'focus_tree'), 'focus')}
        for key in ('review_detentions', 'officer_amnesty', 'national_front', 'officer_civic_timetable'):
            reward = first(focuses[P+key], 'completion_reward')
            native_preview = [v for k, _, v in reward if k == 'effect_tooltip']
            self.assertTrue(any(k == 'add_ideas' and v == P+'civil_rights_cost'
                                for rows in native_preview for k, _, v in walk(rows)), key)


if __name__ == '__main__':
    unittest.main(verbosity=2)
