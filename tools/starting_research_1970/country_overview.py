# IMPERIA COLD WAR — Worldwide January 1970 country review index
"""Generate a compact review index from authoritative historical input records."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROFILE_FILES = (
    "europe_profiles.json",
    "asia_profiles.json",
    "africa_profiles.json",
    "americas_oceania_profiles.json",
)
VARIANT_FILES = (
    "europe_variants.json",
    "asia_variants.json",
    "africa_variants.json",
    "americas_oceania_variants.json",
    "usa_variants.json",
)


def read(name: str) -> dict:
    data = json.loads((ROOT / name).read_text(encoding="utf-8-sig"))
    if data.get("project") != "IMPERIA COLD WAR":
        raise ValueError(f"Missing project identifier: {name}")
    return data


def cell(value: object) -> str:
    return str(value).replace("|", "&#124;").replace("\n", " ")


def main() -> None:
    profiles: dict[str, tuple[str, dict]] = {}
    designs: dict[str, tuple[str, list[str]]] = {}
    model_total = 0
    for name in PROFILE_FILES:
        for tag, profile in read(name)["countries"].items():
            if tag in profiles:
                raise ValueError(f"Duplicate research tag: {tag}")
            profiles[tag] = (name, profile)
    for name in VARIANT_FILES:
        data = read(name)
        model_total += len(data["models"])
        for tag, ids in data["countries"].items():
            if tag in designs:
                raise ValueError(f"Duplicate variant tag: {tag}")
            missing = set(ids) - data["models"].keys()
            if missing:
                raise ValueError(f"Unknown models for {tag}: {sorted(missing)}")
            designs[tag] = (name, ids)
    if set(profiles) != set(designs):
        raise ValueError("Research and design country coverage differ")
    if len(profiles) != 400:
        raise ValueError(f"Expected 400 history tags, found {len(profiles)}")
    assignment_total = sum(len(ids) for _, ids in designs.values())
    populated = sum(bool(ids) for _, ids in designs.values())
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "IMPERIA COLD WAR",
        "",
        "# Worldwide January 1970 country overview",
        "",
        f"Generated from authoritative regional inputs at {stamp} by `country_overview.py`.",
        f"Coverage: {len(profiles)} history tags; {model_total} design records; "
        f"{assignment_total} country-model assignments; {populated} tags with named designs.",
        "",
        "These are mod history tags, including dependent territories, conditional releases "
        "and entities that did not exist independently in 1970. They are not 400 sovereign "
        "states. An empty design list means no separately evidenced named package in this "
        "pass; it does not establish that a force had no weapons. The linked research "
        "record contains status, 22 sector ceilings, rationale, exact exceptions and exclusions.",
        "",
        "Model counts represent available design definitions, not deployed equipment or "
        "stockpile quantities. Open the linked variant input and find the tag in its "
        "`countries` object, then inspect the named models. This index is regenerated "
        "without changing any research, design or runtime input.",
        "",
        "Use [README](README.md) for the method and commands, [MODEL_INDEX](MODEL_INDEX.md) "
        "for physical fittings and native upgrade values, and the regional source "
        "registers for evidence and uncertainty. This index is not a test report.",
        "",
        "| Tag | Country or entity | Research record | Confidence | Named designs | Evidence register |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for tag in sorted(profiles):
        profile_file, profile = profiles[tag]
        design_file, ids = designs[tag]
        source_file = profile_file.replace("_profiles.json", "_sources.md")
        name = profile.get("name", tag)
        if name == "Venezula":
            name = "Venezuela"
        lines.append(
            f"| `{tag}` | {cell(name)} | [Profile]({profile_file}) | "
            f"{cell(profile.get('confidence', 'unspecified'))} | "
            f"[{len(ids)}]({design_file}) | [Sources]({source_file}) |"
        )
    (ROOT / "COUNTRY_OVERVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "project": "IMPERIA COLD WAR",
        "countries": len(profiles),
        "models": model_total,
        "assignments": assignment_total,
        "countries_with_designs": populated,
        "output": str(ROOT / "COUNTRY_OVERVIEW.md"),
    }))


if __name__ == "__main__":
    main()
