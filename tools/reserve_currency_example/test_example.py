# IMPERIA COLD WAR — Executable checks of the inactive example and selected native MD AST.
import hashlib
import json
import re
import unittest
from copy import deepcopy
from decimal import Decimal as D
from pathlib import Path
from integration import HERE, ROOT, PREFIX as P, build, native_effects, budget_hook, month_serial_hook, monthly_preview, walk, script, first
from runtime_model import Model, Country

MEASUREMENTS = {}
LIVE_INPUT_PATHS = tuple(json.loads((HERE / "live_inputs.json").read_text(encoding="utf-8"))["files"])
LIVE_INPUTS_BEFORE_TESTS = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in LIVE_INPUT_PATHS}


def country(model, **overrides):
    values = {
        "debt": "100", "treasury": "20", "gdp_total": "100", "currency_strength": "0.8",
        "interest_rate": "5", "take_debt_amount": "10", "take_debt_cost": "10.1",
        "take_debt_min_gdp": "0", "inflation_rate_var": "0.02", "treasury_rate": "0.1",
        "display_expense": "0.1", "total_subsidies_out": "0.3",
        P + "seed_debt_usd_share": "0.4", P + "seed_reserve_usd_share": "0.8",
        P + "seed_new_usd_share": "0.6",
    }
    values.update(overrides)
    c = Country(variables={k: D(str(v)) for k, v in values.items()})
    c.flags.update({P + "seed_approved": None, P + "clearing_access": None})
    model.run(c, P + "initialize")
    return c


def monthly(model, countries):
    model.execute(countries[0], [month_serial_hook()])
    for c in countries:
        model.run(c, P + "monthly_once")


class ExampleTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        changed = [path for path, digest in LIVE_INPUTS_BEFORE_TESTS.items()
                   if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest]
        if changed:
            raise AssertionError('Example mutated current live economy files: ' + ', '.join(changed))

    def setUp(self):
        self.m = Model()
        self.c = country(self.m)

    def test_initialization_requires_explicit_complete_approved_seed(self):
        for absent in ("receipt", "reserve_share"):
            c = Country(variables=deepcopy(self.c.variables))
            c.variables.pop(P + "seed_reserve_usd_share", None) if absent == "reserve_share" else None
            if absent != "receipt": c.flags[P + "seed_approved"] = None
            self.m.run(c, P + "initialize")
            self.assertNotIn(P + "initialized", c.flags)
        for bad in ("-0.1", "1.1"):
            c = Country(variables=deepcopy(self.c.variables), flags={P + "seed_approved": None})
            c.variables[P + "seed_debt_usd_share"] = D(bad)
            self.m.run(c, P + "initialize")
            self.assertNotIn(P + "initialized", c.flags)

    def test_initialization_and_load_do_not_reseed(self):
        self.c.variables[P + "seed_debt_usd_share"] = D(0)
        self.c.flags[P + "seed_approved"] = None
        self.m.run(self.c, P + "initialize")
        self.assertEqual(self.c.variables[P + "usd_principal"], 40)
        loaded, = self.m.load(self.m.save([self.c]))
        self.m.run(loaded, P + "initialize")
        self.assertEqual(loaded.variables[P + "usd_principal"], 40)

    def test_weighted_fx_does_not_depend_on_reserve_law(self):
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables["debt_fx_factor"], D("1.10"))
        self.c.variables.update({"no_foreign_reserve": D(1), P + "reserve_usd_share": D(0)})
        self.c.ideas.add("french_franc")
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables["debt_fx_factor"], D("1.10"))
        self.assertEqual(self.c.variables[P + "usd_principal"], 40)

    def test_manual_native_borrowing_includes_actual_fee(self):
        self.m.run(self.c, "take_manual_debt_effect")
        self.assertEqual(self.c.variables["treasury"], 30)
        self.assertEqual(self.c.variables["debt"], D("110.1"))
        self.assertEqual(self.c.variables[P + "usd_principal"], D("46.06"))
        self.assertEqual(self.c.refreshes, 1)

    def test_failed_native_borrowing_never_records_exposure(self):
        cases = ("interest", "mission", "gdp")
        for case in cases:
            c = country(self.m)
            if case == "interest": c.variables["interest_rate"] = D(20)
            if case == "mission": c.missions.add("cheap_loan_from_the_imf_mission")
            if case == "gdp": c.variables["take_debt_min_gdp"] = D(100)
            self.m.run(c, "take_manual_debt_effect")
            self.assertEqual(c.variables["debt"], 100)
            self.assertEqual(c.variables[P + "usd_principal"], 40)
            self.assertNotIn(P + "debt_transaction", c.flags)

    def test_automatic_native_borrowing_keeps_its_native_formula(self):
        self.c.variables["treasury"] = D(-2)
        self.m.run(self.c, "automated_debt_taker")
        # Native deficit funding: (2*1.25 + 100*0.01)*1.01 = 3.535 principal.
        self.assertEqual(self.c.variables["debt"], D("103.535"))
        self.assertEqual(self.c.variables[P + "usd_principal"], D("42.121"))
        self.assertEqual(self.c.variables["treasury"], D("1.5"))

    def test_manual_native_repayment_is_proportional(self):
        self.c.variables["repay_debt_amount"] = D(10)
        self.m.run(self.c, "repay_manual_debt_effect")
        self.assertEqual(self.c.variables["debt"], 90)
        self.assertEqual(self.c.variables[P + "usd_principal"], 36)

    def test_native_repayment_is_capped_by_cash_and_debt(self):
        self.c.variables.update({"repay_debt_amount": D(200), "treasury": D(2)})
        self.m.run(self.c, "repay_manual_debt_effect")
        self.assertEqual(self.c.variables["debt"], 98)
        self.assertEqual(self.c.variables["treasury"], 0)
        self.assertEqual(self.c.variables[P + "usd_principal"], D("39.2"))

    def test_native_max_repayment_clears_zero_debt(self):
        self.c.variables.update({"repay_debt_max": D(1), "treasury": D(200)})
        self.m.run(self.c, "repay_manual_debt_effect")
        self.assertEqual(self.c.variables["debt"], 0)
        self.assertEqual(self.c.variables[P + "usd_principal"], 0)
        self.assertEqual(self.c.variables["debt_fx_factor"], 1)

    def test_native_ai_full_and_partial_repayment(self):
        c = country(self.m, treasury="200")
        self.m.run(c, "ai_repay_debt")
        self.assertEqual(c.variables["debt"], 0)
        self.assertEqual(c.variables[P + "usd_principal"], 0)
        c = country(self.m, treasury="10")
        self.m.run(c, "ai_repay_debt")
        self.assertEqual(c.variables["debt"], 92)
        self.assertEqual(c.variables[P + "usd_principal"], D("36.8"))

    def test_native_modify_debt_treats_add_and_clamp_as_one_transaction(self):
        self.m.run(self.c, "modify_debt_effect", {"debt_change": "-200"})
        self.assertEqual(self.c.variables["debt"], 0)
        self.assertEqual(self.c.variables[P + "usd_principal"], 0)
        self.m.run(self.c, "modify_debt_effect", {"debt_change": "10"})
        self.assertEqual(self.c.variables[P + "usd_principal"], 6)

    def test_native_financial_collapse_scales_contract_stocks(self):
        self.c.variables["potential_income"] = D("0.001")
        self.m.run(self.c, "restructure_debt_after_financial_collapse")
        self.assertGreater(self.c.variables["debt"], 0)
        self.assertLess(self.c.variables["debt"], 100)
        self.assertAlmostEqual(self.c.variables[P + "usd_principal"] / self.c.variables["debt"], D("0.4"))
        self.c.variables["potential_income"] = D(0)
        self.m.run(self.c, "restructure_debt_after_financial_collapse")
        self.assertEqual(self.c.variables[P + "usd_principal"], 0)

    def test_commit_is_once_and_freezes_original_contract_share(self):
        self.m.run(self.c, P + "before_debt_change")
        self.c.variables[P + "new_usd_share"] = D("0.2")
        self.c.variables["debt"] += 10
        self.m.run(self.c, P + "after_debt_change")
        self.m.run(self.c, P + "after_debt_change")
        self.assertEqual(self.c.variables[P + "usd_principal"], 46)

    def test_financing_terms_require_receipt_and_change_only_future_borrowing(self):
        self.c.variables[P + "requested_usd_share"] = D("0.2")
        self.m.run(self.c, P + "accept_funding_terms")
        self.assertEqual(self.c.variables[P + "new_usd_share"], D("0.6"))
        self.c.flags[P + "credit_terms_accepted"] = None
        self.m.run(self.c, P + "accept_funding_terms")
        self.assertNotIn(P + "credit_terms_accepted", self.c.flags)
        self.assertEqual(self.c.variables[P + "usd_principal"], 40)
        self.m.run(self.c, "modify_debt_effect", {"debt_change": "10"})
        self.assertEqual(self.c.variables[P + "usd_principal"], 42)

    def test_missing_or_invalid_funding_terms_do_not_change_existing_terms(self):
        for term in (None, "-1", "2"):
            c = country(self.m)
            if term is not None: c.variables[P + "requested_usd_share"] = D(term)
            c.flags[P + "credit_terms_accepted"] = None
            self.m.run(c, P + "accept_funding_terms")
            self.assertEqual(c.variables[P + "new_usd_share"], D("0.6"))

    def test_untracked_change_is_conservative_and_visible_to_audit(self):
        self.c.variables["debt"] += 5
        self.c.variables[P + "new_usd_share"] = D(0)
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables[P + "usd_principal"], 45)
        self.assertIn(P + "untracked_debt_seen", self.c.flags)
        self.c.variables["debt"] = D(21)
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables[P + "usd_principal"], 9)

    def test_round_trip_without_transaction_hooks_is_explicitly_not_detectable(self):
        # Known integration limit: total-debt reconciliation cannot recover hidden gross flows.
        self.c.variables["debt"] -= 10
        self.c.variables["debt"] += 10
        self.m.run(self.c, P + "reconcile_untracked")
        self.assertEqual(self.c.variables[P + "usd_principal"], 40)
        self.assertNotIn(P + "untracked_debt_seen", self.c.flags)

    def test_programme_charges_once_even_after_stale_or_repeated_click(self):
        self.m.run(self.c, P + "begin_diversification")
        self.m.run(self.c, P + "begin_diversification")
        self.assertEqual(self.c.political_power, 125)
        self.assertEqual(self.c.variables["treasury"], D("19.975"))
        self.assertEqual(self.c.variables[P + "months_left"], 24)
        self.assertEqual(self.c.refreshes, 1)

    def test_execution_time_guards_prevent_payment(self):
        for missing in ("pp", "cash", "clearing", "skip"):
            c = country(self.m)
            if missing == "pp": c.political_power = D(74)
            if missing == "cash": c.variables["treasury"] = D("0.024")
            if missing == "clearing": c.flags.pop(P + "clearing_access")
            if missing == "skip": c.flags["MD_skip_treasury_cost"] = None
            before = (c.political_power, c.variables["treasury"])
            self.m.run(c, P + "begin_diversification")
            self.assertEqual((c.political_power, c.variables["treasury"]), before)
            self.assertNotIn(P + "diversification_cooldown", c.flags)

    def test_monthly_receipt_and_derived_refresh_cannot_accelerate_progress(self):
        self.m.run(self.c, P + "begin_diversification")
        monthly(self.m, [self.c])
        expected = self.c.variables[P + "reserve_usd_share"]
        for _ in range(50):
            self.m.run(self.c, P + "monthly_once")
            self.m.run(self.c, P + "refresh_derived")
        self.assertEqual(self.c.variables[P + "months_left"], 23)
        self.assertEqual(self.c.variables[P + "reserve_usd_share"], expected)
        self.assertEqual(self.c.variables["treasury"], D("19.975"))

    def test_24_reviews_reach_exact_target_with_rounding(self):
        m = Model(quantize=True)
        c = country(m)
        m.run(c, P + "begin_diversification")
        for _ in range(24): monthly(m, [c])
        self.assertEqual(c.variables[P + "reserve_usd_share"], D("0.4"))
        self.assertEqual(c.variables[P + "months_left"], 0)
        self.assertEqual(c.variables[P + "weekly_transition_cost"], 0)
        self.assertEqual(c.variables[P + "usd_principal"], 40)
        self.assertEqual(c.variables[P + "new_usd_share"], D("0.6"))
        self.assertEqual(c.variables["reserve_roi_bonus"], D("0.04"))

    def test_agreement_loss_ends_programme_retaining_allocation_and_cooldown(self):
        self.m.run(self.c, P + "begin_diversification")
        monthly(self.m, [self.c])
        allocation = self.c.variables[P + "reserve_usd_share"]
        self.c.flags.pop(P + "clearing_access")
        monthly(self.m, [self.c])
        self.assertEqual(self.c.variables[P + "months_left"], 0)
        self.assertEqual(self.c.variables[P + "reserve_usd_share"], allocation)
        self.assertEqual(self.c.variables[P + "weekly_transition_cost"], 0)
        self.assertTrue(self.m.flag(self.c, P + "diversification_cooldown"))
        self.assertEqual(self.c.variables["treasury"], D("19.975"))

    def test_weekly_budget_hook_is_recalculated_not_charged_per_refresh(self):
        self.m.run(self.c, P + "begin_diversification")
        self.assertEqual(self.c.variables[P + "weekly_transition_cost"], D("0.002"))
        native, _ = native_effects()
        body = native["calculate_additional_expense_rate"]
        # Actual native reset, inserted hook and native subsidies; other native systems are out of scope.
        boundary = body[:1] + budget_hook() + body[1:2]
        for _ in range(3): self.m.execute(self.c, boundary)
        self.assertEqual(self.c.variables["additional_expenses_rate"], D("0.302"))
        self.assertEqual(self.c.variables["treasury"], D("19.975"))

    def test_prospective_weekly_cost_is_clamped_and_visible_before_adoption(self):
        self.assertEqual(self.c.variables[P + "prospective_weekly_cost"], D("0.002"))
        self.assertEqual(self.c.variables[P + "weekly_transition_cost"], 0)
        for gdp, cost in (("0", "0.001"), ("10000", "0.025")):
            self.c.variables["gdp_total"] = D(gdp)
            self.m.run(self.c, P + "calculate_transition_cost")
            self.assertEqual(self.c.variables[P + "prospective_weekly_cost"], D(cost))

    def test_fx_limits_handle_issuer_zero_debt_and_invalid_strength(self):
        for strength, factor in (("0", "1.4"), ("-1", "1.4"), ("4", "0.8")):
            self.c.variables["currency_strength"] = D(strength)
            self.m.run(self.c, "calculate_debt_fx_factor")
            self.assertEqual(self.c.variables["debt_fx_factor"], D(factor))
        self.c.flags["is_usd_issuer"] = None
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables["debt_fx_factor"], 1)
        self.c.variables["debt"] = D(0)
        self.m.run(self.c, "calculate_debt_fx_factor")
        self.assertEqual(self.c.variables[P + "usd_principal"], 0)

    def test_save_load_and_country_processing_order_preserve_state(self):
        a, b = self.c, country(self.m, debt="50", gdp_total="200")
        for c in (a, b): self.m.run(c, P + "begin_diversification")
        for _ in range(7): monthly(self.m, [a, b])
        snap = self.m.save([a, b])
        for _ in range(17): monthly(self.m, [a, b])
        expected = self.m.save([a, b])
        x, y = self.m.load(snap)
        for _ in range(17): monthly(self.m, [y, x])
        self.assertEqual(self.m.save([x, y]), expected)
        self.assertEqual(self.m.temp, {})

    def test_constant_work_without_daily_scans_or_ui_side_effects(self):
        self.m.run(self.c, P + "begin_diversification")
        start = self.m.operations
        monthly(self.m, [self.c])
        MEASUREMENTS["active_month_ast_operations"] = self.m.operations - start
        self.c.variables[P + "months_left"] = D(0)
        start = self.m.operations
        monthly(self.m, [self.c])
        MEASUREMENTS["idle_month_ast_operations"] = self.m.operations - start
        start = self.m.operations
        self.m.run(self.c, P + "monthly_once")
        MEASUREMENTS["repeated_month_ast_operations"] = self.m.operations - start
        self.assertLess(MEASUREMENTS["active_month_ast_operations"], 110)
        self.assertLess(MEASUREMENTS["idle_month_ast_operations"], 90)
        self.assertLess(MEASUREMENTS["repeated_month_ast_operations"], 15)
        effects, _ = build()
        prohibited = {"every_country", "every_state", "every_owned_state", "random", "random_list", "country_event", "ingame_update_setup"}
        for name in ("monthly_once", "refresh_derived", "calculate_transition_cost"):
            self.assertFalse(prohibited.intersection(k for k, _, _ in walk(effects[P + name])))

    def test_native_budget_and_fx_are_routed_once(self):
        effects, _ = build()
        count = sum(k == P + "calculate_transition_cost" for k, _, _ in walk(effects["calculate_additional_expense_rate"]))
        self.assertEqual(count, 1)
        for native, custom in (("calculate_debt_fx_factor", "calculate_debt_fx"), ("calculate_reserve_roi_bonus", "refresh_derived")):
            self.assertEqual(effects[native][0][0], "if")
            self.assertEqual(effects[native][1][0], "else")
            self.assertEqual(sum(k == P + custom for k, _, _ in walk(effects[native])), 1)

    def test_native_monthly_dispatch_has_one_global_serial_and_local_hook(self):
        body = monthly_preview()
        self.assertEqual(sum(k == P + "monthly_once" for k, _, _ in walk(body)), 1)
        self.assertEqual(sum(k == "global." + P + "month_serial" for k, _, _ in walk(body)), 1)
        i = next(i for i, (k, _, _) in enumerate(body) if k == "calculate_currency_strength")
        self.assertEqual(body[i + 1], (P + "monthly_once", "=", "yes"))
        global_block = next(v for k, _, v in body if k == "if" and month_serial_hook() in v)
        self.assertEqual(global_block[0], ("limit", "=", [("NOT", "=", [("has_global_flag", "=", "on_monthly_done")])]))

    def test_recount_uses_existing_scan_and_weights_active_country_once(self):
        self.c.ideas.add("us_dollar")
        self.m.run(self.c, "increment_global_reserve_currency")
        self.assertEqual(self.m.globals["usd_reserve_adoption_count"], D("0.8"))
        legacy = Country(ideas={"us_dollar"})
        self.m.run(legacy, "increment_global_reserve_currency")
        self.assertEqual(self.m.globals["usd_reserve_adoption_count"], D("1.8"))

    def test_encoding_markers_localisation_and_precision(self):
        for path in (HERE / "runtime").rglob("*"):
            if not path.is_file(): continue
            raw = path.read_bytes()
            if path.suffix == ".yml":
                self.assertTrue(raw.startswith(b"\xef\xbb\xbf"), str(path))
            else:
                self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), str(path))
                self.assertTrue(raw.decode("utf-8").startswith("# IMPERIA COLD WAR —"), str(path))
                script(path.relative_to(ROOT))
            self.assertFalse(re.findall(r"(?<![\w.])-?\d+\.\d{6,}(?![\w.])", raw.decode("utf-8-sig")), str(path))
        loc = (HERE / "runtime/localisation/english/COLDWAR_MON_reserves_l_english.yml").read_text(encoding="utf-8-sig")
        self.assertTrue(loc.startswith("l_english:"))
        self.assertIn("COLDWAR_MON_prospective_weekly_cost", loc)

    def test_example_does_not_modify_current_live_economy_files(self):
        # live_inputs.json records the original demonstration's provenance.
        # The example builds from today's providers, so compare before/after
        # this test run instead of rejecting every subsequent economy fix.
        for path, digest in LIVE_INPUTS_BEFORE_TESTS.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest, path)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExampleTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {
        "project": "IMPERIA COLD WAR", "active_in_game": False,
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "measurements": MEASUREMENTS,
        "measurement_scope": "Python AST interpreter instruction counts, not HOI4 timings or OOS evidence",
        "limits": ["Engine save/load and MP/OOS untested", "Uninstrumented net-zero debt flows cannot be recovered", "Agreement provider and complete runtime integration not implemented"],
    }
    (HERE / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)
