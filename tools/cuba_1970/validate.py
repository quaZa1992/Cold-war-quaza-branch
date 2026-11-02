# IMPERIA COLD WAR — Cuba 1970 independent implementation validator.
"""Compare the emitted Cuba focus tree with the approved snapshot using the Vietnam AST parser."""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools" / "vietnam_1970"))
from script_ast import first, parse, values, walk  # noqa: E402

PREFIX = "COLDWAR_CUB_"
SNAPSHOT_PATH = HERE / "approved_design.json"  # immutable pre-foreign baseline
APPROVAL_PATH = HERE / "approval.json"
CONCEPT_PATH = HERE / "revision_design.json"
CONCEPT_APPROVAL_PATH = HERE / "revision_approval.json"
FOCUS_PATH = ROOT / "common" / "national_focus" / "COLDWAR_CUB_1970_focus.txt"
REPORT_PATH = HERE / "IMPLEMENTATION_VALIDATION.json"
TRIGGER_PATH = ROOT / "common" / "scripted_triggers" / "COLDWAR_CUB_1970_triggers.txt"
EFFECT_PATH = ROOT / "common" / "scripted_effects" / "COLDWAR_CUB_1970_effects.txt"
DYNAMIC_PATH = ROOT / "common" / "dynamic_modifiers" / "COLDWAR_CUB_1970_dynamic_modifiers.txt"
IDEAS_PATH = ROOT / "common" / "ideas" / "COLDWAR_CUB_1970_ideas.txt"
GFX_PATH = ROOT / "interface" / "COLDWAR_CUB_1970.gfx"
LOC_PATH = ROOT / "localisation" / "english" / "COLDWAR_CUB_1970_l_english.yml"

# Native MD ruling-party slot predicates. These are the semantic equivalent of
# the old custom numeric party counter and are independently enumerated here.
PARTY_SLOT_TRIGGERS = {
    0: "western_autocrats_are_in_power",
    1: "western_conservatism_are_in_power",
    2: "western_liberals_are_in_power",
    3: "western_social_democrats_are_in_power",
    4: "emerging_communist_state_are_in_power",
    5: "emerging_anarchist_communism_are_in_power",
    6: "emerging_reactionaries_are_in_power",
    7: "emerging_autocracy_are_in_power",
    13: "neutrality_neutral_autocracy_are_in_power",
    18: "neutrality_neutral_social_are_in_power",
    19: "neutrality_neutral_communism_are_in_power",
    20: "nationalist_right_wing_populists_are_in_power",
    22: "nationalist_military_junta_are_in_power",
}

errors: list[str] = []
checks = 0


def check(ok: bool, message: str) -> None:
    global checks
    checks += 1
    if not ok:
        errors.append(message)


def scalar(value):
    if isinstance(value, str) and len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def number(value, label):
    try:
        return float(value)
    except (TypeError, ValueError):
        errors.append(f"Not a numeric {label}: {value!r}")
        return math.nan


def read_ast(path):
    if not path.exists():
        errors.append(f"Missing dependency file: {path.relative_to(ROOT)}")
        return []
    raw_file = path.read_bytes()
    check(not raw_file.startswith(b"\xef\xbb\xbf"), f"Script file has UTF-8 BOM: {path.relative_to(ROOT)}")
    try:
        return parse(raw_file.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        errors.append(f"Cannot parse {path.relative_to(ROOT)}: {exc}")
        return []


def block_map(rows):
    return {k: v for k, _, v in rows if k != "_bare" and isinstance(v, list)}


def normalized(v):
    try:
        return float(scalar(v))
    except (TypeError, ValueError):
        return scalar(v)


snapshot_bytes = SNAPSHOT_PATH.read_bytes()
baseline = json.loads(snapshot_bytes.decode("utf-8-sig"))
approval = json.loads(APPROVAL_PATH.read_text(encoding="utf-8-sig"))
snapshot_hash = hashlib.sha256(snapshot_bytes).hexdigest()
check(snapshot_hash == approval.get("approved_design_sha256"),
      "Approved design snapshot hash differs from approval.json")

# The foreign-policy concept is the authorization for the 120-focus redesign.
# Keep the old snapshot immutable and use it as the source of truth for surviving
# nodes, merge donors, starting ideas, and compatibility receipts.
concept_bytes = CONCEPT_PATH.read_bytes()
snapshot = json.loads(concept_bytes.decode("utf-8-sig"))
concept_approval = json.loads(CONCEPT_APPROVAL_PATH.read_text(encoding="utf-8-sig"))
concept_hash = hashlib.sha256(concept_bytes).hexdigest()
check(CONCEPT_PATH.relative_to(ROOT).as_posix() == concept_approval.get("approved_design"),
      "Foreign concept approval points at a different design file")
check(concept_hash == concept_approval.get("sha256"),
      "Approved foreign concept hash differs from foreign_approval.json")
check(snapshot.get("source_snapshot_sha256") == snapshot_hash,
      "Revision concept is not based on the immutable approved snapshot")
parent_approval = json.loads((HERE / "foreign_approval.json").read_text(encoding="utf-8-sig"))
check(snapshot.get("parent_concept_sha256") == parent_approval.get("sha256") ==
      concept_approval.get("parent_concept_sha256"),
      "Revision does not bind the previously approved foreign concept")

# IMPERIA COLD WAR — Preserve the approved snapshot while checking the authorized repair overlay.
from layout_repair import apply_layout_repair
import generic_navy
snapshot = apply_layout_repair(snapshot)

nodes = snapshot["nodes"]
approved = {n["id"]: n for n in nodes}
baseline_by_key = {n["key"]: n for n in baseline["nodes"]}
approved_by_key = {n["key"]: n for n in nodes}
check(len(nodes) == len(approved), "Duplicate IDs in approved design")
check(len(nodes) == concept_approval.get("focuses", 120) == 120,
      "Approved foreign concept is not the authorized 120-focus tree")
check(all(key.startswith(PREFIX) for key in approved),
      "Unexpected focus ID prefix in approved foreign concept")
check(len(baseline["nodes"]) == approval.get("focuses") == 120,
      "Immutable baseline snapshot is not the original authorized 120-focus tree")
foreign_nodes = [n for n in nodes if n["group"] == "foreign"]
partner_nodes = [n for n in foreign_nodes if n.get("partner")]
check(len(foreign_nodes) == 27, f"Expected 27 foreign focuses; found {len(foreign_nodes)}")
check(len(partner_nodes) == 23, f"Expected 23 partnered offer focuses; found {len(partner_nodes)}")
check(sum(1 for n in nodes if n["group"] == "pcc") == 13,
      "Approved 13-focus Fidel/PCC branch changed")
expected_group_counts = {"foreign": 27, "pcc": 13, "economy": 8, "society": 4, "defence": 5}
actual_group_counts = Counter(n["group"] for n in nodes)
for group, expected_count in expected_group_counts.items():
    check(actual_group_counts[group] == expected_count,
          f"Approved focus count for {group} changed: {actual_group_counts[group]} != {expected_count}")

# The DDR choice must be parallel to Soviet assistance, with ratification after
# either island agreement and both further accords after ratification.
def prereq_groups(key):
    return approved_by_key[key].get("prerequisites", [])

check(prereq_groups("foreign_symbolic") == [] and prereq_groups("foreign_cession") == [],
      "DDR island agreements are no longer independent foreign-policy roots")
check(set(prereq_groups("foreign_ddr")[0]) == {
          PREFIX + "foreign_symbolic", PREFIX + "foreign_cession"},
      "Berlin and Havana is not available after either island agreement")
for key in ("foreign_ddr_industry", "foreign_ddr_science"):
    check(prereq_groups(key) == [[PREFIX + "foreign_ddr"]],
          f"DDR follow-up {key} is not downstream of Berlin and Havana")

# Native focus cards are 165px wide on a 96px focus grid. Check the entire
# approved canvas for same-row collisions, including the newly parallel roots.
same_row = {}
for node in nodes:
    x, y = node["xy"]
    for other_x, other_id in same_row.setdefault(y, []):
        check(abs(x - other_x) * 96 >= 165,
              f"Native cards overlap on row {y}: {other_id} and {node['id']}")
    same_row[y].append((x, node["id"]))

# Independently reconcile the authored consolidation plan against the baseline.
merge_sources = {source.strip() for m in snapshot.get("merges", [])
                 for source in m["source"].split("+")}
merge_targets = {key for m in snapshot.get("merges", []) for key in m.get("targets", [])}
baseline_keys = set(baseline_by_key)
concept_keys = set(approved_by_key)
removed_keys = baseline_keys - concept_keys
replaced_foreign_keys = {n["key"] for n in baseline["nodes"] if n["group"] == "foreign"}
expected_removed = merge_sources | replaced_foreign_keys
check(removed_keys == expected_removed,
      f"Removed baseline focuses differ from approved merge sources: {sorted(removed_keys ^ expected_removed)}")
check(concept_keys & baseline_keys == baseline_keys - expected_removed,
      "Surviving original focus set differs from approved merge plan")
check(len(merge_targets) > 0 and merge_targets <= concept_keys,
      "A merge target is absent from the approved concept")
for merge in snapshot.get("merges", []):
    source_names = [source.strip() for source in merge["source"].split("+")]
    donors = [baseline_by_key.get(source) for source in source_names]
    check(all(donors), f"Merge source is not in immutable baseline: {merge['source']}")
    if merge.get("relocated"):
        check(set(merge.get("targets", [])) <= concept_keys,
              f"Relocated focus targets are missing: {merge['source']}")
        continue
    if len(donors) == 1 and donors[0]:
        donor = donors[0]
        check(donor["days"] == merge.get("days"),
              f"Merge donor duration differs from baseline: {merge['source']}")
        check(donor.get("effects", []) == merge.get("effects", []),
              f"Merge donor effects differ from baseline: {merge['source']}")
        check(donor.get("modifiers", {}) == merge.get("modifiers", {}),
              f"Merge donor modifiers differ from baseline: {merge['source']}")

# The user-approved 120-focus revision adds exactly two consolidation sources.
# Keep their existing identities in the merge metadata so old saves retain the
# same rewards through the original receipts.
expected_revision_merges = {
    "harvest_accounts": {"finish_zafra", "restore_sectors"},
    "health_workforce": {"medical_brigades", "retain_doctors"},
}
actual_revision_merges = {
    merge["source"]: set(merge.get("targets", []))
    for merge in snapshot.get("merges", [])
    if merge["source"] in expected_revision_merges
}
check(actual_revision_merges == expected_revision_merges,
      f"New budget consolidations differ from approval: {actual_revision_merges}")
merge_targets_by_donor = {}
for merge in snapshot.get("merges", []):
    if merge.get("relocated"):
        continue
    for target in merge.get("targets", []):
        merge_targets_by_donor.setdefault(target, []).append(merge["source"])
for target, donors in merge_targets_by_donor.items():
    node = approved_by_key.get(target)
    base = baseline_by_key.get(target)
    if node is None or base is None:
        continue
    expected_sources = sorted(donors)
    check(sorted(node.get("consolidated_from", [])) == expected_sources,
          f"Merged focus {target} does not list every source receipt: {node.get('consolidated_from')}")
    donor_nodes = [baseline_by_key[source] for source in donors]
    expected_cost = base["cost"] + sum(donor["cost"] for donor in donor_nodes)
    expected_days = base["days"] + sum(donor["days"] for donor in donor_nodes)
    check(node["cost"] == expected_cost and node["days"] == expected_days,
          f"Merged focus {target} does not preserve all source cost/duration: "
          f"{node['cost']}/{node['days']} != {expected_cost}/{expected_days}")

# Reused defence focuses retain their original rewards and add only the
# approved Cuban-side Guantánamo approaches. Capacity is checked per province;
# every granted fort level still receives its matching shared state slot.
expected_fortitions = {
    "coastal_patrols": [
        ("bunker", 2, 855, 7590),
        ("coastal_bunker", 1, 855, 7590),
    ],
    "civil_military_pact": [
        ("bunker", 1, 855, 9603),
        ("coastal_bunker", 1, 855, 9603),
        ("coastal_bunker", 1, 855, 7590),
    ],
}
for key, expected_forts in expected_fortitions.items():
    node = approved_by_key[key]
    base = baseline_by_key[key]
    check(node["cost"] == base["cost"] + 3 and node["days"] == base["days"] + 21,
          f"Guantánamo focus {key} does not add the approved cost and 21-day duration")
    check(node.get("modifiers", {}) == base.get("modifiers", {}),
          f"Guantánamo focus {key} changed its original persistent modifiers")
    base_effects = Counter(json.dumps(effect, sort_keys=True) for effect in base.get("effects", []))
    new_effects = Counter(json.dumps(effect, sort_keys=True) for effect in node.get("effects", []))
    check(all(new_effects[item] >= amount for item, amount in base_effects.items()),
          f"Guantánamo focus {key} dropped an original reward")
    declared = node.get("additional_effects", [])
    forts = [(e.get("building"), int(e.get("level", 0)), int(e.get("state", 0)),
              int(e.get("province", 0)))
             for e in declared if e.get("kind") == "building"]
    check(forts == expected_forts,
          f"Guantánamo focus {key} has an unexpected fortification target/level: {forts}")
    check(any(e.get("kind") == "treasury" and e.get("amount") == -0.20
              for e in declared) if key == "coastal_patrols" else
          any(e.get("kind") == "treasury" and e.get("amount") == -0.45
              for e in declared),
          f"Guantánamo focus {key} omits its additional treasury cost")

building_defs = read_ast(ROOT / "common" / "buildings" / "00_buildings.txt")
for building in ("bunker", "coastal_bunker"):
    definitions = [body for name, _, body in walk(building_defs)
                   if name == building and isinstance(body, list)]
    province_caps = [first(first(body, "level_cap", []), "province_max")
                     for body in definitions if first(body, "level_cap") is not None]
    check("7" in province_caps,
          f"Native {building} does not declare province_max = 7")

if not FOCUS_PATH.exists():
    print(json.dumps({
        "status": "waiting_for_emitted_tree",
        "approved_focuses": len(nodes),
        "approved_sha256": snapshot_hash,
        "expected_output": str(FOCUS_PATH),
    }, indent=2))
    raise SystemExit(0)

raw = FOCUS_PATH.read_bytes()
check(not raw.startswith(b"\xef\xbb\xbf"), "Focus script has UTF-8 BOM")
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError as exc:
    errors.append(f"Focus script is not valid UTF-8: {exc}")
    text = raw.decode("utf-8", errors="replace")

try:
    root_ast = parse(text)
except ValueError as exc:
    errors.append(f"Focus parser error: {exc}")
    root_ast = []

tree = first(root_ast, "focus_tree", [])
tree_id = scalar(first(tree, "id"))
focuses = values(tree, "focus")
actual_by: dict[str, list] = {}
earlier_focus_ids: set[str] = set()
for focus in focuses:
    focus_id = scalar(first(focus, "id"))
    if not focus_id:
        errors.append("Focus block is missing id")
        continue
    if focus_id in actual_by:
        errors.append(f"Duplicate emitted focus ID: {focus_id}")
    anchor = scalar(first(focus, "relative_position_id"))
    if anchor:
        check(anchor in earlier_focus_ids,
              f"Relative anchor is declared after its child focus: {focus_id} -> {anchor}")
    actual_by[focus_id] = focus
    earlier_focus_ids.add(focus_id)

check(len(focuses) == 120 + len(generic_navy.IDS), f"Expected 120 Cuban focuses and 26 imported focuses; found {len(focuses)}")
check(set(actual_by) == set(approved) | generic_navy.IDS,
      "Emitted focus ID set differs from the Cuban core and authorized generic naval copy")

# Close over every custom Cuba completed-focus predicate in loaded script
# providers, including kept legacy providers that can still inspect saved flags.
completed_focus_refs = 0
for search_root in (ROOT / "common", ROOT / "events"):
    if not search_root.is_dir():
        continue
    for provider in search_root.rglob("*.txt"):
        try:
            raw_text = provider.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        if PREFIX not in raw_text or "has_completed_focus" not in raw_text:
            continue
        code_text = re.sub(r"(?m)#.*$", "", raw_text)
        for match in re.finditer(r"\bhas_completed_focus\s*=\s*\"?(COLDWAR_CUB_[A-Za-z0-9_]+)\"?", code_text):
            focus_ref = match.group(1)
            completed_focus_refs += 1
            check(focus_ref in actual_by,
                  f"Dangling custom has_completed_focus reference in {provider.relative_to(ROOT)}: {focus_ref}")

resolved: dict[str, tuple[float, float]] = {}
active: set[str] = set()


def resolve(focus_id: str) -> tuple[float, float]:
    if focus_id in resolved:
        return resolved[focus_id]
    if focus_id in active:
        raise ValueError(f"Cyclic relative anchor at {focus_id}")
    if focus_id not in actual_by:
        raise ValueError(f"Missing focus/anchor {focus_id}")
    active.add(focus_id)
    focus = actual_by[focus_id]
    x = number(first(focus, "x"), f"x for {focus_id}")
    y = number(first(focus, "y"), f"y for {focus_id}")
    anchor = scalar(first(focus, "relative_position_id"))
    if anchor:
        ax, ay = resolve(anchor)
        x += ax
        y += ay
    active.remove(focus_id)
    resolved[focus_id] = (x, y)
    return x, y


for focus_id, expected in approved.items():
    actual = actual_by.get(focus_id)
    if actual is None:
        continue
    check(scalar(first(actual, "id")) == focus_id, f"ID changed: {focus_id}")
    expected_anchor = expected.get("anchor")
    actual_anchor = scalar(first(actual, "relative_position_id"))
    check(actual_anchor == expected_anchor,
          f"Relative anchor differs for {focus_id}: {actual_anchor!r} != {expected_anchor!r}")
    expected_local = expected.get("local_xy") if expected_anchor else expected.get("xy")
    actual_local = (number(first(actual, "x"), f"x for {focus_id}"),
                    number(first(actual, "y"), f"y for {focus_id}"))
    check(tuple(map(float, expected_local)) == actual_local,
          f"Local coordinates differ for {focus_id}: {actual_local} != {expected_local}")
    try:
        actual_xy = resolve(focus_id)
        check(tuple(map(float, expected["xy"])) == actual_xy,
              f"Resolved coordinates differ for {focus_id}: {actual_xy} != {expected['xy']}")
    except ValueError as exc:
        errors.append(str(exc))

    actual_cost = number(first(actual, "cost"), f"cost for {focus_id}")
    check(actual_cost == number(expected["cost"], f"approved cost for {focus_id}"),
          f"Focus cost differs for {focus_id}")
    check(actual_cost * 7 == number(expected["days"], f"approved days for {focus_id}"),
          f"Approved duration/cost conversion differs for {focus_id}")

    actual_prerequisites = [
        [scalar(value) for value in values(block, "focus")]
        for block in values(actual, "prerequisite")
    ]
    check(actual_prerequisites == expected.get("prerequisites", []),
          f"Prerequisite AND/OR groups differ for {focus_id}: {actual_prerequisites}")

    actual_exclusions = [
        scalar(value)
        for block in values(actual, "mutually_exclusive")
        for value in values(block, "focus")
    ]
    check(actual_exclusions == expected.get("mutually_exclusive", []),
          f"Mutual exclusions differ for {focus_id}: {actual_exclusions}")

    expected_icon = expected.get("icon")
    actual_icon = scalar(first(actual, "icon"))
    check(actual_icon == expected_icon, f"Focus icon differs for {focus_id}")
    check(not any(ch in focus_id for ch in (" ", "\t", "\r", "\n")),
          f"Malformed ID: {focus_id}")

# Audit actual reward previews, scripted guards/apply helpers, native icon lookup,
# and the English title/description references against the approved source data.
trigger_ast = read_ast(TRIGGER_PATH)
effect_ast = read_ast(EFFECT_PATH)
dynamic_ast = read_ast(DYNAMIC_PATH)
ideas_ast = read_ast(IDEAS_PATH)
gfx_ast = read_ast(GFX_PATH)
trigger_defs = {k: v for k, _, v in trigger_ast if k != "_bare"}
effect_defs = {k: v for k, _, v in effect_ast if k != "_bare"}
dynamic_defs = {k: v for k, _, v in dynamic_ast if k != "_bare"}
idea_defs = {k: v for k, _, v in ideas_ast if k != "_bare"}
if "ideas" in idea_defs:
    idea_defs = {k: v for k, _, v in values(idea_defs["ideas"], "country")[0] if k != "_bare"}
sprite_defs = {
    scalar(first(sprite, "name")): scalar(first(sprite, "texturefile"))
    for sprite in values(gfx_ast, "spriteType")
    if first(sprite, "name") and first(sprite, "texturefile")
}
sprite_registry = dict(sprite_defs)
source_roots = [Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV"),
                Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649"), ROOT]
for provider in source_roots:
    interface = provider / "interface"
    if not interface.is_dir():
        continue
    for gfx_file in interface.glob("*.gfx"):
        try:
            gfx_text = gfx_file.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        for match in re.finditer(r"(?i)spritetype\s*=\s*\{([^{}]*)\}", gfx_text, re.S):
            name = re.search(r'\bname\s*=\s*"([^"]+)"', match.group(1))
            texture = re.search(r'(?i)\btexturefile\s*=\s*"([^"]+)"', match.group(1))
            if name and texture:
                sprite_registry[name.group(1)] = texture.group(1).replace("\\", "/")

loc_raw = LOC_PATH.read_bytes() if LOC_PATH.exists() else b""
check(bool(loc_raw), "Missing generated English localisation file")
check(loc_raw.startswith(b"\xef\xbb\xbf"), "English localisation file is missing UTF-8 BOM")
try:
    loc_text = loc_raw.decode("utf-8-sig")
except UnicodeDecodeError as exc:
    errors.append(f"English localisation is not UTF-8: {exc}")
    loc_text = ""
loc_values = {}
for line in loc_text.splitlines():
    match = re.match(r'^\s*([^\s:]+):\d+\s+"(.*)"\s*$', line)
    if match:
        loc_values[match.group(1)] = match.group(2).replace('\\"', '"')

# Index the English localisation providers used by the local tree and MD.
# Preview rows may intentionally use generic MD tooltip keys rather than CUB keys.
loc_catalog = {}
loc_roots = [ROOT / "localisation" / "english",
             Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/localisation/english"),
             Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV/localisation/english")]
for loc_root in loc_roots:
    if not loc_root.is_dir():
        continue
    for loc_file in loc_root.rglob("*.yml"):
        try:
            for line in loc_file.read_text(encoding="utf-8-sig").splitlines():
                match = re.match(r'^\s*([^\s:]+):(?:\d+)?\s+"(.*)"\s*$', line)
                if match:
                    loc_catalog[match.group(1)] = match.group(2).replace('\\"', '"')
        except (OSError, UnicodeDecodeError):
            continue
loc_catalog.update(loc_values)


def tooltip_localisation_key(row):
    value = row[2]
    if isinstance(value, list):
        key = first(value, "localization_key") or first(value, "tooltip")
        return scalar(key) if key is not None else None
    return scalar(value)


def conditional_effect_signatures(rows, effect_key, effect_value=None):
    """Return (effect value, branch has_idea conditions) for direct if branches."""
    found = []
    for key, _, body in rows:
        if not isinstance(body, list):
            continue
        if key in ("if", "else_if", "else"):
            direct = [scalar(value) for child, _, value in body if child == effect_key]
            if effect_value is None:
                matched = bool(direct)
            else:
                matched = effect_value in direct
            if matched:
                limit = first(body, "limit", [])
                ideas = tuple(sorted(scalar(value) for child, _, value in walk(limit)
                                     if child == "has_idea"))
                found.append((tuple(direct), ideas))
        found.extend(conditional_effect_signatures(body, effect_key, effect_value))
    return found

def flatten_pairs(rows, key):
    return [(k, normalized(v)) for k, _, v in walk(rows) if k == key]


def expected_effect_facts(node):
    """Build simple required code facts from the approved typed reward records."""
    facts = []
    for item in node.get("effects", []):
        kind = item["kind"]
        if kind in ("treasury", "debt"):
            var = "treasury_change" if kind == "treasury" else "debt_change"
            fn = "modify_treasury_effect" if kind == "treasury" else "modify_debt_effect"
            facts += [("set_temp_variable", (var, float(item["amount"]))), (fn, None)]
        elif kind == "stability":
            facts.append(("add_stability", float(item["amount"])))
        elif kind == "building":
            facts.append(("add_building_construction", (item["building"], int(item["level"]),
                                                         int(item["state"]), item.get("province"))))
        elif kind == "research":
            facts.append(("add_tech_bonus", (float(item["bonus"]), int(item["uses"]), item["category"])))
        elif kind == "doctrine":
            facts.append(("add_doctrine_cost_reduction", (float(item["bonus"]), int(item["uses"]), item["category"])))
        elif kind == "experience":
            for branch in ("army", "navy", "air"):
                if item.get(branch):
                    facts.append((branch + "_experience", float(item[branch])))
        elif kind == "law":
            facts.append((item["helper"], "law"))
        elif kind == "offer":
            facts.append((PREFIX + "offer_" + item["contract"], None))
        elif kind == "relations":
            for target in item["targets"]:
                facts.append(("add_opinion_modifier", (target, PREFIX + "opinion_" + str(item["value"]))))
        elif kind == "harvest_course":
            course = "rebalance" if item["course"] == "rebalance" else "mobilisation"
            facts.append(("set_country_flag", PREFIX + "harvest_" + course))
        elif kind == "enterprise_reform":
            facts.append(("remove_ideas", "COLDWAR_CUB_revolutionary_offensive"))
        elif kind == "rename_island":
            facts.append(("set_state_name", PREFIX + "ernst_thaelmann_island"))
        elif kind == "contract_followup":
            facts.append(("set_country_flag", PREFIX + "island_use_protocol_published"))
        elif kind == "transition_charter":
            facts.append(("add_timed_idea", ("COLDWAR_CUB_transition_charter", 365)))
    return facts


def source_receipt_guarded(rows, flag):
    """The legacy donor receipt must gate its reward, not merely be stamped."""
    for key, _, body in walk(rows):
        if key != "if" or not isinstance(body, list):
            continue
        limit = first(body, "limit", [])
        if any(k == "has_country_flag" and scalar(v) == flag
               for k, _, v in walk(limit)) and any(k == "NOT" for k, _, _ in walk(limit)):
            return True
    return False


def effect_fact_present(rows, fact_key, fact):
    """Minimal AST matcher used to confirm each approved merge component."""
    for k, _, body in walk(rows):
        if k != fact_key:
            continue
        if fact_key in ("set_temp_variable",):
            if isinstance(body, list) and first(body, fact[0]) is not None and normalized(first(body, fact[0])) == fact[1]:
                return True
        elif fact_key == "add_building_construction" and isinstance(body, list):
            province = first(body, "province")
            province_matches = (province is None if fact[3] is None
                                else normalized(province) == int(fact[3]))
            if (scalar(first(body, "type")) == fact[0]
                    and normalized(first(body, "level")) == fact[1]
                    and province_matches):
                return True
        elif fact_key in ("add_tech_bonus", "add_doctrine_cost_reduction") and isinstance(body, list):
            amount_key = "bonus" if fact_key == "add_tech_bonus" else "cost_reduction"
            if (normalized(first(body, amount_key)) == fact[0] and normalized(first(body, "uses")) == fact[1]
                    and scalar(first(body, "category")) == fact[2]):
                return True
        elif fact_key == "add_timed_idea" and isinstance(body, list):
            if scalar(first(body, "idea")) == fact[0] and normalized(first(body, "days")) == fact[1]:
                return True
        elif fact_key == "add_opinion_modifier" and isinstance(body, list):
            if scalar(first(body, fact[0])) is not None and scalar(first(first(body, fact[0]), "modifier")) == fact[1]:
                return True
        elif fact_key == "remove_ideas":
            if isinstance(body, list) and fact in [scalar(v) for kk, _, v in body if kk == "_bare"]:
                return True
            if scalar(body) == fact:
                return True
        elif fact_key == "set_country_flag" and scalar(body) == fact:
            return True
        elif fact_key == "set_state_name" and isinstance(body, list):
            if scalar(first(body, "1252")) == fact:
                return True
        elif fact_key.endswith("_experience") or fact_key == "add_stability":
            if normalized(body) == fact:
                return True
        elif fact_key in ("modify_treasury_effect", "modify_debt_effect") or fact_key.startswith(PREFIX + "offer_"):
            if scalar(body) == "yes":
                return True
        elif fact_key == "decrease_corruption" or fact_key.startswith("increase_"):
            if scalar(body) == "yes":
                return True
    return False


for focus_id, node in approved.items():
    focus = actual_by.get(focus_id)
    if focus is None:
        continue
    key = node["key"]
    reward = first(focus, "completion_reward", [])
    reward_keys = [k for k, _, _ in reward]
    check(reward_keys == ["log", "effect_tooltip", "hidden_effect"],
          f"Unexpected completion reward structure for {focus_id}: {reward_keys}")
    preview = first(reward, "effect_tooltip", [])
    hidden = first(reward, "hidden_effect", [])
    preview_calls = [scalar(v) for k, _, v in walk(preview) if k.startswith(PREFIX + "apply_")]
    check(not preview_calls, f"Executable Cuba apply helper appears in preview for {focus_id}: {preview_calls}")
    check(scalar(first(hidden, PREFIX + "apply_" + key)) == "yes",
          f"Hidden reward does not call its matching apply helper for {focus_id}")
    check(sum(1 for k, _, _ in walk(hidden) if k.startswith(PREFIX + "apply_")) == 1,
          f"Hidden reward contains unexpected/multiple apply calls for {focus_id}")

    # The preview is expected to contain the exact approved dynamic-modifier deltas.
    preview_mods = {}
    for row in values(preview, "add_to_variable"):
        for k, _, v in row:
            if k.startswith(PREFIX):
                preview_mods[k] = number(v, f"preview modifier {k}")
    expected_mods = {PREFIX + node["group"] + "_" + mod: float(value)
                     for mod, value in node.get("modifiers", {}).items()}
    check(preview_mods == expected_mods,
          f"Preview modifier set/value differs from approved reward for {focus_id}: {preview_mods} != {expected_mods}")

    # Every native variable modifier tooltip must resolve to an English key and
    # use the engine's RIGHT-value formatter rather than a hand-written delta.
    for add_row in values(preview, "add_to_variable"):
        for variable, _, _ in add_row:
            if not variable.startswith(PREFIX):
                continue
            tooltip_key = scalar(first(add_row, "tooltip"))
            tooltip_text = loc_catalog.get(tooltip_key)
            check(bool(tooltip_key and tooltip_text),
                  f"Missing English modifier tooltip {tooltip_key!r} for {focus_id}/{variable}")
            check(bool(tooltip_text and re.search(r"\$RIGHT\|[^$]+\$", tooltip_text)),
                  f"Modifier tooltip lacks native RIGHT-value formatting: {tooltip_key!r} for {focus_id}/{variable}")

    # Check every explicit tooltip key in the display-only reward. This includes
    # the shared MD dynamic-modifier heading and any deliberately concise CUB line.
    for preview_key, _, value in walk(preview):
        if preview_key != "custom_effect_tooltip":
            continue
        tooltip_key = tooltip_localisation_key((preview_key, "=", value))
        check(bool(tooltip_key and tooltip_key in loc_catalog),
              f"Missing English custom preview tooltip {tooltip_key!r} for {focus_id}")

    # Law previews mirror the live helper/cap branch, including Cuba's own
    # efficiency ideas at the ceiling. This guards against tooltip/runtime drift.
    law_caps = {
        "decrease_corruption": ("COLDWAR_CUB_oversight_efficiency", "corruption_level_01",
                                [f"corruption_level_{i:02d}" for i in range(2, 11)]),
        "increase_education_budget": ("COLDWAR_CUB_education_efficiency", "edu_05",
                                      [f"edu_{i:02d}" for i in range(1, 5)]),
        "increase_healthcare_budget": ("COLDWAR_CUB_health_efficiency", "health_06",
                                       [f"health_{i:02d}" for i in range(1, 6)]),
    }
    for law in (item for item in node.get("effects", []) if item["kind"] == "law"):
        helper = law["helper"]
        cap_idea, cap_level, helper_levels = law_caps[helper]
        preview_helper = conditional_effect_signatures(preview, helper, "yes")
        # The live helper is keyed per focus. Resolve it here directly because
        # the broader apply variable is assigned later in this validation pass.
        live_apply = effect_defs.get(PREFIX + "apply_" + node["key"], [])
        live_helper = conditional_effect_signatures(live_apply, helper, "yes")
        preview_cap = conditional_effect_signatures(preview, "add_ideas", cap_idea)
        live_cap = conditional_effect_signatures(live_apply, "add_ideas", cap_idea)
        expected_helper_condition = (tuple(sorted(helper_levels)),)
        expected_cap_condition = ((cap_level,),)
        check(len(preview_helper) == 1 and preview_helper == live_helper,
              f"Law preview does not match live {helper} branch for {focus_id}: {preview_helper} != {live_helper}")
        check(len(preview_helper) == 1 and preview_helper[0][1] == expected_helper_condition[0],
              f"Law preview {helper} tier conditions differ for {focus_id}: {preview_helper}")
        check(len(preview_cap) == 1 and preview_cap == live_cap,
              f"Law cap preview does not match live {cap_idea} branch for {focus_id}: {preview_cap} != {live_cap}")
        check(len(preview_cap) == 1 and preview_cap[0][1] == expected_cap_condition[0],
              f"Law cap condition differs for {focus_id}: expected {cap_level}, found {preview_cap}")

    obsolete_law_tooltips = {
        PREFIX + "decrease_corruption_reward_tt",
        PREFIX + "increase_education_budget_reward_tt",
        PREFIX + "increase_healthcare_budget_reward_tt",
    }
    for obsolete_key in obsolete_law_tooltips:
        check(obsolete_key not in loc_values,
              f"Obsolete hand-formatted law summary remains in English localisation: {obsolete_key}")
        check(not any(key == "custom_effect_tooltip" and scalar(value) == obsolete_key
                      for key, _, value in walk(preview)),
              f"Obsolete hand-formatted law summary remains in focus preview: {focus_id}/{obsolete_key}")

    # Partnered foreign focuses open a recipient offer. They must preview the
    # paired terms in effect_tooltip and emit the offer only from hidden_effect.
    if node.get("partner"):
        offer_name = PREFIX + "foreign_offer_" + key.removeprefix("foreign_")
        apply_name = PREFIX + "apply_" + key
        apply = effect_defs.get(apply_name, [])
        check(bool(apply), f"Missing partnered focus apply helper {apply_name}")
        hidden_calls = [(k, scalar(v)) for k, _, v in walk(apply)
                        if k == offer_name]
        check(hidden_calls == [(offer_name, "yes")],
              f"Foreign apply helper must issue one matching offer: {focus_id} -> {hidden_calls}")
        visible_calls = [k for k, _, _ in walk(preview) if k == offer_name]
        check(not visible_calls, f"Foreign offer executes from display-only preview: {focus_id}")
        preview_ideas = [scalar(v) for k, _, v in walk(preview) if k == "add_ideas"]
        expected_ideas = (["COLDWAR_CUB_cmea_member",
                           "COLDWAR_CUB_foreign_" + key.removeprefix("foreign_") + "_partner"]
                          if key == "foreign_cmea" else
                          ["COLDWAR_CUB_foreign_" + key.removeprefix("foreign_") + "_cub",
                           "COLDWAR_CUB_foreign_" + key.removeprefix("foreign_") + "_partner"])
        if key == "foreign_limited":
            expected_ideas.append("COLDWAR_CUB_american_embargo_limited")
        check(set(preview_ideas) == set(expected_ideas),
              f"Foreign preview must show both counterpart spirits for {focus_id}: {preview_ideas}")
        check(not any(k.startswith(PREFIX + "apply_") for k, _, _ in walk(preview)),
              f"Foreign proposal executes an apply helper from display-only preview: {focus_id}")
        # The paired effect preview must show each side's setup cost.
        for amount in node.get("setup_costs", []):
            check(any(k in ("modify_treasury_effect", "modify_debt_effect")
                      for k, _, _ in walk(preview)),
                  f"Foreign offer preview omits numeric setup-cost effects: {focus_id}/{amount}")
        continue

    can_name = PREFIX + "can_" + key
    apply_name = PREFIX + "apply_" + key
    check(can_name in trigger_defs, f"Missing scripted availability guard {can_name}")
    check(apply_name in effect_defs, f"Missing scripted apply helper {apply_name}")
    trigger = trigger_defs.get(can_name, [])
    apply = effect_defs.get(apply_name, [])
    hidden_trigger = first(trigger, "hidden_trigger", [])
    internal_flags = {scalar(v) for k, _, v in walk(hidden_trigger) if k == "has_country_flag"}
    check(any(k == PREFIX + "is_1970" and scalar(v) == "yes" for k, _, v in walk(hidden_trigger)),
          f"Availability guard lacks hidden 1970 scenario routing for {focus_id}")
    check(PREFIX + key + "_applied" in internal_flags,
          f"Availability guard lacks one-time applied receipt exclusion for {focus_id}")
    expected_parent_groups = [set(PREFIX + approved[parent]["key"] + "_applied" for parent in group)
                              for group in node.get("prerequisites", [])]
    actual_or_groups = [set(scalar(v) for kk, _, v in walk(block) if kk == "has_country_flag")
                        for block in values(hidden_trigger, "OR")]
    check(actual_or_groups == expected_parent_groups,
          f"Hidden receipt AND/OR groups differ for {focus_id}: {actual_or_groups} != {expected_parent_groups}")
    slot = node.get("slot")
    if slot is not None:
        try:
            slot_number = int(slot)
        except (TypeError, ValueError):
            slot_number = -1
        native_party_predicate = PARTY_SLOT_TRIGGERS.get(slot_number)
        has_numeric_slot = any(k == "check_variable" and first(v, "ruling_party") == str(slot)
                               for k, _, v in walk(trigger))
        has_native_slot = bool(native_party_predicate and any(
            k == native_party_predicate and scalar(v) == "yes" for k, _, v in walk(trigger)))
        check(has_native_slot or has_numeric_slot,
              f"Availability guard lacks exact native ruling-party slot {slot} for {focus_id}")
    if key in expected_fortitions:
        check(any(k == "owns_state" and normalized(v) == 855 for k, _, v in walk(trigger)),
              f"Guantánamo fortification availability does not require Cuban ownership of State 855: {focus_id}")
        check(any(k == "controls_state" and normalized(v) == 855 for k, _, v in walk(trigger)),
              f"Guantánamo fortification availability does not require Cuban control of State 855: {focus_id}")
        expected_capacity = (
            [("bunker", 2, 7590), ("coastal_bunker", 1, 7590)]
            if key == "coastal_patrols" else
            [("bunker", 1, 9603), ("coastal_bunker", 1, 9603), ("coastal_bunker", 1, 7590)]
        )
        capacity_rows = [body for name, _, body in walk(trigger)
                         if name == "free_building_slots" and isinstance(body, list)]
        for building, level, province in expected_capacity:
            found = any(
                scalar(first(body, "building")) == building
                and normalized(first(body, "province")) == province
                and any(name == "size" and op == ">" and normalized(value) == level - 1
                        for name, op, value in body)
                for body in capacity_rows
            )
            check(found,
                  f"Guantánamo fortification lacks per-province native capacity for {building} {level} at {province}: {focus_id}")
    # Infrastructure grants use MD's state infrastructure cap. A raw free-slot
    # check rejects merged alternatives that themselves add one shared slot;
    # require the state-level cap guard and keep the paid construction reward.
    for building_effect in (effect for effect in node.get("effects", [])
                            if effect.get("kind") == "building"
                            and effect.get("building") == "infrastructure"):
        state_id = str(building_effect["state"])
        state_trigger = first(trigger, state_id, [])
        has_infrastructure_cap = any(
            key == "building_level@infrastructure" and op == "<"
            and normalized(value) == 6
            for key, op, value in walk(state_trigger)
        )
        check(has_infrastructure_cap,
              f"Infrastructure grant lacks the MD state cap guard building_level@infrastructure < 6 for {focus_id}/{state_id}")
    apply_limit = first(first(apply, "if", []), "limit", [])
    check(any(k == can_name and scalar(v) == "yes" for k, _, v in walk(apply_limit)),
          f"Apply helper does not recheck its matching guard for {focus_id}")
    applied_stamps = [scalar(v) for k, _, v in walk(apply) if k == "set_country_flag"]
    check(applied_stamps.count(PREFIX + key + "_applied") == 1,
          f"Apply helper must stamp exactly one matching applied receipt for {focus_id}")

    # Compare the approved direct effects to the real helper code. Dynamic modifiers
    # are covered separately by preview-vs-approved deltas and sync-programme checks.
    real_pairs = list(walk(apply))
    for fact_key, fact in expected_effect_facts(node):
        if fact_key in ("set_temp_variable",):
            seen = False
            for _, _, block in real_pairs:
                if isinstance(block, list):
                    for temp in values(block, fact_key):
                        if first(temp, fact[0]) is not None and normalized(first(temp, fact[0])) == fact[1]:
                            seen = True
            check(seen, f"Missing or incorrect {fact_key} {fact} in real reward for {focus_id}")
        elif fact_key == "add_building_construction":
            found = False
            for state in (str(fact[2]),):
                for k, _, body in real_pairs:
                    if k == state:
                        for b in values(body, fact_key):
                            found |= (scalar(first(b, "type")) == fact[0] and
                                      normalized(first(b, "level")) == fact[1] and
                                      (first(b, "province") is None if fact[3] is None else
                                       normalized(first(b, "province")) == int(fact[3])))
            check(found, f"Missing or incorrect building reward {fact} for {focus_id}")
        elif fact_key in ("add_tech_bonus", "add_doctrine_cost_reduction"):
            found = False
            for body in (v for k, _, v in real_pairs if k == fact_key):
                amount_key = "bonus" if fact_key == "add_tech_bonus" else "cost_reduction"
                found |= (normalized(first(body, amount_key)) == fact[0] and
                          normalized(first(body, "uses")) == fact[1] and
                          scalar(first(body, "category")) == fact[2])
            check(found, f"Missing or incorrect research reward {fact} for {focus_id}")
        elif fact_key == "add_timed_idea":
            found = any(scalar(first(body, "idea")) == fact[0] and normalized(first(body, "days")) == fact[1]
                        for body in (v for k, _, v in real_pairs if k == fact_key))
            check(found, f"Missing or incorrect timed idea reward {fact} for {focus_id}")
        elif fact_key == "add_opinion_modifier":
            target, modifier = fact
            found = any(k == target and scalar(first(first(v, fact_key), "modifier")) == modifier
                        for k, _, v in real_pairs)
            check(found, f"Missing opinion reward {fact} for {focus_id}")
        elif fact_key == "remove_ideas":
            found = any((scalar(body) == fact) if not isinstance(body, list) else
                        fact in [scalar(v) for k, _, v in body if k == "_bare"]
                        for k, _, body in real_pairs if k == "remove_ideas")
            check(found, f"Missing idea removal {fact} for {focus_id}")
        elif fact_key == "set_state_name":
            found = any(k == "1252" and any(scalar(v) == fact for v in values(body, fact_key))
                        for k, _, body in real_pairs)
            check(found, f"Missing state rename {fact} for {focus_id}")
        elif fact_key == "set_country_flag":
            check(fact in applied_stamps, f"Missing follow-up flag {fact} for {focus_id}")
        elif fact_key == "decrease_corruption" or fact_key.startswith("increase_"):
            check(any(k == fact_key and scalar(v) == "yes" for k, _, v in real_pairs),
                  f"Missing law helper {fact_key} for {focus_id}")
        elif fact_key.endswith("_experience"):
            check(any(k == fact_key and normalized(v) == fact for k, _, v in real_pairs),
                  f"Missing experience reward {fact_key}={fact} for {focus_id}")
        elif fact_key == "add_stability":
            check(any(k == fact_key and normalized(v) == fact for k, _, v in real_pairs),
                  f"Missing stability reward {fact} for {focus_id}")
        elif fact_key in ("modify_treasury_effect", "modify_debt_effect") or fact_key.startswith(PREFIX + "offer_"):
            check(any(k == fact_key and scalar(v) == "yes" for k, _, v in real_pairs),
                  f"Missing effect call {fact_key} for {focus_id}")

    # Compare intended spelling of legacy mis-decoded names and separators
    # in the immutable preview while retaining all prose and gameplay.
    def intended_spelling(text):
        text = text.replace('\u00e2\u20ac\u201c', '\u2013').replace('\u00c2\u00b7', '\u00b7')
        return re.sub(r'\u00c3[\u0080-\u00bf]',
                      lambda match: match[0].encode('latin-1').decode('utf-8'), text)
    check(loc_values.get(focus_id) == intended_spelling(node.get("native_title")), f"Localised title mismatch for {focus_id}")
    check(loc_values.get(focus_id + "_desc") == intended_spelling(node.get("description")),
          f"Localised description mismatch for {focus_id}")
    check(node.get("icon") in sprite_registry,
          f"Focus icon has no declared spriteType in game/MD/workspace registry: {node.get('icon')} ({focus_id})")

# Removed policy rewards remain independently identifiable components. Each
# recipient applies its bundle once, guarded by the original receipt, so an old
# save that earned the donor does not receive it again after the redesign.
for merge in snapshot.get("merges", []):
    if merge.get("relocated"):
        continue
    source = merge["source"]
    donor = baseline_by_key[source]
    receipt = PREFIX + source + "_applied"
    for target in merge["targets"]:
        target_node = approved_by_key[target]
        apply_name = PREFIX + "apply_" + target
        apply = effect_defs.get(apply_name)
        check(apply is not None, f"Missing merged-reward recipient helper {apply_name}")
        if apply is None:
            continue
        check(source_receipt_guarded(apply, receipt),
              f"Merged reward {source}->{target} is not guarded by the old-save receipt {receipt}")
        check(sum(1 for k, _, v in walk(apply) if k == "set_country_flag" and scalar(v) == receipt) == 1,
              f"Merged reward {source}->{target} must stamp its old-save receipt once")
        for fact_key, fact in expected_effect_facts(donor):
            check(effect_fact_present(apply, fact_key, fact),
                  f"Merged reward {source}->{target} omits donor effect {fact_key} {fact}")

# Programme dynamic modifiers and ideas must have definitions corresponding to all
# authored policy buckets and starting/replacement spirits.
for group in snapshot.get("groups", []):
    ident = PREFIX + group["id"] + "_programme"
    check(ident in dynamic_defs, f"Missing dynamic modifier definition {ident}")
    if ident in dynamic_defs:
        enabled = first(dynamic_defs[ident], "enable", [])
        check(any(k == PREFIX + "is_1970" and scalar(v) == "yes" for k, _, v in walk(enabled)),
              f"Dynamic modifier {ident} lacks 1970 enable guard")
        expected_fields = {(field, PREFIX + group["id"] + "_" + field)
                           for n in nodes if n["group"] == group["id"]
                           for field in n.get("modifiers", {})}
        actual_fields = {(k, scalar(v)) for k, _, v in dynamic_defs[ident]
                         if not isinstance(v, list) and (k, scalar(v)) in expected_fields}
        check(actual_fields == expected_fields,
              f"Dynamic modifier {ident} field-to-variable mapping differs: {actual_fields} != {expected_fields}")
for spirit in baseline.get("starting_spirits", []):
    check(spirit["id"] in idea_defs, f"Missing starting idea definition {spirit['id']}")

# The actual persistent modifier grants are recomputed from applied receipts in
# sync_programmes. Check their exact multiset and the receipt/party context of each.
sync = effect_defs.get(PREFIX + "sync_programmes", [])
sync_body = first(first(sync, "if", []), "limit", [])
check(any(k == PREFIX + "is_1970" and scalar(v) == "yes" for k, _, v in walk(sync_body)),
      "sync_programmes lacks its scenario guard")
check(any(k == "has_country_flag" and scalar(v) == PREFIX + "initialized"
          for k, _, v in walk(sync_body)), "sync_programmes lacks initialization guard")

def guarded_additions(rows, flags=frozenset(), slots=frozenset()):
    for key, _, value in rows:
        if not isinstance(value, list):
            continue
        if key == "if":
            limit = first(value, "limit", [])
            child_flags = flags | frozenset(scalar(v) for k, _, v in walk(limit) if k == "has_country_flag")
            child_slots = slots | frozenset(scalar(first(v, "ruling_party"))
                                             for k, _, v in walk(limit) if k == "check_variable")
            child_slots |= frozenset(str(slot) for slot, predicate in PARTY_SLOT_TRIGGERS.items()
                                      if any(k == predicate and scalar(v) == "yes"
                                             for k, _, v in walk(limit)))
            yield from guarded_additions(value, child_flags, child_slots)
        elif key == "add_to_variable":
            for var, _, amount in value:
                if var.startswith(PREFIX):
                    yield var, normalized(amount), flags, slots
        else:
            yield from guarded_additions(value, flags, slots)

actual_sync = Counter((var, amount) for var, amount, _, _ in guarded_additions(sync))
# Runtime sync keeps original recipient modifiers and adds each merged donor as
# its own component under the donor's preserved receipt. Compare that emitted
# component multiset rather than the concept's deliberately aggregated display.
expected_sync = Counter()
for n in nodes:
    baseline_node = baseline_by_key.get(n["key"])
    base_modifiers = baseline_node.get("modifiers", {}) if baseline_node else n.get("modifiers", {})
    expected_sync.update((PREFIX + n["group"] + "_" + mod, float(amount))
                         for mod, amount in base_modifiers.items())
for merge in snapshot.get("merges", []):
    if merge.get("relocated"):
        continue
    donor = baseline_by_key[merge["source"]]
    expected_sync.update((PREFIX + donor["group"] + "_" + mod, float(amount))
                         for mod, amount in donor.get("modifiers", {}).items())
for legacy_key in ("expeditionary_forces", "mission_schools"):
    donor = baseline_by_key[legacy_key]
    expected_sync.update((PREFIX + donor["group"] + "_" + mod, float(amount))
                         for mod, amount in donor.get("modifiers", {}).items())
check(actual_sync == expected_sync,
      f"sync_programmes modifier values differ from approved focus data: missing={expected_sync-actual_sync}, extra={actual_sync-expected_sync}")

for merge in snapshot.get("merges", []):
    if merge.get("relocated"):
        continue
    donor = baseline_by_key[merge["source"]]
    receipt = PREFIX + merge["source"] + "_applied"
    for modifier, amount in donor.get("modifiers", {}).items():
        variable = PREFIX + donor["group"] + "_" + modifier
        check(any(var == variable and value == float(amount) and receipt in flags
                  for var, value, flags, _ in guarded_additions(sync)),
              f"sync drops donor modifier {merge['source']} under saved receipt {receipt}: {variable}={amount}")

# The old overseas/missions-school receipts continue contributing until one of
# the two replacement foreign-force programmes is completed. Preserve the old
# doctrine benefit once, while a newly completed route avoids double payment.
for legacy_key in ("expeditionary_forces", "mission_schools"):
    donor = baseline_by_key[legacy_key]
    receipt = PREFIX + legacy_key + "_applied"
    for modifier, amount in donor.get("modifiers", {}).items():
        variable = PREFIX + donor["group"] + "_" + modifier
        matches = [(var, value, flags, slots) for var, value, flags, slots in guarded_additions(sync)
                   if var == variable and value == float(amount) and receipt in flags]
        check(bool(matches), f"sync drops legacy posture modifier {legacy_key}: {variable}={amount}")
        check(all(PREFIX + "foreign_advisers_applied" in flags and
                  PREFIX + "foreign_expeditionary_applied" in flags for _, _, flags, _ in matches),
              f"legacy posture modifier {legacy_key} does not stop after either replacement focus")
guarded_rows = list(guarded_additions(sync))
for n in nodes:
    baseline_node = baseline_by_key.get(n["key"])
    base_modifiers = baseline_node.get("modifiers", {}) if baseline_node else n.get("modifiers", {})
    for modifier, amount in base_modifiers.items():
        variable = PREFIX + n["group"] + "_" + modifier
        matching = [row for row in guarded_rows if row[0] == variable and row[1] == float(amount)]
        receipt = PREFIX + n["key"] + "_applied"
        check(any(receipt in row[2] and (n.get("slot") is None or str(n["slot"]) in row[3])
                  for row in matching),
              f"Persistent modifier contribution lacks matching applied receipt/party slot: {n['id']} {modifier}")

# Verify the sprite references emitted for programme ideas resolve to actual texture files.
texture_roots = [ROOT, Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649"),
                 Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV")]
for sprite in values(gfx_ast, "spriteType"):
    texture = scalar(first(sprite, "texturefile"))
    if texture:
        check(any((base / texture).is_file() for base in texture_roots),
              f"Custom programme sprite texture is missing: {texture}")

# Reciprocal MEX is required for a symmetric exclusive choice and is not implied by
# having a one-sided edge.
for focus_id, expected in approved.items():
    for peer in expected.get("mutually_exclusive", []):
        check(peer in approved, f"Unknown approved MEX peer {peer} from {focus_id}")
        if peer in approved:
            check(focus_id in approved[peer].get("mutually_exclusive", []),
                  f"Approved MEX is not reciprocal: {focus_id} / {peer}")
            if peer in actual_by:
                check(focus_id in [
                    scalar(v)
                    for block in values(actual_by[peer], "mutually_exclusive")
                    for v in values(block, "focus")
                ], f"Emitted MEX is not reciprocal: {focus_id} / {peer}")

for focus_id in actual_by:
    resolve(focus_id)
positions = list(resolved.values())
check(len(positions) == len(set(positions)),
      "Two emitted focuses resolve to the same grid position")

title_counts = Counter(scalar(first(f, "id")) for f in focuses)
check(not [key for key, count in title_counts.items() if count != 1],
      "One or more emitted focus IDs are not unique")

# MD's structured timed flags need an explicit nonzero value. Otherwise a
# pending offer/refusal or provisional charter is invisible to has_country_flag.
# IMPERIA COLD WAR — Building grants and their previews include matching state slots.
for folder in ('common/national_focus', 'common/scripted_effects', 'common/decisions', 'events'):
    for provider in (ROOT / folder).glob('COLDWAR_CUB_1970*.txt'):
        for effect, _, payload in walk(parse(provider.read_text(encoding='utf-8'))):
            if isinstance(payload, list):
                for index, (command, _, construction) in enumerate(payload):
                    if command == 'add_building_construction':
                        level = float(first(construction, 'level'))
                        building_type = scalar(first(construction, 'type'))
                        province = first(construction, 'province')
                        slots = sum(float(amount) for name, _, amount in payload[:index]
                                    if name == 'add_extra_state_shared_building_slots')
                        if building_type in ('bunker', 'coastal_bunker') and province is not None:
                            check(level <= 7,
                                  f'Province fortification exceeds native province_max 7: {provider.name}/{effect}/{province}')
                            check(slots == level,
                                  f'Province fortification lacks exactly matching shared slots: {provider.name}/{effect}/{province} ({slots} for {level})')
                        else:
                            check((effect.isdigit() or effect in ('capital_scope', 'every_controlled_state')) and slots >= level,
                                  f'Building grant lacks matching preceding slots in state scope: {provider.name}/{effect}')
            if effect == 'set_country_flag' and isinstance(payload, list) and first(payload, 'days') is not None:
                check(first(payload, 'value') == '1',
                      f'Timed country flag lacks explicit value=1 in {provider.name}: {first(payload, "flag")}')

report = {
    "project": "IMPERIA COLD WAR",
    "status": "pass" if not errors else "fail",
    "checks": checks,
    "errors": errors,
    "approved_snapshot_sha256": snapshot_hash,
    "approved_concept_sha256": concept_hash,
    "partnered_offer_focuses": len(partner_nodes),
    "focus_output_sha256": hashlib.sha256(raw).hexdigest(),
    "focus_tree_id": tree_id,
    "approved_focuses": len(approved),
    "imported_naval_and_feeder_focuses": len(generic_navy.IDS),
    "emitted_focuses": len(focuses),
    "unique_resolved_positions": len(set(positions)),
    "closed_custom_completed_focus_references": completed_focus_refs,
    "exclusive_pairs": len({
        tuple(sorted((n["id"], peer)))
        for n in nodes for peer in n.get("mutually_exclusive", [])
    }),
    "engine_tested": False,
}
REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(bool(errors))


