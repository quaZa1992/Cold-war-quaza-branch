# IMPERIA COLD WAR — Targeted foreign-focus integration review.
"""Read-only checks for the Cyprus guarantor focus output and host footprints."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = Path(__file__).with_name("foreign_focuses.py")
DESIGN = ROOT / "docs/cyprus_1970_rework_20261027/concept.json"
OUTPUT = ROOT / "common/national_focus/COLDWAR_CYP_R2_guarantor_focuses.txt"


def _load_generator() -> Any:
    spec = importlib.util.spec_from_file_location("cyprus_foreign_focuses", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import foreign focus generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _blocks(text: str) -> list[str]:
    lines = text.splitlines()
    result: list[str] = []
    index = 0
    while index < len(lines):
        if not re.match(r"^shared_focus\s*=\s*\{", lines[index]):
            index += 1
            continue
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
        result.append("\n".join(block))
    return result


def review() -> dict[str, Any]:
    generator = _load_generator()
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    generated = generator.build(design)
    expected_text = generated["files"][generator.OUTPUT]
    localization = generated["loc"]
    if len(localization) != 32:
        raise ValueError(f"Expected 32 English focus localization keys, got {len(localization)}")
    if any("—" in value or "–" in value for value in localization.values()):
        raise ValueError("Focus localization contains an en dash or em dash")
    if not OUTPUT.exists():
        raise FileNotFoundError(OUTPUT)
    raw = OUTPUT.read_bytes()
    actual_text = raw.decode("utf-8-sig")
    blocks = _blocks(actual_text)
    ids = [re.search(r"(?m)^\s*id\s*=\s*(\S+)", block).group(1) for block in blocks]
    expected_ids = generated["meta"]["focus_ids"]
    if len(blocks) != 16 or set(ids) != set(expected_ids) or len(set(ids)) != 16:
        raise ValueError(f"Emitted focus IDs mismatch: found {len(ids)} blocks, expected 16")
    if raw.startswith(bytes.fromhex("efbbbf")):
        raise ValueError("Focus script has a UTF-8 BOM")
    if not actual_text.startswith("# IMPERIA COLD WAR"):
        raise ValueError("Focus output is missing its exact project marker")
    player_text = "\n".join(line for line in actual_text.splitlines() if not line.lstrip().startswith("#"))
    if "—" in player_text or "–" in player_text:
        raise ValueError("New focus output contains an en dash or em dash")
    if actual_text != expected_text:
        raise ValueError("Generated focus file differs from current design output")

    by_key = {actor["key"]: actor for actor in design["actor_focuses"]}
    by_id = {actor["id"]: actor for actor in design["actor_focuses"]}
    focus_records: list[dict[str, Any]] = []
    for block in blocks:
        focus_id = re.search(r"(?m)^\s*id\s*=\s*(\S+)", block).group(1)
        actor = by_id[focus_id]
        helper_key = actor["key"]
        expected_helpers = [
            f"COLDWAR_CYP_R2_ACT_{helper_key}_available = yes",
            f"COLDWAR_CYP_R2_ACT_{helper_key}_preview = yes",
            f"COLDWAR_CYP_R2_ACT_{helper_key}_apply = yes",
        ]
        if any(helper not in block for helper in expected_helpers):
            raise ValueError(f"Helper contract missing from {focus_id}")
        for key in actor.get("pre", []):
            if by_key[key]["id"] not in block:
                raise ValueError(f"Prerequisite missing from {focus_id}: {key}")
        for key in actor.get("exclusive", []):
            if by_key[key]["id"] not in block:
                raise ValueError(f"Exclusion missing from {focus_id}: {key}")
        if actor["tag"] in ("TUR", "ENG"):
            expected_gate = f"original_tag = {actor['tag']}"
            if expected_gate not in block or "IMP_is_1970_scenario = yes" not in block:
                raise ValueError(f"Country-scoped generic-host gate missing from {focus_id}")
        focus_records.append({"id": focus_id, "tag": actor["tag"], "key": helper_key})

    attachments = generated["meta"]["host_attachments"]
    host_states = []
    for attach in attachments:
        path = ROOT / attach["host_path"]
        host_text = path.read_text(encoding="utf-8-sig")
        imports_missing = [
            focus_id for focus_id in attach["shared_focus_imports"]
            if f"shared_focus = {focus_id}" not in host_text
        ]
        host_states.append({
            "tag": attach["tag"],
            "tree_id": attach["tree_id"],
            "anchor": attach["anchor"],
            "anchor_present": bool(re.search(rf"(?m)^\s*id\s*=\s*{re.escape(attach['anchor'])}\s*$", host_text)),
            "imports_missing": imports_missing,
            "generator_path_present": (ROOT / attach["source_generator"]).exists(),
        })

    legacy = generated["meta"]["greece_legacy_retirement"]
    gre_text = (ROOT / legacy["source_tree"]).read_text(encoding="utf-8-sig")
    still_present = [focus_id for focus_id in legacy["focus_ids"] if f"id = {focus_id}" in gre_text]
    return {
        "project": "IMPERIA COLD WAR",
        "status": "reviewed source generation; host attachment is a separate integration patch",
        "focus_count": len(focus_records),
        "focuses": focus_records,
        "layout": generated["meta"]["layout_review"],
        "host_states": host_states,
        "legacy_greek_cyprus_focus_ids_remaining": still_present,
        "legacy_shortcut_keys_to_remove": legacy["shortcuts"],
        "generated_file_matches_design": True,
    }


if __name__ == "__main__":
    print(json.dumps(review(), indent=2))
