# IMPERIA CW — Cold War: canonical equilibrium launcher placement.
"""Place the equilibrium launcher in the native lower global-status row.

The original full-system generator cited by the imported files is absent from
this checkout. This bounded patch preserves its remaining authored interface.
Run after an external Cold War UI rebuild; --check performs no writes.
"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[2]
GUI = "interface/mdcw_cold_war.gui"
MARKER = "# IMPERIA CW — Cold War: equilibrium launcher in the lower global-status row."


def replace_once(text, pattern, replacement):
    result, count = re.subn(pattern, lambda match: replacement(match), text)
    if count != 1:
        raise ValueError(f"Expected one authored anchor, found {count}: {pattern}")
    return result


def render():
    files = {GUI: (ROOT / GUI).read_text(encoding="utf-8-sig")}
    gui = files[GUI]
    old_note = "# Topbar button, directly right of the Globalism counter (MD_money.gui, x = 1447, width 80)"
    if old_note in gui:
        gui = gui.replace(old_note, MARKER + "\n\t# Placement: tools/cold_war_ui/place_launcher.py; right anchor follows UI resolution.", 1)
    if MARKER not in gui:
        raise ValueError("Missing launcher ownership anchor")
    gui = replace_once(gui, r'(name = "mdcw_cw_topbar_container"\s*\n\s*)position = \{[^}]*\}(?:\n\s*orientation = upper_right)?',
                       lambda m: m[1] + "position = { x = -210 y = 88 }\n\t\torientation = upper_right")
    files[GUI] = gui

    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = render()
    for path, text in files.items():
        target = ROOT / path
        if args.check:
            if target.read_text(encoding="utf-8-sig") != text or target.read_bytes().startswith(b"\xef\xbb\xbf"):
                raise SystemExit("Placement differs: " + path)
        else:
            target.write_text(text, encoding="utf-8", newline="\n")
    print("Equilibrium launcher: right anchor (-210, 88), lower global-status row; authored controls preserved.")
