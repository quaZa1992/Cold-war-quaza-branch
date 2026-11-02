# IMPERIA COLD WAR — Reverse this dated-history addition for earlier preservation audits.
from pathlib import Path
import hashlib
import json
from history_patch import BEGIN, strip_profile

HERE = Path(__file__).resolve().parent


def reverse_history_extension(name, raw):
    name = str(name).replace("\\", "/")
    if not name.startswith("history/countries/"):
        return raw
    text = raw.decode("utf-8")
    if BEGIN not in text:
        return raw
    records = json.loads((HERE / "inventory.json").read_text(encoding="utf-8"))["countries"]
    expected = next((r["sha256"] for r in records if r["path"] == name), None)
    if expected is None:
        raise AssertionError("Unrecorded history extension: " + name)
    before = strip_profile(text).encode("utf-8")
    assert hashlib.sha256(before).hexdigest() == expected, "History preimage changed: " + name
    return before
