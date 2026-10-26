# IMPERIA CW — Cold War: europe 1970 — check original md reference.
"""Compare the read-only original MD EU reference with the reviewed baseline.

Run before future EU changes. This never writes to the Workshop installation.
Use --refresh only after reviewing changed native files and updating the mapping.
"""

from argparse import ArgumentParser
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/europe_1970_audit/original_md_reference_manifest.json"
DEFAULT_SOURCE = Path(r"E:\SteamLibrary\steamapps\workshop\content\394360\2777392649")
REFERENCE_FILES = (
    "interface/eu.gui",
    "interface/eu.gfx",
    "common/scripted_guis/01_european_union_guis.txt",
    "common/scripted_effects/99_eu_scripted_effects.txt",
    "common/scripted_effects/99_EU_voting_scripted_effects.txt",
    "common/scripted_triggers/99_EU_scripted_triggers.txt",
    "common/scripted_triggers/99_EU_voting_scripted_triggers.txt",
    "common/decisions/categories/EU_voting_categories.txt",
    "common/decisions/EU_voting_decisions.txt",
    "common/decisions/EU_USoE_decisions.txt",
    "common/decisions/EU_POTEF_decisions.txt",
    "events/EU_events.txt",
    "events/EU_news.txt",
    "events/EU_USoE_events.txt",
    "localisation/english/MD_focus_EU_l_english.yml",
    "localisation/english/MD_focus_EU_USoE_l_english.yml",
    "localisation/english/MD_focus_EU_POTEF_l_english.yml",
    "common/ideas/Organizations.txt",
    "common/on_actions/00_on_actions.txt",
    "common/on_actions/MD_on_actions.txt",
    "common/scripted_effects/00_money_system.txt",
)


def inspect(source):
    rows = []
    for relative in REFERENCE_FILES:
        path = source / relative
        if not path.is_file():
            rows.append({"path": relative, "missing": True})
            continue
        content = path.read_bytes()
        rows.append({
            "path": relative,
            "sha256": sha256(content).hexdigest(),
            "bytes": len(content),
            "lines": len(content.splitlines()),
        })
    return rows


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--refresh", action="store_true", help="Record reviewed source hashes in the mod workspace.")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_dir():
        parser.error(f"Original MD installation does not exist: {source}")
    if source == ROOT:
        parser.error("The original reference must not be the Cold War workspace.")
    observed = inspect(source)
    if args.refresh:
        missing = [row["path"] for row in observed if row.get("missing")]
        if missing:
            parser.error("Cannot refresh an incomplete reference: " + ", ".join(missing))
        payload = {
            "source": source.as_posix(),
            "reviewed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "read_only_reference": True,
            "review": "original_md_compatibility.md",
            "files": observed,
        }
        MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Recorded {len(observed)} reviewed reference hashes in {MANIFEST.relative_to(ROOT)}.")
        return 0
    if not MANIFEST.is_file():
        parser.error("No reviewed baseline exists. Review the original files before using --refresh.")
    baseline = json.loads(MANIFEST.read_text(encoding="utf-8"))
    known = {row["path"]: row for row in baseline["files"]}
    changed = []
    for row in observed:
        previous = known.get(row["path"])
        if row.get("missing"):
            changed.append(("MISSING", row["path"]))
        elif not previous:
            changed.append(("UNREVIEWED", row["path"]))
        elif row["sha256"] != previous["sha256"]:
            changed.append(("CHANGED", row["path"]))
    if changed:
        for status, relative in changed:
            print(f"{status}: {relative}")
        print("Review these original MD changes against the compatibility mapping; do not silently refresh.")
        return 1
    print(f"PASS: all {len(observed)} original MD reference files match the reviewed baseline; Workshop files were read only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
