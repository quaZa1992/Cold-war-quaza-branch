# IMPERIA COLD WAR — Cyprus guarantor focus integration generator.
"""Emit shared focus definitions and host attachment/layout metadata.

This module owns the 16 Greek, Turkish and British supporting focus concepts.
Country-tree and runtime helpers are integrated by their respective owners.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = "common/national_focus/COLDWAR_CYP_R2_guarantor_focuses.txt"
PREFIX = "COLDWAR_CYP_R2_ACT_"

HOSTS = {
    "GRE": {
        "tag": "GRE",
        "tree_id": "COLDWAR_GRE_1970_focus",
        "host_path": "common/national_focus/COLDWAR_GRE_1970_focus.txt",
        "anchor": "COLDWAR_GRE_1970_foreign_0",
        "anchor_xy": (224, 0),
        "module_base": (264, 0),
        "source_generator": "tools/greece_1970/compile.py",
        "layout_source": "tools/greece_1970/layout.py",
        "module_keys": [
            "gre_officers", "gre_treaty", "gre_network", "gre_consult",
            "gre_withdraw", "gre_coup", "gre_response", "gre_volunteers",
            "gre_escalate",
        ],
    },
    "TUR": {
        "tag": "TUR",
        "tree_id": "mdcw_1970_generic_focus",
        "host_path": "common/national_focus/mdcw_1970_generic_focus.txt",
        "anchor": "GEN_1970_foreign_policy_review",
        "anchor_xy": (44, 13),
        "module_base": (32, 13),
        "source_generator": "Claude outputs/COLDWAR_GEN_generator/gen_focus.py",
        "layout_source": "Claude outputs/COLDWAR_GEN_generator/gen_build.py",
        "module_keys": ["tur_consult", "tur_terms", "tur_operation", "tur_abstain"],
    },
    "ENG": {
        "tag": "ENG",
        "tree_id": "mdcw_1970_generic_focus",
        "host_path": "common/national_focus/mdcw_1970_generic_focus.txt",
        "anchor": "GEN_1970_foreign_policy_review",
        "anchor_xy": (44, 13),
        "module_base": (33, 17),
        "source_generator": "Claude outputs/COLDWAR_GEN_generator/gen_focus.py",
        "layout_source": "Claude outputs/COLDWAR_GEN_generator/gen_build.py",
        "module_keys": ["eng_consult", "eng_mediation", "eng_restraint"],
    },
}

ICON_BY_KEY = {
    "gre_officers": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_treaty": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_network": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_consult": "GFX_COLDWAR_GRE_1970_diplomacy",
    "gre_withdraw": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_coup": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_response": "GFX_COLDWAR_GRE_1970_cyprus",
    "gre_volunteers": "GFX_COLDWAR_GRE_1970_army",
    "gre_escalate": "GFX_COLDWAR_GRE_1970_army",
    "tur_consult": "diplomacy",
    "tur_terms": "accept_treaty",
    "tur_operation": "naval_dockyard",
    "tur_abstain": "diplomatic_treaty",
    "eng_consult": "diplomacy",
    "eng_mediation": "accept_treaty",
    "eng_restraint": "diplomatic_treaty",
}

FILTERS_BY_KEY = {
    "gre_officers": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_MILITARY_LAWS"),
    "gre_treaty": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "gre_network": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "gre_consult": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "gre_withdraw": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "gre_coup": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_MILITARY_LAWS"),
    "gre_response": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "gre_volunteers": ("FOCUS_FILTER_MILITARY_LAWS", "FOCUS_FILTER_INFLUENCE"),
    "gre_escalate": ("FOCUS_FILTER_MILITARY_LAWS", "FOCUS_FILTER_POLITICAL"),
    "tur_consult": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "tur_terms": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "tur_operation": ("FOCUS_FILTER_MILITARY_LAWS", "FOCUS_FILTER_INFLUENCE"),
    "tur_abstain": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_MILITARY_LAWS"),
    "eng_consult": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "eng_mediation": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
    "eng_restraint": ("FOCUS_FILTER_POLITICAL", "FOCUS_FILTER_INFLUENCE"),
}

RETIRED_GRE_IDS = [f"COLDWAR_GRE_1970_cyprus_{i}" for i in range(20)]

FALLBACK_DESCRIPTIONS = {
    "gre_officers": "The Greek officer mission remains a practical instrument of cooperation with Cyprus, while its presence also carries political weight in the National Guard.",
    "gre_treaty": "Respect for the Republic and its elected institutions limits the use of Greek influence and gives civilian cooperation a firmer basis.",
    "gre_network": "The junta preserves its officer network on Cyprus. This covert course deepens political influence at a material cost and increases the danger to the Republic.",
    "gre_consult": "Greece convenes the guarantor governments after a constitutional crisis and asks each participant to consider a negotiated settlement.",
    "gre_withdraw": "Greece ends its sponsorship of the officer network before a coup is launched, reducing its influence and restoring some confidence.",
    "gre_coup": "Greek officers attempt to overthrow Makarios. Cyprus receives a warning and the outcome depends on the actual strength of the opposing institutions and networks.",
    "eng_consult": "London convenes the guarantors after a constitutional crisis and asks Greece and Turkey to participate in an agreed response.",
    "eng_mediation": "Britain works with Greece and Turkey on a common restoration proposal. Coordinated diplomacy creates administrative obligations as well as a path to settlement.",
    "eng_restraint": "Britain limits its enforcement commitment while retaining its treaty record. This reduces administrative costs but weakens its diplomatic influence.",
}


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _tree_nodes(path: Path) -> dict[str, dict[str, Any]]:
    """Read focus-tree root blocks for anchor resolution, ignoring nested effects."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    nodes: dict[str, dict[str, Any]] = {}
    index = 0
    while index < len(lines):
        if not re.match(r"^\tfocus\s*=\s*\{", lines[index]):
            index += 1
            continue
        start = index
        depth = 0
        block: list[str] = []
        while index < len(lines):
            line = re.sub(r"#.*$", "", lines[index])
            line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
            depth += line.count("{") - line.count("}")
            block.append(lines[index])
            index += 1
            if depth == 0:
                break
        text = "\n".join(block)

        def field(name: str) -> str | None:
            match = re.search(rf"(?m)^\s*{re.escape(name)}\s*=\s*([^\s#]+)", text)
            return match.group(1) if match else None

        ident = field("id")
        if not ident:
            continue
        nodes[ident] = {
            "x": int(field("x") or 0),
            "y": int(field("y") or 0),
            "relative_position_id": field("relative_position_id"),
            "line": start + 1,
        }
    return nodes


def _resolve_positions(nodes: dict[str, dict[str, Any]]) -> dict[str, tuple[int, int]]:
    resolved: dict[str, tuple[int, int]] = {}
    visiting: set[str] = set()

    def resolve(ident: str) -> tuple[int, int]:
        if ident in resolved:
            return resolved[ident]
        if ident in visiting:
            raise ValueError(f"Relative focus anchor cycle at {ident}")
        if ident not in nodes:
            raise ValueError(f"Missing relative focus anchor: {ident}")
        visiting.add(ident)
        node = nodes[ident]
        anchor = node["relative_position_id"]
        origin = resolve(anchor) if anchor else (0, 0)
        point = (origin[0] + node["x"], origin[1] + node["y"])
        visiting.remove(ident)
        resolved[ident] = point
        return point

    for ident in nodes:
        resolve(ident)
    return resolved


def _actor_coordinates(actor: dict[str, Any]) -> tuple[int, int]:
    host = HOSTS[actor["tag"]]
    base_x, base_y = host["module_base"]
    return base_x + int(actor["x"]), base_y + int(actor["y"])


def _focus_text(actor: dict[str, Any], actors_by_key: dict[str, dict[str, Any]]) -> str:
    key = actor["key"]
    ident = actor["id"]
    host = HOSTS[actor["tag"]]
    x, y = _actor_coordinates(actor)
    if actor["tag"] == "GRE":
        relative = host["anchor"]
        anchor_x, anchor_y = host["anchor_xy"]
        dx, dy = x - anchor_x, y - anchor_y
    else:
        pre = actor.get("pre", [])
        if pre:
            relative = actors_by_key[pre[0]]["id"]
            parent_x, parent_y = _actor_coordinates(actors_by_key[pre[0]])
            dx, dy = x - parent_x, y - parent_y
        else:
            relative = host["anchor"]
            anchor_x, anchor_y = host["anchor_xy"]
            dx, dy = x - anchor_x, y - anchor_y

    cost = actor.get("cost", 5)
    cost_text = str(int(cost)) + ".0" if isinstance(cost, (int, float)) else str(cost)
    filters = " ".join(FILTERS_BY_KEY.get(key, ("FOCUS_FILTER_POLITICAL",)))
    lines = [
        "shared_focus = {",
        f"\tid = {ident}",
        f"\ticon = {ICON_BY_KEY[key]}",
        f"\tx = {dx}",
        f"\ty = {dy}",
        f"\trelative_position_id = {relative}",
        f"\tcost = {cost_text}",
        "\tcancel_if_invalid = yes",
        "\tcontinue_if_invalid = no",
        "\tavailable_if_capitulated = no",
    ]
    if actor["tag"] in ("TUR", "ENG"):
        lines += [
            "\tallow_branch = {",
            f"\t\toriginal_tag = {actor['tag']}",
            "\t\tIMP_is_1970_scenario = yes",
            "\t}",
        ]
    for parent in actor.get("pre", []):
        lines += ["\tprerequisite = {", f"\t\tfocus = {actors_by_key[parent]['id']}", "\t}"]
    for excluded in actor.get("exclusive", []):
        lines += ["\tmutually_exclusive = {", f"\t\tfocus = {actors_by_key[excluded]['id']}", "\t}"]
    lines += [
        f"\tsearch_filters = {{ {filters} }}",
        "\tavailable = {",
        f"\t\t{PREFIX}{key}_available = yes",
        "\t}",
        "\tcompletion_reward = {",
        f"\t\t{PREFIX}{key}_preview = yes",
        "\t\thidden_effect = {",
        f"\t\t\t{PREFIX}{key}_apply = yes",
        "\t\t}",
        "\t}",
        "\tai_will_do = { factor = 0 }",
        "}",
    ]
    return "\n".join(lines)


def _required_actor_keys(design: dict[str, Any]) -> set[str]:
    actors = design.get("actor_focuses")
    if not isinstance(actors, list):
        raise ValueError("Design has no actor_focuses list")
    keys = [actor.get("key") for actor in actors]
    if len(keys) != 16 or len(set(keys)) != len(keys):
        raise ValueError(f"Expected exactly 16 unique actor focus keys, got {len(keys)}")
    unknown = set(keys) - {key for host in HOSTS.values() for key in host["module_keys"]}
    if unknown:
        raise ValueError(f"Unhandled actor focus keys: {sorted(unknown)}")
    missing = {key for host in HOSTS.values() for key in host["module_keys"]} - set(keys)
    if missing:
        raise ValueError(f"Missing approved actor focus keys: {sorted(missing)}")
    return set(keys)


def _layout_review(design: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    actors = design["actor_focuses"]
    by_key = {actor["key"]: actor for actor in actors}
    expected_by_host: dict[str, list[dict[str, Any]]] = {"GRE": [], "GENERIC": []}
    host_for_tag = {"GRE": "GRE", "TUR": "GENERIC", "ENG": "GENERIC"}
    for actor in actors:
        host_key = host_for_tag[actor["tag"]]
        x, y = _actor_coordinates(actor)
        expected_by_host[host_key].append({"id": actor["id"], "tag": actor["tag"], "x": x, "y": y})

    reports: dict[str, Any] = {}
    for host_key, host in (("GRE", HOSTS["GRE"]), ("GENERIC", HOSTS["TUR"])):
        source = root / host["host_path"]
        nodes = _tree_nodes(source)
        positions = _resolve_positions(nodes)
        anchor = host["anchor"]
        if anchor not in positions:
            raise ValueError(f"Host anchor {anchor} missing in {host['host_path']}")
        collisions: list[dict[str, Any]] = []
        close_rows: list[dict[str, Any]] = []
        for planned in expected_by_host[host_key]:
            for neighbor, point in positions.items():
                if host_key == "GRE" and neighbor in RETIRED_GRE_IDS:
                    continue
                dx = abs(planned["x"] - point[0])
                dy = abs(planned["y"] - point[1])
                if dx == 0 and dy == 0:
                    collisions.append({"planned": planned["id"], "neighbor": neighbor, "at": list(point)})
                elif dy == 0 and dx < 2:
                    close_rows.append({"planned": planned["id"], "neighbor": neighbor, "distance": dx, "row": planned["y"]})
        reports[host_key] = {
            "host": host["host_path"],
            "tree_id": host["tree_id"],
            "anchor": anchor,
            "anchor_position": list(positions[anchor]),
            "planned": expected_by_host[host_key],
            "same_coordinate_collisions": collisions,
            "same_row_spacing_under_2": close_rows,
            "dynamic_offsets_reviewed": True,
        }
        if host_key == "GENERIC":
            reports[host_key]["existing_shared_focus_neighbors"] = [
                {
                    "id": "COLDWAR_GCC_council",
                    "conditional_host": "COLDWAR_GCC_host = yes",
                    "host_tags": ["SAU", "KUW", "BHR", "QAT", "OMA", "UAE"],
                    "base_position": [32, 11],
                    "TUR_ENG_visible": False,
                    "evidence": "common/national_focus/COLDWAR_GCC_1970_shared.txt:4-31; common/scripted_triggers/COLDWAR_GCC_1970.txt:3-14",
                },
                {
                    "id": "COLDWAR_AP_political_focus",
                    "conditional_host": "COLDWAR_AP_host = yes",
                    "host_tags": ["SAF", "ZIM", "NAM"],
                    "base_position": [8, 23],
                    "TUR_ENG_visible": False,
                    "evidence": "common/national_focus/COLDWAR_AP_1970_shared.txt:4-14; common/scripted_triggers/COLDWAR_AP_1970.txt:3-9",
                },
                {
                    "id": "COLDWAR_UNI_the_union_plan",
                    "conditional_host": "COLDWAR_UNI_union_tag = yes",
                    "host_tags": ["SOV", "UKR", "BLR", "EST", "LAT", "LIT", "ARM", "AZE", "GEO", "KAZ", "KYR", "TAJ", "TRK", "UZB", "MLV"],
                    "generic_host_position": [240, 0],
                    "TUR_ENG_visible": False,
                    "evidence": "common/national_focus/COLDWAR_UNI_1970_union_joint.txt:14-35; common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt:7-10",
                },
            ]
        if collisions:
            raise ValueError(f"Focus layout collision in {host_key}: {collisions}")
        if close_rows:
            raise ValueError(f"Tight focus spacing in {host_key}: {close_rows}")
    return reports


def build(design: dict[str, Any]) -> dict[str, Any]:
    """Build focus code, English localization and exact host integration metadata."""
    _required_actor_keys(design)
    actors = design["actor_focuses"]
    by_key = {actor["key"]: actor for actor in actors}
    focus_ids = [actor["id"] for actor in actors]
    if len(set(focus_ids)) != len(focus_ids):
        raise ValueError("Duplicate actor focus IDs")
    for actor in actors:
        for key in actor.get("pre", []) + actor.get("exclusive", []):
            if key not in by_key:
                raise ValueError(f"Unknown focus reference {key} from {actor['key']}")
    _layout_review(design)

    lines = [
        "# IMPERIA COLD WAR — Cyprus guarantor actor focuses.",
        "# Generated by tools/cyprus_1970_rework/foreign_focuses.py.",
        "# Imported by the authored Greek 1970 tree and the generic 1970 host for Turkey and Britain.",
        "",
    ]
    loc: dict[str, str] = {}
    for actor in actors:
        lines.append(_focus_text(actor, by_key))
        lines.append("")
        loc[actor["id"]] = actor["title"]
        description = actor.get("description") or FALLBACK_DESCRIPTIONS.get(actor["key"])
        if not description:
            raise ValueError(f"No English focus description supplied for {actor['key']}")
        loc[actor["id"] + "_desc"] = description

    attachments = []
    for tag, host in HOSTS.items():
        host_node_ids = [by_key[key]["id"] for key in host["module_keys"]]
        attachments.append({
            "tag": tag,
            "host_path": host["host_path"],
            "tree_id": host["tree_id"],
            "anchor": host["anchor"],
            "source_generator": host["source_generator"],
            "layout_source": host["layout_source"],
            "shared_focus_imports": host_node_ids,
            "attachment_position": "Append imports after all host focus definitions so relative anchors precede these shared focuses.",
            "allow_branch": None if tag == "GRE" else f"original_tag = {tag}; IMP_is_1970_scenario = yes",
            "module_base": list(host["module_base"]),
        })

    meta = {
        "project": "IMPERIA COLD WAR",
        "actor_focus_count": len(actors),
        "focus_ids": focus_ids,
        "focus_file": OUTPUT,
        "host_attachments": attachments,
        "layout_review": _layout_review(design),
        "helpers": {
            "available": PREFIX + "<key>_available",
            "preview": PREFIX + "<key>_preview",
            "apply": PREFIX + "<key>_apply",
            "focus_scope": "Country that owns the foreign focus."
        },
        "greece_legacy_retirement": {
            "source_tree": "common/national_focus/COLDWAR_GRE_1970_focus.txt",
            "source_generator": "tools/greece_1970/compile.py",
            "layout_source": "tools/greece_1970/layout.py",
            "layout_section": "cyprus",
            "focus_ids": RETIRED_GRE_IDS,
            "shortcuts": ["shortcut_cyprus_crisis", "shortcut_cyprus_outcome"],
            "preserve_sections": ["aegean", "foreign", "ioa", "party programmes", "all other Greek focus sections"],
            "replacement": "Nine Greek actor focus modules below the foreign-policy root, including the gated intervention response fork."
        },
        "art": {
            "focus_icons_reused": sorted(set(ICON_BY_KEY.values())),
            "gre_cyprus_sprite": "interface/COLDWAR_GRE_1970_goals.gfx:41-42, focus medallion only",
            "cyprus_idea_art": "interface/COLDWAR_CYP_1970_ideas.gfx uses GFX_idea_COLDWAR_CYP_1970_* and existing idea textures; do not assign focus medallions as idea art."
        },
        "integration_constraints": [
            "Do not change the 100-focus Cyprus coordinates.",
            "Do not place party-dependent allow_branch on these actor modules.",
            "The generic 1970 host imports only Turkey and Britain modules; allow_branch is country and scenario gated, not party gated.",
            "The Greek tree import belongs after its spatial anchor has been declared.",
            "The Turkish and British modules use stable generic foreign-policy anchors and are separated from the Generic tree's defense and economic branches.",
        ],
    }
    return {"files": {OUTPUT: "\n".join(lines)}, "loc": loc, "meta": meta}


def main() -> None:
    design_path = ROOT / "docs/cyprus_1970_rework_20261027/concept.json"
    design = json.loads(design_path.read_text(encoding="utf-8"))
    generated = build(design)
    for relative, text in generated["files"].items():
        output_path = ROOT / relative
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps(generated["meta"], indent=2))


if __name__ == "__main__":
    main()
