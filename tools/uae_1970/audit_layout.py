# IMPERIA CW — Cold War: uae 1970 — audit layout.
"""Independently reconstruct installed UAE focus geometry and native card proofs.

Reads emitted Clausewitz/YML/GFX rather than importing the compiler. Writes only
the installed-layout evidence directory under docs/design/uae_1970/installed.
"""

from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "docs/design/uae_1970/installed"
GAME = Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV")
MD = Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649")
P = "COLDWAR_UAE_"
POLITICAL = {"monarchy", "constitutional", "arab", "left", "islah"}
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[{}=]|[^\s{}=#"]+')


def parse(text):
    tokens = [m[0] for m in TOKEN.finditer(text) if not m[0].startswith("#")]
    cursor = 0

    def value():
        nonlocal cursor
        token = tokens[cursor]
        cursor += 1
        if token == "{":
            return entries(True)
        if token.startswith('"'):
            return json.loads(token)
        return token

    def entries(nested=False):
        nonlocal cursor
        output = []
        while cursor < len(tokens):
            if tokens[cursor] == "}":
                if not nested:
                    raise ValueError("Unmatched closing brace")
                cursor += 1
                return output
            key = value()
            if cursor < len(tokens) and tokens[cursor] == "=":
                cursor += 1
                output.append((key, value()))
            elif cursor < len(tokens) and tokens[cursor] in {">", "<", ">=", "<="}:
                operator = tokens[cursor]
                cursor += 1
                output.append((key, {"operator": operator, "value": value()}))
            else:
                output.append(key)
        if nested:
            raise ValueError("Unclosed block")
        return output

    return entries()


def fields(block, key):
    return [item[1] for item in block if isinstance(item, tuple) and item[0] == key]


def one(block, key, default=None):
    matches = fields(block, key)
    return matches[0] if matches else default


def read_script(relative):
    return parse((ROOT / relative).read_text(encoding="utf-8-sig"))


def read_loc(relative):
    output = {}
    for match in re.finditer(r'^\s+([^\s:]+):\d+\s+(".*")\s*$',
                             (ROOT / relative).read_text(encoding="utf-8-sig"), re.M):
        output[match[1]] = json.loads(match[2])
    return output


def groups_equal(left, right):
    return Counter(tuple(sorted(row)) for row in left) == Counter(tuple(sorted(row)) for row in right)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asset(relative):
    local = ROOT / relative
    return local if local.is_file() else GAME / relative


def glyph_data():
    glyphs, kernings = {}, {}
    path = GAME / "gfx/fonts/hoi_16mbs.fnt"
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        row = {k: int(v) for k, v in re.findall(r'(\w+)=(-?\d+)', line)}
        if line.startswith("char "):
            glyphs[row["id"]] = row
        elif line.startswith("kerning "):
            kernings[row["first"], row["second"]] = row["amount"]
    return glyphs, kernings, Image.open(path.with_suffix(".dds")).convert("RGBA")


def width(text, glyphs, kernings):
    cps = [ord(c) for c in text]
    return sum(glyphs.get(cp, glyphs[63])["xadvance"] for cp in cps) + sum(
        kernings.get((a, b), 0) for a, b in zip(cps, cps[1:]))


def label_image(text, glyphs, kernings, atlas):
    result = Image.new("RGBA", (147, 20))
    x = (147 - width(text, glyphs, kernings)) // 2
    previous = None
    for character in text:
        cp = ord(character)
        glyph = glyphs.get(cp, glyphs[63])
        x += kernings.get((previous, cp), 0)
        crop = atlas.crop((glyph["x"], glyph["y"], glyph["x"] + glyph["width"],
                           glyph["y"] + glyph["height"]))
        result.alpha_composite(crop, (x + glyph["xoffset"], 2 + glyph["yoffset"]))
        x += glyph["xadvance"]
        previous = cp
    return result


def crosses(ax, ay, bx, by, x1, y1, x2, y2):
    if ax == bx:
        return x1 < ax < x2 and max(min(ay, by), y1) < min(max(ay, by), y2)
    if ay == by:
        return y1 < ay < y2 and max(min(ax, bx), x1) < min(max(ax, bx), x2)
    return False


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def descendants(block, key):
    for item in block:
        if not isinstance(item, tuple):
            continue
        name, value = item
        if name == key:
            yield value
        if isinstance(value, list):
            yield from descendants(value, key)


def native_formatters():
    """Read the native inventories independently of the presentation module."""
    paths = [GAME / "localisation/english/modifiers_l_english.yml",
             MD / "localisation/english/MD_dm_modifiers_l_english.yml",
             ROOT / "localisation/english/MD_dm_modifiers_l_english.yml",
             ROOT / "localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml"]
    result = {}
    for path in paths:
        if path.exists():
            result.update(dict(re.findall(r'^\s*([^\s:#]+):(?:\d+)?\s*"([^\r\n]*)"',
                                          path.read_text(encoding="utf-8-sig"), re.M)))
    return result


class PreviewWorld:
    """Small emitted-preview arithmetic evaluator; not an engine/UI emulator."""

    def __init__(self, flags, governments, subject):
        self.flags, self.governments, self.subject = flags, governments, subject
        self.campaign = True
        self.date = (1970, 1, 1)
        self.variables, self.numeric, self.removed, self.treasury = {}, [], [], []
        self.dynamic = set()
        self.leaders, self.ideas = [], []
        self.state_owners = {179: "UAE", 180: "UAE"}
        self.state_controllers = dict(self.state_owners)
        self.province_naval_bases = {3725: 0}
        self.heading = None

    def number(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return self.variables.get(value, 0.0)

    def test(self, rows, state=None):
        return all(self.condition(key, value, state) for key, value in rows if key != "tooltip")

    def condition(self, key, value, state=None):
        if key.isdigit():
            return self.test(value, int(key))
        if key in {"AND", "limit", "hidden_trigger", "custom_trigger_tooltip"}:
            return self.test(value, state)
        if key == "OR":
            return any(self.condition(k, v, state) for k, v in value)
        if key == "NOT":
            return not self.test(value, state)
        if key in {"is_owned_by", "is_controlled_by"}:
            table = self.state_owners if key == "is_owned_by" else self.state_controllers
            return table[state] == ("UAE" if value == "ROOT" else value)
        if key in {'owns_state', 'controls_state'}:
            table = self.state_owners if key == 'owns_state' else self.state_controllers
            return table[int(value)] == 'UAE'
        if key == 'controls_province':
            assert str(value) == '3725'
            return self.state_controllers[179] == 'UAE'
        if key == 'any_province_building_level':
            assert one(value, 'building') == 'naval_base'
            province = int(one(one(value, 'province'), 'id'))
            level = one(value, 'level')
            assert level['operator'] == '>'
            return self.province_naval_bases[province] > int(level['value'])
        if key == "always":
            return value == "yes"
        if key == "has_country_flag":
            return value in self.flags
        if key == "has_dynamic_modifier":
            return one(value, "modifier") in self.dynamic
        if key == P + "1970_campaign":
            return self.campaign == (value == "yes")
        if key == "is_subject":
            return bool(self.subject) == (value == "yes")
        if key == "is_subject_of":
            return self.subject == value
        if key == P + "monarchy_government":
            return bool({"western_autocrats_are_in_power", "nationalist_monarchists_are_in_power"}
                        & self.governments) == (value == "yes")
        if key.endswith("_are_in_power"):
            return (key in self.governments) == (value == "yes")
        if key == "check_variable":
            if one(value, "var"):
                left, right = self.number(one(value, "var")), self.number(one(value, "value"))
            else:
                variable, operand = value[0]
                left, right = self.number(variable), self.number(operand)
            compare = one(value, "compare", "equals")
            return {"equals": left == right, "greater_than": left > right,
                    "less_than": left < right, "greater_than_or_equals": left >= right,
                    "less_than_or_equals": left <= right}[compare]
        if key == "date":
            other = tuple(map(int, value["value"].split(".")))
            return {">": self.date > other, "<": self.date < other,
                    ">=": self.date >= other, "<=": self.date <= other}[value["operator"]]
        raise AssertionError("Unmodelled preview condition: " + key)

    def run(self, rows):
        branch = False
        for key, value in rows:
            if key == "if":
                branch = self.test(one(value, "limit", []))
                if branch:
                    self.run([row for row in value if row[0] != "limit"])
            elif key == "else_if":
                if not branch and self.test(one(value, "limit", [])):
                    self.run([row for row in value if row[0] != "limit"])
                    branch = True
            elif key == "else":
                if not branch:
                    self.run(value)
                branch = False
            elif key in {"set_temp_variable", "set_variable", "add_to_temp_variable", "subtract_from_temp_variable",
                         "add_to_variable", "subtract_from_variable", "multiply_variable", "multiply_temp_variable", "divide_variable", "divide_temp_variable"}:
                operands = [(k, v) for k, v in value if k != "tooltip"]
                if len(operands) != 1:
                    raise AssertionError("Malformed numeric preview instruction: " + str(value))
                variable, operand = operands[0]
                amount = self.number(operand)
                if key.startswith("set_"):
                    self.variables[variable] = amount
                elif key.startswith("add_"):
                    self.variables[variable] = self.number(variable) + amount
                elif key.startswith("subtract_"):
                    self.variables[variable] = self.number(variable) - amount
                elif key.startswith("multiply_"):
                    self.variables[variable] = self.number(variable) * amount
                else:
                    self.variables[variable] = self.number(variable) / amount
                tooltip = one(value, "tooltip")
                if tooltip:
                    self.numeric.append((self.heading, variable, amount, tooltip))
            elif key in {"clamp_temp_variable", "clamp_variable"}:
                variable = one(value, "var")
                self.variables[variable] = max(self.number(one(value, "min", "-inf")),
                    min(self.number(one(value, "max", "inf")), self.number(variable)))
            elif key == "custom_effect_tooltip":
                if isinstance(value, list) and one(value, "localization_key") == "modifies_dynamic_modifier_tt":
                    self.heading = one(value, "MODIFIER")
            elif key == "remove_dynamic_modifier":
                self.removed.append(one(value, "modifier"))
            elif key == "modify_treasury_effect":
                self.treasury.append(self.number("treasury_change"))
            elif key == "create_country_leader":
                self.leaders.append(value)
            elif key == "add_ideas":
                self.ideas.append(value)
            elif key.isdigit():
                self.run(value)
            # Other native, non-numeric completion leaves are checked separately;
            # this evaluator deliberately does not run their real providers.


def runtime_condition(condition):
    return condition.replace("nationalist_monarchists_are_in_power = yes", P + "monarchy_government = yes")


def spirit_component(data, spirit, modifier, flags):
    """Independent strongest-family credit calculation from the design payload."""
    base = spirit["modifiers"][modifier]
    credits = defaultdict(float)
    for candidate in data["nodes"]:
        if P + "done_" + candidate["id"].removeprefix(P) not in flags:
            continue
        for change in candidate.get("spirit_changes", []):
            if change["spirit"] == spirit["id"] and change["component"] == modifier:
                credit = abs(base - change["value"]) if change["operation"] == "set" else abs(change["value"])
                credits[change["family"]] = max(credits[change["family"]], credit)
    amount = base - math.copysign(sum(credits.values()), base)
    if spirit["id"] == P + "unequal_development" and modifier == "stability_factor" and P + "mediate_settled" in flags:
        amount = 0
    if spirit["id"] == P + "fragmented_authority" and modifier == "bureaucracy_cost_multiplier_modifier" and P + "cabinet_settled" in flags:
        amount -= 0.03
    amount = max(amount, 0) if base > 0 else min(amount, 0)
    if spirit['id'] == P+'maritime_livelihoods' and modifier in {
            'agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier'}:
        amount *= maritime_share(flags)
    return amount


def maritime_share(flags):
    oil = ('oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase')
    return max(.2, 1-.2*sum(P+'done_'+key in flags for key in oil))


def expected_numbers(node, data, world):
    """Expected observable deltas, without importing the emitter's preview API."""
    expected = []
    suffix = node["id"].removeprefix(P)
    # Advertise prospective rewards even when this route is currently locked.
    # The real activation predicate remains in the live reconciler. Arithmetic
    # still measures current credits/caps rather than promising nominal relief.
    programme = P + node["group"] + "_programme"
    for modifier, value in node["modifiers"].items():
        if suffix in {'trading_coast', 'port_planning'} and modifier in {
                'agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier'}:
            value *= maritime_share(world.flags)
        if node["group"] in POLITICAL and modifier == "stability_factor" and value > 0:
            before = sum(c["modifiers"].get("stability_factor", 0) for c in data["nodes"]
                if c["group"] == node["group"] and c["modifiers"].get("stability_factor", 0) > 0
                and P + "done_" + c["id"].removeprefix(P) in world.flags
                and world.test(parse(runtime_condition(c["active_condition"])))
                and (not c["temporary_days"] or P + "temporary_" + c["id"].removeprefix(P) in world.flags))
            value = min(before + (0 if P + "done_" + suffix in world.flags else value), 0.15) - min(before, 0.15)
        if modifier == "monthly_population":
            before = sum(c["modifiers"].get("monthly_population", 0) for c in data["nodes"]
                if P + "done_" + c["id"].removeprefix(P) in world.flags
                and world.test(parse(runtime_condition(c["active_condition"])))
                and (not c["temporary_days"] or P + "temporary_" + c["id"].removeprefix(P) in world.flags))
            value = min(before + (0 if P + "done_" + suffix in world.flags else value), 2.0) - min(before, 2.0)
        if suffix == "citizen_republic" and modifier == "stability_factor" and value < 0 and P + "court_settled" in world.flags:
            continue
        expected.append((programme, P + node["group"] + "_" + modifier, value, modifier))
    for conditional in node.get("conditional_contributions", []):
        expected.extend((programme, P + node["group"] + "_" + key, value, key)
            for key, value in conditional["modifiers"].items() if key not in node["modifiers"])
    affected = defaultdict(list)
    for change in node.get("spirit_changes", []):
        if change["component"] not in affected[change["spirit"]]:
            affected[change["spirit"]].append(change["component"])
    removed = []
    after_flags = world.flags | {P + "done_" + suffix}
    if suffix == 'rulers_compact':
        # Direct compact completion now settles the cabinet, independently of
        # whether the former optional dialogue had previously been accepted.
        affected[P+'fragmented_authority'] = list(dict.fromkeys(
            affected[P+'fragmented_authority'] + ['bureaucracy_cost_multiplier_modifier']))
        after_flags = after_flags | {P+'cabinet_settled'}
    for spirit_id, modifiers in affected.items():
        spirit = next(s for s in data["starting_spirits"] if s["id"] == spirit_id)
        for modifier in modifiers:
            before = spirit_component(data, spirit, modifier, world.flags)
            after = spirit_component(data, spirit, modifier, after_flags)
            variable = (spirit_id+'_'+modifier if suffix == 'rulers_compact'
                        else P + "preview_display")
            expected.append((spirit_id, variable, after - before, modifier))
        if spirit_id in world.dynamic and all(math.isclose(spirit_component(data, spirit, m, after_flags), 0, abs_tol=1e-10) for m in spirit["modifiers"]):
            removed.append(spirit_id)
    if suffix in {'oil_accounts', 'onshore_expansion', 'offshore_expansion', 'offshore_second_phase'}:
        spirit = next(s for s in data['starting_spirits'] if s['id'] == P+'maritime_livelihoods')
        scaled = ('agricolture_productivity_modifier', 'offices_productivity', 'social_cost_multiplier_modifier')
        for modifier in scaled:
            before = spirit_component(data, spirit, modifier, world.flags)
            after = spirit_component(data, spirit, modifier, after_flags)
            expected.append((spirit['id'], P+'preview_display', after-before, modifier))
        earned = [n for n in data['nodes'] if n['id'].removeprefix(P) in {'trading_coast', 'port_planning'}
                  and P+'done_'+n['id'].removeprefix(P) in world.flags]
        if earned:
            delta = maritime_share(after_flags)-maritime_share(world.flags)
            for modifier in scaled:
                amount = sum(n['modifiers'].get(modifier, 0) for n in earned
                    if world.test(parse(runtime_condition(n['active_condition']))))*delta
                expected.append((P+'commerce_programme', P+'preview_display', amount, modifier))
    return expected, removed


def numeric_preview_checks(node, data, preview, native_loc, local_loc):
    errors, cases = [], 0
    all_done = {P + "done_" + n["id"].removeprefix(P) for n in data["nodes"] if n["id"] != node["id"]}
    alternating = {flag for index, flag in enumerate(sorted(all_done)) if index % 2}
    temporary = {P + "temporary_" + n["id"].removeprefix(P) for n in data["nodes"] if n["temporary_days"]}
    accepted = {str(value) for value in descendants(preview, "has_country_flag")
                if not str(value).startswith(P + "done_") and not str(value).startswith(P + "temporary_")}
    accepted |= {P + key for key in ("founders_consented", "federation_established", "oil_participation_accepted",
        "broad_charter_accepted", "friendship_accepted", "protection_accepted", "islah_organised",
        "mediate_settled", "cabinet_settled", "court_settled")}
    governments = {"western_autocrats_are_in_power", "nationalist_monarchists_are_in_power",
        "western_liberals_are_in_power", "western_conservatism_are_in_power", "emerging_autocracy_are_in_power",
        "nationalist_military_junta_are_in_power", "emerging_communist_state_are_in_power",
        "neutrality_neutral_social_are_in_power", "neutrality_neutral_muslim_brotherhood_are_in_power"}
    contexts = [(set(), set(), None), (all_done | temporary, governments, None),
                (all_done | temporary | accepted, governments, None), (alternating | accepted, governments, None),
                (all_done | accepted, governments, 179), (all_done | accepted, governments, 180)]
    for flags, current_governments, lost_state in contexts:
        for subject in ("ENG", None, "OTHER"):
            world = PreviewWorld(flags, current_governments, subject)
            if lost_state:
                world.state_controllers[lost_state] = "PER"
            world.dynamic = {spirit["id"] for spirit in data["starting_spirits"]
                if any(not math.isclose(spirit_component(data, spirit, m, flags), 0, abs_tol=1e-10) for m in spirit["modifiers"])}
            wanted, removals = expected_numbers(node, data, world)
            world.run(preview)
            cases += 1
            actual = sorted(world.numeric, key=lambda row: (row[0] or "", row[1], row[3]))
            anticipated = []
            for heading, variable, value, modifier in wanted:
                formatter = modifier + "_tt" if modifier + "_tt" in native_loc else P + "tt_" + modifier
                anticipated.append((heading, variable, value, formatter))
            anticipated.sort(key=lambda row: (row[0] or "", row[1], row[3]))
            if len(actual) != len(anticipated) or any(a[:2] != b[:2] or a[3] != b[3] or not math.isclose(a[2], b[2], abs_tol=1e-9)
                                                   for a, b in zip(actual, anticipated)):
                errors.append(f"Numeric preview differs from independent arithmetic: {node['id']} context {cases}: {actual} != {anticipated}")
                break
            if sorted(world.removed) != sorted(removals):
                errors.append(f"Starting-spirit removal preview differs: {node['id']} context {cases}")
                break
            cost = node["treasury_cost_billion"]
            if world.treasury != ([-cost] if cost else []):
                errors.append(f"Treasury preview differs: {node['id']} context {cases}")
                break
    for entry in descendants(preview, "add_to_variable"):
        formatter = one(entry, "tooltip")
        if formatter and formatter not in native_loc:
            if not formatter.startswith(P + "tt_imp_") or "$RIGHT|" not in local_loc.get(formatter, ""):
                errors.append("Missing native or necessary Imperia numeric formatter: " + str(formatter))
    future_agreement = node["id"].removeprefix(P)
    future_agreement = future_agreement in {"british_friendship", "state_participation"} or any(
        key not in node["modifiers"] for c in node.get("conditional_contributions", []) for key in c["modifiers"])
    if future_agreement and "TT_IF_THEY_ACCEPT" not in list(descendants(preview, "custom_effect_tooltip")):
        errors.append("Future agreement reward lacks native acceptance heading: " + node["id"])
    return errors, cases


def opening_revision_checks(data, by):
    """Check real emitted start predicates and the sole formation dispatch."""
    errors, checked = [], []
    triggers = dict(read_script("common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt"))
    politics_triggers = dict(read_script("common/scripted_triggers/COLDWAR_UAE_1970_politics_triggers.txt"))
    campaign = politics_triggers[P + "1970_campaign"]
    expected_campaign = [("original_tag", "UAE"), ("is_dynamic_country", "no"), ("IMP_is_1970_scenario", "yes")]
    if campaign != expected_campaign:
        errors.append("Campaign identity differs from original, non-dynamic 1970 UAE predicate")
    scenario = (ROOT / "common/scripted_triggers/IMP_cold_war_scenario_triggers.txt").read_text(encoding="utf-8-sig")
    scenario_block = re.search(r'IMP_is_1970_scenario\s*=\s*\{([^{}]+)\}', scenario).group(1)
    if not re.search(r'has_start_date\s*>\s*1969\.12\.31', scenario_block) or not re.search(r'has_start_date\s*<\s*1970\.1\.2', scenario_block):
        errors.append("Actual campaign scenario no longer selects the January 1, 1970 start")
    checked.append("Actual campaign helper: original UAE, non-dynamic, January 1 1970 start-date bounds")
    # Actual scenario identity is evaluated separately from subject status;
    # even zero/negative treasury cannot introduce a silent opening gate.
    count = 0
    for original_tag, dynamic, start in [("UAE", False, (1970, 1, 1)), ("UAE", True, (1970, 1, 1)),
                                         ("ENG", False, (1970, 1, 1)), ("UAE", False, (2000, 1, 1))]:
        identity = original_tag == "UAE" and not dynamic and (1969, 12, 31) < start < (1970, 1, 2)
        for subject in ("ENG", None, "USA"):
            for treasury in (-1, 0, 10):
                world = PreviewWorld(set(), set(), subject)
                world.campaign = identity
                world.variables["treasury"] = treasury
                protected = world.test(triggers[P + "can_apply_treaty_coast"])
                transition = world.test(triggers[P + "can_apply_council"])
                if protected != (identity and subject == "ENG") or transition != (identity and subject is None):
                    errors.append(f"Opening availability differs: {original_tag}/{dynamic}/{start}/{subject}/{treasury}")
                count += 1
    checked.append(f"{count} emitted opening-gate contexts: original/dynamic/modern/foreign identity, ENG/USA/free, negative/zero/funded treasury")
    effects = dict(read_script("common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt"))
    callers = [key for key, body in effects.items() if list(descendants(body, P + "form_federation"))]
    if callers != [P + "apply_proclaim_federation"]:
        errors.append("Federation formation has a caller outside the new proclamation focus: " + str(callers))
    root_apply = effects[P + "apply_treaty_coast"]
    if list(descendants(root_apply, "modify_treasury_effect")):
        errors.append("Protected Coast still charges treasury in its real guarded application")
    politics = dict(read_script("common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt"))
    formation = one(politics[P + "form_federation"], "if")
    required = [("is_subject", "no"), (P + "1970_campaign", "yes"),
        ("has_country_flag", P + "done_sovereign_union"), ("has_country_flag", P + "done_proclaim_federation"),
        ("has_country_flag", P + "founders_consented")]
    if not all(entry in one(formation, "limit") for entry in required) or one(formation, "drop_cosmetic_tag") != "yes":
        errors.append("Federation/name provider lacks actual independence, earned proclamation or founders' settlement")
    if one(one(one(by[P + "proclaim_federation"], "completion_reward"), "effect_tooltip"), "drop_cosmetic_tag") != "yes":
        errors.append("Proclamation does not expose the native cosmetic-name result")
    checked.append("Only new proclamation dispatches formation; real provider rechecks full independence, two earned focuses, founders and one-time guard")
    proclamation = one(one(by[P + "proclaim_federation"], "completion_reward"), "effect_tooltip")
    office_cases = 0
    for date in [(1970, 1, 1), (1971, 12, 2), (1990, 10, 6), (1990, 10, 7), (2004, 11, 1),
                 (2004, 11, 2), (2006, 1, 3), (2006, 1, 4), (2022, 5, 12), (2022, 5, 13)]:
        for slot in (0, 23, 1):
            for cabinet in (False, True):
                flags = {P + "cabinet_settled"} if cabinet else set()
                governments = {"western_autocrats_are_in_power"} if slot == 0 else {"nationalist_monarchists_are_in_power"} if slot == 23 else set()
                world = PreviewWorld(flags, governments, None)
                world.date, world.variables["ruling_party"] = date, slot
                world.run(proclamation)
                if slot in (0, 23):
                    leader = "Mohammed bin Zayed Al Nahyan" if date > (2022, 5, 12) else "Khalifa bin Zayed Al Nahyan" if date > (2004, 11, 1) else "Zayed bin Sultan Al Nahyan"
                    ideology = "Western_Autocracy" if slot == 0 else "Monarchist"
                    expected_pm = P + "prime_minister_rashid" if cabinet and date < (1990, 10, 7) else P + "prime_minister_maktoum" if date < (2006, 1, 4) else None
                    if len(world.leaders) != 1 or one(world.leaders[0], "name") != leader or one(world.leaders[0], "ideology") != ideology:
                        errors.append(f"Native proclamation office preview differs: {date}/{slot}/{cabinet}")
                    if world.ideas != ([expected_pm] if expected_pm else []):
                        errors.append(f"Native proclamation prime-minister preview differs: {date}/{slot}/{cabinet}")
                    for office in world.leaders:
                        if not (ROOT / one(office, "picture")).is_file() or "king" not in one(office, "traits"):
                            errors.append("Native office portrait or dynastic trait is missing")
                elif world.leaders or world.ideas:
                    errors.append("Proclamation advertises royal office appointment under a non-dynastic government")
                office_cases += 1
    checked.append(f"{office_cases} native proclamation office-preview contexts: historical/delayed dates, both dynastic slots, republican government and cabinet status")
    def inspect_funding(rows, seen=frozenset()):
        for key, value in rows:
            if key == "check_variable":
                variable = one(value, "var", value[0][0])
                if variable == "treasury":
                    return True
            if key == "custom_trigger_tooltip" and str(one(value, "tooltip", "")).endswith("_funds_tt"):
                return True
            if isinstance(value, list) and inspect_funding(value, seen):
                return True
            if key in triggers and key not in seen and inspect_funding(triggers[key], seen | {key}):
                return True
        return False
    for node in data["nodes"]:
        trigger = triggers[P + "can_apply_" + node["id"].removeprefix(P)]
        if inspect_funding(trigger):
            errors.append("Focus retains a direct/transitive treasury veto: " + node["id"])
    checked.append(f"All{len(data['nodes'])} actual focus eligibility predicates omit direct/transitive treasury vetoes and funding labels; native cost previews remain")
    return errors, checked


def main():
    approved_path = HERE / "approved_design.json"
    original = json.loads(approved_path.read_text(encoding="utf-8"))
    # The original approval remains immutable. The user's later correction is
    # a separately hashed overlay, rather than a rewritten approval snapshot.
    revision_path = HERE / "revision.py"
    data = load_module("uae_review_revision", revision_path).current_design()
    approval = json.loads((HERE / "approval.json").read_text())
    errors, warnings = [], []
    if sha(approved_path) != approval["sha256"]:
        errors.append("Immutable approved-design hash differs from approval.json")
    original_by = {node["id"]: node for node in original["nodes"]}
    revised_by = {node["id"]: node for node in data["nodes"]}
    from focus_only import NEW_FOCUS_KEYS, FOCUS_ACTIONS
    additions = {P + key for key in ("proclaim_federation", "jebel_ali_smelter", "steel_rolling_mills", *NEW_FOCUS_KEYS)}
    if set(revised_by) - set(original_by) != additions or set(original_by) - set(revised_by):
        errors.append("Revision adds/removes focuses outside the requested federation and industrial focuses")
    allowed = {P + "council": {"available", "description"},
               P + "treaty_coast": {"treasury_cost_billion", "available", "effect_body", "reward_summary"},
               P + "sovereign_union": {"description", "effect_body", "reward_summary"},
               P + "rak_accession": {"xy", "prerequisites"},
               P + "federal_council": {"xy", "prerequisites"}, P + "dirham": {"xy"}}
    development_fields = {"treasury_cost_billion", "days", "cost", "available", "description", "modifiers", "reward_summary"}
    for identifier in original_by:
        allowed.setdefault(identifier, set()).update({"available", "effect_body", "requirement_contracts", "days", "cost"})
    for key in ("oil_accounts", "onshore_expansion", "offshore_expansion", "offshore_second_phase"):
        allowed[P+key].update({"description", "reward_summary"})
    for key in ("schools_clinics", "water_network", "citizen_housing", "worker_towns", "efficient_services"):
        allowed[P + key] = development_fields
    allowed[P + "industrial_port"] = development_fields | {"effect_body"}
    allowed[P + "aviation_hub"] = development_fields | {"effect_body"}
    for key in ("trading_coast", "port_planning"):
        allowed[P + key] = development_fields | {"title", "narrative_title", "spirit_changes"}
    # Explicit later authorizations, scoped to their actual node/field owners.
    direct_fields = {
        'petition_independence': {'description', 'modifiers', 'spirit_changes', 'ownership', 'diplomatic_offer', 'reward_summary'},
        'charter': {'description', 'reward_summary'},
        'dual_veto': set(), 'federal_ministries': set(),
        'development_fund': {'description', 'modifiers', 'spirit_changes', 'reward_summary'},
        'presidential_union': {'description'},
        'rulers_compact': {'description', 'reward_summary'},
        'citizen_republic': {'description', 'modifiers', 'reward_summary'},
        'federal_council': {'description', 'focus_only_effect_body', 'reward_summary'},
        'majlis': {'description'}, 'oil_shock_plan': {'description'},
        'gulf_diplomacy': {'description', 'modifiers', 'reward_summary'},
    }
    for key, fields_allowed in direct_fields.items():
        allowed[P+key].update(fields_allowed | {'streamlined'})
    for identifier, before in original_by.items():
        after = revised_by[identifier]
        normalized_summary = [line for line in before.get('reward_summary', [])
            if not any(word in line.lower() for word in
                ('unlock', 'decision', 'respond to an invasion', 'crisis popup'))]
        if after.get('reward_summary') == normalized_summary:
            allowed[identifier].add('reward_summary')
        key = identifier.removeprefix(P)
        if key in FOCUS_ACTIONS and after.get('focus_actions') == FOCUS_ACTIONS[key]:
            allowed[identifier].add('focus_actions')
    revision_changes = {}
    for identifier, before in original_by.items():
        after = revised_by.get(identifier, {})
        changed = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
        if changed:
            revision_changes[identifier] = sorted(changed)
        if changed - allowed.get(identifier, set()):
            errors.append("Unrequested revision fields: " + identifier + " " + str(sorted(changed)))
    starting_original = {s["id"]: s for s in original["starting_spirits"]}
    # Later explicit user revision replaces only the expatriate military malus.
    starting_original[P+'expatriate_workforce']['modifiers'] = {
        'total_workforce_modifier': 0.10, 'army_morale_factor': -0.20}
    starting_current = {s["id"]: s for s in data["starting_spirits"]}
    if set(starting_current) - set(starting_original) != {P + "maritime_livelihoods"} or any(
            starting_current.get(key) != value for key, value in starting_original.items()):
        errors.append("Starting-spirit revision differs outside the authorized maritime addition and expatriate recovery-rate change")
    maritime = starting_current.get(P + "maritime_livelihoods", {})
    if maritime.get("modifiers") != {"agricolture_productivity_modifier": 0.10,
                                     "offices_productivity": 0.03, "social_cost_multiplier_modifier": -0.05,
                                     "country_productivity_growth_modifier": -0.05}:
        errors.append("Maritime starting-spirit values differ from authorized payload")

    focus_path = "common/national_focus/COLDWAR_UAE_1970_focus.txt"
    focus_text = (ROOT / focus_path).read_text(encoding="utf-8-sig")
    tree = one(parse(focus_text), "focus_tree")
    emitted = fields(tree, "focus")
    by = {one(focus, "id"): focus for focus in emitted}
    expected = {n["id"]: n for n in data["nodes"]}
    if len(emitted) != len(by) or set(by) != set(expected):
        errors.append("Emitted focus IDs or multiplicity differ from the current revision")
    revision_errors, revision_checks = opening_revision_checks(data, by)
    errors.extend(revision_errors)
    positions = {}

    def resolve(identifier, trail=()):
        if identifier in positions:
            return positions[identifier]
        if identifier in trail:
            raise ValueError("Relative-anchor cycle: " + " -> ".join(trail + (identifier,)))
        block = by[identifier]
        anchor = one(block, "relative_position_id")
        base = resolve(anchor, trail + (identifier,)) if anchor else (0, 0)
        positions[identifier] = (base[0] + float(one(block, "x", "0")),
                                 base[1] + float(one(block, "y", "0")))
        return positions[identifier]

    loc_path = "localisation/english/COLDWAR_UAE_1970_focus_l_english.yml"
    loc = read_loc(loc_path)
    native = {one(block, "name"): one(block, "texturefile", one(block, "textureFile"))
              for block in fields(one(read_script("interface/goals.gfx"), "spriteTypes"), "spriteType")}
    gfx_path = "interface/COLDWAR_UAE_1970_goals.gfx"
    gfx = {one(block, "name"): one(block, "texturefile")
           for block in fields(one(read_script(gfx_path), "spriteTypes"), "spriteType")}
    shine_path = "interface/COLDWAR_UAE_1970_goals_shine.gfx"
    shines = {one(block, "name"): block
              for block in fields(one(read_script(shine_path), "spriteTypes"), "spriteType")}

    flavour = load_module("uae_review_flavour", HERE / "flavour.py")
    native_loc = native_formatters()
    numeric_cases = 0
    glyphs, kernings, atlas = glyph_data()
    nodes, art = [], {}
    for identifier, approved in expected.items():
        focus = by[identifier]
        position = resolve(identifier)
        prereqs = [fields(clause, "focus") for clause in fields(focus, "prerequisite")]
        exclusive = [other for clause in fields(focus, "mutually_exclusive") for other in fields(clause, "focus")]
        title = loc.get(identifier)
        description = loc.get(identifier + "_desc")
        icon = one(focus, "icon")
        if list(position) != approved["xy"]:
            errors.append(f"Position differs: {identifier}: {position} != {approved['xy']}")
        if not groups_equal(prereqs, approved["prerequisites"]):
            errors.append("Grouped prerequisites differ: " + identifier)
        if sorted(exclusive) != sorted(approved["mutually_exclusive"]):
            errors.append("Exclusions differ: " + identifier)
        if not math.isclose(float(one(focus, "cost")) * 7, approved["days"], abs_tol=1e-8):
            errors.append("Nominal duration differs: " + identifier)
        if title != approved["title"]:
            errors.append("English title differs: " + identifier)
        # Final reviewed prose is intentionally authored in flavour, including
        # focused overrides of the structured design's historical brief.
        expected_description = approved['description'] if approved.get('streamlined') else flavour.FOCUS_DESCRIPTIONS[identifier]
        if description != expected_description:
            errors.append("Finished English description differs: " + identifier)
        if not title or width(title, glyphs, kernings) > 147:
            errors.append("Title exceeds native field: " + identifier)
        completion = one(focus, "completion_reward", [])
        preview = one(completion, "effect_tooltip", [])
        live = one(completion, "hidden_effect", [])
        suffix = identifier.removeprefix("COLDWAR_UAE_")
        if len(fields(completion, "effect_tooltip")) != 1 or one(live, "COLDWAR_UAE_apply_" + suffix) != "yes":
            errors.append("Completion does not separate native preview from guarded live grant: " + identifier)
        preview_errors, cases = numeric_preview_checks(approved, data, preview, native_loc, loc)
        errors.extend(preview_errors)
        numeric_cases += cases
        treasury_previews = [one(entry, "treasury_change") for entry in fields(preview, "set_temp_variable")
                             if one(entry, "treasury_change") is not None]
        cost = approved["treasury_cost_billion"]
        if (cost and treasury_previews != [f"{-cost:g}"]) or (not cost and treasury_previews):
            errors.append("Displayed native treasury debit differs from approval: " + identifier)
        if cost and one(preview, "modify_treasury_effect") != "yes":
            errors.append("Native treasury formatter/provider missing from preview: " + identifier)
        if icon != "GFX_" + identifier or gfx.get(icon) != native.get(approved["icon"]):
            errors.append("Approved native focus art differs: " + identifier)
        shine = shines.get(str(icon) + "_shine")
        if not shine or one(shine, "texturefile") != gfx.get(icon):
            errors.append("Focus shine texture differs: " + identifier)
        elif any(one(animation, "animationmaskfile") != gfx[icon] for animation in fields(shine, "animation")):
            errors.append("Focus shine mask differs: " + identifier)
        texture = gfx[icon]
        image = Image.open(ROOT / texture).convert("RGBA")
        art[icon] = image
        line = focus_text[:focus_text.index("id = " + identifier + "\n")].count("\n") + 1
        nodes.append(dict(id=identifier, group=approved["group"], title=title, description=description,
                          xy=list(position), anchor=one(focus, "relative_position_id"),
                          emitted_xy=[float(one(focus, "x", "0")), float(one(focus, "y", "0"))],
                          days=float(one(focus, "cost")) * 7, prerequisites=prereqs,
                          mutually_exclusive=exclusive, icon=icon, texture=texture,
                          texture_sha256=sha(ROOT / texture), source_line=line))

    node_by = {n["id"]: n for n in nodes}
    collisions = []
    for node in nodes:
        x, y = node["xy"][0] * 96, node["xy"][1] * 130
        for clause in node["prerequisites"]:
            for parent_id in clause:
                parent = node_by[parent_id]
                px, py = parent["xy"][0] * 96, parent["xy"][1] * 130
                middle = (py + 90 + y - 26) / 2
                segments = [(px + 80, py + 90, px + 80, middle),
                            (px + 80, middle, x + 80, middle), (x + 80, middle, x + 80, y - 26)]
                for other in nodes:
                    if other["id"] in (node["id"], parent_id):
                        continue
                    ox, oy = other["xy"][0] * 96, other["xy"][1] * 130
                    image = art[other["icon"]]
                    bounds = image.getbbox()
                    ix, iy = ox + 87.5 - image.width / 2, oy + 20 - image.height / 2
                    rectangles = [(ix + bounds[0], iy + bounds[1], ix + bounds[2], iy + bounds[3]),
                                  (ox + 5, oy + 40, ox + 169, oy + 90)]
                    if any(crosses(*segment, *rectangle) for segment in segments for rectangle in rectangles):
                        collisions.append([parent_id, node["id"], other["id"]])
    errors.extend("Unrelated card intersection: " + " -> ".join(c) for c in collisions)
    if one(one(tree, "initial_show_position"), "focus") != "COLDWAR_UAE_treaty_coast":
        errors.append("Initial camera no longer targets the approved British opening")
    if len(fields(tree, "shortcut")) != len(data["groups"]) + 1:
        errors.append("Programme shortcut count differs")
    if not any(one(shortcut, 'target') == 'COLDWAR_GCC_council' for shortcut in fields(tree, 'shortcut')):
        errors.append('Shared GCC shortcut is missing')

    programme_loc_path = "localisation/english/COLDWAR_UAE_1970_programmes_l_english.yml"
    programme_loc = read_loc(programme_loc_path)
    for identifier, description in flavour.SPIRIT_DESCRIPTIONS.items():
        if programme_loc.get(identifier + "_desc") != description:
            errors.append("Starting-spirit English differs: " + identifier)
    if programme_loc.get(maritime.get("id")) != maritime.get("label") or programme_loc.get(P + "maritime_livelihoods_desc") != maritime.get("description"):
        errors.append("Maritime starting-spirit English differs from the current revision")
    native_ideas = {one(block, "name"): one(block, "texturefile")
        for block in fields(one(read_script("interface/MD_ideas.gfx"), "spriteTypes"), "spriteType")}
    maritime_texture = native_ideas.get("GFX_idea_maritime_industry")
    maritime_alias = "GFX_idea_" + P + "maritime_livelihoods"
    if not maritime_texture or not maritime_texture.startswith("gfx/interface/ideas/") or gfx.get(maritime_alias) != maritime_texture:
        errors.append("Maritime national spirit does not use the reviewed native national-spirit artwork")
    dynamic_definitions = dict(read_script("common/dynamic_modifiers/COLDWAR_UAE_1970_programmes.txt"))
    maritime_definition = dynamic_definitions.get(P + "maritime_livelihoods", [])
    if one(maritime_definition, "icon") != maritime_alias or any(one(maritime_definition, key) != P + "maritime_livelihoods_" + key for key in maritime["modifiers"]):
        errors.append("Maritime national-spirit artwork or numeric consumers differ")
    programme_effects = read_script("common/scripted_effects/COLDWAR_UAE_1970_programmes.txt")
    if not any(one(row, "modifier") == P + "maritime_livelihoods" for row in descendants(programme_effects, "add_dynamic_modifier")):
        errors.append("Maritime national spirit has no real installation provider")
    native_acceptance_loc = (ROOT / "localisation/english/MD_tooltips_l_english.yml").read_text(encoding="utf-8-sig")
    if not re.search(r'(?m)^\s*TT_IF_THEY_ACCEPT\s*:', native_acceptance_loc):
        errors.append("Native future-acceptance heading has no localisation provider")
    for path in (loc_path, programme_loc_path):
        if not (ROOT / path).read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append("Missing localisation UTF-8 BOM: " + path)
    if "$RIGHT|-=2$" not in native_loc.get("interest_rate_multiplier_modifier_tt", ""):
        errors.append("Interest-rate preview is not using the native lower-is-better formatter")
    obsolete = [key for key in loc if key.startswith((P + "reward_", P + "programme_terms_"))
                or key == P + "political_stability_cap_tt"]
    if obsolete:
        errors.append("Obsolete prose reward paragraphs remain: " + str(obsolete))

    OUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
    bar_path = asset("gfx/interface/focusview/titlebar/focus_unavailable_bg.dds")
    bar = Image.open(bar_path).convert("RGBA")
    proofs = []
    def render(subset, filename, title):
        minx = min(n["xy"][0] for n in subset) * 96 - 30
        miny = min(n["xy"][1] for n in subset) * 130 - 110
        maxx = max(n["xy"][0] for n in subset) * 96 + 205
        maxy = max(n["xy"][1] for n in subset) * 130 + 140
        proof = Image.new("RGBA", (round(maxx - minx), round(maxy - miny)), "#22343c")
        draw = ImageDraw.Draw(proof)
        for node in subset:
            x, y = node["xy"][0] * 96 - minx, node["xy"][1] * 130 - miny
            for clause in node["prerequisites"]:
                for parent_id in clause:
                    parent = node_by[parent_id]
                    px, py = parent["xy"][0] * 96 - minx, parent["xy"][1] * 130 - miny
                    middle = (py + 90 + y - 26) // 2
                    draw.line([(px + 80, py + 90), (px + 80, middle), (x + 80, middle), (x + 80, y - 26)],
                              fill="#9aabad", width=2)
            for peer_id in node["mutually_exclusive"]:
                if peer_id < node["id"]:
                    continue
                peer = node_by[peer_id]
                peer_x = peer["xy"][0] * 96 - minx
                left, right = min(x, peer_x) + 139, max(x, peer_x) + 27
                for dash in range(round(left), round(right), 9):
                    draw.line([(dash, y + 20), (min(dash + 4, right), y + 20)], fill="#d9a287", width=2)
                draw.text(((left + right) // 2 - 4, y - 3), "×", font=font, fill="#d9a287")
        for node in subset:
            x, y = node["xy"][0] * 96 - minx, node["xy"][1] * 130 - miny
            icon = art[node["icon"]]
            proof.alpha_composite(icon, (int(x + 87.5 - icon.width / 2), int(y + 20 - icon.height / 2)))
            proof.alpha_composite(bar, (int(x + 5), int(y + 40)))
            proof.alpha_composite(label_image(node["title"], glyphs, kernings, atlas), (int(x + 15), int(y + 58)))
        draw.text((18, 12), title, font=font, fill="#e3cf90")
        draw.text((18, 38), "Installed source · native cards; approximate lines", font=font, fill="#c4cdcb")
        path = OUT / filename
        proof.convert("RGB").save(path)
        proofs.append(str(path.relative_to(ROOT)))
        return proof

    for group in data["groups"]:
        subset = [n for n in nodes if n["group"] == group["id"]]
        render(subset, "BRANCH_" + group["id"] + ".png", group["label"])
    maritime_image = Image.open(ROOT / maritime_texture).convert("RGBA")
    art_proof = Image.new("RGBA", (660, 235), "#22343c")
    art_draw = ImageDraw.Draw(art_proof)
    art_draw.text((18, 12), "Pearls, Fishing and Dhows · actual native national-spirit artwork", font=font, fill="#e3cf90")
    art_draw.text((18, 38), "GFX_idea_maritime_industry · 72×64 · native pixels and 2× inspection", font=font, fill="#c4cdcb")
    art_proof.alpha_composite(maritime_image, (65, 100))
    art_proof.alpha_composite(maritime_image.resize((144, 128), Image.Resampling.NEAREST), (240, 85))
    art_proof.convert("RGB").save(OUT / "MARITIME_SPIRIT_ART.png")
    proofs.append(str((OUT / "MARITIME_SPIRIT_ART.png").relative_to(ROOT)))
    # One source-derived whole-tree proof and a native-scale crop that retains
    # the complete union, negative-x opening and the row-nine left neighbours.
    overview = render(nodes, "OVERVIEW_NATIVE.png", f"COLDWAR UAE · installed current revision · {len(nodes)} focuses")
    overview.thumbnail((2200, 1800), Image.Resampling.LANCZOS)
    overview.convert("RGB").save(OUT / "OVERVIEW.png")
    proofs.append(str((OUT / "OVERVIEW.png").relative_to(ROOT)))
    neighbours = [n for n in nodes if n["group"] in {"union", "british", "left"}]
    render(neighbours, "UNION_LEFT_NEIGHBOURS.png", "Union, British opening and adjacent left programme · native scale")
    development_neighbours = [n for n in nodes if n["group"] in {"commerce", "oil", "diplomacy"}]
    render(development_neighbours, "INDUSTRIAL_NEIGHBOURS.png", "Industrial extension with oil and diplomacy neighbours · native scale")

    files = [focus_path, loc_path, programme_loc_path, gfx_path, shine_path,
             "common/dynamic_modifiers/COLDWAR_UAE_1970_programmes.txt",
             "common/scripted_effects/COLDWAR_UAE_1970_focus_effects.txt",
             "common/scripted_effects/COLDWAR_UAE_1970_programmes.txt",
             "common/scripted_triggers/COLDWAR_UAE_1970_focus_triggers.txt",
             "common/scripted_triggers/COLDWAR_UAE_1970_politics_triggers.txt",
             "common/scripted_triggers/IMP_cold_war_scenario_triggers.txt",
             "common/scripted_effects/COLDWAR_UAE_1970_politics_effects.txt",
             "tools/uae_1970/revision.py", "tools/uae_1970/presentation.py", "tools/uae_1970/development.py", "tools/uae_1970/maritime.py",
             "tools/uae_1970/streamline.py", "tools/uae_1970/focus_only.py", "tools/uae_1970/flags.py"]
    report = dict(scope="Installed focus/cards/narrative; diplomacy and engine behaviour not certified",
                  approved_sha256=sha(approved_path), revision_sha256=sha(revision_path),
                  explicitly_authorized_revision_changes=revision_changes, errors=errors, warnings=warnings,
                  user_correction_source_checks=revision_checks,
                  focuses=len(nodes), relative_anchors=sum(bool(n["anchor"]) for n in nodes),
                  groups=len(data["groups"]), native_title_max=max(width(n["title"], glyphs, kernings) for n in nodes),
                  geometry_prerequisites_exclusions_durations_titles_art_match=not errors,
                  modifier_and_treasury_preview_values_checked=True,
                  emitted_numeric_preview_contexts=numeric_cases,
                  preview_contract="Prospective programme rows remain visible under currently ineligible governments/statuses; real guards remain in the live reconciler. True future agreement terms carry TT_IF_THEY_ACCEPT. No focus checks treasury, while native costs remain. Maritime rewards use the current retained share; oil previews show only marginal losses of existing coastal contributions. Caps and starting-spirit changes remain marginal.",
                  starting_spirits=len(data["starting_spirits"]),
                  maritime_spirit_art={"sprite": "GFX_idea_maritime_industry", "texture": maritime_texture,
                      "size": list(maritime_image.size), "sha256": sha(ROOT / maritime_texture)},
                  unrelated_visible_card_intersections=len(collisions),
                  engine_checked=False, proofs=proofs, source_hashes={path: sha(ROOT / path) for path in files},
                  inherited_asset_hashes={str(p): sha(p) for p in [bar_path, GAME / "gfx/fonts/hoi_16mbs.fnt", GAME / "gfx/fonts/hoi_16mbs.dds"]})
    (OUT / "LAYOUT_REVIEW.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OUT / "FOCUS_MANIFEST.json").write_text(json.dumps(nodes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
