# IMPERIA COLD WAR — Brazil 1970 art asset integration generator
"""Install Brazil 1970 icon aliases and native framed event art.

Run from the mod root with the project's Python runtime. Outputs are deterministic
and derived only from the frozen, approval-hash-checked design and existing assets.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/south_america_event_art'))
from sa_photo_catalogue import BRAZIL, ASSET_DIR
from sa_photo_export import build_assets
RUNTIME = ROOT / "tools/brazil_1970_runtime"
DESIGN = RUNTIME / "approved_design.json"
APPROVAL = RUNTIME / "APPROVAL.json"
OUT_GFX = ROOT / "interface/COLDWAR_BRA_1970.gfx"
MANIFEST = RUNTIME / "art_manifest.json"
FOCUS_ART = RUNTIME / "focus_art_polish.json"

EVENT_SOURCES = {key:f'{ASSET_DIR}/{asset}.dds' for key,asset in BRAZIL.items()}

SPIRIT_SOURCES = {
    "COLDWAR_BRA_ai5": "gfx/interface/ideas/brazil/BRA_idea_new_military_regime.dds",
    "COLDWAR_BRA_miracle": "gfx/interface/ideas/Imp_Coldwar_General/MilitaryIndustrialComplex_v2.dds",
    "COLDWAR_BRA_wage_squeeze": "gfx/interface/ideas/internal_factions/labour_unions.dds",
    "COLDWAR_BRA_skills": "gfx/interface/ideas/brazil/mercosur_education.dds",
    "COLDWAR_BRA_land_inequality": "gfx/interface/ideas/brazil/BRA_idea_amazon_deforestation.dds",
    "COLDWAR_BRA_urban_pressure": "gfx/interface/ideas/economy/economy_housing.dds",
    "COLDWAR_BRA_oil_exposure": "gfx/interface/ideas/oil/imp_oil_crisis.dds",
    "COLDWAR_BRA_amazon_pressure": "gfx/interface/ideas/brazil/rainforest.dds",
}

GROUP_SOURCES = {
    "military": "gfx/interface/goals/brazil/brazilian_armed_forces.dds",
    "arena": "gfx/interface/ideas/brazil/BRA_idea_nationalism_rise.dds",
    "mdb": "gfx/interface/goals/brazil/BRA_mdb.dds",
    "ptb": "gfx/interface/ideas/internal_factions/labour_unions.dds",
    "pdt": "gfx/interface/goals/brazil/BRA_brazsocdem.dds",
    "pt": "gfx/interface/goals/brazil/workers_party.dds",
    "pfl": "gfx/interface/goals/brazil/BRA_brazneolib.dds",
    "psdb": "gfx/interface/goals/brazil/psdb_focus.dds",
    "pcb": "gfx/interface/ideas/internal_factions/communist_cadres.dds",
    "pcdob": "gfx/interface/ideas/ideology/communism.dds",
    "populist": "gfx/interface/goals/brazil/BRA_brazilian_populist_republic.dds",
    "prn": "gfx/interface/ideas/brazil/BRA_idea_plano_real.dds",
    "ptb_late": "gfx/interface/ideas/brazil/BRA_idea_empowered_pt.dds",
    "society": "gfx/interface/ideas/brazil/BRA_idea_1988_democratic_constitution.dds",
    "economy": "gfx/interface/ideas/brazil/BRA_idea_nationalized_industries.dds",
    "energy": "gfx/interface/goals/00_economy/companies/BRA_petrobras_oil_benefits.dds",
    "defence": "gfx/interface/ideas/Imp_Coldwar_General/MilitaryIndustrialComplex_v2.dds",
    "diplomacy": "gfx/interface/goals/brazil/BRA_Itamaraty.dds",
}


def checked_design() -> dict:
    approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
    digest = hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    if digest != approval["approved_sha256"]:
        raise RuntimeError(f"Frozen design hash mismatch: {digest}")
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if len(design["nodes"]) != 224 or len(design["events"]) != 8:
        raise RuntimeError("Unexpected approved design scope")
    if {g["id"] for g in design["groups"]} != set(GROUP_SOURCES):
        raise RuntimeError("Group idea art keys do not match frozen design")
    if {s["id"] for s in design["starting_spirits"]} != set(SPIRIT_SOURCES):
        raise RuntimeError("Starting spirit art keys do not match frozen design")
    if {e["id"].removeprefix("COLDWAR_BRA_") for e in design["events"]} != set(EVENT_SOURCES) - {"agreement_notice"}:
        raise RuntimeError("Event art keys do not match frozen design")
    return design


def focus_icon_sources(icons: set[str]) -> dict[str, str]:
    text = (ROOT / "interface/goals.gfx").read_text(encoding="utf-8-sig")
    pairs = re.findall(r'name\s*=\s*"([^"\n]+)"\s*texturefile\s*=\s*"([^"]+)"', text)
    native = dict(pairs)
    missing = sorted(icons - native.keys())
    if missing:
        raise RuntimeError(f"Native focus icon textures not found: {missing}")
    return {key: native[key] for key in sorted(icons)}


def all_focus_icon_sources() -> dict[str, str]:
    text = (ROOT / "interface/goals.gfx").read_text(encoding="utf-8-sig")
    pairs = re.findall(r'name\s*=\s*"([^"\n]+)"\s*texturefile\s*=\s*"([^"\n]+)"', text)
    return dict(pairs)


def checked_focus_art(design: dict) -> dict[str, dict]:
    """Validate explicit focus art overrides against the approved node set and native sprite registry."""
    data = json.loads(FOCUS_ART.read_text(encoding="utf-8"))
    if data.get("project") != "IMPERIA COLD WAR":
        raise RuntimeError("Focus art mapping is missing its project marker")
    native = all_focus_icon_sources()
    nodes = {node["id"] for node in design["nodes"]}
    overrides = data.get("focus_icon_overrides", {})
    if not isinstance(overrides, dict):
        raise RuntimeError("focus_icon_overrides must be an object")
    for focus_id, item in overrides.items():
        if focus_id not in nodes:
            raise RuntimeError(f"Focus art override references unknown focus: {focus_id}")
        icon = item.get("native_icon")
        if icon not in native:
            raise RuntimeError(f"Focus art override has no native sprite: {focus_id} -> {icon}")
        if item.get("source_texture") != native[icon]:
            raise RuntimeError(f"Focus art donor path drift for {focus_id}: {item.get('source_texture')} != {native[icon]}")
        if not item.get("semantic"):
            raise RuntimeError(f"Focus art override has no semantic rationale: {focus_id}")
    return overrides


def write_idea_icon(source: Path, target: Path) -> None:
    with Image.open(source) as original:
        image = original.convert("RGBA")
    image.thumbnail((116, 116), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((128 - image.width) // 2, (128 - image.height) // 2))
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, format="DDS")
    with Image.open(target) as check:
        if check.size != (128, 128) or check.mode != "RGBA":
            raise RuntimeError(f"Idea output failed 128x128 RGBA check: {target}")


def install() -> dict:
    build_assets(ROOT)
    design = checked_design()
    art_overrides = checked_focus_art(design)
    # Retain original aliases for approved and archived renders; add only sprites
    # selected by the polish map, rather than registering every MD focus sprite.
    goal_icons = {node["icon"] for node in design["nodes"]}
    goal_icons.update(item["native_icon"] for item in art_overrides.values())
    goal_sources = focus_icon_sources(goal_icons)

    event_outputs = {}
    for key, relative in EVENT_SOURCES.items():
        source = ROOT / relative
        target = ROOT / f"gfx/event_pictures/COLDWAR_BRA_1970/{key}.dds"
        with Image.open(source) as image:
            if image.size != (217, 163):
                raise RuntimeError(f"Event donor must be the inspected 217x163 frame: {relative}={image.size}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        event_outputs[key] = target.relative_to(ROOT).as_posix()

    idea_outputs = {}
    for spirit, relative in SPIRIT_SOURCES.items():
        source = ROOT / relative
        target = ROOT / f"gfx/interface/ideas/COLDWAR_BRA_1970/{spirit}.dds"
        write_idea_icon(source, target)
        idea_outputs[spirit] = target.relative_to(ROOT).as_posix()

    group_outputs = {}
    for group, relative in GROUP_SOURCES.items():
        source = ROOT / relative
        target = ROOT / f"gfx/interface/ideas/COLDWAR_BRA_1970/COLDWAR_BRA_group_{group}.dds"
        write_idea_icon(source, target)
        group_outputs[group] = target.relative_to(ROOT).as_posix()

    lines = [
        "# IMPERIA COLD WAR — Brazil 1970 art sprite aliases",
        "spriteTypes = {",
    ]
    for icon, texture in goal_sources.items():
        for suffix in ("", "_shine"):
            name = f"COLDWAR_BRA_focus_{icon}{suffix}"
            if suffix:
                lines.extend([
                    "\tspriteType = {",
                    f'\t\tname = "{name}"',
                    f'\t\ttexturefile = "{texture}"',
                    '\t\teffectfile = "gfx/FX/buttonstate.lua"',
                    "\t\tanimation = {",
                    f'\t\t\tanimationmaskfile = "{texture}"',
                    '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                    "\t\t\tanimationrotation = -90.0",
                    "\t\t\tanimationlooping = no",
                    "\t\t\tanimationtime = 0.75",
                    "\t\t\tanimationdelay = 0",
                    '\t\t\tanimationblendmode = "add"',
                    '\t\t\tanimationtype = "scrolling"',
                    "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
                    "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }",
                    "\t\t}",
                    "\t\tanimation = {",
                    f'\t\t\tanimationmaskfile = "{texture}"',
                    '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                    "\t\t\tanimationrotation = 90.0",
                    "\t\t\tanimationlooping = no",
                    "\t\t\tanimationtime = 0.75",
                    "\t\t\tanimationdelay = 0",
                    '\t\t\tanimationblendmode = "add"',
                    '\t\t\tanimationtype = "scrolling"',
                    "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
                    "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }",
                    "\t\t}",
                    "\t\tlegacy_lazy_load = no",
                    "\t}",
                ])
            else:
                lines.extend([
                    "\tspriteType = {",
                    f'\t\tname = "{name}"',
                    f'\t\ttexturefile = "{texture}"',
                    "\t\tlegacy_lazy_load = no",
                    "\t}",
                ])
    for key, relative in event_outputs.items():
        lines.append(f'\tspriteType = {{ name = "GFX_COLDWAR_BRA_event_{key}" texturefile = "{relative}" legacy_lazy_load = no }}')
    for spirit, relative in idea_outputs.items():
        lines.append(f'\tspriteType = {{ name = "GFX_idea_{spirit}" texturefile = "{relative}" legacy_lazy_load = no }}')
    for group, relative in group_outputs.items():
        lines.append(f'\tspriteType = {{ name = "GFX_idea_COLDWAR_BRA_group_{group}" texturefile = "{relative}" legacy_lazy_load = no }}')
    lines.append("}")
    OUT_GFX.parent.mkdir(parents=True, exist_ok=True)
    OUT_GFX.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    manifest = {
        "project": "IMPERIA COLD WAR",
        "feature": "Brazil 1970 art integration",
        "approved_design_sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest(),
        "focus_icon_prefix": "COLDWAR_BRA_focus_",
        "focus_icons": {key: {"sprite": f"COLDWAR_BRA_focus_{key}", "shine_sprite": f"COLDWAR_BRA_focus_{key}_shine", "source_texture": path} for key, path in goal_sources.items()},
        "focus_art_overrides": art_overrides,
        "event_pictures": {key: {"sprite": f"GFX_COLDWAR_BRA_event_{key}", "asset": path} for key, path in event_outputs.items()},
        "event_photo_provenance": "tools/south_america_event_art/ASSET_NOTICE.md",
        "idea_icons": {key: {"picture": key, "sprite": f"GFX_idea_{key}", "asset": path} for key, path in idea_outputs.items()},
        "group_idea_icons": {key: {"picture": f"COLDWAR_BRA_group_{key}", "sprite": f"GFX_idea_COLDWAR_BRA_group_{key}", "asset": path} for key, path in group_outputs.items()},
        "native_event_window": {"full_size": [581, 427], "picture_position": [5, 226], "picture_size": [217, 163], "options_position": [215, 220], "options_size": [300, 30], "option_slot": [300, 47]},
        "native_photo_aperture": {"position": [19, 6], "size": [180, 150]},
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    result = install()
    print(f"Installed {len(result['focus_icons'])} focus aliases, {len(result['idea_icons'])} starting ideas, {len(result['group_idea_icons'])} group ideas and {len(result['event_pictures'])} event pictures.")
