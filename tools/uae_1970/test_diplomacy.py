# IMPERIA CW — Cold War: uae 1970 — test diplomacy.
"""Execute the generated diplomacy AST subset, never a second gameplay model.

Native UI, HOI4 loading, economy recalculation and multiplayer delivery remain
outside this harness. Every exercised authored statement is interpreted or
explicitly delegated to a named native/other-module boundary.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/vietnam_1970"))
from script_ast import parse, first

P = "COLDWAR_UAE_"
spec = importlib.util.spec_from_file_location("uae_diplomacy", HERE / "diplomacy.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from revision import current_design
DESIGN = current_design()
OUTPUT = module.build(DESIGN)
E = dict((k, v) for k, _, v in parse(OUTPUT["common/scripted_effects/COLDWAR_UAE_1970_diplomacy.txt"]))
T = dict((k, v) for k, _, v in parse(OUTPUT["common/scripted_triggers/COLDWAR_UAE_1970_diplomacy.txt"]))
EVENTS = {first(v, "id"): v for k, _, v in parse(OUTPUT["events/COLDWAR_UAE_1970_contracts.txt"]) if k == "country_event"}
DECISIONS = {k: v for k, _, v in parse(OUTPUT["common/decisions/COLDWAR_UAE_1970_decisions.txt"])[0][2]}


class World:
    def __init__(self):
        self.tags = ["UAE", "ENG", "BHR", "QAT", "SAU", "KUW", "EGY", "FRA", "PER", "SOV"]
        self.ids = {tag: i + 1 for i, tag in enumerate(self.tags)}
        self.c = {tag: {"v": {"treasury": 10., "gdp_total": .686, P + "start_gdp": .686}, "flags": {}, "ideas": set(), "dynamic": {}, "stock": 5000, "xp": 0, "groups": set(), "wars": set()} for tag in self.tags}
        self.c["UAE"]["groups"] = {"monarchy"}
        self.subject = "ENG"
        self.day = 0
        self.events = []
        self.targets = {}
        self.queue = []
        self.access = set()
        self.delegations = []
        self.states = {179: {"owner": "UAE", "controller": "UAE", "slots": 10, "productivity": 100}, 180: {"owner": "UAE", "controller": "UAE", "slots": 0, "productivity": 100}}
        self.global_v = {"mdcw_cw_oil_ratio": 1.0, "mdcw_cw_oil_level": 1.0}

    def has(self, tag, name):
        expiry = self.c[tag]["flags"].get(name, -1)
        return expiry is None or expiry > self.day

    def scope(self, name, current, root, prev):
        if name == "ROOT": return root
        if name == "PREV": return prev
        if name == "THIS": return current
        if name.startswith("event_target:"): return self.targets.get(name.split(":", 1)[1])
        if name.startswith("var:"):
            ident = self.num(name[4:], current, root, prev)
            return next((tag for tag, i in self.ids.items() if i == ident), None)
        return name if name in self.c else None

    def num(self, value, current, root, prev):
        try: return float(value)
        except (ValueError, TypeError): pass
        if value == "global.date": return self.day * .024
        if str(value).startswith("global."): return self.global_v.get(value[7:], 0)
        if "." in str(value):
            scope, name = value.split(".", 1)
            tag = self.scope(scope, current, root, prev)
            if name == "id": return self.ids[tag]
            return self.c[tag]["v"].get(name, 0)
        return self.c[current]["v"].get(value, 0)

    def test(self, rows, current="UAE", root=None, prev=None, state=None):
        root = root or current
        return all(self.cond(k, o, v, current, root, prev, state) for k, o, v in rows)

    def cond(self, k, op, v, c, root, prev, state):
        if k in {"AND", "limit", "hidden_trigger"}: return self.test(v, c, root, prev, state)
        if k == "OR": return any(self.cond(a, o, x, c, root, prev, state) for a, o, x in v)
        if k == "NOT": return not self.test(v, c, root, prev, state)
        if k in T: return self.test(T[k], c, root, prev, state) == (v == "yes")
        if k.startswith(P) and k.endswith("_government"): return k[len(P):-len("_government")] in self.c[c]["groups"]
        scoped = self.scope(k, c, root, prev)
        if scoped: return self.test(v, scoped, root, c, state)
        if k.isdigit(): return self.test(v, c, root, prev, int(k))
        if k == "tag": return c == v
        if k in {"always", "exists", "IMP_is_1970_scenario"}: return v == "yes"
        if k == "country_exists": return v in self.c
        if k == "has_country_flag": return self.has(c, v)
        if k == "has_global_flag": return False
        if k == "has_variable": return (v[7:] in self.global_v) if v.startswith("global.") else v in self.c[c]["v"]
        if k == "has_idea": return v in self.c[c]["ideas"]
        if k == "is_subject_of": return c == "UAE" and self.subject == v
        if k == "is_subject": return (c == "UAE" and self.subject is not None) == (v == "yes")
        if k == "has_war": return bool(self.c[c]["wars"]) == (v == "yes")
        if k == "has_war_with": return v in self.c[c]["wars"]
        if k == "has_equipment": return self.c[c]["stock"] > float(v[0][2])
        if k == "mdcw_cw_is_opec_member": return c == "UAE"
        if k == "date":
            today = dt.date(1970, 1, 1) + dt.timedelta(days=self.day)
            target = dt.date(*map(int, v.split(".")))
            return {"<": today < target, ">": today > target, "=": today == target}[op]
        if k in {"is_owned_by", "is_controlled_by"}:
            field = "owner" if k == "is_owned_by" else "controller"
            return self.states[state][field] == self.scope(v, c, root, prev)
        if k == "free_building_slots": return self.states[state]["slots"] > 0
        if k == "check_variable":
            if first(v, "var"):
                left, right, cmp = self.num(first(v, "var"), c, root, prev), self.num(first(v, "value"), c, root, prev), first(v, "compare", "equals")
            else:
                name, cmp, val = v[0]
                left, right = self.num(name, c, root, prev), self.num(val, c, root, prev)
            return {"greater_than_or_equals": left >= right, "less_than_or_equals": left <= right, "greater_than": left > right, "less_than": left < right, "equals": left == right, "<": left < right, ">": left > right, "=": left == right}[cmp]
        raise AssertionError("Unmodelled authored trigger " + k)

    def execute(self, rows, current="UAE", root=None, prev=None, state=None):
        root = root or current
        branch = False
        for k, op, v in rows:
            if k == "if":
                branch = self.test(first(v, "limit", []), current, root, prev, state)
                if branch: self.execute([r for r in v if r[0] != "limit"], current, root, prev, state)
                continue
            if k == "else":
                if not branch: self.execute(v, current, root, prev, state)
                branch = False
                continue
            if k == "hidden_effect": self.execute(v, current, root, prev, state); continue
            if k in E: self.execute(E[k], current, root, prev, state); continue
            scoped = self.scope(k, current, root, prev)
            if scoped: self.execute(v, scoped, root, current, state); continue
            if k.isdigit(): self.execute(v, current, root, prev, int(k)); continue
            cv = self.c[current]["v"]
            if k in {"set_variable", "set_temp_variable", "add_to_variable", "subtract_from_variable", "multiply_variable", "multiply_temp_variable"}:
                name, _, value = v[0]
                operand = self.num(value, current, root, prev)
                if k in {"set_variable", "set_temp_variable"}: cv[name] = operand
                elif k == "add_to_variable": cv[name] = cv.get(name, 0) + operand
                elif k == "subtract_from_variable": cv[name] = cv.get(name, 0) - operand
                else: cv[name] = cv.get(name, 0) * operand
            elif k == "set_country_flag":
                name = first(v, "flag") if isinstance(v, list) else v
                self.c[current]["flags"][name] = self.day + int(first(v, "days")) if isinstance(v, list) else None
            elif k == "clr_country_flag": self.c[current]["flags"].pop(v, None)
            elif k == "save_event_target_as": self.targets[v] = current
            elif k == "modify_treasury_effect": cv["treasury"] += cv["treasury_change"]
            elif k == "country_event": self.events.append((first(v, "id"), current))
            elif k == "add_ideas": self.c[current]["ideas"].add(v)
            elif k == "remove_ideas": self.c[current]["ideas"].discard(v)
            elif k == "add_dynamic_modifier": self.c[current]["dynamic"][first(v, "modifier")] = int(first(v, "days", 0))
            elif k == "remove_dynamic_modifier": self.c[current]["dynamic"].pop(first(v, "modifier"), None)
            elif k == "end_puppet":
                assert current == "ENG" and v == "UAE" and self.subject == "ENG"
                self.subject = None
            elif k == "army_experience": self.c[current]["xp"] += float(v)
            elif k == "flat_productivity_change_effect":
                for s in self.states.values():
                    if s["controller"] == current: s["productivity"] += cv["temp_productivity_change"]
            elif k == "add_building_construction":
                self.queue.append((state, first(v, "province"), first(v, "type"), int(first(v, "level"))))
                self.states[state]["slots"] -= int(first(v, "level"))
            elif k == "send_equipment":
                n = int(first(v, "amount")); target = first(v, "target")
                assert self.c[current]["stock"] >= n
                self.c[current]["stock"] -= n; self.c[target]["stock"] += n
            elif k == "give_military_access": self.access.add((current, v))
            elif k == "mdcw_cw_start_opec_vote": self.delegations.append((k, cv["mdcw_cw_t_vote_type"]))
            elif k == P + "organise_association": self.c[current]["flags"][P + "islah_organised"] = None
            elif k in {P + "convene_constitution", P + "accept_cabinet_bargain"}: self.delegations.append((k, current))
            elif k in {"effect_tooltip", "custom_effect_tooltip", "ingame_update_setup", P + "refresh_programmes"}:
                pass  # Explicit UI/native-economy/other-module boundaries.
            else: raise AssertionError("Unmodelled authored effect " + k)

    def call(self, key, country="UAE"):
        self.execute(E[P + key], country)

    def earn(self, *suffixes):
        for suffix in suffixes: self.c["UAE"]["flags"][P + "done_" + suffix] = None

    def click(self, key, partner=None):
        if partner: self.targets["COLDWAR_UAE_contract_recipient"] = partner
        self.execute(first(DECISIONS[P + "decision_" + key], "complete_effect"), "ENG" if key == "british_withdrawal_policy" else "UAE")

    def finish(self, key): self.execute(first(DECISIONS[P + "decision_" + key], "remove_effect"))

    def choose(self, event_id=None, country=None, option=0):
        if event_id is None: event_id, country = self.events[-1]
        opts = [v for k, _, v in EVENTS[event_id] if k == "option"]
        self.execute([r for r in opts[option] if r[0] not in {"name", "trigger", "ai_chance"}], country)


def run():
    from copy import deepcopy
    from focus_delivery import OFFER_TARGETS, focus_action
    cases = []
    def passed(message): cases.append(message)
    def near(a, b): assert abs(a - b) < 1e-9, (a, b)

    w = World(); w.call("init_british"); w.call("init_british")
    assert w.c["UAE"]["v"][P + "treaty_nonce"] == 1
    assert P + "treaty_dependence" in w.c["UAE"]["ideas"]
    w.day = (dt.date(1971, 12, 1) - dt.date(1970, 1, 1)).days
    w.call("british_tick"); w.call("british_tick")
    assert w.subject is None and P + "withdrawal_fulfilled" in w.c["UAE"]["ideas"]
    near(w.c["UAE"]["v"]["treasury"], 10)
    passed("Historical withdrawal remains focus-free, consent-free and money-free, once")

    w = World(); w.call("init_british"); w.earn("renew_protection")
    w.call("send_protection_offer"); old = w.events[-1]
    w.call("close_protection_offer"); w.day = 181; w.call("send_protection_offer"); new = w.events[-1]
    w.choose(*old); assert not w.has("UAE", P + "protection_accepted")
    w.choose(*new); assert w.has("UAE", P + "protection_accepted")
    passed("Old British rounds cannot accept newer proposals")

    w = World(); w.call("init_british"); w.earn("renew_protection"); w.call("send_protection_offer"); old = w.events[-1]
    w.day = 700; w.choose(*old); w.call("british_tick")
    assert w.subject is None and not w.has("UAE", P + "protection_accepted")
    passed("Late protection cannot postpone historical release")

    w = World(); w.call("init_british"); w.call("accept_protection"); w.earn("enduring_protection")
    w.call("focus_british_cofinance"); offer = w.events[-1]
    w.c["ENG"]["v"]["treasury"] = .249; w.choose(*offer); near(w.c["UAE"]["v"]["treasury"], 10)
    w.c["ENG"]["v"]["treasury"] = .25; w.choose(*offer); w.choose(*offer)
    near(w.c["ENG"]["v"]["treasury"], 0); near(w.c["UAE"]["v"]["treasury"], 10.25)
    count = len(w.events); w.call("focus_british_cofinance"); assert len(w.events) == count
    passed("Focus cofinance requires UK funds/consent and transfers exactly250m once")

    w = World(); w.subject = None; w.earn("technical_exchange")
    w.call("focus_exchange_offer"); offer = w.events[-1]
    assert offer[1] == "SOV"
    price = w.c["UAE"]["v"][P + "offer_price_exchange_offer"]
    w.c["UAE"]["v"]["gdp_total"] = 100
    w.c["UAE"]["v"]["treasury"] = price - .001; w.choose(*offer)
    assert w.states[179]["productivity"] == 100
    w.c["UAE"]["v"]["treasury"] = price; w.choose(*offer); w.choose(*offer)
    near(w.c["UAE"]["v"]["treasury"], 0); assert w.states[179]["productivity"] == 110
    assert w.has("SOV", P + "offer_cooldown_exchange_offer")
    passed("Across the Blocs targets SOV, freezes the real invoice, and gives productivity only after consent/payment")

    w = World(); w.earn("air_coastal_shield"); w.call("focus_procurement")
    seller = w.events[-1]; assert seller[1] == "ENG"; w.choose(*seller); quote = w.events[-1]
    near(w.c["UAE"]["v"]["treasury"], 10); assert w.c["UAE"]["stock"] == 5000
    w.c["ENG"]["stock"] = 999; w.choose(*quote); assert w.c["UAE"]["stock"] == 5000
    w.c["ENG"]["stock"] = 1000; w.c["UAE"]["v"]["treasury"] = .25
    w.choose(*quote); w.choose(*quote)
    near(w.c["UAE"]["v"]["treasury"], 0); near(w.c["ENG"]["v"]["treasury"], 10.25)
    assert w.c["UAE"]["stock"] == 6000 and w.c["ENG"]["stock"] == 0
    passed("Focus procurement quotes British existing Rifle Squad stock, then buyer confirms one atomic250m transfer")

    w = World(); w.earn("air_coastal_shield"); w.targets["COLDWAR_UAE_contract_recipient"] = "FRA"
    w.call("send_procurement_offer"); w.choose(); old = w.events[-1]
    w.day = 61; w.call("british_tick"); w.day = 242
    w.call("send_procurement_offer"); w.choose(); current = w.events[-1]
    w.choose(*old, option=1)
    assert w.has("UAE", P + "offer_pending_procurement")
    w.choose(*current); assert w.c["UAE"]["stock"] == 6000
    passed("An old buyer decline cannot close a newer quotation; legacy foreign seller quotes remain valid")

    w = World(); w.earn("adia_savings"); w.click("reserve_deposit")
    near(w.c["UAE"]["v"]["treasury"], 10)
    w.finish("reserve_deposit"); w.finish("reserve_deposit")
    near(w.c["UAE"]["v"][P + "reserve_principal"], .0343)
    near(w.c["UAE"]["v"]["treasury"], 9.9657)
    w.click("reserve_withdraw"); w.click("reserve_withdraw")
    assert not w.events; near(w.c["UAE"]["v"][P + "reserve_principal"], 0)
    near(w.c["UAE"]["v"]["treasury"], 10)
    passed("The explicit reserve exception conserves principal: one paid deposit, direct once-only withdrawal, no interest or popup")

    w = World(); w.earn("oil_institutions"); w.click("oil_restraint")
    assert w.delegations[-1] == ("mdcw_cw_start_opec_vote", 3)
    passed("The explicit OPEC decision delegates the existing native export-restraint vote")

    w = World(); w.earn("gulf_diplomacy", "kuwait_support", "kuwait_transit", "kuwait_deployment")
    w.c["KUW"]["wars"] = {"SAU"}
    w.call("focus_kuwait_transit"); w.choose(); assert ("UAE", "KUW") in w.access
    w.call("focus_kuwait_deployment"); w.choose(); assert ("KUW", "UAE") in w.access
    w.call("focus_kuwait_support"); w.choose()
    near(w.c["UAE"]["v"]["treasury"], 10 - .686 * .03)
    near(w.c["KUW"]["v"]["treasury"], 10 + .686 * .03)
    assert not w.c["UAE"]["wars"] and w.c["UAE"]["stock"] == 5000
    passed("Individual Kuwait focuses deliver consent-based aid/access without a decision menu, free units or automatic war entry")

    for accept in [False, True]:
        w = World(); w.call("init_british"); w.earn("renew_protection"); w.call("send_protection_offer")
        w.choose(option=1); counter = w.events[-1]
        assert w.subject == "ENG" and not w.has("UAE", P + "friendship_accepted")
        w.choose(*counter, option=0 if accept else 1)
        if accept:
            assert w.subject is None and w.has("UAE", P + "friendship_accepted")
            nonce = w.c["UAE"]["v"][P + "treaty_nonce"]; w.choose(*counter)
            assert w.c["UAE"]["v"][P + "treaty_nonce"] == nonce
        else:
            assert w.subject == "ENG" and w.has("UAE", P + "historical_withdrawal_schedule")
    passed("Real British counterproposal needs current UAE confirmation; refusal preserves historical withdrawal")

    prerequisites = {
        "bahrain": "nine_states", "qatar": "nine_states", "arab_exchange": "arab_solidarity",
        "participation": "state_participation", "training_offer": "security_contracts",
        "exchange_offer": "technical_exchange", "procurement": "air_coastal_shield",
        "british_cofinance": "enduring_protection", "kuwait_support": "kuwait_support",
        "kuwait_transit": "kuwait_transit", "kuwait_deployment": "kuwait_deployment",
    }
    for key, target in OFFER_TARGETS.items():
        unauthorized = World(); unauthorized.call('focus_' + key)
        assert not unauthorized.events and not unauthorized.has('UAE', P + 'focus_offer_requested_' + key), key
        w = World(); w.call("init_british"); w.earn(prerequisites[key]); w.c["KUW"]["wars"] = {"SAU"}
        if key == "arab_exchange": w.c["UAE"]["groups"] = {"arab"}
        if key == "british_cofinance": w.call("accept_protection")
        before = deepcopy((w.c, w.events, w.targets))
        w.call("focus_preview_" + key)
        assert (w.c, w.events, w.targets) == before, key
        w.c["UAE"]["v"]["treasury"] = 0
        w.call("focus_" + key); assert w.events[-1][1] == target, key
        count = len(w.events); w.call("focus_" + key); w.call("british_tick")
        assert len(w.events) == count, key
        near(w.c["UAE"]["v"]["treasury"], 0)
    passed("All11 focus offer providers bind fixed partners, preview without side effects, dispatch at zero treasury, charge no PP/cash and never replay")

    w = World(); w.earn("technical_exchange"); partner = w.c.pop("SOV")
    w.call("focus_exchange_offer"); assert not w.events and w.has("UAE", P + "focus_offer_requested_exchange_offer")
    w.call("british_tick"); assert not w.events
    w.c["SOV"] = partner; w.call("british_tick")
    assert w.events[-1][1] == "SOV"
    count = len(w.events); w.call("british_tick"); assert len(w.events) == count
    passed("Only a newly focus-requested offer waits for a missing partner and dispatches once when valid")

    w = World(); w.earn("technical_exchange", "security_contracts", "air_coastal_shield")
    w.c["UAE"]["flags"][P + "course_running_housing"] = None
    w.call("british_tick"); w.call("british_tick")
    assert not w.events and not w.has("UAE", P + "course_running_housing")
    near(w.c["UAE"]["v"]["treasury"], 10); assert not w.c["UAE"]["dynamic"]
    passed("Old completed focuses do not backfill foreign offers; retired domestic courses become inert without late payment/reward")

    w = World(); w.earn("technical_exchange")
    w.c["UAE"]["v"][P + "offer_round_exchange_offer"] = 3
    w.call("focus_exchange_offer"); assert not w.events
    assert w.has("UAE", P + "focus_offer_delivered_exchange_offer")
    assert w.test(T[P + "focus_partner_exchange_offer_available"])
    passed("A legacy already-issued negotiation satisfies the permanent focus without a new invoice or reoffer")

    assert set(DECISIONS) == {P + "decision_" + name for name in ["reserve_deposit", "reserve_withdraw", "oil_restraint"]}
    assert len(DESIGN["decisions"]) == 3
    first_ids = [1001,3001,4001,5001,6001,7001,8001,9001,10001,11001,15001,19001,20001,70001,90001]
    assert set(EVENTS) == {module.NS + "." + str(base + r) for base in first_ids for r in range(module.ROUNDS)}
    assert len(EVENTS) == 1920
    assert 'contract_housing' not in OUTPUT['common/dynamic_modifiers/COLDWAR_UAE_1970_contracts.txt']
    assert 'contract_scholarships' not in OUTPUT['common/dynamic_modifiers/COLDWAR_UAE_1970_contracts.txt']
    assert focus_action('technical_exchange') == P + 'focus_exchange_offer = yes'
    passed("Exactly3 approved decisions and15 real foreign-consent templates remain; immutable IDs preserved and no duplicate domestic timed programme")

    report = {"passed": len(cases), "cases": cases, "errors": [], "generated_event_count": len(EVENTS),
              "limits": "Generated AST subset only; native UI, HOI4 load/save, economy formulas, other-module politics and multiplayer delivery are not emulated."}
    (HERE / "diplomacy_runtime_validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    run()
