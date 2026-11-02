# IMPERIA COLD WAR — Bounded legacy German trust retirement
"""Bounded removal of the legacy DDR 1985 trust meters.

Only the allow-listed files below are read or changed. The script can be run
with --apply repeatedly; once edits are applied, later runs validate the result.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
TRUST_LINE = re.compile(
    r"(?m)^[\t ]*[^\r\n]*\b(?:DDR_state_trust|DDR_moscow_trust)\b[^\r\n]*\r?\n"
)
FILES = (
    "common/scripted_effects/99_DDR_1985_state_crisis_effects.txt",
    "common/national_focus/ddr.txt",
    "common/national_focus/GER_1985.txt",
    "events/DDR_1985.txt",
    "common/scripted_effects/99_1985_western_pressure_effects.txt",
)
LOC_FILES = (
    "localisation/english/DDR_1985_expansion_l_english.yml",
    "localisation/english/mdcw_historical_ddr_state_crisis_l_english.yml",
)
MARKER = "# IMPERIA COLD WAR — 1985 DDR trust removal"
FORMULAS = {
    "DDR_state_crisis_stability_factor": (2600, (
        "set_variable = { DDR_state_crisis_stability_factor = 0 }",
        "add_to_variable = { DDR_state_crisis_stability_factor = DDR_sed_control }",
        "add_to_variable = { DDR_state_crisis_stability_factor = DDR_nva_loyalty }",
        "subtract_from_variable = { DDR_state_crisis_stability_factor = DDR_reform_pressure }",
        "subtract_from_variable = { DDR_state_crisis_stability_factor = DDR_emigration_pressure }",
        "subtract_from_variable = { DDR_state_crisis_stability_factor = DDR_mass_protest_pressure }",
        "subtract_from_variable = { DDR_state_crisis_stability_factor = DDR_supply_pressure }")),
    "DDR_state_crisis_drift_defence_factor": (1100, (
        "set_variable = { DDR_state_crisis_drift_defence_factor = DDR_sed_control }",
        "add_to_variable = { DDR_state_crisis_drift_defence_factor = DDR_stasi_penetration }",
        "subtract_from_variable = { DDR_state_crisis_drift_defence_factor = DDR_west_media_penetration }",
        "subtract_from_variable = { DDR_state_crisis_drift_defence_factor = DDR_west_dependency }")),
    "DDR_state_crisis_communism_drift": (2600, (
        "set_variable = { DDR_state_crisis_communism_drift = DDR_sed_control }",
        "subtract_from_variable = { DDR_state_crisis_communism_drift = DDR_reform_pressure }")),
    "DDR_state_crisis_nationalist_drift": (2400, (
        "set_variable = { DDR_state_crisis_nationalist_drift = DDR_nva_loyalty }",
        "add_to_variable = { DDR_state_crisis_nationalist_drift = DDR_border_crisis_pressure }",
        "add_to_variable = { DDR_state_crisis_nationalist_drift = DDR_emigration_pressure }")),
    "DDR_state_crisis_resistance_growth": (2000, (
        "set_variable = { DDR_state_crisis_resistance_growth = DDR_reform_pressure }",
        "add_to_variable = { DDR_state_crisis_resistance_growth = DDR_mass_protest_pressure }",
        "add_to_variable = { DDR_state_crisis_resistance_growth = DDR_emigration_pressure }",
        "add_to_variable = { DDR_state_crisis_resistance_growth = DDR_youth_unrest }",
        "subtract_from_variable = { DDR_state_crisis_resistance_growth = DDR_stasi_penetration }")),
    "DDR_state_crisis_productivity_growth_modifier": (2200, (
        "set_variable = { DDR_state_crisis_productivity_growth_modifier = 0 }",
        "add_to_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_west_dependency }",
        "add_to_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_ko_ko_funds }",
        "subtract_from_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_supply_pressure }",
        "subtract_from_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_sed_control }",
        "subtract_from_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_emigration_pressure }")),
    "DDR_state_crisis_bureaucracy_cost_multiplier_modifier": (2200, (
        "set_variable = { DDR_state_crisis_bureaucracy_cost_multiplier_modifier = DDR_sed_control }",
        "add_to_variable = { DDR_state_crisis_bureaucracy_cost_multiplier_modifier = DDR_supply_pressure }")),
    "DDR_state_crisis_war_support_factor": (2400, (
        "set_variable = { DDR_state_crisis_war_support_factor = DDR_nva_loyalty }",
        "add_to_variable = { DDR_state_crisis_war_support_factor = DDR_border_crisis_pressure }")),
    "DDR_state_crisis_army_org_factor": (2200, (
        "set_variable = { DDR_state_crisis_army_org_factor = DDR_nva_loyalty }",
        "subtract_from_variable = { DDR_state_crisis_army_org_factor = DDR_regime_panic }")),
}


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw[3:].decode("utf-8") if bom else raw.decode("utf-8"), bom


def write_text(path: Path, value: str, bom: bool) -> None:
    data = value.encode("utf-8")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + data)


def transform_effects(text: str) -> str:
    # Preserve each original divisor and independent input. The two formulas
    # initialized from a trust meter instead reset to zero before adding inputs.
    text = text.replace(
        "\tset_variable = { DDR_state_crisis_stability_factor = DDR_state_trust }\r\n",
        "\tset_variable = { DDR_state_crisis_stability_factor = 0 }\r\n",
    ).replace(
        "\tset_variable = { DDR_state_crisis_productivity_growth_modifier = DDR_state_trust }\r\n",
        "\tset_variable = { DDR_state_crisis_productivity_growth_modifier = 0 }\r\n",
    )
    text = TRUST_LINE.sub("", text)
    text = re.sub(
        r"(?m)^[\t ]*# IMPERIA COLD WAR — 1985 DDR trust removal: recenter removed start values \(44/78\)\.\r?\n"
        r"[\t ]*add_to_variable = \{ DDR_state_crisis_[A-Za-z0-9_]+ = -?\d+ \}\r?\n",
        "",
        text,
    )
    return text


def transform_header(text: str, marker: str) -> str:
    lines = text.splitlines(keepends=True)
    if marker in "".join(lines[:8]):
        return text
    for index, line in enumerate(lines[:8]):
        if line.startswith("# IMPERIA CW —"):
            ending = "\r\n" if line.endswith("\r\n") else "\n"
            lines[index] = marker + ending
            return "".join(lines)
    return marker + "\n" + text


def transform_localisation(text: str) -> str:
    target = ' DDR_1985_state_crisis_dynamic_modifier_desc: "State trust, SED control, Stasi penetration, reform pressure, West dependency, Moscow trust, emigration pressure and NVA loyalty define how brittle the republic really is."'
    replacement = ' DDR_1985_state_crisis_dynamic_modifier_desc: "SED control, Stasi penetration, reform pressure, West dependency, emigration pressure and NVA loyalty define how brittle the republic really is."'
    if target in text:
        text = text.replace(target, replacement, 1)
    if replacement not in text:
        raise ValueError("Expected localized dynamic modifier description missing")
    if MARKER not in text:
        newline = "\r\n" if "\r\n" in text else "\n"
        needle = replacement + newline
        text = text.replace(needle, MARKER + newline + needle, 1)
    return text


def validate() -> list[str]:
    errors: list[str] = []
    for relative in FILES:
        path = ROOT / relative
        text, bom = read_text(path)
        if bom:
            errors.append(f"script unexpectedly has UTF-8 BOM: {relative}")
        if "DDR_state_trust" in text or "DDR_moscow_trust" in text:
            errors.append(f"legacy trust token remains: {relative}")
        if "# IMPERIA COLD WAR —" not in text[:600]:
            errors.append(f"exact project marker missing at file header: {relative}")
        if relative.endswith("99_DDR_1985_state_crisis_effects.txt"):
            start = text.find("DDR_1985_update_state_crisis_values = {")
            end = text.find("\n}", start)
            formula_text = text[start:end] if start >= 0 and end >= 0 else ""
            if not formula_text:
                errors.append("derived state-crisis formula block is missing")
            for variable, (divisor, terms) in FORMULAS.items():
                expected = [*terms, f"divide_variable = {{ {variable} = {divisor} }}"]
                missing = [term for term in expected if term not in formula_text]
                if missing:
                    errors.append(f"independent input or divisor missing for {variable}: {missing[0]}")
            if "recenter removed start values" in formula_text or re.search(
                r"(?m)^[\t ]*add_to_variable = \{ DDR_state_crisis_[A-Za-z0-9_]+ = -?\d+ \}",
                formula_text,
            ):
                errors.append("fixed trust recenter offset remains in derived formulas")
    for relative in LOC_FILES:
        path = ROOT / relative
        text, bom = read_text(path)
        if not bom:
            errors.append(f"localisation missing UTF-8 BOM: {relative}")
        if "State trust" in text or "Moscow trust" in text:
            errors.append(f"removed meter description remains: {relative}")
        if MARKER not in text:
            errors.append(f"exact project marker missing: {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="apply allow-listed transforms")
    args = parser.parse_args()
    if args.apply:
        for relative in FILES:
            path = ROOT / relative
            text, bom = read_text(path)
            if relative.endswith("99_DDR_1985_state_crisis_effects.txt"):
                text = transform_effects(text)
            else:
                text = TRUST_LINE.sub("", text)
            text = transform_header(text, MARKER)
            current, _ = read_text(path)
            if text != current:
                write_text(path, text, bom)
        for relative in LOC_FILES:
            path = ROOT / relative
            text, bom = read_text(path)
            transformed = transform_localisation(text)
            if transformed != text:
                write_text(path, transformed, bom)
    errors = validate()
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: bounded 1985 DDR trust removal validation")
    print(f"Allow-listed script files checked: {len(FILES)}")
    print(f"BOM-preserving localisation files checked: {len(LOC_FILES)}")
    print("1970 files and GUI are outside this transform's allowlist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
