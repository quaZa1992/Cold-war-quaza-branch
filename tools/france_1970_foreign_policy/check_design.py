# IMPERIA COLD WAR — France foreign-policy proposal source checker.
"""Read-only structural/source checks for foreign_policy_design.json."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "tools/france_1970_foreign_policy/foreign_policy_design.json"
NEW_GROUPS = {"african_finance", "african_security", "arab_contracts", "global_partnerships"}
CAPS = {
    "industrial_complex": 50,
    "arms_factory": 35,
    "infrastructure": 6,
    "dockyard": 20,
    "air_base": 10,
    "offices": 50,
    "agriculture_district": 10,
    "fossil_powerplant": 20,
    "internet_station": 11,
}
DOCTRINES = {"land_doctrine", "air_doctrine", "naval_doctrine"}


def block_at(text: str, marker: str) -> str | None:
    pos = text.find(marker)
    if pos < 0:
        return None
    start = text.find("{", pos)
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return None


def history_states() -> dict[int, dict]:
    out = {}
    for path in (ROOT / "history/states").glob("*.txt"):
        match = re.match(r"(\d+)-", path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8-sig")
        state_id = int(match.group(1))
        hist = block_at(text, "history =") or ""
        date_block = block_at(text, "1970.1.1 =") or ""
        owner = re.search(r"\bowner\s*=\s*([A-Z0-9_]+)", date_block)
        if not owner:
            owner = re.search(r"\bowner\s*=\s*([A-Z0-9_]+)", hist)
        controller = re.search(r"\bcontroller\s*=\s*([A-Z0-9_]+)", date_block)
        if not controller:
            controller = re.search(r"\bcontroller\s*=\s*([A-Z0-9_]+)", hist)
        provinces_block = block_at(text, "provinces =") or ""
        provinces = {int(x) for x in re.findall(r"\b\d+\b", provinces_block)}
        buildings = {}
        for source in (hist, date_block):
            b = block_at(source, "buildings =") or ""
            found = defaultdict(int)
            for name, level in re.findall(r"^\s*([a-zA-Z_][\w]*)\s*=\s*(\d+)\s*$", b, re.M):
                found[name] += int(level)
            buildings.update(found)
        out[state_id] = {
            "file": path.relative_to(ROOT).as_posix(),
            "name": path.stem.split("-", 1)[1],
            "owner": owner.group(1) if owner else None,
            "controller": controller.group(1) if controller else None,
            "provinces": provinces,
            "buildings": buildings,
        }
    return out


def coastal_state_ids(states: dict[int, dict]) -> set[int]:
    """Resolve coastline from state province lists and provinces.bmp adjacency."""
    definitions = {}
    water = set()
    max_id = 0
    with (ROOT / "map/definition.csv").open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f, delimiter=";"):
            if len(row) < 5 or not row[0].isdigit():
                continue
            pid = int(row[0])
            rgb = tuple(map(int, row[1:4]))
            definitions[rgb] = pid
            max_id = max(max_id, pid)
            if row[4].lower() == "sea":
                water.add(pid)
    province_state = np.full(max_id + 1, -1, dtype=np.int32)
    for state_id, state in states.items():
        for province in state["provinces"]:
            if province <= max_id:
                province_state[province] = state_id
    lookup = np.zeros(1 << 24, dtype=np.int32)
    for rgb, pid in definitions.items():
        lookup[(rgb[0] << 16) | (rgb[1] << 8) | rgb[2]] = pid
    pixels = np.asarray(Image.open(ROOT / "map/provinces.bmp").convert("RGB"), dtype=np.uint32)
    encoded = (pixels[:, :, 0] << 16) | (pixels[:, :, 1] << 8) | pixels[:, :, 2]
    province_grid = lookup[encoded]
    state_grid = province_state[province_grid]
    water_grid = np.isin(province_grid, np.fromiter(water, dtype=np.int32))
    land_coast = np.zeros_like(water_grid)
    land_coast[:, 1:] |= water_grid[:, :-1]
    land_coast[:, :-1] |= water_grid[:, 1:]
    land_coast[1:, :] |= water_grid[:-1, :]
    land_coast[:-1, :] |= water_grid[1:, :]
    coastal_pixels = land_coast & (state_grid >= 0)
    return set(map(int, np.unique(state_grid[coastal_pixels])))


def add_issue(issues: list[str], text: str) -> None:
    issues.append(text)


def main() -> int:
    raw = DESIGN.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    digest = hashlib.sha256(raw).hexdigest()
    issues: list[str] = []
    notes: list[str] = []
    nodes = data["nodes"]
    node_by_key = {node["key"]: node for node in nodes}
    offers = [node for node in nodes if isinstance(node.get("offer"), dict)]
    new_offers = [node for node in offers if node["offer"].get("family", "").startswith("fp_")]
    new_nodes = [node for node in nodes if node.get("group") in NEW_GROUPS]
    added_keys = set(data.get("foreign_policy_added_keys", []))
    missing_keys = sorted(added_keys - node_by_key.keys())
    if missing_keys:
        add_issue(issues, f"Added focus keys missing from nodes: {missing_keys}")
    if len(new_nodes) != 36 or len(new_offers) != 32:
        add_issue(issues, f"Expected 36 nodes in four new groups and 32 new offers; got {len(new_nodes)} and {len(new_offers)}")
    additions_path = ROOT / "tools/france_1970_foreign_policy/ADDITIONS.json"
    additions = json.loads(additions_path.read_text(encoding="utf-8"))
    baseline = data.get("foreign_policy_baseline_sha256")
    if additions.get("baseline_sha256") != baseline:
        add_issue(issues, "ADDITIONS.json and proposal disagree about the frozen 176-focus baseline hash")

    # Source-backed native modifier and category names.
    source_roots = [ROOT / "common/ideas", ROOT / "common/dynamic_modifiers", ROOT / "common/modifiers", ROOT / "common/bop", ROOT / "common/scripted_effects"]
    code_text = "\n".join(p.read_text(encoding="utf-8-sig", errors="replace") for src in source_roots for p in src.rglob("*.txt"))
    categories_text = (ROOT / "common/technology_tags/00_technology.txt").read_text(encoding="utf-8-sig")
    categories = set(re.findall(r"\bCAT_[A-Za-z0-9_]+\b", categories_text))
    modifier_keys = {
        effect["key"]
        for node in new_offers
        for side in ("france", "recipient")
        for effect in node["offer"][side]["effects"]
        if effect.get("kind") == "modifier"
    }
    research_categories = {
        effect["category"]
        for node in new_offers
        for side in ("france", "recipient")
        for effect in node["offer"][side]["effects"]
        if effect.get("kind") == "research"
    }
    doctrine_categories = {
        effect["category"]
        for node in new_offers
        for side in ("france", "recipient")
        for effect in node["offer"][side]["effects"]
        if effect.get("kind") == "doctrine"
    }
    missing_modifiers = sorted(key for key in modifier_keys if not re.search(rf"\b{re.escape(key)}\b", code_text))
    missing_categories = sorted(research_categories - categories)
    missing_doctrines = sorted(doctrine_categories - DOCTRINES)
    if missing_modifiers:
        add_issue(issues, f"No native code provider/consumer occurrence found for modifier keys: {missing_modifiers}")
    if missing_categories:
        add_issue(issues, f"Research/doctrine category tags absent from native technology tags: {missing_categories}")
    if missing_doctrines:
        add_issue(issues, f"Unknown doctrine categories: {missing_doctrines}")

    families = defaultdict(list)
    for node in new_offers:
        offer = node["offer"]
        families[offer["family"]].append(node)
        if offer.get("delivery") != "recipient_acceptance_decision" or offer.get("no_expiry") is not True:
            add_issue(issues, f"{node['key']}: recipient consent or no-expiry contract is not explicit")
        if not offer.get("source_focus") or offer["source_focus"] != node["id"]:
            add_issue(issues, f"{node['key']}: source focus receipt does not point to its own focus")
        if offer.get("partner") in {"FRA", None}:
            add_issue(issues, f"{node['key']}: invalid named partner")
        if len(offer.get("historical_basis", "").split(";")) < 2:
            notes.append(f"{node['key']}: fewer than two historical source references in design metadata")

        # Every monetary literal in runtime conversion fields is within the engine precision contract.
        for side in ("france", "recipient"):
            for effect in offer[side]["effects"]:
                literal = effect.get("runtime_share_literal")
                if literal is not None and "." in literal and len(literal.rsplit(".", 1)[1]) > 5:
                    add_issue(issues, f"{node['key']} {side}: monetary runtime literal exceeds five decimals: {literal}")
                if effect.get("kind") in {"treasury_gdp", "weekly_gdp_expense", "weekly_transfer"}:
                    base_fraction = Decimal(str(effect.get("gdp_fraction", 0)))
                    share = Decimal(str(effect.get("percent", effect.get("annual_gdp_percent", 0)))) / Decimal(100)
                    if abs(base_fraction - share) > Decimal("0.00000001"):
                        add_issue(issues, f"{node['key']} {side}: GDP fraction differs from written percentage: {effect}")
                    if literal is None or abs(Decimal(literal) - base_fraction) > Decimal("0.00000001"):
                        add_issue(issues, f"{node['key']} {side}: runtime share literal differs from GDP fraction: {effect}")
                    if effect.get("base") != "gdp_total":
                        add_issue(issues, f"{node['key']} {side}: non-GDP basis on fiscal term: {effect}")
                if effect.get("kind") == "weekly_gdp_expense" and (
                    effect.get("valuation") != "weekly_recalculation" or effect.get("divisor") != 52 or effect.get("payer") != "own_country"
                ):
                    add_issue(issues, f"{node['key']} {side}: weekly programme expense is not own GDP / 52: {effect}")
                if effect.get("kind") == "treasury_gdp" and (
                    effect.get("valuation") != "at_payment" or effect.get("once") is not True or effect.get("payer") != "own_country"
                ):
                    add_issue(issues, f"{node['key']} {side}: setup cost is not own GDP once at payment: {effect}")
                if effect.get("kind") == "building":
                    if effect.get("slots") != effect.get("amount") or effect.get("slots_before_construction") is not True:
                        add_issue(issues, f"{node['key']} {side}: building level lacks matching prior extra slots: {effect}")
                if effect.get("kind") == "access":
                    if effect.get("relation") not in {"military_access", "docking_rights"} or effect.get("grantor") not in {"FRA", offer["partner"]} or effect.get("beneficiary") not in {"FRA", offer["partner"]} or effect.get("grantor") == effect.get("beneficiary"):
                        add_issue(issues, f"{node['key']} {side}: invalid bilateral access relation: {effect}")

        france_transfers = [e for e in offer["france"]["effects"] if e.get("kind") == "weekly_transfer"]
        partner_transfers = [e for e in offer["recipient"]["effects"] if e.get("kind") == "weekly_transfer"]
        if len(france_transfers) != 1 or len(partner_transfers) != 1:
            add_issue(issues, f"{node['key']}: expected one mirrored weekly transfer term on each signatory")
        elif france_transfers and partner_transfers:
            a, b = france_transfers[0], partner_transfers[0]
            fields = ("payer", "recipient", "annual_gdp_percent", "gdp_fraction", "runtime_share_literal", "divisor", "base", "valuation")
            if any(a.get(f) != b.get(f) for f in fields) or {a.get("flow"), b.get("flow")} != {"income", "expense"}:
                add_issue(issues, f"{node['key']}: weekly transfer pair is not same-basis and mirrored")
            if a.get("payer") not in {"FRA", offer["partner"]} or a.get("recipient") not in {"FRA", offer["partner"]}:
                add_issue(issues, f"{node['key']}: weekly transfer references a third country")
            if a.get("payer") == a.get("recipient"):
                add_issue(issues, f"{node['key']}: weekly transfer payer and recipient are identical")

    for family, members in families.items():
        if len(members) != 2:
            add_issue(issues, f"{family}: expected exactly two mutually exclusive packages, found {len(members)}")
            continue
        for i, node in enumerate(members):
            other = members[1-i]["key"]
            if other not in node.get("exclusions", []):
                add_issue(issues, f"{node['key']}: does not exclude sibling family choice {other}")

    all_families = defaultdict(list)
    for node in offers:
        all_families[node["offer"].get("family", node["key"])].append(node)

    # Named partner and recipient-state ownership are checked against January 1970 history.
    states = history_states()
    coastal = coastal_state_ids(states)
    asset_claims = defaultdict(lambda: defaultdict(int))
    for node in new_offers:
        offer = node["offer"]
        partner = offer["partner"]
        for side, expected_owner in (("france", "FRA"), ("recipient", partner)):
            for effect in offer[side]["effects"]:
                if effect.get("kind") == "resource_rights":
                    state_id = int(effect["state"])
                    state = states.get(state_id)
                    if not state or state["owner"] != effect.get("grantor"):
                        add_issue(issues, f"{node['key']}: resource-rights grantor {effect.get('grantor')} does not own state {state_id} in 1970")
                    if effect.get("beneficiary") not in {"FRA", partner}:
                        add_issue(issues, f"{node['key']}: resource-rights beneficiary is outside the agreement pair")
                if effect.get("kind") != "building":
                    continue
                state_id = int(effect["state"])
                state = states.get(state_id)
                if not state:
                    add_issue(issues, f"{node['key']}: target state {state_id} is missing from 1970 history")
                    continue
                if state["owner"] != expected_owner:
                    msg = f"{node['key']} {side}: state {state_id} ({state['name']}) is owned by {state['owner']} on 1970-01-01, expected {expected_owner}"
                    compact_conditions = [re.sub(r"\s+", " ", x).strip() for x in offer.get("activation_conditions", [])]
                    state_guard = re.compile(rf"{re.escape(expected_owner)} = \{{[^}}]*owns_state = {state_id}[^}}]*controls_state = {state_id}[^}}]*has_full_control_of_state = {state_id}[^}}]*\}}")
                    if any(state_guard.fullmatch(condition) for condition in compact_conditions):
                        notes.append(msg + "; explicit ownership/control activation guard verified")
                    else:
                        add_issue(issues, msg + "; acceptance and standing-activation guard must require recipient ownership and full control")
                if state["controller"] and state["controller"] != state["owner"]:
                    notes.append(f"{node['key']}: state {state_id} starts with controller {state['controller']} rather than owner {state['owner']}")
                if effect["building"] == "dockyard" and state_id not in coastal:
                    add_issue(issues, f"{node['key']} {side}: dockyard target {state_id} is not coastal by map adjacency")
                asset_claims[(expected_owner, state_id)][(node["offer"]["family"], effect["building"])]+=int(effect["amount"])

    # Check worst-case same-type construction across all mutually exclusive package families.
    # Family alternatives are maxed, not summed, before families are combined.
    family_assets = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    offer_families = defaultdict(list)
    for node in offers:
        family = node["offer"].get("family", node["key"])
        offer_families[family].append(node)
    for family, members in offer_families.items():
        candidate_maps = []
        for node in members:
            result = defaultdict(int)
            offer = node["offer"]
            for side, tag in (("france", "FRA"), ("recipient", offer["partner"])):
                for effect in offer[side]["effects"]:
                    if effect.get("kind") == "building":
                        result[(tag, int(effect["state"]), effect["building"])] += int(effect["amount"])
            candidate_maps.append(result)
        all_keys = set().union(*(m.keys() for m in candidate_maps)) if candidate_maps else set()
        for key in all_keys:
            family_assets[family][key] = max(m.get(key, 0) for m in candidate_maps)
    route_assets = defaultdict(int)
    for family, assets in family_assets.items():
        for key, amount in assets.items():
            route_assets[key] += amount
    for (tag, state_id, building), added in sorted(route_assets.items()):
        cap = CAPS.get(building)
        if cap is None:
            add_issue(issues, f"No verified state cap configured for {building} in state {state_id}")
            continue
        current = states.get(state_id, {}).get("buildings", {}).get(building, 0)
        if current + added > cap:
            add_issue(issues, f"Compatible offer-route upper bound exceeds {building} state cap: {tag} state {state_id}, start {current}, added {added}, cap {cap}")

    # Report comparative finance ceiling by choosing the more costly option in each new family.
    setup_ceiling = defaultdict(float)
    weekly_programme_ceiling = defaultdict(float)
    weekly_transfer_payer_ceiling = defaultdict(float)
    weekly_total_cost_ceiling = defaultdict(float)
    modifier_ranges = defaultdict(lambda: [0.0, 0.0])
    all_setup_ceiling = defaultdict(float)
    all_weekly_total_cost_ceiling = defaultdict(float)
    all_modifier_ranges = defaultdict(lambda: [0.0, 0.0])
    for family, members in families.items():
        candidates_setup = defaultdict(list)
        candidates_weekly = defaultdict(list)
        candidates_transfer = defaultdict(list)
        candidates_total_cost = defaultdict(list)
        candidates_modifiers = defaultdict(lambda: defaultdict(list))
        for node in members:
            offer = node["offer"]
            for side, tag in (("france", "FRA"), ("recipient", offer["partner"])):
                effects = offer[side]["effects"]
                candidates_setup[tag].append(sum(abs(float(e.get("percent", 0))) for e in effects if e.get("kind") == "treasury_gdp"))
                candidates_weekly[tag].append(sum(float(e.get("annual_gdp_percent", 0)) for e in effects if e.get("kind") == "weekly_gdp_expense"))
                payer_terms = [e for e in effects if e.get("kind") == "weekly_transfer" and e.get("payer") == tag]
                candidates_transfer[tag].append(sum(float(e.get("annual_gdp_percent", 0)) for e in payer_terms))
                transfer_cost = sum(float(e.get("annual_gdp_percent", 0)) for e in payer_terms if e.get("flow") == "expense")
                programme_cost = sum(float(e.get("annual_gdp_percent", 0)) for e in effects if e.get("kind") == "weekly_gdp_expense")
                candidates_total_cost[tag].append(programme_cost + transfer_cost)
                for effect in effects:
                    if effect.get("kind") == "modifier":
                        candidates_modifiers[tag][effect["key"]].append(float(effect["value"]))
            if node not in new_offers:
                continue
            # Each newly-added family is summarized independently below.
        for tag, values in candidates_setup.items():
            setup_ceiling[tag] += max(values, default=0)
        for tag, values in candidates_weekly.items():
            weekly_programme_ceiling[tag] += max(values, default=0)
        for tag, values in candidates_transfer.items():
            weekly_transfer_payer_ceiling[tag] += max(values, default=0)
        for tag, values in candidates_total_cost.items():
            weekly_total_cost_ceiling[tag] += max(values, default=0)
        for tag, by_key in candidates_modifiers.items():
            for key, values in by_key.items():
                modifier_ranges[(tag, key)][0] += min(values, default=0)
                modifier_ranges[(tag, key)][1] += max(values, default=0)

    for family, members in all_families.items():
        candidates_setup = defaultdict(list)
        candidates_total_cost = defaultdict(list)
        candidates_modifiers = defaultdict(lambda: defaultdict(list))
        for node in members:
            offer = node["offer"]
            for side, tag in (("france", "FRA"), ("recipient", offer["partner"])):
                effects = offer[side]["effects"]
                candidates_setup[tag].append(sum(abs(float(e.get("percent", 0))) for e in effects if e.get("kind") == "treasury_gdp"))
                transfer_cost = sum(float(e.get("annual_gdp_percent", 0)) for e in effects if e.get("kind") == "weekly_transfer" and e.get("payer") == tag and e.get("flow") == "expense")
                programme_cost = sum(float(e.get("annual_gdp_percent", 0)) for e in effects if e.get("kind") == "weekly_gdp_expense")
                candidates_total_cost[tag].append(programme_cost + transfer_cost)
                for effect in effects:
                    if effect.get("kind") == "modifier":
                        candidates_modifiers[tag][effect["key"]].append(float(effect["value"]))
        for tag, values in candidates_setup.items():
            all_setup_ceiling[tag] += max(values, default=0)
        for tag, values in candidates_total_cost.items():
            all_weekly_total_cost_ceiling[tag] += max(values, default=0)
        for tag, by_key in candidates_modifiers.items():
            for key, values in by_key.items():
                all_modifier_ranges[(tag, key)][0] += min(values, default=0)
                all_modifier_ranges[(tag, key)][1] += max(values, default=0)

    result = {
        "project": "IMPERIA COLD WAR",
        "design_path": DESIGN.relative_to(ROOT).as_posix(),
        "design_sha256": digest,
        "frozen_baseline_sha256": baseline,
        "nodes": len(nodes),
        "groups": len(data["groups"]),
        "added_focus_keys": len(added_keys),
        "new_partner_offers": len(new_offers),
        "new_families": len(families),
        "new_modifiers": sorted(modifier_keys),
        "new_research_categories": sorted(research_categories),
        "new_doctrine_categories": sorted(doctrine_categories),
        "new_route_setup_ceiling_percent_of_each_country_gdp": {k: round(v, 5) for k, v in sorted(setup_ceiling.items())},
        "new_route_weekly_programme_annual_gdp_share_percent_ceiling_by_country": {k: round(v, 5) for k, v in sorted(weekly_programme_ceiling.items())},
        "new_route_weekly_transfer_payer_annual_gdp_share_percent_ceiling_by_country": {k: round(v, 5) for k, v in sorted(weekly_transfer_payer_ceiling.items())},
        "new_route_combined_recurring_cost_annual_gdp_share_percent_ceiling_by_country": {k: round(v, 5) for k, v in sorted(weekly_total_cost_ceiling.items())},
        "new_route_modifier_range_by_country_and_key": {f"{tag}:{key}": [round(v[0], 5), round(v[1], 5)] for (tag, key), v in sorted(modifier_ranges.items())},
        "all_design_offers_setup_ceiling_percent_of_each_country_gdp": {k: round(v, 5) for k, v in sorted(all_setup_ceiling.items())},
        "all_design_offers_combined_recurring_cost_annual_gdp_share_percent_ceiling_by_country": {k: round(v, 5) for k, v in sorted(all_weekly_total_cost_ceiling.items())},
        "all_design_offers_modifier_range_by_country_and_key": {f"{tag}:{key}": [round(v[0], 5), round(v[1], 5)] for (tag, key), v in sorted(all_modifier_ranges.items())},
        "issues": list(dict.fromkeys(issues)),
        "notes": list(dict.fromkeys(notes)),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
