"""MD-style geometry and explicit dependency corrections for Greece 1970.

The reviewed JSON remains an untouched archive.  Call apply_layout(design) once,
immediately after loading it and before constructing NODES/BY in compile.py.
No rewards, costs, exclusions, event conditions or political gates are changed.
Run this file directly for a read-only structural validation report.
"""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs/greece_1970_design/coldwar_greece_1970_design.json"

# Russia 2000 has independent side-by-side policy and political sectors, not
# a stack of party templates above a second stack of general policy templates.
PARTY_ANCHORS = {
    "pap": 7, "ioa": 21, "royal": 35, "kke": 49,
    "pasok": 63, "centre": 77, "nd": 91,
}
POLICY_ANCHORS = {
    "economy": 146, "army": 168, "navy": 184,
    "air": 200, "foreign": 224, "aegean": 246, "cyprus": 266,
}

# These are existing MD filters, also used by 00_generic.txt.  Greece needs
# neither bespoke GUI assets nor Russian-specific labels to be searchable.
SECTION_FILTERS = {
    "economy": "FOCUS_FILTER_INDUSTRY",
    "army": "FOCUS_FILTER_EQUIPMENT",
    "navy": "FOCUS_FILTER_EQUIPMENT",
    "air": "FOCUS_FILTER_AIRCRAFT",
    "foreign": "FOCUS_FILTER_INFLUENCE",
    "aegean": "FOCUS_FILTER_INFLUENCE",
    "contingency": "FOCUS_FILTER_EXPENDITURE",
}

# A political constitution remains the prerequisite for party programmes.
# Economic and diplomatic programmes then run in parallel, with a fiscal and
# political settlement at the end.  Only genuine policy choices are exclusive.
PARTY_POSITIONS = {
    0: (0, 0), 1: (0, 1),
    2: (-2, 3), 3: (2, 3), 4: (-2, 4), 5: (2, 4),
    6: (0, 6), 7: (-4, 8),
    8: (-6, 10), 9: (-2, 10), 10: (-6, 11), 11: (-2, 11),
    12: (-4, 13), 13: (2, 8), 14: (6, 8),
    15: (2, 10), 16: (6, 10), 17: (4, 15),
    18: (-4, 15), 19: (0, 17),
}

# Opening and regime spine are deliberately central and initially visible.
REGIME_POSITIONS = {
    "greece_1970": (104, 0), "state_dossier": (104, 1),
    "officer_loyalties": (98, 2), "civilian_contacts": (104, 2),
    "economic_stocktake": (110, 2),
    "retain_junta": (96, 4), "controlled_opening": (104, 4),
    "civilian_transition": (112, 4), "military_compact": (96, 5),
    "professional_compact": (94, 6), "security_compact": (98, 6),
    "service_procurement": (94, 7), "security_budget": (98, 7),
    "lasting_junta": (96, 8), "military_development": (94, 10),
    "military_exit": (100, 13), "supervised_cabinet": (104, 5),
    "retain_veto": (102, 6), "renounce_veto": (106, 6),
    "tutelary_charter": (102, 7), "opening_handover": (106, 9),
    "opening_tourism": (104, 9), "reverse_opening": (108, 11),
    "transition_offer": (112, 5), "civilian_preparation": (112, 6),
    "legal_parties": (112, 7), "civilian_institutions": (110, 15),
    "civilian_accountability": (108, 16), "civilian_retirement": (112, 16),
    "open_courts": (108, 17), "retirement_guarantees": (112, 17),
    "credible_election": (110, 18), "constitutional_question": (110, 19),
    "civilian_enterprise": (108, 20), "civilian_reconstruction": (112, 20),
    "civilian_settlement": (110, 21),
}


def apply_layout(data):
    """Mutate layout/dependencies in place and return navigation/QA metadata.

    Prerequisite groups retain HOI4 semantics: alternatives inside one group,
    conjunction between groups.  External-response records stay independent
    roots: a foreign crisis must never wait for Greece to complete a survey.
    """
    nodes = data["focuses"]
    by = {node["key"]: node for node in nodes}
    prefix = data["prefix"]
    before = deepcopy(nodes)
    reasons = {}
    positions = {}

    def put(key, x, y):
        if key in positions:
            raise ValueError(f"Duplicate layout assignment: {key}")
        if key not in by:
            raise ValueError(f"Unknown layout focus: {key}")
        positions[key] = (x, y)
        by[key]["x"], by[key]["y"] = x, y

    def depend(key, *groups, reason):
        wanted = [[prefix + parent for parent in group] for group in groups]
        if wanted != by[key]["prerequisite_groups"]:
            by[key]["prerequisite_groups"] = wanted
            reasons[key] = reason

    def sector(name, geometry):
        anchor = POLICY_ANCHORS[name]
        for index, (dx, y) in geometry.items():
            put(f"{name}_{index}", anchor + dx, y)

    for key, (x, y) in REGIME_POSITIONS.items():
        put(key, x + 14, y)

    for party, anchor in PARTY_ANCHORS.items():
        for index, (dx, y) in PARTY_POSITIONS.items():
            put(f"{party}_{index}", anchor + dx, y)
        depend(f"{party}_13", [f"{party}_6"], reason=
               "Diplomatic strategy opens after the constitutional settlement; it does not require completion of the entire economic programme.")
        depend(f"{party}_14", [f"{party}_6"], reason=
               "The alternative diplomatic strategy shares the constitutional gate and retains its original exclusion.")
        depend(f"{party}_17", [f"{party}_12"], [f"{party}_15", f"{party}_16"], reason=
               "The final political settlement joins a funded domestic programme AND either chosen diplomatic strategy.")
        depend(f"{party}_18", [f"{party}_12"], reason=
               "Domestic administrative, regional and social follow-through depends on the fiscal settlement, independently of foreign acceptance.")
        depend(f"{party}_19", [f"{party}_17"], [f"{party}_18"], reason=
               "The final settlement follows both the political agreement and its domestic follow-through.")

    put("pasok_return_narrow", PARTY_ANCHORS["pasok"] - 2, 19)
    put("pasok_return_equal", PARTY_ANCHORS["pasok"] + 2, 19)

    # Three economic arms: manufacturing, rural development, tourism.  This
    # differs intentionally from defence's command spine and two delivery arms.
    sector("economy", {
        0: (0, 0), 1: (0, 1), 2: (-6, 3), 3: (-2, 3),
        4: (-6, 4), 5: (-2, 4), 6: (-4, 6), 7: (4, 3),
        8: (2, 5), 9: (6, 5), 10: (2, 6), 11: (6, 6),
        12: (4, 8), 13: (10, 3), 14: (14, 3),
        15: (10, 4), 16: (14, 4), 17: (12, 6),
        18: (-4, 10), 19: (8, 13),
    })
    depend("economy_7", ["economy_1"], reason=
           "Rural development is a parallel national programme, not a reward for finishing an industrial specialisation.")
    for key in ("economy_13", "economy_14"):
        depend(key, ["economy_1"], reason=
               "Tourism and coastal policy form a third economic arm, independent of the agricultural choice.")
    depend("economy_18", ["economy_6"], ["economy_12"], reason=
           "Tax collection joins the productive base and connected regional markets.")
    depend("economy_19", ["economy_18"], ["economy_17"], reason=
           "A resilient expansion combines revenue institutions with the selected tourism/coastal programme.")

    sector("army", {
        0: (0, 0), 1: (0, 1), 2: (-2, 3), 3: (2, 3),
        4: (-2, 4), 5: (2, 4), 6: (0, 6), 7: (-4, 8),
        8: (-6, 10), 9: (-2, 10), 10: (-6, 11), 11: (-2, 11),
        12: (-4, 13), 13: (2, 8), 14: (6, 8),
        15: (2, 10), 16: (6, 10), 17: (4, 13),
        18: (0, 15), 19: (0, 17),
    })
    for key in ("army_13", "army_14"):
        depend(key, ["army_6"], reason=
               "A credible command opens separate procurement and mainland-defence planning arms.")
    depend("army_18", ["army_12"], ["army_17"], reason=
           "Exercises validate both a funded mobilisation plan and maintainable equipment.")
    depend("army_19", ["army_18"], reason=
           "National doctrine incorporates the completed joint validation exercises.")

    sector("navy", {
        0: (0, 0), 1: (0, 1), 2: (-6, 3), 3: (-2, 3),
        4: (-6, 4), 5: (-2, 4), 6: (-4, 6), 7: (2, 3),
        8: (0, 5), 9: (4, 5), 10: (0, 6), 11: (4, 6),
        12: (2, 8), 13: (-6, 10), 14: (-2, 10),
        15: (-6, 11), 16: (-2, 11), 17: (-4, 13),
        18: (6, 11), 19: (0, 15),
    })
    depend("navy_7", ["navy_1"], reason=
           "Island support is planned alongside fleet doctrine, rather than being locked behind a fleet specialisation.")
    for key in ("navy_13", "navy_14"):
        depend(key, ["navy_6"], reason=
               "Merchant-marine policy is a separate fleet-linked arm; it does not require the naval base programme.")
    depend("navy_18", ["navy_6"], ["navy_12"], reason=
           "Rescue and damage control integrate the chosen fleet mission with the island support network.")
    depend("navy_19", ["navy_17"], ["navy_18"], reason=
           "Fleet sustainability joins merchant-marine planning and operational support.")

    sector("air", {
        0: (0, 0), 1: (0, 1), 2: (-6, 3), 3: (-2, 3),
        4: (-6, 4), 5: (-2, 4), 6: (-4, 6), 7: (2, 3),
        8: (0, 5), 9: (4, 5), 10: (0, 6), 11: (4, 6),
        12: (2, 8), 13: (-6, 10), 14: (-2, 10),
        15: (-6, 11), 16: (-2, 11), 17: (-4, 13),
        18: (6, 11), 19: (0, 15),
    })
    depend("air_7", ["air_1"], reason=
           "Technical training begins from the readiness audit, in parallel with the combat mission choice.")
    for key in ("air_13", "air_14"):
        depend(key, ["air_6"], reason=
               "Airfield concentration/dispersal follows the squadron mission; it does not wait for foreign instructor acceptance.")
    depend("air_18", ["air_6"], ["air_12"], reason=
           "The procurement budget joins the required squadron mission and a funded ground-crew programme.")
    depend("air_19", ["air_17"], ["air_18"], reason=
           "Maintainable aircraft combine operational availability and the procurement budget.")

    sector("foreign", {
        0: (0, 0), 1: (0, 1), 2: (-4, 3), 3: (0, 3),
        4: (-4, 4), 5: (0, 4), 6: (-4, 6), 7: (6, 3),
        8: (4, 5), 9: (8, 5), 10: (4, 6), 11: (8, 6),
        12: (6, 8), 13: (-12, 3), 14: (-8, 3),
        15: (-12, 4), 16: (-8, 4), 17: (-10, 6),
        18: (6, 10), 19: (-2, 13),
    })
    depend("foreign_6", ["foreign_4"], reason=
           "The European rehabilitation dossier requires independent monitoring, as its existing available_code already states; security exceptions cannot satisfy it.")
    depend("foreign_7", ["foreign_1"], reason=
           "American/NATO policy stays playable even when European rehabilitation is refused or barred by a security-state policy.")
    for key in ("foreign_13", "foreign_14"):
        depend(key, ["foreign_1"], reason=
               "Regional commercial diplomacy is independent of American base negotiations.")
    depend("foreign_18", ["foreign_12"], reason=
           "Funding the diplomatic service follows the documented allied commitments.")
    depend("foreign_19", ["foreign_17"], ["foreign_18"], reason=
           "Final delivery combines regional agreements and a funded diplomatic service; the distinct European dossier remains optional.")

    # Aegean and Cyprus retain their factual-event gates.  The Cyprus shelves
    # are intentionally not connected by fabricated focus-completion gates.
    sector("aegean", {
        0: (0, 0), 1: (0, 1), 2: (-2, 3), 3: (2, 3),
        4: (0, 5), 5: (-2, 7), 6: (2, 7), 7: (0, 9),
    })
    sector("cyprus", {
        0: (0, 0), 1: (0, 1), 2: (-2, 3), 3: (2, 3),
        4: (-2, 4), 5: (2, 4), 6: (6, 4),
        7: (0, 8), 8: (-2, 10), 9: (2, 10),
        10: (-2, 11), 11: (2, 11), 12: (0, 15),
        13: (-2, 17), 14: (2, 17), 15: (-2, 18),
        16: (2, 18), 17: (0, 22), 18: (-2, 24), 19: (2, 24),
    })
    contingency = {
        "energy_shock": (130, 21), "energy_ration": (128, 23),
        "energy_diversify": (132, 23), "energy_recovery": (130, 25),
        "credit_review": (140, 21), "credit_taxes": (138, 23),
        "credit_loan": (142, 23),
    }
    for key, (x, y) in contingency.items():
        put(key, x + 14, y)

    missing = set(by) - set(positions)
    if missing:
        raise ValueError(f"Unpositioned focuses: {sorted(missing)}")

    for node in nodes:
        # Keep section-local coordinates consistent for saved-preview consumers.
        section = node["section"]
        anchor = (PARTY_ANCHORS.get(section)
                  or POLICY_ANCHORS.get(section)
                  or (144 if section == "contingency" else 118))
        node["local_x"] = node["x"] - anchor
        node["local_y"] = node["y"]
        filters = [SECTION_FILTERS.get(section, "FOCUS_FILTER_POLITICAL")]
        if section in PARTY_ANCHORS and node["key"].rsplit("_", 1)[-1].isdigit():
            index = int(node["key"].rsplit("_", 1)[-1])
            if 7 <= index <= 12:
                filters.append("FOCUS_FILTER_INDUSTRY")
            elif 13 <= index <= 16:
                filters.append("FOCUS_FILTER_INFLUENCE")
        if node.get("treasury_cost_gdp_percent"):
            filters.append("FOCUS_FILTER_EXPENDITURE")
        if node.get("stability") or "stability_factor" in node.get("modifiers", {}):
            filters.append("FOCUS_FILTER_STABILITY")
        if any("research" in name for name in node.get("modifiers", {})):
            filters.append("FOCUS_FILTER_RESEARCH")
        node["search_filters"] = list(dict.fromkeys(filters))
    for section in data["sections"]:
        first = next(node for node in nodes if node["section"] == section["id"])
        section["anchor"] = [first["x"], first["y"]]

    extra_shortcuts = [
        {"key": "shortcut_civilian", "title": "Civilian government and elections", "target": prefix + "civilian_institutions"},
        {"key": "shortcut_cyprus_crisis", "title": "Cyprus: guarantor crisis response", "target": prefix + "cyprus_7"},
        {"key": "shortcut_cyprus_outcome", "title": "Cyprus: recorded outcome and civilian relief", "target": prefix + "cyprus_17"},
        {"key": "shortcut_credit", "title": "Credit and public financing", "target": prefix + "credit_review"},
    ]
    metadata = {
        "version": 1,
        "reference": "common/national_focus/05_russia.txt",
        "initial_show_position": {"focus": prefix + "greece_1970"},
        "continuous_focus_position": {"x": 11600, "y": 2300},
        "extra_shortcuts": extra_shortcuts,
        "prerequisite_overrides": reasons,
        "qa": validate_layout(data),
    }
    # Protect all gameplay payloads, including gates, contracts and exclusions.
    allowed = {"x", "y", "local_x", "local_y", "prerequisite_groups", "search_filters"}
    for old, new in zip(before, nodes):
        changed = {key for key in old.keys() | new.keys() if old.get(key) != new.get(key)}
        if changed - allowed:
            raise ValueError(f"Layout changed gameplay fields on {new['key']}: {changed - allowed}")
    return metadata


def validate_layout(data):
    """Check engine graph semantics, spatial clearance and exclusion safety.

    Structural reachability means that some internally consistent prerequisite
    choice exists.  It is not a claim that every historical/event gate is true
    in a running game.  Factual external-event gates are deliberately preserved.
    """
    nodes = data["focuses"]
    by_id = {node["id"]: node for node in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("Duplicate focus IDs")
    coordinates = Counter((node["x"], node["y"]) for node in nodes)
    duplicates = [xy for xy, count in coordinates.items() if count > 1]
    if duplicates:
        raise ValueError(f"Focus coordinate collisions: {duplicates}")
    spacing = []
    for row in {node["y"] for node in nodes}:
        ordered = sorted((node["x"], node["key"]) for node in nodes if node["y"] == row)
        for left, right in zip(ordered, ordered[1:]):
            spacing.append(right[0] - left[0])
            if right[0] - left[0] < 2:
                raise ValueError(f"Insufficient label clearance: {left[1]}, {right[1]}")
    for node in nodes:
        for group in node["prerequisite_groups"]:
            if not group:
                raise ValueError(f"Empty prerequisite group: {node['key']}")
            for parent in group:
                if parent not in by_id:
                    raise ValueError(f"Unknown prerequisite: {parent}")
                if by_id[parent]["y"] >= node["y"]:
                    raise ValueError(f"Upward/cyclic prerequisite: {parent} -> {node['id']}")

    # Backtracking is needed here: a plain graph walk incorrectly declares
    # an AND join requiring both mutually exclusive options reachable.
    exclusions = {node["id"]: set(node["excludes"]) for node in nodes}

    def choices(pending, selected):
        if not pending:
            return selected
        wanted, *remaining = pending
        if wanted in selected:
            return choices(remaining, selected)
        if any(other in exclusions[wanted] or wanted in exclusions[other] for other in selected):
            return None
        selected = selected | {wanted}
        groups = by_id[wanted]["prerequisite_groups"]

        def choose_group(index, accumulated):
            if index == len(groups):
                return choices(accumulated + remaining, selected)
            for option in groups[index]:
                result = choose_group(index + 1, accumulated + [option])
                if result is not None:
                    return result
            return None
        return choose_group(0, [])

    unreachable = [node["key"] for node in nodes if choices([node["id"]], set()) is None]
    if unreachable:
        raise ValueError(f"No exclusion-compatible prerequisite path: {unreachable}")

    # The closed-source renderer's exact elbow choice is not available here.
    # Check both source-side and target-side row gutters, allowing icons plus
    # label clearance (0.8 x units, 0.35 y units around each foreign focus).
    # This catches long connections running vertically through intervening
    # focuses even when all node coordinates themselves are unique.
    route_overlaps = {}
    for mode in ("source", "target"):
        overlaps = []
        for node in nodes:
            for group in node["prerequisite_groups"]:
                for parent_id in group:
                    parent = by_id[parent_id]
                    gutter = parent["y"] + 0.5 if mode == "source" else node["y"] - 0.5
                    segments = [
                        ((parent["x"], parent["y"] + 0.4), (parent["x"], gutter)),
                        ((parent["x"], gutter), (node["x"], gutter)),
                        ((node["x"], gutter), (node["x"], node["y"] - 0.4)),
                    ]
                    for other in nodes:
                        if other["id"] in (parent_id, node["id"]):
                            continue
                        for (x1, y1), (x2, y2) in segments:
                            if x1 == x2:
                                hit = (abs(other["x"] - x1) < 0.8
                                       and min(y1, y2) < other["y"] + 0.35
                                       and max(y1, y2) > other["y"] - 0.35)
                            else:
                                hit = (abs(other["y"] - y1) < 0.35
                                       and min(x1, x2) < other["x"] + 0.8
                                       and max(x1, x2) > other["x"] - 0.8)
                            if hit:
                                overlaps.append((parent["key"], node["key"], other["key"]))
                                break
        route_overlaps[mode] = len(overlaps)
        if overlaps:
            raise ValueError(f"Prerequisite lines cross focus bounds ({mode} gutters): {overlaps}")
    return {
        "focuses": len(nodes),
        "coordinate_collisions": len(duplicates),
        "minimum_same_row_spacing": min(spacing),
        "structurally_reachable": len(nodes) - len(unreachable),
        "max_y": max(node["y"] for node in nodes),
        "width": max(node["x"] for node in nodes) - min(node["x"] for node in nodes),
        "orthogonal_route_focus_overlaps": route_overlaps,
        "event_gated_roots": [node["key"] for node in nodes
                              if not node["prerequisite_groups"]
                              and node["section"] in ("cyprus", "contingency", "aegean")],
    }


if __name__ == "__main__":
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = apply_layout(design)
    print(json.dumps(result, indent=2))
