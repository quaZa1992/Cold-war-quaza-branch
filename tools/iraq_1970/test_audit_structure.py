# IMPERIA CW — Cold War: iraq 1970 — test audit structure.
"""Independent read-only checks of the assembled audit revision.

No generator or loaded output is written. Failing endpoint checks identify
unfinished audit promises, rather than authorising this test to repair design.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import unittest

import audit_design

P = "COLDWAR_IRQ_"
POLITICAL_ENDPOINTS = [
    "state_compact", "baath_future", "bakr_succession_plan", "saddam_legacy",
    "officer_settlement", "arab_republic_endures", "icp_socialist_republic",
    "aziz_party_renewal", "civic_mandate", "royal_settlement",
    "kdp_common_republic", "puk_federal_mandate", "dawa_government_review",
    "sciri_iraqi_mandate", "iip_government_mandate",
]


def shape_clusters(data):
    nodes = {n["id"]: n for n in data["nodes"] if not n.get("audit_retired")}
    @lru_cache(None)
    def signature(fid):
        n = nodes[fid]
        # Preserve native AND/OR groups, mutuality and depth, discard labels,
        # positions, chronology and mechanically irrelevant focus-ID spelling.
        grammar = (bool(n["mutually_exclusive"]), tuple(sorted(tuple(sorted(signature(p) for p in group)) for group in n["prerequisites"])))
        return hashlib.sha256(repr(grammar).encode()).hexdigest()
    clusters = defaultdict(list)
    for group in data["groups"]:
        grammar = sorted(signature(n["id"]) for n in nodes.values() if n["group"] == group["id"])
        clusters[hashlib.sha256(repr(grammar).encode()).hexdigest()].append(group["id"])
    return sorted(clusters.values(), key=lambda x: (-len(x), x))


class AuditStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = audit_design.load_design()
        cls.baseline = audit_design.baseline()
        cls.old = {n["id"]: n for n in cls.baseline["nodes"]}
        cls.nodes = {n["id"]: n for n in cls.data["nodes"]}
        cls.active = {k: n for k, n in cls.nodes.items() if not n.get("audit_retired")}

    def test_every_original_id_retained(self):
        self.assertEqual(set(self.nodes), set(self.old))
        self.assertEqual(len(self.nodes), 426)
        self.assertTrue(all(k in self.nodes for k in self.data["retired_focuses"].values()))

    def test_active_references_and_mutuality(self):
        for nid, n in self.active.items():
            for group in n["prerequisites"]:
                self.assertTrue(group, nid)
                self.assertEqual(len(group), len(set(group)), nid)
                self.assertNotIn(nid, group)
                self.assertTrue(all(p in self.active for p in group), (nid, group))
            for opposite in n["mutually_exclusive"]:
                self.assertIn(opposite, self.active)
                self.assertIn(nid, self.active[opposite]["mutually_exclusive"])

    def test_no_focus_cycles(self):
        done = set()
        visiting = set()
        def visit(fid):
            self.assertNotIn(fid, visiting, "Focus cycle at " + fid)
            if fid in done:
                return
            visiting.add(fid)
            for group in self.active[fid]["prerequisites"]:
                for parent in group:
                    visit(parent)
            visiting.remove(fid)
            done.add(fid)
        for fid in self.active:
            visit(fid)

    def test_every_active_focus_has_a_mutually_compatible_graph_route(self):
        pairs = {frozenset((fid, opposite)) for fid, n in self.active.items() for opposite in n["mutually_exclusive"]}
        @lru_cache(None)
        def routes(fid):
            n = self.active[fid]
            got = {frozenset()}
            for group in n["prerequisites"]:
                options = set().union(*(routes(p) for p in group))
                got = {a | b for a in got for b in options}
                got = {r for r in got if not any(pair <= r for pair in pairs)}
            if n["mutually_exclusive"]:
                got = {r | {fid} for r in got}
            return frozenset(r for r in got if not any(pair <= r for pair in pairs))
        dead = [fid for fid in self.active if not routes(fid)]
        self.assertEqual(dead, [])

    def test_native_grid_has_no_collisions_or_non_descending_edges(self):
        positions = defaultdict(list)
        for nid, n in self.active.items():
            positions[tuple(n["xy"])].append(nid)
            for group in n["prerequisites"]:
                for parent in group:
                    self.assertLess(self.active[parent]["xy"][1], n["xy"][1], (parent, nid))
        self.assertEqual({xy: ids for xy, ids in positions.items() if len(ids) > 1}, {})

    def test_native_relative_anchors_resolve_exactly(self):
        for g in self.data["groups"]:
            self.assertIn(g["anchor"], self.active)
        for nid, n in self.active.items():
            if n["anchor"]:
                a = self.active[n["anchor"]]
                resolved = [a["xy"][i] + n["offset"][i] for i in [0, 1]]
            else:
                resolved = n["offset"]
            self.assertEqual(n["xy"], resolved, nid)

    def test_retired_entries_have_no_rewards_or_research(self):
        for fid in self.data["retired_focuses"]:
            n = self.nodes[fid]
            self.assertTrue(n["audit_retired"])
            self.assertEqual(n["modifiers"], {})
            self.assertEqual(n["army_xp"], 0)
            self.assertEqual(n["instant"], [])
            self.assertIsNone(n["building"])
            self.assertEqual(n["budget_gdp_share"], 0)
            self.assertEqual(n["decisions"], [])
            self.assertEqual(n["prerequisites"], [])

    def test_entry_splicing_never_requires_the_opposite_choice(self):
        for key in ["industry_heavy", "industry_light", "defence_professional", "defence_mass"]:
            self.assertEqual(self.active[P + key]["prerequisites"], [], key)
        retired = set(self.data["retired_focuses"])
        self.assertFalse(any(parent in retired for n in self.active.values() for group in n["prerequisites"] for parent in group))

    def test_exact_oil_reordering_and_real_delivery_parents(self):
        training = self.active[P + "oil_technical_training"]
        self.assertEqual(training["prerequisites"], [[P + "oil_state_company", P + "oil_concession_delivery"]])
        self.assertEqual(training["xy"], [45, 18])
        self.assertEqual(self.active[P + "oil_state_company"]["xy"], [42, 17])
        self.assertEqual(self.active[P + "oil_concession_delivery"]["xy"], [48, 17])
        self.assertEqual(self.active[P + "oil_sovereignty"]["xy"], [45, 23])

    def test_war_support_unlocks_are_on_the_common_plan(self):
        plan = self.active[P + "iran_operational_plan"]
        decisions = {d["id"] for d in plan["decisions"]}
        self.assertIn(P + "decision_iran_gulf_credit", decisions)
        self.assertIn(P + "decision_iran_supplier", decisions)
        self.assertEqual(self.active[P + "iran_tehran_assessment"]["prerequisites"], [[P + "iran_frontier"]])
        # No invented limited-war wargoal is certified by this graph test.

    def test_political_endpoints_have_their_own_binding_reform(self):
        unfinished = []
        for key in POLITICAL_ENDPOINTS:
            n = self.active[P + key]
            old = self.old[n["id"]]
            unchanged_three_way_stamp = n["prerequisites"] == old["prerequisites"] and len(n["prerequisites"]) == 1 and len(n["prerequisites"][0]) >= 3
            no_added_contract = n.get("requires", []) == old.get("requires", [])
            if unchanged_three_way_stamp and no_added_contract:
                unfinished.append(key)
        self.assertEqual(unfinished, [], "Still an unchanged broad OR finale: " + ", ".join(unfinished))

    def test_common_finales_remain_reachable_from_each_policy_combination(self):
        from itertools import product
        problems = []
        for key in POLITICAL_ENDPOINTS + ["agri_reform_delivery", "oil_sovereignty", "defence_readiness", "war_peace_dividend"]:
            final = self.active[P + key]
            group = final["group"]
            members = {fid: n for fid, n in self.active.items() if n["group"] == group}
            pairs = sorted({tuple(sorted((fid, opposite))) for fid, n in members.items() for opposite in n["mutually_exclusive"]})
            @lru_cache(None)
            def routes(fid):
                n = self.active[fid]
                got = {frozenset()}
                for prerequisites in n["prerequisites"]:
                    options = set().union(*(routes(p) for p in prerequisites))
                    got = {a | b for a in got for b in options}
                if n["mutually_exclusive"]:
                    got = {r | {fid} for r in got}
                return frozenset(r for r in got if not any(set(pair) <= r for pair in pairs))
            choices = product(*pairs) if pairs else [()]
            for choice in choices:
                chosen = frozenset(choice)
                # Only counterfactual policies that themselves have compatible
                # routes are meaningful. Foreign/date/contract gates are beyond
                # this structural SAT check and reviewed separately.
                if not all(any(not any(set(pair) <= (route | chosen) for pair in pairs) for route in routes(fid)) for fid in chosen):
                    continue
                if not any(not any(set(pair) <= (route | chosen) for pair in pairs) for route in routes(final["id"])):
                    problems.append((key, tuple(fid.removeprefix(P) for fid in chosen)))
        self.assertEqual(problems, [], "Common finale strands an alternative policy: " + repr(problems))

    def test_twelve_fold_skeleton_is_reduced(self):
        before = shape_clusters(self.baseline)
        after = shape_clusters(self.data)
        self.assertLess(len(after[0]), len(before[0]), (before[0], after[0]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
