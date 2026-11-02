# IMPERIA COLD WAR — Chile 1970 domestic politics emitted-script tests.
"""Static parser and contract checks for the pure politics.py output mapping."""
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/vietnam_1970"))
from script_ast import first, parse, values, walk

spec = importlib.util.spec_from_file_location("chile_politics", HERE / "politics.py")
politics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(politics)
OUTPUT = politics.build()


class PoliticsOutputTests(unittest.TestCase):
    def test_generated_scripts_parse_and_markers_are_valid(self):
        for path, text in OUTPUT.items():
            if path.endswith(".yml"):
                self.assertTrue(text.startswith("l_english:\n# IMPERIA COLD WAR —"))
            else:
                self.assertTrue(text.startswith("# IMPERIA COLD WAR —"), path)
                parse(text)

    def test_calendar_wrappers_use_the_approved_windows(self):
        triggers = OUTPUT["common/scripted_triggers/COLDWAR_CHL_1970_politics.txt"]
        effects = OUTPUT["common/scripted_effects/COLDWAR_CHL_1970_politics.txt"]
        self.assertNotIn("COLDWAR_CHL_civilian_government", {k for k, _, _ in parse(triggers)})
        self.assertIn("date > 1969.12.31 date < 1970.9.4", triggers)
        self.assertIn("COLDWAR_CHL_can_event_election = yes", effects)
        self.assertNotIn("date < 1970.1.2", effects)
        self.assertIn("date > 1970.11.2 NOT = { has_country_flag = COLDWAR_CHL_election_installed }", effects)

    def test_ticket_arithmetic_counts_only_the_approved_array_slots_once(self):
        effects = OUTPUT["common/scripted_effects/COLDWAR_CHL_1970_politics.txt"]
        ballot = effects.split("COLDWAR_CHL_election_count = {", 1)[1].split("COLDWAR_CHL_update_congress_support =", 1)[0]
        self.assertIn("COLDWAR_CHL_ticket_1 = party_pop_array^1", ballot)
        self.assertIn("COLDWAR_CHL_ticket_1 = party_pop_array^20", ballot)
        self.assertIn("COLDWAR_CHL_ticket_2 = party_pop_array^2", ballot)
        self.assertIn("COLDWAR_CHL_ticket_2 = party_pop_array^14", ballot)
        for slot in (18, 4, 3, 19):
            self.assertIn(f"COLDWAR_CHL_ticket_18 = party_pop_array^{slot}", ballot)
        self.assertEqual(ballot.count("add_to_temp_variable = { COLDWAR_CHL_ticket_18 ="), 3)
        self.assertNotIn("add_to_variable = { COLDWAR_CHL_ticket_", ballot)

    def test_congress_alternative_requires_native_coalition_majority_and_retries(self):
        triggers = OUTPUT["common/scripted_triggers/COLDWAR_CHL_1970_politics.txt"]
        effects = OUTPUT["common/scripted_effects/COLDWAR_CHL_1970_politics.txt"]
        events = OUTPUT["events/COLDWAR_CHL_1970_politics.txt"]
        self.assertIn("COLDWAR_CHL_congress_runner_up_in_coalition = 1", triggers)
        self.assertIn("COLDWAR_CHL_congress_coalition_support > majority_threshold", triggers)
        self.assertIn("gov_coalition_array", effects)
        self.assertIn("party_pop_elect_array^COLDWAR_CHL_coalition_member", effects)
        self.assertIn("COLDWAR_CHL_congress_coalition_support = party_pop_elect_array^ruling_party", effects)
        self.assertIn("check_variable = { ruling_party = COLDWAR_CHL_election_runner_up_slot }", effects)
        self.assertIn("set_country_flag = { flag = COLDWAR_CHL_congress_retry value = 1 days = 7 }", events)
        self.assertIn("COLDWAR_CHL_congress_alternative_majority = yes", events)

    def test_government_changes_suppress_native_leader_replacement(self):
        effects = OUTPUT["common/scripted_effects/COLDWAR_CHL_1970_politics.txt"]
        self.assertIn("COLDWAR_CHL_apply_government_change = {\nset_country_flag = no_leader_change\nchange_ruling_party_effect = yes\nclr_country_flag = no_leader_change", effects)
        self.assertIn("set_country_flag = no_leader_change\nupdate_set_politics = yes\nclr_country_flag = no_leader_change", effects)
        self.assertIn('ideology = Western_Autocracy', effects)
        self.assertIn('ideology = neutral_Social', effects)

    def test_event_registry_and_portrait_files(self):
        design = politics.SOURCE.read_text(encoding="utf-8")
        events = json.loads(design)["events"]
        emitted = parse(OUTPUT["events/COLDWAR_CHL_1970_politics.txt"])
        records = [row for row in emitted if row[0] == "country_event"]
        self.assertEqual(len(records), len(events))
        for relative in (
            "gfx/leaders/mdcw_historical_pool/CHL_augusto_pinochet.dds",
            "gfx/leaders/mdcw_historical_pool/CHL_patricio_aylwin.dds",
            "gfx/leaders/mdcw_historical_pool/CHL_salvador_allende.dds",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_financial_remedies_preview_and_guard_the_paid_transaction(self):
        text = OUTPUT["common/decisions/COLDWAR_CHL_1970_politics.txt"]
        parsed = parse(text)
        category = first(parsed, "COLDWAR_CHL_civic_remedies")
        decisions = {key: value for key, _, value in category if key != "_bare"}
        public = decisions["COLDWAR_CHL_civilian_bank_restructuring"]
        complete = first(public, "complete_effect")
        preview = first(complete, "effect_tooltip")
        hidden = first(complete, "hidden_effect")
        self.assertTrue(any(k == "modify_treasury_effect" for k, _, _ in walk(preview)))
        self.assertTrue(any(k == "custom_effect_tooltip" and v == "COLDWAR_CHL_weekly_cost_civilian_bank_restructuring" for k, _, v in walk(preview)))
        self.assertTrue(any(k == "idea" and v == "COLDWAR_CHL_restructuring" for k, _, v in walk(preview)))
        self.assertTrue(any(k == "idea" and v == "COLDWAR_CHL_financial_restructuring_funded" for k, _, v in walk(preview)))
        self.assertTrue(any(k == "if" for k, _, _ in walk(hidden)))
        for key in ("COLDWAR_CHL_banking_stress_test", "COLDWAR_CHL_civilian_creditor_losses", "COLDWAR_CHL_full_judicial_settlement"):
            self.assertTrue(any(row[0] == key for row in category), key)
        self.assertIn("days = 365", text)

    def test_weekly_event_cost_previews_use_numeric_md_units(self):
        loc = OUTPUT["localisation/english/COLDWAR_CHL_1970_politics_l_english.yml"]
        self.assertIn("Weekly budget: -$0.05 million per week", loc)
        self.assertIn("Weekly budget: -$0.15 million per week for 365 days", loc)
        events = OUTPUT["events/COLDWAR_CHL_1970_politics.txt"]
        self.assertIn("custom_effect_tooltip = COLDWAR_CHL_weekly_cost_truth_1", events)

    def test_1990_winner_is_counted_from_native_election_array(self):
        effects = OUTPUT["common/scripted_effects/COLDWAR_CHL_1970_politics.txt"]
        events = OUTPUT["events/COLDWAR_CHL_1970_politics.txt"]
        self.assertIn("COLDWAR_CHL_count_1990_election = {", effects)
        self.assertIn("hold_elections = yes", effects)
        self.assertIn("party_pop_elect_array^18", effects)
        self.assertIn("set_country_flag = COLDWAR_CHL_civilian_1990_winner_confirmed", effects)
        self.assertIn("COLDWAR_CHL_install_1990_candidate = yes", events)
        self.assertIn("has_country_flag = COLDWAR_CHL_civilian_1990_winner_confirmed", events)

    def test_all_declared_leader_portraits_exist_and_routes_follow_party(self):
        source = (HERE / "politics.py").read_text(encoding="utf-8")
        for path in re.findall(r'"(gfx/[^\"]+\.dds)"', source):
            self.assertTrue((ROOT / path).is_file(), path)
        self.assertIn("Eduardo Frei Montalva", source)
        self.assertIn("NOT = {{ has_country_flag = {P}election_installed }}", source)
        self.assertIn('"check_variable = { ruling_party = 18 }"', source)
        self.assertIn("has_country_flag = {P}civilian_handover check_variable = {{ ruling_party = 1 }}", source)


if __name__ == "__main__":
    unittest.main()
