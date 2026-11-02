# IMPERIA COLD WAR — guarded rollback of the Cayo Blanco del Sur addition.
"""Default: inspect only. --apply restores this feature, refusing unrelated edits."""
import argparse
import json
import shutil
from build import ROOT, BACKUP, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((BACKUP / "manifest.json").read_text())
    outputs = manifest["installed_outputs_sha256"]
    new = set(manifest["new_runtime_paths"])
    for rel, installed in outputs.items():
        path = (ROOT / rel).resolve()
        assert path.is_relative_to(ROOT.resolve()), f"Path outside mod: {path}"
        original = manifest["files"].get(rel, {}).get("sha256")
        if path.exists():
            assert digest(path.read_bytes()) in (installed, original), f"Unrelated later edit: {rel}"
        else:
            assert rel in new, f"Missing original file: {rel}"
        if rel not in new:
            assert digest((BACKUP / rel).read_bytes()) == original, f"Damaged backup: {rel}"
    if args.apply:
        for rel in outputs:
            path = (ROOT / rel).resolve()
            if rel in new:
                if path.exists():
                    path.unlink()
            else:
                shutil.copyfile(BACKUP / rel, path)
    print(json.dumps({"applied": args.apply, "restore_original_files": sorted(set(outputs) - new), "remove_only_feature_created_files": sorted(new)}, indent=2))


if __name__ == "__main__":
    main()
