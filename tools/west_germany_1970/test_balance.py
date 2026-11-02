# IMPERIA COLD WAR — Emitted multiplayer balance and consent transaction regression.
"""Native-subset source model. External MD budget/programme/rendering/netcode APIs are explicit boundaries."""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/diplomacy_1970'))
from test_diplomacy import DiplomacyModel, Scope, D, first, load, walk

P = 'COLDWAR_GER_1970'
S = P + '_settlement'


class BalanceModel(DiplomacyModel):
    def __init__(self):
        super().__init__()
        self.c = {tag: Scope(tag) for tag in ('GER', 'DDR', 'SOV', 'ENG', 'SWI', 'USA')}
        self.s['1251'] = Scope('1251', 'state')
        self.s['1251'].owner = self.s['1251'].controller = self.c['GER']
        self.root = self.c['GER']
        for kind in ('effects', 'triggers'):
            for stem in (P + '_windows_' + ('effects' if kind == 'effects' else 'triggers'),
                         P + ('_effects' if kind == 'effects' else '_balance_diplomacy'),
                         P + '_balance_diplomacy', 'COLDWAR_DDR_1970_relations'):
                path = ROOT / 'common' / ('scripted_' + kind) / (stem + '.txt')
                if path.exists(): getattr(self, kind).update((k, v) for k, o, v in load(str(path.relative_to(ROOT))))
        support = load('common/scripted_effects/IMP_sanctions_support_effects.txt')
        self.effects['IMP_sanctions_add_dip_from_prev'] = first(support, 'IMP_sanctions_add_dip_from_prev')
        self.external = []
        self.effects[P + '_rv_gui_refresh'] = []
        self.effects[P + '_east_gui_refresh'] = []
        self.effects[P + '_rv_set_stage_modifiers'] = []
        self.effects[P + '_rv_ask_east_berlin'] = []

    def value(self, name, current, root, prev):
        if isinstance(name, str) and '^' in name:
            array, suffix = name.rsplit('^', 1)
            obj, key = self.variable(array, current, root, prev)
            values = obj.vars.get(key)
            if isinstance(values, list):
                if suffix == 'num': return D(len(values))
                if suffix.isdigit(): return values[int(suffix)] if int(suffix) < len(values) else D(0)
        return super().value(name, current, root, prev)

    def condition(self, rows, current, root=None, prev=None):
        root = root or current
        for k, o, v in rows:
            if k == 'has_capitulated': result = ('_capitulated' in current.flags) == (v == 'yes')
            elif k == 'has_war_with':
                target = self.scope(v, current, root, prev)
                result = target is not None and target.id in current.wars
            elif k == 'exists': result = (current in self.c.values()) == (v == 'yes')
            elif k == 'is_in_array':
                name, value = (first(v, 'array'), first(v, 'value')) if first(v, 'array') is not None else (v[0][0], v[0][2])
                obj, key = self.variable(name, current, root, prev)
                result = self.value(value, current, root, prev) in obj.vars.get(key, [])
            else: result = super().condition([(k, o, v)], current, root, prev)
            if not result: return False
        return True

    def execute(self, rows, current, root, prev):
        # Keep ordinary if/else runs together so branch state is never lost.
        ordinary = []
        for k, o, v in rows:
            special = k in ('white_peace', 'transfer_state', 'add_to_array', 'remove_from_array', 'add_power_balance_value',
                            'imp_sanctions_calculate', 'mdcw_cw_on_sanction_imposed', 'mdcw_cw_recalculate_capacity', P + '_start_programme')
            if not special:
                ordinary.append((k, o, v)); continue
            if ordinary:
                super().execute(ordinary, current, root, prev); ordinary = []
            if k in ('add_to_array', 'remove_from_array'):
                name, value = (first(v, 'array'), first(v, 'value')) if first(v, 'array') is not None else (v[0][0], v[0][2])
                obj, key = self.variable(name, current, root, prev)
                target = self.value(value, current, root, prev)
                values = obj.vars.setdefault(key, [])
                if k == 'add_to_array': values.append(target)
                else: values[:] = [item for item in values if item is not target]
            elif k == 'white_peace':
                target = self.scope(v, current, root, prev)
                current.wars.discard(target.id); target.wars.discard(current.id)
                self.external.append((k, current.id, target.id))
            elif k == 'transfer_state': self.s[v].owner = self.s[v].controller = current
            elif k == 'add_power_balance_value':
                current.vars['_bop'] = current.vars.get('_bop', D(0)) + D(first(v, 'value'))
            else: self.external.append((k, current.id))
        if ordinary: super().execute(ordinary, current, root, prev)


class Balance(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.template = BalanceModel()

    def setUp(self):
        self.m = copy.deepcopy(self.template)
        self.g, self.d = self.m.c['GER'], self.m.c['DDR']
        self.g.flags.update(('cwgg_initialized', P + '_initialized', 'mdcw_cw_initialized'))
        self.d.flags.update((P + '_ddr_initialized', 'COLDWAR_DDR_initialized', 'mdcw_cw_initialized'))
        self.m.g.flags.add('mdcw_cw_initialized')
        self.g.vars.update(cwgg_init_brd=D(6), cwgg_init_ddr=D(6), cwgg_krise_typ=D(0), cwgg_countdown=D(0),
                           cwgg_hebel_devisen=D(1), cwgg_klima=D(0), cwgg_stufe=D(2), ruling_party=D(1),
                           gdp_total=D(500), treasury=D(10), mdcw_cw_cap_free=D(4), cwger_stasi_penetration=D(50),
                           cwger_counterintel=D(35), cwgg_hebel_medien=D(2), cwgg_hebel_handel=D(1))
        self.d.vars.update(cwddr_hard_currency=D(60), cwddr_west_dependency=D(10), cwddr_sed_control=D(85),
                           cwddr_exit_pressure=D(30), treasury=D(1))
        self.g.pp = self.d.pp = D(500)

    def apply(self, name, actor=None): self.m.run(name, actor or self.g)

    def war(self, a='GER', b='DDR'):
        self.m.c[a].wars.add(b); self.m.c[b].wars.add(a)
        self.m.g.flags.add('cwgg_german_war')

    def test_two_month_clock_waits_for_both_humans_and_charges_at_resolution(self):
        self.g.vars.update(cwgg_krise_typ=D(5), cwgg_krise_monat=D(0), cwgg_brd_order_ready=D(0), cwgg_ddr_order_ready=D(0))
        self.m.effects[P + '_rv_round'] = [('add_to_variable', '=', [('_round_calls', '=', '1')])]
        self.apply(P + '_rv_crisis_clock')
        self.assertEqual(self.g.vars['cwgg_krise_monat'], 1)
        self.assertNotIn('_round_calls', self.g.vars)
        self.apply(P + '_rv_crisis_clock')
        self.assertEqual(self.g.vars['cwgg_krise_monat'], 1)
        self.assertNotIn('_round_calls', self.g.vars)
        self.g.vars.update(cwgg_brd_order_ready=D(1), cwgg_ddr_order_ready=D(1))
        self.apply(P + '_rv_crisis_clock')
        self.assertEqual(self.g.vars['_round_calls'], 1)
        self.assertEqual(self.g.vars['cwgg_krise_monat'], 0)
        self.apply(P + '_rv_crisis_clock')
        self.assertEqual(self.g.vars['_round_calls'], 1)
        self.apply(P + '_rv_crisis_clock')
        self.assertEqual(self.g.vars['_round_calls'], 2)

    def test_credit_proposal_and_refusal_have_no_concessions_or_treasury_charge(self):
        self.apply(P + '_rv_act_credit')
        self.assertEqual(self.g.pp, 450)
        self.assertEqual(self.g.vars['cwgg_init_brd'], 4)
        self.assertEqual(self.g.vars['cwgg_klima'], 0)
        self.assertEqual(self.g.vars['treasury'], 10)
        self.assertEqual(self.d.vars['cwddr_hard_currency'], 60)
        self.apply(P + '_balance_refuse_credit', self.d)
        self.assertNotIn(P + '_balance_credit_pending', self.g.flags)
        self.apply(P + '_balance_accept_credit', self.d)
        self.assertEqual(self.g.vars['treasury'], 10)
        self.assertEqual(self.g.vars['cwgg_klima'], 0)

    def test_credit_acceptance_executes_once_and_rechecks_live_terms(self):
        self.apply(P + '_rv_act_credit')
        self.apply(P + '_balance_accept_credit', self.d)
        self.assertEqual(self.g.vars['treasury'], D('9.5'))
        self.assertEqual(self.g.vars['cwgg_klima'], 10)
        self.assertEqual(self.g.vars['cwgg_hebel_devisen'], 2)
        self.assertEqual(self.d.vars['cwddr_hard_currency'], 45)
        self.assertEqual(self.g.vars['_bop'], D('0.12'))
        self.apply(P + '_balance_accept_credit', self.d)
        self.assertEqual(self.g.vars['treasury'], D('9.5'))
        self.setUp(); self.apply(P + '_rv_act_credit')
        self.d.vars['cwddr_hard_currency'] = D(20)
        self.apply(P + '_balance_accept_credit', self.d)
        self.assertEqual(self.g.vars['treasury'], 10)

    def test_swing_launches_real_programme_once_after_acceptance_only(self):
        self.apply(P + '_rv_act_swing')
        self.assertEqual(self.g.vars['cwgg_klima'], 0)
        self.assertFalse(any(row[0] == P + '_start_programme' for row in self.m.external))
        self.apply(P + '_balance_accept_swing', self.d)
        self.assertEqual(self.g.vars['cwgg_klima'], 5)
        self.assertEqual(self.d.vars['cwddr_hard_currency'], 54)
        self.assertEqual(sum(row[0] == P + '_start_programme' for row in self.m.external), 1)
        self.apply(P + '_balance_accept_swing', self.d)
        self.assertEqual(sum(row[0] == P + '_start_programme' for row in self.m.external), 1)

    def test_swing_refusal_capacity_loss_and_war_never_grant_partial_terms(self):
        for problem in ('refusal', 'capacity', 'war'):
            with self.subTest(problem=problem):
                self.setUp(); self.apply(P + '_rv_act_swing')
                if problem == 'refusal': self.apply(P + '_balance_refuse_swing', self.d)
                if problem == 'capacity': self.g.vars['mdcw_cw_cap_free'] = D(1)
                if problem == 'war': self.war()
                self.apply(P + '_balance_accept_swing', self.d)
                self.assertEqual(self.g.vars['cwgg_klima'], 0)
                self.assertEqual(self.d.vars['cwddr_hard_currency'], 60)
                self.assertFalse(any(row[0] == P + '_start_programme' for row in self.m.external))
    def test_shared_defence_cooldown_blocks_second_operation_and_direct_replay(self):
        self.apply(P + '_rv_act_raid')
        after = (self.g.pp, self.g.vars['cwger_stasi_penetration'], self.g.vars['cwger_counterintel'])
        self.assertEqual(after, (D(450), D(40), D(38)))
        self.apply(P + '_sec_act_counterspy')
        self.apply(P + '_rv_act_raid')
        self.assertEqual((self.g.pp, self.g.vars['cwger_stasi_penetration'], self.g.vars['cwger_counterintel']), after)

    def test_both_governments_have_matching_offensive_instruction_locks(self):
        self.apply(P + '_rv_act_media')
        before = (self.g.pp, self.d.vars['cwddr_hard_currency'])
        self.apply(P + '_rv_act_freeze')
        self.assertEqual((self.g.pp, self.d.vars['cwddr_hard_currency']), before)
        self.assertIn('cwgg_balance_offensive_cd', self.g.flags)
        self.d.flags.add('cwgg_balance_offensive_cd')
        self.assertFalse(self.m.condition(self.m.triggers[P + '_east_can_transit_checks'], self.d))

    def test_diplomatic_sanction_targets_the_frozen_recogniser_and_cannot_repeat(self):
        x = self.m.c['SWI']
        self.g.vars.update(cwgg_krise_typ=D(5), cwgg_recognition_country=[x], cwgg_special_used=D(0))
        self.g.ideas.add(P + '_idea_hallstein_legacy')
        x.vars['recognised_countries'] = [self.d]
        self.apply(P + '_rv_special_5')
        self.assertIn(x, self.g.vars['imp_dip_sanc_by_us'])
        self.assertIn(self.g, x.vars['imp_dip_sanc_on_us'])
        self.assertEqual(self.g.pp, 465)
        self.assertNotIn('imp_dip_sanc_on_us', self.d.vars)
        self.apply(P + '_rv_special_5')
        self.assertEqual(self.g.pp, 465)
        self.assertEqual(len(x.vars['imp_dip_sanc_on_us']), 1)

    def test_foreign_belligerent_signature_is_required_and_third_party_wars_survive(self):
        self.war(); self.war('GER', 'SOV'); self.war('SOV', 'ENG')
        self.apply(S + '_propose_1')
        self.apply(S + '_accept', self.d)
        self.assertIn('DDR', self.g.wars)
        self.assertIn('SOV', self.g.wars)
        self.apply(S + '_accept', self.m.c['SOV'])
        self.assertNotIn('DDR', self.g.wars)
        self.assertNotIn('SOV', self.g.wars)
        self.assertIn('ENG', self.m.c['SOV'].wars)
        self.assertIn('SOV', self.m.c['ENG'].wars)
        self.assertNotIn('cwgg_settlement_pending', self.g.flags)

    def test_refusal_cancel_and_direct_apply_without_signatures_have_no_rewards(self):
        self.war(); self.d.flags.add('_capitulated')
        self.apply(S + '_propose_3')
        self.apply(S + '_apply')
        self.assertEqual(self.g.vars['treasury'], 10)
        self.assertIn('DDR', self.g.wars)
        self.apply(S + '_refuse', self.d)
        self.apply(S + '_accept', self.d)
        self.assertEqual(self.g.vars['treasury'], 10)
        self.assertIn('DDR', self.g.wars)

    def test_reparations_paid_once_and_lost_funding_invalidates_the_offer(self):
        self.war(); self.d.flags.add('_capitulated')
        self.apply(S + '_propose_3')
        self.apply(S + '_accept', self.d)
        self.assertEqual(self.g.vars['treasury'], D('10.2'))
        self.assertEqual(self.d.vars['treasury'], D('0.8'))
        self.apply(S + '_accept', self.d)
        self.assertEqual(self.g.vars['treasury'], D('10.2'))
        self.setUp(); self.war(); self.d.flags.add('_capitulated')
        self.apply(S + '_propose_3')
        self.d.vars['treasury'] = D('0.1')
        self.apply(S + '_accept', self.d)
        self.assertEqual(self.g.vars['treasury'], 10)
        self.assertIn('DDR', self.g.wars)
        self.assertNotIn('cwgg_settlement_pending', self.g.flags)

    def test_berlin_transfer_needs_bonn_and_all_belligerents_consent(self):
        self.war(); self.g.flags.add('_capitulated')
        self.apply(S + '_propose_2', self.d)
        self.assertIs(self.m.s['1251'].owner, self.g)
        self.apply(S + '_accept', self.g)
        self.assertIs(self.m.s['1251'].owner, self.d)
        self.assertEqual(self.g.vars['treasury'], 10)

    def test_new_entrant_missing_country_or_changed_war_prevents_stale_application(self):
        for problem in ('entrant', 'missing', 'peace'):
            with self.subTest(problem=problem):
                self.setUp(); self.war(); self.apply(S + '_propose_1')
                if problem == 'entrant': self.war('GER', 'SOV')
                if problem == 'missing': del self.m.c['DDR']
                if problem == 'peace': self.g.wars.clear(); self.d.wars.clear()
                self.apply(S + '_maintenance')
                self.assertNotIn('cwgg_settlement_pending', self.g.flags)
                self.apply(S + '_accept', self.d)
                self.assertFalse(any(row[0] == 'white_peace' for row in self.m.external))

    def test_departed_belligerent_invalidates_its_old_signature_request(self):
        self.war(); self.war('GER', 'SOV'); self.apply(S + '_propose_1')
        self.g.wars.remove('SOV'); self.m.c['SOV'].wars.remove('GER')
        self.assertFalse(self.m.condition(self.m.triggers[S + '_can_sign'], self.m.c['SOV']))
        self.apply(S + '_maintenance')
        self.assertNotIn('cwgg_settlement_pending', self.g.flags)
        self.assertIn('DDR', self.g.wars)

    def test_legacy_capitulation_events_and_offer_previews_do_not_execute_outcomes(self):
        events = {first(v, 'id'): v for k, o, v in load('events/' + P + '_events.txt') if k == 'country_event'}
        forbidden = {'annex_country', P + '_absorb_ddr', 'white_peace', 'NATO_leave', 'leave_faction', 'transfer_state'}
        for eid in ('COLDWAR_GGR.40', 'COLDWAR_GGR.41'):
            self.assertFalse(forbidden & {k for k, o, v in walk(events[eid])})
            self.assertEqual(first(events[eid], 'picture'), 'GFX_political_deal')
        before = copy.deepcopy((self.g.vars, self.d.vars, self.g.wars))
        for kind in (1, 2, 3): self.apply(S + '_preview_' + str(kind))
        self.assertEqual((self.g.vars, self.d.vars, self.g.wars), before)


if __name__ == '__main__': unittest.main(verbosity=2)
