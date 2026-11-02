# IMPERIA COLD WAR — France 1970 emitted runtime preview builder.
"""Render Current and Proposed France party programmes with native MD art."""
from __future__ import annotations

import base64
from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import re
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
VIZ = Path("C:/Users/Enes/.codex/visualizations/2026/10/28/01a183df-ceae-74b3-b1f4-d519f043ee74")
MD_ROOT = Path("E:/SteamLibrary/steamapps/workshop/content/394360/2777392649")
GAME_ROOT = Path("E:/SteamLibrary/steamapps/common/Hearts of Iron IV")
LOC_FILE = ROOT / "localisation/english/COLDWAR_FRA2_1970_l_english.yml"
ART_GFX = ROOT / "interface/COLDWAR_FRA2_polish_art.gfx"
TEMPLATE = HERE / "preview_template.html"
PROJECT = "IMPERIA COLD WAR"
BASELINE = HERE / "BASELINE.json"
PROPOSAL = HERE / "proposal.json"
CHANGES = HERE / "CHANGES.json"
ASSET_REFERENCE = HERE / "ASSET_REFERENCE.json"


def parse_localisation(path: Path) -> dict[str, str]:
    text = path.read_bytes().decode("utf-8-sig")
    result: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.lstrip().startswith("#") or ":0 " not in line:
            continue
        key, rest = line.split(":0 ", 1)
        raw = rest.strip()
        if not (raw.startswith('"') and raw.endswith('"')):
            continue
        value = json.loads(raw)
        result[key.strip()] = value
    if not text.startswith("l_english:"):
        raise ValueError("Emitted localisation does not start with l_english:")
    return result


def _blocks(text: str, block_name: str) -> list[str]:
    blocks = []
    for match in re.finditer(rf"\b{re.escape(block_name)}\s*=\s*\{{", text):
        opening = text.find("{", match.start())
        depth, quoted, escaped, end = 0, False, False, None
        for index in range(opening, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise ValueError(f"Unclosed {block_name} block")
        blocks.append(text[match.start():end])
    return blocks


def _scalar(block: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*=\s*(\S+)\s*$", block, re.M)
    return match.group(1) if match else None


def _child_blocks(block: str, name: str) -> list[str]:
    return _blocks(block, name)


def parse_focus_script(path: Path) -> tuple[dict[str, dict], list[dict]]:
    text = path.read_bytes().decode("utf-8")
    if text.startswith("\ufeff") or not text.startswith("# IMPERIA COLD WAR —"):
        raise ValueError("Focus script encoding or project marker is invalid")
    focus_tree = _blocks(text, "focus_tree")[0]
    focuses: dict[str, dict] = {}
    for block in _blocks(focus_tree, "focus"):
        focus_id = _scalar(block, "id")
        if not focus_id or focus_id in focuses:
            raise ValueError(f"Missing or duplicate focus id: {focus_id}")
        prerequisites = []
        for group in _child_blocks(block, "prerequisite"):
            prerequisites.append([m.group(1).removeprefix("COLDWAR_FRA2_") for m in re.finditer(r"\bfocus\s*=\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)", group)])
        exclusions = []
        for group in _child_blocks(block, "mutually_exclusive"):
            exclusions.extend(m.group(1).removeprefix("COLDWAR_FRA2_") for m in re.finditer(r"\bfocus\s*=\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)", group))
        focuses[focus_id] = {
            "icon": _scalar(block, "icon"),
            "x": int(_scalar(block, "x")),
            "y": int(_scalar(block, "y")),
            "anchor": _scalar(block, "relative_position_id"),
            "cost": float(_scalar(block, "cost")),
            "prerequisites": prerequisites,
            "exclusions": sorted(set(exclusions)),
            "asset_requirement_keys": sorted(set(re.findall(r"\btooltip\s*=\s*(COLDWAR_FRA2_asset_requirement_[A-Za-z0-9_]+)", block))),
        }
    shortcuts = []
    for match in re.finditer(r"shortcut\s*=\s*\{([^{}]*)\}", focus_tree):
        row = match.group(1)
        name = re.search(r"\bname\s*=\s*(\S+)", row)
        target = re.search(r"\btarget\s*=\s*(\S+)", row)
        if name and target:
            shortcuts.append({"name": name.group(1), "target": target.group(1)})
    return focuses, shortcuts


def sprite_registry(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff") or not text.startswith("# IMPERIA COLD WAR —"):
        raise ValueError("Emitted GFX encoding or project marker is invalid")
    entries = {}
    for block in _blocks(text, "spriteType"):
        name = re.search(r'\bname\s*=\s*"([^"]+)"', block)
        texture = re.search(r'\btexturefile\s*=\s*"([^"]+)"', block, re.I)
        if name and texture:
            entries[name.group(1)] = texture.group(1)
    return entries


def texture_for_native_sprite(sprite_name: str) -> str:
    gfx = (MD_ROOT / "interface/nationalfocusview.gfx").read_text(encoding="utf-8-sig")
    for block in _blocks(gfx, "spriteType"):
        name = re.search(r'\bname\s*=\s*"([^"]+)"', block)
        texture = re.search(r'\btexturefile\s*=\s*"([^"]+)"', block, re.I)
        if name and texture and name.group(1) == sprite_name:
            return texture.group(1)
    raise KeyError(f"Native titlebar sprite not found: {sprite_name}")


def image_data(texture: str, cache: dict[str, str]) -> str:
    if texture in cache:
        return cache[texture]
    source = Path(texture)
    if not source.is_absolute():
        source = (GAME_ROOT if texture.startswith("gfx/interface/focusview/") else MD_ROOT) / texture
    if not source.is_file():
        raise FileNotFoundError(f"Missing native texture referenced by emitted art: {source}")
    buffer = BytesIO()
    with Image.open(source) as image:
        image.convert("RGBA").save(buffer, format="PNG", optimize=True, compress_level=9)
        size = image.size
    cache[texture] = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    cache[texture + "#size"] = f"{size[0]}x{size[1]}"
    return cache[texture]


def build() -> tuple[str, dict]:
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    change_data = json.loads(CHANGES.read_text(encoding="utf-8"))
    asset_reference = json.loads(ASSET_REFERENCE.read_text(encoding="utf-8"))
    loc = parse_localisation(LOC_FILE)
    registry = sprite_registry(ART_GFX)
    changes = {row["key"]: row for row in change_data["changes"]}
    state_names = {42: "Baden-Wurttemberg", 54: "Hauts-de-France", 55: "Normandie", 56: "Ile de France", 57: "Alsace-Lorraine", 58: "Bourgogne", 59: "Loire", 60: "Aquitaine", 61: "Midi Pyrenees", 62: "Rhone-Alpes", 63: "Provence", 64: "Bretagne", 65: "Corsica", 1080: "Hamburg"}
    state_names.update({site["state_id"]: site["state_name"] for site in asset_reference.get("asset_sites", [])})
    country_names = {"FRA": "France", "SOV": "the Soviet Union", "SER": "Yugoslavia", "USA": "the United States", "GER": "West Germany", "ENG": "Britain", "ITA": "Italy", "ALG": "Algeria"}
    building_names = {"industrial_complex": "civilian factory", "arms_factory": "military factory", "dockyard": "dockyard", "offices": "office", "agriculture_district": "agriculture district", "infrastructure": "infrastructure level", "naval_base": "naval base", "nuclear_reactor": "nuclear reactor", "radar_station": "radar station", "fuel_silo": "fuel silo", "air_base": "air base", "rail_terminal": "rail terminal", "internet_station": "network infrastructure"}
    if len(baseline["nodes"]) != 152 or len(proposal["nodes"]) != 156:
        raise ValueError("Expected the 152-focus baseline and 156-focus proposal")
    if change_data["focuses_before"] != 152 or change_data["focuses_after"] != 156:
        raise ValueError("CHANGES.json counts do not match the two designs")

    def normalize(design: dict, is_proposal: bool) -> dict:
        nodes = deepcopy(design["nodes"])
        by_key = {n["key"]: n for n in nodes}
        if len(by_key) != len(nodes):
            raise ValueError("Duplicate focus key")
        for node in nodes:
            if is_proposal:
                node["title"] = node.get("title") or node.get("full_title") or node["key"]
                node["description"] = node.get("description", "")
            else:
                focus_id = node["id"]
                if focus_id not in loc or focus_id + "_desc" not in loc:
                    raise ValueError(f"English title/description missing for {focus_id}")
                node["title"] = loc[focus_id]
                node["description"] = loc[focus_id + "_desc"]
            sprite = node.get("icon")
            if sprite not in registry:
                raise ValueError(f"Focus texture alias missing from emitted GFX: {sprite} ({node['key']})")
            if sprite + "_shine" not in registry:
                raise ValueError(f"Focus shine texture alias missing from emitted GFX: {sprite}_shine")
            node["_change"] = changes.get(node["key"], {}).get("change_type", "unchanged") if is_proposal else "current"
        return {**design, "nodes": nodes}

    current = normalize(baseline, False)
    proposed = normalize(proposal, True)

    effect_fields = {
        "modifier": ("kind", "key", "value"),
        "treasury_gdp": ("kind", "percent"),
        "weekly_gdp_expense": ("kind", "annual_gdp_percent", "divisor"),
        "building": ("kind", "state", "building", "amount", "slots", "province"),
        "research": ("kind", "category", "bonus", "uses"),
        "doctrine": ("kind", "category", "reduction", "uses"),
        "experience": ("kind", "service", "amount"),
        "faction_opinion": ("kind", "faction", "value"),
        "remove_spirit": ("kind", "spirit"),
        "unlock_decision": ("kind", "id", "label"),
        "political_power": ("kind", "value"),
    }

    def compact_effect(effect: dict) -> dict:
        kind = effect.get("kind")
        if kind not in effect_fields:
            raise ValueError(f"Unsupported player-facing preview effect kind: {kind}")
        return {key: effect[key] for key in effect_fields[kind] if key in effect}

    def compact_effects(effects: list[dict]) -> list[dict]:
        return [compact_effect(effect) for effect in effects]

    def visible_condition(condition: str) -> bool:
        return bool(
            re.search(r"_are_in_power\s*=\s*yes$", condition)
            or re.fullmatch(r"has_idea\s*=\s*(?:EU_member|NATO_member|COLDWAR_FRA2P?_[A-Za-z0-9_]+)", condition)
            or re.fullmatch(r"[A-Z]{3}\s*=\s*\{\s*has_idea\s*=\s*(?:EU_member|NATO_member|COLDWAR_FRA2P?_[A-Za-z0-9_]+)\s*\}", condition)
            or re.fullmatch(r"(?:has_tech\s*=\s*internet_1|[A-Z]{3}\s*=\s*\{\s*has_tech\s*=\s*internet_1\s*\})", condition)
        )

    def compact_design(design: dict, mode: str, changed_only: bool = False) -> dict:
        compact = {
            "project": PROJECT, "revision": design.get("revision", mode),
            "nodes": [], "groups": [], "decisions": [], "starting_spirits": [],
            "navigation": design.get("navigation", {}) if not changed_only else {}, "emitted_shortcuts": [],
        }
        fields = ("key", "group", "title", "description", "x", "y", "icon", "cost", "days", "prerequisites", "exclusions", "conditions", "effects", "spirit", "offer", "_change")
        for node in design["nodes"]:
            if changed_only and node.get("_change") not in ("new", "revised"):
                continue
            item = {key: node[key] for key in fields if key in node}
            item["effects"] = compact_effects(node.get("effects", []))
            item["conditions"] = [condition for condition in node.get("conditions", []) if visible_condition(condition)]
            if item.get("spirit"):
                item["spirit_title"] = loc.get(item["spirit"], item.get("spirit_name", item["spirit"]))
            if item.get("offer"):
                offer = item["offer"]
                # Only player-visible bilateral terms belong in the preview.
                offer_out = {key: offer[key] for key in ("partner", "partner_name") if key in offer}
                for side_name in ("france", "recipient"):
                    side = offer.get(side_name, {})
                    tag = "FRA" if side_name == "france" else offer.get("partner", "recipient")
                    offer_out[side_name] = {
                        "spirit": side.get("spirit"),
                        "title": side.get("name") or loc.get(side.get("spirit", ""), side.get("spirit", "")),
                        "effects": compact_effects(side.get("effects", [])),
                    }
                offer_out["activation_conditions"] = [condition for condition in offer.get("activation_conditions", []) if visible_condition(condition)]
                item["offer"] = offer_out
            compact["nodes"].append(item)
        for group in design["groups"] if not changed_only else []:
            compact["groups"].append({key: group[key] for key in ("id", "title", "x", "y", "slot", "parent_group", "governing_group", "trigger") if key in group})
        for decision in design.get("decisions", []) if not changed_only else []:
            item = {key: decision[key] for key in ("id", "effects", "conditions", "days") if key in decision}
            item["effects"] = compact_effects(decision.get("effects", []))
            item["title"] = decision.get("title") or loc.get(decision["id"], decision["id"])
            compact["decisions"].append(item)
        for spirit in design.get("starting_spirits", []) if not changed_only else []:
            compact["starting_spirits"].append({"id": spirit["id"], "title": loc.get(spirit["id"], spirit.get("title", spirit["id"]))})
        group_for_target = {n["id"]: n["group"] for n in design["nodes"] if not n.get("anchor")}
        for s in design.get("navigation", {}).get("shortcuts", []) if not changed_only else []:
            target = s.get("focus", "")
            group = group_for_target.get(target)
            if group:
                compact["emitted_shortcuts"].append({"group": group, "target": target, "label": s.get("name", group)})
        return compact

    packaged = {
        "project": PROJECT,
        "status": "Proposal, not installed",
        "baseline_sha256": change_data.get("baseline_sha256", ""),
        "change_count": len(change_data["changes"]),
        "changed_keys": {key: {"type": row["change_type"], "reason": row["reason"]} for key, row in changes.items()},
        "current": compact_design(current, "current"),
        "proposed": compact_design(proposed, "proposed", changed_only=True),
    }

    art_cache: dict[str, str] = {}
    art: dict[str, str] = {}
    texture_names = {n["icon"] for design in (current, proposed) for n in design["nodes"]}
    for sprite in sorted(texture_names):
        if sprite:
            if sprite not in registry:
                raise ValueError(f"Sprite alias missing from emitted GFX: {sprite}")
            art[sprite] = image_data(registry[sprite], art_cache)
    for sprite in ("GFX_focus_unavailable", "GFX_focus_can_start"):
        art[sprite] = image_data(texture_for_native_sprite(sprite), art_cache)

    # Keep art bytes deduplicated: one data URI per emitted sprite alias and
    # then assign aliases to focus keys in the fragment's small bootstrap.
    # Keep the preview payload to installed player-visible information. The
    # full source runtime_design remains the semantic audit record.
    template = TEMPLATE.read_text(encoding="utf-8")
    fragment = template.replace("__DESIGN__", json.dumps(packaged, ensure_ascii=False, separators=(",", ":")))
    fragment = fragment.replace("__ART__", json.dumps(art, ensure_ascii=False, separators=(",", ":")))
    fragment = fragment.replace("    const shortcutLabels=", "    for(const view of [PACK.current,PACK.proposed])for(const n of view.nodes)A[n.key]=A[n.icon];\n    const shortcutLabels=")
    if "__DESIGN__" in fragment or "__ART__" in fragment or "__LOC__" in fragment:
        raise ValueError("Preview template placeholders were not fully replaced")
    encoded = fragment.encode("utf-8")
    if len(encoded) >= 1024 * 1024:
        raise ValueError(f"Inline preview exceeds 1 MiB: {len(encoded)} bytes")
    VIZ.mkdir(parents=True, exist_ok=True)
    (VIZ / "france-party-deals.html").write_bytes(encoded)
    full = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>France 1970 National Focus</title><style>body{margin:0;background:#151916}</style></head><body>" + fragment + "</body></html>"
    (HERE / "PREVIEW.html").write_bytes(full.encode("utf-8"))
    report = {
        "project": PROJECT,
        "kind": "Comparison of the current native tree and a proposed amendment; not installed or an HOI4 engine screenshot",
        "current_focus_count": len(current["nodes"]),
        "proposed_focus_count": len(proposed["nodes"]),
        "section_count": len(proposal["groups"]),
        "current_offer_count": sum(bool(n.get("offer")) for n in current["nodes"]),
        "proposed_offer_count": sum(bool(n.get("offer")) for n in proposed["nodes"]),
        "localisation_count": len(loc),
        "emitted_sprite_count": len(registry),
        "used_icon_textures": len({registry[n["icon"]] for design in (current, proposed) for n in design["nodes"]}),
        "converted_texture_count": len(art_cache) // 2,
        "png_dimensions": {key.removesuffix("#size"): value for key, value in art_cache.items() if key.endswith("#size")},
        "fragment_bytes": len(encoded),
        "art_source": "Emitted project GFX aliases and current MD native focus titlebar declarations; DDS to lossless RGBA PNG with no scaling",
        "build_hash": __import__("hashlib").sha256(encoded).hexdigest(),
    }
    (HERE / "PREVIEW_BUILD.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return full, report


if __name__ == "__main__":
    _, result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2))
