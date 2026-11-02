# IMPERIA COLD WAR — Bilateral treaty, crisis order, and unity consent contracts.
"""Execute installed German sandbox scripts with the strict shared native-subset model.

These checks exercise emitted Clausewitz effects and triggers. They do not model
HOI4 event timing, AI selection, multiplayer routing, or the game engine itself.
Unknown script statements remain errors through the inherited strict interpreter.
"""
import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/colonial_affairs"))
from test_runtime import Model, Scope, D, parse, first

P = "COLDWAR_GER_1970"
R = P + "_rv"
U = P + "_uni"
EAST = P + "_east"
EVR = "COLDWAR_GGR"
EVU = "COLDWAR_GGU"


def load(rel):
    return parse((ROOT / rel).read_text(encoding="utf-8-sig"))


class SandboxModel(Model):
    """Load only installed native scripts and add the two German country scopes."""

    def __init__(self):
        super().__init__()
        self.effects.update((k, v) for k, _op, v in load(f"common/scripted_effects/{P}_windows_effects.txt"))
        self.triggers.update((k, v) for k, _op, v in load(f"common/scripted_triggers/{P}_windows_triggers.txt"))
        self.effects.update((k, v) for k, _op, v in load(f"common/scripted_effects/{P}_effects.txt"))
        self.effects.update((k, v) for k, _op, v in load(f"common/scripted_effects/{P}_sandbox.txt"))
        self.effects.update((k, v) for k, _op, v in load(f"common/scripted_effects/{P}_balance_diplomacy.txt"))
        self.effects.update((k, v) for k, _op, v in load("common/scripted_effects/COLDWAR_DDR_1970_relations.txt"))
        self.triggers.update((k, v) for k, _op, v in load("common/scripted_triggers/COLDWAR_DDR_1970_relations.txt"))
        self.events_by_id = {}
        for key, _op, value in load(f"events/{P}_events.txt"):
            if key not in ("country_event", "news_event"):
                continue
            event_id = first(value, "id")
            if event_id:
                self.events_by_id[event_id] = value
        self.c["GER"] = Scope("GER")
        self.c["DDR"] = Scope("DDR")
        self.c["FRA"] = self.c.get("FRA", Scope("FRA"))
        self.c["SOV"] = self.c.get("SOV", Scope("SOV"))
        self.c["USA"] = self.c.get("USA", Scope("USA"))
        self.c["ENG"] = self.c.get("ENG", Scope("ENG"))
        self.root = self.c["GER"]

    def condition(self, rows, current, root=None, prev=None):
        """Add the native division-count predicate to the strict shared interpreter."""
        def lower(items):
            lowered = []
            for key, op, value in items:
                if key == "divisions_in_state":
                    state = first(value, "state")
                    size = next((row for row in value if row[0] == "size"), None)
                    if state is None or size is None:
                        raise ValueError("Malformed native divisions_in_state predicate")
                    variable = f"_test_divisions_{current.id}_{state}"
                    comparison = {">": "greater_than", ">=": "greater_than_or_equals", "=": "equals",
                                  "<": "less_than", "<=": "less_than_or_equals"}[size[1]]
                    lowered.append(("check_variable", "=", [("var", "=", variable), ("compare", "=", comparison), ("value", "=", size[2])]))
                elif key == "is_in_faction_with":
                    lowered.append(("has_country_flag", "=", f"_test_in_faction_{value}"))
                elif isinstance(value, list):
                    lowered.append((key, op, lower(value)))
                else:
                    lowered.append((key, op, value))
            return lowered
        return super().condition(lower(rows), current, root, prev)

    def execute(self, rows, current, root, prev):
        """Model the native primitives used by these consent and war contracts."""
        last_if = None
        for key, op, value in rows:
            if key == "if":
                last_if = self.condition(first(value, "limit", []), current, root, prev)
                if last_if:
                    self.execute([(k, o, v) for k, o, v in value if k != "limit"], current, root, prev)
            elif key == "else_if":
                if last_if is False:
                    last_if = self.condition(first(value, "limit", []), current, root, prev)
                    if last_if:
                        self.execute([(k, o, v) for k, o, v in value if k != "limit"], current, root, prev)
            elif key == "else":
                if last_if is False:
                    self.execute(value, current, root, prev)
                last_if = None
            elif key == "set_global_flag":
                self.g.flags.add(value)
            elif key == "clr_global_flag":
                self.g.flags.discard(value)
            elif key == "declare_war_on":
                target = self.c.get(first(value, "target"))
                if target is None:
                    raise ValueError("Unknown native war target " + str(first(value, "target")))
                current.wars.add(target.id)
                target.wars.add(current.id)
            elif key == "add_to_war":
                target = self.c.get(first(value, "target"))
                if target is None:
                    raise ValueError("Unknown native war target " + str(first(value, "target")))
                current.wars.add(target.id)
                target.wars.add(current.id)
            elif key == "every_other_country":
                limit = first(value, "limit", [])
                body = [(k, o, v) for k, o, v in value if k != "limit"]
                for country in self.c.values():
                    if country is not current and self.condition(limit, country, root, current):
                        self.execute(body, country, root, current)
            elif key == "for_each_scope_loop":
                obj, name = self.variable(first(value, "array"), current, root, prev)
                for target in list(obj.vars.get(name, [])):
                    self.execute([row for row in value if row[0] != "array"], target, root, current)
            elif key == "clear_array":
                obj, name = self.variable(value, current, root, prev)
                obj.vars[name] = []
            else:
                super().execute([(key, op, value)], current, root, prev)

    def event_options(self, event_id):
        event = self.events_by_id[event_id]
        return [v for k, _op, v in event if k == "option"]

    def run_option(self, event_id, index, scope):
        option = self.event_options(event_id)[index]
        ignored = {"name", "ai_chance", "trigger", "tooltip", "highlighted"}
        body = [(k, op, value) for k, op, value in option if k not in ignored]
        self.execute(body, scope, scope, None)

    @staticmethod
    def contains_key(rows, sought):
        return any(key == sought or (isinstance(value, list) and SandboxModel.contains_key(value, sought))
                   for key, _op, value in rows)


class BilateralSandbox(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = SandboxModel()

    def setUp(self):
        self.m = copy.deepcopy(self.template)
        self.g = self.m.c["GER"]
        self.d = self.m.c["DDR"]
        self.m.root = self.g
        self.g.flags.update((P + "_initialized", "cwgg_initialized", "cwgg_unlock_vertrag_1"))
        self.d.flags.update((P + "_ddr_initialized", "COLDWAR_DDR_initialized"))
        self.g.pp = D(500)
        self.d.pp = D(500)
        self.g.vars.update(
            cwgg_init_brd=D(6), cwgg_init_ddr=D(6), cwgg_klima=D(50), cwgg_stufe=D(1),
            cwgg_verh=D(0), cwgg_verh_prog=D(0), cwgg_tr_pending=D(0), cwgg_tr_ready=D(0),
            cwgg_tr_invalid=D(0), cwgg_tr_sender=D(0), cwgg_krise_typ=D(1), cwgg_countdown=D(0),
            cwgg_haltung=D(1), cwgg_ddr_wahl=D(0), cwgg_brd_order_ready=D(0), cwgg_ddr_order_ready=D(0),
            cwgg_mob_brd=D(0), cwgg_mob_ddr=D(0), cwgg_aufm_ddr=D(0), cwgg_u_phase=D(0),
            cwgg_u_cur=D(1), cwgg_u_pos=D(0), cwgg_u_dpos=D(0), cwgg_u_m=D(0),
        )
        for treaty in range(1, 10):
            self.g.vars[f"cwgg_vertrag_{treaty}"] = D(0)
        self.g.vars["cwgg_vertrag_3"] = D(1)
        self.d.ai = False
        self.g.ai = False

    def run_effect(self, name, scope=None):
        self.m.run(name if name.startswith(P + "_") else P + "_" + name, scope or self.g)

    def set_ready_treaty(self, sender=1):
        self.g.vars.update(cwgg_verh=D(6), cwgg_verh_prog=D(100), cwgg_tr_ready=D(6),
                           cwgg_tr_pending=D(0), cwgg_tr_invalid=D(0), cwgg_tr_sender=D(sender))

    def set_ready_unity(self):
        self.g.focuses.add(P + "_european_peace_order")
        self.g.vars.update(cwgg_u_phase=D(0), cwgg_klima=D(75), cwgg_stufe=D(0), cwgg_krise_typ=D(0),
                           cwgg_detente_m=D(36), cwgg_init_ddr=D(6), cwgg_init_brd=D(6),
                           cwgg_vertrag_3=D(1), cwgg_vertrag_5=D(1), cwgg_vertrag_6=D(1),
                           cwgg_vertrag_7=D(1))

    def test_ddr_and_bonn_can_each_initiate_at_the_existing_price(self):
        ddr_trigger = self.m.triggers[EAST + "_can_treaty_6"]
        self.assertTrue(self.m.condition(ddr_trigger, self.d))
        self.run_effect("east_act_treaty_6", self.d)
        self.assertEqual((self.d.pp, self.g.vars["cwgg_init_ddr"]), (D(475), D(4)))
        self.assertEqual((self.g.vars["cwgg_verh"], self.g.vars["cwgg_tr_sender"], self.g.vars["cwgg_vertrag_6"]),
                         (D(6), D(2), D(0)))
        self.run_effect("east_act_treaty_6", self.d)
        self.assertEqual((self.d.pp, self.g.vars["cwgg_init_ddr"]), (D(475), D(4)))

        self.setUp()
        self.assertTrue(self.m.condition(self.m.triggers[R + "_can_treaty_6"], self.g))
        self.run_effect("rv_start_treaty_6", self.g)
        self.assertEqual((self.g.pp, self.g.vars["cwgg_init_brd"]), (D(475), D(4)))
        self.assertEqual((self.g.vars["cwgg_verh"], self.g.vars["cwgg_tr_sender"], self.g.vars["cwgg_vertrag_6"]),
                         (D(6), D(1), D(0)))
        self.run_effect("rv_start_treaty_6", self.g)
        self.assertEqual((self.g.pp, self.g.vars["cwgg_init_brd"]), (D(475), D(4)))

    # IMPERIA COLD WAR — Recipient refusal and save/war transition regressions.
    def test_bonn_declines_ddr_offer_and_releases_the_slot_without_refunding_preparation(self):
        self.run_effect("east_act_treaty_6", self.d)
        self.g.vars["cwgg_verh_prog"] = D(100)
        self.run_effect("rv_negotiation_tick")
        paid = (self.g.pp, self.d.pp, self.g.vars['cwgg_init_brd'], self.g.vars['cwgg_init_ddr'])
        climate = self.g.vars['cwgg_klima']
        option = self.m.event_options(EVR + '.50')[3]
        self.assertTrue(self.m.condition(first(option,'trigger'),self.g))
        self.m.run_option(EVR + '.50',3,self.g)
        for key in ('cwgg_verh','cwgg_verh_prog','cwgg_tr_ready','cwgg_tr_pending','cwgg_tr_invalid','cwgg_tr_sender'):
            self.assertEqual(self.g.vars[key],0,key)
        self.assertEqual(self.g.vars['cwgg_vertrag_6'],0)
        self.assertEqual(self.g.vars['cwgg_klima'],climate)
        self.assertEqual((self.g.pp,self.d.pp,self.g.vars['cwgg_init_brd'],self.g.vars['cwgg_init_ddr']),paid)
        self.assertTrue(self.m.condition(self.m.triggers[EAST+'_can_treaty_6'],self.d))
        self.assertTrue(self.m.condition(self.m.triggers[R+'_can_treaty_6'],self.g))
        before=copy.deepcopy((self.g.vars,self.d.vars,self.g.pp,self.d.pp))
        self.m.run_option(EVR+'.50',3,self.g)
        self.assertEqual((self.g.vars,self.d.vars,self.g.pp,self.d.pp),before)

    def test_bonn_cannot_cancel_after_sending_its_signature_to_ddr(self):
        self.set_ready_treaty()
        self.g.vars['cwgg_tr_pending']=D(6)
        before=copy.deepcopy((self.g.vars,self.d.vars,self.g.pp,self.d.pp))
        option=self.m.event_options(EVR+'.50')[3]
        self.assertFalse(self.m.condition(first(option,'trigger'),self.g))
        self.m.run_option(EVR+'.50',3,self.g)
        self.assertEqual((self.g.vars,self.d.vars,self.g.pp,self.d.pp),before)

    def test_old_save_negotiations_keep_progress_and_still_require_ddr_acceptance(self):
        for progress in (D(47),D(100)):
            with self.subTest(progress=progress):
                self.setUp()
                self.g.flags.update((P+'_sandbox_installed','cwgg_tr_brd_dialogue_open'))
                self.g.vars.update(cwgg_verh=D(6),cwgg_verh_prog=progress)
                for key in ('cwgg_tr_sender','cwgg_tr_ready','cwgg_tr_pending','cwgg_tr_invalid'):
                    self.g.vars.pop(key,None)
                paid=(self.g.pp,self.d.pp,self.g.vars['cwgg_init_brd'],self.g.vars['cwgg_init_ddr'])
                self.run_effect('sandbox_migrate')
                self.assertEqual(self.g.vars['cwgg_verh_prog'],progress)
                self.assertEqual(self.g.vars['cwgg_tr_sender'],1)
                if progress==100:
                    self.assertTrue(self.m.condition(self.m.triggers[R+'_can_review_treaty'],self.g))
                for _ in range(8):
                    if self.g.vars.get('cwgg_tr_ready',0)==6:break
                    self.run_effect('rv_negotiation_tick')
                self.assertEqual(self.g.vars['cwgg_tr_ready'],6)
                self.m.run_option(EVR+'.50',1,self.g)
                self.assertEqual(self.g.vars['cwgg_vertrag_6'],0)
                self.assertEqual(self.g.vars['cwgg_tr_pending'],6)
                self.assertEqual(self.m.events[-1][:2],(EVR+'.256','DDR'))
                self.m.run_option(EVR+'.256',1,self.d)
                self.assertEqual(self.g.vars['cwgg_vertrag_6'],1)
                self.assertEqual((self.g.pp,self.d.pp,self.g.vars['cwgg_init_brd'],self.g.vars['cwgg_init_ddr']),paid)

    def test_migration_preserves_current_ddr_proposals_and_pending_signatures(self):
        for sender,pending in ((2,0),(1,6)):
            with self.subTest(sender=sender,pending=pending):
                self.setUp();self.g.flags.add(P+'_sandbox_installed')
                self.g.vars.update(cwgg_verh=D(6),cwgg_verh_prog=D(80),cwgg_tr_sender=D(sender),cwgg_tr_pending=D(pending))
                before=copy.deepcopy((self.g.vars,self.d.vars,self.g.pp,self.d.pp))
                self.run_effect('sandbox_migrate')
                self.assertEqual((self.g.vars,self.d.vars,self.g.pp,self.d.pp),before)
                self.g.vars.update(cwgg_brd_order_ready=D(1),cwgg_ddr_order_ready=D(1))
                before=copy.deepcopy((self.g.vars,self.d.vars,self.g.pp,self.d.pp))
                self.run_effect('sandbox_migrate')
                self.assertEqual((self.g.vars,self.d.vars,self.g.pp,self.d.pp),before)

    def test_peace_clears_unanswered_armistice_for_the_next_war(self):
        for effect in ('rv_cold_peace','rv_war_watch'):
            with self.subTest(effect=effect):
                self.setUp();self.g.wars.add('DDR');self.d.wars.add('GER')
                self.m.run_option(EVR+'.31',1,self.g)
                self.assertIn('cwgg_armistice_request',self.d.flags)
                self.g.wars.clear();self.d.wars.clear()
                self.run_effect(effect)
                self.assertNotIn('cwgg_armistice_request',self.d.flags)
                self.g.wars.add('DDR');self.d.wars.add('GER')
                option=self.m.event_options(EVR+'.31')[1]
                self.assertTrue(self.m.condition(first(option,'trigger'),self.g))
                self.m.run_option(EVR+'.31',1,self.g)
                self.assertIn('cwgg_armistice_request',self.d.flags)

    def test_new_war_discards_an_old_request_even_without_a_peace_tick(self):
        self.d.flags.add('cwgg_armistice_request')
        self.g.flags.add('cwgg_strike_ordered')
        self.run_effect('rv_final_resolution')
        self.assertIn('GER',self.d.wars)
        self.assertNotIn('cwgg_armistice_request',self.d.flags)
        self.assertTrue(self.m.condition(first(self.m.event_options(EVR+'.31')[1],'trigger'),self.g))

    def test_stale_armistice_defer_clears_request_without_requeuing_after_peace(self):
        self.d.flags.add('cwgg_armistice_request')
        before=len(self.m.events)
        self.m.run_option(EVR+'.260',0,self.d)
        self.assertNotIn('cwgg_armistice_request',self.d.flags)
        self.assertEqual(len(self.m.events),before)

    def test_basic_treaty_keeps_the_requested_no_majority_gate(self):
        self.g.vars.update(cwgg_verh=D(3),cwgg_verh_prog=D(100),cwgg_tr_ready=D(3),cwgg_tr_sender=D(1),
                           cwgg_vertrag_1=D(1),cwgg_vertrag_2=D(1),cwgg_vertrag_3=D(0),cwger_margin=D(-20))
        self.g.flags.add('cwgg_unlock_vertrag_3')
        self.assertTrue(self.m.condition(self.m.triggers[R+'_can_ratify_3'],self.g))
        self.m.run_option(EVR+'.50',1,self.g)
        self.assertEqual(self.g.vars['cwgg_tr_pending'],3)
        self.assertEqual(self.g.vars['cwgg_vertrag_3'],0)
        self.assertEqual(self.m.events[-1][:2],(EVR+'.253','DDR'))

    def test_agreement_requires_bonn_signature_then_human_ddr_acceptance(self):
        self.set_ready_treaty(sender=1)
        self.run_effect("rv_ratify_6", self.g)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(0))

        self.m.run_option(EVR + ".50", 1, self.g)
        self.assertEqual(self.g.vars["cwgg_tr_pending"], D(6))
        self.assertIn((EVR + ".256", "DDR", {}), self.m.events)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(0))

        self.m.run_option(EVR + ".256", 1, self.d)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(1))
        applied_climate = self.g.vars["cwgg_klima"]
        self.m.run_option(EVR + ".256", 1, self.d)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(1))
        self.assertEqual(self.g.vars["cwgg_klima"], applied_climate)
        self.assertEqual(self.g.vars["cwgg_tr_pending"], D(0))

    def test_first_treaty_options_defer_without_acceptance_and_review_reopens_once(self):
        self.set_ready_treaty()
        self.g.flags.add("cwgg_tr_brd_dialogue_open")
        self.m.run_option(EVR + ".50", 0, self.g)
        self.assertNotIn("cwgg_tr_brd_dialogue_open", self.g.flags)
        self.assertEqual((self.g.vars["cwgg_tr_ready"], self.g.vars["cwgg_vertrag_6"]), (D(6), D(0)))
        self.assertTrue(self.m.condition(self.m.triggers[R + "_can_review_treaty"], self.g))
        self.run_effect("rv_review_treaty", self.g)
        self.assertIn("cwgg_tr_brd_dialogue_open", self.g.flags)
        self.assertEqual(self.m.events[-1][:2], (EVR + ".50", "GER"))
        before = len(self.m.events)
        self.assertFalse(self.m.condition(self.m.triggers[R + "_can_review_treaty"], self.g))
        self.run_effect("rv_review_treaty", self.g)
        self.assertEqual(len(self.m.events), before)

        self.g.vars["cwgg_tr_pending"] = D(6)
        self.d.flags.add("cwgg_tr_ddr_dialogue_open")
        self.assertFalse(self.m.condition(self.m.triggers[EAST + "_can_review_treaty"], self.d))
        self.m.run_option(EVR + ".256", 0, self.d)
        self.assertNotIn("cwgg_tr_ddr_dialogue_open", self.d.flags)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(0))
        self.assertTrue(self.m.condition(self.m.triggers[EAST + "_can_review_treaty"], self.d))
        self.run_effect("east_review_treaty", self.d)
        self.assertIn("cwgg_tr_ddr_dialogue_open", self.d.flags)
        self.assertEqual(self.m.events[-1][:2], (EVR + ".256", "DDR"))

    def test_stale_acceptance_rechecks_ratification_and_cannot_apply_twice(self):
        self.set_ready_treaty(sender=1)
        self.g.vars["cwgg_tr_pending"] = D(6)
        self.g.vars["cwgg_klima"] = D(-100)
        self.m.run_option(EVR + ".256", 1, self.d)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(0))
        self.assertEqual(self.g.vars["cwgg_tr_invalid"], D(1))
        self.assertEqual(self.g.vars["cwgg_tr_pending"], D(6))
        self.g.vars["cwgg_klima"] = D(50)
        self.m.run_option(EVR + ".256", 1, self.d)
        self.assertEqual(self.g.vars["cwgg_vertrag_6"], D(0))

    def test_human_crisis_orders_wait_and_invalid_orders_are_not_charged(self):
        before = (copy.deepcopy(self.g.vars), copy.deepcopy(self.d.vars), self.g.pp, self.d.pp)
        self.run_effect("rv_round", self.g)
        self.assertEqual((self.g.vars, self.d.vars, self.g.pp, self.d.pp), before)

        self.g.vars.update(cwgg_brd_order_ready=D(1), cwgg_haltung=D(5), cwgg_ddr_order_ready=D(1), cwgg_ddr_wahl=D(1))
        self.g.vars["cwgg_vertrag_6"] = D(1)
        before = (self.g.vars["cwgg_krise_typ"], self.g.vars["cwgg_init_brd"], self.g.vars["cwgg_init_ddr"], self.g.pp, self.d.pp)
        self.run_effect("rv_round", self.g)
        self.assertEqual(self.g.vars["cwgg_brd_order_ready"], D(0))
        self.assertEqual((self.g.vars["cwgg_krise_typ"], self.g.vars["cwgg_init_brd"], self.g.vars["cwgg_init_ddr"], self.g.pp, self.d.pp), before)

    def test_countdown_and_war_fallback_never_start_war_for_a_human(self):
        self.g.vars.update(cwgg_countdown=D(1), cwgg_krise_typ=D(10), cwgg_t_path=D(0))
        self.run_effect("rv_countdown_step", self.g)
        self.assertEqual(self.g.vars["cwgg_countdown"], D(0))
        self.assertNotIn("cwgg_german_war", self.m.g.flags)
        self.g.vars["cwgg_t_path"] = D(4)
        notifications_before = len(self.m.events)
        self.run_effect("rv_war_start", self.g)
        self.assertNotIn("cwgg_german_war", self.m.g.flags)
        self.assertEqual(len(self.m.events), notifications_before)
        first_countdown_option = self.m.event_options(EVR + ".211")[0]
        self.assertFalse(any(k in ("declare_war_on", "declare_war") for k, _op, _value in first_countdown_option))

    def test_human_ddr_controls_armistice_and_defer_or_reject_cannot_make_peace(self):
        self.g.wars.add("DDR")
        self.d.wars.add("GER")
        self.m.g.flags.add("cwgg_german_war")
        # Bonn can only send a request; the event is delivered to East Berlin.
        self.m.run_option(EVR + ".31", 1, self.g)
        self.assertIn("cwgg_armistice_request", self.d.flags)
        self.assertEqual(self.m.events[-1][:2], (EVR + ".260", "DDR"))
        self.assertIn("DDR", self.g.wars)
        self.assertIn("GER", self.d.wars)
        accept = self.m.event_options(EVR + ".260")[1]
        self.assertTrue(self.m.condition(first(accept, "trigger", []), self.d))

        # Safe first response keeps the request open, schedules only a review,
        # and leaves the war untouched.
        self.m.run_option(EVR + ".260", 0, self.d)
        self.assertIn("cwgg_armistice_request", self.d.flags)
        self.assertEqual(self.m.events[-1][:2], (EVR + ".260", "DDR"))
        self.assertIn("DDR", self.g.wars)
        self.assertIn("GER", self.d.wars)

        # Decline clears the pending offer without triggering white peace.
        self.m.run_option(EVR + ".260", 2, self.d)
        self.assertNotIn("cwgg_armistice_request", self.d.flags)
        self.assertIn("DDR", self.g.wars)
        self.assertIn("GER", self.d.wars)
        armistice_options = self.m.event_options(EVR + ".260")
        self.assertTrue(self.m.contains_key(armistice_options[1], "white_peace"))
        self.assertFalse(self.m.contains_key(armistice_options[0], "white_peace"))
        self.assertFalse(self.m.contains_key(armistice_options[2], "white_peace"))
        self.assertFalse(self.m.condition(first(armistice_options[1], "trigger", []), self.d))

    def test_unity_execution_without_all_four_consents_cannot_annex_or_complete(self):
        self.g.flags.update(("cwgg_u_rat_brd", "cwgg_u_rat_ddr"))
        self.g.vars.update(cwgg_u_phase=D(4), cwgg_u_ch_1=D(1), cwgg_u_ch_2=D(1), cwgg_u_ch_3=D(1),
                           cwgg_u_ch_4=D(1), cwgg_u_ch_5=D(1), cwgg_fp_sov=D(2), cwgg_fp_usa=D(2),
                           cwgg_fp_eng=D(2), cwgg_fp_fra=D(1))
        self.run_effect("uni_execute", self.g)
        self.assertNotIn(P + "_unity_achieved", self.m.g.flags)
        self.assertIn("DDR", self.m.c)
        self.assertEqual(self.g.vars["cwgg_u_phase"], D(4))

    def test_ddr_unity_proposal_waits_for_bonn_and_starts_once(self):
        self.set_ready_unity()
        self.assertTrue(self.m.condition(self.m.triggers[EAST + "_can_propose_unity"], self.d))
        self.run_effect("east_act_propose_unity", self.d)
        self.assertEqual(self.d.pp, D(400))
        self.assertEqual(self.g.vars["cwgg_init_ddr"], D(3))
        self.assertEqual(self.g.vars["cwgg_u_phase"], D(1))
        self.assertEqual(self.m.events[-1][:2], (EVU + ".2", "GER"))
        self.assertTrue(self.m.condition(self.m.triggers[P + "_uni_pending"], self.g))

        self.m.run_option(EVU + ".2", 1, self.g)
        self.assertEqual(self.g.vars["cwgg_u_phase"], D(2))
        self.assertEqual(self.g.pp, D(525))
        self.assertIn((EVU + ".31", "DDR", {}), self.m.events)
        self.assertEqual(sum(1 for event_id, _scope, _targets in self.m.events if event_id == EVU + ".31"), 1)
        self.run_effect("uni_start", self.g)
        self.assertEqual(self.g.vars["cwgg_u_phase"], D(2))
        self.assertEqual(sum(1 for event_id, _scope, _targets in self.m.events if event_id == EVU + ".31"), 1)

    def test_stale_unity_proposal_and_ratification_cannot_charge_or_advance(self):
        self.set_ready_unity()
        self.g.vars["cwgg_u_phase"] = D(2)
        self.assertFalse(self.m.condition(self.m.triggers[EAST + "_can_propose_unity"], self.d))
        before = (self.d.pp, self.g.vars["cwgg_init_ddr"], self.g.vars["cwgg_u_phase"])
        self.run_effect("east_act_propose_unity", self.d)
        self.assertEqual((self.d.pp, self.g.vars["cwgg_init_ddr"], self.g.vars["cwgg_u_phase"]), before)

        self.g.vars.update(cwgg_u_phase=D(3), cwgg_u_ch_1=D(1), cwger_margin=D(0))
        pp_before = self.g.pp
        self.m.run_option(EVU + ".50", 2, self.g)
        self.assertEqual(self.g.pp, pp_before)
        self.assertNotIn("cwgg_u_rat_brd", self.g.flags)

    def test_signed_war_paths_start_without_ai_sov_substitution(self):
        self.g.vars.update(cwgg_krise_typ=D(1), cwgg_mob_ddr=D(2), cwgg_aufm_ddr=D(1), cwgg_aufm_brd=D(1))
        self.g.flags.add("cwgg_strike_ordered")
        self.run_effect("rv_final_resolution", self.g)
        self.assertIn("cwgg_german_war", self.m.g.flags)
        self.assertIn("cwgg_war_active", self.g.flags)
        self.assertIn("DDR", self.g.wars)
        self.assertIn("GER", self.d.wars)
        self.assertIn((EVR + ".230", "DDR", {}), self.m.events)
        self.assertEqual(self.sov_war_participation(), set())

        self.setUp()
        self.g.vars.update(cwgg_krise_typ=D(1), cwgg_mob_ddr=D(2), cwgg_aufm_ddr=D(1), cwgg_t_path=D(2))
        self.g.vars["cwgg_countdown"] = D(0)
        self.m.c["SOV"].ai = False
        self.d.flags.add("_test_in_faction_SOV")
        self.d.flags.add("cwgg_ddr_countdown_dialogue_open")
        self.assertTrue(self.m.condition(first(self.m.event_options(EVR + ".211")[2], "trigger", []), self.d))
        self.m.run_option(EVR + ".211", 2, self.d)
        self.assertIn("cwgg_german_war", self.m.g.flags)
        self.assertIn("GER", self.d.wars)
        self.assertIn("DDR", self.g.wars)
        self.assertEqual(self.sov_war_participation(), set())
        self.assertIn((EVR + ".230", "DDR", {}), self.m.events)

    def sov_war_participation(self):
        return self.m.c["SOV"].wars


if __name__ == "__main__":
    unittest.main(verbosity=2)

