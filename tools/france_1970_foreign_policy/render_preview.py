# IMPERIA COLD WAR — France 1970 foreign policy design preview builder.
"""Render the installed France 1970 foreign-policy tree from emitted sources."""
from __future__ import annotations

import base64
from copy import deepcopy
from io import BytesIO
import gzip
import hashlib
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
DESIGN_PATH = HERE / "foreign_policy_design.json"
BASELINE_PATH = ROOT / "tools/france_1970_runtime/runtime_design.json"
APPROVED_PATH = ROOT / "tools/france_1970_runtime/approved_foreign_policy.json"
MANIFEST_PATH = ROOT / "tools/france_1970_runtime/manifest.json"
FOCUS_SCRIPT = ROOT / "common/national_focus/COLDWAR_FRA2_1970_focus.txt"
IDEA_FILES = (ROOT / "common/ideas/COLDWAR_FRA2_1970_ideas.txt", ROOT / "common/ideas/COLDWAR_FRA2_diplomacy_ideas.txt")
EFFECT_FILES = (ROOT / "common/scripted_effects/COLDWAR_FRA2_1970_effects.txt", ROOT / "common/scripted_effects/COLDWAR_FRA2_diplomacy_effects.txt")
TRIGGER_FILES = (ROOT / "common/scripted_triggers/COLDWAR_FRA2_1970_triggers.txt", ROOT / "common/scripted_triggers/COLDWAR_FRA2_diplomacy_triggers.txt")
PRESSURE_CONFIG = ROOT / "tools/france_1970_runtime/pressure_contracts.json"
PRESSURE_FILES = (
    ROOT / "common/decisions/COLDWAR_FRA2_pressure_decisions.txt",
    ROOT / "common/scripted_effects/COLDWAR_FRA2_pressure_effects.txt",
    ROOT / "common/scripted_triggers/COLDWAR_FRA2_pressure_triggers.txt",
    ROOT / "common/ideas/COLDWAR_FRA2_pressure_ideas.txt",
    ROOT / "events/COLDWAR_FRA2_pressure_events.txt",
)
PROJECT = "IMPERIA COLD WAR"
APPROVED_SHA256 = "7bd27bfa457cda2c8443a4252150ed806396a5cc7adb4353a3e5ddaad0f3785f"
sys.path.insert(0, str(ROOT / "tools/france_1970_runtime"))
from deal_balance_revision import apply_deal_balance_revision
TILE_LAYOUT = {
    "african_finance": (68, 14, ("fp_senegal_clearing", "fp_senegal_boards", "fp_cameroon_guarantee", "fp_cameroon_treasury", "fp_gabon_elf", "fp_gabon_processing", "fp_niger_rights", "fp_niger_processing")),
    "arab_contracts": (88, 14, ("fp_libya_aviation", "fp_egypt_aviation", "fp_iraq_energy", "fp_iraq_industry", "fp_saudi_naval", "fp_saudi_civil", "fp_lebanon_field", "fp_lebanon_recovery")),
    "african_security": (68, 19, ("fp_abidjan_transit", "fp_abidjan_port", "fp_libreville_station", "fp_gabon_officers", "fp_chad_airlift", "fp_chad_cadres", "fp_niger_field_services", "fp_niger_rural")),
    "global_partnerships": (88, 19, ("fp_india_aviation", "fp_india_power", "fp_vietnam_engineering", "fp_vietnam_health", "fp_mauritius_agriculture", "fp_mauritius_marine", "fp_djibouti_defence", "fp_djibouti_civil")),
}


def apply_tile_layout(design: dict) -> bool:
    """Apply the reviewed compact 2x2 chapter placement as a preview-only overlay."""
    by_key = {node["key"]: node for node in design["nodes"]}
    root = by_key["fp_foreign_service"]
    changed = False
    for group_id, (center, entry_y, leaves) in TILE_LAYOUT.items():
        entry = next(node for node in design["nodes"] if node["key"] in set(design["foreign_policy_added_keys"]) and node["group"] == group_id and node["key"] not in {key for _, _, keys in TILE_LAYOUT.values() for key in keys})
        if (entry["x"], entry["y"]) != (center, entry_y):
            changed = True
        entry["x"], entry["y"] = center, entry_y
        entry["anchor"] = root["key"]
        entry["offset"] = [center - root["x"], entry_y - root["y"]]
        group = next(g for g in design["groups"] if g["id"] == group_id)
        group["x"], group["y"] = center, entry_y
        for index, key in enumerate(leaves):
            pair = index // 2
            left_pair = pair % 2 == 0
            x = center + (-4 if left_pair else 2) + 2 * (index % 2)
            y = entry_y + 1 + 2 * (pair // 2)
            node = by_key[key]
            if (node["x"], node["y"]) != (x, y):
                changed = True
            node["x"], node["y"] = x, y
            node["anchor"] = entry["key"]
            node["offset"] = [x - center, y - entry_y]
    return changed


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


def focus_source_blocks(path: Path) -> dict[str, str]:
    text = path.read_bytes().decode("utf-8")
    tree = _blocks(text, "focus_tree")[0]
    result = {}
    for block in _blocks(tree, "focus"):
        key = _scalar(block, "id")
        if key:
            result[key] = block
    return result


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


def named_block(text: str, name: str) -> str:
    blocks = _blocks(text, name)
    if len(blocks) != 1:
        raise ValueError(f"Expected exactly one emitted block for {name}, got {len(blocks)}")
    return blocks[0]


def compact_pressure(design: dict, loc: dict[str, str], config: dict, sources: dict[str, str]) -> dict:
    """Build an inspector payload only after cross-checking compiled decision sources."""
    if design.get("pressure_revision") != config:
        raise ValueError("Runtime design pressure configuration differs from the installed source JSON")
    decisions, effects, triggers, ideas, events = (sources[p.name] for p in PRESSURE_FILES)
    nodes = {n["key"]: n for n in design["nodes"]}
    prefix = config["prefix"]
    entries = {}
    for partner in config["partners"]:
        tag = partner["tag"]
        send_id = f"{prefix}_send_{tag}"
        accept_id = f"{prefix}_accept_decision_{tag}"
        refuse_id = f"{prefix}_refuse_decision_{tag}"
        send = named_block(decisions, send_id)
        accept = named_block(decisions, accept_id)
        refuse = named_block(decisions, refuse_id)
        if int(_scalar(send, "cost") or -1) != config["send_cost_political_power"]:
            raise ValueError(f"Pressure send cost differs for {tag}")
        if not re.search(rf"\b{prefix}_can_send_{tag}\s*=\s*yes", send):
            raise ValueError(f"Pressure send gate is absent for {tag}")
        if not re.search(rf"\b{prefix}_preview_{tag}\s*=\s*yes", send + accept + refuse):
            raise ValueError(f"Pressure choice preview is absent for {tag}")
        required_locs = [send_id, send_id + "_desc", f"{prefix}_send_requirement_{tag}", accept_id, accept_id + "_desc", f"{prefix}_accept_requirement_{tag}", refuse_id, refuse_id + "_desc"]
        for key in required_locs:
            if key not in loc:
                raise ValueError(f"Missing compiled pressure localization: {key}")
        preview = named_block(effects, f"{prefix}_preview_{tag}")
        preview_loc_keys = re.findall(r"custom_effect_tooltip\s*=\s*([A-Z][A-Za-z0-9_.]+)", preview)
        if any(key not in loc and key != "TT_IF_THEY_ACCEPT" for key in preview_loc_keys):
            raise ValueError(f"Pressure preview has an unresolved localization for {tag}")
        aid_rows = []
        aid_focus_keys = []
        for node in design["nodes"]:
            offer = node.get("offer")
            if not offer or offer.get("partner") != tag:
                continue
            for effect in offer["france"].get("effects", []):
                if effect.get("kind") == "weekly_transfer" and effect.get("flow") == "expense" and effect.get("payer") == "FRA":
                    aid_focus_keys.append(node["key"])
                    aid_rows.append({"focus": node["key"], "title": loc.get(node["id"], node["title"]), "annual_gdp_percent": effect["annual_gdp_percent"], "basis": effect.get("payer", "FRA")})
        actual_aid_keys = sorted(set(re.findall(rf"COLDWAR_FRA2_offer_active_(fp_[A-Za-z0-9_]+)\s*=\s*yes", preview)))
        if actual_aid_keys != sorted(set(aid_focus_keys)):
            raise ValueError(f"Pressure refusal preview aid inventory differs from active offers for {tag}: {actual_aid_keys} != {sorted(set(aid_focus_keys))}")
        event_id = re.search(rf"country_event\s*=\s*\{{\s*id\s*=\s*COLDWAR_FRA2_pressure\.(\d+)\s+days\s*=\s*(\d+)", named_block(effects, f"{prefix}_start_{tag}"))
        if not event_id or int(event_id.group(2)) != config["pending_days"]:
            raise ValueError(f"Pressure response deadline differs for {tag}")
        host_idea = named_block(ideas, f"{prefix}_charter_host_{tag}")
        france_idea = named_block(ideas, f"{prefix}_charter_france_{tag}")
        crisis_idea = named_block(ideas, f"{prefix}_withdrawal_crisis")
        def idea_modifiers(block: str) -> dict[str, float]:
            body = _blocks(block, "modifier")[0]
            return {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*=\s*(-?[0-9.]+)\s*$", body, re.M)}
        if idea_modifiers(host_idea) != {k: float(v) for k, v in config["host_charter_modifiers"].items()}:
            raise ValueError(f"Pressure host charter idea differs for {tag}")
        if idea_modifiers(france_idea) != {k: float(v) for k, v in config["france_charter_modifiers"].items()}:
            raise ValueError(f"Pressure French charter idea differs for {tag}")
        if idea_modifiers(crisis_idea) != {k: float(v) for k, v in config["withdrawal_crisis_modifiers"].items()}:
            raise ValueError("Pressure withdrawal crisis idea differs from the installed config")
        entry_titles = []
        for focus in partner["entry_focuses"]:
            node = nodes[focus]
            entry_titles.append({"key": focus, "title": loc.get(node["id"], node["title"])})
        base_contracts = []
        for key in partner["base_contracts"]:
            node = nodes[key]
            base_contracts.append({"key": key, "title": loc.get(node["id"], node["title"])})
        entries[tag] = {
            "tag": tag, "name": partner["name"], "entry_focuses": partner["entry_focuses"], "entry_titles": entry_titles,
            "base_contracts": base_contracts, "aid_rows": aid_rows,
            "send": {"title": loc[send_id], "description": loc[send_id+"_desc"], "requirement": loc[f"{prefix}_send_requirement_{tag}"]},
            "accept": {"title": loc[accept_id], "description": loc[accept_id+"_desc"], "requirement": loc[f"{prefix}_accept_requirement_{tag}"]},
            "refuse": {"title": loc[refuse_id], "description": loc[refuse_id+"_desc"]},
            "host_idea": {"title": loc.get(f"{prefix}_charter_host_{tag}", "Procurement Charter"), "modifiers": idea_modifiers(host_idea)},
            "france_idea": {"title": loc.get(f"{prefix}_charter_france_{tag}", "French Protection Costs"), "modifiers": idea_modifiers(france_idea)},
            "refusal_idea": {"title": loc.get(f"{prefix}_withdrawal_crisis", "Withdrawal of French Support"), "modifiers": idea_modifiers(crisis_idea)},
            "preview_loc_keys": preview_loc_keys, "event_id": int(event_id.group(1)),
        }
    return {"config": config, "partners": list(entries.values()), "prefix": prefix}


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
        "weekly_transfer": ("kind", "payer", "recipient", "annual_gdp_percent", "divisor", "flow"),
        "access": ("kind", "grantor", "beneficiary", "relation"),
        "resource_rights": ("kind", "grantor", "beneficiary", "state", "resources"),
    }
    kind = effect.get("kind")
    if kind not in fields:
        raise ValueError(f"Preview does not know how to render effect kind {kind!r}")
    result = {key: effect[key] for key in fields[kind] if key in effect}
    if kind == "unlock_decision" and "id" not in result and "decision" in effect:
        result["id"] = effect["decision"]
        result["label"] = "Recipient approval decision"
    return result


def build() -> tuple[str, dict]:
    approved = json.loads(APPROVED_PATH.read_text(encoding="utf-8"))
    expected_runtime = apply_deal_balance_revision(approved)
    design = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    approved_bytes = APPROVED_PATH.read_bytes()
    approved_hash = hashlib.sha256(approved_bytes).hexdigest()
    if approved_hash != APPROVED_SHA256 or manifest.get("approved_foreign_policy_sha256") != approved_hash:
        raise ValueError("Installed foreign-policy source does not match the frozen approved input or manifest")
    if design.get("approved_foreign_policy_sha256") != approved_hash:
        raise ValueError("Installed runtime design cites a different foreign-policy approval")
    baseline = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    loc = parse_localisation(LOC_FILE)
    registry = sprite_registry(ART_GFX)
    focus_ast, _ = parse_focus_script(FOCUS_SCRIPT)
    focus_blocks = focus_source_blocks(FOCUS_SCRIPT)
    effect_texts = [p.read_text(encoding="utf-8") for p in EFFECT_FILES]
    effect_source = "\n".join(effect_texts)
    trigger_source = "\n".join(p.read_text(encoding="utf-8") for p in TRIGGER_FILES)
    idea_source = "\n".join(p.read_text(encoding="utf-8") for p in IDEA_FILES)
    pressure_config = json.loads(PRESSURE_CONFIG.read_text(encoding="utf-8"))
    pressure_sources = {path.name: path.read_text(encoding="utf-8") for path in PRESSURE_FILES}
    pressure = compact_pressure(design, loc, pressure_config, pressure_sources)
    source_hashes = {str(path.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(path.read_bytes()).hexdigest() for path in (FOCUS_SCRIPT, LOC_FILE, ART_GFX, *EFFECT_FILES, *IDEA_FILES, *TRIGGER_FILES, *PRESSURE_FILES)}
    pressure_config_hash = hashlib.sha256(PRESSURE_CONFIG.read_bytes()).hexdigest()
    pressure_generator_path = ROOT / "tools/france_1970_runtime/pressure.py"
    pressure_generator_hash = hashlib.sha256(pressure_generator_path.read_bytes()).hexdigest()
    if manifest.get("pressure_contracts_sha256") != pressure_config_hash or manifest.get("pressure_source_sha256") != pressure_generator_hash:
        raise ValueError("Pressure source/configuration hash differs from the installed manifest")
    for relative, digest in source_hashes.items():
        declared = manifest.get("files", {}).get(relative, {}).get("sha256")
        if declared != digest:
            raise ValueError(f"Installed source hash differs from manifest: {relative}")
    nodes = design["nodes"]
    if len(nodes) != 213 or len(nodes) != len({n["key"] for n in nodes}):
        raise ValueError(f"Expected 213 unique installed focus nodes, found {len(nodes)}")
    if manifest.get("focus_count") != 213 or manifest.get("offer_count") != 67:
        raise ValueError("Installed manifest count mismatch")
    baseline_keys = {n["key"] for n in baseline["nodes"]}
    proposal_keys = {n["key"] for n in nodes}
    if baseline_keys != proposal_keys:
        raise ValueError("Runtime design and installed focus inventory differ")
    proposal_by_key = {n["key"]: n for n in nodes}
    added = set(approved.get("foreign_policy_added_keys", []))
    if len(added) != 37 or not added.issubset(proposal_keys):
        raise ValueError("The frozen foreign-policy addition inventory is invalid")
    fields = ("id", "key", "group", "title", "full_title", "description", "x", "y", "anchor", "offset", "cost", "days", "prerequisites", "exclusions", "conditions", "effects", "spirit", "spirit_name", "icon", "icon_source", "offer")
    approved_by_key = {n["key"]: n for n in approved["nodes"]}
    expected_by_key = {n["key"]: n for n in expected_runtime["nodes"]}
    mismatches = [(key, field) for key in sorted(proposal_keys) for field in fields if expected_by_key[key].get(field) != proposal_by_key[key].get(field)]
    if mismatches:
        raise ValueError(f"Installed runtime differs from frozen input after authorized deal-balance revision: {mismatches[:12]}")
    if len(focus_ast) != 213:
        raise ValueError(f"Emitted focus script has {len(focus_ast)} nodes, expected 213")
    for n in nodes:
        ast = focus_ast.get(n["id"])
        if not ast:
            raise ValueError(f"Focus missing from emitted AST: {n['id']}")
        anchor = (n.get("anchor") or "").removeprefix("COLDWAR_FRA2_") or None
        # Script coordinates are relative to the named parent; resolve against
        # the emitted design anchors before comparing them to absolute grid points.
        ax, ay = (proposal_by_key[anchor]["x"], proposal_by_key[anchor]["y"]) if anchor else (0, 0)
        actual_xy = (ax + ast["x"], ay + ast["y"])
        expected_prereqs = [[key.removeprefix("COLDWAR_FRA2_") for key in block] for block in n.get("prerequisites", [])]
        expected_exclusions = sorted(k.removeprefix("COLDWAR_FRA2_") for k in n.get("exclusions", []))
        actual_anchor = (ast["anchor"] or "").removeprefix("COLDWAR_FRA2_") or None
        if actual_xy != (n["x"], n["y"]) or actual_anchor != anchor or ast["icon"] != n["icon"] or abs(ast["cost"] - n.get("cost", 10)) > 0.00001 or ast["prerequisites"] != expected_prereqs or ast["exclusions"] != expected_exclusions:
            raise ValueError(f"Installed AST differs from runtime focus data for {n['key']}: xy={actual_xy}, anchor={ast['anchor']}, prereq={ast['prerequisites']}, exclusions={ast['exclusions']}")
        for loc_key in (n["id"], n["id"] + "_desc"):
            if loc_key not in loc:
                raise ValueError(f"Missing emitted English localization key {loc_key}")
        focus_block = focus_blocks[n["id"]]
        if not _blocks(focus_block, "completion_reward"):
            raise ValueError(f"Focus has no emitted completion reward: {n['key']}")
        try:
            available_block = _blocks(focus_block, "available")[0]
        except IndexError:
            raise ValueError(f"Focus has no emitted availability block: {n['key']}")
        for trigger in re.findall(r"^\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)\s*=\s*yes\s*$", available_block, re.M):
            if not _blocks(trigger_source, trigger):
                raise ValueError(f"Focus references undefined emitted trigger {trigger}: {n['key']}")
        for tooltip_key in re.findall(r"\btooltip\s*=\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)", available_block):
            if tooltip_key not in loc:
                raise ValueError(f"Focus requirement tooltip has no emitted English text: {tooltip_key}")
        complete_key = "COLDWAR_FRA2_complete_" + n["key"]
        if not re.search(rf"\b{re.escape(complete_key)}\s*=\s*\{{", effect_source):
            raise ValueError(f"Missing concrete completion provider {complete_key}")
        if n.get("offer"):
            preview_provider = named_block(effect_source, "COLDWAR_FRA2_offer_preview_" + n["key"])
            for provider in ("COLDWAR_FRA2_offer_preview_" + n["key"], "COLDWAR_FRA2_accept_" + n["key"]):
                if not re.search(rf"\b{re.escape(provider)}\s*=\s*\{{", effect_source):
                    raise ValueError(f"Missing emitted offer provider {provider}")
            for tooltip_key in re.findall(r"custom_effect_tooltip\s*=\s*(COLDWAR_FRA2_[A-Za-z0-9_]+)", preview_provider):
                if tooltip_key not in loc:
                    raise ValueError(f"Offer numeric tooltip has no emitted English text: {tooltip_key}")
            for side in ("france", "recipient"):
                idea_id = n["offer"][side]["spirit"]
                side_effects = n["offer"][side]["effects"]
                idea_block = named_block(idea_source, idea_id)
                if loc.get(idea_id) != n["offer"][side].get("name"):
                    raise ValueError(f"Emitted idea localization differs from the approved title: {idea_id}")
                modifiers = {}
                try:
                    modifier_block = _blocks(idea_block, "modifier")[0]
                    modifiers = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*=\s*(-?[0-9.]+)\s*$", modifier_block, re.M)}
                except IndexError:
                    pass
                expected_modifiers = {e["key"]: float(e["value"]) for e in n["offer"][side]["effects"] if e.get("kind") == "modifier"}
                if modifiers != expected_modifiers:
                    raise ValueError(f"Emitted idea modifiers differ from the approved terms: {idea_id}: {modifiers} != {expected_modifiers}")
                for effect in (side_effects if n["key"] in added else []):
                    if effect.get("kind") in {"treasury_gdp", "weekly_gdp_expense", "weekly_transfer"}:
                        literal = effect.get("runtime_share_literal")
                        emitted_multipliers = [float(v) for v in re.findall(r"\bmultiply\s*=\s*(-?[0-9.]+)", preview_provider)]
                        if literal and not any(abs(v - float(literal)) < 0.000000001 for v in emitted_multipliers):
                            raise ValueError(f"Emitted numeric provider is missing approved share {literal} for {n['key']} / {side}")
                        if effect.get("kind") != "treasury_gdp" and f"divide = {effect.get('divisor', 52)}" not in preview_provider:
                            raise ValueError(f"Emitted weekly provider is missing its approved divisor for {n['key']} / {side}")
                    elif effect.get("kind") == "building":
                        state = str(effect["state"])
                        pattern = rf"(?s){state}\s*=\s*\{{\s*add_extra_state_shared_building_slots\s*=\s*{effect['slots']}.*?type\s*=\s*{re.escape(effect['building'])}\s+level\s*=\s*{effect['amount']}"
                        if not re.search(pattern, preview_provider):
                            raise ValueError(f"Emitted offer provider building/slot data differs for {n['key']} / {side}")
                    elif effect.get("kind") == "research":
                        if f"category = {effect['category']}" not in preview_provider or f"bonus = {effect['bonus']}" not in preview_provider or f"uses = {effect['uses']}" not in preview_provider:
                            raise ValueError(f"Emitted offer provider research differs for {n['key']} / {side}")
    tile_layout_applied = False
    by_key = {node["key"]: node for node in nodes}
    resolved: dict[str, tuple[int, int]] = {}
    resolving: set[str] = set()
    def resolve(key: str) -> tuple[int, int]:
        if key in resolved:
            return resolved[key]
        if key in resolving:
            raise ValueError(f"Relative-position cycle detected at {key}")
        node = by_key[key]
        resolving.add(key)
        anchor = node.get("anchor")
        if anchor:
            anchor_key = anchor.removeprefix("COLDWAR_FRA2_")
            if anchor_key not in by_key:
                raise ValueError(f"Missing relative-position anchor {anchor_key} for {key}")
            offset = node.get("offset")
            if not offset or len(offset) != 2:
                raise ValueError(f"Invalid relative-position offset for {key}")
            parent = resolve(anchor_key)
            point = (parent[0] + offset[0], parent[1] + offset[1])
        else:
            point = (node["x"], node["y"])
            if node.get("offset") and tuple(node["offset"]) != point:
                raise ValueError(f"Absolute root offset disagrees with coordinates for {key}")
        resolving.remove(key)
        resolved[key] = point
        if point != (node["x"], node["y"]):
            raise ValueError(f"Resolved relative position differs for {key}: {point} != {(node['x'], node['y'])}")
        return point
    for key in by_key:
        resolve(key)
    for node in nodes:
        node["title"] = loc.get(node["id"], node.get("title", node["id"]))
        node["full_title"] = node["title"]
        node["description"] = loc.get(node["id"] + "_desc", node.get("description", ""))
        node.setdefault("id", "COLDWAR_FRA2_" + node["key"])
        node.setdefault("icon", "GFX_focus_unavailable")
        node.setdefault("title", node.get("full_title") or node["title"])
        if node["icon"] not in registry:
            raise ValueError(f"Focus icon sprite missing from current project .gfx: {node['icon']} ({node['key']})")
        if "description" not in node or "title" not in node:
            raise ValueError(f"Proposal focus lacks English display text: {node['key']}")
        if node.get("offer"):
            for side in ("france", "recipient"):
                for effect in node["offer"][side].get("effects", []): compact_effect(effect)
        for effect in node.get("effects", []): compact_effect(effect)

    design["emitted_shortcuts"] = []
    for shortcut in design.get("navigation", {}).get("shortcuts", []):
        target = shortcut.get("focus", "").removeprefix("COLDWAR_FRA2_")
        target_node = by_key.get(target)
        if target_node:
            design["emitted_shortcuts"].append({"group": target_node["group"], "target": target_node["id"], "label": shortcut["name"]})
    for group_id, (center, entry_y, _) in TILE_LAYOUT.items():
        entry = next(node for node in nodes if node["key"] == "fp_" + group_id)
        group = next(g for g in design["groups"] if g["id"] == group_id)
        design["emitted_shortcuts"].append({"group": group_id, "target": entry["id"], "label": group["title"]})
    for group in design["groups"]:
        if group["id"] == "diplomacy":
            group["title"] = "Partnerships by Consent"
    design["navigation"] = dict(design.get("navigation", {}), initial_focus="fp_niger_rights", preview_section="african_finance")

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
        "foreign_policy": {"added_focus_keys": sorted(added), "source_sha256": approved_hash},
        "pressure": pressure,
        "preview_layout": {"type": "compact 2x2 foreign-policy chapters", "preview_only_override_applied": tile_layout_applied, "chapter_centres": {group: [data[0], data[1]] for group, data in TILE_LAYOUT.items()}, "entry_rows": [14, 19], "offer_rows": [15, 17, 20, 22]},
        "emitted_shortcuts": design.get("emitted_shortcuts", []),
    }
    node_fields = ("key", "group", "title", "full_title", "description", "x", "y", "icon", "days", "prerequisites", "exclusions", "conditions", "effects", "spirit_name", "anchor", "offset")
    for node in nodes:
        item = {key: node[key] for key in node_fields if key in node}
        item["effects"] = [compact_effect(effect) for effect in node.get("effects", [])]
        item["asset_requirements"] = list(node.get("asset_requirements", []))
        if node.get("spirit"):
            item["spirit_title"] = loc.get(node["spirit"], node.get("spirit_name", node["spirit"]))
        if node.get("offer"):
            offer = node["offer"]
            for effect in item["effects"]:
                if effect.get("kind") == "unlock_decision":
                    effect["label"] = f"{offer.get('partner_name', 'Partner')} approval for {node['title']}"
            item["offer"] = {key: offer[key] for key in ("partner_name", "partner", "activation_conditions", "acceptance_conditions") if key in offer}
            for side_name in ("france", "recipient"):
                side = offer[side_name]
                item["offer"][side_name] = {
                    "spirit": side["spirit"],
                "title": loc.get(side["spirit"], side.get("name", side["spirit"])),
                    "effects": [compact_effect(effect) for effect in side["effects"]],
                }
            for key in ("requirements", "asset_requirements", "activation_conditions", "acceptance_conditions", "delivery", "no_expiry"):
                if key in offer and key not in item["offer"]: item["offer"][key] = offer[key]
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
    design_gzip = base64.b64encode(gzip.compress(json.dumps(compact, ensure_ascii=False, separators=(",", ":")).encode("utf-8"), compresslevel=9, mtime=0)).decode("ascii")
    fragment = template.replace("__DESIGN__", design_gzip)
    fragment = fragment.replace("__ART__", json.dumps(art, ensure_ascii=False, separators=(",", ":")))
    fragment = fragment.replace("    const shortcutLabels=", "    for(const n of D.nodes)A[n.key]=A[n.icon];\n    const shortcutLabels=")
    if "__DESIGN__" in fragment or "__ART__" in fragment or "__LOC__" in fragment:
        raise ValueError("Preview template placeholders were not fully replaced")
    encoded = fragment.encode("utf-8")
    if len(encoded) >= 1_000_000:
        raise ValueError(f"Inline preview exceeds 1,000,000 bytes: {len(encoded)} bytes")
    VIZ.mkdir(parents=True, exist_ok=True)
    (VIZ / "france-foreign-policy.html").write_bytes(encoded)
    full = "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>France 1970 National Focus</title><style>body{margin:0;background:#151916}</style></head><body>" + fragment + "</body></html>"
    (HERE / "PREVIEW.html").write_bytes(full.encode("utf-8"))
    report = {
        "project": PROJECT,
        "kind": "Installed-source preview from the emitted runtime design, focus AST, English localization, GFX aliases and offer providers; not an HOI4 engine screenshot",
        "focus_count": len(nodes),
        "section_count": len(design["groups"]),
        "offer_count": sum(bool(n.get("offer")) for n in nodes),
        "starting_spirit_count": len(design.get("starting_spirits", [])),
        "recovery_stage_count": len(design.get("recovery_stages", [])),
        "spirit_transition_count": sum(1 for n in nodes for effect in n.get("effects", []) if effect.get("kind") == "transition_spirit"),
        "foreign_policy_added_focus_count": len(added),
        "preview_layout_override_applied": tile_layout_applied,
        "standalone_slot_reward_count": sum(1 for n in nodes for effect in n.get("effects", []) if effect.get("kind") == "state_slots"),
        "localisation_count": len(loc),
        "emitted_sprite_count": len(registry),
        "used_icon_textures": len({registry[n["icon"]] for n in nodes}),
        "converted_texture_count": len(art_cache) // 2,
        "png_dimensions": {key.removesuffix("#size"): value for key, value in art_cache.items() if key.endswith("#size")},
        "fragment_bytes": len(encoded),
        "art_source": "Current project GFX aliases and current MD native focus titlebar declarations; DDS to pixel-verified lossless RGBA PNG or WebP, no scaling",
        "approved_input_sha256": approved_hash,
        "runtime_design_sha256": hashlib.sha256(BASELINE_PATH.read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "source_sha256": source_hashes,
        "pressure_source_sha256": pressure_generator_hash,
        "pressure_contracts_sha256": pressure_config_hash,
        "native_ast_crosscheck": {"emitted_focus_count": len(focus_ast), "approved_foreign_node_count": len(added), "authorized_balance_overlay": "tools/france_1970_runtime/deal_balance_revision.py", "normalized_runtime_node_field_mismatches": 0, "coordinates_prerequisites_exclusions_icons_costs_checked": True, "availability_triggers_and_tooltip_localisation_checked": True, "completion_and_offer_providers_checked": True, "offer_numeric_tooltips_and_cost_literals_checked": True, "offer_buildings_slots_and_research_checked": True, "agreement_idea_titles_and_modifiers_checked": True},
        "deal_balance_revision": {
            "removed_negative_corporate_tax_rows": len(expected_runtime.get("deal_balance_revision", {}).get("removed_negative_agreement_tax_modifiers", [])),
            "french_doctrine_changes": len(expected_runtime.get("deal_balance_revision", {}).get("french_land_doctrine_changes", [])),
            "removed_french_doctrine_nodes": sorted(__import__("deal_balance_revision").REMOVED_FRENCH_DOCTRINE),
            "removed_negative_corporate_tax_focuses": sorted({row["focus"] for row in expected_runtime.get("deal_balance_revision", {}).get("removed_negative_agreement_tax_modifiers", [])}),
        },
        "pressure_preview_crosscheck": {
            "partners": len(pressure["partners"]),
            "send_accept_refuse_decision_sets": len(pressure["partners"]),
            "active_aid_payment_rows": sum(len(p["aid_rows"]) for p in pressure["partners"]),
            "charter_idea_modifier_sets": 2 * len(pressure["partners"]),
            "withdrawal_crisis_idea_modifier_set": True,
            "decision_titles_requirements_tooltips_and_30_day_event_deadlines_checked": True,
            "weekly_payment_provider_inventory_matches_runtime_offers": True,
        },
        "design_sha256": hashlib.sha256(BASELINE_PATH.read_bytes()).hexdigest(),
        "build_hash": hashlib.sha256(encoded).hexdigest(),
    }
    (HERE / "PREVIEW_BUILD.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return full, report


if __name__ == "__main__":
    _, result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2))
