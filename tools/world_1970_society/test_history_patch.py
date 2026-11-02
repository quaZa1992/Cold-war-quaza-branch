# IMPERIA COLD WAR — Verify bounded history edits, bookmark isolation and replay behavior.
from pathlib import Path
import hashlib
import json
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/spain_1970_v2"))
from script_ast import parse, first
from history_patch import patched, strip_profile, date_blocks, BEGIN, END

EXAMPLE = {"currency": "us_dollar", "religion": "christian", "factions": ["the_military", "farmers", "small_medium_business_owners"], "no_foreign_reserve": 0, "remove_ideas": ["sunni", "euro"]}

# IMPERIA COLD WAR — Read native hook bodies so defensive tests exercise their resets.
NATIVE_FACTIONS = {
    k: v for k, _, v in first(first(parse((ROOT / "common/ideas/AA_law_internal_factions.txt").read_text(encoding="utf-8")), "ideas"), "internal_factions")
    if isinstance(v, list)
}
NATIVE_CLEANUP = first(parse((ROOT / "common/scripted_effects/00_internal_faction_effects.txt").read_text(encoding="utf-8")), "if_no_longer_has_faction_clear_previous")


def run_profile(rows, start_year, ideas=None, variables=None, native_on_add=False, stats=None, country_exists=True):
    """Evaluate the bounded profile, optionally executing actual native faction on_add.

    Quiet history remains the default. The defensive mode covers native on_add
    reset/cleanup behavior without pretending to emulate the whole game engine.
    """
    ideas, variables = set(ideas or []), dict(variables or {})
    temporary = {}
    stats = {} if stats is None else stats
    for name in ("adds", "removes", "on_add", "cleared", "native_refreshes", "profile_refreshes"):
        stats.setdefault(name, [])
    stats.setdefault("native_full_refreshes", 0)
    def value(raw):
        if isinstance(raw, list):
            answer = 0
            for k, _, v in raw:
                if k == "value": answer = value(v)
                elif k == "add": answer += value(v)
                elif k == "clamp":
                    answer = min(max(answer, value(first(v, "min"))), value(first(v, "max")))
                else: raise AssertionError("Unsupported native inline value: " + k)
            return answer
        if raw.startswith("modifier@"):
            return 0  # No scenario-specific minimum-opinion modifier in these fixtures.
        try: return int(raw)
        except ValueError:
            try: return float(raw)
            except ValueError: return temporary.get(raw, variables.get(raw, 0))
    def check(items):
        answers = []
        for k, _, v in items:
            if k == "IMP_is_1970_scenario": answers.append((start_year == 1970) == (v == "yes"))
            elif k == "NOT": answers.append(not check(v))
            elif k == "has_variable": answers.append(v in variables)
            elif k == "has_idea": answers.append(v in ideas)
            elif k == "exists": answers.append(country_exists == (v == "yes"))
            elif k == "check_variable":
                name, comparison, target = v[0]
                if comparison == ">": answers.append(value(name) > value(target))
                else: raise AssertionError("Unsupported profile variable comparison: " + comparison)
            else: raise AssertionError("Unsupported profile condition: " + k)
        return all(answers)
    def execute(items, native=False):
        for k, _, v in items:
            if k == "if":
                if check(first(v, "limit", [])): execute([row for row in v if row[0] != "limit"], native)
            elif k == "hidden_effect": execute(v, native)
            elif k == "set_variable":
                name, _, raw = v[0]
                variables[name] = value(raw)
            elif k == "set_temp_variable":
                name, _, raw = v[0]
                temporary[name] = value(raw)
            elif k == "clear_variable":
                if v in variables: stats["cleared"].append(v)
                variables.pop(v, None)
            elif k in ("add_ideas", "remove_ideas"):
                members = [row[2] for row in v] if isinstance(v, list) else [v]
                for member in members:
                    if k == "add_ideas":
                        stats["adds"].append(member)
                        ideas.add(member)
                        if native_on_add and member in NATIVE_FACTIONS:
                            stats["on_add"].append(member)
                            execute(first(NATIVE_FACTIONS[member], "on_add", []), True)
                    else:
                        stats["removes"].append(member)
                        ideas.discard(member)
            elif k == "if_no_longer_has_faction_clear_previous": execute(NATIVE_CLEANUP, True)
            elif k == "initialize_internal_faction_dynamic_modifiers":
                stats["native_refreshes" if native else "profile_refreshes"].append(
                    {name: val for name, val in variables.items() if name.endswith("_opinion")}
                )
            elif k == "ingame_update_setup":
                if not native: raise AssertionError("Profile must not invoke a full economy refresh")
                stats["native_full_refreshes"] += 1
            elif k in ("custom_effect_tooltip", "update_mio_catalog_dirty_variable"):
                pass  # Presentation and native cache dirty receipts do not change opinions.
            else: raise AssertionError("Unsupported profile effect: " + k)
    execute(rows)
    return ideas, variables


class HistoryPatchTests(unittest.TestCase):
    # IMPERIA COLD WAR — Latent release tags retain data without initializing live modifiers.
    def test_absent_release_tag_keeps_history_values_without_profile_refresh(self):
        rows = first(parse(patched('1970.1.1 = {\n}\n', EXAMPLE)), '1970.1.1')
        stats = {}
        ideas, values = run_profile(rows, 1970, stats=stats, country_exists=False)
        self.assertTrue({EXAMPLE['currency'], EXAMPLE['religion'], *EXAMPLE['factions']}.issubset(ideas))
        self.assertEqual(values['no_foreign_reserve'], 0)
        self.assertTrue(all(values[group + '_opinion'] == 50 for group in EXAMPLE['factions']))
        self.assertEqual(stats['profile_refreshes'], [])

    def test_quoted_and_commented_braces_do_not_change_spans(self):
        text = '# comment } {\n1970.1.1 = { name = "a } { b" }\n2000.1.1 = { x = yes }\n'
        self.assertEqual(len(date_blocks(text)), 1)
        updated = patched(text, EXAMPLE)
        self.assertIn('name = "a } { b"', updated)
        self.assertEqual(strip_profile(updated), text)
        self.assertEqual(patched(updated, EXAMPLE), updated)
        parse(updated)

    def test_every_real_history_has_a_safe_reversible_plan(self):
        inventory = json.loads((HERE / "inventory.json").read_text(encoding="utf-8"))
        for entry in inventory["countries"]:
            with self.subTest(tag=entry["tag"]):
                text = strip_profile((ROOT / entry["path"]).read_bytes().decode("utf-8"))
                self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(), entry["sha256"])
                updated = patched(text, EXAMPLE)
                self.assertEqual(strip_profile(updated), text)
                self.assertEqual(patched(updated, EXAMPLE), updated)
                self.assertEqual(updated.count(BEGIN), entry["snapshot_count"])
                self.assertEqual(updated.count(END), entry["snapshot_count"])
                parse(updated)

    def test_duplicate_same_date_snapshots_get_identical_profile(self):
        text = '1970.1.1 = { capital = 1 }\n1970.1.1 = { capital = 2 }\n'
        updated = patched(text, EXAMPLE)
        self.assertEqual(updated.count(BEGIN), 2)
        self.assertEqual(strip_profile(updated), text)
        self.assertEqual(patched(updated, EXAMPLE), updated)
        bodies = [v for k, _, v in parse(updated) if k == '1970.1.1']
        self.assertEqual(bodies[0][-1], bodies[1][-1])

    def test_inline_and_line_only_closers_are_reversible(self):
        for newline in ('\n', '\r\n'):
            for close_prefix in ('', ' ', '\t'):
                with self.subTest(newline=repr(newline), close_prefix=repr(close_prefix)):
                    text = (
                        '1970.1.1 = { capital = 1' + close_prefix + '}' + newline
                        + '1970.1.1 = {' + newline + '\tcapital = 2' + newline
                        + close_prefix + '}' + newline
                        + '2000.1.1 = { capital = 3 }' + newline
                    )
                    updated = patched(text, EXAMPLE)
                    self.assertEqual(strip_profile(updated), text)
                    self.assertEqual(patched(updated, EXAMPLE), updated)
                    self.assertEqual(updated.count(BEGIN), 2)
                    parse(updated)
                    if newline == '\r\n':
                        self.assertNotIn('\n', updated.replace('\r\n', ''))

    def test_crlf_is_preserved(self):
        text = 'capital = 1\r\n1970.1.1 = {\r\n\tset_variable = { a = 1 }\r\n}\r\n'
        updated = patched(text, EXAMPLE)
        self.assertNotIn('\n', updated.replace('\r\n', ''))
        self.assertEqual(strip_profile(updated), text)

    def test_bookmark_isolation_and_authored_opinions(self):
        text = '1970.1.1 = {\n}\n'
        rows = first(parse(patched(text, EXAMPLE)), '1970.1.1')
        for year in (1985, 2000, 2017):
            self.assertEqual(run_profile(rows, year, {"sunni"}, {"the_military_opinion": 70}), ({"sunni"}, {"the_military_opinion": 70}))
        ideas, values = run_profile(rows, 1970, {"sunni", "defense_industry"}, {"the_military_opinion": 70})
        self.assertNotIn("sunni", ideas)
        self.assertIn("defense_industry", ideas)
        self.assertEqual(values["the_military_opinion"], 70)
        self.assertEqual(values["farmers_opinion"], 50)
        self.assertEqual(run_profile(rows, 1970, ideas, values), (ideas, values))

    # IMPERIA COLD WAR — Preserve all authored opinions across native cleanup and reset.
    def test_native_on_add_cannot_reset_authored_opinions_or_zero(self):
        rows = first(parse(patched('1970.1.1 = {\n}\n', EXAMPLE)), '1970.1.1')
        original_values = {
            "the_military_opinion": 70,
            "farmers_opinion": 0,
            "small_medium_business_owners_opinion": 91,
            "defense_industry_opinion": 42,
        }
        for hooks in (False, True):
            with self.subTest(native_on_add=hooks):
                stats = {}
                ideas, values = run_profile(rows, 1970, {"sunni", "defense_industry"}, original_values, hooks, stats)
                self.assertTrue(set(EXAMPLE["factions"]).issubset(ideas))
                self.assertIn("defense_industry", ideas)
                for name, original in original_values.items(): self.assertEqual(values[name], original)
                self.assertFalse(any(name.startswith("COLDWAR_1970_society_") for name in values))
                self.assertEqual(len(stats["profile_refreshes"]), 1)
                self.assertEqual(stats["profile_refreshes"][0], original_values)
                if hooks:
                    self.assertEqual(stats["on_add"], EXAMPLE["factions"])
                    self.assertIn("farmers_opinion", stats["cleared"])
                    self.assertIn("small_medium_business_owners_opinion", stats["cleared"])
                    self.assertEqual(len(stats["native_refreshes"]), 3)
                    self.assertEqual(stats["native_refreshes"][0]["the_military_opinion"], 60)
                replay_stats = {}
                self.assertEqual(run_profile(rows, 1970, ideas, values, hooks, replay_stats), (ideas, values))
                for operation in ("adds", "removes", "on_add", "cleared", "native_refreshes", "profile_refreshes"):
                    self.assertEqual(replay_stats[operation], [])

    def test_missing_opinions_are_neutral_with_and_without_native_hooks(self):
        rows = first(parse(patched('1970.1.1 = {\n}\n', EXAMPLE)), '1970.1.1')
        for hooks in (False, True):
            stats = {}
            _, values = run_profile(rows, 1970, native_on_add=hooks, stats=stats)
            for faction in EXAMPLE["factions"]: self.assertEqual(values[faction + "_opinion"], 50)
            self.assertEqual(len(stats["profile_refreshes"]), 1)

    def test_held_memberships_are_not_readded_or_refreshed(self):
        rows = first(parse(patched('1970.1.1 = {\n}\n', EXAMPLE)), '1970.1.1')
        original_ideas = {EXAMPLE["currency"], EXAMPLE["religion"], *EXAMPLE["factions"], "defense_industry"}
        original_values = {"the_military_opinion": 0, "farmers_opinion": 61, "small_medium_business_owners_opinion": 84, "no_foreign_reserve": 0}
        stats = {}
        self.assertEqual(run_profile(rows, 1970, original_ideas, original_values, True, stats), (original_ideas, original_values))
        for operation in ("adds", "removes", "on_add", "cleared", "native_refreshes", "profile_refreshes"):
            self.assertEqual(stats[operation], [])

    def test_later_bookmarks_have_no_native_or_profile_calls(self):
        rows = first(parse(patched('1970.1.1 = {\n}\n', EXAMPLE)), '1970.1.1')
        for year in (1985, 2000, 2017):
            stats = {}
            baseline = ({"sunni"}, {"farmers_opinion": 0, "the_military_opinion": 77})
            self.assertEqual(run_profile(rows, year, *baseline, native_on_add=True, stats=stats), baseline)
            for operation in ("adds", "removes", "on_add", "cleared", "native_refreshes", "profile_refreshes"):
                self.assertEqual(stats[operation], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
