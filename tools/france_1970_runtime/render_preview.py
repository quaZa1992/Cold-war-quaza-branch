# IMPERIA COLD WAR — France 1970 emitted runtime preview builder.
"""Render the installed France focus tree from emitted script, localisation and art."""
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
FOCUS_SCRIPT = ROOT / "common/national_focus/COLDWAR_FRA2_1970_focus.txt"
LOC_FILE = ROOT / "localisation/english/COLDWAR_FRA2_1970_l_english.yml"
ART_GFX = ROOT / "interface/COLDWAR_FRA2_polish_art.gfx"
TEMPLATE = HERE / "preview_template.html"
PROJECT = "IMPERIA COLD WAR"


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
        rgba = image.convert("RGBA")
        rgba.save(buffer, format="PNG", optimize=True, compress_level=9)
        mime = "image/png"
        webp = BytesIO()
        try:
            rgba.save(webp, format="WEBP", lossless=True, quality=100, method=6)
            decoded = Image.open(BytesIO(webp.getvalue())).convert("RGBA")
            if rgba.tobytes() == decoded.tobytes() and len(webp.getvalue()) < len(buffer.getvalue()):
                buffer = webp
                mime = "image/webp"
        except (OSError, ValueError):
            pass
        size = image.size
    cache[texture] = "data:" + mime + ";base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
    cache[texture + "#size"] = f"{size[0]}x{size[1]}"
    return cache[texture]


def compact_effect(effect: dict) -> dict:
    """Keep every player-visible value and drop compiler transaction metadata."""
    fields = {
        "modifier": ("kind", "key", "value"),
        "treasury_gdp": ("kind", "percent"),
        "weekly_gdp_expense": ("kind", "annual_gdp_percent", "divisor"),
        "building": ("kind", "state", "building", "amount", "slots", "province"),
        "state_slots": ("kind", "state", "amount"),
        "research": ("kind", "category", "bonus", "uses"),
        "doctrine": ("kind", "category", "reduction", "uses"),
        "experience": ("kind", "service", "amount"),
        "faction_opinion": ("kind", "faction", "value"),
        "remove_spirit": ("kind", "spirit"),
        "transition_spirit": ("kind", "from", "to"),
        "unlock_decision": ("kind", "id", "label"),
        "political_power": ("kind", "value"),
    }
    kind = effect.get("kind")
    if kind not in fields:
        raise ValueError(f"Preview does not know how to render effect kind {kind!r}")
    return {key: effect[key] for key in fields[kind] if key in effect}


def build() -> tuple[str, dict]:
    design = json.loads((HERE / "runtime_design.json").read_text(encoding="utf-8"))
    loc = parse_localisation(LOC_FILE)
    emitted, shortcuts = parse_focus_script(FOCUS_SCRIPT)
    registry = sprite_registry(ART_GFX)
    nodes = design["nodes"]
    by_id = {n["id"]: n for n in nodes}
    if len(nodes) != 176 or len(emitted) != len(nodes):
        raise ValueError(f"Expected 176 emitted focus nodes, found design={len(nodes)}, script={len(emitted)}")
    for node in nodes:
        actual = emitted.get(node["id"])
        if not actual:
            raise ValueError(f"Focus missing from emitted script: {node['id']}")
        expected = {
            "icon": node["icon"], "x": node["offset"][0], "y": node["offset"][1],
            "anchor": (node["anchor"] if node["anchor"].startswith("COLDWAR_FRA2_") else "COLDWAR_FRA2_" + node["anchor"]) if node.get("anchor") else None,
            "cost": node["cost"],
            "prerequisites": [["COLDWAR_FRA2_" + key for key in group] for group in node.get("prerequisites", [])],
            "exclusions": sorted("COLDWAR_FRA2_" + key for key in node.get("exclusions", [])),
        }
        found = {key: actual[key] for key in expected}
        found["prerequisites"] = [["COLDWAR_FRA2_" + key for key in group] for group in found["prerequisites"]]
        found["exclusions"] = ["COLDWAR_FRA2_" + key for key in found["exclusions"]]
        if expected != found:
            raise ValueError(f"Emitted focus structure differs from runtime design for {node['id']}: expected={expected}, found={found}")
        if node["id"] not in loc or node["id"] + "_desc" not in loc:
            raise ValueError(f"English title/description missing for {node['id']}")
        node["title"] = loc[node["id"]]
        node["description"] = loc[node["id"] + "_desc"]
        if node.get("icon") not in registry:
            raise ValueError(f"Emitted focus icon missing from .gfx: {node['icon']}")
        shine = node["icon"] + "_shine"
        if shine not in registry:
            raise ValueError(f"Emitted focus shine sprite missing from .gfx: {shine}")

    resolved: dict[str, tuple[int, int]] = {}
    def resolve(focus_id: str) -> tuple[int, int]:
        if focus_id in resolved:
            return resolved[focus_id]
        actual = emitted[focus_id]
        if actual["anchor"]:
            parent = resolve(actual["anchor"])
            point = (parent[0] + actual["x"], parent[1] + actual["y"])
        else:
            point = (actual["x"], actual["y"])
        resolved[focus_id] = point
        return point
    for node in nodes:
        point = resolve(node["id"])
        if point != (node["x"], node["y"]):
            raise ValueError(f"Resolved emitted focus coordinate differs for {node['id']}: {point} != {(node['x'], node['y'])}")

    for group in design["groups"]:
        group["title"] = loc.get(f"COLDWAR_FRA2_{group['id']}_programme", group["title"] + " Programme").removesuffix(" Programme")
    design["emitted_shortcuts"] = []
    group_for_target = {n["id"]: n["group"] for n in nodes if not n.get("anchor")}
    for row in shortcuts:
        key = group_for_target.get(row["target"])
        if not key:
            continue
        label = loc.get(row["name"], "")
        if not label or (label.startswith("[") and label.endswith("]")):
            label = design["groups"][[g["id"] for g in design["groups"]].index(key)]["title"]
        design["emitted_shortcuts"].append({"group": key, "target": row["target"], "label": label})

    art_cache: dict[str, str] = {}
    art = {"sprites": {}, "textures": {}}
    texture_names = {n["icon"] for n in nodes}
    for sprite in sorted(texture_names):
        if sprite:
            if sprite not in registry:
                raise ValueError(f"Sprite alias missing from emitted GFX: {sprite}")
            texture = registry[sprite]
            art["sprites"][sprite] = texture
            art["textures"].setdefault(texture, image_data(texture, art_cache))
    for sprite in ("GFX_focus_unavailable", "GFX_focus_can_start"):
        texture = texture_for_native_sprite(sprite)
        art["sprites"][sprite] = texture
        art["textures"].setdefault(texture, image_data(texture, art_cache))

    # Keep art bytes deduplicated: one data URI per emitted sprite alias and
    # then assign aliases to focus keys in the fragment's small bootstrap.
    # Keep the preview payload to installed player-visible information. The
    # full source runtime_design remains the semantic audit record.
    compact = {
        "project": PROJECT,
        "revision": design.get("revision", ""),
        "nodes": [],
        "groups": [],
        "decisions": [],
        "starting_spirits": [],
        "recovery_stages": [],
        "navigation": design.get("navigation", {}),
        "expansion_revision": {
            "added_focus_keys": design.get("expansion_revision", {}).get("added_focus_keys", []),
            "approved_input_sha256": design.get("expansion_revision", {}).get("approved_input_sha256", ""),
        },
        "emitted_shortcuts": design.get("emitted_shortcuts", []),
    }
    node_fields = ("key", "group", "title", "description", "x", "y", "icon", "days", "prerequisites", "exclusions", "conditions", "effects", "spirit_name")
    for node in nodes:
        item = {key: node[key] for key in node_fields if key in node}
        item["effects"] = [compact_effect(effect) for effect in node.get("effects", [])]
        req_keys = emitted[node["id"]]["asset_requirement_keys"]
        item["asset_requirements"] = [loc[key] for key in req_keys if key in loc]
        if node.get("spirit"):
            item["spirit_title"] = loc.get(node["spirit"], node.get("spirit_name", node["spirit"]))
        if node.get("offer"):
            offer = node["offer"]
            item["offer"] = {key: offer[key] for key in ("partner_name", "activation_conditions", "acceptance_conditions") if key in offer}
            for side_name in ("france", "recipient"):
                side = offer[side_name]
                item["offer"][side_name] = {
                    "spirit": side["spirit"],
                    "title": loc.get(side["spirit"], side.get("name", side["spirit"])),
                    "effects": [compact_effect(effect) for effect in side["effects"]],
                }
        compact["nodes"].append(item)
    for group in design["groups"]:
        compact["groups"].append({key: group[key] for key in ("id", "title", "x", "y", "slot", "parent_group", "governing_group", "trigger") if key in group})
    for decision in design.get("decisions", []):
        item = {"id": decision["id"]}
        item["effects"] = [compact_effect(effect) for effect in decision.get("effects", [])]
        item["title"] = loc.get(decision["id"], decision.get("title", decision["id"]))
        compact["decisions"].append(item)
    for spirit in design.get("starting_spirits", []):
        compact["starting_spirits"].append({
            "id": spirit["id"],
            "title": loc.get(spirit["id"], spirit["title"]),
            "modifiers": [compact_effect(effect) for effect in spirit.get("effects", []) if effect.get("kind") == "modifier"],
        })
    for spirit in design.get("recovery_stages", []):
        compact["recovery_stages"].append({
            "id": spirit["id"],
            "title": loc.get(spirit["id"], spirit["name"]),
            "modifiers": [{"kind": "modifier", "key": key, "value": value} for key, value in spirit.get("modifiers", {}).items()],
        })

    template = TEMPLATE.read_text(encoding="utf-8")
    fragment = template.replace("__DESIGN__", json.dumps(compact, ensure_ascii=False, separators=(",", ":")))
    fragment = fragment.replace("__ART__", json.dumps(art, ensure_ascii=False, separators=(",", ":")))
    fragment = fragment.replace("    const shortcutLabels=", "    for(const n of D.nodes)A[n.key]=A[n.icon];\n    const shortcutLabels=")
    if "__DESIGN__" in fragment or "__ART__" in fragment or "__LOC__" in fragment:
        raise ValueError("Preview template placeholders were not fully replaced")
    encoded = fragment.encode("utf-8")
    if len(encoded) >= 1_000_000:
        raise ValueError(f"Inline preview exceeds 1,000,000 bytes: {len(encoded)} bytes")
    VIZ.mkdir(parents=True, exist_ok=True)
    (VIZ / "france-cold-war.html").write_bytes(encoded)
    full = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>France 1970 National Focus</title><style>body{margin:0;background:#151916}</style></head><body>" + fragment + "</body></html>"
    (HERE / "PREVIEW.html").write_bytes(full.encode("utf-8"))
    report = {
        "project": PROJECT,
        "kind": "Emitted native focus tree preview; not an HOI4 engine screenshot",
        "focus_count": len(nodes),
        "section_count": len(design["groups"]),
        "offer_count": sum(bool(n.get("offer")) for n in nodes),
        "starting_spirit_count": len(design.get("starting_spirits", [])),
        "recovery_stage_count": len(design.get("recovery_stages", [])),
        "spirit_transition_count": sum(1 for n in nodes for effect in n.get("effects", []) if effect.get("kind") == "transition_spirit"),
        "expansion_added_focus_count": len(design.get("expansion_revision", {}).get("added_focus_keys", [])),
        "standalone_slot_reward_count": sum(1 for n in nodes for effect in n.get("effects", []) if effect.get("kind") == "state_slots"),
        "localisation_count": len(loc),
        "emitted_sprite_count": len(registry),
        "used_icon_textures": len({registry[n["icon"]] for n in nodes}),
        "converted_texture_count": len(art_cache) // 2,
        "png_dimensions": {key.removesuffix("#size"): value for key, value in art_cache.items() if key.endswith("#size")},
        "fragment_bytes": len(encoded),
        "art_source": "Emitted project GFX aliases and current MD native focus titlebar declarations; DDS to pixel-verified lossless RGBA PNG or WebP, no scaling",
        "build_hash": __import__("hashlib").sha256(encoded).hexdigest(),
    }
    (HERE / "PREVIEW_BUILD.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return full, report


if __name__ == "__main__":
    _, result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2))
